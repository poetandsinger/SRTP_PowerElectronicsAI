---
title: "3L-ANPC · 18-switch · 800 V SiC Traction Inverter — Design & PLECS Validation"
type: topic
field: power-electronics
created: 2026-07-19
updated: 2026-07-19
status: unverified
evidence: theoretical
sources: [sources/power-electronics/cacciato-etal-2022-gan-anpc, sources/power-electronics/sachs-neuburger-2025-3l-tnpc]
tags: [power-electronics, traction-inverter, design, three-level, anpc, sic, efficiency, thd]
review_by: 2026-10-17
---

## What This Note Is

**Track 3 topology unit** (`design-<topology>-<voltage>-<device>`): an 800 V-class **SiC 3-level Active NPC** traction inverter, sized to the same 150 kW anchor as [[design-2l-b6-800v-sic]]. **Planned, not yet built** — populated when Track 3 of [[plan-depth-research]] runs. This is the topology of the **reference study** (`scratchpad/ref_notes.txt`), so Track 3 reproduces that design directly — including its RLC/damped-LC output filter. Topology catalogue: [[circuit-topologies]] §3.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training; **[derived]** → in [[procedure-design]]; **[TBD-PLECS]** → produced by the Track-3 model.

## Why This Topology (industry relevance)

**Research stage**, not in automotive production — the 18-switch count makes BOM and gate-drive cost prohibitive at current SiC pricing. Its distinctive value is **loss distribution**: redundant zero-states equalise thermal loading across all main switches, most useful where conduction loss dominates (partial load, GaN-ANPC research [44]). Included because it is the reference-PDF topology and the richest depth exemplar (18 gate equations, filter derivation, NP balancing).

## Topology Structure

- **18 switches** (6 per leg, ×3): outer S1/S4, inner S2/S3, clamp S5/S6. Three levels: +Vdc/2, 0, −Vdc/2.
- **Redundant zero-states (the point):** O+ (S2+S5) and O− (S3+S6) both give 0 V but route current through different devices — alternating them each cycle **balances losses and junction temperatures** across the four main switches and helps NP balance. States table in [[circuit-topologies]] §3; the reference PDF gives all 18 floating-gate equations (`ref_notes.txt` §4, §6).
- **Output filter (reference-PDF specific):** a series inductor + shunt series-R–C damping branch (damped LC), e.g. LF 1 mH series + RDA 3 Ω / CFA 6.8 µF to MID, f0 ≈ 1.93 kHz (`ref_notes.txt` §9) — Track 3 derives and sweeps this.

## Target Specification (same anchor as 2L-B6)

| Item | Value | Basis |
|------|-------|-------|
| Topology | 3L-ANPC (18-switch) | [[circuit-topologies]] §3 |
| Device | Vdc/2-rated main + clamp SiC (typ. 1200 V used at 800 V) | [T] |
| DC-link | 750 V nom (550–850 V), split-link + NP | matches anchor + reference PDF §3 |
| Peak / continuous power | 150 kW / 70 kW | matches anchor |
| Switching frequency | 16 kHz (reference PDF uses 20 kHz) | comparison control |
| Efficiency / THD / Tj / NP-balance | **[TBD-PLECS]** | Track 3 |

## Planned PLECS Validation (Track 3)

1. Build as a `.plecs` **text** variant of the Track-1 template (18-switch stage, redundant-zero-state modulation, split DC-link with NP, damped-LC output filter). Top-level Outports.
2. Run the 9-corner matrix + the reference PDF's filter/efficiency sweeps (L_FILTER, C_FILTER, R_FILTER, fsw, Tdead).
3. **Calibrate against the reference study + the 2L-B6 baseline:** reproduce three-level pole voltage, NP balance, loss-equalisation across main switches, and the filter's f0/attenuation trade-off.
4. Fold results into [[circuit-topologies]] §5, [[design-emi-emc]] (the filter), and [[design-tradeoffs]]; register in `model_registry.json`.

## Red Team

**Steelman against:** A scaffold with no validated numbers. ANPC is not automotive-production; spending the deepest treatment on it (because a reference PDF exists) risks over-investing in a topology the market has not adopted. The reference model itself is a topology-verification model with a generic switch — its own notes say efficiency is not production-accurate without real device loss surfaces.

**How it could be false:** the loss-balancing benefit may not justify 18 switches at any realistic SiC price; the reference filter values shift the 100 Hz operating point (the PDF shows ~86.7 kW vs 121 kW target) and need retuning; NP balancing without closed-loop control drifts.

**What would change my mind:** a validated Track-3 PLECS model reproducing the reference design's switching/filter behaviour at the three corners; evidence of an automotive ANPC design intent.

**Residual doubt:** Correct as the planned home for ANPC evidence and the direct analogue of the reference study. All numbers `[TBD-PLECS]` until Track 3.

---

> **References:** [[citations]]

← [[circuit-topologies]] | [[design-2l-b6-800v-sic]] | [[plan-depth-research]] →
