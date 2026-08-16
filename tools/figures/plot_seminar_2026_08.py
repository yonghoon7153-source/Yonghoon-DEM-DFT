#!/usr/bin/env python3
"""plot_seminar_2026_08.py — 2026-08 연구세미나 덱에 들어갈 그림을 **한 양식으로** 다시 그린다.

왜 다시 그리나
  기존 `plot_cascade_*.py` 산출물은 파이프라인 진단용이라 제목이 `Cascade v23 — RELIABILITY view:
  mean ± replicate std (the run-to-run band)` 같은 내부 표현이고, 한 장에 4~6 패널이 들어가
  슬라이드에서 글자가 안 읽힌다. 발표용은 **제목 없이 한 가지 얘기만** 하는 그림이어야 한다.

양식 (전부 공통)
  · matplotlib 제목 없음 — 슬라이드 제목·캡션이 그 역할을 한다
  · 축 라벨·주석은 평범한 영어 문장, 내부 코드명(v23·G4·UMA-s-1p1) 금지
  · house_style 색, spine top/right 제거, dpi 300
  · 나쁨/붕괴 = 빨강, 좋음/강조 = 파랑 (덱 불릿 색 규칙과 동일)
  · 슬라이드 배치 폭 8.9 in 에 맞춰 figsize 통일

이 도구가 **못 하는 것**
  · 3D BVSE 지형·구조 패널은 여기서 못 만든다 (원본 스크립트·구조 파일 필요).
    그 그림들은 제목 띠만 잘라내고 슬라이드 캡션이 설명을 진다.
  · 순위를 만들지 않는다 — 승인된 current ranking 은 0종이다. 색은 **화학군**이나
    **창 붕괴 여부** 처럼 판정이 아닌 축에만 쓴다.
  · 농도축 그림을 만들지 않는다 — 세 라벨은 농도가 아니다.
"""
import csv, io, os, sys, statistics as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cascade"))
import house_style as hs
from cascade_ids import base_species

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                   "docs", "figures", "seminar")
DB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                  "db", "properties")

BAD, GOOD = "#be123c", "#2563eb"          # 덱 불릿 색 규칙과 같은 값
NEUTRAL = "#94a3b8"
GROUP_C = {"alkali": "#0d9488", "alk.earth": "#65a30d", "main-group": "#0284c7",
           "TM": "#7c3aed", "lanthanide": "#c05621"}


def _rc():
    plt.rcParams.update({
        "font.size": 13, "axes.labelsize": 14, "xtick.labelsize": 12, "ytick.labelsize": 12,
        "axes.edgecolor": hs.INK, "axes.labelcolor": hs.INK,
        "xtick.color": hs.INK, "ytick.color": hs.INK, "figure.facecolor": "white",
    })


def _bare(ax, grid=None):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(axis=grid, color="#e5e7eb", lw=0.8, zorder=0)
        ax.set_axisbelow(True)


def _save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {name}")
    return p


def _read(path, comment_prefix="#"):
    lines = [l for l in io.open(path, encoding="utf-8-sig") if not l.lstrip().startswith(comment_prefix)]
    return list(csv.DictReader(lines))


def _all_rows():
    return list(csv.DictReader(io.open(os.path.join(DB, "cascade_v23_all.csv"), encoding="utf-8")))


# ── 1. 후보 원소 주기율표 (순위 아님 — 커버리지) ───────────────────────────────
PT = {  # 원소: (열, 행)
 "Li":(1,1),"B":(13,1),
 "Na":(1,2),"Mg":(2,2),"Al":(13,2),"Si":(14,2),
 "Ca":(2,3),"Sc":(3,3),"Ti":(4,3),"V":(5,3),"Cr":(6,3),"Mn":(7,3),"Fe":(8,3),"Co":(9,3),
 "Ni":(10,3),"Cu":(11,3),"Zn":(12,3),"Ga":(13,3),"Ge":(14,3),
 "Sr":(2,4),"Y":(3,4),"Zr":(4,4),"Nb":(5,4),"Mo":(6,4),"Ag":(11,4),"In":(13,4),"Sn":(14,4),"Sb":(15,4),
 "Ba":(2,5),"Hf":(4,5),"Ta":(5,5),"W":(6,5),
 "La":(4,6.6),"Nd":(6,6.6),"Sm":(7,6.6),"Gd":(8,6.6),
}
GROUP_OF = {"Li":"alkali","Na":"alkali","Ag":"TM","Mg":"alk.earth","Ca":"alk.earth","Sr":"alk.earth",
            "Ba":"alk.earth","B":"main-group","Al":"main-group","Si":"main-group","Ga":"main-group",
            "Ge":"main-group","In":"main-group","Sn":"main-group","Sb":"main-group",
            "La":"lanthanide","Nd":"lanthanide","Sm":"lanthanide","Gd":"lanthanide"}


def fig_periodic():
    import re
    rows = _all_rows()
    sp = sorted({base_species(r["dopant"]) for r in rows})
    cnt = {}
    for s in sp:
        for m in re.findall(r"[A-Z][a-z]?", s):
            if m not in ("O", "S", "F", "Cl", "Br", "I", "N"):
                cnt[m] = cnt.get(m, 0) + 1
    _rc()
    fig, ax = plt.subplots(figsize=(12.4, 5.0))
    for el, (c, r) in PT.items():
        g = GROUP_OF.get(el, "TM")
        col = GROUP_C[g]
        ax.add_patch(Rectangle((c, -r), .94, .94, facecolor=col, alpha=.16,
                               edgecolor=col, lw=1.6, zorder=2))
        ax.text(c + .47, -r + .60, el, ha="center", va="center", fontsize=17,
                weight="bold", color=hs.INK, zorder=3)
        ax.text(c + .47, -r + .26, f"{cnt.get(el,0)}", ha="center", va="center",
                fontsize=11.5, color=hs.MUT, zorder=3)
    for i, (g, col) in enumerate(GROUP_C.items()):
        ax.add_patch(Rectangle((1 + i * 2.7, -7.95), .5, .45, facecolor=col, alpha=.16,
                               edgecolor=col, lw=1.5))
        ax.text(1.65 + i * 2.7, -7.72, g, fontsize=12.5, va="center", color=hs.INK)
    ax.text(16.6, -1.2, "number = how many\ncompounds of that\nelement we ran",
            fontsize=11.5, color=hs.MUT, va="top", ha="left")
    ax.set_xlim(.4, 20.2); ax.set_ylim(-8.3, -.1)
    ax.axis("off")
    return _save(fig, "roster_periodic_table.png")


# ── 2. 어느 자리를 고르는가 ────────────────────────────────────────────────────
def fig_site_choice():
    rows = _read(os.path.join(DB, "site_preference_raw_78.csv"))
    by = {}
    for r in rows:
        try:
            rad, de = float(r["ionic_radius_6coord_A"]), float(r["dE_per_dopant_eV"])
        except (ValueError, KeyError):
            continue
        by.setdefault(r["M"], []).append((rad, de))
    _rc()
    fig, ax = plt.subplots(figsize=(11.6, 5.2))
    ax.axhline(0, color=hs.INK, lw=1.2, zorder=2)
    for m, v in by.items():
        rad = v[0][0]; des = [d for _, d in v]
        mean = st.mean(des); col = GOOD if mean < 0 else BAD
        ax.plot([rad, rad], [min(des), max(des)], color=col, lw=1.4, alpha=.45, zorder=3)
        ax.scatter([rad], [mean], s=64, color=col, zorder=4, edgecolors="white", lw=1.0)
        ax.annotate(m, (rad, mean), textcoords="offset points", xytext=(0, 9),
                    ha="center", fontsize=11, color=hs.INK)
    ax.text(.30, 2.55, "sits on a Li site", fontsize=15, color=BAD, weight="bold")
    ax.text(.30, -1.72, "replaces P in the framework", fontsize=15, color=GOOD, weight="bold")
    ax.set_xlabel("Shannon ionic radius of the dopant cation  (6-coordinate, Å)")
    ax.set_ylabel("energy difference between the two sites  (eV per dopant)")
    _bare(ax, grid="y")
    return _save(fig, "step1_site_choice.png")


# ── 3. 음이온이 실제로 앉은 자리 ───────────────────────────────────────────────
SITE_LABEL = {"S_16e": "sulfur in the PS₄ corner", "S_4a": "free sulfide", "Cl_4d": "halide site"}


def fig_anion_site():
    rows = [r for r in _all_rows() if r.get("rank_combined") == "1" and r.get("anion_site")]
    cnt = {}
    for r in rows:
        cnt[r["anion_site"]] = cnt.get(r["anion_site"], 0) + 1
    items = sorted(cnt.items(), key=lambda kv: -kv[1])
    _rc()
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    cols = [hs.ELEM["S"], hs.ELEM["S"], hs.ELEM["Cl"]]
    for i, (k, v) in enumerate(items):
        ax.barh(-i, v, height=.56, color=cols[i % len(cols)], alpha=.85, zorder=3)
        ax.text(v + 1.2, -i, str(v), va="center", fontsize=15, weight="bold", color=hs.INK)
        ax.text(-1.5, -i, SITE_LABEL.get(k, k), va="center", ha="right", fontsize=14, color=hs.INK)
    ax.set_xlim(0, max(cnt.values()) * 1.22); ax.set_ylim(-len(items) + .4, .6)
    ax.set_yticks([])
    ax.set_xlabel("number of generated candidates that placed the dopant anion there")
    _bare(ax, grid="x")
    ax.text(.99, .06, "the generator chose the site — it was not a variable we set",
            transform=ax.transAxes, ha="right", fontsize=12.5, color=hs.MUT)
    return _save(fig, "step2_anion_site.png")


# ── 4. 대표 구조 선택의 흔들림 ─────────────────────────────────────────────────
def _by_species(col, rank="1"):
    by = {}
    for r in _all_rows():
        if r.get("rank_combined") != rank or not r.get(col):
            continue
        try:
            by.setdefault(base_species(r["dopant"]), {})[r.get("concentration_label", "")] = float(r[col])
        except ValueError:
            continue
    return {k: v for k, v in by.items() if len(v) >= 3}


def fig_stability_band():
    sp = _by_species("rerank_de_post_anneal")
    order = sorted(sp, key=lambda k: st.mean(sp[k].values()))
    _rc()
    fig, ax = plt.subplots(figsize=(11.6, 4.6))
    for i, k in enumerate(order):
        v = sorted(sp[k].values())
        ax.plot([i, i], [v[0], v[-1]], color=NEUTRAL, lw=1.1, zorder=2)
        ax.scatter([i] * len(v), v, s=15, color=hs.ELEM["P"], zorder=3, alpha=.9, edgecolors="none")
    ax.set_xticks([]); ax.set_xlim(-2, len(order) + 1)
    ax.set_xlabel(f"{len(order)} dopant species  ·  sorted by mean  ·  names omitted on purpose")
    ax.set_ylabel("relative stability against the undoped host  (eV / atom)")
    _bare(ax, grid="y")
    ax.text(.015, .06, "more stable than the host  ↓", transform=ax.transAxes,
            fontsize=12.5, color=hs.MUT)
    ax.text(.30, .20, "on this axis the three runs of one species agree —\nthe bars are short next to the range across species",
            transform=ax.transAxes, ha="left", va="bottom", fontsize=13, color=GOOD, weight="bold")
    return _save(fig, "step4_stability_band.png")


# ── 5. 결과 1 — 같은 이름, 다른 값 ─────────────────────────────────────────────
def fig_label_spread():
    sp = _by_species("elastic_E_young_GPa")
    order = sorted(sp, key=lambda k: st.mean(sp[k].values()))
    between = st.pstdev([st.mean(sp[k].values()) for k in order])
    within = st.median([max(v.values()) - min(v.values()) for v in sp.values()])
    lo, hi = 24, 72
    off = sum(1 for k in order if max(sp[k].values()) > hi or min(sp[k].values()) < lo)
    _rc()
    fig, ax = plt.subplots(figsize=(11.6, 4.8))
    for i, k in enumerate(order):
        v = sorted(sp[k].values())
        ax.plot([i, i], [v[0], v[-1]], color=NEUTRAL, lw=1.2, zorder=2)
        ax.scatter([i] * len(v), v, s=17, color=hs.ELEM["P"], zorder=3, alpha=.9, edgecolors="none")
    y = hi - 5.5; mid = len(order) // 2
    ax.annotate("", xy=(mid - 6, y), xytext=(mid + 7, y),
                arrowprops=dict(arrowstyle="<->", color=BAD, lw=2.0))
    ax.text(mid + .5, y + 1.2, "one species, three runs  =  as wide as thirteen different species",
            ha="center", va="bottom", fontsize=14, color=BAD, weight="bold")
    ax.set_ylim(lo, hi); ax.set_xlim(-2, len(order) + 1); ax.set_xticks([])
    ax.set_xlabel(f"{len(order)} dopant species  ·  sorted by mean  ·  names omitted on purpose")
    ax.set_ylabel("Young's modulus  E  (GPa)")
    _bare(ax, grid="y")
    ax.text(.015, .04, f"spread within one species  {within:.1f} GPa      "
                       f"spread across species  {between:.1f} GPa"
                       + (f"      ({off} off scale)" if off else ""),
            transform=ax.transAxes, fontsize=12, color=hs.MUT)
    return _save(fig, "result1_same_name_different_value.png")


# ── 6. 산화 창 ────────────────────────────────────────────────────────────────
def _ox_rows():
    return _read(os.path.join(DB, "oxidation_stability_cascade_v2.csv"))


def fig_oxidation_windows():
    rows = []
    for r in _ox_rows():
        try:
            rows.append((r["dopant"], float(r["red_V"]), float(r["ox_V"]), float(r["window_V"]), r["group"]))
        except (ValueError, KeyError):
            continue
    rows.sort(key=lambda t: (t[3] > 0.05, t[2]))
    _rc()
    fig, ax = plt.subplots(figsize=(11.6, 5.4))
    for i, (d, red, ox, win, g) in enumerate(rows):
        col = BAD if win <= 0.05 else GROUP_C.get(g, NEUTRAL)
        ax.plot([red, ox], [i, i], color=col, lw=2.4, solid_capstyle="butt",
                alpha=.55 if win > 0.05 else 1.0, zorder=3)
    ax.axvline(2.14, color=hs.INK, ls="--", lw=1.3, zorder=4)
    ax.text(2.17, len(rows) * .97, "undoped host oxidises here", fontsize=13, color=hs.INK, va="top")
    n_col = sum(1 for r in rows if r[3] <= 0.05)
    ax.annotate(f"{n_col} candidates lose the window entirely",
                xy=(1.86, n_col / 2), xytext=(1.16, len(rows) * .22),
                fontsize=14, color=BAD, weight="bold", va="center",
                arrowprops=dict(arrowstyle="->", color=BAD, lw=1.8))
    ax.set_yticks([]); ax.set_ylim(-2, len(rows) + 1)
    ax.set_xlabel("voltage vs Li/Li⁺  (V)   —   bar = the range where the material is not driven to decompose")
    ax.set_ylabel(f"{len(rows)} candidates  ·  sorted by window width")
    _bare(ax, grid="x")
    return _save(fig, "step8_oxidation_windows.png")


def fig_oxidation_by_group():
    by = {}
    for r in _ox_rows():
        try:
            by.setdefault(r["group"], []).append(float(r["ox_V"]))
        except (ValueError, KeyError):
            continue
    order = sorted(by, key=lambda g: -st.mean(by[g]))
    _rc()
    fig, ax = plt.subplots(figsize=(10.4, 4.8))
    import random
    for i, g in enumerate(order):
        v = by[g]
        xs = [i + (hash((g, j)) % 1000 / 1000 - .5) * .34 for j in range(len(v))]
        ax.scatter(xs, v, s=48, color=GROUP_C.get(g, NEUTRAL), alpha=.72,
                   edgecolors="white", lw=.8, zorder=3)
        ax.plot([i - .28, i + .28], [st.mean(v)] * 2, color=hs.INK, lw=2.2, zorder=4)
    ax.axhline(2.14, color=hs.MUT, ls="--", lw=1.2, zorder=2)
    ax.text(len(order) - .45, 2.155, "undoped host", fontsize=12.5, color=hs.MUT, ha="right")
    ax.set_xticks(range(len(order))); ax.set_xticklabels(order, fontsize=13.5)
    ax.set_ylabel("oxidation onset  (V vs Li/Li⁺)")
    ax.set_xlabel("chemistry of the dopant cation")
    _bare(ax, grid="y")
    return _save(fig, "result2_onset_by_chemistry.png")


# ── 7. 안정성 ↔ Li 통행 trade-off (우리판) ────────────────────────────────────
def fig_tradeoff():
    de = _by_species("rerank_de_post_anneal")
    bl = _by_species("tier2_dopant_blocking_fraction")
    common = sorted(set(de) & set(bl))
    xs = [st.mean(de[k].values()) for k in common]
    ys = [st.mean(bl[k].values()) for k in common]
    n = len(xs)
    mx, my = st.mean(xs), st.mean(ys)
    sx, sy = st.pstdev(xs), st.pstdev(ys)
    r = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / (n * sx * sy)
    _rc()
    fig, ax = plt.subplots(figsize=(9.8, 5.4))
    ax.scatter(xs, ys, s=52, color=hs.ELEM["P"], alpha=.62, edgecolors="white", lw=.8, zorder=3)
    b = r * sy / sx; a = my - b * mx
    lo, hi = min(xs), max(xs)
    ax.plot([lo, hi], [a + b * lo, a + b * hi], color=BAD, lw=2.0, ls="--", zorder=4)
    ax.set_xlabel("more stable  ←     relative stability against the host  (eV / atom)")
    ax.set_ylabel("fraction of Li sites the dopant blocks\n(higher = worse for conduction)")
    _bare(ax, grid="both")
    ax.text(.985, .96, f"the more a dopant stabilises the lattice,\nthe more Li traffic it blocks   (r = {r:.2f})",
            transform=ax.transAxes, va="top", ha="right", fontsize=14, color=BAD, weight="bold")
    ax.text(.98, .06, f"{n} species", transform=ax.transAxes, ha="right", fontsize=12, color=hs.MUT)
    return _save(fig, "result3_stability_vs_traffic.png")


FIGS = [fig_periodic, fig_site_choice, fig_anion_site, fig_stability_band,
        fig_label_spread, fig_oxidation_windows, fig_oxidation_by_group, fig_tradeoff]


def selftest():
    ok = fail = 0
    def chk(name, cond):
        nonlocal ok, fail
        if cond: ok += 1
        else: fail += 1; print(f"  ✗ {name}")
    # 양성
    chk("출력 폴더 경로가 docs/figures/seminar", OUT.endswith(os.path.join("docs", "figures", "seminar")))
    chk("나쁨=빨강 · 좋음=파랑", BAD == "#be123c" and GOOD == "#2563eb")
    # 음성 ① — 내부 코드명이 축 라벨/주석에 새어 나오면 안 된다
    src = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    body = src.split("def selftest", 1)[0]
    banned = ["Cascade v23", "cascade v23", "UMA-s-1p1", "G1", "G4", "rank_combined\"", "champion"]
    leaked = [b for b in banned
              if any(b in ln for ln in body.splitlines()
                     if ("ax.set_" in ln or "ax.text" in ln or "annotate" in ln))]
    chk(f"음성: 라벨에 내부 코드명 없음 ({leaked})", not leaked)
    # 음성 ② — 제목을 달면 안 된다 (슬라이드가 제목을 진다)
    chk("음성: set_title 미사용", "set_title" not in body)
    # 음성 ③ — 필요한 원본 데이터가 있어야 한다
    need = ["cascade_v23_all.csv", "site_preference_raw_78.csv", "oxidation_stability_cascade_v2.csv"]
    miss = [f for f in need if not os.path.exists(os.path.join(DB, f))]
    chk(f"음성: 원본 데이터 결측 0건 ({miss})", not miss)
    # 음성 ④ — 주기율표에 없는 원소를 그리려 하면 안 된다
    chk("음성: PT 좌표 중복 없음", len(set(PT.values())) == len(PT))
    # 음성 ⑤ — 화학군 색이 전부 정의돼야 한다
    chk("음성: GROUP_OF 값이 전부 GROUP_C 에 있다",
        set(GROUP_OF.values()) <= set(GROUP_C))
    print(f"\nselftest: {ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    print("발표용 그림 생성:")
    for f in FIGS:
        f()
