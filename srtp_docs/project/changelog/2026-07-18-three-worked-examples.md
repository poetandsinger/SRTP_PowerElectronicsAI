---
title: "2026-07-18 — Three more worked examples (truck / performance / microcar)"
type: changelog
field: project
created: 2026-07-18
updated: 2026-07-18
tags: [changelog, power-electronics, design, sic, reliability, thermal, simulation]
---

# 2026-07-18 — Three more worked examples across applications + workflows

Extended the design-by-doing set from 1 to 4, deliberately spanning **different applications and different design workflows**, now with web research (sources documented as found) and brutal red-teaming. Three research subagents gathered real OEM/DOE data; runnable models produced the numbers; the cross-workflow comparison is folded into the observed-workflow note (no standalone comparison file, per the brief).

## New worked examples (each: spec → circuit → device → thermal → BOM → report → red-team + new-knowledge, runnable model)
- **[[power-electronics/traction-inverter/worked-example-truck-800v-sic]]** — Class-8 e-truck, 800 V SiC, eActros-class (600 kW peak / **400 kW continuous**). **Lifetime-driven** workflow (mission → Foster `Tj(t)` → rainflow → Miner). Findings: **daily cold-start dominates power-cycling damage (97%)**, not the grade climbs; life is hyper-sensitive to ΔTj (⁻⁵ power) → design to a **Tj ceiling**, not a km number; **the vault's LESIT closed-form is miscalibrated** (gives ~20 cycles at 100 K) — anchored Coffin-Manson to the empirical datapoint instead.
- **[[power-electronics/traction-inverter/worked-example-performance-800v-sic]]** — hypercar, 800 V SiC. **Power-density + transient-`Zth`** workflow; reproduces the real **Porsche 815 kW/2 s, 700 kW/10 s, 580 kW continuous** duration-gating [158]; kW/L derived from **sourced** densities (DOE 13→34→100 kW/L [159], Wolfspeed 33 kW/L [160]).
- **[[power-electronics/traction-inverter/worked-example-microcar-96v-mosfet]]** — city car, **~96 V LV Si-MOSFET** (Wuling-class). **Cost-down** workflow; **voltage is the cost lever**; the 3.6× LV current penalty lands on **interconnect (13× I²R), not the switches** (LV-MOSFET ~as efficient as a 350 V IGBT). Honest boundary: device is **inference**, inverter BOM cost **unsourced** — a structural argument, no fabricated $.

## Process comparison (folded in, not a separate file)
- **[[ai-agents/design-by-doing-observed-workflow]]** extended n=1 → **n=4**: the pipeline structure (⓪ requirements → ④ report) held every time, but the **objective selected the ③ analysis and the binding gate** (efficiency-corners vs rainflow-lifetime vs `Zth`-pulse vs cost-structure). New **G-N**: a Planner needs an objective→(analysis-model, binding-gate) selector. This also answers that note's own earlier "n=1" Red Team ("2–3 more passes" — now done).

## Executable artifacts (repo, outside the vault)
- `worked-designs/truck-800v-sic/` (truck_lifetime.py: road-load + Foster Zth + ASTM rainflow + Coffin-Manson/Miner), `worked-designs/performance-800v-sic/` (perf_zth.py: Zth-pulse duration curve + density), `worked-designs/microcar-96v-mosfet/` (microcar_cost.py: LV-MOSFET vs IGBT loss/cost structure). Each with results.txt + README.

## Logistics
- **[[citations]]** +[158]–[165] (Porsche, DOE OSTI ×2, Wolfspeed, eActros, HD-lifetime anchors, Wuling, city-car peers); every figure tagged [H]/[M]/[TPS]/[mkt]; OEM-undisclosed inverter internals flagged as inference.
- **[[README]]** citation range → [1]–[165]; index updated.

## Segment landscape notes (RAG backbone)

The online-search findings belong *in* the traction-inverter RAG folder, not just compressed into citations + worked-example intros — the MAS retrieves them. Captured the full sourced industry survey per segment as standalone `topic` notes:
- **[[power-electronics/traction-inverter/segment-heavy-duty-truck-inverters]]** — Class-8 power/voltage/battery per vehicle, mission profiles, lifetime targets; inverter internals undisclosed (flagged).
- **[[power-electronics/traction-inverter/segment-performance-motorsport-inverters]]** — hypercar/FE peak-duration + power-density (verified vs marketing) + DSC cooling.
- **[[power-electronics/traction-inverter/segment-low-cost-city-car-inverters]]** — tri-modal voltage, device-by-voltage, cost/volume; the least-sourced segment, honestly flagged.

Each carries reliability tags on every figure and a Red Team about the disclosure gap. Worked examples now link to their segment survey.

## Honesty
All quantitative results are self-authored quasi-static models with **class-typical/invented device params** — status `unverified`. Directional findings are robust device physics; magnitudes are computed hypotheses. The truck's absolute life is coefficient-dominated (±1–2 orders, stated loudly); the microcar's device+cost are the point where RAG+web data ran out.

← [[changelog-index]] | [[power-electronics/traction-inverter/traction-inverter-index]]
