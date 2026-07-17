---
title: AI-Agent MAS Plan — PLECS-Backed Traction Inverter Design
type: plan
field: project
created: 2026-07-17
updated: 2026-07-17
tags: [plan, ai-agents, multi-agent, plecs]
---

# AI-Agent MAS Plan — PLECS-Backed Traction Inverter Design

> **The single AI-agent plan.** Supersedes and replaces the retired phase-plan set (`phase-0..4`, `multi-agent-architecture`, `plans-index`) — deleted 2026-07-17. Grounded in the 2026-07-17 research pass ([[audits/ai-agent-docs-audit-2026-07-17]]).
> **Prior art:** [[sources/ai-agents/pe-mas-flyback-mas]] (adopt its structure). **Backend:** PLECS only. **Knowledge:** RAG over a local research-paper corpus. **No surrogates / no PINN** — PLECS is the sole simulator and source of truth.

---

## 0. What the system does

**One user prompt → a validated traction-inverter design.** The prompt either (a) **designs new** from a spec, or (b) **iterates an existing design/plan** the user supplies. The system then runs a fixed pipeline:

```
                          ┌─────────────── RAG (local paper corpus, online optional) ───────────────┐
                          │                          (heavy retrieval)                              │
   USER PROMPT            ▼                                                                          │
 (new spec OR      ┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐          │
  existing design ─►│  PLAN      │────►│  DESIGN    │────►│  VALIDATE  │────►│  REPORT    │──► result │
  to iterate)      │ (grounded) │     │ (parametrize)    │  (PLECS)   │     │            │          │
                   └────────────┘     └────────────┘     └─────┬──────┘     └────────────┘          │
                          ▲                                    │ fail gate                          │
                          └──────────────── iterate ───────────┘                                    │
                                     (re-plan / re-design)                                          │
```

The value the MAS adds is the reasoning a coding-agent cannot do on its own — **topology choice, control-strategy selection, physics interpretation, literature grounding** ([[sources/ai-agents/plecs-ai-agent-integration-ordonez]]). Everything mechanical (parameter sweeps, simulation, regression) is cheap tool work over PLECS.

**Three invariants (non-negotiable):**
1. **Ground every design decision in retrieved papers** — no un-cited topology/control choices. RAG is the knowledge backbone, not a bolt-on.
2. **PLECS is the only simulator.** No PINN, no learned surrogates. If a number isn't from PLECS (or a cited paper), it isn't evidence.
3. **Summarize before the LLM** — engineered ~36-number summaries, never raw waveforms (~1000× token delta).

---

## 1. Prior-art anchor: PE-MAS

We adopt PE-MAS's proven structure ([[sources/ai-agents/pe-mas-flyback-mas]]) and re-target it from flyback to traction inverter:

| Adopt from PE-MAS | How SRTP uses it |
|-------------------|------------------|
| `requirements → designer → validator → reporter` node flow | Becomes **Plan → Design → Validate → Report** |
| `plecs-mcp` + direct XML-RPC (`PE_MAS_PLECS_BACKEND=auto`) | Reuse/adapt as the PLECS harness ([[ai-agents/harness/plecs-integration]]) |
| Template + `ModelVars` / XML-injection model handling | Per-topology validated templates for traction inverters |
| `model_registry.json` (honest per-topology status) | Same registry, populated with traction topologies |
| Knowledge/formula guardrails + corner-based evidence gates | Same, re-tuned to traction guardrails |
| Lifelong memory (design records, iteration playbooks) | Same, kept simple |
| **Dual-path RAG** (keyword + vector over a doc corpus) | **Elevated to first-class** — large local paper corpus |

**Change from PE-MAS:** flyback → traction (2L-B6, 3L-NPC/TNPC, ANPC + PMSM/IM load); provider-agnostic LLMs; RAG made central; and we explicitly **do not** add PINN surrogates (PE-MAS doesn't either).

---

## 2. Architecture

### 2.1 Agents (mapped to the pipeline stages)

| Agent | Stage | Model | Does | Does NOT |
|-------|-------|-------|------|----------|
| **Orchestrator** | drives the loop | cheap | parse prompt (new vs iterate), route stages, decide iterate/stop | design |
| **Planner** | PLAN | strong + RAG | pick topology + control scheme + targets, **grounded in retrieved papers**; emit a design plan for optional HITL approval | run sims |
| **Designer** | DESIGN | mixed | turn the plan into a concrete parametrization (PLECS template + `ModelVars`, component values from datasheets) | judge pass/fail |
| **Validator** | VALIDATE | cheap tools + strong review | run PLECS across corners, summarize, check guardrails + evidence gates, **k=3 reviewer consensus** (DRCY) | choose topology |

Start with exactly these. Split out a **Thermal** or **Component** specialist only when a *measured* failure mode demands it (AgentSlimming: MAS bloat wastes tokens quadratically — [[sources/ai-agents/agent-frameworks-2026-currency]]).

### 2.2 Shared services

- **RAG service (knowledge backbone)** — see §3.
- **PLECS service** — `plecs-mcp` / XML-RPC; template + `ModelVars`; corner sweeps; native AC/steady-state analysis; result summarizer ([[ai-agents/harness/plecs-integration]]).
- **Memory** — SQLite (design records, iteration playbooks, spec→result) + LanceDB (vector store shared with RAG). Kept simple; no self-evolving memory until it earns its place.

### 2.3 Orchestration

**LangGraph 1.0** state machine (checkpointing, resume-on-failure, HITL interrupt at PLAN approval) + SQLite. CrewAI-style roles as a naming pattern only. The **iterate** edge routes a failed gate back to the responsible stage (thermal fail → re-design; topology can't hit efficiency → re-plan).

---

## 3. RAG — the knowledge backbone (local-first)

The differentiator is grounding, so RAG is built **day one**, not deferred.

- **Corpus:** a **local directory of research papers/datasheets/standards** (PDFs), indexed once and reused. **Online retrieval is optional** (arXiv/web) and off by default — local-first for reproducibility and cost.
- **Engine:** PaperQA2 (local PDF indexing, citation-grounded answers, LiteLLM provider-agnostic) over LanceDB; PE-MAS's keyword+vector dual-path as a fallback ranker.
- **Used by:** the **Planner** (topology/control choice must cite papers), the **Designer** (datasheet-grounded component params), and the **Validator** (baseline efficiencies/THD/thermal limits to compare against).
- **Anti-hallucination gate:** a design claim without a retrievable citation is flagged, not shipped (evidence gate §5).

This directly answers the red-team's "training-knowledge dependence" objection — topology reasoning is grounded in the corpus, not the LLM's memory.

---

## 4. Simulation & validation — PLECS only (no surrogates)

- **PLECS is the sole simulator.** Every efficiency/THD/thermal number is a PLECS result (or a cited paper's). **No PINN, no learned surrogate screening** — this removes surrogate-infidelity risk and keeps evidence physically grounded, at the cost of more PLECS runs (acceptable: PLECS batch-parallelizes via list-of-optStructs).
- **Corners:** low-line / high-line / nominal, load points — the evidence matrix.
- **Loop cost control:** summarize every run to ~36 numbers before the LLM; cache by idempotency key (hash of ModelVars) so identical sims never re-run.

> **Why no PINN (design decision, 2026-07-17):** PLECS is fast enough with parallel batch, and a surrogate that disagrees with PLECS is worse than no surrogate for an evidence-gated system. PHIA/LP-COMDA ([[sources/ai-agents/phia-lpcomda-2026-physics-informed-pe-agent]]) is kept as reference only — not adopted.

---

## 5. Guardrails & evidence gates (from PE-MAS)

**Domain guardrails** (system-prompt hard rules + post-sim hooks): Tj margins (≤150 °C Si / 175 °C SiC, ≥25 °C margin), Vds ≤ 80 % Vbr, DC-link cap ≥ 1.2× Vdc, MI feasibility, P_loss≈ΔT/Rth consistency, efficiency < 100 %, standards flags (ISO 26262, CISPR 25, IEC 61800-5-1).

**Evidence gates** (corner-based, before release): efficiency ≥ cited baseline at ≥3 corners · Tj ≤ Tj,max−25 °C worst case · THD ≤ 5 % · every design claim cites a retrievable source · component stress within derating · human signoff. **No "PLECS-backed evidence" without a validated model in the registry.**

---

## 6. The critical path: validated PLECS models

Per PE-MAS's `model_registry.json`, the real bottleneck is validated per-topology models — an explicit workstream:

| Topology | Model + PMSM/IM load | Built by | Validation |
|----------|----------------------|----------|------------|
| 2L-B6 (SiC) | Phase 0 | efficiency + THD @ 3 corners |
| 3L-NPC | Phase 2 | + thermal |
| 3L-TNPC | Phase 2 | + thermal |
| ANPC | Phase 3 | + thermal + EMI |

---

## 7. Phases (~10–12 weeks)

### Phase 0 — Harness + corpus + one model (Weeks 1–2)
- PLECS harness (adapt PE-MAS `plecs-mcp`) + summarizer/regression/pass-fail pipeline; **verify PLECS license permits scripted batch (day 1).**
- Ingest the **local paper corpus** into RAG (PaperQA2 + LanceDB).
- Build + **validate the 2L-B6 SiC + PMSM** PLECS model.
- **Single agent** runs prompt→plan→design→validate on 2L-B6 (A/B control).
- **Acceptance:** one validated 2L-B6 design from a prompt; RAG cites real papers; token cost/iteration measured.

### Phase 1 — The 4-stage MAS (Weeks 3–5)
- LangGraph pipeline: Orchestrator + Planner(RAG) + Designer + Validator(k=3), with the **iterate** loop and a HITL plan-approval interrupt.
- Support both prompt modes: **design-new** and **iterate-existing** (user supplies a design/plan → re-plan/re-design).
- Guardrails + evidence gates wired in.
- **Acceptance:** MAS ≥ single-agent design quality on 2L-B6; iterate-existing path demonstrably improves a supplied design.

### Phase 2 — Topology breadth (Weeks 6–8)
- Add validated **3L-NPC / 3L-TNPC** models; Planner chooses among ≥3 topologies (RAG-grounded), Validator confirms each in PLECS.
- **Acceptance:** system selects + validates a topology from ≥3 candidates for a given spec, all evidence-gated.

### Phase 3 — Grounding depth + earned specialists (Weeks 9–10)
- Expand corpus; tighten citation gate (≥80 % of claims cite a retrievable source).
- Add **ANPC** model. Add a **Thermal** or **Component** agent **only if** the Validator shows it's the recurring failing gate.
- **Acceptance:** ANPC validated; specialists added only against measured need.

### Phase 4 — Hardening (Weeks 11–12)
- Watchdog + idempotency (light — LangGraph 1.0 does more), packaged CLI, HITL review, published **traction-inverter benchmark** (3–5 specs w/ reference designs), single-vs-MAS A/B reported.

---

## 8. Open questions & risks

**Questions:** Does the 4-stage MAS beat a single agent (P0 vs P1)? Measured $/design? Is the local corpus large/relevant enough to ground topology choices? Which specialist (if any) is earned?

| Risk | Mitigation |
|------|-----------|
| **Validated PLECS models are the bottleneck** | Explicit model workstream; gate evidence on registry status |
| PLECS license blocks scripted batch | **Verify Phase 0 day 1** |
| RAG corpus too thin to ground decisions | Curate corpus early; citation gate surfaces gaps |
| PLECS-only = many sim runs | Parallel batch (list-of-optStructs) + idempotency cache |
| Multi-agent overhead > benefit | P0/P1 A/B; prune (AgentSlimming) |
| Token blowup | Mandatory summarization; complexity routing |
| Confidence inflation from adjacent-domain papers | Hold domain claims at C3 until a PE A/B exists |

---

← [[README]] | [[sources/ai-agents/pe-mas-flyback-mas]] | [[ai-agents/harness/plecs-integration]] | [[audits/ai-agent-docs-audit-2026-07-17]]
