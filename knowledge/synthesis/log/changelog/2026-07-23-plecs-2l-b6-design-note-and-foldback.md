---
title: "2L-B6 Track-1 closed — design note filled, folded back into the method notes, status → supported"
type: changelog
field: project
created: 2026-07-23
updated: 2026-07-23
tags: [changelog, plecs, simulation, engineering-ai, validation, design, thermal, protection, foc]
---

# 2026-07-23 (cont.) — Track-1 Design note → Fold back → Close

Continues [[2026-07-23-plecs-2l-b6-corners-6-9]] (which finished the 9-corner matrix). This entry does the
remaining three Track-1 stages of [[plan-depth-research]] — **Design note → Fold back → Close** — turning the
validated corner results into the topology unit's evidence and propagating them through the agnostic method
notes. No new PLECS runs; this is the write-up/synthesis pass.

---

## 1. Design note filled ([[design-2l-b6-800v-sic]])

Rewrote the note from a `status: unverified` scaffold (superseded rainflow-base PLECS section, `[derived]`
numbers) into a **`status: supported`** validated topology unit:

- **Operating-points table** now pairs each closed-form `[derived]` figure with the PLECS `[sim]` value at the
  matching corner. The validation **confirms the first-pass algebra**: design "≈99.3% / ≈1.0 kW / ≈112 °C @
  150 kW peak" ↔ **C5 sim 99.32% / 1.02 kW / 105 °C**; 300 A launch ↔ C4 (99.16%, 148 °C); CRD anchor ↔ C1
  (99.07%, 175 °C).
- **150 kW-spec vs 300 kW-CRD reconciled explicitly:** the design's own envelope is C4/C5; validation was also
  carried to the Wolfspeed/TI 300 kW CRD (the *measured*, non-circular S5 anchor). All three sit inside one
  validated corner envelope — the CAB450 is 300 kW-capable and this 150 kW design runs well inside it.
- **PLECS section** replaced with the full S1–S7 + 9-corner result (switched C1–C6 table + machine/fault/averaged
  C6–C9 summaries).
- **Frontmatter:** `status: unverified → supported`, `evidence: theoretical → single-study` (one measured anchor).
- **Red Team** rewritten: the old blocker ("no CRD-calibrated model") is resolved; new residual doubts are the
  **sim→hardware gap** (no calorimetric bench), the **single vendor-affiliated anchor** (CRD + datasheet both
  Wolfspeed), **`[T]` machine params**, and **C6/C8 being analytic** not closed-loop PLECS.

## 2. Folded back into the agnostic method notes (scoped per the can/cannot table)

| Note | What was folded in |
|------|--------------------|
| [[circuit-topologies]] | §1 gains a **PLECS-validated 2L-B6 baseline** table (99.07% CRD / 99.32% part-load, loss split, THD 0.15%, C6/C9); §5 comparison row annotated; Red Team's stale "97.5% 2L peak" corrected — 3L gains must re-base on a **~99%** 2L baseline. |
| [[procedure-simulation-and-validation]] | §4 corner matrix marked **executed for Track-1** (all 9 corners + S1–S7). |
| [[thermal-design]] | §7 worked Rth-chain: the soft `[T]` `R_cs` placeholder **pinned by the CRD calibration** (R_cs=0.070 back-calculated from the measured 175 °C); loss→Tj chain confirmed. |
| [[protection-and-safety]] | §3 CAB450 **SC budget** (ID,sat~4.7 kA, SCWT~2.73 µs, survives with soft-off); §5 **ASC** (Ich=611 A, entry 3.1×, no bus overvolt). |
| [[control-schemes]] | §2.4 **field-weakening envelope** (CPSR 2.4×, torque∝ω⁻⁰·⁹¹, 100% voltage util; inverter η flat to 3× speed). |
| [[reliability-and-lifetime]] | §4 **mission-profile front-end built** (drive cycle → Foster Tj(t) → rainflow bins; Tj peak 116 °C, ΔTj≤28 °C) — absolute Nf/Miner still needs module-specific coefficients. |
| [[bom-2l-b6-sic]] | main-switch choice **confirmed** (6× CAB450, validated loss/thermal). |

Each fold-in is a scoped `[sim]`/`[analytic]` callout, not a rewrite — it labels what PLECS confirms vs what
stays analytic/datasheet, per the [[plan-depth-research]] can/cannot discipline.

## 3. Close

- `status`/`evidence` bumped on the design note (§1); Red Team → residual doubt refreshed.
- `system/configs/model_registry.json` 2L-B6 entry already `validation_status: validated` with the
  `corners_6_9` block (from the previous entry) — confirmed consistent.
- The honest boundary held throughout: **`supported` = the *inverter slice*** (efficiency/thermal, CRD-calibrated
  sim). The machine-side (C6/C8 on `[T]` params) and the sim→hardware gap remain the residual, flagged in every
  fold-in and the Red Team.

## 4. What's next (Track-1 done)

Track-1 (2L-B6) is complete through Close. Remaining program: **Track 2 (3L-TNPC)** — reuse the bench/instrument/
analytic-template method (changelog [[2026-07-21-plecs-2l-b6-model-complete-and-corners]] §8 carry-forward), and
eventually the cross-topology synthesis ([[circuit-topologies]] §5 + design-tradeoffs) once all four tracks land.
A closed-loop **PMSM+FOC** model would retro-upgrade C6/C8 from analytic to PLECS-confirmed.

## 5. Files
- [[design-2l-b6-800v-sic]] (filled + status→supported)
- Folded: [[circuit-topologies]], [[procedure-simulation-and-validation]], [[thermal-design]],
  [[protection-and-safety]], [[control-schemes]], [[reliability-and-lifetime]], [[bom-2l-b6-sic]]
- root `README.md`, `LOG.md`, changelog-index, memory `plecs-2l-b6-800v-bench`

> **Graph note:** many notes edited + new changelog — run **`/graphify . --update`** to re-index.
