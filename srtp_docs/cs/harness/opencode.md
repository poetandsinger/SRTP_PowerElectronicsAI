---
title: OpenCode CLI — Architecture Deep Dive
type: topic
field: cs
created: 2026-07-06
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [cs, opencode, architecture]
---

## Overview

OpenCode is a **provider-agnostic, open-source AI coding agent** with a terminal UI (TUI) and CLI. It's designed for autonomous code generation, refactoring, and review within git repositories. Unlike Hermes Agent (general-purpose agent platform), OpenCode focuses specifically on the **coding agent** use case.

OpenCode ships with two built-in agent profiles (`build` for implementation, `plan` for architecture) and supports any LLM provider via OpenRouter or direct API keys.

## Architecture

```
┌─────────────────────────────────────────────┐
│               OPENCODE CLI                   │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐ │
│  │  Build   │  │  Plan    │  │  Custom   │ │
│  │  Agent   │  │  Agent   │  │  Agents   │ │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘ │
│       │              │              │        │
│  ┌────▼──────────────▼──────────────▼─────┐ │
│  │           AGENT LOOP                    │ │
│  │  Prompt → LLM → Tool calls → Repeat    │ │
│  └──────────────────┬────────────────────┘ │
│                     │                       │
│  ┌──────────────────▼────────────────────┐ │
│  │            TOOL SYSTEM                 │ │
│  │  Read │ Write │ Edit │ Bash │ Search  │ │
│  └──────────────────┬────────────────────┘ │
│                     │                       │
│  ┌──────────────────▼────────────────────┐ │
│  │          PROVIDER LAYER                │ │
│  │  OpenRouter │ Anthropic │ OpenAI │ …   │ │
│  └───────────────────────────────────────┘ │
│                                              │
│  ┌───────────────────────────────────────┐ │
│  │         SURFACES                       │ │
│  │  CLI (opencode run) │ TUI (opencode)  │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Agent Modes

- **`build` agent:** Implementation-focused — writes code, runs tests, makes commits
- **`plan` agent:** Architecture-focused — plans before implementing, asks clarifying questions
- **Custom agents:** User-defined via configuration

Agents can be switched mid-session with `Tab` key in the TUI.

### Tool System

Limited to coding-relevant tools:
- **Read:** File reading
- **Write:** File creation
- **Edit:** Targeted file edits
- **Bash:** Shell command execution
- **Search:** Codebase search (grep, find)
- **Web:** Web search and fetch (some configurations)

No skills system, no persistent memory, no cron scheduler, no delegation.

### Provider Model

- **OpenRouter-first:** Primary integration path; supports 200+ models
- **Direct API keys:** Anthropic, OpenAI, Google, DeepSeek, xAI, etc.
- **OpenCode Zen/Go:** First-party API services for managed inference
- **Per-session model switching:** Change model mid-conversation with `Ctrl+X M`

### Session Management

- **Named sessions:** `opencode -s <session_id>` to resume
- **Session listing:** `opencode session list`
- **Cost tracking:** `opencode stats` with per-model breakdowns
- **No cross-session memory:** Each session is independent; no persistent state

## Key Features for Research Agent Use

| Feature | Relevance | Available? |
|---------|-----------|------------|
| Multi-agent | Coordinate researcher + simulator | ❌ No native support |
| Persistent memory | Retain research context across sessions | ❌ No |
| Scheduled tasks | Periodic simulation runs | ❌ No |
| Tool extensibility | Wrap MATLAB as a tool | ⚠️ Limited (Bash-only) |
| Provider-agnostic | Use multiple LLM backends | ✅ Yes |
| Session management | Resume long research sessions | ✅ Yes |
| Non-coding tasks | Literature review, report generation | ⚠️ Possible but not designed for |

## Strengths

1. **Excellent coding agent** — fast, focused, great for software implementation
2. **Provider-agnostic** — works with any LLM via OpenRouter
3. **MIT licensed** — open-source, no restrictions
4. **Clean CLI** — `opencode run "prompt"` is simple and effective
5. **Session resumption** — can continue long-running tasks across restarts
6. **Built-in PR review** — `opencode pr <number>` command

## Weaknesses

1. **Coding-only focus** — no support for non-code research tasks
2. **No persistent memory** — every session starts fresh
3. **No scheduling** — can't run periodic simulations or scans
4. **No tool extensibility** — can't easily add MATLAB/Simulink as first-class tools
5. **No multi-agent orchestration** — one agent, one task at a time
6. **No gateway** — terminal-only; can't receive results on phone

## Suitability for Power Electronics Research

**Rating: 🟡 Moderate (for code tasks only)**

OpenCode could be useful as a **sub-component** — specifically for implementing the MATLAB-Python bridge code, writing simulation scripts, or generating report templates. But as the primary agent harness for a research system, it lacks too many critical features:

- No way to schedule recurring simulations
- No persistent memory for research context
- No multi-agent coordination
- Can't easily wrap MATLAB as a first-class tool (would need to use Bash + `matlab -batch`)

**Best use:** Delegate software implementation tasks to OpenCode while the main research orchestration happens in a more capable harness.


> **References:** [[citations]]


← [[cs/harness/hermes-agent|Prev: Hermes Agent]] | [[cs/harness/claude-code|Next: Claude Code CLI]] → | [[README]]
