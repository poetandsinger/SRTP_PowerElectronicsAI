# ROADMAP — SRTP Power Electronics AI

> Phases, milestones, and the definition of "done" for the multi-agent system that designs traction inverters.
> Strategic view. Active tasks live in [TODO.md](TODO.md); the dev journal is [LOG.md](LOG.md).
>
> Repo reorganized 2026-07-20 to the `knowledge/ system/ experiments/ results/` layout (see [knowledge/SCHEMA.md](knowledge/SCHEMA.md) §Repository Organization).

---

## Where we are

🟡 **Knowledge base complete; PLECS evidence layer in progress.** The 29-chapter traction-inverter textbook and the agent-architecture research are built and red-teamed (cited [1]–[170]). The PLECS harness works headless and the first 2L-B6 model is **confirmed heat-sink-coupled**. The gap is **evidence, not authoring**: every design note is still `status: unverified` because not one validated η/loss/Tj number has cleared the SOP yet.

## Phases

### Phase 0 — Knowledge base ✅ DONE
29-chapter traction-inverter engineering textbook + AI-agent architecture research (12 harness deep-dives, 26 source captures). Every claim carries truth-status + evidence + a red-team block. Cited [1]–[170].

### Phase 1 — PLECS evidence harness ⏳ IN PROGRESS
Prove PLECS can produce trustworthy numbers headless.
- ✅ Readback blocker cleared — `simulate`'s `Values` is empty in 4.8; the working path is `ToFile`→CSV.
- ✅ Reusable harness (`system/src/`): template + direct-RPC runner + numpy summarizer + `system/configs/model_registry.json`.
- ✅ Wolfspeed PLECS model library (669 models) organized under `system/env/models/wolfspeed/`; CAB450M12XM3 loads + runs.
- ✅ 2L-B6 CAB450 model **heat-sink coupling CONFIRMED** (Tj bounded at ambient, not the 684 °C uncoupled runaway).
- ⏳ **Blocker to close the phase:** one validated 2L-B6 number — real 800 V loaded operating point → 9-corner matrix → calibrated to the Wolfspeed/TI 300 kW CRD.

### Phase 2 — Serial 4-topology validation ☐
One validated PLECS model per production/candidate topology, built **serially** (do not start the next until the current is registered `validated`):
**T1 2L-B6 SiC → T2 3L-TNPC → T3 3L-ANPC → T4 3L-NPC.** Each track: model (`.plecs` text variant) → 9-corner matrix → fill the `design-<topology>-<voltage>-<device>` note → fold back into `circuit-topologies` + agnostic notes → Red Team → `model_registry` entry `validated`.

### Phase 3 — Multi-agent system ☐
The live MAS that automates the design loop. 3-agent core (Orchestrator drives Planner + Designer + Validator) on typed LangGraph state (`InverterDesignState`), RAG-first, evidence-gated. Core mechanism: **topology → refine → parameter-optimize** with an *explicit numerical optimizer* over PLECS (LLM picks structure, optimizer picks numbers). Subsystems: architecture · design-loop · knowledge-rag · plecs-harness · guardrails-and-evidence · memory · tech-stack.

### Phase 4 — Evaluation & benchmark ☐
Single-agent vs 3-agent MAS A/B test on a traction-inverter design benchmark (3–5 specs vs reference designs).

## Milestones

| # | Milestone | State |
|---|-----------|-------|
| M1 | PLECS readback proven (`ToFile`→CSV) | ✅ 2026-07-19 |
| M2 | 2L-B6 CAB450 model runs headless, heat-sink-coupled | ✅ 2026-07-19 |
| M3 | **First validated 2L-B6 η/loss/Tj number** (800 V loaded → corners → CRD calibration) | ⏳ next |
| M4 | Track 1 (2L-B6) complete + registered `validated` | ☐ |
| M5–M7 | Tracks 2–4 (TNPC, ANPC, NPC) complete + registered | ☐ |
| M8 | Synthesis: `circuit-topologies` §5 + `design-tradeoffs` filled with 4 validated models | ☐ |
| M9 | MAS 3-agent core runs a design end-to-end | ☐ |
| M10 | Single-vs-3-agent A/B evaluation | ☐ |

## Definition of "done"

**Per design note / per track** (from `plan-depth-research`):
- Every confirmable-subset claim is **PLECS-backed or primary-cited** (or explicitly bounded/refuted).
- Each `[T]` (training-knowledge) / `[derived]` number is replaced with `[NN]`/sim, or flagged bench-only.
- A runnable PLECS artifact exists **and** its `model_registry.json` entry reads `validation_status: validated` — a number counts as evidence only if its model is registered validated.
- `status` / `evidence` frontmatter updated; **Red Team re-run to residual doubt**; links + frontmatter validate.

**Key architecture decisions** (rationale in [knowledge/README.md](knowledge/README.md) §Key Architecture Decisions): A1 CLI-first · A2 3 agents · A3 PLECS backend (not MATLAB) · A4 SQLite · A5 LiteLLM provider-agnostic · A6 explicit optimizer.
