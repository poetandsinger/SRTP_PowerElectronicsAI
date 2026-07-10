---
title: "AgenticTCAD: Multi-Agent LLM Framework for Semiconductor TCAD Simulation and Design"
authors: [multi-institution, not fully captured]
year: 2026
venue: "DATE 2026 (Design, Automation and Test in Europe Conference)"
arxiv: "2512.23742"
captured: 2026-07-10
reliability: high
peer_reviewed: true
reliability_note: "Accepted at DATE 2026 — a premier EDA conference. Peer-reviewed."
sha256: placeholder
---

# AgenticTCAD: Multi-Agent LLM for Semiconductor TCAD

## Summary

A multi-agent LLM framework with a fine-tuned domain LLM for semiconductor TCAD simulation and design automation. Designed a 2nm nanosheet FET meeting IRDS-2024 specifications in **4.2 hours vs 7.1 days** — a **40x speedup** over manual expert design.

## Architecture

- **Multi-agent coordination** — domain-specific agents for device generation, simulation, analysis
- **Fine-tuned domain LLM** — trained on expert TCAD design corpus
- **Closed-loop generate-verify-optimize** — LLM proposes, TCAD simulation validates, agent iterates

## Key Results

- **40x speedup:** 4.2 hours (agent) vs 7.1 days (human expert)
- Met IRDS-2024 specifications for 2nm node
- Peer-reviewed at a premier EDA conference

## Relevance to SRTP

This is the **strongest evidence yet** that multi-agent LLM systems can dramatically accelerate hardware design:
1. **40x speedup** on a complex, multi-parameter optimization problem (structurally similar to traction inverter design)
2. **Fine-tuned domain model** outperforms general models — supports our per-agent model selection strategy
3. **Closed-loop simulation verification** (LLM→TCAD→analyze→iterate) is exactly our pattern (LLM→MATLAB→analyze→iterate)
4. **Peer-reviewed** at a top venue — not a preprint or blog post

**Key difference:** TCAD simulation runs in seconds-minutes. MATLAB/Simulink traction inverter simulation runs in minutes-hours. The 40x speedup may not translate directly (bottleneck shifts from design time to simulation time).

## Epistemic Status

- Peer-reviewed at DATE 2026 (high reliability)
- 4.2 hours vs 7.1 days is a concrete, falsifiable result
- Domain is semiconductor TCAD, not power electronics — but the workflow pattern is structurally identical
