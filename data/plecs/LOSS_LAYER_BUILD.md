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

## Open structural question to resolve during the build
- Does the library **IGBT** converter accept a `MOSFET`-class `file:` description? If it
  rejects it, switch to a MOSFET 2-level converter block, or build the bridge from
  discrete `Mosfet` blocks (the DAB demo's approach) each referencing the XML. This is
  the one remaining unknown — everything else (loss/Tj signal names, readback, XML
  schema, assignment) is resolved above. Probe/loss signal names confirmed from the
  `buck_converter_with_thermal_model` demo (§4).
