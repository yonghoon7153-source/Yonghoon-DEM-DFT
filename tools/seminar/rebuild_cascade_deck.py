#!/usr/bin/env python3
"""rebuild_cascade_deck.py — 세미나 덱의 **내용 영역**을 도형 다이어그램에서 실제 그림으로 바꾼다.

무엇을 하나
  Codex 판 덱(`Research_Seminar_2026_08_cascade_human_story.pptx`)은 머리말(제목·용어 띠·
  구분선·불릿·푸터)까지는 좋은데, 내용 영역이 전부 **사각형 + 좌측 액센트 스트라이프 +
  번호 체브론**으로 채워져 있다. 그게 AI 가 만든 티가 나는 부분이고, 정작 우리 계산 그림은
  25장 중 6장에만 들어 있다.

  이 도구는 슬라이드마다 머리말(shape 0–13)은 **손대지 않고**, 내용 영역만 비운 뒤
  지정한 그림을 앉힌다. 그림이 없는 슬라이드는 텍스트만 남겨 깨끗하게 둔다.

이 도구가 **못 하는 것**
  · 슬라이드를 새로 만들거나 순서를 바꾸지 않는다 (`add_slide.py` / `p:sldIdLst` 담당).
  · 머리말 레이아웃이 다른 템플릿에는 못 쓴다 — shape 0–13 이 머리말이라는 것이 전제다.
    다른 덱에 쓰려면 HEADER_N 을 다시 재야 한다.
  · 그림이 슬라이드 주제에 맞는지 판단하지 않는다. SPEC 은 사람이 채운다.
  · 렌더링 확인을 대신하지 않는다 — 이 환경 LibreOffice 가 이 덱을 못 여는 것과 별개로,
    최종 확인은 PowerPoint 에서 사람이 해야 한다.
"""
import copy, sys, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from PIL import Image

#: 머리말 도형 개수 — 이 인덱스 미만은 절대 건드리지 않는다.
HEADER_N = 14
#: ⚠ 표지(1장)는 머리말 배치가 다르다 — 푸터가 21–23 이라 clear_zone 을 쓰면 푸터가 날아간다.
#:    그래서 표지는 인덱스가 아니라 **y 띠**로 체브론만 지운다.
COVER = 1
COVER_BAND = (3.85, 5.15)
#: 내용 영역 (인치)
ZONE = dict(x=0.55, y=2.52, w=8.90, h=3.86)
CAP_Y = 6.46
MUT = RGBColor(0x6b, 0x7d, 0x8f)
FIG = "/home/user/Yonghoon-DEM-DFT/"


def set_text(shape, s):
    """첫 run 의 서식을 유지한 채 텍스트만 교체. `text_frame.text=` 는 서식을 날린다."""
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    if not p0.runs:
        return False
    p0.runs[0].text = s
    for r in p0.runs[1:]:
        r._r.getparent().remove(r._r)
    for p in tf.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    return True


#: Arial 메트릭 호환 폰트 — 폭 측정용 (LibreOffice 가 이 환경에서 pptx 를 못 열어 렌더 QA 가 안 된다)
_FONT_PATHS = ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


def _text_pt(text, pt):
    """text 를 pt 크기로 그렸을 때의 폭(pt). Arial↔Liberation 은 메트릭 호환."""
    from PIL import ImageFont
    for fp in _FONT_PATHS:
        try:
            f = ImageFont.truetype(fp, 200)
            return f.getlength(text) / 200.0 * pt
        except Exception:
            continue
    return len(text) * pt * 0.5          # 폰트가 없으면 보수적 근사


def autofit_line(shape, floor_pt=15.0, step=0.75):
    """상자 한 줄에 들어갈 때까지 글자 크기를 줄인다. 줄여도 안 되면 floor 에서 멈춘다.

    ⚠ 문구는 건드리지 않는다 — 넘치면 **작아지지 삭제되지 않는다.**
    """
    tf = shape.text_frame
    runs = [r for pgh in tf.paragraphs for r in pgh.runs]
    if not runs:
        return None
    text = "".join(r.text for r in runs)
    box_pt = shape.width / 914400 * 72 - 6          # 좌우 안쪽 여백
    cur = (runs[0].font.size.pt if runs[0].font.size else 18.0)
    size = cur
    while size > floor_pt and _text_pt(text, size) > box_pt:
        size -= step
    if size < cur:
        from pptx.util import Pt as _Pt
        for r in runs:
            r.font.size = _Pt(size)
        return (cur, size, _text_pt(text, size) <= box_pt)
    return None


def clear_zone(slide):
    """머리말 뒤 도형을 전부 지운다."""
    shapes = list(slide.shapes)
    for sh in shapes[HEADER_N:]:
        sh._element.getparent().remove(sh._element)


def fit(pw, ph, bx, by, bw, bh):
    """(px,py,pw,ph) 를 박스 안에 비율 유지로 중앙 정렬."""
    s = min(bw / pw, bh / ph)
    w, h = pw * s, ph * s
    return bx + (bw - w) / 2, by + (bh - h) / 2, w, h


def add_pics(slide, paths, zone=ZONE, gap=0.22):
    """1–2장을 내용 영역에 앉힌다. 2장이면 좌우 분할."""
    n = len(paths)
    cell_w = (zone["w"] - gap * (n - 1)) / n
    for i, rel in enumerate(paths):
        p = FIG + rel
        if not os.path.exists(p):
            print(f"    ⚠ 그림 없음: {rel}")
            continue
        with Image.open(p) as im:
            iw, ih = im.size
        bx = zone["x"] + i * (cell_w + gap)
        x, y, w, h = fit(iw, ih, bx, zone["y"], cell_w, zone["h"])
        slide.shapes.add_picture(p, Inches(x), Inches(y), Inches(w), Inches(h))


def add_caption(slide, text, y=CAP_Y):
    tb = slide.shapes.add_textbox(Inches(ZONE["x"]), Inches(y), Inches(ZONE["w"]), Inches(0.44))
    tf = tb.text_frame
    tf.word_wrap = True
    r = tf.paragraphs[0].add_run()
    r.text = text
    f = r.font
    f.size, f.italic, f.color.rgb, f.name = Pt(9.5), True, MUT, "Arial"


def add_statement(slide, text, y=3.6, size=17.5):
    """그림이 없는 장 — 도형 대신 한 문장을 크게."""
    tb = slide.shapes.add_textbox(Inches(1.05), Inches(y), Inches(7.90), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run(); r.text = line
        r.font.size, r.font.color.rgb, r.font.name = Pt(size), RGBColor(0x1f, 0x29, 0x37), "Arial"
        p.space_after = Pt(6)


def add_lines(slide, rows, x=1.05, y=2.75, w=7.9, size=13, lead=0.34, bold_prefix=True):
    """도형 없는 목록 — `제목 :: 본문` 형태를 굵게/보통으로 나눠 찍는다."""
    for i, row in enumerate(rows):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y + i * lead), Inches(w), Inches(lead))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        if bold_prefix and "::" in row:
            head, body = row.split("::", 1)
            r1 = p.add_run(); r1.text = head.strip() + "  "
            r1.font.size, r1.font.bold, r1.font.name = Pt(size), True, "Arial"
            r1.font.color.rgb = RGBColor(0x1f, 0x29, 0x37)
            r2 = p.add_run(); r2.text = body.strip()
            r2.font.size, r2.font.name = Pt(size), "Arial"
            r2.font.color.rgb = RGBColor(0x37, 0x41, 0x51)
        else:
            r = p.add_run(); r.text = row
            r.font.size, r.font.name = Pt(size), "Arial"
            r.font.color.rgb = RGBColor(0x37, 0x41, 0x51)


# ── 슬라이드별 지시 ────────────────────────────────────────────────────────────
L = "litdb/figures/"
D = "docs/figures/"
SPEC = {
 1:  dict(),   # 표지 — 4단 체브론만 걷어낸다 (부제가 이미 같은 말을 한다)
 2:  dict(pics=[L+"kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review/fig_16.png"],
          cap="Kang et al., Chem. Commun. (2026), Fig. 16 — literature map of coupled failure modes. "
              "Green boxes are the three mitigation levers; this work takes the middle one (SE doping). Not our result."),
 3:  dict(keep_pics=True,
          cap="Left: Xiao et al., Joule 3 (2019) 1252, Fig. 1.   Right: Kahle, Marcolongo & Marzari, "
              "Energy Environ. Sci. 13 (2020) 928, Fig. 1.   Both reduce a broad space before spending on accurate methods."),
 4:  dict(pics=[L+"sendek2017_ml_screening_12k_conductors/fig_1.png"],
          cap="Sendek et al., Energy Environ. Sci. 10 (2017) 306, Fig. 1 — physical gates first, then a data model "
              "trained on 40 measured conductors. We borrow the cost-allocation order, not the thresholds."),
 5:  dict(title="The candidate space",
          header="91 chemistries across seven compound families",
          bullets=["Oxides 37 · chlorides 19 · sulfides 10 · fluorides 10 · bromides 5 · nitrides 5 · iodides 4.",
                   "36 cation elements — 32 also appear in the LLZO experimental dopant survey."],
          pics=[D+"cascade/cascade_v23_ptable.png"],
          cap="Our roster on the periodic table. ⚠ Colour is the 2026-06-29 composite snapshot, NOT an approved ranking — "
              "read the block structure (late transition metals sit together), not the order."),
 6:  dict(title="STEP 1 — Dopant sites",
          header="Where can the dopant sit, and what pays for the charge?",
          bullets=["Li, P, S and Cl sublattices are distinct — an oxide needs a cation site and an anion site.",
                   "Aliovalent substitution adds or removes Li, and more than one recipe balances the charge."],
          pics=[D+"site_preference/site_pref_vs_radius.png"],
          cap="Our calculation: which sublattice a dopant prefers, against its ionic radius (UMA antisite swap). "
              "Large cations go to Li sites; group-14 M⁴⁺ substitute P. Bars are the min–max over the three run labels."),
 7:  dict(title="STEP 2 — Configurations",
          pics=[D+"cascade/cascade_v23_anionsite.png"],
          cap="Our calculation: where the dopant anion ends up across the campaign (left), and whether O prefers "
              "the PS₄ corner (right). The site is an outcome of the generator, not an input we controlled."),
 8:  dict(pics=[D+"cascade/cascade_v23_overview.png"],
          cap="Our calculation: relative stability, stiffness and equation-of-state fit quality across the campaign. "
              "⚠ Energies are MLIP-relative within one convention — not formation energies, not hull distances."),
 9:  dict(title="STEP 4 — Representative",
          pics=[D+"cascade/cascade_v23_errorbars_panelA.png"],
          cap="Our calculation: relative stability with its run-to-run band. Where the band is wide, the number from "
              "any single configuration is not the species value — so picking a representative is a choice, not a result."),
 10: dict(statement="A short anneal asks whether the chosen configuration survives being shaken.\n"
                    "It does not produce a diffusion coefficient or a room-temperature conductivity.",
          stmt_y=3.10, stmt_size=17,
          lines=["Why it matters :: bond lengths set everything measured next — Li pathways, stiffness.",
                 "What we ran :: 500 K for 50 ps, then relax again — affordable for the whole campaign.",
                 "What it is not :: an equilibrium structure, and not a synthesis history."],
          lines_y=4.85, lines_size=13.5, lines_lead=0.46),
 11: dict(title="STEP 6 — Li pathways",
          pics=[D+"cascade/bvse_channel_2p5d.png"],
          cap="Our calculation: the static bond-valence landscape a Li ion sees, undoped vs B₂O₃-doped. "
              "Valleys are low-energy regions, not verified channels — this is a risk indicator, not a conductivity."),
 12: dict(title="STEP 7 — Mechanics",
          keep_pics=True,
          cap="Our calculation: one equation-of-state case checked against DFT. ⚠ This is a single-case check — "
              "the campaign-wide elastic numbers are MLIP values compared within one convention, not DFT-verified."),
 13: dict(title="STEP 8 — Oxidation window",
          pics=[D+"cascade/b2o3_esw_staircase.png"],
          cap="Our calculation: the grand-potential stability window and the reaction at each step. "
              "0 K bulk thermodynamics — it says decomposition is allowed, not how fast it happens or whether it passivates."),
 14: dict(pics=[D+"cascade/cascade_v23_esw.png"],
          cap="Our calculation: oxidation window per dopant (left) and onset grouped by cation chemistry (right). "
              "Red × marks a collapsed window — the late transition metals fail together, which is a chemical pattern, not a ranking."),
 15: dict(lines=["COMPUTED :: generated structures · UMA relaxation · representative configurations · short anneal "
                 "· static Li-path proxies · MLIP equation of state and elastic tensor · bulk grand-potential oxidation",
                 "NOT COMPLETED :: real concentration series · same-site multiseed ensembles · canonical softBV for all "
                 "· long multiseed conductivity MD · explicit relaxed interfaces and adhesion · DFT-matched validation"],
          lines_y=2.95, lines_size=13.5, lines_lead=1.15,
          statement="A missing calculation stays missing.\nA proxy does not fill its place.",
          stmt_y=5.35, stmt_size=18),
 16: dict(title="Result 1 — Identity",
          bullets=["59 / 90 species kept the same exact formula across the three labels; 31 / 90 did not.",
                   "So the label-to-label spread mixes site physics, different formulas and local minima."],
          pics=[D+"cascade/label_spread_E_young.png"],
          cap="Our calculation: the three run labels of a single species (grey bar) scatter as widely as different "
              "species do. 59 of 90 species kept the same exact formula across labels; 31 did not. Same name ≠ same material."),
 17: dict(title="Result 2 — Oxidation",
          header="Oxidation shifts are conditional, not a property of the element",
          bullets=["Cl alone does not move the onset; with a dopant already present it moves by up to +0.28 V.",
                   "The same dopant on the same site shifts up or down depending on the charge recipe."],
          pics=[L+"banik2022_substitutions_oxidative_stability_argyrodite/fig_4.png",
                D+"cascade/cascade_oxidation_vs_banik.png"],
          cap="Left: Banik et al. (2022), Fig. 4 — the valence-band edge of Li₆PS₅Cl is sulfur, so sulfur is oxidised first. "
              "Right: our onsets against that thesis. Most sit pinned at the host value; the exceptions are not yet attributable to an element."),
 18: dict(pics=[D+"bv_structure_panels_comp1.png"],
          cap="Our calculation: framework, Li percolation path and bond-valence channel in the undoped host. "
              "The next campaign fixes formula and site on this footing, then repeats seeds inside that fixed design."),
 19: dict(keep_pics=True, extra_pics=[L+"xiao2019_cathode_coating_screening/fig_7.png"],
          cap="Left: Sendek et al. (2017), Fig. 4 — read the training-domain distance on the x-axis, not only the probability. "
              "Right: Xiao et al. (2019), Fig. 7 — more Li lowers the oxidation limit; stability and transport pull against each other."),
 20: dict(lines=["1. What should be calculated first? :: Realistic low-loading multiseed MD, or an explicit cathode / electrolyte interface?",
                 "2. What does “best” mean? :: Best-case configuration, or robust performance across site and seed ensembles?",
                 "3. How much repetition is enough? :: How many seeds and sites before a chemistry is promoted?",
                 "4. Is a bulk-only screen worth handing to experiment? :: Or must the interface be computed before anything is promoted?"],
          lines_y=2.95, lines_size=14, lines_lead=0.78,
          statement="Screen broadly  →  control the comparison  →  validate selectively",
          stmt_y=6.05, stmt_size=17),
 21: dict(keep_pics=True,
          cap="Anderson et al., Adv. Energy Mater. 14 (2024) 2304025, Fig. 1 — the experimental counterpart in LLZO: "
              "59 dopants actually synthesised and measured. Layout reference for our own periodic-table figure."),
 24: dict(lines=["What the three labels are :: three directory names — x002, x005, x010.",
                 "What they actually were :: the same integer substitution in the small cell — x = 0.25 for all three.",
                 "59 / 90 species :: same exact formula across the three labels.",
                 "31 / 90 species :: different exact formulas — different simulated materials under one name."],
          lines_y=2.95, lines_size=13.5, lines_lead=0.62,
          statement="A directory name is not a concentration,\nand three of them are not three replicates.",
          stmt_y=5.60, stmt_size=17),
 25: dict(pics=[L+"sundar2025_oxide_coating_screening_lpscl/fig_2.png"],
          cap="Sundar et al., Adv. Sci. (2025), Fig. 2 — the same coating element scored at four different interfaces. "
              "An element that looks good against the electrolyte can look bad against the anode. We computed none of these four."),
}
# 텍스트만 손보고 내용 영역은 그대로 두는 장
KEEP_ZONE = {22, 23}


def main():
    src, dst = sys.argv[1], sys.argv[2]
    prs = Presentation(src)
    for i, slide in enumerate(prs.slides, 1):
        if i in KEEP_ZONE:
            for j, floor in ((1, 15.0), (5, 12.75)):
                autofit_line(slide.shapes[j], floor_pt=floor)
            continue
        spec = SPEC.get(i)
        if spec is None:
            # 지시 없는 장 — 좌측 스트라이프/체브론만 정리
            for sh in list(slide.shapes)[HEADER_N:]:
                w, h = sh.width / 914400, sh.height / 914400
                if w <= 0.12 and h >= 0.5:      # 좌측 액센트 스트라이프
                    sh._element.getparent().remove(sh._element)
            for j, floor in ((1, 15.0), (5, 12.75)):
                autofit_line(slide.shapes[j], floor_pt=floor)
            print(f"  P{i:2d} 스트라이프 정리 + 제목 맞춤")
            continue

        kept = []
        if spec.get("keep_pics"):
            kept = [sh for sh in slide.shapes if sh.__class__.__name__ == "Picture"]
            for sh in list(slide.shapes)[HEADER_N:]:
                if sh not in kept:
                    sh._element.getparent().remove(sh._element)
            for sh in kept:                      # 캡션 자리 확보
                if sh.top / 914400 + sh.height / 914400 > CAP_Y - 0.12:
                    sh.height = int((CAP_Y - 0.16 - sh.top / 914400) * 914400)
        elif i == COVER:
            for sh in list(slide.shapes):
                yy = sh.top / 914400
                if COVER_BAND[0] <= yy <= COVER_BAND[1]:
                    sh._element.getparent().remove(sh._element)
        else:
            clear_zone(slide)

        if spec.get("title"):
            set_text(slide.shapes[1], spec["title"])
        if spec.get("header"):
            set_text(slide.shapes[5], spec["header"])
        for k, b in enumerate(spec.get("bullets", [])):
            set_text(slide.shapes[7 + k * 2], b)

        if spec.get("extra_pics"):               # 기존 그림 옆에 추가
            n = len(kept) + len(spec["extra_pics"])
            gap = 0.22
            cw = (ZONE["w"] - gap * (n - 1)) / n
            for j, sh in enumerate(kept):
                bx = ZONE["x"] + j * (cw + gap)
                x, y, w, h = fit(sh.width, sh.height, bx, ZONE["y"], cw, ZONE["h"])
                sh.left, sh.top, sh.width, sh.height = (Inches(x), Inches(y), Inches(w), Inches(h))
            for j, rel in enumerate(spec["extra_pics"], start=len(kept)):
                p = FIG + rel
                with Image.open(p) as im:
                    iw, ih = im.size
                bx = ZONE["x"] + j * (cw + gap)
                x, y, w, h = fit(iw, ih, bx, ZONE["y"], cw, ZONE["h"])
                slide.shapes.add_picture(p, Inches(x), Inches(y), Inches(w), Inches(h))
        if spec.get("pics"):
            add_pics(slide, spec["pics"])
        if spec.get("lines"):
            add_lines(slide, spec["lines"], y=spec.get("lines_y", 2.75),
                      size=spec.get("lines_size", 13), lead=spec.get("lines_lead", 0.34))
        if spec.get("statement"):
            add_statement(slide, spec["statement"], y=spec.get("stmt_y", 3.6),
                          size=spec.get("stmt_size", 17.5))
        if spec.get("cap"):
            add_caption(slide, spec["cap"])
        for j, floor in (() if i == COVER else ((1, 15.0), (5, 12.75))):   # 제목·구역 헤더는 한 줄 유지
            r = autofit_line(slide.shapes[j], floor_pt=floor)
            if r:
                print(f"      · shape[{j}] {r[0]:.2f}→{r[1]:.2f} pt" + ("" if r[2] else "  ⚠ 여전히 넘침"))
        print(f"  P{i:2d} 재구성 (pics={len(spec.get('pics',[]))+len(spec.get('extra_pics',[]))+len(kept)})")

    prs.save(dst)
    print(f"\n저장: {dst}")


def selftest():
    ok = fail = 0
    def chk(name, cond):
        nonlocal ok, fail
        if cond: ok += 1
        else:
            fail += 1; print(f"  ✗ {name}")
    # 양성 — 비율 유지 맞춤
    x, y, w, h = fit(200, 100, 0, 0, 8, 4)
    chk("가로가 꽉 차는 경우", abs(w - 8) < 1e-9 and abs(h - 4) < 1e-9)
    x, y, w, h = fit(100, 200, 0, 0, 8, 4)
    chk("세로가 꽉 차는 경우", abs(h - 4) < 1e-9 and abs(w - 2) < 1e-9)
    chk("세로 맞춤 시 가로 중앙", abs(x - 3.0) < 1e-9)
    # 음성 ① — 박스를 넘치면 안 된다
    for pw, ph in ((3000, 40), (40, 3000), (1, 1), (1920, 1080)):
        x, y, w, h = fit(pw, ph, 0.5, 2.5, 8.9, 3.86)
        chk(f"음성: {pw}x{ph} 박스 이탈 없음",
            w <= 8.9 + 1e-9 and h <= 3.86 + 1e-9 and x >= 0.5 - 1e-9 and y >= 2.5 - 1e-9)
    # 음성 ② — 머리말을 건드리면 안 된다
    chk("음성: HEADER_N 이 푸터(13)보다 크다", HEADER_N > 13)
    # 음성 ③ — 캡션이 푸터(7.11)를 침범하면 안 된다
    chk("음성: 캡션이 푸터 위", CAP_Y + 0.44 < 7.11)
    # 음성 ④ — 내용 영역이 구분선(0.86)/캡션과 겹치면 안 된다
    chk("음성: 영역이 머리말 아래", ZONE["y"] > 2.2)
    chk("음성: 영역이 캡션 위에서 끝난다", ZONE["y"] + ZONE["h"] <= CAP_Y + 1e-9)
    # 음성 ⑤ — SPEC 이 가리키는 그림이 실제로 있어야 한다
    miss = [p for s in SPEC.values() for p in (s.get("pics", []) + s.get("extra_pics", []))
            if not os.path.exists(FIG + p)]
    chk(f"음성: 없는 그림 참조 0건 ({miss[:2]})", not miss)
    # 음성 ⑥ — KEEP_ZONE 과 SPEC 이 겹치면 안 된다 (지웠다 살리는 모순)
    chk("음성: KEEP_ZONE 과 SPEC 배타", not (KEEP_ZONE & set(SPEC)))
    # 음성 ⑨ — 표지 띠가 푸터(7.09)·부제(5.57)를 건드리면 안 된다
    chk("음성: 표지 띠가 부제 위에서 끝난다", COVER_BAND[1] < 5.5)
    chk("음성: 표지 띠가 푸터를 안 건드린다", COVER_BAND[1] < 7.0)
    chk("음성: 표지에는 그림 지시가 없다", not SPEC.get(COVER, {}).get("pics"))
    # 음성 ⑦ — 제목/헤더/불릿이 한 줄 상자를 넘치면 안 된다 (2026-08-16 mock 렌더 실측 한도)
    LIM = dict(title=26, header=66)
    over = [(n, k, len(sp_[k])) for n, sp_ in SPEC.items() for k, lim in LIM.items()
            if sp_.get(k) and len(sp_[k]) > lim]
    chk(f"음성: 제목·헤더 길이 초과 0건 ({over[:2]})", not over)
    ob = [(n, len(b)) for n, sp_ in SPEC.items() for b in sp_.get("bullets", []) if len(b) > 95]
    chk(f"음성: 불릿 길이 초과 0건 ({ob[:2]})", not ob)
    # 음성 ⑧ — 폭 측정이 단조인가 (크기를 키우면 폭도 커져야 축소 루프가 종료된다)
    chk("음성: 폭이 pt 에 단조 증가", _text_pt("abc", 24) > _text_pt("abc", 12) > 0)
    chk("음성: 긴 문자열이 더 넓다", _text_pt("a" * 40, 18) > _text_pt("a" * 10, 18))
    chk("음성: 빈 문자열 폭 0", _text_pt("", 18) == 0)
    print(f"\nselftest: {ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    raise SystemExit(main() or 0)
