---
title: "Plan — Evaluation, benchmark, open questions & risks"
type: plan
field: project
created: 2026-07-17
updated: 2026-07-19
tags: [plan, ai-agents, benchmark, plecs]
---

# Evaluation, benchmark, open questions & risks

> Topic of [[plan-ai-agent-mas]]. How we know the system works, and what could sink it. No phases — this is the standing evaluation contract the workstreams are measured against.

## 1. The benchmark (build it early — it is the ruler)

A **traction-inverter design benchmark**: 3–5 specs, each with a **published/teardown reference design** ([[index-reference-designs]] — 2L-B6-SiC anchor, Wolfspeed 300 kW, Tesla Model 3, Nissan Leaf). For each spec, measure the system's design vs the reference on: **η, THD, Tj margin, BOM cost, % claims cited, $/design, wall-clock, iterations to converge.** Publish it — no standard traction-inverter design benchmark exists; this is a contribution in itself.

## 2. The A/B that justifies the whole architecture

**Single well-tooled agent vs the 3-agent MAS on the same specs.** The multi-agent premise is unproven for this domain (PE-GPT's single-agent success is the standing counter-example — [[claim-multi-agent-outperforms-single]]). Metrics: design quality (above) + $/design + time. Decision rule stated up front:
- MAS ≥ single on quality **and** within a tolerable cost multiple → MAS justified.
- single ≥ 95 % of MAS quality at <50 % cost → **collapse toward single-agent**; don't build specialists.

## 3. Open questions

1. Does the 3-agent MAS beat a single agent for traction-inverter design? (the A/B)
2. Measured **$/design** and tokens/iteration of the real loop? (unmeasured anywhere in the literature — [[ai-agent-docs-audit-2026-07-17]] §8)
3. What is the **free-parameter dimensionality** of a real spec once topology+module are fixed — i.e. does stage ③ need BO/DE or does a grid suffice? ([[design-loop-architecture]])
4. Is the local corpus thick enough to ground **both** 2L-B6 and ANPC? (coverage audit — [[plan-knowledge-rag]])
5. Which specialist, if any, is *earned* by a recurring failing gate?

## 4. Risks

| Risk | Mitigation |
|---|---|
| **Validated PLECS models are the bottleneck** | explicit model-validation procedure + registry gates evidence ([[plan-plecs-harness]]) |
| **PLECS license blocks scripted batch** | **verify day one** — hard blocker |
| **Design loop never converges (no optimizer)** | explicit stage-③ optimizer + best-candidate + stopping rule ([[plan-design-loop]]) |
| RAG corpus too thin to ground decisions | seed from vault sources; coverage audit surfaces gaps early |
| Token blowup | summarize-before-LLM + no-LLM optimizer + trace compaction ([[plan-tech-stack]] §2) |
| Multi-agent overhead > benefit | the A/B; prune (AgentSlimming) |
| Confidence inflation from adjacent-domain papers | hold domain claims at C3 until a PE A/B exists |
| Gate-Goodharting | citation gate + human signoff backstop ([[plan-guardrails-and-evidence]] §4) |

## 5. Definition of done (first milestone, not a phase)

One **validated 2L-B6-SiC + PMSM** design produced from a prompt, every design claim cited from the local corpus, all evidence gates closed against a **validated** model, and **$/design measured** — with the single-vs-MAS A/B run on that same spec. Everything else (topology breadth, ANPC, earned specialists, hardening) extends from there, by dependency, not by calendar.

← [[plan-ai-agent-mas]] | [[plan-design-loop]] | [[index-reference-designs]]
