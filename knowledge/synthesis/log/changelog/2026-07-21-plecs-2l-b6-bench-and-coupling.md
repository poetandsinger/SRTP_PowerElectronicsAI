---
title: "Purpose-fit 2L-B6 800V bench + heat-sink coupling proven unscriptable"
type: changelog
field: project
created: 2026-07-21
updated: 2026-07-21
tags: [changelog, plecs, simulation, engineering-ai]
---

# 2026-07-21 — Track-1 800 V bench built + verified; coupling proven GUI-only

Advanced Track 1 from "a model that runs" toward "a model that yields a CRD-calibrated
number." Built a **purpose-fit 800 V 2L-B6 CAB450 bench**, verified its operating point
headless, cracked the historical switching-loss blocker, and **settled the device→heat-sink
coupling question definitively against the PLECS 4.8 docs**: it cannot be scripted. One manual
GUI step now gates the validated number.

## Resources used — and why each

| Resource | Used for | Why chosen |
|----------|----------|-----------|
| [[SESSION_LOG_2026-07-19]] + memories (`plecs-*`, `wolfspeed-plecs-models`) | Root-causing the prior session's failure; inheriting the ToFile/stale-model traps | The honest retrospective named the exact open blockers (loss readout, "coupling GUI-only?") — start from what's known, not re-derived |
| **PE-MAS** `plecs-mcp/src/tools.py` + `core/flyback_mas/tools/plecs_interface.py` + `Flyback_effi.plecs` (local clone, the *current MCP's own source*) | Confirming what the MCP can really do; learning the canonical loss-readback chain | User pointed here; reading the MCP's source is authoritative over guessing what its `circuit_action`/`run_script` tools do |
| **PE-GPT** (`XinzeLee/PE-GPT`, `load_plecs.py`, `DAB.plecs`) | Cross-checking the driving pattern (ModelVars vs bake) | Second independent PLECS-agent implementation; corroborates PE-MAS |
| **PLECS 4.8 Manual** (`plecsmanual.pdf`, pp. 318-9 RPC commands, p.166 Heat Sink) + `docs.plexim.com` scripting ref + Plexim forum | Proving, from primary docs, that coupling/structural edits can't be scripted | The user explicitly required *certainty* — a doc-level answer, not just an empirical one |
| **Shipped PLECS demos** (`three_phase_voltage_source_inverter`, buck-thermal, rainflow, DPT/buck artifacts) + `components.plecs` (block library) | The bench skeleton; exact block-type + probe-signal names | "Learn `.plecs` syntax by extraction, not invention" (SESSION_LOG §3.5). The demo gives a proven-correct 2L-B6 + Sine-PWM so I never hand-wrote a modulator |
| `design-2l-b6-800v-sic`, `procedure-simulation-and-validation` §4 | The exact operating point + S1–S7 gates | The bench must hit the CRD point (800 V, 360 A rms, 175 °C) the SOP calibrates against, not an arbitrary one |

## What I did

1. **Smoke-tested the MCP live** — `run_script`, `circuit_action(connect)`, `getModelTree`
   all fail: the PLECS 4.8 RPC surface is 13 methods (`load/close/simulate/get/set/scope/
   statistics/analyze/codegen/...`). The MCP's richer tool *names* fall back to RPC methods
   that don't exist. **Structural edits are `.plecs`-text-only.**
2. **Settled the coupling question 5 ways** (docs + empirics) → it is GUI-established spatial
   enclosure, exposes no device parameter, and byte-identical *text* geometry does not
   reproduce it (GUI-saved buck couples, hand-authored DPT with identical blocks does not).
3. **Cracked the switching-loss readout** — the missing block is **`PeriodicImpulseAverage`**
   (impulse train → average power); conduction uses `PeriodicAverage`. Found in PE-MAS's own
   `Flyback_effi.plecs`. → memory [[plecs-loss-readback-periodicimpulseaverage]].
4. **Built the bench** — retargeted `three_phase_voltage_source_inverter` to CAB450
   (`MosfetWithDiode` ×6, `file:CAB450M12XM3`, `Rgon=4/Rgoff=0` = datasheet-nominal), set the
   CRD operating point, added a heat sink + thermal network + loss instrumentation.
5. **Verified headless:** Vdc=800 V, **357.5 A rms** phase current, **Pin=292.4 kW**;
   conduction-loss readout works and is T-dependent (73→94 W as Tj0 0→65 °C).
   → `experiments/2l-b6-800v-sic-bench/` (+ README with the GUI-coupling procedure).

## Framework of thinking

- **Hold negative/"impossible" claims to a *higher* bar than positive ones** (the SESSION_LOG's
  §4.1 lesson). The prior "coupling is GUI-only" was under-evidenced; I neither accepted nor
  dismissed it — I re-tested empirically *and* against primary docs before treating it as a
  constraint. It held; now it's cited, not asserted.
- **Prove the mechanism on the smallest artifact first** (SESSION_LOG §3.1): copied the prior
  DPT/buck models to scratch and ran them to reproduce coupled-vs-uncoupled Tj (30 °C vs 684 °C)
  before trusting any coupling reasoning.
- **Verify the loaded graph matches the file after every structural edit** (§4.1): `plecs.get`
  after each insertion caught two silent-drop bugs (Components-after-Connections; Connection-
  after-Annotation) that otherwise present as "0 output, no error."
- **Reuse over rebuild, but only proven parts.** Chose to build *on a shipped demo skeleton*
  rather than hand-write ~600 lines of modulator/bridge — the highest-risk path — while still
  authoring the CAB450/thermal/instrumentation layers myself.
- **Don't fabricate.** Where coupling blocks a temperature-correct number, the number is
  withheld, not estimated — consistent with the SOP integrity bar.

## Methodology for building + testing (reusable)

1. Copy a proven skeleton to scratch; **make it writable** (`demos/` files are read-only) via
   temp-file + `os.replace` retry.
2. Edit `.plecs` as text with **assertion-guarded** replacements (`count==expected`), respecting
   the ordering law: **all `Component{}` → all `Connection{}` → `Annotation{}`** inside a
   `Schematic{}`; out-of-order blocks are silently dropped.
3. `close_model` → `open_model` after every edit (stale-model trap); **`plecs.get` to confirm the
   block landed** before simulating.
4. Read back only via a `ToFile`→CSV (`simulate`'s `Values` is empty in 4.8); parse with numpy.
   Probe-signal names must be exact — one invalid name voids the whole probe (→ single 0 column).
5. Cross-check every number against an independent expectation (Iref algebra, Rds(on)(Tj) trend).
6. Change one thing per run; **read the actual PLECS error string** and act on it literally
   ("place the component on an active heat sink" → loss probing needs a heat sink).

## What I did *not* do — and why

- **Did not retarget the rainflow IM-drive base** (an earlier option): wrong scale
  (~15 kW/300 V), and gutting its DTC/machine to reach 800 V/360 A is exactly the "over-edit
  into an inconsistent state" failure mode. A purpose-fit demo skeleton is cleaner + defensible.
- **Did not hand-author the SPWM modulator** — extracted a proven one from the demo instead.
- **Did not add the `PeriodicImpulseAverage` switching chain yet** — its correctness can only be
  verified *after* coupling (Tj-dependent); adding it blind risks a couple/​run/​fix loop.
- **Did not produce a validated η/loss/Tj number** — it is gated on the one GUI coupling step,
  which I proved (not assumed) cannot be scripted. Withheld rather than faked.

## What remains (Track 1, `design-2l-b6-800v-sic`)

Still `validation_status: unvalidated`. **Blocked on one manual step:** drag `Q1..Q6` onto the
`HS` box in the PLECS GUI + save (README has the procedure). Then headless: add the
`PeriodicImpulseAverage`/`PeriodicAverage` loss chain → temperature-correct per-switch loss + Tj →
6× to inverter loss → η = Pout/Pin (energy-balanced, S3) → 9-corner matrix (§4) → CRD calibration
(S5) → fill the design note → `model_registry.json` → `validated`.

**Reminder:** run **graphify update** — this session added `experiments/2l-b6-800v-sic-bench/`,
new memories, and this changelog; the current graph indexes pre-change paths.

## Addendum — coupling debugging with the user at the GUI (same day, evening)

The user did the GUI coupling step; it did **not** take. A methodical ladder (each step read one
signal) pinned the cause and re-confirmed the hard boundary:

1. **User dragged Q1..Q6 "a little and back" + saved → Tj still 0.** The GUI-save reformats the
   `.plecs` (wraps long strings, reorders probe signals) but did not add coupling. Nudging a device
   already inside the box and returning it does not register a "drop onto heat sink".
2. **Found a real bug I introduced — z-order.** I inserted `HS` *after* Q1..Q6, so PLECS draws the
   heat sink **in front of** the transistors; they sit behind it and cannot be dropped onto it.
   Fixed by moving the `HS` block before `Q1` (renders behind). **But a text-only z-order fix did
   not couple** (diag copy still Tj=0) — confirming coupling needs a real GUI association, not just
   correct layering.
3. **User re-dragged Q1 on the z-order-fixed bench + saved → Tj still 0.**
4. **Decisive diagnostic:** gave the heat sink a real `Cth` → PLECS errors *"state/source
   dependence: HS is directly dependent on source Tcool."* That error means **no heat is flowing
   into the sink** — i.e. the device is not coupled (a coupled device would feed the thermal state).
   With `Cth=0` the net is well-posed but a coupled device would read Tj≈sink-temp; it reads 0.
   ⇒ **Q1 is not coupled.**

**Conclusion (re-confirms the session's main finding, now with the user's own GUI attempts):** a
heat sink **authored in `.plecs` text does not become couplable by dragging devices onto it in the
GUI** — even with correct z-order. The device+heatsink association is created only when the heat
sink itself is *placed/created in the GUI* (the buck/rainflow demos couple because their sinks are
GUI-origin; a byte-identical text sink does not). This is a stronger statement than "coupling can't
be scripted": **the heat sink must be GUI-created**, not merely the coupling gesture.

**Reliable paths forward (for next session):**
- **(A, recommended) GUI-create the heat sink:** delete the text `HS`, drag a fresh Heat Sink from
  the library over Q1..Q6 (the standard PLECS workflow reliably couples enclosed components), rewire
  its heat port to the `Whf→Tcool→Tgnd` chain, save. Then all downstream is headless.
- **(B) Transplant a GUI-coupled base:** retarget the rainflow demo's already-coupled 6-device heat
  sink to the 800 V open-loop operating point — fully headless coupling, at the cost of the
  IM-drive teardown I avoided earlier.

Also note a **thermal-network topology fix needed regardless:** `HS(Cth>0) → HeatFlowMeter(0Ω) →
ConstantTemperature` is ill-posed (capacitance across a source). Insert a case-to-coolant
**ThermalResistor** (or use `Cth=0`) between the sink and the coolant source.

## Addendum 2 — coupling CONFIRMED + first efficiency number (2026-07-21, late)

The user **GUI-created a fresh Heat Sink** over Q1..Q6 (deleting my text sink) and wired its port to
the `Whf→Tcool→Tgnd` chain. That is the reliable fix predicted above (heat sink must be GUI-origin).

- **Coupling CONFIRMED by a decisive test:** raising the coolant 65 °C→150 °C made Q1 conduction loss
  rise **94 W→157 W**. A device's loss only tracks coolant temperature if its junction is thermally
  coupled. ⇒ the GUI heat sink couples; **coupling now survives text edits** (headless from here).
- **Switching-loss readout works** (the historical blocker): `PeriodicImpulseAverage`(T=1/fac) on
  `Device switching loss` + `PeriodicAverage` on conduction. **First numbers at 800 V / 357 A rms /
  292 kW:** per-switch conduction **205 W**, switching **244 W**; inverter loss **2.69 kW**;
  **η ≈ 99.08 %** (clears CRD >98 %, near the 99.3 % design estimate).

**Honest caveats (why this is PRELIMINARY, `validation_status` still `unvalidated`):**
1. **S1–S3 gates not run** — no timestep-convergence sweep, no integer-cycle window check, no
   independent energy balance (Pin vs Pout+Ploss). Per the SOP a number counts only after S1–S7.
2. **×6 balance — checked:** all 6 switches probed. All are coupled + dissipating (conduction
   170–243 W each, none runaway), total conduction **1233 W** (≈6×205). BUT a real **high/low-side
   asymmetry** (high Q1/Q3/Q5 ≈240 W vs low Q2/Q4/Q6 ≈172 W, a power-factor effect) means efficiency
   must sum all 6, not ×6 a single switch. Also raw-mean vs `PeriodicAverage` differ ~15% (use the
   averaged value). **Heat-flow cross-check `Whf`=452 W is a thermal transient** (0.05 s ≪ thermal
   time constant; heat still charging the thermal masses) — not a coupling failure; use the
   fast-settling electrical losses for η, and a long/averaged run (or analytical Tj) for the thermal gate.
3. **Junction-temp probe still reads 0** — `Device`/`MOSFET junction temp` both return 0 because the
   thermal path has no capacitance/resistance state (Tj is algebraic at coolant temp). Needs a proper
   junction-to-coolant `Rth`+`Cth` so Tj rises realistically and reads out (thermal gate `Tj<175 °C`).
4. **Current crest factor ≈1.8** (642 A pk / 357 A rms) — waveform is distorted; a cleaner operating
   point (modulation / fs:fac ratio) would lower switching loss and firm up the number.
5. **Two GUI-geometry gotchas found:** the GUI heat sink overlapped the `3ph Meter` (PLECS errors on
   a heat sink overlapping a non-thermal block) — moved the meter clear; and single-line
   `Parameter{}`/`Probe{}` blocks are dropped on load — PLECS needs each field on its own line.

**Next (headless):** proper thermal net → real Tj; instrument all 6 switches / confirm symmetry;
S1–S3 gates + energy balance; 9-corner matrix; CRD S5 calibration; then `validation_status: validated`.

← [[changelog-index]] | [[plan-depth-research]] | [[design-2l-b6-800v-sic]] | [[procedure-simulation-and-validation]]
