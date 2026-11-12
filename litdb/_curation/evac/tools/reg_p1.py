#!/usr/bin/env python3
"""reg_p1.py — 본 세션이 넘긴 1 순위 34 편을 대기열 · status.tsv 에 올린다 (한 번 쓰는 도구 · 11-12 인계).

재료 = 인계 묶음 litdb/prompts/ 의 논문별 지시서 19 편 (N-2 … N-35) + _todo_N36_N51.md (N-36 … N-51).
PDF 파일 이름은 이 세션 inbox 의 것 (intake 가 만든 자동 항목의 pdf · si · extra) 을 쓴다.
"""
import json
import re
import sys
from pathlib import Path

SCR = Path(__file__).resolve().parents[1]
PR = SCR / "handoff_20261112/handoff_evac_20261112/litdb/prompts"
QP = SCR / "tools/queue.json"
ST = Path("/home/user/litdb-ctl/litdb/_curation/status.tsv")
Q = json.loads(QP.read_text(encoding="utf-8"))
WANT = [2, 5, 10, 11, 12, 14, 15, 16, 17, 19, 20, 24, 26, 27, 29, 30, 32, 33, 35] + list(range(36, 44)) + list(range(45, 52))
OLD = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad"
info = {}

# ---- 논문별 지시서 (19 편)
for f in sorted(PR.glob("_*_prompt.txt")):
    t = f.read_text(encoding="utf-8")
    m = re.search(r"^이번 논문 \((?:[^)]*?)후보 표 N-(\d+)", t, re.M)
    if not m:
        continue
    n = int(m.group(1))
    L = t.split("\n")
    d = {"src": f.name, "nn": "", "bib": "", "dup": "", "model": "", "model2": "", "note": []}
    keep = False
    for l in L:
        if l.startswith("- 서지 메모:"):
            d["bib"] = l.split(":", 1)[1].strip()
        elif l.startswith("- 중복 확인"):
            d["dup"] = l.split(":", 1)[1].strip() if ":" in l else l[2:].strip()
        elif l.startswith("- 본으로 삼을 카드"):
            mm = re.search(r"litdb/papers/([A-Za-z0-9_]+)\.md", l)
            d["model"] = mm.group(1) if mm else ""
            rest = l.split(".md", 1)[1].strip(" .") if ".md" in l else ""
            d["model2"] = rest
        elif l.startswith("- 정독 출력 NN"):
            d["nn"] = re.search(r"(\d+)", l).group(1)
        elif l.startswith("- PDF") or l.startswith("- 인덱스") or l.startswith("먼저 ") or l.startswith(OLD) or l.startswith("이번 논문"):
            keep = False
        elif l.startswith("- 고른 의도") or l.startswith("- 꼭 뽑을 것") or l.startswith("- ") and keep is not False:
            keep = True
            d["note"].append(l)
        elif keep and l.strip():
            d["note"].append(l)
    info[n] = d

# ---- _todo (N-36 … N-51)
todo = (PR / "_todo_N36_N51.md").read_text(encoding="utf-8")
for sec in re.split(r"^## ", todo, flags=re.M)[1:]:
    m = re.match(r"N-(\d+) · 트리 \d · NN (\d+)", sec)
    if not m:
        continue
    n = int(m.group(1))
    body = [l for l in sec.split("\n")[1:] if l.strip() and not l.startswith("- 파일:") and not l.startswith("- 후보 표 행:")]
    info[n] = {"src": "_todo_N36_N51.md", "nn": m.group(2), "bib": "", "dup": "", "model": "", "model2": "",
               "note": ["- 본 세션이 적어 둔 재료 (지시서는 쓰지 않았다 — 후보 표 행의 '왜' 칸이 고른 의도다):"] + ["  " + l for l in body]}

HEAD = ("- 이 논문은 본 세션 (stoic) 이 맡았던 1 순위 후보다 — 11-12 에 대피 세션이 넘겨받았다. 아래는 본 세션이 써 둔 지시 그대로다 "
        "(그 안의 scratchpad · 트리 경로 · PDF 파일 이름은 본 세션 것이니 이 지시서 머리의 경로 · 파일 이름으로 바꿔 읽는다 · "
        "'다섯 편 공통 지시' = 이 지시서의 공통 지시 절).")
miss = []
for n in WANT:
    k = f"N-{n}"
    if k not in Q:
        miss.append(k)
        continue
    if n not in info:
        miss.append(k + " (지시 재료 없음)")
        continue
    d, q = info[n], Q[k]
    q["nn"] = d["nn"]
    if d["bib"]:
        q["bib"] = d["bib"] + " (본 세션이 적은 서지 메모 — 네가 원문 첫 쪽에서 다시 확인)"
    if d["dup"]:
        q["dup"] = d["dup"] + " — 시작할 때 파일 목록 · DOI · 제1 저자 성으로 한 번 더 확인"
    if d["model"]:
        q["model"] = d["model"]
        if d["model2"]:
            q["model2"] = d["model2"]
    note = [HEAD] + d["note"]
    if q.get("note"):
        note += [q["note"]]
    q["note"] = "\n".join(note)
    q["p1"] = True
if miss:
    sys.exit(f"⛔ 못 올림: {miss}")
QP.write_text(json.dumps(Q, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- status.tsv
L = ST.read_text(encoding="utf-8").split("\n")
i = [j for j, l in enumerate(L) if l.startswith("N-2 · N-5 · ")]
if len(i) != 1:
    sys.exit(f"⛔ 본 세션 '차례 기다림' 묶음 줄을 하나로 못 찾음: {i}")
new = []
for n in WANT:
    q = Q[f"N-{n}"]
    s, e = len(q.get("si", [])), len(q.get("extra", []))
    got = "PDF 받음" + ((" (" + " · ".join(x for x in ((f"+SI {s}" if s else ""), (f"그 밖 {e}" if e else "")) if x) + ")") if s or e else "")
    new.append(f"N-{n}\t대피\t차례 기다림\t\t{got} · 본 세션에서 넘겨받음 (11-12) · 정독 {q['nn']}")
L[i[0]:i[0] + 1] = new
bad = [l[:40] for l in L if l and l.count("\t") != 4]
keys = [l.split("\t")[0] for l in L if l]
dup = sorted({x for x in keys if keys.count(x) > 1})
if bad or dup:
    sys.exit(f"⛔ 칸 수 {bad} · 겹침 {dup}")
ST.write_text("\n".join(L), encoding="utf-8")
print(f"대기열 {len(Q)} 항목 · 1 순위 {len(WANT)} 편 · NN = " + " ".join(f"{n}:{Q[f'N-{n}']['nn']}" for n in WANT))
