import numpy as np, json, sys
# usage: gen_vars.py Vdc Vg_rms Pr [fac fs Ta kL_pu]
# replicates bench InitializationCommands so a corner override is fully consistent
# (model_vars are applied AFTER init, so every block-referenced var must be passed).
a=sys.argv
Vdc=float(a[1]); Vg_rms=float(a[2]); Pr=float(a[3])
fac=float(a[4]) if len(a)>4 else 200.0
fs =float(a[5]) if len(a)>5 else 16e3
Ta =float(a[6]) if len(a)>6 else 65.0
kL_pu=float(a[7]) if len(a)>7 else 0.5

Vg_peak=Vg_rms*np.sqrt(2)
Zb=Vg_rms**2/Pr
Lg=kL_pu*Zb/(2*np.pi*fac)
Rg=0.01*Zb
Zinv=Rg+1j*2*np.pi*fac*Lg
Iref=Pr/(3*Vg_rms)
Vinv=Vg_rms+Iref*Zinv
Vinv_rms=abs(Vinv); Vinv_angle=float(np.angle(Vinv))
pb=[0.0,-2*np.pi/3,2*np.pi/3]
Vref=Vinv_rms*np.sqrt(2)
phase_sine=[p+Vinv_angle for p in pb]
phase_svpwm=[p+Vinv_angle+2*np.pi*(fac/fs/2) for p in pb]
Iout=Iref*np.sqrt(2); Iband_hyst=Iout*0.2

mv={"Vdc":Vdc,"Vg_rms":Vg_rms,"Vg_peak":Vg_peak,"Pr":Pr,"fac":fac,"fs":fs,"Ta":Ta,
    "Zb":Zb,"Lg":Lg,"Rg":Rg,"Iref":Iref,"Vref":Vref,
    "phase_sine":phase_sine,"phase_svpwm":phase_svpwm,"phase_hyst":pb,
    "Iout":Iout,"Iband_hyst":Iband_hyst,"Rcs_val":0.0267}
# m (modulation index) diagnostic
m=Vref/(Vdc/2)
sys.stderr.write(f"Iref={Iref:.1f}A  Vref={Vref:.1f}V  m={m:.3f}  Lg={Lg*1e6:.1f}uH  Zb={Zb:.4f}\n")
print(json.dumps(mv))
