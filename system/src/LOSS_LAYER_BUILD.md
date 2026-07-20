# Loss/thermal layer — turn-key build recipe (Track 1: 2L-B6 SiC)

Upgrades the seed harness (`templates/2l_vsi_pmsm_tofile.plecs`, circuit-level only)
into a **datasheet-calibrated** SiC model that yields real efficiency, loss split,
and Tj — the layer that lets numbers count as evidence (SOP S5 / registry
`validation_status: validated`). Written 2026-07-19 from the PLECS 4.8 demo library;
**gated on real CAB450M12XM3 datasheet numbers** (do NOT fabricate loss tables).

## 1. The loss/thermal description is an XML file

PLECS stores a device's conduction + switching loss + Zth as a `.xml`
`SemiconductorLibrary` (schema v1.1). Reference template shipped with PLECS:
`demos/dual_active_bridge_converter/dual_active_bridge_converter_plecs/C3M0030090K.xml`
(a **Wolfspeed SiC MOSFET** — same class/vendor as our CAB450M12XM3). Structure:

```xml
<SemiconductorLibrary version="1.1">
 <Package class="MOSFET" vendor="Wolfspeed" partnumber="CAB450M12XM3">
  <Variables> Rgon, Rgoff </Variables>        <!-- external gate resistances -->
  <SemiconductorData type="MOSFET">
   <TurnOnLoss>
     <ComputationMethod>Table and formula</ComputationMethod>
     <Formula>E/(...at ref Rg...)*(...at Rgon...)</Formula>   <!-- Rg-scaling -->
     <CurrentAxis>...A...</CurrentAxis>
     <VoltageAxis> -100 0 400 600 800 </VoltageAxis>          <!-- include 800V -->
     <TemperatureAxis> 25 75 100 125 150 175 </TemperatureAxis>
     <Energy scale="0.001">   <!-- mJ; nested [Temperature][Voltage][Current] --></Energy>
   </TurnOnLoss>
   <TurnOffLoss> ... same shape (Eoff) ... </TurnOffLoss>
   <ConductionLoss>
     <ComputationMethod>Table only</ComputationMethod>
     <CurrentAxis>...A (neg for 3rd-quadrant/diode)...</CurrentAxis>
     <TemperatureAxis> -55 25 150 175 </TemperatureAxis>
     <VoltageDrop scale="1"> <!-- [Temperature][Current] Vds drop = Rds(on)*I --></VoltageDrop>
   </ConductionLoss>
  </SemiconductorData>
  <ThermalModel><Branch type="Cauer"> <RCElement R=".." C=".."/> ... </Branch></ThermalModel>
 </Package>
</SemiconductorLibrary>
```

**HAVE IT — use the official Wolfspeed PLECS model (local).** The full Wolfspeed model
library is now at `plecs_models/wolfspeed/` (see its README); the target is
`plecs_models/wolfspeed/mosfet-with-diode/modules/CAB450M12XM3.xml` (Version 4,
2026-03-19). It carries the **full E_on/E_off/E_rr 4-D surface — including 800 V at all
T_j** (VoltageAxis `[-10 0 600 800]`, TempAxis `25…200`), both conduction paths
(channel gate=on + body-diode gate=off), Rg-scaling custom tables (`Eon(Rg)`/`Eoff(Rg)`/
`Err(Rg)`, ref `Rgon=4`/`Rgoff=0`), and a 4-stage **Cauer** net summing to ≈0.095 °C/W
(= datasheet R_th,JC). This **resolves the datasheet's missing 800 V/175 °C switching
curve** — no hand-transcription needed. **Proven 2026-07-19:** copied into the harness
`_plecs/` folder and assigned (`therm=file:CAB450M12XM3`, `Rth`, `T_init=65`), the model
**loads and simulates cleanly on the library converter block** (the block accepts the
"MOSFET with Diode" class). The datasheet capture ([[wolfspeed-cab450m12xm3-datasheet]])
now serves to **bound/sanity-check** the model's output (SOP S5), not to build it.

**FALLBACK (only if the official model were unavailable) — hand-build from the datasheet** ([[wolfspeed-cab450m12xm3-datasheet]], [166]),
flagging every graph-read/approximation:
- **TurnOn/OffLoss Energy** ← E_on/E_off vs I_d. Tabulated at **600 V/450 A**: E_on
  25.4/24.0/24.4 mJ, E_off 7.51/8.10/8.35 mJ at 25/125/175 °C (~flat vs T_j). Linear-in-I:
  E_on≈0.056, E_off≈0.017 mJ/A at 600 V/25 °C. **800 V exists only at 25 °C** (E_on~45,
  E_off~22 mJ @450 A [graph]) — build the 800 V column from that × the flat-T_j behavior
  (approximation; flag). Ref R_g differs: 4.0 Ω @600 V, 5.0 Ω @800 V — keep separate; the
  `<Formula>` rescales for other R_g. VoltageAxis `[-100 0 600 800]`, TemperatureAxis
  `[25 125 175]`, CurrentAxis to ~900 A.
- **E_rr** ← 0.2/0.9/1.1 mJ at 25/125/175 °C (600 V), rises with T_j.
- **ConductionLoss VoltageDrop** ← R_DS(on) 2.6 mΩ@25 °C → 4.7 mΩ@175 °C (×1.81), Vds_drop
  = R_DS(on)·I; freewheeling uses the 3rd-quadrant channel (~R_DS(on) slope), not the
  4.7 V body-diode drop — model negative current with the same channel resistance.
- **ThermalModel** ← R_th,JC steady-state **0.094 °C/W**; the datasheet gives only the
  Z_th(j-c) transient curve (no R_i/τ_i) — a 4-stage Foster summing to 0.094 °C/W with τ
  ~1e-4…1e-1 s reproduces Fig 17 if the official XML is unavailable. Case-to-sink ≈0.08 °C/W [168].

Place the XML in a folder beside the model; reference it by basename with the
`file:` prefix (see §2).

## 2. Assign it — low-risk structural path (no hand-built bridge)

The seed's library **`2-Level IGBT Conv.`** block already exposes a **`therm`**
parameter (thermal description, currently `""`), an `Rth` (case→heatsink), a
`T_init`, and a thermal port. So **do not hand-author a 6-MOSFET bridge** (raw
`.plecs` geometry for 6 switches + DC link + 3-phase is error-prone).

> **RESOLVED 2026-07-19 (empirical):** the **IGBT converter block ACCEPTS a
> `MOSFET`-class `file:` description and simulates cleanly** — tested by assigning the
> shipped Wolfspeed SiC `file:C3M0030090K` + `Rth=0.05` to the seed converter; the run
> completed with no device-type error. So the low-risk path holds; a discrete-`Mosfet`
> bridge is **not** needed. **`file:` search path:** PLECS resolves `file:<Name>` from a
> **`<modelbasename>_plecs/` sibling folder** (the DAB-demo convention) — putting the
> XML next to the `.plecs` is NOT enough (gives "not found in search path"). Set params
> at runtime, then **close+reload** so the search folder registers.

Steps:
1. Drop `CAB450M12XM3.xml` into `<model>_plecs/` next to the `.plecs`.
2. Set the converter's `therm` parameter to `file:CAB450M12XM3` (via
   `set_component_param path=<model>/<conv> param=therm`), or an
   `InitializationCommands` var (DAB pattern: `device = 'file:...'`).
3. Set `Rth` (case→heatsink) and `T_init`=65 (coolant). The block's internal `Rth`+`T_init`
   give a thermal boundary without external heatsink wiring; for a richer network wire the
   thermal port to a `HeatSink` + case-heatsink `ThermalResistor` (DAB pattern). PLECS then
   reports per-device conduction + switching loss and Tj.

## 2b. Execution notes — build MOSFET-based, prefer from-scratch or interactive

Verified 2026-07-19 while attempting the discrete build headless (raw `.plecs` text +
RPC). Three distinct fragilities make **retargeting a complex demo headless unreliable**;
build the bridge **from scratch on an empty canvas** (deliberate coordinates, no inherited
couplings) or **interactively in the PLECS GUI** (see + fix the schematic):

1. **Geometry collisions** — inserting a block at a guessed coordinate, or into the wrong
   nested `Schematic`, throws *"Unconnected terminals overlapped"*. Insert only at the
   top-level schematic; on an empty canvas there is nothing to collide with.
2. **Block class** — `Igbt` and the library `2-Level IGBT Conv.` reject the CAB450 MOSFET
   description (§2). Use `Type Mosfet`.
3. **Probe-width coupling** — swapping `Igbt`→`Mosfet` changes a device's probe-signal set
   (e.g. `"IGBT junction temp"` → a MOSFET temp signal), so a demo's existing
   `PlecsProbe`→`Demux`→scope wiring breaks on a width mismatch. A from-scratch model has no
   such inherited wiring.

**`Mosfet` block terminal map** (from the DAB demo): terminal **1 = drain** (to +rail),
**2 = source** (to −rail / phase), **3 = gate** (signal in); a separate thermal port connects
to the `HeatSink`. `DCVoltageSource`: 1 = +, 2 = −. Connections are **by component name +
terminal index** (the `Points` are cosmetic), so a from-scratch netlist is deterministic once
the indices are known.

**Recommended first target: a single-leg switching-loss / double-pulse test** (SOP corner 1) —
DC source (test V) → load inductor → one `Mosfet` (CAB450) DUT, gate it, on a `HeatSink`;
read `SwitchLossCalculator`(DUT)→ToFile for Eon/Eoff/conduction loss and validate vs the
CAB450 tabulated values (`E_on 25.4 / E_off 7.51 mJ @600 V,450 A,25 °C`,
[[wolfspeed-cab450m12xm3-datasheet]]). Then replicate the leg ×3 for the full 2L bridge.
**Built: `data/plecs/dpt_from_scratch/dpt_cab450_600v.plecs`** (electrically complete).

### CORRECTED 2026-07-19 — the headless build DOES work (earlier "GUI-only" was a false negative)

An earlier version of this note claimed device→heat-sink coupling *needs the GUI*. **That was
wrong** — it was caused by a `.plecs` **syntax bug**: the generator emitted the `Frame` line
*after* the `Parameter` blocks, but PLECS requires `Frame` **immediately after `LabelPosition`**.
The malformed `Frame` made PLECS silently **remove the HeatSink** on load ("syntax error before
'Frame'" → "Removing component HS"), so the device had no heat sink and threw *"place the component
on an active heat sink"*. The user's GUI screenshot surfaced the real error.

**After fixing `Frame` placement, the from-scratch discrete DPT builds, loads, and simulates fully
headless** — heat-sink coupling by spatial enclosure **does** work from `.plecs` text. Two more fixes
were needed: (a) the device must be a **`MosfetWithDiode`** block, not `Mosfet` (plain `Mosfet`
*also* rejects gate-dependent conduction — only `MosfetWithDiode` matches the CAB450 "MOSFET with
Diode" class); (b) `Frame` must precede `Parameter`s in **every** block. Verified: `dpt_cab450_600v.plecs`
runs headless and captures the correct **509 A** double-pulse current ramp.

**UPDATE — root-caused; see `HANDOFF.md` for the authoritative status.** Two things resolved and
one real blocker isolated:
- **Loss/Tj readout SOLVED:** `PlecsProbe` writes fine with the **`"Device conduction loss"`,
  `"Device switching loss"`, `"Device junction temp"`** signal names (my earlier `"MOSFET …"` names
  produced no output — a generic-vs-typed naming split). Heat sink temperature = `"Temperature"`.
- **Device dissipates correctly:** a Voltmeter across the DUT gives Vds=1.83 V @ 509 A → Ron=3.6 mΩ,
  exactly the datasheet.
- **THE blocker — device→heatsink coupling is GUI-baked, not scriptable.** Authored from scratch, the
  device does not thermally couple to the heat sink (heat sink pinned at 25 °C, Tj runs away to
  684 °C, heat flow 0) — even with the buck demo's **byte-identical** HeatSink + device geometry. The
  GUI-saved buck demo *does* couple and the coupling *survives* text-swapping its device to CAB450
  (35.7 W, bounded Tj). No headless workaround (`plecs.saveAs`/`add`/`connect`/script-eval absent from
  the 4.8 RPC server). **Method: build the device-on-heatsink coupling once in the GUI, save, then
  retarget headlessly.** Full evidence + next steps: `HANDOFF.md`.

## 3. Retarget to the 800 V SiC operating point

- **Bus:** `V_dc` 355 → 750 V nom (corners 550 / 750 / 850 V).
- **Machine:** the `[T]` IPMSM params → a real datasheet/flux-map LUT when available
  ([[machine-and-load]]); until then keep `[T]` and flag it.
- **Operating point:** the seed runs a startup *speed ramp* (f_e≈5–17 Hz in 0.2 s) —
  set a **fixed speed + torque** so each corner sits at steady state ≥5 fundamental
  periods (SOP S2). Consider replacing hysteresis (Relay) control with SVPWM+FOC per
  [[procedure-control]] for the modulation corners (5, 6).
- **fsw:** 16 kHz per the design note.

## 4. Instrument for efficiency + loss + Tj (extend the ToFile mux)

Signals PLECS exposes once a thermal description is assigned (from the
`buck_converter_with_thermal_model` demo):
- **`PlecsProbe`** block → per-device junction temps: probe the switch/diode for
  `"IGBT junction temp"` / `"Diode junction temp"` (MOSFET analog) and the `HeatSink`
  for `"Temperature"`. This is how `Tj` becomes a signal.
- **`SwitchLossCalculator`** block → `ConductionLoss`, `SwitchingLoss`, `TurnOnLoss`,
  `TurnOffLoss`, `TotalLoss` as signals (the loss split S4/§4.2 needs).
- **DC ammeter** in series with `V_dc` (structural `.plecs` edit) → `I_dc`; `P_dc = V_dc·I_dc`.

Mux all into `cap_iabc`'s ToFile:
`[ia ib ic, va vb vc, I_dc, V_dc, P_cond, P_sw, Tj_sw, Tj_d, torque, speed]`.
`summarize.py` then computes η = P_ac/P_dc (inverter), loss split, THD_i, ripple, Tj —
the ~36-number summary (plan §4). Devices must sit on a `HeatSink` (or use the
converter block's internal `Rth`/`T_init`) for loss/Tj to compute.

## 5. Validate (SOP S1–S7) and register

Run the 9-corner matrix (`procedure-simulation-and-validation` §4.3), clear S1–S3
run-validity gates, **calibrate ≥1 corner to the measured Wolfspeed/TI CRD** (>98 % η,
360 A rms @ 300 kW scaled to our 150 kW, 175 °C — S5), then set the registry entry to
`validation_status: validated` and fill `design-2l-b6-800v-sic` with the numbers,
replacing every `[derived]`. Only then are they evidence.

## Structural fork — RESOLVED 2026-07-19 (empirical): the library converter block hides its losses

The library `2-Level IGBT Conv.` block **accepts** the CAB450 `MOSFET with Diode`
description and simulates, **but its per-device conduction/switching loss and Tj are NOT
externally readable**: a top-level `SwitchLossCalculator` probing the block (with `Path`
into the subsystem) returns **0** (it can't descend into the block's internal switches),
and a `PlecsProbe` on the block exposes only 1 trivial signal (also 0). So the block is
fine for *system* behaviour but **cannot back a loss/thermal-validated model** on its own.

**⇒ DEFINITIVE (2026-07-19): CAB450 requires a `Mosfet` block.** The CAB450 model has
**gate-dependent conduction** (`ConductionLoss gate="on"` + `gate="off"` — the SiC 3rd-quadrant
channel). An `Igbt` block **rejects** it at sim time: *"Gate dependent conduction losses are
not supported for this device type."* The library `2-Level IGBT Conv.` block is IGBT-type
internally — that is why it "ran" but reported **zero** loss. So the bridge must be built from
discrete **`Mosfet`** blocks (`Type Mosfet`, `thermal=file:CAB450M12XM3`,
`CustomVariables "struct('Rgon',4,'Rgoff',0)"`, `Ron=0.0036`), on a shared `HeatSink`. The
`SwitchLossCalculator`/`PlecsProbe` loss+Tj readout is confirmed to work on **discrete** switches
(the `buck_converter_with_thermal_model` demo reads its discrete switch's losses fine).

**⇒ Path for the validated build:**
1. **Discrete switches (recommended for a *validated* model).** Build the 3-phase 2-level
   bridge from 6 discrete `Mosfet` blocks, each with `therm=file:CAB450M12XM3`, on a shared
   `HeatSink`. Then `SwitchLossCalculator`/`PlecsProbe` read per-device loss split + Tj
   directly (needed for SOP corners 1-4: thermal, loss split). **Don't hand-author the
   geometry** — start from a PLECS demo that already has a discrete-switch 3-phase VSI +
   thermal + heatsink: `three_phase_grid_connected_pv_inverter` or `three_phase_t_type_inverter`
   (both in the thermal-demo set), and retarget device→CAB450, bus→800 V, load→IPMSM/300 kW.
2. **Thermal-port heat-flow (total loss only).** Wire the converter block's thermal port to
   a heat-flow meter → `HeatSink` at 65 °C; the meter reads total device loss (no cond/sw
   split, no per-device Tj). Cheapest, but insufficient for the thermal/loss-split corners.
3. **Energy balance (efficiency only).** Add a DC ammeter (P_dc=V_dc·I_dc) + 3-phase output
   power; η = P_ac/P_dc, loss = P_dc−P_ac. Robust for η (SOP S3) but no split/Tj.

Everything else is resolved: readback (ToFile→CSV), XML assignment + search path, and the
official CAB450 model loading+running. Loss/Tj signal wiring (`SwitchLossCalculator`,
`PlecsProbe`) is confirmed from `buck_converter_with_thermal_model` (§4) — it works on
**discrete** switches, which is why option 1 is the validated path.
