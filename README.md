# SRTP Power Electronics AI

> **AI-powered multi-agent system for traction-inverter design.**
> **Architecture:** LangGraph + PLECS (XML-RPC/MCP) + LiteLLM (CLI-first, provider-agnostic).
> **Method:** every research claim carries truth-status, evidence-strength, and a mandatory red-team block.

**Status:** 🟡 Knowledge base complete (29-chapter textbook + agent-architecture research, cited [1]–[170]); PLECS evidence harness working headless; 2L-B6 CAB450 model **heat-sink-coupling confirmed**. Next milestone: the first PLECS-validated 2L-B6 η/loss/Tj number. See [ROADMAP.md](ROADMAP.md).

## Start here

| Doc | Purpose |
|-----|---------|
| [ROADMAP.md](ROADMAP.md) | Phases, milestones, definition of "done" |
| [TODO.md](TODO.md) | Active tasks — flat, ruthless |
| [LOG.md](LOG.md) | Dev journal — dated what/why/blocked |
| [knowledge/SCHEMA.md](knowledge/SCHEMA.md) | The rules every file obeys (vault + repo organization) |

## What this repo is

Two research fields feeding one build. **Power-electronics** research defines *what* to design (traction inverters); **AI-agents** research defines *how* to build the system that designs them. The live evidence comes from **PLECS** simulations driven headless over XML-RPC.

## Layout

Reorganized 2026-07-20 to the scheme in [knowledge/SCHEMA.md](knowledge/SCHEMA.md) §Repository Organization:

```
knowledge/          Research material (the former srtp_docs vault, dismantled)
  notes/            Digested claims · topics · maps (power-electronics, ai-agents, problem-statement)
  sources/          One markdown capture per source paper (ai-agents, power-electronics)
  synthesis/        Cross-cutting synthesis + research open questions
    plans/          Implementation-plan specs (MAS hub + subsystems)
    trials/         Worked design-example write-ups
    log/            changelog/ + audits/ + session retrospectives (backing detail for LOG.md)
  SCHEMA.md README.md citations.md   _archive/  (retired .base indexes)
system/             The live MAS
  src/              PLECS harness (run_harness.py, summarize.py, templates/) + method docs
  configs/          model_registry.json
  env/models/       Wolfspeed SiC device library (669 models) + user guide   [read-only]
experiments/        One folder per design line / run — numpy loss model + .plecs + README
  <design>/         family-car-400v-sic, microcar-96v-mosfet, performance-800v-sic, truck-800v-sic
  2l-b6-800v-sic-bench/   Track-1 model — coupled 2L-B6 CAB450 bench (800 V, first η ≈ 99.1 %)
  ARCHIVE/          dpt-from-scratch, 2l-b6-rainflow, device-validation-buck (superseded stepping-stones)
results/metrics/    Tracked run outputs (per design); figures/ + logs/ (logs gitignored)
graphify-out/       Knowledge-graph outputs (graph.html, GRAPH_REPORT.md, obsidian/)
ROADMAP.md TODO.md LOG.md README.md   .mcp.json (MCP `plecs` server config — stays at repo root)
```

## Key architecture decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| A1 | CLI-first (not GUI) | Prove the agent works before adding UI. |
| A2 | 3 agents (not 7) | Orchestrator + Planner + Designer + Validator — minimal decomposition for the A/B test. |
| A3 | PLECS backend (not MATLAB) | System-level PE sim with native PMSM/IM + FOC, scriptable via XML-RPC/MCP. |
| A4 | SQLite | LangGraph checkpointer works with it; zero setup. |
| A5 | LiteLLM provider-agnostic | Route each task to the cheapest capable model. |
| A6 | Explicit optimizer | LLM picks structure, a numerical optimizer (DE/PSO/BO) picks numbers over PLECS. |

## Tooling

- **PLECS:** `C:\Users\ferre\OneDrive\Documents\Plexim\PLECS 4.8 (64 bit)` — launch `PLECS.exe -server 1080`; RPC at `http://localhost:1080`.
- **Readback contract:** `simulate`'s `Values` is empty in 4.8 — route signals to a `ToFile`→CSV and read from disk. After any `.plecs` edit, `close_model` then `open_model` (stale-model trap).
