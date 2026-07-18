---
title: "Manufacturing & Test"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, packaging, reliability, design, simulation]
review_by: 2026-10-17
---

## What This Is

How the inverter is **built and verified** — module assembly, system integration, and the test pyramid from double-pulse to HIL to end-of-line. The step between a validated design and a shippable part. Pairs with [[packaging-and-layout]] (what the structure is) and [[simulation-and-validation]] (model-side V&V).

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge.

## 1. Power-Module Assembly

| Step | Process | Key point |
|------|---------|-----------|
| **Die attach** | **silver sintering** (~250 °C/15 MPa/5 min; or 300 °C/3 MPa) | joint k~240 W/m·K, remelts 961 °C → decouples service temp from process temp; the SiC-at-175 °C enabler [127] |
| **Top interconnect** | Al wedge bond (100–500 µm; ~25 A@300 µm, ~60 A@500 µm) **or Cu clip** | clip: ~30% lower R, one clip ≈ 15 wires, ~2.5× thermal-cycle life; Cu-on-Al needs Ni/Pd cap vs Cu₉Al₄ [128] |
| **Substrate** | **AMB Si₃N₄** (active-metal braze; DBC can't wet Si₃N₄) | CTE ~3.2 ppm/K (matches SiC), tough → ~50× substrate reliability vs Al₂O₃ DBC [129] |
| **Encapsulation** | silicone gel (or transfer mold) | suppresses partial discharge; gel limited ~200 °C — a high-temp ceiling [130] |
| **Baseplate** | AlSiC (CTE 6.5–9.0 ppm/K tunable), **direct pin-fin** | CTE-match ~2× module life; pin-fin deletes the grease TIM (~−20% Rth) [131] |

Solder/sinter fatigue and wire-bond lift-off are the leading power-cycling wear-out sites — see [[reliability-and-lifetime]].

## 2. Inverter (System) Assembly

- **Laminated busbar:** multilayer Cu + thin dielectric, laid out for +/− field cancellation → minimizes `Lσ`; integrated designs hit **~6.5 nH (small) / 17.5 nH (large loop)** [132], [[packaging-and-layout]] §2.
- **DC-link:** film (PP) caps for ripple + low ESL, not electrolytic [132][41].
- **Gate-driver PCB:** reinforced isolation (5.7 kV/8 kV), CMTI ≥100 V/ns, DESAT + two-level turn-off + Miller clamp [93][91], [[gate-driver-design]].
- **Cold-plate/TIM:** the TIM is usually the **highest-Rth layer**; control **bond-line thickness (BLT)** to 90–110% of spacer-particle size to kill scatter [104], [[thermal-design]] §5.
- **Enclosure:** IP67 (underbody to **IP6K9K**: 80 °C/80–100 bar jets); HV connectors O-ring + epoxy-potted; EOL sealing by **air-pressure-decay** leak test [137].

## 3. Test & Validation Flow

| Stage | What | Note |
|-------|------|------|
| Incoming | Vth, RDS(on), leakage; devices pre-qual'd AEC-Q101 | [89] |
| In-process | **X-ray / SAM** (die-attach voids, delamination), bond pull/shear | catches §1 defects |
| **Double-pulse test** | Eon/Eoff, transition times, diode reverse recovery vs I, Rg, Tc | scope/probe BW must match ns transients [133] |
| **EOL functional** | dyno or **electronic motor emulator** (back-EMF, saturation, fault injection) sweeps torque-speed map | emulator avoids a physical machine [137] |
| **HiPot / insulation** | dielectric withstand up to **1500 V AC** (ISO 16750-2) + IR | automated, traceable [137] |

## 4. The V-Model — MIL → SIL → PIL → HIL

Design (left) maps to verification (right) [135]: **MIL** (control+plant as models) → **SIL** (compiled code on host) → **PIL** (code on the target processor — timing/memory/precision) → **HIL** (full ECU vs real-time plant) → dyno → vehicle; extended MiL→SiL→PiL→HiL→**DiL→ViL** [135]. This is the software/system side of [[simulation-and-validation]].

## 5. HIL — Timestep Is the Spec

SiC transients are ns-scale, so the real-time plant must run a tiny fixed step [134]:

| Platform | Timestep | Note |
|----------|----------|------|
| **Typhoon HIL** | **200 ns** (down to 25 ns), 3.5 ns DI sampling | captures gate/PWM edges [134] |
| **dSPACE SCALEXIO** | FPGA motor emulation (IM/PMSM/SESM) | Power-HIL [134] |
| **OPAL-RT** | ~100 ns (FPGA) | converter models [134] |
| **Speedgoat** | sub-ms CPU / µs FPGA | driven finer by SiC fsw [134] |

Tested: control stability, PWM/dead-time, fault injection (SC, overcurrent, sensor loss, desat), field-weakening — before hardware/vehicle risk [134].

## 6. Production Quality & Cost

- **QMS:** **IATF 16949**; launch via **APQP**, evidence via **PPAP** — AEC qualification does *not* replace these [136].
- **Zero-defects:** targets moved ppm → **ppb / 0 ppm**, formalized by **AEC-Q004** [136].
- **Cost drivers:** SiC die dominates — a 1200 V SiC MOSFET ~**3× a comparable IGBT** (late 2025); levers are **200 mm wafers** (~2× die/wafer) and die-shrink. US DOE target: **$2.7/kW, 100 kW/L, 98%, 800 V** [138] (target, not achieved). DFM: sinter/clip automation, integrated busbar, direct-cooled baseplate (delete TIM step).

## 7. Burn-in, Traceability & Functional Safety in Production

- **Screening:** **HTRB** (drain leakage → junction/contamination defects) and **HTGB** (gate-oxide → Vth instability; the more severe for SiC); wafer-level burn-in weeds bad die pre-assembly [137].
- **ISO 26262 Part 7** (production) demands **bidirectional traceability** requirements→test and per-unit serialization; capture die lot + sinter/bond parameters + HiPot/EOL results so any field failure bounds a suspect population — the same data spine PPAP/IATF 16949 require [85][136].

## Red Team

**Steelman against:** Much of this is process *typical practice* assembled from vendor pages and single studies, not a specific qualified production line. Sinter recipes, bond-current limits, "50× Si₃N₄ reliability," "60% failures are solder fatigue," and HIL timesteps are all best-case or single-source figures presented as general truths. The DOE $2.7/kW and "SiC 3× IGBT" are a research *target* and a volatile market snapshot, easily mistaken for achieved production cost.

**How it could be false:**
1. **Recipe/limit specificity:** sinter params [127] and wire-current limits [128] are process/tool-specific; a real line differs.
2. **Reliability multipliers** ("50×", "2.5×", "60%") [128][129] are vendor/single-study illustrations — hedge as "studies report."
3. **HIL timesteps** (25/100/200 ns) [134] are best-case FPGA for small models; achievable step degrades with model size — "as low as."
4. **Cost figures** [138] mix a DOE target with a market-analyst snapshot — label date + target-vs-actual; trace to the primary DOE VTO roadmap.

**What would change my mind:** a specific module's process qualification report; a primary DOE EETT roadmap for the cost/density targets; a second pricing source; the chosen HIL platform's timestep at the actual model complexity.

**Residual doubt:** The *process sequence and test pyramid* are solid and well-sourced; the *specific numbers* are typical/illustrative and target-vs-actual must be labeled. Good as the how-it's-built map; not a production traveler.

---

> **References:** [[citations]]

← [[packaging-and-layout]] | [[simulation-and-validation]] | [[reliability-and-lifetime]] →
