# Control How-To: Tuning and Implementing FOC for a Traction Inverter

> **Part of:** [[research/traction-inverter/traction inverter index]]  
> **Status:** 🟢  
> **Last Updated:** 2026-07-08

## 1. What This Note Is For

This is a practical implementation guide for field-oriented control (FOC) of a traction inverter driving a PMSM. It assumes you have a Simulink model and want to know the exact steps to tune the current loop, set up MTPA, and implement safe operating limits. It is the bridge between the theory in [[research/traction-inverter/control-schemes]] and the modeling in [[research/traction-inverter/matlab-modeling]].

## 2. Required Motor Parameters

Before tuning FOC, you need these parameters from the motor datasheet or identification tests [47][50]:

| Parameter | Symbol | Unit | Typical Range (150 kW IPMSM) |
|-----------|--------|------|-------------------------------|
| Stator resistance | Rs | mΩ | 5–30 |
| d-axis inductance | Ld | mH | 0.1–0.5 |
| q-axis inductance | Lq | mH | 0.2–1.0 |
| PM flux linkage | λPM | Wb | 0.05–0.15 |
| Pole pairs | Pp | — | 4–8 |
| Max current | Is,max | A rms | 300–500 |
| Base speed | ωbase | rpm | 3000–5000 |
| Max DC-link voltage | Vdc,max | V | 400–800 |

## 3. Step-by-Step FOC Implementation

### Step 1: Current Sampling and Alignment

- Sample phase currents at the center of the PWM period (center-aligned, symmetric PWM) to avoid switching ripple.
- Use Clarke transform to convert Ia, Ib, Ic → Iα, Iβ [47][50].
- Use Park transform with rotor angle θ to get Id, Iq [47][50].

```matlab
% Clarke (amplitude-invariant)
Ialpha = 2/3 * (Ia - 0.5*Ib - 0.5*Ic);
Ibeta  = 2/3 * (sqrt(3)/2 * Ib - sqrt(3)/2 * Ic);

% Park
Id =  Ialpha * cos(theta) + Ibeta * sin(theta);
Iq = -Ialpha * sin(theta) + Ibeta * cos(theta);
```

### Step 2: Set Up MTPA LUT

For an IPMSM, compute the MTPA trajectory offline [47][50]:

```matlab
% For each torque command Te and speed omega, find id*, iq*
% such that Te = (3/2)*Pp*(lambda_pm*iq + (Ld - Lq)*id*iq)
% and |id + j*iq| is minimized.
```

The output is a 2D lookup table: `id_ref(Te, ω)` and `iq_ref(Te, ω)`.

**Important:** At speeds above base speed, the voltage limit is hit. Use field-weakening LUTs or a voltage regulator that injects negative Id to keep Vd² + Vq² ≤ Vmax² [47][50].

### Step 3: Tune Current PI Controllers

Use Internal Model Control (IMC) pole-zero cancellation [49][50]:

```
Kp_d = bandwidth * Ld
Ki_d = bandwidth * Rs
Kp_q = bandwidth * Lq
Ki_q = bandwidth * Rs
```

where `bandwidth` is the desired current-loop bandwidth in rad/s.

**Practical rule:** Set current-loop bandwidth to 1/10 to 1/5 of the PWM update frequency (not switching frequency). For 10 kHz PWM with double update:

- PWM update frequency = 20 kHz
- Choose bandwidth ≈ 2π × 2 kHz = 12,566 rad/s
- Kp_d ≈ 12566 × 0.0003 = 3.77 V/A
- Ki_d ≈ 12566 × 0.015 = 188 V/(A·s)

Add cross-coupling decoupling and back-EMF feedforward:

```matlab
Vd_ff = -omega_e * Lq * Iq;
Vq_ff =  omega_e * (Ld * Id + lambda_pm);

Vd = Kp_d*(Id_ref - Id) + Ki_d*integral(Id_ref - Id) + Vd_ff;
Vq = Kp_q*(Iq_ref - Iq) + Ki_q*integral(Iq_ref - Iq) + Vq_ff;
```

### Step 4: Anti-Windup and Saturation

- The voltage vector is limited by the DC-link voltage: `Vmax = Vdc / sqrt(3)` in linear modulation.
- Clamp Vd and Vq so that `sqrt(Vd² + Vq²) ≤ Vmax`.
- Use integrator anti-windup (back-calculation or conditional integration) to prevent the PI integral from growing when the output saturates.

### Step 5: Generate SVPWM Gate Signals

Convert Vd, Vq to α, β, then to sector and duty cycles [47][50]:

```matlab
Valpha = Vd*cos(theta) - Vq*sin(theta);
Vbeta  = Vd*sin(theta) + Vq*cos(theta);

% Sector and duty-cycle calculation (7-segment SVPWM)
[sector, T1, T2, T0] = svpwm(Valpha, Vbeta, Vdc, Ts);
```

Apply dead time (1–2 µs for IGBT, 0.2–0.5 µs for SiC) and insert it into the gate signals with shoot-through protection.

### Step 6: Add Safety Limits

| Limit | Condition | Action |
|-------|-----------|--------|
| Overcurrent | Is > Is,max | Disable PWM, latch fault |
| Overvoltage | Vdc > Vdc,max | Disable regen, engage brake chopper if available |
| Undervoltage | Vdc < Vdc,min | Limp-home mode, reduce torque |
| Over-temperature | Tj > Tj,max | Reduce current limit linearly |
| Resolver fault | Position error > 5° | Active short circuit (ASC) |
| Torque mismatch | |T_est - T_ref| > 10% | ASC or freewheel [55] |

## 4. Tuning Procedure in Simulation

1. **Open-loop voltage test:** Apply small Vd, Vq to verify transforms and PWM direction.
2. **Current loop only:** Set speed loop to manual; apply step in Id_ref and Iq_ref. Tune Kp/Ki for ~10–20% overshoot and fast settling.
3. **Add speed loop:** Tune speed PI with bandwidth ~10–50 Hz. Speed loop should be much slower than current loop.
4. **Add MTPA/field weakening:** Verify torque-per-amp is maximized at low speed and voltage limit is respected at high speed.
5. **Drive-cycle test:** Run WLTP or EPA cycle profile and verify efficiency, temperature, and fault-free operation.

## 5. Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Wrong θ reference | Motor does not spin or spins backwards | Check encoder/resolver direction and pole-pair scaling |
| Cross-coupling ignored | q-axis current oscillates when d-axis steps | Add feedforward decoupling terms |
| PWM dead time too large | Current distortion near zero crossing | Reduce dead time; use adaptive dead-time compensation |
| Integrator windup | Large overshoot after transient | Add anti-windup and clamp voltage vector |
| Sample phase wrong | Noisy current feedback | Sample at PWM center, not edges |
| Voltage limit ignored | Inverter saturates at high speed | Add field-weakening control |

## 6. How to Verify It Is Working

| Check | Expected Result |
|-------|-----------------|
| Id, Iq step response | Settling to 95% within 1–2 ms, <20% overshoot |
| Steady-state current | Sinusoidal, low THD (<5%) |
| Torque at rated current | Matches motor torque constant ±5% |
| Efficiency at rated load | 96–99% depending on topology/device |
| Thermal steady-state | Tj < 150°C for IGBT, < 175°C for SiC |
| Fault injection | Safe state reached within 100 ms |

## 7. From Simulation to ECU

Once the Simulink FOC is validated, the typical production path is [51]:

1. **Fixed-point conversion:** Scale all signals to fixed-point arithmetic (e.g., Q15, Q31) for automotive MCUs.
2. **Code generation:** Use Simulink Coder / Embedded Coder to generate C code.
3. **SIL test:** Run generated code in Simulink (Software-in-the-Loop) against the plant model.
4. **PIL test:** Compile and run on target MCU with plant still simulated.
5. **HIL test:** Connect real ECU to real-time motor/inverter simulator.
6. **Vehicle test:** Calibrate on dynamometer, then road test.

## 8. Critical Honesty

- FOC tuning is **parameter-dependent**. If Ld, Lq, or Rs are wrong by 10–20%, the current loop will still work but torque accuracy and stability margins will degrade.
- Saturation, cross-coupling, and inverter nonlinearity (dead time, on-state voltage) become significant at low speeds and high currents. Production calibrations spend most effort here.
- The PI tuning rules above are **starting points**. Final tuning is done empirically on the motor dynamometer.

---

> **References:** [[citations]]

← [[research/traction-inverter/simulation-toolbox]] | [[research/traction-inverter/matlab-modeling]] →
