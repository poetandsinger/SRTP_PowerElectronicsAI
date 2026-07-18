---
title: "Design Trade-offs — How to Compromise"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
sources: [sources/power-electronics/sachs-neuburger-2025-3l-tnpc, sources/power-electronics/sachs-etal-2025-single-dual-inverter]
tags: [power-electronics, traction-inverter, design, efficiency, thd, emi, sic, two-level, three-level]
review_by: 2026-10-17
---

## What This Is

No traction inverter maximizes every objective — each choice buys one metric by spending another. This chapter is the **compromise map**: the recurring decisions, what each trades, and the rule of thumb for resolving it. It sits on top of [[procedure-design]] (which sizes a *fixed* choice) and the reference designs (which are *points* on these trade curves).

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; `[derived]` → from [[procedure-design]].

## The Objective Vector

You are optimizing, simultaneously and in tension:

| Objective | Driven by | Conflicts with |
|-----------|-----------|----------------|
| Peak efficiency | device, fsw, topology | cost, power density |
| **Drive-cycle** efficiency | partial-load behavior (SiC unipolar, multilevel) | cost [28] |
| Power density (kW/L) | fsw↑ (smaller passives), cooling | efficiency, EMI, reliability |
| Cost ($/kW) | device area, cap, cooling | efficiency, density [29] |
| THD / current ripple | fsw↑, multilevel | switching loss, cost |
| EMI | dv/dt↓, fsw↓, filtering | efficiency, density |
| Reliability / lifetime | Tj margin, derating | cost, density |
| NVH (acoustic) | fsw (above ~10–15 kHz inaudible), PWM pattern | switching loss |

**The core tension:** efficiency and power density both want high fsw and SiC; cost, EMI, and reliability all push back. There is no free axis [28][50].

## The Big Decisions

### 1. Device — Si IGBT vs SiC MOSFET vs GaN
- **Buy with SiC:** 50–70% lower switching loss, higher fsw → smaller passives, far better **partial-load** efficiency (unipolar, no tail current) [[components]] §1.2, [28].
- **Pay:** 1.5–2.5× device $/A (falling) [29]; faster dv/dt → worse EMI and motor-insulation stress [54][87]; lower short-circuit withstand (3–5 µs vs 10 µs) → harder protection [40].
- **Rule:** SiC wins at **high voltage/power and cycle-efficiency-critical** designs; IGBT still rational **<100 kW, 400 V, cost-first** [[reference-design-nissan-leaf-400v-igbt]]; GaN not yet traction-ready (650 V, current limits) [[components]] §1.3.

### 2. Voltage class — 400 V vs 800 V
- **Buy with 800 V:** half the current for a given power → lower I²R and busbar/connector loss, faster charging; higher density [28].
- **Pay:** forces 1200 V devices (no cheap 650 V option), higher isolation/creepage spec, smaller mature-ecosystem [derived §2][28].
- **Rule:** 800 V for **new premium/high-power** platforms (the industry direction); 400 V for **cost-sensitive, highest-volume today** (Tesla-class) [[reference-design-tesla-model3-400v-sic]] [94].

### 3. Switching frequency
- **Buy with fsw↑ (e.g. 8→20 kHz):** smaller DC-link cap and motor harmonic loss, lower THD, above ~15 kHz pushes PWM tone out of hearing (NVH) [50].
- **Pay:** switching loss ∝ fsw → lower efficiency, higher Tj; worse EMI [derived §3][25].
- **Rule:** pick the **lowest fsw that meets THD + NVH + passive-size targets**; SiC's low loss lets you afford 10–20 kHz where IGBT is stuck at 8–12 kHz [[circuit-topologies]] §1.

### 4. Topology — 2L vs 3L (NPC / TNPC / ANPC)
- **Buy with 3L:** ~½ dv/dt and switch voltage stress, lower THD at equal fsw, best partial-load efficiency (3L-TNPC: −0.67 kWh/100 km vs SiC 2L for +30% chip area) [28][27].
- **Pay:** 12–18 switches vs 6, neutral-point balancing, gate-drive count and BOM/control complexity [[circuit-topologies]] §5.
- **Rule:** 2L dominates production (>95%) because SiC-at-800 V already closes most of the gap; 3L-TNPC is the **2030 partial-load-efficiency play**, only compelling at 800 V and if SiC $/area keeps falling [28][43].

### 5. Modulation — SVPWM vs DPWM vs overmodulation
- **SVPWM:** best THD, full linear range to MI 0.907 [50], [[control-schemes]] §4.2.
- **DPWM:** ~33% lower switching loss at the cost of THD — used at high load/speed [50] §4.3.
- **Rule:** SVPWM at light load (THD/NVH), switch to DPWM1 at high load (efficiency), overmodulate for peak torque/field-weakening headroom [50] §4.4.

### 6. Cooling — single vs double-sided, pin-fin vs jet
- **Buy with better cooling:** higher continuous current from the same silicon (Zth-limited) → smaller/cheaper module for a power target [25].
- **Pay:** complexity, cost, pumping, packaging volume.
- **Rule:** pin-fin water-glycol is the default (10–20 kW/L); jet-impingement/double-sided when density-limited (Tesla/Lucid) [[components]] §6.1, [94].

### 7. Module architecture — many small vs few large
- **Many small 2-in-1 (Tesla, 24 modules):** spreads heat/current, uses mature small die, easy paralleling [94].
- **Few large half-bridge (Wolfspeed CAB450, 3 modules):** lower part count, lower loop inductance, simpler assembly [91][92].
- **Rule:** driven by thermal spreading, loop inductance target, and supply chain — both ship in volume.

## Decision Table (given a spec, start here)

| If the spec emphasizes… | Lean toward |
|--------------------------|-------------|
| Lowest cost, <100 kW, 400 V | Si IGBT, 2L, 8–12 kHz, pin-fin |
| High cycle efficiency + fast charge | SiC, 800 V, 2L, 12–20 kHz |
| Max range at fixed pack (2028+) | SiC, 800 V, **3L-TNPC**, partial-load-optimized [28] |
| Max power density (performance) | SiC, 800 V, double-sided cooling, higher fsw [94] |
| Lowest EMI / long motor cables | lower dv/dt (Rg↑ or 3L), stronger CM filter [54] |

## How To Choose (heuristic)

1. Fix **voltage class** from the pack/charging spec (400 vs 800). 
2. Fix **device** from cost-vs-cycle-efficiency priority (IGBT vs SiC).
3. Fix **topology** — default 2L unless partial-load efficiency is the top objective and budget allows 3L.
4. Set **fsw** to the lowest value meeting THD+NVH+passive-size.
5. Size everything ([[procedure-design]]), then **validate the compromise in PLECS** at 3 corners — the trade-offs only become real numbers there [80].

## Red Team

**Steelman against:** This chapter states trade directions as if they were laws, but the crossover points are design-, cost-, and year-specific. "SiC wins above X kW" has no fixed X — it moves with SiC $/area [29], cooling, and drive cycle. The 3L-TNPC advantage rests on a single preprint [28] (see [[circuit-topologies]] Red Team). And "lowest fsw that meets targets" hides that the targets themselves trade against each other.

**How it could be false:**
1. **Crossovers are not fixed** — device pricing [29] and mission profile move every threshold; the table is directional, not prescriptive.
2. **Single-source multilevel claim** — the TNPC number is one preprint [28], unreplicated.
3. **Objectives are coupled nonlinearly** — treating them as independent axes understates interactions (e.g. fsw affects efficiency *and* EMI *and* NVH *and* cap size at once).
4. **No cost model** — "$/kW" directions are qualitative; real BOM cost needs [[bom-price-database]] + volume quotes.

**What would change my mind:** a PLECS-backed Pareto sweep (efficiency vs cost vs density) across device/voltage/fsw/topology reproducing these directions with numbers; updated SiC pricing shifting the IGBT/SiC crossover.

**Residual doubt:** The *directions* are well-supported and match the reference designs; the *thresholds* are judgment. Use this to frame a design, then let PLECS place the actual crossover.

---

> **References:** [[citations]]

← [[procedure-design]] | [[reference-designs-index]] | [[circuit-topologies]] →
