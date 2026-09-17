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
**2026-09-17: 대체가 확정됐다** (1저자 *"교체한것만 남겨줘"*). 옛 Fig. 2 (양극 개수
막대 집계) 를 저 생성기에서 지웠고, 이 파일이 **Fig. 2 번호를 승계**했다.
⚠ 애초 계획은 "대체가 확정되면 저 생성기로 옮기고 이 파일을 지운다" 였는데 **안 옮긴다** —
옛 그림이 사라진 지금 저기로 합칠 상대가 없고, 소스(ladder JSON)가 다른 채로 합치면
이 그림 하나 때문에 §3·§4 본문이 매번 다시 쓰인다. 파일을 나눠 두는 편이 싸다.

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
EXCH = ROOT / "db/properties/cei_tm_exchange_2026_09_17.json"
LADDER_CSV = ROOT / "db/properties/cei_figs/cei_li_budget_ladder.csv"
TIE = 0.30      # 구분되지 않는 폭 (eV/P) — D-2026-09-16-trivalent-dopant-phosphate-screen
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


LI_PER_P = {"Li3PO4": 3.0, "Li4P2O7": 2.0, "LiPO3": 1.0, "LiNd(PO3)4": 0.25,
            "Ni(PO3)2": 0.0, "NiP4O11": 0.0, "Mn(PO3)2": 0.0, "Mn2P2O7": 0.0,
            "MnP4O11": 0.0, "CoP4O11": 0.0}


def _tex(f):
    """Li3PO4 -> Li$_3$PO$_4$ (그림 라벨용. 영문·기호만 — 한글 안 쓴다)."""
    out, i = [], 0
    while i < len(f):
        if f[i].isdigit():
            j = i
            while j < len(f) and f[j].isdigit():
                j += 1
            out.append("$_{" + f[i:j] + "}$"); i = j
        else:
            out.append(f[i]); i += 1
    return "".join(out)


def exchange_map(exch_path=EXCH, ladder_csv=LADDER_CSV):
    """공여 인산염 → Nd←M 교환에너지 (eV/P). 두 레코드를 합친다.

    같은 형식 `<공여> + ½Nd2O3 -> NdPO4 + <산화물>` 이라 한 축에 놓을 수 있다.
    Li 쪽은 §3 의 사다리 CSV, 전이금속 쪽은 2026-09-17 의 교환 레코드다.

    ⛔ 못 하는 것
      · Nd 인산염(NdPO4·Nd(PO3)3·NdP5O14)은 **교환 상대가 자기 자신**이라 값이 없다.
        0 으로 채우지 않는다 — 키가 아예 없다.
      · Li+전이금속 혼합 인산염(LiMnPO4 등)과 P2S7·PCl5 는 아직 안 쟀다.
      · 눈금이 섞였다: Li 쪽은 전부 GGA, 전이금속 쪽은 인산염·산화물이 GGA+U 다.
        **부호만** 판정하고 순위는 TIE(0.30 eV/P) 안에서 안 가른다.
    """
    import csv as _csv
    out, src = {}, {}
    d = json.loads(Path(exch_path).read_text(encoding="utf-8"))
    for spec, r in d["reactions"].items():
        if r.get("ok"):
            out[spec.split(",")[0]] = r["E_eV_per_P"]; src[spec.split(",")[0]] = "tm_exchange"
    with open(ladder_csv, encoding="utf-8") as fh:
        for row in _csv.reader(fh):
            if len(row) >= 5 and row[0] and row[0] != "donor_phosphate":
                f, v = row[0], float(row[3])
                if f in out and abs(out[f] - v) > 1e-4:     # 두 레코드가 겹치면 대조가 된다
                    raise ValueError(f"{f}: 두 레코드가 어긋난다 {out[f]} vs {v}")
                out.setdefault(f, v); src.setdefault(f, "li_ladder")
    return out, src


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
    dE, _ = exchange_map()
    for q in pts:
        q["dE_exchange"] = dE.get(q["formula"])     # 없으면 None — 0 으로 안 채운다
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
    from house_style import INK, MUT, apply_axes

    d, pts = load()
    dE, src = exchange_map()
    have = [q for q in pts if q["dE_exchange"] is not None]
    miss = sorted({q["formula"] for q in pts if q["dE_exchange"] is None})

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.4, 4.6),
                                   gridspec_kw={"width_ratios": [1.1, 1]})
    xs = list(range(len(VS)))
    rng = __import__("random").Random(0)
    C_LI, C_TM, C_ND = "#0d9488", "#0284c7", "#6d28d9"

    def col(f):
        return C_ND if "Nd" in f else (C_TM if any(t in f for t in TM) else C_LI)

    # ── (a) 전압이 고르는 상대 ────────────────────────────────────────────
    for q in have:
        axL.scatter(xs[VS.index(q["voltage_V"])] + rng.uniform(-.26, .26),
                    q["dE_exchange"] + rng.uniform(-.03, .03), s=28,
                    color=col(q["formula"]), alpha=.75, lw=.5,
                    edgecolor="white", zorder=3)
    axL.axhspan(-TIE, TIE, color="#e5e7eb", zorder=1)
    axL.axhline(0, color=INK, lw=1.6, zorder=2)
    axL.text(-0.48, 2.02, "Nd LOSES the exchange", fontsize=8.6,
             color="#b91c1c", fontweight="bold")
    axL.text(-0.48, -2.60, "Nd WINS the exchange", fontsize=8.6,
             color=C_TM, fontweight="bold")
    axL.text(len(VS) - .55, TIE + .07, f"$\\pm${TIE:g} eV/P: not resolved",
             fontsize=7.4, color=MUT, ha="right")
    apply_axes(axL, "Voltage (V vs Li/Li$^+$)",
               "Nd$\\leftarrow$M exchange of the host  (eV per P)")
    axL.set_xticks(xs); axL.set_xticklabels([f"{v:g}" for v in VS])
    axL.set_xlim(-.55, len(VS) - .45); axL.set_ylim(-2.85, 2.30)
    axL.set_title("(a)  Voltage changes who Nd is competing against",
                  fontsize=10, color=INK, pad=8, loc="left")

    # ── (b) 교환 사다리 (§3 Fig. 4a 를 전이금속까지 넓힌 것) ─────────────
    # ⚠ Li/P = 0 에 여섯이 몰려서 라벨이 겹친다 — 세로로 벌려 지시선으로 잇는다.
    _slots, _used = sorted(dE.items(), key=lambda kv: -kv[1]), []
    for f, v in _slots:
        lp = LI_PER_P.get(f)
        if lp is None:
            continue
        axR.scatter(lp, v, s=74, color=col(f), lw=.6, edgecolor="white", zorder=4)
        ty = v
        while any(abs(ty - u) < 0.28 for u in _used):     # 겹치면 아래로 민다
            ty -= 0.28
        _used.append(ty)
        axR.annotate(_tex(f), (lp, v), (lp + 0.16, ty), textcoords="data",
                     fontsize=7.6, color=INK, va="center",
                     arrowprops=dict(arrowstyle="-", lw=.6, color=MUT,
                                     shrinkA=3, shrinkB=1)
                     if abs(ty - v) > 0.01 else None)
    axR.axhspan(-TIE, TIE, color="#e5e7eb", zorder=1)
    axR.axhline(0, color=INK, lw=1.6, zorder=2)
    axR.axvline(CROSSOVER, color="#92400e", ls=":", lw=1.3, zorder=2)
    axR.text(CROSSOVER + .06, 2.02, f"Li/P $\\approx$ {CROSSOVER}",
             fontsize=7.8, color="#92400e")
    apply_axes(axR, "Li : P of the donor phosphate", "Exchange energy (eV per P)")
    axR.set_xlim(-.45, 3.45); axR.set_ylim(-2.85, 2.30)
    axR.set_title("(b)  The same ladder, extended to the cathode's metals",
                  fontsize=10, color=INK, pad=8, loc="left")
    axR.legend(handles=[Patch(facecolor=C_LI, label="Li phosphate"),
                        Patch(facecolor=C_TM, label="transition-metal phosphate"),
                        Patch(facecolor=C_ND, label="already contains Nd")],
               frameon=False, fontsize=7.6, loc="lower right")

    fig.tight_layout()
    png = OUT / "cei_p_host_ladder.png"
    fig.savefig(png, dpi=300); plt.close(fig)

    csv_path = OUT / "cei_p_host_ladder_fig.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["panel", "voltage_V", "electrolyte", "cathode", "p_host_formula",
                    "li_per_P", "host_class", "nd_side", "exchange_eV_per_P"])
        for q in pts:
            w.writerow(["a", q["voltage_V"], q["electrolyte"], q["cathode"], q["formula"],
                        q["li_per_P"], q["klass"],
                        "with_Nd" if q["nd_side"] else "no_Nd",
                        "" if q["dE_exchange"] is None else q["dE_exchange"]])
        w.writerow([])
        w.writerow(["panel", "donor_phosphate", "li_per_P", "exchange_eV_per_P", "source"])
        for fo, v in sorted(dE.items(), key=lambda kv: -kv[1]):
            w.writerow(["b", fo, LI_PER_P.get(fo, ""), v, src[fo]])
    n_neg = {V: sum(1 for q in have if q["voltage_V"] == V and q["dE_exchange"] < 0)
             for V in VS}
    print(f"{len(have)}/{len(pts)} 점에 교환에너지 있음 ({len(have)/len(pts):.0%}) · "
          f"미측정 상 {len(miss)}: {', '.join(miss)}")
    print("전압별 '음수(Nd 이김)' 비율: " +
          "  ".join(f"{V:g}V {n_neg[V]}/{sum(1 for q in have if q['voltage_V']==V)}"
                    for V in VS))
    print(f"→ {png}\n→ {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_selftest() if "--selftest" in sys.argv else main())
