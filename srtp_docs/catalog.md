# Research Vault Catalog

> Every note, one line, grouped by field then status.
> Format: `- [[path]] — status/evidence — one-line summary`
> Last updated: 2026-07-10

## EE — Power Electronics

### Index
- [[_index/ee]] — EE field hub: power electronics research overview
- [[ee/traction-inverter/traction inverter index]] — Traction inverter industry research hub

### Unverified / Single-study
- [[ee/traction-inverter/what-is-a-traction-inverter]] — unverified/single-study — Fundamentals: what a traction inverter is and why it matters
- [[ee/traction-inverter/circuit-topologies]] — unverified/single-study — Two-level, three-level, multilevel topologies for EV traction
- [[ee/traction-inverter/components]] — unverified/single-study — Power semiconductor components: SiC MOSFETs, GaN HEMTs, IGBTs
- [[ee/traction-inverter/control-schemes]] — unverified/single-study — FOC, DTC, MPC, and other control strategies
- [[ee/traction-inverter/simulation-toolbox]] — unverified/single-study — Simulation toolbox landscape for traction inverters
- [[ee/traction-inverter/matlab-modeling]] — unverified/single-study — MATLAB/Simulink modeling approaches
- [[ee/traction-inverter/open-problems]] — unverified/single-study — Unsolved problems and research frontiers
- [[ee/traction-inverter/research-synthesis-2025-2026]] — index — Hub page pointing to 6 extracted topic notes (was 538-line synthesis, now fragmented)
- [[ee/traction-inverter/topology-landscape-2025-2026]] — unverified/single-study — Topology & semiconductor landscape: 2L/3L/multilevel, SiC vs GaN vs Si, 800V trends
- [[ee/traction-inverter/simulation-workflows-2025-2026]] — unverified/single-study — 10 simulation tools compared, 10-phase design workflow, pain points
- [[ee/traction-inverter/standards-landscape-2025-2026]] — unverified/single-study — 11 core standards (IEC 61800, ISO 26262, AEC-Q, AQG 324, CISPR 25)
- [[ee/traction-inverter/market-trends-2025-2026]] — unverified/single-study — $8.75B→$36.8B market, 17.3% CAGR, supplier deep dives
- [[ee/problem-statement/problem statement index]] — unverified/single-study — AI for traction inverter design: problem definition
- [[_lint/audit-changelog-traction-inverter]] — Research audit changelog for traction inverter literature

### Unverified / Theoretical
- [[ee/traction-inverter/control-how-to]] — unverified/theoretical — Practical guide: tuning and implementing FOC

## CS — AI / Agent Architecture

### Index
- [[_index/cs]] — CS field hub: AI agent architecture research overview
- [[cs/harness/harness index]] — Agent harness research hub
- [[cs/agent-papers/agent papers index]] — Agent architectures from research papers

### Unverified / Single-study
- [[cs/harness/architecture-patterns]] — unverified/single-study — Recurring architecture patterns across agent harnesses
- [[cs/harness/comparative-analysis]] — unverified/single-study — Side-by-side comparison of all agent harnesses
- [[cs/harness/claude-code]] — unverified/single-study — Claude Code CLI architecture deep dive
- [[cs/harness/codex-cli]] — unverified/single-study — Codex CLI architecture deep dive
- [[cs/harness/opencode]] — unverified/single-study — OpenCode CLI architecture deep dive
- [[cs/harness/hermes-agent]] — unverified/single-study — Hermes Agent architecture deep dive
- [[cs/harness/langgraph]] — unverified/single-study — LangGraph architecture deep dive
- [[cs/harness/crewai]] — unverified/single-study — CrewAI architecture deep dive
- [[cs/harness/autogen]] — unverified/single-study — AutoGen architecture deep dive
- [[cs/harness/research-agents]] — unverified/single-study — Research-specific agent patterns and tools

### Unverified / Theoretical
- [[cs/harness/matlab-integration]] — unverified/theoretical — Strategies for integrating MATLAB with AI agent harnesses

### Unverified / Single-study (Cross-Cutting)
- [[cs/multi-agent-synthesis]] — unverified/single-study — Multi-agent system design patterns synthesized from 7 harnesses + 2 arXiv papers
- [[cs/traction-inverter-mas-integration]] — **NEW (2026-07-10):** Integration architecture: 7-agent MAS for traction inverter design with confidence-ranked claims, guardrails, evidence gates
- [[sources/cs/masrouter-2025-llm-routing]] — MasRouter: LLM routing for multi-agent systems
- [[sources/cs/evoagent-2025-evolutionary-delegation]] — EvoAgent: evolutionary multi-agent generation
- [[sources/cs/pe-mas-flyback-mas]] — PE-MAS: working LangGraph-based power electronics multi-agent system

### NEW Source Notes (2026-07-10 research pass)
- [[sources/cs/pe-gpt-2025-multimodal-pe-design]] — PE-GPT (IEEE TIE 2025): LLM agent 22.2% better than humans on power electronics design
- [[sources/cs/power-circuit-ai-2026-abb-mas-pcb]] — Power Circuit AI (ABB 2026): Multi-agent PCB design, 100% connectivity
- [[sources/cs/hybrid-langgraph-crewai-2026-ieee]] — Hybrid LangGraph-CrewAI (IEEE Access 2026): 96.1% success, 76.2% token reduction
- [[sources/cs/agentic-tcad-2026-date]] — AgenticTCAD (DATE 2026): 40× speedup on semiconductor design
- [[sources/cs/drcy-2026-allspice-mas-review]] — DRCY (AllSpice 2026): Production multi-agent schematic review
- [[sources/cs/ltspice-mcp-2026]] — ltspice-mcp: 51 MCP tools for SPICE simulation via LLM
- [[sources/cs/langgraph-production-gaps-2026-diagrid]] — LangGraph checkpointing ≠ durable execution (Diagrid 2026)
- [[sources/cs/multi-agent-llm-control-2026-pe]] — 6-agent LLM control framework for power electronics
- [[sources/cs/thermrag-2025-pe-thermal-agent]] — ThermRAG (IEEE 2025): Multimodal agent for PE thermal design
- [[sources/ee/zhang-negri-2026-ai-multiphysics-sustainability]] — AI-assisted multi-physics sustainability evaluation for traction inverters

### NEW Claim Notes (2026-07-10)
- [[cs/claim-multi-agent-outperforms-single]] — **supported/replicated** — Multi-agent outperforms single-agent for complex engineering design (C4)
- [[cs/claim-hybrid-architecture-token-reduction]] — **supported/single-study** — Hybrid LangGraph-CrewAI reduces tokens 76% vs pure CrewAI (C4)
- [[cs/ai-ml-power-electronics-2025-2026]] — unverified/single-study — 16 AI application areas in PE design with quantitative results
- [[cs/design-automation-gaps-2025-2026]] — unverified/single-study — 10 design automation gaps, 11 AI augmentation opportunities

## Operational (no status — project docs)

- [[implementation/plans/plan index]] — **UPDATED 2026-07-10:** 5-phase implementation roadmap (CLI-first, 3 agents, PySpice primary)
- [[implementation/plans/phase-0-foundation]] — **NEW:** Phase 0: Foundation + A/B test (single vs multi-agent)
- [[implementation/plans/phase-1-multi-agent]] — **NEW:** Phase 1: 3-agent LangGraph core with guardrails and evidence gates
- [[implementation/plans/phase-2-simulation]] — **NEW:** Phase 2: MATLAB/PySpice dual-engine + ltspice-mcp device-level sim
- [[implementation/plans/phase-3-knowledge]] — **NEW:** Phase 3: PaperQA2 literature + Nexar components + memory
- [[implementation/plans/phase-4-production]] — **NEW:** Phase 4: Watchdog, HITL, benchmark, CLI packaging
- [[implementation/plans/architecture]] — Architecture decision record (pre-2026-07-10)
- [[implementation/plans/tech-stack]] — Technology stack decisions (pre-2026-07-10)
- [[implementation/plans/risks-metrics]] — Risk register and success metrics
- [[implementation/plans/multi-agent-architecture]] — Original multi-agent architecture plan (superseded by phase plans)
- [[cs/implementation-research]] — **NEW:** Implementation research: verified APIs, code patterns, technology decisions

### Archived Phase Plans (pre-2026-07-10)
- [[implementation/plans/phase-0-skeleton]] — (archived) GUI skeleton → replaced by phase-0-foundation
- [[implementation/plans/phase-1-agent]] — (archived) smolagents → replaced by phase-1-multi-agent
- [[implementation/plans/phase-2-matlab]] — (archived) → incorporated into phase-2-simulation
- [[implementation/plans/phase-3-topology]] — (archived) GUI topology editor → deferred
- [[implementation/plans/phase-4-workflow]] — (archived) → incorporated into phase-1-multi-agent
- [[implementation/plans/phase-5-components]] — (archived) → replaced by phase-3-knowledge
- [[implementation/plans/phase-6-reports]] — (archived) → distributed across phases
- [[implementation/plans/phase-7-polish]] — (archived) → replaced by phase-4-production

## Audit Reports
- [[_lint/multi-agent-audit-2026-07-09]] — 2026-07-09 self-audit of multi-agent synthesis
- [[_lint/multi-agent-traction-inverter-audit-2026-07-10]] — **NEW:** 2026-07-10 comprehensive audit + fresh research pass

## Root

- [[README]] — SRTP Power Electronics AI project overview
- [[citations]] — Master bibliography (42 refs)
- [[SCHEMA]] — Schema, taxonomy, conventions
- [[changelog/log]] — Append-only action log
