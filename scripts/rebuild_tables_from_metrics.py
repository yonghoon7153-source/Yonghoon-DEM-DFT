#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`full_metrics.json` → 분석 요약 **탭 CSV 4종** 재생성.

★ 왜 (2026-08-25): 윈도우 재설치로 `webapp/results/*` 를 잃었다.  `rebuild_cases_from_csv.py`
  가 `case_master.csv`(163 케이스 × 421 지표)에서 `full_metrics.json` 을 되살렸는데,
  **분석 요약 탭 6개 중 2개만 떴다**.  이유는 데이터가 아니라 **배관**이었다:

    · 취성 파괴 · 종합 등급  → `full_metrics.json` 에서 **조립**한다  → 살아났다
    · 입자 정보 · 접촉 요약 · 배위수 · 네트워크 지표
                            → `results/<id>/*.csv` **파일을 읽는다**  → 파일이 없어 안 뜬다

  ⇒ 그 넷도 `full_metrics.json` 에서 만들어 준다 (취성 탭이 이미 하는 방식의 확장).

⚠⚠ 정직 계약 — **없는 것은 만들지 않는다**:
  · 키가 없으면 그 **행을 아예 안 만든다** (0 이나 '-' 로 채우지 않는다)
  · 그 결과 섹션이 비면 **섹션 머리글도 안 넣는다**
  · 각 CSV 첫 행에 `── 복원(CSV 유래) ──` 머리글을 넣어 **재실행 결과와 구분**한다
  · **기존 CSV 는 덮지 않는다** (진짜 런이 있으면 그쪽이 정본)

⚠ **배위수 탭은 원본과 같은 양이 아니다.**  원래 `coordination_summary.csv` 의 배위수는
  **입자당 총 접촉 수**(모든 쌍유형 합)인데, 우리가 가진 것은 **쌍유형별 CN**(AM_P–SE 등)뿐이다.
  총 배위수는 원자료(접촉 덤프) 없이는 복원할 수 없다.  ⇒ 열 이름을 `SE와의 배위수` 로 바꾸고
  머리글에 그렇게 적는다.  같은 이름으로 다른 양을 내놓지 않는다.

  python3 scripts/rebuild_tables_from_metrics.py --check
  python3 scripts/rebuild_tables_from_metrics.py --write
  python3 scripts/rebuild_tables_from_metrics.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))


def _data_root():
    return os.environ.get('DEM_WEB_DATA') or os.path.join(os.path.expanduser('~'),
                                                          'Yonghoon-DEM-DFT')


def _g(m, *path):
    """중첩 dict 조회.  없으면 None.  (점 표기 키도 받는다)"""
    for p in path:
        cur = m
        for part in str(p).split('.'):
            if not isinstance(cur, dict) or part not in cur:
                cur = None
                break
            cur = cur[part]
        if cur is not None:
            return cur
    return None


def _r(v, n=2):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return v
    return int(f) if n == 0 else round(f, n)


# ══ ① 입자 정보 ═══════════════════════════════════════════════════════════════════
def atom_statistics(m):
    rows = []
    for name, n_key, r_key in (('AM_P', 'AM_P_n_particles', ('r_AM_P', 'inp.r_AM_P')),
                               ('AM_S', 'AM_S_n_particles', ('r_AM_S', 'inp.r_AM_S')),
                               ('SE', 'n_SE', ('r_SE', 'inp.r_SE'))):
        n = _g(m, n_key)
        if n is None:
            continue                       # 없는 상은 행을 안 만든다
        row = {'입자유형': name, '입자수': _r(n, 0)}
        rad = _g(m, *r_key)
        row['반지름(μm)'] = _r(rad, 3) if rad is not None else '-'
        #  영률: SE 만 기록돼 있다 (e_se_eff_gpa).  AM 은 없으므로 '-' — 140 을 지어넣지 않는다.
        if name == 'SE':
            e = _g(m, 'e_se_eff_gpa')
            row['영률'] = f'{_r(e, 2)} GPa (유효)' if e is not None else '-'
        else:
            row['영률'] = '-'
        rows.append(row)
    return rows or None


# ══ ② 접촉 요약 ═══════════════════════════════════════════════════════════════════
_CT = ('AM_P-SE', 'AM_S-SE', 'AM전체-SE', 'SE-SE', 'AM_P-AM_P', 'AM_S-AM_S', 'AM_P-AM_S')


def contact_summary(m):
    rows = []
    for ct in _CT:
        base = 'area_' + ct.replace('-', '_')
        n = _g(m, base + '_n')
        if n is None:
            continue
        row = {'접촉유형': ct, '접촉수': _r(n, 0)}
        mean = _g(m, base + '_mean')
        tot = _g(m, base + '_total')
        row['접촉면적_mean(μm²)'] = _r(mean, 4) if mean is not None else '-'
        row['접촉면적_total(μm²)'] = _r(tot, 2) if tot is not None else '-'
        rows.append(row)
    return rows or None


# ══ ③ 배위수 (⚠ 쌍유형 CN — 총 배위수 아님) ════════════════════════════════════════
def coordination_summary(m):
    rows = []
    for name, n_key, pre in (('AM_P', 'AM_P_n_particles', 'AM_P_se_cn'),
                             ('AM_S', 'AM_S_n_particles', 'AM_S_se_cn')):
        n = _g(m, n_key)
        mean = _g(m, pre + '_mean')
        if n is None or mean is None:
            continue
        rows.append({'입자유형': name, '입자수': _r(n, 0),
                     'SE와의 배위수_mean': _r(mean),
                     'SE와의 배위수_std': _r(_g(m, pre + '_std')),
                     'SE와의 배위수_median': _r(_g(m, pre + '_median')),
                     'SE와의 배위수_max': _r(_g(m, pre + '_max'))})
    se_cn = _g(m, 'se_se_cn')
    if se_cn is not None:
        rows.append({'입자유형': 'SE', '입자수': _r(_g(m, 'n_SE'), 0),
                     'SE와의 배위수_mean': _r(se_cn),
                     'SE와의 배위수_std': _r(_g(m, 'se_se_cn_std')),
                     'SE와의 배위수_median': '-', 'SE와의 배위수_max': '-'})
    if not rows:
        return None
    #  ⚠ 같은 이름으로 다른 양을 내놓지 않기 위한 명시 (템플릿이 `──` 를 구분선으로 렌더)
    return [{'입자유형': '── 복원: **쌍유형 CN** (원본의 총 배위수와 다른 양) ──',
             '입자수': '', 'SE와의 배위수_mean': '', 'SE와의 배위수_std': '',
             'SE와의 배위수_median': '', 'SE와의 배위수_max': ''}] + rows


# ══ ④ 네트워크 지표 (지표/값 2열, `──` 는 섹션 머리글) ═══════════════════════════════
#  (라벨, 키 후보…, 소수자리) — 키가 없으면 **행을 안 만든다**
_NET = [
    ('── 구조 ──', None, None),
    ('Porosity(%)', ('porosity', 'porosity_spheresum'), 2),
    ('전극두께(μm)', ('thickness_um',), 2),
    ('── 계면 ──', None, None),
    ('AM-SE Total(μm²)', ('area_AM전체_SE_total',), 2),
    ('SE-SE Total(μm²)', ('area_SE_SE_total',), 2),
    ('Coverage AM_P(%)', ('coverage_AM_P_mean',), 1),
    ('Coverage AM_S(%)', ('coverage_AM_S_mean',), 1),
    ('── 이온경로: 연결성 ──', None, None),
    ('SE-SE CN mean', ('se_se_cn',), 2),
    ('SE-SE CN std', ('se_se_cn_std',), 2),
    ('SE Cluster 수', ('n_components',), 0),
    ('SE Percolation(%)', ('percolation_pct',), 1),
    ('Top Reachable(%)', ('top_reachable_pct',), 1),
    ('── 이온경로: 경로 효율 ──', None, None),
    ('Tortuosity mean', ('tortuosity_mean',), 2),
    ('Tortuosity median', ('tortuosity_median',), 2),
    ('Tortuosity std', ('tortuosity_std',), 2),
    ('GB Density(hops/μm)', ('gb_density_mean',), 3),
    ('── 이온경로: 경로 품질 ──', None, None),
    ('Path Hop Area mean(μm²)', ('path_hop_area_mean',), 4),
    ('Path Conductance(μm²)', ('path_conductance_mean',), 4),
    ('── 활성도 ──', None, None),
    ('AM-SE CN mean', ('am_se_cn_mean',), 2),
    ('  ├ AM_P-SE CN mean', ('AM_P_se_cn_mean',), 2),
    ('  ├ AM_S-SE CN mean', ('AM_S_se_cn_mean',), 2),
    ('  └ AM-SE CN (surface-weighted)', ('am_se_cn_surface_weighted',), 2),
    ('Ionic Active AM(%)', ('ionic_active_pct',), 1),
    ('AM Vulnerable(%)', ('am_vulnerable_pct',), 1),
    ('  ├ AM_P Vulnerable(%)', ('AM_P_vulnerable_pct',), 1),
    ('  └ AM_S Vulnerable(%)', ('AM_S_vulnerable_pct',), 1),
    ('── 이온전도 ──', None, None),
    ('SE Volume Fraction', ('phi_se',), 3),
    ('σ_brug/σ_grain (Bruggeman)', ('sigma_ratio',), 4),
    ('── Network Solver (Hertzian DEM-native) ──', None, None),
    ('σ_ionic (mS/cm)', ('sigma_full_mScm',), 4),
    ('R_brug (과대추정 배수)', ('R_brug_over_full',), 1),
    ('σ_electronic (mS/cm)', ('electronic_sigma_full_mScm',), 2),
    ('σ_thermal (mS/cm equiv)', ('thermal_sigma_full_mScm',), 3),
    ('── Physics (Plastic film, Tabor+volume) ──', None, None),
    ('σ_ionic [physics] (mS/cm)', ('sigma_full_mScm_physics',), 4),
    ('σ_electronic [physics] (mS/cm)', ('electronic_sigma_full_mScm_physics',), 2),
    ('σ_thermal [physics] (mS/cm equiv)', ('thermal_sigma_full_mScm_physics',), 3),
    #  ── MPM (압밀 시뮬) ──  키가 두 갈래다: 중첩 `mpm.*`(case_master 27건) 와
    #     평평한 `mpm_*`(코퍼스 146건).  둘 다 후보로 넣어 **있는 쪽**을 쓴다.
    ('── MPM (압밀) ──', None, None),
    ('MPM Porosity(%)', ('mpm.porosity_mpm_pct', 'mpm_porosity_mpm_pct', 'mpm_porosity_pct'), 2),
    ('MPM 압밀 Porosity(%)', ('mpm.compacted_porosity_pct', 'mpm_compacted_porosity_pct'), 2),
    ('MPM seed Porosity(%)', ('mpm.seed_porosity_pct', 'mpm_seed_porosity_pct'), 2),
    ('MPM 두께(μm)', ('mpm.thickness_mpm_um', 'mpm_thickness_mpm_um'), 2),
    ('MPM ρ_bulk(g/cm³)', ('mpm.bulk_density_g_cm3', 'mpm_bulk_density_g_cm3'), 3),
    ('MPM SE 분율(%)', ('mpm.se_fraction_pct', 'mpm_se_fraction_pct'), 2),
    ('  ├ Coverage AM_P Hertz(%)', ('mpm.coverage_AM_P_hertz_pct', 'mpm_coverage_AM_P_hertz_pct'), 1),
    ('  ├ Coverage AM_P Tabor(%)', ('mpm.coverage_AM_P_tabor_pct', 'mpm_coverage_AM_P_tabor_pct'), 1),
    ('  ├ Coverage AM_S Hertz(%)', ('mpm.coverage_AM_S_hertz_pct', 'mpm_coverage_AM_S_hertz_pct'), 1),
    ('  └ Coverage AM_S Tabor(%)', ('mpm.coverage_AM_S_tabor_pct', 'mpm_coverage_AM_S_tabor_pct'), 1),
    ('  · rigid 대조 AM_P Tabor(%)', ('mpm.coverage_AM_P_rigid_tabor_pct', 'mpm_coverage_AM_P_rigid_tabor_pct'), 1),
    ('소성변형 dg_mean', ('mpm.dg_mean', 'mpm_dg_mean'), 4),
    ('소성변형 dg_max', ('mpm.dg_max',), 4),
    ('소성변형 nonzero(%)', ('mpm.dg_nonzero_pct',), 1),
    ('MPM E_SE(GPa)', ('mpm.E_SE_GPa',), 2),
    ('MPM σ_y(GPa)', ('mpm.sigma_y_GPa',), 3),
    ('MPM ν_SE', ('mpm.nu_SE',), 3),
    ('MPM 최종응력(GPa)', ('mpm.final_stress_GPa',), 3),
    ('MPM protocol', ('mpm.protocol',), None),
    ('MPM n_grid', ('mpm.n_grid',), 0),
    ('── 응력 ──', None, None),
    ('Stress CV(%)', ('stress_cv',), 1),
    ('σ_AM_P/σ_mean', ('stress_ratio_AM_P',), 3),
    ('σ_AM_S/σ_mean', ('stress_ratio_AM_S',), 3),
    ('σ_SE/σ_mean', ('stress_ratio_SE',), 3),
]


def network_summary(m):
    out, pending = [], None
    for label, keys, nd in _NET:
        if keys is None:
            pending = label                     # 섹션 머리글은 **내용이 생길 때만** 넣는다
            continue
        v = _g(m, *keys)
        if v is None:
            continue
        if pending:
            out.append({'지표': pending, '값': ''})
            pending = None
        out.append({'지표': label, '값': (v if nd is None else _r(v, nd))})
    #  Constriction 은 유도량 (1 − bulk_resistance_fraction)
    brf = _g(m, 'bulk_resistance_fraction')
    if brf is not None:
        out.append({'지표': 'Constriction 비율(%)', '값': round((1 - float(brf)) * 100, 1)})
    return out or None


TABLES = {'atom_statistics': atom_statistics, 'contact_summary': contact_summary,
          'coordination_summary': coordination_summary, 'network_summary': network_summary}
#: 첫 행에 넣는 복원 표식 (템플릿이 `──` 로 시작하는 행을 구분선으로 렌더한다)
_BANNER = '── 복원(CSV 유래) — 재실행 아님 ──'


def build(metrics):
    """→ {name: rows}  ·  만들 수 없는 표는 아예 안 넣는다."""
    out = {}
    for name, fn in TABLES.items():
        rows = fn(metrics)
        if not rows:
            continue
        head = dict.fromkeys(rows[0], '')
        head[list(rows[0])[0]] = _BANNER
        out[name] = [head] + rows
    return out


def run(data_root=None, write=False):
    dr = data_root or _data_root()
    rs = os.path.join(dr, 'webapp', 'results')
    made = skipped = nocase = 0
    per_table = {k: 0 for k in TABLES}
    if not os.path.isdir(rs):
        return {'error': f'results 폴더가 없다: {rs}'}
    for cid in sorted(os.listdir(rs)):
        d = os.path.join(rs, cid)
        fm = os.path.join(d, 'full_metrics.json')
        if not os.path.isfile(fm):
            nocase += 1
            continue
        try:
            with open(fm, encoding='utf-8') as f:
                m = json.load(f)
        except (OSError, ValueError):
            nocase += 1
            continue
        for name, rows in build(m).items():
            p = os.path.join(d, f'{name}.csv')
            if os.path.exists(p):
                skipped += 1
                continue          # ⚠ 진짜 런이 있으면 그쪽이 정본 — 안 덮는다
            per_table[name] += 1
            if write:
                with open(p, 'w', encoding='utf-8', newline='') as f:
                    w = csv.DictWriter(f, fieldnames=list(rows[0]))
                    w.writeheader()
                    w.writerows(rows)
            made += 1
    return {'made': made, 'skipped': skipped, 'no_metrics': nocase,
            'per_table': per_table, 'root': rs}


def _selftest():
    import tempfile
    n = [0, 0]

    def chk(msg, ok):
        n[1] += 1
        n[0] += bool(ok)
        print(f'  {"PASS" if ok else "FAIL"}  {msg}')

    full = {'AM_P_n_particles': 36, 'AM_S_n_particles': 421, 'n_SE': 32833,
            'r_AM_P': 6.0, 'r_AM_S': 2.0, 'r_SE': 0.5, 'e_se_eff_gpa': 1.35,
            'area_SE_SE_n': 100, 'area_SE_SE_mean': 0.01, 'area_SE_SE_total': 1.0,
            'AM_P_se_cn_mean': 12.3, 'AM_P_se_cn_std': 1.1, 'AM_P_se_cn_median': 12,
            'AM_P_se_cn_max': 20, 'se_se_cn': 6.5, 'se_se_cn_std': 1.2,
            'porosity': 15.6, 'thickness_um': 30.3, 'tortuosity_mean': 1.4,
            'sigma_full_mScm': 0.137, 'bulk_resistance_fraction': 0.4,
            'percolation_pct': 99.0}
    t = build(full)
    chk(f'① 네 표를 다 만든다 ({sorted(t)})', set(t) == set(TABLES))
    chk('② 첫 행이 복원 표식', all(_BANNER in list(v[0].values()) for v in t.values()))
    chk(f'③ 입자 정보 3상 ({len(t["atom_statistics"]) - 1}행)',
        len(t['atom_statistics']) == 4)
    chk('④ ★ AM 영률은 없으므로 "-" — 140 을 지어넣지 않는다',
        all(r['영률'] == '-' for r in t['atom_statistics'][1:] if r['입자유형'] != 'SE'))
    chk('⑤ ★ 배위수 표가 **총 배위수가 아님**을 밝힌다',
        '쌍유형 CN' in t['coordination_summary'][1]['입자유형'])
    labels = [r['지표'] for r in t['network_summary']]
    chk(f'⑥ 네트워크 지표 {len(labels)}행 · 있는 키만',
        'Porosity(%)' in labels and 'σ_ionic (mS/cm)' in labels)
    chk('⑦ ★ 없는 키는 행을 안 만든다 (GB Density 없음)',
        not any('GB Density' in x for x in labels))
    chk('⑧ ★ 내용 없는 섹션은 **머리글도 안 넣는다**',
        '── 응력 ──' not in labels and '── 구조 ──' in labels)
    chk('⑨ Constriction 은 유도 (1−bulk_resistance_fraction = 60.0)',
        any(r['지표'] == 'Constriction 비율(%)' and r['값'] == 60.0
            for r in t['network_summary']))
    thin = build({'porosity': 1.0})
    chk(f'⑩ ★ 지표가 거의 없으면 만들 수 있는 표만 ({sorted(thin)})',
        set(thin) == {'network_summary'})
    chk('⑪ 아무것도 없으면 아무 표도 안 만든다', build({}) == {})
    with tempfile.TemporaryDirectory() as d:
        cd = os.path.join(d, 'webapp', 'results', 'C1')
        os.makedirs(cd)
        json.dump(full, open(os.path.join(cd, 'full_metrics.json'), 'w', encoding='utf-8'))
        r1 = run(d, write=True)
        chk(f'⑫ 파일을 실제로 만든다 ({r1["made"]}개)',
            r1['made'] == 4 and os.path.exists(os.path.join(cd, 'network_summary.csv')))
        with open(os.path.join(cd, 'network_summary.csv'), encoding='utf-8') as f:
            back = list(csv.DictReader(f))
        chk(f'⑬ 다시 읽힌다 ({len(back)}행)', len(back) >= 5 and back[0]['지표'] == _BANNER)
        r2 = run(d, write=True)
        chk(f'⑭ ★ 기존 CSV 는 **안 덮는다** (재실행 made {r2["made"]} skip {r2["skipped"]})',
            r2['made'] == 0 and r2['skipped'] == 4)
    print(f'\nrebuild_tables_from_metrics selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    res = run(write=a.write)
    if res.get('error'):
        raise SystemExit(res['error'])
    print(f'대상 {res["root"]}')
    for k, v in sorted(res['per_table'].items()):
        print(f'   {k:<22} {v:>4} 케이스')
    print(f'   합계 {res["made"]}개 CSV · 이미 있어 건너뜀 {res["skipped"]} · '
          f'metrics 없음 {res["no_metrics"]}')
    if a.write:
        print('\n✓ 썼다.  `demstop; dem5002` 로 다시 띄우면 탭이 켜진다.')
        print('  ⚠ 첫 행 `── 복원(CSV 유래) ──` = 재실행이 아니다.')
        print('  ⚠ 배위수 탭은 **쌍유형 CN** 이다 (원본의 총 배위수와 다른 양).')
    else:
        print('\n(--check — 쓰지 않았다.  실제로 쓰려면 --write)')
