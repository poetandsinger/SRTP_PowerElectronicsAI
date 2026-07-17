---
title: "Agentic Workflow Patterns — 2026 catalog mapped to SRTP"
type: topic
field: ai-agents
created: 2026-07-17
updated: 2026-07-17
status: unverified
evidence: single-study
tags: [ai-agents, multi-agent, architecture, patterns, orchestration, review, synthesis]
sources:
  - sources/ai-agents/analogsage-2025-self-evolving-analog-mas
  - sources/ai-agents/phia-lpcomda-2026-physics-informed-pe-agent
  - sources/ai-agents/drcy-2026-allspice-mas-review
  - sources/ai-agents/masrouter-2025-llm-routing
  - sources/ai-agents/context-engineering-2026
  - sources/ai-agents/pe-mas-flyback-mas
review_by: 2026-10-17
---

# Agentic Workflow Patterns — 2026 catalog mapped to SRTP

The vault's per-harness pattern list ([[ai-agents/harness/architecture-patterns]]) predates the canonical 2026 workflow vocabulary. This note pins that vocabulary down, maps SRTP onto it, and records the deliberate exclusions.

> **Governing distinction (Anthropic *Building Effective Agents*; 2026 guides):** a **workflow** orchestrates LLMs + tools through *predefined code paths*; an **agent** directs its own process at runtime. Prefer the simplest that works. SRTP is a workflow, not an autonomous agent — keep it so until a measured need forces otherwise.

## 1. The six patterns

| # | Pattern | Use when |
|---|---------|----------|
| P1 | **Prompt chaining** — fixed sequence, each step feeds the next | decomposition known and stable |
| P2 | **Routing** — classify input → dispatch to a path | inputs fall into distinct kinds |
| P3 | **Orchestrator–workers** — plan subtasks at runtime, fan out, synthesize | subtasks not known upfront; parallelizable |
| P4 | **Evaluator–optimizer** — generator proposes → separate judge scores on explicit criteria → revise | quality measurable, first try won't be right |
| P5 | **Reflection** — agent critiques/revises its own output | self-contained, no external judge needed |
| P6 | **Tool use / ReAct** — reason → call tool → observe → repeat | grounding in external state |

*Sources: Anthropic "Building Effective Agents"; 2026 pattern catalogs (sitepoint, augmentcode, huggingface/dcarpintero) — the six recur across all surveyed.* Production systems compose them (orchestrator top level, reflection in workers, evaluator-optimizer at gates, tool-use throughout).

## 2. SRTP mapping

| SRTP element ([[project/plans/ai-agent-mas-plan]]) | Pattern | Status |
|---|---|---|
| PLAN → DESIGN → VALIDATE → REPORT | P1 chaining | explicit |
| Orchestrator parses new-vs-iterate, routes stages | P2 routing (explicit, not learned) | explicit |
| Validator (k=3 consensus) + `iterate` edge | P4 evaluator–optimizer | **used; make first-class (§3)** |
| Planner grounding on retrieved papers; PLECS sweeps | P6 tool use | explicit |
| Parameter search → converged values | inner optimizer | **missing → [[ai-agents/design-loop-architecture]]** |

SRTP is a **prompt-chain workflow with an evaluator-optimizer gate** — the right shape. The design-loop's missing numerical optimizer is treated in [[ai-agents/design-loop-architecture]]; this note covers the pattern discipline around it.

## 3. Evaluator–optimizer as first-class

The `VALIDATE --fail--> re-plan/re-design` edge is an evaluator–optimizer loop. It earns its keep only with a **separate judge** and **explicit criteria** (DRCY — [[sources/ai-agents/drcy-2026-allspice-mas-review]]); otherwise "iterate" is vibes. SRTP already has the materials: evidence gates = rubric, k=3 consensus = judge, Planner/Designer = optimizer. Obligations that follow:
- judge runs on a **different model/context** from the generator;
- loop needs a **stopping rule** + **best-so-far** tracking (PE-MAS `best_design_candidate`);
- each iteration **compacts** its reasoning trace or context reinflates ([[sources/ai-agents/context-engineering-2026]]).

Wired into [[project/plans/design-loop]] and [[project/plans/guardrails-and-evidence]].

## 4. Exclusions (each with a re-open trigger)

| Excluded | Reason | Re-open if |
|---|---|---|
| Autonomous / runtime task discovery | subtasks are known (topology→params→validate); adds routing-failure surface | tasks become genuinely open-ended |
| Learned routing (MasRouter) | coding-benchmark result; explicit map suffices at 3–4 stages | measured routing errors |
| Deep recursion (subagents spawning subagents) | one delegation level covers the workflow ([[ai-agents/multi-agent-synthesis]] §1) | a subtask needs its own team |
| Debate / group-chat (AutoGen) | multiplies tokens; AutoGen EOL. A ranked, cited topology comparison gets ~90% | topology ties can't be broken by ranking |

## 5. Decision

Prompt-chain + evaluator-optimizer + tool-use, flat delegation, explicit routing. Name the evaluator-optimizer loop (§3); add the numerical optimizer ([[ai-agents/design-loop-architecture]]); defer the rest against the triggers above.

## Red Team
**Steelman against:** naming patterns is documentation, not engineering — PE-MAS shipped without this vocabulary. **How it could be false:** if the `iterate` edge already behaves as a disciplined evaluator-optimizer, formalizing changes nothing. **What would change my mind:** a Phase-0 run where the un-named loop converges with a stopping rule and compacted traces. **Residual doubt:** the substantive gap is the missing optimizer, not the missing names; the naming matters only insofar as it forces the judge/stopping-rule/compaction obligations into the build.

← [[ai-agents/multi-agent-synthesis]] | [[ai-agents/design-loop-architecture]] | [[ai-agents/harness/architecture-patterns]] | [[project/plans/ai-agent-mas-plan]]
