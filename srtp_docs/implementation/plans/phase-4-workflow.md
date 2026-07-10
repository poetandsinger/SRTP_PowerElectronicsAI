# Phase 4 — Research Workflow (Weeks 8-9)

> **Part of:** [[plan index|Plan Index]]  
> **Goal:** Iterative research loop: Plan→Sim→Analyze→Replan with checkpointing.

| ID | Task | Deliverable | Verify |
|----|------|-------------|--------|
| P4.1 | StateGraph class | Nodes, conditional edges, state dict | Plan→Sim→Analyze→Replan graph |
| P4.2 | Checkpointer (SQLite) | Save/resume state at any node | Kill mid-sim, resume from checkpoint |
| P4.3 | Plan Node (LLM) | "Design 800V inverter" → topology, params | Valid simulation parameters |
| P4.4 | Simulate Node | Calls MATLAB Bridge, stores results | Runs within graph |
| P4.5 | Analyze Node (Python+LLM) | Extract efficiency, losses, THD | Identifies convergence |
| P4.6 | Conditional Edge | `should_continue()` → report or replan | Cycles until targets met |
| P4.7 | Progress visualization | Node status in workflow panel | "Simulating... iteration 3/10" |
| P4.8 | Integration test | "Design 400V 150kW >97% efficiency" | Agent iterates until converged |

← [[implementation/plans/phase-3-topology]] | [[implementation/plans/phase-5-components]] →
