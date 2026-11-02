"""새 6장 = MPM 소성 해석 — 기공 · 활물질 표면 피복 (3, 2, 1 µm) (1저자 11-02 Q3 · Q4 *"다 권고대로"*).
  4장 (기공도 · 그림 셋 + 막대) 을 5장 뒤로 복제 → 그림 · 라벨을 지우고:
   - 왼쪽 셋 = MPM 기공 그림 (4장 기공 3D 와 같은 자리 · 크기) · 오른쪽 셋 = MPM 활물질 표면 피복 그림 (같은 크기)
   - 묶음 이름 두 줄 (MPM 기공 · MPM 활물질 표면 피복) · 입도 라벨 (3 · 2 · 1 µm) · 기공 그림 아래 MPM 기공도 (값 = 리포 묶음 그대로)
   - 글머리 · 캡션 · 노트.  피복률 숫자는 넣지 않는다 (Q4 · 정의가 띠 = 5장 DEM 피복률과 뜻이 다름 · 원장 MPMC-01 – 03)
  그림 = figs/mpm/ (1저자 웹앱 Screenshot · alpha 로 자름 · MANIFEST.json) · 기공도 = docs/data/kg50_mpm_20261102/kg50_mpm_results_slim.tgz 의 mpm_metrics.json
usage: python3 put_mpm_s6.py in.pptx out.pptx FIGDIR SKILL_DIR <repo>
  (add_slide.py = pptx 기술의 장 복제 도구 — 그 폴더의 office 모듈을 쓰므로 -I 없이 부른다)
"""
import copy
import json
import subprocess
import sys
import tarfile
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches

SRC, DST, FIG, SKILL, REPO = sys.argv[1:6]
FIG, REPO = Path(FIG), Path(REPO)
A = lambda t: qn('a:' + t)
E = 914400
BEDS = ('3', '2', '1')
KIT = {'261102_091413_c2e9a7': '3', '261102_091440_0845a7': '2', '261102_091500_598f38': '1'}

# ── 값 (리포 묶음 그대로) ─────────────────────────────────────────
por = {}
with tarfile.open(REPO / 'docs/data/kg50_mpm_20261102/kg50_mpm_results_slim.tgz', 'r:gz') as tf:
    for m in tf.getmembers():
        if m.isfile() and m.name.endswith('/latest_run/mpm_metrics.json'):
            kit = m.name.split('/')[0]
            met = json.load(tf.extractfile(m))
            assert met['porosity_at_target_pct'] is not None, kit          # None = 목표 미도달 (CLAUDE.md DO-NOT)
            por[KIT[kit]] = met['porosity_at_target_pct']
assert set(por) == set(BEDS), por
ptxt = {b: f'{por[b]:.1f}' for b in BEDS}

# ── 장 복제 (4장 → 5장 뒤) ─────────────────────────────────────────
p0 = Presentation(SRC)
n0 = len(p0.slides)
part = lambda k: p0.slides[k].part.partname.split('/')[-1]
tmp = DST + '.dup.pptx'
subprocess.run([sys.executable, str(Path(SKILL) / 'scripts/add_slide.py'), SRC, part(3), '--after', part(4), '-o', tmp],
               check=True, capture_output=True)
prs = Presentation(tmp)
S = prs.slides
assert len(S) == n0 + 1, (len(S), n0)
s = S[5]


def shape(sl, name):
    hit = [sh for sh in sl.shapes if sh.name == name]
    assert len(hit) == 1, (name, len(hit))
    return hit[0]


rect = shape(s, 'Rectangle 23')
assert '기공도 변화' in rect.text_frame.paragraphs[0].runs[0].text, '복제한 장이 4장이 아니다'
label_tmpl = copy.deepcopy(shape(s, '3D 라벨 3 µm')._element)
for sh in list(s.shapes):
    if sh.shape_type == 13 or sh.name.startswith('3D 라벨'):            # 13 = 그림
        sh._element.getparent().remove(sh._element)
assert sorted(sh.name for sh in s.shapes) == ['Rectangle 23', 'Text Box 36', 'TextBox 1'], [sh.name for sh in s.shapes]

# ── 글머리 (4장 세 문단 꼴 그대로 · run 글만 바꿈) ─────────────────
P = rect.text_frame.paragraphs
assert len(P) == 3 and len(P[0].runs) == 1 and len(P[1].runs) == 1 and len(P[2].runs) == 3, [len(p.runs) for p in P]
P[0].runs[0].text = '  MPM 소성 해석: 기공 · 활물질 표면 피복 (3, 2, 1 µm)'
P[1].runs[0].text = 'DEM 구조에서 활물질 고정, 전해질만 소성 변형체로 300 MPa 재가압'
P[2].runs[1].text = 'MPM 기공도'
P[2].runs[2].text = f' {ptxt["3"]} → {ptxt["2"]} → {ptxt["1"]} %, DEM과 같은 입도 순서'

cap = shape(s, 'Text Box 36').text_frame.paragraphs[0]
assert len(cap.runs) == 1
cap.runs[0].text = '【 MPM 소성 해석 후 전해질 입도별 기공 및 활물질 표면 피복 】'


# ── 그림 · 라벨 (4장 기공 3D 자리 = x 0.55 · 2.02 · 3.49 · y 3.17 · 1.37 × 2.37 in) ──
def label(name, text, x, y, w):
    el = copy.deepcopy(label_tmpl)
    s.shapes._spTree.append(el)
    sh = s.shapes[-1]
    sh.name = name
    sh.left, sh.top, sh.width = Inches(x), Inches(y), Inches(w)
    r = sh.text_frame.paragraphs[0].runs
    assert len(r) == 1
    r[0].text = text
    return sh


SLOT_W, SLOT_H, Y0 = 1.37, 2.37, 3.17
XL = (0.55, 2.02, 3.49)
XR = (5.15, 6.62, 8.09)
SIZE = {(stem, b): Image.open(FIG / f'{stem}_{b}um.png').size for stem in ('mpm_pore', 'mpm_cov') for b in BEDS}
H = min([SLOT_H] + [SLOT_W * h / w for (w, h) in SIZE.values()])     # 여섯 그림 같은 높이 · 칸 폭 안
for xs, stem, group in ((XL, 'mpm_pore', 'MPM 기공'), (XR, 'mpm_cov', 'MPM 활물질 표면 피복')):
    label(f'MPM 묶음 이름 {group}', group, xs[0], 2.95, xs[2] + SLOT_W - xs[0])
    for x, b in zip(xs, BEDS):
        png = FIG / f'{stem}_{b}um.png'
        w_px, h_px = SIZE[(stem, b)]
        w = H * w_px / h_px
        assert w <= SLOT_W + 1e-9, (png, w)
        pic = s.shapes.add_picture(str(png), Inches(x + (SLOT_W - w) / 2), Inches(Y0), height=Inches(H))
        pic.name = f'{group} {b} µm'
        label(f'{group} 라벨 {b} µm', f'{b} µm', x, 5.58, SLOT_W)
        if stem == 'mpm_pore':
            label(f'MPM 기공도 {b} µm', f'기공도 {ptxt[b]} %', x, 5.84, SLOT_W)

# ── 노트 (복제 장 = 빈 노트 → 5장 노트 첫 run 의 꼴로 한 문단) ─────────
notes = (f'MPM은 DEM으로 300 MPa까지 누른 구조에서 활물질 위치를 그대로 두고, 전해질만 소성 변형하는 연속체로 바꿔 다시 300 MPa까지 누른 결과입니다. '
         f'기공도는 3 µm {ptxt["3"]} %, 2 µm {ptxt["2"]} %, 1 µm {ptxt["1"]} %로 DEM과 같은 입도 순서이고, 전해질이 소성 변형으로 빈 곳을 조금 더 채워 DEM보다 약간 낮습니다. '
         '피복 그림의 색 점은 변형된 전해질이 맞닿거나 바로 곁에 있는 활물질 표면입니다.')
tf = s.notes_slide.notes_text_frame
tmpl = [p for p in S[4].notes_slide.notes_text_frame.paragraphs if p.runs][0].runs[0]._r.find(A('rPr'))
ps = tf._txBody.findall(A('p'))
target = ps[0]
for r in target.findall(A('r')):
    target.remove(r)
r = etree.Element(A('r'))
r.append(copy.deepcopy(tmpl) if tmpl is not None else etree.Element(A('rPr'), lang='ko-KR'))
etree.SubElement(r, A('t')).text = notes
end = target.find(A('endParaRPr'))
(end.addprevious(r) if end is not None else target.append(r))
for p in ps[1:]:
    tf._txBody.remove(p)

prs.save(DST)
Path(tmp).unlink()
print(f'{n0} → {len(S)} 장 · 6장 MPM · 기공도 ' + ' · '.join(f'{b} µm {ptxt[b]} %' for b in BEDS))
