---
title: PLECS Integration Strategy
type: topic
field: ai-agents
created: 2026-07-06
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [ai-agents, simulation, integration, plecs, architecture, tool-calling]
sources:
  - sources/ai-agents/plecs-xmlrpc-scripting-interface
  - sources/ai-agents/plecs-ai-agent-integration-ordonez
  - sources/ai-agents/pe-mas-flyback-mas
---

## Overview

**PLECS (Plexim) is the SRTP simulation backend** (2026-07 pivot away from MATLAB/Simulink). It is a system-level power-electronics simulator with **native machine models** (PMSM incl. saturation lookup, induction machine) and FOC traction demos, so it covers the motor-drive simulation that previously "required" MATLAB and removes the MATLAB license dependency. Installed build: **PLECS 4.8 (Standalone)**.

The research agent must be able to:
1. **Invoke PLECS** — load a model, run transient/AC/steady-state simulations.
2. **Pass parameters** — override component values / init variables per run.
3. **Retrieve results** — waveforms, efficiency, losses, Bode data — **summarized before the LLM sees them**.
4. **Iterate** — parameter sweeps, corners (low/high line, load), optimization loops.

> **The binding constraint is not the interface — it is validated per-topology models.** Per PE-MAS's `model_registry.json`, an agent can only produce "PLECS-backed evidence" for topologies that have a *built and validated* PLECS model. See [[pe-mas-flyback-mas]].

## Integration Approaches

PLECS Standalone runs a built-in **HTTP server speaking XML-RPC and JSON-RPC** (localhost, default port **1080**, enabled in Preferences). Full API: [[plecs-xmlrpc-scripting-interface]].

### Approach 1: Direct XML-RPC from Python (simplest)

```
Agent (Python) → xmlrpc.client → PLECS Standalone (port 1080)
```

```python
import xmlrpc.client
plecs = xmlrpc.client.ServerProxy("http://localhost:1080", allow_none=True)
plecs.plecs.load("/abs/path/inverter_2L_B6.plecs")
opts = {"ModelVars": {"Vdc": 800, "fsw": 10e3}, "SolverOpts": {"Solver": "dopri", "TimeSpan": 0.1}}
res = plecs.plecs.simulate("inverter_2L_B6", opts)   # -> {Time: vector, Values: m-by-n array}
```

**Pros:** first-class Python (natural for a Hermes/LangGraph agent); `plecs.set`/`plecs.get` give per-component parameter access without rebuilding the model; **AC small-signal analysis is native** (`plecs.analyze`). **Cons:** the RPC server is **blocking / single-request** — serialize calls or run multiple PLECS instances on different ports.

### Approach 2: PLECS MCP Server (recommended — proven prior art)

```
Agent ←→ MCP ←→ plecs-mcp server ←→ xmlrpc.client ←→ PLECS
```

PE-MAS ships a **working `plecs-mcp` FastMCP server** (~29 tools: `open_model`, `simulate`, `simulate_advanced`, `get/set_component_param`, `run_script`, `circuit_action/patch`, plus a **capability-discovery layer** — `list_methods`/`rpc_try_methods`/`call_first_available` — that probes which RPC methods a given PLECS build supports). Same MCP pattern as the already-captured `ltspice-mcp`, and the cleanest fit for an MCP-native harness (Claude Code, or Microsoft Agent Framework's native MCP).

**Pros:** clean separation; language-agnostic; robust to PLECS version drift; persistent PLECS process. **Cons:** one extra process. **Adopt this** — adapt PE-MAS's server rather than writing from scratch.

### Approach 3: Parallel batch via list-of-optStructs

Pass a **list of optStructs** to `plecs.simulate(model, [opts1, opts2, ...])`; PLECS distributes across CPU cores and returns a matching list. This is the supported route for corner sweeps and sensitivity runs without spinning up N instances.

## Model handling — template + injection, not free-form authoring

`.plecs` files are **XML**; control code lives in editable `.c/.h`. Two model paths, both proven in PE-MAS:
1. **Template + `ModelVars`/`plecs.set`** — a validated base model per topology; the agent only tunes parameters. Low risk; de-risks the "LLM can't write netlists" concern (G5).
2. **XML injection** (`PLECSGenerator`, ElementTree) — inject components into a base schematic for structural variants. Higher risk; keep for controlled topology edits, not blind synthesis.

## Tool API design (agent-facing)

```yaml
tools:
  - name: plecs_simulate      # load+run a topology template with ModelVars overrides
    parameters: {topology: string, model_vars: object, solver: object}
  - name: plecs_sweep         # list-of-optStructs corner/parameter sweep (parallel)
    parameters: {topology: string, base_vars: object, sweep: object, corners: string[]}
  - name: plecs_set_param     # plecs.set on a component path
  - name: plecs_analyze       # AC sweep / steady-state (native)
  - name: summarize_result    # CSV/waveform -> ~36-number report (NOT raw rows to the LLM)
```

The **`summarize_result` layer is not optional.** The only direct AI+PLECS prior art ([[plecs-ai-agent-integration-ordonez]]) found raw-waveform ingestion bankrupts the loop (~$20/hr), while engineered summaries cut tokens ~1000×. Mirror its 5-layer design: capture → summarize → regression-check vs baseline → pass/fail gate → agent.

## Capability boundary (design around this)

The same prior art showed an agent reliably handles **parameter sweeps, control-code refactoring, comparative analysis** but **not topology design, control-strategy selection, physics interpretation, or literature review**. So: cheap tool-calling models drive PLECS runs; strong reasoning models (+ RAG grounding) own topology/control/physics. The MAS must honor this split.

## Performance considerations

- **Blocking RPC:** serialize per instance; use list-of-optStructs or multiple ports for concurrency.
- **Solver choice via `SolverOpts`:** `dopri` (non-stiff), `radau` (stiff), `discrete` (fixed-step) — set per model, no code-gen needed.
- **`Timeout` field** guards against runaway sims.
- **Summarize on the Python side**, never stream raw `Values` arrays into the context window.

> **References:** [[citations]], [[plecs-xmlrpc-scripting-interface]], [[plecs-ai-agent-integration-ordonez]]

← [[harness-comparison|Prev: Comparative Analysis]] | [[harness-architecture-patterns|Next: Architecture Patterns]] → | [[README]]
