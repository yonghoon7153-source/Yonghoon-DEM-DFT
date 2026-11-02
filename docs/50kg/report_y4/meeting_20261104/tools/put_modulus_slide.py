"""새 장 = 고체전해질 영률에 따른 변화 (2 µm: 0.675 · 1.35 · 2.025 GPa) — 손익분기 장 뒤 · 결론 장 앞 (11 → 12 장).
  결론 장 (머리 글 · 글머리 · 결과 표 꼴 = 12 pt KoPub 표) 을 손익분기 장 뒤로 복제 → 머리 글 · 글머리 한 줄 · 표 (영률 셋 × 일곱 줄) ·
  캡션 (부록 장 캡션 꼴 · σ0 기준) · 노트 한 문장.  빨강 없음 (나쁜 결과 표시 아님).
  칸 값 = 기록 그대로 (손으로 적은 숫자 없음):
    기공도 · 활물질 표면 피복률 · 유효 이온전도도 (f × σ0 1.5) · 활물질 응력 σ_VM ÷ 끝 판 압력 · 끝 판 압력 = draft2 metrics_<침대>.json
      (D2 = 리포 기록 · D2E05 · D2E15 = --data-root/data/<침대>/)
    가압 하중 중 활물질–활물질 몫 (21 단면 = 부록 표와 같은 도구) · 활물질–전해질 접촉점 압력 = tools/modulus_load_share.py 출력 (--load-share)
  기록이 없는 침대 = 칸 '—' (값을 만들지 않는다) · 글머리 · 노트의 방향 문장 = 있는 침대들의 값에서 단조 방향을 확인한 뒤에만 쓴다.
usage: python3 put_modulus_slide.py in.pptx out.pptx SKILL_DIR <repo> [--data-root <draft2 출력 뿌리>] [--load-share <json>]
  (add_slide.py = pptx 기술의 장 복제 도구 — 그 폴더의 office 모듈을 쓰므로 -I 없이 부른다)
"""
import argparse
import copy
import importlib
import json
import subprocess
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Inches

ap = argparse.ArgumentParser()
ap.add_argument('src')
ap.add_argument('dst')
ap.add_argument('skill')
ap.add_argument('repo')
ap.add_argument('--data-root', default=None, help='draft2 출력 뿌리 (data/<침대>/metrics_<침대>.json) — 기본 리포 draft2')
ap.add_argument('--load-share', default=None, help='modulus_load_share.json — 기본 values/modulus/')
a = ap.parse_args()
REPO = Path(a.repo).resolve()
sys.path.insert(0, str(REPO / 'docs/50kg/report_y4/draft2'))
R = importlib.import_module('run_draft2_metrics')
src = R.src
DATA_ROOT = Path(a.data_root).resolve() if a.data_root else R.HERE
LS_PATH = Path(a.load_share) if a.load_share else REPO / 'docs/50kg/report_y4/meeting_20261104/values/modulus/modulus_load_share.json'
SIGMA0 = 1.5                         # mS/cm — 덱 보고 기준 (7장 · 부록 표와 같음)
A = lambda t: qn('a:' + t)
BEDS = ('D2E05', 'D2', 'D2E15')      # 영률 차례

# ── 값 ─────────────────────────────────────────────────────────────
b2 = next(x for x in src.BEDS if x['case'] == R.CASE['D2'])
E = {'D2': src.parse_deck(src.rp(b2['deck']).read_text(encoding='utf-8'), b2['case'])['E_se_GPa']}
E.update({b: R._gpa(R.E_BEDS[b]['se_E_sim']) for b in R.E_BEDS})
assert sorted(BEDS, key=E.get) == list(BEDS), E
lsd = json.loads(LS_PATH.read_text(encoding='utf-8'))['beds'] if LS_PATH.is_file() else {}
rec, ls = {}, {}
for b in BEDS:
    pth = R.BASE_D2_RECORD if b == 'D2' else DATA_ROOT / 'data' / b / f'metrics_{b}.json'
    if not pth.is_file():
        rec[b] = ls[b] = None
        continue
    r = json.loads(pth.read_text(encoding='utf-8'))
    assert r['schema'] == R.SCHEMA and r['bed'] == b, pth
    if b != 'D2':
        assert abs(r['variant']['se_E_GPa'] - E[b]) < 1e-12, (b, r['variant'])
    e = lsd.get(b)
    assert e and e['status'] == 'OK' and e['plane21']['status'] == 'OK', f'{b}: 짐 몫 · 접촉 압력 기록 없음 또는 OK 아님 ({LS_PATH})'
    assert e['end_set']['tgz_sha256'] == r['provenance']['end_set']['tgz_sha256'], f'{b}: 짐 몫 기록 묶음 ≠ metrics 묶음'
    rec[b], ls[b] = r, e
assert rec['D2'] is not None
have = [b for b in BEDS if rec[b] is not None]
assert len(have) >= 2, have


def raw(b):
    m, e = rec[b]['metrics'], ls[b]
    return dict(por=m['eps_union_exact_pct'], cov=m['coverage_physics_union_pct'], sig=SIGMA0 * m['f_ion_hertz'],
                svm=m['lw_am_nowall_median_MPa'] / m['p_end_MPa'], amam=e['plane21']['contribution_sigma_zz_pct']['AM–AM'],
                cp=e['am_se_contact_pressure']['mean_MPa'], pend=m['p_end_MPa'])


FMT = dict(por='.1f', cov='.1f', sig='.3f', svm='.2f', amam='.1f', cp='.0f', pend='.1f')
V = {b: raw(b) for b in have}
cellv = {k: [format(V[b][k], f) if b in V else '—' for b in BEDS] for k, f in FMT.items()}
gtxt = [f'{E[b]:g}' for b in BEDS]


def mono(k):
    """있는 침대들 (영률 차례) 에서 k 의 방향: +1 = 영률과 함께 증가 · −1 = 감소 · 0 = 단조 아님."""
    xs = [V[b][k] for b in have]
    d = [y - x for x, y in zip(xs, xs[1:])]
    return 1 if all(v > 0 for v in d) else (-1 if all(v < 0 for v in d) else 0)


# 글머리 · 노트 = 값의 방향을 확인한 문장만 (어긋나면 멈춘다 — 문장을 바꿀지 사람이 정한다)
want = dict(por=1, cov=-1, sig=-1, amam=-1, svm=-1, cp=1)
bad = {k: mono(k) for k, w in want.items() if mono(k) != w}
assert not bad, f'방향이 문장과 다르다 {bad} (영률 차례 {have})'
cp_lo, cp_hi = V[have[0]]['cp'], V[have[-1]]['cp']
assert cp_hi / cp_lo > 1.5, (cp_lo, cp_hi)                  # '크게' 낮음
svm_lo, svm_hi = V[have[-1]]['svm'], V[have[0]]['svm']
assert 1.0 < svm_hi / svm_lo < 1.2, (svm_lo, svm_hi)        # '약간' 높음
HEAD = f'  고체전해질 영률에 따른 변화 (2 µm: {gtxt[0]} · {gtxt[1]} · {gtxt[2]} GPa)'
BULLET = '영률이 낮을수록 기공도 감소, 피복률 · 유효 이온전도도 증가, 접촉점 압력 감소'
egs = ', '.join(f'{E[b]:g}' for b in have)
NOTE = (f'2 µm 전해질의 영률을 {egs} GPa로 바꾼 계산에서, 영률이 낮을수록 기공도는 낮고 활물질 표면 피복률과 유효 이온전도도는 높으며, '
        '가압 하중을 활물질–활물질 접촉이 더 많이 지고 활물질 응력도 약간 높아지는 반면, 활물질–전해질 접촉점 압력은 크게 낮아집니다.')
CAP = ('【 고체전해질 영률별 2 µm 복합양극 해석 결과 (유효 이온전도도: ', f' = {SIGMA0:g} mS/cm 기준) 】')
I_, SUB, SUP = {'i': '1'}, {'baseline': '-25000'}, {'baseline': '30000'}
ROWS = [
    ([('고체전해질 영률', {})], [(f'{g} GPa', {}) for g in gtxt]),
    ([('기공도 (%)', {})], cellv['por']),
    ([('활물질 표면 피복률 (%)', {})], cellv['cov']),
    ([('유효 이온전도도 ', {}), ('σ', I_), ('eff', SUB), (' (mS cm', {}), ('−1', SUP), (')', {})], cellv['sig']),
    ([('활물질 응력 ', {}), ('σ', I_), ('VM', SUB), (' ÷ 끝 판 압력 (중앙값, 벽 접촉 입자 제외)', {})], cellv['svm']),
    ([('가압 하중 중 활물질–활물질 몫 (%)', {})], cellv['amam']),
    ([('활물질–전해질 접촉점 압력 (평균, MPa)', {})], cellv['cp']),
    ([('끝 판 압력 (MPa)', {})], cellv['pend']),
]

# ── 장 복제 (결론 장 → 손익분기 장 뒤) ─────────────────────────────
p0 = Presentation(a.src)
n0 = len(p0.slides)


def head(sl):
    return ''.join(''.join(r.text for r in sh.text_frame.paragraphs[0].runs) for sh in sl.shapes
                   if sh.name == 'Rectangle 23' and sh.has_text_frame and sh.text_frame.paragraphs)


i_be = [i for i, sl in enumerate(p0.slides) if '손익분기' in head(sl)]
i_co = [i for i, sl in enumerate(p0.slides) if 'DEM 해석 결론' in head(sl)]
i_ap = [i for i, sl in enumerate(p0.slides) if '부록' in head(sl)]
assert len(i_be) == 1 and len(i_co) == 1 and len(i_ap) == 1 and i_co[0] == i_be[0] + 1, (i_be, i_co, i_ap)
assert not any('영률' in head(sl) for sl in p0.slides), '영률 장이 이미 있다'
i_be, i_co, i_ap = i_be[0], i_co[0], i_ap[0]
part = lambda k: p0.slides[k].part.partname.split('/')[-1]
tmp = a.dst + '.dup.pptx'
subprocess.run([sys.executable, str(Path(a.skill) / 'scripts/add_slide.py'), a.src, part(i_co), '--after', part(i_be), '-o', tmp],
               check=True, capture_output=True)
prs = Presentation(tmp)
S = prs.slides
assert len(S) == n0 + 1, (len(S), n0)
s = S[i_be + 1]
assert head(s) == head(S[i_co + 1]) and 'DEM 해석 결론' in head(s), head(s)


def shape(sl, name):
    hit = [sh for sh in sl.shapes if sh.name == name]
    assert len(hit) == 1, (name, len(hit))
    return hit[0]


def put_runs(p, segs, tmpl):
    """문단 p 의 run 을 segs [(글, 속성)] 로 바꾼다 — rPr = tmpl 사본 (i · baseline 만 바꿈)."""
    for r in p.findall(A('r')):
        p.remove(r)
    end = p.find(A('endParaRPr'))
    for text, attrs in segs:
        r = etree.Element(A('r'))
        rp = copy.deepcopy(tmpl)
        for k in ('i', 'baseline'):
            rp.attrib.pop(k, None)
        for k, v in attrs.items():
            rp.set(k, v)
        r.append(rp)
        etree.SubElement(r, A('t')).text = text
        (end.addprevious(r) if end is not None else p.append(r))


# ── 머리 글 · 글머리 (결론 장 꼴 · 셋째 · 넷째 문단 지움) ──────────────
rect = shape(s, 'Rectangle 23')
P = rect.text_frame.paragraphs
assert len(P) == 4 and len(P[0].runs) == 1 and len(P[1].runs) == 1, [len(p.runs) for p in P]
P[0].runs[0].text = HEAD
P[1].runs[0].text = BULLET
c = P[1].runs[0]._r.find(A('rPr')).find(A('solidFill') + '/' + A('srgbClr'))
assert c is None or c.get('val') != 'FF5050'
txb = rect.text_frame._txBody
for p in txb.findall(A('p'))[2:]:
    txb.remove(p)
rect.height = Inches(1.25)

# ── 표 (결론 장 결과 표 꼴 12 pt · 2 열 → 4 열 · 5 줄 → 8 줄) ─────────
fr = shape(s, '결과 요약 표')
fr.name = '영률 비교 표'
tbl = fr._element.find('.//' + A('tbl'))
grid = tbl.find(A('tblGrid'))
gc = grid.findall(A('gridCol'))
trs = tbl.findall(A('tr'))
assert len(gc) == 2 and len(trs) == 5
W_LAB, W_VAL = 5.0, 1.3                                       # in · 합 8.9 = 결론 장 표 폭
assert abs(int(fr.width) - Inches(W_LAB + 3 * W_VAL)) < 10, fr.width
gc[0].set('w', str(Inches(W_LAB)))
gc[1].set('w', str(Inches(W_VAL)))
for _ in range(2):
    grid.append(copy.deepcopy(gc[1]))
for tr in trs:
    tcs = tr.findall(A('tc'))
    assert len(tcs) == 2
    for _ in range(2):
        tr.append(copy.deepcopy(tcs[1]))
for tr in trs[2:]:
    tbl.remove(tr)
for _ in range(len(ROWS) - 2):
    tbl.append(copy.deepcopy(trs[1]))
trs = tbl.findall(A('tr'))
assert len(trs) == len(ROWS)
for tr, (label_segs, vals) in zip(trs, ROWS):
    tcs = tr.findall(A('tc'))
    for k, tc in enumerate(tcs):
        body = tc.find(A('txBody'))
        ps = body.findall(A('p'))
        for extra in ps[1:]:
            body.remove(extra)
        tmpl = ps[0].find(A('r')).find(A('rPr'))
        if k == 0:
            segs = label_segs
        else:
            v = vals[k - 1]
            segs = [v] if isinstance(v, tuple) else [(v, {})]
        put_runs(ps[0], segs, tmpl)
row_h = int(trs[0].get('h'))
fr.top = Inches(2.75)                                         # 글머리가 두 줄이 돼도 겹치지 않게 · 표 끝 6.11 in < 캡션 6.45 in
fr.height = row_h * len(trs)

# ── 캡션 (부록 장 캡션 꼴 · σ0 = 이탤릭 σ + 아래첨자 0) ────────────────
cap_src = shape(S[i_ap + 1], 'Text Box 36')
el = copy.deepcopy(cap_src._element)
ids = [int(x.get('id')) for x in s.shapes._spTree.iter(qn('p:cNvPr'))]
el.find('.//' + qn('p:cNvPr')).set('id', str(max(ids) + 1))
s.shapes._spTree.append(el)
cap = s.shapes[-1]
cp_ = cap.text_frame.paragraphs[0]
runs = cp_.runs
k = [i for i, r in enumerate(runs) if r.text == 'σ'][0]
assert runs[k + 1].text == '0', [r.text for r in runs]
runs[0].text = CAP[0]
for r in runs[1:k]:
    cp_._p.remove(r._r)
runs = cp_.runs
k = [i for i, r in enumerate(runs) if r.text == 'σ'][0]
runs[k + 2].text = CAP[1]
for r in runs[k + 3:]:
    cp_._p.remove(r._r)
assert cap.text_frame.text == CAP[0] + 'σ0' + CAP[1], cap.text_frame.text

# ── 노트 (복제 장 = 빈 노트 → 결론 장 노트 첫 run 꼴로 한 문단) ─────────
tf = s.notes_slide.notes_text_frame
tmpl = [p for p in S[i_co + 1].notes_slide.notes_text_frame.paragraphs if p.runs][0].runs[0]._r.find(A('rPr'))
ps = tf._txBody.findall(A('p'))
target = ps[0]
for r in target.findall(A('r')):
    target.remove(r)
r = etree.Element(A('r'))
r.append(copy.deepcopy(tmpl) if tmpl is not None else etree.Element(A('rPr'), lang='ko-KR'))
etree.SubElement(r, A('t')).text = NOTE
end = target.find(A('endParaRPr'))
(end.addprevious(r) if end is not None else target.append(r))
for p in ps[1:]:
    tf._txBody.remove(p)

prs.save(a.dst)
Path(tmp).unlink()
print(f'{n0} → {len(S)} 장 · {i_be + 2}장 영률 · 침대 기록 {have}')
for (lab, vals) in ROWS[1:]:
    print('  ', ''.join(t for t, _ in lab), '|', ' | '.join(vals))
