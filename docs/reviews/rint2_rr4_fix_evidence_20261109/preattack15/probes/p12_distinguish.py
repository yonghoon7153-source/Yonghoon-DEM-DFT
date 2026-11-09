# -*- coding: utf-8 -*-
"""P12 — 생존 변이마다 가르는 입력 (지금 코드 = 거부 · 변이 = 받음?) — 변이를 pa15/mut/scripts/rint_r_chain.py 에 적용한 프로세스에서 (argv[1] = 변이 id ·
   'none' = 변이 없음) 세 자리.  입력: V09 attempt.json machine 바꿈 (요약 정직) · V14 복사 런 end 만 다름 · V14L 복사 런 launch 만 다름 · V15 복사 런 payload ·
   SRC 원천 폴더에 파일 하나 더 (원천 결과 줄 뒤 · 쓰기 자리)."""
import json
import os
import sys
from pathlib import Path

PA15 = Path(__file__).resolve().parent.parent
MID = sys.argv[1]
src_txt = (PA15 / 'tree' / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
dst = PA15 / 'mut' / 'scripts' / 'rint_r_chain.py'
ns = {}
mt = (PA15 / 'probes' / 'mutate15.py').read_text(encoding='utf-8')
exec(mt[mt.index('M = ['):mt.index('\n]\n', mt.index('M = [')) + 3], ns)
if MID != 'none':
    old, new = {m[0]: (m[1], m[2]) for m in ns['M']}[MID]
    assert src_txt.count(old) == 1
    dst.write_text(src_txt.replace(old, new), encoding='utf-8')
else:
    dst.write_text(src_txt, encoding='utf-8')
os.environ['PA15_TREE'] = str(PA15 / 'mut')
sys.path.insert(0, str(PA15 / 'probes'))
try:
    import h  # noqa: E402
finally:
    dst.write_text(src_txt, encoding='utf-8')     # 원본 되돌림 (이미 불러온 모듈은 변이 그대로)
T, RR = h.T, h.RR


class P5:
    """p5_variants 의 도우미 사본 (그 모듈 실행부를 돌리지 않으려고)."""

    @staticmethod
    def ed(base_fn, *fns, att=None, disk=None):
        def mk(tag):
            atts = base_fn(tag)
            atts = T.rr4_edit(atts, *fns, att=att) if (fns or att) else atts
            if disk:
                disk(atts)
            return atts
        return mk

    @staticmethod
    def disk_end_byte(atts):
        p = Path(atts[-1][0]) / 'groups' / f'{h.N1}.end.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        d['killed'] = 0
        p.write_bytes(RR.canon_bytes(d))

    @staticmethod
    def disk_copy_payload(atts):
        od = RR.record_outdir(T.rr4_req(1))
        p = Path(atts[-1][0]) / od / T.RR4_FN
        p.write_bytes(RR.canon_bytes({'synthetic': 'tampered-floor'}))



def disk_launch_byte(atts):
    p = Path(atts[-1][0]) / 'groups' / f'{h.N1}.launch.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['argv'] = ['tampered']
    p.write_bytes(RR.canon_bytes(d))


okc = lambda t: T.rr4_two(t, 'source-ceiling')   # noqa: E731
rows = {'V09_machine': P5.ed(okc, att={'machine': 'gabia'}), 'V14_end_only': P5.ed(okc, disk=P5.disk_end_byte),
        'V14L_launch_only': P5.ed(okc, disk=disk_launch_byte), 'V15_payload': P5.ed(okc, disk=P5.disk_copy_payload)}
res = {}
for nm, mk in rows.items():
    o = h.three(f'D_{MID}_{nm}', mk)
    res[nm] = 'ACCEPTED' if h.accepted(o) else 'rejected'
# 원천 폴더 바뀜 (쓰기 자리만 · 원장 = 바뀌기 전)
atts = okc(f'D_{MID}_src')
st = RR.ledger_parse(''.join(RR.ledger_line(x) for x in T.rr4_lines(atts, last_result=False)).encode('utf-8'))
(Path(atts[0][0]) / 'extra_after_result.txt').write_text('x', encoding='utf-8')
line, why = RR.attempt_result(2, atts[1][0], atts[1][1], 'recover', st)
res['SRC_changed_writer'] = 'ACCEPTED' if line['resume_ok'] else 'rejected ' + ''.join(T.rr4_tag(why))
print(MID, json.dumps(res, ensure_ascii=False))
