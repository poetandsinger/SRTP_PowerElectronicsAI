---
title: "Traction Inverter Research Synthesis — 2025-2026 (Hub)"
type: index
field: ee
created: 2026-07-10
updated: 2026-07-10
tags: [ee, cs, index, review, synthesis]
---

# Traction Inverter Technology & Design Workflows: 2025-2026 Research Synthesis

> **This is a hub page.** The original 538-line synthesis has been fragmented into separate topic notes organized by field. Use this page to navigate the extracted pieces.

**Date:** 2026-07-10  
**Scope:** Comprehensive literature and market review of traction inverter technology, design workflows, control strategies, AI applications, standards, and market trends.

---

## Extracted Notes

### EE — Power Electronics

| Section | Note | Content |
|---------|------|---------|
| §1 Topologies & Semiconductors | [[ee/traction-inverter/topology-landscape-2025-2026]] | 2L/3L/multilevel comparison, SiC vs GaN vs Si IGBT, voltage architecture trends, SiC+GaN coexistence |
| §2 Design Parameters | → Appended to [[ee/traction-inverter/open-problems]] | Critical KPIs, optimization targets, multi-objective trade-offs |
| §3 Simulation Workflows | [[ee/traction-inverter/simulation-workflows-2025-2026]] | 10 tools compared, 10-phase design workflow, pain points |
| §4 Control Strategies | → Appended to [[ee/traction-inverter/control-schemes]] | FOC vs DTC vs MPC head-to-head, AI-enhanced control, sensorless |
| §5 Standards | [[ee/traction-inverter/standards-landscape-2025-2026]] | 11 core standards (IEC, ISO, AEC-Q, AQG 324, CISPR 25), safety goals, emerging WBG standards |
| §6 Market Trends | [[ee/traction-inverter/market-trends-2025-2026]] | $8.75B→$36.8B market, 17.3% CAGR, BYD/Denso/Tesla share, supplier deep dives |

### CS — AI / Design Automation

| Section | Note | Content |
|---------|------|---------|
| §7 AI/ML Applications | [[cs/ai-ml-power-electronics-2025-2026]] | 16 AI application areas with quantitative results, 6 AI paradigms compared |
| §8 Design Automation Gaps | [[cs/design-automation-gaps-2025-2026]] | 10 gaps, 11 AI augmentation opportunities, near-term trajectory |

---

## Key Conclusions (from original synthesis)

1. **SiC is the undisputed winner for 2025-2026 main-drive traction inverters**, with >98-99% efficiency, 1200V+ capability, and rapidly declining costs. GaN is emerging seriously for 400V main drive (VisIC/Hyundai) but faces thermal and reliability hurdles.

2. **800V architecture is the dominant trend**, with ~14% penetration in late 2025 and 25-30%+ forecast by 2027.

3. **Design workflows remain fragmented** across ECAD, MCAD, circuit simulation, and system simulation tools. Multi-physics coupling is the primary pain point.

4. **FOC remains the dominant control strategy** (>80% market share), but MPC is gaining. AI-enhanced control is emerging but not production-proven.

5. **AI applications in power electronics are real but focused on narrow tasks.** "Hybrid autonomy" is the realistic near-term path, not unsupervised approval.

6. **The biggest automation gaps** are: toolchain integration, multi-physics coupling, EMI compliance prediction, reliability optimization, and automated standards checking.

7. **Market is hyper-growing** (17.3% CAGR) with OEM vertical integration challenging Tier-1 suppliers. SiC supply chain is the critical bottleneck.

8. **Standards for WBG devices are still evolving** — ECPE AQG 324 has Annex SiC but GaN annex is pending.

---

## Cross-References

- [[cs/traction-inverter-mas-integration]] — Multi-agent system architecture informed by these findings
- [[cs/implementation-research]] — Technology decisions derived from this research
- [[cs/design-automation-gaps-2025-2026]] — Gaps this project aims to address
- [[catalog]] — Full vault catalog
- [[citations]] — Master bibliography
