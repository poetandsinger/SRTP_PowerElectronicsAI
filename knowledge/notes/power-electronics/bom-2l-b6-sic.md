---
title: Traction Inverter Bill of Materials (2L-B6 SiC)
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: theoretical
tags: [power-electronics, traction-inverter, bom, two-level, sic, gate-driver, dc-link, design]
review_by: 2026-10-17
---

## What This Note Is

A **component-class BOM** for the 800V-class SiC 2L-B6 reference design ([[design-2l-b6-800v-sic]]), organized by function. Each line gives the sizing driver, a **representative part/part-class**, and its citation. Intentionally *class-level, not procurement-level*: exact MPNs, prices, and stock go stale fast and are better pulled live by the DigiKey/Nexar adapters noted in the handoff. Sizing rationale for every quantity is in [[procedure-design]].

> **Priced version:** [[bom-price-database]] carries real, dated distributor prices for these parts (and the distributor-vs-volume caveat). A real, buildable instantiation of this BOM — with vendor part numbers — is the Wolfspeed/TI CRD in [[reference-design-wolfspeed-ti-300kw-800v]].

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; representative parts are drawn from the part-classes already catalogued in [[circuit-components]] to keep this grounded. Part numbers are illustrative of the class and must be datasheet-checked before use (`[T]`), cf. schematic-vs-datasheet review [68].

---

## 1. Power Stage

| # | Function | Qty | Sizing driver (see [[procedure-design]]) | Representative class | Cite |
|---|----------|-----|----------------------------------------|----------------------|------|
| 1.1 | Main switch | 6 (or 3 half-bridge modules) | 1200 V, ~450 A, hot Rds(on)~5 mΩ; §2 | SiC MOSFET module — Wolfspeed XM3 / onsemi VE-Trac Direct / Infineon CoolSiC HybridPACK class | [38][39][36], [[circuit-components]] §1.2 |
| 1.2 | Freewheel path | intrinsic | body diode / co-pack SBD, dead-time conduction; §3 | integral to SiC module | [T], components §1.2 |
| 1.3 | Module qualification | — | AQG 324 / AEC-Q101 power/temp cycling | automotive-qualified module | [88][89] |

Packaging note: direct-cooled pin-fin baseplate assumed (§Thermal); some OEMs integrate the DC-link cap onto the module to cut Lσ [[circuit-components]] §5 [37].

---

## 2. Gate Drive (per switch ×6)

| # | Function | Qty | Sizing driver | Representative class | Cite |
|---|----------|-----|---------------|----------------------|------|
| 2.1 | Isolated gate-driver IC | 6 | ≥5 kV reinforced, ±10 A, desat <1.5 µs, Miller clamp; §5 | TI UCC21750 / Infineon 1EDI3021AS / onsemi NCD57000 class | [40][86], [[circuit-components]] §2.2 |
| 2.2 | Isolated bias supply | 6 | +15 V / −4 V, few W/ch | Murata MGJ2 / RECOM push-pull DC-DC class | [40], components §2.3 |
| 2.3 | Gate resistors | 12 | Rg(on)/Rg(off) for di/dt vs loss; §5 | pulse-rated thick-film | [40] |
| 2.4 | Gate-loop caps / clamp | per ch | Vgs stability, Miller-clamp path | X7R/C0G MLCC | [T], components §2 |

---

## 3. DC-Link & HV Bus

| # | Function | Qty | Sizing driver | Representative class | Cite |
|---|----------|-----|---------------|----------------------|------|
| 3.1 | DC-link capacitor | 1 bank (~500 µF) | ~120 A rms ripple, ≥900 Vdc, low ESL; §4 | metallized-PP **film** module (TDK/CDE automotive DC-link class) | [41][84][90], [[circuit-components]] §3 |
| 3.2 | Laminated busbar | 1 | Lσ < 10–15 nH; §8 | Cu laminated planes + thin dielectric | [41][25], components §5 |
| 3.3 | HV fuse | 1 | pack fault current, HV rating | automotive HV fuse | [T] |
| 3.4 | Main + negative contactors | 2 | make/break HV, precharge sequence | HV EV contactor | [T] |
| 3.5 | Pre-charge resistor | 1 | limit `C·dV/dt` inrush; [schematics] §5 | power resistor | [50] |
| 3.6 | Active-discharge / bleed | 1 | bus <60 V on shutdown | discharge network | [55][85] |

---

## 4. Sensing

| # | Function | Qty | Sizing driver | Representative class | Cite |
|---|----------|-----|---------------|----------------------|------|
| 4.1 | Phase-current sensor | 2–3 | BW ≥50 kHz, isolated, ±1–2%; §6 | Allegro ACS37002 (Hall) / Infineon TLI4971 / TI INA253 + shunt class | [42], [[circuit-components]] §4.2 |
| 4.2 | DC-link voltage sense | 1 | isolated divider/iso-amp; §6 | isolated amplifier + divider | [50], components §4 |
| 4.3 | Module temperature | 1–3 | NTC → thermal model; §6 | module-integrated NTC | [25] |
| 4.4 | Rotor position | 1 | ±0.1°, ASIL-D; §6 | resolver + RDC, or inductive encoder | [48], [[control-schemes]] §5.1 |

---

## 5. Control & Compute

| # | Function | Qty | Sizing driver | Representative class | Cite |
|---|----------|-----|---------------|----------------------|------|
| 5.1 | Motor-control MCU | 1 | ASIL-D, motor-PWM, resolver IF, ≥6 ADC; §9 | Infineon AURIX TC3xx / TI C2000 / NXP S32K3 class | [T], [[control-schemes]] §7.1 |
| 5.2 | Software architecture | — | AUTOSAR Classic, ASIL-D partitioning | AUTOSAR stack | [53] |
| 5.3 | LV power tree | 1 | 12 V → 5/3.3 V + isolated rails | automotive PMIC + DC-DC | [T] |

---

## 6. Thermal, EMI & Mechanical

| # | Function | Qty | Sizing driver | Representative class | Cite |
|---|----------|-----|---------------|----------------------|------|
| 6.1 | Cold plate / heatsink | 1 | pin-fin water-glycol, 10–20 kW/L; §3 | direct-cooled pin-fin | [T], [[circuit-components]] §6.1 |
| 6.2 | Thermal interface | — | low Rth, no pump-out | phase-change / graphite pad | [T], components §6.2 |
| 6.3 | EMI input filter | 1 | CISPR 25 conducted/radiated | CM choke + Y-caps | [56][54] |
| 6.4 | Enclosure / HV connectors | 1 set | IP67, HVIL, creepage per §isolation | automotive HV connector set | [86] |

---

## 7. Rough Cost Split (order-of-magnitude, `[T]`)

Not a quote — a **relative** allocation to guide design effort, from public teardown-level commentary [T], [[index-traction-inverter]]:

| Subsystem | Share of inverter BOM | Note |
|-----------|:---:|------|
| SiC power modules | ~40–50% | dominant; falls as $/A drops [29] |
| DC-link film cap | ~10–15% | film premium vs electrolytic [41] |
| Gate drive + isolation | ~5–10% | 6 isolated channels |
| Sensing (current/position/temp) | ~5–10% | resolver + Hall dominate |
| Control MCU + PCB | ~5% | |
| Cooling + busbar + mech/connectors | ~15–20% | |

**The switch dominates**, so device selection and thermal/loss design (which set how much silicon you buy) are where cost is won or lost [28][43].

> [!note] **Device/loss now PLECS-validated (Track-1, 2026-07-23)** `[sim]`. The main-switch choice (row 1.1) is
> confirmed: **6× Wolfspeed CAB450M12XM3** (1200 V/450 A/2.6 mΩ SiC), loss model loaded (Ron = 3.6 mΩ = datasheet),
> validates at **99.07% η / 175 °C at the 300 kW CRD** and 99.32% at the design's 150 kW peak — a single half-bridge
> module per leg carries the design well inside its limits ([[design-2l-b6-800v-sic]]). This fixes the switch
> quantity/class the BOM's Red Team flagged as needing a validated design.

---

## Red Team

**Steelman against:** A BOM implies a buildable, sourced design. This one is class-level with `[T]` representative parts and an order-of-magnitude cost split — it cannot be sent to procurement, and treating it as such would be wrong. Real MPNs have footprints, lifecycle, and second-source constraints absent here.

**How it could be false:**
1. **Representative parts may be mis-scoped** — e.g., a named gate-driver IC might lack an automotive grade or the exact isolation rating; every `[T]` MPN needs a datasheet check [68].
2. **Cost split is teardown-derived commentary**, not audited BOM cost; the SiC share especially moves with wafer economics [29] (a `motivated` source, [[circuit-components]] Red Team).
3. **Quantities assume the anchor spec** — a different Vdc/power changes module count, paralleling, and cap bank.
4. **Missing lines** a production BOM needs: snubbers, current-sense burden/filters, protection ICs, crystal/clock, watchdog, connectors pinout, conformal coat.

**What would change my mind:** A live DigiKey/Nexar pull resolving each class to an in-stock automotive MPN, plus a PLECS-validated design fixing the quantities.

**Residual doubt:** Good as a design checklist and RAG scaffold that maps function → part-class → citation. Not a procurement artifact.

---

> **References:** [[citations]]

← [[procedure-design]] | [[design-2l-b6-800v-sic]] | [[circuit-components]] →
