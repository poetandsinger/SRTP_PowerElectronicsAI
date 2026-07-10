# SRTP Research Vault — Schema

> Science Research Vault conventions for power electronics + AI agent architecture research.
> Every claim carries truth-status, evidence-strength, and a red-team block.
> Part of: `RESEARCH_VAULT` = `D:\Engineering Projects\AI\SRTP_PowerElectronicsAI\srtp_docs`

## Fields

| Field | Folder | Domain |
|-------|--------|--------|
| `ee` | `ee/` | Power electronics — traction inverter design: topologies, semiconductors (SiC/GaN/Si), modulation, thermal, control, MATLAB modeling |
| `cs` | `cs/` | AI agent architectures — Claude Code, Codex CLI, OpenCode, Hermes Agent, LangGraph, CrewAI, AutoGen, research agents, architecture patterns |

Field folders are the only Layer-2 content locations. All claim/topic notes live under a field folder.

## Note Types

| Type | Folder | Purpose | Red-team? |
|------|--------|---------|-----------|
| `source` | `sources/<field>/` | Immutable raw capture of one paper/source. Never edited. | no |
| `claim` | `<field>/` | One defensible finding + evidence + red-team. Carries status + evidence. | **required** |
| `topic` | `<field>/` | Synthesis across claims/papers. State of knowledge on a subject. | required if it advances a position |
| `index` | `_index/` | Field/topic hub linking key notes. Navigation only. | no |

**Claim vs topic:** a claim defends *one* checkable finding ("SiC switching losses ~40% below Si IGBT at 100 kHz, 650 V"). A topic synthesizes many ("state of wide-bandgap adoption in traction inverters"). One sharp result → claim. A landscape → topic linking its claims.

**Append-first:** before creating a note, search the vault. If the idea extends an existing note, append and bump `updated` (re-run the red-team if status could shift). Only spawn a new note when the finding is genuinely distinct.

## Frontmatter

### Claim / Topic / Index notes (Layer 2):
```yaml
---
title: Note Title
type: claim | topic | index
field: ee | cs
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: supported | contested | refuted | unverified
evidence: replicated | single-study | theoretical | disputed
tags: [from taxonomy]
sources: [sources/ee/foo.md, doi:10.1234/xyz, arxiv:2401.01234]
contradicts: [slug-of-conflicting-note]
review_by: YYYY-MM-DD
---
```

### Source notes (Layer 1):
```yaml
---
title: Paper Title
authors: [...]
year: YYYY
venue: "journal / conference / preprint server"
doi: 10.1234/xyz          # or:
arxiv: 2401.01234
pmid: 12345678
captured: YYYY-MM-DD
reliability: high | medium | low | unknown
peer_reviewed: true
motivated: true            # omit if not
reliability_note: "..."
sha256: <hash>
---
```

## Truth-Status

- `supported` — corroborated by 2+ independent credible sources; red-team failed to break it.
- `contested` — credible sources disagree, OR the red-team raised a serious unresolved objection.
- `refuted` — evidence shows it false. Keep the note as a record; link what replaced it.
- `unverified` — single source, unknown-reliability source, or not yet cross-checked.

**New claims default to `unverified`.** Never default to `supported` — earn it.

## Evidence-Strength

- `replicated` — independent groups reproduced it; meta-analysis or multiple confirmations.
- `single-study` — one (or a few, but not independently reproduced) papers; no independent replication yet.
- `theoretical` — derived/modeled/simulated, not yet empirically tested.
- `disputed` — replication attempts conflict or have failed.

## Source Reliability

- **high** — primary/original: peer-reviewed papers in credible venues, replicated datasets, standards bodies, direct experimental reports.
- **medium** — solid secondary: reputable preprints (arxiv from known groups), review articles, textbooks, well-run reproductions reported informally.
- **low** — weak/motivated: press releases, vendor whitepapers, marketing, single blog posts, un-refereed theses, popular-science coverage.
- **unknown** — provenance unassessable.

`peer_reviewed: false` (preprint) does not automatically mean low — a preprint from a strong group is often `medium` — but it caps a single-source claim at `unverified` until peer-reviewed or independently reproduced.

**`motivated` is orthogonal to reliability** — a vendor's own well-run benchmark can be `high` *and* `motivated: true`. Motivation does NOT gate status.

**Reliability gates status:** a `low`/`unknown` source can't push a claim past `unverified` on its own.

## Red-Team Block (mandatory on claim notes)

```markdown
## Red Team
**Steelman against:** [Strongest good-faith case the finding is wrong or overstated.]
**How it could be false:** [Concrete mechanism — small n, p-hacking, no controls, cherry-picked regime, unreproduced, motivated funding, sim≠reality, measurement artifact.]
**What would change my mind:** [Specific result that would flip status or evidence-strength.]
**Residual doubt:** [One line — what still nags after reading.]
```

## Tag Taxonomy

Every tag on a note must exist here. Add first, then use.

### Fields
- `ee` — power electronics
- `cs` — computer science / AI

### EE: Power Electronics
- **Topologies:** `topology`, `inverter`, `two-level`, `three-level`, `multilevel`, `npc`, `t-type`, `anpc`
- **Components:** `mosfet`, `igbt`, `gan`, `sic`, `diode`, `capacitor`, `dc-link`, `gate-driver`
- **Modulation:** `pwm`, `svpwm`, `dpwm`, `she-pwm`, `hysteresis`, `mpc`
- **Thermal:** `thermal`, `heatsink`, `junction-temperature`, `cooling`, `thermal-resistance`
- **Control:** `foc`, `dtc`, `sliding-mode`, `observer`, `sensorless`, `pi-control`
- **Performance:** `efficiency`, `thd`, `ripple`, `emi`, `power-factor`, `dvdt`, `switching-loss`
- **Standards:** `ieee`, `iec`, `iso`, `mil-std`, `aec-q`
- **Domain:** `traction-inverter`, `market-research`
- **Method:** `tuning`

### CS: AI / Agent Architecture
- **Agent frameworks:** `claude-code`, `codex-cli`, `opencode`, `hermes-agent`, `langgraph`, `crewai`, `autogen`
- **Agent concepts:** `multi-agent`, `tool-calling`, `delegation`, `orchestration`, `subagent`
- **Architecture:** `architecture`, `patterns`, `comparison`, `integration`, `gui-vs-cli`
- **Engineering AI:** `matlab-integration`, `simulation`, `code-generation`, `design-automation`

### Cross-cutting
- **Method:** `experiment`, `simulation`, `theory`, `dataset`, `benchmark`, `review`
- **Evidence:** `replication`, `reproducibility`, `ablation`, `baseline`, `n-size`
- **Meta:** `contested`, `open-problem`, `sota`, `prediction`, `preprint`, `retracted`, `index`, `comparison`, `audit`

## Page Thresholds
- **Create** when a finding is distinct and defensible (not covered in an existing note)
- **Append** when extending an existing note's scope
- **Split** when a note exceeds ~200 lines
- **Archive** when content is fully superseded → `_archive/`, remove from catalog

## Implementation Notes (operational)

The `implementation/` folder contains project plans, changelogs, and architecture decisions.
These are **operational documents**, not research claims. They do not carry truth-status,
evidence-strength, or red-team blocks. They are tracked here for project context but sit
outside the research vault proper.
