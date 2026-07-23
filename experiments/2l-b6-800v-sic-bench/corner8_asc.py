"""
Corner 8 — Active Short Circuit (ASC) entry: short all low-side switches at max speed.
Pass criteria: bounded entry transient (within device SOA), drag torque, NO bus overvoltage.

SCOPE: ASC is a MACHINE result. The 2L-B6 bench models the "machine" as a back-EMF
voltage source behind a 0.5 p.u. filter Lg — it has no Ld/Lq/lambda dq dynamics, so it
cannot represent the ASC current trajectory. Per plan-depth-research's protection
can/cannot table, PLECS confirms "ASC/freewheel + regen overvoltage" only with a proper
PMSM model. Here we integrate the dq state equations for the representative 300 kW IPMSM
(same params as corner 6), which IS the faithful ASC model. protection-and-safety.md sec.5.

dq state (motor convention), terminals shorted so vd = vq = 0:
  did/dt = (-Rs*id + we*Lq*iq)/Ld
  diq/dt = (-Rs*iq - we*(Ld*id + lambda))/Lq
Steady state (d/dt=0):
  id_sc = -lambda*we^2*Lq/(Rs^2 + we^2*Ld*Lq)   -> -lambda/Ld = -Ich as we->inf
  iq_sc = -lambda*we*Rs /(Rs^2 + we^2*Ld*Lq)     -> 0          as we->inf
Te = 1.5*Pp*[lambda*iq + (Ld-Lq)*id*iq]  (negative iq -> braking/drag torque)
"""
import numpy as np

# ---- representative 300 kW IPMSM (identical to corner6_field_weakening.py) ----
Pp, lam, Ld, Lq, Rs = 4, 0.110, 0.18e-3, 0.42e-3, 8e-3
Ich = lam/Ld
IDM = 900.0        # device pulsed-current rating (A) [166]
Vdc = 850.0        # worst-case bus for the overvoltage check
print(f"Machine: lam={lam} Wb, Ld={Ld*1e3:.2f} mH, Lq={Lq*1e3:.2f} mH, Rs={Rs*1e3:.0f} mOhm, Pp={Pp}")
print(f"characteristic current Ich = lam/Ld = {Ich:.0f} A pk  (steady ASC current -> Ich at high speed)\n")

def asc_steady(we):
    den = Rs**2 + we**2*Ld*Lq
    id_ = -lam*we**2*Lq/den
    iq_ = -lam*we*Rs/den
    return id_, iq_

def torque(id_, iq_):
    return 1.5*Pp*(lam*iq_ + (Ld-Lq)*id_*iq_)

# ---- 1. steady ASC current + drag torque vs speed (find the drag-torque corner) ----
rpm = np.linspace(20, 16500, 800)
we = 2*np.pi*(rpm/60)*Pp
ids, iqs = asc_steady(we)
Imag = np.hypot(ids, iqs)
Td = torque(ids, iqs)                      # drag torque (negative)
kpk = np.argmin(Td)                        # most-negative = peak drag
print("Steady ASC vs speed:")
print(" rpm     fe_Hz   id_A    iq_A   |I|_A   Tdrag_Nm")
for r in [500, 1500, 3000, 6000, 10000, 16500]:
    j = np.argmin(np.abs(rpm-r))
    print(f" {rpm[j]:6.0f}  {we[j]/2/np.pi:6.0f}  {ids[j]:6.0f}  {iqs[j]:6.0f}  {Imag[j]:6.0f}   {Td[j]:7.0f}")
print(f"\nPeak DRAG torque {Td[kpk]:.0f} N.m at {rpm[kpk]:.0f} rpm (corner speed); falls ~1/w above it.")
print(f"Steady ASC current saturates at Ich={Ich:.0f} A (|I|={Imag[-1]:.0f} A at max speed) — bounded.\n")

# ---- 2. entry transient at MAX speed: integrate dq ODE (RK4), worst-case pre-fault IC ----
we_max = 2*np.pi*(16500/60)*Pp
def deriv(x):
    id_, iq_ = x
    return np.array([(-Rs*id_ + we_max*Lq*iq_)/Ld,
                     (-Rs*iq_ - we_max*(Ld*id_ + lam))/Lq])
# pre-fault worst case: motoring at the current limit (id~0, iq~+Ipk) then terminals short
x = np.array([0.0, 360.0*np.sqrt(2)])      # start at +Iq (motoring), A pk
dt, T = 2e-7, 6e-3
n = int(T/dt)
peak = 0.0; t_peak = 0.0
for i in range(n):
    k1 = deriv(x); k2 = deriv(x+0.5*dt*k1); k3 = deriv(x+0.5*dt*k2); k4 = deriv(x+dt*k3)
    x = x + (dt/6)*(k1+2*k2+2*k3+k4)
    im = np.hypot(*x)
    if im > peak: peak, t_peak = im, i*dt
id_ss, iq_ss = asc_steady(we_max)
I_ss = np.hypot(id_ss, iq_ss)
print(f"Entry transient @ 16500 rpm (fe={we_max/2/np.pi:.0f} Hz), pre-fault motoring at current limit:")
print(f"  peak |I| = {peak:.0f} A at t={t_peak*1e3:.2f} ms  ({peak/I_ss:.1f}x the {I_ss:.0f} A steady ASC)")
print(f"  settles to steady ASC {I_ss:.0f} A (~Ich). Peak vs device I_DM {IDM:.0f} A: "
      f"{'WITHIN' if peak<IDM else 'EXCEEDS'} pulsed rating "
      f"({peak/IDM*100:.0f}% of I_DM)")
if peak >= IDM:
    print(f"  -> entry peak exceeds I_DM: use staged/hybrid ASC (freewheel pulses) to damp entry, "
          f"or verify transient SOA covers {peak:.0f} A for {t_peak*1e3:.1f} ms.")
print()

# ---- 3. no bus overvoltage (the ASC safety rationale vs uncontrolled freewheel) ----
e_pk = we_max*lam                          # back-EMF peak at max speed
print("Bus overvoltage check:")
print(f"  back-EMF peak at max speed = we*lam = {e_pk:.0f} V (L-N pk); line-line pk {e_pk*np.sqrt(3):.0f} V.")
print(f"  UNCONTROLLED FREEWHEEL (all off): back-EMF {e_pk*np.sqrt(3):.0f} V "
      f"{'>' if e_pk*np.sqrt(3)>Vdc else '<'} bus {Vdc:.0f} V -> "
      f"{'rectifies through body diodes -> BUS PUMPING/OVERVOLT' if e_pk*np.sqrt(3)>Vdc else 'no rectification'}.")
print(f"  ASC (all low-side on): terminals shorted, fault current circulates in the machine + low-side")
print(f"     switches; NOT delivered to the DC-link cap -> dV_bus ~ 0. No bus pumping. This is why ASC is")
print(f"     the safe state at medium/high speed (freewheel is safe only when back-EMF < bus, i.e. low speed).\n")

print("VERDICT (corner 8):")
print(f"  Steady ASC current bounded at Ich={Ich:.0f} A; entry transient peaks ~{peak/I_ss:.1f}x steady "
      f"(~{peak:.0f} A) then decays.")
print(f"  Drag torque peaks {abs(Td[kpk]):.0f} N.m near {rpm[kpk]:.0f} rpm, falls ~1/w — a controlled braking, not a runaway.")
print(f"  No DC-bus overvoltage (fault current does not reach the cap). ASC is the correct high-speed safe state.")
print(f"  [analytic dq — representative IPMSM params [T]; bench cannot model ASC (back-EMF-source machine).]")
