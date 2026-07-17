---
title: "PLECS Standalone Simulation Scripting — XML-RPC/JSON-RPC Interface"
type: source
field: ai-agents
tags: [ai-agents, simulation, integration, plecs, code-generation]
authors: [Plexim GmbH]
year: 2024
venue: "PLECS 5.0 Documentation / Plexim vendor docs"
url: "https://docs.plexim.com/plecs/5.0/scripting/"
captured: 2026-07-17
reliability: high
peer_reviewed: false
motivated: true
reliability_note: "Primary vendor documentation — authoritative on the API surface. `motivated` because it is the vendor's own docs, but the API contract is verifiable by running it. Feature exists in PLECS Standalone 4.x (the installed version is 4.8) and 5.x."
---

# PLECS Standalone Scripting — XML-RPC / JSON-RPC Interface

**Why this matters:** This is the concrete mechanism by which an AI agent drives PLECS. It replaces the MATLAB Engine API as the SRTP simulation backend. Confirmed available in PLECS Standalone (the installed build is 4.8).

## Interface

- PLECS Standalone runs a built-in **HTTP server** implementing **both XML-RPC and JSON-RPC** (auto-detected per request).
- **localhost only** (security). Enable in **Preferences → General → XML-RPC interface**, default TCP port **1080**. Disabled by default.
- Commands are **blocking** — the RPC server processes one request at a time.
- Any language with an RPC client works: Python (`xmlrpc.client`), MATLAB (`jsonrpc`), Java, C++, Ruby.

```python
import xmlrpc.client
proxy = xmlrpc.client.ServerProxy("http://localhost:1080")
```

## RPC procedures

| Procedure | Purpose |
|-----------|---------|
| `plecs.load(mdlFileName)` | Open model by **absolute** path |
| `plecs.close(mdlName)` | Close model without saving |
| `plecs.get(path[, param])` | Read all params (struct) or one param of a component |
| `plecs.set(path, param, value)` | Set a component parameter (paths like `'DTC/Mechanical'`) |
| `plecs.simulate(mdlName[, optStruct])` | Run transient sim |
| `plecs.analyze(mdlName, analysisName[, optStruct])` | Run a defined analysis (AC sweep, steady-state, impulse, multitone) |
| `plecs.scope(scopePath, cmd[, arg])` | `HoldTrace` / `RemoveTrace` / `ClearTraces` / `SaveTraces` / `LoadTraces` |

## optStruct (the sweep + solver control mechanism)

- **`ModelVars`** — struct overriding model-initialization variables (applied after init, before parameter evaluation). This is the **parameter sweep** hook. Values: scalars, vectors, matrices, 3-D arrays, strings.
- **`OutputFormat`** — `'Plain'` or `'MatFile'`.
- **`SolverOpts`** — `Solver` (`auto`/`dopri`/`radau`/`discrete`), `StartTime`, `TimeSpan`, `MaxStep`, `InitStep`, `FixedStep`, `AbsTol`, `RelTol`, `Timeout` (wall-clock seconds, 0 = off), `InitialSystemState`.
- **`AnalysisOpts`** — `TimeSpan`, `Tolerance`, `MaxIter`, `FrequencyRange`, `FrequencyScale`, `NumPoints`, `Perturbation`, `Response`, `ShowResults`.

```python
opts = {'ModelVars': {'varL': 50e-6}}
res = proxy.plecs.simulate("BuckParamSweep", opts)
```

## Parallelism

Pass a **list/cell array of optStructs** to `simulate()` or `analyze()`; PLECS distributes them across CPU cores and returns a matching list of results (or per-item error strings):

```python
results = proxy.plecs.simulate(mdl, [opts1, opts2, opts3])
```

## Output data

- Transient / steady-state: struct `{Time: vector, Values: m×n array}` (m timestamps × n signals).
- Small-signal (AC Sweep, Impulse, Multitone): `{F: freq vector, Gr, Gi}` (real/imag transfer function). **AC analysis is native** — no external Bode tooling needed.

## Implications for the SRTP MAS

1. **Sweeps, parallel batch, solver control, and AC analysis are all first-class over RPC** — the Simulation Agent needs only an RPC client, not code generation for the solver.
2. **`plecs.set`/`plecs.get` give programmatic parameter access** without rebuilding the model — the agent tunes a *template* model rather than authoring netlists (HAVEN-style template pattern, de-risks the "LLMs can't write netlists" concern).
3. **`.plecs` files are XML** — topology can in principle be edited/generated as structured text, but the low-risk path is a parameterized template + `ModelVars`.
4. **Blocking, single-request server** — the orchestrator must serialize PLECS calls or run multiple PLECS instances on different ports for true concurrency (the list-of-optStructs path is the supported parallel route).

See [[sources/ai-agents/plecs-ai-agent-integration-ordonez]] for a practitioner report of doing exactly this, and [[ai-agents/implementation-research]] for where this slots into the stack.
