---
title: "Segment Landscape — High-Performance / Motorsport Traction Inverters"
type: topic
field: power-electronics
created: 2026-07-18
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, sic, thermal, efficiency, market-research, review]
review_by: 2026-10-18
---

## What This Is

The **production/motorsport landscape** for high-performance traction inverters — the sourced data behind [[worked-example-performance-800v-sic]]. RAG backbone for the MAS on the **power-density + transient-thermal** end of the design space. Web-researched 2026-07-18; tags **[H]** OEM/DOE/IEEE · **[M]** trade press · **[TPS]** aggregator · **[mkt]** vendor superlative.

## 1. Vehicles — Power, Peak Duration, Voltage (sourced)

| System | Peak | **Peak duration** | Continuous | Inverters | Bus | Cite/Tag |
|--------|-----:|-------------------|-----------:|:---------:|----:|----------|
| **Porsche Taycan Turbo GT** | **815 kW** | **2 s** (700 kW/**10 s**) | **580 kW** | 2 (SiC pulse, rear) | 800 V | [158][H] |
| Lucid Air Sapphire | ~900 kW sys | n/p | — | 3 | ~900 V | [M] |
| Rimac Nevera | 1408 kW | n/p | — | **4** (rear 480 kW/1000 Arms ea) | 800 V | [TPS/H] |
| Tesla Model S Plaid | ~760 kW | n/p | — | 3 (810 A SiC) | ~400 V | [M/TPS] |
| McMurtry Spéirling | ~745 kW | n/p | — | 2 | — | [M] |
| **Formula E Gen3** | **350 kW** race | lap-energy-limited | — | rear MGU + front FPK | **900 V** | [H] |

**Porsche's 815 kW/2 s → 700 kW/10 s → 580 kW continuous is the cleanest published *duration-gated peak* (Zth-pulse) in production** [158]. FE Gen3: 350 kW race / **600 kW total regen**, min car 840 kg, FPK (Lucid) **32 kg** [H].

## 2. Power Density — verified vs marketing (the headline metric)

- **DOE/ORNL trajectory:** inverter **13.3 (2012) → 34 (2022) → 100 kW/L target (2025)**; $2.7/kW, 98% eff [159][H].
- **Wolfspeed 300 kW SiC reference: ~32–34 kW/L** (<9 L) — the credible "SiC SOTA ≈ 33 kW/L" anchor [160][H].
- **100 kW/L** = double-side-cooled SiC + sintered-Ag interposer + mini-channel demonstrator (**lab, <1 L**, not production) [160][H].
- **Marketing (flagged):** McLaren IPG5 ">125 **kVA**/L, >85 kVA/kg" — **kVA not kW**, ~90 kW/L real [mkt]; YASA "59 kW/kg motor / ~100 kW/kg inverter" — prototype/forward claim [mkt]; Lucid "24 kW/kg drive unit" is **unsupported** (real ~6.5–8.8 kW/kg at unit level) [mkt].

## 3. Device / Cooling / Transient Thermal

- **SiC modules:** Lucid = **Wolfspeed XM3 1200 V** [H]; Wolfspeed CAB450M12XM3 = 1200 V/450 A; Tesla Plaid ~810 A SiC; Porsche 900 A pulse inverter [158]. 1200 V device on 800–900 V bus is the standard headroom.
- **Cooling = the density enabler:** **double-side-cooled (DSC)** SiC ("40% lighter, 30% smaller") + sintered-Ag + micro/mini-channel; local flux **~100–300 W/cm²** [160][M].
- **Transient thermal:** the peak is thermal-mass-gated — Porsche's 2 s/10 s vs continuous is the textbook `Zth`-pulse exploitation; SiC's 175 °C junction widens the burst headroom vs 125 °C Si [158][M].
- **fsw:** not publicly specified for any named performance inverter — any number is a guess.

**Verdict:** the dominant driver is **volumetric/gravimetric power density + transient `Zth`-pulse capability (a 2–10 s burst above continuous) — not partial-load efficiency.** (Efficiency still matters for FE energy limits and Lucid range, but is secondary to the *hardware* design driver.)

## Red Team

**Steelman against:** The one rock-solid engineering datapoint is Porsche 815/2 s, 700/10 s, 580 cont [158]; almost everything else on *density* is a DOE roadmap target, a single vendor reference (Wolfspeed 33 kW/L), or marketing superlatives in the wrong units (kVA, prototype kW/kg). A MAS could over-anchor on "100 kW/L" as achievable in production when it's a <1 L lab coupon.

**How it could be false:**
1. **Density superlatives are contaminated:** kVA≠kW (McLaren), prototype/forward (YASA), unit-level≠inverter-level (Lucid) — the "sourced" 60 kW/L DSC I use elsewhere is a mid-range estimate, not one datasheet [160].
2. **Peak durations** beyond Porsche are unpublished; Rimac/Plaid/Lucid peak-hold times are unknown.
3. **Per-inverter power splits** (Lucid Sapphire, Rimac) are inferred from system totals [TPS].
4. **fsw, Zth curves** for the named cars: **none public** — the transient-thermal story rests on Porsche's 2 s/10 s alone.

**What would change my mind:** a production (not lab) inverter at >50 kW/L with a full bill-of-volume; published Zth curves or peak-hold times for a named hypercar; the FIA FE inverter technical regs (device/fsw limits — not found).

**Residual doubt:** The *segment shape* — 800–900 V, SiC 1200 V, DSC+sintered+microchannel, density-and-burst-driven — is well-supported, and Porsche anchors the transient-thermal claim firmly. Every kW/L above ~34 and every peak-duration except Porsche's is a target/marketing/inference, not a production measurement.

---

> **References:** [[citations]]

← [[worked-example-performance-800v-sic]] | [[thermal-design]] | [[traction-inverter-index]] →
