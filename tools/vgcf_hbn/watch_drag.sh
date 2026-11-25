#!/usr/bin/env bash
# watch_drag.sh — Li 확산 constrained-drag 진행 (kgy). 7 이미지/케이스, barrier=max-start.
#   watch -n 60 'bash ~/Yonghoon-DEM-DFT/tools/vgcf_hbn/watch_drag.sh'
set +H
W=${WORK:-$HOME/work/vgcf_hbn}; D=$W/drag
echo "══ Li diffusion constrained-drag (hollow→hollow, Li x,y 고정, 7 img)  $(date '+%m-%d %H:%M:%S') ══"
gpu=$(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
run=$(pgrep -af 'pw\.x' 2>/dev/null | grep -aoE 'img[0-9]+\.in' | head -1)
echo "  실행중: ${run:-없음}  | GPU ${gpu} (used,free,util%)"
python3 - "$D" <<'PY'
import re, sys, os, glob
D = sys.argv[1]; Ry = 13.605693
for c in ("Li_on_hbn", "Li_on_graphene", "Li_in_gallery", "Li_in_gallery_2L2L"):
    d = f"{D}/{c}"
    if not os.path.isdir(d): print(f"  {c:22s} · 대기"); continue
    outs = sorted(glob.glob(f"{d}/img*.out"), key=lambda p: int(re.search(r"img(\d+)", p).group(1)))
    E, done = [], 0
    for o in outs:
        t = open(o, errors="ignore").read()
        m = re.findall(r"^!\s+total energy\s+=\s+(-\d+\.\d+)", t, re.M)
        if "JOB DONE" in t and m: E.append(float(m[-1])); done += 1
        else: E.append(None)
    n = len(glob.glob(f"{d}/img*.in"))
    if done and E[0] is not None:
        prof = [(e - E[0]) * Ry if e is not None else None for e in E]
        bar = max(p for p in prof if p is not None)
        ps = " ".join(f"{p:+.2f}" if p is not None else " ..." for p in prof)
        tag = "barrier=%.3f eV" % bar if done == n else "부분"
        print(f"  {c:22s} {done}/{n}  {tag}  [{ps}]")
    else:
        print(f"  {c:22s} {done}/{n} (start 대기)")
PY
echo "  기준: hBN 표면 0.10(Shi) / graphene ~0.3(문헌) / gallery=신규. img3≈bridge(TS)."
