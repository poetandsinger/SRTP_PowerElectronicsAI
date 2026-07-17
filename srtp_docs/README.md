---
title: README
type: map
field: root
created: 2026-07-06
updated: 2026-07-17
tags: [index]
---

# SRTP Power Electronics AI

> **AI-powered multi-agent system for traction inverter design.**
> **Architecture:** LangGraph + **PLECS** (XML-RPC/MCP) + LiteLLM (CLI-first, provider-agnostic)
> **Method:** Science Research Vault — every claim carries truth-status, evidence-strength, and a mandatory red-team block.
> **Status:** 🟡 Knowledge base built (29-chapter textbook, cited [1]–[148]) + AI-agent architecture research complete; implementation plan is spec-level and phase-ready ([[ai-agent-mas-plan]]). **Next: PLECS license check → harness + first validated 2L-B6 model.**

---

## What This Vault Is

Two research fields feeding one build. **Power electronics** research defines *what* to design (traction inverters); **AI agents** research defines *how* to build the system that designs them. Every folder name is plain English, every file carries metadata, and every research claim has been red-teamed. See [[SCHEMA]] for the full rules.

## Vault Structure

```
srtp_docs/
├── README.md               # This file
├── SCHEMA.md               # The rules: folders, metadata, status/evidence, red-team
├── catalog.md              # Every note, one line, grouped by field then status
├── citations.md            # Master bibliography (IEEE format)
│
├── power-electronics/      # FIELD: what to design — traction-inverter ENGINEERING ONLY (29-chapter textbook)
│   └── traction-inverter/  #   fundamentals · topologies · components · materials · machine · control ·
│                           #   design-procedure · schematics · thermal · gate-drive · protection/safety ·
│                           #   EMI/EMC · packaging · BOM+prices · trade-offs · 2 worked examples ·
│                           #   4 reference designs · manufacturing/test · reliability · simulation · standards
│
├── problem-statement/      # PREFACE (not engineering): why AI for traction inverter design,
│                           #   market, workforce, competitive landscape (moved out of power-electronics/ 2026-07-17)
│
├── ai-agents/              # FIELD: how to build the designer
│   ├── harness/            #   12 deep dives — Claude Code, Codex, LangGraph, CrewAI, AutoGen…
│   ├── agent-papers/       #   Agent architectures from research papers
│   ├── claim-*.md          #   Red-teamed claims (MAS > single-agent, token reduction)
│   ├── agentic-workflow-patterns.md  #   2026 pattern catalog mapped to SRTP
│   ├── design-loop-architecture.md   #   topology→refine→parameter-optimize (the key finding)
│   └── *.md                #   MAS integration bridge, synthesis, implementation research
│
├── sources/                # LAYER 1: immutable raw captures (never edited)
│   ├── power-electronics/  #   6 source papers
│   └── ai-agents/          #   12 source papers
│
├── maps/                   # Navigation hubs (one per field)
│   ├── power-electronics.md
│   └── ai-agents.md
│
├── audits/                 # 5 lint reports + self-audits of the vault
│
└── project/                # OPERATIONAL (no truth-status — these are decisions, not findings)
    ├── plans/              #   ai-agent-mas-plan (hub) + 8 topic files (architecture, design-loop,
    │                       #   knowledge-rag, plecs-harness, guardrails-and-evidence, memory,
    │                       #   tech-stack, evaluation-and-benchmark) — no phases
    └── changelog/          #   Dated setup milestones
```

## Research

| Field | Hub | Content |
|-------|-----|---------|
| Power Electronics | [[maps/power-electronics]] | **29-chapter traction-inverter textbook** (red-teamed, cited [1]–[148]) + 6 source papers |
| Problem Statement (preface) | [[problem-statement/problem-statement-index]] | Why AI for traction inverter design: market, workforce, competitive landscape |
| AI / Agent Architecture | [[maps/ai-agents]] | 12 harness deep dives, 19 source captures, 2 red-teamed claims, workflow-patterns + design-loop findings, MAS bridge |

> **The textbook is grounded but not yet PLECS-validated:** design/thermal/loss numbers are closed-form or teardown/vendor figures, flagged in each chapter's Red Team. Turning them into simulation-backed evidence is the top depth-first task — see `HANDOFF-DEPTH-RESEARCH.md` (repo root).

## Implementation

**The plan:** [[ai-agent-mas-plan]] (hub) — PLECS-backed MAS, 3-agent core (Planner + Designer + Validator, Orchestrator drives), RAG-first, evidence-gated. Split into **8 topic files, no phases**: [[architecture]] · [[design-loop]] · [[knowledge-rag]] · [[plecs-harness]] · [[guardrails-and-evidence]] · [[memory]] · [[tech-stack]] · [[evaluation-and-benchmark]]. The core mechanism is a **topology → refine → parameter-optimize** design loop with an *explicit numerical optimizer* over PLECS (the LLM picks structure, the optimizer picks numbers).

Grounded in: [[audits/plan-sufficiency-review-2026-07-17]] · [[audits/ai-agent-docs-audit-2026-07-17]] · [[ai-agents/design-loop-architecture]] · [[ai-agents/agentic-workflow-patterns]] · [[ai-agents/harness/plecs-integration]]

## Key Architecture Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| A1 | **CLI-first** (not GUI) | Remove UI complexity from the critical path. Prove the agent works first. |
| A2 | **3 agents** (not 7) | Orchestrator + Simulation + Reviewer. Minimal decomposition for A/B test. |
| A3 | **PLECS backend** (not MATLAB) | System-level PE sim with native PMSM/IM + FOC models; scriptable via XML-RPC/MCP. PySpice/ltspice-mcp for device-level only. (2026-07 pivot off MATLAB.) |
| A4 | **SQLite** (not Postgres) | LangGraph checkpointer works with SQLite. Zero setup. |
| A5 | **LiteLLM provider-agnostic** | Route to cheapest capable model per task (DeepSeek for sim scripts, Claude for review). |
| A6 | **Explicit optimizer** (LLM picks structure, optimizer picks numbers) | Every 2026 PE/analog design agent converges via a numerical optimizer (DE/PSO/BO), not LLM re-guessing. PLECS-only; surrogate is a deferred *search* accelerator, never evidence. See [[design-loop]]. |

## Conventions (see [[SCHEMA]])

- **Folder = field.** The folder a note lives in is its `field` value. No abbreviations.
- **Every file has frontmatter.** No metadata, no file.
- **Every claim has a red-team block.** No red-team, no claim.
- **Truth-status** on every claim: `supported | contested | refuted | unverified` (new claims default to `unverified`).
- **Evidence-strength** on every claim: `replicated | single-study | theoretical | disputed`.
- **Append-first.** Search before creating. **Contradictions surface, never overwrite.**

## References

| File | Content |
|------|---------|
| [[catalog]] | Every note, grouped by field then status |
| [[SCHEMA]] | Full conventions, taxonomy, status/evidence rules |
| [[citations]] | Master bibliography, credits, licenses |

## Programs

- MATLAB: `C:\Program Files\MATLAB\R2024a\bin`
- PLECS: `C:\Users\ferre\OneDrive\Documents\Plexim\PLECS 4.8 (64 bit)`

---

← [[catalog]] | [[maps/power-electronics]] | [[maps/ai-agents]]
