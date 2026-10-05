#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RINT-03 실침대 측정 — 입자별 AM 전류 (je) 의 옛 정의 ↔ 새 정의 (`am-final-sid-v2`) 를 **같은 해**에서 맞댄다 (읽기 전용).

배경 (원장 `RINT-03` · Codex r_int 1단계 판정 10-03): 옛 `per_particle_current` 는 pid ≥ 0 인 셀을 다 셌다 — 첨가제 스탬프가
sid 만 바꾸고 남긴 AM 번호를 가진 **탄소 셀**의 전류가 AM 평균에 섞였다 (합성 반례 121–127× · 순위 역전).  G1-1 (`f1f92d009`) 이
최종 sid ∈ {1, 2} ∧ 유효 pid 로 고쳤다 (r 를 끈 산출에서도 je 가 **의도적으로** 바뀌는 선언된 예외).  이 도구는 그 변화가 **실제
침대에서 얼마나 큰가**를 잰다 — Codex G1 재검증 요청서의 실측 증거.

입력 = 킷이 남기는 `step4_grid.npz` (`mpm_webapp_payload.py --save-step4-grid`: sid · pid · vox_um · z_top_um · sig_e_S_cm ·
origin_shift_um · am_r_um · periodic_xy).  σ_e 를 payload 와 같은 인자로 다시 풀고 (r 끔), 면 전류 |J_z| 대리량을 한 번 만든 뒤
두 마스크로 나눈다.  ★ 새 정의 값은 `step3_sigma.per_particle_current` 의 출력과 **같아야** 한다 (복제 검산 — 다르면 거부).

출력 열 주의: `n_carbon_cells_with_am_pid` 는 이름과 달리 **유효 AM 번호를 단 비-AM 셀 전부** (최종 sid ∉ {1, 2} — 탄소뿐 아니라
PTFE · SE 등도 센다) 다.  전류는 σ_e > 0 인 셀만 나르므로 `old_je_mass_share_from_non_am_cells` 는 사실상 그중 **도체 (탄소)** 의 몫이다.
열 이름은 이미 낸 JSON (kgy 10-05) 과 맞추려고 그대로 둔다.  수렴 정보 (`cg_info` · `resid` · `unconverged`) 를 싣고, 소비자 계약
(cg_info == 0 ∧ unconverged False ∧ 0 ≤ resid ≤ 1e-6) 을 못 채우면 상태 = `UNCONVERGED` (SELF-85 — 옛 판은 미수렴 해도 `OK`).

순위 요약의 동률 규약 (RGL-09 · Codex 10-05 — 옛 판은 double argsort 라 동률에 서로 다른 순위를 줬다):
  · `spearman_old_new` = 평균 동률 순위 (scipy `rankdata` average) 의 Pearson.  정의 안 되면 (상수 · n < 2 · 비유한) None 이고
    `spearman_status` 가 이유를 말한다.  `rank_ties` = 순위에 든 입자 수 · old/new 동률 값 수 · 묶음 수 (앞으로 검산할 자료).
  · `top10pct_overlap` = |상위 k 옛 ∩ 상위 k 새| / k (k = 입자 수의 10 % 반올림 · 최소 1).  k 번째 값과 같은 값이 컷 안팎에
    걸치면 집합이 정해지지 않으므로 None · `top10pct_status = boundary_tie` · `top10pct_boundary_ties` = 그 값의 수.
  ⚠ 10-05 kgy 세 JSON (`docs/data/rint03_je_20261005/`) 은 옛 판 출력이라 동률 수가 없다 — 그 Spearman · top 10 % 를 이 판으로
    다시 계산할 수 없다 (입자 벡터 미보존).

  python3 scripts/rint03_je_compare.py --selftest
  python3 scripts/rint03_je_compare.py GRID.npz [GRID2.npz …] [--json OUT.json]
"""
import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step3_sigma as S3   # noqa: E402

AM_SIDS = (1, 2)


def face_current_proxy(res, sid, sigma_of_sid):
    """`per_particle_current` 와 같은 면 전류 대리량 |J_z| (r 끔 · 셀마다 위아래 면의 절반씩)."""
    P, cond = res['phi'], res['cond']
    sig = S3.sigma_field(sigma_of_sid, sid)
    sa, sb = sig[:, :, :-1], sig[:, :, 1:]
    both = cond[:, :, :-1] & cond[:, :, 1:]
    g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
    f = g * (P[:, :, :-1] - P[:, :, 1:])
    jz = np.zeros(sid.shape, np.float64)
    jz[:, :, :-1] += np.abs(f) * 0.5
    jz[:, :, 1:] += np.abs(f) * 0.5
    return jz


def masked_mean(jz, pid, mask, n_am):
    je = np.zeros(n_am, np.float64)
    nv = np.zeros(n_am, np.int64)
    np.add.at(je, pid[mask], jz[mask])
    np.add.at(nv, pid[mask], 1)
    return np.where(nv > 0, je / np.maximum(nv, 1), 0.0), nv


def _spearman(a, b):
    """Spearman → `(rho | None, 상태)`.  ★ RGL-09 (Codex 10-05) — **평균 동률 순위** (`scipy.stats.rankdata(method=
    'average')`) 의 Pearson 이다.  옛 판은 double argsort 라 동률에 서로 다른 순위를 줬다 ([1,1,2] vs [1,2,2] → 1.0 ·
    참 0.5) · 상수 벡터도 막지 못했다 (전부 0 → 0.9999999999999999 · 참 미정의).  입자 전류의 0 · 동률은 합법 입력이다.
    상태: 'ok' · 'too_few' (n < 2) · 'nonfinite_input' · 'constant_input' (어느 한 쪽 순위가 상수 = 정의 안 됨 → 값 None)."""
    from scipy.stats import rankdata
    a, b = np.asarray(a, np.float64), np.asarray(b, np.float64)
    if a.size != b.size:
        raise ValueError(f'_spearman: 길이가 다르다 ({a.size} ≠ {b.size})')
    if a.size < 2:
        return None, 'too_few'
    if not (np.isfinite(a).all() and np.isfinite(b).all()):
        return None, 'nonfinite_input'
    ra, rb = rankdata(a, method='average'), rankdata(b, method='average')
    if np.all(ra == ra[0]) or np.all(rb == rb[0]):
        return None, 'constant_input'
    da, db = ra - ra.mean(), rb - rb.mean()
    return float(np.sum(da * db) / np.sqrt(np.sum(da * da) * np.sum(db * db))), 'ok'


def _tie_counts(v):
    """→ (동률에 든 값의 수, 동률 묶음 수) — 정확히 같은 값 (float ==).  출력에 남겨 순위 요약을 검산할 수 있게 (RGL-09)."""
    _, c = np.unique(np.asarray(v, np.float64), return_counts=True)
    return int(c[c > 1].sum()), int((c > 1).sum())


def _top_k(v, idx, k):
    """상위 k 개 입자 집합 → `(집합 | None, 경계 동률 수)`.  ★ RGL-09 규약: k 번째 값과 같은 값이 컷 **안팎에 걸치면**
    상위 k 집합이 정해지지 않는다 → None (정렬 알고리즘 · 입자 번호로 임의로 고르지 않는다) · 경계 동률 수 = k 번째
    값과 같은 값의 수.  걸치지 않으면 집합은 유일하고 경계 동률 수 = 0."""
    vv = np.asarray(v, np.float64)[idx]
    order = np.argsort(-vv, kind='stable')
    kth = vv[order[k - 1]]
    if k < vv.size and vv[order[k]] == kth:
        return None, int((vv == kth).sum())
    return set(idx[order[:k]].tolist()), 0


def compare(res, sid, pid, sigma_of_sid, n_am):
    """같은 해 → 옛 · 새 je 와 요약.  새 값 = 모듈 출력과 복제 검산."""
    jz = face_current_proxy(res, sid, sigma_of_sid)
    valid = (pid >= 0) & (pid < n_am)
    m_new = valid & np.isin(sid, AM_SIDS)
    m_old = valid                                          # 옛 정의 (pid 만)
    je_new, nv_new = masked_mean(jz, pid, m_new, n_am)
    je_old, nv_old = masked_mean(jz, pid, m_old, n_am)
    je_mod = S3.per_particle_current(res, sid, pid, sigma_of_sid, n_am)
    if not np.allclose(je_new, je_mod, rtol=1e-12, atol=0.0):
        raise RuntimeError('복제한 새 정의가 step3_sigma.per_particle_current 와 다르다 — 도구를 믿을 수 없다')
    carbon_with_pid = valid & ~np.isin(sid, AM_SIDS)
    has = nv_new > 0
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(has & (je_new > 0), je_old / je_new, np.nan)
    contaminated = np.zeros(n_am, bool)
    contaminated[np.unique(pid[carbon_with_pid])] = True
    k = max(1, int(round(0.1 * int(has.sum()))))
    idx = np.where(has)[0]
    #  ★ RGL-09 — 순위 요약은 동률 규약을 명시하고 (평균 순위 · top 10 % 경계 동률 = None) 동률 수를 남긴다.
    rho, rho_st = _spearman(je_old[idx], je_new[idx])
    if idx.size == 0:
        top_new = top_old = None
        b_new = b_old = 0
    else:
        top_new, b_new = _top_k(je_new, idx, k)
        top_old, b_old = _top_k(je_old, idx, k)
    top_st = ('too_few' if idx.size == 0 else
              'boundary_tie' if (top_new is None or top_old is None) else 'ok')
    t_old, t_new = _tie_counts(je_old[idx]), _tie_counts(je_new[idx])
    r_ok = ratio[np.isfinite(ratio)]
    old_mass_non_am = float(jz[carbon_with_pid].sum() / jz[m_old].sum()) if jz[m_old].sum() > 0 else float('nan')
    return {
        'n_am': int(n_am), 'n_am_with_cells': int(has.sum()),
        'n_carbon_cells_with_am_pid': int(carbon_with_pid.sum()),
        'n_am_contaminated': int(contaminated.sum()),
        'old_je_mass_share_from_non_am_cells': round(old_mass_non_am, 6),
        'ratio_old_over_new': {'median': round(float(np.median(r_ok)), 6) if r_ok.size else None,
                               'p90': round(float(np.percentile(r_ok, 90)), 6) if r_ok.size else None,
                               'max': round(float(r_ok.max()), 6) if r_ok.size else None,
                               'n_gt_1p1': int((r_ok > 1.1).sum()), 'n_gt_2': int((r_ok > 2.0).sum())},
        'spearman_old_new': None if rho is None else round(rho, 6),
        'spearman_status': rho_st,
        'rank_ties': {'n_ranked': int(idx.size), 'old_tied_values': t_old[0], 'old_tie_groups': t_old[1],
                      'new_tied_values': t_new[0], 'new_tie_groups': t_new[1]},
        'top10pct_overlap': (round(len(top_new & top_old) / k, 6) if top_st == 'ok' else None),
        'top10pct_status': top_st,
        'top10pct_boundary_ties': {'old': b_old, 'new': b_new},
        'je_def_module': S3.PER_PARTICLE_CURRENT_DEF,
    }


def run_grid(path):
    g = np.load(path, allow_pickle=False)
    need = ('sid', 'pid', 'vox_um', 'z_top_um', 'sig_e_S_cm', 'am_r_um')
    miss = [k for k in need if k not in g.files]
    if miss:
        raise ValueError(f'{os.path.basename(path)}: npz 에 키 없음 {miss}')
    sid = g['sid'].astype(np.int8)
    pid = g['pid'].astype(np.int32)
    vox = float(g['vox_um'])
    z_top = float(g['z_top_um'])
    osh = np.asarray(g['origin_shift_um'], np.float64) if 'origin_shift_um' in g.files else np.zeros(3)
    periodic = bool(g['periodic_xy']) if 'periodic_xy' in g.files else False
    sig = np.asarray(g['sig_e_S_cm'], np.float64)
    n_am = int(len(g['am_r_um']))
    res = S3.solve_sigma_z(sid, sig, vox, return_field=True, z_top_um=z_top, z_bot_um=float(osh[2]), periodic_xy=periodic)
    if res.get('reason') or 'phi' not in res:
        return {'grid': path, 'status': 'NOT_SOLVABLE', 'reason': res.get('reason')}
    # ★ SELF-85 — 수렴 정보를 싣고 상태를 가른다 (옛 판: 미수렴 해도 'OK').  계약 = R4-CX-02 의 conjunction.
    cg_info, resid = int(res.get('cg_info', 0)), float(res.get('resid', float('nan')))
    unconv = bool(res.get('unconverged')) or cg_info != 0 or not (0.0 <= resid <= 1e-6)
    out = compare(res, sid, pid, sig, n_am)
    out.update({'grid': path, 'status': 'UNCONVERGED' if unconv else 'OK', 'cg_info': cg_info, 'resid': resid,
                'unconverged': unconv, 'sigma_e_eff_S_cm': float(res['sigma_eff']), 'shape': list(sid.shape),
                'vox_um': vox, 'periodic_xy': periodic})
    return out


def selftest():
    ok, fails = 0, []

    def chk(name, cond, detail=''):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + name + ('' if cond else f'  ({detail})'))
        if cond:
            ok += 1
        else:
            fails.append(name)
    kw = dict(z_top_um=5.0, z_bot_um=0.0)
    # T1 두 AM 입자 (x 앞쪽 = 입자 0 · 뒤쪽 = 입자 1) · 입자 0 쪽에 VGCF 띠 (σ 100) 가 입자 0 의 번호를 물려받음
    sid = np.ones((8, 6, 10), np.int8)
    pid = np.zeros(sid.shape, np.int32)
    pid[4:, :, :] = 1
    sid[0:2, :, :] = 3                                    # 탄소 셀 · pid 0 (물려받음)
    sig = np.array([0.0, 1.0, 0.0, 100.0])
    res = S3.solve_sigma_z(sid, sig, 0.5, return_field=True, **kw)
    out = compare(res, sid, pid, sig, 2)
    chk('T1a 복제 새 정의 = 모듈 출력 (compare 가 거부하지 않음)', out['je_def_module'] == 'am-final-sid-v2')
    chk('T1b 오염 입자 = 1 (입자 0 만 탄소 셀을 가짐) · 탄소 셀 수 = 2·6·10',
        out['n_am_contaminated'] == 1 and out['n_carbon_cells_with_am_pid'] == 120, out)
    chk('T1c 옛/새 비 최대 > 5 (탄소 전류가 옛 평균을 끌어올림)', (out['ratio_old_over_new']['max'] or 0) > 5.0, out['ratio_old_over_new'])
    chk('T1d 옛 je 질량 중 비-AM 셀 몫 > 0.5', out['old_je_mass_share_from_non_am_cells'] > 0.5, out)
    # T2 탄소 셀이 pid −1 (번호 없음) → 두 정의가 같다 (비 = 1 · 오염 0)
    pid2 = pid.copy()
    pid2[0:2, :, :] = -1
    out2 = compare(res, sid, pid2, sig, 2)
    chk('T2 탄소 셀 pid −1 이면 옛 = 새 (비 1 · 오염 0)',
        out2['n_am_contaminated'] == 0 and abs((out2['ratio_old_over_new']['max'] or 0) - 1.0) < 1e-12, out2)
    # T3 n_am 밖 번호 · 음수 번호는 두 정의 모두에서 빠진다
    pid3 = pid.copy()
    pid3[5, 5, 5] = 9
    out3 = compare(res, sid, pid3, sig, 2)
    chk('T3 n_am 밖 번호는 셈에서 빠진다 (IndexError 없음)', out3['n_am'] == 2)
    # T4 순위 역전 탐지 — 입자 0 은 AM 셀 전류가 작고 탄소로 부풀려짐 · 입자 1 은 AM 전류가 더 큼
    sid4 = np.ones((8, 6, 10), np.int8)
    sid4[0:2, :, :] = 3
    sid4[2:4, :, :] = 2                                   # 입자 0 의 AM 셀 = AM_P (σ 0 → 거의 절연)
    sig4 = np.array([0.0, 1.0, 1e-3, 100.0])
    res4 = S3.solve_sigma_z(sid4, sig4, 0.5, return_field=True, **kw)
    out4 = compare(res4, sid4, pid, sig4, 2)
    chk('T4 순위가 뒤집히면 top 10 % 겹침 < 1 · Spearman < 1', out4['top10pct_overlap'] < 1.0 and (out4['spearman_old_new'] or 1) < 1.0, out4)
    # T5 · T6 (SELF-85) 수렴 정보 — 옛 판은 미수렴 해도 'OK' 로 냈다 (JSON 에 cg_info · resid 없음).
    #   소비자 수렴 계약 (R4-CX-02) = cg_info == 0 ∧ unconverged False ∧ 0 ≤ resid ≤ 1e-6.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p5 = os.path.join(td, 'step4_grid.npz')
        np.savez(p5, sid=sid, pid=pid, vox_um=np.float64(0.5), z_top_um=np.float64(5.0),
                 sig_e_S_cm=sig, am_r_um=np.ones(2), origin_shift_um=np.zeros(3), periodic_xy=np.bool_(False))
        r5 = run_grid(p5)
        chk('T5 수렴한 해 = OK 이고 cg_info 0 · resid ≤ 1e-6 · unconverged False 를 싣는다',
            r5.get('status') == 'OK' and r5.get('cg_info') == 0 and r5.get('unconverged') is False
            and isinstance(r5.get('resid'), float) and 0.0 <= r5['resid'] <= 1e-6, r5)
        mi = S3.CG_MAXITER
        try:
            S3.CG_MAXITER = 1                             # CG 한 번 → 미수렴
            r6 = run_grid(p5)
        finally:
            S3.CG_MAXITER = mi
        chk('T6 미수렴 해는 OK 가 아니다 (status UNCONVERGED · cg_info > 0 · unconverged True)',
            r6.get('status') == 'UNCONVERGED' and (r6.get('cg_info') or 0) > 0 and r6.get('unconverged') is True, r6)
    # T7–T11 (RGL-09 · Codex 10-05) — Spearman 은 **평균 동률 순위** (rankdata average) 의 Pearson 이다.  옛 double argsort
    #   는 동률에 서로 다른 순위를 줘 [1,1,2] vs [1,2,2] → 1.0 (참 0.5) · 상수 벡터 → 0.9999999999999999 (참 미정의).
    #   입자 전류의 0 · 동률은 합법 입력이다 (판에 안 닿은 AM = je 0 정확히).
    def _rho(r):
        return r[0] if isinstance(r, tuple) else r       # 옛 판은 float 만 돌려준다 (그래도 값으로 판정)
    r7 = _spearman(np.array([1.0, 1.0, 2.0]), np.array([1.0, 2.0, 2.0]))
    chk('T7 동률 반례 [1,1,2] vs [1,2,2] → 0.5 (평균 순위) · 상태 ok',
        _rho(r7) is not None and abs(_rho(r7) - 0.5) < 1e-12 and isinstance(r7, tuple) and r7[1] == 'ok', r7)
    r8 = [_spearman(np.zeros(5), np.zeros(5)), _spearman(np.zeros(5), np.arange(5.0)),
          _spearman(np.array([3.0]), np.array([1.0])), _spearman(np.array([1.0, np.nan, 2.0]), np.arange(3.0))]
    chk('T8 정의 안 되는 입력 = 값 None + 상태 (상수 · 한쪽 상수 · n<2 · 비유한) — 숫자를 지어내지 않는다',
        all(isinstance(x, tuple) and x[0] is None for x in r8)
        and [x[1] for x in r8] == ['constant_input', 'constant_input', 'too_few', 'nonfinite_input'], r8)
    from scipy.stats import spearmanr as _sr                # 검증된 함수 = 오라클 (동률 많은 정수 표본)
    _rng = np.random.default_rng(7)
    _d9 = []
    for _ in range(25):
        _n = int(_rng.integers(5, 60))
        _a, _b = _rng.integers(0, 4, _n).astype(float), _rng.integers(0, 4, _n).astype(float)
        if np.ptp(_a) == 0 or np.ptp(_b) == 0:
            continue
        _d9.append(abs(_rho(_spearman(_a, _b)) - float(_sr(_a, _b)[0])))
    _a9 = _rng.normal(size=40); _b9 = _a9 + _rng.normal(scale=0.5, size=40)    # 동률 없는 표본 = 옛 정의와 같아야
    _old9 = float(np.corrcoef(np.argsort(np.argsort(_a9)), np.argsort(np.argsort(_b9)))[0, 1])
    chk(f'T9 동률 많은 표본 {len(_d9)} 개에서 scipy.stats.spearmanr 와 1e-12 안 · 동률 없으면 옛 정의와 같은 값',
        len(_d9) >= 20 and max(_d9) < 1e-12 and abs(_rho(_spearman(_a9, _b9)) - _old9) < 1e-12, max(_d9 or [0]))
    # T10 top 10 % 경계 동률 — 판에 닿은 기둥 입자 1 개 + 떠 있는 AM 19 개 (je 0 정확히) → k=2 번째 값 0 이 컷 안팎에
    #   걸친다.  규약: 집합이 정해지지 않으면 겹침 None · 상태 boundary_tie · 경계 동률 수 (임의 tie-break 로 숫자를 안 낸다).
    sid10 = np.zeros((12, 12, 10), np.int8)
    pid10 = np.full(sid10.shape, -1, np.int32)
    sid10[0, 0, :] = 1
    pid10[0, 0, :] = 0
    _pos = [(x, y) for x in (2, 4, 6, 8, 10) for y in (2, 4, 6, 8, 10)][:19]
    for _i, (_x, _y) in enumerate(_pos, start=1):
        sid10[_x, _y, 5] = 1
        pid10[_x, _y, 5] = _i
    sig10 = np.array([0.0, 1.0])
    res10 = S3.solve_sigma_z(sid10, sig10, 0.5, return_field=True, **kw)
    out10 = compare(res10, sid10, pid10, sig10, 20)
    chk('T10 top 10 % 경계 동률 → 겹침 None · 상태 boundary_tie · 경계 동률 수 19 (old · new)',
        out10.get('top10pct_overlap') is None and out10.get('top10pct_status') == 'boundary_tie'
        and out10.get('top10pct_boundary_ties') == {'old': 19, 'new': 19}, {k: out10.get(k) for k in
        ('top10pct_overlap', 'top10pct_status', 'top10pct_boundary_ties')})
    # T11 출력 — 동률 수 · 상태를 남기고 (앞으로 검산 가능) · bare NaN 토큰 없이 엄격 JSON 으로 직렬화된다
    _rt = out10.get('rank_ties') or {}
    try:
        json.dumps(out10, allow_nan=False)
        _strict = True
    except ValueError:
        _strict = False
    chk('T11 출력에 rank_ties (old · new 동률 값 수 · 묶음 수 · n_ranked) · spearman_status · 엄격 JSON',
        _rt.get('n_ranked') == 20 and _rt.get('old_tied_values') == 19 and _rt.get('new_tied_values') == 19
        and _rt.get('old_tie_groups') == 1 and _rt.get('new_tie_groups') == 1
        and out10.get('spearman_status') == 'ok' and _strict
        and out4.get('top10pct_status') == 'ok' and out4.get('top10pct_boundary_ties') == {'old': 0, 'new': 0}, _rt)
    print(f'\n{ok} PASS · {len(fails)} FAIL')
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description='RINT-03 — 입자별 AM 전류 옛/새 정의 실침대 대조 (읽기 전용)')
    ap.add_argument('grids', nargs='*')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--json', default=None)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.grids:
        ap.error('step4_grid.npz 경로를 주거나 --selftest')
    rows = []
    for p in a.grids:
        try:
            rows.append(run_grid(p))
        except Exception as e:   # noqa: BLE001 — 한 격자 실패가 다른 격자를 막지 않게 · 상태로 남긴다
            rows.append({'grid': p, 'status': 'INPUT_ERROR', 'reason': f'{type(e).__name__}: {e}'})
        print(json.dumps(rows[-1], ensure_ascii=False))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
    return 0 if all(r.get('status') == 'OK' for r in rows) else 2


if __name__ == '__main__':
    sys.exit(main())
