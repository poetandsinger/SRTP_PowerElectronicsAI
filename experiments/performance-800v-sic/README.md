# Performance/Hypercar Inverter (800 V SiC) — power-density + Zth artifacts

Backs `srtp_docs/power-electronics/traction-inverter/worked-example-performance-800v-sic.md`.

- `perf_zth.py` — continuous rating (steady `Tj`≤160 °C), transient `Zth(t)` peak-duration curve (reproduces the Porsche 815 kW/2 s, 700 kW/10 s, 580 cont shape), and power density with **volume derived from sourced kW/L** (DOE 13→34→100; Wolfspeed 33).
- `results.txt` — captured run.

Run: `python perf_zth.py` (numpy). **Honesty:** Foster thermal-mass values are illustrative; only the "higher peak → shorter burst" shape and the sourced densities are firm.
