# 2L-B6 800 V SiC traction-inverter bench (purpose-fit, CRD operating point)

`bench_2l_b6_800v_sic.plecs` — a **purpose-built** 3-phase 2-level B6 inverter for the Track-1
CAB450M12XM3 validation, at the **Wolfspeed/TI 300 kW CRD operating point** (S5 anchor).
**Status (2026-07-21): VALIDATED** — heat-sink-coupled, Step-1 model complete, corner matrix (S1/S3/S4/S5) run.
Results: [`results/metrics/2l-b6-800v-sic-bench.txt`](../../results/metrics/2l-b6-800v-sic-bench.txt).

Built 2026-07-21 by retargeting the shipped PLECS demo `three_phase_voltage_source_inverter`
(a clean, proven 2L-B6 VSI + Sine/SV-PWM skeleton) to Wolfspeed CAB450M12XM3, then adding a heat
sink + thermal network + loss/efficiency/energy-balance/Tj instrumentation.

## Operating point (defaults in `InitializationCommands`; override per corner via `model_vars`)
| Var | Value | Meaning |
|-----|-------|---------|
| `Vdc` | 800 V | DC bus (CRD) |
| `Vg_rms` | 278 V | back-EMF (L-N rms) → sets current via `Iref=Pr/(3·Vg_rms)` |
| `Pr` | 300e3 W | rated power → **Iref ≈ 360 A rms** |
| `fac` | 200 Hz | fundamental (traction) |
| `fs` | 16 kHz | switching frequency (design spec) |
| `Ta` | 65 °C | coolant/ambient |
| `Lg` | 0.5 p.u. reactance (~102 µH) | motor-like filter → clean current (crest 1.46, THD 0.15 %) |
| Controller | **SV PWM** (Configuration=2) | extended linear range (m up to ~1.15) |

Devices: 6× `MosfetWithDiode` `Q1..Q6`, `thermal=file:CAB450M12XM3`, `Ron=0.0036`,
`CustomVariables struct('Rgon',4,'Rgoff',0)` (reproduce the **datasheet-nominal** Eon/Eoff).

## Validated results (2026-07-21)
**η = 99.07 %** at the CRD point (800 V / 359 A rms / 302 kW), clears the CRD **> 98 %** anchor.
Per-switch (avg of 6): conduction **208 W** + switching **262 W**. Σ6 loss **2815 W**.
**Tj_ss = 175 °C** at rated (analytic, R_cs CRD-calibrated) — matches the CRD 175 °C limit;
148 °C at the 300 A launch corner (< 175, PASS). Energy balance within ±0.6 % (S3). See the results file
for the full 6-corner table, the S1 convergence check, and the analytic conduction cross-check (−3.5 %).

## Coupling (the one manual step — DONE)
Device→heat-sink coupling is GUI-established spatial enclosure, not scriptable (PLECS 4.8 RPC =
get/set/load/close/simulate only). The `Heat Sink` block was GUI-created over Q1–Q6 and wired to the
coolant chain; coupling is **confirmed** and now **survives text edits**. Everything since is headless.
**Do NOT text-delete/recreate the `Heat Sink` block** — it would break the association.

## How to drive it headless (recipe)
```
# PLECS running: PLECS.exe -server 1080
close_model bench_2l_b6_800v_sic          # escape the stale-model trap after ANY text edit
open_model  <abs>/bench_2l_b6_800v_sic.plecs
# point every ToFile at an absolute path (reload resets them to relative):
set_component_param <model>/mCap Filename <abs>/main.csv   # + condCap swCap hfCap allCap allSwCap pwrCap tjCap
simulate <model>  model_vars={...full consistent set...}
# read CSVs with numpy.genfromtxt(delimiter=','); average over the steady-state tail.
```
**model_vars are applied AFTER `InitializationCommands`** — so derived quantities (`Iref`, `Vref`, `Lg`,
`phase_*`, `i_init`) do NOT recompute from a raw `Pr`/`Vg_rms` override. To run a consistent corner you must
pass the **complete** variable set (see `gen_vars.py` in the run scratch, which replicates the init math).
Overriding `Vdc` alone is safe (it only feeds the live DC source + modulation ratio).

## Instrumentation (each ToFile `Filename` is relative in-file; set absolute at run time)
| Chain | ToFile | Columns (col 0 = Time) |
|---|---|---|
| `mProbe` V_dc1{V,I} + L1{I} + Q1{cond,sw} | `mCap` | Vdc, Idc, Ia, Q1_cond, Q1_sw |
| `allP`{Q1..6 cond} → `paAllCond`(1/fac) | `allCap` | 6× conduction **avg** |
| `allSwP`{Q1..6 sw} → `piaAllSw`(1/fac) | `allSwCap` | 6× switching **avg** (PeriodicImpulseAverage) |
| `pwrProbe` V_3ph{v_abc} + L1/L2/L3{i_abc} | `pwrCap` | vg_a,b,c, i_a,b,c (2 µs — for P_out, THD, crest) |
| `tjProbe` Q1,Q2{Device junction temp} + Heat Sink{Temperature} | `tjCap` | Q1_Tj, Q2_Tj, T_sink (in-model, transient) |
| `Whf`:3, `condP`→`paCond`, `swP`→`piaSw` | `hfCap`,`condCap`,`swCap` | legacy single-switch references |

Thermal net: `Heat Sink`(Cth via RPC) → `Whf` → **`Rcs`** (ThermalResistor, `Rth=Rcs_val`=0.0267) → `Tcool`(=Ta) → `Tgnd`.
The series `Rcs` gives the sink node a real impedance so `Device junction temp` reads (rises 65→107 °C in 0.05 s;
full steady state needs the thermal timescale, hence the **analytic** Tj_ss for the reported number).

## Gotchas (each cost real time)
- After ANY `.plecs` text edit: `close_model` **then** `open_model`. Verify new blocks with `get_component_param`.
- Block order in a `Schematic{}`: all `Component{}` before all `Connection{}` before `Annotation{}`. Multi-line blocks only.
- Probe signal names are exact: `"Device conduction loss"`, `"Device switching loss"`, **`"Device junction temp"`**
  (NOT "MOSFET junction temp" — that yields no column). Heat sink: `"Temperature"`.
- ThermalResistor resistance param is **`Rth`** (not `R`). Averaging blocks: input=term 2, output=term 1.
- Cannot save or add components via RPC (only `plecs.set`) — persistent changes are text edits; per-run values (Filenames,
  Heat Sink `Cth`, corner `model_vars`) are RPC/runtime.
