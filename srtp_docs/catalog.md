---
title: Catalog
type: catalog
field: root
created: 2026-07-06
updated: 2026-07-17
tags: [index]
---

# Research Vault Catalog

> Every note, one line, grouped by field then status. **The global flat index** — the one file that lists *all* notes with their `status/evidence`. (The per-field [[maps/power-electronics]] / [[maps/ai-agents]] are navigation hubs; this is the complete inventory.)
> Format: `- [[path]] — status/evidence — one-line summary`

## Power Electronics

### Maps
- [[maps/power-electronics]] — power electronics field hub
- [[power-electronics/traction-inverter/traction-inverter-index]] — traction inverter industry research hub
- [[power-electronics/traction-inverter/reference-designs-index]] — map — reference designs hub (1 synthetic anchor + 3 real)

### Unverified / Single-study
- [[power-electronics/traction-inverter/what-is-a-traction-inverter]] — unverified/single-study — fundamentals: what a traction inverter is and why it matters
- [[power-electronics/traction-inverter/circuit-topologies]] — unverified/single-study — two-level, three-level, multilevel topologies for EV traction
- [[power-electronics/traction-inverter/components]] — unverified/single-study — power semiconductor components: SiC MOSFETs, GaN HEMTs, IGBTs
- [[power-electronics/traction-inverter/control-schemes]] — unverified/single-study — FOC, DTC, MPC, and other control strategies
- [[power-electronics/traction-inverter/open-problems]] — unverified/single-study — unsolved problems and research frontiers
- [[power-electronics/traction-inverter/simulation-and-validation]] — unverified/single-study — PLECS-first simulation & validation workflow, corner tests
- [[power-electronics/traction-inverter/standards-and-compliance]] — unverified/single-study — IEC 61800, ISO 26262, AEC-Q, AQG 324, CISPR 25 requirements
- [[power-electronics/traction-inverter/reference-design-wolfspeed-ti-300kw-800v]] — unverified/single-study — real vendor CRD: 800V/300kW SiC, actual parts + measured metrics
- [[power-electronics/traction-inverter/reference-design-tesla-model3-400v-sic]] — unverified/single-study — production teardown: 400V SiC, highest-volume inverter
- [[power-electronics/traction-inverter/reference-design-nissan-leaf-400v-igbt]] — unverified/single-study — production teardown: 400V Si-IGBT baseline
- [[power-electronics/traction-inverter/bom-price-database]] — unverified/single-study — priced BOM: real dated distributor prices + volume caveat

### Unverified / Theoretical
- [[power-electronics/traction-inverter/control-how-to]] — unverified/theoretical — practical guide: tuning and implementing FOC
- [[power-electronics/traction-inverter/machine-and-load]] — unverified/theoretical — the PMSM/IPMSM plant: dq model, torque, operating regions, limits
- [[power-electronics/traction-inverter/materials-and-properties]] — unverified/single-study — material property reference (semiconductor/ceramic/die-attach/dielectric/magnet)
- [[power-electronics/traction-inverter/reference-design-2l-b6-sic-800v]] — unverified/theoretical — design cluster anchor (synthetic): 800V SiC 2L-B6, 150 kW
- [[power-electronics/traction-inverter/design-procedure]] — unverified/theoretical — end-to-end sizing/design procedure (worked)
- [[power-electronics/traction-inverter/schematics]] — unverified/theoretical — mermaid schematics (power stage, gate drive, control, ASC)
- [[power-electronics/traction-inverter/thermal-design]] — unverified/single-study — Rth/Zth chain, cooling, TIM, Tj estimation, derating (real values)
- [[power-electronics/traction-inverter/gate-driver-design]] — unverified/single-study — SiC gate drive: rails, Rg/Ig/Pdrive, desat, isolation, ICs, worked example
- [[power-electronics/traction-inverter/protection-and-safety]] — unverified/single-study — protection layers + safety-factor/derating table (cosmic-ray, SC, OV, ASC, ISO 26262)
- [[power-electronics/traction-inverter/emi-emc-design]] — unverified/single-study — CISPR 25, CM/DM, input filter, dv/dt reflected wave, bearing currents
- [[power-electronics/traction-inverter/packaging-and-layout]] — unverified/single-study — module stack, laminated busbar Lσ, Kelvin loop, creepage/clearance
- [[power-electronics/traction-inverter/bom]] — unverified/theoretical — component-class BOM with representative parts + cost split
- [[power-electronics/traction-inverter/worked-example-400v-150kw]] — unverified/theoretical — 400V SiC 150kW worked example (current-doubling penalty)
- [[power-electronics/traction-inverter/design-tradeoffs]] — unverified/single-study — how to compromise: device/voltage/fsw/topology trade-offs + decision table
- [[power-electronics/traction-inverter/manufacturing-and-test]] — unverified/single-study — module assembly, double-pulse, HIL, EOL test, production quality
- [[power-electronics/traction-inverter/reliability-and-lifetime]] — unverified/single-study — power-cycling wear-out, lifetime models, mission profile, SiC-specific degradation

### Sources
- [[sources/power-electronics/cacciato-etal-2022-gan-anpc]] — GaN ANPC inverter
- [[sources/power-electronics/pimpale-mahadik-2025-asc-discharge]] — active short-circuit discharge
- [[sources/power-electronics/sachs-etal-2025-single-dual-inverter]] — single vs dual inverter
- [[sources/power-electronics/sachs-neuburger-2025-3l-tnpc]] — 3L T-NPC BEV trends review
- [[sources/power-electronics/zhang-negri-2026-ai-multiphysics-sustainability]] — AI-assisted multi-physics sustainability evaluation
- [[sources/power-electronics/zuo-etal-2024-mtpa-dcee]] — MTPA / DC-link energy efficiency

## Problem Statement (preface — motivation, not engineering)
- [[problem-statement/problem-statement-index]] — unverified/single-study — why AI for traction inverter design: workforce, market, competitive landscape (moved out of power-electronics/ 2026-07-17)

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
- [[ai-agents/harness/plecs-integration]] — unverified/single-study — strategies for integrating PLECS (XML-RPC/MCP) with AI agent harnesses

### Cross-cutting
- [[ai-agents/agentic-workflow-patterns]] — unverified/single-study — 2026 agentic pattern catalog (routing, orchestrator-workers, evaluator-optimizer, reflection) mapped to SRTP
- [[ai-agents/design-loop-architecture]] — unverified/single-study — **key finding:** topology→refine→parameter-optimize is the field-standard PE/analog agent shape; the plan's missing optimizer
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
- [[sources/ai-agents/plecs-xmlrpc-scripting-interface]] — PLECS XML-RPC/JSON-RPC scripting API (the sim backend)
- [[sources/ai-agents/plecs-ai-agent-integration-ordonez]] — direct AI+PLECS prior art: capability boundary + token economics
- [[sources/ai-agents/phia-lpcomda-2026-physics-informed-pe-agent]] — PHIA/LP-COMDA (AAAI 2026): physics-informed PE agent, low-data surrogates
- [[sources/ai-agents/analogsage-2025-self-evolving-analog-mas]] — AnalogSAGE: 3-stage EDA MAS + stratified self-evolving memory
- [[sources/ai-agents/agent-frameworks-2026-currency]] — mid-2026 framework currency (LangGraph 1.0, MAF, AgentSlimming)
- [[sources/ai-agents/liu-2026-iet-llm-power-converter-framework]] — Liu et al. (IET PE 2026): universal circuit-encoding LLM framework for converter design
- [[sources/ai-agents/context-engineering-2026]] — context engineering (write/select/compress/isolate) + agent-memory survey

## Project (operational — no status)

### Plans (hub + 8 topic files, no phases)
- [[ai-agent-mas-plan]] — **plan hub** — schematic, invariants, prior-art anchor, topic map
- [[architecture]] — agents, orchestration, typed `InverterDesignState` schema
- [[design-loop]] — topology→refine→parameter-optimize; explicit optimizer; evaluator-optimizer; iterate routing
- [[knowledge-rag]] — RAG backbone: corpus, ingestion, citation gate, coverage audit
- [[plecs-harness]] — PLECS service, template+registry validation procedure, 5-layer summarizer contract
- [[guardrails-and-evidence]] — domain guardrails + evidence gates (the evaluator rubric)
- [[memory]] — episodic/procedural/semantic memory + context-isolation
- [[tech-stack]] — frameworks, LLM routing, licenses
- [[evaluation-and-benchmark]] — benchmark, single-vs-MAS A/B, open questions, risks

### Changelog
- [[changelog-index]] — changelog index
- [[2026-07-17-traction-inverter-textbook]] — 29-chapter traction-inverter textbook built; problem-statement→root; meta files removed
- [[2026-07-06-initial-setup]] — initial setup
- [[2026-07-06-restructure]] — vault restructure
- [[2026-07-06-architecture-pivot]] — architecture pivot
- [[2026-07-06-subagent-findings]] — subagent findings integrated

## Audits
- [[audits/traction-inverter-kb-audit-2026-07-17]] — **2026-07-17 textbook audit** — 29-chapter build manual; citation coverage; P0 gap = PLECS validation (EMI/packaging/thermal/reliability now covered)
- [[audits/ai-agent-docs-audit-2026-07-17]] — **2026-07-17 audit** — MATLAB→PLECS pivot, 7-vs-3 agents, confidence inflation, gap closures
- [[audits/plan-sufficiency-review-2026-07-17]] — **2026-07-17 plan sufficiency review** — is the MAS plan enough? strategy yes, build-spec no (8 gaps → topic split)
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
