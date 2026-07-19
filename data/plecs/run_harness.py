"""Direct-RPC runner for the PLECS traction-inverter harness.

Drives PLECS 4.8 over XML-RPC (PLECS.exe -server 1080) without the MCP layer, so
the harness is usable from plain Python. Implements the verified workflow:

    close -> load -> set params (incl. ToFile Filename) -> simulate -> read CSV

Readback contract (verified 2026-07-19): plecs.simulate returns EMPTY Values in
this build; the ToFile block writes the CSV we actually read. After editing a
.plecs on disk you MUST close before re-loading (re-loading an open model is
stale). Sim duration is set by the model TimeSpan param, NOT the simulate arg.

Usage:
    python run_harness.py <model.plecs> <out.csv> [labels] [--timespan 0.2]
"""
import os
import sys
import xmlrpc.client

RPC_URL = os.environ.get("PLECS_RPC_URL", "http://localhost:1080")


def connect():
    return xmlrpc.client.ServerProxy(RPC_URL, allow_none=True)


def run(model_path, csv_path, tofile_block="cap_iabc", timespan=None,
        params=None, model_vars=None):
    """Load model_path, point its ToFile block at csv_path, simulate, return csv_path."""
    server = connect()
    name = os.path.splitext(os.path.basename(model_path))[0]
    # stale-model trap: close any prior instance of this name before loading
    try:
        server.plecs.close(name)
    except Exception:
        pass
    server.plecs.load(os.path.abspath(model_path))
    # point the ToFile block at an absolute CSV path (runtime injection)
    server.plecs.set(f"{name}/{tofile_block}", "Filename", os.path.abspath(csv_path))
    if timespan is not None:
        server.plecs.set(name, "TimeSpan", str(timespan))
    for comp_param, value in (params or {}).items():
        comp, param = comp_param.rsplit("/", 1)
        server.plecs.set(f"{name}/{comp}", param, str(value))
    if os.path.exists(csv_path):
        os.remove(csv_path)
    opts = {"ModelVars": model_vars} if model_vars else {}
    server.plecs.simulate(name, opts)   # Values ignored — read the CSV instead
    if not (os.path.exists(csv_path) and os.path.getsize(csv_path) > 0):
        raise RuntimeError(
            f"No CSV at {csv_path}. Check the ToFile block name ('{tofile_block}') "
            f"and that the model actually ran (see PLECS console)."
        )
    return csv_path


if __name__ == "__main__":
    import argparse
    from summarize import summarize
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("csv")
    ap.add_argument("labels", nargs="?", default=None)
    ap.add_argument("--block", default="cap_iabc")
    ap.add_argument("--timespan", default=None)
    a = ap.parse_args()
    run(a.model, a.csv, tofile_block=a.block, timespan=a.timespan)
    import json
    labels = a.labels.split(",") if a.labels else None
    print(json.dumps(summarize(a.csv, labels), indent=2))
