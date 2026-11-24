#!/usr/bin/env python3
"""Measure a narration track (reference video or our TTS files).

Pure numpy/scipy.  Reads a WAV (any rate, mono or stereo; stereo is averaged).

Measures
  * frame levels (10 ms hop, 30 ms window, dBFS RMS)
  * speech / pause segmentation relative to the noise-or-music floor
    (pause = frames at least `--rel-db` below the speech median for >= `--min-pause` s)
  * pause durations (histogram), speech-run durations
  * F0 by YIN (frame 40 ms, hop 10 ms, 70-400 Hz), per speech run:
      median F0, range in semitones (p10-p90), final movement (last voiced
      250 ms vs run median, semitones), slope of the whole run
  * music / bed check: level and spectral flatness of pause frames, tonal peaks
  * onset / offset sharpness (dB change over the first/last 30 ms of each run)

Usage
  python3 -I audio_measure.py file.wav --out report.json [--rel-db 14 --min-pause 0.12]
"""
import argparse
import json
import wave

import numpy as np


def read_wav(path):
    w = wave.open(path, "rb")
    n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
    raw = w.readframes(n)
    w.close()
    if sw == 2:
        x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768.0
    elif sw == 4:
        x = np.frombuffer(raw, np.int32).astype(np.float64) / 2147483648.0
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
        v = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
        v = np.where(v >= 1 << 23, v - (1 << 24), v)
        x = v.astype(np.float64) / (1 << 23)
    else:
        raise SystemExit(f"unsupported sample width {sw}")
    x = x.reshape(-1, ch)
    return x.mean(axis=1), sr, x


def frame_levels(x, sr, hop=0.010, win=0.030):
    h, wl = int(sr * hop), int(sr * win)
    n = max(1, (len(x) - wl) // h + 1)
    idx = np.arange(wl)[None, :] + h * np.arange(n)[:, None]
    fr = x[idx]
    rms = np.sqrt((fr ** 2).mean(axis=1) + 1e-20)
    return 20 * np.log10(rms + 1e-12), h


def yin_f0(x, sr, hop=0.010, win=0.040, fmin=70.0, fmax=400.0, thr=0.15):
    """Vectorised YIN (difference function via FFT autocorrelation)."""
    # resample-free: work at given sr, but decimate to 16 kHz if higher
    if sr > 16000:
        q = int(round(sr / 16000))
        from scipy.signal import decimate
        x = decimate(x, q, ftype="fir", zero_phase=True)
        sr = sr / q
    h, W = int(sr * hop), int(sr * win)
    tmin, tmax = int(sr / fmax), int(sr / fmin)
    n = max(1, (len(x) - W - tmax) // h)
    f0 = np.zeros(n)
    ap = np.ones(n)
    for start in range(0, n, 2000):
        k = np.arange(start, min(n, start + 2000))
        idx = np.arange(W + tmax)[None, :] + h * k[:, None]
        fr = x[idx]
        a = fr[:, :W]
        # difference d(tau) = sum (a_t - x_{t+tau})^2 for tau in [0, tmax]
        e0 = (a ** 2).sum(axis=1)
        cs = np.cumsum(fr ** 2, axis=1)
        cs = np.concatenate([np.zeros((len(k), 1)), cs], axis=1)
        taus = np.arange(tmax + 1)
        etau = cs[:, taus + W] - cs[:, taus]
        nfft = 1 << int(np.ceil(np.log2(W + tmax + W)))
        Fa = np.fft.rfft(a, nfft, axis=1)
        Ff = np.fft.rfft(fr, nfft, axis=1)
        xc = np.fft.irfft(np.conj(Fa) * Ff, nfft, axis=1)[:, :tmax + 1]
        d = e0[:, None] + etau - 2 * xc
        d[:, 0] = 0
        cmnd = np.ones_like(d)
        c = np.cumsum(d[:, 1:], axis=1)
        cmnd[:, 1:] = d[:, 1:] * np.arange(1, tmax + 1)[None, :] / np.maximum(c, 1e-12)
        sub = cmnd[:, tmin:tmax + 1]
        below = sub < thr
        has = below.any(axis=1)
        first = np.where(has, below.argmax(axis=1), sub.argmin(axis=1))
        # walk to local minimum after first crossing
        for j in range(len(k)):
            i = first[j]
            while i + 1 < sub.shape[1] and sub[j, i + 1] < sub[j, i]:
                i += 1
            first[j] = i
        best = first + tmin
        val = sub[np.arange(len(k)), first]
        # parabolic interpolation
        t = best.astype(float)
        ok = (best > 1) & (best < tmax)
        y0 = cmnd[np.arange(len(k)), np.clip(best - 1, 0, tmax)]
        y1 = cmnd[np.arange(len(k)), best]
        y2 = cmnd[np.arange(len(k)), np.clip(best + 1, 0, tmax)]
        den = (y0 - 2 * y1 + y2)
        shift = np.where(ok & (np.abs(den) > 1e-12), 0.5 * (y0 - y2) / np.where(den == 0, 1, den), 0)
        t = t + np.clip(shift, -1, 1)
        f0[k] = sr / t
        ap[k] = val
    times = (np.arange(n) * h + W / 2) / sr
    return times, f0, ap


def runs(mask):
    d = np.diff(np.concatenate([[0], mask.astype(int), [0]]))
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))


def st(f, ref):
    return 12 * np.log2(f / ref)


def analyse(path, rel_db=14.0, min_pause=0.12, min_speech=0.08, f0_lo=70, f0_hi=400):
    x, sr, xs = read_wav(path)
    dur = len(x) / sr
    lev, h = frame_levels(x, sr)
    hop = h / sr
    tl = np.arange(len(lev)) * hop + 0.015
    speech_med = float(np.percentile(lev, 70))
    floor = float(np.percentile(lev, 3))
    thr = speech_med - rel_db
    quiet = lev < thr
    # pauses: quiet runs >= min_pause
    pauses = [(a, b) for a, b in runs(quiet) if (b - a) * hop >= min_pause]
    pmask = np.zeros(len(lev), bool)
    for a, b in pauses:
        pmask[a:b] = True
    sp_runs = [(a, b) for a, b in runs(~pmask) if (b - a) * hop >= min_speech]
    pause_d = np.array([(b - a) * hop for a, b in pauses])
    run_d = np.array([(b - a) * hop for a, b in sp_runs])
    # F0
    tf, f0, ap = yin_f0(x, sr, fmin=f0_lo, fmax=f0_hi)
    lev_at_f = np.interp(tf, tl, lev)
    voiced = (ap < 0.2) & (lev_at_f > thr + 3) & (f0 > f0_lo) & (f0 < f0_hi)
    fv = f0[voiced]
    gmed = float(np.median(fv)) if len(fv) else float("nan")
    per_run = []
    for a, b in sp_runs:
        t0, t1 = a * hop, b * hop
        m = voiced & (tf >= t0) & (tf < t1)
        if m.sum() < 8:
            continue
        ff = f0[m]
        tt = tf[m]
        med = np.median(ff)
        rng = st(np.percentile(ff, 90), np.percentile(ff, 10))
        last = ff[tt >= tt[-1] - 0.25]
        first = ff[tt <= tt[0] + 0.25]
        fin = st(np.median(last), med)
        ini = st(np.median(first), med)
        slope = np.polyfit(tt - tt[0], st(ff, gmed), 1)[0] if len(ff) > 3 else 0.0
        per_run.append(dict(t0=round(t0, 2), t1=round(t1, 2), dur=round(t1 - t0, 2), f0_med=round(float(med), 1),
                            range_st=round(float(rng), 2), final_st=round(float(fin), 2), initial_st=round(float(ini), 2),
                            slope_st_per_s=round(float(slope), 2)))
    # bed / music check in pause frames
    bed = {}
    if pmask.any():
        bl = lev[pmask]
        bed["pause_level_dbfs_median"] = round(float(np.median(bl)), 1)
        bed["pause_level_dbfs_p10_p90"] = [round(float(np.percentile(bl, 10)), 1), round(float(np.percentile(bl, 90)), 1)]
        # spectrum of pause frames (concatenate up to 60 s)
        segs = []
        tot = 0
        for a, b in pauses:
            s0, s1 = int((a + 3) * h), int((b - 3) * h)
            if s1 - s0 > 2048:
                segs.append(x[s0:s1])
                tot += s1 - s0
            if tot > 60 * sr:
                break
        if segs:
            from scipy.signal import welch
            seg = np.concatenate(segs)
            fr, P = welch(seg, sr, nperseg=8192)
            Pdb = 10 * np.log10(P + 1e-20)
            band = (fr > 60) & (fr < 8000)
            flat = float(np.exp(np.mean(np.log(P[band] + 1e-20))) / (np.mean(P[band]) + 1e-20))
            # tonal peaks: bins >= 12 dB above a 1/3-octave median
            from scipy.ndimage import median_filter
            base = median_filter(Pdb, size=61)
            peaks = fr[(Pdb - base > 12) & band]
            bed["pause_spectral_flatness"] = round(flat, 4)
            bed["pause_tonal_peak_bins"] = int(len(peaks))
            bed["pause_tonal_peaks_hz_sample"] = [round(float(p), 1) for p in peaks[:20]]
            # energy distribution by band
            def bandp(lo, hi):
                m = (fr >= lo) & (fr < hi)
                return float(10 * np.log10(P[m].sum() + 1e-20))
            bed["pause_band_db"] = {f"{lo}-{hi}": round(bandp(lo, hi), 1) for lo, hi in
                                    [(20, 200), (200, 800), (800, 3000), (3000, 8000), (8000, 16000)]}
    # stereo difference (side signal level) - music beds are often stereo
    if xs.shape[1] == 2:
        side = (xs[:, 0] - xs[:, 1]) / 2
        mid = (xs[:, 0] + xs[:, 1]) / 2
        sl, _ = frame_levels(side, sr)
        ml, _ = frame_levels(mid, sr)
        bed["side_minus_mid_db_speech"] = round(float(np.median(sl[~pmask] - ml[~pmask])), 1) if (~pmask).any() else None
        bed["side_minus_mid_db_pause"] = round(float(np.median(sl[pmask] - ml[pmask])), 1) if pmask.any() else None
        bed["side_level_dbfs_pause_median"] = round(float(np.median(sl[pmask])), 1) if pmask.any() else None
    # onset / offset sharpness
    on, off = [], []
    for a, b in sp_runs:
        if a >= 3:
            on.append(float(lev[min(a + 3, len(lev) - 1)] - lev[a - 3]))
        if b + 3 < len(lev):
            off.append(float(lev[b - 3] - lev[b + 3]))
    rep = dict(file=path, duration_s=round(dur, 2), sr=sr,
               level=dict(speech_ref_p70_dbfs=round(speech_med, 1), floor_p3_dbfs=round(floor, 1),
                          pause_threshold_dbfs=round(thr, 1)),
               pauses=dict(n=int(len(pause_d)), total_s=round(float(pause_d.sum()), 2),
                           median=round(float(np.median(pause_d)), 3) if len(pause_d) else None,
                           mean=round(float(pause_d.mean()), 3) if len(pause_d) else None,
                           p10=round(float(np.percentile(pause_d, 10)), 3) if len(pause_d) else None,
                           p90=round(float(np.percentile(pause_d, 90)), 3) if len(pause_d) else None,
                           cv=round(float(pause_d.std() / pause_d.mean()), 3) if len(pause_d) else None,
                           hist_edges=[0.12, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0, 5.0],
                           hist=np.histogram(pause_d, [0.12, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0, 5.0])[0].tolist(),
                           list=[(round(a * hop, 2), round((b - a) * hop, 3)) for a, b in pauses]),
               speech_runs=dict(n=int(len(run_d)), total_s=round(float(run_d.sum()), 2),
                                median=round(float(np.median(run_d)), 3) if len(run_d) else None,
                                p10=round(float(np.percentile(run_d, 10)), 3) if len(run_d) else None,
                                p90=round(float(np.percentile(run_d, 90)), 3) if len(run_d) else None),
               f0=dict(voiced_frames=int(voiced.sum()), median_hz=round(gmed, 1),
                       p5_hz=round(float(np.percentile(fv, 5)), 1) if len(fv) else None,
                       p95_hz=round(float(np.percentile(fv, 95)), 1) if len(fv) else None,
                       range_p5_p95_st=round(float(st(np.percentile(fv, 95), np.percentile(fv, 5))), 2) if len(fv) else None,
                       per_run=per_run),
               bed=bed,
               edges=dict(onset_rise_db_median=round(float(np.median(on)), 1) if on else None,
                          offset_fall_db_median=round(float(np.median(off)), 1) if off else None))
    return rep, (tl, lev, tf, f0, voiced, pmask)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--out", required=True)
    ap.add_argument("--rel-db", type=float, default=14.0)
    ap.add_argument("--min-pause", type=float, default=0.12)
    ap.add_argument("--npz", default=None, help="also save frame arrays")
    a = ap.parse_args()
    rep, arrs = analyse(a.wav, a.rel_db, a.min_pause)
    json.dump(rep, open(a.out, "w"), ensure_ascii=False, indent=1)
    if a.npz:
        tl, lev, tf, f0, voiced, pmask = arrs
        np.savez_compressed(a.npz, tl=tl, lev=lev, tf=tf, f0=f0, voiced=voiced, pmask=pmask)
    p = rep["pauses"]
    print(f"dur {rep['duration_s']} s | speech ref {rep['level']['speech_ref_p70_dbfs']} dBFS | floor {rep['level']['floor_p3_dbfs']}")
    print(f"pauses n={p['n']} median {p['median']} p10 {p['p10']} p90 {p['p90']} cv {p['cv']} hist {p['hist']}")
    print(f"speech runs n={rep['speech_runs']['n']} median {rep['speech_runs']['median']}")
    print(f"F0 median {rep['f0']['median_hz']} Hz p5-p95 {rep['f0']['p5_hz']}-{rep['f0']['p95_hz']} ({rep['f0']['range_p5_p95_st']} st)")
    print("bed", rep["bed"])
    print("edges", rep["edges"])


if __name__ == "__main__":
    main()
