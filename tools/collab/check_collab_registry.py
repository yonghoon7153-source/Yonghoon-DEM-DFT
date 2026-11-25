#!/usr/bin/env python3
"""check_collab_registry.py — docs/collab 의 공유 HTML 이 웹앱 '공유 보고서' 표 (webapp/data.py COLLAB_REPORTS) 에 걸려 있는지 본다.

사용자 2026-11-24: '앞으로 html 생성하거나 그럴 때 공유 보고서 이 부분 수정하거나 추가하는 걸 자동으로 진행해줘' ·
'그리고 웹앱도 수정했다고 얘기해주고'. 판정은 webapp/data.py collab_registration() 한 곳에서 한다 (사본을 안 만든다).

  python3 tools/collab/check_collab_registry.py --hook      # PostToolUse 훅 (stdin = 훅 JSON) — .claude/settings.json
  python3 tools/collab/check_collab_registry.py [rel ...]   # 손으로 · 인자 없으면 표 밖 HTML 전부 (있으면 종료 1)
  python3 tools/collab/check_collab_registry.py --selftest

--hook 은 Write/Edit 된 파일이 공유 HTML 폴더 (data.collab_dirs) 의 .html 일 때만 말한다 (다른 파일은 조용히 0):
  · 표에 없음  → 표에 넣으라는 말 (additionalContext) — slug · rel · title = 문서 <h1> · date · track · nav_parent · 옛 판은 earlier
  · 표에 있음  → 웹앱 공유 보고서가 이 파일을 그대로 띄운다 · 답에 '웹앱에도 반영' 을 적으라는 한 줄
  · 표를 못 읽음 → '못 읽었다' 를 그대로 말한다 (없음과 구분 · 조용히 넘기지 않는다)

⛔ 이 도구가 못 하는 것
  · Bash (sed · python · cat >) 로 쓴 파일은 훅이 안 걸린다 (Write/Edit 만) — 그 경우의 그물은 webapp 시험
    test_collab_reports::test_every_collab_html_is_on_the_reports_page 다.
  · 표에 넣는 일 자체는 하지 않는다 (트랙 · 부모 캠페인 · 제목은 판단이 필요하다) — 알리기만 한다.
  · 공유 HTML 폴더 = data.collab_dirs() (docs/collab + 표에 든 보고서의 폴더 · 예: CEI db/properties/cei_figs) 만 본다 —
    표에 한 번도 안 든 새 폴더에 만든 HTML 은 못 본다 (그런 HTML 은 docs/collab 에 둔다 · CLAUDE.md 규칙).
"""
import json
import os
import re
import sys
from pathlib import Path

_PAT = re.compile(r"(?:^|/)(docs/collab/[^/]+\.html)$")


def _load_data(root: Path):
    """그 root 의 webapp/data.py 를 **파일 경로로** 불러온다 — `import data` 는 이미 불러온 다른 root (다른 worktree) 의
    모듈을 그대로 돌려줘서 엉뚱한 표를 읽는다 (selftest 가 실제로 잡았다). 파일이 없으면 FileNotFoundError ('못 읽음')."""
    import importlib.util
    f = Path(root).resolve() / "webapp" / "data.py"
    if not f.is_file():
        raise FileNotFoundError(f"{f} 이 없다")
    sys.path.insert(0, str(f.parent))                 # data.py 의 이웃 모듈 import 용
    try:
        spec = importlib.util.spec_from_file_location(f"_collab_data_{abs(hash(str(f)))}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path.pop(0)


def _find_root(p: Path):
    """파일 위치에서 거슬러 올라가 webapp/data.py 가 있는 레포 뿌리 (worktree 면 그 worktree) 를 찾는다. 없으면 None."""
    for d in [p.parent, *p.parents]:
        if (d / "webapp" / "data.py").is_file():
            return d
    return None


def message_for(path: str, root=None):
    """파일 경로 → (rel, 알릴 글) | None (공유 HTML 폴더의 .html 이 아니면).

    공유 HTML 폴더 = data.collab_dirs() (docs/collab + 표에 든 보고서의 폴더 — 예: CEI db/properties/cei_figs).
    표를 못 읽으면 docs/collab 꼴의 경로에만 '못 읽었다' 를 말한다 (다른 폴더는 그 폴더가 공유 폴더인지부터 모른다)."""
    p = Path(path.replace("\\", "/"))
    if p.suffix.lower() != ".html":
        return None
    base = Path(root) if root else _find_root(p)
    m = _PAT.search(p.as_posix())
    if base is None:
        if not m:
            return None
        return m.group(1), (f"⚠ 공유 보고서 표를 못 읽었다 (위 폴더에서 webapp/data.py 를 못 찾음) — {m.group(1)} 이 웹앱 공유 보고서에 "
                            f"걸려 있는지 손으로 확인한다. '없다' 가 아니라 '못 읽었다' 다.")
    try:
        rel = p.resolve().relative_to(Path(base).resolve()).as_posix()
    except ValueError:
        return None
    try:
        D = _load_data(base)
        dirs = D.collab_dirs()
        reg = D.collab_registration(rel)
    except Exception as e:                                        # noqa: BLE001 — 못 읽음을 그대로 말한다
        if not m:
            return None
        return rel, (f"⚠ 공유 보고서 표를 못 읽었다 ({type(e).__name__}: {e}) — {rel} 이 웹앱 공유 보고서 (webapp/data.py COLLAB_REPORTS) "
                     f"에 걸려 있는지 손으로 확인한다. '없다' 가 아니라 '못 읽었다' 다.")
    if Path(rel).parent.as_posix() not in dirs:
        return None
    if reg["registered"]:
        return rel, (f"공유 보고서: {rel} 은 웹앱 공유 보고서 표에 있다 ({reg['kind']} · {reg['url']}) — 웹앱이 이 파일을 그대로 띄우므로 "
                     f"사용자에게 '웹앱 공유 보고서에도 반영됨' 을 같이 알린다. 새 날짜 판으로 바꿨다면 표의 rel 을 새 파일로 · 옛 판은 earlier 로.")
    return rel, (f"⚠ 공유 보고서: {rel} 이 웹앱 공유 보고서 표 (webapp/data.py COLLAB_REPORTS) 에 없다 — 같은 작업에서 표에 넣는다 "
                 f"(slug · rel · title = 문서 <h1> · date · track · nav_parent = 사이드바 캠페인 url · 같은 트랙의 옛 판은 earlier). "
                 f"그다음 webapp 시험 (test_collab_reports) 을 돌리고, 답에 '웹앱도 고쳤다 (공유 보고서)' 를 적는다 (CLAUDE.md 공유 보고서 규칙).")


def hook_main() -> int:
    try:
        ev = json.load(sys.stdin)
    except Exception:                                             # noqa: BLE001 — 훅 입력이 깨졌으면 할 말이 없다
        return 0
    ti = ev.get("tool_input") or {}
    tr = ev.get("tool_response") or {}
    path = ti.get("file_path") or (tr.get("filePath") if isinstance(tr, dict) else None) or ""
    out = message_for(path)
    if out:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": out[1]}}, ensure_ascii=False))
    return 0


def _selftest() -> int:
    import io
    import tempfile
    repo = Path(__file__).resolve().parents[2]
    ok = []

    def ck(name, cond):
        ok.append((name, bool(cond)))

    D = _load_data(repo)
    cur = D.COLLAB_REPORTS[-1]["rel"]
    r = message_for(str(repo / cur), root=repo)
    ck("양성: 표에 있는 보고서 → '표에 있다' + 보기 화면 url", r and "표에 있다" in r[1] and f"/reports/{D.COLLAB_REPORTS[-1]['slug']}" in r[1])
    r = message_for(str(repo / D.INTERFACE_THERMO_REL), root=repo)
    ck("양성: 통합 보고 → integrated", r and "integrated" in r[1])
    r = message_for(str(repo / "docs/collab/__no_such_new_report__.html"), root=repo)
    ck("⛔음성: 표 밖 HTML → '표에 없다' + 넣으라는 말", r and "표 (webapp/data.py COLLAB_REPORTS) 에 없다" in r[1] and "웹앱도 고쳤다" in r[1])
    cei = D.COLLAB_BY_SLUG["cei"]["rel"]
    r = message_for(str(repo / cei), root=repo)
    ck("양성: docs/collab 밖 공유 폴더 (CEI) 의 보고서 → '표에 있다' + /reports/cei", r and "표에 있다" in r[1] and "/reports/cei" in r[1])
    r = message_for(str(repo / "db/properties/cei_figs/__new_cei_page__.html"), root=repo)
    ck("⛔음성: 공유 폴더 (CEI) 의 표 밖 HTML → '표에 없다'", r and "에 없다" in r[1])
    ck("⛔음성: 공유 폴더 밖 HTML (db/properties 아래 다른 곳) 은 말하지 않는다",
       message_for(str(repo / "db/properties/some_other_dir/x.html"), root=repo) is None)
    ck("⛔음성: docs/collab 밖 · HTML 아닌 파일은 말하지 않는다",
       message_for(str(repo / "docs/collab/figs/x.html"), root=repo) is None
       and message_for(str(repo / "docs/collab/sei_reply_2026_08_07.md"), root=repo) is None
       and message_for(str(repo / "webapp/data.py"), root=repo) is None)
    with tempfile.TemporaryDirectory() as td:
        r = message_for(str(Path(td) / "docs/collab/a.html"), root=td)
        ck("⛔음성: 표를 못 읽으면 '못 읽었다' (없음과 구분)", r and "못 읽었다" in r[1] and "표에 없다" not in r[1])
    # 훅 입출력: stdin JSON → stdout JSON (hookSpecificOutput.additionalContext)
    old_in, old_out = sys.stdin, sys.stdout
    try:
        sys.stdin = io.StringIO(json.dumps({"tool_name": "Write", "tool_input": {"file_path": str(repo / "docs/collab/__no_such_new_report__.html")}}))
        sys.stdout = buf = io.StringIO()
        hook_main()
        js = json.loads(buf.getvalue())
        ck("훅: 표 밖 → hookSpecificOutput.additionalContext", js["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
           and "에 없다" in js["hookSpecificOutput"]["additionalContext"])
        sys.stdin = io.StringIO("not json")
        sys.stdout = buf = io.StringIO()
        ck("훅: 깨진 입력 → 종료 0 · 출력 없음", hook_main() == 0 and buf.getvalue() == "")
        sys.stdin = io.StringIO(json.dumps({"tool_name": "Edit", "tool_input": {"file_path": str(repo / "webapp/data.py")}}))
        sys.stdout = buf = io.StringIO()
        hook_main()
        ck("훅: 다른 파일 → 출력 없음", buf.getvalue() == "")
    finally:
        sys.stdin, sys.stdout = old_in, old_out
    for n, v in ok:
        print(("PASS " if v else "FAIL ") + n)
    bad = [n for n, v in ok if not v]
    print(f"selftest {len(ok) - len(bad)}/{len(ok)}")
    return 1 if bad else 0


def main() -> int:
    args = sys.argv[1:]
    if args[:1] == ["--hook"]:
        return hook_main()
    if args[:1] == ["--selftest"]:
        return _selftest()
    repo = Path(__file__).resolve().parents[2]
    if not args:
        D = _load_data(repo)
        miss = D.collab_unlisted(repo)
        print("표 밖 공유 HTML (" + ", ".join(D.collab_dirs()) + "): " + (", ".join(miss) if miss else "없음"))
        return 1 if miss else 0
    for a in args:
        out = message_for(str(repo / a) if not os.path.isabs(a) else a, root=repo)
        print(out[1] if out else f"{a}: docs/collab HTML 이 아니다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
