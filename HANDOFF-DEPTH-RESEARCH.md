# HANDOFF — Depth-First Research on the Traction-Inverter Textbook

Written 2026-07-17 for the next agent. Assumes zero prior context. No fluff.

---

## 1. Your Mission

The knowledge base is **broad and cited but shallow in verification**. Your job is **depth-first**: take the textbook's claims — especially the numbers — and drive each one from *plausible* to *proven* (or *refuted*). You are not adding chapters; you are **deepening, verifying, and correcting** the ones that exist.

The vault already tells you exactly where to dig: **every chapter ends with a Red Team block whose "What would change my mind" line is a concrete depth task.** Work that backlog.

**Prime directive:** always cite. Every quantitative or factual claim carries `[NN]` (→ `srtp_docs/citations.md`), `[T]` (training knowledge, unverified), or `[derived]` (computed in-vault). No bare claims. When you verify a `[T]` or `[derived]` claim against a primary source, upgrade it to `[NN]` and bump the note's `status`/`evidence`.

---

## 2. Current State (what exists)

- **`srtp_docs/`** is an Obsidian vault. Rules: `srtp_docs/SCHEMA.md`. Orientation: `srtp_docs/README.md`, `srtp_docs/catalog.md`.
- **`srtp_docs/power-electronics/traction-inverter/`** — a **29-chapter engineering textbook**, cited `[1]`–`[148]`, every chapter red-teamed. This folder is **engineering only**.
- **`srtp_docs/problem-statement/`** — preface (why-AI, market, workforce). Non-engineering context goes **here**, never in `power-electronics/`.
- **`srtp_docs/citations.md`** — the single bibliography. Add new sources here (next number is **[149]**), then cite.
- **Audit of what's shallow:** `srtp_docs/audits/traction-inverter-kb-audit-2026-07-17.md` — read it first.
- **Chapters most in need of depth** carry the softest numbers: `design-procedure`, `thermal-design`, `gate-driver-design`, `protection-and-safety`, `emi-emc-design`, `reliability-and-lifetime`, `worked-example-400v-150kw`, `bom-price-database`.

The whole textbook shares one honest weakness: **nothing is PLECS-validated.** Design/thermal/loss numbers are closed-form or teardown/vendor figures. That is the P0 target.

---

## 3. The Depth Backlog (prioritized)

Each item: **what → why → where → produce.**

### P0 — Turn `[derived]` into evidence (the point of the whole project)
1. **Build & validate the 2L-B6 SiC + IPMSM + FOC PLECS model.**
   - *Why:* grounds `design-procedure` §1–4, `thermal-design` §7, `worked-example-400v-150kw`, and the reference designs. The handoff (`handoff.md`) makes PLECS the only source of truth.
   - *Where/how:* enable PLECS XML-RPC on `localhost:1080`; use the native PMSM + FOC demo as the load. Validate **efficiency + THD + thermal at 3 bus corners (550 / 750 / 850 V)** and calibrate against the Wolfspeed/TI CRD's published **>98% / 32 kW/L** (`reference-design-wolfspeed-ti-300kw-800v`).
   - *Produce:* replace the `[derived]` operating-point/loss/thermal numbers with PLECS-backed values (new `[NN]` citing the model run); start `data/plecs/model_registry.json`; update each affected chapter's Red Team.

### P1 — Replace `[T]` placeholders with primary data
2. **Real IPMSM datasheet / flux maps (id,iq → λd,λq).**
   - *Why:* `machine-and-load` §3, `design-procedure` §0, `control-how-to` §2 all run on `[T]` Ld/Lq/λPM. Every operating point inherits the error.
   - *Produce:* one real motor's parameters (or a PLECS saturation-LUT machine); update the three notes and their Red Teams.
3. **Exact power-module datasheet deep-read** (CAB450M12XM3 and/or the chosen module).
   - *Why:* `thermal-design` (full Zth Foster/Cauer, not the `[T]` cold-plate placeholders), `gate-driver-design` (Eon/Eoff vs I/T/Rg), `protection-and-safety` (SCWT test conditions, cosmic-ray FIT).
   - *Note:* a copy of the TI TIDUF23A design guide PDF may still be in the scratchpad tool-results; the CAB450 datasheet URL is in `[92]`.
4. **Standards texts — verify the paraphrases.** Currently cited by designation only.
   - *CISPR 25:2021* limit tables → `emi-emc-design` §1 (Class-5 dBµV values came from a calculator `[114]`).
   - *IEC 61800-5-1* creepage/clearance tables → `packaging-and-layout` §4, `gate-driver-design` §4.
   - *AQG 324 Rel 04.1/2025* power-cycling target cycles → `reliability-and-lifetime` §2, `protection-and-safety` §7.
   - *ISO 26262* FTTI derivation → `protection-and-safety` §6 (the "200 ms" is representative, not a requirement).

### P1 — Resolve the flagged model/number uncertainties (named in Red Teams)
5. **Lifetime-model coefficients.** Verify CIPS 2008 Bayerer K/β from the primary paper `[142]`; re-fit for SiC; quantify a safety factor on Miner `LC=1`. → `reliability-and-lifetime` §3, Red Team RT-1/RT-2.
6. **Cosmic-ray SEB.** Get the **device-specific neutron-FIT-vs-Vdc curve** for the chosen MOSFET; replace the generic "70–80%" rule. → `protection-and-safety` §1 Red Team.
7. **Loss-model precision.** Confirm the closed-form conduction/switching split with a double-pulse dataset or PLECS. → `design-procedure` §3, `worked-example-400v-150kw`.

### P2 — Complete BOM & breadth
8. **Full board BOM.** Parse the TI TIDUF23A design guide for the complete BOM (snubbers, sense conditioning, protection ICs, connectors); pull **live DigiKey/Nexar** pricing (with as-of dates) → `bom`, `bom-price-database`.
9. **3L reference designs** (TNPC / NPC / ANPC) — currently *noted only* in `reference-design-2l-b6-sic-800v` §Alternatives. Build them out only if multilevel depth is wanted.
10. **Verify secondary numbers:** reflected-wave critical-length for the *actual* harness (`emi-emc-design` §4); pin vendor uplift "×" figures to their test conditions (`reliability-and-lifetime` §6).

---

## 4. How to Work (the loop)

For each depth item, run this loop and **write as you go**:

1. **Pick a chapter's Red Team objection** (or a backlog item above).
2. **Pull the primary source** it names (datasheet table, standard clause, the CIPS08 paper, a PLECS run). Prefer primary/peer-reviewed over vendor/blog; label reliability per SCHEMA §6.
3. **Answer the objection in place** — append to the existing chapter (append-first; don't spawn a parallel note). Replace the soft number, or bound it.
4. **Add the source** to `citations.md` (next: `[149]`), cite it inline.
5. **Re-run the Red Team** — update `status`/`evidence`; a claim verified by 2+ independent credible sources can move `unverified → supported`; a broken one → `contested`/`refuted` (keep it, link the replacement — never silently overwrite).
6. **Validate** (see §6).

**Use subagents** for parallel primary-source gathering (you have that tool). Have each return a **dense cited brief + proposed bibliography entries + its own red-team** — do **not** let multiple subagents write `citations.md` concurrently (write conflicts); author centrally. This is how the current textbook was built; it works.

**Keep it dense and clean.** Tables over prose. Upgrade in place. Split a note only when it exceeds ~200 lines. Don't bloat.

---

## 5. Environment

- **Repo:** `D:\Engineering Projects\AI\SRTP_PowerElectronicsAI` — git, branch `main`, user Ferrell. Commit only when asked; branch off `main` if you do.
- **OS:** Windows 10. Shells: PowerShell (primary) + Git Bash. Python 3.12.
- **PLECS:** `C:\Users\ferre\OneDrive\Documents\Plexim\PLECS 4.8 (64 bit)` — **PLECS Standalone 4.8**. Enable XML-RPC in Preferences (port 1080, off by default). Python: `xmlrpc.client.ServerProxy("http://localhost:1080", allow_none=True)`. **Confirm the license permits scripted batch — potential blocker.**
- **MATLAB** installed but **deliberately unused** (PLECS-only constraint).
- **Obsidian CLI** available (needs the app running): `obsidian search`, `obsidian read`, `obsidian backlinks`. Use file tools for bulk edits.
- **RAG corpus:** this vault's markdown + a local PDF collection — **confirm the PDF folder path with the human.**

---

## 6. Conventions & Validation (don't skip)

- **Follow `srtp_docs/SCHEMA.md` exactly.** Folder = field. Every file has frontmatter. Every claim note has a Red Team. New tags go into SCHEMA §8 *before* use.
- **After structural edits, validate** — from `srtp_docs/`:
  ```bash
  find . -name '*.md' | sed -E 's#.*/##; s/\.md$//' | sort -u > /tmp/exist.txt
  find . -name '*.md' -not -path './.obsidian/*' -not -path './project/changelog/*' | while read f; do
    grep -ohE '\[\[[^]]+\]\]' "$f" | sed -E 's/\[\[//; s/\]\]//; s/\|.*//; s/#.*//; s/\.md$//' | while read l; do
      grep -qx "$(echo $l|sed -E 's#.*/##')" /tmp/exist.txt || echo "DANGLING: $f -> $l"; done; done
  ```
  Confirm every `[[link]]` resolves and every file has its required frontmatter keys.

## 7. Gotchas
- A linter **re-stamps frontmatter** after writes (benign — re-read before an Edit if it complains "modified since read").
- Git warns **LF→CRLF** (benign).
- **Historical `project/changelog/` and `audits/` files intentionally reference the OLD structure and deleted notes — do NOT "fix" them.**
- The Bash sandbox classifier is occasionally unavailable; retry or use read-only tools meanwhile.
- **Never read a subagent's output JSONL via the shell** — it overflows context; you get a completion notification automatically.
- `.obsidian/workspace.json` references stale paths — editor state, ignore.

## 8. Definition of Done (per depth item)
A depth item is done when: the target claim is **backed by a primary citation** (or explicitly refuted/bounded), the soft number is **replaced or bounded with its source and conditions**, the note's `status`/`evidence` reflect the new strength, the **Red Team is updated** to the residual (not the old) doubt, and **links + frontmatter validate**.

## 9. Read These First (in order)
1. `srtp_docs/audits/traction-inverter-kb-audit-2026-07-17.md` — what's shallow and why.
2. `srtp_docs/power-electronics/traction-inverter/traction-inverter-index.md` — the textbook map + reading order.
3. `srtp_docs/SCHEMA.md` — the rules.
4. `handoff.md` (this repo root) — the *original* mission handoff (build the PLECS-backed MAS); it explains why PLECS validation (your P0) is the linchpin.
5. Then open the chapters in §3 and start on their Red Teams.
