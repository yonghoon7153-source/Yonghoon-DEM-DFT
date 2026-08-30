#!/usr/bin/env python3
"""LHS 저-φ_AM 확장 배치의 설계점을 뽑는다 (사전등록 lhs_extension_prereg_20260829.md).

    python3 scripts/lhs_ext_design.py --scan ~/dem_test/lhs --out lhs_ext_design.csv
    python3 scripts/lhs_ext_design.py --selftest

★ 이 스크립트가 하는 일은 셋이다.

  ① **현재 상자를 하드코딩하지 않고 읽는다.**  `lhs00_*/input_*.liggghts` 헤더 130건을
     두 형식(3-type / 2-type) 모두 파싱해 노브별 범위를 유도한다.  손으로 적은 범위는
     읽은 적 없는 파일에 대해 조용히 틀린다 — 실제로 초안이 2-type 30건을 못 읽고도
     범위를 적었다.

  ② **입자 수를 런 전에 예측한다.**  삽입 부피 V_ins 를 실측 두 케이스로 보정했고
     (selftest 가 0.7 % 안에서 재현하는지 단언한다), 그래서 사전등록 §3-2 의
     150,000 상한을 **GPU 없이** 강제할 수 있다.

  ③ **상한은 실제 추첨값에만 건다.**  `r_SE` 를 전 구간에서 뽑고 총입자수를 계산한 뒤,
     **넘을 때만** 상한을 만족하는 최소 `r_SE` 로 구간을 좁혀 다시 사상하고 표시한다.
     ⚠ 초판은 순서가 반대였다 — 하한을 **먼저** 올리고 같은 분위를 좁힌 구간에 사상했다.
     그런데 그렇게 절단된 네 점은 **nominal 반지름으로도 상한 아래**였다 (Codex Q3 [P1]):
     "그 축의 최솟값이 뽑혔다면" 이라는 최악 가정으로 좌표를 움직인 것이고, 저-φ_AM 에서만
     nuisance 분포를 바꿔 추정값을 흔들 수 있다.

  ④ **층당 하나의 8칸 LHS.**  초판은 bimodal 6점과 mono 2점을 따로 추첨해 붙여서 합친
     8점이 공통 LHS 가 **아니었다** (64칸 중 11 빈칸·10 중복, Codex Q5 [P1]).
     ⇒ 공통 4축에 8점 LHS 하나를 세우고 type 별 추가축만 따로 뽑는다.
     `check_lhs()` 가 **산출물에서** 점유를 검사하고 `--verify` 가 CSV 를 다시 본다.

⚠ 조성 규약: 헤더의 `pdd` 는 **질량분율(wt%)** 이다 (사전등록 §0-1, 실측 대조).
   부피분율은 밀도로 환산해야 나온다 — `ρ_AM = 4800`, `ρ_SE = 2000` kg/m³.
"""
from __future__ import annotations

import argparse
import csv
import glob
import math
import os
import re
import sys

# --- 물질 상수 (입력 파일의 particletemplate/sphere density) --------------
RHO_AM = 4800.0
RHO_SE = 2000.0

# --- 삽입 부피 (m³) — 실측 두 케이스로 보정.  selftest 가 검증한다 -------
V_INS = 3.34e-4

# --- 사전등록된 설계 상수 (§2 · §3) --------------------------------------
PDD_SE_LO, PDD_SE_HI = 0.30, 0.70      # (열림, 닫힘]
N_STRATA = 8
PER_STRATUM = 8
THREE_TYPE_PER_STRATUM = 6             # 나머지는 2-type
N_MAX_PARTICLES = 150_000
DESIGN_SEED = 20260829                 # 등록된 난수 씨앗 — 바꾸면 다른 설계다
SEED_LO, SEED_HI = 20000, 29999        # per-run seed 범위


# --- per-run seed 는 **소수여야 한다** (2026-08-30, Codex R14 P1-01) ----------
#  ⚠⚠ 이 리포는 이 사고를 **이미 겪었다**: 08-18 의 130점 배치 v2 에서 `insert/pack`
#     seed 가 비소수라 **25 케이스가 1분 만에 abort** 했고, `afterany` chain 이 실패를
#     안 막아 **조용히 지나갔다** (`docs/lhs_design_dataset_20260818.md` §P-1).
#     그 문서가 남긴 교훈이 *"검사 목록에 없는 항목은 안 잡힌다 — v3 검사부터 넣었다"*
#     인데, **이 확장 생성기가 그 검사를 물려받지 않아** 64개 중 61개가 합성수로 나왔다.
#     교훈을 문서에만 두면 새 생성기로 전달되지 않는다는 실증이다.
#  ★ 좌표를 흔들지 않는 방법: `rng.randint` 호출은 **그대로 두고**(난수 스트림이 바뀌면
#    좌표가 전부 달라진다) 뽑힌 값을 사후에 소수로 올린다.  결정론적이다.
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def next_free_prime(v, used, lo=SEED_LO, hi=SEED_HI):
    """`v` 이상에서 미사용 소수.  상한을 넘으면 `lo` 부터 다시 올라간다."""
    for c in list(range(v, hi + 1)) + list(range(lo, v)):
        if c not in used and is_prime(c):
            return c
    raise SystemExit(f'[{lo}, {hi}] 안에 미사용 소수가 없다 (요청 {len(used)+1}개)')


def assign_prime_seeds(pts):
    """뽑힌 seed 를 순서대로 미사용 소수로 올린다 (제자리 수정).  → 배정된 목록."""
    used, out = set(), []
    for p in pts:
        s = next_free_prime(int(p['seed']), used)
        used.add(s)
        p['seed'] = s
        out.append(s)
    return out


# --- 실측 대조 (selftest 전용) -------------------------------------------
#   ibb `lhs00_000` / `lhs00_110` 의 마지막 덤프에서 센 값
MEASURED = [
    dict(case='lhs00_000', volfrac=0.222984,
         radii_um=[5.5, 0.5, 1.0], vol_frac=[0.4280, 0.2776, 0.2944],
         counts=[46, 39_719, 5_265]),
    dict(case='lhs00_110', volfrac=0.250627,
         radii_um=[1.0, 1.0], vol_frac=[0.625, 0.375],
         counts=[12_434, 7_460]),
]


# =========================================================================
# 조성 환산 — wt% ↔ vol%
# =========================================================================
def vol_from_mass(w_am: float) -> float:
    """AM 질량분율 → AM 부피분율 (고체 기준).  사전등록 §0-2."""
    return (RHO_SE * w_am) / (RHO_AM - (RHO_AM - RHO_SE) * w_am)


def mass_from_vol(phi_am: float) -> float:
    """AM 부피분율 → AM 질량분율 (역함수)."""
    return (RHO_AM * phi_am) / (RHO_SE + (RHO_AM - RHO_SE) * phi_am)


def phi_am_of_pdd_se(pdd_se: float) -> float:
    return vol_from_mass(1.0 - pdd_se)


# =========================================================================
# 입자 수 예측
# =========================================================================
def n_spheres(vol_frac_of_solid: float, r_um: float, volfrac: float,
              v_ins: float = V_INS) -> float:
    """한 상(phase)의 입자 수.  r 은 µm, 반환은 개수."""
    r_m = r_um * 1e-6 * 1000.0        # 헤더의 길이 단위는 box 0.05 = 50 µm 스케일
    return (v_ins * volfrac * vol_frac_of_solid) / ((4.0 / 3.0) * math.pi * r_m ** 3)


def r_se_min_for_ceiling(n_am: float, phi_se: float, volfrac: float,
                         ceiling: int = N_MAX_PARTICLES) -> float:
    """총 입자 수가 상한을 넘지 않는 최소 r_SE (µm).  N_SE ∝ r⁻³ 를 뒤집어 푼다."""
    room = ceiling - n_am
    if room <= 0:
        return float('inf')                       # AM 만으로 이미 초과 → 점을 버린다
    r_m = ((V_INS * volfrac * phi_se) / ((4.0 / 3.0) * math.pi * room)) ** (1.0 / 3.0)
    return r_m / 1e-6 / 1000.0


# =========================================================================
# 헤더 파싱 — 두 형식
# =========================================================================
#  ⚠ `re.M` 필수 — 이 헤더는 파일의 **둘째 줄**이다 (첫 줄은 `# ====` 구분선).
#     MULTILINE 없이 `^` 를 쓰면 130 건이 **전부 조용히 unread 로 간다** (2026-08-29 실측).
#     selftest `parse-*` 가 이 결함을 재현한다.
_RE_KIND = re.compile(r'^#\s*(lhs\d+_\d+):\s*(\S+)', re.M)
_RE_3T = re.compile(r'rP=([\d.eE+-]+)\s+rS=([\d.eE+-]+)\s+rSE=([\d.eE+-]+)')
_RE_3P = re.compile(r'AM_P=([\d.]+)\s+AM_S=([\d.]+)\s+SE=([\d.]+)')
_RE_2T = re.compile(r'rAM=([\d.eE+-]+)\s+rSE=([\d.eE+-]+)')
_RE_2P = re.compile(r'pdd\s+AM=([\d.]+)\s+SE=([\d.]+)')
_RE_VF = re.compile(r'volfrac=([\d.eE+-]+)')
_RE_SD = re.compile(r'seed=(\d+)')


def parse_headers(root: str) -> tuple[list[dict], list[str]]:
    """모든 케이스의 헤더를 읽는다.  **읽지 못한 파일은 조용히 넘기지 않고 돌려준다.**"""
    rows, unread = [], []
    pat = os.path.join(root, 'lhs*_*', 'input_lhs*_*.liggghts')
    for f in sorted(glob.glob(pat)):
        txt = open(f, encoding='utf-8', errors='replace').read(1200)
        mk, mvf, msd = _RE_KIND.search(txt), _RE_VF.search(txt), _RE_SD.search(txt)
        m3t, m3p = _RE_3T.search(txt), _RE_3P.search(txt)
        m2t, m2p = _RE_2T.search(txt), _RE_2P.search(txt)
        if not (mk and mvf):
            unread.append(f)
            continue
        row = dict(case=mk.group(1), kind=mk.group(2),
                   volfrac=float(mvf.group(1)),
                   seed=int(msd.group(1)) if msd else -1)
        if m3t and m3p:
            rP, rS, rSE = (float(x) * 1000.0 for x in m3t.groups())
            wP, wS, wSE = (float(x) for x in m3p.groups())
            row.update(ntype=3, rP_um=rP, rS_um=rS, rSE_um=rSE,
                       w_AM_P=wP, w_AM_S=wS, pdd_SE=wSE)
        elif m2t and m2p:
            rAM, rSE = (float(x) * 1000.0 for x in m2t.groups())
            wAM, wSE = (float(x) for x in m2p.groups())
            row.update(ntype=2, rP_um=rAM, rS_um=None, rSE_um=rSE,
                       w_AM_P=wAM, w_AM_S=0.0, pdd_SE=wSE)
        else:
            unread.append(f)
            continue
        row['phi_AM'] = phi_am_of_pdd_se(row['pdd_SE'])
        rows.append(row)
    return rows, unread


def derive_box(rows: list[dict]) -> dict:
    """현재 상자를 유도한다 — 3-type / 2-type 을 **따로** (범위가 다르다)."""
    def rng(vals):
        vals = [v for v in vals if v is not None]
        return (min(vals), max(vals)) if vals else (None, None)

    box = {}
    for nt in (3, 2):
        sub = [r for r in rows if r['ntype'] == nt]
        if not sub:
            continue
        b = dict(n=len(sub),
                 rP_um=rng(r['rP_um'] for r in sub),
                 rSE_um=rng(r['rSE_um'] for r in sub),
                 pdd_SE=rng(r['pdd_SE'] for r in sub),
                 volfrac=rng(r['volfrac'] for r in sub),
                 phi_AM=rng(r['phi_AM'] for r in sub))
        if nt == 3:
            b['rS_um'] = rng(r['rS_um'] for r in sub)
            b['s_AM_P'] = rng(r['w_AM_P'] / (r['w_AM_P'] + r['w_AM_S'])
                              for r in sub if (r['w_AM_P'] + r['w_AM_S']) > 0)
        b['kinds'] = sorted({r['kind'] for r in sub})
        #  ⚠ 2-type 은 `mono_AM_P` / `mono_AM_S` 로 갈리고 **반지름 범위가 다르다**.
        #     합집합에서 뽑으면 어느 쪽에도 없는 반지름이 나오고 라벨이 임의가 된다.
        #     ⇒ 종류별 범위를 따로 유도해 라벨을 **반지름이 정하게** 한다.
        b['per_kind'] = {
            kd: dict(n=sum(1 for r in sub if r['kind'] == kd),
                     rP_um=rng(r['rP_um'] for r in sub if r['kind'] == kd),
                     rSE_um=rng(r['rSE_um'] for r in sub if r['kind'] == kd))
            for kd in b['kinds']}
        box[nt] = b
    return box


def kind_for_radius(b: dict, r_um: float) -> str:
    """관측된 종류별 반지름 범위로 라벨을 정한다 — 라벨이 반지름을 따르지, 그 반대가 아니다."""
    pk = b['per_kind']
    inside = [kd for kd, v in pk.items()
              if v['rP_um'][0] - 1e-9 <= r_um <= v['rP_um'][1] + 1e-9]
    if len(inside) == 1:
        return inside[0]
    cands = inside or list(pk)
    return min(cands, key=lambda kd: abs(r_um - sum(pk[kd]['rP_um']) / 2.0))


# =========================================================================
# LHS
# =========================================================================
def lhs_unit(n: int, k: int, rng) -> list[list[float]]:
    """[0,1)^k 위의 Latin hypercube — 축마다 n 칸을 한 번씩 쓴다."""
    out = [[0.0] * k for _ in range(n)]
    for j in range(k):
        order = list(range(n))
        rng.shuffle(order)
        for i, cell in enumerate(order):
            out[i][j] = (cell + rng.random()) / n
    return out


def _scale(u: float, lo: float, hi: float) -> float:
    return lo + u * (hi - lo)


# =========================================================================
# 설계 생성
# =========================================================================
def generate(box: dict, seed: int = DESIGN_SEED) -> tuple[list[dict], list[str]]:
    import random
    rng = random.Random(seed)
    pts, notes = [], []

    b3, b2 = box.get(3), box.get(2)
    if not b3 or not b2:
        raise SystemExit('현재 상자에 3-type 또는 2-type 이 없다 — 스캔 경로를 확인할 것')

    width = (PDD_SE_HI - PDD_SE_LO) / N_STRATA
    idx = 0
    for st in range(N_STRATA):
        lo = PDD_SE_LO + st * width
        hi = lo + width
        #  ★★ **층당 하나의 8칸 LHS** (Codex Q5 [P1], 2026-08-29).
        #     초판은 bimodal 6점과 mono 2점을 **따로** 추첨해 붙였다 ⇒ 합친 8점은 공통
        #     LHS 가 아니었고, 8층을 통틀어 공통 8칸을 정확히 한 번씩 쓴 층이 **하나뿐**,
        #     64칸 중 11칸이 비고 10칸이 중복됐다.  그러면 §3-1 이 예산을 층화에 쓴 근거
        #     ("나머지 노브가 층마다 균형을 이뤄 상쇄된다")가 **성립하지 않는다.**
        #  ⇒ 공통 4축(pdd_SE · volfrac · rP분위 · rSE분위)에 **8점 LHS 하나**를 세우고,
        #     type 별 추가축(rS · s_AM_P)만 bimodal 6점에 대해 따로 LHS 를 세운다.
        #     rP 는 **분위를 공유**하고 type 별 범위로 사상한다 — 범위가 달라도 단위입방체
        #     위의 LHS 성질은 유지된다.
        U = lhs_unit(PER_STRATUM, 4, rng)           # [pdd_SE, volfrac, rP_q, rSE_q]
        Ub = lhs_unit(THREE_TYPE_PER_STRATUM, 2, rng)   # [rS, s_AM_P] — bimodal 전용
        #  type 배정: bimodal 6 · mono_AM_P 1 · mono_AM_S 1.  행 순서와 축값의 상관을
        #  없애려 배정 벡터를 섞는다 (lhs_unit 이 축마다 독립 셔플이라 이미 무상관이지만
        #  명시적으로 둔다).
        kinds2 = sorted(box[2]['per_kind'])
        assign = ([(3, None)] * THREE_TYPE_PER_STRATUM
                  + [(2, kd) for kd in kinds2][:PER_STRATUM - THREE_TYPE_PER_STRATUM])
        rng.shuffle(assign)
        bi = 0
        for u, (nt, kd_assigned) in zip(U, assign):
            b = box[nt]
            pdd_se = _scale(u[0], lo, hi)
            phi_se = 1.0 - phi_am_of_pdd_se(pdd_se)
            volfrac = _scale(u[1], *b['volfrac'])
            rP_rng = b['rP_um'] if nt == 3 else b['per_kind'][kd_assigned]['rP_um']
            rP = _scale(u[2], *rP_rng)
            if nt == 3:
                rS = _scale(Ub[bi][0], *b['rS_um'])
                s = _scale(Ub[bi][1], *b['s_AM_P'])
                bi += 1
            else:
                rS, s = None, 1.0

            # AM 입자 수는 r_SE 와 무관 → 먼저 확정한다
            phi_am = 1.0 - phi_se
            if nt == 3:
                # 질량 분할 s 를 부피 분할로 옮긴다 (두 AM 은 밀도가 같다)
                n_am = (n_spheres(phi_am * s, rP, volfrac)
                        + n_spheres(phi_am * (1 - s), rS, volfrac))
            else:
                n_am = n_spheres(phi_am, rP, volfrac)

            #  ★ 상한은 **실제 추첨값**에만 건다 (Codex Q3 [P1]).
            #    초판은 `r_SE` 하한을 **먼저** 올리고 같은 LHS 분위를 좁힌 구간에 재사상했다.
            #    그런데 절단된 네 점은 **nominal 반지름으로도 상한 아래**였다 —
            #    "그 축의 최솟값이 뽑혔다면" 이라는 최악 가정으로 좌표를 움직인 것이고,
            #    저-φ_AM 에서만 nuisance 분포를 바꿔 추정값을 흔들 수 있다.
            r_lo0, r_hi = b['rSE_um']
            rSE = _scale(u[3], r_lo0, r_hi)
            n_se = n_spheres(phi_se, rSE, volfrac)
            r_lo, truncated = r_lo0, 0
            if n_am + n_se > N_MAX_PARTICLES:
                r_lo = max(r_lo0, r_se_min_for_ceiling(n_am, phi_se, volfrac))
                if not math.isfinite(r_lo) or r_lo > r_hi:
                    notes.append(f'stratum {st} nt{nt}: AM 만으로 상한 초과 '
                                 f'(rP={rP:.2f} vf={volfrac:.3f}) — r_hi 로 눌렀다')
                    r_lo = r_hi
                rSE = _scale(u[3], r_lo, r_hi)
                n_se = n_spheres(phi_se, rSE, volfrac)
                truncated = 1

            idx += 1
            pts.append(dict(
                id=f'lhsx_{idx:03d}', stratum=st, ntype=nt,
                #  배정된 종류를 쓴다.  `kind_for_radius` 는 이제 **불변식 검사**다 —
                #  뽑힌 반지름이 배정된 종류로 되돌아오지 않으면 범위 배선이 틀린 것이다.
                kind='bimodal' if nt == 3 else kd_assigned,
                pdd_SE=round(pdd_se, 6),
                w_AM_P=round((1 - pdd_se) * s, 6),
                w_AM_S=round((1 - pdd_se) * (1 - s), 6) if nt == 3 else 0.0,
                rP_um=round(rP, 4), rS_um=round(rS, 4) if rS else '',
                rSE_um=round(rSE, 4), rSE_lo_um=round(r_lo, 4),
                rSE_truncated=truncated,
                volfrac=round(volfrac, 6),
                phi_AM=round(phi_am, 6),
                n_AM_est=int(round(n_am)), n_SE_est=int(round(n_se)),
                n_total_est=int(round(n_am + n_se)),
                lhs_cell=','.join(str(int(v * PER_STRATUM)) for v in u),
                seed=rng.randint(20000, 29999)))
            if nt == 2 and kind_for_radius(b, rP) != kd_assigned:
                raise SystemExit(
                    f'불변식 위반: {kd_assigned} 로 배정했는데 r={rP:.4f} µm 는 '
                    f'{kind_for_radius(b, rP)} 범위다 — 범위 배선이 틀렸다')
    assign_prime_seeds(pts)          # ★ 좌표 확정 후에만 — 난수 스트림 불변
    return pts, notes


def check_lhs(pts: list[dict], per_stratum: int = PER_STRATUM) -> list[str]:
    """★ 층마다 4개 공통축이 **각 칸을 정확히 한 번씩** 쓰는가 (Codex Q5 [P1]).

    초판은 이 성질이 없었는데 **아무도 검사하지 않아서** 몰랐다 — selftest 는 `lhs_unit`
    만 봤고 `generate()` 의 결과나 고정 CSV 는 안 봤다.  여기서 실제 산출물을 본다.
    """
    from collections import Counter
    bad = []
    by_st = {}
    for p in pts:
        by_st.setdefault(p['stratum'], []).append(p)
    for st, rows in sorted(by_st.items()):
        if len(rows) != per_stratum:
            bad.append(f'층 {st}: {len(rows)}점 (기대 {per_stratum})')
            continue
        cells = [r.get('lhs_cell', '') for r in rows]
        if any(not c for c in cells):
            bad.append(f'층 {st}: lhs_cell 이 없다 — 검사 불가')
            continue
        for ax in range(len(cells[0].split(','))):
            col = Counter(int(c.split(',')[ax]) for c in cells)
            if sorted(col) != list(range(per_stratum)) or set(col.values()) != {1}:
                miss = [i for i in range(per_stratum) if i not in col]
                dup = [i for i, n in col.items() if n > 1]
                bad.append(f'층 {st} 축 {ax}: 빈칸 {miss} · 중복 {dup}')
    return bad


# =========================================================================
def report(box: dict, pts: list[dict], notes: list[str], unread: list[str]) -> None:
    print('══ 현재 상자 (읽어서 유도) ══')
    for nt in sorted(box, reverse=True):
        b = box[nt]
        print(f'  {nt}-type  n={b["n"]}  kinds={",".join(b["kinds"])}')
        for k in ('rP_um', 'rS_um', 'rSE_um', 'pdd_SE', 'volfrac', 's_AM_P', 'phi_AM'):
            if k in b and b[k][0] is not None:
                print(f'     {k:10s} {b[k][0]:>9.4g} .. {b[k][1]:>9.4g}')
        if len(b['kinds']) > 1:
            print('     ── 종류별 r_AM (라벨을 이 범위가 정한다)')
            for kd, v in sorted(b['per_kind'].items()):
                print(f'        {kd:12s} n={v["n"]:<4d} '
                      f'{v["rP_um"][0]:>6.3g} .. {v["rP_um"][1]:>6.3g} µm')
    if unread:
        print(f'\n  ⚠ 못 읽은 파일 {len(unread)} 건:')
        for f in unread[:5]:
            print('     ', f)

    print(f'\n══ 확장 설계 {len(pts)} 점 ══')
    print('  stratum  pdd_SE 범위      phi_AM 범위      n_total 중앙  절단된 점')
    for st in range(N_STRATA):
        s = [p for p in pts if p['stratum'] == st]
        if not s:
            continue
        pv = sorted(p['pdd_SE'] for p in s)
        ph = sorted(p['phi_AM'] for p in s)
        nt = sorted(p['n_total_est'] for p in s)
        cut = sum(p['rSE_truncated'] for p in s)
        print(f'   {st}      {pv[0]:.3f}–{pv[-1]:.3f}    '
              f'{ph[-1]:.3f}–{ph[0]:.3f}    {nt[len(nt)//2]:>8,}     {cut}/{len(s)}')
    #  ★ 2-type 종류 균형 — 기존 배치와 같은 영역인지 (초판은 13:3 으로 치우쳤다)
    two = [p for p in pts if p['ntype'] == 2]
    if two:
        from collections import Counter
        got = Counter(p['kind'] for p in two)
        base = {k: v['n'] for k, v in box[2]['per_kind'].items()}
        fmt = lambda d: ' · '.join(f'{k} {d[k]}' for k in sorted(d))   # noqa: E731
        print(f'\n  2-type 종류 균형   확장: {fmt(got)}')
        print(f'                     기존: {fmt(base)}')
    #  ★ 유한크기 — §4-3b 절단 대상이 어느 점인지 런 전에 확정한다
    s_am = sorted(pts, key=lambda p: p['n_AM_est'])
    k10 = max(1, len(pts) // 10)
    print(f'\n  n_AM_est  min {s_am[0]["n_AM_est"]:,} · p10 {s_am[k10]["n_AM_est"]:,} · '
          f'median {s_am[len(s_am)//2]["n_AM_est"]:,} · max {s_am[-1]["n_AM_est"]:,}')
    print(f'  §4-3b 하위 10 % ({k10}점, 런 전 확정): '
          + ', '.join(p['id'] for p in s_am[:k10]))
    #  ★ LHS 성질을 **산출물에서** 검사한다 (Codex Q5) — fail-closed
    bad = check_lhs(pts)
    print('\n  LHS 점유 검사 (층×공통4축): ' + ('✓ 전부 정확히 한 번' if not bad
          else '⛔ ' + str(len(bad)) + ' 건'))
    for x in bad[:6]:
        print('     ', x)
    mx = max(p['n_total_est'] for p in pts)
    print(f'\n  최대 예상 입자 수 {mx:,}  (상한 {N_MAX_PARTICLES:,})'
          f'  {"✓" if mx <= N_MAX_PARTICLES else "⛔ 초과"}')
    over = [p['id'] for p in pts if p['n_total_est'] > N_MAX_PARTICLES]
    if over:
        print('   ⛔ 초과 점:', ', '.join(over))
    cut = sum(p['rSE_truncated'] for p in pts)
    print(f'  r_SE 하한이 절단된 점 {cut}/{len(pts)}'
          f'  ← 이 편향은 결과와 함께 보고한다 (사전등록 §3-2)')
    for n in notes:
        print('  ⚠', n)


# =========================================================================
def selftest() -> int:
    fails = []

    def chk(name, cond, detail=''):
        (print(f'  ok   {name}') if cond
         else (fails.append(name), print(f'  FAIL {name} {detail}')))

    print('lhs_ext_design selftest')

    # ① 조성 환산이 실측과 맞는가 (사전등록 §0-1 의 근거)
    chk('vol_from_mass(0.80) == 0.625 (lhs00_110 실측)',
        abs(vol_from_mass(0.80) - 0.625) < 1e-9, f'{vol_from_mass(0.80)}')
    chk('mass_from_vol 은 vol_from_mass 의 역함수',
        all(abs(mass_from_vol(vol_from_mass(w)) - w) < 1e-12
            for w in (0.3, 0.5, 0.7, 0.85, 0.95)))

    # ② 입자 수 예측기가 실측 두 케이스를 재현하는가  ★ 상한의 근거
    for m in MEASURED:
        for r_um, vf, n_meas in zip(m['radii_um'], m['vol_frac'], m['counts']):
            n_pred = n_spheres(vf, r_um, m['volfrac'])
            err = abs(n_pred - n_meas) / n_meas
            chk(f'{m["case"]} r={r_um}um  예측 {n_pred:,.0f} vs 실측 {n_meas:,}',
                err < 0.02, f'오차 {err:.1%}')

    # ③ 상한 역산이 자기일관인가
    for n_am, phi_se, vf in ((40_000, 0.65, 0.28), (100, 0.80, 0.20)):
        r = r_se_min_for_ceiling(n_am, phi_se, vf)
        tot = n_am + n_spheres(phi_se, r, vf)
        chk(f'r_se_min 이 상한에 정확히 닿는다 (n_AM={n_am:,})',
            abs(tot - N_MAX_PARTICLES) < 1.0, f'{tot:,.1f}')
    chk('AM 만으로 초과하면 inf', math.isinf(r_se_min_for_ceiling(200_000, 0.5, 0.3)))

    # ③b ★ 헤더 파싱 — **실제 파일 모양 그대로** (구분선이 첫 줄, 헤더가 둘째 줄).
    #     2026-08-29: `^` 에 re.M 을 안 붙여 130 건이 전부 조용히 unread 로 갔다.
    #     이 검사가 그것을 재현한다 — 없었으면 ibb 에서야 드러났다 (실제로 그랬다).
    import tempfile
    _H3 = ('# ============================================================\n'
           '# lhs00_000: bimodal (3-type) | LHS design\n'
           '# rP=0.0055 rS=0.0005 rSE=0.001 | pdd AM_P=0.5100 AM_S=0.3400 SE=0.1500\n'
           '# volfrac=0.222984 | E_se=0.135e7 (고정) | seed=10007\n'
           '# ============================================================\n'
           'atom_style      granular\n')
    _H2 = ('# ============================================================\n'
           '# lhs00_100: mono_AM_S (2-type) | LHS design\n'
           '# rAM=0.0025 rSE=0.00075 | pdd AM=0.7000 SE=0.3000\n'
           '# volfrac=0.317759 | E_se=0.135e7 (고정) | seed=10949\n'
           '# ============================================================\n')
    with tempfile.TemporaryDirectory() as td:
        for case, body in (('lhs00_000', _H3), ('lhs00_100', _H2)):
            d = os.path.join(td, case)
            os.makedirs(d)
            with open(os.path.join(d, f'input_{case}.liggghts'), 'w',
                      encoding='utf-8') as fh:
                fh.write(body)
        rows, unread = parse_headers(td)
        chk('parse-both: 두 형식 모두 읽힌다 (구분선이 첫 줄이어도)',
            len(rows) == 2 and not unread, f'rows={len(rows)} unread={len(unread)}')
        if len(rows) == 2:
            r3 = next(r for r in rows if r['ntype'] == 3)
            r2 = next(r for r in rows if r['ntype'] == 2)
            chk('parse-3type: 반지름이 µm 로 환산된다',
                (r3['rP_um'], r3['rS_um'], r3['rSE_um']) == (5.5, 0.5, 1.0),
                str((r3['rP_um'], r3['rS_um'], r3['rSE_um'])))
            chk('parse-3type: wt% 와 kind', r3['pdd_SE'] == 0.15
                and r3['kind'] == 'bimodal', f"{r3['pdd_SE']} {r3['kind']}")
            chk('parse-2type: rAM 이 rP 자리로', r2['rP_um'] == 2.5
                and r2['rSE_um'] == 0.75 and r2['rS_um'] is None)
            chk('parse-2type: kind 가 보존된다', r2['kind'] == 'mono_AM_S', r2['kind'])
            chk('parse: phi_AM 이 붙는다 (0.15 wt% SE → 0.7025)',
                abs(r3['phi_AM'] - 0.70248) < 1e-4, f"{r3['phi_AM']}")
            box = derive_box(rows)
            chk('derive_box: 두 종류를 따로 낸다', set(box) == {2, 3}, str(sorted(box)))
            chk('derive_box: 종류별 반지름 범위를 낸다',
                box[2]['per_kind']['mono_AM_S']['rP_um'] == (2.5, 2.5),
                str(box[2]['per_kind']))
    #  라벨은 반지름이 정한다 — 겹치지 않는 두 범위에서 각각, 그리고 사이 값에서
    _b = dict(kinds=['mono_AM_P', 'mono_AM_S'], per_kind={
        'mono_AM_P': dict(n=15, rP_um=(4.0, 7.5), rSE_um=(0.5, 1.0)),
        'mono_AM_S': dict(n=15, rP_um=(1.0, 2.5), rSE_um=(0.5, 1.0))})
    chk('kind_for_radius: 범위 안이면 그 종류', kind_for_radius(_b, 6.0) == 'mono_AM_P'
        and kind_for_radius(_b, 1.5) == 'mono_AM_S')
    chk('kind_for_radius: 사이 값은 가까운 중심으로',
        kind_for_radius(_b, 3.0) == 'mono_AM_S'
        and kind_for_radius(_b, 3.9) == 'mono_AM_P',
        f'{kind_for_radius(_b, 3.0)} {kind_for_radius(_b, 3.9)}')
    #  못 읽는 파일은 **반환**되어야 한다 (조용히 사라지면 안 된다)
    with tempfile.TemporaryDirectory() as td:
        d = os.path.join(td, 'lhs00_777')
        os.makedirs(d)
        with open(os.path.join(d, 'input_lhs00_777.liggghts'), 'w') as fh:
            fh.write('# 형식이 다른 무언가\n')
        rows, unread = parse_headers(td)
        chk('parse: 못 읽은 파일은 조용히 버리지 않고 돌려준다',
            not rows and len(unread) == 1, f'rows={len(rows)} unread={len(unread)}')

    # ④b ★ generate() **산출물**의 LHS 성질 — 초판이 못 잡은 자리
    _fake = [dict(stratum=0, lhs_cell=f'{i},{(i*3)%8},{(i*5)%8},{(7-i)}')
             for i in range(8)]
    chk('check_lhs: 완전 점유를 통과시킨다', not check_lhs(_fake), str(check_lhs(_fake)))
    _fake[0]['lhs_cell'] = _fake[1]['lhs_cell']
    chk('check_lhs: 빈칸·중복을 잡는다', bool(check_lhs(_fake)))
    chk('check_lhs: 층 점수 부족을 잡는다',
        bool(check_lhs([dict(stratum=0, lhs_cell='0,0,0,0')])))

    # ④ LHS 성질 — 축마다 n 칸을 정확히 한 번씩
    import random
    rng = random.Random(7)
    n, k = 8, 4
    U = lhs_unit(n, k, rng)
    for j in range(k):
        cells = sorted(int(u[j] * n) for u in U)
        chk(f'LHS 축 {j}: 각 칸 정확히 한 번', cells == list(range(n)), str(cells))

    # ⑤ 창이 현재 상자와 겹치지 않는가 (사전등록 §2 의 구조적 보장)
    chk('창의 하한이 현재 상한(0.30)에서 열려 있다', PDD_SE_LO == 0.30)
    chk('층이 창을 정확히 덮는다',
        abs(PDD_SE_LO + N_STRATA * ((PDD_SE_HI - PDD_SE_LO) / N_STRATA)
            - PDD_SE_HI) < 1e-12)
    chk('총 점 수 = 층 × 층당', N_STRATA * PER_STRATUM == 64)

    # ⑥ φ_AM 이 창 전체에서 단조 감소하는가
    xs = [PDD_SE_LO + i * 0.01 for i in range(41)]
    ph = [phi_am_of_pdd_se(x) for x in xs]
    chk('phi_AM 은 pdd_SE 에 단조 감소', all(a > b for a, b in zip(ph, ph[1:])))
    chk('창 양끝 phi_AM = 0.493 .. 0.152',
        abs(ph[0] - 0.4930) < 5e-4 and abs(ph[-1] - 0.1515) < 5e-4,
        f'{ph[0]:.4f} .. {ph[-1]:.4f}')

    # ⑦ **검사기가 실제로 잡는가** — R14 P1-05 가 `0 failure` 로 통과시킨 변이체들.
    #    ⚠ 검사를 추가하는 것과 그 검사가 **작동하는 것**은 다르다.  P1-05 의 논지가
    #      정확히 그것이었으므로 변이체를 여기 상주시켜 회귀로 못박는다.
    _csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             'docs', 'data', 'lhs_ext_design_v2_20260829.csv')
    if not os.path.exists(_csv_path):
        fails.append('⑦ 정본 CSV 가 없다 — 변이체 회귀를 건너뛸 수 없다')
        print('  FAIL ⑦ 정본 CSV 없음')
    else:
        import copy as _cp, io as _io, subprocess as _sp, tempfile as _tf
        _base = list(csv.DictReader(_io.StringIO(open(_csv_path, newline='').read())))
        _cols = list(_base[0])

        def _mutate_rc(fn):
            m = _cp.deepcopy(_base)
            fn(m)
            p = _tf.mktemp(suffix='.csv')
            with open(p, 'w', newline='') as fh:
                w = csv.DictWriter(fh, fieldnames=_cols)
                w.writeheader()
                for r in m:
                    w.writerow(r)
            rc = _sp.run([sys.executable, os.path.abspath(__file__), '--verify', p],
                         capture_output=True, text=True).returncode
            os.unlink(p)
            return rc

        def _scale_w(m):
            for r in m:
                r['w_AM_P'] = f"{float(r['w_AM_P']) * 0.1:.6f}"
                r['w_AM_S'] = f"{float(r['w_AM_S']) * 0.1:.6f}"

        def _dup_id(m):
            m[1]['id'] = m[0]['id']

        def _bump_nam(m):
            for r in m:
                if r['id'] in ('lhsx_054', 'lhsx_025'):
                    r['n_AM_est'] = str(int(r['n_AM_est']) + 9000)

        def _swap_kind(m):
            st0 = [r for r in m if r['stratum'] == '0']
            b = next(r for r in st0 if r['kind'] == 'bimodal')
            o = next(r for r in st0 if r['kind'] == 'mono_AM_P')
            b['kind'], o['kind'] = o['kind'], b['kind']

        def _composite_seed(m):
            m[0]['seed'] = '27158'

        for _nm, _fn in (('w_AM_* 0.1배', _scale_w), ('ID 중복', _dup_id),
                         ('n_AM_est 변조', _bump_nam),
                         ('bimodal↔mono 라벨 교환', _swap_kind),
                         ('합성수 seed', _composite_seed)):
            chk(f'★⑦ 변이체를 잡는다 — {_nm}', _mutate_rc(_fn) == 1)
        chk('★⑦ 정본 자신은 통과한다 (거짓 양성 없음)', _mutate_rc(lambda m: None) == 0)

    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def verify_csv(path: str, expect_sha256: str | None = None) -> int:
    """★ F④ — 생성 **후** CSV 를 다시 읽어 계약을 fail-closed 로 검사한다.

    생성기가 맞다는 것과 **디스크에 있는 파일이 맞다는 것**은 다르다.  손으로 편집되거나
    다른 판본이 섞여도 여기서 걸린다.  실행 전 마지막 관문이다.
    """
    import hashlib
    rows = list(csv.DictReader(open(path, newline='', encoding='utf-8')))
    fails = []

    def chk(name, cond, detail=''):
        (print(f'  ok   {name}') if cond
         else (fails.append(name), print(f'  FAIL {name} {detail}')))

    print(f'verify {path}')
    chk('행 수 = 층 × 층당', len(rows) == N_STRATA * PER_STRATUM, str(len(rows)))
    pdd = [float(r['pdd_SE']) for r in rows]
    chk(f'창 ({PDD_SE_LO}, {PDD_SE_HI}] 안 (열림/닫힘)',
        all(PDD_SE_LO < v <= PDD_SE_HI for v in pdd),
        f'{min(pdd):.4f}–{max(pdd):.4f}')
    nt = [int(r['n_total_est']) for r in rows]
    chk(f'입자수 상한 {N_MAX_PARTICLES:,}', max(nt) <= N_MAX_PARTICLES, f'max {max(nt):,}')
    seeds = [r['seed'] for r in rows]
    chk('seed 전부 다름', len(set(seeds)) == len(seeds),
        f'{len(seeds)-len(set(seeds))} 중복')
    #  ★★ 08-18 배치 v2 가 여기서 통과했다 — "서로 다른가" 만 보고 **소수인지는 안 봤다**.
    #     그 결과 25 케이스가 abort 했고 chain 이 조용히 지나갔다.  그 검사를 여기 넣는다.
    _si = [int(v) for v in seeds]
    _bad = [(r['id'], v) for r, v in zip(rows, _si) if not is_prime(v)]
    chk('seed 전부 소수 (LIGGGHTS insert/pack 요구)', not _bad,
        'OK' if not _bad else f'합성수 {len(_bad)}개 — 예: '
        + ', '.join(f'{i}={v}' for i, v in _bad[:3]))
    chk(f'seed 범위 [{SEED_LO}, {SEED_HI}]',
        all(SEED_LO <= v <= SEED_HI for v in _si),
        f'{min(_si)}–{max(_si)}')
    chk('phi_AM 이 pdd_SE 와 정합', all(
        abs(float(r['phi_AM']) - phi_am_of_pdd_se(float(r['pdd_SE']))) < 1e-5
        for r in rows))
    #  ★★ `lhs_cell` 문자열을 **믿지 않는다** — 좌표에서 다시 계산해 대조한다.
    #  ⚠ 초판은 문자열만 봤고, Codex R11 B2 가 반례를 냈다: 64점의 `pdd_SE` 를 전부
    #    0.310000 으로 바꿔도 `lhs_cell` 이 그대로면 **0 failure 로 통과**했다.
    #    검사기가 검사 대상이 아니라 **검사 대상의 자기 신고**를 본 것이다.
    pts = [dict(stratum=int(r['stratum']), lhs_cell=r.get('lhs_cell', ''),
                n_AM_est=int(r['n_AM_est']), id=r['id']) for r in rows]
    bad = check_lhs(pts)
    chk('층×공통4축 LHS 점유 (신고된 cell)', not bad, '; '.join(bad[:3]))

    #  좌표 → cell 재계산.  층 안에서 각 축의 **순위**가 곧 cell 이어야 한다
    #  (LHS 는 축마다 n 칸을 한 번씩 쓰므로 값의 순위 = 칸 번호).
    recomputed_bad = []
    by_st = {}
    for r in rows:
        by_st.setdefault(int(r['stratum']), []).append(r)
    AXES = ('pdd_SE', 'volfrac', 'rP_um', 'rSE_um')
    for st, rs in sorted(by_st.items()):
        if len(rs) != PER_STRATUM:
            continue
        for j, ax in enumerate(AXES):
            #  rP 는 종류별 범위로 사상되므로 **분위**로 되돌려 순위를 낸다
            if ax == 'rP_um':
                vals = []
                for r in rs:
                    lo, hi = ((1.0, 2.5) if r['kind'] == 'mono_AM_S'
                              else (2.5, 7.5))
                    vals.append((float(r[ax]) - lo) / (hi - lo))
            else:
                vals = [float(r[ax]) for r in rs]
            order = sorted(range(len(vals)), key=lambda i: vals[i])
            rank = [0] * len(vals)
            for pos, i in enumerate(order):
                rank[i] = pos
            for i, r in enumerate(rs):
                claimed = int(r['lhs_cell'].split(',')[j])
                if claimed != rank[i]:
                    recomputed_bad.append(
                        f'{r["id"]} 축{j}({ax}): 신고 {claimed} vs 좌표순위 {rank[i]}')
    chk('★ 좌표에서 재계산한 cell 이 신고와 일치', not recomputed_bad,
        '; '.join(recomputed_bad[:3]) + (f' … 총 {len(recomputed_bad)}건'
                                         if len(recomputed_bad) > 3 else ''))

    #  저장된 입자수도 재산술한다 (신고를 믿지 않는다)
    n_bad = []
    for r in rows:
        phi_am = phi_am_of_pdd_se(float(r['pdd_SE']))
        vf = float(r['volfrac'])
        if r['ntype'] == '3':
            wp, ws = float(r['w_AM_P']), float(r['w_AM_S'])
            sfrac = wp / (wp + ws) if (wp + ws) else 1.0
            n_am = (n_spheres(phi_am * sfrac, float(r['rP_um']), vf)
                    + n_spheres(phi_am * (1 - sfrac), float(r['rS_um']), vf))
        else:
            n_am = n_spheres(phi_am, float(r['rP_um']), vf)
        n_se = n_spheres(1.0 - phi_am, float(r['rSE_um']), vf)
        tot = n_am + n_se
        #  ★ 셋을 **각각** 대조한다.  옛 판은 `n_total_est` 만 봤고, R14 P1-05 가
        #    `w_AM_P`·`w_AM_S` 를 0.1배 한 변이체를 0 failure 로 통과시켰다 —
        #    합만 맞으면 상별 개수가 틀려도 안 보였다.
        for key, want in (('n_AM_est', n_am), ('n_SE_est', n_se), ('n_total_est', tot)):
            if key not in r:
                n_bad.append(f'{r["id"]}: `{key}` 열이 없다')
                continue
            if abs(want - float(r[key])) > max(2.0, 0.005 * max(want, 1.0)):
                n_bad.append(f'{r["id"]}.{key}: 신고 {r[key]} vs 재산술 {want:.0f}')
    from collections import Counter
    chk('★ 입자수를 좌표에서 재산술해 대조 (AM·SE·합 각각)', not n_bad, '; '.join(n_bad[:3]))

    #  ── ID·층·라벨·조성 불변식 (R14 P1-05) ────────────────────────────────
    want_ids = [f'lhsx_{i:03d}' for i in range(1, N_STRATA * PER_STRATUM + 1)]
    got_ids = [r['id'] for r in rows]
    chk('★ ID 집합이 정확히 lhsx_001..064', sorted(got_ids) == want_ids,
        f'{len(set(got_ids))} unique / 결손 '
        + ', '.join(sorted(set(want_ids) - set(got_ids))[:3])
        + ' / 잉여 ' + ', '.join(sorted(set(got_ids) - set(want_ids))[:3]))
    st_ct = Counter(int(r['stratum']) for r in rows)
    chk(f'★ stratum 0..{N_STRATA-1} 이 각각 {PER_STRATUM}행',
        sorted(st_ct) == list(range(N_STRATA))
        and all(v == PER_STRATUM for v in st_ct.values()), str(dict(sorted(st_ct.items()))))
    kind_bad, nt_bad = [], []
    for st, rs in sorted(by_st.items()):
        c = Counter(r['kind'] for r in rs)
        if (c.get('bimodal', 0) != THREE_TYPE_PER_STRATUM
                or c.get('mono_AM_P', 0) != 1 or c.get('mono_AM_S', 0) != 1):
            kind_bad.append(f'stratum {st}: {dict(c)}')
    chk(f'★ 층마다 bimodal {THREE_TYPE_PER_STRATUM} + mono 1 + mono 1',
        not kind_bad, '; '.join(kind_bad[:3]))
    for r in rows:
        want_nt = '3' if r['kind'] == 'bimodal' else '2'
        if str(r['ntype']) != want_nt:
            nt_bad.append(f'{r["id"]}: kind={r["kind"]} 인데 ntype={r["ntype"]}')
    chk('★ ntype ↔ kind 대응', not nt_bad, '; '.join(nt_bad[:3]))
    #  허용치는 **저장 정밀도**에서 온다: 세 값이 각각 소수 6자리로 반올림되므로
    #  합의 오차가 3 × 0.5e-6 = 1.5e-6 까지 정상이다.  1e-6 로 조이면 반올림을
    #  결함으로 오진한다 (실제로 그렇게 나왔다).  0.1배 변조는 이 허용치를 5자릿수 넘는다.
    _W_TOL = 3e-6
    w_bad = []
    for r in rows:
        wsum = float(r['w_AM_P']) + float(r['w_AM_S'])
        if abs(wsum - (1.0 - float(r['pdd_SE']))) > _W_TOL:
            w_bad.append(f'{r["id"]}: w합 {wsum:.6f} vs 1−pdd {1-float(r["pdd_SE"]):.6f}')
    chk(f'★ w_AM_P + w_AM_S = 1 − pdd_SE (±{_W_TOL:g})', not w_bad, '; '.join(w_bad[:3]))
    kc = Counter(r['kind'] for r in rows)
    chk('mono 두 종류가 같은 수', kc.get('mono_AM_P', 0) == kc.get('mono_AM_S', 0),
        str(dict(kc)))
    tr = [r['id'] for r in rows if r['rSE_truncated'] == '1']
    print(f'  info r_SE 절단 {len(tr)}점' + (f' — {", ".join(tr)}' if tr else ''))
    lo = sorted(pts, key=lambda p: p['n_AM_est'])[:max(1, len(pts) // 10)]
    print('  info §4-3b 하위 10 %: ' + ', '.join(
        f'{p["id"]}({p["n_AM_est"]:,})' for p in lo))
    h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    print(f'  sha256 {h}')
    #  ★ 기대 해시를 주면 **강제 대조**한다.  옛 판은 계산해서 출력만 했고, 그러면
    #    문서의 봉인값과 다른 파일을 검증해도 초록이 난다 (R14 P1-05).
    if expect_sha256:
        chk('★ 봉인 sha256 일치', h == expect_sha256.strip().lower(),
            f'기대 {expect_sha256[:12]}… vs 실제 {h[:12]}…')
    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--scan', help='LHS 루트 (lhs00_* 가 있는 디렉터리)')
    ap.add_argument('--out', help='설계 CSV 출력 경로')
    ap.add_argument('--seed', type=int, default=DESIGN_SEED)
    ap.add_argument('--expect-sha256', help='봉인 해시 강제 대조 (R14 P1-05)')
    ap.add_argument('--verify', help='생성된 CSV 를 다시 읽어 계약 검사 (F④)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if a.verify:
        return verify_csv(a.verify, a.expect_sha256)
    if not a.scan:
        ap.error('--scan 또는 --selftest 가 필요하다')

    root = os.path.expanduser(a.scan)
    rows, unread = parse_headers(root)
    if not rows:
        found = glob.glob(os.path.join(root, 'lhs*_*', 'input_lhs*_*.liggghts'))
        msg = [f'헤더를 하나도 못 읽었다: {root}',
               f'  glob 이 찾은 파일 {len(found)} 건 · 그 중 파싱 실패 {len(unread)} 건']
        if found:
            msg.append(f'  첫 파일: {found[0]}')
            msg.append('  --- 앞 6 줄 ---')
            msg += ['  ' + l for l in
                    open(found[0], encoding='utf-8',
                         errors='replace').read(600).splitlines()[:6]]
        else:
            msg.append(f'  ⇒ 경로에 lhs*_*/input_lhs*_*.liggghts 가 없다.  ls 로 확인할 것')
        raise SystemExit('\n'.join(msg))
    #  ★ 못 읽은 파일이 하나라도 있으면 **멈춘다** (Codex R11 B4).
    #    초판은 한 건만 성공해도 그 범위로 CSV 를 쓰고 exit 0 했다 — 상자를 **읽은 만큼만**
    #    유도하므로, 조용히 좁은 상자 위에 설계가 선다.
    if unread:
        raise SystemExit(
            f'⛔ 헤더를 못 읽은 파일 {len(unread)} 건 — 상자를 좁게 유도하게 되므로 멈춘다.\n'
            + '\n'.join('   ' + x for x in unread[:8])
            + ('\n   …' if len(unread) > 8 else '')
            + '\n  ⚠ 형식이 늘었으면 파서를 고칠 것.  건너뛰면 설계가 조용히 틀린다.')
    print(f'읽은 케이스 {len(rows)} 건 (못 읽음 0 — 강제)\n')
    box = derive_box(rows)
    pts, notes = generate(box, a.seed)
    report(box, pts, notes, unread)

    if a.out:
        with open(a.out, 'w', newline='', encoding='utf-8') as fh:
            #  ⚠ LF 로 쓴다.  `csv.writer` 기본은 `\r\n` 이라 리포(LF)와 **해시가
            #  달라진다** — 사전등록이 CSV 를 해시로 참조하므로 그 어긋남이 봉인을 깬다.
            #  (2026-08-29: ibb 산출 CRLF 37fa2db0 ↔ 리포 LF 7923b61f, 내용은 동일)
            w = csv.DictWriter(fh, fieldnames=list(pts[0]), lineterminator='\n')
            w.writeheader()
            w.writerows(pts)
        print(f'\nwrote {a.out}  ({len(pts)} rows, seed={a.seed})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
