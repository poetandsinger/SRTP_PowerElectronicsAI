---
title: Changelog Index
type: map
field: project
created: 2026-07-06
updated: 2026-07-19
tags: [index]
---

# Changelog Index

> **Part of:** [[README]]  
> **Purpose:** Timestamped index — each entry links to a detailed changelog file  

---

| Timestamp | Summary | Detail |
|-----------|---------|--------|
| 2026-07-19 | Topology-unit naming: `design-<topology>-<voltage>-<device>` scheme; renamed 2L anchor to `design-2l-b6-800v-sic`; added TNPC/ANPC/NPC scaffolds; split reference-designs-index | [[2026-07-19-topology-units]] |
| 2026-07-19 | Vault refactor: stage-based folders (`sources`/`notes`/`trials`/`plans`/`log`), 867 links → bare basenames (files move without breaking), per-stage `.base` indexes, density pass over 70 notes. No information lost (verified) | [[2026-07-19-vault-refactor]] |
| 2026-07-18 | Three more worked examples across applications+workflows: Class-8 truck (lifetime/rainflow-Miner), hypercar (power-density/Zth-pulse, Porsche-anchored), 96V microcar (cost/voltage-lever). Web-researched sources [158]–[165]; process comparison folded into observed-workflow note (n→4) | [[2026-07-18-three-worked-examples]] |
| 2026-07-18 | Design-by-doing: invented family-car 400V SiC inverter, ran a numerical model (efficiency/thermal/cycle, SiC-vs-IGBT), confirmed PLECS licensed + drive simulates. New worked-example + findings notes; `worked-designs/` artifacts | [[2026-07-18-family-car-design-by-doing]] |
| 2026-07-18 | Depth-first traction-inverter pass: rewrote standards-and-compliance (actual requirements per standard) + simulation-and-validation (PLECS model layers + corner-test matrix); added Red Team to both; PLECS-MCP grounded against PE-MAS; citations → [1]–[157] | [[2026-07-18-standards-simulation-deepdive]] |
| 2026-07-17 | Depth-first AI-agent pass: design-loop finding (topology→refine→parameter-optimize + explicit optimizer), workflow-pattern catalog, plan-sufficiency verdict; plan split into hub + 8 topic files (no phases) | [[2026-07-17-plan-split-design-loop]] |
| 2026-07-17 | Traction-inverter engineering textbook built (29 chapters, cited [1]–[148]); problem-statement moved to root; meta files removed | [[2026-07-17-traction-inverter-textbook]] |
| 2026-07-06 23:45 | Restructured vault: single citations.md, descriptive indexes, plans/changelog folders | [[2026-07-06-restructure]] |
| 2026-07-06 23:30 | Subagent data integrated: smolagents as agent engine, PulsimGUI reference, NiceGUI option | [[2026-07-06-subagent-findings]] |
| 2026-07-06 22:00 | Architecture pivot: standalone GUI app, not Hermes Agent-based. MATLAB external. | [[2026-07-06-architecture-pivot]] |
| 2026-07-06 21:30 | Initial setup: 17 research notes, agent harness survey, traction inverter research | [[2026-07-06-initial-setup]] |

---

← [[README]] | [[ai-agent-mas-plan]]
