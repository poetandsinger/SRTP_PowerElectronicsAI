---
title: Changelog Index
type: map
field: project
created: 2026-07-06
updated: 2026-07-21
tags: [index]
---

# Changelog Index

> **Part of:** [[README]]  
> **Purpose:** Timestamped index — each entry links to a detailed changelog file  

---

| Timestamp | Summary | Detail |
|-----------|---------|--------|
| 2026-07-21 | **Purpose-fit 2L-B6 800 V bench built + verified; heat-sink coupling proven GUI-only**: retargeted the shipped `three_phase_voltage_source_inverter` demo to Wolfspeed CAB450 — operating point CONFIRMED headless (800 V, 357.5 A rms, 292 kW), conduction-loss readout T-dependent. Cracked the switching-loss blocker (`PeriodicImpulseAverage`). Proved 5 ways (PLECS 4.8 manual RPC-command list + heat-sink §, `plecs.get` param probe, byte-identical geometry test, Plexim forum) that device→heat-sink **coupling cannot be scripted** — one manual GUI drag now gates the validated number. Bench + handoff README under `experiments/2l-b6-800v-sic-bench/` | [[2026-07-21-plecs-2l-b6-bench-and-coupling]] |
| 2026-07-19 | **Session retrospective** — critical, honest account of the long autonomous PLECS-harness + Track-1 loss-layer session (testing methodology, the `Frame` silent-drop failure, the loss-readout=0 debugging ladder, the "GUI-only coupling" question). Backing detail behind the 2026-07-19 changelog entries | [[SESSION_LOG_2026-07-19]] |
| 2026-07-19 | **PLECS readback blocker cleared + loss layer activated**: `simulate` Values is empty in 4.8 — reliable readback is a `ToFile`→CSV (corrects the "top-level Outport" claim); proven on toy + real 2L-VSI models (stale-model + TimeSpan traps found). Reusable harness under `data/plecs/` (template + direct-RPC runner + summarizer + `model_registry.json`). Official **Wolfspeed PLECS model library** organized under `plecs_models/wolfspeed/` (669 models); CAB450M12XM3 loads+simulates on the harness. SOP/plan/memories/citations corrected ([166]–[170]) | [[2026-07-19-plecs-readback-harness]] |
| 2026-07-19 | Descriptive renames (26 files → `harness-*`/`plan-*`/`index-*` clusters) + plain-text→wikilink cleanup; **frontmatter-as-index** navigation model in SCHEMA (rg-filter on field/type/status/tags → pick by filename), index-maintenance rule, prefixes demoted to optional sugar, 5 tags registered | [[2026-07-19-naming-and-navigation]] |
| 2026-07-19 | PLECS validation SOP (S1–S7 gates: convergence, steady-state window, energy balance, measured calibration, per-topology NP-balance); method notes → `procedure-*`; control/PLECS toolchain reconciled; SCHEMA/README updated | [[2026-07-19-validation-sop]] |
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

← [[README]] | [[plan-ai-agent-mas]]
