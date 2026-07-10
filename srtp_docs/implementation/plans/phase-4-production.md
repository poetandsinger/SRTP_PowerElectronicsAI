# Phase 4 — Production Hardening (Weeks 11-12)

> **Part of:** [[plan index|Plan Index]]
> **Goal:** Watchdog, human-in-the-loop, evaluation benchmark, packaging. 24h autonomous operation.
> **Architecture:** Watchdog process + HITL interrupts + CLI packaging + published benchmark

---

## Context

Phases 0-3 built a working research agent. Phase 4 makes it reliable enough to run autonomously for 24+ hours and produces results that can be shared publicly.

---

## Week 11: Reliability

### P4.1 — Watchdog Process (Days 1-2)

**Critical gap from Diagrid (Feb 2026):** LangGraph checkpointing saves state but doesn't auto-resume. We need a watchdog.

```python
# src/srtp_ai/watchdog.py
import asyncio
import time
from datetime import datetime, timedelta

class Watchdog:
    """
    Monitors LangGraph runs and auto-resumes stuck graphs.
    
    Pattern: Diagrid analysis (Feb 2026) — checkpointing saves state,
    but YOU must detect failures and resume. This watchdog does that.
    """
    
    def __init__(self, checkpointer, timeout_minutes: int = 30):
        self.checkpointer = checkpointer
        self.timeout = timeout_minutes
        self.active_runs: dict[str, WatchEntry] = {}
    
    async def monitor(self, graph_id: str):
        """Monitor a running graph. Auto-resume if stuck."""
        entry = WatchEntry(graph_id=graph_id, started=datetime.now(), last_transition=datetime.now())
        self.active_runs[graph_id] = entry
        
        while True:
            await asyncio.sleep(60)  # Check every minute
            
            # Check if graph is stuck (no state transition in T_timeout)
            stuck_for = (datetime.now() - entry.last_transition).total_seconds() / 60
            if stuck_for > self.timeout:
                logger.warning(f"Graph {graph_id} stuck for {stuck_for:.0f} min — attempting resume")
                self._resume(graph_id)
            
            # Check if graph completed
            state = self.checkpointer.get(graph_id)
            if state and state.get("next_step") == "end":
                logger.info(f"Graph {graph_id} completed")
                del self.active_runs[graph_id]
                break
    
    def _resume(self, graph_id: str):
        """Resume a stuck graph from last checkpoint."""
        config = {"configurable": {"thread_id": graph_id}}
        try:
            # Reload state from checkpoint
            state = app.get_state(config)
            logger.info(f"Resuming {graph_id} from checkpoint at iteration {state.values.get('iteration', '?')}")
            
            # Resume execution
            app.invoke(None, config)
            
            self.active_runs[graph_id].last_transition = datetime.now()
        except Exception as e:
            logger.error(f"Failed to resume {graph_id}: {e}")
            self._alert_human(graph_id, str(e))
    
    def record_transition(self, graph_id: str):
        """Called by LangGraph after every state transition."""
        if graph_id in self.active_runs:
            self.active_runs[graph_id].last_transition = datetime.now()
    
    def _alert_human(self, graph_id: str, error: str):
        """Alert human operator when auto-resume fails."""
        # For now: log + print. Future: Telegram/email via Hermes Gateway.
        logger.critical(f"HUMAN INTERVENTION NEEDED: Graph {graph_id} failed auto-resume: {error}")
        print(f"\n{'='*60}")
        print(f"⚠️  AGENT STUCK — HUMAN INTERVENTION NEEDED")
        print(f"Graph: {graph_id}")
        print(f"Error: {error}")
        print(f"Checkpoint saved. Resume manually:")
        print(f"  python -m srtp_ai resume {graph_id}")
        print(f"{'='*60}\n")
```

**Deliverable:** Watchdog that polls every 60s, auto-resumes stuck graphs, alerts human on failure.
**Verify:** Start a design → kill the process → watchdog auto-resumes → design completes.

### P4.2 — Idempotency Keys (Day 2)

Prevent duplicate simulation runs (Diagrid gap: no duplicate prevention in LangGraph):

```python
# src/srtp_ai/idempotency.py
import hashlib
import json

class IdempotencyManager:
    """Prevent duplicate simulation runs."""
    
    def __init__(self, db_path: str = "idempotency.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS executed_runs (
                key TEXT PRIMARY KEY,
                result_json TEXT,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def key(self, spec: dict, components: dict, params: dict) -> str:
        """Generate idempotency key from canonical representation."""
        canonical = json.dumps({
            "spec": spec,
            "components": components,
            "params": params,
        }, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]
    
    def get_or_execute(self, key: str, fn, *args, **kwargs):
        """Execute fn only if this exact run hasn't been done before."""
        existing = self.conn.execute(
            "SELECT result_json FROM executed_runs WHERE key = ?", (key,)
        ).fetchone()
        
        if existing:
            logger.info(f"Idempotency hit: {key} — returning cached result")
            return json.loads(existing[0])
        
        result = fn(*args, **kwargs)
        self.conn.execute(
            "INSERT INTO executed_runs (key, result_json) VALUES (?, ?)",
            (key, json.dumps(result))
        )
        return result
```

**Deliverable:** Idempotency manager. No duplicate simulation for same inputs.
**Verify:** Run same simulation twice → second run returns cached result, no ngspice process spawned.

### P4.3 — Human-in-the-Loop (Days 2-3)

```python
# src/srtp_ai/hitl.py
class HumanInTheLoop:
    """
    Human review gates before expensive operations.
    
    Pattern: PE-MAS interrupt_before + Osprey plan review.
    """
    
    interrupt_points = [
        "before_simulation",    # Review plan before spending compute
        "before_iteration_3",   # Review if design isn't converging after 3 iterations
        "before_release",       # Final human signoff on design
    ]
    
    async def review_plan(self, state: DesignState):
        """Present execution plan for human approval before simulation."""
        print(f"""
╔══════════════════════════════════════════════╗
║  EXECUTION PLAN — REVIEW BEFORE SIMULATING  ║
╠══════════════════════════════════════════════╣
║  Spec: {state['spec']['vdc']}V, {state['spec']['pout']}kW                       ║
║  Topology: {state['topology']}                           ║
║  Components: {len(state['components'])} selected                  ║
║  Estimated sim time: ~{state.get('est_sim_time', '?')} min                ║
║  Estimated cost: ${state.get('token_cost', 0):.2f}                     ║
╠══════════════════════════════════════════════════╣
║  [A]pprove  [R]eject  [E]dit parameters         ║
╚══════════════════════════════════════════════════╝
        """)
        
        choice = input("> ").strip().lower()
        if choice == 'a':
            return "approved"
        elif choice == 'e':
            # Let human edit parameters
            edits = self._interactive_edit(state)
            return "edited", edits
        else:
            return "rejected"
```

**Deliverable:** HITL interrupts at 3 critical points. Human can approve, reject, or edit.
**Verify:** Run a design → plan presented for approval → approve → simulation runs. Reject → stops.

---

## Week 12: Evaluation + Packaging

### P4.4 — Evaluation Benchmark (Days 4-6)

Build a publishable benchmark for traction inverter design:

```python
# src/srtp_ai/benchmark.py (final version)
TRACTION_INVERTER_BENCHMARK = {
    "name": "SRTP Traction Inverter Design Benchmark v1.0",
    "specs": [
        {
            "id": "TI-400-150",
            "description": "400V 150kW 2L-B6 — entry-level BEV",
            "vdc": 400, "pout": 150, "topology": "2L-B6",
            "efficiency_baseline": 0.96,  # Published IGBT baseline
            "reference": "Infineon HybridPACK Drive IGBT, ~96% peak"
        },
        {
            "id": "TI-800-250",
            "description": "800V 250kW 2L-B6 — premium BEV",
            "vdc": 800, "pout": 250, "topology": "2L-B6",
            "efficiency_baseline": 0.975,  # Published SiC baseline
            "reference": "Tesla Model S Plaid, ~97.5% peak (estimated)"
        },
        {
            "id": "TI-800-200-3L",
            "description": "800V 200kW 3L-TNPC — premium efficiency focus",
            "vdc": 800, "pout": 200, "topology": "3L-TNPC",
            "efficiency_baseline": 0.98,  # Sachs & Neuburger (2025) 3L-TNPC
            "reference": "Sachs & Neuburger (2025), arXiv:2508.14224v1"
        },
        {
            "id": "TI-400-100",
            "description": "400V 100kW 2L-B6 — cost-sensitive city car",
            "vdc": 400, "pout": 100, "topology": "2L-B6",
            "efficiency_baseline": 0.95,
            "reference": "Entry-level IGBT design"
        },
        {
            "id": "TI-800-150-GaN",
            "description": "800V 150kW — GaN HEMT stretch goal",
            "vdc": 800, "pout": 150, "topology": "3L-ANPC",
            "efficiency_baseline": 0.985,  # Cacciato et al. (2022) GaN ANPC
            "reference": "Cacciato et al. (2022), arXiv:2212.05246v1"
        },
    ],
    "metrics": {
        "efficiency": "Peak inverter efficiency from simulation",
        "thd": "Line current THD at rated power (%)",
        "vds_margin": "Max Vds as % of rated voltage",
        "tj_margin": "Max Tj below rated maximum (°C)",
        "bom_cost": "Total BOM cost from Nexar pricing (USD)",
        "simulation_time": "Wall clock time (seconds)",
        "token_cost": "LLM API cost (USD)",
        "iterations": "Design iterations to convergence",
        "citations": "Number of real, verified paper citations",
    },
    "scoring": {
        "efficiency_above_baseline": "efficiency - baseline (higher is better)",
        "composite_score": "weighted sum: efficiency(40%) + thd(20%) + tj_margin(20%) + cost(20%)",
    }
}
```

**Deliverable:** 5-spec benchmark with scoring, baselines, and published references.
**Verify:** Run agent against all 5 specs. Publish results.

### P4.5 — CLI Packaging (Days 6-7)

```bash
# src/srtp_ai/cli.py
"""
SRTP Power Electronics AI — CLI

Usage:
  srtp-ai design "800V 250kW SiC traction inverter"
  srtp-ai design --spec spec.json
  srtp-ai benchmark                    # Run full benchmark
  srtp-ai resume <graph_id>           # Resume from checkpoint
  srtp-ai memory search "SiC MOSFET efficiency"
  srtp-ai memory stats                 # Memory store statistics
"""

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

@click.group()
def cli():
    """SRTP Power Electronics AI — Multi-Agent Traction Inverter Design."""
    pass

@cli.command()
@click.argument("description")
@click.option("--topology", "-t", help="Force topology: 2L-B6, 3L-NPC, 3L-TNPC")
@click.option("--max-iterations", "-n", default=10, help="Max design iterations")
@click.option("--approve/--no-approve", default=True, help="Require human approval before simulation")
def design(description, topology, max_iterations, approve):
    """Design a traction inverter from a natural language description."""
    spec = parse_spec(description, topology)
    
    console.print(f"[bold]Designing:[/bold] {spec['vdc']}V {spec['pout']}kW {spec['topology']}")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Designing...", total=None)
        
        result = asyncio.run(app.ainvoke({
            "spec": spec,
            "max_iterations": max_iterations,
            "human_approval": approve,
        }))
        
        progress.update(task, completed=100)
    
    # Display results
    table = Table(title="Design Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    r = result["simulation_results"]
    table.add_row("Efficiency", f"{r['efficiency']*100:.1f}%")
    table.add_row("THD", f"{r['thd']:.1f}%")
    table.add_row("Max Tj", f"{r['tj_est']:.0f}°C")
    table.add_row("Iterations", str(result["iteration"]))
    table.add_row("Cost", f"${result.get('token_cost', 0):.2f}")
    
    console.print(table)

@cli.command()
def benchmark():
    """Run the full evaluation benchmark."""
    console.print("[bold]SRTP Traction Inverter Design Benchmark v1.0[/bold]\n")
    
    results = []
    for spec in TRACTION_INVERTER_BENCHMARK["specs"]:
        console.print(f"→ {spec['id']}: {spec['description']}")
        result = asyncio.run(app.ainvoke({"spec": spec, "max_iterations": 10}))
        results.append(result)
    
    # Summary table
    table = Table(title="Benchmark Results")
    table.add_column("Spec", style="cyan")
    table.add_column("Efficiency", style="green")
    table.add_column("vs Baseline", style="yellow")
    table.add_column("Iterations")
    table.add_column("Cost")
    
    for r, spec in zip(results, TRACTION_INVERTER_BENCHMARK["specs"]):
        eff = r["simulation_results"]["efficiency"]
        delta = eff - spec["efficiency_baseline"]
        table.add_row(
            spec["id"],
            f"{eff*100:.1f}%",
            f"{delta*100:+.1f}%",
            str(r["iteration"]),
            f"${r.get('token_cost', 0):.2f}",
        )
    
    console.print(table)

if __name__ == "__main__":
    cli()
```

**Deliverable:** CLI with `design`, `benchmark`, `resume`, `memory` commands. Rich-formatted output.
**Verify:** `srtp-ai design "400V 150kW 2-level inverter"` → produces design with formatted results.

### P4.6 — Documentation (Days 7-9)

```markdown
# README.md
- Project overview
- Quick start (3 commands to first design)
- Architecture diagram
- Benchmark results
- How to contribute

# CONTRIBUTING.md
- Development setup
- Running tests
- Adding new SPICE templates
- Adding new agent roles

# docs/
- Architecture deep dive
- Agent role specification
- Simulation backend guide
- Benchmark methodology
```

**Deliverable:** README + CONTRIBUTING + docs/ with architecture guide.
**Verify:** A new developer can clone, install, and run a design in < 10 minutes.

### P4.7 — Error Handling & Edge Cases (Days 9-10)

```python
# src/srtp_ai/errors.py
class SrtpError(Exception): ...

# Simulation errors
class SimulationDivergenceError(SrtpError): ...
class SimulationTimeoutError(SrtpError): ...
class NaNInResultsError(SrtpError): ...

# Agent errors
class RoutingError(SrtpError): ...        # Orchestrator sent task to wrong agent
class ComponentNotFoundError(SrtpError): ...  # No real component found for specs
class CitationVerificationError(SrtpError): ...  # PaperQA2 citation not verifiable

# Recovery strategies
ERROR_RECOVERY = {
    SimulationDivergenceError: "Retry with adjusted solver settings (smaller step, different solver)",
    SimulationTimeoutError: "Reduce simulation stop time or model complexity",
    NaNInResultsError: "Check for floating-point issues in netlist (zero resistances, etc.)",
    RoutingError: "Explicit route to correct agent, log misrouting for analysis",
    ComponentNotFoundError: "Relax spec constraints by 10% and retry",
    CitationVerificationError: "Flag as unverified, don't block design",
}
```

**Deliverable:** Typed error hierarchy with recovery strategies.
**Verify:** Inject each error type → agent recovers with appropriate strategy.

### P4.8 — Final Benchmark Run + Report (Days 10-12)

```bash
# Run full benchmark
srtp-ai benchmark > benchmark_results_$(date +%Y-%m-%d).txt

# Generate report
python -m srtp_ai report --benchmark benchmark_results_*.txt --output benchmark_report.pdf
```

**Deliverable:** Benchmark report with all 5 specs, efficiency deltas vs baselines, cost analysis.
**Verify:** Results are reproducible (same spec → same results within 1%).

---

## Phase 4 Checklist

- [ ] P4.1: Watchdog auto-resumes stuck graphs. Human alerted on failure.
- [ ] P4.2: Idempotency prevents duplicate simulation runs.
- [ ] P4.3: HITL: plan review, iteration-3 check, release signoff.
- [ ] P4.4: 5-spec evaluation benchmark with scoring.
- [ ] P4.5: CLI: `design`, `benchmark`, `resume`, `memory` commands.
- [ ] P4.6: README + CONTRIBUTING + docs/. New dev onboarded in < 10 min.
- [ ] P4.7: Error handling: typed errors + recovery strategies.
- [ ] P4.8: Benchmark report published. Results reproducible.

## Phase 4 Acceptance

1. Agent runs 24+ hours autonomously without human intervention
2. Watchdog successfully auto-resumes from at least 3 simulated failures
3. HITL interrupts functional at all 3 points
4. Full benchmark completes on all 5 specs
5. Benchmark results are reproducible (within 1% across runs)
6. Package installable: `pip install srtp-ai && srtp-ai design "400V 150kW inverter"` works

---

← [[implementation/plans/phase-3-knowledge]] | [[plan index|Plan Index]] →
