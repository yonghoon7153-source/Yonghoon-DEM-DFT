#!/usr/bin/env python3
"""build_v7c_trimer.py — 이완된 v7c 다이머에서 올리고머(n=3..8)를 α–α' 접합으로 조립.

원래는 트라이머 전용이었고 (파일명이 그 흔적), 2026-08-28 doped 재개 설계 v2
(`kb/questions/sdcp_doped_reopen_v2_2026_08_28.md`)의 Stage 0 을 위해 **n=4·6 과
홀 배치 선택 + machine manifest** 로 확장했다 (재승인 조건 ⑤·⑦ 준비).

n=3의 목적 (n=2 결과의 다음 질문):
  다이머 doped 스핀: A_SO3 62.3 / A_ring 17.4 / B_SO3 0.0 / B_ring 15.2 / rest 5.0 %
  → SO3:백본 파티션(62:33)은 모노머(65:35) 그대로, 백본 몫은 두 고리에 거의 반반.
  고리가 3개면?
   - trimer_doped_mid: 가운데 고리 SO3⁻ → 폴라론이 양옆 대칭으로 3고리에 퍼지는가 (헤드라인)
   - trimer_doped_end: 끝 고리 SO3⁻   → 결함에서 멀수록 몫이 어떻게 감쇠하는가 (감쇠길이)

n=4·6 의 목적 (재개 v2):
   - DP4/+1: 도핑률 25 % — DP3/+1(33 %)과 조성 bracket
   - DP6/+2: polaron/bipolaron 스핀 섹터 셋 (s=closed singlet · t=triplet · bs=BS singlet)
     을 **같은 조성·같은 전자수**에서 비교. 홀 간격 2종 이상 (--holes 반복 지정)

입력은 이완된 dimer_neutral.xyz 하나뿐 (모노머 파일·ASE·numpy 불필요):
  - 다이머 B쪽 절반(이완 기하)을 복제해 유닛으로 사용 — 유닛의 열린 α(과거 결합 자리)를
    사슬 끝의 자유 α에 C–C 1.45 A로 접합, 그 자유 α-H는 제거. n−2 회 반복.
  - 비틀림각은 원자간 최소거리 최대화(입체 회피)로 자동 선택 — 다이머 빌더와 동일 철학

  python3 build_v7c_trimer.py --selftest
  python3 build_v7c_trimer.py --dimer dimer_neutral.xyz --out trimer            # 레거시 n=3
  python3 build_v7c_trimer.py --dimer dimer_neutral.xyz --out dp4 --n 4 --holes B
  python3 build_v7c_trimer.py --dimer dimer_neutral.xyz --out dp6 --n 6 \\
      --holes B,E --holes C,D          # 홀 간격 2종, 각각 스핀 섹터 s/t/bs 생성

레거시 생성물 (--n 3, --holes 미지정 — 종전과 동일):
  trimer_neutral.xyz / trimer_doped_mid.xyz / trimer_doped_end.xyz /
  groups_trimer.json / trimer_*.inp / run_trimer.sh / analyze_trimer_spin.py / watch_trimer.sh

일반 생성물 (--n N [--holes ...]):
  dpN_neutral.xyz(.inp) / dpN_h<링들>_<섹터>.xyz(.inp) / groups_dpN.json /
  **manifest_stage0.json** — estimand_id·조성·전자수·스핀섹터·state-selection policy·
  중단 코드가 잡별로 박힌다 (재승인 조건 ⑦: 손으로 적은 숫자 없음)

이 도구가 **못 하는 것**
  · 기하를 이완하지 않는다 — 조립 + 입체 회피 배치까지. 이완은 ORCA 몫.
  · 스핀 상태를 보장하지 않는다 — 섹터별 기대값(M, <S2>)을 manifest 에 선언할 뿐,
    수렴 결과가 그 섹터인지는 회수 분석이 게이트로 검사해야 한다.
  · BS(broken-symmetry) 해는 순수 singlet 이 아니다 — manifest 가 <S2> 오염 보고를
    요구 사항으로 명시하지만 그 보고를 강제 실행하지는 못한다.
  · conformer 탐색을 하지 않는다 — 비틀림각 1개(입체 최적)만. conformer 2종은
    --step 을 바꾼 별도 빌드로 만든다 (Stage 0 설계 참조).
"""
import argparse
import hashlib
import json
import math
import os

RCOV = {"H": 0.31, "C": 0.76, "N": 0.71, "O": 0.66, "S": 1.05}
ZNUM = {"H": 1, "C": 6, "N": 7, "O": 8, "S": 16}
CC_NEW = 1.45          # 새 C–C 접합 길이 (다이머 빌더와 동일; 이완 다이머 실측 1.44)
UNIT_NAMES = "ABCDEFGH"

#: 스핀 섹터 (회신 R 반영: conditioning 에는 ansatz 만 — 'polaron/bipolaron' 은 realized).
#:   (라벨, ORCA mult, wavefunction_class, n_alpha_minus_beta(최종 Ms 기준), 설명)
#:   bs 는 고스핀(triplet) mult 로 수렴 후 BrokenSym 플립 — **BS M_s=0 determinant,
#:   nominal OSS candidate**. raw E 를 singlet 에너지로 쓰지 않는다.
SECTORS_ODD = (("d", 2, "UKS", 1, "doublet"),)
SECTORS_EVEN = (("s", 1, "RKS", 0, "RKS closed-shell candidate"),
                ("t", 3, "UKS", 2, "UKS triplet"),
                ("bs", 3, "UKS-BS", 0,
                 "BS M_s=0 determinant (nominal OSS candidate) — <S2>·국소 signed spin·"
                 "UNO 보고 필수; Yamaguchi AP 는 2-중심 식별시에만, 아니면 "
                 "NA_SPIN_MODEL_NOT_IDENTIFIED"))
ABORT_CODES = ("NA_STATE_NOT_IDENTIFIED", "NA_SPIN_MODEL_NOT_IDENTIFIED",
               "METHOD_DEPENDENT", "SECTOR_MISMATCH", "SCF_UNCONVERGED",
               "SPIN_CONTAMINATION_UNREPORTED")


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


def graft(csym, cpos, cnb, attC, attH, tpl, cc, step):
    """사슬의 자유 α(attC, 그 H=attH)에 템플릿을 접합. → (sym, pos, 채택각, dmin)"""
    d_dir = unit(sub(cpos[attH], cpos[attC]))
    p_new = add(cpos[attC], scal(d_dir, cc))
    R0 = rot_between(tpl["u_dangle"], scal(d_dir, -1.0))
    b0 = [apply_rot(R0, p) for p in tpl["base0"]]
    exclB = set([attC] + list(cnb[attC]))
    base_atoms = [i for i in range(len(csym)) if i != attH]
    best = None
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
        if best is None or dmin > best[0]:
            best = (dmin, th, newpos)
    dmin, th, npos = best
    nsym = [csym[i] for i in base_atoms] + list(tpl["sym"])
    nposs = [cpos[i] for i in base_atoms] + npos
    return nsym, nposs, th, dmin


def build_chain(sym, pos, n, cc, step, log=print):
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
                                     tpl, cc, step)
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
HYBRID_SPEC = {
    "method": "wB97X-D3 def2-TZVP defgrid3 TightSCF",
    "fresh_start": "r2SCAN orbital 미승계 (MORead 금지)",
    "decision_set": "vertical 승자 + adiabatic 승자 + 승자 대비 0.10 eV 이내의 경쟁 상태",
    "escalation": "hybrid 가 state identity/localization/순서를 바꾸면 그 경쟁 상태만 hybrid 재최적화",
    "disagreement": "두 방법이 갈리면 평균하지 않고 METHOD_DEPENDENT",
    "version_field": "orca_version 은 회수 시 .out 배너에서 채운다 (사전 기재 금지)",
}


def stage0_manifest(out, n, dimer_path, dimer_sha, jobs, torsions):
    """재승인 조건 ⑦ — 손으로 적은 숫자 없이, 빌더가 계산한 값만 들어간다."""
    man = {
        "schema": "sdcp_stage0_manifest/v1",
        "estimand_id": "sdcp-doped-gas-stage0/v2",
        "design_card": "kb/questions/sdcp_doped_reopen_v2_2026_08_28.md",
        "state_selection_policy": (
            "free-spin UKS/RKS, 선언된 스핀 섹터별 바닥상태. 제약 없음(NUPDOWN 상당 금지). "
            "bs 섹터만 예외적으로 triplet 수렴 후 BrokenSym 플립 — 그 결과는 순수 singlet "
            "이 아니며 <S2> 보고 없이는 SPIN_CONTAMINATION_UNREPORTED 로 중단"),
        "abort_codes": list(ABORT_CODES),
        "dp": n,
        "closed_form": "C_{11n} H_{14n+2-m} O_{6n} S_{2n} · N_e = 160n+2-m (회신 R 조건 1)",
        "hybrid_crosscheck": HYBRID_SPEC,
        "stage0_observable": "carrier_localization_profile — 집합별 charge·signed spin · "
                             "sum|m_i| · centroid/participation ratio · BLA/quinoid · UNO "
                             "unpaired 지표. ⛔ 기체상에서 carrier_retention 은 자명(전계=분자)이라 "
                             "측정 불가 (회신 R P0-2). slab carrier_retention_change 는 별도 규약",
        "input_dimer": {"path": os.path.abspath(dimer_path), "sha256": dimer_sha},
        "assembly_torsions": torsions,
        "jobs": jobs,
        "⚠": "회수 분석은 잡별 expected(mult, n_electrons, charge)를 manifest 와 대조해야 "
             "한다 — 수렴 여부만 보고 통과시키면 아홉 번째 실패다",
    }
    path = os.path.join(out, "manifest_stage0.json")
    json.dump(man, open(path, "w"), ensure_ascii=False, indent=1)
    return path


def orca_input(path, tag, mult, bs):
    with open(path, "w") as f:
        f.write("! UKS r2SCAN-3c Opt TightSCF\n%maxcore 6000\n")
        if bs:
            f.write("%scf BrokenSym 1,1 end\n")
        f.write(f"* xyzfile 0 {mult} {tag}.xyz\n")


def build_general(a, sym, pos):
    """--n N [--holes ...] 경로: dpN_* 산출 + manifest."""
    csym, cpos, torsions = build_chain(sym, pos, a.n, a.cc, a.step)
    cnb, crings, csulf = analyze(csym, cpos)
    assert len(crings) == a.n and len(csulf) == a.n, \
        f"{a.n}-량체: 링 {len(crings)} · 설포네이트 {len(csulf)}"
    names = ring_chain_names(crings)
    order = "".join(names[ri] for ri in sorted(names, key=lambda r: names[r]))
    print(f"사슬 명명: {order} (앵커 A = 최소 인덱스 끝 링)")

    groups = {}
    for su in csulf:
        nm = names[su["ring"]]
        groups[f"{nm}_SO3"] = sorted([su["sS"]] + su["sO"])
        groups[f"{nm}_ring"] = sorted(crings[su["ring"]]["ring"])
    json.dump({"neutral": groups,
               "acidH": {names[su["ring"]]: su["aH"] for su in csulf}},
              open(os.path.join(a.out, f"groups_dp{a.n}.json"), "w"), indent=1)

    v7c_real = (formula_of(sym) == V7C_DIMER_FORMULA)
    if not v7c_real:
        print(f"⚠ 입력 다이머 조성 {formula_of(sym)} ≠ v7c({V7C_DIMER_FORMULA}) — "
              "닫힌꼴 검증 생략 (합성/시험 입력)")

    def _validate(vsym, m):
        if v7c_real and not check_closed_form(vsym, a.n, m):
            we_f, we_e = expected_species(a.n, m)
            raise SystemExit(f"⛔ 닫힌꼴 불일치 — 빌더 산출 {formula_of(vsym)}/{electrons_of(vsym)}e "
                             f"vs 기대 {we_f}/{we_e}e (n={a.n}, m={m}). 빌더/입력 오류 — 멈춘다")

    def _micro(m, rmH, sec, wf):
        return {"DP": a.n, "formal_oxidation_count": m, "removed_H_indices": rmH,
                "external_counterion_inventory": "none — internal-compensation stratum "
                    "(m tethered SO3- compensate formal backbone oxidation +m)",
                "conformer_cluster": f"torsion_scan_step{a.step}",
                "wavefunction_spin_sector": f"{wf}/{sec}",
                "localization_seed": "default", "realized_localization": None,
                "pose": None, "slab_basin": None}

    jobs = []
    tag0 = f"dp{a.n}_neutral"
    write_xyz(os.path.join(a.out, f"{tag0}.xyz"), csym, cpos,
              f"v7c DP{a.n} neutral (assembled; torsions "
              f"{[t['torsion_deg'] for t in torsions]} deg)")
    e0 = electrons_of(csym)
    check_parity(e0, 1)
    _validate(csym, 0)
    orca_input(os.path.join(a.out, f"{tag0}.inp"), tag0, 1, False)
    jobs.append(dict(tag=tag0, species=f"DP{a.n}_h0_Q0", holes=[], removed_H_indices=[],
                     sector="n", wavefunction_class="RKS", orca_mult=1,
                     n_alpha_minus_beta=0, net_charge=0, n_atoms=len(csym),
                     all_electron_count=e0, formula=formula_of(csym),
                     sector_label="RKS closed-shell (neutral reference)",
                     seeded_separation=None, microstate_id=_micro(0, [], "n", "RKS")))

    for spec in (a.holes or []):
        hs = resolve_holes(spec, names, csulf)
        letters = "".join(h[0] for h in hs)
        rmH = sorted(h[1] for h in hs)
        m = len(hs)
        vsym, vpos, _ = remove_atoms(csym, cpos, rmH)
        e = electrons_of(vsym)
        _validate(vsym, m)
        sectors = SECTORS_ODD if m % 2 == 1 else SECTORS_EVEN
        sep = (abs(ord(letters[0]) - ord(letters[1])) if m == 2 else None)
        base = f"dp{a.n}_h{letters}"
        write_xyz(os.path.join(a.out, f"{base}.xyz"), vsym, vpos,
                  f"DP{a.n}_h{m}_Q0: neutral minus acid H of ring(s) {letters} "
                  f"(net charge 0, formal_oxidation_count {m})")
        for sec, mult, wf, nab, label in sectors:
            check_parity(e, mult)
            tag = f"{base}_{sec}"
            # 섹터별 .xyz 는 같은 기하 — inp 가 xyzfile 로 base 를 공유한다
            orca_input(os.path.join(a.out, f"{tag}.inp"), base, mult, bs=(sec == "bs"))
            jobs.append(dict(tag=tag, species=f"DP{a.n}_h{m}_Q0", holes=list(letters),
                             removed_H_indices=rmH, sector=sec, wavefunction_class=wf,
                             orca_mult=mult, n_alpha_minus_beta=nab, net_charge=0,
                             n_atoms=len(vsym), all_electron_count=e,
                             formula=formula_of(vsym), sector_label=label,
                             seeded_separation=sep,
                             microstate_id=_micro(m, rmH, sec, wf)))
        print(f"  홀 {letters}: {len(sectors)}섹터 ({'/'.join(s[0] for s in sectors)}) · "
              f"전자 {e} · {formula_of(vsym)}"
              + (" · 닫힌꼴 ✓" if v7c_real else ""))

    sha = hashlib.sha256(open(a.dimer, "rb").read()).hexdigest()
    mp = stage0_manifest(a.out, a.n, a.dimer, sha, jobs, torsions)
    man = json.load(open(mp))
    man["closed_form_validated"] = v7c_real
    man["atom_sets_neutral_frame"] = atom_sets_of(csym, cnb, crings, csulf, names)
    man["⚠_atom_sets"] = ("중성 프레임 인덱스 — doped 잡에서는 removed_H_indices 만큼 "
                          "밀린다. 재매핑은 분석기가 수행하고 검증한다")
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=1)
    print(f"manifest: {mp}  (잡 {len(jobs)}개 · 닫힌꼴 검증 "
          f"{'✓' if v7c_real else '생략(비실물)'} · atom_sets {len(man['atom_sets_neutral_frame'])}집합)")
    return jobs


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
    인덱스: 0 S · 1 Ca1 · 2 Cb1 · 3 Cb2 · 4 Ca2 · 5 H(Ca1) · 6 H(Ca2) · 7 Csp ·
            8 Ssulf · 9-11 O · 12 산성H
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
    """유닛 2개를 α–α' 1.45 Å 로 접합한 합성 다이머 (24원자, 자유 α-H 양끝 1개씩).

    B 유닛 = A 유닛을 새 결합 중점에 대해 **점반전**한 사본 — 거리 보존이라 위상이
    그대로 유지되고, B 가 A 의 반대쪽(+x)으로 뻗는다 (거울 배치는 되돌아 접혀 실패했다).
    """
    s1, p1 = _synthetic_unit()
    d = unit(sub(p1[6], p1[4]))                          # Ca2 의 H 방향 = 새 결합 방향
    target = add(p1[4], scal(d, 1.45))
    M = scal(add(p1[4], target), 0.5)
    p2 = [sub(scal(M, 2.0), p) for p in p1]              # 점반전: B.Ca2 가 target 에 앉는다
    # 결합 α 의 H 제거: A 의 H6, B 의 H6-상 (결합 안쪽을 향한다)
    sym = [x for i, x in enumerate(s1) if i != 6] + [x for i, x in enumerate(s1) if i != 6]
    pos = [x for i, x in enumerate(p1) if i != 6] + [x for i, x in enumerate(p2) if i != 6]
    return sym, pos


def selftest():
    import tempfile
    fails = []

    def chk(ok, msg):
        print(("  ✓ " if ok else "  ✗ ") + msg)
        if not ok:
            fails.append(msg)

    print("── build_v7c_trimer selftest ──")
    sym, pos = _synthetic_dimer()
    nb, rings, sulf = analyze(sym, pos)
    chk(len(sym) == 24 and len(rings) == 2 and len(sulf) == 2,
        f"합성 다이머 위상 (원자 {len(sym)} · 링 {len(rings)} · SO3 {len(sulf)})")

    with tempfile.TemporaryDirectory() as td:
        dim = os.path.join(td, "dimer.xyz")
        write_xyz(dim, sym, pos, "synthetic dimer for selftest")

        # ── n=3: 사슬 성장 + 명명
        c3, p3, t3 = build_chain(sym, pos, 3, CC_NEW, 30, log=lambda *a: None)
        chk(len(c3) == 24 + 11, f"n=3 조립 원자수 {len(c3)} (기대 35)")
        _, r3, s3 = analyze(c3, p3)
        n3 = ring_chain_names(r3)
        chk(sorted(n3.values()) == ["A", "B", "C"], f"n=3 링 명명 {sorted(n3.values())}")

        # ── n=4: bracket 크기
        c4, p4, _ = build_chain(sym, pos, 4, CC_NEW, 30, log=lambda *a: None)
        chk(len(c4) == 24 + 22, f"n=4 조립 원자수 {len(c4)} (기대 46)")
        _, r4, _ = analyze(c4, p4)
        chk(sorted(ring_chain_names(r4).values()) == ["A", "B", "C", "D"], "n=4 링 명명 A–D")

        # ── 일반 경로 CLI 로 n=4, 홀 1개 (doublet 섹터 1개)
        a4 = argparse.Namespace(dimer=dim, out=os.path.join(td, "dp4"), cc=CC_NEW,
                                step=30, n=4, holes=["B"])
        os.makedirs(a4.out)
        jobs4 = build_general(a4, sym, pos)
        man4 = json.load(open(os.path.join(a4.out, "manifest_stage0.json")))
        chk(len(jobs4) == 2 and jobs4[1]["sector"] == "d" and jobs4[1]["orca_mult"] == 2
            and jobs4[1]["n_alpha_minus_beta"] == 1,
            "n=4 홀 1개 → neutral + doublet 1섹터 (orca_mult·nab 분리)")
        chk(man4["estimand_id"] == "sdcp-doped-gas-stage0/v2"
            and man4["jobs"][1]["all_electron_count"] == man4["jobs"][0]["all_electron_count"] - 1,
            "manifest: estimand_id + 전전자수(중성−1) 자동 계산 — 손 전사 없음")
        chk(man4["jobs"][1]["species"] == "DP4_h1_Q0"
            and man4["jobs"][1]["net_charge"] == 0
            and man4["jobs"][1]["removed_H_indices"],
            "종 ID 는 DP4_h1_Q0 형식 — 'DP4/+1' 오독 방지 (회신 R 조건 1)")
        chk(man4["closed_form_validated"] is False,
            "합성 입력은 닫힌꼴 검증 생략 표시 (validated=False — 통과 아님)")
        mtxt = open(os.path.join(a4.out, "manifest_stage0.json")).read()
        chk("bipolaron" not in mtxt and "polaron" not in mtxt.replace("polaron_", ""),
            "conditioning 순수성: manifest 에 'polaron/bipolaron' 라벨 없음 (회신 R P0-3)")
        chk("carrier_localization_profile" in mtxt and "NA_SPIN_MODEL_NOT_IDENTIFIED" in mtxt
            and "METHOD_DEPENDENT" in mtxt,
            "Stage0 관측량 교체 + 신규 중단코드 2종 (회신 R P0-2 · 조건 5·7)")
        chk("atom_sets_neutral_frame" in man4
            and set(man4["atom_sets_neutral_frame"]) >= {"backbone", "sidechain_rest"},
            "atom_sets 고정 (carrier_localization_profile 의 집합 — 회신 R 조건 4)")
        allsets = sum(man4["atom_sets_neutral_frame"].values(), [])
        chk(len(allsets) == len(set(allsets)) == man4["jobs"][0]["n_atoms"],
            "atom_sets 는 전 원자를 정확히 1회씩 분할 (겹침·누락 없음)")
        chk("NA_STATE_NOT_IDENTIFIED" in man4["abort_codes"],
            "manifest 에 중단 코드 선언 (정의역 공백을 코드가 말한다)")

        # ── n=6, 홀 2개 × 간격 2종 → 짝수 전자 → 섹터 s/t/bs
        a6 = argparse.Namespace(dimer=dim, out=os.path.join(td, "dp6"), cc=CC_NEW,
                                step=45, n=6, holes=["B,E", "C,D"])
        os.makedirs(a6.out)
        jobs6 = build_general(a6, sym, pos)
        secs = [j["sector"] for j in jobs6 if j["species"] == "DP6_h2_Q0"]
        chk(secs == ["s", "t", "bs", "s", "t", "bs"],
            f"n=6 홀 2개 × 간격 2종 → 섹터 s/t/bs ×2 ({secs})")
        bs_inp = open(os.path.join(a6.out, "dp6_hBE_bs.inp")).read()
        chk("BrokenSym" in bs_inp and " 0 3 " in bs_inp,
            "bs 섹터 입력: triplet(mult 3) 수렴 후 BrokenSym 플립")
        e_even = all(j["all_electron_count"] % 2 == 0 for j in jobs6 if j["holes"])
        chk(e_even, "홀 2개 종은 전자수 짝수 (parity 정합)")

        # ── ⛔ 음성 1: 없는 링 홀
        try:
            a_bad = argparse.Namespace(dimer=dim, out=os.path.join(td, "bad"), cc=CC_NEW,
                                       step=45, n=3, holes=["Z"])
            os.makedirs(a_bad.out)
            build_general(a_bad, sym, pos)
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "음성: --holes Z (없는 링) → 멈춘다")

        # ── 닫힌꼴 기대식 (회신 R 조건 1) — 실물 다이머가 repo 에 있으면 실검증
        rd = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "..", "db", "structures", "sdcp_v7c_dimer_neutral.xyz")
        if os.path.isfile(rd):
            rs, rp = read_xyz(rd)
            aR = argparse.Namespace(dimer=rd, out=os.path.join(td, "real3"), cc=CC_NEW,
                                    step=60, n=3, holes=["B"])
            os.makedirs(aR.out)
            jR = build_general(aR, rs, rp)
            mR = json.load(open(os.path.join(aR.out, "manifest_stage0.json")))
            chk(mR["closed_form_validated"] is True
                and jR[1]["all_electron_count"] == 160 * 3 + 2 - 1,
                f"실물 다이머 닫힌꼴 검증 ✓ (DP3_h1 전자 {jR[1]['all_electron_count']} = 481)")
        else:
            print("  (실물 다이머 없음 — 닫힌꼴 실검증 생략)")
        chk(not check_closed_form(["C"] * 33, 3, 1),
            "음성: 닫힌꼴 함수가 틀린 조성을 거부한다")

        # ── ⛔ 음성 2: 전자 짝홀 ↔ 다중도 불일치는 잡을 만들지 않는다
        try:
            check_parity(101, 1)
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "음성: 전자 101개 + singlet → 정의부터 불가, 거부")

        # ── ⛔ 음성 3: 다이머가 아닌 입력 (트라이머를 먹임)
        try:
            build_chain(c3, p3, 4, CC_NEW, 45, log=lambda *a: None)
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "음성: 트라이머를 --dimer 로 먹이면 거부 (링 3 검출)")

        # ── 레거시 경로가 그대로 도는가 (합성 다이머, 출력 파일 세트)
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
    ap.add_argument("--step", type=int, default=10, help="비틀림각 스캔 간격(도)")
    ap.add_argument("--n", type=int, default=3, help="올리고머 길이 (3..8)")
    ap.add_argument("--holes", action="append",
                    help="탈양성자화할 링 (예: 'B' · 'B,E'). 반복 지정 = 배치 여러 종. "
                         "미지정 + --n 3 이면 레거시 mid/end 경로")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.dimer and a.out):
        ap.error("--dimer 와 --out 이 필요하다 (--selftest 제외)")
    if not (3 <= a.n <= 8):
        ap.error("--n 은 3..8")
    os.makedirs(a.out, exist_ok=True)
    sym, pos = read_xyz(a.dimer)
    if len(sym) != 68:
        print(f"⚠ 다이머 {len(sym)}원자 — v7c 실물(68)이 아니다. 합성/시험 입력으로 간주하고 진행")
    if a.n == 3 and not a.holes:
        build_legacy_trimer(a, sym, pos)
    else:
        build_general(a, sym, pos)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
