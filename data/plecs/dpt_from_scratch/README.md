# From-scratch CAB450 double-pulse test (Track-1, SOP corner 1)

`dpt_cab450_600v.plecs` — a from-scratch double-pulse test built **fully headless** (2026-07-19,
raw `.plecs` text + XML-RPC) to validate the Wolfspeed **CAB450M12XM3** switching/conduction losses
against its datasheet — the foundational loss validation for the 2L-B6 SiC build
([[design-2l-b6-800v-sic]]).

## What it is

A half-bridge leg of two **`MosfetWithDiode`** blocks (both `file:CAB450M12XM3`, Rgon=4/Rgoff=0):
- **Vdc** 600 V (the datasheet's tabulated switching-loss condition), stiff source.
- **L** 100 µH from DC+ to the switch node (`di/dt = 6 A/µs`).
- **Shigh** freewheel (gate = 0 → body diode freewheels); **Slow** = DUT.
- **Gate** = `Clock`→`Function` double pulse: ON `[5,80] µs` (ramp to ~450 A) then `[90,100] µs`.
- Both devices enclosed in a `HeatSink` frame → `HeatFlowMeter` → `ConstantTemperature 25 °C` → `ThermalGround`.
- `Ammeter`(L) → ToFile (`dpt_cur.csv`); `HeatFlowMeter` → ToFile (`dpt_loss.csv`).

## Status (verified headless)

- ✅ **Builds, loads, and simulates fully headless** — no GUI step needed.
- ✅ **Current capture correct**: 509 A peak double-pulse ramp.
- ✅ Heat-sink coupling by **spatial enclosure works from `.plecs` text** (device inside the
  HeatSink `Frame`) — contradicting an earlier (wrong) conclusion; see below.
- ❌ **Loss readout reads 0** — the one open blocker (see below).

## Three fixes that were needed (each a real PLECS gotcha)

1. **`Frame` placement.** `Frame` must come **immediately after `LabelPosition`**, *before* the
   `Parameter` blocks. Emitting it after the parameters gives *"syntax error before 'Frame'"* and
   PLECS **silently removes the component** on load. This bug removed the HeatSink, which produced
   the misleading *"place the component on an active heat sink"* error and my earlier false
   conclusion that heat-sink coupling needs the GUI. **It does not.**
2. **Block type.** The CAB450 model is class `"MOSFET with Diode"` (gate-dependent conduction). It
   requires a **`MosfetWithDiode`** block. Both `Igbt` *and plain* `Mosfet` reject it
   (*"Gate dependent conduction losses are not supported for this device type"*), and the library
   `2-Level IGBT Conv.` is IGBT-type internally.
3. **Search path.** `file:CAB450M12XM3` resolves from the `<basename>_plecs/` sibling folder
   (`dpt_cab450_600v_plecs/`); the folder must exist before load (close+reopen after adding it).

## The open blocker: loss readout = 0

The device conducts 450 A but the measured loss is 0 W. Attempts:
- `SwitchLossCalculator` (empty `Signals{}`, buck-demo config) → writes to ToFile but outputs **0**.
- `PlecsProbe(Slow, {"MOSFET conduction loss","MOSFET switching loss","MOSFET junction temp"})` →
  **writes no CSV** (the switching-loss signal is a Dirac impulse a `ToFile` won't serialize; even
  dropping it to conduction+Tj, a probe→ToFile still won't write).
- `HeatFlowMeter` in the HS→ambient thermal path → writes, but reads **0 W**.

Root cause unresolved. Likely one of: the loss isn't being injected into the measured thermal path,
the `SwitchLossCalculator`/`PlecsProbe` needs signal-set configuration only doable in the GUI, or a
thermal-wiring detail. **This is the single thing standing between "the model runs" and a real
Eon/Eoff/Tj number.** See `../LOSS_LAYER_BUILD.md` §2b.
