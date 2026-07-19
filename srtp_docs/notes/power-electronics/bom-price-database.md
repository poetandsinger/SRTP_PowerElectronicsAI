---
title: BOM Component Price Database (2L-B6 SiC)
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, bom, sizing, design]
review_by: 2026-10-17
---

## What This Is

A **priced** version of the component-class BOM ([[bom-2l-b6-sic]]) for the SiC 2L-B6 reference designs. Each line carries a representative part, a **single-unit distributor price** with its source and date, and a note where the price is an estimate. It gives an LLM designing a board real cost anchors — with the critical caveat below.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training-knowledge estimate. Prices accessed **2026-07-17** via DigiKey [98] unless noted; they go stale — re-pull before use.

> ⚠️ **Single-unit distributor price ≠ automotive volume price.** The whole Tesla Model 3 SiC inverter cost ~**$810** in 2018 at OEM volume [94], yet **one** CAB450M12XM3 module lists at ~**$898** single-unit today [92][98]. OEM pricing at 10k–1M/yr is commonly **5–10× lower** per part than distributor 1-off. Use this table for *relative* sizing and prototype budgeting, not for a production cost model.

---

## Priced BOM — 300 kW / 800 V SiC class (Wolfspeed/TI CRD parts) [91]

| # | Function | Representative part | Spec | Qty | Unit price (1-off) | Basis | Cite |
|---|----------|---------------------|------|----:|-------------------:|-------|------|
| 1 | SiC power module | **Wolfspeed CAB450M12XM3** | 1200 V, 450 A, half-bridge | 3 | **$898.44** | DigiKey 2026-07-17 | [92][98] |
| 2 | Isolated gate driver | **TI UCC5880-Q1** (UCC5880QDFCRQ1) | 20 A, 5 kV, adjustable, desat | 6 | **≈$11** | DigiKey 2026-07-17 | [93][98] |
| 3 | Control MCU | **TI AM2634-Q1** | Arm R5F, ASIL, motor PWM | 1 | ≈$20–40 `[T]` | class estimate | [91][T] |
| 3b | (alt MCU) | **Infineon AURIX TC397** (TC397XP…) | 6-core, ASIL-D | 1 | **$78.26** | DigiKey 2026-07-17 | [98] |
| 4 | Phase-current sensor | **LEM LF 510-S** | closed-loop Hall, 500 A, ±0.6% | 2–3 | ≈$40–60 `[T]` | distributor class | [100][T] |
| 5 | Isolated bias DC-DC | Murata MGJ2 class | +15/−4 V, per channel | 6 | ≈$5–8 `[T]` | class estimate | [40][T] |
| 6 | DC-link capacitor | TDK xEVCap / B3277x film class | ~300–600 µF, ≥900 V | 1 bank | ≈$40–90 `[T]` (quote at volume) | vendor quote-only | [41][90][T] |
| 7 | Gate resistors / MLCC | thick-film / X7R | per channel | many | <$0.50 ea `[T]` | class estimate | [T] |
| 8 | HV contactors | Gigavac/TE EV contactor | make/break HV | 2–3 | ≈$30–80 `[T]` | class estimate | [T] |
| 9 | HV fuse | automotive HV fuse | pack fault current | 1 | ≈$15–40 `[T]` | class estimate | [T] |
| 10 | Resolver + RDC | VR resolver + resolver-to-digital IC | ±0.1° position | 1 | ≈$15–40 `[T]` | class estimate | [48][T] |
| 11 | Laminated busbar | custom Cu laminate | Lσ < 15 nH | 1 | custom (NRE) `[T]` | — | [25][T] |
| 12 | Cold plate | pin-fin water-glycol | 10–20 kW/L | 1 | custom (NRE) `[T]` | — | [T] |

**Anchored prices (verifiable):** #1 module $898.44, #2 driver ≈$11, #3b AURIX $78.26 — all DigiKey 2026-07-17 [98]. Everything marked `[T]` is a class estimate pending a live distributor pull.

---

## Rough Prototype vs Volume (300 kW class)

| Basis | Semiconductors | Rest of BOM | Approx total | Note |
|-------|---------------:|------------:|-------------:|------|
| **Distributor 1-off** [98] | ~$2,700 (3× module) | ~$300–600 | **~$3,000–3,300** | prototype budget only |
| **OEM volume (illustrative)** [94] | far lower (5–10×) | lower | **~$500–1,000** class | cf. Tesla inverter ~$810 (2018, 211 kW) [94] |

The switch dominates either way — which is why device selection and loss/thermal design (how much silicon you must buy) is where cost is won [28][43], [[bom-2l-b6-sic]] §7.

---

## For the AI Pipeline

PE-MAS ships DigiKey / Nexar-Octopart data adapters (handoff §7). This note is the **static fallback / schema**; the live path is those adapters resolving each part-class to an in-stock MPN + current price. Store price with an as-of date and source, exactly as here — a price without a date is a bug.

---

## Red Team

**Steelman against:** A "price database" implies authority these numbers don't have. Most rows are `[T]` estimates; the three anchored ones are single-unit distributor snapshots that (a) expire fast and (b) mislead by ~10× versus the automotive volume pricing that actually matters. Automotive DC-link caps, busbars, and cold plates are custom/NRE items with no meaningful catalog price at all.

**How it could be false:**
1. **Distributor ≠ volume** by ~5–10× — the headline caveat; using these for a production cost model would be wrong [94][98].
2. **Snapshots decay:** semiconductor prices move monthly; SiC is on a declining curve [29].
3. **`[T]` rows are guesses** at the class level, not quotes.
4. **Custom items (cap bank, busbar, cold plate)** are quote/NRE — the biggest cost uncertainties are the least catalog-priced.

**What would change my mind:** a live DigiKey/Nexar pull dated at use-time, plus at least one real OEM-volume quote to calibrate the distributor-to-volume ratio.

**Residual doubt:** Useful as *relative* cost structure (module dominates; SiC premium vs IGBT) and as a prototype budget. Not a production BOM cost. The date and source on every number are the point — treat undated prices as invalid.

---

> **References:** [[citations]]

← [[bom-2l-b6-sic]] | [[reference-design-wolfspeed-ti-300kw-800v]] →
