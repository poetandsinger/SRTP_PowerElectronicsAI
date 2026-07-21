---
title: README
type: map
field: root
created: 2026-07-06
updated: 2026-07-20
tags: [index]
---

> **Knowledge-base (research vault) index.** The repo-root index is [../README.md](../README.md); the rules every file obeys are in [SCHEMA.md](SCHEMA.md). Reorganized 2026-07-20: this vault lives under `knowledge/`; `plans/`·`trials/`·`log/` are folded into `synthesis/`; the retired `.base` dataview indexes sit in `_archive/`.

# SRTP Power Electronics AI — Research Vault

> **AI-powered multi-agent system for traction inverter design.**
> **Architecture:** LangGraph + **PLECS** (XML-RPC/MCP) + LiteLLM (CLI-first, provider-agnostic).
> **Method:** Science Research Vault — every claim carries truth-status, evidence-strength, and a mandatory red-team block ([[SCHEMA]]).
> **Status:** 🟡 Knowledge base built (cited [1]–[170]) + agent-architecture research complete; MAS plan is spec-level ([[plan-ai-agent-mas]]). PLECS harness proven (ToFile→CSV readback, `system/src/`); a purpose-fit 2L-B6 CAB450 bench runs headless with confirmed heat-sink coupling and a first η ≈ 99.1 % (`experiments/2l-b6-800v-sic-bench/`). **Next: junction-temp readout + the 9-corner matrix → first PLECS-validated 2L-B6.**

## What This Vault Is

Two research fields feeding one build. **Power electronics** defines *what* to design (traction inverters); **AI agents** defines *how* to build the system that designs them. Every folder name is plain English, every file carries frontmatter, every research claim is red-teamed.

## Structure (`knowledge/`)

Folder = lifecycle stage; `field` lives in frontmatter and one shallow subfolder. Wikilinks are bare basenames, so files move without breaking links. Full rules: [SCHEMA.md](SCHEMA.md) §Folder = Stage.

```
knowledge/
├── README.md  SCHEMA.md  citations.md      # vault index, rules, bibliography
├── sources/<field>/                        # raw capture — one per source, never edited
│   ├── power-electronics/   ai-agents/
├── notes/<field>/                          # digested: claims · topics · maps
│   ├── power-electronics/                  #   traction-inverter build manual + market-and-industry
│   ├── ai-agents/                          #   harness deep-dives, surveys, workflow patterns
│   └── problem-statement/                  #   preface: why AI for inverter design
├── synthesis/                              # cross-cutting synthesis + open questions
│   ├── plans/                              #   MAS implementation specs (plan-ai-agent-mas hub)
│   ├── trials/                             #   worked design-by-doing examples
│   └── log/{changelog,audits}/             #   dated records + self-audits (narrative → root LOG.md)
├── papers/                                 # raw source PDFs (read-only) — currently empty
└── _archive/                               # retired .base dataview indexes
```

> Runnable artifacts live **outside** the vault: `experiments/<design>/` (numpy loss models + `.plecs`), `system/src/` (the PLECS harness), `system/env/models/` (Wolfspeed library), `results/metrics/` (run outputs).

## Navigating

- **Relationships / "what connects to what" →** graphify (whole repo): `graphify query "…"`, `graphify path "A" "B"`, or open `graphify-out/graph.html`. See [SCHEMA.md](SCHEMA.md) §Navigating the repo.
- **Precise filter →** ripgrep on frontmatter: `rg -l "^type: X" knowledge/`, then pick by descriptive filename.
- **Curated entry points (hubs):**

| Field | Hub | Content |
|-------|-----|---------|
| Power Electronics | [[index-traction-inverter]] | Traction-inverter build manual: topologies, devices, machine/control, 4 topology-unit designs, procedures + PLECS SOP, subsystem chapters |
| Reference designs | [[index-reference-designs]] | 4 topology units + 3 external refs (Wolfspeed/TI, Tesla, Nissan Leaf) |
| Industry / market | [[market-and-industry]] | Production topologies, device adoption, suppliers, 2025–26 market data |
| Problem statement | [[problem-statement-index]] | Why AI for traction inverter design: market, workforce |
| AI / Agent Architecture | [[harness-index]] | Harness deep-dives + [[harness-survey]] (frameworks, findings) |

> **Grounded but not yet PLECS-validated:** design/thermal/loss numbers are closed-form or teardown/vendor figures, flagged in each Red Team. Turning them into simulation-backed evidence is the top task — governed by the PLECS validation SOP ([[procedure-simulation-and-validation]] §4, S1–S7) and a serial 4-topology build program ([[plan-depth-research]]: 2L-B6 → TNPC → ANPC → NPC).

## Implementation

**The plan:** [[plan-ai-agent-mas]] (hub) — PLECS-backed MAS, 3-agent core (Planner + Designer + Validator, Orchestrator drives), RAG-first, evidence-gated. Subsystem specs: [[plan-architecture]] · [[plan-design-loop]] · [[plan-knowledge-rag]] · [[plan-plecs-harness]] · [[plan-guardrails-and-evidence]] · [[plan-memory]] · [[plan-tech-stack]] · [[plan-evaluation-and-benchmark]]. Core mechanism: a **topology → refine → parameter-optimize** loop with an *explicit numerical optimizer* over PLECS (LLM picks structure, optimizer picks numbers).

### Key architecture decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| A1 | **CLI-first** (not GUI) | Remove UI complexity from the critical path; prove the agent works first. |
| A2 | **3 agents** (not 7) | Orchestrator + Simulation + Reviewer — minimal decomposition for the A/B test. |
| A3 | **PLECS backend** (not MATLAB) | System-level PE sim with native PMSM/IM + FOC, scriptable via XML-RPC/MCP. (2026-07 pivot off MATLAB.) |
| A4 | **SQLite** (not Postgres) | LangGraph checkpointer works with SQLite; zero setup. |
| A5 | **LiteLLM provider-agnostic** | Route to the cheapest capable model per task. |
| A6 | **Explicit optimizer** | Every 2026 PE/analog design agent converges via a numerical optimizer (DE/PSO/BO), not LLM re-guessing. PLECS-only evidence. See [[plan-design-loop]]. |

## Conventions

Full rules in [SCHEMA.md](SCHEMA.md). In brief: folder = stage; links are bare basenames (globally unique); every file has frontmatter (the index); every claim has a red-team block; truth-status (`supported`/`contested`/`refuted`/`unverified`, default `unverified`) + evidence-strength on every claim; append-first, contradictions surface (never overwrite). After any add/move/rename, rebuild the graph (`/graphify . --update`).

---

← repo root [../README.md](../README.md) | [[SCHEMA]] | [[index-traction-inverter]] | [[harness-index]] | [[citations]]
