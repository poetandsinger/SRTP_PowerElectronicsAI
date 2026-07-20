# From-scratch CAB450 double-pulse test (Track-1, SOP corner 1)

`dpt_cab450_600v.plecs` — a from-scratch double-pulse test built headless to validate the
Wolfspeed **CAB450M12XM3** losses vs its datasheet. **Read `../HANDOFF.md` for the full status.**

## What works (headless, verified)

- Half-bridge leg of two **`MosfetWithDiode`** blocks (`file:CAB450M12XM3`, Rgon=4/Rgoff=0), 600 V,
  100 µH load, `Clock`→`Function` double-pulse gate.
- Builds, loads, simulates. **Current capture correct: 509 A peak ramp.**
- **Device dissipates correctly** — Voltmeter across the DUT gives Vds=1.83 V @ 509 A → **Ron=3.6 mΩ,
  exactly the CAB450 datasheet value**.
- **Loss/Tj readout solved:** a `PlecsProbe` with signal names **`"Device conduction loss"`,
  `"Device junction temp"`** → `ToFile` writes fine. (The earlier `"MOSFET …"` names were wrong and
  silently produced no output.)

## The one blocker (needs the GUI — see `../HANDOFF.md`)

Device→heatsink coupling does **not** reproduce from scratch-scripted `.plecs`: the heat sink stays
pinned at 25 °C while **Tj runs away to 684 °C** (adiabatic) and heat flow = 0. This persists even
with the buck-thermal demo's **byte-identical** HeatSink + device geometry. Root cause: the
device-on-heat-sink association is a **GUI-baked** thing (it survives text edits to a GUI-saved base —
see `../device_validation_buck/`). No headless workaround (the 4.8 RPC server has no save/add/connect).

**To finish:** open this file in the PLECS GUI, drag `Shigh` and `Slow` onto the `HS` heat sink until
they highlight as coupled, save. Then headless: run it and read `dpt_dev.csv` → validate Eon≈25.4 /
Eoff≈7.51 mJ (600 V, 450 A, 25 °C).

## Captures (ToFile → CSV, absolute scratch paths baked in — edit before reuse)

`dpt_cur.csv` (current) · `dpt_vds.csv` (Vds) · `dpt_loss.csv` (heat flow) · `dpt_dev.csv`
(device conduction loss, Tj, heat-sink temp).
