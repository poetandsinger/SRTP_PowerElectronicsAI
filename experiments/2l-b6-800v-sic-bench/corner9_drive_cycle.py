"""
Corner 9 — Drive-cycle efficiency & thermal history (averaged model).
Pass criteria: cycle-average eta; Tj history for lifetime (rainflow bins).

METHOD (the averaged model the switched bench cannot run directly): build an inverter
LOSS MAP from the 6 PLECS-validated corners, drive it with a representative US06/WLTP-class
speed trace through a vehicle + IPMSM model, integrate energy over the cycle for eta_cycle,
and convolve the loss with the device Cauer thermal network for the Tj(t) history ->
rainflow ->   delta-Tj bins for a Coffin-Manson lifetime estimate (coefficients scoped to
reliability-and-lifetime.md). Loss map calibrated to C1-C6 (fit error < 8%, mostly < 1%).

The drive cycle here is REPRESENTATIVE (synthesized to US06/WLTP class statistics: urban
stop-go + highway cruise + aggressive accelerations), not the certified regulatory trace.
Vehicle params are a representative 300 kW performance BEV ([T]-class).
"""
import numpy as np

# ---------- 1. inverter loss map (fit to the 6 validated corners) ----------
kc, ks = 9.585e-3, 5.974e-3        # Pcond=kc*Irms^2 ; Psw=ks*Vdc*Irms  (6 switches total)
def inv_loss(Vdc, Irms):
    return kc*Irms**2 + ks*Vdc*np.abs(Irms)     # W, total for all 6 switches

# ---------- 2. machine / vehicle (representative 300 kW performance BEV) ----------
Pp, lam, Ld, Lq = 4, 0.110, 0.18e-3, 0.42e-3   # same IPMSM as corners 6/8
Ismax = 360.0                       # inverter current limit (A rms)
Pmax  = 300e3                       # inverter power limit (W)
Vmax_ph = 750/np.sqrt(3)            # SVPWM phase-voltage ceiling at 750 V bus
Vdc   = 750.0
m_veh, rw, gear, Cd_A, Crr = 2200., 0.34, 9.0, 0.62, 0.011
rho, g = 1.20, 9.81
Trated = 1.5*Pp*lam*(Ismax*np.sqrt(2))          # approx magnet torque at current limit

def motor_op(v, a):
    """vehicle speed v (m/s), accel a (m/s^2) -> (Irms, wm, P_mech, motoring?)."""
    F = m_veh*a + 0.5*rho*Cd_A*v**2 + Crr*m_veh*g*np.sign(max(v,1e-3))
    Tw = F*rw
    wm = (v/rw)*gear                             # motor mech rad/s
    Tm = Tw/gear
    Pmech = Tm*wm
    # cap to inverter envelope
    if abs(Pmech) > Pmax:  Pmech = np.sign(Pmech)*Pmax; Tm = Pmech/max(wm,1e-3)
    # torque -> q-current (magnet torque dominant); field-weakening id above base speed
    iq = Tm/(1.5*Pp*lam)
    we = Pp*wm
    # field-weakening: if back-EMF*iq would exceed voltage ceiling, add negative id
    id_ = 0.0
    if we*lam > Vmax_ph*0.9:                      # near/над base speed -> weaken
        id_ = -min((we*lam - Vmax_ph*0.9)/(we*Ld+1e-9), Ismax*np.sqrt(2))
    Ipk = np.hypot(id_, iq)
    Irms = min(Ipk/np.sqrt(2), Ismax)
    return Irms, wm, Pmech, (Pmech >= 0)

# ---------- 3. representative US06/WLTP-class speed trace ----------
def build_cycle():
    seg = []   # (duration s, v_start, v_end) in m/s ; ramps
    kmh = 1/3.6
    def ramp(t, a, b): seg.append((t, a*kmh, b*kmh))
    # urban stop-go (WLTP low/medium class)
    for _ in range(3):
        ramp(8, 0, 35); ramp(10, 35, 35); ramp(6, 35, 0); ramp(4, 0, 0)
    ramp(12, 0, 60); ramp(20, 60, 55); ramp(10, 55, 0); ramp(5,0,0)
    # highway cruise (WLTP extra-high)
    ramp(15, 0, 110); ramp(60, 110, 120); ramp(15, 120, 90)
    # US06 aggressive bursts
    ramp(9, 90, 129); ramp(12, 129, 100); ramp(7, 100, 130); ramp(15, 130, 80)
    ramp(10, 80, 0); ramp(6, 0, 0)
    # build 1 Hz trace
    t, v = [0.0], [0.0]
    for dur, v0, v1 in seg:
        n = int(dur)
        for k in range(1, n+1):
            t.append(t[-1]+1.0); v.append(v0 + (v1-v0)*k/n)
    return np.array(t), np.array(v)

t, v = build_cycle()
a = np.gradient(v, t)
dt = 1.0

# ---------- 4. integrate energy + losses over the cycle ----------
E_in = E_out_mot = E_loss = E_regen = 0.0
Ploss_t = np.zeros_like(t); Irms_t = np.zeros_like(t)
for i in range(len(t)):
    Irms, wm, Pmech, motoring = motor_op(v[i], a[i])
    Pl = inv_loss(Vdc, Irms); Ploss_t[i] = Pl; Irms_t[i] = Irms
    if motoring:
        Pdc = Pmech + Pl                 # inverter draws mech + its own loss
        E_in += Pdc*dt; E_out_mot += Pmech*dt; E_loss += Pl*dt
    else:                                # regen: mech power returned, minus inverter loss
        E_regen += (abs(Pmech) - Pl)*dt; E_loss += Pl*dt

eta_cycle = E_out_mot/E_in*100
dist_km = np.trapz(v, t)/1000 if hasattr(np,'trapz') else np.trapezoid(v, t)/1000
print(f"Cycle: {t[-1]:.0f} s, {dist_km:.2f} km, v_max {v.max()*3.6:.0f} km/h, v_avg {v.mean()*3.6:.0f} km/h")
print(f"Energy: E_in(motor) {E_in/3.6e6*1e3:.2f} Wh, E_out {E_out_mot/3.6e6*1e3:.2f} Wh, "
      f"inverter loss {E_loss/3.6e6*1e3:.2f} Wh, regen recovered {E_regen/3.6e6*1e3:.2f} Wh")
print(f"CYCLE-AVERAGE INVERTER EFFICIENCY (motoring, energy-weighted) = {eta_cycle:.2f} %")
print(f"  (slightly BELOW the rated-point 99.07%: the cycle spends time at low speed/light load where")
print(f"   switching loss ~ ks*Vbus*I is set by the FULL bus and is a larger fraction of delivered power)")
print(f"  peak inverter loss {Ploss_t.max():.0f} W at I={Irms_t[np.argmax(Ploss_t)]:.0f} A rms; "
      f"mean loss {Ploss_t.mean():.0f} W\n")

# ---------- 5. Tj history: Foster thermal impedance driven by loss (stable recursion) ----------
# Foster form gives Tj directly (Tj = Ta + sum of stage rises); exact for piecewise-const P.
# Junction->case: 4 stages, Ri = CAB450 Cauer R's (sum 0.0948 = Rth,jc), representative tau.
# Case->coolant: R_cs (CRD-calibrated 0.070) with a cold-plate time constant, driven by the
# MODULE loss (2 switches share the baseplate) — matches the corners 1-5 analytic Tj_ss.
Rjc = np.array([0.00879, 0.02757, 0.04532, 0.01311]); tjc = np.array([1e-4, 1e-3, 1e-2, 5e-2])
R_cs, tau_cs = 0.070, 0.56                              # case->coolant R (C/W) and tau (s)
Ta = 65.0
Pdev = Ploss_t/6.0                                      # per-switch loss (near-symmetric)
Pmod = 2.0*Pdev                                         # module-pair loss into the baseplate
def foster_tj(Pdev, Pmod, tgrid):
    dt = 1.0
    ajc = np.exp(-dt/tjc); acs = np.exp(-dt/tau_cs)
    Sjc = np.zeros(len(Rjc)); Scs = 0.0
    out = np.zeros(len(tgrid))
    for i in range(len(tgrid)):
        Sjc = Sjc*ajc + Pdev[i]*Rjc*(1-ajc)            # junction->case stage rises
        Scs = Scs*acs + Pmod[i]*R_cs*(1-acs)           # case->coolant rise
        out[i] = Ta + Sjc.sum() + Scs
    return out

Tj = foster_tj(Pdev, Pmod, t)
print(f"Tj history: peak {Tj.max():.0f} C, mean {Tj.mean():.0f} C, min {Tj.min():.0f} C "
      f"(limit 175 C -> {'OK' if Tj.max()<175 else 'EXCEEDS'})")

# ---------- 6. rainflow on Tj(t) -> delta-Tj bins for lifetime ----------
def rainflow(series):
    # ASTM simplified: extract reversals, then 4-point counting
    s = np.asarray(series, float)
    # reduce to turning points
    d = np.diff(s); idx = np.where(np.diff(np.sign(d)) != 0)[0] + 1
    ext = np.concatenate([[s[0]], s[idx], [s[-1]]])
    cycles = []; stack = []
    for x in ext:
        stack.append(x)
        while len(stack) >= 3:
            a0, a1, a2 = stack[-3], stack[-2], stack[-1]
            if abs(a1-a0) <= abs(a2-a1):
                cycles.append(abs(a1-a0)); del stack[-2]
            else:
                break
    for i in range(len(stack)-1):
        cycles.append(abs(stack[i+1]-stack[i]))
    return np.array(cycles)

dTj = rainflow(Tj)
print(f"Rainflow: {len(dTj)} cycles; delta-Tj max {dTj.max():.0f} C, mean {dTj.mean():.1f} C")
bins = [0,10,20,40,80,200]
h,_ = np.histogram(dTj, bins=bins)
print("  delta-Tj bins (C):  " + "  ".join(f"{bins[i]}-{bins[i+1]}:{h[i]}" for i in range(len(h))))

# Coffin-Manson relative-life proxy: Nf ~ A*dTj^-n ; sum Miner damage ~ sum dTj^n (relative)
n_cm = 5.0    # representative SiC/sinter exponent (reliability-and-lifetime.md; A unknown -> relative only)
damage_rel = np.sum(dTj**n_cm)
print(f"  relative cyclic damage proxy sum(dTj^{n_cm:.0f}) = {damage_rel:.2e} (per cycle-run; "
      f"absolute Nf needs Coffin-Manson A,n from reliability-and-lifetime.md)\n")

print("VERDICT (corner 9):")
print(f"  Cycle-average inverter efficiency {eta_cycle:.2f} % over a {dist_km:.1f} km US06/WLTP-class cycle;")
print(f"  regen recovers {E_regen/3.6e6*1e3:.0f} Wh. Tj stays {Tj.max():.0f} C peak (< 175 C) with "
      f"delta-Tj up to {dTj.max():.0f} C.")
print(f"  Tj(t) + rainflow bins are the lifetime front-end; absolute Nf/Miner scoped to reliability note.")
print(f"  [averaged model: loss map calibrated to PLECS C1-C6 (<8% fit); cycle+vehicle representative [T].]")
