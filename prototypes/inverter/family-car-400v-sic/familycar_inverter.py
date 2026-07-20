"""
SRTP "FamilyCrossover" traction-inverter design-by-doing model.
RAG source: srtp_docs/power-electronics/traction-inverter + undergrad vehicle/PE physics.

Produces the simulation-backed numbers the vault defers to PLECS:
  - vehicle road-load -> motor (T,w) operating points (NOT in vault; new)
  - MTPA + field-weakening dq solver
  - inverter conduction + switching loss -> efficiency (SiC vs Si-IGBT)
  - 3 voltage corners, a synthetic mixed drive cycle, DC-link ripple, Tj at peak
"""
import numpy as np

g = 9.81

# ----------------------------------------------------------------------------
# 1. INVENTED VEHICLE: C-segment family crossover, FWD single motor
# ----------------------------------------------------------------------------
veh = dict(
    m      = 1850.0,   # test mass incl driver+pax [kg]
    Cd     = 0.29,     # drag coeff
    Af     = 2.30,     # frontal area [m^2]
    Cr     = 0.010,    # rolling resistance coeff
    rho    = 1.20,     # air density [kg/m^3]
    rw     = 0.32,     # wheel radius [m]
    ig     = 9.0,      # single-speed gear ratio
    eta_gb = 0.97,     # gearbox efficiency
)

def road_load_force(v, a=0.0, grade=0.0):
    """Tractive force at the wheels [N] for speed v[m/s], accel a[m/s^2], grade[rad]."""
    F_roll = veh['m']*g*veh['Cr']*np.cos(grade)
    F_agrade = veh['m']*g*np.sin(grade)
    F_aero = 0.5*veh['rho']*veh['Cd']*veh['Af']*v*v
    F_acc  = veh['m']*a
    return F_roll + F_agrade + F_aero + F_acc

def wheel_to_motor(v, Fwheel):
    """(v[m/s], wheel force) -> (motor mech speed wm[rad/s], motor torque Tm[Nm])."""
    wm = v*veh['ig']/veh['rw']
    # motoring: torque reduced by gearbox eff going wheel->motor is /eta on demand
    Twheel = Fwheel*veh['rw']
    if Fwheel >= 0:
        Tm = Twheel/(veh['ig']*veh['eta_gb'])
    else:  # regen: gearbox eats a share the other way
        Tm = Twheel*veh['eta_gb']/veh['ig']
    return wm, Tm

# ----------------------------------------------------------------------------
# 2. INVENTED IPMSM (scaled from vault machine-and-load typical ranges)
# ----------------------------------------------------------------------------
mot = dict(
    Pp     = 4,          # pole pairs
    Rs     = 0.015,      # stator resistance [ohm]
    Ld     = 0.15e-3,    # d-axis inductance [H]
    Lq     = 0.30e-3,    # q-axis inductance [H]
    lam    = 0.075,      # PM flux linkage [Wb]
    Is_max = 400.0,      # max phase current [A rms]
    wm_max = 14000*2*np.pi/60,  # max mech speed [rad/s]
)
Ip_max = mot['Is_max']*np.sqrt(2)   # peak phase-current amplitude [A]

def torque(id_, iq):
    return 1.5*mot['Pp']*(mot['lam']*iq + (mot['Ld']-mot['Lq'])*id_*iq)

def voltage_mag(id_, iq, we):
    vd = mot['Rs']*id_ - we*mot['Lq']*iq
    vq = mot['Rs']*iq + we*(mot['Ld']*id_ + mot['lam'])
    return np.hypot(vd, vq)

def solve_operating_point(Tdem, wm, Vdc):
    """Return dict of dq currents / voltages / mod index for torque demand Tdem at wm, Vdc.
       Implements MTPA, current limit, then field-weakening under the voltage ceiling."""
    we = mot['Pp']*wm
    Vmax = Vdc/np.sqrt(3.0)          # linear SVPWM phase-voltage peak
    sign = 1.0 if Tdem >= 0 else -1.0
    Tt = abs(Tdem)

    # search current angle beta (from q-axis, id=-Ip*sin b, iq=+Ip*cos b) and amplitude
    best = None
    for Ip in np.linspace(1.0, Ip_max, 160):
        for beta in np.linspace(0.0, np.radians(89.0), 160):
            id_ = -Ip*np.sin(beta)
            iq  =  Ip*np.cos(beta)*sign
            Te = torque(id_, iq)
            if abs(Te) < Tt-0.5:      # not enough torque yet
                continue
            if voltage_mag(id_, iq, we) > Vmax*1.001:
                continue
            # feasible: prefer minimum current (MTPA), tie-break lower |id|
            key = (Ip, abs(id_))
            if best is None or key < best[0]:
                best = (key, id_, iq, Ip)
            break   # smallest Ip that reaches torque at this beta; move to next Ip
    if best is None:
        # voltage/current limited: find max achievable torque within limits
        bt, bid, biq = 0.0, 0.0, 0.0
        for Ip in np.linspace(1.0, Ip_max, 120):
            for beta in np.linspace(0.0, np.radians(89.0), 120):
                id_ = -Ip*np.sin(beta); iq = Ip*np.cos(beta)*sign
                if voltage_mag(id_, iq, we) > Vmax*1.001: continue
                Te = abs(torque(id_, iq))
                if Te > bt:
                    bt, bid, biq = Te, id_, iq
        id_, iq, Ip = bid, biq, np.hypot(bid, biq)
        Te = bt*sign
        limited = True
    else:
        _, id_, iq, Ip = best
        Te = torque(id_, iq)
        limited = False

    Irms = Ip/np.sqrt(2.0)
    Vph  = voltage_mag(id_, iq, we)
    mi   = Vph/(Vdc/np.sqrt(3.0)) if Vdc > 0 else 0.0     # modulation index (1.0 = linear limit)
    Pmech = Te*wm
    # electrical input power to motor ~ mech + copper (iron neglected at this layer)
    Pcu = 3*Irms**2*mot['Rs']
    Pelec = Pmech + Pcu
    cosphi = Pelec/(3*(Vph/np.sqrt(2))*Irms) if Irms > 1 else 0.9
    cosphi = float(np.clip(cosphi, -1, 1))
    return dict(id=id_, iq=iq, Ip=Ip, Irms=Irms, Te=Te, we=we, Vph=Vph, mi=mi,
                Pmech=Pmech, Pelec=Pelec, cosphi=cosphi, limited=limited)

# ----------------------------------------------------------------------------
# 3. DEVICE LOSS MODELS (datasheet-class; per switch position)
#    SiC 750V module ~600-800A class ; Si-IGBT 750V/820A class comparator
# ----------------------------------------------------------------------------
def rds_sic(Tj):   # positive tempco
    return 2.7e-3*(1 + 0.006*(Tj-25))          # ~4.5 mOhm at 150C

SIC = dict(name='SiC 750V', kind='mosfet', fsw=12e3,
           Vref=400.0, Iref=400.0, Esw_ref=9.0e-3,   # Eon+Eoff @400V,400A,150C [J]
           rth=0.30)                                  # jc+ch+cooler per switch [K/W]
IGBT = dict(name='Si-IGBT 750V', kind='igbt', fsw=8e3,
            Vref=400.0, Iref=400.0, Esw_ref=32.0e-3,  # Eon+Eoff+Err
            Vce0=0.9, Rce=2.5e-3, Vf0=1.0, Rd=1.8e-3, rth=0.30)

def inverter_loss(op, Vdc, dev, Tj=150.0):
    """Total inverter semiconductor loss [W] for an operating point."""
    Ip, Irms, mi, cosphi = op['Ip'], op['Irms'], min(op['mi'],1.0), op['cosphi']
    # --- conduction ---
    if dev['kind'] == 'mosfet':
        Rds = rds_sic(Tj)
        Pcond = 3*Irms**2*Rds                     # channel carries phase rms, both quadrants
    else:
        # split IGBT / diode by modulation & power factor (standard averaged formulas)
        Ig_avg = Ip*(1/(2*np.pi) + mi*cosphi/8)
        Ig_rms = Ip*np.sqrt(1/8 + mi*cosphi/(3*np.pi))
        Id_avg = Ip*(1/(2*np.pi) - mi*cosphi/8)
        Id_rms = Ip*np.sqrt(max(1/8 - mi*cosphi/(3*np.pi), 0.0))
        Pigbt = dev['Vce0']*Ig_avg + dev['Rce']*Ig_rms**2
        Pdio  = dev['Vf0']*Id_avg + dev['Rd']*Id_rms**2
        Pcond = 6*(Pigbt + Pdio)
    # --- switching (linear in switched current & voltage; |i| avg = (2/pi)Ip) ---
    Ksw = dev['Esw_ref']/dev['Iref']
    Psw = 3*dev['fsw']*Ksw*(Vdc/dev['Vref'])*(2/np.pi)*Ip
    return Pcond + Psw, Pcond, Psw

# ----------------------------------------------------------------------------
# 4. QUICK VEHICLE PERFORMANCE CHECK
# ----------------------------------------------------------------------------
print("="*74)
print("VEHICLE / MOTOR SANITY")
print("="*74)
v_top = 160/3.6
F_top = road_load_force(v_top)
print(f"Top-speed 160 km/h: road force {F_top:6.0f} N -> power {F_top*v_top/1000:5.1f} kW (steady)")
wm_top, Tm_top = wheel_to_motor(v_top, F_top)
print(f"  motor at top speed: {wm_top*60/2/np.pi:6.0f} rpm, {Tm_top:5.1f} Nm")
# peak launch torque available:
op0 = solve_operating_point(1e9, 50*2*np.pi/60, 355)  # ask 'infinite' torque -> current-limited
print(f"Peak motor torque (Is_max, low speed): {op0['Te']:6.1f} Nm  (id={op0['id']:.0f}, iq={op0['iq']:.0f} A)")
# peak power at base speed:
wm_base = 4500*2*np.pi/60
opb = solve_operating_point(op0['Te'], wm_base, 355)
print(f"Peak power at 4500 rpm base: {opb['Te']*wm_base/1000:5.1f} kW (T={opb['Te']:.0f} Nm, mi={opb['mi']:.2f})")

# ----------------------------------------------------------------------------
# 5. THREE VOLTAGE CORNERS at peak-power demand
# ----------------------------------------------------------------------------
print("\n"+"="*74)
print("EFFICIENCY AT 3 DC CORNERS  (peak-power operating point)")
print("="*74)
Ppk_target = 130e3
for Vdc, tag in [(280,'low-line'),(355,'nominal'),(420,'high-line')]:
    # find a high-speed operating point near peak power at this bus
    wm = 6000*2*np.pi/60
    # torque so that T*wm ~ Ppk
    Tdem = Ppk_target/wm
    for dev in (SIC, IGBT):
        op = solve_operating_point(Tdem, wm, Vdc)
        Ploss,Pc,Ps = inverter_loss(op, Vdc, dev)
        Pel = op['Pelec']
        eta = Pel/(Pel+Ploss)*100
        print(f"  {tag:9s} {dev['name']:12s}: P_el={Pel/1000:5.1f}kW Irms={op['Irms']:3.0f}A "
              f"mi={op['mi']:.2f} loss={Ploss:5.0f}W (cond {Pc:.0f}/sw {Ps:.0f}) eta={eta:5.2f}%")

# ----------------------------------------------------------------------------
# 6. THERMAL at continuous + peak
# ----------------------------------------------------------------------------
print("\n"+"="*74)
print("THERMAL (per-switch loss -> Tj, coolant 65C)")
print("="*74)
Tcool=65
for label, Pdem, wm_rpm in [("continuous 55kW", 55e3, 8000),("peak 130kW",130e3,6000)]:
    wm=wm_rpm*2*np.pi/60; Tdem=Pdem/wm
    for dev in (SIC,IGBT):
        op=solve_operating_point(Tdem,wm,355)
        Ploss,Pc,Ps=inverter_loss(op,355,dev)
        Tj=Tcool+(Ploss/6)*dev['rth']
        print(f"  {label:16s} {dev['name']:12s}: loss {Ploss:5.0f}W  Tj~{Tj:5.0f}C")

# ----------------------------------------------------------------------------
# 7. DC-LINK RIPPLE (Kolar approx) at peak
# ----------------------------------------------------------------------------
print("\n"+"="*74); print("DC-LINK RIPPLE"); print("="*74)
op=solve_operating_point(130e3/(6000*2*np.pi/60),6000*2*np.pi/60,355)
m=min(op['mi'],1.0); cph=op['cosphi']; Iph=op['Irms']
Icap = Iph*np.sqrt(2*m*(np.sqrt(3)/(4*np.pi) + cph**2*(np.sqrt(3)/np.pi - 9*m/16)))
print(f"  Iph={Iph:.0f}A rms, m={m:.2f}, cosphi={cph:.2f} -> I_cap,rms ~ {Icap:.0f} A")

# ----------------------------------------------------------------------------
# 8. SYNTHETIC MIXED DRIVE CYCLE  (representative, NOT the official WLTP trace)
# ----------------------------------------------------------------------------
def ramp(v0,v1,t): return list(np.linspace(v0,v1,int(t)))
def hold(v,t): return [v]*int(t)

def cycle_urban():
    """Urban-heavy stop-go, mean ~ 30 km/h (WLTP-Low-like)."""
    seg=[]
    for _ in range(8):
        seg += ramp(0,35,7)+hold(35,8)+ramp(35,15,4)+hold(15,6)+ramp(15,50,8)+hold(50,10)+ramp(50,0,7)+hold(0,6)
    return np.array(seg,dtype=float)

def cycle_mixed():
    """Mixed urban+suburban+highway, mean ~ 48 km/h (WLTP-class-like)."""
    seg=[]
    for _ in range(3):
        seg += ramp(0,40,8)+hold(40,10)+ramp(40,0,6)+hold(0,5)          # urban
    seg += ramp(0,70,15)+hold(70,50)+ramp(70,45,7)+hold(45,25)+ramp(45,80,14)+hold(80,45)+ramp(80,0,12)  # suburb
    seg += ramp(0,110,24)+hold(110,70)+ramp(110,120,10)+hold(120,40)+ramp(120,0,22)                       # highway
    return np.array(seg,dtype=float)

Vdc=355; dt=1.0
def run_cycle(vt, label):
    a=np.gradient(vt/3.6,dt); v=vt/3.6
    E_loss={SIC['name']:0.0,IGBT['name']:0.0}; E_elec={SIC['name']:0.0,IGBT['name']:0.0}
    dist=np.trapz(v,dx=dt); mot_t=0
    for i in range(len(v)):
        if v[i]<0.1: continue
        F=road_load_force(v[i],a[i]); wm,Tm=wheel_to_motor(v[i],F)
        if wm<1: continue
        op=solve_operating_point(Tm,wm,Vdc)
        for dev in (SIC,IGBT):
            Ploss,_,_=inverter_loss(op,Vdc,dev)
            E_loss[dev['name']]+=Ploss*dt; E_elec[dev['name']]+=abs(op['Pelec'])*dt
        if Tm>0: mot_t+=1
    print(f"\n  {label}  ({len(v)} s, {dist/1000:.2f} km, mean {np.mean(v)*3.6:.1f} km/h, "
          f"motoring {mot_t/len(v)*100:.0f}%)")
    for dev in (SIC,IGBT):
        n=dev['name']; eta=E_elec[n]/(E_elec[n]+E_loss[n])*100
        print(f"    {n:12s}: inv-loss {E_loss[n]/3600:5.1f} Wh  cycle-avg inv-eff {eta:5.2f}%")
    d=(E_loss[IGBT['name']]-E_loss[SIC['name']])/3600
    print(f"    -> SiC saves {d:5.1f} Wh = {d/(dist/1000)*100:5.1f} Wh/100km (inverter only)")

print("\n"+"="*74); print("DRIVE CYCLES (synthetic, representative; NOT official WLTP traces)"); print("="*74)
run_cycle(cycle_urban(),"URBAN-heavy")
run_cycle(cycle_mixed(),"MIXED")
