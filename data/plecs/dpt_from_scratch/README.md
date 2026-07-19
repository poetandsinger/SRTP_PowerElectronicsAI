# From-scratch CAB450 double-pulse test (Track-1, SOP corner 1)

`dpt_cab450_600v.plecs` — a from-scratch double-pulse test built headless (2026-07-19) to
validate the Wolfspeed **CAB450M12XM3** switching energies (Eon/Eoff) against its datasheet,
the foundational loss validation for the 2L-B6 SiC build ([[design-2l-b6-800v-sic]]).

## What it is (electrically complete)

A half-bridge leg of two `Mosfet` blocks (both = `file:CAB450M12XM3`, Rgon=4/Rgoff=0):
- **Vdc** 600 V (the datasheet's tabulated switching-loss condition), stiff source.
- **L** 100 µH load inductor from DC+ to the switch node (`di/dt = 6 A/µs`).
- **Shigh** freewheel (gate held at 0 → body diode freewheels); **Slow** = DUT.
- **Gate** = `Clock`→`Function` double pulse: ON `[5,80] µs` (ramp to ~450 A) then `[90,100] µs`;
  turn-**off** at 80 µs ≈ 450 A, turn-**on** at 90 µs — the datasheet's 450 A point.
- `SwitchLossCalculator`(Slow) + `Ammeter`(L) → `SignalMux` → `ToFile` (`dpt_out.csv`) for readback.
- Devices sit in a `HeatSink` frame → `ConstantTemperature` 25 °C → `ThermalGround`.

The **electrical netlist is valid** — the model loads and simulates up to the thermal check.

## The one step it needs (GUI) — then it's fully drivable headless

**Blocker found:** PLECS couples a semiconductor to a heat sink by a **GUI association**
(dragging the device onto the heat sink), NOT by `.plecs` coordinates. Verified headless: even
with the two Mosfets geometrically dead-center inside a huge HeatSink `Frame`, and with an
explicit thermal-terminal connection attempt, PLECS still errors *"place the component on an
active heat sink"* — loss/Tj probing is impossible without the GUI step. (The device's
switching energy lives only in the thermal loss tables; PLECS switches ideally in the electrical
domain, so integrating Vds·Id gives ~0 — the table-based Eon/Eoff is only readable via the
heat-sink-coupled probe.)

**To finish (≈1 min in the PLECS GUI):** open this model, delete the scripted `HeatSink`, drop a
Heat Sink block from the library, and drag `Shigh` and `Slow` onto it (so they highlight as
coupled); keep the `ConstantTemperature 25` on its port. Save. **Then everything else is headless:**
`run_harness.py`-style RPC drives the sim, and `dpt_out.csv` gives conduction + switching loss vs
the `Ammeter` current — validate Eon≈25.4 mJ / Eoff≈7.51 mJ at 450 A, 600 V, 25 °C
([[wolfspeed-cab450m12xm3-datasheet]]). Replicate the leg ×3 for the full 2L bridge.

See `../LOSS_LAYER_BUILD.md` §2b for the full recipe and the headless-vs-GUI boundary.
