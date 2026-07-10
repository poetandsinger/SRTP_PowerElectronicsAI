---
title: Power Semiconductor Components
type: topic
field: ee
created: 2026-07-07
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [ee, mosfet, igbt, sic, gan, gate-driver, dc-link, review]
---

## Overview

The traction inverter's heart is its power semiconductor switches. This note catalogues the devices, modules, gate drivers, DC-link capacitors, current sensors, and thermal interfaces used in production automotive inverters. Data sourced from OEM teardowns (Munro & Associates, UBS Evidence Lab) [T], supplier market reports [29], and IEEE literature [44]. [T] tags mark training-knowledge entries not yet verified against live datasheets.

---

## 1. Power Semiconductor Devices

### 1.1 Silicon IGBT

The incumbent device for automotive traction. Despite SiC's rise, IGBT still powers the majority of 400V cost-sensitive BEVs and all HEV/PHEVs.

**Device physics (summary):**
- N-channel, conductivity-modulated bipolar device in a MOS-gate structure
- Forward voltage drop: VCE(sat) ≈ 1.5–2.5 V at rated current (higher than SiC at light load, competitive at full load)
- **Tail current during turn-off** — minority carrier recombination causes a current "tail," the dominant switching loss mechanism
- Short-circuit withstand time: ~10 µs (rugged, well-understood failure mode)

**Production Modules (Automotive):**

| Module Family    | Supplier   | Voltage  | Current  | Package           | Key OEM                       |     |
| ---------------- | ---------- | -------- | -------- | ----------------- | ----------------------------- | --- |
| HybridPACK Drive | Infineon   | 750V     | 400–820A | Pin-fin baseplate | VW MEB, Hyundai E-GMP (early) | [T] |
| VE-Trac Direct   | onsemi     | 750V     | 400–800A | Direct cooled     | VW, various                   | [T] |
| ACEPACK DRIVE    | STMicro    | 650–750V | 300–600A | Transfer molded   | Various EU OEMs               | [T] |
| J1-Series        | Mitsubishi | 650V     | 300–800A | Transfer molded   | Japanese OEMs                 | [T] |
| BYD IGBT Module  | BYD Semi   | 650V     | 200–600A | In-house package  | BYD (vertical integration)    | [T] |

**Who still uses IGBT (2025):**
- Nissan Leaf (all generations)
- Toyota Prius / Camry Hybrid / RAV4 Hybrid
- VW ID.3 / ID.4 (MEB entry trims)
- Most 400V compact Chinese BEVs (BYD Dolphin, Wuling Mini EV)
- All series-parallel HEV/PHEV powertrains (Toyota, Honda, Ford, Hyundai)

---

### 1.2 Silicon Carbide (SiC) MOSFET

The fastest-growing segment. Toyota's 2017 Model 3 was the watershed mass-production adoption. Yole Group [29]: automotive SiC market ~$2B (2024) → >$6B by 2029.

**Device physics (summary):**
- 3.26 eV bandgap (≈3× Si) → critical E-field ≈ 10× Si → much thinner drift region for same voltage rating
- Unipolar device — no tail current, purely capacitive turn-off → **50–70% switching loss reduction vs. Si IGBT**
- Rds(on) increases with temperature (positive temp coefficient) — naturally enables paralleling
- Short-circuit withstand: 3–5 µs (less rugged than IGBT — requires fast desat detection, typically <1 µs)

**Production Modules (Automotive SiC):**

| Module Family | Supplier | Voltage | Typical Rds(on) | Package | Key OEM |
|--------------|----------|---------|-----------------|---------|---------|
| Tesla Custom SiC Module | STMicro (primary) | 650V | ~3–5 mΩ total | Pin-fin, 24-die parallel | Tesla Model 3/Y/S/X | [T]
| Wolfspeed XM3 | Wolfspeed | 1200V | 3.5–8 mΩ | High-density power module | Lucid Air, premium EVs | [T]
| EliteSiC VE-Trac | onsemi | 900–1200V | 3.9–8 mΩ | Direct cooled | Various 800V platforms | [T]
| CoolSiC HybridPACK | Infineon | 1200V | 5–12 mΩ | Pin-fin baseplate | VW PPE, Mercedes EQS | [T]
| Rohm 4th-Gen SiC | Rohm | 750–1200V | Varies | Various | Japanese OEMs | [T]
| BYD SiC Module | BYD Semi | 1200V | Varies | In-house | BYD Seal, Han (premium) | [T]

**SiC Cost Trajectory:**
- 2017 (Tesla Model 3 launch): ~3–4× IGBT $/A
- 2021: ~2–3× IGBT $/A
- 2024: ~1.5–2.5× IGBT $/A (per Yole, Infineon investor presentations)
- 2027 projection: ~1.0–1.5× IGBT $/A (150mm → 200mm wafer transition)
- At price parity (~1× IGBT), SiC will dominate all voltage classes

**Key Failure Modes (SiC-specific):**
- **Gate oxide degradation** at high temperature and negative bias — threshold voltage (Vth) drifts over time
- **Body diode degradation** — bipolar degradation from stacking fault expansion during forward conduction of intrinsic body diode
- **Short-circuit ruggedness** — SiC MOSFETs fail faster than IGBTs (3–5 µs vs. 10 µs). Gate drivers must detect and turn off within 1–2 µs.

---

### 1.3 Gallium Nitride (GaN) HEMT

**Not used for traction as of 2026.** Primary automotive applications: on-board charger (OBC, 3.3–22 kW) and DC-DC converter (400V→12V).

| Parameter | 650V GaN HEMT | 1200V SiC MOSFET | Comparison |
|-----------|---------------|------------------|------------|
| Rds(on) × Qg (figure of merit) | ~5× better than SiC | Baseline | GaN superior for MHz switching |
| Current per die | 30–120A | 100–800A | SiC still leads for high power |
| Gate drive voltage | 5–6V (narrow window) | 15–20V | GaN harder to drive |
| Short-circuit withstand | <1 µs | 3–5 µs | GaN extremely fragile |
| Body diode | No (no p-n junction) | Yes (intrinsic) | GaN: zero reverse recovery — but third-quadrant conduction via gate drive |

**Toyota/Denso GaN traction prototype (sub-50 kW):** Demonstrated but not in production. GaN's current limitation means it will likely enter through dual-inverter architectures (one axle GaN for cruising, one axle SiC for acceleration) or 48V mild-hybrid traction [T].

Cacciato et al. (2022) [44] proposed an analytical loss-modelling approach for GaN HEMT based 3L-ANPC inverters, validating it against PSIM circuit simulations and preliminary experimental measurements with <3% error. The paper positions GaN as a promising candidate for traction inverters when paired with 3L-ANPC topologies that mitigate the 650V breakdown-voltage limitation; however, the experimental validation is at low power (200V, 3A). The claim that GaN is *not yet viable* for traction is a training-knowledge assessment, not a conclusion of [44].

---

## 2. Gate Drivers

The gate driver is the critical interface between the low-voltage control electronics and the high-voltage power switches. It must provide electrical isolation, fast switching, and comprehensive protection.

### 2.1 Functional Requirements

| Function | Requirement | Rationale |
|----------|------------|-----------|
| Galvanic isolation | ≥ 3.75 kV (basic), ≥ 6 kV (reinforced) | IEC 61800-5-1, functional safety |
| Gate current | ±4–15 A peak | Drive SiC MOSFET gate capacitance (Ciss ≈ 3–10 nF at 1200V) |
| Propagation delay | <100 ns | Minimize control loop latency |
| Desaturation (desat) detection | <1 µs (SiC), <3 µs (IGBT) | Short-circuit protection |
| Active Miller clamp | VGS pull-down during dv/dt | Prevent parasitic turn-on |
| Undervoltage lockout (UVLO) | VGS monitoring | Prevent thermal runaway from insufficient gate drive |
| Soft turn-off | Controlled di/dt at fault | Reduce voltage overshoot on overcurrent |

### 2.2 Common Automotive Gate Driver ICs

| Part Number | Supplier | Channels | Isolation                 | Peak Current        | SiC/IGBT | Key Features                          |     |
| ----------- | -------- | -------- | ------------------------- | ------------------- | -------- | ------------------------------------- | --- |
| UCC21750    | TI       | 1        | 5.7 kV capacitive         | ±10A                | SiC/IGBT | Desat, Miller clamp, ASC              |     |
| ISO5852S    | TI       | 1        | 5.7 kV capacitive         | ±2.5A (ext booster) | IGBT     | Desat, soft turn-off, ASC             |     |
| 1EDI3021AS  | Infineon | 1        | 8 kV coreless transformer | ±10A                | SiC      | Desat, Miller clamp, I2T protection   |     |
| NCD57000    | onsemi   | 1        | 5 kV capacitive           | ±6A                 | SiC/IGBT | Desat, Miller clamp                   |     |
| Si828x      | Skyworks | 1        | 5 kV                      | ±4A                 | SiC/IGBT | Desat, Miller clamp, DC-DC controller |     |

[T] — part numbers from training knowledge; verify against latest datasheets.

### 2.3 Isolated Power Supply

Each gate driver channel requires an isolated DC-DC supply (typically +15V / -5V for SiC, +15V / -8V for IGBT). Common approaches:

- **Push-pull transformer** with post-regulation
- **Integrated isolated DC-DC modules** (e.g., Murata MGJ2, RECOM RxxPxx)
- **Bootstrap supply** (for low-side only — not suitable for high-side at high duty cycles)

**Negative gate bias (-5V to -8V):** Essential for SiC MOSFETs to prevent parasitic turn-on during high dv/dt switching. SiC's low threshold voltage (Vth ≈ 2.5–4V) and high switching speeds make Miller-induced turn-on a real risk.

---

## 3. DC-Link Capacitor

The DC-link capacitor serves three functions:
1. **Ripple current filtering** — absorbs the high-frequency switching ripple from the inverter
2. **Voltage stabilization** — maintains stiff DC bus during load transients
3. **Commutation loop** — provides the low-inductance path for switching currents

### 3.1 Capacitor Technologies

| Type | Dielectric | Capacitance Density | Ripple Current Rating | Voltage Range | Use |
|------|-----------|---------------------|----------------------|---------------|-----|
| Film (metallized PP) | Polypropylene | 0.5–2 µF/mL | Excellent (ESR < 1 mΩ) | 450–1200 Vdc | **Primary DC-link capacitor** |
| Ceramic (MLCC) | X7R / C0G | 5–20 µF/mL | Moderate | 50–1000 Vdc | Snubber, high-frequency bypass |
| Aluminum electrolytic | Al₂O₃ | 50-200 µF/mL | Poor (ESR ≈ 10–100 mΩ) | 400–500 Vdc | Legacy designs, bulk storage |

**Film capacitors dominate automotive traction.** Polypropylene film capacitors offer:
- Extremely low ESR and ESL — critical for handling the RMS ripple current (typically 50–100 A RMS for a 150 kW inverter)
- Self-healing — metallized film clears internal faults without catastrophic failure
- No electrolyte dry-out — lifetime exceeds vehicle life (15+ years)
- High voltage capability — 500–1200 Vdc rated parts standard

**Typical DC-link capacitor bank (150 kW SiC inverter, 400V):** 400–600 µF total, constructed from 4–8 parallel film capacitors (e.g., 50–100 µF each, 500 Vdc rated).

### 3.2 Ripple Current

The DC-link capacitor must handle the inverter's switching-frequency ripple current, which depends on modulation index and load power factor:

- Worst-case RMS ripple current ≈ 0.5–0.65 × Irms (phase) at MI ≈ 0.6
- For a 150 kW, 400V inverter: Irms ≈ 300 A → capacitor ripple ≈ 150–200 A RMS
- Film capacitors typically rated 10–30 A RMS each → requires 6–10 parallel units

[T] — ripple current formulas from Kolar et al. analysis; verify with simulation.

---

## 4. Current Sensors

Motor phase current measurement is critical for field-oriented control (FOC). Requirements:

- **Bandwidth:** ≥ 50 kHz (to capture switching ripple for dead-time compensation)
- **Accuracy:** ±1–2% over -40°C to +125°C
- **Isolation:** galvanic isolation from HV bus (≥ 2.5 kV)
- **Latency:** < 5 µs (for real-time control loop at 10–20 kHz)

### 4.1 Sensor Technologies

| Type | Principle | Bandwidth | Accuracy | Cost | Automotive Use |
|------|-----------|-----------|----------|------|---------------|
| Hall-effect (open-loop) | Hall element + magnetic core | 50–200 kHz [T] | ±1–2% | Medium | Tesla Model 3 (3-phase) |
| Hall-effect (closed-loop) | Hall + compensation winding | 100–200 kHz [T] | ±0.5–1% | High | Premium vehicles |
| Shunt resistor + isolated ADC | I × R measurement | >500 kHz | ±0.5% | Low (BOM) | Many Chinese/OEM designs |
| Fluxgate | Magnetic saturation | 100–500 kHz [T] | ±0.1–0.5% | Very High | Precision applications |

**Shunt-based sensing is gaining share** because:
- Lower cost than Hall modules
- Higher bandwidth (excellent for SiC inverters with fast switching)
- Smaller footprint
- Challenges: power dissipation at high current (500 µΩ × 300A² = 45W — requires kelvin connection and thermal design)

### 4.2 Common Automotive Current Sensor ICs

| Part Number | Supplier | Type | Range | Isolation | Key Feature |
|------------|----------|------|-------|-----------|-------------|
| ACS725 / ACS37002 | Allegro | Hall (open-loop) | ±50–200A | 4.8 kV | Integrated conductor, automotive qualified |
| MLX91208 | Melexis | Hall (planar) | ±100–2000A | Via external conductor | IMC-Hall, programmable |
| TLI4971 | Infineon | Hall (open-loop) | ±25–120A | 5.3 kV | Digital output (SPI), temperature compensated |
| INA253 | TI | Shunt amplifier | ±150A (with shunt) | Via shunt + iso | Integrated shunt amp, 80V/V gain |

[T] — part numbers from training knowledge; verify against latest datasheets.

---

## 5. Busbars and Interconnects

The interconnection between DC-link capacitor and power module is performance-critical. Stray inductance in the commutation loop (Lσ) determines:

- Voltage overshoot at turn-off: Vovershoot = Lσ × di/dt
- Switching loss: higher Lσ → longer switching transition → higher Eon/Eoff
- EMI: ringing frequency f_ring = 1/(2π√(Lσ × Coss))

**Target:** Lσ < 10–15 nH for SiC inverters switching at >20 kA/µs. For IGBT switching at 3–5 kA/µs, 20–30 nH is acceptable.

**Design approaches:**
- Laminated busbar (wide, thin copper planes separated by thin insulator) — most common
- Power module integrated capacitor (direct die-attach to DC-link) — e.g., Tesla's approach with custom ST modules
- PCB with embedded planar capacitance — emerging technology

---

## 6. Thermal Management

### 6.1 Cooling Technologies

| Method | Power Density | Complexity | Key OEM |
|--------|--------------|------------|---------|
| Pin-fin heatsink (water-glycol) | 10–20 kW/L | Medium | Most OEMs (Infineon HybridPACK standard) |
| Direct jet impingement | 20–30 kW/L | High | Tesla (custom), Lucid Air |
| Two-phase / vapor chamber | 30–50 kW/L | Very High | Research stage |
| Oil immersion | 15–25 kW/L | Medium | Some Chinese OEMs |

### 6.2 Thermal Interface Materials (TIM)

The interface between power module baseplate and heatsink:

- **Thermal grease:** 1–3 W/m·K, simple application, pump-out risk
- **Phase-change material:** 3–5 W/m·K, improves with thermal cycling
- **Graphite pad:** 5–10 W/m·K, compressible, no pump-out
- **Sintered silver:** 200+ W/m·K at die-attach level, not for module-heatsink

---

> **References:** [[citations]]

## Red Team

**Steelman against:** The SiC market data [29] is paywalled and unverifiable. The Yole Group sells reports to SiC vendors — their forecasts have systematic upward bias. The components note treats market forecasts as facts and training-knowledge [T] claims as industry consensus.

**How it could be false:**
1. **Yole market data ($2B→$6B):** Source [29] is unverifiable (paywalled, CloudFront-protected). Analyst forecasts systematically over-estimate growth — they sell to the companies they're forecasting. Actual automotive SiC revenue may be 30–50% lower.
2. **GaN viability:** The note says GaN is "not yet viable" but cites Cacciato et al. (2022) [44] which positions GaN as promising with 3L-ANPC. The limitation is acknowledged (low-power experiments) but the "not viable" framing undersells active research. See [[citations]] [44] for the paper's actual position.
3. **Production vehicle examples (Tesla Model 3, Hyundai E-GMP, etc.):** These are based on public teardowns and press reports — not primary engineering data. The actual device specifications (current rating, Rds(on), switching frequency) in production vehicles are proprietary.
4. **OEM teardowns [T]:** Munro and UBS teardowns are proprietary reports. Claims derived from them ("Toyota's 2017 Model 3 was the watershed mass-production adoption") are second-hand and unverifiable.
5. **Thermal interface material specs:** The TIM conductivity ranges (3–5 W/m·K for phase-change, 5–10 for graphite) are unsourced training knowledge. These values vary significantly by manufacturer and grade.

**What would change my mind:**
- Public quarterly revenue data from Wolfspeed/onsemi/STMicro breaking out automotive SiC revenue.
- A post-2024 peer-reviewed review of GaN in traction applications.
- Access to the actual Munro/UBS teardown reports (proprietary — unlikely).

**Residual doubt:** The components note is the most vulnerable to motivated-source bias. Supplier market reports and OEM teardowns are explicitly designed to promote specific technologies (SiC) and companies. The note acknowledges this with [T] tags but doesn't adjust confidence levels accordingly.

← [[ee/traction-inverter/circuit-topologies]] | [[ee/traction-inverter/control-schemes]] →
