#!/usr/bin/env python3
"""Fig. 3 — Nd 가 고전압에서 P 를 가로채 양극 TM 의 인산염 소모를 막는다.

자료: db/properties/cei_figs/cei_nd_protection_allcells.csv (120 행 · 4 양극 × 6 전압 × 5 농도)
기록: db/properties/cei_protection_allcells_result_2026_09_21.json
카드: db/properties/cei_protection_allcells_prereg_2026_09_21.json (결과 보기 전 봉인)

⭐ 2026-09-21 개정 — 전조건 라운드로 자료가 34 행 → **120 행**이 됐다. 바뀐 것 셋:
  · (a) 곡선이 둘 → **셋**. NMC811 이 처음 들어왔다 (Ni-rich 고전압 양극).
  · (b) 를 **예측 vs 실측 산점도**로 바꿨다. 옛 (b)(P 행선지 막대)는 이번 라운드가
    답한 더 큰 질문 — *"식이 언제 맞고 언제 안 맞나"* — 에 자리를 내줬다.
    ⚠ 옛 (b) 의 P₂S₇ 누출 이야기는 G2 게이트와 §2b 본문에 남아 있다.
  · (c) 제목이 "둘만 산다" → 실제 생존 수로 바뀐다 (자료에서 센다 — 손으로 안 적는다).

⛔ 이 그림이 **하지 않는 것**
  · 게이트 탈락 칸을 (a) 에 그리지 않는다 — 대신 (c) 가 왜 탈락했는지를 그린다.
    (조용히 버리면 "왜 몇 점뿐이지" 가 된다.)
  · 속도·두께·연속성을 말하지 않는다. 0 K hull 열역학이다.
  · 절대 반응에너지를 쓰지 않는다 (Li 장부 교란 — 감사 기록 참조).
  · **(b) 의 대각선 이탈을 "계산 오차" 로 읽지 않는다** — 예측은 **P** 를 세고 실측은
    **TM** 을 센다. 둘이 같아지는 것은 가로챈 P 가 원래 TM 에게 갈 P 였을 때뿐이다.

색 규약: Nd 는 하우스 팔레트에 #db2777 이지만 이 family(Fig. 1)가 O(crimson)와
  안 갈려 보라 #6d28d9 로 고정했다. 양극은 원소가 아니라 조건이므로 원소 팔레트를
  쓰지 않고 **명도 램프**로 가른다 (Fig. 5 가 전압을 그렇게 처리한 관례).
"""
import csv, pathlib, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from house_style import INK, MUT, apply_axes  # noqa: E402

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC = REPO / "db/properties/cei_figs/cei_nd_protection_allcells.csv"
OUT = REPO / "db/properties/cei_figs"

ND_DARK, ND_MID, ND_LIGHT = "#6d28d9", "#8b5cf6", "#a78bfa"   # 명도 램프 (양극 = 조건)
OKC, BADC, TMP = "#0d9488", "#be123c", "#6b7280"
WARNC = "#c05621"          # 하우스 팔레트의 S — 여기선 "곡선이 아닌 열" 표식
DX_MAX = 0.05

#: (a) 에 그리는 열 — **식이 전 농도에서 맞는 열**이다. 기록 §✅_식이_잘_맞는_열 과 같아야 한다.
#: ⛔ k 를 여기 손으로 적지 않는다 — 자료의 k_observed 에서 읽고, 열 안에서 갈리면 죽는다.
CLEAN = [("LiCoO2", 4.3, ND_DARK,  "o"),
         ("LiNiO2", 3.5, ND_MID,   "s"),
         ("NMC811", 3.5, ND_LIGHT, "^")]
TEX = {"NdPO4": "NdPO$_4$", "Nd(PO3)3": "Nd(PO$_3$)$_3$",
       "LiNd(PO3)4": "LiNd(PO$_3$)$_4$", "NdP5O14": "NdP$_5$O$_{14}$"}


SAT = 0.995   #: 이 위는 **포화**다 — min(1,·) 가 걸려 k 가 뭐든 예측이 같다


def _column_k(cat, V, pts):
    """열 하나의 k — **포화 안 된 점에서만** 읽는다.

    왜 나누나: 보호율이 100 % 에 붙은 점에서는 min(1, k·x/(1−x)) 가 k 에 무감각하다.
    실제로 LiCoO₂@4.30 은 x=0.20 에서 hull 이 상을 섞어(NdP₅O₁₄|Nd(PO₃)₃) k 가 5 → 4 로
    떨어지는데, 그 점은 이미 포화라 곡선이 안 바뀐다. 그걸 "k 가 갈렸다" 로 읽으면
    멀쩡한 열을 버리고, 반대로 평균을 내면 **안 포화된 구간의 곡선이 틀어진다**.
    ⇒ 포화 점은 k 판정에서 빼고, 뺀 뒤에도 갈리면 **죽는다**.

    ⛔ 이 함수가 못 하는 것: 포화 점이 정말 포화인지는 실측 보호율로만 본다
      (예측으로 보면 순환이다). 열 전체가 포화면 k 를 못 정하고 죽는다.
    """
    unsat = [r for r in pts if r["k_observed"] is not None
             and r["protection_observed"] is not None and r["protection_observed"] < SAT]
    ks = {r["k_observed"] for r in unsat}
    if len(ks) != 1:
        raise SystemExit(f"⛔ {cat}@{V} 의 k 가 **포화 안 된 점에서** 갈린다 {sorted(ks)} — "
                         "한 곡선으로 못 그린다. CLEAN 에서 빼거나 열을 나눠라")
    k = ks.pop()
    #: ⛔ 2026-09-21 정정 (외부 리뷰). 첫 판은 뺀 점을 **공통 k** 로 검사했다.
    #  그러면 그 행의 k 가 달라도 공통 k 가 포화를 주는 한 통과해서, 실제로는 그 행의
    #  예측이 포화가 아닌데도 100 % 곡선을 그렸다 (x=0.20·자기 k=3 이면 예측 75 %).
    #  포화라서 빼도 되는 근거는 **그 행 자신의 k 로도 포화일 때**만 성립한다.
    for r in pts:
        if r["protection_observed"] is not None and r["protection_observed"] >= SAT:
            kr = r["k_observed"] if r["k_observed"] is not None else k
            if min(1.0, kr * r["x_Nd"] / (1 - r["x_Nd"])) < SAT:
                raise SystemExit(f"⛔ {cat}@{V} x={r['x_Nd']} 는 실측이 포화인데 "
                                 f"**그 행의 k={kr:g}** 예측은 포화가 아니다 "
                                 f"({min(1.0, kr * r['x_Nd'] / (1 - r['x_Nd']))*100:.0f} %) — "
                                 "포화로 빼면 안 되는 점이다. 한 곡선으로 못 그린다")
    return k


def load():
    rows = []
    with SRC.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            def f(k):
                v = r.get(k, "")
                return float(v) if v not in ("", "None") else None
            rows.append({"cathode": r["cathode"], "voltage_V": f("voltage_V"),
                         "x_Nd": f("x_Nd"), "delta_x": f("delta_x"),
                         "gate_pass": r["gate_pass"] == "True",
                         "protection_observed": f("protection_observed"),
                         "P_taken_by_Nd": f("P_taken_by_Nd"),
                         "k_observed": f("k_observed"),
                         "nd_phases": r.get("nd_phases", ""),
                         "gate_fail_reason": r.get("gate_fail_reason", "")})
    return rows


def _col(rows, cat, V, only_pass=True):
    return sorted((r for r in rows if r["cathode"] == cat and abs(r["voltage_V"] - V) < 1e-9
                   and (r["gate_pass"] or not only_pass)), key=lambda r: r["x_Nd"])


def _full_pass(rows):
    """전 농도 통과 열 — **자료에서 센다**. 손으로 적으면 자료가 바뀔 때 갈린다.

    ⛔ 2026-09-21 정정 (외부 리뷰). 첫 판은 남아 있는 행의 `all(gate_pass)` 만 봤다.
    그러면 **농도가 빠져도** 전 농도 통과로 올라간다 — 실패한 행을 지우기만 해도
    승격됐고, 농도 하나를 중복시켜도 안 걸렸다. 그래서 **기대 농도 집합**(자료 전체의
    x 합집합)을 만들고, 그것과 정확히 같은 집합을 가진 열만 인정한다.
    """
    want = {round(r["x_Nd"], 6) for r in rows}
    cols = {}
    for r in rows:
        cols.setdefault((r["cathode"], r["voltage_V"]), []).append(r)
    out = []
    for c, v in cols.items():
        xs = [round(r["x_Nd"], 6) for r in v]
        if len(xs) != len(set(xs)):
            raise SystemExit(f"⛔ {c[0]}@{c[1]} 에 농도가 중복돼 있다 {sorted(xs)} — 자료가 깨졌다")
        if set(xs) == want and all(r["gate_pass"] for r in v):
            out.append(c)
    return sorted(out)


def _non_monotonic(rows):
    """실측 보호율이 x 를 따라 **한 번이라도 줄어드는** 열 — 자료에서 찾는다.

    왜 필요한가: 그런 열은 게이트를 통과해도 **곡선이 아니다**(최소 꺾임이 농도마다 다른
    가지로 튄다). (b) 에서 대각선 한참 위에 놓이는데, 표시를 안 하면 "식이 과소예측한다"
    로 잘못 읽힌다. ⚠ 이것은 **게이트가 아니다** — 걸러내지 않고 **표시만** 한다
    (결과를 보고 문턱을 만들면 사전등록이 죽는다).
    """
    #: 범위를 **전 농도 통과 열**로 못박는다. 통과·탈락이 섞인 열은 남은 점이 성긴 것이지
    #  "단조롭지 않은" 것이 아니다 — 범위를 안 적으면 3 과 5 가 갈린다(2026-09-21 실측).
    out = set()
    for c in _full_pass(rows):
        ys = [r["protection_observed"] for r in _col(rows, *c)
              if r["protection_observed"] is not None]
        if any(b < a - 1e-9 for a, b in zip(ys, ys[1:])):
            out.add(c)
    return out


def panel_a(ax, rows):
    """(a) 보호 곡선 — 식은 맞춘 매개변수가 0 이다. k 는 자료에서 읽는다."""
    xs = np.linspace(0.0, 0.22, 300)
    for cat, V, col, mk in CLEAN:
        pts = _col(rows, cat, V)
        if not pts:                     # _preflight 가 먼저 잡지만 이중으로 둔다
            raise SystemExit(f"⛔ CLEAN 열 {cat}@{V} V 가 비었다")
        k = _column_k(cat, V, pts)
        #: 상 라벨도 k 와 **같은 점들**(포화 전)에서 읽는다. 포화 점은 hull 이 상을 섞어
        #  내서 "NdP5O14|Nd(PO3)3" 처럼 나오고, 그걸 라벨로 쓰면 빈칸이 된다(2026-09-21 실측).
        ph = {r["nd_phases"] for r in pts
              if r["protection_observed"] is not None and r["protection_observed"] < SAT}
        lab_ph = TEX.get(ph.pop(), "") if len(ph) == 1 else "mixed"
        ax.plot(xs, np.minimum(1.0, k * xs / (1 - xs)) * 100, "--",
                color=col, lw=1.3, alpha=.75, zorder=1)
        ax.plot([r["x_Nd"] for r in pts], [r["protection_observed"] * 100 for r in pts],
                mk, color=col, ms=7, mec="white", mew=1.1, zorder=3,
                label=f"{cat}  {V:.1f} V   $k$ = {k:.0f}  ({lab_ph})")
    ax.axhline(100, color=MUT, lw=.8, ls=":", zorder=0)
    ax.axvline(0.02, color=MUT, lw=.8, ls=":", zorder=0)
    ax.annotate("target\ncomposition", xy=(0.02, 10.3), xytext=(0.003, 34),
                fontsize=9, color=MUT,
                arrowprops=dict(arrowstyle="->", color=MUT, lw=.9,
                                connectionstyle="arc3,rad=-0.25"))
    ax.text(.004, 62, r"$\min\left(1,\ k\,\dfrac{x_{\mathrm{Nd}}}{1-x_{\mathrm{Nd}}}\right)$"
                      "\n(dashed, no fitted parameter)", fontsize=10, color=INK, va="center")
    ax.set_xlim(0, .22); ax.set_ylim(-4, 112)
    apply_axes(ax, "Nd content $x$ in Li$_{5.4+2x}$Nd$_x$P$_{1-x}$S$_{4.37}$O$_{0.03}$Cl$_{1.6}$",
               "Cathode TM spared from phosphate (%)",
               "(a)  One Nd sequesters $k$ phosphorus")
    ax.legend(frameon=False, fontsize=8.6, loc="lower right", labelcolor=INK)


def panel_b(ax, rows):
    """(b) 예측(P 가로챔) vs 실측(TM 아낌) — **둘은 다른 양이다**.

    대각선 위 = 가로챈 P 가 그대로 TM 을 아꼈다. 아래(특히 y = 0) = P 는 가로챘는데
    TM 은 안 아꼈다 — TM 이 그 P 를 노리고 있지 않았다는 뜻이다.
    """
    full = set(_full_pass(rows))
    nonmono = _non_monotonic(rows)
    #: 무엇이 빠지는지 **세어서 그림에 적는다**. 캡션이 "every comparable column" 이라고
    #  적혀 있었는데 실제로는 k 없는 열을 조용히 뺐다 (2026-09-21 외부 리뷰).
    have = {c for c in full
            if any(r["protection_observed"] is not None
                   for r in rows if (r["cathode"], r["voltage_V"]) == c)}
    drawn = {c for c in have
             if any(r["protection_observed"] is not None and r["k_observed"] is not None
                    for r in rows if (r["cathode"], r["voltage_V"]) == c)}
    skipped = sorted(have - drawn)
    ax.plot([0, 100], [0, 100], "-", color=MUT, lw=1.0, zorder=1)
    ax.fill_between([0, 100], [-5, 95], [5, 105], color=OKC, alpha=.10, zorder=0)
    seen = set()
    for r in rows:
        if not r["gate_pass"] or r["protection_observed"] is None or r["k_observed"] is None:
            continue
        col = (r["cathode"], r["voltage_V"])
        if col not in full:
            continue
        x = r["x_Nd"]
        pred = min(1.0, r["k_observed"] * x / (1 - x)) * 100
        obs = r["protection_observed"] * 100
        lo = r["voltage_V"] <= 3.0 and obs <= 1.0
        nm = col in nonmono
        #: 세 갈래 — 정상 · TM 이 그 P 를 안 노림(y=0) · **곡선이 아닌 열**(속 빈 표식).
        #  세 번째를 안 나누면 대각선 위 점들이 "식이 과소예측" 으로 읽힌다.
        if nm:
            kw = dict(mfc="none", mec=WARNC, mew=1.4, color=WARNC)
            lab = "not monotonic in $x$ — not a curve"
            key = "nm"
        elif lo:
            kw = dict(color=BADC, mec="white", mew=.8)
            lab = "TM was not competing for that P"
            key = "lo"
        else:
            kw = dict(color=ND_DARK, mec="white", mew=.8)
            lab = "comparable columns"
            key = "hi"
        ax.plot(pred, obs, "o", ms=6, alpha=.85, zorder=3,
                label=(lab if key not in seen else None), **kw)
        seen.add(key)
    ax.set_xlim(-3, 105); ax.set_ylim(-8, 108)
    ax.text(66, 14, "predicted P intercepted\nbut no TM spared", fontsize=8.6,
            color=BADC, ha="center", va="center", linespacing=1.35)
    if skipped:
        names = ", ".join(f"{c[0]} {c[1]:.1f} V" for c in skipped)
        #: 범례 바로 아래 빈 자리에 둔다 — y=0 의 빨간 점 위에 얹으면 둘 다 안 읽힌다.
        ax.text(1, 74,
                f"{len(drawn)} of {len(have)} columns drawn\n"
                f"({names} has no $k$: 0 vs 0)",
                fontsize=7.8, color=MUT, ha="left", va="top", linespacing=1.35,
                bbox=dict(fc="white", ec="none", alpha=.85, pad=2.0))
    ax.text(84, 72, "$\\pm$5 %p", fontsize=8.6, color="#0f766e", va="center",
            ha="center", rotation=42)
    apply_axes(ax, "Predicted: share of P taken by Nd (%)",
               "Measured: cathode TM spared (%)",
               "(b)  The rule holds where TM competes for the P")
    ax.legend(frameon=False, fontsize=8.6, loc="upper left", labelcolor=INK,
              bbox_to_anchor=(0.0, 1.0), handletextpad=.4)


def panel_c(ax, rows):
    """(c) 게이트 — **열 단위**로 그린다. 점만 뿌리면 "어느 열이 살았나" 를 못 읽는다."""
    ax.axhspan(0, DX_MAX, color="#dcfce7", zorder=0)
    ax.axhline(DX_MAX, color="#16a34a", lw=1.0, zorder=1)
    #: 라벨은 녹색 선 **바로 위 오른쪽**에 둔다 — 띠 안은 실선 자료가 꽉 차 있다.
    ax.text(.222, DX_MAX * 1.10, f"$\\Delta x \\leq$ {DX_MAX:.2f}  comparable",
            fontsize=9, color="#166534", ha="right", va="bottom",
            bbox=dict(fc="white", ec="none", alpha=.85, pad=1.6))
    survivors = set(_full_pass(rows))
    ramp = {"LiCoO2": ND_DARK, "LiNiO2": ND_MID, "NMC811": ND_LIGHT, "LiMnO2": "#c4b5fd"}
    for cat, V in sorted({(r["cathode"], r["voltage_V"]) for r in rows}):
        pts = [r for r in _col(rows, cat, V, only_pass=False) if r["delta_x"] is not None]
        if not pts:
            continue
        live = (cat, V) in survivors
        col = ramp.get(cat, MUT)
        ax.plot([r["x_Nd"] for r in pts], [r["delta_x"] for r in pts],
                "-" if live else ":", color=col if live else MUT,
                lw=1.7 if live else .9, alpha=1 if live else .5,
                marker="o" if live else None, ms=4.5, mec="white", mew=.8,
                zorder=4 if live else 2)
    for cat, c in ramp.items():
        ax.plot([], [], "-", color=c, lw=1.7, label=cat)
    #: ⛔ 상한을 0.20 으로 박아 뒀더니 **가장 크게 탈락한 두 점**(0.2448 · 0.2883)이
    #  표시도 없이 잘려 나갔다 (2026-09-21 외부 리뷰). 탈락 정도를 보여주는 패널에서
    #  제일 큰 값을 못 읽으면 패널이 제 일을 못 한다. ⇒ 상한을 **자료에서** 잡는다.
    dmax = max((r["delta_x"] for r in rows if r["delta_x"] is not None), default=DX_MAX)
    ax.set_xlim(0, .225); ax.set_ylim(0, dmax * 1.08)
    apply_axes(ax, "Nd content $x$", "$|\\Delta x_{\\mathrm{mix}}|$ vs lithium-matched control",
               f"(c)  {len(survivors)} of "
               f"{len({(r['cathode'], r['voltage_V']) for r in rows})} columns survive")
    #: ⛔ 종전 문구는 점선을 **전부** "혼합비 이동" 으로 설명했다. 실제로는 점선 선택이
    #  전체 게이트 결과라, LiMnO₂ 4.5 V 처럼 Δx 는 0.001–0.002 로 멀쩡한데 끝점·P₂S₇
    #  사유로 탈락한 열도 점선이다 (2026-09-21 외부 리뷰). 사유를 갈라 적는다.
    ax.text(.004, dmax * 1.045,
            "solid = every concentration comparable\n"
            "dotted = some concentration failed a gate\n"
            "  above the line = the comparability gate itself\n"
            "  below it = the thiophosphate or endpoint gate",
            fontsize=8.5, color=MUT, va="top",
            bbox=dict(fc="white", ec="none", alpha=.85, pad=2.4))
    ax.legend(frameon=False, fontsize=8.6, loc="center right", labelcolor=INK,
              bbox_to_anchor=(1.0, .62))


PANELS = {"a": (panel_a, "One Nd sequesters k P"),
          "b": (panel_b, "The rule holds where TM competes"),
          "c": (panel_c, "How many columns survive")}
#: 패널 하나당 폭. 3패널 13.2 인치를 그대로 나눈 값이라 `--panels abc` 가 원본과 같다.
PANEL_W, FIG_H = 4.4, 4.3


def _preflight(which, rows):
    """그리기 **전에** 죽는다 — 잘못된 PNG 를 남기지 않으려고.

    ⛔ 2026-09-21 추가 (외부 리뷰). 종전에는 panel_a 가 없는 CLEAN 열을 조용히 건너뛰고
    그림을 **저장한 뒤** CSV 단계에서야 죽었다 — 곡선 둘짜리 PNG 와 0 바이트 CSV 가
    남았다. 검증을 앞으로 당긴다.
    """
    if "a" not in which:
        return
    for cat, V, _, _ in CLEAN:
        pts = _col(rows, cat, V)
        if not pts:
            raise SystemExit(f"⛔ CLEAN 열 {cat}@{V} V 가 자료에 없다 — "
                             "조용히 빼고 그리지 않는다. CLEAN 을 고치거나 자료를 확인해라")
        _column_k(cat, V, pts)          # k 가 못 정해지면 여기서 죽는다


def build(which="abc", out=None, rows=None):
    rows = rows if rows is not None else load()
    bad = [w for w in which if w not in PANELS]
    if bad:
        raise SystemExit(f"⛔ 모르는 패널 {bad} — 있는 것은 {sorted(PANELS)}")
    if not which:
        raise SystemExit("⛔ 패널을 하나도 안 골랐다")
    which = "".join(dict.fromkeys(which))   # 중복 패널은 합친다 (abca → abc)
    _preflight(which, rows)
    fig, axs = plt.subplots(1, len(which), figsize=(PANEL_W * len(which), FIG_H))
    axs = np.atleast_1d(axs)
    for ax, w in zip(axs, which):
        PANELS[w][0](ax, rows)
    fig.tight_layout()
    png = pathlib.Path(out) if out else (OUT / ("cei_nd_protection.png" if which == "abc"
                                                else f"cei_nd_protection_{which}.png"))
    fig.savefig(png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return png


def write_pred_csv(xs=None, out=None, rows=None):
    """예측선 Origin CSV (실측점은 cei_nd_protection_allcells.csv 에 이미 있다).

    `out`·`rows` 는 selftest 용이다 — 시험이 db/ 의 정본을 덮어쓰지 않게.
    """
    rows = load() if rows is None else rows
    xs = xs if xs is not None else np.linspace(0, 0.22, 111)
    p = pathlib.Path(out) if out else OUT / "cei_nd_protection_fig.csv"
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        hdr = ["x_Nd"]
        ks = []
        for cat, V, _, _ in CLEAN:
            pts = _col(rows, cat, V)
            #: ⛔ 여기서 k 를 따로 세지 않는다. 첫 판은 `{r["k_observed"]}` 의 원소가 1 개일
            #  때만 쓰고 아니면 **조용히 건너뛰었다** — LiCoO2 4.30 V 는 포화점 k 가 4 라
            #  집합이 {4,5} 가 되고, 그림의 주연 곡선이 CSV 에서 **말없이 빠졌다**
            #  (2026-09-21 실측: 세 열 중 두 열만 나왔다). 그림과 CSV 가 갈리면 안 되므로
            #  panel_a 와 **같은 함수**로 읽고, 못 읽으면 죽는다.
            if not pts:
                raise SystemExit(f"⛔ {cat} {V} V 열이 비었다 — CSV 를 쓸 수 없다")
            k = _column_k(cat, V, pts)
            ks.append((cat, V, k))
            hdr.append(f"protection_pct_{cat}_{V:g}V_k{k:g}")
        w.writerow(hdr)
        for x in xs:
            w.writerow([round(float(x), 5)] +
                       [round(float(min(1.0, k * x / (1 - x)) * 100), 4) for _, _, k in ks])
    return p


def _selftest():
    import copy as _cp, shutil as _sh, tempfile as _tf
    ok = True
    #: ⛔ /tmp 를 박아 쓰면 Windows 에서 FileNotFoundError 로 죽고, 공유 기계에서는
    #  두 세션이 같은 이름을 두고 경합한다 (2026-09-21 외부 리뷰 · 실제 재현됨).
    TD = _tf.mkdtemp(prefix="pcap_selftest_")

    def tp(name):
        return str(pathlib.Path(TD) / name)

    def chk(c, m):
        nonlocal ok
        ok = ok and bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    try:
        _selftest_body(chk, tp, _cp)
    finally:
        _sh.rmtree(TD, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def _selftest_body(chk, tp, _cp):
    rows = load()
    chk(len(rows) == 120, f"[양성] 자료 120 행 (실측 {len(rows)})")
    npass = sum(1 for r in rows if r["gate_pass"])
    chk(npass == 101 and len(rows) - npass == 19,
        f"[양성] 통과 {npass} · 탈락 {len(rows)-npass} 행도 CSV 에 남아 있다")
    full = _full_pass(rows)
    chk(len(full) == 17, f"[양성] 전 농도 통과 열 {len(full)} (자료에서 셈)")
    chk(all(_col(rows, c, v) for c, v, _, _ in CLEAN),
        "[양성] (a) 가 그리는 세 열이 자료에 있다")
    chk(("NMC811", 3.5) in full,
        "[양성] NMC811 3.5 V 가 전 농도 통과다 — 이 개정의 이유다")
    # ⛔음성 — 열 안에서 k 가 갈리면 한 곡선으로 그리지 않고 죽는다
    bad = _cp.deepcopy(rows)
    for r in bad:                       # x=0.02 는 포화가 아니다 — 여기를 깨야 잡혀야 한다
        if r["cathode"] == "LiCoO2" and abs(r["voltage_V"] - 4.3) < 1e-9 and r["x_Nd"] == 0.02:
            r["k_observed"] = 99.0
    died = False
    try:
        build("a", out=tp("bad.png"), rows=bad)
    except SystemExit as e:
        died = "갈린다" in str(e)
    chk(died, "[⛔음성] **포화 안 된 점**에서 k 가 갈리면 평균 내지 않고 죽는다")

    # ⛔음성 — 포화 점이라도 **그 행의 자기 k** 로 포화가 아니면 빼면 안 된다.
    #   ⚠ 첫 판은 이 입력을 "통과해야 하는 사례" 로 **축복했다**. k=3·x=0.20 이면
    #     그 행의 예측은 75 % 인데 공통 k=5 로 100 % 를 그렸다 (2026-09-21 외부 리뷰).
    sat_bad = _cp.deepcopy(rows)
    for r in sat_bad:
        if r["cathode"] == "LiCoO2" and abs(r["voltage_V"] - 4.3) < 1e-9 and r["x_Nd"] == 0.2:
            r["k_observed"] = 3.0       # 3×0.25 = 0.75 → 포화 아님
    died_sb = False
    try:
        build("a", out=tp("satbad.png"), rows=sat_bad)
    except SystemExit as e:
        died_sb = "포화로 빼면 안 되는 점" in str(e)
    chk(died_sb, "[⛔음성] 포화 점의 **자기 k** 예측이 포화가 아니면 죽는다 (75 % 를 100 % 로 안 그린다)")

    # [양성] 실제 자료처럼 자기 k 로도 포화면(4×0.25 = 1.0) 열을 버리지 않는다
    sat_ok = _cp.deepcopy(rows)
    for r in sat_ok:
        if r["cathode"] == "LiCoO2" and abs(r["voltage_V"] - 4.3) < 1e-9 and r["x_Nd"] == 0.2:
            r["k_observed"] = 4.0
    okpass = True
    try:
        build("a", out=tp("satok.png"), rows=sat_ok)
    except SystemExit:
        okpass = False
    chk(okpass, "[양성] 포화 점의 자기 k 로도 포화면(k=4·x=0.20) 열을 버리지 않는다")

    # ⛔음성 — 농도가 빠지거나 중복되면 '전 농도 통과' 로 안 올려준다
    miss = [r for r in _cp.deepcopy(rows)
            if not (r["cathode"] == "NMC811" and abs(r["voltage_V"] - 4.5) < 1e-9
                    and r["x_Nd"] == 0.2)]
    chk(("NMC811", 4.5) not in _full_pass(miss),
        "[⛔음성] 농도 하나가 빠진 열은 전 농도 통과가 아니다")
    drop_fail = [r for r in _cp.deepcopy(rows)
                 if not (r["cathode"] == "LiMnO2" and abs(r["voltage_V"] - 4.0) < 1e-9
                         and not r["gate_pass"])]
    chk(("LiMnO2", 4.0) not in _full_pass(drop_fail),
        "[⛔음성] 탈락 행을 지운다고 승격되지 않는다")
    dup = _cp.deepcopy(rows)
    for r in dup:
        if r["cathode"] == "NMC811" and abs(r["voltage_V"] - 4.5) < 1e-9 and r["x_Nd"] == 0.2:
            r["x_Nd"] = 0.15
    died_dup = False
    try:
        _full_pass(dup)
    except SystemExit as e:
        died_dup = "중복" in str(e)
    chk(died_dup, "[⛔음성] 농도가 중복되면 죽는다 (조용히 세지 않는다)")

    # ⛔음성 — CLEAN 열이 없으면 **그리기 전에** 죽는다 (잘못된 PNG 를 안 남긴다)
    nocol = [r for r in _cp.deepcopy(rows)
             if not (r["cathode"] == "NMC811" and abs(r["voltage_V"] - 3.5) < 1e-9)]
    png_missing = tp("nocol.png")
    died_nc = False
    try:
        build("a", out=png_missing, rows=nocol)
    except SystemExit as e:
        died_nc = "CLEAN 열" in str(e)
    chk(died_nc and not pathlib.Path(png_missing).exists(),
        "[⛔음성] CLEAN 열이 없으면 죽고 **PNG 를 안 남긴다**")
    # ── 단조성 탐지: (b) 가 세 갈래로 나눌 수 있어야 한다 ─────────────────────
    nm = _non_monotonic(rows)
    chk(("LiMnO2", 3.0) in nm,
        "[양성] LiMnO2 3.00 V 를 '곡선 아님' 으로 잡는다 (1.5→44.9→9.8→100→100 %)")
    chk(("LiCoO2", 4.3) not in nm,
        "[⛔음성] 단조로운 열(LiCoO2 4.30 V)은 잡지 않는다")
    flat = _cp.deepcopy(rows)                 # 전부 단조로 만들면 하나도 안 잡혀야 한다
    for r in flat:
        if r["protection_observed"] is not None:
            r["protection_observed"] = r["x_Nd"]
    chk(not _non_monotonic(flat),
        "[⛔음성] 전부 단조인 자료에서는 하나도 안 잡는다 (탐지가 항상 참이 아니다)")
    chk(len(nm) >= 1 and all(c in {(r["cathode"], r["voltage_V"]) for r in rows} for c in nm),
        f"[양성] 탐지된 열 {len(nm)} 개가 전부 자료에 있는 열이다")

    # ── 예측선 CSV: 그림과 **같은 열 수**여야 한다 ────────────────────────────
    #   왜 재나: 첫 판은 k 집합이 2 원소면 조용히 건너뛰어 **LiCoO2 4.30 V 가 빠졌다**.
    #   그림은 3 곡선, CSV 는 2 열 — 아무도 오류를 안 봤다.
    hdr = open(write_pred_csv(out=tp("pred.csv"), rows=rows),
               encoding="utf-8").readline().strip().split(",")
    chk(len(hdr) == 1 + len(CLEAN),
        f"[양성] 예측선 CSV 열 {len(hdr)-1} = 그림 곡선 {len(CLEAN)}")
    chk(all(any(f"{c}_{v:g}V" in x for x in hdr) for c, v, _, _ in CLEAN),
        "[양성] 세 열이 이름으로 전부 들어 있다 (LiCoO2 4.3 V 포함)")
    died3 = False
    try:
        write_pred_csv(out=tp("pred_bad.csv"), rows=bad)
    except SystemExit as e:
        died3 = "갈린다" in str(e)
    chk(died3, "[⛔음성] k 가 갈리는 열은 CSV 에서도 **건너뛰지 않고** 죽는다")
    # ⛔음성 — 모르는 패널
    died2 = False
    try:
        build("z", out=tp("bad2.png"), rows=rows)
    except SystemExit as e:
        died2 = "모르는 패널" in str(e)
    chk(died2, "[⛔음성] 모르는 패널 이름은 거부한다")
    # ⛔음성 — 되살린 가드 둘 (빈 선택 · 중복 패널)
    died4 = False
    try:
        build("", out=tp("empty.png"), rows=rows)
    except SystemExit as e:
        died4 = "하나도 안 골랐다" in str(e)
    chk(died4, "[⛔음성] 패널을 하나도 안 고르면 거부한다")
    f_dup = pathlib.Path(build("abca", out=tp("dup.png"), rows=rows))
    from PIL import Image as _Im
    w_dup = _Im.open(f_dup).size[0]
    w_abc = _Im.open(pathlib.Path(build("abc", out=tp("abc_ref.png"), rows=rows))).size[0]
    chk(abs(w_dup - w_abc) < 40, "[⛔음성] 중복 패널(abca)은 합쳐져 abc 와 같은 폭이다")
    chk(build.__defaults__[0] == "abc", "[양성] 기본 패널이 abc 다 (바뀌면 기존 그림이 조용히 달라진다)")
    for w in ("a", "b", "c", "abc"):
        f = pathlib.Path(build(w, out=tp(f"{w}.png"), rows=rows))
        chk(f.exists() and f.stat().st_size > 20000, f"[양성] --panels {w} 가 그려진다")


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--panels", default="abc",
                    help="그릴 패널 (기본 abc) — 부분집합이면 파일명이 달라진다")
    ap.add_argument("--out", default=None, help="저장 경로 (기본: cei_figs/ 아래 자동)")
    a = ap.parse_args(argv)
    png = build(a.panels, out=a.out)
    _p = pathlib.Path(png).resolve()
    print(f"✓ {_p.relative_to(REPO) if _p.is_relative_to(REPO) else _p}")
    if a.panels == "abc" and a.out is None:
        pc = write_pred_csv()
        print(f"✓ {pc.relative_to(REPO)}  (예측선; 실측점은 cei_nd_protection_allcells.csv)")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest() if "--selftest" in sys.argv else main())
