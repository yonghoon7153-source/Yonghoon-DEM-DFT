#!/usr/bin/env python3
"""talk_transcript.py — 발표 **녹취(STT)** 를 digest 가 쓸 수 있는 꼴로 정리한다.

왜 이 파일인가 (2026-08-25)
  `litdb/talks/` 의 기존 5편은 **덱만** 있었다. 심포지엄 세션부터는 **음성 녹취**가 같이
  들어온다 — 그리고 녹취가 덱보다 값어치 있는 경우가 많다: 슬라이드에 안 쓰인
  **전문가의 판단·단서·"실제로는 이렇다"** 가 거기 있기 때문이다.

  그런데 STT 는 전문용어를 심하게 망가뜨린다(실측: `오승목`=오승모 ·
  `셀 코리라리제이션`=cell polarization · `a미타`=η · `IR 포탈`=IR drop).
  **오탈자를 고치지 않고 인용하면 없는 말을 만든 것**이 되므로, 이 도구는
  ① 시간축을 살려 블록으로 자르고 ② **오탈자 의심 구간을 표시**하고
  ③ 슬라이드와 맞출 **빈 표**를 만들어 준다.

이 도구가 **하지 않는 것** (중요)
  · **자동 정렬을 하지 않는다.** 심포지엄 자료집 PDF 는 대개 텍스트 레이어가 없는
    스캔이라(실측 0자) 키워드 매칭이 불가능하다. 슬라이드는 **사람/에이전트가 눈으로**
    읽고 맞춰야 한다. 이 도구는 그 표의 **뼈대만** 만든다.
  · **오탈자를 자동으로 고치지 않는다.** 후보를 제시할 뿐 — 무엇이 맞는지는
    슬라이드를 봐야 안다. 조용히 고치면 근거 없는 창작이 된다.
  · 화자 분리의 정확성을 보증하지 않는다 (STT 가 준 라벨을 옮길 뿐).

    python3 tools/litdb/talk_transcript.py --txt <녹취> --slug <slug>
    python3 tools/litdb/talk_transcript.py --txt <녹취> --slug <slug> --minutes 5
    python3 tools/litdb/talk_transcript.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_ROOT = os.path.join(ROOT, "litdb", "talks", "_transcripts")

#: STT 가 전문용어를 망가뜨린 실측 사례. **자동 치환하지 않는다** — 후보만 띄운다.
#: (2026-08-25 오승모 튜토리얼에서 실제로 나온 것들)
SUSPECT = [
    (r"코리라리제이션|콜라리제이션|콜라겐|코라리제이션", "polarization (분극)"),
    (r"a\s*미타|에이타|이타\b", "η (overpotential)"),
    (r"IR\s*포탈|아이알\s*포탈|IR\s*드랍", "IR drop"),
    (r"네른스트|넌스트|너스트", "Nernst"),
    (r"인터칼레이[션숀]|인터컬레이션", "intercalation"),
    (r"임피던[스쓰]|임피던시", "impedance"),
    (r"컨버[전젼]|컨벡션", "convection / conversion (문맥 확인)"),
    (r"디퓨[전젼]|디퓨션", "diffusion"),
    (r"익스체인지\s*커런트", "exchange current"),
    (r"타펠|터펠", "Tafel"),
    (r"쿨롱\s*효율|쿨롬빅", "Coulombic efficiency"),
    (r"에스오씨|에스오시", "SOC"),
    (r"씨\s*레이[트를]|C\s*레이트", "C-rate"),
]

_TS = re.compile(r"^\s*(참석자\s*\d+|화자\s*\d+|[A-Za-z가-힣]+)\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*$")


def parse(text):
    """녹취 → [{t_sec, speaker, text}]. 타임스탬프 줄을 경계로 자른다.

    ⚠ 형식은 STT 도구마다 다르다. 지금 받는 꼴은 `참석자 1 12:34` 한 줄 뒤에 본문이
      오는 형태다. 못 읽으면 **조용히 0개를 주지 말고** 그렇게 말해야 한다.
    """
    blocks, cur = [], None
    for ln in text.splitlines():
        m = _TS.match(ln)
        if m:
            if cur:
                blocks.append(cur)
            h, mm, ss = m.group(2), m.group(3), m.group(4)
            t = int(h) * 60 + int(mm) if ss is None else int(h) * 3600 + int(mm) * 60 + int(ss)
            cur = {"t_sec": t, "speaker": m.group(1).strip(), "text": ""}
        elif cur is not None:
            cur["text"] += (" " if cur["text"] else "") + ln.strip()
    if cur:
        blocks.append(cur)
    for b in blocks:
        b["text"] = " ".join(b["text"].split())
    return [b for b in blocks if b["text"]]


def suspects(blocks):
    """오탈자 의심 구간. **고치지 않고 위치와 후보만** 돌려준다."""
    out = []
    for i, b in enumerate(blocks):
        for pat, why in SUSPECT:
            for m in re.finditer(pat, b["text"]):
                out.append({"block": i, "t_sec": b["t_sec"],
                            "found": m.group(0), "likely": why,
                            "context": b["text"][max(0, m.start() - 30):m.end() + 30]})
    return out


def fmt(t):
    return f"{t // 60:02d}:{t % 60:02d}" if t < 3600 else f"{t // 3600}:{(t % 3600) // 60:02d}:{t % 60:02d}"


def chapters(blocks, minutes=5):
    """N 분 단위로 묶어 **훑을 수 있는 목차**를 만든다 (정렬 표의 행이 된다)."""
    if not blocks:
        return []
    step = minutes * 60
    out, cur = [], None
    for b in blocks:
        k = b["t_sec"] // step
        if cur is None or cur["bucket"] != k:
            if cur:
                out.append(cur)
            cur = {"bucket": k, "t_start": b["t_sec"], "t_end": b["t_sec"],
                   "n_blocks": 0, "head": b["text"][:120]}
        cur["t_end"] = b["t_sec"]
        cur["n_blocks"] += 1
    if cur:
        out.append(cur)
    return out


def render_scaffold(slug, blocks, chs, sus, slides=None):
    """digest 에 붙일 **정렬 표 뼈대**. 슬라이드 칸은 비워 둔다 — 사람이 채운다."""
    L = [f"## 슬라이드 ↔ 녹취 정렬  ({slug})", "",
         "> ⚠ 이 표는 **뼈대**다. 슬라이드 칸은 자동으로 못 채운다 — 자료집 PDF 에",
         "> 텍스트 레이어가 없어(스캔) 키워드 매칭이 불가능하다. **그림을 실제로 보고** 채운다.",
         "> 채우지 않은 행은 지우지 말고 `?` 로 남긴다 — 빈칸이 곧 '아직 안 봤다' 는 기록이다.",
         "",
         "| 시각 | 슬라이드 | 무엇을 말했나 | 슬라이드에 없는 말인가 |",
         "|---|---|---|---|"]
    for c in chs:
        L.append(f"| {fmt(c['t_start'])}–{fmt(c['t_end'])} | ? | {c['head'][:70]}… | ? |")
    L += ["", f"총 {len(blocks)} 블록 · {fmt(blocks[-1]['t_sec']) if blocks else '—'} 분량",
          ""]
    if sus:
        L += ["## ⚠ STT 오탈자 의심 " + f"({len(sus)}건)", "",
              "> **자동으로 고치지 않았다.** 슬라이드를 보고 확정한 뒤 digest 본문에서 쓸 것.",
              "> 고치기 전에는 인용하지 않는다 — 없는 말을 만들게 된다.", "",
              "| 시각 | 들린 것 | 아마도 | 문맥 |", "|---|---|---|---|"]
        seen = set()
        for s in sus:
            k = (s["found"], s["likely"])
            if k in seen:
                continue
            seen.add(k)
            L.append(f"| {fmt(s['t_sec'])} | `{s['found']}` | {s['likely']} | …{s['context']}… |")
        L.append("")
    return "\n".join(L)


def _selftest():
    ok = True

    def say(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok = ok and c

    print("── talk_transcript selftest ──")
    txt = ("제목\n2026.08.25\n\n참석자 1 00:00\n안녕하세요\n\n"
           "참석자 2 02:15\n셀 코리라리제이션이 뭐냐 하면 a미타 더하기 IR 포탈입니다\n"
           "이어지는 줄\n\n참석자 1 1:05:30\n마지막\n")
    b = parse(txt)
    say(len(b) == 3, f"① 블록 3개로 잘린다 (얻은 값 {len(b)})")
    say(b[1]["t_sec"] == 135, f"① mm:ss → 초 (135 기대, {b[1]['t_sec']})")
    say(b[2]["t_sec"] == 3930, f"① h:mm:ss 도 읽는다 (3930 기대, {b[2]['t_sec']})")
    say("이어지는 줄" in b[1]["text"], "① 여러 줄이 한 블록으로 합쳐진다")
    # [음성] 타임스탬프가 없으면 **조용히 0개** 가 아니라 0개임이 드러나야 한다
    say(parse("아무 형식도 아닌 글") == [], "② [음성] 형식이 다르면 빈 리스트 (지어내지 않는다)")
    s = suspects(b)
    found = {x["likely"] for x in s}
    say("polarization (분극)" in found and "η (overpotential)" in found
        and "IR drop" in found, f"③ 오탈자 3종을 잡는다 ({sorted(found)})")
    # [음성] **자동 치환하지 않는다** — 원문이 그대로여야 한다
    say("코리라리제이션" in b[1]["text"], "③ [음성] 원문을 고치지 않는다 (후보만 제시)")
    ch = chapters(b, minutes=5)
    say(len(ch) >= 2, f"④ 5분 묶음 목차 ({len(ch)}개)")
    md = render_scaffold("t", b, ch, s)
    say("슬라이드" in md and "| ? |" in md, "⑤ 정렬 표 뼈대에 빈칸(?)이 남는다")
    say("자동으로 고치지 않았다" in md, "⑤ 오탈자 표에 '고치지 않았다' 가 명시된다")
    say(fmt(135) == "02:15" and fmt(3930) == "1:05:30", "⑥ 시각 표기")
    print("  " + ("✅ selftest 통과" if ok else "⛔ selftest 실패"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--txt", help="STT 녹취 파일")
    ap.add_argument("--slug", help="litdb/talks slug")
    ap.add_argument("--minutes", type=int, default=5, help="목차 묶음 단위 (기본 5분)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.txt and a.slug):
        ap.error("--txt 와 --slug 가 필요하다 (또는 --selftest)")
    text = open(a.txt, encoding="utf-8-sig", errors="replace").read()
    blocks = parse(text)
    if not blocks:
        print("⛔ 타임스탬프 블록을 하나도 못 읽었다 — 녹취 형식이 다르다.")
        print("   지금 지원하는 꼴:  `참석자 1 12:34` 한 줄 뒤에 본문")
        print("   앞 5줄:")
        for ln in text.splitlines()[:5]:
            print("     " + ln[:90])
        return 1
    sus, chs = suspects(blocks), chapters(blocks, a.minutes)
    os.makedirs(OUT_ROOT, exist_ok=True)
    jp = os.path.join(OUT_ROOT, f"{a.slug}.json")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump({"slug": a.slug, "n_blocks": len(blocks),
                   "duration_sec": blocks[-1]["t_sec"],
                   "blocks": blocks, "suspects": sus, "chapters": chs},
                  f, ensure_ascii=False, indent=1)
    mp = os.path.join(OUT_ROOT, f"{a.slug}_scaffold.md")
    with open(mp, "w", encoding="utf-8") as f:
        f.write(render_scaffold(a.slug, blocks, chs, sus))
    print(f"✓ 블록 {len(blocks)} · 길이 {fmt(blocks[-1]['t_sec'])} · "
          f"오탈자 의심 {len(sus)}건 ({len({x['likely'] for x in sus})}종)")
    print(f"  → {os.path.relpath(jp, ROOT)}")
    print(f"  → {os.path.relpath(mp, ROOT)}   (digest 에 붙일 뼈대)")
    print("  ⚠ 슬라이드 칸은 **비어 있다** — 그림을 보고 채울 것. 자동 정렬은 하지 않는다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
