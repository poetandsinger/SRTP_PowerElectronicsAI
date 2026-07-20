---
title: "Context Engineering & Agent Memory — 2026 practice + survey"
type: source
field: ai-agents
tags: [ai-agents, architecture, patterns, multi-agent, orchestration, review]
authors: [multiple — practitioner guides + arXiv surveys]
year: 2026
venue: "arXiv surveys (2507.13334 context engineering; 2603.07670 agent memory) + practitioner guides"
url: "https://arxiv.org/abs/2507.13334"
captured: 2026-07-17
reliability: medium
peer_reviewed: false
reliability_note: "Mix of arXiv surveys (medium) and vendor/practitioner blogs (low-medium, marketing-adjacent). The taxonomy (write/select/compress/isolate; five memory types) is consistent across independent sources, so the *framing* is reliable even where individual numbers are not. Not power-electronics-specific — general agent-engineering discipline."
---

# Context Engineering & Agent Memory — 2026 snapshot

**Why it matters for SRTP:** the plan's core cost rule — *summarize before the LLM* ([[plecs-ai-agent-integration-ordonez]]) — is one tactic inside a named discipline, **context engineering**. The discipline gives SRTP a checklist for the memory/summarization design instead of one ad-hoc rule, and maps onto the [[plan-ai-agent-mas|plan]].

## The four operations (write / select / compress / isolate)
A 2026 survey of context engineering ([arXiv 2507.13334]) organises the field into four operations:
- **Write / offload** — move state out of the context window into an external store (files, SQLite, vector DB) and page it back in on demand. *SRTP:* PLECS results, design records, and the paper corpus live outside context; only summaries enter it.
- **Select / retrieve** — inject only the records relevant to the current step (semantic + recency + importance scoring). *SRTP:* RAG retrieval for the Planner; retrieve the matching baseline for the Validator.
- **Compress / compact** — summarise older history when nearing the window limit. *SRTP:* the ~36-number PLECS summary is a domain-specific compaction; iteration traces should be compacted too.
- **Isolate** — separate context per sub-task/agent so one agent's clutter doesn't pollute another's reasoning. *SRTP:* per-agent context (Planner sees papers; Validator sees numbers, not prose) — the [[harness-architecture-patterns|granular-context]] pattern.

## Five memory types (agent-memory survey, arXiv 2603.07670)
Working (the live context window) · episodic (past design runs) · semantic (domain facts / the RAG corpus) · procedural (how-to playbooks / skills) · and long-term stores that persist across sessions. This cognitive framing lines up with the SRTP memory split: **episodic = design records**, **semantic = RAG corpus**, **procedural = iteration playbooks / skills**.

## SRTP implications
- The plan's "SQLite + LanceDB, kept simple" is defensible, but it should be *named against this taxonomy* so gaps are visible: SRTP has write/offload + select/retrieve + a domain compaction, but **isolation** (per-agent context scoping) and **procedural memory** (iteration playbooks) are under-specified. See [[plan-memory]].
- Compaction is not just the 36-number summary: **iteration reasoning traces** must also be compacted, or a long re-design loop reinflates the context (the AnalogSAGE "Compression Module" does exactly this — [[analogsage-2025-self-evolving-analog-mas]]).
- This is *engineering discipline*, not domain evidence — no PE-specific result here. Use as a design checklist, not a citation for design quality.

← [[harness-index]] | [[agentic-workflow-patterns]] | [[plan-memory]]
