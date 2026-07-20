---
title: "3L-NPC · 12-switch + 6-diode · 800 V SiC Traction Inverter — Design & PLECS Validation"
type: topic
field: power-electronics
created: 2026-07-19
updated: 2026-07-19
status: unverified
evidence: theoretical
sources: [sources/power-electronics/sachs-neuburger-2025-3l-tnpc]
tags: [power-electronics, traction-inverter, design, three-level, npc, sic, efficiency, thd]
review_by: 2026-10-17
---

## What This Note Is

**Track 4 topology unit** (`design-<topology>-<voltage>-<device>`): an 800 V-class **3-level diode-clamped NPC** traction inverter, sized to the same 150 kW anchor as [[design-2l-b6-800v-sic]]. **Planned, not yet built** — populated when Track 4 of [[plan-depth-research]] runs. NPC is the classic three-level baseline against which TNPC and ANPC are the evolutions. Topology catalogue: [[circuit-topologies]] §2.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training; **[derived]** → in [[procedure-design]]; **[TBD-PLECS]** → produced by the Track-4 model.

## Why This Topology (industry relevance)

**Industrial/rail baseline, not automotive-production** (Siemens/Alstom traction, ABB/Siemens VFDs). Included as the diode-clamped reference point: it establishes what the *active* variants (ANPC) and the *T-type* variant (TNPC) improve on. Its main liability — neutral-point balancing — is the shared "Achilles' heel" of all NP topologies.

## Topology Structure

- **12 switches + 6 clamping diodes** (4 switches S1–S4 + 2 clamp diodes Dc1/Dc2 per leg, ×3). Three levels: +Vdc/2, 0 (NP), −Vdc/2.
- **Half switch-voltage:** each device blocks Vdc/2 → on an 800 V bus, **650–900 V devices** become usable (a device-cost advantage over TNPC's full-Vdc outer switches). 27 switching states → 19 space vectors; states P/O/N in [[circuit-topologies]] §2.
- **NP balancing is the design problem:** midpoint current depends on state and load; without active balancing the two DC-link capacitor voltages diverge (uneven switch stress, low-frequency ripple, DC offset). Handled by redundant small-vector dwell redistribution or carrier zero-sequence injection.

## Target Specification (same anchor as 2L-B6)

| Item | Value | Basis |
|------|-------|-------|
| Topology | 3L-NPC (12-switch + 6-diode) | [[circuit-topologies]] §2 |
| Device | 650–900 V SiC (Vdc/2 stress) + clamp diodes | [T] |
| DC-link | 750 V nom (550–850 V), split-link + NP | matches anchor |
| Peak / continuous power | 150 kW / 70 kW | matches anchor |
| Switching frequency | 16 kHz | comparison control |
| Efficiency / THD / Tj / NP-balance | **[TBD-PLECS]** | Track 4 |

## Planned PLECS Validation (Track 4)

1. Build as a `.plecs` **text** variant of the Track-1 template (12-switch + 6-diode clamped leg, split DC-link with NP, NP-balancing modulation). Top-level Outports.
2. Run the 9-corner matrix at 550/750/850 V; explicitly test NP-voltage divergence with and without balancing.
3. **Calibrate against the 2L-B6 baseline + literature:** confirm half switch-voltage, ~½ dv/dt, lower THD at equal fsw, and quantify the balancing burden.
4. Fold results into [[circuit-topologies]] §5 and [[design-tradeoffs]]; register in `model_registry.json`.

## Red Team

**Steelman against:** A scaffold with no validated numbers. NPC is the least automotive-relevant of the four (no BEV production), so a full design note risks documenting a topology no car will ship. Its value is comparative baseline only.

**How it could be false:** the device-cost advantage (Vdc/2 devices) may be offset by 6 clamp diodes + NP-balancing control; uneven inner/outer switch loss (the flaw ANPC fixes) may make NPC thermally worse than the switch count suggests.

**What would change my mind:** a validated Track-4 PLECS model quantifying NP-balance behaviour and the loss asymmetry versus ANPC at the three corners.

**Residual doubt:** Correct as the planned diode-clamped baseline for the topology comparison. All numbers `[TBD-PLECS]` until Track 4.

---

> **References:** [[citations]]

← [[circuit-topologies]] | [[design-2l-b6-800v-sic]] | [[plan-depth-research]] →
