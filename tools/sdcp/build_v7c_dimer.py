#!/usr/bin/env python3
"""build_v7c_dimer.py — v7c 모노머 2개를 α–α 커플링한 다이머 + ORCA 잡 패키지 생성.

목적: 폴라론 비편재의 사슬-길이 의존 검증. 모노머 doped의 스핀 분포는 O₃ 65% /
백본 35% — 도로(공액)가 고리 1개뿐이라 정공이 O에 눌러앉은 값(하한). n=2에서
백본 몫이 커지는지 실측한다. 커지면 "폴리머에서 백본 폴라론" 그림 입증.

  python3 build_v7c_dimer.py --mol sdcp_v7c_neutral.xyz --out dimer [--uma cuda]

생성물 (out/):
  dimer_neutral.xyz (68원자 = 2×35 − α-H 2)   전하 0, 스핀 싱글렛
  dimer_doped.xyz   (67원자 = 위 − A쪽 산성H)  전하 0, 더블렛 (정공 1개/고리 2개)
  groups.json  스핀 분석용 원자 그룹 (A/B 설포네이트·싸이오펜 고리)
  dimer_*.inp + run_dimer.sh + analyze_dimer_spin.py  (r2SCAN-3c Opt, 모노머와 동일 레벨)
α–α 결합: 각 모노머의 링-S 이웃 C(α)에서 H 하나씩 제거, C–C 1.45 A로 접합,
비틀림각은 A–B 원자간 최소거리를 최대화하는 각으로 자동 선택(입체충돌 회피).
--uma 주면 ORCA 전에 UMA로 기하 정돈 (권장; kgy GPU 잔여로 가능).
"""
import argparse
import json
import os
import numpy as np
from ase.io import read, write


def find_parts(m):
    sym = m.get_chemical_symbols()
    d = m.get_all_distances()
    S_all = [i for i, s in enumerate(sym) if s == "S"]
    sulfS = [i for i in S_all
             if sum(1 for j, t in enumerate(sym) if t == "O" and d[i][j] < 1.8) >= 3]
    ringS = [i for i in S_all if i not in sulfS]
    assert len(sulfS) == 1 and len(ringS) == 1, "S 식별 실패"
    sS, rS = sulfS[0], ringS[0]
    sO = [j for j, t in enumerate(sym) if t == "O" and d[sS][j] < 1.8]
    aCs = [j for j, t in enumerate(sym) if t == "C" and d[rS][j] < 1.85]
    alphas = []
    for c in aCs:
        Hs = [h for h, t in enumerate(sym) if t == "H" and d[c][h] < 1.25]
        if Hs:
            alphas.append((c, Hs[0]))
    assert alphas, "α C–H 없음 (이미 커플링된 구조?)"
    betas = set()
    for c in aCs:
        for j, t in enumerate(sym):
            if t == "C" and j not in aCs and 0 < d[c][j] < 1.52 and d[rS][j] > 1.85:
                betas.add(j)
    ring = [rS] + aCs + sorted(betas)
    aO = aH = None
    for o in sO:
        for h, t in enumerate(sym):
            if t == "H" and d[o][h] < 1.15:
                aO, aH = o, h
    return dict(sS=sS, sO=sO, rS=rS, alphas=alphas, ring=ring, aO=aO, aH=aH)


def rot_to(mol, v_from, v_to, center):
    a = v_from / np.linalg.norm(v_from)
    b = v_to / np.linalg.norm(v_to)
    ax = np.cross(a, b)
    n = np.linalg.norm(ax)
    if n < 1e-8:
        if np.dot(a, b) < 0:
            p = np.array([0.0, 1.0, 0.0]) if abs(a[0]) > 0.9 else np.array([1.0, 0.0, 0.0])
            ax = np.cross(a, p)
            mol.rotate(180.0, ax / np.linalg.norm(ax), center=center)
        return
    ang = np.degrees(np.arccos(np.clip(np.dot(a, b), -1, 1)))
    mol.rotate(ang, ax / n, center=center)


def drop(atoms, idx):
    """원자 idx 제거 + old->new 인덱스 맵 반환."""
    keep = [i for i in range(len(atoms)) if i != idx]
    amap = {}
    for new, old in enumerate(keep):
        amap[old] = new
    return atoms[keep], amap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mol", required=True, help="sdcp_v7c_neutral.xyz (35원자)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--uma", default="", choices=["", "cuda", "cpu"],
                    help="ORCA 전 UMA 기하 정돈")
    ap.add_argument("--cc", type=float, default=1.45, help="새 C–C 길이 (A)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    A0 = read(a.mol)
    pa = find_parts(A0)
    cA, hA = pa["alphas"][0]
    vA = A0.positions[hA] - A0.positions[cA]
    vAu = vA / np.linalg.norm(vA)

    # ---- B: 복제, α방향을 -vA로 정렬, C–C 접합, 비틀림각 자동 ----
    best = None
    for th in range(0, 360, 20):
        B = A0.copy()
        vB = B.positions[hA] - B.positions[cA]
        rot_to(B, vB, -vAu, center=B.positions[cA])
        B.rotate(th, vAu, center=B.positions[cA])
        B.positions += (A0.positions[cA] + vAu * a.cc) - B.positions[cA]
        dmin = 9e9
        for i in range(len(A0)):
            if i == hA:
                continue
            dd = np.linalg.norm(B.positions - A0.positions[i], axis=1)
            dd[hA] = 9e9
            if i == cA:
                dd[cA] = 9e9          # 새 C–C 자체는 제외
            dmin = min(dmin, dd.min())
        if best is None or dmin > best[0]:
            best = (dmin, th, B)
    dmin, th, B = best
    print(f"비틀림각 {th}° 채택 (A–B 최소 원자간 {dmin:.2f} A)")

    A1, mA = drop(A0, hA)              # A: α-H 제거
    B1, mB = drop(B, hA)               # B: 같은 로컬 인덱스의 α-H 제거
    nA = len(A1)
    dimer = A1 + B1
    write(os.path.join(a.out, "dimer_neutral.xyz"), dimer)

    # ---- doped: A쪽 산성 H 제거 ----
    aH_n = mA[pa["aH"]]
    doped, mD = drop(dimer, aH_n)
    write(os.path.join(a.out, "dimer_doped.xyz"), doped)
    print(f"dimer_neutral {len(dimer)}원자 / dimer_doped {len(doped)}원자")

    # ---- groups.json (중성/도핑 각각의 인덱스) ----
    def grp(amap, off=0):
        return {
            "SO3": [amap[i] + off for i in [pa["sS"]] + pa["sO"] if i in amap],
            "ring": [amap[i] + off for i in pa["ring"] if i in amap],
        }
    gN = {"A_" + k: v for k, v in grp(mA).items()}
    gN.update({"B_" + k: v for k, v in grp(mB, off=nA).items()})
    gD = {k: [mD[i] for i in v if i in mD] for k, v in gN.items()}
    json.dump({"neutral": gN, "doped": gD,
               "monomer_ref": "doped spin: O3 ~65% / backbone ~35% (v7c, r2SCAN-3c)"},
              open(os.path.join(a.out, "groups.json"), "w"), indent=1)

    # ---- UMA 정돈 (선택) ----
    if a.uma:
        from ase.optimize import FIRE
        from fairchem.core import pretrained_mlip
        from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
        calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device=a.uma),
                                  task_name="oc20")
        for tag in ("dimer_neutral", "dimer_doped"):
            m = read(os.path.join(a.out, f"{tag}.xyz"))
            m.center(vacuum=8.0)
            m.calc = calc
            FIRE(m, logfile=None).run(fmax=0.05, steps=500)
            m.positions -= m.positions.mean(axis=0)
            write(os.path.join(a.out, f"{tag}.xyz"), m)
            print(f"[uma] {tag} 정돈 완료")

    # ---- ORCA 입력 + 러너 + 분석기 ----
    for tag, mult in (("dimer_neutral", 1), ("dimer_doped", 2)):
        with open(os.path.join(a.out, f"{tag}.inp"), "w") as f:
            f.write(f"! r2SCAN-3c Opt TightSCF\n%pal nprocs 8 end\n%maxcore 3000\n"
                    f"* xyzfile 0 {mult} {tag}.xyz\n")
    with open(os.path.join(a.out, "run_dimer.sh"), "w") as f:
        f.write("""#!/bin/bash
# 실행: nohup bash run_dimer.sh > run.log 2>&1 &   (ORCA 경로는 환경변수 ORCA로 덮어쓰기 가능)
ORCA=${ORCA:-$HOME/apps/orca-6.1.1/orca}
cd "$(dirname "$0")"
for j in dimer_neutral dimer_doped; do
    grep -q "ORCA TERMINATED NORMALLY" $j.out 2>/dev/null && { echo "[$j] done — skip"; continue; }
    echo "[$j] START $(date)"
    $ORCA $j.inp > $j.out 2>&1
    grep -q "ORCA TERMINATED NORMALLY" $j.out && echo "[$j] DONE $(date)" || echo "[$j] FAILED $(date)"
done
python3 analyze_dimer_spin.py
""")
    with open(os.path.join(a.out, "analyze_dimer_spin.py"), "w") as f:
        f.write('''#!/usr/bin/env python3
"""dimer_doped.out의 Loewdin 스핀을 groups.json 그룹별로 합산 — 모노머 65/35와 비교."""
import json, re
g = json.load(open("groups.json"))["doped"]
txt = open("dimer_doped.out", errors="ignore").read()
blocks = txt.split("LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS")
assert len(blocks) > 1, "Loewdin spin 블록 없음 (계산 미완?)"
spin = {}
for line in blocks[-1].splitlines()[2:]:
    m = re.match(r"\\s*(\\d+)\\s+\\w+\\s*:\\s*[-\\d.]+\\s+([-\\d.]+)", line)
    if not m:
        if spin: break
        continue
    spin[int(m.group(1))] = float(m.group(2))
tot = sum(spin.values())
print(f"total spin = {tot:.3f} (더블렛이면 ~1.0)")
acc = 0.0
for name, idx in g.items():
    s = sum(spin.get(i, 0.0) for i in idx)
    acc += s
    print(f"  {name:8s} {s:+.3f}  ({100*s/tot:5.1f}%)")
print(f"  {'rest':8s} {tot-acc:+.3f}  ({100*(tot-acc)/tot:5.1f}%)")
print("\\n판독: A_SO3+B_SO3 = 산소 라디칼 몫, A_ring+B_ring = 백본 폴라론 몫.")
print("모노머 참조: O3 ~65% / 백본 ~35%. 백본 몫이 커졌으면 비편재 입증(폴리머로 갈수록 더).")
''')
    print(f"패키지 완성: {a.out}/ (run_dimer.sh 실행 → 완료 시 스핀 분석 자동)")


if __name__ == "__main__":
    main()
