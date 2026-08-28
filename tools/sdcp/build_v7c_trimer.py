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
        except SystemExit:
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
def neutral_receipt(a, manA):
    """stage A manifest + ORCA .out + 최종 xyz 를 **묶어서** 검증한다.

    검증: ① manifest 의 gseed 항목 존재 ② .out strict decode · 마지막 run segment 의
    정상종료 + **Opt 수렴** ③ .out 마지막 좌표블록 == neutral_xyz 좌표 (원자별 1e-5 Å)
    ④ neutral_xyz 가 stage A 의 미이완 xyz 와 **달라야** 한다 (동일 = 미이완 재사용 적발)
    ⑤ 조성·닫힌꼴 → receipt(해시·최종에너지·버전·calc id) 반환. 하나라도 어기면 중단.
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
    csym, cpos = read_xyz(a.neutral_xyz)
    blocks = seg.split("CARTESIAN COORDINATES (ANGSTROEM)")
    if len(blocks) < 2:
        raise SystemExit("⛔ neutral .out: 좌표 블록 없음 — xyz 와 결합 불가")
    last = blocks[-1].splitlines()[2:2 + len(csym)]
    ocoords = []
    for ln in last:
        t = ln.split()
        if len(t) >= 4:
            ocoords.append((t[0], float(t[1]), float(t[2]), float(t[3])))
    if len(ocoords) != len(csym):
        raise SystemExit(f"⛔ .out 좌표 {len(ocoords)}원자 ≠ xyz {len(csym)} — 결합 실패")
    for k, (el, x, y, z) in enumerate(ocoords):
        if el != csym[k] or max(abs(x - cpos[k][0]), abs(y - cpos[k][1]),
                                abs(z - cpos[k][2])) > 1e-4:
            raise SystemExit(f"⛔ 원자 {k}: .out 최종좌표와 neutral_xyz 불일치 — "
                             "이 xyz 는 이 .out 의 산물이 아니다")
    if os.path.exists(os.path.join(os.path.dirname(a.stage_a_manifest),
                                   sm["dir"], sm["tag"] + ".xyz")):
        if _sha(os.path.join(os.path.dirname(a.stage_a_manifest),
                             sm["dir"], sm["tag"] + ".xyz")) == _sha(a.neutral_xyz):
            raise SystemExit("⛔ neutral_xyz 가 stage A 조립본과 **동일** — 미이완 부모다. "
                             "ORCA Opt 최종 xyz 를 넣어라 (R3 P0-2)")
    return {"gseed": a.gseed, "stage_a_calculation_id": sm["calculation_id"],
            "stage_a_manifest_sha256": _sha(a.stage_a_manifest),
            "out_path": os.path.abspath(a.neutral_out), "out_sha256": _sha(a.neutral_out),
            "xyz_sha256": _sha(a.neutral_xyz),
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
    if q and int(q[-1]) != exp["charge"]:
        codes.append("SECTOR_MISMATCH")
    if mu and int(mu[-1]) != exp["mult"]:
        codes.append("SECTOR_MISMATCH")
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
    if jt == "sp_vertical" and sec != "bs":
        if re.search(r"stability analysis indicates.*unstable", seg, re.I):
            codes.append("STABILITY_UNSTABLE")
        elif not re.search(r"stability analysis indicates", seg, re.I):
            codes.append("STABILITY_UNVERIFIED")      # 수행 양성 증거 요구 (R3)
    if jt == "opt_adiabatic" and "THE OPTIMIZATION HAS CONVERGED" not in seg:
        codes.append("OPT_UNCONVERGED")
    # localization class (사전 규칙 — Löwdin 국소 스핀 + atom_sets remap)
    if atom_sets and cond["wavefunction_class"] != "RKS":
        mvals = _lowdin_spins(seg)
        if mvals is not None:
            nat = job["n_atoms"]
            if len(mvals) != nat:
                codes.append("SECTOR_MISMATCH")       # 원자수 불일치 = 다른 계의 출력
            else:
                cls, shares = _loc_class(mvals, atom_sets, removed_H or [])
                realized["localization_class"] = cls
                realized["loc_shares"] = shares
    if codes:
        return "GATED", codes, realized
    return "OK", [], realized


def _lowdin_spins(seg):
    """LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS → [m_i] (마지막 블록)."""
    blocks = seg.split("LOEWDIN ATOMIC CHARGES AND SPIN POPULATIONS")
    if len(blocks) < 2:
        return None
    out = []
    for ln in blocks[-1].splitlines()[2:]:
        m = re.match(r"\s*(\d+)\s+\w+\s*:\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)", ln)
        if not m:
            if out:
                break
            continue
        out.append(float(m.group(3)))
    return out or None


def _loc_class(mvals, atom_sets_neutral, removed_H):
    """중성 프레임 atom_sets 를 doped 프레임으로 **재매핑 검증** 후 사전 규칙 적용."""
    kill = sorted(set(removed_H))
    def remap(i):
        if i in kill:
            return None
        return i - sum(1 for k in kill if k < i)
    tot_abs = sum(abs(m) for m in mvals)
    if tot_abs < LOC_ABS_MIN:
        return "NO_SPIN", {}
    shares = {}
    for g, idxs in atom_sets_neutral.items():
        mapped = [remap(i) for i in idxs]
        mapped = [i for i in mapped if i is not None]
        if any(i >= len(mvals) for i in mapped):
            return "REMAP_ERROR", {}
        shares[g] = round(sum(mvals[i] for i in mapped) / tot_abs, 4)
    winners = [g for g, v in shares.items() if abs(v) >= LOC_CLASS_MIN]
    return (winners[0] if len(winners) == 1 else "MIXED_UNRESOLVED"), shares


def analyze_dir(a):
    man = json.load(open(os.path.join(a.analyze, "manifest_stage_b.json")))
    atom_sets = man.get("atom_sets_neutral_frame")
    out = {"schema": "sdcp_stage0_analysis/v2", "jobs": {}, "emitted": {}}
    n_pend = n_bad = 0
    sha_seen = {}
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
    # 중복 출력물 (R3: 같은 가짜 OUT 복사 적발) — 관련 잡 전부 게이트
    for osha, tags in sha_seen.items():
        if len(tags) > 1:
            for t in tags:
                out["jobs"][t]["status"] = "GATED"
                out["jobs"][t].setdefault("codes", []).append("DUPLICATE_OUTPUT")
            out["emitted"].setdefault("DUPLICATE_OUTPUT", []).extend(tags)
            n_bad += len(tags)
    # SP→Opt dependency (R3 P0-3): 선행 sp 가 OK 아니면 opt 는 DEPENDENCY_NOT_MET
    for job in man["jobs"]:
        dep = job.get("depends_on")
        if not dep:
            continue
        rec = out["jobs"].get(job["tag"])
        if rec is None or rec.get("status") == "PENDING":
            continue
        if by_cid.get(dep) != "OK":
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
    made = []
    for t in picks:
        c = meta[t]["conditioning"]
        tag = t + "_hyb"
        make_inp(os.path.join(a.hybrid, f"{tag}.inp"),
                 f"dp{c['dp']}_{c['geometry_seed'].replace('g','gs')}_h"
                 f"{''.join(sorted(set(''.join(c['pattern'].split(',')))))}.xyz"
                 if False else meta[t]["tag"].rsplit("_", 3)[0] + ".xyz",
                 c["wavefunction_class"], c["orca_mult"],
                 bs=(c["sector"] == "bs"), job_type="sp_vertical",
                 scf_seed="s0", hybrid=True)
        made.append(tag)
    print(f"hybrid: decision set {len(picks)}잡 → 입력 생성 (NoAutoStart 강제)")
    return made


def compare_methods(a):
    """--compare <dir1> <dir2>: 두 분석의 그룹별 승자·순서 비교 → METHOD_DEPENDENT emit."""
    outs = []
    for d in a.compare:
        man = json.load(open(os.path.join(d, "manifest_stage_b.json")))
        ana = json.load(open(os.path.join(d, "analysis_stage_b.json")))
        meta = {j["tag"]: j for j in man["jobs"]}
        win = {}
        for t, r in ana["jobs"].items():
            if r.get("status") != "OK" or t not in meta:
                continue
            key = (meta[t]["conditioning"]["species"], meta[t]["conditioning"]["pattern"],
                   meta[t]["conditioning"]["job_type"])
            e = r["realized"]["energy_Eh"]
            if key not in win or e < win[key][1]:
                win[key] = (meta[t]["conditioning"]["sector"], e)
        outs.append(win)
    diff = {k: (outs[0][k][0], outs[1][k][0]) for k in outs[0]
            if k in outs[1] and outs[0][k][0] != outs[1][k][0]}
    if diff:
        for k, (s1, s2) in diff.items():
            print(f"  ⛔ METHOD_DEPENDENT: {k} 승자 {s1} ≠ {s2}")
        return 2
    print("  ✓ 두 방법의 그룹별 승자 일치")
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
                   coords=None, spins=None, version="6.1.0"):
    """R3 게이트 검증용 합성 ORCA 출력 — 양성 증거를 골라 넣고 뺄 수 있다."""
    t = "                                 * O   R   C   A *\n"
    t += f"                       Program Version {version} - RELEASE\n"
    if hf:
        t += f" Hartree-Fock type      HFTyp           .... {hf}\n"
    t += f" Total Charge           Charge          ....    {charge}\n"
    if mult is not None:
        t += f" Multiplicity           Mult            ....    {mult}\n"
    if coords is not None:
        t += "CARTESIAN COORDINATES (ANGSTROEM)\n---------------------------------\n"
        for el, p in coords:
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
            coords=list(zip(s3, p3o)), energies=(-500.0, -500.123456789)))
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
                                               coords=list(zip(s3, p3o))))
        raises(lambda: stage_b(B(neutral_out=out_nc)),
               "음성: Opt 수렴 문구 없는 .out → 거부")
        out_mm = os.path.join(td, "mm.out")
        p3bad = [[x + 0.5, y, z] for x, y, z in p3o]
        open(out_mm, "w").write(_fake_orca_out(hf="RHF", charge=0, mult=1,
                                               opt_converged=True,
                                               coords=list(zip(s3, p3bad))))
        raises(lambda: stage_b(B(neutral_out=out_mm)),
               "음성: .out 최종좌표 ≠ neutral_xyz → 결합 실패 거부")
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
    return 1 if fails else 0


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
    a = ap.parse_args()
    if a.selftest:
        return selftest()
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
    ap.error("--stage a|b · --analyze · --hybrid · --compare · --legacy · --selftest 중 하나")


if __name__ == "__main__":
    raise SystemExit(main())
