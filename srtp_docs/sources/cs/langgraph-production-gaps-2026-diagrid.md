---
title: "Why Checkpoints Aren't Durable Execution — LangGraph, CrewAI, Google ADK Production Gaps"
authors: [Yaron Schneider]
year: 2026
venue: "Diagrid Blog (February 2026)"
url: "https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows"
captured: 2026-07-10
reliability: medium
peer_reviewed: false
motivated: true
reliability_note: "Industry blog post by Diagrid CTO. Diagrid sells Dapr (competing durable execution platform) — motivated source. However, the technical analysis of LangGraph's checkpointing limitations is specific, verifiable, and consistent with LangGraph's own documentation."
sha256: placeholder
---

# LangGraph Checkpointing: Not Durable Execution

## Core Argument

LangGraph's checkpointing saves state at every superstep, but this is **NOT durable execution**. The distinction matters critically for production multi-agent systems, including the SRTP project.

## The Gap

| Feature | LangGraph Checkpointing | Durable Execution (Dapr) |
|---------|------------------------|--------------------------|
| **Automatic failure detection** | ❌ No supervisor, watchdog, or heartbeat | ✅ Built-in |
| **Automatic resumption** | ❌ Developer must detect failure and manually re-invoke | ✅ Runtime handles it |
| **Duplicate execution prevention** | ❌ No distributed locking | ✅ At-least-once with dedup |
| **Multi-process execution** | ❌ Single-process only | ✅ Distributed task queue + worker pool |

## Key Failures at Production Scale

1. **No automatic failure detection** — if the process crashes, the graph sits in Postgres until someone notices
2. **No automatic resumption** — you must write custom code to detect stuck graphs and re-invoke them
3. **Exactly-once semantics** — no built-in mechanism to prevent replay of already-executed nodes
4. **Single-process only** — can't distribute agent nodes across machines for parallel simulation

## Relevance to SRTP

The SRTP implementation plan relies on LangGraph checkpointing as "non-negotiable" for simulation fault tolerance. This article identifies a critical gap:

- **What we claimed:** Checkpointing = fault tolerance for expensive simulations
- **Reality:** Checkpointing = state saved, but YOU must detect the failure, resume it, and handle duplicates
- **Impact:** For a MATLAB simulation that crashes at sweep 47/100, the agent won't automatically resume — we need custom watchdog logic

## Mitigation for SRTP

1. **Implement a watchdog process** that polls for stuck graphs (no state transition in > T_timeout)
2. **Idempotency keys** on simulation runs (hash of parameters) to prevent duplicate execution
3. **Manual resume workflow** — if auto-resume fails, human-in-the-loop picks up from checkpoint
4. **Consider Dapr Workflows** as a future migration path if LangGraph checkpointing proves insufficient

## Epistemic Status

- Technical analysis is verifiable against LangGraph docs — the limitations described are real
- Author is motivated (selling Dapr) but the analysis is specific and falsifiable
- Does not invalidate LangGraph for SRTP — just adds requirements we didn't plan for
