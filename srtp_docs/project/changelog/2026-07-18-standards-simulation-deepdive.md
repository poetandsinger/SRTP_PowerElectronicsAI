---
title: "2026-07-18 — Standards substance + PLECS simulation deep-dive"
type: changelog
field: project
created: 2026-07-18
updated: 2026-07-18
tags: [changelog, power-electronics, standards, plecs, simulation]
---

# 2026-07-18 — Standards substance + PLECS simulation deep-dive

Depth-first research pass over every topic in [[power-electronics/traction-inverter/traction-inverter-index]], hunting the "names the thing but never says what it is" gap. The vault is mature (29-chapter textbook, cited [1]–[148]) — most chapters already carry real numbers and red-team blocks. Two chapters were the genuine offenders and got rewritten; the rest were spot-checked and left as-is.

## What changed

- **[[power-electronics/traction-inverter/standards-and-compliance]]** — was a table of standard *designations*. Now states **what each standard actually requires**: IEC 61800-5-1 DVC/creepage-clearance worked numbers (≈8–11.4 mm creepage at 800 V reinforced) + ≤60 V/5 s discharge; ISO 26262 ASIL = S×E×C and the HW-metric targets (SPFM ≥90/97/99%, LFM ≥60/80/90%, PMHF <100/<100/<10 FIT for B/C/D); IEC 61800-5-2 STO/SS1/SS2/… sub-functions; AEC-Q101/Q100/Q200 stress suites with conditions; AQG 324 PCsec/PCmin split + EOL (+5% Vf / +20% Rth) + SiC annex (DGS/DRB); CISPR 25 Class-5 dBµV limit table; ISO 7637-2/-4 pulses; LV123/124; ISO 6469-3/R100 (≥100 Ω/V, ≤0.2 J). Added the missing **Red Team** block. Every number carries an **[H]/[M]/[TPS]** reliability tag; the paywalled/NOT-FOUND items (exact DVC boundaries, stated 800 V creepage, LV123 sub-classes, AQG 324 DGS/DRB voltages) are called out honestly.
- **[[power-electronics/traction-inverter/simulation-and-validation]]** — was a tool catalogue + a 10-phase ASCII flow that duplicated the manufacturing chapter. Rewritten to the **model side**: the four PLECS modelling layers (circuit → loss table → thermal network → plant), switched-vs-averaged fidelity choice, and a concrete **9-row corner-test matrix** (double-pulse, 3-corner efficiency, thermal, DC-link ripple, overmodulation, field-weakening, short-circuit, ASC, drive-cycle) each tied to a design-procedure step and pass criterion. Added the missing **Red Team** block (scopes "PLECS-validated" to circuit+thermal+control; EMC/parasitics/fatigue explicitly out of scope). HIL/V-model deferred to [[power-electronics/traction-inverter/manufacturing-and-test]] to kill duplication.

## Grounding — PLECS MCP (applied the "clone it locally" tip)

Cloned **PE-MAS** ([72], `github.com/spongelovesorange/PE-MAS`) and read its real **PLECS-MCP server** (`plecs-mcp/`): ~30 MCP tools wrapping PLECS XML-RPC (`plecs.load` / `plecs.simulate(model, {ModelVars, StartTime, StopTime})` / `plecs.set/get` / `plecs.eval`, transactional circuit-edit + rollback, capability discovery). Used it to replace the hand-wavy "scriptable, lets an agent drive it" sentence in the simulation chapter with the concrete method surface + `ModelVars` sweep mechanism.

## Logistics

- **[[citations]]** — added **[149]–[157]** (TI SLUAAR5 creepage; IEC 61800-5-2 functions; ISO 26262 metrics; AEC-Q101/Q100/Q200 base docs; AQG 324 04.1/2025; ISO 7637; LV123/124 + ZVEI; ISO 6469-3/R100). Reused [85][86][88][89][113][114][115][124][137][141].
- **[[README]]** citation range [1]–[148] → **[1]–[157]**.
- **[[power-electronics/traction-inverter/traction-inverter-index]]** — bumped `updated`; fixed broken audit-changelog wikilink (`power-electronics/…` → `audits/…`).
- **[[audits/audit-changelog-traction-inverter]]** — appended a 2026-07-18 verification section.

## Audit

Citation integrity (all refs in both files defined in citations.md) ✅ · wikilink integrity (12/12 resolve) ✅ · both files < 200 lines, Red Team + nav footer + citation-convention present ✅. ISO 26262 metrics and CISPR 25 FM limits independently corroborated against a second source before commit.

## Not done (noted, not fixed — out of scope)

- `what-is-a-traction-inverter.md` uses ASCII block diagrams where SCHEMA prefers mermaid (content is correct; purely cosmetic).
- The paywalled exact values flagged **[TPS]/NOT-FOUND** in the standards chapter remain to be confirmed against purchased standard texts + the program's own EMC/HV spec.

← [[changelog-index]] | [[power-electronics/traction-inverter/traction-inverter-index]]
