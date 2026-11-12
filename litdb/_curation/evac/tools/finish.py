#!/usr/bin/env python3
"""finish.py — 논문 에이전트 한 편이 끝난 뒤의 마무리를 한 번에 한다 (litdb-ctl 에서 커밋 · push).

python3 -I finish.py --key N-56 --slug <slug> --commit <sha> --memo "<의도 대조 · 카드 문제 한 줄>" \
        [--next N-61 --tree 1|2]

하는 일
  1. 원격 끝에서 확인: 커밋이 원격에 있는가 · litdb 밖 파일 0 · 카드 줄 수 · png · 식 크롭 · 필수 절 · 메타 줄 · 모음 그림
  2. status.tsv: 그 줄을 '끝 · slug · 커밋 · 메모' 로 · --next 가 있으면 그 줄을 '도는 중 · 시작 시각' 으로
  3. wishlist.md 끝에 `### batch_NN (대피 세션)` + 정독 출력의 n 절 (없으면 건너뜀)
  4. 이어가기 자료 (queue.json · STATE.md · 도구) 를 litdb/_curation/evac/ 에 복사
  5. 커밋 · fetch · rebase · push (세 번까지)
  6. --next 가 있으면 지시서를 만들고 Agent 에 넣을 짧은 지시문을 찍는다
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCR = Path(__file__).resolve().parents[1]
CTL = Path("/home/user/litdb-ctl")
BR = "claude/friendly-meitner-lldvar"
REF = f"origin/{BR}"
TREES = {"1": ("/home/user/litdb-canon", "tmp-litdb-evac"), "2": ("/home/user/litdb-canon2", "tmp-litdb-evac2")}
def _trailer():
    """커밋 끝 두 줄 (공동 저자 줄 · 세션 줄) — 세션마다 다르므로 scratchpad tools/trailer.txt 에 두고 정본에는 올리지 않는다."""
    p = SCR / "tools" / "trailer.txt"
    if not p.is_file():
        sys.exit("⛔ tools/trailer.txt 가 없다 — 이 세션의 커밋 끝 두 줄을 그 파일에 적는다 (정본에 올리지 않는다)")
    return p.read_text(encoding="utf-8").strip()


TRAILER = _trailer()


def git(*a, check=False):
    r = subprocess.run(["git", "-C", str(CTL), *a], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"⛔ git {' '.join(a)}\n{r.stdout}{r.stderr}")
    return r


def prefix(key, q):
    return q.get(key, {}).get("status_prefix") or {
        "X-68": "후보 밖 (68 번 파일)\t", "X-68-1": "보강 (68-1 번 파일)\t", "X-68-2": "보강 (68-2 번 파일)\t",
        "N-72": "N-72 둘째\t대피\t"}.get(key, f"{key}\t대피\t")


def sync_evac():
    d = CTL / "litdb" / "_curation" / "evac"
    (d / "tools").mkdir(parents=True, exist_ok=True)
    for f in ("make_sheet.py", "make_brief.py", "launch.py", "intake.py", "finish.py", "restore.py", "queue.json",
              "received_files.tsv", "AGENT_PROMPT_TEMPLATE.md"):
        s = SCR / "tools" / f
        if s.is_file():
            shutil.copy2(s, d / "tools" / f)
    if (SCR / "STATE.md").is_file():
        shutil.copy2(SCR / "STATE.md", d / "STATE.md")


def push(msg):
    git("add", "litdb/_curation")
    if not git("status", "--porcelain").stdout.strip():
        return git("rev-parse", "--short", "HEAD").stdout.strip() + " (바뀐 것 없음)"
    git("commit", "-q", "-m", msg + "\n\n" + TRAILER, check=True)
    for i in range(3):
        git("fetch", "-q", "origin", BR)
        r = git("rebase", "-q", REF)
        if r.returncode:
            sys.exit(f"⛔ rebase 충돌 — 손으로 푼다 (litdb-ctl)\n{r.stdout}{r.stderr}")
        git("push", "-q", "origin", f"HEAD:{BR}")
        git("fetch", "-q", "origin", BR)
        if git("rev-list", "--count", f"{REF}..HEAD").stdout.strip() == "0":
            return git("rev-parse", "--short", "HEAD").stdout.strip()
        time.sleep(3)
    sys.exit("⛔ push 세 번 실패")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key")
    ap.add_argument("--slug")
    ap.add_argument("--commit")
    ap.add_argument("--memo", default="")
    ap.add_argument("--next", default="")
    ap.add_argument("--tree", default="")
    ap.add_argument("--sync-only", action="store_true", help="이어가기 자료만 올린다")
    a = ap.parse_args()
    q = json.loads((SCR / "tools/queue.json").read_text(encoding="utf-8"))
    git("fetch", "-q", "origin", BR)
    r = git("rebase", "-q", REF)
    if r.returncode:
        sys.exit(f"⛔ 시작 rebase 실패\n{r.stderr}")
    if a.sync_only:
        sync_evac()
        print("pushed", push("litdb: _curation/evac — 대피 세션 이어가기 자료 갱신 (상태 메모 · 대기열 · 도구)"))
        return
    nn = q.get(a.key, {}).get("nn", "?")
    show = lambda p: git("show", f"{REF}:{p}").stdout
    ok = git("merge-base", "--is-ancestor", a.commit, REF).returncode == 0
    names = git("show", "--name-only", "--format=", a.commit).stdout.split()
    outside = [n for n in names if not n.startswith("litdb/")]
    card = show(f"litdb/papers/{a.slug}.md")
    figs = git("ls-tree", "--name-only", REF, f"litdb/figures/{a.slug}/").stdout.split("\n")
    png = [f for f in figs if f.endswith(".png")]
    sheets = sorted(str(p) for p in (SCR / "litcards").glob(f"{a.slug}_sheet*.png"))
    print(f"확인: 커밋 원격에 {'있음' if ok else '⛔ 없음'} · litdb 밖 파일 {len(outside)} · 카드 {len(card.splitlines())} 줄 · png {len(png)} (식 {sum('/eq_' in f for f in png)}) · "
          f"필수 절 {len(re.findall(r'^## .*(의도 대조|자세한 분석|넣는 까닭)', card, re.M))} · 메타 줄 {len(re.findall(r'^> slug', card, re.M))} · 다른 카드 수정 {[n for n in names if n.startswith('litdb/papers/') and a.slug not in n]}")
    print("모음 그림:", *sheets, sep="\n  ")
    if not ok or outside or not card:
        sys.exit("⛔ 확인 실패 — status 를 고치지 않았다")
    p = CTL / "litdb/_curation/status.tsv"
    L = p.read_text(encoding="utf-8").split("\n")
    pre = prefix(a.key, q)
    k = [i for i, l in enumerate(L) if l.startswith(pre)]
    if len(k) != 1:
        sys.exit(f"⛔ status 줄을 하나로 못 찾음: {pre!r} {k}")
    c = L[k[0]].split("\t")
    L[k[0]] = "\t".join([c[0], c[1], "끝", f"{a.slug} · {a.commit[:9]}", f"정독 {nn} · {a.memo}".strip(" ·")])
    start = ""
    if a.next:
        pre2 = prefix(a.next, q)
        k2 = [i for i, l in enumerate(L) if l.startswith(pre2)]
        if len(k2) != 1:
            sys.exit(f"⛔ 다음 줄을 하나로 못 찾음: {pre2!r} {k2}")
        c2 = L[k2[0]].split("\t")
        start = subprocess.run(["date", "+%m-%d %H:%M KST"], capture_output=True, text=True, env={"TZ": "Asia/Seoul"}).stdout.strip()
        c2[2] = "도는 중"
        c2[4] = c2[4] + f" · 시작 {start}"
        L[k2[0]] = "\t".join(c2)
    bad = [l[:40] for l in L if l and l.count("\t") != 4]
    if bad:
        sys.exit(f"⛔ 칸 수 어긋남 {bad}")
    p.write_text("\n".join(L), encoding="utf-8")
    f = show(f"litdb/_curation/reading/batch_{nn}_findings.md").split("\n")
    out, on = [], False
    for l in f:
        if re.match(r"^## n\b", l):
            on = True
            continue
        if on and l.startswith("## "):
            break
        if on:
            out.append(l)
    body = "\n".join(out).strip("\n")
    w = CTL / "litdb/_curation/wishlist.md"
    if body and f"### batch_{nn} (대피 세션)" not in w.read_text(encoding="utf-8"):
        w.write_text(w.read_text(encoding="utf-8").rstrip("\n") + f"\n\n### batch_{nn} (대피 세션)\n{body}\n", encoding="utf-8")
    print(f"정독 n 절: {len([l for l in out if l.startswith('- [n]')])} 줄" + ("" if body else " (없음 — 정독 출력 확인 필요)"))
    sync_evac()
    msg = f"litdb: _curation status — {a.key} 끝 ({a.commit[:9]})" + (f" · {a.next} 도는 중" if a.next else "") + f" · wishlist 에 batch_{nn} 의 n 절"
    print("pushed", push(msg))
    if a.next:
        wt, br = TREES[a.tree]
        dirty = subprocess.run(["git", "-C", wt, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        if dirty:
            print(f"⚠ {wt} 가 깨끗하지 않다:\n{dirty[:400]}")
        r = subprocess.run([sys.executable, "-I", str(SCR / "tools/launch.py"), a.next, wt, br], capture_output=True, text=True)
        if r.returncode:
            sys.exit(r.stdout + r.stderr)
        (SCR / "briefs" / f"prompt_{a.next}.txt").write_text(r.stdout, encoding="utf-8")
        print(f"--- 다음 {a.next} (트리 {a.tree} · 시작 {start}) 지시문 ↓\n{r.stdout}")


if __name__ == "__main__":
    main()
