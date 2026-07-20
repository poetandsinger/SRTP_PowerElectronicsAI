# Class-8 e-Truck Inverter (800 V SiC) — lifetime-driven artifacts

Backs `srtp_docs/power-electronics/traction-inverter/worked-example-truck-800v-sic.md`.

- `truck_lifetime.py` — road-load → inverter loss → Foster `Zth` `Tj(t)` → ASTM rainflow → Coffin-Manson (anchored to the vault's empirical Nf datapoint) → Miner `LC` → life in km, over a synthetic long-haul day (cruise + 7% Davis-Dam grade + overnight cold-start). Prints damage-by-cycle and a sizing sweep.
- `results.txt` — captured run.

Run: `python truck_lifetime.py` (numpy). **Honesty:** device params class-typical [T]; Nf coefficients technology-specific → absolute life uncertain ±1–2 orders. Robust output = cold-start dominates + ΔTj-ceiling design rule.
