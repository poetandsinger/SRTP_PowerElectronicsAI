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

## Status: **runs headless (`ok:true`)**, per-switch readout NOT yet confirmed

The model **loads and simulates** with all 6 CAB450 MOSFETs + body diodes. Because the switches sit
at the demo's original heat-sink positions, coupling should be preserved (as proven for the buck
retarget). **BUT** the per-switch loss/Tj readout is unconfirmed: a `PlecsProbe` on `IGBT1` inside the
`Circuit` subsystem writes a CSV but reads **0** for every signal name tried (`"Device …"`, `"MOSFET …"`
junction temp / conduction loss). Root cause unresolved — likely the exact probe signal name/path for
the legacy plain-`Mosfet` device, or the probe isn't resolving the nested component. **Do not claim the
switches are validated until Tj reads ≥ Ta and losses are non-zero.**

## Next steps (for the next agent)

1. **Confirm coupling/readout:** find the correct per-switch Tj/loss signal — try reading the demo's
   *own* thermal path (it computes junction temps for its rainflow/lifetime analysis; inspect its
   scopes/Analysis), or open once in the GUI to read the exact probe signal names, or probe the diode.
   A coupled Tj reads ≥ 65 °C; an uncoupled one runs away.
2. **Retarget the operating point to 800 V** (the demo's DC bus + machine are its own values) and a
   defined corner; run the 9-corner matrix (`procedure-simulation-and-validation` §4).
3. **Calibrate** ≥1 corner to the Wolfspeed CRD (S5), fill `design-2l-b6-800v-sic`, set
   `model_registry.json` → `validation_status: validated` (Step 5).

## Why this matters

It removes the hardest blocker: a **6-switch 2L-B6 with device→heatsink coupling** now exists and runs
with CAB450, entirely from text edits to a GUI-saved base — no from-scratch coupling needed. See
`../HANDOFF.md` for the full method and the coupling root-cause.
