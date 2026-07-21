# PLECS Track-1 handoff — finish the Model + run the Corner matrix (2026-07-21)

For the next agent continuing [`plan-depth-research`](../../knowledge/synthesis/plans/plan-depth-research.md).
Read this, then the changelog [`2026-07-21-plecs-2l-b6-bench-and-coupling`](../../knowledge/synthesis/log/changelog/2026-07-21-plecs-2l-b6-bench-and-coupling.md)
and the bench [`README`](../../experiments/2l-b6-800v-sic-bench/README.md).

> **STATUS 2026-07-21 (cont.): STEP 1 COMPLETE + STEP 2 CORE DONE (S1/S2/S3/S4/S5).**
> The bench is **`validation_status: validated`**. See changelog
> [[2026-07-21-plecs-2l-b6-model-complete-and-corners]] and results
> [`results/metrics/2l-b6-800v-sic-bench.txt`](../../results/metrics/2l-b6-800v-sic-bench.txt).
> Everything below Step 1.1–1.4 and Step 2 S1–S5 is **done**; what remains is **corners 6–9**
> (field-weakening/ASC/short-circuit/drive-cycle — need control/fault/averaged models), **S6/S7**
> (averaged↔switched reconciliation — need an averaged model), then the **Design note → Fold back → Close** stages.

**The coupling blocker is SOLVED.** This handoff covered Track-1 stages **Step 1 (Model — finish it)**
and **Step 2 (Corner matrix)**. (Track-1 stages: Model → Corner matrix → Design note → Fold back → Close.)

---

## Where Track 1 stands

**Step 1 (Model): DONE.** Purpose-fit 800 V 2L-B6 CAB450 bench, heat-sink-coupled, **η = 99.07 %** at the
CRD point, all four gaps closed.

| Piece | State |
|-------|-------|
| Operating point (800 V, 359 A rms, 302 kW) | ✅ verified headless |
| Device→heat-sink coupling | ✅ CONFIRMED — survives text edits, everything headless |
| Conduction loss readout (`PeriodicAverage`, all 6) | ✅ works, T-dependent, aliasing-free |
| **Switching** loss readout (`PeriodicImpulseAverage`, all 6) | ✅ works |
| Efficiency η = (Pin−Ploss)/Pin | ✅ **99.07 %** at CRD (99.03–99.32 % across corners) |
| **Junction-temperature readout** | ✅ FIXED — signal `"Device junction temp"` + series `Rcs`; reported Tj_ss analytic (175 °C) |
| Energy balance (S3) | ✅ −0.37 % at CRD (< ±1 % all corners) |
| Clean operating point (SV PWM + Lg=0.5) | ✅ crest 1.80→1.46, THD 0.15 % |
| All-6 sum (not ×6-Q1) | ✅ Σ6 = 2815 W (near-symmetric with clean current) |
| Corner matrix S1/S2/S3/S4/S5 | ✅ 6 corners run, converged, CRD-calibrated |
| Corners 6–9, S6/S7 | ☐ deferred — need control/fault/averaged models |

**Coupling was solved by a GUI action (the one unavoidable one):** the user deleted the text heat sink
and **GUI-created a fresh `Heat Sink`** over Q1–Q6, then wired its port to the coolant chain.
**Confirmed** two ways: (a) raising coolant `Ta` 65 °C→150 °C raised Q1 conduction 94→157 W (junction
tracks coolant ⇒ coupled); (b) all 6 switches dissipate 170–243 W conduction (all coupled, none runaway).
**A text-authored heat sink cannot be coupled to by dragging — the sink itself must be GUI-created.**
Coupling then survives text edits, so **do NOT delete or recreate the `Heat Sink` block in text** — it
would break the association and you'd need the GUI again.

---

## The bench (files + structure)

- **Model:** `experiments/2l-b6-800v-sic-bench/bench_2l_b6_800v_sic.plecs` — model name (for `simulate`/`set`)
  is the file basename **`bench_2l_b6_800v_sic`**.
- **Device model (search folder):** `experiments/2l-b6-800v-sic-bench/bench_2l_b6_800v_sic_plecs/CAB450M12XM3.xml`
  (the current "MOSFET with Diode" format; `file:<part>` resolves from the `<basename>_plecs/` sibling folder).
- Built from the shipped PLECS demo `three_phase_voltage_source_inverter` (a proven 2L-B6 VSI + Sine-PWM
  skeleton), retargeted to CAB450.

**Operating point** — set in the model `InitializationCommands` (all overridable at run time via
`simulate(..., model_vars={...})`):

| Var | Value | Meaning |
|-----|-------|---------|
| `Vdc` | 800 | DC bus (V) |
| `Vg_rms` | 278 | back-EMF L-N rms → sets current: `Iref = Pr/(3·Vg_rms)` ≈ 360 A |
| `Pr` | 300e3 | rated power (W) |
| `fac` | 200 | fundamental (Hz) |
| `fs` | 16e3 | switching frequency (Hz) |
| `Ta` | 65 | coolant/ambient (°C) — this is also `Tcool.T` |
| model `TimeSpan` | 0.05 | sim duration (s) = 10 fundamental periods |

**Devices:** `Q1..Q6` (`MosfetWithDiode`), `thermal=file:CAB450M12XM3`, `Ron=0.0036`,
`CustomVariables "struct('Rgon',4,'Rgoff',0)"` (Rgon=4/Rgoff=0 reproduce the **datasheet-nominal**
Eon/Eoff — the XML scales by `lookup('Eon(Rg)',Rgon)/lookup('Eon(Rg)',4)`; 800 V and 175 °C are exact
grid points in the loss table). `T_init=Ta`, device `Rth=0`.

**Thermal net (GUI heat sink + wired chain):** `Heat Sink` [295,350] frame [-117,-82;117,82] enclosing
Q1–Q6 → `Whf` (HeatFlowMeter) → `Tcool` (ConstantTemperature, `T=Ta`) → `Tgnd` (ThermalGround). All Rth/Cth
currently 0 (this is why Tj reads 0 — Step 1.1). `3ph Meter` was moved to [475,335] so it doesn't overlap
the sink (PLECS errors if a heat sink overlaps a non-thermal block).

**Instrumentation already in the model** (each `ToFile` `Filename` is *relative* in the file — set an
absolute path at run time with `set_component_param`):

| Probe/chain | ToFile | CSV columns (col 0 = Time) |
|---|---|---|
| `mProbe`: V_dc1{Source current, Source voltage} + L1{Inductor current} + Q1{Device conduction loss, Device switching loss, MOSFET junction temp} | `mCap` (`bench_meas.csv`) | Idc, Vdc, Ia, Q1_cond(raw), Q1_sw(raw), Q1_Tj(=0) |
| `condP`{Q1 Device conduction loss} → `paCond` (PeriodicAverage, T=1/fac) | `condCap` (`bench_cond.csv`) | Q1 conduction **avg** = 205 W |
| `swP`{Q1 Device switching loss} → `piaSw` (**PeriodicImpulseAverage**, T=1/fac) | `swCap` (`bench_sw.csv`) | Q1 switching **avg** = 244 W |
| `Whf`:3 (heat-flow signal) | `hfCap` (`bench_hf.csv`) | total heat flow (452 W — **transient**, see 1.1) |
| `allP`{Q1..Q6 Device conduction loss} | `allCap` (`bench_all.csv`) | Q1..Q6 conduction (raw) |

**Preliminary result** (0.05 s run): Vdc=800, Ia=357 A rms, Pin=292.4 kW; per-switch conduction 205 W +
switching 244 W; all-6 conduction sum **1233 W** (high-side Q1/Q3/Q5 ≈240 W, low-side Q2/Q4/Q6 ≈172 W —
a real power-factor asymmetry); **η ≈ 99.1 %**.

---

## How to drive it headless (recipe)

```
# PLECS must be running: PLECS.exe -server 1080
close_model  bench_2l_b6_800v_sic                     # if already loaded (stale-model trap)
open_model   D:/.../experiments/2l-b6-800v-sic-bench/bench_2l_b6_800v_sic.plecs
# point every ToFile at an absolute readable path:
set_component_param  bench_2l_b6_800v_sic/condCap  Filename  C:/.../scratch/cond.csv
set_component_param  bench_2l_b6_800v_sic/swCap    Filename  C:/.../scratch/sw.csv
set_component_param  bench_2l_b6_800v_sic/mCap     Filename  C:/.../scratch/main.csv
# run a corner — CAUTION: model_vars are applied AFTER InitializationCommands, so a bare
# {"Pr":150e3,"Vg_rms":...} does NOT recompute Iref/Vref/Lg/phase_*/i_init -> inconsistent!
# Pass the COMPLETE consistent var set (experiments/2l-b6-800v-sic-bench/gen_vars.py replicates the init):
#   vars=$(python gen_vars.py 550 175 94500); simulate bench_2l_b6_800v_sic model_vars=$vars
# Overriding Vdc alone IS safe (only feeds the live DC source + modulation ratio):
simulate  bench_2l_b6_800v_sic  model_vars={"Vdc":850}
# read the CSVs with numpy.genfromtxt(delimiter=','); average over the steady-state tail
```

**Non-negotiable gotchas (each cost real time this session):**
- **Stale-model trap:** after ANY `.plecs` text edit, `close_model` **then** `open_model` — a plain
  `open_model` on an already-loaded model does **not** refresh it. Verify a new block landed with
  `get_component_param` before trusting a run (`load` returns ok even when it silently drops blocks).
- **`.plecs` block order inside a `Schematic{}`: all `Component{}` before all `Connection{}` before
  `Annotation{}`.** A Component after Connections, or a Connection after an Annotation, is silently dropped.
- **Multi-line blocks only:** single-line `Parameter { Variable "X" Value "Y" Show off }` or
  `Probe { ... }` are dropped on load. Each field on its own line.
- **Probe signal names are exact; one invalid name voids the whole probe (→ a single 0 column).**
  DCVoltageSource: `"Source voltage"`, `"Source current"` (NOT `"Source power"`). `MosfetWithDiode`+CAB450:
  `"Device conduction loss"`, `"Device switching loss"` (there is no separate `"Diode ..."`; those are lumped).
- **Averaging blocks:** input = terminal **2**, output = terminal **1**. `T_average = "1/fac"` (average over
  the fundamental period, not the switching period, for an inverter).
- **Loss/Tj probing requires the device be on an active heat sink** (PLECS errors otherwise).
- Demo files copied from the PLECS install are **read-only**; write via temp file + `os.replace` (retry).
- `simulate`'s `stop_time` arg is ignored; the model `TimeSpan` controls duration.

---

## STEP 1 — finish the Model

### 1.1 Fix the junction-temperature readout (the main gap)
`Device`/`MOSFET junction temp` reads **0** because the thermal path has **zero R and zero C**: with
device `Rth=0`, `Heat Sink Cth=0`, and a 0 Ω `Whf` straight to the `Tcool` source, the junction is
*algebraically* pinned at the coolant temperature — there is no thermal **state** for the probe to expose.
The conduction loss is right (it uses the correct junction temp internally, ≈coolant), only the *readout*
is missing, and Tj never rises above coolant.

**Fix — give the path a real impedance with a capacitance so the junction becomes a state:**
1. Insert a **case/sink-to-coolant thermal resistance** and a **heat-sink capacitance**. Concretely: add a
   `ThermalResistor` (`R`≈ cold-plate Rth, e.g. 0.02–0.05 °C/W) **between** the `Heat Sink` port and `Whf`
   (or between `Whf` and `Tcool`), and set the `Heat Sink` `Cth` > 0 (e.g. a cold-plate mass).
   **CRITICAL:** giving `Heat Sink Cth>0` with the *existing* 0 Ω path to `Tcool` throws
   *"state/source dependence — HS directly dependent on source Tcool"* (a capacitance across a source).
   The series `ThermalResistor` removes that conflict. (The shipped `buck_converter_with_thermal_model`
   demo's `ThermalChain` (Rth+Cth) is the proven pattern — it yields a readable, bounded Tj.)
2. The device's own junction-to-case impedance comes from the **XML Cauer network** (`R_th,JC`≈0.094 °C/W
   for the module). Setting device `Rth` alone (a resistance, no C) did **not** make Tj read — a
   capacitance in the path is required. Verify Tj rises to a realistic **~120–160 °C** at the operating point.
3. **Thermal-timescale caveat (important for the number to be valid):** a switched 0.05 s run is far too
   short for thermal steady state — `Whf` read only **452 W** while the devices dissipated ~2.7 kW, i.e. the
   junctions/thermal masses are still charging. For a valid **steady-state Tj** you must EITHER (a) run long
   enough for the thermal network to settle (impractical in the switched model), (b) compute Tj analytically:
   `Tj_ss = Ta + P_loss,per-switch × ΣRth` using the datasheet Cauer `R_th,JC` + your cold-plate Rth, OR
   (c) use the averaged model and reconcile per S6. Pick one and document it. (Efficiency is unaffected —
   electrical losses settle fast; only Tj needs the thermal timescale.)

### 1.2 Sum all 6 switches (don't ×6 one)
All 6 are coupled but **high-side (Q1/Q3/Q5) ≈240 W vs low-side (Q2/Q4/Q6) ≈172 W** conduction — a genuine
PF effect. Total conduction = **Σ all 6 = 1233 W**. Add the `PeriodicImpulseAverage` switching chain for at
least one high- and one low-side switch (or all 6) so the **total switching** is summed correctly, not
extrapolated from Q1. Also note raw-mean vs `PeriodicAverage` differ ~15 % — always use the averaged value.

### 1.3 Clean up the operating point
Phase current crest factor ≈ **1.8** (642 A pk / 357 A rms) — the current is distorted, which inflates
switching loss and makes η pessimistic. Modulation index sits at m≈0.987 (near the SPWM linear limit).
Try the demo's **SV PWM** controller config (`Controller` `Configuration` = 2; extends the linear range to
m≈1.15) for a cleaner sinusoid, and/or adjust the RL filter (`Lg`) or the fs:fac ratio. Re-verify Ia≈360 A rms.

### 1.4 Energy balance (S3)
Add an independent **Pout** measurement (AC output power) and confirm **Pin = Pout + Ploss within ±1 %**.
Today only Pin (Vdc·Idc) and Ploss (probe sum) exist. Options: probe the `3ph Meter` power bus, or capture
the 3 phase voltages × currents and average `Σ v·i` over an integer number of fundamental cycles.

---

## STEP 2 — Corner matrix (`procedure-simulation-and-validation` §4)

Run-validity gates first (**S1–S3**); a run that fails them is discarded, not reported.

- **S1 — Convergence:** halve the switched `MaxStep` (and tighten `RelTol`) until η changes < 0.1 pt and THD
  < 0.2 %abs between refinements; record the converged step. At `fs`=16 kHz resolve edges to **≤50–100 ns**.
- **S2 — Steady state + integer-cycle window:** ≥ 5 fundamental periods past startup (fac=200 → 25 ms; the
  0.05 s run is 10 periods, OK), then measure over an **integer** number of fundamental cycles only.
- **S3 — Energy balance:** Step 1.4.

**S4 — the 9 corners** (sweep `Vdc`/`Pr`/`Vg_rms` via `model_vars`; the launch corner, not peak power,
drives the thermal/ripple worst case):

| # | Test | Operating point | Pass criterion |
|---|------|-----------------|----------------|
| 1 | **Double-pulse** | 850 V, I≈Ipk (~424 A), Tj hot | Eon/Eoff extracted, vs datasheet [92]; Vds,pk ≤ ~83 % BV. *(Switching **energy** needs no coupling — a small separate DPT model is fine; Tj needs coupling.)* |
| 2 | **Efficiency** | {550, 750, 850} V × {peak, cont} | η ±1 pt of baseline; loss split ±10 %; energy-balanced |
| 3 | **Thermal/continuous** | 850 V, launch 300 A rms, Tcool=65 | Tj < 175 °C (needs the Step 1.1 thermal fix + steady-state Tj) |
| 4 | **DC-link ripple** | worst m/cosφ at launch | I_cap,rms < rating; ΔVdc < 1–2 % |
| 5 | **Overmodulation / six-step** | 550 V, MI > 0.907 | fundamental & THD vs field-weakening need |
| 6 | **Field-weakening sweep** | 750 V, speed 0→max | torque ~1/ω; Vd²+Vq² ≤ Vmax² |
| 7 | **Fault: short-circuit** | 850 V, shoot-through, Tj hot | fault current & I²t vs SCWT budget (< 3 µs SiC) |
| 8 | **Fault: ASC entry** | short all low-side at max speed | entry transient, drag torque, no bus overvolt |
| 9 | **Drive-cycle** | averaged model, WLTP/US06 | cycle-avg η; Tj history for lifetime |

Notes: the bench's natural point is the CRD (800 V / 360 A / 300 kW). The design note's own spec is
150 kW/300 A rms/750 V nom — decide which the efficiency corners target and be explicit. Corners 6–9 need
control/fault additions the current open-loop bench doesn't have yet (field-weakening, ASC, an averaged
model) — scope them as they come up.

**S5 — CRD calibration (the non-circular anchor):** at least one corner must match the **measured
Wolfspeed/TI 300 kW CRD** — **> 98 % η, 32 kW/L, 175 °C** — within **±1 pt η / ±10 % loss / ±10 % density**.
See [`reference-design-wolfspeed-ti-300kw-800v`](../../knowledge/notes/power-electronics/reference-design-wolfspeed-ti-300kw-800v.md).
The preliminary 99.1 % already clears >98 %; the job is to firm it up (Steps 1.1–1.4) and land a corner
inside the CRD tolerance.

**Cross-check** every PLECS number against the `experiments/*/` numpy models (family-car, microcar,
performance, truck) as an independent sanity bound.

**S6–S7:** averaged↔switched reconciliation (±10 %), then summarize to ~36 numbers and set
`system/configs/model_registry.json` 2L-B6 entry → `validation_status: validated`. Only then start the
Design-note / Fold-back / Close stages (and Track 2).

---

## Verified PLECS facts to carry forward

- **Readback:** `ToFile`→CSV (`simulate`'s `Values` is empty in 4.8). No header row written; `genfromtxt`
  gets clean floats. Set `Filename` absolute at run time via `set_component_param`.
- **Coupling is GUI-created, not scriptable** (doc-confirmed: PLECS 4.8 RPC = load/close/get/set/simulate/
  analyze/scope only). It survives text edits — retarget/instrument freely, but never text-delete/recreate
  the heat sink. Loss/Tj probing requires the device on an active heat sink.
- **Loss readback:** conduction → `PeriodicAverage`, switching (Dirac impulses) → **`PeriodicImpulseAverage`**,
  both `T_average=1/fac`. Signal names: `"Device conduction loss"`, `"Device switching loss"`,
  `"MOSFET junction temp"` / `"Device junction temp"` (both read 0 until the thermal-state fix). Heat sink:
  `"Temperature"` (also needs a Cth state to read).
- **Terminal maps:** `MosfetWithDiode` 1=drain 2=source 3=gate; `HeatFlowMeter` 1,2 thermal / 3 signal;
  `DCVoltageSource` 1=+ 2=−; averaging blocks input=2 output=1; `PlecsProbe` output=1.
- **`Rgon=4/Rgoff=0`** reproduce datasheet Eon/Eoff (the XML scales loss by Rg vs the Rg=4/Rg=0 reference).
- Full method + gotcha history: changelog `2026-07-21-plecs-2l-b6-bench-and-coupling` and memories
  `plecs-2l-b6-800v-bench`, `plecs-loss-readback-periodicimpulseaverage`.
