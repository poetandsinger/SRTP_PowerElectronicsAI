# Phase 2 — MATLAB Bridge (Weeks 4-5)

> **Part of:** [[plan index|Plan Index]]  
> **Goal:** Start MATLAB externally, send commands, retrieve results.

| ID | Task | Deliverable | Verify |
|----|------|-------------|--------|
| P2.1 | `MatlabBridge` class | `start()`, `stop()`, `simulate()` | MATLAB starts, runs sim, returns data |
| P2.2 | Register MATLAB tools | `matlab_simulate`, `matlab_sweep`, `matlab_get_variable` | Agent calls tools successfully |
| P2.3 | Session management | Engine stays alive, auto-restart on crash | 10 calls without restart |
| P2.4 | Simulink parameterization | `set_param()` from Python | Change fs without reloading model |
| P2.5 | Post-simulation validation | Sanity check: efficiency 0-100%, no NaN | Bad result → agent retries |
| P2.6 | Wire to Results Dashboard | Waveforms in plots, efficiency in table | Simulation → GUI update |

← [[implementation/plans/phase-1-agent]] | [[implementation/plans/phase-3-topology]] →
