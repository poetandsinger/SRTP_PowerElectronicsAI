---
title: "3L-TNPC · 12-switch · 800 V SiC Traction Inverter — Design & PLECS Validation"
type: topic
field: power-electronics
created: 2026-07-19
updated: 2026-07-19
status: unverified
evidence: theoretical
sources: [sources/power-electronics/sachs-neuburger-2025-3l-tnpc]
tags: [power-electronics, traction-inverter, design, three-level, t-type, sic, efficiency, thd]
review_by: 2026-10-17
---

## What This Note Is

**Track 2 topology unit** (`design-<topology>-<voltage>-<device>`): an 800 V-class **SiC 3-level T-type NPC** traction inverter, sized to the same 150 kW anchor as [[design-2l-b6-800v-sic]] for a like-for-like comparison. **Planned, not yet built** — this note is the home for TNPC's validated numbers; it is populated when Track 2 of [[plan-depth-research]] runs, after Track 1 (2L-B6) is validated and registered. Topology catalogue: [[circuit-topologies]] §4.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; **[derived]** → computed in [[procedure-design]]; **[TBD-PLECS]** → to be produced by the Track-2 model.

## Why This Topology (industry relevance)

The **leading multilevel candidate for automotive 800 V**: [28] reports **−0.67 kWh/100 km** drive-cycle loss reduction versus a SiC 2L-B6 baseline for **+30 % SiC chip area** — the best cost/benefit of the three-level options. Only 12 switches (vs 18 for ANPC). Growing share projected for 2030 BEVs; no production vehicle yet.

## Topology Structure

- **12 switches** (4 main S1–S4 + a bidirectional NP switch S5/S6 in anti-series per leg, ×3). Three levels: +Vdc/2, 0, −Vdc/2.
- **Voltage stress asymmetry (the key design constraint):** the **outer switches S1/S4 block the full Vdc** — unlike NPC/ANPC where series devices share it. On an 800 V bus this forces **1200 V SiC** on the outer positions; the NP branch sees Vdc/2. Structure + switching states (P/O/N) in [[circuit-topologies]] §4.
- vs 2L-B6: doubled apparent switching frequency at the output, ~½ dv/dt, lower motor-harmonic loss.

## Target Specification (same anchor as 2L-B6)

| Item | Value | Basis |
|------|-------|-------|
| Topology | 3L-TNPC (12-switch) | [[circuit-topologies]] §4 |
| Device | 1200 V SiC outer, ~650–900 V NP switches | [T], voltage-stress asymmetry |
| DC-link | 750 V nom (550–850 V) | matches anchor |
| Peak / continuous power | 150 kW / 70 kW | matches anchor |
| Switching frequency | 16 kHz | comparison control |
| Efficiency / THD / Tj | **[TBD-PLECS]** | Track 2 |

## Planned PLECS Validation (Track 2)

1. Build as a `.plecs` **text** variant of the Track-1 template (swap the 6-switch leg for the 12-switch T-type leg; add NP-balancing modulation). Top-level Outports per [[procedure-simulation-and-validation]] §1.
2. Run the 9-corner matrix ([[procedure-simulation-and-validation]] §4) at 550/750/850 V.
3. **Calibrate against the validated 2L-B6 baseline + [28]:** target the ~0.67 kWh/100 km drive-cycle delta and lower partial-load loss; confirm NP balance holds.
4. Fold η/THD/dv/dt/NP-balance into [[circuit-topologies]] §5 and [[design-tradeoffs]]; register in `model_registry.json`.

## Red Team

**Steelman against:** This note is a scaffold — it has a structure and a target, no validated numbers. The whole automotive case for TNPC rests on **one preprint** [28]; authoring a design note before the model risks anchoring on that single source's assumptions (WLTP cycle, specific device models). "Best multilevel candidate" is a projection, not a shipped product.

**How it could be false:** the 0.67 kWh/100 km figure may not reproduce with different device/loss models or drive cycles; the full-Vdc outer-switch requirement erodes the device-cost advantage; NP-balancing complexity may cost more than the efficiency gain returns.

**What would change my mind:** a validated Track-2 PLECS model reproducing the partial-load advantage at the three corners; an independent (non-[28]) source; a production TNPC traction inverter.

**Residual doubt:** Correct as the planned home for TNPC evidence. Every performance number here is `[TBD-PLECS]` until Track 2 runs.

---

> **References:** [[citations]]

← [[circuit-topologies]] | [[design-2l-b6-800v-sic]] | [[plan-depth-research]] →
