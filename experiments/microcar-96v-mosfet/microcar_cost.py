"""
WE-3: A-segment / city microcar traction inverter — COST-DOWN workflow.
Binding constraint: absolute BOM cost / lowest $-per-kW. The dominant lever is
DC-BUS VOLTAGE: the Wuling Mini EV runs a ~96 V pack (research-confirmed), which
enables the cheapest power stage -> LOW-VOLTAGE Si MOSFETs (NOT IGBT/SiC),
minimal isolation, relaxed creepage.

BRUTAL HONESTY: the Wuling *device* (MOSFET) is an ENGINEERING INFERENCE from the
confirmed ~96 V bus, NOT teardown-confirmed. Inverter BOM $ cost is UNSOURCED
(MarkLines paywalled, no Munro city-car inverter) -> NO absolute $ here; only a
STRUCTURAL (relative) cost argument from device-class economics + physics.

Compares the 96 V LV-MOSFET choice against a hypothetical 350 V Si-IGBT build of the
SAME 30 kW, to show what low voltage buys and costs.
"""
import numpy as np

P=30e3            # 30 kW city car (Wuling/Changan class)
cosphi=0.9

def phase_current(Vdc):
    VLL=0.72*Vdc
    Irms=P/(np.sqrt(3)*VLL*cosphi); return Irms, Irms*np.sqrt(2)

def loss_mosfet(Vdc, Rds, fsw, Esw_ref, Iref=200.0, Vref=100.0):
    Irms,Ip=phase_current(Vdc)
    Pcond=3*Irms**2*Rds
    Psw=3*fsw*(Esw_ref/Iref)*(Vdc/Vref)*(2/np.pi)*Ip
    return Pcond,Psw,Irms

def loss_igbt(Vdc, Vce0, Rce, Esw_ref, fsw, Iref=100.0, Vref=350.0):
    Irms,Ip=phase_current(Vdc); m=0.9; cph=cosphi
    Ig_avg=Ip*(1/(2*np.pi)+m*cph/8); Ig_rms=Ip*np.sqrt(1/8+m*cph/(3*np.pi))
    Pcond=6*(Vce0*Ig_avg+Rce*Ig_rms**2)
    Psw=3*fsw*(Esw_ref/Iref)*(Vdc/Vref)*(2/np.pi)*Ip
    return Pcond,Psw,Irms

print("="*72); print("WE-3  CITY MICROCAR INVERTER — COST-DOWN (voltage is the lever)"); print("="*72)

# Option A: 96 V LV Si MOSFET (Wuling-class inference)
Rds_lv=1.0e-3    # ~100 V Si MOSFET, several dies paralleled -> ~1 mOhm/switch [T]
PcA,PsA,IrA=loss_mosfet(96.0, Rds_lv, 10e3, 1.5e-3)
etaA=P/(P+PcA+PsA)*100
# Option B: 350 V Si IGBT (Dacia Spring / Seagull-class) same 30 kW
PcB,PsB,IrB=loss_igbt(350.0, 0.9, 3.0e-3, 8e-3, 8e3)
etaB=P/(P+PcB+PsB)*100

# interconnect (busbar + connectors), ~0.4 mOhm/phase -> the LV current penalty lands HERE (I^2)
Rint=0.4e-3
PiA=3*IrA**2*Rint; PiB=3*IrB**2*Rint
etaA=P/(P+PcA+PsA+PiA)*100; etaB=P/(P+PcB+PsB+PiB)*100
print(f"\n{'':24s}{'96V LV-MOSFET':>16s}{'350V Si-IGBT':>16s}")
print(f"{'phase current (rms)':24s}{IrA:13.0f} A{IrB:13.0f} A")
print(f"{'conduction loss':24s}{PcA:13.0f} W{PcB:13.0f} W")
print(f"{'switching loss':24s}{PsA:13.0f} W{PsB:13.0f} W")
print(f"{'busbar/connector I2R':24s}{PiA:13.0f} W{PiB:13.0f} W  <- LV penalty ({IrA**2/IrB**2:.0f}x)")
print(f"{'inverter efficiency':24s}{etaA:13.2f} %{etaB:13.2f} %")
print(f"  NOTE: switch efficiency is COMPETITIVE (LV MOSFET Rds is tiny); the {IrA/IrB:.1f}x current")
print(f"  penalty of 96 V shows up in INTERCONNECT + DC-link ripple, not the semiconductors.")

print("\n--- WHY LOW VOLTAGE IS THE COST LEVER (structural, not $) ---")
print(f"  * 96 V draws {IrA:.0f} A vs {IrB:.0f} A at 350 V for the same 30 kW ({IrA/IrB:.1f}x current)")
print( "    -> heavier busbar/connectors + larger DC-link RIPPLE current: the LV penalty.")
print( "  * BUT the device: at <~200 V, low-voltage Si MOSFETs beat IGBTs on cost AND")
print( "    conduction (no Vce0 knee); >200 V forces IGBT (or costly SiC). Voltage picks the device class.")
print( "  * 96 V also relaxes isolation/creepage, shrinks the isolated-bias + gate-drive scope,")
print( "    and cuts HV-safety content vs a 350-400 V design -> the real per-unit BOM saving.")
print( "  * SiC appears in NONE of this class (research): its $/A never pays at cost-first, low-power.")

print("\n--- COST STRUCTURE (RELATIVE ONLY — absolute $ is UNSOURCED, do not fabricate) ---")
# relative device $/kW class ranking (general-knowledge ordinal, NOT a quote)
for dev,rel in [("100 V Si MOSFET (LV)","1.0x  (cheapest per kW at low V)"),
                ("650-750 V Si IGBT","~1.5-2x"),
                ("650-750 V SiC MOSFET","~3-4x (SemiInsight late-2025)")]:
    print(f"   {dev:24s}: {rel}")
print("  The trade: LV-MOSFET at 96 V spends EFFICIENCY and POWER DENSITY (huge current,")
print("  bulky DC-link/busbar) to buy the lowest device + isolation + safety BOM. That is")
print("  the defining signature of a cost-first inverter (Wuling ~$4.2k car, >1M units/yr).")
