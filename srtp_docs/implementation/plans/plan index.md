# Implementation Plan — Index

> **Single source of truth for implementation.** Each phase links to a detailed subplan.
> **Audience:** Programmers
> **Architecture:** CLI-first Python agent → optional MATLAB backend → optional GUI
> **Last updated:** 2026-07-10 (rewritten based on comprehensive 2026 research pass)

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────┐
│                  CLI / Python API                     │
├─────────────────────────────────────────────────────┤
│  ORCHESTRATOR (LangGraph StateGraph + SQLite checkpoints)
│       │              │              │
│  ┌────┴────┐   ┌─────┴─────┐  ┌────┴─────┐
│  │LIT AGENT│   │SIM AGENT  │  │REVIEWER  │
│  │PaperQA2 │   │PySpice/   │  │3-run     │
│  │arXiv    │   │MATLAB(MCP)│  │consensus │
│  └─────────┘   └───────────┘  └──────────┘
├─────────────────────────────────────────────────────┤
│  INFRASTRUCTURE: LiteLLM │ SQLite+LanceDB │ Guardrails │
├─────────────────────────────────────────────────────┤
│  EXTERNAL: PySpice │ ltspice-mcp │ Nexar API │ arXiv │
└─────────────────────────────────────────────────────┘
```

**Design principles (from research):**
- **CLI-first:** Validate the agent works before building a GUI
- **3 agents, not 7:** Start simple. Add specialists only when proven necessary.
- **PySpice primary, MATLAB optional:** Free, open-source, Python-native. MATLAB as upgrade path.
- **A/B test in Phase 0:** Single-agent vs multi-agent on same tasks. Kill multi-agent if single wins.
- **Template-based generation:** LLMs fill SPICE templates, don't generate raw netlists (HAVEN pattern).
- **Multi-run consensus:** Reviewer runs 3× independently, reconciled (DRCY pattern).

---

## Phase Map

| Phase | Plan | Goal | Duration | Key Deliverable |
|:-----:|------|------|----------|-----------------|
| 0 | [[phase-0-foundation]] | **Foundation + A/B test.** Single agent proves the concept. Multi-agent tested against it. | 2 weeks | Single agent designs a working inverter in simulation |
| 1 | [[phase-1-multi-agent]] | **Multi-agent core.** 3-agent LangGraph system with checkpointing, guardrails, evidence gates. | 3 weeks | Multi-agent matches or beats single-agent on benchmark |
| 2 | [[phase-2-simulation]] | **Simulation depth.** MATLAB/Simulink backend, PySpice device-level, ltspice-mcp integration. | 3 weeks | System-level + device-level co-simulation |
| 3 | [[phase-3-knowledge]] | **Knowledge + components.** Literature agent (PaperQA2), component agent (Nexar API), memory. | 2 weeks | Agent selects real components from catalogs, cites papers |
| 4 | [[phase-4-production]] | **Production hardening.** Watchdog, human-in-the-loop, evaluation benchmark, packaging. | 2 weeks | 24h autonomous operation, published benchmark results |

**Total: 12 weeks (was 8 in old plan — expanded for research rigor)**

### Phase Dependency Graph

```
Phase 0 ──→ Phase 1 ──→ Phase 2
              │            │
              └──→ Phase 3 ←──┘
                       │
                       └──→ Phase 4
```

Phase 2 and 3 can partially overlap (simulation backend work is independent of literature/component API work).

---

## What Changed From the Old Plan (2026-07-09)

| Dimension | Old Plan | New Plan | Why |
|-----------|----------|----------|-----|
| **First deliverable** | PySide6 GUI window | CLI agent designs inverter | Validate the agent, not the UI |
| **Simulation engine** | MATLAB/Simulink only | PySpice primary, MATLAB optional | Free, no license dependency |
| **Agent count** | 5-7 agents from start | 3 agents (Orch, Sim, Reviewer) | EvoAgent: human-designed roles suboptimal; start simple |
| **Phase count** | 8 phases (P0-P7) | 5 phases (P0-P4) | Collapsed GUI phases into one; added A/B test |
| **GUI timeline** | Phase 0 | Phase 4+ (stretch) | Agent capability > visual polish |
| **A/B testing** | Implicit (Phase 0 "baseline") | Explicit (Phase 0 deliverable) | Red-team identified this as critical gap |
| **Token budget** | Not specified | SlowBurn backpressure pattern | ACL 2026 research: budget enforcement matters |
| **Consensus** | Single review pass | 3-run DRCY consensus pattern | Production deployment at Fortune 500 |
| **Component DB** | Unspecified | Nexar GraphQL (verified API) | Researched and validated 2026-07-10 |
| **Literature** | Unspecified RAG | PaperQA2 (verified API) | Superhuman performance on scientific QA |
| **Surrogate models** | Phase 4 (original) | Phase 4 (stretch) | Need simulation data first |

---

## Risk Register

| # | Risk | P | I | Mitigation |
|---|------|---|---|------------|
| R1 | MATLAB unavailable | M | H | PySpice primary. MATLAB optional upgrade path. |
| R2 | LLMs can't generate SPICE netlists | M | C | Template-based generation (HAVEN pattern). Test in Phase 0 day 1. |
| R3 | Coordination overhead > benefit | M | H | Phase 0 A/B test. Kill multi-agent if single-agent wins. |
| R4 | Simulation time dominates agent time | H | M | Analytical models for screening. Surrogates in Phase 4. |
| R5 | LangGraph checkpointing ≠ durable execution | M | M | Watchdog + idempotency + manual resume (Phase 4). |
| R6 | No evaluation benchmark exists | H | M | Build benchmark in Phase 0. 3-5 specs with published references. |
| R7 | Nexar API rate limits | L | L | Cache aggressively. Components don't change often. |
| R8 | PaperQA2 hallucinates citations | M | M | Cross-check with arXiv API. Flag unverifiable citations. |

P = Probability (H/M/L), I = Impact (C=Critical, H=High, M=Medium, L=Low)

---

## Success Metrics

| Metric | Target | Phase | Measurement |
|--------|--------|-------|-------------|
| **Single-agent baseline** | Designs working inverter (converges in simulation) | P0 | Simulation convergence + efficiency > 90% |
| **Multi-agent ≥ single-agent** | Multi-agent produces better or equal designs on benchmark | P1 | A/B test: 3-spec benchmark |
| **Component selection accuracy** | ≥ 90% of selected components have correct voltage/current ratings | P3 | Reviewer agent validation |
| **Literature citation rate** | ≥ 80% of claims cite a real, retrievable paper | P3 | Manual audit of 20 claims |
| **Time to first design** | < 30 minutes from spec to simulation results | P1 | Wall clock for benchmark specs |
| **Autonomous runtime** | 24+ hours without intervention | P4 | Overnight run on benchmark suite |
| **Checkpoint recovery** | Resume from exact failure point | P1 | Integration test: kill mid-sim, resume |
| **API cost per design** | < $5 | P1 | Token usage tracking |
| **Guardrail catch rate** | 100% of physically impossible designs rejected | P1 | Inject 10 known-bad specs, verify rejection |

---

## Supporting Documents

| Document | Purpose |
|----------|---------|
| [[implementation/plans/architecture]] | Why standalone, architecture diagram |
| [[implementation/plans/tech-stack]] | Complete technology choices |
| [[cs/implementation-research]] | **NEW:** Implementation research: API specifics, code patterns, verified technologies |
| [[cs/traction-inverter-mas-integration]] | Integration architecture: 7-agent design, guardrails, evidence gates |
| [[cs/multi-agent-synthesis]] | Multi-agent patterns from 7 harnesses + 10 papers |
| [[cs/harness/comparative-analysis]] | Feature matrix across all agent harnesses |
| [[ee/problem-statement/problem statement index]] | Why this project exists |
| [[citations]] | Master bibliography |
| [[_lint/multi-agent-traction-inverter-audit-2026-07-10]] | Latest audit report |

---

← [[README]] | [[implementation/plans/phase-0-foundation]] →
