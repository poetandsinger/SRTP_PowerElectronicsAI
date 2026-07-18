---
title: "EMI / EMC Design"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, emi, dvdt, sic, design, protection]
review_by: 2026-10-17
---

## What This Is

Why a SiC inverter is an EMI source and how to tame it: standards, noise modes, input filter, motor-side dv/dt, bearing currents, layout. SiC's fast edges make this harder than for IGBT — the chapter the procedure-design only names ([[procedure-design]] §8).

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge.

## 1. The Target — CISPR 25

- **Scope:** protects *on-board* receivers, **150 kHz–2.5 GHz**, at the **component/module** level (DUT + harness on a bench) [56][114].
- **Conducted (CE):** voltage method (LISN) **0.15–108 MHz** in dBµV; current-probe **0.1–245 MHz** in dBµA [115].
- **Radiated (RE):** ALSE method, 150 kHz–2.5 GHz, dBµV/m [114].
- **Classes 1–5:** Class 5 = most stringent, Class 1 = most permissive; **~6 dB per class step** [114]. A traction inverter shares the HV harness near sensitive receivers → typically **Class 5** (or OEM-specified) [114].
- **LISN:** a **5 µH** line-impedance network stabilizes source impedance (~50 Ω HF) and provides the measurement port; two LISNs on HV+/HV−, the idle one 50 Ω-terminated [115].
- Representative Class-5 CE voltage limits (Pk/QP/Avg dBµV): LW 150–300 kHz **70/57/50**; VHF 30–54 MHz **44/31/24**; FM 76–108 MHz **38/25/18** [114] *(third-party tables — verify vs CISPR 25:2021).*

## 2. Common-Mode vs Differential-Mode

- **DM** — line-to-line (HV+↔HV−), driven by DC-link switching-ripple current; a loop problem [116].
- **CM** — line-to-ground/chassis, `i_CM = C_par·dv/dt`, returning through parasitics [117].
- **Dominant CM source:** the fast switching node coupled through **parasitic capacitance to the heatsink/baseplate/chassis** (die→substrate cap→baseplate→heatsink→chassis→source) and motor winding-to-frame capacitance [117].
- **Why SiC is worse:** hard-switched SiC dv/dt is **40–150 kV/µs** (vendor data; the 15–50 kV/µs often quoted is conservative) — since `i_CM ∝ dv/dt`, faster edges inject proportionally larger CM current and push spectral energy higher, worsening conducted **and** radiated CM emissions [117][108]. `Rg`/active gate drive trades dv/dt (EMI) against switching loss [108], [[gate-driver-design]] §2.

## 3. HV-Input EMI Filter

Worked 800 V DC filter (automotive CE target) [116]:

| Element | Value | Role |
|---------|-------|------|
| CM choke | ~**1.5 mH** | high series-Z to CM current |
| X-caps (DM, line-line) | ~**170 nF** effective (e.g. 2× series); range 0.01–2.2 µF | DM shunt |
| Y-caps (CM, line-chassis) | e.g. **4× 47 nF** (~188 nF); Y2 range 1–470 nF, ~1000 VDC | CM shunt — **at the input terminals** |

- **Targets:** ~**60 dB CM / 40 dB DM at 300 kHz**; CM corner ~9.5 kHz, DM ~65 kHz [116].
- CM-choke **leakage inductance** (~1% of L) doubles as the DM inductor with the X-caps [116].
- **Y-cap total is capped** by HV chassis-leakage / isolation-monitoring limits — you cannot add Y-cap freely [116].
- Production 800 V/550 kVA SiC designs integrate the filter with a full-ceramic DC-link [116].

## 4. Motor-Side dv/dt — Reflected Wave

- **Mechanism:** fast edges launch a traveling wave; the high-Z motor terminal reflects it → **~2× bus voltage** at the terminals ("reflected-wave" / long-cable overvoltage) [120].
- **Magnitudes:** industrial 460 V → 1200–1600 V; 575 V → ~2100 V [120]. Faster dv/dt **lowers the critical cable length** for full doubling, so even short EV cables are edge-stressed [120].
- **Insulation:** motor must be inverter-duty **Type I per IEC 60034-18-41** (partial-discharge-free) [87].
- **Filters:** dv/dt filter (slows edge, ~15–50 m cables); sine-wave filter (near-sinusoidal, long cables) [120].

## 5. Bearing Currents (EDM)

- **Cause:** CM voltage couples across the air gap to the shaft; lubricant film breaks down → **EDM discharge → fluting/pitting** [119].
- **Numbers:** PWM drives put **50–1500 V** CM on the shaft; EDM cuts bearing life to 25–50% [119]. Fast SiC edges + high fsw make EV motors especially exposed [119].
- **Mitigations:** shaft grounding ring (shaft <1 V), ceramic/hybrid bearings, insulated bearings, CM chokes / reduced source CM voltage. **Best practice: insulated bearing on NDE + shaft-grounding ring on DE** [119][54].

## 6. Layout & Shielding — Attack the Source First

Order of levers: **layout → grounding → shielding → filtering** [118].

- **Laminated busbar** (parallel plates, dielectric <100 µm) minimizes DC-link `Lσ` → cuts overshoot and the source magnetic-loop EMI [118], [[packaging-and-layout]].
- **Minimize commutation-loop area** (cap↔module) → less radiated H-field and overshoot [118].
- **Shielded enclosure + single-point HF grounding**; bond heatsink/baseplate CM path directly to chassis; Y-caps at the HV entry [117][118].

## 7. Engineer's Checklist

1. Fix the target: CISPR 25 class (usually 5), CE 0.15–108 MHz + RE to 2.5 GHz [114].
2. **Attack the source:** slowest dv/dt (largest `Rg`/active gate) that meets switching-loss + dead-time — every dv/dt cut reduces `i_CM` linearly [108][117].
3. **Shrink parasitics:** laminated low-`Lσ` busbar, minimal loop area, defined HF return for device→heatsink capacitance [118].
4. **Input filter:** CM choke + Y-caps (chassis-leakage-limited) for CM; X-caps + choke leakage-L for DM; size corners for ~40 dB DM / 60 dB CM at the worst frequency; Y-caps at terminals [116].
5. **Motor side:** dv/dt/sine filter + Type-I insulation for 2× reflected-wave [87][120].
6. **Bearings:** shaft-grounding ring (DE) + insulated/ceramic (NDE); shaft <1 V [119].
7. **Verify with LISN pre-compliance scan**, iterate source vs filter [115][116].

## Red Team

**Steelman against:** The specific numbers are the soft spots. The Class-5 dBµV limits come from a third-party calculator, not the CISPR 25:2021 text (and OEMs tailor classes/bands per program). The 2× reflected-wave / 1200–2100 V figures are industrial 460/575 V VFD practice, not an 800 V automotive drive with a <3 m cable. And `i_CM = C·dv/dt` with "40–150 kV/µs" lumps a distributed, frequency-dependent parasitic network into one capacitor and one slew number.

**How it could be false:**
1. **CISPR limits unverified** against the standard text; also customer-tailorable [114].
2. **Reflected-wave magnitudes** are industrial [120]; EV short cables may not fully double at the fundamental — the risk is **edge-rate-driven**, so compute the actual critical length from measured rise time.
3. **dv/dt and i_CM** are order-of-magnitude sizing inputs; confirm with a double-pulse dv/dt and a measured/simulated CM-impedance model before finalizing filter attenuation [117].
4. **Filter values** [116] are one worked 800 V design — not universal; depends on the actual noise spectrum.

**What would change my mind:** a LISN pre-compliance scan of the real hardware; the purchased CISPR 25 tables + OEM EMC spec; a measured CM impedance model; the actual harness critical-length calc.

**Residual doubt:** The *method* (source→parasitics→filter→motor→bearings) and *directions* are solid and well-sourced. Every numeric limit/filter value is a starting point to be replaced by the standard text and a bench scan.

---

> **References:** [[citations]]

← [[procedure-design]] | [[packaging-and-layout]] | [[standards-and-compliance]] →
