# TODO — active tasks

> Flat, ruthless. Strategic context is in [ROADMAP.md](ROADMAP.md); research open questions are **not** here (they live in the synthesis notes). Done items move to [LOG.md](LOG.md).

## Now — close Phase 1 (first validated 2L-B6 number)
- [ ] Set a real **800 V loaded operating point** on `experiments/2l-b6-rainflow/2l_b6_cab450_rainflow.plecs`
- [ ] Run the **9-corner matrix** (`procedure-simulation-and-validation` §4: double-pulse, η×3, thermal, ripple, overmod, field-weakening, SC, ASC, drive-cycle)
- [ ] **Calibrate to the Wolfspeed/TI 300 kW CRD** (SOP gate S5) — >98 % η, 32 kW/L, 360 A rms, 175 °C anchor
- [ ] Crack the **switching-energy readout**: `SwitchLossCalculator` with empty `Signals{}` sums to 0 in scripted mode — likely needs GUI signal selection (open sub-item)
- [ ] Cross-check every PLECS number against the `prototypes/inverter/*/` numpy models

## Track 1 — 2L-B6 SiC (finish + register)
- [ ] Fill `design-2l-b6-800v-sic` with validated numbers; replace all `[T]`/`[derived]`
- [ ] Fold 2L-B6 numbers back into `circuit-topologies` row + agnostic notes (thermal, gate-driver, control, protection, EMI, BOM)
- [ ] Re-run Red Team → residual doubt; bump `status`/`evidence`
- [ ] Set `system/configs/model_registry.json` 2L-B6 entry → `validation_status: validated`

## Shared agnostic layer (validate the sim-adjacent notes during T1)
- [ ] `machine-and-load` — real IPMSM datasheet params or saturation LUT
- [ ] `circuit-components` — SiC loss delta + DC-link ripple ("verify with simulation")
- [ ] `reliability-and-lifetime` — fatigue models (loss→Tj(t) front-end shared with thermal)

## Tracks 2–4 (serial — one at a time, only after the prior is registered)
- [ ] T2 **3L-TNPC**: model → corners → `design-3l-tnpc-800v-sic` → register
- [ ] T3 **3L-ANPC**: model (+ RLC/damped-LC output-filter derivation, `ref_notes.txt` §9) → corners → `design-3l-anpc-800v-sic` → register
- [ ] T4 **3L-NPC**: model → corners → `design-3l-npc-800v-sic` → register
- [ ] Synthesis: fill `circuit-topologies` §5 + `design-tradeoffs` (PLECS Pareto sweep); regenerate the reference-design indexes

## Phase 3 — MAS implementation (after evidence layer is proven)
- [ ] Scaffold LangGraph 3-agent core (Orchestrator + Planner + Designer + Validator) on `InverterDesignState`
- [ ] Wire the explicit numerical optimizer (DE/PSO/BO) over the PLECS harness
- [ ] RAG grounding over the knowledge notes + evidence gates
- [ ] Single-agent vs 3-agent A/B benchmark harness

## Housekeeping
- [x] Repo reorg to `knowledge/ prototypes/ system/ experiments/ results/` (2026-07-20)
- [ ] Rebuild the graphify knowledge graph against the new paths (current graph indexes pre-move paths)
- [ ] Point Obsidian at `knowledge/` as the vault root; the `.base` indexes in `knowledge/_archive/` are retired (query the old folder layout)
