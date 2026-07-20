---
title: "Descriptive renames + frontmatter-as-index navigation"
type: changelog
field: project
created: 2026-07-19
updated: 2026-07-19
tags: [changelog, index]
---

# 2026-07-19 — Naming & Navigation

Renamed notes to descriptive, type-clustered basenames; converted lingering plain-text cross-references to wikilinks; then settled the navigation model: **frontmatter is the index, the filename carries the specifics.** Filename prefixes became *optional sugar*, not a taxonomy to keep in sync.

## What changed

**1. Descriptive renames (26 files, backlinks auto-updated via `obsidian rename`).**

| Cluster | Rename |
|---------|--------|
| agent harnesses | `autogen`, `claude-code`, `codex-cli`, `crewai`, `langgraph`, `opencode`, `hermes-agent`, `research-agents` → `harness-*`; `comparative-analysis`→`harness-comparison`; `architecture-patterns`→`harness-architecture-patterns` |
| plans | `ai-agent-mas-plan`, `architecture`, `depth-research`, `design-loop`, `memory`, `tech-stack`, `knowledge-rag`, `plecs-harness`, `guardrails-and-evidence`, `evaluation-and-benchmark` → `plan-*` |
| maps / notes | `traction-inverter-index`→`index-traction-inverter`; `reference-designs-index`→`index-reference-designs`; `components`→`circuit-components`; `bom`→`bom-2l-b6-sic`; `emi-emc-design`→`design-emi-emc`; `gate-driver-design`→`design-gate-driver` |

Link targets updated vault-wide — including `sources/` and `log/` — are **wikilink retargets only**, no content change (source immutability holds).

**2. Plain-text → wikilinks (~27).** Citation-style section refs made navigable: `circuit-topologies §1` → `[[circuit-topologies]] §1`; stale shorthands fixed (`design-proc §3`→`[[procedure-design]]`, `SCHEMA.md`→`[[SCHEMA]]`, `reliability-and-lifetime.md`→`[[reliability-and-lifetime]]`); [[plan-depth-research]] table column linked; one stale `sources:` path list repointed.

**3. Frontmatter-as-index navigation** ([[SCHEMA]]). CLI test showed `obsidian search "#tag"` / `base:query` return no file list — **ripgrep on frontmatter** does. So the model is a two-step:

```mermaid
flowchart LR
    Q["need a note"] --> F["filter: rg on field/type/status/tags"]
    F --> P["pick: descriptive filename"] --> O["open"]
```

- New **Navigating this vault (CLI)** section: axis table (broad `field` · kind `type` · maturity `status` · topic `tags` · specific *filename*), rg recipes, controlled vocab, hubs.
- **Naming** relaxed: filenames describe specifics; prefixes are optional sugar, never a second taxonomy.
- **Lifecycle** gains the index-maintenance rule: on create/rename/delete, set `field`/`type`/`status`/`tags` + link from a `map` hub in the same pass — `.base`, `obsidian tags`, and `rg` all read that one frontmatter, so nothing drifts.
- [[README]] Conventions gains a matching bullet.

**4. Tag hygiene.** Registered 5 in-use-but-unlisted tags in the taxonomy (`ai`, `machine-learning`, `cost`, `gaps`, `implementation`); `sources/` untouched. Audit found device/concern/topology filter-tags already complete, so no re-tagging.

## Verification

- **rg recipes** return correct sets (`field: power-electronics`→48, `type: plan`→10, `tags…three-level`→5); two-step lands the 3L units.
- **Tag orphans:** 0 — every used tag is in the taxonomy.
- **Link integrity:** 0 real broken wikilinks (only the two backtick *examples* in [[SCHEMA]] and a changelog).

---

← [[changelog-index]] | [[README]] | [[SCHEMA]]
