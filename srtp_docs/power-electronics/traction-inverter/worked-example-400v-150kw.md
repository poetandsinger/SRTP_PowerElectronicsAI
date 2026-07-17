---
title: "Worked Example — 400V SiC 2L-B6, 150 kW"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-17
status: unverified
evidence: theoretical
tags: [power-electronics, traction-inverter, design, sizing, two-level, sic, example]
review_by: 2026-10-17
---

## What This Is

The [[power-electronics/traction-inverter/design-procedure]] applied a **second time**, at 400 V, for the same 150 kW as the 800 V anchor ([[power-electronics/traction-inverter/reference-design-2l-b6-sic-800v]]). Side-by-side, it shows the single biggest voltage-class lesson: **halving the bus doubles the current, and I²R conduction loss dominates.** Grounded against the 400 V production designs [94][95].

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; `[derived]` → computed here from the cited relations in [[power-electronics/traction-inverter/design-procedure]].

## Spec (400 V variant)

| Input | Value | vs 800 V anchor |
|-------|-------|-----------------|
| Vdc | 350 V nom (280–420 V) | half |
| Power | 150 kW peak | same |
| Device | **650 V SiC** (Tesla-class) or 750 V for margin | vs 1200 V |
| fsw | 16 kHz | same |
| Motor | IPMSM, Is,max ≈ 480 A rms | ~2× current |

## Operating Points [derived]

- **Max linear V_LL,rms** = Vdc/√2 = 350/√2 = **247 V** [50].
- **Phase current at peak power** = 150000 / (√3·235·0.9) ≈ **410 A rms** (~580 A peak) — vs ~192 A rms at 800 V. **~2.1× the current** for the same power [derived].
- **Launch corner** Is,max ≈ 480 A rms (~680 A peak) → module needs ~600–800 A, or two 450 A modules paralleled per switch [derived].

## Device [derived]

- **Voltage:** worst-case 420 V + overshoot (Lσ·di/dt ≈ 120 V at the higher di/dt) ≈ 540 V → 540/650 = **83%** of a 650 V device (tight; 750 V gives comfortable 72%). Tesla ships 650 V here [94]; a clean-sheet design would weigh 750 V for cosmic-ray margin [T][89].
- **Current:** ~2× the 800 V design → **more silicon or paralleling**, the root of the 400 V cost/thermal penalty.

## Losses [derived] — the headline

| Loss | 400 V (this) | 800 V anchor | Why |
|------|-------------:|-------------:|-----|
| Conduction (6×) | ≈ **1.5 kW** | ≈ 0.55 kW | I² term: 2.1× current → ~4.4× I²R (partly offset by lower Rds of 650 V die) [25] |
| Switching (6×) | ≈ **0.24 kW** | ≈ 0.38 kW | E_sw scales with bus V → **lower** at 400 V [25] |
| Total | ≈ **1.75 kW** | ≈ 1.0 kW | conduction now dominates |
| Inverter efficiency @150 kW | ≈ **98.8%** | ≈ 99.3% | ~0.5 pt lower [derived] |

**Lesson:** at 400 V, **conduction (I²R) dominates and efficiency drops**; at 800 V, loss shifts to switching (which SiC handles cheaply) and total loss falls. This is the quantitative core of the 800 V migration [28], [[power-electronics/traction-inverter/design-tradeoffs]] §2. Cross-check: 400 V production inverters run ~95–98% system efficiency [95][94] — consistent once motor and cycle losses are added.

## DC-Link & Busbar [derived]

- **Ripple current** ≈ 0.6·410 ≈ **246 A rms** — ~2× the 800 V case → a **bigger cap bank** (≈600–1000 µF class). This matches the ~1088 µF seen in the 400 V IGBT Leaf [95] (IGBT's lower fsw needs even more) [84].
- **Busbar:** 2× current makes the `Lσ < 15 nH` budget harder and I²R busbar loss 4× — laminated busbar and short commutation loops are more critical, not less [25], [[power-electronics/traction-inverter/design-procedure]] §8.

## When 400 V Still Wins

Despite the penalty, 400 V is rational for **cost-first, <100–150 kW, high-volume** vehicles: mature 650 V devices, cheaper isolation, huge ecosystem — exactly Tesla Model 3/Y's choice and most Chinese BEVs [94], [[power-electronics/traction-inverter/design-tradeoffs]] §2. The penalty is efficiency/density, not viability.

## Red Team

**Steelman against:** Every number is closed-form on `[T]` motor/device assumptions, like the 800 V anchor — provisional until PLECS. The efficiency delta (99.3% vs 98.8%) is within the uncertainty of the loss model itself [25]; presenting a 0.5-point difference as decisive overstates the precision. Rds(on) of the 650 V die was assumed lower than the 1200 V die, which drives the conduction comparison and is not pinned to a datasheet here.

**How it could be false:**
1. **Loss-model precision:** ±20–40% on analytic Eon/Eoff and Rds(Tj) [25] swamps a 0.5-point efficiency gap — the *direction* (conduction-dominated at 400 V) is robust; the *magnitude* is soft.
2. **Assumed device parameters `[T]`:** 650 V Rds and Esw are class estimates, not a specific module datasheet.
3. **Is,max ≈ 480 A `[T]`:** the launch corner drives module sizing and is a placeholder.

**What would change my mind:** a PLECS 400 V model with real 650 V SiC device data reproducing the conduction-dominated loss split and the ~98.8% figure.

**Residual doubt:** The qualitative lesson — 400 V doubles current, conduction dominates, efficiency and density drop, cost falls — is solid and matches production data [94][95]. The exact efficiency numbers are a hypothesis for PLECS.

---

> **References:** [[citations]]

← [[power-electronics/traction-inverter/design-procedure]] | [[power-electronics/traction-inverter/reference-design-tesla-model3-400v-sic]] | [[power-electronics/traction-inverter/design-tradeoffs]] →
