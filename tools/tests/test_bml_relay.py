#!/usr/bin/env python3
"""중계기(`tools/bml_relay.py`)가 요청을 제대로 넘기는가.

가짜 터널 엣지를 하나 띄운다: 자체 서명 인증서를 쓰는 로컬 HTTPS 서버가 받은
요청을 그대로 되읊는다.  중계기를 **IP 로** 그리로 보내고, 브라우저 노릇은
평문 HTTP 로 한다.  그러면 여기서 실제로 확인되는 것이:

  * TLS 의 SNI 와 HTTP 의 `Host` 가 **원래 터널 이름**으로 나가는가 —
    엣지가 어느 터널인지 가르는 값이라 이것이 틀리면 아무 데도 안 닿는다.
  * 인증서를 **그 이름으로** 검증하는가 (`SSL_CERT_FILE` 로 이 CA 만 믿게
    해 두고, 이름이 다르면 실패해야 한다).
  * POST 몸통과 이진 응답이 **바이트 그대로** 오가는가 — CSV·XLSX 내려받기가
    여기서 깨지면 화면에서는 "파일이 이상하다" 로만 보인다.
  * 엣지가 죽었을 때 빈 화면 대신 **읽히는 502** 가 나오는가.

사용: python3 tools/tests/test_bml_relay.py     (실패 0 이면 exit 0)
"""

from __future__ import annotations

import http.client
import os
import socket
import ssl
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
RELAY = HERE.parent / "bml_relay.py"
NAME = "fake.lhr.life"
#: 이진 그대로 오가는지 보려고 일부러 UTF-8 로 못 읽는 바이트를 섞는다.
BLOB = bytes(range(256)) * 8

passed = 0
failed = 0


def check(what: str, got, want) -> None:
    global passed, failed
    if got == want:
        passed += 1
        print(f"  ok   {what}")
    else:
        failed += 1
        print(f"  FAIL {what}\n           얻음: {got!r}\n           기대: {want!r}")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class Echo(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # noqa: A003
        pass

    def _reply(self, payload: bytes, kind: str = "text/plain") -> None:
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/blob":
            self._reply(BLOB, "application/octet-stream")
            return
        # 받은 Host 를 그대로 돌려준다 — 중계기가 고쳐 적었는지가 여기서 보인다.
        self._reply(f"host={self.headers.get('Host')} path={self.path}".encode())

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self._reply(b"echo:" + body, "application/octet-stream")


def make_cert(tmp: Path) -> tuple[Path, Path]:
    cert, key = tmp / "c.pem", tmp / "k.pem"
    subprocess.run(
        ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", str(key),
         "-out", str(cert), "-days", "2", "-nodes", "-subj", f"/CN={NAME}",
         "-addext", f"subjectAltName=DNS:{NAME}"],
        check=True, capture_output=True)
    return cert, key


def get(port: int, path: str) -> tuple[int, bytes]:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=15)
    conn.request("GET", path)
    response = conn.getresponse()
    out = (response.status, response.read())
    conn.close()
    return out


def post(port: int, path: str, body: bytes) -> tuple[int, bytes]:
    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=15)
    conn.request("POST", path, body=body,
                 headers={"Content-Length": str(len(body))})
    response = conn.getresponse()
    out = (response.status, response.read())
    conn.close()
    return out


def wait_for(port: int, seconds: float = 10.0) -> bool:
    deadline = time.time() + seconds
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False


def main() -> int:
    tmp = Path(os.environ.get("TMPDIR", "/tmp")) / f"bml-relay-test-{os.getpid()}"
    tmp.mkdir(parents=True, exist_ok=True)
    cert, key = make_cert(tmp)

    edge_port, relay_port = free_port(), free_port()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(str(cert), str(key))
    edge = ThreadingHTTPServer(("127.0.0.1", edge_port), Echo)
    edge.socket = context.wrap_socket(edge.socket, server_side=True)
    edge.daemon_threads = True
    threading.Thread(target=edge.serve_forever, daemon=True).start()

    # 이 CA 하나만 믿게 한다.  중계기가 인증서를 진짜로 검증하는지도 같이
    # 걸린다 -- 검증을 끄고 있으면 이 파일이 없어도 통과할 것이다.
    env = {**os.environ, "SSL_CERT_FILE": str(cert)}

    print("bml 중계기")

    # --check 는 띄우지 않고 한 번만 물어본다.
    probe = subprocess.run(
        [sys.executable, str(RELAY), "--listen", str(relay_port), "--host", NAME,
         "--ip", "127.0.0.1", "--port", str(edge_port), "--check"],
        env=env, capture_output=True, text=True, timeout=30)
    check("--check 는 엣지에 한 번 물어보고 끝난다", probe.returncode, 0)
    check("--check 가 본 코드를 적는다", probe.stdout.strip(), "200")

    relay = subprocess.Popen(
        [sys.executable, str(RELAY), "--listen", str(relay_port), "--host", NAME,
         "--ip", "127.0.0.1", "--port", str(edge_port)],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        check("중계기가 떴다", wait_for(relay_port), True)

        code, body = get(relay_port, "/hello?x=1")
        check("GET 이 통과한다", code, 200)
        # 요점: 브라우저는 127.0.0.1 에 대고 말했는데 엣지는 터널 이름을 들었다.
        check("Host 를 터널 이름으로 고쳐 적는다",
              body.decode(), f"host={NAME} path=/hello?x=1")

        code, body = post(relay_port, "/api/upload", BLOB)
        check("POST 몸통이 바이트 그대로 간다", (code, body), (200, b"echo:" + BLOB))

        code, body = get(relay_port, "/blob")
        check("이진 응답이 바이트 그대로 온다", (code, body), (200, BLOB))
        check("길이도 그대로다", len(body), len(BLOB))
    finally:
        relay.terminate()
        relay.wait(timeout=10)
        edge.shutdown()
        edge.server_close()

    # 엣지가 죽은 뒤에도 화면에 이유가 나와야 한다.  빈 응답으로 끝나면
    # 사람은 중계기가 아니라 워크벤치를 의심하고 엉뚱한 데를 뒤진다.
    dead_port, relay_port = free_port(), free_port()
    relay = subprocess.Popen(
        [sys.executable, str(RELAY), "--listen", str(relay_port), "--host", NAME,
         "--ip", "127.0.0.1", "--port", str(dead_port)],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        wait_for(relay_port)
        code, body = get(relay_port, "/")
        check("엣지가 죽었으면 502", code, 502)
        check("그 이유를 화면에 적는다",
              "못 닿았습니다" in body.decode("utf-8", "replace"), True)
    finally:
        relay.terminate()
        relay.wait(timeout=10)

    for path in (cert, key):
        path.unlink(missing_ok=True)
    tmp.rmdir()

    print(f"\n{passed}개 통과" + (f", {failed}개 실패" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
