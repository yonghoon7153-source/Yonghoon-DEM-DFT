#!/usr/bin/env python3
"""이름 없이 터널을 보는 길 — 127.0.0.1 의 평문 HTTP 를 터널 엣지로 넘긴다.

**왜 있는가.**  랩 망은 터널 도메인(`*.lhr.life` 등)을 DNS 에서 거른다.  그런데
막힌 것은 **이름뿐이고 길은 멀쩡하다** — IP 를 알면 그리로 HTTPS 가 그대로
간다 (`curl --resolve` 로 200 을 실측했다).  브라우저에는 `--resolve` 가 없어서
지금까지의 우회는 `/etc/hosts` 였는데, 그것이 이 랩에서 특히 나쁘다:

  * 브라우저가 **Windows** 에 있어서 WSL 의 `/etc/hosts` 를 아예 안 본다.
    그래서 관리자 PowerShell 로 Windows 쪽에도 같은 줄을 박아야 한다.
  * WSL 은 켤 때마다 `/etc/hosts` 를 다시 만든다 — 재부팅하면 사라진다.
  * 터널 주소는 열 때마다 바뀐다.  바뀔 때마다 위 둘을 처음부터 다시 한다.

이 중계기는 그 셋을 통째로 없앤다.  브라우저는 `http://127.0.0.1:<포트>` 만
보고, 이름 풀이는 아예 일어나지 않는다.  OS 파일을 안 건드리므로 sudo 도,
관리자 PowerShell 도, 재부팅 뒤 복구도 없다.  주소가 바뀌면 이 프로그램만
다시 띄우면 된다.

**하는 일은 한 줄이다**: 받은 요청을 엣지의 **IP** 로 다시 보내되, TLS 의 SNI 와
HTTP 의 `Host` 는 원래 터널 이름으로 적는다.  그 둘이 곧 엣지가 "어느 터널이냐"
를 가르는 값이라, 이름을 안 물어보고도 정확히 같은 곳에 닿는다.

인증서는 **검증한다** (`server_hostname=<터널 이름>`).  IP 로 붙되 이름을
증명하게 하는 것이라, 중간에서 가로채는 것을 놓치지 않는다.

사용:
    python3 bml_relay.py --listen 5013 --host abc.lhr.life --ip 1.2.3.4
    python3 bml_relay.py --listen 5013 --host abc.lhr.life --ip 1.2.3.4 --check

표준 라이브러리만 쓴다.  이 기계에는 워크벤치가 안 깔릴 수도 있어서 (브라우저
노릇만 하는 기계다 — ADR 0011), 의존성을 만들면 그 자체가 새 걸림돌이 된다.
"""

from __future__ import annotations

import argparse
import http.client
import socket
import ssl
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

#: 넘기지 않는 머리글.  한 홉(hop)에서만 뜻이 있는 것들이라, 그대로 옮기면
#: 다음 홉이 거짓말을 듣는다 — 특히 `Transfer-Encoding` 은 우리가 이미 풀어
#: 놓은 몸통에 "아직 청크로 싸여 있다" 고 적는 셈이 된다.
HOP_BY_HOP = frozenset({
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade",
})

CHUNK = 64 * 1024
TIMEOUT = 60


def _open(host: str, ip: str, port: int) -> http.client.HTTPSConnection:
    """엣지로 가는 TLS 연결 하나 — **IP 로 붙고 이름으로 증명받는다.**

    `HTTPSConnection(host)` 만 쓰면 그 이름을 이 기계의 resolver 에 물어보는데,
    그 resolver 가 바로 막힌 곳이다.  그래서 소켓을 직접 열어 (IP) 붙이고,
    `server_hostname` 으로 SNI 와 인증서 검증 이름만 원래 이름으로 준다.
    """
    context = ssl.create_default_context()
    raw = socket.create_connection((ip, port), timeout=TIMEOUT)
    try:
        sock = context.wrap_socket(raw, server_hostname=host)
    except Exception:
        raw.close()
        raise
    conn = http.client.HTTPSConnection(host, port, timeout=TIMEOUT)
    conn.sock = sock
    return conn


class Relay(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    # 기본 구현은 요청마다 stderr 에 한 줄을 찍는다.  그림 한 장에 요청이
    # 수십 개라 로그가 그것만으로 찬다 — 정작 실패가 묻힌다.
    def log_message(self, fmt, *args):  # noqa: A003 - BaseHTTPRequestHandler API
        pass

    def _relay(self) -> None:
        target = self.server.target                                  # type: ignore[attr-defined]
        body = None
        length = self.headers.get("Content-Length")
        if length:
            try:
                body = self.rfile.read(int(length))
            except (ValueError, OSError):
                self._fail(400, "요청 몸통을 읽지 못했습니다.")
                return

        headers = {}
        for name, value in self.headers.items():
            if name.lower() in HOP_BY_HOP or name.lower() == "host":
                continue
            headers[name] = value
        # 엣지는 이 값으로 어느 터널인지 고른다.  브라우저가 적어 보낸
        # `localhost:5013` 을 그대로 넘기면 엣지는 우리를 모른다.
        headers["Host"] = target.host
        # 압축은 그대로 통과시킨다 (Content-Encoding 을 안 건드린다).

        try:
            conn = _open(target.host, target.ip, target.port)
        except Exception as cause:                                   # noqa: BLE001
            self._fail(502, f"터널 엣지에 붙지 못했습니다: {cause}")
            return

        try:
            conn.request(self.command, self.path, body=body, headers=headers)
            upstream = conn.getresponse()
        except Exception as cause:                                   # noqa: BLE001
            conn.close()
            self._fail(502, f"터널이 응답하지 않습니다: {cause}")
            return

        try:
            self.send_response(upstream.status, upstream.reason)
            declared = None
            for name, value in upstream.getheaders():
                if name.lower() in HOP_BY_HOP:
                    continue
                if name.lower() == "content-length":
                    declared = value
                self.send_header(name, value)
            # 길이를 안 알려 주는 응답은 **연결을 닫아서** 끝을 알린다.
            # HTTP/1.1 로 답하면서 길이도 청크도 없으면 브라우저가 다음 요청을
            # 이 연결에서 기다리다 멈춘다.
            if declared is None:
                self.send_header("Connection", "close")
                self.close_connection = True
            self.end_headers()
            if self.command != "HEAD":
                while True:
                    piece = upstream.read(CHUNK)
                    if not piece:
                        break
                    self.wfile.write(piece)
        except (BrokenPipeError, ConnectionResetError):
            # 사람이 탭을 닫았거나 새로고침했다.  중계기가 죽을 일이 아니다.
            self.close_connection = True
        finally:
            conn.close()

    def _fail(self, code: int, message: str) -> None:
        """실패를 **브라우저 안에서** 읽히게 한다.

        빈 화면이나 ERR_EMPTY_RESPONSE 로 끝나면, 사람은 중계기가 아니라
        워크벤치를 의심하고 엉뚱한 데를 뒤진다.
        """
        page = (
            "<!doctype html><meta charset=utf-8>"
            "<style>body{font:14px system-ui;margin:3rem;line-height:1.7}"
            "code{background:#eee;padding:2px 6px;border-radius:4px}</style>"
            f"<h2>중계기가 터널에 못 닿았습니다</h2><p>{message}</p>"
            "<p>중추 서버에서 <code>bml status</code> 를 보세요 — "
            "'공유 주소' 가 없으면 터널이 닫힌 것이고, 그때는 새 주소로 "
            "<code>bmlonly &lt;새 주소&gt; &lt;IP&gt;</code> 를 다시 칩니다.</p>"
        ).encode("utf-8")
        try:
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(page)
        except (BrokenPipeError, ConnectionResetError):
            pass
        self.close_connection = True

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = do_HEAD = _relay
    do_OPTIONS = _relay


class Target:
    __slots__ = ("host", "ip", "port")

    def __init__(self, host: str, ip: str, port: int) -> None:
        self.host, self.ip, self.port = host, ip, port


def check(target: Target) -> int:
    """한 번 물어보고 끝낸다 — 띄우기 전에 이 조합이 맞는지 보는 자리."""
    try:
        conn = _open(target.host, target.ip, target.port)
        conn.request("GET", "/api/health", headers={"Host": target.host})
        code = conn.getresponse().status
        conn.close()
    except Exception as cause:                                       # noqa: BLE001
        print(f"안 닿습니다: {cause}", file=sys.stderr)
        return 1
    print(code)
    return 0 if code == 200 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="터널을 이름 없이 보는 중계기")
    parser.add_argument("--listen", type=int, required=True, help="이 기계에서 열 포트")
    parser.add_argument("--host", required=True, help="터널 이름 (SNI · Host)")
    parser.add_argument("--ip", required=True, help="그 이름의 IP")
    parser.add_argument("--port", type=int, default=443, help="엣지 포트 (기본 443)")
    parser.add_argument("--check", action="store_true",
                        help="한 번 물어보고 끝낸다 (띄우지 않는다)")
    args = parser.parse_args(argv)

    target = Target(args.host, args.ip, args.port)
    if args.check:
        return check(target)

    # **127.0.0.1 에만 연다.**  0.0.0.0 에 열면 같은 망의 아무나 암호 화면까지
    # 오게 되는데, 이 기계는 그런 문을 열어 달라고 한 적이 없다.
    server = ThreadingHTTPServer(("127.0.0.1", args.listen), Relay)
    server.target = target                                           # type: ignore[attr-defined]
    server.daemon_threads = True
    print(f"중계 중 127.0.0.1:{args.listen} → {target.host} ({target.ip})",
          file=sys.stderr, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
