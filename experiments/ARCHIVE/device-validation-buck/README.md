# Buck + CAB450 — proof the retarget-a-GUI-base method works

`buck_cab450_ref.plecs` is the shipped `buck_converter_with_thermal_model` demo with its `Igbt`
**text-swapped in place** to a `MosfetWithDiode` carrying `file:CAB450M12XM3` (Ron=3.6 mΩ, Rgon=4/
Rgoff=0), plus a `PlecsProbe`("Device conduction loss","Device junction temp")→`myCap` ToFile.

**Why it matters:** the demo is **GUI-saved**, so its device→heat-sink coupling is baked in. The
swap is pure text, and the coupling **survives** — CAB450 then reports **35.7 W conduction loss with
a bounded Tj** (max ~19.5 °C over the 50 ms run). This proves two things:

1. CAB450's loss model reads correctly on a working coupling (the device model is sound).
2. The reliable build method for T1–T4: **retarget a GUI-saved base** rather than author on-heat-sink
   devices from scratch (which does not couple — see `../HANDOFF.md`).

It is a buck (step-down), not the target inverter operating point, so it does **not** by itself
validate Eon/Eoff at 600 V/450 A — it validates the *method* and that the loss tables evaluate.
