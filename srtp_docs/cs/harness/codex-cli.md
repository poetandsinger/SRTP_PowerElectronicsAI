---
title: Codex CLI — Architecture Deep Dive
type: topic
field: cs
created: 2026-07-08
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [cs, codex-cli, architecture]
---

## Overview

Codex CLI is OpenAI's **autonomous coding agent** for the terminal. It runs inside git repositories and can autonomously implement features, fix bugs, refactor code, and review PRs. It requires an OpenAI API key or Codex OAuth credentials.

Codex is the **most constrained** of the coding agents — it offers the fewest extension points and is tightly coupled to OpenAI's ecosystem.

## Architecture

```
┌─────────────────────────────────────────────┐
│                CODEX CLI                     │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │           AGENT LOOP                    │ │
│  │  Prompt → OpenAI Model → Tools → Loop  │ │
│  └──────────────────┬─────────────────────┘ │
│                     │                        │
│  ┌──────────────────▼─────────────────────┐ │
│  │            TOOL SYSTEM                  │ │
│  │  file_read │ file_write │ bash │ grep  │ │
│  │  + workspace-write (sandboxed)         │ │
│  └──────────────────┬─────────────────────┘ │
│                     │                        │
│  ┌──────────────────▼─────────────────────┐ │
│  │          SANDBOX LAYER                  │ │
│  │  Default: bubblewrap/namespace isolation│ │
│  │  --yolo: no sandbox (skip)             │ │
│  │  --sandbox danger-full-access: process  │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │           SURFACES                      │ │
│  │  CLI (codex exec) │ Interactive?        │ │
│  └────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Agent Loop

Standard ReAct loop with minimal customization:

1. Takes a natural language prompt
2. Reads relevant files
3. Plans and executes changes
4. Runs tests (if configured)
5. Commits changes (if `--full-auto` or `--yolo`)

### Tool System

**Minimal toolset:** `file_read`, `file_write`, `bash`, `grep` (search)

No custom tool support, no MCP integration, no hooks, no subagents.

### Sandbox Modes

| Mode | Flag | Behavior |
|------|------|----------|
| Default | *(none)* | Sandboxed with bubblewrap; prompts for file writes |
| Full Auto | `--full-auto` | Sandboxed but auto-approves file changes in workspace |
| YOLO | `--yolo` | No sandbox, no approvals; full system access |

**Caveat:** On Hermes gateway/service contexts, bubblewrap often fails due to namespace restrictions. `--sandbox danger-full-access` is the workaround.

### Execution Modes

- **`codex exec "prompt"`** — one-shot execution, exits when done
- **Interactive mode** — TUI (requires pty)

### Git Requirement

Codex **refuses to run outside a git repository**. This is a deliberate safety/accountability measure — all changes are tracked in git.

## Key Features for Research Agent Use

| Feature | Relevance | Available? |
|---------|-----------|------------|
| Multi-agent | Coordinate researcher + simulator | ❌ No |
| Persistent memory | Research context across sessions | ❌ No |
| Scheduled tasks | Periodic simulation runs | ❌ No |
| Tool extensibility | Wrap MATLAB as a tool | ❌ No |
| Provider flexibility | Multiple LLM backends | ❌ OpenAI-only |
| Sandbox | Safe execution environment | ✅ Yes |
| Git tracking | Reproducible research | ✅ Yes |

## Strengths

1. **Simple** — `codex exec "prompt"` is the simplest interface of all agents
2. **Apache 2.0 licensed** — permissive, no restrictions
3. **Sandbox safety** — bubblewrap isolation by default
4. **Git-native** — all changes tracked, easy to review and revert

## Weaknesses

1. **OpenAI-only** — locked to GPT models; can't use Claude, DeepSeek, or open-source models
2. **No extensibility** — can't add custom tools; no hooks, no MCP
3. **No multi-agent** — single agent, single task
4. **No memory** — every session starts fresh
5. **No scheduling** — can't run periodic tasks
6. **Git requirement** — can't run on arbitrary data/research directories without git init
7. **Sandbox failures** — bubblewrap often breaks in containerized/service environments
8. **Minimal features** — compared to Claude Code or Hermes, extremely bare-bones

## Suitability for Power Electronics Research

**Rating: 🔴 Poor**

Codex CLI is the least suitable harness for research. It's a straightforward coding agent with no extension points, no multi-agent support, and no support for non-code tasks. Using it for power electronics research would require:

- Wrapping MATLAB calls entirely in bash scripts (awkward, fragile)
- No way to persist research context across sessions
- No way to schedule periodic simulations
- Locked into OpenAI's ecosystem

**Best use:** None for research orchestration. Could be useful for implementing small, self-contained Python utilities.


> **References:** [[citations]]


← [[cs/harness/claude-code|Prev: Claude Code CLI]] | [[comparative-analysis|Next: Comparative Analysis]] → | [[README]]
