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
> **Status:** 🟡 Knowledge base built (29-chapter textbook, cited [1]–[165]) + AI-agent architecture research complete; implementation plan is spec-level and phase-ready ([[ai-agent-mas-plan]]). **PLECS confirmed licensed + XML-RPC-driveable (2026-07-18); a 2L-VSI+IPMSM+FOC drive retargeted to a family-car machine ran to completion (`worked-designs/family-car-400v-sic/`). Next: top-level outports → first quantitatively PLECS-validated 2L-B6 model.**

---

## What This Vault Is

Two research fields feeding one build. **Power electronics** research defines *what* to design (traction inverters); **AI agents** research defines *how* to build the system that designs them. Every folder name is plain English, every file carries metadata, and every research claim has been red-teamed. See [[SCHEMA]] for the full rules.

## Vault Structure

Top folder = **lifecycle stage** (source → digested note → trial → plan). Field lives in frontmatter and one shallow subfolder; the `.base` files do the indexing. Wikilinks are bare basenames, so files move between folders without breaking links.

```
srtp_docs/
├── README.md   SCHEMA.md   citations.md    # root docs (rules, bibliography)
├── catalog.base                            # master index — every note
├── notes.base  sources.base  trials.base  plans.base   # per-stage indexes
│
├── sources/                # raw capture — immutable, never edited
│   ├── power-electronics/  #   6 source papers
│   └── ai-agents/          #   19 source papers
│
├── notes/                  # digested: claims · topics · maps
│   ├── power-electronics/  #   traction-inverter engineering — topologies, devices, machine, control;
│   │                       #   4 topology-unit designs (2L-B6 + 3L TNPC/ANPC/NPC) + 3 external refs;
│   │                       #   procedures: procedure-design, procedure-control, procedure-simulation-and-validation (SOP);
│   │                       #   thermal, gate-drive, protection, EMI, packaging, BOM, reliability, standards
│   ├── ai-agents/          #   harness deep dives (Claude Code, Codex, LangGraph, CrewAI, AutoGen…),
│   │                       #   agent-paper notes, red-teamed claims, workflow-patterns, design-loop
│   └── problem-statement/  #   preface: why AI for inverter design — market, workforce
│
├── trials/                 # applied design runs — 5 worked examples + design-by-doing experiment
│                           #   (runnable artifacts live in worked-designs/, outside the vault)
│
├── plans/                  # implementation plans — ai-agent-mas-plan hub + 8 subsystem topics
│
└── log/                    # operational records (no truth-status — decisions, not findings)
    ├── changelog/          #   dated milestones
    └── audits/             #   lint reports + vault self-audits
```

> **Outside the vault** (repo root, non-markdown — executable artifacts can't carry frontmatter, so they live outside `srtp_docs/`): `worked-designs/` holds runnable design artifacts (Python loss models, `.plecs` files, results) that back the worked examples — e.g. `worked-designs/family-car-400v-sic/` behind [[worked-example-family-car-400v-sic]]. The depth-research roadmap is [[depth-research-plan]].

## Research

| Field | Hub | Content |
|-------|-----|---------|
| Power Electronics | [[traction-inverter-index]] | **Traction-inverter engineering** (red-teamed, cited [1]–[165]): 4 topology-unit designs, procedures + PLECS validation SOP, subsystem chapters, 3 external reference designs + 6 source papers |
| Problem Statement (preface) | [[problem-statement-index]] | Why AI for traction inverter design: market, workforce, competitive landscape |
| AI / Agent Architecture | [[harness-index]] | 12 harness deep dives, 19 source captures, 2 red-teamed claims, workflow-patterns + design-loop findings, MAS bridge |
| *Full inventory* | [[catalog.base]] | Live table of every note (field · type · status · evidence), auto-generated |

> **Grounded but not yet PLECS-validated:** design/thermal/loss numbers are closed-form or teardown/vendor figures, flagged in each Red Team. Turning them into simulation-backed evidence is the top task, now governed by a **PLECS validation SOP** ([[procedure-simulation-and-validation]] §4, gates S1–S7) and a **serial 4-topology build program** ([[depth-research-plan]]: 2L-B6 → TNPC → ANPC → NPC).

## Implementation

**The plan:** [[ai-agent-mas-plan]] (hub) — PLECS-backed MAS, 3-agent core (Planner + Designer + Validator, Orchestrator drives), RAG-first, evidence-gated. Split into **8 topic files, no phases**: [[architecture]] · [[design-loop]] · [[knowledge-rag]] · [[plecs-harness]] · [[guardrails-and-evidence]] · [[memory]] · [[tech-stack]] · [[evaluation-and-benchmark]]. The core mechanism is a **topology → refine → parameter-optimize** design loop with an *explicit numerical optimizer* over PLECS (the LLM picks structure, the optimizer picks numbers).

Grounded in: [[plan-sufficiency-review-2026-07-17]] · [[ai-agent-docs-audit-2026-07-17]] · [[design-loop-architecture]] · [[agentic-workflow-patterns]] · [[plecs-integration]]

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

- **Folder = stage.** The top folder is the lifecycle stage (`sources` → `notes` → `trials`/`plans`); `field` lives in frontmatter.
- **Links are bare basenames**, so notes move freely. Basenames stay globally unique.
- **Every file has frontmatter.** No metadata, no file.
- **Every claim has a red-team block.** No red-team, no claim.
- **Truth-status** on every claim: `supported | contested | refuted | unverified` (new claims default to `unverified`).
- **Evidence-strength** on every claim: `replicated | single-study | theoretical | disputed`.
- **Append-first.** Search before creating. **Contradictions surface, never overwrite.**

## References

| File | Content |
|------|---------|
| [[catalog.base]] | Master index — every note (field · type · status · evidence) |
| [[notes.base]] · [[sources.base]] · [[trials.base]] · [[plans.base]] | Per-stage indexes |
| [[SCHEMA]] | Full conventions, taxonomy, status/evidence rules |
| [[citations]] | Master bibliography, credits, licenses |

## Programs

- MATLAB: `C:\Program Files\MATLAB\R2024a\bin`
- PLECS: `C:\Users\ferre\OneDrive\Documents\Plexim\PLECS 4.8 (64 bit)`

---

← [[catalog.base]] | [[traction-inverter-index]] | [[harness-index]]
