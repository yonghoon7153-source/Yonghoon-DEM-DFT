#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-S04 (Codex 재확인 2 판정 §5 · 표기 L214RR2-04) — 과거 · 외부 메트릭의 null 이 `/single` 을 500 으로 죽이지 않는다 (시험 먼저).

  python3 webapp/test_single_null_metrics.py          # 종료코드 0 = 전부 PASS

근거 = Codex 재확인 2 판정문 `docs/reviews/codex_review_lhs214rr_fix_recheck_20261019.md` §5 · 수정 계획 `docs/reviews/lhs214s_fix_plan_20261019.md`
(1저자 10-19 Q4 = 같이 고침).  Codex 반례 = 채택 이온값 H .24 · P .72 그대로 · 보조 메트릭 `sigma_ratio` 만 JSON null → loader 성공 · `/single` 500
(`single.html` 의 `%.4f` · 툴팁 곱셈).  현재 생산자는 None 이면 키를 넣지 않는다 (`analyze_contacts.py` — 정상 생산자가 null 을 쓴다는 증거 없음) →
과거 · 외부 nullable 자료의 화면 견고성.

★ 시험 먼저 — 고치기 전 템플릿에서 빨갛다: sigma_ratio · phi_se · percolation_pct · tortuosity_* 가 null 이면 500 · sigma_ratio 키가 없으면 툴팁이
  지어낸 '0.0000'.  고친 뒤 = 그 툴팁 세 개 (σ_brug/σ_grain · σ_brug / σ_ionic · σ_Bruggeman) 가 숫자일 때만 형식화 · 곱셈하고 아니면 '—' 또는 일반 문구.
대조 (그대로) — 정상 케이스의 세 툴팁 수치 (= 0.2400 · 0.7200 / 0.2400 · 0.7200 mS/cm) · R_brug null = 200 (Codex 대조).
⚠ 범위 — `/single` 의 이 세 툴팁 블록 (서버 Jinja).  single.html 전체의 모든 nullable 메트릭 렌더 보증 아님 · 브라우저 JS (what-if 응답) 아님 · app.py 안 건드림.
  같은 부류 남은 것 = 머리 배지 (`percolation_pct` 등 `is defined` 만 보고 형식화 — null 이면 여전히 500 · 10-19 실측) → 원장 `L214R-S05` (범위 밖 · 따로).
"""
import contextlib
import csv
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (HERE, os.path.join(os.path.dirname(HERE), 'scripts')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

#  케이스 · 보관함 폴더 = 임시 폴더 (리포 안 webapp/results 를 건드리지 않는다) — app import 전에
WORK = tempfile.mkdtemp(prefix='single_null_')
for _k, _n in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
               ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
    os.environ[_k] = os.path.join(WORK, _n)
os.environ['MPLCONFIGDIR'] = os.path.join(WORK, 'mplconfig')
os.environ['SUPABASE_URL'] = ''
os.environ['SUPABASE_KEY'] = ''

_ok, _fail = 0, []


def chk(label, ok, detail=''):
    global _ok
    if ok:
        _ok += 1
        print(f'  PASS  {label}')
    else:
        _fail.append(label)
        print(f'  FAIL  {label}' + (f'   {str(detail)[:400]}' if detail else ''))
    return ok


#: Codex 반례의 정상 메트릭 (채택 이온값 H .24 · P .72 · sigma_ratio .24 · σ₀ 3.0 mS/cm)
BASE = dict(sigma_full_mScm=.24, sigma_full_mScm_physics=.72, sigma_full_status='computed', sigma_full_status_physics='computed',
            network_solver_status='success', sigma_ratio=.24, sigma_grain_S_cm=.003, phi_se=.5, percolation_pct=100.0,
            sigma_bulk_net_mScm=1., sigma_bulk_net_mScm_physics=1., R_brug_over_full=7.2, R_brug_over_full_physics=2.4,
            bulk_resistance_fraction=.6, bulk_resistance_fraction_physics=.8, electronic_sigma_full_mScm=2.,
            electronic_sigma_full_mScm_physics=3., thermal_sigma_full_mScm=.3, thermal_sigma_full_mScm_physics=.45,
            tortuosity_mean=1.2, tortuosity_recommended=1.2)
ROWS = [['── Network Solver (Hertzian DEM-native) ──', '', '', ''], ['σ_ionic (mS/cm)', '0.24', '0.72', '+200.0%'], ['SE Volume Fraction', '.5', '.5', '0%']]
DROP = object()


def page(client, name, mut):
    m = dict(BASE)
    for k, v in mut.items():
        if v is DROP:
            m.pop(k, None)
        else:
            m[k] = v
    rd, ud = os.path.join(WORK, 'results', name), os.path.join(WORK, 'uploads', name)
    os.makedirs(rd, exist_ok=True)
    os.makedirs(ud, exist_ok=True)
    with open(os.path.join(rd, 'full_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(m, f)
    with open(os.path.join(ud, 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(name=name, status='done', scale=1), f)
    with open(os.path.join(rd, 'network_summary.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['metric', 'H', 'P', 'delta'])
        w.writerows(ROWS)
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        r = client.get('/single/' + name)
    return r.status_code, r.get_data(as_text=True)


#: 렌더된 툴팁 (JS 문자열 리터럴 안이라 개행 = 백슬래시-n 두 글자)
T_BG_NUM = "+ '= 0.2400\\n\\n'"                                     # σ_brug/σ_grain 끝 줄 (정상)
T_BG_DASH = "+ '= —\\n\\n'"                                         # σ_brug/σ_grain 끝 줄 (값 없음)
T_BI_NUM = "'σ_brug / σ_ionic = 0.7200 / 0.2400\\n'"                # σ_brug / σ_ionic (정상)
T_BI_GEN = "'σ_brug / σ_ionic\\nBruggeman 추정 / Network Solver 실측'"  # σ_brug / σ_ionic (일반 문구)
T_BR_NUM = "+ '= 0.7200 mS/cm\\n\\n'"                               # σ_Bruggeman (정상)
T_BR_GEN = "'σ_Bruggeman = σ_grain × φ_SE × f_perc / τ²\\nσ_grain = "  # σ_Bruggeman (일반 문구)


def main():
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import app as A
        A.app.config['TESTING'] = True
        A.app.config['PROPAGATE_EXCEPTIONS'] = False
        c = A.app.test_client()
        print('[N] /single — null 메트릭 (서버 Jinja 툴팁 세 개)')
        s0, h0 = page(c, 'sn_normal', {})
        chk('N1 대조 — 정상 케이스 200 · 세 툴팁 수치 그대로 (σ_brug/σ_grain = 0.2400 · σ_brug / σ_ionic = 0.7200 / 0.2400 · σ_Bruggeman = 0.7200 mS/cm)',
            s0 == 200 and T_BG_NUM in h0 and T_BI_NUM in h0 and T_BR_NUM in h0, (s0, T_BG_NUM in h0, T_BI_NUM in h0, T_BR_NUM in h0))
        s1, h1 = page(c, 'sn_sr_null', {'sigma_ratio': None})
        chk('N2 ★ sigma_ratio null (Codex 반례) → 200 · σ_brug/σ_grain 끝 줄 = — · 나머지 두 툴팁 = 일반 문구 (고치기 전: 500 — single.html %.4f)',
            s1 == 200 and T_BG_DASH in h1 and T_BI_GEN in h1 and T_BR_GEN in h1, (s1, T_BG_DASH in h1, T_BI_GEN in h1, T_BR_GEN in h1))
        s2, h2 = page(c, 'sn_sr_absent', {'sigma_ratio': DROP})
        chk('N3 ★ sigma_ratio 키 없음 → 200 · σ_brug/σ_grain 끝 줄 = — (고치기 전: 지어낸 \'0.0000\')',
            s2 == 200 and T_BG_DASH in h2 and "'= 0.0000\\n\\n'" not in h2, (s2, T_BG_DASH in h2))
        s3, h3 = page(c, 'sn_sr_null_nophi', {'sigma_ratio': None, 'phi_se': DROP})
        chk('N4 ★ sigma_ratio null + phi_se 없음 (Codex 둘째 반례) → 200 · σ_brug / σ_ionic = 일반 문구 (고치기 전: 500 — 툴팁 곱셈)',
            s3 == 200 and T_BI_GEN in h3, (s3, T_BI_GEN in h3))
        nul = {}
        for key in ('phi_se', 'tortuosity_recommended'):
            mut = {key: None}
            if key == 'tortuosity_recommended':
                mut['tortuosity_mean'] = None
            nul[key] = page(c, f'sn_null_{key}', mut)[0]
        chk(f'N5 ★ 같은 툴팁 블록의 다른 값 null (phi_se · tortuosity_recommended + _mean) → 200 (고치기 전: 500) {nul}',
            all(v == 200 for v in nul.values()), nul)
        s6, h6 = page(c, 'sn_rbrug_null', {'R_brug_over_full': None})
        chk('N6 대조 — R_brug_over_full null → 200 (Codex 대조 · 고치기 전도 200)', s6 == 200, s6)
    finally:
        shutil.rmtree(WORK, ignore_errors=True)
    print(f'\ntest_single_null_metrics: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
