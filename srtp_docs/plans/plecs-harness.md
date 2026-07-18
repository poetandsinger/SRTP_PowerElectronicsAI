---
title: "Plan — PLECS harness (service, models, summarizer)"
type: plan
field: project
created: 2026-07-17
updated: 2026-07-19
tags: [plan, ai-agents, plecs, simulation]
---

# PLECS harness

> Topic of [[ai-agent-mas-plan]]. PLECS is the sole simulator and source of evidence (invariants #2, #6). Fills gap G-E (summarizer is a promise, not a contract) and G-F (model workstream is a table, not a procedure). Research basis: [[plecs-integration]], [[plecs-xmlrpc-scripting-interface]], [[plecs-ai-agent-integration-ordonez]], PE-MAS `plecs-mcp`.

## 1. Service

- **Access path:** adapt PE-MAS's **`plecs-mcp`** (~29 FastMCP tools) + direct XML-RPC (`PE_MAS_PLECS_BACKEND=auto`). Reuse its **capability-discovery layer** (`list_methods` / `rpc_try_methods` / `call_first_available`) for robustness against PLECS-version drift. Installed build: **PLECS 4.8 Standalone**, HTTP server on port 1080.
- **License check — ✅ CONFIRMED 2026-07-18.** PLECS 4.8 Standalone here is licensed for headless/scripted use: `PLECS.exe -server 1080` starts the XML-RPC server and a full 2L-VSI+IPMSM+FOC drive loads and simulates to completion via RPC ([[worked-example-family-car-400v-sic]] §7, [[simulation-and-validation]] §1). The day-one blocker is cleared.
- **Verified RPC surface (4.8):** `plecs.load/set/get/simulate/getModelTree/scope/statistics/analyze/codegen/close`. **No `plecs.add`/`connect`/`eval`** — confirms §2 path 1 (template + param) is the *only* RPC path; structural variants must be `.plecs` **text** edits, not RPC. Keep PE-MAS's `call_first_available` probing for version drift.
- **Readback requirement (was implicit, now explicit):** `plecs.simulate` returns `Values` **only from top-level Outport blocks** — a scope-only model returns empty. **Every template must terminate each summarized signal (§4) in a top-level Outport**, or the summarizer gets nothing. This is the concrete blocker between "model runs" and "model yields evidence."
- **Agent-facing tools:** `plecs_simulate`, `plecs_sweep` (list-of-optStructs, parallel), `plecs_set_param`, `plecs_analyze` (native AC/steady-state), `summarize_result`. The optimizer ([[design-loop]] §2) calls `plecs_sweep` one generation at a time.
- **Concurrency:** the RPC server is blocking/single-request — use the list-of-optStructs batch path (PLECS fans across cores) or multiple PLECS instances on different ports. Never hand-roll N serial calls where a batch works.

## 2. Model handling — template + injection, not free-form authoring

Two paths, both proven in PE-MAS:
1. **Template + `ModelVars`/`plecs.set`** (default, low-risk): a validated base model per topology; the agent tunes parameters only. De-risks "LLMs can't write netlists" (G5).
2. **XML injection** (`PLECSGenerator`, ElementTree) for controlled structural variants — higher risk, keep for refinement (② ) not blind synthesis.

## 3. Model-validation procedure + registry (gap G-F) — the critical path

Per PE-MAS's `model_registry.json`, **validated per-topology models are the bottleneck, not the agent.** A model is only usable as evidence once it passes this procedure:

**Validation procedure (per topology + machine load):**
1. Build the PLECS template (power stage + gate model + thermal network + native PMSM/IM + FOC).
2. Run the **corner matrix** (low-line / nominal / high-line × load points).
3. Compare η, THD, losses, Tj against a **named reference** (a `reference-design-*` note or a cited paper), within a **stated tolerance** (e.g. η within ±1 pt, losses within ±10%).
4. Record the outcome in the registry with provenance.

**Registry schema (extend PE-MAS):**
```json
{ "topology": "2L-B6-SiC",
  "template": "templates/2l_b6_sic_pmsm.plecs",
  "status": "available | planned | not_in_release",
  "validation_status": "validated | unvalidated",
  "validated_against": "reference-design-2l-b6-sic-800v",
  "tolerance": {"eta_pts": 1.0, "loss_pct": 10},
  "corners_seen": ["low_line","nominal","high_line"],
  "rag_coverage_sources": 6 }
```

**Registry status = evidence status.** `validation_status: unvalidated` ⇒ the Validator may *run* the model but **may not close the PLECS evidence gate** with it. Topologies to bring up: **2L-B6-SiC** (first, the A/B anchor) → **3L-NPC / 3L-TNPC** (+thermal) → **ANPC** (+thermal +EMI). This is a workstream, not a schedule — no phases; the order is by dependency and difficulty.

## 4. The 5-layer summarizer contract (gap G-E)

Mirror Ordonez's 5 layers; the ~36 numbers must be **enumerated**, not gestured at. Illustrative summary schema per corner:

```
efficiency: eta, P_loss_total, P_cond, P_sw           (4)
thermal:    Tj_max_sw, Tj_max_diode, Tj_margin, Rth_used  (4)
quality:    THD_i, THD_v, ripple_i, ripple_vdc          (4)
stress:     Vds_peak, Vds_margin, Id_peak, dvdt          (4)
control:    MI, torque_ripple, current_error            (3)
per-corner: {low_line, nominal, high_line} × key metrics
convergence/health: solver_ok, no_nan, sim_time, timeout_hit (4)
```

- **Layers:** capture (XML-RPC runner) → summarize (streaming CSV → the numbers above) → **regression-check** vs the topology's validated baseline (tight per-signal tolerances) → **pass/fail exit code** → agent sees only the summary + gate result.
- **The agent never sees raw `Values` arrays** (invariant #3; Ordonez ~1000× / ~$20/hr).
- **Idempotency:** cache by `hash(ModelVars)` so identical sims never re-run.

← [[ai-agent-mas-plan]] | [[design-loop]] | [[guardrails-and-evidence]] | [[plecs-integration]]
