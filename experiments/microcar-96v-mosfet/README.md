# City Microcar Inverter (~96 V LV Si-MOSFET) — cost-down artifacts

Backs `srtp_docs/power-electronics/traction-inverter/worked-example-microcar-96v-mosfet.md`.

- `microcar_cost.py` — 30 kW inverter as 96 V LV-MOSFET vs 350 V Si-IGBT: phase current, conduction/switching/interconnect loss, efficiency, and a **relative** (ordinal, no $) cost-structure argument. Shows the LV current penalty lands on interconnect, not switches.
- `results.txt` — captured run.

Run: `python microcar_cost.py` (numpy). **Honesty:** the Wuling device (LV MOSFET) is INFERENCE from the confirmed ~96 V bus; inverter BOM $ is UNSOURCED — nothing here is a quote.
