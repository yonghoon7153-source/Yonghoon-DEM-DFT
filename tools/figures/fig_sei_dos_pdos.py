#!/usr/bin/env python3
"""fig_sei_dos_pdos.py — SEI 분해상 6종의 DOS/PDOS 패널 + 갭 사다리.

무엇을 보여 주나
  SEI 의 임무는 **Li⁺ 통과 · 전자 차단**이다. 그래서 축은 "전자 절연이 되나" 하나다.
  6종 중 **Li₃P 만 0.709 eV** 로 한 자릿수 좁다 — 전자가 새면 전해질 분해가
  자기종결(self-limiting)되지 않는다. 그 대비가 그림의 전부다.

⚠⚠ 데이터 규율
  · 갭은 **fixed-occ nscf 고유값**(db/properties/sei_electronic.json)이다.
    그림의 노란 띠는 그 값으로 그린다 — **DOS 곡선에서 문턱을 읽어 그리지 않는다.**
  · PBE 갭은 넓은 갭 절연체에서 30–50% 과소다. 그림 안에 그 문구를 박아 둔다.
  · Nd 계 3종은 4f 를 원자가에 넣은 PBE 라 갭이 닫힌다 — **이 그림에서 제외**한다.
    (진단이 필요하면 --with-nd 로 별도 파일에 그린다. 인용 금지 표식이 붙는다.)
  · tools/figures/plot_nd_sei_gaps.py 의 숫자는 **MP 소환값**이다(LiCl 6.65 / Li₂S 3.90 …).
    이 그림은 **우리 QE 값**이다. 두 세트를 한 그림·한 표에 섞지 말 것.

  python3 tools/figures/fig_sei_dos_pdos.py
  python3 tools/figures/fig_sei_dos_pdos.py --with-nd     # 진단용 Nd 3종 추가 파일

--raw 판 (2026-11-17 · [혁주] 2a Li₂ZrO₃ 띠틈 — 같은 SEI 체인 · 같은 꼴)
  회수한 QE 작업 폴더 (gap.json · *.dos · *.pdos_atm#*) 를 **바로** 읽는다 — db 갭 표 (sei_electronic.json)
  · sei_dos CSV 를 거치지 않는다. 그 표에 올리는 것은 extract_gap · collect_results 경로이고 여기서 안 한다
  (10-27 CEI 생성물 선례: 값은 카드 · 원자료에만).
    python3 tools/figures/fig_sei_dos_pdos.py --raw <폴더> [<폴더> …] --run_log <run.log> \\
        --out docs/figures/<…>.png --csv <db/properties 안 파일 이름> --title "…"
  · 노란 띠 = gap.json 의 VBM · CBM (fixed-occ nscf 고유값) · 에너지 영점 = 그 VBM.
  · PDOS = pdos_atm 파일의 ldos 열 (그 wfc 기여 합) 을 원소별로 더한다 (collect_results 와 같은 읽기).
  · --run_log 를 주면 그 로그에 '✅ 완료 → …/<상위 폴더>/<태그>' 줄이 있어야 그린다 (DOS 단계 완주 확인 ·
    회수 폴더엔 .out 이 없다). 안 주면 패널에 '⚠ DOS-stage completion not checked' 를 박는다.
  · CSV 는 그린 그대로 (가우시안 0.10 eV · 0.01 eV 격자) total + 원소별 PDOS 를 낸다 (Origin-ready).
  ⛔ --raw 판이 못 하는 것: 갭 값을 db 에 등재하지 않는다 · 금속 (gap = null) 은 그리지 않는다 (VBM 영점이 없다 ·
    그 경우 collect_results 경로) · 궤도 (s · p · d) 를 나누어 그리지 않는다 (원소 합만) · 두 계의 VBM 을 절대 정렬하지
    않는다 (패널마다 자기 VBM 영점) · 스핀을 나누지 않는다 (스핀분극 계는 거부).
  python3 tools/figures/fig_sei_dos_pdos.py --selftest      # --raw 읽기의 양성 · 음성 시험
"""
import argparse
import csv
import glob
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tools.figures.house_style import INK, MUT, ELEM, GAPBAND, GAPLINE, GAPTEXT, apply_axes

EL = json.load(open("db/properties/sei_electronic.json"))["results"]
from tools.sei.collect_results import read_cols, PDOS_RE   # QE .dos/.pdos 읽기 — 회수기와 같은 읽기를 쓴다
DOSDIR = "db/properties/sei_dos"
FIGDIR = "docs/figures/sei"
CSVDIR = "db/properties"

# 표시명 · 패널 순서 = **갭 내림차순**(절연 잘 되는 것부터 → Li₃P 가 맨 끝에 홀로 남는다)
DISP = {
    "licl_mp-22905":    "LiCl",
    "li3po4_mp-13725":  r"Li$_3$PO$_4$ ($\beta$)",
    "li3po4g_mp-2878":  r"Li$_3$PO$_4$ ($\gamma$)",
    "li2o_mp-1960":     r"Li$_2$O",
    "li2s_mp-1153":     r"Li$_2$S",
    "li3p_mp-736":      r"Li$_3$P",
    "lindo2_mp-1222355": r"LiNdO$_2$",
    "nd2o3_mp-2763":    r"Nd$_2$O$_3$",
    "nd2s3_mp-438":     r"Nd$_2$S$_3$",
    # [혁주] LZO 트랙 (--raw 판 · 태그 = QE 작업 폴더 이름)
    "Li2ZrO3_mp-aaaaagdw": r"Li$_2$ZrO$_3$ (C2/c)",
    "ZrO2_mp-aaaaaefy":    r"ZrO$_2$ (P2$_1$/c)",
}
CITABLE = ["licl_mp-22905", "li3po4_mp-13725", "li3po4g_mp-2878",
           "li2o_mp-1960", "li2s_mp-1153", "li3p_mp-736"]
ND = ["lindo2_mp-1222355", "nd2o3_mp-2763", "nd2s3_mp-438"]
ELEM_X = dict(ELEM, Nd="#a21caf")           # Nd 는 house 팔레트에 없다 — 진단용에만 쓴다
SIG_EV = 0.10                               # 가우시안 평활 폭 [eV]


def load(tag):
    """PDOS CSV 를 읽어 원소별로 합산한다(s+p+d+f). 궤도 분해는 이 그림의 요점이 아니다."""
    p = os.path.join(DOSDIR, f"{tag}_pdos.csv")
    with open(p, encoding="utf-8") as f:
        f.readline()                                    # '#' 출처 주석
        r = csv.reader(f); hdr = next(r)
        rows = np.array([[float(x) for x in v] for v in r if len(v) == len(hdr)])
    E = rows[:, hdr.index("E_minus_VBM_eV")]
    by_el = {}
    for i, h in enumerate(hdr):
        if "_" not in h or h.startswith("E_"):
            continue
        el = h.split("_")[0]
        by_el[el] = by_el.get(el, 0.0) + rows[:, i]
    # total 은 dos.x 산출을 쓴다 — projwfc 합은 투영 손실 때문에 항상 조금 모자란다
    pd_ = os.path.join(DOSDIR, f"{tag}_dos.csv")
    with open(pd_, encoding="utf-8") as f:
        f.readline(); r = csv.reader(f); h2 = next(r)
        d2 = np.array([[float(x) for x in v] for v in r if len(v) == len(h2)])
    Et = d2[:, h2.index("E_minus_VBM_eV")]
    tot = np.interp(E, Et, d2[:, h2.index("DOS_states_per_eV")])
    return E, tot, by_el


def load_raw(d, run_log=None):
    """--raw 판: 회수한 QE 작업 폴더 하나 → (E−VBM, total DOS, 원소별 PDOS, g).

    g 는 gap.json 그대로 + `dos_chain_complete` (True = run.log 에 완료 줄 · None = 확인 안 함).
    못 그리는 폴더는 SystemExit 로 거부한다 — 조용히 빈 패널을 만들지 않는다.
    """
    tag = os.path.basename(os.path.normpath(d))
    gj = os.path.join(d, "gap.json")
    if not os.path.isfile(gj):
        raise SystemExit(f"⛔ {d}: gap.json 이 없다 — 띠틈 단계 (03) 결과가 없는 폴더는 그리지 않는다")
    g = json.load(open(gj, encoding="utf-8"))
    if g.get("gap") is None or g.get("vbm") is None or g.get("cbm") is None:
        raise SystemExit(f"⛔ {tag}: gap.json 에 gap · vbm · cbm 이 다 있어야 한다 (금속 · 미정은 collect_results 경로)")
    if g.get("spin_polarized"):
        raise SystemExit(f"⛔ {tag}: 스핀분극 계는 --raw 판이 다루지 않는다 (위 · 아래 스핀을 합쳐 그리면 틀린다)")
    dosf = sorted(glob.glob(os.path.join(d, "*.dos")))
    if len(dosf) != 1:
        raise SystemExit(f"⛔ {tag}: *.dos 가 {len(dosf)} 개다 — 하나여야 한다")
    td = np.array(read_cols(dosf[0], 3))
    if td.size == 0:
        raise SystemExit(f"⛔ {tag}: {os.path.basename(dosf[0])} 에 숫자 줄이 없다")
    by_el, egrid = {}, None
    for f in sorted(glob.glob(os.path.join(d, "*.pdos_atm#*"))):
        m = PDOS_RE.search(os.path.basename(f))
        if not m:
            continue
        rows = np.array(read_cols(f, 3))
        if rows.size == 0:
            raise SystemExit(f"⛔ {tag}: {os.path.basename(f)} 에 숫자 줄이 없다")
        if egrid is None:
            egrid = rows[:, 0]
        elif len(rows) != len(egrid) or not np.allclose(rows[:, 0], egrid):
            raise SystemExit(f"⛔ {tag}: {os.path.basename(f)} 의 에너지 격자가 다른 PDOS 파일과 다르다")
        el = m.group(2)
        by_el[el] = by_el.get(el, 0.0) + rows[:, 1]          # ldos 열 = 그 wfc 의 기여 합
    if egrid is None:
        raise SystemExit(f"⛔ {tag}: *.pdos_atm#* 파일이 없다 — projwfc 단계 (06) 결과가 없다")
    g = dict(g)
    g["dos_chain_complete"] = None
    if run_log is not None:
        sub = os.path.basename(os.path.dirname(os.path.normpath(d)))
        want = f"/{sub}/{tag}"
        lines = [ln.rstrip() for ln in open(run_log, encoding="utf-8", errors="ignore")]
        if not any("✅ 완료" in ln and ln.endswith(want) for ln in lines):
            raise SystemExit(f"⛔ {tag}: {run_log} 에 '✅ 완료 → …{want}' 줄이 없다 — DOS 단계 완주를 확인 못 했다")
        g["dos_chain_complete"] = True
    vbm = float(g["vbm"])
    E = egrid - vbm
    tot = np.interp(egrid, td[:, 0], td[:, 1])            # total 은 dos.x 산출 (projwfc 합은 투영 손실로 모자란다)
    g["_source_dir"] = d
    return E, tot, by_el, g


def smooth(E, y, sig=SIG_EV):
    dE = float(np.median(np.diff(E)))
    n = max(1.0, sig / max(dE, 1e-9))
    from scipy.ndimage import gaussian_filter1d
    return gaussian_filter1d(y, n)


def panel(ax, tag, xlim, data=None):
    """data = load_raw() 결과 (--raw 판) · 없으면 db (sei_electronic.json · sei_dos CSV) 에서 읽는다."""
    if data is None:
        g = EL[tag]
        E, tot, by_el = load(tag)
    else:
        E, tot, by_el, g = data
    m = (E >= xlim[0] - 1) & (E <= xlim[1] + 1)
    E, tot = E[m], smooth(E[m], tot[m])
    # ★ 갭 띠는 **고유값**으로 그린다 (DOS 문턱 아님)
    ax.axvspan(0.0, g["gap"], color=GAPBAND, zorder=0)
    for x in (0.0, g["gap"]):
        ax.axvline(x, color=GAPLINE, ls="--", lw=1.0, zorder=1)
    sm_el = {}
    for el, y in sorted(by_el.items(), key=lambda kv: -np.max(kv[1])):
        sm_el[el] = smooth(E, y[m])
        ax.fill_between(E, 0, sm_el[el], color=ELEM_X.get(el, MUT),
                        alpha=0.45, lw=0, label=el, zorder=2)
    ax.plot(E, tot, color=INK, lw=1.3, zorder=5)
    ax.set_xlim(*xlim); ax.set_ylim(0, None)
    ax.text(0.015, 0.93, DISP.get(tag, tag), transform=ax.transAxes,
            fontsize=11.5, color=INK, va="top", fontweight="bold")
    lab = f"{g['gap']:.2f} eV" if g["gap"] > 0.05 else f"{g['gap']:.3f} eV (closed)"
    ax.text(g["gap"] / 2 if g["gap"] > 1.2 else g["gap"] + 0.35, 0.62,
            lab, transform=ax.get_xaxis_transform(),
            ha="center" if g["gap"] > 1.2 else "left",
            fontsize=9.5, color=GAPTEXT, fontweight="bold")
    # ⚠ 범례가 오른쪽 위에 있다 — 경고문을 같은 자리에 두면 글자가 겹쳐 둘 다 못 읽는다
    #   (2026-08-07 1차 렌더에서 LiCl 패널이 그랬다). 상 이름 바로 아래 왼쪽에 붙인다.
    if g.get("dos_chain_complete", True) is False:
        ax.text(0.015, 0.79, "⚠ curve from an earlier run (gap unaffected)",
                transform=ax.transAxes, va="top", fontsize=7.5, color="#b45309")
    elif g.get("dos_chain_complete", True) is None:     # --raw 판에서 run.log 를 안 준 경우
        ax.text(0.015, 0.79, "⚠ DOS-stage completion not checked",
                transform=ax.transAxes, va="top", fontsize=7.5, color="#b45309")
    apply_axes(ax)
    ax.legend(loc="upper right", fontsize=8, frameon=False, ncol=2,
              handlelength=1.1, labelspacing=0.25, columnspacing=0.9)
    return E, tot, sm_el


def figure(tags, out, title, sub, xlim, csvname, data=None):
    """data = {tag: load_raw(...)} 이면 --raw 판 — CSV 에 원소별 PDOS 열도 같이 낸다 (db 에 원소 CSV 가 없으니까)."""
    n = len(tags)
    fig, axs = plt.subplots(n, 1, figsize=(7.6, 1.62 * n + 1.5), sharex=True)
    axs = np.atleast_1d(axs)
    curves = {}
    for ax, t in zip(axs, tags):
        curves[t] = panel(ax, t, xlim, None if data is None else data[t])
    axs[-1].set_xlabel(r"$E - E_{\mathrm{VBM}}$  (eV)", fontsize=12, color=INK)
    fig.text(0.012, 0.5, "DOS  (states / eV)", rotation=90, va="center",
             fontsize=12, color=INK)
    axs[0].set_title(title, fontsize=13, color=INK, pad=12)
    fig.text(0.5, 0.985, sub, ha="center", va="top", fontsize=8.6, color=MUT)
    fig.tight_layout(rect=[0.035, 0.0, 1, 0.972])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=300); plt.close(fig)
    print(f"  → {out}")

    # Origin-ready: 그림에 **실제로 그린** total 곡선(평활·창 적용)만 모아 낸다.
    # 원소분해 원자료는 db/properties/sei_dos/*.csv 에 이미 있다.
    grid = np.arange(xlim[0], xlim[1] + 1e-9, 0.01)
    cols = {t: np.interp(grid, curves[t][0], curves[t][1]) for t in tags}
    hdr = [f"{t.split('_mp')[0]}_DOS_states_per_eV" for t in tags]
    keys = [(t, None) for t in tags]
    if data is not None:                                   # --raw 판: 원소별 PDOS (그린 그대로) 도 싣는다
        for t in tags:
            for el in sorted(curves[t][2]):
                cols[(t, el)] = np.interp(grid, curves[t][0], curves[t][2][el])
                hdr.append(f"{t.split('_mp')[0]}_{el}_PDOS_states_per_eV")
                keys.append((t, el))
    p = os.path.join(CSVDIR, csvname)
    with open(p, "w", encoding="utf-8") as f:
        what = "total DOS + element PDOS" if data is not None else "total DOS"
        f.write(f"# {title} — {what} as plotted (Gaussian {SIG_EV} eV, "
                f"E referenced to each phase's own VBM). Gaps are fixed-occ nscf "
                f"eigenvalues, NOT read off these curves. QE/PBE — our calculation, "
                f"do not mix with Materials Project values.\n")
        if data is not None:
            for t in tags:
                g = data[t][3]
                f.write(f"# {t}: VBM {g['vbm']} eV · CBM {g['cbm']} eV · gap {g['gap']:.4f} eV (gap.json) · "
                        f"source {g['_source_dir']} · DOS-stage completion "
                        f"{'checked in run.log' if g['dos_chain_complete'] else 'NOT checked'}\n")
        f.write("E_minus_VBM_eV," + ",".join(hdr) + "\n")
        for i, e in enumerate(grid):
            f.write(f"{e:.3f}," + ",".join(
                f"{(cols[k[0]] if k[1] is None else cols[k])[i]:.5g}" for k in keys) + "\n")
    print(f"  → {p}")


def ladder(out):
    """갭 사다리 — '절연 되나 / 새나' 한 장 요약."""
    tags = sorted(CITABLE, key=lambda t: EL[t]["gap"])
    g = [EL[t]["gap"] for t in tags]

    def col(x):
        return "#15803d" if x >= 4.0 else "#ca8a04" if x >= 2.0 else "#b91c1c"

    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    y = np.arange(len(tags))
    ax.barh(y, g, color=[col(x) for x in g], edgecolor=INK, lw=0.6, height=0.62, zorder=3)
    for i, x in enumerate(g):
        ax.text(x + 0.12, i, f"{x:.2f}", va="center", fontsize=10, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([DISP[t] for t in tags], fontsize=11, color=INK)
    ax.axvline(2.0, color=MUT, ls=":", lw=1.0, zorder=1)
    # ⚠ 이 주석을 맨 위 막대 위에 그냥 두면 제목과 겹친다 — ylim 을 열어 자리를 만든다.
    ax.set_ylim(-0.62, len(tags) - 0.25)
    ax.text(2.05, len(tags) - 0.42, "electron leak  ←|→  insulating",
            fontsize=8.6, color=MUT, va="center")
    ax.set_xlim(0, max(g) * 1.18)
    apply_axes(ax, xlabel="Band gap (eV)  —  fixed-occupation nscf eigenvalues, PBE")
    ax.set_title("SEI decomposition phases: electronic insulation",
                 fontsize=12.5, color=INK, pad=10)
    fig.text(0.5, 0.005, "PBE underestimates wide gaps by 30–50% — use the ORDER, "
                         "not the absolute values. Our QE calculation (not Materials Project).",
             ha="center", fontsize=7.8, color=MUT)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=300); plt.close(fig)
    print(f"  → {out}")

    p = os.path.join(CSVDIR, "sei_gap_ladder_origin.csv")
    with open(p, "w", encoding="utf-8") as f:
        f.write("# SEI decomposition phase band gaps — fixed-occ nscf eigenvalues (QE/PBE, ours).\n"
                "# NOT Materials Project values; do not mix with tools/figures/plot_nd_sei_gaps.py.\n")
        f.write("phase,material_id,VBM_eV,CBM_eV,gap_eV,verdict\n")
        for t in tags:
            d = EL[t]
            f.write(f"{t.split('_mp')[0]},{t.split('_')[-1]},"
                    f"{d['vbm']:.3f},{d['cbm']:.3f},{d['gap']:.3f},{d['verdict']}\n")
    print(f"  → {p}")


def selftest():
    """--raw 읽기 (load_raw · figure CSV) 의 양성 · 음성 시험. 임시 폴더에 가짜 QE 산출을 만든다."""
    import shutil
    import tempfile
    res = []

    def chk(name, cond):
        res.append(bool(cond)); print(("  ✓ " if cond else "  ✗ ") + name)

    def refused(fn):
        try:
            fn()
        except SystemExit as e:
            return str(e)
        return None

    root = tempfile.mkdtemp(prefix="figsei_")
    try:
        def make(sub, tag, gap=True, spin=False, pdos=True, bad_grid=False):
            d = os.path.join(root, sub, tag); os.makedirs(d, exist_ok=True)
            if gap is not None:
                gj = {"vbm": 2.0, "cbm": 5.0, "gap": 3.0, "spin_polarized": spin} if gap else \
                     {"vbm": None, "cbm": None, "gap": None}
                json.dump(gj, open(os.path.join(d, "gap.json"), "w"))
            E = np.arange(-10.0, 10.0001, 0.01)
            with open(os.path.join(d, f"{tag}.dos"), "w") as f:
                f.write("#  E (eV)   dos(E)     Int dos(E)\n")
                for e in E:
                    f.write(f"{e:.3f} {np.exp(-(e - 1.0) ** 2):.6e} 0.0\n")
            if pdos:
                for i, (el, l, amp) in enumerate([("A", "s", 1.0), ("A", "p", 2.0), ("B", "d", 0.5)], 1):
                    EE = E[:-5] if (bad_grid and i == 3) else E
                    with open(os.path.join(d, f"{tag}.pdos_atm#{i}({el})_wfc#1({l})"), "w") as f:
                        f.write("# E (eV)  ldos(E)  pdos(E)\n")
                        for e in EE:
                            f.write(f"{e:.3f} {amp:.6e} {amp / 4:.6e}\n")   # ldos ≠ pdos — 열을 바꿔 읽으면 잡힌다
            return d

        d = make("main", "X_mp-1")
        E, tot, by_el, g = load_raw(d)
        chk("양성: 영점 = gap.json 의 VBM (E[0] = −10 − 2)", abs(E[0] - (-12.0)) < 1e-9)
        chk("양성: 원소별 ldos 합 (A = 1 + 2 · B = 0.5)", abs(by_el["A"][0] - 3.0) < 1e-9 and abs(by_el["B"][0] - 0.5) < 1e-9)
        chk("양성: total 은 .dos 열 (E = 1 eV 에서 최대)", abs(E[int(np.argmax(tot))] - (1.0 - 2.0)) < 0.011)
        chk("양성: run.log 없으면 완주 '확인 안 함' (None)", g["dos_chain_complete"] is None)
        log = os.path.join(root, "run.log")
        open(log, "w").write(f"[02:42:10]   ✅ 완료 → /home/x/runs/main/X_mp-1\n")
        chk("양성: run.log 에 main/X 완료 줄 → True", load_raw(d, log)[3]["dos_chain_complete"] is True)
        d90 = make("ecut90", "X_mp-1")
        chk("⛔음성: 완료 줄이 main 뿐이면 ecut90 폴더는 거부 (다른 폴더의 완료로 통과시키지 않는다)",
            refused(lambda: load_raw(d90, log)) is not None)
        open(log, "w").write("[02:42:10]   ▶ 06_projwfc.in\n")
        chk("⛔음성: 완료 줄 없는 run.log → 거부", refused(lambda: load_raw(d, log)) is not None)
        chk("⛔음성: gap.json 없음 → 거부", refused(lambda: load_raw(make("main", "NoGap_mp-2", gap=None))) is not None)
        chk("⛔음성: 금속 (gap null) → 거부", refused(lambda: load_raw(make("main", "Metal_mp-3", gap=False))) is not None)
        chk("⛔음성: 스핀분극 → 거부", refused(lambda: load_raw(make("main", "Spin_mp-4", spin=True))) is not None)
        chk("⛔음성: PDOS 파일 없음 → 거부", refused(lambda: load_raw(make("main", "NoP_mp-5", pdos=False))) is not None)
        chk("⛔음성: PDOS 에너지 격자 불일치 → 거부", refused(lambda: load_raw(make("main", "Grid_mp-6", bad_grid=True))) is not None)
        png = os.path.join(root, "f.png"); csvp = os.path.join(root, "f.csv")
        figure(["X_mp-1"], png, "selftest", "sub", (-8.0, 10.0), csvp, data={"X_mp-1": load_raw(d)})
        lines = open(csvp, encoding="utf-8").read().splitlines()
        hdr = next(ln for ln in lines if ln.startswith("E_minus_VBM_eV"))
        chk("양성: CSV 에 total + 원소별 PDOS 열 (X_A · X_B)", hdr.split(",") ==
            ["E_minus_VBM_eV", "X_DOS_states_per_eV", "X_A_PDOS_states_per_eV", "X_B_PDOS_states_per_eV"])
        chk("양성: CSV 머리에 완주 'NOT checked' 가 적힌다 (run.log 안 준 판)", any("NOT checked" in ln for ln in lines[:4]))
        chk("양성: PNG 가 생겼다", os.path.getsize(png) > 1000)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    n_ok = sum(res); n_bad = len(res) - n_ok
    print(f"selftest: {n_ok} 통과 / {n_bad} 실패")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-nd", action="store_true",
                    help="Nd 계 3종을 별도 파일로 (진단용 — 인용 금지 표식이 붙는다)")
    ap.add_argument("--raw", nargs="+", metavar="DIR",
                    help="회수한 QE 작업 폴더 (gap.json · *.dos · *.pdos_atm#*) — db 를 거치지 않고 바로 그린다")
    ap.add_argument("--run_log", help="--raw 판: DOS 단계 완주를 확인할 run.log (안 주면 패널에 '확인 안 함' 표식)")
    ap.add_argument("--out", help="--raw 판: PNG 경로")
    ap.add_argument("--csv", help="--raw 판: db/properties 안의 Origin CSV 파일 이름")
    ap.add_argument("--title", default="DOS / PDOS", help="--raw 판: 그림 제목 (영어)")
    ap.add_argument("--xlim", nargs=2, type=float, default=(-8.0, 10.0), help="E − VBM 창 [eV] (기본 SEI 와 같다)")
    ap.add_argument("--selftest", action="store_true", help="--raw 읽기의 양성 · 음성 시험")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if a.raw:
        if not (a.out and a.csv):
            sys.exit("⛔ --raw 판은 --out 과 --csv 가 둘 다 필요하다")
        data = {}
        for d in a.raw:
            t = os.path.basename(os.path.normpath(d))
            if t in data:
                sys.exit(f"⛔ 같은 태그가 두 번: {t}")
            data[t] = load_raw(d, a.run_log)
        tags = list(data)
        figure(tags, a.out, a.title,
               "Gap band (yellow) = fixed-occupation nscf eigenvalues, not a DOS threshold. "
               "QE/PBE; wide gaps underestimated 30–50%.",
               tuple(a.xlim), a.csv, data=data)
        print("\n⚠ 갭은 fixed-occ nscf 고유값이 정본이다 — 이 곡선에서 문턱을 읽지 말 것.")
        return 0

    missing = [t for t in CITABLE if not os.path.isfile(os.path.join(DOSDIR, f"{t}_pdos.csv"))]
    if missing:
        sys.exit(f"⛔ PDOS CSV 없음: {missing} — tools/sei/collect_results.py 먼저")

    figure(CITABLE, os.path.join(FIGDIR, "sei_dos_pdos.png"),
           "SEI decomposition phases — DOS / PDOS",
           "Gap band (yellow) = fixed-occupation nscf eigenvalues, not a DOS threshold. "
           "QE/PBE; wide gaps underestimated 30–50%.",
           (-8.0, 10.0), "sei_dos_panels_origin.csv")
    ladder(os.path.join(FIGDIR, "sei_gap_ladder.png"))

    if a.with_nd:
        figure(ND, os.path.join(FIGDIR, "sei_dos_pdos_Nd_DIAGNOSTIC.png"),
               "Nd phases — DIAGNOSTIC ONLY, DO NOT CITE",
               "Nd 4f is in the valence: PBE puts the 4f band at E_F and closes the gap. "
               "This is a method failure, not metallicity. Cite MP frozen-4f gaps instead.",
               (-8.0, 10.0), "sei_dos_panels_Nd_DIAGNOSTIC_origin.csv")
    print("\n⚠ 갭은 fixed-occ nscf 고유값이 정본이다 — 이 곡선에서 문턱을 읽지 말 것.")
    print("⚠ 이 숫자는 **우리 QE 값**이다. plot_nd_sei_gaps.py 의 MP 소환값과 섞지 말 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
