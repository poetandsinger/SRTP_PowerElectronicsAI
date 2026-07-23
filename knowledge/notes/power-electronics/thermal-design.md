---
title: "Thermal Design"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, thermal, thermal-resistance, junction-temperature, cooling, heatsink, sic, design]
review_by: 2026-10-17
---

## What This Is

The thermal chapter: how heat leaves the die, how hot the junction gets, and how that caps continuous torque. Deep-dive behind [[circuit-components]] §6 and [[procedure-design]] §3. Reference device: Wolfspeed CAB450M12XM3 (1200 V/450 A SiC, Tj,max 175 °C) [92].

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; `[derived]` → computed here.

## 1. The Thermal Resistance Chain

Steady state is series-additive: **`Tj = Tcoolant + P·(Rth,jc + Rth,cs + Rth,s-coolant)`** [25][101]. Real per-switch junction-to-case values:

| Module | Device | Rth(j-c) per switch | Note |
|--------|--------|--------------------:|------|
| Wolfspeed CAB450M12XM3 | 1200 V/450 A SiC | **0.094 °C/W** (FET, typ) | Tj,max 175 °C [92] |
| Infineon HybridPACK Drive (Si IGBT ref) | 750 V IGBT | 0.12–0.14 K/W (j-to-**fluid**) | 10 L/min, 50/50 WEG, 75 °C [99] |
| Infineon HybridPACK Drive G2 (CoolSiC) | 1200 V SiC | >15% lower Rth than G1 (.XT die attach) | direct/top-cooled variants [99] |
| onsemi EliteSiC (NVXR) | 900/1200 V SiC | low via sintered-Ag die attach | pin-fin baseplate [99] |

`Rth,jc` is fixed by die area + die-attach + DBC/AMB substrate. Modern **direct-/pin-fin-cooled** modules eliminate the baseplate+TIM stage and quote **`Rth(j-fluid)` ≈ 0.10–0.15 K/W per SiC switch** instead [99][101]. **The design lever is the TIM + cold-plate stages, not `Rth,jc`** (§7).

## 2. Transient Thermal Impedance `Zth(t)` — sets peak/overload ratings

`Zth(t)` rises from ~0 (t→0) to steady `Rth` as thermal capacitances charge [101]. For short overloads (launch/boost, ~30–60 s), the die heat capacity absorbs the energy → **effective Rth ≪ steady Rth**, so a device that would cook continuously survives a bounded pulse. **Peak-power ratings come from `Zth(pulse)`, not `Rth(steady)`** [105].

- **Foster network:** curve-fit parallel R–C pairs (Rᵢ/τᵢ on datasheets) — convenient for convolving loss profiles, but nodes are **non-physical**; do not truncate or append a heatsink to it [101].
- **Cauer network:** physical ladder (die → attach → substrate → baseplate → TIM → cold-plate) — cascade this with the cold-plate model [101].
- Measured per JEDEC **JESD51-14** (transient dual-interface) [101].

## 3. Junction-Temperature Estimation

| Method | Speed | Accuracy | Limit |
|--------|-------|----------|-------|
| **NTC** (on DBC near dies) | slow (100s ms–s) | reads *substrate*, not Tj | cheap, robust, EMI-immune; needs chip→NTC model; misses transients/hot-die [106] |
| **TSEP** (Vds(on), Vth, turn-on delay) | fast (µs–cycle) | good with calibration | needs sense circuitry, EMI-sensitive, gives **lumped average** across paralleled dies (misses hottest) [106] |

Production split: **NTC for slow protection/derating; TSEP/model-based for fast condition monitoring** [106]. NTC lag is why the procedure-design derating loop uses a thermal model on top of the NTC ([[procedure-design]] §6).

## 4. Cooling Technologies (performance)

| Technology | Performance | Conditions | Status |
|------------|-------------|-----------|--------|
| Pin-fin baseplate, single-phase WEG | ~50–100 W/cm² class (baseline) | 50/50 water-glycol, ~8–12 L/min, 65–75 °C inlet | **production default** [99][101] |
| Jet impingement + microfins | **−45% Rth, +79% power density** vs pin-fin | WEG | emerging [102] |
| Double-sided cooling (DSC) | **Rth −30–39%**, ~2× cooling | coolers both faces | premium (100 kW/L target) [103] |
| Direct-cooled (TIM eliminated) | further **>30%** Rth | coolant hits fin directly | growing [103] |
| Single-phase oil immersion | ~50 W/cm² | shared e-drive oil | some OEMs [T] |
| Two-phase immersion / boiling | ~100 W/cm² (up to ~400 W/cm² lab) | dielectric, Tsat ~40 °C | pre-production [T] |

Production 100–300 kW SiC inverters overwhelmingly use **single-phase pin-fin WEG (65 °C, ~10 L/min)**; DSC/direct/jet are the density levers [99][103].

## 5. Thermal Interface Materials

| TIM | k (W/m·K) | Where |
|-----|----------:|-------|
| Thermal grease/paste (filled) | 2.9–7.5 (Ag-filled ~8.9) | baseplate↔cold-plate; use *flowable* paste for contact [104] |
| Phase-change (PCM) | 3–7 | resists pump-out under cycling vs grease [104] |
| Graphite pad | 5–15 in-plane | dry/reworkable interface [104] |
| **Sintered silver** | **80–280** | **die-attach** (chip→DBC) & DSC interposers — bonded, inside Rth,jc [104][103] |

The ~2-order gap matters: sintered-Ag die-attach is *inside* `Rth,jc`; the bulk TIM (single-digit W/m·K) dominates `Rth,cs` and is the weakest link — motivating TIM-less direct cooling [103].

## 6. Derating — How Tj Caps Torque

Continuous current is bounded by self-heating: **`ID(max) = √[(Tj,max − Tc)/(Rth,jc · RDS(on)(Tj))]`** [105]. `RDS(on)` rises with Tj (positive tempco → thermally self-limiting, eases paralleling). As coolant/case temp rises, `(Tj,max − Tc)` shrinks so allowable current falls ~`√(Tj,max − Tc)`. Control: full torque below a Tj threshold, **linear current roll-back** above it, hard clamp near Tj,max [105], [[control-schemes]] §6.2. Overload torque is time-limited by the `Zth(pulse)` energy budget (§2).

## 7. Worked Rth-Chain Example (CAB450M12XM3, per switch)

Mid-load `P_loss ≈ 500 W/switch`, coolant `Tc = 65 °C`, pin-fin WEG:

- `Rth,jc = 0.094 K/W` [92]
- `Rth,cs` (TIM grease ~0.1 mm, k≈5) ≈ **0.03 K/W** `[T]` placeholder [104]
- `Rth,s-coolant` (pin-fin cold plate) ≈ **0.05 K/W** `[T]` placeholder

`ΣRth = 0.174 K/W` → `ΔT = 500·0.174 = 87 K` → **`Tj = 65 + 87 = 152 °C`** → 23 K under 175 °C [derived].

**Sensitivity:** DSC/direct cooling halving the (TIM+cold-plate) stages (0.08→0.04) gives `ΣRth=0.134`, `Tj=132 °C` — the recovered ~20 K converts to **~15–25% more continuous current** [103]. This is why the TIM + cold-plate stages, not `Rth,jc`, are where you design.

> [!success] **PLECS-validated + CRD-calibrated (Track-1, 2026-07-23)** `[sim]`. The soft `Rth,cs` placeholder
> above is now pinned by the measured anchor: on the validated 2L-B6 bench ([[design-2l-b6-800v-sic]]), at the
> 300 kW CRD point the per-switch loss is **470 W** (208 conduction + 262 switching) and the reported steady-state
> **Tj = 175 °C** is analytic (`Tj = Ta + P_module·R_cs + P_switch·R_jc`, R_jc = 0.0948 °C/W = XML Cauer sum, module
> pairs share the baseplate). **R_cs = 0.070 °C/W/module was back-calculated from the CRD's measured 175 °C**
> (non-circular S5 calibration — app-note ~0.08 gives a pessimistic 185 °C). At the design's own 150 kW peak
> (C5, ~170 W/switch) Tj = **105 °C**; over a US06/WLTP-class drive cycle (C9) Tj peaks **116 °C** with rainflow
> ΔTj ≤ 28 °C. The loss→Tj chain and the "TIM+cold-plate dominate" conclusion are confirmed; the calibrated
> R_cs replaces the `[T]` guess for this module/cold-plate.

## Red Team

**Steelman against:** The chain math is textbook, but the two dominant terms in the worked example (`Rth,cs`, `Rth,s-coolant`) are `[T]` placeholders, not sourced for the CAB450's actual cold plate — and they swing 2–3× with bond-line and cold-plate design, so `Tj = 152 °C` could be anywhere from ~135–170 °C. The cooling "−45%/+79%/−39%" figures are *relative* to unstated baselines and come from research demos on small coupons, not qualified 300 kW modules.

**How it could be false:**
1. **Placeholder Rth stages** dominate the result and are unsourced `[T]` — the headline Tj is soft [104].
2. **Relative cooling gains** [102][103] need their baseline pinned before quoting.
3. **Immersion/jet W/cm²** are lab peaks on coupons (some GaN, some boiling), not module-area-averaged automotive flux [102].
4. **Infineon G2 SiC Rth** numbers mix per-die/per-module and variants — verify the exact FS…MA2B datasheet table before quoting [99].

**What would change my mind:** the chosen cold plate's measured `Rth` vs flow curve + `Rth,cs = BLT/(k·A)` for the real bond-line; a full-module qualified flux datapoint at automotive coolant temp; a PLECS/FEA thermal run reproducing the chain.

**Residual doubt:** The chain method, `Zth`-sets-overload logic, and TIM-is-the-bottleneck conclusion are solid and sourced. The specific worked Tj is provisional on two placeholder resistances — flagged, replace with cold-plate data.

---

> **References:** [[citations]]

← [[circuit-components]] | [[procedure-design]] | [[packaging-and-layout]] →
