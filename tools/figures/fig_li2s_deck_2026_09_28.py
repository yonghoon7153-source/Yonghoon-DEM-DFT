#!/usr/bin/env python3
"""li2s 발표 덱(2026-09-28)용 그림 8 장 — 처음 보는 사람용 · 영어 라벨 · 하우스 스타일 · CSV 동시 출력.

    python3 tools/figures/fig_li2s_deck_2026_09_28.py            # 그림 + CSV
    python3 tools/figures/fig_li2s_deck_2026_09_28.py --selftest # 양성 + 음성

그림 (docs/figures/li2s_deck_2026_09_28/):
  f1_quench_protocol    담금질 온도 프로그램 (seed5 런의 설정·순간 온도) + Tg 띠
  f2_force_check        UMA vs QE-PBE 힘 RMSE 원소별 (120 원자 · 10 프레임)
  f3_neb_endpoints      NEB 가지: MD 변위 vs 0 K 이완 끝점 사이 변위 (lag 5 ps 8 건 · lag 1–4 ps 18 건)
  f4_temperature_window 담금질 램프 진단 — 움직인 Li 비율 · p90 변위 vs 반 상자 길이
  f5_pilot_beta         예비 런 3 개의 MSD 지수 β (다중 시간원점) vs 확산영역 기준 0.8–1.2
  f6_pcoord_stages      다섯 담금질 구조 — 단계별 '4 배위가 아닌 P 가 있는 프레임' 비율
  f7_identity_census    다섯 담금질 구조 — 4 배위 P 수 vs 원래 S 넷을 그대로 가진 P 수
  f8_s54_event          seed5 — S54 이탈과 말단 P–S–S 형성 시간선

원자료는 전부 repo 안에 있다 (아래 SRC). 재사용: fig_weekly_2026_09_27.load_pcoord / load_beta.

⛔ 이 도구가 못 하는 것:
  - D · σ · Ea 의 **값**을 그리지 않는다 (카드 §1c · 1저자 인용정책 2026-09-18). 그 경로를 막는
    가드(_guard_text)는 그림 글자를 **문자열로** 볼 뿐이다 — 숫자를 다른 단위로 적으면 못 잡는다.
  - 판정을 새로 내리지 않는다 — 원장 기록의 값을 옮겨 그린다. β 는 내부 진단(citable false)이라
    그림에 'provisional' 을 박는다.
  - f4 는 **비평형 담금질 램프**(seed1)의 진단이다 — 평형 MSD 가 아니다. 온도 선택 근거로만 쓴다.
  - f8 은 거리 기준(P–S < 2.6 Å · S–S < 2.3 Å) 이다 — 결합 차수·속도·일반화를 말하지 않는다.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys

R = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "tools/figures"))
import house_style as H  # noqa: E402
from fig_weekly_2026_09_27 import load_beta, load_pcoord, _plt  # noqa: E402  (재사용)

DB = R / "db/properties"
RAW = R / "db/raw/lpscl_smallcell_glass_cc_2026_09_26"
OUT = R / "docs/figures/li2s_deck_2026_09_28"
TAG = "li2s_deck_2026_09_28"

SRC = {
    "trace": RAW / "seed5_ss_event_cc.json",
    "census": RAW / "census_5seeds_2026_09_28.json",
    "gb3": DB / "lpscl_smallcell_gb3_result_2026_09_18.json",
    "neb1": DB / "lpscl_smallcell_neb_raw/endpoint_coupled_gate.json",
    "neb2": DB / "lpscl_smallcell_shortlag_raw/union_v2/endpoint_coupled_gate.json",
    "scan": DB / "lpscl_smallcell_quench_scan_2026_09_21.json",
    "follow": DB / "lpscl_smallcell_glass_md_cc_followup_2026_09_26.json",
    "pcoord_csv": DB / "li2s_p_coord_frames_origin_2026_09_27.csv",
}
L_BOX = 13.9827          # Å, 카드 §1b
HALF_BOX = L_BOX / 2      # 6.99 Å — 무상관 한계 (L/2)² = 48.88 Å²
TG_BAND = (400, 450)      # K, 담금질 스캔 판독 (10¹² K/s 의 동역학적 정지 온도 — 실험 Tg 아님)
MD_T = (400, 465, 550)    # K, 카드 §1b
EVENTS = ((109, "1"), (278, "2"), (369, "3"), (388, "4"))  # s54_history 사건_순서_실측
BAR = "#475569"           # 단일 계열 막대 (크기 비교 — 범주색 불필요)
SERIES2 = (H.ELEM["Li"], H.ELEM["P"])  # 두 계열 — validate_palette.js 통과 (ΔE 21.0 deutan · 30.2 normal)
BAND = "#e5e7eb"

#: 그림 글자에 나오면 안 되는 것 — 수송 **값**의 단위·기호 (값 인용 금지 경로를 막는다)
FORBIDDEN = (r"cm\s*(\^?2|²|\$\^\{?2\}?\$)\s*/\s*s", r"\bS\s*/\s*cm\b", r"mS\s*/\s*cm",
             r"\bE_?a\s*=", r"\bD\s*=\s*\d", r"σ\s*=\s*\d")


# ────────────────────────────────────────────────────────────── 적재 (검증 포함)
def _j(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def load_trace(p=SRC["trace"]) -> dict:
    d = _j(p)
    rows = d["rows"]
    if len(rows) != d["n_frames"]:
        raise ValueError(f"trace: rows {len(rows)} ≠ n_frames {d['n_frames']}")
    t = [r["t_ps"] for r in rows]
    if any(b <= a for a, b in zip(t, t[1:])):
        raise ValueError("trace: 시간이 단조 증가하지 않는다")
    n4 = []
    for r in rows:
        h = r["P_S_coord_hist"]
        if sum(h.values()) != 12:
            raise ValueError(f"trace t={r['t_ps']}: P 가 12 개가 아니다 {h}")
        n4.append(h.get("4", 0))
    on = d["onset"]
    return {"t": t, "Tset": [r["T_set_K"] for r in rows], "Tinst": [r["T_K"] for r in rows],
            "n4": n4, "ssmin": [r["ss_min_A"] for r in rows], "kind": [r["ss_kind"] for r in rows],
            "onset_t": on["t_ps"], "onset_d": on["d_A"], "cut": d["ss_cut_A"], "rps": d["R_PS_A"],
            "last_d": d["persistence"]["last_frame_pair_d_A"]}


def load_census(p=SRC["census"], follow=SRC["follow"]) -> dict:
    d = _j(p)
    rows = d["다섯_시드_표_설계_기준"]
    if [r["seed"] for r in rows] != [1, 2, 3, 4, 5]:
        raise ValueError("census: 시드 1–5 순서가 아니다")
    b3 = _j(follow)
    b3 = b3[[k for k in b3 if k.startswith("B3")][0]]["표"]
    out = []
    for r in rows:
        m = re.fullmatch(r"(\d+)/(\d+)", r["정체_온전_P"])
        if not m or int(m[2]) != 12 or not 0 <= int(m[1]) <= 12:
            raise ValueError(f"census seed{r['seed']}: 정체 온전 '{r['정체_온전_P']}' 형식 오류")
        ps4 = float(str(r["배위_PS4_게이트_relax"]).split()[0])
        g = b3[f"seed{r['seed']}"]
        if abs(g["PS4"] - ps4) > 1e-4:
            raise ValueError(f"census seed{r['seed']}: PS4 {ps4} ≠ 게이트 A 표 {g['PS4']}")
        out.append({"seed": r["seed"], "keep4": int(m[1]), "coord4": round(ps4 * 12),
                    "s_left": int(r["주인을_떠난_S"]), "rho": g["rho"]})
    return {"rows": out}


def load_gb3(p=SRC["gb3"]) -> dict:
    d = _j(p)
    tab = d[[k for k in d if "원소별" in k][0]]["표"]
    els = ("S", "P", "Cl", "Li")
    rows = [{"el": e, **tab[e]} for e in els]
    n = sum(r["n_atoms"] for r in rows)
    tot = (sum(r["rmse_eVA"] ** 2 * r["n_atoms"] for r in rows) / n) ** 0.5
    if abs(tot - 0.0390) > 0.0015:   # 원소별 RMSE 를 원자수로 합치면 총 RMSE 로 돌아와야 한다
        raise ValueError(f"gb3: 원소별에서 되짚은 총 RMSE {tot:.4f} ≠ 0.0390")
    return {"rows": rows, "total": 0.0390, "e_mae_meV": 0.55}


def load_neb(p1=SRC["neb1"], p2=SRC["neb2"]) -> dict:
    out = []
    for lab, lag, p in (("lag 5 ps", "5", p1), ("lag 1-4 ps", "1-4", p2)):
        d = _j(p)
        for r in d["rows"]:
            if r["status"] == "duplicate_raw_pair":
                continue
            if r["status"] != "coupled_endpoint_failed" and r["li_disp_A"] < r["thresh_A"]:
                raise ValueError(f"neb {r['tag']}: 문턱 아래인데 status {r['status']}")
            if r["status"] == "coupled_endpoint_failed" and r["li_disp_A"] >= r["thresh_A"]:
                raise ValueError(f"neb {r['tag']}: 문턱 위({r['li_disp_A']})인데 실패로 적혀 있다")
            out.append({"round": lab, "lag_ps": lag, "tag": r["tag"], "md": r["hop_A_from_events"],
                        "relaxed": r["li_disp_A"], "rmsd": r["nonli_rmsd_A"], "thresh": r["thresh_A"]})
    return {"rows": out}


def load_scan(p=SRC["scan"]) -> dict:
    d = _j(p)["2_실측"]["표"]
    rows = []
    for r in d:
        a, b = r["T_set_K"]
        rows.append({"t0": r["t_from_ps"], "t1": r["t_to_ps"], "Ta": a, "Tb": b, "Tm": (a + b) / 2,
                     "moved": r["n_moved"], "nLi": r["n_Li"], **{k: r["per_ion_max_A"][k]
                                                                 for k in ("max", "median", "p90")}})
    if any(r["nLi"] != 48 for r in rows):
        raise ValueError("scan: n_Li ≠ 48")
    return {"rows": rows}


# ────────────────────────────────────────────────────────────── 가드
def _guard_text(texts) -> None:
    for s in texts:
        for pat in FORBIDDEN:
            if re.search(pat, s):
                raise ValueError(f"그림 글자에 수송값 표기가 있다: {s!r} (패턴 {pat})")


def _save(fig, name: str) -> str:
    texts = [t.get_text() for t in fig.findobj(lambda o: hasattr(o, "get_text"))]
    _guard_text(texts)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{name}.png"
    fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)
    return str(p.relative_to(R))


def _note(fig, s, y=-0.02):
    import textwrap
    width = int(fig.get_size_inches()[0] * 14.5)     # 9.5 pt 글자 ≈ 인치당 14–15 자
    fig.text(0.01, y, textwrap.fill(s, width), fontsize=9.5, color=H.MUT, ha="left", va="top",
             linespacing=1.35)


def _r3(x) -> str:
    """세 자리 반올림(사사오입) — 0.4195 가 이진 표현 탓에 0.419 로 찍히지 않게 (기록은 0.420)."""
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(str(x)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def _signed(x, nd=1) -> str:
    return f"{x:+.{nd}f}".replace("-", "−")


def _csv(name: str, header, rows) -> str:
    p = DB / f"{TAG}_{name}.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return str(p.relative_to(R))


# ────────────────────────────────────────────────────────────── 그림
def f1(tr):
    plt = _plt()
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    ax.axhspan(*TG_BAND, color=BAND, zorder=0, lw=0)
    ax.plot(tr["t"], tr["Tinst"], color="#9ca3af", lw=0.7, label="instantaneous T (one run)")
    ax.plot(tr["t"], tr["Tset"], color=H.INK, lw=2.2, label="set point")
    ax.text(75, 800, "melt\n1200 K\n100 ps", ha="center", va="center", fontsize=11, color=H.INK)
    ax.text(1040, 1040, "linear quench · 900 ps\n1 K/ps (10$^{12}$ K/s)", ha="right", va="center",
            fontsize=11, color=H.INK)
    ax.text(1045, 215, "hold 300 K · 50 ps", ha="right", va="center", fontsize=11, color=H.INK)
    ax.text(30, 425, "kinetic arrest at this quench rate: T$_g$ ≈ 400–450 K", va="center",
            fontsize=10.5, color=H.INK)
    ax.set_xlim(0, 1050)
    ax.set_ylim(170, 1330)
    H.apply_axes(ax, "time (ps)", "temperature (K)")
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 0.0), frameon=False, fontsize=10)
    _note(fig, "NPT at 0 GPa · UMA (uma-s-1p1) · 120 atoms · then 0 K relaxation. "
               "Five independent quenches (different random packings).", y=-0.04)
    rows = list(zip(tr["t"], tr["Tset"], tr["Tinst"]))
    return _save(fig, "f1_quench_protocol"), _csv("f1_quench_protocol",
                                                  ["t_ps", "T_set_K", "T_instantaneous_K_seed5_run"], rows)


def f2(g):
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    xs = range(len(g["rows"]))
    ys = [r["rmse_eVA"] for r in g["rows"]]
    ax.bar(xs, ys, width=0.56, color=BAR, zorder=2)
    for x, y in zip(xs, ys):
        ax.text(x, y + 0.0012, f"{y:.3f}", ha="center", va="bottom", fontsize=11, color=H.INK)
    ax.axhline(g["total"], color=H.INK, ls="--", lw=1.3, zorder=3)
    ax.text(3.42, g["total"] + 0.0012, f"all atoms  {g['total']:.3f}", ha="right", va="bottom",
            fontsize=10.5, color=H.INK)
    ax.set_xticks(list(xs), [f"{r['el']}\n({r['n_atoms']} forces)" for r in g["rows"]], fontsize=11)
    ax.set_ylim(0, 0.068)
    H.apply_axes(ax, None, "force RMSE vs DFT (eV/Å)")
    ax.grid(axis="y", color="#eef0f3", zorder=0)
    _note(fig, f"UMA vs QE-PBE on 10 frames of one 120-atom glass · relative-energy MAE "
               f"{g['e_mae_meV']:.2f} meV/atom. S and P carry larger errors than Li and Cl.", y=-0.1)
    rows = [[r["el"], r["n_atoms"], r["rmse_eVA"], r["mae_eVA"], r["rms_ref_eVA"], r["rel_mae_pct"],
             r["softening_slope"]] for r in g["rows"]]
    return _save(fig, "f2_force_check"), _csv(
        "f2_force_check", ["element", "n_atom_forces", "force_rmse_eV_per_A", "force_mae_eV_per_A",
                           "rms_dft_force_eV_per_A", "relative_mae_percent", "force_softening_slope"], rows)


def f3(nb):
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    th = nb["rows"][0]["thresh"]
    ax.axhspan(th, 3.3, color="#f1f5f9", zorder=0, lw=0)
    ax.axhline(th, color=H.INK, ls="--", lw=1.2)
    ax.plot([1.9, 3.3], [1.9, 3.3], color="#cbd5e1", ls=":", lw=1.2)
    ax.text(3.25, 3.13, "no relaxation back", ha="right", fontsize=9.5, color=H.MUT, rotation=0)
    ax.text(1.95, th + 0.85, "needed for a barrier calculation:\nendpoints at least 2.0 Å apart",
            fontsize=10.5, color=H.INK, va="center")
    for (lab, mk, col) in (("lag 5 ps", "o", SERIES2[0]), ("lag 1-4 ps", "^", SERIES2[1])):
        rr = [r for r in nb["rows"] if r["round"] == lab]
        ax.scatter([r["md"] for r in rr], [r["relaxed"] for r in rr], marker=mk, s=58, color=col,
                   edgecolor="white", linewidth=1.0, zorder=3,
                   label=f"{lab.replace('-', '–')}  ({len(rr)} events)")
    n_ok = sum(r["relaxed"] >= r["thresh"] for r in nb["rows"])
    ax.text(1.95, th + 0.3, f"{n_ok} of {len(nb['rows'])} events reach this region", ha="left",
            fontsize=11, color=H.INK, fontweight="bold")
    ax.set_xlim(1.9, 3.3)
    ax.set_ylim(0, 3.3)
    H.apply_axes(ax, "Li displacement seen in MD over the lag (Å)",
                 "Li displacement between\nrelaxed endpoints (Å)")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.02), frameon=False, fontsize=10)
    _note(fig, "Glass seed 1 at 300 K, window 1000–1050 ps. Each event: relax start → move that Li → "
               "relax again. No barrier (Eb) is defined on these events.", y=-0.03)
    rows = [[r["round"], r["lag_ps"], r["tag"], round(r["md"], 4), r["relaxed"], r["rmsd"], r["thresh"]]
            for r in nb["rows"]]
    return _save(fig, "f3_neb_endpoints"), _csv(
        "f3_neb_endpoints", ["round", "lag_ps", "event", "li_disp_md_A", "li_disp_relaxed_endpoints_A",
                             "framework_rmsd_A", "threshold_A"], rows)


def f4(sc):
    plt = _plt()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.0, 5.2), sharex=True,
                                 gridspec_kw={"hspace": 0.12})
    rows = sc["rows"]
    Tm = [r["Tm"] for r in rows]
    xerr = [[r["Tm"] - min(r["Ta"], r["Tb"]) for r in rows], [max(r["Ta"], r["Tb"]) - r["Tm"] for r in rows]]
    for ax in (a1, a2):
        ax.axvspan(*TG_BAND, color=BAND, zorder=0, lw=0)
        for T in MD_T:
            ax.axvline(T, color=H.INK, ls=":", lw=1.1, zorder=1)
    a1.errorbar(Tm, [100 * r["moved"] / r["nLi"] for r in rows], xerr=xerr, fmt="o", ms=5,
                color=H.ELEM["Li"], ecolor="#99d5cf", elinewidth=1.2, capsize=0, zorder=3)
    a1.set_ylim(0, 108)
    H.apply_axes(a1, None, "Li that moved > 2 Å\nwithin 5 ps (%)")
    a1.text(1210, 114, "dotted lines: MD temperatures 400 · 465 · 550 K", ha="right", fontsize=10,
            color=H.INK)
    a1.text(sum(TG_BAND) / 2, 33, "T$_g$ ≈ 400–450 K", ha="center", va="center", rotation=90,
            fontsize=9.5, color=H.INK)
    a2.errorbar(Tm, [r["p90"] for r in rows], xerr=xerr, fmt="o", ms=5, color=H.ELEM["Li"],
                ecolor="#99d5cf", elinewidth=1.2, capsize=0, zorder=3)
    a2.axhline(HALF_BOX, color=H.INK, ls="--", lw=1.2)
    a2.text(1195, HALF_BOX + 0.4, f"half box length  L/2 = {HALF_BOX:.2f} Å", ha="right",
            fontsize=10, color=H.INK)
    a2.text(1195, 2.2, "above ≈ 575 K a Li can cross half the box in 5 ps\n→ periodic-image limit, "
                       "so 600 K and above are not used", ha="right", fontsize=9.5, color=H.MUT)
    a2.set_ylim(0, 18)
    a2.set_xlim(280, 1220)
    H.apply_axes(a2, "set temperature during the quench (K)",
                 "90th-percentile Li\ndisplacement in 5 ps (Å)")
    _note(fig, "Diagnostic from one non-equilibrium quench ramp (seed 1), used only to choose the MD "
               "temperatures. Horizontal bars = temperature range covered by each 50 ps window. "
               "Not a diffusion coefficient.", y=0.0)
    out_rows = [[r["t0"], r["t1"], r["Ta"], r["Tb"], r["Tm"], r["moved"], r["nLi"], r["p90"], r["median"],
                 r["max"]] for r in rows]
    return _save(fig, "f4_temperature_window"), _csv(
        "f4_temperature_window", ["t_from_ps", "t_to_ps", "T_set_start_K", "T_set_end_K", "T_set_mid_K",
                                  "n_Li_moved_over_2A_in_5ps", "n_Li", "p90_disp_5ps_A",
                                  "median_disp_5ps_A", "max_disp_5ps_A"], out_rows)


START = {"P-2_550K_MTO": "as-quenched start", "P-1_400K_400ps_MTO": "as-quenched start",
         "pilot800_400K_MTO": "relaxed start"}


def f5(be):
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    lo, hi = be["band"]
    ax.axhspan(lo, hi, color="#e8eef5", zorder=0, lw=0)
    ax.text(2.45, 1.17, f"diffusive regime  {lo} ≤ β ≤ {hi}", ha="right", va="top", fontsize=10.5,
            color=H.INK)
    for i, r in enumerate(be["runs"]):
        filled = START[r["key"]].startswith("as-")
        ax.errorbar(i, r["beta"], yerr=2 * r["sigma"], fmt="o", ms=9, color=H.INK,
                    mfc=H.INK if filled else "white", mew=1.6, elinewidth=1.4, capsize=4, zorder=3)
        side = "inside band" if lo <= r["beta"] <= hi else "below band"
        ax.text(i, r["beta"] + 2 * r["sigma"] + 0.02, f"β = {_r3(r['beta'])}\n{_signed(r['dos'])}σ · {side}",
                ha="center", va="bottom", fontsize=10.5, color=H.INK, linespacing=1.3)
    ax.set_xticks([0, 1, 2], [f"{r['T']} K · {r['ps']} ps\n{START[r['key']]}" for r in be["runs"]],
                  fontsize=10.5)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(0.3, 1.25)
    H.apply_axes(ax, None, "MSD exponent β\n(d ln MSD / d ln t, 2–50 ps)")
    _note(fig, "Pilot runs on quench seed 1 · multiple-time-origin MSD · bars = ±2σ, σ from block "
               "bootstrap (a lower bound); '+3.4σ' = distance from the 0.8 edge in units of σ · "
               "provisional internal diagnostic.", y=-0.06)
    rows = [[r["key"], r["T"], r["ps"], START[r["key"]], r["beta"], r["sigma"], r["dos"], lo, hi]
            for r in be["runs"]]
    return _save(fig, "f5_pilot_beta"), _csv(
        "f5_pilot_beta", ["run", "T_K", "production_ps", "start_structure", "beta_mto",
                          "sigma_lower_bound", "distance_from_lower_edge_in_sigma", "band_lo", "band_hi"], rows)


def f6(pc):
    plt = _plt()
    stages = (("melt_hold", "melt hold · 1200 K"), ("quench", "quench · 1200 → 300 K"),
              ("final_hold", "final hold · 300 K"))
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.5), sharey=True, gridspec_kw={"wspace": 0.08})
    seeds = pc["seeds"]
    for ax, (st, title) in zip(axes, stages):
        vals = [pc["frames"][s][st] for s in seeds]
        pct = [100 * n / N for n, N in vals]
        xs = range(1, len(seeds) + 1)
        ax.bar(xs, pct, width=0.6, color=BAR, zorder=2)
        for x, (n, N), p in zip(xs, vals, pct):
            ax.text(x, p + 2, f"{n}", ha="center", va="bottom", fontsize=10, color=H.INK)
        N = vals[0][1]
        ax.set_title(f"{title}\n({N} frames)", fontsize=11, color=H.INK)
        ax.set_xticks(list(xs), [str(x) for x in xs], fontsize=10.5)
        ax.set_ylim(0, 112)
        H.apply_axes(ax, "quench seed")
    axes[0].set_ylabel("frames with ≥ 1 P not bonded\nto four S (% of frames)", fontsize=11,
                       color=H.INK)
    axes[2].annotate("one P stays\n3-coordinated", xy=(4.75, 96), xytext=(2.6, 62), ha="center",
                     va="center", fontsize=10, color=H.INK,
                     arrowprops={"arrowstyle": "->", "color": H.MUT, "lw": 1.0})
    _note(fig, "Numbers above bars = frame counts. P–S neighbour cut 2.6 Å (distance criterion). "
               "Frames saved every 1 ps.", y=-0.06)
    return _save(fig, "f6_pcoord_stages"), str(SRC["pcoord_csv"].relative_to(R))


def f7(cs):
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.8, 3.9))
    rows = cs["rows"]
    xs = [r["seed"] for r in rows]
    w = 0.36
    b1 = ax.bar([x - w / 2 for x in xs], [r["coord4"] for r in rows], width=w, color=SERIES2[0],
                zorder=2, label="P bonded to four S (after relaxation)")
    b2 = ax.bar([x + w / 2 for x in xs], [r["keep4"] for r in rows], width=w, color=SERIES2[1],
                zorder=2, label="P still bonded to its original four S")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.15, f"{int(b.get_height())}",
                    ha="center", va="bottom", fontsize=10, color=H.INK)
    ax.set_xticks(xs, [f"seed {r['seed']}\n{r['s_left']} S moved" for r in rows], fontsize=10.5)
    ax.set_ylim(0, 15.2)
    ax.set_yticks([0, 3, 6, 9, 12])
    H.apply_axes(ax, None, "P atoms (of 12)")
    ax.set_ylim(0, 13.4)
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), frameon=False, fontsize=10, ncol=1)
    _note(fig, "Identity tracked by atom index from the first frame · 'S moved' = S atoms that left "
               "their original P during melt/quench · distance criterion P–S < 2.6 Å.", y=-0.06)
    out = [[r["seed"], r["coord4"], r["keep4"], 12, r["s_left"], r["rho"]] for r in rows]
    return _save(fig, "f7_identity_census"), _csv(
        "f7_identity_census", ["quench_seed", "P_bonded_to_4S_after_relax", "P_keeping_original_4S", "n_P",
                               "S_left_original_P", "density_g_cm3_after_relax"], out)


def f8(tr):
    plt = _plt()
    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(7.4, 5.8), sharex=True,
                                     gridspec_kw={"hspace": 0.1, "height_ratios": [1, 0.8, 1.1]})
    t = tr["t"]
    a1.plot(t, tr["Tinst"], color="#9ca3af", lw=0.6)
    a1.plot(t, tr["Tset"], color=H.INK, lw=1.8)
    a1.set_ylim(250, 1300)
    H.apply_axes(a1, None, "T (K)")
    a2.step(t, tr["n4"], where="post", color=BAR, lw=1.3)
    a2.set_ylim(9.6, 12.4)
    a2.set_yticks([10, 11, 12])
    H.apply_axes(a2, None, "P bonded to\nfour S (of 12)")
    a3.plot(t, tr["ssmin"], color=H.ELEM["S"], lw=0.8)
    a3.axhline(tr["cut"], color=H.INK, ls="--", lw=1.1)
    a3.text(1045, tr["cut"] + 0.04, f"S–S cut {tr['cut']} Å", ha="right", va="bottom", fontsize=9.5,
            color=H.INK)
    a3.text(1045, 2.62, f"{tr['last_d']:.2f} Å at 300 K", ha="right", va="bottom", fontsize=10,
            color=H.INK)
    a3.set_ylim(1.8, 3.4)
    H.apply_axes(a3, "time (ps)", "shortest S–S\ndistance (Å)")
    for ax in (a1, a2, a3):
        for x, lab in EVENTS:
            ax.axvline(x, color=H.MUT, ls=":", lw=1.0)
    for i, (x, lab) in enumerate(EVENTS):
        a1.text(x + (-6 if i == 2 else 6), 1235, lab, ha="right" if i == 2 else "left", fontsize=11,
                color=H.INK, fontweight="bold")
    a1.set_xlim(0, 1050)
    _note(fig, "Quench seed 5. 1: S54 leaves P50 · 2: S59 moves from P55 to P30 · 3: P30 loses a third S "
               "and stays 3-coordinated · 4: S54–S59 at 2.14 Å (terminal P–S–S). Distance criteria only.",
          y=0.02)
    rows = list(zip(t, tr["Tset"], tr["Tinst"], tr["n4"], tr["ssmin"], tr["kind"]))
    return _save(fig, "f8_s54_event"), _csv(
        "f8_s54_event", ["t_ps", "T_set_K", "T_instantaneous_K", "n_P_bonded_to_4S", "shortest_SS_A",
                         "SS_kind"], rows)


def build() -> list:
    tr = load_trace()
    out = [f1(tr), f2(load_gb3()), f3(load_neb()), f4(load_scan()), f5(load_beta()),
           f6(load_pcoord()), f7(load_census()), f8(tr)]
    return out


# ────────────────────────────────────────────────────────────── selftest
def _selftest() -> int:
    import copy
    import tempfile
    ok = bad = 0

    def chk(cond, msg):
        nonlocal ok, bad
        print(("  ✓ " if cond else "  ✗ ") + msg)
        ok += bool(cond)
        bad += not cond

    def raises(fn, msg):
        try:
            fn()
        except ValueError:
            chk(True, msg)
            return
        chk(False, msg + " (안 막혔다)")

    # 양성 — 원장 값 그대로 들어오는가
    cs = load_census()
    chk([r["keep4"] for r in cs["rows"]] == [12, 12, 9, 5, 5], "census: 원래 S 넷 유지 12·12·9·5·5")
    chk([r["coord4"] for r in cs["rows"]] == [12, 12, 12, 12, 11], "census: 4 배위 P 12·12·12·12·11")
    nb = load_neb()
    chk(len(nb["rows"]) == 26 and not any(r["relaxed"] >= r["thresh"] for r in nb["rows"]),
        "neb: 고유 사건 26 (8 + 18) 전부 문턱 아래")
    tr = load_trace()
    chk(tr["onset_t"] == 388.0 and abs(tr["last_d"] - 2.0305) < 1e-4, "trace: onset 388 ps · 마지막 2.03 Å")
    chk(abs(load_gb3()["total"] - 0.039) < 1e-9, "gb3: 원소별 → 총 RMSE 0.039 되짚기")
    sc = load_scan()
    chk(any(abs(r["p90"] - 6.99) < 0.005 for r in sc["rows"]), "scan: 반 상자 6.99 Å 에 닿는 창이 있다")
    # 음성 — 틀린 입력을 잡는가
    raises(lambda: _guard_text(["D = 4.77e-07 cm$^2$/s"]), "가드: D 절대값 표기를 막는다")
    raises(lambda: _guard_text(["Ea = 0.31 eV"]), "가드: Ea 값 표기를 막는다")
    raises(lambda: _guard_text(["σ = 1.2 mS/cm"]), "가드: 전도도 표기를 막는다")
    _guard_text(["β = 0.856", "force RMSE vs DFT (eV/Å)"])
    chk(True, "가드: β·힘 RMSE 표기는 통과시킨다")
    with tempfile.TemporaryDirectory() as td:
        d = json.loads(SRC["census"].read_text(encoding="utf-8"))
        bad_d = copy.deepcopy(d)
        bad_d["다섯_시드_표_설계_기준"][2]["정체_온전_P"] = "13/12"
        p = pathlib.Path(td) / "c.json"
        p.write_text(json.dumps(bad_d, ensure_ascii=False), encoding="utf-8")
        raises(lambda: load_census(p), "census: '13/12' 를 막는다")
        bad_d = copy.deepcopy(d)
        bad_d["다섯_시드_표_설계_기준"][4]["배위_PS4_게이트_relax"] = "1.0000"
        p.write_text(json.dumps(bad_d, ensure_ascii=False), encoding="utf-8")
        raises(lambda: load_census(p), "census: 게이트 A 표와 어긋난 PS4 를 막는다")
        n = json.loads(SRC["neb1"].read_text(encoding="utf-8"))
        n["rows"][0]["li_disp_A"] = 2.5
        q = pathlib.Path(td) / "n.json"
        q.write_text(json.dumps(n), encoding="utf-8")
        raises(lambda: load_neb(q, SRC["neb2"]), "neb: 문턱 위인데 실패로 적힌 행을 막는다")
        t = json.loads(SRC["trace"].read_text(encoding="utf-8"))
        t["rows"][10]["P_S_coord_hist"] = {"4": 11}
        u = pathlib.Path(td) / "t.json"
        u.write_text(json.dumps(t), encoding="utf-8")
        raises(lambda: load_trace(u), "trace: P 가 12 개가 아닌 프레임을 막는다")
        g = json.loads(SRC["gb3"].read_text(encoding="utf-8"))
        k = [k for k in g if "원소별" in k][0]
        g[k]["표"]["S"]["rmse_eVA"] = 0.09
        v = pathlib.Path(td) / "g.json"
        v.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
        raises(lambda: load_gb3(v), "gb3: 총 RMSE 와 안 맞는 원소별 값을 막는다")
    print(f"selftest: {ok} ✓ · {bad} ✗")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    for p in build():
        print(p)
