---
title: "Worked Example — Family-Car Traction Inverter (400 V SiC, vehicle-grounded, model-run)"
type: topic
field: power-electronics
created: 2026-07-18
updated: 2026-07-19
status: unverified
evidence: single-study
sources: [sources/power-electronics/sachs-neuburger-2025-3l-tnpc, sources/ai-agents/pe-mas-flyback-mas]
tags: [power-electronics, traction-inverter, design, sizing, two-level, sic, igbt, example, efficiency]
review_by: 2026-10-17
---

## What This Is

A **design-by-doing** worked example: invent a common family 4-wheeler, size its traction inverter end-to-end with the vault's method, then **actually run a numerical model** (`worked-designs/family-car-400v-sic/familycar_inverter.py`) to produce the efficiency/thermal/cycle numbers the other worked examples defer to PLECS ([[design-2l-b6-800v-sic]], [[worked-example-400v-150kw]]). New here vs those: (1) operating points are **derived from vehicle road-load physics**, not assumed; (2) a **SiC-vs-IGBT drive-cycle comparison is computed**; (3) the design was **loaded and simulated in PLECS**. Findings distilled in [[findings-family-car-design-by-doing]].

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training/undergrad common knowledge; `[model]` → computed by the model script (datasheet-class loss model, params in §3); `[derived]` → from the cited relations.

## 1. The Vehicle — "SRTP FamilyCrossover" (invented)

C-segment front-drive BEV crossover (VW ID.4 / Kona-EV class). Road load `F = mg·Cr + ½ρ·Cd·Af·v² + m·a` [30][T]:

| Param | Value | | Param | Value |
|-------|-------|-|-------|-------|
| Test mass `m` | 1850 kg | | Wheel radius `rw` | 0.32 m |
| Drag `Cd` | 0.29 | | Gear ratio `ig` | 9.0 |
| Frontal area `Af` | 2.30 m² | | Gearbox η | 0.97 |
| Rolling `Cr` | 0.010 | | Air density `ρ` | 1.20 kg/m³ |

**Derived performance** [model]: 160 km/h needs **43 kW** steady (aero-limited); the machine delivers **≈135 kW peak / 345 Nm** (0–100 km/h ≈ 7.5 s) and **~55 kW continuous** (sustains hill/tow). Max motor speed at 160 km/h = **11 940 rpm**. This is the first vault example where `Is,max` is *output* of the vehicle, not an input `[T]`.

## 2. Electrical Specification

| Item | Value | Basis |
|------|-------|-------|
| Topology | 2-level B6 (6-switch VSI) | >95% of production, [[circuit-topologies]] §1 |
| DC bus | **355 V nom** (280–420 V), 450 V clamp | 96S NMC family pack `[T]` |
| Motor | IPMSM: `Pp`=4, `Rs`=15 mΩ, `Ld`=0.15 mH, `Lq`=0.30 mH (saliency 2.0), `λPM`=0.075 Wb | scaled from [[machine-and-load]] §3 [47][50] |
| Max phase current | **400 A rms** (566 A pk) | launch/thermal limit [model] |
| Device | **750 V SiC MOSFET**, ~600–800 A class | §3, [99] |
| Switching freq | 12 kHz (SiC) | SiC 2L band [50] |
| Cooling | pin-fin water-glycol, 65 °C inlet | [[thermal-design]] |

## 3. Topology, Device & Loss Model

**2L-B6 SiC**, benchmarked against a **750 V Si-IGBT** comparator. Device loss params are datasheet-class typicals `[T]` (per switch): SiC `Rds(on,150°C)`≈4.5 mΩ, `Eon+Eoff@400V/400A`≈9 mJ; IGBT `Vce0`≈0.9 V + `Rce`≈2.5 mΩ, diode 1.0 V + 1.8 mΩ, `Eon+Eoff+Err`≈32 mJ [25][122]. SiC at 12 kHz, IGBT at 8 kHz (its practical ceiling). **750 V not 650 V:** worst-case 420 V bus + `Lσ·di/dt` overshoot → ~72% utilization with cosmic-ray margin [[protection-and-safety]] §1 [121].

## 4. Results — the Model Run  `[model]`

**Efficiency at 3 DC corners** (peak-power operating point; conduction dominates at low-line as [[worked-example-400v-150kw]] predicts):

| Corner | SiC η | IGBT η | note |
|--------|:-----:|:------:|------|
| low-line 280 V | 98.08% | 97.95% | 397 A rms, conduction-heavy |
| nominal 355 V | 98.69% | 98.44% | 335 A rms |
| high-line 420 V | 98.96% | 98.64% | 290 A rms, lowest loss |

**Thermal** (per-switch loss → Tj, 65 °C coolant, `Rth`≈0.30 K/W): peak 135 kW → **SiC Tj ≈ 155 °C** (20 °C margin); **IGBT Tj ≈ 173 °C** — only **2 °C** under its 175 °C limit. Continuous 55 kW: SiC 83 °C. **DC-link ripple** ≈ **170 A rms** at peak → the driver is *ripple current*, not capacitance → ~450 µF film, ≥600 V, 170 A-rms class [84][41].

**Synthetic drive cycles** (representative, *not* official WLTP traces):

| Cycle | SiC inv-η | IGBT inv-η | SiC saves (inverter only) |
|-------|:---------:|:----------:|---------------------------|
| Urban (mean 27 km/h) | 98.16% | 96.65% | **591 Wh/100 km** (+1.5 pt) |
| Mixed (mean 68 km/h) | 98.99% | 97.95% | **281 Wh/100 km** (+1.0 pt) |

## 5. Control (FOC, instantiated)

Per [[control-how-to]]: FOC + MTPA + field-weakening, SVPWM, resolver, ASC safe state. **IMC current-loop gains** at BW = 2π·1.5 kHz [derived §3, control-how-to §3]: `Kp_d`=1.41, `Kp_q`=2.83 V/A, `Ki_d=Ki_q`=141 V/(A·s). 12 kHz → 83 µs PWM, double-update 42 µs, current-loop BW ~1/8 of update. MTPA runs `id<0` for reluctance torque (saliency 2.0); field-weakening from ~4500 rpm base to 12 000 rpm. Safety: resolver-fault / torque-mismatch → **ASC** (bus would otherwise pump via body diodes at speed) [55], [[protection-and-safety]] §5.

## 6. BOM — the actual parts and why

Class-level method in [[bom]]; here are the **specific parts chosen for this design**, each tied to the computed sizing driver. Part numbers are representative-class and must be datasheet-checked `[T]`, per vault convention.

| Function | Chosen part | Key spec | Qty | **Why this part** (driver) | Cite |
|----------|-------------|----------|----:|----------------------------|------|
| **Power module** | **Infineon HybridPACK Drive G2, 750 V SiC (CoolSiC)** | 750 V, ~600–820 A, `Rds`~3–5 mΩ, pin-fin direct-cooled | 1 (3 half-bridges) | 750 V blocks the 420 V-max bus + overshoot at ~55–72% util (650 V too tight); ~800 A class covers the **566 A peak** launch current (§4); the family-car standard module (VW MEB / E-GMP) [36][99] | [36][99] |
| *— IGBT comparator* | *Infineon HybridPACK Drive FS820R08A6P2B* | *750 V, 820 A, EDT2 Si-IGBT* | *1* | *same footprint/cooler → isolates the device-tech variable for §4* | [36] |
| **Gate driver** | **TI UCC21750-Q1** | isolated ±10 A, 5.7 kV reinf., desat, Miller clamp, ASC pin | 6 | ±10 A charges SiC gate at 12 kHz; **desat <1 µs** for SiC's 3–5 µs SCWT; built-in **ASC** = the safe state (§5); 5.7 kV meets IEC 61800-5-1 | [40][93], components §2.2 |
| **Isolated bias** | **Murata MGJ2 class** | +15 V / **−4 V**, 5.2 kV, per channel | 6 | SiC needs **negative off-bias** (−4 V) to stop Miller-induced turn-on at low `Vth` | [40] |
| **DC-link cap** | **TDK xEV film (metallized PP), ~450 µF, 600 V** | ≥ **180 A rms** ripple, low ESL, self-healing | 1 bank | **ripple current (170 A, §4) is the driver, not µF**; 600 V = 420 V bus + margin; film (not electrolytic) for ripple/ESR/no-dry-out over life | [41][90][84] |
| **Phase-current sensor** | **LEM LF 510-S** (closed-loop Hall) | 500 A nom, ±800 A range, ±0.6%, BW>50 kHz | 2 (+1 for ASIL) | isolated, BW>50 kHz for FOC; ±800 A range spans the 566 A peak; 2 suffice (ΣI=0), 3rd adds redundancy | [100][42] |
| **Rotor position** | VR **resolver + RDC** | ±0.1°, absolute from standstill | 1 | ASIL-D needs **guaranteed** position; fails safe (vs sensorless) | [48] |
| **Control MCU** | **Infineon AURIX TC397** | 6-core, ASIL-D, 3-φ center-aligned PWM, resolver IF | 1 | ASIL-D torque path + hardware FOC/PWM + safety monitoring (§5) | [98] |
| **Cold plate** | pin-fin water-glycol, 65 °C inlet | `Rth`~0.30 K/W (jc+ch+cooler) | 1 | hits the computed **SiC Tj 155 °C** at peak; single-side suffices for SiC (IGBT would need more — Finding 3) | [101] |
| **Busbar / HV** | laminated Cu busbar; HV contactors ×2; precharge R; HV fuse; active-discharge | `Lσ<15 nH`; bus **<60 V** on shutdown | 1 set | 2× current (vs 800 V) makes low-`Lσ` + I²R **harder**; discharge per ISO 6469-3 [157] | [25][157], packaging-and-layout |

**Device electrical params used in the model (§4) ↔ part:** SiC `Rds(on,150°C)`≈4.5 mΩ, `Eon+Eoff@400V/400A`≈9 mJ, `Tj,max` 175 °C — consistent with the 750 V CoolSiC HybridPACK class [99]; IGBT `Vce0`≈0.9 V + `Rce`≈2.5 mΩ, `Esw`≈32 mJ — consistent with the FS820R08A6P2 EDT2 class [36]. These are class-typicals `[T]`; the SiC-vs-IGBT gap is sensitive to the `Esw` ratio (Red Team). Cost split unchanged: module ~40–50% [29].

## 7. PLECS Status

PLECS Standalone is **licensed and driveable via XML-RPC** here (`plecs.load/set/simulate`) — this **clears the vault's flagged "PLECS license check"** blocker [[README]]. The `permanent_magnet_synchronous_machine` FOC demo was **retargeted to this machine** (`Rs`=15 mΩ, salient `Ld/Lq`, `λ`=0.075, 355 V) and **simulated to completion** (`worked-designs/family-car-400v-sic/pmsm_mycar.plecs`) [58][78][72]. Quantitative readback needs top-level outports on torque/current/loss — the documented next step ([[simulation-and-validation]] §4). Until then §4 numbers are the analytic model, equivalent to PLECS's *averaged* thermal-loss layer, pending its *switching-resolved* confirmation.

## 8. The Report — Compromises

- **400 V, not 800 V:** chosen for a *common* family car — mature 650/750 V devices, cheaper isolation, huge ecosystem [94]. Cost: 2× current → conduction-dominated loss, bigger cap/busbar, ~0.5 pt lower peak η than an 800 V build [[worked-example-400v-150kw]].
- **SiC, not IGBT:** buys +1.0–1.5 pt cycle efficiency and **18 °C thermal headroom at peak**; IGBT is cheaper die but here is **thermally marginal (173 °C)** at 135 kW and would force a bigger cooler or a peak-power derate. A strict cost-first economy trim → IGBT + reduced peak.
- **12 kHz:** above cabin-audible harshness, low enough for loss/EMI; SiC could clock higher but EMI/switching-loss rises [[emi-emc-design]] §2.
- **750 V device on a 420 V-max bus:** ~55–72% utilization — deliberately conservative for cosmic-ray/overshoot margin over a 650 V part [121].

## Red Team

**Steelman against:** The numbers look authoritative but rest on **invented device loss parameters** (`Rds`, `Esw`, `Vce`) that are class-typicals `[T]`, not a specific datasheet — the same soft spot as every other vault example, plus a self-authored quasi-static loss model instead of PLECS. The 591 vs 281 Wh/100 km "urban 2×" split is real in the model but inflated by an **aggressive synthetic cycle** (hard launches, no coast-down map), not WLTP. The SiC-vs-IGBT delta scales directly with the assumed `Esw` ratio (9 vs 32 mJ), which I chose.

**How it could be false:**
1. **Loss params drive everything** — a ±30% error in `Esw` or `Rds` [25] moves every efficiency figure and the whole SiC-IGBT gap; the *direction* is robust, the *magnitude* is soft.
2. **Quasi-static model** ignores dead-time distortion, reverse recovery detail, DC-ripple feedback, and real PWM harmonics — exactly what PLECS's switching layer would add (a few % on cycle loss) [63].
3. **Synthetic cycles** are not WLTP/EPA; absolute Wh/100 km is indicative, `%`-points are the robust metric.
4. **Motor params `[T]`** (saturation, temperature) shift MTPA and currents ±20–30% [[machine-and-load]] Red Team.
5. **PLECS "ran" ≠ validated** — completion proves numerical stability, not that its losses match §4; readback pending.

**What would change my mind:** PLECS with real 750 V SiC/IGBT loss tables + top-level outports reproducing §4 at the three corners; the official WLTP class-3 trace replacing the synthetic cycle; a real IPMSM datasheet.

**Residual doubt:** The *method* (vehicle → operating points → loss → cycle) and the *directional findings* (SiC wins on cycle + thermal; advantage is switching-loss-driven so largest in urban; conduction crosses over at extreme current) are solid and internally consistent. The absolute numbers are a computed hypothesis — but a **runnable, inspectable** one, which is the step forward.

---

> **References:** [[citations]] · model: `worked-designs/family-car-400v-sic/`

← [[worked-example-400v-150kw]] | [[findings-family-car-design-by-doing]] | [[reference-designs-index]] →
