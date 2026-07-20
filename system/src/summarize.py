"""PLECS ToFile-CSV summarizer for the traction-inverter harness.

Readback contract (PLECS 4.8, verified 2026-07-19): plecs.simulate returns an
empty Values array; the reliable path is a ToFile block writing a CSV to disk,
read here with numpy. CSV layout: col 0 = Time, cols 1..N = the muxed signals in
mux order. No header row is written despite WriteSignalNames=1.

This computes steady-state RMS + current THD over an integer number of
fundamental periods (SOP S2). It does NOT compute efficiency/Tj unless the model
carries a datasheet loss/thermal description (the next harness layer).
"""
import sys
import numpy as np


def load_csv(path):
    d = np.genfromtxt(path, delimiter=",")
    if d.ndim == 1:
        d = d.reshape(1, -1)
    if np.isnan(d[0, 0]):          # tolerate a stray header/NaN first row
        d = d[1:]
    return d[:, 0], d[:, 1:]


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)))


def dominant_freq(t, x):
    """Fundamental frequency of x via FFT on a uniform resample."""
    n = len(t)
    tu = np.linspace(t[0], t[-1], n)
    xu = np.interp(tu, t, x - np.mean(x))
    fft = np.abs(np.rfft(xu)) if hasattr(np, "rfft") else np.abs(np.fft.rfft(xu))
    freqs = np.fft.rfftfreq(n, d=(tu[-1] - tu[0]) / (n - 1))
    k = 1 + int(np.argmax(fft[1:]))
    return float(freqs[k])


def thd_current(t, x, f0=None, nharm=40):
    """THD of a current waveform over the last whole fundamental periods."""
    if f0 is None:
        f0 = dominant_freq(t, x)
    if f0 <= 0:
        return float("nan"), float("nan")
    T = 1.0 / f0
    tend = t[-1]
    nper = int((tend - t[0]) / T)
    if nper < 1:
        return float("nan"), f0
    tstart = tend - nper * T
    m = t >= tstart
    tw, xw = t[m], x[m]
    N = 4096
    tu = np.linspace(tstart, tend, N, endpoint=False)
    xu = np.interp(tu, tw, xw)
    fft = np.fft.rfft(xu * np.hanning(N))
    mag = np.abs(fft)
    # fundamental bin ~ nper (nper periods in the window)
    fund_bin = nper
    if fund_bin >= len(mag):
        return float("nan"), f0
    fund = mag[fund_bin]
    harm = np.sqrt(np.sum(mag[2 * fund_bin::fund_bin][:nharm] ** 2)) if fund_bin else 0.0
    thd = float(harm / fund) if fund > 0 else float("nan")
    return thd, f0


def summarize(path, labels=None):
    t, sig = load_csv(path)
    ncol = sig.shape[1]
    labels = labels or [f"col{j+1}" for j in range(ncol)]
    ss = t >= t[0] + 0.5 * (t[-1] - t[0])   # last 50% as steady-state proxy
    out = {"file": path, "n_rows": len(t), "t_span": [float(t[0]), float(t[-1])]}
    metrics = {}
    for j in range(ncol):
        x = sig[:, j]
        rec = {"rms_ss": rms(x[ss]), "peak": float(x.max()), "min": float(x.min())}
        if labels[j].lower().startswith(("i", "cur")):
            thd, f0 = thd_current(t, x)
            rec["thd"] = thd
            rec["f0_hz"] = f0
        metrics[labels[j]] = rec
    out["metrics"] = metrics
    return out


if __name__ == "__main__":
    import json
    path = sys.argv[1]
    labels = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    print(json.dumps(summarize(path, labels), indent=2))
