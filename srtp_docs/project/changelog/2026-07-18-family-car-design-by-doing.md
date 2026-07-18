---
title: "2026-07-18 — Design-by-doing: family-car inverter + first PLECS run"
type: changelog
field: project
created: 2026-07-18
updated: 2026-07-18
tags: [changelog, power-electronics, design, sic, plecs, simulation]
---

# 2026-07-18 — Design-by-doing: family-car inverter + first PLECS run

"Research by doing": invented a common family 4-wheeler and designed its traction inverter end-to-end (spec → circuit → device → thermal → DC-link → control → BOM), RAG-limited to the traction-inverter vault + undergrad physics, then **ran a numerical model** to produce the efficiency/thermal/cycle numbers the vault had always deferred to PLECS.

## New content
- **[[power-electronics/traction-inverter/worked-example-family-car-400v-sic]]** — full worked example. Invented "SRTP FamilyCrossover" (1850 kg C-segment FWD crossover); road-load physics → ~135 kW/345 Nm peak, 55 kW cont, 355 V bus, IPMSM (salient `Ld/Lq`). 2L-B6 **750 V SiC** vs Si-IGBT comparator. Computed: 3-corner efficiency (SiC 98.1–99.0%), thermal (SiC 155 °C / IGBT 173 °C at peak), 170 A DC-link ripple, two drive cycles. Report on compromises (400 V vs 800 V, SiC vs IGBT, `fsw`, device voltage).
- **[[power-electronics/traction-inverter/findings-family-car-design-by-doing]]** — the *new knowledge*: (1) SiC's cycle advantage is switching-loss-driven, so **~2× larger in urban (591 Wh/100 km, +1.5 pt) than mixed (281 Wh/100 km, +1.0 pt)** — quantifies the vault's qualitative "partial-load is where SiC pays" [28]; (2) at launch currents **SiC conduction loss exceeds the IGBT's** (flat `Vce` knee vs `I²Rds`); (3) the **IGBT variant is thermally marginal** at family-car peak (173 vs 155 °C); (4) vehicle road-load should *set* the operating points, not be assumed; (5) **the PLECS blocker is cleared**.

## Executable artifacts (repo, outside the markdown vault)
- `worked-designs/family-car-400v-sic/familycar_inverter.py` — runnable design/loss model (numpy). `results.txt` — its output.
- `worked-designs/family-car-400v-sic/pmsm_mycar.plecs` — the PLECS PMSM-FOC demo retargeted to this machine (355 V, salient `Ld/Lq`), which simulated to completion via XML-RPC.

## Project-status change
- **PLECS confirmed licensed + XML-RPC-driveable** (`PLECS.exe -server`, `plecs.load/set/simulate`). A 2L-VSI+IPMSM+FOC drive with this machine's parameters ran to completion. README status updated. Remaining gap is *result readback* (top-level outports), not tool access — the next concrete step toward the first quantitatively PLECS-validated model.
- Confirmed the RPC surface has **no circuit-building methods** → agent-built models must parameterize a `.plecs` template, not assemble from scratch (informs [[project/plans/plecs-harness]]).

## Miscellaneous PLECS-driving findings (captured)
Verified by hand and written up as a reusable cheat-sheet — [[power-electronics/traction-inverter/simulation-and-validation]] §1 "Driving PLECS headless" and [[project/plans/plecs-harness]] §1:
- **Launch:** `PLECS.exe -server <port>` (blocking, single-request).
- **Method surface (4.8):** `load/set/get/simulate/getModelTree/scope/statistics/analyze/codegen/close` — **no `add`/`connect`/`eval`** (corrected an earlier note that listed `plecs.eval`).
- **Readback gotcha:** `simulate` returns `Values` only from **top-level Outport** blocks; scope-only models return empty — templates must expose an outport per summarized signal.
- **`.plecs` format:** ASCII `Component{…Parameter{Variable,Value}}` + `Connection{…}`; retarget via text-replace or `plecs.set`; `Reference`/library blocks carry param overrides.
- **Demo library** names the ready seed templates (`permanent_magnet_synchronous_machine`, `electric_vehicle_with_active_damping`, `look_up_table_based_pmsm`, …) — the "native PMSM/FOC demo" [80] the plan assumed, now concrete.

## Meta: the design *process*, extracted for the MAS
- **[[ai-agents/design-by-doing-observed-workflow]]** — the workflow this single design pass revealed, mapped to MAS roles. Gold nuggets: **⓪ requirements-derivation** (vehicle road-load → spec) and **④ reporter** bookends the 3-agent loop is missing; **parts = retrieval, not generation** (key `(function,V,I,qual)` → vetted KB part, never a hallucinated MPN); **provenance-typed numbers** the evidence gate can refuse to close on; a **sensitivity step** to steer look-up effort; a cheap **RAG-consistency pre-gate** before spending a PLECS run; **cost-aware de-scope** on exploration. Proposes gaps G-I…G-M against [[project/plans/ai-agent-mas-plan]] (to test against a second pass, n=1).

## Honesty
All numbers come from a self-authored quasi-static model with **class-typical (invented) device loss parameters** — status `unverified`, evidence `single-study`. Directional findings are robust (device physics); absolute magnitudes are a computed hypothesis pending PLECS-with-loss-tables + WLTP trace + real datasheets. Each note's Red Team scopes this.

← [[changelog-index]] | [[power-electronics/traction-inverter/worked-example-family-car-400v-sic]]
