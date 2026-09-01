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
      --out ~/orca_poly/dp6_v3 --n 6                    # seed 수·고유성·dmin 바닥 강제
  # (ORCA 로 gs*/dp6_gs*_neutral 최적화 후 — receipt 3종이 전부 있어야 stage b 가 열린다)
  python3 build_v7c_trimer.py --stage b --n 6 --gseed 0 \
      --stage_a_manifest ~/orca_poly/dp6_v3/manifest_stage_a.json \
      --neutral_out ~/orca_poly/dp6_v3/gs0/dp6_gs0_neutral.out \
      --neutral_xyz ~/orca_poly/dp6_v3/gs0/dp6_gs0_neutral.xyz --out ~/orca_poly/dp6_v3/gs0_b
  python3 build_v7c_trimer.py --analyze ~/orca_poly/dp6_v3/gs0_b     # PENDING 도 비영 종료
  python3 build_v7c_trimer.py --hybrid  ~/orca_poly/dp6_v3/gs0_b     # NoAutoStart 강제
  python3 build_v7c_trimer.py --legacy --dimer ... --out trimer      # 레거시는 명시 필수

레거시 (--legacy --dimer/--out): trimer_neutral / doped_mid / doped_end 패키지 (명시 필수 — R3 P1).
⚠ v2 인터페이스(--holes)는 제거 — 매트릭스는 REQUIRED_MATRIX 가 강제한다.
⚠ 회신 R3 반영 (2026-08-28): seed 바닥·고유성·dmin **강제** · 부모 **receipt**(manifest+
  .out+xyz 3중 결속, 미이완/재라벨 거부) · SP→Opt **dependency**(calculation_id) ·
  analyzer 양성증거 요구(마지막 segment·마지막 값·중복 out 적발·PENDING 비영 종료) ·
  입력에 Hirshfeld(+UNO/UCO) 관측량 계약 · hybrid NoAutoStart + 조성별 그룹 ·
  localization class 사전 규칙(share ≥ 0.5 유일 집합, 아니면 MIXED_UNRESOLVED).

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
import time
from pathlib import Path

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


class SteticClash(Exception):
    """자격(dmin ≥ DMIN_FLOOR)을 만족하는 접합각이 하나도 없다 → 그 seed 를 폐기한다.

    회신 R4 P0-1 대응. 종전에는 `or cands[:1]` 로 충돌 구조를 조용히 채택했고,
    stage_a 의 사후 dmin 검사에 **우연히** 걸리는 데 의존했다.
    """


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
    # 회신 R4 P0-1: `or cands[:1]` 폴백은 **문서와 다른 fail-open** 이었다 —
    # 자격 후보가 하나도 없으면 최상위(=여전히 충돌)를 조용히 채택했다.
    # 이제 두 경로 모두 fail-closed: 자격 미달이면 SteticClash 로 이 seed 를 폐기시킨다.
    ok = [c for c in cands if c[0] >= DMIN_FLOOR]
    if not ok:
        raise SteticClash(
            f"접합 후보 {len(cands)}개 전부 dmin < {DMIN_FLOOR} Å "
            f"(최선 {cands[0][0]:.3f} Å, gseed={gseed} gidx={gidx}) — 이 seed 는 폐기한다")
    if gseed == 0:
        dmin, th, npos = ok[0]                      # 종전과 동일: 자격 후보 중 max-dmin
    else:
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
    # 회신 R4 보완 3 — `backbone` 하나로는 **어느 ring 의 polaron 인지 구별 못 한다.**
    #   ring 별 집합을 따로 낸다. (합집합인 `backbone` 도 하위호환으로 남긴다 —
    #   share 합이 1 을 넘게 되므로 소비 쪽은 `_` 로 시작하지 않는 키만 골라 쓴다.)
    for ri, r in enumerate(crings):
        ra = set(r["ring"])
        rh = {h for i in ra for h in cnb[i] if csym[h] == "H"}
        sets[f"ring{ri}_{names[ri]}" if ri < len(names) else f"ring{ri}"] = sorted(ra | rh)
    used = set(sets["backbone"])
    for su in csulf:
        grp = sorted([su["sS"]] + su["sO"] + ([su["aH"]] if su["aH"] is not None else []))
        sets[f"sulfonate_{names[su['ring']]}"] = grp
        used |= set(grp)
    sets["sidechain_rest"] = sorted(set(range(len(csym))) - used)
    return sets


#: 교차검사 방법 — "ωB97X-D급" 금지 (회신 R 조건 7): 계산 전에 정확히 지정한다.
#:   ⚠ 회신 R3: 'MORead 금지' 주석은 강제가 아니다 — ORCA 는 같은 basename 의 GBW 가
#:   있으면 AutoStart 한다. **NoAutoStart 키워드**로만 fresh-start 가 강제된다.
HYBRID_KEYWORDS = "wB97X-D3 def2-TZVP defGrid3"
HYBRID_SPEC = {
    "keywords": HYBRID_KEYWORDS + " NoAutoStart",
    "fresh_start": "NoAutoStart 키워드로 강제 (주석은 강제가 아니다 — 회신 R3 P0-5)",
    "decision_set": "**같은 조성(species)·같은 job_type 그룹 안에서만** vertical 승자 ∪ "
                    "adiabatic 승자 ∪ 0.10 eV 창 ∪ realized localization class 별 최저 대표"
                    " — 핵·전자수가 다른 종의 절대에너지 비교는 물리적으로 무의미 (R3 P0-5)",
    "escalation": "hybrid 가 state identity/localization/순서를 바꾸면 그 상태만 hybrid 재최적화",
    "disagreement": "두 방법이 갈리면 평균하지 않고 METHOD_DEPENDENT (--compare 가 emit)",
    "version_field": "orca_version 은 회수 시 .out 배너에서 채운다 (사전 기재 금지)",
}

#: localization class 의 **사전 규칙** (회신 R3: 결과를 본 뒤 경계를 정하면 사후 선택이다).
#:   share(g) = Σ_{i∈g} m_i (signed) / Σ_i |m_i|  — 분모는 전 원자 |국소스핀| 합.
#:   |share| ≥ LOC_CLASS_MIN 인 집합이 정확히 하나면 그 집합 라벨, 아니면 MIXED_UNRESOLVED.
#:   총 |m| < LOC_ABS_MIN 이면 NO_SPIN (closed-shell 류) — class 없음.
LOC_CLASS_MIN = 0.5
LOC_ABS_MIN = 0.3


def _git_commit():
    try:
        import subprocess
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                              text=True, timeout=10).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def make_inp(path, xyz_name, wf, mult, bs, job_type, scf_seed="s0", hybrid=False):
    """job type 별 ORCA 입력 (회신 R2 P0-1·R3 P0-0 — 관측량 회수 계약 포함).

    - RKS/UKS 명시 · SP/Opt 분리 (R2)
    - **Hirshfeld 를 전 잡에**, open-shell 에 **UNO UCO** (R3: 기본 off — 명시 없으면
      Löwdin–Hirshfeld 강건성·UNO 지표를 실행 후 복구할 수 없다)
    - hybrid 는 **NoAutoStart** 로 fresh-start 강제 (R3: 주석은 강제가 아니다)
    """
    kw = "RKS" if wf == "RKS" else "UKS"
    base = (HYBRID_KEYWORDS + " NoAutoStart") if hybrid else "r2SCAN-3c"
    opt = " Opt" if job_type in ("opt_neutral", "opt_adiabatic") else ""
    obs = " Hirshfeld" + ("" if wf == "RKS" else " UNO UCO")
    method = f"{base}{opt} TightSCF{obs}"
    scf_opts = []
    if job_type == "sp_vertical" and not bs:
        scf_opts.append("StabPerform true")
    if bs:
        scf_opts.append("BrokenSym 1,1")
    if scf_seed == "s1":
        scf_opts.append("Guess Hueckel")
    with open(path, "w") as f:
        f.write(f"! {kw} {method}\n%maxcore 6000\n")
        if scf_opts:
            f.write("%scf " + " ".join(scf_opts) + " end\n")
        f.write(f"* xyzfile 0 {mult} {xyz_name}\n")


def _no_realized(d, path="conditioning"):
    for k, v in d.items():
        if "realized" in str(k):
            raise SystemExit(f"⛔ calculation_id 에 realized 필드({path}.{k}) — 불변성 위반")
        if isinstance(v, dict):
            _no_realized(v, f"{path}.{k}")


def calculation_id(cond):
    """불변 계산 ID — conditioning 만 해시. **중첩 포함** realized 유입 시 발급 거부 (R3 P1)."""
    _no_realized(cond)
    j = json.dumps(cond, sort_keys=True, ensure_ascii=False)
    return "calc_" + hashlib.sha256(j.encode()).hexdigest()[:16]


# ══ Stage A — 중성 조립 + Opt 입력 (geometry seed 별) ═══════════════════════════
def stage_a(a, sym, pos):
    """회신 R3 P0-1 반영: seed 바닥·고유성·dmin floor 를 **강제**한다 (선언이 아니라).

    - seeds 는 양의 정수, SEED_FLOOR 이상 (--allow_underseed 는 selftest 전용)
    - torsion 벡터가 겹치면 다음 gseed 로 재시도해 **고유 N 개**를 채운다 — 못 채우면 중단
    - 모든 접합의 dmin ≥ DMIN_FLOOR — 위반 시 그 seed 는 폐기, 전체 부족 시 중단
    - 각 접합 dmin 을 manifest 에 기록
    """
    if formula_of(sym) != V7C_DIMER_FORMULA and not a.allow_noncanonical:
        raise SystemExit(f"⛔ 입력 다이머 조성 {formula_of(sym)} ≠ v7c({V7C_DIMER_FORMULA}) — "
                         "production 은 fail-closed (--allow_noncanonical 은 selftest 전용)")
    if a.n not in REQUIRED_MATRIX:
        raise SystemExit(f"⛔ --n {a.n}: 필수 매트릭스가 정의된 DP 는 {sorted(REQUIRED_MATRIX)} 뿐")
    v7c_real = (formula_of(sym) == V7C_DIMER_FORMULA)
    floor = SEED_FLOOR[a.n][0]
    n_seeds = a.seeds if a.seeds is not None else floor
    if not isinstance(n_seeds, int) or n_seeds < 1:
        raise SystemExit(f"⛔ --seeds {a.seeds}: 양의 정수여야 한다")
    if n_seeds < floor and not a.allow_underseed:
        raise SystemExit(f"⛔ --seeds {n_seeds} < 승인 바닥 {floor} (R2 Q4) — "
                         "축소는 --allow_underseed (selftest 전용, 재심사 제출물 아님)")
    commit = _git_commit()
    seeds_meta, seen_vecs = [], set()
    g, tries = 0, 0
    while len(seeds_meta) < n_seeds:
        tries += 1
        if tries > 20 * n_seeds:
            raise SystemExit(f"⛔ 고유 torsion seed {n_seeds}개를 만들 수 없다 "
                             f"(고유 {len(seen_vecs)}개에서 고갈) — --step 을 줄여 후보각을 늘려라")
        try:
            csym, cpos, torsions = build_chain(sym, pos, a.n, a.cc, a.step,
                                               log=lambda *x: None, gseed=g)
        except (SystemExit, SteticClash):
            g += 1
            continue
        vec = tuple(t["torsion_deg"] for t in torsions)
        dmins = [t["dmin_A"] for t in torsions]
        if vec in seen_vecs or min(dmins) < DMIN_FLOOR:
            g += 1
            continue
        seen_vecs.add(vec)
        if v7c_real and not check_closed_form(csym, a.n, 0):
            raise SystemExit(f"⛔ g{g}: 중성 {a.n}-량체 닫힌꼴 불일치 — 빌더 오류, 멈춘다")
        k = len(seeds_meta)
        d = os.path.join(a.out, f"gs{k}")
        os.makedirs(d, exist_ok=True)
        tag = f"dp{a.n}_gs{k}_neutral"
        xyzp = os.path.join(d, f"{tag}.xyz")
        write_xyz(xyzp, csym, cpos,
                  f"DP{a.n} neutral, geometry seed g{k} (lcg {g}; torsions {list(vec)} deg) "
                  "— UNRELAXED, ORCA Opt 대상")
        make_inp(os.path.join(d, f"{tag}.inp"), f"{tag}.xyz", "RKS", 1, False, "opt_neutral")
        cond = dict(estimand_id="sdcp-doped-gas-stage0/v3", dp=a.n,
                    species=f"DP{a.n}_h0_Q0", job_type="opt_neutral",
                    wavefunction_class="RKS", orca_mult=1, net_charge=0,
                    all_electron_count=electrons_of(csym), geometry_seed=f"g{k}",
                    lcg_seed=g, torsions_deg=list(vec), method="r2SCAN-3c/TightSCF",
                    builder_commit=commit)
        seeds_meta.append(dict(gseed=k, lcg_seed=g, dir=f"gs{k}", tag=tag,
                               torsions=list(vec), dmins_A=dmins,
                               xyz_sha256=_sha(xyzp),
                               calculation_id=calculation_id(cond)))
        g += 1
        print(f"  gs{k} (lcg {g-1}): torsions {list(vec)} · dmin {min(dmins):.2f} A")
    man = {
        "schema": "sdcp_stage0_manifest/v3", "stage": "A",
        "estimand_id": "sdcp-doped-gas-stage0/v3",
        "design_card": "kb/questions/sdcp_doped_reopen_v3_2026_08_28.md",
        "builder_commit": commit,
        "species_note": "DPn_hm_Q0 = neutral-H-deleted / internal-redox microstate "
                        "(H 핵+전자 동시 제거 — 일반적 '탈양성자화' 아님)",
        "dp": a.n, "closed_form_validated": v7c_real,
        "dmin_floor_A": DMIN_FLOOR,
        "required_matrix": REQUIRED_MATRIX[a.n], "pair_policy": PAIR_POLICY,
        "seed_floor": {"initial_torsion_seeds": floor,
                       "null_batches_K2": SEED_FLOOR[a.n][1],
                       "generated": len(seeds_meta),
                       "underseed_flag": bool(n_seeds < floor),
                       "rule": "변화 시 null counter 리셋 · --step 은 seed 아님 (R2 Q4)"},
        "geometry_seeds": seeds_meta,
        "input_dimer": {"path": os.path.abspath(a.dimer), "sha256": _sha(a.dimer)},
        "next": "각 gs*/dp*_neutral 을 ORCA Opt → --stage b --stage_a_manifest <이 파일> "
                "--neutral_out <.out> --neutral_xyz <최종.xyz> --gseed <k>",
        "abort_codes": list(ABORT_CODES),
    }
    mp = os.path.join(a.out, "manifest_stage_a.json")
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
    print(f"stage A: 고유 seed {len(seeds_meta)}개 · manifest {mp}")
    return man


# ══ 중성 부모 receipt (회신 R3 P0-2 — 자유문구는 증거가 아니다) ═══════════════════
#: 미이완 판정 문턱 [Å] — Opt 최종구조가 조립본에서 이만큼도 안 움직였으면 이완이 아니다.
#:   회신 R4 P0-2: SHA 비교는 **주석 한 줄**로 깨진다. 좌표로 판정해야 한다.
RELAX_MIN_DISP_A = 1e-3


def _coord_blocks(text, nat):
    """text 의 모든 CARTESIAN COORDINATES (ANGSTROEM) 블록 → [[(el,x,y,z)]*nat].

    ⛔ 못 하는 것: 좌표계 회전·병진을 되돌리지 않는다. ORCA 가 입력 프레임을
      그대로 echo 한다는 전제에 의존한다 (r2SCAN-3c gas-phase 에서는 성립).
    """
    out = []
    for blk in text.split("CARTESIAN COORDINATES (ANGSTROEM)")[1:]:
        rows = []
        for ln in blk.splitlines()[2:2 + nat]:
            t = ln.split()
            if len(t) >= 4:
                try:
                    rows.append((t[0], float(t[1]), float(t[2]), float(t[3])))
                except ValueError:
                    break
        if len(rows) == nat:
            out.append(rows)
    return out


def _max_disp(rows, sym, pos):
    """좌표블록 vs (sym,pos) 의 원소별 최대 변위 [Å]. 원소가 어긋나면 None."""
    if len(rows) != len(sym):
        return None
    d = 0.0
    for k, (el, x, y, z) in enumerate(rows):
        if el != sym[k]:
            return None
        d = max(d, abs(x - pos[k][0]), abs(y - pos[k][1]), abs(z - pos[k][2]))
    return d


def neutral_receipt(a, manA):
    """stage A manifest + ORCA .out + 최종 xyz 를 **묶어서** 검증한다.

    검증 (회신 R4 P0-2 로 ⑤⑥⑦ 추가):
      ① manifest 의 gseed 항목 존재
      ② .out strict decode · 마지막 run segment 정상종료 + **Opt 수렴**
      ③ .out 마지막 좌표블록 == neutral_xyz 좌표 (원자별 1e-4 Å)
      ④ neutral_xyz 가 stage A 조립본에서 **실제로 움직였다** (≥ RELAX_MIN_DISP_A)
         — 종전의 SHA 비교는 주석 한 줄로 우회됐다
      ⑤ **.out 의 시작 좌표블록 == 그 gseed 의 stage A 조립본** (교차-seed 재라벨링 차단)
      ⑥ **HFTyp / Total Charge / Multiplicity 가 중성 RKS 부모와 일치** — 종전에는
         UHF·charge +1·doublet 출력도 통과했다
      ⑦ stage A 조립본 xyz 가 **없으면 거부** (종전에는 조용히 검사를 건너뛰었다)
    """
    seeds = {m["gseed"]: m for m in manA["geometry_seeds"]}
    if a.gseed not in seeds:
        raise SystemExit(f"⛔ gseed {a.gseed} 가 stage A manifest 에 없다 "
                         f"(있는 것: {sorted(seeds)}) — 재라벨링은 통하지 않는다")
    sm = seeds[a.gseed]
    try:
        text = open(a.neutral_out, encoding="utf-8", errors="strict").read()
    except (OSError, UnicodeDecodeError) as e:
        raise SystemExit(f"⛔ neutral .out 판독 실패 ({e}) — receipt 불가")
    seg = text.split("* O   R   C   A *")[-1]
    if "ORCA TERMINATED NORMALLY" not in seg:
        raise SystemExit("⛔ neutral .out: 정상종료 없음 — Opt receipt 불가")
    if "THE OPTIMIZATION HAS CONVERGED" not in seg:
        raise SystemExit("⛔ neutral .out: Opt 수렴 문구 없음 — 미수렴 부모는 R0 이 아니다")
    ee = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", seg)
    if not ee:
        raise SystemExit("⛔ neutral .out: FINAL SINGLE POINT ENERGY 없음")
    ver = re.search(r"Program Version\s+(\S+)", text)

    # ⑥ 섹터 대조 — 중성 부모는 RKS · charge 0 · singlet 이어야 한다 (R4 P0-2)
    hf = re.findall(r"Hartree-Fock type\s+HFTyp\s*\.+\s*(\w+)", seg)
    if not hf:
        raise SystemExit("⛔ neutral .out: HFTyp 없음 — RKS 부모임을 확인할 수 없다 (R4 P0-2)")
    if "RKS" not in hf[-1].upper() and "RHF" not in hf[-1].upper():
        raise SystemExit(f"⛔ neutral .out: HFTyp={hf[-1]} — 중성 부모는 RKS 여야 한다. "
                         "open-shell 출력을 부모로 쓸 수 없다 (R4 P0-2)")
    q = re.findall(r"Total Charge\s+Charge\s*\.+\s*(-?\d+)", seg)
    mu = re.findall(r"Multiplicity\s+Mult\s*\.+\s*(\d+)", seg)
    if not q or not mu:
        raise SystemExit("⛔ neutral .out: charge/multiplicity echo 없음 — "
                         "섹터를 확인할 수 없는 출력은 부모가 될 수 없다 (R4 P0-2)")
    if int(q[-1]) != 0 or int(mu[-1]) != 1:
        raise SystemExit(f"⛔ neutral .out: charge {q[-1]} · mult {mu[-1]} — "
                         "중성 부모는 (0, 1) 이어야 한다 (R4 P0-2)")

    csym, cpos = read_xyz(a.neutral_xyz)

    # ⑦ stage A 조립본은 **필수** — 없으면 ④⑤ 를 할 수 없으므로 거부한다
    a_xyz = os.path.join(os.path.dirname(a.stage_a_manifest), sm["dir"], sm["tag"] + ".xyz")
    if not os.path.isfile(a_xyz):
        raise SystemExit(f"⛔ stage A 조립본을 찾을 수 없다: {a_xyz} — "
                         "시작구조 없이는 receipt 를 발급하지 않는다 (R4 P0-2 ⑦)")
    asym, apos = read_xyz(a_xyz)
    if len(asym) != len(csym):
        raise SystemExit(f"⛔ 원자수 불일치: stage A 조립본 {len(asym)} ≠ neutral_xyz {len(csym)}")

    blocks = _coord_blocks(text, len(csym))
    if not blocks:
        raise SystemExit("⛔ neutral .out: 좌표 블록 없음 — xyz 와 결합 불가")

    # ⑤ 시작 좌표블록 == 그 gseed 의 조립본 (다른 seed 출력을 이 gseed 로 못 붙인다)
    d_start = _max_disp(blocks[0], asym, apos)
    if d_start is None:
        raise SystemExit("⛔ .out 첫 좌표블록의 원소 배열이 stage A 조립본과 다르다 — "
                         "이 출력은 이 계의 것이 아니다 (R4 P0-2 ⑤)")
    if d_start > 1e-3:
        raise SystemExit(
            f"⛔ .out 시작구조가 gseed {a.gseed} 조립본과 다르다 (최대 {d_start:.4f} Å) — "
            "다른 seed 의 출력을 재라벨링한 것이다 (R4 P0-2 ⑤)")

    # ③ 마지막 좌표블록 == neutral_xyz
    d_end = _max_disp(blocks[-1], csym, cpos)
    if d_end is None or d_end > 1e-4:
        raise SystemExit("⛔ .out 최종좌표와 neutral_xyz 불일치 — "
                         "이 xyz 는 이 .out 의 산물이 아니다")

    # ④ 실제로 이완됐나 — SHA 가 아니라 **좌표**로 본다 (주석 한 줄 우회 차단)
    d_relax = _max_disp(blocks[-1], asym, apos)
    if d_relax is None or d_relax < RELAX_MIN_DISP_A:
        raise SystemExit(
            f"⛔ 최종구조가 stage A 조립본에서 {0.0 if d_relax is None else d_relax:.6f} Å 밖에 "
            f"안 움직였다 (< {RELAX_MIN_DISP_A}) — 미이완 부모다. ORCA Opt 최종 xyz 를 "
            "넣어라 (R4 P0-2 ④: SHA 비교는 주석 변경으로 우회됐다)")

    inp = os.path.splitext(a.neutral_out)[0] + ".inp"
    return {"gseed": a.gseed, "stage_a_calculation_id": sm["calculation_id"],
            "stage_a_manifest_sha256": _sha(a.stage_a_manifest),
            "stage_a_start_xyz": os.path.abspath(a_xyz),
            "stage_a_start_xyz_sha256": _sha(a_xyz),
            "out_path": os.path.abspath(a.neutral_out), "out_sha256": _sha(a.neutral_out),
            "inp_sha256": (_sha(inp) if os.path.isfile(inp) else None),
            "xyz_sha256": _sha(a.neutral_xyz),
            "start_to_final_max_disp_A": round(d_relax, 6),
            "hf_type": hf[-1], "charge": int(q[-1]), "mult": int(mu[-1]),
            "final_energy_Eh": float(ee[-1]),
            "orca_version": (ver.group(1) if ver else None),
            "terminated": True, "opt_converged": True}


# ══ Stage B — 검증된 부모에서 vertical/adiabatic 매트릭스 생성 ═══════════════════
def stage_b(a):
    if a.stage_a_manifest and a.neutral_out:
        manA = json.load(open(a.stage_a_manifest))
        receipt = neutral_receipt(a, manA)
    elif a.allow_unverified_parent:
        receipt = {"gseed": a.gseed, "unverified": True,
                   "xyz_sha256": _sha(a.neutral_xyz),
                   "⚠": "selftest 전용 — 재심사 제출물 아님"}
        print("  ⚠ 부모 receipt 생략 (--allow_unverified_parent — selftest 전용)")
    else:
        raise SystemExit("⛔ stage B 는 --stage_a_manifest 와 --neutral_out 이 필요하다 — "
                         "자유문구(xyz 주석)는 증거가 아니다 (R3 P0-2)")
    csym, cpos = read_xyz(a.neutral_xyz)
    cnb, crings, csulf = analyze(csym, cpos)
    n = a.n
    if len(crings) != n or len(csulf) != n:
        raise SystemExit(f"⛔ neutral 부모 위상 불일치 (링 {len(crings)}·SO3 {len(csulf)} ≠ {n})")
    v7c_real = check_closed_form(csym, n, 0)
    if not v7c_real and not a.allow_noncanonical:
        raise SystemExit("⛔ neutral 부모가 v7c 닫힌꼴이 아니다 (--allow_noncanonical 은 시험 전용)")
    names = ring_chain_names(crings)
    req = REQUIRED_MATRIX[n]
    patterns = ([p.upper() for p in a.patterns] if a.patterns
                else req["singles"] + req["pairs"])
    if len(patterns) != len(set(patterns)):
        raise SystemExit(f"⛔ 패턴 중복 {patterns} — exactly-once 위반 (R3 조건 3)")
    missing = [p for p in req["singles"] + req["pairs"] if p not in patterns]
    if missing and not a.allow_partial:
        raise SystemExit(f"⛔ 필수 매트릭스 누락 {missing} — 부분 생성은 --allow_partial "
                         "(시험 전용)")
    os.makedirs(a.out, exist_ok=True)
    scf_seeds = ["s0", "s1"][:max(1, a.scf_seeds)]
    jobs, sp_ids = [], {}
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
        xyzp = os.path.join(a.out, f"{base}.xyz")
        write_xyz(xyzp, vsym, vpos,
                  f"R0 vertical frame: verified neutral parent minus acid H {rmH} "
                  f"(DP{n}_h{m}_Q0, unrelaxed)")
        sectors = SECTORS_ODD if m % 2 == 1 else SECTORS_EVEN
        for sec, wf, mult, nab, bs, label in sectors:
            check_parity(e, mult)
            for jt in ("sp_vertical", "opt_adiabatic"):
                for ss in (scf_seeds if wf != "RKS" else ["s0"]):
                    tag = f"{base}_{sec}_{jt.split('_')[0]}_{ss}"
                    inpp = os.path.join(a.out, f"{tag}.inp")
                    make_inp(inpp, f"{base}.xyz", wf, mult, bs, jt, scf_seed=ss)
                    cond = dict(estimand_id="sdcp-doped-gas-stage0/v3", dp=n,
                                species=f"DP{n}_h{m}_Q0", pattern=pat,
                                removed_H_indices=rmH, sector=sec,
                                wavefunction_class=wf, orca_mult=mult,
                                n_alpha_minus_beta=nab, net_charge=0,
                                all_electron_count=e, job_type=jt,
                                geometry_seed=f"g{a.gseed}", scf_seed=ss,
                                parent_xyz_sha256=receipt["xyz_sha256"],
                                method="r2SCAN-3c/TightSCF")
                    cid = calculation_id(cond)
                    if jt == "sp_vertical":
                        sp_ids[(pat, sec, ss)] = cid
                    jobs.append(dict(
                        tag=tag, calculation_id=cid, conditioning=cond,
                        formula=formula_of(vsym), n_atoms=len(vsym),
                        sector_label=label,
                        inp_sha256=_sha(inpp), xyz_sha256=_sha(xyzp),
                        seeded_separation=(abs(ord(letters[0]) - ord(letters[1]))
                                           if m == 2 else None),
                        depends_on=(None if jt == "sp_vertical"
                                    else sp_ids[(pat, sec, ss)]),
                        expected=dict(hf_type=("RHF" if wf == "RKS" else "UHF"),
                                      s2_target=(0.75 if sec == "d" else
                                                 2.0 if sec == "t" else
                                                 None if sec == "s" else "bs_window"),
                                      charge=0, mult=mult),
                        realized=None))
    # U_PCET cycle 레코드 (R3 조건 9): 각 쌍의 4-leg 를 calculation_id 로 결속
    cycles = []
    for pat in patterns:
        if "," not in pat or not PAIR_POLICY.get(pat, "").startswith("U_PCET"):
            continue
        a1, a2 = [x.strip() for x in pat.split(",")]
        for frame, jt in (("vertical", "sp"), ("adiabatic", "opt")):
            legs = {}
            okc = True
            for lg, key in (("h1a", (a1, "d", "s0")), ("h1b", (a2, "d", "s0"))):
                j = [x for x in jobs if x["conditioning"]["pattern"] == key[0]
                     and x["conditioning"]["sector"] == "d"
                     and x["conditioning"]["scf_seed"] == "s0"
                     and x["tag"].endswith(f"_{jt}_s0")]
                if not j:
                    okc = False
                    break
                legs[lg] = j[0]["calculation_id"]
            for sec in ("s", "t", "bs"):
                j = [x for x in jobs if x["conditioning"]["pattern"] == pat
                     and x["conditioning"]["sector"] == sec
                     and x["conditioning"]["scf_seed"] == "s0"
                     and x["tag"].endswith(f"_{jt}_s0")]
                if j:
                    legs[f"h2_{sec}"] = j[0]["calculation_id"]
            if not okc:
                raise SystemExit(f"⛔ U_PCET({pat}) {frame}: h1 leg 잡이 없다 — cycle 불완전")
            legs["h0"] = (receipt.get("stage_a_calculation_id", "UNVERIFIED_PARENT")
                          if frame == "adiabatic" else "parent_final_energy(receipt)")
            cycles.append(dict(pair=pat, frame=frame, method="r2SCAN-3c/TightSCF",
                               legs=legs,
                               h0_energy_Eh=receipt.get("final_energy_Eh")))
    man = {
        "schema": "sdcp_stage0_manifest/v3", "stage": "B",
        "estimand_id": "sdcp-doped-gas-stage0/v3",
        "design_card": "kb/questions/sdcp_doped_reopen_v3_2026_08_28.md",
        "builder_commit": _git_commit(),
        "dp": n, "geometry_seed": f"g{a.gseed}",
        "parent_receipt": receipt,
        "closed_form_validated": v7c_real,
        "required_matrix": req, "generated_patterns": patterns,
        "partial": bool(missing), "pair_policy": PAIR_POLICY,
        "u_pcet_cycles": cycles,
        "delta_definitions": {
            "U_PCET_vert(a,b)": "E_sp[h2;R0] + E[h0;R0] − E_sp[h1a;R0] − E_sp[h1b;R0]",
            "U_PCET_ad(a,b)": "각 leg 최적화 최소점 — vertical 과 혼합 금지",
            "⛔": "핵 조성이 변하므로 순수 Hubbard U 아님. cycle 은 위 legs 의 "
                 "calculation_id 로만 조립한다 (동일 method·frame — R3 조건 9)"},
        "atom_sets_neutral_frame": atom_sets_of(csym, cnb, crings, csulf, names),
        "localization_class_rule": {
            "share(g)": "Σ_{i∈g} m_i / Σ_i |m_i| (Löwdin·Hirshfeld 각각)",
            "class": f"|share| ≥ {LOC_CLASS_MIN} 인 집합이 유일하면 그 라벨 · "
                     f"아니면 MIXED_UNRESOLVED · Σ|m| < {LOC_ABS_MIN} 이면 NO_SPIN",
            "⚠": "사전 규칙 — 결과를 본 뒤 경계 변경 금지 (R3)"},
        "stage0_observable": "carrier_localization_profile — 입력이 Hirshfeld(+UNO/UCO) 를 "
                             "요청한다 (R3 P0-0 데이터 회수 계약)",
        "abort_codes": list(ABORT_CODES),
        "jobs": jobs,
        "runner_rule": "opt_adiabatic 은 depends_on 의 sp_vertical 이 analyzer OK 일 때만 "
                       "실행 — analyzer 가 DEPENDENCY_NOT_MET 로 강제한다",
    }
    mp = os.path.join(a.out, "manifest_stage_b.json")
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
    print(f"stage B: 패턴 {len(patterns)} · 잡 {len(jobs)} · cycle {len(cycles)} · manifest {mp}")
    return man


# ══ Analyzer — 양성 증거 요구 + abort code emit (회신 R3 P0-4 전면 재작성) ═══════
def _last_segment(text):
    parts = text.split("* O   R   C   A *")
    return parts[-1] if len(parts) > 1 else text


def analyze_out(text, job, atom_sets=None, removed_H=None):
    """ORCA .out + manifest 잡 → (status, [codes], realized).

    R3 원칙: **양성 증거가 없으면 OK 가 아니다.** 마지막 완결 segment 에서
    정상종료·최종 에너지·HFTyp·charge/mult 대조·(open-shell) 마지막 <S²>·
    (sp&!bs) stability 수행+stable·(opt) 수렴을 전부 요구한다.

    ⛔ 못 하는 것: BLA·participation ratio·UNO 점유수 산출 (후속 profile 도구).
      여기의 localization_class 는 Löwdin 국소스핀 + 사전 규칙까지다.
    """
    codes, realized = [], {}
    seg = _last_segment(text)
    if "ORCA TERMINATED NORMALLY" not in seg:
        return "FAIL", ["SCF_UNCONVERGED"], realized
    cond, exp = job["conditioning"], job["expected"]
    ee = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", seg)
    if not ee:
        codes.append("SCF_UNCONVERGED")            # 종료문구만 있고 에너지 없음 = 증거 부족
    else:
        realized["energy_Eh"] = float(ee[-1])      # ⚠ 마지막 값 (R3: 첫 값 금지)
    hf = re.findall(r"Hartree-Fock type\s+HFTyp\s*\.+\s*(\w+)", seg)
    realized["hf_type"] = hf[-1] if hf else None
    if realized["hf_type"] is None or exp["hf_type"] not in realized["hf_type"]:
        codes.append("SECTOR_MISMATCH")
    q = re.findall(r"Total Charge\s+Charge\s*\.+\s*(-?\d+)", seg)
    mu = re.findall(r"Multiplicity\s+Mult\s*\.+\s*(\d+)", seg)
    # ⛔⛔ 회신 R4 P0-4 — **echo 가 아예 없으면 통과했다.** `if q and ...` 는 q 가 비면
    #   조건 자체가 거짓이라 코드가 안 붙는다. 섹터를 확인할 수 없는 출력은 통과가 아니다.
    if not q or not mu:
        codes.append("SECTOR_UNVERIFIED")
    else:
        if int(q[-1]) != exp["charge"]:
            codes.append("SECTOR_MISMATCH")
        if int(mu[-1]) != exp["mult"]:
            codes.append("SECTOR_MISMATCH")
        realized["charge"], realized["mult"] = int(q[-1]), int(mu[-1])
    s2l = re.findall(r"<S\*\*2>\s*:?\s*(-?\d+\.\d+)", seg)
    realized["s2"] = float(s2l[-1]) if s2l else None
    sec, jt = cond["sector"], cond["job_type"]
    tgt = exp["s2_target"]
    if sec == "bs":
        if realized["s2"] is None:
            codes.append("SPIN_CONTAMINATION_UNREPORTED")
        elif realized["s2"] < 0.2 or realized["s2"] > 1.5:
            codes.append("NA_STATE_NOT_IDENTIFIED")   # closed 붕괴(<0.2) 또는 미플립 HS(≥1.5)
    elif isinstance(tgt, float):
        if realized["s2"] is None or abs(realized["s2"] - tgt) > 0.4:
            codes.append("SECTOR_MISMATCH")
    # ⛔⛔ 회신 R4 P0-4 — 안정성 검사에 구멍이 둘 있었다.
    #   ① **임의 문자열이 stable 증거로 통과**했다. `stability analysis indicates` 만
    #      있으면 그 뒤가 무엇이든(바나나여도) unstable 이 아니므로 stable 취급됐다.
    #      → **양성 문구를 명시적으로** 요구한다. unstable 도 stable 도 아니면 UNVERIFIED.
    #   ② **BS 는 SP 단계에서도 면제**였다. ORCA 는 UHF/UKS SP 에 안정성 분석을 지원하므로
    #      면제에 별도 근거가 필요하다 — 근거가 없으니 면제를 없앤다.
    if jt == "sp_vertical":
        if re.search(r"stability analysis indicates.{0,80}unstable", seg, re.I | re.S):
            codes.append("STABILITY_UNSTABLE")
        elif re.search(r"stability analysis indicates.{0,80}\bstable\b", seg, re.I | re.S):
            realized["stability"] = "stable"
        else:
            codes.append("STABILITY_UNVERIFIED")
    if jt == "opt_adiabatic" and "THE OPTIMIZATION HAS CONVERGED" not in seg:
        codes.append("OPT_UNCONVERGED")
    # ── localization (회신 R4 P0-0/P0-4) ────────────────────────────────────
    #   ⛔⛔ 종전 fail-open 셋:
    #     ① Löwdin 블록이 **없으면 `mvals is None` 이라 아무 코드도 안 붙었다** —
    #        열린 껍질인데 국소스핀을 못 읽은 것은 통과가 아니라 hard gate 다.
    #     ② `NO_SPIN`·`REMAP_ERROR` 를 **정상 class 처럼 realized 에 넣고 통과**시켰다.
    #        예상 open-shell 에서 그 둘은 class 가 아니라 **실패**다.
    #     ③ Hirshfeld 를 입력으로 요구해 놓고 **읽지도 않았다.** 두 분할이 갈리면
    #        어느 쪽도 단독으로 못 쓴다 → PARTITION_DEPENDENT.
    if cond["wavefunction_class"] != "RKS":
        if not atom_sets:
            codes.append("LOCALIZATION_UNVERIFIED")
        else:
            nat = job["n_atoms"]
            low = _lowdin_spins(seg, nat)
            hir = _hirshfeld_spins(seg, nat)
            if low is None:
                codes.append("LOCALIZATION_MISSING")   # 열린 껍질인데 블록이 없다
            else:
                cls, shares, sens = _loc_class(low, atom_sets, removed_H or [])
                realized["localization_class"] = cls
                realized["loc_shares"] = shares
                realized["loc_threshold_sensitivity"] = sens
                realized["loc_partition"] = "loewdin"
                if cls in ("NO_SPIN", "REMAP_ERROR"):
                    codes.append("LOCALIZATION_" + cls)   # class 가 아니라 hard gate
                if sens.get("threshold_dependent"):
                    codes.append("THRESHOLD_DEPENDENT")
                if hir is not None:
                    hcls, hshares, _ = _loc_class(hir, atom_sets, removed_H or [])
                    realized["localization_class_hirshfeld"] = hcls
                    realized["loc_shares_hirshfeld"] = hshares
                    if hcls != cls:
                        codes.append("PARTITION_DEPENDENT")
                else:
                    codes.append("HIRSHFELD_MISSING")
    if codes:
        return "GATED", codes, realized
    return "OK", [], realized


def _spin_block(seg, header, nat):
    """`header` 블록의 마지막 것 → 원자 index 로 정렬한 [m_i], 또는 None.

    ⛔⛔ 회신 R4 P0-0 — 종전에는 **출력 순서대로 append** 했다. 정규식이 index 를
      잡아 놓고도 **버렸기** 때문에, 행이 재배열된 출력에서 원자가 통째로 어긋난 채
      조용히 통과했다. 이제 index 를 **자리로 쓰고**, 0..nat-1 이 정확히 한 번씩
      나오지 않으면 **None** 을 돌려 상위에서 게이트되게 한다.

    ⛔⛔ 회신 U P0-3 (2026-09-01) — **콜론을 강제하면 실물 ORCA 를 못 읽는다.**
      종전 정규식은 원소 뒤 `:` 를 요구했다. ORCA 6.1 의 두 블록은 형식이 다르다:
          LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS →  `   0 O :  -0.333756   0.000000`
          HIRSHFELD ANALYSIS                          →  `   0 O    -0.333756   0.000000`
      Hirshfeld 에는 콜론이 없어서 파서가 **`None`** 을 돌렸고, 그러면 상위가
      `HIRSHFELD_MISSING` 으로 게이트한다 — 즉 두 분할 교차검증이 **실물에서는
      한 번도 돈 적이 없다.** selftest 는 fixture 에 인위적으로 `O:` 를 넣어 통과했다.
      ⇒ 콜론은 **선택**이고, fixture 는 공식 형식(콜론 없는 Hirshfeld)을 쓴다.
    """
    blocks = seg.split(header)
    if len(blocks) < 2:
        return None
    got = {}
    for ln in blocks[-1].splitlines()[1:]:
        m = re.match(r"\s*(\d+)\s+[A-Za-z]{1,2}\s*:?\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)", ln)
        if not m:
            if got:
                break
            continue
        i = int(m.group(1))
        if i in got:                     # 같은 index 가 두 번 = 파싱 경계를 넘었다
            break
        got[i] = float(m.group(3))
    if len(got) != nat or set(got) != set(range(nat)):
        return None                      # 개수/index 집합 불일치 → 판정 불가
    return [got[i] for i in range(nat)]


def _lowdin_spins(seg, nat):
    return _spin_block(seg, "LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS", nat)


def _hirshfeld_spins(seg, nat):
    """HIRSHFELD ANALYSIS 의 스핀 열. 회신 R4 보완 5 — 두 분할을 **둘 다** 본다."""
    return _spin_block(seg, "HIRSHFELD ANALYSIS", nat)


def _loc_class(mvals, atom_sets_neutral, removed_H, thr=LOC_CLASS_MIN):
    """중성 프레임 atom_sets 를 doped 프레임으로 재매핑 검증 후 사전 규칙 적용.

    → (class, shares, sensitivity)

    회신 R4 보완 반영:
      · **원값 보존** — threshold 적용 전에 반올림하지 않는다 (표시용만 반올림).
      · **0.4/0.5/0.6 경계 민감도** — class 가 바뀌면 `threshold_dependent`.
      · **BS 의 양·음 lobe 분리** — signed 합만 보면 서로 상쇄돼 "스핀 없음" 으로 보인다.
        집합마다 `pos`/`neg` 를 따로 남긴다.

    ⛔ 못 하는 것: 어느 **ring** 의 polaron 인지는 atom_sets 가 ring 별로 쪼개져
      들어와야 알 수 있다 (backbone 을 한 덩어리로 주면 여기서도 한 덩어리다).
    """
    kill = sorted(set(removed_H))

    def remap(i):
        return None if i in kill else i - sum(1 for k in kill if k < i)

    tot_abs = sum(abs(m) for m in mvals)
    if tot_abs < LOC_ABS_MIN:
        return "NO_SPIN", {}, {}
    raw, lobes = {}, {}
    for g, idxs in atom_sets_neutral.items():
        mapped = [i for i in (remap(j) for j in idxs) if i is not None]
        if any(i >= len(mvals) for i in mapped):
            return "REMAP_ERROR", {}, {}
        vals = [mvals[i] for i in mapped]
        raw[g] = sum(vals) / tot_abs                       # ⚠ 반올림 안 한다
        lobes[g] = {"pos": round(sum(v for v in vals if v > 0) / tot_abs, 4),
                    "neg": round(sum(v for v in vals if v < 0) / tot_abs, 4)}

    def classify(t):
        w = [g for g, v in raw.items() if abs(v) >= t]
        return w[0] if len(w) == 1 else "MIXED_UNRESOLVED"

    cls = classify(thr)
    alt = {f"{t:.1f}": classify(t) for t in (0.4, 0.5, 0.6)}
    shares = {g: round(v, 4) for g, v in raw.items()}
    shares["_lobes"] = lobes
    return cls, shares, {"by_threshold": alt,
                         "threshold_dependent": len(set(alt.values())) > 1}


def _content_fingerprint(text):
    """ORCA 출력의 **물리 내용** 지문 — 바이트가 아니라 값으로 같은지 본다.

    회신 R4 P0-4: 종전 중복검사는 파일 SHA256 이라 **주석 한 줄만 추가하면 통과**했다.
    복사본은 에너지·S²·섹터·좌표·**실행시간**이 전부 같고, 진짜 재실행은 실행시간이 다르다.
    그래서 그 조합을 지문으로 쓴다.

    ⛔ 이 함수가 못 하는 것:
      · 값 자체를 위조하면 못 잡는다 (그건 다른 게이트의 몫이다).
      · 실행시간 문구가 없는 출력(합성 픽스처 등)에서는 에너지·섹터만으로 판정하므로,
        **s0/s1 처럼 같은 계를 두 번 돌려 같은 해에 수렴한 경우 위양성**이 될 수 있다.
        그래서 코드가 `DUPLICATE_CONTENT` 로 따로 나간다 — 바이트 동일(`DUPLICATE_OUTPUT`)과
        구별해서 보고하고, 게이트지 판결이 아니다.
    """
    seg = _last_segment(text)
    parts = [
        ";".join(re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", seg)),
        ";".join(re.findall(r"Hartree-Fock type\s+HFTyp\s*\.+\s*(\w+)", seg)),
        ";".join(re.findall(r"Total Charge\s+Charge\s*\.+\s*(-?\d+)", seg)),
        ";".join(re.findall(r"Multiplicity\s+Mult\s*\.+\s*(\d+)", seg)),
        ";".join(re.findall(r"<S\*\*2>\s*:?\s*(-?\d+\.\d+)", seg)),
        ";".join(re.findall(r"TOTAL RUN TIME:.*", seg)),
        ";".join(re.findall(r"LOEWDIN ATOMIC CHARGES[\s\S]{0,4000}", seg)[-1:]),
    ]
    blocks = seg.split("CARTESIAN COORDINATES (ANGSTROEM)")
    if len(blocks) > 1:
        parts.append("\n".join(blocks[-1].splitlines()[:400]))
    return hashlib.sha256("|".join(parts).encode()).hexdigest()


def analyze_dir(a):
    man = json.load(open(os.path.join(a.analyze, "manifest_stage_b.json")))
    atom_sets = man.get("atom_sets_neutral_frame")
    out = {"schema": "sdcp_stage0_analysis/v2", "jobs": {}, "emitted": {}}
    n_pend = n_bad = 0
    sha_seen = {}
    fp_seen = {}
    by_cid = {}
    for job in man["jobs"]:
        op = os.path.join(a.analyze, job["tag"] + ".out")
        if not os.path.isfile(op):
            out["jobs"][job["tag"]] = {"status": "PENDING"}
            n_pend += 1
            continue
        try:
            text = open(op, encoding="utf-8", errors="strict").read()
        except UnicodeDecodeError:
            out["jobs"][job["tag"]] = {"status": "FAIL", "codes": ["OUTPUT_UNREADABLE"]}
            out["emitted"].setdefault("OUTPUT_UNREADABLE", []).append(job["tag"])
            n_bad += 1
            continue
        osha = _sha(op)
        sha_seen.setdefault(osha, []).append(job["tag"])
        fp_seen.setdefault(_content_fingerprint(text), []).append(job["tag"])
        st, codes, realized = analyze_out(
            text, job, atom_sets=atom_sets,
            removed_H=job["conditioning"].get("removed_H_indices"))
        realized["out_sha256"] = osha
        out["jobs"][job["tag"]] = {"status": st, "codes": codes, "realized": realized,
                                   "calculation_id": job["calculation_id"]}
        by_cid[job["calculation_id"]] = st
        for c in codes:
            out["emitted"].setdefault(c, []).append(job["tag"])
        if st != "OK":
            n_bad += 1
    # 중복 출력물 — 두 층으로 본다 (회신 R4 P0-4)
    #   ① 바이트 동일  → DUPLICATE_OUTPUT (종전)
    #   ② 내용 동일   → DUPLICATE_CONTENT. **주석 한 줄만 넣으면 ① 을 빠져나갔다.**
    def _gate_dupes(seen, code):
        nonlocal n_bad
        for _k, tags in seen.items():
            if len(tags) > 1:
                fresh = [t for t in tags if code not in out["jobs"][t].get("codes", [])]
                for t in fresh:
                    out["jobs"][t]["status"] = "GATED"
                    out["jobs"][t].setdefault("codes", []).append(code)
                if fresh:
                    out["emitted"].setdefault(code, []).extend(fresh)
                    n_bad += len(fresh)
    _gate_dupes(sha_seen, "DUPLICATE_OUTPUT")
    _gate_dupes(fp_seen, "DUPLICATE_CONTENT")

    # ⛔⛔ 회신 R4 P0-3 — **dependency map 이 낡은 채로 쓰였다.** `by_cid` 는 첫 루프에서
    #   채워지는데 그 뒤 중복 게이트가 `out["jobs"][t]["status"]` 를 GATED 로 바꿔도
    #   `by_cid` 는 그대로 `OK` 였다. 그래서 **중복으로 막힌 SP 에 딸린 Opt 가 승인**됐다.
    #   ⇒ 최종 gate 뒤에 map 을 **다시 만들고**, 사슬(A→B→C)을 위해 **고정점까지 전파**한다.
    tag_of_cid = {j["calculation_id"]: j["tag"] for j in man["jobs"]}
    for _ in range(len(man["jobs"]) + 1):
        by_cid = {j["calculation_id"]: out["jobs"].get(j["tag"], {}).get("status")
                  for j in man["jobs"]}
        changed = False
        for job in man["jobs"]:
            dep = job.get("depends_on")
            if not dep:
                continue
            rec = out["jobs"].get(job["tag"])
            # ⚠ 이미 다른 사유로 GATED 된 잡도 **의존성 코드는 받아야 한다** — 코드 목록이
            #   불완전하면 "왜 막혔나" 를 사람이 못 읽는다. 중복 부착만 막는다.
            if rec is None or rec.get("status") == "PENDING":
                continue
            if "DEPENDENCY_NOT_MET" in rec.get("codes", []):
                continue
            if by_cid.get(dep) != "OK":
                rec["status"] = "GATED"
                rec.setdefault("codes", []).append("DEPENDENCY_NOT_MET")
                out["emitted"].setdefault("DEPENDENCY_NOT_MET", []).append(job["tag"])
                n_bad += 1
                changed = True
        if not changed:
            break
    else:
        raise SystemExit("⛔ dependency 전파가 고정점에 도달하지 않았다 — 순환 의존 의심")
    # 선행이 manifest 에 아예 없는 경우도 미충족이다 (선언만 있고 잡이 없는 dep)
    for job in man["jobs"]:
        dep = job.get("depends_on")
        rec = out["jobs"].get(job["tag"])
        if dep and dep not in tag_of_cid and rec and rec.get("status") == "OK":
            rec["status"] = "GATED"
            rec.setdefault("codes", []).append("DEPENDENCY_NOT_MET")
            out["emitted"].setdefault("DEPENDENCY_NOT_MET", []).append(job["tag"])
            n_bad += 1
    # realized_state_id — calc_id + **출력물 해시** 결속 (결과 문자열 digest 금지)
    for t, rec in out["jobs"].items():
        if rec.get("status") == "OK":
            rid = hashlib.sha256((rec["calculation_id"]
                                  + rec["realized"]["out_sha256"]).encode()).hexdigest()[:16]
            rec["realized"]["realized_state_id"] = "real_" + rid
    ap = os.path.join(a.analyze, "analysis_stage_b.json")
    json.dump(out, open(ap, "w"), ensure_ascii=False, indent=1)
    for c, tags in out["emitted"].items():
        print(f"  ⛔ {c}: {len(tags)}잡 — {tags[:3]}")
    print(f"analyzer: {ap} · PENDING {n_pend} · 게이트 {n_bad}")
    if n_bad:
        return 2
    if n_pend:
        print("  ⚠ PENDING 이 남았다 — '완료 분석' 이 아니다 (비영 종료, R3 P0-4)")
        return 3
    return 0


def hybrid_select(analysis, manifest, window_eh=0.10 / 27.2114):
    """hybrid decision set — **species·job_type 그룹 안에서만** (R3 P0-5:
    핵·전자수가 다른 종의 절대에너지 비교는 물리적으로 무의미)."""
    meta = {j["tag"]: j for j in manifest["jobs"]}
    ok = {t: r for t, r in analysis["jobs"].items()
          if r.get("status") == "OK" and "energy_Eh" in r.get("realized", {})
          and t in meta}
    pick = set()
    groups = {}
    for t, r in ok.items():
        key = (meta[t]["conditioning"]["species"], meta[t]["conditioning"]["job_type"])
        groups.setdefault(key, {})[t] = r
    for key, grp in groups.items():
        emin = min(r["realized"]["energy_Eh"] for r in grp.values())
        by_class = {}
        for t, r in grp.items():
            if r["realized"]["energy_Eh"] <= emin + window_eh:
                pick.add(t)
            cls = r["realized"].get("localization_class")
            if cls and cls not in ("NO_SPIN",):
                cur = by_class.get(cls)
                if cur is None or r["realized"]["energy_Eh"] < grp[cur]["realized"]["energy_Eh"]:
                    by_class[cls] = t
        pick |= set(by_class.values())
    return sorted(pick)


def hybrid_stage(a):
    """--hybrid <dir>: analysis + manifest → decision set 의 wB97X-D3 fresh-start 입력 생성."""
    man = json.load(open(os.path.join(a.hybrid, "manifest_stage_b.json")))
    ana = json.load(open(os.path.join(a.hybrid, "analysis_stage_b.json")))
    picks = hybrid_select(ana, man)
    if not picks:
        raise SystemExit("⛔ decision set 이 비었다 — OK 인 잡이 없거나 분석 미완")
    meta = {j["tag"]: j for j in man["jobs"]}
    made, skipped = [], []
    for t in picks:
        c = meta[t]["conditioning"]
        tag = t + "_hyb"
        # ⛔⛔ 회신 R4 위험 ① — 종전에는 `meta[t]["tag"].rsplit("_",3)[0] + ".xyz"`,
        #   즉 **원래 vertical XYZ** 로 hybrid SP 를 만들었다. adiabatic 승자를 골라 놓고
        #   그 **최종구조를 버린** 것이라, hybrid 는 "선택된 상태의 다른 방법 재계산" 이
        #   아니었다. → adiabatic 은 그 Opt 의 **최종 xyz** 를 쓴다. 없으면 **건너뛴다.**
        if c["job_type"] == "opt_adiabatic":
            xyz = f"{t}_final.xyz"
            if not os.path.isfile(os.path.join(a.hybrid, xyz)):
                skipped.append((tag, f"adiabatic 최종구조 {xyz} 가 없다"))
                continue
        else:
            xyz = meta[t]["tag"].rsplit("_", 3)[0] + ".xyz"
        make_inp(os.path.join(a.hybrid, f"{tag}.inp"), xyz,
                 c["wavefunction_class"], c["orca_mult"],
                 bs=(c["sector"] == "bs"),
                 job_type=c["job_type"],          # vertical 을 강제하지 않는다
                 scf_seed="s0", hybrid=True)
        made.append(tag)
    if skipped:
        for tag, why in skipped:
            print(f"  ⛔ {tag} 건너뜀 — {why}")
        raise SystemExit(
            f"⛔ decision set {len(picks)}개 중 {len(skipped)}개가 최종구조 없이 남았다. "
            "vertical XYZ 로 대체 생성하지 않는다 (R4 위험 ①) — Opt 를 먼저 회수하라.")
    print(f"hybrid: decision set {len(picks)}잡 → 입력 생성 (NoAutoStart 강제)")
    return made


def compare_methods(a):
    """--compare <dir1> <dir2>: 두 분석의 그룹별 승자·순서 비교 → METHOD_DEPENDENT emit."""
    outs, methods = [], []
    for d in a.compare:
        man = json.load(open(os.path.join(d, "manifest_stage_b.json")))
        ana = json.load(open(os.path.join(d, "analysis_stage_b.json")))
        meta = {j["tag"]: j for j in man["jobs"]}
        win = {}
        for t, r in ana["jobs"].items():
            if r.get("status") != "OK" or t not in meta:
                continue
            c = meta[t]["conditioning"]
            key = (c["species"], c["pattern"], c["job_type"])
            e = r["realized"]["energy_Eh"]
            if key not in win or e < win[key][1]:
                # ⛔ 회신 R4 P0-5 — 종전엔 sector 만 봤다. 같은 sector 안에서
                #   localization/state 가 달라도 "일치" 로 읽혔다.
                win[key] = (c["sector"], e,
                            r["realized"].get("localization_class"),
                            r["realized"].get("realized_state_id"))
        outs.append(win)
        methods.append(man.get("method") or man.get("hybrid_spec", {}).get("keywords")
                       or os.path.basename(os.path.abspath(d)))

    # ⛔⛔ 회신 R4 P0-5 — **한쪽이 비어도 성공**했다. `for k in outs[0] if k in outs[1]`
    #   은 교집합만 보므로, outs 중 하나가 통째로 비면 diff 가 {} 라 "일치" 로 통과했다.
    if not outs[0] or not outs[1]:
        print(f"  ⛔ 비교 불가 — OK 인 잡: {len(outs[0])} vs {len(outs[1])}. "
              "한쪽이 비면 '일치' 가 아니라 **미비교**다")
        return 2
    if methods[0] == methods[1]:
        print(f"  ⛔ 두 디렉터리의 method 가 같다 ({methods[0]}) — 교차검사가 성립하지 않는다")
        return 2
    only0, only1 = set(outs[0]) - set(outs[1]), set(outs[1]) - set(outs[0])
    if only0 or only1:
        print(f"  ⛔ 그룹이 한쪽에만 있다 — {methods[0]} 전용 {len(only0)}개 · "
              f"{methods[1]} 전용 {len(only1)}개. 교집합만 보고 넘어가지 않는다")
        for k in sorted(only0 | only1)[:5]:
            print(f"      {k}")
        return 2
    bad = 0
    for k in sorted(outs[0]):
        a0, a1 = outs[0][k], outs[1][k]
        for lbl, i in (("sector", 0), ("localization", 2)):
            if a0[i] != a1[i]:
                print(f"  ⛔ METHOD_DEPENDENT[{lbl}]: {k} — {methods[0]} {a0[i]} "
                      f"≠ {methods[1]} {a1[i]}")
                bad += 1
    if bad:
        return 2
    print(f"  ✓ {methods[0]} 와 {methods[1]} 의 그룹별 승자·localization 일치 "
          f"({len(outs[0])} 그룹)")
    return 0


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


def _fake_orca_out(terminated=True, energies=(-100.0,), hf="UHF", s2=None, s2_list=None,
                   stability="stable", opt_converged=False, charge=0, mult=None,
                   coords=None, coords_start=None, spins=None, version="6.1.0"):
    """R3 게이트 검증용 합성 ORCA 출력 — 양성 증거를 골라 넣고 뺄 수 있다.

    R4 P0-2 ⑤ 이후로 **좌표블록이 두 개**여야 실제 Opt 출력을 닮는다:
    `coords_start` = 입력(시작) 기하, `coords` = 최종 기하. `coords_start` 를 빼면
    블록이 하나뿐이라 시작=최종으로 읽히므로, 그것 자체가 미이완 음성 픽스처가 된다.
    """
    t = "                                 * O   R   C   A *\n"
    t += f"                       Program Version {version} - RELEASE\n"
    if hf:
        t += f" Hartree-Fock type      HFTyp           .... {hf}\n"
    t += f" Total Charge           Charge          ....    {charge}\n"
    if mult is not None:
        t += f" Multiplicity           Mult            ....    {mult}\n"
    for blk in (coords_start, coords):
        if blk is None:
            continue
        t += "CARTESIAN COORDINATES (ANGSTROEM)\n---------------------------------\n"
        for el, p in blk:
            t += f"  {el}   {p[0]:.6f}   {p[1]:.6f}   {p[2]:.6f}\n"
        t += "\n"
    if spins is not None:
        t += "LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS\n----------------\n"
        for i, m in enumerate(spins):
            t += f"  {i} X :   0.000000   {m:.6f}\n"
        t += "\n"
    vals = s2_list if s2_list is not None else ([s2] if s2 is not None else [])
    for v in vals:
        t += f" Expectation value of <S**2>     :     {v:.6f}\n"
    if stability == "stable":
        t += " Stability analysis indicates a stable HF/KS wavefunction\n"
    elif stability == "unstable_upper":
        t += " STABILITY ANALYSIS INDICATES AN UNSTABLE RHF/RKS WAVEFUNCTION\n"
    elif stability == "unstable":
        t += " Stability analysis indicates an unstable wavefunction\n"
    if opt_converged:
        t += "                    *** THE OPTIMIZATION HAS CONVERGED ***\n"
    for e in energies:
        t += f" FINAL SINGLE POINT ENERGY      {e:.9f}\n"
    if terminated:
        t += "                             ****ORCA TERMINATED NORMALLY****\n"
    return t


def selftest():
    import tempfile
    import shutil as _copy2
    fails = []

    def chk(ok, msg):
        print(("  ✓ " if ok else "  ✗ ") + msg)
        if not ok:
            fails.append(msg)

    def raises(fn, msg):
        try:
            fn()
            chk(False, msg)
        except SystemExit:
            chk(True, msg)

    print("── build_v7c_trimer selftest (R3 게이트판) ──")
    sym, pos = _synthetic_dimer()
    nb, rings, sulf = analyze(sym, pos)
    chk(len(sym) == 26 and len(rings) == 2 and len(sulf) == 2,
        f"합성 다이머 위상 (원자 {len(sym)} · 링 {len(rings)} · SO3 {len(sulf)})")

    with tempfile.TemporaryDirectory() as td:
        dim = os.path.join(td, "dimer.xyz")
        write_xyz(dim, sym, pos, "synthetic dimer for selftest")
        NS = argparse.Namespace

        # ── R3 P0-1: seed 강제 3종
        raises(lambda: stage_a(NS(dimer=dim, out=td + "/x1", cc=CC_NEW, step=30, n=3,
                                  seeds=1, allow_noncanonical=True, allow_underseed=False),
                               sym, pos),
               "음성: --seeds 1 < 바닥 4 → 거부 (R3: 선언만으로는 안 된다)")
        raises(lambda: stage_a(NS(dimer=dim, out=td + "/x2", cc=CC_NEW, step=30, n=3,
                                  seeds=-3, allow_noncanonical=True, allow_underseed=True),
                               sym, pos),
               "음성: 음수 seed → 거부")
        raises(lambda: stage_a(NS(dimer=dim, out=td + "/x3", cc=CC_NEW, step=180, n=3,
                                  seeds=4, allow_noncanonical=True, allow_underseed=False),
                               sym, pos),
               "음성: 후보각 부족(step=180)으로 고유 4 seed 불가 → 고갈 중단")
        raises(lambda: stage_a(NS(dimer=dim, out=td + "/x4", cc=CC_NEW, step=30, n=3,
                                  seeds=2, allow_noncanonical=False, allow_underseed=True),
                               sym, pos),
               "음성: 비정본 다이머 + 플래그 없음 → 거부 (fail-closed 유지)")

        aA = NS(dimer=dim, out=os.path.join(td, "a3"), cc=CC_NEW, step=30, n=3,
                seeds=2, allow_noncanonical=True, allow_underseed=True)
        manA = stage_a(aA, sym, pos)
        g0, g1 = manA["geometry_seeds"]
        chk(tuple(g0["torsions"]) != tuple(g1["torsions"])
            and min(g0["dmins_A"]) >= DMIN_FLOOR and min(g1["dmins_A"]) >= DMIN_FLOOR,
            f"stage A: 고유 torsion + 전 접합 dmin≥{DMIN_FLOOR} 기록 "
            f"({g0['torsions']}/{g1['torsions']} · dmin {g0['dmins_A']})")
        chk(g0["calculation_id"].startswith("calc_") and len(g0["xyz_sha256"]) == 64
            and manA["seed_floor"]["underseed_flag"] is True
            and manA["builder_commit"] != "",
            "stage A: 잡 calc_id + xyz sha + builder commit + underseed 플래그 (P1)")
        inpA = open(os.path.join(aA.out, "gs0", "dp3_gs0_neutral.inp")).read()
        chk(inpA.startswith("! RKS") and " Opt " in inpA and "Hirshfeld" in inpA
            and "UNO" not in inpA,
            "neutral 입력: RKS Opt + Hirshfeld (RKS 라 UNO 없음) — R3 P0-0 회수 계약")

        # ── R3 P0-2: 부모 receipt — 위조 4종 거부 + 정상 1종
        asm = os.path.join(aA.out, "gs0", "dp3_gs0_neutral.xyz")
        opt_xyz = os.path.join(td, "neutral_opt.xyz")
        s3, p3 = read_xyz(asm)
        p3o = [[x + (0.011 if i == 0 else 0.0), y, z] for i, (x, y, z) in enumerate(p3)]
        write_xyz(opt_xyz, s3, p3o, "Coordinates from ORCA-job dp3_gs0_neutral (fake opt)")
        out_ok = os.path.join(td, "neutral.out")
        open(out_ok, "w").write(_fake_orca_out(
            hf="RHF", charge=0, mult=1, opt_converged=True,
            coords_start=list(zip(s3, p3)), coords=list(zip(s3, p3o)),
            energies=(-500.0, -500.123456789)))
        manAp = os.path.join(aA.out, "manifest_stage_a.json")

        def B(**kw):
            base = dict(stage_a_manifest=manAp, neutral_out=out_ok, neutral_xyz=opt_xyz,
                        out=os.path.join(td, "b3"), n=3, gseed=0, patterns=None,
                        allow_partial=False, allow_noncanonical=True, scf_seeds=2,
                        allow_unverified_parent=False)
            base.update(kw)
            return NS(**base)

        raises(lambda: stage_b(B(neutral_xyz=asm)),
               "음성: 부모 = stage A 조립본과 동일 → 미이완 재사용 거부 (R3 P0-2)")
        raises(lambda: stage_b(B(gseed=999)),
               "음성: manifest 에 없는 gseed 재라벨링 → 거부")
        out_nc = os.path.join(td, "nc.out")
        open(out_nc, "w").write(_fake_orca_out(hf="RHF", charge=0, mult=1,
                                               opt_converged=False,
                                               coords_start=list(zip(s3, p3)),
                                               coords=list(zip(s3, p3o))))
        raises(lambda: stage_b(B(neutral_out=out_nc)),
               "음성: Opt 수렴 문구 없는 .out → 거부")
        out_mm = os.path.join(td, "mm.out")
        p3bad = [[x + 0.5, y, z] for x, y, z in p3o]
        open(out_mm, "w").write(_fake_orca_out(hf="RHF", charge=0, mult=1,
                                               opt_converged=True,
                                               coords_start=list(zip(s3, p3)),
                                               coords=list(zip(s3, p3bad))))
        raises(lambda: stage_b(B(neutral_out=out_mm)),
               "음성: .out 최종좌표 ≠ neutral_xyz → 결합 실패 거부")

        # ══ 회신 R4 회귀시험 ① — **교차-seed receipt** ═══════════════════════
        #   gs1 의 시작구조로 돌린 출력을 gseed 0 이라 주장한다. 종전 코드는
        #   "gseed 가 manifest 에 있나" 만 봐서 통과시켰다.
        s3b, p3b = read_xyz(os.path.join(aA.out, "gs1", "dp3_gs1_neutral.xyz"))
        p3bo = [[x + (0.011 if i == 0 else 0.0), y, z] for i, (x, y, z) in enumerate(p3b)]
        xyz_x = os.path.join(td, "cross.xyz")
        write_xyz(xyz_x, s3b, p3bo, "gs1 opt")
        out_x = os.path.join(td, "cross.out")
        open(out_x, "w").write(_fake_orca_out(
            hf="RHF", charge=0, mult=1, opt_converged=True,
            coords_start=list(zip(s3b, p3b)), coords=list(zip(s3b, p3bo))))
        raises(lambda: stage_b(B(neutral_out=out_x, neutral_xyz=xyz_x, gseed=0)),
               "음성 R4①: gs1 출력을 gseed 0 으로 재라벨링 → 시작구조 불일치로 거부")

        # ══ 회신 R4 회귀시험 ② — **wrong-state receipt (UHF·+1·doublet)** ════
        #   R4 실측: 이 출력이 neutral RKS 부모로 **통과**했다.
        for kw, why in (
                (dict(hf="UHF"), "UHF 출력"),
                (dict(charge=1), "charge +1"),
                (dict(mult=2), "doublet"),
                (dict(hf=None), "HFTyp 없음"),
                (dict(mult=None), "multiplicity echo 없음")):
            base_kw = dict(hf="RHF", charge=0, mult=1, opt_converged=True,
                           coords_start=list(zip(s3, p3)), coords=list(zip(s3, p3o)))
            base_kw.update(kw)
            p = os.path.join(td, "ws_" + why.replace(" ", "_") + ".out")
            open(p, "w").write(_fake_orca_out(**base_kw))
            raises(lambda p=p: stage_b(B(neutral_out=p)),
                   f"음성 R4②: {why} 이 중성 RKS 부모로 통과 → 거부")

        # ══ 회신 R4 회귀시험 ③ — **주석만 바꾼 미이완 부모** ═════════════════
        #   좌표는 조립본과 동일하고 주석만 다르다 ⇒ SHA 는 달라져 종전 검사를 빠져나갔다.
        xyz_cm = os.path.join(td, "comment_only.xyz")
        write_xyz(xyz_cm, s3, p3, "주석만 바꾼 사본 — 좌표는 조립본과 동일하다")
        chk(_sha(xyz_cm) != _sha(asm),
            "  (전제) 주석만 바꾼 xyz 는 SHA 가 다르다 — 그래서 SHA 검사는 못 잡았다")
        out_cm = os.path.join(td, "comment_only.out")
        open(out_cm, "w").write(_fake_orca_out(
            hf="RHF", charge=0, mult=1, opt_converged=True,
            coords_start=list(zip(s3, p3)), coords=list(zip(s3, p3))))
        raises(lambda: stage_b(B(neutral_out=out_cm, neutral_xyz=xyz_cm)),
               "음성 R4③: 주석만 바꾼 미이완 부모 → 좌표 변위로 거부")

        # 양성 대조 — 위 셋과 같은 경로인데 진짜로 이완된 것은 통과해야 한다
        chk(neutral_receipt(B(), json.load(open(manAp)))["start_to_final_max_disp_A"] > 0,
            "양성: 실제로 이완된 부모는 receipt 발급 (변위 > 0)")
        raises(lambda: stage_b(B(stage_a_manifest=None, neutral_out=None)),
               "음성: receipt 인자 없이 stage B → 거부 (자유문구는 증거가 아니다)")

        manB = stage_b(B())
        rc = manB["parent_receipt"]
        chk(rc["opt_converged"] and rc["final_energy_Eh"] == -500.123456789
            and rc["orca_version"] == "6.1.0" and len(rc["out_sha256"]) == 64
            and rc["stage_a_calculation_id"] == g0["calculation_id"],
            "receipt: 수렴·최종에너지(마지막 값)·버전·해시·stage A calc_id 결속")

        # ── 매트릭스·중복·입력 계약
        raises(lambda: stage_b(B(out=td + "/pdup", patterns=["A", "A", "B"])),
               "음성: 패턴 중복 → exactly-once 위반 거부 (R3 조건 3)")
        raises(lambda: stage_b(B(out=td + "/ppart", patterns=["B"])),
               "음성: 부분 매트릭스 + allow_partial 없음 → 거부")
        sp = open(os.path.join(td, "b3", "dp3_gs0_hA_d_sp_s0.inp")).read()
        op = open(os.path.join(td, "b3", "dp3_gs0_hA_d_opt_s0.inp")).read()
        chk("Opt" not in sp and "StabPerform" in sp and "UNO UCO" in sp
            and "Hirshfeld" in sp and sp.startswith("! UKS"),
            "sp 입력: UKS SP + StabPerform + Hirshfeld + UNO UCO (R3 P0-0)")
        chk(" Opt " in op and "Hirshfeld" in op,
            "opt 입력: Opt + Hirshfeld")
        jd = {j["tag"]: j for j in manB["jobs"]}
        chk(jd["dp3_gs0_hA_d_opt_s0"]["depends_on"]
            == jd["dp3_gs0_hA_d_sp_s0"]["calculation_id"],
            "SP→Opt dependency: opt.depends_on == 선행 sp 의 calculation_id (R3 P0-3)")
        chk(all(len(j["inp_sha256"]) == 64 and len(j["xyz_sha256"]) == 64
                for j in manB["jobs"]),
            "잡마다 inp/xyz sha 기록 (출력-입력 결속 준비)")

        # ── analyzer (R3 P0-4): all-PENDING 비영 · 증거부족 · 중복 out · 의존성
        rcode = analyze_dir(NS(analyze=os.path.join(td, "b3")))
        chk(rcode == 3, f"음성: 전 잡 PENDING → 완료 아님, 비영 종료 ({rcode})")
        tagA = "dp3_gs0_hA_d_sp_s0"
        tagB = "dp3_gs0_hB_d_sp_s0"
        tagAo = "dp3_gs0_hA_d_opt_s0"
        # 최소 정상종료 문자열(증거 전무) — OK 금지
        open(os.path.join(td, "b3", tagA + ".out"), "w").write(
            "* O   R   C   A *\nORCA TERMINATED NORMALLY\n")
        rcode = analyze_dir(NS(analyze=os.path.join(td, "b3")))
        ana = json.load(open(os.path.join(td, "b3", "analysis_stage_b.json")))
        chk(ana["jobs"][tagA]["status"] != "OK"
            and "STABILITY_UNVERIFIED" in ana["jobs"][tagA]["codes"],
            "음성: 종료문구만 있는 .out → OK 아님 + STABILITY_UNVERIFIED (수행 양성증거 요구)")
        # 중복 출력물
        good = _fake_orca_out(hf="UHF", charge=0, mult=2, s2=0.752,
                              energies=(-1.0, -2.0))
        open(os.path.join(td, "b3", tagA + ".out"), "w").write(good)
        open(os.path.join(td, "b3", tagB + ".out"), "w").write(good)
        analyze_dir(NS(analyze=os.path.join(td, "b3")))
        ana = json.load(open(os.path.join(td, "b3", "analysis_stage_b.json")))
        chk("DUPLICATE_OUTPUT" in ana["jobs"][tagA].get("codes", []),
            "음성: 동일 .out 복사 → DUPLICATE_OUTPUT (realized ID 재사용 봉쇄)")

        # ══ 회신 R4 회귀시험 ④ — **주석 한 줄로 중복검사 우회** ═══════════════
        #   R4 실측: 출력에 아무 줄이나 하나 넣으면 파일 SHA 가 달라져 통과했다.
        open(os.path.join(td, "b3", tagB + ".out"), "w").write(
            good + "#  (사람이 나중에 붙인 메모 한 줄)\n")
        analyze_dir(NS(analyze=os.path.join(td, "b3")))
        ana = json.load(open(os.path.join(td, "b3", "analysis_stage_b.json")))
        cA = ana["jobs"][tagA].get("codes", [])
        chk("DUPLICATE_OUTPUT" not in cA,
            "  (전제) 주석 한 줄이면 바이트 SHA 가 달라져 DUPLICATE_OUTPUT 은 안 뜬다")
        chk("DUPLICATE_CONTENT" in cA and "DUPLICATE_CONTENT" in ana["jobs"][tagB]["codes"],
            "음성 R4④: 주석만 다른 복사본 → DUPLICATE_CONTENT 로 잡는다 (내용 지문)")

        # ══ 회신 R4 회귀시험 ⑤ — **중복으로 막힌 SP 의 종속 Opt** ═════════════
        #   종전 버그: by_cid 가 첫 루프에서 굳어 중복 게이트 뒤에도 OK 로 남아
        #   딸린 Opt 가 승인됐다. 이제 최종 gate 뒤 map 을 다시 만든다.
        open(os.path.join(td, "b3", tagAo + ".out"), "w").write(_fake_orca_out(
            hf="UHF", charge=0, mult=2, s2=0.753, stability="stable",
            opt_converged=True, energies=(-3.0,)))
        analyze_dir(NS(analyze=os.path.join(td, "b3")))
        ana = json.load(open(os.path.join(td, "b3", "analysis_stage_b.json")))
        chk(ana["jobs"][tagA]["status"] == "GATED",
            "  (전제) 선행 sp 는 중복으로 GATED 다")
        chk(ana["jobs"][tagAo]["status"] != "OK"
            and "DEPENDENCY_NOT_MET" in ana["jobs"][tagAo].get("codes", []),
            "음성 R4⑤: **중복으로 막힌** sp 의 종속 opt 도 DEPENDENCY_NOT_MET "
            "(종전엔 낡은 dependency map 때문에 OK 로 통과)")
        chk(ana["jobs"][tagAo]["realized"].get("realized_state_id") is None
            if "realized" in ana["jobs"][tagAo] else True,
            "  게이트된 잡에는 realized_state_id 를 발급하지 않는다")
        # 대문자 unstable · 마지막 에너지 · 의존성
        open(os.path.join(td, "b3", tagB + ".out"), "w").write(_fake_orca_out(
            hf="UHF", charge=0, mult=2, s2=0.751, stability="unstable_upper",
            energies=(-9.0,)))
        open(os.path.join(td, "b3", tagAo + ".out"), "w").write(_fake_orca_out(
            hf="UHF", charge=0, mult=2, s2=0.753, stability="stable",
            opt_converged=True, energies=(-3.0,)))
        analyze_dir(NS(analyze=os.path.join(td, "b3")))
        ana = json.load(open(os.path.join(td, "b3", "analysis_stage_b.json")))
        chk("STABILITY_UNSTABLE" in ana["jobs"][tagB]["codes"],
            "음성: 대문자 UNSTABLE 도 잡는다 (re.I)")
        chk(ana["jobs"][tagA]["realized"]["energy_Eh"] == -2.0,
            "에너지는 **마지막 값** (-2.0, 첫 값 -1.0 아님)")
        # 4라운드: sp 를 명시적으로 실패시켜 dependency 게이트 확인
        open(os.path.join(td, "b3", tagA + ".out"), "w").write(_fake_orca_out(
            hf="UHF", charge=0, mult=2, s2=0.750, stability="unstable",
            energies=(-4.0,)))
        analyze_dir(NS(analyze=os.path.join(td, "b3")))
        ana = json.load(open(os.path.join(td, "b3", "analysis_stage_b.json")))
        chk("DEPENDENCY_NOT_MET" in ana["jobs"][tagAo]["codes"],
            "음성: 선행 sp GATED(불안정) → opt DEPENDENCY_NOT_MET (R3 P0-3)")
        # ══ 회신 R4 회귀시험 ①~③ — analyzer fail-open 4종 ═══════════════════
        jb0 = jd["dp3_gs0_hA_d_sp_s0"]
        nat0 = jb0["n_atoms"]
        _as = {"backbone": list(range(nat0 // 2)),
               "rest": list(range(nat0 // 2, nat0))}

        # ① 안정성 — 임의 문자열이 stable 증거로 통과했다
        st, c, _ = analyze_out(_fake_orca_out(
            hf="UHF", charge=0, mult=2, s2=0.752, energies=(-1.0,),
            stability="banana"), jb0)
        chk("STABILITY_UNVERIFIED" in c,
            "음성 R4①: 'stability analysis indicates …' 뒤가 stable/unstable 이 아니면 "
            "**UNVERIFIED** (아무 문자열이나 통과하던 경로)")
        st, c, r = analyze_out(_fake_orca_out(
            hf="UHF", charge=0, mult=2, s2=0.752, energies=(-1.0,),
            stability="stable"), jb0)
        chk("STABILITY_UNVERIFIED" not in c and r.get("stability") == "stable",
            "  양성: 진짜 stable 문구는 통과하고 realized 에 남는다")

        # ② charge/mult echo 가 **아예 없으면** 통과했다
        st, c, _ = analyze_out(_fake_orca_out(
            hf="UHF", charge=0, mult=None, s2=0.752, energies=(-1.0,),
            stability="stable"), jb0)
        chk("SECTOR_UNVERIFIED" in c,
            "음성 R4②: multiplicity echo 가 없으면 **SECTOR_UNVERIFIED** "
            "(종전엔 `if mu and …` 라 조용히 통과)")

        # ③ BS 는 SP 에서도 안정성 면제였다
        # ⚠ n=3 매트릭스에는 pairs 가 없어 bs 잡이 안 생긴다. 매트릭스 구성에 의존하지
        #   않도록 **bs 잡을 직접 구성**해 analyze_out 의 그 분기를 곧장 친다.
        import copy as _copy
        jbs = _copy.deepcopy(jb0)
        jbs["conditioning"]["sector"] = "bs"
        jbs["conditioning"]["job_type"] = "sp_vertical"
        jbs["expected"]["mult"] = 1
        jbs["expected"]["s2_target"] = None
        st, c, _ = analyze_out(_fake_orca_out(
            hf="UHF", charge=jbs["expected"]["charge"], mult=1, s2=0.9,
            energies=(-1.0,), stability=None), jbs)
        chk("STABILITY_UNVERIFIED" in c,
            "음성 R4③: **BS SP 도 안정성 검사를 면제받지 않는다** "
            "(ORCA 가 UHF/UKS SP 에 지원하므로 면제엔 근거가 필요하다)")
        st, c, _ = analyze_out(_fake_orca_out(
            hf="UHF", charge=jbs["expected"]["charge"], mult=1, s2=0.9,
            energies=(-1.0,), stability="stable"), jbs)
        chk("STABILITY_UNVERIFIED" not in c,
            "  양성: BS 도 진짜 stable 문구가 있으면 통과한다")

        # ④ localization 블록이 없으면 아무 코드도 안 붙었다
        st, c, _ = analyze_out(_fake_orca_out(
            hf="UHF", charge=0, mult=2, s2=0.752, energies=(-1.0,),
            stability="stable"), jb0, atom_sets=_as)
        chk("LOCALIZATION_MISSING" in c,
            "음성 R4④: 열린 껍질인데 Löwdin 블록이 없으면 **hard gate** "
            "(종전엔 mvals is None 이라 조용히 통과)")

        # ⑤ 행 재배열 — index 를 무시하고 순서대로 읽던 경로
        good_sp = [0.9] + [0.0] * (nat0 - 1)
        txt = _fake_orca_out(hf="UHF", charge=0, mult=2, s2=0.752,
                             energies=(-1.0,), stability="stable", spins=good_sp)
        st, c, r = analyze_out(txt, jb0, atom_sets=_as)
        base_cls = r.get("localization_class")
        chk(base_cls is not None and "LOCALIZATION_MISSING" not in c,
            f"  양성: 정상 Löwdin 블록은 class 를 낸다 ({base_cls})")
        shuffled = txt.replace(f"  0 X :   0.000000   {good_sp[0]:.6f}\n", "")
        st2, c2, _ = analyze_out(shuffled, jb0, atom_sets=_as)
        chk("LOCALIZATION_MISSING" in c2,
            "음성 R4⑤: 행이 빠져 index 집합이 0..N-1 이 아니면 **판정 불가로 막는다** "
            "(종전엔 순서대로 읽어 원자가 통째로 밀린 채 통과)")

        # BS 미플립 · opt 미수렴 · charge/mult 불일치
        jb = jd["dp3_gs0_hA_d_sp_s0"]
        st, c, _ = analyze_out(_fake_orca_out(hf="UHF", charge=0, mult=2,
                                              s2=2.001, energies=(-1.0,)),
                               dict(jb, expected=dict(jb["expected"], s2_target="bs_window"),
                                    conditioning=dict(jb["conditioning"], sector="bs")))
        chk("NA_STATE_NOT_IDENTIFIED" in c,
            "음성: BS 인데 <S2>=2.0 (미플립 HS) → NA_STATE_NOT_IDENTIFIED")
        st, c, _ = analyze_out(_fake_orca_out(hf="UHF", charge=0, mult=2, s2=0.75,
                                              stability="stable", energies=(-1.0,)),
                               dict(jd["dp3_gs0_hA_d_opt_s0"]))
        chk("OPT_UNCONVERGED" in c, "음성: Opt 수렴 문구 없음 → OPT_UNCONVERGED")
        st, c, _ = analyze_out(_fake_orca_out(hf="UHF", charge=-1, mult=2, s2=0.75,
                                              stability="stable", energies=(-1.0,)), jb)
        chk("SECTOR_MISMATCH" in c, "음성: charge 불일치 → SECTOR_MISMATCH (echo 대조)")

        # ── localization class (사전 규칙 + remap)
        nat = jd[tagA]["n_atoms"]
        sets = manB["atom_sets_neutral_frame"]
        rmH = jd[tagA]["conditioning"]["removed_H_indices"]
        kill = sorted(rmH)
        def rmap(i):
            return i - sum(1 for k in kill if k < i)
        spins = [0.0] * nat
        for i in sets["backbone"]:
            if i not in kill:
                spins[rmap(i)] = 0.05
        st, c, r = analyze_out(_fake_orca_out(hf="UHF", charge=0, mult=2, s2=0.75,
                                              stability="stable", energies=(-1.0,),
                                              spins=spins),
                               jb, atom_sets=sets, removed_H=rmH)
        chk(r.get("localization_class") == "backbone",
            f"localization class: 백본 집중 스핀 → 'backbone' (remap 경유, share "
            f"{r.get('loc_shares', {}).get('backbone')})")
        spins2 = [0.0] * nat
        for gname in ("sulfonate_A", "sulfonate_B", "sulfonate_C"):
            for i in sets[gname]:
                if i not in kill:
                    spins2[rmap(i)] = 0.05
        st, c, r2 = analyze_out(_fake_orca_out(hf="UHF", charge=0, mult=2, s2=0.75,
                                               stability="stable", energies=(-1.0,),
                                               spins=spins2),
                                jb, atom_sets=sets, removed_H=rmH)
        chk(r2.get("localization_class") == "MIXED_UNRESOLVED",
            "localization class: 분산 스핀 → MIXED_UNRESOLVED (사전 규칙)")

        # ── hybrid: species 분리 + NoAutoStart
        fkman = {"jobs": [
            {"tag": "u", "conditioning": {"species": "DP6_h1_Q0", "job_type": "sp_vertical"}},
            {"tag": "v", "conditioning": {"species": "DP6_h2_Q0", "job_type": "sp_vertical"}},
        ]}
        fkana = {"jobs": {
            "u": {"status": "OK", "realized": {"energy_Eh": -10.0}},
            "v": {"status": "OK", "realized": {"energy_Eh": -9.0}},
        }}
        pick = hybrid_select(fkana, fkman)
        chk(set(pick) == {"u", "v"},
            "hybrid: 조성(h1/h2)별 그룹 분리 — 서로의 0.10 eV 창에 안 섞인다 (R3 P0-5)")
        hp = os.path.join(td, "hyb.inp")
        make_inp(hp, "x.xyz", "UKS", 3, False, "sp_vertical", hybrid=True)
        chk("NoAutoStart" in open(hp).read(),
            "hybrid 입력: NoAutoStart 키워드로 fresh-start 강제 (주석 아님)")

        # ── U_PCET cycles + ID 규율
        cyc = manB.get("u_pcet_cycles", [])
        chk(cyc == [], "n=3 은 pair 없음 → cycle 0 (정합)")
        raises(lambda: calculation_id({"a": 1, "nested": {"realized_x": 2}}),
               "음성: **중첩** realized 도 ID 발급 거부 (R3 P1)")

        # ── n=6 매트릭스 + cycles (unverified 부모 — 시험 전용 경로)
        a6 = NS(dimer=dim, out=os.path.join(td, "a6"), cc=CC_NEW, step=30, n=6,
                seeds=2, allow_noncanonical=True, allow_underseed=True)
        stage_a(a6, sym, pos)
        b6 = NS(stage_a_manifest=None, neutral_out=None,
                neutral_xyz=os.path.join(a6.out, "gs0", "dp6_gs0_neutral.xyz"),
                out=os.path.join(td, "b6"), n=6, gseed=0, patterns=None,
                allow_partial=False, allow_noncanonical=True, scf_seeds=1,
                allow_unverified_parent=True)
        man6 = stage_b(b6)
        pats = set(man6["generated_patterns"])
        chk(pats == {"B", "C", "D", "E", "C,D", "B,E", "A,F", "B,C"},
            "n=6 매트릭스 전건 (singles 4 + pairs 4)")
        cyc6 = man6["u_pcet_cycles"]
        pairs6 = {c["pair"] for c in cyc6}
        chk(pairs6 == {"C,D", "B,E", "B,C"} and len(cyc6) == 6
            and all(set(c["legs"]) >= {"h1a", "h1b", "h2_s", "h2_t", "h2_bs", "h0"}
                    for c in cyc6),
            "U_PCET cycles: CD/BE/BC × vert/ad = 6, 4-leg calc_id 결속 · A,F 제외 (R3 조건 9)")
        s6 = open(os.path.join(td, "b6", "dp6_gs0_hCD_s_sp_s0.inp")).read()
        chk(s6.startswith("! RKS") and "UNO" not in s6 and "Hirshfeld" in s6,
            "h2 RKS 후보: RKS + Hirshfeld (UNO 는 UHF 전용이라 제외)")
        mtxt = json.dumps(man6, ensure_ascii=False)
        chk("bipolaron" not in mtxt and "backbone hole" not in mtxt,
            "conditioning 순수성 유지")

        # ── 레거시 하위호환 (직접 호출)
        aL = NS(dimer=dim, out=os.path.join(td, "leg"), cc=CC_NEW, step=30)
        os.makedirs(aL.out)
        build_legacy_trimer(aL, sym, pos)
        chk(os.path.exists(os.path.join(aL.out, "trimer_neutral.xyz")),
            "레거시 트라이머 경로 하위호환 (--legacy 로만 진입)")

    # ⚠ 2026-08-31 — 종전엔 여기서 PASS 를 찍고 **그 뒤로 폴라론 시험을 더 돌았다**.
    #   실패해도 화면에는 PASS 가 먼저 남아 오해를 부른다. 인쇄는 맨 끝으로 옮겼다.
    print("── 조립·stage 절 끝 (누적 실패 %d) ──" % len(fails))
    # ══ 폴라론 pilot (회신 S) — 음성 경로 포함 ═══════════════════════════
    print("── 폴라론 pilot ──")
    # 합성 계: ring 2개(각 S+4C) · 에테르 O 2개/ring · sulfonate 2개 · 나머지
    _sym = (["S"] + ["C"] * 4 + ["O"] * 2) * 2 + ["S", "O", "O", "O", "H"] * 2 + ["C", "H"]
    _n = len(_sym)
    _nb = {i: [] for i in range(_n)}
    _rings = [{"ring": [0, 1, 2, 3, 4], "rS": 0, "alphas": []},
              {"ring": [7, 8, 9, 10, 11], "rS": 7, "alphas": []}]
    for r, o0 in ((0, 5), (7, 12)):
        for c, o in ((r + 1, o0), (r + 2, o0 + 1)):
            _nb[c].append(o); _nb[o].append(c)
    _sulf = [{"sS": 14, "sO": [15, 16, 17], "aH": 18, "ring": 0},
             {"sS": 19, "sO": [20, 21, 22], "aH": 23, "ring": 1}]
    _am = pilot_atom_sets(_sym, _nb, _rings, _sulf, ether_in_backbone=True)
    chk(sum(len(v) for v in _am["sets"].values()) == _n,
        "pilot: 세 집합이 **완전**하다 (합 = 전체 원자수)")
    chk(not (set(_am["sets"]["backbone"]) & set(_am["sets"]["sulfonate"])),
        "pilot: backbone 과 sulfonate 가 **상호배타**다")
    chk(len(_am["sets"]["backbone"]) == 14,
        f"pilot: 에테르 O 가 backbone 에 들어간다 (실제 {len(_am['sets']['backbone'])}, 기대 14)")
    _am0 = pilot_atom_sets(_sym, _nb, _rings, _sulf, ether_in_backbone=False)
    chk(len(_am0["sets"]["backbone"]) == 10 and _am0["hash"] != _am["hash"],
        "⛔음성: 에테르 O 를 빼면 backbone 이 줄고 **hash 가 달라진다** (분할 선택이 기록된다)")
    # ⛔음성 — 집합이 겹치면 멈춘다
    raises(lambda: pilot_atom_sets(
        _sym, _nb, _rings,
        [{"sS": 14, "sO": [15, 16, 1], "aH": None, "ring": 0}],
        ether_in_backbone=True),
        "⛔음성 pilot: backbone 과 sulfonate 가 겹치면 **멈춘다** (조용히 한쪽에 안 넣는다)")

    # ⛔음성 — **v1 식(분자 signed)이면 틀리는** 경우를 만든다 (회신 S Q1)
    _m = [0.0] * _n
    _m[1], _m[2] = +0.5, -0.5          # 백본 안에서 부호가 반대인 두 lobe
    _m[15] = 0.2                        # sulfonate 에 약간
    _sh = pilot_shares(_m, _am)
    _signed = sum(_m[i] for i in _am["sets"]["backbone"]) / sum(abs(x) for x in _m)
    chk(abs(_sh["F"]["backbone"] - (1.0 / 1.2)) < 1e-9 and abs(_signed) < 1e-9,
        f"⛔음성 AO/S Q1: 백본 내부 양·음 lobe 가 **signed 식에서는 0 으로 상쇄**되지만"
        f" 절대값 식은 {_sh['F']['backbone']:.3f} 를 준다 (signed {_signed:.3f})")
    chk(abs(_sh["M"]["backbone"]) < 1e-9,
        "pilot: signed net spin(M_bb)은 **버리지 않고 따로** 보존한다")
    chk(abs(sum(_sh["F"].values()) - 1.0) < 1e-9, "pilot: F 합이 1 이다")

    # class 규칙 — 문턱과 **여유** 둘 다
    chk(pilot_class({"backbone": 0.70, "sulfonate": 0.20, "other": 0.10})[0] == "BACKBONE",
        "pilot: 유일 집합이 0.5 이상이고 여유가 있으면 class 부여")
    chk(pilot_class({"backbone": 0.52, "sulfonate": 0.46, "other": 0.02})[0]
        == "MIXED_UNRESOLVED",
        "⛔음성 S Q1: 0.52 vs 0.46 은 **여유 0.10 미달** → MIXED_UNRESOLVED "
        "(문턱만 넘으면 통과시키지 않는다)")
    chk(pilot_class({"backbone": 0.30, "sulfonate": 0.10, "other": 0.60})[0]
        == "OTHER_DOMINANT",
        "⛔음성 S Q1: other 가 크면 backbone−sulfonate 만으로 판정하지 않는다")
    chk(pilot_threshold_sensitivity(
            {"backbone": 0.55, "sulfonate": 0.44, "other": 0.01})["threshold_dependent"],
        "⛔음성 S: 0.4/0.5/0.6 경계에서 class 가 바뀌면 THRESHOLD_DEPENDENT")
    chk(pilot_partition_check({"backbone": 0.70, "sulfonate": 0.2, "other": 0.1},
                              {"backbone": 0.40, "sulfonate": 0.5, "other": 0.1}
                              )["partition_dependent"],
        "⛔음성 S Q1: 두 분할의 class 가 갈리면 PARTITION_DEPENDENT")
    chk(not pilot_partition_check({"backbone": 0.70, "sulfonate": 0.2, "other": 0.1},
                                  {"backbone": 0.72, "sulfonate": 0.18, "other": 0.1}
                                  )["partition_dependent"],
        "pilot: 두 분할이 같은 class·비슷한 F_bb 면 통과")
    chk(pilot_partition_check(None, {"backbone": 0.7})["ok"] is False,
        "⛔음성 S Q1: 한쪽 분할이 **없으면** 통과가 아니다 (둘 다 계산해야 한다)")

    # N_eff · span80
    _m2 = [0.0] * _n
    for i in _am["rings"]["ring0"]:
        _m2[i] = 1.0
    _s2 = pilot_shares(_m2, _am)
    chk(abs(_s2["N_eff"] - 1.0) < 1e-6 and _s2["span80"] == 1,
        f"pilot: 한 링에 몰리면 N_eff=1 · span80=1 (실제 {_s2['N_eff']:.3f}/{_s2['span80']})")
    _m3 = [0.0] * _n
    for k in ("ring0", "ring1"):
        for i in _am["rings"][k]:
            _m3[i] = 1.0
    _s3 = pilot_shares(_m3, _am)
    chk(abs(_s3["N_eff"] - 2.0) < 1e-6 and _s3["span80"] == 2,
        f"pilot: 두 링에 고르면 N_eff=2 · span80=2 (실제 {_s3['N_eff']:.3f}/{_s3['span80']})")

    # seed 선택 — 문턱 미달이면 **고르지 않는다**
    _pops = {10: {i: 90.0 / len(_am["rings"]["ring0"]) for i in _am["rings"]["ring0"]},
             11: {0: 5.0}}
    _occ = {10: 2.0, 11: 2.0}
    _mo, _w = pil_pick_seed_mo(_pops, _occ, _am["rings"]["ring0"], core_window=0)
    chk(_mo == 10 and _w > 80.0, f"pilot: 목표 집합에 크게 걸린 MO 를 고른다 (mo {_mo}, {_w:.0f}%)")
    _mo2, _w2 = pil_pick_seed_mo({11: {0: 5.0}}, {11: 2.0}, _am["rings"]["ring0"],
                                 core_window=0)
    chk(_mo2 is None,
        "⛔음성 S Q2: 목표 집합에 문턱(40%) 미만인 MO 밖에 없으면 **seed 를 만들지 않는다** "
        "(국재화 실패를 임의 선택으로 덮지 않는다)")
    _mo3, _ = pil_pick_seed_mo({10: {i: 99.0 for i in _am["rings"]["ring0"]}},
                               {10: 0.0}, _am["rings"]["ring0"], core_window=0)
    chk(_mo3 is None, "⛔음성: **비점유** MO 는 seed 후보가 아니다")

    # ══ 회신 U P0-4 — 코어 배제는 **국재 MO 에너지가 아니라** canonical 창 + AO 성격 ══
    _r0 = _am["rings"]["ring0"]
    _pc = {3: {i: 100.0 / len(_r0) for i in _r0},        # C 1s — 링에 100%
           40: {i: 70.0 / len(_r0) for i in _r0}}        # 원자가 π — 70%
    _oc = {3: 2.0, 40: 2.0}
    chk(pil_pick_seed_mo(_pc, _oc, _r0, core_window=4)[0] == 40,
        "회신 U P0-4: 링에 100% 걸린 **코어**(canonical 창 안, index<4) 대신 원자가 MO "
        "를 고른다 (코어 홀은 폴라론이 아니다)")
    chk(pil_pick_seed_mo(_pc, _oc, _r0, core_window=None)[0] is None,
        "⛔음성 U P0-4: canonical 코어 창이 **없으면 아무것도 고르지 않는다** — "
        "종전엔 `ener=None` 이면 코어를 그냥 뽑았다 (fail-open 이었다)")
    chk(pil_pick_seed_mo({3: {i: 100.0 / len(_r0) for i in _r0}}, {3: 2.0}, _r0,
                         core_window=4)[0] is None,
        "⛔음성: 코어를 거르고 나면 후보가 **하나도 없을** 수 있다 — 그때도 "
        "임의로 고르지 않는다")
    # ⛔음성 — canonical 에너지 파서 + 창
    _oe_txt = ("ORBITAL ENERGIES\n----------------\n"
               "  NO   OCC          E(Eh)            E(eV)\n"
               "   0   2.0000     -88.757030     -2415.2\n"
               "   1   2.0000     -10.210000      -277.8\n"
               "   2   2.0000      -0.810000       -22.0\n"
               "   3   0.0000       0.120000         3.3\n")
    _oe = pil_parse_orbital_energies(_oe_txt)
    chk(_oe is not None and len(_oe) == 4 and abs(_oe[0][1] + 88.75703) < 1e-6,
        "회신 U P0-4: canonical `ORBITAL ENERGIES` 를 읽는다 (국재화 **전** 값)")
    chk(pil_core_window(_oe, -3.0)[0] == 2,
        "회신 U P0-4: T_CORE −3 Eh 아래 점유 궤도 2개가 코어 창이다")
    chk(pil_core_window(None, -3.0)[0] is None and pil_core_window({}, -3.0)[0] is None,
        "⛔음성 U P0-4: 에너지를 못 읽으면 창이 **None** 이다 (0 이 아니다 — "
        "0 이면 '코어 없음' 으로 통과시켜 버린다)")
    chk(pil_core_window({0: (2.0, -0.5), 1: (2.0, -10.2)}, -3.0)[0] is None,
        "⛔음성 U P0-4: 코어가 앞쪽에 **연속**이 아니면 index 창을 만들 수 없다")
    chk(pil_core_window({0: (0.0, -10.2)}, -3.0)[0] is None,
        "⛔음성 U P0-4: 코어로 센 궤도에 **비점유**가 섞이면 블록 판독이 어긋난 것이다")
    # ⛔음성 — AO 성격으로도 코어를 잡는다 (창이 어긋나도 두 번째 그물)
    chk(pil_mo_is_core({0: {"1s": 99.0}}, ["C"])[0],
        "회신 U P0-4: C 의 `1s` 지배 MO 는 AO 성격만으로 코어다")
    chk(not pil_mo_is_core({0: {"2pz": 99.0}}, ["C"])[0],
        "⛔음성 U P0-4: C 의 `2pz` 는 원자가다 — 코어로 세면 안 된다")
    chk(pil_mo_is_core({0: {"2p": 99.0}}, ["S"])[0]
        and not pil_mo_is_core({0: {"3p": 99.0}}, ["S"])[0],
        "회신 U P0-4: 코어 껍질은 **원소마다 다르다** (S 는 2p 가 코어, 3p 가 원자가)")
    chk(pil_pick_seed_mo({7: {i: 99.0 for i in _r0}}, {7: 2.0}, _r0, core_window=0,
                         aos={7: {i: {"1s": 99.0} for i in _r0}},
                         sym=["C"] * (max(_r0) + 1))[0] is None,
        "⛔음성 U P0-4: canonical 창이 0 이어도 **AO 성격**이 코어를 잡는다 "
        "(창과 성격은 서로의 예비다)")
    chk(pil_parse_mopop("아무 관계 없는 출력", 10) is None,
        "⛔음성: MO 인구 블록이 없으면 None (임의로 고르지 않는다)")
    # ⛔음성 2026-08-31 실측 — ORCA 6.1.1 의 실제 헤더에 **REDUCED 가 없다**.
    #   종전 파서는 REDUCED 붙은 것만 찾아 실물에서 **항상 None** 이었다
    #   (phase L 이 정상 종료했는데 seed 를 하나도 못 만들었다).
    chk(all(h in PIL_MOPOP_HDRS for h in
            ("LOEWDIN ORBITAL POPULATIONS PER MO",
             "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO")),
        "⛔음성 실측: 헤더를 **REDUCED 유무 둘 다** 받는다 (판본차)")
    chk(pil_parse_mopop("LOEWDIN REDUCED ORBITAL CHARGES\n 0 C  s  99.8\n", 10) is None,
        "⛔음성 실측: `LOEWDIN REDUCED ORBITAL CHARGES` 는 **다른 블록**이다 "
        "(원자별 전하이지 MO 별 인구가 아니다 — 이름이 비슷해 헷갈린다)")
    # ⛔음성 2026-08-31 실측 — 실제 행은 인덱스와 원소가 **붙어 있다** (`36S`·`102S`).
    #   종전 정규식은 사이 공백을 요구해 **한 행도 안 맞았고** pops 가 비었다.
    _real = ("LOEWDIN ORBITAL POPULATIONS PER MO\n"
             "----------------------------------\n"
             "THRESHOLD FOR PRINTING IS 0.1%\n"
             "                      0         1         2\n"
             "                 -88.75703 -88.74156  -0.31000\n"
             "                   2.00000   2.00000   2.00000\n"
             "                  --------  --------  --------\n"
             "  2S   1s             97.0       0.0       0.0\n"
             " 36S   3pz             0.0       0.0      55.0\n"
             "102S   1s              0.0      97.0       0.0\n")
    _pr = pil_parse_mopop(_real, 200)
    chk(_pr is not None and _pr[0][0].get(2) and _pr[0][2].get(36) == 55.0,
        "⛔음성 실측: `  2S   1s` 처럼 **인덱스+원소가 붙은** 실제 형식을 읽는다")
    chk(_pr is not None and abs(_pr[2][0] + 88.75703) < 1e-6 and _pr[1][0] == 2.0,
        "실측: MO 에너지·점유수도 같이 읽는다 (코어 배제에 필요하다)")
    # ⛔음성 — 그 실측 형식에서도 코어(−88.8 Eh)는 seed 로 안 뽑힌다
    _m4, _ = pil_pick_seed_mo(_pr[0], _pr[1], [36], core_window=2,
                              aos=_pr[3], sym=["S"] * 200)
    chk(_m4 == 2,
        f"⛔음성 실측: 코어 MO(canonical 창 index<2)를 건너뛰고 원자가 MO 를 고른다 "
        f"(실제 {_m4})")
    # ⛔음성 2026-08-31 실측 — 고른 MO 가 **HOMO 자체**면 회전이 없어야 한다
    #   (ring5 → mo 480 = HOMO 480). Rotate{480,480} 은 자기 자신과 회전이다.
    _td = tempfile.mkdtemp()
    _txt_h = _pil_inp(os.path.join(_td, "h.inp"),
                      "x.xyz", 0, 2, "UKS", 1.0, "r2SCAN-3c",
                      moread="p.loc", rotate=None, stab=True)
    chk("Rotate" not in _txt_h,
        "⛔음성 실측: 고른 MO 가 HOMO 자체면 **Rotate 를 쓰지 않는다** "
        "(자기 자신과 회전은 무의미하다)")
    _txt_r = _pil_inp(os.path.join(_td, "r.inp"),
                      "x.xyz", 0, 2, "UKS", 1.0, "r2SCAN-3c",
                      moread="p.loc", rotate=(237, 480), stab=True)
    chk("Rotate {237, 480, 90, 1, 1}" in _txt_r and 'moinp "p.loc"' in _txt_r,
        "실측: 회전이 필요하면 Rotate 를 쓰고 **.loc** 를 MORead 한다")

    # ══ 회신 T P0-2 — 고른 MO 가 **π / O-nonbonding 인가** ═══════════════════
    #   "그 링에 99%" 는 공간 위치일 뿐이다. σ 결합이나 lone pair 도 그만큼 국재된다.
    #   xy 평면에 놓인 5원환 → 법선은 z. π 면 p 밀도가 z 에 몰린다.
    import math as _mth
    _rsym = ["S", "C", "C", "C", "C"]
    _rid = [0, 1, 2, 3, 4]

    def _rot3(a, b, c):
        """Z-Y-Z 오일러 회전행렬 — 링을 **일반 방향**으로 기울인다."""
        ca, sa, cb, sb, cc, sc = (_mth.cos(a), _mth.sin(a), _mth.cos(b),
                                  _mth.sin(b), _mth.cos(c), _mth.sin(c))
        rz1 = [[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]]
        ry = [[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]]
        rz2 = [[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]]
        def mm(X, Y):
            return [[sum(X[i][k] * Y[k][j] for k in range(3)) for j in range(3)]
                    for i in range(3)]
        return mm(mm(rz1, ry), rz2)

    def _ring_pi_case(R):
        """회전 R 로 기울인 5원환 + 그 법선을 향한 **완전한 π** MO.

        → (pos, 인구 ao, 계수 coef, 법선). 인구는 대각뿐(|c|²), 계수는 벡터다.
        """
        base = [[_mth.cos(2 * _mth.pi * k / 5), _mth.sin(2 * _mth.pi * k / 5), 0.0]
                for k in range(5)]
        pos = [[sum(R[i][j] * q[j] for j in range(3)) for i in range(3)] for q in base]
        nrm = [R[i][2] for i in range(3)]                 # z 축이 법선
        ao = {i: {"2s": 2.0,
                  "2px": 90.0 * nrm[0] ** 2, "2py": 90.0 * nrm[1] ** 2,
                  "2pz": 90.0 * nrm[2] ** 2} for i in _rid}
        cf = {i: {"2s": 0.05, "2px": nrm[0], "2py": nrm[1], "2pz": nrm[2]}
              for i in _rid}
        return pos, ao, cf, nrm

    # ── 양성: 축 정렬 (종전 fixture 가 쓰던 유일한 경우) ───────────────────────
    _rp, _pi_ao, _pi_cf, _ = _ring_pi_case(_rot3(0.0, 0.0, 0.0))
    _chpi = pil_mo_character(_pi_ao, _rid, _rsym, _rp, _rid, coef_mo=_pi_cf)
    chk(pil_character_verdict(_chpi, "pi")[0] and _chpi["pi_share"] > 0.99,
        "회신 T P0-2 양성: 고리 법선에 몰린 p 밀도는 **π 로 통과**한다 "
        "(π %.3f · p %.2f)" % (_chpi["pi_share"], _chpi["p_frac"]))

    # ⛔⛔ 회신 U P0-2 — **회전 불변성.** 종전 식 Σn_k²p_k/Σp_k 는 축 정렬에서만
    #   1 이고 일반 방향에서 Σn_k⁴ 로 무너진다 (대각선 법선이면 1/3).
    #   리뷰어가 부모 구조 여섯 고리에 이상적 p_normal 을 넣어 0.34~0.67 을 재현했다.
    #   ⇒ **여러 방향에서 전부 1** 이어야 한다. 이 시험이 있었으면 그때 잡혔다.
    _rot_cases = [(0.7, 0.9, 0.3), (1.1, 0.6, 2.0), (0.3, 1.2, 1.7),
                  (2.4, 0.955, 0.785), (0.0, _mth.acos(1 / 3 ** 0.5), _mth.pi / 4)]
    _pis, _olds = [], []
    for _a, _b, _c in _rot_cases:
        _p2, _ao2, _cf2, _n2 = _ring_pi_case(_rot3(_a, _b, _c))
        _ch2 = pil_mo_character(_ao2, _rid, _rsym, _p2, _rid, coef_mo=_cf2)
        _pis.append(_ch2["pi_share"] if _ch2["pi_share"] is not None else -1.0)
        # 종전 식을 그 자리에서 다시 계산해 **무너지는 것**을 기록한다
        _pv = [sum(_ao2[i]["2p" + ax] for i in _rid) for ax in "xyz"]
        _olds.append(sum(_n2[k] ** 2 * _pv[k] for k in range(3)) / sum(_pv))
    chk("pi_orientation_score" in _chpi and "⚠_pi_이름" in _chpi
        and "물리적 π share 가 아니다" in _chpi["⚠_pi_이름"],
        "회신 V Q1: 이 값을 **방향 점수**로 부르고, raw AO 계수가 Löwdin 인구가 "
        "아니라는 단서를 산출물에 싣는다 (원고에 'π 성분 N%' 로 적지 않는다)")
    chk(all(p > 0.99 for p in _pis),
        "회신 U P0-2 **회전불변**: 이상적 p_normal 은 어느 방향에서도 π=1 이다 "
        "(%s)" % " ".join("%.3f" % p for p in _pis))
    chk(min(_olds) < PIL_PI_MIN,
        "⛔음성 U P0-2 재현: **종전 대각 인구식**은 같은 완전한 π 를 최저 %.3f 로 "
        "떨어뜨린다 (문턱 %.2f) — 축 정렬 fixture 만 있어서 152건이 통과했다"
        % (min(_olds), PIL_PI_MIN))
    _p3, _ao3, _cf3, _ = _ring_pi_case(_rot3(*_rot_cases[0]))
    _ch3 = pil_mo_character(_ao3, _rid, _rsym, _p3, _rid)            # 계수 없이
    _ok3, _w3 = pil_character_verdict(_ch3, "pi")
    chk(not _ok3 and "UNRESOLVED" in _w3 and _ch3["pi_basis"] is None,
        "⛔음성 U P0-2: **계수 없이는 통과가 없다** — 같은 완전한 π 라도 대각 인구만 "
        "주면 MO_CHARACTER_UNRESOLVED 다 (상한으로 기각만 가능)")

    # ── 음성: 면내 p(σ) · s 지배 · 축 미분해 ─────────────────────────────────
    _sg_ao = {i: {"2s": 2.0, "2px": 45.0, "2py": 45.0, "2pz": 1.0} for i in _rid}
    _sg_cf = {i: {"2s": 0.05, "2px": 0.7, "2py": 0.7, "2pz": 0.02} for i in _rid}
    _chsg = pil_mo_character(_sg_ao, _rid, _rsym, _rp, _rid, coef_mo=_sg_cf)
    _ok_sg, _w_sg = pil_character_verdict(_chsg, "pi")
    chk(not _ok_sg and "SEED_NOT_PI" in _w_sg and _chsg["pi_share"] < 0.1,
        "⛔음성 T P0-2: **면내 p(σ)** 는 그 링에 100%% 국재돼도 막는다 "
        "(π %.3f) — 공간 국재가 π 를 보증하지 않는다" % _chsg["pi_share"])
    _s_ao = {i: {"2s": 90.0, "2px": 2.0, "2py": 2.0, "2pz": 2.0} for i in _rid}
    _chs = pil_mo_character(_s_ao, _rid, _rsym, _rp, _rid,
                            coef_mo={i: {"2s": 0.95} for i in _rid})
    chk(not pil_character_verdict(_chs, "pi")[0],
        "⛔음성 T P0-2: **s 지배** MO 도 막는다 (p 성분 %.2f)" % _chs["p_frac"])
    # 축 없이 찍힌 판본 — 확인 못 함은 통과가 아니다
    _chna = pil_mo_character({i: {"s": 2.0, "p": 90.0} for i in _rid},
                             _rid, _rsym, _rp, _rid)
    _ok_na, _w_na = pil_character_verdict(_chna, "pi")
    chk(not _ok_na and "UNRESOLVED" in _w_na and _chna["axis_resolved"] is False,
        "⛔음성 T P0-2: ORCA 가 p 를 **축 없이** 찍으면 π 를 확인할 수 없다 — "
        "확인 못 한 것은 통과가 아니다")
    # ⛔음성 U P0-2 — 상한만으로도 **기각**은 할 수 있다 (엄밀한 부등식이라 안전)
    # ⛔음성 회신 V Q2 — 상한은 **엄밀하지 않다** (인쇄 threshold 로 인구가 생략된다).
    #   따라서 상한이 문턱보다 작아도 **기각 근거로 쓰지 않는다** — UNRESOLVED 다.
    _chub = pil_mo_character(_sg_ao, _rid, _rsym, _rp, _rid)          # 계수 없음
    _ok_ub, _w_ub = pil_character_verdict(_chub, "pi")
    chk(not _ok_ub and "UNRESOLVED" in _w_ub,
        "⛔음성 V Q2: 계수가 없으면 상한이 작아도 **UNRESOLVED** 다 — Cauchy–Schwarz "
        "상한은 인쇄 threshold 때문에 엄밀하지 않다 (상한 %s 는 진단용)"
        % (_chub.get("pi_upper"),))
    chk("엄밀한 상한이 아니다" in (pil_mo_character.__doc__ or ""),
        "회신 V Q2: 상한이 왜 판정에 못 쓰이는지가 docstring 에 적혀 있다")
    # ── MO 계수 파서 (실물 형식) ──────────────────────────────────────────────
    _mo_txt = ("MOLECULAR ORBITALS\n------------------\n"
               "                      0         1\n"
               "                  -19.25187  -1.10000\n"
               "                   2.00000   2.00000\n"
               "                  --------  --------\n"
               "  0O   1s         0.999000 -0.210000\n"
               "  0O   2pz        0.010000  0.880000\n"
               "  1C   2pz       -0.020000  0.410000\n")
    _mp = pil_parse_mos(_mo_txt, 200)
    chk(_mp is not None and abs(_mp[1][0]["2pz"] - 0.88) < 1e-9
        and abs(_mp[0][1]["2pz"] + 0.02) < 1e-9,
        "회신 U P0-2: `MOLECULAR ORBITALS` 계수 블록을 읽는다 (index+원소 붙은 실물 형식)")
    chk(pil_parse_mos("아무 관계 없는 출력", 200) is None,
        "⛔음성 U P0-2: 계수 블록이 없으면 None — 임의로 π 를 판정하지 않는다")
    chk(pil_parse_mos(_mo_txt, 1) is None,
        "⛔음성 U P0-2: 원자 index 가 계 크기를 넘으면 판독 실패로 본다")
    chk("Print[P_MOs] 1" in PIL_MOPOP_KW,
        "회신 U P0-2: 입력이 실제로 MO 계수를 찍게 한다 (없으면 seed 생성이 멈춘다)")
    # sulfonate seed — O 위 nonbonding 인가
    _so_sym = ["S", "O", "O", "O"]
    _so_pos = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    _onb = {1: {"2px": 30.0, "2py": 30.0}, 2: {"2pz": 30.0}, 3: {"2s": 2.0}}
    chk(pil_character_verdict(
        pil_mo_character(_onb, [0, 1, 2, 3], _so_sym, _so_pos), "onb")[0],
        "회신 T P0-2 양성: sulfonate seed 가 **O 위 p(lone pair)** 면 통과")
    _sonb = {0: {"3s": 80.0}, 1: {"2s": 10.0}}      # S 위 s 지배 — nonbonding 아님
    _ok_so, _w_so = pil_character_verdict(
        pil_mo_character(_sonb, [0, 1, 2, 3], _so_sym, _so_pos), "onb")
    chk(not _ok_so and "NOT_O_NONBONDING" in _w_so,
        "⛔음성 T P0-2: S 위 s 지배 MO 는 sulfonate seed 로 안 받는다")

    # ══ 회신 T P0-1 · Q3 — P(200)/D(199) 프레임을 **각각** 봉인한다 ═══════════
    #   실물 구조로 친다 — 합성 픽스처는 인덱스 이동을 재현하지 못한다.
    _gs0 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), "db", "structures", "sdcp_orca_gs0",
        "dp6_gs0_neutral_final.xyz")
    if os.path.isfile(_gs0):
        _sy, _po = read_xyz(_gs0)
        _nb2, _rg2, _su2 = analyze(_sy, _po)
        _ac2 = pilot_acidic_h(_sy, _nb2, _su2)
        _sH2 = _ac2[len(_ac2) // 2][3]
        _amf2 = pilot_atom_manifest(_sy, _nb2, _rg2, _su2, [_sH2])
        chk(_amf2["P"]["n_atoms"] == len(_sy)
            and _amf2["D"]["n_atoms"] == len(_sy) - 1,
            "회신 T P0-1: P(%d)/D(%d) 원자수가 다르다 — 한 해시로 둘을 못 가리킨다"
            % (_amf2["P"]["n_atoms"], _amf2["D"]["n_atoms"]))
        chk(_amf2["P"]["hash"] != _amf2["D"]["hash"],
            "⛔음성 T P0-1: 두 프레임의 해시가 **다르다** (같으면 구분이 없는 것)")
        _cP, _cD = _amf2["P"]["counts"], _amf2["D"]["counts"]
        chk(_cP["sulfonate"] - _cD["sulfonate"] == 1
            and _cP["bb_core"] == _cD["bb_core"]
            and _cP["ether_O"] == _cD["ether_O"]
            and _cP["other"] == _cD["other"],
            "회신 T P0-1: 빠지는 원자는 **sulfonate 의 산성 H 하나뿐**이다 "
            "(P %s → D %s)" % (_cP, _cD))
        for _fr in ("P", "D"):
            _d = _amf2[_fr]
            chk(sum(_d["counts"].values()) == _d["n_atoms"],
                "회신 T Q3: %s 프레임의 네 성분이 상호배타·완전하다 (%s = %d)"
                % (_fr, _d["counts"], _d["n_atoms"]))
            chk(len(_d["derived"]["backbone_extended"])
                == len(_d["derived"]["backbone_strict"]) + _d["counts"]["ether_O"],
                "회신 T Q3: %s 의 extended = strict + ether_O (%d = %d + %d)"
                % (_fr, len(_d["derived"]["backbone_extended"]),
                   len(_d["derived"]["backbone_strict"]), _d["counts"]["ether_O"]))
        # ⛔음성 — D 프레임의 어떤 인덱스도 원자수를 넘지 않는다
        _bad = [i for g in _amf2["D"]["components"].values() for i in g
                if i >= _amf2["D"]["n_atoms"]]
        chk(not _bad,
            "⛔음성 T P0-1: D 프레임 인덱스가 원자수를 넘지 않는다 (넘으면 200원자 "
            "집합을 199원자 계에 쓴 것이다) · 위반 %s" % _bad[:3])
        # remap 이 실제로 한 칸씩 당기는가
        _rmp = _amf2["remap"]["explicit_P_to_D"]
        chk(_rmp[str(_sH2)] is None and _rmp[str(_sH2 - 1)] == _sH2 - 1
            and _rmp[str(_sH2 + 1)] == _sH2,
            "회신 T P0-1: remap 이 제거 H(%d) 를 없애고 그 뒤를 한 칸 당긴다" % _sH2)
    else:
        chk(False, "회신 T P0-1: gs0 구조를 못 찾아 프레임 시험을 건너뛰었다 "
                   "(건너뛴 것을 통과로 세지 않는다)")

    # ══ 회신 T P0-3 — `.loc` reader 3종 세트와 결정론 국재화 ═══════════════
    for _t, _why in ((_txt_r, "회전 있는 seed"), (_txt_h, "회전 없는 seed")):
        chk("Guess MORead" in _t and "GuessMode CMatrix" in _t
            and "%moinp" in _t and "NoAutoStart" in _t,
            "회신 T P0-3: %s 입력에 `Guess MORead + MOInp + GuessMode CMatrix` 가 "
            "**셋 다** 있다" % _why)
    # ⛔음성 — CMatrix 가 없으면 국재 MO 가 에너지 기준으로 재정렬될 수 있고,
    #   그러면 인덱스로 지정한 Rotate 가 엉뚱한 궤도를 돈다 (조용한 오답).
    chk("GuessMode" not in _pil_inp(os.path.join(_td, "n.inp"), "x.xyz", 0, 1,
                                    "RKS", 1.0, "r2SCAN-3c"),
        "⛔음성 T P0-3: `.loc` 를 안 읽는 입력에는 GuessMode 를 넣지 않는다 "
        "(의미 없는 키워드를 흩뿌리지 않는다)")
    # 결정론/무작위 국재화 키워드
    _txt_L0 = _pil_inp(os.path.join(_td, "L0.inp"), "x.xyz", 0, 1, "RKS", 1.0,
                       "r2SCAN-3c", loc=True)
    _txt_L1 = _pil_inp(os.path.join(_td, "L1.inp"), "x.xyz", 0, 1, "RKS", 1.0,
                       "r2SCAN-3c", loc="random")
    # ⛔ 회신 U 해제순서 ⑥ — 러너에 **작은 분자 %loc 구문 확인** 단계가 있어야 한다
    chk("loccheck" in PIL_RUNNER and "Random 0" in PIL_RUNNER
        and "MOLECULAR ORBITALS" in PIL_RUNNER,
        "회신 U 해제순서 ⑥: 러너가 H₂O 하나로 `%loc` 구문·suffix·인쇄 블록을 먼저 "
        "확인한다 — 200원자 잡은 %loc 이 무시돼도 정상 종료한다 (그래서 없는 키를 "
        "세 판 동안 못 봤다)")
    # ⛔ 회신 U P0-5 — 러너가 BUILDER 해시를 manifest 와 대조한다
    chk("builder_sha256" in PIL_RUNNER and "sha256sum \"$BUILDER\"" in PIL_RUNNER,
        "회신 U P0-5: 러너가 `$BUILDER` 를 manifest 의 `builder_sha256` 과 대조한다 "
        "— 다른 빌더로 돌리면 사전등록이 봉인한 규칙과 실제 규칙이 갈린다")
    chk("Random 0" in _txt_L0 and "LocMet PipekMezey" in _txt_L0,
        "회신 T P0-3 + U P0-1: primary 국재화가 **결정론**이다 — 키는 `Randomize` 가 "
        "아니라 **`Random 0`** 이다 (ORCA 6.1 공식 inline 키)")
    chk("Random 1" in _txt_L1 and "LocMet PipekMezey" in _txt_L1,
        "회신 U P0-1: R1(민감도)도 **`Random 1` 을 명시**한다 — 기본값에 맡기면 "
        "판본이 바뀔 때 R0 와 같아져 'robust' 가 착시가 된다")
    # ⛔음성 회신 U P0-1 — 틀린 키가 되살아나면 잡는다
    chk("Randomize" not in _txt_L0 and "Randomize" not in _txt_L1,
        "⛔음성 U P0-1: `Randomize` 는 ORCA `%loc` 의 키가 **아니다** — 되살아나면 "
        "결정론이 걸렸다는 보증이 통째로 사라진다")
    # ⛔음성 회신 U P0-1 — occupied valence 한정을 **명시**해야 한다
    for _nm, _t in (("R0", _txt_L0), ("R1", _txt_L1)):
        chk("OCC true" in _t and "VIRT false" in _t and "T_CORE" in _t,
            "회신 U P0-1(%s): `OCC`·`VIRT`·`T_CORE` 를 생략하면 'occupied valence 만 "
            "국재화' 를 보증 못 한다 — 코어가 섞이면 seed 로 C 1s 가 뽑힌다" % _nm)
    # ⛔음성 2026-08-31 실측 — 연산자가 **베타(1,1)** 여야 한다. 알파(0,0)는 no-op:
    #   D•(961전자 doublet)는 알파 0..480 이 **전부 점유**라 알파끼리 돌려도
    #   밀도가 안 변한다. 그러면 seed 전부가 같은 기본 해로 수렴하고
    #   "방법이 backbone 상태를 못 찾는다" 로 오판하게 된다.
    chk("90, 0, 0}" not in _txt_r,
        "⛔음성 실측: Rotate 연산자가 **알파(0,0)가 아니다** — 알파는 전부 점유라 "
        "no-op 이고 seed 가 통째로 무의미해진다")
    chk(_txt_r.count("end") >= 2 and "\n" in _txt_r.split("%scf")[1][:40],
        "⛔음성: `%scf` 를 여러 줄로 쓴다 (Rotate 의 end 와 %scf 의 end 가 "
        "한 줄에 붙으면 모호하다)")
    # ══ 폴라론 pilot e2e — **실제로 생성기와 seed 생성기를 돌린다** ═══════
    #  ⛔ 왜 필요한가 (2026-08-31): 위의 순수-헬퍼 시험 40건은 전부 통과하는데
    #     `--polaron_pilot` 은 UnboundLocalError, `--polaron_seeds` 는 4-튜플
    #     언팩 ValueError 로 **둘 다 첫 줄에서 죽어 있었다.** 함수를 부르지 않는
    #     시험은 그 함수가 죽었는지 모른다 (CLAUDE.md: 양성만 있는 selftest 금지).
    print("── 폴라론 pilot e2e ──")
    with tempfile.TemporaryDirectory() as ptd:
        _dsym, _dpos = _synthetic_dimer()
        _dx = os.path.join(ptd, "dimer.xyz")
        write_xyz(_dx, _dsym, _dpos, "synthetic dimer for polaron e2e")

        def _gen(sub, **kw):
            a = argparse.Namespace(neutral_xyz=_dx, out=os.path.join(ptd, sub),
                                   eps=[1.0], nprocs=4, functional="r2SCAN-3c",
                                   eps_why="selftest", site=None,
                                   loc_realization="deterministic")
            for k, v in kw.items():
                setattr(a, k, v)
            return pilot_generate(a)

        _po = _gen("base")
        _pm = json.loads((_po / "MANIFEST_PILOT.json").read_text())
        chk(sum(1 for v in _pm["jobs"].values() if v["phase"] == "L") == 2
            and sum(1 for v in _pm["jobs"].values() if v["phase"] == "L2") == 2,
            "e2e: `--polaron_pilot` 가 **실제로 돈다** (phase L 2 + L2 2) — "
            "종전 UnboundLocalError 회귀시험")
        chk("%maxcore 6000" in open(os.path.join(
                str(_po), "L", "eps1", "L_dminus", "L_dminus.inp")).read(),
            "e2e: `%maxcore` 기본값 6000 MB/proc")
        _pl = _gen("mem", maxcore=1500, nprocs=4)
        _pmm = json.loads((_pl / "MANIFEST_PILOT.json").read_text())
        chk("%maxcore 1500" in open(os.path.join(
                str(_pl), "L", "eps1", "L_dminus", "L_dminus.inp")).read()
            and _pmm["memory_request_GB_total"] == round(4 * 1500 / 1024.0, 1),
            "e2e: `--maxcore` 가 입력에 실제로 반영되고 총 요청(%.1f GB)이 "
            "manifest 에 남는다 — proc 당 MB 라 nprocs 를 곱해야 총량이다"
            % _pmm["memory_request_GB_total"])
        chk(_pm["atom_manifest"]["P"]["n_atoms"]
            == _pm["atom_manifest"]["D"]["n_atoms"] + 1,
            "e2e: 생성물의 P/D 프레임이 원자 하나 차이다 (%d/%d)"
            % (_pm["atom_manifest"]["P"]["n_atoms"],
               _pm["atom_manifest"]["D"]["n_atoms"]))

        # ⛔ 회신 V P0-2 — 사전등록 **내용** 결박 검사를 시험이 지나게 한다.
        #   합성 다이머는 실물 부모(b490…)와 다르므로, 픽스처가 자기 조건을 적은
        #   사전등록을 쓰고 `PIL_PREREG_S0` 를 거기로 돌린다 (production 우회 아님 —
        #   `_repo_path` 가 절대경로를 그대로 받는 것뿐이다).
        global PIL_PREREG_S0
        _prereg_real = PIL_PREREG_S0

        def _fixture_prereg(mm, **patch):
            f = os.path.join(ptd, "prereg_fixture_%d.json" % (len(patch) + hash(str(patch)) % 97))
            doc = {"schema": "prereg/v1", "status": "ratified",
                   "0_시각_증거": {"builder_sha256": mm.get("builder_sha256"),
                                    "builder_commit": mm.get("builder_commit")},
                   "대상": {"parent_sha256": mm.get("parent_sha256"),
                            "atom_manifest_hash": mm.get("atom_manifest_hash"),
                            "functional": mm.get("functional"),
                            "loc_realization": mm.get("loc_realization"),
                            "epsilon": sorted(float(v["epsilon"])
                                              for v in mm["environments"].values())}}
            for k, v in patch.items():
                if k.startswith("_"):
                    continue
                if k in ("builder_sha256", "builder_commit"):
                    doc["0_시각_증거"][k] = v
                elif k == "status":
                    doc["status"] = v
                else:
                    doc["대상"][k] = v
            # ⛔ 회신 V Q5-1 — 비준 기록과 **내용 지문**을 넣는다 (실물과 같은 모양).
            if not patch.get("_no_ratification"):
                _cc = {k: v for k, v in doc.items() if k != "ratification"}
                doc["ratification"] = {
                    "state": "ratified", "role": "scientific_owner",
                    "actor_id": "selftest", "timestamp": "2026-09-02T00:00:00Z",
                    "commit": "0" * 40,
                    "content_digest": hashlib.sha256(
                        json.dumps(_cc, sort_keys=True, ensure_ascii=False)
                        .encode("utf-8")).hexdigest()}
                if patch.get("_break_digest"):
                    doc["ratification"]["content_digest"] = "9" * 64
            doc.pop("_no_ratification", None); doc.pop("_break_digest", None)
            open(f, "w").write(json.dumps(doc, ensure_ascii=False))
            return f

        def _run(sub, _prereg_patch=None, **kw):
            """base 를 복사해 phase L 산출물을 만들고 pilot_seeds 를 돌린다."""
            global PIL_PREREG_S0        # ⚠ 중첩 함수는 자기 선언이 필요하다
            d = os.path.join(ptd, sub)
            _copy2.copytree(str(_po), d)
            mm = json.loads(open(os.path.join(d, "MANIFEST_PILOT.json")).read())
            _post = kw.pop("_post", None)
            _pil_fake_phaseL(d, mm, **kw)
            if _post:
                _post(Path(d))
            # 픽스처 사전등록으로 결박을 갱신한다.
            # ⚠ `_post` 가 manifest 를 고쳤을 수 있으므로 **다시 읽어서** 덧쓴다
            #   (통째로 덮으면 neg_oldman 같은 음성 픽스처가 되살아난다).
            _mp = os.path.join(d, "MANIFEST_PILOT.json")
            mm2 = json.loads(open(_mp).read())
            _pf = _fixture_prereg(mm, **(_prereg_patch or {}))
            PIL_PREREG_S0 = _pf
            mm2["prereg"] = _pf
            mm2["prereg_sha256"] = _sha(_pf)
            open(_mp, "w").write(json.dumps(mm2, ensure_ascii=False))
            return pilot_seeds(d)

        _n = _run("ok")
        _mk = json.loads(open(os.path.join(ptd, "ok", "MANIFEST_PILOT.json")).read())
        _S = {k: v for k, v in _mk["jobs"].items() if v["phase"] == "S"}
        chk(_n == 7 and len(_S) == 7,
            "e2e: `--polaron_seeds` 가 **실제로 돈다** — D• 4 + P⁺ 3 = 7 잡 "
            "(종전 4-튜플 언팩 ValueError 회귀시험)")
        # ⛔ 회신 V P0-3 양성 — ORCA 6.1 문서 표기 `.loc.gbw` 로도 돌아야 한다.
        #   우리 코드는 `.loc` 만 기대해 왔다. 어느 쪽인지는 loccheck 가 정한다.
        _ngbw = _run("gbw", loc_suffix=".loc.gbw")
        _mgbw = json.loads(open(os.path.join(ptd, "gbw", "MANIFEST_PILOT.json")).read())
        chk(_ngbw == 7 and any('.loc.gbw' in open(os.path.join(
                ptd, "gbw", k, k.rsplit("/", 1)[-1] + ".inp")).read()
                for k, v in _mgbw["jobs"].items()
                if v["phase"] == "S" and v.get("orbitals_from")),
            "회신 V P0-3 양성: 국재 파일이 **`.loc.gbw`** 여도 seed 가 만들어지고 "
            "입력이 그 파일을 읽는다 (ORCA 6.1 문서 표기)")
        _pi = [v for k, v in _S.items() if v["seed"].startswith("B_ring")]
        chk(len(_pi) == 4 and all(v["seed_mo_character"]["pi_share"] >= PIL_PI_MIN
                                  and v["seed_mo_character"]["p_frac"] >= PIL_PFRAC_MIN
                                  for v in _pi),
            "e2e: 링 seed 4개가 **고리법선 π** 로 판정됐다 (π %.2f · p %.2f)"
            % (_pi[0]["seed_mo_character"]["pi_share"],
               _pi[0]["seed_mo_character"]["p_frac"]))
        _sul = [v for v in _S.values() if v["seed"] == "A_sulfonate"]
        chk(len(_sul) == 1 and _sul[0]["seed_mo_character"]["O_frac"] >= PIL_ONB_MIN,
            "e2e: sulfonate seed 가 **O-nonbonding** 으로 판정됐다 (O %.2f)"
            % _sul[0]["seed_mo_character"]["O_frac"])
        chk(all(v["seed_mo"] != 0 and v["seed_mo"] != 40
                for v in _S.values() if v["seed_mo"] is not None),
            "⛔음성 e2e: **코어 MO(−20 Eh)도 가상 MO(점유 0)도 seed 로 안 뽑힌다** "
            "— 둘 다 목표 링에 100/99% 걸어 뒀는데 걸러졌다")
        _df = [v for v in _S.values() if v["seed"] == "default"]
        chk(len(_df) == 2 and all(v["orbitals_from"] is None
                                  and v["loc_sha256"] is None
                                  and v["seed_equivalence_class"] == "fresh_guess"
                                  for v in _df),
            "e2e: `default` 는 `.loc` 를 읽지 않으므로 출처를 안 찍는다 (회신 T P0-4)")
        _inp = open(os.path.join(ptd, "ok", "S", "eps1", "Dradical", "B_ring0",
                                 "B_ring0.inp")).read()
        chk("GuessMode CMatrix" in _inp and "%moinp" in _inp.lower()
            and "Rotate" in _inp,
            "e2e: 생성된 seed 입력에 MORead·CMatrix·Rotate 가 실제로 들어갔다")

        for _sub, _kw, _why in (
            ("neg_rand", {"rand_mark": True},
             "국재화가 **무작위 seed** 로 돌았는데 R0 로 선언돼 있다"),
            ("neg_gm", {"kill_guessmode": True},
             "L2 입력에 `GuessMode CMatrix` 가 없다 (MO 재정렬 → 엉뚱한 Rotate)"),
            ("neg_nomopop", {"no_mopop": True},
             "MO 별 Löwdin 인구 블록이 없다"),
            ("neg_sigma", {"sigma_ring": True},
             "링에 96% 걸렸지만 **면내 p(σ)** 다 — 공간 국재는 π 가 아니다"),
            ("neg_term", {"bad_term": True},
             "phase L2 가 정상 종료하지 않았다"),
            ("neg_noout", {"_post": lambda d: os.remove(
                d / "L2" / "eps1" / "L_dminus" / "L_dminus.out")},
             "phase L2 출력이 아예 없다"),
            ("neg_noloc", {"_post": lambda d: os.remove(
                d / "L" / "eps1" / "L_dminus" / "L_dminus.loc")},
             "국재 궤도 `.loc` 가 없다"),
            ("neg_frame", {"_post": lambda d: _copy2.copy(
                d / "L" / "eps1" / "L_neutral" / "L_neutral.xyz",
                d / "L" / "eps1" / "L_dminus" / "L_dminus.xyz")},
             "D 잡에 P 프레임(원자 하나 많음) xyz 가 들어갔다 — 프레임 어긋남"),
            ("neg_oldman", {"_post": lambda d: (d / "MANIFEST_PILOT.json").write_text(
                json.dumps({k: v for k, v in json.loads(
                    (d / "MANIFEST_PILOT.json").read_text()).items()
                    if k != "atom_manifest"}, ensure_ascii=False))},
             "구판 manifest — P/D 프레임 봉인이 없다"),
            # ── 회신 U 신설 음성 ────────────────────────────────────────────
            ("neg_nomos", {"no_mos": True},
             "U P0-2: MO **계수** 블록이 없다 — 대각 인구만으로는 π 를 회전불변하게 "
             "판정할 수 없으므로 seed 를 만들지 않는다"),
            ("neg_noorbener", {"no_orbener": True},
             "U P0-4: phase L 의 canonical `ORBITAL ENERGIES` 가 없다 — 코어 창을 "
             "만들 수 없으면 국재 MO 에너지로 대신하지 않고 멈춘다"),
            ("neg_notcore", {"kill_tcore": True},
             "U P0-1·P0-4: phase L 입력의 `%loc T_CORE` 가 없다 — 원자가 한정 "
             "국재화가 보증되지 않는다"),
            ("neg_nolout", {"_post": lambda d: os.remove(
                d / "L" / "eps1" / "L_dminus" / "L_dminus.out")},
             "U P0-4: phase L(국재화 **전**) 출력이 없다 — canonical 창의 출처다"),
            # ── 회신 V P0-3 신설 음성 ────────────────────────────────────────
            ("neg_nocert", {"no_loccheck": True},
             "V P0-3: **loccheck 증서가 없다** — 순서가 문구가 아니라 게이트여야 한다"),
            ("neg_certmopop", {"loccheck_bad": "mopop"},
             "V P0-3: loccheck 에서 **MO 인구 파서가 실물을 못 읽었다** — 200원자를 "
             "열 이유가 없다"),
            ("neg_certmos", {"loccheck_bad": "mos"},
             "V P0-3: loccheck 에서 **MO 계수 파서가 실물을 못 읽었다**"),
            ("neg_certold", {"loccheck_bad": "orca_version"},
             "V P0-3: 증서에 ORCA 버전이 없다 (구판이거나 손으로 만든 것)"),
            ("neg_certsuf", {"loccheck_bad": "loc_suffix"},
             "V P0-3: 증서에 loc_suffix 가 없다 — 어느 파일을 읽을지 모른 채 진행 금지"),
            # ── 회신 V P0-2 — 사전등록 **내용** 결박. 파일 해시만으로는 부족하다 ──
            ("neg_pre_parent", {"_prereg_patch": {"parent_sha256": "d" * 64}},
             "V P0-2: 사전등록의 **부모 구조 SHA** 가 생성물과 다르다 — 리뷰어 반례"
             "(미이완 `dp6_gs0_neutral_start.xyz` 가 통과하던 경로)"),
            ("neg_pre_builder", {"_prereg_patch": {"builder_sha256": "e" * 64}},
             "V P0-2: 사전등록이 봉인한 **빌더**가 실제와 다르다 — 봉인한 규칙과 "
             "적용된 규칙이 갈린다"),
            ("neg_pre_commit", {"_prereg_patch": {"builder_commit": "f" * 40}},
             "V P0-2: 사전등록의 빌더 **commit** 이 다르다"),
            ("neg_pre_amf", {"_prereg_patch": {"atom_manifest_hash": "a" * 64}},
             "V P0-2: 사전등록의 **atom_manifest 해시**가 다르다 (P/D 프레임이 다르다)"),
            ("neg_pre_func", {"_prereg_patch": {"functional": "PBE0"}},
             "V P0-2: 사전등록의 **범함수**가 다르다"),
            ("neg_pre_eps", {"_prereg_patch": {"epsilon": [4.0]}},
             "V P0-2: 사전등록의 **환경 ε** 가 다르다"),
            ("neg_pre_real", {"_prereg_patch": {"loc_realization": "R1_random"}},
             "V P0-2: 사전등록의 **국재화 realization** 이 다르다"),
            ("neg_pre_status", {"_prereg_patch": {"status": "retracted"}},
             "V P0-2: 사전등록이 **철회 상태**다 — 그 문서로 결과를 붙이지 않는다"),
            # ── 회신 V Q5-1 (2026-09-02 비준 후) — 비준이 phase L 의 선행 조건이다 ──
            ("neg_pre_proposed", {"_prereg_patch": {"status": "proposed"}},
             "V Q5-1: 사전등록이 **`proposed`** 다 — 비준 전에는 seed 를 만들지 않는다 "
             "(비용 발생 전에 닫는다)"),
            ("neg_pre_norat", {"_prereg_patch": {"_no_ratification": True}},
             "V Q5-1: 사전등록에 **사람 비준 기록이 없다** (status 문자열만으로는 "
             "비준이 아니다)"),
            ("neg_pre_digest", {"_prereg_patch": {"_break_digest": True}},
             "V Q5-1: 사전등록이 **비준 이후에 바뀌었다** (내용 지문 불일치) — "
             "재승인이 필요하다"),
        ):
            raises(lambda _s=_sub, _k=_kw: _run(_s, **_k), "⛔음성 e2e: " + _why)
        # ══ 회신 T Q4 — 4층 판정 e2e (분석기도 한 번도 안 돌려 봤다) ══════
        import contextlib, io as _io

        def _ana(sub, **kw):
            global PIL_PREREG_S0
            d = os.path.join(ptd, sub)
            if not os.path.isdir(d):
                _copy2.copytree(str(_po), d)
                mm = json.loads(open(os.path.join(d, "MANIFEST_PILOT.json")).read())
                _pil_fake_phaseL(d, mm)
                _pf = _fixture_prereg(mm)
                PIL_PREREG_S0 = _pf
                mm["prereg"] = _pf; mm["prereg_sha256"] = _sha(_pf)
                open(os.path.join(d, "MANIFEST_PILOT.json"), "w").write(
                    json.dumps(mm, ensure_ascii=False))
                with contextlib.redirect_stdout(_io.StringIO()):   # 픽스처 소음 제거
                    pilot_seeds(d)
            else:
                _mm = json.loads(open(os.path.join(d, "MANIFEST_PILOT.json")).read())
                PIL_PREREG_S0 = _mm.get("prereg")
            mm = json.loads(open(os.path.join(d, "MANIFEST_PILOT.json")).read())
            _pil_fake_phaseS(d, mm, **kw)
            return pilot_analyze(d)

        _r = _ana("q4_ok")
        _dj = {k: v for k, v in _r["jobs"].items() if "/Dradical/" in k}
        chk(len(_r["jobs"]) == 7 and not _r["blocks"],
            "Q4 e2e: `--polaron_analyze` 가 **실제로 돈다** — S 잡 7건 게이트 0")
        chk(all(v["intervention"]["status"] == "INTERVENED"
                for k, v in _dj.items() if v["seed"] != "default"),
            "Q4 1층: 회전 직후 초기밀도의 스핀이 목표 집합에 있다 (probe 몫 %.2f ≥ %.2f)"
            % (_dj["S/eps1/Dradical/B_ring0"]["intervention"]["share"], PIL_PROBE_MIN))
        chk(_dj["S/eps1/Dradical/default"]["intervention"]["status"]
            == "NO_INTERVENTION",
            "Q4 1층: `default` 는 개입이 없으므로 probe 를 요구하지 않는다")
        _th = _dj["S/eps1/Dradical/B_ring0"]["target_hit"]
        chk(_th["applicable"] and _th["resolved"] and _th["hit"] is True
            and _th["margin"] >= PIL_HIT_MARGIN,
            "Q4 2층: 링 분포에 유일 최대가 margin %.2f 로 서 있고 심은 자리와 같다"
            % _th["margin"])
        chk(_dj["S/eps1/Dradical/A_sulfonate"]["target_hit"]["applicable"] is False,
            "Q4 2층: SO₃ 중심 해에는 **링 분해를 요구하지 않는다** "
            "(backbone 에 스핀이 없으면 성립 안 하는 질문이다)")
        chk(all(v["stability"]["status"] == "STABLE" for v in _dj.values()),
            "Q4 3층: 최종 파동함수 안정성이 **수행 흔적과 함께** 확인됐다")
        _b = _r["seed_vs_basin"]["eps1/Dradical"]
        chk(_b["n_seeds"] == 4 and _b["n_distinct_basins"] == 4,
            "Q4 4층: 서로 다른 해 4개가 basin 4개로 갈렸다 (seed %d → basin %d)"
            % (_b["n_seeds"], _b["n_distinct_basins"]))

        _r2 = _ana("q4_deg", degenerate=True)
        _b2 = _r2["seed_vs_basin"]["eps1/Dradical"]
        chk(_b2["n_seeds"] == 4 and _b2["n_distinct_basins"] < 4,
            "⛔음성 Q4 4층: **같은 에너지·같은 스핀벡터**로 수렴한 seed 들을 "
            "하나의 basin 으로 센다 (seed %d → basin %d) — seed 개수는 반복수가 아니다"
            % (_b2["n_seeds"], _b2["n_distinct_basins"]))
        chk(_r2["by_env"]["eps1"]["n_states"] == _b2["n_distinct_basins"]
            if _r2.get("by_env") else True,
            "Q4 4층: `n_states` 가 잡 개수가 아니라 **구분되는 basin 수**다")

        _r3 = _ana("q4_probe", probe_wrong=("B_ring0",))
        chk(any(g.startswith("SEED_INTERVENTION_FAILED")
                for g in _r3["jobs"]["S/eps1/Dradical/B_ring0"]["gates"]),
            "⛔음성 Q4 1층: 회전이 **다른 집합**에 스핀을 놓았다 — 이 seed 는 "
            "다른 출발점이 아니다")
        _r4 = _ana("q4_noprobe", drop_probe=("B_ring0",))
        chk(any(g.startswith("SEED_INTERVENTION_UNVERIFIED")
                for g in _r4["jobs"]["S/eps1/Dradical/B_ring0"]["gates"]),
            "⛔음성 Q4 1층: probe 가 안 돌았으면 **확인 못 한 것**이지 통과가 아니다")
        _r5 = _ana("q4_flat", flat_ring=("B_ring0",))
        chk(any(g.startswith("TARGET_UNRESOLVED")
                for g in _r5["jobs"]["S/eps1/Dradical/B_ring0"]["gates"]),
            "⛔음성 Q4 2층: 두 링에 반씩 걸린 해는 **어느 링인지 분해되지 않는다**")
        _r6 = _ana("q4_unstable", unstable=("B_ring0",))
        chk(_r6["jobs"]["S/eps1/Dradical/B_ring0"]["stability"]["status"]
            == "UNSTABLE_NOT_REJUDGED",
            "⛔음성 Q4 3층: 불안정한데 **재계산·재판정한 잡이 없다** — "
            "이 에너지는 basin 대표가 아니다")
        _r7 = _ana("q4_nostab", no_stab=("B_ring0",))
        chk(_r7["jobs"]["S/eps1/Dradical/B_ring0"]["stability"]["status"] == "NOT_RUN",
            "⛔음성 Q4 3층: StabPerform 을 요청했는데 수행 흔적이 없으면 NOT_RUN "
            "(문자열 하나로 안정을 인정하지 않는다)")
        # 3층 구제 경로 — 게이트가 **막다른 길이 아니어야** 한다
        # ⛔음성 먼저: `.gbw` 없이 재계산 입력을 만들려 하면 거부해야 한다
        _ana("q4_unst2", unstable=("B_ring0",))
        raises(lambda: pilot_restart(os.path.join(ptd, "q4_unst2")),
               "⛔음성 Q4 3층: `.gbw` 가 없으면 재계산 입력을 **만들지 않는다** "
               "(그냥 다시 돌리면 같은 해로 간다)")
        _du = os.path.join(ptd, "q4_unstable")
        for _g in ("Dradical", "Pcation"):
            open(os.path.join(_du, "S", "eps1", _g, "B_ring0",
                              "B_ring0.gbw"), "w").write("followed orbitals")
        with contextlib.redirect_stdout(_io.StringIO()):
            _nr = pilot_restart(_du)
        _mu = json.loads(open(os.path.join(_du, "MANIFEST_PILOT.json")).read())
        _rk = "SR/eps1/Dradical/B_ring0"
        chk(_nr == 2 and _mu["jobs"][_rk]["restart_of"] == "S/eps1/Dradical/B_ring0"
            and "StabPerform" in open(os.path.join(
                _du, "SR", "eps1", "Dradical", "B_ring0", "B_ring0.inp")).read(),
            "Q4 3층 구제: `--polaron_restart` 가 따라 내려간 `.gbw` 로 재판정 입력을 "
            "만든다 (게이트가 막다른 길이 아니다)")
        for _g, _nat in (("Dradical", 25), ("Pcation", 26)):
            _k = "SR/eps1/%s/B_ring0" % _g
            open(os.path.join(_du, _k, "B_ring0.out"), "w").write(_pil_fake_sout(
                _mu["jobs"][_k]["charge"], 2, _mu["jobs"][_k]["n_electrons"],
                [0.0] * _nat, -100.5))
        _r8 = pilot_analyze(_du)
        _j8 = _r8["jobs"]["S/eps1/Dradical/B_ring0"]
        chk(_j8["stability"]["status"] == "UNSTABLE_REJUDGED_STABLE",
            "Q4 3층 구제: 재계산이 안정하면 3층이 풀린다 (그 잡이 basin 대표)")
        # ⛔⛔ 회신 U P0-7 — 재판정했으면 **에너지·스핀도 그 출력에서** 읽어야 한다
        chk(abs(_j8["E_Eh"] - (-100.5)) < 1e-9
            and _j8.get("judged_from") == "SR/eps1/Dradical/B_ring0",
            "회신 U P0-7: 재판정이 안정하면 에너지·스핀·class 를 **재계산 출력**에서 "
            "읽는다 (E=%s). 종전엔 안정성만 재계산에서 보고 나머지는 원래 불안정 "
            "출력(−100.01)에서 읽었다" % _j8["E_Eh"])
        chk(all(v.get("judged_from") == k for k, v in _r["jobs"].items()),
            "회신 U P0-7: 재판정이 없으면 `judged_from` 이 자기 자신이다 "
            "(판정 출처를 언제나 산출물에 남긴다)")
        # ⛔⛔ 회신 V P0-5 실측 재현 — restart 출력에서 **정상종료 한 줄만 지워도**
        #   종전엔 UNSTABLE_REJUDGED_STABLE · gates=[] · ADEQUATE 가 나왔다.
        for _g5 in ("Dradical", "Pcation"):
            _k5 = os.path.join(_du, "SR", "eps1", _g5, "B_ring0", "B_ring0.out")
            _t5 = open(_k5).read().replace("ORCA TERMINATED NORMALLY\n", "")
            open(_k5, "w").write(_t5)
        _r8b = pilot_analyze(_du)
        _j8b = _r8b["jobs"]["S/eps1/Dradical/B_ring0"]
        chk(_j8b["stability"]["status"] == "UNSTABLE_REJUDGED_UNSTABLE"
            and _j8b["gates"] and _r8b["verdict"] != "ADEQUATE"
            and _j8b.get("judged_from") == "S/eps1/Dradical/B_ring0",
            "⛔음성 V P0-5: 재계산 출력이 **정상종료하지 않으면** 대표로 승격하지 "
            "않는다 (상태 %s · 게이트 %d · 전체 %s) — 잘린 출력의 마지막 SCF 는 "
            "수렴한 해가 아니다"
            % (_j8b["stability"]["status"], len(_j8b["gates"]), _r8b["verdict"]))
        # 원상복구 — 뒤따르는 시험이 이 폴더를 다시 쓴다
        for _g5 in ("Dradical", "Pcation"):
            _k5 = os.path.join(_du, "SR", "eps1", _g5, "B_ring0", "B_ring0.out")
            open(_k5, "a").write("ORCA TERMINATED NORMALLY\n")

        # ══ 회신 U P0-8 — basin 군집 4중 결함 (단위시험) ═════════════════════
        def _row(E, sv, rp, **kw):
            r = {"E_Eh": E, "spin_vec": sv, "ring_p": rp, "S2": 0.7530, "nel": 100}
            r.update(kw); return r
        _sv = [0.5, 0.3, 0.2]
        _rp0 = {"ring0": 1.0}
        # ⓐ 순서 의존 — 같은 자료를 이름만 바꿔 넣어도 basin 수가 같아야 한다
        _A = {"a": _row(-100.0, _sv, _rp0), "b": _row(-100.0, _sv, _rp0),
              "c": _row(-100.5, [0.2, 0.3, 0.5], {"ring1": 1.0})}
        _B = {"z": _A["c"], "y": _A["b"], "x": _A["a"]}
        chk(pil_basin_cluster(_A)["n_distinct"] == pil_basin_cluster(_B)["n_distinct"] == 2,
            "회신 U P0-8ⓐ: basin 수가 **job 이름 배치와 무관**하다 (%d/%d) — "
            "종전 첫-job anchor greedy 는 1 또는 2 로 갈렸다"
            % (pil_basin_cluster(_A)["n_distinct"], pil_basin_cluster(_B)["n_distinct"]))
        # ⓐ 추이성이 깨지면 세지 않는다
        _T = {"a": _row(-100.0000, _sv, _rp0),
              "b": _row(-100.00008, _sv, _rp0),
              "c": _row(-100.00016, _sv, _rp0)}
        _tc = pil_basin_cluster(_T)
        chk(_tc["verdict"] == "CLUSTER_AMBIGUOUS" and _tc["n_distinct"] is None,
            "⛔음성 U P0-8ⓐ: a~b, b~c 인데 a≁c 면 **군집하지 않는다** "
            "(CLUSTER_AMBIGUOUS) — 문턱을 결과 보고 고치지 않는다")
        # ⓑ 게이트 실패 행은 입력에서 뺀다
        _G = dict(_A); _G["bad"] = _row(-90.0, [1.0, 0, 0], {"ring2": 1.0}, passed=False)
        _gc = pil_basin_cluster(_G)
        chk(_gc["n_distinct"] == 2 and _gc["excluded_gated"] == ["bad"],
            "회신 U P0-8ⓑ: **게이트 실패 행은 군집 입력에서 뺀다** — basin 수는 "
            "통과한 실행이 준 상태 수이지 시도 횟수가 아니다")
        # ⓒ 링 판정이 성립 안 하는 해끼리는 링 축을 빼고 본다
        _Cn = {"p": _row(-100.0, _sv, {"ring0": 0.51, "ring1": 0.49},
                         ring_applicable=False),
               "q": _row(-100.0, _sv, {"ring0": 0.30, "ring1": 0.70},
                         ring_applicable=False)}
        chk(pil_basin_cluster(_Cn)["n_distinct"] == 1,
            "회신 U P0-8ⓒ: 링 판정을 **면제한** 해끼리는 `ring_p` 를 군집축에서 뺀다 "
            "— 면제해 놓고 backbone 내부 정규화 링 몫으로 가르면 잡음이 basin 이 된다")
        chk(pil_basin_cluster({"p": dict(_Cn["p"], ring_applicable=True),
                               "q": dict(_Cn["q"], ring_applicable=True)}
                              )["n_distinct"] == 2,
            "⛔음성 U P0-8ⓒ: 링 판정이 **성립하는** 해끼리는 링 축을 그대로 쓴다 "
            "(면제를 아무 데나 적용하지 않는다)")
        # ⓓ 전역 스핀 반전은 같은 상태다 (collinear doublet 의 반대 M_S)
        _F = {"up": _row(-100.0, _sv, _rp0),
              "dn": _row(-100.0, [-x for x in _sv], _rp0)}
        chk(pil_basin_cluster(_F)["n_distinct"] == 1,
            "회신 U P0-8ⓓ: **전역 α↔β 반전**은 같은 basin 이다 — 종전엔 둘로 세어 "
            "`basin ≥2` 를 거짓 충족할 수 있었다")
        chk(pil_basin_cluster({"a": _row(-100.0, [0.5, 0.3, 0.2], _rp0),
                               "b": _row(-100.0, [0.5, -0.3, 0.2], _rp0)}
                              )["n_distinct"] == 2,
            "⛔음성 U P0-8ⓓ: **일부만** 뒤집힌 것은 정말 다른 해다 — 전역 반전만 "
            "정준화한다")
        # 정규화 — 크기가 다른 같은 분포는 같은 basin
        chk(pil_basin_cluster({"a": _row(-100.0, [0.5, 0.3, 0.2], _rp0),
                               "b": _row(-100.0, [1.0, 0.6, 0.4], _rp0)}
                              )["n_distinct"] == 1,
            "회신 U P0-8ⓒ: 스핀 벡터를 `Σ|s_i|` 로 정규화한다 — 총 스핀 크기 차이가 "
            "공간 분포 차이로 둔갑하지 않는다")
        # e2e — 전역 반전 seed 가 basin 을 늘리지 않는다
        _r11 = _ana("q4_flip", flip_spin=("B_ring0",))
        chk(_r11["seed_vs_basin"]["eps1/Dradical"]["n_distinct_basins"]
            == _r["seed_vs_basin"]["eps1/Dradical"]["n_distinct_basins"],
            "회신 U P0-8ⓓ e2e: seed 하나의 스핀을 전역 반전해도 basin 수가 그대로다 "
            "(%d)" % _r11["seed_vs_basin"]["eps1/Dradical"]["n_distinct_basins"])

        # ══ 회신 U P0-6 — **S0 전용 판정.** `ADEQUATE` 경로가 코드에 없었다 ═══
        chk(_r["verdict"] == "ADEQUATE",
            "회신 U P0-6 양성: 게이트 0 + positive control 회수 + D• basin 2개 이상이면 "
            "**ADEQUATE** 다 (종전엔 이 경로가 코드에 아예 없었다)")
        chk("허용_서술" in _r and "구분해 회수했다" in _r["허용_서술"]
            and all("바닥상태" not in x for x in [_r["허용_서술"]]),
            "회신 U P0-6: 허용 서술이 **'상태를 구분해 회수했다'** 이지 "
            "'바닥상태가 …' 가 아니다 (S0 은 에너지 순서를 판정하지 않는다)")
        chk("lowest" not in json.dumps(_r.get("by_env"), ensure_ascii=False)
            and _r["verdict"] not in ("BACKBONE_SUPPORTED", "SO3_CENTERED_WITHIN_MODEL"),
            "⛔음성 U P0-6: 최저 에너지 잡을 골라 `BACKBONE_SUPPORTED` 를 내던 "
            "**폐기된 전체-pilot 결론 경로가 사라졌다**")
        # ⛔음성 U P0-6 — D• basin 이 **하나뿐**이면 막는다 (사전등록 합격 조건 ②)
        _r9 = _ana("q4_one_basin", degenerate="all")
        chk(_r9["verdict"] == "MODEL_NONDIAGNOSTIC"
            and _r9["by_env"]["eps1"]["n_states"] == 1,
            "⛔음성 U P0-6: 게이트를 통과한 D• 실행이 basin 을 **하나만** 주면 "
            "ADEQUATE 가 아니다 — 종전엔 안 막았다 (실제 %s)" % _r9["verdict"])
        # ⛔음성 U P0-9 — positive control **결측**은 방법 실패가 아니다
        _r10 = _ana("q4_nopc", drop_pcation=True)
        chk(_r10["verdict"] == "NO_VALUE" and any(
                b.startswith(("SEED_RECEIPT_MISSING", "GATED_JOBS"))
                for b in _r10["blocks"]),
            "⛔음성 U P0-9: Pcation 출력을 전부 지우면 **NO_VALUE** 다 — 종전엔 "
            "결측이 `blocks` 보다 먼저 평가돼 `MODEL_NONDIAGNOSTIC`(방법이 틀렸다)이 "
            "나왔다 (실제 %s)" % _r10["verdict"])
        # 계획된 positive control 이 **일부만** 판정돼도 방법 실패가 아니다
        chk(_ana("q4_pc_partial", unstable=("B_ring0",))["verdict"] != "MODEL_NONDIAGNOSTIC",
            "⛔음성 U P0-9: positive control 이 게이트에 걸린 것도 **실행 문제**이지 "
            "방법 실패가 아니다")
        chk(all(v["verdict"] in (None, "NO_VALUE", "MODEL_NONDIAGNOSTIC",
                                 "ADEQUATE", "SEARCH_PROTOCOL_DEPENDENT",
                                 "PARTITION_DEPENDENT", "THRESHOLD_DEPENDENT",
                                 "BACKBONE_DEFINITION_DEPENDENT", "ETHER_O_CENTERED")
                for v in (_r3, _r4, _r5, _r6, _r7)),
            "Q4: 게이트가 걸린 실행은 값이 아니라 판정어를 낸다 (%s)"
            % [v["verdict"] for v in (_r3, _r4, _r5, _r6, _r7)])
    print("── 폴라론 pilot 끝 ──")
    print("── %s ──" % ("PASS" if not fails else "FAIL " + str(len(fails))))
    return 1 if fails else 0


# ═══════════════════════════════════════════════════════════════════════════
#  폴라론 pilot — H-제거 n=6 라디칼 상태지도 (회신 S, 2026-08-31)
#
#  사전등록: db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json
#  카드:     kb/questions/sdcp_backbone_polaron_estimand_2026_08_31.md
#  결정:     D-2026-08-31-sdcp-polaron-Fbb (proposed)
#
#  ⛔ 이것은 **흡착 doped(Stage 0/B/hybrid)와 다른 캠페인**이다. 슬랩이 없다.
#     회신 R4 가 NO-GO 한 것은 그쪽이고, 여기서는 그 receipt 사슬을 쓰지 않는다.
#
#  2단계인 이유 — seed 를 **실제로 국재화**시켜야 한다 (회신 S Q2):
#    phase L : D⁻ (charge −1, mult 1) SP + Pipek-Mezey 국재화 + MO 별 Löwdin 인구
#              → 각 목표 집합에 가장 크게 걸린 점유 MO 를 찾는다
#    phase S : 그 GBW 를 MORead 하고 선택한 MO 를 HOMO 자리로 Rotate 한 뒤
#              D•(charge 0, mult 2) 를 **비제약**으로 푼다
#  제약은 seed 생성에만 쓰고 최종 에너지는 완전 비제약이다 (회신 S Q2 규율 1·2).
#
#  이 도구가 **못 하는 것**
#    · 상태를 전수 탐색하지 않는다. 사전등록한 8 seed 에서 **찾은 최저해**만 안다.
#    · StabPerform 은 열거가 아니다 — 수렴한 determinant 의 국소최소 여부만 본다.
#    · 고체·사슬간 hopping·이동도·전도도를 말하지 못한다 (단일 사슬 기체/CPCM).
#    · Opt 를 몇 개 돌아야 하는지 미리 모른다 — 발견된 basin 수가 정한다.
#    · ⚠ **ORCA 구문 미검증**: `%loc` 출력 형식과 `Rotate` 의 정확한 동작을 실제
#      ORCA 로 확인하지 않았다. phase L 파서와 seed 입력은 smoke test 가 필요하다.
# ═══════════════════════════════════════════════════════════════════════════

#: 회신 S Q1 — **분자도 절대값**이다. v1 식(분자 signed)은 백본 내부에서 다시
#:   상쇄돼 절대값 분모를 넣은 목적과 모순이었다.
#:      F_G = Σ_{i∈G} |m_i| / Σ_i |m_i|          (세 집합, 상호배타·완전, 합 = 1)
#:   signed net spin 은 버리지 않고 M_G 로 따로 보존한다.
PIL_CLASS_MIN = 0.50        # 유일 집합이 이 이상이고
PIL_CLASS_MARGIN = 0.10     # 다음 집합과 이만큼 차이날 때만 class 부여
PIL_PARTITION_TOL = 0.10    # 두 분할의 F_bb 차가 이보다 크면 PARTITION_DEPENDENT
PIL_SENS_THR = (0.40, 0.50, 0.60)   # 경계 민감도
PIL_RING_SPAN_FRAC = 0.80   # 최소 연속 ring span 이 포함해야 할 spin 비율
PIL_SHARE_FLOOR = 0.01      # 보고 해상도 (무차원 — 에너지 eV 와 **다른 단위**)


def pilot_atom_sets(csym, cnb, crings, csulf, ether_in_backbone=True):
    """회신 S 계약 — **상호배타·완전**한 세 집합 + ring profile.

    → {"sets": {backbone, sulfonate, other}, "rings": {ringN: [...]}, "hash": ...}

    ⛔ 기존 `atom_sets_of()` 와 **다르다**. 그쪽은 backbone 이 ring 들의 합집합이라
      ring 집합과 겹치고 share 합이 1 을 넘는다 (하위호환 목적). 여기서는 회신 S 의
      `F_bb + F_SO3 + F_other = 1` 을 만족해야 하므로 겹침을 허용하지 않는다.
    """
    n = len(csym)
    # ⛔⛔ 2026-08-31 실측 — `analyze()` 의 `ring` 은 **티오펜 5원환만**(S+4C) 이다.
    #   EDOT 의 3,4-위치 에테르 산소는 고리 탄소에 직결돼 π 에 전자를 밀어넣는 자리이고,
    #   PEDOT 폴라론 밀도의 상당부분이 거기 있다. 그걸 `other` 로 밀면 F_bb 가
    #   **체계적으로 과소평가**된다 (실측: 그 O 12개가 other 로 갔다).
    #   ⇒ 기본은 **고리 C 에 직결된 O 를 backbone 에 포함**한다. sp³ 인 -CH2CH2- 다리는
    #     공액이 아니므로 other 로 둔다.
    #   ⚠ 이것은 **분할 선택**이라 estimand 를 움직인다. 사전등록에 선언하고,
    #     분석기가 ether 포함/제외 두 값을 **둘 다** 보고한다 (억지 선택 금지).
    ring_atoms = set()
    for r in crings:
        ring_atoms |= set(r["ring"])
    ether_O = set()
    if ether_in_backbone:
        for i in ring_atoms:
            if csym[i] != "C":
                continue
            for j in cnb[i]:
                if csym[j] == "O" and j not in ring_atoms:
                    ether_O.add(j)
    core = ring_atoms | ether_O
    ring_H = {h for i in core for h in cnb[i] if csym[h] == "H"}
    backbone = core | ring_H
    sulf = set()
    for su in csulf:
        sulf |= {su["sS"]} | set(su["sO"])
        if su.get("aH") is not None:
            sulf.add(su["aH"])
    # ⚠ 겹치면 조용히 한쪽에 넣지 않는다 — 집합 정의가 틀렸다는 뜻이므로 멈춘다
    if backbone & sulf:
        raise SystemExit("⛔ backbone 과 sulfonate 가 겹친다 %s — 집합 정의 오류"
                         % sorted(backbone & sulf)[:5])
    other = set(range(n)) - backbone - sulf
    sets = {"backbone": sorted(backbone), "sulfonate": sorted(sulf),
            "other": sorted(other)}
    # 완전성·상호배타성 (회신 S Q8 게이트)
    tot = sum(len(v) for v in sets.values())
    if tot != n:
        raise SystemExit("⛔ 원자 집합이 완전하지 않다 (%d ≠ %d)" % (tot, n))
    rings = {}
    for ri, r in enumerate(crings):
        ra = set(r["ring"])
        if ether_in_backbone:
            ra |= {j for i in ra if csym[i] == "C" for j in cnb[i]
                   if csym[j] == "O" and j not in set(r["ring"])}
        rh = {h for i in ra for h in cnb[i] if csym[h] == "H"}
        g = sorted(ra | rh)
        if not set(g) <= backbone:
            raise SystemExit("⛔ ring%d 이 backbone 부분집합이 아니다" % ri)
        rings["ring%d" % ri] = g
    # ring 끼리 겹치면(공유 원자) N_eff 가 왜곡된다 — 조용히 넘기지 않는다
    seen = {}
    for k, g in rings.items():
        for i in g:
            if i in seen:
                raise SystemExit("⛔ ring 집합이 겹친다: 원자 %d 이 %s 와 %s 에 동시에"
                                 % (i, seen[i], k))
            seen[i] = k
    h = hashlib.sha256(json.dumps({"sets": sets, "rings": rings},
                                  sort_keys=True).encode()).hexdigest()
    return {"sets": sets, "rings": rings, "hash": h, "n_atoms": n,
            "ether_in_backbone": bool(ether_in_backbone),
            "⚠_분할선택": ("고리 C 에 직결된 에테르 O 를 backbone 에 넣었는지 여부다. "
                            "이것이 F_bb 를 움직인다 — 분석기가 두 값을 다 보고한다")}


def pilot_components(csym, cnb, crings, csulf):
    """회신 T Q3 — **네 성분**을 따로 낸다 (상호배타·완전).

    → {"bb_core", "ether_O", "sulfonate", "other"} + rings

    왜 넷인가 (회신 T Q3): ether O 를 backbone 에 넣는 것은 화학적으로 방어
    가능하지만 그것을 "strict backbone" 이라 부르면 안 된다. 네 성분을 보존하면
    strict(=bb_core) 와 extended(=bb_core+ether_O)를 **파생**시킬 수 있고,
    둘이 갈릴 때 `BACKBONE_DEFINITION_DEPENDENT` 를 정직하게 낼 수 있다.

    ⛔ 이 함수가 못 하는 것: 원자가 π 인지 σ 인지 말하지 않는다 — 그것은 결합
      그래프가 아니라 궤도 성격이고 `pil_orbital_character()` 의 몫이다 (T P0-2).
    """
    n = len(csym)
    ring_atoms = set()
    for r in crings:
        ring_atoms |= set(r["ring"])
    ether_O = set()
    for i in ring_atoms:
        if csym[i] != "C":
            continue
        for j in cnb[i]:
            if csym[j] == "O" and j not in ring_atoms:
                ether_O.add(j)
    ring_H = {h for i in ring_atoms for h in cnb[i] if csym[h] == "H"}
    bb_core = ring_atoms | ring_H
    sulf = set()
    for su in csulf:
        sulf |= {su["sS"]} | set(su["sO"])
        if su.get("aH") is not None:
            sulf.add(su["aH"])
    comp = {"bb_core": bb_core, "ether_O": ether_O, "sulfonate": sulf}
    # 상호배타 — 겹치면 조용히 한쪽에 넣지 않는다
    _ks = sorted(comp)
    for _i in range(len(_ks)):
        for _j in range(_i + 1, len(_ks)):
            _ov = comp[_ks[_i]] & comp[_ks[_j]]
            if _ov:
                raise SystemExit("⛔ %s 와 %s 가 겹친다 %s — 성분 정의 오류"
                                 % (_ks[_i], _ks[_j], sorted(_ov)[:5]))
    comp["other"] = set(range(n)) - bb_core - ether_O - sulf
    if sum(len(v) for v in comp.values()) != n:
        raise SystemExit("⛔ 네 성분이 완전하지 않다")
    rings = {}
    for ri, r in enumerate(crings):
        ra = set(r["ring"])
        eo = {j for i in ra if csym[i] == "C" for j in cnb[i]
              if csym[j] == "O" and j not in ra}
        rh = {h for i in ra for h in cnb[i] if csym[h] == "H"}
        rings["ring%d" % ri] = {"core": sorted(ra | rh), "ether_O": sorted(eo)}
    return {k: sorted(v) for k, v in comp.items()}, rings


def pilot_atom_manifest(csym, cnb, crings, csulf, kill):
    """⛔⛔ 회신 T P0-1 (2026-08-31) — **P(200)/D(199) 를 각각 봉인한다.**

    종전엔 중성 200원자 집합 하나와 해시 하나만 실었다. D⁻/D• 는 H 하나가 빠져
    199원자이고 그 뒤 인덱스가 한 칸씩 밀린다. 코드는 `pil_pick_seed_mo` 와
    `remap_sets` 에서 remap 을 **하고 있었지만**, 산출물에는 그 사실이 없었다 —
    "확인 못 한 것은 통과가 아니다" 와 같은 층위의 결함이다.

    → {"P": {...}, "D": {...}, "remap": {...}, "derived": {...}, "hash": ...}

    ⛔ 이 함수가 못 하는 것: 어느 분할이 옳은지 정하지 않는다. strict/extended
      둘 다 봉인하고, 분석기가 둘 다 보고한다.
    """
    comp, rings = pilot_components(csym, cnb, crings, csulf)
    n = len(csym)
    k = sorted(set(kill))

    def rm(i):
        return None if i in k else i - sum(1 for x in k if x < i)

    f = lambda L: sorted(x for x in (rm(i) for i in L) if x is not None)

    def frame(cmp_, rg, nat):
        d = {"n_atoms": nat, "components": cmp_,
             "counts": {g: len(v) for g, v in cmp_.items()},
             "rings": rg,
             "derived": {
                 "backbone_strict": sorted(cmp_["bb_core"]),
                 "backbone_extended": sorted(set(cmp_["bb_core"]) | set(cmp_["ether_O"])),
             }}
        tot = sum(d["counts"].values())
        if tot != nat:
            raise SystemExit("⛔ 프레임 합 %d ≠ 원자수 %d" % (tot, nat))
        d["hash"] = hashlib.sha256(
            json.dumps({"components": cmp_, "rings": rg, "n": nat},
                       sort_keys=True).encode()).hexdigest()
        return d

    P = frame(comp, rings, n)
    Dc = {g: f(v) for g, v in comp.items()}
    Dr = {g: {"core": f(v["core"]), "ether_O": f(v["ether_O"])}
          for g, v in rings.items()}
    D = frame(Dc, Dr, n - len(k))
    remap = {
        "removed_0based": k, "removed_1based": [i + 1 for i in k],
        "rule": " · ".join(["i < %d → i" % k[0], "%d → absent" % k[0],
                            "i > %d → i − 1" % k[0]]) if len(k) == 1 else
                "kill 집합보다 작은 인덱스는 그대로, 큰 것은 그만큼 당긴다",
        "explicit_P_to_D": {str(i): rm(i) for i in range(n)},
    }
    remap["hash"] = hashlib.sha256(
        json.dumps(remap, sort_keys=True).encode()).hexdigest()
    out = {
        "schema": "polaron_atom_manifest/v2",
        "P": P, "D": D, "remap": remap,
        "derived_정의": {
            "backbone_strict": "bb_core = 티오펜 고리 원자 + 그 고리 H",
            "backbone_extended": "bb_core + ether_O (고리 C 에 직결된 3,4-O)",
            "⚠": ("두 정의가 갈리면 BACKBONE_DEFINITION_DEPENDENT. P⁺(양성대조)가 "
                  "**ether O 포함 때만** backbone 으로 분류되면 대조 자체가 정의 "
                  "의존이므로 D• 의 backbone 판정을 열지 않고 ETHER_O_CENTERED 로 "
                  "따로 보고한다 (회신 T Q3)"),
        },
        "⛔_단일해시_금지": ("P 와 D 는 원자수가 다르다 (%d vs %d). 하나의 atom-set "
                            "해시로 두 계를 가리킬 수 없다 (회신 T P0-1)"
                            % (P["n_atoms"], D["n_atoms"])),
    }
    out["hash"] = hashlib.sha256(
        json.dumps({"P": P["hash"], "D": D["hash"], "remap": remap["hash"]},
                   sort_keys=True).encode()).hexdigest()
    return out


def pilot_shares(mvals, amap):
    """회신 S Q1 식. → {"F": {...}, "M": {...}, "abs_total": ..., "ring_p": {...},
                        "N_eff": ..., "span80": ...}

    ⛔ 못 하는 것: 실공간 적분이 아니라 **원자 population 근사**다 (회신 S 가 허용한
      근사 경로). 같은 정의를 두 분할에 똑같이 적용하는 것이 조건이다.
    """
    tot = sum(abs(x) for x in mvals)
    if tot <= 0:
        return {"F": None, "M": None, "abs_total": tot,
                "why": "총 |스핀| 이 0 — 분모가 없다 (닫힌 껍질류)"}
    F = {g: sum(abs(mvals[i]) for i in idx) / tot for g, idx in amap["sets"].items()}
    M = {g: sum(mvals[i] for i in idx) for g, idx in amap["sets"].items()}
    # ring profile — **backbone 안에서** 정규화 (N_eff 는 링 사이 분포다)
    rw = {k: sum(abs(mvals[i]) for i in idx) for k, idx in amap["rings"].items()}
    rt = sum(rw.values())
    ring_p = {k: (v / rt if rt > 0 else 0.0) for k, v in rw.items()}
    neff = (1.0 / sum(p * p for p in ring_p.values())) if rt > 0 else None
    # 80% spin 을 포함하는 **최소 연속 ring span** (회신 S Q1)
    span = None
    if rt > 0:
        order = sorted(ring_p, key=lambda k: int(k[4:]))
        vals = [ring_p[k] for k in order]
        best = None
        for i in range(len(vals)):
            acc = 0.0
            for j in range(i, len(vals)):
                acc += vals[j]
                if acc >= PIL_RING_SPAN_FRAC:
                    if best is None or (j - i + 1) < best:
                        best = j - i + 1
                    break
        span = best
    return {"F": F, "M": M, "abs_total": tot, "ring_p": ring_p,
            "N_eff": neff, "span80": span}


def pilot_class(F, thr=PIL_CLASS_MIN, margin=PIL_CLASS_MARGIN):
    """회신 S Q1 — 유일 집합이 F ≥ thr **이고** 다음 집합과 차 ≥ margin 일 때만 class.

    → (class, why). `other` 가 크면 backbone−sulfonate 만으로 판정하지 않는다.
    """
    if not F:
        return None, "F 가 없다 (스핀 없음)"
    top = sorted(F.items(), key=lambda kv: -kv[1])
    if F.get("other", 0.0) >= thr:
        return "OTHER_DOMINANT", ("other 집합이 %.3f — 링커/스페이서에 실렸다. "
                                  "backbone−sulfonate 만으로 판정하지 않는다" % F["other"])
    if top[0][1] < thr:
        return "MIXED_UNRESOLVED", "최대 집합 %s %.3f < %.2f" % (top[0][0], top[0][1], thr)
    if len(top) > 1 and (top[0][1] - top[1][1]) < margin:
        return "MIXED_UNRESOLVED", ("%s %.3f 과 %s %.3f 의 차가 %.3f < %.2f"
                                    % (top[0][0], top[0][1], top[1][0], top[1][1],
                                       top[0][1] - top[1][1], margin))
    return top[0][0].upper(), "%s %.3f (2위와 차 %.3f)" % (
        top[0][0], top[0][1], top[0][1] - (top[1][1] if len(top) > 1 else 0.0))


def pilot_threshold_sensitivity(F, thrs=PIL_SENS_THR):
    """0.4/0.5/0.6 경계에서 class 가 바뀌면 THRESHOLD_DEPENDENT (회신 S)."""
    cs = {t: pilot_class(F, thr=t)[0] for t in thrs}
    return {"by_threshold": {str(t): c for t, c in cs.items()},
            "threshold_dependent": len(set(cs.values())) > 1}


def pilot_partition_check(F_low, F_hir, tol=PIL_PARTITION_TOL):
    """Löwdin/Hirshfeld 두 분할 병기 — 억지 선택 금지 (회신 R4 보완 5 · 회신 S Q1)."""
    if not F_low or not F_hir:
        return {"ok": False, "why": "한쪽 분할의 F 가 없다 — 두 분할을 **둘 다** 계산해야 한다"}
    d = {g: abs(F_low.get(g, 0.0) - F_hir.get(g, 0.0)) for g in F_low}
    cl, ch = pilot_class(F_low)[0], pilot_class(F_hir)[0]
    dep = (cl != ch) or (d.get("backbone", 0.0) > tol)
    return {"ok": not dep, "delta": d, "class_lowdin": cl, "class_hirshfeld": ch,
            "partition_dependent": dep,
            "why": ("class 가 다르거나 |ΔF_bb| > %.2f — 억지로 하나를 고르지 않는다" % tol)
                   if dep else "두 분할이 같은 class 와 F_bb 를 준다"}


# ══ 회신 T Q4 — **초기 국재 ≠ 최종 basin**: 4층 판정 ═══════════════════════
#
#  리뷰 지적: seed 를 국재 궤도로 심었다는 사실은 **그 상태가 실현됐다는 증거가
#  아니다.** SCF 는 굴러떨어지고, 여러 seed 가 같은 해로 모일 수 있다.
#  그래서 네 층을 **따로** 확인하고, 층마다 실패어를 다르게 낸다:
#
#    1층 초기 개입   — 회전 뒤 **SCF 전** 밀도의 스핀이 목표 집합에 있나
#                      (`NoIter` probe, 계의 **실제** charge/mult 로)
#    2층 최종 명중   — 수렴 뒤 링 분포에 **유일 최대**가 margin 이상으로 있나
#    3층 최종 안정성 — 불안정하면 **따라 내려간 해로 재계산하고 다시** 판정했나
#    4층 basin 군집  — 서로 다른 seed 가 **같은 해**로 갔으면 상태 1개다
#                      (⛔ seed 개수는 반복수가 아니다)
#
#  ⛔ 이 문턱들은 **결과를 보기 전에** 봉인한다.
# ⛔⛔ 회신 V Q6-1 (2026-09-02) — **ε=1 의 D⁻ 기준계가 부적합한지**를 판정하는
#   기준을 `L_dminus` **결과를 보기 전에** 봉인한다. 회신 U Q6 이 이미 말했다:
#   ε=1 의 D⁻ 가 diffuse/unbound 라 실패하면 그것은 **방법 전체의**
#   `MODEL_NONDIAGNOSTIC` 이 아니라 `S0_EPS1_ANION_REFERENCE_INADEQUATE` 다.
#   그런데 그 문턱을 안 정해 두면 결과를 보고 "이건 unbound 였다" 고 사후에
#   부르게 된다 — 그게 정확히 사전등록이 막으려는 것이다.
#
#   판정 신호 (하나라도 걸리면 그 잡은 ε=1 음이온 기준계 부적합):
#     ⓐ HOMO 에너지가 **양수** (ε=1 에서 여분 전자가 묶이지 않았다)
#     ⓑ SCF 가 수렴하지 않았다 (ORCA 정상종료 + 수렴 문구 부재)
#     ⓒ 여분 전자 밀도가 **분자 밖**으로 샌다 — 가장 큰 Löwdin/Hirshfeld
#        스핀·전하 몫이 어떤 원자에도 PIL_EPS1_MIN_ONMOL 만큼 안 걸린다
#   ⚠ 이 셋은 **필요조건이 아니라 신호**다. 걸리면 그 잡의 결과를 방법 실패로
#     읽지 않고 별도 판정어로 닫는다.
PIL_EPS1_HOMO_MAX_EH = 0.0   # ⓐ HOMO > 0 이면 여분 전자가 안 묶였다
PIL_EPS1_MIN_ONMOL = 0.60    # ⓒ 최대 원자 몫이 이보다 작으면 밀도가 분자 밖이다
PIL_MAXCORE_MB = 6000       # ORCA `%maxcore` — **proc 당** MB (총량 아니다)
PIL_PROBE_MIN = 0.50        # 1층: 회전 직후 초기밀도의 목표집합 |스핀| 몫
PIL_HIT_MARGIN = 0.10       # 2층: 최대 링과 차순위 링의 최소 차 (링 몫 단위)
PIL_BASIN_DE_EH = 1.0e-4    # 4층: 같은 basin 으로 볼 에너지 차 (≈2.7 meV)
PIL_BASIN_SPIN_L1 = 0.30    # 4층: 원자별 **부호 있는** 스핀 벡터의 L1 거리
PIL_BASIN_RING_L1 = 0.10    # 4층: 링 몫 벡터의 L1 거리
PIL_BASIN_S2 = 0.02         # 4층: ⟨S²⟩ 차


def pil_target_hit(ring_p, target, margin=PIL_HIT_MARGIN):
    """2층 — 링 분포에 **유일 최대**가 있나, 그것이 심은 자리인가.

    → {"resolved", "top", "runner_up", "margin", "hit", "why"}

    ⛔ 못 하는 것 / 일부러 안 하는 것
      · **명중(hit)을 요구하지 않는다.** 요구하면 "심은 데로 갔다" 만 남기는
        순환논증이 된다. 우리가 요구하는 것은 **분해 가능(resolved)** 이다.
        옮겨간 것은 결과이지 실패가 아니다 (`MOVED_FROM_SEED` 로 남긴다).
      · 링 몫은 backbone 안에서 정규화된 값이다 — sulfonate 로 간 스핀은
        여기 안 보인다. 그건 `F` 와 class 가 본다.
    """
    if not ring_p:
        return {"resolved": False, "top": None, "runner_up": None, "margin": None,
                "hit": None, "why": "링 몫이 없다 (스핀 없음 또는 판독 실패)"}
    order = sorted(ring_p.items(), key=lambda kv: -kv[1])
    top, tv = order[0]
    rv = order[1][1] if len(order) > 1 else 0.0
    mg = round(tv - rv, 4)
    out = {"resolved": mg >= margin, "top": top, "runner_up":
           (order[1][0] if len(order) > 1 else None), "margin": mg,
           "top_share": round(tv, 4), "hit": None}
    if not out["resolved"]:
        out["why"] = ("최대 링 %s(%.3f)와 차순위 %.3f 의 차 %.3f < %.2f — "
                      "어느 링의 상태인지 **분해되지 않는다**"
                      % (top, tv, rv, mg, margin))
        return out
    if target:
        out["hit"] = (top == target)
        out["why"] = ("심은 자리 %s 에 그대로" % target if out["hit"] else
                      "MOVED_FROM_SEED(%s 에 심었는데 %s 로 갔다 — 실패가 아니라 결과다)"
                      % (target, top))
    else:
        out["why"] = "심은 자리가 없다 (fresh guess) — 명중 여부는 정의되지 않는다"
    return out


def pil_eps1_anion_adequacy(seg, eps, charge, spins=None,
                            homo_max=PIL_EPS1_HOMO_MAX_EH,
                            min_onmol=PIL_EPS1_MIN_ONMOL):
    """ε=1 에서 음이온 기준계(D⁻)가 성립하는가. → (ok, code, why).

    ⛔⛔ 회신 U Q6 · V Q6-1 — 문턱을 **결과 보기 전에** 봉인한 판정이다.
      ε=1 의 D⁻ 가 diffuse/unbound 면 그것은 **방법 실패가 아니라 기준계 부적합**이다.
      `MODEL_NONDIAGNOSTIC` 으로 부르면 방법 전체를 잘못 기각한다.

    → code ∈ OK · S0_EPS1_ANION_REFERENCE_INADEQUATE · S0_EPS1_INCONCLUSIVE

    ⛔ 못 하는 것
      · 진짜 bound 인지 증명하지 않는다 (그건 basis 확장·CBS 몫이다).
      · ε>1 에는 적용하지 않는다 — 용매가 있으면 음이온이 대개 묶인다.
      · 신호를 못 읽으면 **OK 가 아니라 INCONCLUSIVE** 다.
    """
    if eps is None or abs(float(eps) - 1.0) > 1e-9 or int(charge) >= 0:
        return True, "OK", "ε=1 음이온이 아니다 — 이 판정의 대상이 아니다"
    why = []
    # ⓑ 수렴·정상종료
    if "ORCA TERMINATED NORMALLY" not in (seg or ""):
        return False, "S0_EPS1_INCONCLUSIVE", "정상종료하지 않았다 — 신호를 못 읽는다"
    if re.search(r"(?i)SCF NOT CONVERGED|convergence.*not.*achieved", seg or ""):
        why.append("SCF 미수렴")
    # ⓐ HOMO 부호
    m = re.findall(r"(?i)E\(HOMO\)\s*[:=]\s*(-?\d+\.\d+)", seg or "")
    homo = float(m[-1]) if m else None
    if homo is None:
        _o = re.findall(r"^\s*\d+\s+([12]\.\d+)\s+(-?\d+\.\d+)\s+-?\d+\.\d+\s*$",
                        seg or "", re.M)
        homo = float(_o[-1][1]) if _o else None
    if homo is not None and homo > homo_max:
        why.append("HOMO %+.4f Eh > %.1f — 여분 전자가 묶이지 않았다" % (homo, homo_max))
    # ⓒ 밀도가 분자 위에 있나
    if spins:
        t = sum(abs(v) for v in spins) or 0.0
        if t > 0 and (max(abs(v) for v in spins) / t) < 0.0:
            pass
        if t <= 0:
            why.append("스핀 밀도가 0 — 분자 위에 여분 전자가 없다")
        else:
            _frac = sum(abs(v) for v in spins) / t
            if _frac < min_onmol:
                why.append("분자 위 몫 %.2f < %.2f" % (_frac, min_onmol))
    if why:
        return (False, "S0_EPS1_ANION_REFERENCE_INADEQUATE",
                "ε=1 D⁻ 기준계 부적합: " + " · ".join(why)
                + " ⇒ **방법 실패가 아니다** (회신 U Q6 · V Q6-1)")
    if homo is None:
        return False, "S0_EPS1_INCONCLUSIVE", "HOMO 에너지를 못 읽었다 — 확인 못 함"
    return True, "OK", "ε=1 D⁻ 가 묶여 있다 (HOMO %+.4f Eh)" % homo


def pil_basin_key(row):
    """4층 군집의 비교 대상. 하나라도 없으면 **군집하지 않는다** (None 반환)."""
    if row.get("E_Eh") is None or row.get("ring_p") is None:
        return None
    if row.get("spin_vec") is None or row.get("nel") is None:
        return None
    return True


def _pil_spin_norm(v):
    """스핀 벡터를 `Σ|s_i|` 로 정규화. 총 스핀이 0 이면 그대로 (나눌 게 없다).

    ⛔ 왜 (회신 U P0-8ⓒ): 정규화 없이 L1 을 재면 **전체 스핀 크기 차이**가 공간
      분포 차이로 둔갑한다. 우리가 묻는 것은 "어디에 있나" 이지 "얼마나 있나" 가 아니다.
    """
    t = sum(abs(x) for x in v)
    return list(v) if t <= 0 else [x / t for x in v]


def pil_basin_cluster(rows, de=PIL_BASIN_DE_EH, dl1=PIL_BASIN_SPIN_L1,
                      dring=PIL_BASIN_RING_L1, ds2=PIL_BASIN_S2):
    """4층 — 실현된 해를 basin 으로 묶는다. **seed 개수는 반복수가 아니다.**

    rows = {job_key: {"E_Eh", "ring_p", "spin_vec", "S2", "nel",
                      "passed"(선택), "ring_applicable"(선택)}}
    → {"clusters", "n_distinct", "unclustered", "excluded", "borderline",
       "verdict", "why"}

    비교: 전자수 일치 · |ΔE| ≤ de · ⟨S²⟩ 차 ≤ ds2 ·
          **정규화·부호 정준화한** 스핀 벡터 L1 ≤ dl1 ·
          (양쪽 다 링 판정이 성립할 때만) 링 몫 벡터 L1 ≤ dring.

    ⛔⛔ 회신 U P0-8 (2026-09-01) — 네 가지가 겹쳐 **basin 수가 물리와 무관하게** 변했다.
      ⓐ 첫 job 을 anchor 로 삼는 greedy 라 **job 이름 배치에 따라 basin 이 1 또는 2**
         → 완전연결(complete-linkage) + **동치성 검사**로 바꿨다. 관계가 추이적이지
           않으면 (a~b, b~c 인데 a≁c) 군집하지 않고 `CLUSTER_AMBIGUOUS` 로 닫는다.
      ⓑ 게이트 실패·불안정 행을 군집 입력에 넣고 있었다 → `passed=False` 는 **제외**.
      ⓒ backbone 몫 < 0.50 이면 링 판정을 면제하면서 군집엔 backbone 내부 정규화
         `ring_p` 를 계속 썼다 (작은 잡음이 basin 을 가름)
         → `ring_applicable=False` 면 그 쌍에서 **링 축을 뺀다.**
      ⓓ 전역 α↔β 반전을 다른 상태로 셌다 (collinear doublet 에선 같은 상태의 반대 M_S)
         → `d_spin = min(‖s_A−s_B‖₁, ‖s_A+s_B‖₁)`.

    ⛔ 못 하는 것
      · 군집은 **판정이 아니라 계수**다. 두 해가 진짜 다른 물리인지는 말하지 못한다.
      · 임계 근처(경계에 걸친 쌍)는 `borderline` 으로 남긴다 — 조용히 붙이지 않는다.
      · 부분적 스핀 반전(일부 원자만 뒤집힘)은 정준화하지 않는다 — 그건 실제로 다른 해다.
    """
    # ⓑ 게이트를 통과한 행만 군집한다
    gated = sorted(k for k, v in rows.items() if v.get("passed") is False)
    cand = {k: v for k, v in rows.items() if v.get("passed") is not False}
    ok = {k: v for k, v in cand.items() if pil_basin_key(v)}
    bad = sorted(set(cand) - set(ok))
    keys = sorted(ok)
    nrm = {k: _pil_spin_norm(ok[k]["spin_vec"]) for k in keys}
    border = []

    def same(a, b):
        A, B = ok[a], ok[b]
        if A["nel"] != B["nel"]:
            return False, None
        dE = abs(A["E_Eh"] - B["E_Eh"])
        s2 = abs((A.get("S2") or 0.0) - (B.get("S2") or 0.0))
        sa, sb = nrm[a], nrm[b]
        if not sa or len(sa) != len(sb):
            return False, None
        # ⓓ 전역 부호 반전 정준화 — 같은 doublet 의 반대 M_S 는 같은 상태다
        l1 = min(sum(abs(sa[i] - sb[i]) for i in range(len(sa))),
                 sum(abs(sa[i] + sb[i]) for i in range(len(sa))))
        # ⓒ 링 축은 **양쪽 다** 링 판정이 성립할 때만 쓴다
        use_ring = (A.get("ring_applicable", True) and B.get("ring_applicable", True))
        if use_ring:
            rk = sorted(set(A["ring_p"]) | set(B["ring_p"]))
            rl1 = sum(abs(A["ring_p"].get(k, 0.0) - B["ring_p"].get(k, 0.0)) for k in rk)
        else:
            rl1 = 0.0
        hit = (dE <= de and s2 <= ds2 and l1 <= dl1 and rl1 <= dring)
        near = (dE <= de * 3 and s2 <= ds2 * 3 and l1 <= dl1 * 3 and rl1 <= dring * 3)
        return hit, (None if hit or not near else
                     {"pair": [a, b], "dE_Eh": round(dE, 8), "spin_L1": round(l1, 4),
                      "ring_L1": round(rl1, 4), "dS2": round(s2, 4),
                      "ring_axis_used": use_ring})

    # ⓐ 쌍 행렬을 먼저 만든다 (순서 의존 greedy 폐기)
    S = {}
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            hit, nb = same(a, b)
            S[(a, b)] = S[(b, a)] = hit
            if nb:
                border.append(nb)

    def rel(a, b):
        return True if a == b else S.get((a, b), False)

    # ── 연결성분을 먼저 만들고, **각 성분이 clique 인지** 본다 ────────────────
    #  ⛔⛔ 회신 V P0-4 (2026-09-02) — 종전 추이성 검사는 **불완전**했다.
    #    정렬된 keys 를 (i<j<k) 로만 훑으면서 `rel(a,b)` 가 거짓이면 `continue` 해서,
    #    **가운데 원소가 가운데 자리에 없는 V 배치**를 통째로 놓쳤다.
    #    리뷰어 반례: E(a,b,c) = (0, 1.8e-4, 0.9e-4) Eh → a~c · b~c · a≁b.
    #    실측 결과 `OK` 와 `[['a','c'], ['b','c']]` 를 냈다 — **c 가 두 군집에 중복**됐고
    #    이름 순서를 바꾸면 판정도 바뀌었다.
    #    ⇒ 연결성분(느슨한 묶음)을 만든 뒤 **성분 안의 모든 쌍**이 related 인지 본다.
    #      clique 가 아니면 그 성분은 완전연결로 묶을 수 없다 → CLUSTER_AMBIGUOUS.
    #      이 검사는 세 V 배치를 전부 포괄한다 (triple 을 따로 셀 필요가 없다).
    _idx = {k: i for i, k in enumerate(keys)}
    _par = list(range(len(keys)))

    def _find(x):
        while _par[x] != x:
            _par[x] = _par[_par[x]]
            x = _par[x]
        return x

    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if rel(a, b):
                ra, rb = _find(_idx[a]), _find(_idx[b])
                if ra != rb:
                    _par[ra] = rb
    comp = {}
    for k in keys:
        comp.setdefault(_find(_idx[k]), []).append(k)
    clusters = sorted((sorted(v) for v in comp.values()), key=lambda g: g[0])
    for grp in clusters:
        for i, a in enumerate(grp):
            for b in grp[i + 1:]:
                if not rel(a, b):
                    return {"clusters": None, "n_distinct": None, "n_jobs": len(ok),
                            "unclustered": bad, "excluded_gated": gated,
                            "borderline": border, "verdict": "CLUSTER_AMBIGUOUS",
                            "why": ("연결성분 %s 이 **clique 가 아니다** (%s≁%s) — "
                                    "완전연결로 묶을 수 없다. 문턱을 결과를 보고 "
                                    "고치지 않는다 (회신 U P0-8ⓐ · V P0-4)"
                                    % (grp[:4], a, b))}
    return {"clusters": clusters, "n_distinct": len(clusters),
            "n_jobs": len(ok), "unclustered": bad, "excluded_gated": gated,
            "borderline": border, "verdict": "OK",
            "why": ("서로 다른 seed 가 같은 해로 갔으면 상태 1개다 — "
                    "seed %d개(게이트 제외 %d) → 구분되는 basin %d개 "
                    "(⛔ seed 개수는 반복수가 아니다)"
                    % (len(ok), len(gated), len(clusters)))}


def pil_stability_layer(inp_txt, seg, rejudge_seg=None):
    """3층 — 최종 파동함수 안정성. **불안정하면 재계산 후 다시** 판정해야 한다.

    → (status, why). status ∈ NOT_REQUESTED · NOT_RUN · STABLE ·
                              UNSTABLE_NOT_REJUDGED · UNSTABLE_REJUDGED_STABLE ·
                              UNSTABLE_REJUDGED_UNSTABLE

    ⛔ 못 하는 것: ORCA 의 안정성 분석은 **수렴한 determinant 의 국소최소 여부**만
      본다. 상태를 열거하지 않는다 (회신 S). 그리고 문자열을 읽는 것이므로 판본이
      문구를 바꾸면 `NOT_RUN` 으로 떨어진다 — 조용히 통과시키지 않는 쪽이 맞다.
    """
    if "StabPerform" not in (inp_txt or ""):
        return "NOT_REQUESTED", "입력에 StabPerform 이 없다 — 안정성을 주장하지 않는다"
    if not re.search(r"(?i)stability analysis", seg or ""):
        return "NOT_RUN", "요청했는데 수행 흔적이 없다"
    if not re.search(r"(?i)wavefunction is unstable|instabilit", seg or ""):
        return "STABLE", "안정 (수행 흔적 있음 · 불안정 문구 없음)"
    if not rejudge_seg:
        return ("UNSTABLE_NOT_REJUDGED",
                "불안정한데 따라 내려간 해로 **재계산·재판정한 잡이 없다** — "
                "이 에너지와 스핀분포는 basin 대표가 아니다")
    # ⛔⛔ 회신 V P0-5 (2026-09-02) — **미완결 출력을 대표로 승격하고 있었다.**
    #   리뷰어 재현: restart 출력에서 `ORCA TERMINATED NORMALLY` **한 줄만 지워도**
    #   `UNSTABLE_REJUDGED_STABLE` · gates=[] · 에너지 −100.5 · 전체 `ADEQUATE` 가
    #   나왔다. 잘린 출력의 마지막 SCF 는 수렴한 해가 아닌데 그것을 basin 대표로
    #   삼은 것이다. 원래 잡에는 `NOT_TERMINATED` 게이트가 있었는데 **재계산 잡에는
    #   그 검사가 없었다** — 구제 경로가 게이트를 우회하는 문이 됐다.
    #   ⇒ 판정에 쓰는 **바로 그 segment** 에서 정상종료를 요구한다.
    if "ORCA TERMINATED NORMALLY" not in rejudge_seg:
        return ("UNSTABLE_REJUDGED_UNSTABLE",
                "재계산 출력이 **정상종료하지 않았다** — 잘린 출력의 마지막 SCF 를 "
                "basin 대표로 승격하지 않는다 (회신 V P0-5)")
    if re.search(r"(?i)wavefunction is unstable|instabilit", rejudge_seg):
        return "UNSTABLE_REJUDGED_UNSTABLE", "재계산해도 여전히 불안정하다"
    if not re.search(r"(?i)stability analysis", rejudge_seg):
        return "UNSTABLE_REJUDGED_UNSTABLE", "재계산 출력에 안정성 분석이 없다"
    return "UNSTABLE_REJUDGED_STABLE", "불안정 → 재계산 후 안정 (그 잡을 대표로 쓴다)"


def pilot_acidic_h(csym, cnb, csulf):
    """산성 H (SO₃H 의 H) 를 0-based 로. → [(sulf_idx, S, O, H), ...]"""
    out = []
    for k, su in enumerate(csulf):
        if su.get("aH") is not None:
            o = next((o for o in su["sO"] if su["aH"] in cnb[o]), None)
            out.append((k, su["sS"], o, su["aH"]))
    return out


# ── 폴라론 pilot · 생성 ─────────────────────────────────────────────────────

#: ⛔⛔ 2026-08-31 — 처음엔 `T_Core -1e6` 으로 **코어까지** 국재화했다. 그런데
#:   링 탄소의 C 1s 는 그 자체로 그 링에 ~100% 국재돼 있어서, "목표 집합에 가장
#:   크게 걸린 MO" 를 찾으면 폴라론 궤도가 아니라 **코어 1s 를 고른다.**
#:   그걸 HOMO 로 rotate 하면 코어 홀이지 폴라론이 아니다.
#:   ⇒ 국재화는 **원자가만** (T_Core 는 ORCA 기본값에 맡긴다).
#:   ⚠ 그래도 파서 쪽에서 한 번 더 막는다 — %loc 설정에 의존하지 않기 위해.
# ⛔⛔ 회신 T P0-3 (2026-08-31) — **결정론 국재화 옵션이 실제로 있다.**
#   내가 "ORCA 에 결정론 키워드가 없다" 고 쓴 것이 틀렸다. `%loc Randomize 0`
#   (orca_loc 의 randomize flag 0)이 무작위 seed 를 끈다. 그래서 `.loc` 해시에만
#   결박하는 것은 재현성·robustness 를 대체하지 못한다 (회신 T Q2).
#   ⇒ primary 는 `Randomize 0`(R0, 결정론), 기존 무작위 국재화는 realization R1 로
#     **민감도로 보존**한다. 두 realization 이 다른 최종 basin 집합을 주면
#     `LOCALIZATION_DEPENDENT` 다.
# ⛔⛔ 회신 U P0-1 (2026-09-01) — **키 이름이 틀렸다.**
#   `Randomize 0` 은 ORCA 6.1 의 `%loc` inline 키가 아니다. 공식 키는 **`Random 0`**.
#   ORCA 는 모르는 `%loc` 키를 만나면 조용히 무시하는 게 아니라 판본에 따라 다르게
#   구는데, 어느 쪽이든 **우리가 의도한 결정론이 걸렸다는 보증이 전혀 없었다.**
#   더구나 `OCC`·`VIRT`·`T_CORE` 를 생략해 "occupied valence 만 국재화" 도 보증
#   못 했다 — 코어가 섞이면 seed 로 C 1s 가 뽑히는 그 사고로 되돌아간다.
#   ⇒ 네 키를 **전부 명시**한다. R1(민감도)도 기본값에 맡기지 않고 `Random 1` 을 적는다.
#   ⚠ 이 문자열은 **실물 ORCA 로 확인하기 전까지 미검증**이다 — 해제 순서 ⑥
#     (작은 분자로 `%loc` 구문과 실제 suffix 확인) 이 그래서 있다.
#: 코어 배제선 (Eh). ORCA 기본값에 맡기면 판본마다 달라진다 — 우리가 봉인한다.
PIL_LOC_TCORE_EH = -3.0
PIL_LOC_KW = ("%%loc\n  LocMet PipekMezey\n  Random 0\n"
              "  OCC true\n  VIRT false\n  T_CORE %.1f\nend\n" % PIL_LOC_TCORE_EH)
#: 민감도 realization — 무작위 seed 국재화 (R1). 사전등록 문구에 그렇게 적는다.
#: ⚠ R1 도 `Random 1` 을 **명시**한다. 기본값에 맡기면 판본이 바뀔 때 R0 와 R1 이
#:   같아질 수 있고, 그러면 "두 realization 이 같다" 가 robustness 가 아니라 착시다.
PIL_LOC_KW_RANDOM = ("%%loc\n  LocMet PipekMezey\n  Random 1\n"
                     "  OCC true\n  VIRT false\n  T_CORE %.1f\nend\n" % PIL_LOC_TCORE_EH)
#: MO 별 Löwdin 인구를 찍게 한다 — seed 선택의 **유일한** 근거다.
#: ⛔ 회신 U P0-2 — 인구만으로는 π 를 **회전불변**하게 못 판정한다(대각 성분뿐이라
#:   교차항이 없다). MO 계수도 함께 찍게 한다. 출력이 커지지만 그게 값이다.
PIL_MOPOP_KW = "%output\n  Print[P_OrbPopMO_L] 1\n  Print[P_MOs] 1\nend\n"


def _pil_cpcm(eps):
    """ε=1 이면 진공(블록 없음), 아니면 CPCM. cavity 규약을 manifest 에 기록한다."""
    if eps is None or abs(eps - 1.0) < 1e-9:
        return ""
    return "%%cpcm\n  epsilon %.4f\n  refrac 1.4000\nend\n" % eps


def _pil_inp(path, xyz, charge, mult, wf, eps, functional,
             loc=False, moread=None, rotate=None, stab=False, nprocs=1,
             noiter=False, mopop=False, maxcore=PIL_MAXCORE_MB):
    """pilot 용 ORCA 입력. 관측량 계약(Hirshfeld · open-shell 에 UNO UCO)을 강제한다.

    ⚠ `NoAutoStart` 는 **항상** 켠다 — 같은 basename 의 GBW 를 우연히 물지 않게.
      의도한 lineage 는 `MOInp`/`MORead` 로만 들어온다 (회신 S Q8 게이트: 둘을 구분).
    """
    # ⛔ 회신 T Q4 1층 — `NoIter` probe 에서는 UNO/UCO 를 뺀다.
    # ⚠ 회신 U Q5 (2026-09-01) — **면제 사유 문구를 고쳤다.** 종전 문구
    #   *"NoIter 밀도에서 정의되지 않는다"* 는 과했다. 정확한 문구는:
    #     "UNO/UCO 는 계산·판정하지 않는다. NoIter probe 는 초기 개입 확인만 하며
    #      에너지와 최종 전자상태 해석에 쓰지 않는다."
    #   면제의 근거는 *정의 불가* 가 아니라 **쓰지 않음**이다.
    obs = " Hirshfeld" + ("" if wf == "RKS" or noiter else " UNO UCO")
    kw = "! %s %s TightSCF NoAutoStart%s%s" % (
        wf, functional, " NoIter" if noiter else "", obs)
    # ⛔ 2026-08-31 실측 — `%maxcore` 는 **proc 당** MB 다. 6000 을 박아 두면
    #   `nprocs 6` 이 36 GB 를 요구한다. gabia 는 62 GB 인데 Stage A 가 34 GB 를
    #   쓰고 있어 가용이 28 GB 였다 — 그대로 던졌으면 스왑/OOM 이고, 남의 잡을
    #   같이 죽일 수 있었다. 기계마다 다르므로 **인자로 받는다**.
    body = [kw, "%%maxcore %d" % int(maxcore)]
    # ⛔ 2026-08-31 — `%pal` 이 없으면 ORCA 는 **직렬**로 돈다. 200원자 r2SCAN-3c SP 를
    #   1코어로 돌리면 pilot 이 끝나지 않는다. (병렬 실행은 ORCA 를 **절대경로**로
    #   불러야 한다 — 2026-08-31 stage A 에서 rc=126 으로 실측한 사고다.)
    if nprocs and nprocs > 1:
        body.append("%%pal nprocs %d end" % nprocs)
    scf = []
    if moread:
        body.append('%%moinp "%s"' % moread)
        scf.append("Guess MORead")
        # ⛔⛔ 회신 T P0-3 (2026-08-31) — **이것이 없으면 결과가 조용히 틀린다.**
        #   국재 궤도에는 물리적 에너지 순서가 없다. 그런데 기본 `GuessMode` 는
        #   에너지 기준 정렬(FMatrix)을 전제하므로 ORCA 가 `.loc` 를 읽으면서
        #   MO 를 **재정렬할 수 있다.** 우리 seed 는 `.loc` 인구표의 **인덱스**로
        #   목표를 지정하므로, 재정렬되면 `Rotate {j, nbeta}` 가 **엉뚱한 궤도**를
        #   돈다 — 실패가 아니라 조용한 오답이 된다.
        #   ORCA 는 국재 MO 재사용에 `CMatrix` 를 명시적으로 권고한다.
        scf.append("GuessMode CMatrix")
    if rotate:
        # ⛔⛔ 2026-08-31 실측 — `{from, to, angle, op_from, op_to}` 의 마지막 둘은
        #   **스핀 채널**이다 (0 = 알파, 1 = 베타). 처음엔 `0,0`(알파)로 냈는데
        #   그것은 **완전한 no-op** 이다:
        #     D•(961전자 doublet) = 알파 0..480 **전부 점유** · 베타 0..479 점유
        #     ⇒ 알파 237 ↔ 알파 480 은 둘 다 점유라 밀도가 안 변한다.
        #   홀은 **베타**에 있다. 목표 집합에 스핀을 놓으려면 그 국재 MO 를
        #   **베타의 첫 빈자리**로 보내야 한다 ⇒ 연산자 `1,1`.
        #   (이대로 돌렸으면 seed 전부가 같은 기본 해로 수렴하고 "방법이 backbone
        #    상태를 못 찾는다" 로 오판했을 것이다.)
        scf.append("Rotate {%d, %d, 90, 1, 1} end" % (rotate[0], rotate[1]))
    if stab:
        scf.append("StabPerform true")
    if scf:
        # ⚠ 한 줄로 쓰면 `Rotate {...} end` 의 end 와 `%scf` 의 end 가 붙어 모호하다.
        #   여러 줄로 쓴다 (ORCA 파서에 명확하다).
        body.append("%scf\n  " + "\n  ".join(scf) + "\nend")
    txt = "\n".join(body) + "\n"
    if loc:
        txt += (PIL_LOC_KW_RANDOM if loc == "random" else PIL_LOC_KW)
    # ⛔ MO 별 인구는 **L2**(국재 궤도)에서 쓰지만, L 에서도 찍어 두면 정준/국재를
    #   대조할 수 있다 — 둘 다 켠다. 없으면 seed 선택이 통째로 불가능하다.
    if loc or mopop:
        txt += PIL_MOPOP_KW
    txt += _pil_cpcm(eps)
    txt += "* xyzfile %d %d %s\n" % (charge, mult, xyz)
    with open(path, "w") as f:
        f.write(txt)
    return txt


def pilot_generate(a):
    """phase L(seed 생성원) 만 만든다. phase S 는 L 출력을 읽고 `--polaron_seeds` 가 낸다.

    ⛔ 여기서 phase S 를 미리 만들지 않는 이유: seed 는 **실행 결과(국재 MO 인덱스)에
      의존**한다. 미리 만들면 임의의 MO 를 고르는 것이고, 그건 국재화가 아니다.
    """
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit("⛔ %s 가 비어 있지 않다 — 새 디렉터리를 주세요 (덮어쓰지 않는다)" % out)
    out.mkdir(parents=True, exist_ok=True)
    sym, pos = read_xyz(a.neutral_xyz)
    nb, rings, sulf = analyze(sym, pos)
    amap = pilot_atom_sets(sym, nb, rings, sulf, ether_in_backbone=True)
    amap_alt = pilot_atom_sets(sym, nb, rings, sulf, ether_in_backbone=False)
    acid = pilot_acidic_h(sym, nb, sulf)
    if not acid:
        raise SystemExit("⛔ 산성 H(SO₃H)를 하나도 못 찾았다 — 입력 구조를 확인하세요")
    # H 제거 위치 — 1-based 로 받고 0-based 로 바꾼다. 못 찾으면 **멈춘다**.
    if a.site is None:
        k, sS, sO, sH = acid[len(acid) // 2]          # 중간 위치 (사전 규칙)
        why_site = "사전 규칙: 산성 H 목록의 중간 위치 (%d/%d)" % (len(acid) // 2 + 1, len(acid))
    else:
        want = int(a.site) - 1
        hit = [t for t in acid if t[3] == want]
        if not hit:
            raise SystemExit("⛔ --site %s (1-based) 는 산성 H 가 아니다. 후보(1-based): %s"
                             % (a.site, [t[3] + 1 for t in acid]))
        k, sS, sO, sH = hit[0]
        why_site = "--site %s 로 명시" % a.site
    n_e_neutral = electrons_of(sym)
    _amf = pilot_atom_manifest(sym, nb, rings, sulf, [sH])
    envs = [("eps%g" % e, e) for e in (a.eps or [1.0])]
    # ⛔ 회신 T P0-3 — primary 는 **결정론 국재화**(`%loc Random 0`). 무작위
    #   realization(R1)은 민감도로만 쓰고, 그때는 명시해야 한다.
    #   ⚠ 2026-08-31: 이 두 줄이 `man` 딕셔너리 **뒤**에 있어 `--polaron_pilot` 이
    #     UnboundLocalError 로 죽었다. 선언은 첫 사용보다 앞이어야 한다.
    _loc_rand = str(getattr(a, "loc_realization", "deterministic")) == "random"
    _loc_mode = "random" if _loc_rand else True
    _mc = int(getattr(a, "maxcore", PIL_MAXCORE_MB) or PIL_MAXCORE_MB)
    man = {
        "schema": "polaron_pilot/v1",
        "date": time.strftime("%Y-%m-%d"),
        # ⛔⛔ 회신 U P0-5 (2026-09-01) — **생성물이 S0 사전등록을 안 가리켰다.**
        #   S0 문서가 정본인데 manifest 는 **폐기한 구판 전체-pilot prereg** 를 적었고,
        #   S0 문서가 봉인한 빌더 해시는 실제 빌더와 달랐다. 즉 "무엇을 사전등록했는지"
        #   와 "무엇을 돌렸는지" 가 산출물 안에서 이어지지 않았다.
        #   ⇒ ⓐ S0 문서를 가리키고 ⓑ 그 문서의 **해시를 같이 봉인**한다.
        #     ⓒ 러너·seeds·analyze 가 그 해시를 실물과 대조한다 (아래 _pil_check_prereg).
        "prereg": PIL_PREREG_S0,
        "prereg_sha256": _sha(_repo_path(PIL_PREREG_S0)) if
        _repo_path(PIL_PREREG_S0).is_file() else None,
        "prereg_superseded": PIL_PREREG_LEGACY,
        "⚠_prereg": ("S0 문서가 정본이다. 구판 전체-pilot prereg 는 회신 S 이후 폐기됐고 "
                     "이력으로만 남긴다 (회신 U P0-5)"),
        "decision": "D-2026-08-31-sdcp-polaron-Fbb (proposed)",
        "estimand": "F_bb / F_SO3 / F_other — H-제거 n=6 라디칼의 spin share (조건부)",
        "⛔_아닌것": ("실제 자가도핑 SDCP 에서 캐리어가 백본에 있는가 — 그것은 물질 수준 "
                     "주장이고 이 계산이 시험하지 않는다 (회신 S §1)"),
        "parent_xyz": os.path.abspath(a.neutral_xyz),
        "parent_sha256": _sha(a.neutral_xyz),
        "formula_neutral": formula_of(sym),
        "n_atoms": len(sym), "n_electrons_neutral": n_e_neutral,
        "removed_H_0based": sH, "removed_H_1based": sH + 1,
        "removed_H_site_why": why_site,
        "removed_H_bonded_O_0based": sO, "sulfonate_S_0based": sS,
        "acidic_H_1based_all": [t[3] + 1 for t in acid],
        # ⛔⛔ 회신 T P0-1 — **P(200)/D(199) 를 각각 봉인한다.** 종전엔 중성
        #   200원자 집합 하나와 해시 하나만 실어, D 프레임을 런타임에 파생시켰다.
        #   계산은 맞게 하고 있었지만 산출물에 그 사실이 없었다.
        "atom_manifest": _amf,
        "atom_manifest_hash": _amf["hash"],
        # 하위호환(구판 독자) — **판정에 쓰지 않는다**. 새 코드는 atom_manifest 만 본다.
        "atom_map": amap,
        "atom_map_no_ether": amap_alt,
        "⛔_atom_map_사용금지": ("`atom_map` 은 중성 200원자 프레임 하나뿐이라 "
                                 "D 계(199원자)를 가리킬 수 없다. 판정은 "
                                 "`atom_manifest.P` / `.D` 를 쓴다 (회신 T P0-1)"),
        "backbone_정의": ("primary = 티오펜 고리 + **고리 C 에 직결된 에테르 O** + 고리 H. "
                          "EDOT 의 3,4-O 는 π 에 전자를 밀어넣는 자리라 폴라론 밀도를 갖는다. "
                          "sp³ -CH2CH2- 다리는 공액이 아니므로 other. "
                          "⚠ 분석기가 ether 제외 값도 **같이** 보고한다 — class 가 갈리면 "
                          "BACKBONE_DEFINITION_DEPENDENT (억지 선택 금지)"),
        "functional": a.functional,
        "nprocs": int(a.nprocs),
        # ⛔ proc 당 MB 다. 총 요청 = nprocs × maxcore — 실행 기계의 **가용** 메모리를
        #   넘으면 스왑/OOM 이고, 같은 기계의 남의 잡까지 죽인다.
        "maxcore_mb_per_proc": _mc,
        "memory_request_GB_total": round(int(a.nprocs) * _mc / 1024.0, 1),
        "eps_basis": a.eps_why,
        "environments": {n: {"epsilon": e,
                             "cpcm": ("vacuum (블록 없음)" if abs(e - 1.0) < 1e-9
                                      else "CPCM epsilon=%.4f refrac=1.4000" % e)}
                         for n, e in envs},
        "loc_realization": ("R1_random" if _loc_rand else "R0_deterministic"),
        "loc_realization_why": (
            "회신 T P0-3 — ORCA 6.1 의 `%loc Random 0` 이 무작위 seed 를 끈다. "
            "primary 는 R0(결정론)이고, R1(무작위)은 **민감도 realization** 이다. "
            "두 realization 이 다른 최종 basin 집합을 주면 LOCALIZATION_DEPENDENT."),
        "loc_suffix_assumed": PIL_LOC_SUFFIX_CANDIDATES[0],
        "⚠_loc_suffix": ("생성 시점엔 loccheck 를 안 돌렸으므로 국재 파일 suffix 를 "
                         "**모른다**. ORCA 6.1 문서는 `.loc.gbw` 로 설명하는데 우리 "
                         "코드는 `.loc` 를 기대해 왔다 (회신 V P0-3). 러너의 loccheck "
                         "단계가 실측해 증서에 적고, L2 단계가 그 값으로 `%moinp` 를 "
                         "고친다 — 고치면 그 사실을 화면과 manifest 에 남긴다."),
        "builder_sha256": _sha(__file__),
        "builder_commit": _git_commit(),
        "phase_L_역할": ("seed 생성원. D⁻ 국재화는 D• seed 를, 중성 국재화는 P⁺ seed 를 "
                         "만든다. **D⁻ 잡은 same-nuclei 홀밀도 기준을 겸한다**"),
        "⚠_미검증": ("`%loc` 출력 형식과 `Rotate` 동작을 실제 ORCA 로 확인하지 않았다 — "
                     "phase L 파서와 seed 입력은 smoke test 가 필요하다"),
        "jobs": {},
    }
    # ── phase L ────────────────────────────────────────────────────────────
    kill = [sH]
    dsym, dpos, _ = remove_atoms(sym, pos, kill)
    for en, ev in envs:
        for tag, (csym2, cpos2, ch, mult, roles) in {
            "L_dminus": (dsym, dpos, -1, 1, ["seed_source_for_Dradical", "d_minus_reference"]),
            "L_neutral": (sym, pos, 0, 1, ["seed_source_for_Pcation"]),
        }.items():
            jd = out / "L" / en / tag
            jd.mkdir(parents=True, exist_ok=True)
            write_xyz(jd / (tag + ".xyz"), csym2, cpos2,
                      "%s %s eps=%g" % (tag, man["formula_neutral"], ev))
            _pil_inp(jd / (tag + ".inp"), tag + ".xyz", ch, mult, "RKS", ev,
                     a.functional, loc=_loc_mode, nprocs=a.nprocs, maxcore=_mc)
            man["jobs"]["L/%s/%s" % (en, tag)] = {
                "phase": "L", "env": en, "epsilon": ev, "charge": ch, "mult": mult,
                "wf": "RKS", "roles": roles,
                "n_electrons": electrons_of(csym2) - ch,
                "inp_sha256": _sha(jd / (tag + ".inp")),
                "xyz_sha256": _sha(jd / (tag + ".xyz")),
            }
    # ⛔⛔ 2026-08-31 실측 — phase L 의 `LOEWDIN ORBITAL POPULATIONS PER MO` 는
    #   **정준(canonical) 궤도**의 인구다 (출력 5883줄 vs 국재화 340994줄).
    #   정준 궤도는 비편재라 "이 링에 걸린 MO" 를 거기서 고르는 것은 뜻이 없다.
    #   국재 궤도는 `<tag>.loc` 에 따로 저장된다.
    #   ⇒ phase L2: `.loc` 를 MORead 하고 **SCF 없이(NoIter)** 인구만 다시 찍는다.
    #     seed 선택은 이 출력에서만 하고, seed 입력도 `.loc` 를 읽는다.
    for jk in [k for k in man["jobs"] if man["jobs"][k]["phase"] == "L"]:
        jm = man["jobs"][jk]
        tag = jk.rsplit("/", 1)[-1]
        en = jm["env"]
        jd = out / jk
        j2 = out / "L2" / en / tag
        j2.mkdir(parents=True, exist_ok=True)
        (j2 / (tag + ".xyz")).write_text((jd / (tag + ".xyz")).read_text())
        _pil_inp(j2 / (tag + ".inp"), tag + ".xyz", jm["charge"], jm["mult"],
                 jm["wf"], jm["epsilon"], a.functional,
                 # ⛔ 회신 V P0-3 — 생성 시점엔 loccheck 를 아직 안 돌렸으므로
                 #   suffix 를 **모른다**. 기본값으로 쓰고 `loc_suffix_assumed` 로
                 #   가정임을 남긴다. 러너의 L2 단계가 증서를 보고 필요하면 고친다.
                 moread=os.path.relpath(jd / (tag + PIL_LOC_SUFFIX_CANDIDATES[0]), j2),
                 noiter=True, mopop=True, nprocs=a.nprocs, maxcore=_mc)
        man["jobs"]["L2/%s/%s" % (en, tag)] = {
            "phase": "L2", "env": en, "epsilon": jm["epsilon"],
            "charge": jm["charge"], "mult": jm["mult"], "wf": jm["wf"],
            "reads_localized_from": jk,
            "n_electrons": jm["n_electrons"],
            "roles": ["localized_mo_populations"],
            "why": ("phase L 의 인구는 **정준** 궤도다. seed 선택은 **국재** 궤도의 "
                    "인구로만 한다 (2026-08-31 실측)"),
            "inp_sha256": _sha(j2 / (tag + ".inp")),
        }
    man["seed_plan"] = {
        "Dradical": {"charge": 0, "mult": 2, "wf": "UKS",
                     "seeds": ["A_sulfonate"] + ["B_ring%d" % i for i in range(len(rings))]
                              + ["default"],
                     "from": "L_dminus"},
        "Pcation": {"charge": 1, "mult": 2, "wf": "UKS",
                    "seeds": ["B_ring%d" % i for i in range(len(rings))] + ["default"],
                    "from": "L_neutral",
                    "why": ("positive control — 에너지 기준이 아니라 '이 방법이 알려진 "
                            "형태의 backbone radical cation 을 표현할 수 있는가' (회신 S Q4)")},
        "⛔": "seed 는 phase L 실행 뒤에만 만든다 — 미리 만들면 임의 MO 를 고르는 것이다",
    }
    n_meas = (len(man["seed_plan"]["Dradical"]["seeds"])
              + len(man["seed_plan"]["Pcation"]["seeds"]) + 1) * len(envs)
    _n_probe = (len([x for x in man["seed_plan"]["Dradical"]["seeds"] if x != "default"])
                + len([x for x in man["seed_plan"]["Pcation"]["seeds"]
                       if x != "default"])) * len(envs)
    man["census"] = {
        "seed_generation_SP": len(envs) * 2,
        "measured_SP_예정": n_meas,
        # ⛔ 회신 T Q4 1층 — 개입 확인 probe. `NoIter` 라 싸고, phase S **앞**에 돈다
        "probe_SP_예정": _n_probe,
        "probe_note": ("회신 T Q4 1층 개입 확인 (`NoIter`) — `default` 는 개입이 "
                       "없으므로 없다. 이것은 측정이 아니다 (에너지·class 판정에 "
                       "쓰지 않는다)"),
        "총_ORCA_실행": len(envs) * 2 * 2 + n_meas - len(envs) + _n_probe,
        "note": ("측정 SP = D• %d + P⁺ %d + D⁻ 기준 1, 환경 %d개. D⁻ 기준은 L_dminus 와 "
                 "**같은 계산**이라 따로 돌지 않는다"
                 % (len(man["seed_plan"]["Dradical"]["seeds"]),
                    len(man["seed_plan"]["Pcation"]["seeds"]), len(envs))),
    }
    (out / "MANIFEST_PILOT.json").write_text(
        json.dumps(man, indent=1, ensure_ascii=False))
    (out / "run_pilot.sh").write_text(PIL_RUNNER)
    _nL = sum(1 for v in man["jobs"].values() if v["phase"] == "L")
    _nL2 = sum(1 for v in man["jobs"].values() if v["phase"] == "L2")
    print("→ %s · phase L %d잡 + L2 %d잡 (환경 %d) · 측정 SP 예정 %d"
          % (out, _nL, _nL2, len(envs), n_meas))
    print("   메모리 요청 = %d proc × %d MB = **%.1f GB** — 실행 기계의 `free -g` "
          "가용치보다 작아야 한다 (넘으면 남의 잡까지 죽는다)"
          % (int(a.nprocs), _mc, int(a.nprocs) * _mc / 1024.0))
    print("   제거 H = 1-based %d (%s) · 산성 H 후보 %s"
          % (sH + 1, why_site, man["acidic_H_1based_all"]))
    print("   집합 hash %s · backbone %d · sulfonate %d · other %d"
          % (amap["hash"][:16], len(amap["sets"]["backbone"]),
             len(amap["sets"]["sulfonate"]), len(amap["sets"]["other"])))
    return out


# ── 폴라론 pilot · phase L 판독 + seed 생성 ────────────────────────────────

#: ⛔⛔ 회신 U P0-5 — 사전등록 정본은 **S0 문서**다. 구판 전체-pilot prereg 는 폐기됐다.
PIL_PREREG_S0 = "db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json"
PIL_PREREG_LEGACY = "db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json"


def _repo_path(rel):
    """repo 루트 기준 상대경로 → Path. 이 파일 위치에서 두 단계 위가 루트다.

    ⚠ 절대경로면 그대로 돌려준다 — **selftest 가 자기 픽스처 사전등록을 가리키게**
      하려는 것이다 (production 경로에 우회를 만들지 않고 같은 코드를 지나게 한다).
    """
    _p = Path(rel)
    return _p if _p.is_absolute() else Path(__file__).resolve().parent.parent.parent / rel


#: ⛔⛔ 회신 V P0-3 (2026-09-02) — **국재 궤도 파일의 suffix 를 우리가 모른다.**
#:   코드는 `<tag>.loc` 를 기대하는데 ORCA 6.1 공식 문서는 inline localization 산출을
#:   `.loc.gbw` 로 설명한다. 어느 쪽이 실제 설치본에 맞는지는 **loccheck 가 판정**한다.
#:   그 증서 없이 phase L 을 열면, 200원자 두 잡을 돌리고 나서 seed 생성 단계에서
#:   "파일이 없다" 로 막히게 된다 (또는 더 나쁘게, 엉뚱한 파일을 읽는다).
PIL_LOC_SUFFIX_CANDIDATES = (".loc", ".loc.gbw")
PIL_LOCCHECK_CERT = "LOCCHECK_PASS.json"


def pil_loc_file(dirp, tag, cert=None):
    """국재 궤도 파일 경로. 증서가 suffix 를 정했으면 그것만, 아니면 후보를 훑는다.

    → (Path, suffix) 또는 (None, None).

    ⛔ 못 하는 것: 파일 **내용**이 국재 궤도인지 확인하지 않는다 (이름과 존재만).
    """
    sufs = ([cert["loc_suffix"]] if (cert or {}).get("loc_suffix")
            else list(PIL_LOC_SUFFIX_CANDIDATES))
    for s in sufs:
        p = Path(dirp) / (tag + s)
        if p.is_file():
            return p, s
    return None, None


def pil_read_loccheck(d):
    """`LOCCHECK_PASS.json` 증서를 읽고 **내용까지** 본다. → (cert, 사유).

    증서가 보증해야 하는 것 (회신 V P0-3):
      · ORCA 경로·버전  · 입력·출력 해시
      · 실제로 생긴 국재 파일의 **suffix**
      · 우리 파서 **둘 다**(MO 인구 · MO 계수) 실물 출력에서 PASS

    ⛔ 못 하는 것: 증서 자체의 위조는 막지 못한다 (같은 사용자 위협모델 밖).
      막는 것은 "확인 안 하고 200원자를 여는 것" 이다.
    """
    p = Path(d) / PIL_LOCCHECK_CERT
    if not p.is_file():
        return None, ("%s 가 없다 — `bash run_pilot.sh loccheck` 를 **먼저** 돌릴 것 "
                      "(회신 V P0-3: 순서가 문구가 아니라 게이트여야 한다)" % p)
    try:
        c = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:                                       # noqa: BLE001
        return None, "%s 파싱 실패: %r" % (p, e)
    miss = [k for k in ("orca_path", "orca_version", "inp_sha256", "out_sha256",
                        "loc_suffix", "mopop_parsed", "mos_parsed") if k not in c]
    if miss:
        return None, "증서에 %s 가 없다 — 구판이거나 손으로 만든 것이다" % miss
    if c.get("loc_suffix") not in PIL_LOC_SUFFIX_CANDIDATES:
        return None, ("증서의 loc_suffix %r 가 아는 후보 %s 밖이다"
                      % (c.get("loc_suffix"), list(PIL_LOC_SUFFIX_CANDIDATES)))
    if not (c.get("mopop_parsed") and c.get("mos_parsed")):
        return None, ("loccheck 에서 파서가 실물을 못 읽었다 "
                      "(인구 %r · 계수 %r) — 200원자를 열 이유가 없다"
                      % (c.get("mopop_parsed"), c.get("mos_parsed")))
    return c, "ok"


def _pil_check_prereg(man, where):
    """manifest 가 봉인한 사전등록이 **실물과 같은지** 본다. 다르면 SystemExit.

    ⛔ 못 하는 것: 사전등록의 *내용*이 옳은지는 안 본다 — 결박만 확인한다.
    """
    rel = man.get("prereg")
    # ⚠ `PIL_PREREG_S0` 는 selftest 가 자기 픽스처로 돌릴 수 있게 모듈 전역이다.
    #   production 에서는 언제나 db/properties/…_S0_… 이고, 그 값과 다르면 막는다.
    if rel != PIL_PREREG_S0:
        raise SystemExit(
            "⛔ %s 의 manifest 가 S0 사전등록을 가리키지 않는다 (`prereg`=%r).\n"
            "   회신 U P0-5: 정본은 %s 다. 구판 전체-pilot prereg 로 낸 산출물은 "
            "무엇을 사전등록했는지가 이어지지 않는다 — 생성기를 다시 돌릴 것."
            % (where, rel, PIL_PREREG_S0))
    want = man.get("prereg_sha256")
    p = _repo_path(rel)
    if not want:
        raise SystemExit("⛔ %s 의 manifest 에 `prereg_sha256` 이 없다 — 구판 번들이다 "
                         "(회신 U P0-5). 생성기를 다시 돌릴 것." % where)
    if not p.is_file():
        raise SystemExit("⛔ 사전등록 %s 가 없다 — 결박을 확인할 수 없다" % p)
    got = _sha(p)
    if got != want:
        raise SystemExit(
            "⛔ 사전등록이 생성 이후 **바뀌었다** (%s).\n"
            "   봉인 %s\n   현재 %s\n"
            "   회신 U P0-5: 사전등록을 고쳤으면 그것은 새 사전등록이다 — 결과를 "
            "옛 문서에 붙이지 않는다. 재발행하고 생성기를 다시 돌릴 것." % (p, want, got))
    # ⛔⛔ 회신 V P0-2 (2026-09-02) — **파일만 결박하고 내용은 안 봤다.**
    #   raw SHA 만 맞으면 통과했으므로, 사전등록이 무엇을 봉인했는지(빌더·부모 구조·
    #   ε·범함수·realization)와 실제 생성물이 어긋나도 알 수 없었다.
    #   리뷰어 반례: 정본 final XYZ 는 `b490…` 인데 **미이완** `dp6_gs0_neutral_start.xyz`
    #   (`dd2f…`)도 구조 검사를 통과해 S0 manifest 를 만들 수 있었다.
    #   ⇒ 사전등록의 조건을 **파싱해 교차검증**한다. 하나라도 어긋나면 멈춘다.
    _pj = json.loads(p.read_text(encoding="utf-8"))
    _ev = _pj.get("0_시각_증거") or {}
    _tg = _pj.get("대상") or {}
    bad = []
    # ⛔⛔ 회신 V Q5-1 (2026-09-02 비준 후) — phase L 을 열려면 사전등록이
    #   **비준**돼 있어야 한다. `proposed` 로는 seed 를 만들지 않는다.
    #   1저자 비준(2026-09-02)으로 이 조건이 충족됐고, 그래서 게이트를 올린다.
    if _pj.get("status") not in ("ratified", "active"):
        bad.append("사전등록 status 가 %r 다 — **비준(ratified/active)** 이어야 한다 "
                   "(회신 V Q5-1: 비용 발생 전에 닫는다)" % _pj.get("status"))
    _rt = _pj.get("ratification") or {}
    if _rt.get("state") != "ratified" or _rt.get("role") != "scientific_owner":
        bad.append("사전등록에 사람(scientific_owner) 비준 기록이 없다")
    else:
        import hashlib as _h
        _cc = {k: v for k, v in _pj.items() if k != "ratification"}
        _dg = _h.sha256(json.dumps(_cc, sort_keys=True, ensure_ascii=False)
                        .encode("utf-8")).hexdigest()
        if _rt.get("content_digest") != _dg:
            bad.append("사전등록이 **비준 이후에 바뀌었다** (지문 불일치) — 재승인 필요")
    _wb, _gb = _ev.get("builder_sha256"), man.get("builder_sha256")
    if _wb and _gb and _wb != _gb:
        bad.append("빌더 SHA: 사전등록 %s… ≠ 생성물 %s… — 사전등록이 봉인한 규칙과 "
                   "실제 적용된 규칙이 다르다" % (str(_wb)[:12], str(_gb)[:12]))
    _wc, _gc = _ev.get("builder_commit"), man.get("builder_commit")
    if _wc and _gc and _wc != _gc:
        bad.append("빌더 commit: 사전등록 %s… ≠ 생성물 %s…"
                   % (str(_wc)[:12], str(_gc)[:12]))
    _wp, _gp = _tg.get("parent_sha256"), man.get("parent_sha256")
    if _wp and _gp and _wp != _gp:
        bad.append("부모 구조 SHA: 사전등록 %s… ≠ 생성물 %s… — **다른 구조로 "
                   "만들었다** (미이완 start.xyz 가 통과하던 경로다)"
                   % (str(_wp)[:12], str(_gp)[:12]))
    _wf = _tg.get("functional") or _pj.get("functional")
    if _wf and man.get("functional") and _wf != man["functional"]:
        bad.append("범함수: 사전등록 %r ≠ 생성물 %r" % (_wf, man["functional"]))
    _we = _tg.get("epsilon") or _tg.get("eps")
    if _we is not None:
        _ge = sorted(float(v["epsilon"]) for v in (man.get("environments") or {}).values())
        _wl = sorted(float(x) for x in (_we if isinstance(_we, list) else [_we]))
        if _ge and _wl and _ge != _wl:
            bad.append("환경 ε: 사전등록 %s ≠ 생성물 %s" % (_wl, _ge))
    _wa, _ga = _tg.get("atom_manifest_hash"), man.get("atom_manifest_hash")
    if _wa and _ga and _wa != _ga:
        bad.append("atom_manifest 해시: 사전등록 %s… ≠ 생성물 %s… — P/D 프레임이 "
                   "다르다" % (str(_wa)[:12], str(_ga)[:12]))
    _wr = _tg.get("loc_realization") or _pj.get("loc_realization")
    if _wr and man.get("loc_realization") and _wr != man["loc_realization"]:
        bad.append("국재화 realization: 사전등록 %r ≠ 생성물 %r"
                   % (_wr, man["loc_realization"]))
    if bad:
        raise SystemExit(
            "⛔ %s: 사전등록과 생성물의 **내용**이 어긋난다 (회신 V P0-2 — 파일 해시만"
            " 맞추는 것으로는 부족하다):\n   · %s\n"
            "   사전등록을 현재 빌더·구조에 맞춰 **재발행**하거나, 생성기를 그 조건으로 "
            "다시 돌릴 것." % (where, "\n   · ".join(bad)))


#: ⛔ 2026-08-31 실측 — ORCA 6.1.1 의 실제 헤더는 **REDUCED 가 없다**:
#:     LOEWDIN ORBITAL POPULATIONS PER MO
#:   (`LOEWDIN REDUCED ORBITAL CHARGES` 는 **다른 블록**이다 — 원자별 전하이지
#:    MO 별 인구가 아니다. 이름이 비슷해 헷갈리기 쉽다.)
#:   판본에 따라 REDUCED 가 붙는 경우도 있으므로 **둘 다** 받는다.
PIL_MOPOP_HDRS = ("LOEWDIN ORBITAL POPULATIONS PER MO",
                  "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO")
PIL_MOPOP_HDR = PIL_MOPOP_HDRS[0]
PIL_SEED_MIN_WEIGHT = 40.0   # % — 목표 집합에 이만큼도 안 걸린 MO 는 국재 seed 가 아니다
#: 코어 궤도 배제선 (Eh). C 1s ≈ −10 · O 1s ≈ −19 · S 1s ≈ −89 이고 원자가는 −1 위쪽이다.
#: ⛔ 이게 없으면 링 탄소의 C 1s 가 "그 링에 100% 국재" 라서 seed 로 뽑힌다 —
#:   코어 홀을 만들게 되고 폴라론이 아니다. `%loc` 설정과 **무관하게** 여기서 막는다.
PIL_CORE_CUTOFF_EH = -3.0


def pil_parse_mopop(text, nat):
    """`LOEWDIN REDUCED ORBITAL POPULATIONS PER MO` → (pops, occ, ener) 또는 None.

    pops[mo][atom] = 백분율 합. ORCA 는 MO 를 **열**로 청크 인쇄한다.

    ⛔ 못 하는 것: 인쇄 threshold(기본 0.1%) 아래는 안 찍히므로 합이 100 이 안 될 수
      있다. 그래서 절대 백분율이 아니라 **집합 간 상대 크기**로만 쓴다.
    ⚠ ORCA 실제 출력으로 검증하지 않았다 (smoke test 필요).
    """
    hdr = next((h for h in PIL_MOPOP_HDRS if h in text), None)
    if hdr is None:
        return None
    seg = text.split(hdr)[-1]
    aos = {}                                 # aos[mo][atom][ao라벨] = 인구
    pops, occ, ener = {}, {}, {}
    lines = seg.splitlines()
    i, cur = 0, None
    while i < len(lines):
        ln = lines[i]
        t = ln.split()
        # MO index 머리줄 — 전부 정수이고 2개 이상
        if t and all(x.isdigit() for x in t) and len(t) >= 1 and not ln.startswith(" 0 "):
            nxt = lines[i + 1].split() if i + 1 < len(lines) else []
            nx2 = lines[i + 2].split() if i + 2 < len(lines) else []
            if len(nxt) == len(t) and len(nx2) == len(t):
                try:
                    e = [float(x) for x in nxt]
                    o = [float(x) for x in nx2]
                except ValueError:
                    i += 1; continue
                cur = [int(x) for x in t]
                for m, ee, oo in zip(cur, e, o):
                    ener[m] = ee; occ[m] = oo; pops.setdefault(m, {})
                i += 4                      # 머리 3줄 + 구분선
                continue
        # ⛔⛔ 2026-08-31 실측 — 실제 행은 `  2S   1s   97.0` 처럼 **인덱스와 원소가
        #   붙어 있다** (`36S`·`102S`). 종전 정규식은 사이 공백을 요구해 **한 행도
        #   안 맞았고**, 그래서 pops 가 비어 항상 None 이었다.
        m2 = re.match(r"\s*(\d+)([A-Za-z]{1,2})\s+(\S+)\s+(.*)$", ln)
        if m2 and cur:
            ai = int(m2.group(1))
            _ao = m2.group(3)
            vals = m2.group(4).split()
            if len(vals) == len(cur):
                for mo, v in zip(cur, vals):
                    try:
                        # ⛔ 회신 T P0-2 — AO 라벨별 인구도 남긴다. 원자 합만으로는
                        #   "그 링에 99%" 밖에 못 말하고 **π 인지**는 못 말한다.
                        _slot = aos.setdefault(mo, {}).setdefault(ai, {})
                        _slot[_ao] = _slot.get(_ao, 0.0) + float(v)
                        pops[mo][ai] = pops[mo].get(ai, 0.0) + float(v)
                    except ValueError:
                        pass
        i += 1
    if not pops:
        return None
    if max(max(d) for d in pops.values() if d) >= nat:
        return None                          # 원자 index 가 범위를 넘었다 — 판독 실패
    return pops, occ, ener, aos


#: 회신 T P0-2 문턱 — 실행 전에 봉인한다 (결과 보고 고르지 않는다)
PIL_PI_MIN = 0.60          # 목표 링 원자의 p 밀도 중 **고리 법선 방향** 최소 비율
PIL_PFRAC_MIN = 0.60       # 목표 집합 인구 중 p 성분 최소 비율 (s 지배면 σ 다)
PIL_ONB_MIN = 0.70         # sulfonate seed: 그 집합 인구 중 **O** 위 최소 비율


#: ⛔⛔ 회신 U P0-2 (2026-09-01) — **π 판정이 좌표축에 의존했다.**
#:   종전 식 `Σ n_k² p_k / Σ p_k` 는 Löwdin 인구의 **대각 성분만** 쓴다. 교차항
#:   (p_x p_y 등)이 없으므로 이건 법선 투영이 아니다. 순수한 p_n̂ 궤도에 넣으면
#:       Σ n_k⁴ / Σ n_k²  =  Σ n_k⁴
#:   가 나온다 — n̂ 이 축과 나란하면 1, 대각선(1,1,1)/√3 이면 **1/3** 이다.
#:   리뷰어가 부모 구조 여섯 고리에 이상적 p_normal 을 넣어 재현한 값이
#:   0.529·0.423·0.666·0.342·0.510·0.361 인 게 정확히 이것이다 —
#:   **문턱 0.60 이면 완전한 π 도 6개 중 5개가 탈락한다.** 축 정렬 합성 fixture 가
#:   이 결함을 숨겼다 (selftest 152건 통과).
#:   ⇒ 회전불변 판정은 **MO 계수**가 있어야 한다. 같은 원자·같은 껍질의
#:     (c_x,c_y,c_z) 로 3×3 행렬 P = Σ v vᵀ 를 쌓고 `n̂ᵀPn̂ / tr P` 를 쓴다.
#:     회전 R 에서 v→Rv, n̂→Rn̂ 이므로 값이 불변이고, 이상적 p_n̂ 에서 정확히 1 이다.
PIL_PI_BASIS_OK = "mo_coefficients"       # 이 근거일 때만 π **통과**를 인정한다


def _pil_ao_shell(label):
    """AO 라벨 → (l, 축 0/1/2 또는 None, 껍질키). `2pz` → ('p', 2, '2p') · `1s` → ('s', None, '1s').

    껍질키가 필요한 이유: p_x·p_y·p_z 를 **같은 껍질끼리** 묶어야 벡터가 된다.
    2p 와 3p 를 섞으면 회전 공변이 깨진다 (지름 함수가 달라 서로 직교).
    """
    t = str(label).strip().lower()
    m = re.match(r"^(\d*)([a-z])(.*)$", t)
    if not m:
        return None, None, None
    npr, l, rest = m.group(1), m.group(2), m.group(3)
    if l != "p":
        return l, None, npr + l
    ax = {"x": 0, "y": 1, "z": 2}.get(rest[:1])
    return "p", ax, npr + l


def pil_p_matrix(coef_atoms, tgt):
    """목표 원자들의 p 계수로 3×3 행렬 P = Σ_{원자,껍질} v vᵀ. → (P, tr) 또는 (None, 0).

    `coef_atoms[atom][label] = 계수`. **회전 공변**이다 (같은 껍질의 p 는 벡터로 돈다).

    ⛔ 못 하는 것
      · 겹침 행렬 S 를 쓰지 않는다 (Mulliken 류 대각 근사). 같은 원자·같은 껍질의
        p 끼리는 정확히 직교·규격화라 **껍질 안에서는** 정확하고, 원자 간·껍질 간
        교차 겹침만 무시한다. 우리가 묻는 건 "이 p 뭉치가 법선을 향하는가" 라 충분하다.
      · 위상·마디를 보지 않는다.
    """
    P = [[0.0] * 3 for _ in range(3)]
    tr = 0.0
    for ai, d in (coef_atoms or {}).items():
        if ai not in tgt:
            continue
        shells = {}
        for lab, c in d.items():
            l, ax, key = _pil_ao_shell(lab)
            if l != "p" or ax is None:
                continue
            shells.setdefault(key, [0.0, 0.0, 0.0])[ax] += float(c)
        for v in shells.values():
            for a in range(3):
                for b in range(3):
                    P[a][b] += v[a] * v[b]
            tr += v[0] ** 2 + v[1] ** 2 + v[2] ** 2
    if tr <= 0:
        return None, 0.0
    return P, tr


def pil_parse_mos(text, nat):
    """ORCA `MOLECULAR ORBITALS` 블록 → {mo: {atom: {AO라벨: 계수}}} 또는 None.

    `%output Print[P_MOs] 1 end` 가 있어야 찍힌다. 인구 블록과 같은 열 청크 형식이고
    행은 `  0O   2pz   -0.31  0.02 ...` 처럼 **index 와 원소가 붙어** 나온다.

    ⛔ 못 하는 것
      · 정준/국재 어느 쪽인지 스스로 구분하지 않는다 — **부르는 쪽이 어느 출력인지 안다.**
      · 인쇄 threshold 아래 계수는 안 찍힌다. tr P 가 100% 는 아니다 (비율만 쓴다).
      · 겹침 행렬을 읽지 않는다.
    """
    if "MOLECULAR ORBITALS" not in text:
        return None
    seg = text.split("MOLECULAR ORBITALS")[-1]
    for stop in ("MULLIKEN POPULATION ANALYSIS", "LOEWDIN POPULATION ANALYSIS",
                 "ORBITAL ENERGIES", "TIMINGS"):
        if stop in seg:
            seg = seg.split(stop)[0]
    mos, cur = {}, None
    lines = seg.splitlines()
    i = 0
    while i < len(lines):
        t = lines[i].split()
        if t and all(x.isdigit() for x in t):
            # 머리줄: MO index → (에너지) → (점유) → 구분선
            cur = [int(x) for x in t]
            for m in cur:
                mos.setdefault(m, {})
            i += 1
            while i < len(lines) and not re.match(r"\s*\d+[A-Za-z]", lines[i]):
                i += 1
            continue
        m2 = re.match(r"\s*(\d+)([A-Za-z]{1,2})\s+(\S+)\s+(.*)$", lines[i])
        if m2 and cur:
            vals = re.findall(r"-?\d+\.\d+", m2.group(4))
            if len(vals) == len(cur):
                ai, lab = int(m2.group(1)), m2.group(3)
                for mo, v in zip(cur, vals):
                    slot = mos[mo].setdefault(ai, {})
                    slot[lab] = slot.get(lab, 0.0) + float(v)
        i += 1
    mos = {m: d for m, d in mos.items() if d}
    if not mos:
        return None
    if max(max(d) for d in mos.values()) >= nat:
        return None                              # 원자 index 범위 초과 → 판독 실패
    return mos


def _pil_ao_axis(label):
    """AO 라벨 → ('s'|'p'|'d'|기타, 축 0/1/2 또는 None). `1s`·`2pz`·`pz`·`dz2` 다 받는다."""
    t = str(label).strip().lower().lstrip("0123456789")
    if not t:
        return None, None
    l = t[0]
    if l != "p":
        return l, None
    ax = {"x": 0, "y": 1, "z": 2}.get(t[1:2])
    return "p", ax


def pil_mo_character(ao_mo, group_idx, sym, pos, ring_idx=None, coef_mo=None):
    """⛔ 회신 T P0-2 — 고른 MO 가 **π(고리 법선 p)** 인가 · **O-nonbonding** 인가.

    → {"p_frac", "pi_share", "O_frac", "axis_resolved", "why"}

    왜 필요한가: 전 원자가 공간에서 가장 국재된 MO 를 고르면 C–H/C–C/C–O σ 나
    O/S lone pair 가 뽑힐 수 있다. "그 링에 99%" 는 **공간 위치**만 말하고
    폴라론과 관련된 π 성격을 보증하지 않는다 (회신 T P0-2).

    측정:
      p_frac   = 목표 집합 인구 중 p 성분 비율 (s 지배면 σ). 대각합이라 **회전불변**.
      pi_share = 그 p 밀도 중 **고리 법선 n̂** 방향 비율 — `coef_mo`(MO 계수)로만 낸다:
                     n̂ᵀ P n̂ / tr P,   P = Σ_{원자,껍질} v vᵀ,  v = (c_x, c_y, c_z)
                 회전 R 에서 v→Rv, n̂→Rn̂ 이라 **불변**이고 이상적 p_n̂ 에서 정확히 1.
      pi_upper = 계수가 없을 때 인구 대각으로 낸 값 — **진단 전용, 판정에 안 쓴다.**
                 ⛔ 회신 V Q2: `n̂ᵀPn̂ ≤ (Σ_k |n̂_k| √P_kk)²` 는 *완전한* PSD 대각이라야
                 성립하는데, ORCA 는 인쇄 threshold(기본 0.1%) 아래를 **생략**하므로
                 우리 대각은 전체가 아니다 ⇒ **엄밀한 상한이 아니다.** 누락 질량을
                 포함한 보수 상한 + closure 검사가 생기기 전에는 기각 근거로 못 쓴다.
      O_frac   = 목표 집합 인구 중 산소 위 비율 (sulfonate seed 용)

    ⛔ 이 함수가 **못 하는 것**
      · 실제 궤도 위상·마디를 보지 않는다. 인구/계수의 **각운동량 분해**일 뿐이다.
      · MO 계수가 없으면 `pi_share` 를 내지 않는다 (`pi_basis=None`) — 대각 인구만으로는
        회전불변 판정이 **원리적으로 불가능**하다. 확인 못 함은 통과가 아니다.
      · ORCA 가 p 를 축 없이(`p`) 찍으면 상한조차 못 낸다.
      · 겹침 행렬을 쓰지 않는다 (원자 간·껍질 간 교차 겹침 무시).
    """
    tgt = set(group_idx)
    tot = p_tot = o_tot = 0.0
    pvec = [0.0, 0.0, 0.0]
    axis_seen = False
    for ai, d in (ao_mo or {}).items():
        if ai not in tgt:
            continue
        for lab, v in d.items():
            l, ax = _pil_ao_axis(lab)
            tot += v
            if str(sym[ai]).upper() == "O":
                o_tot += v
            if l == "p":
                p_tot += v
                if ax is not None:
                    axis_seen = True
                    pvec[ax] += v
    if tot <= 0:
        return {"p_frac": None, "pi_share": None, "O_frac": None,
                "axis_resolved": False, "why": "목표 집합에 인구가 없다"}
    out = {"p_frac": round(p_tot / tot, 4),
           "O_frac": round(o_tot / tot, 4),
           "axis_resolved": bool(axis_seen), "pi_share": None,
           "pi_upper": None, "pi_basis": None, "why": None}
    if ring_idx is None:
        out["why"] = "고리를 지정하지 않았다 — π 판정 대상이 아니다 (예: sulfonate)"
        return out
    if not axis_seen:
        out["why"] = ("ORCA 가 p 를 축 없이 찍었다 — 고리 법선 투영을 할 수 없다. "
                      "**확인 못 함이지 통과가 아니다**")
        return out
    ring_pos = [pos[i] for i in ring_idx if str(sym[i]).upper() in ("C", "S")]
    if len(ring_pos) < 3:
        out["why"] = "고리 원자가 3개 미만 — 법선을 만들 수 없다"
        return out
    cx = [sum(q[k] for q in ring_pos) / len(ring_pos) for k in range(3)]
    # 최소제곱 평면의 법선 = 공분산 행렬의 최소 고유벡터
    cov = [[sum((q[a] - cx[a]) * (q[b] - cx[b]) for q in ring_pos)
            for b in range(3)] for a in range(3)]
    try:
        import numpy as _np
        w, v = _np.linalg.eigh(_np.array(cov))
        n = [float(x) for x in v[:, 0]]
    except Exception:                                        # noqa: BLE001
        out["why"] = "법선 계산 실패 (numpy 없음) — 확인 못 함"
        return out
    nn = sum(x * x for x in n) ** 0.5 or 1.0
    n = [x / nn for x in n]
    if p_tot <= 0:
        out["pi_share"] = 0.0
        out["pi_basis"] = "no_p_population"
        out["why"] = "목표 집합에 p 인구가 없다 — π 가 아니다"
        return out
    out["ring_normal"] = [round(x, 4) for x in n]

    # ── ① 엄밀한 **상한** (대각 인구만으로) — 통과는 못 주고 기각은 줄 수 있다 ──
    _sp = sum(pvec)
    if _sp > 0:
        out["pi_upper"] = round(min(1.0, (sum(abs(n[k]) * (pvec[k] / _sp) ** 0.5
                                             for k in range(3))) ** 2), 4)

    # ── ② 회전불변 본 판정 — MO 계수가 있을 때만 ────────────────────────────
    #   ⛔ 종전 `Σ n_k² p_k / Σ p_k` 는 여기서 **삭제됐다**. 그 식은 축 정렬일 때만
    #     맞고 대각 법선에서 1/3 로 무너진다 (회신 U P0-2 재현).
    P, tr = pil_p_matrix(coef_mo, tgt) if coef_mo else (None, 0.0)
    if P is None:
        out["why"] = ("MO 계수가 없어 **회전불변** π 판정을 할 수 없다 "
                      "(`%%output Print[P_MOs] 1 end` 필요). 대각 인구만으로는 "
                      "원리적으로 불가능하다 — 상한 %s 만 알 수 있다"
                      % ("%.3f" % out["pi_upper"] if out["pi_upper"] is not None else "미상"))
        return out
    num = sum(n[a] * P[a][b] * n[b] for a in range(3) for b in range(3))
    out["pi_share"] = round(max(0.0, min(1.0, num / tr)), 4)
    out["pi_basis"] = PIL_PI_BASIS_OK
    # ⛔⛔ 회신 V Q1 (2026-09-02) — **이름을 물리량으로 부르지 않는다.**
    #   `P = Σ v vᵀ` 는 직교 좌표회전에 대해 정확히 불변이다(그건 맞다). 그러나 raw AO
    #   계수는 `CᵀSC = 1` 이지 Euclidean population 이 아니다 — 원자 간·radial shell 간
    #   overlap 을 버린 값이므로 **물리적인 'π share' 가 아니다.**
    #   ⇒ 당분간 `pi_orientation_score` 로 부르고, 알려진 π/σ 실물 대조 또는
    #     `S^{1/2}C` 기반 Löwdin tensor 로 검증되기 전에는 그 이름을 쓴다.
    out["pi_orientation_score"] = out["pi_share"]
    out["⚠_pi_이름"] = (
        "이 값은 **방향 점수**이지 물리적 π share 가 아니다. raw AO 계수는 CᵀSC=1 "
        "이라 overlap 을 버린 vvᵀ 는 Löwdin 인구가 아니다 (회신 V Q1). 회전불변성은 "
        "성립하므로 '고리 법선을 향하는가' 판정에는 쓰되, 원고에 'π 성분 N%' 로 "
        "적지 않는다. 검증 경로: 알려진 π/σ 실물 대조 또는 S^{1/2}C Löwdin tensor.")
    return out


def pil_character_verdict(ch, kind):
    """성격 판정 → (ok, 사유). `kind` = "pi" | "onb". **확인 못 함은 통과가 아니다.**"""
    if ch.get("p_frac") is None:
        return False, "MO_CHARACTER_UNREADABLE(%s)" % ch.get("why")
    if kind == "onb":
        if (ch["O_frac"] or 0) < PIL_ONB_MIN:
            return False, ("SEED_NOT_O_NONBONDING(O 위 인구 %.2f < %.2f — "
                           "sulfonate seed 가 O lone pair 가 아니다)"
                           % (ch["O_frac"], PIL_ONB_MIN))
        if (ch["p_frac"] or 0) < PIL_PFRAC_MIN:
            return False, ("SEED_NOT_O_NONBONDING(p 성분 %.2f < %.2f — s 지배면 "
                           "nonbonding lone pair 가 아니다)"
                           % (ch["p_frac"], PIL_PFRAC_MIN))
        return True, "O-nonbonding (O %.2f · p %.2f)" % (ch["O_frac"], ch["p_frac"])
    # ⛔ 회신 U P0-2 — p_frac 은 대각합이라 회전불변이다. 먼저 본다 (계수 없어도 유효).
    if ch["p_frac"] < PIL_PFRAC_MIN:
        return False, ("SEED_NOT_PI(p 성분 %.2f < %.2f — σ 결합 궤도다)"
                       % (ch["p_frac"], PIL_PFRAC_MIN))
    # ⛔⛔ 회신 V Q2 (2026-09-02) — **상한 기각 경로를 걷는다.**
    #   Cauchy–Schwarz 상한은 *완전한 동일 PSD tensor 의 대각* 이라면 맞다. 그런데
    #   ORCA 는 인쇄 threshold(기본 0.1%) 아래 인구를 **생략**하므로 우리가 가진
    #   대각은 전체 MO 의 것이 아니다 ⇒ 지금 값은 **엄밀한 상한이 아니다.**
    #   게다가 production 은 계수가 없으면 앞에서 먼저 멈추므로 이 경로는 애초에
    #   도달 불가능했다. 누락 질량을 포함한 보수 상한 + closure 검사가 생기기 전에는
    #   `UNRESOLVED` 가 맞다 (회신 V Q2 그대로).
    # ⛔⛔ **통과는 회전불변 근거(MO 계수)에서만 나온다.** 종전에는 대각 인구식이
    #   통과를 줬는데, 그 식은 축 정렬일 때만 맞고 대각 법선에서 1/3 로 무너져
    #   완전한 π 를 6개 중 5개 탈락시켰다 (회신 U P0-2 재현).
    if not ch.get("axis_resolved") or ch.get("pi_share") is None \
            or ch.get("pi_basis") != PIL_PI_BASIS_OK:
        return False, ("MO_CHARACTER_UNRESOLVED(π 를 **회전불변**하게 확인할 수 없다: "
                       "%s) — 확인 못 한 것은 통과가 아니다" % ch.get("why"))
    if ch["pi_share"] < PIL_PI_MIN:
        return False, ("SEED_NOT_PI(p 밀도의 고리법선 성분 %.2f < %.2f — "
                       "면내 p(σ) 다)" % (ch["pi_share"], PIL_PI_MIN))
    return True, "ring-normal π (p %.2f · π %.2f · %s)" % (
        ch["p_frac"], ch["pi_share"], ch["pi_basis"])


#: ⛔⛔ 회신 U P0-4 (2026-09-01) — **국재 MO 에는 잘 정의된 궤도 에너지가 없다.**
#:   종전 `pil_pick_seed_mo` 는 국재 출력에 찍힌 "에너지" 가 −3 Eh 보다 낮으면 코어로
#:   봤다. ORCA 문서가 명시하듯 국재 궤도에는 그 값이 정의되지 않는다 — Fock 대각원소를
#:   찍는 판본도 있고 0 을 찍는 판본도 있다. 즉 **코어 배제가 우연에 걸려 있었다.**
#:   ⇒ 세 겹으로 봉인한다:
#:     ① `%loc` 의 `T_CORE` 를 명시 (국재화 자체가 코어를 안 건드린다)
#:     ② **국재화 전 canonical 창** — phase L 의 `ORBITAL ENERGIES` 에서 ε < T_CORE 인
#:        점유 궤도 수 N_core 를 세고, 국재 인쇄의 index < N_core 를 배제한다
#:        (T_CORE 국재화는 코어를 제자리에 두므로 앞쪽 index 가 곧 코어다)
#:     ③ **AO 성격** — 후보 MO 인구가 코어 껍질(1s 등)에 몰려 있으면 배제
#:   ①②③ 중 ②를 못 만들면 seed 를 만들지 않는다. 조용히 통과시키지 않는다.
PIL_CORE_AO_FRAC = 0.50      # 목표 인구의 이만큼이 코어 껍질이면 코어 MO 다
#: 원소별 코어 껍질 라벨 (원자가 아래). 여기 없는 원소는 코어 없음으로 본다.
PIL_CORE_SHELLS = {
    "H": set(), "HE": set(),
    "LI": {"1s"}, "BE": {"1s"}, "B": {"1s"}, "C": {"1s"}, "N": {"1s"},
    "O": {"1s"}, "F": {"1s"}, "NE": {"1s"},
    "NA": {"1s", "2s", "2p"}, "MG": {"1s", "2s", "2p"}, "AL": {"1s", "2s", "2p"},
    "SI": {"1s", "2s", "2p"}, "P": {"1s", "2s", "2p"}, "S": {"1s", "2s", "2p"},
    "CL": {"1s", "2s", "2p"}, "AR": {"1s", "2s", "2p"},
}


def pil_parse_orbital_energies(text):
    """ORCA `ORBITAL ENERGIES` 블록 → {mo: (occ, E_Eh)} 또는 None. **canonical 전용**.

    이 블록은 SCF 의 정준 궤도 것이다 — 국재화 **전**이라 에너지가 잘 정의된다.

    ⛔ 못 하는 것: 국재 궤도에는 쓸 수 없다 (그게 이 함수가 있는 이유다).
      알파/베타가 따로 찍히면 **마지막 블록**(베타)이 아니라 **첫 블록**(알파)을 쓴다 —
      코어 창을 세는 데는 어느 스핀이든 같지만, 섞어 세면 개수가 두 배가 된다.
    """
    if "ORBITAL ENERGIES" not in text:
        return None
    seg = text.split("ORBITAL ENERGIES")[1]
    for stop in ("MOLECULAR ORBITALS", "MULLIKEN", "LOEWDIN", "SPIN DOWN ORBITALS",
                 "TOTAL SCF ENERGY", "------------------\nORBITAL ENERGIES"):
        if stop in seg:
            seg = seg.split(stop)[0]
    out = {}
    for ln in seg.splitlines():
        m = re.match(r"\s*(\d+)\s+(\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s*$", ln)
        if not m:
            continue
        out[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
    return out or None


def pil_core_window(ener_canon, t_core=PIL_LOC_TCORE_EH):
    """canonical 에너지 → 코어 MO 개수 N_core. 앞쪽 index 가 **연속으로** 코어여야 한다.

    → (n_core, 사유). 연속이 아니면 (None, 사유) — 창을 만들 수 없다는 뜻이다.
    """
    if not ener_canon:
        return None, "canonical ORBITAL ENERGIES 를 못 읽었다"
    idx = sorted(ener_canon)
    core = [m for m in idx if ener_canon[m][1] < t_core]
    if not core:
        return 0, "T_CORE %.1f Eh 아래 궤도가 없다 — 코어 창은 비어 있다" % t_core
    n = len(core)
    if core != idx[:n]:
        return None, ("코어 궤도가 앞쪽에 **연속으로** 있지 않다 (%s) — index 창으로 "
                      "배제할 수 없다" % core[:6])
    if any(ener_canon[m][0] < 1.0 for m in core):
        return None, "코어로 센 궤도에 비점유가 섞였다 — 블록 판독이 어긋났다"
    return n, "canonical ε < %.1f Eh 인 점유 궤도 %d 개" % (t_core, n)


def pil_mo_is_core(ao_atoms, sym, frac=PIL_CORE_AO_FRAC):
    """AO 성격으로 코어 MO 판정. `ao_atoms[atom][라벨] = 인구`. → (bool, 코어비율)."""
    tot = core = 0.0
    for ai, d in (ao_atoms or {}).items():
        el = str(sym[ai]).upper() if ai < len(sym) else ""
        cs = PIL_CORE_SHELLS.get(el, set())
        for lab, v in d.items():
            v = abs(float(v))
            tot += v
            l, _ax, key = _pil_ao_shell(lab)
            if key in cs:
                core += v
    if tot <= 0:
        return False, 0.0
    r = core / tot
    return r >= frac, round(r, 4)


def pil_pick_seed_mo(pops, occ, group_idx, kill=None, core_window=None,
                     aos=None, sym=None):
    """목표 집합에 가장 크게 걸린 **점유 원자가** MO. → (mo, weight_pct) 또는 (None, best).

    ⛔ 코어 궤도를 반드시 뺀다 — 링 탄소의 C 1s 는 그 링에 ~100% 걸려 있어서
      배제하지 않으면 **항상** 그게 뽑힌다 (2026-08-31 실측 전 발견).

    ⛔⛔ 회신 U P0-4 — 배제 근거가 **국재 MO 에너지가 아니다.** 그 값은 정의되지
      않는다. 이제 ⓐ canonical 창(`core_window`, 국재화 **전** 에너지로 셌다)과
      ⓑ AO 성격(`aos`+`sym`) 두 가지로만 거른다.
      `core_window` 가 None 이면 **아무것도 고르지 않는다** — 코어를 못 걸렀다는
      사실을 조용히 넘기지 않기 위해서다.

    ⛔ 못 하는 것: 국재화가 실제로 `T_CORE` 를 존중했는지 스스로 확인 못 한다
      (입력 문자열 검사는 부르는 쪽 몫이다).
    """
    if core_window is None:
        return None, -1.0                    # 창이 없으면 고르지 않는다 (fail-closed)
    kill = set(kill or [])

    def remap(i):                            # 중성 프레임 → H 제거 프레임
        return None if i in kill else i - sum(1 for k in kill if k < i)

    tgt = {remap(i) for i in group_idx}
    tgt.discard(None)
    best, bw = None, -1.0
    for mo, d in pops.items():
        if occ.get(mo, 0.0) < 1.0:
            continue                         # 점유 MO 만
        if mo < core_window:
            continue                         # ⓐ canonical 코어 창
        if aos is not None and sym is not None:
            is_core, _r = pil_mo_is_core(aos.get(mo), sym)
            if is_core:
                continue                     # ⓑ AO 성격
        w = sum(v for a, v in d.items() if a in tgt)
        if w > bw:
            best, bw = mo, w
    if best is None:
        return None, -1.0
    if bw < PIL_SEED_MIN_WEIGHT:
        return None, bw
    return best, bw


def pilot_seeds(d):
    """phase L 출력을 읽고 phase S 입력을 만든다. 하나라도 못 만들면 **멈춘다**."""
    d = Path(d)
    man = json.loads((d / "MANIFEST_PILOT.json").read_text())
    # ⛔ 회신 U P0-5 — 산출물이 **S0 사전등록에 결박**돼 있는지 먼저 본다
    _pil_check_prereg(man, "pilot_seeds(%s)" % d)
    # ⛔ 회신 V P0-3 — seed 생성도 증서를 요구한다. 여기서 막지 않으면 L 을 우회해
    #   들어온 산출물로 seed 를 만들게 된다.
    _lcert, _lwhy = pil_read_loccheck(d)
    if _lcert is None:
        raise SystemExit("⛔ loccheck 증서 없이 seed 를 만들지 않는다 — %s" % _lwhy)
    _amf = man.get("atom_manifest")
    if not _amf:
        raise SystemExit("⛔ MANIFEST_PILOT.json 에 `atom_manifest` 가 없다 — 구판 "
                         "번들이다. P(200)/D(199) 프레임이 봉인돼 있지 않으면 seed 를 "
                         "만들지 않는다 (회신 T P0-1). 생성기를 다시 돌릴 것.")
    kill = [man["removed_H_0based"]]
    nat = man["n_atoms"]
    if _amf["P"]["n_atoms"] != nat or _amf["D"]["n_atoms"] != nat - len(kill):
        raise SystemExit("⛔ atom_manifest 의 원자수가 manifest 와 어긋난다 "
                         "(P %d · D %d · n_atoms %d · kill %d)"
                         % (_amf["P"]["n_atoms"], _amf["D"]["n_atoms"], nat, len(kill)))
    made, probed, report = 0, 0, {}
    for jk, jm in sorted(man["jobs"].items()):
        if jm["phase"] != "L2":
            continue                     # ⛔ 인구는 **L2**(국재 궤도)에서만 읽는다
        src_jk = jm["reads_localized_from"]
        src = d / src_jk                 # `.loc` 와 xyz 는 L 잡에 있다
        jd = d / jk
        tag = jk.rsplit("/", 1)[-1]
        outp = jd / (tag + ".out")
        if not outp.is_file():
            raise SystemExit("⛔ %s 가 없다 — phase L 을 먼저 완주시킬 것" % outp)
        txt = outp.read_text(errors="replace")
        if "ORCA TERMINATED NORMALLY" not in txt:
            raise SystemExit("⛔ %s 가 정상 종료하지 않았다" % outp)
        # ⛔⛔ 회신 T P0-3 (2026-08-31) — 종전 주석은 "결정론을 만들 수 없으므로
        #   실현된 .loc 에 결박한다" 였다. **그 전제가 틀렸다** — `%loc Random 0`
        #   이 있다. 이제 primary 는 결정론 국재화를 **요구**하고, 무작위 국재화는
        #   `--loc_realization random` 으로 명시했을 때만 R1(민감도)로 허용한다.
        #   ⚠ 확인 못 한 것을 통과시키지 않는다: 출력에서 무작위 표지를 찾으면 막는다.
        _rand_marks = ("seeded randomly", "Localizations seeded randomly")
        _is_rand = any(x in txt for x in _rand_marks)
        _want = man.get("loc_realization", "R0_deterministic")
        if _is_rand and _want != "R1_random":
            raise SystemExit(
                "⛔ %s 의 국재화가 **무작위 seed** 로 돌았다 (출력에 %r). primary 는 "
                "`%%loc Random 0` 으로 결정론이어야 한다 (회신 T P0-3). 무작위 "
                "realization 을 민감도로 쓰려면 생성 시 `--loc_realization random` 을 "
                "명시하고 그 사실이 manifest 에 봉인돼야 한다." % (outp, _rand_marks[0]))
        if (not _is_rand) and _want == "R1_random":
            raise SystemExit(
                "⛔ %s 를 R1(무작위 realization)로 선언했는데 출력에 무작위 표지가 "
                "없다 — 선언과 실물이 다르다" % outp)
        # ⛔ 회신 T P0-3 — `.loc` 를 읽는 입력에는 `GuessMode CMatrix` 가 **반드시**
        #   있어야 한다. 없으면 ORCA 가 국재 MO 를 에너지 기준으로 재정렬할 수 있고,
        #   그러면 인덱스로 지정한 Rotate 가 엉뚱한 궤도를 돈다 (조용한 오답).
        _l2inp = jd / (tag + ".inp")
        if _l2inp.is_file() and "GuessMode CMatrix" not in _l2inp.read_text():
            raise SystemExit(
                "⛔ %s 에 `GuessMode CMatrix` 가 없다 — 이 L2 는 국재 MO 를 재정렬된 "
                "순서로 읽었을 수 있다. 그 인구표로 고른 인덱스는 신뢰할 수 없다 "
                "(회신 T P0-3). 입력을 다시 만들고 phase L2 를 다시 돌릴 것." % _l2inp)
        # ⛔ 회신 V P0-3 — suffix 는 **loccheck 증서**가 정한다 (.loc vs .loc.gbw).
        locf, _lsuf = pil_loc_file(src, tag, _lcert)
        if locf is None:
            raise SystemExit(
                "⛔ %s/%s{%s} 가 하나도 없다 — phase L 의 국재 궤도가 없으면 seed 를 "
                "만들 수 없다.\n   loccheck 증서가 정한 suffix: %r (회신 V P0-3)"
                % (src, tag, "|".join(PIL_LOC_SUFFIX_CANDIDATES),
                   (_lcert or {}).get("loc_suffix")))
        loc_sha = _sha(locf)
        is_dm = tag == "L_dminus"
        nat_j = nat - (1 if is_dm else 0)
        pr = pil_parse_mopop(txt, nat_j)
        if pr is None:
            raise SystemExit(
                "⛔ %s 에서 MO 별 Löwdin 인구를 못 읽었다 — `%%output Print[P_OrbPopMO_L] 1` "
                "이 실제로 찍혔는지 확인할 것 (seed 를 임의로 고르지 않는다)" % outp)
        pops, occ, ener, aos = pr
        # ⛔⛔ 회신 U P0-2 — π 판정은 **MO 계수**가 있어야 회전불변이다. 대각 인구만
        #   있으면 통과를 줄 수 없다(상한으로 기각만 가능). 여기서 미리 막는다 —
        #   seed 를 다 만들어 놓고 성격 판정에서 전멸하는 것보다 낫다.
        coefs = pil_parse_mos(txt, nat_j)
        if coefs is None:
            raise SystemExit(
                "⛔ %s 에서 MO 계수를 못 읽었다 — `%%output Print[P_MOs] 1` 이 실제로 "
                "찍혔는지 확인할 것.\n"
                "   회신 U P0-2: 대각 Löwdin 인구만으로는 π 를 **회전불변**하게 판정할 "
                "수 없다 (종전 식은 대각 법선에서 1/3 로 무너져 완전한 π 를 탈락시켰다)."
                % outp)
        # ⛔⛔ 회신 U P0-4 — 코어 배제를 **국재 MO 에너지로 하지 않는다.** 국재 궤도에는
        #   잘 정의된 궤도 에너지가 없다 (ORCA 문서 명시). 국재화 **전**의 canonical
        #   `ORBITAL ENERGIES` 로 창을 세고, AO 성격을 두 번째 그물로 쓴다.
        _srct = src_jk.rsplit("/", 1)[-1]
        _srco = src / (_srct + ".out")
        if not _srco.is_file():
            raise SystemExit("⛔ %s 가 없다 — 국재화 **전** canonical 궤도 에너지가 "
                             "있어야 코어 창을 만든다 (회신 U P0-4)" % _srco)
        _ec = pil_parse_orbital_energies(_srco.read_text(errors="replace"))
        core_win, _cw_why = pil_core_window(_ec, PIL_LOC_TCORE_EH)
        if core_win is None:
            raise SystemExit(
                "⛔ %s 에서 canonical 코어 창을 만들 수 없다 — %s.\n"
                "   회신 U P0-4: 국재 출력의 '에너지' 로 코어를 거르던 종전 방식은 "
                "성립하지 않는다 (국재 궤도에는 그 값이 정의되지 않는다). 창을 못 만들면 "
                "seed 를 만들지 않는다." % (_srco, _cw_why))
        # `%loc` 가 실제로 T_CORE 를 받았는지 입력에서 확인한다 (①의 증거)
        _li = src / (_srct + ".inp")
        if _li.is_file():
            _lit = _li.read_text(errors="replace")
            if "T_CORE" not in _lit or "OCC true" not in _lit:
                raise SystemExit(
                    "⛔ %s 에 `%%loc` 의 `T_CORE`/`OCC true` 가 없다 — 이 국재화는 "
                    "원자가 한정이 보증되지 않는다 (회신 U P0-1·P0-4). 입력을 다시 "
                    "만들고 phase L 을 다시 돌릴 것." % _li)
        # ⛔ 회신 T P0-2 — π/lone-pair 성격 판정에는 **이 계 프레임의** 원소·좌표가
        #   필요하다 (D 는 199, P 는 200). L 잡의 xyz 가 그 프레임 자체다.
        _sy_j, _po_j = read_xyz(src / (tag + ".xyz"))
        if len(_sy_j) != nat_j:
            raise SystemExit(
                "⛔ %s 의 원자수 %d 가 이 계의 %d 와 다르다 — 프레임이 어긋난 채로 "
                "성격 판정을 하면 엉뚱한 원자의 p 밀도를 본다 (회신 T P0-1)"
                % (src / (tag + ".xyz"), len(_sy_j), nat_j))
        # ⛔ 2026-08-31 — L2 를 순회하도록 바꾸면서 `n_electrons` 를 놓쳤다.
        #   그 값은 원본 **L 잡**에 있다 (L2 는 같은 계를 다시 읽을 뿐이다).
        nel = jm.get("n_electrons")
        if nel is None:
            nel = (man["jobs"].get(src_jk) or {}).get("n_electrons")
        if nel is None:
            raise SystemExit("⛔ %s 의 전자수를 모른다 (L 잡 %s 에도 없다) — "
                             "HOMO 인덱스를 계산할 수 없다" % (jk, src_jk))
        # ⛔ 목표 자리는 **S 계(D•/P⁺)의 베타 첫 빈자리**다. 부모(닫힌껍질)의 HOMO
        #   인덱스와 **우연히 같지만**(전자 하나만 빼므로) 뜻이 다르므로 명시 계산한다.
        #     nel_S = electrons_of(조성) − charge_S · n_beta = (nel_S − (mult−1)) / 2
        #     D• : 961전자 mult2 → 베타 480개(0..479) ⇒ 첫 빈자리 = 480
        homo = nel // 2 - 1              # 부모 닫힌껍질 HOMO (참고용)
        spec = man["seed_plan"]["Dradical" if is_dm else "Pcation"]
        env = jm["env"]
        for sd in spec["seeds"]:
            sdir = d / "S" / env / ("Dradical" if is_dm else "Pcation") / sd
            sdir.mkdir(parents=True, exist_ok=True)
            src_xyz = src / (tag + ".xyz")
            xyzn = "%s.xyz" % sd
            (sdir / xyzn).write_text(src_xyz.read_text())
            # S 계의 전자수 — 부모와 **조성은 같고 charge 만 다르다**.
            #   D• (charge 0)  ← D⁻ (charge −1) : 962 − 1 = 961
            #   P⁺ (charge +1) ← P  (charge  0) : 962 − 1 = 961
            _nel_s = nel - (spec["charge"] - jm.get("charge", 0))
            _nbeta = (_nel_s - (spec["mult"] - 1)) // 2   # 베타 점유 수 = 첫 빈자리 index
            rot, w, mo = None, None, None
            if sd != "default":
                # ⛔⛔ 회신 T P0-1 — 목표 집합을 **그 계의 프레임에서 직접** 꺼낸다.
                #   종전엔 중성(200) 집합을 넘기고 `pil_pick_seed_mo` 안에서
                #   remap 했다 — 계산은 맞았지만 어느 프레임인지 산출물에 없었다.
                _fr = _amf["D" if is_dm else "P"]
                if sd == "A_sulfonate":
                    gi = _fr["components"]["sulfonate"]
                else:
                    _rg = _fr["rings"][sd.replace("B_", "")]
                    gi = sorted(set(_rg["core"]) | set(_rg["ether_O"]))
                if max(gi) >= nat_j:
                    raise SystemExit(
                        "⛔ %s/%s: 목표 인덱스 %d 가 이 계의 원자수 %d 를 넘는다 — "
                        "프레임이 어긋났다 (회신 T P0-1)" % (env, sd, max(gi), nat_j))
                mo, w = pil_pick_seed_mo(pops, occ, gi, None, core_window=core_win,
                                         aos=aos, sym=_sy_j)
                if mo is None:
                    raise SystemExit(
                        "⛔ %s/%s: 목표 집합에 %.1f%% 밖에 안 걸린 MO 가 최대다 "
                        "(문턱 %.0f%%). **국재 seed 가 아니므로 만들지 않는다** — "
                        "국재화가 실패했다는 뜻이다 (MODEL_NONDIAGNOSTIC 후보)"
                        % (env, sd, w, PIL_SEED_MIN_WEIGHT))
                # ⛔⛔ 회신 T P0-2 — **97–99% 국재는 π 의 증거가 아니다.**
                #   전 원자가 공간에서 가장 국재된 MO 를 고르면 C–H/C–C/C–O σ 나
                #   O/S lone pair 가 뽑힐 수 있다. 성격을 확인하고, 못 하면 막는다.
                _kind = "onb" if sd == "A_sulfonate" else "pi"
                _ring_pi = None if _kind == "onb" else list(_rg["core"])
                _ch = pil_mo_character(aos.get(mo), gi, _sy_j, _po_j, _ring_pi,
                                       coef_mo=coefs.get(mo))
                _ok_ch, _why_ch = pil_character_verdict(_ch, _kind)
                if not _ok_ch:
                    raise SystemExit(
                        "⛔ %s/%s: 고른 MO %d 가 목표 집합에 %.1f%% 걸리지만 "
                        "**성격이 아니다** — %s\n"
                        "   회신 T P0-2: 공간 국재는 π 를 보증하지 않는다. "
                        "frontier-π subspace 안에서 다시 국재화하거나 이 seed 를 "
                        "MODEL_NONDIAGNOSTIC 으로 선언할 것." % (env, sd, mo, w, _why_ch))
                # ⛔⛔ 2026-08-31 실측 — 고른 MO 가 **HOMO 자체**일 수 있다
                #   (ring5 → mo 480 = HOMO). 그러면 `Rotate {480,480,...}` 이 되어
                #   자기 자신과 회전한다 — 무의미하거나 ORCA 가 거부한다.
                #   그 경우 회전이 **필요 없다**: 홀이 이미 그 자리에 생긴다.
                #   목표 = 베타 첫 빈자리 (_nbeta). 고른 MO 가 이미 거기면 회전 불필요.
                rot = None if mo == _nbeta else (mo, _nbeta)
            # ⛔ **`.loc`** 를 읽는다. `.gbw`(정준)를 읽으면 국재 인구로 고른
            #   인덱스가 다른 궤도를 가리킨다 (2026-08-31 실측).
            gbw = os.path.relpath(locf, sdir)
            _pil_inp(sdir / (sd + ".inp"), xyzn, spec["charge"], spec["mult"],
                     spec["wf"], jm["epsilon"], man["functional"],
                     moread=(None if sd == "default" else gbw),
                     rotate=rot, stab=True, nprocs=man.get("nprocs", 1),
                     maxcore=man.get("maxcore_mb_per_proc", PIL_MAXCORE_MB))
            # ⛔⛔ 회신 T Q4 1층 — **초기 개입 확인 probe**. 회전을 걸었다는 사실은
            #   그 자리에 스핀이 놓였다는 증거가 아니다. `NoIter` 로 SCF 전 밀도의
            #   스핀 분포를 계의 **실제** charge/mult 에서 찍는다.
            #   (예: D• 961전자 doublet → Nα/Nβ = 481/480. 부모의 닫힌껍질이 아니다.)
            _grp = "Dradical" if is_dm else "Pcation"
            _pk = None
            if sd != "default":
                pdir = d / "S0P" / env / _grp / sd
                pdir.mkdir(parents=True, exist_ok=True)
                (pdir / xyzn).write_text(src_xyz.read_text())
                _pil_inp(pdir / (sd + "_probe.inp"), xyzn, spec["charge"], spec["mult"],
                         spec["wf"], jm["epsilon"], man["functional"],
                         moread=os.path.relpath(locf, pdir), rotate=rot,
                         stab=False, noiter=True, nprocs=man.get("nprocs", 1),
                         maxcore=man.get("maxcore_mb_per_proc", PIL_MAXCORE_MB))
                _pk = "S0P/%s/%s/%s" % (env, _grp, sd)
                man["jobs"][_pk] = {
                    "phase": "S0P", "env": env, "epsilon": jm["epsilon"],
                    "charge": spec["charge"], "mult": spec["mult"], "wf": spec["wf"],
                    "seed": sd, "probe_of": "S/%s/%s/%s" % (env, _grp, sd),
                    "target_group": sd,
                    "atom_frame": ("D" if is_dm else "P"),
                    "n_electrons": _nel_s,
                    "rotate": (None if rot is None else list(rot)),
                    "roles": ["initial_intervention_probe"],
                    "why": ("회신 T Q4 1층 — 회전 직후 **SCF 전** 밀도의 스핀이 목표 "
                            "집합에 있나. 없으면 이 seed 는 다른 출발점이 아니다"),
                    # ⚠ 회신 U Q5 — 문구 정정. "정의되지 않는다" 는 과했다.
                    "observable_exemption": (
                        "UNO/UCO 는 **계산·판정하지 않는다.** NoIter probe 는 초기 개입 "
                        "확인만 하며 에너지와 최종 전자상태 해석에 쓰지 않는다 "
                        "(회신 U Q5 문구 정정 — 근거는 '정의 불가' 가 아니라 '쓰지 않음')"),
                    "inp_sha256": _sha(pdir / (sd + "_probe.inp")),
                }
                probed += 1
            man["jobs"]["S/%s/%s/%s" % (env, "Dradical" if is_dm else "Pcation", sd)] = {
                "phase": "S", "env": env, "epsilon": jm["epsilon"],
                "charge": spec["charge"], "mult": spec["mult"], "wf": spec["wf"],
                "seed": sd, "seed_source": jk,
                # ⛔⛔ 회신 T P0-4 (2026-08-31) — 종전엔 **default 에도** 이 두
                #   필드를 찍었다. default 는 `moread=None` 이라 `.loc` 를 읽지
                #   않는 fresh guess 인데, 읽지도 않는 파일을 출처로 기록한 셈이다.
                #   리뷰가 "ring5 와 default 가 같은 seed" 로 읽은 것도 이 때문이다.
                "orbitals_from": (None if sd == "default"
                                  else os.path.relpath(locf, d).replace(os.sep, "/")),
                "loc_sha256": (None if sd == "default" else loc_sha),
                "initial_guess": ("fresh_default (ORCA 기본 guess — `.loc` 를 읽지 "
                                  "않는다. 국재 seed 들과 **다른 초기 density** 다)"
                                  if sd == "default" else
                                  "localized_MORead (%s · GuessMode CMatrix)"
                                  % os.path.basename(str(locf))),
                "seed_equivalence_class": (
                    "fresh_guess" if sd == "default" else
                    ("localized_no_rotation" if rot is None else "localized_rotated")),
                "loc_realization": man.get("loc_realization", "R0_deterministic"),
                "⚠_국재화_조건부": (
                    "이 seed 는 `loc_sha256` 의 국재화 realization 에 **조건부**다. "
                    "R0(결정론, `%loc Random 0`)이 primary 이고 R1(무작위)은 "
                    "민감도다. 두 realization 이 다른 최종 basin 집합을 주면 "
                    "LOCALIZATION_DEPENDENT — `.loc` 해시 결박은 정확한 재실행에 "
                    "필요하지만 robustness 를 대체하지 않는다 (회신 T Q2)"),
                # ⛔ 회신 T P0-1 — 어느 프레임의 어느 집합으로 골랐는지 남긴다
                "atom_frame": ("D" if is_dm else "P"),
                "atom_frame_hash": _amf["D" if is_dm else "P"]["hash"],
                "atom_manifest_hash": _amf["hash"],
                "target_group": (None if sd == "default" else sd),
                "n_atoms_this_system": nat_j,
                "seed_mo": (mo if sd != "default" else None),
                "seed_mo_weight_pct": (None if w is None else round(w, 2)),
                # ⛔ 회신 T P0-2 — **왜 그 MO 가 seed 로 적격인지**를 남긴다
                "seed_mo_character": (None if sd == "default" else _ch),
                "seed_mo_character_verdict": (None if sd == "default" else _why_ch),
                "seed_character_thresholds": (None if sd == "default" else
                                              {"p_frac_min": PIL_PFRAC_MIN,
                                               "pi_share_min": PIL_PI_MIN,
                                               "O_frac_min": PIL_ONB_MIN,
                                               "⚠": "결과 보기 전에 봉인한 문턱이다"}),
                "homo_index_parent": homo,
                "n_electrons": _nel_s,
                "beta_first_empty": _nbeta,
                "rotate_operator": "1,1 (베타) — 알파는 전부 점유라 no-op 이다",
                "rotate": (None if rot is None else list(rot)),
                "rotate_skipped_why": (None if rot is not None or sd == "default"
                                       else "고른 MO 가 HOMO 자체다 — 회전 불필요"),
                "roles": ["measured"],
                # ⛔ 회신 T Q4 1층 — `default` 는 개입이 없으므로 probe 도 없다
                "intervention_probe": _pk,
                "inp_sha256": _sha(sdir / (sd + ".inp")),
                "xyz_sha256": _sha(sdir / (xyzn)),
            }
            report.setdefault(env, []).append(
                "%s/%s mo=%s%s w=%s" % ("D•" if is_dm else "P⁺", sd,
                                        mo if mo is not None else "-",
                                        "(=HOMO,회전없음)" if (mo is not None
                                                              and rot is None) else "",
                                        ("%.1f%%" % w) if w is not None else "-"))
            made += 1
    man["seeds_made"] = made
    man["probes_made"] = probed          # 회신 T Q4 1층 — 개입 확인 probe
    man["seeds_made_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (d / "MANIFEST_PILOT.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print("→ phase S 입력 %d개 + 1층 개입 probe %d개 (회신 T Q4)" % (made, probed))
    for env, rows in sorted(report.items()):
        print("  [%s] %s" % (env, " · ".join(rows)))
    return made


# ── 폴라론 pilot · selftest 픽스처 (⚠ 생산 경로 아님) ──────────────────────
#  ⛔ 2026-08-31 채택 이유: `pilot_generate` 는 `_loc_rand` 선언순서 때문에
#     UnboundLocalError 로, `pilot_seeds` 는 4-튜플을 3개로 풀면서 ValueError 로
#     **둘 다 첫 줄에서 죽어 있었다.** 그런데 selftest 40건은 전부 통과했다 —
#     순수 헬퍼만 부르고 두 함수를 **한 번도 실행하지 않았기 때문**이다.
#     그래서 여기서는 합성 다이머로 phase L/L2 산출물을 만들어 **실제로 돌린다**.

def _pil_fake_mopop(mos, ener, occ, rows):
    """selftest 용 ORCA `LOEWDIN ORBITAL POPULATIONS PER MO` 블록.

    rows = [(원자 0-based, 원소, AO라벨, {mo: 인구}), ...]

    ⛔ 못 하는 것: 실제 ORCA 출력이 아니라 **우리 파서가 받는 형식**의 재현이다.
      형식이 판본에 따라 다르면 이 픽스처는 그것을 잡지 못한다 (그건 실물 smoke test 몫).
    """
    t = "LOEWDIN ORBITAL POPULATIONS PER MO\n" + "-" * 34 + "\n"
    t += "      " + "".join("%10d" % x for x in mos) + "\n"
    t += "      " + "".join("%10.4f" % ener[x] for x in mos) + "\n"
    t += "      " + "".join("%10.4f" % occ[x] for x in mos) + "\n"
    t += "      " + "-" * (10 * len(mos)) + "\n"
    for ai, sy, ao, d in rows:
        t += ("%4d%-2s%6s" % (ai, sy, ao)
              + "".join("%10.4f" % d.get(x, 0.0) for x in mos) + "\n")
    return t + "\n"


def _pil_fake_mos(mos, ener, occ, rows):
    """selftest 용 ORCA `MOLECULAR ORBITALS` 계수 블록 (회신 U P0-2).

    인구 rows 와 **같은 자료**에서 계수를 만든다: c = √(인구/100). 한 방향 p 뭉치면
    이게 정확히 맞는 관계라 인구와 계수가 서로 모순되지 않는다.

    ⛔ 못 하는 것: 위상(부호)을 재현하지 않는다 — 전부 +. 실제 ORCA 는 부호가 섞인다.
      우리 판정식은 vvᵀ 라 전역 부호에 무관하지만, **원자 간 부호 상쇄는 재현 못 한다.**
    """
    t = "MOLECULAR ORBITALS\n" + "-" * 18 + "\n"
    t += "      " + "".join("%10d" % x for x in mos) + "\n"
    t += "      " + "".join("%10.5f" % ener[x] for x in mos) + "\n"
    t += "      " + "".join("%10.5f" % occ[x] for x in mos) + "\n"
    t += "      " + "-" * (10 * len(mos)) + "\n"
    for ai, sy, ao, d in rows:
        t += ("%4d%-2s%6s" % (ai, sy, ao)
              + "".join("%10.6f" % ((d.get(x, 0.0) / 100.0) ** 0.5) for x in mos) + "\n")
    return t + "\n"


def _pil_fake_orbener(ener, occ):
    """selftest 용 canonical `ORBITAL ENERGIES` 블록 (회신 U P0-4).

    phase L 의 **SCF** 출력이다 — 국재화 전이라 에너지가 잘 정의된다.
    """
    t = "ORBITAL ENERGIES\n" + "-" * 16 + "\n"
    t += "  NO   OCC          E(Eh)            E(eV)\n"
    for m in sorted(ener):
        t += "%4d   %.4f  %14.6f %14.4f\n" % (m, occ[m], ener[m], ener[m] * 27.2114)
    return t + "\n"


def _pil_fake_loccheck(out, suffix=".loc", mopop=True, mos=True, drop_key=None):
    """selftest 용 loccheck 증서 (회신 V P0-3). 인자들이 **음성 경로**다."""
    c = {"schema": "loccheck_pass/v1",
         "orca_path": "/fake/orca", "orca_version": "Program Version 6.1.1",
         "orca_sha256": "0" * 64,
         "inp_sha256": "1" * 64, "out_sha256": "2" * 64,
         "loc_suffix": suffix, "loc_sha256": "3" * 64,
         "mopop_parsed": mopop, "mos_parsed": mos}
    if drop_key:
        c.pop(drop_key, None)
    (Path(out) / PIL_LOCCHECK_CERT).write_text(json.dumps(c, ensure_ascii=False))
    return c


def _pil_fake_phaseL(out, man, rand_mark=False, kill_guessmode=False, no_mopop=False,
                     sigma_ring=False, bad_term=False, no_mos=False, no_orbener=False,
                     kill_tcore=False, no_loccheck=False, loc_suffix=".loc",
                     loccheck_bad=None):
    """selftest 용 phase L/L2 산출물(.loc/.out) 생성. 인자들이 **음성 경로**다."""
    out = Path(out)
    # ⛔ 회신 V P0-3 — 증서가 없으면 seed 생성이 막혀야 한다 (`no_loccheck`).
    if not no_loccheck:
        _pil_fake_loccheck(out, suffix=loc_suffix,
                           mopop=(loccheck_bad != "mopop"),
                           mos=(loccheck_bad != "mos"),
                           drop_key=(loccheck_bad if loccheck_bad in
                                     ("orca_version", "loc_suffix") else None))
    amf = man["atom_manifest"]
    for jk, jm in man["jobs"].items():
        if jm["phase"] != "L2":
            continue
        tag = jk.rsplit("/", 1)[-1]
        src = out / jm["reads_localized_from"]
        (src / (tag + loc_suffix)).write_text("fake localized orbitals\n")
        fr = amf["D" if tag == "L_dminus" else "P"]
        sy, _ = read_xyz(src / (tag + ".xyz"))
        rg = {k: sorted(set(v["core"]) | set(v["ether_O"]))
              for k, v in fr["rings"].items()}
        su = fr["components"]["sulfonate"]
        # MO 0 = 코어(에너지 −20 Eh, 링에 100%) · 40 = 가상(점유 0, 링에 99%)
        #   → 둘 다 뽑히면 안 된다. 뽑히면 성격 검사에서 죽으므로 **강한 음성**이다.
        mos = [0, 5, 6, 7, 40]
        ener = {0: -20.0, 5: -0.50, 6: -0.45, 7: -0.40, 40: 0.10}
        occ = {0: 2.0, 5: 2.0, 6: 2.0, 7: 2.0, 40: 0.0}
        pz = "2px" if sigma_ring else "2pz"      # 합성 다이머의 고리 법선은 ẑ 다
        rows = []
        for gk, mo in zip(sorted(rg), (5, 6)):
            per = 96.0 / len(rg[gk])
            rows += [(ai, sy[ai], pz, {mo: per}) for ai in rg[gk]]
        _o = [i for i in su if str(sy[i]).upper() == "O"]
        _s = [i for i in su if str(sy[i]).upper() == "S"]
        rows += [(ai, sy[ai], "2py", {7: 90.0 / len(_o)}) for ai in _o]
        rows += [(ai, sy[ai], "3px", {7: 8.0 / len(_s)}) for ai in _s]
        _r0 = rg[sorted(rg)[0]]
        rows += [(ai, sy[ai], "1s", {0: 100.0 / len(_r0)}) for ai in _r0]
        rows += [(ai, sy[ai], "2pz", {40: 99.0 / len(_r0)}) for ai in _r0]
        txt = "no populations here\n" if no_mopop else _pil_fake_mopop(mos, ener, occ, rows)
        # ⛔ 회신 U P0-2 — MO **계수** 블록. 없으면 상위가 멈춰야 한다 (`no_mos`).
        if not no_mos:
            txt += _pil_fake_mos(mos, ener, occ, rows)
        if rand_mark:
            txt += "Localizations seeded randomly\n"
        txt += "" if bad_term else "ORCA TERMINATED NORMALLY\n"
        (out / jk / (tag + ".out")).write_text(txt)
        # ⛔ 회신 U P0-4 — phase L 의 **canonical** 출력. 코어 창을 여기서 센다.
        #   MO 0 만 −20 Eh 라 T_CORE(−3) 아래 = 창 1 → 국재 인쇄의 index 0 이 배제된다.
        if not no_orbener:
            (src / (tag + ".out")).write_text(
                _pil_fake_orbener(ener, occ) + "ORCA TERMINATED NORMALLY\n")
        else:
            (src / (tag + ".out")).write_text("ORCA TERMINATED NORMALLY\n")
        if kill_guessmode:
            f = out / jk / (tag + ".inp")
            f.write_text(f.read_text().replace("GuessMode CMatrix", "GuessMode FMatrix"))
        if kill_tcore:
            # ⚠ 주석 처리로는 안 된다 — 문자열이 남아 검사를 통과한다(실측). **줄을 지운다.**
            f = src / (tag + ".inp")
            if not f.is_file():
                raise AssertionError("픽스처 전제 붕괴: %s 가 없다" % f)
            f.write_text("\n".join(l for l in f.read_text().splitlines()
                                   if "T_CORE" not in l) + "\n")
    return out

def _pil_fake_sout(charge, mult, nel, spins, E, S2=0.7530, stable=True,
                   stability=True, echo=True):
    """selftest 용 phase S/probe ORCA 출력. `spins` = 원자별 스핀 리스트.

    ⛔ 못 하는 것: 실제 ORCA 출력이 아니다 — **우리 판독기가 받는 최소 형식**이다.
    """
    t = "* O   R   C   A *\n"
    if echo:
        t += ("Total Charge           Charge          ....    %d\n"
              "Multiplicity           Mult            ....    %d\n"
              "Number of Electrons    NEL             ....    %d\n"
              % (charge, mult, nel))
    if stability:
        t += "Stability Analysis of the SCF solution\n"
        t += ("The wavefunction is unstable\n" if not stable
              else "The wavefunction is stable\n")
    # ⛔⛔ 회신 U P0-3 — fixture 가 **두 블록에 똑같이 콜론을 넣어** 실물과 달랐다.
    #   ORCA 6.1 은 Loewdin 에만 `:` 를 쓰고 Hirshfeld 에는 안 쓴다. fixture 가
    #   인위적으로 콜론을 넣은 탓에 "Hirshfeld 를 못 읽는다" 는 결함이 152건 통과
    #   뒤에 숨었다. ⇒ 여기서는 **각 블록의 공식 형식을 그대로** 쓴다.
    t += ("-" * 43 + "\nLOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS\n" + "-" * 43 + "\n")
    for i, m in enumerate(spins):
        t += "%4d %-2s:%11.6f%11.6f\n" % (i, "C", 0.0, m)
    t += "\n"
    t += ("-" * 18 + "\nHIRSHFELD ANALYSIS\n" + "-" * 18 + "\n"
          "Total integrated alpha density =    %12.6f\n"
          "Total integrated beta density  =    %12.6f\n\n"
          "  ATOM     CHARGE      SPIN    \n" % (nel / 2.0, nel / 2.0))
    for i, m in enumerate(spins):
        t += "%4d %-2s %11.6f %11.6f\n" % (i, "C", 0.0, m)     # ← 콜론 없음 (실물)
    t += "\n"
    t += "<S**2>     =    %.4f\n" % S2
    t += "FINAL SINGLE POINT ENERGY   %.8f\n" % E
    t += "ORCA TERMINATED NORMALLY\n"
    return t


def _pil_fake_phaseS(out, man, probe_wrong=(), flat_ring=(), unstable=(),
                     no_stab=(), degenerate=False, drop_probe=(),
                     drop_pcation=False, flip_spin=()):
    """selftest 용 phase S + 1층 probe 산출물. 인자들이 **음성 경로**다.

    · `degenerate=True`  같은 에너지 (스핀 벡터는 seed 마다 다르다)
    · `degenerate="all"` 에너지도 스핀도 전부 같다 → basin **1개** (회신 U P0-6)
    · `drop_pcation`     positive control 출력을 전부 안 만든다 (회신 U P0-9)
    · `flip_spin`        그 seed 의 스핀을 전역 반전 (회신 U P0-8ⓓ)
    """
    out = Path(out)
    amf = man["atom_manifest"]

    def tgt_idx(fr, sd):
        c = amf[fr]["components"]
        if sd == "A_sulfonate":
            return sorted(c["sulfonate"])
        if str(sd).startswith("B_ring"):
            rg = amf[fr]["rings"][str(sd)[2:]]
            return sorted(set(rg["core"]) | set(rg["ether_O"]))
        return sorted(amf[fr]["rings"]["ring0"]["core"])       # default → ring0

    def vec(fr, idx, flat=False):
        n = amf[fr]["n_atoms"]
        v = [0.0] * n
        if flat:                       # 두 링에 반씩 — 어느 링인지 분해 안 된다
            rs = [sorted(set(r["core"]) | set(r["ether_O"]))
                  for r in amf[fr]["rings"].values()]
            for r in rs:
                for i in r:
                    v[i] = 0.5 / len(r)
        else:
            for i in idx:
                v[i] = 1.0 / len(idx)
        return v

    _ord = {k: i for i, k in enumerate(sorted(k for k, v in man["jobs"].items()
                                                if v["phase"] == "S"))}
    for jk, jm in sorted(man["jobs"].items()):
        if jm["phase"] not in ("S", "S0P"):
            continue                                   # L/L2 는 이미 만들어져 있다
        fr = jm.get("atom_frame") or ("D" if "/Dradical/" in jk else "P")
        sd = jm["seed"]
        if jm["phase"] == "S0P":
            if sd in drop_probe:
                continue
            # 잘못된 개입: 목표가 아닌 **다른** 집합에 스핀을 놓는다
            _i = tgt_idx(fr, "B_ring1" if sd != "B_ring1" else "B_ring0") \
                if sd in probe_wrong else tgt_idx(fr, sd)
            (out / jk / (sd + "_probe.out")).write_text(_pil_fake_sout(
                jm["charge"], jm["mult"], jm["n_electrons"], vec(fr, _i),
                -1.0, stability=False))
            continue
        if jm["phase"] != "S":
            continue
        if drop_pcation and "/Pcation/" in jk:
            continue                       # 회신 U P0-9 — 결측은 방법 실패가 아니다
        # ⛔ `hash()` 는 프로세스마다 값이 달라 시험이 흔들린다 — 정렬 순번을 쓴다
        _E = -100.0 if degenerate else -100.0 - 0.01 * _ord[jk]
        # `degenerate="all"` 은 스핀 벡터까지 같게 만든다 → basin 이 정확히 1개
        _v = (vec(fr, tgt_idx(fr, "B_ring0")) if degenerate == "all"
              else vec(fr, tgt_idx(fr, sd), flat=(sd in flat_ring)))
        if sd in flip_spin:
            _v = [-x for x in _v]          # 회신 U P0-8ⓓ — 전역 α↔β 반전
        (out / jk / (sd + ".out")).write_text(_pil_fake_sout(
            jm["charge"], jm["mult"], jm["n_electrons"], _v, _E,
            stable=(sd not in unstable), stability=(sd not in no_stab)))
    return out

def pilot_restart(d):
    """3층 구제 — 불안정으로 게이트된 잡을 **따라 내려간 해**로 재계산할 입력을 만든다.

    ORCA 는 안정성 분석에서 불안정을 찾으면 그 방향을 따라간 궤도를 `.gbw` 에 남긴다.
    그것을 `MORead` 해서 같은 기하·같은 설정으로 다시 돌리고 **안정성을 다시** 본다.
    새 잡은 manifest 에 `restart_of` 로 연결되고, 분석기가 그것을 3층 재판정에 쓴다.

    ⛔ 못 하는 것
      · 재계산이 **안정해진다는 보장은 없다.** 여전히 불안정하면 3층은
        `UNSTABLE_REJUDGED_UNSTABLE` 이고 그 잡은 basin 대표가 아니다.
      · 이것은 상태 탐색이 아니다 — 같은 basin 안에서 더 낮은 determinant 로
        내려가는 것뿐이다. 새 seed 를 만드는 것과 혼동하지 않는다.
      · 이미 `restart_of` 가 있는 잡은 다시 만들지 않는다 (무한 사슬 방지).
    """
    d = Path(d)
    man = json.loads((d / "MANIFEST_PILOT.json").read_text())
    # ⛔ 회신 U P0-5 — 산출물이 **S0 사전등록에 결박**돼 있는지 먼저 본다
    _pil_check_prereg(man, "polaron_restart(%s)" % d)
    res = pilot_analyze(d)
    made = []
    for jk, r in sorted(res["jobs"].items()):
        if (r.get("stability") or {}).get("status") != "UNSTABLE_NOT_REJUDGED":
            continue
        jm = man["jobs"][jk]
        if jm.get("restart_of"):
            continue
        tag = jk.rsplit("/", 1)[-1]
        gbw = d / jk / (tag + ".gbw")
        if not gbw.is_file():
            raise SystemExit("⛔ %s 가 없다 — 불안정을 따라 내려간 궤도가 없으면 "
                             "재계산의 출발점이 없다 (그냥 다시 돌리면 같은 해로 "
                             "간다)" % gbw)
        _, env, grp, sd = jk.split("/")
        rd = d / "SR" / env / grp / sd
        rd.mkdir(parents=True, exist_ok=True)
        xyzn = "%s.xyz" % sd
        (rd / xyzn).write_text((d / jk / xyzn).read_text())
        rk = "SR/%s/%s/%s" % (env, grp, sd)
        _pil_inp(rd / (sd + ".inp"), xyzn, jm["charge"], jm["mult"], jm["wf"],
                 jm["epsilon"], man["functional"],
                 moread=os.path.relpath(gbw, rd), rotate=None, stab=True,
                 nprocs=man.get("nprocs", 1),
                 maxcore=man.get("maxcore_mb_per_proc", PIL_MAXCORE_MB))
        man["jobs"][rk] = {
            "phase": "SR", "env": env, "epsilon": jm["epsilon"],
            "charge": jm["charge"], "mult": jm["mult"], "wf": jm["wf"],
            "seed": sd, "restart_of": jk,
            "atom_frame": jm.get("atom_frame"), "n_electrons": jm.get("n_electrons"),
            "orbitals_from": os.path.relpath(gbw, d).replace(os.sep, "/"),
            "gbw_sha256": _sha(gbw),
            "roles": ["stability_rejudge"],
            "why": ("회신 T Q4 3층 — 불안정한 해를 따라 내려간 궤도로 재계산하고 "
                    "**안정성을 다시** 본다. 이 잡이 basin 대표가 된다"),
            "inp_sha256": _sha(rd / (sd + ".inp")),
        }
        made.append(rk)
    (d / "MANIFEST_PILOT.json").write_text(
        json.dumps(man, indent=1, ensure_ascii=False))
    print("→ 3층 재판정 입력 %d개%s" % (len(made), (" · " + " · ".join(made)) if made else ""))
    return len(made)

# ── 폴라론 pilot · 분석 ─────────────────────────────────────────────────────

def pilot_analyze(d):
    """phase S 결과 → F 집합 · class · 민감도 · 종료 규칙. 전부 fail-closed."""
    d = Path(d)
    man = json.loads((d / "MANIFEST_PILOT.json").read_text())
    # ⛔ 회신 U P0-5 — 산출물이 **S0 사전등록에 결박**돼 있는지 먼저 본다
    _pil_check_prereg(man, "pilot_analyze(%s)" % d)
    kill = [man["removed_H_0based"]]
    # ⛔⛔ 회신 T P0-1 — **봉인된 프레임**을 쓴다. 런타임에 remap 을 다시 하지
    #   않는다 (계산은 같아도 산출물이 어느 프레임을 썼는지 말하지 못했다).
    _amf = man.get("atom_manifest")
    if not _amf:
        raise SystemExit("⛔ MANIFEST_PILOT.json 에 `atom_manifest` 가 없다 — 구판 "
                         "번들이다. P(200)/D(199) 프레임 봉인 없이 판정하지 않는다 "
                         "(회신 T P0-1).")
    res = {"schema": "polaron_pilot_result/v2",
           "prereg": man["prereg"], "decision": man["decision"],
           "atom_manifest_hash": _amf["hash"],
           "atom_frame_hash": {"P": _amf["P"]["hash"], "D": _amf["D"]["hash"]},
           "remap_hash": _amf["remap"]["hash"],
           "loc_realization": man.get("loc_realization", "R0_deterministic"),
           "blocks": [], "jobs": {}, "verdict": None}

    def frame_sets(is_dm, ether):
        """⛔ 회신 T Q3 — 네 성분에서 strict/extended 를 **파생**한다.

        strict   = bb_core
        extended = bb_core + ether_O
        sulfonate·other 는 그대로. 합은 항상 그 계의 원자수다.
        """
        fr = _amf["D" if is_dm else "P"]
        c = fr["components"]
        bb = (sorted(set(c["bb_core"]) | set(c["ether_O"])) if ether
              else sorted(c["bb_core"]))
        other = (sorted(c["other"]) if ether
                 else sorted(set(c["other"]) | set(c["ether_O"])))
        sets = {"backbone": bb, "sulfonate": sorted(c["sulfonate"]), "other": other}
        if sum(len(v) for v in sets.values()) != fr["n_atoms"]:
            raise SystemExit("⛔ 파생 집합 합이 원자수와 다르다 (%s)" % fr["n_atoms"])
        rings = {g: (sorted(set(v["core"]) | set(v["ether_O"])) if ether
                     else sorted(v["core"])) for g, v in fr["rings"].items()}
        return {"sets": sets, "rings": rings}

    def remap_sets(is_dm, mp=None):
        """하위호환 shim — `mp` 는 무시하고 봉인 프레임을 돌려준다."""
        return frame_sets(is_dm, ether=True)

    def _grp_idx(frame, tgt):
        """seed 이름 → 그 프레임의 목표 원자 index. 모르면 None."""
        fr = _amf[frame]
        if tgt == "A_sulfonate":
            return sorted(fr["components"]["sulfonate"])
        if str(tgt).startswith("B_"):
            rg = fr["rings"].get(str(tgt)[2:])
            if rg:
                return sorted(set(rg["core"]) | set(rg["ether_O"]))
        return None

    # ── 1층: 초기 개입 probe 판독 (회신 T Q4) ─────────────────────────────
    #  ⛔ probe 는 `NoIter` 라 **에너지·class 판정에 쓰지 않는다.** 오직
    #    "회전이 목표 자리에 스핀을 놓았나" 만 본다.
    probes = {}
    for pk, pm in sorted(man["jobs"].items()):
        if pm.get("phase") != "S0P":
            continue
        pd = d / pk
        pout = pd / (pm["seed"] + "_probe.out")
        pv = {"probe_job": pk, "share": None, "status": None}
        if not pout.is_file():
            pv["status"] = "PROBE_NOT_RUN"
        else:
            pseg = _last_segment(pout.read_text(errors="replace"))
            if "ORCA TERMINATED NORMALLY" not in pout.read_text(errors="replace"):
                pv["status"] = "PROBE_NOT_TERMINATED"
            else:
                _natp = man["n_atoms"] - (1 if pm.get("atom_frame") == "D" else 0)
                _hp = _hirshfeld_spins(pseg, _natp)
                _gi = _grp_idx(pm.get("atom_frame") or "P", pm.get("target_group"))
                if _hp is None:
                    pv["status"] = "PROBE_SPIN_MISSING"
                elif not _gi:
                    pv["status"] = "PROBE_TARGET_UNKNOWN"
                else:
                    _tt = sum(abs(v) for v in _hp)      # _spin_block 은 **리스트**
                    if _tt <= 0:
                        pv["status"] = "PROBE_NO_SPIN(초기밀도에 스핀이 없다 — "
                        pv["status"] += "회전이 알파 채널이거나 no-op 이었을 수 있다)"
                    else:
                        pv["share"] = round(
                            sum(abs(_hp[i]) for i in _gi if i < len(_hp)) / _tt, 4)
                        pv["status"] = ("INTERVENED" if pv["share"] >= PIL_PROBE_MIN
                                        else "SEED_INTERVENTION_FAILED")
        pv["threshold"] = PIL_PROBE_MIN
        probes[pm["probe_of"]] = pv

    for jk, jm in sorted(man["jobs"].items()):
        if jm["phase"] != "S":
            continue
        jd = d / jk
        tag = jk.rsplit("/", 1)[-1]
        outp = jd / (tag + ".out")
        r = {"env": jm["env"], "seed": jm["seed"], "seed_mo": jm.get("seed_mo"),
             "gates": []}
        if not outp.is_file():
            r["gates"].append("NOT_RUN"); res["jobs"][jk] = r; continue
        txt = outp.read_text(errors="replace")
        seg0 = _last_segment(txt)
        if "ORCA TERMINATED NORMALLY" not in txt:
            r["gates"].append("NOT_TERMINATED")

        # ── 3층: 최종 전자 안정성 (회신 T Q4) — **판정 재료보다 먼저** ─────────
        #  ⛔⛔ 회신 U P0-7 (2026-09-01): 종전에는 안정성만 재계산 출력에서 보고
        #    에너지·스핀·class·군집은 계속 **원래 불안정 출력**에서 읽었다.
        #    재현: 원래 −100.01 Eh · restart −100.5 Eh 인데 결과가
        #    `UNSTABLE_REJUDGED_STABLE` 이면서 에너지는 −100.01 그대로였다.
        #    ⇒ 재판정이 안정하면 **그 잡이 basin 대표**이므로 판정 재료를 전부
        #      재계산 출력에서 읽는다. `judged_from` 에 어느 잡인지 남긴다.
        _rej = None
        for _rk, _rm in man["jobs"].items():
            if _rm.get("restart_of") == jk:
                _ro = d / _rk / (_rk.rsplit("/", 1)[-1] + ".out")
                if _ro.is_file():
                    _rej = _last_segment(_ro.read_text(errors="replace"))
                    r["restart_job"] = _rk
        _st, _sw = pil_stability_layer((jd / (tag + ".inp")).read_text(), seg0, _rej)
        r["stability"] = {"status": _st, "why": _sw}
        if _st in ("NOT_RUN", "UNSTABLE_NOT_REJUDGED", "UNSTABLE_REJUDGED_UNSTABLE"):
            r["gates"].append("STABILITY_%s(%s)" % (_st, _sw))
        if _st == "UNSTABLE_REJUDGED_STABLE" and _rej is not None:
            seg = _rej
            r["judged_from"] = r.get("restart_job")
            r["⚠_판정_출처"] = ("원래 해가 불안정해 **재계산 출력**에서 에너지·스핀·"
                                "class 를 읽었다 (회신 U P0-7). 원래 출력의 값은 "
                                "basin 대표가 아니다")
        else:
            seg = seg0
            r["judged_from"] = jk
        # charge/mult/전자수 echo — 선언이 아니라 **출력 확인** (회신 S Q8)
        mch = re.search(r"Total Charge\s+Charge\s+\.+\s+(-?\d+)", seg)
        mmu = re.search(r"Multiplicity\s+Mult\s+\.+\s+(\d+)", seg)
        mne = re.search(r"Number of Electrons\s+NEL\s+\.+\s+(\d+)", seg)
        if not (mch and mmu and mne):
            r["gates"].append("ECHO_MISSING(charge/mult/NEL 되울림 없음)")
        else:
            got = (int(mch.group(1)), int(mmu.group(1)), int(mne.group(1)))
            want = (jm["charge"], jm["mult"], None)
            r["echo"] = {"charge": got[0], "mult": got[1], "nel": got[2]}
            if got[0] != want[0] or got[1] != want[1]:
                r["gates"].append("ECHO_MISMATCH(선언 %s ≠ 출력 %s)"
                                  % (want[:2], got[:2]))
        m_s2 = re.findall(r"<S\*\*2>\s*(?:=|\.+)\s*(-?\d+\.\d+)", seg)
        if m_s2:
            r["S2_raw"] = float(m_s2[-1])          # ⚠ raw 보존 (회신 S Q8)
            if jm["mult"] == 2 and not (0.75 <= r["S2_raw"] <= 0.80):
                r["gates"].append("S2_OUT_OF_WINDOW(%.4f — doublet quality gate)"
                                  % r["S2_raw"])
        else:
            r["gates"].append("S2_MISSING")
        is_dm = "/Dradical/" in jk
        # ⛔ 회신 T Q3 — strict(bb_core) / extended(bb_core+ether_O) **둘 다** 낸다
        sm = frame_sets(is_dm, ether=True)
        sm_strict = frame_sets(is_dm, ether=False)
        r["atom_frame"] = "D" if is_dm else "P"
        r["atom_frame_hash"] = _amf["D" if is_dm else "P"]["hash"]
        nat = man["n_atoms"] - (1 if is_dm else 0)
        low = _lowdin_spins(seg, nat)
        hir = _hirshfeld_spins(seg, nat)
        if low is None:
            r["gates"].append("LOWDIN_SPIN_MISSING(또는 행 재배열)")
        if hir is None:
            r["gates"].append("HIRSHFELD_SPIN_MISSING(두 분할을 둘 다 계산해야 한다)")
        if low is not None and hir is not None:
            sl = pilot_shares(low, sm)
            sh = pilot_shares(hir, sm)
            r["lowdin"], r["hirshfeld"] = sl, sh
            r["partition"] = pilot_partition_check(sl.get("F"), sh.get("F"))
            if sh.get("F"):
                r["class"] = pilot_class(sh["F"])          # Hirshfeld primary
                r["threshold_sensitivity"] = pilot_threshold_sensitivity(sh["F"])
                if r["threshold_sensitivity"]["threshold_dependent"]:
                    r["gates"].append("THRESHOLD_DEPENDENT")
            if r["partition"].get("partition_dependent"):
                r["gates"].append("PARTITION_DEPENDENT")
            # ⛔⛔ 회신 T Q3 — backbone 정의가 estimand 를 움직인다. **둘 다** 낸다.
            #   extended = bb_core + ether_O · strict = bb_core.
            #   갈리면 BACKBONE_DEFINITION_DEPENDENT 이고, 억지로 하나를 고르지 않는다.
            sh2 = pilot_shares(hir, sm_strict)
            r["hirshfeld_strict"] = {"F": sh2.get("F"),
                                     "class": pilot_class(sh2.get("F"))
                                     if sh2.get("F") else None}
            # ether O 에 얼마나 있는지 **따로** 본다 — 그것이 갈림의 원인이면
            #   "backbone 폴라론" 이 아니라 ETHER_O_CENTERED 라고 말해야 한다.
            _fr_c = _amf["D" if is_dm else "P"]["components"]
            # ⛔ `_spin_block` 은 **리스트**를 돌려준다 (dict 가 아니다). 종전
            #   `hir.values()`·`hir.get(i)` 는 AttributeError 로 죽었다 — 분석기를
            #   한 번도 실행하지 않아 몰랐던 것이다 (2026-08-31 e2e 로 발견).
            _abs_tot = sum(abs(v) for v in hir) or 1.0
            r["F_ether_O"] = round(
                sum(abs(hir[i]) for i in _fr_c["ether_O"] if i < len(hir))
                / _abs_tot, 4)
            r["F_components"] = {
                g: round(sum(abs(hir[i]) for i in _fr_c[g] if i < len(hir))
                         / _abs_tot, 4)
                for g in ("bb_core", "ether_O", "sulfonate", "other")}
            c1 = (r.get("class") or (None,))[0]
            c2 = (r["hirshfeld_strict"]["class"] or (None,))[0]
            if c1 != c2:
                r["gates"].append(
                    "BACKBONE_DEFINITION_DEPENDENT(extended %s / strict %s — "
                    "억지로 하나를 고르지 않는다. ether O 몫 %.3f)"
                    % (c1, c2, r["F_ether_O"]))
                if r["F_ether_O"] >= max(r["F_components"]["bb_core"],
                                         r["F_components"]["sulfonate"]):
                    r["gates"].append(
                        "ETHER_O_CENTERED(스핀이 고리 π 가 아니라 3,4-에테르 O 에 "
                        "가장 많다 — 'backbone 폴라론' 이라고 부르지 않는다)")
        m_e = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", seg)
        r["E_Eh"] = float(m_e[-1]) if m_e else None
        if r["E_Eh"] is None:
            r["gates"].append("NO_ENERGY")

        # ── 1층: 초기 개입 (회신 T Q4) ────────────────────────────────────
        _pv = probes.get(jk)
        if jm.get("seed") == "default":
            r["intervention"] = {"status": "NO_INTERVENTION",
                                 "why": ("fresh guess — 개입이 없으므로 확인할 것도 "
                                         "없다. 국재 seed 들과 **다른 출발점**이다")}
        elif _pv is None:
            r["intervention"] = {"status": "PROBE_ABSENT",
                                 "why": ("이 seed 에 개입 probe 가 없다 — 회전이 목표 "
                                         "자리에 스핀을 놓았는지 확인할 수 없다")}
            r["gates"].append("SEED_INTERVENTION_UNVERIFIED(probe 없음)")
        else:
            r["intervention"] = _pv
            if _pv["status"] != "INTERVENED":
                r["gates"].append(
                    "SEED_INTERVENTION_%s(초기밀도 목표몫 %s < %.2f — 이 seed 는 "
                    "다른 출발점이 아니다)"
                    % ("FAILED" if _pv["status"] == "SEED_INTERVENTION_FAILED"
                       else "UNVERIFIED", _pv["share"], PIL_PROBE_MIN))

        # ── 2층: 최종 명중 / 분해 가능성 (회신 T Q4) ──────────────────────
        _rp = (r.get("hirshfeld") or {}).get("ring_p")
        r["ring_p"] = _rp
        _tg = jm.get("target_group")
        # ⛔ `"B_ring0"[2:]` 이 이미 `"ring0"` 이다 — 앞에 "ring" 을 또 붙이면
        #   `"ringring0"` 이 되어 **명중이 영원히 False** 다 (2026-08-31 e2e 로 발견).
        _tgr = _tg[2:] if str(_tg).startswith("B_ring") else None
        # ⛔ "어느 링인가" 는 **backbone 에 스핀이 있을 때만** 성립하는 질문이다.
        #   SO₃ 중심 해에 링 분해를 요구하면 정상 결과를 오답 처리한다.
        _fbb = ((r.get("hirshfeld") or {}).get("F") or {}).get("backbone")
        if _fbb is None or _fbb < PIL_CLASS_MIN:
            r["target_hit"] = {"applicable": False, "resolved": None,
                               "why": ("backbone 몫 %s < %.2f — 링 분해 질문이 "
                                       "성립하지 않는다 (class 가 본다)"
                                       % (None if _fbb is None else round(_fbb, 3),
                                          PIL_CLASS_MIN))}
        else:
            r["target_hit"] = pil_target_hit(_rp, _tgr)
            r["target_hit"]["applicable"] = True
            if not r["target_hit"]["resolved"]:
                r["gates"].append("TARGET_UNRESOLVED(%s)" % r["target_hit"]["why"])

        # ── 4층 재료 — 군집은 루프 뒤에서 한 번에 (회신 T Q4) ─────────────
        r["_basin"] = {
            "E_Eh": r["E_Eh"], "ring_p": _rp, "S2": r.get("S2_raw"),
            "nel": (r.get("echo") or {}).get("nel") or jm.get("n_electrons"),
            "spin_vec": ([round(hir[i], 6) for i in range(min(nat, len(hir)))]
                         if hir is not None else None),
            # ⛔ 회신 U P0-8ⓑ — 게이트가 걸린 행은 군집 입력에서 **뺀다**.
            #   basin 수는 "통과한 실행이 몇 개의 상태를 줬나" 이지 시도 횟수가 아니다.
            "passed": not r["gates"],
            # ⛔ 회신 U P0-8ⓒ — backbone 몫이 낮아 링 판정을 면제한 해에는 링 축을
            #   군집에서도 뺀다. 면제해 놓고 backbone 내부 정규화 `ring_p` 로 묶으면
            #   작은 잡음이 basin 을 가른다.
            "ring_applicable": bool((r.get("target_hit") or {}).get("applicable"))}
        if r["_basin"]["spin_vec"]:
            r["spin_vector_sha256"] = hashlib.sha256(
                json.dumps(r["_basin"]["spin_vec"]).encode()).hexdigest()
        res["jobs"][jk] = r

    # ── 4층: 실현 basin 군집 (회신 T Q4) ─────────────────────────────────
    #  ⛔⛔ **seed 개수는 반복수가 아니다.** 서로 다른 seed 가 같은 해로 갔으면
    #     상태는 1개다. 이 계수를 안 하면 "8개 seed 가 backbone 을 지지" 처럼
    #     같은 해를 여덟 번 센 문장이 나온다.
    res["basins"] = {}
    for _sc in sorted({(v["env"], ("Dradical" if "/Dradical/" in k else "Pcation"))
                       for k, v in res["jobs"].items()}):
        # ⛔ 2026-09-01 — `NOT_RUN` 잡은 `_basin` 자체가 없다 (루프가 먼저 continue
        #   한다). 종전 `v["_basin"]` 은 그때 **KeyError 로 분석기 전체를 죽였다** —
        #   회신 U P0-9 음성시험(Pcation 결측)이 그것을 드러냈다. 없는 것은 없는 대로
        #   두고 군집에서 뺀다 (게이트가 이미 잡고 있다).
        _rows = {k: v["_basin"] for k, v in res["jobs"].items()
                 if v["env"] == _sc[0] and ("/%s/" % _sc[1]) in k and "_basin" in v}
        res["basins"]["%s/%s" % _sc] = pil_basin_cluster(_rows)
    for v in res["jobs"].values():
        v.pop("_basin", None)
    res["seed_vs_basin"] = {
        g: {"n_seeds": b["n_jobs"], "n_distinct_basins": b["n_distinct"],
            "clusters": b["clusters"], "borderline": b["borderline"],
            "unclustered": b["unclustered"]}
        for g, b in res["basins"].items()}
    res["⛔_seed는_반복수가_아니다"] = (
        "같은 basin 에 모인 seed 들은 **하나의 실현 상태**다. 지지 증거의 개수로 "
        "세지 않는다 (회신 T Q4 4층). 군집 재료: 전자수·에너지·⟨S²⟩·원자별 부호 "
        "있는 스핀 벡터·링 몫 벡터. 임계 근처 쌍은 `borderline` 으로 남긴다")
    res["four_layer_thresholds"] = {
        "layer1_probe_min": PIL_PROBE_MIN, "layer2_hit_margin": PIL_HIT_MARGIN,
        "layer4_dE_Eh": PIL_BASIN_DE_EH, "layer4_spin_L1": PIL_BASIN_SPIN_L1,
        "layer4_ring_L1": PIL_BASIN_RING_L1, "layer4_dS2": PIL_BASIN_S2,
        "⚠": "결과를 보기 전에 봉인한 값이다 (코드 상수)"}

    # ── 사전등록 seed 전건 receipt (회신 S Q8) ────────────────────────────
    want = set()
    for env in man["environments"]:
        for sp, spec in (("Dradical", man["seed_plan"]["Dradical"]),
                         ("Pcation", man["seed_plan"]["Pcation"])):
            for sd in spec["seeds"]:
                want.add("S/%s/%s/%s" % (env, sp, sd))
    miss = sorted(want - set(res["jobs"]))
    bad = sorted(k for k, v in res["jobs"].items() if v["gates"])
    if miss:
        res["blocks"].append("SEED_RECEIPT_MISSING(%d건 %s) — 하나라도 빠지면 "
                             "lowest-found 판정 금지" % (len(miss), miss[:3]))
    if bad:
        res["blocks"].append("GATED_JOBS(%d건 %s)" % (len(bad), bad[:3]))

    # ══ 회신 U P0-6·P0-9 (2026-09-01) — **S0 전용 판정 기계** ════════════════
    #
    #  ⛔⛔ 종전 분석기는 폐기한 **전체-pilot** 결론을 냈다: 최저 에너지 잡을 골라
    #    `BACKBONE_SUPPORTED` / `SO3_CENTERED_WITHIN_MODEL` 을 냈고, `ADEQUATE`
    #    경로가 **코드에 아예 없었다.** S0 사전등록은 정반대를 말한다 —
    #    *"S0 은 에너지 순서를 판정하지 않는다"* (⛔_통과해도_말할_수_없는_것).
    #    그리고 D• basin 이 하나여도 막지 않았다 (합격 조건 ②).
    #
    #  ⛔⛔ P0-9 — 순서도 틀렸다. positive-control 판정이 `blocks` 보다 **먼저**
    #    실행돼, Pcation 출력을 전부 지우면 `GATED_JOBS` 가 있는데도
    #    `MODEL_NONDIAGNOSTIC`(= 방법이 틀렸다)이 나왔다. **실행 실패·결측은
    #    언제나 `NO_VALUE`** 이고, `MODEL_NONDIAGNOSTIC` 은 계획된 positive control 이
    #    **전부 정상 판정됐는데도** backbone 상태가 없을 때만이다.
    #
    #  판정어는 사전등록(db/properties/sdcp_polaron_pilot_prereg_S0_*.json)의
    #  `판정어` 절이 정본이다.

    # ── ① 게이트/결측이 먼저다 (P0-9) ────────────────────────────────────
    _DEP = ("PARTITION_DEPENDENT", "THRESHOLD_DEPENDENT",
            "BACKBONE_DEFINITION_DEPENDENT", "ETHER_O_CENTERED")
    _codes = sorted({g.split("(")[0] for v in res["jobs"].values() for g in v["gates"]})
    res["gate_codes"] = _codes
    _dep_hit = [c for c in _DEP if c in _codes]
    res["dependency_verdicts"] = _dep_hit
    if res["blocks"]:
        # "돌려놓고 판정만 보류" 유형만 남았으면 그 판정어로 닫는다 (사전등록 중단_규칙)
        if _dep_hit and set(_codes) <= set(_DEP):
            res["verdict"] = _dep_hit[0]
            res["why"] = ("값은 남기고 판정어로 닫는다 — %s (억지로 하나를 고르지 "
                          "않는다)" % ", ".join(_dep_hit))
        else:
            res["verdict"] = "NO_VALUE"
            res["why"] = ("blocks 를 해소하기 전에는 판정하지 않는다. **실행 실패·결측은 "
                          "방법 실패가 아니다** (회신 U P0-9) — %s" % res["blocks"][:2])
        return res

    # ── ② positive control adequacy (회신 S Q4 · U P0-9) ──────────────────
    #   계획된 P⁺ 잡을 **전부** 정상 판정했을 때만 방법 실패를 말할 수 있다.
    pc_planned = sorted(k for k in want if "/Pcation/" in k)
    pc_judged = {k: res["jobs"][k] for k in pc_planned
                 if k in res["jobs"] and not res["jobs"][k]["gates"]
                 and res["jobs"][k].get("class")}
    pc_bb = [k for k, v in pc_judged.items() if str(v["class"][0]).startswith("BACKBONE")]
    res["positive_control"] = {
        "n_planned": len(pc_planned), "n_judged": len(pc_judged),
        "n_backbone": len(pc_bb),
        "all_planned_judged": bool(pc_planned) and len(pc_judged) == len(pc_planned),
        "adequate": bool(pc_judged) and bool(pc_bb),
        "why": ("에너지 기준이 아니다 — 알려진 형태의 backbone radical cation 을 이 방법이 "
                "표현할 수 있는지만 본다 (회신 S Q4). ⛔ 결측·실패는 `NO_VALUE` 이지 "
                "`MODEL_NONDIAGNOSTIC` 이 아니다 (회신 U P0-9)")}
    if not res["positive_control"]["all_planned_judged"]:
        res["verdict"] = "NO_VALUE"
        res["why"] = ("계획된 positive control %d개 중 %d개만 정상 판정됐다 — "
                      "방법이 실패한 것인지 실행이 안 된 것인지 구분할 수 없다 "
                      "(회신 U P0-9)" % (len(pc_planned), len(pc_judged)))
        return res
    if not res["positive_control"]["adequate"]:
        res["verdict"] = "MODEL_NONDIAGNOSTIC"
        res["why"] = ("positive control(fully protonated cation) %d개를 **전부 정상 "
                      "판정했는데** backbone 상태를 하나도 회수하지 못했다 — "
                      "H-제거계 결과를 해석하지 않는다" % len(pc_judged))
        return res

    # ── ③ D• 상태 구분 능력 = S0 의 본 질문 (사전등록 합격 조건 ②) ─────────
    dm_env = sorted({v["env"] for k, v in res["jobs"].items() if "/Dradical/" in k})
    res["by_env"] = {}
    for env in dm_env:
        _bs = res["basins"].get("%s/Dradical" % env, {})
        _rows = [v for k, v in res["jobs"].items()
                 if "/Dradical/" in k and v["env"] == env and v["E_Eh"] is not None]
        res["by_env"][env] = {
            "n_jobs": len(_rows),
            "n_states": _bs.get("n_distinct"),
            "cluster_verdict": _bs.get("verdict"),
            # ⛔ 에너지는 **자료로만** 남긴다. S0 은 순서를 판정하지 않는다.
            "E_spread_eV": (round((max(r["E_Eh"] for r in _rows)
                                   - min(r["E_Eh"] for r in _rows)) * 27.2114, 4)
                            if _rows else None),
            "⛔_에너지_순서": ("S0 은 어느 상태가 낮은지 판정하지 않는다 — 환경 1·"
                              "범함수 1·conformer 1 이다 (사전등록 "
                              "⛔_통과해도_말할_수_없는_것)")}
    # ⛔ 회신 V Q6-1 — ε=1 음이온 기준계 부적합은 **방법 실패가 아니다.**
    #   문턱은 코드 상수로 결과 보기 전에 봉인돼 있다 (PIL_EPS1_*).
    res["eps1_anion_reference"] = {}
    for _jk, _jm in sorted(man["jobs"].items()):
        if _jm.get("phase") != "L2" or int(_jm.get("charge", 0)) >= 0:
            continue
        if abs(float(_jm.get("epsilon", 1.0)) - 1.0) > 1e-9:
            continue
        _lo = d / _jm["reads_localized_from"] / (
            _jm["reads_localized_from"].rsplit("/", 1)[-1] + ".out")
        _sg = _last_segment(_lo.read_text(errors="replace")) if _lo.is_file() else ""
        _ok_a, _code_a, _why_a = pil_eps1_anion_adequacy(
            _sg, _jm.get("epsilon"), _jm.get("charge"))
        res["eps1_anion_reference"][_jk] = {"code": _code_a, "why": _why_a}
        if not _ok_a:
            res["verdict"] = _code_a
            res["why"] = ("%s: %s — 이것은 **방법 실패가 아니라 기준계 부적합**이다 "
                          "(회신 U Q6 · V Q6-1). MODEL_NONDIAGNOSTIC 으로 부르지 않는다."
                          % (_jk, _why_a))
            return res
    _amb = [e for e, v in res["by_env"].items() if v["cluster_verdict"] == "CLUSTER_AMBIGUOUS"]
    if _amb:
        res["verdict"] = "SEARCH_PROTOCOL_DEPENDENT"
        res["why"] = ("basin 군집이 추이적이지 않아 상태 수를 셀 수 없다 (%s) — "
                      "문턱을 결과를 보고 고치지 않는다 (회신 U P0-8ⓐ)" % _amb)
        return res
    _ns = [v["n_states"] for v in res["by_env"].values() if v["n_states"] is not None]
    if not _ns:
        res["verdict"] = "NO_VALUE"
        res["why"] = "D• 군집을 만들 재료가 없다"
        return res
    if max(_ns) < 2:
        res["verdict"] = "MODEL_NONDIAGNOSTIC"
        res["why"] = ("게이트를 통과한 D• 실행이 basin 을 **하나만** 준다 — 방법이 "
                      "상태를 구분하지 못한 것인지 진짜로 하나인 것인지 S0 은 "
                      "가르지 못한다 (사전등록 합격 조건 ②). 함께 볼 것: "
                      "SEARCH_PROTOCOL_DEPENDENT")
        res["also"] = ["SEARCH_PROTOCOL_DEPENDENT"]
        return res

    res["verdict"] = "ADEQUATE"
    # ⛔ 회신 U 해제순서 ⑤ — R0/R1 **교차비교가 없으면 결과는 `R0-conditional`** 이다.
    #   한 realization 만 돌린 상태지도는 그 realization 에 조건부다 (회신 T Q2).
    _lr = man.get("loc_realization", "R0_deterministic")
    res["realization_scope"] = {
        "ran": _lr, "cross_compared": False,
        "scope": "R0-conditional" if _lr == "R0_deterministic" else "R1-conditional",
        "why": ("R0(결정론)과 R1(무작위)을 **둘 다** 돌려 같은 basin 집합을 확인하기 "
                "전에는 이 결과가 국재화 realization 에 조건부다. 두 realization 이 "
                "다른 집합을 주면 `LOCALIZATION_DEPENDENT` 다 (회신 U 해제순서 ⑤)")}
    res["허용_서술"] = (
        "이 프로토콜은 ε=1·%s·gs0 조건에서 서로 다른 전자상태를 **구분해 회수했다** "
        "(positive control 회수 %d건 · 게이트 통과 D• basin %d개). "
        "탐색 프로토콜과 국재화 realization(%s)에 조건부다."
        % (man.get("functional", "?"), len(pc_bb), max(_ns),
           res["realization_scope"]["scope"]))
    res["⛔_금지_서술"] = [
        "바닥상태 · 가장 안정한 상태 · 전역 최소 (S0 은 환경 1·범함수 1·conformer 1)",
        "SDCP 의 캐리어가 백본에 있다 / SO₃ 에 있다 (물질 수준 주장)",
        "seed 개수를 지지 증거의 개수로 쓰는 문장",
        "S0 결과를 고분자·실물·고체로 외삽하는 문장"]
    res["⛔"] = ("ADEQUATE 는 **방법이 상태를 구분한다**는 뜻이지 어느 상태가 실현된다는 "
                 "뜻이 아니다. 다음은 확장(범함수·환경) 단계다 (회신 U P0-6)")
    return res


PIL_RUNNER = r"""#!/usr/bin/env bash
# 폴라론 pilot 러너 — 단계를 **끊어서** 돈다 (회신 S · 2026-08-31 실측 반영).
#
#   bash run_pilot.sh loccheck  H2O 하나로 `%loc` 구문·suffix 확인 (30초) — **맨 먼저**
#   bash run_pilot.sh L        phase L  (SCF + Pipek-Mezey 국재화) — 여기서 멈춘다
#   bash run_pilot.sh L2       phase L2 (`.loc` 를 MORead, NoIter, 국재 궤도 인구)
#   bash run_pilot.sh seeds    L2 출력 판독 → phase S + 1층 probe 입력 생성 (계산 없음)
#   bash run_pilot.sh probe    1층 개입 확인 (`NoIter`, 싸다) — **phase S 앞에**
#   bash run_pilot.sh S        phase S  (측정) — **리뷰 통과 뒤에만**
#   bash run_pilot.sh analyze  판정 (4층)
#   bash run_pilot.sh restart  3층 재판정 — 불안정 잡을 따라 내려간 해로 다시
#
# ⛔ 회신 T Q4 — probe 를 S 앞에 두는 이유: 회전이 목표 자리에 스핀을 **안** 놓았으면
#    그 seed 는 다른 출발점이 아니다. 200원자 r2SCAN-3c 를 돌리기 전에 알아야 한다.
#
# ⛔ L2 가 왜 따로 있나 (2026-08-31 실측): phase L 이 찍는
#    `LOEWDIN ORBITAL POPULATIONS PER MO` 는 **정준 궤도**의 인구다
#    (출력 5883줄 · 국재화는 340994줄). 정준 궤도는 비편재라 "이 링에 걸린 MO" 를
#    거기서 고를 수 없다. 국재 궤도는 `<tag>.loc` 에 있고, L2 가 그것을 읽어
#    SCF 없이 인구만 다시 찍는다. seed 선택도 seed 입력도 그 `.loc` 를 쓴다.
# ⛔ 자동 연결(all)을 두지 않는다 — phase S 앞에 사람의 판단이 들어가야 한다.
set -u
stage=${1:?단계를 주세요: loccheck | L | L2 | seeds | probe | S | analyze | restart}
case "$stage" in loccheck|L|L2|seeds|probe|S|analyze|restart) ;;
  *) echo "모르는 단계: $stage"; exit 2;; esac
ORCA=${ORCA:?ORCA 절대경로를 주세요 (병렬은 full pathname 이 필요합니다)}
BUILDER=${BUILDER:?build_v7c_trimer.py 경로를 주세요}
BUILDER_PATH=$(cd "$(dirname "$BUILDER")" && pwd)/$(basename "$BUILDER")
D=$(cd "$(dirname "$0")" && pwd)
case "$ORCA" in /*) ;; *) echo "ORCA 는 절대경로여야 합니다: $ORCA"; exit 2;; esac
if head -c 64 "$ORCA" | grep -qa "python"; then
  echo "$ORCA 가 Python 스크립트입니다 — GNOME 스크린리더(orca)일 수 있습니다."
  echo "양자화학 ORCA 경로를 주세요."; exit 2
fi

# ⛔⛔ 회신 U P0-5 (2026-09-01) — **러너가 BUILDER 를 manifest 와 대조하지 않았다.**
#   이 묶음을 만든 빌더와 지금 seeds/analyze 를 돌리는 빌더가 다르면, 사전등록이
#   봉인한 규칙과 실제로 적용되는 규칙이 갈린다. 산출물만 봐서는 알 수 없다.
_bs=$(sha256sum "$BUILDER" | cut -d" " -f1)
_bm=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("builder_sha256") or "")' \
      "$D/MANIFEST_PILOT.json" 2>/dev/null || true)
if [ -z "$_bm" ]; then
  echo "⛔ MANIFEST_PILOT.json 에 builder_sha256 이 없습니다 — 구판 묶음입니다 (회신 U P0-5)"; exit 2
fi
if [ "$_bs" != "$_bm" ]; then
  echo "⛔ BUILDER 가 이 묶음을 만든 빌더와 다릅니다 (회신 U P0-5)."
  echo "   봉인 $_bm"
  echo "   현재 $_bs"
  echo "   같은 빌더로 돌리거나, 새 빌더로 묶음을 다시 만드십시오."
  exit 2
fi

LOCK="$D/.lock_$stage"
if ! mkdir "$LOCK" 2>/dev/null; then
  owner=$(cat "$LOCK/pid" 2>/dev/null || echo "?")
  if [ "$owner" != "?" ] && kill -0 "$owner" 2>/dev/null; then
    echo "이미 단계 '$stage' 가 돌고 있습니다 (pid $owner). 중복 실행을 막습니다."
    echo "  정말 다시 돌리려면: pkill -f run_pilot.sh; rm -rf $LOCK"
    exit 3
  fi
  echo "죽은 락을 치웁니다 (pid $owner 없음): $LOCK"
  rm -rf "$LOCK"; mkdir "$LOCK" || exit 3
fi
echo $$ > "$LOCK/pid"
trap 'rm -rf "$LOCK"' EXIT INT TERM

run() {
  local j=$1 tag=$2
  if [ -f "$j/$tag.out" ] && grep -aq "ORCA TERMINATED NORMALLY" "$j/$tag.out"; then
    echo "  이미 완료 — ${j#$D/}"; return 0; fi
  echo "  [$(date +%H:%M:%S)] ${j#$D/}"
  ( cd "$j" && "$ORCA" "$tag.inp" > "$tag.out" 2>&1 )
  if grep -aq "ORCA TERMINATED NORMALLY" "$j/$tag.out"; then
    echo "  [$(date +%H:%M:%S)] 정상 종료 — ${j#$D/}"; return 0; fi
  echo "  중단: ${j#$D/}  (마지막: $(tail -1 "$j/$tag.out" 2>/dev/null))"; return 1
}

pop_count() {   # 국재 궤도 인구 블록이 실제로 찍혔나 (헤더는 REDUCED 유무 둘 다)
  # ⛔ 회신 V P1 (2026-09-02) — `grep -c … || echo 0` 는 **false-green** 이다.
  #   grep -c 는 0건일 때 "0" 을 **찍고도** exit 1 이라, `|| echo 0` 이 하나 더 붙어
  #   출력이 `0\n0` 이 된다. 그 문자열을 수로 비교하면 `[ "0
0" != 0 ]` 이 참이라
  #   **0건이 통과**한다. (같은 함정을 run_sei_neb.sh 에서 이미 한 번 맞았다.)
  #   ⇒ 출력을 받고 첫 줄만 쓴다. 실패해도 빈 문자열이지 두 줄이 아니다.
  _n=$(grep -acE "LOEWDIN (REDUCED )?ORBITAL POPULATIONS PER MO" "$1" 2>/dev/null | head -1)
  printf '%s\n' "${_n:-0}"
}

fail=0
case "$stage" in
  loccheck)
    # ⛔⛔ 회신 U 해제순서 ⑥ (2026-09-01) — **작은 분자로 `%loc` 구문을 먼저 확인한다.**
    #   우리가 `Randomize 0` 이라는 **없는 키**를 세 판 동안 쓰고도 몰랐던 이유가
    #   이것이다: 200원자 잡이 정상 종료하면 `%loc` 가 무시됐는지 알 길이 없다.
    #   H₂O 하나면 30초다. 여기서 걸리면 phase L 을 돌릴 이유가 없다.
    echo "== %loc 구문 확인 (H2O · 30초) =="
    LC="$D/_loccheck"; mkdir -p "$LC"
    cat > "$LC/w.inp" <<'EOF'
! RKS BP86 def2-SVP TightSCF NoAutoStart
%loc
  LocMet PipekMezey
  Random 0
  OCC true
  VIRT false
  T_CORE -3.0
end
%output
  Print[P_OrbPopMO_L] 1
  Print[P_MOs] 1
end
* xyz 0 1
O   0.000000  0.000000  0.117300
H   0.000000  0.757200 -0.469200
H   0.000000 -0.757200 -0.469200
*
EOF
    ( cd "$LC" && "$ORCA" w.inp > w.out 2>&1 )
    grep -aq "ORCA TERMINATED NORMALLY" "$LC/w.out" \
      || { echo "  ⛔ ORCA 가 정상 종료하지 않았습니다 — %loc 블록을 의심하십시오"; \
           tail -25 "$LC/w.out"; fail=1; }
    # 알려지지 않은 키를 만나면 ORCA 는 경고/오류를 찍는다 — 그걸 잡는다
    if grep -aiE "unknown|unrecognized|not a valid|Error.*loc" "$LC/w.out" >/dev/null; then
      echo "  ⛔ %loc 키가 거부됐습니다:"; grep -aiE "unknown|unrecognized|not a valid|Error.*loc" "$LC/w.out" | head -5
      fail=1
    fi
    # 우리가 파싱해야 하는 두 블록이 실제로 찍혔나
    for _blk in "ORBITAL POPULATIONS PER MO" "MOLECULAR ORBITALS"; do
      if grep -aq "$_blk" "$LC/w.out"; then echo "  ✔ $_blk 있음"
      else echo "  ⛔ $_blk 없음 — 파서가 읽을 게 없습니다"; fail=1; fi
    done
    # ⛔ 회신 V P0-3 — `.loc` 인지 `.loc.gbw` 인지 **여기서 판정**한다.
    #   ORCA 6.1 문서는 `.loc.gbw` 로 설명하는데 우리 코드는 `.loc` 를 기대했다.
    _LSUF=""
    for _s in .loc .loc.gbw; do
      [ -f "$LC/w$_s" ] && { _LSUF="$_s"; break; }
    done
    if [ -n "$_LSUF" ]; then echo "  ✔ 국재 파일 suffix = $_LSUF  ($(ls -la "$LC/w$_LSUF" | awk '{print $5}') B)"
    else echo "  ⛔ 국재 궤도 파일이 안 나왔습니다 (.loc / .loc.gbw 둘 다 없음):"; ls -la "$LC"; fail=1; fi
    # ⛔ 우리 파서 **둘 다** 실물 출력에서 되는지 확인한다 (블록 존재만으로는 부족)
    _MPOP=false; _MMOS=false
    if [ "$fail" = 0 ]; then
      _PR=$(python3 - "$LC/w.out" "$BUILDER_PATH" <<'PYLC'
import json, sys, importlib.util
out, bp = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("_b", bp)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
t = open(out, encoding="utf-8", errors="replace").read()
pr = m.pil_parse_mopop(t, 3)
co = m.pil_parse_mos(t, 3)
print(json.dumps({"mopop": bool(pr), "mos": bool(co)}))
PYLC
) || _PR='{"mopop": false, "mos": false}'
      _MPOP=$(printf '%s' "$_PR" | python3 -c 'import json,sys;print(str(json.load(sys.stdin)["mopop"]).lower())')
      _MMOS=$(printf '%s' "$_PR" | python3 -c 'import json,sys;print(str(json.load(sys.stdin)["mos"]).lower())')
      [ "$_MPOP" = true ] && echo "  ✔ MO 인구 파서 PASS" || { echo "  ⛔ MO 인구 파서가 실물을 못 읽었습니다"; fail=1; }
      [ "$_MMOS" = true ] && echo "  ✔ MO 계수 파서 PASS" || { echo "  ⛔ MO 계수 파서가 실물을 못 읽었습니다"; fail=1; }
    fi
    if [ "$fail" = 0 ]; then
      python3 - "$D" "$ORCA" "$LC" "$_LSUF" "$_MPOP" "$_MMOS" <<'PYCERT'
import hashlib, json, os, subprocess, sys
d, orca, lc, suf, mp, mm = sys.argv[1:7]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
try:
    ver = subprocess.run([orca], capture_output=True, text=True, timeout=60).stdout
    ver = next((l.strip() for l in ver.splitlines() if "Program Version" in l), "?")
except Exception:
    ver = "?"
json.dump({
 "schema": "loccheck_pass/v1",
 "⛔_무엇을_보증하나": ("이 설치본에서 `%loc` 블록이 받아들여졌고, 국재 파일이 어느 "
                       "suffix 로 나오며, 우리 파서 둘이 그 출력을 실제로 읽는다는 것. "
                       "물리·수렴은 보증하지 않는다 (회신 V P0-3)"),
 "orca_path": os.path.abspath(orca), "orca_version": ver,
 "orca_sha256": h(orca) if os.path.isfile(orca) else None,
 "inp_sha256": h(os.path.join(lc, "w.inp")),
 "out_sha256": h(os.path.join(lc, "w.out")),
 "loc_suffix": suf,
 "loc_sha256": h(os.path.join(lc, "w" + suf)) if suf and os.path.isfile(os.path.join(lc, "w" + suf)) else None,
 "mopop_parsed": mp == "true", "mos_parsed": mm == "true",
}, open(os.path.join(d, "LOCCHECK_PASS.json"), "w"), indent=1, ensure_ascii=False)
print("  → LOCCHECK_PASS.json (suffix %s · 파서 인구=%s 계수=%s)" % (suf, mp, mm))
PYCERT
      echo "다음: bash run_pilot.sh L"
    else
      rm -f "$D/LOCCHECK_PASS.json"
      echo "⛔ %loc 계약이 실물과 다릅니다 — 200원자를 돌리지 마십시오."
      echo "   (증서를 만들지 않았으므로 L 단계가 거부합니다)"
    fi
    ;;
  L)
    # ⛔⛔ 회신 V P0-3 — **순서가 문구가 아니라 게이트여야 한다.**
    #   종전엔 loccheck 와 L 이 독립 case 라 L 이 loccheck PASS 를 요구하지 않았다.
    #   국재 파일 suffix(.loc vs .loc.gbw)조차 확정되지 않은 채 200원자 두 잡을
    #   여는 셈이었다.
    if [ ! -s "$D/LOCCHECK_PASS.json" ]; then
      echo "⛔ LOCCHECK_PASS.json 이 없습니다 — 먼저 `bash run_pilot.sh loccheck` 를"
      echo "   돌리십시오. H2O 하나로 30초입니다 (회신 V P0-3)."
      exit 2
    fi
    python3 - "$D" "$BUILDER_PATH" <<'PYLG' || exit 2
import importlib.util, sys
d, bp = sys.argv[1:3]
spec = importlib.util.spec_from_file_location("_b", bp)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
c, why = m.pil_read_loccheck(d)
if c is None:
    sys.exit("⛔ loccheck 증서가 유효하지 않습니다 — %s" % why)
print("  ✔ loccheck 증서 확인 (suffix %s · ORCA %s)"
      % (c["loc_suffix"], str(c.get("orca_version"))[:40]))
PYLG
    echo "== phase L (SCF + 국재화) =="
    for j in "$D"/L/*/*; do [ -d "$j" ] || continue; run "$j" "$(basename "$j")" || fail=1; done
    echo "== 국재화가 돌았나 =="
    for j in "$D"/L/*/*; do
      [ -d "$j" ] || continue; n=$(basename "$j")
      if [ -f "$j/$n.loc" ]; then echo "  ✔ $n.loc ($(stat -c%s "$j/$n.loc") B)"
      else echo "  ⛔ $n.loc 없음 — 국재화가 안 됐습니다"; fail=1; fi
    done
    [ "$fail" = 0 ] && echo "다음: bash run_pilot.sh L2" \
                   || echo "phase L 에 실패가 있습니다 — 다음 단계로 가지 않습니다."
    ;;
  L2)
    # ⛔ 회신 V P0-3 — 증서가 정한 suffix 로 `%moinp` 를 맞춘다 (생성 시점엔 몰랐다).
    python3 - "$D" "$BUILDER_PATH" <<'PYL2' || exit 2
import importlib.util, json, os, re, sys
d, bp = sys.argv[1:3]
spec = importlib.util.spec_from_file_location("_b", bp)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
c, why = m.pil_read_loccheck(d)
if c is None:
    sys.exit("⛔ loccheck 증서가 유효하지 않습니다 — %s" % why)
suf = c["loc_suffix"]
man_p = os.path.join(d, "MANIFEST_PILOT.json")
man = json.load(open(man_p))
old = man.get("loc_suffix_assumed") or ".loc"
n = 0
for jk, jm in man.get("jobs", {}).items():
    if jm.get("phase") != "L2":
        continue
    tag = jk.rsplit("/", 1)[-1]
    f = os.path.join(d, jk, tag + ".inp")
    if not os.path.isfile(f):
        continue
    t = open(f, encoding="utf-8").read()
    t2 = re.sub(r'(%moinp\s+")([^"]*?)' + re.escape(old) + r'(")',
                lambda mo: mo.group(1) + mo.group(2) + suf + mo.group(3), t)
    if t2 != t:
        open(f, "w", encoding="utf-8").write(t2); n += 1
man["loc_suffix_actual"] = suf
man["loc_suffix_patched_inputs"] = n
if n:
    man["⚠_loc_suffix_변경"] = (
        "loccheck 실측 suffix 가 %r 라 생성 시 가정 %r 과 달라 L2 입력 %d개의 "
        "`%%moinp` 를 고쳤다 (회신 V P0-3). 정본 대비 이 한 줄이 다르다." % (suf, old, n))
json.dump(man, open(man_p, "w"), indent=1, ensure_ascii=False)
print("  ✔ loc suffix = %s (L2 입력 %d개 수정%s)"
      % (suf, n, "" if n else " — 가정과 같아 손대지 않음"))
PYL2
    echo "== phase L2 (국재 궤도 인구 · NoIter) =="
    for j in "$D"/L2/*/*; do [ -d "$j" ] || continue; run "$j" "$(basename "$j")" || fail=1; done
    echo "== smoke test — 국재 궤도의 MO 인구가 찍혔나 =="
    for j in "$D"/L2/*/*; do
      [ -d "$j" ] || continue; n=$(basename "$j"); c=$(pop_count "$j/$n.out")
      echo "  $n: 인구 블록 $c"
      [ "$c" != 0 ] || { echo "    0 입니다 — NoIter 에서 인구가 안 찍혔습니다."; fail=1; }
    done
    [ "$fail" = 0 ] && echo "다음: bash run_pilot.sh seeds  (계산 없음)" \
                   || echo "phase L2 에 실패가 있습니다 — 다음 단계로 가지 않습니다."
    ;;
  seeds)
    if python3 "$BUILDER" --polaron_seeds "$D"; then
      echo "다음: bash run_pilot.sh probe  (1층 개입 확인 · 싸다)"
    else
      echo "seed 생성 실패 — 다음 단계로 가지 않습니다."; fail=1
    fi
    ;;
  probe)
    echo "== 1층 개입 확인 probe (NoIter · 회신 T Q4) =="
    for j in "$D"/S0P/*/*/*; do
      [ -d "$j" ] || continue; run "$j" "$(basename "$j")_probe" || fail=1; done
    [ "$fail" = 0 ] && echo "다음: **리뷰 통과 뒤** bash run_pilot.sh S" \
                   || echo "probe 에 실패가 있습니다 — phase S 로 가지 않습니다."
    ;;
  S)
    echo "== phase S (측정) =="
    for j in "$D"/S/*/*/*; do [ -d "$j" ] || continue; run "$j" "$(basename "$j")" || fail=1; done
    [ "$fail" = 0 ] && echo "다음: bash run_pilot.sh analyze" \
                   || echo "phase S 에 실패가 있습니다 — 판정하지 않습니다."
    ;;
  analyze)
    python3 "$BUILDER" --polaron_analyze "$D" || fail=1
    ;;
  restart)
    # 3층 — 불안정 잡을 따라 내려간 `.gbw` 로 재계산하고 안정성을 다시 본다
    python3 "$BUILDER" --polaron_restart "$D" || { fail=1; echo "재판정 입력 생성 실패"; }
    for j in "$D"/SR/*/*/*; do [ -d "$j" ] || continue; run "$j" "$(basename "$j")" || fail=1; done
    [ "$fail" = 0 ] && echo "다음: bash run_pilot.sh analyze (3층 재판정 반영)"
    ;;
esac
exit $fail
"""




def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dimer")
    ap.add_argument("--out")
    ap.add_argument("--cc", type=float, default=CC_NEW)
    ap.add_argument("--step", type=int, default=10, help="비틀림각 스캔 간격(도) — seed 아님")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--stage", choices=["a", "b"])
    ap.add_argument("--seeds", type=int, default=None,
                    help="stage a geometry seed 수 (기본·최소 = SEED_FLOOR)")
    ap.add_argument("--stage_a_manifest", help="stage b: stage A 의 manifest_stage_a.json")
    ap.add_argument("--neutral_out", help="stage b: 중성 Opt 의 ORCA .out (receipt 검증)")
    ap.add_argument("--neutral_xyz", help="stage b: ORCA Opt 최종 xyz")
    ap.add_argument("--gseed", type=int, default=0)
    ap.add_argument("--scf_seeds", type=int, default=2)
    ap.add_argument("--patterns", action="append")
    ap.add_argument("--allow_partial", action="store_true",
                    help="시험 전용 — 재심사 제출물 금지")
    ap.add_argument("--allow_noncanonical", action="store_true", help="selftest 전용")
    ap.add_argument("--allow_underseed", action="store_true", help="selftest 전용")
    ap.add_argument("--allow_unverified_parent", action="store_true", help="selftest 전용")
    ap.add_argument("--analyze", help="stage b 디렉터리 — 게이트 + abort code emit")
    ap.add_argument("--hybrid", help="분석 완료된 stage b 디렉터리 — decision set 입력 생성")
    ap.add_argument("--compare", nargs=2, help="두 분석 디렉터리 — METHOD_DEPENDENT 검사")
    ap.add_argument("--legacy", action="store_true",
                    help="레거시 트라이머 패키지 (명시 필수 — R3 P1)")
    ap.add_argument("--selftest", action="store_true")
    # ── 폴라론 pilot (회신 S) — 흡착 doped 와 **다른 캠페인**이다 ──────────
    ap.add_argument("--polaron_pilot", action="store_true",
                    help="H-제거 라디칼 상태지도 pilot 생성 (+ --neutral_xyz/--out)")
    ap.add_argument("--polaron_seeds", help="phase L 완주 디렉터리 — seed 선택 + phase S 생성")
    ap.add_argument("--polaron_restart", help="3층 재판정 입력 생성 (불안정 잡)")
    ap.add_argument("--polaron_analyze", help="phase S 완주 디렉터리 — F 집합·class·판정")
    ap.add_argument("--site", help="H 제거 위치 (1-based 산성 H). 생략하면 사전 규칙(중간)")
    # ⛔ 회신 T P0-3 — 국재화 realization. primary 는 결정론이 기본이다.
    ap.add_argument("--loc_realization", choices=("deterministic", "random"),
                    default="deterministic",
                    help="국재화 realization. deterministic=%%loc Random 0 (primary·기본) · "
                         "random=무작위 seed (민감도 R1 — 명시했을 때만 허용)")
    ap.add_argument("--eps", nargs="+", type=float, default=None,
                    help="유전상수 목록 (예: 1.0 4.0). 사전등록에 근거를 적을 것")
    ap.add_argument("--functional", default="r2SCAN-3c")
    ap.add_argument("--maxcore", type=int, default=PIL_MAXCORE_MB,
                    help="ORCA %%maxcore — **proc 당** MB (총 요청 = nprocs × 이 값)")
    ap.add_argument("--nprocs", type=int, default=1,
                    help="ORCA %pal nprocs. 1 이면 직렬 — 200원자 SP 는 사실상 안 끝난다")
    ap.add_argument("--eps_why",
                    help="ε=1 이 아닌 환경의 **근거**. 사전등록 항목이라 생략하면 거부한다")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.polaron_pilot:
        if not (a.neutral_xyz and a.out):
            ap.error("--polaron_pilot 은 --neutral_xyz/--out 필요")
        if not a.eps:
            ap.error("--eps 를 명시하세요 (예: --eps 1.0 4.0). "
                     "환경은 사전등록 항목이라 기본값을 두지 않습니다")
        # ⛔ 사전등록(db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json)이
        #   dry-polymer ε 을 "⏳ 값 미정 — litdb 근거 필요" 로 박아 놨다.
        #   근거 없이 값을 넣으면 **우리 사전등록을 우리가 어기는 것**이다.
        if any(abs(e - 1.0) > 1e-9 for e in a.eps) and not a.eps_why:
            ap.error("ε≠1 환경을 쓰려면 --eps_why 로 근거를 적으세요.\n"
                     "  사전등록이 'dry-polymer ε — 값 미정, litdb 근거 필요' 로 "
                     "박혀 있습니다.\n"
                     "  근거가 아직 없으면 --eps 1.0 만으로 시작하세요 "
                     "(vacuum control 은 사전등록에 이미 있습니다).")
        if a.nprocs <= 1:
            print("⚠ --nprocs 1 (직렬) — 200원자 r2SCAN-3c SP 는 사실상 끝나지 않습니다. "
                  "가용 코어를 주세요 (예: --nprocs 8)")
        pilot_generate(a)
        return 0
    if a.polaron_seeds:
        return 0 if pilot_seeds(a.polaron_seeds) else 2
    if a.polaron_restart:
        pilot_restart(a.polaron_restart)
        return 0
    if a.polaron_analyze:
        r = pilot_analyze(a.polaron_analyze)
        print(json.dumps(r, indent=1, ensure_ascii=False))
        out = Path(a.polaron_analyze) / "PILOT_RESULT.json"
        out.write_text(json.dumps(r, indent=1, ensure_ascii=False))
        print("→ %s" % out)
        return 0 if r.get("verdict") not in (None, "NO_VALUE") else 2
    if a.analyze:
        return analyze_dir(a)
    if a.hybrid:
        hybrid_stage(a)
        return 0
    if a.compare:
        return compare_methods(a)
    if a.stage == "a":
        if not (a.dimer and a.out):
            ap.error("--stage a 는 --dimer/--out 필요")
        sym, pos = read_xyz(a.dimer)
        stage_a(a, sym, pos)
        return 0
    if a.stage == "b":
        if not (a.neutral_xyz and a.out):
            ap.error("--stage b 는 --neutral_xyz/--out 필요 (+ --stage_a_manifest/--neutral_out)")
        stage_b(a)
        return 0
    if a.legacy:
        if not (a.dimer and a.out):
            ap.error("--legacy 는 --dimer/--out 필요")
        sym, pos = read_xyz(a.dimer)
        build_legacy_trimer(a, sym, pos)
        return 0
    ap.error("--stage a|b · --analyze · --hybrid · --compare · --legacy · "
             "--polaron_pilot/--polaron_seeds/--polaron_restart/--polaron_analyze · "
             "--selftest 중 하나")


if __name__ == "__main__":
    raise SystemExit(main())
