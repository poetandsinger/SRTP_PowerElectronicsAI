"""
WE-1: Class-8 long-haul e-truck traction inverter — LIFETIME-DRIVEN workflow.
Binding constraint is power-cycling life over ~1.5M km, NOT 0-100 peak.
Workflow = mission -> loss -> Foster Tj(t) -> rainflow -> LESIT Nf -> Miner LC.

Vault basis: reliability-and-lifetime.md (LESIT A=640, alpha=-5.039,
Ea=0.617 eV; PoF chain), thermal-design.md (Foster Zth). Device params
class-typical [T]; truck specs refined from web research (see note).
"""
import numpy as np
kB = 8.617e-5  # eV/K

# ------------------------------------------------------------------ vehicle
truck = dict(m=37000.0, Cd=0.55, Af=10.0, Cr=0.006, rho=1.2, rw=0.50)
g=9.81
def road_P(v, grade=0.0):
    F=(truck['m']*g*truck['Cr']*np.cos(grade) + truck['m']*g*np.sin(grade)
       + 0.5*truck['rho']*truck['Cd']*truck['Af']*v*v)
    return F*v

# ------------------------------------------------------------------ inverter loss (per switch)
Vdc=800.0; fsw=8e3
Rds0=3.0e-3; Esw_ref=12e-3; Iref=400.0; Vref=800.0
def loss_per_switch(P_elec, Rds, cosphi=0.9):
    VLL=0.72*Vdc
    Irms=abs(P_elec)/(np.sqrt(3)*VLL*cosphi) if P_elec else 0.0
    Ip=Irms*np.sqrt(2)
    Pcond=3*Irms**2*Rds
    Psw=3*fsw*(Esw_ref/Iref)*(Vdc/Vref)*(2/np.pi)*Ip
    return (Pcond+Psw)/6.0

# ------------------------------------------------------------------ Foster Zth (per switch -> coolant)
FOSTER0=[(0.020,0.0005),(0.050,0.01),(0.080,0.2),(0.090,5.0)]  # (Ri K/W, tau s); sum~0.24 (cost-sized module runs hot)
def tj_trace(P_sw, Tcool, dt, foster):
    n=len(P_sw); Tj=np.empty(n); state=[0.0]*len(foster)
    for k in range(n):
        rise=0.0
        for i,(R,tau) in enumerate(foster):
            a=np.exp(-dt/tau); state[i]=state[i]*a + P_sw[k]*R*(1-a); rise+=state[i]
        Tj[k]=Tcool[k]+rise
    return Tj

# ------------------------------------------------------------------ mission (one long-haul day, 1 Hz) + coolant profile
def mission_day():
    P=[];
    def const(x,t): P.extend([x]*int(t))
    def ramp(a,b,t): P.extend(list(np.linspace(a,b,int(t))))
    const(0,600)                                        # parked, key-on warm-up
    for _ in range(15):                                # terminal maneuver 15 min
        ramp(0,70e3,8); const(70e3,4); ramp(70e3,0,6); const(0,10)
    for _ in range(3):                                 # 3 highway blocks
        ramp(0,150e3,40); const(150e3,2400)            # 40 min cruise @150 kW (loaded 37-40t)
        const(350e3,1000)                              # ~17 min 7% Davis-Dam grade @350 kW (near 400 kW cont rating)
        const(-90e3,900)                               # descent regen
        const(150e3,1800)                              # cruise
    for _ in range(15):
        ramp(0,70e3,8); const(70e3,4); ramp(70e3,0,6); const(0,10)
    const(0,3600)                                      # parked overnight cooldown
    P=np.array(P,float)
    # coolant: ambient 25 when parked, warms to 70 running, decays back parked
    running = np.abs(P)>1e3
    Tc=np.full(len(P),25.0)
    warm=25.0                                          # parked at ambient 25 C (not 0!)
    for k in range(len(P)):
        target=75.0 if running[k] else 25.0            # hot truck coolant when running
        warm += (target-warm)*(1-np.exp(-1/180.0))     # ~3 min coolant time-const
        Tc[k]=warm
    return P, Tc

# ------------------------------------------------------------------ rainflow (ASTM E1049, 3-point)
def rainflow(series):
    s=np.asarray(series,float)
    tp=[s[0]]
    for i in range(1,len(s)-1):
        if (s[i]-s[i-1])*(s[i+1]-s[i])<0: tp.append(s[i])
    tp.append(s[-1])
    stack=[]; cyc=[]
    for x in tp:
        stack.append(x)
        while len(stack)>=3:
            X=abs(stack[-1]-stack[-2]); Y=abs(stack[-2]-stack[-3])
            if X<Y: break
            rng=Y; mean=(stack[-2]+stack[-3])/2
            if len(stack)==3:
                cyc.append((rng,mean,0.5)); stack.pop(0)
            else:
                cyc.append((rng,mean,1.0)); last=stack[-1]; del stack[-3:]; stack.append(last)
    for i in range(len(stack)-1):
        cyc.append((abs(stack[i+1]-stack[i]),(stack[i]+stack[i+1])/2,0.5))
    return cyc

# self-test rainflow: the largest extracted range must equal the global span
_seq=[-2,1,-3,5,-1,3,-4,4,-2]
_rng=[r for r,_,_ in rainflow(_seq)]
assert abs(max(_rng)-(max(_seq)-min(_seq)))<1e-6, "rainflow global-range invariant failed"

# ------------------------------------------------------------------ Nf: Coffin-Manson anchored to a REAL vault datapoint
# NOTE: the closed-form LESIT (A=640, Ea=0.617eV) in reliability-and-lifetime.md gives
# physically wrong absolute Nf (~20 cycles at 100K) -- a coefficient inconsistency the
# vault's own Red Team flags. Instead anchor Coffin-Manson+Arrhenius to the note's
# EMPIRICAL datapoint: 110,000 cycles at dTj=50K, Tj,max=110C (Tm~85C), ton~10s [139].
# Absolute life is coefficient-dominated (uncertain ~1-2 orders); the RANKING of cycles
# and the dTj^-n leverage are the robust outputs.
N_REF=110000.0; DT_REF=50.0; TM_REF=358.15; N_CM=5.0; EA=0.10  # eV
MODULE_UPLIFT=3.0   # sintered-Ag + Cu-clip premium SiC module vs the IGBT anchor [147] (flagged)
def Nf(dTj,Tjm_C):
    Tm=Tjm_C+273.15
    cm=(DT_REF/max(dTj,1.0))**N_CM
    arr=np.exp((EA/kB)*(1/Tm - 1/TM_REF))
    return N_REF*MODULE_UPLIFT*cm*arr

def life_km(k_uplift, km_day=850.0):
    """k_uplift = silicon+cooling scale: Rds/k and Rth/k (cuts dTj).
    Two-timescale decomposition (standard PoF practice):
      * daily cold-start MACRO-cycle: 1/day, dTj = Tj,max - parked ambient
      * intra-day MICRO-cycles: rainflow of the running segment only.
    Avoids the rainflow residue ambiguity for the once-a-day macro-cycle."""
    Rds=Rds0/k_uplift; foster=[(r/k_uplift,t) for r,t in FOSTER0]
    P,Tc=mission_day()
    Psw=np.array([loss_per_switch(p,Rds) for p in P])
    Tj=tj_trace(Psw,Tc,1.0,foster)
    # rainflow the full single day; grade cycles ride the warm baseline correctly.
    cyc=rainflow(Tj)
    rmax=max(r for r,_,_ in cyc)                       # the daily cold-start = global range
    LC=0.0; big=[]
    for rng,mean,cnt in cyc:
        if rng<3: continue
        if abs(rng-rmax)<1e-6: cnt=1.0                 # cold-start is 1 FULL cycle/day (periodic)
        nf=Nf(rng,mean); dmg=cnt/nf; LC+=dmg
        if rng>10:
            kind="COLD-START (daily)" if abs(rng-rmax)<1e-6 else ("grade soak" if rng>25 else "cruise/regen")
            big.append((rng,mean,cnt,nf,dmg,kind))
    return LC,Tj,big,km_day

# ------------------------------------------------------------------ run
print("="*72); print("WE-1  CLASS-8 E-TRUCK INVERTER -- LIFETIME-DRIVEN"); print("="*72)
print(f"cruise 80 km/h flat: {road_P(80/3.6)/1000:5.0f} kW")
print(f"6% grade @37t, 40 km/h: {road_P(40/3.6,np.arctan(0.06))/1000:5.0f} kW sustained (the driver)")
print(f"Foster steady Rth/switch {sum(r for r,_ in FOSTER0):.3f} K/W")

LC,Tj,big,km_day=life_km(1.0)
print(f"\nBASELINE (cost-sized, Rth~0.24)  Tj: min {Tj.min():3.0f}  max {Tj.max():3.0f}  mean {Tj.mean():3.0f} C")
print("Damage cycles ranked by contribution (dTj K, Tm C, n/day, Nf, damage/day):")
tot=sum(d for *_,d,_ in big)
for r,m,c,nf,d,kind in sorted(big,key=lambda x:-x[4])[:8]:
    print(f"   dTj={r:4.0f}  Tm={m:4.0f}  n={c:4.1f}  Nf={nf:11,.0f}  dmg={d:.2e} ({d/tot*100:4.1f}%)  {kind}")
print(f"\nLC/day={LC:.3e} -> {1/LC:,.0f} days -> {1/LC*km_day/1e6:.2f} M km to LC=1 "
      f"(target 1 M km; margin {1/LC*km_day/1e6:.1f}x)")

print("\n--- LIFETIME-DRIVEN SIZING (upsize to cut dTj; Nf ~ dTj^-5) ---")
for k,lbl in [(1.0,"baseline (hot)"),(1.15,"+15% Si+cooling"),(1.3,"+30% Si+cooling")]:
    LCk,Tjk,_,_=life_km(k)
    print(f"  {lbl:16s}: Tj,max {Tjk.max():3.0f} C  dTj_day {Tjk.max()-Tjk.min():3.0f} K  "
          f"life {1/LCk*km_day/1e6:6.2f} M km")
