# -*- coding: utf-8 -*-
"""고침 C — 지정 변이마다 어느 시험 행이 가르나 (행 단위): 변이 하나를 MUT 트리 사슬에 적용 → rows_dump5 (RR5A–F · RR4D 행 값) → 기대와 다른 행 이름.
PC15-06 (사전 공격 15 P3-3) 이 지목한 생존 변이 · R1/R2 짝 · 다시 셈 자리 셋 · close_old 의 "그 가드 하나만 가르는 행" 확인용.
쓰임: python3 mutant_rows.py <mutate15.py> <고친 판 사슬> <MUT 트리> <도구 폴더> <출력 JSON> <변이 id 쉼표>"""
import json
import subprocess
import sys
from pathlib import Path

M15, SRC, MUT, TOOLS, OUT = (Path(x) for x in sys.argv[1:6])
SEL = sys.argv[6].split(',')
MUT = MUT.absolute()
sys.argv = [sys.argv[0], str(M15), str(SRC), str(MUT), '/dev/null']
ns = {'__name__': 'mutate_c_lib'}
src_mc = (TOOLS / 'mutate_c.py').read_text(encoding='utf-8')
exec(src_mc[:src_mc.index('def run_one(')], ns)              # 변이 목록 (M15_LIST · ADAPT · NEW) 만
plan = {}
for mid, old, new in ns['M15_LIST']:
    a = ns['ADAPT'].get(mid, (old, new)) if mid in ns['ADAPT'] else (old, new)
    plan[mid] = a
for mid, old, new in ns['NEW']:
    plan[mid] = (old, new)
DST = MUT / 'scripts' / 'rint_r_chain.py'
txt = SRC.read_text(encoding='utf-8')
res = {}
try:
    for mid in SEL:
        old, new = plan[mid]
        if txt.count(old) != 1:
            res[mid] = f'NOT_UNIQUE {txt.count(old)}'
            continue
        DST.write_text(txt.replace(old, new), encoding='utf-8')
        jp = MUT / f'_rows_{mid}.json'
        subprocess.run([sys.executable, str(TOOLS / 'rows_dump5.py'), str(MUT), '-', str(jp)], capture_output=True, text=True, timeout=900)
        d = json.loads(jp.read_text(encoding='utf-8'))
        bad = []
        for cid, v in d['checks'].items():
            info = v['info']
            if isinstance(info, dict) and 'bad_names' in info:
                bad += [f'{cid}:{b}' for b in info['bad_names']]
            elif not v['ok']:
                bad.append(f'{cid}:(검사 실패 · {str(info)[:80]})')
        res[mid] = bad
        jp.unlink()
        print(mid, bad, flush=True)
finally:
    DST.write_text(txt, encoding='utf-8')
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
