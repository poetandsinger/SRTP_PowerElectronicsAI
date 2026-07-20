---
title: "Inverter Designs — Index (topology units + external references)"
type: map
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
tags: [power-electronics, traction-inverter, reference-design, design, index]
---

## What This Is

Two kinds of complete inverter design in this build manual: **topology units** we design and PLECS-validate ourselves (`design-<topology>-<voltage>-<device>`, one per topology, built serially — see [[plan-depth-research]]), and **external references** (one vendor CRD, two production teardowns) that calibrate and ground them. Together they let an LLM answer "show me a complete traction inverter of type X" with a grounded example, and give the PLECS effort its calibration targets.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge.

## Topology units (`design-*`) — ours, PLECS-validated

The four production/candidate topologies, same 800 V / 150 kW anchor, built and validated one at a time. Only 2L-B6 is developed; the 3L notes are scaffolds filled by their track.

| Topology unit | Topology | Switches | Track | State |
|---------------|----------|---------:|:-----:|-------|
| [[design-2l-b6-800v-sic]] | 2L-B6 | 6 | 1 | anchor — sizing worked in [[procedure-design]]; **first to validate** |
| [[design-3l-tnpc-800v-sic]] | 3L-TNPC | 12 | 2 | scaffold — leading multilevel candidate [28] |
| [[design-3l-anpc-800v-sic]] | 3L-ANPC | 18 | 3 | scaffold — the reference-PDF topology (+ RLC filter) |
| [[design-3l-npc-800v-sic]] | 3L-NPC | 12 + 6 D | 4 | scaffold — diode-clamped baseline |

## External references (`reference-design-*`) — calibration + context

| Reference | Class | Power | Device | Grounding | Role |
|-----------|-------|------:|--------|-----------|------|
| [[reference-design-wolfspeed-ti-300kw-800v]] | 800 V 2L | 300 kW | 1200 V SiC (CAB450M12XM3) | **real vendor CRD** [91] | **measured PLECS calibration anchor** (>98 %, 32 kW/L) |
| [[reference-design-tesla-model3-400v-sic]] | 400 V 2L | ~211 kW | 650 V SiC (ST, 24 modules) | **production teardown** [94] | 400 V + volume-cost context (no published η/THD/Tj) |
| [[reference-design-nissan-leaf-400v-igbt]] | 400 V 2L | 80 kW | Si IGBT | **production teardown** [95] | IGBT contrast baseline (low-reliability teardown) |

## How To Read Them

1. **Learn the method** on [[design-2l-b6-800v-sic]] + [[procedure-design]].
2. **Validate it** against the Wolfspeed/TI CRD — the measured anchor [91].
3. **Compare topologies** across the four `design-*` units once each is validated ([[circuit-topologies]] §5).
4. **See the voltage/device trade-space** across the external refs: 800 V-SiC → 400 V-SiC → 400 V-IGBT — device voltage, DC-link size, efficiency, and cost move together.
5. **Price it** in [[bom-price-database]] (mind distributor-vs-volume pricing).

---

> **References:** [[citations]]

← [[index-traction-inverter]] | [[procedure-design]] | [[bom-2l-b6-sic]] →
