#!/usr/bin/env python3
"""plot_mixing_curves.py — 닫힌계 pseudo-binary 혼합 곡선 (kink 전부) 그림 + Origin CSV.

입력은 `interface_reactivity_v2.py --closed --record_kinks` 의 JSONL 이다 (행 = 한 쌍).
kink 의 `x` 는 pymatgen 혼합비 그대로 = **첫 반응물 (species) 의 원자 분율**이다
(x = 0 은 상대 (cathode) 혼자 · x = 1 은 species 혼자). 그림의 가로축은 문헌 꼴
(Banerjee 2019 Fig. 4a: *x in (1−x) A + x B*) 에 맞춰 **상대 쪽 분율 = 1 − x** 로 옮긴다.

  python3 tools/figures/plot_mixing_curves.py \
     --jsonl db/properties/hyeokju_lzo_s1_closed_2026_11_16.jsonl \
     --curves "LPSCl:NCA721_y" "LZO:NCA721_y" --ys 1.0 0.5 0.2 --extra "LPSCl:LZO" \
     --out_png docs/figures/hyeokju_lzo/fig_s1_mixing_curves.png \
     --out_csv db/properties/hyeokju_lzo_s1_mixing_curves_2026_11_16.csv
  python3 tools/figures/plot_mixing_curves.py --jsonl … --min_vs_y "LPSCl:NCA721_y" "LZO:NCA721_y" … \
     --hline "LPSCl:LZO" --out_png … --out_csv …
  python3 tools/figures/plot_mixing_curves.py --selftest

⛔ 이 도구가 못 하는 것
  · 열린계 (grand potential) 행을 그리지 않는다 — 정규화 (Li 뺀 원자당) 가 달라 같은 축에 못 놓는다. 열린계 행이 오면 거부한다.
  · 'error' · 'skipped' 행 · kink 없는 행 · 끝점 (x = 0 과 x = 1) 이 없는 행은 그리지 않고 **멈춘다** (조용히 빼지 않는다).
  · 전압 라벨을 붙이지 않는다 — y (양극 Li 함량) 만 쓴다. y → 전압 환산은 카드 G5 의 일이다.
  · 반응 속도 · 생성량은 아무것도 말하지 않는다 (0 K 열역학 끝 상태).
  · 상대 끝점 반응식에 O₂ 가 있으면 깃발만 단다 (판단은 카드 §3).
"""
import argparse
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def products(rxn):
    """반응식 오른쪽의 생성물 화학식 목록 (계수 뺌). 'LiNiO2' 를 'O2' 로 읽지 않는다 — 항 단위로 자른다."""
    if "->" not in rxn:
        raise ValueError(f"반응식이 아니다: {rxn!r}")
    out = []
    for t in rxn.split("->", 1)[1].split(" + "):
        t = t.strip()
        m = re.match(r"^([0-9.eE+-]+)\s+(\S+)$", t)
        out.append(m.group(2) if m else t)
    return out


def check_row(r):
    """그릴 수 있는 닫힌계 행인가. 못 그리면 이유를 낸다 (None 이면 통과)."""
    if "error" in r or "skipped" in r:
        return f"{r.get('species')} × {r.get('cathode')}: 오류 · 건너뜀 행 — 그리지 않는다"
    if r.get("mode") != "closed_0V":
        return f"{r.get('species')} × {r.get('cathode')}: 닫힌계 행이 아니다 (mode={r.get('mode')}) — 정규화가 달라 거부"
    ks = r.get("kinks") or []
    if not ks:
        return f"{r.get('species')} × {r.get('cathode')}: kink 가 없다 (--record_kinks 없이 돈 행)"
    xs = [float(k["x"]) for k in ks]
    if min(xs) != 0.0 or max(xs) != 1.0:
        return f"{r.get('species')} × {r.get('cathode')}: 끝점 (x=0 · x=1) 이 없다 — 곡선이 정의되지 않는다"
    return None


def curve(r):
    """(상대 분율, meV/atom, 반응식) 목록 — 상대 분율 오름차순."""
    pts = [(round(1.0 - float(k["x"]), 6), 1000.0 * float(k["dE_eV_per_atom"]), k["reaction"]) for k in r["kinks"]]
    return sorted(pts, key=lambda p: p[0])


def cathode_o2(r):
    """상대 끝점 (x = 0) 의 자기 hull 분해에 O2 가 있는가."""
    k0 = [k for k in r["kinks"] if float(k["x"]) == 0.0]
    return bool(k0) and "O2" in products(k0[0]["reaction"])


def summary_row(r):
    xs = r.get("mixing_x")
    return {"species": r["species"], "cathode": r["cathode"],
            "dE_min_meV_per_atom": round(1000.0 * r["dE_eV_per_atom"], 2),
            "cathode_frac_at_min": None if xs is None else round(1.0 - float(xs), 6),
            "min_at_endpoint_no_reaction": bool(r.get("min_kink_at_endpoint")),
            "cathode_endpoint_has_O2": cathode_o2(r),
            "products": " + ".join(products(r["reaction"])), "reaction": r["reaction"]}


def load(path):
    return [json.loads(ln) for ln in open(path, encoding="utf-8") if ln.strip()]


def pick(rows, spec, y=None):
    """'SPECIES:CATHODE_PREFIX' (+ y) → 행 하나. 없거나 둘 이상이면 멈춘다."""
    sp, _, cat = spec.partition(":")
    want = cat + (y if y is not None else "")
    hit = [r for r in rows if r.get("species") == sp and r.get("cathode") == want]
    if len(hit) != 1:
        raise SystemExit(f"⛔ {sp} × {want}: 행 {len(hit)} 개 (하나여야 한다)")
    why = check_row(hit[0])
    if why:
        raise SystemExit("⛔ " + why)
    return hit[0]


def label_of(spec, y=None):
    sp, _, cat = spec.partition(":")
    cat = cat.rstrip("_y").replace("_", " ")
    return f"{sp}–{cat}" + (f" (y = {y})" if y is not None else "")


def plot_curves(rows, specs, ys, extra, out_png, out_csv, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from house_style import INK, MUT, apply_axes
    cols = ["#c05621", "#0284c7", "#7c3aed", "#65a30d"]
    sty = {ys[0]: "-", **({ys[1]: "--"} if len(ys) > 1 else {}), **({ys[2]: ":"} if len(ys) > 2 else {})}
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    out = []
    for i, spec in enumerate(specs):
        for y in ys:
            r = pick(rows, spec, y)
            c = curve(r)
            ax.plot([p[0] for p in c], [p[1] for p in c], sty.get(y, "-"), color=cols[i % len(cols)], lw=1.8,
                    marker="o", ms=3.2, label=label_of(spec, y))
            out += [{"pair": label_of(spec), "y": y, "cathode_frac": p[0], "E_rxn_meV_per_atom": round(p[1], 2),
                     "reaction": p[2]} for p in c]
    for j, spec in enumerate(extra or []):
        r = pick(rows, spec)
        c = curve(r)
        ax.plot([p[0] for p in c], [p[1] for p in c], "-", color=cols[(len(specs) + j) % len(cols)], lw=1.8,
                marker="s", ms=3.2, label=label_of(spec))
        out += [{"pair": label_of(spec), "y": "", "cathode_frac": p[0], "E_rxn_meV_per_atom": round(p[1], 2),
                 "reaction": p[2]} for p in c]
    ax.axhline(0, color=MUT, lw=0.8)
    apply_axes(ax, xlabel="x in (1−x) A + x B   (B = second phase)", ylabel="Reaction energy (meV/atom)", title=title)
    ax.set_xlim(0, 1)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.text(0.99, 0.01, "Materials Project (GGA/GGA+U) · pymatgen · closed system · 0 K", ha="right", va="bottom",
             fontsize=7, color=MUT)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    write_csv(out_csv, out, ["pair", "y", "cathode_frac", "E_rxn_meV_per_atom", "reaction"])
    return out


def plot_min_vs_y(rows, specs, ys, hline, out_png, out_csv, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from house_style import MUT, apply_axes
    cols = ["#c05621", "#0284c7", "#7c3aed", "#65a30d"]
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    out = []
    fams = {}
    for spec in specs:
        sp, _, cat = spec.partition(":")
        fams.setdefault(sp, []).append(spec)
    for i, (sp, group) in enumerate(fams.items()):
        for j, spec in enumerate(group):
            pts = []
            for y in ys:
                s = summary_row(pick(rows, spec, y))
                s["y"] = float(y)
                pts.append(s)
                out.append(s)
            ls = "-" if j == 0 else "--"
            ax.plot([p["y"] for p in pts], [p["dE_min_meV_per_atom"] for p in pts], ls, color=cols[i % len(cols)],
                    lw=1.8, label=label_of(spec).replace(" y", ""))
            for p in pts:
                ax.plot(p["y"], p["dE_min_meV_per_atom"], "o", ms=4.5, color=cols[i % len(cols)],
                        mfc="white" if p["cathode_endpoint_has_O2"] else cols[i % len(cols)])
    for k, spec in enumerate(hline or []):
        s = summary_row(pick(rows, spec))
        s["y"] = ""
        out.append(s)
        ax.axhline(s["dE_min_meV_per_atom"], color=cols[(len(fams) + k) % len(cols)], lw=1.4, ls="-.",
                   label=label_of(spec) + " (no y)")
    ax.axhline(0, color=MUT, lw=0.8)
    apply_axes(ax, xlabel="Li content y in the cathode (1.0 = pristine; charging →)",
               ylabel="Most negative reaction energy (meV/atom)", title=title)
    ax.set_xlim(max(float(v) for v in ys) + 0.03, min(float(v) for v in ys) - 0.03)
    ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.text(0.99, 0.01, "open marker: O2 in the cathode's own hull decomposition · MP (GGA/GGA+U) · closed · 0 K",
             ha="right", va="bottom", fontsize=7, color=MUT)
    fig.tight_layout()
    os.makedirs(os.path.dirname(out_png) or ".", exist_ok=True)
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    write_csv(out_csv, out, ["species", "cathode", "y", "dE_min_meV_per_atom", "cathode_frac_at_min",
                             "min_at_endpoint_no_reaction", "cathode_endpoint_has_O2", "products", "reaction"])
    return out


def write_csv(path, rows, cols):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def selftest():
    import tempfile
    n = {"ok": 0, "bad": 0}

    def chk(c, msg):
        n["ok" if c else "bad"] += 1
        print(("  ✓ " if c else "  ✗ ") + msg)

    def row(sp, cat, kinks, mode="closed_0V", **kw):
        r = {"species": sp, "cathode": cat, "mode": mode, "kinks": kinks,
             "dE_eV_per_atom": min(k["dE_eV_per_atom"] for k in kinks) if kinks else 0.0,
             "mixing_x": None, "min_kink_at_endpoint": False, "reaction": "A -> B"}
        r.update(kw)
        return r
    K = [{"x": 0.0, "dE_eV_per_atom": 0.0, "reaction": "Li1Ni1O2 -> LiNiO2"},
         {"x": 0.25, "dE_eV_per_atom": -0.2, "reaction": "0.5 A + 0.5 B -> Li3PO4 + LiCl"},
         {"x": 1.0, "dE_eV_per_atom": 0.0, "reaction": "Li6PS5Cl -> Li6PS5Cl"}]
    KO2 = [dict(K[0], reaction="Li0.1Ni1O2 -> 0.45 NiO + 0.1 LiNiO2 + 0.3 O2")] + K[1:]
    chk(products("0.3 LiNiO2 + 0.2 Li2CoO3 -> 0.5 LiNiO2 + 0.25 O2") == ["LiNiO2", "O2"], "[양성] 생성물 항 단위 (계수 뺌)")
    chk("O2" not in products("Li1Ni1O2 -> LiNiO2 + Li2CoO3"), "[⛔음성] 'LiNiO2' · 'Li2CoO3' 를 O2 로 읽지 않는다")
    r = row("LPSCl", "NCA_y1.0", K)
    c = curve(r)
    chk([p[0] for p in c] == [0.0, 0.75, 1.0] and c[1][1] == -200.0, "[양성] 가로축 = 상대 분율 1 − x · meV/atom · 오름차순")
    chk(cathode_o2(row("LPSCl", "NCA_y0.1", KO2)) and not cathode_o2(r), "[양성] 상대 끝점 O2 깃발 (x = 0 반응식만)")
    chk(check_row(r) is None, "[양성] 정상 닫힌계 행은 통과")
    chk("열린계" not in (check_row(row("LPSCl", "N", K, mode="grand_potential")) or "") and
        "닫힌계 행이 아니다" in (check_row(row("LPSCl", "N", K, mode="grand_potential")) or ""),
        "[⛔음성] 열린계 행은 거부 (정규화가 다르다)")
    chk("오류" in (check_row(dict(r, error="X")) or ""), "[⛔음성] error 행은 거부 (조용히 빼지 않는다)")
    chk("kink" in (check_row(row("LPSCl", "N", [])) or ""), "[⛔음성] kink 없는 행은 거부")
    chk("끝점" in (check_row(row("LPSCl", "N", K[:2])) or ""), "[⛔음성] x = 1 끝점이 없으면 거부")
    try:
        pick([r, dict(r)], "LPSCl:NCA_y", "1.0")
        chk(False, "[⛔음성] 같은 쌍이 둘이면 멈춘다")
    except SystemExit:
        chk(True, "[⛔음성] 같은 쌍이 둘이면 멈춘다")
    s = summary_row(dict(r, mixing_x=0.25, reaction=K[1]["reaction"]))
    chk(s["cathode_frac_at_min"] == 0.75 and s["products"] == "Li3PO4 + LiCl", "[양성] 요약 행: 최소점 상대 분율 · 생성물")
    try:
        import matplotlib  # noqa: F401
        with tempfile.TemporaryDirectory() as td:
            rows = [row("LPSCl", f"NCA_y{y}", K) for y in ("1.0", "0.5")] + [row("LPSCl", "LZO", K)]
            o = plot_curves(rows, ["LPSCl:NCA_y"], ["1.0", "0.5"], ["LPSCl:LZO"], os.path.join(td, "a.png"),
                            os.path.join(td, "a.csv"), "t")
            chk(os.path.getsize(os.path.join(td, "a.png")) > 1000 and len(o) == 9, "[양성] 곡선 그림 · CSV (행 9)")
            o2 = plot_min_vs_y(rows, ["LPSCl:NCA_y"], ["1.0", "0.5"], ["LPSCl:LZO"], os.path.join(td, "b.png"),
                               os.path.join(td, "b.csv"), "t")
            chk(len(o2) == 3 and o2[-1]["y"] == "", "[양성] 최소값 대 y 그림 · CSV (가로선 행은 y 빈칸)")
    except ImportError:
        chk(False, "[전제] matplotlib 이 있어야 그림 시험이 돈다")
    print(f"selftest {'PASS' if n['bad'] == 0 else 'FAIL'} ({n['ok']} ok · {n['bad']} bad)")
    return 0 if n["bad"] == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--jsonl")
    ap.add_argument("--curves", nargs="*", default=[], metavar="SPECIES:CATHODE_PREFIX")
    ap.add_argument("--ys", nargs="*", default=[])
    ap.add_argument("--extra", nargs="*", default=[], metavar="SPECIES:CATHODE")
    ap.add_argument("--min_vs_y", nargs="*", default=[], metavar="SPECIES:CATHODE_PREFIX")
    ap.add_argument("--hline", nargs="*", default=[], metavar="SPECIES:CATHODE")
    ap.add_argument("--title", default="")
    ap.add_argument("--out_png")
    ap.add_argument("--out_csv")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.jsonl and a.out_png and a.out_csv and a.ys and (a.curves or a.min_vs_y)):
        ap.error("--jsonl · --ys · --out_png · --out_csv 와 --curves 또는 --min_vs_y 가 필요하다")
    rows = load(a.jsonl)
    if a.curves:
        out = plot_curves(rows, a.curves, a.ys, a.extra, a.out_png, a.out_csv, a.title)
    else:
        out = plot_min_vs_y(rows, a.min_vs_y, a.ys, a.hline, a.out_png, a.out_csv, a.title)
    print(f"→ {a.out_png} · {a.out_csv} ({len(out)} 행)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
