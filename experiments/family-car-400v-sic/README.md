# Family-Car Traction Inverter — runnable design artifacts

Executable artifacts backing the worked example **`srtp_docs/power-electronics/traction-inverter/worked-example-family-car-400v-sic.md`** and its findings note. These live here (repo root, outside the markdown vault) because they carry no note frontmatter and so don't belong in `srtp_docs/`.

| File | What it is |
|------|-----------|
| `familycar_inverter.py` | Self-contained design + loss model (numpy). Invents a C-segment family crossover, derives its operating points from the road-load equation, sizes the 2L-B6 inverter, and computes efficiency at 3 DC corners, thermal, DC-link ripple, and two synthetic drive cycles for **750 V SiC vs Si-IGBT**. |
| `results.txt` | Captured stdout of the model run. |
| `pmsm_mycar.plecs` | The PLECS `permanent_magnet_synchronous_machine` FOC demo **retargeted to this machine** (`Rs`=15 mΩ, salient `Ld/Lq`, `λ`=0.075 Wb, 355 V bus). Loaded and simulated to completion via XML-RPC. |

## Run

```bash
python familycar_inverter.py          # needs numpy; prints the full report
```

To run the PLECS model: `PLECS.exe -server 1080`, then `plecs.load(<abs path to pmsm_mycar.plecs>)` and `plecs.simulate("pmsm_mycar")` over XML-RPC. Note: quantitative readback needs top-level Outport blocks (see `srtp_docs/power-electronics/traction-inverter/simulation-and-validation.md` §1).

## Honesty

Device loss parameters (`Rds`, `Esw`, `Vce`) are **class-typical, invented** values, not a specific datasheet — status `unverified`. Directional findings are robust device physics; absolute magnitudes are a computed hypothesis pending PLECS-with-loss-tables + the official WLTP trace + real module datasheets. The model's Red Team lives in the worked-example note.
