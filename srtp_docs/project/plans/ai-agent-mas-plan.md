---
title: AI-Agent MAS Plan — PLECS-Backed Traction Inverter Design (hub)
type: plan
field: project
created: 2026-07-17
updated: 2026-07-17
tags: [plan, ai-agents, multi-agent, plecs]
---

# AI-Agent MAS Plan — Hub

> **The single AI-agent plan, split into topics.** This file is the **hub**: system schematic, invariants, prior-art anchor, topic map, and the build-order DAG. Topics are organized by *subsystem*, not by phase; the build-order DAG (below) gives the split points when the work is phased. Grounded in [[audits/ai-agent-docs-audit-2026-07-17]] and [[audits/plan-sufficiency-review-2026-07-17]].
> **Prior art:** [[sources/ai-agents/pe-mas-flyback-mas]] (adopt its structure). **Backend:** PLECS only. **Knowledge:** RAG over a local research-paper corpus. **No surrogates as evidence** — PLECS is the sole source of truth (a surrogate may later accelerate *search* only; see [[project/plans/design-loop]]).

---

## 0. What the system does

**One user prompt → a validated traction-inverter design.** The prompt either (a) **designs new** from a spec, or (b) **iterates an existing design** the user supplies. The value the MAS adds is the reasoning a coding-agent cannot do alone — **topology choice, control-strategy selection, physics interpretation, literature grounding** ([[sources/ai-agents/plecs-ai-agent-integration-ordonez]]); everything mechanical (parametrization, sweeps, optimization, regression) is cheap tool work over PLECS.

### System schematic (subsystem view)

```mermaid
flowchart TB
    U(["User prompt<br/>(new spec OR design to iterate)"]) --> ORCH
    subgraph CORE["3-agent core (LangGraph workflow)"]
        ORCH["ORCHESTRATOR<br/>parse · route · stop"]
        PLAN["PLANNER<br/>① topology + control<br/>(RAG-grounded)"]
        DES["DESIGNER<br/>② refine · ③ parameter-optimize"]
        VAL["VALIDATOR<br/>corner sweep · gates · k=3 consensus"]
        ORCH --> PLAN --> DES --> VAL
        VAL -. "iterate: params→③ · structure→② · architecture→①" .-> ORCH
    end
    VAL --> REP["REPORT"] --> R(["result"])
    RAG[("RAG service<br/>local paper corpus")] -.-> PLAN
    RAG -.-> DES
    RAG -.-> VAL
    PLECS[("PLECS service<br/>templates · optimizer · summarizer")] -.-> DES
    PLECS -.-> VAL
    MEM[("Memory<br/>episodic · procedural · semantic")] -.-> CORE
```

The pipeline is a **prompt-chain workflow with an evaluator-optimizer inner loop** ([[ai-agents/agentic-workflow-patterns]]); the DESIGN box is itself the **topology→refine→parameter-optimize** loop ([[ai-agents/design-loop-architecture]]).

---

## Invariants

1. **Ground every design decision in retrieved papers.** No un-cited topology/control choices. RAG is the backbone, not a bolt-on. → [[project/plans/knowledge-rag]]
2. **PLECS is the only source of evidence.** No PINN/surrogate *as evidence*. If a number isn't from PLECS (or a cited paper), it isn't evidence. → [[project/plans/plecs-harness]]
3. **Summarize before the LLM.** Engineered ~36-number summaries, never raw waveforms (~1000× token delta). → [[project/plans/plecs-harness]]
4. **The LLM picks structure; an optimizer picks numbers.** DESIGN converges via an explicit numerical optimizer over PLECS, not LLM re-guessing. → [[project/plans/design-loop]]
5. **Start at 3 agents; earn specialists against a measured failing gate.** (AgentSlimming.) → [[project/plans/architecture]]
6. **No "PLECS-backed evidence" without a validated model in the registry.** → [[project/plans/plecs-harness]]

---

## Prior-art anchor: PE-MAS

Adopt PE-MAS's proven structure ([[sources/ai-agents/pe-mas-flyback-mas]]), re-targeted flyback → traction:

| Adopt from PE-MAS | SRTP use | Topic |
|---|---|---|
| `requirements → designer → validator → reporter` flow | Plan → Design → Validate → Report | [[project/plans/architecture]] |
| Typed `PowerSupplyState` (~30 fields) | typed `InverterDesignState` | [[project/plans/architecture]] |
| `plecs-mcp` + XML-RPC (`PE_MAS_PLECS_BACKEND=auto`) | PLECS harness | [[project/plans/plecs-harness]] |
| Template + `ModelVars` / XML-injection | per-topology validated templates | [[project/plans/plecs-harness]] |
| `model_registry.json` (honest per-topology status) | same, traction topologies | [[project/plans/plecs-harness]] |
| Guardrails + corner-based evidence gates | re-tuned to traction | [[project/plans/guardrails-and-evidence]] |
| Lifelong memory + iteration playbooks | episodic + procedural memory | [[project/plans/memory]] |
| Dual-path RAG | elevated to first-class | [[project/plans/knowledge-rag]] |

**Change from PE-MAS:** flyback → traction (2L-B6, 3L-NPC/TNPC, ANPC + PMSM/IM); provider-agnostic LLMs; RAG central; explicit parameter optimizer; no PINN as evidence.

---

## Topic map

| Topic | Covers | Fills gap |
|---|---|---|
| [[project/plans/architecture]] | agents, orchestration, shared services, **typed state schema** | G-C |
| [[project/plans/design-loop]] | topology→refine→**parameter-optimize**, evaluator-optimizer, iterate routing, stopping rule | G-A/B/H |
| [[project/plans/knowledge-rag]] | corpus, ingestion, citation gate, coverage audit | G-G |
| [[project/plans/plecs-harness]] | PLECS service, templates, **model-validation procedure + registry**, **5-layer summarizer contract** | G-E/F |
| [[project/plans/guardrails-and-evidence]] | domain guardrails + evidence gates (the evaluator rubric) | — |
| [[project/plans/memory]] | episodic · procedural · semantic · isolation; what's deferred | G-D |
| [[project/plans/tech-stack]] | frameworks, LLM routing, licenses | — |
| [[project/plans/evaluation-and-benchmark]] | benchmark, single-vs-MAS A/B, open questions, risks | — |

Gap IDs (G-A…G-H) are defined in [[audits/plan-sufficiency-review-2026-07-17]].

---

## Build order (dependency graph — split points for phasing)

Phasing is a cut across this DAG; the dependencies, not the calendar, set the order.

```mermaid
flowchart TD
    L["PLECS license check<br/>(scripted batch allowed?)"] --> H["PLECS harness<br/>+ 5-layer summarizer"]
    H --> M1["2L-B6-SiC template<br/>+ validate vs reference"]
    C["RAG corpus ingest<br/>+ citation gate"] --> SA["single-agent baseline<br/>(A/B control)"]
    M1 --> SA
    ST["InverterDesignState<br/>+ LangGraph skeleton"] --> MAS["3-agent MAS<br/>Plan·Design·Validate"]
    SA --> MAS
    OPT["optimizer (grid→DE)<br/>stage ③"] --> MAS
    G["guardrails + evidence gates"] --> MAS
    MAS --> BR["breadth: 3L-NPC/TNPC<br/>+thermal, then ANPC +EMI"]
    MAS --> BM["benchmark + single-vs-MAS A/B"]
    BR --> SP["earned specialist<br/>(only if a gate keeps failing)"]
```

**Natural split points** (each a candidate phase boundary): harness+summarizer+first validated model → single-agent baseline on 2L-B6 (A/B control) → 3-agent MAS with optimizer + gates → topology breadth → earned specialists + hardening. First milestone (definition of done) in [[project/plans/evaluation-and-benchmark]] §5.

**Hard prerequisite:** the PLECS license check gates everything downstream — do it before harness work.

---

← [[README]] | [[sources/ai-agents/pe-mas-flyback-mas]] | [[audits/plan-sufficiency-review-2026-07-17]] | [[ai-agents/design-loop-architecture]]
