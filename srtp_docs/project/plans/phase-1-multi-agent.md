---
title: Phase 1 — Multi-Agent Core
type: plan
field: project
created: 2026-07-06
updated: 2026-07-10
tags: [plan]
---

# Phase 1 — Multi-Agent Core (Weeks 3-5)

> **Part of:** [[plans-index|Plan Index]]
> **Goal:** 3-agent LangGraph system with checkpointing, guardrails, evidence gates. Matches or beats single-agent on benchmark.
> **Architecture:** LangGraph StateGraph + SqliteSaver + LiteLLM + PySpice

---

## Context

Phase 0 proved the single agent can design an inverter. Phase 1 builds the multi-agent system and validates it against the same benchmark. This phase implements the hybrid LangGraph-CrewAI pattern validated at 96.1% success rate (IEEE Access, April 2026).

**We start with 3 agents** (Orchestrator, Simulation, Reviewer) — not the 7-agent architecture from the integration note. The integration architecture defines the end-state. Phase 1 builds the minimum viable decomposition. We add specialists in Phase 3 only if needed.

---

## Week 3: LangGraph State Machine

### P1.1 — Typed State Definition (Day 1)

```python
# src/srtp_ai/state.py
from typing import TypedDict, Literal, Annotated
from langgraph.graph.message import add_messages
import operator

class DesignState(TypedDict):
    """Complete state for traction inverter design workflow."""
    # Input
    spec: dict                      # {vdc, pout, topology, efficiency_target, constraints}
    
    # Planning
    execution_plan: dict | None     # Plan-then-execute (PE-MAS pattern)
    planning_summary: str | None    # Human-readable plan summary
    
    # Design
    topology: str | None            # "2L-B6" | "3L-NPC" | "3L-TNPC" | "ANPC"
    components: dict | None         # {switches: [...], gate_drivers: [...], dc_link_cap: {...}, sensors: [...]}
    netlist: str | None             # Generated SPICE netlist
    
    # Simulation
    simulation_params: dict | None  # {fs, modulation, dead_time, solver, tstop}
    simulation_results: dict | None # {efficiency, thd, waveforms, converged, vds_max, tj_est}
    
    # Review
    review_findings: list[dict] | None  # [{issue, severity, agent, recommendation}]
    consensus_score: float | None   # DRCY multi-run consensus (0.0-1.0)
    
    # Iteration
    iteration: int
    max_iterations: int
    best_design: dict | None        # Best-effort tracking (PE-MAS pattern)
    best_efficiency: float
    
    # Gates
    evidence_gates: dict | None     # {efficiency: bool, thermal: bool, thd: bool, ...}
    guardrail_violations: list[str] # Active violations
    
    # Messages (append-only audit trail)
    messages: Annotated[list, add_messages]
    
    # Routing
    next_step: str  # "simulate" | "review" | "iterate" | "report" | "end"
```

**Deliverable:** `state.py` with complete typed state.
**Verify:** StateGraph compiles with this state. All fields have defaults.

### P1.2 — Orchestrator Agent (Days 1-3)

```python
# src/srtp_ai/agents/orchestrator.py
class OrchestratorAgent:
    """
    Decomposes inverter spec → generates execution plan → routes to specialists.
    
    Model: deepseek-chat (cheap, fast coordination)
    LLM calls per design: 2 (plan + decide)
    """
    
    model = "deepseek-chat"
    
    def plan(self, state: DesignState) -> DesignState:
        """
        Build execution plan (PE-MAS pattern: plan-then-execute).
        
        LLM PROMPT:
        You are a senior power electronics research lead.
        Given this traction inverter specification:
        - Vdc: {spec.vdc}V
        - Pout: {spec.pout}kW
        - Topology preference: {spec.topology or "not specified"}
        - Target efficiency: {spec.efficiency_target}
        
        Create an execution plan with:
        1. Recommended topology (justify)
        2. Key component ratings (Vdc, Idc, fs range)
        3. Simulation approach (solver, stop time, measurements)
        4. Expected challenges (thermal, EMI, convergence)
        
        Return as structured JSON.
        """
        ...
    
    def decide(self, state: DesignState) -> str:
        """
        Review results → decide: iterate or conclude.
        
        Decision rules:
        - efficiency < target AND iteration < max → "iterate"
        - guardrail violations present → "iterate" (must resolve)
        - efficiency >= target AND all gates closed → "done"
        - iteration >= max → "done" (best effort)
        """
        if state["guardrail_violations"]:
            return "iterate"
        if state["evidence_gates"] and all(state["evidence_gates"].values()):
            return "done"
        if state["iteration"] >= state["max_iterations"]:
            return "done"
        if state["simulation_results"]["efficiency"] >= state["spec"]["efficiency_target"]:
            return "done"
        return "iterate"
```

**Deliverable:** `OrchestratorAgent` with `plan()` and `decide()`.
**Verify:** Given 3 benchmark specs, produces plausible execution plans. Routes correctly.

### P1.3 — Simulation Agent (Days 2-4)

```python
# src/srtp_ai/agents/simulator.py
class SimulationAgent:
    """
    Fills SPICE templates, runs PySpice, validates output.
    
    Model: deepseek-chat (mechanical code generation)
    LLM calls per design: 1-2 (template fill + iteration adjust)
    """
    
    model = "deepseek-chat"
    
    def size_components(self, spec: dict, topology: str) -> dict:
        """
        Calculate component values from spec using analytical equations.
        
        LLM PROMPT:
        For a {topology} traction inverter:
        - DC voltage: {spec.vdc}V
        - Output power: {spec.pout}kW
        - Assume PWM frequency: 10-20 kHz
        - Assume SiC MOSFETs (if 800V) or IGBTs (if 400V)
        
        Calculate:
        1. Switch voltage rating: ≥ 1.2 × Vdc (IGBT) or ≥ 1.5 × Vdc (SiC)
        2. Switch current rating: Pout / (√3 × Vdc × cosφ), cosφ ≈ 0.85
        3. DC-link capacitance: ~2-4 μF/kW for film capacitors
        4. Switching frequency: recommend based on device type and power level
        5. Dead time: 1-2 μs (IGBT), 0.2-0.5 μs (SiC)
        
        Return as structured JSON.
        """
        ...
    
    def fill_template(self, components: dict, spec: dict, topology: str) -> str:
        """Fill SPICE template with sized components. ZERO LLM calls."""
        template = TEMPLATES[topology]
        return template.format(**components, **spec)
    
    def simulate(self, netlist: str, params: dict) -> SimulationResult:
        """
        Run PySpice simulation. ZERO LLM calls.
        
        Includes post-simulation validation (Claude Code hook pattern):
        - Check output file exists
        - Check efficiency ∈ [0, 100]%
        - Check no NaN/inf in waveforms
        - Check simulation converged
        """
        # Run ngspice
        simulator = CircuitSimulator(netlist)
        raw = simulator.run(**params)
        
        # Validate
        assert 0 <= raw.efficiency <= 1.0, f"Efficiency out of range: {raw.efficiency}"
        assert not raw.has_nan(), "NaN in simulation output"
        assert raw.converged, "Simulation did not converge"
        
        return SimulationResult.from_raw(raw)
```

**Deliverable:** `SimulationAgent` with component sizing, template fill, simulation, and validation.
**Verify:** Takes a spec → produces a converged simulation → passes all post-sim validation checks.

### P1.4 — Reviewer Agent with Multi-Run Consensus (Days 3-5)

```python
# src/srtp_ai/agents/reviewer.py
class ReviewerAgent:
    """
    Reviews simulation results against spec and baselines.
    
    Model: claude-sonnet (critical analysis needs best reasoning)
    Pattern: DRCY multi-run consensus (k=3 independent reviews)
    LLM calls per design: 3 (independent reviews) + 1 (consensus) = 4
    """
    
    model = "claude-sonnet"
    consensus_runs = 3
    
    async def review(self, state: DesignState) -> DesignState:
        """Run 3 independent reviews + reconcile."""
        # 3 independent reviews
        reviews = await asyncio.gather(*[
            self._single_review(state) for _ in range(self.consensus_runs)
        ])
        
        # Reconcile (DRCY pattern)
        consensus = self._reconcile(reviews)
        
        state["review_findings"] = consensus.findings
        state["consensus_score"] = consensus.confidence
        state["evidence_gates"] = self._check_gates(state)
        
        return state
    
    def _single_review(self, state: DesignState) -> ReviewReport:
        """
        LLM PROMPT:
        You are a skeptical power electronics design reviewer.
        
        Design: {state.topology}, {state.spec.vdc}V, {state.spec.pout}kW
        Simulation results: efficiency={result.efficiency}, THD={result.thd}%
        
        Check:
        1. Efficiency vs published baseline for this voltage/power class
        2. THD: < 5% per IEEE 519
        3. Thermal: Tj_est < Tj_max - 25°C
        4. Voltage stress: Vds_max < 80% rating
        5. Current stress: Id_peak < 90% rating
        6. EMI: dv/dt < 30 kV/μs
        7. DC-link ripple: < 5% of Vdc
        
        Return findings as structured JSON. Be brutally honest.
        """
        ...
    
    def _reconcile(self, reviews: list[ReviewReport]) -> ConsensusReport:
        """Multi-run consensus (DRCY pattern)."""
        # Findings appearing in ≥2/3 reviews → high confidence
        # Findings appearing in 1/3 reviews → critically evaluate
        # Contradictions → re-examine with full context
        
        findings_by_id = {}
        for review in reviews:
            for finding in review.findings:
                fid = finding["id"]
                if fid not in findings_by_id:
                    findings_by_id[fid] = []
                findings_by_id[fid].append(finding)
        
        high_confidence = [f for fid, finds in findings_by_id.items() if len(finds) >= 2]
        uncertain = [f for fid, finds in findings_by_id.items() if len(finds) == 1]
        
        return ConsensusReport(
            findings=high_confidence + uncertain,
            confidence=len(high_confidence) / max(1, len(high_confidence) + len(uncertain))
        )
```

**Deliverable:** `ReviewerAgent` with 3-run consensus, evidence gate checking.
**Verify:** Review a known-good design → high confidence, few findings. Review a known-bad design → catches all issues.

### P1.5 — LangGraph Assembly (Days 5-7)

```python
# src/srtp_ai/workflow.py
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

def build_design_workflow() -> StateGraph:
    workflow = StateGraph(DesignState)
    
    # Nodes
    workflow.add_node("orchestrator", OrchestratorAgent().plan)
    workflow.add_node("simulate", SimulationAgent().run)
    workflow.add_node("review", ReviewerAgent().review)
    workflow.add_node("report", ReportGenerator().generate)
    
    # Edges
    workflow.set_entry_point("orchestrator")
    workflow.add_edge("orchestrator", "simulate")
    workflow.add_edge("simulate", "review")
    
    # Conditional: iterate or conclude
    workflow.add_conditional_edges(
        "review",
        OrchestratorAgent().decide,
        {
            "iterate": "orchestrator",
            "done": "report"
        }
    )
    
    workflow.add_edge("report", END)
    
    # Checkpointing
    checkpointer = SqliteSaver.from_conn_string("design_checkpoints.db")
    return workflow.compile(checkpointer=checkpointer)

# Usage
app = build_design_workflow()
config = {"configurable": {"thread_id": "design-001"}}

# Plan-then-execute (PE-MAS pattern)
plan = orchestrator.plan({"spec": spec})
print(f"Execution plan: {plan['planning_summary']}")
# Human reviews plan here (optional HITL)

# Execute
for event in app.stream(initial_state, config):
    print(f"→ {event}")
```

**Deliverable:** Working LangGraph workflow. Full design → simulate → review → iterate → report.
**Verify:** Run against all 3 benchmark specs. Compare to Phase 0 single agent results.

---

## Week 4-5: Integration, Testing, Benchmarking

### P1.6 — Evidence Gates (Days 8-9)

Implement all 8 evidence gates from the integration architecture (§3.5):

```python
# src/srtp_ai/gates.py
class EvidenceGates:
    gates = {
        "efficiency": lambda s: s["simulation_results"]["efficiency"] >= s["spec"]["efficiency_target"],
        "thermal": lambda s: s["simulation_results"]["tj_est"] <= (175 if "SiC" in str(s["components"]) else 150) - 25,
        "thd": lambda s: s["simulation_results"]["thd"] <= 5.0,
        "emi": lambda s: s["simulation_results"].get("dvdt", 0) <= 30,  # kV/μs
        "component_stress": lambda s: all_stress_within_limits(s),
        "standards": lambda s: len(s["guardrail_violations"]) == 0,
        "cost": lambda s: s.get("bom_cost", float("inf")) <= s["spec"].get("cost_baseline", float("inf")) * 1.2,
        "human_signoff": lambda s: s.get("human_approved", False),
    }
    
    def check_all(self, state: DesignState) -> dict[str, bool]:
        return {name: check(state) for name, check in self.gates.items()}
```

**Deliverable:** All 8 gates implemented. Gate status visible in design state.
**Verify:** A passing design has all gates closed. A failing design has specific gate failures.

### P1.7 — A/B Test: Multi-Agent vs Single-Agent (Days 9-10)

**Re-run the Phase 0 A/B test with the full Phase 1 implementation:**

| Metric | Single Agent (P0) | Multi-Agent (P1) | Winner |
|--------|------------------|------------------|--------|
| Efficiency (avg across 3 specs) | ? | ? | ? |
| Convergence rate | ? | ? | ? |
| Wall time (per design) | ? | ? | ? |
| Token cost (per design) | ? | ? | ? |
| Iterations to converge | ? | ? | ? |
| Guardrail violations caught | ? | ? | ? |

**Decision gate:** Multi-agent must match or beat single-agent on efficiency AND not exceed 3× cost.

### P1.8 — Tests & Documentation (Days 10-12)

```bash
# Tests
pytest tests/ -q --cov=src/srtp_ai --cov-report=term

# Minimum test coverage:
# - Unit tests: each agent, each guardrail, each gate
# - Integration test: full workflow on simplest spec
# - Regression test: benchmark results don't degrade
```

**Deliverable:** 20+ tests passing, ≥ 70% coverage.
**Verify:** `pytest -q` all green. Integration test: "Design 400V 150kW inverter" runs end-to-end without human intervention.

---

## Phase 1 Checklist

- [ ] P1.1: Typed state definition, StateGraph compiles
- [ ] P1.2: Orchestrator plans correctly for 3 benchmark specs
- [ ] P1.3: Simulation agent: component sizing → template fill → simulate → validate
- [ ] P1.4: Reviewer agent: 3-run consensus, evidence gate checking
- [ ] P1.5: Full LangGraph workflow: design → simulate → review → iterate → report
- [ ] P1.6: All 8 evidence gates implemented
- [ ] P1.7: **A/B test complete. Multi-agent ≥ single-agent on benchmark?**
- [ ] P1.8: 20+ tests passing, ≥ 70% coverage
- [ ] P1.9: Token cost tracked, < $5 per design
- [ ] P1.10: Checkpoint recovery: kill mid-sim → resume from exact point

## Phase 1 Acceptance

1. Multi-agent matches or exceeds single-agent efficiency on all 3 benchmark specs
2. Full workflow runs end-to-end without human intervention
3. Reviewer catches 80%+ of intentionally injected design flaws
4. Checkpoint recovery works (kill process, resume, no lost progress)
5. All 7 guardrails functional, all 8 evidence gates functional
6. < $5 API cost per design

---

← [[project/plans/phase-0-foundation]] | [[project/plans/phase-2-simulation]] →
