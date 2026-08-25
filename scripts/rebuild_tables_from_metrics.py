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
#: ★★ **정본** — "이 케이스에 MPM porosity 가 있나" 를 판정하는 열 이름 전부.
#:   2026-08-25 실측: 이 목록이 **세 곳에 각자 적혀 있다가 갈라졌다** —
#:     ① `_NET` 표 행            → 별칭 있었음  ✓
#:     ② `mpm_metrics()`         → 없었음  → mpm_metrics.json 17건 누락
#:     ③ `rebuild_cases_from_csv.GAP_AXES` → 없었음  → "MPM 결손 23건" 오보
#:   같은 파일 안에서도 갈라졌으니 주석으로는 못 막는다.  ⇒ **여기 하나만 두고 나머지가
#:   가져다 쓴다**, 그리고 selftest 가 일치를 강제한다.
MPM_POROSITY_KEYS = ('mpm.porosity_mpm_pct', 'mpm_porosity_mpm_pct', 'mpm_porosity_pct')


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
    ('── MPM (압밀) ⚠ porosity 는 정본이 신뢰성 유보 (CL-04·플래튼 정본) ──', None, None),
    ('MPM Porosity(%)', MPM_POROSITY_KEYS, 2),
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


# ══ ⑤ MPM 결과 파라미터 (`mpm_metrics.json`) ══════════════════════════════════════
#  케이스 페이지의 **MPM 결과 파라미터** 박스는 탭이 아니라 `results/<id>/mpm_metrics.json`
#  을 읽는다 (`app._load_mpm_metrics`).  그 파일이 없으면 박스가 `display:none` 이다.
#  ⇒ 우리가 가진 MPM 지표로 그 파일을 만든다.
#  ⚠ `mpm_payload.json`(3D·무거움)은 못 만든다 — 원자료가 필요하다.  그래서 3D "MPM" 버튼과
#    `has_mpm` 배지는 여전히 꺼진다.  **파라미터 표만** 살아난다.
_MPM_KEYS = ('porosity_mpm_pct', 'thickness_mpm_um', 'bulk_density_g_cm3', 'se_fraction_pct',
             'compacted_porosity_pct', 'seed_porosity_pct', 'seed_AM_frac_pct',
             'seed_SE_frac_pct', 'E_SE_GPa', 'K_SE_GPa', 'nu_SE', 'sigma_y_GPa',
             'target_GPa', 'final_stress_GPa', 'protocol', 'n_am', 'n_grid', 'n_vox',
             'n_strain_pts', 'se_surface_tris', 'strain_kind', 'cov_method',
             'cov_hertz_um', 'cov_tabor_um', 'dg_mean', 'dg_max', 'dg_nonzero_pct',
             'dg_vmax98',
             'coverage_AM_P_hertz_pct', 'coverage_AM_P_tabor_pct', 'coverage_AM_P_mpm_pct',
             'coverage_AM_S_hertz_pct', 'coverage_AM_S_tabor_pct', 'coverage_AM_S_mpm_pct',
             'coverage_AM_P_rigid_hertz_pct', 'coverage_AM_P_rigid_tabor_pct',
             'coverage_AM_S_rigid_hertz_pct', 'coverage_AM_S_rigid_tabor_pct')


#: ⚠⚠ 2026-08-25 (사용자 지적) — 복원이 **규율 ④ 를 어길 뻔했다**.  MPM porosity 는
#:   정본이 신뢰성을 유보한 축인데, 표지 없이 UI 로 되돌리면 그 유보가 사라진다.
#:   ⇒ 되살릴 때 **경고를 함께 싣는다** (수치를 지우지는 않는다 — 지우면 왜 없는지 모른다).
MPM_POROSITY_CAVEAT = (
    '⚠⚠ MPM porosity 는 **정본이 신뢰성을 유보한 축**이다 (CLAUDE.md 트랙 2 · docs/mpm_platen_kinematic_stop_defect.md · docs/reviews/fam_platen_prereg_20260812.md): ① porosity 는 **정지 프레임의 함수**이고 속도 사다리(sub 40/80/160)에서 14.38 → 12.76 → 11.08 % 로 **수렴하지 않는다** ② scaffold 런에서 `solid_vol` 은 씨앗 시점에 DEM dump 로 고정된 상수라 **porosity 가 독립 정보를 담지 않는다** (MPM 의 유일한 출력은 wall_z) ③ 정지 결함을 고치면 ε_sphere 1.13 % = 실험 대비 **14.5 %p 과압축** (CL-04) ④ 따라서 **DEM↔MPM porosity 일치를 validity 증명서로 쓰면 순환**이다 — `cross-validated` 배지를 그렇게 읽지 말 것.  ⇒ 살아 있는 MPM 산출물: **응력-정지 두께** · 형태(morphology) · 소성 변형장.')



#: 같은 양인데 **표마다 열 이름이 다르다** → 명시적 별칭표.
#:  ⚠⚠ 2026-08-25 실측 — 접미사 깎기 휴리스틱(`k[:-4]`)이 조용히 빗나갔다:
#:    `porosity_mpm_pct` → `mpm_porosity_mpm` 을 찾는데 실제 열은 `mpm_porosity_pct` 라
#:    **17건이 통째로 누락**됐다 (a9_p00~p10 · 2mAh_real_16~20 · 8mAh_real_11~15 · 1mAh_100_15).
#:    나는 그걸 "원래 MPM 이 없는 케이스" 로 사용자에게 잘못 말했다.  추측 대신 표를 읽는다.
#:  ★ 같은 양임을 확인하고 넣었다: 두 열을 다 가진 **139건에서 중앙 |Δ| = 0.0000**
#:    (135건 완전 일치).  어긋나는 4건은 corpus 열이 우선이라 영향 없다
#:    (최대 input_1mAh_100_10 Δ 5.87 — 이 불일치 자체는 별도 항목).
#:  ⇒ corpus 열(`mpm_<key>`)을 **먼저** 보고, 없을 때만 별칭을 쓴다.
#:  ⇒ 표준 조회(`mpm.<k>` · `mpm_<k>`)로 **안 잡히는 것만** 별칭이다 — 손으로 안 적고 뺀다.
_MPM_ALIASES = {
    #  mpm_dem_porosity_reliability.csv · case_3d_collection.csv 의 열 이름
    'porosity_mpm_pct': tuple(k for k in MPM_POROSITY_KEYS
                              if k not in ('mpm.porosity_mpm_pct', 'mpm_porosity_mpm_pct')),
}


def mpm_metrics(m):
    """중첩 `mpm.*` (풍부) 를 우선하고, 없으면 평평한 `mpm_*` 에서 접두사를 떼어 모은다."""
    nested = m.get('mpm') if isinstance(m.get('mpm'), dict) else {}
    out = {k: v for k, v in nested.items() if v is not None}
    for k in _MPM_KEYS:
        if k in out:
            continue
        v = m.get('mpm_' + k)
        if v is None and k.endswith('_pct'):
            v = m.get('mpm_' + k[:-4])          # mpm_se_fraction 같은 축약형
        if v is None:
            for alias in _MPM_ALIASES.get(k, ()):
                v = m.get(alias)
                if v is not None:
                    break
        if v is not None:
            out[k] = v
    #  ⚠ 하나도 없으면 파일을 안 만든다 — 빈 박스를 띄우지 않는다
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
    per_table['mpm_metrics'] = 0
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
        mm = mpm_metrics(m)
        if mm:
            pmm = os.path.join(d, 'mpm_metrics.json')
            if os.path.exists(pmm):
                skipped += 1
            else:
                per_table['mpm_metrics'] = per_table.get('mpm_metrics', 0) + 1
                made += 1
                if write:
                    with open(pmm, 'w', encoding='utf-8') as f:
                        json.dump({**mm, '_reconstructed': True,
                                   '_reconstructed_note': 'CSV 유래 — 재실행 아님.  '
                                                          'mpm_payload.json(3D)은 없다',
                                   '_porosity_caveat': MPM_POROSITY_CAVEAT},
                                  f, ensure_ascii=False, indent=1)
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
    chk('⑮ ★ MPM 이 없으면 mpm_metrics 도 안 만든다', mpm_metrics({'porosity': 1}) is None)
    chk('⑮a ★★ porosity 유보 경고문이 정본 근거를 지목한다 (규율 ④)',
        'CL-04' in MPM_POROSITY_CAVEAT and '순환' in MPM_POROSITY_CAVEAT
        and 'mpm_platen_kinematic_stop_defect' in MPM_POROSITY_CAVEAT)
    chk('⑮b ★ MPM 섹션 머리글에도 유보가 붙는다',
        any('신뢰성 유보' in lbl for lbl, k, _ in _NET if k is None and 'MPM' in lbl))
    mm = mpm_metrics({'mpm': {'porosity_mpm_pct': 15.9, 'E_SE_GPa': 1.53}})
    chk(f'⑯ 중첩 mpm.* 를 그대로 쓴다 ({sorted(mm)})', mm['E_SE_GPa'] == 1.53)
    mm2 = mpm_metrics({'mpm_porosity_mpm_pct': 20.9, 'mpm_thickness_mpm_um': 115.2})
    chk(f'⑰ ★ 평평한 mpm_* 도 접두사를 떼어 모은다 ({sorted(mm2)})',
        mm2.get('porosity_mpm_pct') == 20.9 and mm2.get('thickness_mpm_um') == 115.2)
    # ── ⑱ 표마다 열 이름이 다른 문제 — 접미사 깎기가 17건을 조용히 놓쳤다 ────────────────
    mm3 = mpm_metrics({'mpm_porosity_pct': 27.42})
    chk(f'⑱a ★★ `mpm_porosity_pct`(reliability·3d 표 이름)도 잡는다 ({mm3})',
        mm3 is not None and mm3.get('porosity_mpm_pct') == 27.42)
    mm4 = mpm_metrics({'mpm_porosity_mpm_pct': 21.78, 'mpm_porosity_pct': 15.91})
    chk('⑱b ★ 둘 다 있으면 **corpus 열이 이긴다** (별칭은 대타일 뿐)',
        mm4.get('porosity_mpm_pct') == 21.78)
    #  ★★ 복사본 표류 감시 — 같은 파일 안에 키 목록이 **둘** 있다 (표 행 · mpm_metrics).
    #     실제로 갈라져 있었다: 표 행엔 `mpm_porosity_pct` 가 있었는데 mpm_metrics 엔 없었다.
    _row_cands = next(c for lab, c, _ in _NET if lab == 'MPM Porosity(%)')
    _mm_cands = ('mpm.porosity_mpm_pct', 'mpm_porosity_mpm_pct') + \
        _MPM_ALIASES['porosity_mpm_pct']
    chk(f'⑱c ★★ 표 행과 mpm_metrics 의 porosity 열 이름이 **같은 집합** ({len(_row_cands)}개)',
        set(_row_cands) == set(_mm_cands))
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
