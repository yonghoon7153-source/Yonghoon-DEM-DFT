#!/usr/bin/env python3
"""build_ptfe_c10f22.py — PTFE 올리고머(C10F22, 32원자) ORCA 패키지.

목적: 건식전극 표준 바인더 PTFE의 NCM 앵커링을 SDCP와 정면 비교하는 캠페인 1단계.
  1단계(데스크톱 ORCA): C10F22 r2SCAN-3c 이완 — 이 스크립트
  2단계(gabia QE, Phase-B 5/5 이후): mol_ptfe(감마 박스) + complex_ptfe(동일 slab 재사용)
     → E_bind(PTFE) vs E_bind(SDCP doped/neutral); D3 후보정 패스 셋 동일 적용.
사이즈 패리티: C10F22 = 32원자 ≈ mol_doped 34원자 (같은 급 접촉 면적).

시작 기하 = PTFE 고유 13/6 헬릭스 (비틀림 166.15°/CF2, 상승 1.298 A, 반지름 0.42 A)
— all-trans가 아닌 실제 헬릭스로 시작해 수렴을 앞당김. 의존성 없음(표준 라이브러리).

  python3 build_ptfe_c10f22.py --out ptfe
"""
import argparse
import math
import os

NC = 10          # C10F22
CC_TWIST = math.radians(166.15)   # 13/6 helix twist per CF2
CC_RISE = 1.298
HELIX_R = 0.42
D_CF = 1.35
BETA = math.radians(52.0)         # F-C-F = 104도
TET = math.radians(70.5)          # CF3: 109.5도 보각


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    C = [[HELIX_R*math.cos(i*CC_TWIST), HELIX_R*math.sin(i*CC_TWIST), i*CC_RISE]
         for i in range(NC)]

    sym, pos = ["C"]*NC, [list(p) for p in C]

    def add_F(p):
        sym.append("F"); pos.append(p)

    for i in range(NC):
        if 0 < i < NC-1:                       # 내부 CF2
            t = unit(sub(C[i+1], C[i-1]))
            u = unit([C[i][0], C[i][1], 0.0])  # 헬릭스 축(z)에서 바깥 방향
            w = unit(cross(t, u))
            for s in (+1, -1):
                d = add(scal(u, math.cos(BETA)), scal(w, s*math.sin(BETA)))
                add_F(add(C[i], scal(unit(d), D_CF)))
        else:                                   # 말단 CF3
            nb = C[1] if i == 0 else C[NC-2]
            ax = unit(sub(C[i], nb))            # 사슬 반대 방향
            p = unit(cross(ax, [0.0, 0.0, 1.0] if abs(ax[2]) < 0.9 else [1.0, 0.0, 0.0]))
            q = unit(cross(ax, p))
            for k in range(3):
                ph = math.radians(120.0*k + 60.0)
                d = add(scal(ax, math.cos(TET)),
                        add(scal(p, math.sin(TET)*math.cos(ph)),
                            scal(q, math.sin(TET)*math.sin(ph))))
                add_F(add(C[i], scal(unit(d), D_CF)))

    assert len(sym) == 32 and sym.count("F") == 22, "C10F22 구성 오류"

    # sanity: 결합/비결합 통계
    ccb, cfb, ffmin, ang = [], [], 9e9, []
    for i in range(1, NC):
        ccb.append(norm(sub(pos[i], pos[i-1])))
    for i in range(NC-2):
        v1, v2 = sub(pos[i], pos[i+1]), sub(pos[i+2], pos[i+1])
        ang.append(math.degrees(math.acos(dot(v1, v2)/(norm(v1)*norm(v2)))))
    for i in range(32):
        for j in range(i+1, 32):
            d = norm(sub(pos[i], pos[j]))
            if sym[i] == "C" and sym[j] == "F" and d < 1.6:
                cfb.append(d)
            if sym[i] == "F" and sym[j] == "F" and d < ffmin:
                ffmin = d
    print(f"C-C {min(ccb):.3f}~{max(ccb):.3f} A | C-C-C {min(ang):.1f}~{max(ang):.1f}도 | "
          f"C-F {min(cfb):.3f}~{max(cfb):.3f} A ({len(cfb)}개) | F...F 최소 {ffmin:.2f} A")
    assert len(cfb) == 22 and ffmin > 2.0, "기하 이상"

    with open(os.path.join(a.out, "ptfe_c10f22.xyz"), "w") as f:
        f.write("32\nPTFE oligomer C10F22 - 13/6 helix start (build_ptfe_c10f22.py)\n")
        for s, p in zip(sym, pos):
            f.write(f"  {s:<2s}  {p[0]:16.8f} {p[1]:16.8f} {p[2]:16.8f}\n")
    with open(os.path.join(a.out, "ptfe.inp"), "w") as f:
        f.write("! r2SCAN-3c Opt TightSCF\n%maxcore 6000\n* xyzfile 0 1 ptfe_c10f22.xyz\n")
    with open(os.path.join(a.out, "run_ptfe.sh"), "w") as f:
        f.write("""#!/bin/bash
# 실행: nohup bash run_ptfe.sh > run.log 2>&1 &
ORCA=${ORCA:-/home/yonghoon/orca/orca}
cd "$(dirname "$0")"
if grep -q "ORCA TERMINATED NORMALLY" ptfe.out 2>/dev/null; then echo "[ptfe] done — skip"; exit 0; fi
echo "[ptfe] START $(date)"
$ORCA ptfe.inp > ptfe.out 2>&1
if grep -q "ORCA TERMINATED NORMALLY" ptfe.out; then
    conv="종료"; grep -q "THE OPTIMIZATION HAS CONVERGED" ptfe.out && conv="수렴"
    echo "[ptfe] DONE ($conv)  E=$(grep 'FINAL SINGLE POINT ENERGY' ptfe.out | tail -1 | awk '{print $NF}') Eh  $(date)"
else
    echo "[ptfe] FAILED  $(date)"
fi
""")
    print(f"패키지 완성: {a.out}/  (nohup bash {a.out}/run_ptfe.sh > {a.out}/run.log 2>&1 &)")


if __name__ == "__main__":
    main()
