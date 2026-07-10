# Technology Stack

> **Part of:** [[plan index|Plan Index]]  

| Component | Technology | License | Why |
|-----------|-----------|---------|-----|
| **GUI** | PySide6 + NiceGUI (chat) | LGPLv3 / MIT | QGraphicsView for schematics, Python-only chat panel |
| **Plots** | pyqtgraph + matplotlib | MIT / PSF | 60 FPS waveforms + IEEE-quality plots |
| **Agent Engine** | smolagents (HF) | Apache 2.0 | ~1k lines, code-first, writes MATLAB-invoking Python |
| **Workflow** | LangGraph | MIT | Checkpointing for fault-tolerant long simulations |
| **LLM (reasoning)** | DeepSeek API | — | Cost-effective, validated |
| **LLM (code gen)** | Claude API (Kimi) | — | Best for MATLAB script generation |
| **MATLAB** | Engine API for Python | MathWorks | External, not embedded |
| **Literature** | PaperQA2 | Apache 2.0 | Citation-grounded RAG |
| **Reports** | STORM | MIT | Multi-perspective generation |
| **Memory** | SQLite (built-in) | Public Domain | Agent memory, results, project state |
| **Reference** | PulsimGUI | MIT | Same framework, same domain |
| **Packaging** | PyInstaller | GPL bootloader | Single .exe |

## LLM Provider Strategy

| Provider | Use Case | Why |
|----------|----------|-----|
| DeepSeek | Reasoning, analysis, planning | Cheap, good at structured thinking |
| Claude (Kimi) | MATLAB code generation, report writing | Best code quality |

← [[architecture|Architecture]] | [[implementation/plans/phase-0-skeleton]] →
