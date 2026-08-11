#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""컨텍스트 사용량 계기 — 트랜스크립트의 **실측 usage** 로 현재 점유율을 낸다.

왜 (2026-08-11 사용자 요청): `/context` 를 눈으로 보고 50 % 근처에서 `/compact` 하는
운용을 자동화한다.  추정이 아니라 **실측**이다 — 트랜스크립트 JSONL 의 assistant 줄에
`message.usage` 가 그대로 들어 있다:

    현재 컨텍스트 = input_tokens + cache_creation_input_tokens + cache_read_input_tokens

⚠ 성능: 트랜스크립트는 수십 MB 로 자란다 (실측 46 MB).  매 프롬프트마다 전부 읽으면
느려지므로 **꼬리만** 읽는다 (기본 512 KB).  꼬리에 usage 가 없으면 창을 키워 재시도.

⚠ 판단: compaction 은 공짜가 아니다 — 이 리포의 가치는 한정어에 있고 압축은 그것부터
깎는다 (context_budget 의 caveman 기각과 같은 논리).  그래서 이 도구는 **알리기만** 하고
자동으로 compact 하지 않는다.  임계 초과 시 사람이/에이전트가 판단한다.

사용:
    python3 scripts/context_meter.py --transcript <path>          # 사람이 직접
    python3 scripts/context_meter.py --hook                       # 훅 모드 (stdin JSON)
    python3 scripts/context_meter.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

#: 표준 컨텍스트 창 후보 — `--window auto` 가 관측 최대치를 넘는 **가장 작은** 것을 고른다.
WINDOWS = (200_000, 500_000, 1_000_000)
DEFAULT_THRESHOLD = 50.0
TAIL_BYTES = 512 * 1024


def usage_total(u):
    """usage dict → 현재 컨텍스트에 올라간 토큰 수.

    ★ output_tokens 는 **더하지 않는다** — 그건 이번 턴에 생성한 양이고, 다음 요청의
    입력으로 넘어갈 때 cache_creation/read 에 이미 반영된다.  더하면 이중 계산이다."""
    if not isinstance(u, dict):
        return None
    keys = ('input_tokens', 'cache_creation_input_tokens', 'cache_read_input_tokens')
    vals = [u.get(k) for k in keys]
    if all(v is None for v in vals):
        return None
    return sum(int(v or 0) for v in vals)


def last_usage(path, tail_bytes=TAIL_BYTES):
    """트랜스크립트 꼬리에서 **가장 마지막** assistant usage 합계.  없으면 None.

    꼬리부터 읽되, 못 찾으면 창을 2배씩 키워 파일 전체까지 재시도한다 (긴 도구-출력
    한 줄이 512 KB 를 넘길 수 있어서 — 실측 트랜스크립트에 그런 줄이 있다)."""
    if not path or not os.path.exists(path):
        return None
    size = os.path.getsize(path)
    want = min(tail_bytes, size)
    while True:
        with open(path, 'rb') as fh:
            fh.seek(size - want)
            chunk = fh.read().decode('utf-8', errors='replace')
        best = None
        for ln in chunk.splitlines():
            ln = ln.strip()
            if not ln.startswith('{'):
                continue
            try:
                d = json.loads(ln)
            except ValueError:
                continue                       # 잘린 첫 줄 — 정상
            if d.get('type') != 'assistant':
                continue
            t = usage_total((d.get('message') or {}).get('usage'))
            if t is not None:
                best = t
        if best is not None or want >= size:
            return best
        want = min(want * 2, size)


def pick_window(observed, window):
    """--window 값 해석.  'auto' 면 관측치를 넘는 가장 작은 표준 창."""
    if window and window != 'auto':
        return int(window)
    for w in WINDOWS:
        if observed is not None and observed <= w * 0.99:
            return w
    return WINDOWS[-1]


def report(used, window, threshold):
    """→ (pct, 한 줄 메시지, 초과 여부)."""
    pct = 100.0 * used / window
    bar_n = int(pct / 5)
    bar = '█' * bar_n + '·' * (20 - bar_n)
    over = pct >= threshold
    msg = (f'컨텍스트 {used:,} / {window:,} tok  [{bar}] {pct:.1f}%'
           + (f'  ⚠ 임계 {threshold:g}% 초과 — /compact 권장' if over else ''))
    return pct, msg, over


# ───────────────────────────── selftest ─────────────────────────────

def _selftest():
    import tempfile
    ok = fail = 0

    def chk(m, c):
        nonlocal ok, fail
        print(('  PASS  ' if c else '  FAIL  ') + m)
        ok, fail = ok + (1 if c else 0), fail + (0 if c else 1)

    u = {'input_tokens': 2, 'cache_creation_input_tokens': 6751,
         'cache_read_input_tokens': 503623, 'output_tokens': 2073}
    chk('1) ★ output_tokens 를 안 더한다 (이중 계산 방지)', usage_total(u) == 510376)
    chk('2) usage 없으면 None', usage_total({}) is None and usage_total(None) is None)
    chk('3) 일부 키만 있어도 합산', usage_total({'input_tokens': 5}) == 5)

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 't.jsonl')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps({'type': 'user', 'message': {}}) + '\n')
            fh.write(json.dumps({'type': 'assistant',
                                 'message': {'usage': {'input_tokens': 1,
                                                       'cache_read_input_tokens': 99}}}) + '\n')
            fh.write(json.dumps({'type': 'assistant',
                                 'message': {'usage': {'input_tokens': 2,
                                                       'cache_read_input_tokens': 500}}}) + '\n')
        chk('4) 마지막 usage 를 쓴다 (100 아니라 502)', last_usage(p) == 502)

        # ★ 꼬리보다 긴 줄이 있어도 찾는다 (창 확대 재시도)
        p2 = os.path.join(td, 'big.jsonl')
        with open(p2, 'w', encoding='utf-8') as fh:
            fh.write(json.dumps({'type': 'assistant',
                                 'message': {'usage': {'input_tokens': 7}}}) + '\n')
            fh.write(json.dumps({'type': 'user', 'message': {'x': 'y' * 300_000}}) + '\n')
        chk('5) ★ 꼬리에 usage 가 없으면 창을 키워 찾는다', last_usage(p2, tail_bytes=1024) == 7)
        chk('6) 없는 파일은 None', last_usage(os.path.join(td, 'nope.jsonl')) is None)

    chk('7) auto 창: 510k → 1M', pick_window(510_376, 'auto') == 1_000_000)
    chk('8) auto 창: 80k → 200k', pick_window(80_000, 'auto') == 200_000)
    chk('9) 명시 창이 우선', pick_window(80_000, '500000') == 500_000)

    pct, msg, over = report(510_376, 1_000_000, 50)
    chk(f'10) 51.0% 판정 + 초과 경고 ({pct:.1f}%)', abs(pct - 51.04) < 0.01 and over and '/compact' in msg)
    _, msg2, over2 = report(100_000, 1_000_000, 50)
    chk('11) 미만이면 경고 없음', not over2 and '/compact' not in msg2)
    print(f'\ncontext_meter selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--transcript', default=os.environ.get('CLAUDE_TRANSCRIPT', ''))
    ap.add_argument('--window', default=os.environ.get('CLAUDE_CONTEXT_WINDOW', 'auto'),
                    help="컨텍스트 창 토큰 수 또는 'auto' (관측치를 넘는 가장 작은 표준 창)")
    ap.add_argument('--threshold', type=float,
                    default=float(os.environ.get('CLAUDE_CONTEXT_THRESHOLD', DEFAULT_THRESHOLD)))
    ap.add_argument('--hook', action='store_true',
                    help='훅 모드 — stdin 의 JSON 에서 transcript_path 를 읽고, '
                         '임계 초과일 때만 한 줄 출력 (평소엔 조용).')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()

    path = a.transcript
    if a.hook:
        try:
            path = (json.load(sys.stdin) or {}).get('transcript_path') or path
        except Exception:                      # noqa: BLE001 — 훅은 절대 세션을 막지 않는다
            return 0
    used = last_usage(path)
    if used is None:
        if not a.hook:
            print(f'컨텍스트 계기: usage 를 못 찾음 (transcript={path or "미지정"})')
        return 0
    window = pick_window(used, a.window)
    pct, msg, over = report(used, window, a.threshold)
    if a.hook:
        if over:
            # UserPromptSubmit 훅의 stdout 은 컨텍스트에 실린다 → 에이전트가 보고 판단한다.
            print(f'[context-meter] {msg}  '
                  f'(이번 턴을 마치면 /compact 를 사용자에게 권할 것. '
                  f'⚠ 압축은 한정어를 깎으니, 진행 중 판정·수치는 압축 전에 파일로 내려둘 것.)')
        return 0
    print(msg)
    return 0


if __name__ == '__main__':
    sys.exit(main())
