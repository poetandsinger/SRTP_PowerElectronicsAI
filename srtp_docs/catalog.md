---
title: Catalog
type: catalog
field: root
created: 2026-07-06
updated: 2026-07-17
tags: [index]
---

# Research Vault Catalog

> Every note, one line, grouped by field then status.
> Format: `- [[path]] — status/evidence — one-line summary`

## Power Electronics

### Maps
- [[maps/power-electronics]] — power electronics field hub
- [[power-electronics/traction-inverter/traction-inverter-index]] — traction inverter industry research hub
- [[power-electronics/traction-inverter/research-synthesis-2025-2026]] — map — hub pointing to 6 extracted topic notes (was a 538-line synthesis)

### Unverified / Single-study
- [[power-electronics/traction-inverter/what-is-a-traction-inverter]] — unverified/single-study — fundamentals: what a traction inverter is and why it matters
- [[power-electronics/traction-inverter/circuit-topologies]] — unverified/single-study — two-level, three-level, multilevel topologies for EV traction
- [[power-electronics/traction-inverter/components]] — unverified/single-study — power semiconductor components: SiC MOSFETs, GaN HEMTs, IGBTs
- [[power-electronics/traction-inverter/control-schemes]] — unverified/single-study — FOC, DTC, MPC, and other control strategies
- [[power-electronics/traction-inverter/simulation-toolbox]] — unverified/single-study — simulation toolbox landscape for traction inverters
- [[power-electronics/traction-inverter/matlab-modeling]] — unverified/single-study — MATLAB/Simulink modeling approaches
- [[power-electronics/traction-inverter/open-problems]] — unverified/single-study — unsolved problems and research frontiers
- [[power-electronics/traction-inverter/topology-landscape-2025-2026]] — unverified/single-study — topology & semiconductor landscape: 2L/3L/multilevel, SiC vs GaN vs Si, 800V trends
- [[power-electronics/traction-inverter/simulation-workflows-2025-2026]] — unverified/single-study — 10 simulation tools compared, 10-phase design workflow, pain points
- [[power-electronics/traction-inverter/standards-landscape-2025-2026]] — unverified/single-study — 11 core standards (IEC 61800, ISO 26262, AEC-Q, AQG 324, CISPR 25)
- [[power-electronics/traction-inverter/market-trends-2025-2026]] — unverified/single-study — $8.75B→$36.8B market, 17.3% CAGR, supplier deep dives
- [[power-electronics/problem-statement/problem-statement-index]] — unverified/single-study — AI for traction inverter design: problem definition

### Unverified / Theoretical
- [[power-electronics/traction-inverter/control-how-to]] — unverified/theoretical — practical guide: tuning and implementing FOC

### Sources
- [[sources/power-electronics/cacciato-etal-2022-gan-anpc]] — GaN ANPC inverter
- [[sources/power-electronics/pimpale-mahadik-2025-asc-discharge]] — active short-circuit discharge
- [[sources/power-electronics/sachs-etal-2025-single-dual-inverter]] — single vs dual inverter
- [[sources/power-electronics/sachs-neuburger-2025-3l-tnpc]] — 3L T-NPC BEV trends review
- [[sources/power-electronics/zhang-negri-2026-ai-multiphysics-sustainability]] — AI-assisted multi-physics sustainability evaluation
- [[sources/power-electronics/zuo-etal-2024-mtpa-dcee]] — MTPA / DC-link energy efficiency

## AI / Agent Architecture

### Maps
- [[maps/ai-agents]] — AI agent architecture field hub
- [[ai-agents/harness/harness-index]] — agent harness research hub
- [[ai-agents/agent-papers/agent-papers-index]] — agent architectures from research papers

### Unverified / Single-study (harnesses)
- [[ai-agents/harness/architecture-patterns]] — unverified/single-study — recurring architecture patterns across agent harnesses
- [[ai-agents/harness/comparative-analysis]] — unverified/single-study — side-by-side comparison of all agent harnesses
- [[ai-agents/harness/claude-code]] — unverified/single-study — Claude Code CLI architecture deep dive
- [[ai-agents/harness/codex-cli]] — unverified/single-study — Codex CLI architecture deep dive
- [[ai-agents/harness/opencode]] — unverified/single-study — OpenCode CLI architecture deep dive
- [[ai-agents/harness/hermes-agent]] — unverified/single-study — Hermes Agent architecture deep dive
- [[ai-agents/harness/langgraph]] — unverified/single-study — LangGraph architecture deep dive
- [[ai-agents/harness/crewai]] — unverified/single-study — CrewAI architecture deep dive
- [[ai-agents/harness/autogen]] — unverified/single-study — AutoGen architecture deep dive
- [[ai-agents/harness/research-agents]] — unverified/single-study — research-specific agent patterns and tools

### Unverified / Theoretical
- [[ai-agents/harness/matlab-integration]] — unverified/theoretical — strategies for integrating MATLAB with AI agent harnesses

### Cross-cutting
- [[ai-agents/multi-agent-synthesis]] — unverified/single-study — MAS design patterns synthesized from 7 harnesses + 2 papers
- [[ai-agents/traction-inverter-mas-integration]] — integration architecture: 7-agent MAS for traction inverter design with confidence-ranked claims, guardrails, evidence gates
- [[ai-agents/implementation-research]] — implementation research: verified APIs, code patterns, technology decisions
- [[ai-agents/ai-ml-power-electronics-2025-2026]] — unverified/single-study — 16 AI application areas in PE design with quantitative results
- [[ai-agents/design-automation-gaps-2025-2026]] — unverified/single-study — 10 design automation gaps, 11 AI augmentation opportunities

### Claims
- [[ai-agents/claim-multi-agent-outperforms-single]] — **supported/replicated** — multi-agent outperforms single-agent for complex engineering design (C4)
- [[ai-agents/claim-hybrid-architecture-token-reduction]] — **supported/single-study** — hybrid LangGraph-CrewAI reduces tokens 76% vs pure CrewAI (C4)

### Sources
- [[sources/ai-agents/masrouter-2025-llm-routing]] — MasRouter: LLM routing for multi-agent systems
- [[sources/ai-agents/evoagent-2025-evolutionary-delegation]] — EvoAgent: evolutionary multi-agent generation
- [[sources/ai-agents/pe-mas-flyback-mas]] — PE-MAS: working LangGraph power electronics multi-agent system
- [[sources/ai-agents/pe-gpt-2025-multimodal-pe-design]] — PE-GPT (IEEE TIE 2025): LLM agent 22.2% better than humans on PE design
- [[sources/ai-agents/power-circuit-ai-2026-abb-mas-pcb]] — Power Circuit AI (ABB 2026): multi-agent PCB design, 100% connectivity
- [[sources/ai-agents/hybrid-langgraph-crewai-2026-ieee]] — Hybrid LangGraph-CrewAI (IEEE Access 2026): 96.1% success, 76.2% token reduction
- [[sources/ai-agents/agentic-tcad-2026-date]] — AgenticTCAD (DATE 2026): 40× speedup on semiconductor design
- [[sources/ai-agents/drcy-2026-allspice-mas-review]] — DRCY (AllSpice 2026): production multi-agent schematic review
- [[sources/ai-agents/ltspice-mcp-2026]] — ltspice-mcp: 51 MCP tools for SPICE simulation via LLM
- [[sources/ai-agents/langgraph-production-gaps-2026-diagrid]] — LangGraph checkpointing ≠ durable execution (Diagrid 2026)
- [[sources/ai-agents/multi-agent-llm-control-2026-pe]] — 6-agent LLM control framework for power electronics
- [[sources/ai-agents/thermrag-2025-pe-thermal-agent]] — ThermRAG (IEEE 2025): multimodal agent for PE thermal design

## Project (operational — no status)

### Plans
- [[project/plans/plans-index]] — 5-phase implementation roadmap (CLI-first, 3 agents, PySpice primary)
- [[project/plans/phase-0-foundation]] — Phase 0: foundation + A/B test (single vs multi-agent)
- [[project/plans/phase-1-multi-agent]] — Phase 1: 3-agent LangGraph core with guardrails and evidence gates
- [[project/plans/phase-2-simulation]] — Phase 2: MATLAB/PySpice dual-engine + ltspice-mcp device-level sim
- [[project/plans/phase-3-knowledge]] — Phase 3: PaperQA2 literature + Nexar components + memory
- [[project/plans/phase-4-production]] — Phase 4: watchdog, HITL, benchmark, CLI packaging
- [[project/plans/multi-agent-architecture]] — multi-agent architecture plan
- [[project/plans/architecture]] — architecture decision record
- [[project/plans/tech-stack]] — technology stack decisions
- [[project/plans/risks-metrics]] — risk register and success metrics

### Changelog
- [[project/changelog/log]] — append-only action log
- [[project/changelog/changelog-index]] — changelog index
- [[project/changelog/2026-07-06-initial-setup]] — initial setup
- [[project/changelog/2026-07-06-restructure]] — vault restructure
- [[project/changelog/2026-07-06-architecture-pivot]] — architecture pivot
- [[project/changelog/2026-07-06-subagent-findings]] — subagent findings integrated

## Audits
- [[audits/lint-report-2026-07-08]] — 2026-07-08 lint report
- [[audits/multi-agent-audit-2026-07-09]] — 2026-07-09 self-audit of multi-agent synthesis
- [[audits/multi-agent-traction-inverter-audit-2026-07-10]] — 2026-07-10 comprehensive audit + fresh research pass
- [[audits/audit-changelog-traction-inverter]] — research audit changelog for traction inverter literature

## Root
- [[README]] — SRTP Power Electronics AI project overview
- [[citations]] — master bibliography
- [[SCHEMA]] — schema, taxonomy, conventions

---

← [[README]] | [[SCHEMA]]
