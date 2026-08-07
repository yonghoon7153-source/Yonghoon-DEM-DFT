#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""공개 배포용 인증 게이트 — 쓰기·삭제·고비용 계산을 막는다 (코드리뷰 F-01).

배경: `render.yaml` (gunicorn `--bind 0.0.0.0`) 로 공개 배포돼 있었고 인증·인가·CSRF
방어가 전혀 없었다 — 외부에서 `/upload`, `/analyze`, `/delete`, archive 변경/삭제,
predictor 학습까지 그대로 호출됐고 서버는 Supabase **service-role key** 를 쥐고 있다.

★ 2026-08-07: 사용자가 **클라우드 배포를 폐지**해 `render.yaml` 을 삭제했다 (웹앱은 로컬
`run_dem5002.sh` :5002 전용).  그래서 지금 이 게이트는 릴리스 블로커 해소가 아니라
**심층 방어**다 — 기본은 OFF 라 로컬 사용에 마찰이 없고, LAN 노출·ngrok·재배포처럼
누군가 다시 열었을 때만 켜면 된다.  (같은 Phase A 의 F-06 경로 봉쇄와 F-15 XSS 수정은
배포 여부와 무관하게 **로컬에서도 유효**하다.)

═══ 설계: 사설망은 그대로, 공개 배포는 fail-closed ═══════════════════════════════
연구용 로컬 실행을 매번 로그인시키면 쓸모가 떨어지고, 그렇다고 공개 배포에서 열어두면
릴리스 블로커다.  그래서 **환경변수로 두 모드를 가른다**:

  WEBAPP_REQUIRE_AUTH=1  → 게이트 ON.  토큰이 없으면 **모든 쓰기를 503 으로 거부**한다
                           (열어두는 게 아니라 잠근다 = fail-closed).
  (미설정)               → 게이트 OFF.  로컬·사설망 기존 동작 그대로 + 기동 시 경고 1줄.
  WEBAPP_AUTH_TOKEN=…    → 이 토큰으로 로그인/Bearer 인증.

다시 클라우드로 올릴 때는 배포 설정에 `WEBAPP_REQUIRE_AUTH=1` 을 넣고 토큰은 그 플랫폼의
secret 으로 둘 것.  토큰을 넣기 전까지 인스턴스는 **읽기 전용**이 된다 (fail-closed).

═══ CSRF: 토큰 주입 대신 Origin 검사 ════════════════════════════════════════════
UI 의 쓰기는 100+ 개 `fetch()` 에 흩어져 있어 CSRF 토큰을 전부 배선하면 변경 범위가
과도하다.  대신 OWASP 의 표준 대안을 쓴다:
  ① 세션 쿠키에 `SameSite=Strict` + `HttpOnly` (+ HTTPS 면 Secure)
  ② 상태 변경 요청은 **Origin/Referer 의 host 가 요청 host 와 같아야** 통과
Bearer 토큰 요청(CLI/스크립트)은 브라우저가 자동으로 붙이지 않으므로 ②에서 면제한다.

⚠ 이것은 **애플리케이션 레벨** 방어다.  진짜 경계는 배포 ingress 에 두는 것이 낫고,
  rate limit / 업로드 개수·형식 제한은 여기서 다루지 않는다 (리뷰 권장 3·4번 미대응).
"""
from __future__ import annotations

import hmac
import os
from urllib.parse import urlparse

from flask import abort, jsonify, redirect, render_template_string, request, session

#: 인증 없이도 허용되는 경로 접두 (로그인 자체와 정적 파일).
_EXEMPT_PREFIXES = ('/login', '/logout', '/static/', '/healthz', '/favicon.ico')

#: GET 이지만 **상태를 바꾸거나 비싼** 경로 — 리뷰 F-16 이 지적한 것들.
_PROTECTED_GETS = ('/predictor/train',)

_WRITE_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

_LOGIN_HTML = """<!doctype html><meta charset="utf-8"><title>DEM — 로그인</title>
<style>body{background:#12141a;color:#e6e9ef;font-family:system-ui,sans-serif;
display:grid;place-items:center;height:100vh;margin:0}
form{background:#1b1e26;padding:28px 32px;border:1px solid #2a2f3a;border-radius:10px}
input{background:#12141a;color:#e6e9ef;border:1px solid #2a2f3a;border-radius:6px;
padding:9px 11px;width:260px;font-size:.95rem}
button{margin-top:12px;width:100%;padding:9px;border:0;border-radius:6px;
background:#6c8cff;color:#fff;font-weight:600;cursor:pointer}
p{color:#ff6b6b;font-size:.85rem;margin:10px 0 0}</style>
<form method="post"><div style="font-weight:700;margin-bottom:14px">DEM 분석 웹앱</div>
<input type="password" name="token" placeholder="접근 토큰" autofocus>
<button type="submit">들어가기</button>
{% if error %}<p>{{ error }}</p>{% endif %}</form>"""


def _truthy(v):
    return str(v or '').strip().lower() in ('1', 'true', 'yes', 'on')


def auth_config():
    """(게이트 켜짐?, 토큰).  토큰이 있으면 REQUIRE_AUTH 없이도 켠다."""
    token = os.environ.get('WEBAPP_AUTH_TOKEN') or ''
    required = _truthy(os.environ.get('WEBAPP_REQUIRE_AUTH')) or bool(token)
    return required, token


def _same_origin(req):
    """상태 변경 요청이 **같은 출처**에서 왔는가 (CSRF 방어).

    Origin 이 있으면 그것을, 없으면 Referer 를 본다.  둘 다 없으면 브라우저 폼/fetch 가
    아니므로(스크립트) 통과시킨다 — 그 경로는 Bearer 토큰으로 이미 인증됐다.
    """
    src = req.headers.get('Origin') or req.headers.get('Referer')
    if not src:
        return True
    try:
        host = urlparse(src).netloc
    except ValueError:
        return False
    return bool(host) and host == req.host


def _is_protected(req):
    path = req.path or '/'
    if path.startswith(_EXEMPT_PREFIXES):
        return False
    if req.method in _WRITE_METHODS:
        return True
    return any(path.startswith(g) for g in _PROTECTED_GETS)


def _authenticated(req, token):
    if session.get('dem_auth') is True:
        return 'session'
    supplied = (req.headers.get('X-Auth-Token')
                or (req.headers.get('Authorization') or '').removeprefix('Bearer ').strip())
    if supplied and token and hmac.compare_digest(supplied, token):
        return 'bearer'
    return None


def init_security(app):
    """Flask 앱에 게이트를 설치한다.  → (켜짐?, 토큰 있음?)"""
    required, token = auth_config()

    app.config.setdefault('SESSION_COOKIE_HTTPONLY', True)
    app.config.setdefault('SESSION_COOKIE_SAMESITE', 'Strict')
    if _truthy(os.environ.get('WEBAPP_HTTPS')):
        app.config.setdefault('SESSION_COOKIE_SECURE', True)
    if not app.secret_key:
        # 토큰에서 유도 → 재시작해도 세션이 유지되고, 토큰이 없으면 임시 키.
        app.secret_key = (token or os.urandom(24).hex())

    @app.before_request
    def _gate():                                          # noqa: ANN202
        if not required or not _is_protected(request):
            return None
        if not token:
            # ★ fail-closed: 게이트를 켜라고 했는데 토큰이 없으면 **열지 않는다**.
            return jsonify({'error': 'WEBAPP_AUTH_TOKEN 미설정 — 쓰기가 잠겨 있습니다. '
                                     '배포 환경변수에 토큰을 넣으세요.'}), 503
        how = _authenticated(request, token)
        if not how:
            if request.accept_mimetypes.accept_html and request.method == 'GET':
                return redirect('/login?next=' + request.path)
            return jsonify({'error': '인증이 필요합니다.'}), 401
        # 쿠키 인증만 CSRF 대상이다 (Bearer 는 브라우저가 자동으로 붙이지 않는다).
        if how == 'session' and request.method in _WRITE_METHODS and not _same_origin(request):
            return jsonify({'error': '교차 출처 요청이 거부되었습니다 (CSRF).'}), 403
        return None

    @app.route('/login', methods=['GET', 'POST'])
    def login():                                          # noqa: ANN202
        if not required:
            return redirect('/')
        error = None
        if request.method == 'POST':
            supplied = (request.form.get('token') or '').strip()
            if token and hmac.compare_digest(supplied, token):
                session['dem_auth'] = True
                session.permanent = True
                return redirect(request.args.get('next') or '/')
            error = '토큰이 올바르지 않습니다.'
        return render_template_string(_LOGIN_HTML, error=error), (401 if error else 200)

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():                                         # noqa: ANN202
        session.pop('dem_auth', None)
        return redirect('/login')

    if not required:
        print('[Security] ⚠ 인증 OFF — 사설망/로컬 전용 가정. 공개 배포라면 '
              'WEBAPP_REQUIRE_AUTH=1 + WEBAPP_AUTH_TOKEN 을 설정하세요.')
    elif not token:
        print('[Security] ★ REQUIRE_AUTH=1 인데 WEBAPP_AUTH_TOKEN 이 없습니다 — '
              '쓰기·계산이 전부 503 으로 잠깁니다 (fail-closed).')
    else:
        print('[Security] 인증 ON (세션 쿠키 SameSite=Strict + Bearer, 쓰기에 Origin 검사).')
    return required, bool(token)
