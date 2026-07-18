---
title: AI-Agent Docs Audit — 2026-07-17
type: audit
field: project
created: 2026-07-17
updated: 2026-07-17
tags: [audit, ai-agents, multi-agent]
---

# AI-Agent Docs Audit — 2026-07-17

**Scope:** audit of the `ai-agents/` notes, the AI-agent-facing `project/plans/`, and the `sources/ai-agents/` captures, against the project goal — **a multi-agent system (MAS) for traction inverter design** — plus a fresh 2026 research pass. No gaps hidden.

**Summary:** the AI-agent research is broad, well-structured, and red-teamed, but it is (1) **anchored to MATLAB**, which the project has now abandoned in favor of **PLECS**; (2) **internally contradictory** on agent count (7 vs 3); (3) **inflating confidence** off coding-benchmark papers; and (4) **~1 week to several months stale** on framework facts. The good news: the MATLAB→PLECS pivot is a *technical upgrade*, and three of the old "open gaps" are now largely closed by fresh evidence.

---

## 1. MATLAB anchoring — the biggest problem (now obsolete)

- **~350 MATLAB/Simulink mentions across ~30 notes.** The architecture has a first-class **"MATLAB Agent"** ([[traction-inverter-mas-integration]] §3.2, [[multi-agent-synthesis]] §4), a MATLAB-centric tech stack ([[implementation-research]] §1.1), and a whole harness note (now [[plecs-integration]], formerly matlab-integration with 57 MATLAB mentions) that was dedicated to MATLAB+agents.
- The bridge note §5 explicitly justifies "MATLAB/Simulink primary, PLECS optional — MATLAB is the industry standard." **That rationale is now inverted.** [[pe-mas-flyback-mas]]'s own note ended with "keep our differentiation: MATLAB/Simulink (not PLECS)" — exactly backwards after the pivot.
- **The pivot is an upgrade, not a downgrade** (see [[plecs-xmlrpc-scripting-interface]], [[plecs-ai-agent-integration-ordonez]], PE-MAS re-clone): PLECS has a scriptable XML-RPC/JSON-RPC backend, native PMSM/induction-machine + FOC traction demo models, and a **working MCP prior art** inside PE-MAS. → **Action: Task #5 pivot.**

## 2. Internal contradiction: 7 agents vs 3 agents (never reconciled)

- [[traction-inverter-mas-integration]] specs a **7-agent** architecture (adds Topology, Thermal, Multi-Physics Coordinator) at **C2 confidence** and even admits (§7 red-team) it's "second-system effect."
- [[implementation-research]] §A2 says **start with 3** (Orchestrator, Sim, Reviewer). Both dated 2026-07-10. **The vault simultaneously recommends 3 and 7 with no resolution.**
- **New evidence breaks the tie toward minimal:** AgentSlimming (ACL 2026, verified) shows automated MAS bloat wastes tokens quadratically and prunes 78.9% with no loss ([[agent-frameworks-2026-currency]]). Ordonez's real PLECS agent did useful work with essentially one agent + scaffolding ([[plecs-ai-agent-integration-ordonez]]). → **The plan must commit to 3, with specialists earned, not assumed.**

## 3. Confidence inflation off domain-mismatched benchmarks

- The bridge §2.5 claims the hybrid LangGraph-CrewAI result "**upgrades our architecture from C3 to C4**." That paper's 96.1%/76.2% numbers are from a **100-agent coding benchmark**. A coding-benchmark result does **not** upgrade a *traction-inverter-domain* architectural claim. This is Goodharting our own confidence scale.
- "76.2% token reduction" and "96.1% success" recur across notes as if domain-validating. They are not. The status stays **C3** until a power-electronics A/B test exists.
- "Multi-Agent LLM Control (6 agents, ~3000 tokens, <2% error)" is flagged "suspiciously cheap" yet still used as P1 support. Keep the flag louder.

## 4. Cited-but-not-captured sources (evidence hygiene)

Named in the notes with no source capture, i.e. unverifiable as written:
- **Osprey Framework** (Berkeley Lab, "production LangGraph") — load-bearing for P2/P8; never captured.
- **Electrical Design MAS + RAG** (42.7% cycle reduction) — C2, uncaptured.
- **DNN+NSGA-III cooling, ANN thermal (<3.5%/1s), MOO-EMC (100M/48h)** — the C4 "surrogate works" pillar rests on these; **none captured**.
- **SEPOC 2025 LLC framework, HAVEN template pattern** — cited as proof PySpice works / templates de-risk netlists; uncaptured.
- **SCALE, SlowBurn, Q-planner** (token-reduction) — cost story depends on them; only **AgentSlimming** is now verified (ACL 2026). Treat the rest as **[unverified]** until captured or downgrade the cost claims.

## 5. Staleness (all AI-agent notes dated 2026-07-09/10)

- **Framework facts have already moved** ([[agent-frameworks-2026-currency]]): LangGraph 1.0 (Oct 2025) + Q2-2026 durable streaming/timeouts **partially supersede** the Diagrid "checkpointing ≠ durable" concern; Microsoft Agent Framework 1.0 (Apr 2026, native MCP+A2A) is the AutoGen successor; CrewAI 1.14.
- The 2026 **analog-EDA multi-agent wave** (AnalogSAGE, AnalogAgent, RFAmpDesigner, SABLE, EEsizer) post-dates the synthesis and is absent. Only [[analogsage-2025-self-evolving-analog-mas]] now captured.

## 6. Gaps CLOSED by this research pass (update the notes)

- **G1 (no PMSM/IPMSM in SPICE)** → **closed.** PLECS ships native PMSM (incl. saturation lookup), induction machines, and FOC traction demos. This was the main reason MATLAB was "needed"; it evaporates.
- **G2 (surrogate needs 1000+ sims)** → **largely closed.** PHIA/LP-COMDA physics-informed PINN surrogates hit strong accuracy at **~10 samples** ([[phia-lpcomda-2026-physics-informed-pe-agent]]). Surrogates can move to Phase 1–2, not Phase 4.
- **G5 (LLMs can't write SPICE netlists)** → **mostly moot** under PLECS: the agent tunes a **template via `plecs.set`/`ModelVars`** and does XML injection over a base model (PE-MAS `PLECSGenerator`), not free-form netlist authoring.

## 7. The scoping fact everything should hinge on

From the only direct AI+PLECS prior art ([[plecs-ai-agent-integration-ordonez]]): an agent reliably does **parameter sweeps, control-code refactoring, comparative analysis** — and does **not** do **topology design, control-strategy selection, physics interpretation, literature review**. **That boundary is the SRTP value proposition.** The MAS must supply exactly the reasoning the coding-agent cannot; if it doesn't, it degrades to a sweep runner. Token economics are existential: raw waveforms bankrupt the loop; engineered ~36-number summaries are ~1000× cheaper.

## 8. Genuine remaining gaps (not yet filled)

1. **Traction-inverter PLECS model availability.** Per PE-MAS's `model_registry.json`, *validated per-topology models are the bottleneck*, not the agent. There is **no plan** to build/validate PLECS models for 2L-B6, 3L-NPC, 3L-TNPC, ANPC + PMSM/IM load. This is the critical path.
2. **Measured token cost of the actual loop.** PHIA doesn't report it; Ordonez is anecdotal. We have no SRTP-measured cost.
3. **An analog-EDA-MAS synthesis note.** The 3-stage (topology→refine→param-opt) + stratified self-evolving memory pattern is now field-standard; only partially captured.
4. **PLECS licensing for automation.** XML-RPC works in installed PLECS 4.8, but confirm the license permits headless/scripted batch use.

---

## Action register

| # | Finding | Action | Task |
|---|---------|--------|------|
| 1 | MATLAB anchoring | Pivot all sim-backend framing to PLECS; rewrite `matlab-integration` harness note | #5 |
| 2 | 7 vs 3 agents | Plan commits to 3-agent core; specialists earned | #6 |
| 3 | Confidence inflation | Downgrade coding-benchmark "C4" claims back to C3 in bridge §2.5 | #5/#6 |
| 4 | Uncaptured sources | Mark [unverified]; capture or downgrade dependent claims | later |
| 5 | Staleness | Fold framework currency + G1/G2/G5 closures into notes | #5 |
| 6 | Structure | Fix duplicate §4/§5 headings in multi-agent-synthesis | #5 |
| 7 | Model bottleneck | Add traction-inverter PLECS-model build+validate track to plan | #6 |

← [[harness-index]] | [[traction-inverter-mas-integration]] | [[implementation-research]]
