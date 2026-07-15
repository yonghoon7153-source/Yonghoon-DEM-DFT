#!/usr/bin/env python3
"""build_ptfe_dimer_c4h2f8.py — 문헌 관행 'PTFE dimer' = H-(CF2CF2)2-H (C4H2F8, 14원자).

역할: PTFE 벤치마크의 문헌 비교 기준점. 물리 본편은 C10F22(패리티)가 담당하고,
이 조각은 binder-DFT 문헌들(PTFE_dimer 관행)과 나란히 놓을 숫자를 제공한다.
말단 C-H는 실제 PTFE에 없는 인공 캡이므로 해석 주의 (사이즈 수렴성 데이터로도 사용).

  python3 build_ptfe_dimer_c4h2f8.py --out ptfe_dimer
"""
import argparse
import math
import os

NC = 4
CC_TWIST = math.radians(166.15)
CC_RISE = 1.298
HELIX_R = 0.42
D_CF = 1.35
D_CH = 1.09
BETA = math.radians(52.0)


def sub(a, b): return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
def add(a, b): return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]
def scal(a, s): return [a[0]*s, a[1]*s, a[2]*s]
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def norm(a): return math.sqrt(dot(a, a))
def unit(a):
    n = norm(a)
    return [a[0]/n, a[1]/n, a[2]/n]


def bb(i):  # 가상 이웃 포함 헬릭스 좌표
    return [HELIX_R*math.cos(i*CC_TWIST), HELIX_R*math.sin(i*CC_TWIST), i*CC_RISE]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    C = [bb(i) for i in range(NC)]
    sym, pos = ["C"]*NC, [list(p) for p in C]

    for i in range(NC):
        prevC = bb(i-1)          # i=0이면 가상 C_{-1}
        nextC = bb(i+1)          # i=NC-1이면 가상 C_{NC}
        t = unit(sub(nextC, prevC))
        u = unit([C[i][0], C[i][1], 0.0])
        w = unit(cross(t, u))
        for s in (+1, -1):       # 모든 C에 F 2개
            d = add(scal(u, math.cos(BETA)), scal(w, s*math.sin(BETA)))
            sym.append("F"); pos.append(add(C[i], scal(unit(d), D_CF)))
        if i == 0:               # 말단 H: 사슬이 이어질 자리(가상 이웃 방향)
            sym.append("H"); pos.append(add(C[i], scal(unit(sub(prevC, C[i])), D_CH)))
        if i == NC-1:
            sym.append("H"); pos.append(add(C[i], scal(unit(sub(nextC, C[i])), D_CH)))

    assert len(sym) == 14 and sym.count("F") == 8 and sym.count("H") == 2, "C4H2F8 구성 오류"

    ccb = [norm(sub(pos[i], pos[i-1])) for i in range(1, NC)]
    cf = [norm(sub(p, q)) for si, p in zip(sym, pos) if si == "F"
          for sj, q in zip(sym, pos) if sj == "C" if norm(sub(p, q)) < 1.6]
    ch = [norm(sub(p, q)) for si, p in zip(sym, pos) if si == "H"
          for sj, q in zip(sym, pos) if sj == "C" if norm(sub(p, q)) < 1.3]
    print(f"C-C {min(ccb):.3f}~{max(ccb):.3f} | C-F x{len(cf)} {min(cf):.3f}~{max(cf):.3f} | "
          f"C-H x{len(ch)} {min(ch):.3f}~{max(ch):.3f} A")
    assert len(cf) == 8 and len(ch) == 2

    with open(os.path.join(a.out, "ptfe_dimer_c4h2f8.xyz"), "w") as f:
        f.write("14\nPTFE dimer H-(CF2CF2)2-H, literature-convention fragment (helix start)\n")
        for s, p in zip(sym, pos):
            f.write(f"  {s:<2s}  {p[0]:16.8f} {p[1]:16.8f} {p[2]:16.8f}\n")
    with open(os.path.join(a.out, "ptfe_dimer.inp"), "w") as f:
        f.write("! r2SCAN-3c Opt TightSCF\n%maxcore 6000\n* xyzfile 0 1 ptfe_dimer_c4h2f8.xyz\n")
    with open(os.path.join(a.out, "run_ptfe_dimer.sh"), "w") as f:
        f.write("""#!/bin/bash
# 실행: nohup bash run_ptfe_dimer.sh > run.log 2>&1 &
ORCA=${ORCA:-/home/yonghoon/orca/orca}
cd "$(dirname "$0")"
if grep -q "ORCA TERMINATED NORMALLY" ptfe_dimer.out 2>/dev/null; then echo "[ptfe_dimer] done — skip"; exit 0; fi
echo "[ptfe_dimer] START $(date)"
$ORCA ptfe_dimer.inp > ptfe_dimer.out 2>&1
if grep -q "ORCA TERMINATED NORMALLY" ptfe_dimer.out; then
    conv="종료"; grep -q "THE OPTIMIZATION HAS CONVERGED" ptfe_dimer.out && conv="수렴"
    echo "[ptfe_dimer] DONE ($conv)  E=$(grep 'FINAL SINGLE POINT ENERGY' ptfe_dimer.out | tail -1 | awk '{print $NF}') Eh  $(date)"
else
    echo "[ptfe_dimer] FAILED  $(date)"
fi
""")
    print(f"패키지 완성: {a.out}/")


if __name__ == "__main__":
    main()
