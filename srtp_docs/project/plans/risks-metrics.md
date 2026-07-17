---
title: Risk Register & Success Metrics
type: plan
field: project
created: 2026-07-06
updated: 2026-07-10
tags: [plan]
---

# Risk Register & Success Metrics

> **Part of:** [[plans-index|Plan Index]]
> **Last updated:** 2026-07-10 (updated based on comprehensive research pass)

## Risk Register

### Technical Risks

| # | Risk | P | I | Phase | Mitigation |
|---|------|---|---|-------|-----------|
| R1 | **MATLAB unavailable** — license not obtainable | M | H | P2 | PySpice + ngspice primary. Python PMSM behavioral model. MATLAB is optional upgrade. |
| R2 | **LLMs can't generate correct SPICE netlists** — syntax errors, non-convergence | M | C | P0 | Template-based generation (HAVEN pattern). LLMs fill parameters, don't write raw SPICE. Test Day 1. |
| R3 | **Coordination overhead > benefit** — multi-agent costs more but delivers same quality | M | H | P0-P1 | Phase 0 A/B test. Kill multi-agent if single-agent wins. Start with 3 agents, not 7. |
| R4 | **Simulation time dominates agent time** — 30-min sim makes iteration impractical | H | M | P2 | Analytical models for rapid screening. Surrogate models in P4 (stretch). Parallel batch simulation (SEPOC 2025 pattern). |
| R5 | **LangGraph checkpointing ≠ durable execution** — no auto-resume on crash | M | M | P4 | Watchdog process (poll every 60s). Idempotency keys. Manual resume fallback. |
| R6 | **No evaluation benchmark exists** — can't measure if we're good | H | M | P0 | Build benchmark in P0.4: 5 specs with published reference designs. Make it open-source. |
| R7 | **Nexar API rate limits** — 1,000 queries/month free tier | L | L | P3 | Cache aggressively. Components don't change often. Local component DB backup. |
| R8 | **PaperQA2 hallucinates citations** — cites non-existent papers | M | M | P3 | CitationChecker: cross-check every citation against arXiv API. Flag unverifiable. |
| R9 | **PySpice motor model insufficient** — behavioral PMSM not accurate enough | M | M | P2 | Validate against Simscape PMSM block. Accept 5-10% accuracy for screening; MATLAB for final verification. |
| R10 | **Provider API downtime** — DeepSeek/Claude/GPT unavailable during design | L | M | P1 | LiteLLM provider-agnostic: auto-failover between providers. Local fallback (Ollama) for non-critical tasks. |
| R11 | **SPICE model availability** — no SPICE models for automotive SiC MOSFETs | M | M | P0 | Start with generic VDMOS models. Add manufacturer models (Infineon, Wolfspeed provide SPICE). Behavioral models as fallback. |
| R12 | **Context window overflow** — state + SPICE netlist + results + review > context | M | M | P1 | Compaction at 70%. Store large results in files, not context. Summary before passing between agents. |

P = Probability (H/M/L), I = Impact (C=Critical, H=High, M=Medium, L=Low)

### Project Risks

| Risk | P | I | Mitigation |
|------|---|---|-----------|
| **Scope creep** — adding agents/features before baseline works | H | M | Phase gates: no Phase N+1 until Phase N acceptance met |
| **Dependency abandonment** — LangGraph/CrewAI/PaperQA2 unmaintained | L | H | MIT/Apache licensed — can fork. Monitor community health. |
| **Vault-research mismatch** — plans deviate from research findings | M | M | Audit every phase. Red-team every claim. Cross-reference plans against sources. |
| **Single developer bottleneck** — one person, many components | H | M | CLI-first (simpler than GUI). Off-the-shelf where possible (PaperQA2, ltspice-mcp, LiteLLM). |

---

## Success Metrics

### Phase Gates

| Phase | Metric | Target | Measurement |
|-------|--------|--------|-------------|
| **P0** | Single-agent designs working inverter | Simulation converges, efficiency > 90% | Benchmark spec TI-400-150 |
| **P0** | A/B test complete | Multi vs single comparison documented | Data, not opinions |
| **P1** | Multi-agent ≥ single-agent on benchmark | Efficiency + convergence rate compared | 3-spec benchmark run |
| **P1** | Guardrail catch rate | 100% of known-bad designs rejected | 10 injected bad designs |
| **P1** | Checkpoint recovery | Resume from exact failure point | Kill mid-sim, resume, verify state |
| **P2** | Simulation accuracy | Results within 5% of published reference | Tesla Model 3 approximate, Porsche Taycan |
| **P2** | Co-simulation converges | SPICE inverter + motor model runs end-to-end | Motor spins, steady-state reached |
| **P3** | Citation verification rate | ≥ 80% of citations are real papers | Manual audit of 20 citations |
| **P3** | Component selection accuracy | ≥ 90% have correct voltage/current ratings | Reviewer agent validation |
| **P4** | Autonomous runtime | 24+ hours without human intervention | Overnight benchmark run |
| **P4** | Watchdog auto-resume | ≥ 3 simulated failures auto-resumed | Integration test |
| **P4** | Design reproducibility | Same spec → same results within 1% | 3 repeated runs on TI-400-150 |

### Quality Metrics (End-State)

| Metric | Baseline (Manual) | Target (Agent) | Measured By |
|--------|-------------------|----------------|-------------|
| **Design quality** | Published baseline for voltage class | Efficiency ≥ baseline + 0.5% | Benchmark comparison |
| **Design throughput** | 12-18 months per design | < 1 hour per design | Wall clock for benchmark specs |
| **Design space explored** | 50-100 points (human) | 1,000+ points (agent) | Parameter sweep count |
| **Iterations to convergence** | 1-3 redesign cycles (weeks each) | ≤ 5 iterations (minutes each) | LangGraph state counter |
| **API cost per design** | N/A | < $5 | Token usage tracking |
| **Literature grounding** | Expert knowledge (tacit) | ≥ 3 real citations per design | Citation verifier |
| **Component reality** | Hand-picked from known vendors | ≥ 80% real MPNs with verified specs | Component validator |
| **Standards compliance** | Manual checklist (error-prone) | Automated guardrail checking | Guardrail violation log |
| **Reproducibility** | Varies by engineer | Same spec → same result within 1% | Repeated benchmark runs |

---

← [[plans-index|Plan Index]] | [[citations]] →
