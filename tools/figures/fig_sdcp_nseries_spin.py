#!/usr/bin/env python3
"""fig_sdcp_nseries_spin.py — SDCP doped-state spin partition: why 7.7 + 79.7 ≠ 100.

무엇을 그리나
  (a) n=6 D• 의 Loewdin 스핀을 **네 칸으로 100 % 까지** 나눈 가로 막대 —
      SO₃ 7.7 · 아릴 고리 79.7 · 에테르 O 12.1 · 기타 0.5 (고리 H −0.2 + 알킬/말단 H 0.7).
      "두 칸만 더하면 87.4" 가 왜 정상인지 한눈에 보이게 하는 것이 목적이다.
  (b) n = 1 · 2 · 3(end) · 3(mid) · 6 의 같은 분할 (7월 값은 SO₃·백본 두 칸만 있어
      나머지를 **가르지 못한다** → 빗금 한 칸 'unresolved remainder').
  ⛔ (c) 고리별 프로파일은 **2026-09-09 에 원고에서 뺐다** (1저자 결정) — 그림은 (a)(b) 둘이다.
     데이터·CSV 는 남는다(`ring_profile()` · CSV_RING). 사유는 원고 문서의 결정 블록 참조.

데이터 원본: db/properties/sdcp_nseries_spin_2026_09_08.json — 숫자는 여기서만 읽는다.
  그림 옆에 Origin-ready CSV 두 개를 db/properties/ 에 같이 쓴다.

⛔ 이 도구가 **못 하는 것**
  · 자가도핑의 증거를 만들지 않는다 — 산화 상태(D•)를 **주고** 스핀 위치를 본 것이다.
  · 전역 최소 스핀 상태를 보증하지 않는다 (fresh SCF 한 번, 7월과 같은 한계).
  · n=1–3 의 나머지를 에테르 O 와 H 로 가르지 못한다 — 7월 표에 그 분해가 없다.
    빗금 칸은 "모른다" 는 표시지 "기타" 가 아니다.
  · CSV_RING 의 값은 고리 **원자만**(7월 정의)이다 — 말단 α-H 의 −0.2 는 참고 열에만 있다.
    도핑 자리가 어느 고리인지는 이 그림이 말하지 않는다 (JSON site 필드가 비어 있다) — 그래서
    "자리 근방에 국재" 같은 해석 라벨을 붙이지 않는다.
  · 고리별 합이 backbone_july 와 0.1 %p 넘게 다르면 그리지 않는다 (정의가 바뀌었는데 라벨이 그대로인 사고 방지).
  · SP 값과 섞지 않는다 — Opt 계열만 그린다.

  python3 tools/figures/fig_sdcp_nseries_spin.py
  python3 tools/figures/fig_sdcp_nseries_spin.py --out docs/figures/sdcp_nseries_spin/x.png
  python3 tools/figures/fig_sdcp_nseries_spin.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, ELEM, apply_axes  # noqa: E402

DB = "db/properties/sdcp_nseries_spin_2026_09_08.json"
OUT_PNG = "docs/figures/sdcp_nseries_spin/sdcp_nseries_spin_partition.png"
CSV_PART = "db/properties/sdcp_nseries_spin_partition_fig.csv"
CSV_RING = "db/properties/sdcp_n6_ring_profile_fig.csv"

COL = {
    "so3": ELEM["S"],       # sienna — sulfonate group
    "ring": "#7c3aed",      # violet — aryl (thiophene) rings, the π backbone
    "ether": ELEM["O"],     # crimson — ether O
    "other": "#9ca3af",     # grey — H / alkyl linker
    "unres": "#d1d5db",     # light grey + hatch — not resolved in the July data
}
TOL = 0.06   # % — 반올림(0.1) 두 번 허용


class PartitionError(SystemExit):
    pass


def load(repo=REPO):
    return json.loads((Path(repo) / DB).read_text(encoding="utf-8"))


def rows(db):
    """(label, so3, ring, ether, other, unresolved, resolved?) — 각 행이 100 이어야 한다."""
    out = []
    for v in db["값"]:
        n, site = v["n"], v.get("site", "-")
        so3, ring = float(v["SO3_pct"]), float(v["backbone_pct"])
        if v.get("ether_O_pct") is not None:                     # fully resolved (n=6)
            eth, oth, unres, res = float(v["ether_O_pct"]), float(v["other_pct"]), 0.0, True
        else:
            rem = v.get("remainder_pct")
            if rem is None:
                raise PartitionError(f"n={n} {site}: remainder_pct 없음 — 100 까지 못 채운다")
            eth, oth, unres, res = 0.0, 0.0, float(rem), bool(v.get("remainder_resolved"))
            if res and abs(unres) > TOL:
                raise PartitionError(f"n={n} {site}: resolved 인데 나머지 {unres} 가 0 이 아니다")
        tot = so3 + ring + eth + oth + unres
        if abs(tot - 100.0) > TOL:
            raise PartitionError(f"n={n} {site}: 합 {tot:.2f} ≠ 100 — 분해가 닫히지 않았다")
        short = {"A-ring": "A", "end(A)": "end", "mid(B)": "mid"}.get(site, site)
        lab = f"n = {n}" if site in ("-", "") or n == 6 else f"n = {n} ({short})"
        out.append(dict(n=n, site=site, label=lab, so3=so3, ring=ring, ether=eth,
                        other=oth, unresolved=unres, resolved=res))
    return out


def ring_profile(db):
    """n=6 ring0..ring5 (%, 고리 원자만 = 7월 정의) — 합이 backbone_july(backbone_pct) 여야 한다.

    참고 열(+고리H)은 `ring_profile_incl_ringH_pct` 에서 같이 읽어 CSV 에만 싣는다."""
    v6 = [v for v in db["값"] if v["n"] == 6][0]
    prof = v6.get("ring_profile_pct")
    if not prof:
        raise PartitionError("n=6 ring_profile_pct 없음 — (c) 를 그릴 수 없다")
    keys = sorted(prof, key=lambda k: int(k.replace("ring", "")))
    vals = [float(prof[k]) for k in keys]
    july = float(v6["backbone_pct"])
    if abs(sum(vals) - july) > 0.11:
        raise PartitionError(f"ring 합 {sum(vals):.1f} ≠ backbone_july {july} — "
                             "정의가 바뀌었는데 라벨이 그대로다 (+고리H 값을 넣었나?)")
    ref = v6.get("ring_profile_incl_ringH_pct") or {}
    return keys, vals, [float(ref[k]) if k in ref else None for k in keys]


def write_csv(rws, keys, vals, ref=None, repo=REPO):
    ref = ref if ref is not None else [None] * len(keys)
    p1 = Path(repo) / CSV_PART
    p1.parent.mkdir(parents=True, exist_ok=True)
    with p1.open("w", newline="", encoding="utf-8-sig") as f:
        f.write("# SDCP doped state (doublet D.), Loewdin spin partition summing to 100 %. "
                "ORCA r2SCAN-3c Opt. Source: db/properties/sdcp_nseries_spin_2026_09_08.json\n")
        f.write("# aryl_rings = ring atoms only (July definition). For n=1-3 the July table "
                "gives only SO3 and rings, so the balance is one unresolved column "
                "(ether O + H, not separable). Not evidence of self-doping.\n")
        w = csv.writer(f)
        w.writerow(["n", "site", "SO3_pct", "aryl_rings_pct", "ether_O_pct",
                    "other_H_linker_pct", "unresolved_remainder_pct", "total_pct",
                    "remainder_resolved"])
        for r in rws:
            w.writerow([r["n"], r["site"], r["so3"], r["ring"], r["ether"], r["other"],
                        r["unresolved"],
                        round(r["so3"] + r["ring"] + r["ether"] + r["other"] + r["unresolved"], 1),
                        "yes" if r["resolved"] else "no"])
    p2 = Path(repo) / CSV_RING
    with p2.open("w", newline="", encoding="utf-8-sig") as f:
        f.write("# n=6 D. Loewdin spin per thiophene ring, %. spin_pct_ring_atoms = ring atoms only "
                "(July definition; sums to backbone 79.7). spin_pct_incl_ring_H = reference including the "
                "terminal alpha-H of ring0/ring5 (sums to 79.5; the -0.2 is spin polarization on ring5's H). "
                "Re-analysis 2026-09-08 (gabia analyze_n6_v2.log), no recomputation.\n")
        w = csv.writer(f)
        w.writerow(["ring_index", "ring_label", "spin_pct_ring_atoms", "spin_pct_incl_ring_H", "definition"])
        for k, v, r in zip(keys, vals, ref):
            w.writerow([int(k.replace("ring", "")), k, v, "" if r is None else r, "ring atoms only (July definition)"])
    return p1, p2


def _seg(ax, y, x0, w, color, hatch=None, h=0.55):
    ax.barh(y, w, left=x0, height=h, color=color, edgecolor="white", lw=0.8,
            hatch=hatch, zorder=3)
    return x0 + w


def draw(db, out, repo=REPO):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    rws = rows(db)
    keys, vals, _ref = ring_profile(db)
    r6 = [r for r in rws if r["n"] == 6][0]

    fig = plt.figure(figsize=(11.5, 7.6))
    # ⛔ 2026-09-09 (1저자 결정) — 패널 (c) 고리별 프로파일을 **원고에서 뺐다**.
    #   남기는 주장은 (a)(b) 하나뿐이다: 홀이 술폰산 → 백본 π (SO₃ 7.7 % · 백본 79.7 %).
    #   뺀 이유는 kb/papers/self_doping_dft_paragraph_2026_09_08.md 의 결정 블록에 있다 —
    #   고리별 값으로 말하려면 "왜 산화 자리가 최대가 아닌가" 에 답해야 하는데
    #   대조가 없고(n=6 1점·자리 1개) fresh SCF 한 번이며 오차막대가 없다.
    #   ⚠ 데이터(`ring_profile`)와 CSV 출력은 **남긴다** — 실측이라 지우지 않는다.
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.55],
                          hspace=0.62, left=0.10, right=0.985, top=0.93,
                          bottom=0.235)
    axA = fig.add_subplot(gs[0, 0])
    axB = fig.add_subplot(gs[1, 0])

    # ── (a) n=6, one bar to 100 % ─────────────────────────────────────────────
    x = 0.0
    segs = [("so3", r6["so3"], "SO$_3$ group"), ("ring", r6["ring"], "aryl rings"),
            ("ether", r6["ether"], "ether O"), ("other", r6["other"], "other")]
    for key, w, name in segs:
        x1 = _seg(axA, 0, x, w, COL[key], h=0.62)
        mid = (x + x1) / 2
        if w >= 12:
            axA.text(mid, 0, f"{name}\n{w:.1f} %", ha="center", va="center", fontsize=11,
                     color="white", fontweight="bold", zorder=4)
        else:   # narrow segment: label above with a leader (SO3 7.7, other 0.5)
            axA.annotate(f"{name} {w:.1f} %", xy=(mid, 0.31), xytext=(mid, 0.78),
                         ha="center", va="bottom", fontsize=9.5, color=INK,
                         arrowprops=dict(arrowstyle="-", color=MUT, lw=0.8))
        x = x1
    # bracket: the two named groups vs the balance
    named = r6["so3"] + r6["ring"]
    for a, b, txt, dy in ((0, named, f"named in the table: SO$_3$ + rings = {named:.1f} %", -0.55),
                          (named, 100, f"balance {100 - named:.1f} %", -0.55)):
        axA.plot([a + 0.3, b - 0.3], [dy, dy], color=INK, lw=1.0)
        axA.plot([a + 0.3, a + 0.3], [dy, dy + 0.08], color=INK, lw=1.0)
        axA.plot([b - 0.3, b - 0.3], [dy, dy + 0.08], color=INK, lw=1.0)
        axA.text((a + b) / 2, dy - 0.12, txt, ha="center", va="top", fontsize=9.5, color=INK)
    axA.text(100.6, 0, "= 100.0 %", ha="left", va="center", fontsize=11, color=INK,
             fontweight="bold")
    axA.set_xlim(0, 112)
    axA.set_ylim(-1.15, 1.05)
    axA.set_yticks([])
    axA.set_xticks(range(0, 101, 10))
    axA.spines["left"].set_visible(False)
    apply_axes(axA, "Löwdin spin population (% of total spin = 1.000)", None,
               "(a)  n = 6 doped state (D$^{\\bullet}$): the whole spin, four groups", fontsize=11)
    axA.title.set_ha("left"); axA.title.set_position((0.0, 1.0))

    # ── (b) stacked bars vs n ────────────────────────────────────────────────
    ys = list(range(len(rws)))[::-1]
    for y, r in zip(ys, rws):
        x = 0.0
        x = _seg(axB, y, x, r["so3"], COL["so3"])
        x = _seg(axB, y, x, r["ring"], COL["ring"])
        if r["resolved"]:
            x = _seg(axB, y, x, r["ether"], COL["ether"])
            x = _seg(axB, y, x, r["other"], COL["other"])
        elif r["unresolved"] > 0:
            x = _seg(axB, y, x, r["unresolved"], COL["unres"], hatch="////")
        # direct labels for the two named groups
        axB.text(r["so3"] / 2, y, f"{r['so3']:.1f}", ha="center", va="center", fontsize=8.5,
                 color="white", fontweight="bold", zorder=4)
        axB.text(r["so3"] + r["ring"] / 2, y, f"{r['ring']:.1f}", ha="center", va="center",
                 fontsize=8.5, color="white", fontweight="bold", zorder=4)
        tail = r["ether"] + r["other"] if r["resolved"] else r["unresolved"]
        if tail > 0:
            axB.text(101, y, f"{tail:.1f}", ha="left", va="center", fontsize=8.5, color=MUT)
    axB.set_yticks(ys)
    axB.set_yticklabels([r["label"] for r in rws], fontsize=10, color=INK)
    axB.set_xlim(0, 108)
    axB.set_xticks(range(0, 101, 20))
    axB.axvline(50, color=MUT, lw=0.7, ls=":", zorder=2)
    axB.set_ylim(-0.95, len(rws) - 0.45)
    axB.text(50, -0.72, "50 %", ha="center", va="center", fontsize=8, color=MUT,
             bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))
    apply_axes(axB, "Löwdin spin population (%)", None,
               "(b)  Same partition vs oligomer length", fontsize=11)
    axB.title.set_ha("left"); axB.title.set_position((0.0, 1.0))
    handles = [Patch(color=COL["so3"], label="SO$_3$ group"),
               Patch(color=COL["ring"], label="aryl rings (ring atoms only)"),
               Patch(color=COL["ether"], label="ether O"),
               Patch(color=COL["other"], label="other (ring H, linker H)"),
               Patch(facecolor=COL["unres"], hatch="////", edgecolor="white",
                     label="balance not resolved in July data")]
    axB.legend(handles=handles, fontsize=8.2, frameon=False, loc="upper left",
               bbox_to_anchor=(-0.02, -0.17), ncol=3, handlelength=1.4, columnspacing=1.2)

    import textwrap
    note = ("ORCA r2SCAN-3c, optimized geometry, doublet (H-removed doped model D\u2022), "
            "L\u00f6wdin spin populations, total spin 1.000. 'Aryl rings' = ring atoms only, "
            "the definition used in the July table, so SO3 + rings alone give 87.4 % at n = 6; "
            "the balance is ether O (+12.1) and H/linker (+0.5, of which ring H is \u22120.2 by "
            "spin polarization). n = 1\u20133 are transcribed from the July series, where the "
            "balance was not split into ether O and H. The oxidized state is imposed: this is "
            "not evidence of self-doping.")
    for i, line in enumerate(textwrap.wrap(note, 150)):
        fig.text(0.10, 0.088 - 0.023 * i, line, fontsize=7.8, color=MUT, ha="left", va="top")

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=300)
    plt.close(fig)
    return out


def selftest():
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m)
        if c:
            ok += 1
        else:
            bad += 1

    db = load()
    rws = rows(db)
    chk(len(rws) == 5, "행 5개 (n=1·2·3end·3mid·6)")
    chk(all(abs(r["so3"] + r["ring"] + r["ether"] + r["other"] + r["unresolved"] - 100) <= TOL
            for r in rws), "모든 행이 100 으로 닫힌다")
    r6 = [r for r in rws if r["n"] == 6][0]
    chk(r6["resolved"] and r6["ether"] == 12.1 and r6["other"] == 0.5,
        "n=6 은 에테르 O 12.1 · 기타 0.5 로 완전 분해")
    chk(abs(r6["so3"] + r6["ring"] - 87.4) < TOL, "n=6 두 칸 합 87.4 (표에 오르는 값)")
    chk(all(not r["resolved"] for r in rws if r["n"] in (2, 3)),
        "n=2·3 의 나머지는 unresolved 로 표시된다 (7월 표에 분해 없음)")
    keys, vals, ref = ring_profile(db)
    chk(keys == [f"ring{i}" for i in range(6)], "ring0..ring5 순서")
    chk(abs(sum(vals) - 79.7) < 0.11, "ring 합 79.7 = backbone_july (고리 원자만 · 7월 정의)")
    chk(max(vals) == vals[4], "최댓값은 ring4 (23.3)")
    chk(ref[5] == 19.8 and ref[0] == 3.8 and abs(sum(ref) - 79.5) < 0.11,
        "참고 열(+고리H) 은 합 79.5 — 말단 α-H 의 −0.2 가 ring5 에 있다")

    # ⛔음성 ①: 합이 100 이 아닌 행은 그리지 않는다
    bad_db = json.loads(json.dumps(db))
    bad_db["값"][4]["other_pct"] = 3.0
    try:
        rows(bad_db)
        chk(False, "⛔음성: 합 102.5 행이 통과하면 안 된다")
    except PartitionError as e:
        chk("≠ 100" in str(e), "⛔음성: 합이 100 이 아니면 PartitionError")

    # ⛔음성 ②: remainder 없는 옛 행은 100 까지 못 채우므로 거부
    bad_db = json.loads(json.dumps(db))
    del bad_db["값"][1]["remainder_pct"]
    try:
        rows(bad_db)
        chk(False, "⛔음성: remainder_pct 없는 행이 통과하면 안 된다")
    except PartitionError as e:
        chk("remainder_pct" in str(e), "⛔음성: remainder_pct 없으면 거부")

    # ⛔음성 ③: ring 합이 backbone_july 와 다르면 (예: +고리H 값을 잘못 넣으면) 거부
    bad_db = json.loads(json.dumps(db))
    bad_db["값"][4]["ring_profile_pct"] = dict(bad_db["값"][4]["ring_profile_incl_ringH_pct"])   # 합 79.5
    try:
        ring_profile(bad_db)
        chk(False, "⛔음성: +고리H 값(합 79.5)이 7월 정의 자리에 들어가면 막아야 한다")
    except PartitionError as e:
        chk("backbone_july" in str(e), "⛔음성: ring 합 ≠ backbone_july 면 거부 (+고리H 값 혼입 차단)")

    # ⛔음성 ④: resolved=true 인데 나머지가 남으면 거부
    bad_db = json.loads(json.dumps(db))
    bad_db["값"][1]["remainder_resolved"] = True
    try:
        rows(bad_db)
        chk(False, "⛔음성: resolved 인데 나머지 5.1 이 통과하면 안 된다")
    except PartitionError as e:
        chk("resolved" in str(e), "⛔음성: resolved 표시와 나머지가 모순이면 거부")

    # 양성: 실제로 그려지고 CSV 두 개가 나온다 (임시 폴더)
    import tempfile
    T = Path(tempfile.mkdtemp())
    out = draw(db, T / "x.png")
    chk(Path(out).stat().st_size > 20_000, "PNG 생성")
    p1, p2 = write_csv(rws, keys, vals, ref, repo=T)
    txt = p1.read_text(encoding="utf-8-sig").splitlines()
    chk(txt[2].startswith("n,site,SO3_pct,aryl_rings_pct,ether_O_pct"), "CSV 열 이름 명시적")
    chk(sum(1 for l in txt if l and not l.startswith("#")) == 6, "CSV 데이터 5행 + 헤더")
    chk(all(float(l.split(",")[7]) == 100.0 for l in txt[3:]), "CSV total_pct 전부 100.0")
    _rl = p2.read_text(encoding="utf-8-sig").splitlines()
    chk(len(_rl) == 8 and _rl[1].startswith("ring_index,ring_label,spin_pct_ring_atoms,spin_pct_incl_ring_H")
        and _rl[-1].split(",")[2:4] == ["20.0", "19.8"], "ring CSV 6행 + 헤더 + 주석 · 두 정의 열 (ring5 20.0 / 19.8)")
    print(f"  selftest: ⭕ {ok} · ⛔ {bad}")
    return bad == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / OUT_PNG))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    db = load()
    rws = rows(db)
    keys, vals, ref = ring_profile(db)
    out = draw(db, a.out)
    p1, p2 = write_csv(rws, keys, vals, ref)
    print(f"PNG  {out}\nCSV  {p1}\nCSV  {p2}")


if __name__ == "__main__":
    main()
