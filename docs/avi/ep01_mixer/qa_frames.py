#!/usr/bin/env python3
"""Dense frame check for a rendered preview (SKILL §8): extract frames, build contact sheets, run automatic checks.

  python3 -I qa_frames.py VIDEO SCENES_JSON OUT_DIR --fps 0.5 [--t0 A --t1 B] [--tiles 4x4 --tile-w 480]
          [--strip T1,T2,...]   (10 fps filmstrips of ±1 s around each time)  [--corner-tag]  (internal clip)

Automatic checks (frames at --fps, content area = above the caption band):
  ① same picture > 5 s (content area unchanged)   ② one-frame flicker (i-1 == i+1 != i)
  ③ caption box over non-background content        ④ ink inside edge bands (left/right 10 %, top 8 %)
  ⑤ blank screen ≥ 1 s (content ink < 0.15 %) · speech running or pause      --timing = real narration timeline
Writes OUT_DIR/report.json and OUT_DIR/sheet_XX.jpg.  ffmpeg runs with -threads 2 (caller uses nice -n 19).
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

TOOLS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools")
sys.path.insert(0, TOOLS)
import avi_style as S  # noqa: E402
import avi_timeline as T  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("scenes")
ap.add_argument("out")
ap.add_argument("--fps", type=float, default=2.0)
ap.add_argument("--t0", type=float, default=0.0)
ap.add_argument("--t1", type=float, default=None)
ap.add_argument("--tiles", default="4x4")
ap.add_argument("--tile-w", type=int, default=480)
ap.add_argument("--strip", default="")
ap.add_argument("--corner-tag", action="store_true", help="ignore the internal corner tag box in edge checks")
ap.add_argument("--timing", help="audio/timing.json of the real narration (final render) — labels use the real timeline")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
fdir = os.path.join(a.out, "frames")
os.makedirs(fdir, exist_ok=True)
for fn in os.listdir(fdir):
    os.remove(os.path.join(fdir, fn))
dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", a.video],
                                      capture_output=True, text=True).stdout)["format"]["duration"])
t1 = a.t1 if a.t1 is not None else dur
cmd = ["ffmpeg", "-v", "error", "-threads", "2", "-y", "-ss", f"{a.t0:.3f}", "-to", f"{t1:.3f}", "-i", a.video,
       "-vf", f"fps={a.fps},scale=640:-1", os.path.join(fdir, "f_%05d.png")]
subprocess.run(cmd, check=True)
files = sorted(os.listdir(fdir))
# ffmpeg fps filter (round=near): output frame k (0-based) shows the video at t0 + (k + 0.5)/fps
# (measured 11-24: the frame labelled k/fps matched an exact seek at k/fps + 0.5/fps, mean |diff| 0.001)
times = [a.t0 + (k + 0.5) / a.fps for k in range(len(files))]
ep = T.load(a.scenes)
tl = T.build(ep, a.timing)


def shot_at(t):
    for sh in tl["shots"]:
        if sh["t_start"] <= t < sh["t_end"]:
            return sh["id"]
    return "end"


def cap_at(t):
    for c in tl["captions"]:
        if c["on"] <= t < c["off"]:
            return c["text"]
    return ""


H6, W6 = 360, 640
cap_y0 = int((S.CAPTION["cy"] - S.CAPTION["box_h"] / 2) / S.H * H6)      # caption band top (y 933 @1080)
bg = np.array(S.BG, float)
arrs, inks = [], []
for fn in files:
    im = np.asarray(Image.open(os.path.join(fdir, fn)).convert("RGB")).astype(float)
    arrs.append(im)
# ① static content, ② flicker
content = [x[: int(0.80 * H6)] for x in arrs]          # above the source-line slot / caption band
diff = [float(np.abs(content[i] - content[i - 1]).mean()) for i in range(1, len(content))]
static_runs, st = [], None
for i, d in enumerate(diff + [99.0]):
    if d < 0.05 and st is None:
        st = i
    if d >= 0.05 and st is not None:
        run = (times[st], times[i])
        if run[1] - run[0] > 5.0:
            static_runs.append([round(run[0], 1), round(run[1], 1), shot_at(run[0])])
        st = None
flicker = []
for i in range(1, len(arrs) - 1):
    a0, a1, a2 = arrs[i - 1], arrs[i], arrs[i + 1]
    if np.abs(a0 - a2).mean() < 0.3 and np.abs(a1 - a0).mean() > 1.5:
        flicker.append([round(times[i], 2), shot_at(times[i])])
# ⑤ blank screen: content area (above the caption band) nearly empty for ≥ 1.0 s · flagged when narration is running
ink = []
for im in arrs:
    m = np.abs(im - bg).sum(axis=2) > 60
    m[int(0.77 * H6):] = False          # source-line slot (y ≈ 858/1080) and caption band excluded: a frame with
    ink.append(float(m.mean()))         # only a source line is an empty picture (11-25: s05b 4 s was missed at 0.80)
blank, st = [], None
for i, v in enumerate([x < 0.0015 for x in ink] + [False]):
    if v and st is None:
        st = i
    if not v and st is not None:
        r0, r1 = times[st] - 0.5 / a.fps, times[i - 1] + 0.5 / a.fps
        if r1 - r0 >= 1.0:
            talk = any(ln['t0'] < r1 and ln['t1'] > r0 for ln in tl['lines'])
            blank.append([round(r0, 2), round(r1, 2), shot_at(times[st]), 'speech' if talk else 'pause'])
        st = None
# ③ caption box over content: inside the caption box rows, non-box pixels that are neither bg nor box nor text
cap_cover = []
# ④ edge bands (content area only, above caption band); internal corner tag = top-left box ignored if --corner-tag
edge = []
for i, im in enumerate(arrs):
    m = np.abs(im - bg).sum(axis=2) > 60
    m[cap_y0 - 4:] = False
    if a.corner_tag:
        m[: int(0.10 * H6), : int(0.20 * W6)] = False
    band = np.zeros_like(m)
    band[:, : int(0.10 * W6)] = True
    band[:, int(0.90 * W6):] = True
    band[: int(0.08 * H6), :] = True
    n = int((m & band).sum())
    if n > 40:
        edge.append([round(times[i], 2), shot_at(times[i]), n])
    # caption box region: pixels directly above/below the caption box that are dark (box spill) — skip (box is fixed geometry)
# contact sheets
cols, rows = (int(x) for x in a.tiles.split("x"))
tw = a.tile_w
th = int(tw * 9 / 16)
per = cols * rows
try:
    fnt = ImageFont.truetype(S.FONTS["semibold"], max(12, tw // 26))
except OSError:
    fnt = ImageFont.load_default()
sheets = []
for k in range(0, len(files), per):
    sheet = Image.new("RGB", (cols * tw, rows * (th + 18)), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for j, fn in enumerate(files[k:k + per]):
        im = Image.open(os.path.join(fdir, fn)).convert("RGB").resize((tw, th), Image.BILINEAR)
        x, y = (j % cols) * tw, (j // cols) * (th + 18)
        sheet.paste(im, (x, y + 18))
        t = times[k + j]
        d.text((x + 4, y + 1), f"{int(t // 60)}:{t % 60:05.2f}  {shot_at(t)}", fill=(255, 230, 120), font=fnt)
    sp = os.path.join(a.out, f"sheet_{k // per + 1:02d}.jpg")
    sheet.save(sp, quality=88)
    sheets.append(sp)
# 10 fps filmstrips around given times
strips = []
for ts in [float(x) for x in a.strip.split(",") if x.strip()]:
    sd = os.path.join(a.out, f"strip_{ts:.1f}")
    os.makedirs(sd, exist_ok=True)
    for fn in os.listdir(sd):
        os.remove(os.path.join(sd, fn))
    subprocess.run(["ffmpeg", "-v", "error", "-threads", "2", "-y", "-ss", f"{max(0, ts - 1.0):.3f}", "-to", f"{ts + 1.0:.3f}",
                    "-i", a.video, "-vf", "fps=10,scale=384:-1", os.path.join(sd, "s_%03d.png")], check=True)
    sf = sorted(os.listdir(sd))
    c2, w2, h2 = 5, 384, 216
    r2 = (len(sf) + c2 - 1) // c2
    sheet = Image.new("RGB", (c2 * w2, r2 * (h2 + 16)), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for j, fn in enumerate(sf):
        im = Image.open(os.path.join(sd, fn)).convert("RGB").resize((w2, h2), Image.BILINEAR)
        x, y = (j % c2) * w2, (j // c2) * (h2 + 16)
        sheet.paste(im, (x, y + 16))
        t = max(0, ts - 1.0) + (j + 0.5) / 10
        d.text((x + 3, y), f"{t:.2f}s {shot_at(t)}", fill=(255, 230, 120), font=fnt)
    sp = os.path.join(a.out, f"strip_{ts:.1f}.jpg")
    sheet.save(sp, quality=88)
    strips.append(dict(at=ts, frames=len(sf), sheet=sp))
rep = dict(video=a.video, fps=a.fps, t0=a.t0, t1=round(t1, 2), frames=len(files), sheets=len(sheets),
           static_over_5s=static_runs, flicker=flicker, edge_band=edge[:40], edge_band_n=len(edge), blank_over_1s=blank,
           timing=a.timing,
           strips=strips, caption_chars_max=max(len(c["text"]) for c in tl["captions"]),
           captions_over_22=[c["text"] for c in tl["captions"] if len(c["text"]) > 22])
with open(os.path.join(a.out, "report.json"), "w", encoding="utf-8") as f:
    json.dump(rep, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in rep.items() if k not in ("edge_band",)}, ensure_ascii=False)[:1500])
