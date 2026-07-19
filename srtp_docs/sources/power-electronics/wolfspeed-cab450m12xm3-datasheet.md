---
title: "CAB450M12XM3 — 1200 V, 2.6 mΩ Silicon Carbide Half-Bridge Module (Data Sheet)"
type: source
field: power-electronics
tags: [power-electronics, sic, mosfet, traction-inverter, thermal, switching-loss, two-level, reference-design]
authors: [Wolfspeed, Inc.]
year: 2024
venue: "Wolfspeed data sheet, Rev. 3 (June 2024), 12 pp."
captured: 2026-07-19
reliability: high
peer_reviewed: false
motivated: true
reliability_note: "Primary vendor datasheet; values are typical unless a Max column is shown. Vendor is motivated (sells the part) but datasheet parameters are the primary engineering spec. Switching energies fully specified only at 600 V; 800 V and E_sw-vs-current points are read from graphs (±10–15%)."
---

## What This Is

The primary datasheet [166] for the **Wolfspeed CAB450M12XM3** SiC MOSFET half-bridge module — the device used ×3 in the Wolfspeed/TI 300 kW 800 V CRD ([[reference-design-wolfspeed-ti-300kw-800v]], [160]) and the target device for the Track-1 **2L-B6 SiC** PLECS model ([[design-2l-b6-800v-sic]], [[plan-depth-research]]). Captured to feed the PLECS loss/thermal description (`data/plecs/LOSS_LAYER_BUILD.md`). All params are **per position** (per switch); the "diode" is the intrinsic SiC body diode of the same MOSFET die (no separate antiparallel diode).

URL: https://assets.wolfspeed.com/uploads/2024/01/Wolfspeed_CAB450M12XM3_data_sheet.pdf · cached PDF in session scratchpad.

## Conduction (tabulated, p.2)

| Param | @25 °C | @175 °C | Conditions |
|-------|--------|---------|------------|
| R_DS(on) typ | **2.6 mΩ** (3.4 mΩ max) | **4.7 mΩ** | V_GS=15 V, I_D=450 A |
| Body-diode V_SD | 4.7 V | 4.2 V | V_GS=−4 V, I_SD=450 A |

R_DS(on) vs T_j ≈ 1.81× over 25→175 °C (Fig 3, ~flat to 100 °C then rises). Package resistance R_M1=0.72 mΩ (HS) / R_M2=0.63 mΩ (LS) at 125 °C adds to terminal-to-terminal loss. In an inverter, freewheeling uses the **3rd-quadrant channel** (~R_DS(on) slope, Fig 5), not the 4.7 V body-diode drop.

## Switching energy (tabulated, p.2 — V_DD=600 V, I_D=450 A, R_g,on=4.0 Ω, R_g,off=0 Ω, L_s=10.2 nH)

| T_VJ | E_on | E_off | E_rr |
|------|------|-------|------|
| 25 °C | 25.4 mJ | 7.51 mJ | 0.2 mJ |
| 125 °C | 24.0 mJ | 8.10 mJ | 0.9 mJ |
| **175 °C** | **24.4 mJ** | **8.35 mJ** | **1.1 mJ** |

- **E_on/E_off are nearly flat vs T_j** (Fig 13) — do not apply a strong temperature multiplier. **E_rr rises strongly with T_j** (Fig 14).
- **Current scaling** (Fig 11, 600 V/25 °C) ≈ linear through origin: E_on ≈ 0.056 mJ/A, E_off ≈ 0.017 mJ/A (anchored on the 450 A point). [graph, ±10–15%]
- **800 V** (Fig 12, 25 °C only, R_g,on=5.0 Ω): at 450 A ≈ E_on ~45 mJ, E_off ~22 mJ [graph]. **No 800 V / 175 °C curve exists** — for an 800 V bus at 175 °C combine 800 V/25 °C current-scaling with the ~flat-T_j behavior (approximation; flag it). R_g,int=2.5 Ω; E_off scales ~linearly with R_g,off.

## Thermal (p.2, Fig 17)

- Steady-state **R_th,JC = 0.094 °C/W** per position (MOSFET; body diode shares the die → reuse).
- **Foster/Cauer R_i–τ_i pairs are NOT in the datasheet** — only the Z_th(j-c) transient curve. The R_i/τ_i live in **Wolfspeed's downloadable PLECS XML** [167] (preferred source; datasheet p.11 links it). Read-off Z_th single-pulse: ~0.001@1e-5 s, 0.005@1e-4, 0.02@1e-3, 0.06@1e-2, 0.09@0.1 s, plateau 0.094. Case-to-sink ≈0.08 °C/W app-note guidance [168].

## Ratings

V_DS 1200 V · I_D 450 A (25 °C) / 438 A (90 °C) · I_DM 900 A · P_D 1670 W · T_VJ −40…**+175 °C** · L_stray **6.7 nH** (module) / 10.2 nH (DPT bus) · V_isol 4 kV · V_GS(th) 2.5 V typ.

## The official PLECS model (now local — supersedes hand-building)

The full Wolfspeed PLECS library was downloaded 2026-07-19 to
`plecs_models/wolfspeed/` (669 models; usage guide PRD-09611 [170]). The target is
`mosfet-with-diode/modules/CAB450M12XM3.xml` (Version 4, 2026-03-19,
`class="MOSFET with Diode"`). It carries the **full E_on/E_off/E_rr 4-D surface incl.
800 V at all T_j** (VoltageAxis `[-10 0 600 800]`, TempAxis `25…200 °C`) — **resolving the
datasheet's missing 800 V/175 °C switching curve** — plus Rg-scaling custom tables
(`Eon(Rg)`/`Eoff(Rg)`/`Err(Rg)`, ref `Rgon=4`/`Rgoff=0`), both conduction paths, and a
4-stage **Cauer** net (R = 0.00879/0.02757/0.04532/0.01311, ΣR ≈ 0.0948 °C/W = R_th,JC).
Model constants: Ron 3.6 mΩ, Vf 3.234 V, Rdio 3.1 mΩ.

## Use in this project

Assign the official model to the PLECS converter (`therm=file:CAB450M12XM3`) per
`data/plecs/LOSS_LAYER_BUILD.md` — **proven 2026-07-19 to load + simulate on the harness**.
The tabulated datasheet numbers above now **bound/sanity-check** the model's output rather
than build it. Calibration anchor for SOP S5: reproduce the CRD's >98 % η / 175 °C.

> **References:** [[citations]] [166][167][168][170][160]
