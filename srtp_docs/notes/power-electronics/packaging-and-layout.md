---
title: "Packaging, Busbar & Layout"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, packaging, busbar, design, thermal, emi, reliability]
review_by: 2026-10-17
---

## What This Is

The physical build: module internals, the laminated busbar, gate/power-loop layout, creepage/clearance, and enclosure. These are where the `Lσ<15 nH`, thermal, and EMI targets are met or lost — the procedure-design treats them as budgets ([[procedure-design]] §8); this chapter is how you hit them.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge.

## 1. Power Module Internals (die → coolant)

Stack, top to bottom [103][104][25]:

| Layer | Function | Choice / note |
|-------|----------|---------------|
| SiC die | switch | 1200 V, paralleled for current |
| **Die attach** | die→substrate bond | **sintered silver (k 80–280)** for low Rth + high-temp; solder legacy [104][103] |
| Top interconnect | source/gate | Al wire-bond (legacy) → **Cu clip / ribbon** (lower R, better thermal, higher power-cycle life) [T][103] |
| DBC/AMB substrate | isolate + spread | Al₂O₃/AlN/Si₃N₄ ceramic; **AMB Si₃N₄** for thermal-cycle robustness [T] |
| Baseplate | spread to cooler | Cu / AlSiC; **direct/pin-fin** eliminates the TIM stage [103] |

Power-cycling lifetime is set by CTE-mismatch fatigue at these interfaces (wire-bond lift-off, solder/sinter cracking) — the AQG 324 wear-out metric (+20% Rth / +5% Vf) [88], [[protection-and-safety]] §7.

## 2. DC-Link Busbar — Meeting the `Lσ` Budget

- **Target `Lσ < 10–15 nH`** for SiC: overshoot `V=Lσ·di/dt`, ring `f=1/(2π√(Lσ·Coss))` [25], [[components]] §5. Reference designs hit **5.3 nH power loop / 6.7 nH module** [91].
- **Laminated busbar:** parallel Cu plates with a thin dielectric (**spacing <100 µm**) → field cancellation between opposing currents minimizes inductance [118]. The narrower the gap and wider the plates, the lower `Lσ` [118].
- **Minimize commutation-loop area** (DC-link cap ↔ module terminals): shortest, widest, most-overlapped path; place the cap directly over/against the module [118][41].
- Cap-integrated-into-module (Tesla-style) is the extreme case of loop minimization [37], [[components]] §5.

## 3. Gate-Loop & Power-Loop Layout (PCB)

- **Kelvin source** (separate gate-return from power-source): mandatory for SiC — keeps power-loop `di/dt` out of the gate loop, or switching speed collapses and false-turn-on margin vanishes [107], [[gate-driver-design]] §1, [[schematics]] §3.
- **Tight gate loop:** minimize gate-driver→gate→Kelvin-source area to cut loop inductance and ringing; place driver close to the module [107].
- **Separate power and signal grounds**, single-point HF bond; keep sense (current/NTC) routing away from the switching node [117], [[emi-emc-design]] §6.

## 4. Creepage & Clearance (HV isolation)

Set by working voltage, pollution degree, material group, altitude — per **IEC 60664 / IEC 61800-5-1** [86][113]:

| Barrier | 800 V system guidance |
|---------|-----------------------|
| Reinforced-isolation gate driver package | **~8 mm** typical; **~11.4 mm** for 800 V margin; up to ~14.5 mm extra-wide [113] |
| HV creepage (PCB, PD2) | scale from working voltage + pollution degree; add altitude derating (>2000 m) [86] |
| Working-voltage margin | reinforced ≥ ~1.4–2× convention `[T]` [86] |

Clearance = shortest air path; creepage = shortest surface path (worse with contamination/humidity → pollution degree). Slots/ribs in the housing extend creepage without growing the board [113].

## 5. Enclosure, Cooling Integration, Environment

- **Sealing:** IP67-class, HV interlock loop (HVIL), HV connectors with touch-safe/creepage-rated interfaces [86].
- **Cooling integration:** cold plate is structural — module bolts to it through the TIM (or is direct-cooled); coolant 65 °C WEG, ~10 L/min [99], [[thermal-design]] §4.
- **Environment:** −40 to +85 °C ambient, severe vibration/shock, salt — busbar/connector mechanical fatigue and TIM pump-out are lifetime risks [T], [[what-is-a-traction-inverter]] §7.

## Red Team

**Steelman against:** This chapter mixes well-sourced facts (busbar `Lσ` physics [118], creepage basis [113], module stack [103]) with `[T]` construction claims (Cu-clip vs wire-bond lifetime, AMB Si₃N₄ choice, IP/vibration specifics) that are general industry knowledge, not tied to a specific qualified design. The `Lσ<15 nH` and 5.3 nH numbers are real [91][25], but achieving them is a layout/measurement outcome a note cannot prove.

**How it could be false:**
1. **`[T]` packaging choices** (clip vs bond, substrate material, IP rating) are typical, not sourced to a specific module datasheet — verify against the chosen module.
2. **`Lσ` is a measured property**; "laminated busbar → <15 nH" is achievable but layout-dependent and must be extracted (Q3D/measurement), not assumed [118].
3. **Creepage ~8–11.4 mm** [113] is package-level guidance; the actual PCB creepage depends on the full pollution-degree/altitude/material-group calc, not a single number [86].
4. **Power-cycling lifetime** attribution to interfaces is qualitatively right but needs the module's own AQG 324 data for numbers [88].

**What would change my mind:** an extracted/measured `Lσ` for the actual busbar; the chosen module's construction and AQG 324 power-cycling datasheet; a full IEC 60664 creepage/clearance calc for the board.

**Residual doubt:** The physics and design targets are solid and sourced; the specific construction and dimensional numbers are typical values to replace with the chosen module's datasheet and a layout extraction.

---

> **References:** [[citations]]

← [[thermal-design]] | [[emi-emc-design]] | [[components]] →
