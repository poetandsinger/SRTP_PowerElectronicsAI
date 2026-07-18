---
title: "AI/ML Applications in Power Electronics Design — 2025-2026"
type: topic
field: ai-agents
created: 2026-07-10
updated: 2026-07-19
status: unverified
evidence: single-study
tags: [ai-agents, power-electronics, ai, machine-learning, design-automation, simulation, review]
sources:
  - sources/ai-agents/pe-gpt-2025-multimodal-pe-design
  - sources/ai-agents/thermrag-2025-pe-thermal-agent
  - sources/ai-agents/agentic-tcad-2026-date
review_by: 2026-08-10
---

# AI/ML Applications in Power Electronics Design — 2025-2026

> AI-side companion to the engineering build manual in [[traction-inverter-index]]; motivation in [[problem-statement-index]].

## AI/ML Applications in Power Electronics Design

### 7.1 Current Application Areas and Performance

| Application Area | AI/ML Method | Key Result | Source |
|-----------------|--------------|-----------|--------|
| **Topology & component optimization** | Generative AI, surrogate modeling, DNNs | Automated design space exploration; AI-driven assistant reduces design time vs manual | IEEE TPEL 2025-2026 [Reliability: High] |
| **Control parameter tuning** | PSO + LSTM/ANN, random forest, KNN | 98.21% positive outcome rate; 84.95% stability recovery rate for grid-following inverters | IEEE TPEL May 2026 [Reliability: High] |
| **Switching efficiency (ZVS prediction)** | Deep learning + time-frequency feature extraction | MAPE < 0.098%, R2 > 0.95, 42.2% accuracy improvement over traditional methods; 93.77% max efficiency | Engineering Apps of AI 2026 [Reliability: High] |
| **Real-time inverter control** | Deep Q-Network (RL) | 1.8% THD (vs 3.9% PI, 2.4% MPC), 2.7% efficiency gain, 35% faster dynamic response | ICIESC 2025 [Reliability: Medium] |
| **Harmonic elimination (multilevel)** | Hybrid metaheuristic + ANN | IEEE 519 compliance; validated on 7/13/21-level CHB inverters | Springer 2026 [Reliability: Medium] |
| **EMI spectrum prediction** | FBA-PIGAN (GAN-based) | Mean spectral error 2.1 dB, 93.8% peak-frequency accuracy, 0.93 physical consistency score on 10kW SiC inverter | IEEE TPEL 2024 [Reliability: High] |
| **Active EMI filtering** | Reinforcement Learning | 25-30 dB attenuation improvements on experimentally measured spectra in automotive drives | IEEE 2024-2025 [Reliability: High] |
| **Thermal resistance surrogate** | DNN | ~99.93% accuracy for power module chip-area optimization vs FEA | Cambridge/SJTU survey 2026 [Reliability: High] |
| **EMI prediction** | KNN | R2 > 0.97, MAE < 5.9 dB-microV for conducted EMI | IEEE 2024 [Reliability: High] |
| **ANN-based multi-objective optimization** | ANN surrogate + optimization | 78% and 67% computational time reduction vs numerical and geometric programming; 1kW prototype achieved 98.4% efficiency, 4.57 kW/dm3 | Wang et al. 2024 [Reliability: High] |
| **SiC X-ray defect screening** | YOLOv5 + Multi-Head Attention | 93% average accuracy on STMicroelectronics ACEPACK/TPACK modules | IEEE 2025 [Reliability: High] |
| **Sensor fault diagnosis** | Ensemble learning + spatiotemporal correlation | 12.5% RMSE reduction vs single-model; deployed on NVIDIA Jetson | MDPI Machines Jul 2025 [Reliability: High] |
| **ITSC fault detection (motor)** | DWT + Transformer | 97% validation accuracy under EV transient drive cycles | MDPI Energies 2025 [Reliability: High] |
| **LLM-based datasheet extraction** | D2S-FLOW | Exact-match score 0.86, F1 score 0.92, 38% reduction in API-token consumption | IEEE 2025 [Reliability: High] |
| **LLM power design (PE-GPT)** | Custom LLM | 22.2% improvement over human experts, 35.6% over other LLMs for DAB and buck converter design | 2024 [Reliability: High] |
| **SPICE + LLM iterative design** | LLM + SPICE feedback loop | Solve rate increased from 15% to 91% on 269 SMPS benchmark tasks (topology adaptation remained difficult) | Nau et al. 2024 [Reliability: High] |

*Sources: arXiv 2606.15948 (Cambridge/SJTU/Leicester/NTHU/NTU survey, Jun 2026) [Reliability: High - comprehensive peer-review survey]; Individual cited papers as listed [Reliability: High for IEEE/Elsevier]*

### 7.2 AI Methods Used in Power Electronics

| Paradigm | Applications | Strengths | Limitations |
|----------|-------------|-----------|-------------|
| **Supervised Learning (ANN, CNN, KNN)** | FEA surrogates, EMI prediction, loss modeling, thermal mapping | High interpolation accuracy; millisecond inference; mature workflows | Data-intensive; weak extrapolation |
| **Physics-Informed Neural Networks (PINNs)** | Electromagnetic field solving, thermal modeling | Embeds physics (Maxwell, heat diffusion); improved data efficiency | Harder to train; problem-specific |
| **Reinforcement Learning** | Topology discovery, active EMI filtering, real-time control | Learns optimal policies without supervised data; handles sequential decisions | Sample-inefficient; reward design is challenging |
| **GANs / Generative Models** | EMI spectrum synthesis, PCB layout generation | Can generate realistic synthetic data | Training instability; mode collapse |
| **Evolutionary / Metaheuristic** | Pareto optimization, magnetic geometry optimization | Gradient-free global search | Slow convergence; high simulation cost without surrogates |
| **LLMs / Knowledge Graphs** | Requirement interpretation, datasheet extraction, SPICE model generation, code generation | Massive knowledge; natural language interface | Hallucination risk; unreliable for verification-critical tasks |
| **Agentic AI Frameworks** | Multi-tool orchestration, simulation-in-the-loop design | Coordinates geometric parameterization, FEA surrogates, optimizers, circuit simulators | Nascent technology; integration challenges |

### 7.3 Key Quantitative Claims from AI Research

1. **Design time reduction:** ANN-based multi-objective optimization reduced computational time by 78% and 67% relative to numerical modeling and geometric programming (Wang et al., IEEE 2024)
2. **Efficiency prediction accuracy:** AI thermal-resistance surrogates achieved ~99.93% accuracy (Cambridge/SJTU survey 2026, citing peer-reviewed results)
3. **EMI prediction accuracy:** FBA-PIGAN on 10kW SiC inverter achieved 2.1 dB mean spectral error, 93.8% peak-frequency accuracy (IEEE TPEL 2024)
4. **RL-based control improvement:** 1.8% THD, 2.7% efficiency gain, 35% faster dynamic response vs PI control (ICIESC 2025)
5. **LLM design capability:** SPICE feedback loop with LLM increased solve rate from 15% to 91% (Nau et al. 2024)
6. **SiC defect detection:** 93% accuracy on X-ray screening via attention-based deep network (IEEE 2025)

---

## Red Team

**Steelman against:** Every result cited here comes from authors with an incentive to report positive outcomes. PE-GPT's "22.2% improvement over human experts" is on specific tasks (DAB, buck converter), not general power electronics design. The "91% solve rate" from LLM+SPICE used 269 benchmark tasks; real design problems are not benchmark-curated.

**How it could be false:** Almost all results are on simplified benchmarks or specific topologies. No study tests AI on a novel, un-curated design problem. The LLM results risk benchmark contamination — training data may include solutions to the exact problems tested. The SPICE+LLM improvement (15%→91%) may reflect prompt engineering of the benchmark, not general design capability.

**What would change my mind:** A blinded A/B test comparing AI-generated and human-expert designs on novel specifications neither has seen. Independent reproduction of the PE-GPT 22.2% claim on traction inverter design specifically.

**Residual doubt:** AI-for-PE is a hot funding area; every paper here comes from authors and institutions that benefit from positive results. The convergence of findings is suggestive but not probative — we need adversarial testing, not more benchmarks.
