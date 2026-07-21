#!/usr/bin/env python3
"""drag_build_kgy.py — Li hollow->hollow barrier via CONSTRAINED-DRAG profile.

neb.x가 kgy QE-GPU 빌드에 없음(pw.x/pp.x만) -> Li3N에서 검증된 사내 방법
"구속 PES-직접 프로파일"로 barrier를 뽑는다 (pw.x만 사용). Li의 이동좌표 x를
고정(if_pos = 0 0 1: x,y 고정 / z 자유)하고 나머지 원자 전부 이완 -> 각 이미지의
구속-최소 에너지 -> E(x) 프로파일 -> barrier = max - start.

hollow->hollow(+a1 = +2.46 A) 직선 홉이라 대칭상 MEP가 y로 안 휘어(fix x,y OK).
Shi2017 hBN 표면 0.10 eV가 검증 앵커. 7 이미지(끝점 2 + 중간 5).

Cases: 원본 relax(.out)가 있는 것만. Li가 마지막 원자.
  각 case c -> drag/<c>/img{0..6}.in  (calculation='relax', Li if_pos 0 0 1)
"""
import os
import re

WORK = os.environ.get("WORK", os.path.expanduser("~/work/vgcf_hbn"))
DRAG = f"{WORK}/drag"
CASES = ["Li_on_hbn", "Li_on_graphene", "Li_in_gallery", "Li_in_gallery_2L2L"]
HOP = 2.46      # A, +a1 (nearest hollow-hollow on the honeycomb)
N_IMG = 7       # img0=start hollow ... img6=next hollow; img3 ~ bridge (TS)


def final_coords(path):
    if not os.path.exists(path):
        return None
    t = open(path, errors="ignore").read()
    if "JOB DONE" not in t or "Begin final coordinates" not in t:
        return None
    blk = t.split("Begin final coordinates")[-1].split("End final coordinates")[0]
    at = [l.split() for l in blk.splitlines() if re.match(r"\s*[A-Z][a-z]?\s+-?\d", l)]
    return [(a[0], float(a[1]), float(a[2]), float(a[3])) for a in at]


def main():
    os.makedirs(DRAG, exist_ok=True)
    for c in CASES:
        A = final_coords(f"{WORK}/{c}.out")
        if A is None:
            print(f"  {c}: 원본 relax 미완/없음 — skip")
            continue
        assert A[-1][0] == "Li", f"{c}: Li가 마지막 원자가 아님"
        tin = open(f"{WORK}/{c}.in").read()
        d = f"{DRAG}/{c}"
        os.makedirs(d, exist_ok=True)
        e, xA, yA, zA = A[-1]
        for i in range(N_IMG):
            xi = xA + i * HOP / (N_IMG - 1)
            # 기판 = 이완된 A 그대로 (모든 이미지 공통 시작점), Li만 x,y 고정
            lines = [f"  {s:2s} {x:14.8f} {yy:14.8f} {z:14.8f}   1 1 1"
                     for s, x, yy, z in A[:-1]]
            lines.append(f"  Li {xi:14.8f} {yA:14.8f} {zA:14.8f}   0 0 1")
            pos = "\n".join(lines)
            t = re.sub(r"(ATOMIC_POSITIONS angstrom\n).*?(\n\nK_POINTS)",
                       lambda m: m.group(1) + pos + m.group(2), tin, flags=re.S)
            t = t.replace("prefix          = '", f"prefix          = 'd{i}", 1)
            open(f"{d}/img{i}.in", "w").write(t)
        print(f"  {c}: {N_IMG} drag 이미지 -> {d}/img*.in  (Li x: {xA:.2f}->{xA+HOP:.2f} A, if_pos 0 0 1)")


if __name__ == "__main__":
    main()
