"""진도점검 덱 이야기 보강 (1저자 11-02 "story로도 잘 넣어봐요" → 권고 A · "다 권고대로" · σzz = 부록 표만 "%로 넣자").
  8 장 → 10 장:
   6장 (새 · 5장 복제)  전해질 접촉 망 — 배위수 (SE–SE · AM–AM) + 전해질 망에서 끊긴 입자 비율
   7장 (옛 6)           유효 이온전도도 (σ0 1.5 기준 절대값) + 이온 전류 3D 자리 셋 (1저자 웹앱 캡처) · 71–74 %
   8장 (옛 7)           왼쪽 = 1 µm ÷ 3 µm 구조 × pellet = 곱 막대 · 노트 LPSC 메모 뺌
   9장 (옛 8)           향후 계획 표 (글머리 '→ 향후' 두 줄 → 표)
   10장 (새 · 1장 복제) 부록 — 해석 조건 표 + 입도별 지표 표 (가압 응력 기여 % 포함)
usage: python3 build_story_u7.py in.pptx out.pptx FIGDIR SLOT_SRC.pptx SKILL_DIR <repo>
  in = 사슬 ⑭ 결과 (4장 기공 그림 뒤) · SLOT_SRC = ⑬ 결과 (4장 점선 자리 셋이 남은 판 — 자리 도형만 복사) · 값 = values_D123 의 원천과 같음
  (add_slide.py = pptx 기술의 장 복제 도구 — 그 폴더의 office 모듈을 쓰므로 -I 없이 부른다)
"""
import copy
import csv
import json
import subprocess
import sys
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches

SRC, DST, FIG, SLOT_SRC, SKILL, REPO = sys.argv[1:7]
FIG, REPO = Path(FIG), Path(REPO)
A = lambda t: qn('a:' + t)
BLUE = '0070C0'
IN_ = 914400

# ── 값 (원천 그대로) ─────────────────────────────────────────────
D2 = REPO / 'docs/50kg/report_y4/draft2'
rows = {r['bed']: r for r in csv.DictReader(open(D2 / 'metrics_all.csv', encoding='utf-8'))}
PL = json.loads((REPO / 'docs/50kg/report_y4/meeting_20261104/values/szz_share/plane_load.json').read_text(encoding='utf-8'))
ORDER, LBL = ('D3', 'D2', 'D1'), {'D3': 'SE3um', 'D2': 'SE2um', 'D1': 'SE1um'}
v = lambda b, k: float(rows[b][k])
f = lambda xs, nd: [f'{x:.{nd}f}' for x in xs]
cn_se = f([v(b, 'se_se_cn_mean') for b in ORDER], 1)
cn_am = f([v(b, 'am_am_cn_mean') for b in ORDER], 1)
disc = f([100 - v(b, 'percolation_pct') for b in ORDER], 1)
sig = f([1.5 * v(b, 'f_ion_hertz') for b in ORDER], 3)
frel = f([v(b, 'f_ion_hertz') / v('D3', 'f_ion_hertz') for b in ORDER], 1)
tau = f([v(b, 'tau2_ion_hertz') for b in ORDER], 1)
cps = [100 * v(b, 'constriction_power_share_ion_hertz') for b in ORDER]
szz = {g: f([PL['cases'][LBL[b]]['contribution_sigma_zz_pct'][g] for b in ORDER], 1) for g in ('AM–AM', 'AM–SE', 'SE–SE')}

# ── 장 복제 (5장 → 6장 · 1장 → 맨 끝) ─────────────────────────────
p0 = Presentation(SRC)
part = lambda k: p0.slides[k].part.partname.split('/')[-1]
s5, s1, sl = part(4), part(0), part(len(p0.slides) - 1)
tmp1, tmp2 = DST + '.dup1.pptx', DST + '.dup2.pptx'
add = str(Path(SKILL) / 'scripts/add_slide.py')
subprocess.run([sys.executable, add, SRC, s5, '--after', s5, '-o', tmp1], check=True, capture_output=True)
subprocess.run([sys.executable, add, tmp1, s1, '--after', sl, '-o', tmp2], check=True, capture_output=True)
prs = Presentation(tmp2)
S = prs.slides
assert len(S) == 10, len(S)
Path(tmp1).unlink()


def shape(s, name):
    hit = [sh for sh in s.shapes if sh.name == name]
    assert len(hit) == 1, (name, len(hit))
    return hit[0]


def set_fill(rpr, hexval):
    for el in rpr.findall(A('solidFill')):
        rpr.remove(el)
    sf = etree.Element(A('solidFill'))
    etree.SubElement(sf, A('srgbClr')).set('val', hexval)
    first = rpr.find(A('ln'))
    (first.addnext(sf) if first is not None else rpr.insert(0, sf))


def rewrite(p, segs, base=None):
    """p 의 run 을 segs [(글, 꼴)] 로 다시 — 꼴 n · blue · i · sub · sup · b.  base = 바탕 rPr (없으면 p 의 첫 run)."""
    old = p._p.findall(A('r'))
    if base is None:
        base = old[0].find(A('rPr')) if old else None
    base = copy.deepcopy(base) if base is not None else etree.Element(A('rPr'), lang='ko-KR')
    for el in base.findall(A('solidFill')):
        if el.find(A('srgbClr')) is not None and el.find(A('srgbClr')).get('val') == BLUE:
            base.remove(el)
    for el in ('i', 'baseline'):
        base.attrib.pop(el, None)
    for r in old:
        p._p.remove(r)
    end = p._p.find(A('endParaRPr'))
    for text, kind in segs:
        r = etree.Element(A('r'))
        rpr = copy.deepcopy(base)
        if kind == 'blue':
            set_fill(rpr, BLUE)
        if kind == 'i':
            rpr.set('i', '1')
        if kind == 'sub':
            rpr.set('baseline', '-25000')
        if kind == 'sup':
            rpr.set('baseline', '30000')
        r.append(rpr)
        etree.SubElement(r, A('t')).text = text
        (end.addprevious(r) if end is not None else p._p.append(r))


def drop_pars(tf, keep):
    ps = tf._txBody.findall(A('p'))
    for k, p in enumerate(ps):
        if k not in keep:
            tf._txBody.remove(p)


def set_notes(s, text):
    """노트 = 한 문단.  복제 장 (add_slide) 은 노트가 비어 있다 → 5장 노트 첫 run 의 꼴로 새 run."""
    tf = s.notes_slide.notes_text_frame
    ps = [p for p in tf.paragraphs if p.runs]
    if ps:
        rewrite(ps[0], [(text, 'n')])
        target = ps[0]._p
    else:
        tmpl = [p for p in S[4].notes_slide.notes_text_frame.paragraphs if p.runs][0].runs[0]._r.find(A('rPr'))
        target = tf._txBody.findall(A('p'))[0]
        r = etree.Element(A('r'))
        r.append(copy.deepcopy(tmpl) if tmpl is not None else etree.Element(A('rPr'), lang='ko-KR'))
        etree.SubElement(r, A('t')).text = text
        end = target.find(A('endParaRPr'))
        (end.addprevious(r) if end is not None else target.append(r))
    for p in tf._txBody.findall(A('p')):
        if p is not target:
            tf._txBody.remove(p)


def replace_pic(s, name, png):
    sh = shape(s, name)
    x, y, w, h = sh.left, sh.top, sh.width, sh.height
    sh._element.getparent().remove(sh._element)
    pic = s.shapes.add_picture(str(png), x, y, width=w, height=h)
    pic.name = name
    return pic


def first_rpr(sh):
    return copy.deepcopy(sh.text_frame.paragraphs[0].runs[0]._r.find(A('rPr')))


# ── 표 (1장 'Table 4' 꼴을 복사해 칸 · 줄을 다시) ───────────────────
TBL_SRC = copy.deepcopy(shape(S[9], 'Table 4')._element)        # 10장 = 1장 복제 (아직 손대지 않음)


def make_table(s, name, x, y, colw_in, rows_txt, rowh_in, sz):
    gf = copy.deepcopy(TBL_SRC)
    tbl = gf.find('.//' + A('tbl'))
    grid = tbl.find(A('tblGrid'))
    trs = tbl.findall(A('tr'))
    head_tc, body_tc = trs[0].findall(A('tc'))[0], trs[1].findall(A('tc'))[1]   # 머리 칸 · 값 칸 꼴
    lab_tc = trs[1].findall(A('tc'))[0]                                          # 값 줄의 첫 칸 (항목) 꼴
    for g in list(grid):
        grid.remove(g)
    for w in colw_in:
        etree.SubElement(grid, A('gridCol')).set('w', str(int(w * IN_)))
    for tr in trs:
        tbl.remove(tr)
    for ri, cells in enumerate(rows_txt):
        tr = etree.SubElement(tbl, A('tr'))
        tr.set('h', str(int(rowh_in * IN_)))
        for ci, segs in enumerate(cells):
            tc = copy.deepcopy(head_tc if ri == 0 else (lab_tc if ci == 0 else body_tc))
            p = tc.find('.//' + A('p'))
            if ci == 0 and ri > 0:
                ppr = p.find(A('pPr'))
                if ppr is not None:
                    ppr.set('algn', 'l')
            base = copy.deepcopy(p.find(A('r')).find(A('rPr')))
            base.set('sz', str(sz))
            for r in p.findall(A('r')):
                p.remove(r)
            for text, kind in (segs if isinstance(segs, list) else [(segs, 'n')]):
                r = etree.SubElement(p, A('r'))
                rpr = copy.deepcopy(base)
                if kind == 'i':
                    rpr.set('i', '1')
                if kind == 'sub':
                    rpr.set('baseline', '-25000')
                if kind == 'sup':
                    rpr.set('baseline', '30000')
                r.append(rpr)
                etree.SubElement(r, A('t')).text = text
            tr.append(tc)
    xfrm = gf.find(qn('p:xfrm'))
    xfrm.find(A('off')).set('x', str(int(x * IN_)))
    xfrm.find(A('off')).set('y', str(int(y * IN_)))
    xfrm.find(A('ext')).set('cx', str(int(sum(colw_in) * IN_)))
    xfrm.find(A('ext')).set('cy', str(int(rowh_in * len(rows_txt) * IN_)))
    nv = gf.find(qn('p:nvGraphicFramePr')).find(qn('p:cNvPr'))
    nv.set('name', name)
    nv.set('id', str(900 + len(list(s.shapes._spTree))))
    s.shapes._spTree.append(gf)


log = []
# ── 6장 (새) — 전해질 접촉 망 ───────────────────────────────────
s6 = S[5]
P = shape(s6, 'Rectangle 23').text_frame.paragraphs
rewrite(P[0], [('  고체전해질 미립화에 따른 전해질 접촉 망', 'n')])
rewrite(P[1], [('입자 1개당 접촉 수 (배위수) 및 전해질 망 연결 분석', 'n')])
rewrite(P[2], [('   → ', 'n'), ('전해질 미립화', 'blue'), (f'에 따라 전해질–전해질 배위수 증가 ({cn_se[0]} → {cn_se[1]} → {cn_se[2]})', 'n')])
rewrite(P[3], [(f'   → 전해질 망에서 끊긴 입자 감소 ({disc[0]} → {disc[1]} → {disc[2]} %) → ', 'n'), ('촘촘한 전해질 망', 'blue')])
replace_pic(s6, 'Picture 3', FIG / 's6_cn_network.png')
replace_pic(s6, 'Picture 4', FIG / 's6_disconnected.png')
cap = shape(s6, 'Text Box 36')
rewrite(cap.text_frame.paragraphs[0], [('【 전해질 입도별 배위수 및 전해질 망에서 끊긴 입자 비율 】', 'n')])
set_notes(s6, f'작은 전해질일수록 전해질 하나가 닿는 전해질 수가 {cn_se[0]}, {cn_se[1]}, {cn_se[2]}개로 늘고, 활물질끼리 닿는 수는 '
              f'{cn_am[0]}, {cn_am[1]}, {cn_am[2]}개로 줄어듭니다. 위아래로 이어진 전해질 망에 들지 않은 입자도 {disc[0]}, {disc[1]}, {disc[2]} %로 '
              f'줄어, 작은 전해질이 활물질 사이로 들어가 전해질 망을 촘촘하게 만드는 방향과 맞습니다.')
log.append('6장 새: 배위수 · 끊긴 입자')

# ── 7장 (옛 6) — 유효 이온전도도 + 이온 전류 3D 자리 ─────────────────
s7 = S[6]
R7 = shape(s7, 'Rectangle 23')
P = R7.text_frame.paragraphs
rewrite(P[0], [('  고체전해질 미립화에 따른 유효 이온전도도 및 이온 전류 분포', 'n')])
rewrite(P[1], [('전해질 물성 동일 가정 (', 'n'), ('σ', 'i'), ('0', 'sub'), (' = 1.5 mS/cm) 하 유효 이온전도도 및 이온 전류 분포 분석', 'n')])
rewrite(P[2], [('   → ', 'n'), ('전해질 미립화', 'blue'),
               (f'에 따라 유효 이온전도도 {frel[1]}배 (2 µm), {frel[2]}배 (1 µm)', 'n')])
rewrite(P[3], [(f'   → tortuosity 감소 ({tau[0]} → {tau[1]} → {tau[2]}), 이온 전달 저항의 {min(cps):.0f}–{max(cps):.0f} %가 전해질 접촉부', 'n')])
pic = shape(s7, 'Picture 3')
pic._element.getparent().remove(pic._element)
slot_src = Presentation(SLOT_SRC).slides[3]
for k in ('3', '2', '1'):
    for nm in (f'3D 그림 자리 (웹앱) {k} µm', f'3D 라벨 {k} µm'):
        el = copy.deepcopy(shape(slot_src, nm)._element)
        for t in el.iter(A('t')):
            if t.text == '기공 보기':
                t.text = '이온 전류 보기'
        s7.shapes._spTree.append(el)
replace_pic(s7, 'Picture 4', FIG / 's7_sigma_li.png')
cap = shape(s7, 'Text Box 36')
rewrite(cap.text_frame.paragraphs[0], [('【 전해질 입도별 이온 전류 밀도 분포 및 유효 이온전도도 (', 'n'), ('σ', 'i'), ('0', 'sub'), (' = 1.5 mS/cm) 】', 'n')])
set_notes(s7, f'전해질 물성을 같게 두고 (σ0 = 1.5 mS/cm) 구조만 비교하면 유효 이온전도도는 3 µm {sig[0]}, 2 µm {sig[1]}, 1 µm {sig[2]} mS/cm로 '
              f'{frel[1]}배, {frel[2]}배가 됩니다. 같은 계산에서 tortuosity는 {tau[0]}, {tau[1]}, {tau[2]}으로 줄고, 이온 전달 저항의 '
              f'{min(cps):.0f}–{max(cps):.0f} %가 전해질끼리 맞닿은 접촉부에 있습니다. tortuosity는 전해질 부피 분율을 정규화 유효 이온전도도로 '
              f'나눈 값이고, 경로 길이의 비가 아닙니다. 3D 그림은 같은 계산의 이온 전류 밀도 분포입니다.')
log.append('7장: σ_Li+ 막대 · 3D 자리 셋 · 71–74 %')

# ── 8장 (옛 7) — 곱 막대 · 노트 LPSC 메모 뺌 ─────────────────────────
s8 = S[7]
replace_pic(s8, 'Picture 3', FIG / 's8_net.png')
cap = shape(s8, 'Text Box 36')
rewrite(cap.text_frame.paragraphs[0], [('【 1 µm ÷ 3 µm 이온전도도 비 (구조 × 전해질) 및 3 µm 전극과 같아지는 전해질 이온전도도 (◆ 실측) 】', 'n')])
ntf = s8.notes_slide.notes_text_frame
gone = [p for p in ntf._txBody.findall(A('p')) if '※ 진도점검 회의 자료' in ''.join(t.text or '' for t in p.iter(A('t')))]
assert len(gone) == 1, len(gone)
ntf._txBody.remove(gone[0])
log.append('8장: 곱 막대 · 노트 LPSC 메모 뺌')

# ── 9장 (옛 8) — 향후 계획 표 ─────────────────────────────────────
s9 = S[8]
R9 = shape(s9, 'Rectangle 23')
ps = R9.text_frame._txBody.findall(A('p'))
keep = [k for k, p in enumerate(ps) if not ''.join(t.text or '' for t in p.iter(A('t'))).strip().startswith(('→ 향후', '→ DEM 구조'))]
assert len(keep) == len(ps) - 2, (len(ps), keep)
drop_pars(R9.text_frame, set(keep))
R9.height = Inches(2.25)
make_table(s9, '향후 계획 표', 0.55, 3.60, [3.6, 5.3], [
    ['향후 계획', '내용'],
    ['입도별 반복 계산', '시드 추가 · 압축/언로딩 절차 갱신 (정적 300 MPa 유지 · 하중 제거)'],
    ['2 µm 펠릿 이온전도도 측정', '손익분기 곡선 보완 (3 µm · 1 µm 사이)'],
    ['DEM 구조 기반 3차원 전기화학 시뮬레이션', '입도별 방전 용량 비교'],
    ['MPM 소성 변형 해석', '입도별 활물질 피복률 비교 (DEM ↔ MPM)'],
], 0.42, 1200)
n9 = [p for p in s9.notes_slide.notes_text_frame.paragraphs if p.runs][0]
n9.runs[-1].text = n9.runs[-1].text.rstrip() + (' 향후에는 입도별 반복 계산 (압축·언로딩 절차 갱신 포함), 2 µm 펠릿 이온전도도 측정, DEM 구조 기반 '
                                                '3차원 전기화학 시뮬레이션, MPM 소성 변형 기반 피복률 비교를 진행합니다.')
log.append('9장: 향후 계획 표 (글머리 두 줄 → 표)')

# ── 10장 (새 · 1장 복제) — 부록 ─────────────────────────────────
s10 = S[9]
for sh in list(s10.shapes):
    if sh.name.startswith(('3D 그림', '3D 라벨')) or sh.name == 'Table 4':
        sh._element.getparent().remove(sh._element)
R10 = shape(s10, 'Rectangle 23')
drop_pars(R10.text_frame, {0})
rewrite(R10.text_frame.paragraphs[0], [('  부록: DEM 해석 조건 및 입도별 주요 지표', 'n')])
R10.height = Inches(0.55)
sup = lambda unit: [(unit, 'n'), ('−1', 'sup')]
make_table(s10, '부록 조건 표', 0.55, 1.80, [1.75, 2.30], [
    ['해석 조건', '값'],
    ['복합양극 크기', '50 × 50 µm'],
    ['면적당 용량', [('6.5 mAh cm', 'n'), ('−2', 'sup')]],
    ['가압 압력', '300 MPa'],
    ['NCM 입경 · 함량', '6 µm · 85 wt%'],
    [[('고체전해질 입경 (', 'n'), ('D', 'i'), ('50', 'sub'), (')', 'n')], '3 · 2 · 1 µm'],
    ['입자 수', [('7.7 × 10', 'n'), ('3', 'sup'), (' · 2.2 × 10', 'n'), ('4', 'sup'), (' · 1.7 × 10', 'n'), ('5', 'sup')]],
    ['진밀도 (NCM / SE)', [('4.85 / 1.64 g cm', 'n'), ('−3', 'sup')]],
    ['영률 (NCM / SE)', '140 / 22 GPa (DEM 유효 1.35)'],
    ['푸아송비 (NCM / SE)', '0.25 / 0.3'],
], 0.42, 1000)
make_table(s10, '부록 지표 표', 4.85, 1.80, [2.35, 0.80, 0.80, 0.80], [
    ['입도별 지표', '3 µm', '2 µm', '1 µm'],
    ['porosity (%)'] + f([v(b, 'eps_union_exact_pct') for b in ORDER], 1),
    ['AM coverage (%)'] + f([v(b, 'coverage_physics_union_pct') for b in ORDER], 1),
    ['tortuosity'] + tau,
    ['AM–SE 배위수'] + f([v(b, 'am_se_cn_mean') for b in ORDER], 1),
    ['SE–SE 배위수'] + cn_se,
    ['AM–AM 배위수'] + cn_am,
    ['가압 응력 기여 AM–AM (%)'] + szz['AM–AM'],
    ['가압 응력 기여 AM–SE (%)'] + szz['AM–SE'],
    ['가압 응력 기여 SE–SE (%)'] + szz['SE–SE'],
    [[('유효 이온전도도 (mS cm', 'n'), ('−1', 'sup'), (')', 'n')]] + sig,
    ['정규화 유효 이온전도도'] + frel,
    ['전해질 접촉부 저항 몫 (%)'] + [f'{c:.1f}' for c in cps],
    [[('pellet 이온전도도 (mS cm', 'n'), ('−1', 'sup'), (')', 'n')], '5.1', '—', '2.3'],
], 0.30, 950)
cap = shape(s10, 'Text Box 36')
rewrite(cap.text_frame.paragraphs[0], [('【 DEM 해석 조건 및 전해질 입도별 주요 지표 (유효 이온전도도: ', 'n'), ('σ', 'i'), ('0', 'sub'),
                                       (' = 1.5 mS/cm 기준 · 정규화 = 3 µm 대비) 】', 'n')])
set_notes(s10, '부록입니다. 왼쪽 표는 해석 조건, 오른쪽 표는 입도별 지표입니다. 가압 응력 기여는 높이 방향 단면을 지나는 수직 하중을 '
               '접촉 종류별로 나눈 비율 (21개 단면 평균)입니다.')
log.append('10장 새: 부록 표 둘')

prs.save(DST)
Path(tmp2).unlink()
print('\n'.join(log))
