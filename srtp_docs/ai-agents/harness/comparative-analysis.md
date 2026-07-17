---
title: Comparative Analysis — Agent Harnesses
type: topic
field: ai-agents
created: 2026-07-06
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [ai-agents, comparison, benchmark, review]
---

## Executive Summary

**Two categories of harness exist:**

### Operational Platforms (Complete Systems)
**Hermes Agent** — the only platform with all primitives: multi-agent delegation, persistent memory, self-improving skills, cron scheduling, multi-platform gateway, provider flexibility, and extensible tools. MIT licensed.

### Library Frameworks (Build Your Own Infrastructure)
**LangGraph** — state-machine architecture maps cleanly to research workflows (plan→simulate→analyze→replan). Built-in checkpointing for fault-tolerant long simulations. Human-in-the-loop for expert review. MIT licensed.

**CrewAI** — role-based multi-agent teams with built-in memory. Natural mapping to research lab structure: Researcher, Simulation Engineer, Data Analyst, Report Writer.

Claude Code and OpenCode are excellent coding agents but lack the operational infrastructure that research workflows demand. Coding-only agents (Codex CLI, Aider, Cline) are architecturally designed for code editing, not scientific simulation workflows.

## Feature Matrix — Operational Platforms

| Feature | [[ai-agents/harness/hermes-agent]] | [[ai-agents/harness/claude-code]] | [[ai-agents/harness/opencode]] | [[ai-agents/harness/codex-cli]] |
|---------|:---:|:---:|:---:|:---:|
| **License** | MIT | Proprietary | MIT | Apache 2.0 |
| **Language** | Python | Python | TypeScript | Rust |
| **Provider Model** | 20+ providers | Claude only | 75+ providers | OpenAI only |
| **Multi-Agent** | ✅ Native delegation | ✅ @subagents + Teams | ✅ Multi-agent | ❌ None |
| **Persistent Memory** | ✅ Cross-session | ⚠️ CLAUDE.md only | ❌ None | ❌ None |
| **Scheduled Tasks** | ✅ Cron scheduler | ❌ None | ❌ None | ❌ None |
| **Tool Extensibility** | ✅ Plugins + MCP | ✅ MCP + Hooks | ✅ MCP/ACP | ❌ None |
| **Hooks System** | ❌ None | ✅ 8 hook types | ❌ None | ❌ None |
| **Skills/Self-Improving** | ✅ Native skills | ✅ Skills | ✅ Agent Skills | ❌ None |
| **Multi-Platform Delivery** | ✅ 20+ platforms | ❌ Terminal only | ❌ Terminal only | ❌ Terminal only |
| **Structured Output** | ❌ JSON only | ✅ json-schema | ❌ None | ❌ None |
| **Desktop App** | ✅ Electron | ❌ CLI only | ✅ Desktop (beta) | ❌ CLI only |
| **IDE Integration** | ✅ ACP server | ❌ CLI only | ✅ IDE extensions | ❌ CLI only |
| **Open Source** | ✅ Full | ❌ Proprietary | ✅ Full | ✅ Full |

## Feature Matrix — Library Frameworks

These are Python libraries — operational infrastructure (CLI, scheduling, delivery, persistence) must be built separately.

| Feature | [[ai-agents/harness/langgraph]] | [[ai-agents/harness/crewai]] | [[ai-agents/harness/autogen]] | LangChain |
|---------|:---:|:---:|:---:|:---:|
| **License** | MIT | MIT | CC-BY-4.0 | MIT |
| **Architecture** | State machine graphs | Role-based crews | Conversation groups | Chain/tool abstraction |
| **Multi-Agent** | ✅ Subgraphs | ✅ Role-based | ✅ Group chat | ✅ Via LangGraph |
| **Checkpointing** | ✅ Built-in | ❌ None | ❌ None | ❌ None |
| **Human-in-Loop** | ✅ Interrupts | ✅ Review steps | ✅ UserProxyAgent | ⚠️ Manual |
| **Built-in Memory** | ❌ (via LangChain) | ✅ Short/long/entity | ❌ | ✅ Buffer/summary |
| **Streaming** | ✅ Node-level | ⚠️ Final only | ⚠️ Final only | ✅ Via LangGraph |
| **MATLAB Fit** | 🟢 Very High | 🟢 High | 🟢 High | 🟢 High |
| **Research Fit** | 🟢 Excellent | 🟢 Excellent | 🟢 Good | 🟢 Good |

## Architecture Comparison

### Agent Loop

All use a **ReAct (Reasoning + Acting) loop**: prompt → LLM → tool calls → results → repeat.

| Harness | Loop Enhancements |
|---------|-------------------|
| [[ai-agents/harness/hermes-agent]] | Context compression, prompt caching, checkpoint/rollback, multi-profile |
| [[ai-agents/harness/claude-code]] | Context compaction, `/rewind` checkpoints, visual context grid |
| [[ai-agents/harness/opencode]] | Agent mode switching (build ↔ plan), model switching mid-session |
| [[ai-agents/harness/codex-cli]] | Minimal — just prompt, run, exit |

### Tool System

| Harness | Tool Count | Extensibility | Permission Model |
|---------|-----------|---------------|-----------------|
| [[ai-agents/harness/hermes-agent]] | 30+ toolsets | Plugins, MCP, custom Python | Toolset per-platform, approval prompts |
| [[ai-agents/harness/claude-code]] | ~6 + MCP | MCP, hooks, custom commands | allow/ask/deny patterns, hook gates |
| [[ai-agents/harness/opencode]] | Built-in | MCP/ACP | Trust-based |
| [[ai-agents/harness/codex-cli]] | ~4 built-in | None | Sandbox-based (bubblewrap) |

### Memory & Context

| Harness | Cross-Session | Project Context | Self-Improving |
|---------|:---:|:---:|:---:|
| [[ai-agents/harness/hermes-agent]] | ✅ Durable memory store | .hermes.md, AGENTS.md | ✅ Skills accumulate |
| [[ai-agents/harness/claude-code]] | ⚠️ Auto-memory (25KB) | CLAUDE.md hierarchy | ❌ |
| [[ai-agents/harness/opencode]] | ❌ | .opencode/rules/ | ❌ |
| [[ai-agents/harness/codex-cli]] | ❌ | None | ❌ |

### Multi-Agent Support

| Harness | Mechanism | Depth | Concurrent |
|---------|-----------|-------|:---:|
| [[ai-agents/harness/hermes-agent]] | `delegate_task` | Configurable depth | Up to 3 parallel |
| [[ai-agents/harness/claude-code]] | @agent + Agent Teams | Multi-session with P2P | Via tmux worktrees |
| [[ai-agents/harness/opencode]] | Multi-agent | Flat | Built-in |
| [[ai-agents/harness/codex-cli]] | None | — | Manual parallel CLI |

### Scheduling & Automation

| Harness | Cron | Hooks | Webhooks |
|---------|:---:|:---:|:---:|
| [[ai-agents/harness/hermes-agent]] | ✅ Full cron scheduler | ❌ | ✅ Webhook triggers |
| [[ai-agents/harness/claude-code]] | ❌ | ✅ 8 event hooks | ❌ |
| [[ai-agents/harness/opencode]] | ❌ | ❌ | ❌ |
| [[ai-agents/harness/codex-cli]] | ❌ | ❌ | ❌ |

## Research-Specific Comparison

### Power Electronics Research Workflow Requirements

```
1. Literature Review → 2. Topology Selection → 3. Component Sizing 
→ 4. MATLAB/Simulink Simulation → 5. Results Analysis → 6. Report Generation
→ 7. (Loop back with refined parameters)
```

| Requirement | [[ai-agents/harness/hermes-agent]] | [[ai-agents/harness/claude-code]] | [[ai-agents/harness/langgraph]] | [[ai-agents/harness/crewai]] |
|-------------|:---:|:---:|:---:|:---:|
| Read papers from arXiv | ✅ Web + Skills | ✅ WebSearch | ✅ LangChain tools | ✅ Agent tools |
| Store paper summaries | ✅ Memory | ⚠️ CLAUDE.md | ⚠️ External DB needed | ✅ Entity memory |
| Run MATLAB simulation | ✅ Custom tool | ✅ MCP server | ✅ Graph node tool | ✅ Agent tool |
| Parse simulation results | ✅ Python tool | ✅ JSON schema | ✅ Python node | ✅ Agent tool |
| Compare against baselines | ✅ Memory recall | ⚠️ CLAUDE.md | ✅ State persistence | ✅ Memory |
| Schedule daily sim runs | ✅ Cron | ❌ | ❌ | ❌ |
| Send results to phone | ✅ Gateway | ❌ | ❌ | ❌ |
| Iterate with new params | ✅ Skills + Memory | ⚠️ New prompt | ✅ Cyclic graph | ✅ Task loops |
| Generate IEEE report | ✅ All tools | ✅ Write tool | ✅ Agent output | ✅ Agent output |
| Fault-tolerant long runs | ⚠️ Session-based | ⚠️ Process-based | ✅ Checkpointing | ❌ |

## Research-Specific Gap Analysis

No existing harness provides these capabilities natively — they must be custom-built regardless of harness choice:

1. **MATLAB/Simulink tool integration** — No harness ships with MATLAB tools
2. **Power electronics domain knowledge** — No harness has built-in PE expertise
3. **Simulation result validation** — No harness validates simulation output semantics
4. **Component library integration** — No harness connects to component databases
5. **IEEE-format report generation** — No harness generates IEEE-formatted technical papers

## Architecture Selection Considerations

Key trade-offs from the analysis:

- **Build vs. Buy:** Operational platforms (Hermes, Claude Code, OpenCode) provide infrastructure out of the box. Library frameworks (LangGraph, CrewAI) require building operational layers but offer more workflow flexibility.
- **Fault tolerance:** Only LangGraph provides built-in checkpointing for long-running workflows. This matters for multi-hour MATLAB simulations that may fail mid-run.
- **Provider lock-in:** Claude Code is Claude-only. Codex is OpenAI-only. Hermes, OpenCode, LangGraph, and CrewAI are provider-agnostic.
- **Memory persistence:** Only Hermes Agent and CrewAI provide cross-session memory as a built-in primitive. Others require external persistence.
- **Self-improvement:** Hermes, Claude Code, and OpenCode all have skills systems that accumulate knowledge over time. Library frameworks require manual knowledge management.

See [[architecture-patterns]] for extracted reusable patterns across all harnesses.

## Radar Chart Summary

Qualitative strength per dimension (● strong · ◐ medium · ○ weak). Rendered as a matrix rather than a mermaid radar chart, which is not reliably supported in Obsidian.

| Harness | Multi-Agent | Memory & Persistence | Provider Flexibility | Scheduling | Tool Extensibility |
|---------|:-----------:|:--------------------:|:--------------------:|:----------:|:------------------:|
| **Hermes Agent** | ◐ | ● | ● | ● | ● |
| **Claude Code** | ● | ○ | ○ | ○ | ● |
| **OpenCode** | ◐ | ○ | ● | ○ | ◐ |
| **Codex CLI** | ○ | ○ | ○ | ○ | ◐ |


> **References:** [[citations]]


← [[ai-agents/harness/codex-cli]] | [[architecture-patterns]] → | [[README]]
