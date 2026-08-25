#!/usr/bin/env python3
"""daily_refresh.py — 최신성에 민감한 것들이 **낡았는지** 매일 한 번 본다.

왜 이 파일인가
  2026-08-25 실측: 대시보드 카드가 08-20 에서 멈춰 있었고, 그중 b2o3 카드는 이미
  뒤집힌 판정("판정 보류 · 보류 대상 Ea 0.199")을 계속 말하고 있었다. 그 값은
  08-23 에 철회됐다. **화면이 낡으면 끝난 논의를 다시 하게 된다.**
  낡음은 조용히 진행되므로 사람이 눈치채길 기다리면 안 된다 — 매일 기계가 본다.

이 도구의 자리
  · 여기서 하는 것: **낡았다는 사실의 탐지**. 전부 결정론적이라 LLM 이 필요 없다.
  · 여기서 안 하는 것: **판단**. 카드 문구를 새로 쓰거나 철회 사유를 적는 건
    사람/Claude 의 일이다. 이 스크립트는 "무엇이 어긋났나" 만 말하고 종료코드로 알린다.

종료코드
  0  이상 없음        1  손봐야 할 것이 있다        2  스크립트 자체 오류

이 도구가 **못 하는 것**
  · 값의 과학적 타당성을 판정하지 않는다.
  · 서버(gabia/kgy)의 계산 상태를 안 본다 — 그건 server_status.sh 다.
  · 고치지 않는다. 고치는 건 사람이 보고 결정한다.

    python3 tools/claude/daily_refresh.py            # 요약
    python3 tools/claude/daily_refresh.py --verbose  # 항목별 상세
    python3 tools/claude/daily_refresh.py --selftest # 음성 경로 포함 자체검사
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

# ⛔ 2026-08-25 — dirname 을 두 번만 걸어 ROOT 가 `tools/` 가 됐다. 이 파일은
#   tools/claude/ 에 있으므로 **세 번** 올라가야 repo 루트다. 두 번이면 모든 점검이
#   FileNotFoundError 로 죽는데, 그게 "점검 실패" 로 보고돼 진짜 문제처럼 보였다.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KST = timezone(timedelta(hours=9))

#: 대시보드 카드가 kb 최신 카드보다 이만큼 뒤처지면 알린다.
#: 0 일이면 매일 울려 무뎌지고, 너무 길면 낡은 채로 발표에 나간다. 그 사이.
STALE_DAYS = 3


def _kst_today():
    return datetime.now(KST).date()


def _dates_in(text):
    """⛔ 2026-08-25 — 첫 판은 하이픈만 봤다. 우리 kb 파일명 규약은 **밑줄**이라
    (`b2o3_arrhenius_curvature_2026_08_23.md`) 실제 repo 에서 **한 건도 안 잡혔다**.
    selftest 는 통과했는데(합성 입력이 하이픈이었다) 실물에서 None 이 나왔다 —
    양성만 맞춘 selftest 의 전형적인 실패다. 둘 다 받는다."""
    return re.findall(r"(20\d\d)[-_](\d\d)[-_](\d\d)", text)


def newest_kb_card_date(root=ROOT):
    """kb/ 파일명·frontmatter 의 최신 날짜. 없으면 None."""
    best = None
    kb = os.path.join(root, "kb")
    for dirpath, _dn, files in os.walk(kb):
        for f in files:
            if not f.endswith(".md"):
                continue
            for y, m, d in _dates_in(f):
                s = f"{y}-{m}-{d}"
                if best is None or s > best:
                    best = s
    return best


def newest_dashboard_card_date(root=ROOT):
    D = _webapp("data", root)
    ds = [c.get("d") for c in D.dashboard_highlights() if c.get("d")]
    return max(ds) if ds else None


def _webapp(name, root=ROOT):
    """webapp/<name>.py 를 **파일 경로로** 로드한다.

    ⛔ 2026-08-25 — `sys.path.insert` + `import data` 로 했더니 repo 루트의
      **`data/` 디렉터리**(namespace package)가 먼저 잡혀
      `module 'data' has no attribute 'dashboard_highlights'` 로 죽었다.
      이름 충돌은 조용히 다른 모듈을 주므로 경로로 못박는다.
    """
    import importlib.util
    path = os.path.join(root, "webapp", f"{name}.py")
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    wd = os.path.join(root, "webapp")
    if wd not in sys.path:
        sys.path.insert(0, wd)          # webapp 내부 상호 import 용
    spec = importlib.util.spec_from_file_location(f"_wa_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(cmd, root=ROOT):
    try:
        p = subprocess.run(cmd, cwd=root, shell=True, capture_output=True,
                           text=True, timeout=300)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as ex:                            # noqa: BLE001
        return 2, f"실행 실패: {ex}"


# ── 개별 점검 ────────────────────────────────────────────────────────────
def check_dashboard_freshness(root=ROOT):
    kbd, dsh = newest_kb_card_date(root), newest_dashboard_card_date(root)
    if not kbd or not dsh:
        return ("dashboard", None, "날짜를 못 읽었다 (kb 또는 대시보드)")
    lag = (datetime.strptime(kbd, "%Y-%m-%d").date()
           - datetime.strptime(dsh, "%Y-%m-%d").date()).days
    if lag > STALE_DAYS:
        return ("dashboard", False,
                f"대시보드 최신 카드 {dsh} · kb 최신 {kbd} — **{lag}일 뒤처졌다.** "
                f"그 사이 난 판정이 화면에 없다")
    return ("dashboard", True, f"대시보드 {dsh} · kb {kbd} (차 {lag}일)")


def check_canonical(root=ROOT):
    C = _webapp("canonical", root)
    bad = C.validate(C.load_registry())
    if bad:
        return ("canonical", False,
                f"레지스트리 {len(bad)}건이 원자료와 어긋난다: "
                + " · ".join(f"{e.get('metric')}/{e.get('system')}" for e, _ in bad[:4]))
    return ("canonical", True, "레지스트리 ↔ 원자료 일치")


def check_governance(root=ROOT):
    C = _webapp("canonical", root)
    bad = C.validate_governance()
    return ("governance", not bad,
            f"판정 원장 위반 {len(bad)}건: {bad[0]}" if bad else "판정 원장 통과")


def check_kb_lint(root=ROOT):
    rc, out = _run("python3 tools/kb_wiki.py lint", root)
    ok = "RESULT: 0 errors" in out
    m = re.search(r"RESULT: (\d+) errors", out)
    return ("kb-lint", ok, f"kb lint {m.group(1) if m else '?'} errors")


def check_conventions(root=ROOT):
    rc, out = _run("python3 tools/convention_check.py", root)
    ok = "0 위반" in out
    return ("convention", ok, out.strip().splitlines()[-1] if out.strip() else "출력 없음")


def check_requests_ledger(root=ROOT):
    D = _webapp("data", root)
    rows = D.requests_ledger()
    if not rows:
        return ("requests", False, "요청 대장 표를 못 읽었다 — 형식이 바뀌었나")
    conf = [r["n"] for r in rows if r.get("conflict")]
    if conf:
        return ("requests", False,
                f"요청 {', '.join(conf)} 의 이모지와 문장이 어긋난다 — 원문을 고칠 것")
    return ("requests", True, f"요청 {len(rows)}건 · 표시 불일치 0")


def check_fairchem(root=ROOT):
    FC = _webapp("fairchem", root)
    if not FC.available():
        return ("fairchem", None, "번들 미설치 (건너뜀)")
    FC.manifest.cache_clear()
    v = FC.verify_hashes()
    if not v["ok"]:
        return ("fairchem", False,
                f"번들 sha256 불일치 {len(v['mismatch'])}건 · 없음 {len(v['missing'])}건 "
                f"— 공식 스냅샷이라고 인용할 수 없다")
    return ("fairchem", True, f"번들 sha256 {v['checked']}/{v['declared']} 일치")


def check_litdb_index(root=ROOT):
    """어느 인덱스에도 없는 digest 를 잡는다.

    ⛔ 2026-08-25 — 첫 판은 `INDEX.md` **하나만** 봤다. litdb 는 축이 둘로 나뉘어 있고
      (`INDEX.md` = SE/DFT 축, 사람 큐레이션 · `INDEX_DEM.md` = DEM 축, 생성)
      DEM digest 66편을 전부 "미등재" 로 오보했다. 멀쩡한 분리를 결함으로 읽은 것이다.
      판정 로직은 `tools/litdb/build_index.py --check` 하나뿐이다 — 복사하지 말고 쓴다.
    """
    tool = os.path.join(root, "tools", "litdb", "build_index.py")
    if not os.path.isfile(tool):
        return ("litdb", None, "build_index.py 없음 (건너뜀)")
    rc, out = _run("python3 tools/litdb/build_index.py --check", root)
    m = re.search(r"어느 인덱스에도 없는 것 (\d+)편", out)
    if not m:
        return ("litdb", False, f"점검 출력을 못 읽었다 (rc={rc})")
    n = int(m.group(1))
    if n:
        names = re.findall(r"^\s+\[(\w+)\] (\S+)", out, re.M)[:3]
        return ("litdb", False,
                f"어느 인덱스에도 없는 digest {n}편: "
                + " · ".join(f"[{a}] {b}" for a, b in names))
    return ("litdb", True, "digest 전부 인덱스 등재 (DFT·DEM 축 각각)")


def check_uncommitted(root=ROOT):
    rc, out = _run("git status --porcelain", root)
    n = len([l for l in out.splitlines() if l.strip()])
    if n:
        return ("git", False, f"커밋 안 된 변경 {n}건 — 컨테이너가 죽으면 사라진다")
    return ("git", True, "작업트리 깨끗")


CHECKS = [check_dashboard_freshness, check_canonical, check_governance,
          check_kb_lint, check_conventions, check_requests_ledger,
          check_fairchem, check_litdb_index, check_uncommitted]


def run_all(root=ROOT, verbose=False):
    rows = []
    for fn in CHECKS:
        try:
            rows.append(fn(root))
        except Exception as ex:                        # noqa: BLE001
            rows.append((fn.__name__.replace("check_", ""), False,
                         f"점검 자체가 실패했다: {type(ex).__name__}: {ex}"))
    bad = [r for r in rows if r[1] is False]
    print(f"════ daily refresh · {datetime.now(KST):%Y-%m-%d %H:%M} KST ════")
    for name, ok, msg in rows:
        mark = "✅" if ok else ("⛔" if ok is False else "·")
        if verbose or ok is not True:
            print(f"  {mark} {name:12s} {msg}")
    if not bad:
        print("  ✅ 전부 최신 — 손댈 것 없다")
        return 0
    print(f"\n  ⛔ 손봐야 할 것 {len(bad)}건. 아래를 Claude 에게 그대로 주면 된다:")
    print("     " + " / ".join(n for n, _o, _m in bad))
    return 1


# ── selftest ────────────────────────────────────────────────────────────
def _selftest():
    """음성 경로 포함. 양성만 있는 selftest 는 통과해도 아무것도 보증 못 한다."""
    import tempfile
    ok = True

    def say(good, msg):
        nonlocal ok
        print(("  ✓ " if good else "  ✗ ") + msg)
        if not good:
            ok = False

    print("── daily_refresh selftest ──")
    # ★ ROOT 가 repo 루트인지 — 여기가 틀리면 **모든 점검이 조용히 죽는다**
    say(os.path.isdir(os.path.join(ROOT, "webapp"))
        and os.path.isdir(os.path.join(ROOT, "kb"))
        and os.path.isfile(os.path.join(ROOT, "CLAUDE.md")),
        f"⓪ ROOT 가 repo 루트다: {ROOT}")
    # ① 날짜 추출
    # ★ 이 한 줄이 실물 버그를 놓쳤던 자리다 — 합성 입력만 하이픈으로 맞춰 놓고
    #   "밑줄은 안 잡는 게 맞다" 고 단언했다. 우리 kb 는 전부 밑줄이다.
    say(_dates_in("b2o3_x_2026_08_23.md") == [("2026", "08", "23")],
        "① 밑줄 날짜를 잡는다 (우리 kb 파일명 규약)")
    say(_dates_in("card 2026-08-23 ok") == [("2026", "08", "23")], "① 하이픈 날짜를 잡는다")

    # ② [음성] kb 가 대시보드보다 훨씬 새로우면 **반드시** 어긋남으로 잡아야 한다
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "kb", "results"))
        open(os.path.join(td, "kb", "results", "x-2026-12-31.md"), "w").write("x")
        say(newest_kb_card_date(td) == "2026-12-31", "② kb 최신 날짜를 파일명에서 찾는다")

    # ③ [음성] kb 가 비면 None 이어야 한다 (0000-00-00 같은 걸 지어내면 안 된다)
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "kb"))
        say(newest_kb_card_date(td) is None, "③ [음성] kb 가 비면 None (날짜를 지어내지 않는다)")

    # ④ [음성] 점검 함수가 터져도 run_all 이 죽지 않고 '실패' 로 보고해야 한다
    global CHECKS
    keep = CHECKS

    def _boom(root=ROOT):
        raise RuntimeError("일부러 터뜨림")
    CHECKS = [_boom]
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run_all()
    CHECKS = keep
    say(rc == 1 and "점검 자체가 실패했다" in buf.getvalue(),
        "④ [음성] 점검이 예외를 던져도 죽지 않고 실패로 보고한다")

    # ⑤ [음성] litdb 점검이 **두 축을 다 본다** — INDEX.md 만 보면 DEM digest 를
    #   전부 미등재로 오보한다 (첫 판이 66편을 그렇게 잡았다). 소스를 뒤지지 말고
    #   **동작**으로 건다: DEM 축 slug 가 미등재로 나오면 안 된다.
    _n, _ok, _msg = check_litdb_index()
    _dem_leak = any(k in _msg for k in ("dem_", "_dem", "cgmd", "bazzoun", "bucci"))
    say(not _dem_leak,
        f"⑤ [음성] DEM digest 를 미등재로 오보하지 않는다 ({_msg[:52]})")
    say(_ok is not None, "⑤ litdb 점검이 판정을 낸다(건너뛰지 않는다)")

    print("  " + ("✅ selftest 통과" if ok else "⛔ selftest 실패"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true", help="통과한 항목도 전부 찍는다")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true", help="기계용 출력")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.json:
        rows = []
        for fn in CHECKS:
            try:
                n, o, m = fn()
            except Exception as ex:                    # noqa: BLE001
                n, o, m = fn.__name__, False, str(ex)
            rows.append({"check": n, "ok": o, "message": m})
        print(json.dumps({"at": datetime.now(KST).isoformat(), "checks": rows},
                         ensure_ascii=False, indent=1))
        return 1 if any(r["ok"] is False for r in rows) else 0
    return run_all(verbose=a.verbose)


if __name__ == "__main__":
    sys.exit(main())
