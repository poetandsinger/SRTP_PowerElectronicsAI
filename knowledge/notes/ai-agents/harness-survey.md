---
title: "Agent Harness Survey — Frameworks & Findings"
type: topic
field: ai-agents
created: 2026-07-20
updated: 2026-07-20
status: unverified
evidence: single-study
sources: [citations]
tags: [ai-agents, multi-agent, review, comparison, sota]
review_by: 2026-10-20
---

> **Survey content**, separated from [[harness-index]] on 2026-07-20 so the index stays pure wayfinding. The per-harness deep-dives are the `harness-*` notes ([[harness-index]] lists them); this note holds the cross-harness survey tables and findings. Star counts are point-in-time (GitHub API, 2026-07-06) and drift.

## Scope

Surveys AI-agent harnesses (frameworks, CLIs, platforms) as candidate foundations for a **power-electronics research agent**. Requirements: (1) multi-agent orchestration (researcher / simulator / reviewer), (2) tool extensibility (wrap MATLAB, Simulink, PLECS, LTspice), (3) persistent memory across sessions, (4) non-coding task support (literature review, sim analysis, reporting), (5) provider-agnostic (DeepSeek, Claude, GPT).

## Operational Agent Platforms

Complete platforms with built-in infrastructure (CLI, memory, scheduling, delivery):

| Harness | ⭐ Stars | Forks | License | Open Issues | Multi-Agent | Research Fit |
|---------|---------|-------|---------|:---:|:---:|:---:|
| [[harness-hermes-agent]] | 210,142 | 38,464 | MIT | 26,179 | ✅ Native delegation | 🟢 Excellent |
| [[harness-claude-code]] | 136,513 | 21,925 | Proprietary | 9,943 | ✅ @subagents + Teams | 🟡 Moderate |
| [[harness-opencode]] | 182,896 | 22,658 | MIT | 4,771 | ✅ Multi-agent | 🟢 Good |
| [[harness-codex-cli]] | 95,830 | 14,222 | Apache 2.0 | — | ❌ None | 🔴 Poor |

> Star counts verified via GitHub API 2026-07-06. Hermes leads operational platforms at 210k★; OpenCode's 183k★ + 75+ providers make it the strongest provider-agnostic alternative; Claude Code 137k★ despite proprietary license. Hermes Agent v0.18.0, 14,661 commits.

## Library-Level Agent Frameworks

Python libraries; you provide the operational infrastructure:

| Framework | ⭐ Stars | License | Multi-Agent | Research Fit | MATLAB Fit |
| --------- | ------- | ------- | :---------: | :----------: | :--------: |
| [[harness-langgraph]] | 36,626 | MIT | ✅ Subgraphs | 🟢 Excellent | 🟢 Very High |
| [[harness-crewai]] | 55,014 | MIT | ✅ Role-based | 🟢 Excellent | 🟢 High |
| [[harness-autogen]] | 59,526 | CC-BY-4.0 | ✅ Group chat | 🟢 Good | 🟢 High |
| LangChain | 141,092 | MIT | ✅ Via LangGraph | 🟢 Good | 🟢 High |
| smolagents (HF) | 28,215 | Apache 2.0 | ✅ Multi-agent | 🟡 Good | 🟡 Medium |
| Aider | 47,109 | Apache 2.0 | ⚠️ Architect/Editor | 🔴 Poor | 🔴 Low |
| Cline | 64,346 | Apache 2.0 | ❌ None | 🔴 Poor | 🟡 Medium |
| PraisonAI | 8,353 | MIT | ✅ Wraps others | 🟡 Good | 🟡 Medium |
| Langroid | 4,054 | MIT | ✅ Hierarchical | 🟡 Good | 🟡 Medium |

## Specialized Research Agents

Purpose-built for specific research tasks — ideal as sub-components (all detailed in [[harness-research-agents]]):

| Agent | ⭐ Stars | License | Specialization | Integration |
|-------|---------|---------|----------------|-------------|
| PaperQA2 | 8,822 | Apache 2.0 | Scientific literature Q&A w/ citations | RAG sub-agent |
| GPT Researcher | 28,107 | Apache 2.0 | Deep web research + report generation | Literature review |
| STORM (Stanford) | 29,864 | MIT | Multi-perspective report generation | Report writing |

## Key Findings

1. **Two architecture categories:** (a) operational platforms (Hermes 210k★, Claude Code 137k★, OpenCode 183k★) — complete with CLI, memory, scheduling, delivery; (b) library frameworks (LangGraph 37k★, CrewAI 55k★, AutoGen 60k★) — compose agents, operational infra built separately.
2. **Hermes Agent has the most built-in primitives** — native delegation, self-improving skills, cron, cross-session memory, 20+ platform gateway. OpenCode (183k★, 75+ providers) is the strongest provider-agnostic alternative.
3. **LangGraph's checkpointing is architecturally unique** — the only framework with built-in fault tolerance for long-running workflows (matters for multi-hour simulations).
4. **CrewAI's built-in memory is unique among libraries** — short-term + long-term + entity memory, no external deps; role-based model maps to research teams.
5. **Specialized agents are components, not foundations** — PaperQA2, GPT Researcher, STORM excel at tasks but lack simulation; integrate as sub-agents.
6. **No existing harness natively supports PLECS** — custom tool dev (or PE-MAS's `plecs-mcp`) required regardless. See [[plecs-integration]].
7. **Coding agents (Codex, Aider, Cline) are architecturally wrong for research** — optimized for code editing, not scientific simulation.

## Red Team

**Steelman against:** star counts are popularity, not fitness, and drift monthly; the "research fit" ratings are subjective; a fast-moving field dates any snapshot within months.
**How it could be false:** selection bias toward GitHub-popular tools; some star batches were pending at capture (Hermes/Claude Code/OpenCode flagged); ratings not from head-to-head trials.
**What would change my mind:** an actual build on two shortlisted harnesses with the PLECS toolchain, comparing orchestration/memory/tool-wrapping effort head-to-head.
**Residual doubt:** the category split (platforms vs libraries) and "no native PLECS support" are robust; the specific star numbers and fit grades are soft.

> **References:** [[citations]]

← [[harness-index]] | [[harness-comparison]] | [[README]]
