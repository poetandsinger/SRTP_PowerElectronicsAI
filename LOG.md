# LOG — dev journal

> Dated entries: what changed, why, and what's blocked. Newest first.
> Assembled from the vault changelogs (`knowledge/synthesis/log/changelog/`) and the PLECS Track-1 session notes (`knowledge/synthesis/log/SESSION_LOG_2026-07-19.md`, `system/src/HANDOFF.md`). Strategic direction is in [ROADMAP.md](ROADMAP.md); active tasks in [TODO.md](TODO.md).

---

## 2026-07-20 — repo reorganization plan + schema rules
**What:** Reorganized the whole repo to the `knowledge/ system/ experiments/ results/` layout. Added a `## Repository Organization` section to `knowledge/SCHEMA.md` (two-log-types rule, three-planning-streams sort, papers↔notes matching, migration discipline, read-only zones, gitignore obligations). Authored root `ROADMAP.md`/`TODO.md`/`LOG.md`/`README.md`. Dismantled the Obsidian vault → `knowledge/` (notes, sources; plans/trials/log folded under `knowledge/synthesis/`); harness → `system/src/`, registry → `system/configs/`, Wolfspeed library → `system/env/models/`; all empirical work (worked-designs, PLECS run folders, and the superseded DPT) → `experiments/` (design lines + runs + `experiments/ARCHIVE/`); results.txt → `results/metrics/`. All moves via `git mv` (history preserved). MAS code, when written, starts under `system/`.
**Why:** The repo had accumulated three overlapping schemes (the Obsidian vault, loose `data/plecs/`, `worked-designs/`); one flat structure makes it navigable.
**Notes:** `.mcp.json` kept at repo root (MCP loader needs it there); residual `plans/` specs → `knowledge/synthesis/plans/`; `.base` indexes retired to `knowledge/_archive/`. The graphify graph still indexes pre-move paths — rebuild pending.

## 2026-07-19 — PLECS readback blocker cleared + loss layer activated
**What:** Proved `simulate`'s `Values` is empty in PLECS 4.8; reliable readback is a `ToFile`→CSV (corrects the earlier "top-level Outport verified" claim). Built the reusable harness under `data/plecs/` (template + direct-RPC runner + summarizer + `model_registry.json`). Organized the Wolfspeed PLECS model library (669 models); CAB450M12XM3 loads + simulates. Corrected the SOP/plan/memories/citations ([166]–[170]).
**Why:** Readback gates all downstream evidence — without it nothing counts.
**Blocked (then):** device→heatsink coupling would not reproduce from scratch-scripted `.plecs`.

## 2026-07-19 — 2L-B6 coupling CONFIRMED (blocker cleared)
**What:** Retargeted the shipped `rainflow_counting` demo (a GUI-saved 2L 6-IGBT+6-diode VSI on a heat sink) to CAB450 **purely by text edits** → `2l_b6_rainflow_base/`. Loads, simulates, and is **confirmed heat-sink-coupled**: Tj = 65.3 °C mean, bounded at ambient (uncoupled would run to 684 °C). Key enabler: the **legacy** CAB450 MOSFET file (`class="MOSFET"`, no gate-dependent conduction) is accepted by a plain `Mosfet` block. Correct readout form: top-level `PlecsProbe`, `Component "IGBT1"`, `Path "Circuit"`, signal `"MOSFET junction temp"`.
**Why:** Root cause of the coupling blocker was that the device↔heat-sink association is GUI-baked into the file; the fix is to retarget a GUI-saved base, not author from scratch.
**Blocked:** per-switch validated loss/η/Tj number — needs the 800 V loaded operating point + corner matrix + CRD calibration. Empirically, the earlier 800 V/300 kW rebuild attempt is not yet a validated result.

## 2026-07-19 — vault refactor, naming, validation SOP
**What:** Stage-based folders (`sources`/`notes`/`trials`/`plans`/`log`); 867 links → bare basenames; per-stage `.base` indexes; frontmatter-as-index navigation model in SCHEMA. Added the PLECS validation SOP (gates S1–S7). Topology-unit naming `design-<topology>-<voltage>-<device>`; added TNPC/ANPC/NPC scaffolds.
**Why:** Make the vault filterable by frontmatter and give every design a repeatable validation gate.

## 2026-07-18 — worked examples + design-by-doing
**What:** Invented a family-car 400 V SiC inverter, ran a numerical model (efficiency/thermal/cycle, SiC-vs-IGBT), **confirmed PLECS licensed + a drive simulates**. Added three more worked examples (Class-8 truck / lifetime-rainflow, hypercar / power-density-Zth, 96 V microcar / cost-voltage-lever). Deep-dive rewrite of standards-and-compliance + simulation-and-validation. Citations → [1]–[165].
**Why:** Learn the design workflow by doing it end-to-end before automating it.

## 2026-07-17 — textbook + plan split
**What:** Built the 29-chapter traction-inverter engineering textbook (cited [1]–[148]). Depth-first AI-agent pass: design-loop finding (topology→refine→parameter-optimize + explicit optimizer), workflow-pattern catalog, plan-sufficiency verdict. Split the implementation plan into a hub + 8 topic files (no phases).
**Why:** Establish the domain knowledge base and a spec-level, phase-ready implementation plan.

## 2026-07-06 — project setup + architecture pivot
**What:** Initial 17 research notes + agent-harness survey. Architecture pivot to a standalone app (MATLAB external, later pivoted to PLECS backend per decision A3). Subagent findings integrated (smolagents engine, PulsimGUI reference, NiceGUI). Restructured to a single `citations.md` + descriptive indexes.
**Why:** Stand up the research vault and settle the initial architecture direction.
