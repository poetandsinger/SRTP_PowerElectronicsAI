---
title: 2026-07-06 — Subagent Findings Integrated
type: changelog
field: project
created: 2026-07-06
updated: 2026-07-06
tags: [changelog]
---

# 2026-07-06 — Subagent Findings Integrated

> **Part of:** [[changelog-index]]

## Key Changes
1. **Agent engine:** smolagents (Apache 2.0) as library dependency — not custom-built
2. **Reference GUI:** PulsimGUI (MIT) discovered — same PySide6 stack, same PE domain
3. **GUI framework confirmed:** PySide6 is industry standard (PLECS, Qucs-S, OpenModelica all use Qt)
4. **NiceGUI** ranked #1 for AI chat/dashboard panels

## New Stack
```
GUI:     PySide6 + NiceGUI (chat)
Agent:   smolagents (Apache 2.0)
Workflow: LangGraph (MIT)
MATLAB:   Engine API (external)
Papers:   PaperQA2 (Apache 2.0)
Reports:  STORM (MIT)
Ref:      PulsimGUI (MIT)
```

← [[changelog-index]]
