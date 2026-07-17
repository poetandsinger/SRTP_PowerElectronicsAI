---
title: Control Schemes
type: topic
field: power-electronics
created: 2026-07-07
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [power-electronics, foc, dtc, mpc, sliding-mode, sensorless, review]
---

## Overview

The traction inverter's control architecture determines torque accuracy, efficiency, NVH (noise, vibration, harshness), and functional safety compliance. This note catalogues the control schemes used in production automotive traction inverters: field-oriented control (FOC), direct torque control (DTC), modulation strategies (SPWM, SVPWM, DPWM), overmodulation, sensorless control, and automotive-specific requirements.

Theory drawn from established textbooks (Bose, Vas, Kazmierkowski, Mohan) [47][48][49][50] and verified against IEEE literature where possible.

---

## 1. Control Architecture Overview

### 1.1 Cascaded Control Structure

Automotive traction inverters universally use a **cascaded (nested) control architecture**:

```
  ω_ref ──→ ┌──────────┐  Te_ref ──→ ┌────────────┐  idq_ref ──→ ┌────────────┐  vdq_ref ──→ ┌──────────┐
            │  SPEED    │             │  TORQUE/    │              │  CURRENT       │              │  PWM +    │  → Motor
            │  CONTROL  │             │  MTPA/      │              │  CONTROL     │              │  INVERTER │
  ω_act ←── │  (PI)     │  idq_act ←─ │  FLUX-WEAK  │  idq_act ←─ │  (PI/PR)     │   S1–S6 ←── │  MODULATOR│
            └──────────┘              └────────────┘              └────────────┘              └──────────┘
```

**Layers (outer to inner):**

1. **Speed control loop** (outermost): Regulates motor speed to driver demand. Bandwidth: 10–50 Hz.
2. **Torque/flux control:** Converts torque demand to current references (id_ref, iq_ref) via MTPA, MTPV, or field-weakening lookup tables.
3. **Current control loop** (innermost): Regulates dq-axis currents. Bandwidth: 500–2000 Hz (10–20× PWM frequency). This is the fastest electrical loop.
4. **Modulation:** Converts voltage references to gate signals via PWM.

### 1.2 Sampling and Update Timing

- **Asymmetric PWM:** Current sampled at PWM peak (center-aligned) → computation → duty cycle updated at next PWM valley. Update latency = 1 PWM cycle.
- **Symmetric PWM (double-update):** Sampling and update at both PWM peak and valley → effective control frequency = 2 × fPWM. This doubles the current loop bandwidth without increasing switching losses.
- **Oversampling:** Multiple ADC samples per PWM cycle → digital filtering to remove switching ripple without analog anti-aliasing filters.

### 1.3 Coordinate Transforms

The fundamental mathematical framework for AC machine control:

**Clarke Transform (abc → αβ, amplitude-invariant):**
```
[Vα]    2  [1   -1/2   -1/2 ] [Va]
[Vβ] =  ─  [0   √3/2  -√3/2] [Vb]
        3                       [Vc]
```

**Park Transform (αβ → dq, rotating reference frame):**
```
[Vd]    [ cos(θ)   sin(θ)] [Vα]
[Vq] =  [-sin(θ)   cos(θ)] [Vβ]
```

Where θ is the rotor electrical angle. The d-axis is aligned with the rotor flux for synchronous machines (PMSM, IPMSM), or the rotor flux vector for induction machines.

---

## 2. Field-Oriented Control (FOC)

> **Production dominance: Nearly 100% of automotive traction inverters.** FOC is the industry-standard control scheme for AC drives. No production BEV uses scalar (V/f) control for traction.

### 2.1 Principle

FOC decouples torque and flux control by transforming stator currents into the rotor's rotating reference frame:

- **d-axis current (id):** Controls the rotor flux. For PMSM, id < 0 (negative) weakens the permanent magnet flux (field weakening).
- **q-axis current (iq):** Controls the electromagnetic torque. Torque ∝ iq × (λPM + (Ld - Lq)id) for IPMSM.

### 2.2 Current Regulators

**PI Controllers in Synchronous Frame:**

The PMSM electrical dynamics in the dq-frame (with decoupling):

```
vd = Rs·id + Ld·(did/dt) − ωe·Lq·iq          (1)
vq = Rs·iq + Lq·(diq/dt) + ωe·(Ld·id + λPM)  (2)
```

The cross-coupling terms (ωe·Lq·iq, ωe·Ld·id) must be decoupled for independent d and q control. The standard approach:

```
vd* = Kp·(id* − id) + Ki·∫(id* − id)dt − ωe·Lq·iq   (decoupling)
vq* = Kp·(iq* − iq) + Ki·∫(iq* − iq)dt + ωe·(Ld·id + λPM)   (decoupling + back-EMF feedforward)
```

**PI Tuning (Internal Model Control / Pole-Zero Cancellation):**
- Desired bandwidth: ωc = 500–2000 rad/s (80–320 Hz)
- Kp = ωc × Ld (or Lq) → directly sets the current loop bandwidth
- Ki = ωc × Rs → cancels the electrical pole
- For automotive: typically Kp tuned for ωc ≈ 2π × 300 Hz for 10 kHz PWM with double-update

**Complex Vector PI:** An alternative that handles cross-coupling inherently via complex-valued transfer functions. Used in some high-performance drives but less common in automotive due to computational overhead vs. well-decoupled PI.

### 2.3 Maximum Torque Per Ampere (MTPA)

For IPMSM (Lq > Ld — salient rotor), maximum torque for a given stator current occurs when the current vector angle is optimized:

```
Te = (3/2)·P/2·[λPM·iq + (Ld−Lq)·id·iq]  →  includes reluctance torque

Optimal current angle:  θMTPA = sin⁻¹[ (−λPM + √(λPM² + 8(Lq−Ld)²Is²)) / (4(Lq−Ld)·Is) ]
```

**Implementation in automotive:**
- **Lookup table (LUT):** Precomputed id*(Te, ω) and iq*(Te, ω) tables from dynamometer characterization. Interpolated in real-time. **This is the most common production method.**
- **Online MTPA tracking:** Extremum-seeking or signal injection to find optimal angle. Zuo et al. (2024) propose a dual-control exploration/exploitation method via recursive least squares [45].
- **Analytical curve-fit:** Polynomial approximation of MTPA trajectory. Compromise between LUT memory and online computation.

### 2.4 Field Weakening (Flux Weakening)

When motor back-EMF reaches inverter voltage limit (ωe × λPM ≈ Vdc/√3), torque capability drops. Field weakening injects negative id to reduce net flux:

```
Voltage constraint:  vd² + vq² ≤ Vmax²  where Vmax = Vdc/√3 (linear) or Vdc·(2/π) (overmodulation)

id* = (λPM/Ld)·[(ωbase/ωe) − 1]  →  (ideal, ignoring resistance)
```

**Production approaches:**
- **Voltage margin control:** PI regulator on voltage headroom (Vmax − |Vdq|) → generates negative id* reference. Simple and robust.
- **Lookup table:** Precomputed id*(Te, ω, Vdc) from motor characterization. Highest accuracy.
- **Analytical (model-based):** Direct computation from motor parameters. Sensitive to parameter errors at high speed.

**Deep field weakening (ωe >> ωbase):** motor enters constant-power region where id approaches the characteristic current Ichar = λPM/Ld. For IPMSM with high saliency (Lq/Ld > 2), the constant-power speed range can exceed 3:1.

---

## 3. Direct Torque Control (DTC)

> **Not used in automotive traction.** DTC dominates industrial VFDs (ABB ACS800/ACS880) but has not been adopted for EV traction. Documented for completeness.

### 3.1 Principle

DTC directly controls torque and stator flux magnitude using hysteresis comparators and an optimal switching table — no current loops, no coordinate transforms, no PI tuning:

1. Estimate stator flux (λs) and torque (Te) from measured voltages and currents
2. Compare to references via hysteresis (±ΔTe, ±Δλs)
3. Select next switching state from a look-up table based on flux sector and hysteresis outputs

### 3.2 Why DTC Isn't Used in Automotive

| Issue | FOC | DTC |
|-------|-----|-----|
| Torque ripple | Low (PWM-controlled) | High (hysteresis bands → variable switching frequency) |
| Switching frequency | Fixed (predictable losses, EMI) | Variable (complicates thermal design, EMI filter) |
| Current control | Explicit (overcurrent protection inherent) | Implicit (requires separate current limiting) |
| Low-speed performance | Good (sensorless back-EMF + HF injection) | Poor (stator flux estimation fails at low speed) |
| Acoustic noise | Predictable (fixed PWM frequency) | Variable-frequency switching causes tonal noise |
| Parameter sensitivity | Moderate | Low (but at cost of other issues) |

**Verdict:** The automotive requirement for smooth torque (NVH), predictable EMI, and low-speed sensorless control makes FOC the universal choice. DTC's variable switching frequency is fundamentally incompatible with automotive EMI requirements (CISPR 25).

---

## 4. Modulation Strategies

### 4.1 Carrier-Based Sinusoidal PWM (SPWM)

Reference sine waves (va*, vb*, vc*) compared to a high-frequency triangular carrier:

- Phase voltage: va(t) = MI × (Vdc/2) × sin(ωt) where MI = Vref/(Vdc/2)
- **Maximum linear MI:** 1.0 (phase voltage peak = Vdc/2)
- **Line-line RMS (max linear):** Vdc × √3/(2√2) ≈ 0.612 × Vdc
- **THD:** Poor at low MI, improving near MI=1.0

### 4.2 Space Vector PWM (SVPWM)

> **The dominant modulation in automotive traction inverters.**

SVPWM synthesises the reference voltage vector by time-averaging adjacent active vectors and zero vectors within each switching period Ts:

```
Vref·Ts = Vk·Tk + Vk+1·Tk+1 + V0·T0

where Tk + Tk+1 + T0 = Ts (half period)
```

**SVPWM is equivalent to SPWM with third-harmonic injection (1/6 of fundamental amplitude).** This boosts the linear modulation range by 15.5%:

- **Maximum linear MI (SVPWM):** 2/√3 ≈ 1.155 (15.5% higher than SPWM)
- **Line-line RMS (max linear SVPWM):** Vdc/√2 ≈ 0.707 × Vdc

**Switching sequence optimization:**
- **Symmetrical 7-segment:** Each half-period uses V0 → Vk → Vk+1 → V7 → Vk+1 → Vk → V0. Minimizes harmonic distortion. Most common in automotive.
- **Symmetrical 5-segment:** Drops one zero vector. Reduces switching events by 1/3 but increases THD at high MI.

### 4.3 Discontinuous PWM (DPWM)

Clamps one phase to the DC rail for 60° or 120° of the fundamental period by dropping switching in that phase. Reduces switching losses by ~33%:

| DPWM Variant | Clamping Pattern | Switching Loss Reduction | Best For |
|-------------|-----------------|------------------------|----------|
| DPWM0 | Clamp at Vdc (top) | ~33% | Low MI (startup) |
| DPWM1 | Clamp at peak current | ~33% | General purpose, reduces conduction losses |
| DPWM2 | Clamp at Vdc/2 | ~33% | High MI, lower THD than DPWM1 |
| DPWM3 | 30° clamp | ~33% | Compromise, commonly referenced |
| GDPWM (Generalized) | Adaptive clamp angle | Variable | Optimized for instantaneous power factor |

**Automotive use:** DPWM1 is used at high speed/high load to reduce switching losses and increase available voltage (through overmodulation). At light load (<25% rated torque), switching losses are already low, so SVPWM is preferred for better THD.

### 4.4 Overmodulation

When the reference vector magnitude exceeds the hexagon boundary, the inverter enters overmodulation:

| Region | MI Range | Operation | Effect |
|--------|----------|-----------|--------|
| Linear | 0 → 0.907 | Normal SVPWM | Sinusoidal output, low THD |
| Overmodulation I | 0.907 → 0.952 | Reference clipped at hexagon boundary | Lower-order harmonics (5th, 7th) appear |
| Overmodulation II | 0.952 → 1.0 | Transition to six-step | Progressive loss of PWM control |
| Six-step | MI = 1.0 (max) | Square-wave phase voltage | No PWM, full DC-link utilization |

**Maximum fundamental line-line voltage (six-step):** VLL1 = (2/π) × √3 × Vdc ≈ 1.103 × Vdc (peak) = 0.780 × Vdc (RMS)

**Automotive use:** Overmodulation is used during:
- Motor start from standstill (high torque, low speed → high current, limited voltage)
- High-speed passing maneuvers (field weakening + overmodulation combined)
- Transient acceleration where voltage headroom is temporarily sacrificed for torque response

---

## 5. Sensorless Control

Eliminating the rotor position sensor (resolver/encoder) reduces cost, packaging volume, and failure modes. However, automotive traction universally uses position sensors for critical safety/reliability reasons.

### 5.1 Position Sensor Technologies (Production)

| Sensor | Principle | Resolution | Accuracy | Cost | Key OEM |
|--------|-----------|-----------|----------|------|---------|
| Resolver | Variable reluctance transformer | ~12-14-bit equivalent | ±0.1° | High | Tesla, most premium BEVs |
| Inductive encoder | Eddy current sensing | 12-16 bit | ±0.1–0.5° | Medium | Growing share |
| Hall-effect (3-element) | Magnetic field angle | 8-10 bit | ±1–2° | Low | Cost-sensitive designs |
| MR / GMR sensor | Magnetoresistive | 10-14 bit | ±0.5–1° | Medium | Some Japanese OEMs |

### 5.2 Sensorless Methods

**Back-EMF estimation (medium-high speed):**
- Estimate back-EMF from voltage model: e = V − Rs·I − L·(dI/dt)
- Derived rotor position: θ = atan2(eα, eβ) ± 90° (depending on machine type)
- **Limitation:** Fails below ~5% of rated speed (back-EMF too small for reliable estimation)

**High-frequency injection (zero-low speed):**
- Inject rotating or pulsating HF voltage (500–2000 Hz) superimposed on fundamental
- Demodulate HF current response to extract rotor saliency (Ld ≠ Lq)
- **Limitations:** Additional losses, acoustic noise, only works with salient machines (IPMSM, not SPMSM)

**In production:** Almost all EVs use resolvers despite their cost. Functional safety (ISO 26262 ASIL C/D) requires guaranteed rotor position knowledge — sensorless can fail silently at zero speed. However, sensorless methods are used as **backup observers** for fault detection: if estimated and measured positions diverge by >5–10°, a resolver fault is flagged.

---

## 6. Automotive-Specific Control Requirements

### 6.1 Torque Accuracy and Response

- **Torque accuracy:** ±5% of reference (or ±3 Nm, whichever larger) — ISO 26262 torque monitoring
- **Torque step response:** <50 ms from 0 → 90% of rated torque (typical for passenger BEVs)
- **Torque reversal (regeneration → motoring):** <100 ms, smooth transition without driveline shock

### 6.2 Derating and Thermal Protection

The inverter controller continuously monitors:
- **Junction temperature (Tj):** Estimated from NTC sensors in power module + thermal model
- **Motor winding temperature:** Estimated from resistance or thermistor
- **DC-link voltage:** Brownout detection, overvoltage from regeneration

**Derating strategy:**
- Tj > 150°C → reduce current limit linearly
- Tj > 175°C (SiC) / Tj > 150°C (IGBT) → immediate torque reduction to 0 within 100 ms
- Vdc < Vdc_min → enter limp-home mode (reduced torque, reduced speed)

### 6.3 Functional Safety (ISO 26262 ASIL C/D)

| Safety Goal | ASIL | Monitoring | Fault Reaction |
|-------------|------|-----------|---------------|
| Unintended acceleration | C/D | Torque estimate vs. reference | ASC (active short circuit) or freewheel within 100 ms |
| Loss of propulsion | B/C | Phase current, DC-link voltage | Limp-home mode, notify driver |
| Overvoltage protection | B | Vdc monitoring | Disable regeneration, engage brake chopper if present |
| Thermal runaway | C | Tj estimation, NTC sensors | Reduce torque to 0, shut down inverter |
| Position sensor failure | D | Resolver signal monitoring, sensorless backup observer | ASC, flag fault |

### 6.4 Active Short Circuit (ASC)

When a critical fault is detected (e.g., resolver failure, unintended torque), the safest state for a PMSM is to short all three phases:

- All low-side switches ON → motor windings shorted → back-EMF circulates current through windings → braking torque proportional to speed
- **ASC vs. freewheel:** ASC produces controlled braking torque (safe for highway). Freewheel (all switches OFF) allows back-EMF to pump DC-link voltage via body diodes → risk of overvoltage at high speed.
- **Trade-off:** ASC produces sustained braking torque (~0.1–0.3 pu) → driver must pull over. Acceptable for ASIL D fault.

---

## 7. Control Implementation in Production

### 7.1 Typical Microcontroller Platforms

| MCU Family | Supplier | Core | Key Features | OEM Examples |
|------------|----------|------|-------------|-------------|
| C2000 (TMS320F2838x) | TI | C28x + CLA | Dual-core, 16× ADC, resolver interface, FPU, TMU | Tesla Model 3 (early), many designs |
| Infineon AURIX TC3xx | Infineon | TriCore (3-core) | ASIL-D, 6× ADC, SENT, resolver, hardware security | VW MEB, modern EU OEMs |
| RH850 | Renesas | G3MH/G4MH | ASIL-D, motor control timer, resolver | Japanese OEMs |
| S32K3 / S32E | NXP | Arm Cortex-M7 / R52 | ASIL-D, motor control PWM, resolver | Chinese/South Korean OEMs |

[T] — MCU families from training knowledge; verify exact part numbers against teardown reports.

### 7.2 Control Loop Timing (Typical 150 kW SiC Inverter)

```
PWM frequency:        10–20 kHz
PWM period:           50–100 µs
Current loop update:  25–50 µs (double-update)
  - ADC sampling:      2–3 µs (6 channels: 3× phase current, Vdc, temperature, resolver)
  - Clarke/Park:       1–2 µs
  - PI current control: 2–3 µs
  - Decoupling + MTPA: 2–3 µs
  - SVPWM generation:  2–3 µs
  - Total CPU per update: ~10–15 µs at 200 MHz
Speed loop update:    1–5 ms (much slower outer loop)
```

---

## Control Strategies Comparison (FOC / DTC / MPC — 2025–2026 literature)

## 4. Control Strategies Comparison

### 4.1 Head-to-Head Comparison

| Metric | FOC (Field-Oriented Control) | DTC (Direct Torque Control) | MPC (Model Predictive Control) |
|--------|------|------|------|
| **Dynamic response** | Good | Good | Excellent (real-time optimization) |
| **Torque ripple** | Low | Higher | Low to moderate |
| **Steady-state precision** | High | Moderate | High |
| **Parameter sensitivity** | Moderate (sensitive to rotor flux) | Low (less dependent on motor params) | High (requires precise model) |
| **Computational load** | Moderate (PWM + PI loops) | Low (hysteresis + switching table) | High (optimization in real-time) |
| **Low-speed stability** | Good | Moderate | Good |
| **Implementation complexity** | Moderate | Low | High |
| **Efficiency** | High | Moderate-High | High |
| **Robustness** | Moderate | High | Moderate |
| **Switching frequency** | Fixed (deterministic) | Variable (hysteresis-based) | Variable (FCS-MPC) or Fixed (CCS-MPC) |
| **Industry adoption** | Dominant (~80-85% of production) | Moderate (~10-15%) | Growing (~5%, mainly research/high-end) |
| **Hardware requirement** | Standard MCU/DSP | Standard MCU/DSP | High-performance DSP/FPGA |

*Sources: Nature Scientific Reports 2025 - Table 2 comparison [Reliability: High (peer-reviewed)]; IEEE Conference Aug 2025 review [Reliability: Medium-High]; MDPI WEVJ Oct 2025 [Reliability: High]*

### 4.2 Detailed findings from 2025 Literature

**FOC (Field-Oriented Control):**
- Remains the industry workhorse for production EVs
- Decouples torque and flux control for good dynamic response
- Mature ecosystem: extensive literature, proven implementations, broad MCU support
- Requires position sensor or high-performance observer for sensorless operation

**DTC (Direct Torque Control):**
- Simplest implementation (no PWM modulator, no coordinate transforms)
- Less dependent on motor parameters (more robust)
- Higher torque ripple and variable switching frequency limit efficiency at light load
- Still used in some industrial drives but declining in automotive

**MPC (Model Predictive Control):**
- **FCS-MPC (Finite Control Set):** Less complex, directly selects inverter switching states; reduces inverter losses but has higher THD and lower robustness to parameter variations
- **CCS-MPC (Continuous Control Set):** Better performance but higher complexity, potentially limiting real-time implementation
- **Key 2025 result (Aalborg University, IEEE ITEC+EATS):** Adaptive switching-frequency MPCC achieved 91.17% system efficiency vs 87.69% for standard MPCC and fixed-frequency FOC
- **Multi-Vector MPC + LMC (IEEE Trans. IA, Oct 2025):** Low switching frequency with reduced inverter-motor system losses, outperforming MTPA+FOC
- **Limitation:** The main barrier to MPC adoption is computational complexity; new reduced-computation FCS-MPC variants (~40% faster) are emerging

**Sensorless Control:**
- Essential for cost reduction (eliminates resolver/encoder)
- Standard methods: back-EMF observers (MRAS, SMO) at medium/high speed; signal injection at zero/low speed
- Active research area: AI-enhanced observers (ANN, fuzzy logic) for improved low-speed performance
- Industry adoption: Many production inverters use sensorless FOC, typically with rotor position observer

### 4.3 Emerging AI-Enhanced Control (2025)

- **ANN-aided VSVPWM (IEEE Trans. IA, May 2025):** Artificial neural network assists virtual-space-vector PWM for 3-level NPC inverters; validated via Simulink/PLECS co-simulation; designed for TI C2000 and STM32
- **Deep Q-Network RL (ICIESC 2025):** RL-based inverter control achieving 1.8% THD (vs 3.9% PI, 2.4% MPC), 2.7% efficiency improvement, 35% faster dynamic response
- **LMC + Multi-Vector MPC (IEEE Trans. IA, Oct 2025):** AI-assisted loss minimization combined with MPC

---


## Red Team

**Steelman against:** This note catalogues control theory as established fact, but virtually every claim about what "automotive traction inverters universally use" comes from [T]-tagged training knowledge, not verified production teardowns or OEM documentation. Automotive OEMs treat their control architectures as proprietary — public knowledge is approximate. The specific PI tuning rules, MTPA LUT implementations, and overmodulation strategies used in production may differ materially from the textbook versions described here.

**How it could be false:**
1. **Production control is proprietary:** Tesla, BYD, and VW do not publish their FOC implementations. The claim that "nearly 100% of automotive traction inverters use FOC" is industry consensus (plausible) but not verifiable from public sources.
2. **DTC's non-use may be overstated:** ABB's DTC is used in some electric bus and commercial vehicle inverters (where NVH is less critical). The blanket "DTC isn't used in automotive" may be wrong for heavy-duty applications.
3. **MTPA implementation details are guesses:** The LUT-based MTPA description matches textbook implementations. Production implementations may use hybrid approaches (LUT + online trim) that aren't publicly documented.
4. **Sensorless as "backup only" may be outdated:** Some Chinese OEMs are reportedly shipping sensorless-capable inverters with resolver backup (opposite of the described pattern). Verification needed.
5. **MCU platform claims are [T]-tagged:** The specific part numbers and OEM mappings are from training knowledge — likely correct but unverified. Teardown reports (Munro, SystemPlus) would be more reliable sources.
6. **Timing numbers are idealized:** The "10-15 µs at 200 MHz" control loop timing assumes optimized assembly code. Production code (often model-generated from Simulink) may be 2-3× slower.

**What would change my mind:**
- A public teardown report (Munro, SystemPlus, UBS) documenting the actual control architecture, MCU, and current-loop timing of a production traction inverter.
- An OEM application note or SAE paper describing their specific FOC implementation (some exist — see Tesla's SAE papers on Model 3).
- Evidence that a production BEV uses DTC or another non-FOC scheme for main traction.

**Residual doubt:** The control theory is textbook-correct. The production implementation details are educated guesses. For an AI agent making control design decisions, the theory is sufficient for simulation — but the gap between "textbook FOC" and "Tesla's production FOC" may be significant for real-world performance prediction.

---
> **References:** [[citations]]

← [[power-electronics/traction-inverter/components]] | [[power-electronics/traction-inverter/control-how-to]] →
