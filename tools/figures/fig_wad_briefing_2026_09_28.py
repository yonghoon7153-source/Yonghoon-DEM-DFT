#!/usr/bin/env python3
"""fig_wad_briefing_2026_09_28.py — 점착(W_ad) 트랙 브리핑 그림 1장 (슬라이드용).

  (a) What we measure — 슬랩 둘을 떼어내는 모식도 + W_sep 정의. DEM 은 이 값을 JKR 의 w 로 쓴다.
  (b) Which interfaces — 대상별 상태. 잡 수는 점착 원장 runs[].jobs 의 state 를 **세어서** 넣는다.
  (c) A′ rule — 작은 모형은 DFT 값 · 전체 계면은 UMA+D3 예측 · DEM 은 민감도 시나리오로만.

    python3 tools/figures/fig_wad_briefing_2026_09_28.py
    python3 tools/figures/fig_wad_briefing_2026_09_28.py --selftest

이 도구가 **못 하는 것**
  · ⛔ **W_ad 숫자를 그리지 않는다** (W_sep · SE|SE 4층 값 · ATM 열 · G3 차이값).
    결과 기록이 *"원장·화면 게재는 1저자 별도"* 로 막아 두었다. 라벨(G3 FAIL)·정의식만 쓴다.
    같은 금지가 `tools/figures/fig_weekly_2026_09_27.py` 에도 박혀 있다.
  · 판정을 내리지 않는다 — 상태·잡 수는 원장에서 읽고, 없으면 **죽는다**(0 으로 두지 않는다).
  · 원격 기계의 **지금** 상태를 모른다. (b) 는 원장 기준이고 실측 시각을 같이 적는다.
  · 모식도는 **정의를 보여주는 그림**이다 — 실제 셀 크기·원자 배치가 아니다.
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


def load_v4():
    """(b) 용 — V4 본 잡의 state 별 개수. 원장에서 세고, 없으면 죽는다."""
    d = json.loads(LEDGER.read_text("utf-8"))
    run = next((r for r in d["runs"] if r["id"] == "aprime_v4_main_gabia_2026_09_27"), None)
    if run is None:
        raise SystemExit("⛔ 원장에 V4 본 잡 run 이 없다")
    cnt = {}
    for j in run["jobs"]:
        cnt[j.get("state", "?")] = cnt.get(j.get("state", "?"), 0) + 1
    if "?" in cnt:
        raise SystemExit("⛔ state 없는 잡이 있다 — 세지 않는다")
    return len(run["jobs"]), cnt


def panel_a(ax):
    """무엇을 재나 — 정의를 보여주는 모식도 (실제 셀이 아니다)."""
    import matplotlib.patches as mp
    for y, lab, c in ((2.55, "slab A", "#7c3aed"), (0.35, "slab B", "#c05621")):
        ax.add_patch(mp.FancyBboxPatch((0.25, y), 3.5, 1.0, boxstyle="round,pad=0.03",
                                       fc=c, ec="none", alpha=.28))
        ax.text(2.0, y + .5, lab, ha="center", va="center", fontsize=11, color=INK)
    ax.annotate("", xy=(2.0, 3.95), xytext=(2.0, 3.05),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    ax.annotate("", xy=(2.0, -0.60), xytext=(2.0, 0.30),
                arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    ax.text(4.05, 1.95, "separate\nat fixed geometry", fontsize=9, color=MUT,
            va="center", linespacing=1.3)
    ax.text(2.0, 1.83, r"$W_{\rm sep}=\dfrac{E_A+E_B-E_{AB}}{A}$",
            ha="center", va="center", fontsize=13, color=INK)
    ax.text(2.0, -1.35, "DEM uses it as the JKR work of adhesion $w$",
            ha="center", fontsize=9.4, color=MUT)
    ax.set_xlim(-.3, 6.3); ax.set_ylim(-1.9, 4.5)
    ax.set_xticks([]); ax.set_yticks([])
    apply_axes(ax, None, None, "(a)  What we compute")
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)


def panel_b(ax, n_v4, cnt):
    run_n = cnt.get("run", 0) + cnt.get("done", 0)
    rows = [("SE | SE  (control)", GO, "5 jobs done \u2014 alarm kept, diagnosis only"),
            ("V2  Ag | graphene", GO, "done \u2014 delivered with a G3 FAIL label"),
            ("V4  production", COND,
             f"{n_v4} jobs: {cnt.get('done',0)} done, {cnt.get('run',0)} running, "
             f"{cnt.get('wait',0)} queued"),
            ("V5  largest model", NOGO, "over one GPU \u2192 VASP outsourcing package"),
            ("P1  LPSCl | Ag(111)", MUT, "not started \u2014 what DEM actually asked for"),
            ("P2  LPSCl | graphite", MUT, "not started")]
    for i, (name, c, txt) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.scatter(0, y, s=150, color=c, edgecolor="white", lw=1.2, zorder=3)
        ax.text(.20, y + .15, name, fontsize=9.6, color=INK, va="center", fontweight="bold")
        ax.text(.20, y - .24, txt, fontsize=8.5, color=MUT, va="center")
    ax.text(0, -1.15, f"as of {AS_OF} \u2014 remote state is not live here",
            fontsize=8.2, color=MUT)
    ax.set_xlim(-.22, 5.4); ax.set_ylim(-1.6, len(rows) - .3)
    ax.set_xticks([]); ax.set_yticks([])
    apply_axes(ax, None, None, "(b)  Which interfaces, and where each stands")
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)


def panel_c(ax, steps):
    lines = [("Small periodic model", GO, "report its own DFT value (PBE+D3)"),
             ("Full interface", COND, "UMA+D3 prediction, kept separately"),
             ("What DEM may do", NOGO,
              "use the two as a sensitivity band \u2014\nnot a validated material constant")]
    for i, (h, c, t) in enumerate(lines):
        y = 2 - i
        ax.scatter(0, y, s=150, color=c, edgecolor="white", lw=1.2, zorder=3)
        ax.text(.20, y + .18, h, fontsize=9.6, color=INK, va="center", fontweight="bold")
        ax.text(.20, y - .28, t, fontsize=8.5, color=MUT, va="center", linespacing=1.35)
    n_nogo = sum(1 for _, cls in steps if cls == "nogo")
    ax.text(0, -1.15,
            f"fixed before any production run \u2014 {len(steps)} review rounds, "
            f"{n_nogo} NO-GO",
            fontsize=8.2, color=MUT)
    ax.set_xlim(-.22, 5.4); ax.set_ylim(-1.6, 2.7)
    ax.set_xticks([]); ax.set_yticks([])
    apply_axes(ax, None, None, "(c)  Decision A\u2032 \u2014 what each number may be used for")
    for sp in ("left", "bottom"):
        ax.spines[sp].set_visible(False)


def build(out=None):
    steps = load_path()
    n_v4, cnt = load_v4()
    fig, axs = plt.subplots(1, 3, figsize=(14.4, 4.3),
                            gridspec_kw={"width_ratios": [.92, 1.12, 1.02]})
    panel_a(axs[0]); panel_b(axs[1], n_v4, cnt); panel_c(axs[2], steps)
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
        n_v4, cnt = load_v4()
        chk(n_v4 == sum(cnt.values()) and n_v4 > 0,
            f"[양성] V4 잡 {n_v4} 개가 state 합과 같다 {cnt}")
        chk(set(cnt) <= {"done", "run", "wait", "failed_technical", "not_started",
                         "incomplete"},
            f"[⛔음성] 모르는 state 가 섞여 있지 않다 {set(cnt)}")
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
