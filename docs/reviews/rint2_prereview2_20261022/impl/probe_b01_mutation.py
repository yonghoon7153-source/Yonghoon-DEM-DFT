# -*- coding: utf-8 -*-
"""탐침 D1 (RINT2-B01) — 시험 작성기 J0w 의 판별력: 원본 = 통과 · write_copy 의 newline='\n' 을 빼는 한 줄 변이 = 실패 (옳은 이유: CRLF 바이트).
시험 파일 사본을 탐침 폴더에 두고 (리포에 안 쓴다) 모듈로 불러 t_writer_portable 만 부른다.  parser 는 부르지 않는다."""
import importlib.util
import io
import contextlib
import os
import sys
import tempfile

REPO = os.environ.get('PRE_REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d')
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(REPO, 'scripts', 'test_rint_g2_join.py'), encoding='utf-8').read()
MARK = "with open(p, 'w', encoding='utf-8', newline='\\n') as fh:"
assert src.count(MARK) == 1, src.count(MARK)
res = {}
for tag, text in (('original', src), ('mutant_no_newline', src.replace(MARK, "with open(p, 'w', encoding='utf-8') as fh:"))):
    d = tempfile.mkdtemp(prefix=f'b01_{tag}_', dir=HERE)
    p = os.path.join(d, 'test_rint_g2_join_copy.py')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)
    sys.path.insert(0, os.path.join(REPO, 'scripts'))
    spec = importlib.util.spec_from_file_location(f'tj_{tag}', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.TMP = d
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        m.t_writer_portable()
    res[tag] = {'ok': m._ok, 'fail': list(m._fail), 'out': buf.getvalue().strip().splitlines()}
    print(tag, res[tag]['ok'], res[tag]['fail'])
import json
with open(os.path.join(HERE, 'probe_b01_mutation.json'), 'w', encoding='utf-8') as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
