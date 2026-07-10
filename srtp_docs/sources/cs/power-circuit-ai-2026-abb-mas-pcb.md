---
title: "Power Circuit AI: Designing Power Electronic Circuits for Motor Drives with Generative AI"
authors: [ABB Inc. / ABB US Corporate Research Center]
year: 2026
venue: "engrXiv preprint"
doi: "10.31224/6706"
captured: 2026-07-10
reliability: medium
peer_reviewed: false
motivated: true
reliability_note: "Preprint from ABB corporate research. Author is a major industrial player with application interest — results are self-reported and not independently replicated. However, ABB has strong engineering credibility and the framework produces verifiable outputs (PCB layouts)."
sha256: placeholder
---

# Power Circuit AI: Autonomous Multi-Agent Framework for PCB Design

## Summary

ABB's Power Circuit AI is an **autonomous multi-agent framework** that orchestrates end-to-end power electronic circuit design — from natural language specifications to clean PCB layouts — **without fine-tuning** the underlying LLMs. This is the closest industrial prior art to the SRTP project's vision.

## Architecture

**Multi-agent pipeline:**
1. **Device Specification Agent** — parses natural language requirements into electrical specs
2. **Component Selection Agent** — selects real components from libraries
3. **SKiDL Netlist Agent** — generates netlists using the SKiDL Python library
4. **Layout Agent** — completes PCB routing and placement

**Key design choices:**
- No LLM fine-tuning — uses prompt engineering + tool integration
- SKiDL (Python-to-netlist) as the bridge between LLM text output and EDA tools
- Each agent is a specialized LLM call with domain-specific tools

## Key Results

- **100% logical connectivity** on generated PCBs
- **Automated routing achieved** (not just schematic — actual PCB layout)
- Validated on a 400V 3-phase converter for a variable frequency drive
- End-to-end: natural language → working PCB

## Relevance to SRTP

This is **direct industrial validation** of the multi-agent approach for power electronics:
1. ABB is using multi-agent architecture for power electronics design — validates our core premise
2. SKiDL as netlist generator parallels our MATLAB Engine API as simulation backend
3. "No fine-tuning" approach matches our provider-agnostic strategy
4. 400V 3-phase VFD is structurally similar to a traction inverter

**Key differences from SRTP:**
- ABB targets PCB layout; SRTP targets simulation + optimization
- ABB uses proprietary internal tools; SRTP targets open/accessible tools
- ABB is a single company's internal tool; SRTP aims to be general-purpose

## Critical Assessment

**Strengths:**
- Industrial (ABB) — not academic toy problem
- End-to-end: spec → PCB
- No fine-tuning needed

**Weaknesses:**
- Preprint, not peer-reviewed
- ABB is inherently motivated (selling this capability)
- Results are self-reported; no independent verification
- "100% logical connectivity" is necessary but not sufficient — says nothing about electrical performance, thermal, EMI
