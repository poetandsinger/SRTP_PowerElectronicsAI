---
title: "Plan — Knowledge / RAG backbone"
type: plan
field: project
created: 2026-07-17
updated: 2026-07-19
tags: [plan, ai-agents, plecs, design-automation]
---

# Knowledge / RAG backbone

> Topic of [[plan-ai-agent-mas]]. RAG is invariant #1 (ground every decision), so it is built day one, not deferred. Fills gap G-G (corpus/index asserted but unspecified). Research basis: AnalogSAGE's RAG-over-10k-papers grounding ([[analogsage-2025-self-evolving-analog-mas]]), PaperQA2 ([[implementation-research]] §1.5).

## 1. Corpus (local-first)

- A **local directory** of research papers / datasheets / standards (PDFs), indexed once and reused. **Online retrieval (arXiv/web) is optional and off by default** — local-first for reproducibility and cost.
- **Seed corpus is the vault's own `sources/` + the reference designs** ([[index-reference-designs]]) + curated topology/control/thermal papers. This makes the citation gate real from day one.
- **Coverage audit (new):** before claiming a topology is "groundable," check the corpus actually contains ≥N retrievable sources for it. A thin corpus silently degrades invariant #1. Track per-topology coverage next to the model registry ([[plan-plecs-harness]]).

## 2. Engine

- **PaperQA2** (local PDF indexing, citation-grounded answers, LiteLLM provider-agnostic) over **LanceDB** (shared vector store with Memory — [[plan-memory]]).
- **PE-MAS dual-path** (keyword + vector) as a fallback ranker for datasheet lookups where semantic search underperforms on part numbers.

## 3. Who uses it

- **Planner (①):** topology + control choice **must cite** retrievable papers → `plan_citations` in state.
- **Designer (②):** datasheet-grounded component/parameter bounds.
- **Validator:** baseline efficiencies / THD / thermal limits to compare the design against.

## 4. Citation gate (anti-hallucination)

A design claim without a retrievable citation is **flagged, not shipped** (an evidence gate — [[plan-guardrails-and-evidence]]). Mechanics to specify:
- a "claim" = any topology/control/component decision recorded in state;
- "retrievable" = PaperQA2 returns a supporting passage above a relevance threshold from the **local** corpus (not the LLM's memory);
- the gate reports **% of claims cited**; the evaluation target tightens this over time ([[plan-evaluation-and-benchmark]]).

This is the direct answer to the red-team's "training-knowledge dependence" objection ([[traction-inverter-mas-integration]] §7): topology reasoning is grounded in the corpus, not LLM training data.

## 5. Deferred

- Self-evolving / stratified knowledge memory (AnalogSAGE's 4-layer scheme) — capable but heavy; adopt only if flat RAG proves insufficient to ground decisions ([[plan-memory]]).
- Online/agentic web retrieval — enable per-run behind a flag when the local corpus is demonstrably thin for a spec.

← [[plan-ai-agent-mas]] | [[plan-memory]] | [[plan-guardrails-and-evidence]] | [[analogsage-2025-self-evolving-analog-mas]]
