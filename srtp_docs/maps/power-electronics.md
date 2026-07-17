---
title: Power Electronics Field Hub
type: map
field: power-electronics
created: 2026-07-08
updated: 2026-07-10
tags: [power-electronics, index]
---

# Power Electronics Research

> Hub for all electrical engineering research in this vault.
> Sub-fields: traction inverter design, power semiconductors, control schemes, PLECS modeling.

## Traction Inverter Design

- [[power-electronics/traction-inverter/traction-inverter-index]] — Entry point: industry research hub
- [[power-electronics/traction-inverter/what-is-a-traction-inverter]] — Fundamentals
- [[power-electronics/traction-inverter/circuit-topologies]] — Two-level, 3L-NPC, ANPC, T-type, flying capacitor
- [[power-electronics/traction-inverter/components]] — SiC MOSFETs, GaN HEMTs, IGBTs, gate drivers, DC-link
- [[power-electronics/traction-inverter/control-schemes]] — FOC, DTC, MPC, sliding mode, sensorless
- [[power-electronics/traction-inverter/control-how-to]] — Practical FOC tuning guide
- [[power-electronics/traction-inverter/machine-and-load]] — The PMSM/IPMSM plant: dq model, torque, operating regions, limits

### Design Cluster (build knowledge base — 2L-B6 SiC 800V)

- [[power-electronics/traction-inverter/reference-designs-index]] — **Reference designs hub** (1 synthetic anchor + 3 real)
- [[power-electronics/traction-inverter/reference-design-2l-b6-sic-800v]] — Synthetic anchor: 800V SiC 2L-B6, 150 kW
- [[power-electronics/traction-inverter/reference-design-wolfspeed-ti-300kw-800v]] — Real vendor CRD: 800V/300kW SiC (CAB450M12XM3)
- [[power-electronics/traction-inverter/reference-design-tesla-model3-400v-sic]] — Production: Tesla Model 3 400V SiC
- [[power-electronics/traction-inverter/reference-design-nissan-leaf-400v-igbt]] — Production: Nissan Leaf 400V IGBT baseline
- [[power-electronics/traction-inverter/materials-and-properties]] — Material property reference (semiconductor/ceramic/dielectric/magnet)
- [[power-electronics/traction-inverter/machine-and-load]] — The PMSM/IPMSM plant (dq model, operating regions)
- [[power-electronics/traction-inverter/design-procedure]] — End-to-end sizing/design procedure (worked)
- [[power-electronics/traction-inverter/schematics]] — Mermaid schematics (power stage, gate drive, control, ASC)
- [[power-electronics/traction-inverter/thermal-design]] — Thermal: Rth/Zth, cooling, TIM, derating
- [[power-electronics/traction-inverter/gate-driver-design]] — Gate drive: rails, Rg, desat, isolation, ICs
- [[power-electronics/traction-inverter/protection-and-safety]] — Protection & safety factors / derating table
- [[power-electronics/traction-inverter/emi-emc-design]] — EMI/EMC: CISPR 25, filters, dv/dt, bearing currents
- [[power-electronics/traction-inverter/packaging-and-layout]] — Packaging, busbar Lσ, creepage/clearance
- [[power-electronics/traction-inverter/bom]] — Component-class BOM with representative parts
- [[power-electronics/traction-inverter/bom-price-database]] — Priced BOM (real dated distributor prices)
- [[power-electronics/traction-inverter/design-tradeoffs]] — How to compromise: device/voltage/fsw/topology trade-offs
- [[power-electronics/traction-inverter/worked-example-400v-150kw]] — Worked example: 400V SiC 150kW

### Simulation, Standards & Frontiers

- [[power-electronics/traction-inverter/manufacturing-and-test]] — Assembly, double-pulse, HIL, EOL test, production quality
- [[power-electronics/traction-inverter/reliability-and-lifetime]] — Power-cycling, lifetime models, mission profile, SiC degradation
- [[power-electronics/traction-inverter/simulation-and-validation]] — PLECS-first simulation & validation workflow
- [[power-electronics/traction-inverter/standards-and-compliance]] — Standards (IEC 61800, ISO 26262, AEC-Q, AQG 324, CISPR 25)
- [[power-electronics/traction-inverter/open-problems]] — Research frontiers

## Problem Statement (preface — now at vault root, not in power-electronics/)

- [[problem-statement/problem-statement-index]] — Why AI for traction inverter design (motivation, market, workforce, competitive landscape)

## Audit

- [[audits/audit-changelog-traction-inverter]] — Literature audit changelog

## Sources (ee/)

- [[sources/power-electronics/zuo-etal-2024-mtpa-dcee]] — Zuo et al. (2024): RLS-based DCEE for online MTPA
- [[sources/power-electronics/cacciato-etal-2022-gan-anpc]] — Cacciato et al. (2022): GaN HEMT 3L-ANPC loss modeling
- [[sources/power-electronics/sachs-neuburger-2025-3l-tnpc]] — Sachs & Neuburger (2025): 3L-TNPC vs 2L SiC efficiency
- [[sources/power-electronics/sachs-etal-2025-single-dual-inverter]] — Sachs et al. (2025): Single vs dual inverter optimization
- [[sources/power-electronics/pimpale-mahadik-2025-asc-discharge]] — Pimpale & Mahadik (2025): ASC discharge for SiC inverters
- [[sources/power-electronics/zhang-negri-2026-ai-multiphysics-sustainability]] — **NEW:** Zhang & Negri (2026): AI-assisted multi-physics sustainability evaluation

## Cross-field Links

- [[maps/ai-agents]] — AI agent architectures (including [[ai-agents/traction-inverter-mas-integration|traction inverter MAS integration]])
- [[ai-agents/traction-inverter-mas-integration]] — **NEW:** Bridge note: multi-agent system for traction inverter design
- [[catalog.md]] — Full vault catalog
- [[citations]] — Master bibliography
