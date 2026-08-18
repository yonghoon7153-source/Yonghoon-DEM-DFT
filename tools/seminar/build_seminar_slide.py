#!/usr/bin/env python3
"""build_seminar_slide.py — 세미나 덱의 한 장을 단독 파일로 다시 만든다.

  python3 tools/seminar/build_seminar_slide.py 8
  python3 tools/seminar/build_seminar_slide.py 9
  python3 tools/seminar/build_seminar_slide.py --selftest

왜 한 도구인가 — 8·9장이 **같은 머리말 골격**(도형 0–13)을 쓴다. 장마다 파일을
  만들면 레이아웃 수정을 N 번 해야 하고, 실제로 8장에서 고친 세 가지(용어줄 위치·
  중복 각주·글자폭)가 9장에 그대로 남아 있었다. 문장만 SLIDES 에 둔다.

8장 배경 (2026-08-18)

왜 (2026-08-18)
  v6 덱의 8장에 세 가지 문제가 있었다. 전부 **화면에서 눈으로 보이는** 것들이다:
    ① 용어 설명줄(shape 2)이 헤더 불릿(shape 5) 위에 올라타고 오른쪽이 잘렸다
       — `how many compounds of that eleme` 에서 끊겼다.
    ② 같은 단서("superseded snapshot")가 **세 번** 나왔다: 소불릿 · 그림 밑 빨간 줄 ·
       맨 아래 이탤릭. 그 이탤릭도 잘려서 `current rank ing is 0 species` 로 보였다.
    ③ 색이 47종 풀(2026-06-29)이었다. 89종 풀로 바꾸면서 캡션도 같이 가야 한다.

  ⚠ 소불릿의 "superseded snapshot" 은 **변명**이었다. 89종으로 다시 매겨도 상·하위
    집합이 그대로라는 실측이 나왔으므로(카드 아래 참조), 이제 근거 있는 문장으로 바꾼다.

  python3 tools/seminar/build_slide08_periodic.py --selftest
  python3 tools/seminar/build_slide08_periodic.py

⚠ PowerPoint 자동서식 주의 (2026-08-18 실측)
  빌더가 쓴 것은 평범한 run 이라 그대로 나온다. 그런데 **PowerPoint 안에서 다시 타이핑**하면
  `A 2+ dopant` 의 `2+` 가 위첨자로 올라가 **A²⁺**(원소 A 의 2가 이온)처럼 보인다.
  → 이 파일에서 만든 슬라이드는 **복사해 붙이고, 그 줄을 다시 치지 않는다.**
     (1저자 판단 2026-08-18: 문구는 `A 2+` 로 유지하고 입력 쪽에서 처리한다.)

이 도구가 못 하는 것
  · 점수를 다시 매기지 않는다. 그림은 plot_seminar_2026_08.fig_periodic 이 만든다.
  · 원본 덱(v6)을 고치지 않는다 — 단독 파일만 만든다. 덱 반영은 사람이 붙여넣는다.
  · 머리말 도형(0–13)의 위치를 바꾸지 않는다. 로고·푸터 규약을 건드리면 안 된다.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "seminar"))

SRC = os.path.join(ROOT, "docs", "Research_Seminar_2026_08_cascade_story_v6.pptx")
SCRIPT = os.path.join(ROOT, "kb", "seminars", "cascade_dopant_screening_story_2026_08.md")

#: 장별 문장 — 대본(kb/seminars/…)과 **1:1**이어야 한다. selftest 가 대조한다.
#: idx 는 0-based (덱의 N 장 = idx N-1). fig 는 repo 루트 기준 (add_pics 규약).
SLIDES = {
 8: dict(
    idx=7, out="Slide08_periodic_table.pptx",
    fig="docs/figures/seminar/roster_periodic_table.png",
    zone=dict(x=0.55, y=2.28, w=8.90, h=3.62),
    title="Candidate set on the periodic table",
    head="Candidate set (2): 36 cation elements, colored by their best score",
    sub1="Late transition metals (Fe–Cu) form the [r]red[/r] block — their oxidation window is the narrowest.",
    sub2="[b]Group trends[/b] are robust, the exact order is not — the same elements stay at both ends.",
    label="best score per element, 89-species pool (2026-08-13)",
    note="[r]no approved ranking yet[/r] — the same elements stayed top and bottom when the set doubled (47 → 89)",
    gloss=("Cation: the metal we substitute in  ·  Coverage: how many compounds of that element "
           "were scored  ·  de: stability against the host"),
    drop=[10],
 ),
 9: dict(
    idx=8, out="Slide09_site_and_charge.pptx",
    fig="docs/figures/seminar/step1_site_choice.png",
    zone=dict(x=0.55, y=2.28, w=8.90, h=3.62),
    title="Substitution site and charge compensation",
    head="Step 1: The substitution site is enumerated before a structure is built",
    sub1="Li, P, S and Cl are separate sublattices — an oxide has to take [b]one cation and one anion site[/b].",
    sub2="A 2+ dopant on a Li site leaves extra charge — [r]each way of balancing it is a different structure[/r].",
    label="site preference vs ionic radius",
    note="only Si always takes the P framework; 19 of 26 always take Li — [r]6 switch with the doping level[/r]",
    gloss=("Sublattice: equivalent positions of one element  ·  Charge compensation: adding "
           "or removing Li to keep the cell neutral  ·  bars = three doping levels, not repeat runs"),
    drop=[10],
 ),
 10: dict(
    idx=9, out="Slide10_structure_generation.pptx",
    figs=["docs/figures/seminar/step2_anion_site.png",
          "docs/figures/seminar/step2_site_grid.png"],
    zone=dict(x=0.55, y=2.42, w=8.90, h=3.34),
    title="Candidate structure generation",
    head="Step 2: Each allowed placement becomes a separate structure",
    sub1="One compound became [b]30 structures[/b] on average, and 3,615 in total.",
    sub2="The winning site is [r]an output of the generator[/r], not a variable that was set.",
    label="where the anion landed  ·  structures per site pair",
    note="all nine site pairs were populated — [r]the site was never fixed by design[/r]",
    gloss=("Configuration: one specific arrangement of atoms in the cell  ·  "
           "24g / 48h / 4b / 4a / 16e / 4d: Wyckoff labels for the sublattice positions"),
    drop=[10],
 ),
}


def keep_one_slide(prs, idx):
    """prs 에서 idx 한 장만 남긴다.

    ⚠ python-pptx 에 슬라이드 삭제 API 가 없다. sldIdLst 항목을 지우고 관계도 같이
      끊어야 한다 — 관계를 안 끊으면 파일이 열리긴 하나 고아 파트가 남는다.
    """
    xml_slides = prs.slides._sldIdLst
    keep = list(xml_slides)[idx]
    for sld in list(xml_slides):
        if sld is not keep:
            prs.part.drop_rel(sld.rId)
            xml_slides.remove(sld)
    return prs.slides[0]


def build(n):
    from pptx import Presentation
    from pptx.util import Inches
    import rebuild_cascade_deck as M

    S = SLIDES[n]
    prs = Presentation(SRC)
    sl = keep_one_slide(prs, S["idx"])
    M.clear_zone(sl)                       # 14번 이후(그림·캡션·각주) 전부 정리

    M.set_text(sl.shapes[1], S["title"])
    M.set_text(sl.shapes[5], S["head"])
    M.set_text(sl.shapes[7], S["sub1"])
    M.set_text(sl.shapes[9], S["sub2"])

    # ① 용어줄을 **맨 아래로** — 원래 (5.02, 0.94) 라 헤더 불릿 위에 올라타 잘렸다.
    g = sl.shapes[2]
    g.left, g.top, g.width, g.height = Inches(0.57), Inches(6.86), Inches(8.86), Inches(0.24)
    M.set_text(g, S["gloss"])

    # ② 오른쪽 이탤릭 주석은 지운다 — 그림 밑 이름표와 같은 말이다.
    for i in sorted(S.get("drop", []), reverse=True):
        sl.shapes[i]._element.getparent().remove(sl.shapes[i]._element)

    M.add_pics(sl, S["figs"] if "figs" in S else [S["fig"]], zone=S["zone"])
    M.add_fig_label(sl, S["label"], 0.55, 5.96, 8.90)
    M.add_fig_note(sl, S["note"], 0.55, 6.30, 8.90, size=11.5)

    out = os.path.join(ROOT, "docs", S["out"])
    prs.save(out)
    return out


def selftest():
    ok = fail = 0

    def chk(c, m):
        nonlocal ok, fail
        if c:
            ok += 1; print(f"  ✓ {m}")
        else:
            fail += 1; print(f"  ✗ {m}")

    import re as _re
    from pptx import Presentation
    import rebuild_cascade_deck as M

    def plain(t):
        # 강조 표기가 두 벌이다: 덱 [r]/[b] · 대본 [빨강]/[파랑]. 닫는 쪽은 빈 토큰 `[/]`.
        return _re.sub(r"\[/?(?:r|b|빨강|파랑)?\]", "", t)

    chk(os.path.exists(SRC), f"원본 덱이 있다 ({os.path.basename(SRC)})")
    body = plain(open(SCRIPT, encoding="utf-8").read()) if os.path.exists(SCRIPT) else ""
    src = Presentation(SRC)

    for n, S in sorted(SLIDES.items()):
        figs = S["figs"] if "figs" in S else [S["fig"]]
        for f in figs:
            chk(os.path.exists(os.path.join(ROOT, f)),
                f"{n}장 그림이 있다 ({os.path.basename(f)})")
            # 음성 — add_pics 는 repo 루트 기준. 경로가 틀리면 **조용히 건너뛴다**
            chk(f.startswith("docs/"), f"{n}장 그림 경로가 repo 루트 기준")

        # 대본과 1:1 — 헤더·이름표·소불릿까지
        chk(S["head"] in body, f"{n}장 헤더가 대본에도 있다")
        for tag in ("sub1", "sub2"):
            key = plain(S[tag]).split(" — ")[0].split(";")[0].strip()
            chk(key in body, f"{n}장 {tag} 가 대본에도 있다 ('{key[:30]}…')")

        # ★ 글자폭 — 넘치면 두 줄로 감겨 그림을 밀거나 잘린다.
        #   v6 8·9장의 용어줄이 그래서 `of that eleme` 에서 끊겼다.
        for tag, w_in, pt in (("head", 8.49, 17.2), ("sub1", 7.92, 12.8),
                              ("sub2", 7.92, 12.8), ("gloss", 8.86, 8.6),
                              ("note", 8.90, 11.5)):
            w = M._text_pt(plain(S[tag]), pt) / 72.0
            chk(w < w_in - 0.15, f"{n}장 {tag} 한 줄에 들어간다 ({w:.2f} < {w_in} in)")

        # 음성 — 지울 도형이 정말 그 주석인지 (번호로 지우므로 확인이 필수)
        sl = src.slides[S["idx"]]
        for i in S.get("drop", []):
            t = sl.shapes[i].text_frame.text if sl.shapes[i].has_text_frame else ""
            chk(len(t) < 60 and ("Our" in t or "·" in t),
                f"{n}장 지울 shape[{i}] 이 짧은 주석이다 ('{t[:30]}')")
        # 용어줄은 "낱말: 뜻 · 낱말: 뜻" 꼴이다. 낱말을 목록으로 두면 장마다 고쳐야 하므로
        # **모양**으로 본다 — 콜론과 가운뎃점이 있고, 문장이 아니라 정의 나열.
        _t2 = sl.shapes[2].text_frame.text
        chk(":" in _t2 and "·" in _t2 and len(_t2) > 40,
            f"{n}장 옮길 shape[2] 가 용어줄이다 ('{_t2[:34]}…')")

    # 음성 — 영국식 철자가 슬라이드 문장에 섞이면 안 된다 (1저자 지적 2026-08-18)
    allt = " ".join(plain(v) for S in SLIDES.values() for k, v in S.items()
                    if isinstance(v, str))
    brit = [w for w in ("coloured", "colour", "centre", "labelled", "analyse",
                        "behaviour", "normalise") if w in allt.lower()]
    chk(not brit, f"음성: 영국식 철자 없음 ({brit})")

    print(f"\nselftest: {ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    args = [a for a in sys.argv[1:] if a.isdigit()]
    todo = [int(a) for a in args] or sorted(SLIDES)
    for n in todo:
        if n not in SLIDES:
            raise SystemExit(f"⛔ {n}장은 SLIDES 에 없다 (있는 것: {sorted(SLIDES)})")
        print("→", build(n))
