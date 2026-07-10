---
title: README
type: index
field: root
created: 2026-07-06
updated: 2026-07-10
tags: [index]
---

# SRTP Power Electronics AI

> **AI-powered multi-agent system for traction inverter design.**  
> **Architecture:** LangGraph StateGraph + PySpice/ngspice + LiteLLM (CLI-first, provider-agnostic)  
> **Research vault:** Science Research Vault conventions — every claim carries truth-status, evidence-strength, and mandatory red-team review.  
> **Status:** 🟡 Research complete — Phase 0 implementation ready  
> **Last Updated:** 2026-07-10

---

## Vault Structure

```
srtp_docs/                  # RESEARCH_VAULT
├── SCHEMA.md               # Conventions, taxonomy, status/evidence rules
├── catalog.md              # Every note, grouped by field then status
├── README.md               # This file
├── citations.md            # Master bibliography (42 refs, IEEE format)
├── sources/                # Layer 1: 18 source notes (5 ee/, 13 cs/)
│   ├── ee/                 #   6 traction inverter papers + AI sustainability
│   └── cs/                 #   MAS papers, prior art (PE-MAS, PE-GPT, ABB), tool research
├── ee/                     # Power electronics research (14 notes)
│   ├── traction-inverter/  #   topology-landscape, simulation-workflows,
│   │                       #   standards-landscape, market-trends (2025-2026),
│   │                       #   research-synthesis hub, circuit-topologies,
│   │                       #   components, control-schemes, control-how-to,
│   │                       #   matlab-modeling, simulation-toolbox, open-problems
│   └── problem-statement/  #   Why AI for traction inverter design
├── cs/                     # AI agent architecture research (18 notes)
│   ├── harness/            #   14 harness deep dives (Hermes, Claude Code, LangGraph, CrewAI…)
│   ├── agent-papers/       #   ReAct, Toolformer, DSO.ai, ChemCrow
│   ├── traction-inverter-mas-integration.md  # Bridge: 7-agent architecture for inverter design
│   ├── implementation-research.md            # Verified tech stack, APIs, code patterns
│   ├── multi-agent-synthesis.md              # Cross-harness synthesis + PE-MAS validation
│   ├── ai-ml-power-electronics-2025-2026.md  # 16 AI/ML applications in PE design
│   ├── design-automation-gaps-2025-2026.md   # 10 gaps, 11 AI augmentation opportunities
│   ├── claim-multi-agent-outperforms-single.md         # C4: MAS > single-agent
│   └── claim-hybrid-architecture-token-reduction.md    # C4: 76% token reduction
├── _index/                 # Field/topic hub notes
│   ├── ee.md
│   └── cs.md
├── _archive/               # Superseded notes (old phase plans, old structure)
├── _lint/                  # 2 audit reports (2026-07-09, 2026-07-10)
├── changelog/              # log.md + audit-changelog-traction-inverter.md
└── implementation/         # Operational: 5 phase plans, architecture, research
```

## Research

| Field | Hub | Content |
|-------|-----|---------|
| EE — Power Electronics | [[_index/ee]] | 14 traction inverter notes (all red-teamed), 6 source notes, 4 new 2025-2026 topic notes |
| CS — Agent Architecture | [[_index/cs]] | 14 harness deep dives, 13 source notes, 2 claim notes, 2 AI/automation notes, MAS bridge |

## Implementation

| Area | Plan | Status |
|------|------|--------|
| Phase 0 | [[implementation/plans/phase-0-foundation]] | Single-agent baseline + A/B test (PySpice/ngspice) |
| Phase 1 | [[implementation/plans/phase-1-multi-agent]] | 3-agent LangGraph core with guardrails |
| Phase 2 | [[implementation/plans/phase-2-simulation]] | MATLAB/PySpice dual-engine + ltspice-mcp |
| Phase 3 | [[implementation/plans/phase-3-knowledge]] | PaperQA2 + Nexar components + memory |
| Phase 4 | [[implementation/plans/phase-4-production]] | Watchdog, HITL, benchmark, CLI packaging |
| Architecture | [[implementation/plans/multi-agent-architecture]] | Original architecture plan (validated by PE-MAS) |
| Research | [[cs/implementation-research]] | Verified APIs, code patterns, tech decisions |

## Key Architecture Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| A1 | **CLI-first** (not GUI) | Remove UI complexity from the critical path. Prove the agent works first. |
| A2 | **3 agents** (not 7) | Orchestrator + Simulation + Reviewer. Minimal decomposition for A/B test. |
| A3 | **PySpice primary** (not MATLAB-only) | Free, no license dependency, works immediately. MATLAB added in Phase 2. |
| A4 | **SQLite** (not Postgres) | LangGraph checkpointer works with SQLite. Zero setup. |
| A5 | **LiteLLM provider-agnostic** | Route to cheapest capable model per task (DeepSeek for sim scripts, Claude for review). |

## References

| File | Content |
|------|---------|
| [[citations]] | All citations, credits, licenses — single source (42 refs) |
| [[catalog]] | Every note, grouped by field then status |
| [[SCHEMA]] | Full conventions, taxonomy, status/evidence rules |

## Programs

- MATLAB is installed in `C:\Program Files\MATLAB\R2024a\bin`
- PLECS is installed in `C:\Users\ferre\OneDrive\Documents\Plexim\PLECS 4.8 (64 bit)`

## Conventions

- **Every claim note has a red-team block** — no red-team, no file.
- **Truth-status on every claim:** `supported | contested | refuted | unverified`
- **Evidence-strength on every claim:** `replicated | single-study | theoretical | disputed`
- **Confidence-ranked claims** (C1–C5) on integration notes
- **Append-first:** search existing notes before creating new ones.
- **Contradictions surface, never overwrite.**
- See [[SCHEMA]] for full conventions.

---

← [[catalog]] | [[_index/ee]] | [[_index/cs]]
