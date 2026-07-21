# 2L-B6 800 V SiC traction-inverter bench (purpose-fit, CRD operating point)

`bench_2l_b6_800v_sic.plecs` — a **purpose-built** 3-phase 2-level B6 inverter for the Track-1
CAB450M12XM3 validation, at the **Wolfspeed/TI 300 kW CRD operating point** (S5 anchor).

Built 2026-07-21 by retargeting the shipped PLECS demo `three_phase_voltage_source_inverter`
(a clean, proven 2L-B6 VSI + Sine-PWM skeleton) to Wolfspeed CAB450M12XM3, then adding a heat
sink + thermal network + loss/efficiency instrumentation. Chosen over hacking the `rainflow`
IM-drive base because the demo gives a physically-correct, parameter-clean 800 V inverter.

## Operating point (set in `InitializationCommands`)
| Var | Value | Meaning |
|-----|-------|---------|
| `Vdc` | 800 V | DC bus (CRD) |
| `Vg_rms` | 278 V | back-EMF (L-N rms) → sets current via `Iref=Pr/(3·Vg_rms)` |
| `Pr` | 300e3 W | rated power → **Iref ≈ 360 A rms** |
| `fac` | 200 Hz | fundamental (traction) |
| `fs` | 16 kHz | switching frequency (design spec) |
| `Ta` | 65 °C | coolant/ambient |

Devices: 6× `MosfetWithDiode` `Q1..Q6`, `thermal=file:CAB450M12XM3`, `Ron=0.0036`,
`CustomVariables struct('Rgon',4,'Rgoff',0)` (Rgon=4/Rgoff=0 reproduce the **datasheet-nominal**
Eon/Eoff — the XML scales by `lookup('Eon(Rg)',Rgon)/lookup('Eon(Rg)',4)`; the 800 V and 175 °C
loss-table grid points are exact).

## Verified headless (2026-07-21)
- **Operating point CONFIRMED:** Vdc=800.0 V, phase current **357.5 A rms** (target 360),
  **Pin = 292.4 kW** (target ~300). Electrical skeleton + CAB450 loads and runs.
- **Conduction-loss readout works** and is temperature-dependent: Q1 `Device conduction loss`
  = 73 W @Tj0=0 °C → 94 W @Tj0=65 °C (Rds(on)(Tj) responding correctly).
- Model instrumented: `mProbe`→`mCap` ToFile captures `[Vdc, Idc, Ia, Q1_Pcond, Q1_Psw, Q1_Tj]`.

## THE ONE MANUAL STEP — couple the devices to the heat sink (GUI)
Device→heat-sink coupling **cannot be scripted** (confirmed against the PLECS 4.8 manual:
the RPC/scripting API is get/set/load/close/simulate/analyze/scope only — no add/connect/heat-sink
command; coupling is GUI-established spatial enclosure, not a settable parameter). Until coupled,
**`Q1 Device junction temp` reads 0** and losses are at the wrong temperature.

**Do this once in the PLECS GUI, then save:**
1. Open `bench_2l_b6_800v_sic.plecs`.
2. The yellow **`HS`** heat-sink box already encloses `Q1..Q6`. For each of `Q1..Q6`, click the
   device and nudge it (drag 1 px or cut+paste **onto** the `HS` box) so PLECS registers it as
   *on* the heat sink (it highlights when coupled).
3. **Save.** Then tell me — I run the corner matrix headless from there.

Verify coupling took: after saving, a run should show `Q1 Device junction temp` **bounded near
Ta+ΔT** (not 0, not the 684 °C uncoupled runaway).

## Remaining (headless, after coupling)
1. Add `PeriodicImpulseAverage`(T=1/fac) on `Device switching loss` + `PeriodicAverage` on
   conduction (raw switching sample 194 W is unreliable — impulses need the dedicated block; see
   memory `plecs-loss-readback-periodicimpulseaverage`).
2. Read temperature-correct per-switch losses + Tj; inverter loss = 6× (balanced); η = Pout/Pin.
3. Confirm energy balance (S3: Pin=Pout+Ploss ±1%).
4. Run the 9-corner matrix (`procedure-simulation-and-validation` §4); calibrate ≥1 corner to the
   CRD (S5: >98 % η, 175 °C). Cross-check vs the `experiments/*/` numpy models.
5. Fill `design-2l-b6-800v-sic`; set `model_registry.json` → `validated`.

## Runner note
`mCap` writes `bench_meas.csv` (relative). Set an absolute path via
`plecs.set("<model>/mCap","Filename","<abs>.csv")` before a headless run, or it lands next to the model.
