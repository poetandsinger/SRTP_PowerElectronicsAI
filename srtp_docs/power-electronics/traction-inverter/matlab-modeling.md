---
title: MATLAB/Simulink Modeling
type: topic
field: power-electronics
created: 2026-07-07
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [power-electronics, simulation, matlab-integration, review]
---

## Overview

This note documents modeling approaches for traction inverter systems in MATLAB/Simulink and Simscape Electrical — from basic averaged models to detailed switching models with thermal effects. Covers the blocks, parameters, simulation trade-offs, and integration patterns relevant to power electronics AI-assisted design. MATLAB is used as an external simulation backend, invoked from Python via the MATLAB Engine API [26][51].

---

## 1. Modeling Fidelity Levels

Traction inverter simulation spans four fidelity tiers, each trading accuracy for speed:

| Level | Name | Time Step | Suitable For | Simulation Speed (relative) |
|-------|------|-----------|-------------|----------------------------|
| L1 | Behavioral / Averaged | 50–500 µs | System-level, drive cycles, energy consumption | 10,000× real-time |
| L2 | Switching-Function | 1–10 µs | Harmonics analysis, control tuning | 1,000× real-time |
| L3 | Detailed Switching | 50–500 ns | Switching loss, EMI, dv/dt analysis | 10–100× real-time |
| L4 | Physics-Based (SPICE/FEM) | 1–50 ns | Device physics, parasitic extraction | 0.1–10× real-time |

**Automotive workflow:** L1 for drive-cycle efficiency → L2 for control design → L3 for loss verification and thermal → L4 only for device-level analysis (rarely in Simulink; usually PLECS, LTspice, or TCAD).

---

## 2. Level 1: Averaged Model (Behavioral)

### 2.1 Approach

The inverter is modeled as a **controlled three-phase voltage source** — no switching events, no PWM. The output voltage is continuous and equal to the reference voltage (ideal gain):

```
Va = Vdc × da   where da = duty cycle of phase A (0 to 1)
Vb = Vdc × db
Vc = Vdc × dc
```

DC-side current is computed from power balance: Idc = (Va·Ia + Vb·Ib + Vc·Ic) / Vdc

### 2.2 Simulink Implementation

**Blocks used (Simscape Electrical / Specialized Power Systems):**
- `Three-Phase Programmable Voltage Source` — simplest approach
- `Controlled Voltage Source` (3×) + `Three-Phase V-I Measurement` — more flexible
- Custom masked subsystem with algebraic Idc computation

**Key parameters:**
- DC-link voltage: Vdc = 400 V (or 800 V for 800V-class)
- Output frequency: 0–400 Hz (typical PMSM — 8-pole, 0–6000 rpm)
- Voltage magnitude: |Vdq| = √(vd² + vq²), limited to Vdc/√3 (linear) or up to Vdc·(2/π) (overmodulation)

### 2.3 Efficiency Modeling

Add conduction and switching losses via lookup tables or analytical models:

```
P_loss = P_cond(Idc, Tj) + P_sw(Idc, Vdc, fsw, Tj)

where:
  P_cond = Rds(on)(Tj) × Irms²   or   VCE(sat)(Tj) × Iavg + R_on × Irms²
  P_sw   = (Eon + Eoff)(Idc, Vdc, Tj) × fsw
```

**Data sources for loss parameters:**
- Manufacturer datasheets (Eon/Eoff vs. Id curves at multiple Tj and Vdc points) [T]
- PLECS thermal descriptions (XML) exported from manufacturer
- Double-pulse test characterization data

**Sachs & Neuburger (2025) [28] methodology:** Inverter-motor co-simulation with detailed loss maps derived from device datasheets, validated against dynamometer measurements. Drive-cycle losses computed by integrating instantaneous loss over WLTP velocity profile.

### 2.4 Use Cases

- Drive-cycle energy consumption (WLTP, EPA, CLTC)
- System-level trade studies (topology comparison, voltage class selection)
- Control algorithm development (outer loops: speed, torque, field weakening)
- Thermal management sizing (steady-state and transient)

---

## 3. Level 2: Switching-Function Model

### 3.1 Approach

The inverter is modeled with ideal switches — switching events occur but switching transients (dv/dt, di/dt) are instantaneous. Uses the switching function S(t) ∈ {0, 1} per phase:

```
Va(t) = Vdc × Sa(t)  where Sa(t) is the PWM-generated switching function
```

### 3.2 Simulink Implementation

**Blocks used:**
- `Universal Bridge` (Simscape / Specialized Power Systems) — configure as "IGBT/Diode" or "MOSFET/Diode" with ideal switching
- `PWM Generator (2-Level)` or `SVPWM Generator (2-Level)` — generates six gate pulses from vdq* references
- `Three-Phase V-I Measurement` — voltage and current sensing

**Key PWM Generator parameters:**

| Parameter | Typical Value | Notes |
|-----------|-------------|-------|
| Carrier frequency | 10,000–20,000 Hz | IGBT: 8-10 kHz, SiC: 15-20 kHz |
| Sample time | 1/(fsw × 100) or -1 (inherited) | At least 100× carrier for clean waveform |
| Modulation index range | 0–1.155 | 1.155 = 2/√3 (SVPWM max linear) |
| Dead time | 0–3 µs | 1–2 µs IGBT, 0.2–0.5 µs SiC |
| PWM mode | Symmetrical (center-aligned) | Standard for motor drives |

### 3.3 Custom SVPWM Implementation

For research/flexibility beyond the built-in blocks, a custom SVPWM generator in a MATLAB Function block:

```
Inputs:  Vα*, Vβ*, Vdc, Ts (switching period)
Outputs: Ta, Tb, Tc (duty cycles, 0–1)

Algorithm:
1. Compute reference vector: |Vref| = √(Vα² + Vβ²),  θ = atan2(Vβ, Vα)
2. Determine sector (1–6) from θ
3. Compute dwell times T1, T2, T0 from |Vref| × Ts / Vdc
4. Assign to phase duty cycles per sector (7-segment sequence)
5. Apply overmodulation clamping if T1+T2 > Ts
```

### 3.4 Use Cases

- Harmonic analysis (line-line voltage THD, motor current THD)
- Control loop tuning (PI current controller bandwidth)
- DC-link capacitor ripple current analysis
- EMI filter design (conducted emissions prediction)

---

## 4. Level 3: Detailed Switching Model

### 4.1 Approach

Each semiconductor switch is modeled with finite switching times, on-state resistance/voltage drop, and anti-parallel diode with reverse recovery. Switching transients produce realistic dv/dt, di/dt, and switching losses.

### 4.2 Simulink Implementation (Simscape Electrical)

**Blocks used:**
- `N-Channel IGBT` or `N-Channel MOSFET` (Simscape Electrical → Semiconductors & Converters)
- Configure with key device parameters
- Add `Diode` blocks in anti-parallel

**Key MOSFET/IGBT block parameters:**

| Parameter | SiC MOSFET (1200V) | Si IGBT (750V) | Source |
|-----------|-------------------|----------------|--------|
| Rds(on) / Vf | 3–12 mΩ | VCE(sat) 1.5–2.5 V | Datasheet |
| Internal diode Rs | 3–8 mΩ | N/A (separate diode) | Datasheet |
| Junction capacitance | Ciss, Coss, Crss | Cies, Coes, Cres | Datasheet |
| Threshold voltage | 2.5–4 V | 5–7 V | Datasheet |
| Rise/fall time | 20–80 ns | 50–200 ns | Datasheet |
| Gate resistance | 2–10 Ω (external) | 2–20 Ω (external) | Design choice |

### 4.3 Gate Driver Modeling

Gate driver parasitics affect switching behavior significantly for SiC:

- **Gate resistance (Rg):** Controls switching speed. Lower Rg → faster switching, higher dv/dt, more EMI, less switching loss.
- **Gate-source capacitance (Cgs):** Together with Rg determines turn-on delay: τ = Rg × Cgs
- **Miller capacitance (Cgd/Crss):** The dominant source of switching loss. Gate driver must sink/source current to charge/discharge Cgd.

### 4.4 Stray Inductance

The commutation loop stray inductance (Lσ = 10–30 nH) must be included for accurate switching loss and voltage overshoot:

```
V_overshoot = Vdc + Lσ × di/dt

Example: Lσ = 15 nH, di/dt = 5 kA/µs → V_overshoot = 75 V on top of Vdc
```

**Implementation:** Add an `Inductor` block in series with each switch, or use RL parasitic impedance in the DC-link path.

### 4.5 Use Cases

- Switching loss verification (Eon, Eoff vs. datasheet)
- Voltage overshoot analysis (busbar design validation)
- Dead-time optimization
- Common-mode voltage and bearing current analysis
- Radiated/conducted EMI prediction (with frequency-domain post-processing)

---

## 5. Motor and Load Models

### 5.1 PMSM Model

**Built-in blocks (Simscape Electrical):**
- `PMSM` — lumped-parameter model, sinusoidal back-EMF
- `FEM-Parameterized PMSM` — flux-linkage lookup tables from FEA

**Key motor parameters for FOC:**

| Parameter | Symbol | Typical Range (150 kW) | Unit |
|-----------|--------|------------------------|------|
| Stator resistance | Rs | 5–30 | mΩ |
| d-axis inductance | Ld | 0.1–0.5 | mH |
| q-axis inductance | Lq | 0.2–1.0 | mH |
| PM flux linkage | λPM | 0.05–0.15 | Wb |
| Pole pairs | P/2 | 4–8 | — |
| Rated speed | ωrated | 3000–6000 | rpm |
| Rated torque | Trated | 200–400 | Nm |
| Inertia | J | 0.05–0.2 | kg·m² |

**PMSM voltage equations (dq-frame):**
```
vd = Rs·id + Ld·did/dt − ωe·Lq·iq
vq = Rs·iq + Lq·diq/dt + ωe·(Ld·id + λPM)

Te = (3/2)·(P/2)·[λPM·iq + (Ld − Lq)·id·iq]
```

### 5.2 Mechanical Load

```
J·dωm/dt = Te − TL − B·ωm
```

Where J = total inertia (motor + vehicle reflected through gear), TL = load torque, B = viscous friction.

**Vehicle load torque reflection:**
```
TL = (R_wheel / GR) × (F_roll + F_aero + F_grade + F_accel) / η_gear

where:
  F_roll  = Crr × m × g
  F_aero  = 0.5 × ρ × Cd × A × v²
  F_grade = m × g × sin(α)
  GR = gear ratio, η_gear = transmission efficiency
```

### 5.3 Battery Model

Simplest model: DC voltage source with series resistance:
```
Vdc = V_oc(SOC) − I_dc × R_int(SOC)
```

For drive-cycle simulation, a lookup-table battery model (V_oc vs. SOC, R_int vs. SOC and temperature) is sufficient. The battery block in Simscape Electrical (`Battery`) provides generic Li-ion parameterization.

---

## 6. Thermal Modeling

### 6.1 Lumped Thermal Network (Foster or Cauer)

The power module's junction-to-case thermal impedance is modeled as an RC ladder network:

**Foster network (common in datasheets):**
```
Tj − Tc = Ploss × Zth(t)  where Zth(t) = Σ Ri·(1 − exp(−t/τi))
```

Typical 4th-order Foster network per switch:
| i | Ri (K/W) | τi (s) |
|---|---------|--------|
| 1 | 0.02 | 0.001 |
| 2 | 0.05 | 0.01 |
| 3 | 0.10 | 0.1 |
| 4 | 0.15 | 1.0 |

### 6.2 Implementation in Simulink

- **Cauer thermal network** blocks in Simscape Electrical
- Custom Simulink model: Ploss → heat flow source → RC ladder → Tj
- Coolant temperature (Tc) as boundary condition (typically 65–85°C for automotive water-glycol loop)

---

## 7. Simulation Setup and Verification

### 7.1 Solver Configuration

| Model Level | Recommended Solver | Max Step Size | Tolerance |
|-------------|-------------------|---------------|-----------|
| L1 (Averaged) | ode45 (Dormand-Prince) | 100 µs | 1e-4 |
| L2 (Switching-Function) | ode23tb (stiff) | 1 µs | 1e-6 |
| L3 (Detailed Switching) | ode23tb or ode15s | 10–50 ns | 1e-8 |

**Critical guideline:** max step size must be ≤ 1/20 of the smallest time constant (switching period or electrical time constant L/R).

### 7.2 Key Verification Checks

1. **DC power balance:** |Pdc − Pac − Ploss| < 1% of Pdc at steady state
2. **Phase current waveforms:** sinusoidal with expected THD (L2: <5% THD at rated load with SVPWM)
3. **Switching waveforms:** Vds and Id transitions match expected dv/dt and di/dt
4. **Thermal steady-state:** Tj converges to expected value (typically 125–150°C at rated power with 65°C coolant)
5. **Torque ripple:** within expected band (±5–10% for 2-level, <±3% for 3-level)

### 7.3 Common Simulation Pitfalls

| Issue | Symptom | Fix |
|-------|---------|-----|
| Algebraic loop | Simulink error / slow simulation | Add unit delay (1/z) in feedback paths |
| Stiff solver divergence | Simulation crashes at switching events | Use ode23tb with tighter tolerances |
| Numerical ringing | High-frequency oscillation on Vds after switching | Add snubber (R-C across switch) or increase parasitic resistance |
| Zero-crossing distortion | Current distortion near zero crossing | Reduce max step size; enable zero-crossing detection |
| Initialization transient | Large DC offset in first few cycles | Start from steady-state ICs or ramp Vdc from zero |

---

## 8. Integration with External Tools

### 8.1 PLECS Co-Simulation

PLECS (Plexim) provides more accurate switching loss and thermal models than Simscape. Common pattern:

```
Simulink (control + system) ←→ PLECS (power stage + thermal)
                                  ↓
                           Detailed loss maps
```

PLECS integrates via `PLECS Circuit` block in Simulink or standalone PLECS Standalone with MATLAB Engine API for scripting.

### 8.2 MATLAB Engine API (Python/External)

For AI-assisted design workflows, MATLAB is invoked as an external simulation backend:

```python
import matlab.engine
eng = matlab.engine.start_matlab()
eng.load_system('traction_inverter_model')
eng.set_param('traction_inverter_model/Vdc', 'Value', '400', nargout=0)
eng.sim('traction_inverter_model', nargout=0)
results = eng.workspace['logsout']
```

Referenced in the project's [[ai-agents/harness/matlab-integration]] research [26].

### 8.3 Data Export for AI/ML

For topology optimization via AI agents, the simulation pipeline exports:
- **Time-series:** phase currents, voltages, torque, speed, losses (`.mat` or CSV)
- **Aggregated metrics:** drive-cycle efficiency, peak efficiency, THD, BOM cost weight
- **Design parameter vectors:** {topology, device type, fsw, Vdc, module selection} → {efficiency, cost, power density}

---

## 9. Example Model Architecture (Simulink)

```
traction_inverter_model.slx
├── [Control Subsystem]
│   ├── Speed Controller (PI)
│   ├── MTPA / Flux Weakening LUT
│   ├── Current Controller (dq PI + decoupling)
│   ├── SVPWM Generator
│   └── Gate Signal Conditioning (dead time, inversion)
├── [Power Stage]
│   ├── DC Source (battery model)
│   ├── DC-Link Capacitor
│   ├── Three-Phase Inverter Bridge (Universal Bridge or custom switches)
│   └── Phase Current Sensors
├── [Motor + Load]
│   ├── PMSM (or Induction Motor)
│   ├── Mechanical Load (vehicle model)
│   └── Resolver / Position Sensor
├── [Thermal]
│   ├── Loss Calculator (conduction + switching)
│   └── Foster Thermal Network (×6 switches)
└── [Measurements + Scopes]
    ├── Power Analyzer (Pdc, Pac, efficiency)
    ├── THD Analyzer
    └── Data Logging to Workspace
```

---

> **References:** [[citations]]

## Red Team

**Steelman against:** This is a comprehensive catalog of MATLAB/Simulink blocks and modeling approaches, but it describes what's *possible* — not what produces *accurate* results. A Simulink model that runs without errors can still be physically wrong by 5-10% on efficiency and 20-30% on thermal predictions. The note provides no validation methodology, no calibration procedure, and no accuracy benchmarks. An AI agent following this guide would produce syntactically correct models with unknown physical accuracy.

**How it could be false:**
1. **No validation against hardware:** None of the modeling approaches described are validated against dynamometer data. A model built per this guide could predict 98% efficiency while the real inverter achieves 94%.
2. **Missing parasitic elements:** The switching models described (Universal Bridge, N-Channel MOSFET blocks) may omit DC-link ESL, busbar inductance, and gate-drive loop parasitics — all significant for SiC switching at >20 kV/µs.
3. **Thermal model fidelity gap:** The Foster/Cauer network approach assumes known thermal impedances. Real TIM degradation, mounting pressure variation, and aging effects can change Rth by 20-50%.
4. **Solver selection is critical and under-specified:** "ode23tb for stiff circuits" is correct but insufficient — step size, tolerance, and solver reset conditions dramatically affect both accuracy and runtime. A wrong MaxStep setting can produce stable but incorrect results.
5. **Training-knowledge dominance:** The recommended blocks, solver settings, and modeling fidelity levels are [T]-tagged — not verified against MathWorks documentation or published validation studies.

**What would change my mind:**
- A validation study: build a model per this guide, simulate a known inverter (e.g., Tesla Model 3 rear drive unit), and compare predicted vs measured efficiency to within 2% across the WLTP cycle.
- Published accuracy benchmarks for Simscape Electrical traction inverter models (MathWorks has some — cite them).
- Evidence that the automated modeling workflow (MATLAB Engine API from Python) produces models that match hand-built Simulink models within 1% on key metrics.

**Residual doubt:** The modeling guide is useful as a starting point. But the gap between "model runs" and "model is accurate" is where most simulation projects fail. An AI agent that doesn't calibrate against real data will produce believable but wrong results.

---
← [[power-electronics/traction-inverter/control-schemes]] | [[power-electronics/traction-inverter/traction-inverter-index]] →
