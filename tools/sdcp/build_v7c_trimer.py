#!/usr/bin/env python3
"""build_v7c_trimer.py — v7c 다이머에서 올리고머(DP3/4/6) Stage 0 패키지를 조립한다.

원래는 트라이머 전용이었고 (파일명이 그 흔적), doped 재개 v3
(`kb/questions/sdcp_doped_reopen_v3_2026_08_28.md`)의 Stage 0 을 위해 **2단계(stage A/B)
아키텍처 + 회수 analyzer** 로 재작성했다 (회신 R2 의 8개 최소 수정 반영, 2026-08-28).

  [stage A]  다이머 → geometry seed 별 중성 조립 + RKS Opt 입력
  [ORCA]     각 seed 의 neutral 을 사람이/러너가 최적화
  [stage B]  최적화된 부모(R⁰)에서 REQUIRED_MATRIX 전건 생성 —
             R⁰−H 수직(vertical) 기하 · sp_vertical(SP+StabPerform) · opt_adiabatic ·
             RKS/UKS 명시 · SCF seed(s0/s1) · calculation_id(불변) · manifest v3
  [ORCA]     sp 먼저 → analyzer 게이트 통과한 (pattern,sector) 만 opt
  [analyze]  --analyze <dir>: .out 게이트, **abort code 실제 emit**
  [hybrid]   hybrid_select(): 승자∪창내∪localization class 대표 → wB97X-D3 fresh-start

  python3 build_v7c_trimer.py --selftest
  python3 build_v7c_trimer.py --stage a --dimer db/structures/sdcp_v7c_dimer_neutral.xyz \
      --out ~/orca_poly/dp6_v3 --n 6                    # seed 수는 SEED_FLOOR 기본(8)
  # (ORCA 로 gs*/dp6_gs*_neutral 최적화 후)
  python3 build_v7c_trimer.py --stage b --n 6 --gseed 0 \
      --neutral_xyz ~/orca_poly/dp6_v3/gs0/dp6_gs0_neutral.xyz --out ~/orca_poly/dp6_v3/gs0_b
  python3 build_v7c_trimer.py --analyze ~/orca_poly/dp6_v3/gs0_b

레거시 (--dimer/--out 만, 종전과 동일): trimer_neutral / doped_mid / doped_end 패키지.
⚠ v2 인터페이스(--holes)는 회신 R2 로 **제거** — 매트릭스는 REQUIRED_MATRIX 가 강제한다.

이 도구가 **못 하는 것**
  · 기하를 이완하지 않는다 — ORCA 몫. stage B 는 "최적화된 부모" 를 신뢰가 아니라
    위상·닫힌꼴 검사로 받는다 (그래도 Opt 수렴 여부 자체는 analyzer/.out 몫).
  · 스핀 상태를 보장하지 않는다 — 섹터별 기대(HFTyp·<S²>)를 manifest 에 선언하고
    analyzer 가 게이트할 뿐이다.
  · carrier_localization_profile 을 산출하지 않는다 — analyzer 는 **게이트까지**
    (수렴·섹터·오염·안정성). 집합별 스핀 적분·BLA·UNO 프로파일은 후속 도구.
  · Yamaguchi AP·spin-flip 을 계산하지 않는다 — BS 는 기록 요구만 강제한다.
  · adaptive stopping 을 자동 실행하지 않는다 — SEED_FLOOR 규칙을 manifest 에 선언하고
    seed 를 발급할 뿐, 정지 판정은 배치 결과를 보고 사람이/analyzer 확장이 한다.
"""
import argparse
import hashlib
import json
import math
import os
import re

RCOV = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "S": 1.05}
ZNUM = {"H": 1, "C": 6, "N": 7, "O": 8, "S": 16}
CC_NEW = 1.45          # 새 C–C 접합 길이 (다이머 빌더와 동일; 이완 다이머 실측 1.44)
UNIT_NAMES = "ABCDEFGH"

#: 스핀 섹터 — conditioning 에는 **ansatz 만** ('polaron/bipolaron' 은 realized 판정).
#:   (sec, wavefunction_class, orca_mult, n_alpha_minus_beta(최종 Ms), bs_flip, 라벨)
#:   ⚠ 회신 R2 P0-1 정정: closed-shell 은 **RKS 를 명시**해 생성한다 — 종전엔 전 잡이
#:   UKS 로 나가 manifest 와 모순이었다. bs 는 고스핀(mult 3) 수렴 후 BrokenSym 플립 —
#:   BS M_s=0 determinant (nominal OSS candidate). raw E 를 singlet 에너지로 쓰지 않는다.
SECTORS_ODD = (("d", "UKS", 2, 1, False, "doublet"),)
SECTORS_EVEN = (("s", "RKS", 1, 0, False, "RKS closed-shell candidate"),
                ("t", "UKS", 3, 2, False, "UKS triplet"),
                ("bs", "UKS-BS", 3, 0, True,
                 "BS M_s=0 determinant (nominal OSS candidate) — <S2>·국소 signed spin·"
                 "UNO 보고 필수; Yamaguchi AP 는 2-중심 식별시에만"))
ABORT_CODES = ("NA_STATE_NOT_IDENTIFIED", "NA_SPIN_MODEL_NOT_IDENTIFIED",
               "METHOD_DEPENDENT", "SECTOR_MISMATCH", "SCF_UNCONVERGED",
               "SPIN_CONTAMINATION_UNREPORTED", "STABILITY_UNSTABLE")

#: 필수 job matrix (회신 R2 조건 3 — **하나라도 못 만들면 stage B 는 실패한다**).
#:   dp6 pairs 에 off-center B,C 포함 (R2 Q2 권고 — 기존 singles 재사용).
REQUIRED_MATRIX = {
    3: {"singles": ["A", "B"], "pairs": []},          # end / middle
    4: {"singles": ["A", "B"], "pairs": []},          # end / inner
    6: {"singles": ["B", "C", "D", "E"],
        "pairs": ["C,D", "B,E", "A,F", "B,C"]},
}
#: 쌍별 정책 (회신 R2 Q2): A,F 는 섹터 비교 전용 — U 값·거리 추세·부호 일반화 주장 금지.
PAIR_POLICY = {
    "C,D": "U_PCET", "B,E": "U_PCET", "B,C": "U_PCET (off-center)",
    "A,F": "sector_comparison_only — U(AF)·short-medium-long 추세·DP6 전체 부호 일반화 "
           "주장 금지. 필요해지면 hA·hF 자동 승격 (회신 R2 Q2)",
}
#: geometry seed 승인 바닥 (회신 R2 Q4): (초기 독립 torsion seed 수, 연속 K=2 null batch 수).
#:   새 저에너지 basin·상태순서·localization class 변화가 나오면 null counter 리셋.
#:   --step 변경은 독립 seed 로 세지 않는다.
SEED_FLOOR = {3: (4, 2), 4: (4, 2), 6: (8, 4)}


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
    """링/설포네이트/α/산성H 식별 — 모노머·다이머·올리고머 공통."""
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


def ring_chain_names(rings):
    """링을 사슬 순서로 A,B,C,... 명명. 앵커(A)=최소 원자 인덱스를 가진 끝 링.

    ⛔ 못 하는 것: 가지 친(branched) 사슬. 경로가 유일하지 않으면 멈춘다.
    """
    a2r = {}
    for ri, r in enumerate(rings):
        for al in r["alphas"]:
            a2r[al["C"]] = ri
    adj = {ri: set() for ri in range(len(rings))}
    for ri, r in enumerate(rings):
        for al in r["alphas"]:
            c = al["coupled"]
            if c is not None:
                rj = a2r.get(c)
                assert rj is not None, f"링 {ri} 의 coupled C{c} 가 어떤 링의 α 도 아니다"
                adj[ri].add(rj)
                adj[rj].add(ri)
    ends = [ri for ri in adj if len(adj[ri]) == 1]
    if len(rings) == 1:
        return {0: "A"}
    if len(ends) != 2:
        raise SystemExit(f"⛔ 사슬 위상이 아니다 (끝 링 {len(ends)}개) — 가지/고리 구조는 지원 밖")
    start = min(ends, key=lambda ri: min(rings[ri]["ring"]))
    path = [start]
    while len(path) < len(rings):
        nxt = [x for x in adj[path[-1]] if x not in path]
        assert len(nxt) == 1, "사슬 경로가 유일하지 않다"
        path.append(nxt[0])
    return {ri: UNIT_NAMES[k] for k, ri in enumerate(path)}


# ---------- 조립 ----------
def make_template(sym, pos, nb, rings, riB, cA, cB):
    """다이머 B쪽 절반 → 재사용 가능한 접합 유닛 템플릿 (cB 원점 로컬 좌표)."""
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
    assert len(sideB) * 2 == len(sym) and cA not in seen, \
        f"B쪽 분리 실패 ({len(sideB)}/{len(sym)}원자)"
    u_dangle = unit(sub(pos[cA], pos[cB]))
    base0 = [sub(pos[i], pos[cB]) for i in sideB]
    tsym = [sym[i] for i in sideB]
    # 템플릿 내부 이웃 (접합부 제외 규칙용) + 자유 α/H 로컬 인덱스
    loc = {g: k for k, g in enumerate(sideB)}
    dangle_loc = loc[cB]
    tnb = neighbors(tsym, base0)
    free_al = [al for al in rings[riB]["alphas"] if al["H"] is not None]
    assert len(free_al) == 1, "B 링의 자유 α 가 1개가 아니다"
    return dict(sym=tsym, base0=base0, u_dangle=u_dangle, dangle=dangle_loc,
                dangle_nb=set(tnb[dangle_loc]) | {dangle_loc},
                freeC=loc[free_al[0]["C"]], freeH=loc[free_al[0]["H"]])


DMIN_FLOOR = 2.0    # Å — geometry seed 후보각 자격 (이하는 입체 충돌로 제외)


def graft(csym, cpos, cnb, attC, attH, tpl, cc, step, gseed=0, gidx=0):
    """사슬의 자유 α(attC, 그 H=attH)에 템플릿을 접합. → (sym, pos, 채택각, dmin)

    geometry seed (회신 R2 조건 6): gseed=0 은 종전과 동일한 max-dmin 결정론.
    gseed>0 은 dmin ≥ DMIN_FLOOR 인 **후보각들 중에서** 결정론적 LCG 로 고른다 —
    같은 max-dmin 탐색의 격자 간격(--step)을 바꾸는 것은 독립 seed 가 아니다.
    """
    d_dir = unit(sub(cpos[attH], cpos[attC]))
    p_new = add(cpos[attC], scal(d_dir, cc))
    R0 = rot_between(tpl["u_dangle"], scal(d_dir, -1.0))
    b0 = [apply_rot(R0, p) for p in tpl["base0"]]
    exclB = set([attC] + list(cnb[attC]))
    base_atoms = [i for i in range(len(csym)) if i != attH]
    cands = []
    for th in range(0, 360, step):
        R1 = rotmat(d_dir, math.radians(th))
        newpos = [add(apply_rot(R1, p), p_new) for p in b0]
        dmin = 9e9
        for bi in base_atoms:
            for k in range(len(newpos)):
                if bi in exclB and k in tpl["dangle_nb"]:
                    continue
                dd = dist(cpos[bi], newpos[k])
                if dd < dmin:
                    dmin = dd
        cands.append((dmin, th, newpos))
    cands.sort(key=lambda c: -c[0])
    if gseed == 0:
        dmin, th, npos = cands[0]
    else:
        ok = [c for c in cands if c[0] >= DMIN_FLOOR] or cands[:1]
        pick = ((gseed * 2654435761 + gidx * 40503) & 0xFFFFFFFF) % len(ok)
        dmin, th, npos = ok[pick]
    nsym = [csym[i] for i in base_atoms] + list(tpl["sym"])
    nposs = [cpos[i] for i in base_atoms] + npos
    return nsym, nposs, th, dmin


def build_chain(sym, pos, n, cc, step, log=print, gseed=0):
    """다이머(n=2) → n-량체. 각 단계에서 앵커 반대쪽 끝의 자유 α 에 접합."""
    nb, rings, sulf = analyze(sym, pos)
    if not (len(rings) == 2 and len(sulf) == 2):
        raise SystemExit(f"⛔ 입력이 다이머가 아니다 (링 {len(rings)} · 설포네이트 {len(sulf)})")
    coupled = [(ri, al) for ri, r in enumerate(rings) for al in r["alphas"]
               if al["coupled"] is not None]
    assert len(coupled) == 2, "링간 결합 α는 정확히 2개여야 함"
    riA, riB = 0, 1
    cB = [al["C"] for ri, al in coupled if ri == riB][0]
    cA = [al["C"] for ri, al in coupled if ri == riA][0]
    assert cA in nb[cB], "링간 결합 불일치"
    tpl = make_template(sym, pos, nb, rings, riB, cA, cB)
    torsions = []
    csym, cpos = list(sym), list(pos)
    for k in range(n - 2):
        cnb, crings, _ = analyze(csym, cpos)
        names = ring_chain_names(crings)
        # 앵커(A) 반대쪽 끝 = 이름이 가장 뒤인 링의 자유 α
        last = max(names, key=lambda ri: names[ri])
        free_al = [al for al in crings[last]["alphas"] if al["H"] is not None]
        assert len(free_al) == 1, "끝 링의 자유 α 가 1개가 아니다"
        csym, cpos, th, dmin = graft(csym, cpos, cnb, free_al[0]["C"], free_al[0]["H"],
                                     tpl, cc, step, gseed=gseed, gidx=k)
        torsions.append(dict(step=k + 3, torsion_deg=th, dmin_A=round(dmin, 3)))
        log(f"  유닛 {k+3}/{n} 접합: 비틀림 {th}° (최소 원자간 {dmin:.2f} A)")
    expect = len(sym) + (n - 2) * (len(sym) // 2 - 1)
    assert len(csym) == expect, f"{n}-량체 {expect}원자 기대, {len(csym)}"
    return csym, cpos, torsions


# ---------- 조성·홀·manifest ----------
#: v7c 실물 선형 n-량체의 닫힌꼴 기대식 (회신 R): C_{11n} H_{14n+2-m} O_{6n} S_{2n},
#: 전전자 N_e = 160n + 2 - m. 빌더 산출이 이것과 다르면 **빌더가 틀린 것** — 멈춘다.
V7C_DIMER_FORMULA = "C22H30O12S4"


def expected_species(n, m):
    return ({"C": 11 * n, "H": 14 * n + 2 - m, "O": 6 * n, "S": 2 * n},
            160 * n + 2 - m)


def check_closed_form(sym, n, m):
    want_f, want_e = expected_species(n, m)
    cnt = {}
    for x in sym:
        cnt[x] = cnt.get(x, 0) + 1
    return cnt == want_f and electrons_of(sym) == want_e


def formula_of(sym):
    cnt = {}
    for s in sym:
        cnt[s] = cnt.get(s, 0) + 1
    return "".join(f"{e}{cnt[e]}" for e in ("C", "H", "N", "O", "S") if e in cnt)


def electrons_of(sym):
    return sum(ZNUM[s] for s in sym)


def check_parity(n_e, mult):
    """전자수 짝홀 ↔ 다중도 정합. 어긋나면 그 잡은 정의부터 틀린 것 — 만들지 않는다."""
    if (n_e + mult) % 2 != 1:
        raise SystemExit(f"⛔ 전자 {n_e}개에 다중도 {mult} 는 불가능 — 잡을 만들지 않는다")


def remove_atoms(sym, pos, kill):
    kill = sorted(set(kill), reverse=True)
    vsym, vpos = list(sym), list(pos)
    for k in kill:
        del vsym[k]
        del vpos[k]
    def remap(i):
        return i - sum(1 for k in kill if k < i)
    return vsym, vpos, remap


def resolve_holes(spec, names, sulf):
    """--holes 'B,E' → 제거할 산성 H 인덱스들. 없는 링/산성H 없는 링이면 멈춘다."""
    ring_by_name = {v: k for k, v in names.items()}
    out = []
    for letter in [x.strip().upper() for x in spec.split(",") if x.strip()]:
        if letter not in ring_by_name:
            raise SystemExit(f"⛔ --holes {spec}: 링 '{letter}' 가 없다 (있는 링: "
                             f"{''.join(sorted(ring_by_name))})")
        su = [s for s in sulf if s["ring"] == ring_by_name[letter]]
        if not su or su[0]["aH"] is None:
            raise SystemExit(f"⛔ 링 {letter} 에 산성 H 가 없다 — 홀을 만들 수 없다")
        out.append((letter, su[0]["aH"]))
    if not out:
        raise SystemExit(f"⛔ --holes '{spec}' 에서 링을 못 읽었다")
    return out


def atom_sets_of(csym, cnb, crings, csulf, names):
    """carrier_localization_profile 용 원자 집합 (중성 프레임 인덱스).

    backbone = 공액 고리 원자 + 고리에 붙은 H · sulfonate_X = S+3O(+산성H) ·
    sidechain_rest = 나머지(스페이서 등). ⛔ doped 프레임 인덱스는 removed_H 로
    밀린다 — 재매핑은 분석기 몫 (manifest 에 경고 포함).
    """
    ring_atoms = set()
    for r in crings:
        ring_atoms |= set(r["ring"])
    ring_H = {h for i in ring_atoms for h in cnb[i] if csym[h] == "H"}
    sets = {"backbone": sorted(ring_atoms | ring_H)}
    used = set(sets["backbone"])
    for su in csulf:
        grp = sorted([su["sS"]] + su["sO"] + ([su["aH"]] if su["aH"] is not None else []))
        sets[f"sulfonate_{names[su['ring']]}"] = grp
        used |= set(grp)
    sets["sidechain_rest"] = sorted(set(range(len(csym))) - used)
    return sets


#: 교차검사 방법 — "ωB97X-D급" 금지 (회신 R 조건 7): 계산 전에 정확히 지정한다.
HYBRID_KEYWORDS = "wB97X-D3 def2-TZVP defGrid3"
HYBRID_SPEC = {
    "keywords": HYBRID_KEYWORDS,
    "fresh_start": "r2SCAN orbital 미승계 (MORead 금지 — 입력에 주석으로 박힌다)",
    "decision_set": "vertical 승자 ∪ adiabatic 승자 ∪ 승자 0.10 eV 이내 ∪ "
                    "**realized localization class 별 최저 대표 전부** (회신 R2 조건 8)",
    "escalation": "hybrid 가 state identity/localization/순서를 바꾸면 그 상태만 hybrid 재최적화",
    "disagreement": "두 방법이 갈리면 평균하지 않고 METHOD_DEPENDENT",
    "version_field": "orca_version 은 회수 시 .out 배너에서 채운다 (사전 기재 금지)",
}


def make_inp(path, xyz_name, wf, mult, bs, job_type, scf_seed="s0", hybrid=False):
    """job type 별 ORCA 입력 (회신 R2 P0-1·조건 2 — RKS/UKS 와 SP/Opt 를 명시 생성).

    job_type: 'opt_neutral' (RKS Opt) · 'sp_vertical' (SP + StabPerform) ·
              'opt_adiabatic' (Opt — analyzer 가 vertical stability 통과를 확인한 뒤에만 실행)
    scf_seed: s0 = 기본 guess · s1 = Hueckel (독립 SCF/localization seed — R2 조건 6)
    """
    kw = "RKS" if wf == "RKS" else "UKS"
    base = HYBRID_KEYWORDS if hybrid else "r2SCAN-3c"
    opt = " Opt" if job_type in ("opt_neutral", "opt_adiabatic") else ""
    method = f"{base}{opt} TightSCF"
    scf_opts = []
    if job_type == "sp_vertical" and not bs:
        scf_opts.append("StabPerform true")
    if bs:
        scf_opts.append("BrokenSym 1,1")
    if scf_seed == "s1":
        scf_opts.append("Guess Hueckel")
    with open(path, "w") as f:
        f.write(f"! {kw} {method}\n%maxcore 6000\n")
        if hybrid:
            f.write("# fresh-start: MORead 금지 (r2SCAN orbital 미승계 — HYBRID_SPEC)\n")
        if scf_opts:
            f.write("%scf " + " ".join(scf_opts) + " end\n")
        f.write(f"* xyzfile 0 {mult} {xyz_name}\n")


def calculation_id(cond):
    """불변 계산 ID (회신 R2 조건 6·8) — **conditioning 만** 해시. realized 값이 들어가면
    ID 가 결과에 따라 변해 immutable 이 아니게 된다 (selftest 가 막는다)."""
    for k in cond:
        if "realized" in k:
            raise SystemExit(f"⛔ calculation_id 에 realized 필드({k})가 들어왔다 — 불변성 위반")
    j = json.dumps(cond, sort_keys=True, ensure_ascii=False)
    return "calc_" + hashlib.sha256(j.encode()).hexdigest()[:16]


def _n_from_atoms(nat, unit_half):
    """원자수 → DP (nat = 2u + (n−2)(u−1), u = 다이머 절반)."""
    n = (nat - 2 * unit_half) // (unit_half - 1) + 2
    return n if 2 * unit_half + (n - 2) * (unit_half - 1) == nat else None


# ══ Stage A — 중성 조립 + Opt 입력 (geometry seed 별) ═══════════════════════════
def stage_a(a, sym, pos):
    if formula_of(sym) != V7C_DIMER_FORMULA and not a.allow_noncanonical:
        raise SystemExit(f"⛔ 입력 다이머 조성 {formula_of(sym)} ≠ v7c({V7C_DIMER_FORMULA}) — "
                         "production 은 fail-closed 다. 합성/시험 입력은 --allow_noncanonical "
                         "(회신 R2 P0-4)")
    if a.n not in REQUIRED_MATRIX:
        raise SystemExit(f"⛔ --n {a.n}: 필수 매트릭스가 정의된 DP 는 {sorted(REQUIRED_MATRIX)} 뿐")
    v7c_real = (formula_of(sym) == V7C_DIMER_FORMULA)
    n_seeds = a.seeds if a.seeds else SEED_FLOOR[a.n][0]
    seeds_meta = []
    for g in range(n_seeds):
        d = os.path.join(a.out, f"gs{g}")
        os.makedirs(d, exist_ok=True)
        csym, cpos, torsions = build_chain(sym, pos, a.n, a.cc, a.step,
                                           log=lambda *x: None, gseed=g)
        if v7c_real and not check_closed_form(csym, a.n, 0):
            raise SystemExit(f"⛔ gs{g}: 중성 {a.n}-량체 닫힌꼴 불일치 — 빌더 오류, 멈춘다")
        tag = f"dp{a.n}_gs{g}_neutral"
        write_xyz(os.path.join(d, f"{tag}.xyz"), csym, cpos,
                  f"DP{a.n} neutral, geometry seed g{g} (torsions "
                  f"{[t['torsion_deg'] for t in torsions]} deg) — UNRELAXED, ORCA Opt 대상")
        make_inp(os.path.join(d, f"{tag}.inp"), f"{tag}.xyz", "RKS", 1, False, "opt_neutral")
        seeds_meta.append(dict(gseed=g, dir=f"gs{g}", tag=tag,
                               torsions=[t["torsion_deg"] for t in torsions]))
        print(f"  gs{g}: torsions {[t['torsion_deg'] for t in torsions]}")
    sha = hashlib.sha256(open(a.dimer, "rb").read()).hexdigest()
    man = {
        "schema": "sdcp_stage0_manifest/v3", "stage": "A",
        "estimand_id": "sdcp-doped-gas-stage0/v3",
        "design_card": "kb/questions/sdcp_doped_reopen_v3_2026_08_28.md",
        "species_note": "DPn_hm_Q0 = neutral-H-deleted / internal-redox microstate "
                        "(H 핵+전자 동시 제거 — 일반적 '탈양성자화' 아님, 회신 R2 조건 1)",
        "dp": a.n, "closed_form_validated": v7c_real,
        "required_matrix": REQUIRED_MATRIX[a.n], "pair_policy": PAIR_POLICY,
        "seed_floor": {"initial_torsion_seeds": SEED_FLOOR[a.n][0],
                       "null_batches_K2": SEED_FLOOR[a.n][1],
                       "rule": "새 저에너지 basin/상태순서/localization class 변화 시 "
                               "null counter 리셋. --step 은 seed 가 아니다 (회신 R2 Q4)"},
        "geometry_seeds": seeds_meta,
        "input_dimer": {"path": os.path.abspath(a.dimer), "sha256": sha},
        "next": "각 gs*/dp*_neutral 을 ORCA 로 Opt → 최종 xyz 로 "
                "`--stage b --neutral_xyz <opt.xyz> --n {n} --gseed <g>` (매트릭스 전건 생성)",
        "abort_codes": list(ABORT_CODES),
    }
    mp = os.path.join(a.out, "manifest_stage_a.json")
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
    print(f"stage A: seed {n_seeds}개 · manifest {mp}")
    return man


# ══ Stage B — 최적화된 중성 부모에서 vertical/adiabatic 매트릭스 생성 ═══════════
def stage_b(a):
    """R⁰ 규약 (회신 R2 P0-2·Q3): 모든 leg 가 **같은 좌표 프레임** —
    h0 = R⁰(=neutral opt) · h1(x) = R⁰−Hx · h2(a,b) = R⁰−Ha−Hb. 추가 이완 없음."""
    csym, cpos = read_xyz(a.neutral_xyz)
    hdr = open(a.neutral_xyz).read().splitlines()[1] if True else ""
    if "ORCA" not in hdr:
        print("  ⚠ 부모 xyz 주석에 ORCA 마커가 없다 — 최적화 완료본이 맞는지 확인할 것 "
              "(R0 규약은 **Opt 된** 부모를 요구한다. 이 도구는 수렴 여부를 검증 못 한다)")
    cnb, crings, csulf = analyze(csym, cpos)
    n = a.n
    if len(crings) != n or len(csulf) != n:
        raise SystemExit(f"⛔ neutral 부모 위상 불일치 (링 {len(crings)}·SO3 {len(csulf)} ≠ {n})")
    v7c_real = check_closed_form(csym, n, 0)
    if not v7c_real and not a.allow_noncanonical:
        raise SystemExit("⛔ neutral 부모가 v7c 닫힌꼴이 아니다 — --allow_noncanonical 은 시험 전용")
    names = ring_chain_names(crings)
    req = REQUIRED_MATRIX[n]
    patterns = ([p.upper() for p in a.patterns] if a.patterns
                else req["singles"] + req["pairs"])
    missing = [p for p in req["singles"] + req["pairs"] if p not in patterns]
    if missing and not a.allow_partial:
        raise SystemExit(f"⛔ 필수 매트릭스 누락 {missing} — 부분 생성은 --allow_partial "
                         "(시험 전용, 재심사 제출물 아님) (회신 R2 조건 3)")
    os.makedirs(a.out, exist_ok=True)
    parent_sha = hashlib.sha256(open(a.neutral_xyz, "rb").read()).hexdigest()
    scf_seeds = ["s0", "s1"][:max(1, a.scf_seeds)]
    jobs = []
    u_pairs = {}
    for pat in patterns:
        hs = resolve_holes(pat, names, csulf)
        letters = "".join(h[0] for h in hs)
        rmH = sorted(h[1] for h in hs)
        m = len(hs)
        vsym, vpos, _ = remove_atoms(csym, cpos, rmH)
        e = electrons_of(vsym)
        if v7c_real and not check_closed_form(vsym, n, m):
            raise SystemExit(f"⛔ h{letters}: 닫힌꼴 불일치 — 멈춘다")
        base = f"dp{n}_gs{a.gseed}_h{letters}"
        write_xyz(os.path.join(a.out, f"{base}.xyz"), vsym, vpos,
                  f"R0 vertical frame: neutral-opt parent minus acid H {rmH} "
                  f"(DP{n}_h{m}_Q0, unrelaxed — 회신 R2 Q3 공통 부모 규약)")
        sectors = SECTORS_ODD if m % 2 == 1 else SECTORS_EVEN
        if m == 2 and PAIR_POLICY.get(pat, "").startswith("U_PCET"):
            u_pairs[pat] = dict(needs_singles=[x.strip() for x in pat.split(",")])
        for sec, wf, mult, nab, bs, label in sectors:
            check_parity(e, mult)
            for jt in ("sp_vertical", "opt_adiabatic"):
                for ss in (scf_seeds if wf != "RKS" else ["s0"]):
                    tag = f"{base}_{sec}_{jt.split('_')[0]}_{ss}"
                    make_inp(os.path.join(a.out, f"{tag}.inp"), f"{base}.xyz",
                             wf, mult, bs, jt, scf_seed=ss)
                    cond = dict(estimand_id="sdcp-doped-gas-stage0/v3", dp=n,
                                species=f"DP{n}_h{m}_Q0", pattern=pat,
                                removed_H_indices=rmH, sector=sec,
                                wavefunction_class=wf, orca_mult=mult,
                                n_alpha_minus_beta=nab, net_charge=0,
                                all_electron_count=e, job_type=jt,
                                geometry_seed=f"g{a.gseed}", scf_seed=ss,
                                parent_neutral_sha256=parent_sha,
                                method="r2SCAN-3c/TightSCF")
                    jobs.append(dict(tag=tag, calculation_id=calculation_id(cond),
                                     conditioning=cond, formula=formula_of(vsym),
                                     n_atoms=len(vsym), sector_label=label,
                                     seeded_separation=(abs(ord(letters[0]) - ord(letters[1]))
                                                        if m == 2 else None),
                                     expected=dict(
                                         hf_type=("RHF" if wf == "RKS" else "UHF"),
                                         s2_target=(0.75 if sec == "d" else
                                                    2.0 if sec == "t" else
                                                    None if sec == "s" else "report_required"),
                                     ),
                                     realized=None))
    # U_PCET 완전성: 쌍이 요구하는 singles 가 매트릭스에 있는가 (없으면 실패)
    for pat, u in u_pairs.items():
        for sng in u["needs_singles"]:
            if sng not in patterns:
                raise SystemExit(f"⛔ U_PCET({pat}) 에 필요한 single h{sng} 가 매트릭스에 없다")
    man = {
        "schema": "sdcp_stage0_manifest/v3", "stage": "B",
        "estimand_id": "sdcp-doped-gas-stage0/v3",
        "design_card": "kb/questions/sdcp_doped_reopen_v3_2026_08_28.md",
        "dp": n, "geometry_seed": f"g{a.gseed}",
        "parent_neutral": {"path": os.path.abspath(a.neutral_xyz), "sha256": parent_sha,
                           "h0_energy_source": "이 부모의 ORCA Opt FINAL SINGLE POINT ENERGY "
                                               "(= 같은 프레임의 h0 leg — 별도 잡 불필요)"},
        "closed_form_validated": v7c_real,
        "required_matrix": req, "generated_patterns": patterns,
        "partial": bool(missing), "pair_policy": PAIR_POLICY,
        "delta_definitions": {
            "U_PCET_vert(a,b)": "E_sp[h2(a,b);R0] + E[h0;R0] − E_sp[h1(a);R0] − E_sp[h1(b);R0]",
            "U_PCET_ad(a,b)": "각 leg 를 각자 최적화한 최소점 에너지로 — vertical 과 **혼합 금지**",
            "⛔": "핵 조성이 함께 변하므로 순수 Hubbard U/hole-pairing 이 아니다 — "
                 "disproportionation/PCET 에너지로만 부른다 (회신 R2 조건 3·7). "
                 "순수 pairing 은 동일 h2 조성 안의 sector 에너지차로 별도 판정",
        },
        "atom_sets_neutral_frame": atom_sets_of(csym, cnb, crings, csulf, names),
        "⚠_atom_sets": "중성 프레임 인덱스 — doped 잡은 removed_H_indices 만큼 밀린다 "
                       "(재매핑·검증은 analyzer)",
        "stage0_observable": "carrier_localization_profile (기체상 retention 은 자명 — 측정 불가)",
        "abort_codes": list(ABORT_CODES),
        "jobs": jobs,
        "runner_rule": "opt_adiabatic 은 같은 (pattern, sector) 의 sp_vertical 이 "
                       "analyzer 게이트(stability·sector)를 통과한 뒤에만 실행한다",
    }
    mp = os.path.join(a.out, "manifest_stage_b.json")
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
    print(f"stage B: 패턴 {len(patterns)} · 잡 {len(jobs)} · manifest {mp}")
    return man


# ══ Analyzer — abort code 를 실제로 emit (회신 R2 조건 5) ═══════════════════════
def analyze_out(text, job):
    """ORCA .out 텍스트 + manifest 잡 → (status, [codes], realized).

    ⛔ 못 하는 것: localization profile 산출(집합별 스핀 적분)은 아직 없다 —
    여기는 **게이트**(수렴·섹터·오염·안정성)까지. 프로파일은 후속 도구.
    """
    codes = []
    realized = {}
    if "ORCA TERMINATED NORMALLY" not in text:
        return "FAIL", ["SCF_UNCONVERGED"], realized
    m = re.search(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", text)
    if m:
        realized["energy_Eh"] = float(m.group(1))
    hf = re.search(r"Hartree-Fock type\s+HFTyp\s*\.+\s*(\w+)", text)
    realized["hf_type"] = hf.group(1) if hf else None
    exp = job["expected"]
    if realized["hf_type"] and exp["hf_type"] not in realized["hf_type"]:
        codes.append("SECTOR_MISMATCH")
    s2 = re.search(r"<S\*\*2>\s*:?\s*(-?\d+\.\d+)", text)
    realized["s2"] = float(s2.group(1)) if s2 else None
    tgt = exp["s2_target"]
    sec = job["conditioning"]["sector"]
    if sec == "bs":
        if realized["s2"] is None:
            codes.append("SPIN_CONTAMINATION_UNREPORTED")
        elif realized["s2"] < 0.2:
            codes.append("NA_STATE_NOT_IDENTIFIED")   # 플립 실패 — closed 로 붕괴
    elif isinstance(tgt, float):
        if realized["s2"] is None or abs(realized["s2"] - tgt) > 0.4:
            codes.append("SECTOR_MISMATCH")
    if job["conditioning"]["job_type"] == "sp_vertical" and sec != "bs":
        if re.search(r"[Ss]tability [Aa]nalysis.*unstable", text):
            codes.append("STABILITY_UNSTABLE")
    if not codes:
        rid = hashlib.sha256((job["calculation_id"]
                              + json.dumps(realized, sort_keys=True)).encode()).hexdigest()[:16]
        realized["realized_state_id"] = "real_" + rid
        return "OK", [], realized
    return "GATED", codes, realized


def analyze_dir(a):
    man = json.load(open(os.path.join(a.analyze, "manifest_stage_b.json")))
    out = {"schema": "sdcp_stage0_analysis/v1", "jobs": {}, "emitted": {}}
    bad = 0
    for job in man["jobs"]:
        op = os.path.join(a.analyze, job["tag"] + ".out")
        if not os.path.isfile(op):
            out["jobs"][job["tag"]] = {"status": "PENDING"}
            continue
        st, codes, realized = analyze_out(open(op, errors="ignore").read(), job)
        out["jobs"][job["tag"]] = {"status": st, "codes": codes, "realized": realized}
        for c in codes:
            out["emitted"].setdefault(c, []).append(job["tag"])
        if st != "OK":
            bad += 1
    ap = os.path.join(a.analyze, "analysis_stage_b.json")
    json.dump(out, open(ap, "w"), ensure_ascii=False, indent=1)
    for c, tags in out["emitted"].items():
        print(f"  ⛔ {c}: {len(tags)}잡 — {tags[:3]}")
    print(f"analyzer: {ap} · 게이트 걸림 {bad}")
    return 2 if bad else 0


def hybrid_select(analysis, window_eh=0.10 / 27.2114):
    """hybrid decision set (회신 R2 조건 8): vertical/adiabatic 승자 + 창 이내 +
    **realized localization class 별 최저 대표 전부**."""
    ok = {t: r for t, r in analysis["jobs"].items()
          if r.get("status") == "OK" and "energy_Eh" in r.get("realized", {})}
    if not ok:
        return []
    pick = set()
    for jt in ("sp", "opt"):
        grp = {t: r for t, r in ok.items() if f"_{jt}_" in t}
        if not grp:
            continue
        emin = min(r["realized"]["energy_Eh"] for r in grp.values())
        for t, r in grp.items():
            if r["realized"]["energy_Eh"] <= emin + window_eh:
                pick.add(t)
    by_class = {}
    for t, r in ok.items():
        cls = r["realized"].get("localization_class")
        if cls:
            cur = by_class.get(cls)
            if cur is None or r["realized"]["energy_Eh"] < ok[cur]["realized"]["energy_Eh"]:
                by_class[cls] = t
    pick |= set(by_class.values())
    return sorted(pick)


# ---------- 레거시 트라이머 경로 (종전 출력과 동일) ----------
def build_legacy_trimer(a, sym, pos):
    csym, cpos, torsions = build_chain(sym, pos, 3, a.cc, a.step)
    th = torsions[0]["torsion_deg"]
    dmin = torsions[0]["dmin_A"]
    write_xyz(os.path.join(a.out, "trimer_neutral.xyz"), csym, cpos,
              f"v7c trimer (built from relaxed dimer; torsion {th} deg, dmin {dmin:.2f} A)")

    tnb, trings, tsulf = analyze(csym, cpos)
    assert len(trings) == 3 and len(tsulf) == 3, "트라이머: 링 3 + 설포네이트 3이어야 함"
    names = ring_chain_names(trings)
    print("링 판정:", {names[i]: f"S{trings[i]['rS']}" for i in range(3)})

    groups_n, acidH = {}, {}
    for su in tsulf:
        nm = names[su["ring"]]
        groups_n[f"{nm}_SO3"] = sorted([su["sS"]] + su["sO"])
        groups_n[f"{nm}_ring"] = sorted(trings[su["ring"]]["ring"])
        assert su["aH"] is not None, f"{nm} 설포네이트에 산성 H 없음"
        acidH[nm] = su["aH"]
    print("산성 H (neutral 기준):", acidH)

    variants = {"trimer_doped_mid": acidH["B"], "trimer_doped_end": acidH["A"]}
    groups_all = {"neutral": groups_n}
    for tag, k in variants.items():
        vsym, vpos, remap = remove_atoms(csym, cpos, [k])
        write_xyz(os.path.join(a.out, f"{tag}.xyz"), vsym, vpos,
                  f"{tag}: trimer_neutral minus acid H{k} (charge 0, doublet)")
        groups_all[tag] = {g: [remap(i) for i in idx if i != k]
                           for g, idx in groups_n.items()}
    groups_all["acidH"] = variants
    groups_all["dimer_ref"] = "doped: A_SO3 62.3 / A_ring 17.4 / B_SO3 0.0 / B_ring 15.2 / rest 5.0 %"
    groups_all["monomer_ref"] = "doped: O3 ~65% / backbone ~35%"
    json.dump(groups_all, open(os.path.join(a.out, "groups_trimer.json"), "w"), indent=1)

    for tag, mult in (("trimer_neutral", 1), ("trimer_doped_mid", 2), ("trimer_doped_end", 2)):
        with open(os.path.join(a.out, f"{tag}.inp"), "w") as f:
            f.write(f"! r2SCAN-3c Opt TightSCF\n%maxcore 6000\n* xyzfile 0 {mult} {tag}.xyz\n")

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




# ---------- selftest ----------
def _synthetic_unit():
    """티오펜-SO3H 흉내 유닛 (13원자). analyze() 의 위상 요구를 전부 만족하는 합성 기하.

    ring: S + C4 (정오각형, 변 1.45) · α-C 2개에 H · β-C 하나에 스페이서 C → SO3H
    인덱스: 0 S · 1 Ca1 · 2 Cb1 · 3 Cb2 · 4 Ca2 · 5 H(Ca1) · 6 H(Ca2) · 7 H(Cb1) ·
            8 Csp · 9 Ssulf · 10-12 O · 13 산성H  (14원자 — 전자 90, 짝수)
    """
    R = 1.45 / (2 * math.sin(math.pi / 5))
    ang = [90, 162, 234, 306, 18]                        # S, Ca1, Cb1, Cb2, Ca2
    ring = [[R * math.cos(math.radians(t)), R * math.sin(math.radians(t)), 0.0]
            for t in ang]
    sym = ["S", "C", "C", "C", "C"]
    pos = list(ring)
    for k in (1, 4):                                     # α-H (radially outward)
        u = unit(ring[k])
        sym.append("H")
        pos.append(add(ring[k], scal(u, 1.09)))
    u2 = unit(ring[2])                                   # Cb1-H — 전자수 짝수 맞춤 (중성 singlet)
    sym.append("H")
    pos.append(add(ring[2], scal(u2, 1.09)))
    u = unit(ring[3])                                    # Cb2 → 스페이서
    csp = add(ring[3], scal(u, 1.50))
    ss = add(csp, scal(u, 1.77))
    sym += ["C", "S"]
    pos += [csp, ss]
    perp = [0.0, 0.0, 1.0]
    side = unit(cross(u, perp))
    for kv in (scal(perp, 1.0), add(scal(perp, -0.5), scal(side, 0.86)),
               add(scal(perp, -0.5), scal(side, -0.86))):
        sym.append("O")
        pos.append(add(ss, scal(unit(add(scal(u, 0.6), kv)), 1.45)))
    sym.append("H")                                       # 산성 H (첫 O 에)
    pos.append(add(pos[-3], scal(unit(sub(pos[-3], ss)), 0.97)))
    return sym, pos


def _synthetic_dimer():
    """유닛 2개를 α–α' 1.45 Å 로 접합한 합성 다이머 (26원자, 전자 178 짝수).

    B 유닛 = A 유닛을 새 결합 중점에 대해 **점반전**한 사본 (거리 보존 → 위상 유지)."""
    s1, p1 = _synthetic_unit()
    d = unit(sub(p1[6], p1[4]))
    target = add(p1[4], scal(d, 1.45))
    M = scal(add(p1[4], target), 0.5)
    p2 = [sub(scal(M, 2.0), p) for p in p1]
    sym = [x for i, x in enumerate(s1) if i != 6] + [x for i, x in enumerate(s1) if i != 6]
    pos = [x for i, x in enumerate(p1) if i != 6] + [x for i, x in enumerate(p2) if i != 6]
    return sym, pos


def _fake_orca_out(terminated=True, energy=-100.0, hf="UHF", s2=0.75, stable=True):
    t = "                                 * O   R   C   A *\n"
    t += f" Hartree-Fock type      HFTyp           .... {hf}\n"
    if s2 is not None:
        t += f" Expectation value of <S**2>     :     {s2:.6f}\n"
    if not stable:
        t += " Stability analysis indicates an unstable RHF/RKS wavefunction\n"
    else:
        t += " Stability analysis indicates a stable HF/KS wavefunction\n"
    t += f" FINAL SINGLE POINT ENERGY      {energy:.9f}\n"
    if terminated:
        t += "                             ****ORCA TERMINATED NORMALLY****\n"
    return t


def selftest():
    import tempfile
    fails = []

    def chk(ok, msg):
        print(("  ✓ " if ok else "  ✗ ") + msg)
        if not ok:
            fails.append(msg)

    print("── build_v7c_trimer selftest (stage 아키텍처 v3) ──")
    sym, pos = _synthetic_dimer()
    nb, rings, sulf = analyze(sym, pos)
    chk(len(sym) == 26 and len(rings) == 2 and len(sulf) == 2,
        f"합성 다이머 위상 (원자 {len(sym)} · 링 {len(rings)} · SO3 {len(sulf)})")

    with tempfile.TemporaryDirectory() as td:
        dim = os.path.join(td, "dimer.xyz")
        write_xyz(dim, sym, pos, "synthetic dimer for selftest")

        # ── ⛔ 음성 (R2 P0-4): 비정본 다이머는 플래그 없이 멈춘다 (production fail-closed)
        aX = argparse.Namespace(dimer=dim, out=os.path.join(td, "x"), cc=CC_NEW, step=30,
                                n=3, seeds=1, allow_noncanonical=False)
        try:
            stage_a(aX, sym, pos)
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "음성: 비정본 다이머 + 플래그 없음 → stage A 거부 (fail-closed)")

        # ── stage A (합성, 시험 플래그) — seed 2개 독립성
        aA = argparse.Namespace(dimer=dim, out=os.path.join(td, "a3"), cc=CC_NEW, step=30,
                                n=3, seeds=2, allow_noncanonical=True)
        manA = stage_a(aA, sym, pos)
        chk(manA["schema"].endswith("/v3") and manA["estimand_id"].endswith("/v3")
            and "v3_2026_08_28" in manA["design_card"],
            "manifest provenance = v3 (R2 P0-6)")
        t0, t1 = manA["geometry_seeds"][0]["torsions"], manA["geometry_seeds"][1]["torsions"]
        chk(t0 != t1, f"geometry seed 독립성: g0 {t0} ≠ g1 {t1}")
        inpA = open(os.path.join(aA.out, "gs0", "dp3_gs0_neutral.inp")).read()
        chk(inpA.startswith("! RKS") and " Opt " in inpA,
            "neutral 입력 = RKS Opt (R2 P0-1: UKS 전면 오생성 수정)")

        # ── stage B (합성 n=3): '최적화된 부모' 대신 stage A 기하 재사용 (시험)
        parent = os.path.join(aA.out, "gs0", "dp3_gs0_neutral.xyz")
        aB = argparse.Namespace(neutral_xyz=parent, out=os.path.join(td, "b3"), n=3,
                                gseed=0, patterns=None, allow_partial=False,
                                allow_noncanonical=True, scf_seeds=2)
        manB = stage_b(aB)
        tags = [j["tag"] for j in manB["jobs"]]
        chk(any("_hA_" in t for t in tags) and any("_hB_" in t for t in tags),
            "n=3 필수 매트릭스 (hA end · hB middle) 전건 생성")
        sp = open(os.path.join(aB.out, "dp3_gs0_hA_d_sp_s0.inp")).read()
        op = open(os.path.join(aB.out, "dp3_gs0_hA_d_opt_s0.inp")).read()
        chk("Opt" not in sp and "StabPerform" in sp and sp.startswith("! UKS"),
            "sp_vertical = UKS SP + StabPerform (Opt 없음)")
        chk(" Opt " in op and "StabPerform" not in op,
            "opt_adiabatic = Opt (stability 게이트는 runner_rule 로 분리)")
        s1i = open(os.path.join(aB.out, "dp3_gs0_hA_d_sp_s1.inp")).read()
        chk("Guess Hueckel" in s1i, "SCF seed s1 = Hueckel (geometry seed 와 분리 관리)")

        # ── ⛔ 음성 (R2 조건 3): 매트릭스 부분 생성은 기본 거부
        aP = argparse.Namespace(neutral_xyz=parent, out=os.path.join(td, "p3"), n=3,
                                gseed=0, patterns=["B"], allow_partial=False,
                                allow_noncanonical=True, scf_seeds=1)
        try:
            stage_b(aP)
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "음성: --patterns 부분 지정 + allow_partial 없음 → 생성 실패 (fail-open 봉쇄)")

        # ── stage A/B (합성 n=6): 섹터·매트릭스·U_PCET 완전성
        a6 = argparse.Namespace(dimer=dim, out=os.path.join(td, "a6"), cc=CC_NEW, step=45,
                                n=6, seeds=1, allow_noncanonical=True)
        stage_a(a6, sym, pos)
        parent6 = os.path.join(a6.out, "gs0", "dp6_gs0_neutral.xyz")
        b6 = argparse.Namespace(neutral_xyz=parent6, out=os.path.join(td, "b6"), n=6,
                                gseed=0, patterns=None, allow_partial=False,
                                allow_noncanonical=True, scf_seeds=1)
        man6 = stage_b(b6)
        pats = set(man6["generated_patterns"])
        chk(pats == {"B", "C", "D", "E", "C,D", "B,E", "A,F", "B,C"},
            f"n=6 매트릭스: singles 4 + pairs 4 (off-center B,C 포함) — {sorted(pats)}")
        s_inp = open(os.path.join(b6.out, "dp6_gs0_hCD_s_sp_s0.inp")).read()
        bs_inp = open(os.path.join(b6.out, "dp6_gs0_hCD_bs_sp_s0.inp")).read()
        chk(s_inp.startswith("! RKS") and "Opt" not in s_inp,
            "h2 closed-shell 후보 = **RKS** SP (R2 P0-1 핵심 수정)")
        chk(bs_inp.startswith("! UKS") and "BrokenSym 1,1" in bs_inp and " 0 3 " in bs_inp,
            "bs = UKS mult3 + BrokenSym (StabPerform 은 bs 에 안 붙임)")
        chk(man6["pair_policy"]["A,F"].startswith("sector_comparison_only"),
            "A,F 쌍 = 섹터 비교 전용 (U·거리추세 주장 금지 — R2 Q2)")
        mtxt = json.dumps(man6, ensure_ascii=False)
        chk("bipolaron" not in mtxt and "backbone hole" not in mtxt,
            "conditioning 순수성 유지 (polaron/bipolaron 라벨 없음)")

        # ── calculation_id 불변성 (R2 조건 8)
        j0 = man6["jobs"][0]
        cid_again = calculation_id(j0["conditioning"])
        chk(cid_again == j0["calculation_id"] and j0["realized"] is None,
            "calculation_id 재계산 동일 + realized 는 ID 밖 (immutable)")
        try:
            calculation_id({"a": 1, "realized_localization": "x"})
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "음성: conditioning 에 realized 필드가 섞이면 ID 발급 거부")

        # ── analyzer e2e (R2 조건 5) — 음성 4종 + 양성 1종
        job_t = next(j for j in man6["jobs"] if j["conditioning"]["sector"] == "t"
                     and j["conditioning"]["job_type"] == "sp_vertical")
        job_s = next(j for j in man6["jobs"] if j["conditioning"]["sector"] == "s"
                     and j["conditioning"]["job_type"] == "sp_vertical")
        job_bs = next(j for j in man6["jobs"] if j["conditioning"]["sector"] == "bs"
                      and j["conditioning"]["job_type"] == "sp_vertical")
        st, c, _ = analyze_out(_fake_orca_out(terminated=False), job_t)
        chk("SCF_UNCONVERGED" in c, "analyzer 음성①: 미종료 → SCF_UNCONVERGED emit")
        st, c, _ = analyze_out(_fake_orca_out(hf="UHF", s2=0.76), job_t)
        chk("SECTOR_MISMATCH" in c, "analyzer 음성②: triplet 기대인데 <S2>=0.76 → SECTOR_MISMATCH")
        st, c, _ = analyze_out(_fake_orca_out(hf="UHF", s2=None), job_bs)
        chk("SPIN_CONTAMINATION_UNREPORTED" in c,
            "analyzer 음성③: bs 인데 <S2> 미보고 → SPIN_CONTAMINATION_UNREPORTED")
        st, c, _ = analyze_out(_fake_orca_out(hf="UHF", s2=0.0), job_s)
        chk("SECTOR_MISMATCH" in c, "analyzer 음성④: RKS 요청인데 UHF 로 돎 → SECTOR_MISMATCH")
        st, c, r = analyze_out(_fake_orca_out(hf="UHF", s2=2.003), job_t)
        chk(st == "OK" and r["realized_state_id"].startswith("real_"),
            "analyzer 양성: 정상 triplet → OK + realized_state_id 발급 (calc_id 와 분리)")
        st, c, _ = analyze_out(_fake_orca_out(hf="UHF", s2=2.0, stable=False), job_t)
        chk("STABILITY_UNSTABLE" in c, "analyzer: 불안정 파동함수 → STABILITY_UNSTABLE (opt 차단 마크)")

        # ── hybrid decision set (R2 조건 8): class 대표 포함
        fake = {"jobs": {
            "x_sp_a": {"status": "OK", "realized": {"energy_Eh": -10.000, "localization_class": "L1"}},
            "x_sp_b": {"status": "OK", "realized": {"energy_Eh": -9.900, "localization_class": "L2"}},
            "x_sp_c": {"status": "OK", "realized": {"energy_Eh": -9.500, "localization_class": "L3"}},
        }}
        pick = hybrid_select(fake)
        chk(set(pick) == {"x_sp_a", "x_sp_b", "x_sp_c"},
            "hybrid decision set: 승자+창 이내 + **모든 localization class 대표** 포함")

        # ── 실물 다이머 (repo) — 닫힌꼴 stage A e2e
        rd = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "db", "structures", "sdcp_v7c_dimer_neutral.xyz")
        if os.path.isfile(rd):
            rs, rp = read_xyz(rd)
            aR = argparse.Namespace(dimer=rd, out=os.path.join(td, "r3"), cc=CC_NEW,
                                    step=60, n=3, seeds=1, allow_noncanonical=False)
            mR = stage_a(aR, rs, rp)
            chk(mR["closed_form_validated"] is True,
                "실물 다이머: 닫힌꼴 검증 통과 (플래그 불필요 — 정본 경로)")
        else:
            print("  (실물 다이머 없음 — 닫힌꼴 실검증 생략)")
        chk(not check_closed_form(["C"] * 33, 3, 1), "음성: 닫힌꼴 함수가 틀린 조성 거부")

        # ── 레거시 경로 하위호환
        aL = argparse.Namespace(dimer=dim, out=os.path.join(td, "leg"), cc=CC_NEW, step=30)
        os.makedirs(aL.out)
        build_legacy_trimer(aL, sym, pos)
        need = ["trimer_neutral.xyz", "trimer_doped_mid.xyz", "trimer_doped_end.xyz",
                "groups_trimer.json", "run_trimer.sh", "analyze_trimer_spin.py"]
        chk(all(os.path.exists(os.path.join(aL.out, f)) for f in need),
            "레거시 트라이머 출력 세트 전부 생성 (하위호환)")

    print(f"── {'PASS' if not fails else 'FAIL ' + str(len(fails))} ──")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dimer", help="이완된 dimer_neutral.xyz (v7c 실물 68원자)")
    ap.add_argument("--out")
    ap.add_argument("--cc", type=float, default=CC_NEW)
    ap.add_argument("--step", type=int, default=10, help="비틀림각 스캔 간격(도) — seed 아님")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--stage", choices=["a", "b"],
                    help="a: 중성 조립+Opt 입력 (seed 별) · b: 최적화된 부모에서 매트릭스 생성")
    ap.add_argument("--seeds", type=int, default=0,
                    help="stage a 의 geometry seed 수 (기본 SEED_FLOOR — R2 Q4 바닥)")
    ap.add_argument("--neutral_xyz", help="stage b: ORCA 최적화 완료된 중성 부모 xyz")
    ap.add_argument("--gseed", type=int, default=0, help="stage b: 이 부모의 geometry seed 번호")
    ap.add_argument("--scf_seeds", type=int, default=2,
                    help="stage b: 열린 껍질 잡의 독립 SCF seed 수 (s0 기본 · s1 Hueckel)")
    ap.add_argument("--patterns", action="append",
                    help="stage b 부분 생성 (⚠ --allow_partial 필수 — 시험 전용)")
    ap.add_argument("--allow_partial", action="store_true",
                    help="필수 매트릭스 미달 허용 — **재심사 제출물에는 금지** (시험 전용)")
    ap.add_argument("--allow_noncanonical", action="store_true",
                    help="비정본 다이머 허용 — selftest/합성 전용 (production 은 fail-closed)")
    ap.add_argument("--analyze", help="stage b 출력 디렉터리 — .out 게이트 + abort code emit")
    ap.add_argument("--holes", action="append", help="(구 v2 인터페이스 — 제거됨)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.analyze:
        return analyze_dir(a)
    if a.holes:
        ap.error("--holes 는 v2 인터페이스다 — 회신 R2 로 제거됐다. --stage a → (ORCA Opt) → "
                 "--stage b 를 쓴다 (매트릭스는 REQUIRED_MATRIX 가 강제)")
    if a.stage == "a":
        if not (a.dimer and a.out):
            ap.error("--stage a 는 --dimer 와 --out 이 필요하다")
        sym, pos = read_xyz(a.dimer)
        stage_a(a, sym, pos)
        return 0
    if a.stage == "b":
        if not (a.neutral_xyz and a.out):
            ap.error("--stage b 는 --neutral_xyz 와 --out 이 필요하다")
        stage_b(a)
        return 0
    # 레거시 트라이머 (하위호환)
    if not (a.dimer and a.out):
        ap.error("--dimer/--out (레거시) 또는 --stage/--selftest/--analyze 중 하나가 필요하다")
    sym, pos = read_xyz(a.dimer)
    if len(sym) != 68:
        print(f"⚠ 다이머 {len(sym)}원자 — v7c 실물(68)이 아니다. 합성/시험 입력으로 간주하고 진행")
    build_legacy_trimer(a, sym, pos)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
