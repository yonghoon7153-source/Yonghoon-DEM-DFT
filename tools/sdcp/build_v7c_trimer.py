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
    """
    blocks = seg.split(header)
    if len(blocks) < 2:
        return None
    got = {}
    for ln in blocks[-1].splitlines()[1:]:
        m = re.match(r"\s*(\d+)\s+[A-Za-z]{1,2}\s*:\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)", ln)
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

    print(f"── {'PASS' if not fails else 'FAIL ' + str(len(fails))} ──")
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
    _mo, _w = pil_pick_seed_mo(_pops, _occ, _am["rings"]["ring0"])
    chk(_mo == 10 and _w > 80.0, f"pilot: 목표 집합에 크게 걸린 MO 를 고른다 (mo {_mo}, {_w:.0f}%)")
    _mo2, _w2 = pil_pick_seed_mo({11: {0: 5.0}}, {11: 2.0}, _am["rings"]["ring0"])
    chk(_mo2 is None,
        "⛔음성 S Q2: 목표 집합에 문턱(40%) 미만인 MO 밖에 없으면 **seed 를 만들지 않는다** "
        "(국재화 실패를 임의 선택으로 덮지 않는다)")
    _mo3, _ = pil_pick_seed_mo({10: {i: 99.0 for i in _am["rings"]["ring0"]}},
                               {10: 0.0}, _am["rings"]["ring0"])
    chk(_mo3 is None, "⛔음성: **비점유** MO 는 seed 후보가 아니다")
    chk(pil_parse_mopop("아무 관계 없는 출력", 10) is None,
        "⛔음성: MO 인구 블록이 없으면 None (임의로 고르지 않는다)")
    print("── 폴라론 pilot 끝 ──")
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


def pilot_acidic_h(csym, cnb, csulf):
    """산성 H (SO₃H 의 H) 를 0-based 로. → [(sulf_idx, S, O, H), ...]"""
    out = []
    for k, su in enumerate(csulf):
        if su.get("aH") is not None:
            o = next((o for o in su["sO"] if su["aH"] in cnb[o]), None)
            out.append((k, su["sS"], o, su["aH"]))
    return out


# ── 폴라론 pilot · 생성 ─────────────────────────────────────────────────────

PIL_LOC_KW = "%loc\n  LocMet PipekMezey\n  T_Core -1e6\nend\n"
#: MO 별 Löwdin 인구를 찍게 한다 — seed 선택의 **유일한** 근거다.
PIL_MOPOP_KW = "%output\n  Print[P_OrbPopMO_L] 1\nend\n"


def _pil_cpcm(eps):
    """ε=1 이면 진공(블록 없음), 아니면 CPCM. cavity 규약을 manifest 에 기록한다."""
    if eps is None or abs(eps - 1.0) < 1e-9:
        return ""
    return "%%cpcm\n  epsilon %.4f\n  refrac 1.4000\nend\n" % eps


def _pil_inp(path, xyz, charge, mult, wf, eps, functional,
             loc=False, moread=None, rotate=None, stab=False, nprocs=1):
    """pilot 용 ORCA 입력. 관측량 계약(Hirshfeld · open-shell 에 UNO UCO)을 강제한다.

    ⚠ `NoAutoStart` 는 **항상** 켠다 — 같은 basename 의 GBW 를 우연히 물지 않게.
      의도한 lineage 는 `MOInp`/`MORead` 로만 들어온다 (회신 S Q8 게이트: 둘을 구분).
    """
    obs = " Hirshfeld" + ("" if wf == "RKS" else " UNO UCO")
    kw = "! %s %s TightSCF NoAutoStart%s" % (wf, functional, obs)
    body = [kw, "%maxcore 6000"]
    # ⛔ 2026-08-31 — `%pal` 이 없으면 ORCA 는 **직렬**로 돈다. 200원자 r2SCAN-3c SP 를
    #   1코어로 돌리면 pilot 이 끝나지 않는다. (병렬 실행은 ORCA 를 **절대경로**로
    #   불러야 한다 — 2026-08-31 stage A 에서 rc=126 으로 실측한 사고다.)
    if nprocs and nprocs > 1:
        body.append("%%pal nprocs %d end" % nprocs)
    scf = []
    if moread:
        body.append('%%moinp "%s"' % moread)
        scf.append("Guess MORead")
    if rotate:
        # {from, to, angle, spin_from, spin_to} — 선택한 국재 MO 를 HOMO 자리로
        scf.append("Rotate {%d, %d, 90, 0, 0} end" % (rotate[0], rotate[1]))
    if stab:
        scf.append("StabPerform true")
    if scf:
        body.append("%scf " + " ".join(scf) + " end")
    txt = "\n".join(body) + "\n"
    if loc:
        txt += PIL_LOC_KW + PIL_MOPOP_KW
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
    envs = [("eps%g" % e, e) for e in (a.eps or [1.0])]
    man = {
        "schema": "polaron_pilot/v1",
        "date": time.strftime("%Y-%m-%d"),
        "prereg": "db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json",
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
        "atom_map": amap,
        "atom_map_no_ether": amap_alt,
        "backbone_정의": ("primary = 티오펜 고리 + **고리 C 에 직결된 에테르 O** + 고리 H. "
                          "EDOT 의 3,4-O 는 π 에 전자를 밀어넣는 자리라 폴라론 밀도를 갖는다. "
                          "sp³ -CH2CH2- 다리는 공액이 아니므로 other. "
                          "⚠ 분석기가 ether 제외 값도 **같이** 보고한다 — class 가 갈리면 "
                          "BACKBONE_DEFINITION_DEPENDENT (억지 선택 금지)"),
        "functional": a.functional,
        "nprocs": int(a.nprocs),
        "eps_basis": a.eps_why,
        "environments": {n: {"epsilon": e,
                             "cpcm": ("vacuum (블록 없음)" if abs(e - 1.0) < 1e-9
                                      else "CPCM epsilon=%.4f refrac=1.4000" % e)}
                         for n, e in envs},
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
                     a.functional, loc=True, nprocs=a.nprocs)
            man["jobs"]["L/%s/%s" % (en, tag)] = {
                "phase": "L", "env": en, "epsilon": ev, "charge": ch, "mult": mult,
                "wf": "RKS", "roles": roles,
                "n_electrons": electrons_of(csym2) - ch,
                "inp_sha256": _sha(jd / (tag + ".inp")),
                "xyz_sha256": _sha(jd / (tag + ".xyz")),
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
    man["census"] = {
        "seed_generation_SP": len(envs) * 2,
        "measured_SP_예정": n_meas,
        "note": ("측정 SP = D• %d + P⁺ %d + D⁻ 기준 1, 환경 %d개. D⁻ 기준은 L_dminus 와 "
                 "**같은 계산**이라 따로 돌지 않는다"
                 % (len(man["seed_plan"]["Dradical"]["seeds"]),
                    len(man["seed_plan"]["Pcation"]["seeds"]), len(envs))),
    }
    (out / "MANIFEST_PILOT.json").write_text(
        json.dumps(man, indent=1, ensure_ascii=False))
    (out / "run_pilot.sh").write_text(PIL_RUNNER)
    print("→ %s · phase L %d잡 (환경 %d) · 측정 SP 예정 %d"
          % (out, len(man["jobs"]), len(envs), n_meas))
    print("   제거 H = 1-based %d (%s) · 산성 H 후보 %s"
          % (sH + 1, why_site, man["acidic_H_1based_all"]))
    print("   집합 hash %s · backbone %d · sulfonate %d · other %d"
          % (amap["hash"][:16], len(amap["sets"]["backbone"]),
             len(amap["sets"]["sulfonate"]), len(amap["sets"]["other"])))
    return out


# ── 폴라론 pilot · phase L 판독 + seed 생성 ────────────────────────────────

PIL_MOPOP_HDR = "LOEWDIN REDUCED ORBITAL POPULATIONS PER MO"
PIL_SEED_MIN_WEIGHT = 40.0   # % — 목표 집합에 이만큼도 안 걸린 MO 는 국재 seed 가 아니다


def pil_parse_mopop(text, nat):
    """`LOEWDIN REDUCED ORBITAL POPULATIONS PER MO` → (pops, occ, ener) 또는 None.

    pops[mo][atom] = 백분율 합. ORCA 는 MO 를 **열**로 청크 인쇄한다.

    ⛔ 못 하는 것: 인쇄 threshold(기본 0.1%) 아래는 안 찍히므로 합이 100 이 안 될 수
      있다. 그래서 절대 백분율이 아니라 **집합 간 상대 크기**로만 쓴다.
    ⚠ ORCA 실제 출력으로 검증하지 않았다 (smoke test 필요).
    """
    if PIL_MOPOP_HDR not in text:
        return None
    seg = text.split(PIL_MOPOP_HDR)[-1]
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
        m2 = re.match(r"\s*(\d+)\s+[A-Za-z]{1,2}\s+\S+\s+(.*)$", ln)
        if m2 and cur:
            ai = int(m2.group(1))
            vals = m2.group(2).split()
            if len(vals) == len(cur):
                for mo, v in zip(cur, vals):
                    try:
                        pops[mo][ai] = pops[mo].get(ai, 0.0) + float(v)
                    except ValueError:
                        pass
        i += 1
    if not pops:
        return None
    if max(max(d) for d in pops.values() if d) >= nat:
        return None                          # 원자 index 가 범위를 넘었다 — 판독 실패
    return pops, occ, ener


def pil_pick_seed_mo(pops, occ, group_idx, kill=None):
    """목표 집합에 가장 크게 걸린 **점유** MO. → (mo, weight_pct) 또는 (None, best)."""
    kill = set(kill or [])

    def remap(i):                            # 중성 프레임 → H 제거 프레임
        return None if i in kill else i - sum(1 for k in kill if k < i)

    tgt = {remap(i) for i in group_idx}
    tgt.discard(None)
    best, bw = None, -1.0
    for mo, d in pops.items():
        if occ.get(mo, 0.0) < 1.0:
            continue                         # 점유 MO 만
        w = sum(v for a, v in d.items() if a in tgt)
        if w > bw:
            best, bw = mo, w
    if bw < PIL_SEED_MIN_WEIGHT:
        return None, bw
    return best, bw


def pilot_seeds(d):
    """phase L 출력을 읽고 phase S 입력을 만든다. 하나라도 못 만들면 **멈춘다**."""
    d = Path(d)
    man = json.loads((d / "MANIFEST_PILOT.json").read_text())
    amap = man["atom_map"]
    kill = [man["removed_H_0based"]]
    nat = man["n_atoms"]
    made, report = 0, {}
    for jk, jm in sorted(man["jobs"].items()):
        if jm["phase"] != "L":
            continue
        jd = d / jk
        tag = jk.rsplit("/", 1)[-1]
        outp = jd / (tag + ".out")
        if not outp.is_file():
            raise SystemExit("⛔ %s 가 없다 — phase L 을 먼저 완주시킬 것" % outp)
        txt = outp.read_text(errors="replace")
        if "ORCA TERMINATED NORMALLY" not in txt:
            raise SystemExit("⛔ %s 가 정상 종료하지 않았다" % outp)
        is_dm = tag == "L_dminus"
        nat_j = nat - (1 if is_dm else 0)
        pr = pil_parse_mopop(txt, nat_j)
        if pr is None:
            raise SystemExit(
                "⛔ %s 에서 MO 별 Löwdin 인구를 못 읽었다 — `%%output Print[P_OrbPopMO_L] 1` "
                "이 실제로 찍혔는지 확인할 것 (seed 를 임의로 고르지 않는다)" % outp)
        pops, occ, _ = pr
        nel = jm["n_electrons"]
        homo = nel // 2 - 1
        spec = man["seed_plan"]["Dradical" if is_dm else "Pcation"]
        env = jm["env"]
        for sd in spec["seeds"]:
            sdir = d / "S" / env / ("Dradical" if is_dm else "Pcation") / sd
            sdir.mkdir(parents=True, exist_ok=True)
            src_xyz = jd / (tag + ".xyz")
            xyzn = "%s.xyz" % sd
            (sdir / xyzn).write_text(src_xyz.read_text())
            rot, w = None, None
            if sd != "default":
                gi = (amap["sets"]["sulfonate"] if sd == "A_sulfonate"
                      else amap["rings"][sd.replace("B_", "")])
                mo, w = pil_pick_seed_mo(pops, occ, gi, kill if is_dm else None)
                if mo is None:
                    raise SystemExit(
                        "⛔ %s/%s: 목표 집합에 %.1f%% 밖에 안 걸린 MO 가 최대다 "
                        "(문턱 %.0f%%). **국재 seed 가 아니므로 만들지 않는다** — "
                        "국재화가 실패했다는 뜻이다 (MODEL_NONDIAGNOSTIC 후보)"
                        % (env, sd, w, PIL_SEED_MIN_WEIGHT))
                rot = (mo, homo)
            gbw = os.path.relpath(jd / (tag + ".gbw"), sdir)
            _pil_inp(sdir / (sd + ".inp"), xyzn, spec["charge"], spec["mult"],
                     spec["wf"], jm["epsilon"], man["functional"],
                     moread=(None if sd == "default" else gbw),
                     rotate=rot, stab=True, nprocs=man.get("nprocs", 1))
            man["jobs"]["S/%s/%s/%s" % (env, "Dradical" if is_dm else "Pcation", sd)] = {
                "phase": "S", "env": env, "epsilon": jm["epsilon"],
                "charge": spec["charge"], "mult": spec["mult"], "wf": spec["wf"],
                "seed": sd, "seed_source": jk,
                "seed_mo": (None if rot is None else rot[0]),
                "seed_mo_weight_pct": (None if w is None else round(w, 2)),
                "homo_index": homo,
                "roles": ["measured"],
                "inp_sha256": _sha(sdir / (sd + ".inp")),
                "xyz_sha256": _sha(sdir / (xyzn)),
            }
            report.setdefault(env, []).append(
                "%s/%s mo=%s w=%s" % ("D•" if is_dm else "P⁺", sd,
                                      rot[0] if rot else "-",
                                      ("%.1f%%" % w) if w is not None else "-"))
            made += 1
    man["seeds_made"] = made
    man["seeds_made_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (d / "MANIFEST_PILOT.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print("→ phase S 입력 %d개" % made)
    for env, rows in sorted(report.items()):
        print("  [%s] %s" % (env, " · ".join(rows)))
    return made


# ── 폴라론 pilot · 분석 ─────────────────────────────────────────────────────

def pilot_analyze(d):
    """phase S 결과 → F 집합 · class · 민감도 · 종료 규칙. 전부 fail-closed."""
    d = Path(d)
    man = json.loads((d / "MANIFEST_PILOT.json").read_text())
    amap = man["atom_map"]
    kill = [man["removed_H_0based"]]
    res = {"schema": "polaron_pilot_result/v1",
           "prereg": man["prereg"], "decision": man["decision"],
           "atom_map_hash": amap["hash"], "blocks": [], "jobs": {}, "verdict": None}

    amap_alt = man.get("atom_map_no_ether")

    def remap_sets(is_dm, mp=None):
        """중성 프레임 집합 → 그 계의 프레임. D•/D⁻ 만 H 하나가 빠진다."""
        mp = mp or amap
        if not is_dm:
            return {"sets": mp["sets"], "rings": mp["rings"]}
        k = set(kill)

        def rm(i):
            return None if i in k else i - sum(1 for x in k if x < i)
        f = lambda L: sorted(x for x in (rm(i) for i in L) if x is not None)
        return {"sets": {g: f(v) for g, v in mp["sets"].items()},
                "rings": {g: f(v) for g, v in mp["rings"].items()}}

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
        seg = _last_segment(txt)
        if "ORCA TERMINATED NORMALLY" not in txt:
            r["gates"].append("NOT_TERMINATED")
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
        if "StabPerform" in (jd / (tag + ".inp")).read_text():
            if re.search(r"(?i)wavefunction is unstable|instabilit", seg):
                r["gates"].append("SCF_UNSTABLE(따라 내려간 해로 재계산 필요)")
            elif not re.search(r"(?i)stability analysis", seg):
                r["gates"].append("STABILITY_NOT_RUN(요청했는데 수행 흔적이 없다)")
        is_dm = "/Dradical/" in jk
        sm = remap_sets(is_dm)
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
            # ⛔ backbone 정의(에테르 O 포함 여부)도 estimand 를 움직인다 — 둘 다 낸다
            if amap_alt:
                sm2 = remap_sets(is_dm, amap_alt)
                sh2 = pilot_shares(hir, sm2)
                r["hirshfeld_no_ether"] = {"F": sh2.get("F"),
                                           "class": pilot_class(sh2.get("F"))
                                           if sh2.get("F") else None}
                c1 = (r.get("class") or (None,))[0]
                c2 = (r["hirshfeld_no_ether"]["class"] or (None,))[0]
                if c1 != c2:
                    r["gates"].append(
                        "BACKBONE_DEFINITION_DEPENDENT(에테르 O 포함 %s / 제외 %s — "
                        "억지로 하나를 고르지 않는다)" % (c1, c2))
        m_e = re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+\.\d+)", seg)
        r["E_Eh"] = float(m_e[-1]) if m_e else None
        if r["E_Eh"] is None:
            r["gates"].append("NO_ENERGY")
        res["jobs"][jk] = r

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

    # ── positive control adequacy (회신 S Q4) ─────────────────────────────
    pc = {k: v for k, v in res["jobs"].items()
          if "/Pcation/" in k and not v["gates"] and v.get("class")}
    pc_bb = [k for k, v in pc.items() if str(v["class"][0]).startswith("BACKBONE")]
    res["positive_control"] = {
        "n_ok": len(pc), "n_backbone": len(pc_bb),
        "adequate": bool(pc) and bool(pc_bb),
        "why": ("에너지 기준이 아니다 — 알려진 형태의 backbone radical cation 을 이 방법이 "
                "표현할 수 있는지만 본다 (회신 S Q4)")}
    if not res["positive_control"]["adequate"]:
        res["verdict"] = "MODEL_NONDIAGNOSTIC"
        res["why"] = ("positive control(fully protonated cation)이 backbone 상태를 "
                      "하나도 회수하지 못했다 — H-제거계 결과를 해석하지 않는다")
        return res
    if res["blocks"]:
        res["verdict"] = "NO_VALUE"
        res["why"] = "blocks 를 해소하기 전에는 판정하지 않는다"
        return res

    # ── A/B 분기와 환경 의존 (회신 S Q3) ──────────────────────────────────
    dm = {k: v for k, v in res["jobs"].items() if "/Dradical/" in k}
    by_env = {}
    for k, v in dm.items():
        by_env.setdefault(v["env"], []).append((v["E_Eh"], k, v))
    order = {}
    for env, rows in by_env.items():
        rows = [r for r in rows if r[0] is not None]
        if not rows:
            continue
        rows.sort()
        lo = rows[0]
        order[env] = {"lowest": lo[1], "class": lo[2].get("class"),
                      "F": (lo[2].get("hirshfeld") or {}).get("F"),
                      "N_eff": (lo[2].get("hirshfeld") or {}).get("N_eff"),
                      "span80": (lo[2].get("hirshfeld") or {}).get("span80"),
                      "n_states": len(rows),
                      "E_spread_eV": round((rows[-1][0] - rows[0][0]) * 27.2114, 4)}
    res["by_env"] = order
    cls = {e: (v["class"][0] if v.get("class") else None) for e, v in order.items()}
    res["class_by_env"] = cls
    if len(set(c for c in cls.values() if c)) > 1:
        res["verdict"] = "ENVIRONMENT_DEPENDENT"
        res["why"] = "plausible ε 범위에서 최저해의 class 가 갈린다 %s" % cls
        return res
    c0 = next((c for c in cls.values() if c), None)
    res["verdict"] = ("BACKBONE_SUPPORTED" if c0 == "BACKBONE" else
                      "SO3_CENTERED_WITHIN_MODEL" if c0 == "SULFONATE" else
                      "MIXED_UNRESOLVED" if c0 else "NO_VALUE")
    res["허용_서술"] = (
        "검사한 n=6 H-제거 분자모형에서는 **탐색된 최저상태**가 %s 였다"
        % {"BACKBONE_SUPPORTED": "백본 중심",
           "SO3_CENTERED_WITHIN_MODEL": "SO₃ 중심"}.get(res["verdict"], "판정 불가"))
    res["⛔"] = ("이 판정은 **한 범함수·한 conformer·한 H 위치**에 조건부다. "
                 "다른 범함수가 순서나 class 를 달리하면 FUNCTIONAL_DEPENDENT 로 닫는다. "
                 "고체·전도도·이동도를 말하지 않는다")
    return res


PIL_RUNNER = r"""#!/usr/bin/env bash
# 폴라론 pilot 러너 — 순서를 강제한다 (회신 S).
#   phase L(seed 생성원) → seed 선택 → phase S(측정) → 분석
# ⛔ seed 는 phase L **결과**에 의존한다. 순서를 건너뛰면 임의 MO 를 고르는 것이다.
set -u
ORCA=${ORCA:?ORCA 절대경로를 주세요 (병렬 실행은 full pathname 이 필요합니다)}
BUILDER=${BUILDER:?build_v7c_trimer.py 경로를 주세요}
D=$(cd "$(dirname "$0")" && pwd)
run() {
  local j=$1 tag=$2
  if [ -f "$j/$tag.out" ] && grep -aq "ORCA TERMINATED NORMALLY" "$j/$tag.out"; then
    echo "  이미 완료 — $j"; return 0; fi
  echo "  ▶ $j"
  ( cd "$j" && "$ORCA" "$tag.inp" > "$tag.out" 2>&1 )
  grep -aq "ORCA TERMINATED NORMALLY" "$j/$tag.out" || { echo "  중단: $j"; return 1; }
}
echo "== phase L =="
fail=0
for j in "$D"/L/*/*; do
  [ -d "$j" ] || continue
  run "$j" "$(basename "$j")" || fail=1
done
[ "$fail" = 0 ] || { echo "phase L 실패 — seed 를 만들지 않는다"; exit 2; }
echo "== seed 선택 =="
python3 "$BUILDER" --polaron_seeds "$D" || { echo "seed 생성 실패"; exit 2; }
echo "== phase S =="
for j in "$D"/S/*/*/*; do
  [ -d "$j" ] || continue
  run "$j" "$(basename "$j")" || fail=1
done
echo "== 분석 =="
python3 "$BUILDER" --polaron_analyze "$D"
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
    ap.add_argument("--polaron_analyze", help="phase S 완주 디렉터리 — F 집합·class·판정")
    ap.add_argument("--site", help="H 제거 위치 (1-based 산성 H). 생략하면 사전 규칙(중간)")
    ap.add_argument("--eps", nargs="+", type=float, default=None,
                    help="유전상수 목록 (예: 1.0 4.0). 사전등록에 근거를 적을 것")
    ap.add_argument("--functional", default="r2SCAN-3c")
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
             "--polaron_pilot/--polaron_seeds/--polaron_analyze · --selftest 중 하나")


if __name__ == "__main__":
    raise SystemExit(main())
