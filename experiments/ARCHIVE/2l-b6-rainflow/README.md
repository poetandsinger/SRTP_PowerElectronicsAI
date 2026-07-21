# 2L-B6 SiC base — rainflow demo retargeted to CAB450 (the real Track-1 model base)

`2l_b6_cab450_rainflow.plecs` is the shipped PLECS **`rainflow_counting`** demo — a **3-phase
2-level VSI (6 IGBT + 6 diode) on a heat sink, driving an induction machine** (a 2L-B6 topology,
GUI-saved with working thermal coupling) — **retargeted headlessly to Wolfspeed CAB450M12XM3**.

**This is the base for a validated 2L-B6 (Steps 1–5), built by the proven method** (retarget a
GUI-saved base, since device→heatsink coupling can't be authored from scratch — see `../HANDOFF.md`).

## What the retarget did (pure text edits; device positions unchanged → coupling preserved)

- 6× `Igbt` → **`Mosfet`** (legacy split model), `thermal=file:CAB450M12XM3`, Ron=0.0036,
  `CustomVariables "struct('Rgon',4,'Rgoff',0)"`. The **legacy** CAB450 MOSFET file
  (`legacy-mosfets/modules/`) is `class="MOSFET"` with **no gate-dependent conduction**, so a plain
  `Mosfet` block accepts it (unlike the current "MOSFET with Diode" file, which needs `MosfetWithDiode`).
- 6× `Diode` → `thermal=file:CAB450M12XM3_bodydiode` (the matching legacy body-diode file).
- Search folder `2l_b6_cab450_rainflow_plecs/` holds both XMLs.
- Ambient `Ta=65 °C`; `Tsim` shortened to 0.25 s for iteration (original 7.5 s drive cycle).

## Status: **runs headless (`ok:true`) AND coupling CONFIRMED**

The model **loads and simulates** with all 6 CAB450 MOSFETs + body diodes, and the **device→heatsink
coupling is confirmed**: the demo's own junction-temp probe (fixed here from `"IGBT junction temp"`
→ `"MOSFET junction temp"`) reads **Tj = 65.3 °C mean / 65.8 °C max — bounded at ambient (Ta=65 °C)**,
not the 684 °C runaway of an uncoupled device. So the switches dissipate into the heat sink correctly.
This is a working, coupled 2L-B6 SiC model, entirely from text edits — **the hard blocker is cleared.**

**Readout note (the fix that worked):** the switch Tj is read by a **top-level** `PlecsProbe` with
`Component "IGBT1"`, `Path "Circuit"` (the demo's own probe named `IGBT`), signal `"MOSFET junction
temp"`. Probing from inside the subsystem, or with `"Device …"` names, reads 0 — use the demo's form.
The Tj rise is small here (~0.8 °C) because the rainflow IM startup is lightly loaded; a real operating
point (§ next steps) will load the switches.

## Next steps (for the next agent) — Steps 2–5

1. **Set a real operating point:** raise the DC bus toward **800 V** and load the machine (or replace
   with a defined 3-phase load at the launch corner ~360 A rms) so the switches carry real current;
   read per-switch conduction/switching loss (`"MOSFET conduction loss"`, and switching energy via a
   `SwitchLossCalculator`) + Tj.
2. **Run the 9-corner matrix** (`procedure-simulation-and-validation` §4); clear S1–S3 gates.
3. **Calibrate** ≥1 corner to the Wolfspeed CRD (S5: >98 % η, 175 °C); fill `design-2l-b6-800v-sic`,
   fold back into `circuit-topologies` + agnostic notes, Red Team, set `model_registry.json` →
   `validation_status: validated` (Step 5). Then start T2.

## Why this matters

It removes the hardest blocker: a **6-switch 2L-B6 with device→heatsink coupling** now exists and runs
with CAB450, entirely from text edits to a GUI-saved base — no from-scratch coupling needed. See
`../HANDOFF.md` for the full method and the coupling root-cause.
