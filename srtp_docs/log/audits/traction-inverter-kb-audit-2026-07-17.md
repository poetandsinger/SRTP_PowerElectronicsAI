---
title: "Traction Inverter Build-Manual Audit — 2026-07-17"
type: audit
field: project
created: 2026-07-17
updated: 2026-07-17
tags: [power-electronics, traction-inverter, audit, design, index]
---

# Traction Inverter KB Audit — Build-Manual Completeness

Audit of `power-electronics/traction-inverter/` after the 2026-07-17 design pass (design procedure, schematics, BOM + price DB, 4 reference designs) and the preface move. Goal: is this a **complete manual for building a traction inverter**, RAG-ready and fully cited? Critical, question-driven.

## 1. What This Pass Did

- **Restructured:** `power-electronics/` now holds **only** traction-inverter engineering. Moved `problem-statement/` → vault root (preface); confirmed `market-trends`/`matlab-modeling`/`simulation-toolbox`/`topology-landscape` already deleted (consolidated).
- **Added design cluster:** [[design-procedure]], [[schematics]] (mermaid), [[bom]], [[bom-price-database]].
- **Added reference designs:** [[reference-designs-index]] + 3 real ([[reference-design-wolfspeed-ti-300kw-800v|Wolfspeed/TI 300kW]], [[reference-design-tesla-model3-400v-sic|Tesla]], [[reference-design-nissan-leaf-400v-igbt|Nissan Leaf]]) alongside the synthetic anchor.
- **Researched "why AI":** updated [[problem-statement-index]] with sourced workforce [97], market [96], and demonstrated-capability [60][81][61] evidence; softened the unsourced cost/time figures.
- **Citations [91]–[100]** added for reference designs, prices, market, workforce.

## 2. Citation Coverage — Assessment

| Layer | State |
|-------|-------|
| Reference designs | **Well-cited** — real vendor/teardown sources [91][92][94][95]; anchored prices [98] |
| "Why AI" | **Improved** — workforce/market/capability now sourced [96][97][60][81]; cost/time still `[T]` (flagged) |
| Design procedure numbers | **Cited but derived** — formulas cited [25][50][84], but results are closed-form `[derived]` on `[T]` motor params — **not validated** |
| Standards | **Cited by designation only** [85]–[89] — texts paywalled, not read in full |
| Prices | **Mixed** — 3 anchored (module/MCU/driver [98]); rest `[T]` class estimates |

**No bare uncited claims found** in the new notes — every number carries `[NN]`, `[T]`, or `[derived]`. That was the standard set mid-task and it holds.

## 3. Gaps (prioritized) — is this really a full build manual?

**P0 — blocks "trustworthy":**
1. **Nothing is PLECS-validated.** Every efficiency/THD/thermal/current number is closed-form or teardown-reported. The handoff makes PLECS the ground truth; until the 2L-B6 model runs at 3 corners, the manual is a *design scaffold*, not verified. → build the model against the Wolfspeed/TI CRD metrics (>98%, 32 kW/L) as calibration [91].
2. **Motor parameters are `[T]` placeholders.** No real IPMSM datasheet; every operating point inherits this. → obtain one datasheet or PLECS saturation-LUT machine.

**P1 — CLOSED in the 2026-07-17 textbook pass (2):** dedicated, web-researched, cited chapters added — [[thermal-design]], [[gate-driver-design]], [[protection-and-safety]] (with safety-factor/derating table), [[emi-emc-design]], [[packaging-and-layout]], plus [[design-tradeoffs]] ("how to compromise") and a second [[worked-example-400v-150kw]]. Citations [101]–[126] added (real datasheet/app-note/standard/paper sources). "research synthesis"-style meta files removed; two research-pass filenames renamed to clean chapter names.

**P1 — still open:**
6. **Full board BOM** — BOM is class-level + price DB; snubbers, sense conditioning, protection ICs, connectors, passives still not enumerated. The TI TIDUF23A design guide has a complete BOM not yet parsed [91].

**P2 — CLOSED in the textbook pass:** [[reliability-and-lifetime]] (power-cycling Nf data, LESIT/CIPS08 models, mission-profile/Miner, SiC degradation), [[manufacturing-and-test]] (sinter/bond, double-pulse, HIL, EOL, quality), and [[materials-and-properties]] (consolidated property reference) added; citations [127]–[148]. Reliability subagent flagged CIPS08 coefficients and Miner `LC=1` as the load-bearing uncertainties — captured in that chapter's Red Team.

**P2 — still open:**
9. **Multilevel reference designs** (3L-NPC/TNPC/ANPC) and GaN/dual-inverter are *noted only*, not built — the manual is 2L-deep by design.

## 4. Structural / Link Hygiene

- **`research-synthesis-2025-2026`** — **RESOLVED (deleted 2026-07-17):** the meta "synthesis hub" was removed per the "no research-synthesis files" directive; its engineering pointers are covered by the index, its AI/market pointers by [[problem-statement-index]] and the ai-agents notes. `standards-landscape-2025-2026` → `standards-and-compliance`, `simulation-workflows-2025-2026` → `simulation-and-validation`.
- **`[[audit-changelog-traction-inverter]]`** (linked from the index) resolves by basename but the path is wrong (file is under `audits/`). Minor; Obsidian resolves it.
- **Historical audits/changelogs** still reference deleted notes (`matlab-modeling`, etc.) — **intentional** per handoff (they record old structure); not fixed.
- **`.obsidian/workspace.json`** references old paths — editor state, regenerates; ignore.

## 5. Open Questions (for the human)

1. **Anchor voltage:** primary reference = 800 V (forward-looking) vs 400 V (Tesla-class, highest volume)? A judgment was made (800 V); confirm.
2. **Manual depth:** add the P1 chapters (EMI, packaging, PCB layout, full BOM) now, or keep the manual 2L-electrical-focused and push those to the MAS/PLECS phase?
3. **Prices:** is a class-level price DB with 3 anchored parts enough, or parse the full TI CRD BOM [91] for a complete priced board?
4. **research-synthesis:** engineering or preface — keep in `power-electronics/` or move to root?

## 6. Verdict

The folder is now a **dense, cited 2L-B6 SiC textbook** (**29 chapters**): fundamentals → topology → components → **materials** → machine → control → sizing → schematics → **thermal → gate-drive → protection/safety-factors → EMI/EMC → packaging/layout** → BOM/prices → trade-offs → two worked examples → real reference designs → **manufacturing/test → reliability/lifetime** → standards → simulation → open problems. Every quantitative claim carries `[NN]`/`[T]`/`[derived]`; every chapter has a red-team. Numbers are grounded in real datasheets/app-notes/standards/papers (CAB450M12XM3, UCC5880-Q1, CISPR 25, AQG 324 04.1/2025, LESIT/CIPS08, NREL, MDPI reviews); citations run [1]–[148].

**The one gap that still matters (P0):** it is **not PLECS-validated** — the design/thermal/loss numbers are closed-form or teardown/vendor figures, not simulation ground truth. Secondary: a full board BOM (parse TI TIDUF23A) and multilevel (3L) reference designs. Those are the next steps, stated in each chapter's Red Team rather than hidden.

---

> **References:** [[citations]]

← [[traction-inverter-index]] | [[catalog.base]] | [[ai-agent-docs-audit-2026-07-17]]
