"""
Corner 7 — Short-circuit fault (850 V hard switch fault / shoot-through, Tj hot).
Pass criterion: fault current & I^2t within the SC-withstand budget (SCWT < 3 us, SiC).

SCOPE (why this corner is analytic/datasheet-bounded, not a PLECS run):
The PLECS MosfetWithDiode is a LOSS model: constant Ron = 3.6 mOhm, NO gm-limited
saturation (verified — the CAB450 XML has no transfer/transconductance table). Turning
a device fully on across 850 V in that model gives I = Vdc/Ron = 850/0.0036 = 236 kA,
which is unphysical. The real SC current is transconductance-limited to ID,sat (a few kA)
and the device survives only for the SC-withstand time. PLECS cannot produce either, so
per plan-depth-research's protection can/cannot table ("SC fault current/energy vs SOA ->
bench/datasheet"), corner 7 is bounded by the datasheet + first principles below.

Anchor: CAB016M12FM3 (16 mOhm FM3-family SiC) — SCWT 2.9 us @ 800 V/175 C, critical SC
energy ~1.4 J, ID,sat ~1050 A (protection-and-safety.md sec.3, [110][126]). Scaled to the
CAB450M12XM3 (2.6 mOhm) by die area (both gfs and thermal mass scale with area).
"""
import numpy as np

# ---- device / operating point ----
Vbus   = 850.0        # corner-7 bus (worst-case high bus)
BV     = 1200.0       # device blocking voltage
Ron    = 3.6e-3       # CAB450 loss-model on-resistance (ohm)
Irated = 450.0        # CAB450 continuous rating (A)
Lsig   = 6.7e-9       # module stray inductance (H) [166]
Tj0    = 175.0        # hot start (C)

# ---- 1. why the loss model can't do this ----
I_unphysical = Vbus/Ron
print(f"[scope] loss-model would give I = Vbus/Ron = {Vbus}/{Ron*1e3:.1f}mOhm = {I_unphysical/1e3:.0f} kA (UNPHYSICAL)")
print(f"        real SC current is gm-limited to ID,sat; the model has no transfer curve -> analytic below.\n")

# ---- 2. scale ID,sat and E_crit from the CAB016 anchor (both ~ die area ~ 1/Ron) ----
Ron_anchor, IDsat_anchor, Ecrit_anchor, SCWT_anchor_800 = 16e-3, 1050.0, 1.4, 2.9e-6
area_ratio = Ron_anchor/Ron                      # CAB450 die is this much bigger
IDsat = IDsat_anchor*area_ratio                  # A
Ecrit = Ecrit_anchor*area_ratio                  # J
print(f"die-area ratio (Ron 16mOhm / 2.6mOhm) = {area_ratio:.2f}x")
print(f"ID,sat(CAB450) ~ {IDsat_anchor:.0f} x {area_ratio:.2f} = {IDsat/1e3:.1f} kA  (~{IDsat/Irated:.0f}x rated {Irated:.0f} A)")
print(f"critical SC energy ~ {Ecrit_anchor} x {area_ratio:.2f} = {Ecrit:.1f} J\n")

# ---- 3. SCWT: take from the datasheet as a TECHNOLOGY property, voltage-scale only ----
# NB: the real SC current is not constant — it peaks then decays as the die self-heats
# (Ron rises, gm falls with T), so E_crit != V*IDsat*SCWT with a constant IDsat (that
# product would give 1.67 us, underestimating the measured 2.9 us). SCWT is therefore
# taken directly from the FM3-family measurement and scaled by bus voltage (P ~ V), not
# derived from the energy product. It is ~die-area-independent (channel/thermal property).
SCWT_850 = SCWT_anchor_800*(800.0/Vbus)           # first-order voltage scaling
print(f"SCWT (measured, FM3-family SiC) = {SCWT_anchor_800*1e6:.1f} us @ 800 V/175 C — ~die-independent tech property")
print(f"SCWT @ {Vbus:.0f} V/175 C ~ {SCWT_anchor_800*1e6:.1f}us x 800/{Vbus:.0f} = {SCWT_850*1e6:.2f} us   (higher bus -> shorter)")
P_SC_pk = Vbus*IDsat                              # peak (initial) SC power/device
print(f"peak SC power/device ~ V*IDsat = {P_SC_pk/1e6:.2f} MW (decays as die heats);  critical energy ~{Ecrit:.1f} J\n")

# ---- 4. protection timing budget: detect + soft turn-off must finish inside SCWT ----
t_desat = 300e-9      # DESAT detection [110][126]
t_softoff = 1.0e-6    # soft (slowed) turn-off
t_react = t_desat + t_softoff
margin = SCWT_850 - t_react
print(f"protection: DESAT {t_desat*1e9:.0f} ns + soft turn-off {t_softoff*1e6:.1f} us = {t_react*1e6:.2f} us reaction")
print(f"  vs SCWT {SCWT_850*1e6:.2f} us  ->  margin {margin*1e6:.2f} us ({SCWT_850/t_react:.1f}x)  {'PASS' if margin>0 else 'FAIL'}\n")

# ---- 5. turn-off overvoltage clearing the fault: dV = Lsig*di/dt, why SOFT off is required ----
V_margin = BV - Vbus
print(f"turn-off overvoltage (clearing {IDsat/1e3:.1f} kA), voltage headroom to BV = {V_margin:.0f} V:")
for label, t_fall in [("soft  (~500 ns)", 500e-9), ("hard  (~100 ns)", 100e-9)]:
    didt = IDsat/t_fall
    dV = Lsig*didt
    frac = dV/V_margin
    ok = f"{frac*100:.0f}% of BV headroom" + ("" if frac < 0.7 else " — uncomfortably close")
    print(f"  {label}: di/dt={didt/1e9:.1f} kA/us -> dV=Lsig*di/dt={dV:.0f} V  ({ok})")
print("  -> soft turn-off is preferred: it keeps dV well inside BV headroom; a hard turn-off of the")
print("     multi-kA fault current pushes VDS to ~90% of the BV margin (avalanche risk if IDsat is higher).\n")

# ---- verdict ----
print("VERDICT (corner 7):")
print(f"  CAB450 @ 850V/175C: ID,sat ~{IDsat/1e3:.1f} kA, SCWT ~{SCWT_850*1e6:.2f} us (<3 us, SiC).")
print(f"  DESAT+soft-off reacts in ~{t_react*1e6:.1f} us, inside SCWT with ~{SCWT_850/t_react:.1f}x margin -> device SURVIVES a single SC.")
print(f"  ~us-scale margin confirms SiC's hard SC-protection need (vs Si IGBT ~10 us); soft turn-off strongly preferred.")
print(f"  [analytic/datasheet — PLECS loss-model cannot represent gm-saturated SC current; scaling flagged +/-30%]")
