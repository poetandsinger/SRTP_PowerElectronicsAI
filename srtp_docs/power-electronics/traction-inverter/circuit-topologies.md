---
title: Circuit Topologies
type: topic
field: power-electronics
created: 2026-07-07
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [power-electronics, topology, two-level, three-level, multilevel, npc, t-type, anpc, review]
---

## Overview

A traction inverter converts DC battery voltage to three-phase AC for the traction motor. The core topology determines voltage levels, harmonic content, semiconductor stress, efficiency, and ultimately vehicle range. This note catalogues every topology observed in production or advanced research — circuit structure, switching states, voltage waveforms, and key design trade-offs.

---

## 1. Two-Level Voltage Source Inverter (2L-B6)

> **Production dominance: >95% of all BEV/PHEV traction inverters as of 2026.**

### Circuit Structure

The 2L-VSI (also called B6 bridge) consists of six controllable switches arranged as three half-bridge legs, each with an upper (high-side) and lower (low-side) switch:

```
        +─────────── Vdc ───────────+
        │           │               │
       ┌┴┐         ┌┴┐             ┌┴┐
    S1 ││       S3 ││           S5 ││   ← High-side switches
       └┬┘         └┬┘             └┬┘
        ├─── Va ────┤─── Vb ────────┤─── Vc     → Motor phases
       ┌┴┐         ┌┴┐             ┌┴┐
    S2 ││       S4 ││           S6 ││   ← Low-side switches
       └┬┘         └┬┘             └┬┘
        │           │               │
        +─────────── GND ───────────+
```

Each switch is a power semiconductor (IGBT or SiC MOSFET) with an anti-parallel freewheeling diode. The DC-link capacitor (Cdc) sits across the DC bus to filter ripple and provide a low-impedance path for switching currents.

### Switching States and Space Vectors

With the constraint that each leg's two switches are complementary (S1 = ¬S2), there are 2³ = **8 valid switching states**. Each state produces a distinct voltage space vector:

| State | S1 S3 S5 (High-side) | Va | Vb | Vc | Vector | Type |
|-------|----------------------|----|----|-----|--------|------|
| V₀ | 0 0 0 | 0 | 0 | 0 | (000) | Zero |
| V₁ | 1 0 0 | +Vdc | 0 | 0 | (100) | Active |
| V₂ | 1 1 0 | +Vdc | +Vdc | 0 | (110) | Active |
| V₃ | 0 1 0 | 0 | +Vdc | 0 | (010) | Active |
| V₄ | 0 1 1 | 0 | +Vdc | +Vdc | (011) | Active |
| V₅ | 0 0 1 | 0 | 0 | +Vdc | (001) | Active |
| V₆ | 1 0 1 | +Vdc | 0 | +Vdc | (101) | Active |
| V₇ | 1 1 1 | +Vdc | +Vdc | +Vdc | (111) | Zero |

These eight vectors form a hexagon in the α-β plane. The six active vectors (V₁–V₆) define six sectors, each spanning 60°. The two zero vectors (V₀, V₇) sit at the origin.

### Voltage Transfer Ratio

- **Linear modulation (SPWM):** max phase voltage = Vdc/2, max line-line voltage = √3 × Vdc/2 ≈ 0.866 × Vdc
- **SVPWM (with third-harmonic injection):** max line-line voltage = Vdc, modulation index MI ≤ 0.907
- **Overmodulation:** MI > 0.907 up to six-step operation where line-line voltage reaches (2/π) × Vdc ≈ 0.637 × Vdc (fundamental)

### Key Design Parameters

| Parameter | Typical Automotive Range |
|-----------|------------------------|
| DC-link voltage | 300–450 V (400V class), 600–900 V (800V class) |
| Switching frequency | 8–20 kHz (IGBT), 15–40 kHz (SiC MOSFET) |
| Dead time | 1–3 µs (IGBT), 0.2–1 µs (SiC) |
| DC-link capacitance | 300–800 µF for 100–200 kW |
| dv/dt at motor terminals | 5–15 kV/µs (IGBT), 15–50 kV/µs (SiC) |

### Limitations

- **Fixed two-level switching:** no ability to reduce effective switching frequency at light load without discontinuous PWM (DPWM)
- **High dv/dt stress on motor windings** — especially with SiC MOSFETs switching at >20 kV/µs. Requires motor insulation rated for inverter-duty (IEC 60034-18-41).
- **Bearing currents** — common-mode voltage transitions (Vdc/3, 2Vdc/3) drive capacitive coupling through motor bearings, causing EDM pitting. Mitigation: ceramic bearings, shaft grounding rings, common-mode chokes.
- **Harmonic distortion** — line-line voltage THD ranges from ~30% (at MI=0.5 with SVPWM) to ~5% (at MI=0.9)

---

## 2. Three-Level Neutral-Point-Clamped (3L-NPC)

### Circuit Structure

Each leg has four switches (S1–S4) and two clamping diodes (Dc1, Dc2) connected to the DC-link midpoint:

```
        +─── Vdc/2 ───+
        │              │
       ┌┴┐             │
    S1 ││─────┬────────┤
       └┬┘    │        │
        ├──┬──┴── Dc1 ─┤
        │  │           │
        │ ┌┴┐          ├── Va (phase output)
    S2  │ ││ S3        │
        │ └┬┘          │
        │  │           │
        ├──┴── Dc2 ────┤
       ┌┴┐             │
    S4 ││──────────────┤
       └┬┘             │
        │              │
        +─── -Vdc/2 ───+
             (Midpoint = NP)
```

The two DC-link capacitors (C1, C2) create a neutral point (NP). Each leg outputs three voltage levels: +Vdc/2, 0 (NP), -Vdc/2.

### Switching States Per Leg

| State | S1 | S2 | S3 | S4 | VxO | 
|-------|----|----|----|-----|-----|
| P (positive) | ON | ON | OFF | OFF | +Vdc/2 |
| O (zero) | OFF | ON | ON | OFF | 0 (NP) |
| N (negative) | OFF | OFF | ON | ON | -Vdc/2 |

S1 and S3 are complementary; S2 and S4 are complementary. **Critical constraint:** S1 and S4 must never conduct simultaneously (shoot-through across full DC-link).

### Total Switching States: 3³ = 27

These 27 states map to 19 distinct space vectors (12 small, 6 medium, 6 large, plus the zero vector). This provides finer voltage resolution than 2L.

### Neutral-Point Voltage Balancing

**This is the Achilles' heel of NPC.** The midpoint current (iNP) depends on switching state and load current. Without active balancing, the two capacitor voltages diverge, causing:

- Uneven voltage stress across switches
- Low-frequency ripple in output waveform
- DC offset in motor current

**Balancing methods:**
- **Carrier-based:** add zero-sequence offset proportional to voltage error
- **SVPWM-based:** redistribute dwell times between redundant small vectors (e.g., between [POO] and [ONN] for Sector 1)
- **Hardware:** front-end balancing circuit (adds cost)

### Advantages Over 2L

| Feature | 3L-NPC | 2L-B6 |
|---------|--------|-------|
| Voltage stress per switch | Vdc/2 | Vdc |
| Effective switching frequency | 2× fsw (apparent) | fsw |
| Line-line voltage THD | ~45% lower at same fsw | baseline |
| dv/dt | ~half | baseline |
| Output filter size | ~50–70% smaller | baseline |

### Automotive Status

**Not in production for BEV traction.** Used in railway traction (Siemens, Alstom) and industrial VFDs (ABB ACS800, Siemens Sinamics). The cost/complexity penalty (12 switches, 6 clamping diodes, NP balancing) has not been justified for automotive where SiC at 800V already addresses many 2L limitations.

---

## 3. Three-Level Active NPC (3L-ANPC)

### Circuit Structure

Replaces the two clamping diodes per leg with active switches (typically lower-rated MOSFETs):

```
        +─── Vdc/2 ───+
        │              │
       ┌┴┐             │
    S1 ││──┬───────────┤
       └┬┘ │           │
        │  │           │
        ├──┤ S5 ───────┤
        │  │           │
        │ ┌┴┐          ├── Va
        │ ││ S6        │
        │ └┬┘          │
        ├──┤───────────┤
       ┌┴┐ │           │
    S4 ││──┴───────────┤
       └┬┘             │
        │              │
        +─── -Vdc/2 ───+
```

Total: 6 switches per leg × 3 phases = **18 switches** + gate drivers.

### Key Advantage: Loss Distribution

In NPC, the inner switches (S2, S3) carry current continuously during the O-state, causing uneven thermal loading. ANPC adds redundant zero-state paths:

- **O+ state:** S2 and S5 conduct (bypasses S3)
- **O- state:** S3 and S6 conduct (bypasses S2)

This allows alternating between O+ and O- every switching cycle, equalizing losses across all four main switches. For SiC devices where conduction losses dominate at partial load, this is significant.

### Switching States Per Leg (6 valid states)

| State | S1 | S2 | S3 | S4 | S5 | S6 | VxO |
|-------|----|----|----|----|----|-----|-----|
| P | ON | ON | OFF | OFF | OFF | ON | +Vdc/2 |
| O+ | OFF | ON | OFF | OFF | ON | OFF | 0 |
| O- | OFF | OFF | ON | OFF | OFF | ON | 0 |
| N | OFF | OFF | ON | ON | ON | OFF | -Vdc/2 |

### Automotive Status

**Research stage.** Evaluated in Sachs & Neuburger (2025) [28] as a candidate for 2030 BEVs. No known production automotive application. The 18-switch count makes BOM cost and gate-drive complexity prohibitive at current semiconductor pricing.

---

## 4. Three-Level T-Type NPC (3L-TNPC)

### Circuit Structure

The most promising multilevel topology for automotive. Each leg uses four main switches (S1–S4) plus a bidirectional switch (S5 + S6 in anti-series) to the midpoint:

```
        +─── Vdc/2 ───+
        │              │
       ┌┴┐             │
    S1 ││──┬───────────┤
       └┬┘ │           │
        │  │           ├── Va
        │  ├── S5 ─────┤
        │  │  (bidirectional
        │  ├── S6 ─────┤  switch to NP)
        │  │           │
       ┌┴┐ │           │
    S4 ││──┴───────────┤
       └┬┘             │
        │              │
        +─── -Vdc/2 ───+
```

Only 12 switches total (4 per leg) vs. 18 for ANPC. The bidirectional switch (T-type) connects the output to the midpoint via S5/S6.

### Critical Design Trade-off

**Unlike NPC/ANPC, the outer switches (S1, S4) must block the FULL DC-link voltage** — they cannot share voltage like the series-connected switches in NPC. This means:
- 1200V SiC MOSFETs required for 800V systems (no 650V option)
- The T-type excels when DC-link voltage is ≤ half the switch rating (i.e., 650V devices on 400V bus, or 1200V devices on 600V bus)

### Switching States

| State | S1 | S4 | S5 | S6 | VxO |
|-------|----|----|----|-----|-----|
| P | ON | OFF | OFF | ON | +Vdc/2 |
| O | OFF | OFF | ON | ON | 0 |
| N | OFF | ON | ON | OFF | -Vdc/2 |

### Key Finding from Sachs & Neuburger (2025)

> **"The 3L-TNPC inverter, realised with only 30% additional SiC chip area, lowers drive-cycle drivetrain losses by 0.67 kWh/100 km relative to a SiC 2L-B6 baseline."** [28]

This is the headline result that makes TNPC the most cost-effective multilevel candidate for 2030 BEVs. The partial-load efficiency gain comes from:

- **Lower conduction losses at mid-modulation-index:** The O-state (midpoint) bypasses two switch voltage drops vs. the full DC-link path in 2L
- **Doubled apparent switching frequency:** Output sees 2× fsw, reducing motor harmonic losses
- **Reduced dv/dt:** Each transition is Vdc/2 instead of full Vdc

### Automotive Status

**Research stage.** TNPC is the primary multilevel topology being evaluated for next-gen 800V BEV traction inverters. No production vehicles yet, but the 0.67 kWh/100 km improvement (equivalent to ~3.5% range gain on a typical 75 kWh pack) provides a compelling business case if SiC costs continue declining.

---

## 5. Topology Comparison Matrix

| Parameter | 2L-B6 | 3L-NPC | 3L-ANPC | 3L-TNPC |
|-----------|-------|--------|---------|---------|
| Switches per phase | 2 | 4 | 6 | 4 |
| Total switches (3-phase) | 6 | 12 + 6 diodes | 18 | 12 |
| Clamping elements | None | 6 diodes | None (active) | Bidirectional switch |
| Voltage levels | 2 (Vdc, 0) | 3 (+½Vdc, 0, -½Vdc) | 3 | 3 |
| Max switch voltage | Vdc | Vdc/2 | Vdc/2 | Vdc |
| NP balancing needed | No | Yes (complex) | Yes (manageable) | Yes (manageable) |
| Partial-load efficiency | Baseline | Better | Better | Best |
| dv/dt at motor | Highest | ~½ of 2L | ~½ of 2L | ~½ of 2L |
| THD (same fsw) | Baseline | ~45% lower | ~45% lower | ~45% lower |
| Gate driver count | 6 | 12 | 18 | 12 |
| Production automotive | Yes (dominant) | No | No | No |
| Semiconductor cost (relative) | 1× | 2.3–2.8× | 3.0–3.8× | 1.8–2.2× |
| 2030 projection | Still dominant | Niche | Limited | Growing share |

---

## 6. Topologies NOT Suitable for Automotive

These are documented for completeness but have fundamental limitations for traction use:

| Topology | Key Limitation for Automotive |
|----------|-------------------------------|
| Flying Capacitor Multilevel (FCM) | Large capacitor bank required; capacitor pre-charge and balancing difficult at automotive power densities |
| Cascaded H-Bridge (CHB) | Requires isolated DC sources per cell — not compatible with single battery pack |
| Modular Multilevel Converter (MMC) | Designed for HVDC (hundreds of submodules); physically too large and heavy for vehicle integration |
| Current Source Inverter (CSI) | Requires large DC-link inductor (heavy, lossy); poor partial-load efficiency; voltage overshoot on inductive load |
| Matrix Converter | Voltage transfer ratio limited to 0.866; complex commutation control; no inherent fault isolation |
| Z-Source / Quasi-Z-Source | Shoot-through states add stress; extra passive components (L, C); limited OEM interest |

---

## 7. 2025–2026 Topology Adoption & Voltage Architecture (consolidated)

> Consolidated here from the former `topology-landscape-2025-2026` note (2026-07-17 audit). Dated data; reliability tags are the capturing sources'. Semiconductor detail lives in [[power-electronics/traction-inverter/components]] §7.

### 7.1 Topology Adoption Trend

| Topology | Application | Adoption trend | Note |
|----------|-------------|----------------|------|
| 2L-VSI (B6) | mainstream 400–800V | dominant (>80% share) | simplest, lowest cost |
| 3L-NPC | higher power, 800V+ | growing with SiC | better harmonics, lower dv/dt, higher part count |
| 3L-T-Type | medium power, OBC, some traction | niche, growing | lower switching loss in some ranges; GaN-compatible |
| Multilevel (CHB, FC) | heavy-duty >200 kW | emerging | best harmonics; GaN-favored; highest cost |
| CSI | specialized | research | reduced DC-link cap; not production-ready |

*Sources: Soomro et al., Results in Engineering (Jun 2025) [Medium]; Kynix 2026 [Medium].* The 3L/multilevel shift accelerates with SiC because higher fsw makes improved harmonics more valuable — consistent with [28] and §4 (3L-TNPC).

### 7.2 Voltage Architecture

- **400V:** dominant by volume; SiC and D-Mode GaN competing here.
- **800V:** mainstream in premium EVs; enables 200–350 kW charging. Q4 2025 ~14% of installs; Q1 2026 ~920k units (+21% YoY); forecast 25–30%+ by 2027.
- **>550V** is the fastest-growing class; ≤300V declining (−11% YoY).

*Sources: TrendForce Q1 2026 [High]; Compound Semiconductor News [Medium].*

---

## Key References

> **References:** [[citations]]

## Red Team

**Steelman against:** The Sachs & Neuburger (2025) [28] finding — 0.67 kWh/100 km savings with 30% SiC chip area for 3L-TNPC — is a single arXiv preprint, not a peer-reviewed paper. It's one simulation study with specific assumptions (WLTP drive cycle, specific device models). Extrapolating this to a universal claim about 3L topology superiority is premature.

**How it could be false:**
1. **Single-source dependency:** The entire 3L-TNPC case rests on one preprint [28]. No independent reproduction exists. Device models, loss parameters, and drive cycle assumptions may not generalize.
2. **Production viability unaddressed:** The paper evaluates electrical performance but does not examine manufacturing cost, reliability, or gate-drive complexity of 18-switch topologies. The "no known production application" caveat (line 204) is buried in one sentence.
3. **Topology comparison table unverified:** The claims about "SiC 2L: 97.5% peak, SiC 3L-NPC: 98.7%, SiC 3L-TNPC: 99.0%" are approximate ranges. Actual efficiencies depend on device selection, switching frequency, and modulation strategy — a 0.3% difference is within measurement uncertainty at these levels.
4. **Production dominance claim (">95% 2L-B6"):** Unsourced. This is training knowledge [T] or extrapolated from known OEM designs. No market survey is cited.

**What would change my mind:**
- Independent reproduction of the 0.67 kWh/100 km finding with different device models.
- A production 3L-TNPC traction inverter (expected ~2028 per [28]).
- A peer-reviewed version of [28] with reviewer scrutiny on the assumptions.

**Residual doubt:** The 3L-TNPC result is the most interesting finding in the note and also the least replicated. It's a preprint making a strong claim — exactly the kind of finding that needs adversarial review before being treated as evidence.

← [[power-electronics/traction-inverter/traction-inverter-index]] | [[power-electronics/traction-inverter/components]] →
