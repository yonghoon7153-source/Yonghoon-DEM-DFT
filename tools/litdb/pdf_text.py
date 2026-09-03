#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF → 텍스트. pdfminer 우선, 실패하면 stdlib 스캐너로 폴백.

왜 있나 (2026-09-03):
    이 컨테이너의 `cryptography` 가 깨져 있어(`pyo3_runtime.PanicException`)
    **pdfminer 를 그냥 import 하면 터진다.** 그런데 pdfminer 가 cryptography 를 쓰는 곳은
    **암호화된 PDF 복호화 하나뿐**이다 → 그 모듈만 스텁으로 막으면 pdfminer 가 정상 동작한다.
    이 도구가 그 스텁을 자동으로 깔아준다.

    ⚠ 2026-09-03 정정: 그 전에는 "PDF 라이브러리를 못 쓴다" 고 판단하고 stdlib 스캐너만
    썼는데 **틀렸다.** pdfminer 는 이미 설치돼 있었고(`pip install` 이 안 될 뿐),
    실측 비교에서 Wiley 논문 1편 기준 stdlib 스캐너 **367자(워터마크만)** vs
    pdfminer **39,482자(본문 전체)** 였다. 기본 백엔드는 pdfminer 다.

백엔드:
    pdfminer (기본) — 폰트 인코딩·좌표 기반 줄바꿈까지 제대로. 느리다(논문 1편 ~10-60 s).
    stdlib          — 의존성 0. 콘텐츠 스트림을 정규식으로 훑는다. pdfminer 가 실패할 때만.

동작:
    xref 를 파싱하지 않는다. 파일 전체를 정규식으로 훑어 `stream…endstream` 블록을 찾고,
    zlib 해제 후 텍스트 연산자(BT)가 있는 것만 골라 문자열 리터럴 `(...)` 과
    16진 문자열 `<...>`(UTF-16BE) 을 뽑는다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 이 도구가 **못 하는 것**  (§1-8 은 stdlib 백엔드 한계, §9- 는 공통)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **폰트 인코딩을 안 푼다.** CID/ToUnicode CMap 을 무시하므로 서브셋 폰트·한글·수식은
   깨진 글자로 나온다. 실제로 발표자료에서 "ZnI₂"가 "ŶI2", "→"가 "ї" 로 나온 사례가 있다.
   → **깨진 글자를 추측해서 복원하지 마라.** 원문 확인이 필요하면 사람이 PDF 를 열어야 한다.
2. **이미지 슬라이드는 아무것도 못 낸다.** 스캔본·그림만 있는 장은 빈 페이지로 나온다.
   빈 결과를 "내용 없음" 으로 오해하면 안 된다 — `--stats` 로 몇 장이 비었는지 먼저 봐라.
3. **레이아웃·읽기 순서를 보장 못 한다.** 다단·표·각주가 섞인다. **표는 신뢰하지 마라.**
4. **페이지 경계가 근사다.** 콘텐츠 스트림 단위로 자르므로 PDF 페이지 번호와 어긋날 수 있다.
   (발표자료처럼 1장=1스트림이면 대체로 맞는다.)
5. 암호화 PDF · Flate 이외 필터(LZW/CCITT/JBIG2) · 오브젝트 스트림 안의 텍스트는 못 읽는다.
6. **좌표를 안 본다** → 위첨자/아래첨자, 줄바꿈, 단어 사이 공백이 사라지거나 붙는다.
7. 추출 성공 여부를 스스로 검증하지 못한다. 나온 텍스트가 맞는지는 사람이 봐야 한다.
8. 문자열을 정규식으로 찾으므로 **균형이 안 맞는 괄호**가 든 리터럴은 앞부분을 잃는다
   (스펙상 이스케이프돼 있어야 하지만, 어긴 생성기가 있다). 괄호가 많은 본문은 의심해라.
   ⚠ **Wiley/Elsevier 논문은 본문이 Form XObject 안에 있어 stdlib 백엔드로는 워터마크만 나온다.**
   실측: 본문 대신 "Downloaded from …wiley.com…" 367자만 19장 반복. 반드시 pdfminer 를 써라.

■ 공통 한계 (백엔드 무관)
9. **암호화된 PDF 는 못 연다** (cryptography 스텁이라 복호화 불가 — 명시적으로 예외를 던진다).
10. **스캔본/이미지 PDF 는 아무것도 못 낸다.** OCR 없음. 빈 결과 = "내용 없음" 이 아니다.
11. **표는 신뢰하지 마라.** 셀 경계가 사라져 숫자가 뒤섞인다. 표는 사람이 PDF 를 열어 봐야 한다.
12. 추출이 맞는지 스스로 검증 못 한다 — `--stats` 로 길이를 먼저 보고, 이상하면 의심해라.

사용:
    python3 tools/litdb/pdf_text.py --selftest
    python3 tools/litdb/pdf_text.py IN.pdf -o out.txt
    python3 tools/litdb/pdf_text.py IN.pdf --stats          # 몇 장이 비었나 먼저 확인
    python3 tools/litdb/pdf_text.py IN.pdf --min-ascii 0.6  # 폰트 깨진 장 걸러내기
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
import zlib

STREAM_RE = re.compile(rb"stream\r?\n")
#  \\[\s\S] 이어야 한다 — `.` 은 개행을 안 먹어서 줄 이어쓰기(\\<newline>)가 든
#  리터럴을 통째로 놓친다 (selftest 가 잡은 실제 버그, 2026-09-03).
STR_RE = re.compile(rb"\((?:\\[\s\S]|[^\\()])*\)|<[0-9A-Fa-f\s]+>")
OCT_RE = re.compile(rb"\\([0-7]{1,3})")
ESC_RE = re.compile(rb"\\([()\\])")


_NAMED = {ord("n"): 10, ord("r"): 13, ord("t"): 9, ord("b"): 8, ord("f"): 12}


def _decode_literal(g: bytes) -> str:
    """PDF 7.3.4.2 문자열 리터럴. 한 번만 훑는다 — 정규식 다단 치환은 \\( 같은 걸 틀린다.

    스펙: 알려지지 않은 이스케이프(예: \\%)는 **백슬래시를 버리고** 뒤 문자를 남긴다.
    """
    v, out, i, n = g[1:-1], bytearray(), 0, len(g) - 2
    while i < n:
        ch = v[i]
        if ch != 0x5C:                      # 백슬래시 아님
            out.append(ch)
            i += 1
            continue
        i += 1
        if i >= n:                          # 끝의 고아 백슬래시
            break
        c = v[i]
        if 0x30 <= c <= 0x37:               # \ddd 8진 (최대 3자리)
            oct_ = 0
            k = 0
            while i < n and k < 3 and 0x30 <= v[i] <= 0x37:
                oct_ = oct_ * 8 + (v[i] - 0x30)
                i += 1
                k += 1
            out.append(oct_ & 0xFF)
        elif c in _NAMED:
            out.append(_NAMED[c])
            i += 1
        elif c in (0x0A, 0x0D):             # 줄 이어쓰기 — 아무것도 안 남긴다
            i += 1
            if c == 0x0D and i < n and v[i] == 0x0A:
                i += 1
        else:                               # \( \) \\ 및 미지의 이스케이프
            out.append(c)
            i += 1
    return bytes(out).decode("latin-1", "replace")


def _decode_hex(g: bytes) -> str:
    h = re.sub(rb"\s", b"", g[1:-1])
    if len(h) % 2:
        h += b"0"
    try:
        return bytes.fromhex(h.decode("ascii")).decode("utf-16-be", "replace")
    except Exception:
        return ""


def extract_pages(raw: bytes) -> list[str]:
    """텍스트 연산자를 가진 콘텐츠 스트림들을 순서대로 문자열 리스트로."""
    if not raw.startswith(b"%PDF"):
        raise ValueError("PDF 가 아니다 (%%PDF 헤더 없음) — 경로를 확인해라")
    pages = []
    for m in STREAM_RE.finditer(raw):
        s = m.end()
        e = raw.find(b"endstream", s)
        if e < 0:
            continue                      # 잘린 스트림 — 건너뛴다
        blob = raw[s:e]
        try:
            blob = zlib.decompress(blob)
        except Exception:
            continue                      # Flate 아님 / 손상
        if b"BT" not in blob:
            continue                      # 텍스트 스트림이 아님 (이미지·폰트 등)
        buf = []
        for t in STR_RE.finditer(blob):
            g = t.group(0)
            buf.append(_decode_literal(g) if g.startswith(b"(") else _decode_hex(g))
        j = "".join(buf)
        if j.strip():
            pages.append(j)
    return pages


def _install_crypto_stub() -> None:
    """pdfminer import 사슬의 cryptography 를 스텁으로 대체 (암호화 PDF 에만 쓰이는 의존성)."""
    if "cryptography" in sys.modules:
        return
    import types
    for n in ("cryptography", "cryptography.hazmat", "cryptography.hazmat.primitives",
              "cryptography.hazmat.primitives.ciphers", "cryptography.hazmat.backends"):
        m = types.ModuleType(n)
        m.__path__ = []
        sys.modules[n] = m

    class _Blocked:
        def __init__(self, *a, **k):
            raise RuntimeError("암호화된 PDF 다 — 이 환경의 cryptography 가 깨져 못 연다")

    c = sys.modules["cryptography.hazmat.primitives.ciphers"]
    c.Cipher, c.algorithms, c.modes = _Blocked, types.SimpleNamespace(
        AES=_Blocked, ARC4=_Blocked), types.SimpleNamespace(CBC=_Blocked, ECB=_Blocked)
    sys.modules["cryptography.hazmat.backends"].default_backend = lambda: None


def extract_pdfminer(path: str) -> list[str]:
    """pdfminer 백엔드. 페이지별 텍스트 리스트."""
    _install_crypto_stub()
    from pdfminer.high_level import extract_text
    from pdfminer.pdfpage import PDFPage
    with open(path, "rb") as fh:
        n = sum(1 for _ in PDFPage.get_pages(fh))
    return [extract_text(path, page_numbers=[i]) or "" for i in range(n)]


def extract(path: str, backend: str = "auto") -> tuple[list[str], str]:
    """(페이지 리스트, 실제 사용한 백엔드)."""
    if backend in ("auto", "pdfminer"):
        try:
            pages = extract_pdfminer(path)
            if any(p.strip() for p in pages):
                return pages, "pdfminer"
            if backend == "pdfminer":
                return pages, "pdfminer"
        except Exception as e:
            if backend == "pdfminer":
                raise
            print("  (pdfminer 실패 → stdlib 폴백: %s)" % e, file=sys.stderr)
    with open(path, "rb") as fh:
        return extract_pages(fh.read()), "stdlib"


def ascii_ratio(s: str) -> float:
    if not s:
        return 0.0
    return sum(1 for ch in s if 32 <= ord(ch) < 127) / len(s)


def _fixture(text: bytes = b"(Hello XRD) Tj", extra: bytes = b"BT ", ok: bool = True) -> bytes:
    body = extra + text + b" ET"
    blob = zlib.compress(body) if ok else b"NOT-DEFLATE-DATA"
    head = b"%PDF-1.4\n1 0 obj\n<< /Length " + str(len(blob)).encode() + \
           b" /Filter /FlateDecode >>\nstream\n"
    return head + blob + b"\nendstream\nendobj\n%%EOF\n"


def selftest() -> int:
    f, P = [], 0

    def ok(c, n):
        nonlocal P
        P += 1
        if not c:
            f.append(n)

    # ══ 양성 ═══════════════════════════════════════════════════════════════
    ok(extract_pages(_fixture()) == ["Hello XRD"], "기본 리터럴 추출")
    ok(extract_pages(_fixture(b"(a) Tj (b) Tj")) == ["ab"], "리터럴 두 개 이어붙임")
    ok(extract_pages(_fixture(rb"(50\% \(v\/v\)) Tj")) == ["50% (v/v)"], "괄호·백슬래시 이스케이프")
    ok(extract_pages(_fixture(rb"(\101\102) Tj")) == ["AB"], "8진 이스케이프")
    ok(extract_pages(_fixture(rb"(\1012) Tj")) == ["A2"], "8진은 최대 3자리에서 끊김")
    ok(extract_pages(_fixture(b"(a" + b"\\\\" + b"b) Tj")) == ["a\\b"],
       "이스케이프된 백슬래시")
    ok(extract_pages(_fixture(b"(x\\\ny) Tj")) == ["xy"], "줄 이어쓰기는 사라짐")
    ok(extract_pages(_fixture(b"(a\\\\(b) Tj")) == ["b"],
       "N: 균형 안 맞는 괄호가 든 문자열은 앞부분을 잃는다 (한계 §8)")
    ok(extract_pages(_fixture(rb"(tab\there) Tj")) == ["tab\there"], "명명 이스케이프 \\t")
    hexpdf = _fixture(b"<00480065006C006C006F> Tj")
    ok(extract_pages(hexpdf) == ["Hello"], "16진 UTF-16BE 문자열")
    two = _fixture() + _fixture(b"(page two) Tj")
    ok(len(extract_pages(two)) == 2, "스트림 2개 → 페이지 2개")
    ok(extract_pages(two)[1] == "page two", "두 번째 페이지 내용")
    ok(abs(ascii_ratio("abc") - 1.0) < 1e-9, "ascii_ratio 순수 ASCII = 1")
    ok(ascii_ratio("ƵЗД") == 0.0, "ascii_ratio 비ASCII = 0")

    # ══ 음성 — 틀린 입력을 실제로 잡아내는가 ═══════════════════════════════
    def raises(fn, exc=Exception):
        try:
            fn()
        except exc:
            return True
        return False

    ok(raises(lambda: extract_pages(b"hello world, not a pdf"), ValueError),
       "N: PDF 헤더 없음 → 예외 (조용한 빈 결과 금지)")
    ok(raises(lambda: extract_pages(b""), ValueError), "N: 빈 바이트 → 예외")
    ok(extract_pages(_fixture(ok=False)) == [], "N: Flate 아님 → 건너뜀(크래시 없음)")
    # BT 없는 스트림은 텍스트로 잡히면 안 된다 — 필터가 공허하지 않은지
    nobt = _fixture(b"(should not appear) Tj", extra=b"")
    ok(extract_pages(nobt) == [], "N: BT 없는 스트림은 추출 안 됨")
    ok(b"should not appear" in zlib.decompress(
        nobt[nobt.find(b"stream\n") + 7: nobt.find(b"\nendstream")]),
       "N: 그 스트림에 문자열이 실제로 들어있음 (위 검사가 공허하지 않음)")
    trunc = _fixture().replace(b"endstream", b"XXXXXXXXX")
    ok(extract_pages(trunc) == [], "N: endstream 없음 → 건너뜀")
    ok(extract_pages(_fixture(b"() Tj")) == [], "N: 빈 문자열만 → 페이지 아님")
    # 이미지 전용 PDF 는 빈 결과를 내야 하고, 그건 '성공' 이 아니다
    imgonly = (b"%PDF-1.4\n1 0 obj\n<< /Subtype /Image >>\nstream\n"
               + zlib.compress(b"\x00" * 64) + b"\nendstream\nendobj\n")
    ok(extract_pages(imgonly) == [], "N: 이미지 전용 → 빈 결과")
    ok(_decode_hex(b"<48656C6C6F>") != "Hello", "N: 홀수/비UTF16 16진은 원문 그대로 안 나옴")

    # ══ pdfminer 백엔드 ═══════════════════════════════════════════════════
    try:
        _install_crypto_stub()
        import pdfminer  # noqa: F401
        ok(True, "pdfminer import (스텁 적용 후)")
        import cryptography.hazmat.primitives.ciphers as _c
        ok(raises(lambda: _c.Cipher(), RuntimeError),
           "N: 암호화 PDF 경로는 조용히 통과하지 않고 예외")
        from pdfminer.high_level import extract_text  # noqa: F401
        ok(True, "pdfminer.high_level import")
        ok(extract("/nonexistent-xyz.pdf", "stdlib") is None
           if False else raises(lambda: extract("/nonexistent-xyz.pdf", "stdlib"), OSError),
           "N: 없는 파일 → 예외")
    except ImportError:
        ok(False, "pdfminer 사용 불가 — stdlib 로만 동작 (Wiley 본문 못 읽음)")

    print("selftest: %d/%d 통과" % (P - len(f), P))
    for n in f:
        print("  ✗ " + n)
    return 1 if f else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", nargs="?", help="입력 PDF")
    ap.add_argument("-o", "--out", help="출력 txt (기본 stdout)")
    ap.add_argument("--stats", action="store_true", help="장별 길이·ASCII 비율만 출력")
    ap.add_argument("--min-ascii", type=float, default=0.0,
                    help="ASCII 비율이 이 값 미만인 장은 버린다 (폰트 깨진 장 거르기)")
    ap.add_argument("--sep", default="\n===PAGE===\n")
    ap.add_argument("--backend", choices=("auto", "pdfminer", "stdlib"), default="auto")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.pdf:
        ap.print_help()
        return 0
    pages, used = extract(a.pdf, a.backend)
    if used == "stdlib":
        print("⚠ stdlib 백엔드로 떨어졌다 — Wiley/Elsevier 본문은 못 읽는다(한계 §8).",
              file=sys.stderr)
    kept = [(i, p) for i, p in enumerate(pages, 1) if ascii_ratio(p) >= a.min_ascii]
    if a.stats:
        print("백엔드: %s" % used)
        print("텍스트가 나온 장: %d" % len(pages))
        print("ASCII 비율 %.2f 이상 유지: %d  (버림 %d)"
              % (a.min_ascii, len(kept), len(pages) - len(kept)))
        for i, p in enumerate(pages, 1):
            print("  [%3d] %6d자  ascii=%.2f  %s" % (i, len(p), ascii_ratio(p), p[:60].replace("\n", " ")))
        print("\n⚠ 빈 장이 많으면 이미지 슬라이드다 — 이 도구로는 못 읽는다(한계 §2).")
        return 0
    body = a.sep.join("[%d] %s" % (i, p) for i, p in kept)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(body)
        print("→ %s  (%d 장, %d 자)" % (a.out, len(kept), len(body)))
    else:
        sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
