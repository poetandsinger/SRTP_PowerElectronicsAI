---
title: "MasRouter: Learning to Route LLMs for Multi-Agent Systems"
authors: [Yanwei Yue, Guibin Zhang, Boyang Liu, Guancheng Wan, Kun Wang, Dawei Cheng, Yiyan Qi]
year: 2025
venue: "arXiv preprint"
arxiv: "2502.11133v1"
captured: 2026-07-09
reliability: medium
peer_reviewed: false
reliability_note: "Preprint (Feb 2025). Not yet peer-reviewed. Authors from multiple institutions; results on standard coding benchmarks (HumanEval, MBPP) — may not generalize to domain-specific simulation routing."
sha256: placeholder
---

# MasRouter: Learning to Route LLMs for Multi-Agent Systems

## Core Problem

Multi-Agent System Routing (MASR): given a task, determine which collaboration mode, agent roles, and LLM models to use. Prior work routed LLMs for single agents; MASR extends this to the multi-agent setting.

## Architecture

Cascaded controller network with three stages:
1. **Collaboration mode determination** — sequential vs parallel vs debate
2. **Role allocation** — which agents with which responsibilities
3. **LLM routing** — which model serves each role

## Key Results

- **Performance:** 1.8%–8.2% improvement over SOTA on MBPP
- **Cost:** Up to 52.07% overhead reduction vs SOTA on HumanEval
- **Plug-and-play:** Integrates with mainstream MAS frameworks; 17.21%–28.17% overhead reduction via customized routing
- **Code:** https://github.com/yanweiyue/masrouter

## Relevance to SRTP

**Directly addresses the orchestrator routing gap identified in our synthesis.** The synthesis claimed "one-level delegation covers 90% of workflows" without evidence. MasRouter shows:
1. Routing IS a recognized research problem (validates our red-team concern)
2. Learning-based routing outperforms static routing
3. Cost reduction from intelligent routing is significant (~28–52%)

**Critical limitation:** All results are on code generation benchmarks (HumanEval, MBPP). No evidence MasRouter works for domain-specific simulation workflows. The MATLAB simulation routing problem (deciding whether to simulate, which solver, which topology) is structurally different from coding tasks.

## Epistemic Status

- MasRouter demonstrates routing is solvable → weakens the "orchestrator routing is unsolved" red-team argument
- But results are on a different domain → doesn't fully address our concern
- Overall: MasRouter suggests routing CAN work, but we don't know for simulation tasks
