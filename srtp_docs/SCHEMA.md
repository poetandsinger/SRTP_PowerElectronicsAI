---
title: Schema
type: schema
field: root
created: 2026-07-06
updated: 2026-07-17
tags: [schema, index]
---

# SRTP Research Vault — Schema

> The rules every file in this vault obeys. Folder names are plain English, every
> file carries metadata, and every research claim carries truth-status, evidence-strength,
> and a red-team block.
> Vault root: `D:\Engineering Projects\AI\SRTP_PowerElectronicsAI\srtp_docs`

---

## 1. Folder = Field

Folder names are self-explanatory. The folder a note lives in **is** its `field` value — no lookup table, no abbreviations.

| Folder | `field` value | Holds |
|--------|---------------|-------|
| `power-electronics/` | `power-electronics` | Traction inverter design: topologies, semiconductors (SiC/GaN/Si), modulation, thermal, control, MATLAB modeling |
| `ai-agents/` | `ai-agents` | AI agent architectures: Claude Code, Codex CLI, OpenCode, Hermes, LangGraph, CrewAI, AutoGen, research agents, MAS patterns |
| `sources/<field>/` | matches subfolder | Immutable raw captures of one paper/source each |
| `maps/` | matches the map's subject | Navigation hubs (field and topic indexes) |
| `project/` | `project` | Operational docs: implementation plans, changelog |
| `audits/` | `project` | Lint reports and self-audits of the vault |
| root (`/`) | `root` | Singletons: `README`, `SCHEMA`, `catalog`, `citations` |

Field content notes (`claim`, `topic`, `source`) live **only** under `power-electronics/`, `ai-agents/`, or `sources/`.

---

## 2. Every File Has Metadata

No file ships without a YAML frontmatter block. Four **identity** keys are mandatory on every `.md` file, plus a **date** — `created` + `updated` for authored notes, or `captured` for source captures (one date, not three):

```yaml
---
title: Human-readable title
type: <see §3>
field: power-electronics | ai-agents | project | root
created: YYYY-MM-DD        # authored notes
updated: YYYY-MM-DD        # authored notes
tags: [from the taxonomy in §8]
---
```

Two note kinds extend this block:

**Claim / topic notes** add the research fields:
```yaml
status: supported | contested | refuted | unverified
evidence: replicated | single-study | theoretical | disputed
sources: [sources/ai-agents/foo, doi:10.1234/xyz, arxiv:2401.01234]
contradicts: [slug-of-conflicting-note]   # omit if none
review_by: YYYY-MM-DD
```

**Source notes** (`type: source`) keep the four identity keys (`title`, `type`, `field`, `tags`) but date with a single `captured` instead of `created`/`updated`, and add capture provenance:
```yaml
authors: [...]
year: YYYY
venue: "journal / conference / preprint server"
doi: 10.1234/xyz          # or arxiv: / pmid:
captured: YYYY-MM-DD       # the source's one date
reliability: high | medium | low | unknown
peer_reviewed: true | false
motivated: true            # omit if not
reliability_note: "..."
```

---

## 3. Note Types

| `type` | Lives in | Purpose | Red-team? |
|--------|----------|---------|-----------|
| `source` | `sources/<field>/` | Immutable raw capture of one paper/source. Never edited. | no |
| `claim` | `<field>/` | One defensible finding + evidence + red-team. Carries status + evidence. | **required** |
| `topic` | `<field>/` | Synthesis across claims/papers. State of knowledge on a subject. | required if it advances a position |
| `map` | `maps/`, `<field>/` | Navigation hub linking related notes. Pure wayfinding. | no |
| `plan` | `project/plans/` | Implementation plan or architecture decision. Operational. | no |
| `changelog` | `project/changelog/` | Dated record of what changed. Operational. | no |
| `audit` | `audits/` | Lint report or self-audit of the vault. Operational. | no |
| `catalog` / `schema` / `citations` | root | The three root singletons besides README. | no |

**Claim vs topic:** a claim defends *one* checkable finding ("SiC switching losses ~40% below Si IGBT at 100 kHz, 650 V"). A topic synthesizes many ("state of wide-bandgap adoption in traction inverters"). One sharp result → claim. A landscape → topic linking its claims.

**Operational vs research:** `plan`, `changelog`, and `audit` notes are project docs. They carry the base metadata block but **no** truth-status, evidence-strength, or red-team — they record decisions, not defensible findings.

---

## 4. Truth-Status (claim/topic only)

- `supported` — corroborated by 2+ independent credible sources; red-team failed to break it.
- `contested` — credible sources disagree, OR the red-team raised a serious unresolved objection.
- `refuted` — evidence shows it false. Keep the note as a record; link what replaced it.
- `unverified` — single source, unknown-reliability source, or not yet cross-checked.

**New claims default to `unverified`.** Never default to `supported` — earn it.

## 5. Evidence-Strength (claim/topic only)

- `replicated` — independent groups reproduced it; meta-analysis or multiple confirmations.
- `single-study` — one (or a few, not independently reproduced) papers.
- `theoretical` — derived/modeled/simulated, not yet empirically tested.
- `disputed` — replication attempts conflict or have failed.

## 6. Source Reliability

- **high** — primary/original: peer-reviewed papers in credible venues, standards bodies, direct experimental reports.
- **medium** — solid secondary: reputable preprints, review articles, textbooks, well-run informal reproductions.
- **low** — weak/motivated: press releases, vendor whitepapers, marketing, single blog posts, un-refereed theses.
- **unknown** — provenance unassessable.

`peer_reviewed: false` (preprint) does not automatically mean low — a preprint from a strong group is often `medium` — but it caps a single-source claim at `unverified` until peer-reviewed or independently reproduced.

**`motivated` is orthogonal to reliability** — a vendor's own well-run benchmark can be `high` *and* `motivated: true`. Motivation does NOT gate status. **Reliability gates status:** a `low`/`unknown` source can't push a claim past `unverified` on its own.

---

## 7. Red-Team Block (mandatory on claim notes)

```markdown
## Red Team
**Steelman against:** [Strongest good-faith case the finding is wrong or overstated.]
**How it could be false:** [Concrete mechanism — small n, p-hacking, no controls, cherry-picked regime, unreproduced, motivated funding, sim≠reality, measurement artifact.]
**What would change my mind:** [Specific result that would flip status or evidence-strength.]
**Residual doubt:** [One line — what still nags after reading.]
```

No red-team, no claim.

---

## 8. Tag Taxonomy

Every tag on a note must exist here. Add to this list first, then use.

### Fields
- `power-electronics` — power electronics
- `ai-agents` — AI agent architecture

### Power Electronics
- **Topologies:** `topology`, `inverter`, `two-level`, `three-level`, `multilevel`, `npc`, `t-type`, `anpc`
- **Components:** `mosfet`, `igbt`, `gan`, `sic`, `diode`, `capacitor`, `dc-link`, `gate-driver`
- **Modulation:** `pwm`, `svpwm`, `dpwm`, `she-pwm`, `hysteresis`, `mpc`
- **Thermal:** `thermal`, `heatsink`, `junction-temperature`, `cooling`, `thermal-resistance`
- **Control:** `foc`, `dtc`, `sliding-mode`, `observer`, `sensorless`, `pi-control`
- **Performance:** `efficiency`, `thd`, `ripple`, `emi`, `power-factor`, `dvdt`, `switching-loss`
- **Standards:** `ieee`, `iec`, `iso`, `mil-std`, `aec-q`
- **Domain:** `traction-inverter`, `market-research`
- **Method:** `tuning`

### AI / Agent Architecture
- **Frameworks:** `claude-code`, `codex-cli`, `opencode`, `hermes-agent`, `langgraph`, `crewai`, `autogen`
- **Concepts:** `multi-agent`, `tool-calling`, `delegation`, `orchestration`, `subagent`
- **Architecture:** `architecture`, `patterns`, `comparison`, `integration`, `gui-vs-cli`
- **Engineering AI:** `plecs`, `simulation`, `code-generation`, `design-automation`, `engineering-ai`

### Cross-cutting
- **Method:** `experiment`, `simulation`, `theory`, `dataset`, `benchmark`, `review`
- **Evidence:** `replication`, `reproducibility`, `ablation`, `baseline`, `n-size`
- **Meta:** `contested`, `open-problem`, `sota`, `prediction`, `preprint`, `retracted`, `index`, `audit`, `synthesis`
- **Operational:** `plan`, `changelog`

---

## 9. Naming & Linking

- **Filenames are kebab-case.** No spaces, no capitals: `traction-inverter-index.md`, not `Traction Inverter Index.md`.
- **Wikilinks are path-based** from the vault root: `[[power-electronics/traction-inverter/components]]`, not the bare basename. Display text and anchors are fine: `[[path|Label]]`, `[[path#Section]]`.
- **Sources are referenced by path** in the `sources:` frontmatter list, matching the file under `sources/<field>/`.

---

## 10. Lifecycle

- **Append-first.** Before creating a note, search the vault. If the idea extends an existing note, append and bump `updated` (re-run the red-team if status could shift). Only spawn a new note when the finding is genuinely distinct.
- **Create** when a finding is distinct and defensible.
- **Split** when a note exceeds ~200 lines.
- **Contradictions surface, never overwrite** — set `contradicts:` and let both notes stand.
- **Delete** superseded operational docs (git preserves history). **Never delete** a research note that was ever `supported` or `contested` — mark it `refuted` and link its replacement.

---

← [[README]] | [[catalog]] | [[maps/power-electronics]] | [[maps/ai-agents]]
