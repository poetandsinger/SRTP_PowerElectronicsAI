---
title: AI Agents Field Hub
type: map
field: ai-agents
created: 2026-07-08
updated: 2026-07-10
tags: [ai-agents, index]
---
# AI Agents — Agent Architecture Research

> Hub for all computer science / AI research in this vault.
> Sub-fields: agent harness architectures, multi-agent patterns, MATLAB integration, traction inverter integration.

## Traction Inverter MAS Integration
- [[ai-agents/traction-inverter-mas-integration]] — **NEW (2026-07-10):** Comprehensive integration architecture: 7-agent MAS for traction inverter design with confidence-ranked claims (C1-C5), 7 domain guardrails, 8 evidence gates, red-team block
- [[ai-agents/implementation-research]] — **NEW (2026-07-10):** Implementation research: verified APIs (MATLAB Engine, Nexar, PaperQA2, PySpice), code patterns, technology decisions, identified gaps
- [[ai-agents/claim-multi-agent-outperforms-single]] — **NEW:** Claim: multi-agent > single-agent for complex engineering design (C4, supported/replicated)
- [[ai-agents/claim-hybrid-architecture-token-reduction]] — Claim: hybrid LangGraph-CrewAI reduces tokens 76% (C4, supported/single-study)
- [[ai-agents/ai-ml-power-electronics-2025-2026]] — **NEW:** 16 AI/ML applications in power electronics design (from 2025-2026 synthesis)
- [[ai-agents/design-automation-gaps-2025-2026]] — **NEW:** 10 design automation gaps, 11 AI augmentation opportunities

## Multi-Agent Synthesis
- [[ai-agents/multi-agent-synthesis]] — Synthesis of multi-agent design patterns from 7 harnesses + updated with 2026-07-10 research pass

## Agent Harness Deep Dives

### Operational Platforms
- [[ai-agents/harness/hermes-agent]] — Hermes Agent (Nous Research): multi-agent, memory, skills, cron
- [[ai-agents/harness/claude-code]] — Claude Code (Anthropic): hooks, MCP, subagents
- [[ai-agents/harness/opencode]] — OpenCode: model switching, MCP/ACP
- [[ai-agents/harness/codex-cli]] — Codex CLI (OpenAI): sandbox-based, Rust

### Library Frameworks
- [[ai-agents/harness/langgraph]] — LangGraph: state-machine graphs, checkpointing
- [[ai-agents/harness/crewai]] — CrewAI: role-based multi-agent teams
- [[ai-agents/harness/autogen]] — AutoGen (Microsoft): ⚠️ MAINTENANCE MODE since Sept 2025; use MAF for new projects

## Cross-cutting

- [[ai-agents/harness/comparative-analysis]] — Feature matrix across all harnesses
- [[ai-agents/harness/architecture-patterns]] — Recurring architecture patterns
- [[ai-agents/harness/research-agents]] — Research-specific agents (PaperQA2, STORM, GPT Researcher)
- [[ai-agents/harness/plecs-integration]] — PLECS integration strategies (agent↔simulation backend)
- [[project/plans/ai-agent-mas-plan]] — Implementation plan: multi-agent system for SRTP

## Agent Papers

- [[ai-agents/agent-papers/agent-papers-index]] — ReAct, Toolformer, DSO.ai, ChemCrow, Coscientist

## NEW: 2026-07-10 Source Notes

### Peer-Reviewed
- [[sources/ai-agents/pe-gpt-2025-multimodal-pe-design]] — PE-GPT (IEEE TIE 2025): LLM agent beats humans on PE design
- [[sources/ai-agents/hybrid-langgraph-crewai-2026-ieee]] — Hybrid LangGraph-CrewAI (IEEE Access 2026): 96.1% success, 76.2% token reduction
- [[sources/ai-agents/agentic-tcad-2026-date]] — AgenticTCAD (DATE 2026): 40× speedup on semiconductor design
- [[sources/ai-agents/thermrag-2025-pe-thermal-agent]] — ThermRAG (IEEE 2025): Thermal design agent for PE

### Preprints & Industry
- [[sources/ai-agents/power-circuit-ai-2026-abb-mas-pcb]] — Power Circuit AI (ABB 2026): Multi-agent PCB design
- [[sources/ai-agents/drcy-2026-allspice-mas-review]] — DRCY (AllSpice 2026): Production schematic review MAS
- [[sources/ai-agents/ltspice-mcp-2026]] — ltspice-mcp: 51 SPICE tools via MCP protocol
- [[sources/ai-agents/langgraph-production-gaps-2026-diagrid]] — LangGraph checkpointing gaps (Diagrid 2026)
- [[sources/ai-agents/multi-agent-llm-control-2026-pe]] — 6-agent LLM control for PE

### Earlier Sources
- [[sources/ai-agents/masrouter-2025-llm-routing]] — MasRouter: learned routing for MAS
- [[sources/ai-agents/evoagent-2025-evolutionary-delegation]] — EvoAgent: evolutionary agent generation
- [[sources/ai-agents/pe-mas-flyback-mas]] — PE-MAS: working flyback MAS

## Cross-field Links

- [[maps/power-electronics]] — Power electronics (target domain for agent application)
- [[catalog.md]] — Full vault catalog
- [[citations]] — Master bibliography
