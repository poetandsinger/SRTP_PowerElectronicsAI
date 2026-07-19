# `<model>_plecs/` — PLECS thermal-description search folder

PLECS resolves a switch's `file:<Name>` thermal description from this
`<modelbasename>_plecs/` sibling folder (auto-added to the search path at load).
Placing the XML next to the `.plecs` is NOT enough.

For the 2L-B6 SiC build, drop **`CAB450M12XM3.xml`** here (official Wolfspeed PLECS
model [167], or hand-built per `../../LOSS_LAYER_BUILD.md` from datasheet [166]), then
set the converter's `therm` param to `file:CAB450M12XM3`.

(Verified 2026-07-19 with the shipped Wolfspeed `C3M0030090K` demo XML — the IGBT
converter block accepts a MOSFET description and simulates. That demo file is Plexim's
and is not committed here.)
