#!/usr/bin/env python3
"""build_v7c_trimer.py — 이완된 v7c 다이머에서 세 번째 고리를 α–α' 접합한 트라이머 패키지.

n=3의 목적 (n=2 결과의 다음 질문):
  다이머 doped 스핀: A_SO3 62.3 / A_ring 17.4 / B_SO3 0.0 / B_ring 15.2 / rest 5.0 %
  → SO3:백본 파티션(62:33)은 모노머(65:35) 그대로, 백본 몫은 두 고리에 거의 반반.
  고리가 3개면?
   - trimer_doped_mid: 가운데 고리 SO3⁻ → 폴라론이 양옆 대칭으로 3고리에 퍼지는가 (헤드라인)
   - trimer_doped_end: 끝 고리 SO3⁻   → 결함에서 멀수록 몫이 어떻게 감쇠하는가 (감쇠길이)

입력은 이완된 dimer_neutral.xyz 하나뿐 (모노머 파일·ASE·numpy 불필요):
  - 다이머 B쪽 절반(이완 기하)을 복제해 C-유닛으로 사용 — C-유닛의 열린 α(과거 A와
    결합하던 자리)를 B의 자유 α에 C–C 1.45 A로 접합, B의 자유 α-H는 제거
  - 비틀림각은 원자간 최소거리 최대화(입체 회피)로 자동 선택 — 다이머 빌더와 동일 철학

  python3 build_v7c_trimer.py --dimer dimer_neutral.xyz --out trimer

생성물 (out/):
  trimer_neutral.xyz (101원자, 전하0 싱글렛) / trimer_doped_mid.xyz·trimer_doped_end.xyz
  (100원자, 전하0 더블렛) / groups_trimer.json (그룹 인덱스 + 산성H 인덱스) /
  trimer_*.inp (r2SCAN-3c Opt, 시리얼·maxcore 6000) / run_trimer.sh (neutral 완료 시
  doped를 neutral 최종기하에서 warm-start) / analyze_trimer_spin.py / watch_trimer.sh
"""
import argparse
import json
import math
import os

RCOV = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "S": 1.05}
CC_NEW = 1.45          # 새 C–C 접합 길이 (다이머 빌더와 동일; 이완 다이머 실측 1.44)


# ---------- 기하 유틸 (numpy 없이) ----------
def sub(a, b): return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]
def add(a, b): return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]
def scal(a, s): return [a[0]*s, a[1]*s, a[2]*s]
def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
def norm(a): return math.sqrt(dot(a, a))
def unit(a):
    n = norm(a)
    return [a[0]/n, a[1]/n, a[2]/n]
def dist(a, b): return norm(sub(a, b))


def rotmat(axis, ang):
    x, y, z = axis
    c, s, C = math.cos(ang), math.sin(ang), 1.0 - math.cos(ang)
    return [[x*x*C+c,   x*y*C-z*s, x*z*C+y*s],
            [y*x*C+z*s, y*y*C+c,   y*z*C-x*s],
            [z*x*C-y*s, z*y*C+x*s, z*z*C+c]]


def apply_rot(R, p):
    return [R[0][0]*p[0]+R[0][1]*p[1]+R[0][2]*p[2],
            R[1][0]*p[0]+R[1][1]*p[1]+R[1][2]*p[2],
            R[2][0]*p[0]+R[2][1]*p[1]+R[2][2]*p[2]]


def rot_between(v_from, v_to):
    """v_from → v_to 정렬 회전행렬 (Rodrigues; 평행/역평행 안전)."""
    a, b = unit(v_from), unit(v_to)
    ax = cross(a, b)
    n = norm(ax)
    d = max(-1.0, min(1.0, dot(a, b)))
    if n < 1e-8:
        if d > 0:
            return rotmat([1.0, 0.0, 0.0], 0.0)
        p = [0.0, 1.0, 0.0] if abs(a[0]) > 0.9 else [1.0, 0.0, 0.0]
        return rotmat(unit(cross(a, p)), math.pi)
    return rotmat([ax[0]/n, ax[1]/n, ax[2]/n], math.acos(d))


# ---------- xyz / 연결성 ----------
def read_xyz(path):
    L = open(path).read().strip().splitlines()
    n = int(L[0].split()[0])
    sym, pos = [], []
    for l in L[2:2+n]:
        t = l.split()
        sym.append(t[0])
        pos.append([float(t[1]), float(t[2]), float(t[3])])
    assert len(sym) == n, "xyz 원자 수 불일치"
    return sym, pos


def write_xyz(path, sym, pos, comment):
    with open(path, "w") as f:
        f.write(f"{len(sym)}\n{comment}\n")
        for s, p in zip(sym, pos):
            f.write(f"  {s:<2s}  {p[0]:18.10f} {p[1]:18.10f} {p[2]:18.10f}\n")


def neighbors(sym, pos):
    n = len(sym)
    nb = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if dist(pos[i], pos[j]) < 1.25 * (RCOV.get(sym[i], 0.8) + RCOV.get(sym[j], 0.8)):
                nb[i].append(j)
                nb[j].append(i)
    return nb


def analyze(sym, pos):
    """링/설포네이트/α/산성H 식별 — 모노머·다이머·트라이머 공통."""
    nb = neighbors(sym, pos)
    ringS, sulfS = [], []
    for i, s in enumerate(sym):
        if s != "S":
            continue
        nO = sum(1 for j in nb[i] if sym[j] == "O")
        (sulfS if nO >= 3 else ringS).append(i)
    rings = []
    for rS in sorted(ringS):
        aC = [j for j in nb[rS] if sym[j] == "C"]
        assert len(aC) == 2, f"S{rS}: α-C {len(aC)}개 (2개여야 함)"
        a1, a2 = aC
        closure = None
        for b1 in nb[a1]:
            if sym[b1] != "C" or b1 in (rS, a1, a2):
                continue
            for b2 in nb[a2]:
                if sym[b2] != "C" or b2 in (rS, a1, a2, b1):
                    continue
                if b2 in nb[b1]:
                    closure = (b1, b2)
                    break
            if closure:
                break
        assert closure, f"S{rS}: 5-ring 폐환 실패"
        alphas = []
        for c in (a1, a2):
            Hs = [h for h in nb[c] if sym[h] == "H"]
            ext = [j for j in nb[c] if sym[j] == "C" and j not in (rS, a1, a2) + closure]
            alphas.append(dict(C=c, H=(Hs[0] if Hs else None),
                               coupled=(ext[0] if ext else None)))
        rings.append(dict(rS=rS, alphas=alphas,
                          ring=[rS, a1, a2, closure[0], closure[1]]))
    sulf = []
    for sS in sorted(sulfS):
        sO = [j for j in nb[sS] if sym[j] == "O"]
        aH = None
        for o in sO:
            for h in nb[o]:
                if sym[h] == "H":
                    aH = h
        # 이 설포네이트가 붙은 링: BFS로 처음 만나는 링
        owner = None
        seen, q = {sS}, [sS]
        while q and owner is None:
            cur = q.pop(0)
            for r_i, r in enumerate(rings):
                if cur in r["ring"]:
                    owner = r_i
                    break
            if owner is not None:
                break
            for j in nb[cur]:
                if j not in seen:
                    seen.add(j)
                    q.append(j)
        assert owner is not None, f"설포네이트 S{sS}의 소속 링 못 찾음"
        sulf.append(dict(sS=sS, sO=sO, aH=aH, ring=owner))
    return nb, rings, sulf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dimer", required=True, help="이완된 dimer_neutral.xyz (68원자)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cc", type=float, default=CC_NEW)
    ap.add_argument("--step", type=int, default=10, help="비틀림각 스캔 간격(도)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    sym, pos = read_xyz(a.dimer)
    assert len(sym) == 68, f"다이머 68원자 기대, {len(sym)}개"
    nb, rings, sulf = analyze(sym, pos)
    assert len(rings) == 2 and len(sulf) == 2, "다이머: 링 2 + 설포네이트 2여야 함"

    # ---- 다이머 위상: 링간 결합 (cA–cB), 각 링의 자유 α ----
    coupled = [(r_i, al) for r_i, r in enumerate(rings) for al in r["alphas"] if al["coupled"] is not None]
    assert len(coupled) == 2, "링간 결합 α는 정확히 2개여야 함"
    free = {r_i: al for r_i, r in enumerate(rings) for al in r["alphas"] if al["H"] is not None}
    assert len(free) == 2, "각 링에 자유 α-H 1개씩이어야 함"

    # B쪽 = 인덱스가 큰 링 (구성상 34..67). 링간 결합을 끊고 flood-fill로 절반 분리.
    riA, riB = 0, 1
    cB = [al["C"] for r_i, al in coupled if r_i == riB][0]
    cA = [al["C"] for r_i, al in coupled if r_i == riA][0]
    assert cA in nb[cB], "링간 결합 불일치"
    seen, q = {cB}, [cB]
    while q:
        cur = q.pop(0)
        for j in nb[cur]:
            if (cur, j) in ((cB, cA), (cA, cB)):
                continue
            if j not in seen:
                seen.add(j)
                q.append(j)
    sideB = sorted(seen)
    assert len(sideB) == 34 and cA not in seen, f"B쪽 분리 실패 ({len(sideB)}원자)"

    cBf, hBf = free[riB]["C"], free[riB]["H"]          # B의 자유 α와 그 H (제거 대상)
    print(f"위상: 링간결합 C{cA}–C{cB} ({dist(pos[cA], pos[cB]):.3f} A) | "
          f"B 자유 α = C{cBf} (H{hBf}) | B쪽 {len(sideB)}원자")

    # ---- C-유닛 배치: 열린 α(cB 사본)를 cBf에 접합 ----
    d_dir = unit(sub(pos[hBf], pos[cBf]))              # 새 결합 방향 (기존 C–H 방향)
    p_new = add(pos[cBf], scal(d_dir, a.cc))           # cB 사본의 목표 위치
    u_dangle = unit(sub(pos[cA], pos[cB]))             # 사본의 열린 원자가 방향
    R0 = rot_between(u_dangle, scal(d_dir, -1.0))

    base0 = [apply_rot(R0, sub(pos[i], pos[cB])) for i in sideB]   # cB 원점 로컬 좌표

    exclB = set([cBf] + list(nb[cBf]))                  # 접합부 1-2/1-3 (θ 불변) 제외
    exclC = set([cB] + [j for j in nb[cB] if j in seen])
    baseAtoms = [i for i in range(68) if i != hBf]

    best = None
    for th in range(0, 360, a.step):
        R1 = rotmat(d_dir, math.radians(th))
        newpos = [add(apply_rot(R1, p), p_new) for p in base0]
        dmin = 9e9
        for bi in baseAtoms:
            for k, oj in enumerate(sideB):
                if bi in exclB and oj in exclC:
                    continue
                dd = dist(pos[bi], newpos[k])
                if dd < dmin:
                    dmin = dd
        if best is None or dmin > best[0]:
            best = (dmin, th, newpos)
    dmin, th, cpos = best
    print(f"비틀림각 {th}° 채택 (최소 원자간 {dmin:.2f} A)")

    # ---- 조립: 다이머(−hBf) + C-유닛 ----
    tsym = [sym[i] for i in baseAtoms] + [sym[i] for i in sideB]
    tpos = [pos[i] for i in baseAtoms] + cpos
    n_tri = len(tsym)
    assert n_tri == 101, f"트라이머 101원자 기대, {n_tri}"
    write_xyz(os.path.join(a.out, "trimer_neutral.xyz"), tsym, tpos,
              f"v7c trimer (built from relaxed dimer; torsion {th} deg, dmin {dmin:.2f} A)")

    # ---- 조립체 재분석 → 그룹/산성H (인덱스 부기 대신 신선 검출) ----
    tnb, trings, tsulf = analyze(tsym, tpos)
    assert len(trings) == 3 and len(tsulf) == 3, "트라이머: 링 3 + 설포네이트 3이어야 함"
    n_coup = [sum(1 for al in r["alphas"] if al["coupled"] is not None) for r in trings]
    mids = [i for i, c in enumerate(n_coup) if c == 2]
    ends = [i for i, c in enumerate(n_coup) if c == 1]
    assert len(mids) == 1 and len(ends) == 2, f"사슬 위상 이상 (coupled={n_coup})"
    ends.sort(key=lambda i: min(trings[i]["ring"]))
    name = {ends[0]: "A", mids[0]: "B", ends[1]: "C"}   # A=원래 끝, B=가운데, C=새 유닛
    print("링 판정:", {name[i]: f"S{trings[i]['rS']}(coupled α {n_coup[i]})" for i in range(3)})

    groups_n, acidH = {}, {}
    for su in tsulf:
        nm = name[su["ring"]]
        groups_n[f"{nm}_SO3"] = sorted([su["sS"]] + su["sO"])
        groups_n[f"{nm}_ring"] = sorted(trings[su["ring"]]["ring"])
        assert su["aH"] is not None, f"{nm} 설포네이트에 산성 H 없음"
        acidH[nm] = su["aH"]
    print("산성 H (neutral 기준):", acidH)

    # ---- doped 변형: mid = B의 산성H 제거, end = A의 산성H 제거 ----
    variants = {"trimer_doped_mid": acidH["B"], "trimer_doped_end": acidH["A"]}
    groups_all = {"neutral": groups_n}
    for tag, k in variants.items():
        vsym = [s for i, s in enumerate(tsym) if i != k]
        vpos = [p for i, p in enumerate(tpos) if i != k]
        write_xyz(os.path.join(a.out, f"{tag}.xyz"), vsym, vpos,
                  f"{tag}: trimer_neutral minus acid H{k} (charge 0, doublet)")
        remap = lambda i: i - (1 if i > k else 0)
        groups_all[tag] = {g: [remap(i) for i in idx if i != k] for g, idx in groups_n.items()}
    groups_all["acidH"] = {t: k for t, k in variants.items()}
    groups_all["dimer_ref"] = "doped: A_SO3 62.3 / A_ring 17.4 / B_SO3 0.0 / B_ring 15.2 / rest 5.0 %"
    groups_all["monomer_ref"] = "doped: O3 ~65% / backbone ~35%"
    json.dump(groups_all, open(os.path.join(a.out, "groups_trimer.json"), "w"), indent=1)

    # ---- ORCA 입력 (시리얼 — 데스크톱 검증된 레시피: %pal 없음, maxcore 6000) ----
    for tag, mult in (("trimer_neutral", 1), ("trimer_doped_mid", 2), ("trimer_doped_end", 2)):
        with open(os.path.join(a.out, f"{tag}.inp"), "w") as f:
            f.write(f"! r2SCAN-3c Opt TightSCF\n%maxcore 6000\n* xyzfile 0 {mult} {tag}.xyz\n")

    # ---- 러너: neutral → (완료 시 doped를 neutral 최종기하에서 warm-start) → mid → end ----
    with open(os.path.join(a.out, "run_trimer.sh"), "w") as f:
        f.write("""#!/bin/bash
# 실행: nohup bash run_trimer.sh > run.log 2>&1 &
ORCA=${ORCA:-/home/yonghoon/orca/orca}
cd "$(dirname "$0")"

refresh_doped () {   # $1=tag — neutral 최종 xyz에서 산성H 제거해 warm-start xyz 재생성
python3 - "$1" <<'PY'
import json, sys
tag = sys.argv[1]
k = json.load(open("groups_trimer.json"))["acidH"][tag]
L = open("trimer_neutral.xyz").read().strip().splitlines()
n = int(L[0].split()[0]); atoms = L[2:2+n]
del atoms[k]
open(f"{tag}.xyz", "w").write(f"{n-1}\\n{tag}: warm-start from trimer_neutral final (H{k} removed)\\n"
                              + "\\n".join(atoms) + "\\n")
print(f"[{tag}] xyz를 neutral 최종기하에서 재생성 ({n-1}원자)")
PY
}

run_job () {
    j=$1
    if grep -q "ORCA TERMINATED NORMALLY" $j.out 2>/dev/null; then echo "[$j] done — skip"; return; fi
    echo "[$j] START $(date)"
    $ORCA $j.inp > $j.out 2>&1
    grep -q "ORCA TERMINATED NORMALLY" $j.out && echo "[$j] DONE $(date)" || echo "[$j] FAILED $(date)"
}

run_job trimer_neutral
if grep -q "ORCA TERMINATED NORMALLY" trimer_neutral.out 2>/dev/null; then
    [ -f trimer_doped_mid.out ] || refresh_doped trimer_doped_mid
    [ -f trimer_doped_end.out ] || refresh_doped trimer_doped_end
fi
run_job trimer_doped_mid
run_job trimer_doped_end
python3 analyze_trimer_spin.py
""")

    # ---- 분석기 ----
    with open(os.path.join(a.out, "analyze_trimer_spin.py"), "w") as f:
        f.write('''#!/usr/bin/env python3
"""트라이머 doped 잡들의 Loewdin 스핀을 그룹 합산 — 모노머 65/35, 다이머 62/17/15와 비교."""
import json, os, re
G = json.load(open("groups_trimer.json"))
for tag in ("trimer_doped_mid", "trimer_doped_end"):
    if not os.path.exists(f"{tag}.out"):
        print(f"[{tag}] 아직 출력 없음"); continue
    txt = open(f"{tag}.out", errors="ignore").read()
    blocks = txt.split("LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS")
    if len(blocks) < 2:
        print(f"[{tag}] Loewdin 블록 아직 없음 (진행 중)"); continue
    spin = {}
    for line in blocks[-1].splitlines()[2:]:
        m = re.match(r"\\s*(\\d+)\\s+\\w+\\s*:\\s*[-\\d.]+\\s+([-\\d.]+)", line)
        if not m:
            if spin: break
            continue
        spin[int(m.group(1))] = float(m.group(2))
    tot = sum(spin.values())
    print(f"\\n===== {tag}  (total spin {tot:.3f}; 더블렛 ~1.0) =====")
    acc = 0.0
    ringsum = {}
    for gname in ("A_SO3","A_ring","B_SO3","B_ring","C_SO3","C_ring"):
        s = sum(spin.get(i, 0.0) for i in G[tag][gname])
        acc += s
        if gname.endswith("_ring"): ringsum[gname[0]] = s
        print(f"  {gname:8s} {s:+.3f}  ({100*s/tot:5.1f}%)")
    print(f"  {'rest':8s} {tot-acc:+.3f}  ({100*(tot-acc)/tot:5.1f}%)")
    bb = sum(ringsum.values())
    print(f"  백본 합계 {bb:+.3f} ({100*bb/tot:.1f}%) | 고리별 A:B:C = "
          + " : ".join(f"{100*ringsum[r]/tot:.1f}" for r in "ABC"))
print("\\n참조: 모노머 O3 65 / 백본 35  |  다이머 A_SO3 62.3, 고리 17.4/15.2 (백본 32.6)")
print("판독: mid는 대칭 확산(A~C), end는 감쇠(A>B>C)가 나오면 비편재 그림 완성.")
''')

    # ---- watch ----
    with open(os.path.join(a.out, "watch_trimer.sh"), "w") as f:
        f.write("""#!/bin/bash
# watch -n 60 bash ~/orca_poly/trimer/watch_trimer.sh
cd "$(dirname "$0")"
echo "══════ SDCP trimer ORCA (serial, ext4)  $(date '+%m-%d %H:%M:%S') ══════"
cpu=$(ps -eo comm,pcpu | awk '/orca|mpirun/{s+=$2} END{printf "%d", s+0}')
echo " 일꾼 CPU 합계: ${cpu}%  (시리얼 정상 ~100%)"
for j in trimer_neutral trimer_doped_mid trimer_doped_end; do
    o=$j.out
    if [ ! -f "$o" ]; then echo " $j: ⬚ 대기"; continue; fi
    cyc=$(grep -c "GEOMETRY OPTIMIZATION CYCLE" "$o")
    e=$(grep "FINAL SINGLE POINT ENERGY" "$o" | tail -1 | awk '{print $NF}')
    if grep -q "ORCA TERMINATED NORMALLY" "$o"; then
        conv="수렴"; grep -q "THE OPTIMIZATION HAS CONVERGED" "$o" || conv="종료"
        echo " $j: ✅ DONE($conv)  cycles=$cyc  E=$e Eh"
    else
        g=$(grep "MAX gradient" "$o" | tail -1 | awk '{print $3}')
        age=$(( $(date +%s) - $(stat -c %Y "$o") ))
        tag="⏳ RUN"; [ $age -gt 900 ] && tag="⚠정체${age}s"
        echo " $j: $tag  cycle $cyc  E=${e:-–}  MAXgrad=${g:-–} (${age}s前)"
    fi
done
python3 analyze_trimer_spin.py 2>/dev/null | sed 's/^/ /'
""")
    print(f"패키지 완성: {a.out}/  (nohup bash {a.out}/run_trimer.sh > {a.out}/run.log 2>&1 &)")


if __name__ == "__main__":
    main()
