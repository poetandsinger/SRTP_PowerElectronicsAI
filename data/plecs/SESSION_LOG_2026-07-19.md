# Session log — PLECS harness + Track-1 loss layer (2026-07-19)

A critical, honest retrospective of a long autonomous session driving the
[`plan-depth-research`](../../srtp_docs/plans/plan-depth-research.md) PLECS-first program.
Written at the user's request. Includes the testing methodology used throughout.

---

## 1. Executive summary

**Goal for the session:** advance the PLECS-first depth-research plan — turn `unverified`
traction-inverter notes into PLECS-backed evidence, starting with the harness and Track 1
(2L-B6 SiC, calibrated to the Wolfspeed/TI 300 kW CRD).

**What actually got done (committed on branch `plecs-harness-readback-wolfspeed-models`):**
1. **Cleared the program's #1 blocker — PLECS readback.** `plecs.simulate` returns empty
   `Values` in this 4.8 build; the working path is a `ToFile`→CSV read from disk. Proven on a
   toy model and the real 2L-VSI+PMSM model.
2. **Built a reusable harness** (`data/plecs/`): template, direct-RPC runner, numpy summarizer
   (THD unit-tested), `model_registry.json`, READMEs.
3. **Corrected the vault** where it documented the wrong (Outport) readback as "verified", plus
   the datasheet capture and citations [166]–[170].
4. **Organized the full Wolfspeed PLECS model library** (669 models) under `plecs_models/wolfspeed/`;
   confirmed the official CAB450M12XM3 model loads + runs.
5. **Built a from-scratch discrete double-pulse test** that runs fully headless and captures the
   correct 509 A current ramp.

**What did NOT get done:** a single validated loss/efficiency/Tj number. The DPT's **loss readout
reads 0** and I have not cracked why. So Track 1 has **zero PLECS evidence** produced — the design
notes are still `unverified`. The harness and the discrete-model path are proven; the evidence isn't.

**Biggest mistake:** I twice concluded a "hard boundary" (first "loss readout impossible on the
library block", then "device-on-heatsink coupling needs the GUI") that were **premature** — the
second was outright wrong, caused by a `.plecs` `Frame` syntax bug I didn't diagnose. The user's
screenshot of the actual PLECS error corrected me. I committed the wrong conclusion before that.

---

## 2. What I did, and why (chronological)

**Phase A — Readback blocker.** The plan named "prove `simulate` returns `Values`" as the gate.
I reproduced the empty-`Values` behavior, then read PE-MAS's own `plecs_interface.py` and found
they parse a `ToFile` CSV (treating `res['Values']` as an unreliable bonus). I proved ToFile→CSV
on a minimal sine model and the real switched model. *Why:* this unblocks all downstream evidence;
without it nothing counts.

**Phase B — Harness + registry.** Packaged the proven method into a template + `run_harness.py`
(direct XML-RPC) + `summarize.py` + `model_registry.json`. *Why:* the plan calls for a registry
and reusable harness; and a hard-won method stranded in scratch is worthless.

**Phase C — Vault correction.** The SOP and plans asserted the Outport readback as "verified
2026-07-18". I corrected them + memories + changelog. *Why:* the vault's integrity rule — a
documented falsehood is worse than a gap.

**Phase D — Datasheet + Wolfspeed models.** Dispatched a subagent for the CAB450M12XM3 datasheet
(cited brief, [166]–[170]). The user then supplied the full Wolfspeed PLECS library; I reorganized
it space-free under `plecs_models/wolfspeed/` and confirmed the official CAB450 model (full 800 V
loss surface + Cauer net) loads and runs. *Why:* the official model removes any need to hand-build
loss tables (which would risk fabrication).

**Phase E — Discrete loss model (the hard part).** Established CAB450 needs a `MosfetWithDiode`
block, built a from-scratch double-pulse test, and — after the user's screenshot exposed a `Frame`
syntax bug — got it running headless with correct current. Loss readout still 0. *Why:* the user
chose the full-validation (discrete-switch) path; the DPT (SOP corner 1) is the smallest circuit
that validates CAB450's switching loss.

---

## 3. Testing methodology

The method that worked, and the discipline behind it.

### 3.1 Prove the mechanism on the smallest possible model first
Before building anything real, isolate each unknown in a minimal artifact:
- Readback: a `SineGenerator→Output` model (does `simulate` return `Values`? no) → a
  `SineGenerator→ToFile` model (does the CSV write? yes). Only then apply to the real model.
- Loss model: assign the device XML to one block and *just simulate* (does it load? does it error?)
  before wiring any measurement.

This localizes failures to one variable. It's why I could state each finding crisply.

### 3.2 Change one thing per run; read the actual error text
Every PLECS error string was treated as data and acted on literally:
`"place the component on an active heat sink"`, `"Gate dependent conduction losses are not
supported"`, `"syntax error before 'Frame'"`, `"Width ... does not match"`. Each named the next
fix. **The failure below (§4.1) is where I violated this — I inferred a boundary instead of reading
the error PLECS was actually about to give in the GUI.**

### 3.3 The edit→close→open→simulate→read-CSV loop
The stable RPC loop, with two traps baked in:
- **Stale model:** after any `.plecs` text edit, `close_model` then `open_model` (re-loading an
  open model keeps the old graph). Verify a new block landed with `get_component_param` before sim.
- **Sim duration:** set the model `TimeSpan` (the `simulate` `stop_time` arg is ignored).
Read results by pointing a `ToFile` at an absolute path and parsing with `np.genfromtxt` (no header
row is written). Runtime params (`Filename`, device `thermal`, `Rth`) injected via
`set_component_param` so the template stays path-free.

### 3.4 Cross-check numbers against an independent expectation
- Summarizer THD: fed a synthetic fundamental + known 5th/7th harmonic; asserted the computed THD
  matched the injected value (0.0894) before trusting it on real data.
- DPT current: `di/dt = Vdc/L = 6 A/µs` predicts ~450 A at 75 µs; the sim's 509 A peak matched the
  expected ramp, confirming the electrical circuit was correct.
- Loss (attempted): the datasheet's tabulated `Eon 25.4 / Eoff 7.51 mJ @600 V,450 A,25 °C` is the
  target the DPT must reproduce (not yet reached).

### 3.5 Learn `.plecs` syntax by extraction, not invention
Every block/connection form was copied from a shipped demo (buck-thermal, DAB, PV inverter) via
`awk`/Python block extraction, never guessed. Terminal indices were read from real connections
(`Mosfet`: 1=drain, 2=source, 3=gate; `Ammeter`: 1,2 power / 3 signal; `HeatFlowMeter`: 1,2 thermal
/ 3 signal). Signal names likewise (`"MOSFET conduction loss"`, `"MOSFET junction temp"`). **The one
form I got wrong — `Frame` position — I had *placed by my generator's convention* rather than
matched to a demo's ordering. That single deviation caused the worst failure of the session.**

### 3.6 Build from scratch on an empty canvas to avoid geometry couplings
Retargeting a complex demo failed three ways (coordinate collisions, block-class rejection,
probe-width couplings). A from-scratch model on an empty canvas removes all inherited geometry and
wiring, leaving only terminal-index correctness — far more reliable headless.

---

## 4. Problems encountered (critical)

### 4.1 The `Frame` bug and my wrong "GUI-only" conclusion — the worst failure
I concluded, committed, and documented that device-on-heatsink coupling *cannot be scripted and
needs the GUI*. **This was false.** The real cause was a syntax bug: my generator wrote `Frame`
after the `Parameter` blocks; PLECS needs it right after `LabelPosition`, and silently *removed the
HeatSink* on load — so the device genuinely had no heat sink, giving the "active heat sink" error.

Why this is a serious methodology failure:
- I "tested exhaustively" (huge frame, explicit terminal) but all my tests shared the **same latent
  syntax bug**, so they all failed for the same hidden reason — a classic confirmation trap.
- `plecs.load` returned `ok:true` even while *removing* the malformed component. I trusted `ok:true`
  as "the model is as I wrote it." **The RPC load is lenient; it does not guarantee the graph
  matches the file.** I should have verified the HS existed post-load (`get_component_param
  harness/HS ...`) — the same check I *did* use for the stale-model trap, but failed to apply here.
- I let a **negative** result (can't do X) become a **committed conclusion** without the same rigor
  I'd demand for a positive result. Negative claims need *more* scrutiny, not less.
- It took the user opening the file in the GUI — which shows the parse error the RPC hid — to
  surface it. I had the same information available headless (I could have opened the file in the GUI
  via the running PLECS, or checked component existence post-load) and didn't.

### 4.2 The loss readout = 0 — still unresolved
The device conducts 450 A, but every loss readout reads 0:
- `SwitchLossCalculator` with empty `Signals{}` (copied from the working buck demo) → 0.
- `PlecsProbe` with explicit loss/temp signal names → **writes no CSV at all** (the switching-loss
  signal is a Dirac impulse a `ToFile` apparently won't serialize; dropping to conduction+Tj still
  won't write).
- `HeatFlowMeter` in the HS→ambient path → 0 W total.
I have hypotheses (loss not reaching the measured thermal path; probe signal-sets needing GUI
config; the empty-`Signals{}` on the SLC meaning "sum nothing" in scripted mode) but no confirmed
root cause. **This is the single blocker between a running model and a real number.** I did not
solve it, and I burned ~15 tool-calls circling it before regenerating a clean model.

### 4.3 Over-editing a single file into an inconsistent state
While chasing the loss readout I made many incremental edits to one `.plecs`; at one point the
current-capture (which had worked) stopped writing. I couldn't cleanly attribute it. The fix was to
**stop patching and regenerate the whole model from a single script** — which restored a coherent
state (current 509 A, loss 0). Lesson: past ~3 incremental structural edits, regenerate rather than
patch.

### 4.4 Time discipline
I spent a very large number of tool-calls, some on low-yield trial-and-error (the loss readout, the
retarget attempts). A tighter rule — "after N failed attempts on one mechanism, stop and change
strategy or surface the blocker" — would have saved effort. I did eventually surface blockers to
the user, but later than ideal.

---

## 5. What I did NOT do (and why)

- **No validated PLECS numbers.** The whole point of the plan (η/loss/Tj as evidence) is not
  achieved — blocked on §4.2. Every design note remains `unverified`. This is the honest headline.
- **No full 2L-B6 bridge, no 9-corner matrix, no S5 Wolfspeed calibration.** All gated on getting
  one loss number out of the DPT first.
- **No agnostic-note validation** (machine-and-load, circuit-components, etc.) — the plan's shared
  layer beyond the harness. Deferred behind Track 1.
- **Did not fabricate anything.** Where I lacked data (datasheet loss tables, a loss number) I said
  so rather than inventing plausible values — consistent with the SOP's integrity bar.
- **Did not commit to `main`.** Branched (`plecs-harness-readback-wolfspeed-models`); the user
  commits/merges.

---

## 6. Current state & concrete next steps

**Proven and committed:** ToFile readback; reusable harness; Wolfspeed library organized; official
CAB450 model loads+runs; from-scratch discrete DPT runs headless with correct current; corrected
vault + docs.

**The one thing to crack next:** the loss readout. Concrete things to try (in order):
1. Open `dpt_cab450_600v.plecs` in the GUI, add a `SwitchLossCalculator`, and in its dialog
   **select the loss signals explicitly** (the empty `Signals{}` is the prime suspect); save; then
   the sim + read is headless. This tests whether the SLC signal-set is the issue.
2. Check the device is actually dissipating: in the GUI, probe `Slow`'s "MOSFET conduction loss"
   on a scope during the 450 A conduction window — is it non-zero? If yes, the problem is my
   *measurement path*; if no, it's the *device/loss-model config*.
3. Verify the loss reaches the heat sink: confirm `Tj` rises with a non-zero device `Rth`.
Once one real Eon/Eoff/conduction number validates against the datasheet, replicate the leg ×3 →
2L-B6 bridge → corner matrix → CRD calibration → fill `design-2l-b6-800v-sic` → registry
`validated`.

**Meta-lesson for next time:** verify the loaded graph matches the file after every structural edit
(`ok:true` from `load` is not enough); hold negative/"impossible" conclusions to a higher bar than
positive ones; regenerate rather than patch after a few edits; and timebox single-mechanism
debugging before changing strategy or surfacing the blocker.
