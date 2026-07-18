---
title: Reference Designs Index
type: map
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
tags: [power-electronics, traction-inverter, reference-design, design, index]
---

## What This Is

The **worked and real reference designs** in this build manual. One synthetic anchor (fully derived and cited) plus three real designs (one vendor kit, two production teardowns) spanning voltage class and device technology. Together they let an LLM answer "show me a complete traction inverter of type X" with a grounded example, and give the PLECS effort a calibration target.


**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge.

## The Designs

| Design | Class | Power | Device | Grounding | Note |
|--------|-------|------:|--------|-----------|------|
| [[reference-design-2l-b6-sic-800v]] | 800 V 2L | 150 kW | 1200 V SiC | **synthetic** — derived + cited | The anchor; sizing math worked end-to-end in [[design-procedure]] |
| [[reference-design-wolfspeed-ti-300kw-800v]] | 800 V 2L | 300 kW | 1200 V SiC (CAB450M12XM3) | **real vendor CRD** [91] | Public part numbers + BOM; PLECS calibration anchor (>98%, 32 kW/L) |
| [[reference-design-tesla-model3-400v-sic]] | 400 V 2L | ~211 kW | 650 V SiC (ST, 24 modules) | **production teardown** [94] | Highest-volume SiC inverter; 400 V lesson + volume-cost reality |
| [[reference-design-nissan-leaf-400v-igbt]] | 400 V 2L | 80 kW | Si IGBT | **production teardown** [95] | The IGBT baseline SiC is measured against; bigger DC-link, lower efficiency |

## How To Read Them

1. **Learn the method** on the synthetic anchor + [[design-procedure]].
2. **Validate the method** against the Wolfspeed/TI CRD — real parts, measured metrics [91].
3. **See the trade-space** across 800 V-SiC → 400 V-SiC → 400 V-IGBT: device voltage, DC-link size, efficiency, and cost all move together.
4. **Price it** in [[bom-price-database]] (and mind distributor-vs-volume pricing).

## The Spectrum in One Line

- **800 V + 1200 V SiC** → highest efficiency/density, forced to 1200 V devices, the industry's forward direction [28][91].
- **400 V + 650 V SiC** → mature cheaper devices, highest volume today (Tesla) [94].
- **400 V + Si IGBT** → lowest cost, lower efficiency, bigger passives — the incumbent floor [95].

Not built (noted only): 3L-NPC / 3L-TNPC / 3L-ANPC and dual-inverter — see the alternatives table in [[reference-design-2l-b6-sic-800v]] and [[circuit-topologies]].

---

> **References:** [[citations]]

← [[traction-inverter-index]] | [[design-procedure]] | [[bom]] →
