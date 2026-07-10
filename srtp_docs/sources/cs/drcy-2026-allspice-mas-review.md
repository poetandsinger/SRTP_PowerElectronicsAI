---
title: "DRCY: Multi-Agent System for Schematic Connection Review Against Datasheets"
authors: [AllSpice]
year: 2026
venue: "arXiv preprint / production deployment"
arxiv: "2603.15672"
captured: 2026-07-10
reliability: medium
peer_reviewed: false
motivated: true
reliability_note: "Describes a production-deployed system at Fortune 500 companies but not peer-reviewed. AllSpice is the vendor — motivated source. However, deployment at named enterprise customers and specific performance metrics lend credibility."
sha256: placeholder
---

# DRCY: Production Multi-Agent Schematic Review System

## Summary

DRCY is a **production-deployed** multi-agent pipeline for semantic schematic connection verification against manufacturer datasheets. Deployed at Fortune 500 enterprises, autonomous vehicle companies, and commercial space companies. This is the closest industrial prior art to an AI agent that verifies power electronics designs against real component specifications.

## Architecture

**5-agent pipeline:**
1. **Netlist Augmentation Agent** — enriches netlist with design context
2. **Selection Agent** — identifies relevant components and connections
3. **Datasheet Retrieval Pipeline** — fetches and parses manufacturer datasheets
4. **Group Review Agents** — k separate review agents run concurrently per functional group
5. **Consensus Agent** — reconciles multi-run results; higher confidence for multi-run findings
6. **Error Grouping Agent** — clusters findings for human review

**Multi-run consensus mechanism:**
- k separate review agents per functional group
- Findings appearing in multiple runs get higher confidence
- Single-run findings critically evaluated
- Contradictions re-examined with full context
- **Separately configurable model** for consensus step

**Performance:** Typical 10-page schematic with 50-100 components completes analysis in < 20 minutes.

## Relevance to SRTP

1. **Multi-run consensus** is a pattern we should adopt for Reviewer Agent → run 3 independent reviews and reconcile
2. **Datasheet retrieval pipeline** validates our Component Agent's DigiKey/Octopart integration
3. **Production deployment** at Fortune 500 companies proves multi-agent engineering review works at scale
4. **< 20 minutes** for 50-100 components is the right order of magnitude for interactive use
5. **Semantic correctness checking** (does this connection match the datasheet?) is a capability our Reviewer Agent currently lacks

**Pattern to adopt:** Run the Reviewer Agent 3 times independently, reconcile with a Consensus step. Cost: 3× review tokens. Benefit: higher confidence, fewer false positives.

## Epistemic Status

- Production-deployed (credibility from enterprise adoption)
- Not peer-reviewed (vendor whitepaper)
- Multi-run consensus is independently sensible regardless of DRCY's specific results
- The 5-agent pipeline maps cleanly to our architecture
