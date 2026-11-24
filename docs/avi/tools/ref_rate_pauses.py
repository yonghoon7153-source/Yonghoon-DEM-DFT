#!/usr/bin/env python3
"""Join caption timing (frames) + caption text (read from frames) + audio frames.

For each caption window [t0, t1): spoken syllables, speech time (non-pause
frames), rate; and the pause at the caption boundary, classified by the
caption's ending (sentence-final vs clause-internal).

Usage: python3 -I ref_rate_pauses.py capmids.json captions_read.txt ref_frames.npz --out rate.json
"""
import argparse
import json
import re
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__file__))
from korean_text import syllables  # noqa: E402

FINAL = re.compile(r"(다|요|죠|까|냐|\?|니다|네요|군요)\s*[.?!]?$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("capmeta")
    ap.add_argument("captext")
    ap.add_argument("frames")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    meta = json.load(open(a.capmeta))
    txt = {}
    for line in open(a.captext, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        i, t = line.split("\t", 1)
        txt[int(i)] = t
    z = np.load(a.frames)
    tl, pmask, tf, f0, voiced = z["tl"], z["pmask"], z["tf"], z["f0"], z["voiced"]
    hop = float(tl[1] - tl[0])
    rows = []
    for k, m in enumerate(meta):
        t = txt.get(k, "")
        t0, t1 = m["t0"], m["t1"]
        sel = (tl >= t0) & (tl < t1)
        sp = float((~pmask[sel]).sum() * hop)
        syl = syllables(t)
        # pause around the boundary at t1 (search +-0.35 s)
        b = (tl >= t1 - 0.35) & (tl < t1 + 0.35)
        idx = np.where(b)[0]
        pause = 0.0
        if len(idx):
            pm = pmask[idx]
            # longest pause run touching the window
            best, cur = 0, 0
            for v in pm:
                cur = cur + 1 if v else 0
                best = max(best, cur)
            # extend that run fully
            pause = best * hop
        # full pause run length containing the nearest pause frame to t1
        near = None
        if pmask[b].any():
            j = idx[pmask[idx]][np.argmin(np.abs(tl[idx[pmask[idx]]] - t1))]
            s0 = j
            while s0 > 0 and pmask[s0 - 1]:
                s0 -= 1
            s1 = j
            while s1 + 1 < len(pmask) and pmask[s1 + 1]:
                s1 += 1
            near = (s1 - s0 + 1) * hop
        kind = "final" if FINAL.search(t) else "clause"
        if t.endswith("?"):
            kind = "question"
        # final F0 movement within this caption (last 250 ms voiced vs caption median)
        fm = (tf >= t0) & (tf < t1) & voiced
        fin = None
        if fm.sum() > 10:
            ff, tt = f0[fm], tf[fm]
            med = np.median(ff)
            last = ff[tt >= tt[-1] - 0.25]
            fin = float(12 * np.log2(np.median(last) / med))
        rows.append(dict(i=k, t0=t0, t1=t1, text=t, syl=syl, speech_s=round(sp, 3),
                         rate=round(syl / sp, 2) if sp > 0.2 else None, pause_after=round(near, 3) if near else 0.0,
                         kind=kind, final_f0_st=round(fin, 2) if fin is not None else None))
    out = dict(rows=rows)
    R = np.array([r["rate"] for r in rows if r["rate"]])
    syl_tot = sum(r["syl"] for r in rows)
    sp_tot = sum(r["speech_s"] for r in rows)
    span = meta[-1]["t1"] - meta[0]["t0"]
    out["summary"] = dict(captions=len(rows), syllables=syl_tot, speech_s=round(sp_tot, 1), span_s=round(span, 1),
                          articulation_rate=round(syl_tot / sp_tot, 2), speaking_rate_incl_pauses=round(syl_tot / span, 2),
                          caption_rate_median=round(float(np.median(R)), 2), caption_rate_p10=round(float(np.percentile(R, 10)), 2),
                          caption_rate_p90=round(float(np.percentile(R, 90)), 2), caption_rate_cv=round(float(R.std() / R.mean()), 3),
                          syl_per_caption_median=float(np.median([r["syl"] for r in rows])),
                          chars_per_caption_median=float(np.median([len(r["text"]) for r in rows])),
                          chars_per_caption_p10_p90=[float(np.percentile([len(r["text"]) for r in rows], q)) for q in (10, 90)])
    for kind in ("final", "question", "clause"):
        p = np.array([r["pause_after"] for r in rows if r["kind"] == kind])
        f = np.array([r["final_f0_st"] for r in rows if r["kind"] == kind and r["final_f0_st"] is not None])
        if len(p):
            out["summary"][f"pause_after_{kind}"] = dict(n=int(len(p)), median=round(float(np.median(p)), 3),
                                                         p10=round(float(np.percentile(p, 10)), 3),
                                                         p90=round(float(np.percentile(p, 90)), 3),
                                                         zero_frac=round(float((p == 0).mean()), 3))
        if len(f):
            out["summary"][f"final_f0_{kind}"] = dict(median_st=round(float(np.median(f)), 2),
                                                      p10=round(float(np.percentile(f, 10)), 2),
                                                      p90=round(float(np.percentile(f, 90)), 2),
                                                      sd=round(float(f.std()), 2))
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out["summary"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
