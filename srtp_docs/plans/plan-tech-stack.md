---
title: "Plan — Tech stack & LLM routing"
type: plan
field: project
created: 2026-07-17
updated: 2026-07-19
tags: [plan, ai-agents, plecs]
---

# Tech stack & LLM routing

> Topic of [[plan-ai-agent-mas]]. Consolidates the technology decisions, refreshed to mid-2026 currency ([[agent-frameworks-2026-currency]]). Full rationale for the older choices: [[implementation-research]] (note its §1.1 MATLAB backend is superseded by PLECS).

## 1. Stack

| Component | Choice | License | Why |
|---|---|---|---|
| **Simulator (sole evidence)** | PLECS 4.8 Standalone (XML-RPC/JSON-RPC + `plecs-mcp`) | commercial (installed) | native PMSM/IM + FOC; scriptable; PE-MAS prior art. [[plan-plecs-harness]] |
| **Orchestration** | LangGraph 1.0 StateGraph + SQLite checkpointer | MIT | durable-execution leader; checkpoint/resume, per-node timeouts, HITL |
| **Role semantics** | CrewAI patterns (naming only, not runtime) | MIT | no checkpointing → pattern donor, not engine |
| **Agent glue / LLM interface** | custom Python + **LiteLLM** | MIT | provider-agnostic (200+ providers) |
| **Optimizer** | scipy DE / pyswarm PSO / Ax-BoTorch or scikit-optimize BO | BSD/MIT | stage ③. [[plan-design-loop]] |
| **RAG** | PaperQA2 over LanceDB | Apache 2.0 | citation-grounded, LiteLLM-native. [[plan-knowledge-rag]] |
| **Memory** | SQLite (episodic/procedural) + LanceDB (semantic) | PD + Apache 2.0 | [[plan-memory]] |
| **Consensus** | DRCY multi-run (k=3 + separate reconcile model) | — | [[plan-guardrails-and-evidence]] |
| **CLI** | Click + Rich | BSD/MIT | CLI-first (decision A1); GUI deferred |

**Weigh but don't default to:** Microsoft Agent Framework (MAF) 1.0 — native MCP/A2A, attractive because the PLECS backend is an MCP server; only switch if LangGraph's MCP story proves worse in practice. **Excluded:** AutoGen (EOL), MATLAB Engine (backend pivot), PySpice/ltspice-mcp as primary (device-level only, optional).

## 2. LLM routing (provider-agnostic, complexity-based)

Route per task, cheapest capable model wins ([[implementation-research]] §1.2, re-tuned):

| Task | Tier | Example |
|---|---|---|
| orchestration / routing | cheap | deepseek-chat |
| topology + control selection (①) | strong | claude (sonnet/opus) |
| RAG literature grounding | strong | claude |
| structural refinement (②) | mixed | claude / deepseek |
| PLECS scripting / sweep driving | cheap | deepseek |
| optimizer objective evals | **no LLM** | pure tool (PLECS) |
| reviewer consensus judge | strong, **separate** from generator | claude (distinct context) |
| report writing | strong-writing | gpt / claude |

**Token discipline is architectural, not incidental:** summarize-before-LLM (invariant #3), the optimizer replaces LLM re-guessing with tool search (no LLM tokens in stage ③), and iteration traces are compacted ([[plan-memory]]). These three are what keep $/design bounded — measure it ([[plan-evaluation-and-benchmark]]).

← [[plan-ai-agent-mas]] | [[implementation-research]] | [[agent-frameworks-2026-currency]]
