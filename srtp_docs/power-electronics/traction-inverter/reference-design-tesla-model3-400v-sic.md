---
title: "Reference Design — Tesla Model 3 400V SiC (production)"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-17
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, design, reference-design, two-level, sic]
review_by: 2026-10-17
---

## What This Is

The **highest-volume SiC traction inverter in production** and the design that started mass-market SiC adoption (2017–2018). Documented through teardowns (System Plus/Yole, Munro) rather than a vendor design kit, so specs are teardown-derived, not datasheet-exact [94][31]. It anchors the **400 V** end of the design space against the 800 V reference designs.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge. Teardown figures are `reliability: medium` — second-hand, some proprietary detail unknowable [94].

---

## Specification (teardown-derived) [94][31]

| Item | Value | Note |
|------|-------|------|
| Topology | 2-level B6 | discrete-module bridge |
| DC bus | ~400 V class | Model 3/Y pack |
| Output power | ~211 kW (rear drive unit) | performance variants higher |
| Devices | **24× ST 650 V SiC MOSFET modules** (2-in-1) | 8 die paralleled per switch position in early builds; later Gen-3 die reduced count |
| Packaging | copper-clip die attach, copper baseplate, **pin-fin** direct cooling | high power density |
| Controller | Tesla custom (early TI C2000-class) | [T], [[power-electronics/traction-inverter/control-schemes]] §7.1 |
| Inverter cost (2018) | ~**$810** | Munro estimate [94] |

**Why 24 discrete modules, not 3 big ones:** paralleling many small 2-in-1 modules across the phase legs spreads heat and current and let ST use a mature 650 V planar die — a different philosophy from the 3-module CAB450 approach in [[power-electronics/traction-inverter/reference-design-wolfspeed-ti-300kw-800v]] [94][92].

---

## What It Teaches

- **650 V devices on a 400 V bus** — the T-type/2L device-voltage logic in [[power-electronics/traction-inverter/circuit-topologies]] §4: at 400 V you can use cheaper, mature 650 V SiC; at 800 V you are forced to 1200 V (the reference-design anchor's reason for 1200 V) [28].
- **Volume pricing reality:** a whole 2018 SiC inverter for ~$810 [94] is *less than one* 1200 V distributor module today [92][98] — the sharpest illustration of volume-vs-distributor pricing in [[power-electronics/traction-inverter/bom-price-database]].
- **Paralleling small die** is a valid alternative to large modules — relevant to the "how much silicon" cost driver in [[power-electronics/traction-inverter/bom]] §7.

---

## Red Team

**Steelman against:** Every number here is from teardown analysts, not Tesla or ST engineering data [94][31]. Die counts, exact ratings, and switching frequency are inferred or proprietary; reports from different years disagree (48 die vs 24 die as Gen-3 changed). Treating any single figure as exact is unsafe.

**How it could be false:**
1. **Die-count/config drift:** early vs Gen-3 builds differ; sources conflict [94].
2. **Cost figure is an analyst estimate** ($810, 2018) and predates SiC price declines [94][29].
3. **Control/switching detail is `[T]`** — Tesla does not publish it [[power-electronics/traction-inverter/control-schemes]] Red Team.
4. **400 V "class"** spans pack SOC; exact bus voltage varies.

**What would change my mind:** primary ST/Tesla documentation (unlikely) or a current teardown with updated Gen-3 device data.

**Residual doubt:** Directionally reliable and historically decisive; not a source of exact design parameters. Use it for the 400 V-vs-800 V and volume-cost lessons, not for datasheet numbers.

---

> **References:** [[citations]]

← [[power-electronics/traction-inverter/reference-designs-index]] | [[power-electronics/traction-inverter/reference-design-nissan-leaf-400v-igbt]] →
