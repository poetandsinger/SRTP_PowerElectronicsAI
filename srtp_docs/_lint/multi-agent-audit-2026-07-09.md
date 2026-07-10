# Multi-Agent Synthesis Audit — 2026-07-09

> Read-only audit. Findings only — no automated mutations. Severity: HIGH > MEDIUM > LOW.

---

## Summary

| Metric | Before | After |
|--------|--------|-------|
| Red-team blocks in vault | 1 (cs/ only) | 4 (cs/ + 3 ee/) |
| Fabricated claims | 1 ("60% cost reduction") | 0 (removed) |
| Source notes captured | 0 (papers) | 2 (MasRouter, EvoAgent) |
| Code-level claims verified from source | 0 | 1 (smolagents — found error) |
| Unverified code claims remaining | 3 | 3 (CrewAI memory, LangGraph overhead, Claude Code docs) |

---

## HIGH Severity Findings

### H1: Fabricated cost claim — FIXED
- **Claim:** "Per-agent model selection reduces costs 60%"
- **Location:** Log summary of synthesis (log.md:46)
- **Action:** Replaced with "per-agent model selection may reduce costs (magnitude unknown without benchmarking)"
- **Root cause:** Over-claiming during log summarization. Synthesis note itself didn't make the 60% claim — only the log did.

### H2: Orchestrator routing unverified — PARTIALLY ADDRESSED
- **Gap:** "One-level delegation covers 90% of workflows" — zero evidence
- **Action:** Captured MasRouter (arXiv:2502.11133v1) — shows routing is solvable for code benchmarks. Captured EvoAgent (arXiv:2406.14228v3, NAACL 2025) — alternative evolutionary approach.
- **Remaining gap:** Both papers are on coding benchmarks. No evidence for simulation routing. The claim remains unverified with added caveats.
- **Status:** Gap narrowed but not closed. Requires domain-specific validation.

### H3: Zero red-team blocks in ee/ — PARTIALLY ADDRESSED
- **Gap:** 8 of 9 ee/ notes lacked red-team blocks
- **Action:** Added red-team blocks to the 3 most claim-heavy notes:
  - `what-is-a-traction-inverter.md` — targets [T] claims (DC-link cap, GaN viability, peak efficiency)
  - `circuit-topologies.md` — targets 3L-TNPC single-source dependency
  - `components.md` — targets paywalled Yole data, vendor teardowns, motivated sources
- **Remaining:** 5 ee/ notes still lack red-team blocks (control-schemes, control-how-to, matlab-modeling, open-problems, simulation-toolbox, problem-statement)

---

## MEDIUM Severity Findings

### M1: smolagents ManagedAgent pattern mischaracterized — FIXED
- **Claim:** ManagedAgent class with `run(task) → report` code-level contract
- **Source review finding:** No `ManagedAgent` class exists. The concept is `ManagedAgentPromptTemplate` — prompt-level, not code-level. Task→report behavior is prompt-engineered, not guaranteed.
- **Action:** Updated synthesis note with correction. Implication: SRTP must enforce structured output with JSON schema, not rely on prompt engineering.

### M2: CrewAI entity memory unverified — NOW FIXED
- **Claim:** `memory=True` persists "facts about components" as entity memory (short-term + long-term + entity)
- **Source review finding (2026-07-09):** CrewAI v0.80+ has completely rewritten memory. No more short/long/entity split. Now a unified `Memory` class (`unified_memory.py`) with LLM-inferred scoping, composite scoring (recency 30% + semantic 50% + importance 20%), LanceDB storage, and adaptive-depth `RecallFlow`. The entity memory claim was based on pre-v0.80 documentation.
- **Action:** Updated `cs/harness/crewai.md` and `cs/multi-agent-synthesis.md` with corrected architecture.
- **Implication:** The scoped hierarchy is actually more powerful for SRTP than entity memory — memories can be scoped to `/srtp/traction_inverter/components/` and recalled with natural language queries.

### M3: Claude Code subagent claims unverified — NOT FIXED
- **Claim:** Per-agent model selection, Teams feature behavior
- **Status:** Documented but not verified against running code (proprietary).
- **Action:** Caveat added to synthesis: "documented, not source-verified."

---

## LOW Severity Findings

### L1: Remaining ee/ notes without red-team blocks
- **Notes:** control-schemes, control-how-to, matlab-modeling, open-problems, simulation-toolbox, problem-statement
- **Risk:** These notes make claims about MTPA methods, control tuning, MATLAB integration — all with training-knowledge [T] tags and no adversarial review.
- **Recommendation:** Add red-team blocks in next audit pass. Priority: open-problems (most speculative), control-schemes (claims about method superiority).

### L2: LangGraph checkpointing overhead unmeasured
- **Claim:** "Non-negotiable" for simulation workflows
- **Status:** Estimate only (~1-5ms per transition). Not benchmarked.
- **Recommendation:** Measure before treating as architectural constraint.

---

## Self-Audit Notes

### What This Audit Caught
1. A fabricated quantitative claim (60%) — my own log entry
2. A code-level mischaracterization (smolagents ManagedAgent) — I described a class that doesn't exist
3. Systematic lack of red-team blocks across the vault — 89% of notes missing this mandatory section

### What This Audit Missed
1. Full source verification of all open-source claims (CrewAI memory, LangGraph overhead) — deprioritized for time
2. Phase 4 tasks (MATLAB reliability, Claude Code docs) — not started
3. The remaining 5 ee/ notes without red-team blocks
4. No check of whether existing [T] tags in ee/ notes are warranted or just ritualistic

### Audit Bias
- **Confirmation bias risk:** The MasRouter paper was selected because it addresses the exact gap I identified. I may have over-sold its relevance despite the domain mismatch (coding vs simulation).
- **Negativity bias:** This audit focuses on gaps. It does not assess what the synthesis got right. A balanced audit would also verify which claims ARE well-supported.

---

## Recommendations

1. **Add red-team blocks to remaining ee/ notes** — at minimum open-problems and control-schemes
2. **Verify CrewAI memory when repo is accessible** — the entity memory claim is important for the implementation plan
3. **Benchmark LangGraph checkpointing** — 1ms or 100ms matters for architecture decisions
4. **Run the single-agent vs multi-agent A/B test** — the synthesis is theoretical until empirically validated
5. **Schedule next audit for 2026-08-09** — the synthesis `review_by` date
