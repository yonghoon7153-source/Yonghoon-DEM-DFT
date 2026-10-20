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

  python3 webapp/test_ca_ext_labels.py
"""
import os
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
    import mpm_lab_register as REG                         # 봉인 파일 — 읽기만 (고치지 않는다)
    data = {'mpm_metrics': {'step3': {'manifest': {'ptfe_stamp': 'face_alpha', 'ptfe_stamp_requested': 'face_alpha',
                                                   'ptfe_cells_observed': 0, 'vox_um': 0.15}}}}
    meta = REG.build_meta(data, 'fa_case', uploaded_at='2026-10-20 00:00', size_mb=0.1)
    chk('W4 봉인 build_meta → 규약 칩 "PTFE face_alpha" · 불일치 없음',
        'PTFE face_alpha' in meta.get('convention_label', '') and meta.get('convention_mismatch') == [],
        (meta.get('convention_label'), meta.get('convention_mismatch')))
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
