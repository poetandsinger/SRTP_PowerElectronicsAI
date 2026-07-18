---
title: "Reference Design — Nissan Leaf 400V Si-IGBT (production baseline)"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, design, reference-design, two-level, igbt, dc-link]
review_by: 2026-10-17
---

## What This Is

The **Si-IGBT baseline**: a high-volume, cost-driven 400 V traction inverter with none of the SiC premium. Here to show what the SiC designs are measured *against* — the incumbent technology, its DC-link and cooling choices, and why IGBT still ships in cost-sensitive 400 V BEVs [95], [[components]] §1.1.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge. Specs are teardown-derived (`reliability: low–medium`) [95][32].

---

## Specification (teardown-derived) [95][32]

| Item | Value | Note |
|------|-------|------|
| Topology | 2-level B6 | IGBT module bridge |
| DC bus | ~400 V (350–403 V pack) | |
| Motor / power | PMSM, **80 kW**, 280 N·m | 2018 gen |
| Devices | Si IGBT module (+ anti-parallel diodes) | brazed module, not direct-cooled early gen |
| DC-link cap | **1088 µF, 600 V, SH film** | notably larger than SiC designs — IGBT ripple + lower fsw |
| Peak phase current | ~200–222 A | at 80 kW / ~400 V, ~90% total efficiency [95] |
| Cooling | water-glycol cold plate | |

---

## What It Teaches

- **IGBT needs more DC-link capacitance:** 1088 µF here [95] vs the ~300–600 µF the design procedure sizes for a *higher-power* SiC design [[design-procedure]] §4. Lower switching frequency and higher ripple demand more capacitance — a concrete illustration of the SiC "smaller passives" advantage [[components]] §1.2, §3.
- **~90–95% system efficiency** [95] vs >98% for SiC 800 V [91] — the efficiency gap that justifies the SiC premium at higher power/voltage [28].
- **Cost/simplicity floor:** for <100 kW, 400 V, cost-sensitive vehicles, IGBT 2L stays rational — why [[circuit-topologies]] calls SiC a *high-power/high-voltage* win, not a universal one.

---

## Red Team

**Steelman against:** Reconstructed from enthusiast and analyst teardowns [95], the weakest source class in the cluster. The 1088 µF figure and efficiency numbers come from a DIY teardown blog and a MarkLines summary — not Nissan data. Generation mixing (2011 / 2013 / 2018 Leaf) blurs which spec belongs to which car.

**How it could be false:**
1. **Source reliability low:** hobbyist teardowns can misread ratings [95].
2. **Generation confusion:** Leaf changed inverter across 2011/2013/2018; specs may be cross-contaminated.
3. **Efficiency "~90% total"** conflates motor+inverter; inverter-only is higher [95].

**What would change my mind:** a Munro/UBS Leaf teardown report [32] or Nissan service documentation with the exact IGBT part and DC-link rating.

**Residual doubt:** Good enough for the qualitative IGBT-vs-SiC contrast (bigger cap, lower efficiency, lower cost); not for exact numbers. The *direction* is solid and well-corroborated across the vault [[components]].

---

> **References:** [[citations]]

← [[reference-designs-index]] | [[reference-design-tesla-model3-400v-sic]] →
