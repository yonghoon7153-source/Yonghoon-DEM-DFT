#!/usr/bin/env python3
"""plot_li_uptake_profile.py — grand-potential 사다리 (get_element_profile 꼴 `steps`) 를
전압–Li 흡수 계단 그림 (PNG · 하우스 스타일 · 영어 라벨) 과 Origin 용 CSV 로 바꾼다.

읽는 규칙 (HZ-esw-reduction-limit-label · 2026-09-22 정정과 같은 뜻)
  steps 의 행 [V, n, 반응식] = '임계 조성 (Li n 개 흡수 · 음수는 방출) 에서 Li 가 더 많은 쪽 면의 전위'.
  ⇒ n 오름차순으로 놓으면 행 k 의 V_k 는 구간 [n_k, n_{k+1}] 의 평탄 전위다.
     예 Li6PS5Cl: 1.717 V = 0 → 5 Li (→ 5 Li2S + LiCl + P) · 1.242 V = 5 → 5.143 (P → LiP7).
     1.242 를 '환원 시작' 으로 읽지 않는다 — 옛 도구의 off-by-one 이 바로 그 읽기였다.
  구간 끝 산물 = 다음 행 반응식의 오른쪽 (Li 항은 저장소라 뺀다). 마지막 행 (n 최대) 은 끝 상태다.

쓰는 법
  python3 tools/oxidation/plot_li_uptake_profile.py --esw db/properties/esw_lis4excluded.json \
      --label comp1 --name "Li6PS5Cl" --side reduction \
      --out_png docs/figures/sdi_agc/fig1_lpscl_li_uptake_profile.png \
      --out_csv db/properties/sdi_agc_lpscl_li_uptake_profile_2026_11_16.csv
  python3 tools/oxidation/plot_li_uptake_profile.py --selftest

이 도구가 못 하는 것
  - 사다리를 계산하지 않는다 (MP · pymatgen 없음) — esw 결과 JSON (`results.<label>.steps` 또는
    esw_grand_potential.py 의 `results.<label>.profile`) 을 읽기만 한다. 상집합 판 (뺀 상) 은 입력 파일이 정한다.
  - 입력의 `reduction_limit_V` 같은 요약 키는 믿지 않는다 (옛 off-by-one 규칙) — 가장자리는 사다리에서 다시 낸다.
  - 동역학 · 계면 에너지 · 반응 부피 변형 (constrained_esw.py 몫) 을 넣지 않는다 — 0 K 열역학 끝 상태다.
  - n 이 같은 행이 둘이거나 · V 가 n 과 함께 오르거나 (단조 아님) · Li 교환 0 행이 없거나 ·
    숫자가 유한하지 않으면 그리지 않고 멈춘다 (추측해서 메우지 않는다).
"""
import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path

EPS_N = 1e-6


def _products(rxn):
    """반응식 오른쪽 산물 (Li 저장소 항 제외 · 계수는 보기 좋게)."""
    if not isinstance(rxn, str) or "->" not in rxn:
        raise ValueError(f"반응식에 '->' 가 없다: {rxn!r}")
    out = []
    for tok in rxn.split("->", 1)[1].split(" + "):
        tok = tok.strip()
        m = re.match(r"^([0-9.]+)\s+(\S+)$", tok)
        coef, form = (float(m.group(1)), m.group(2)) if m else (1.0, tok)
        if form == "Li":
            continue
        if abs(coef - 1.0) < 1e-9:
            out.append(form)
        elif abs(coef - round(coef)) < 1e-3:
            out.append(f"{int(round(coef))} {form}")
        else:
            out.append(f"{coef:.3g} {form}")
    return " + ".join(out)


def rows_from_result(res):
    """esw 결과 한 조성 → [V, n, 반응식] 행.
    두 꼴을 받는다: `steps` ([V, n, rxn] 목록 · esw_lis4excluded.json 꼴) ·
    `profile` (esw_grand_potential.py 꼴 dict — V_vs_Li · evolution_Li · reaction).
    ⛔ 그 도구의 `reduction_limit_V` 키는 옛 규칙 (HZ-esw-reduction-limit-label) 이라 읽지 않는다 — 사다리만 쓴다."""
    if "steps" in res:
        return res["steps"]
    if "profile" in res:
        out = []
        for d in res["profile"]:
            if not all(k in d for k in ("V_vs_Li", "evolution_Li", "reaction")):
                raise ValueError(f"profile 행에 V_vs_Li · evolution_Li · reaction 이 다 없다 (Li 를 연 결과가 아니다?): {sorted(d)}")
            out.append([d["V_vs_Li"], d["evolution_Li"], d["reaction"]])
        return out
    raise ValueError("결과에 steps 도 profile 도 없다")


def profile(steps):
    """steps → 평탄 구간 목록 (n 오름차순) + 가장자리. 규칙 위반이면 ValueError."""
    if not steps:
        raise ValueError("steps 가 비었다")
    rows = []
    for r in steps:
        if len(r) < 3:
            raise ValueError(f"행 꼴이 [V, n, 반응식] 이 아니다: {r!r}")
        V, n = float(r[0]), float(r[1])
        if not (math.isfinite(V) and math.isfinite(n)):
            raise ValueError(f"유한하지 않은 값: {r!r}")
        rows.append((n, V, r[2]))
    rows.sort(key=lambda t: t[0])
    for a, b in zip(rows, rows[1:]):
        if abs(a[0] - b[0]) < EPS_N:
            raise ValueError(f"n 이 같은 행이 둘이다: {a[0]}")
        if not b[1] < a[1]:
            raise ValueError(f"전위가 Li 흡수와 같이 오른다 (단조 아님): n {a[0]}→{b[0]} · V {a[1]}→{b[1]}")
    zero = [k for k, t in enumerate(rows) if abs(t[0]) < EPS_N]
    if not zero:
        raise ValueError("Li 교환 0 행이 없다 — 환원 가장자리를 정할 수 없다")
    k0 = zero[0]
    segs = []
    for k, (n, V, _r) in enumerate(rows):
        nxt = rows[k + 1] if k + 1 < len(rows) else None
        segs.append({"V": V, "n0": n, "n1": nxt[0] if nxt else None,
                     "end_products": _products(nxt[2]) if nxt else _products(rows[k][2])})
    return {"segments": segs,
            "edge_reduction_V": rows[k0][1],
            "edge_oxidation_V": rows[k0 - 1][1] if k0 > 0 else None,
            "end_state": {"n": rows[-1][0], "V": rows[-1][1], "products": _products(rows[-1][2])}}


def _mt(s):
    """화학식 숫자 → mathtext 아래첨자 (계수 숫자는 그대로)."""
    return re.sub(r"([A-Za-z\)])(\d+(?:\.\d+)?)", r"\1$_{\2}$", s)


def staircase_rows(prof, side):
    keep = [s for s in prof["segments"] if s["n1"] is not None and (side == "both" or s["n0"] >= -EPS_N)]
    pts = []
    for i, s in enumerate(keep):
        pts.append({"Li_uptake_per_fu": s["n0"], "V_vs_Li_V": s["V"], "segment": i + 1,
                    "products_at_segment_end": s["end_products"]})
        pts.append({"Li_uptake_per_fu": s["n1"], "V_vs_Li_V": s["V"], "segment": i + 1,
                    "products_at_segment_end": s["end_products"]})
    end = prof["end_state"]
    pts.append({"Li_uptake_per_fu": end["n"], "V_vs_Li_V": end["V"], "segment": "end",
                "products_at_segment_end": end["products"]})
    return keep, pts


def plot(prof, name, side, out_png, title=None, contact_label="0 V: Li metal contact", group_below=None, group_label=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from tools.figures.house_style import INK, MUT, GAPLINE, apply_axes

    keep, pts = staircase_rows(prof, side)
    end = prof["end_state"]
    edge = prof["edge_reduction_V"]
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    xmax = end["n"]
    ytop = max(2.0, edge + 0.3)
    ax.axhspan(edge, ytop, color="#f3f4f6", zorder=0)
    ax.text(xmax * 0.98, ytop - 0.07, f"no Li uptake above {edge:.2f} V", ha="right", va="top", fontsize=9, color=MUT)
    xs, ys = [], []
    for s in keep:
        xs += [s["n0"], s["n1"]]
        ys += [s["V"], s["V"]]
    xs.append(end["n"]); ys.append(end["V"])
    ax.plot(xs, ys, color=MUT, lw=2.2, zorder=2, solid_joinstyle="miter")
    first = keep[0]
    ax.plot([first["n0"], first["n1"]], [first["V"]] * 2, color=GAPLINE, lw=3.2, zorder=3)
    ax.text((first["n0"] + first["n1"]) / 2, first["V"] + 0.05, f"{first['V']:.2f} V", ha="center", va="bottom",
            fontsize=10.5, fontweight="bold", color=INK)
    lab0 = _mt(f"{name} + {first['n1']:g} Li → {first['end_products']}")
    fits = len(re.sub(r"\$_\{[^}]*\}\$", "x", lab0)) * 0.085 < (first["n1"] - first["n0"]) - 0.2
    ax.text(first["n0"] + 0.12 if fits else first["n1"] + 0.15, first["V"] - 0.06, lab0,
            ha="left", va="top", fontsize=9.5, color=INK)
    rest = keep[1:]
    grouped = [s for s in rest if group_below is not None and s["V"] < group_below]
    rest = [s for s in rest if s not in grouped]
    narrow = [s for s in rest if (s["n1"] - s["n0"]) < 1.0]
    wide = [s for s in rest if (s["n1"] - s["n0"]) >= 1.0]
    if grouped:
        vlo, vhi = min(s["V"] for s in grouped), max(s["V"] for s in grouped)
        bx = xmax + 0.28
        ax.plot([bx, bx + 0.08, bx + 0.08, bx], [vhi, vhi, vlo, vlo], color=MUT, lw=1.0, clip_on=False)
        ax.text(bx + 0.18, (vlo + vhi) / 2 + 0.06, _mt(f"{group_label or 'grouped steps'}\n{vlo:.2f}–{vhi:.2f} V"),
                ha="left", va="center", fontsize=9, color=INK)
    prev = None
    for j, s in enumerate(sorted(narrow, key=lambda q: -q["V"])):
        ly = s["V"] if prev is None else min(s["V"], prev - 0.17)
        prev = ly
        lx = xmax + 0.35
        phase = re.sub(r"^[0-9.]+\s+", "", s["end_products"].split(" + ")[0])
        ax.annotate(_mt(f"{s['V']:.2f} V  → {phase}"), xy=((s["n0"] + s["n1"]) / 2, s["V"]),
                    xytext=(lx, ly), fontsize=9, color=INK, va="center",
                    arrowprops=dict(arrowstyle="-", color="#d1d5db", lw=0.8))
    for s in wide:
        phase = re.sub(r"^[0-9.]+\s+", "", s["end_products"].split(" + ")[0])
        low = s["V"] < 0.3
        ax.text((s["n0"] + s["n1"]) / 2, s["V"] + (0.03 if low else -0.06), _mt(f"{s['V']:.2f} V  → {phase}"), ha="center",
                va="bottom" if low else "top", fontsize=9.5, color=INK)
    ax.plot([end["n"]], [end["V"]], "o", color=INK, ms=5, zorder=4)
    ax.annotate(_mt(f"{contact_label}\n{end['products']}"), xy=(end["n"], end["V"]), xytext=(xmax + (0.55 if grouped else 0.35), 0.06 if grouped else 0.22),
                fontsize=9, color=INK, va="center", arrowprops=dict(arrowstyle="-", color="#d1d5db", lw=0.8))
    ax.set_xlim(min(0.0, xs[0]), xmax * 1.0 + 0.2)
    ax.set_ylim(0, ytop)
    apply_axes(ax, xlabel=_mt(f"Li taken up per {name}"), ylabel="Voltage vs Li/Li$^+$ (V)",
               title=_mt(title or f"{name}: Li uptake vs voltage (grand potential, MP phases, 0 K)"), fontsize=11)
    fig.tight_layout()
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)


def ag2s_grid_from_interface(inter, cathode="Ag", elab="LPSCl"):
    """열린계 계면 결과 → 격자 전압마다 (Ag2S 가 최소 반응 산물에 있나, 끝점인가).
    ⛔ 끝점 (자체 분해) 칸 · Ag2S 가 반응물 쪽에만 있는 칸은 'Ag2S 생성' 으로 세지 않는다."""
    c = inter["results"][cathode]
    rows = []
    for V, rx in c["reactions"].items():
        r = rx.get(elab)
        deg = bool(c["endpoint_degenerate"][V].get(elab))
        rhs = r.split("->", 1)[1] if isinstance(r, str) and "->" in r else ""
        has = (not deg) and bool(re.search(r"(^|\s)Ag2S(\s|$)", rhs.replace("+", " ")))
        e = c["by_voltage"][V].get(elab)
        rows.append({"V": float(V), "ag2s_product": has, "endpoint": deg,
                     "dE_meV_per_atom": None if e is None else round(e * 1000, 1), "reaction": r})
    rows.sort(key=lambda d: d["V"])
    yes = [d["V"] for d in rows if d["ag2s_product"]]
    no_below = [d["V"] for d in rows if not d["ag2s_product"] and (not yes or d["V"] < min(yes))]
    return {"rows": rows, "onset_grid_V": min(yes) if yes else None,
            "last_without_V": max(no_below) if (yes and no_below) else None}


def window_regions(ladders, se, ag2s, ag, inter=None):
    """사다리 셋 (+ 열린계 격자) → 전위 지도 구간. 가장자리는 전부 사다리에서 다시 낸다."""
    pse, p2s, pag = profile(rows_from_result(ladders[se])), profile(rows_from_result(ladders[ag2s])), profile(rows_from_result(ladders[ag]))
    v_red, v_ox = pse["edge_reduction_V"], pse["edge_oxidation_V"]
    v_ag2s, v_agli = p2s["edge_reduction_V"], pag["edge_reduction_V"]
    if v_ox is None:
        raise ValueError("SE 사다리에 산화 가장자리가 없다")
    regs = [
        ("Li6PS5Cl", "reduced by Li (Li2S + LiCl + P, then Li3P)", 0.0, v_red),
        ("Li6PS5Cl", "stable", v_red, v_ox),
        ("Li6PS5Cl", "oxidized", v_ox, None),
        ("Ag2S", "reduced by Li to Li2S + Ag", 0.0, v_ag2s),
        ("Ag2S", "stable", v_ag2s, None),
        ("Ag metal next to Li6PS5Cl", "Li-Ag alloys", 0.0, v_agli),
        ("Ag metal next to Li6PS5Cl", "Ag metal, no reaction", v_agli, v_ag2s),
        ("Ag metal next to Li6PS5Cl", "Ag + Li6PS5Cl -> Ag2S + Li", v_ag2s, None)]
    out = {"regions": [{"species": a, "region": b, "V_low": lo, "V_high": hi} for a, b, lo, hi in regs],
           "V": {"se_reduction": v_red, "se_oxidation": v_ox, "ag2s_reduction": v_ag2s, "ag_lithiation": v_agli}}
    if inter is not None:
        out["grid"] = ag2s_grid_from_interface(inter)
    return out


def plot_window_map(wm, out_png, vmax=2.6, title=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from tools.figures.house_style import INK, MUT, GAPLINE, apply_axes
    rows = ["Li6PS5Cl", "Ag2S", "Ag metal next to Li6PS5Cl"]
    ylab = {"Li6PS5Cl": "Li$_6$PS$_5$Cl", "Ag2S": "Ag$_2$S", "Ag metal next to Li6PS5Cl": "Ag next to\nLi$_6$PS$_5$Cl"}
    accent_regions = {"stable", "Ag + Li6PS5Cl -> Ag2S + Li"}
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    for k, sp in enumerate(rows):
        y = len(rows) - 1 - k
        for r in [r for r in wm["regions"] if r["species"] == sp]:
            lo, hi = r["V_low"], (r["V_high"] if r["V_high"] is not None else vmax)
            acc = (sp != "Li6PS5Cl" and r["region"] in accent_regions)
            light = r["region"] == "stable" or r["region"].startswith("Ag metal, no")
            col = GAPLINE if acc else ("#e5e7eb" if light else "#9ca3af")
            ax.barh(y, hi - lo, left=lo, height=0.56, color=col, alpha=0.85 if acc else 1.0, edgecolor="white", lw=1.2)
            lab = _mt(r["region"].replace("->", "→").replace("Li-Ag", "Li–Ag"))
            if hi - lo > 0.3:
                ax.text((lo + hi) / 2, y, lab, ha="center", va="center", fontsize=7.8, color="white" if (acc or not light) else INK)
        ax.text(-0.05, y, ylab[sp], ha="right", va="center", fontsize=10, color=INK)
    v = wm["V"]
    top = len(rows) - 0.55
    ax.plot([v["ag2s_reduction"]] * 2, [-0.62, top + 0.25], color=GAPLINE, ls="--", lw=1.2, zorder=4)
    ax.text(v["ag2s_reduction"] + 0.03, top + 0.18, f"{v['ag2s_reduction']:.2f} V", ha="left", va="center", fontsize=9.5,
            color=GAPLINE, fontweight="bold")
    ax.plot([0.01, v["ag_lithiation"]], [top + 0.18] * 2, color=MUT, lw=1.6, solid_capstyle="butt")
    ax.text(v["ag_lithiation"] + 0.03, top + 0.18, f"Li / Li–Ag contact (≤ {v['ag_lithiation']:.2f} V)", ha="left",
            va="center", fontsize=8.5, color=MUT)
    g = wm.get("grid")
    if g:
        for d in g["rows"]:
            ax.plot(d["V"], -0.47, "o", ms=5, mfc=INK if d["ag2s_product"] else "white", mec=INK, mew=1.0, zorder=5)
        ax.text(0.01, -0.70, "open-Li grid (filled = Ag₂S among Ag + Li₆PS₅Cl reaction products)", ha="left", va="center",
                fontsize=8, color=MUT)
    ax.set_xlim(0, vmax)
    ax.set_ylim(-0.85, top + 0.35)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    apply_axes(ax, xlabel="Voltage vs Li/Li$^+$ (V)",
               title=_mt(title or "Ag2S is stable next to Li6PS5Cl only above 1.91 V vs Li"), fontsize=11)
    fig.tight_layout()
    Path(out_png).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_window_csv(wm, out_csv):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["species", "region", "V_low_vs_Li_V", "V_high_vs_Li_V"])
        for r in wm["regions"]:
            w.writerow([r["species"], r["region"], r["V_low"], "" if r["V_high"] is None else r["V_high"]])
        g = wm.get("grid")
        if g:
            w.writerow([])
            w.writerow(["open_Li_grid_V", "Ag2S_in_min_reaction_products", "endpoint_self_decomposition", "dE_meV_per_atom", "reaction"])
            for d in g["rows"]:
                w.writerow([d["V"], d["ag2s_product"], d["endpoint"], "" if d["dE_meV_per_atom"] is None else d["dE_meV_per_atom"], d["reaction"]])


def write_csv(pts, out_csv):
    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["Li_uptake_per_fu", "V_vs_Li_V", "segment", "products_at_segment_end"])
        w.writeheader()
        for p in pts:
            w.writerow(p)


COMP1_FIXTURE = [[0.0, 8.0, "Li6PS5Cl + 8 Li -> Li3P + 5 Li2S + LiCl"],
                 [0.87, 6.0, "Li6PS5Cl + 6 Li -> LiP + 5 Li2S + LiCl"],
                 [0.932, 5.429, "Li6PS5Cl + 5.429 Li -> 0.1429 Li3P7 + 5 Li2S + LiCl"],
                 [1.177, 5.143, "Li6PS5Cl + 5.143 Li -> 0.1429 LiP7 + 5 Li2S + LiCl"],
                 [1.242, 5.0, "Li6PS5Cl + 5 Li -> 5 Li2S + LiCl + P"],
                 [1.717, 0.0, "Li6PS5Cl -> Li3PS4 + Li2S + LiCl"],
                 [2.256, -2.0, "Li6PS5Cl -> Li3PS4 + LiCl + S + 2 Li"],
                 [2.385, -5.0, "Li6PS5Cl -> 0.5 P2S7 + LiCl + 1.5 S + 5 Li"],
                 [3.326, -6.0, "Li6PS5Cl -> 0.5 P2S7 + 0.5 S + SCl + 6 Li"]]


AG2S_FIXTURE = [[1.914, 0.0, "Ag2S -> Ag2S"], [0.592, 2.0, "Ag2S + 2 Li -> Li2S + 2 Ag"],
                [0.369, 2.6667, "Ag2S + 2.667 Li -> 0.6667 LiAg3 + Li2S"], [0.14, 4.0, "Ag2S + 4 Li -> 2 LiAg + Li2S"],
                [0.072, 5.2, "Ag2S + 5.2 Li -> 0.4 Li8Ag5 + Li2S"], [0.0, 8.0, "Ag2S + 8 Li -> 2 Li3Ag + Li2S"]]
AG_FIXTURE = [[0.592, 0.0, "Ag -> Ag"], [0.369, 0.3333, "Ag + 0.3333 Li -> 0.3333 LiAg3"], [0.14, 1.0, "Ag + Li -> LiAg"],
              [0.072, 1.6, "Ag + 1.6 Li -> 0.2 Li8Ag5"], [0.0, 3.0, "Ag + 3 Li -> Li3Ag"]]


def _iface_fixture():
    def cell(V, rx, deg, e):
        return V, rx, deg, e
    cells = [cell("1.90", "Li6PS5Cl -> Li2S + Li3PS4 + LiCl", True, 0.0),
             cell("2.00", "0.6667 Ag + 0.3333 Li6PS5Cl -> 0.6667 Li + 0.3333 Li3PS4 + 0.3333 Ag2S + 0.3333 LiCl", False, -0.019),
             cell("1.50", "Li6PS5Cl + 5 Li -> P + 5 Li2S + LiCl", True, -0.155),
             cell("2.10", "0.8333 Ag + 0.1667 Li6PS5Cl -> 0.8333 Li + 0.1667 Ag3PS4 + 0.1667 Ag2S + 0.1667 LiCl", False, -0.055)]
    c = {"reactions": {}, "endpoint_degenerate": {}, "by_voltage": {}}
    for V, rx, deg, e in cells:
        c["reactions"][V] = {"LPSCl": rx}
        c["endpoint_degenerate"][V] = {"LPSCl": deg}
        c["by_voltage"][V] = {"LPSCl": e}
    return {"results": {"Ag": c}}


def selftest():
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok, fail = ok + bool(cond), fail + (not cond)

    def raises(fn):
        try:
            fn()
        except ValueError:
            return True
        return False

    p = profile(COMP1_FIXTURE)
    seg = {round(s["n0"], 3): s for s in p["segments"]}
    chk("[양성] 환원 가장자리 = 1.717 (1.242 아님 · off-by-one 방지)", p["edge_reduction_V"] == 1.717)
    chk("[양성] 산화 가장자리 = 2.256", p["edge_oxidation_V"] == 2.256)
    chk("[양성] 1.717 V 평탄 = 0 → 5 Li · 끝 산물 5 Li2S + LiCl + P",
        seg[0.0]["V"] == 1.717 and seg[0.0]["n1"] == 5.0 and seg[0.0]["end_products"] == "5 Li2S + LiCl + P")
    chk("[양성] 1.242 V 평탄 = 5 → 5.143 (P → LiP7)", seg[5.0]["V"] == 1.242 and seg[5.0]["n1"] == 5.143
        and seg[5.0]["end_products"].startswith("0.143 LiP7"))
    chk("[양성] 0.87 V 평탄 = 6 → 8 · 끝 상태 Li3P + 5 Li2S + LiCl",
        seg[6.0]["V"] == 0.87 and seg[6.0]["n1"] == 8.0 and p["end_state"]["products"] == "Li3P + 5 Li2S + LiCl")
    chk("[양성] 산화 쪽 2.256 V = −2 → 0 · 산물에서 Li 저장소 항을 뺀다",
        seg[-2.0]["V"] == 2.256 and seg[-2.0]["n1"] == 0.0 and seg[-2.0]["end_products"] == "Li3PS4 + Li2S + LiCl")
    chk("[양성] 2.385 V = −5 → −2 · 끝 산물에서 '+ 2 Li' (저장소) 를 뺀다",
        seg[-5.0]["V"] == 2.385 and seg[-5.0]["end_products"] == "Li3PS4 + LiCl + S")
    keep, pts = staircase_rows(p, "reduction")
    chk("[양성] reduction 쪽 계단 = 평탄 5 개 · 점 11 개", len(keep) == 5 and len(pts) == 11)
    bad = [list(r) for r in COMP1_FIXTURE]
    bad[3][0], bad[4][0] = bad[4][0], bad[3][0]
    chk("[음성] 전위가 단조가 아니면 멈춘다", raises(lambda: profile(bad)))
    chk("[음성] Li 교환 0 행이 없으면 멈춘다", raises(lambda: profile([r for r in COMP1_FIXTURE if r[1] != 0.0])))
    chk("[음성] n 이 같은 행이 둘이면 멈춘다", raises(lambda: profile(COMP1_FIXTURE + [[1.5, 5.0, "x -> y"]])))
    chk("[음성] 유한하지 않은 값이면 멈춘다", raises(lambda: profile(COMP1_FIXTURE + [[float("nan"), 9.0, "x -> y"]])))
    chk("[음성] 반응식에 '->' 가 없으면 멈춘다", raises(lambda: _products("Li2S + LiCl")))
    chk("[음성] 빈 steps 는 멈춘다", raises(lambda: profile([])))
    prof_dicts = [{"V_vs_Li": r[0], "evolution_Li": r[1], "reaction": r[2], "mu_Li_eV": -1.9 - r[0]} for r in COMP1_FIXTURE]
    p2 = profile(rows_from_result({"profile": prof_dicts, "reduction_limit_V": 1.242}))
    chk("[양성] profile(dict) 꼴도 같은 가장자리 1.717 — reduction_limit_V 키 (옛 규칙 1.242) 는 안 읽는다",
        p2["edge_reduction_V"] == 1.717)
    chk("[음성] V_vs_Li 없는 profile (Li 를 안 연 결과) 은 멈춘다",
        raises(lambda: rows_from_result({"profile": [{"evolution_Li": 0, "reaction": "a -> b"}]})))
    chk("[음성] steps 도 profile 도 없으면 멈춘다", raises(lambda: rows_from_result({"reduction_limit_V": 1.242})))
    lad = {"comp1": {"steps": COMP1_FIXTURE}, "Ag2S": {"steps": AG2S_FIXTURE}, "Ag": {"steps": AG_FIXTURE}}
    wmap = window_regions(lad, "comp1", "Ag2S", "Ag", _iface_fixture())
    chk("[양성] 전위 지도 가장자리 = SE 1.717 / 2.256 · Ag2S 1.914 · Li–Ag 0.592 (전부 사다리에서)",
        wmap["V"] == {"se_reduction": 1.717, "se_oxidation": 2.256, "ag2s_reduction": 1.914, "ag_lithiation": 0.592})
    chk("[양성] 열린계 격자: Ag2S 첫 등장 2.0 V · 그 아래 마지막 '없음' 1.9 V", wmap["grid"]["onset_grid_V"] == 2.0
        and wmap["grid"]["last_without_V"] == 1.9)
    fx2 = _iface_fixture()
    fx2["results"]["Ag"]["reactions"]["1.80"] = {"LPSCl": "Ag2S + 2 Li -> Li2S + 2 Ag"}
    fx2["results"]["Ag"]["endpoint_degenerate"]["1.80"] = {"LPSCl": False}
    fx2["results"]["Ag"]["by_voltage"]["1.80"] = {"LPSCl": -0.076}
    chk("[음성] Ag2S 가 반응물 쪽에만 있으면 '생성' 으로 세지 않는다", ag2s_grid_from_interface(fx2)["onset_grid_V"] == 2.0)
    fx3 = _iface_fixture()
    fx3["results"]["Ag"]["endpoint_degenerate"]["2.00"] = {"LPSCl": True}
    chk("[음성] 끝점 (자체 분해) 칸은 Ag2S 가 있어도 세지 않는다", ag2s_grid_from_interface(fx3)["onset_grid_V"] == 2.1)
    fx4 = _iface_fixture()
    for V in ("2.00", "2.10"):
        fx4["results"]["Ag"]["endpoint_degenerate"][V] = {"LPSCl": True}
    g4 = ag2s_grid_from_interface(fx4)
    chk("[음성] Ag2S 칸이 하나도 없으면 첫 등장은 None (0 으로 두지 않는다)", g4["onset_grid_V"] is None and g4["last_without_V"] is None)
    print(f"\nselftest: {ok} passed, {fail} failed")
    return 0 if fail == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--esw", help="esw_grand_potential.py 꼴 JSON (results.<label>.steps)")
    ap.add_argument("--label", help="results 안의 조성 라벨 (예: comp1)")
    ap.add_argument("--name", help="그림에 쓸 조성 이름 (예: Li6PS5Cl)")
    ap.add_argument("--side", choices=["reduction", "both"], default="reduction")
    ap.add_argument("--title")
    ap.add_argument("--out_png")
    ap.add_argument("--out_csv")
    ap.add_argument("--selftest", action="store_true", help="자체 점검 (음성 경로 포함)")
    ap.add_argument("--window_map", nargs=3, metavar=("SE", "AG2S", "AG"),
                    help="전위 지도 모드 — --esw 안의 세 라벨 (예: comp1 Ag2S Ag) · --interface 를 주면 열린계 격자 점을 얹는다")
    ap.add_argument("--interface", help="interface_reactivity_v2.py 열린계 결과 JSON (cathodes 에 Ag · 전해질 라벨 LPSCl)")
    ap.add_argument("--group_below", type=float, help="이 전위 아래 계단 (첫 계단 제외) 은 그림에서 묶음 하나로 표시 (CSV 에는 다 남는다)")
    ap.add_argument("--group_label", help="--group_below 묶음 이름 (예: 'Li–Ag alloying')")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.window_map:
        if not (a.esw and (a.out_png or a.out_csv)):
            ap.error("--window_map 은 --esw 와 --out_png 또는 --out_csv 가 필요하다")
        lad = json.loads(Path(a.esw).read_text(encoding="utf-8"))["results"]
        inter = json.loads(Path(a.interface).read_text(encoding="utf-8")) if a.interface else None
        se, s2, ag = a.window_map
        wmap = window_regions(lad, se, s2, ag, inter)
        print("전위 지도:", {k: round(v, 3) for k, v in wmap["V"].items()})
        if wmap.get("grid"):
            g = wmap["grid"]
            print(f"  열린계 격자: Ag2S 첫 등장 {g['onset_grid_V']} V · 그 아래 마지막 '없음' {g['last_without_V']} V")
        if a.out_csv:
            write_window_csv(wmap, a.out_csv); print(f"→ {a.out_csv}")
        if a.out_png:
            plot_window_map(wmap, a.out_png, title=a.title); print(f"→ {a.out_png}")
        return 0
    if not (a.esw and a.label and a.name and (a.out_png or a.out_csv)):
        ap.error("--esw --label --name 과 --out_png 또는 --out_csv 가 필요하다 (또는 --selftest)")
    d = json.loads(Path(a.esw).read_text(encoding="utf-8"))
    res = d.get("results", {})
    if a.label not in res:
        sys.exit(f"⛔ {a.esw} 에 results.{a.label} 이 없다 (있는 라벨: {', '.join(res) or '없음'})")
    prof = profile(rows_from_result(res[a.label]))
    keep, pts = staircase_rows(prof, a.side)
    print(f"{a.name}: 환원 가장자리 {prof['edge_reduction_V']:.3f} V · 산화 가장자리 "
          f"{prof['edge_oxidation_V'] if prof['edge_oxidation_V'] is not None else '—'} V · 끝 상태 "
          f"Li {prof['end_state']['n']:g} → {prof['end_state']['products']}")
    for s in keep:
        print(f"  {s['V']:.3f} V : Li {s['n0']:g} → {s['n1']:g}  ({s['end_products']})")
    if a.out_csv:
        write_csv(pts, a.out_csv)
        print(f"→ {a.out_csv}")
    if a.out_png:
        plot(prof, a.name, a.side, a.out_png, title=a.title, group_below=a.group_below, group_label=a.group_label)
        print(f"→ {a.out_png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
