"""연구세미나 덱 v3 "보는 판" (2026-10-13) — 한 양식으로 다시 그리는 그림 전부.

값은 전부 리포 정본에서 가져온다 (아래 SRC 주석 · --selftest 가 정본 파일과 대조).  철회값 (claims.json quotation_ban) 은 쓰지 않는다.
  F_poro      다섯 조성 porosity (exact union)                     SRC docs/report_20261021/summary.json G1
  F_trans     수송 tortuosity · σ(Li⁺) 두 패널 (Hertz · σ₀ 1.5)       SRC docs/data/ps45_r45_network_g2_20261007/README.md
  F_limits    (a) 격자 의존 (b) 모델 ↔ DC 분극 (c) ps45 σ_e            SRC CLAUDE.md SR-01 (CL-24 공개값) · sdcp_sigma_e_dcp_anchor_registration_20261012.md · ps45_sigmae_factor_off_20261013/README.md
  F_load      σ_zz 기여 누적 막대 (AM–AM · AM–SE · SE–SE)              SRC docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json (contribution_sigma_zz_pct)
  F_vgcf      σ(e⁻) vs VGCF wt% · 복셀 셋                             SRC docs/report_20261021/summary.json G6
  F_dataset   (a) 기하 tortuosity vs SE 분율 130 + 64 (b) porosity vs SE 분율 130   SRC docs/data/lhs_release_20261006_v12/*.csv
  F_mix1      층상 캠페인 10 런 Lacey M (8 바퀴)                      SRC docs/report_20261021/summary.json G7 (= mixer_final10_20260930)
  F_mix2      개발 런 ΔM (비점착 AM 팔 − 각 팔) · 칸 셋                SRC docs/data/mixer_highbo_{devrot,devbo,devu}_prelim_*/README.md
  F_mix3      SE–SE 접촉 군집 분율 (bin 1) · 접착일 도식               SRC docs/data/mixer_highbo_devu_prelim_20261006/README.md §3 · docs/hetero_thesis.md §2-2
글씨 = 덱 최종 배치 크기 기준 ≈ 12 pt (각 그림의 figsize = 배치 크기 1:1 · font 13 → 배율 0.93–1.0).
실행: python3 make_seminar_figs.py <out_dir> [--repo <리포>]   · selftest: --selftest
"""
import csv
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch  # noqa: E402
from matplotlib.ticker import FuncFormatter, MaxNLocator  # noqa: E402

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "axes.labelsize": 13, "xtick.labelsize": 12.5, "ytick.labelsize": 12.5,
                     "legend.fontsize": 11.5, "axes.linewidth": 0.9, "svg.fonttype": "none", "mathtext.fontset": "dejavusans",
                     "axes.titlesize": 13, "axes.titleweight": "bold"})
NAVY, RED, SKY, ORANGE, GRAY, GREEN, LIGHT = "#1F3A68", "#C0392B", "#4A90C8", "#D95D12", "#6B7280", "#2E8B57", "#B8C4D6"
CM = 1 / 2.54
REPO = Path(__file__).resolve()
REPO = next((p for p in REPO.parents if (p / "CLAUDE.md").exists()), Path("/home/user/Yonghoon-DEM-DFT"))

# ── 정본 값 (SRC) ────────────────────────────────────────────────────────────
PS = ["0:10", "3:7", "5:5", "7:3", "10:0"]
PORO = [20.59, 18.67, 17.67, 16.49, 16.90]                     # G1 union %
TAU2 = [7.2433, 5.9733, 5.4495, 5.0297, 5.2864]                # ps45 README (Hertz · 주 값)
SIG_ION = [0.0587, 0.0730, 0.0814, 0.0893, 0.0838]             # ps45 README §σ₀ = 1.5
GRID = dict(vox_um=[0.4, 0.3, 0.25], sigma_e_ratio=[1.4215, 1.1621, 1.0849], sigma_ion_ratio=[1.0742, 0.9926, 0.9908])  # CL-24 공개값
SIGMA_E_EXP = dict(labels=["SBE", "DBE"], model=[54.0, 70.6], exp=[4.47, 12.4])       # DC 분극 앵커 등록
PS45_SIG_E = [0.391, 0.406, 0.402, 0.375, 0.467]                                       # 인자 끔 주 값
LOAD = {"0:10": (59.562, 31.008, 9.429), "3:7": (54.635, 34.660, 10.705), "5:5": (52.372, 36.219, 11.409),
        "7:3": (48.464, 39.144, 12.392), "10:0": (56.914, 32.954, 10.132)}             # plane_load.json contribution_sigma_zz_pct (AM–AM · AM–SE · SE–SE)
VGCF = dict(wt=[1.0, 2.0, 3.0, 4.0], vox=[0.15, 0.2, 0.25],
            mean={0.15: [2.12, 15.24, 59.34, 130.98], 0.2: [3.31, 26.87, 90.04, 189.16], 0.25: [4.74, 40.42, 127.52, 262.26]})  # G6 means (mS/cm)
MIX1 = [("L0", 0.9724, 0.0254), ("LA s1", 0.9817, 0.0263), ("LA s2", 0.9726, 0.0293), ("LA s3", 0.9904, 0.0313),
        ("LB1", 0.9869, 0.0320), ("LB2", 0.9646, 0.0305), ("LB3", 0.9776, 0.0313),
        ("LC s1", 0.9684, 0.0269), ("LC s2", 0.9824, 0.0276), ("LC s3", 0.9975, 0.0305)]                    # G7 runs (planned.M_final · bin-7 SD)
MIX1_MAIN = dict(Delta=0.0012, SE=0.0073)                                                                   # 16×16×4 주판정 칸
# 개발 런 (seed 1 · 2 바퀴 · n = 1) — ΔM = M(낮은 점착 비교군) − M(팔) · 칸 (16×16×4 · 12×12×3 · 8×8×2) · 값 = 판독 JSON (dev_delta_m · dev_cluster)


DEV_JSON = dict(rot="docs/data/mixer_highbo_devrot_prelim_20261002/ref_r2_c{}.json",
                bo="docs/data/mixer_highbo_devbo_prelim_20261003/devbo_c{}.json",
                u="docs/data/mixer_highbo_devu_prelim_20261006/devu_c{}.json")
GRIDS = ("16x4", "12x3", "8x2")
DEV_ARMS = {"Bo38.4": ("rot", "LH_ref"), "Bo384": ("bo", "LHx10_ref"), "Bo1152": ("bo", "LHx30_ref"),
            "CED10": ("u", "LU212_ref"), "CED14": ("u", "LU637_ref")}   # 원 런 이름 = 판독 JSON 열쇠 (화면에는 안 쓴다)


def dev_planned_m(repo=REPO):
    """등록 최종값 planned.M_final · 칸 셋 (16×16×4 · 12×12×3 · 8×8×2) — 'low' = 낮은 점착 비교군 · 나머지 = DEV_ARMS 열쇠."""
    out = {}
    for key, (src, arm) in DEV_ARMS.items():
        vals, low = [], []
        for g in GRIDS:
            runs = {it["run"].rstrip("/").split("/")[-1]: it["planned"]["M_final"]
                    for it in json.loads((Path(repo) / DEV_JSON[src].format(g)).read_text(encoding="utf-8"))}
            low.append(next(v for k, v in runs.items() if k.startswith("LC_ref")))
            vals.append(next(v for k, v in runs.items() if k.startswith(arm + "_")))
        out[key] = tuple(vals)
        out.setdefault("low", tuple(low))
    return out


def dev_delta_m(repo=REPO):
    """ΔM = M(낮은 점착 비교군) − M(팔) · 등록 최종값 planned.M_final · 칸 셋 (16×16×4 · 12×12×3 · 8×8×2)."""
    m = dev_planned_m(repo)
    return {k: tuple(lo - v for lo, v in zip(m["low"], vals)) for k, vals in m.items() if k != "low"}


def dev_cluster(repo=REPO):
    """SE–SE 군집 SE 분율 (2 바퀴째 bin 1 · 100 프레임 평균 · [확실, 가능] 덤프 해상도 범위의 평균)."""
    c = json.loads((Path(repo) / "docs/data/mixer_highbo_devu_prelim_20261006/devu_contact.json").read_text(encoding="utf-8"))
    name = {"LC_ref": "low", "LU212_ref": "CED10", "LU637_ref": "CED14"}
    out = {}
    for r in c["runs"]:
        run = r["run"].rstrip("/").split("/")[-1]
        key = next((v for k, v in name.items() if run.startswith(k + "_")), None)
        if key:
            m = r["bin"]["mean"]
            out[key] = (m["se_frac_in_clusters"], m["lo.se_frac_in_clusters"], m["hi.se_frac_in_clusters"])
    return out


def _fmt(ax, ny=4, nx=None):
    if nx:
        ax.xaxis.set_major_locator(MaxNLocator(nx))
    ax.yaxis.set_major_locator(MaxNLocator(ny))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace("-", "−")))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


OVERLAPS = []   # (그림, 글 A, 글 B) — 그려진 글자 상자끼리 겹친 쌍 (selftest 가 0 을 요구)


def _text_items(fig):
    """실제로 그려지는 글자만: 보이는 범위 안 눈금 라벨 · 축 이름 · 제목 · 축 안 글 · 범례 · 그림 글."""
    import matplotlib.text as mtext
    items = []
    def add(t):
        if isinstance(t, mtext.Text) and t.get_visible() and t.get_text().strip():
            items.append(t)
    for ax in fig.axes:
        for axis, lim in ((ax.xaxis, ax.get_xlim()), (ax.yaxis, ax.get_ylim())):
            lo, hi = min(lim), max(lim)
            span = hi - lo
            for tick in axis.get_major_ticks():
                loc = tick.get_loc()
                if lo - 1e-9 * abs(span) <= loc <= hi + 1e-9 * abs(span):
                    add(tick.label1)
            add(axis.label)
        for t in (ax.title, ax._left_title, ax._right_title):
            add(t)
        for t in ax.texts:
            add(t)
        leg = ax.get_legend()
        if leg is not None:
            for t in leg.get_texts():
                add(t)
            add(leg.get_title())
    for t in fig.texts:
        add(t)
    return items


def _text_overlaps(fig, pad=0.5):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    boxes = [(t.get_text().strip().replace("\n", " ")[:28], t.get_window_extent(r)) for t in _text_items(fig)]
    out = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            if min(a.x1, b.x1) - max(a.x0, b.x0) > pad and min(a.y1, b.y1) - max(a.y0, b.y0) > pad:
                out.append((boxes[i][0], boxes[j][0]))
    return out


def _save(fig, out, name, rows=None, header=None):
    OVERLAPS.extend((name, a, b) for a, b in _text_overlaps(fig))
    fig.savefig(f"{out}/{name}.png", dpi=300, transparent=False, facecolor="white", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(f"{out}/{name}.svg", transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    if rows is not None:
        with open(f"{out}/{name}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(header)
            for r in rows:
                w.writerow(r)


def _bar_labels(ax, bars, fmt="{:.1f}", dy=0.0, size=11.5, color=None):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + dy, fmt.format(b.get_height()), ha="center", va="bottom", fontsize=size, color=color or b.get_facecolor())


# ── F_poro ──────────────────────────────────────────────────────────────────
def fig_poro(out):
    fig, ax = plt.subplots(figsize=(7.9 * CM, 6.6 * CM))
    cols = [RED if v == min(PORO) else NAVY for v in PORO]
    bars = ax.bar(range(5), PORO, 0.6, color=cols)
    _bar_labels(ax, bars, dy=0.3, size=11, color=None)
    ax.set_xticks(range(5)); ax.set_xticklabels(PS)
    ax.set_xlabel("Large : small NCM (mass)")
    ax.set_ylabel("Porosity (%)")
    ax.set_ylim(0, 25)
    _fmt(ax, ny=5)
    fig.tight_layout(pad=0.3)
    _save(fig, out, "F_poro", rows=list(zip(PS, PORO)), header=["PC:SC", "porosity union (%)"])


# ── F_trans ─────────────────────────────────────────────────────────────────
def fig_trans(out):
    fig, (a, b) = plt.subplots(1, 2, figsize=(13.4 * CM, 7.0 * CM))
    cols_t = [RED if v == min(TAU2) else NAVY for v in TAU2]
    bars = a.bar(range(5), TAU2, 0.6, color=cols_t)
    _bar_labels(a, bars, fmt="{:.1f}", dy=0.1, size=10.5)
    a.set_ylim(0, 8.5); a.set_ylabel("Transport tortuosity\nT = φ$_{SE}$ σ$_0$ / σ$_{eff}$"); a.set_title("(a)", loc="left")
    cols_s = [RED if v == max(SIG_ION) else NAVY for v in SIG_ION]
    b.bar(range(5), SIG_ION, 0.6, color=cols_s)          # 값 표시 없음 (세 자리 값끼리 겹쳤다 · 값은 notes)
    b.set_ylim(0, 0.1); b.set_ylabel("σ(Li$^+$) (mS cm$^{-1}$)"); b.set_title("(b)", loc="left")
    for ax in (a, b):
        ax.set_xticks(range(5)); ax.set_xticklabels(PS, fontsize=9.5)
        ax.set_xlabel("Large : small NCM (mass)", fontsize=12)
        _fmt(ax, ny=4)
    fig.tight_layout(pad=0.3, w_pad=1.6)
    _save(fig, out, "F_trans", rows=list(zip(PS, TAU2, SIG_ION)), header=["PC:SC", "transport tortuosity (Hertz)", "sigma_ion (mS/cm, sigma0 = 1.5)"])


# ── F_limits ────────────────────────────────────────────────────────────────
def fig_limits(out):
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(22.8 * CM, 7.6 * CM), gridspec_kw=dict(width_ratios=[1.0, 0.95, 1.25]))
    v = GRID["vox_um"]
    a.plot(v, GRID["sigma_e_ratio"], "-o", color=RED, lw=1.6, ms=6, label="electronic")
    a.plot(v, GRID["sigma_ion_ratio"], "-s", color=SKY, lw=1.6, ms=6, label="ionic")
    a.axhline(1.0, color=GRAY, lw=0.8, ls=":")
    a.invert_xaxis(); a.set_xticks(v); a.set_xticklabels([f"{x:g}" for x in v])
    a.set_xlabel("Voxel size (µm)"); a.set_ylabel("Conductivity ratio\n(with / without polymer)"); a.set_ylim(0.95, 1.5)
    a.legend(frameon=False, loc="upper right", fontsize=10.5); a.set_title("(a)", loc="left")
    x = [0, 1]; wdt = 0.34
    b.bar([i - wdt / 2 for i in x], SIGMA_E_EXP["model"], wdt, color=NAVY, label="voxel model")
    b.bar([i + wdt / 2 for i in x], SIGMA_E_EXP["exp"], wdt, color=ORANGE, label="DC polarization")
    b.set_xticks(x); b.set_xticklabels(SIGMA_E_EXP["labels"]); b.set_yscale("log"); b.set_ylim(1, 600)
    b.set_ylabel("Electronic conductivity\n(mS cm$^{-1}$)")
    b.legend(frameon=False, loc="upper left", fontsize=10.5, handlelength=1.0, borderaxespad=0.2); b.set_title("(b)", loc="left")
    b.spines["top"].set_visible(False); b.spines["right"].set_visible(False)
    c.bar(range(5), PS45_SIG_E, 0.55, color=NAVY)
    c.set_xticks(range(5)); c.set_xticklabels(PS, fontsize=10.5); c.set_xlabel("Large : small NCM (mass)", fontsize=12)
    c.set_ylabel("Electronic conductivity\n(mS cm$^{-1}$)"); c.set_ylim(0, 0.6); c.set_title("(c)", loc="left")
    _fmt(a, ny=5); _fmt(c, ny=4)
    fig.tight_layout(pad=0.3, w_pad=2.2)
    rows = [("grid", vv, r1, r2) for vv, r1, r2 in zip(v, GRID["sigma_e_ratio"], GRID["sigma_ion_ratio"])]
    rows += [("model_vs_exp", lab, m, e) for lab, m, e in zip(SIGMA_E_EXP["labels"], SIGMA_E_EXP["model"], SIGMA_E_EXP["exp"])]
    rows += [("ps45_sigma_e", p, s, "") for p, s in zip(PS, PS45_SIG_E)]
    _save(fig, out, "F_limits", rows=rows, header=["panel", "x", "y1", "y2"])


# ── F_load ──────────────────────────────────────────────────────────────────
def fig_load(out):
    fig, ax = plt.subplots(figsize=(8.8 * CM, 7.6 * CM))
    aa = [LOAD[p][0] for p in PS]; ase = [LOAD[p][1] for p in PS]; ss = [LOAD[p][2] for p in PS]
    x = range(5)
    b1 = ax.bar(x, aa, 0.62, color=NAVY, label="NCM–NCM")
    ax.bar(x, ase, 0.62, bottom=aa, color=SKY, label="NCM–SE")
    ax.bar(x, ss, 0.62, bottom=[i + j for i, j in zip(aa, ase)], color=ORANGE, label="SE–SE")
    for b, v in zip(b1, aa):
        ax.text(b.get_x() + b.get_width() / 2, v / 2, f"{v:.0f}", ha="center", va="center", color="white", fontsize=11.5)
    ax.set_xticks(list(x)); ax.set_xticklabels(PS); ax.set_xlabel("Large : small NCM (mass)")
    ax.set_ylabel("Contribution to σ$_{zz}$ (%)"); ax.set_ylim(0, 100)
    _fmt(ax, ny=5)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.17), handlelength=0.9, columnspacing=0.8, fontsize=10.5)
    fig.tight_layout(pad=0.3)
    _save(fig, out, "F_load", rows=[(p, *LOAD[p]) for p in PS], header=["PC:SC", "AM-AM (%)", "AM-SE (%)", "SE-SE (%)"])


# ── F_vgcf ──────────────────────────────────────────────────────────────────
def fig_vgcf(out):
    fig, ax = plt.subplots(figsize=(8.8 * CM, 6.3 * CM))      # 7 장 자리 (본문 3 줄 × 2 → 그림 띠 2.45 in) 에 1:1
    for vox, col, mk in zip(VGCF["vox"], (NAVY, SKY, ORANGE), ("o", "s", "^")):
        ax.plot(VGCF["wt"], VGCF["mean"][vox], "-" + mk, color=col, lw=1.6, ms=6, label=f"voxel {vox:g} µm")
    ax.set_yscale("log"); ax.set_ylim(1, 500)
    ax.set_xticks(VGCF["wt"]); ax.set_xticklabels([f"{w:g}" for w in VGCF["wt"]])
    ax.set_xlabel("VGCF (wt%)"); ax.set_ylabel("Electronic conductivity\n(mS cm$^{-1}$)")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout(pad=0.3)
    rows = [(vox, w, m) for vox in VGCF["vox"] for w, m in zip(VGCF["wt"], VGCF["mean"][vox])]
    _save(fig, out, "F_vgcf", rows=rows, header=["voxel (um)", "VGCF wt%", "sigma_e mean (mS/cm)"])


# ── F_dataset ───────────────────────────────────────────────────────────────
def _release_rows(repo):
    def load(p):
        with open(p, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    base = Path(repo) / "docs/data/lhs_release_20261006_v12"
    return load(base / "lhs_release_20261006_v12.csv"), load(base / "lhsx_release_20261006_v12.csv")


def _col(rows, key, scale=1.0):
    out = []
    for r in rows:
        v = r.get(key, "")
        try:
            out.append(float(v) * scale)
        except ValueError:
            out.append(math.nan)
    return out


def fig_dataset(out, repo):
    r130, r64 = _release_rows(repo)
    def se_pct(rows):
        v = _col(rows, "se_of_solid_vol")
        mx = max(x for x in v if not math.isnan(x))
        return [x * (100 if mx <= 1.0 else 1) for x in v]
    se130, se64 = se_pct(r130), se_pct(r64)
    t130, t64 = _col(r130, "tortuosity_SE_wall"), _col(r64, "tortuosity_SE_wall")
    p130 = _col(r130, "porosity_union_exact_pct")
    fig, (a, b) = plt.subplots(1, 2, figsize=(11.2 * CM, 7.6 * CM))
    ok130 = [(s, t) for s, t in zip(se130, t130) if not math.isnan(t)]
    non130 = [s for s, t in zip(se130, t130) if math.isnan(t)]
    a.scatter([s for s, _ in ok130], [t for _, t in ok130], s=16, color=NAVY, zorder=3)
    a.scatter(se64, t64, s=16, color=SKY, marker="s", zorder=3)
    a.scatter(non130, [1.0] * len(non130), s=26, color=GRAY, marker="x", lw=1.0, zorder=3)
    # 범례 대신 직접 표지 (점 위에 범례가 얹히던 것 · Codex P2) · × 는 표시 위치일 뿐 (값 = 결측)
    a.text(68, 3.05, "130-bed set", color=NAVY, fontsize=10.5, ha="center")
    a.text(68, 1.95, "64-bed set", color=SKY, fontsize=10.5, ha="center")
    a.text(7, 0.68, "× no spanning path", color=GRAY, fontsize=9.5, ha="left", va="center")
    a.set_xlabel("SE (vol% of solid)"); a.set_ylabel("Geometric tortuosity"); a.set_title("(a)", loc="left")
    a.set_ylim(0.5, 4.6); a.set_xlim(5, 90)
    b.scatter(se130, p130, s=16, color=NAVY, zorder=3)
    b.set_xlabel("SE (vol% of solid)"); b.set_ylabel("Porosity (%)"); b.set_title("(b)", loc="left")
    for ax in (a, b):
        _fmt(ax, ny=4, nx=5)
    fig.tight_layout(pad=0.3, w_pad=1.8)
    rows = [("130", s, t, p) for s, t, p in zip(se130, t130, p130)] + [("64", s, t, "") for s, t in zip(se64, t64)]
    _save(fig, out, "F_dataset", rows=rows, header=["set", "SE fraction of solid (vol%)", "geometric tortuosity (blank = non-percolating)", "porosity union (%)"])
    return dict(n130=len(r130), n64=len(r64), nonspan130=len(non130), tau130=(min(t for _, t in ok130), max(t for _, t in ok130)),
                tau64=(min(t64), max(t64)))


# ── F_mix1 ──────────────────────────────────────────────────────────────────
MIX1_GROUPS = [("no cohesion\n(control)", ["L0"]), ("low NCM–NCM\ncohesion", ["LC s1", "LC s2", "LC s3"]),
               ("reference\ncohesion", ["LA s1", "LA s2", "LA s3"]), ("lower\ncohesion\n(3 levels)", ["LB1", "LB2", "LB3"])]
MIX1_MEMBER = {"L0": "seed 1", "LB1": "Bo 0.1", "LB2": "Bo 0.5", "LB3": "Bo 1.5"}   # CSV 에 팔 코드 대신 적는 이름 (seed n · 명목 Bo)


def fig_mix1(out):
    fig, ax = plt.subplots(figsize=(12.0 * CM, 6.2 * CM))      # 11 장 그림 띠 (≈ 4.75 × 2.45 in) 에 1:1
    look = {k: (m, sd) for k, m, sd in MIX1}
    x = 0.0; ticks = []; rows = []
    for gi, (lab, keys) in enumerate(MIX1_GROUPS):
        xs = []
        col = [GRAY, RED, NAVY, SKY][gi]
        for k in keys:
            m, sd = look[k]
            ax.bar(x, m, 0.8, color=col, yerr=sd, error_kw=dict(ecolor="#333333", lw=0.9, capsize=2))
            member = MIX1_MEMBER.get(k, "seed " + k.split(" s")[-1])
            xs.append(x); rows.append((lab.replace("\n", " "), member, m, sd)); x += 1.0
        ticks.append((sum(xs) / len(xs), lab)); x += (3.8 if gi == 0 else 2.0)   # 대조군 (막대 하나) 뒤는 넓게 — 라벨 폭
    ax.axhline(1.0, color=GRAY, lw=0.8, ls=":")
    ax.set_xticks([t for t, _ in ticks]); ax.set_xticklabels([l for _, l in ticks], fontsize=10)
    ax.set_xlim(-2.2, x - 2.0 + 0.2)
    ax.set_ylabel("Lacey index M\n(8 revolutions)"); ax.set_ylim(0, 1.12)
    _fmt(ax, ny=5)
    fig.tight_layout(pad=0.3)
    _save(fig, out, "F_mix1", rows=rows, header=["setting", "member", "M after 8 revolutions (16x16x4)", "within-run SD"])


# ── F_mix2 ──────────────────────────────────────────────────────────────────
MIX2_LABELS = [("Bo38.4", "38.4"), ("Bo384", "384"), ("Bo1152", "1152"), ("CED10", "×10"), ("CED14", "×14.42")]
MIX2_QC = {"Bo384": (0,), "Bo1152": (0,), "CED14": (0,)}   # 16×16×4 칸 부피 누락 QC 미달 (판독 기록)


def fig_mix2(out, repo=REPO):
    """ΔM = M(낮은 점착 비교군) − M(팔).  두 계열을 가른다 (Codex v3 재확인 SEMV3-04): 큰 NCM 자기쌍 모형 Bond number 38.4 → 384 → 1152
    (CED 로는 ×2.154 · ×3.107) ↔ 비교군의 0 아닌 CED 아홉 항 전부 ×10 · ×14.42."""
    dm = dev_delta_m(repo)
    fig, ax = plt.subplots(figsize=(12.0 * CM, 7.0 * CM))      # 12 장 그림 띠 (≈ 4.75 × 2.75 in) 에 1:1
    grids = ["16×16×4", "12×12×3", "8×8×2"]; cols = [NAVY, SKY, ORANGE]
    xs = [0.0, 1.0, 2.0, 3.6, 4.6]
    w = 0.26; rows = []
    for x0, (key, tick) in zip(xs, MIX2_LABELS):
        qc = MIX2_QC.get(key, ())
        series = "NCM-pair Bo" if key.startswith("Bo") else "All-pair CED"
        for j, (val, col) in enumerate(zip(dm[key], cols)):
            hatch = j in qc
            ax.bar(x0 + (j - 1) * w, val, w, color=col, hatch="////" if hatch else None, edgecolor="white" if hatch else col, lw=0.6,
                   label=grids[j] if key == "Bo38.4" else None)
            rows.append((f"{series} {tick}", grids[j], val, "volume-coverage check not met" if hatch else ""))
    ax.axhline(0, color=GRAY, lw=0.8)
    ax.axvline(2.8, color=LIGHT, lw=0.9, ls="--")
    ax.set_xticks(xs); ax.set_xticklabels([t for _, t in MIX2_LABELS], fontsize=11)
    tr = ax.get_xaxis_transform()
    ax.text(1.0, -0.2, "NCM-pair model Bond number", transform=tr, ha="center", va="top", fontsize=10.5, color="#333333")
    ax.text(4.1, -0.2, "all-pair CED scale", transform=tr, ha="center", va="top", fontsize=10.5, color="#333333")
    ax.set_xlim(-0.6, 5.2)
    ax.set_ylabel("ΔM (low-cohesion\ncomparator − arm)"); ax.set_ylim(-0.2, 3.4)
    _fmt(ax, ny=5)
    ax.legend(frameon=False, loc="upper left", title="bin grid", title_fontsize=10.5, fontsize=10)
    fig.tight_layout(pad=0.3)
    _save(fig, out, "F_mix2", rows=rows, header=["setting", "bin grid", "delta M = M(low-cohesion comparator) - M(setting)", "note"])


# ── F_mix3 ──────────────────────────────────────────────────────────────────
MIX3_LABELS = [("low", "low NCM–NCM\ncohesion"), ("CED10", "all-pair\nCED ×10"), ("CED14", "all-pair\nCED ×14.42")]


def fig_mix3(out, repo=REPO):
    cl = dev_cluster(repo)
    fig, ax = plt.subplots(figsize=(10.0 * CM, 6.3 * CM))      # 13 장 왼쪽 띠 (≈ 3.95 × 2.5 in) 에 1:1
    cols = [RED, SKY, NAVY]; rows = []
    for i, ((key, lab), col) in enumerate(zip(MIX3_LABELS, cols)):
        v, lo, hi = cl[key]
        ax.bar(i, v, 0.6, color=col)
        ax.errorbar(i, v, yerr=[[v - lo], [hi - v]], fmt="none", ecolor="#333333", lw=0.9, capsize=3)
        rows.append((lab.replace("\n", " "), v, lo, hi))
    ax.set_xticks(range(3)); ax.set_xticklabels([l for _, l in MIX3_LABELS], fontsize=10)
    ax.set_xlim(-0.75, 2.6)
    ax.set_ylabel("SE fraction in\nSE–SE clusters"); ax.set_ylim(0, 1.1)
    _fmt(ax, ny=5)
    fig.tight_layout(pad=0.3)
    _save(fig, out, "F_mix3", rows=rows, header=["setting", "cluster SE fraction (2nd revolution mean)", "dump-resolution low", "dump-resolution high"])


def fig_mix3_scheme(out):
    """조건부 접착일 도식 — docs/hetero_thesis.md §2-2 · Codex v3 재확인 SEMV3-05: 가정 (기하평균 결합 · 같은 접촉 면적) 과 단위 (J m⁻²) 를 그림에 적는다.
    면적당 접착일 차이일 뿐 — 군집 생존은 입자 크기만으로 정해지지 않는다."""
    fig = plt.figure(figsize=(12.2 * CM, 6.4 * CM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 12.2); ax.set_ylim(0, 6.4); ax.set_aspect("equal"); ax.axis("off")
    def pair(x, y, left, right):
        r_l, r_r = left[2], right[2]
        xl, xr = x - (r_l + 0.02), x + (r_r + 0.02)
        for cx, (lab, col, r) in ((xl, left), (xr, right)):
            ax.add_patch(Circle((cx, y), r, fc=col, ec="none"))
            ax.text(cx, y, lab, ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    A = ("A", NAVY, 0.55); S = ("S", ORANGE, 0.32)
    ax.text(6.1, 6.0, "Assumed W$_{AS}$ = 2√(γ$_A$γ$_S$); equal contact areas", ha="center", va="center", fontsize=11, color="#333333")
    ax.text(2.2, 5.15, "two A–S contacts", ha="center", va="center", fontsize=11.5, color="#333333")
    ax.text(6.6, 5.15, "one A–A + one S–S", ha="center", va="center", fontsize=11.5, color="#333333")
    pair(2.2, 4.25, A, S); pair(2.2, 2.9, A, S)
    pair(6.6, 4.25, A, A); pair(6.6, 2.9, S, S)
    ax.add_patch(FancyArrowPatch((3.5, 3.58), (5.1, 3.58), arrowstyle="-|>", mutation_scale=16, lw=1.4, color=GRAY))
    ax.text(8.4, 3.58, "A = NCM\nS = sulfide SE", ha="left", va="center", fontsize=11, color="#333333")
    ax.text(5.2, 1.75, "ΔW = 2(√γ$_A$ − √γ$_S$)² ≥ 0", ha="center", va="center", fontsize=13.5, color=NAVY, fontweight="bold")
    ax.text(8.85, 1.75, "(J m⁻²)", ha="left", va="center", fontsize=12, color=NAVY)
    ax.text(6.1, 0.95, "Conditional adhesive-work comparison.", ha="center", va="center", fontsize=10.5, color="#333333")
    ax.text(6.1, 0.42, "Contact survival is not determined by particle size alone.", ha="center", va="center", fontsize=10.5, color="#333333")
    _save(fig, out, "F_mix3_scheme")


# ── selftest ────────────────────────────────────────────────────────────────
def selftest(repo=REPO):
    repo = Path(repo)
    s = json.loads((repo / "docs/report_20261021/summary.json").read_text(encoding="utf-8"))
    assert [round(s["G1"][k]["union"], 2) for k in PS] == PORO, s["G1"]
    for vox in VGCF["vox"]:
        assert [round(s["G6"]["mean"][f"{vox}|{w}"], 2) for w in VGCF["wt"]] == VGCF["mean"][vox]
    assert [(k, round(m, 4), round(sd, 4)) for k, m, sd in s["G7"]["runs"]] == MIX1, s["G7"]["runs"]
    assert round(s["G7"]["main"]["16x4"]["Delta"], 4) == MIX1_MAIN["Delta"] and round(s["G7"]["main"]["16x4"]["SE"], 4) == MIX1_MAIN["SE"]
    t = (repo / "docs/data/ps45_r45_network_g2_20261007/README.md").read_text(encoding="utf-8")
    for v in TAU2:
        assert f"{v}" in t, v
    for v in SIG_ION:
        assert f"{v:.4f}" in t, v
    pl = json.loads((repo / "docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json").read_text(encoding="utf-8"))
    for p in PS:
        c = pl["cases"][p]["contribution_sigma_zz_pct"]
        assert tuple(round(c[k], 3) for k in ("AM–AM", "AM–SE", "SE–SE")) == LOAD[p], (p, c)
    t = (repo / "docs/data/ps45_sigmae_factor_off_20261013/README.md").read_text(encoding="utf-8")
    for a, b in zip(PS45_SIG_E, (0.390802, 0.405815, 0.402466, 0.374697, 0.467175)):
        assert f"{b}" in t and abs(a - round(b, 3)) < 1e-9
    c = (repo / "CLAUDE.md").read_text(encoding="utf-8")
    assert "1.4215 → 1.1621 → 1.0849" in c and "1.0742 → 0.9926 → 0.9908" in c
    r = (repo / "docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md").read_text(encoding="utf-8")
    assert all(x in r for x in ("54.0", "70.6", "4.47", "12.4"))
    dr = (repo / "docs/data/mixer_highbo_devrot_prelim_20261002/README.md").read_text(encoding="utf-8")
    assert all(x in dr for x in ("+0.0105", "−0.0064", "+0.0078")), "dev-rot d"
    db = (repo / "docs/data/mixer_highbo_devbo_prelim_20261003/README.md").read_text(encoding="utf-8")
    assert all(x in db for x in ("+0.827", "+0.928", "+0.988", "+1.876", "+2.432", "+3.164")), "dev-bo d"
    du = (repo / "docs/data/mixer_highbo_devu_prelim_20261006/README.md").read_text(encoding="utf-8")
    assert all(x in du for x in ("+0.239", "+0.165", "+0.103", "+0.866", "+0.484", "+0.267", "0.401 [0.143, 0.542]", "0.954 [0.875, 0.957]", "0.988 [0.981, 0.988]")), "dev-u"
    ban = json.loads((repo / "docs/reviews/claims.json").read_text(encoding="utf-8")).get("quotation_ban", [])
    pats = [q.get("pattern") if isinstance(q, dict) else q for q in ban]
    src = Path(__file__).read_text(encoding="utf-8")
    hits = [p for p in pats if p and p in src]
    assert not hits, hits
    import re
    assert not re.search(r"\b(?:LC|LH|LHx\d*|LU\d*|LB\d|LA)\b", "".join(l for _, l in MIX2_LABELS) + "".join(l for _, l in MIX3_LABELS) + "".join(l for l, _ in MIX1_GROUPS)), "arm codes in figure labels"
    # 개발 런 값 = 원 판독 JSON 에서 직접 (README 요약 반올림을 베끼지 않는다 · Codex v3 재확인 SEMV3-06)
    dm, cl = dev_delta_m(repo), dev_cluster(repo)
    assert round(dm["Bo384"][1], 3) == 0.927 and round(dm["CED14"][0], 3) == 0.865 and round(cl["low"][0], 3) == 0.400, (dm, cl)
    assert abs(dm["Bo1152"][2] - 3.163938904) < 1e-6 and abs(cl["CED10"][1] - 0.875368565) < 1e-6
    import tempfile
    OVERLAPS.clear()
    with tempfile.TemporaryDirectory() as d:
        fig_poro(d); fig_trans(d); fig_limits(d); fig_load(d); fig_vgcf(d); fig_dataset(d, repo)
        fig_mix1(d); fig_mix2(d, repo); fig_mix3(d, repo); fig_mix3_scheme(d)
        svg = {n: Path(d, f"{n}.svg").read_text(encoding="utf-8") for n in ("F_limits", "F_mix1", "F_mix2", "F_mix3", "F_mix3_scheme")}
        assert all(k in svg["F_limits"] for k in PS), "F_limits (c) composition labels"
        for n in ("F_mix1", "F_mix2", "F_mix3"):
            assert not re.search(r"\b(?:LC|LH|LHx\d*|LU\d*|LA|LB\d|L0)\b", svg[n]), f"arm code in {n}"
            assert "removed" not in svg[n] and "non-cohesive" not in svg[n], f"zero-cohesion wording in {n} (SEMV3-02)"
        assert "low NCM" in svg["F_mix1"] and "low NCM" in svg["F_mix3"], "low-cohesion comparator label"
        assert all(k in svg["F_mix2"] for k in ("38.4", "1152", "14.42", "Bo", "CED")) and "reference" not in svg["F_mix2"], "F_mix2 Bo / CED labels (SEMV3-04)"
        assert all(k in svg["F_mix3"] for k in ("CED", "14.42")), "F_mix3 CED labels"
        assert all(k in svg["F_mix3_scheme"] for k in ("Assumed", "Conditional", "J m")), "scheme assumptions (SEMV3-05)"
        assert not any(k in svg["F_mix3_scheme"] for k in ("favoured", "holds on most")), "scheme survival claim (SEMV3-05)"
        with open(Path(d, "F_mix2.csv"), encoding="utf-8") as f:
            vals = [float(r[2]) for r in list(csv.reader(f))[1:]]
        assert abs(vals[1 * 3 + 1] - dm["Bo384"][1]) < 1e-12, "F_mix2.csv must carry the JSON values"
    assert not OVERLAPS, f"overlapping text in figures: {OVERLAPS}"
    print("selftest ok — values match canonical sources and the readout JSONs · no banned strings · no arm codes · no overlapping text · labels checked")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2] if len(sys.argv) > 2 else REPO)
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "."
        repo = sys.argv[sys.argv.index("--repo") + 1] if "--repo" in sys.argv else REPO
        Path(out).mkdir(parents=True, exist_ok=True)
        fig_poro(out); fig_trans(out); fig_limits(out); fig_load(out); fig_vgcf(out)
        info = fig_dataset(out, repo)
        fig_mix1(out); fig_mix2(out, repo); fig_mix3(out, repo); fig_mix3_scheme(out)
        print("written", out, info)
