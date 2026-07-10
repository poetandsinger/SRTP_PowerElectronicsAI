---
title: "ThermRAG: A Multimodal Knowledge-Enhanced Agent for Power Electronics Thermal Design"
authors: [not fully identified]
year: 2025
venue: "IEEE (conference/journal, 2025)"
doi: "IEEE Xplore 11516791"
captured: 2026-07-10
reliability: medium
peer_reviewed: true
reliability_note: "Published in an IEEE venue — peer-reviewed. Specific journal/conference not confirmed from search results. IEEE publishing implies some review."
sha256: placeholder
---

# ThermRAG: Multimodal Agent for Power Electronics Thermal Design

## Summary

ThermRAG is a knowledge-enhanced agent integrating a Thermal Calculation Engine with a dual-knowledge-base architecture (Core KB + Dynamic KB), using a locally deployed DeepSeek R1 model. It extracts parameters from datasheets, runs thermal scripts, and generates design recommendations.

## Architecture

- **Dual Knowledge Base:**
  - Core KB: Static domain knowledge (thermal equations, material properties, package standards)
  - Dynamic KB: Project-specific data accumulated during design
- **Thermal Calculation Engine:** Deterministic thermal modeling (not LLM-hallucinated)
- **DeepSeek R1:** Locally deployed for reasoning and recommendation generation
- **Datasheet parser:** Extracts thermal parameters (RθJC, RθCS, max Tj) from PDF datasheets

## Key Claims

- Integrates multimodal data (datasheet PDFs, thermal specs, design constraints)
- Uses locally deployed model (no cloud dependency — important for proprietary designs)
- Generates thermal design recommendations with evidence traceability

## Relevance to SRTP

1. **Thermal domain agent** is a missing piece in our current 5-agent architecture
2. **Dual KB pattern** (Core + Dynamic) matches our proposed memory architecture
3. **Local deployment (DeepSeek R1)** validates our provider-agnostic, cost-conscious strategy
4. **Datasheet parsing** is a capability our Literature Agent currently lacks

## Epistemic Status

- IEEE published → peer-reviewed
- But details thin from search results — full methodology and quantitative results not captured
- The dual-KB pattern is independently sensible regardless of ThermRAG's specific results
