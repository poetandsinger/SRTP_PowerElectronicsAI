---
title: "Plan — Guardrails & evidence gates"
type: plan
field: project
created: 2026-07-17
updated: 2026-07-19
tags: [plan, ai-agents, plecs, protection, standards]
---

# Guardrails & evidence gates

> Topic of [[plan-ai-agent-mas]]. These are the **evaluator's rubric** for the evaluator-optimizer loop ([[plan-design-loop]] §3). Adopted from PE-MAS, re-tuned to traction. Domain grounding: [[protection-and-safety]], [[standards-and-compliance]].

## 1. Domain guardrails REVISE, NEED [[standards-and-compliance]] ( hard rules — system-prompt + post-sim hooks)

Non-overridable; injected as system-prompt constraints **and** enforced as post-simulation hooks so a violating result never enters agent context (Claude Code PostToolUse pattern — [[harness-architecture-patterns]] P3):

1. **Safety / thermal margin:** Tj ≤ 150 °C (Si) / 175 °C (SiC), **≥25 °C margin**; ASC engages within spec on critical fault.
2. **Voltage:** Vds ≤ 80 % Vbr; Vdc ripple ≤ 5 %; DC-link cap rating ≥ 1.2× Vdc,max.
3. **Current:** Id,cont ≤ 80 % rated; Ipeak ≤ 90 % rated for ≤10 ms.
4. **Physical realism:** 0 < η < 100 %; flag >99 % as suspicious; no NaN/inf.
5. **Modulation feasibility:** MI in achievable range for the topology; overmodulation only when intended.
6. **Thermal consistency:** P_loss(elec) ≈ ΔT/Rth(thermal) within 10 % — mismatch ⇒ model error, not a valid design.
7. **Standards flags:** ISO 26262, CISPR 25, IEC 61800-5-1 violations are raised.

Conflict order (PE-MAS): **safety > compliance > physics > efficiency > cost > size.**

## 2. Evidence gates (before release — the rubric)

Corner-based; each is a measurable criterion the optimizer's objective and the Validator's judge share:

| Gate | Criterion | Owner |
|---|---|---|
| **Efficiency** | η ≥ cited baseline at **≥3 corners** | Validator |
| **Thermal** | Tj ≤ Tj,max − 25 °C worst case (low-speed high-torque) | Validator |
| **THD** | line-current THD ≤ 5 % at rated power | Validator |
| **Stress** | all Vds/Id/Tj within derated limits | Validator |
| **EMI (screen)** | dv/dt ≤ threshold, conducted pre-compliance check | Validator |
| **Standards** | no flagged ISO 26262 / CISPR 25 / IEC 61800-5-1 violation | Validator |
| **Citation** | every design claim cites a **retrievable** source ([[plan-knowledge-rag]]) | Validator |
| **Cost** | BOM within stated band of baseline | Validator |
| **Human signoff** | design-review package presented; human approves | process gate |

**Hard rule:** no gate may close as "PLECS-backed" against an **unvalidated** model ([[plan-plecs-harness]] §3).

## 3. Judge mechanics (DRCY)

- Run the reviewer **k=3** independently, reconcile with a **consensus step on a separately-configured model**. Multi-run findings get higher confidence; single-run findings are critically evaluated.
- Gate failures return to the **narrowest** responsible stage via the `iterate` router ([[plan-design-loop]] §4).

## 4. Anti-Goodhart caution

Gates are metrics; metrics get gamed. Two guards: (a) the **citation gate** ties design choices to external evidence, not just to passing numbers; (b) **human signoff** on the review package is the backstop the optimizer cannot optimize away. Watch for designs that pass all gates but are physically odd — the red-team's "design by checklist" risk ([[traction-inverter-mas-integration]] §7).

← [[plan-ai-agent-mas]] | [[plan-design-loop]] | [[plan-plecs-harness]] | [[protection-and-safety]]
