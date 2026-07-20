# Wolfspeed PLECS device models

The complete Wolfspeed SiC PLECS thermal/loss library (669 `.xml` models), organized
space-free for CLI / PLECS `file:` search paths. Source: Wolfspeed
[LTspice & PLECS models portal](https://www.wolfspeed.com/tools-and-support/power/ltspice-and-plecs-models/)
([167]); usage: `PLECS_Model_User_Guide_Rev2.pdf` (Wolfspeed PRD-09611, Rev 2, Jan 2026).
Outside the Obsidian vault by design (executable artifacts carry no frontmatter).

## Layout

| Folder | Count | What |
|--------|------:|------|
| `diodes/` | 109 | standalone SiC Schottky diodes |
| `mosfet-with-diode/mosfets/` | 119 | **current format** — discrete MOSFETs, body diode integrated in one model |
| `mosfet-with-diode/modules/` | 55 | **current format** — half-bridge / module packages (CAB/CBB/CCB/WAB/ECB/EDB…) |
| `legacy-mosfets/mosfets/` | 268 | **legacy format** — discrete MOSFETs, split `PART.xml` + `PART_bodydiode.xml` |
| `legacy-mosfets/modules/` | 118 | **legacy format** — modules, split MOSFET + `_bodydiode` pairs |

**Two model formats** (PRD-09611 §2): the **MOSFET with Diode** models are a single XML
used with PLECS's integrated MOSFET-with-diode block (preferred, simplest). The **Legacy**
models split the MOSFET and its body diode into two XMLs (`PART.xml` + `PART_bodydiode.xml`),
used with separate MOSFET + diode blocks. Same loss/thermal data, different block wiring.
4-D loss tables (Eon/Eoff/Err vs Id, Vds, Tj, Rg) **require PLECS 4.8+** (we run 4.8).

## Install (make `file:PART` resolve)

1. **Global (GUI):** File → PLECS Preferences → add this folder (and subfolders) to the
   **thermal-description search path**. Then any block's Thermal description = `file:PART`.
2. **Self-contained (what our harness uses):** copy the needed XML into a
   `<modelbasename>_plecs/` folder next to the `.plecs` — PLECS auto-searches it. Travels
   with the model (reproducible); no machine-global preference. Verified 2026-07-19.

Block Thermal-tab params (PRD-09611 §2.1.1): Thermal description (`file:PART`), external
turn-on/off gate resistance (`Rgon`/`Rgoff` — model Variables), thermal interface resistance
K/W (case→heatsink), initial temperature °C.

## Traction-relevant subset — 800 V-bus SiC half-bridge modules (1200 V, XM3)

The design cluster's target class ([[design-2l-b6-800v-sic]], [[reference-design-wolfspeed-ti-300kw-800v]]).
All `mosfet-with-diode/modules/`, Version 4 (2026-03-19), 1200 V, integrated body diode:

| Part | Ron (mΩ) | Vf (V) | Rdio (mΩ) | Role |
|------|---------:|-------:|----------:|------|
| **CAB450M12XM3** | **3.6** | 3.234 | 3.1 | **Track-1 target** — the module ×3 in the Wolfspeed/TI 300 kW CRD [160][166] |
| CAB425M12XM3 | 4.2 | 3.522 | 3.9 | sibling (slightly lower current) |
| CAB400M12XM3 | 5.3 | 3.634 | 5.2 | sibling |

Each model carries the full **Eon/Eoff/Err 4-D surface (incl. 800 V at all Tj)**, both
conduction paths (channel + body diode), and a 4-stage **Cauer** thermal net summing to
≈0.095 °C/W (= datasheet R_th,JC). Other 1200 V modules present: CAB011/016M12FM3,
CAB525F12XM3, CAB530M12BM3, CBB/CCB families, WAB300/400M12BM3. Higher-voltage traction:
CAB320M17XM3 (1700 V), CAB600M33LM3 (3300 V).

## Use in this project

Track-1 loss layer (`../../data/plecs/LOSS_LAYER_BUILD.md`): copy
`mosfet-with-diode/modules/CAB450M12XM3.xml` into the harness `_plecs/` folder, set the
converter's `therm` param to `file:CAB450M12XM3`, `Rgon=4`/`Rgoff=0` (datasheet ref),
`Rth`(case→sink), `T_init=65`. This **replaces the hand-built-XML fallback** — the official
model has the full V-I-T surface the datasheet alone lacked.
