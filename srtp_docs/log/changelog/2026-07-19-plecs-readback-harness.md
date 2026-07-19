---
title: "PLECS readback blocker cleared + reusable harness"
type: changelog
field: project
created: 2026-07-19
updated: 2026-07-19
tags: [changelog, plecs, simulation, engineering-ai]
---

# 2026-07-19 — PLECS readback cleared + harness scaffolding

Cleared the single hard blocker on the [[plan-depth-research]] PLECS-first program:
turning "the model runs" into "the model yields evidence."

## The finding (corrects a "verified" claim)

`plecs.simulate` returns an **empty** `{Time, Values}` in PLECS 4.8 Standalone here
— even with a top-level `Output` block wired to a live signal. Verified on both a
minimal `SineGenerator→Output` model and the real 2L-VSI+PMSM model, via the MCP
tool *and* direct `plecs.simulate` RPC. This **disproves** the earlier
"Values come only from top-level Outport blocks" assumption recorded as verified
2026-07-18.

**Working readback = a `ToFile` block → CSV on disk**, read with `numpy`
(`FileType=1`, `WriteSignalNames=1`, `SampleTime=-1`, absolute `Filename`; mux
signals into its single input; no header row is written). This mirrors how PE-MAS
actually reads results (`plecs_interface.py` parses a ToFile CSV; treats
`res['Values']` as an unreliable bonus).

Two traps found and documented: **stale model** (after editing a `.plecs`, must
`close` then `load` — re-loading an open model does not refresh it) and
**sim duration** (the `simulate` `StopTime` arg is not honored; set the model
`TimeSpan`).

## What changed

- **Notes corrected** (they had documented the wrong mechanism as verified):
  [[procedure-simulation-and-validation]] §1 readback bullet, [[plan-plecs-harness]]
  §1 readback requirement, [[plan-depth-research]] (harness bullet ⧗, environment
  table, gotchas). Memories `plecs-readback-tofile` (new) + `plecs-mcp-setup`.
- **Reusable harness added** under `data/plecs/` (outside the vault — runnable
  artifacts): `templates/2l_vsi_pmsm_tofile.plecs` (ToFile-instrumented seed,
  path-free), `run_harness.py` (direct-XML-RPC runner: close→load→set→simulate→CSV),
  `summarize.py` (CSV→RMS/f0/THD), `model_registry.json` (validation registry;
  `validation_status` gates evidence per [[plan-plecs-harness]] §3), `README.md`.
- **Proven end-to-end**: edit→close→open→set `Filename`/`TimeSpan`→simulate→CSV
  (88k rows)→numpy RMS/f0 on the real switched 2L model, and via runtime parameter
  injection with `set_component_param`.

## Loss-layer prep (Track 1 staged, not fabricated)

- **Loss/thermal XML schema learned** from the PLECS demo library (the Wolfspeed
  `C3M0030090K.xml` in the DAB demo) and the assignment mechanism (`therm='file:...'`
  on a library converter block + HeatSink). Written up turn-key in
  `data/plecs/LOSS_LAYER_BUILD.md`, incl. the low-risk path (assign to the seed's
  converter block, no hand-built 6-MOSFET bridge).
- **Primary source gathered + cited** (subagent, honestly flagged): the target module
  **Wolfspeed CAB450M12XM3** datasheet → [[wolfspeed-cab450m12xm3-datasheet]] (new
  `type: source`) + citations [166]–[169]. R_DS(on) 2.6/4.7 mΩ, E_on/E_off/E_rr at
  600 V for 25/125/175 °C, R_th,JC 0.094 °C/W, ratings. **Wolfspeed publishes a ready
  PLECS XML** [167] (full V-I-T loss surface + Cauer net) — the preferred artifact
  (dynamic portal; needs an interactive fetch). Linked into the Wolfspeed reference
  design + [[design-2l-b6-800v-sic]]; registry entry staged.

## Loss layer ACTIVATED — official Wolfspeed models in-repo

The user supplied the **complete Wolfspeed PLECS device library** → reorganized
space-free under `plecs_models/wolfspeed/` (669 models: diodes, mosfet-with-diode,
legacy-mosfets; + `README.md` manifest + PRD-09611 user guide [170], citation added).
Outside the vault (no frontmatter on executables).

The target **CAB450M12XM3.xml** (official, Version 4 2026-03-19) carries the **full
E_on/E_off/E_rr 4-D surface incl. 800 V at all T_j** (resolves the datasheet's missing
800 V/175 °C curve) + Rg-scaling tables + both conduction paths + a 4-stage Cauer net
≈0.095 °C/W. **Proven 2026-07-19:** copied into the harness `_plecs/` folder, assigned
(`therm=file:CAB450M12XM3`, `Rth`, `T_init=65`) — **loads + simulates cleanly on the
library converter block** (it accepts the "MOSFET with Diode" class). Hand-building the
XML is no longer needed. Source note + registry + `LOSS_LAYER_BUILD.md` updated.

## What remains (Track 1, `design-2l-b6-800v-sic`)

Still `validation_status: unvalidated`. Next: wire `PlecsProbe`(Tj) +
`SwitchLossCalculator`(P_cond/P_sw) + a DC ammeter into the ToFile mux; retarget to
800 V + a fixed steady operating point (the seed runs a startup speed ramp); run the
9-corner matrix; calibrate to the Wolfspeed CRD (SOP S1–S7). Numbers count as evidence
only after `validation_status: validated`.

← [[changelog-index]] | [[plan-depth-research]] | [[procedure-simulation-and-validation]]
