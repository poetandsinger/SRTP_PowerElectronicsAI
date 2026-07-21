# TODO — active tasks

> Flat, ruthless. Strategic context is in [ROADMAP.md](ROADMAP.md); research open questions are **not** here (they live in the synthesis notes). Done items move to [LOG.md](LOG.md).

## Now — close Phase 1 (first validated 2L-B6 number)  ✅ DONE 2026-07-21 (on `experiments/2l-b6-800v-sic-bench/`, not rainflow)
- [x] 800 V loaded operating point (800 V/359 A rms/302 kW) — on the purpose-fit bench
- [x] Corner matrix S1/S2/S3/S4/S5 — 6 corners run (η 99.03–99.32 %); **deferred:** corners 6–9 (field-weakening/ASC/SC/drive-cycle) + S6/S7 need control/fault/averaged models
- [x] **Calibrate to the Wolfspeed/TI 300 kW CRD** (S5) — CRD point = 99.07 % η + 175 °C (within tol)
- [x] Switching-energy readout — solved via `PeriodicImpulseAverage` (not `SwitchLossCalculator`)
- [x] Cross-check vs numpy models — analytic conduction −3.5 %; numpy device params are invented/unverified
- [x] `system/configs/model_registry.json` 2L-B6 → `validation_status: validated`

## Track 1 — 2L-B6 SiC (finish the design note)
- [ ] Fill `design-2l-b6-800v-sic` with the validated numbers (results/metrics/2l-b6-800v-sic-bench.txt); replace `[T]`/`[derived]`
- [ ] Fold 2L-B6 numbers back into `circuit-topologies` row + agnostic notes (thermal, gate-driver, control, protection, EMI, BOM)
- [ ] Re-run Red Team → residual doubt; bump `status`/`evidence`
- [ ] (optional) Corners 6–9 + S6/S7 once control/fault/averaged models exist

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
- [x] Repo reorg to `knowledge/ system/ experiments/ results/` (2026-07-20)
- [ ] Rebuild the graphify knowledge graph against the new paths (current graph indexes pre-move paths)
- [ ] Point Obsidian at `knowledge/` as the vault root; the `.base` indexes in `knowledge/_archive/` are retired (query the old folder layout)
