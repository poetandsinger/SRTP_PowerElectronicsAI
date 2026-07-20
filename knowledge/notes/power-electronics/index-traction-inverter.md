---
title: "Traction Inverter — Index"
type: map
field: power-electronics
created: 2026-07-07
updated: 2026-07-20
tags: [power-electronics, traction-inverter, index]
---

> Pure wayfinding for the traction-inverter knowledge base — table of contents + reading order, no knowledge of its own. For relationships and "what connects to what", use graphify (`graphify query …`, `graphify-out/graph.html`). The industry/market survey moved to [[market-and-industry]].

## Notes in this Cluster

| Note | Content |
|------|---------|
| [[what-is-a-traction-inverter]] | First principles: what it does, why it is needed, energy flow, vehicle context |
| [[circuit-topologies]] | 2L-B6, 3L-NPC, 3L-ANPC, 3L-TNPC — circuits, switching states, trade-off matrix |
| [[circuit-components]] | Power semiconductors (SiC/IGBT/GaN), gate drivers, DC-link caps, sensors, thermal |
| [[materials-and-properties]] | Property reference: semiconductor / ceramic / die-attach / dielectric / magnet constants |
| [[control-schemes]] | FOC, DTC, MTPA, SVPWM, DPWM, overmodulation, field weakening, ISO 26262 safety |
| [[procedure-control]] | Practical FOC recipe: parameter tuning, MTPA, field weakening, safety limits |
| [[machine-and-load]] | The plant: PMSM/IPMSM types, dq model, torque, operating regions, limits |
| [[design-2l-b6-800v-sic]] | Topology unit 1 (anchor): 800V SiC 2L-B6, 150 kW — spec, decisions, validation plan |
| [[design-3l-tnpc-800v-sic]] | Topology unit 2 (scaffold): 800V SiC 3L-TNPC, 12-switch |
| [[design-3l-anpc-800v-sic]] | Topology unit 3 (scaffold): 800V SiC 3L-ANPC, 18-switch + RLC filter |
| [[design-3l-npc-800v-sic]] | Topology unit 4 (scaffold): 800V SiC 3L-NPC, 12-switch + 6-diode |
| [[procedure-design]] | End-to-end sizing: switch → thermal → DC-link → gate-drive → sensing → protection → busbar |
| [[schematics]] | Mermaid schematics: system, power stage, half-bridge, gate driver, DC-link, sensing, ASC |
| [[thermal-design]] | Rth chain, Zth, Tj estimation, cooling, TIM, derating, worked example |
| [[design-gate-driver]] | Rails, Rg/Ig/Pdrive, desat, isolation, bias, real ICs, CAB450 worked example |
| [[protection-and-safety]] | Derating (cosmic-ray/thermal/SC/OV), ASC, ISO 26262, qualification |
| [[design-emi-emc]] | CISPR 25, CM/DM, input filter, dv/dt reflected wave, bearing currents, layout |
| [[packaging-and-layout]] | Module stack, laminated busbar Lσ, Kelvin loop, creepage/clearance, enclosure |
| [[bom-2l-b6-sic]] | Component-class BOM: function → part-class → sizing driver → citation |
| [[bom-price-database]] | Priced BOM: dated distributor prices + volume caveat |
| [[design-tradeoffs]] | How to compromise: device / voltage / fsw / topology / cooling + decision table |
| [[manufacturing-and-test]] | Module assembly, busbar, double-pulse, HIL, EOL, production quality |
| [[reliability-and-lifetime]] | Power-cycling wear-out, Nf data, lifetime models (LESIT/CIPS08), Miner |
| [[procedure-simulation-and-validation]] | PLECS-first simulation & validation workflow, corner tests |
| [[standards-and-compliance]] | IEC 61800, ISO 26262, AEC-Q, AQG 324, CISPR 25 |
| [[open-problems]] | Active research questions and design tensions |
| **Reference designs** | [[index-reference-designs]] · [[reference-design-wolfspeed-ti-300kw-800v]] · [[reference-design-tesla-model3-400v-sic]] · [[reference-design-nissan-leaf-400v-igbt]] |
| **Worked examples** | [[worked-example-400v-150kw]] · [[worked-example-family-car-400v-sic]] · [[worked-example-truck-800v-sic]] · [[worked-example-performance-800v-sic]] · [[worked-example-microcar-96v-mosfet]] · [[findings-family-car-design-by-doing]] |
| **Segments** | [[segment-heavy-duty-truck-inverters]] · [[segment-performance-motorsport-inverters]] · [[segment-low-cost-city-car-inverters]] |
| **Industry / market** | [[market-and-industry]] — production topologies, device adoption, suppliers, market data |
| [[audit-changelog-traction-inverter]] | Source-fidelity audit changelog |

## Reading Order

1. [[what-is-a-traction-inverter]] — *why* the inverter exists and what it controls.
2. [[circuit-topologies]] — the circuit options.
3. [[circuit-components]] — the physical parts that make it work.
4. [[control-schemes]] (theory) → [[procedure-control]] (practice).
5. **Design cluster (how one is built):** anchor spec [[design-2l-b6-800v-sic]] → sizing math [[procedure-design]] → wiring [[schematics]]. Then subsystem deep-dives: [[thermal-design]], [[design-gate-driver]], [[protection-and-safety]], [[design-emi-emc]], [[packaging-and-layout]]. Parts & prices: [[bom-2l-b6-sic]] + [[bom-price-database]]. Compromises: [[design-tradeoffs]]. Second example: [[worked-example-400v-150kw]].
6. **Compare against real designs:** [[index-reference-designs]] — Wolfspeed/TI 300 kW CRD, Tesla Model 3, Nissan Leaf across 800V-SiC → 400V-SiC → 400V-IGBT.
7. [[procedure-simulation-and-validation]] — how to model and validate it in PLECS.
8. [[open-problems]] — the unresolved research questions.

*Industry context (market size, adoption, supply chain) is a side-read: [[market-and-industry]].*

← [[harness-index|Agent Harness Research]] | [[README|SRTP Index]]
