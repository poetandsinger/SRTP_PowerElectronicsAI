# Phase 0 — Skeleton Application (Week 1)

> **Part of:** [[plan index|Plan Index]]  
> **Goal:** Running desktop window with basic layout. No AI yet.

| ID | Task | Deliverable | Verify |
|----|------|-------------|--------|
| P0.1 | Initialize project with `uv` | `pyproject.toml`, `src/`, `tests/` | `uv run python -c "from srtp_ai import __version__"` |
| P0.2 | Main window (PySide6) | Menu bar, status bar, dock widgets | Window launches, resizes, closes |
| P0.3 | Project Explorer (QTreeView) | Folder tree with mock projects | Click items, see selection |
| P0.4 | Topology Designer canvas | QGraphicsView + grid | Zoom, pan, grid visible |
| P0.5 | Results Dashboard placeholder | Tab widget, empty plot areas | Tabs switch, layout stable |
| P0.6 | AI Chat Panel | QTextEdit + QLineEdit | Type message, see echo |
| P0.7 | First tests | 5+ tests passing | `pytest -q` green |
| P0.8 | Git setup | Clean initial commit | `git status` clean |

← [[implementation/plans/tech-stack]] | [[implementation/plans/phase-1-agent]] →
