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
from cascade_ids import base_species, slot_key

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


_SUBS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def formula(s):
    """`V2O5` → `V₂O₅`. 덱 다른 그림(roster·anion site)과 표기를 맞춘다.

    ⚠ 조성식 전용이다 — `x005` 같은 **라벨**에 쓰면 안 된다(숫자가 내려가 버린다).
    """
    return s.translate(_SUBS)


def _write_csv(name, cols, rows, header=()):
    """Origin 재작도용 CSV 를 db/properties/ 에 떨군다 (하우스 규칙: 데이터 그림은 CSV 동반).

    header 는 `#` 주석 줄들 — **열 이름만으로 안 되는 단서**(기준계·라벨 함정 등)를 여기 적는다.
    이 파일의 `_read()` 가 `#` 를 걸러내므로 우리 도구끼리도 그대로 읽힌다.
    """
    p = os.path.join(DB, name)
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        for h in header:
            f.write(h.rstrip() + "\n")
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
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


#: 점수 풀 — (csv, 컬러바 라벨). v2 가 기본이다 (2026-08-18).
POOLS = {
    "v2": ("cascade_v23_ranked_v2.csv", "composite score  (89-species pool, 2026-08-13)"),
    "v1": ("cascade_v23_ranked.csv", "composite score  (47-species pool, 2026-06-29)"),
}


def fig_periodic(pool="v2"):
    """주기율표 성능 지도 — 원본(plot_cascade_summary.py) 양식을 발표용으로 다시 그린다.

    ⚠ **순위로 인용하면 안 된다.** 승인된 current ranking 은 0종이다 (감사표
      db/properties/cascade_audit_artifact_status.csv: v1=superseded,
      v2=recovered_diagnostic). 슬라이드 캡션이 그 단서를 진다.

    풀 선택 (2026-08-18)
      기본을 **v2(89종)** 로 바꿨다. v2 는 v1 의 **완전한 상위집합**이고(v1 전용 종 0),
      원소 36개가 같으며, 두 풀의 블록 패턴이 일치한다 — selftest 가 그걸 검사한다.
      v1 대비 점수가 평균 +0.050 오르는데, 이는 순위 변화가 아니라 min-max 정규화
      모집단이 커진 데 따른 **수평 이동**이다.
      ⚠ AlI3 는 **두 풀 모두** 없다 — v2 만의 결함이 아니라 캠페인 공백이다.

    ⚠ 이 함수의 ax.text 는 **칸 라벨**(원소 기호·숫자)이라 '그림 안 글씨 금지' 규칙의 예외다.
      문장은 넣지 않는다.
    """
    csv_name, cb_label = POOLS[pool]
    import csv as _csv
    from matplotlib.patches import Rectangle as _R
    import matplotlib.pyplot as _plt
    D = []
    for r in _read(os.path.join(DB, csv_name)):
        try:
            D.append(dict(dop=r["dopant"], comp=float(r["score"]),
                          de=float(r["de"]) if r.get("de") else 0.0))
        except (KeyError, ValueError):
            continue
    import re
    best = {}
    for x in D:
        for m in re.findall(r"[A-Z][a-z]?", base_species(x["dop"])):
            if m in ("O", "S", "F", "Cl", "Br", "I", "N"):
                continue
            if m not in best or x["comp"] > best[m]["comp"]:
                best[m] = x

    lo = min(x["comp"] for x in D); hi = max(x["comp"] for x in D)
    cmap = hs.score_cmap()          # RdYlGn 대체 — 적록색맹·인쇄·house 색 (house_style)
    _rc()
    fig, ax = _plt.subplots(figsize=(14.5, 6.6))
    for el, (c, r) in PT.items():
        if el in best:
            x = best[el]
            t = (x["comp"] - lo) / (hi - lo)
            col = cmap(t)
            # ⚠ 글자색을 칸 색에서 정한다 (2026-08-18). 앞 판은 늘 INK 라 진한 칸
            #   (Sc·Cr·Cu·Gd)의 기호와 점수가 슬라이드에서 안 읽혔다.
            fg = hs.on_fill(col)
            sub = fg if fg != hs.INK else "#4b5563"
            ax.add_patch(_R((c, -r), 0.92, 0.92, facecolor=col, edgecolor="#374151", lw=0.9))
            ax.text(c + 0.46, -r + 0.63, el, ha="center", va="center",
                    fontsize=15, fontweight="bold", color=fg)
            ax.text(c + 0.46, -r + 0.34, f"{x['comp']:.2f}", ha="center", va="center",
                    fontsize=11, color=fg)
            ax.text(c + 0.46, -r + 0.13, f"de {x['de']:+.1f}", ha="center", va="center",
                    fontsize=8, color=sub)
        else:
            ax.add_patch(_R((c, -r), 0.92, 0.92, facecolor="#f1f5f9",
                            edgecolor="#cbd5e1", lw=0.7))
            ax.text(c + 0.46, -r + 0.46, el, ha="center", va="center",
                    fontsize=13, color="#94a3b8")
    ax.set_xlim(0.4, 16.4); ax.set_ylim(-8.05, 0.10); ax.axis("off")
    sm = _plt.cm.ScalarMappable(cmap=cmap, norm=_plt.Normalize(lo, hi))
    cb = fig.colorbar(sm, ax=ax, fraction=0.022, pad=0.01)
    cb.set_label(cb_label, fontsize=12)
    cb.ax.tick_params(labelsize=10)
    # ⚠ 파일명에 **빌드 날짜**를 박되 컬러바 라벨은 **데이터 날짜**를 유지한다.
    #   둘은 다른 것이고, 섞으면 6월 점수가 8월 결과로 읽힌다 (오늘 β 0.77 사고와 같은 종류).
    if pool != "v2":
        return _save(fig, f"roster_periodic_table_pool_{pool}.png")
    _save(fig, "roster_periodic_table_build_2026-08-18.png")
    return _save(fig, "roster_periodic_table.png")


# ── 2. 어느 자리를 고르는가 ────────────────────────────────────────────────────
def fig_site_choice():
    """자리 선호 vs 이온 반지름.

    ⚠⚠ 2026-08-18 정정 — 세 점은 **시드가 아니라 도핑 농도**다 (라벨 x002/x005/x010).
      ⛔ 라벨을 **실제 x 로 읽지 말 것.** 실측된 한 건: `Y2O3_x005` = 47원자 셀에 Y 2개
        = 4.3 at% = P 자리의 33 % (kb/results/site_preference_findings_2026_06_19.md).
        다른 캠페인(cascade multi_category_v23)은 같은 라벨을 쓰면서 actual_x 가 셋 다
        0.25 라 농도시리즈가 **무효**였다(hard_dopant_handling_protocol.md).
        이 캠페인은 그게 아니다 — 26종 중 25종이 세 농도에서 dE 가 다르다(폭 중앙값 1.53 eV).
      앞 판 캡션이 "spread across our three runs" 라고 했는데 **틀렸다.** 막대는 재현
      산포가 아니라 **농도 의존성**이다. 그래서 막대가 0 을 걸치는 것은 잡음이 아니라
      "농도에 따라 자리가 바뀐다" 는 실측이다 (1저자 지적: "B같은경우에는 P 경우도
      Li 경우도 있어"). 26종 중 **6종**(Al·B·Cr·Ge·Ni·Sn)이 그렇다.
    ⚠ 원소 기호와 이 함수의 ax.text 는 **점 라벨**이라 '그림 안 글씨 금지' 예외다.
    """
    rows = _read(os.path.join(DB, "site_preference_raw_78.csv"))
    by, site, unconv = {}, {}, {}
    for r in rows:
        try:
            rad, de = float(r["ionic_radius_6coord_A"]), float(r["dE_per_dopant_eV"])
        except (ValueError, KeyError):
            continue
        by.setdefault(r["M"], []).append((rad, de))
        site.setdefault(r["M"], set()).add(r.get("preferred_site", ""))
        # ⚠ 미수렴 점(3/78) — 원본 헤더: "M@P did not reach fmax; dE is an UPPER bound,
        #   the SIGN stays trustworthy for large cations". 지우지 않고 **표시**한다:
        #   지우면 Ag 평균이 +1.94 → +2.44 로 뛰어 그림이 실제보다 확실해 보인다.
        if r.get("converged") != "y":
            unconv.setdefault(r["M"], []).append(de)
    _rc()
    fig, ax = plt.subplots(figsize=(11.6, 5.2))
    ax.axhline(0, color=hs.INK, lw=1.2, zorder=2)
    MIX = "#b45309"          # 농도에 따라 자리가 바뀌는 종 — 앰버, 속 빈 마커
    labels = []
    for m, v in by.items():
        rad = v[0][0]; des = [d for _, d in v]
        mean = st.mean(des)
        flips = len(site.get(m, set())) > 1
        col = MIX if flips else (GOOD if mean < 0 else BAD)
        ax.plot([rad, rad], [min(des), max(des)], color=col, lw=1.4,
                alpha=.55 if flips else .45, zorder=3)
        ax.scatter([rad], [mean], s=64, zorder=4, lw=1.4 if flips else 1.0,
                   facecolors="white" if flips else col,
                   edgecolors=col if flips else "white")
        for du in unconv.get(m, []):
            ax.scatter([rad], [du], s=34, marker="s", zorder=4.5,
                       facecolors="none", edgecolors=hs.MUT, lw=1.1)
        up = mean >= 0
        labels.append([rad, (max(des) + 0.13) if up else (min(des) - 0.13), m, col, up])
    labels.sort(key=lambda a: (a[0], a[1]))
    for i in range(1, len(labels)):
        x0, y0, _, _, u0 = labels[i - 1]
        x1, y1, _, _, u1 = labels[i]
        if abs(x1 - x0) < 0.025 and u0 == u1 and abs(y1 - y0) < 0.30:
            labels[i][1] = y0 + (0.30 if u1 else -0.30)
    for x, y, m, col, up in labels:
        ax.text(x, y, m, ha="center", va="bottom" if up else "top",
                fontsize=8.5, color=col, alpha=.9, zorder=5,
                fontweight="bold", clip_on=False)
    # 범례 — 마커만. 설명 문장은 슬라이드 캡션이 진다.
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([], [], marker="o", ls="", mfc=BAD, mec="white", ms=8, label="Li site"),
        Line2D([], [], marker="o", ls="", mfc=GOOD, mec="white", ms=8, label="P framework"),
        Line2D([], [], marker="o", ls="", mfc="white", mec=MIX, mew=1.4, ms=8,
               label="changes with x"),
        Line2D([], [], marker="s", ls="", mfc="none", mec=hs.MUT, mew=1.1, ms=7,
               label="not converged (upper bound)"),
    ], loc="lower right", frameon=False, fontsize=10, handletextpad=.4)
    ax.set_xlabel("Shannon ionic radius of the dopant cation  (6-coordinate, Å)")
    ax.set_ylabel("P framework site   ←     ΔE  (eV per dopant)     →   Li site")
    _bare(ax, grid="y")
    return _save(fig, "step1_site_choice.png")


# ── 2b. 자리 조합이 실제로 몇 가지였나 ────────────────────────────────────────
def fig_site_grid():
    """(양이온 자리 × 음이온 자리) 격자에 구조가 몇 개씩 들어갔나 — confusion-matrix 양식.

    왜 이 그림인가 (2026-08-18) — 10장 불릿이 "several structures per compound were
    generated" 라고만 해서 **얼마나·어떻게** 가 비어 있었다. 이 격자는 그 답이다:
      · 9칸이 **전부 채워져** 있다 = 자리 조합을 실제로 훑었다
      · 칸마다 수가 다르다 = 어떤 조합은 애초에 가능한 화합물이 적다
    양식은 1저자가 지정한 confusion matrix 꼴 — 칸 안에 **수 + 비율** 두 줄, 컬러바,
    축 제목. 값 라벨은 `--selftest` 의 LABEL_OK 예외다(문장이 아니라 셀 라벨).

    ⚠ 이 수는 **구조 수**이지 화합물 수가 아니다. 화합물 90종에서 구조 3,615개가 나왔고
      화합물당 중앙값은 30개다. 왼쪽 막대 그림(step2_anion_site)은 champion 행만 세므로
      분모가 다르다 — 두 숫자를 나란히 인용하면 안 된다.
    """
    from collections import Counter as _C
    from matplotlib.colors import LinearSegmentedColormap as _LSC
    rows = _all_rows()
    cn = _C((r.get("cation_site"), r.get("anion_site")) for r in rows
            if r.get("cation_site") and r.get("anion_site"))
    cats = sorted({k[0] for k in cn}, key=lambda c: -sum(v for k, v in cn.items() if k[0] == c))
    ans = sorted({k[1] for k in cn}, key=lambda a: -sum(v for k, v in cn.items() if k[1] == a))
    tot = sum(cn.values())
    cmap = _LSC.from_list("bml_seq", ["#f7fafc", "#bcd7ea", "#5b93c4", "#16365c"])
    _rc()
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    M = [[cn.get((c, a), 0) for a in ans] for c in cats]
    im = ax.imshow(M, cmap=cmap, vmin=0, vmax=max(cn.values()), aspect="auto")
    for i, c in enumerate(cats):
        for j, a in enumerate(ans):
            v = cn.get((c, a), 0)
            fg = hs.on_fill(cmap(v / max(cn.values())))
            ax.text(j, i - 0.16, f"{v:,}", ha="center", va="center",
                    fontsize=16, fontweight="bold", color=fg)
            ax.text(j, i + 0.19, f"{100 * v / tot:.0f} % of all", ha="center", va="center",
                    fontsize=10, color=fg, alpha=.85)
    ax.set_xticks(range(len(ans)))
    ax.set_xticklabels([SITE_LABEL.get(a, a) for a in ans], fontsize=11)
    ax.set_yticks(range(len(cats)))
    ax.set_yticklabels([CATION_LABEL.get(c, c) for c in cats], fontsize=11)
    ax.set_xlabel("Anion site  (where the dopant's O / halide went)", fontsize=11.5)
    ax.set_ylabel("Cation site  (where the dopant metal went)", fontsize=11.5)
    ax.tick_params(length=0)
    ax.set_xticks([x - .5 for x in range(1, len(ans))], minor=True)
    ax.set_yticks([y - .5 for y in range(1, len(cats))], minor=True)
    ax.grid(which="minor", color="white", lw=2.5)
    ax.tick_params(which="minor", length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.030, pad=0.02)
    cb.set_label("structures generated", fontsize=10.5)
    cb.ax.tick_params(labelsize=9.5)
    cb.outline.set_visible(False)
    return _save(fig, "step2_site_grid.png")


# ── 3b. 부피 게이트가 에너지와 독립인가 ──────────────────────────────────────
def fig_screen_axes():
    """|ΔV|/V₀ vs 상대에너지 — **부피 게이트가 에너지로는 못 잡는 것을 잡는다.**

    왜 이 그림인가 (2026-08-18) — 11장이 히스토그램 하나뿐이라 "왜 부피로 자르나,
    에너지로 자르면 되지 않나" 라는 당연한 반문에 답이 없었다. 실측이 답한다:
      · |ΔV| > 25 % 로 떨어뜨린 **100 개**와, 에너지 상위 100 개는 **겹치는 것이 0 개**다
      · 떨어진 것들의 에너지 중앙값은 오히려 **더 낮다** (−0.619 vs −0.480 eV/atom)
      → 에너지만 봤으면 **오히려 좋아 보여서 통과**했을 구조들이다

    ⚠ 세로축은 **이 스크린 안에서만** 비교 가능한 상대에너지다. 생성에너지도
      hull 거리도 아니다 — 절대값으로 인용 금지 (슬라이드 불릿이 그 단서를 진다).
    """
    xs, ys = [], []
    for r in _all_rows():
        try:
            xs.append(abs(float(r["screen_dV_over_V0"])) * 100)
            ys.append(float(r["screen_de_per_atom"]))
        except (ValueError, KeyError, TypeError):
            continue
    CUT = 25.0
    keep = [(x, y) for x, y in zip(xs, ys) if x <= CUT]
    drop = [(x, y) for x, y in zip(xs, ys) if x > CUT]
    _rc()
    # ⚠ 슬라이드에서 Origin 판 히스토그램과 **나란히** 놓인다 (2026-08-18). 이 그림은
    #   기본값(14/12)으로는 왼쪽 Origin 판보다 작아 보인다. 한 단계만 올린다.
    #   ⚠ 크게 올리면 안 된다 — bbox_inches="tight" 라 라벨이 캔버스를 먹어 플롯이
    #     쪼그라든다 (24 pt 로 올렸다가 실제로 그랬다).
    #   ⚠ 축 라벨을 길게 쓰면 폰트를 안 올려도 같은 일이 난다 — 세로 라벨이 축보다
    #     길어지면 캔버스가 위아래로 늘어나 플롯이 가운데서 쪼그라든다. 짧게 쓴다
    #     ("this screen only" 단서는 슬라이드 불릿이 진다).
    plt.rcParams.update({"font.size": 16, "axes.labelsize": 17,
                         "xtick.labelsize": 15, "ytick.labelsize": 15})
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.scatter([x for x, _ in keep], [y for _, y in keep], s=7, alpha=.28,
               color=GOOD, lw=0, zorder=2, label=f"kept ({len(keep):,})")
    ax.scatter([x for x, _ in drop], [y for _, y in drop], s=20, alpha=.9,
               color=BAD, lw=0, zorder=4, label=f"dropped, > 25 % ({len(drop)})")
    ax.axvline(CUT, color=hs.INK, lw=1.2, ls="--", zorder=3)
    # 에너지로 잘랐다면 어디였을지 — 같은 개수만큼 위에서 자른 선
    thr = sorted(ys, reverse=True)[len(drop) - 1]
    ax.axhline(thr, color=hs.MUT, lw=1.1, ls=":", zorder=3)
    ax.set_xlabel("cell volume change during relaxation  (%)")
    ax.set_ylabel("relative energy per atom  (eV)")
    ax.legend(loc="lower left", frameon=False, fontsize=15, markerscale=2.4)
    _bare(ax, grid="y")
    out = _save(fig, "step3_screen_axes.png")
    _rc()                      # 다음 그림을 위해 기본값 복구
    return out


# ── 3. 음이온이 실제로 앉은 자리 ───────────────────────────────────────────────
SITE_LABEL = {"S_16e": "sulfur in the PS₄ corner", "S_4a": "free sulfide", "Cl_4d": "halide site"}
CATION_LABEL = {"Li_24g": "Li 24g", "Li_48h": "Li 48h", "P_4b": "P 4b (framework)"}


def fig_anion_site():
    rows = [r for r in _all_rows() if r.get("rank_combined") == "1" and r.get("anion_site")]
    cnt = {}
    for r in rows:
        cnt[r["anion_site"]] = cnt.get(r["anion_site"], 0) + 1
    items = sorted(cnt.items(), key=lambda kv: -kv[1])
    _rc()
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    # ⛔ 2026-08-18 — 색이 **순위 자리**로 칠해지고 있었다(`cols[i % 3]`). 그래서
    #   할라이드 자리가 황 색, 황 자리 하나가 염소 색이었다 — 화학과 반대다.
    #   원소로 칠한다. 황 부격자 둘은 같은 계열의 진하기 차이로 구분한다.
    SITE_COLOR = {"S_4a": hs.ELEM["S"], "S_16e": "#dd8f5f", "Cl_4d": hs.ELEM["Cl"]}
    for i, (k, v) in enumerate(items):
        ax.barh(-i, v, height=.56, color=SITE_COLOR.get(k, hs.MUT), alpha=.9, zorder=3)
    ax.set_xlim(0, max(cnt.values()) * 1.22); ax.set_ylim(-len(items) + .4, .6)
    # ⚠ 2026-08-18 — set_yticks([]) 로 **부격자 이름이 통째로 빠져** 있었다. 막대 셋이
    #   무엇인지 화면만 봐서는 알 수 없었다. 범주 라벨은 축 라벨이지 '그림 안 문장' 이 아니다.
    ax.set_yticks([-i for i in range(len(items))])
    ax.set_yticklabels([SITE_LABEL.get(k, k) for k, _ in items], fontsize=11.5)
    for i, (_, v) in enumerate(items):
        ax.annotate(str(v), (v, -i), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=11, color=hs.MUT)
    ax.set_xlabel("number of generated candidates that placed the dopant anion there")
    _bare(ax, grid="x")
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


#: 대표 구조 선택이 흔들린다고 볼 폭 (eV/atom). 물리 상수가 아니라 **표시용 기준**이다 —
#: 폭 분포의 꼬리가 여기서 갈린다(중앙 0.037, 88종 중 6종만 초과).
BAND_WIDE = 0.10


def fig_stability_band():
    """종마다 세 챔피언 구조가 host 상대 안정성에서 얼마나 벌어지나.

    ⛔⛔ **세 점은 '같은 것을 세 번 돌린 재현 산포' 가 아니다** (2026-08-18 3회째 적발).
      `concentration_label` 은 x002/x005/x010 인데 `concentration` 열은 270행 **전부 0.25**다.
      세 챔피언이 실제로 다른 것은 **치환 자리와 시드**다. 예: ZrO₂ 는
        x020 → P_4b / S_4a  (s03)
        x050 → Li_24g / S_16e (s01)
        x100 → Li_24g / S_4a  (s01)
      ⇒ "runs agree" 라고 쓰면 안 된다. 맞는 말은 **"이긴 구조의 자리가 달라져도 이 축은
        거의 안 움직인다"** 이고, 그게 오히려 더 센 진술이다.
      근거: kb/results/site_preference_bar_meaning_2026_08_18.md §4b

    그림에 담은 것 (2026-08-18 보강)
      · 폭 > BAND_WIDE 인 종은 **빨강 + 이름표** — 대표 하나로 뭉개면 안 되는 곳을 보여준다.
        (순위 주장이 아니다. 세로 위치가 아니라 **폭**으로 고른 것이다.)
      · 오른쪽 패널 = 폭의 분포. "막대가 짧다" 를 주장이 아니라 **분포로** 보인다.
      · 범례 한 줄이 세 점의 정체를 진다 — 위 ⛔ 를 화면에서 막는 마지막 방어선.

    이 그림이 **못 하는 것**
      · 순위가 아니다. 세로 위치로 종을 고르면 안 된다 (승인된 ranking 0종).
      · 세 점이 자리·시드 중 무엇 때문에 갈렸는지 구분하지 않는다 — 둘이 섞여 있다.
    """
    sp = _by_species("rerank_de_post_anneal")
    order = sorted(sp, key=lambda k: st.mean(sp[k].values()))
    width = {k: max(sp[k].values()) - min(sp[k].values()) for k in order}
    wide = [k for k in order if width[k] > BAND_WIDE]
    _rc()
    fig, (ax, axh) = plt.subplots(
        1, 2, figsize=(12.6, 4.9), gridspec_kw=dict(width_ratios=[4.4, 1.0], wspace=0.28))

    for i, k in enumerate(order):
        v = sorted(sp[k].values())
        hot = k in wide
        ax.plot([i, i], [v[0], v[-1]], color=BAD if hot else NEUTRAL,
                lw=1.9 if hot else 1.1, zorder=4 if hot else 2)
        ax.scatter([i] * len(v), v, s=22 if hot else 15,
                   color=BAD if hot else hs.ELEM["P"], zorder=5 if hot else 3,
                   alpha=.95 if hot else .9, edgecolors="none")
    # 이름표는 **가로**로 — 세로로 세우면 인접한 둘(WO₃·MoO₃)이 서로 파고든다.
    #   그래도 x 가 붙어 있으면 겹치므로 앞 이름과의 간격을 보고 한 층 올린다.
    prev_i, prev_lvl = -99, 0
    for i, k in enumerate(order):
        if k not in wide:
            continue
        lvl = 1 - prev_lvl if i - prev_i < 6 else 0
        ax.annotate(formula(k), (i, max(sp[k].values())), xytext=(0, 9 + 15 * lvl),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=10, color=BAD)
        prev_i, prev_lvl = i, lvl

    ax.set_xticks([]); ax.set_xlim(-2, len(order) + 1)
    ax.set_ylim(min(min(v.values()) for v in sp.values()) - 0.06,
                max(max(v.values()) for v in sp.values()) + 0.30)
    ax.set_xlabel(f"{len(order)} dopant species  ·  sorted by mean  ·  "
                  f"names shown only where the band is wide")
    ax.set_ylabel("relative stability vs host  (eV / atom)")
    # 세 점의 정체 — 범례로 화면에 박아 둔다 ('세 번 돌린 것' 오독 방지)
    from matplotlib.lines import Line2D
    ax.legend(handles=[
        Line2D([], [], color=hs.ELEM["P"], marker="o", ls="none", ms=5,
               label="3 top-ranked structures per species (different site / seed)"),
        Line2D([], [], color=BAD, marker="o", ls="-", ms=5, lw=1.9,
               label=f"band wider than {BAND_WIDE:.2f} eV / atom  ({len(wide)} of {len(order)})"),
    ], loc="lower right", frameon=False, fontsize=10.5, handletextpad=.6)
    # ⬇ 방향 표시 — y 라벨 안에 화살표를 넣으면 회전 때문에 방향이 뒤집혀 보인다.
    ax.annotate("more stable", xy=(-0.115, 0.10), xytext=(-0.115, 0.42),
                xycoords="axes fraction", textcoords="axes fraction",
                rotation=90, ha="center", va="center", fontsize=10.5, color=hs.MUT,
                arrowprops=dict(arrowstyle="->", color=hs.MUT, lw=1.1))
    _bare(ax, grid="y")

    # ── 오른쪽: 폭의 분포 ("막대가 짧다" 를 분포로 보인다) ───────────────────
    ws = sorted(width.values())
    axh.hist(ws, bins=[i * 0.02 for i in range(11)], orientation="horizontal",
             color=hs.ELEM["P"], alpha=.75, zorder=3)
    axh.axhline(BAND_WIDE, color=BAD, ls="--", lw=1.3, zorder=4)
    axh.axhline(st.median(ws), color=hs.INK, ls=":", lw=1.3, zorder=4)
    axh.annotate(f"median {st.median(ws):.3f}", (axh.get_xlim()[1], st.median(ws)),
                 xytext=(-4, 5), textcoords="offset points", ha="right",
                 fontsize=9.5, color=hs.INK)
    axh.set_ylim(0, 0.215)          # 0.20 이면 최대(0.180) 막대가 위 테두리에 붙어 잘려 보인다
    axh.set_ylabel("band width  (eV / atom)")
    axh.set_xlabel("species")
    _bare(axh, grid="x")

    _write_csv("seminar_table_stability_band.csv",
               ["species", "de_min_eV_per_atom", "de_max_eV_per_atom",
                "de_mean_eV_per_atom", "band_width_eV_per_atom", "band_wide_flag"],
               [[k, f"{min(sp[k].values()):.4f}", f"{max(sp[k].values()):.4f}",
                 f"{st.mean(sp[k].values()):.4f}", f"{width[k]:.4f}",
                 "wide" if k in wide else ""] for k in order],
               header=[
                "# Step 4 — representative structure selection (seminar 2026-08)",
                "# de = rerank_de_post_anneal, host-relative stability (NOT hull distance).",
                "# The three values per species are the three top-ranked structures whose folder",
                "#   labels read x020/x050/x100 (or x002/x005/x010 in concentration_label).",
                "# !! THOSE LABELS ARE NOT CONCENTRATIONS — the `concentration` column is 0.25 for",
                "#    all 270 rows. The three differ by substitution SITE and SEED, not by doping",
                "#    level, and they are NOT repeat runs of the same structure.",
                "# band_width = max - min. wide flag = width > %.2f eV/atom." % BAND_WIDE,
               ])
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
    ax.set_ylim(lo, hi); ax.set_xlim(-2, len(order) + 1); ax.set_xticks([])
    ax.set_xlabel(f"{len(order)} dopant species  ·  sorted by mean  ·  names omitted on purpose")
    ax.set_ylabel("Young's modulus  E  (GPa)")
    _bare(ax, grid="y")
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
    ax.set_yticks([]); ax.set_ylim(-2, len(rows) + 1)
    ax.set_xlabel("voltage vs Li/Li⁺  (V)      dashed line = undoped host onset")
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
    ax.set_ylabel("more Li traffic blocked   →\nfraction of Li sites occupied")
    _bare(ax, grid="both")
    return _save(fig, "result3_stability_vs_traffic.png")



# ── 8. STEP 3 — 어떤 구조가 살아남았나 ────────────────────────────────────────
def fig_screen_survival():
    """부피가 얼마나 움직였나. 25 % 넘게 부푼 구조는 다음 단계로 안 보낸다."""
    vals = []
    for r in _all_rows():
        try:
            vals.append(abs(float(r["screen_dV_over_V0"])) * 100)
        except (ValueError, KeyError, TypeError):
            continue
    keep = [v for v in vals if v <= 25]
    drop = [v for v in vals if v > 25]
    _rc()
    fig, ax = plt.subplots(figsize=(10.8, 4.7))
    bins = list(range(0, 62, 2))
    ax.hist(keep, bins=bins, color=GOOD, alpha=.85, zorder=3, label="kept")
    ax.hist([min(v, 60) for v in drop], bins=bins, color=BAD, alpha=.92, zorder=4,
            label="dropped (> 25 %)")
    ax.axvline(25, color=hs.INK, ls="--", lw=1.5, zorder=5)
    ax.legend(frameon=False, fontsize=13, loc="upper right", bbox_to_anchor=(1.0, .78))
    ax.set_xlabel("cell volume change during relaxation  (%)")
    ax.set_ylabel("number of candidate structures")
    _bare(ax, grid="y")
    return _save(fig, "step3_survival.png")


# ── 9. STEP 5 — 흔들었더니 얼마나 내려갔나 ────────────────────────────────────
def fig_anneal_gain():
    vals = []
    for r in _all_rows():
        try:
            vals.append(float(r["anneal_delta_E_meV"]))
        except (ValueError, KeyError, TypeError):
            continue
    down = [v for v in vals if v < 0]
    _rc()
    fig, ax = plt.subplots(figsize=(10.4, 4.6))
    n_, _, _ = ax.hist(vals, bins=44, color=hs.ELEM["P"], alpha=.82, zorder=3)
    ax.axvline(0, color=hs.INK, lw=1.4, zorder=4)
    ax.set_ylim(0, max(n_) * 1.34)
    ax.set_xlabel("energy change caused by the short anneal  (meV per cell)")
    ax.set_ylabel("number of structures")
    _bare(ax, grid="y")
    return _save(fig, "step5_anneal_gain.png")


# ── 10. 무엇이 있고 무엇이 없나 ───────────────────────────────────────────────
def fig_coverage():
    rows = _all_rows()
    # ⚠ raw dopant 로 세면 `WO3` 와 `WO3+Clrich` 가 갈려 303 이 된다 — 정본은 slot_key
    n_slot = len({slot_key(r) for r in rows})
    def cov(col):
        return len({slot_key(r) for r in rows if r.get(col)})
    items = [("candidate structures", n_slot, True),
             ("fast relaxation", n_slot, True),
             ("short anneal", cov("anneal_delta_E_meV"), True),
             ("static Li-path map", cov("bvs_li_proxy_score"), True),
             ("stiffness / equation of state", cov("elastic_E_young_GPa"), True),
             ("oxidation window", n_slot, True),
             ("conductivity from dynamics", 0, False),
             ("cathode interface, adhesion", 0, False)]
    _rc()
    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    for i, (name, v, good) in enumerate(items):
        y = -i
        ax.barh(y, n_slot, height=.52, color="#eef1f5", zorder=2)
        ax.barh(y, v, height=.52, color=(GOOD if good else BAD), alpha=.85, zorder=3)
    ax.set_xlim(-108, n_slot * 1.12)
    ax.set_ylim(-len(items) + .4, .7)
    ax.set_yticks([])
    ax.set_xlabel(f"how many of the {n_slot} planned runs actually produced this")
    _bare(ax, grid="x")
    ax.set_xticks([0, 90, 180, 270])
    return _save(fig, "evidence_coverage.png")


FIGS = [fig_periodic, fig_site_choice, fig_anion_site, fig_site_grid, fig_screen_axes, fig_stability_band,
        fig_label_spread, fig_oxidation_windows, fig_oxidation_by_group, fig_tradeoff,
        fig_screen_survival, fig_anneal_gain, fig_coverage]


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
    # 음성 ⑥ — 그림 안에 문장을 넣지 않는다 (슬라이드가 문구를 진다, 2026-08-16 지시)
    # ⚠ ax.text 예외는 **칸/점 라벨**뿐이다 (원소 기호). fig_periodic 과 fig_site_choice
    #   두 곳만 허용하고, 그 밖에서는 여전히 금지한다 — 그림 안에 문장을 넣지 않는 규칙.
    # ★ 그림 안에 **문장**을 넣지 않는다. 예외는 **칸·점·막대 라벨**뿐이고, 그 라벨을
    #   쓰는 함수를 여기 목록으로 못 박는다. 앞 판은 파일 위치로 갈랐는데(주석 기준 split),
    #   새 그림을 그 뒤에 추가하니 정당한 라벨이 위반으로 잡혔다 — 목록이 맞다.
    import re
    LABEL_OK = {"fig_periodic", "fig_site_choice", "fig_site_grid", "fig_anion_site",
            # 폭이 넓은 6종의 **이름표** — 순위가 아니라 "여기선 대표 하나로 못 뭉갠다"
            # 를 가리키는 범주 라벨이다 (2026-08-18).
            "fig_stability_band"}
    _fns = re.split(r"\ndef ", body)
    _bad = []
    for _f in _fns[1:]:
        _name = _f.split("(", 1)[0].strip()
        if ("ax.text(" in _f or "ax.annotate(" in _f) and _name not in LABEL_OK:
            _bad.append(_name)
    chk(f"음성: 라벨 허용 함수 밖에서 그림 안 글씨 없음 ({_bad})", not _bad)
    # 음성 — 허용 함수 안에서도 **문장**은 금지 (라벨은 짧다). 40자 넘는 리터럴을 잡는다.
    _long = []
    for _f in _fns[1:]:
        if _f.split("(", 1)[0].strip() not in LABEL_OK:
            continue
        for _m in re.finditer(r"ax\.(?:text|annotate)\(([^\n]*)", _f):
            for _q in re.findall(r'"([^"]{40,})"', _m.group(1)):
                _long.append(_q[:36])
    chk(f"음성: 라벨이 문장으로 길어지지 않았다 ({_long})", not _long)
    # 음성 ③ — 필요한 원본 데이터가 있어야 한다
    need = ["cascade_v23_all.csv", "site_preference_raw_78.csv", "oxidation_stability_cascade_v2.csv"]
    miss = [f for f in need if not os.path.exists(os.path.join(DB, f))]
    chk(f"음성: 원본 데이터 결측 0건 ({miss})", not miss)
    # 음성 ④ — 주기율표에 없는 원소를 그리려 하면 안 된다
    chk("음성: PT 좌표 중복 없음", len(set(PT.values())) == len(PT))
    # ★ 슬라이드가 기대는 주장 — "풀을 두 배로 키워도 **블록 패턴**은 안 바뀐다".
    #   캡션이 "read the block pattern, not the order" 라고 말하는 근거가 이것이다.
    #   풀을 바꿨는데 이게 깨지면 그 캡션이 거짓말이 되므로 여기서 막는다 (2026-08-18).
    import csv as _c, io as _io, re as _re
    _AN = {"O", "S", "F", "Cl", "Br", "I", "N"}

    def _best(fn):
        try:
            _rows = [l for l in open(os.path.join(DB, fn)) if not l.startswith("#")]
        except OSError:
            return {}
        b = {}
        for x in _c.DictReader(_io.StringIO("".join(_rows))):
            try:
                sc = float(x["score"])
            except (KeyError, ValueError):
                continue
            for el in _re.findall(r"[A-Z][a-z]?", base_species(x["dopant"])):
                if el not in _AN and (el not in b or sc > b[el]):
                    b[el] = sc
        return b

    _b1, _b2 = _best(POOLS["v1"][0]), _best(POOLS["v2"][0])
    chk("두 풀의 원소 집합이 같다", bool(_b1) and set(_b1) == set(_b2))
    _lo1 = set(sorted(_b1, key=lambda k: _b1[k])[:10])
    _lo2 = set(sorted(_b2, key=lambda k: _b2[k])[:10])
    chk(f"두 풀의 최하위10 집합이 같다 (차이 {sorted(_lo1 ^ _lo2)})", _lo1 == _lo2)
    _late = {"Mn", "Fe", "Co", "Ni", "Cu"}
    chk("후기전이금속 5종이 두 풀 모두 최하위12 안에 있다 (대본이 'red' 라고 부르는 블록)",
        all(_late <= set(sorted(b, key=lambda k: b[k])[:12]) for b in (_b1, _b2)))
    # 음성 — 풀 정의가 비거나 같은 파일을 가리키면 비교가 무의미하다
    chk("음성: 두 풀이 서로 다른 파일이다", POOLS["v1"][0] != POOLS["v2"][0])
    chk("음성: v2 가 v1 의 상위집합이다 (v1 전용 원소 0)", not (set(_b1) - set(_b2)))
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
