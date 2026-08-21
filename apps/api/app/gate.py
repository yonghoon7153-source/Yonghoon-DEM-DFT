"""공유 암호 — 바깥에 열었을 때만 생기는 문 하나 (ADR 0014).

랩 안에서는 이 파일이 하는 일이 없다.  `WORKBENCH_PASSWORD` 가 비어 있으면
모든 요청이 그대로 지나간다.  암호가 있을 때만, 즉 `bml share` 로 터널을 열어
주소가 인터넷에 있는 동안에만 문이 선다.

문은 정확히 하나다.  사람별 계정이 아니다 — ADR 0012 는 여전히 유효하고,
여기서 푸는 문제는 "네가 누구냐" 가 아니라 "이 주소를 우연히 마주친 사람을
들이지 않는다" 이다.
"""

from __future__ import annotations

import hashlib
import hmac

COOKIE = "workbench_gate"
#: 문 밖에 두는 경로.
#:
#: `/api/health` 는 응답에 데이터가 없고, `bml use` 가 주소를 확인하는
#: 통로다 — 이것까지 막으면 암호를 아는 사람도 주소를 등록할 수 없다.
#: `/__login` 은 문 자체라서 당연히 밖에 있어야 한다.
OPEN_PATHS = frozenset({"/api/health", "/__login"})
#: 쿠키를 얼마나 들고 있게 할지.  한 달.  실험이 그보다 길게 도는 일이 흔해서
#: 짧게 잡으면 결과를 보러 갈 때마다 다시 친다.
MAX_AGE = 60 * 60 * 24 * 30


def token(password: str) -> str:
    """암호에서 쿠키 값을 만든다.

    쿠키에 암호를 그대로 담지 않는다.  담으면 브라우저 저장소를 들여다본
    사람이 그대로 다시 쓸 수 있고, 사람들은 이 암호를 다른 곳에도 쓴다.
    """
    return hmac.new(password.encode("utf-8"), b"workbench-gate-v1",
                    hashlib.sha256).hexdigest()


def accepts_cookie(value: str | None, password: str) -> bool:
    """이 쿠키가 이 암호에서 나온 것인가."""
    if not value or not password:
        return False
    return hmac.compare_digest(value, token(password))


def accepts_password(given: str | None, password: str) -> bool:
    """친 암호가 맞는가.

    `==` 를 쓰지 않는다.  문자열 비교는 첫 다른 글자에서 멈추므로 걸린 시간이
    "몇 글자까지 맞았는지" 를 알려 준다.  여기서 그것이 실제 위협인지와는
    별개로, 맞다고 판정하는 자리가 두 군데인데 한 쪽만 상수 시간인 코드는
    나중에 읽는 사람을 헷갈리게 한다.
    """
    if given is None or not password:
        return False
    return hmac.compare_digest(given.encode("utf-8"), password.encode("utf-8"))


def is_open(path: str) -> bool:
    """문 밖에 두는 경로인가."""
    return path in OPEN_PATHS


def login_page(*, wrong: bool = False) -> str:
    """암호를 묻는 한 장.

    빌드된 프론트엔드를 쓰지 않는다 — 그 파일들도 문 안에 있어서, 문을 열기
    전에는 못 가져온다.  그래서 이 한 장은 스스로 완결돼야 한다.
    """
    message = ("<p class='bad'>암호가 다릅니다.</p>" if wrong else
               "<p class='hint'>이 주소는 바깥에 열려 있습니다. "
               "공유 암호를 적어 주세요.</p>")
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Battery Lab Workbench</title>
<style>
  :root {{ color-scheme: dark light; }}
  body {{ margin: 0; min-height: 100vh; display: grid; place-items: center;
         background: #0f1420; color: #e6e9ef;
         font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  form {{ width: min(360px, 90vw); padding: 28px; border-radius: 14px;
         background: #161c2b; border: 1px solid #26304a; }}
  h1 {{ font-size: 17px; margin: 0 0 4px; }}
  .hint, .bad {{ font-size: 13px; margin: 0 0 18px; }}
  .hint {{ color: #96a0b5; }}
  .bad {{ color: #ff8f8f; }}
  input {{ width: 100%; box-sizing: border-box; padding: 10px 12px;
          border-radius: 9px; border: 1px solid #33405f; background: #0f1420;
          color: inherit; font: inherit; }}
  button {{ width: 100%; margin-top: 12px; padding: 10px; border: 0;
           border-radius: 9px; background: #4c7dff; color: #fff;
           font: inherit; font-weight: 600; cursor: pointer; }}
</style></head>
<body>
  <form method="post" action="/__login">
    <h1>Battery Lab Workbench</h1>
    {message}
    <input type="password" name="password" autofocus autocomplete="current-password"
           aria-label="공유 암호">
    <button type="submit">들어가기</button>
  </form>
</body></html>"""
