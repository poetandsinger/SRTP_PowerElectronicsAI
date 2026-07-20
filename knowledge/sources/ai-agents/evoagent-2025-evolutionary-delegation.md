---
title: "EvoAgent: Towards Automatic Multi-Agent Generation via Evolutionary Algorithms"
type: source
field: ai-agents
tags: [ai-agents]
authors: [Siyu Yuan, Kaitao Song, Jiangjie Chen, Xu Tan, Dongsheng Li, Deqing Yang]
year: 2024
venue: "NAACL 2025 (accepted main conference paper)"
arxiv: "2406.14228v3"
captured: 2026-07-09
reliability: high
peer_reviewed: true
reliability_note: "Accepted at NAACL 2025 main conference. Peer-reviewed."
sha256: placeholder
---

# EvoAgent: Automatic Multi-Agent Generation via Evolutionary Algorithms

## Core Problem

Existing multi-agent systems depend on **human-designed frameworks** (hand-crafted roles, static routing). This limits scalability and functional scope. EvoAgent asks: can agents be automatically generated and optimized via evolution?

## Architecture

Evolutionary algorithm applied to agent configuration:
1. **Initial individual** — existing single-agent framework
2. **Mutation** — modify agent settings (roles, prompts, tools)
3. **Crossover** — combine traits from successful agents
4. **Selection** — keep highest-performing configurations
5. Iterate → diverse multi-agent population emerges

## Key Claims

- "Significantly enhance the task-solving capability of LLM-based agents"
- "Can be generalized to any LLM-based agent framework"
- Accepted at NAACL 2025 (peer-reviewed)

## Relevance to SRTP

**Orthogonal approach to our hand-designed 5-role system.** Our synthesis follows the CrewAI pattern (human-designed roles: Orchestrator, Literature, MATLAB, Reviewer, Writer). EvoAgent suggests an alternative: let evolution discover the optimal agent configuration.

**Implication for our design:**
- Our 5-role system is a reasonable starting point (human-designed baseline)
- EvoAgent provides a path to optimization: if the 5-role system underperforms, evolutionary search could discover better agent configurations
- The claim "human-designed frameworks limit scalability" is a direct challenge to our approach

## Epistemic Status

- Peer-reviewed (NAACL 2025) → higher reliability than MasRouter
- But the evolutionary approach adds significant computational cost — running N agent configurations to find the best one
- For expensive simulation workflows (each MATLAB run costs minutes), evolutionary search may be prohibitively expensive
