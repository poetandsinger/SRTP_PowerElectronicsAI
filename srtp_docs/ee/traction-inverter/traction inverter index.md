---
title: Traction Inverter Industry Research
type: index
field: ee
created: 2026-07-07
updated: 2026-07-08
tags: [ee, traction-inverter, index]
---

## Notes in this Cluster

| Note | Content |
|------|---------|
| [[ee/traction-inverter/what-is-a-traction-inverter]] | First principles: what it does, why it is needed, energy flow, vehicle context |
| [[ee/traction-inverter/circuit-topologies]] | Deep dive: 2L-B6, 3L-NPC, 3L-ANPC, 3L-TNPC — circuits, switching states, trade-off matrix |
| [[ee/traction-inverter/components]] | Power semiconductors (SiC/IGBT/GaN), gate drivers, DC-link caps, sensors, thermal management |
| [[ee/traction-inverter/control-schemes]] | FOC, DTC, MTPA, SVPWM, DPWM, overmodulation, field weakening, ISO 26262 safety |
| [[ee/traction-inverter/control-how-to]] | Practical FOC recipe: parameter tuning, MTPA, field weakening, safety limits |
| [[ee/traction-inverter/matlab-modeling]] | Simulink/Simscape modeling at 4 fidelity levels, solver config, PLECS integration |
| [[ee/traction-inverter/simulation-toolbox]] | Tools, licenses, and hardware needed to run the simulations |
| [[ee/traction-inverter/open-problems]] | Active research questions and design tensions |
| [[research/audit-changelog-traction-inverter]] | Source-fidelity audit changelog (what was verified and what was fixed) |

## Reading Order

1. Start with [[ee/traction-inverter/what-is-a-traction-inverter]] to understand *why* the inverter exists and what it controls.
2. Read [[ee/traction-inverter/circuit-topologies]] to learn the circuit options.
3. Read [[ee/traction-inverter/components]] to understand what physical parts make it work.
4. Read [[ee/traction-inverter/control-schemes]] for the theory, then [[ee/traction-inverter/control-how-to]] for the practical implementation.
5. Read [[ee/traction-inverter/matlab-modeling]] and [[ee/traction-inverter/simulation-toolbox]] to see how to model and validate it.
6. Finish with [[ee/traction-inverter/open-problems]] for the unresolved research questions.

## Scope

This research catalogues the state of traction inverter design in the electric vehicle industry: which topologies are in production, what power semiconductors are used, key design parameters, and how major OEMs approach inverter design. Data verified against OEM teardowns (Munro & Associates, UBS Evidence Lab), datasheets, and academic literature.

## Production Topologies

### 2-Level VSI (B6) — Dominant (>95% of production EVs)

The conventional two-level voltage-source inverter with six half-bridge switches remains the overwhelming industry standard.

**Why dominant:**
- Simplest topology — fewest semiconductor switches (6 per inverter)
- Lowest component count and BOM cost
- Well-understood control (SVPWM, DPWM)
- Most mature gate-driver and protection IC ecosystem
- SiC MOSFET adoption has extended 2-level viability to 800V+ systems

**Who uses it:**
- Tesla Model 3/Y/S/X (SiC), Nissan Leaf (IGBT), Toyota Prius (IGBT), BYD Han/Seal (SiC), VW ID.3/ID.4 (IGBT), Hyundai Ioniq 5 (SiC), Porsche Taycan (SiC), Lucid Air (SiC)

**Limitations:**
- Fixed two-level switching limits part-load efficiency
- High dv/dt stress on motor windings (especially with SiC)
- Requires larger DC-link capacitor for ripple handling
- Higher THD compared to multilevel topologies

### 3-Level NPC — Research/Pre-Production

Neutral-Point-Clamped: each leg has four switches and two clamping diodes connected to DC-link midpoint. Outputs three voltage levels (+Vdc, 0, -Vdc).

- **Advantages:** Half voltage stress per switch, lower THD, reduced dv/dt, doubled effective switching frequency
- **Disadvantages:** More switches (12 vs 6), clamping diodes (6), neutral-point balancing complexity, uneven loss distribution
- **Who uses:** Limited automotive traction — mainly industrial VFDs and railway traction. Research prototypes for next-gen EVs.
- **Why not production:** Cost/complexity penalty too high for automotive. SiC at 800V addresses many 2-level limitations that would motivate NPC.

### 3-Level ANPC — Research (2030 Projection)

Active Neutral-Point Clamped: replaces clamping diodes with active switches for better loss distribution.

- **Advantages:** Better loss distribution, fault-tolerant switching states, lower conduction losses than NPC
- **Disadvantages:** 18 switches per 3-phase (most complex), complex gate-drive requirements, higher BOM cost
- **Status:** Evaluated in Sachs & Neuburger (2025). No known production automotive application as of 2026.

### 3-Level T-Type NPC (TNPC) — Most Promising Multilevel

T-type NPC uses a bidirectional switch connected between output and DC-link midpoint.

- **Key finding (Sachs & Neuburger, 2025):** "3L-TNPC inverter, realised with only 30% additional SiC chip area, lowers drive-cycle drivetrain losses by 0.67 kWh/100 km relative to a SiC 2L-B6 baseline."
- **Advantages:** Only 12 switches, excellent partial-load efficiency (key for automotive), lower conduction losses at mid-voltage
- **Disadvantages:** Switch voltage rating must be full DC-link (unlike NPC/ANPC that halve it), NP voltage balancing needed
- **Status:** Research stage. Most cost-effective multilevel candidate for 2030 BEVs.

### Other Topologies (Not Suitable for Automotive)

| Topology | Status | Why Not |
|----------|--------|---------|
| Flying Capacitor Multilevel | Research | Large capacitor bank, high component count |
| Cascaded H-Bridge | Not suitable | Needs isolated DC sources |
| Modular Multilevel (MMC) | Not suitable | Too bulky for automotive |
| Current Source Inverter | Niche | Requires large DC inductor, poor part-load efficiency |
| Matrix Converter | Research | Limited voltage transfer ratio, complex commutation |

## Power Semiconductor Components

Semiconductor comparison data is presented throughout this document.

| Parameter | Si IGBT | SiC MOSFET | GaN HEMT |
|-----------|---------|------------|----------|
| Voltage rating | 650–1200V | 650–1700V | 650V (lateral) |
| Current rating | 200–800A | 100–800A | 30–150A |
| Switching freq | 5–20 kHz | 20–100 kHz | 100 kHz–1 MHz |
| Bandgap | 1.12 eV | 3.26 eV | 3.39 eV |
| Tj max | 150–175°C | 175–200°C | 150–200°C |
| Cost ($/A relative) | 1x baseline | 2–3x (declining) | 1.5–3x |
| Primary auto use | 400V traction, HEV/PHEV | 400V–800V+ traction | OBC, DC-DC, 48V |
| Production maturity | 30+ years | Since 2017 (Tesla) | Since ~2020 (OBC) |
| Short-circuit withstand | ~10 µs | 3–5 µs | <1 µs |

### Si IGBT — Declining Share in BEV

Still dominant in 400V cost-sensitive segments and hybrids. Infineon estimates IGBT still >60% of automotive power semiconductor revenue in 2025.

**Major suppliers:** Infineon (HybridPACK Drive, ~30% market share), onsemi (VE-Trac), STMicroelectronics (ACEpack), Fuji Electric, Mitsubishi, Semikron Danfoss, BYD Semiconductor (in-house)

**Who still uses IGBT:** Nissan Leaf (all generations), Toyota Prius (all generations), VW ID.3/ID.4 (MEB entry trims), BYD early models, most 400V Chinese compact EVs, HEV/PHEV applications.

### SiC MOSFET — Fastest Growing

Tesla's 2017 Model 3 adoption was the watershed moment. Yole Group: automotive SiC market ~$2B (2024) → >$6B by 2029.

**Major suppliers:** STMicroelectronics (~40% automotive SiC, Tesla's primary), Wolfspeed (XM3, WolfPACK), onsemi (EliteSiC), Infineon (CoolSiC), Rohm (4th-gen), Bosch, BYD Semiconductor (in-house)

**Who uses SiC:** Tesla Model 3/Y/S/X, Hyundai Ioniq 5/Kia EV6/Genesis GV60 (E-GMP), Porsche Taycan, Lucid Air, BYD Seal/Han (premium), VW PPE platform, Mercedes EQS/EQE, NIO/XPeng/Li Auto (Chinese premium 800V)

**Key advantages:** ~10× critical E-field enables thinner drift region, no tail current (50-70% switching loss reduction vs IGBT), unipolar device scales favorably at partial load, enables higher switching frequency → smaller passives.

### GaN HEMT — Not Ready for Traction

Primary automotive use today: on-board chargers (3.3–22 kW) and DC-DC converters (400V→12V). No production BEV uses GaN for traction as of 2026.

**Key limitation:** 650V rating limits use to 400V DC-link; limited current ratings for 100 kW+ traction. Toyota/Denso have demonstrated GaN-based traction for sub-50 kW segment.

## Key Design Parameters

### DC-Link Voltage Classes

| Class | Range | Battery | Who Uses | Key Trade-off |
|-------|-------|---------|----------|---------------|
| 400V | 300–450V | 350–400V | Nissan Leaf, Tesla Model 3 SR, VW MEB entry, most Chinese EVs | Mature ecosystem, lower cost; limited charging power (~200 kW) |
| 800V | 600–900V | 700–800V | Porsche Taycan, Hyundai E-GMP, Lucid Air, BYD Seal, VW PPE | Half current → reduced losses; 350 kW+ charging; requires 1200V semiconductors |
| 900V+ | 800–1,000V | 900–924V | Lucid Air (only production example) | Maximizes efficiency at extreme power; limited component ecosystem |

### Power Levels

| Range | Vehicle Class | Examples | Typical Topology |
|-------|--------------|----------|-----------------|
| <100 kW | Compact/commuter | Nissan Leaf (80 kW), VW ID.3 (93 kW), Wuling Mini (20 kW) | 2-level IGBT, 300–400V |
| 100–250 kW | Mid-size/family | Tesla Model 3 (211 kW), VW ID.4 (150 kW), Ioniq 5 (168 kW) | 2-level IGBT or SiC, 350–800V |
| 250–500 kW | Performance/large | Tesla Model 3 Perf (~380 kW), Taycan (560 kW), Ioniq 5 N (478 kW) | 2-level SiC, 400–800V |
| >500 kW | Ultra/hypercar/truck | Model S Plaid (~760 kW), Lucid Sapphire (~920 kW), Rimac Nevera (1.4 MW) | Multiple 2-level SiC, 400–924V |

### Efficiency Targets

| Metric | Si IGBT 2-Level | SiC MOSFET 2-Level | SiC 3-Level TNPC (2030) |
|--------|:---:|:---:|:---:|
| Peak efficiency | 96–98% | 98–99% | ~99% |
| WLTP cycle-average | ~92–95% | ~96–98% | ~97–98.5% |
| Range benefit vs baseline | — | +3–5% | +3–4% vs SiC 2L |

**Key insight:** Peak efficiency is misleading. WLTP/EPA drive cycles average only 15-25% of peak power, where inverter losses are dominated by partial-load semiconductor behavior. SiC's unipolar characteristic gives disproportionate benefit here.

**Loss breakdown (typical 2-level SiC, 150 kW):**
- Semiconductor conduction losses: 30-40%
- Semiconductor switching losses: 20-30%
- DC-link capacitor ESR losses: 5-10%
- Busbar/connector I²R: 5-10%
- Gate driver + control: 2-5%
- Motor harmonic losses (topology-dependent): 10-20%

## Major OEM Inverter Designs

### Major OEM Inverter Designs

The following summarizes each manufacturer's approach. Data from OEM teardowns (Munro & Associates, UBS Evidence Lab), IEEE literature, and supplier datasheets.

## Semiconductor Supply Chain

| Supplier | Si IGBT Share | SiC Share | Key Automotive Customers |
|----------|:---:|:---:|----------|
| Infineon | ~30% | Growing | VW Group, Hyundai, many European OEMs |
| STMicroelectronics | Medium | ~40% | Tesla (primary), Hyundai (secondary) |
| onsemi | Growing | Growing | VW Group, various |
| Wolfspeed | — | Major | Multiple (via module partners) |
| Rohm | — | Growing | Various Japanese OEMs |
| Bosch | — | Emerging | VW Group (Reutlingen fab) |
| BYD Semiconductor | In-house | In-house | BYD (vertical integration) |

**Critical supply chain fact:** BYD is the only OEM that manufactures its own power semiconductors at scale (both IGBT and SiC). BYD Semiconductor SiC capacity exceeded 30,000 wafers/month (6-inch equivalent) by 2024.

## Key Trends

1. **800V migration accelerating** — Porsche (2019) → Hyundai (2021) → BYD/VW (2023+) → Tesla Cybertruck (2024). Almost all new premium platforms are 800V.
2. **SiC replacing IGBT in BEV traction** — Tesla (2017) → Hyundai (2021) → BYD (2022) → VW PPE (2024). IGBT holding in 400V cost-sensitive and HEV.
3. **Multilevel topologies not yet production-ready for automotive** — TNPC most promising for 2030 per Sachs & Neuburger.
4. **Power density race** — 30-50 kW/L (2024) → 50-100 kW/L (2025 target) → 100+ kW/L (2030 target) via WBG + advanced packaging.
5. **Vertical integration trend** — Tesla, BYD, and increasingly VW/Hyundai moving inverter design in-house. BYD unique in fabricating own semiconductors.


> **References:** [[citations]]


← [[cs/harness/harness index|Agent Harness Research]] | [[README|SRTP Index]]
