---
title: "2L-B6 · 6-switch · 800 V SiC Traction Inverter — Design & PLECS Validation"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: theoretical
sources: [sources/power-electronics/sachs-neuburger-2025-3l-tnpc, sources/power-electronics/sachs-etal-2025-single-dual-inverter, sources/power-electronics/wolfspeed-cab450m12xm3-datasheet]
tags: [power-electronics, traction-inverter, design, two-level, sic, inverter, efficiency, thd]
review_by: 2026-10-17
---

## What This Note Is

**Track 1 topology unit** (`design-<topology>-<voltage>-<device>`) and the anchor of the design cluster: an 800 V-class **SiC 2-level B6** traction inverter, 150 kW, driving an IPMSM. Collects the spec, key decisions, and validation plan in one place. This is the first of four topology units ([[circuit-topologies]]); sizing math in [[procedure-design]], diagrams in [[schematics]], parts in [[bom-2l-b6-sic]]. See [[plan-depth-research]] for the serial build order.

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

## Computed Operating Points (first-pass, replace with PLECS)

All **[derived]** in [[procedure-design]]; these are algebra on `[T]` assumptions, not measurements [80].

| Quantity | Value | Where |
|----------|-------|-------|
| Max linear V_LL,rms @750 V | 530 V | §1 |
| Phase current @ peak power | ≈192 A rms | §1 |
| Current-rating corner (launch) | 300 A rms / 424 A pk | §1 |
| Device voltage utilization | 71% nom / 83% worst-case | §2 |
| Semiconductor loss @150 kW | ≈1.0 kW | §3 |
| Inverter efficiency @ peak | ≈99.3% | §3 |
| Junction temp @ peak | ≈112 °C (Tj,max 175) | §3 |
| DC-link ripple current | ≈115 A rms (peak-pwr), ~180 A pk (launch) | §4 |

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

## Validation Plan (the point of the whole thing)

Closed-form numbers above are **not evidence**. Per the handoff, a design is only "PLECS-backed" once a validated `.plecs` model reproduces it [80][58]:

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

**Steelman against:** Calling this a "reference design" overstates it. It is a spec plus first-pass algebra plus decisions justified from literature — no PLECS run, no hardware, `[T]` motor parameters. Every performance number is provisional. The industry-relevance argument for 800 V is also contestable: by units shipped, 400 V is more representative, so "most industry relevant" is a judgment, not a fact.

**How it could be false:**
1. **No validated model exists yet** — the efficiency/THD/thermal figures are unverified estimates [80]; the handoff is explicit that these must come from PLECS.
2. **800-vs-400 framing is a choice.** If the goal were to match the highest-volume production inverter, 400 V (Tesla-class) would be the anchor [31]. We chose 800 V for forward relevance and instructiveness; a reviewer could reasonably prefer 400 V.
3. **The 3L-TNPC advantage rests on one preprint** [28] — see the Red Team in [[circuit-topologies]]; the alternatives table inherits that single-source risk.
4. **Motor parameters `[T]`** propagate into every operating point; a real datasheet could shift currents and PF materially [[procedure-control]] §8.

**What would change my mind:** A PLECS-validated 2L-B6 model at the three corners; a real IPMSM datasheet; and, for the anchor choice, an explicit human decision on 400 V vs 800 V as the primary target (flagged as an open question in the handoff).

**Residual doubt:** Solid as the organizing spine of the design KB and the input to the first PLECS model. Its numbers are a hypothesis to be tested, not a result.

---

> **References:** [[citations]]

← [[procedure-design]] | [[schematics]] | [[bom-2l-b6-sic]] | [[index-traction-inverter]] →
