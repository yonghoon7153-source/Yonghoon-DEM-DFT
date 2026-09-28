#!/usr/bin/env python3
"""fig_wad_briefing_2026_09_28.py — 점착(W_ad) 트랙 브리핑 그림 1장 (슬라이드용).

  (a) Decision path — 계획 v1 → v2 → v3 → A′ 와 A′ 파일럿 사전등록 BY → CB → S1 봉인.
      판정은 `db/pipelines/adhesion_pipeline.json` 의 reviews[].verdict 앞머리에서 읽는다.
  (b) V5 VASP 외주 준비본 리뷰 라운드 CE → CK 의 P0 · P1 개수.
      값은 `db/properties/weekly_review_traffic_origin_2026_09_27.csv` (이미 검증된 주간 산출물)에서 읽는다.
  (c) 트랙 현재 상태 — V2 / V4 / V5 한 줄씩.

    python3 tools/figures/fig_wad_briefing_2026_09_28.py
    python3 tools/figures/fig_wad_briefing_2026_09_28.py --selftest

이 도구가 **못 하는 것**
  · ⛔ **W_ad 숫자를 그리지 않는다** (W_sep · SE|SE 4층 값 · ATM 열 · G3 차이값).
    결과 기록이 *"원장·화면 게재는 1저자 별도"* 로 막아 두었다. 라벨(G3 FAIL)만 쓴다.
    같은 금지가 `tools/figures/fig_weekly_2026_09_27.py` 에도 박혀 있다.
  · 판정을 내리지 않는다 — 전부 원장·CSV 에서 읽고, 없으면 **죽는다**(0 으로 두지 않는다).
  · 원격 기계의 **지금** 상태를 모른다. (c) 의 V4 문구는 원장 기준이고 실측 시각을 같이 적는다.
  · 리뷰 P0/P1 은 회신 제목 세기 규칙의 결과다 — 규칙은 주간 도구 docstring 에 있다.
"""
from __future__ import annotations

import csv
import json
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from house_style import INK, MUT, apply_axes  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
LEDGER = REPO / "db/pipelines/adhesion_pipeline.json"
TRAFFIC = REPO / "db/properties/weekly_review_traffic_origin_2026_09_27.csv"
OUT = REPO / "db/properties/cei_figs"

NOGO, COND, GO = "#be123c", "#c05621", "#0d9488"
#: 실측 시각 — (c) 에 같이 적는다. 이 뒤로는 사용자가 붙여 주는 출력으로만 갱신한다.
AS_OF = "2026-09-27 14:02"


def _verdict_class(v: str) -> str:
    """판정 문장 앞머리로 세 갈래. 모르는 문구면 죽는다 (조용히 회색으로 두지 않는다)."""
    head = (v or "").strip()
    if head.startswith("NO-GO"):
        return "nogo"
    if head.startswith("조건부 GO"):
        return "cond"
    if head.startswith("GO"):
        return "go"
    raise SystemExit(f"⛔ 모르는 판정 문구: {head[:40]!r} — 분류 규칙을 고쳐라")


def load_rounds():
    """(b) 용 — V5 라운드의 P0/P1. CSV 에 없으면 죽는다."""
    #: ⚠ 주석 첫 줄이 따옴표에 싸여 있다(`"# …`) — lstrip('"') 없이는 그 줄이 머리로 잡힌다.
    rows = [r for r in csv.DictReader(
        (ln for ln in TRAFFIC.open(encoding="utf-8") if not ln.lstrip('"').startswith("#")))
        if r["channel"] == "v5"]
    if not rows:
        raise SystemExit("⛔ CSV 에 v5 라운드가 없다")
    out = []
    for r in rows:
        if r["P0_count"] == "" or r["P1_count"] == "":
            raise SystemExit(f"⛔ {r['letter']} 의 P0/P1 이 비어 있다 — 0 으로 두지 않는다")
        out.append((r["letter"], int(r["P0_count"]), int(r["P1_count"]), r["verdict_class"]))
    return out


def load_path():
    """(a) 용 — 계획·사전등록 판정 사슬. 원장 reviews 순서를 그대로 쓴다."""
    d = json.loads(LEDGER.read_text("utf-8"))
    rv = d["reviews"]
    if len(rv) < 8:
        raise SystemExit(f"⛔ 원장 reviews 가 {len(rv)} 개다 — 사슬을 그릴 수 없다")
    steps = [("Plan v1", rv[0]["verdict"]), ("Plan v2", rv[1]["verdict"]),
             ("Plan v3 → A′", rv[2]["verdict"]),
             ("Prereg v1", rv[4]["verdict"]), ("Prereg v2", rv[5]["verdict"]),
             ("Prereg v3", rv[6]["verdict"]), ("Prereg v4", rv[7]["verdict"])]
    return [(n, _verdict_class(v)) for n, v in steps]


def panel_a(ax, steps):
    col = {"nogo": NOGO, "cond": COND, "go": GO}
    for i, (name, cls) in enumerate(steps):
        ax.scatter(i, 0, s=340, color=col[cls], zorder=3, edgecolor="white", lw=1.4)
        ax.text(i, .42, name, ha="center", va="bottom", fontsize=8.6, color=INK, rotation=28)
        ax.text(i, -.40, {"nogo": "NO-GO", "cond": "cond. GO", "go": "GO"}[cls],
                ha="center", va="top", fontsize=7.8, color=col[cls])
        if i:
            ax.add_patch(FancyArrowPatch((i - 1, 0), (i, 0), arrowstyle="-|>",
                                         mutation_scale=11, color=MUT, lw=1.0, zorder=1,
                                         shrinkA=11, shrinkB=11))
    ax.scatter(len(steps), 0, s=340, marker="s", color=GO, zorder=3,
               edgecolor="white", lw=1.4)
    ax.text(len(steps), .42, "S1 sealed", ha="center", va="bottom",
            fontsize=8.6, color=INK, rotation=28)
    ax.text(len(steps), -.40, "09-25", ha="center", va="top", fontsize=7.8, color=MUT)
    ax.add_patch(FancyArrowPatch((len(steps) - 1, 0), (len(steps), 0), arrowstyle="-|>",
                                 mutation_scale=11, color=MUT, lw=1.0, zorder=1,
                                 shrinkA=11, shrinkB=11))
    ax.set_xlim(-.7, len(steps) + .7); ax.set_ylim(-1.5, 1.7)
    ax.set_yticks([]); ax.set_xticks([])
    #: 개수를 손으로 적지 않는다 — 원장 단계가 늘면 제목이 조용히 틀려진다.
    apply_axes(ax, None, None,
               f"(a)  {len(steps)} review rounds fixed the plan before any production run")
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)


def panel_b(ax, rounds):
    xs = range(len(rounds))
    p0 = [r[1] for r in rounds]
    p1 = [r[2] for r in rounds]
    ax.bar([x - .19 for x in xs], p0, width=.36, color=NOGO, label="P0 (blocking)")
    ax.bar([x + .19 for x in xs], p1, width=.36, color=COND, label="P1")
    for x, (lt, a, b, cls) in zip(xs, rounds):
        if cls == "go":
            ax.text(x, .28, "GO", ha="center", fontsize=9, color=GO, fontweight="bold")
    ax.set_xticks(list(xs)); ax.set_xticklabels([r[0] for r in rounds])
    ax.set_ylim(0, max(p0 + p1) + 1.2)
    apply_axes(ax, "Review round (V5 VASP outsourcing package)", "Findings",
               "(b)  Blocking findings driven to zero")
    ax.legend(frameon=False, fontsize=8.6, labelcolor=INK)


def panel_c(ax):
    rows = [("V2  Ag | graphene", GO,
             "done — reported with a G3 FAIL label; DEM open questions 0"),
            ("V4  production", COND,
             f"9 jobs running on one GPU (as of {AS_OF})"),
            ("V5  largest model", NOGO,
             "does not fit 48 GB → VASP outsourcing package, technical GO only")]
    for i, (name, c, txt) in enumerate(rows):
        y = 2 - i
        ax.scatter(0, y, s=190, color=c, edgecolor="white", lw=1.3, zorder=3)
        ax.text(.22, y + .17, name, fontsize=9.4, color=INK, va="center", fontweight="bold")
        ax.text(.22, y - .22, txt, fontsize=8.4, color=MUT, va="center")
    ax.set_xlim(-.25, 5.2); ax.set_ylim(-.7, 2.8)
    ax.set_xticks([]); ax.set_yticks([])
    apply_axes(ax, None, None, "(c)  Where the track stands")
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)


def build(out=None):
    steps, rounds = load_path(), load_rounds()
    fig, axs = plt.subplots(1, 3, figsize=(14.4, 3.9),
                            gridspec_kw={"width_ratios": [1.25, 1.0, 1.05]})
    panel_a(axs[0], steps); panel_b(axs[1], rounds); panel_c(axs[2])
    fig.tight_layout()
    p = pathlib.Path(out) if out else OUT / "wad_briefing_2026_09_28.png"
    fig.savefig(p, dpi=300, bbox_inches="tight"); plt.close(fig)
    return p


def write_csv(out=None):
    p = pathlib.Path(out) if out else OUT / "wad_briefing_rounds_origin_2026_09_28.csv"
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["round_letter", "P0_blocking_count", "P1_count", "verdict_class"])
        for lt, a, b, cls in load_rounds():
            w.writerow([lt, a, b, cls])
    return p


def _selftest():
    import tempfile, shutil
    ok = True
    td = tempfile.mkdtemp(prefix="wadbrief_")

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    try:
        rounds = load_rounds()
        chk(len(rounds) == 6, f"[양성] V5 라운드 {len(rounds)} 개 (CE–CK)")
        chk(rounds[0][1] == 4 and rounds[-1][1] == 0,
            f"[양성] P0 가 {rounds[0][1]} → {rounds[-1][1]} 로 떨어진다")
        chk(rounds[-1][3] == "go", "[양성] 마지막 라운드가 GO 다")
        src_all = pathlib.Path(__file__).read_text("utf-8")
        steps = load_path()
        chk(len(steps) == 7 and steps[0][1] == "nogo",
            f"[양성] 판정 사슬 {len(steps)} 단계 · 첫 단계 NO-GO")
        f = pathlib.Path(build(out=f"{td}/b.png"))
        chk(f.exists() and f.stat().st_size > 30000, "[양성] 그림이 그려진다")
        c = pathlib.Path(write_csv(out=f"{td}/r.csv"))
        chk(c.exists() and len(c.read_text('utf-8').splitlines()) == 7,
            "[양성] Origin CSV 가 머리 1 + 6 행")
        # ⛔음성 — 모르는 판정 문구는 회색으로 두지 않고 죽는다
        died = False
        try:
            _verdict_class("아마도 괜찮음")
        except SystemExit as e:
            died = "모르는 판정" in str(e)
        chk(died, "[⛔음성] 모르는 판정 문구는 분류하지 않고 죽는다")
        # ⛔음성 — GO 로 시작하지만 NO-GO 인 문장을 GO 로 읽지 않는다
        chk(_verdict_class("NO-GO (V5 …) — GO 아님") == "nogo",
            "[⛔음성] 'NO-GO …' 안의 GO 글자에 안 속는다")
        #: 쪼개서 쓴다 — 붙여 쓰면 이 시험 줄 자신이 걸려 영원히 빨간불이다.
        chk(("Six" + " review") not in src_all,
            "[⛔음성] (a) 제목에 개수가 손으로 박혀 있지 않다")
        # ⛔음성 — 그림에 W 값을 넣지 않는다 (소스에 금지 숫자가 없는지)
        chk("J/m" not in src_all.split('"""')[2],
            "[⛔음성] 본문 코드에 W 단위(J/m²) 문자열이 없다 — 숫자 게재 금지")
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    png, csvp = build(), write_csv()
    print(f"✓ {png.relative_to(REPO)}")
    print(f"✓ {csvp.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest() if "--selftest" in sys.argv else main())
