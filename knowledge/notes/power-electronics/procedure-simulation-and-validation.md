---
title: "Simulation & Validation"
type: topic
field: power-electronics
created: 2026-07-10
updated: 2026-07-19
status: unverified
evidence: single-study
sources: [sources/ai-agents/plecs-ai-agent-integration-ordonez, sources/ai-agents/phia-lpcomda-2026-physics-informed-pe-agent, sources/ai-agents/pe-mas-flyback-mas]
tags: [power-electronics, simulation, plecs, review, design]
review_by: 2026-10-17
---

# Simulation & Validation

> How to model and validate a traction-inverter design. The project's simulator is **PLECS only** (MATLAB dropped) [80][58]. This chapter is the *model side* of V&V — how PLECS represents the inverter, and the corner tests that turn a sizing spec ([[procedure-design]]) into evidence. The *hardware side* (double-pulse bench, HIL, EOL) lives in [[manufacturing-and-test]]; validation closes the loop against [[index-reference-designs]].

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge.

## 1. Why PLECS, and Where It Stops

**PLECS is chosen** because it does together the two things a traction-inverter model needs: piecewise-linear switching-circuit simulation (fast, no SPICE convergence pain) *and* a coupled thermal network driven by device loss tables [58][80]. It ships native **PMSM (with saturation LUT) and induction-machine models plus an FOC traction demo**, so the plant is a library block, not a from-scratch build [80], [[machine-and-load]] §8. It is scriptable over XML-RPC (`PLECS.exe -server <port>`); an MCP wrapper exposes those calls as agent tools and sweeps designs by passing `ModelVars`, as in the PE-MAS PLECS MCP server [72][78][79]. The **verified** call surface is below.

**Where it stops:** PLECS is a circuit+thermal solver, not a 3-D field solver. It does **not** give you parasitic extraction, EMI radiated fields, mechanical stress, or CFD coolant flow — those need FEA/CFD tools (§5) and, ultimately, hardware. Loop inductance `Lσ`, CM-capacitance, and EMI spectra enter PLECS only as *numbers you supply from elsewhere*, not results it derives [T], [[design-emi-emc]].

### Driving PLECS headless — verified surface (PLECS 4.8, 2026-07-18)

Confirmed by directly driving the installed Standalone build (basis for [[worked-example-family-car-400v-sic]] §7):

- **Launch:** `PLECS.exe -server 1080` starts the XML-RPC server (blocking, one request at a time — batch or run parallel instances on separate ports).
- **Methods present:** `plecs.load`, `plecs.set`, `plecs.get`, `plecs.simulate`, `plecs.getModelTree`, `plecs.scope`, `plecs.statistics`, `plecs.analyze`, `plecs.codegen`, `plecs.close`. **No circuit-building or script-eval methods** — `plecs.add`/`connect`/`eval` are **absent in 4.8** (PE-MAS probes for them because they are build-dependent [72]). ⇒ **parameterize a `.plecs` template; you cannot assemble a netlist over RPC.**
- **Readback — corrected 2026-07-19 (supersedes the Outport assumption).** `plecs.simulate('model')` returns `{Time, Values}` that are **empty in this 4.8 build**, even with a top-level `Output` block wired to a live signal — verified on both a minimal `SineGenerator→Output` model and the real 2L-VSI+PMSM model, via the MCP tool *and* direct `plecs.simulate` RPC. **The working readback is a `ToFile` block → CSV on disk**, read back with `numpy.genfromtxt`. Configure `ToFile`: `Filename`=absolute path (`Evaluate off`), `FileType=1` (CSV), `WriteSignalNames=1`, `SampleTime=-1` (every step; set a number to decimate). Mux multiple signals into its single input. CSV = col 0 Time, cols 1..N the muxed signals in order; **no header row is written** despite `WriteSignalNames`. This is exactly how PE-MAS reads results (`plecs_interface.py` parses a ToFile CSV; treats `res['Values']` as an unreliable bonus). **Stale-model trap:** after editing a `.plecs`, `close` then re-`load` — re-loading an open model does not refresh it. ([[plan-plecs-harness]] §4.)
- **`.plecs` is ASCII:** `Component{Type,Name,Position,Parameter{Variable,Value}}` + `Connection{SrcComponent,SrcTerminal,Dst…}`; parameters live per-block or in a model-level `InitializationCommands` script. Retarget by text-replacing `Value` fields or via `plecs.set`. Library/`Reference` blocks carry parameter overrides (e.g. PMSM `R`, `L=[Ld Lq]`, `phi`, `p`).
- **Demo library = ready templates** [80] to seed from: `permanent_magnet_synchronous_machine` (clean 2L-VSI + PMSM + FOC, ~1500 lines), `electric_vehicle_with_active_damping` (full EV drive), `look_up_table_based_pmsm` (saturation LUT), `two_axle_vehicle_with_driving_profile`, `induction_machine_drive_controlled_with_dtc`.

## 2. How PLECS Models the Inverter — the Four Layers

```mermaid
flowchart TD
  C["1. Circuit layer<br/>piecewise-linear switches, DC-link, motor"] --> L["2. Loss layer<br/>Eon/Eoff/Econd lookup vs (V, I, Tj)"]
  L --> T["3. Thermal layer<br/>Foster/Cauer RC → Tj feeds back to loss"]
  T --> L
  C --> P["4. Plant layer<br/>native PMSM+FOC demo as the load"]
```

| Layer | What it is | Where the data comes from | Cite |
|-------|-----------|---------------------------|------|
| **Circuit** | ideal PWL switch (on-R, threshold, off = open); DC-link cap+ESR/ESL; 3-phase bridge | topology from [[circuit-topologies]] | [58] |
| **Loss** | 3-D lookup: `Eon,Eoff = f(Vblock, I, Tj)` and `Vf/Rds = f(I, Tj)` — the *thermal description* | **datasheet DPT curves** of the chosen module (e.g. CAB450M12XM3 [92]); extracted by double-pulse [133] | [58][133][25] |
| **Thermal** | Foster (fit to datasheet Zth) or Cauer (physical layers) RC chain; junction→case→cooler | datasheet `Zth,jc`; TIM+cold-plate `Rth` [101] | [101][143] |
| **Plant** | native PMSM (dq + saturation LUT) + FOC controller demo | PLECS library; machine params from [[machine-and-load]] §3 | [80] |

**The loss↔thermal coupling is the point.** Loss raises `Tj`; higher `Tj` raises `Rds(on)` and switching energy; that raises loss again. A model with a *fixed* `Tj` understates hot-corner loss — the coupled network is what makes the efficiency and `Tj` numbers trustworthy [25][58]. Loss tables are **only as good as the datasheet DPT data**; a bench double-pulse on the real module is what closes the gap [133], [[manufacturing-and-test]] §3.

## 3. Model Fidelity — Switching vs Averaged

Pick the coarsest model that answers the question; the two live in one file [T][58]:

| Model | Timestep | Answers | Blind to |
|-------|----------|---------|----------|
| **Switched** (every edge resolved) | ~10–100 ns | switching loss, THD, dv/dt-at-node, ripple, dead-time | slow — minutes per electrical second |
| **Averaged** (duty-cycle sources) | ~10–100 µs | drive-cycle efficiency, thermal over a cycle, control stability | anything inside a switching period |

A full **WLTP cycle** (~1800 s) is only tractable in the averaged model; the switched model validates the loss/thermal tables at a handful of operating points that the averaged model then reuses [T][63]. This two-tier approach (switched for point accuracy, averaged for cycle coverage) is standard practice [63][143].

## 4. The Validation SOP

A design's numbers are **evidence only after this procedure**. The order is deliberate: **run-validity gates (S1–S3) first** — a run that fails them is *discarded, not reported* — then the corner matrix (S4), the non-circular calibration (S5), the fidelity reconciliation (S6), and registration (S7). **S1–S7 are topology-general;** §4.4 lists what a topology *adds*.

### 4.1 Run-validity gates (every switched run passes these before its numbers count)

- **S1 — Numerical convergence.** Halve the switched `max-timestep` (and tighten `reltol`) until η and THD change **< 0.1 pt** and **< 0.2 %abs** between refinements; record the converged step. At `fsw`=16 kHz resolve edges to **≤ ~50–100 ns**. A non-converged run is invalid. (The reference study fixes Gear / `maxord=2` / `reltol=1e-4` / 100 ns for this reason.)
- **S2 — Steady state + integer-cycle window.** Run **≥ 5 fundamental periods** past startup (until half-bus, `Tj`, and RMS currents settle), then measure **only over an integer number of fundamental cycles** (e.g. the last 2). Startup or non-integer windows give wrong η/THD/ripple — the failure that made the reference doc's 5.59 ms (0.56-cycle) run unusable.
- **S3 — Energy balance.** Verify **P_in = P_out + P_loss within ±1 %** (PLECS reports all three independently — mind the source-current sign). A mismatch means a sign error, a missing loss term, or a bad window: fix before reporting η.

### 4.2 Acceptance tolerances

| Metric | Tolerance | Against |
|--------|-----------|---------|
| Efficiency η | **±1 pt** | measured reference (S5); hand estimate = sanity only |
| Convergence Δη / ΔTHD | < 0.1 pt / < 0.2 %abs | timestep halving (S1) |
| Loss split (cond / sw) | ±10 % | reference / baseline |
| Junction temp `Tj` | ±5 °C | reference / baseline |
| Energy balance | ±1 % | P_in vs P_out+P_loss (S3) |
| DC-link ripple ΔVdc | < 1–2 % | rating |
| Averaged vs switched | ±10 % | shared operating points (S6) |

### 4.3 S4 — Corner matrix (each corner pins a (Vdc, load) point + a numeric criterion)

| # | Test | Operating point (Vdc, load) | Pass criterion | Ties to |
|---|------|-----------------------------|----------------|---------|
| 1 | **Double-pulse** | 850 V, I≈`Ipk` (~424 A), `Tj` hot | Eon/Eoff extracted; `Vds,pk` within switching-SOA (≤~83 % BV) | [[procedure-design]] §2–3 |
| 2 | **Efficiency** | {550, 750, 850} V × {peak 150 kW, cont 70 kW} | η within ±1 pt of baseline; loss split ±10 %; **energy-balanced (S3)** | [[procedure-design]] §3 |
| 3 | **Thermal / continuous** | 850 V, **launch 300 A rms**, `Tcool`=65 °C | `Tj` < 175 °C over `Zth`-limited duration | [[thermal-design]] §6 |
| 4 | **DC-link ripple** | worst `m`/cosφ at launch | `I_cap,rms` < rating; ΔVdc < 1–2 % | [[procedure-design]] §4 |
| 5 | **Overmodulation / six-step** | 550 V (low line), MI > 0.907 | fundamental & THD vs field-weakening need | [[control-schemes]] §4.4 |
| 6 | **Field-weakening sweep** | 750 V, speed 0→max | torque ~1/ω; `Vd²+Vq² ≤ Vmax²`; current within limit | [[machine-and-load]] §5 |
| 7 | **Fault: short-circuit** | 850 V, shoot-through, `Tj` hot | fault current & `I²t` vs SCWT budget (< 3 µs SiC) | [[protection-and-safety]] §3 |
| 8 | **Fault: ASC entry** | short all low-side at max speed | entry transient, drag torque, **no bus overvolt** | [[protection-and-safety]] §5 |
| 9 | **Drive-cycle** | averaged, WLTP / US06 | cycle-average η; `Tj` history for lifetime | [[reliability-and-lifetime]] |

S1 applies to every switched corner; S2 to 2/4/5/6/9; S3 to 2/9. The launch corner (300 A rms / 424 A pk), not peak power, drives the thermal/ripple worst case [[procedure-design]] §1.

### 4.4 Per-topology additions (when the topology opens new specs)

The 9 corners are topology-general. A topology **adds**, it does not replace:

- **All 3-level (NPC / TNPC / ANPC):** **Corner 10 — neutral-point balance.** At worst `m`/load, capacitor-voltage divergence must stay bounded — run **with and without** balancing (the ANPC reference shows the half-bus drifting 477→534 V un-balanced). A first-order stress/stability spec 2L does not have.
- **ANPC:** verify **redundant-zero-state loss/`Tj` equalisation** across the four main switches, and sweep the **RLC/damped-LC output filter** (f0, attenuation at `fsw`, 100 Hz drop) per the reference study.
- **TNPC:** confirm the **outer switches block full Vdc** (1200 V device stress) while the NP branch sees Vdc/2.
- **NPC:** quantify the **inner-vs-outer switch loss asymmetry** (the flaw ANPC fixes).

### 4.5 S5–S7 — calibrate, reconcile, register

- **S5 — Calibrate against measured data (the non-circular anchor).** Closed-form hand estimates share the model's `[T]` device/machine assumptions, so agreement proves *self-consistency, not correctness*. Before a model is `validated`, at least one corner must match the **measured Wolfspeed/TI CRD** — >98 % η, 32 kW/L, 175 °C — within **±1 pt η / ±10 % loss / ±10 % density** [91], [[reference-design-wolfspeed-ti-300kw-800v]].
- **S6 — Averaged↔switched reconciliation.** The averaged model must reproduce the switched model's loss and `Tj` at the shared operating points within **±10 %** before its drive-cycle result (Corner 9) is trusted [63].
- **S7 — Summarise & register.** Reduce to the ~36-number summary; regression-check against the topology's validated baseline; pass/fail exit; write the registry entry with **model hash + solver settings + loss-table source** ([[plan-plecs-harness]] §3–4). Only now is the number evidence, and Corner 9 feeds the `Tj` mission profile into rainflow→Miner [143], [[reliability-and-lifetime]].

## 5. Tool Landscape (PLECS-first, others for what PLECS can't do)

| Tool | Role here | Why not primary |
|------|-----------|-----------------|
| **PLECS** | circuit + thermal + machine — the workhorse [58][80] | — |
| MATLAB/Simulink | *dropped* as sim backend; controls-design reference only | not PE-switching-optimized; licensing/agent-cost [79] |
| ANSYS Maxwell / Icepak, COMSOL | EM parasitic extraction, CFD coolant, magnetics | slow; feed *numbers into* PLECS, not replace it |
| JMAG / Motor-CAD | machine FEA → flux maps (`Ld,Lq,λ` vs i) | supplies the saturation LUT PLECS consumes [80] |
| Typhoon / dSPACE / OPAL-RT | real-time HIL — see [[manufacturing-and-test]] §5 | hardware-in-loop, not desktop design |

*Sources: Plexim PLECS docs [58][80] [Reliability: High/vendor]; Ordonez AI+PLECS [79] [Medium]; Zhang & Negri AI multi-physics [63] [High].*

## 6. Pain Points (why this is not push-button)

1. **Loss tables gate everything.** Wrong DPT data → wrong η and `Tj`; must trace to the *orderable* module datasheet, ideally bench-verified [133].
2. **Switched↔averaged handoff** loses detail; the averaged model inherits any error in the point-validated tables [63].
3. **Parasitics are exogenous.** `Lσ`, CM-cap, and EMI come from layout/FEA, not PLECS — a PLECS-clean design can still fail EMC [T], [[design-emi-emc]].
4. **Machine params are provisional.** `[T]` IPMSM values (design-proc §0) swing torque/current; a real flux-map LUT is needed for MTPA/field-weakening accuracy [45][80].
5. **Sim ≠ silicon.** Every PLECS number is a hypothesis until double-pulse + HIL + dyno confirm it [133][134].

## Red Team

**Steelman against:** This chapter sells PLECS as *the* validator, but PLECS validates only the slice of the design that is a circuit+thermal problem. The failure modes that actually kill traction inverters in the field — EMC non-compliance, `Lσ` overshoot, bearing currents, power-cycling fatigue, control edge cases — are largely **outside** what PLECS resolves. Calling a design "PLECS-validated" risks false confidence: it means the loss/thermal/ripple math checks out with *assumed* device and machine data, nothing more.

**How it could be false:**
1. **Garbage-in on loss tables:** datasheet DPT is measured on a reference layout at a fixed `Lσ`; the real inverter's overshoot and `Eoff` differ — sim understates loss until bench-corrected [133].
2. **Machine model is linear-ish:** even the saturation LUT is FEA- or datasheet-derived; if that data is `[T]` (as in the anchor), corners 5–8 rest on placeholder physics [45].
3. **Averaged drive-cycle η** hides switching-period effects (dead-time distortion, reverse recovery) that shift real cycle loss by several %  [63].
4. **No EMC/parasitic coverage:** the biggest compliance risk (CISPR 25) is not in scope here — a structural gap, not a tuning error.
5. **Single-vendor lock-in:** "PLECS only" is a project decision [79], not an independent finding that PLECS is most accurate; a SPICE/FEA cross-check would strengthen any number.

**What would change my mind:** a PLECS 2L-B6 model that clears the S1–S7 SOP and whose efficiency, THD, and `Tj` at three corners match *measured* double-pulse + calorimetric data on the real module (S5) within a few %; a flux-map LUT from machine FEA replacing the `[T]` parameters.

**Residual doubt:** The SOP now closes the *procedural* gaps — run-validity gates (S1–S3) stop a coarse-timestep or non-steady-state run from counting, and S5 breaks the hand-estimate circularity by requiring a measured anchor. Two bounded doubts remain: (a) **execution** — no model has yet cleared S1–S7; the numbers are provisional until one does; (b) **scope** — "PLECS-validated" still means circuit + thermal + control only, with EMC, parasitics, and fatigue explicitly out of scope and pushed to FEA and hardware.

---

> **References:** [[citations]]

← [[procedure-design]] | [[manufacturing-and-test]] | [[reliability-and-lifetime]] →
