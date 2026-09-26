#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""깨진 meta.json 회귀 — 2026-09-26 WSL 이 죽을 때 업로드 두 케이스의 meta.json 이 0 B · 반쪽이 됐고
첫 화면 (/) 전체가 500 이었다 (`list_cases` 가 모든 meta.json 을 예외 처리 없이 json.load).

  ① 목록 (list_cases · /) 은 깨진 meta.json 을 건너뛰고 (기본값 + status 'meta_broken') 200 을 낸다
  ② meta.json 을 쓰는 곳은 전부 원자적 쓰기 (pipeline_service.atomic_write_json: temp → fsync → os.replace) 다
     — 제자리 `open(…, 'w')` 는 기존 파일을 **먼저 잘라** 쓰다 죽으면 반쪽을 남긴다 (깨진 두 파일의 0600 권한 =
       전날 원자적 쓰기로 만든 파일을 제자리 쓰기가 잘랐다는 흔적).
  ③ 원자적 쓰기가 중간에 실패해도 옛 파일은 그대로이고 임시 파일이 남지 않는다

  python3 webapp/test_meta_json_robust.py
"""
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


def main():
    td = tempfile.mkdtemp()
    up, rs = os.path.join(td, 'uploads'), os.path.join(td, 'results')
    cases_in = {'260925_000001_good': json.dumps({'name': 'good', 'created': '', 'mode': 'bimodal', 'status': 'done'}),
                '260925_000002_empty': '',
                '260925_000003_trunc': '{\n  "name": "x",\n  "mode": "bim'}
    for cid, content in cases_in.items():
        os.makedirs(os.path.join(up, cid))
        with open(os.path.join(up, cid, 'meta.json'), 'w') as f:
            f.write(content)
    os.makedirs(rs)
    os.environ['WEBAPP_UPLOAD_FOLDER'], os.environ['WEBAPP_RESULTS_FOLDER'] = up, rs
    import app as webapp
    webapp.app.config['UPLOAD_FOLDER'], webapp.app.config['RESULTS_FOLDER'] = up, rs

    try:
        cases, err = webapp.list_cases(), None
    except Exception as e:                       # 옛 판: JSONDecodeError 가 그대로 올라왔다
        cases, err = [], e
    chk(f'① list_cases 가 깨진 meta.json 에서 죽지 않는다{"" if err is None else " — " + type(err).__name__}', err is None)
    by = {c['id']: c for c in cases}
    chk('①b 세 케이스가 모두 목록에 있다 (깨진 것도 사라지지 않는다)', set(by) == set(cases_in))
    chk('①c 깨진 둘은 status meta_broken · 이름 = 폴더 id',
        all(by.get(c, {}).get('status') == 'meta_broken' and by.get(c, {}).get('name') == c
            for c in ('260925_000002_empty', '260925_000003_trunc')))
    chk('①d 멀쩡한 케이스는 그대로 읽힌다', by.get('260925_000001_good', {}).get('name') == 'good')
    r = webapp.app.test_client().get('/')
    chk(f'② / 가 200 (옛 판 500) — {r.status_code}', r.status_code == 200)

    src = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    bad = [f'app.py:{i}' for i, ln in enumerate(src.split('\n'), 1)
           if re.search(r"\bopen\(.*,\s*'w'\)", ln) and re.search(r"meta_file|'meta\.json'|\bmp\b", ln)]
    chk(f'③ meta.json 을 제자리 open(…, \'w\') 로 쓰는 줄이 없다 {bad if bad else ""}', not bad)

    import pipeline_service as ps
    p = os.path.join(td, 'm.json')
    ps.atomic_write_json(p, {'name': 'old'})

    class Boom:
        def __str__(self):
            raise RuntimeError('boom')
    try:
        ps.atomic_write_json(p, {'name': 'new', 'x': Boom()})
        raised = False
    except RuntimeError:
        raised = True
    chk('④ 원자적 쓰기가 중간에 실패하면 예외가 올라오고 옛 파일은 그대로',
        raised and json.load(open(p)) == {'name': 'old'})
    chk('④b 임시 파일이 남지 않는다', not [f for f in os.listdir(td) if f.startswith('.tmp_')])

    print(f'\ntest_meta_json_robust: {_ok} PASS / {len(_fail)} FAIL')
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
