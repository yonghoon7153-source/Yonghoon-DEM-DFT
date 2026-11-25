#!/usr/bin/env python3
"""fig_c12_pose_screen.py — SI figure: the MLIP pose screen that C-12 froze.

무엇을 그리나
  LiNiO₂(104) 위 SDCP/PTFE 조각의 **자세 전수 스크린**을 기하(높이·기울기)와
  **앵커 원소쌍**으로 보여 준다. 원고 §Methods 의 "MLIP 가 넓게 훑고 DFT 가 한 점을
  정밀하게 찍는다" 구조를 그림 하나로 세우는 것이 목적이다.

⛔⛔ **에너지 축을 그리지 않는다.**
  `E_pose` 는 결합에너지가 **아니다** — `E_pose = E_complex − E_slab − E_mol(기체 ORCA 기하)`
  라 조각·표면 변형 몫이 실려 자세마다 다르게 상쇄된다
  (`db/properties/sdcp_ptfe_site_preference_uma_v1.json` 의 `do_not_cite`).
  사전등록(`sdcp_c12_claim_prereg_2026_08_31.json` §6)이 MLIP 에 허용한 것은
  **탐색의 폭 · 선정 규칙 · 그 선정이 DFT 전에 동결됐다는 사실** 뿐이다.
  ⇒ 이 그림은 그 셋만 말한다. 순위조차 축으로 쓰지 않는다 (순위는 에너지의 함수다).

⛔ 이 도구가 **못 하는 것**
  · 흡착에너지를 그리지 않는다 — 그건 C-12 DFT 반송 뒤 별도 그림이다.
  · 어느 자세가 "가장 잘 붙는다" 고 말하지 않는다. primary 는 **규칙의 결과**지
    이 그림의 결론이 아니다.
  · 앵커의 `H` 가 **산성 H 인지 탄소결합 H 인지 구분하지 못한다** — 스크린 데이터가
    원소쌍만 담는다. 개별 자세(b00)의 화학은 좌표를 따로 봐야 한다.
  · 걸러진(gated) 자세의 사유를 그리지 않는다 (수만 센다).
  · DFT 를 보지 않는다. 이 그림은 DFT 0잡 시점의 산출물로만 만들어진다.

  python3 tools/figures/fig_c12_pose_screen.py --out figures/fig_c12_pose_screen.png
  python3 tools/figures/fig_c12_pose_screen.py --selftest
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.figures.house_style import INK, MUT, ELEM, apply_axes  # noqa: E402

SCREEN = "db/properties/prospective_basins_2026_08_29.json"
PROTOCOL = "db/properties/sdcp_c12_protocol_2026_08_30.json"
CSV_GEOM = "db/properties/c12_pose_screen_geometry.csv"
CSV_ANCH = "db/properties/c12_pose_screen_anchor_census.csv"

#: 표면 파트너 색. Ni 는 원소 팔레트에 없어 슬레이트를 쓴다 (Li teal · O crimson 과 구분).
SURF_COLOR = {"Li": ELEM["Li"], "O": ELEM["O"], "Ni": "#475569"}
#: 분자쪽 원자 = 마커 모양
MOL_MARKER = {"H": "o", "O": "s", "F": "^", "C": "D"}
FRAG_TITLE = {"sdcp_neutral": "SDCP repeat unit", "ptfe_c10": "PTFE segment (C$_{10}$F$_{22}$)"}


def load(repo=REPO):
    """스크린 + 프로토콜을 읽고 **역할이 실제 스크린에 있는지** 대조한다.

    → (screen_dict, roles) · roles[fragment][basin_id] = "primary" | "sensitivity" | …

    ⛔ 프로토콜이 지목한 basin 이 스크린에 없거나 `rep_label`·`anchor` 가 다르면
      **그림을 그리지 않는다** — 계보가 끊긴 그림은 없는 것보다 나쁘다.
    """
    repo = Path(repo)
    scr = json.loads((repo / SCREEN).read_text(encoding="utf-8"))
    pro = json.loads((repo / PROTOCOL).read_text(encoding="utf-8"))
    # ⛔ 회신 BC P0-4 — 역할 분류 **규칙**의 정본은 프로토콜의 `⛔_자세_역할_규칙_2026_09_02`
    #   다 (비준 대상). 자세 파일의 JSON 키를 역할로 쓰면 비준 없이 분류가 바뀔 수 있다.
    #   ⇒ 대안 자세의 역할은 `ΔE_pose ≤ W0` 규칙으로 **계산**한다.
    _rule = pro.get("⛔_자세_역할_규칙_2026_09_02") or {}
    W0 = _rule.get("W0_eV")
    roles, bad = {}, []
    if W0 is None:
        bad.append("프로토콜에 `⛔_자세_역할_규칙_2026_09_02.W0_eV` 가 없다 — "
                   "역할 분류 규칙 없이 자세에 이름을 붙이지 않는다")
    for frag, spec in (pro.get("2_자세_동결", {}).get("fragments") or {}).items():
        fs = (scr.get("fragments") or {}).get(frag)
        if fs is None:
            bad.append("스크린에 조각 %r 이 없다" % frag)
            continue
        by = {b["basin_id"]: b for b in fs["basins"]}
        for role, want in spec.items():
            if not isinstance(want, dict) or "basin_id" not in want:
                continue
            bid = want["basin_id"]
            got = by.get(bid)
            if got is None:
                bad.append("%s: 프로토콜이 지목한 %s 가 스크린에 없다" % (frag, bid))
                continue
            if got.get("rep_label") != want.get("rep_label"):
                bad.append("%s/%s: rep_label 이 다르다 (%r ≠ %r)"
                           % (frag, bid, got.get("rep_label"), want.get("rep_label")))
            if list(got.get("anchor") or []) != list(want.get("anchor") or []):
                bad.append("%s/%s: anchor 가 다르다 (%r ≠ %r)"
                           % (frag, bid, got.get("anchor"), want.get("anchor")))
            if role == "primary":
                roles.setdefault(frag, {})[bid] = "primary"
            else:
                _d = spec.get("dE_pose_eV")
                if _d is None or W0 is None:
                    bad.append("%s/%s: ΔE_pose 나 W0 가 없어 역할을 **계산할 수 없다** — "
                               "JSON 키를 역할로 대신 쓰지 않는다" % (frag, bid))
                else:
                    roles.setdefault(frag, {})[bid] = (
                        "sensitivity" if float(_d) <= float(W0) else "stress_sensitivity")
    if bad:
        raise SystemExit("⛔ 계보 대조 실패 — 그리지 않는다:\n   " + "\n   ".join(bad))
    return scr, roles


def rows(scr, roles):
    """basin → 평평한 행 목록 (CSV·그림 공용). 열 이름은 명시적으로."""
    out = []
    for frag, fs in (scr.get("fragments") or {}).items():
        for b in fs["basins"]:
            lab = b.get("rep_label") or ""
            p = lab.split("__")
            anc = b.get("anchor") or [None, None, None]
            out.append({
                "fragment": frag,
                "basin_id": b["basin_id"],
                "rep_label": lab,
                "site": p[1] if len(p) > 1 else "",
                "fib": p[2] if len(p) > 2 else "",
                "roll": p[3] if len(p) > 3 else "",
                "anchor_mol_element": anc[0],
                "anchor_surface_element": anc[1],
                "anchor_distance_A": anc[2],
                "height_A": b.get("height_A"),
                "tilt_deg": b.get("tilt_deg"),
                "n_members": b.get("n_members"),
                "role_in_c12": roles.get(frag, {}).get(b["basin_id"], ""),
            })
    return out


def census(rws):
    """앵커 원소쌍 census. → {fragment: Counter[(mol, surf)]}"""
    c = collections.defaultdict(collections.Counter)
    for r in rws:
        c[r["fragment"]][(r["anchor_mol_element"], r["anchor_surface_element"])] += 1
    return c


def write_csv(rws, cen, repo=REPO):
    repo = Path(repo)
    cols = list(rws[0].keys())
    with (repo / CSV_GEOM).open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in sorted(rws, key=lambda x: (x["fragment"], x["basin_id"])):
            w.writerow(r)
    with (repo / CSV_ANCH).open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["fragment", "anchor_molecule_element", "anchor_surface_element",
                    "n_basins"])
        for frag in sorted(cen):
            for (m, s), n in sorted(cen[frag].items(), key=lambda kv: -kv[1]):
                w.writerow([frag, m, s, n])
    return repo / CSV_GEOM, repo / CSV_ANCH


def draw(rws, cen, scr, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    frags = ["sdcp_neutral", "ptfe_c10"]
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.3),
                             gridspec_kw={"width_ratios": [1.0, 1.0, 0.9]})
    # 두 조각을 **같은 x 범위**로 그린다 — 최단 접촉의 차이가 눈에 보여야 한다
    allx = [r["anchor_distance_A"] for r in rws]
    xlo, xhi = min(allx) - 0.09, max(allx) + 0.09
    x_prim = next(r["anchor_distance_A"] for r in rws
                  if r["fragment"] == "sdcp_neutral" and r["role_in_c12"] == "primary")
    for ax, frag in zip(axes[:2], frags):
        sub = [r for r in rws if r["fragment"] == frag]
        ax.axvline(x_prim, color=MUT, lw=0.9, ls=":", zorder=0)
        for r in sub:
            ax.scatter(r["anchor_distance_A"], r["height_A"],
                       marker=MOL_MARKER.get(r["anchor_mol_element"], "o"),
                       s=36, alpha=0.65, linewidths=0.7, facecolor="none",
                       edgecolor=SURF_COLOR.get(r["anchor_surface_element"], MUT))
        for r in sub:
            if not r["role_in_c12"]:
                continue
            prim = r["role_in_c12"] == "primary"
            ax.scatter(r["anchor_distance_A"], r["height_A"], s=190 if prim else 140,
                       marker="o", facecolor="none", edgecolor=INK,
                       linewidths=2.1 if prim else 1.2, zorder=5)
            ax.annotate("%s  %s\n%s···%s %.2f Å"
                        % (r["basin_id"],
                           "DFT primary" if prim else r["role_in_c12"].replace("_", " "),
                           r["anchor_mol_element"], r["anchor_surface_element"],
                           r["anchor_distance_A"]),
                        (r["anchor_distance_A"], r["height_A"]),
                        textcoords="offset points", xytext=(9, 9),
                        fontsize=8.5, color=INK,
                        fontweight="bold" if prim else "normal")
        fs = scr["fragments"][frag]
        apply_axes(ax, "Closest anchor contact (Å)", "Height above surface (Å)",
                   FRAG_TITLE.get(frag, frag), fontsize=11)
        ax.set_xlim(xlo, xhi)
        # 주석과 겹치지 않는 빈 구석에 놓는다 (조각마다 데이터 분포가 다르다)
        _tx, _ty, _ha, _va = ((0.98, 0.97, "right", "top") if frag == "sdcp_neutral"
                              else (0.02, 0.97, "left", "top"))  # 조각별 빈 구석
        ax.text(_tx, _ty, "%d basins\n(%d poses, %d gated)"
                % (len(fs["basins"]), fs["n_poses_passed"], fs["n_gated"]),
                transform=ax.transAxes, va=_va, ha=_ha, fontsize=8.5, color=MUT)

    ax = axes[2]
    labels, vals, cols = [], [], []
    for frag in frags:
        for (m, s), n in sorted(cen[frag].items(), key=lambda kv: -kv[1]):
            labels.append("%s···%s" % (m, s))
            vals.append(n)
            cols.append(SURF_COLOR.get(s, MUT))
    ypos = list(range(len(labels)))[::-1]
    ax.barh(ypos, vals, color=cols, alpha=0.85, height=0.7)
    ax.set_yticks(ypos)
    ax.set_yticklabels(labels, fontsize=9.5)
    for y, v in zip(ypos, vals):
        ax.text(v + 1.2, y, str(v), va="center", fontsize=8.5, color=MUT)
    nsd = len(cen["sdcp_neutral"])
    ax.axhline(ypos[nsd - 1] - 0.5, color=MUT, lw=0.9, ls=":")
    xr = max(vals) * 1.38
    ax.text(xr * 0.97, ypos[0], "SDCP", ha="right", va="center",
            fontsize=10, color=INK, fontweight="bold")
    ax.text(xr * 0.97, ypos[nsd], "PTFE", ha="right", va="center",
            fontsize=10, color=INK, fontweight="bold")
    apply_axes(ax, "Basins with this anchor contact", None,
               "Anchor contact census", fontsize=11)
    ax.set_xlim(0, xr)

    hm = [Line2D([], [], marker=MOL_MARKER[e], color=MUT, ls="none",
                 markerfacecolor="none", label="%s (molecule)" % e)
          for e in ("H", "O", "F") if any(r["anchor_mol_element"] == e for r in rws)]
    hs = [Line2D([], [], marker="o", color=SURF_COLOR[e], ls="none",
                 markerfacecolor="none", label="%s (surface)" % e)
          for e in ("Li", "O", "Ni")]
    axes[0].legend(handles=hm + hs, fontsize=8, frameon=False,
                   loc="upper left", bbox_to_anchor=(-0.02, 1.02), ncol=1,
                   handletextpad=0.4, columnspacing=1.0)

    fig.text(0.005, 0.055,
             "Rigid single-point screen on LiNiO$_2$(104): 7 adsorption sites × 4 "
             "in-plane rolls × Fibonacci orientations, two freeze settings. Poses were "
             "clustered into basins by contact fingerprint and RMSD; the pose taken "
             "forward to DFT was fixed by a written rule",
             fontsize=7.8, color=MUT, ha="left", va="bottom")
    fig.text(0.005, 0.012,
             "before any DFT result was seen. Dotted vertical line marks the shortest "
             "anchor contact found anywhere in the screen (SDCP, 1.83 Å). Screening "
             "energies are not shown — they are not binding energies.",
             fontsize=7.8, color=MUT, ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.085, 1, 1))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=300)
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

    scr, roles = load()
    chk(roles.get("sdcp_neutral", {}).get("b00") == "primary",
        "프로토콜의 sdcp primary(b00)가 스크린에 있고 역할이 붙는다")
    chk(roles.get("ptfe_c10", {}).get("b00") == "primary",
        "프로토콜의 ptfe primary(b00)가 스크린에 있고 역할이 붙는다")
    chk(roles.get("sdcp_neutral", {}).get("b12") == "stress_sensitivity",
        "sdcp 대안 자세는 `stress_sensitivity` 다 (ΔE_pose 0.278 > W0 0.15)")

    rws = rows(scr, roles)
    chk(len(rws) == 101 + 96, "basin 197개를 전부 행으로 낸다 (101 + 96)")
    chk(all(r["anchor_mol_element"] and r["anchor_surface_element"] for r in rws),
        "모든 basin 에 앵커 원소쌍이 있다")
    cen = census(rws)
    chk(cen["ptfe_c10"] and all(m == "F" for (m, _s) in cen["ptfe_c10"]),
        "PTFE 는 전 basin 이 F 앵커다 (조각에 H·O 가 없다)")
    chk(sum(cen["sdcp_neutral"].values()) == 101, "census 합이 basin 수와 같다")

    # ⛔음성 ①: 프로토콜이 스크린에 없는 basin 을 가리키면 그리지 않는다
    import tempfile
    T = Path(tempfile.mkdtemp())
    for sub in ("db/properties", "tools/figures"):
        (T / sub).mkdir(parents=True, exist_ok=True)
    (T / "tools/figures/house_style.py").write_text(
        (REPO / "tools/figures/house_style.py").read_text(encoding="utf-8"), encoding="utf-8")
    (T / SCREEN).write_text(json.dumps(scr, ensure_ascii=False), encoding="utf-8")
    pro = json.loads((REPO / PROTOCOL).read_text(encoding="utf-8"))
    pro["2_자세_동결"]["fragments"]["sdcp_neutral"]["primary"]["basin_id"] = "b99"
    (T / PROTOCOL).write_text(json.dumps(pro, ensure_ascii=False), encoding="utf-8")
    try:
        load(T)
        chk(False, "⛔음성: 없는 basin 을 가리키면 SystemExit 여야 한다")
    except SystemExit as e:
        chk("b99" in str(e), "⛔음성: 프로토콜이 스크린에 없는 basin 을 가리키면 막는다")

    # ⛔음성 ②: rep_label 이 달라지면(자세 파일이 갈리면) 막는다
    pro = json.loads((REPO / PROTOCOL).read_text(encoding="utf-8"))
    pro["2_자세_동결"]["fragments"]["ptfe_c10"]["primary"]["rep_label"] = "somewhere_else"
    (T / PROTOCOL).write_text(json.dumps(pro, ensure_ascii=False), encoding="utf-8")
    try:
        load(T)
        chk(False, "⛔음성: rep_label 이 달라도 통과하면 안 된다")
    except SystemExit as e:
        chk("rep_label" in str(e), "⛔음성: rep_label 이 갈리면 막는다 (자세 파일 계보)")

    # ⛔음성 ③: anchor 가 달라지면 막는다 — 기하가 바뀐 채로 같은 그림을 그리지 않는다
    pro = json.loads((REPO / PROTOCOL).read_text(encoding="utf-8"))
    pro["2_자세_동결"]["fragments"]["sdcp_neutral"]["primary"]["anchor"] = ["O", "Li", 2.0]
    (T / PROTOCOL).write_text(json.dumps(pro, ensure_ascii=False), encoding="utf-8")
    try:
        load(T)
        chk(False, "⛔음성: anchor 가 달라도 통과하면 안 된다")
    except SystemExit as e:
        chk("anchor" in str(e), "⛔음성: anchor 원소쌍·거리가 갈리면 막는다")

    # ⛔음성 ④: 에너지를 축으로 쓰지 않는다 — **그리는 함수**에 E_pose·eV 가 없어야 한다
    src = Path(__file__).read_text(encoding="utf-8")
    _draw = src.split("\ndef draw(")[1].split("\ndef selftest(")[0]
    chk("E_pose" not in _draw,
        "⛔음성: draw() 가 `E_pose` 를 쓰지 않는다 (do_not_cite 를 축으로 못 올린다)")
    chk("eV" not in _draw, "⛔음성: draw() 안에 eV 축·주석이 없다")
    # ⛔음성 ⑤: CSV 에도 E_pose 열을 만들지 않는다 (Origin 에서 그리면 같은 위반이다)
    chk(all("E_pose" not in k and "energy" not in k.lower() for k in rws[0]),
        "⛔음성: Origin-ready CSV 에 에너지 열이 없다 — 우리 쪽에서 안 그려도 못 그리게 한다")
    # ⛔음성 ⑥: 역할을 JSON 키가 아니라 **규칙**으로 계산한다 (회신 BC P0-4)
    _load = src.split("\ndef load(")[1].split("\ndef rows(")[0]
    chk("dE_pose_eV" in _load and "W0" in _load,
        "역할은 ΔE_pose ≤ W0 규칙으로 계산한다 (자세 파일의 JSON 키가 아니다)")
    _pro = json.loads((REPO / PROTOCOL).read_text(encoding="utf-8"))
    _pro.pop("⛔_자세_역할_규칙_2026_09_02", None)
    (T / PROTOCOL).write_text(json.dumps(_pro, ensure_ascii=False), encoding="utf-8")
    (T / SCREEN).write_text(json.dumps(scr, ensure_ascii=False), encoding="utf-8")
    try:
        load(T)
        chk(False, "⛔음성: 역할 규칙이 없어도 그리면 안 된다")
    except SystemExit as e:
        chk("W0" in str(e), "⛔음성: 프로토콜에 역할 규칙(W0)이 없으면 그리지 않는다")

    print("selftest: %d 통과 / %d 실패" % (ok, bad))
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="figures/fig_c12_pose_screen.png")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    scr, roles = load()
    rws = rows(scr, roles)
    cen = census(rws)
    g, c = write_csv(rws, cen)
    out = draw(rws, cen, scr, os.path.join(str(REPO), a.out)
               if not os.path.isabs(a.out) else a.out)
    print("→ %s" % out)
    print("→ %s  (%d rows)" % (g, len(rws)))
    print("→ %s" % c)
    for frag in ("sdcp_neutral", "ptfe_c10"):
        top = sorted(cen[frag].items(), key=lambda kv: -kv[1])
        print("   %-14s %s" % (frag, " · ".join("%s···%s %d" % (m, s, n)
                                                for (m, s), n in top)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
