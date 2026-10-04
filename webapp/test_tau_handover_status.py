#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""τ 결정 16 ② — 케이스 τ 블록의 **인계 상태 · 띠 규칙** 두 행 (웹앱 같은 묶음 J20-l · 1저자 비준 2026-10-04 *"권고대로"*).

계산은 도우미 `scripts/tau_flux.py` (v2 §5-1 열 · §5-2 게이트 G1–G6) 가 하고 웹앱은 **표시만** 한다 — 같은 정의 · 같은 이름 · 같은 한정어.
값 행 (tau2 · √tau2 · 비율) 은 그대로 둔다 (① 라벨 묶음) — 인계 열이 막히는 케이스 (띠 폴백 · 관통 불일치 · 옛 산출물) 를 화면에서 읽게 한다.

  T1 `_ion_handover(results_dir, metrics)` = tau_flux.ion_columns (dual 파일 + full_metrics 장부)
  T2 두 경로 (Step 4 · Step 4b) 에서 상태 행 "OK" · 띠 행 "L0 · 0.200" (H · P) · T2c 라우트와 같은 전체 체인 뒤 순서
  T3 안 A 전 산출물 (띠 규칙 기록 없음) → "NOT_COMPUTED (missing_input)" · 띠 행 "기록 없음 …"
  T4 `_ion_handover` 키가 없으면 행을 내지 않는다 (다른 렌더러 · 옛 시험 무영향)
  T5 키는 있는데 None (도우미를 못 불러옴) → "미계산 …"
  T6 비관통 (τ 블록 없음) 이어도 상태 행이 보인다 — NOT_PERCOLATING
  T7 번역 · 정렬 표 · 툴팁 · 별칭
  T8 케이스 라우트가 transform 전에 `_ion_handover` 를 붙인다

  python3 webapp/test_tau_handover_status.py
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))


STATUS = 'tau2 인계 상태 (게이트 G1–G6 · v2 §5-2)'
BAND = '띠 규칙 · 띠 폭/판 간격 (G1 · TAU-24)'
RATIO = 'τ_Lap,eff / τ_Dij (정의가 다른 두 τ 의 비)'


def res(mode, **kw):
    b = {'sigma_full': 0.05 if mode == 'hertzian' else 0.08, 'percolating_fraction': 0.9, 'boundary_rule': 'L0',
         'boundary_band_frac': 0.2, 'phi_se': 0.1995, 'resistance_model': 'maxwell' if mode == 'hertzian' else 'mikic',
         'psi_placement': 'legacy_divide', 'sigma_grain_S_cm': 0.003,
         'temperature_provenance': {'T_C': None, 'T_ref_C': 25.0, 'sigma_ion_T_factor': 1.0}}
    b.update(kw)
    return b


LED = {'thickness_um': 30.0, 'thickness_mass_conserving_um': 28.5, 'phi_se_mass_conserving': 0.21, 'percolation_pct': 92.0}
MET = dict(LED, phi_se=0.30, sigma_full_mScm=0.12, sigma_full_mScm_physics=0.30, sigma_bulk_net_mScm=0.50,
           tortuosity_mean=1.50, tortuosity_all_mean=1.45)


def case_dir(tmp, name, dual):
    d = os.path.join(tmp, name)
    os.makedirs(d)
    if dual is not None:
        with open(os.path.join(d, 'network_conductivity_dual.json'), 'w', encoding='utf-8') as fh:
            json.dump(dual, fh)
    return d


def main():
    import app as webapp

    def render(metrics, csv_net_section):
        data = [['Porosity(%)', 15.0], ['── 응력 ──', ''], ['Stress CV(%)', 40.0]]
        if csv_net_section:
            data = [['Porosity(%)', 15.0], ['── Network Solver (Hertzian DEM-native) ──', ''],
                    ['σ_ionic (mS/cm)', metrics.get('sigma_full_mScm')], ['── 응력 ──', ''], ['Stress CV(%)', 40.0]]
        tables = {'network_summary': {'columns': ['지표', '값'], 'data': [list(r) for r in data]}}
        webapp.transform_network_summary_4col(tables, metrics, {})
        return [list(r) for r in tables['network_summary']['data']]

    def row(rows, label):
        return next((r for r in rows if isinstance(r, list) and r and str(r[0]).strip() == label), None)

    tmp = tempfile.mkdtemp(prefix='tauho_')
    try:
        d_new = case_dir(tmp, 'new', {'hertzian': res('hertzian'), 'physics': res('physics')})
        ih = webapp._ion_handover(d_new, dict(MET))
        chk('T1 _ion_handover = tau_flux.ion_columns (dual + 장부) — 두 모드 OK · 같은 키',
            isinstance(ih, dict) and ih.get('ion_net_status_hertz') == 'OK' and ih.get('ion_net_status_physics') == 'OK'
            and 'tau2_ion_physics' in ih)
        for path_name, csvsec in (('Step 4', False), ('Step 4b', True)):
            rows = render(dict(MET, _ion_handover=ih), csvsec)
            st, bd = row(rows, STATUS), row(rows, BAND)
            chk(f'T2 [{path_name}] 상태 행 OK · OK · 띠 행 "L0 · 0.200" (H · P) · 각 한 번',
                st is not None and st[1] == 'OK' and st[2] == 'OK' and bd is not None and bd[1] == bd[2] == 'L0 · 0.200'
                and sum(1 for r in rows if r and r[0] == STATUS) == 1, repr((st, bd)))
            chk(f'T2b [{path_name}] 값 행 (tau2 · √tau2 · 비율) 은 그대로 있다 (표시만 더했다)', row(rows, RATIO) is not None)

        # T2c — 케이스 라우트와 같은 전체 체인 (transform → tier1 → Stage E → ASR → 정규화 → 논문 라벨) 뒤에도 두 행이 살아 있고
        #       비율 행 바로 뒤에 그 순서로 선다 (정규화가 모르는 행을 버리거나 뒤로 미는지까지 본다)
        data = [['Porosity(%)', 15.0], ['── Network Solver (Hertzian DEM-native) ──', ''], ['σ_ionic (mS/cm)', 0.12],
                ['── 응력 ──', ''], ['Stress CV(%)', 40.0]]
        tbl = {'network_summary': {'columns': ['지표', '값'], 'data': [list(r) for r in data]}}
        mm = dict(MET, _ion_handover=ih)
        webapp.transform_network_summary_4col(tbl, mm, {})
        webapp.inject_tier1_patch_rows(tbl, mm)
        webapp.inject_stage_e_rows(tbl, mm)
        webapp.inject_cell_asr_rows(tbl, mm, {})
        webapp.normalize_network_summary_layout(tbl, mm)
        webapp.apply_paper_labels(tbl)
        lab = [str(r[0]) for r in tbl['network_summary']['data'] if r]
        PLm = webapp._PAPER_LABEL_MAP
        want_seq = [PLm[RATIO], PLm[STATUS], PLm[BAND]]
        i0 = lab.index(want_seq[0]) if want_seq[0] in lab else -1
        chk('T2c 전체 체인 (정규화 · 논문 라벨) 뒤에도 비율 행 → 상태 행 → 띠 행 이 붙어 선다',
            i0 >= 0 and lab[i0:i0 + 3] == want_seq, repr(lab[i0:i0 + 3] if i0 >= 0 else lab))

        old = {'hertzian': res('hertzian'), 'physics': res('physics')}
        for r_ in old.values():
            r_.pop('boundary_rule')
            r_.pop('boundary_band_frac')
        ih3 = webapp._ion_handover(case_dir(tmp, 'old', old), dict(MET))
        rows3 = render(dict(MET, _ion_handover=ih3), True)
        st3, bd3 = row(rows3, STATUS), row(rows3, BAND)
        chk('T3 안 A 전 산출물 → 상태 "NOT_COMPUTED (missing_input)" · 띠 행 "기록 없음 …" (짐작하지 않는다)',
            st3 is not None and st3[1] == st3[2] == 'NOT_COMPUTED (missing_input)'
            and bd3 is not None and bd3[1].startswith('기록 없음'), repr((st3, bd3)))

        rows4 = render(dict(MET), True)
        chk('T4 _ion_handover 키 없음 → 인계 행 없음 (다른 렌더러 · 옛 시험 무영향)',
            row(rows4, STATUS) is None and row(rows4, BAND) is None)
        rows5 = render(dict(MET, _ion_handover=None), True)
        st5 = row(rows5, STATUS)
        chk('T5 키는 있는데 None (도우미 못 불러옴) → "미계산 …" 한 행', st5 is not None and str(st5[1]).startswith('미계산'), repr(st5))

        npd = {'hertzian': res('hertzian', percolating_fraction=0.0, sigma_full=None),
               'physics': res('physics', percolating_fraction=0.0, sigma_full=None)}
        m6 = dict(MET, percolation_pct=0.0, sigma_full_mScm=None, sigma_full_mScm_physics=None)
        ih6 = webapp._ion_handover(case_dir(tmp, 'nonperc', npd), m6)
        rows6 = render(dict(m6, _ion_handover=ih6), True)
        st6 = row(rows6, STATUS)
        chk('T6 비관통 (σ 없음 → τ 블록 없음) 이어도 상태 행 = NOT_PERCOLATING (H · P)',
            st6 is not None and st6[1] == st6[2] == 'NOT_PERCOLATING' and row(rows6, RATIO) is None, repr(st6))

        ihx = webapp._ion_handover(os.path.join(tmp, 'missing_case'), dict(MET))
        chk('T6b dual 파일 없는 케이스 → NOT_COMPUTED (missing_input) — 조용히 빠지지 않는다',
            isinstance(ihx, dict) and ihx['ion_net_status_hertz'] == 'NOT_COMPUTED'
            and ihx['ion_net_status_reason_hertz'] == 'missing_input')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ── T7 번역 · 정렬 · 툴팁 · 별칭 ──
    PL = webapp._PAPER_LABEL_MAP
    chk('T7a 두 라벨에 논문 라벨이 있다', STATUS in PL and BAND in PL)
    src = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    ci = src.find('_CANONICAL_ROW_ORDER = [')
    canon = src[ci:src.find(']', src.find('Electronic Active AM (%)', ci))] if ci >= 0 else ''
    chk('T7b 정렬 표: 비율 행 바로 뒤에 상태 · 띠 행 (그 순서)',
        RATIO in canon and STATUS in canon and BAND in canon
        and canon.index(RATIO) < canon.index(STATUS) < canon.index(BAND))
    html = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
    tip_s = html.find(f"'{STATUS}': {{")
    tip_b = html.find(f"'{BAND}': {{")
    body_s = html[tip_s:html.find('\n  },', tip_s)] if tip_s >= 0 else ''
    body_b = html[tip_b:html.find('\n  },', tip_b)] if tip_b >= 0 else ''
    chk('T7c 툴팁: 상태 행 = 다섯 상태 · 네 사유 · tau_flux · G5 값 유지 · 띠 행 = L0/L1/L2 · 4r_SE/L (TAU-24) · 안 A 전 산출물',
        all(w in body_s for w in ('OK', 'NOT_PERCOLATING', 'BAND_FALLBACK', 'MODEL_BELOW_CONTINUUM_BOUND', 'NOT_COMPUTED',
                                  'missing_input', 'percolation_disagree', 'solver_guard', 'temperature_mismatch', 'tau_flux'))
        and all(w in body_b for w in ('L0', 'L1', 'L2', '4r_SE/L', 'TAU-24')), (tip_s, tip_b))
    a = html.find('const PAPER_TO_ORIG = {')
    alias = html[a:html.find('};', a)] if a >= 0 else ''
    chk('T7d 별칭 표 (PAPER_TO_ORIG) 가 두 논문 라벨 → 원 라벨', f"'{PL.get(STATUS, '?')}'" in alias and f"'{STATUS}'" in alias
        and f"'{PL.get(BAND, '?')}'" in alias and f"'{BAND}'" in alias)

    # ── T8 라우트 배선 ──
    i_set = src.find("metrics['_ion_handover'] = _ion_handover(results_dir, metrics)")
    i_tr = src.find('    transform_network_summary_4col(tables, metrics, meta)')
    chk('T8 케이스 라우트가 transform 전에 _ion_handover 를 붙인다', 0 <= i_set < i_tr, (i_set, i_tr))

    print(f'\ntest_tau_handover_status: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
