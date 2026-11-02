"""9장 향후 계획 뺌 (1저자 11-02 — *"이게 마지막 연차라서 향후 계획 이런건 안들어가도돼"*).
  - 머리 글 'DEM 해석 결론 및 향후 계획' → 'DEM 해석 결론'
  - '향후 계획 표' (같은 자리 · 같은 꼴 2 열 × 5 줄) → '결과 요약 표' — 입도별 핵심 결과 (3 µm → 2 µm → 1 µm) · 값 = values/values_D123.csv 그대로 (옮김뿐)
  - 노트: 다음 단계 · 향후 문장 뺌 · '접촉 상태도 다음 과제입니다' → '몰려 있습니다' · 표 설명 한 줄
usage: python3 -I drop_future_s9.py in.pptx out.pptx values_D123.csv
"""
import csv
import sys

from pptx import Presentation

SRC, DST, VAL = sys.argv[1:4]
rows = {r['항목']: r for r in csv.DictReader(open(VAL, encoding='utf-8'))}
B = ('3 µm (D3)', '2 µm (D2)', '1 µm (D1)')


def vals(key, fmt):
    r = rows[key]
    return ' → '.join(fmt(float(r[b])) for b in B)


por = vals('기공도 (정확 합집합)', lambda x: f'{x:.1f}')
cn = vals('CN AM–SE (NCM 1개당 SE 접촉 수)', lambda x: f'{x:.1f}')
tau = vals('수송 tortuosity', lambda x: f'{x:.1f}')
sig = vals('유효 이온전도도 σ_Li+ (σ₀ = 1.5 mS/cm)', lambda x: f'{x:.3f}')
TABLE = [
    [[('입도별 결과', 'n')], [('3 µm → 2 µm → 1 µm', 'n')]],
    [[('기공도', 'n')], [(por + ' %', 'n')]],
    [[('활물질 1개당 전해질 접촉 수', 'n')], [(cn, 'n')]],
    [[('tortuosity', 'n')], [(tau, 'n')]],
    [[('유효 이온전도도', 'n')], [(sig + ' mS cm', 'n'), ('−1', 'sup')]],
]

prs = Presentation(SRC)
s = prs.slides[8]
box = [x for x in s.shapes if x.name == 'Rectangle 23']
tbl = [x for x in s.shapes if x.name == '향후 계획 표']
if len(box) != 1 or len(tbl) != 1:
    raise SystemExit(f'9장 상자 {len(box)} · 표 {len(tbl)} (둘 다 1 이어야 한다)')
head = [r for r in box[0].text_frame.paragraphs[0].runs if '및 향후 계획' in r.text]
if len(head) != 1:
    raise SystemExit('9장 머리 글 못 찾음')
head[0].text = head[0].text.replace(' 및 향후 계획', '')
t = tbl[0].table
if len(t.rows) != 5 or len(t.columns) != 2:
    raise SystemExit(f'표 꼴 {len(t.rows)} × {len(t.columns)} (5 × 2 이어야 한다)')
for ri, row in enumerate(TABLE):
    for ci, segs in enumerate(row):
        p = t.cell(ri, ci).text_frame.paragraphs[0]
        runs = p.runs
        base = runs[0]._r.get_or_add_rPr()
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        runs[0].text = segs[0][0]
        for text, kind in segs[1:]:
            nr = p.add_run()
            nr.text = text
            nr._r.insert(0, __import__('copy').deepcopy(base))
            if kind == 'sup':
                nr._r.get_or_add_rPr().set('baseline', '30000')
tbl[0].name = '결과 요약 표'
notes = [p for p in s.notes_slide.notes_text_frame.paragraphs if p.runs][0]
full = ''.join(r.text for r in notes.runs)
cuts = [' 다음 단계는 입도별 반복 계산, 2 µm 펠릿 측정, 그리고 이 구조로 3차원 전기화학 시뮬레이션입니다.',
        ' 향후에는 입도별 반복 계산 (압축·언로딩 절차 갱신 포함), 2 µm 펠릿 이온전도도 측정, DEM 구조 기반 3차원 전기화학 시뮬레이션, MPM 소성 변형 기반 피복률 비교를 진행합니다.']
for c in cuts:
    if c not in full:
        raise SystemExit(f'9장 노트 문장 못 찾음: {c[:30]}')
    full = full.replace(c, '')
old = '몰려 있어 접촉 상태도 다음 과제입니다.'
if old not in full:
    raise SystemExit('9장 노트 접촉 문장 못 찾음')
full = full.replace(old, '몰려 있습니다.').rstrip() + ' 아래 표는 입도별 핵심 결과를 3 µm, 2 µm, 1 µm 순서로 모은 것입니다.'
for r in notes.runs[1:]:
    r._r.getparent().remove(r._r)
notes.runs[0].text = full
prs.save(DST)
print('9장: 머리 글 · 결과 요약 표 ·', ' | '.join([por, cn, tau, sig]))
print('노트:', full)
