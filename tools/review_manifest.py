#!/usr/bin/env python3
"""review_manifest.py — 리뷰에 실을 해시를 **커밋된 트리에서** 뽑는다.

⛔⛔ 왜 만들었나 (2026-09-02 · 회신 V P0-1)
  리뷰 요청 V 에 이렇게 적었다:

      커밋      35eb8a9f…
      S0 사전등록 60a58f65…

  두 수는 **서로 다른 상태**의 것이었다. 사전등록 해시는 내 **작업 트리** 파일에서
  계산했고, 커밋은 `git rev-parse HEAD` 로 그 변경이 **아직 안 들어간** 커밋이었다.
  재발행은 그 다음 커밋(546b5876)에 들어갔고 리뷰어에게 말한 적이 없다.
  리뷰어가 내가 준 커밋을 받으니 당연히 옛 파일(4c5eb9a5)이 나왔다.

  이 캠페인이 내내 문제 삼는 형태 그대로다 — **산출물과 그에 대한 주장이 결박되지
  않았다.** 그리고 손으로 하는 한 또 난다.

  ⇒ 이 도구는 `git show <commit>:<path>` 로만 해시를 계산한다. 작업 트리를 안 본다.
    트리가 dirty 면 **거부**한다 (그 상태에서 만든 표는 재현되지 않는다).

사용
  python3 tools/review_manifest.py <경로> [<경로> ...]          # HEAD 기준
  python3 tools/review_manifest.py --commit <sha> <경로> ...
  python3 tools/review_manifest.py --allow_dirty <경로> ...     # 초안 전용 표시가 붙는다
  python3 tools/review_manifest.py --selftest

⛔ 이 도구가 **못 하는 것**
  · 파일 내용이 옳은지 보지 않는다 (결박만 본다).
  · 원격에 push 됐는지 확인하지 않는다 — 리뷰어가 받을 수 있는지는 별개다.
    (`--require_pushed` 로 원격 포함 여부를 확인한다.)
  · ZIP 처럼 git 밖에 있는 산출물은 다루지 않는다 — 그건 생성기 receipt 의 몫이다.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys


def _git(*a, check=True):
    r = subprocess.run(["git", *a], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit("⛔ git %s 실패: %s" % (" ".join(a), r.stderr.strip()[:200]))
    return r.stdout


def _blob_sha(commit: str, path: str):
    """`git show <commit>:<path>` 의 sha256. 없으면 None."""
    r = subprocess.run(["git", "show", "%s:%s" % (commit, path)],
                       capture_output=True)
    if r.returncode != 0:
        return None
    return hashlib.sha256(r.stdout).hexdigest()


def review_manifest(paths, commit="HEAD", allow_dirty=False, require_pushed=False):
    """→ dict. 커밋된 트리의 해시만 담는다. dirty 면 (허용 안 하면) SystemExit."""
    dirty = bool(_git("status", "--porcelain").strip())
    if dirty and not allow_dirty:
        raise SystemExit(
            "⛔ 작업 트리가 dirty 다 — 이 상태에서 만든 리뷰 표는 **재현되지 않는다**.\n"
            "   커밋한 뒤에 다시 부르거나, 초안이면 --allow_dirty 를 주십시오\n"
            "   (그러면 산출물에 `draft: true` 가 박혀 리뷰에 그대로 실립니다).\n"
            "   ⚠ 2026-09-02 회신 V P0-1 이 정확히 이 실수였다: 작업 트리 파일의 해시를\n"
            "     그 변경이 없는 커밋과 함께 공표해 리뷰어가 옛 파일을 받았다.")
    sha = _git("rev-parse", commit).strip()
    out = {"schema": "review_manifest/v1",
           "commit": sha,
           "branch": _git("rev-parse", "--abbrev-ref", "HEAD").strip(),
           "git_dirty": dirty,
           "draft": bool(dirty),
           "⛔_해시_출처": ("전부 `git show %s:<path>` 에서 계산했다. **작업 트리를 "
                            "보지 않는다** — 리뷰어가 이 커밋을 받으면 같은 수가 나온다."
                            % sha[:12]),
           "files": {}}
    missing = []
    for p in paths:
        h = _blob_sha(sha, p)
        if h is None:
            missing.append(p)
        out["files"][p] = h
    if missing:
        raise SystemExit(
            "⛔ 커밋 %s 에 없는 경로: %s\n"
            "   리뷰에 실을 수 없다 — 커밋하지 않았거나 경로가 틀렸다."
            % (sha[:12], missing))
    if require_pushed:
        rem = _git("branch", "-r", "--contains", sha, check=False).strip()
        out["pushed"] = bool(rem)
        out["remote_branches"] = [x.strip() for x in rem.splitlines() if x.strip()]
        if not rem:
            raise SystemExit(
                "⛔ 커밋 %s 가 **원격 어디에도 없다** — 리뷰어가 받을 수 없다.\n"
                "   push 한 뒤에 다시 부르십시오." % sha[:12])
    return out


def _render(m):
    w = max((len(p) for p in m["files"]), default=8)
    lines = ["```"]
    for p, h in m["files"].items():
        lines.append("%-*s  %s" % (w, p, h))
    lines.append("%-*s  %s%s" % (w, "커밋", m["commit"],
                                 "   ⚠ DRAFT (dirty)" if m["draft"] else ""))
    if "pushed" in m:
        lines.append("%-*s  %s" % (w, "원격", "있음" if m["pushed"] else "**없음**"))
    lines.append("```")
    return "\n".join(lines)


def selftest():
    ok = [0], [0]
    n_ok, n_bad = [0], [0]

    def chk(c, m):
        print(("  ⭕ " if c else "  ⛔ ") + m)
        (n_ok if c else n_bad)[0] += 1

    import json as _j
    import os
    import tempfile
    td = tempfile.mkdtemp()
    cwd = os.getcwd()
    try:
        os.chdir(td)
        _git("init", "-q")
        _git("config", "user.email", "t@t"); _git("config", "user.name", "t")
        open("a.txt", "w").write("one\n")
        _git("add", "a.txt"); _git("commit", "-qm", "c1")
        c1 = _git("rev-parse", "HEAD").strip()
        m = review_manifest(["a.txt"])
        want = hashlib.sha256(b"one\n").hexdigest()
        chk(m["files"]["a.txt"] == want, "커밋된 파일의 sha256 을 낸다")
        chk(m["commit"] == c1 and m["draft"] is False, "커밋과 draft 표시가 맞다")

        # ⛔음성 (핵심) — **작업 트리를 고쳐도 해시가 안 바뀐다.** 회신 V P0-1 재현.
        open("a.txt", "w").write("two\n")
        try:
            review_manifest(["a.txt"])
            chk(False, "dirty 트리를 거부해야 한다")
        except SystemExit as e:
            chk("dirty" in str(e), "⛔음성: dirty 트리는 **거부**한다 (재현 안 되는 표)")
        m2 = review_manifest(["a.txt"], allow_dirty=True)
        chk(m2["files"]["a.txt"] == want and m2["draft"] is True,
            "⛔음성 V P0-1 재현: --allow_dirty 라도 해시는 **커밋된 내용**이다 "
            "(작업 트리의 'two' 가 아니다) + draft 표시")

        # ⛔음성 — 커밋에 없는 경로는 조용히 빠지지 않는다
        _git("checkout", "-q", "--", "a.txt")
        try:
            review_manifest(["nope.txt"])
            chk(False, "없는 경로를 거부해야 한다")
        except SystemExit as e:
            chk("없는 경로" in str(e), "⛔음성: 커밋에 없는 경로는 거부한다 (빈 칸 금지)")

        # ⛔음성 — push 안 된 커밋은 리뷰어가 못 받는다
        try:
            review_manifest(["a.txt"], require_pushed=True)
            chk(False, "원격에 없는 커밋을 거부해야 한다")
        except SystemExit as e:
            chk("원격 어디에도 없다" in str(e),
                "⛔음성: **원격에 없는** 커밋은 거부한다 (리뷰어가 받을 수 없다)")

        # 옛 커밋 지정
        open("a.txt", "w").write("three\n")
        _git("add", "a.txt"); _git("commit", "-qm", "c2")
        m3 = review_manifest(["a.txt"], commit=c1)
        chk(m3["files"]["a.txt"] == want, "--commit 으로 옛 커밋의 해시를 낸다")
        chk("git show" in m3["⛔_해시_출처"], "해시 출처를 산출물에 적는다")
        chk("```" in _render(m3), "붙여넣기용 표를 낸다")
    finally:
        os.chdir(cwd)
    print("selftest: %d 통과 / %d 실패" % (n_ok[0], n_bad[0]))
    return 1 if n_bad[0] else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--commit", default="HEAD")
    ap.add_argument("--allow_dirty", action="store_true",
                    help="dirty 트리를 허용한다 — 산출물에 draft:true 가 박힌다")
    ap.add_argument("--require_pushed", action="store_true",
                    help="커밋이 원격에 있는지 확인한다 (리뷰어가 받을 수 있는가)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.paths:
        ap.error("경로를 하나 이상 주십시오")
    import json
    m = review_manifest(a.paths, a.commit, a.allow_dirty, a.require_pushed)
    print(json.dumps(m, ensure_ascii=False, indent=1) if a.json else _render(m))
    return 0


if __name__ == "__main__":
    sys.exit(main())
