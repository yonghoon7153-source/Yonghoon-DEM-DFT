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

⚠⚠ `.claude/settings.json` 에 **autoCompactWindow 를 넣지 말 것** (2026-08-11, 다른
브랜치 실사고).  자동압축을 스테일 읽기에 물리면 압축→스테일→압축 **무한루프**가 된다.
아래 두 가드가 그 루프의 두 마디를 각각 끊는다:

  ① 압축 직후 스테일 (loop-breaker).  트랜스크립트 꼬리의 마지막 usage 는 **압축 前**
     숫자다 — 압축 요약 줄(`isCompactSummary`)이 그 뒤에 오기 때문.  실측 2026-08-11:
     압축 직후 훅이 572,191(=compactMetadata.preTokens 573,306)을 읽고 "57.2 % 초과"를
     찍었다.  ⇒ 압축 경계가 마지막 usage **뒤**면 **조용히 있는다**(다음 턴에 재측정).
  ② 되풀이 잔소리.  임계를 넘긴 채로 있으면 매 프롬프트마다 같은 줄을 찍어 컨텍스트를
     더 먹는다.  자기 이전 출력(`[context-meter] … NN.N%`)이 **마지막 압축 이후에** 있고
     지금이 그때보다 REWARN_STEP %p 넘게 오르지 않았으면 조용히 있는다.

사용:
    python3 scripts/context_meter.py --transcript <path>          # 사람이 직접
    python3 scripts/context_meter.py --hook                       # 훅 모드 (stdin JSON)
    python3 scripts/context_meter.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

#: 표준 컨텍스트 창 후보 — `--window auto` 가 관측 최대치를 넘는 **가장 작은** 것을 고른다.
WINDOWS = (200_000, 500_000, 1_000_000)
DEFAULT_THRESHOLD = 50.0
TAIL_BYTES = 512 * 1024
#: 이미 경고한 뒤, 다시 경고하려면 이만큼(%p)은 더 올라야 한다 (가드 ②).
REWARN_STEP = 10.0
#: 훅이 남긴 자기 출력에서 백분율을 되읽는다.  `[context-meter]` 는 ASCII 라 JSON 이
#: 한글/블록문자를 \uXXXX 로 escape 해도 살아남는다.
_SELF_PCT = re.compile(r'\[context-meter\].{0,400}?([0-9]+(?:\.[0-9]+)?)%')


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


#: 창 하한을 찾는 넓은 훑기 (세션당 1회, 사이드카가 그 뒤를 맡는다).  실측 8 MB / 86 ms.
PEAK_BYTES = 8 * 1024 * 1024


def scan_peak(path, max_bytes=PEAK_BYTES):
    """넓은 꼬리에서 **최대 점유량**만 뽑는다 = 창의 하한 (가드 ③).

    ⚠ 정규식으로 `"..._tokens":(\\d+)` 를 줄마다 합산하면 **틀린다** — 한 줄에 usage 객체가
    여럿 실리는 줄(압축 요약 등)이 있어 합치면 창을 넘는 값이 나온다 (실측 1,933,526 > 1 M).
    그래서 구조로 읽되, 후보 줄만 파싱해 비용을 줄인다 (실측 8 MB → 795 줄만 파싱, 86 ms)."""
    if not path or not os.path.exists(path):
        return 0
    size = os.path.getsize(path)
    want = min(max_bytes, size)
    with open(path, 'rb') as fh:
        fh.seek(size - want)
        chunk = fh.read().decode('utf-8', errors='replace')
    best = 0
    for ln in chunk.splitlines():
        if '"cache_read_input_tokens"' not in ln and '"preTokens"' not in ln:
            continue                           # 대부분의 줄은 여기서 걸러진다
        ln = ln.strip()
        if not ln.startswith('{'):
            continue
        try:
            d = json.loads(ln)
        except ValueError:
            continue                           # 잘린 첫 줄 — 정상
        best = max(best, usage_total((d.get('message') or {}).get('usage')) or 0,
                   int((d.get('compactMetadata') or {}).get('preTokens') or 0))
    return best


def peak_path(path):
    """관측 최대치 사이드카 (가드 ③).  트랜스크립트 옆에 두면 세션별로 자동 분리된다."""
    return path + '.ctxpeak' if path else None


def load_peak(path):
    try:
        with open(peak_path(path), encoding='utf-8') as fh:
            return int(json.load(fh).get('peak') or 0)
    except Exception:                          # noqa: BLE001 — 캐시는 없어도 동작해야 한다
        return 0


def save_peak(path, peak):
    try:
        with open(peak_path(path), 'w', encoding='utf-8') as fh:
            json.dump({'peak': int(peak)}, fh)
    except Exception:                          # noqa: BLE001 — 못 써도 계기는 계속 돈다
        pass


def scan_tail(path, tail_bytes=TAIL_BYTES):
    """트랜스크립트 꼬리 1회 훑기 → {'used', 'peak', 'stale', 'warned_pct'}.

    · used       마지막 assistant usage 합계 (없으면 None)
    · peak       꼬리에서 본 **최대** 점유량 (압축 前 usage · compactMetadata.preTokens 포함)
    · stale      압축 요약 줄이 그 usage **뒤**에 있는가 = 읽은 숫자가 압축 前 것인가 (가드 ①)
    · warned_pct 마지막 압축 이후 훅이 스스로 찍은 마지막 백분율 (없으면 None, 가드 ②)

    ★ peak 이 필요한 이유 (가드 ③, 2026-08-11 실측): `--window auto` 가 **지금 담긴 양**만
    보고 창을 고르면, 압축으로 양이 줄었을 때 창도 같이 내려잡혀 백분율이 **부풀어 오른다** —
    실측에서 155,604 tok 이 1M 창의 15.6 % 인데 200k 창으로 잘못 잡혀 **77.8 %** 로 찍혔다.
    573 k 를 담았던 세션의 창은 200 k 일 수 없다 ⇒ 창은 관측 최대치에 대해 **단조**여야 한다.

    꼬리부터 읽되 usage 를 못 찾으면 창을 2배씩 키워 파일 전체까지 재시도한다 (긴 도구-출력
    한 줄이 512 KB 를 넘길 수 있어서 — 실측 트랜스크립트에 그런 줄이 있다)."""
    empty = {'used': None, 'peak': 0, 'stale': False, 'warned_pct': None}
    if not path or not os.path.exists(path):
        return empty
    size = os.path.getsize(path)
    want = min(tail_bytes, size) or 1
    while True:
        with open(path, 'rb') as fh:
            fh.seek(size - want)
            chunk = fh.read().decode('utf-8', errors='replace')
        used = used_i = compact_i = warn_pct = warn_i = None
        peak = 0
        for i, ln in enumerate(chunk.splitlines()):
            ln = ln.strip()
            if not ln.startswith('{'):
                continue
            # ★ 훅의 자기 출력은 어느 줄 종류에 실릴지 보장이 없다 → 원문에서 직접 찾는다.
            m = _SELF_PCT.search(ln)
            if m:
                warn_pct, warn_i = float(m.group(1)), i
            try:
                d = json.loads(ln)
            except ValueError:
                continue                       # 잘린 첫 줄 — 정상
            if d.get('isCompactSummary') or d.get('compactMetadata'):
                compact_i = i
                # 압축 前 점유량이 여기 남아 있다 — 창 하한의 증거 (가드 ③)
                peak = max(peak, int((d.get('compactMetadata') or {}).get('preTokens') or 0))
                continue
            if d.get('type') != 'assistant':
                continue
            t = usage_total((d.get('message') or {}).get('usage'))
            if t is not None:
                used, used_i = t, i
                peak = max(peak, t)
        if used is not None or want >= size:
            return {
                'used': used,
                'peak': peak,
                # 압축 경계가 마지막 usage 뒤 → 읽은 값은 압축 前 숫자다
                'stale': compact_i is not None and (used_i is None or compact_i > used_i),
                # 마지막 압축 이후에 찍은 경고만 센다 (압축했으면 잔소리 카운터도 리셋)
                'warned_pct': warn_pct if (warn_i is not None
                                           and (compact_i is None or warn_i > compact_i)) else None,
            }
        want = min(want * 2, size)


def last_usage(path, tail_bytes=TAIL_BYTES):
    """마지막 assistant usage 합계만 (없으면 None)."""
    return scan_tail(path, tail_bytes)['used']


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

    # ── 가드 ①/② 회귀 (2026-08-11 실사고 재현) ────────────────────────────────
    import contextlib
    import io

    def _hook_out(lines):
        """훅 모드를 실제로 돌려 stdout 을 받는다 (판정 로직이 아니라 **동작**을 본다)."""
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, 't.jsonl')
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(''.join(ln + '\n' for ln in lines))
            argv, stdin = sys.argv, sys.stdin
            sys.argv = ['context_meter.py', '--hook', '--window', '1000000']
            sys.stdin = io.StringIO(json.dumps({'transcript_path': p}))
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    main()
            finally:
                sys.argv, sys.stdin = argv, stdin
            return buf.getvalue(), p

    USE = json.dumps({'type': 'assistant', 'message': {'usage': {'input_tokens': 2,
                      'cache_creation_input_tokens': 6751,
                      'cache_read_input_tokens': 566553}}})          # = 573,306
    SMALL = json.dumps({'type': 'assistant', 'message': {'usage': {'input_tokens': 120_000}}})
    COMPACT = json.dumps({'type': 'user', 'isCompactSummary': True,
                          'compactMetadata': {'trigger': 'manual', 'preTokens': 573306}})
    WARNED = json.dumps({'type': 'user', 'message': {'content':
                         '[context-meter] 컨텍스트 573,306 / 1,000,000 tok  '
                         '[███████████·········] 57.3%  ⚠ 임계 50% 초과'}})

    out, _ = _hook_out([USE])
    chk('12) 압축 없으면 평소대로 경고한다', '[context-meter]' in out and '57.3%' in out)

    out, _ = _hook_out([USE, COMPACT])
    chk('13) ★ 압축 직후엔 조용 — 마지막 usage 는 압축 前 값 (자동압축 무한루프의 마디)',
        out.strip() == '')

    out, _ = _hook_out([USE, COMPACT, SMALL])
    chk('14) 압축 뒤 새 usage 가 들어오면 다시 측정 (12%→경고 없음)', out.strip() == '')

    out, _ = _hook_out([USE, WARNED, USE])
    chk('15) ★ 이미 경고했고 안 올랐으면 조용 (매 턴 잔소리 금지)', out.strip() == '')

    BIG = json.dumps({'type': 'assistant', 'message': {'usage': {'input_tokens': 700_000}}})
    out, _ = _hook_out([USE, WARNED, BIG])
    chk('16) 10%p 넘게 오르면 다시 경고 (57.3→70.0)', '70.0%' in out)

    out, _ = _hook_out([USE, WARNED, COMPACT, BIG])
    chk('17) 압축이 잔소리 카운터를 리셋한다', '70.0%' in out)

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 't.jsonl')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(USE + '\n' + WARNED + '\n' + USE + '\n')
        s = scan_tail(p)
        chk('18) scan_tail 이 자기 출력을 JSON escape 너머로 되읽는다 (57.3)',
            s['warned_pct'] == 57.3 and s['used'] == 573306 and not s['stale'])

    # ── 가드 ③: 창은 단조 (압축으로 양이 줄어도 창이 따라 내려가면 안 된다) ──────
    def _human_out(lines, window='auto'):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, 't.jsonl')
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(''.join(ln + '\n' for ln in lines))
            argv = sys.argv
            sys.argv = ['context_meter.py', '--transcript', p, '--window', window]
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    main()
            finally:
                sys.argv = argv
            return buf.getvalue()

    out = _human_out([USE, COMPACT, SMALL])
    chk('19) ★ 압축 뒤 120k 는 1M 창의 12.0 % — 200k 창으로 내려잡아 60 % 로 부풀지 않는다',
        '12.0%' in out and '1,000,000' in out)
    out = _human_out([COMPACT, SMALL])
    chk('20) usage 가 다 스크롤아웃돼도 compactMetadata.preTokens 가 창 하한을 준다',
        '12.0%' in out)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 't.jsonl')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(USE + '\n')
        sys.argv = ['context_meter.py', '--transcript', p, '--window', 'auto']
        with contextlib.redirect_stdout(io.StringIO()):
            main()                                     # ← peak 사이드카 기록
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(SMALL + '\n')                     # 압축 흔적조차 스크롤아웃된 상태
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main()
        chk('21) 사이드카가 관측 최대치를 기억한다 (증거가 꼬리에서 사라진 뒤에도 1M)',
            '12.0%' in buf.getvalue() and load_peak(p) == 573306)

    with tempfile.TemporaryDirectory() as td:
        # ★ 한 줄에 usage 가 여럿 실린 줄 (압축 요약이 이전 메시지를 품는 형태).
        #   합산하면 1,046,612 = 창 초과 → peak 은 **최댓값**이어야 한다.
        p = os.path.join(td, 't.jsonl')
        nested = json.dumps({'type': 'assistant',
                             'message': {'usage': {'cache_read_input_tokens': 573306},
                                         'prior': [{'usage': {'cache_read_input_tokens': 473306}}]}})
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(nested + '\n')
        chk('22) ★ scan_peak 은 줄 안의 usage 를 합치지 않는다 (정규식 합산 1.93M 버그)',
            scan_peak(p) == 573306)
        chk('23) 후보 없는 파일은 0', scan_peak(os.path.join(td, 'none.jsonl')) == 0)

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
    scan = scan_tail(path)
    used = scan['used']
    if used is None:
        if not a.hook:
            print(f'컨텍스트 계기: usage 를 못 찾음 (transcript={path or "미지정"})')
        return 0
    if scan['stale']:
        # 가드 ① — 압축 직후.  읽은 숫자는 압축 前 것이라 여기서 경고하면 방금 압축한
        # 사용자에게 또 압축을 권한다 (자동압축이면 그대로 무한루프).
        if not a.hook:
            print(f'컨텍스트 계기: 압축 직후 — 마지막 usage({used:,})는 압축 前 값이라 '
                  f'보고를 보류한다 (다음 assistant 턴에 재측정).')
        return 0
    # 가드 ③ — 창은 관측 최대치에 대해 단조.  꼬리에서 스크롤아웃돼도 사이드카가 기억한다.
    cached = load_peak(path)
    peak = max(used, scan['peak'], cached)
    if cached <= 0:
        peak = max(peak, scan_peak(path))      # 사이드카가 빈 세션에서만 넓게 훑는다
    if peak > cached:
        save_peak(path, peak)
    window = pick_window(peak, a.window)
    pct, msg, over = report(used, window, a.threshold)
    if a.hook:
        already = scan['warned_pct']
        if over and (already is None or pct >= already + REWARN_STEP):
            # UserPromptSubmit 훅의 stdout 은 컨텍스트에 실린다 → 에이전트가 보고 판단한다.
            print(f'[context-meter] {msg}  '
                  f'(이번 턴을 마치면 /compact 를 사용자에게 권할 것. '
                  f'⚠ 압축은 한정어를 깎으니, 진행 중 판정·수치는 압축 전에 파일로 내려둘 것.)')
        return 0
    print(msg)
    return 0


if __name__ == '__main__':
    sys.exit(main())
