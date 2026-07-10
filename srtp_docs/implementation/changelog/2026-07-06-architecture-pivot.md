# 2026-07-06 — Architecture Pivot

> **Part of:** [[changelog index]]

## Change
Architecture completely revised from "build on Hermes Agent CLI" to "standalone desktop GUI application."

## Why
User requirements: GUI interface, standalone (not CLI agent harness), MATLAB external only.

## New Architecture
- GUI: PySide6 (Qt) + NiceGUI (chat panel)
- Agent: smolagents (Apache 2.0) — embedded, not CLI
- MATLAB: Engine API — external, not embedded
- Workflow: LangGraph (MIT) for checkpointing

## Open Source Reuse
- smolagents (Apache 2.0): Agent engine
- LangGraph (MIT): Workflow checkpointing
- PaperQA2 (Apache 2.0): Literature RAG
- STORM (MIT): Report generation
- Hermes Agent (MIT): Memory, skills patterns
- PulsimGUI (MIT): Reference architecture
- Claude Code: Ideas only (hooks, permissions)

← [[changelog index]]
