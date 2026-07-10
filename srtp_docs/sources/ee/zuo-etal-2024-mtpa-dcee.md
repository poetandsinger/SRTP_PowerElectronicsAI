---
title: "Auto-Optimized Maximum Torque Per Ampere Control of IPMSM Using Dual Control for Exploration and Exploitation"
authors: [Yuefei Zuo, Yalei Yu, Jun Yang, Wen-Hua Chen]
year: 2024
venue: "arXiv preprint"
arxiv: "2404.18176v1"
captured: 2026-07-08
reliability: medium
peer_reviewed: false
reliability_note: "Preprint. Proposes RLS-based DCEE method for online MTPA tracking."
---

## Abstract

In this paper, a maximum torque per ampere (MTPA) control strategy for the interior permanent magnet synchronous motor (IPMSM) using dual control for exploration and exploitation (DCEE). In the proposed method, the permanent magnet flux and the difference between the d- and q-axis inductance are identified by multiple estimators using the recursive least square method. 

The audit confirmed this paper supports online RLS-based MTPA with better dynamic performance than extremum seeking. However, it does NOT explicitly state "noise and convergence risk" — that was authorial inference added to open-problems.md.

## Vault References
- [[ee/traction-inverter/control-schemes]] — MTPA section
- [[ee/traction-inverter/open-problems]] — MTPA tracking challenges
- [[_lint/audit-changelog-traction-inverter]] — Correction documented
