"""1저자 저장본 (한 장) 의 1장 상태를 8장 덱 1장에 옮긴다 (1저자 11-02 1.pptx).
옮기는 것: 같은 이름 도형의 위치 · 크기 / 글 도형의 txBody 통째 / 표의 a:tbl 통째.  그림 = 위치만 (그림 내용 같은지 sha 확인).
usage: python3 -I sync_slide1.py deck8.pptx user1.pptx out.pptx
"""
import copy
import hashlib
import sys

from pptx import Presentation
from pptx.oxml.ns import qn

A_PATH, B_PATH, OUT = sys.argv[1:4]
A = Presentation(A_PATH)
B = Presentation(B_PATH)
sa, sb = A.slides[0], B.slides[0]
na = {}
for sh in sa.shapes:
    na.setdefault(sh.name, []).append(sh)
nb = {}
for sh in sb.shapes:
    nb.setdefault(sh.name, []).append(sh)
assert all(len(v) == 1 for v in na.values()) and all(len(v) == 1 for v in nb.values()), '이름 겹침'
assert set(na) == set(nb), (set(na) ^ set(nb))
for name, (b,) in nb.items():
    a = na[name][0]
    a.left, a.top, a.width, a.height = b.left, b.top, b.width, b.height
    if b.shape_type == 13:  # picture
        ha = hashlib.sha256(a.image.blob).hexdigest()
        hb = hashlib.sha256(b.image.blob).hexdigest()
        assert ha == hb, f'{name}: 그림 내용 다름'
        continue
    if b.has_text_frame:
        tb = b._element.find(qn('p:txBody'))
        assert tb is not None
        # txBody 안 관계 참조 (그림 글머리표 buBlip 등) = A 쪽 같은 rId 가 같은 그림을 가리킬 때만 허용
        for el in tb.iter():
            for att in (qn('r:embed'), qn('r:id')):
                rid = el.get(att)
                if rid is None:
                    continue
                pa, pb = sa.part.related_part(rid), sb.part.related_part(rid)
                assert hashlib.sha256(pa.blob).digest() == hashlib.sha256(pb.blob).digest(), f'{name}: {rid} 가 다른 대상'
                print(f'  {name}: {rid} 같은 대상 확인 ({pb.partname})')
        ta = a._element.find(qn('p:txBody'))
        ta.getparent().replace(ta, copy.deepcopy(tb))
    if getattr(b, 'has_table', False) and b.has_table:
        tbl_b = b._element.find('.//' + qn('a:tbl'))
        tbl_a = a._element.find('.//' + qn('a:tbl'))
        from lxml import etree
        assert b'r:id' not in etree.tostring(tbl_b) and b'r:embed' not in etree.tostring(tbl_b)
        tbl_a.getparent().replace(tbl_a, copy.deepcopy(tbl_b))
A.save(OUT)
print('synced', len(nb), 'shapes')
