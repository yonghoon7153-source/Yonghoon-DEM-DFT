"""연구세미나 덱 v3.3 (2026-10-15) — Problem 4 그림의 띠 이름 판 = F_p4_v33 (Codex v3.2 재확인 §5 · 1저자 10-15 비준 Q2).

Codex §5: 8.3–11.7 % 띠는 결과 전 B2 의 **모델 예측 띠**다 (실험 범위 · 통계 신뢰구간 아님) → 그림에서 `registered prediction band` 로 부른다.
그리는 코드 = make_seminar_figs_v32.fig_p4 **그대로** (같은 P4 기록 문자열 · 같은 막대 · 같은 빗금 · 새 계산 없음).
바뀌는 것 (저장 직전에만): (b) 패널 이름표 `registered prediction band` + 지시선 · (b) y 상한 18 → 20 (이름표 자리 · 값 무관) ·
CSV state 이름 셋 (`registered band …` → `registered prediction band …` · 값 · 단위 · 출처 열 그대로).
실행: python3 make_seminar_figs_v33.py <out_dir>   · selftest: python3 make_seminar_figs_v33.py --selftest [<리포>]
"""
import csv
import re
import sys
import tempfile
from pathlib import Path

import make_seminar_figs as m        # 같은 폴더 (v3 양식 · _save · 겹침 검사)
import make_seminar_figs_v32 as v32  # 같은 폴더 (F_p4 그리는 코드 · 기록 문자열 · 값 selftest)

NAME = "F_p4_v33"
BAND_LABEL = "registered prediction band"
B_YMAX = 20
ROW_RENAME = {"registered band low (before the run)": "registered prediction band low (before the run)",
              "registered band high (before the run)": "registered prediction band high (before the run)",
              "registered point (before the run)": "registered prediction point (before the run)"}
SVG_VALUES = ("300.9", "165.3", "299.3", "14.95", "10.77", "111.05", "105.84", "57.9")


def _label_band(fig):
    """(b) 패널: y 상한 18 → 20 · 오른쪽 위 세 줄 이름표 (회색) · 띠 오른쪽 위 모서리로 가는 지시선 (글자 아님 · 겹침 검사 밖)."""
    _a, b = fig.axes
    b.set_ylim(0, B_YMAX)
    t = b.text(2.33, B_YMAX - 0.2, "registered\nprediction\nband", ha="right", va="top", fontsize=10, color=m.GRAY, linespacing=1.05)
    fig.canvas.draw()
    bb = t.get_window_extent(fig.canvas.get_renderer()).transformed(b.transData.inverted())
    hi = float(v32.P4["band_hi"])
    b.plot([2.20, 2.06], [bb.y0 - 0.25, hi - 0.15], color=m.GRAY, lw=0.8, solid_capstyle="butt")


def fig_p4_v33(out):
    """make_seminar_figs_v32.fig_p4 를 그대로 부르고, 저장 (m._save) 직전에만 이름표 · y 상한 · CSV 이름을 바꾼다."""
    orig = m._save

    def _save(fig, out_dir, name, rows=None, header=None):
        assert name == "F_p4", name
        _label_band(fig)
        rows = [(r[0], ROW_RENAME.get(r[1], r[1])) + tuple(r[2:]) for r in rows]
        return orig(fig, out_dir, NAME, rows=rows, header=header)

    m._save = _save
    try:
        v32.fig_p4(out)
    finally:
        m._save = orig


def _read(p):
    return Path(p).read_text(encoding="utf-8")


def _rows(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.reader(f))


def svg_text(svg):
    """SVG 에 그려진 글 (svg.fonttype = none → <text> 안 글자 · 여러 줄 글은 줄마다 따로) 을 순서대로 이어 붙인다."""
    parts = re.findall(r"<text[^>]*>(.*?)</text>", svg, flags=re.S)
    parts = [re.sub(r"<[^>]+>", "", p) for p in parts]
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def _hatch(svg):
    """빗금 = <pattern> 본문 (id 뺌 — matplotlib 는 그릴 때마다 id 에 무작위 salt 를 섞는다) · 쓰인 횟수."""
    out = []
    for pm in re.finditer(r'<pattern[^>]*id="([^"]+)"[^>]*>(.*?)</pattern>', svg, flags=re.S):
        body = re.sub(r"\s+", " ", pm.group(0).replace(pm.group(1), "ID"))
        out.append((body, len(re.findall(r"url\(#%s\)" % re.escape(pm.group(1)), svg))))
    return sorted(out)


def check_fig_files(svg_path, csv_path, base_svg_path, base_csv_path):
    """새 그림 (svg · csv) ↔ v3.2 F_p4 (svg · csv).  실패 목록 (빈 목록 = 통과)."""
    fails = []
    svg, base_svg = _read(svg_path), _read(base_svg_path)
    rows, base_rows = _rows(csv_path), _rows(base_csv_path)
    if BAND_LABEL not in svg_text(svg):
        fails.append(f"in-figure label '{BAND_LABEL}' missing")
    if "static" in svg.lower():
        fails.append("'static' wording in the figure (MV-01)")
    miss = [s for s in SVG_VALUES if s not in svg]
    if miss:
        fails.append(f"value labels missing {miss}")
    if rows[:1] != base_rows[:1] or len(rows) != len(base_rows):
        fails.append("CSV header / row count differs from F_p4.csv")
    for r, b in zip(rows[1:], base_rows[1:]):
        if (r[0], r[2], r[3], r[4]) != (b[0], b[2], b[3], b[4]):
            fails.append(f"CSV value / unit / source changed: {b} → {r}")
        if r[1] != ROW_RENAME.get(b[1], b[1]):
            fails.append(f"CSV state name: want {ROW_RENAME.get(b[1], b[1])!r}, got {r[1]!r}")
    if not any(BAND_LABEL in r[1] for r in rows[1:]):
        fails.append("no CSV row names the registered prediction band")
    if any("registered band" in r[1] for r in rows[1:]):
        fails.append("old CSV name 'registered band' still present")
    if _hatch(svg) != _hatch(base_svg):
        fails.append(f"hatch patterns / uses differ: {_hatch(base_svg)} → {_hatch(svg)}")
    return fails


def selftest(repo=m.REPO):
    v32.selftest(repo)                                  # F_p4 값 = README §1 · §4 · §12-4 · DEMP-01 기록 문자열 (v3.2 와 같은 대조)
    m.OVERLAPS.clear()
    with tempfile.TemporaryDirectory() as d0, tempfile.TemporaryDirectory() as d1:
        v32.fig_p4(d0)
        fig_p4_v33(d1)
        fails = check_fig_files(Path(d1, f"{NAME}.svg"), Path(d1, f"{NAME}.csv"), Path(d0, "F_p4.svg"), Path(d0, "F_p4.csv"))
        here = Path(__file__).resolve().parent
        if (here / f"{NAME}.csv").exists() and _read(here / f"{NAME}.csv") != _read(Path(d1, f"{NAME}.csv")):
            fails.append("committed F_p4_v33.csv differs from the regenerated one")
    assert not fails, fails
    assert not m.OVERLAPS, f"overlapping text in F_p4 / F_p4_v33: {m.OVERLAPS}"
    print("selftest ok — F_p4_v33 = F_p4 (v3.2) values · hatch · bars; band named 'registered prediction band'; no overlapping text")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2] if len(sys.argv) > 2 else m.REPO)
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "."
        Path(out).mkdir(parents=True, exist_ok=True)
        fig_p4_v33(out)
        print("written", out)
