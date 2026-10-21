#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S1 웹앱 표지 — `ptfe_stamp = face_alpha` (설계 §3-6 · J20-l · 2026-10-20 · 시험 먼저).

⚠ 설계 §3-6 의 표지 자리 `webapp/mpm_lab_register.py` `build_meta` 는 **LHS 봉인 32 파일**이라 고치지 않는다
  (코디네이터 10-20 — LHS214 재발사 지문).  그래서:
  · 표시 문자열 = producer 상수 하나 (`ptfe_face_alpha.LABEL`) → payload 매니페스트 `ca_ext.ptfe_face.evidence.label`
  · 화면 = 봉인 밖 템플릿 `webapp/templates/mpm_lab.html` (Jinja 서버 행 · JS 행 둘 다) 이 그 문자열을 **읽어** 띄운다
  · `build_meta` 는 이미 `ptfe_stamp` 값을 그대로 옮기므로 (`PTFE <값>`) 목록 규약 칩은 고치지 않아도 `PTFE face_alpha` 가 된다

  W1  표지 문자열 — 한정어 (α · Ø0.248 rope = 규약 선택 · 불투과 가정 · 전자/이온)
  W2  템플릿 두 행 (Jinja · JS) 이 매니페스트의 표지를 읽는다 · 문자열 사본을 두지 않는다
  W3  face_alpha 인데 관측 PTFE 셀 > 0 = 불일치 경고 (두 행)
  W4  봉인 `build_meta` (읽기만) 가 face_alpha 매니페스트에서 `PTFE face_alpha` 칩을 낸다

  ★ 2026-10-20 (Rint ② B6 · 설계 §4-6 · §5-6 · 시험 먼저) — S2 탄소 접합 · S3 SDCP 수정자 표지 (같은 두 행 · 매니페스트 값을 읽기만):
  W8  두 행이 `ca_ext.cjunc` · `ca_ext.sdcp_mod` 를 읽는다 · 표지 문자열 사본 없음 (producer 상수 `ca_ext_cjunc.LABEL_*` 하나)
  W9  Jinja 렌더 — 접합 = 표지 · R_j · P0/P1 · 세대 접두 · 수정자 = 표지 · c · 판별 표지 False = no-op 알림 · 요청 ↔ 블록 불일치 ·
      블록 ↔ 세대 id 불일치 경고 · 옛 meta = 아무것도 없음
  W10 JS 행 (node 실행) — 같은 경우들
  W11 봉인 `build_meta` (읽기만) 가 매니페스트를 그대로 싣는다 (템플릿이 읽는 자리) — 규약 칩의 접합 표시는 봉인이라 미룸

  ★ 2026-10-21 (D · 등록 R 3판 §5-0 · §5-6 SV 행 · 사전 리뷰 PRE-impl-08 · 시험 먼저) — 같은 두 행 (매니페스트 · step3 값을 읽기만):
  W12 해 상태 — `step3.conv_cert` · `step3.ion_conv_cert` 의 상태 (`step3_conv_cert.STATUS_*` 와 같은 낱말) — VALID_ZERO_TOPOLOGY =
      "σ = 0 · 두 판을 잇는 성분 없음 (정상 결과)" · ELECTRODE_SHORT = ★ 4판 (10-21 · 1저자 Q1 · 등록 R 4판 §5-0) "게시 안 됨 · 사슬 판정
      NOT_COMPUTED (사유 ELECTRODE_SHORT · J11 단락)" (3판 = "σ = +∞" 철회) · NOT_CERTIFIABLE = 경고 · POSITIVE_SOLVED · 증서 없음 = 표지 없음
      (Jinja · JS)
  W13 SV 반사실 — 증거 `solve.sv_counterfactual` 의 비 (유한 · +∞ = ratio_limit 'inf') · 상태 · producer 표지 (SV_DEPENDENT) ·
      문턱 = 사슬 계획 (화면은 비만 · 판정은 사슬) · 기록 없음 = 줄 없음
  W14 접합 한정어 (PRE-impl-08) — 증거 `qualifiers` (producer `carbon_junction.CJUNC_QUALIFIERS`) 가 화면에 그대로 · 설계 v1 §4-6 의
      세 표지 (분산판 · 같은 셀 재방문 · SV 진단 = 반사실 대조 따로) 를 실제 렌더에서 본다 · 템플릿에 한정어 사본 없음

  python3 webapp/test_ca_ext_labels.py
"""
import os
import shutil
import sys

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
    return cond


def _cj_meta(lab_cj, lab_sd, *, c=None, disc=None, pid='p3ca-0123456789abcdef', block=True, req=None):
    """템플릿이 읽는 칸만 실은 매니페스트 (S2 · S3 블록 꼴 = ca_ext_cjunc 의 기록 함수가 내는 키)."""
    m = {'ptfe_stamp': 'off', 'ptfe_cells_observed': 0, 'physics_protocol_id': pid,
         'ca_ext_requested': (req if req is not None else (['cjunc'] + (['sdcp_mod'] if c is not None else [])))}
    if block:
        m['ca_ext'] = {'schema': 'ca-ext-v1',
                       'cjunc': {'protocol': {'R_j_ohm': 1000000.0, 'ptfe_jlaw': 'P0'}, 'evidence': {'label': lab_cj}}}
        if c is not None:
            m['ca_ext']['sdcp_mod'] = {'protocol': {'c': c}, 'evidence': {'label': lab_sd, 's3_discriminating': disc}}
    return {'id': 'x', 'has_additives': True, 'recipe': 'VGCF 3', 'convention_label': 'PTFE off',
            'mpm_metrics': {'step3': {'manifest': m}}}


#: 렌더 경우 — (이름, meta, 있어야 할 조각, 없어야 할 조각) · 조각 '{CJ}' · '{SD}' = 표지 문자열 (렌더러마다 이스케이프)
_B6_CASES = (
    ('접합', dict(), ('{CJ}', 'R_j', '1000000', 'Ω', 'P0', 'p3ca'), ('{SD}', '블록 없음', '기록 불일치')),
    ('접합 + 수정자 c 1 (판별)', dict(c=1.0, disc=True), ('{CJ}', '{SD}', 'c = 1'), ('구성상 no-op', '블록 없음')),
    ('접합 + 수정자 (SDCP 0 침대)', dict(c=0.0, disc=False), ('{CJ}', '{SD}', 'c = 0', '구성상 no-op'), ('블록 없음',)),
    ('요청 · 블록 없음', dict(block=False), ('블록 없음', 'unknown:ca_ext'), ('{CJ}', '🔗')),
    ('블록인데 id 가 p2', dict(pid='p2-0123456789abcdef'), ('{CJ}', '기록 불일치'), ()),
)


def _b6_labels(tpl, jinja, js, jinja2, REG):
    """② B6 — S2 탄소 접합 · S3 SDCP 수정자 표지 (W8–W11)."""
    try:
        import ca_ext_cjunc as CW
    except Exception as e:                                  # noqa: BLE001 — 구현 전 (모듈 없음) 도 기록
        CW = None
        print(f'  ⚠ ca_ext_cjunc 를 못 불러온다 ({type(e).__name__}: {e})')
    lab_cj = getattr(CW, 'LABEL_CJUNC', '') if CW else ''
    lab_sd = getattr(CW, 'LABEL_SDCP', '') if CW else ''
    chk('W8a Jinja 행이 매니페스트 ca_ext.cjunc · ca_ext.sdcp_mod 를 읽는다',
        len(jinja) == 1 and all(t in jinja[0] for t in ('cjunc', 'sdcp_mod', 'label')), len(jinja))
    chk('W8b JS 행이 매니페스트 ca_ext.cjunc · ca_ext.sdcp_mod 를 읽는다',
        len(js) == 1 and all(t in js[0] for t in ('cjunc', 'sdcp_mod', 'label')), len(js))
    chk('W8c S2 · S3 표지 문자열 사본을 템플릿에 두지 않는다 (producer 상수 하나)',
        bool(lab_cj) and bool(lab_sd) and lab_cj not in tpl and lab_sd not in tpl)
    metas = [(nm, _cj_meta(lab_cj, lab_sd, **kw), want, avoid) for nm, kw, want, avoid in _B6_CASES]
    old_meta = {'id': 'o', 'has_additives': True, 'recipe': 'VGCF 3', 'mpm_metrics': {}}

    def _check(lbl, outs, esc):
        for (nm, _m, want, avoid), out in zip(metas, outs):
            sub = lambda t: t.replace('{CJ}', esc(lab_cj) if lab_cj else '\0').replace('{SD}', esc(lab_sd) if lab_sd else '\0')   # noqa: E731
            miss = [t for t in want if sub(t) not in (out or '')]
            bad = [t for t in avoid if sub(t) in (out or '')]
            chk(f'{lbl} [{nm}] — 있어야 할 조각 {len(want)} · 없어야 할 조각 {len(avoid)}', out is not None and not miss and not bad,
                (miss, bad, (out or '')[-260:]))
    if jinja2 is not None and len(jinja) == 1:
        from markupsafe import escape as _escape
        env = jinja2.Environment(autoescape=True)
        row = env.from_string(jinja[0])
        outs = [row.render(it=m) for _nm, m, _w, _a in metas]
        _check('W9 Jinja', outs, lambda s: str(_escape(s)))
        o_old = row.render(it=old_meta)
        chk('W9 Jinja [옛 meta (매니페스트 없음)] — 접합 · 수정자 표지 · 경고 없음',
            '🔗' not in o_old and '🧴' not in o_old and '블록 없음' not in o_old, o_old[-160:])
    else:
        print('  SKIP  W9 (jinja2 없음)')
    import shutil as _sh
    if _sh.which('node') is None:
        print('  SKIP  W10 (node 없음)')
    else:
        import json as _json
        from test_closed_param_labels import js_fn, run_node
        script = ('const made = [];\n'
                  'const document = {getElementById: (id) => ({style: {}, textContent: "", insertBefore: () => {}, '
                  'firstChild: null, querySelectorAll: () => []}), createElement: (t) => { const o = {dataset: {}, style: {}}; '
                  'made.push(o); return o; }};\n' + js_fn(tpl, 'labAddRow') + '\n'
                  f'const cases = {_json.dumps([m for _nm, m, _w, _a in metas] + [old_meta], ensure_ascii=False)};\n'
                  'const out = cases.map(c => { labAddRow(c); return made[made.length - 1].innerHTML; });\n'
                  'console.log(JSON.stringify(out));\n')
        try:
            outs = run_node(script)
            _check('W10 JS', outs[:-1], lambda s: s)
            chk('W10 JS [옛 meta] — 접합 · 수정자 표지 · 경고 없음',
                '🔗' not in outs[-1] and '🧴' not in outs[-1] and '블록 없음' not in outs[-1], outs[-1][-160:])
        except Exception as e:                              # noqa: BLE001
            chk('W10 JS 행 (node 실행)', False, f'{type(e).__name__}: {e}')
    data = {'mpm_metrics': {'step3': {'manifest': dict(_cj_meta(lab_cj, lab_sd, c=1.0, disc=True)['mpm_metrics']['step3']['manifest'],
                                                       ptfe_stamp_requested='off', vox_um=0.15)}}}
    meta = REG.build_meta(data, 'cj_case', uploaded_at='2026-10-20 00:00', size_mb=0.1)
    _mm = ((meta.get('mpm_metrics') or {}).get('step3') or {}).get('manifest') or {}
    chk('W11 봉인 build_meta (읽기만) 가 매니페스트를 그대로 싣는다 — 템플릿이 읽는 ca_ext.cjunc · sdcp_mod 자리가 meta 에 있다',
        ((_mm.get('ca_ext') or {}).get('cjunc') or {}).get('evidence', {}).get('label') == lab_cj
        and ((_mm.get('ca_ext') or {}).get('sdcp_mod') or {}).get('protocol', {}).get('c') == 1.0, sorted(_mm))


def _d_meta(*, cert=None, ion_cert=None, sv=None, quals=None, lab_cj='L'):
    """★ D — 해 상태 · SV 반사실 · 접합 한정어 꼴 (템플릿이 읽는 칸만 · 키 = payload 가 쓰는 자리)."""
    m = {'ptfe_stamp': 'face_alpha', 'ptfe_cells_observed': 0, 'physics_protocol_id': 'p3ca-0123456789abcdef',
         'ca_ext_requested': ['cjunc'],
         'ca_ext': {'schema': 'ca-ext-v1', 'cjunc': {'protocol': {'R_j_ohm': 1000000.0, 'ptfe_jlaw': 'P0'},
                                                       'evidence': {'label': lab_cj, 'solve': {}}}}}
    if quals is not None:
        m['ca_ext']['cjunc']['evidence']['qualifiers'] = list(quals)
    if sv is not None:
        m['ca_ext']['cjunc']['evidence']['solve']['sv_counterfactual'] = sv
    st = {'manifest': m}
    if cert is not None:
        st['conv_cert'] = {'status': cert}
    if ion_cert is not None:
        st['ion_conv_cert'] = {'status': ion_cert}
    return {'id': 'd', 'has_additives': True, 'recipe': 'VGCF 3', 'convention_label': 'PTFE face_alpha', 'mpm_metrics': {'step3': st}}


def _d_states(tpl, jinja, js, jinja2):
    """★ D — W12 해 상태 · W13 SV 반사실 · W14 접합 한정어 (Jinja · JS 두 행)."""
    try:
        import step3_conv_cert as CC
        ZERO, SHORT, NOTC, POS = CC.STATUS_ZERO, CC.STATUS_SHORT, CC.STATUS_NOT_CERTIFIABLE, CC.STATUS_POSITIVE
    except Exception as e:                                  # noqa: BLE001
        ZERO, SHORT, NOTC, POS = 'VALID_ZERO_TOPOLOGY', 'ELECTRODE_SHORT', 'NOT_CERTIFIABLE', 'POSITIVE_SOLVED'
        print(f'  ⚠ step3_conv_cert 를 못 불러온다 ({type(e).__name__}: {e})')
    try:
        import carbon_junction as CJ
        quals = list(CJ.CJUNC_QUALIFIERS)
    except Exception as e:                                  # noqa: BLE001
        quals = []
        print(f'  ⚠ carbon_junction 을 못 불러온다 ({type(e).__name__}: {e})')
    chk('W12a 두 행이 증서 상태 낱말을 producer 상수와 같은 철자로 쓴다 (VALID_ZERO_TOPOLOGY · ELECTRODE_SHORT · NOT_CERTIFIABLE)',
        len(jinja) == 1 and len(js) == 1 and all(s in ln for s in (ZERO, SHORT, NOTC) for ln in (jinja[0], js[0]))
        and all(k in ln for k in ('conv_cert', 'ion_conv_cert') for ln in (jinja[0], js[0])))
    chk('W14a 템플릿에 접합 한정어 사본이 없다 (producer 상수 CJUNC_QUALIFIERS 하나 · 매니페스트에서 읽는다) · 두 행이 qualifiers 를 읽는다',
        bool(quals) and not [q for q in quals if q[:24] in tpl] and len(jinja) == 1 and len(js) == 1
        and all('qualifiers' in ln for ln in (jinja[0], js[0])), [q[:24] for q in quals if q[:24] in tpl])
    _three = ('분산판', '재방문', '반사실')
    chk('W14b producer 한정어가 설계 v1 §4-6 의 세 표지를 담는다 (긴 접촉 = 분산판 · 같은 셀 재방문 = 가지 따로 · SV 진단 = 반사실 대조 따로)',
        all(any(t in q for q in quals) for t in _three), [t for t in _three if not any(t in q for q in quals)])
    sv_fin = {'kind': 'counterfactual_cut_sv_faces', 'status': 'computed', 'sv_counterfactual_ratio': 1.25, 'ratio_limit': None,
              'flag': None}
    sv_inf = {'kind': 'counterfactual_cut_sv_faces', 'status': 'no_through_without_sv', 'sv_counterfactual_ratio': None,
              'ratio_limit': 'inf', 'flag': None}
    sv_dep = dict(sv_fin, sv_counterfactual_ratio=3.5, flag='SV_DEPENDENT')
    sv_unc = {'kind': 'counterfactual_cut_sv_faces', 'status': 'unconverged', 'sv_counterfactual_ratio': None, 'ratio_limit': None,
              'flag': None}
    cases = (
        ('σ_e 영값 위상', _d_meta(cert=ZERO), (ZERO, 'σ_e', 'σ = 0', '두 판을 잇는 성분'), (SHORT, NOTC, 'SV 반사실')),
        #  ★ 4판 (10-21 · 1저자 Q1 · 등록 R 4판 §5-0 · R4-Q5) — 단락 = 생산자 미게시 · 사슬 판정 = NOT_COMPUTED (사유 ELECTRODE_SHORT) · σ +∞ 아님
        ('σ_e 단락', _d_meta(cert=SHORT), (SHORT, 'σ_e', '게시 안 됨', 'NOT_COMPUTED', 'J11'), (ZERO, NOTC, 'σ = +∞', '+∞')),
        ('σ_e 증서 못 정함', _d_meta(cert=NOTC), (NOTC, 'σ_e'), (ZERO, SHORT)),
        ('σ_ion 영값 위상', _d_meta(cert=POS, ion_cert=ZERO), (ZERO, 'σ_ion', 'σ = 0'), (SHORT, NOTC)),
        ('양의 해', _d_meta(cert=POS), (), (ZERO, SHORT, NOTC, 'σ = +∞')),
        ('증서 없음', _d_meta(), (), (ZERO, SHORT, NOTC)),
        ('SV 비 유한', _d_meta(sv=sv_fin), ('SV 반사실', '1.25', 'computed', '사슬 계획'), ('SV_DEPENDENT', '∞')),
        ('SV 비 +∞', _d_meta(sv=sv_inf), ('SV 반사실', '∞', 'no_through_without_sv'), ('SV_DEPENDENT',)),
        ('SV producer 표지', _d_meta(sv=sv_dep), ('SV 반사실', '3.5', 'SV_DEPENDENT'), ()),
        ('SV 비 없는 상태', _d_meta(sv=sv_unc), ('SV 반사실', 'unconverged', '—'), ('SV_DEPENDENT', '∞')),
        ('SV 기록 없음', _d_meta(), (), ('SV 반사실',)),
        ('접합 한정어', _d_meta(quals=quals), ('{Q}',) + _three + ('접합 한정어',), ()),
        ('한정어 없는 옛 기록', _d_meta(), (), ('접합 한정어',) + _three),    # 세 표지는 템플릿 글이 아니라 producer 한정어에서만
    )

    def _check(lbl, outs, esc):
        for (nm, _m, want, avoid), out in zip(cases, outs):
            miss = []
            for t in want:
                if t == '{Q}':
                    miss += [q[:30] for q in quals if esc(q) not in (out or '')] or ([] if quals else ['(한정어 없음)'])
                elif t not in (out or ''):
                    miss.append(t)
            bad = [t for t in avoid if t in (out or '')]
            chk(f'{lbl} [{nm}] — 있어야 할 조각 {len(want)} · 없어야 할 조각 {len(avoid)}', out is not None and not miss and not bad,
                (miss, bad, (out or '')[-300:]))
    from markupsafe import escape as _escape
    _esc = lambda s: str(_escape(s))                        # noqa: E731 — 두 렌더러 같은 이스케이프 (JS 행은 같은 꼴 도우미)
    if jinja2 is not None and len(jinja) == 1:
        env = jinja2.Environment(autoescape=True)
        row = env.from_string(jinja[0])
        _check('W12-14 Jinja', [row.render(it=m) for _nm, m, _w, _a in cases], _esc)
    else:
        print('  SKIP  W12-14 Jinja (jinja2 없음)')
    if shutil.which('node') is None:
        print('  SKIP  W12-14 JS (node 없음)')
        return
    import json as _json
    from test_closed_param_labels import js_fn, run_node
    script = ('const made = [];\n'
              'const document = {getElementById: (id) => ({style: {}, textContent: "", insertBefore: () => {}, '
              'firstChild: null, querySelectorAll: () => []}), createElement: (t) => { const o = {dataset: {}, style: {}}; '
              'made.push(o); return o; }};\n' + js_fn(tpl, 'labAddRow') + '\n'
              f'const cases = {_json.dumps([m for _nm, m, _w, _a in cases], ensure_ascii=False)};\n'
              'const out = cases.map(c => { labAddRow(c); return made[made.length - 1].innerHTML; });\n'
              'console.log(JSON.stringify(out));\n')
    try:
        outs = run_node(script)
        if outs is None:
            raise RuntimeError('node 실행 실패')
        _check('W12-14 JS', outs, _esc)
    except Exception as e:                                  # noqa: BLE001
        chk('W12-14 JS 행 (node 실행)', False, f'{type(e).__name__}: {e}')


def main():
    try:
        import ptfe_face_alpha as FA
    except Exception as e:                                  # noqa: BLE001 — 구현 전 (모듈 없음) 도 기록
        FA = None
        print(f'  ⚠ ptfe_face_alpha 를 못 불러온다 ({type(e).__name__}: {e})')
    lab = getattr(FA, 'LABEL', '') if FA else ''
    chk('W1 표지 문자열 한정어 (PTFE 면 개구율 · α · Ø0.248 rope · 규약 선택 · 불투과 가정 · 전자/이온)',
        all(t in lab for t in ('PTFE 면 개구율', 'α', 'Ø0.248', 'rope', '규약 선택', '불투과 가정', '전자/이온')), lab)
    tpl = open(os.path.join(HERE, 'templates', 'mpm_lab.html'), encoding='utf-8').read()
    lines = tpl.splitlines()
    jinja = [ln for ln in lines if '{{ it.convention_label }}' in ln]
    js = [ln for ln in lines if '${it.convention_label}' in ln]
    chk('W2a Jinja 행이 매니페스트 ca_ext.ptfe_face 표지를 읽는다',
        len(jinja) == 1 and 'ca_ext' in jinja[0] and 'ptfe_face' in jinja[0] and 'label' in jinja[0], len(jinja))
    chk('W2b JS 행이 매니페스트 ca_ext.ptfe_face 표지를 읽는다',
        len(js) == 1 and 'ca_ext' in js[0] and 'ptfe_face' in js[0] and 'label' in js[0], len(js))
    chk('W2c 표지 문자열 사본을 템플릿에 두지 않는다 (producer 상수 하나)', bool(lab) and lab not in tpl)
    chk('W3 face_alpha + 관측 PTFE 셀 > 0 = 불일치 경고 (두 행)',
        all('face_alpha' in ln and 'ptfe_cells_observed' in ln for ln in (jinja + js)) and len(jinja + js) == 2)
    try:
        import jinja2
    except Exception:                                       # noqa: BLE001
        jinja2 = None
    if jinja2 is None:
        print('  SKIP  W5 · W6 (jinja2 없음)')
    else:
        env = jinja2.Environment(autoescape=True)
        try:
            env.parse(tpl)
            _parsed = True
        except jinja2.TemplateSyntaxError as e:
            _parsed = False
            print(f'      {e}')
        chk('W5 템플릿 전체가 Jinja 문법으로 파싱된다', _parsed)
        if len(jinja) == 1:
            row = env.from_string(jinja[0])
            fa = {'mpm_metrics': {'step3': {'manifest': {'ptfe_stamp': 'face_alpha', 'ptfe_cells_observed': 0,
                                                         'ca_ext': {'ptfe_face': {'evidence': {'label': lab}}}}}}}
            bad = {'mpm_metrics': {'step3': {'manifest': {'ptfe_stamp': 'face_alpha', 'ptfe_cells_observed': 7,
                                                          'ca_ext': {'ptfe_face': {'evidence': {'label': lab}}}}}}}
            out_fa = row.render(it=fa)
            out_bad = row.render(it=bad)
            out_plain = row.render(it={'mpm_metrics': {}})
            out_none = row.render(it={})
            from markupsafe import escape as _escape
            esc = str(_escape(lab)) if lab else '\0'
            chk('W6 Jinja 행 렌더 — face_alpha = 표지 · 셀 > 0 = 경고 · 옛 meta (매니페스트 없음) = 둘 다 없음',
                esc in out_fa and '이중 계상 의심' not in out_fa and '이중 계상 의심' in out_bad
                and esc not in out_plain and '🧱' not in out_plain and '🧱' not in out_none,
                (out_fa[-200:], out_plain[-120:]))
    if shutil.which('node') is None:
        print('  SKIP  W7 (node 없음)')
    else:
        import json as _json
        from test_closed_param_labels import js_fn, run_node
        mk = lambda cells, with_ca: {'id': 'x', 'has_additives': True, 'recipe': 'PTFE 1', 'convention_label': 'PTFE face_alpha',   # noqa: E731
                                     'mpm_metrics': ({'step3': {'manifest': {'ptfe_stamp': 'face_alpha', 'ptfe_cells_observed': cells,
                                                                            **({'ca_ext': {'ptfe_face': {'evidence': {'label': lab}}}}
                                                                               if with_ca else {})}}}
                                                     if with_ca is not None else {})}
        script = ('const made = [];\n'
                  'const document = {getElementById: (id) => ({style: {}, textContent: "", insertBefore: () => {}, '
                  'firstChild: null, querySelectorAll: () => []}), createElement: (t) => { const o = {dataset: {}, style: {}}; '
                  'made.push(o); return o; }};\n' + js_fn(tpl, 'labAddRow') + '\n'
                  f'const cases = {_json.dumps([mk(0, True), mk(5, True), mk(0, None)], ensure_ascii=False)};\n'
                  'const out = cases.map(c => { labAddRow(c); return made[made.length - 1].innerHTML; });\n'
                  'console.log(JSON.stringify(out));\n')
        try:
            o_fa, o_bad, o_old = run_node(script)          # run_node = 마지막 줄 JSON (실패면 None → 아래 except)
            chk('W7 JS 행 (node 실행) — face_alpha = 표지 · 셀 > 0 = 경고 · 옛 meta = 둘 다 없음',
                lab in o_fa and '이중 계상 의심' not in o_fa and '이중 계상 의심' in o_bad and '🧱' not in o_old)
        except Exception as e:                              # noqa: BLE001
            chk('W7 JS 행 (node 실행)', False, f'{type(e).__name__}: {e}')
    import mpm_lab_register as REG                         # 봉인 파일 — 읽기만 (고치지 않는다)
    data = {'mpm_metrics': {'step3': {'manifest': {'ptfe_stamp': 'face_alpha', 'ptfe_stamp_requested': 'face_alpha',
                                                   'ptfe_cells_observed': 0, 'vox_um': 0.15}}}}
    meta = REG.build_meta(data, 'fa_case', uploaded_at='2026-10-20 00:00', size_mb=0.1)
    chk('W4 봉인 build_meta → 규약 칩 "PTFE face_alpha" · 불일치 없음',
        'PTFE face_alpha' in meta.get('convention_label', '') and meta.get('convention_mismatch') == [],
        (meta.get('convention_label'), meta.get('convention_mismatch')))
    _b6_labels(tpl, jinja, js, jinja2, REG)
    _d_states(tpl, jinja, js, jinja2)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
