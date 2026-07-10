---
title: Research Audit Changelog — Traction Inverter
type: topic
field: ee
created: 2026-07-08
updated: 2026-07-08
tags: [ee, audit, review]
status: unverified
evidence: single-study
---

## Audit Method

1. Fetched arXiv abstracts and LaTeX source/PDFs for every cited paper.
2. Dispatched 3 leaf subagents to verify specific claims against their sources.
3. Cross-checked every numbered citation in the traction-inverter notes against `citations.md`.
4. Checked wikilink integrity and nav-footer consistency.

## Final Verification Status

- **Broken wikilinks:** 0
- **Undefined citations in traction-inverter notes:** 0
- **Unused citations removed:** [46] Tyagi & Mayergoyz (2019), [57] Wikipedia Power Inverter
- **Remaining `[T]` markers:** 35 (honest training-knowledge gaps; listed below)
- **Remaining `[N]` markers:** 0

## Fixed Issues

| Issue | Finding | Fix |
|---|---|---|
| **1. Misattribution of 0.67 kWh/100 km figure** | The 0.67 kWh/100 km and 30% SiC chip-area claim was cited as [43] (Sachs et al.) but it actually comes from Sachs & Neuburger [28]. | Changed all three occurrences in `circuit-topologies.md`, `open-problems.md`, and `matlab-modeling.md` from [43] to [28]. |
| **2. GaN viability claim unsupported by [44]** | Cacciato et al. (2022) does not claim GaN is “not viable” for traction; the paper argues GaN is promising when combined with 3L-ANPC. The 200 kHz / SiC comparison / low-power sub-module claim was also unsupported. | Rewrote the GaN section in `components.md` to accurately reflect the paper: it is an analytical loss-modeling study with PSIM validation and preliminary 200 V/3 A experiments. Added explicit [T] marker for the training-knowledge viability opinion. |
| **3. MTPA “noise and convergence risk” over-interpreted** | Zuo et al. (2024) [45] supports online RLS-based MTPA and better dynamic performance than extremum seeking, but does not explicitly state “noise and convergence risk.” | Rewrote the bullet in `open-problems.md` to separate the source-supported claim from the authorial inference. |
| **4. Unused [46] and [57] citations** | Tyagi & Mayergoyz (2019) [46] was unused; Wikipedia Power Inverter [57] was unused. | Removed [46] and [57] from `citations.md`. |
| **5. [43] unused after fixes** | [43] was originally cited only for the misattributed finding. | Added a valid, limited use in `open-problems.md`: [43] is an optimization-based comparative evaluation of single/dual traction-inverter architectures trading chip area against partial-load efficiency. |
| **6. Broken citation [1] in new overview note** | `what-is-a-traction-inverter.md` still used placeholder [1] for a DC-link capacitor claim. | Replaced [1] with [50] (Mohan textbook) and kept the [T] flag because the exact µF range is not verified. |

## Remaining `[T]` / `[N]` Gaps (Honest Unverified Claims)

These are training-knowledge or note claims that could not be verified against live sources because manufacturer portals and paid market reports were blocked or inaccessible:

- Specific IGBT/SiC module part numbers and current/voltage ratings (Infineon, Wolfspeed, STMicro, etc.).
- OEM-specific adoption timelines (e.g., “Tesla uses SiC in Model 3/Y,” “Hyundai E-GMP uses SiC”).
- Exact sensor bandwidths, gate-driver propagation delays, and DC-link capacitor part numbers.
- GaN traction viability, cost ratios, and 2027 SiC market projections.
- SiC gate-oxide NBTI threshold drift and bearing-current effects at automotive scale.
- The exact MathWorks Simscape block-level workflow (URL blocked by bot detection).

## Verified Sources

| Citation | Source | Status |
|---|---|---|
| [28] | Sachs & Neuburger (2025), arXiv:2508.14224v1 | ✅ Verified; abstract and conclusion quote the 0.67 kWh/100 km and 30% SiC chip-area findings. |
| [43] | Sachs et al. (2025), arXiv:2507.03573v1 | ✅ Verified; supports optimization-based comparative evaluation of single/dual traction inverters with chip-area vs. efficiency trade-off. |
| [44] | Cacciato et al. (2022), arXiv:2212.05246v1 | ✅ Verified; supports loss-modeling approach for GaN HEMT 3L-ANPC inverters. Does NOT support broad GaN viability claim. |
| [45] | Zuo et al. (2024), arXiv:2404.18176v1 | ✅ Verified; supports online RLS-based MTPA with better dynamic performance than extremum seeking. |
| [57] | Wikipedia Power Inverter | ✅ Verified; supports basic inverter/H-bridge/three-phase definitions, but was unused so removed. |

## Blocked / Could Not Verify

- MathWorks Simscape Electrical documentation: blocked by bot detection; URL assumed correct but content not fetched live.
- Infineon HybridPACK Drive, Wolfspeed XM3 pages: returned only 693–913 chars (likely blocked or JS-required).
- Yole / Precedence market reports: paid reports; not fetched live.

## Actions Taken on Files

- `docs/SRTP/research/traction-inverter/circuit-topologies.md`
- `docs/SRTP/research/traction-inverter/open-problems.md`
- `docs/SRTP/research/traction-inverter/matlab-modeling.md`
- `docs/SRTP/research/traction-inverter/components.md`
- `docs/SRTP/research/traction-inverter/what-is-a-traction-inverter.md`
- `docs/SRTP/citations.md`
- `docs/SRTP/research/audit-changelog-traction-inverter.md` (this file)

## Next Steps

1. Replace remaining `[T]` entries with live manufacturer datasheets or teardown reports as they become accessible.
2. Validate MATLAB/Simulink modeling recipes on a machine with MATLAB + Simscape Electrical installed.
3. Verify the textbook references ([47]–[50]) against current editions via a library or publisher source.
4. Add a dedicated “Single vs. Dual Traction Inverter” note if [43] becomes a central source.
