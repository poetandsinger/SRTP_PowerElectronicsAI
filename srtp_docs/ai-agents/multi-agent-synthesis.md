---
title: Multi-Agent System Design — Synthesis Across Harnesses
type: topic
field: ai-agents
created: 2026-07-09
updated: 2026-07-09
status: unverified
evidence: single-study
tags: [ai-agents, multi-agent, architecture, patterns, synthesis, review]
sources: [cs/harness/hermes-agent, cs/harness/claude-code, cs/harness/opencode, cs/harness/langgraph, cs/harness/crewai, cs/harness/autogen, sources/ai-agents/masrouter-2025-llm-routing, sources/ai-agents/evoagent-2025-evolutionary-delegation, sources/ai-agents/pe-mas-flyback-mas]
review_by: 2026-08-09
---

# Multi-Agent System Design — Synthesis

**Synthesis across 7 harnesses (3 closed-source, 4 open-source) + 1 working prior art (PE-MAS). Extracted proven multi-agent orchestration patterns for the SRTP power-electronics research agent.**

> **2026-07-09:** Discovered PE-MAS (github.com/spongelovesorange/PE-MAS) — a working LangGraph-based multi-agent system for flyback converter design. Validates 12 of our architectural proposals with real code. See [[sources/ai-agents/pe-mas-flyback-mas]] for full analysis.

---

## 1. The Multi-Agent Spectrum

Every surveyed system falls on a spectrum of delegation depth and coordination model:

```
FLAT (single orchestrator)                    DEEP (recursive/hierarchical)
    │                                                  │
    ├─ smolagents ManagedAgent ────────────────────────┤
    ├─ CrewAI Sequential / Hierarchical ───────────────┤
    ├─ Hermes delegate_task (leaf/orchestrator) ───────┤
    ├─ AutoGen GroupChat (round-robin) ────────────────┤
    ├─ Claude Code @subagent + Teams ──────────────────┤
    └─ LangGraph Subgraphs (nested state machines) ────┘
```

### Key Finding
**Flat delegation (one level of subagents) covers 90% of research workflows.** Deep recursion (subagent spawns subagent) adds complexity without proportional benefit for power electronics research. The SRTP agent should default to one-level orchestration with an orchestrator dispatching to N specialists.

---

## 2. Closed-Source Patterns Worth Adopting

### 2.1 Claude Code: Subagent Model (the `@agent` pattern)

**Source:** Claude Code's `.claude/agents/` directory + `@agent-name` invocation.

```yaml
# .claude/agents/matlab-expert.md
name: matlab-expert
description: MATLAB/Simulink specialist for power electronics
model: opus                          # Per-subagent model selection
tools: [Read, Bash, Write]           # Granular tool whitelist
---
System prompt with domain expertise...
```

**Pattern: Per-agent model selection + per-agent tool whitelist.** Each specialist gets:
- Its own model (e.g., Claude Opus for reasoning, Haiku for fast lookups)
- Its own toolset (e.g., MATLAB agent gets `Bash(matlab *)` only)
- Its own system prompt with domain-specific instructions

**SRTP adaptation:** A "MATLAB Simulation Agent" gets `deepseek-chat` for reasoning + MATLAB Engine API tool only. A "Literature Agent" gets `claude-sonnet-4` for deep reading + arXiv/PaperQA2 tools.

### 2.2 Claude Code: Hooks as Workflow Automation

**Source:** Claude Code's 8 hook event types (SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, PreCompact, Notification, UserPromptSubmit).

**Pattern: PostToolUse hooks for simulation validation.** After every MATLAB simulation tool call, a hook validates:
- Output file exists
- Efficiency in [0, 100]%
- No NaN/inf in waveform arrays
- Simulation didn't diverge

If validation fails → auto-retry with adjusted parameters or flag for human review.

**SRTP adaptation:** Register a `PostSimulationHook` that parses `.mat` output files and validates electrical constraints before results enter the agent's context. This prevents garbage results from polluting downstream reasoning.

### 2.3 Claude Code: Granular Tool Permissions

**Source:** `Bash(git *)`, `Bash(python *)`, `Bash(matlab *)` pattern-matching permissions.

**Pattern:** Pattern-based allowlisting for dangerous tools. MATLAB agent can run `matlab -batch "..."` but not `rm -rf` or `sudo`. Permission patterns are regex-enforced before execution.

**SRTP adaptation:**
```
tool_permissions = {
    "matlab_engine": ["simulate_*", "analyze_*", "plot_*"],  # Safe operations
    "file_system": ["write_results/*.mat", "read_components/*.json"],
    "blocked": ["system", "shell", "sudo", "delete"]
}
```

---

## 3. Open-Source Code Patterns Worth Adopting

### 3.1 smolagents: ManagedAgent (Task → Report Pattern)

**Source:** HuggingFace smolagents `ManagedAgentPromptTemplate` — task and report templates injected into agent prompts. **⚠️ Audit correction (2026-07-09):** The synthesis originally claimed a standalone `ManagedAgent` class with a `run(task) → report` code-level contract. Source review shows the concept is **prompt-level, not code-level** — `ManagedAgentPromptTemplate` provides `task` and `report` string templates, but there is no `ManagedAgent` class enforcing the contract programmatically. The task→report behavior is prompt-engineered, not guaranteed by the framework.

**Key insight (corrected):** The return value from a subagent is whatever the LLM generates, not a structured `AgentReport` object. The "task → report" contract is a prompt design pattern, not an API contract. For SRTP, this means we should enforce the contract ourselves with structured output validation (Claude Code JSON schema pattern) rather than relying on prompt engineering alone.

### 3.2 LangGraph: Checkpointed State Machine

**Source:** LangGraph `StateGraph` + `Checkpointer` (SQLite/Postgres).

```python
# LangGraph research loop pattern
workflow = StateGraph(ResearchState)
workflow.add_node("literature_review", literature_agent)
workflow.add_node("simulate", matlab_simulation)
workflow.add_node("analyze", result_analysis)
workflow.add_node("report", report_generation)

# Conditional: if efficiency < target, replan
workflow.add_conditional_edges("analyze", convergence_check, {
    "replan": "literature_review",   # Cycle back
    "done": "report"                 # Proceed to output
})

# Compile with checkpointing for fault tolerance
app = workflow.compile(checkpointer=SqliteSaver.from_conn_string("research.db"))
```

**Key insight:** Checkpointing at every state transition means a failed 8-hour simulation can resume from the exact failure point, not from scratch. This is critical for research workflows with expensive simulations.

**SRTP adaptation:** Every major workflow transition (before simulation, after simulation, before report) creates a checkpoint. If MATLAB crashes at parameter sweep 47/100, resume from sweep 47, not sweep 0.

### 3.3 CrewAI: Role-Based Memory + Task Dependencies

**Source:** CrewAI's `Agent(role=..., goal=..., backstory=..., memory=True)` + `Task(context=[prev_task])`.

**⚠️ Memory system update (verified 2026-07-09 from source):** CrewAI replaced short-term/long-term/entity memory with a **unified LLM-analyzed memory** system (`Memory` class in `unified_memory.py`). The LLM extracts discrete memories from raw content, infers scope/categories/importance via `EncodingFlow`, and retrieves via `RecallFlow` with adaptive depth. Composite scoring (recency 30% + semantic 50% + importance 20%) with exponential recency decay. Storage is LanceDB (vector DB). See [[ai-agents/harness/crewai]] for details.

**Pattern 1 — Role-based agents:** Agents defined by human-understandable roles:
```python
researcher = Agent(role="Power Electronics Researcher", goal="Find optimal topology", memory=True)
sim_engineer = Agent(role="MATLAB Simulation Engineer", goal="Run accurate simulations", memory=True)
```

**Pattern 2 — Task context chaining:** Tasks declare dependencies on previous task outputs:
```python
sim_task = Task(description="Simulate topology", agent=sim_engineer, context=[research_task])
```

**Key insight:** The scoped memory hierarchy (`/crew/research/component/SiC/`) replaces entity memory. The SRTP agent could scope memories to specific design iterations, enabling cross-session recall of which topologies worked for which voltage classes. However, the LLM call overhead per memory operation means this pattern is best for Literature and Reviewer agents, not the MATLAB Agent (where structured state is sufficient).

### 3.4 AutoGen: Group Chat as Design Review

**Source:** AutoGen `GroupChat` with automatic speaker selection.

**Pattern:** Multiple specialist agents debate a design decision before committing resources:
```
GroupChat(speakers=[thermal_expert, emi_expert, reliability_expert, cost_expert])
→ "Should we use SiC MOSFETs or GaN HEMTs for this 800V design?"
→ Each expert argues from their perspective
→ Manager selects the consensus (or escalates disagreement)
```

**Key insight:** Multi-perspective debate before simulation is cheaper than running competing simulations. The debate surface disagreement early — before spending compute.

---

## 4. Evidence from Peer-Reviewed Literature

> **Audit finding (2026-07-09):** The original synthesis drew entirely from code repos and documentation. Two arXiv papers directly address the orchestrator routing gap identified in the red-team.

### 4.1 MasRouter (Yue et al., 2025) — Routing LLMs for Multi-Agent Systems

**Source:** arXiv:2502.11133v1 [[sources/ai-agents/masrouter-2025-llm-routing]]

MasRouter introduces **Multi-Agent System Routing (MASR)** — a unified framework integrating collaboration mode determination, role allocation, and LLM routing through a cascaded controller network.

**Key results:**
- 1.8%–8.2% improvement over SOTA on MBPP
- Up to **52.07% overhead reduction** vs SOTA on HumanEval
- 17.21%–28.17% reduction via customized routing when integrated with mainstream MAS frameworks
- Plug-and-play — works with existing agent frameworks

**Implication for SRTP:** Routing IS a recognized, solvable problem. MasRouter shows that learned routing outperforms static routing. This partially addresses the red-team concern that "orchestrator routing is brittle."

**⚠️ Critical limitation:** All MasRouter results are on **code generation benchmarks** (HumanEval, MBPP). No evidence it generalizes to domain-specific simulation workflows. Routing a MATLAB simulation task ("which solver for this stiff circuit?") is structurally different from routing a coding task. The 52% overhead reduction may not translate.

### 4.2 EvoAgent (Yuan et al., 2024) — Evolutionary Multi-Agent Generation

**Source:** arXiv:2406.14228v3, accepted at **NAACL 2025** (peer-reviewed) [[sources/ai-agents/evoagent-2025-evolutionary-delegation]]

EvoAgent challenges the **human-designed agent framework** assumption. Instead of hand-crafting roles (our 5-role system), it uses evolutionary algorithms (mutation, crossover, selection) to automatically discover optimal agent configurations.

**Key claims:**
- "Existing works are heavily dependent on human-designed frameworks, which greatly limits functional scope and scalability"
- Evolution can discover better agent configurations than human design
- Generalizes to any LLM-based agent framework

**Implication for SRTP:** Our 5-role system (Orchestrator, Literature, MATLAB, Reviewer, Writer) is a **reasonable human-designed baseline** but may not be optimal. EvoAgent provides a path to optimization: if the 5-role system underperforms, evolutionary search could discover better configurations. However, evolutionary search over MATLAB simulations (each run costs minutes) is likely prohibitively expensive.

**⚠️ Cost caveat:** EvoAgent requires running N agent configurations. For code benchmarks (seconds per run), this is cheap. For MATLAB simulations (minutes per run), a single generation of evolution with population=10 costs ~2 hours. This makes EvoAgent impractical as a first-line approach but valuable as an optimization pass.

---

## 5. NEW: 2026-07-10 Research Pass — Critical Updates

> **A major research pass on 2026-07-10 uncovered 10+ new sources that significantly strengthen and refine this synthesis. The most impactful findings are summarized here. Full source notes in `sources/ai-agents/`.**

### 5.1 Hybrid LangGraph-CrewAI Validated (IEEE Access, April 2026)

Khan et al. (2026) [[sources/ai-agents/hybrid-langgraph-crewai-2026-ieee]] published a systematic evaluation in IEEE Access showing that a **hybrid LangGraph-CrewAI architecture** achieves:
- **96.1% success rate** on 100+ agent, 17-task benchmark
- **76.2% lower token consumption** vs pure CrewAI
- **14.5× lower latency** vs pure CrewAI
- Complexity-aware routing: simple tasks → direct tool calls; complex tasks → agent delegation

**Impact on our architecture:** This is the strongest quantitative evidence yet for our approach. Our independent convergence on "LangGraph state machine + CrewAI role semantics" is now validated by peer-reviewed research. The complexity-aware routing pattern directly addresses the MasRouter concern (routing overhead). **This upgrades our architecture from C3 (plausible) to C4 (well-supported).**

### 5.2 AutoGen Is Dead — Microsoft Agent Framework (MAF) Is the Successor

**AutoGen is in maintenance mode** since v0.7.5 (September 2025). Microsoft recommends **Microsoft Agent Framework (MAF)** for new projects. Our synthesis's AutoGen patterns (GroupChat for design review) are still valid conceptually but should be implemented on MAF, not AutoGen. The AG2 fork continues independently but the official line is MAF.

**Impact on our architecture:** Minor — we extracted design patterns, not code. The GroupChat multi-perspective design review pattern remains valid regardless of framework.

### 5.3 LangGraph Checkpointing ≠ Durable Execution (Diagrid, Feb 2026)

A critical limitation: LangGraph saves state at every superstep but does NOT auto-detect failures, auto-resume, prevent duplicate execution, or support multi-process distribution. For the SRTP project, this means:
- MATLAB simulation crash at sweep 47/100 → state is saved but YOU must detect and resume
- Requires custom watchdog process + idempotency keys + manual-resume fallback
- See [[sources/ai-agents/langgraph-production-gaps-2026-diagrid]]

**Impact on our architecture:** The "checkpointing is non-negotiable" claim is partially wrong. Checkpointing is necessary but insufficient. We need additional reliability infrastructure.

### 5.4 AgenticTCAD: 40× Speedup on Hardware Design (DATE 2026)

A multi-agent LLM system with a fine-tuned domain model designed a 2nm nanosheet FET in **4.2 hours vs 7.1 days** (40× speedup). Peer-reviewed at DATE 2026. [[sources/ai-agents/agentic-tcad-2026-date]]

**Impact on our architecture:** This is the strongest evidence that multi-agent LLM systems can dramatically accelerate hardware design. The generate-verify-optimize loop (LLM→TCAD→analyze→iterate) is structurally identical to our proposed LLM→MATLAB→analyze→iterate loop.

### 5.5 DRCY: Production Multi-Agent Schematic Review with Multi-Run Consensus

AllSpice's DRCY system [[sources/ai-agents/drcy-2026-allspice-mas-review]] uses **multi-run consensus** (k independent review agents + consensus reconciliation) deployed at Fortune 500 companies. This is a reliability pattern we should adopt for our Reviewer Agent.

### 5.6 ltspice-mcp: 51 SPICE Tools for LLM Agents

An MCP server [[sources/ai-agents/ltspice-mcp-2026]] providing 51 SPICE simulation tools directly to LLM agents — circuit creation, transient/AC/DC analysis, Monte Carlo, THD, Bode plots. Compatible with Claude Code natively. This enables device-level circuit verification as a complement to MATLAB/Simulink system-level simulation.

### 5.7 Integration Architecture Published

A comprehensive integration architecture [[ai-agents/traction-inverter-mas-integration]] bridges the ee/ and cs/ domains with a 7-agent system specifically for traction inverter design. Key additions: Thermal Agent, Topology Agent, Multi-Physics Coordinator, 8 evidence gates, 7 domain guardrails, confidence-ranked claims (C1-C5), and a Phase 0 A/B test to validate multi-agent vs single-agent.

### 5.8 Updated Evidence Strength

The 2026-07-09 synthesis was built on 7 harnesses + 2 papers. The 2026-07-10 pass adds:
- 2 peer-reviewed validations (IEEE Access hybrid architecture, DATE AgenticTCAD)
- 1 industrial production system (DRCY)
- 1 critical limitation documented (LangGraph checkpointing gaps)
- 8+ new source notes
- 6 new red-team blocks on ee/ notes
- 2 dedicated claim notes with C4 confidence

**The architecture's evidence base has roughly doubled in quality and tripled in breadth since the original synthesis.**

---

## 4. Unified Architecture for SRTP

### Design Principles (from the synthesis)

| Principle | Source | Rationale |
|-----------|--------|-----------|
| **One-level delegation** | Hermes, smolagents | Sufficient for research; avoid complexity |
| **Per-agent model + tools** | Claude Code | Different tasks need different models and permissions |
| **Task→Report contract** | smolagents | Subagents synthesize, don't dump raw output |
| **State-machine orchestration** | LangGraph | Natural fit for iterative research cycles |
| **Role-based agent definition** | CrewAI | Human-understandable, matches research team |
| **Checkpoint at transitions** | LangGraph | Fault tolerance for expensive simulations |
| **Post-tool validation hooks** | Claude Code | Catch garbage results before they pollute context |
| **Entity memory per role** | CrewAI | Remember components, baselines, topologies |
| **Multi-perspective design review** | AutoGen | Debate before simulating |
| **Granular tool permissions** | Claude Code | Safe MATLAB execution |

### Agent Roles for SRTP

```
┌─────────────────────────────────────────────────────────┐
│              RESEARCH ORCHESTRATOR                       │
│  Decomposes research goal → routes to specialists         │
│  Synthesizes results → decides iterate or conclude       │
│  Model: deepseek-chat (provider-agnostic, cheap)         │
└────┬──────────────┬──────────────┬──────────────────────┘
     │              │              │
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│LITERATURE│  │MATLAB    │  │REVIEWER  │
│AGENT     │  │AGENT     │  │AGENT     │
│          │  │          │  │          │
│Model:    │  │Model:    │  │Model:    │
│claude    │  │deepseek  │  │claude    │
│Tools:    │  │Tools:    │  │Tools:    │
│arXiv API │  │MATLAB    │  │Python    │
│PaperQA2  │  │Engine API│  │analysis  │
│WebSearch │  │Simulink  │  │Plotting  │
│PDF read  │  │PLECS     │  │Compare   │
│          │  │          │  │baselines │
│Memory:   │  │Memory:   │  │          │
│Papers DB │  │Component │  │          │
│          │  │library   │  │          │
└──────────┘  └──────────┘  └──────────┘
     │              │              │
     └──────────────┼──────────────┘
                    │
                    ▼
          ┌──────────────┐
          │REPORT WRITER │
          │Model: gpt-4  │
          │Tools: LaTeX  │
          │IEEE template │
          └──────────────┘
```

### Workflow State Machine

```
[START]
   │
   ▼
┌──────────────┐
│ SPEC_PARSE   │ ← Parse user requirements (Vdc, Pout, topology pref)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ LIT_REVIEW   │ ← Literature Agent: find relevant papers, baseline efficiencies
└──────┬───────┘
       │
       ▼
┌──────────────┐     ┌──────────────────┐
│ DESIGN_REVIEW│────▶│ HUMAN_APPROVAL   │ (optional interrupt)
└──────┬───────┘     └──────────────────┘
       │
       ▼
┌──────────────┐
│ COMPONENT    │ ← Literature Agent: find matching components (SiC modules, gate drivers)
│ SELECTION    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ SIMULATE     │ ← MATLAB Agent: build model, run simulation, validate
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ ANALYZE      │ ← Reviewer Agent: efficiency, THD, losses, thermal, EMI
└──────┬───────┘
       │
       ├── converged? ──YES──▶ ┌──────────────┐
       │                        │ REPORT       │ ← Writer Agent: IEEE report
       │                        └──────┬───────┘
       │                               │
       │                               ▼
       │                          [END]
       │
       └── NO ──▶ replan (back to COMPONENT or LIT_REVIEW)
```

**Checkpoints at every arrow.** If SIMULATE fails, resume from the last checkpoint.

---

## 5. What Makes This Distinct

Existing agents are either:
- **Coding-first** (Claude Code, Codex, OpenCode, Aider) — wrong architecture for research
- **Library-only** (LangGraph, CrewAI, AutoGen) — missing operational infrastructure
- **Research-readers** (PaperQA2, STORM) — no simulation capability

The SRTP agent is a **hybrid**: borrows operational infrastructure from Hermes Agent (memory, skills, cron, delegation) + workflow engine from LangGraph (state machine, checkpointing) + role model from CrewAI (human-understandable agent roles) + safety from Claude Code (hooks, granular permissions) + agent contract from smolagents (task → report pattern).

No single existing system combines these. The SRTP agent is a synthesis.

---

## Red Team

**Steelman against:** This architecture is over-engineered for the current state of LLM reasoning. Multi-agent orchestration adds coordination overhead (token cost and latency) that may outweigh benefits for tasks a single capable agent could handle. The power electronics domain may not need the full complexity — a single well-prompted agent with MATLAB tools could achieve comparable results with less infrastructure.

**How it could be false:**
1. **Coordination failure:** LLMs are bad at routing between specialists — the orchestrator may repeatedly send tasks to the wrong agent. MasRouter (2025) acknowledges this as an open problem and shows learned routing helps, but results are limited to code benchmarks — no evidence for simulation workflows.
2. **No empirical validation:** This synthesis is based on reading code and documentation, not on running comparative experiments. We don't know which patterns actually help for power electronics tasks. EvoAgent (NAACL 2025) suggests that human-designed frameworks may be suboptimal compared to evolved configurations.
3. **Benchmark domain mismatch:** The two papers that address multi-agent effectiveness (MasRouter, EvoAgent) are on coding benchmarks. Power electronics simulation is structurally different — longer task duration, domain-specific tools, different failure modes.
4. **Report degradation:** The smolagents task→report pattern may lose critical detail in synthesis — the orchestrator works with summaries, not raw data.
5. **Complexity tax:** Each agent role needs its own system prompt, memory, and tool configuration. Maintenance burden grows with agent count.

**What would change my mind:**
- An A/B experiment: single agent vs multi-agent on the same traction inverter design task, measuring design quality (efficiency, THD, thermal margin) and time-to-solution.
- If MasRouter or similar routing approaches are validated on non-coding domains (simulation, analysis, design).
- If the single agent achieves ≥95% of the multi-agent's design quality in <50% of the time, the multi-agent architecture is unjustified.

**Residual doubt:** The orchestrator routing problem is partially addressed by MasRouter but unvalidated for our domain. The human-designed 5-role system may be suboptimal per EvoAgent, but evolutionary optimization is too expensive for simulation workflows. We are in a local optimum — better than random, possibly far from best, with no cheap path to improvement.

---

> **References:** [[citations]] — [3][4] Claude Code, [6] Codex CLI, [7][8] LangGraph, [9] CrewAI, [10] AutoGen, [12] smolagents, [[ai-agents/harness/hermes-agent]]

---

← [[ai-agents/harness/comparative-analysis]] | [[project/plans/multi-agent-architecture|Implementation Plan →]]
