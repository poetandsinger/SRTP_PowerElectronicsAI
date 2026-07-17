---
title: "2026-07-17 — Traction-Inverter Textbook Build"
type: changelog
field: project
created: 2026-07-17
updated: 2026-07-17
tags: [changelog, power-electronics, traction-inverter]
---

# 2026-07-17 — Traction-Inverter Engineering Textbook

Turned `power-electronics/traction-inverter/` from a research cluster into a **29-chapter engineering textbook**, cited [1]–[148], every chapter red-teamed.

## Structure
- **`power-electronics/` is now engineering-only.** Moved `problem-statement/` (motivation, market, workforce, competitive landscape) to the **vault root**; updated SCHEMA §1 to register the `problem-statement` field.
- **Removed meta files:** deleted the `research-synthesis-2025-2026` hub; renamed `standards-landscape-2025-2026` → `standards-and-compliance`, `simulation-workflows-2025-2026` → `simulation-and-validation`. Fixed all inbound links (zero dangling links vault-wide).

## Chapters added (web-researched via subagents, cited)
- Design cluster: `design-procedure`, `schematics` (mermaid), `bom`, `bom-price-database` (real dated prices), `design-tradeoffs` ("how to compromise"), `worked-example-400v-150kw`, `materials-and-properties`.
- Subsystem deep-dives: `thermal-design`, `gate-driver-design`, `protection-and-safety` (safety-factor/derating table), `emi-emc-design`, `packaging-and-layout`.
- Build/verify: `manufacturing-and-test`, `reliability-and-lifetime`.
- Reference designs: `reference-designs-index` + Wolfspeed/TI 300kW (real CRD), Tesla Model 3, Nissan Leaf, + synthetic 800V anchor.

## Sourcing
- 7 research subagents (thermal, gate-drive, protection, EMI, manufacturing, reliability + earlier design pass) returned dense cited briefs; authored centrally to keep schema/citation discipline.
- Citations grew [90]→[148]: real datasheets (CAB450M12XM3, UCC5880-Q1), standards (CISPR 25, AQG 324 04.1/2025, ISO 26262), and peer-reviewed lifetime/EMI/thermal papers.

## Honest gaps (see [[audits/traction-inverter-kb-audit-2026-07-17]])
- **P0:** nothing PLECS-validated — numbers are closed-form/teardown/vendor.
- Full board BOM (parse TI TIDUF23A) and 3L reference designs not built.
- Next agent: **depth-first research** — see `HANDOFF-DEPTH-RESEARCH.md` (repo root).

← [[changelog-index]] | [[README]]
