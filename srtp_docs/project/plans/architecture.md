---
title: Architecture Decision
type: plan
field: project
created: 2026-07-06
updated: 2026-07-10
tags: [plan, architecture]
---

# Architecture Decision

> **Part of:** [[plans-index|Plan Index]]
> **⚠️ Pre-2026-07-10.** See [[plans-index|updated plans-index]] and [[ai-agents/implementation-research]] for current architecture decisions.

## Why Standalone

| Factor | Hermes Agent | Standalone |
|--------|:---:|:---:|
| GUI | CLI/TUI only | Full Qt desktop GUI |
| Target user | Developers | Power electronics engineers |
| Distribution | Python package | Single .exe |
| MATLAB | Custom Hermes tool | Direct Engine API |

## Open Source Reuse

| Source | License | What | How |
|--------|---------|------|-----|
| smolagents (HF) | Apache 2.0 | Agent engine | Library dependency |
| [[../../research/harness/langgraph]] | MIT | State machine + checkpointing | Library dependency |
| PulsimGUI | MIT | PE desktop GUI | Study reference |
| [[../../research/harness/hermes-agent]] | MIT | Memory, skills patterns | Study patterns |
| [[../../research/harness/research-agents]] | Apache 2.0 | PaperQA2 (literature) | Library dependency |
| [[../../research/harness/research-agents]] | MIT | STORM (reports) | Library dependency |
| [[../../research/harness/claude-code]] | Proprietary | Ideas: hooks, permissions | Implement own |

## Closed Source Ideas (No Code)

| Source | Pattern |
|--------|---------|
| PLECS | Dock-based GUI, simulation toolbar |
| Synopsys DSO.ai | RL simulation loop |
| Cadence Cerebrus | Pareto frontier visualization |
| LTspice | Netlist generation from schematic |

## Key Principles

1. MATLAB is external — called via Engine API
2. GUI-first — no terminal required
3. Agent engine embedded — smolagents runs in-app
4. Open source reuse with credit

← [[plans-index|Plan Index]] | [[project/plans/tech-stack]] →
