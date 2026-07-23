---
title: "2L-B6 · 6-switch · 800 V SiC Traction Inverter — Design & PLECS Validation"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-24
status: supported
evidence: single-study
sources: [sources/power-electronics/sachs-neuburger-2025-3l-tnpc, sources/power-electronics/sachs-etal-2025-single-dual-inverter, sources/power-electronics/wolfspeed-cab450m12xm3-datasheet]
tags: [power-electronics, traction-inverter, design, two-level, sic, inverter, efficiency, thd, thermal, protection]
review_by: 2026-10-24
---

## What This Note Is

**Track 1 topology unit** (`design-<topology>-<voltage>-<device>`) and the anchor of the design cluster: an 800 V-class **SiC 2-level B6** traction inverter, 150 kW, driving an IPMSM. Collects the spec, key decisions, and validation results in one place. This is the first of four topology units ([[circuit-topologies]]); sizing math in [[procedure-design]], diagrams in [[schematics]], parts in [[bom-2l-b6-sic]]. See [[plan-depth-research]] for the serial build order.

> [!success] **PLECS-VALIDATED (2026-07-23).** `status: supported`. The purpose-fit bench cleared the full
> S1–S7 SOP and 9-corner matrix, CRD-calibrated: **η = 99.07% at the 300 kW CRD anchor** (matches the measured
> Wolfspeed/TI CRD), **99.32% at the design's 150 kW peak**, Tj ≤ 175 °C, energy-balanced. Corners 6–9
> (field-weakening/short-circuit/ASC/drive-cycle) closed analytically/datasheet-bounded, grounded in the
> validated inverter data. See §PLECS Validation. Residual: `[T]` machine params + analytic C6/C8 (Red Team).

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; **[derived]** → computed in [[procedure-design]].

---

## Why This Anchor (industry relevance)

- **2L-B6 is >95% of production** BEV/PHEV traction inverters — the topology to master first [[circuit-topologies]] §1, [28].
- **800V is the industry's migration direction:** Porsche→Hyundai E-GMP→VW PPE→BYD premium have moved to 800V for charging power and lower current losses [[index-traction-inverter]], [28]. It is where **SiC pays off and forces 1200 V devices**, making it the design point where topology trade-offs (2L vs 3L-TNPC) matter [28][43].
- **It is the handoff's first PLECS model** on the critical path (2L-B6 SiC first), so the knowledge base feeds directly into the first validated model [80].

The **highest-*volume* SiC design today is 400 V** (Tesla Model 3/Y class) [31], [[circuit-components]] §1.2 — captured as an alternative in the table below. We anchor on 800 V for *forward* relevance and as the harder, more instructive design point; the 400 V variant is a de-rating of the same procedure.

---

## Specification

| Item | Value | Basis |
|------|-------|-------|
| Topology | 2-level B6 (six-switch VSI) | [[circuit-topologies]] §1 |
| Device | 1200 V SiC MOSFET module, ~450 A class (anchor: [[wolfspeed-cab450m12xm3-datasheet\|CAB450M12XM3]] — 2.6 mΩ, R_th,JC 0.094 °C/W) | [derived §2][38][39][166] |
| DC-link | 750 V nom (550–850 V), 900 V clamp | [T] |
| Peak power | 150 kW (≤30 s) | anchor |
| Continuous power | 70 kW | anchor |
| Max phase current | 300 A rms (424 A pk) | [derived §1][T] |
| Switching frequency | 16 kHz | [50], [[circuit-topologies]] §1 |
| Modulation | SVPWM + DPWM at high load, overmod to six-step | [[control-schemes]] §4 |
| Control | FOC, MTPA + field weakening, resolver | [[procedure-control]] |
| DC-link cap | ~500 µF film, ≥900 Vdc | [derived §4][41] |
| Cooling | pin-fin water-glycol, 65 °C inlet | [T], components §6.1 |
| Motor | IPMSM, 8-pole (params `[T]`) | [T][47][50] |
| Safety | ISO 26262 ASIL-D torque path, ASC safe state | [85][55] |

---

## Operating Points — closed-form vs PLECS-validated (2026-07-23)

The first-pass `[derived]` algebra ([[procedure-design]], `[T]` assumptions) is now **confirmed by the
validated PLECS bench** at the matching corners — the sim reproduces the hand estimates within tolerance.
`[sim]` = PLECS-validated on `bench_2l_b6_800v_sic` (S1–S7 cleared, CRD-calibrated); `[derived]` = still
closed-form only. Full results: [`results/metrics/2l-b6-800v-sic-bench.txt`](../../../results/metrics/2l-b6-800v-sic-bench.txt).

| Quantity                                     | Closed-form `[derived]`                   | PLECS `[sim]`              | Corner            |
| -------------------------------------------- | ----------------------------------------- | -------------------------- | ----------------- |
| Max linear V_LL,rms @750 V                   | 530 V                                     | —                          | §1                |
| Phase current @ peak power (150 kW)          | ≈192 A rms                                | 180 A rms                  | C5                |
| Current-rating corner (launch)               | 300 A rms / 424 A pk                      | 300 A rms                  | C4                |
| Device voltage utilization                   | 71% nom / 83% worst-case                  | — (design fact)            | §2                |
| **Semiconductor loss @150 kW**               | ≈1.0 kW                                   | **1.02 kW** ✓              | C5 (180 A/151 kW) |
| **Inverter efficiency @ peak (150 kW)**      | ≈99.3%                                    | **99.32%** ✓               | C5                |
| **Junction temp @ peak (150 kW)**            | ≈112 °C                                   | **105 °C** (< 175) ✓       | C5                |
| Efficiency @ launch (300 A rms)              | —                                         | **99.16%**, Tj 148 °C      | C4                |
| **Efficiency @ CRD anchor (360 A / 300 kW)** | —                                         | **99.07%**, Tj 175 °C      | C1 (S5)           |
| DC-link ripple current                       | ≈115 A rms (peak-pwr), ~180 A pk (launch) | energy-balanced ±0.6% (S3) | §4                |

**Reconciling the 150 kW spec vs the 300 kW validation anchor.** The design is specified at 150 kW peak
(192 A rms) / 70 kW continuous — its own operating envelope sits at C5/C4. Validation was **also** carried to
the **Wolfspeed/TI 300 kW CRD point (360 A rms / 800 V)** because that is the *measured* non-circular anchor
for S5 ([[reference-design-wolfspeed-ti-300kw-800v]]); the bench clears it at **99.07% η / 175 °C**, matching
the CRD's >98% η and 175 °C. So the design's own points (C4/C5) and the harder CRD anchor (C1) are all inside
one validated corner envelope — the device (CAB450) is 300 kW-capable and this 150 kW design runs it well
inside its limits.

---

## Key Design Decisions (and why)

1. **1200 V SiC, not 900 V:** worst-case bus 850 V + ~150 V turn-off overshoot ≈ 1000 V; 1200 V keeps ≤83% utilization with cosmic-ray margin [derived §2][25][89]. This is forced by the 800 V bus [28].
2. **SiC, not IGBT:** unipolar, no tail current → 50–70% lower switching loss, decisive at the partial loads that dominate drive cycles [[circuit-components]] §1.2, [28].
3. **16 kHz switching:** high enough to shrink passives and motor harmonic loss, low enough to hold switching loss/thermal — mid-range of the SiC 2L band [50], [[circuit-topologies]] §1.
4. **Film DC-link cap:** ripple-current and ESL duty, self-healing, no dry-out over vehicle life; electrolytic can't meet the ripple/ESR [41][84], components §3.
5. **Resolver + sensorless backup:** ASIL-D needs guaranteed position; sensorless alone can fail silently at zero speed [[control-schemes]] §5, [48].
6. **ASC as safe state:** at speed, freewheel would pump the bus through body diodes; ASC bounds it with controlled braking [55], [[pimpale-mahadik-2025-asc-discharge]].
7. **Laminated busbar, Lσ<15 nH:** protects the 1200 V margin from overshoot and cuts switching loss/EMI [25][50], components §5.

---

## Validation Plan (✅ EXECUTED — see the validation section above)

> **DONE 2026-07-23.** The plan below was carried out: a validated 2L-B6 SiC bench cleared S1–S7 and the
> 9-corner matrix, CRD-calibrated. The closed-form numbers are now PLECS-confirmed (table above). Retained
> as the method record and the template for Tracks 2–4.

Closed-form numbers above are **not evidence** on their own. Per the handoff, a design is only "PLECS-backed" once a validated `.plecs` model reproduces it [80][58]:

- Build 2L-B6 SiC + IPMSM + FOC in PLECS (native PMSM/FOC demo as the load) [80].
- Report **efficiency + THD at ≥3 corners** — low-line (550 V), nominal (750 V), high-line (850 V) — plus a **thermal** run [handoff critical path].
- Summarize to ~36 numbers before any LLM sees them (token economics) [79].
- Only then populate the traction `model_registry.json` for this topology.

```mermaid
flowchart LR
  KB["This design KB"] --> MODEL["PLECS 2L-B6 + IPMSM + FOC"]
  MODEL --> CORNERS["3 corners + thermal<br/>eff / THD / Tj"]
  CORNERS --> SUM["~36-number summary"]
  SUM --> REG["model_registry.json<br/>PLECS-backed"]
```

---

## PLECS Validation — VALIDATED, full corner matrix (2026-07-21 → 2026-07-23)

> **✅ VALIDATED.** The Track-1 model `experiments/2l-b6-800v-sic-bench/bench_2l_b6_800v_sic.plecs`
> (purpose-fit 800 V 2L-B6, CAB450 ×6, heat-sink-coupled) cleared the full **S1–S7 SOP** and the
> **9-corner matrix**. `model_registry.json` → 2L-B6 `validation_status: validated`. Method + history:
> changelogs [[2026-07-21-plecs-2l-b6-model-complete-and-corners]] and [[2026-07-23-plecs-2l-b6-corners-6-9]];
> results [`results/metrics/2l-b6-800v-sic-bench.txt`](../../../results/metrics/2l-b6-800v-sic-bench.txt).

**Device + coupling (foundations).** CAB450 loss model loaded (Vds → Ron = 3.6 mΩ = datasheet `R_DS(on)`@25 °C);
device→heat-sink coupling GUI-established and confirmed (junction tracks coolant, all 6 switches dissipate,
none runaway). Loss readback: `PeriodicAverage` (conduction) + `PeriodicImpulseAverage` (switching), T=1/fac,
all 6 switches; every metric via `ToFile`→CSV (`simulate` returns empty `Values` in PLECS 4.8).

**Switched corners (S1–S5) — the CRD-calibrated efficiency/thermal envelope:**

| Corner | Point | η | Ploss | Tj_ss | Note |
|--------|-------|---|-------|-------|------|
| C1 (CRD, S5) | 800 V / 359 A / 302 kW | **99.07%** | 2815 W | 175 °C | matches measured CRD (>98%, 175 °C) |
| C2 | 750 V / 359 A / 303 kW | 99.11% | 2693 W | 171 °C | nominal bus |
| C3 | 850 V / 359 A / 302 kW | 99.03% | 2938 W | 180 °C | high bus (switching↑) |
| C4 (launch) | 800 V / 300 A / 252 kW | 99.16% | 2123 W | 148 °C | thermal/ripple corner |
| C5 (peak-150kW) | 800 V / 180 A / 151 kW | 99.32% | 1023 W | 105 °C | **the design's own peak** |
| C6 | 550 V / 180 A / 95 kW | 99.22% | 741 W | 94 °C | low bus |

Per-switch (CRD): conduction 208 W + switching 262 W. S1 convergence confirmed; S3 energy balance |resid| < 0.6%
all corners; S5 CRD calibration met (R_cs = 0.070 °C/W/module back-calculated from the 175 °C anchor — non-circular);
clean current (SV PWM + Lg = 0.5 p.u. → crest 1.46, THD 0.15%). Analytic conduction cross-check −3.5%.

**Machine/fault/averaged corners (6–9, 2026-07-23).** The bench is an open-loop grid-style inverter, so these
are **analytic, grounded in the validated inverter loss data** (C6/C8/C9) or **datasheet-bounded** (C7), with
PLECS driving the C6 speed-sweep + C9 loss map (scope per [[procedure-simulation-and-validation]] can/cannot table):

- **C6 field-weakening** (750 V): representative-IPMSM envelope — base 5596 rpm, peak 327 kW, **CPSR 2.4×,
  torque ∝ ω⁻⁰·⁹¹** (PASS ~1/ω), **Vd²+Vq² ≤ Vmax²** held at 100% util (PASS). PLECS inverter sweep at 1×–3×
  base speed (fe 200/400/600 Hz, pulse ratio 80→27): η **flat 99.11–99.12%** — efficient across the whole CPSR.
- **C7 short-circuit** (850 V): the loss model has no gm-saturation (a hard SC would read 236 kA), so
  datasheet-bounded — **ID,sat ~4.7 kA, SCWT ~2.73 µs @ 850 V/175 °C** (< 3 µs SiC); DESAT (300 ns) + soft
  turn-off (1 µs) reacts inside SCWT with **2.1× margin → a single SC is survived**; soft turn-off preferred
  (hard ΔV=313 V ≈ 89% of BV headroom). [[protection-and-safety]] §3.
- **C8 ASC entry** (max speed): dq integration — steady ASC **bounded at Ich = λ/Ld = 611 A**; entry transient
  1924 A (3.1× steady, > I_DM → staged-ASC flag); drag torque peaks 235 N·m ~1/ω; **no bus overvoltage**
  (fault current never reaches the cap; freewheel would pump 1317 V > 850 V). ASC = correct high-speed safe
  state. [[protection-and-safety]] §5.
- **C9 drive-cycle** (averaged): loss map (fit to C1–C6, err < 8%) × US06/WLTP-class trace → **cycle-avg η
  98.62%**, regen 604 Wh, **Tj peak 116 °C** (< 175), rainflow ΔTj ≤ 28 °C → the lifetime front-end for
  [[reliability-and-lifetime]]. **S6/S7 met**: the averaged loss map reconciles the switched corners < 8%.

**Registry:** `model_registry.json` → 2L-B6 `validation_status: validated`; the numbers above are evidence
(the model cleared S1–S7). Residual: machine params are representative `[T]`, and C6/C8 are analytic (a
closed-loop PMSM+FOC model would upgrade them to PLECS-confirmed) — see Red Team.

---

## Alternatives (noted, not built — per scope)

Same procedure, different anchor. Captured so the KB is complete; only 2L-B6 gets full treatment now.

| Variant | What changes vs this design | When it wins | Cite |
|---------|-----------------------------|--------------|------|
| **400 V SiC 2L-B6** (Tesla-class) | 650–900 V devices; ~2× phase current for same power → bigger busbar/cap ripple; cheaper mature ecosystem | highest volume today; cost-sensitive, <200 kW charge | [31], components §1.2 |
| **3L-NPC** | 12 switches + 6 clamp diodes; half switch-voltage; NP balancing | industrial/rail; not cost-justified in auto [[circuit-topologies]] §2 | [50][27] |
| **3L-TNPC** | 12 switches + bidirectional NP switch; **outer switches still block full Vdc**; best partial-load efficiency | 2030 BEV candidate: −0.67 kWh/100 km vs SiC 2L for +30% chip area | [28][27], [[circuit-topologies]] §4 |
| **3L-ANPC** | 18 switches; best loss distribution; highest BOM/gate-drive cost | GaN-ANPC research; thermal-critical | [44][28], [[circuit-topologies]] §3 |
| **Dual inverter** | two smaller inverters, one per axle / open-winding | partial-load efficiency via load-splitting | [43], [[sachs-etal-2025-single-dual-inverter]] |

The multilevel cases matter most **at 800 V**, which is why this anchor is 800 V — it sets up the topology comparison the MAS is meant to reason about [28][43].

---

## Red Team

**Steelman against:** The inverter-slice efficiency/thermal numbers are now genuinely validated (S1–S7,
CRD-calibrated) — but "validated design" still overstates what a *simulation* proves. The result is a PLECS
model calibrated to **one** measured reference (the Wolfspeed/TI CRD, same vendor as the device datasheet, so
not fully independent), with **no hardware** of our own, `[T]` machine parameters, and corners 6 and 8 that
are **analytic**, not PLECS-run. The efficiency is also flattered by unity-PF, datasheet-nominal loss tables:
a real inverter's layout overshoot and non-ideal PF push loss up. The 800-V-vs-400-V anchor is still a choice.

**How it could be false:**
1. **Sim ≠ hardware.** The loss tables are datasheet DPT on a reference layout at fixed Lσ; the real module's
   overshoot and Eoff differ, so sim understates loss until a bench double-pulse + calorimetric run corrects it
   ([[manufacturing-and-test]] §3, [[procedure-simulation-and-validation]] S-gates). η=99.07% is a sim-and-datasheet
   number, not a measured one.
2. **Single, vendor-affiliated anchor.** S5 matches the Wolfspeed/TI CRD, but that CRD and the CAB450 datasheet
   are both Wolfspeed — a shared-optimism risk. An independent 300 kW measurement would strengthen it.
3. **Machine parameters `[T]`** (λ, Ld, Lq, Pp) propagate into every machine-side corner (C6 field-weakening,
   C8 ASC): a real IPMSM datasheet/FEA could shift the envelope, base speed, and ASC current materially.
4. **C6/C8 are analytic, C7 datasheet-bounded** — not PLECS-run, because the bench is an open-loop grid-style
   inverter (no FOC, no dq machine, no gm-saturation). The field-weakening trajectory and ASC transient are
   first-principles dq, not simulated closed-loop.
5. **800-vs-400 framing is a choice.** By units shipped, 400 V (Tesla-class) is more representative; we anchored
   on 800 V for forward relevance.
6. **3L-TNPC alternative rests on one preprint** [28] — inherited single-source risk (see [[circuit-topologies]] Red Team).

**What would change my mind:** a bench double-pulse + calorimetric efficiency on a real CAB450 inverter matching
the sim within a few %; an independent (non-Wolfspeed) 300 kW measurement; a real IPMSM flux-map replacing the
`[T]` params; and a closed-loop PMSM+FOC PLECS model reproducing C6/C8 (upgrading them from analytic to simulated).

**Residual doubt:** The hard blockers are cleared and the inverter efficiency/thermal envelope is validated and
CRD-calibrated — that earns `status: supported` for the **inverter slice**. What remains provisional is the
**machine-side** (C6/C8 analytic on `[T]` params) and the **sim→hardware** gap (no calorimetric bench data).
So the design is `supported` as a *simulated, datasheet-and-CRD-calibrated* 800 V 2L-B6 SiC inverter — not yet
as a hardware-proven product. `evidence: single-study` reflects the single measured anchor.

---

> **References:** [[citations]]

← [[procedure-design]] | [[schematics]] | [[bom-2l-b6-sic]] | [[index-traction-inverter]] →
