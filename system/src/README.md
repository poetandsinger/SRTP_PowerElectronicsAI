# PLECS harness (`data/plecs/`)

Runnable harness that turns a `.plecs` model into numbers, per
[`plan-plecs-harness`](../../srtp_docs/plans/plan-plecs-harness.md) and the
validation SOP
([`procedure-simulation-and-validation`](../../srtp_docs/notes/power-electronics/procedure-simulation-and-validation.md) §1, §4).

## The readback contract (verified 2026-07-19, PLECS 4.8 Standalone, port 1080)

`plecs.simulate` returns an **empty** `{Time, Values}` in this build — even with a
top-level `Output` block wired to a live signal (tested on a minimal
`SineGenerator→Output` model *and* the real 2L-VSI+PMSM model, via the MCP tool
and direct RPC). **This corrected the earlier "Values only from top-level Outport"
assumption.**

The working path is a **`ToFile` block that writes a CSV to disk**, read back with
numpy:

- `ToFile` params: `FileType=1` (CSV), `WriteSignalNames=1`, `SampleTime=-1`
  (log every solver step; set a number to decimate), `Filename`=absolute path
  (`Evaluate off`). Mux multiple signals into its single input (terminal 1).
- CSV layout: **col 0 = Time, cols 1..N = the muxed signals in mux order**. No
  header row is written despite `WriteSignalNames=1`, so `np.genfromtxt` sees
  clean floats.
- This is how PE-MAS reads results (`plecs_interface.py`); it treats
  `simulate`'s `Values` as an unreliable bonus.

### Two traps

1. **Stale model.** After editing a `.plecs` on disk, `plecs.load` on an
   already-open model of the same name does **not** refresh it — you keep
   simulating the old graph (a new block yields "Invalid component path", no CSV).
   **Always `close` then `load`.** `run_harness.py` does this automatically.
2. **Sim duration.** The `simulate` `StopTime` argument is **not honored** — set
   the model's `TimeSpan` parameter (`plecs.set(name, "TimeSpan", ...)`).

## Files

| File | Role |
|------|------|
| `templates/2l_vsi_pmsm_tofile.plecs` | Seed harness: 2L-VSI + PMSM + hysteresis control, instrumented with a `ToFile` (`cap_iabc`) capturing 3-phase currents. Derived from `worked-designs/family-car-400v-sic/pmsm_mycar.plecs`. **Path-free** — the runner injects `Filename` at runtime. |
| `run_harness.py` | Direct-XML-RPC runner: `close→load→set Filename/TimeSpan/params→simulate→read CSV`. No MCP needed. |
| `summarize.py` | CSV→metrics: steady-state RMS, fundamental freq, current THD over integer periods (SOP S2). |
| `model_registry.json` | Per-model validation registry. `validation_status` gates evidence (plan §3): `unvalidated` models may be run but **may not close the evidence gate**. |

## Run it

```bash
# PLECS.exe -server 1080 must be running first
cd data/plecs
python run_harness.py templates/2l_vsi_pmsm_tofile.plecs out.csv ia,ib,ic --timespan 0.2
```

## Status & next layer

The **readback pipeline is proven end-to-end** (2026-07-19). What the seed harness
does **not** yet have (the Track-1 build, `design-2l-b6-800v-sic`):

- **Datasheet SiC loss/thermal description** — the library `2-Level IGBT Conv.`
  block uses ideal switches with an `Rth` only (no `Eon/Eoff/Econd` vs `V,I,Tj`).
  Efficiency is not production-accurate until a real loss/thermal description +
  Foster/Cauer net loads.
- **DC-side ammeter** — needed for inverter η (`P_dc` vs `P_ac`); the seed meters
  only the AC phase currents/voltage.
- **800 V SiC retarget** + a **defined steady traction operating point** (the seed
  is a speed ramp — `f_e≈5–17 Hz` in the first 0.2 s).
- The **S1–S7 SOP** + 9-corner matrix + Wolfspeed/TI CRD calibration (S5).

A number is evidence only after its model reaches `validation_status: validated`
in the registry.
