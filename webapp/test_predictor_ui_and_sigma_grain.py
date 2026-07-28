#!/usr/bin/env python3
"""σ_grain 단일출처 + 예측기 온도-UI 고지 회귀시험 (2026-07-28 적대검증 담당 C).

  python3 webapp/test_predictor_ui_and_sigma_grain.py     # 종료코드 0 = PASS

왜 이 파일이 있나 — 검증이 찾은 3건을 각각 못 되돌리게 못박는다.

  [C-1] `se_material.py` 는 자기 헤더에서 σ_grain 의 "SINGLE SOURCE OF TRUTH" 라고 주장했지만
        **살아있는 Flask 앱 안에 bare 3.0 이 7곳** 남아 있었다 (σ_brug ×3, SIGMA_GRAIN_MS ×2,
        MD 리포트 ×2).  τ_Lap_eff = √(φ·σ_grain/σ_full) 은 σ_grain 과 σ_full 이 같은 온도일 때만
        옳으므로, 온도를 켠 런에서 25 °C 상수를 쓰면 τ 가 조용히 틀린다.
        → app.py 전 사이트를 `_sigma_grain_mS_cm()` 로 통일했고, 이 시험이 재발을 막는다.
  [C-3] 예측기 UI(233–373 K 슬라이더)는 손대지 않은 채였는데 σ_e 기본 동작이
        "Ea_AM=0.50 eV Arrhenius" → "T-무관" 으로 바뀌었다.  사용자가 알 방법이 없었다.
        → predictor.html 에 무엇이 스케일되고 무엇이 안 되는지 + legacy 선택지를 노출했다.
  [C-4] docs/temp_pressure_capability.md 가 출하 코드와 모순됐다.
        → 구현/미구현 표를 넣었고, 이 시험이 문서-코드 동기화를 확인한다.

★ 최우선 불변식: 기본 경로 bitwise 동일.  legacy 메트릭(온도 provenance 없음)에서
  `_sigma_grain_mS_cm()` 은 **정확히 3.0** 을 돌려주고, 파생량(σ_brug, τ_Lap)이 옛 bare-3.0
  수식과 **비트 단위로** 같은지 직접 비교한다.
"""
import json
import math
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APP_PY = os.path.join(HERE, 'app.py')
PRED_HTML = os.path.join(HERE, 'templates', 'predictor.html')
DOC_MD = os.path.join(ROOT, 'docs', 'temp_pressure_capability.md')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import se_material  # noqa: E402

_FAILS = []


def chk(name, cond, extra=''):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")
    if not cond:
        _FAILS.append(name)
    return bool(cond)


# ══════════════════════════════════════════════════════════════════════════════
# [1] app.py 에 bare σ_grain 리터럴이 되살아나지 않는다
# ══════════════════════════════════════════════════════════════════════════════
def _code_lines(path):
    """주석·문자열(=docstring)을 제거한 '실행되는 코드'만 남긴다.

    단순 라인 grep 은 이 파일 자신의 설명 문장("bare 3.0 이 7곳")까지 잡아 오탐이 난다.
    tokenize 로 COMMENT/STRING 토큰을 버리고 나머지만 재조립한다.
    """
    import io
    import tokenize
    out = {}
    with open(path, 'rb') as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type in (tokenize.COMMENT, tokenize.STRING,
                            tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                            tokenize.DEDENT, tokenize.ENCODING, tokenize.ENDMARKER):
                continue
            out.setdefault(tok.start[0], []).append(tok.string)
    del io
    return [' '.join(v) for v in out.values()]


def test_no_bare_sigma_grain_in_app():
    src = open(APP_PY, encoding='utf-8').read()
    code = _code_lines(APP_PY)
    pats = [
        (r'\b3\.0\s*\*\s*metrics\[', 'σ_brug = 3.0 * metrics[...]'),
        (r"sigma_ratio\s*\*\s*3\.0", 'sigma_ratio * 3.0'),
        (r'SIGMA_GRAIN_MS\s*=\s*3\.0', 'SIGMA_GRAIN_MS = 3.0'),
        (r"=\s*3\.0e-3\b", 'σ_grain S/cm 리터럴'),
    ]
    hits = []
    for pat, label in pats:
        for i, ln in enumerate(code, 1):
            if re.search(pat, ln):
                hits.append(f'{label}: {ln.strip()[:70]}')
    chk('[C-1] app.py 에 bare σ_grain 리터럴 0개 (전부 _sigma_grain_mS_cm 경유)',
        not hits, '; '.join(hits))
    chk('[C-1] app.py 가 _sigma_grain_mS_cm 를 정의하고 쓴다',
        'def _sigma_grain_mS_cm(' in src and src.count('_sigma_grain_mS_cm(') >= 6,
        f"호출 {src.count('_sigma_grain_mS_cm(')}회")
    # predictor_engine 은 이미 se_material 경유 — 같이 지킨다
    pe = open(os.path.join(HERE, 'predictor_engine.py'), encoding='utf-8').read()
    chk('[C-1] predictor_engine 도 se_material 경유 유지',
        're.SIGMA_GRAIN = se_material' or 'SIGMA_GRAIN = se_material.SIGMA_GRAIN_MS_CM_25C' in pe)


# ══════════════════════════════════════════════════════════════════════════════
# [2] _sigma_grain_mS_cm 계약 — 기본 bitwise 3.0, provenance 있으면 따라간다
# ══════════════════════════════════════════════════════════════════════════════
def test_sigma_grain_helper():
    os.environ.setdefault('WEBAPP_RESULTS_FOLDER', tempfile.mkdtemp(prefix='sgtest_res_'))
    sys.path.insert(0, HERE)
    import app                                            # noqa: E402
    f = app._sigma_grain_mS_cm

    chk('[C-1] metrics 없음 → bitwise 3.0', f().hex() == (3.0).hex(), f().hex())
    chk('[C-1] legacy metrics(온도 키 없음) → bitwise 3.0',
        f({'phi_se': 0.35, 'sigma_ratio': 2.0}).hex() == (3.0).hex())
    chk('[C-1] dict 아닌 입력에도 안전', f(None).hex() == (3.0).hex() and f(5).hex() == (3.0).hex())

    prov_off = se_material.provenance()
    chk('[C-1] T 미적용 provenance(factor 1.0) → bitwise 3.0',
        f({'temperature_provenance': prov_off}).hex() == (3.0).hex())
    chk('[C-1] sigma_grain_S_cm=3.0e-3 폴백도 bitwise 3.0',
        f({'sigma_grain_S_cm': se_material.SIGMA_GRAIN_S_CM_25C}).hex() == (3.0).hex())

    for t_c, want in ((30.0, 1.28), (45.0, 2.56), (60.0, 4.79)):
        got = f({'temperature_provenance': se_material.provenance(t_c)})
        chk(f'[C-1] T={t_c:.0f} °C provenance → σ_grain = 3.0 × {want}',
            abs(got / 3.0 - se_material.arrhenius_sigma_factor(t_c)) < 1e-15
            and abs(round(got / 3.0, 2) - want) < 5e-3, f'{got:.4f} mS/cm')
    # ★ 2026-07-28 정정 (재검증 HIGH, e-follow-on): 예전 이 테스트는 Stage-E 키도 인수분해
    #   대상으로 "인식" 하는 것을 PASS 로 못박아서 **버그를 고정하고 있었다**.
    #   run_network_full_corrections.py --temp-c 는 Stage-E σ 만 스케일하고 베이스라인
    #   sigma_full_mScm 은 25 °C 로 남긴다 (그 스크립트 selftest 가 명시 검증).  이 헬퍼의
    #   소비자는 전부 σ_grain 을 그 **베이스라인**과 나누므로, Stage-E 배수를 따르면 분자만
    #   ×4.79 되어 σ_brug/σ_ionic·τ_Lap 이 조용히 틀린다 → 25 °C 상수를 유지해야 짝이 맞는다.
    chk('[C-1] Stage-E-only provenance → 25 °C 베이스라인과 짝맞춰 bitwise 3.0 (배수 적용 안 함)',
        f({'stage_e_temperature_provenance': se_material.provenance(60.0)}).hex() == (3.0).hex())
    _v, _note = app._sigma_grain_context(
        {'stage_e_temperature_provenance': se_material.provenance(60.0)})
    chk('[C-1] Stage-E-only 런은 혼합-온도 경고를 노출한다',
        _v.hex() == (3.0).hex() and isinstance(_note, str) and '혼합 온도' in _note
        and '60' in _note, repr(_note))
    chk('[C-1] Stage-E factor 1.0(=T 미적용)은 경고 없음',
        app._sigma_grain_context(
            {'stage_e_temperature_provenance': se_material.provenance()})[1] is None)
    chk('[C-1] 짝이 맞는 temperature_provenance 는 그대로 배수 적용 + 경고 없음',
        abs(app._sigma_grain_context(
            {'temperature_provenance': se_material.provenance(60.0)})[0] / 3.0
            - se_material.arrhenius_sigma_factor(60.0)) < 1e-15
        and app._sigma_grain_context(
            {'temperature_provenance': se_material.provenance(60.0)})[1] is None)
    # 둘 다 있으면 짝이 맞는 쪽(temperature_provenance)이 이긴다
    chk('[C-1] 두 키 공존 시 σ_full 과 짝이 맞는 temperature_provenance 우선',
        abs(f({'temperature_provenance': se_material.provenance(45.0),
               'stage_e_temperature_provenance': se_material.provenance(60.0)}) / 3.0
            - se_material.arrhenius_sigma_factor(45.0)) < 1e-15)
    # 망가진/거짓 provenance 는 무시하고 기본값 (조용한 오답 방지)
    for bad in ({'sigma_ion_T_factor': None}, {'sigma_ion_T_factor': 0}, {'sigma_ion_T_factor': True}):
        chk(f'[C-1] 이상한 provenance({bad}) → 기본 3.0 로 폴백',
            f({'temperature_provenance': bad}).hex() == (3.0).hex())
    return app


# ══════════════════════════════════════════════════════════════════════════════
# [3] ★ 파생량 bitwise A/B — 옛 bare-3.0 수식 vs 새 헬퍼 (legacy 메트릭)
# ══════════════════════════════════════════════════════════════════════════════
def test_derived_quantities_bitwise(app):
    f = app._sigma_grain_mS_cm
    cases = [
        {'phi_se': 0.351, 'sigma_ratio': 2.7183, 'sigma_full_mScm': 0.1234,
         'sigma_bulk_net_mScm': 0.9871},
        {'phi_se': 0.4823, 'sigma_ratio': 0.0177, 'sigma_full_mScm': 1.4142,
         'sigma_bulk_net_mScm': 2.7181},
        {'phi_se': 0.2001, 'sigma_ratio': 11.9, 'sigma_full_mScm': 0.00317,
         'sigma_bulk_net_mScm': 0.05},
    ]
    ok_brug = ok_tau = True
    for m in cases:
        old_brug = 3.0 * m['sigma_ratio']
        new_brug = f(m) * m['sigma_ratio']
        ok_brug &= (old_brug.hex() == new_brug.hex())
        old_tau = math.sqrt(m['phi_se'] * 3.0 / m['sigma_full_mScm'])
        new_tau = math.sqrt(m['phi_se'] * f(m) / m['sigma_full_mScm'])
        old_geo = math.sqrt(m['phi_se'] * 3.0 / m['sigma_bulk_net_mScm'])
        new_geo = math.sqrt(m['phi_se'] * f(m) / m['sigma_bulk_net_mScm'])
        ok_tau &= (old_tau.hex() == new_tau.hex() and old_geo.hex() == new_geo.hex())
    chk('[C-1] σ_Bruggeman = σ_grain×ratio 가 옛 3.0 수식과 bitwise 동일', ok_brug)
    chk('[C-1] τ_Lap_eff / τ_Lap_geom 이 옛 3.0 수식과 bitwise 동일', ok_tau)
    chk('[C-1] MD 리포트 포맷 f"{sg:.1f}" 이 옛 "3.0" 문자열과 동일',
        f'{f({}):.1f}' == '3.0')
    # 온도가 켜지면 τ 가 실제로 움직인다 (= 이 수정이 하는 일)
    m = dict(cases[0], temperature_provenance=se_material.provenance(60.0))
    tau_25 = math.sqrt(cases[0]['phi_se'] * 3.0 / cases[0]['sigma_full_mScm'])
    tau_60 = math.sqrt(m['phi_se'] * f(m) / m['sigma_full_mScm'])
    chk('[C-1] T 런에서 τ_Lap 이 √배수만큼 정합 이동 (25 °C 고정이면 이만큼 틀렸다)',
        abs(tau_60 / tau_25 - math.sqrt(se_material.arrhenius_sigma_factor(60.0))) < 1e-12,
        f'τ {tau_25:.3f} → {tau_60:.3f} (×{tau_60/tau_25:.3f})')

    # ── 실제 표 생성 함수를 통째로 돌려서 legacy 산출물이 옛 하드코딩 결과와 같은지 확인 ──
    # transform_network_summary_4col 이 7곳 중 4곳(σ_brug ×2 · τ_Lap 블록 ×2)을 갖고 있었다.
    metrics = {
        'sigma_full_mScm': 0.1234, 'sigma_full_mScm_physics': 0.1501,
        'sigma_bulk_net_mScm': 0.9871, 'sigma_ratio': 2.7183,
        'sigma_bruggeman_mScm': 0.8161, 'R_brug_over_full': 6.61,
        'R_brug_over_full_physics': 5.44, 'bulk_resistance_fraction': 0.37,
        'phi_se': 0.351, 'tortuosity_mean': 1.62, 'percolation_pct': 98.0,
    }
    tbl = {'network_summary': {'data': [['σ_eff/σ_bulk', 0.184341],
                                        ['── 응력 ──', '', '', ''],
                                        ['Von Mises mean(MPa)', 12.3]]}}
    app.transform_network_summary_4col(tbl, dict(metrics), {})
    rows = {str(r[0]): r for r in tbl['network_summary']['data'] if isinstance(r, list) and r}
    want_brug = 3.0 * metrics['sigma_ratio'] / metrics['sigma_full_mScm']   # 옛 하드코딩 수식
    got = rows.get('σ_brug / σ_ionic')
    chk('[C-1] 표의 σ_brug/σ_ionic 이 옛 3.0 수식 결과와 동일',
        got is not None and got[1] == f'{want_brug:.1f}×', f'{got}')
    want_tau = math.sqrt(metrics['phi_se'] * 3.0 / metrics['sigma_full_mScm'])
    tau_row = next((r for k, r in rows.items() if k.startswith('τ_Lap_eff')), None)
    chk('[C-1] 표의 τ_Lap_eff 가 옛 3.0 수식 결과와 동일',
        tau_row is not None and abs(float(tau_row[1]) - round(want_tau, 2)) < 1e-9,
        f'{tau_row} vs {round(want_tau, 2)}')


# ══════════════════════════════════════════════════════════════════════════════
# [4] predictor.html — 온도 축이 무엇을 하고 안 하는지 화면에 적혀 있다
# ══════════════════════════════════════════════════════════════════════════════
def test_predictor_ui():
    html = open(PRED_HTML, encoding='utf-8').read()
    chk('[C-3] 슬라이더 옆에 스코프 고지 블록이 있다', 'id="temp-scope-note"' in html)
    for needle, why in (
            ('sigma_ionic', 'σ_ion 이 스케일된다는 서술'),
            ('Kraft 2017', '규약 출처'),
            ('0.41 eV', '기본 Eₐ'),
            ('스케일 안 됨', '무엇이 안 되는지'),
            ('Find Optimal Design', '스윕이 온도를 무시한다는 고지'),
            ('단일값 보고 금지', 'Eₐ 밴드 규약'),
            ('&sect;F1', '앵커 없음 표기')):
        chk(f'[C-3] 고지에 {why} 포함', needle in html, needle)
    chk('[C-3] legacy σ_e Arrhenius 선택지가 UI 에 노출된다',
        'id="sigma_e_t_model"' in html and 'legacy_arrhenius' in html)
    chk('[C-3] σ_e 기본 선택지가 T-무관(none) — 첫 option 이 none',
        re.search(r'id="sigma_e_t_model".*?<option value="none"', html, re.S) is not None)
    chk('[C-3] Eₐ 밴드 3값이 셀렉터에 있다',
        all(f'value="{v}"' in html for v in ('0.29', '0.41', '0.46'))
        and 'id="ea_ion_ev"' in html)
    chk('[C-3] Eₐ 기본 선택지는 빈 값 = 엔진 기본(0.41) → 요청이 기본과 동일',
        re.search(r'id="ea_ion_ev"[^>]*>\s*<option value=""', html) is not None)
    chk('[C-3] getParams 가 두 키를 실어 보낸다',
        'sigma_e_t_model: document.getElementById' in html
        and 'ea_ion_ev: document.getElementById' in html)
    chk('[C-3] 결과에 온도 provenance 박스를 렌더한다',
        't-prov-box' in html and 'temperature_provenance' in html
        and 'sigma_e_T_model' in html)
    # ★ "조용한 no-op 팔" 은 작동시키거나 막아야 한다.  온도 스윕은 엔진에 레인지도 없고
    #   predict() 에 값도 안 넘어가 1점 축퇴 + 298 K 고정 → 명시적으로 차단한다.
    chk('[C-3] 온도 스윕(no-op 팔)을 명시적으로 차단한다',
        "sweepKeys.includes('temperature')" in html and '스윕할 수 없습니다' in html)
    chk('[C-3] 스윕 결과 화면에 "298 K 고정" 배너를 붙인다',
        'opt-temp-note' in html and '298 K (25 °C) 고정' in html)

    # JS 문법 검사 (node 있으면)
    node = subprocess.run(['bash', '-lc', 'command -v node'], capture_output=True, text=True)
    if node.returncode != 0:
        print('  SKIP  [C-3] JS 문법검사 (node 없음)')
        return
    m = re.findall(r'<script>(.*?)</script>', html, re.S)
    chk('[C-3] predictor.html 에 script 블록이 있다', bool(m))
    js = '\n'.join(m)
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as fh:
        fh.write(js)
        p = fh.name
    try:
        cp = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        chk('[C-3] 인라인 JS 가 문법적으로 파싱된다 (node --check)',
            cp.returncode == 0, (cp.stderr or '')[-200:])
    finally:
        os.unlink(p)


# ══════════════════════════════════════════════════════════════════════════════
# [5] /predictor 렌더 + /predictor/predict 라우트 기본 전달
# ══════════════════════════════════════════════════════════════════════════════
def test_routes(app):
    c = app.app.test_client()
    r = c.get('/predictor')
    chk('[C-3] /predictor 가 200 이고 고지가 실제 렌더된다',
        r.status_code == 200 and b'temp-scope-note' in r.data
        and b'sigma_e_t_model' in r.data, f'status {r.status_code}')
    src = open(APP_PY, encoding='utf-8').read()
    chk('[C-3] predict 라우트 기본이 sigma_e_t_model=none (σ_e T-무관)',
        "data.get('sigma_e_t_model', 'none')" in src)
    chk('[C-3] ea_ion_ev 미지정/빈값 → None (엔진 기본 0.41)',
        "data.get('ea_ion_ev') not in (None, '')" in src)


# ══════════════════════════════════════════════════════════════════════════════
# [6] 문서가 출하 코드와 일치한다
# ══════════════════════════════════════════════════════════════════════════════
def test_doc_sync():
    doc = open(DOC_MD, encoding='utf-8').read()
    chk('[C-4] 구현/미구현 상태표가 있다', '## 9.' in doc and '구현 상태' in doc)
    chk('[C-4] σ_e 기본이 T-무관으로 바뀐 사실이 적혀 있다',
        'legacy_arrhenius' in doc and 'T-무관' in doc)
    chk('[C-4] Stage-E --temp-c 배선이 적혀 있다',
        'run_network_full_corrections.py --temp-c' in doc)
    chk('[C-4] σ_grain 잔존 하드코딩 인벤토리가 적혀 있다',
        'physics_surface_contact_fit.py' in doc and 'triage_cases.py' in doc)
    chk('[C-4] 이번 검증의 잔존 한계(다른 담당분 포함)가 적혀 있다',
        '별도 수정 중' in doc)
    # 옛 서술이 "현재 동작"으로 남아 있으면 안 된다 (역사 서술은 허용 → 같은 줄에 과거 표지 필요)
    bad = []
    for i, ln in enumerate(doc.splitlines(), 1):
        if 'Ea_AM' in ln and '0.50' in ln:
            if not any(k in ln for k in ('이전', '옛', 'legacy', '제거', '2026-07-28', '過去', '역사')):
                bad.append(f'{i}: {ln.strip()[:80]}')
    chk('[C-4] "predictor 가 σ_e 에 Ea_AM=0.50 을 곱한다"가 현재형으로 남아있지 않음',
        not bad, ' | '.join(bad))


# ══════════════════════════════════════════════════════════════════════════════
# [7] ★ 템플릿(서버렌더) 경로에 bare σ_grain 이 남아있지 않은가
#     — 2026-07-28 재검증 HIGH-e: app.py 는 깨끗한데 single.html 이 Jinja 로
#       `metrics.sigma_ratio * 3.0` 을 직접 계산하고 있었다.  app.py 만 보는 [1] 검사로는
#       절대 안 잡힌다 → 템플릿 소스 자체를 본다.
# ══════════════════════════════════════════════════════════════════════════════
def test_no_bare_sigma_grain_in_templates(app):
    import re
    tdir = os.path.join(HERE, 'templates')
    # 계산 슬롯: 산술식 안의 3.0, 또는 "= 3.0 ×" 처럼 값을 인쇄하는 자리
    calc_pat = re.compile(r'(sigma_ratio\s*\*\s*3\.0|\*\s*3\.0\s*/|=\s*3\.0\s*×)')
    bad = []
    for fn in sorted(os.listdir(tdir)):
        if not fn.endswith('.html'):
            continue
        for i, ln in enumerate(open(os.path.join(tdir, fn), encoding='utf-8'), 1):
            if calc_pat.search(ln):
                bad.append(f'{fn}:{i}')
    chk('[C-1t] 템플릿에 σ_grain 산술 하드코딩 0개', not bad, ' | '.join(bad))

    # single.html 은 헬퍼 전역을 실제로 쓴다
    src = open(os.path.join(tdir, 'single.html'), encoding='utf-8').read()
    chk('[C-1t] single.html 이 sigma_grain() 전역을 쓴다',
        src.count('sigma_grain(metrics)') >= 6, str(src.count('sigma_grain(metrics)')))

    # 전역이 컨텍스트 프로세서로 주입된다 = 어떤 route 로 렌더돼도 따라온다
    with app.app.app_context():
        ctx = {}
        for f in app.app.template_context_processors[None]:
            ctx.update(f())
        chk('[C-1t] sigma_grain/sigma_grain_note 가 전역 주입됨',
            callable(ctx.get('sigma_grain')) and callable(ctx.get('sigma_grain_note')))
        # 렌더 결과: legacy 런은 옛 "3.0" 문자열 그대로, T 런은 스케일된 값
        t = app.app.jinja_env.from_string(
            '{{ "%.1f"|format(sigma_grain(metrics)) }}')
        leg = t.render(metrics={'phi_se': 0.35}, **ctx)
        chk('[C-1t] legacy 렌더 문자열이 옛 "3.0" 과 동일', leg == '3.0', leg)
        hot = t.render(metrics={'temperature_provenance': se_material.provenance(60.0)}, **ctx)
        chk('[C-1t] 짝맞는 T 런은 스케일된 값을 렌더', hot == '14.4', hot)
        mix = t.render(
            metrics={'stage_e_temperature_provenance': se_material.provenance(60.0)}, **ctx)
        chk('[C-1t] Stage-E-only 런은 25 °C 값을 렌더(베이스라인과 짝)', mix == '3.0', mix)
    # 템플릿 전체가 파싱된다 (Jinja 문법 깨짐 방지)
    with app.app.app_context():
        for tpl in ('single.html', 'group.html'):
            app.app.jinja_env.get_template(tpl)
        chk('[C-1t] single/group 템플릿 파싱 OK', True)


def main():
    print('σ_grain 단일출처 + 예측기 온도-UI 회귀시험')
    test_no_bare_sigma_grain_in_app()
    app = test_sigma_grain_helper()
    test_no_bare_sigma_grain_in_templates(app)
    test_derived_quantities_bitwise(app)
    test_predictor_ui()
    test_routes(app)
    test_doc_sync()
    print(('ALL PASS' if not _FAILS else f'FAIL ({len(_FAILS)}): ' + '; '.join(_FAILS)))
    return 0 if not _FAILS else 1


if __name__ == '__main__':
    sys.exit(main())
