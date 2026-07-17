---
title: "Protection, Safety Factors & Derating"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-17
status: unverified
evidence: single-study
sources: [sources/power-electronics/pimpale-mahadik-2025-asc-discharge]
tags: [power-electronics, traction-inverter, protection, sizing, iso, aec-q, sic, design]
review_by: 2026-10-17
---

## What This Is

Every protection layer and the **safety factors / derating** behind them. Consolidates the safety threads from [[power-electronics/traction-inverter/design-procedure]] §7, [[power-electronics/traction-inverter/gate-driver-design]], and [[power-electronics/traction-inverter/control-schemes]] §6. The baseline utilization — **800 V bus on 1200 V SiC = 67% of rating** — is the anchor; this chapter is why 67%, not 85%, is the sweet spot.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge.

## 1. Voltage Derating — Cosmic-Ray Single-Event Burnout (SEB)

The hard reason SiC is not run near its rated voltage even when *static* blocking looks fine:

- **Mechanism:** terrestrial neutrons (cosmic-ray showers) strike the biased drift region; the charge track under high field triggers avalanche/filamentation → burnout. A **field-driven, device-OFF** failure, independent of switching [121].
- **Steep FIT vs voltage:** failure rate is ~flat to ~50–60% BV, has a knee near **~70–80% BV**, then rises ~exponentially toward BV [121]. Heavy-ion SEB onset on 1200 V SiC is ~525 V (~44% BV) for baseline epi [121] (heavy-ion is a conservative lower bound, not neutron FIT).
- **The lever is voltage class:** a 2 kV SiC has ~10× lower cosmic-ray FIT than 1700 V at the same bus [121]; modern Gen-4 die claim up to 100× FIT improvement [121].
- **Rule:** keep **static DC bus ≤ 70–80% of Vds** → 800 V/1200 V (67%) sits below the knee [121][122]. Cosmic-ray SEB is a **separate accelerated-neutron test**, not covered by standard HTRB in AQG 324/AEC-Q101 [121].

## 2. Current & Thermal Derating

- **Tj,max 175 °C** (some 200 °C); design worst-case peak to ~150–160 °C [122].
- **Continuous ID** is quoted at 25 °C and **derates to zero as Tj→Tj,max**: `ID,cont ∝ √((Tj,max−Tc)/(Rth·RDS(on)))` [122], [[power-electronics/traction-inverter/thermal-design]] §6.
- **Peak/overload** is `Zth(pulse)`-limited and far higher than continuous — size the RMS envelope on continuous, the launch burst on `Zth(t)` [122].

## 3. Overcurrent / Short-Circuit

- **SCWT < 3 µs** (Wolfspeed FM3: **2.9 µs @ 800 V/175 °C**), falls with bus voltage; critical SC energy ~constant ~**1.4 J** [110]. Fault current `ID,sat ≈ 1050 A (>11× rated)` [110].
- **DESAT** detects in ~300 ns; detect+**soft turn-off must finish inside 1–3 µs** [110][126], [[power-electronics/traction-inverter/gate-driver-design]] §3.
- **Failure if too slow:** thermal runaway (top-metal reflow→short), gate-oxide crack, parasitic-BJT latch [110].

## 4. Overvoltage

- **Turn-off overshoot** `ΔV = Lσ·di/dt`, dominated by power-loop stray inductance; keep VDS peak within **±5% of bus** by low-`Lσ` layout + `Rg` tuning [110][125], [[power-electronics/traction-inverter/design-procedure]] §8.
- **Clamping:** active gate clamp (variable Rg/V/I), gate-drain TVS active clamp, Miller clamp, RC/RCD snubber [125].
- **Regen bus pumping:** layered thresholds — brake chopper ON/OFF with hysteresis (e.g. 1170/1140 V on a 1200 V link), hard crowbar ~1250 V, trip at ~90–95% of the OV limit with 3–8% hysteresis; chopper needs its own diagnostics [125].

## 5. Safe States — ASC vs Freewheel (PMSM)

| | **Freewheel** (all off, terminals open) | **ASC** (all low- or high-side ON, terminals shorted) |
|--|------------------------------------------|-------------------------------------------------------|
| DC-link | back-EMF rectifies through body diodes → **overvolts at speed** | **no bus pumping** |
| Torque/current | low steady | large **entry transient** (several× steady) + drag torque |
| Use | **low speed** (back-EMF < bus) | **medium/high speed** [123][55] |

Common strategy: freewheel at low speed, ASC at high speed; hybrid schemes inject freewheel intervals to damp the ASC entry transient [123]. ASC drag torque peaks near a corner speed, falls ~1/ω [123], [[sources/power-electronics/pimpale-mahadik-2025-asc-discharge]].

## 6. Functional Safety (ISO 26262)

- **ASIL:** unintended acceleration/torque (esp. from standstill) = **ASIL D**; loss-of-torque / unintended braking ≈ ASIL C [124][85].
- **Timing:** ASIL-D traction hazards use **FTTI ≈ 200 ms** (representative, item-specific — *not* a standard constant) = FDTI (detect) + FRTI (react); gate-driver SC reaction <2 µs is ~10⁵× inside it [124].
- **EGAS 3-level monitoring** (no torque sensor added): L1 torque control; **L2 independent torque plausibility** (commanded vs estimated); L3 µC self-check (independent watchdog, question-answer) [124].
- **Safe-state actuators:** ASC/freewheel via the gate driver (§5); ASIL-C/D gate drivers carry desat, UVLO, soft-off, safe-state pins [124].

## 7. Qualification (component level — feeds FuSa, distinct from it)

- **AEC-Q101** — discrete SiC MOSFET stress qual: HTRB, HTGB, H3TRB, IOL/power-temp-cycle [89].
- **AQG 324** (ECPE) — power-**module** qual: power cycling (PCsec/PCmin), thermal shock/cycling, HTRB/HTGB/H3TRB; **end-of-life = +5% Vf or +20% Rth**; modern sintered/Al-bond modules reach **>100k cycles at ΔTj=100 K, Tvj=175 °C** [88].
- Driver ICs → AEC-Q100; passives → AEC-Q200 [89].

## 8. Consolidated Safety-Factor / Derating Table

| Parameter | Rating | Operating limit | Margin | Cite |
|-----------|--------|-----------------|--------|------|
| DC bus vs Vds (static/cosmic-ray) | 1200 V | ≤70–80% → **800 V (67%)** | below SEB knee | [121][122] |
| Transient VDS (incl. overshoot) | 1200 V | within **±5%** of bus; clamp < BV | (BV−bus) ≈ 400 V | [110][125] |
| Junction temp Tj | 175 °C | design **~150–160 °C** peak | ~15–25 °C | [122] |
| Continuous current | ID@25 °C | Zth-derated → 0 at Tj,max | thermal-limited | [122] |
| Short-circuit | SCWT <3 µs, ~1.4 J | trip in **1–3 µs**; desat ~300 ns | ~7× energy | [110][126] |
| DC-link OV (regen) | cap/device limit | chopper ~1170/1140 V, crowbar ~1250 V | 3–8% hyst | [125] |
| Isolation (800 V) | per creepage | reinforced, ≥~1.4–2× working-V margin `[T]` | ≥40–100% | [86][113] |
| FuSa timing | FTTI ~200 ms (ASIL-D) | gate-driver reaction <2 µs | ~10⁵× inside | [124] |

## Red Team

**Steelman against:** The table reads authoritatively, but several load-bearing numbers are generalized from single sources or vendor framing. The "70–80% SEB knee" is Infineon marketing plus a heavy-ion (not neutron) threshold; "2.9 µs/1.4 J" is one specific module at one condition; "FTTI 200 ms" is a secondary summary, not the ISO 26262 text; the isolation ≥1.4–2× margin is convention, not a cited value.

**How it could be false:**
1. **Cosmic-ray knee is device-specific:** the actionable number is the chosen MOSFET's **neutron-FIT-vs-Vdc curve** (target e.g. <100 FIT), not a generic 70–80% [121].
2. **SCWT is condition-bound:** 2.9 µs/1.4 J is CAB016M12FM3 at 175 °C/VGS=15/Rg=4 Ω [110]; hotter start or another die gives shorter withstand.
3. **FTTI 200 ms is representative, not required** — the real value comes from the vehicle HARA; do not quote as a standard [124].
4. **Isolation margin `[T]`** is a design convention, not a single standard number [86].

**What would change my mind:** the target device's cosmic-ray reliability datasheet; SCWT at worst-case Tj/VGS; the item-level HARA fixing FTTI and ASIL; AQG 324 power-cycling targets for the chosen module class.

**Residual doubt:** The *layering* (voltage/thermal/SC/OV/safe-state/FuSa/qual) and the *directions* are solid and well-sourced. Specific thresholds are illustrative — replace each with the chosen part's datasheet and the vehicle HARA before design freeze.

---

> **References:** [[citations]]

← [[power-electronics/traction-inverter/gate-driver-design]] | [[power-electronics/traction-inverter/design-procedure]] | [[power-electronics/traction-inverter/standards-and-compliance]] →
