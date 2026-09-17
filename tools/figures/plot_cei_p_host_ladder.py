#!/usr/bin/env python3
"""plot_cei_p_host_ladder.py — Fig. 2b: P 가 어느 방으로 가는가 (Li 값 · 방 주인).

왜 새 파일인가 (2026-09-17)
---------------------------
tools/figures/plot_cei_nd_o_decomposition.py 가 §2–§7 그림을 다 만들지만 **거기에
넣지 않았다.** 두 가지 이유다:
  ① 소스가 다르다 — 이 그림은 `db/properties/cei_p_host_ladder_2026_09_17.json`
     (interface_reactivity_v2.py --p_host_ladder 산출) 을 읽고, 저 생성기는
     `cei_interface_V_*.json` 을 읽는다.
  ② 저 생성기를 돌리면 §3·§4 **본문 HTML 이 통째로 다시 쓰인다**. Fig. 2 의 끝점
     필터 결함(⏭-NOW-l)을 고칠 때 한 번에 재생성하기로 미뤄 둔 상태라, 지금
     건드리면 그 diff 와 섞인다.
Fig. 2 를 대체할 후보다 (1저자 2026-09-17: *"이 plot 그래프가 그렇게 직관적이지도
않은거 같아"*). 대체가 확정되면 저 생성기로 옮기고 이 파일을 지운다.

두 패널
-------
(a) 사다리 — 가로 전압, 세로 **P 를 받은 상의 Li/P**. 점 하나가 (조건, 수용상) 하나다.
    굵은 계단선은 그 전압에서 살아 있는 **가장 비싼 방**(max Li/P). 수평 점선은
    §3 의 부호 반전선 Li/P ≈ 1.67 — 그 아래에서 Nd 경로가 이긴다.
(b) 행선지 — 같은 점들을 **방 주인**으로 나눠 100 % 스택. Nd 없음 / Nd 있음 두 막대.
    "Nd 가 없으면 P2S7" 이 아니라 "Nd 가 없으면 **양극의 전이금속을 먹는다**" 가 보인다.

⛔ 이 그림이 못 하는 것
  · **최소 꺾임 하나만** 본다 (Fig. 2 와 같은 한정). 나머지 꺾임은 안 본다.
  · 계수를 안 본다 — "P 가 몇 mol 갔나" 가 아니라 "어느 상이 받았나" 다.
    그래서 세로축을 *양*으로 읽으면 안 된다.
  · 끝점(x=0/1) 조건은 레코드 단계에서 이미 빠졌다 (자체분해라 계면 산물이 아니다).
  · 속도·수송은 없다 — 전부 0 K 열역학이다.

  python3 tools/figures/plot_cei_p_host_ladder.py [--selftest]
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))

REC = ROOT / "db/properties/cei_p_host_ladder_2026_09_17.json"
OUT = ROOT / "db/properties/cei_figs"
VS = [2.5, 3.0, 3.5, 4.0, 4.3, 4.5]
ND_BEARING = {"nd_only", "modelc_nd"}
CROSSOVER = 1.67          # §3 · cei_li_budget_ladder.csv 의 부호 반전 Li/P

#: 방 주인 분류. **순서가 규칙이다** — 위에서부터 처음 맞는 것으로 정한다.
#:   ⛔ LiMnPO4 처럼 Li 와 전이금속을 **둘 다** 가진 상이 있다. 순서를 안 정하면
#:     같은 상이 판마다 다른 칸에 들어간다 (조용히 틀린 경로).
TM = ("Co", "Ni", "Mn")
CLASSES = [
    ("P–S (thiophosphate)",      "#c05621"),
    ("Nd phosphate",             "#6d28d9"),
    ("Li phosphate (Li/P ≥ 1)",  "#0d9488"),
    ("TM phosphate (Li/P = 0)",  "#0284c7"),
    ("P–Cl escape (PCl$_5$)",    "#9ca3af"),
]


def classify(formula, li_per_P, anion):
    """수용상 → 방 주인 칸. 규칙은 **위에서부터 처음 맞는 것**이다.

    ⛔ 못 하는 것: 화학적으로 옳은 분류가 아니라 **이 그림의 표시 규칙**이다.
      LiMnPO4(Li/P = 1, Mn 포함)는 'Li phosphate' 로 간다 — Li 를 쓰는 것이
      이 그림의 축이기 때문이다. 캡션에 그렇게 적는다.
    """
    if anion == "P-S":
        return CLASSES[0][0]
    if "Nd" in formula:
        return CLASSES[1][0]
    if li_per_P >= 1:
        return CLASSES[2][0]
    if any(t in formula for t in TM):
        return CLASSES[3][0]
    return CLASSES[4][0]        # 현재 레코드에서는 PCl5 뿐이다


def load(rec_path=REC):
    d = json.loads(Path(rec_path).read_text(encoding="utf-8"))
    pts = []
    for r in d["rows"]:
        for h in r["p_hosts"]:
            pts.append({"electrolyte": r["electrolyte"], "cathode": r["cathode"],
                        "voltage_V": r["voltage_V"], "formula": h["formula"],
                        "li_per_P": h["li_per_P"],
                        "nd_side": r["electrolyte"] in ND_BEARING,
                        "klass": classify(h["formula"], h["li_per_P"], h["anion"])})
    return d, pts


def rung(pts, V):
    """그 전압에서 살아 있는 가장 비싼 방 (max Li/P). 점이 없으면 None."""
    v = [p["li_per_P"] for p in pts if p["voltage_V"] == V]
    return max(v) if v else None


def median(pts, V):
    """그 전압 점들의 Li/P 중앙값. 점이 없으면 None (0 으로 그리지 않는다)."""
    v = sorted(p["li_per_P"] for p in pts if p["voltage_V"] == V)
    if not v:
        return None
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def stack(pts, V, nd_side):
    """(전압, Nd 유무) 의 방 주인 분포 → {칸: 비율}. 점이 없으면 빈 dict."""
    sel = [p for p in pts if p["voltage_V"] == V and p["nd_side"] is nd_side]
    if not sel:
        return {}
    n = len(sel)
    return {k: sum(p["klass"] == k for p in sel) / n for k, _ in CLASSES}


def _selftest():
    ok = True
    def chk(c, m):
        nonlocal ok
        ok &= bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    chk(classify("P2S7", 0.0, "P-S") == "P–S (thiophosphate)",
        "P–S 는 인산염 칸에 안 들어간다")
    chk(classify("LiNd(PO3)4", 0.25, "P-O") == "Nd phosphate",
        "[음성] Li 를 조금 가진 Nd 인산염도 Nd 칸이다 (Li/P 0.25 에 속지 않는다)")
    chk(classify("LiMnPO4", 1.0, "P-O") == "Li phosphate (Li/P ≥ 1)",
        "[음성] Li 와 전이금속을 둘 다 가진 상은 **순서 규칙**대로 Li 칸이다")
    chk(classify("Mn(PO3)2", 0.0, "P-O") == "TM phosphate (Li/P = 0)",
        "Li 없는 전이금속 인산염은 TM 칸이다")
    chk(classify("CoP4O11", 0.0, "P-O") != classify("Li3PO4", 3.0, "P-O"),
        "[음성] Li/P 0 과 3 이 같은 칸에 들어가지 않는다")

    _pts = [{"voltage_V": 2.5, "li_per_P": 3.0, "nd_side": False, "klass": CLASSES[2][0]},
            {"voltage_V": 2.5, "li_per_P": 0.0, "nd_side": True,  "klass": CLASSES[1][0]},
            {"voltage_V": 4.5, "li_per_P": 0.0, "nd_side": False, "klass": CLASSES[3][0]}]
    chk(rung(_pts, 2.5) == 3.0 and rung(_pts, 4.5) == 0.0,
        "칸(max Li/P)이 전압과 함께 내려간다")
    chk(rung(_pts, 3.5) is None,
        "[음성] 점이 없는 전압은 0 이 아니라 **None** 이다 (없는 값을 0 으로 안 그린다)")
    chk(median(_pts, 2.5) == 1.5 and median(_pts, 4.5) == 0.0,
        "중앙값이 짝수 개일 때 두 가운데의 평균이다")
    chk(median(_pts, 3.5) is None,
        "[음성] 점이 없는 전압의 중앙값은 0 이 아니라 None 이다")
    _s = stack(_pts, 2.5, False)
    chk(abs(sum(_s.values()) - 1.0) < 1e-9 and _s[CLASSES[2][0]] == 1.0,
        "스택이 100 % 로 정규화된다")
    chk(stack(_pts, 3.5, False) == {},
        "[음성] 점이 없는 칸은 빈 스택이다 (막대를 지어내지 않는다)")

    if REC.exists():
        _, pts = load()
        chk(all(rung(pts, a) >= rung(pts, b) for a, b in zip(VS, VS[1:])),
            "[실측] 실제 레코드에서 사다리가 단조 비증가다")
        chk(rung(pts, 2.5) == 3.0 and rung(pts, 4.5) == 0.0,
            "[실측] 2.5 V 는 3, 4.5 V 는 0")
    else:
        chk(False, f"레코드가 없다: {REC}")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from house_style import INK, MUT, apply_axes  # noqa: F401

    d, pts = load()
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.2, 4.4),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    xs = list(range(len(VS)))          # 범주형 — 4.3/4.5 가 실좌표면 겹친다
    cmap = dict(CLASSES)

    # ── (a) 사다리 ────────────────────────────────────────────────────────
    rng = __import__("random").Random(0)          # 지터는 고정 시드 (판마다 안 흔들리게)
    for p in pts:
        x = xs[VS.index(p["voltage_V"])] + rng.uniform(-0.26, 0.26)
        axL.scatter(x, p["li_per_P"] + rng.uniform(-0.035, 0.035), s=26,
                    color=cmap[p["klass"]], alpha=.75, lw=.5, edgecolor="white", zorder=3)
    ru = [rung(pts, V) for V in VS]
    axL.step(xs, ru, where="mid", color=INK, lw=2.2, zorder=4)
    axL.scatter(xs, ru, s=44, color=INK, zorder=5)
    # ⚠ max 만 그리면 3.0 V 가 안 내려간 것처럼 보인다 (한 조건의 Li3PO4 가 칸을 붙든다).
    #   같은 점들의 중앙값을 얇게 같이 그린다 — 둘 다 정의된 통계다.
    md = [median(pts, V) for V in VS]
    axL.step(xs, md, where="mid", color=MUT, lw=1.4, ls="--", zorder=4)
    # ⚠ 인라인 라벨을 두 번 옮겼는데 "median" 이 1.67 점선 위에 얹혔다.
    #   선 범례로 바꾼다 — 점 구름이 어디에 있든 안 겹친다.
    axL.plot([], [], color=INK, lw=2.2, label="max over all conditions")
    axL.plot([], [], color=MUT, lw=1.4, ls="--", label="median")
    axL.legend(frameon=False, fontsize=8.2, loc="upper right",
               bbox_to_anchor=(1.0, 1.02), handlelength=1.8)
    axL.axhline(CROSSOVER, color="#92400e", ls=":", lw=1.4, zorder=2)
    axL.text(-0.45, CROSSOVER + .10,
             f"sign flip of the Nd$\\leftarrow$Li exchange  (Li/P $\\approx$ {CROSSOVER})",
             fontsize=8, color="#92400e", ha="left")
    apply_axes(axL, "Voltage (V vs Li/Li$^+$)", "Li : P of the P-accepting phase")
    axL.set_xticks(xs); axL.set_xticklabels([f"{v:g}" for v in VS])
    axL.set_xlim(-0.55, len(VS) - 0.45); axL.set_ylim(-0.25, 3.35)
    axL.set_title("(a)  Voltage locks the Li-paying rooms, one rung at a time",
                  fontsize=10, color=INK, pad=8, loc="left")

    # ── (b) 행선지 100 % 스택 ─────────────────────────────────────────────
    w = 0.38
    for j, (nd, off, lab) in enumerate(((False, -w / 2 - .02, "no Nd"),
                                        (True, w / 2 + .02, "with Nd"))):
        for i, V in enumerate(VS):
            bot = 0.0
            for k, col in CLASSES:
                frac = stack(pts, V, nd).get(k, 0.0)
                if frac <= 0:
                    continue
                axR.bar(i + off, frac * 100, width=w, bottom=bot * 100, color=col,
                        edgecolor="white", lw=.6, zorder=3)
                bot += frac
        _ = lab   # 막대 위 라벨은 폭이 좁아 겹친다 — 아래 한 줄 설명으로 대신한다
    apply_axes(axR, "Voltage (V vs Li/Li$^+$)", "Share of P-accepting phases (%)")
    axR.set_xticks(xs); axR.set_xticklabels([f"{v:g}" for v in VS])
    axR.set_ylim(0, 112); axR.set_yticks([0, 25, 50, 75, 100])
    axR.text(-0.55, 106, "at each voltage:  left bar = no Nd   ·   right bar = with Nd",
             fontsize=8, color=MUT, ha="left")
    axR.set_title("(b)  The Nd-free route is the cathode's own metal, not P$_2$S$_7$",
                  fontsize=10, color=INK, pad=8, loc="left")
    axR.legend(handles=[Patch(facecolor=c, label=k) for k, c in CLASSES],
               frameon=False, fontsize=7.6, ncol=2, loc="lower left",
               bbox_to_anchor=(0.0, -0.40))

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.28)
    png = OUT / "cei_p_host_ladder.png"
    fig.savefig(png, dpi=300); plt.close(fig)

    # Origin-ready CSV — 열 이름을 명시한다
    csv_path = OUT / "cei_p_host_ladder_fig.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w2 = csv.writer(f)
        w2.writerow(["panel", "voltage_V", "electrolyte", "cathode",
                     "p_host_formula", "li_per_P", "host_class", "nd_side"])
        for p in pts:
            w2.writerow(["a", p["voltage_V"], p["electrolyte"], p["cathode"],
                         p["formula"], p["li_per_P"], p["klass"],
                         "with_Nd" if p["nd_side"] else "no_Nd"])
        w2.writerow([])
        w2.writerow(["panel", "voltage_V", "rung_max_li_per_P"])
        for V in VS:
            w2.writerow(["a_rung", V, rung(pts, V)])
        w2.writerow([])
        w2.writerow(["panel", "voltage_V", "nd_side", "host_class", "share_percent"])
        for V in VS:
            for nd in (False, True):
                for k, _ in CLASSES:
                    fr = stack(pts, V, nd).get(k, 0.0)
                    if fr > 0:
                        w2.writerow(["b", V, "with_Nd" if nd else "no_Nd",
                                     k, round(fr * 100, 4)])
    print(f"{len(pts)} 수용상 · 사다리 {[rung(pts, V) for V in VS]}")
    print(f"→ {png}\n→ {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest() if "--selftest" in sys.argv else main())
