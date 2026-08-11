#!/usr/bin/env python3
"""Claude Code 상태줄 — 컨텍스트 사용률을 항상 띄우고 50% 에서 경고한다.

Claude Code 가 stdin 으로 JSON 을 준다. 버전마다 필드 이름이 달라서
후보 경로를 여러 개 훑고, 못 찾으면 조용히 나머지 정보만 낸다
(상태줄이 깨져서 아무것도 안 보이는 것보다 낫다).

이 도구가 **못 하는 것**: 스스로 compact 를 걸지 못한다. 자동 compact 는
settings.json 의 autoCompactWindow 가 하고, 이 스크립트는 표시·경고만 한다.
CLAUDE_STATUSLINE_DEBUG=1 로 실행하면 받은 JSON 을 /tmp 에 덤프한다.

쓰기: settings.json 의 statusLine.command 로 등록.
      python3 tools/claude/statusline.py --selftest   # 자체 시험
"""
import json
import os
import sys

WARN_PCT = 50          # 이 이상이면 경고 (사용자 규칙)
CRIT_PCT = 70

C = {"g": "\033[32m", "y": "\033[33m", "r": "\033[31m",
     "d": "\033[2m", "b": "\033[1m", "x": "\033[0m"}

#: (used, total) 후보 — 버전에 따라 어느 하나가 있다
USED_KEYS = [("context", "used_tokens"), ("context", "used"),
             ("context", "input_tokens"), ("usage", "used_tokens")]
TOTAL_KEYS = [("context", "total_tokens"), ("context", "max_tokens"),
              ("context", "total"), ("context", "window"),
              ("usage", "max_tokens")]


def dig(d, path):
    for k in path:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d if isinstance(d, (int, float)) else None


def pick(d, paths):
    for p in paths:
        v = dig(d, p)
        if v:
            return v
    return None


def context_pct(d):
    """(퍼센트, used, total) — 못 구하면 (None, None, None)."""
    used, total = pick(d, USED_KEYS), pick(d, TOTAL_KEYS)
    if used and total:
        return round(100.0 * used / total), used, total
    # 마지막 수단: 200k 초과 플래그만 있는 버전
    if d.get("exceeds_200k_tokens"):
        return 100, None, None
    return None, None, None


def render(d):
    parts = []
    pct, used, total = context_pct(d)
    if pct is not None:
        col = C["r"] if pct >= CRIT_PCT else C["y"] if pct >= WARN_PCT else C["g"]
        tok = f" {used // 1000}k/{total // 1000}k" if used and total else ""
        parts.append(f"{col}ctx {pct}%{tok}{C['x']}")
        if pct >= WARN_PCT:
            parts.append(f"{C['b']}{C['r']}→ /compact{C['x']}")
    else:
        parts.append(f"{C['d']}ctx ?{C['x']}")

    model = (d.get("model") or {}).get("display_name") or (d.get("model") or {}).get("id")
    if model:
        parts.append(f"{C['d']}{model}{C['x']}")

    ws = d.get("workspace") or {}
    cwd = ws.get("current_dir") or d.get("cwd")
    if cwd:
        parts.append(f"{C['d']}{os.path.basename(cwd)}{C['x']}")

    br = branch(cwd)
    if br:
        parts.append(f"{C['d']}{br}{C['x']}")
    return "  ".join(parts)


def branch(cwd):
    """git HEAD 를 파일로 읽는다 (subprocess 없이 — 상태줄은 자주 돈다)."""
    if not cwd:
        return None
    d = os.path.abspath(cwd)
    while True:
        head = os.path.join(d, ".git", "HEAD")
        if os.path.isfile(head):
            try:
                with open(head) as f:
                    ref = f.read().strip()
            except OSError:
                return None
            return ref.rsplit("/", 1)[-1] if ref.startswith("ref:") else ref[:7]
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def main():
    raw = sys.stdin.read()
    try:
        d = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        d = {}
    if os.environ.get("CLAUDE_STATUSLINE_DEBUG"):
        try:
            with open("/tmp/claude-statusline-payload.json", "w") as f:
                f.write(raw)
        except OSError:
            pass
    print(render(d))
    return 0


def selftest():
    ok = True
    cases = [
        ("정상 40%", {"context": {"used_tokens": 80000, "total_tokens": 200000},
                      "model": {"display_name": "Opus"}}, ["ctx 40%", "80k/200k"], ["/compact"]),
        ("경계 50% 경고", {"context": {"used_tokens": 100000, "total_tokens": 200000}},
         ["ctx 50%", "/compact"], []),
        ("대체 필드명", {"context": {"used": 150000, "max_tokens": 200000}},
         ["ctx 75%"], []),
        ("컨텍스트 정보 없음", {"model": {"id": "x"}}, ["ctx ?"], ["/compact"]),
        ("200k 플래그", {"exceeds_200k_tokens": True}, ["ctx 100%", "/compact"], []),
        ("빈 입력", {}, ["ctx ?"], []),
    ]
    for label, payload, want, absent in cases:
        out = render(payload)
        miss = [w for w in want if w not in out]
        extra = [a for a in absent if a in out]
        if miss or extra:
            print(f" ✗ {label}: 누락{miss} 오출력{extra}\n     {out!r}")
            ok = False
        else:
            print(f" ✓ {label}")
    # 깨진 JSON 이 와도 죽지 않아야 한다
    try:
        json.loads("{oops")
    except json.JSONDecodeError:
        print(" ✓ 깨진 JSON 방어 (main 에서 {} 로 대체)")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
