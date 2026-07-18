---
title: "Materials & Properties"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, sic, gan, igbt, capacitor, design]
review_by: 2026-10-17
---

## What This Is

A **one-stop property reference** for the materials a traction inverter is built from — semiconductor, substrate, die-attach, baseplate, DC-link dielectric, conductor, magnet, insulation. Consolidates constants used across [[components]], [[thermal-design]], and [[packaging-and-layout]]; those chapters give the *why*, this gives the *numbers*.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge (standard material constants). Values are typical room-temperature figures — verify against the specific grade/datasheet.

## 1. Power Semiconductor Materials

| Property | Si | 4H-SiC | GaN | Consequence |
|----------|----|--------|-----|-------------|
| Bandgap (eV) | 1.12 | 3.26 | 3.4 | WBG → higher Tmax, lower leakage [22] |
| Critical field (MV/cm) | ~0.3 | ~2.2–3.0 | ~3.3 | ~10× → thinner drift → lower Rds·A [22] |
| Electron mobility (cm²/Vs) | 1400 | ~950 | 1500–2000 (2DEG) | GaN best for HF [22] |
| Sat. drift velocity (10⁷ cm/s) | 1.0 | 2.0 | 2.5 | faster switching [22] |
| Thermal cond. (W/cm·K) | 1.5 | 3.7–4.9 | 1.3 (bulk) | SiC removes heat well; GaN bulk poor [22] |
| Max junction (°C) | 150–175 | 175–200 | 150–200 | [[components]] §1 |

**Read:** SiC's ~10× critical field is the whole ballgame — thinner drift region for the same block voltage → far lower `Rds(on)·area` at 1200 V, and 3× thermal conductivity to remove the loss [22]. GaN's mobility wins at MHz but bulk thermal + 650 V ceiling keep it out of traction [22], [[components]] §1.3.

## 2. Substrate Ceramics (DBC / AMB)

| Ceramic | k (W/m·K) | Strength | Use |
|---------|----------:|----------|-----|
| Al₂O₃ (alumina) | 24–30 | low | cheap DBC, lower-power |
| AlN | 150–200 | low-mod | high thermal, brittle |
| **Si₃N₄** | 70–90 | **high (fracture-tough)** | **AMB** — best thermal-cycle robustness for traction `[T]` |

Si₃N₄ AMB trades some conductivity for the mechanical toughness that survives power cycling — why it dominates automotive modules [T], [[packaging-and-layout]] §1.

## 3. Die-Attach & Baseplate

| Material | k (W/m·K) | Notes |
|----------|----------:|-------|
| SAC solder (SnAgCu) | ~60 | Tmelt 217 °C; fatigues under cycling [T] |
| **Sintered silver** | **80–280** | sinters ~250 °C, remelts ~961 °C → high-temp headroom + low Rth; the SiC enabler [104][103] |
| Cu baseplate | ~400 | best spread; CTE mismatch to ceramic |
| AlSiC baseplate | 180–200 | CTE-matched to ceramic, lower fatigue |

## 4. DC-Link Dielectric & Conductors

| Material | Key property | Use |
|----------|--------------|-----|
| Metallized PP film | self-healing, ESR <1 mΩ, low ESL, Tmax ~105–125 °C | **DC-link cap** — [41], [[components]] §3 |
| Electrolytic (Al₂O₃) | high C-density but ESR 10–100 mΩ, dry-out | **excluded** from traction [41] |
| Copper (busbar) | σ ≈ 5.8×10⁷ S/m | laminated busbar; I²R + `Lσ` [118] |

## 5. Machine Materials (context)

| Material | Property | Note |
|----------|----------|------|
| Sintered NdFeB magnet | Br ~1.2–1.4 T; needs Dy/Tb for high-temp coercivity | IPMSM rotor; demag limit [T], [[machine-and-load]] §6 |
| Electrical steel (laminated) | low core loss, thin gauge | stator/rotor core [T] |
| Hairpin Cu winding | high slot fill → low Rs | modern traction stator [T] |
| Inverter-duty enamel | PD-resistant per IEC 60034-18-41 Type I | survives SiC dv/dt [87] |

## 6. Thermal Interface (cross-ref)

Full TIM table in [[thermal-design]] §5: grease 2.9–7.5, PCM 3–7, graphite 5–15, sintered-Ag 80–280 W/m·K [104].

## Red Team

**Steelman against:** These are textbook room-temperature constants; real device/module behavior is temperature-dependent (SiC thermal conductivity falls ~1/T, mobility drops with T, magnet Br falls ~0.1%/°C) and grade-specific. A single-number table invites quoting a 25 °C value at 150 °C operation. Several substrate/magnet/steel rows are `[T]` standard knowledge, not tied to a specific supplier datasheet.

**How it could be false:**
1. **Temperature dependence omitted** — SiC k, mobility, and NdFeB Br all move strongly with T; the table is a 25 °C snapshot [22].
2. **Ranges span grades** — critical field, ceramic k, sintered-Ag k vary 2–4× by grade/process; use the actual datasheet.
3. **`[T]` rows** (ceramics, magnet, steel) are general knowledge, not sourced to a part.

**What would change my mind:** temperature-dependent property curves from the chosen device/module/magnet datasheets replacing the 25 °C singletons.

**Residual doubt:** Correct as an orientation/lookup reference and the *relative* physics (why SiC, why Si₃N₄ AMB, why sintered Ag, why PP film) is solid and sourced. Use datasheet values at operating temperature for any real calculation.

---

> **References:** [[citations]]

← [[components]] | [[thermal-design]] | [[packaging-and-layout]] →
