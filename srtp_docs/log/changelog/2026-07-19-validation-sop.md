---
title: "PLECS validation SOP + procedure-* method notes"
type: changelog
field: project
created: 2026-07-19
updated: 2026-07-19
tags: [changelog, plecs, simulation, design]
---

# 2026-07-19 — Validation SOP

Hardened the testing methodology into a **clear SOP** and consolidated the method notes under a `procedure-*` scheme.

## What changed

**SOP** — [[procedure-simulation-and-validation]] §4 rewritten from a loose corner-list into a gated procedure (S1–S7):
- **Run-validity gates first** (a failing run is discarded, not reported): **S1** numerical convergence (timestep-independence), **S2** steady-state + integer-cycle measurement window, **S3** energy balance (P_in = P_out + P_loss ±1 %).
- **§4.2 acceptance tolerances** (η ±1 pt, loss ±10 %, Tj ±5 °C…) folded into the corner matrix; each corner now pins a **(Vdc, load) operating point** with the launch corner for thermal/ripple.
- **S5** non-circular calibration against the *measured* Wolfspeed anchor (kills the hand-estimate circularity); **S6** averaged↔switched reconciliation; **S7** register with model hash + solver settings + loss-table source.
- **§4.4 per-topology additions** — the 9 corners are topology-general; 3L adds **Corner 10 neutral-point balance**, ANPC adds redundant-zero-state loss-equalisation + RLC filter sweep, TNPC the full-Vdc outer-switch check, NPC the inner/outer loss asymmetry. A topology *extends* the SOP, never replaces it.

**Consistency fix** — [[procedure-control]] no longer implies a Simulink backend: its checks run in the PLECS drive model and obey the SOP gates; §7 scoped to the embedded-controller path (Embedded Coder for controller C only, PLECS as plant). Title/tags cleaned.

**Naming** — method notes consolidated to `procedure-*`: `design-procedure`→`procedure-design`, `simulation-and-validation`→`procedure-simulation-and-validation`, `control-how-to`→`procedure-control` (documented in [[SCHEMA]]). Wikilinks auto-updated; ~30 stale plain-text references (`… §N` citations) fixed by hand.

**Docs** — [[SCHEMA]] naming-schemes table gains the `procedure-*` family + an evidence-gate note; [[README]] updated for the topology units, procedures, and SOP.

## Why

A review found the old corner matrix would let a coarse-timestep, non-steady-state, self-consistent-but-wrong model pass as "validated." The SOP closes those procedural gaps — nothing is evidence until it clears S1–S7 — while staying topology-general with explicit per-topology extensions.

---

← [[changelog-index]] | [[procedure-simulation-and-validation]] | [[depth-research-plan]]
