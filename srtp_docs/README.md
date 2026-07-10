---
title: README
type: index
field: root
created: 2026-07-06
updated: 2026-07-08
tags: [index]
---

# SRTP Power Electronics AI

> **Standalone desktop GUI for AI-assisted traction inverter design.**  
> **Architecture:** PySide6/Qt + smolagents + external MATLAB  
> **Research vault:** Science Research Vault conventions — every claim carries truth-status, evidence-strength, and mandatory red-team review.  
> **Status:** 🟢 Research in progress
> **Last Updated:** 2026-07-08

---

## Vault Structure

```
srtp_docs/                  # RESEARCH_VAULT
├── SCHEMA.md               # Conventions, taxonomy, status/evidence rules
├── catalog.md              # Every note, grouped by field then status
├── log.md                  # Append-only action log
├── README.md               # This file
├── citations.md            # Master bibliography (42 refs, IEEE format)
├── sources/                # Layer 1: immutable paper captures (future)
├── ee/                     # Power electronics research
│   ├── traction-inverter/  # Topologies, SiC/GaN, control, MATLAB
│   ├── problem-statement/  # Why AI for traction inverter design
│   └── audit-*.md          # Literature audits
├── cs/                     # AI agent architecture research
│   ├── harness/            # Claude Code, Codex CLI, Hermes, LangGraph, etc.
│   └── agent-papers/       # ReAct, Toolformer, DSO.ai, ChemCrow
├── _index/                 # Field/topic hub notes
│   ├── ee.md               # EE field hub
│   └── cs.md               # CS field hub
├── _archive/               # Superseded notes
├── _lint/                  # Lint reports
└── implementation/         # Operational: project plans, changelogs (not research claims)
```

## Research

| Field | Hub | Content |
|-------|-----|---------|
| EE — Power Electronics | [[_index/ee]] | Traction inverter design, SiC/IGBT/GaN, topologies, control, MATLAB modeling |
| CS — Agent Architecture | [[_index/cs]] | 14 harnesses surveyed, architecture patterns, MATLAB integration strategies |

## Implementation

| Area | Index | Content |
|------|-------|---------|
| Plan | `implementation/plans/plan index` | 12-week roadmap, architecture, tech stack, risks |
| Changelog | `implementation/changelog/changelog index` | Change tracking |

## References

| File | Content |
|------|---------|
| [[citations]] | All citations, credits, licenses — single source (42 refs) |

# Programs
- MATLAB is installed in C:\Program Files\MATLAB\R2024a\bin
- PLECS is installed in C:\Users\ferre\OneDrive\Documents\Plexim\PLECS 4.8 (64 bit)

## Conventions

- **Every claim note has a red-team block** — no red-team, no file.
- **Truth-status on every claim:** `supported | contested | refuted | unverified`
- **Evidence-strength on every claim:** `replicated | single-study | theoretical | disputed`
- **Append-first:** search existing notes before creating new ones.
- **Contradictions surface, never overwrite.**
See [[SCHEMA.md]] for full conventions.

---

← [[catalog]] | [[_index/ee]] | [[_index/cs]]
