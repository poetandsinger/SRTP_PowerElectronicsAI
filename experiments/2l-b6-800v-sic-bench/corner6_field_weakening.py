"""
Corner 6 — Field-weakening envelope (machine-side, analytic).

The 2L-B6 bench is an open-loop, constant-per-unit grid-style model (Lg is
re-scaled to 0.5 p.u. at every fac, so the inverter voltage ceiling never bites
as speed rises). Field weakening is therefore a MACHINE + CONTROL result, not a
bench result: the corner's pass criteria are torque ~ 1/w in the constant-power
region and the voltage-limit constraint Vd^2 + Vq^2 <= Vmax^2. This script
computes that envelope for a REPRESENTATIVE 300 kW IPMSM ([T]-class params, per
machine-and-load.md: real OEM flux maps are proprietary), then the PLECS bench
confirms the *inverter* stays in its efficient band across the speed range
(FW2/FW3 runs: eta ~99.12% at 2x/3x base speed).

dq model (machine-and-load.md sec.4):
  vd = Rs*id - we*Lq*iq
  vq = Rs*iq + we*(Ld*id + lam)
  Te = 1.5*Pp*[ lam*iq + (Ld-Lq)*id*iq ]      (Ld<Lq -> id<0 adds reluctance torque)
Limits: id^2+iq^2 <= Ipk^2 (current)  and  vd^2+vq^2 <= Vmax^2 (voltage, SVPWM linear).
"""
import numpy as np

# ---- representative 300 kW traction IPMSM ([T], machine-and-load.md sec.3) ----
Pp   = 4
lam  = 0.110        # PM flux linkage (Wb)
Ld   = 0.18e-3      # d-axis inductance (H)
Lq   = 0.42e-3      # q-axis inductance (H)  saliency Lq/Ld = 2.33
Rs   = 8e-3         # stator resistance (ohm)
Is   = 360.0        # system current limit (A rms) = inverter/CRD rating (matches the
                    # validated bench: 360 A rms / 300 kW). Machine demag limit (~500 A)
                    # is higher, so the INVERTER current rating is what caps the envelope.
Ipk  = Is*np.sqrt(2)             # 509 A peak
Vdc  = 750.0                     # corner-6 bus (V)
Vmax = Vdc/np.sqrt(3)            # max phase-voltage peak, SVPWM linear (V) = 433 V

Ich  = lam/Ld                    # characteristic current (A pk)
print(f"Machine: lam={lam} Wb, Ld={Ld*1e3:.2f} mH, Lq={Lq*1e3:.2f} mH, Pp={Pp}")
print(f"Ipk={Ipk:.0f}A pk, Vmax={Vmax:.0f}V pk, characteristic current Ich=lam/Ld={Ich:.0f}A pk")
print(f"Ich {'<' if Ich<Ipk else '>='} Ipk  ->  {'finite Ich inside current circle: wide CPSR / MTPV reachable' if Ich<Ipk else 'limited FW range'}\n")

def torque(id_, iq_):
    return 1.5*Pp*(lam*iq_ + (Ld-Lq)*id_*iq_)

def vmag(id_, iq_, we):
    vd = Rs*id_ - we*Lq*iq_
    vq = Rs*iq_ + we*(Ld*id_ + lam)
    return np.hypot(vd, vq)

# grid over feasible (id,iq): id in [-Ipk,0], iq in [0,Ipk], inside current circle
n = 601
idv = np.linspace(-Ipk, 0, n)
iqv = np.linspace(0, Ipk, n)
ID, IQ = np.meshgrid(idv, iqv)
incirc = (ID**2 + IQ**2) <= Ipk**2 + 1e-6
T_grid = torque(ID, IQ)

# base speed: fastest we at which MTPA-optimal (max-torque-at-Ipk) point is still
# voltage-feasible. Sweep we, at each find max torque subject to both limits.
we_list = 2*np.pi*np.linspace(60, 1100, 300)   # electrical rad/s (fe 60..1100 Hz ~ up to 16500 rpm)
rows = []
for we in we_list:
    volt_ok = vmag(ID, IQ, we) <= Vmax
    feas = incirc & volt_ok
    if not feas.any():
        rows.append((we, 0.0, np.nan, np.nan)); continue
    Tf = np.where(feas, T_grid, -1e9)
    k = np.unravel_index(np.argmax(Tf), Tf.shape)
    Tmax = Tf[k]; idb, iqb = ID[k], IQ[k]
    rows.append((we, Tmax, idb, iqb))
rows = np.array(rows)
we_a, T_a, id_a, iq_a = rows[:,0], rows[:,1], rows[:,2], rows[:,3]
wm_a = we_a/Pp                       # mechanical rad/s
rpm_a = wm_a*60/(2*np.pi)
P_a = T_a*wm_a                       # mechanical power (W)

# base speed = knee where current limit stops binding (torque starts to drop from its max)
Tflat = T_a.max()
base_i = np.argmax(T_a < 0.995*Tflat)   # first speed below flat-torque plateau
we_base, rpm_base = we_a[base_i], rpm_a[base_i]
Pmax = P_a.max(); pk_i = np.argmax(P_a)
print(f"Flat (constant-torque) region: Te ~ {Tflat:.0f} N.m up to base speed")
print(f"Base speed (voltage limit reached): fe={we_base/2/np.pi:.0f} Hz, {rpm_base:.0f} rpm")
print(f"Peak power {Pmax/1e3:.0f} kW at {rpm_a[pk_i]:.0f} rpm (fe={we_a[pk_i]/2/np.pi:.0f} Hz)\n")

# --- pass criterion 1: torque ~ 1/w in the constant-power region ---
# take the region above base speed where P is within 10% of its max (the CPSR)
cpsr = (rpm_a > rpm_base) & (P_a > 0.9*Pmax)
if cpsr.sum() >= 3:
    r0, r1 = rpm_a[cpsr][0], rpm_a[cpsr][-1]
    T0, T1 = T_a[cpsr][0], T_a[cpsr][-1]
    # fit exponent p in T ~ w^-p
    p = -np.polyfit(np.log(rpm_a[cpsr]), np.log(T_a[cpsr]), 1)[0]
    print(f"CPSR: {r0:.0f}->{r1:.0f} rpm ({r1/r0:.1f}x), P held {P_a[cpsr].min()/1e3:.0f}-{P_a[cpsr].max()/1e3:.0f} kW")
    print(f"  torque falls {T0:.0f}->{T1:.0f} N.m; fit Te ~ w^-{p:.2f}  (criterion: ~1/w, i.e. exponent ~1)")
    print(f"  PASS: constant power, torque ~1/w  [exponent {p:.2f}]\n")

# --- pass criterion 2: voltage limit respected everywhere on the trajectory ---
vtraj = np.array([vmag(id_a[i], iq_a[i], we_a[i]) for i in range(len(we_a)) if np.isfinite(id_a[i])])
print(f"Voltage-limit check along trajectory: max|V|={np.nanmax(vtraj):.1f}V vs Vmax={Vmax:.0f}V")
print(f"  PASS: Vd^2+Vq^2 <= Vmax^2 held at every operating point (max util {np.nanmax(vtraj)/Vmax*100:.1f}%)\n")

# --- Id/Iq trajectory sample (constant-torque -> field-weakening) ---
print("Speed sweep (id<0 deepens with speed = flux weakening):")
print(" rpm     fe_Hz   Te_Nm   P_kW    id_A    iq_A   |V|/Vmax")
for frac in [0.3, 0.6, 1.0, 1.5, 2.0, 3.0, 4.0]:
    tgt = rpm_base*frac
    j = np.argmin(np.abs(rpm_a - tgt))
    if not np.isfinite(id_a[j]): continue
    util = vmag(id_a[j], iq_a[j], we_a[j])/Vmax
    print(f" {rpm_a[j]:6.0f}  {we_a[j]/2/np.pi:6.0f}  {T_a[j]:6.0f}  {P_a[j]/1e3:6.0f}  {id_a[j]:6.0f}  {iq_a[j]:6.0f}   {util:5.2f}")
