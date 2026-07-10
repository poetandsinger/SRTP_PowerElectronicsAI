# Phase 1 — Agent Engine (Weeks 2-3)

> **Part of:** [[plan index|Plan Index]]  
> **Goal:** Embedded agent using smolagents + MATLAB tools + memory + skills.

| ID | Task | Deliverable | Verify |
|----|------|-------------|--------|
| P1.1 | Install smolagents, configure LLMs | `CodeAgent` with DeepSeek + Claude | Agent responds to "What is a buck converter?" |
| P1.2 | Register MATLAB tools (`@tool`) | `matlab_simulate`, `matlab_sweep` | Agent calls `matlab_simulate(...)` |
| P1.3 | MemoryStore (SQLite+FTS5) | `save()`, `search()`, `get_all()` | Save fact, retrieve across sessions |
| P1.4 | SkillsManager | Skills in `~/.srtp-ai/skills/` | Create skill, load into agent |
| P1.5 | HooksSystem (PreToolUse, PostToolUse, Stop) | 5 hook types | PostToolUse validates MATLAB output |
| P1.6 | Wire Agent + GUI chat | smolagents → chat panel | Interactive AI chat in GUI |

← [[implementation/plans/phase-0-skeleton]] | [[implementation/plans/phase-2-matlab]] →
