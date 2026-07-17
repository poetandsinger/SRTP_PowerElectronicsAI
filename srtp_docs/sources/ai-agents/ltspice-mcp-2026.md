---
title: "ltspice-mcp: Model Context Protocol Server for LTspice/ngspice Simulation"
type: source
field: ai-agents
tags: [ai-agents, preprint]
authors: [cognitohazard]
year: 2026
venue: "GitHub"
url: "https://github.com/cognitohazard/ltspice-mcp"
captured: 2026-07-10
reliability: medium
peer_reviewed: false
reliability_note: "Open-source project (GPL-3.0). 51 documented MCP tools. Active development. Not peer-reviewed but functionally verifiable — you can run the tools and check the outputs."
sha256: placeholder
---

# ltspice-mcp: MCP Server for SPICE Simulation

## Summary

An MCP (Model Context Protocol) server providing **51 tools** for LLM-driven SPICE circuit simulation via LTspice and ngspice. Compatible with Claude (Desktop, Code), Cursor, Windsurf, Gemini CLI, and other MCP-supporting agents. Provides the bridge between LLM reasoning and ground-truth circuit simulation.

## Capabilities

**51 MCP tools across categories:**
- Circuit creation and component editing
- Schematic geometry management
- Simulation lifecycle (setup, run, collect)
- Time-domain analysis (transient)
- Frequency-domain analysis (AC, Bode, stability)
- DC operating point with device parameter readout (gm, gds, Vth)
- Parameter sweeps and Monte Carlo analysis
- THD, noise, pulse response metrics
- Library management

**Design philosophy:** "Judging whether a result is trustworthy is left to the model reading it" — server reports facts, not verdicts. This is exactly the "LLM proposes, simulation disposes" pattern.

## Relevance to SRTP

1. **51 ready-made simulation tools** that an agent can use TODAY for circuit-level verification
2. **MCP protocol** means Claude (and other MCP-compatible agents) can natively invoke SPICE simulation
3. **Complementary to MATLAB/Simulink:** ltspice-mcp for device-level switching verification; MATLAB for system-level motor drive simulation
4. **Monte Carlo and parameter sweeps** enable statistical design — a capability our current architecture lacks
5. **Bode/stability analysis** enables the agent to verify control loop stability autonomously

**Integration proposal:** Add ltspice-mcp as an optional tool for the MATLAB Agent (or a separate "SPICE Agent"). Use cases: gate drive verification, snubber design, EMI filter simulation, control loop stability check — all at the device/circuit level where SPICE excels and MATLAB/Simulink is overkill.

## Epistemic Status

- Open-source, functionally verifiable (medium-high reliability for tool existence)
- Not peer-reviewed (tool, not research)
- 51 tools is a LOT — suggests mature development
- GPL-3.0 license is compatible with our MIT/Apache stack (we'd use it as an external tool, not incorporate the code)
