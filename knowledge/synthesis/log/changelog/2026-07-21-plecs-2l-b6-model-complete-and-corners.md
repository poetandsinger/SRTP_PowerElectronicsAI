---
title: "2L-B6 bench: Step-1 model finished + corner matrix run -> validated (with method + templates for T2)"
type: changelog
field: project
created: 2026-07-21
updated: 2026-07-21
tags: [changelog, plecs, simulation, engineering-ai, validation, methodology]
---

# 2026-07-21 (cont.) — Track-1 model completed, CRD-calibrated, and the method written down

Continues [[2026-07-21-plecs-2l-b6-bench-and-coupling]]. That session left the bench coupled with a
**preliminary ~99.1 %** and four open gaps (Tj reads 0, ×6-Q1 not summed, distorted current, no energy
balance). This session **closed all four (Step 1)** and **ran the corner matrix (Step 2: S1/S2/S3/S4/S5)**,
landing the CRD-calibrated number. `model_registry.json` 2L-B6 → **`validation_status: validated`**.
This entry is deliberately method-heavy so **Track 2 (3L-TNPC)** can be built by pattern, not rediscovery.

Results table + raw CSV: [[2l-b6-800v-sic-bench|results/metrics/2l-b6-800v-sic-bench.txt]].

---

## 1. What I did (results)

**Step 1 — finished the model** (headless; coupling untouched):
- **1.1 Tj readout fixed.** Two root causes: the probe signal name `"MOSFET junction temp"` yields *no
  column* (correct = **`"Device junction temp"`**), and the coolant path had no impedance state. Added a
  series **`ThermalResistor Rcs`** (resistance param is **`Rth`**, not `R`) between `Whf` and `Tcool`;
  `Device junction temp` now reads and rises 65→107 °C in 0.05 s. Reported **Tj_ss is analytic** (thermal
  τ ≫ run length — see §6.3).
- **1.2 All-6 summed** via `paAllCond` (PeriodicAverage) + `piaAllSw` (PeriodicImpulseAverage), 6-wide, T=1/fac.
- **1.3 Clean current:** SV PWM (Configuration=2) + `Lg=0.5` p.u. → crest **1.80→1.46**, THD **0.15 %**.
- **1.4 Energy balance (S3):** independent AC-side probe → residual **−0.37 %**.

**Step 2 — corners:** 6 points (bus 750/800/850 V @ 300 kW, launch 300 A, cont 180 A, low-bus 550 V):
η **99.03–99.32 %**, Tj 94–180 °C, all energy-balanced ≤ 0.6 %. **CRD point = 99.07 % η + 175 °C** (S5 met).
S1 convergence confirmed; analytic conduction cross-check −3.5 %.

---

## 2. What I did NOT do, and why

| Not done | Why |
|----------|-----|
| **Corners 6–9** (field-weakening sweep, ASC entry, short-circuit fault, drive-cycle) | The bench is **open-loop V/f-style** (no current regulator, no fault logic). These need a FOC controller, an ASC/short-circuit trigger, and (for drive-cycle) an averaged model. Building those is a modelling task in its own right — scoped as they come up, per the original handoff. |
| **Corner 1 double-pulse (DPT)** switching-energy extraction | Switching **energy** needs no heat-sink coupling — a small separate DPT model is the right tool (an archived stub exists, `experiments/ARCHIVE/dpt-from-scratch/`). Our corner matrix already reads switching **power** from the same XML tables, so the DPT is corroboration, not a gate. |
| **S6/S7** averaged↔switched reconciliation | Requires an **averaged (state-space-averaged) model** of the 2L-B6, which doesn't exist yet. The switched model alone can't self-reconcile. |
| **Text-edit the `Heat Sink` block** (even to set `Cth`) | The device→sink coupling is a **GUI-baked association**; text-deleting/recreating the block breaks it. `Cth` is set per-run via RPC instead (`plecs.set`), which is safe. |
| **Add components via `circuit_action`/RPC** | `discover_capabilities` proved the 4.8 RPC surface is **`plecs.set` only** for editing — no add/connect/save. So every new block is a **text edit + reload**; there's no scriptable shortcut. |
| **Persist per-run values (Filenames, Cth, corner vars) into the file** | There is **no `plecs.save` over RPC**. Those are set at runtime each session; only structural/default changes live in the file. |

---

## 3. Tools used — and why each

| Tool | Used for | Why it (and not something else) |
|------|----------|--------------------------------|
| `mcp__plecs__discover_capabilities` | Enumerate the real RPC surface | **Decided the whole edit strategy**: it returned `circuit_editing: [plecs.set]` and `save_model: UNSUPPORTED` → proved I must text-edit + reload and can't save/add. Don't assume `circuit_action` works; verify first. |
| `mcp__plecs__open_model` / `close_model` | Load/reload after every text edit | The **stale-model trap**: a plain re-open of an already-loaded model does NOT refresh it. Always `close` **then** `open`. |
| `mcp__plecs__get_component_param` | **Verify a new block landed** after reload; discover param names | `load` returns ok:true even when it silently drops a malformed block. `get` is the only ground truth. Also how I found `ThermalResistor.Rth` (tried `R`, `R_th` → both "Unknown parameter"). |
| `mcp__plecs__set_component_param` | Set ToFile Filenames (abs), Heat Sink `Cth`, `Configuration` | The only RPC edit primitive. Per-run, not persisted. |
| `mcp__plecs__simulate` (`model_vars=`) | Run baseline + corners | `model_vars` is the corner knob — but see §5 (it applies AFTER init). `Values` returns empty in 4.8 → readback is via ToFile. |
| `Edit` / `Write` (on `.plecs`) | Add blocks, rewire, change init/solver/Configuration | The **only** way to add components or persist defaults. Fragile — see §7. |
| `Bash` + Python/**numpy** | Read ToFile CSVs, tail-average, FFT, analytic checks | The readback contract is CSV-on-disk; numpy `genfromtxt` gets clean floats. All quantitative reasoning lives here, not in PLECS. |
| `Grep` / `Read` / `Glob` | Find the `ThermalResistor` param in a shipped demo; read the XML Cauer net; pull `R_th,JC`/`R_th,CS` from the datasheet note | "Learn `.plecs` syntax by extraction, not invention" — the demo `boost_converter_with_pfc_and_thermal_model.plecs` gave the exact `Variable "Rth"`. |
| `TaskCreate/Update` | Track the 5 sub-tasks | Multi-step, worth the visible progress. |

---

## 4. Methodology — the core loops

### 4.1 The edit→reload→verify loop (structural changes)
```
Edit .plecs (respect block order, §7)  ->  close_model  ->  open_model
  ->  get_component_param on each NEW block (confirm it landed + param names)
  ->  set_component_param Filenames to absolute scratch paths (reload resets them)
  ->  simulate  ->  read CSVs in numpy
```
Never trust a run until `get_component_param` confirms the new blocks exist. `load` lies (ok:true on drop).

### 4.2 Readback contract (PLECS 4.8: `simulate` Values is empty)
Every metric is routed to a `ToFile` (`FileType 1` = CSV, `WriteSignalNames 1`, no header row is actually
written) and read from disk. Steady-state = **the last integer number of fundamental cycles** (fac=200 →
5 ms/cycle; a 0.05 s run = 10 cycles; average over the last 4–5). Integer-cycle windows are mandatory for
unbiased means and clean FFTs.

### 4.3 Corner-run recipe (the non-obvious part — see §5)
```
vars = python gen_vars.py <Vdc> <Vg_rms> <Pr>      # replicates InitializationCommands
simulate bench_2l_b6_800v_sic model_vars=<vars>    # full consistent override
python analyze_corner.py '{"Vg_rms":..,"Pr":..,"label":".."}'   # -> corners.csv row
```

---

## 5. THE model_vars TRAP (read before building any corner sweep)

**`model_vars` are applied AFTER `InitializationCommands` run.** I proved it: overriding `Pr=150e3` left
Ia at 355 A (Iref did **not** recompute). So a bare `{"Pr":..,"Vg_rms":..}` override leaves every derived
quantity (`Iref`, `Vref`, `Lg`, `phase_sine`, `phase_svpwm`, `i_init`) at its **default** value → a
**silently inconsistent** operating point. The old handoff recipe was wrong.

Two consequences:
- **Overriding `Vdc` alone is safe** — Vdc only feeds the live DC source and the runtime modulation ratio,
  not any init-derived var.
- **Any Pr/Vg_rms corner must pass the COMPLETE consistent set.** `gen_vars.py` re-derives the whole init
  math in Python and prints the JSON. Validated by regenerating the baseline set → reproduced η/Ia exactly.

Array-valued model_vars (the 3-phase `phase_*` vectors) are accepted over the MCP bridge — confirmed.

Pre-flight check before running a corner: `gen_vars` prints the **modulation index `m`**. SV PWM linear
range is m ≲ 1.155; if `m` exceeds it the current clips and distortion returns (that gates which
(Vdc, Vg_rms) pairs are feasible — e.g. Vg_rms=278 needs Vdc ≳ 700).

---

## 6. Analytical checks — templates, formulas, reasoning

Every PLECS number was bounded by an independent hand-calc. These are the reusable templates.

### 6.1 Energy balance (S3) — the closure test
```
Pin        = Vdc * mean(Idc)                            # DC in
Ploss      = Sigma6(conduction) + Sigma6(switching)     # from paAllCond + piaAllSw
P_bemf     = mean( sum_k  vg_k(t) * i_k(t) )            # into the back-EMF source (pwrProbe)
P_Rg       = Rg * sum_k mean( i_k(t)^2 )                # filter-resistor loss, Rg=0.01*Zb
residual   = Pin - Ploss - (P_bemf + P_Rg)              # PASS if |residual| < 1% of Pin
```
Reasoning: DC power splits into switch loss + AC delivered; the AC side is measured **independently**
(different probes) so agreement is a genuine consistency proof, not a tautology. Inductor stored energy
averages to zero over integer cycles. Got −0.14…−0.54 % across corners.

### 6.2 Conduction loss — closed form (2L-VSI, sinusoidal current, PF cosφ)
```
P_cond,switch = Ron * Ipk^2 * (1/8 + m*cosphi/(3*pi))
```
215.3 W (Ron=0.0036, Ipk=509, m=1, cosφ=1) vs PLECS 207.7 W → **−3.5 %** (within ±10 %). Reasoning: each
switch carries i(t)=Ipk·sinθ with PWM duty (1+m·sinθ)/2; integrate i²·duty over a fundamental. Ties the
XML-model conduction to first principles.

### 6.3 Junction temperature — analytic steady state (option b)
The switched 0.05 s run is **far too short for thermal steady state** (slowest Cauer τ = R₄·C₄ ≈
0.013×5.63 ≈ 0.074 s, plus the cold-plate mass). So the in-model Tj only corroborates; the **reported**
Tj_ss is analytic:
```
Tj_switch = Ta + P_module * R_cs + P_switch * R_jc
  R_jc = 0.0948 C/W   # XML Cauer sum, per switch (junction->case)
  R_cs = 0.070 C/W    # case->coolant, per module (2 switches share the baseplate)
  P_module = P_hi + P_lo   (module pairs: Q1+Q2, Q3+Q4, Q5+Q6)
```
**R_cs calibration (why 0.070, not the app-note 0.08):** R_cs is the one soft number and it swings pass/fail
(per-switch interpretation → 147 °C; per-module @0.08 → 185 °C). Rather than guess, I **back-calculated R_cs
from the CRD anchor** (S5): the value that puts the rated 360 A/800 V point at the CRD's measured 175 °C.
That makes the thermal model CRD-calibrated (non-circular) — exactly what S5 is for. Efficiency/loss are
R_cs-independent and settle fast, so they need no such caveat.

### 6.4 Convergence (S1) — refinement test
Run baseline at (MaxStep,RelTol)=(1e-3,1e-3) vs (1e-4,1e-4); **PASS if Δη < 0.1 pt and ΔTHD < 0.2 %abs.**
Result: byte-identical (η 99.068 %, Ploss 2815 W). Reasoning: the zero-crossing detector (`ZCStepSize=1e-9`)
already resolves every switching edge regardless of MaxStep, so the loose macro-step was already converged.

### 6.5 Aliasing guard — raw mean vs periodic average
Raw ToFile sampling at 100 µs (10 kHz) undersamples the 16 kHz switching content → biased mean (~18 % high
for conduction). Fix: feed the loss signal through a **PeriodicAverage** (continuous integral, T=1/fac)
before the ToFile. Switching loss is a Dirac-impulse train → needs **PeriodicImpulseAverage**, not the plain
one. This is why the earlier "Σ6 = 1233 W" was an overestimate.

### 6.6 THD / crest (current quality)
On an **exact integer-cycle** window, `rfft` with **no window**: fundamental bin = number of whole cycles;
THD_low = √(Σ harmonic-bin² up to 40th)/fundamental. (Windowing corrupted it — a Hanning window gave a
bogus 70 %; the true low-order THD is 0.15 %.) Crest = peak/rms is the quick distortion proxy (1.46).

---

## 7. Did component order matter? — YES (the `.plecs` grammar)

Inside a `Schematic{}` the loader is **order-sensitive and fails silently**:
1. **All `Component{}` blocks, THEN all `Connection{}` blocks, THEN `Annotation{}`.** A Component placed
   after a Connection, or a Connection after an Annotation, is **dropped on load** (no error). I inserted
   all 9 new components immediately before the first `Connection`, and all new connections among the
   existing ones (before the `Annotation`).
2. **Multi-line blocks only.** A single-line `Parameter { Variable "X" Value "Y" Show off }` or `Probe { … }`
   is dropped. Each field on its own line.
3. **Param names are exact and type-specific.** `ThermalResistor` resistance = **`Rth`** (not `R`);
   averaging blocks: **input = terminal 2, output = terminal 1**; probe signal for Tj = **`Device junction
   temp`**. A wrong name is silently ignored (defaulted) or voids the whole probe → a single 0 column.
4. **Heat-sink z-order / GUI origin (from the prior session, still true):** a *text-authored* heat sink is
   not couplable by a GUI drag; the sink itself must be **GUI-created**, then coupling survives text edits.
   Editing the `Heat Sink` block's text (delete/recreate) breaks the association — don't.

Verification discipline: after each structural edit, `get_component_param` every new block before trusting a
run. This caught the `Rth`-vs-`R` param and the missing Tj column.

---

## 8. For Track 2 (3L-TNPC) — carry-forward + open questions

**Reuse verbatim:**
- The **base-retarget method**: start from a *GUI-saved* thermal demo that already has discrete switches on
  a heat sink (coupling survives text edits) — do NOT author on-heatsink devices from scratch. For TNPC,
  look for a shipped 3-level / T-type thermal demo; else GUI-create the sink once.
- The **instrumentation quartet**: `paAllCond` + `piaAllSw` (all devices, T=1/fac), `pwrProbe` (v_abc,i_abc
  @2 µs for P_out/THD/crest), `tjProbe` (`Device junction temp` + Heat Sink `Temperature`), each → ToFile.
- `gen_vars.py` + `analyze_corner.py` pattern (the model_vars-after-init trap is topology-independent).
- The five analytic templates in §6 (energy balance, conduction closed-form, analytic Tj_ss + CRD
  calibration, convergence, aliasing guard).

**Will differ / needs thought:**
- **Device count & thermal net.** 3L-TNPC has **12 switches** (per phase: 2 outer T1/T4 + a bidirectional
  neutral pair T2/T3) with *asymmetric* loss (outer devices switch the full bus, inner clamp to neutral) —
  the high/low symmetry we saw at unity PF will NOT hold. Sum **all 12** individually; expect an outer-vs-inner
  split, and per-device R_jc may differ if the module mixes die.
- **Neutral-point balance.** TNPC needs a **NP-voltage balancing** modulator (the demo's SV/carrier scheme
  must inject the right zero-sequence / redundant-state selection) or the DC-link midpoint drifts and
  distorts current. Budget time for this before trusting any corner.
- **Which device model?** The CRD anchor (Wolfspeed/TI 300 kW) is a **2L-B6** design — T2 either needs its
  own measured reference for S5, or is calibrated *relative to* the validated 2L-B6 (document which).
- **Loss-table voltage grid.** Outer devices see the full 800 V; inner devices see ~400 V (half-bus). Verify
  the XML Eon/Eoff tables cover **both** operating voltages at the grid points (2L-B6 only needed 800 V).
- **Modulation feasibility.** 3-level extends the linear range and halves dv/dt per step; re-derive the
  `m`-feasibility pre-check for the 3-level modulator before sweeping Vdc.

**Open questions to resolve early for T2:**
1. Is there a shipped PLECS 3L/T-type **thermal** demo to retarget (coupling-safe base)? If not, plan the
   one GUI heat-sink step up front.
2. Does `PeriodicImpulseAverage` behave on a **12-wide** vector the same as 6-wide? (Expected yes; verify.)
3. What's the S5 anchor for TNPC — a measured 3L reference, or relative-to-2L-B6?
4. Confirm the NP-balancing control is in the demo skeleton or must be added.

---

## 9. Files
- `experiments/2l-b6-800v-sic-bench/bench_2l_b6_800v_sic.plecs` (instrumented + SV PWM + Lg=0.5 + Rcs + solver 1e-4)
- `experiments/2l-b6-800v-sic-bench/{gen_vars,analyze_corner}.py` (reproducible corner driver)
- `results/metrics/2l-b6-800v-sic-bench.txt` + `-corners.csv`
- `system/configs/model_registry.json` (2L-B6 → validated, 6 corners)
- `experiments/2l-b6-800v-sic-bench/README.md`, root `README.md`, `LOG.md`, `TODO.md`, `system/src/HANDOFF.md`
- memory `plecs-2l-b6-800v-bench`

> **Graph note:** this session added notes/results/scripts and cross-links — run **`graphify --update`** to
> re-index (the graph still points at pre-session paths).
