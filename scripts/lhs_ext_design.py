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

  ③ **상한을 기각재추출이 아니라 `r_SE` 구간 절단으로 건다.**  기각재추출은 층화를
     깨고 편향을 보이지 않게 만든다.  입자 수는 r_SE 가 지배하므로 (N_SE ∝ r_SE⁻³),
     각 점에서 상한을 만족하는 최소 r_SE 를 **해석적으로** 풀어 그 위에서만 뽑는다.
     ⇒ 절단은 CSV 에 `rSE_lo_um` 로 남고, 편향이 보고 가능한 형태로 드러난다.

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
_RE_KIND = re.compile(r'^#\s*(lhs\d+_\d+):\s*(\S+)')
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
        box[nt] = b
    return box


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
        for nt, cnt in ((3, THREE_TYPE_PER_STRATUM),
                        (2, PER_STRATUM - THREE_TYPE_PER_STRATUM)):
            b = box[nt]
            k = 5 if nt == 3 else 3          # pdd_SE, rP, rSE, volfrac (+rS, s)
            k = 6 if nt == 3 else 4
            U = lhs_unit(cnt, k, rng)
            for u in U:
                pdd_se = _scale(u[0], lo, hi)
                phi_se = 1.0 - phi_am_of_pdd_se(pdd_se)
                volfrac = _scale(u[1], *b['volfrac'])
                rP = _scale(u[2], *b['rP_um'])
                if nt == 3:
                    rS = _scale(u[3], *b['rS_um'])
                    s = _scale(u[4], *b['s_AM_P'])
                    ui_rse = u[5]
                else:
                    rS, s, ui_rse = None, 1.0, u[3]

                # AM 입자 수는 r_SE 와 무관 → 먼저 확정한다
                phi_am = 1.0 - phi_se
                if nt == 3:
                    # 질량 분할 s 를 부피 분할로 옮긴다 (두 AM 은 밀도가 같다)
                    n_am = (n_spheres(phi_am * s, rP, volfrac)
                            + n_spheres(phi_am * (1 - s), rS, volfrac))
                else:
                    n_am = n_spheres(phi_am, rP, volfrac)

                r_lo_ceiling = r_se_min_for_ceiling(n_am, phi_se, volfrac)
                r_lo = max(b['rSE_um'][0], r_lo_ceiling)
                r_hi = b['rSE_um'][1]
                if not math.isfinite(r_lo) or r_lo > r_hi:
                    notes.append(f'stratum {st} nt{nt}: AM 만으로 상한 초과 → 점 재추출 필요 '
                                 f'(rP={rP:.2f} vf={volfrac:.3f})')
                    r_lo = r_hi                       # 상한 반지름으로 눌러 담는다
                rSE = _scale(ui_rse, r_lo, r_hi)

                n_se = n_spheres(phi_se, rSE, volfrac)
                idx += 1
                pts.append(dict(
                    id=f'lhsx_{idx:03d}', stratum=st, ntype=nt,
                    kind='bimodal' if nt == 3 else 'mono_AM',
                    pdd_SE=round(pdd_se, 6),
                    w_AM_P=round((1 - pdd_se) * s, 6),
                    w_AM_S=round((1 - pdd_se) * (1 - s), 6) if nt == 3 else 0.0,
                    rP_um=round(rP, 4), rS_um=round(rS, 4) if rS else '',
                    rSE_um=round(rSE, 4), rSE_lo_um=round(r_lo, 4),
                    rSE_truncated=int(r_lo > b['rSE_um'][0] + 1e-12),
                    volfrac=round(volfrac, 6),
                    phi_AM=round(phi_am, 6),
                    n_AM_est=int(round(n_am)), n_SE_est=int(round(n_se)),
                    n_total_est=int(round(n_am + n_se)),
                    seed=rng.randint(20000, 29999)))
    return pts, notes


# =========================================================================
def report(box: dict, pts: list[dict], notes: list[str], unread: list[str]) -> None:
    print('══ 현재 상자 (읽어서 유도) ══')
    for nt in sorted(box, reverse=True):
        b = box[nt]
        print(f'  {nt}-type  n={b["n"]}  kinds={",".join(b["kinds"])}')
        for k in ('rP_um', 'rS_um', 'rSE_um', 'pdd_SE', 'volfrac', 's_AM_P', 'phi_AM'):
            if k in b and b[k][0] is not None:
                print(f'     {k:10s} {b[k][0]:>9.4g} .. {b[k][1]:>9.4g}')
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

    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--scan', help='LHS 루트 (lhs00_* 가 있는 디렉터리)')
    ap.add_argument('--out', help='설계 CSV 출력 경로')
    ap.add_argument('--seed', type=int, default=DESIGN_SEED)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.scan:
        ap.error('--scan 또는 --selftest 가 필요하다')

    rows, unread = parse_headers(os.path.expanduser(a.scan))
    if not rows:
        raise SystemExit(f'헤더를 하나도 못 읽었다: {a.scan}')
    print(f'읽은 케이스 {len(rows)} 건 (못 읽음 {len(unread)})\n')
    box = derive_box(rows)
    pts, notes = generate(box, a.seed)
    report(box, pts, notes, unread)

    if a.out:
        with open(a.out, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(pts[0]))
            w.writeheader()
            w.writerows(pts)
        print(f'\nwrote {a.out}  ({len(pts)} rows, seed={a.seed})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
