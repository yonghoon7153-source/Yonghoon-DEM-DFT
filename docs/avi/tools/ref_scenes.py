#!/usr/bin/env python3
"""Scene / animation-event / caption-segment analysis from framestats.npz.

Writes a JSON with:
  caption_segments: [{i, f0, f1, t0, t1, dur, has_box}]
  content_events:   [{f0, f1, dur_s, net_frac, add_frac, rem_frac, kind}]
  scenes:           [{f0, f1, t0, t1, dur}]  (boundaries = events that remove
                     a large part of the previous composition)
Usage: python3 -I ref_scenes.py framestats.npz --out scenes.json
"""
import argparse
import json

import numpy as np


def group(idx, gap=2):
    groups = []
    for i in idx:
        if groups and i - groups[-1][-1] <= gap:
            groups[-1].append(int(i))
        else:
            groups.append([int(i)])
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stats")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--cap-thr", type=float, default=2.0)
    ap.add_argument("--evt-thr", type=float, default=0.15)
    a = ap.parse_args()
    z = np.load(a.stats)
    dc, dk, th = z["d_content"], z["d_caption"], z["thumbs"].astype(np.int16)
    n = len(dc)
    fps = a.fps
    # ---- caption presence: dark box rows 47..50 of the 54-row thumb, centre cols
    capL = th[:, 47:51, 36:60].mean(axis=(1, 2))
    has_box = capL < 170
    # ---- caption segments between hard caption changes
    ev = group(np.where(dk > a.cap_thr)[0], gap=1)
    cuts = [g[0] for g in ev]
    bounds = [0] + cuts + [n]
    segs = []
    for k in range(len(bounds) - 1):
        f0, f1 = bounds[k], bounds[k + 1] - 1
        if f1 < f0:
            continue
        hb = bool(has_box[f0:f1 + 1].mean() > 0.5)
        segs.append(dict(i=len(segs), f0=int(f0), f1=int(f1), t0=round(f0 / fps, 3),
                         t1=round((f1 + 1) / fps, 3), dur=round((f1 - f0 + 1) / fps, 3), has_box=hb))
    # ---- content events
    cev = group(np.where(dc > a.evt_thr)[0], gap=3)
    bgL = np.median(th[:, :40, :].reshape(n, -1), axis=1)  # background level per frame
    events = []
    for g in cev:
        f0, f1 = g[0], g[-1]
        pre = th[max(f0 - 2, 0), :43]
        post = th[min(f1 + 2, n - 1), :43]
        b = float(np.median(pre))
        d = post - pre
        changed = np.abs(d) > 12
        net = float(changed.mean())
        # addition: pre ~ background, post darker/coloured; removal: the reverse
        pre_bg = np.abs(pre - b) < 8
        post_bg = np.abs(post - b) < 8
        add = float((changed & pre_bg & ~post_bg).mean())
        rem = float((changed & ~pre_bg & post_bg).mean())
        prev_fg = float((~pre_bg).mean())
        rem_share = rem / prev_fg if prev_fg > 0 else 0.0
        kind = "build"
        if rem_share > 0.5 and add > 0.002:
            kind = "scene_change"
        elif rem_share > 0.5:
            kind = "clear"
        elif rem > add and rem > 0.002:
            kind = "remove"
        elif net < 0.002:
            kind = "subtle"
        events.append(dict(f0=int(f0), f1=int(f1), t0=round(f0 / fps, 3), dur_s=round((f1 - f0 + 1) / fps, 3),
                           net_frac=round(net, 4), add_frac=round(add, 4), rem_frac=round(rem, 4),
                           rem_share_prev=round(rem_share, 3), peak=round(float(dc[f0:f1 + 1].max()), 3), kind=kind))
    # ---- scenes = split at scene_change / clear events
    sb = [0] + [e["f0"] for e in events if e["kind"] in ("scene_change", "clear")] + [n]
    scenes = []
    for k in range(len(sb) - 1):
        f0, f1 = sb[k], sb[k + 1] - 1
        if f1 - f0 < 3:
            continue
        nev = sum(1 for e in events if f0 <= e["f0"] <= f1 and e["kind"] in ("build", "remove", "subtle"))
        scenes.append(dict(i=len(scenes), f0=int(f0), f1=int(f1), t0=round(f0 / fps, 3), t1=round((f1 + 1) / fps, 3),
                           dur=round((f1 - f0 + 1) / fps, 3), n_builds=int(nev)))
    out = dict(n_frames=int(n), fps=fps, caption_segments=segs, content_events=events, scenes=scenes)
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=1)
    cs = [s for s in segs if s["has_box"]]
    durs = np.array([s["dur"] for s in cs])
    print("caption segments with box:", len(cs), "dur median %.2f mean %.2f p10 %.2f p90 %.2f" %
          (np.median(durs), durs.mean(), np.percentile(durs, 10), np.percentile(durs, 90)))
    gaps = [s for s in segs if not s["has_box"]]
    print("no-box segments:", len(gaps), [(s["t0"], s["dur"]) for s in gaps][:20])
    kinds = {}
    for e in events:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    print("content events:", len(events), kinds)
    sd = np.array([s["dur"] for s in scenes])
    print("scenes:", len(scenes), "dur median %.2f mean %.2f p10 %.2f p90 %.2f max %.2f" %
          (np.median(sd), sd.mean(), np.percentile(sd, 10), np.percentile(sd, 90), sd.max()))


if __name__ == "__main__":
    main()
