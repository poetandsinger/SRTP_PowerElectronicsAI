---
title: "How I Wired PLECS to an AI Coding Agent, And What I Actually Learned"
type: source
field: ai-agents
tags: [ai-agents, simulation, integration, plecs, code-generation, design-automation, tool-calling]
authors: [Marc Ordonez]
year: 2026
venue: "Substack (polyaxyellowbox) — practitioner blog"
url: "https://polyaxyellowbox.substack.com/p/how-i-wired-plecs-to-an-ai-coding"
captured: 2026-07-17
reliability: low
peer_reviewed: false
reliability_note: "Single practitioner blog post, un-refereed, n=1, no released code inspected yet. BUT it is the closest direct prior art to the SRTP thesis (AI agent + PLECS for power electronics) and its capability-boundary finding is highly actionable. Treat quantitative claims (1000x token reduction, $20/hr) as directional, not measured."
---

# Wiring PLECS to an AI Coding Agent (Ordonez, 2026)

**The closest direct prior art to SRTP.** An independent practitioner connected an AI coding agent to PLECS via XML-RPC and reported, concretely, what the agent could and could not do. This is the empirical boundary the SRTP MAS must respect.

## Architecture — a 5-layer abstraction (agent never sees raw data)

1. **Data capture** — Python XML-RPC runner executes simulations (port 1080).
2. **Summarization** — streaming CSV analyzer → compact report (**~36 numbers instead of 500,000+ rows**).
3. **Regression testing** — sample-by-sample baseline comparison with tight tolerances.
4. **Validation pipeline** — single-entry-point script returning **pass/fail exit codes**.
5. **AI interaction** — the agent calls Layer 4 and receives concise results.

Key enabling insight: *"PLECS files are just XML"* and the control code lives in editable `.c`/`.h` files on disk — so both the model and the controller are agent-accessible as text.

## What the agent DID succeed at

- **Parameter sweeps** — iteratively adjusting PI gains across test cycles.
- **Refactoring** — breaking an 800-line control function into modular pieces, with **regression verification after each extraction**.
- **Analysis & reporting** — comparative simulations, summaries across operating points.

## What the agent DID NOT do (the boundary that matters)

> topology design · control-strategy selection · physics interpretation · literature review

The key scoping fact for SRTP: **an unaugmented coding agent handles parametric/regression/analysis work but not the creative-engineering and physics-reasoning work.** It maps directly onto our role split — cheap tool-calling models for the Simulation/parameter work, strong reasoning models (and RAG/literature grounding) for topology, control, and physics.

## Hard lessons (directional numbers)

- **Token economics dominate.** Feeding raw waveforms "burned through $20 in roughly an hour" (~thousands of tokens/iteration). Engineered summaries cut this to **~175 tokens/iteration** (~1000×). Rule: *"use a narrow, cheap tool where a narrow tool works and use the expensive model only where it adds value."*
- **A project-rules file is essential** — encoding domain constraints ("one change at a time", "check both operating points") stopped the agent from brute-forcing or masking root causes. Validates hard **guardrails** as system-prompt constraints.

## SRTP implications

- Confirms the **summarize-before-the-LLM** pattern (aligns with SCALE / AgentSlimming / Q-planner token-reduction findings) is not optional — it is the difference between viable and bankrupt.
- Confirms the **capability boundary**: SRTP's value-add (topology selection, control-scheme choice, physics-grounded review) is precisely what this agent could *not* do — i.e., the SRTP MAS must supply exactly that scaffolding, or it reduces to a glorified sweep runner.
- Confirms the **template + `ModelVars` + regression-gate** loop is a proven, cheap inner loop for the Simulation Agent.

## Red-flag caveats

n=1, un-refereed, no code inspected, quantitative claims unmeasured. Use as a design compass, not evidence. **To verify:** locate any released repo, reproduce the 5-layer harness against a PLECS demo model, and measure the token delta ourselves.

See [[plecs-xmlrpc-scripting-interface]] for the API this rests on.
