---
title: "Standards & Compliance"
type: topic
field: power-electronics
created: 2026-07-10
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, ieee, iec, iso, aec-q, standards, review]
review_by: 2026-10-17
---

# Standards & Compliance

> The standards a traction inverter must meet — and, for each, **what it actually requires of the design**: the voltage classes, creepage numbers, ASIL metrics, qualification test suites, and EMC limits, not just the designations. The standard texts are paywalled and were **not read in full**; numeric values come from official base documents, standards-body summaries, or reputable app notes, each tagged by reliability. Treat every number as a starting point to confirm against the purchased text before design freeze.

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge. Reliability tags: **[H]** standard text / multi-source; **[M]** single reputable technical source; **[TPS]** third-party summary of a paywalled clause.

## 1. The Landscape — What Each One Governs and the Requirement That Bites

| Standard | Governs | The requirement that actually constrains the design | Cite |
|----------|---------|------------------------------------------------------|------|
| **IEC 61800-5-1:2022** | PDS electrical/thermal/energy safety | creepage/clearance vs working voltage; stored-energy discharge to ≤60 V | [86][113][149] |
| **IEC 61800-5-2:2016** | PDS functional safety | defines STO/SS1/SS2/… safety sub-functions and their SIL | [150] |
| **ISO 26262:2018** | vehicle E/E functional safety | ASIL from S×E×C; HW metrics SPFM/LFM/PMHF; FTTI budget | [85][151] |
| **AEC-Q101** | discrete SiC/Si device qual | stress suite (HTRB/HTGB/H3TRB/TC/PTC/ESD) at defined conditions | [89][152] |
| **AEC-Q100** | IC (gate driver, MCU) qual | temperature Grade 0/1 for under-hood; 7 test groups | [153] |
| **AEC-Q200** | passive (DC-link cap, filter) qual | 85/85 humidity-bias, thermal-cycle, endurance on R/C/L | [154] |
| **ECPE AQG 324** (04.1/2025) | power-**module** qual | power cycling PCsec/PCmin; EOL = +5% Vf / +20% Rth; SiC annex | [88][141] |
| **CISPR 25 Ed.5:2021** | on-board EMI | conducted/radiated dBµV limits, Class 1–5 | [114][115] |
| **ISO 7637-2 / -4** | conducted transients (12 V / HV) | transient pulse immunity on the DC lines | [155] |
| **LV123 / LV124** | German-OEM HV / 12 V component spec | HV voltage-range test points; 12 V electrical/environmental | [156] |
| **ISO 16750-2** | environmental electrical loads | dielectric withstand (HiPot), insulation resistance | [137] |
| **ISO 6469-3 / UN ECE R100** | EV electrical safety | ≤60 V DC touch threshold; ≥100 Ω/V isolation; ≤0.2 J | [157] |

## 2. Electrical Safety — Isolation, Creepage, Discharge

**Voltage classes set the whole shock-protection scheme.** Both IEC 61800-5-1 (via *Decisive Voltage Class*, DVC) and the automotive world (ISO 6469-3 / R100 / ZVEI "voltage class") draw the same line: **≤60 V DC or ≤30 V AC-rms is touch-safe** (DVC A/B, ELV); above it (an 800 V bus is DVC C/D / VC B) the design must protect against direct contact [149][156][157] **[H]**. HV band spans **60 V < U ≤ 1500 V DC** [156] **[H]**.

**Creepage and clearance** are inherited from IEC 60664-1: **clearance** ← impulse-withstand voltage + pollution degree (PD2 typical inside a sealed inverter); **creepage** ← working voltage + PD + material group (CTI) [113][149] **[H]**. Reinforced insulation ≈ 2× basic. Worked points:

| Working / impulse (PD2) | Clearance | Creepage (basic → reinforced) | Cite |
|-------------------------|-----------|-------------------------------|------|
| 1500 V impulse (functional) | 0.5 mm | — | [149] |
| 6000 V impulse (reinforced) | 5.5 mm | — | [149] |
| 565 V working | — | 2.8 mm → **5.6 mm** | [149] |
| **~800 V DC working, reinforced** | **~5.5–8 mm** | **~8–11.4 mm** | [113][149] |

**Stored-energy discharge:** after HV disconnect, the DC-link (hundreds of µF) must bleed to the touch-safe **≤60 V within 5 s** (or ~1 s where quicker access is possible); active discharge meets the window, a passive bleeder is the minutes-range backup [149][157] **[TPS]**. ISO 6469-3 also caps accessible **stored energy at ≤0.2 J** for the no-shock class [157] **[M]**. This is the standards basis for the ASC/safe-discharge duty in [[protection-and-safety]] §5 and [[procedure-design]] §7. **Isolation resistance:** ≥**100 Ω/V for the DC bus**, ≥500 Ω/V AC [157] **[H]**. Dielectric withstand (HiPot) to representative **1500 V AC** per ISO 16750-2 [137] **[TPS]**.

## 3. Functional Safety — ISO 26262 + IEC 61800-5-2

**ASIL is computed, not chosen:** `ASIL = f(Severity S0–3, Exposure E0–4, Controllability C0–3)` → QM/A/B/C/D; only **S3×E4×C3 = ASIL D** [85][151] **[H]**. Unintended torque/acceleration (esp. from standstill) lands **ASIL D**; loss-of-torque ≈ **ASIL C** [124], [[protection-and-safety]] §6.

**Hardware architectural metric targets** (Part 5) — the numbers a traction-inverter ECU must prove [151] **[H, multi-source]**:

| Metric | What it bounds | ASIL B | ASIL C | ASIL D |
|--------|----------------|:------:|:------:|:------:|
| **SPFM** (single-point fault) | residual/single-point faults | ≥90% | ≥97% | ≥99% |
| **LFM** (latent fault) | undetected latent faults | ≥60% | ≥80% | ≥90% |
| **PMHF** (random-HW failure) | prob. of SG violation | <100 FIT | <100 FIT | **<10 FIT** |

**Timing:** the safety mechanism must **detect (FDTI) + react (FRTI) inside the FTTI** (fault→hazard time); a gate-driver SC reaction <2 µs sits ~10⁵× inside the ~200 ms traction FTTI (item-specific, *not* a standard constant) [124][151] **[M]**. ISO 26262 has **12 parts**; **Part 11 (semiconductors)** is the one that speaks directly to the SiC die [151] **[H]**.

**IEC 61800-5-2 safety sub-functions** — the drive-level actions ISO 26262 calls on, each ratable to **SIL 1/2/3** (IEC 61508) [150] **[M]**:

| Function | Does | Function | Does |
|----------|------|----------|------|
| **STO** Safe Torque Off | remove torque energy (gate disable); base fn, often SIL 3 | **SOS** Safe Operating Stop | hold position, stay energized |
| **SS1** Safe Stop 1 | ramp-down → STO (stop cat. 1) | **SLS** Safely-Limited Speed | cap speed |
| **SS2** Safe Stop 2 | stop, stay energized (cat. 2) → SOS | **SDI / SLI / SLP** | safe direction / increment / position |
| **SBC** Safe Brake Control | drive external holding brake | **SSM / SAR** | safe speed monitor / accel range |

STO maps directly to the inverter's **ASC/freewheel** safe states [[protection-and-safety]] §5. Reference designs that carry the assessment: **TI TIDM-02009** (ASIL D, TÜV SÜD) and **NXP** S32K39 + GD316x [124].

## 4. Device & Module Qualification — the Test Suites

Qualification is component-level and **feeds** functional safety but is distinct from it. Two tiers: **discrete/IC** (AEC-Q) and **power module** (AQG 324).

**AEC-Q101** discrete SiC/Si stress suite (Rev-E base doc) [89][152] **[H/M]**:

| Test | Stress | Condition |
|------|--------|-----------|
| **HTRB** | reverse-bias blocking | 1000 h, Tj,max, 80–100% rated V |
| **HTGB** | gate-oxide | 1000 h, Tj,max, max VGS |
| **H3TRB** | humidity + blocking | 85 °C / 85 %RH, 1000 h, ~80% VDS |
| **TC** | thermal cycling | −40→+150 °C, 1000 cycles |
| **PTC/IOL** | power cycling | ΔTj-driven (JESD22-A105) |
| **HTSL / Autoclave** | storage / moisture | 1000 h Tstg,max / 121 °C 100%RH |
| **ESD** | HBM + CDM | classified by withstand level |

**AEC-Q100** (gate-driver ICs, MCU): temperature **Grade 0 (−40…+150 °C)** or **Grade 1 (−40…+125 °C)** for traction; HTOL 1000 h; 7 test groups A–G (environment, lifetime, package, die, electrical, screening, cavity) [153] **[M]**. **AEC-Q200** (DC-link film cap, EMI-filter passives): 85/85 humidity-bias, temperature cycling, endurance/HTOL, terminal-strength, ESD — the qualifying stresses for the ripple-duty DC-link [154], [[components]] §3.

**AQG 324 (ECPE, Rev 04.1/2025)** — power-**module** qual, the SiC-relevant one [88][141] **[H, from guideline text]**:
- **Power cycling** splits by load on-time: **PCsec (ton < 5 s)** stresses **chip-near** interconnect (die-attach, bond wires/metallization); **PCmin (ton > 15 s)** additionally stresses **chip-remote** system solder [141].
- **End-of-life = +5% forward voltage (Vf/VCE,sat/VDS) or +20% thermal resistance (Rth)** [141] **[H]** — the same criteria used in [[reliability-and-lifetime]] and [[protection-and-safety]] §7.
- **TST** −40→+125 °C ~1000 cycles; **H3TRB** 85 °C/85%RH/1000 h at 0.8× blocking, VGE=0; lifetime fit to **B5 at 80% confidence** (VDA) [141].
- **SiC Annex (QL-09/10/11):** **DGS** dynamic gate stress (gate-oxide/Vth), **DRB** dynamic reverse bias, **dynamic H3TRB** — the switching-stress tests standard HTRB/HTGB miss [141]. Cosmic-ray SEB is still a **separate** accelerated-neutron test, not in AQG 324 [121], [[protection-and-safety]] §1.

## 5. EMC & Transients — CISPR 25, ISO 7637, LV

**CISPR 25 Ed.5** protects on-board receivers **150 kHz–2.5 GHz**; **Classes 1–5**, ~**6 dB per class step**, Class 5 tightest. Conducted **voltage method** uses a **5 µH LISN** over 0.15–108 MHz; current-probe to 245 MHz; radiated (ALSE) to 2.5 GHz [114][115], [[emi-emc-design]] §1. Representative **Class 5 conducted (voltage-method) limits, dBµV** [114] **[TPS — third-party table, verify vs CISPR 25:2021]**:

| Band | Freq | Peak | QP | Avg |
|------|------|:----:|:--:|:---:|
| LW | 0.15–0.30 MHz | 70 | 57 | 50 |
| MW | 0.53–1.8 MHz | 54 | 41 | 34 |
| SW | 5.9–6.2 MHz | 53 | 40 | 33 |
| VHF | 26–54 MHz | 44 | 31 | 24 |
| **FM** | **76–108 MHz** | **38** | **25** | **18** |

The FM band (**38 Pk / 18 Avg**) is the hardest for a fast-switching SiC inverter — the driver of the input filter in [[emi-emc-design]] §3.

**ISO 7637** transient immunity on the DC lines: **-2** (12/24 V) defines Pulses 1, 2a/2b, 3a/3b (inductive-disconnect, supply-spike, fast bursts); **ISO/TS 7637-4** (HV, 60–1500 V DC) adds **Pulse A** (HF burst, models SiC ringing) and **Pulse B** (LF sinusoidal, models motor-driven transients) [155] **[M]**. **LV123** fixes HV-component voltage-range test points (min/nom/max); **LV124** the 12 V supply-variation + environmental suite — de-facto for German OEMs [156] **[M]**.

## Red Team

**Steelman against:** This chapter now *looks* authoritative because it has numbers, and that is exactly the risk. The load-bearing values are secondary: the creepage points, the CISPR 25 Class-5 table, and the discharge-time rule are all from app notes and a third-party calculator, not the purchased standard texts. Several genuinely important figures are **not in any free source** — the exact DVC A/B/C/D boundaries, the 800 V reinforced creepage as a *stated* value (it is extrapolated here), the AEC-Q101 ESD class thresholds, the AQG 324 DGS/DRB voltages, and the LV123 HV sub-class bands. A reader could cite "≥100 Ω/V" or "38 dBµV" as gospel when program-specific tailoring routinely overrides them.

**How it could be false:**
1. **Creepage at 800 V is derived, not quoted** — the 8–11.4 mm comes from a TI app note's method [113][149], not IEC 60664-1 Table F.4 directly; material group (CTI) and real pollution degree move it.
2. **CISPR 25 table is third-party** [114] and OEMs redefine classes/bands per program — the number to design to is the customer EMC spec, not this table.
3. **Discharge "≤60 V in 5 s"** [149][157] is the commonly-cited rule; the exact clause, residual-energy threshold, and which access case applies were not confirmed against the standard.
4. **ISO 26262 metric targets are firm and multi-sourced** [151] — but SPFM/LFM/PMHF are computed from FMEDA failure-rate *assumptions*; the metric passing is only as good as the FIT data behind it.
5. **AQG 324 EOL (+5% Vf / +20% Rth) and PCsec/PCmin** are extracted from the guideline text [141] and are the most trustworthy numbers here; the AEC-Q durations are JEDEC-standard but device-program-tailored.

**What would change my mind:** the purchased IEC 61800-5-1 + IEC 60664-1 tables giving stated 800 V creepage/clearance; the CISPR 25:2021 limit tables; the customer's EMC and HV-safety specs; a device FMEDA showing the SPFM/LFM/PMHF actually met.

**Residual doubt:** The *structure* — which standard owns which requirement, and the qualification/safety/EMC split — is solid and well-sourced. The ISO 26262 metrics and AQG 324 criteria are trustworthy; the electrical-safety dimensions and the CISPR 25 table are directional until replaced by the standard texts and the program's own spec.

---

> **References:** [[citations]]

← [[protection-and-safety]] | [[emi-emc-design]] | [[traction-inverter-index]] →
