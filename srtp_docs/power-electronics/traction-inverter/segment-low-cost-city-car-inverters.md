---
title: "Segment Landscape — Low-Cost / City-Car Traction Inverters"
type: topic
field: power-electronics
created: 2026-07-18
updated: 2026-07-18
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, igbt, mosfet, bom, market-research, review]
review_by: 2026-10-18
---

## What This Is

The **production landscape** for low-cost A-segment / city BEV traction inverters — the sourced data behind [[power-electronics/traction-inverter/worked-example-microcar-96v-mosfet]]. RAG backbone for the MAS on the **cost-down** end of the space. Web-researched 2026-07-18; tags **[H]** OEM · **[M]** reputable · **[TPS]** aggregator · **[mkt]** marketing/AI-blurb.

> **Blunt caveats:** (1) inverter **device (LV MOSFET vs IGBT) is inference** from bus voltage — **no teardown opened names a die**; (2) inverter **BOM $ cost does not exist in sourced form** (MarkLines paywalled; no Munro city-car inverter) — **fabricate no $/kW**; (3) Wuling pack voltage is internally inconsistent (~85–115 V) — only the **≪400 V** magnitude is safe.

## 1. Vehicles — Power, Voltage, Device (sourced where possible)

| Vehicle | Power | **Bus** | Energy | Device (class) | Cite/Tag |
|---------|------:|--------:|-------:|----------------|----------|
| **Wuling Hongguang Mini EV** | 20–30 kW | **~96 V** (26S, ~85–115 V) | 9.2–26.5 kWh | **LV Si MOSFET** *(inferred)* | [164][M/TPS] |
| Dacia Spring / Renault Kwid | 33–48 kW | ~240 V | 26.8 kWh | Si IGBT *(inferred)* | [165][M] |
| BYD Seagull | 55 kW | **403 V** | 30–39 kWh | Si IGBT *(inferred)* | [165][M] |
| Changan Lumin | 30 kW | n/p | 13–28 kWh | — | [165][TPS] |
| Tata Tiago/Punch EV | 45–95 kW | ~300 V+ (est) | 19–35 kWh | **liquid-cooled** MCU (device n/p) | [165][H cooling] |
| MG Comet | 30 kW | n/p | 17.3 kWh | — | [165][TPS] |
| Citroën Ami (**L6e**) | 6 kW | **48 V** | 5.5 kWh | LV MOSFET | [165][M] |

**Tri-modal in voltage** (48 → 96 → 240 → 403 V), and **SiC is absent from the entire class** [165]. Device follows voltage: **<~200 V → LV Si MOSFET; >~200 V → Si IGBT** [165][M].

## 2. Cost-Down Levers (evidence-ranked)

1. **Low bus voltage (Wuling ~96 V) — the load-bearing lever** [confirmed]. Enables LV Si MOSFETs (cheapest per kW, no IGBT `Vce0` knee), thinner isolation, cheaper caps, relaxed creepage, less HV-safety content.
2. **"3-in-1" integration** (motor+inverter+reducer) — shrinks housings/harness/seals [164][M].
3. **Deliberately minimal content** — MarkLines' own summary: "simple structure… lack of equipment" [164][M].
4. **Simplest cooling** — likely **air** on the stock low-power Wuling unit (*conflicting/unverified*; liquid claims trace to aftermarket-kit marketing) [164].
5. **Reduced sensing / no redundancy** — expected, but **no teardown confirmed sensor count** [inference].

## 3. Why the Segment Matters (volume)

**Wuling Mini EV: >1,000,000 cumulative by early 2023; world's best-selling EV 2021–22** (395k/2021, ~405k/2022), ~$4,200 launch price [164][M]. At 250k–550k units/yr on one nameplate, **$1 saved on the inverter = $250k–550k/yr** — the reason this segment optimizes ruthlessly for per-unit BOM over efficiency/density.

**Verdict:** the dominant driver is **absolute BOM cost / lowest $-per-kW**, and the biggest lever is **bus voltage** — chosen *low* here (opposite to the 800 V premium designs). The trade spent is power density + current-handling, not (as intuition suggests) switch efficiency (see the worked example's LV-MOSFET-vs-IGBT result).

## Red Team

**Steelman against:** This is the **least-sourced** segment note in the vault. The load-bearing device claim (LV MOSFET) is inference; the cost claim has **zero sourced $**; the cooling is conflicting; the flagship voltage figure is internally inconsistent. It's a segment shape hung on one confirmed fact (Wuling's ≪400 V pack) plus device-economics reasoning. A MAS must not treat any device/cost specific here as fact.

**How it could be false:**
1. **Device unconfirmed** — if Wuling uses an LV IGBT or integrated ASIC, the "MOSFET" specifics change (voltage-picks-device principle still holds) [164].
2. **No inverter cost anywhere** — MarkLines paywalled, no Munro city-car inverter; the relative $/kW ordinal is general knowledge, not a quote [164][165].
3. **Voltage figure soft** — battery-vendor blog, 83-vs-96-vs-115 V internal conflict [164].
4. **Cooling unresolved** — air-vs-liquid claims both appear; liquid ones are aftermarket marketing [164].
5. **Chinese-market specs shift by model year** via TPS aggregators [165].

**What would change my mind:** a real Wuling-class inverter teardown naming the die + a should-cost BOM; a confirmed stock-unit cooling scheme; a reconciled pack voltage from a primary source.

**Residual doubt:** The *segment shape* — tri-modal low voltage, LV-MOSFET-below-200 V / IGBT-above, SiC absent, cost-and-volume-driven, voltage as the lever — is sound and matches the confirmed low Wuling pack. This is the segment where the honest RAG entry is "here is the structure and where the data runs out," not a spec table to trust.

---

> **References:** [[citations]]

← [[power-electronics/traction-inverter/worked-example-microcar-96v-mosfet]] | [[power-electronics/traction-inverter/bom-price-database]] | [[power-electronics/traction-inverter/traction-inverter-index]] →
