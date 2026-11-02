#!/usr/bin/env python3
"""진도점검 덱 (2026-11-04 회의 · DEM 8 장) 검사 — 화면 · 표 · 노트의 숫자 = 원자료 · 1저자 11-02 규칙.

숫자 원천 (리포): docs/50kg/report_y4/draft2/metrics_all.csv · docs/50kg/report_y4/draft2/figs/p5_breakeven_sigma.csv
검사:
  N  숫자 — 원자료에서 다시 계산해 만든 글이 정해진 장의 화면 · 표 · 노트에 있는가
  W  금지 낱말 (내부 용어 · 지운 단서 · D0.7) 이 화면 · 표 · 노트에 없는가
  C  캡션 (Text Box 36) 에 왼쪽 · 오른쪽 이 없는가
  R  빨강 (FF5050) = 나쁜 결과 문구 셋에만
  I  σ = 이탤릭 · 바로 뒤 첨자 (eff · 0) = 아래첨자 · 똑바로
  F  글꼴 = KoPubWorld돋움체
사용:
  python3 -I check_meeting_deck.py <deck.pptx> --repo <리포> [--json out.json]
  python3 -I check_meeting_deck.py <deck.pptx> --repo <리포> --selftest   (덱을 메모리에서 다섯 가지로 망가뜨려 각각 FAIL 인지)
"""
import argparse
import copy
import csv
import io
import json
import os
import re
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

ORDER = ('D3', 'D2', 'D1')                       # 3 → 2 → 1 µm
RED_OK = {'전해질 이온전도도 감소 (0.45배)와 상쇄', '이온전도도 감소', '미립 전해질 이온전도도 감소 (0.45배)와 상쇄'}
BANNED = r'(?i)hertz|physics|union|sphere|ε|합집합|수송 tortuosity|이온 이동 경로|156|재확인|빗금|D0\.7|0\.7 ?µm|0\.66'


def load_data(repo):
    d2 = os.path.join(repo, 'docs/50kg/report_y4/draft2')
    rows = {r['bed']: r for r in csv.DictReader(open(os.path.join(d2, 'metrics_all.csv'), encoding='utf-8'))}
    be = list(csv.DictReader(open(os.path.join(d2, 'figs/p5_breakeven_sigma.csv'), encoding='utf-8')))
    meas = {r['bed']: float(r['sigma_meas_mScm']) for r in be if r['kind'] == 'measured' and r['sigma_meas_mScm']}
    req = {r['bed']: float(r['sigma_req_mScm']) for r in be if r['kind'] == 'required' and r['basis'] == 'f_mc Hertz'}
    return rows, meas, req


def expected(rows, meas, req):
    """(장 번호, 칸 'screen'|'table'|'notes'|'any', 있어야 할 글, 근거) — 글은 원자료에서 다시 만든다."""
    v = lambda b, k: float(rows[b][k])
    eps = [f"{v(b, 'eps_union_exact_pct'):.1f}" for b in ORDER]
    cn = [f"{v(b, 'am_se_cn_mean'):.0f}" for b in ORDER]
    cov = [f"{v(b, 'coverage_physics_union_pct'):.1f}" for b in ORDER]
    f3 = v('D3', 'f_ion_hertz')
    frel = [f"{v(b, 'f_ion_hertz') / f3:.1f}" for b in ORDER]
    tau = [f"{v(b, 'tau2_ion_hertz'):.1f}" for b in ORDER]
    cps = [100 * v(b, 'constriction_power_share_ion_hertz') for b in ORDER]
    pel3, pel1 = meas['D3'], meas['D1']
    loss = pel1 / pel3
    need = req['D1']
    ratio_cn = v('D1', 'am_se_cn_mean') / v('D3', 'am_se_cn_mean')
    gain = v('D1', 'f_ion_hertz') / f3
    E = []
    E += [(1, 'table', x, 'eps_union_exact_pct') for x in eps]
    E += [(4, 'screen', f'({eps[0]} → {eps[1]} → {eps[2]} %)', 'eps_union_exact_pct')]
    E += [(1, 'table', x, 'am_se_cn_mean (반올림)') for x in cn]
    E += [(5, 'screen', f'({cn[0]} → {cn[1]} → {cn[2]}개)', 'am_se_cn_mean')]
    assert 9.5 <= ratio_cn < 10.5, ratio_cn
    E += [(1, 'screen', '접촉 수 약 10배', f'D1/D3 = {ratio_cn:.3f}'), (5, 'screen', '접촉 수 약 10배', f'D1/D3 = {ratio_cn:.3f}'),
          (8, 'screen', '접촉 수 약 10배', f'D1/D3 = {ratio_cn:.3f}')]
    E += [(1, 'table', x, 'coverage_physics_union_pct') for x in cov]
    E += [(5, 'screen', f'증가하지 않음 ({cov[0]} → {cov[1]} → {cov[2]} %)', 'coverage_physics_union_pct (1저자 11-02 문구)')]
    E += [(1, 'table', x, 'f_ion_hertz / f_ion_hertz(D3)') for x in frel]
    E += [(6, 'screen', f'{frel[1]}배 (2 µm), {frel[2]}배 (1 µm)', 'f_ion_hertz 비')]
    E += [(1, 'table', x, 'tau2_ion_hertz') for x in tau]
    E += [(6, 'screen', f'({tau[0]} → {tau[1]} → {tau[2]})', 'tau2_ion_hertz')]
    E += [(1, 'table', f'{pel3:.1f}', '펠릿 실측 3 µm'), (1, 'table', f'{pel1:.1f}', '펠릿 실측 1 µm')]
    E += [(2, 'screen', f'{pel3:.1f} → {pel1:.1f}', '펠릿 실측 (단위 표기 = 1저자 mS cm⁻¹)')]
    E += [(n, 'screen', f'{loss:.2f}배', f'{pel1}/{pel3} = {loss:.4f}') for n in (1, 7, 8)]
    E += [(7, 'screen', f'{need:.1f} mS/cm', f'필요 σ (f_mc Hertz) = {need:.5f}')]
    E += [(7, 'screen', f'{need / pel3:.2f}배', f'{need:.5f}/{pel3} = {need / pel3:.4f}')]
    E += [(7, 'screen', f'{gain:.1f}배 × 전해질 이온전도도 {loss:.2f}배 ≈ {gain * loss:.1f}배', f'{gain:.4f} × {loss:.4f} = {gain * loss:.4f}')]
    E += [(6, 'notes', f'{min(cps):.0f}–{max(cps):.0f} %', f'constriction_power_share_ion_hertz × 100 = {", ".join(f"{c:.1f}" for c in cps)}')]
    assert 0.70 <= min(cps) / 100 and max(cps) / 100 <= 0.80
    E += [(8, 'screen', f'{min(cps):.0f}–{max(cps):.0f} %가 전해질–전해질 접촉부', f'{min(cps):.1f}–{max(cps):.1f} %')]
    E += [(7, 'screen', f'↔ 실측 {pel1:.1f}', '펠릿 실측 1 µm')]
    E += [(7, 'notes', '조건부 추정', 'KG50B-02 조건 (노트)')]
    return E


def slide_texts(prs):
    out = []
    for s in prs.slides:
        scr = '\n'.join(''.join(r.text for r in p.runs) for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs)
        tab = '\n'.join(c.text for sh in s.shapes if getattr(sh, 'has_table', False) and sh.has_table for row in sh.table.rows for c in row.cells)
        notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ''
        out.append({'screen': scr, 'table': tab, 'notes': notes})
    return out


def run_checks(prs, rows, meas, req):
    prob, ok = [], 0
    T = slide_texts(prs)
    if len(T) != 8:
        prob.append(f'장 수 {len(T)} ≠ 8')
    for n, where, txt, src in expected(rows, meas, req):
        hay = T[n - 1]['screen'] + '\n' + T[n - 1]['table'] + '\n' + T[n - 1]['notes'] if where == 'any' else T[n - 1][where]
        if txt in hay:
            ok += 1
        else:
            prob.append(f'N {n}장 {where}: "{txt}" 없음 ({src})')
    for n, t in enumerate(T, 1):
        for where, s in t.items():
            for m in re.finditer(BANNED, s):
                prob.append(f'W {n}장 {where}: 금지 "{m.group(0)}" …{s[max(0, m.start() - 15):m.end() + 15]}…')
    for n, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.name == 'Text Box 36' and sh.has_text_frame and re.search('왼쪽|오른쪽', sh.text_frame.text):
                prob.append(f'C {n}장 캡션: {sh.text_frame.text}')
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                runs = p.runs
                for k, r in enumerate(runs):
                    rpr = r._r.find(qn('a:rPr'))
                    if rpr is None:
                        continue
                    c = rpr.find(qn('a:solidFill') + '/' + qn('a:srgbClr'))
                    if c is not None and c.get('val') == 'FF5050' and r.text not in RED_OK:
                        prob.append(f'R {n}장 빨강: "{r.text}"')
                    if r.text == 'σ':
                        if rpr.get('i') != '1':
                            prob.append(f'I {n}장 σ 이탤릭 아님')
                        nxt = runs[k + 1] if k + 1 < len(runs) else None
                        nrpr = nxt._r.find(qn('a:rPr')) if nxt is not None else None
                        if nxt is None or nxt.text not in ('eff', '0') or nrpr is None or nrpr.get('baseline') != '-25000' or nrpr.get('i') == '1':
                            prob.append(f'I {n}장 σ 뒤 첨자 (eff · 0 · 아래첨자 · 똑바로) 아님')
                    lat = rpr.find(qn('a:latin'))
                    if re.search('[가-힣A-Za-z]', r.text) and (lat is None or not lat.get('typeface', '').startswith('KoPubWorld')):   # 기호만 든 run (예: 위첨자 −1) 은 글꼴 자유
                        prob.append(f'F {n}장 글꼴 {lat.get("typeface") if lat is not None else "없음"}: "{r.text[:20]}"')
    return ok, prob


def mutate(prs_bytes, kind):
    prs = Presentation(io.BytesIO(prs_bytes))
    s = prs.slides
    if kind == 'number':
        for sh in s[0].shapes:
            if getattr(sh, 'has_table', False) and sh.has_table:
                for row in sh.table.rows:
                    for c in row.cells:
                        for p in c.text_frame.paragraphs:
                            for r in p.runs:
                                if r.text == '22.4':
                                    r.text = '22.5'
                                    return prs
    if kind == 'caption':
        for sh in s[3].shapes:
            if sh.name == 'Text Box 36':
                r = sh.text_frame.paragraphs[0].runs[0]
                r.text = r.text.replace(' 】', ' (왼쪽) 】')
                return prs
    if kind == 'red':
        for sh in s[3].shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.text == '전해질 미립화':
                            rpr = r._r.get_or_add_rPr()
                            for f in rpr.findall(qn('a:solidFill')):
                                rpr.remove(f)
                            fill = rpr.makeelement(qn('a:solidFill'), {})
                            fill.append(fill.makeelement(qn('a:srgbClr'), {'val': 'FF5050'}))
                            rpr.insert(0, fill)
                            return prs
    if kind == 'italic':
        for sh in s[0].shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.text == 'σ':
                            r._r.find(qn('a:rPr')).attrib.pop('i', None)
                            return prs
    if kind == 'banned':
        p = s[5].notes_slide.notes_text_frame.paragraphs[0]
        p.runs[-1].text += ' (hertz)'
        return prs
    raise SystemExit(f'변이 자리 못 찾음: {kind}')


def main():
    ap = argparse.ArgumentParser(description='진도점검 덱 검사 (숫자 = 원자료 · 1저자 11-02 규칙)')
    ap.add_argument('deck', help='덱 PPTX')
    ap.add_argument('--repo', default='.', help='리포 뿌리 (원자료 CSV 위치)')
    ap.add_argument('--json', help='결과 JSON 저장 경로')
    ap.add_argument('--selftest', action='store_true', help='덱을 다섯 가지로 망가뜨려 각각 FAIL 인지 확인')
    a = ap.parse_args()
    rows, meas, req = load_data(a.repo)
    raw = open(a.deck, 'rb').read()
    ok, prob = run_checks(Presentation(io.BytesIO(raw)), rows, meas, req)
    res = {'deck': os.path.basename(a.deck), 'n_number_checks_ok': ok, 'problems': prob}
    if a.selftest:
        st = {}
        for kind in ('number', 'caption', 'red', 'italic', 'banned'):
            _, pb = run_checks(mutate(raw, kind), rows, meas, req)
            st[kind] = len(pb) > len(prob)
        res['selftest_mutations_detected'] = st
    if a.json:
        json.dump(res, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'숫자 검사 통과 {ok} · 문제 {len(prob)}')
    for p in prob:
        print('  ', p)
    if a.selftest:
        print('변이 탐지:', res['selftest_mutations_detected'])
        return 0 if (not prob and all(res['selftest_mutations_detected'].values())) else 1
    return 0 if not prob else 1


if __name__ == '__main__':
    sys.exit(main())
