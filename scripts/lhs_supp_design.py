#!/usr/bin/env python3
"""LHS 보충 침대 (#3 · 설계 공간 빈 곳) + 후막 짝 (#4 · 6 · 8 mAh/cm²) 설계 — 1저자 결정 2026-10-06 밤.

    python3 scripts/lhs_supp_design.py --out docs/data/lhs_supp_design_20261006.csv \\
                                       --report docs/data/lhs_supp_design_20261006.json
    python3 scripts/lhs_supp_design.py --verify <CSV> --expect-sha256 <sha>   # lhs_ext_materialize --points 가 부른다
    python3 scripts/lhs_supp_design.py --selftest

계기 (ML 담당 피드백 10-05 · 1저자 정리 10-06):
  ③ 설계 공간 (큰 AM 비율 · SE 함량 wt% · SE 지름) 에 빈 곳이 있다 → 보충 침대 20 (2 mAh 규약).
  ④ "후막에서의 파라미터가 면용량 낮을 때와 같은가" → 2 mAh 침대가 이미 있는 조성 넷을 6 · 8 mAh 로 다시 돌린다.

★ 규약 — 새로 만들지 않고 이미 돈 것을 따른다:
  · 덱 = `lhs_ext_materialize` 가 실물 템플릿 (lhs00_000 · lhs00_110) 을 외과적으로 치환 (64 확장과 같은 길).
  · 2 mAh 규칙: volfrac = L / (C · φ_AM,solid) — C 는 lhs00_000 (volfrac 0.222984 · AM 85 wt%) 실측에서 유도하고
    selftest 가 lhs00_110 (0.250627) 과 상자 경계 (0.176428 · 0.317759) 를 다시 낸다.
  · SE > 30 wt% 는 2 mAh 가 삽입 불가 (volfrac > 0.318) — 64 확장처럼 volfrac 를 상자 [0.176428, 0.317759] 안의 설계 축으로 둔다.
  · 후막 = 짝 (2 mAh) 과 **같은 조성 · 반지름 · volfrac** 에서 삽입 영역 높이만 L/2 배 (reg_mix z 위끝) — 새 seed.
    삽입 위끝 2 mAh 0.138 → 6 mAh 0.404 · 8 mAh 0.537 (덱 단위 · ×1000 = µm) · 침강 중력 98.1 에서 자유낙하 ≤ 0.105 s
    = 105 k step < 침강 200 k step.
  · 시뮬 가능 범위 (1저자 10-06 — "반지름을 작게 만드는건 안돼"): SE 지름 ≥ 1.0 µm · 총 입자 수 ≤ 이미 돈 최대 (194 의 n_total_est 최대).
    범위 밖은 채우지 않고 '한계 구역' 비율로 보고한다.
⚠ 계산량은 **추정**이다 — 기준 = lhs00_000 (45,030 입자 · 2.42 M step · 43 h · 1 코어 · 08-29 기록).  다중 코어 효율 0.8 가정.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import lhs_ext_design as X  # noqa: E402  (n_spheres · vol_from_mass · is_prime · next_free_prime · V_INS)

D130 = os.path.join(ROOT, 'docs', 'data', 'lhs_design_20260818.csv')
D64 = os.path.join(ROOT, 'docs', 'data', 'lhsx_design_adapted_20260929.csv')
DESC = os.path.join(ROOT, 'docs', 'data', 'lhs_descriptors_20260919')

DESIGN_SEED = 20261006
N_SUPP = 20
GAP_THR = 0.20                       # 정규화 3 축 거리 — 10-06 보고 (13.3 % → +20 점 ≈ 1.5 %) 와 같은 문턱
D_SE_MIN = 1.0                       # µm — 시뮬 가능 범위
SEED_LO, SEED_HI = 30000, 39999      # 130 (10007–11243) · 64 (20000–29999) 와 겹치지 않는다
VF_LO, VF_HI = 0.176428, 0.317759    # lhs_ext_box_v2 의 volfrac 상자 (= 2 mAh 규칙의 AM 95 · 70 wt%)
SE_SPLIT = 0.30                      # pdd_SE > 0.30 = 64 확장 영역 (volfrac 자유)
R_P = (2.5, 7.5)                     # µm — 130 · 64 상자
R_S = (0.5, 2.5)
R_MONO_S = (1.0, 2.5)                # lhs_ext_box_v2 mono_AM_S
THICK_PARTNERS = (
    ('lhs00_078', 'AM 75 wt% · SE d 2.0 · τ2 3.1 (낮은 굴곡)'),
    ('lhs00_036', 'AM 80 wt% · SE d 1.5 · τ2 5.4'),
    ('lhs00_045', 'AM 85 wt% · SE d 2.0 · τ2 7.8 (중앙)'),
    ('lhs00_008', 'AM 90 wt% · SE d 1.5 · τ2 22 (관통 경계 근처)'),
)
THICK_LOADINGS = (6.0, 8.0)
SLOTS = 60                           # ibb qos cpu-60
REF = dict(case='lhs00_000', n=45030, steps=2_420_000, hours_1core=43.0)
FIXED_STEPS = 500_001                # 침강 200 k + 1 + 안정 200 k + 완화 100 k (압축 루프 밖)
EFF_MPI = 0.8
WALL_TARGET_H = 100.0
MIN_PP = 5000                        # 코어당 입자 하한 — LIGGGHTS 는 코어당 5 k–20 k 에서 잘 확장 (lhs_design_dataset_20260818.md)

COLS = ['id', 'block', 'partner', 'stratum', 'ntype', 'kind', 'pdd_SE', 'w_AM_P', 'w_AM_S', 'rP_um', 'rS_um',
        'rSE_um', 'rSE_lo_um', 'rSE_truncated', 'volfrac', 'loading_rule', 'loading_mAh_cm2', 'ins_scale',
        'phi_AM', 'n_AM_est', 'n_SE_est', 'n_total_est', 'cap_adjust', 'gap_dist', 'lhs_cell', 'seed',
        'ntasks', 'steps_est', 'core_h_est', 'wall_h_est']
_ID = re.compile(r'^(lhss_\d{3}|lhst_\d{3}_\d+m)$')

# lhs00_000 실측 (lhs_ext_design.MEASURED) 에서 유도한 2 mAh 상수
C_LOAD = 2.0 / (0.222984 * X.vol_from_mass(0.85))


def volfrac_for_loading(w_am: float, loading: float = 2.0) -> float:
    return loading / (C_LOAD * X.vol_from_mass(w_am))


def loading_of(w_am: float, volfrac: float) -> float:
    return C_LOAD * volfrac * X.vol_from_mass(w_am)


def counts(pdd_se, w_p, w_s, rP, rS, rSE, ntype, volfrac, ins_scale=1.0):
    """→ (n_AM, n_SE, phi_AM_solid).  ntype 2 = AM 한 종 (rP 자리)."""
    w_am = 1.0 - pdd_se
    phi = X.vol_from_mass(w_am)
    v = X.V_INS * ins_scale
    if ntype == 3:
        n_am = (X.n_spheres(phi * w_p / w_am, rP, volfrac, v) + X.n_spheres(phi * w_s / w_am, rS, volfrac, v))
    else:
        n_am = X.n_spheres(phi, rP, volfrac, v)
    return n_am, X.n_spheres(1.0 - phi, rSE, volfrac, v), phi


# ── 이미 있는 점 ────────────────────────────────────────────────────────────
def load_existing():
    pts = []
    for path, src in ((D130, '130'), (D64, '64')):
        for r in csv.DictReader(open(path, encoding='utf-8')):
            pts.append(dict(id=r['case_id'], src=src, ps=float(r['ps_frac']), se=100.0 - float(r['am_pct']),
                            dse=float(r['d_se_um']), n=float(r['n_total_est'])))
    return pts


def norm(ps, se, dse):
    return (ps, (se - 5.0) / 65.0, (dse - 1.0) / 1.0)


def _d2(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def gap_fraction(points, thr=GAP_THR, n_mc=20000, seed=7, feasible=None):
    rng = random.Random(seed)
    far = tot = 0
    for _ in range(n_mc):
        q = (rng.random(), rng.random(), rng.random())
        if feasible is not None and not feasible(q):
            continue
        tot += 1
        if min(_d2(q, p) for p in points) > thr * thr:
            far += 1
    return far / max(tot, 1), tot


def _best_case_n(ps, se, dse):
    """가장 유리한 반지름 · volfrac 에서의 총 입자 수 (한계 구역 판정)."""
    pdd = se / 100.0
    if pdd <= SE_SPLIT + 1e-12:
        vf = volfrac_for_loading(1.0 - pdd)
    else:
        vf = VF_LO
    w_am = 1.0 - pdd
    if 0.0 < ps < 1.0:
        n_am, n_se, _ = counts(pdd, w_am * ps, w_am * (1 - ps), R_P[1], R_S[1], dse / 2, 3, vf)
    else:
        n_am, n_se, _ = counts(pdd, w_am, 0.0, R_P[1] if ps >= 1 else R_MONO_S[1], 0.0, dse / 2, 2, vf)
    return n_am + n_se


def maximin(existing_xyz, candidates, k):
    chosen = []
    cur = list(existing_xyz)
    dmin = [min(_d2(c[0], p) for p in cur) for c in candidates]
    for _ in range(k):
        i = max(range(len(candidates)), key=lambda j: (dmin[j], -j))
        chosen.append((candidates[i], math.sqrt(dmin[i])))
        x = candidates[i][0]
        dmin = [min(dmin[j], _d2(candidates[j][0], x)) for j in range(len(candidates))]
        dmin[i] = -1.0
    return chosen


def _strata(k, lo, hi, rng):
    cells = list(range(k))
    rng.shuffle(cells)
    return [lo + (hi - lo) * (c + rng.random()) / k for c in cells]


def _cost(n, steps, ntasks):
    core_h = n * steps * REF['hours_1core'] / (REF['n'] * REF['steps'])
    eff = 1.0 if ntasks == 1 else EFF_MPI
    return core_h, core_h / (ntasks * eff)


def _ntasks_for(core_h, lo, hi):
    if core_h <= WALL_TARGET_H:
        return max(lo, 1)
    return int(min(hi, max(lo, math.ceil(core_h / (EFF_MPI * WALL_TARGET_H)))))


def allocate_cores(rows, slots=SLOTS, min_pp=MIN_PP):
    """qos 코어 (60) 를 꽉 채운다 — 1저자 10-06 밤 "10만 넘는것들에 코어 잘 분배해서 60코어 꽉꽉 채워".

    모든 런 1 코어에서 시작해, **추정 벽시계가 가장 긴 런**에 한 코어씩 더한다 (코어당 입자 ≥ min_pp 인 동안).
    결과: 가장 늦게 끝나는 런 (makespan) 이 줄어든다.  ⚠ 효율 0.8 은 가정 (첫 완주 런으로 고친다).
    """
    nt = {r['id']: 1 for r in rows}

    def wall(r, n):
        return float(r['core_h_est']) / (n * (1.0 if n == 1 else EFF_MPI))
    while sum(nt.values()) < slots:
        cand = [r for r in rows if (nt[r['id']] + 1) * min_pp <= float(r['n_total_est'])]
        if not cand:
            break
        r = max(cand, key=lambda r: (wall(r, nt[r['id']]), r['id']))
        nt[r['id']] += 1
    for r in rows:
        r['ntasks'] = nt[r['id']]
        r['wall_h_est'] = round(wall(r, nt[r['id']]), 1)
    return rows


def generate(seed=DESIGN_SEED):
    rng = random.Random(seed)
    ex = load_existing()
    cap = max(p['n'] for p in ex)
    ex_xyz = [norm(p['ps'], p['se'], p['dse']) for p in ex]
    cands = []
    for i in range(21):
        ps = i / 20
        for j in range(27):
            se = 5.0 + 2.5 * j
            for m in range(11):
                dse = round(1.0 + 0.1 * m, 1)
                if dse < D_SE_MIN or _best_case_n(ps, se, dse) > cap:
                    continue
                cands.append((norm(ps, se, dse), (ps, se, dse)))
    picks = maximin(ex_xyz, cands, N_SUPP)
    #  보충 침대의 step 추정 = 130 실측 총 step 의 중앙값 (2 mAh · 압축 이동이 두께에 비례)
    _ts = []
    for _f in sorted(os.listdir(DESC)) if os.path.isdir(DESC) else []:
        try:
            _ts.append(int(json.load(open(os.path.join(DESC, _f)))['timestep']))
        except Exception:
            pass
    supp_steps = sorted(_ts)[len(_ts) // 2] if _ts else REF['steps']
    rows, used = [], set()
    bim = [p for p in picks if 0.0 < p[0][1][0] < 1.0]
    rp_b, rs_b = _strata(len(bim), *R_P, rng), _strata(len(bim), *R_S, rng)
    monoP = [p for p in picks if p[0][1][0] >= 1.0]
    monoS = [p for p in picks if p[0][1][0] <= 0.0]
    rp_m, rs_m = _strata(len(monoP), *R_P, rng), _strata(len(monoS), *R_MONO_S, rng)
    serich = [p for p in picks if p[0][1][1] / 100.0 > SE_SPLIT + 1e-12]
    vf_free = _strata(len(serich), VF_LO, VF_HI, rng)
    for k, ((xyz, (ps, se, dse)), gd) in enumerate(picks, 1):
        pdd = round(se / 100.0, 6)
        w_am = 1.0 - pdd
        if 0.0 < ps < 1.0:
            ntype, kind = 3, 'bimodal'
            i = bim.index(((xyz, (ps, se, dse)), gd))
            rP, rS = round(rp_b[i], 4), round(rs_b[i], 4)
            w_p, w_s = round(w_am * ps, 6), round(w_am * (1 - ps), 6)
        elif ps >= 1.0:
            ntype, kind = 2, 'mono_AM_P'
            rP, rS = round(rp_m[monoP.index(((xyz, (ps, se, dse)), gd))], 4), ''
            w_p, w_s = round(w_am, 6), 0.0
        else:
            ntype, kind = 2, 'mono_AM_S'
            rP, rS = round(rs_m[monoS.index(((xyz, (ps, se, dse)), gd))], 4), ''
            w_p, w_s = round(w_am, 6), 0.0
        if pdd > SE_SPLIT + 1e-12:
            rule, vf = 'volfrac_free', round(vf_free[serich.index(((xyz, (ps, se, dse)), gd))], 6)
        else:
            rule, vf = '2mAh_fixed', round(volfrac_for_loading(w_am), 6)
        adj = ''
        n_am, n_se, phi = counts(pdd, w_p, w_s, rP, rS or 0, dse / 2, ntype, vf)
        if n_am + n_se > cap and rule == 'volfrac_free':
            vf2 = max(VF_LO, vf * cap / (n_am + n_se) * 0.999)
            vf, adj = round(vf2, 6), 'volfrac'
            n_am, n_se, phi = counts(pdd, w_p, w_s, rP, rS or 0, dse / 2, ntype, vf)
        while n_am + n_se > cap:          # 작은 AM 반지름을 올린다 (가장 유리한 경우가 상한 안이라 끝난다)
            if ntype == 3 and rS < R_S[1]:
                rS = round(min(R_S[1], rS * 1.05), 4)
            elif ntype == 2 and kind == 'mono_AM_S' and rP < R_MONO_S[1]:
                rP = round(min(R_MONO_S[1], rP * 1.05), 4)
            elif ntype == 3 and rP < R_P[1]:
                rP = round(min(R_P[1], rP * 1.05), 4)
            else:
                raise SystemExit(f'⛔ lhss_{k:03d} 상한을 못 맞춘다 (후보 판정과 모순)')
            adj = (adj + '+r').lstrip('+')
            n_am, n_se, phi = counts(pdd, w_p, w_s, rP, rS or 0, dse / 2, ntype, vf)
        s = X.next_free_prime(rng.randint(SEED_LO, SEED_HI), used, SEED_LO, SEED_HI)
        used.add(s)
        steps = supp_steps
        core_h, _ = _cost(n_am + n_se, steps, 1)
        nt = _ntasks_for(core_h, 1, 4)
        core_h, wall_h = _cost(n_am + n_se, steps, nt)
        rows.append(dict(id=f'lhss_{k:03d}', block='supp', partner='', stratum='', ntype=ntype, kind=kind,
                         pdd_SE=pdd, w_AM_P=w_p, w_AM_S=w_s, rP_um=rP, rS_um=rS, rSE_um=round(dse / 2, 4),
                         rSE_lo_um=D_SE_MIN / 2, rSE_truncated=0, volfrac=vf, loading_rule=rule,
                         loading_mAh_cm2=round(loading_of(w_am, vf), 4), ins_scale=1.0, phi_AM=round(phi, 6),
                         n_AM_est=round(n_am), n_SE_est=round(n_se), n_total_est=round(n_am + n_se),
                         cap_adjust=adj, gap_dist=round(gd, 4), lhs_cell='', seed=s, ntasks=nt,
                         steps_est=steps, core_h_est=round(core_h, 1), wall_h_est=round(wall_h, 1)))
    d130 = {r['case_id']: r for r in csv.DictReader(open(D130, encoding='utf-8'))}
    for pid, _why in THICK_PARTNERS:
        p = d130[pid]
        am = float(p['am_pct']) / 100.0
        ps = float(p['ps_frac'])
        pdd = round(1.0 - am, 6)
        w_p, w_s = round(am * ps, 6), round(am * (1 - ps), 6)
        rP, rS, rSE = float(p['r_AM_P_um']), float(p['r_AM_S_um']), float(p['r_SE_um'])
        vf = round(volfrac_for_loading(am), 6)
        try:
            psteps = int(json.load(open(os.path.join(DESC, pid + '.json')))['timestep'])
        except Exception:
            psteps = REF['steps']
        for L in THICK_LOADINGS:
            sc = L / 2.0
            n_am, n_se, phi = counts(pdd, w_p, w_s, rP, rS, rSE, 3, vf, sc)
            steps = int(FIXED_STEPS + (psteps - FIXED_STEPS) * sc)
            core_h, _ = _cost(n_am + n_se, steps, 1)
            nt = _ntasks_for(core_h, 2, 8)
            core_h, wall_h = _cost(n_am + n_se, steps, nt)
            s = X.next_free_prime(rng.randint(SEED_LO, SEED_HI), used, SEED_LO, SEED_HI)
            used.add(s)
            rows.append(dict(id=f'lhst_{pid[-3:]}_{int(L)}m', block='thick', partner=pid, stratum='', ntype=3,
                             kind='bimodal', pdd_SE=pdd, w_AM_P=w_p, w_AM_S=w_s, rP_um=rP, rS_um=rS, rSE_um=rSE,
                             rSE_lo_um=D_SE_MIN / 2, rSE_truncated=0, volfrac=vf, loading_rule='2mAh_fixed',
                             loading_mAh_cm2=L, ins_scale=sc, phi_AM=round(phi, 6), n_AM_est=round(n_am),
                             n_SE_est=round(n_se), n_total_est=round(n_am + n_se), cap_adjust='', gap_dist='',
                             lhs_cell='', seed=s, ntasks=nt, steps_est=steps, core_h_est=round(core_h, 1),
                             wall_h_est=round(wall_h, 1)))
    allocate_cores(rows)
    feas = (lambda q: _best_case_n(q[0], 5.0 + 65.0 * q[1], 1.0 + q[2]) <= cap)
    gb, tot = gap_fraction(ex_xyz, feasible=feas)
    ga, _ = gap_fraction(ex_xyz + [norm(r['w_AM_P'] / (1 - r['pdd_SE']) if r['ntype'] == 3 else
                                        (1.0 if r['kind'] == 'mono_AM_P' else 0.0),
                                        r['pdd_SE'] * 100, r['rSE_um'] * 2) for r in rows if r['block'] == 'supp'],
                         feasible=feas)
    n_lim = 20000 - tot
    report = dict(cap_n_total=cap, n_candidates=len(cands), gap_thr=GAP_THR, feasible_mc=tot,
                  limit_zone_frac=round(n_lim / 20000, 4), gap_before=round(gb, 4), gap_after=round(ga, 4),
                  slots=SLOTS, cores_total=sum(r['ntasks'] for r in rows), C_LOAD=C_LOAD,
                  ref=REF, eff_mpi=EFF_MPI, design_seed=seed, supp_steps=supp_steps)
    return rows, report


def to_csv(rows) -> bytes:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLS, lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, '') for c in COLS})
    return buf.getvalue().encode('utf-8')


# ── 검증 (materialize --points 가 부른다) ──────────────────────────────────
def verify_rows(rows, cap=None):
    bad = []
    if cap is None:
        cap = max(p['n'] for p in load_existing())
    d130 = {r['case_id']: r for r in csv.DictReader(open(D130, encoding='utf-8'))}
    ids, seeds = set(), set()
    for r in rows:
        rid = r.get('id', '')
        miss = [c for c in COLS if c not in r]
        if miss:
            bad.append(f'{rid}: 열 없음 {miss}')
            continue
        if not _ID.match(rid) or rid in ids:
            bad.append(f'{rid}: ID 형식 · 중복')
        ids.add(rid)
        try:
            s = int(r['seed'])
            nt, ntasks = int(r['ntype']), int(r['ntasks'])
            pdd, wp = float(r['pdd_SE']), float(r['w_AM_P'])
            ws = float(r['w_AM_S'] or 0)
            rP, rSE, vf, sc = float(r['rP_um']), float(r['rSE_um']), float(r['volfrac']), float(r['ins_scale'])
            rS = float(r['rS_um']) if r['rS_um'] not in ('', None) else 0.0
            L = float(r['loading_mAh_cm2'])
        except (TypeError, ValueError) as e:
            bad.append(f'{rid}: 숫자 아님 ({e})')
            continue
        if not (SEED_LO <= s <= SEED_HI and X.is_prime(s)) or s in seeds:
            bad.append(f'{rid}: seed {s} (소수 · 범위 · 중복)')
        seeds.add(s)
        if abs(pdd + wp + ws - 1.0) > 1e-6:
            bad.append(f'{rid}: 가중 합 {pdd + wp + ws:.8f}')
        if 2 * rSE < D_SE_MIN - 1e-9:
            bad.append(f'{rid}: SE 지름 {2 * rSE} < {D_SE_MIN}')
        if not (VF_LO - 1e-6 <= vf <= VF_HI + 1e-6):
            bad.append(f'{rid}: volfrac {vf} 상자 밖')
        kinds = {3: ('bimodal',), 2: ('mono_AM_P', 'mono_AM_S')}
        if r['kind'] not in kinds.get(nt, ()):
            bad.append(f'{rid}: kind {r["kind"]} ↔ ntype {nt}')
        if nt == 2 and abs(ws) > 1e-12:
            bad.append(f'{rid}: 2-type 인데 w_AM_S {ws}')
        if nt == 3 and not (R_S[0] - 1e-9 <= rS <= R_S[1] + 1e-9 and R_P[0] - 1e-9 <= rP <= R_P[1] + 1e-9):
            bad.append(f'{rid}: bimodal 반지름 상자 밖 ({rP}, {rS})')
        n_am, n_se, _ = counts(pdd, wp, ws, rP, rS, rSE, nt, vf, sc)
        if n_am + n_se > cap + 0.5:
            bad.append(f'{rid}: 입자 수 {n_am + n_se:.0f} > 상한 {cap:.0f}')
        if not (1 <= ntasks <= SLOTS):
            bad.append(f'{rid}: ntasks {ntasks}')
        if ntasks > 1 and (n_am + n_se) / ntasks < MIN_PP:
            bad.append(f'{rid}: 코어당 입자 {(n_am + n_se) / ntasks:.0f} < {MIN_PP} ({ntasks} 코어)')
        if abs(loading_of(1 - pdd, vf) * sc - L) > 1e-3:
            bad.append(f'{rid}: 로딩 {L} ↔ volfrac·높이 {loading_of(1 - pdd, vf) * sc:.4f}')
        if r['block'] == 'supp':
            if abs(sc - 1.0) > 1e-12:
                bad.append(f'{rid}: 보충 침대 ins_scale {sc} ≠ 1')
            rule_ok = ((r['loading_rule'] == '2mAh_fixed' and pdd <= SE_SPLIT + 1e-9
                        and abs(vf - volfrac_for_loading(1 - pdd)) < 2e-6)
                       or (r['loading_rule'] == 'volfrac_free' and pdd > SE_SPLIT + 1e-9))
            if not rule_ok:
                bad.append(f'{rid}: 로딩 규칙 {r["loading_rule"]} ↔ pdd_SE {pdd} · volfrac {vf}')
        elif r['block'] == 'thick':
            p = d130.get(r['partner'])
            if p is None:
                bad.append(f'{rid}: 짝 {r["partner"]} 이 130 설계에 없다')
            else:
                am, ps = float(p['am_pct']) / 100, float(p['ps_frac'])
                want = (1 - am, am * ps, am * (1 - ps), float(p['r_AM_P_um']), float(p['r_AM_S_um']),
                        float(p['r_SE_um']), volfrac_for_loading(am))
                got = (pdd, wp, ws, rP, rS, rSE, vf)
                if any(abs(a - b) > 2e-6 for a, b in zip(want, got)) or nt != 3:
                    bad.append(f'{rid}: 짝 {r["partner"]} 과 조성 · 반지름 · volfrac 불일치')
            if abs(sc - L / 2.0) > 1e-9 or L not in THICK_LOADINGS:
                bad.append(f'{rid}: 후막 ins_scale {sc} ↔ 로딩 {L}')
        else:
            bad.append(f'{rid}: block {r["block"]}')
    tot = sum(int(r['ntasks']) for r in rows if str(r.get('ntasks', '')).isdigit())
    if tot > SLOTS:
        bad.append(f'코어 합 {tot} > {SLOTS} (qos cpu-60)')
    return bad


def verify_csv(path, expect_sha=None):
    raw = open(path, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if expect_sha and sha != expect_sha.strip().lower():
        return [f'sha256 불일치 — 기대 {expect_sha[:12]}… 실제 {sha[:12]}…'], sha
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
    return verify_rows(rows), sha


# ── selftest ──────────────────────────────────────────────────────────────
def selftest() -> int:
    fails = []

    def chk(name, cond):
        print(f"  {'✓' if cond else '✗'} {name}")
        if not cond:
            fails.append(name)

    m = {r['case']: r for r in X.MEASURED}
    chk('s1 2 mAh 규칙 = lhs00_000 volfrac', abs(volfrac_for_loading(0.85) - 0.222984) < 1e-9)
    chk('s1 2 mAh 규칙 = lhs00_110 volfrac (0.250627)', abs(volfrac_for_loading(X.mass_from_vol(0.625)) - m['lhs00_110']['volfrac']) < 2e-5)
    chk('s1 상자 경계 = AM 95 · 70 wt%', abs(volfrac_for_loading(0.95) - VF_LO) < 2e-5 and abs(volfrac_for_loading(0.70) - VF_HI) < 2e-5)
    n_am, n_se, _ = counts(0.15, 0.85 * 0.6, 0.85 * 0.4, 5.5, 0.5, 1.0, 3, 0.222984)
    chk('s2 입자 수 = lhs00_000 실측 45,030 (±2 %)', abs(n_am + n_se - 45030) / 45030 < 0.02)
    rows, rep = generate()
    rows2, _ = generate()
    chk('s3 결정론 (같은 seed = 같은 바이트)', to_csv(rows) == to_csv(rows2))
    chk(f's4 생성물 검증 통과 ({len(rows)} 행)', verify_rows(rows) == [])
    chk(f's5 빈 곳 줄어듦 ({rep["gap_before"]} → {rep["gap_after"]})', rep['gap_after'] < rep['gap_before'])
    chk('s5 보충 20 · 후막 8', sum(r['block'] == 'supp' for r in rows) == 20 and sum(r['block'] == 'thick' for r in rows) == 8)

    def mut(fn, name):
        rr = [dict({k: str(v) for k, v in r.items()}) for r in rows]
        fn(rr)
        chk(f's6 변이 거부 — {name}', verify_rows(rr) != [])
    mut(lambda rr: rr[0].update(seed='30030'), '합성수 seed')
    mut(lambda rr: rr[1].update(seed=rr[0]['seed']), 'seed 중복')
    mut(lambda rr: rr[0].update(w_AM_P=str(float(rr[0]['w_AM_P']) + 0.01)), '가중 합 어긋남')
    mut(lambda rr: rr[0].update(rSE_um='0.4'), 'SE 지름 < 1.0')
    mut(lambda rr: rr[2].update(id=rr[1]['id']), 'ID 중복')
    th = [i for i, r in enumerate(rows) if r['block'] == 'thick']
    sp = [i for i, r in enumerate(rows) if r['block'] == 'supp']
    mut(lambda rr: rr[th[0]].update(ins_scale='2.5'), '후막 ins_scale ↔ 로딩')
    mut(lambda rr: rr[th[0]].update(rP_um=str(float(rr[th[0]]['rP_um']) + 0.5)), '후막 짝 조성 어긋남')
    mut(lambda rr: rr[sp[0]].update(ins_scale='3.0', loading_mAh_cm2=str(float(rr[sp[0]]['loading_mAh_cm2']) * 3)), '보충 침대 ins_scale ≠ 1')
    mut(lambda rr: [r.update(ntasks='4') for r in rr], '코어 합 > 60')
    mut(lambda rr: rr[th[0]].update(partner='lhs00_999'), '짝 없음')
    mut(lambda rr: rr[sp[0]].update(kind='trimodal'), '모르는 kind')
    mut(lambda rr: rr[sp[0]].update(rSE_um='0.5', rS_um='0.5', ntype='3', kind='bimodal', pdd_SE='0.7', w_AM_P='0.15',
                                     w_AM_S='0.15', volfrac='0.317759', loading_rule='volfrac_free',
                                     loading_mAh_cm2=str(loading_of(0.3, 0.317759))), '입자 수 상한 초과')
    _nt = sum(int(r['ntasks']) for r in rows)
    chk(f's8 코어 = {SLOTS} 꽉 채움 (1저자 10-06 밤 — "60코어 꽉꽉 채워" · 지금 {_nt})', _nt == SLOTS)
    chk('s8 코어당 입자 ≥ MIN_PP (1 코어 런 제외)',
        all(int(r['ntasks']) == 1 or float(r['n_total_est']) / int(r['ntasks']) >= MIN_PP for r in rows))
    _big = [r for r in rows if float(r['n_total_est']) > 100_000]
    chk('s8 10 만 넘는 런은 3 코어 이상', bool(_big) and all(int(r['ntasks']) >= 3 for r in _big))
    _w1 = max(float(r['core_h_est']) for r in rows)
    chk('s8 최장 벽시계 < 1 코어 최장 core-h 의 절반', max(float(r['wall_h_est']) for r in rows) < 0.5 * _w1)
    mut(lambda rr: rr[0].update(ntasks='9'), '코어당 입자 < MIN_PP')
    toy = maximin([(0.0, 0.0, 0.0)], [((0.1, 0.1, 0.1), 'a'), ((1.0, 1.0, 1.0), 'b'), ((0.5, 0.5, 0.5), 'c')], 1)
    chk('s7 maximin 첫 점 = 가장 먼 구석', toy[0][0][1] == 'b')
    print(f'\n{"전부 통과" if not fails else f"실패 {len(fails)}"}')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out')
    ap.add_argument('--report')
    ap.add_argument('--verify')
    ap.add_argument('--expect-sha256')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.verify:
        bad, sha = verify_csv(a.verify, a.expect_sha256)
        for b in bad[:20]:
            print('  ⛔', b)
        print(f'검증 {"✓" if not bad else "✗"} · sha256 {sha}')
        return 1 if bad else 0
    rows, rep = generate()
    raw = to_csv(rows)
    bad = verify_rows(rows)
    if bad:
        raise SystemExit(f'⛔ 생성물이 자기 검증을 통과하지 못했다: {bad[:3]}')
    if a.out:
        open(a.out, 'wb').write(raw)
    rep['sha256'] = hashlib.sha256(raw).hexdigest()
    rep['rows'] = rows
    if a.report:
        json.dump(rep, open(a.report, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        open(a.report, 'a').write('\n')
    print(json.dumps({k: v for k, v in rep.items() if k != 'rows'}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
