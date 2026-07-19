---
title: "PHIA / LP-COMDA: Physics-Informed LLM-Agent for Automated Modulation Design in Power Electronics"
type: source
field: ai-agents
tags: [ai-agents, design-automation, simulation, power-factor, mpc, preprint, engineering-ai]
authors: [Junhua Liu, Fanfan Lin, Xinze Li, Kwan Hui Lim, Shuai Zhao]
year: 2026
venue: "AAAI 2026 (arXiv 2411.14214); same group as PE-GPT"
arxiv: "2411.14214"
url: "https://arxiv.org/html/2411.14214v1"
captured: 2026-07-17
reliability: high
peer_reviewed: true
motivated: true
reliability_note: "AAAI 2026 (peer-reviewed) from the PE-GPT author group (Lin, Li, Zhao). In-domain power electronics (DAB DC-DC modulation), not traction inverter — adjacent topology class. `motivated`: same group advancing its own agent line, but the user study (20 practitioners) and 12-baseline modeling comparison are substantive."
---

# PHIA / LP-COMDA — Physics-Informed LLM-Agent for PE Modulation Design (AAAI 2026)

**Why it matters most:** it is the concrete answer to SRTP gap **G2 (surrogate training-data)**. Physics-informed neural surrogates work in the **low-data regime (10 samples)** — killing the red-team objection that surrogates need 1000+ simulations before they're useful.

## Architecture (planner + physics-informed tools + optimizer)
- **Planner:** GPT-4 parses requirements, coordinates the workflow (chat interface).
- **Surrogate tools — hierarchical PINNs:**
  - **ModNet** — switch-level model (layer-normalized GRU) learning switching behavior → predicts intermediate voltages (vp, vs).
  - **CirNet** — system-level model (LN-GRU) embedding **Kirchhoff / Faraday / Gauss** laws → predicts states (iL, vC1, vC2).
- **Optimizers:** PSO, Differential Evolution, Genetic Algorithms over the surrogate.

Loop: LLM plans → PINN surrogate evaluates candidate modulations cheaply → metaheuristic optimizes → returns optimal modulation parameters. This is the **"LLM proposes, fast surrogate disposes, optimizer refines"** pattern — a cheaper inner loop than full PLECS on every candidate.

## Problem
- **Converter:** Dual Active Bridge (DAB) isolated DC-DC.
- **Task:** phase-shift modulation strategy selection + parameter optimization (single/double/extended/triple/hybrid phase-shift, 1–3 DOF).
- **Objectives:** efficiency, soft switching, current-stress minimization, voltage regulation, stability.

## Results (precise)
- **Low-data modeling (10 samples, 5% training):** 0.245 MAE vs 0.666 (2nd-best TST) → **63.2% error reduction.** High-data (100 samples): 0.201 vs 0.264 → 23.7% reduction. Statistically significant (p<0.05) vs **12 baselines** (BN, SVR, XGBoost, RF, LSTM, GRU, LN-GRU, TCN, GRU-VAE, TST, TSiTPlus, MiniRocket).
- **User study (20 industrial practitioners):** junior engineers **96.3× faster**, seniors **33.9× faster**, overall **>33× design-time reduction**, **100% task completion.**
- Token/wall-clock cost **not reported** (a gap — cannot verify the cost story from this paper).

> **SRTP adoption status (2026-07-17): NOT adopted.** The plan ([[plan-ai-agent-mas]]) is **PLECS-only, no PINN/surrogates** — a surrogate that can disagree with PLECS is a liability for an evidence-gated system, and PLECS batch-parallelizes well enough. This note is kept as **reference/method evidence**, not an adopted component. (It does show surrogates *could* be revisited cheaply later if PLECS runtime ever dominates.)

## SRTP implications (reference only — not on the roadmap)
- **Resolves G2 directionally:** physics-informed surrogates are viable with ~10 sims, so a Traction-Inverter surrogate (efficiency/thermal) could be bootstrapped early (Phase 1–2), not deferred to Phase 4. This changes the plan.
- **Adopt the two-tier PINN idea** for the Simulation/Surrogate agent: switch-level + system-level physics-embedded surrogates, trained on a handful of PLECS runs, then optimized with PSO/DE/GA instead of brute-force PLECS sweeps.
- **Caveat — domain gap:** DAB modulation ≠ 3-phase traction inverter with a motor load. The PINN structure (ModNet/CirNet) is DAB-specific; a traction-inverter version must be re-derived. Cite as method evidence (C4), not domain proof.
- Same group as [[pe-gpt-2025-multimodal-pe-design]] — consistent line of work; weigh the `motivated` flag.
