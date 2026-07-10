---
title: CS Field Hub
type: index
field: cs
created: 2026-07-08
updated: 2026-07-10
tags: [cs, index]
---
# CS — AI Agent Architecture Research

> Hub for all computer science / AI research in this vault.
> Sub-fields: agent harness architectures, multi-agent patterns, MATLAB integration, traction inverter integration.

## Traction Inverter MAS Integration
- [[cs/traction-inverter-mas-integration]] — **NEW (2026-07-10):** Comprehensive integration architecture: 7-agent MAS for traction inverter design with confidence-ranked claims (C1-C5), 7 domain guardrails, 8 evidence gates, red-team block
- [[cs/implementation-research]] — **NEW (2026-07-10):** Implementation research: verified APIs (MATLAB Engine, Nexar, PaperQA2, PySpice), code patterns, technology decisions, identified gaps
- [[cs/claim-multi-agent-outperforms-single]] — **NEW:** Claim: multi-agent > single-agent for complex engineering design (C4, supported/replicated)
- [[cs/claim-hybrid-architecture-token-reduction]] — Claim: hybrid LangGraph-CrewAI reduces tokens 76% (C4, supported/single-study)
- [[cs/ai-ml-power-electronics-2025-2026]] — **NEW:** 16 AI/ML applications in power electronics design (from 2025-2026 synthesis)
- [[cs/design-automation-gaps-2025-2026]] — **NEW:** 10 design automation gaps, 11 AI augmentation opportunities

## Multi-Agent Synthesis
- [[cs/multi-agent-synthesis]] — Synthesis of multi-agent design patterns from 7 harnesses + updated with 2026-07-10 research pass

## Agent Harness Deep Dives

### Operational Platforms
- [[cs/harness/hermes-agent]] — Hermes Agent (Nous Research): multi-agent, memory, skills, cron
- [[cs/harness/claude-code]] — Claude Code (Anthropic): hooks, MCP, subagents
- [[cs/harness/opencode]] — OpenCode: model switching, MCP/ACP
- [[cs/harness/codex-cli]] — Codex CLI (OpenAI): sandbox-based, Rust

### Library Frameworks
- [[cs/harness/langgraph]] — LangGraph: state-machine graphs, checkpointing
- [[cs/harness/crewai]] — CrewAI: role-based multi-agent teams
- [[cs/harness/autogen]] — AutoGen (Microsoft): ⚠️ MAINTENANCE MODE since Sept 2025; use MAF for new projects

## Cross-cutting

- [[cs/harness/comparative-analysis]] — Feature matrix across all harnesses
- [[cs/harness/architecture-patterns]] — Recurring architecture patterns
- [[cs/harness/research-agents]] — Research-specific agents (PaperQA2, STORM, GPT Researcher)
- [[cs/harness/matlab-integration]] — MATLAB integration strategies
- [[implementation/plans/multi-agent-architecture]] — Implementation plan: multi-agent system for SRTP

## Agent Papers

- [[cs/agent-papers/agent papers index]] — ReAct, Toolformer, DSO.ai, ChemCrow, Coscientist

## NEW: 2026-07-10 Source Notes

### Peer-Reviewed
- [[sources/cs/pe-gpt-2025-multimodal-pe-design]] — PE-GPT (IEEE TIE 2025): LLM agent beats humans on PE design
- [[sources/cs/hybrid-langgraph-crewai-2026-ieee]] — Hybrid LangGraph-CrewAI (IEEE Access 2026): 96.1% success, 76.2% token reduction
- [[sources/cs/agentic-tcad-2026-date]] — AgenticTCAD (DATE 2026): 40× speedup on semiconductor design
- [[sources/cs/thermrag-2025-pe-thermal-agent]] — ThermRAG (IEEE 2025): Thermal design agent for PE

### Preprints & Industry
- [[sources/cs/power-circuit-ai-2026-abb-mas-pcb]] — Power Circuit AI (ABB 2026): Multi-agent PCB design
- [[sources/cs/drcy-2026-allspice-mas-review]] — DRCY (AllSpice 2026): Production schematic review MAS
- [[sources/cs/ltspice-mcp-2026]] — ltspice-mcp: 51 SPICE tools via MCP protocol
- [[sources/cs/langgraph-production-gaps-2026-diagrid]] — LangGraph checkpointing gaps (Diagrid 2026)
- [[sources/cs/multi-agent-llm-control-2026-pe]] — 6-agent LLM control for PE

### Earlier Sources
- [[sources/cs/masrouter-2025-llm-routing]] — MasRouter: learned routing for MAS
- [[sources/cs/evoagent-2025-evolutionary-delegation]] — EvoAgent: evolutionary agent generation
- [[sources/cs/pe-mas-flyback-mas]] — PE-MAS: working flyback MAS

## Cross-field Links

- [[_index/ee]] — Power electronics (target domain for agent application)
- [[catalog.md]] — Full vault catalog
- [[citations]] — Master bibliography
