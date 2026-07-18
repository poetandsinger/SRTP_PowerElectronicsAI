---
title: "Observed Design Workflow — What One Full Design Pass Teaches the MAS"
type: topic
field: ai-agents
created: 2026-07-18
updated: 2026-07-18
status: unverified
evidence: single-study
sources: [sources/ai-agents/pe-mas-flyback-mas, sources/ai-agents/plecs-ai-agent-integration-ordonez, sources/ai-agents/phia-lpcomda-2026-physics-informed-pe-agent]
tags: [ai-agents, multi-agent, architecture, design-automation, engineering-ai, synthesis, review]
review_by: 2026-10-17
---

# Observed Design Workflow — What One Full Design Pass Teaches the MAS

On 2026-07-18 a single agent ran a **complete** traction-inverter design by hand (vehicle → spec → circuit → device → thermal → DC-link → control → BOM → model-run → report), RAG-limited to the traction-inverter vault + undergrad physics. This note extracts the **process** — the workflow, the lookups, the gates, the de-scope points — and maps each to a MAS requirement, so [[project/plans/ai-agent-mas-plan]] can build what worked. Companion to [[ai-agents/design-loop-architecture]] (loop derived from *published* systems); this derives it from **one observed run**. Engineering output: [[power-electronics/traction-inverter/worked-example-family-car-400v-sic]], [[power-electronics/traction-inverter/findings-family-car-design-by-doing]].

**Up front: n = 1**, one agent, reconstructed partly post-hoc — a hypothesis-rich field note, not a validated methodology (Red Team).

## The Observed Pipeline (mapped to plan roles)

```mermaid
flowchart LR
  V(["vehicle brief"]) --> Z["⓪ REQUIREMENTS<br/>road-load → P,T,Is,max,speeds,bus<br/>(tool + undergrad RAG)"]
  Z --> A["① TOPOLOGY<br/>2L-B6, RAG-grounded"]
  A --> B["② DEVICE + SUBSYSTEMS<br/>parts RETRIEVED by (fn,V,I,qual)<br/>thermal/DC-link/gate/control"]
  B --> C["③ COMPUTE / OPTIMIZE<br/>runnable model, iterate"]
  C --> E{"EVALUATE<br/>corpus-consistency + gates"}
  E -->|fail| B
  E -->|pass| R["④ REPORT<br/>doc rendered from the numbers,<br/>every value provenance-tagged"]
```

Roles today: **Planner**=①, **Designer**=②③, **Validator**=evaluate ([[ai-agents/design-loop-architecture]] §4). The pass shows the loop needs **two cheap bookends** — ⓪ and ④ — neither a new *core* agent (AgentSlimming holds).

## The Gold Nuggets (particular → MAS requirement)

| # | What the pass actually did | MAS requirement | Plan status |
|---|----------------------------|-----------------|-------------|
| 1 | **Derived** the spec from the vehicle (road-load eqn → 135 kW/345 Nm, `Is,max`≈400 A, speeds, 400 V class) — did not accept it as given | **Stage ⓪ Requirements** upstream of Planner: a `vehicle-brief → spec-vector` road-load tool | **NEW** (propose G-I). Loop starts at "spec"; hand-fed `Is,max` is an error source (prior worked examples *guessed* it) |
| 2 | **Retrieved** parts, never generated them: keyed `(function, V-class, I-class, auto-qual)` → nearest vetted part in [[power-electronics/traction-inverter/components]]/[[power-electronics/traction-inverter/bom]] → `{spec, sizing-driver, cite}`; mapped 1200 V→750 V *within the same family* (HybridPACK Drive). Zero web calls, zero hallucinated MPNs | **Parts-retriever tool** for the Designer over the component KB + DigiKey/Nexar live adapters; the LLM sets *constraints*, the tool returns the *part* | **NEW** (G-J). Only implicit via BOM adapters. LLMs hallucinate MPNs if asked to *generate* |
| 3 | **Computed before writing**; ran the model, iterated, *then* wrote the note from its output | **Reporter (④) consumes only the summarizer's numbers + a run-id**; forbid the LLM narrating plausible numbers | Reinforces invariant #3 + G-E; adds explicit downstream doc-gen step |
| 4 | **Provenance-tagged every number** (`[model]/[derived]/[T]/[NN]`) | Make provenance a **typed field on every emitted quantity**; the evidence gate **refuses to close on `[T]`/assumed** values | **NEW** (G-K). Runtime enforcement of the vault status/evidence schema |
| 5 | **Sensitivity steered effort** — the headline SiC-vs-IGBT result hinged on one input (the `Esw` ratio); flagged it | Cheap **sensitivity step** (perturb each input, watch the summary) → tells the loop *which input to spend a datasheet/web call on* vs accept a class-typical | **NEW** (G-L). Feeds data-acquisition priority + the optimizer |
| 6 | **Cheap corpus-consistency check** before any sim: computed η / loss-split vs the KB's stated ranges & directions ([28], worked-example-400v) | **RAG-consistency pre-gate** before the Validator spends a PLECS batch — near-free, catches gross errors | **NEW** (G-M). Complements the evidence gate |
| 7 | **Cost-aware de-scope**: probed PLECS incrementally (launch→methods→readback→demos); when full retarget hit diminishing returns/risk, fell back to a bounded, honest outcome | The **G-H stopping rule must cover exploration/tool-probing**, not just the optimizer: bound probe depth, return best defensible partial | Extends G-H; SimulCost/AgentSlimming [73][74] |
| 8 | **Iterated the artifact, not the prose** — compute→inspect→adjust→recompute (fixed a highway-heavy drive cycle) | Evaluator-optimizer loop runs on the **executable**; write once at the end | Confirms ③+evaluate |

## Two Bookends the 3-Agent Core Is Missing

Cheap, Orchestrator-owned steps — not new agents:
- **⓪ Requirements** (`vehicle → spec vector`): a road-load tool + undergrad-vehicle RAG. Without it, `Is,max` is a human guess and the whole sizing rests on it.
- **④ Reporter** (`summary → worked-example doc`, every number provenance-tagged): renders the human-facing artifact *from* the validated numbers, downstream of the Validator.

## Confirmed (not new)
- **Template + param-injection, not free-form authoring** — retargeted a *named* PLECS demo by `Value`/`plecs.set` (plan §2 ✓, [[project/plans/plecs-harness]]).
- **Explicit compute over LLM re-guessing** — the model, not prose, produced the numbers (design-loop ③ ✓).
- **RAG-first grounding** — read the method files (design-procedure, machine-and-load, control-how-to, bom) *before* designing; the design instantiates the vault's method, it does not reinvent it.
- **3-agent core sufficient** — the bookends are Orchestrator-owned steps, not agents.

## Red Team

**Steelman against:** n = 1, one agent, one domain, reconstructed post-hoc — this risks dressing up a single improvised session as "methodology" and minting gap IDs (G-I…G-M) the plan may not need. Several nuggets (compute-before-write, provenance) are good-practice restatements already implicit in the plan's invariants. And #2 (parts = retrieval) is **only true inside the KB's coverage** — for a genuinely novel spec the retriever returns nothing and live-search/generation is unavoidable.

**How it could be false:**
1. **ⓠ Requirements may belong *inside* the Planner**, not as a separate stage — an org choice, not a finding.
2. **The consistency pre-gate can reject correct *novel* results** that legitimately depart from the corpus — a real false-negative risk; it must gate "gross-error" bands, not tight agreement.
3. **The sensitivity step can cost more than its value** on a ≤3-parameter design.
4. **n = 1 can't separate workflow-general from task-specific** — the stage boundaries may be an artifact of this one problem.

**What would change my mind:** 2–3 more full passes (different vehicle/topology) reproducing the same stage boundaries and failure points; a Planner that derives requirements inline making ⓠ redundant; a logged case where the consistency pre-gate blocks a true result.

**Residual doubt:** The two bookends (ⓠ requirements, ④ reporter) and **parts = retrieval-not-generation** are the robust, actionable finds. Provenance-typing and cost-aware de-scope are sound but already near the plan. The new gap IDs are proposals to test, not settled — validate against a second design pass before wiring them in.

---

> **References:** [[citations]]

← [[ai-agents/design-loop-architecture]] | [[project/plans/ai-agent-mas-plan]] | [[power-electronics/traction-inverter/findings-family-car-design-by-doing]] | [[ai-agents/harness/harness-index]]
