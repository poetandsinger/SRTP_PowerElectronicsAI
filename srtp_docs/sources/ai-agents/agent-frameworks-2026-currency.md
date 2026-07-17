---
title: "Agent Orchestration Framework Currency — mid-2026 snapshot"
type: source
field: ai-agents
tags: [ai-agents, langgraph, crewai, autogen, orchestration, comparison, architecture]
authors: [multiple — vendor docs + ACL 2026 + comparison surveys]
year: 2026
venue: "LangChain/CrewAI/Microsoft docs + ACL 2026 + framework comparison surveys"
url: "https://www.langchain.com/resources/ai-agent-frameworks"
captured: 2026-07-17
reliability: medium
peer_reviewed: false
reliability_note: "Version/feature facts sourced from vendor docs + 2026 comparison surveys (medium-low; marketing-adjacent). The AgentSlimming result is ACL 2026 (high). Verify exact LangGraph durable-execution semantics against primary docs before relying on them in the plan."
---

# Agent Orchestration Framework Currency — mid-2026

Refreshes the framework facts in [[ai-agents/implementation-research]] and [[ai-agents/multi-agent-synthesis]], several of which are ~1 week to several months stale.

## What changed since the 2026-07-10 pass

- **LangGraph 1.0** — GA October 2025. **Q2 2026** added **per-node timeouts** and **durable streaming**. It remains the pick for durable execution: explicit graph nodes/edges, checkpointing, **resume-on-failure**, HITL interrupts, typed shared state.
  - **Correction to our docs:** the "LangGraph checkpointing ≠ durable execution" concern ([[sources/ai-agents/langgraph-production-gaps-2026-diagrid]], Feb 2026) is **partially superseded** — 1.0 + Q2-2026 features narrow the gap. We still want a watchdog + idempotency keys, but the framework now does more of the work. **Re-verify against primary LangGraph docs before finalizing.**
- **Microsoft Agent Framework (MAF) 1.0** — released **April 3, 2026**, the unified successor merging Semantic Kernel + AutoGen. Ships **native MCP + A2A**. Confirms "AutoGen is EOL." **Relevant to SRTP:** our simulation backend is an MCP server (PLECS MCP), so a framework with native MCP is now a real option to weigh against LangGraph.
- **CrewAI 1.14** — May–June 2026, pluggable backends. Still **no built-in checkpointing** for long-running workflows; role-based, fast to prototype (~10 min vs LangGraph ~45 min).

## AgentSlimming (ACL 2026) — verified, and it cuts our way
`aclanthology.org/2026.acl-long.1387` / arXiv 2605.08813. Reduces average token cost **up to 78.9%** with negligible degradation by **estimating each agent's importance and pruning redundant agents** (neural-net-compression analogy). Token cost grows **quadratically** with agents × turns; automated MAS expansion tends to bloat.

**SRTP implication:** hard evidence for the **"start minimal, prune aggressively"** principle. It directly supports the implementation-research A2 decision (3 agents, not 7) and undercuts the bridge note's 7-agent architecture as a *starting* point.

## Net for the plan
1. **Keep LangGraph** as the orchestration engine — it is now the durable-execution leader at 1.0, and the durability gap our docs flag is shrinking. Weigh MAF only for its native MCP/A2A.
2. **CrewAI stays a pattern donor** (role semantics), not the runtime — no checkpointing.
3. **Design for minimality and pruning** from day one (AgentSlimming); do not ship 7 agents before the 3-agent core is proven.
