---
title: "Segment Landscape — Heavy-Duty / Class-8 Truck Traction Inverters"
type: topic
field: power-electronics
created: 2026-07-18
updated: 2026-07-18
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, sic, reliability, market-research, review]
review_by: 2026-10-18
---

## What This Is

The **production landscape** for Class-8 / long-haul BEV truck traction inverters — the sourced industry data behind [[power-electronics/traction-inverter/worked-example-truck-800v-sic]]. RAG backbone for the MAS: "what does a real HD truck inverter look like, and what drives it?" Web-researched 2026-07-18; every figure tagged **[H]** OEM/DOE · **[M]** trade press · **[TPS]** aggregator · **[mkt]** press-release.

**Blunt caveat:** **no mainstream truck OEM publicly discloses its production inverter's device, module, or cooling.** The power/voltage/battery rows are solid; the inverter-internals rows are inference and flagged.

## 1. Vehicles — Power & Voltage (sourced)

| Vehicle | Peak | **Continuous** | Bus | Battery | Tag | Cite |
|---------|-----:|---------------:|----:|--------:|-----|------|
| Tesla Semi | 800 kW | ~525 kW `[mkt]` | **~1000 V** | 822/548 kWh (CARB) | [H peak]/[mkt cont] | [163] |
| Mercedes **eActros 600** | 600 kW | **400 kW** | **800 V** | 621 kWh LFP | [H] | [162] |
| Volvo FH Electric | — | ~490 kW | **<750 V** | 450–540 kWh | [M] | [163] |
| Freightliner eCascadia | — | 240–350 kW | **400 V** | 291–438 kWh | [H] | [163] |
| MAN eTGX | — | 400 kW | **800 V** | ≤480 kWh | [M/H] | [163] |
| Scania 45 R/S | — | 400–450 kW | ~650 V (inf.) | ≤560 kWh | [H/M] | [163] |
| Nikola Tre BEV | ~481 kW | — | **800 V** | 733 kWh | [M/mkt] | [163] |
| Windrose R700 | ~1044 kW | — | **800 V** | 729 kWh | [mkt] | [163] |

**Pattern:** the meaningful spec is **continuous ~400–490 kW, peak ~1.3–1.5×** — the inverse of a passenger car's brief-peak emphasis. **"Everything is 800 V" is only half true:** verified 800 V (eActros/MAN/Nikola/Windrose), ~1000 V (Tesla Semi), <750 V (Volvo/Renault), 400 V (eCascadia).

## 2. Device / Module / Cooling — the undisclosed layer

- **No OEM discloses production inverter internals.** Sourceable: Tesla Semi = SiC "same as Cybertruck" (inheritance, [M]); eActros e-axle in-house Daimler, device undisclosed [162]; **Cummins/Accelera 17Xe e-axle = Danfoss Editron SiC inverter** — the clearest sourced HD-SiC datapoint (a Tier-1, not a named truck) [163][M].
- **Do NOT conflate:** the "BorgWarner Viper + ST 750 V SiC" deal is **Volvo *Cars*, not Volvo Trucks** [163].
- **Direction (Tier-1 generic):** **double-side-cooled sintered SiC modules** (Infineon HybridPACK DSC, Danfoss DCM, ZF AxTrax) for continuous-load heat + power-cycling life — inference, not per-vehicle-confirmed [163].

## 3. Mission Profile & Lifetime (the design driver)

- **DOE HEP program (the clearest intent statement):** **800 V, 250 kW *continuous* SiC inverter "for high continuous loads and the shock/vibration of heavy-duty trucks"** [161][H].
- **Grade standard:** Davis Dam ~**7% grade, ~11 km climb** — junction dwells near limit for many minutes; VECTO long-haul cycles at ~40 t GCW [163][TPS].
- **Lifetime:** Renault E-Tech T **8 yr / 1,000,000 km** battery warranty [163][H]; commercial inverters cited for **>2M power cycles** vs passenger [163][TPS]. Passenger DOE contrast: 480k km / 15 yr [163].
- **SiC benefit:** ~**4% mission efficiency** over Si-IGBT at HD partial load [163][TPS].

**Verdict:** the dominant driver is **thermal-lifetime / power-cycling under sustained continuous load + steep-grade soak — not 0–100 peak.** This is why the worked example uses a rainflow→Miner workflow, not an efficiency-corner one.

## Red Team

**Steelman against:** This "landscape" is mostly power/voltage/battery specs (solid) wrapped around an inverter layer that is **entirely undisclosed** — the device/module/cooling section is inference, and several headline numbers ("525 kW continuous," ">2M cycles") are marketing or generic, not measured ratings [163]. A MAS retrieving this could mistake the inferred SiC-DSC direction for confirmed fact.

**How it could be false:**
1. **Inverter internals unsourced** — no named truck confirms SiC-vs-IGBT, module, or cooling; the Danfoss 17Xe and Tesla-Cybertruck-inheritance are the only real anchors, and neither is a spec'd truck inverter [163].
2. **"Continuous 400–490 kW"** mixes OEM ratings (eActros 400 kW [H]) with derived/press figures (Tesla 525 kW [mkt]).
3. **Voltage inference** for Scania/Renault (~650 V) is platform-guessed, not published.
4. **Mission/lifetime numbers** (Davis Dam, >2M cycles, 1M km) are real but from mixed [H]/[TPS]/press — the >2M-cycle figure is generic industry, not per-inverter.

**What would change my mind:** an OEM or Tier-1 spec sheet naming a production HD inverter's module + cooling; a published HD inverter power-cycling/B10 dataset; a measured VECTO Tj mission profile.

**Residual doubt:** The *segment shape* — continuous-power-dominated, mixed 400–1000 V, lifetime-driven, SiC-DSC direction — is well-supported and the right RAG frame. Every inverter-internals specific is inference until an OEM discloses one.

---

> **References:** [[citations]]

← [[power-electronics/traction-inverter/worked-example-truck-800v-sic]] | [[power-electronics/traction-inverter/reliability-and-lifetime]] | [[power-electronics/traction-inverter/traction-inverter-index]] →
