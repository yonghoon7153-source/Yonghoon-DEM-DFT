"""덱 꾸러미 정리 — 회의 덱 원본에서 따라온 흔적 빼기 (화면 · 노트 · 그림 내용은 그대로).
  항상: 꾸러미 미리보기 그림 (회의 덱 표지) · 장마다 쓰지 않는 관계 (지운 그림의 연결 — 예: 3장 합친 접촉 모델 그림) · 공동 편집 변경 이력 (changesInfo — 다른 사람 이름 · 원본 편집 이력) · revisionInfo
  --repo (리포 · Codex 사본): + 내장 글꼴 (KoPub · Book Antiqua · 맑은 고딕 부분 글꼴) · SharePoint customXml
usage: python3 -I clean_pkg.py in.pptx out.pptx [--repo]
"""
import re
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

SRC, DST = sys.argv[1:3]
REPO = '--repo' in sys.argv[3:]
prs = Presentation(SRC)
log = []
RID_ATTRS = (qn('r:embed'), qn('r:link'), qn('r:id'), qn('r:pict'))
for n, s in enumerate(prs.slides, 1):
    used = {v for el in s._element.iter() for a in RID_ATTRS for v in [el.get(a)] if v}
    for rid, rel in list(s.part.rels.items()):
        if rel.reltype.endswith(('/image', '/hdphoto')) and rid not in used:
            tgt = rel.target_part.partname
            s.part.drop_rel(rid)
            log.append(f'{n}장 안 쓰는 그림 연결 {rid} → {tgt}')
pp = prs.part
drop_types = ['/changesInfo', '/revisionInfo'] + (['/font', '/customXml'] if REPO else [])
for rid, rel in list(pp.rels.items()):
    if any(rel.reltype.endswith(t) for t in drop_types):
        log.append(f'꾸러미: {rel.reltype.rsplit("/", 1)[-1]} {rel.target_ref}')
        pp.rels.pop(rid) if hasattr(pp.rels, 'pop') else pp.drop_rel(rid)
pkg = prs.part.package                              # 꾸러미 미리보기 (docProps/thumbnail) = 회의 덱 표지 (로고 · 과제명 · 사람 이름) — 늘 뺀다
for rid, rel in list(pkg._rels.items()):
    if rel.reltype.endswith('/thumbnail'):
        log.append(f'꾸러미: 미리보기 그림 {rel.target_ref}')
        pkg._rels.pop(rid)
if REPO:
    pres = prs.part._element
    efl = pres.find(qn('p:embeddedFontLst'))
    if efl is not None:
        pres.remove(efl)
    for att in ('embedTrueTypeFonts', 'saveSubsetFonts'):
        pres.attrib.pop(att, None)
    log.append('p:embeddedFontLst 뺌')
prs.save(DST)
print('\n'.join(log))
