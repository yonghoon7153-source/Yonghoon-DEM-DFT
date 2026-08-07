#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase A 회귀 — 인증 게이트(F-01) · archive path containment(F-06) · XSS(F-15).

리뷰 §6.3 이 요구한 입력을 그대로 넣는다: `../`, `..\\`, 절대경로, UNC, `archive:../../…`,
케이스 이름의 경로 구분자.  전부 **거부**되고 archive 밖에 읽기/쓰기가 없어야 한다.

  python3 webapp/test_security_phase_a.py
"""
import os
import re
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
    # ── 격리된 데이터 루트로 앱을 띄운다 (실제 데이터를 건드리지 않는다) ──
    tmp = tempfile.mkdtemp(prefix='phaseA_')
    for k, sub in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                   ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
        os.environ[k] = os.path.join(tmp, sub)
    os.environ['WEBAPP_REQUIRE_AUTH'] = '1'
    os.environ['WEBAPP_AUTH_TOKEN'] = 's3cret'
    import app as webapp                                  # noqa: E402

    aroot = os.path.realpath(webapp.app.config['ARCHIVE_FOLDER'])
    outside = os.path.join(tmp, 'OUTSIDE_SECRET')
    os.makedirs(outside, exist_ok=True)
    open(os.path.join(outside, 'full_metrics.json'), 'w').write('{"stolen": true}')

    # ══ F-06: archive containment ══
    from werkzeug.exceptions import HTTPException
    hostile = ['../OUTSIDE_SECRET', '..\\OUTSIDE_SECRET', '../../etc',
               '/etc', 'C:\\Windows', '\\\\server\\share',
               'a/../../OUTSIDE_SECRET', './../OUTSIDE_SECRET']
    esc = []
    with webapp.app.test_request_context('/'):
        for h in hostile:
            try:
                got = webapp._archive_join(h)
                if got != aroot and not got.startswith(aroot + os.sep):
                    esc.append((h, got))
            except HTTPException as e:
                if e.code != 400:
                    esc.append((h, f'HTTP {e.code}'))
    chk(f'1) ★ archive 탈출 시도 {len(hostile)}종이 전부 차단', not esc)
    if esc:
        print('     탈출:', esc)

    with webapp.app.test_request_context('/'):
        ok_rel = webapp._archive_join('folder/case_1')
        chk('2) 정상 상대경로는 루트 안으로 해석', ok_rel.startswith(aroot + os.sep))
        chk('3) 조회가 유령 디렉터리를 만들지 않는다 (F-16)', not os.path.exists(ok_rel))

    # ══ F-06: 표시 이름 ↔ 저장 slug 분리 ══
    bad_names = ['../evil', 'a/b', 'a\\b', '..', '.', '', 'C:\\x', '  ../  ']
    slugs = [webapp._slugify_case_name(n, fallback='fb') for n in bad_names]
    chk('4) ★ 케이스 이름의 경로 문자가 slug 에서 제거된다',
        all(('/' not in s and '\\' not in s and s not in ('.', '..', '')) for s in slugs))
    chk('5) 정상 이름(한글 포함)은 보존', webapp._slugify_case_name('실험_2mAh-real.14')
        == '실험_2mAh-real.14')

    # ══ F-01: 인증 게이트 ══
    c = webapp.app.test_client()
    chk('6) 읽기(GET /)는 통과', c.get('/').status_code == 200)
    chk('7) ★ 미인증 쓰기는 401', c.post('/delete/nope').status_code == 401)
    chk('8) ★ 고비용 GET(/predictor/train)도 보호', c.get('/predictor/train').status_code in (302, 401))
    chk('9) 정적/로그인은 면제', c.get('/login').status_code == 200)
    chk('10) 헬스체크는 면제', c.get('/healthz').status_code == 200)
    chk('11) 틀린 토큰 거부', c.post('/login', data={'token': 'x'}).status_code == 401)
    chk('12) 맞는 토큰 → 세션 발급', c.post('/login', data={'token': 's3cret'}).status_code == 302)
    chk('13) 로그인 후 쓰기 통과', c.post('/delete/nope').status_code != 401)
    chk('14) ★ 교차 출처 쓰기는 403 (CSRF)',
        c.post('/delete/nope', headers={'Origin': 'https://evil.example'}).status_code == 403)
    chk('15) 같은 출처 쓰기는 통과',
        c.post('/delete/nope', headers={'Origin': 'http://localhost'}).status_code != 403)
    c2 = webapp.app.test_client()
    chk('16) Bearer 토큰 경로 동작', c2.post('/delete/nope',
        headers={'Authorization': 'Bearer s3cret'}).status_code != 401)
    chk('17) 틀린 Bearer 는 401', webapp.app.test_client().post('/delete/nope',
        headers={'Authorization': 'Bearer wrong'}).status_code == 401)

    # ══ F-01: fail-closed (게이트 켜라 했는데 토큰 없음) ══
    import importlib

    import security as sec
    prev = os.environ.pop('WEBAPP_AUTH_TOKEN')
    importlib.reload(sec)
    req, tok = sec.auth_config()
    chk('18) ★ REQUIRE_AUTH=1 + 토큰없음 → 게이트는 켜진 채 토큰만 없음(=fail-closed 조건)',
        req is True and not tok)
    os.environ['WEBAPP_AUTH_TOKEN'] = prev

    # ══ F-15: group.html 에 이스케이프 안 된 보간이 남았는가 ══
    g = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'templates', 'group.html'), encoding='utf-8').read()
    chk('19) escHtml 헬퍼가 정의돼 있다', 'function escHtml(' in g)
    chk('20) ★ 보간이 들어간 인라인 이벤트 핸들러가 없다',
        not re.search(r'on[a-z]+="[^"]*\$\{', g))
    for var in ('c.name', 'w.msg', 'w.name', 'p.title', 'p.origin_tip'):
        chk(f'21) {var} 가 escaping 없이 남아있지 않다',
            not re.search(r'\$\{\s*' + re.escape(var) + r'\s*\}', g))

    print(f'\ntest_security_phase_a: {_ok}/{_ok + len(_fail)} PASS'
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
