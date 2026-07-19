# PLECS Track-1 handoff — the device↔heatsink coupling blocker (2026-07-19)

For the next agent continuing [`plan-depth-research`](../../srtp_docs/plans/plan-depth-research.md).
Read this first, then `LOSS_LAYER_BUILD.md` and `SESSION_LOG_2026-07-19.md`.

## Where Track 1 stands: Step 1 (Model), blocked at ONE point

Everything is proven headless **except** device→heatsink thermal coupling:

| Piece | State |
|-------|-------|
| Readback (`ToFile`→CSV) | ✅ proven |
| Discrete `MosfetWithDiode` + CAB450 loads/simulates | ✅ proven |
| Double-pulse circuit + gate + current capture | ✅ proven (509 A ramp, correct) |
| Device **electrically** dissipates | ✅ proven (Vds=1.83 V @509 A → Ron=3.6 mΩ = datasheet) |
| Device **loss tables** compute | ✅ proven (conduction loss + Tj register via probe) |
| Loss/Tj **readout** | ✅ solved — `PlecsProbe` with **`"Device conduction loss"`, `"Device switching loss"`, `"Device junction temp"`** (NOT `"MOSFET …"`), routed to a `ToFile` |
| **Device→heatsink coupling** | ❌ **the blocker** — does not reproduce from scratch-scripted `.plecs` |

## The blocker, precisely (well-evidenced)

A `MosfetWithDiode` placed inside a `HeatSink` frame **does not thermally couple** when the
model is authored from scratch in `.plecs` text. Symptom: the device dissipates, but its heat
never reaches the heat sink — **heat-sink temperature stays pinned at 25 °C while Tj runs away to
684 °C** (adiabatic, no path out), and a `HeatFlowMeter` in the HS→ambient path reads **0 W**.

Ruled out (each tested):
- **Not a syntax error** — the model loads and runs; `Frame` is correctly placed (after `LabelPosition`).
- **Not the block type** — `MosfetWithDiode` is required (plain `Mosfet`/`Igbt` reject CAB450's
  gate-dependent conduction) and is used.
- **Not geometry** — I copied the buck-thermal demo's **exact** HeatSink block (byte-identical:
  `Cth 0`, frame `[-37,-52;37,52]`, HeatPort `[-57,15]`) and device positions (`[190,135]`,
  `[215,170]`). Still 0 coupling.
- **No explicit thermal terminal** — `MosfetWithDiode` has no terminal 4; wiring one is rejected.
- **Heat-sink→ambient path is fine** — the heat sink correctly sits at the 25 °C ambient.

**Root cause:** the device-on-heat-sink association is **created in the PLECS GUI (dragging the
device onto the heat sink) and baked into the saved file** in a form not reproducible by scripting
geometry. Proof it lives in the file and survives text edits: the shipped
`buck_converter_with_thermal_model` demo (GUI-saved) couples correctly, and when I text-swap its
`Igbt`→`MosfetWithDiode`+CAB450 **in place**, the coupling **survives** — CAB450 then reports
**35.7 W conduction loss with bounded Tj**. See `device_validation_buck/buck_cab450_ref.plecs`.

## The reliable method (this is the important takeaway for T1–T4)

**Do NOT author power stages with on-heat-sink devices from scratch.** Instead:
1. **In the PLECS GUI, once per topology:** build the power stage with its discrete
   `MosfetWithDiode` switches **dragged onto heat sink(s)**, save the `.plecs`.
2. **Then headless (RPC + text):** retarget the device (`thermal=file:<part>`, `Ron`, `Rgon/Rgoff`),
   set the operating point, add `ToFile` captures, run the corner matrix, read CSVs. The coupling
   survives — proven.

**A ready 2L-B6 base already exists — no GUI needed to start.** The shipped `rainflow_counting`
demo is a **3-phase 2-level VSI (6 IGBT + 6 diode) on a heat sink** driving an induction machine
(GUI-saved coupling). I retargeted it headlessly to CAB450 → `2l_b6_rainflow_base/2l_b6_cab450_rainflow.plecs`,
which **loads and simulates (`ok:true`)** with 6 CAB450 `Mosfet`s + body diodes. Key enabler: the
**legacy** CAB450 MOSFET file (`legacy-mosfets/`) is `class="MOSFET"` with no gate-dependent
conduction, so a plain `Mosfet` block accepts it (needs `CustomVariables "struct('Rgon',4,'Rgoff',0)"`).
**Open item:** the per-switch Tj/loss probe reads 0 (wrong signal name/path for the legacy device) —
must be confirmed before trusting it (see `2l_b6_rainflow_base/README.md`). This is the fastest route
to Step 5: fix the readout, retarget to 800 V, run corners, calibrate.

## Two artifacts in this folder

- `dpt_from_scratch/dpt_cab450_600v.plecs` — from-scratch CAB450 double-pulse test. Electrical +
  gate + current + loss-probe all work; **needs the 2 devices dragged onto the heat sink in the GUI**
  (or a GUI-saved base) to make the thermal path live. 600 V, ~450 A, validates Eon≈25.4/Eoff≈7.51 mJ.
- `device_validation_buck/buck_cab450_ref.plecs` — the buck-thermal demo with `Igbt` text-swapped to
  `MosfetWithDiode`+CAB450. **Coupling works** (inherited from the GUI-saved demo): 35.7 W conduction,
  bounded Tj. Proves the retarget-a-GUI-base method and that CAB450's loss model reads correctly.

## Next concrete steps to finish Step 1 → Step 5

1. **GUI (minutes):** open `dpt_from_scratch/dpt_cab450_600v.plecs`, drag `Shigh` and `Slow` onto the
   `HS` heat sink (until they highlight as coupled), save. OR build a 6-switch 2L-bridge base in the GUI.
2. **Headless:** run the DPT → read `dpt_dev.csv`; confirm Eon/Eoff/conduction vs datasheet
   ([[wolfspeed-cab450m12xm3-datasheet]]).
3. Scale to the full 2L-B6 bridge + 800 V + a defined operating point; run the 9-corner matrix
   (`procedure-simulation-and-validation` §4); **calibrate to the Wolfspeed CRD** (S5).
4. Fill `design-2l-b6-800v-sic`, fold back into `circuit-topologies` + agnostic notes, Red Team,
   set `model_registry.json` → `validation_status: validated`. Only then start T2.

## Verified PLECS facts to carry forward (save re-discovery)

- Readback: `ToFile`→CSV (simulate's `Values` is empty in 4.8). No header row written.
- After any `.plecs` edit: `close_model` then `open_model` (stale-model trap). Verify a new block
  landed with `get_component_param` — `load` returns `ok:true` even when it silently drops a
  malformed component.
- Sim duration = model `TimeSpan` (the `simulate` `stop_time` arg is ignored).
- `file:<part>` resolves from a `<modelbasename>_plecs/` sibling folder; must exist before load.
- Loss/Tj probe signal names: **`"Device conduction loss"`, `"Device switching loss"`,
  `"Device junction temp"`**; heat sink: `"Temperature"`. The switching-loss signal is an impulse a
  `ToFile` won't serialize — capture conduction + Tj continuously; get switching **energy** from a
  properly-configured `SwitchLossCalculator` (its empty `Signals{}` in scripted mode sums to 0 — it
  likely needs GUI signal selection, an open sub-item).
- Terminal maps: `MosfetWithDiode` 1=drain 2=source 3=gate (no thermal terminal); `Ammeter`/`Voltmeter`
  1,2 power / 3 signal; `HeatFlowMeter` 1,2 thermal / 3 signal; `DCVoltageSource` 1=+ 2=−.
