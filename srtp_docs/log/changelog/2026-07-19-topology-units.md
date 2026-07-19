---
title: "Topology-unit naming scheme + 3L design scaffolds"
type: changelog
field: project
created: 2026-07-19
updated: 2026-07-19
tags: [changelog, design, traction-inverter]
---

# 2026-07-19 — Topology units

Established a **per-topology naming scheme** for the power-electronics design cluster so the multi-topology depth program ([[plan-depth-research]]) has one note per topology, consistently named.

## What changed

**Scheme** (now in [[SCHEMA]] §Naming & Linking):
- `design-<topology>-<voltage>-<device>` — our own PLECS-validated **topology units**.
- `reference-design-<source>-<class>` — **external references** (vendor CRDs, teardowns) we calibrate against.
- Titles must be specific (e.g. `3L-ANPC · 18-switch · 800 V SiC Traction Inverter`).

**Directory:**
- Renamed `reference-design-2l-b6-sic-800v` → **`design-2l-b6-800v-sic`** (it is our synthetic anchor design, not an external reference). 17 wikilinks updated across the vault; the `plecs-harness` registry example and the plan repointed.
- Created three scaffolds (structure + target spec + planned PLECS validation + Red Team, numbers `[TBD-PLECS]`): **`design-3l-tnpc-800v-sic`**, **`design-3l-anpc-800v-sic`**, **`design-3l-npc-800v-sic`** — filled by Tracks 2–4.
- External references (Wolfspeed/TI, Tesla Model 3, Nissan Leaf) kept their `reference-design-*` names.

**Indexes:** [[index-reference-designs]] split into *topology units* vs *external references*; the four units added to [[index-traction-inverter]].

## Why

The multi-topology plan (Option C, serial) builds a validated model for each of 2L-B6 → 3L-TNPC → 3L-ANPC → 3L-NPC. Each needs a stable, consistently named home so its numbers land in one place and the set groups in the file tree and bases. Keeping `design-*` (our evidence) distinct from `reference-design-*` (external anchors) prevents conflating what we produced with what we cite.

---

← [[changelog-index]] | [[plan-depth-research]] | [[README]]
