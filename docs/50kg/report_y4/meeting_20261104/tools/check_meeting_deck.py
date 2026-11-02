#!/usr/bin/env python3
"""진도점검 덱 (2026-11-04 회의 · DEM 11 장 — 11-02 이야기 보강 + MPM 장) 검사 — 화면 · 표 · 노트의 숫자 = 원자료 · 1저자 11-02 규칙.

장 = 장 머리 글 (Rectangle 23 첫 문단) 의 낱말로 찾는다 (번호 고정 아님 — 11-02 MPM 장 · 영률 장 끼우기).  모든 장이 역할 하나씩 · 역할마다 장 하나.

숫자 원천 (리포): docs/50kg/report_y4/draft2/metrics_all.csv · docs/50kg/report_y4/draft2/figs/p5_breakeven_sigma.csv
검사:
  N  숫자 — 원자료에서 다시 계산해 만든 글이 정해진 장의 화면 · 표 · 노트에 있는가
  W  금지 낱말 (내부 용어 · 지운 단서 · D0.7) 이 화면 · 표 · 노트에 없는가
  C  캡션 (Text Box 36) 에 왼쪽 · 오른쪽 이 없는가
  R  빨강 (FF5050) = 나쁜 결과 문구 셋에만
  I  σ = 이탤릭 · 바로 뒤 첨자 (eff · 0) = 아래첨자 · 똑바로
  F  글꼴 = KoPubWorld돋움체
  M  MPM 장: MPM 기공도 (리포 묶음 docs/data/kg50_mpm_20261102) 숫자 · MPM 피복률 숫자 없음 (1저자 11-02 Q4 · 원장 MPMC-01 – 03)
  E  영률 장 (선택 · 2 µm 전해질 영률 0.675 · 1.35 · 2.025 GPa): 머리 글 영률 셋 · 표 머리 = 영률 차례 · 일곱 줄 칸 = 기록에서 다시 만든 글
     (draft2 metrics_<침대>.json · tools/modulus_load_share.py 출력 · 묶음 sha256 결합 · 기록 없는 침대 = '—') · 표 안 σ 이탤릭/첨자 · 글꼴
사용:
  python3 -I check_meeting_deck.py <deck.pptx> --repo <리포> [--json out.json]
      [--modulus-data-root <draft2 출력 뿌리 · 기본 리포 draft2>] [--modulus-load-share <modulus_load_share.json · 기본 values/modulus/>]
  python3 -I check_meeting_deck.py <deck.pptx> --repo <리포> --selftest   (덱을 메모리에서 망가뜨려 각각 FAIL 인지 · 영률 장이 있으면 칸 값 변이 포함)
"""
import argparse
import copy
import csv
import io
import json
import os
import re
import sys
import tarfile

from pptx import Presentation
from pptx.oxml.ns import qn

ORDER = ('D3', 'D2', 'D1')                       # 3 → 2 → 1 µm
RED_OK = {'전해질 이온전도도 감소 (0.45배)와 상쇄', '이온전도도 감소', '미립 전해질 이온전도도 감소 (0.45배)와 상쇄'}
BANNED = r'(?i)hertz|physics|union|sphere|ε|합집합|수송 tortuosity|이온 이동 경로|156|재확인|빗금|D0\.7|0\.7 ?µm|0\.66'
#: 장 역할 ← 장 머리 글 (Rectangle 23 첫 문단) 의 낱말 · 차례 = 덱 차례 · optional = 아직 없어도 됨 (영률 장 = E05 · E15 끝난 뒤)
ROLES = (('summary', '해석 결과 요약'), ('background', '미립화 검토 배경'), ('method', '미세구조 시뮬레이션'), ('porosity', '기공도 변화'),
         ('contact', '활물질/전해질 접촉'), ('mpm', 'MPM 소성 해석'), ('network', '전해질 접촉 망'), ('ionic', '유효 이온전도도 및 이온 전류'),
         ('breakeven', '손익분기'), ('modulus', '영률'), ('conclusion', 'DEM 해석 결론'), ('appendix', '부록'))
OPTIONAL = {'modulus'}
#: 옛 번호 (10 장 판) → 역할 — expected() 의 장 번호는 이 표로 역할이 된다
OLD_NO = {1: 'summary', 2: 'background', 4: 'porosity', 5: 'contact', 6: 'network', 7: 'ionic', 8: 'breakeven', 9: 'conclusion', 10: 'appendix'}
MPM_KIT = {'261102_091413_c2e9a7': 'D3', '261102_091440_0845a7': 'D2', '261102_091500_598f38': 'D1'}


def load_data(repo):
    d2 = os.path.join(repo, 'docs/50kg/report_y4/draft2')
    rows = {r['bed']: r for r in csv.DictReader(open(os.path.join(d2, 'metrics_all.csv'), encoding='utf-8'))}
    be = list(csv.DictReader(open(os.path.join(d2, 'figs/p5_breakeven_sigma.csv'), encoding='utf-8')))
    meas = {r['bed']: float(r['sigma_meas_mScm']) for r in be if r['kind'] == 'measured' and r['sigma_meas_mScm']}
    req = {r['bed']: float(r['sigma_req_mScm']) for r in be if r['kind'] == 'required' and r['basis'] == 'f_mc Hertz'}
    szz = json.load(open(os.path.join(repo, 'docs/50kg/report_y4/meeting_20261104/values/szz_share/plane_load.json'), encoding='utf-8'))['cases']
    mpm = {}
    with tarfile.open(os.path.join(repo, 'docs/data/kg50_mpm_20261102/kg50_mpm_results_slim.tgz'), 'r:gz') as tf:
        for m in tf.getmembers():
            if m.isfile() and m.name.endswith('/latest_run/payload_slim.json'):
                mm = json.load(tf.extractfile(m))['mpm_metrics']
                mpm[MPM_KIT[m.name.split('/')[0]]] = mm
    assert set(mpm) == set(ORDER), mpm.keys()
    rows['_mpm'] = mpm
    return rows, meas, req, szz


MOD_BEDS = ('D2E05', 'D2', 'D2E15')          # 영률 차례 (0.675 → 1.35 → 2.025 GPa)
SIGMA0 = 1.5                                  # mS/cm — 보고 기준 (7장 · 부록 표와 같음)
#: 영률 장 표 줄 (첫 칸이 이 글로 시작 · 정의) — 칸 글은 load_modulus 의 기록에서 만든다
MOD_ROWS = (('기공도', 'eps_union_exact_pct · .1f'), ('활물질 표면 피복률', 'coverage_physics_union_pct · .1f'),
            ('유효 이온전도도', 'f_ion_hertz × σ0 1.5 · .3f'), ('활물질 응력', 'lw_am_nowall_median_MPa ÷ p_end_MPa · .2f'),
            ('가압 하중 중 활물질–활물질 몫', 'plane21 contribution AM–AM · .1f'), ('활물질–전해질 접촉점 압력', 'AM–SE |Fn|/면적 평균 · .0f'),
            ('끝 판 압력', 'p_end_MPa · .1f'))


def load_modulus(repo, data_root=None, load_share=None):
    """영률 장 원자료 → dict(E, rec, ls, problems).  D2 = 리포 기록 · 변형 = data_root/data/<침대>/ · 짐 몫 · 접촉 압력 = load_share JSON."""
    sys.path.insert(0, os.path.join(repo, 'docs/50kg/report_y4/draft2'))
    import run_draft2_metrics as R
    src = R.src
    data_root = data_root or str(R.HERE)
    load_share = load_share or os.path.join(repo, 'docs/50kg/report_y4/meeting_20261104/values/modulus/modulus_load_share.json')
    b2 = next(x for x in src.BEDS if x['case'] == R.CASE['D2'])
    E = {'D2': src.parse_deck(src.rp(b2['deck']).read_text(encoding='utf-8'), b2['case'])['E_se_GPa']}
    E.update({b: R._gpa(R.E_BEDS[b]['se_E_sim']) for b in R.E_BEDS})
    prob, rec, ls = [], {}, {}
    lsd = json.load(open(load_share, encoding='utf-8'))['beds'] if os.path.isfile(load_share) else {}
    for b in MOD_BEDS:
        pth = str(R.BASE_D2_RECORD) if b == 'D2' else os.path.join(data_root, 'data', b, f'metrics_{b}.json')
        if not os.path.isfile(pth):
            rec[b] = ls[b] = None
            continue
        r = json.load(open(pth, encoding='utf-8'))
        if r.get('schema') != R.SCHEMA or r.get('bed') != b:
            prob.append(f'E 기록 {pth}: schema · 침대 이름')
        if b != 'D2' and abs(r['variant']['se_E_GPa'] - E[b]) > 1e-12:
            prob.append(f'E 기록 {b}: 영률 {r["variant"]["se_E_GPa"]} ≠ 설계 {E[b]}')
        e = lsd.get(b)
        if not e or e.get('status') != 'OK' or e['plane21']['status'] != 'OK':
            prob.append(f'E {b}: 짐 몫 · 접촉 압력 기록 없음 또는 상태 OK 아님 ({load_share})')
            e = None
        elif e['end_set']['tgz_sha256'] != r['provenance']['end_set']['tgz_sha256']:
            prob.append(f'E {b}: 짐 몫 기록 묶음 sha256 ≠ metrics 묶음 sha256')
            e = None
        rec[b], ls[b] = r, e
    if rec['D2'] is None:
        prob.append('E 기준 D2 기록 없음')
    return dict(E=E, rec=rec, ls=ls, problems=prob, data_root=data_root, load_share=load_share)


def modulus_expected(mod, szz):
    """→ (머리 글 조각, 표 머리 [영률 셋], [(첫 칸 낱말, [칸 글 셋])], 문제).  기록 없는 침대 = '—'."""
    prob = []
    E = mod['E']
    gtxt = [f'{E[b]:g}' for b in MOD_BEDS]
    rows = []
    for key, _ in MOD_ROWS:
        vals = []
        for b in MOD_BEDS:
            r, e = mod['rec'][b], mod['ls'][b]
            if r is None or e is None:
                vals.append('—')
                continue
            m = r['metrics']
            x = {'기공도': f"{m['eps_union_exact_pct']:.1f}", '활물질 표면 피복률': f"{m['coverage_physics_union_pct']:.1f}",
                 '유효 이온전도도': f"{SIGMA0 * m['f_ion_hertz']:.3f}", '활물질 응력': f"{m['lw_am_nowall_median_MPa'] / m['p_end_MPa']:.2f}",
                 '가압 하중 중 활물질–활물질 몫': f"{e['plane21']['contribution_sigma_zz_pct']['AM–AM']:.1f}",
                 '활물질–전해질 접촉점 압력': f"{e['am_se_contact_pressure']['mean_MPa']:.0f}", '끝 판 압력': f"{m['p_end_MPa']:.1f}"}[key]
            vals.append(x)
        rows.append((key, vals))
    if mod['ls'].get('D2'):                    # 기준 D2 짐 몫 = 부록 표 (values/szz_share) 와 같은 값이어야 한다
        a_ = mod['ls']['D2']['plane21']['contribution_sigma_zz_pct']
        b_ = szz['SE2um']['contribution_sigma_zz_pct']
        if any(abs(a_[g] - b_[g]) > 1e-9 for g in ('AM–AM', 'AM–SE', 'SE–SE')):
            prob.append(f'E 기준 D2 짐 몫 {a_} ≠ 부록 기록 {b_}')
    return f'2 µm: {gtxt[0]} · {gtxt[1]} · {gtxt[2]} GPa', [f'{g} GPa' for g in gtxt], rows, prob


def check_modulus(prs, i, mod, szz):
    s = prs.slides[i]
    ok, prob = 0, list(mod['problems'])
    head_txt, hdr, rows, p2 = modulus_expected(mod, szz)
    prob += p2
    h = ''.join(''.join(r.text for r in sh.text_frame.paragraphs[0].runs) for sh in s.shapes if sh.name == 'Rectangle 23')
    if head_txt in h:
        ok += 1
    else:
        prob.append(f'E {i + 1}장 머리 글에 "{head_txt}" 없음 ("{h}")')
    tabs = [sh for sh in s.shapes if getattr(sh, 'has_table', False) and sh.has_table]
    if len(tabs) != 1:
        return ok, prob + [f'E {i + 1}장 표 {len(tabs)} 개 (하나여야 함)']
    t = tabs[0].table
    cell = lambda r, c: t.cell(r, c).text.strip()
    if len(t.columns) != 4:
        return ok, prob + [f'E {i + 1}장 표 열 {len(t.columns)} (4 여야 함)']
    got_hdr = [cell(0, c) for c in (1, 2, 3)]
    if got_hdr == hdr:
        ok += 1
    else:
        prob.append(f'E {i + 1}장 표 머리 {got_hdr} ≠ {hdr}')
    for key, vals in rows:
        hit = [r for r in range(1, len(t.rows)) if cell(r, 0).startswith(key)]       # 첫 칸 = 줄 이름으로 시작
        if len(hit) != 1:
            prob.append(f'E {i + 1}장 표 "{key}" 줄 {len(hit)} 개')
            continue
        got = [cell(hit[0], c) for c in (1, 2, 3)]
        if got == vals:
            ok += 1
        else:
            prob.append(f'E {i + 1}장 표 "{key}" {got} ≠ 기록 {vals}')
    if len(t.rows) != 1 + len(rows):
        prob.append(f'E {i + 1}장 표 줄 {len(t.rows)} ≠ {1 + len(rows)}')
    for r_ in t.rows:                          # 표 안 글자 규칙 (표는 아래 공통 I · F 검사 밖이라 여기서)
        for c_ in r_.cells:
            for p_ in c_.text_frame.paragraphs:
                runs = p_.runs
                for k, r in enumerate(runs):
                    rpr = r._r.find(qn('a:rPr'))
                    lat = rpr.find(qn('a:latin')) if rpr is not None else None
                    if re.search('[가-힣A-Za-z]', r.text) and (lat is None or not lat.get('typeface', '').startswith('KoPubWorld')):
                        prob.append(f'F {i + 1}장 표 글꼴: "{r.text[:20]}"')
                    c = rpr.find(qn('a:solidFill') + '/' + qn('a:srgbClr')) if rpr is not None else None
                    if c is not None and c.get('val') == 'FF5050':
                        prob.append(f'R {i + 1}장 표 빨강: "{r.text}"')
                    if r.text == 'σ':
                        nxt = runs[k + 1] if k + 1 < len(runs) else None
                        nrpr = nxt._r.find(qn('a:rPr')) if nxt is not None else None
                        if rpr is None or rpr.get('i') != '1' or nxt is None or nxt.text not in SIGMA_SUB or nrpr is None \
                                or nrpr.get('baseline') != '-25000' or nrpr.get('i') == '1':
                            prob.append(f'I {i + 1}장 표 σ 이탤릭 · 첨자 아님')
    return ok, prob


def expected(rows, meas, req, szz):
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
          (9, 'screen', '접촉 수 약 10배', f'D1/D3 = {ratio_cn:.3f}')]
    E += [(1, 'table', x, 'coverage_physics_union_pct') for x in cov]
    E += [(5, 'screen', f'증가하지 않음 ({cov[0]} → {cov[1]} → {cov[2]} %)', 'coverage_physics_union_pct (1저자 11-02 문구)')]
    E += [(1, 'table', x, 'f_ion_hertz / f_ion_hertz(D3)') for x in frel]
    E += [(7, 'screen', f'{frel[1]}배 (2 µm), {frel[2]}배 (1 µm)', 'f_ion_hertz 비')]
    E += [(1, 'table', x, 'tau2_ion_hertz') for x in tau]
    E += [(7, 'screen', f'({tau[0]} → {tau[1]} → {tau[2]})', 'tau2_ion_hertz')]
    E += [(1, 'table', f'{pel3:.1f}', '펠릿 실측 3 µm'), (1, 'table', f'{pel1:.1f}', '펠릿 실측 1 µm')]
    E += [(2, 'screen', f'{pel3:.1f} → {pel1:.1f}', '펠릿 실측 (단위 표기 = 1저자 mS cm⁻¹)')]
    E += [(n, 'screen', f'{loss:.2f}배', f'{pel1}/{pel3} = {loss:.4f}') for n in (1, 8, 9)]
    E += [(8, 'screen', f'{need:.1f} mS/cm', f'필요 σ (f_mc Hertz) = {need:.5f}')]
    E += [(8, 'screen', f'{need / pel3:.2f}배', f'{need:.5f}/{pel3} = {need / pel3:.4f}')]
    E += [(8, 'screen', f'{gain:.1f}배 × 전해질 이온전도도 {loss:.2f}배 ≈ {gain * loss:.1f}배', f'{gain:.4f} × {loss:.4f} = {gain * loss:.4f}')]
    E += [(7, 'notes', f'{min(cps):.0f}–{max(cps):.0f} %', f'constriction_power_share_ion_hertz × 100 = {", ".join(f"{c:.1f}" for c in cps)}')]
    assert 0.70 <= min(cps) / 100 and max(cps) / 100 <= 0.80
    E += [(9, 'screen', f'{min(cps):.0f}–{max(cps):.0f} %가 전해질–전해질 접촉부', f'{min(cps):.1f}–{max(cps):.1f} %')]
    E += [(8, 'screen', f'↔ 실측 {pel1:.1f}', '펠릿 실측 1 µm')]
    E += [(8, 'notes', '조건부 추정', 'KG50B-02 조건 (노트)')]
    # 11-02 이야기 보강 (6 · 7 · 10장) — 배위수 · 끊긴 입자 · σ0 1.5 기준 유효 이온전도도 · 부록 표 (가압 응력 기여 %)
    cse = [f"{v(b, 'se_se_cn_mean'):.1f}" for b in ORDER]
    cam = [f"{v(b, 'am_am_cn_mean'):.1f}" for b in ORDER]
    dsc = [f"{100 - v(b, 'percolation_pct'):.1f}" for b in ORDER]
    sig = [f"{1.5 * v(b, 'f_ion_hertz'):.3f}" for b in ORDER]
    E += [(6, 'screen', f'배위수 증가 ({cse[0]} → {cse[1]} → {cse[2]})', 'se_se_cn_mean')]
    E += [(6, 'screen', f'끊긴 입자 감소 ({dsc[0]} → {dsc[1]} → {dsc[2]} %)', '100 − percolation_pct')]
    E += [(6, 'notes', f'{cam[0]}, {cam[1]}, {cam[2]}개', 'am_am_cn_mean')]
    E += [(7, 'screen', f'{min(cps):.0f}–{max(cps):.0f} %가 전해질 접촉부', 'constriction_power_share_ion_hertz')]
    E += [(7, 'notes', f'3 µm {sig[0]}, 2 µm {sig[1]}, 1 µm {sig[2]} mS/cm', 'f_ion_hertz × σ0 1.5')]
    E += [(10, 'table', x, 'se_se_cn_mean') for x in cse] + [(10, 'table', x, 'am_am_cn_mean') for x in cam]
    E += [(10, 'table', x, 'f_ion_hertz × 1.5') for x in sig] + [(10, 'table', x, 'eps_union_exact_pct') for x in eps]
    for g in ('AM–AM', 'AM–SE', 'SE–SE'):
        E += [(10, 'table', f"{szz[lab]['contribution_sigma_zz_pct'][g]:.1f}", f'plane_load_share {lab} {g}') for lab in ('SE3um', 'SE2um', 'SE1um')]
    # 11-02 MPM 장 (1저자 Q3 · Q4) — MPM 기공도 = 리포 묶음 payload 의 mpm_metrics.porosity_mpm_pct
    pm = [f"{rows['_mpm'][b]['porosity_mpm_pct']:.1f}" for b in ORDER]
    E += [('mpm', 'screen', f'{pm[0]} → {pm[1]} → {pm[2]} %', 'MPM porosity_mpm_pct')]
    E += [('mpm', 'screen', f'기공도 {x} %', 'MPM porosity_mpm_pct') for x in pm]
    E += [('mpm', 'notes', f'3 µm {pm[0]} %, 2 µm {pm[1]} %, 1 µm {pm[2]} %', 'MPM porosity_mpm_pct')]
    return E


def slide_roles(prs):
    """장 머리 글 (Rectangle 23 첫 문단) → 역할.  → (역할 → 장 index, 문제)."""
    roles, prob = {}, []
    for i, s in enumerate(prs.slides):
        h = ''.join(''.join(r.text for r in sh.text_frame.paragraphs[0].runs) for sh in s.shapes
                    if sh.name == 'Rectangle 23' and sh.has_text_frame and sh.text_frame.paragraphs)
        hit = [r for r, key in ROLES if key in h]
        if len(hit) != 1:
            prob.append(f'역할 {i + 1}장: 머리 글 "{h[:40]}" → {hit or "없음"}')
            continue
        if hit[0] in roles:
            prob.append(f'역할 {hit[0]} 장 둘 ({roles[hit[0]] + 1} · {i + 1})')
        roles[hit[0]] = i
    prob += [f'역할 {r} 장 없음' for r, _ in ROLES if r not in roles and r not in OPTIONAL]
    order = [roles[r] for r, _ in ROLES if r in roles]
    if order != sorted(order):
        prob.append(f'장 차례 ≠ 역할 차례 ({order})')
    return roles, prob


def slide_texts(prs):
    out = []
    for s in prs.slides:
        scr = '\n'.join(''.join(r.text for r in p.runs) for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs)
        tab = '\n'.join(c.text for sh in s.shapes if getattr(sh, 'has_table', False) and sh.has_table for row in sh.table.rows for c in row.cells)
        notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ''
        out.append({'screen': scr, 'table': tab, 'notes': notes})
    return out


SIGMA_SUB = ('eff', '0', 'VM')                # σ 바로 뒤 아래첨자 (VM = 영률 장 활물질 응력 σ_VM)


def run_checks(prs, rows, meas, req, szz, mod=None):
    prob, ok = [], 0
    T = slide_texts(prs)
    roles, rprob = slide_roles(prs)
    prob += rprob
    if 'modulus' in roles:
        if mod is None:
            prob.append('E 영률 장이 있는데 원자료 (load_modulus) 를 안 읽었다')
        else:
            k, pb = check_modulus(prs, roles['modulus'], mod, szz)
            ok += k
            prob += pb
    for n, where, txt, src in expected(rows, meas, req, szz):
        role = OLD_NO[n] if isinstance(n, int) else n
        if role not in roles:
            prob.append(f'N {role}: 장 없음 ("{txt}")')
            continue
        i = roles[role]
        hay = T[i]['screen'] + '\n' + T[i]['table'] + '\n' + T[i]['notes'] if where == 'any' else T[i][where]
        if txt in hay:
            ok += 1
        else:
            prob.append(f'N {i + 1}장 ({role}) {where}: "{txt}" 없음 ({src})')
    if 'mpm' in roles:                      # M — MPM 피복률 숫자 없음 (Q4: 띠 정의 · 씨앗 치우침 · 주기 경계 = 원장 MPMC-01 – 03)
        t = T[roles['mpm']]
        hay = t['screen'] + '\n' + t['table'] + '\n' + t['notes']
        for b in ORDER:
            mm = rows['_mpm'][b]
            for k in ('coverage_AM_S_hertz_pct', 'coverage_AM_S_tabor_pct', 'coverage_AM_S_rigid_hertz_pct', 'coverage_AM_S_rigid_tabor_pct'):
                x = mm.get(k)
                for s_ in ({f'{x:.1f}', f'{x:.0f}'} if x is not None else ()):
                    if re.search(rf'(?<![\d.]){re.escape(s_)}(?![\d.])', hay):
                        prob.append(f'M {roles["mpm"] + 1}장: MPM 피복률 숫자 {s_} ({b} {k}) — 1저자 Q4 = 넣지 않음')
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
                        if nxt is None or nxt.text not in SIGMA_SUB or nrpr is None or nrpr.get('baseline') != '-25000' or nrpr.get('i') == '1':
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
    if kind == 'mpm_cov':
        roles, _ = slide_roles(prs)
        p = s[roles['mpm']].notes_slide.notes_text_frame.paragraphs[0]
        p.runs[-1].text += ' 1 µm 피복률은 80 %입니다.'
        return prs
    if kind == 'modulus_value':               # 영률 장 표의 기공도 줄 마지막 칸 (2.025 GPa) 숫자 끝자리 하나 바꿈
        roles, _ = slide_roles(prs)
        t = [sh for sh in s[roles['modulus']].shapes if getattr(sh, 'has_table', False) and sh.has_table][0].table
        for row in t.rows:
            if row.cells[0].text.startswith('기공도'):
                r = row.cells[3].text_frame.paragraphs[0].runs[0]
                r.text = r.text[:-1] + ('1' if r.text[-1] != '1' else '2')
                return prs
    raise SystemExit(f'변이 자리 못 찾음: {kind}')


def main():
    ap = argparse.ArgumentParser(description='진도점검 덱 검사 (숫자 = 원자료 · 1저자 11-02 규칙)')
    ap.add_argument('deck', help='덱 PPTX')
    ap.add_argument('--repo', default='.', help='리포 뿌리 (원자료 CSV 위치)')
    ap.add_argument('--json', help='결과 JSON 저장 경로')
    ap.add_argument('--selftest', action='store_true', help='덱을 망가뜨려 각각 FAIL 인지 확인 (영률 장이 있으면 칸 값 변이 포함)')
    ap.add_argument('--modulus-data-root', default=None, help='영률 변형 침대 metrics 뿌리 (data/<침대>/) — 기본 리포 draft2')
    ap.add_argument('--modulus-load-share', default=None, help='modulus_load_share.json — 기본 values/modulus/')
    a = ap.parse_args()
    rows, meas, req, szz = load_data(a.repo)
    raw = open(a.deck, 'rb').read()
    prs0 = Presentation(io.BytesIO(raw))
    has_mod = 'modulus' in slide_roles(prs0)[0]
    mod = load_modulus(a.repo, a.modulus_data_root, a.modulus_load_share) if has_mod else None
    ok, prob = run_checks(prs0, rows, meas, req, szz, mod)
    res = {'deck': os.path.basename(a.deck), 'n_slides': len(prs0.slides), 'n_number_checks_ok': ok, 'problems': prob,
           'modulus': (dict(data_root=mod['data_root'], load_share=mod['load_share'],
                            beds_with_record=[b for b in MOD_BEDS if mod['rec'][b] is not None]) if mod else None)}
    if a.selftest:
        st = {}
        for kind in ('number', 'caption', 'red', 'italic', 'banned', 'mpm_cov') + (('modulus_value',) if has_mod else ()):
            _, pb = run_checks(mutate(raw, kind), rows, meas, req, szz, mod)
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
