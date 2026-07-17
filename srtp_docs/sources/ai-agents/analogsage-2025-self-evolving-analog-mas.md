---
title: "AnalogSAGE: Self-evolving Analog Design Multi-Agents with Stratified Memory and Grounded Experience"
type: source
field: ai-agents
tags: [ai-agents, multi-agent, architecture, design-automation, simulation, review, preprint]
authors: [Zining Wang, Jian Gao, Weimin Fu, Xiaolong Guo, Xuan Zhang]
year: 2025
venue: "arXiv preprint 2512.22435 (Northeastern U., Kansas State U.)"
arxiv: "2512.22435"
url: "https://arxiv.org/html/2512.22435"
captured: 2026-07-17
reliability: medium
peer_reviewed: false
reliability_note: "arXiv preprint (Dec 2025), open-source code released. Strong quantitative benchmark vs 3 baselines but single-team, op-amp-only, un-refereed. Adjacent domain (analog IC, not power electronics) — pattern-transferable, not directly domain-matched."
---

# AnalogSAGE — Self-evolving Analog Design Multi-Agents (Dec 2025)

**Why it matters for SRTP:** the strongest current template for the exact flow we want (topology → refine → parameter-optimize) *and* for a memory architecture far more sophisticated than what our synthesis currently specs. Adjacent domain (analog op-amps), so **C3 pattern evidence**, not domain-matched proof.

## Three sequential agents (maps onto our topology→component→sim flow)
1. **Topology Selection Agent** — spec → architecture via memory context + retrieval from a topology database (50 candidates).
2. **Topology Refinement Agent** — localized structural edits (bias networks, compensation paths) to fix issues.
3. **Parameter Optimization Agent** — numerical device values via **Bayesian optimization + circuit simulation** (ngspice, SKY130 PDK).

Closed-loop: topology → refine → param-opt, with feedback re-entry when specs fail (max 3 iterations, matched to baselines).

## Stratified self-evolving memory (4 layers) — the transferable novelty
- **Evolution Memory** — cross-task design insights (effective topology choices, compensation strategies) as concise summaries.
- **Introspective Optimization** — within-task failure reflections ("why it failed").
- **Stage Context Fusion** — a Compression Module that compresses reasoning traces to stay under context limits (echoes SCALE/AgentSlimming token-reduction).
- **Analog Design Experience** — grounding via three modules: *Candidates* (vector-DB topology retrieval), *Knowledge* (**RAG over ~10,000 ISSCC papers, 1955–2024**), *Numerical* (Bayesian-opt + ngspice feedback).

This is a concrete answer to two SRTP open questions: how memory should work across design iterations, and how to ground topology reasoning in literature (RAG over a large corpus) rather than raw LLM training knowledge.

## Results (10 op-amp tasks, easy→hard)
| Metric | AnalogSAGE | Artisan-style | AnalogCoder-Pro | SPICEPilot |
|---|---|---|---|---|
| Pass rate | **100%** | 70% | 10% | 0% |
| Pass@1 | **96%** | 46% | 2% | 0% |
| Param search space | 0.26× | — | — | — |

→ 10× pass rate, 48× Pass@1, 4× search-space reduction vs baselines. Models: Gemini-2.5-flash + text-embedding-3-large.

## SRTP implications
- **Adopt the 3-stage decomposition** (topology → refine → parameter) — it is emerging as the field-standard analog/PE agent structure (see also PHIA, AnalogAgent) and matches our topology→component→simulate workflow.
- **Upgrade our memory model.** Current SRTP synthesis specs CrewAI unified memory + PE-MAS lifelong memory; AnalogSAGE shows the 2026 SOTA is *stratified* (cross-task evolution + within-task introspection + compression + RAG-grounded experience). Strong candidate to adopt.
- **RAG-grounded topology reasoning** (10k-paper corpus) directly addresses the red-team's "training-knowledge dependence" objection to our EE notes.

## Caveats
Op-amp-only; generalization unproven; depends on a curated topology DB + knowledge corpus; 3-iteration cap; tied to SKY130/ngspice. No power-electronics or motor-drive evidence. Do **not** cite as proof for traction inverters — cite as the pattern to adapt. See [[ai-agents/multi-agent-synthesis]] and [[ai-agents/traction-inverter-mas-integration]].
