---
title: "PE-MAS: Power Electronics Multi-Agent Design Studio"
type: source
field: ai-agents
tags: [ai-agents, preprint, plecs, multi-agent, langgraph, simulation, integration]
authors: [spongelovesorange]
year: 2026
venue: "GitHub"
url: "https://github.com/spongelovesorange/PE-MAS"
captured: 2026-07-09
reliability: medium
peer_reviewed: false
reliability_note: "Solo developer project (0 stars, no description). Python + LangGraph. Active development through Jun 2026 (518KB, 173 files). Not peer-reviewed but highly relevant as closest prior art to SRTP. Implementation quality appears high — well-structured with typed state, guardrails, skills, memory, HITL."
sha256: placeholder
---

# PE-MAS: Power Electronics Multi-Agent Design Studio

## Summary

PE-MAS is the closest prior art to the SRTP project — a **working multi-agent system for power electronics design** using LangGraph StateGraph, domain guardrails, a skills system, lifelong memory, PLECS integration, and evidence-gated release. Currently scoped to flyback converter design, but the architecture is domain-agnostic.

## Architecture

### Workflow (LangGraph StateGraph)

10 agent nodes in the flyback design workflow:

```
requirements → designer → magnetics_advisor → component_selector → simulator → validator
                                                                                    ↓
                                                                         route_validation()
                                                                          ↙        ↘
                                                                     PASS/MAX_ITR   FAIL
                                                                          ↓           ↓
                                                                     correction   END (HITL)
                                                                          ↓
                                                                   memory_synthesizer
                                                                          ↓
                                                                       reporter → END
```

**Conditional routing:**
- `route_validation()`: PASS → correction; FAIL with max iterations → correction (generate report with failed state); FAIL under max → END (human review)
- `route_requirements()`: chitchat → END; skill request → skill_executor; design task → designer

**Checkpointing:** Postgres (with MemorySaver fallback). Two compiled graphs: `app` (with HITL interrupts) and `app_headless` (autonomous).

**Human-in-the-loop:** `interrupt_before=["selector", "simulator", "reporter", "correction"]`

### State Definition (`PowerSupplyState`)

Richly typed with ~30 fields including:
- `specifications: DesignSpecs` — parsed electrical specs
- `request_profile: DesignRequestProfile` — intent classification (new_design, modify_existing, follow_up_qa, etc.)
- `theoretical_design: TheoreticalDesign` — calculated parameters (Lp, Ipk, N, Dmax, Vor)
- `bom: BillOfMaterials` — real components (mosfet, diode, controller, transformer, caps, EMI filter, snubber)
- `simulation_results: SimulationMetrics` — PLECS output (efficiency, ripple, Vds_spike, convergence)
- `verification: VerificationResult` — PASS/FAIL/WARN/NEEDS_HUMAN_REVIEW
- `reasoning_trace: List[ReasoningTraceItem]` — DeepRare-style traceability (step, agent, action, evidence, conclusion, confidence)
- `literature_references: List[EvidenceSource]` — verified sources (Paper, Datasheet, AppNote, Standard, Web)
- `memory_context`, `memory_writeback`, `memory_insights` — lifelong learning artifacts
- `execution_plan`, `planning_summary` — plan-then-execute
- `evidence_grade`, `peer_review_findings`, `simulation_consistency` — quality gates

### Domain Guardrails

**Hard guardrails** (non-overridable, injected as system prompt):
1. Safety and stress margin first — reject designs with marginal Vds spikes
2. Duty cycle feasibility — keep Dmax in practical range (0.35–0.45 for wide-input flyback)
3. Soft-switching preference — valley switching / QR / ACF where applicable
4. CCM/DCM tradeoff must be explicit — explain mode choice
5. Ripple, EMI, thermal, isolation are pass/fail gates
6. Physical realism — flag unrealistically high efficiency as suspicious
7. Conflict resolution: safety > compliance > physics > efficiency > cost > size

**Knowledge retrieval:** Dual-path RAG — (1) .docx keyword scoring (`_score_chunk` with Wu-Mannber-style overlap + domain-term bonus) + (2) llama_index vector index subprocess. Merged results with deduplication.

### Skills System (`SkillManager`)

**Per-skill structure:**
```
skills/<skill_id>/
├── manifest.json   # {name, description, version, author, capabilities, entry_point}
├── prompt.txt      # Skill-specific system prompt
└── tools.py        # Callable tool functions
```

**Skill matching:** Jaccard-style token overlap between query tokens and (capabilities + name + description + tool names), with bonuses for description and entry_point.

**Singleton pattern:** `SkillManager.__new__` ensures one instance. `refresh_skills()` detects stale skills by mtime comparison. `recommend_skills()` returns top-5 scored skills.

**Skill execution:** `skill_executor_node` invokes skill entry_point via `tools_module`. Skills can be loaded per-design-step via the `active_skill` state field.

### Lifelong Memory

**SQLite-backed** with tables for:
- Design records keyed by spec hash
- Quality scoring (0.0–1.0) per design iteration
- Power-band tagging (low_power <15W, mid_power <45W, high_power >45W)
- Iteration playbooks — best strategies for each correction type

**Memory synthesis:** `memory_synthesizer_node` runs after correction to write iteration learnings back to the DB.

### Evidence Gates

- **PLECS validation matrix** across line/load corners
- **Loop evidence** for TL431/opto feedback, Bode response, PM/GM, CTR aging
- **Thermal evidence** for MOSFET, rectifier, transformer, snubber, capacitor ripple
- **EMI/safety evidence** for input filter, layout, pre-scan fields
- **BOM source-quality** for custom magnetics and mains EMI/filter items
- **Human signoff** before any release-ready claim

Designs are presented as "engineering review packages" until all gates close.

### PLECS Integration

- `plecs_interface.py` — PLECS API wrapper
- `plecs_generator.py` — auto-generate PLECS models from design params
- `plecs_mcp_client.py` — MCP client for PLECS (optional)
- Separate `plecs-mcp/` package for local PLECS MCP helper

### Data Adapters

- `datasheet.py` — datasheet parsing
- `digikey.py` — DigiKey API
- `nexar_octopart.py` — Nexar/Octopart for BOM sourcing
- `literature.py` — literature retrieval

## Relevance to SRTP

This is **direct prior art** — it implements almost exactly what our synthesis proposed:

| Our Synthesis Proposal          | PE-MAS Implementation                                                                                                                    | Match                                                       |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| LangGraph StateGraph            | ✅ `workflow = StateGraph(PowerSupplyState)`                                                                                              | **Exact**                                                   |
| Role-based agent nodes          | ✅ 10 nodes (requirements, designer, magnetics, selector, simulator, validator, correction, reporter, skill_executor, memory_synthesizer) | **Matches**                                                 |
| Conditional edges for iteration | ✅ `route_validation()`, `route_requirements()`                                                                                           | **Exact**                                                   |
| Checkpointing                   | ✅ Postgres + MemorySaver fallback                                                                                                        | **Exact**                                                   |
| Human-in-the-loop               | ✅ `interrupt_before=[...]`, `NEEDS_HUMAN_REVIEW`                                                                                         | **Exact**                                                   |
| Domain guardrails               | ✅ `HARD_GUARDRAILS_PROMPT` — 7 non-overridable rules                                                                                     | **Exact**                                                   |
| Skills system                   | ✅ `SkillsManager` with manifest.json + prompt.txt + tools.py, Jaccard scoring                                                            | **Matches** (different from Hermes skills but same concept) |
| Entity memory                   | ✅ SQLite lifelong memory with quality scoring, power-band tagging, iteration playbooks                                                   | **Exact**                                                   |
| Post-tool validation            | ✅ `design_validator_node` (928 lines of real validation!)                                                                                | **Exact**                                                   |
| Evidence before release         | ✅ 6 evidence gates (PLECS, loop, thermal, EMI, BOM, human)                                                                               | **More rigorous** than our proposal                         |
| Structured output               | ✅ TypedDict for all state fields (DesignSpecs, BOM, SimulationMetrics, etc.)                                                             | **Exact**                                                   |
| Reasoning traceability          | ✅ DeepRare-inspired ReasoningTraceItem with confidence scores                                                                            | **Beyond** our proposal                                     |

### What PE-MAS Has That We Didn't Plan

1. **Plan-then-execute:** `build_execution_plan()` + `planning_summary` — plans the design workflow before running it
2. **Best-effort tracking:** `best_design_candidate` — keeps the best design across iterations
3. **Correction review:** Post-validation alignment check against original user intent
4. **Iteration playbooks:** Memory of which corrections worked for which failure modes
5. **Dual knowledge retrieval:** Keyword + vector hybrid RAG with subprocess isolation
6. **Evidence grading:** `evidence_grade`, `peer_review_findings`, `simulation_consistency` fields

### What We Have That PE-MAS Doesn't

1. **Provider-agnostic** — PE-MAS uses `get_llm()` which appears to be a single provider
2. **Cron scheduling** — Hermes Agent infrastructure
3. **Multi-platform delivery** — Gateway
4. **Cross-session memory** — Hermes memory is persistent across sessions
5. **Broader domain scope** — PE-MAS is flyback-only; SRTP targets traction inverters

## Critical Assessment

**Strengths:**
- Real, working code — not a paper or proposal
- Hard guardrails are exactly what domain-specific agents need
- Evidence gates prevent over-confident design releases
- The state design is thorough (30+ typed fields)
- Skills system is lightweight and well-implemented

**Weaknesses:**
- Solo developer, 0 stars, no community — single point of failure
- Flyback-only — topology assumptions are baked into state fields
- PLECS-only — no MATLAB/Simulink, no LTSpice, no open-source simulators
- No published evaluation — no benchmarks comparing PE-MAS designs against human engineers
- Heavy LangChain dependency (llama_index, langgraph, langchain_core)
- Chinese-language knowledge base (.docx with Chinese filename) limits accessibility

**Integration recommendation:** Adopt PE-MAS patterns for:
1. Domain guardrails (non-overridable safety rules)
2. Evidence gates before design release
3. Skills system structure (manifest.json + prompt.txt + tools.py)
4. State design with reasoning traces and confidence scoring
5. Plan-then-execute workflow
6. Best-effort tracking across iterations

Keep our differentiation: provider-agnostic, **PLECS as primary simulation backend** (matching PE-MAS, per the 2026-07 pivot — see re-clone below), traction inverter domain (not flyback), Hermes infrastructure (cron, gateway, cross-session memory).

---

## 2026-07-17 Re-clone — PLECS MCP, model generation, and the honest model-registry

Re-cloned at the user's direction to inspect the **PLECS MCP** (the repo grew substantially since the 2026-07-09 capture). This is the single strongest piece of prior art for the SRTP MATLAB→PLECS pivot: a **working** MCP + XML-RPC PLECS backend inside a power-electronics MAS.

### Two PLECS access paths (selectable via `PE_MAS_PLECS_BACKEND=auto`)
- **Direct XML-RPC** — `core/flyback_mas/tools/plecs_interface.py` (`run_plecs_simulation`).
- **MCP** — standalone `plecs-mcp/` package (`run_plecs_simulation_via_mcp`).
- `rpc.py` is a thin wrapper: `xmlrpc.client.ServerProxy(rpc_url(), allow_none=True)`, plus `call()`, and **`call_first_available(candidates)`** which tries multiple RPC method names — a robustness pattern for **PLECS-version drift** (different builds expose different RPC methods).

### `plecs-mcp` tool surface (~29 FastMCP tools)
- **Introspection/robustness:** `ping`, `list_methods`, `inspect_method`, `rpc_call`, `rpc_catalog`, `rpc_try_methods`, `rpc_profile`, `rpc_batch`, `discover_capabilities` — the server *probes* the live PLECS to learn what it supports.
- **Model mgmt:** `open_model`, `close_model`, `list_open_models`, `save_model`, `save_model_as`.
- **Simulation:** `simulate`, `simulate_advanced` (full optStruct), `simulate_flyback` (domain wrapper).
- **Parameters:** `get_component_param`, `set_component_param`, `set_component_params_batch`.
- **Scripting/editing:** `run_script` (language `plecs`/octave), `circuit_action`, `circuit_patch`, `script_transaction`.
- **Console/UI:** `clear_console`, `get_console_output`, `ui_action_catalog`, `ui_invoke`, `ui_macro`.

### Model generation — "XML injector" over a base template
`core/flyback_mas/tools/plecs_generator.py` (`PLECSGenerator`) parses a **base `.plecs` template as XML** (`xml.etree.ElementTree`), indexes existing components, and **injects primitive components** (`inject_component` → `<Component><Type>…</Type><Param Name=…>…</Param></Component>`), writing a per-session model. Confirms the **template + XML-injection** path is real (not just `ModelVars` tuning) — but note it's basic and template-anchored, not free-form topology synthesis.

### The honest bottleneck: `data/plecs/model_registry.json`
Only **Flyback** is `status: available` (and `validation_status: unvalidated`). Buck/Boost/Buck-Boost/DAB are `not_in_release`/`planned` with the note: *"add a validated local model before claiming PLECS coverage."* **Lesson for SRTP:** the constraint is **validated per-topology PLECS models**, not the agent. Traction inverter coverage (2L-B6, 3L-NPC, 3L-TNPC, ANPC + PMSM/IM load) each needs a built-and-validated PLECS model before any "PLECS-backed evidence" can be claimed.

### Evidence gates are corner-based
`nodes/simulation.py` resolves a **simulation corner** (`low_line`/`high_line`/`nominal`) and `_build_evidence_closure` only closes the PLECS gate when waveforms exist across corners (`low_line_seen`, `high_line_seen`, `plecs_waveforms`). Directly implements the "≥3 operating points" evidence gate we specced.

**Net:** the pivot is de-risked. A reference PLECS MCP exists; the remaining SRTP work is (a) traction-inverter PLECS model templates + validation, and (b) the topology/control/physics reasoning that Ordonez's agent (and this template-injector) do **not** do. See [[plecs-xmlrpc-scripting-interface]] and [[plecs-ai-agent-integration-ordonez]].
