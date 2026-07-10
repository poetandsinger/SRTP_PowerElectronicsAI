---
title: "Implementation Research: Building a Multi-Agent System for Traction Inverter Design"
type: topic
field: cs
created: 2026-07-10
updated: 2026-07-10
status: unverified
evidence: single-study
tags: [cs, multi-agent, implementation, architecture, integration, traction-inverter, design-automation]
sources:
  - cs/traction-inverter-mas-integration
  - cs/multi-agent-synthesis
  - sources/cs/pe-mas-flyback-mas
  - sources/cs/hybrid-langgraph-crewai-2026-ieee
  - sources/cs/agentic-tcad-2026-date
  - sources/cs/drcy-2026-allspice-mas-review
  - sources/cs/ltspice-mcp-2026
  - sources/cs/langgraph-production-gaps-2026-diagrid
review_by: 2026-08-10
---

# Implementation Research: Building a Multi-Agent System for Traction Inverter Design

**This note translates the integration architecture into implementable engineering decisions.** Every technology choice is sourced and justified. Where we don't know something, it's marked as a gap with a research plan.

---

## 1. Technology Stack Decisions (Verified)

### 1.1 Simulation Backend: Dual-Engine Strategy

**Decision:** MATLAB/Simulink (system-level) + PySpice/ngspice or ltspice-mcp (device-level)

**Evidence:**
- **MATLAB Engine API for Python** is mature and documented. Key capabilities from MathWorks docs (verified):
  - `matlab.engine.start_matlab()` — start session
  - `eng.sim('model_name')` — run Simulink
  - `eng.set_param('model', 'SimulationCommand', 'pause/continue/stop')` — runtime control
  - `eng.load_system()`, `eng.set_param()` — programmatic model building
  - Install: `pip install matlabengine` (PyPI) or from `matlabroot/extern/engines/python/`
  - **Gap:** Requires MATLAB license. Academic ~$500/yr, commercial ~$10-20K/yr
  
- **PySpice + ngspice** (verified via SEPOC 2025 LLC converter framework): Production-ready for power converter design with automated frequency search, multi-operating-point testing, parallel batch simulation, and steady-state detection. Free (GPLv3).

- **ltspice-mcp** (cloned 2026-07-10, verified): 51 MCP tools including transient, AC, DC, Monte Carlo, THD, Bode analysis. Compatible with Claude natively via MCP protocol. GPL-3.0 license.

**Implementation strategy:**
1. Phase 0-1: PySpice + ngspice (free, no license dependency, works immediately)
2. Phase 2+: MATLAB Engine API (when MATLAB license available)
3. Phase 3+: ltspice-mcp for device-level verification (gate drive, snubber, EMI filter)

**Fallback:** If MATLAB is unavailable, the entire system-level simulation can run on PySpice + ngspice. The LLC converter framework (SEPOC 2025) proves this is viable for power converters. The limitation is motor models (PMSM, IPMSM) — ngspice has no native motor library. Workaround: behavioral motor model in SPICE or external Python motor model coupled to SPICE inverter model.

### 1.2 LLM Provider Strategy

**Decision:** Provider-agnostic with complexity-based routing

**Evidence from research:**
- AgentSlimming (ACL 2026): Reduces token cost up to 78.9% by compressing multi-agent workflows
- SCALE (ACL 2026): Task-level workflow generation reduces token usage up to 83% vs query-level
- SlowBurn: Dollar-denominated backpressure for budget enforcement
- Q-planner (ChemRxiv 2026): 95% token reduction by confining LLM to planning stages only

**Implementation:**
```python
# Complexity-based routing
MODEL_ROUTING = {
    "orchestration": "deepseek-chat",      # Cheap, fast coordination
    "literature_review": "claude-sonnet",   # Deep reading needs best reasoning
    "topology_selection": "claude-sonnet",  # Critical design decision
    "component_selection": "deepseek-chat", # Mechanical search, cheap model OK
    "simulation_scripting": "deepseek-chat",# Mechanical code generation
    "thermal_analysis": "deepseek-chat",    # Running CFD-ROM scripts
    "design_review": "claude-sonnet",       # Critical analysis needs best reasoning
    "report_writing": "gpt-4",             # Best structured writing
}
```

**Token budget strategy (SlowBurn pattern):**
- Per-design budget: $5 (target from success metrics)
- Backpressure: pause agents when budget at 80%, don't crash
- Task-level workflow generation (SCALE pattern): plan all steps, execute deterministically where possible

### 1.3 Orchestration Engine

**Decision:** LangGraph StateGraph with SQLite checkpointing

**Evidence:**
- Hybrid LangGraph-CrewAI (IEEE Access 2026): 96.1% success rate, validated pattern
- PE-MAS: Working LangGraph implementation for power electronics
- Osprey Framework: Production LangGraph at Berkeley Lab

**Critical gap (Diagrid, Feb 2026):** LangGraph checkpointing saves state but does NOT auto-resume. We need:
1. Watchdog process: poll for stuck graphs (no state transition in > T_timeout)
2. Idempotency keys: hash(simulation_parameters) to prevent duplicate execution
3. Manual resume workflow: human-in-the-loop fallback

**Implementation:**
```python
import hashlib
from langgraph.checkpoint.sqlite import SqliteSaver

# Idempotency for simulation runs
def simulation_idempotency_key(params: dict) -> str:
    """Prevent duplicate simulation runs."""
    canonical = json.dumps(params, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]

# Watchdog for stuck graphs
def watchdog_check(checkpointer, timeout_minutes=30):
    """Poll for graphs stuck with no state transition."""
    stuck = checkpointer.find_stuck_graphs(since=timeout_minutes)
    for graph_id in stuck:
        logger.warning(f"Graph {graph_id} stuck — attempting resume")
        resume_graph(graph_id)
```

### 1.4 Component Database

**Decision:** Nexar/Octopart GraphQL API (primary) + DigiKey API (ordering/BOM)

**Evidence (verified 2026-07-10):**
- **Nexar GraphQL API:** `https://api.nexar.com/graphql` — covers 30+ distributors in one query. Free tier: ~1,000 queries/month. OAuth 2.0 client credentials. Key queries: `supSearch`, `supSearchMpn`, `supParts`.
- **DigiKey API:** RESTful OAuth 2.0. Python SDK: `pip install digikey-api`. Endpoints: Part Search, Price & Availability, BOM Upload & Match.
- **DigiKey MCP Server:** Exists (FastMCP-based) — keyword search, product details, pricing, manufacturer/category search.
- **Octopart MCP Server:** Exists (LobeHub) — specialized tools for resistors, capacitors, inductors, semiconductors, connectors.

**⚠️ Critical finding:** Octopart's public web UI is now PerimeterX (PX) bot-walled. The ONLY programmatic path is the Nexar GraphQL API. REST API v1-v4 is deprecated.

**Implementation:**
```python
# Nexar GraphQL query for component search
import requests

def search_components(keyword: str, limit: int = 10) -> list[dict]:
    query = """
    query SearchComponents($keyword: String!, $limit: Int!) {
      supSearch(q: $keyword, limit: $limit) {
        results {
          part {
            mpn
            manufacturer { name }
            category { name }
            medianPrice1000 { price currency }
            specs { attribute displayValue }
          }
        }
      }
    }
    """
    # OAuth2 token from https://identity.nexar.com/connect/token
    headers = {"Authorization": f"Bearer {get_nexar_token()}"}
    response = requests.post("https://api.nexar.com/graphql", 
                            json={"query": query, "variables": {...}},
                            headers=headers)
    return response.json()
```

### 1.5 Literature Review

**Decision:** PaperQA2 (primary) + arXiv API (supplementary)

**Evidence (verified 2026-07-10):**
- **PaperQA2** (Future-House, GitHub): `pip install paper-qa>=5`. Superhuman performance on scientific QA. Three-phase algorithm: Paper Search → Gather Evidence → Generate Answer (with citations).
- Supports Claude, GPT, Gemini, local models via LiteLLM (200+ providers)
- Bundled settings: `high_quality`, `fast`, `wikicrow`, `contracrow`
- Sync and async APIs: `Docs.add()`, `Docs.aquery()`, `Docs.get_evidence()`
- Key settings: `evidence_k=8`, `answer_max_sources=4`, `search_count=6`
- **PaperPipe** wrapper: `papi ask "Compare topologies"` — unified paper database

### 1.6 Memory Architecture

**Decision:** SQLite (structured) + LanceDB (vector) dual-store

**Evidence:**
- PE-MAS: SQLite for design records, quality scoring, iteration playbooks
- CrewAI (verified v0.80+): LanceDB for unified LLM-analyzed memory with composite scoring (recency 30% + semantic 50% + importance 20%)

**Implementation:**
```python
# Dual memory store
class MemoryStore:
    def __init__(self):
        self.structured = sqlite3.connect("srtp_memory.db")  # Design records, specs, results
        self.vector = lancedb.connect("srtp_vectors")         # Semantic search for papers, components
```

### 1.7 Guardrails & Evidence Gates

**Decision:** PE-MAS pattern: hard guardrails as non-overridable system prompts, evidence gates as post-simulation validation

**7 Domain Guardrails (from integration architecture):**
1. Safety: Tj ≤ 150°C (Si) / 175°C (SiC) with ≥25°C margin
2. Voltage: Vds ≤ 80% Vbr_dss; DC-link cap ≥ 1.2× Vdc_max
3. Current: Id_cont ≤ 80% rated
4. Physical realism: Efficiency < 100%; flag >99% as suspicious
5. Duty cycle: MI in achievable range for topology
6. Thermal consistency: P_loss(elec) ≈ ΔT/Rth(thermal) within 10%
7. Standards: Flag CISPR 25, ISO 26262, IEC 61800-5-1 violations

**8 Evidence Gates (before design release):**
1. Efficiency ≥ baseline for voltage class at 3+ operating points
2. Thermal: Tj ≤ Tj,max − 25°C at worst case
3. THD ≤ 5% at rated power
4. EMI: dv/dt ≤ 30 kV/µs pre-compliance check
5. Component stress: all within derated limits
6. Standards: no flagged violations
7. Cost: BOM within 20% of baseline
8. Human signoff: design review package presented

### 1.8 Multi-Run Consensus (DRCY Pattern)

**Decision:** Run Reviewer Agent 3× independently, reconcile with consensus step

**Evidence:** DRCY (AllSpice, production at Fortune 500): k separate reviews → consensus agent reconciles. Multi-run findings get higher confidence. Single-run findings critically evaluated.

**Implementation:**
```python
async def multi_run_review(design: dict, k: int = 3) -> ReviewResult:
    reviews = await asyncio.gather(*[reviewer_agent.review(design) for _ in range(k)])
    consensus = consensus_agent.reconcile(reviews)
    consensus.confidence = sum(1 for r in reviews if r.matches(consensus)) / k
    return consensus
```

---

## 2. Open Research Gaps (Needs Investigation)

### G1: SPICE motor model fidelity
- **Problem:** PySpice/ngspice has no native PMSM/IPMSM model. MATLAB/Simscape has built-in motor blocks. 
- **Impact:** If we rely on PySpice (no MATLAB), we need a behavioral motor model in SPICE or external Python motor model.
- **Research plan:** Build a dq-frame motor model in Python, couple to PySpice inverter model via co-simulation. Validate against Simscape PMSM block.

### G2: Surrogate model training data
- **Problem:** DNN+NSGA-III cooling optimization (2025) needed CFD simulations to train. How many simulations do we need for a useful surrogate?
- **Impact:** If 1000+ simulations needed, Phase 0-3 can't build surrogates.
- **Research plan:** Literature review on minimum training data for power electronics surrogates. Start with analytical models (no training data needed) and upgrade to ML surrogates as simulation data accumulates.

### G3: MATLAB license availability
- **Problem:** MATLAB license may not be available. Academic license ~$500/yr, commercial ~$10-20K/yr.
- **Impact:** Architecture assumes MATLAB; Phase 0 may need to run entirely on open-source.
- **Mitigation:** PySpice + ngspice as primary in Phase 0-1. MATLAB Engine API as upgrade path in Phase 2+.

### G4: Evaluation benchmark
- **Problem:** No standard benchmark exists for traction inverter design quality.
- **Impact:** Can't objectively measure if our system is good.
- **Research plan:** Create a benchmark: 3-5 traction inverter specs with published reference designs. Measure: efficiency, THD, thermal margin, BOM cost vs reference. Publish as open benchmark.

### G5: LLM performance on SPICE netlist generation
- **Problem:** LLMs are good at Python/Verilog code. Unknown performance on SPICE netlist generation.
- **Impact:** If LLMs can't generate correct SPICE netlists, the simulation loop breaks.
- **Research plan:** Test Claude, GPT-4, DeepSeek on generating SPICE netlists for basic power stages (buck, boost, 3-phase inverter). Measure: syntax errors, simulation convergence, electrical correctness.

---

## 3. Architecture Decisions (Record)

### A1: Code-first, not GUI-first for Phase 0
- **Rationale:** The Phase 0 plan (2026-07-09) starts with PySide6 GUI. This is wrong. The minimum viable product is a Python script that takes a spec and produces a simulation result. GUI comes after the agent works.
- **Decision:** Phase 0 = CLI + Python API. GUI starts in Phase 3+.

### A2: Start with 3 agents, not 7
- **Rationale:** EvoAgent (NAACL 2025) shows human-designed roles may be suboptimal. The integration architecture claims 7 agents at C2 confidence. Start with 3 (Orchestrator, MATLAB, Reviewer) and add specialists only when needed.
- **Decision:** Phase 1-2: 3 agents. Phase 3+: add Literature, Component, Thermal, Topology as demonstrated need.

### A3: PySpice first, MATLAB optional
- **Rationale:** PySpice is free, open-source, Python-native, and proven for power converters (SEPOC 2025). Zero license dependency. MATLAB is better for motor drives but adds cost and deployment complexity.
- **Decision:** Phase 0-1: PySpice + ngspice. Phase 2+: add MATLAB Engine API as optional backend. The agent should work with either backend.

### A4: LangGraph + SQLite, not Postgres
- **Rationale:** PE-MAS uses Postgres. For a research project (not 24/7 production), SQLite is sufficient and simpler. SQLite supports the LangGraph SqliteSaver natively.
- **Decision:** SQLite for Phase 0-3. Migration path to Postgres if production deployment needed.

### A5: Provider-agnostic with LiteLLM
- **Rationale:** PaperQA2 uses LiteLLM for 200+ provider compatibility. This matches our provider-agnostic requirement perfectly.
- **Decision:** Use LiteLLM as the unified LLM interface. Route per model complexity as defined in §1.2.

---

## 4. Technology Stack (Final)

| Component | Technology | License | Why |
|-----------|-----------|---------|-----|
| **Simulation (primary)** | PySpice + ngspice | GPLv3 | Free, Python-native, proven for power converters |
| **Simulation (upgrade)** | MATLAB Engine API | MathWorks | Industry standard for traction drives |
| **Device-level sim** | ltspice-mcp (MCP server) | GPL-3.0 | 51 tools, native Claude integration |
| **Orchestration** | LangGraph StateGraph | MIT | 96.1% success in hybrid architecture, checkpointing |
| **Agent framework** | Custom Python + LiteLLM | MIT | Provider-agnostic, pattern-matched to 7 harnesses |
| **LLM (coordination)** | deepseek-chat | — | Cheap, fast coordination |
| **LLM (reasoning)** | claude-sonnet | — | Best for deep analysis |
| **LLM (writing)** | gpt-4 | — | Best structured output |
| **Literature** | PaperQA2 | Apache 2.0 | Superhuman scientific QA, citation-grounded |
| **Components** | Nexar GraphQL API | Free tier | 30+ distributors, cross-reference |
| **Memory** | SQLite + LanceDB | Public Domain + Apache 2.0 | Structured + vector dual-store |
| **Checkpointing** | LangGraph SqliteSaver | MIT | Built-in, sufficient for research |
| **Token budget** | SlowBurn pattern | MIT | Dollar-denominated backpressure |
| **Consensus** | DRCY multi-run pattern | — | k=3 independent reviews + reconciliation |
| **CLI** | Click + Rich | BSD + MIT | Python-native CLI with rich formatting |

---

## 5. What We're NOT Building (Yet)

| Feature | Why Deferred |
|---------|-------------|
| **PySide6 GUI** | Phase 0 should validate the agent, not the UI. CLI first. |
| **Simulink model builder** | Too complex for Phase 0-2. Start with PySpice netlist generation. |
| **Visual schematic editor** | Phase 3+ stretch goal. KiCad integration is simpler. |
| **Cron scheduling** | Phase 4+. Not needed until agent works reliably. |
| **Gateway delivery (Telegram)** | Phase 4+. CLI output is sufficient for Phase 0-3. |
| **Thermal Agent** | Phase 3+. MATLAB/Reviewer agent can handle basic thermal checks. |
| **Topology Agent** | Phase 3+. Orchestrator + Literature can handle topology selection initially. |
| **Surrogate models** | Phase 4+. Need simulation data corpus first. |

---

## 6. Key Risks (Updated from 2026-07-09)

| Risk | Prob. | Impact | Mitigation |
|------|:-----:|:------:|-----------|
| **MATLAB unavailable** | Medium | High | PySpice primary. MATLAB optional upgrade. |
| **LLMs can't generate SPICE netlists** | Medium | Critical | Template-based generation (HAVEN pattern), not raw LLM. Test in Phase 0. |
| **Coordination overhead > benefit** | Medium | High | Start with 3 agents, not 7. A/B test vs single agent in Phase 0. |
| **Simulation time dominates** | High | Medium | Analytical models for rapid screening. Surrogate models in Phase 4. |
| **LangGraph checkpoint gaps** | Medium | Medium | Watchdog process + idempotency keys + manual resume. |
| **Nexar API rate limits** | Low | Low | 1,000 queries/month free tier; components don't change often. Cache aggressively. |
| **Evaluation benchmark missing** | High | Medium | Build benchmark in Phase 0. 3-5 specs with published reference designs. |

---

> **References:** [[cs/traction-inverter-mas-integration]], [[cs/multi-agent-synthesis]], [[sources/cs/pe-mas-flyback-mas]], [[citations]]
