---
title: "An Accessible LLM-Based Framework for Power Converter Design (Liu et al., 2026)"
type: source
field: ai-agents
tags: [ai-agents, design-automation, simulation, code-generation, engineering-ai, preprint]
authors: [Junhua Liu, et al.]
year: 2026
venue: "IET Power Electronics (Wiley)"
doi: "10.1049/pel2.70259"
url: "https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/pel2.70259"
captured: 2026-07-17
reliability: medium
peer_reviewed: true
motivated: true
reliability_note: "Peer-reviewed in IET Power Electronics (2026). Captured from publisher abstract + search-index summary — full text was paywalled/403 at capture time, so architectural detail below is second-hand and marked [unverified] where not confirmed against the PDF. Same lead author (Liu) as PHIA/LP-COMDA. In-domain (power converters) but converter-class, not traction inverter."
---

# An Accessible LLM-Based Framework for Power Converter Design (Liu et al., 2026)

**Why it matters for SRTP:** a *peer-reviewed* (not preprint) 2026 framework whose central contribution is a **universal circuit-encoding method** that lets an LLM read and emit converter connectivity as structured text, then generate a customised simulation model directly from a natural-language spec. This is the same "template + structured-model" problem the SRTP PLECS harness solves — evidence the encoding step is a recognised, publishable sub-problem, and that "the LLM authors a *structured circuit representation*, not a raw netlist" is the field-standard framing.

## Architecture (from abstract / index summary — [unverified] against full text)
- **LLM-based autonomous design loop:** natural-language spec → circuit encoding → simulation-model generation → verification.
- **Universal circuit-encoding method:** a text representation of circuit connections the LLM can both parse and produce, aimed at scalability across converter scenarios (topology-agnostic encoding rather than per-topology hand-coding).
- **Simulation-in-the-loop verification:** generated models are simulated to verify the design meets the spec (design → verify closed loop).
- **Accessibility framing:** targets non-expert users driving converter design from text (echoes PHIA's >33× design-time-reduction user-study motivation).

## Relevance / how SRTP should read it
- **Confirms the encoding boundary.** SRTP's decision to use *validated per-topology PLECS templates + `ModelVars`/XML-injection* ([[plecs-integration]]) is the low-risk instance of this paper's "universal encoding." A universal encoder is more ambitious (and more failure-prone) than SRTP needs — keep the template path, treat universal encoding as a **stretch/again-later** idea, not a Phase-0 dependency.
- **Design→verify loop is field-standard.** Reinforces the [[design-loop-architecture]] finding that a bare PLAN→DESIGN→VALIDATE single pass is under-specified; the published systems all close a generate→simulate→check loop.
- **Same author line as PE-GPT / PHIA** ([[pe-gpt-2025-multimodal-pe-design]], [[phia-lpcomda-2026-physics-informed-pe-agent]]) — weigh the `motivated` flag; this is one group iterating on its own paradigm, not independent replication.

## Caveats
Captured from abstract/index only (full text paywalled at capture). Do **not** cite specific quantitative claims until the PDF is read. Converter-class, not traction inverter — pattern evidence (C3), not domain proof. **To verify:** obtain the PDF, confirm the encoding scheme and whether any multi-agent decomposition is used, and record measured cost/accuracy.

← [[harness-index]] | [[design-loop-architecture]] | [[phia-lpcomda-2026-physics-informed-pe-agent]]
