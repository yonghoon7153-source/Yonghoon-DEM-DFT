#!/usr/bin/env python3
"""NMR 화학적 이동 설명 그림 7 장 (SVG) — webapp 용어집 '더보기' (kb/concepts/nmr_shift.md) 용.

    python3 tools/figures/build_nmr_shift_figures.py            # docs/figures/nmr_shift/*.svg 를 쓴다
    python3 tools/figures/build_nmr_shift_figures.py --selftest # 양성 + 음성 (파일을 안 쓴다)

그림은 개념 모식도다 — 데이터 그림이 아니라 Origin CSV 를 안 낸다.
  01 스핀 세차 · 02 공명 · 03 차폐 · 04 ppm 축 (up-field) · 05 ⁷Li 이동 · 06 ³¹P 이동 (방향만) · 07 Nd³⁺ 상자성
색은 tools/figures/house_style.py (INK · MUT · ELEM) · 그림 안 글자는 영어만 (하우스 규약 · 사용자 뷰어 한글 깨짐).

검사 (selftest · 그림을 쓸 때마다도 돈다):
  ① SVG 가 XML 로 읽힌다 ② 글자 노드에 한글이 없다 ③ ⁷Li 그림의 두 봉우리 꼭대기가 축 눈금으로 원고 문장 숫자
  (1.48 · 1.16 ppm) 자리에 있고, 인쇄된 숫자도 그 둘이다 (그림과 글자가 따로 놀면 잡는다).
음성: 한글 라벨 · 봉우리를 1.40 으로 옮김 · 인쇄 숫자만 바꿈 · 깨진 XML — 넷 다 잡혀야 한다.

이 도구가 못 하는 것:
  · NMR 을 계산하지 않는다 — 봉우리 모양 · 폭은 임의다 (Lorentzian · FWHM 0.30 ppm). 위치만 원고 문장 숫자에 맞췄다.
  · ⁷Li 숫자 (1.48 · 1.16) 는 NdO-LPSCl1.6 원고 문장에 적힌 값이다 — 우리 계산값이 아니다. ³¹P 그림에는 숫자가 없다.
  · 그림을 webapp 에 붙이는 것은 kb/concepts/nmr_shift.md 의 이미지 줄이다 (/api/file/docs/figures/nmr_shift/…).
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.figures.house_style import ELEM, INK, MUT  # noqa: E402

OUT = ROOT / "docs" / "figures" / "nmr_shift"
FIELD = ELEM["N"]          # 자기장 화살표 (#2563eb)
CLOUD = "#cfe8e5"          # 전자 구름 (Li 청록의 옅은 판)
LINE = "#d3dcdc"
WHITE = "#ffffff"
LI_EXPECTED = {"li-a": 1.48, "li-b": 1.16}   # 원고 문장 숫자 (LPSCl1.6 → NdO-LPSCl1.6)

STYLE = f"""<style>
text{{font-family:"DejaVu Sans","Helvetica Neue",Arial,sans-serif;font-size:15px;fill:{INK}}}
.mono{{font-family:"DejaVu Sans Mono",Menlo,Consolas,monospace;font-size:14px}}
.note{{font-size:13.5px;fill:{MUT}}}
.li{{fill:{ELEM['Li']}}} .p{{fill:{ELEM['P']}}} .nd{{fill:{ELEM['Nd']}}} .fld{{fill:{FIELD}}} .wht{{fill:{WHITE}}}
.ax{{stroke:{MUT};stroke-width:1.2;fill:none}}
.guide{{stroke:{MUT};stroke-width:1;stroke-dasharray:3 4;fill:none}}
.trace{{fill:none;stroke-width:2.2;stroke-linejoin:round}}
</style>"""


def _svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">\n{STYLE}\n'
            f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="8" fill="{WHITE}" stroke="{LINE}"/>\n'
            f'{body}\n</svg>\n')


def _arrowhead(mid, color):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>')


def lorentz_path(x_of, y_base, d0, fwhm, height, lo, hi, step=0.004):
    pts, d = [], hi
    while d >= lo - 1e-9:
        y = height / (1 + ((d - d0) / (fwhm / 2)) ** 2)
        pts.append(f"{x_of(d):.1f},{y_base - y:.1f}")
        d -= step
    return "M" + " L".join(pts)


def fig_spin():
    b = [f'<defs>{_arrowhead("af", FIELD)}{_arrowhead("ak", INK)}</defs>']
    for x in (40, 70, 100):
        b.append(f'<line x1="{x}" y1="185" x2="{x}" y2="30" stroke="{FIELD}" stroke-width="2" marker-end="url(#af)"/>')
    b.append('<text class="fld" x="70" y="22" text-anchor="middle">B₀</text>')
    b.append(f'<ellipse cx="250" cy="58" rx="56" ry="13" fill="none" stroke="{MUT}" stroke-dasharray="4 4"/>')
    b.append(f'<line x1="250" y1="132" x2="194" y2="58" stroke="{MUT}" stroke-dasharray="4 4"/>')
    b.append(f'<line x1="250" y1="132" x2="306" y2="58" stroke="{MUT}" stroke-dasharray="4 4"/>')
    b.append(f'<line x1="250" y1="132" x2="292" y2="66" stroke="{INK}" stroke-width="2" marker-end="url(#ak)"/>')
    b.append(f'<circle cx="250" cy="132" r="17" fill="{ELEM["Li"]}"/>')
    b.append('<text class="wht" x="250" y="137" text-anchor="middle" style="font-size:12px">⁷Li</text>')
    b += ['<text x="335" y="52">spin precesses</text>', '<text class="mono" x="335" y="74">f = γ·B / 2π</text>',
          '<text class="note" x="335" y="108">at 9.4 T</text>', '<text class="mono" x="335" y="130">¹H   400.2 MHz</text>',
          '<text class="mono li" x="335" y="152">⁷Li  155.5 MHz</text>', '<text class="mono p" x="335" y="174">³¹P  162.0 MHz</text>']
    return _svg(540, 200, "Nuclear spin precessing in the field B0; frequency proportional to the field", "\n".join(b))


def fig_resonance():
    s = ELEM["S"]
    b = [f'<defs>{_arrowhead("ar", s)}</defs>',
         f'<path d="M20,80 q10,-22 20,0 t20,0 t20,0 t20,0 t20,0" fill="none" stroke="{s}" stroke-width="2" marker-end="url(#ar)"/>',
         '<text x="20" y="122">radio wave</text>',
         f'<circle cx="160" cy="80" r="17" fill="{ELEM["Li"]}"/>',
         '<text class="wht" x="160" y="85" text-anchor="middle" style="font-size:12px">⁷Li</text>',
         '<line class="ax" x1="200" y1="80" x2="244" y2="80"/>', f'<path d="M244,74 L256,80 L244,86 z" fill="{INK}"/>',
         '<line class="ax" x1="280" y1="136" x2="520" y2="136"/>',
         f'<path class="trace" stroke="{ELEM["Li"]}" d="M280,135 C360,134 380,128 392,96 C398,70 402,40 400,40 '
         'C398,40 402,70 408,96 C420,128 440,134 520,135"/>',
         '<text x="388" y="52" text-anchor="end">absorbs only at its own f</text>',
         '<text class="note" x="520" y="160" text-anchor="end">frequency →</text>']
    return _svg(540, 172, "Absorption happens only at the nucleus's own frequency, giving one peak", "\n".join(b))


def fig_shielding():
    li = ELEM["Li"]
    b = [f'<defs>{_arrowhead("af2", FIELD)}{_arrowhead("ak2", INK)}</defs>',
         f'<line x1="22" y1="196" x2="22" y2="40" stroke="{FIELD}" stroke-width="2" marker-end="url(#af2)"/>',
         '<text class="fld" x="22" y="30" text-anchor="middle">B₀</text>',
         '<text class="mono" x="275" y="30" text-anchor="middle">B_eff = B₀ − b_ind = B₀ (1 − σ)</text>']
    for cx, r, tail, lab, n1, n2 in ((150, 34, 136, "thin electron cloud", "small b_ind · feels more B",
                                      "→ higher f · higher ppm"),
                                     (395, 52, 150, "thick electron cloud", "larger b_ind · feels less B",
                                      "→ lower f · lower ppm (up-field)")):
        b.append(f'<circle cx="{cx}" cy="104" r="{r}" fill="{CLOUD}" stroke="{li}" stroke-dasharray="2 3"/>')
        b.append(f'<circle cx="{cx}" cy="104" r="12" fill="{li}"/>')
        b.append(f'<line x1="{cx}" y1="124" x2="{cx}" y2="{tail}" stroke="{INK}" stroke-width="2" marker-end="url(#ak2)"/>')
        b.append(f'<text x="{cx}" y="184" text-anchor="middle">{lab}</text>')
        b.append(f'<text class="note" x="{cx}" y="204" text-anchor="middle">{n1}</text>')
        b.append(f'<text class="note" x="{cx}" y="222" text-anchor="middle">{n2}</text>')
    return _svg(540, 236, "Thin and thick electron clouds; the thicker cloud shields the nucleus more", "\n".join(b))


def fig_ppm_axis():
    b = [f'<defs>{_arrowhead("am", INK)}</defs>',
         '<line class="ax" x1="40" y1="74" x2="500" y2="74"/>',
         '<line class="ax" x1="40" y1="74" x2="40" y2="81"/><text class="mono" x="40" y="98" text-anchor="middle">high ppm</text>',
         '<line class="ax" x1="500" y1="74" x2="500" y2="81"/><text class="mono" x="500" y="98" text-anchor="middle">low ppm</text>',
         f'<line x1="250" y1="40" x2="70" y2="40" stroke="{INK}" stroke-width="2" marker-end="url(#am)"/>',
         f'<line x1="290" y1="40" x2="470" y2="40" stroke="{INK}" stroke-width="2" marker-end="url(#am)"/>',
         '<text x="160" y="28" text-anchor="middle">down-field</text>', '<text x="380" y="28" text-anchor="middle">up-field</text>',
         '<text class="note" x="40" y="122">less shielded · higher f</text>',
         '<text class="note" x="500" y="122" text-anchor="end">more shielded · lower f</text>']
    return _svg(540, 136, "ppm axis: left is high ppm (down-field, less shielded), right is low ppm (up-field, more shielded)",
                "\n".join(b))


X0, X1, PMAX, PMIN, AX = 60.0, 480.0, 3.0, -1.0, 240.0


def xli(d):
    return X0 + (PMAX - d) / (PMAX - PMIN) * (X1 - X0)


def fig_li7(centers=None, printed=None):
    """centers · printed 는 selftest 의 음성 경로만 바꾼다 (기본 = 원고 문장 숫자)."""
    centers = centers or dict(LI_EXPECTED)
    printed = printed or dict(LI_EXPECTED)
    li = ELEM["Li"]
    base = {"li-a": 100.0, "li-b": 220.0}
    h = 70.0
    a_x, b_x = xli(centers["li-a"]), xli(centers["li-b"])
    b = [f'<defs>{_arrowhead("al", li)}</defs>',
         f'<line class="guide" x1="{a_x:.1f}" y1="{base["li-a"] - h - 6:.1f}" x2="{a_x:.1f}" y2="{AX - 2}"/>',
         f'<line class="guide" stroke="{li}" x1="{b_x:.1f}" y1="{base["li-b"] - h - 6:.1f}" x2="{b_x:.1f}" y2="{AX - 2}" style="stroke:{li}"/>',
         f'<text x="{X0}" y="{base["li-a"] - h - 6:.1f}">LPSCl1.6</text>',
         f'<path id="li-a" class="trace" stroke="{MUT}" d="{lorentz_path(xli, base["li-a"], centers["li-a"], 0.30, h, PMIN, PMAX)}"/>',
         f'<text class="li" x="{X0}" y="{base["li-b"] - h - 6:.1f}">NdO-LPSCl1.6</text>',
         f'<path id="li-b" class="trace" stroke="{li}" d="{lorentz_path(xli, base["li-b"], centers["li-b"], 0.30, h, PMIN, PMAX)}"/>',
         f'<text class="mono" data-for="li-a" x="{a_x - 10:.1f}" y="{base["li-a"] - h + 6:.1f}" text-anchor="end">{printed["li-a"]:.2f}</text>',
         f'<text class="mono li" data-for="li-b" x="{b_x + 10:.1f}" y="{base["li-b"] - h + 6:.1f}">{printed["li-b"]:.2f}</text>',
         f'<line x1="{a_x:.1f}" y1="128" x2="{b_x - 2:.1f}" y2="128" stroke="{li}" stroke-width="1.8" marker-end="url(#al)"/>',
         f'<text class="li" x="{b_x + 10:.1f}" y="133">{abs(printed["li-a"] - printed["li-b"]):.2f} ppm up-field</text>',
         f'<line id="li-axis" class="ax" data-ppm-left="{PMAX:g}" data-ppm-right="{PMIN:g}" x1="{X0}" y1="{AX}" x2="{X1}" y2="{AX}"/>']
    for t in (3, 2, 1, 0, -1):
        b.append(f'<line class="ax" x1="{xli(t):.1f}" y1="{AX}" x2="{xli(t):.1f}" y2="{AX + 6}"/>'
                 f'<text class="mono" x="{xli(t):.1f}" y="{AX + 24}" text-anchor="middle">{t:g}</text>')
    b.append(f'<text x="{(X0 + X1) / 2:.1f}" y="{AX + 52}" text-anchor="middle">⁷Li shift (ppm)   ← higher · lower →</text>')
    return _svg(540, 304, "7Li peak moves from 1.48 to 1.16 ppm, 0.32 ppm toward lower ppm (schematic positions)",
                "\n".join(b))


def fig_p31():
    p = ELEM["P"]
    b = []
    for i, (lab, shift) in enumerate((("x = 0", 0), ("x = 0.02", 14), ("x = 0.04", 28))):
        y0 = 74 + i * 62
        pts = " L".join(f"{u:.1f},{y0 - 46 / (1 + ((u - (300 + shift)) / 11) ** 2):.1f}"
                        for u in (150 + k * 1.5 for k in range(241)))
        b.append(f'<path class="trace" stroke="{p if i else MUT}" d="M{pts}"/>')
        b.append(f'<text {"class=" + chr(34) + "p" + chr(34) if i else ""} x="40" y="{y0 - 4}">{lab}</text>')
    b += ['<line class="guide" x1="300" y1="18" x2="300" y2="210"/>', '<line class="ax" x1="150" y1="212" x2="510" y2="212"/>',
          '<text x="330" y="238" text-anchor="middle">³¹P shift   ← higher · lower →</text>',
          '<text class="note" x="510" y="22" text-anchor="end">schematic · direction only</text>',
          '<text class="note" x="150" y="22">PS₄³⁻ peak</text>']
    return _svg(540, 252, "31P PS4 peak moves slightly toward lower ppm as substitution increases (schematic, no values)",
                "\n".join(b))


def fig_nd():
    nd, p = ELEM["Nd"], ELEM["P"]
    b = [f'<defs>{_arrowhead("an", WHITE)}</defs>',
         f'<circle cx="150" cy="105" r="52" fill="none" stroke="{nd}" stroke-dasharray="2 4"/>',
         f'<circle cx="150" cy="105" r="80" fill="none" stroke="{nd}" stroke-dasharray="2 4" opacity="0.7"/>',
         f'<circle cx="150" cy="105" r="26" fill="{nd}"/>']
    for x in (138, 150, 162):
        b.append(f'<line x1="{x}" y1="118" x2="{x}" y2="92" stroke="{WHITE}" stroke-width="2" marker-end="url(#an)"/>')
    b += [f'<text class="nd" x="150" y="208" text-anchor="middle">Nd³⁺ · 4f³</text>',
          '<text class="note" x="150" y="228" text-anchor="middle">3 unpaired electrons</text>',
          f'<circle cx="200" cy="70" r="12" fill="{p}"/>', '<text class="p" x="236" y="64">P nearby</text>',
          '<text class="note" x="236" y="86">peak shifted or broadened</text>',
          f'<circle cx="440" cy="150" r="12" fill="{p}"/>', '<text class="p" x="440" y="186" text-anchor="middle">P far away</text>',
          '<text class="note" x="440" y="208" text-anchor="middle">unchanged</text>']
    return _svg(540, 240, "Nd3+ with three unpaired 4f electrons acts as a small magnet; nearby P is shifted or broadened",
                "\n".join(b))


BUILDERS = {
    "nmr_01_spin_precession.svg": fig_spin,
    "nmr_02_resonance.svg": fig_resonance,
    "nmr_03_shielding.svg": fig_shielding,
    "nmr_04_ppm_axis.svg": fig_ppm_axis,
    "nmr_05_li7_shift.svg": fig_li7,
    "nmr_06_p31_schematic.svg": fig_p31,
    "nmr_07_paramagnetic_nd.svg": fig_nd,
}

_HANGUL = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
_NS = "{http://www.w3.org/2000/svg}"


def check(svgs: dict) -> list[str]:
    """그림 묶음 → 오류 목록 (빈 목록 = 통과)."""
    errs = []
    for name, s in svgs.items():
        try:
            root = ET.fromstring(s)
        except ET.ParseError as e:
            errs.append(f"{name}: XML 로 안 읽힌다 ({e})")
            continue
        for t in root.iter(_NS + "text"):
            if _HANGUL.search("".join(t.itertext())):
                errs.append(f"{name}: 그림 안 글자에 한글 — {''.join(t.itertext())!r} (하우스 규약: 영어만)")
        if name != "nmr_05_li7_shift.svg":
            continue
        axis = next((e for e in root.iter(_NS + "line") if e.get("id") == "li-axis"), None)
        if axis is None:
            errs.append(f"{name}: 축 (id li-axis) 이 없다")
            continue
        x1, x2 = float(axis.get("x1")), float(axis.get("x2"))
        pl, pr = float(axis.get("data-ppm-left")), float(axis.get("data-ppm-right"))
        for pid, want in LI_EXPECTED.items():
            path = next((e for e in root.iter(_NS + "path") if e.get("id") == pid), None)
            if path is None:
                errs.append(f"{name}: 봉우리 {pid} 가 없다")
                continue
            pts = [tuple(map(float, q.split(","))) for q in re.findall(r"-?\d+\.?\d*,-?\d+\.?\d*", path.get("d"))]
            apex_x = min(pts, key=lambda q: q[1])[0]
            apex_ppm = pl + (apex_x - x1) / (x2 - x1) * (pr - pl)
            if abs(apex_ppm - want) > 0.01:
                errs.append(f"{name}: {pid} 꼭대기가 {apex_ppm:.3f} ppm — 원고 문장 숫자 {want} 와 다르다")
            lab = next((e for e in root.iter(_NS + "text") if e.get("data-for") == pid), None)
            if lab is None or abs(float(lab.text) - want) > 1e-9:
                errs.append(f"{name}: {pid} 에 인쇄된 숫자 {getattr(lab, 'text', None)!r} ≠ {want}")
    return errs


def build() -> dict:
    return {n: f() for n, f in BUILDERS.items()}


def selftest() -> int:
    fails = []

    def ck(label, cond):
        print(f"  {'✓' if cond else '✗'} {label}")
        if not cond:
            fails.append(label)
    svgs = build()
    ck(f"양성: 그림 {len(svgs)} 장 · 검사 오류 0", len(svgs) == 7 and check(svgs) == [])
    bad = dict(svgs, **{"nmr_02_resonance.svg": svgs["nmr_02_resonance.svg"].replace("radio wave", "전파")})
    ck("⛔음성: 그림 안 한글 라벨 → 잡는다", any("한글" in e for e in check(bad)))
    bad = dict(svgs, **{"nmr_05_li7_shift.svg": fig_li7(centers={"li-a": 1.40, "li-b": 1.16})})
    ck("⛔음성: 봉우리를 1.40 에 그리고 글자는 1.48 → 잡는다", any("꼭대기" in e and "li-a" in e for e in check(bad)))
    bad = dict(svgs, **{"nmr_05_li7_shift.svg": fig_li7(printed={"li-a": 1.48, "li-b": 1.12})})
    ck("⛔음성: 봉우리는 맞고 인쇄 숫자만 1.12 → 잡는다", any("인쇄된 숫자" in e for e in check(bad)))
    bad = dict(svgs, **{"nmr_04_ppm_axis.svg": svgs["nmr_04_ppm_axis.svg"].replace("</svg>", "")})
    ck("⛔음성: 깨진 XML → 잡는다", any("XML" in e for e in check(bad)))
    print(f"selftest {'PASS' if not fails else 'FAIL'} ({len(fails)} 실패)")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    svgs = build()
    errs = check(svgs)
    if errs:
        print("⛔ 검사 실패 — 쓰지 않는다:\n  " + "\n  ".join(errs))
        return 2
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for n, s in svgs.items():
        (out / n).write_text(s, encoding="utf-8")
    print(f"✓ {len(svgs)} 장 → {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
