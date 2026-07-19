---
title: "Plan — Architecture (agents, orchestration, state)"
type: plan
field: project
created: 2026-07-17
updated: 2026-07-19
tags: [plan, ai-agents, multi-agent, plecs, architecture]
---

# Architecture — agents, orchestration, shared state

> Topic of [[plan-ai-agent-mas]]. Defines the 3-agent core, how they are orchestrated, the shared services they call, and — critically — the **typed shared state** they read and write (gap G-C).

## 1. Agents (the 3-agent core)

| Agent | Stage | Model | Does | Does NOT |
|---|---|---|---|---|
| **Orchestrator** | drives the loop | cheap (deepseek) | parse prompt (new vs iterate), route stages, apply stopping rule, decide iterate/stop | design |
| **Planner** | PLAN = design-loop ① | strong (claude) + RAG | pick topology + control scheme + targets, **grounded in retrieved papers**; emit a design plan for optional HITL approval | run sims |
| **Designer** | DESIGN = ②+③ | mixed | refine structure (pick PLECS template, fix discrete choices) and **drive the parameter optimizer** over PLECS | judge pass/fail |
| **Validator** | VALIDATE | cheap tools + strong review | run PLECS corners, summarize, check guardrails + evidence gates, **k=3 reviewer consensus** (DRCY), route the fail edge | choose topology |

Start with **exactly these three** (+ Orchestrator). Split out a **Thermal** or **Component** specialist **only when the Validator shows it is the recurring failing gate** — AgentSlimming: automated MAS bloat wastes tokens quadratically ([[agent-frameworks-2026-currency]]). The Orchestrator is scaffolding, not a design agent; the "3-agent" count is Planner/Designer/Validator.

The **design-loop three stages are internal structure, not agents** — see [[plan-design-loop]]. This keeps the roster minimal while honoring the field-standard decomposition.

## 2. Orchestration

**LangGraph 1.0 StateGraph** (checkpointing, resume-on-failure, per-node timeouts, HITL interrupt at PLAN approval) over SQLite. CrewAI-style roles are a **naming pattern only**, not the runtime (CrewAI has no checkpointing — [[agent-frameworks-2026-currency]]). Weigh Microsoft Agent Framework only for its native MCP (the PLECS backend is an MCP server); default is LangGraph.

- **Nodes:** `spec_parse` → `plan` → `design` → `validate` → `report`, plus `human_approval` (interrupt) and `iterate` (conditional router).
- **Checkpoint at every transition.** ~ms overhead; lets a crashed PLECS batch resume mid-sweep.
- **The `iterate` router is failure-mode-aware** (not a generic "replan"): params → re-optimize (③), structure → refine (②), architecture → re-plan (①). See [[plan-design-loop]] §routing.
- **Watchdog + idempotency** kept light — LangGraph 1.0 does more of this now; idempotency key = hash(ModelVars) so identical sims never re-run.

## 3. Shared services

- **RAG service** — knowledge backbone. [[plan-knowledge-rag]]
- **PLECS service** — templates, optimizer, corner sweeps, native AC/steady-state, 5-layer summarizer. [[plan-plecs-harness]]
- **Memory** — episodic (design records) + procedural (iteration playbooks) + semantic (vector store shared with RAG). [[plan-memory]]

## 4. Shared state schema (gap G-C) — `InverterDesignState`

A LangGraph MAS *is* its state. Adopt PE-MAS's typed-state discipline (~30 fields) re-targeted to traction. Sketch (Python `TypedDict`, illustrative — not final):

```python
class InverterDesignState(TypedDict):
    # --- request ---
    prompt: str
    mode: Literal["design_new", "iterate_existing"]
    spec: DesignSpec              # Vdc, P_out, motor(PMSM/IM) params, cooling, drive-cycle, constraints
    supplied_design: Optional[Design]   # for iterate_existing

    # --- plan (① Planner, RAG-grounded) ---
    topology: TopologyChoice      # 2L-B6 | 3L-NPC | 3L-TNPC | ANPC  (+ ranked alternatives)
    control_scheme: ControlChoice # FOC/DTC/MPC + modulation (SVPWM/DPWM/…)
    targets: Targets             # eta_target, THD_max, Tj_margin, cost_ceiling
    plan_citations: List[Citation]      # every choice cites a retrievable source

    # --- design (② refine / ③ optimize, Designer) ---
    template_id: str             # which validated PLECS template
    fixed_choices: dict          # module, gate-driver, DC-link cap class …
    free_params: ParamSpace      # bounds for fsw, deadtime, Rg, C_dc, MI, loop gains
    optimizer: OptimizerConfig    # DE|PSO|BO|grid, budget, objective weights
    best_candidate: Design        # best-so-far across iterations (PE-MAS pattern)

    # --- validate (Validator) ---
    corner_results: List[PlecsSummary]  # ~36 numbers per corner, never raw waveforms
    gate_results: GateReport      # per-gate pass/fail + margins
    consensus: ConsensusResult    # k=3 reviewer reconciliation + confidence

    # --- provenance / control ---
    reasoning_trace: List[TraceItem]    # step, agent, evidence, conclusion, confidence
    iteration: int
    stop_reason: Optional[str]           # converged | max_iter | infeasible | human_stop
    evidence_grade: str
```

**Rules:** every design-affecting field that came from an LLM carries a citation or a PLECS provenance tag; `corner_results` holds summaries only (invariant #3); `reasoning_trace` is **compacted** each iteration ([[plan-memory]]). This schema is the contract the topic plans below fill in.

## 5. Output artifact (the REPORT node)

REPORT emits an **engineering review package**, not a single answer — the design plus the evidence that closes each gate:
- **Spec + design:** topology, control scheme, PLECS template id, final parameters, BOM class.
- **Evidence table:** per-gate pass/fail + margin, each corner's ~36-number summary, the validated-model registry reference.
- **Citations:** every topology/control/component decision → its retrievable source (the citation-gate output).
- **Provenance:** `reasoning_trace` (compacted), iteration count, `stop_reason`, best-candidate history, evidence grade, k=3 consensus + confidence.
- **Reproducibility:** the `ModelVars` / optimizer config needed to re-run (idempotency key).

Released only when every gate closes against a **validated** model; otherwise presented as an in-progress package with open gates named. Consumed by the HITL signoff and the benchmark scorer ([[plan-evaluation-and-benchmark]]).

← [[plan-ai-agent-mas]] | [[plan-design-loop]] | [[pe-mas-flyback-mas]]
