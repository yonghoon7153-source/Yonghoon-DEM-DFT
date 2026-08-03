#!/usr/bin/env python3
"""design_performance_dataset — 케이스당 **한 벡터**: 설계 ∪ DEM ∪ MPM ∪ STEP4.

동기 (2026-08-03 실측)
──────────────────────
코퍼스: 케이스 190 · full_metrics(DEM) 187 · **mpm_metrics(MPM) 187** · STEP4 **0**.
그런데 `webapp/predictor_engine.py` 의 MPM 참조는 `grep -c mpm` = **0** 이다 — 187 케이스분
MPM 산출물(진짜 소성 porosity·두께·coverage)이 예측기에 **한 번도 안 들어간다**.
이 모듈이 그 층을 만든다 (CLAUDE.md 로드맵 Phase 2 "single data layer").

★ 설계값 유도는 **재구현하지 않는다**
──────────────────────────────────
`predictor_engine.load_training_data` 를 그대로 호출해서 설계+DEM 을 얻는다.  d_SE/d_AM/AM%/
P:S 를 여기서 다시 파싱하면 두 곳이 갈라진다 — 이번 리뷰의 HIGH-10(테스트가 프로덕션 사본을
검사해 커버리지 0) 과 같은 실패 유형.  이 모듈은 **조인만** 한다.

★ §F1 — 없는 층은 비운다
────────────────────────
MPM/STEP4 가 없는 케이스는 그 칼럼이 **빈칸**이고, `has_dem/has_mpm/has_step4` 플래그와
커버리지 리포트로 드러낸다.  0 으로 채우면 "측정했는데 0" 과 구별이 안 된다.

Selftest:  python3 scripts/design_performance_dataset.py --selftest
사용:      python3 scripts/design_performance_dataset.py \
               --results ~/Yonghoon-DEM-DFT/webapp/results \
               --archive ~/Yonghoon-DEM-DFT/webapp/archive \
               --mpm-lab ~/Yonghoon-DEM-DFT/webapp/mpm_lab \
               --out docs/data/design_performance_corpus.csv
"""

import argparse
import json
import os
import sys

# ── MPM 산출물 (webapp payload writer 스키마 — 실측 188건에서 확인, 2026-08-03) ──────────
#    ⚠ mpm3d_compaction --save-metrics 와 **다른 스키마**다.  실제 키를 쓴다.
MPM_KEYS = (
    # 구조 — DEM 과 **같은 물리량의 독립 측정**(frame[4])
    'porosity_mpm_pct', 'thickness_mpm_um', 'bulk_density_g_cm3', 'se_fraction_pct',
    'compacted_porosity_pct', 'seed_porosity_pct',
    # coverage — ★RIGID(기하, 해석적) 와 PLASTIC(변형 SE 점) 두 규약을 같은 밴드에서
    'coverage_AM_P_hertz_pct', 'coverage_AM_S_hertz_pct',          # plastic @Hertz
    'coverage_AM_P_tabor_pct', 'coverage_AM_S_tabor_pct',          # plastic @Tabor
    'coverage_AM_P_rigid_hertz_pct', 'coverage_AM_S_rigid_hertz_pct',
    'coverage_AM_P_rigid_tabor_pct', 'coverage_AM_S_rigid_tabor_pct',
    'cov_hertz_um', 'cov_tabor_um', 'cov_method',
    # 소성 변형장 — **MPM 고유** (강체구 DEM 엔 존재하지 않는 양)
    'dg_mean', 'dg_max', 'dg_vmax98', 'dg_nonzero_pct', 'strain_kind',
    # 재료·프로토콜 (같은 캘리브레이션인지 확인용)
    'E_SE_GPa', 'nu_SE', 'sigma_y_GPa', 'K_SE_GPa',
    'final_stress_GPa', 'target_GPa', 'protocol', 'n_grid', 'n_am',
)
# ★★ 절대 가져오지 않는 키 — CLAUDE.md 가 명시적으로 보고 금지한 것:
#   "NEVER report the voxel-adjacency `coverage_AM_*_mpm_pct` (~26 %) — density/n_vox-bound,
#    does NOT converge; it is a preview artifact."
#   ML feature 로 넣으면 격자 해상도를 물리인 척 학습한다.  이름이 그럴듯해서 자동수집에
#   섞이기 쉬우므로 **명시 차단**하고, selftest 가 부재를 확인한다.
MPM_FORBIDDEN = ('coverage_AM_P_mpm_pct', 'coverage_AM_S_mpm_pct')

# ── regime-gate: 어느 모델의 porosity 를 믿을 것인가 (docs/mpm_scaffold_reliability_and_am_freeze.md)
#    ★ 부호 규약 충돌 주의 (2026-08-03): 원 DB `mpm_dem_porosity_reliability.csv` 의 컬럼은
#      `gap_dem_minus_mpm` = **DEM − MPM** 이고, 이 모듈은 **MPM − DEM** 을 쓴다.  같은 리포에
#      반대 규약 둘이 있으므로 여기 컬럼명을 `porosity_gap_mpm_minus_dem_pp` 로 **명시**한다.
#    ★ 규칙: MPM 이 DEM 보다 4 %p 이상 낮으면(=MPM 과압축, SE-poor corner) DEM 을 쓴다.
#      그 외(교차검증 일치 + SE-rich 에서 DEM 이 ε_sphere artifact) 는 MPM.
#      ⇒ 원 DB 117 건의 큐레이션된 `use_source` 를 **100 % 재현**한다 (2026-08-03 검증).
#      단 `trust`(both/MPM/review/bracket/anchor 5단계)는 이 규칙이 못 만드는 **추가 정보**라
#      조인으로 가져오고, 없는 케이스는 reviewed=0 으로 낙인한다.
GATE_BAND_PP = 4.0
CURATED_DB = 'docs/data/mpm_dem_porosity_reliability.csv'


def _load_curated(root):
    """큐레이션된 판정 DB → {case: row}.  없으면 빈 dict (자동판정만 남음)."""
    import csv as _csv
    p = os.path.join(root, CURATED_DB)
    try:
        return {r['case']: r for r in _csv.DictReader(open(p))}
    except Exception:
        return {}

# STEP4 viz json 에서 가져올 성능 (있을 때만)
S4_KEYS = ('c_rate', 'charge', 'end_reason', 'i_1c_a', 'v_min', 'v_max', 'cv_hold')


def _load_json(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception:
        return None


def _find_layer(case_name, roots, filename=None, glob_pat=None):
    """케이스 이름으로 MPM/STEP4 산출물을 찾는다 (results/archive/mpm_lab 어디에 있든)."""
    import glob as _g
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        d = os.path.join(root, case_name)
        if filename:
            p = os.path.join(d, filename)
            if os.path.isfile(p):
                return p
        if glob_pat:
            hits = sorted(_g.glob(os.path.join(d, glob_pat)))
            if hits:
                return hits[0]
    return None


def build(results_folder, archive_folder, mpm_lab=None, verbose=True):
    """설계+DEM(predictor_engine) ⋈ MPM ⋈ STEP4 → rows, coverage."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'webapp'))
    import predictor_engine as _pe                     # ★ 설계값 유도의 단일 출처
    rows = _pe.load_training_data(results_folder, archive_folder)
    roots = [r for r in (results_folder, archive_folder, mpm_lab) if r]
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    curated = _load_curated(_root)
    cov = {'n': len(rows), 'dem': len(rows), 'mpm': 0, 'step4': 0,
           'reviewed': 0, 'use_dem': 0, 'use_mpm': 0}
    for r in rows:
        r['has_dem'] = 1
        # ★ 원 DB 가 쓰는 판별 축 = SE/solid.  am_pct(wt%) 가 아니라 이것으로 봐야 문서와 대조된다.
        _pse, _pam = r.get('phi_se') or 0.0, r.get('phi_am') or 0.0
        if (_pse + _pam) > 0:
            r['se_of_solid_pct'] = round(100.0 * _pse / (_pse + _pam), 2)
        r['has_mpm'] = 0
        r['has_step4'] = 0
        mp = _find_layer(r['name'], roots, filename='mpm_metrics.json')
        if mp:
            m = _load_json(mp) or {}
            if m:
                r['has_mpm'] = 1
                cov['mpm'] += 1
                for k in MPM_KEYS:
                    if k in m and m[k] is not None:
                        r['mpm_' + k] = m[k]
                # ★ MPM **고유** 파생: 소성 conforming = plastic − rigid coverage.
                #   강체구 DEM 은 이 값이 정의상 0 이다 (docs/mpm_coverage_plastic_vs_rigid.md).
                #   ⇒ 예측기에 넣을 가치가 있는 것은 coverage 절대값이 아니라 **이 증분**이다.
                for _am in ('AM_P', 'AM_S'):
                    for _band in ('hertz', 'tabor'):
                        _pl = m.get(f'coverage_{_am}_{_band}_pct')
                        _rg = m.get(f'coverage_{_am}_rigid_{_band}_pct')
                        if _pl is not None and _rg is not None:
                            r[f'mpm_plastic_gain_{_am}_{_band}_pp'] = round(
                                float(_pl) - float(_rg), 3)
                # ★ frame[4] 교차검증 지표: 같은 porosity 를 DEM 과 MPM 이 독립으로 잰 차이.
                #   |gap| ≤ 4 %p 가 신뢰 밴드 (docs/mpm_scaffold_reliability_and_am_freeze.md).
                dp, mpp = r.get('porosity'), m.get('porosity_mpm_pct')
                if dp and mpp is not None:
                    dp_pct = dp * 100.0 if dp <= 1.0 else dp
                    _gap = round(float(mpp) - dp_pct, 3)      # ★MPM − DEM (원 DB 는 반대 부호)
                    r['porosity_gap_mpm_minus_dem_pp'] = _gap
                    r['porosity_cross_validated'] = int(abs(_gap) <= GATE_BAND_PP)
                    # ★ regime-gate — ML 이 학습할 porosity 진실값
                    _dem_wins = _gap <= -GATE_BAND_PP        # MPM 과압축 (SE-poor corner)
                    r['use_source'] = 'DEM' if _dem_wins else 'MPM'
                    r['use_porosity_pct'] = round(dp_pct if _dem_wins else float(mpp), 3)
                    r['regime'] = ('SE-poor-corner(MPM-overcompress)' if _dem_wins else
                                   ('SE-rich(DEM-eps-artifact)' if _gap >= GATE_BAND_PP
                                    else 'cross-validated'))
                    cov['use_dem' if _dem_wins else 'use_mpm'] += 1
                    # 큐레이션 DB 에 있으면 신뢰등급·근거를 **덧붙인다** (규칙이 못 만드는 정보)
                    _cu = curated.get(r['name'])
                    r['reviewed'] = int(bool(_cu))
                    if _cu:
                        cov['reviewed'] += 1
                        r['trust_curated'] = _cu.get('trust')
                        r['verdict_curated'] = (_cu.get('verdict') or '')[:300]
                        r['se_of_solid_pct_curated'] = _cu.get('se_of_solid_pct')
                        # 큐레이션 판정과 자동 규칙이 갈리면 **드러낸다** (조용한 덮어쓰기 금지)
                        if _cu.get('use_source') and _cu['use_source'] != r['use_source']:
                            r['use_source_disagrees_with_curated'] = _cu['use_source']
        sp = _find_layer(r['name'], roots, glob_pat='step4_*viz*.json')
        if sp:
            v = _load_json(sp) or {}
            if v.get('kind') == 'step4_viz':
                r['has_step4'] = 1
                cov['step4'] += 1
                for k in S4_KEYS:
                    if k in v:
                        r['s4_' + k] = v[k]
                cu = v.get('curve') or {}
                xm = cu.get('x_mean') or []
                if len(xm) >= 2:
                    x0, x100 = v.get('x0'), v.get('x100')
                    if x0 is not None and x100 is not None and x100 != x0:
                        r['s4_delivered_frac'] = round(
                            abs(xm[-1] - xm[0]) / abs(float(x100) - float(x0)), 5)
    if verbose:
        print(f"  케이스 {cov['n']} · DEM {cov['dem']} · MPM {cov['mpm']} · STEP4 {cov['step4']}")
        nx = sum(1 for r in rows if r.get('porosity_cross_validated') == 1)
        nb = sum(1 for r in rows if 'porosity_gap_mpm_minus_dem_pp' in r)
        if nb:
            print(f"  ★frame[4] porosity 교차검증: {nx}/{nb} 가 |gap| ≤ 4 %p "
                  f"({nx / nb * 100:.0f}%)")
            _dis = sum(1 for r in rows if 'use_source_disagrees_with_curated' in r)
            print(f"  ★regime-gate: use MPM {cov['use_mpm']} / use DEM {cov['use_dem']}  "
                  f"· 큐레이션 판정 보유 {cov['reviewed']}건 (나머지는 reviewed=0 자동판정)"
                  + (f"  ⚠자동↔큐레이션 불일치 {_dis}건" if _dis else "  (불일치 0)"))
        if cov['step4'] == 0:
            print("  ⚠ STEP4 0건 — 성능 회귀 불가.  구조→성능은 "
                  "scripts/perf_reduced_order.py (적합 없는 물리) 로 간다.")
    return rows, cov


def write_csv(rows, path):
    import csv as _csv
    cols, seen = [], set()
    for r in rows:                                     # 열 순서 = 첫 등장 순 (재현 가능)
        for k in r:
            if k not in seen:
                seen.add(k)
                cols.append(k)
    os.makedirs(os.path.dirname(os.path.abspath(path)) or '.', exist_ok=True)
    with open(path, 'w', newline='') as fh:
        w = _csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cols})   # ★없는 층 = 빈칸 (0 아님)
    return cols


def _selftest():
    ok = tot = 0

    def chk(name, cond, extra=''):
        nonlocal ok, tot
        tot += 1
        ok += 1 if cond else 0
        print(f"  {'✓' if cond else '✗ FAIL'} {name}" + (f' — {extra}' if extra else ''))

    import tempfile
    import csv as _csv
    td = tempfile.mkdtemp(prefix='dpds_')
    res = os.path.join(td, 'results')
    lab = os.path.join(td, 'mpm_lab')
    # 합성 케이스 3개: (A) DEM+MPM+STEP4, (B) DEM+MPM, (C) DEM 만
    # ★ caseD 는 caseA 와 **지표가 완전히 동일**하고 이름만 다르다 — 옛 dedup(지표 튜플)이
    #   서로 다른 케이스를 지우는지 판별하는 유일한 fixture (형제-seed 실측 상황과 동형).
    for _i, (nm, mpm, s4) in enumerate(
            (('caseA', True, True), ('caseB', True, False), ('caseC', False, False),
             ('caseD_same_metrics_as_A', False, False),
             ('input_1mAh_100_14', True, False))):     # ★큐레이션 DB 에 실재 (use_source=DEM)
        if nm.startswith('caseD'):
            _i = 0                                        # caseA 와 지표 동일하게 강제
        # ★ input_1mAh_100_14 는 큐레이션 DB 의 실제 값 (DEM 18.2 / MPM 11.4 → gap −6.8 = 게이트 발동)
        _real = nm.startswith('input_')
        _mpm_por = 11.4 if _real else 16.7
        _dem_por = 0.182 if _real else 0.15
        d = os.path.join(res, nm)
        os.makedirs(d, exist_ok=True)
        # ★지표를 케이스별로 살짝 다르게 — 옛 dedup(지표 튜플)이면 여기서 3→1 로 뭉갰다
        json.dump({'phi_se': 0.30 + _i * 0.01, 'phi_am': 0.55, 'porosity': _dem_por,
                   'se_se_cn': 4.2, 'tortuosity_mean': 1.8 + _i * 0.05,
                   'thickness_um': 72.0 + _i, 'am_am_cn': 3.1,
                   'percolation_pct': 92.0, 'sigma_full_mScm': 0.20,
                   'electronic_sigma_full_mScm': 1.98, 'thermal_sigma_full_mScm': 8.0,
                   'coverage_AM_P_mean': 48.0, 'ps_ratio': '7:3'},
                  open(os.path.join(d, 'full_metrics.json'), 'w'))
        # LIGGGHTS 규약 d[µm] = r/scale·1e6·2 → r_SE 5e-4 = d_SE 1 µm (실제 침대 값)
        json.dump({'scale': 1000, 'r_SE': 5e-4, 'r_AM_P': 3e-3, 'r_AM_S': 1e-3,
                   'am_se_ratio': '80:20', 'box_x': 0.05},
                  open(os.path.join(d, 'input_params.json'), 'w'))
        if mpm:
            md = os.path.join(lab, nm)
            os.makedirs(md, exist_ok=True)
            # 실제 webapp payload 스키마 (188건 실측 확인)
            json.dump({'porosity_mpm_pct': _mpm_por, 'thickness_mpm_um': 71.2,
                       'coverage_AM_P_tabor_pct': 74.0, 'coverage_AM_P_rigid_tabor_pct': 70.0,
                       'coverage_AM_P_hertz_pct': 52.0, 'coverage_AM_P_rigid_hertz_pct': 46.0,
                       'coverage_AM_P_mpm_pct': 26.0,        # ★금지 키 — 들어오면 안 됨
                       'coverage_AM_S_mpm_pct': 25.0,        # ★금지 키
                       'dg_mean': 0.31, 'dg_max': 1.8, 'final_stress_GPa': 0.30,
                       'E_SE_GPa': 1.53, 'nu_SE': 0.49, 'protocol': 'hold'},
                      open(os.path.join(md, 'mpm_metrics.json'), 'w'))
        if s4:
            json.dump({'kind': 'step4_viz', 'c_rate': 2.0, 'charge': True,
                       'end_reason': 'V_cutoff', 'x0': 0.264, 'x100': 0.9084,
                       'curve': {'x_mean': [0.9084, 0.40]}},
                      open(os.path.join(d, 'step4_sched00n1_viz_chg_c2.json'), 'w'))
    rows, cov = build(res, os.path.join(td, 'archive'), lab, verbose=False)
    by = {r['name']: r for r in rows}
    chk('★dedup 이 이름-기준 — 지표가 같아도 다른 케이스는 남는다',
        cov['n'] == 5 and 'caseD_same_metrics_as_A' in by, f"{cov['n']}건: {sorted(by)}")
    chk('층 커버리지 정확 (MPM 3 · STEP4 1)', cov['mpm'] == 3 and cov['step4'] == 1)
    chk('★MPM 값이 mpm_ 접두사로 조인된다 (예측기가 0건 쓰던 층)',
        by['caseA'].get('mpm_porosity_mpm_pct') == 16.7
        and by['caseA'].get('mpm_thickness_mpm_um') == 71.2
        and by['caseA'].get('mpm_dg_mean') == 0.31)
    # ★★ CLAUDE.md 가 보고 금지한 복셀-인접 coverage 가 절대 안 들어와야 한다
    _leak = [k for k in by['caseA'] if k.endswith('_mpm_pct') and 'coverage' in k]
    chk('★금지 키(coverage_AM_*_mpm_pct, 복셀-인접 preview 아티팩트)가 차단된다',
        not _leak, f'누출: {_leak}' if _leak else '없음')
    # ★ MPM 고유 파생: 소성 − 강체 coverage 증분 (강체구 DEM 은 정의상 0)
    chk('★소성 conforming 증분이 계산된다 (plastic − rigid)',
        abs(by['caseA'].get('mpm_plastic_gain_AM_P_tabor_pp', 0) - 4.0) < 1e-9
        and abs(by['caseA'].get('mpm_plastic_gain_AM_P_hertz_pp', 0) - 6.0) < 1e-9,
        f"tabor +{by['caseA'].get('mpm_plastic_gain_AM_P_tabor_pp')} · "
        f"hertz +{by['caseA'].get('mpm_plastic_gain_AM_P_hertz_pp')} %p")
    # ★ regime-gate: gap 이 −4 를 넘으면(MPM 과압축) DEM 을 쓴다
    _cur = by.get('input_1mAh_100_14', {})
    chk('★regime-gate: MPM 과압축(gap ≤ −4) → use_source=DEM',
        _cur.get('use_source') == 'DEM' and _cur.get('regime','').startswith('SE-poor'),
        f"gap {_cur.get('porosity_gap_mpm_minus_dem_pp')} → {_cur.get('use_source')}")
    chk('★use_porosity_pct 가 선택된 모델의 값 (DEM 18.2)',
        abs((_cur.get('use_porosity_pct') or 0) - 18.2) < 1e-9, str(_cur.get('use_porosity_pct')))
    chk('★일치 케이스는 use_source=MPM + 그 값',
        by['caseA'].get('use_source') == 'MPM'
        and abs(by['caseA'].get('use_porosity_pct', 0) - 16.7) < 1e-9)
    # ★ 큐레이션 조인 — 규칙이 못 만드는 trust 등급이 붙는다
    chk('★큐레이션 DB 판정이 조인된다 (trust·verdict·reviewed)',
        _cur.get('reviewed') == 1 and _cur.get('trust_curated')
        and _cur.get('verdict_curated'),
        f"trust={_cur.get('trust_curated')}")
    chk('★큐레이션 없는 케이스는 reviewed=0 (자동판정임을 낙인)',
        by['caseA'].get('reviewed') == 0 and 'trust_curated' not in by['caseA'])
    chk('★자동 규칙이 큐레이션 use_source 와 일치 (불일치 플래그 없음)',
        'use_source_disagrees_with_curated' not in _cur)
    # ★ SE/solid = 원 DB 의 판별 축 (am_pct 아님)
    chk('★SE/solid 이 phi 에서 유도된다 (원 DB 판별 축)',
        abs(by['caseA'].get('se_of_solid_pct', 0) - 100*0.30/(0.30+0.55)) < 0.01,
        f"{by['caseA'].get('se_of_solid_pct')} %")
    chk('★frame[4] porosity gap = MPM − DEM (독립 측정 대조)',
        abs(by['caseA']['porosity_gap_mpm_minus_dem_pp'] - (16.7 - 15.0)) < 1e-9
        and by['caseA']['porosity_cross_validated'] == 1,
        f"{by['caseA']['porosity_gap_mpm_minus_dem_pp']:+.2f} %p")
    chk('STEP4 delivered = |Δx̄| / 창', abs(by['caseA']['s4_delivered_frac']
                                          - abs(0.40 - 0.9084) / (0.9084 - 0.264)) < 1e-5,
        f"{by['caseA']['s4_delivered_frac']:.4f}")
    chk('★없는 층은 채우지 않는다 (0 위장 금지)',
        'mpm_porosity_settled_pct' not in by['caseC']
        and by['caseC']['has_mpm'] == 0 and by['caseB']['has_step4'] == 0)
    # CSV: 빈칸이 정말 빈칸인가
    cp = os.path.join(td, 'corpus.csv')
    cols = write_csv(rows, cp)
    got = {r['name']: r for r in _csv.DictReader(open(cp))}
    chk('CSV 열이 모든 층의 합집합',
        'mpm_porosity_mpm_pct' in cols and 'mpm_plastic_gain_AM_P_tabor_pp' in cols
        and 's4_c_rate' in cols)
    chk('★MPM 없는 케이스의 MPM 칸이 빈 문자열 (0 아님)',
        got['caseC']['mpm_porosity_mpm_pct'] == ''
        and got['caseC']['mpm_plastic_gain_AM_P_tabor_pp'] == ''
        and got['caseC']['porosity'] not in ('', None))
    # 설계값은 predictor_engine 의 규약 d[µm] = r/scale·1e6·2 를 그대로 따라야 한다
    chk('설계값이 predictor_engine 유도와 동일 (재구현 안 함)',
        abs(float(got['caseA']['d_se']) - 1.0) < 1e-9
        and abs(float(got['caseA']['d_am']) - 6.0) < 1e-6
        and abs(float(got['caseA']['am_pct']) - 80.0) < 1e-9,
        f"d_se={got['caseA']['d_se']} d_am={got['caseA']['d_am']} "
        f"am_pct={got['caseA']['am_pct']}")
    # ★ P:S 는 full_metrics 의 ps_ratio 에서 (7:3 → 0.7)
    chk('P:S 분율이 ps_ratio 에서 유도된다 (7:3 → 0.7)',
        abs(float(got['caseA']['ps_frac']) - 0.7) < 1e-9, got['caseA']['ps_frac'])
    import shutil
    shutil.rmtree(td, ignore_errors=True)
    print(f"DESIGN-PERF-DATASET SELFTEST {ok}/{tot} {'PASS' if ok == tot else 'FAIL'}")
    return 0 if ok == tot else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--results', default=os.environ.get('WEBAPP_RESULTS_FOLDER', 'webapp/results'))
    ap.add_argument('--archive', default=os.environ.get('WEBAPP_ARCHIVE_FOLDER', 'webapp/archive'))
    ap.add_argument('--mpm-lab', default=os.environ.get('WEBAPP_MPM_LAB_FOLDER', 'webapp/mpm_lab'))
    ap.add_argument('--out', default='', help='CSV 경로 (미지정 = 커버리지만 인쇄)')
    a = ap.parse_args(argv)
    if a.selftest:
        raise SystemExit(_selftest())
    print(f'통합 데이터층 — results={a.results} · archive={a.archive} · mpm_lab={a.mpm_lab}')
    rows, cov = build(a.results, a.archive, a.mpm_lab)
    if not rows:
        print('  ⚠ 케이스 0건 — 경로를 확인하세요 (데이터는 dem-web 이 아니라 '
              '~/Yonghoon-DEM-DFT/webapp/* 에 있습니다)')
        return 1
    if a.out:
        cols = write_csv(rows, a.out)
        print(f'  → {a.out}  ({len(rows)} 행 × {len(cols)} 열)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
