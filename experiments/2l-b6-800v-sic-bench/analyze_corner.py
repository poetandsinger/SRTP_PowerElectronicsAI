import numpy as np, sys, os, json

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plecs_runs")
# operating point (for Rg, Zb); override via argv JSON
op = {"Vg_rms":278.0,"Pr":300e3,"fac":200.0,"Ta":65.0}
if len(sys.argv) > 1:
    op.update(json.loads(sys.argv[1]))
Vg_rms, Pr, fac, Ta = op["Vg_rms"], op["Pr"], op["fac"], op["Ta"]
Zb = Vg_rms**2/Pr
Rg = 0.01*Zb

R_jc = 0.0948      # junction-to-case per switch (Cauer sum), C/W
# case-to-coolant per module (2 switches share baseplate), C/W.
# CRD-calibrated (S5): value that puts the rated 360A/300kW point at Tj=175C (CRD anchor).
# app-note guidance [168] gives ~0.08 (pessimistic); 0.070 reproduces the CRD 175C limit.
R_cs = float(os.environ.get("RCS", "0.070"))

def load(n):
    p=os.path.join(D,n); a=np.genfromtxt(p,delimiter=',');
    return a.reshape(1,-1) if a.ndim==1 else a

def tail(a,t0):     # rows with time>=t0
    return a[a[:,0]>=t0]

main=load("main.csv"); allc=load("all.csv"); allsw=load("allsw.csv")
tj=load("tj.csv"); pwr=load("pwr.csv"); hf=load("hf.csv")

Tend=main[-1,0]
# integer-cycle steady window: last 5 fundamental periods (25-50ms for 0.05s run)
Tcyc=1.0/fac
nwin=int((Tend*0.5)//Tcyc)          # whole cycles in second half
t0=Tend - nwin*Tcyc
print(f"steady window: {t0*1e3:.1f}-{Tend*1e3:.1f} ms ({nwin} cycles)")

# --- electrical ---
m=tail(main,t0)
Vdc=m[:,1].mean(); Idc=m[:,2].mean(); Pin=Vdc*Idc
Ia=m[:,3]; Ia_rms=np.sqrt(np.mean(Ia**2)); Ia_pk=np.max(np.abs(Ia)); crest=Ia_pk/Ia_rms
print(f"Vdc={Vdc:.1f} V  Idc={Idc:.2f} A  Pin={Pin/1e3:.2f} kW")
print(f"Ia_rms={Ia_rms:.1f} A  Ia_pk={Ia_pk:.1f} A  crest={crest:.3f}")

# --- losses (periodic-averaged, steady tail) ---
cond6=tail(allc,t0)[:,1:].mean(axis=0)
sw6  =tail(allsw,t0)[:,1:].mean(axis=0)
Pcond=cond6.sum(); Psw=sw6.sum(); Ploss=Pcond+Psw
print(f"\ncond/switch: {np.array2string(cond6,precision=1)}  Σ={Pcond:.1f} W")
print(f"sw  /switch: {np.array2string(sw6,precision=1)}  Σ={Psw:.1f} W")
print(f"Ploss(6 sw) = {Ploss:.1f} W  (cond {Pcond:.0f} + sw {Psw:.0f})")

eta=(Pin-Ploss)/Pin*100
print(f"eta = (Pin-Ploss)/Pin = {eta:.3f} %")

# --- energy balance (S3) ---
pw=tail(pwr,t0)
vg=pw[:,1:4]; ii=pw[:,4:7]
P_Vg=np.mean(np.sum(vg*ii,axis=1))          # power into back-EMF source
Irms2=np.mean(ii**2,axis=0); P_Rg=Rg*Irms2.sum()   # resistor loss (3 phases)
Pout_ac=P_Vg+P_Rg
resid=Pin-Ploss-Pout_ac
print(f"\n--- energy balance ---")
print(f"P_Vg(into bemf)={P_Vg/1e3:.2f} kW  P_Rg={P_Rg:.1f} W  Pout_ac={Pout_ac/1e3:.2f} kW")
print(f"Pin={Pin/1e3:.2f}  Ploss={Ploss/1e3:.3f}  Pout_ac={Pout_ac/1e3:.2f} kW")
print(f"residual Pin-Ploss-Pout = {resid:.1f} W = {resid/Pin*100:.2f} % of Pin")

# --- THD of phase-A current (exact integer cycles -> no window needed) ---
ia=pw[:,4]; N=len(ia)
F=np.fft.rfft(ia); mag=np.abs(F)
k=nwin                                   # fundamental bin = number of whole cycles in window
fund=mag[k]
tot=np.sqrt(np.sum(mag[1:]**2))          # all AC content (excl DC)
thd_full=np.sqrt(max(tot**2-fund**2,0))/fund
# low-order THD (harmonics up to 40th, excludes switching ripple)
hmask=np.zeros_like(mag,bool)
for h in range(2,41): hmask[h*k]=True
thd_lo=np.sqrt(np.sum(mag[hmask]**2))/fund
print(f"\nTHD(Ia): full(incl ripple)={thd_full*100:.1f}%  low-order(<=40th)={thd_lo*100:.2f}%")

# --- analytic steady-state Tj (option b) ---
# module pairs: A=Q1+Q2, B=Q3+Q4, C=Q5+Q6
Ptot=cond6+sw6
mods=[(0,1),(2,3),(4,5)]
print(f"\n--- analytic Tj_ss (Ta={Ta}, R_jc={R_jc}, R_cs={R_cs}/module) ---")
Tj_all=[]
for hi,lo in mods:
    Pmod=Ptot[hi]+Ptot[lo]
    Tcase=Ta+Pmod*R_cs
    for idx in (hi,lo):
        Tji=Tcase+Ptot[idx]*R_jc
        Tj_all.append(Tji)
        print(f"  Q{idx+1}: P={Ptot[idx]:.0f}W Tcase={Tcase:.1f} Tj={Tji:.1f} C")
print(f"  hottest Tj_ss = {max(Tj_all):.1f} C   (limit 175)")

# --- in-model transient Tj readout (corroboration, not settled) ---
tjt=tj[-1,1:]
print(f"\nin-model Tj @ {Tend*1e3:.0f}ms (transient): Q1={tjt[0]:.1f} Q2={tjt[1]:.1f} HS={tjt[2]:.1f} C")
print(f"heat-flow to coolant @ end = {hf[-1,1]:.1f} W (transient, not settled)")

print(f"\nSUMMARY  eta={eta:.2f}%  Ploss={Ploss:.0f}W  Ia={Ia_rms:.0f}Arms  crest={crest:.2f}  Tj_ss={max(Tj_all):.0f}C  ebal={resid/Pin*100:+.2f}%")

label=op.get("label","")
if label:
    row=f"{label},{Vdc:.0f},{Ia_rms:.1f},{Pin/1e3:.1f},{eta:.3f},{Pcond:.0f},{Psw:.0f},{Ploss:.0f},{crest:.3f},{thd_lo*100:.2f},{max(Tj_all):.1f},{resid/Pin*100:+.2f}\n"
    f=os.path.join(os.path.dirname(os.path.abspath(__file__)),"corners.csv")
    new=not os.path.exists(f)
    with open(f,"a") as fh:
        if new: fh.write("label,Vdc,Ia_rms,Pin_kW,eta_pct,Pcond_W,Psw_W,Ploss_W,crest,THDlo_pct,Tj_ss_C,ebal_pct\n")
        fh.write(row)
    print("appended:",row.strip())
