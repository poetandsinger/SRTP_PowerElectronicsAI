---
title: "Worked Example — City Microcar Inverter (~96 V LV Si-MOSFET, cost-down)"
type: topic
field: power-electronics
created: 2026-07-18
updated: 2026-07-18
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, design, igbt, mosfet, two-level, bom, example]
review_by: 2026-10-17
---

## What This Is

A worked example driven by **absolute BOM cost / lowest $-per-kW** — the A-segment city car (Wuling Mini EV class, ~$4.2 k, >1 M units/yr [164]). The dominant lever is **DC-bus voltage**: the Wuling runs a **~96 V pack** [164], which enables the cheapest possible power stage. Runnable model: `worked-designs/microcar-96v-mosfet/microcar_cost.py`.

> **Brutal caveat (read first):** the Wuling *inverter device* (low-voltage Si MOSFET) is an **engineering inference from the confirmed ~96 V bus, not teardown-confirmed**; and the inverter **BOM $ cost is unsourced** (MarkLines paywalled; no Munro city-car inverter) [164]. This note therefore makes a **structural (relative) cost argument only — no fabricated $/kW.**

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training/undergrad inference; `[model]` → computed; web specs **[H]/[M]/[TPS]/[mkt]**.

## 1. The Application (real-grounded)

Full sourced survey: [[power-electronics/traction-inverter/segment-low-cost-city-car-inverters]].

| Vehicle | Power | Bus | Device (class) | Source |
|---------|------:|----:|----------------|--------|
| **Wuling Mini EV** | 20–30 kW | **~96 V** | **LV Si MOSFET** *(inferred)* | [164][M/TPS] |
| Dacia Spring | ~48 kW | ~240 V | Si IGBT *(inferred)* | [165][M] |
| BYD Seagull | 55 kW | 403 V | Si IGBT *(inferred)* | [165][M] |
| Citroën Ami (L6e) | 6 kW | 48 V | LV MOSFET | [165][M] |

The class is **tri-modal in voltage** (48 → 96 → 240 → 403 V), and **SiC is absent from all of it** [165]. Device follows voltage: **<~200 V → LV Si MOSFET; >~200 V → Si IGBT** [165].

## 2. The Workflow — Cost Structure, Not Efficiency  `[model]`

Design a 30 kW inverter twice — **96 V LV-MOSFET** vs a hypothetical **350 V Si-IGBT** — and read what low voltage buys and costs:

| | 96 V LV-MOSFET | 350 V Si-IGBT |
|--|:---:|:---:|
| phase current (rms) | **278 A** | 76 A |
| conduction / switching loss | 233 / 54 W | 196 / 132 W |
| busbar+connector I²R | **93 W** | 7 W |
| inverter efficiency | **98.75%** | 98.90% |

**The surprise:** switch efficiency is **competitive** — LV MOSFET `Rds` is tiny, so despite 3.6× current the semiconductors are fine (even lower switching loss). **The 3.6× current penalty lands on interconnect (13× I²R) and DC-link ripple, not the switches** [model]. Low voltage does **not** cost efficiency here; it costs **power density and current-handling** (busbar, connectors, cap).

## 3. Why Low Voltage Is the Cost Lever (structural)

- **Device:** at <~200 V, low-voltage Si MOSFETs are the cheapest per kW and beat IGBTs (no `Vce0` knee); >200 V forces IGBT or costly SiC [165]. **Voltage picks the device class.**
- **Isolation/safety:** 96 V relaxes creepage/clearance, shrinks isolated gate-drive + bias scope, and cuts HV-safety content vs 400 V (though 96 V > 60 V DC is still ISO 6469 voltage-class B, [[power-electronics/traction-inverter/standards-and-compliance]] §2).
- **Relative device $/kW** (ordinal, **not a quote**): LV Si MOSFET 1.0× < 650 V Si IGBT ~1.5–2× < 650 V SiC ~3–4× [T][165].
- **Integration:** "3-in-1" motor+inverter+reducer, minimal sensing/redundancy — cost moves the OEM makes [164][M].

## 4. New Knowledge  `[model]`

1. **Low voltage is a *cost* lever, not an *efficiency* lever — and it doesn't cost switch efficiency.** The intuitive "cheap car = worse efficiency" is wrong at the semiconductor level: a 96 V LV-MOSFET inverter is ~as efficient as a 350 V IGBT. The real trade is **power density + interconnect burden** (278 A vs 76 A), plus the cost/safety saving from low voltage. This inverts the premium-car logic where **high** voltage (800 V) is chosen for efficiency.
2. **The cheapest EV inverters are the mirror image of the premium ones on the voltage axis** — microcars go *low* (cost), hypercars/trucks go *high* (efficiency/charge/density). Same device physics, opposite optimum, set entirely by the objective.
3. **Where the design data runs out.** This is the example where the vault + web could **not** confirm the device or price — a hard boundary of "design by RAG": below a certain market/price tier, teardown data simply doesn't exist, and the honest output is a *structural argument*, not numbers.

## 5. Report — Compromises

- **Cost bought with density + current-handling:** 3.6× current → heavy busbar, big DC-link ripple, thermal spreading of huge current — the LV penalty, paid in bulk not efficiency.
- **LV Si MOSFET over IGBT/SiC:** cheapest device at 96 V; SiC's $/A never pays at cost-first, low power [165].
- **Minimal everything:** simplest cooling (air on the low-power stock unit — *unverified* [164]), least sensing, no functional-safety redundancy — the per-unit-cost objective at >1 M units/yr [164].
- **Process contrast:** family car optimized η at corners; truck optimized ΔTj over a mission; performance optimized volume + `Zth` burst; **this one starts from a cost target and strips** — and its dominant variable (bus voltage) is chosen *opposite* to the premium designs. Four objectives, four different first moves (see [[ai-agents/design-by-doing-observed-workflow]]).

## Red Team

**Steelman against:** The load-bearing claim — Wuling uses LV MOSFETs — is **unconfirmed inference**, and the whole "voltage is the cost lever" narrative is built on one confirmed fact (the ~96 V pack, itself from a battery-vendor blog with an internal 83-vs-96-vs-115 V inconsistency [164]). The efficiency comparison uses invented device params `[T]`; the "cost structure" is an ordinal with **no sourced $** at all. A skeptic could say this example is 20% data and 80% plausible story.

**How it could be false:**
1. **Device unconfirmed:** if Wuling actually uses a low-voltage *IGBT* or an integrated ASIC, finding #1's efficiency detail shifts (though the voltage-picks-device principle still holds) [164].
2. **Efficiency numbers are param-driven** `[T]`: the LV-MOSFET `Rds`=1 mΩ (paralleled) and IGBT `Vce0` are class estimates; a different set could flip the 98.75 vs 98.90 ordering.
3. **Cost is unquantified:** the relative 1.0/1.5–2/3–4× ranking is general-knowledge ordinal, not a quote; real BOM cost could differ and moves with SiC pricing [29][165].
4. **Interconnect `Rint`=0.4 mΩ is assumed;** the 93 W LV penalty scales directly with it.

**What would change my mind:** an actual Wuling-class inverter teardown naming the die + a should-cost BOM; a measured efficiency map at 96 V/278 A; a datasheet LV-MOSFET `Rds` at the real die count.

**Residual doubt:** The *principle* — objective picks bus voltage, voltage picks device class, and at low power/cost the LV-MOSFET's penalty is density/interconnect not efficiency — is sound device physics and matches the (confirmed-low) Wuling voltage. The *specific* efficiency numbers and cost ordering are a lightly-sourced hypothesis, and this is the example where the data honestly ran out — which is itself the finding.

---

> **References:** [[citations]] · model: `worked-designs/microcar-96v-mosfet/`

← [[power-electronics/traction-inverter/worked-example-performance-800v-sic]] | [[power-electronics/traction-inverter/design-tradeoffs]] | [[power-electronics/traction-inverter/worked-example-family-car-400v-sic]] →
