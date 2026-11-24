#!/usr/bin/env python3
"""ep01 final render checks — run after the final render (real narration):

  python3 -I final_check.py [--video ep01_final.mp4] [--timing audio/timing.json]   -> qc_final_check.md · qa/final_check/

  1 file · length          video ↔ timeline ↔ narration durations, streams, size, +faststart
  2 captions ↔ real voice   srt == timeline · ≤ 22 chars · no sentence-final period · first caption of a line vs speech start ·
                            every caption overlaps its own line's speech · no speech without a caption · changed lines
  3 element timing          (real timing moves anchors) element that would appear after its shot ends · appears < 0.6 s before
                            the shot ends · move / dim / out after the shot ends
  4 sound                   integrated loudness · true peak (ffmpeg ebur128 on the mp4's own audio track) · clipping ·
                            pause between sentences = timing.json · long gap inside a sentence (dropout candidate)
  5 public safety           internal/public_deny_list.txt over the public files · retracted-value sweep (claims.json ·
                            read only) · internal / repo image paths
  6 first · last frames · thumbnail   extracted for viewing (qa/final_check/first_last.jpg) · thumbnail size
Nothing here sends audio or text anywhere; ffmpeg runs under nice -n 10 with 2 threads.
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(os.path.dirname(HERE), "tools")
sys.path.insert(0, TOOLS)
import avi_audio as A  # noqa: E402
import avi_style as S  # noqa: E402
import avi_timeline as T  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--video", default="ep01_final.mp4")
ap.add_argument("--timing", default="audio/timing.json")
ap.add_argument("--out", default="qc_final_check.md")
a = ap.parse_args()
mp4 = os.path.join(HERE, a.video)
tpath = os.path.join(HERE, a.timing)
ep = T.load(os.path.join(HERE, "scenes.json"))
tl = T.build(ep, tpath)
tm = json.load(open(tpath, encoding="utf-8"))
qa_dir = os.path.join(HERE, "qa", "final_check")
os.makedirs(qa_dir, exist_ok=True)
L = [f"# 최종판 점검 — `{a.video}` (실제 음성 시각 `{a.timing}`)", "",
     "> 자동 검사 = 이 스크립트 (`final_check.py`) 가 렌더 결과 · 자막 파일 · 음성 시각표를 다시 잰 값.  "
     "장면 그림 (0.5 s) = `qa_frames.py --timing` 대조표를 사람이 직접 본 기록 (`rubric_ep01_v2.md` 최종판 절).", ""]
fails = []


def ok(cond, what):
    if not cond:
        fails.append(what)
    return "통과" if cond else "**걸림**"


def fmt_t(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


# ------------------------------------------------------------------ 1 file · length
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels,duration:format=duration,size",
                                "-of", "json", mp4], capture_output=True, text=True, check=True).stdout)
vs = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
au = [s for s in pr["streams"] if s["codec_type"] == "audio"][0]
dur_f, size = float(pr["format"]["duration"]), int(pr["format"]["size"])
with open(mp4, "rb") as f:
    head = f.read(4 << 20)
fast = head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
dv, da = float(vs.get("duration", dur_f)), float(au.get("duration", dur_f))
L += ["## 1. 파일 · 길이", "",
      f"- {vs['width']}×{vs['height']} · {vs['r_frame_rate']} fps · {vs['codec_name']} · 소리 {au['codec_name']} {au['sample_rate']} Hz "
      f"{au['channels']} ch · {size / 1e6:.1f} MB · +faststart {'예' if fast else '아니오'}",
      f"- 길이: 영상 {dv:.2f} s ({fmt_t(dv)}) · 소리 {da:.2f} s · 타임라인 {tl['duration']:.2f} s · 이어 붙인 음성 {tm['total']:.2f} s → "
      f"영상 ↔ 타임라인 {abs(dv - tl['duration']):.3f} s {ok(abs(dv - tl['duration']) <= 0.06, '영상 길이 ≠ 타임라인')} · "
      f"소리 ↔ 음성 {abs(da - tm['total']):.3f} s {ok(abs(da - tm['total']) <= 0.1, '소리 길이 ≠ 음성')}",
      f"- 문장 {len(tl['lines'])} · 자막 {len(tl['captions'])} · 장면 {len(ep['scenes'])} · 샷 {len(tl['shots'])} · "
      f"첫 말 {tl['lines'][0]['t0']:.2f} s · 마지막 말 끝 {tl['lines'][-1]['t1']:.2f} s ({fmt_t(tl['lines'][-1]['t1'])})", ""]

# ------------------------------------------------------------------ 2 captions ↔ real voice
srt = open(os.path.join(HERE, "ep01.srt"), encoding="utf-8").read().strip().split("\n\n")


def srt_t(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000.0


sc_ = []
for blk in srt:
    ls = blk.strip().split("\n")
    t0s, t1s = ls[1].split(" --> ")
    sc_.append((srt_t(t0s), srt_t(t1s), "\n".join(ls[2:])))
caps = tl["captions"]
same = len(sc_) == len(caps) and all(abs(x[0] - c["on"]) < 0.002 and abs(x[1] - c["off"]) < 0.002 and x[2] == c["text"]
                                     for x, c in zip(sc_, caps))
long_ = [c["text"] for c in caps if len(c["text"]) > 22]
period = [c["text"] for c in caps if c["text"].rstrip().endswith(".") or re.search(r"\.(?!\d)", c["text"].replace("...", ""))]
lid = tl["lid"]
first = {}
for c in caps:
    first.setdefault(c["line"], c)
leads = np.array([lid[i]["t0"] - c["on"] for i, c in first.items()])
late = [(i, round(lid[i]["t0"] - c["on"], 3)) for i, c in first.items() if lid[i]["t0"] - c["on"] < 0.0]
early = [(i, round(lid[i]["t0"] - c["on"], 3)) for i, c in first.items() if lid[i]["t0"] - c["on"] > 0.45]
no_overlap = [(c["line"], c["text"]) for c in caps if not (c["on"] < lid[c["line"]]["t1"] and c["off"] > lid[c["line"]]["t0"])]
gaps = []
for ln in tl["lines"]:
    cs = sorted([c for c in caps if c["line"] == ln["id"]], key=lambda c: c["on"])
    t = ln["t0"]
    for c in cs:
        if c["on"] > t + 0.15:
            gaps.append((ln["id"], round(t, 2), round(c["on"], 2)))
        t = max(t, c["off"])
    if t < ln["t1"] - 0.15:
        gaps.append((ln["id"], round(t, 2), round(ln["t1"], 2)))
changed = {}


def bare(t):                                     # captions drop the comma at a split and the final period
    return re.sub(r"[\s,.?!·…]", "", t)


for i in ("s06_l04", "s10_l03"):
    got = "".join(c["text"] for c in caps if c["line"] == i)
    changed[i] = (" / ".join(c["text"] for c in caps if c["line"] == i), bare(got) == bare(lid[i]["say"]))
L += ["## 2. 자막 ↔ 실제 음성 시각", "",
      f"- `ep01.srt` = 타임라인 자막 ({len(sc_)} ↔ {len(caps)} · 글 · 켜짐 · 꺼짐 ±2 ms): {ok(same, 'srt ≠ 타임라인')}",
      f"- 22 자 넘는 자막 {len(long_)} {long_ if long_ else ''}: {ok(not long_, '22 자 넘음')} · 마침표로 끝나는 자막 {len(period)} "
      f"{period[:5] if period else ''}: {ok(not period, '마침표 자막')}",
      f"- 문장 첫 자막이 말보다 앞서는 시간 (설정 0.20 s): 중앙 {np.median(leads):.2f} · 최소 {leads.min():.2f} · 최대 {leads.max():.2f} s · "
      f"말보다 늦은 자막 {len(late)} {late[:6] if late else ''}: {ok(not late, '말보다 늦은 자막')} · 0.45 s 넘게 이른 자막 {len(early)} "
      f"{early[:6] if early else ''}",
      f"- 자기 문장의 말과 겹치지 않는 자막 {len(no_overlap)}: {ok(not no_overlap, '말과 안 겹치는 자막')} · "
      f"말하는데 자막이 없는 틈 (0.15 s 넘음) {len(gaps)} {gaps[:6] if gaps else ''}: {ok(not gaps, '자막 없는 말')}",
      "- 바뀐 두 문장 (11-25 끝말 고침): " + " · ".join(f"{i} = '{v[0]}' {ok(v[1], i + ' 자막 = 새 글 아님')}" for i, v in changed.items()),
      ""]

# ------------------------------------------------------------------ 3 element timing under the real timeline
issues, flash, brief = [], [], []
for sh in tl["shots"]:
    for e in sh.get("elements", []):
        if e.get("keep"):
            for k in ("move_at", "dim_at"):
                if k in e:
                    tt = T.resolve(e[k], tl, sh)
                    if tt >= sh["t_end"]:
                        issues.append((sh["id"], e.get("id", e.get("keep")), k, round(tt - sh["t_end"], 2)))
            continue
        t_in = T.resolve(e.get("at", "shot+0.3"), tl, sh)
        if t_in >= sh["t_end"]:
            issues.append((sh["id"], e.get("id"), "at", round(t_in - sh["t_end"], 2)))
        elif sh["t_end"] - t_in < 0.6:
            flash.append((sh["id"], e.get("id"), round(sh["t_end"] - t_in, 2)))
        elif sh["t_end"] - t_in < 1.0:
            brief.append((sh["id"], e.get("id"), round(sh["t_end"] - t_in, 2)))
        for k in ("dim", "undim", "out"):
            if k in e and T.resolve(e[k], tl, sh) >= sh["t_end"] + 0.01:
                issues.append((sh["id"], e.get("id"), k, round(T.resolve(e[k], tl, sh) - sh["t_end"], 2)))
        for mv in e.get("moves", []):
            if T.resolve(mv["at"], tl, sh) >= sh["t_end"]:
                issues.append((sh["id"], e.get("id"), "moves", round(T.resolve(mv["at"], tl, sh) - sh["t_end"], 2)))
spans = [(sh["id"], round(sh["t_end"] - sh["t_start"], 2)) for sh in tl["shots"]]
short = [x for x in spans if x[1] < 2.0]
L += ["## 3. 화면 개체 시각 (실제 음성으로 닻이 옮겨진 뒤)", "",
      f"- 샷이 끝난 뒤에야 나오거나 움직이는 개체 {len(issues)} {issues[:8] if issues else ''}: {ok(not issues, '샷 끝난 뒤 개체')}",
      f"- 샷 끝 0.6 s 안에 나와 바로 사라지는 개체 {len(flash)} {flash[:8] if flash else ''}: {ok(not flash, '깜빡 개체')} · "
      f"1.0 s 안 (참고) {len(brief)} {brief[:8] if brief else ''}",
      f"- 샷 길이 최소 {min(x[1] for x in spans):.2f} s · 2 s 안 되는 샷 {len(short)} {short if short else ''}", ""]

# ------------------------------------------------------------------ 4 sound (the mp4's own audio track)
er = subprocess.run(["nice", "-n", "10", "ffmpeg", "-nostats", "-hide_banner", "-threads", "2", "-i", mp4, "-map", "0:a",
                     "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
summ = er[er.rfind("Summary:"):]


def grab(pat):
    m = re.search(pat, summ)
    return float(m.group(1)) if m else None


I_, LRA, TP = grab(r"I:\s+(-?[\d.]+) LUFS"), grab(r"LRA:\s+(-?[\d.]+) LU"), grab(r"Peak:\s+(-?[\d.]+) dBFS")
x = A.decode(mp4, threads=2)
clip = int(np.sum(np.abs(x) >= 0.999))
sil, info = A.silences(x, min_dur=0.12)
sil = np.array(sil) if sil else np.zeros((0, 2))
perr, dropouts = [], []
for k in range(len(tl["lines"]) - 1):
    l0, l1 = tl["lines"][k], tl["lines"][k + 1]
    want = l1["t0"] - l0["t1"]
    lo, hi = l0["t1"] - 0.3, l1["t0"] + 0.3                    # the measured quiet run, clipped to the gap ± 0.3 s
    cov = [min(s1, hi) - max(s0, lo) for s0, s1 in sil if s0 < hi and s1 > lo]
    perr.append((l0["id"], round(want, 3), round(max(cov) if cov else 0.0, 3)))
for ln in tl["lines"]:
    inner = [(s0, s1) for s0, s1 in sil if s0 > ln["t0"] + 0.05 and s1 < ln["t1"] - 0.05 and s1 - s0 > 0.6]
    dropouts += [(ln["id"], round(s0, 2), round(s1 - s0, 2)) for s0, s1 in inner]
errs = np.array([abs(g - w_) for _, w_, g in perr]) if perr else np.zeros(1)
bad_p = [p for p in perr if abs(p[2] - p[1]) > 0.12]
L += ["## 4. 소리 (mp4 안의 소리를 다시 잼)", "",
      f"- 음량 (ffmpeg ebur128 · 통합) {I_} LUFS {ok(I_ is not None and abs(I_ + 14) <= 1.0, '음량 −14 ± 1 밖')} · LRA {LRA} LU · "
      f"참 최고점 {TP} dBFS {ok(TP is not None and TP <= -1.0, '참 최고점 > −1')} · 클리핑 표본 {clip} {ok(clip == 0, '클리핑')}",
      f"- 문장 사이 쉼 = 음성 시각표 ({len(perr)} 이음매 · 잰 쉼 = 소리 레벨로 찾은 무음 · 경계 ±0.1 s): 차 중앙 {np.median(errs):.3f} · "
      f"최대 {errs.max():.3f} s · 0.12 s 넘게 다른 곳 {len(bad_p)} {bad_p[:6] if bad_p else ''}",
      f"- 문장 안 0.6 s 넘는 무음 (끊김 후보) {len(dropouts)} {dropouts[:8] if dropouts else ''} · 무음 문턱 {info['thr']:.1f} dB "
      f"(말 {info['ref']:.1f} · 바닥 {info['floor']:.1f})",
      f"- 시작 {tl['lines'][0]['t0']:.2f} s 전 = 무음 · 끝 = 마지막 말 뒤 {dv - tl['lines'][-1]['t1']:.2f} s (끝 화면)", ""]

# ------------------------------------------------------------------ 5 public safety
deny = [ln.strip() for ln in open(os.path.join(HERE, "internal", "public_deny_list.txt"), encoding="utf-8")
        if ln.strip() and not ln.startswith("#")]
pub = ["scenes.json", "ep01.srt", "script.md", "script_header.md", "timeline.json", "tts_typecast.tsv", "tts_elevenlabs.txt",
       "tts_plain.txt", "tts_ssml.xml", "voice_audition.txt"]
dh = []
for fn in pub:
    txt = open(os.path.join(HERE, fn), encoding="utf-8").read()
    dh += [(fn, d) for d in deny if d in txt]
bs = subprocess.run([sys.executable, "-I", os.path.join(TOOLS, "ban_sweep_files.py")] + [os.path.join(HERE, f_) for f_ in pub],
                    capture_output=True, text=True)
imgs = sorted({e["path"] for sc in ep["scenes"] for sh in sc["shots"] for e in sh["elements"] if e.get("type") == "image"})
leak = [p for p in imgs if "internal" in p or not p.startswith(os.path.join(HERE, "assets"))]
L += ["## 5. 공개 안전", "",
      f"- 내부 숫자 목록 (`internal/public_deny_list.txt` · {len(deny)} 줄) × 공개 파일 {len(pub)} 개 ({' · '.join(pub)}): 걸림 {len(dh)} "
      f"{dh if dh else ''} {ok(not dh, '내부 숫자 누출')}",
      f"- 철회값 스윕 (`docs/reviews/claims.json` `quotation_ban` · 읽기만): rc {bs.returncode} {ok(bs.returncode == 0, '철회값')} "
      f"{bs.stdout.strip().splitlines()[-1] if bs.stdout.strip() else ''}",
      f"- 화면 그림 파일 {[os.path.relpath(p, HERE) for p in imgs]} · 내부판 · 리포 그림 {len(leak)} {ok(not leak, '그림 누출')}",
      "- 결과 · 숫자 · 우리 계산 그림 = S10 은 비교의 설계만 (숫자 · 그림 파일 없음 — `qc_final.md` §5) · 내부판은 `internal/` 무음 그대로", ""]

# ------------------------------------------------------------------ 6 first · last frames · thumbnail
lt = tl["lines"]
pts = [("시작 0.3 s", 0.3), ("첫 말", lt[0]["t0"] + 0.3), ("첫 샷 끝", tl["shots"][0]["t_end"] - 0.2),
       ("마지막 장면 첫 샷", [sh for sh in tl["shots"] if sh["scene"] == ep["scenes"][-1]["id"]][0]["t_start"] + 1.0),
       ("마지막 말", lt[-1]["t1"] - 0.3), ("끝 화면", dv - 0.15)]
tiles = []
for k, (lab, t) in enumerate(pts):
    p = os.path.join(qa_dir, f"fl_{k}.png")
    subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-threads", "2", "-y", "-ss", f"{t:.3f}", "-i", mp4,
                    "-frames:v", "1", "-vf", "scale=640:-1", p], check=True)
    tiles.append((lab, t, p))
sheet = Image.new("RGB", (3 * 640, 2 * (360 + 22)), (40, 40, 40))
d = ImageDraw.Draw(sheet)
f = S.font("semibold", 18)
for k, (lab, t, p) in enumerate(tiles):
    x0, y0 = (k % 3) * 640, (k // 3) * (360 + 22)
    sheet.paste(Image.open(p).convert("RGB"), (x0, y0 + 22))
    d.text((x0 + 6, y0 + 2), f"{lab}  {fmt_t(t)}", fill=(255, 230, 120), font=f)
fl = os.path.join(qa_dir, "first_last.jpg")
sheet.save(fl, quality=88)
th = Image.open(os.path.join(HERE, "thumbnail.png"))
L += ["## 6. 첫 · 끝 장면 · 썸네일", "",
      f"- 대조표 `qa/final_check/first_last.jpg` ({' · '.join(f'{lab} {fmt_t(t)}' for lab, t, _ in tiles)}) — 사람이 본 기록은 기준표 절",
      f"- 썸네일 `thumbnail.png` {th.size[0]}×{th.size[1]} {ok(th.size == (1280, 720), '썸네일 크기')}", ""]
L += ["## 요약", "", f"- 자동 검사 걸림 {len(fails)} {fails if fails else ''}"]
with open(os.path.join(HERE, a.out), "w", encoding="utf-8") as fo:
    fo.write("\n".join(L) + "\n")
print("\n".join(L))
sys.exit(1 if fails else 0)
