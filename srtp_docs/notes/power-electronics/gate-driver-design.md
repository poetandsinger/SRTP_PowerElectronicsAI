---
title: "Gate-Driver Design"
type: topic
field: power-electronics
created: 2026-07-17
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [power-electronics, traction-inverter, gate-driver, sic, protection, design, example]
review_by: 2026-10-17
---

## What This Is

The gate-driver deep-dive: rails, resistor sizing, protection, isolation, bias, real ICs, worked example. Behind [[components]] §2 and [[procedure-design]] §5. Reference device: Wolfspeed CAB450M12XM3 (1200 V/450 A SiC) — all its electrical values below are datasheet-sourced [92].

**Citation convention:** `[NN]` → [[citations]]; `[T]` → training knowledge; `[derived]` → computed here.

## 1. Drive Rails — Why +15 V / −4 V

- **Datasheet VGS: −4 V/+15 V static, abs-max −8/+19 V** [92]. Common alternatives: +15/−3, +18/−3 [112].
- **+15 V (not 18–20 V):** RDS(on) keeps falling to ~18 V but with diminishing returns; 15 V is the efficiency/gate-oxide-stress compromise Wolfspeed uses on its own modules [92][107].
- **Negative off-rail defeats Miller-induced false turn-on.** When the complementary device turns on, switch-node dv/dt drives `i = C_GD·dv/dt` through the gate loop, lifting VGS; if it exceeds VGS(th), shoot-through [107][109].
- **SiC VGS(th) is low → thin margin:** CAB450M12XM3 **VGS(th) = 2.5 V typ (1.8 min), falling to ~2.0 V at 175 °C** [92]. A 0 V off-state leaves almost no noise margin against a hot device; **−3 to −4 V** restores several volts [107][109].
- **Don't over-negative:** beyond ~−5 to −8 V risks threshold instability/oxide stress and raises 3rd-quadrant (body-diode) dead-time loss [108]. Sweet spot −3 to −4 V; 0 V with a strong active Miller clamp is a documented cost option [108].

## 2. Gate Resistor, Peak Current, Drive Power

- **Trade-off:** small `Rg` → fast dv/dt, lower switching loss, but more overshoot/ringing/EMI and worse Miller cross-talk; large `Rg` → clean but higher Eon/Eoff. `Rg` is the primary switching-trajectory knob [107][108].
- **Peak gate current:** `Ig,peak = (Von − Voff)/(Rg,ext + Rg,int)` — the driver output stage must supply this.
- **Average drive power:** `Pdrive = Qg·Vdrive·fsw`; average current `Ig,avg = Qg·fsw` — this sizes the isolated bias supply.
- **CAB450M12XM3 gate data (VDS=800 V, VGS=−4/+15, ID=450 A):** **Qg = 1300 nC, Qgd = 475 nC, Rg,int = 2.5 Ω** (at 100 kHz) [92].

## 3. Protection

| Function | Requirement | Why |
|----------|-------------|-----|
| **Desaturation (DESAT)** | detect in ~300 ns, blank the turn-on VDS collapse | SiC's resistive output (no VCE(sat) knee) makes threshold/blanking harder than IGBT; must retune [108][110][126] |
| **Short-circuit withstand** | total detect+off **inside 1–3 µs** | SiC SCWT ~1–3 µs (Wolfspeed FM3: **2.9 µs @ 800 V/175 °C**) vs ~10 µs IGBT [110]; SCWT falls with bus voltage |
| **Soft / two-level turn-off** | staged/elevated Rg,off on fault | bounds `Lσ·di/dt` overshoot from ~1000 A fault current below BV [110][111] |
| **Active Miller clamp** | low-Z clamp when VGS < ~2 V | shunts `C_GD·dv/dt` so it can't raise VGS [109][111] |
| **Dual UVLO** | on **both** rails | +rail UVLO avoids high-RDS(on) partial-on (thermal runaway); −rail UVLO ensures the off-margin exists [111] |

DESAT clearing a hard fault in ~300 ns cuts dissipated energy from ~1.4 J to <0.2 J — large SOA margin [110].

## 4. Isolation

- **Reinforced isolation** across the HV/LV barrier for 800 V automotive: governed by **IEC 61800-5-1** (creepage/clearance from working voltage, pollution degree, altitude) and **UL 1577** (VISO in kVrms) [86][113].
- **Creepage/clearance:** ~**8 mm** typical reinforced parts; **~11.4 mm** for 800 V-margin parts; up to ~14.5 mm extra-wide [113].
- **CMTI ≥ 100 kV/µs** required for SiC (switch-node slew 50–150 kV/µs); best parts 150–200 kV/µs — far above old IGBT-driver ~50 kV/µs [107][111].

## 5. Isolated Bias Supply

Asymmetric-output push-pull "gate bricks", ~2 W/switch:

| Module | Output | Isolation | Note |
|--------|--------|-----------|------|
| Murata MGJ2 | +15/−5 V (and variants), 2 W | **5.2 kVDC** | purpose-built bridge bias [112] |
| RECOM RxxP21503D | **+15/−3 V**, 2 W | 6.4 kVDC, 65 kV/µs CM | SiC-targeted, <10 pF barrier [112] |
| Würth MagI³C | +15/−4 class | reinforced | drop-in [112] |

Size so +rail rating ≫ `Qg·fsw` + clamp/quiescent (worked below).

## 6. Real Gate-Driver ICs

| IC | Peak drive | Isolation / CMTI | Protection |
|----|-----------|------------------|-----------|
| **TI UCC5880-Q1** | 5–20 A, **SPI-adjustable** | 5.0 kVrms / **150 kV/µs** | DESAT, two-level turn-off, Miller clamp, dual UVLO, ADC monitor, FuSa [93][111] |
| **Infineon 1ED3491MC12M** | ±9 A | 5.7 kV / 100 kV/µs | DESAT, soft-off, Miller clamp [111] |
| **onsemi NCV57000** | ~7.8 A | >5 kV / ~100 kV/µs | DESAT+soft-off, Miller clamp, dual UVLO [111] |
| **Skyworks Si828x** | high, split pins | 5.0 kV / **>200 kV/µs** | DESAT, Miller clamp, UVLO [111] |

## 7. Worked Example — CAB450M12XM3 @ 16 kHz

Inputs [92]: Qg=1300 nC, Rg,int=2.5 Ω, Von=+15, Voff=−4 → **Vdrive=19 V**.

- Choose **Rg,ext = 4.0 Ω** (datasheet test condition) → Rtot=6.5 Ω → **`Ig,peak = 19/6.5 = 2.9 A`** [derived].
- **`Pdrive = 1300 nC·19 V·16 kHz = 0.40 W/switch`**; **`Ig,avg = 1300 nC·16 kHz = 20.8 mA`** on +15 V [derived].
- Bias check: 20.8 mA ≪ MGJ2 (80 mA) / RECOM (93 mA); a 2 W brick covers the 0.4 W with 2–3× headroom [112].
- **Rg sensitivity** (Rg,int=2.5 Ω fixed):

| Rg,ext | Rtot | Ig,peak |
|-------:|-----:|--------:|
| 0 Ω | 2.5 Ω | 7.6 A (fastest dv/dt) |
| 1 Ω | 3.5 Ω | 5.4 A |
| 4 Ω | 6.5 Ω | 2.9 A (datasheet) |

All fit UCC5880-Q1 (20 A) and 1ED3491 (9 A); NCV57000 (~7.8 A) only covers Rg,ext ≥ 0 marginally — so the driver constrains how aggressively you shrink Rg [93][111].

## Red Team

**Steelman against:** `Ig,peak = V/(Rg,ext+Rg,int)` and `Pdrive = Qg·Vdrive·fsw` are idealizations. The real gate current is not rectangular — the Miller plateau holds VGS nearly constant so the effective driving voltage is far below 19 V there, gate-loop inductance rings the waveform, and Rg,int=2.5 Ω is a distributed value measured only at 100 kHz [92]. So the "2.9 A / 0.4 W" figures are sizing bounds, not the actual waveform.

**How it could be false:**
1. **Formula idealization** — lumps Miller plateau, loop inductance, and frequency-dependent Rg,int into a linear model; true peak is lower/non-rectangular [92].
2. **Qg = 1300 nC is nominal** (VDS=800 V, ID=450 A); Qgd scales with bus voltage and shifts at partial load — worst-case differs [92].
3. **Pdrive is total charge-energy**, ignoring source/sink split, active-clamp sink pulses, quiescent and fault currents — hence 2 W bricks for a <0.5 W nominal load [112].
4. **SCWT "2.9 µs" is one module** (Wolfspeed FM3, 800 V/175 °C, Rg=4 Ω) [110] — strongly condition-dependent; don't quote generically.
5. **Driver-IC CMTI/creepage** from product pages — re-confirm against the exact orderable-part datasheet [111].

**What would change my mind:** a double-pulse test giving the real gate-current waveform, measured dv/dt, and turn-off overshoot at the chosen Rg; and the specific device's SCWT at worst-case Tj/VGS.

**Residual doubt:** The design *method* and *directions* (negative bias, Rg trade, desat-inside-SCWT, reinforced iso, bias headroom) are solid and datasheet-grounded. The exact worked numbers are first-order until a double-pulse bench confirms them.

---

> **References:** [[citations]]

← [[components]] | [[schematics]] | [[protection-and-safety]] →
