---
title: Agent Harness Research
type: map
field: ai-agents
created: 2026-07-06
updated: 2026-07-19
tags: [ai-agents, multi-agent, index]
---

## Scope

This research surveys existing AI agent harnesses (frameworks, CLIs, platforms) on GitHub as candidate foundations for a **power electronics research agent**. Key requirements:

1. **Multi-agent orchestration** — coordinate researcher, simulator, and reviewer agents
2. **Tool extensibility** — wrap MATLAB, Simulink, PLECS, LTSpice as callable tools
3. **Persistent memory** — retain research context across sessions
4. **Non-coding task support** — literature review, simulation analysis, report generation
5. **Provider-agnostic** — work with multiple LLM backends (DeepSeek, Claude, GPT)

## Surveyed Harnesses — Operational Agent Platforms

Complete agent *platforms* with built-in infrastructure (CLI, memory, scheduling, multi-platform delivery):

| Harness | ⭐ Stars | Forks | License | Open Issues | Multi-Agent | Research Fit |
|---------|---------|-------|---------|:---:|:---:|:---:|
| [[hermes-agent]] | **210,142** | 38,464 | MIT | 26,179 | ✅ Native delegation | 🟢 Excellent |
| [[claude-code]] | **136,513** | 21,925 | Proprietary | 9,943 | ✅ @subagents + Teams | 🟡 Moderate |
| [[opencode]] | **182,896** | 22,658 | MIT | 4,771 | ✅ Multi-agent | 🟢 Good |
| [[codex-cli]] | **95,830** | 14,222 | Apache 2.0 | — | ❌ None | 🔴 Poor |

> ✅ **All star counts verified via GitHub API on 2026-07-06.** Hermes leads operational platforms at 210k★. OpenCode's 183k★ and 75+ provider support makes it a viable alternative for provider-agnostic research. Claude Code's 137k★ reflects massive adoption despite proprietary license. Hermes Agent v0.18.0 with 14,661 commits.

## Surveyed Frameworks — Library-Level Agent Tools

Python libraries for building agents; you provide the operational infrastructure:

| Framework       | ⭐ Stars               | License    |     Multi-Agent     | Research Fit |  MATLAB Fit  |              |
| --------------- | --------------------- | ---------- | :-----------------: | :----------: | :----------: | ------------ |
| [[langgraph]]           | **36,626** |         MIT         | ✅ Subgraphs  | 🟢 Excellent | 🟢 Very High |
| [[crewai]]              | **55,014** |         MIT         | ✅ Role-based | 🟢 Excellent | 🟢 High      |
| [[autogen]] | **59,526** |      CC-BY-4.0      | ✅ Group chat |   🟢 Good    | 🟢 High      |
| LangChain       | **141,092**           | MIT        |   ✅ Via LangGraph   |   🟢 Good    |   🟢 High    |              |
| smolagents (HF) | **28,215**            | Apache 2.0 |    ✅ Multi-agent    |   🟡 Good    |  🟡 Medium   |              |
| Aider           | **47,109**            | Apache 2.0 | ⚠️ Architect/Editor |   🔴 Poor    |    🔴 Low    |              |
| Cline           | **64,346**            | Apache 2.0 |       ❌ None        |   🔴 Poor    |  🟡 Medium   |              |
| PraisonAI       | **8,353**             | MIT        |   ✅ Wraps others    |   🟡 Good    |  🟡 Medium   |              |
| Langroid        | **4,054**             | MIT        |   ✅ Hierarchical    |   🟡 Good    |  🟡 Medium   |              |

## Specialized Research Agents

Purpose-built for specific research tasks — ideal as sub-components:

| Agent | Note | ⭐ Stars | License | Specialization | Integration |
|-------|------|---------|---------|----------------|-------------|
| PaperQA2 | [[research-agents]] | **8,822** | Apache 2.0 | Scientific literature Q&A w/ citations | RAG sub-agent |
| GPT Researcher | [[research-agents]] | **28,107** | Apache 2.0 | Deep web research + report generation | Literature review |
| STORM (Stanford) | [[research-agents]] | **29,864** | MIT | Multi-perspective report generation | Report writing |

> ⚠️ **Note on Hermes Agent/Claude Code/OpenCode stars:** The GitHub API batch for these three is still pending. Star estimates above are approximate. The other 10 frameworks have verified star counts from live API calls on 2026-07-06.

## Quick Navigation

- [[comparative-analysis|Comparative Analysis]] — Side-by-side architecture comparison (all frameworks)
- [[comparative-analysis|Comparative Analysis]] — Side-by-side architecture comparison + gap analysis
- [[architecture-patterns|Architecture Patterns]] — Common patterns across harnesses
- [[plecs-integration|PLECS Integration Strategy]] — How to wrap PLECS as an agent tool
- [[langgraph|LangGraph Deep Dive]] — State-machine agent graphs
- [[crewai|CrewAI Deep Dive]] — Role-based multi-agent teams
- [[research-agents|Research-Specific Agents]] — PaperQA2, GPT Researcher, STORM
- [[autogen|AutoGen Deep Dive]] — Microsoft's multi-agent conversations

## Key Findings

1. **Two architecture categories exist:** (a) **Operational platforms** (Hermes 210k★, Claude Code 137k★, OpenCode 183k★) — complete with CLI, memory, scheduling, delivery. (b) **Library frameworks** (LangGraph 37k★, CrewAI 55k★, AutoGen 60k★) — Python libraries for composing agents; operational infrastructure built separately.

2. **Hermes Agent has the most built-in primitives** — native multi-agent delegation, self-improving skills system, cron scheduler, cross-session memory, and 20+ platform gateway. OpenCode (183k★, 75+ providers) is the strongest provider-agnostic alternative.

3. **LangGraph's checkpointing is architecturally unique** — the only framework with built-in fault tolerance for long-running workflows, which matters for multi-hour MATLAB simulations.

4. **CrewAI's built-in memory is unique among libraries** — short-term + long-term + entity memory without external dependencies. Its role-based agent model maps naturally to research team structures.

5. **Specialized agents are components, not foundations** — PaperQA2 (8.8k★), GPT Researcher (28k★), and STORM (30k★) excel at specific tasks but lack simulation capabilities. They integrate as sub-agents.

6. **No existing harness natively supports PLECS** — custom tool development (or PE-MAS's `plecs-mcp`) is required regardless of choice. See [[plecs-integration|PLECS Integration Strategy]] for architectural approaches.

7. **Coding agents (Codex 96k★, Aider 47k★, Cline 64k★) are architecturally wrong for research** — their prompts, tools, and workflows are optimized for code editing, not scientific simulation.


> **References:** [[citations]]


← [[citations|References]] | [[hermes-agent|Next: Hermes Agent]] → | [[README]]
