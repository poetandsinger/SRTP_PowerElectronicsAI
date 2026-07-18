---
title: "Worked Example — Performance/Hypercar Inverter (800 V SiC, power-density & Zth-pulse)"
type: topic
field: power-electronics
created: 2026-07-18
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, design, sic, thermal, junction-temperature, efficiency, example]
review_by: 2026-10-17
---

## What This Is

A worked example driven by **power density (kW/L) and how long a peak far above the continuous rating holds** — set by transient `Zth(t)` (thermal mass), *not* drive-cycle efficiency. It exercises the `Zth`-pulse logic in [[thermal-design]] §2 against a **real anchor**: the Porsche Taycan Turbo GT publishes **815 kW/2 s, 700 kW/10 s, 580 kW continuous** [158][H] — a textbook duration-gated peak. Runnable model: `worked-designs/performance-800v-sic/perf_zth.py`.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training/undergrad; `[model]` → computed; web specs **[H]/[M]/[mkt]**.

## 1. The Application (real-grounded)

Full sourced survey: [[segment-performance-motorsport-inverters]].

| Item | Value | Basis |
|------|-------|-------|
| Bus | 800–900 V | Taycan 800 V [158]; Lucid/FE-Gen3 ~900 V [H] |
| Power (per inverter) | ~400 kW continuous, **~1.1–1.6× peak for seconds** | model, anchored to [158] |
| Device / cooling | 1200 V SiC, **double-side-cooled (DSC)** + sintered-Ag + micro-channel | the density enablers [160][H] |
| Metric | **kW/L, kW/kg** + peak-duration | DOE 13→34→**100 kW/L** [159][H] |

Real density anchors: Wolfspeed 300 kW SiC reference ≈ **33 kW/L** [160][H]; **100 kW/L** double-side-cooled + sintered-Ag demonstrator (lab) [160]. Vendor superlatives (McLaren ">125 kVA/L" — note **kVA not kW**; YASA "~100 kW/kg inverter") are `[mkt]` and inflated [performance research].

## 2. The Workflow — Transient Thermal, Not Efficiency  `[model]`

Continuous rating = highest power with steady `Tj ≤ 160 °C`; **peak** is `Zth(t)`-gated from a cruise baseline:

| peak / continuous | peak kW | sustainable burst | ← the shape |
|:-----------------:|--------:|-------------------|-------------|
| 1.10× | 457 | ~15 s | matches |
| 1.25× | 519 | ~2.5 s | Porsche |
| 1.40× | 581 | ~1 s | 815 kW/2 s |
| 1.60× | 664 | <0.5 s | 700 kW/10 s |

Continuous ≈ **415 kW** (steady `Tj` 160 °C) [model]. **Higher peak ⇒ shorter burst** — the model reproduces the Porsche duration-gating from thermal mass alone. **Power density** (volume derived from *sourced* densities, not invented): a 581 kW-peak inverter is **17.6 L** at single-side 33 kW/L, **9.7 L** at DSC ~60 kW/L, **5.8 L** at the DOE 100 kW/L target [159][160].

## 3. Circuit / Device / BOM (deltas)

2L-B6 with **minimum silicon at maximum flux**: small-die 1200 V SiC on **double-side cooling** (coolers both faces, sintered-Ag interposers, micro-channel cold plate) — `Rth` −30–39% vs single-side, the lever that buys kW/L ([[thermal-design]] §4, [103]). Highest practical `fsw` (~15 kHz) to shrink passives; **laminated busbar with lowest `Lσ`** for the 900 A-class edges. DC-link and gate-drive are the [[bom]] classes, minimized in volume. Multiple such inverters per car (Rimac = 4, Plaid = 3) [performance research].

## 4. New Knowledge  `[model]`

1. **The peak rating is a *time*, not a number.** The model reproduces Porsche's 815/2 s → 700/10 s → 580-continuous purely from `Zth(t)` and thermal mass — confirming that a performance inverter's headline "peak kW" is meaningless without its duration, and that the design variable is **thermal capacitance** (how much energy the die+cold-plate absorb) as much as steady `Rth`.
2. **Density figures must be read in the right units and basis.** Separating verified from marketing: SiC SOTA ≈ 33 kW/L single-side [160]; DSC roughly doubles it; McLaren's ">125" is **kVA/L** (~90 kW/L real). A vault that quotes "kW/L" without (peak vs continuous) and (kW vs kVA) will over-state by ~1.4–2×.
3. **This inverter would *lose* the family-car efficiency contest and not care.** Sized for a 1 s burst and minimum volume, it runs hot (`Tj` ~160 °C continuous) and accepts higher loss than a range-optimized design — the inverse trade to WE-1's lifetime margin and the family car's cycle efficiency.

## 5. Report — Compromises

- **Density over efficiency and life:** small hot die + DSC buys kW/L and burst capability, spending junction-temperature margin (hence power-cycling life — the opposite of WE-1) and part-load efficiency.
- **Multiple inverters** (per-axle/per-wheel) for total power + torque vectoring, at BOM/complexity cost.
- **Peak is thermally rationed:** the control must budget the burst against `Zth` energy and recover — a launch/lap logic absent from a commuter car.
- **Process contrast:** the family car optimized η at fixed corners; the truck optimized ΔTj over a mission; **this one optimizes volume + a transient `Zth` budget** — a third distinct model and binding constraint (see [[design-by-doing-observed-workflow]]).

## Red Team

**Steelman against:** The burst-duration curve is qualitatively Porsche-shaped but the *exact* seconds are set by my invented Foster thermal-mass values — I could tune 1.25×/2.5 s to 1.2×/10 s by changing capacitances, so the match to 700 kW/10 s is a plausibility demo, not a validation. The kW/L numbers are defensible only because I *derived volume from sourced densities*; the underlying inverter volume is not independently modeled. Continuous "415 kW at Tj 160 °C" rests on an assumed `Rth` and loss params.

**How it could be false:**
1. **Thermal-mass values are unmeasured** — the whole peak-duration curve scales with the Foster `C`s I chose; only the *monotonic* "higher peak → shorter burst" is robust [101].
2. **Density is derived, not modeled:** I used sourced kW/L to get volume; a real design's volume depends on cap bank, busbar, housing, coolant — not just the module [160].
3. **Marketing contamination:** several density superlatives are kVA or prototype/forward claims; even my "sourced" 60 kW/L DSC is a mid-range estimate, not one datasheet [performance research].
4. **Porsche's 580 kW is a *system* (2 inverters);** mapping it to a single-inverter continuous rating is an approximation.

**What would change my mind:** the chosen module's measured `Zth` curve reproducing a target burst; a bill-of-volume for a real 400 kW SiC inverter giving kW/L bottom-up; a datasheet DSC `Rth` at automotive coolant temperature.

**Residual doubt:** The *workflow* (Zth-pulse gates the peak; density from sourced anchors; driver = volume + transient, not efficiency) is sound and the Porsche anchor makes it the best-grounded of the three peaks. The specific burst seconds and kW/L are illustrative, pinned to assumptions and sourced ranges, not a bottom-up model.

---

> **References:** [[citations]] · model: `worked-designs/performance-800v-sic/`

← [[worked-example-truck-800v-sic]] | [[thermal-design]] | [[worked-example-microcar-96v-mosfet]] →
