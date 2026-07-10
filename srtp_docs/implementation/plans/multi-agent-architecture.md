# Multi-Agent Architecture Plan — SRTP Power Electronics AI

> **Type:** Implementation Plan (operational — not a research claim)
> **Derived from:** [[cs/multi-agent-synthesis]] — synthesis of 7 harness architectures
> **Validated against:** [[sources/cs/pe-mas-flyback-mas]] — working LangGraph MAS for flyback design (2026)
> **Created:** 2026-07-09
> **Status:** Draft — for review. Architecture validated by prior art.

---

## 0. Where This Plan Comes From

This plan synthesizes concrete implementation ideas from:

| Source | Type | What We Take |
|--------|------|-------------|
| **Claude Code** [3][4] | Closed-source | Subagent model (per-agent model+tools), hooks for post-simulation validation, granular tool permissions |
| **Hermes Agent** [1][2] | Open-source (MIT) | delegate_task pattern, skills/memory infrastructure, cron scheduling, multi-profile isolation |
| **LangGraph** [7][8] | Open-source (MIT) | State-machine orchestration, checkpointing, conditional edges, human-in-the-loop interrupts |
| **CrewAI** [9] | Open-source (MIT) | Role-based agent definition, entity memory per role, task dependency chaining |
| **smolagents** [12] | Open-source (Apache 2.0) | ManagedAgent task→report contract, CodeAgent for code-generation tasks |
| **AutoGen** [10] | Open-source (CC-BY-4.0) | GroupChat for multi-perspective design review |

Full synthesis and rationale in [[cs/multi-agent-synthesis]].

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SRTP AGENT PLATFORM                           │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 ORCHESTRATOR (LangGraph StateGraph)         ││
│  │  State machine: SPEC → LIT_REVIEW → COMPONENT → SIM →      ││
│  │                ANALYZE → (iterate or REPORT)                ││
│  │  Checkpoint at every transition (SQLite)                    ││
│  └───┬──────────────┬──────────────┬───────────────────────────┘│
│      │              │              │                             │
│      ▼              ▼              ▼                             │
│  ┌────────┐   ┌──────────┐   ┌──────────┐                       │
│  │LIT     │   │MATLAB    │   │REVIEWER  │  ← Specialist Agents  │
│  │AGENT   │   │AGENT     │   │AGENT     │    (delegate_task)    │
│  └────────┘   └──────────┘   └──────────┘                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              INFRASTRUCTURE (Hermes Agent)                   ││
│  │  Memory │ Skills │ Cron │ Gateway │ Profiles │ Toolsets     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              EXTERNAL TOOLS                                  ││
│  │  MATLAB Engine API │ Simulink │ PLECS │ arXiv │ PaperQA2    ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### The Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Orchestration** | LangGraph `StateGraph` | Research workflow state machine with checkpointing |
| **Agent Framework** | Custom (Python) | Agent class wrapping LLM + tools + memory |
| **Subagent Spawning** | Hermes `delegate_task` pattern | Isolated specialist agents with own context |
| **Memory** | Hermes memory store / CrewAI entity memory pattern | Persistent research context across sessions |
| **Tools** | Custom Python + MATLAB Engine API | Power electronics simulation and analysis |
| **Validation** | Claude Code hook pattern (custom impl.) | Post-tool output validation |
| **Delivery** | Hermes Gateway | Results to Telegram, desktop, email |

---

## 2. Agent Role Definitions

### 2.1 Research Orchestrator

```python
orchestrator = Agent(
    role="Power Electronics Research Lead",
    goal="Decompose the inverter design problem, route to specialists, synthesize results",
    model="deepseek-chat",           # Provider-agnostic, cheap for coordination
    tools=["delegate_task"],         # Only needs to spawn subagents
    memory=True,
    system_prompt="""
    You are a senior power electronics research lead. Given a traction inverter
    specification (DC voltage, power rating, topology preference, constraints),
    coordinate a team of specialist agents to:
    1. Review relevant literature for baseline designs
    2. Select components matching the specs
    3. Run MATLAB/Simulink simulations
    4. Analyze simulation results (efficiency, THD, thermal, EMI)
    5. Iterate until efficiency ≥ target or max iterations reached
    6. Generate an IEEE-format research report
    
    Route tasks to the correct specialist. When results are ambiguous, request
    a multi-perspective design review before committing to simulation.
    """
)
```

### 2.2 Literature Agent

```python
literature_agent = Agent(
    role="Power Electronics Literature Reviewer",
    goal="Find state-of-the-art designs, baseline efficiencies, and relevant research",
    model="claude-sonnet-4",        # Best for deep reading and synthesis
    tools=["arxiv_search", "paperqa_query", "web_search", "pdf_read", "datasheet_search"],
    memory=True,                     # Remembers which papers cover which topics
    tool_permissions={
        "arxiv_search": ["all"],     # Read-only — no restrictions needed
        "web_search": ["all"],
        "pdf_read": ["*.pdf"],
        "blocked": ["write", "delete", "execute"]
    }
)
```

**Task → Report contract:**
```python
@dataclass
class LiteratureReport:
    findings: str              # Narrative summary
    key_papers: list[dict]     # [{title, doi, key_finding, relevance}]
    baseline_efficiency: float # Best published efficiency for this voltage class
    topology_recommendations: list[str]
    component_candidates: list[dict]
    confidence: float          # 0.0–1.0
    sources: list[str]         # Citation keys
```

### 2.3 MATLAB Simulation Agent

```python
matlab_agent = Agent(
    role="MATLAB Simulation Engineer",
    goal="Build and run accurate MATLAB/Simulink simulations of power electronic circuits",
    model="deepseek-chat",          # Fast, cheap, good enough for simulation scripts
    tools=["matlab_engine", "simulink_build", "plecs_thermal", "python_analysis"],
    memory=True,                     # Remembers component models, convergence tricks
    tool_permissions={
        "matlab_engine": ["simulate_*", "analyze_*", "plot_*"],
        "simulink_build": ["load_system", "set_param", "sim"],
        "blocked": ["system", "delete", "rmdir"]
    },
    post_tool_hooks=["validate_matlab_output"],  # ← Claude Code pattern
    system_prompt="""
    You are a MATLAB/Simulink expert for power electronics simulation.
    You have access to Simscape Electrical, PLECS, and custom loss models.
    
    CRITICAL RULES:
    - Always validate output files exist before reporting results
    - Check efficiency is in [0, 100]% range
    - Check for NaN/inf in all numeric outputs
    - Set solver to 'ode23tb' for stiff power electronic circuits
    - Use fixed-step solver at 100× switching frequency for FFT analysis
    - Confirm simulation converged before reporting
    """
)
```

**Post-simulation validation hook (Claude Code pattern):**
```python
def validate_matlab_output(tool_result: dict) -> bool:
    """PostToolUse hook — validate MATLAB output before it enters agent context."""
    output_file = tool_result.get("output_file")
    
    checks = {
        "file_exists": os.path.exists(output_file),
        "efficiency_in_range": 0 <= tool_result.get("efficiency", -1) <= 100,
        "no_nan_inf": not any(np.isnan(v) or np.isinf(v) 
                             for v in tool_result.get("waveforms", {}).values()),
        "converged": tool_result.get("converged", False)
    }
    
    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        raise SimulationValidationError(f"Validation failed: {failed}")
    
    return True
```

### 2.4 Reviewer Agent

```python
reviewer_agent = Agent(
    role="Power Electronics Design Reviewer",
    goal="Critically analyze simulation results against specifications and baselines",
    model="claude-sonnet-4",
    tools=["python_analysis", "plot_compare", "baseline_check"],
    memory=False,                    # Each review is independent
    system_prompt="""
    You are a skeptical power electronics design reviewer. For every simulation result:
    1. Compare efficiency against published baselines for the same topology/voltage class
    2. Check THD against IEEE 519 and automotive standards (typically <5%)
    3. Verify thermal margins (Tj_max ≤ 150°C for SiC, ≤ 175°C for Si)
    4. Flag EMI concerns (dv/dt, di/dt rates)
    5. Check component stress (Vds < 80% Vbr_dss, Id < 80% Id_cont)
    6. Identify the single biggest weakness in the design
    
    Be brutally honest. If the design fails any criterion, say so clearly.
    """
)
```

### 2.5 Report Writer

```python
writer_agent = Agent(
    role="IEEE Report Author",
    goal="Compile research findings into a publication-quality IEEE technical report",
    model="gpt-4",                   # Best for structured writing
    tools=["latex_compile", "figure_gen", "bibtex_gen"],
    memory=False,
    system_prompt="""
    You write IEEE-format technical reports for power electronics research.
    Structure: Abstract → Introduction → Topology Selection → Component Sizing →
    Simulation Results → Analysis → Conclusion → References.
    Every claim must cite its source. Every figure must have a caption.
    """
)
```

---

## 3. Workflow State Machine (LangGraph)

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict, Literal

class ResearchState(TypedDict):
    """State that flows through the research workflow."""
    # Input
    spec: dict                      # {Vdc, Pout, topology_pref, constraints}
    
    # Literature
    literature_report: LiteratureReport | None
    baseline_efficiency: float
    
    # Component selection
    selected_components: dict | None  # {switches, gate_drivers, dc_link_cap, sensors}
    
    # Simulation
    simulation_params: dict | None    # {topology, modulation, fs, Vdc, ...}
    simulation_results: dict | None   # {efficiency, thd, losses, thermal, waveforms}
    
    # Analysis
    efficiency_gap: float             # target - achieved
    issues: list[str]                 # Thermal, EMI, THD issues found
    converged: bool
    
    # Iteration
    iteration: int
    max_iterations: int
    
    # Report
    report_path: str | None


def build_research_graph() -> StateGraph:
    workflow = StateGraph(ResearchState)
    
    # Nodes — each delegates to a specialist agent
    workflow.add_node("spec_parse", parse_specification)
    workflow.add_node("literature_review", run_literature_agent)
    workflow.add_node("design_review", run_multi_perspective_review)  # ← AutoGen pattern
    workflow.add_node("component_select", run_literature_agent)       # Reuse lit agent
    workflow.add_node("simulate", run_matlab_agent)
    workflow.add_node("analyze", run_reviewer_agent)
    workflow.add_node("report", run_writer_agent)
    
    # Edges
    workflow.set_entry_point("spec_parse")
    workflow.add_edge("spec_parse", "literature_review")
    workflow.add_edge("literature_review", "design_review")
    workflow.add_edge("design_review", "component_select")
    workflow.add_edge("component_select", "simulate")
    workflow.add_edge("simulate", "analyze")
    
    # Conditional: iterate or conclude
    workflow.add_conditional_edges(
        "analyze",
 lambda state: "report" if state["converged"] or state["iteration"] >= state["max_iterations"] else "replan",
        {"report": "report", "replan": "component_select"}  # Cycle back
    )
    
    workflow.add_edge("report", END)
    
    # Compile with checkpointing (LangGraph pattern)
    checkpointer = SqliteSaver.from_conn_string("research_checkpoints.db")
    return workflow.compile(checkpointer=checkpointer, interrupt_before=["design_review"])
    # ↑ Human-in-the-loop interrupt before committing to simulation (optional)
```

---

## 4. Key Design Decisions

### 4.1 Why Not a Single Agent?

**Decision: Multi-agent with one-level delegation.**

**Rationale:**
- Power electronics research is inherently multi-disciplinary (literature, simulation, analysis, writing)
- Different tasks benefit from different models: deep-reading needs Claude, simulation scripting is fine with DeepSeek, report writing benefits from GPT-4
- Isolating the MATLAB agent's errors (crashes, NaN results) from the orchestrator's context prevents pollution
- Per-agent tool permissions mean the literature agent can't accidentally delete simulation files

**Fallback:** If multi-agent coordination proves unreliable, collapse to a single agent with all tools and a strong system prompt. The LangGraph state machine still runs — just with one agent in every node.

### 4.2 Why LangGraph for Orchestration?

**Decision: LangGraph over CrewAI or custom.**

**Rationale:**
- **Checkpointing is non-negotiable** for expensive simulations — only LangGraph provides this natively
- **Conditional edges** map directly to "iterate or conclude" decisions
- **State persistence** means the workflow survives process restarts — a multi-hour research run across days
- **Human-in-the-loop interrupts** let experts review before committing to 8-hour simulations
- **Subgraphs** enable nested agent workflows (e.g., literature review contains PaperQA2 subgraph)

**Alternative considered:** CrewAI's role-based model is more intuitive but lacks checkpointing. If LangGraph's learning curve proves too steep, CrewAI + external checkpointing (manual state saves) is the fallback.

### 4.3 Why Hermes Agent for Infrastructure?

**Decision: Hermes Agent provides operational infrastructure; LangGraph provides workflow engine.**

**Rationale:**
- **Memory:** Hermes has cross-session persistent memory — research context survives across days
- **Skills:** Domain knowledge (MATLAB debugging procedures, topology selection heuristics) accumulates as reusable skills
- **Cron:** Scheduled literature scans, weekly simulation runs
- **Gateway:** Results delivered to Telegram/desktop — user doesn't need to sit at the terminal
- **Profiles:** Isolate different research projects (traction inverter vs DC-DC converter vs motor control)
- **MIT license:** No restrictions

This is the "Hermes + LangGraph" pairing identified in [[cs/harness/comparative-analysis]].

### 4.4 Per-Agent Model Selection (Claude Code Pattern)

**Decision: Different models for different agent roles.**

| Agent | Model | Why |
|-------|-------|-----|
| Orchestrator | `deepseek-chat` | Cheap, fast, good enough for coordination |
| Literature Agent | `claude-sonnet-4` | Best for deep reading, synthesis, nuanced reasoning |
| MATLAB Agent | `deepseek-chat` | Simulation scripts are mechanical — don't need top reasoning |
| Reviewer Agent | `claude-sonnet-4` | Critical analysis needs best reasoning |
| Report Writer | `gpt-4` | Best structured writing quality |

**Cost optimization:** Only 2 of 5 agents use premium models. The orchestrator and MATLAB agent (highest token volume) use the cheapest model.

---

## 5. Implementation Phases

### Phase 0: Single-Agent Baseline (Week 1-2)
- Build the simplest version: one agent with all tools
- No LangGraph, no delegation — just ReAct loop + MATLAB Engine API
- Goal: prove the concept works end-to-end before adding complexity
- **Acceptance:** Design one inverter from spec to simulation results

### Phase 1: Agent Roles + Tools (Week 3-4)
- Implement the Agent class with role, model, tools, memory, permissions
- Build all 5 agent types with their tool sets
- Implement the task→report contract (smolagents pattern)
- Implement post-tool validation hooks (Claude Code pattern)
- **Acceptance:** Each agent can independently perform its role

### Phase 2: Multi-Agent Orchestration (Week 5-6)
- Implement the orchestrator's `delegate_task` routing
- Build the LangGraph state machine
- Implement checkpointing with SQLite
- Add conditional edges for iteration control
- **Acceptance:** Full research workflow runs from spec to report

### Phase 3: Memory + Skills (Week 7-8)
- Implement entity memory per agent role (CrewAI pattern)
- Build first skills: `matlab-debugging`, `topology-selection`
- Implement multi-perspective design review (AutoGen GroupChat pattern)
- **Acceptance:** Agent remembers component choices across sessions

### Phase 4: Production Hardening (Week 9-10)
- Cron scheduling for automated research runs
- Gateway delivery (Telegram notification on simulation completion)
- Human-in-the-loop interrupts (pause before expensive simulation)
- Profile isolation for multiple research projects
- **Acceptance:** Agent runs autonomously for 24+ hours without intervention

---

## 6. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|:---:|:---:|-----------|
| **Orchestrator routes to wrong agent** | High | Medium | Start with explicit routing (hardcoded edges); add LLM routing only after baseline works |
| **MATLAB Engine API instability** | Medium | High | Checkpoint before every simulation; retry with adjusted solver settings |
| **Context window overflow** | Medium | Medium | Compaction threshold at 70%; store large results in files, not context |
| **Coordination overhead > benefit** | Medium | High | Phase 0 single-agent baseline for comparison; fallback if multi-agent underperforms |
| **Model cost explosion** | Low | High | Per-agent model budgets; orchestrator and MATLAB agent use cheapest models |

---

## 6b. Prior Art Validation (PE-MAS)

The architecture is validated by **PE-MAS** (github.com/spongelovesorange/PE-MAS), a working LangGraph-based multi-agent system for flyback converter design. See [[sources/cs/pe-mas-flyback-mas]] for full analysis.

**Confirmed patterns (PE-MAS implements these successfully):**
- LangGraph StateGraph with 10 agent nodes
- Conditional routing (PASS/FAIL/MAX_ITR)
- Postgres checkpointing with MemorySaver fallback
- Human-in-the-loop interrupts
- Domain guardrails as non-overridable system prompts
- Skills system (manifest.json + prompt.txt + tools.py)
- SQLite lifelong memory with iteration playbooks
- Evidence gates before design release
- Structured state with TypedDict (30+ fields)
- Reasoning traces with confidence scoring

**New patterns from PE-MAS to adopt:**
1. **Plan-then-execute:** `build_execution_plan()` before running the workflow
2. **Best-effort tracking:** Keep the best design candidate across iterations
3. **Correction review:** Post-validation alignment check against original user intent
4. **Iteration playbooks:** Memory of which correction strategies worked for which failure modes
5. **Dual knowledge retrieval:** Keyword scoring + vector index subprocess (our ee/ knowledge could use this)
6. **Evidence grading:** Structured quality scores per evidence dimension

**Key difference:** PE-MAS is flyback/PLECS-specific. SRTP extends the same architecture to traction inverters with MATLAB/Simulink, adds provider-agnostic model selection, and layers on Hermes Agent infrastructure (cron, gateway, cross-session memory).

---

## 7. Success Metrics

| Metric | Target | Measured By |
|--------|--------|------------|
| **Design quality** | Efficiency ≥ published baseline for voltage class | Reviewer agent comparing against literature |
| **Time to first design** | < 2 hours from spec to simulation results | Wall clock |
| **Iterations to convergence** | ≤ 5 iterations (spec → converged design) | LangGraph state counter |
| **Autonomous runtime** | 24+ hours without intervention | Cron job uptime |
| **Checkpoint recovery** | Resume from exact failure point, no lost progress | Integration test |
| **Cost per design** | < $5 in API costs | Token usage tracking |

---

## 8. References

- [[cs/multi-agent-synthesis]] — Full synthesis of multi-agent patterns
- [[cs/harness/comparative-analysis]] — Harness comparison and selection rationale
- [[cs/harness/langgraph]] — LangGraph state machine engine
- [[cs/harness/hermes-agent]] — Operational infrastructure (memory, skills, cron)
- [[cs/harness/claude-code]] — Hooks, permissions, subagent patterns
- [[cs/harness/crewai]] — Role-based agent definition and entity memory
- [[cs/harness/matlab-integration]] — MATLAB Engine API integration strategy
- [[citations]] — [1][2] Hermes Agent, [3][4] Claude Code, [7][8] LangGraph, [9] CrewAI, [10] AutoGen, [12] smolagents

---

← [[cs/multi-agent-synthesis|Research Synthesis]] | [[implementation/plans/architecture|Architecture Decision Record]] →
