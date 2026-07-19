---
title: "Reference Design — Wolfspeed/TI 300 kW 800V SiC (CRD300DA12E-XM3 / TIDM-02014)"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
sources: [sources/power-electronics/sachs-neuburger-2025-3l-tnpc, sources/power-electronics/wolfspeed-cab450m12xm3-datasheet]
tags: [power-electronics, traction-inverter, design, reference-design, two-level, sic, gate-driver, dc-link, efficiency]
review_by: 2026-10-17
---

## What This Is

A **real, published, buildable** 800 V / 300 kW SiC traction-inverter reference design co-developed by Wolfspeed and Texas Instruments — vendor part numbers, schematic, and BOM are public [91]. The closest thing to a "known-good answer" for the anchor class in [[design-2l-b6-800v-sic]], and the best template for the PLECS 2L-B6 SiC model on the critical path.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; prices are single-unit distributor snapshots (2026-07-17) [98], **not** automotive volume pricing.

---

## Headline Specification [91]

| Item | Value |
|------|-------|
| Topology | 2-level B6 (three CAB450M12XM3 half-bridge modules) |
| DC bus | 800 V |
| Output power | 300 kW (peak) |
| Phase current | 360 A rms |
| Efficiency | >98% |
| Power density | 32 kW/L |
| Max junction temp | 175 °C |
| Power-loop inductance | 5.3 nH (module 6.7 nH class) |
| Motor speed supported | >20,000 rpm |
| Cooling | pin-fin, water-glycol |

This confirms the procedure-design order of magnitude: an 800 V SiC 2L inverter reaches >98% efficiency at ~30 kW/L with 1200 V modules — consistent with [[procedure-design]] §3 [derived] and the SiC-2L ranges in [[index-traction-inverter]] [28].

---

## Actual Bill of Materials (key lines) [91]

| Function | Part | Spec | Unit price (1-off) | Cite |
|----------|------|------|-------------------:|------|
| Power module ×3 | **Wolfspeed CAB450M12XM3** ([[wolfspeed-cab450m12xm3-datasheet\|datasheet]]) | 1200 V, 450 A (2.6 mΩ), half-bridge SiC | ≈ **$898** ea | [92][98][166] |
| Gate driver ×6 | **TI UCC5880-Q1** | isolated, 20 A, real-time adjustable drive, desat, functional-safety | ≈ $11 | [93][98] |
| Control MCU | **TI AM2634-Q1** (AM263x, Arm Cortex-R5F) | real-time, functional-safety, motor-control PWM | — (class ~$20–40) | [91][T] |
| Phase-current sensor | **LEM LF 510-S** | closed-loop Hall, 500 A, ±0.6% | — (class ~$40–60) | [100][T] |
| Isolated bias | integrated-transformer bias supply | per-channel gate power | — | [91] |
| DC-link | film capacitor bank | 800 V bus, ripple/ESL duty | — (see [[bom-price-database]]) | [41][90] |

**Cost:** three CAB450 modules at single-unit distributor price ≈ **$2,700** — yet the entire Tesla Model 3 inverter cost ~**$810** in 2018 at automotive volume [94]. Distributor single-unit ≠ OEM volume pricing by roughly an order of magnitude; the price database says so explicitly [[bom-price-database]].

---

## How It Maps to Our Design Notes

- **Module = 1200 V/450 A**, exactly the class the sizing procedure lands on for an 800 V bus [[procedure-design]] §2 [92].
- **Gate driver = UCC5880-Q1** implements the desat / adjustable-drive / functional-safety primitives described in [[schematics]] §4 and [[circuit-components]] §2 [93].
- **Low power-loop inductance (5.3 nH)** meets the `Lσ < 10–15 nH` busbar budget [[procedure-design]] §8 [91].
- **360 A rms @ 300 kW** scales linearly to ~180 A rms @ 150 kW — matching the anchor design's peak-power current corner [derived, [[procedure-design]] §1].

---

## Use in This Project

The **template to replicate in PLECS**: build 2L-B6 with a 1200 V SiC model (CAB450-class parameters), FOC + IPMSM load, and validate efficiency/THD/thermal at the three bus corners [80]. Because the vendor publishes measured efficiency (>98%) and power density (32 kW/L), it is a **calibration anchor** — the PLECS model should reproduce these before any novel topology is trusted [91][58].

---

## Red Team

**Steelman against:** Vendor reference designs are marketing artifacts as much as engineering ones [91] — the ">98% efficiency" and "32 kW/L" are best-case, measured under favorable conditions Wolfspeed/TI chose, not a drive-cycle average. A single reference design also encodes one company's device bias (Wolfspeed silicon, TI control), not a neutral optimum.

**How it could be false:**
1. **Best-case metrics:** peak efficiency and peak power density are not WLTP-average numbers; partial-load and thermal-limited continuous ratings will be lower [28].
2. **Motivated source:** both vendors sell the parts in the BOM; the design is optimized to show them well [91].
3. **BOM is partial here:** I list headline parts from public summaries [91]; the full board (snubbers, sense conditioning, protection, connectors) is in the TI/Wolfspeed design files, not reproduced.
4. **Prices are single-unit snapshots** [98] and swing with market and quantity.

**What would change my mind:** the full published BOM/schematic parsed from the TI design guide (TIDUF23A) [91], and a PLECS model reproducing the >98%/32 kW/L claims at stated conditions.

**Residual doubt:** The strongest single grounding point in the whole design cluster — a real, measured, buildable 800 V SiC 2L inverter — but read its metrics as vendor best-case, not guaranteed drive-cycle performance.

---

> **References:** [[citations]]

← [[index-reference-designs]] | [[design-2l-b6-800v-sic]] | [[bom-price-database]] →
