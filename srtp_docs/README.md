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
> **Architecture:** LangGraph StateGraph + PySpice/ngspice + LiteLLM (CLI-first, provider-agnostic)
> **Method:** Science Research Vault — every claim carries truth-status, evidence-strength, and a mandatory red-team block.
> **Status:** 🟡 Research complete — Phase 0 implementation ready

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
├── power-electronics/      # FIELD: what to design
│   ├── traction-inverter/  #   14 notes — topologies, components, control, sim, standards, market
│   └── problem-statement/  #   Why AI for traction inverter design
│
├── ai-agents/              # FIELD: how to build the designer
│   ├── harness/            #   12 deep dives — Claude Code, Codex, LangGraph, CrewAI, AutoGen…
│   ├── agent-papers/       #   Agent architectures from research papers
│   ├── claim-*.md          #   Red-teamed claims (MAS > single-agent, token reduction)
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
├── audits/                 # 4 lint reports + self-audits of the vault
│
└── project/                # OPERATIONAL (no truth-status — these are decisions, not findings)
    ├── plans/              #   5 phase plans + architecture + tech-stack + risks
    └── changelog/          #   Dated log of what changed
```

## Research

| Field | Hub | Content |
|-------|-----|---------|
| Power Electronics | [[maps/power-electronics]] | 15 traction inverter notes (red-teamed) + 6 source papers |
| AI / Agent Architecture | [[maps/ai-agents]] | 12 harness deep dives, 12 source papers, 2 red-teamed claims, MAS bridge |

## Implementation

Full roadmap: [[project/plans/plans-index]]

| Phase | Plan | Goal |
|-------|------|------|
| 0 | [[project/plans/phase-0-foundation]] | Single-agent baseline + A/B test (PySpice/ngspice) |
| 1 | [[project/plans/phase-1-multi-agent]] | 3-agent LangGraph core with guardrails |
| 2 | [[project/plans/phase-2-simulation]] | MATLAB/PySpice dual-engine + ltspice-mcp |
| 3 | [[project/plans/phase-3-knowledge]] | PaperQA2 + Nexar components + memory |
| 4 | [[project/plans/phase-4-production]] | Watchdog, HITL, benchmark, CLI packaging |

Supporting: [[project/plans/architecture]] · [[project/plans/tech-stack]] · [[project/plans/risks-metrics]] · [[ai-agents/implementation-research]]

## Key Architecture Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| A1 | **CLI-first** (not GUI) | Remove UI complexity from the critical path. Prove the agent works first. |
| A2 | **3 agents** (not 7) | Orchestrator + Simulation + Reviewer. Minimal decomposition for A/B test. |
| A3 | **PySpice primary** (not MATLAB-only) | Free, no license dependency, works immediately. MATLAB added in Phase 2. |
| A4 | **SQLite** (not Postgres) | LangGraph checkpointer works with SQLite. Zero setup. |
| A5 | **LiteLLM provider-agnostic** | Route to cheapest capable model per task (DeepSeek for sim scripts, Claude for review). |

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
