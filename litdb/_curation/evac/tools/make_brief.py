#!/usr/bin/env python3
"""make_brief.py — 논문 에이전트 지시서 한 편을 틀에서 만든다 (scratchpad 에만 쓴다).

python3 -I make_brief.py --n N-52 --nn 101 --wt /home/user/litdb-canon --branch tmp-litdb-evac \
    --pdf "<본문 파일 이름>" [--si "<SI 파일 이름>" ...] [--extra "<영상 등 파일 이름>" ...] \
    --bib "<첫 쪽 서지>" --model <본 카드 slug> [--model2 "<덧붙일 본 설명>"] --dup "<중복 확인 결과>" \
    [--note "<이 논문만의 덧붙임>"]
"""
import argparse
import re
import sys
from pathlib import Path

SCR = Path(__file__).resolve().parents[1]
TPL = SCR / "tools" / "AGENT_PROMPT_TEMPLATE.md"
T1 = "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>"
T2 = "Claude-Session: https://claude.ai/code/session_019HKnbzGsY9U5Gyw4qGqqzA"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", required=True)
    ap.add_argument("--nn", required=True)
    ap.add_argument("--wt", required=True)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--si", action="append", default=[])
    ap.add_argument("--extra", action="append", default=[])
    ap.add_argument("--bib", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--model2", default="")
    ap.add_argument("--dup", required=True)
    ap.add_argument("--note", default="")
    ap.add_argument("--row", default="", help="후보 표 행이 아닐 때 그 자리에 넣을 글 (S8 조회를 건너뛴다)")
    a = ap.parse_args()

    wt = Path(a.wt)
    s8 = (wt / "litdb/_curation/S8_candidates.md").read_text(encoding="utf-8").split("\n")
    if a.row:
        row, tail = [a.row], []
    else:
        num = a.n.split("-")[1]
        row = [l for l in s8 if re.match(rf"\| N-{num} \|", l)]
        if len(row) != 1:
            sys.exit(f"⛔ S8 행을 하나로 못 찾음: {a.n} ({len(row)} 개)")
        tail = [l for l in s8 if l.startswith("- ") and re.search(rf"\bN-{num}\b", l)]
    common = (wt / "litdb/_curation/COMMON.md").read_text(encoding="utf-8")
    for f in [a.pdf] + a.si + a.extra:
        if not (wt / "litdb/inbox" / f).is_file():
            sys.exit(f"⛔ inbox 에 없음: {f}")

    si_line = ""
    if a.si:
        si_line += " · 보충 " + " · ".join(f"`{wt}/litdb/inbox/{f}`" for f in a.si)
    if a.extra:
        si_line += " · 그 밖 (영상 등) " + " · ".join(f"`{wt}/litdb/inbox/{f}`" for f in a.extra)
    model = a.model + (f"` (구조 · 절 번호 · 두 필수 절의 본) · 덧붙임: {a.model2} `" if a.model2 else "")
    t = TPL.read_text(encoding="utf-8")
    rep = {
        "{WT}": str(wt), "{LOCAL_BRANCH}": a.branch,
        "{PDF_MAIN}": f"{wt}/litdb/inbox/{a.pdf}", "{PDF_SI_LINE}": si_line,
        "{SCRATCH}": str(SCR), "{N}": a.n, "{NN}": a.nn,
        "{TRAILER_1}": T1, "{TRAILER_2}": T2,
        "{MODEL_CARD}": a.model,
        "{S8_ROW}": row[0], "{S8_TAIL}": ("\n  ".join(tail) if tail else "없음"),
        "{BIB}": a.bib, "{DUP}": a.dup, "{COMMON}": common,
        "{slug}": "<slug>",
    }
    # 첫 줄 제목의 {…} 안내 문구는 그대로 둔다
    head, body = t.split("\n", 1)
    for k, v in rep.items():
        body = body.replace(k, v)
    if a.model2:
        body = body.replace(
            f"`{wt}/litdb/papers/{a.model}.md` (절 번호",
            f"`{wt}/litdb/papers/{a.model}.md` · 덧붙임 = {a.model2} (절 번호")
    if a.note:
        body += "\n## 이 논문만의 덧붙임\n\n" + a.note.strip() + "\n"
    left = re.findall(r"\{[A-Z_0-9]+\}", body)
    if left:
        sys.exit(f"⛔ 안 채운 자리: {sorted(set(left))}")
    out = SCR / "briefs" / f"brief_{a.n}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(f"# 논문 에이전트 지시서 — {a.n} (정독 {a.nn})\n" + body, encoding="utf-8")
    (SCR / f"agent_{a.n}").mkdir(exist_ok=True)
    print(out, len(body.split("\n")), "줄")


if __name__ == "__main__":
    main()
