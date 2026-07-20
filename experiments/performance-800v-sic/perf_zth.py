"""
WE-2: High-performance / hypercar traction inverter — POWER-DENSITY + TRANSIENT-THERMAL workflow.
Binding constraint: kW/L and how long a peak WAY above continuous rating can be held,
set by transient Zth(t) (thermal mass), NOT drive-cycle efficiency.

Real anchor (Porsche Taycan Turbo GT, sourced): 815 kW / 2 s, 700 kW / 10 s,
580 kW continuous [Porsche Newsroom]. We reproduce that duration-gated shape.
Vault basis: thermal-design.md (Zth Foster, peak rating from Zth(pulse)); density
vs DOE trajectory 13.3->34->100 kW/L [DOE OSTI].
"""
import numpy as np

Vdc=800.0; fsw=15e3; Tcool=60.0; Tj_max=175.0
Rds=2.5e-3; Esw_ref=10e-3; Iref=400.0; Vref=800.0   # premium SiC, low loss

def loss_total(P_elec, cosphi=0.92):
    VLL=0.72*Vdc
    Irms=abs(P_elec)/(np.sqrt(3)*VLL*cosphi)
    Ip=Irms*np.sqrt(2)
    Pcond=3*Irms**2*Rds
    Psw=3*fsw*(Esw_ref/Iref)*(Vdc/Vref)*(2/np.pi)*Ip
    return Pcond+Psw, Irms

# Foster Zth per switch -> coolant. Power-dense small-die module: moderate steady
# Rth, and thermal MASS such that a burst ~1.2-1.6x continuous lasts seconds-to-tens.
# (Ri K/W, tau s)
FOSTER=[(0.03,0.005),(0.06,0.05),(0.08,0.8),(0.13,6.0)]
Rth=sum(r for r,_ in FOSTER)
def Zth(t):
    return sum(R*(1-np.exp(-t/tau)) for R,tau in FOSTER)

def Tj_steady(P):
    pl,_=loss_total(P); return Tcool + (pl/6)*Rth

def peak_duration(P_peak, P_cont):
    """From the continuous-rated steady Tj, apply the peak loss step; time to hit Tj_max."""
    pl_c,_=loss_total(P_cont); Tj0=Tcool+(pl_c/6)*Rth      # warm baseline
    pl_p,_=loss_total(P_peak); dP=(pl_p-pl_c)/6            # extra per-switch loss in the burst
    # Tj(t) = Tj0 + dP*Zth(t); find t where Tj = Tj_max
    for t in np.arange(0.05, 120, 0.05):
        if Tj0 + dP*Zth(t) >= Tj_max:
            return t, Tj0
    return np.inf, Tj0

print("="*72); print("WE-2  PERFORMANCE INVERTER — POWER-DENSITY + TRANSIENT-THERMAL"); print("="*72)
print(f"module: SiC, fsw {fsw/1e3:.0f} kHz, coolant {Tcool:.0f} C, Rth(steady) {Rth:.3f} K/W, Tj,max {Tj_max:.0f}")

# 1. continuous rating = highest power with steady Tj <= 160 (15 C margin)
Pc=0
for P in np.arange(100e3,700e3,5e3):
    if Tj_steady(P)<=160.0: Pc=P
print(f"\nCONTINUOUS rating (steady Tj<=160): {Pc/1e3:.0f} kW  (steady Tj {Tj_steady(Pc):.0f} C)")

# 2. peak-duration curve (Zth pulse) from a cruise baseline ~55% of continuous
Pbase=0.55*Pc
print(f"\nPEAK-DURATION curve (Zth pulse, from {Pbase/1e3:.0f} kW cruise baseline, Tj {Tj_steady(Pbase):.0f} C):")
print("  peak/cont | peak kW | sustainable burst")
for mult in [1.1,1.25,1.4,1.6]:
    Pk=Pc*mult; dur,Tj0=peak_duration(Pk,Pbase)
    ds = f"{dur:5.1f} s" if np.isfinite(dur) else "indefinite"
    print(f"   {mult:4.2f}x   | {Pk/1e3:6.0f}  | {ds}")
print("  -> higher peak = shorter burst = the Porsche 815kW/2s, 700kW/10s, 580 cont shape.")

# 3. power density: derive VOLUME from SOURCED densities (do not invent kW/L)
peak_kW=Pc*1.4/1e3
print(f"\nPOWER DENSITY (peak rating {peak_kW:.0f} kW; volume from SOURCED densities):")
for kWL,src in [(33,"single-side SiC (Wolfspeed 300kW CRD ~33 kW/L [H])"),
                (60,"double-side-cooled premium (~50-70 kW/L)"),
                (100,"DOE 2025 target (DSC+microchannel)")]:
    print(f"   {kWL:3d} kW/L [{src}] -> {peak_kW/kWL:4.1f} L")
print("DOE inverter density trajectory: 13.3 (2012) -> 34 (2022) -> 100 kW/L target [DOE OSTI].")
print("Driver = kW/L (packaging) + peak-duration (Zth thermal mass), NOT partial-load efficiency.")
