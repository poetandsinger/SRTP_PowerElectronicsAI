---
title: "Plan — Memory architecture"
type: plan
field: project
created: 2026-07-17
updated: 2026-07-17
tags: [plan, ai-agents, multi-agent]
---

# Memory architecture

> Topic of [[project/plans/ai-agent-mas-plan]]. Fills gap G-D (memory named as a choice, not designed). Framed against the 2026 context-engineering taxonomy ([[sources/ai-agents/context-engineering-2026]]); depth ceiling from AnalogSAGE ([[sources/ai-agents/analogsage-2025-self-evolving-analog-mas]]); baseline from PE-MAS lifelong memory.

## 1. Four memory roles (name them, then decide depth)

| Role | Holds | Store | Status |
|---|---|---|---|
| **Working** | the live LangGraph state ([[project/plans/architecture]] §4) | context window | built-in |
| **Episodic** | design records keyed by spec-hash: spec → topology → params → gate results → quality score | SQLite | **build** (PE-MAS proven) |
| **Procedural** | **iteration playbooks** — which fix worked for which failed gate | SQLite | **build** (PE-MAS proven; cheap, high-value) |
| **Semantic** | the paper corpus / domain facts | LanceDB (shared w/ RAG) | **build** ([[project/plans/knowledge-rag]]) |

## 2. Context-engineering obligations (the checklist)

- **Write / offload:** PLECS results, design records, corpus live outside context; only summaries enter it (invariant #3).
- **Select / retrieve:** RAG for the Planner; the Validator retrieves the *matching baseline* for the design under test, not the whole corpus.
- **Compress / compact:** two compactions — the ~36-number PLECS summary (domain) **and** the per-iteration reasoning-trace compaction (AnalogSAGE Compression Module). Without the second, a long re-design loop reinflates context and the cost story breaks ([[project/plans/design-loop]] §3).
- **Isolate:** per-agent context scoping — the Planner sees papers/prose; the Validator sees numbers, not prose; the optimizer sees only the objective. Prevents one agent's clutter polluting another's reasoning.

## 3. Deferred (earn it)

- **Stratified self-evolving memory** (AnalogSAGE's Evolution + Introspective layers — cross-task insight accumulation, within-task failure reflection). Powerful and clearly the 2026 SOTA, but heavy. Adopt **only if** episodic + procedural memory prove insufficient to improve iteration quality across runs. Keep the schema forward-compatible so this is an addition, not a rewrite.
- **Cross-session persistence beyond SQLite** (Hermes-style). Not needed until the single-run loop works.

## 4. Why simple first

PE-MAS ships a working system on plain SQLite lifelong memory; AgentSlimming's lesson generalizes — start minimal, add sophistication against measured need. The four roles above are the minimum that makes the **procedural** memory (playbooks) and **isolation** (per-agent context) real — the two things the original "SQLite + LanceDB, kept simple" line left undefined.

← [[project/plans/ai-agent-mas-plan]] | [[project/plans/knowledge-rag]] | [[sources/ai-agents/context-engineering-2026]]
