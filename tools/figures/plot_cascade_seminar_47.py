#!/usr/bin/env python3
"""Build seminar figures from the audited cascade roster and 47-row pool.

The historical v23 figures are visual references only.  This script keeps the
campaign lineage (91 compounds / 273 attempted run slots -> a versioned 141-row,
47-species snapshot) separate from the post-hoc physical gates applied inside
that 47-row pool.  It deliberately avoids a composite rank or a "winner" label.

Outputs
-------
docs/figures/cascade/cascade_seminar_pool_attrition_273_to_47.{png,pdf}
docs/figures/cascade/cascade_seminar_oxidation_transport_47.{png,pdf}
docs/figures/cascade/cascade_seminar_pareto_47.{png,pdf}
docs/figures/cascade/cascade_seminar_scorecard_47.{png,pdf}
db/properties/cascade_seminar_pool_attrition_273_to_47.csv
db/properties/cascade_seminar_oxidation_transport_47.csv
db/properties/cascade_seminar_pareto_47.csv
db/properties/cascade_seminar_scorecard_47.csv
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.figures.house_style import ELEM, INK, MUT, apply_axes  # noqa: E402

# ── 회수분(90종) 병렬 생성 shim (2026-08-14) ────────────────────────────────
#   CASCADE_SUFFIX=_v2 CASCADE_FIGDIR=docs/figures/cascade_v2 로 돌리면 정본을 안 건드리고
#   같은 그림을 회수 풀로 다시 그린다. 접미사가 비면 동작이 100% 이전과 같다.
import os as _os
_SUF = _os.environ.get("CASCADE_SUFFIX", "")
_FIGDIR = _os.environ.get("CASCADE_FIGDIR", "")
def _csv(name):
    """db/properties 상대 경로에 접미사를 끼운다. 'a/b/x.csv' → 'a/b/x_v2.csv'."""
    if not _SUF: return name
    root, ext = _os.path.splitext(name)
    cand = root + _SUF + ext
    return cand if _os.path.exists(cand) else name



PROP = ROOT / "db" / "properties"
FIG = ROOT / "docs" / "figures" / "cascade"
FUNNEL = PROP / "cascade_screening_funnel.json"
LITRANSPORT = PROP / _csv("cascade_v23_litransport.csv")

HOST_OX_V = 2.14
G4_TRANSPORT_CUT = 0.30
G4_BLOCKING_CUT = 0.60
RAISED = {"B2O3", "Cr2O3", "Ga2O3", "In2O3", "Sc2O3", "Y2O3"}
DFT_DEEP = {"B2O3", "Nd2O3"}
EXPECTED_CONDITIONAL_PARETO = {"WO3", "SiO2", "CaF2", "CaO"}

# Exact 91-compound roster from
# origin/claude/unified-2026-05-15:tools/doping/master_batch_273.sh
# (branch snapshot 411194a66df90c91711aec3fcaab3be0d40c6899).
ROSTER_FAMILIES = [
    (
        "Oxides",
        [
            "Li2O", "Na2O", "Cu2O", "Ag2O", "MgO", "ZnO", "CaO", "SrO", "BaO",
            "MnO", "CoO", "NiO", "Al2O3", "Sc2O3", "Y2O3", "La2O3", "Nd2O3",
            "Sm2O3", "Gd2O3", "Ga2O3", "In2O3", "Cr2O3", "Fe2O3", "B2O3",
            "SiO2", "GeO2", "SnO2", "TiO2", "ZrO2", "HfO2", "V2O5", "Nb2O5",
            "Ta2O5", "Sb2O5", "CrO3", "MoO3", "WO3",
        ],
    ),
    ("Fluorides", ["LiF", "MgF2", "CaF2", "AlF3", "YF3", "LaF3", "NdF3", "ZrF4", "TiF4", "ScF3"]),
    (
        "Chlorides",
        [
            "LiCl", "MgCl2", "CaCl2", "SrCl2", "BaCl2", "AlCl3", "GaCl3", "FeCl3",
            "CrCl3", "YCl3", "LaCl3", "NdCl3", "SmCl3", "ScCl3", "ZrCl4", "HfCl4",
            "TiCl4", "NbCl5", "TaCl5",
        ],
    ),
    ("Bromides", ["LiBr", "MgBr2", "CaBr2", "AlBr3", "ZrBr4"]),
    ("Iodides", ["LiI", "NaI", "MgI2", "AlI3"]),
    ("Nitrides", ["Li3N", "Mg3N2", "Ca3N2", "AlN", "GaN"]),
    ("Sulfides", ["Li2S", "Na2S", "MgS", "CaS", "Al2S3", "Ga2S3", "SiS2", "GeS2", "SnS2", "As2S3", "Sb2S3"]),
]

FAMILY_COLORS = {
    "Oxides": ELEM["O"],
    "Fluorides": ELEM["B"],
    "Chlorides": "#9ca3af",
    "Bromides": "#a78bfa",
    "Iodides": "#c4b5fd",
    "Nitrides": ELEM["N"],
    "Sulfides": ELEM["S"],
}

STAGE_ORDER = {"PASS": 0, "G4": 1, "G3": 2, "G2": 3, "G1": 4}
STAGE_COLOR = {
    "PASS": ELEM["Li"],
    "G4": ELEM["S"],
    "G3": MUT,
    "G2": ELEM["O"],
    "G1": ELEM["P"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(line for line in fh if not line.startswith("#")))


def formula_label(formula: str) -> str:
    """Return a compact mathtext chemical formula, e.g. Sc2O3 -> Sc$_2$O$_3$."""
    return re.sub(r"(\d+)", r"$_{\1}$", formula)


def first_stop(row: dict) -> str:
    failed = set(row["gates_failed"])
    for gate in ("G1", "G2", "G3", "G4"):
        if gate in failed:
            return gate
    return "PASS"


def favorable_percentile(values: list[float], *, higher_is_better: bool) -> np.ndarray:
    """Empirical within-pool percentile; tied values receive identical mean ranks."""
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    if n <= 1:
        return np.full(n, 0.5)
    order = np.argsort(arr, kind="mergesort")
    ranks = np.empty(n, dtype=float)
    i = 0
    while i < n:
        j = i + 1
        while j < n and np.isclose(arr[order[j]], arr[order[i]], rtol=0, atol=1e-12):
            j += 1
        mean_rank = 0.5 * (i + j - 1)
        ranks[order[i:j]] = mean_rank / (n - 1)
        i = j
    return ranks if higher_is_better else 1.0 - ranks


def load_rows() -> list[dict]:
    data = json.loads(FUNNEL.read_text(encoding="utf-8"))
    rows = [dict(row) for row in data["pool"]]
    if len(rows) != 47 or len({row["dopant"] for row in rows}) != 47:
        raise AssertionError("canonical cascade pool must contain 47 unique dopants")

    x005 = {}
    for row in read_csv(LITRANSPORT):
        dopant, _, level = row["_dir"].rpartition("_x")
        if level == "005":
            x005[dopant] = {
                "bvs_x005": float(row["bvs_li_proxy_score"]),
                "blocking_x005": float(row["tier2_dopant_blocking_fraction"]),
            }

    for row in rows:
        if row["dopant"] not in x005:
            raise AssertionError(f"missing x005 BVSE row for {row['dopant']}")
        row.update(x005[row["dopant"]])
        if not np.isclose(row["blocking"], row["blocking_x005"], atol=1e-12):
            raise AssertionError(f"funnel/litransport blocking mismatch for {row['dopant']}")
        row["first_stop"] = first_stop(row)
        row["pass_G1_G4"] = row["first_stop"] == "PASS"
        row["dft_deep"] = row["dopant"] in DFT_DEEP

    counts = {stage: sum(row["first_stop"] == stage for row in rows) for stage in STAGE_ORDER}
    expected = {"PASS": 11, "G4": 14, "G3": 18, "G2": 4, "G1": 0}
    if counts != expected:
        raise AssertionError(f"unexpected representative-order stage counts: {counts}")

    raised = {row["dopant"] for row in rows if row["ox_V"] > HOST_OX_V + 0.01}
    if raised != RAISED:
        raise AssertionError(f"unexpected oxidation-raising set: {sorted(raised)}")
    if any(row["pass_G1_G4"] for row in rows if row["dopant"] in RAISED):
        raise AssertionError("all six oxidation-raising candidates must stop at G4")
    return rows


def add_percentile_columns(rows: list[dict]) -> None:
    specs = [
        ("stable_pct", "de", False),
        ("window_pct", "window_V", True),
        ("oxidation_pct", "ox_V", True),
        ("bvs_pct", "bvs_x005", True),
        ("blocking_pct", "blocking", False),
        ("soft_pct", "E_GPa", False),
        ("ductile_pct", "GoverB", False),
    ]
    for out, key, higher in specs:
        vals = favorable_percentile([float(row[key]) for row in rows], higher_is_better=higher)
        for row, value in zip(rows, vals):
            row[out] = float(value)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def save(fig: plt.Figure, stem: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{stem}.png", dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(FIG / f"{stem}.pdf", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def build_roster(rows: list[dict]) -> list[dict]:
    retained = {row["dopant"] for row in rows}
    roster = []
    for family, compounds in ROSTER_FAMILIES:
        phase = "Phase 1A" if family == "Oxides" else "Phase 1B"
        for candidate in compounds:
            complete = candidate in retained
            roster.append(
                {
                    "candidate": candidate,
                    "family": family,
                    "campaign_phase": phase,
                    "nominal_levels": "x002|x005|x010",
                    "attempted_executions": 3,
                    "ingested_in_2026_06_25_snapshot": int(complete),
                    "included_in_47_pool": int(complete),
                    "pool_status": "versioned_47_snapshot" if complete else "not_ingested_in_canonical_snapshot",
                    "reason": (
                        "Present in the 2026-06-25 141-row champion snapshot"
                        if complete
                        else "Absent from the versioned canonical table; individual cause unverified and not a physical rejection"
                    ),
                    "roster_source": "origin/claude/unified-2026-05-15:tools/doping/master_batch_273.sh",
                    "roster_source_snapshot": "411194a66df90c91711aec3fcaab3be0d40c6899",
                }
            )
    if len(roster) != 91 or len({row["candidate"] for row in roster}) != 91:
        raise AssertionError("pre-pool roster must contain 91 unique compounds")
    if sum(row["attempted_executions"] for row in roster) != 273:
        raise AssertionError("pre-pool roster must map to 273 campaign run slots")
    if sum(row["included_in_47_pool"] for row in roster) != 47:
        raise AssertionError("versioned canonical subset must contain 47 compounds")
    observed = {row["candidate"] for row in roster if row["included_in_47_pool"]}
    if observed != retained:
        raise AssertionError(f"91-roster/47-pool mismatch: {sorted(observed ^ retained)}")
    return roster


def plot_pool_attrition(rows: list[dict]) -> None:
    roster = build_roster(rows)
    families = [family for family, _ in ROSTER_FAMILIES]
    total = [sum(row["family"] == family for row in roster) for family in families]
    complete = [sum(row["family"] == family and row["included_in_47_pool"] for row in roster) for family in families]
    incomplete = [a - b for a, b in zip(total, complete)]

    fig, (ax, ax_text) = plt.subplots(1, 2, figsize=(12, 9), gridspec_kw={"width_ratios": [1.45, 1.0], "wspace": 0.20})
    y = np.arange(len(families))
    ax.barh(y, complete, height=0.62, color=[FAMILY_COLORS[f] for f in families], label="In canonical snapshot")
    ax.barh(y, incomplete, left=complete, height=0.62, color="#e5e7eb", edgecolor="white", hatch="///", label="Not ingested")
    ax.set_yticks(y)
    ax.set_yticklabels(families, fontsize=11, color=INK)
    ax.invert_yaxis()
    for yi, n_total, n_complete in zip(y, total, complete):
        ax.text(n_total + 0.6, yi, f"{n_complete}/{n_total}", va="center", fontsize=9.5, color=INK, fontweight="bold")
    apply_axes(ax, xlabel="Number of curated compounds", title="Versioned snapshot coverage by chemical family", fontsize=11)
    ax.set_xlim(0, 41)
    ax.grid(axis="x", color="#d1d5db", lw=0.7, alpha=0.65)
    ax.legend(
        handles=[
            Patch(facecolor=ELEM["Li"], label="Present in canonical 47 snapshot"),
            Patch(facecolor="#e5e7eb", edgecolor="white", hatch="///", label="Not ingested into canonical table"),
        ],
        loc="lower right",
        frameon=False,
        fontsize=8.8,
    )

    ax_text.axis("off")
    ax_text.text(0.50, 0.87, "91", ha="center", va="center", fontsize=42, color=INK, fontweight="bold")
    ax_text.text(0.50, 0.80, "curated compounds", ha="center", fontsize=13, color=MUT)
    ax_text.text(0.50, 0.70, "$\\times$ 3 campaign labels", ha="center", fontsize=16, color=INK)
    ax_text.text(0.50, 0.61, "273", ha="center", va="center", fontsize=42, color=ELEM["B"], fontweight="bold")
    ax_text.text(0.50, 0.54, "campaign run slots", ha="center", fontsize=13, color=MUT)
    ax_text.annotate("", xy=(0.50, 0.40), xytext=(0.50, 0.49), arrowprops={"arrowstyle": "-|>", "lw": 1.8, "color": MUT})
    ax_text.text(0.50, 0.35, "2026-06-25 versioned snapshot", ha="center", fontsize=13, color=INK, fontweight="bold")
    ax_text.text(0.25, 0.20, "47", ha="center", fontsize=34, color=ELEM["Li"], fontweight="bold")
    ax_text.text(0.25, 0.135, "species\n141 records", ha="center", fontsize=10.5, color=INK)
    ax_text.text(0.75, 0.20, "44", ha="center", fontsize=34, color=MUT, fontweight="bold")
    ax_text.text(0.75, 0.135, "species\nnot ingested", ha="center", fontsize=10.5, color=INK)
    ax_text.text(0.50, 0.045, "Post-hoc G1-G5 audit starts here: 47", ha="center", fontsize=11, color=ELEM["S"], fontweight="bold")

    fig.suptitle("The canonical 47 is a versioned snapshot, not a 273-run funnel result", fontsize=17, color=INK, y=0.96)
    fig.text(0.5, 0.915, "273 counts attempted run slots; the committed 2026-06-25 table contains the first 141 rows = 47 species x 3 labels.", ha="center", fontsize=10.2, color=INK)
    fig.text(
        0.5,
        0.025,
        "Later notes say 273/273 completed, but the unified 273-row table is not versioned. Missing from this snapshot does not mean physically rejected.",
        ha="center",
        fontsize=8.8,
        color=MUT,
    )
    fig.subplots_adjust(top=0.84, bottom=0.10, left=0.10, right=0.96)
    save(fig, "cascade_seminar_pool_attrition_273_to_47")

    write_csv(PROP / "cascade_seminar_pool_attrition_273_to_47.csv", list(roster[0]), roster)


def plot_scorecard(rows: list[dict]) -> None:
    ordered = sorted(rows, key=lambda row: row["dopant"])
    metrics = [
        ("stable_pct", "Mean $\\Delta E$\n$\\downarrow$"),
        ("window_pct", "Window\n$\\uparrow$"),
        ("oxidation_pct", "$V_{ox}$\n$\\uparrow$"),
        ("bvs_pct", "BVSE\n$\\uparrow$"),
        ("blocking_pct", "Blocking\n$\\downarrow$"),
        ("soft_pct", "$E$\n$\\downarrow$"),
        ("ductile_pct", "$G/B$\n$\\downarrow$"),
    ]
    cmap = LinearSegmentedColormap.from_list("cascade_percentile", ["#f3f4f6", "#bfdbfe", ELEM["Li"], "#134e4a"])

    fig, axes = plt.subplots(1, 2, figsize=(12, 9), gridspec_kw={"wspace": 0.38})
    splits = [ordered[:24], ordered[24:]]
    image = None
    for ax, block in zip(axes, splits):
        matrix = np.asarray([[row[key] for key, _ in metrics] for row in block], dtype=float)
        image = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto", interpolation="nearest")
        ax.set_xticks(range(len(metrics)))
        ax.set_xticklabels([label for _, label in metrics], fontsize=8.4, color=INK)
        ax.tick_params(axis="x", length=0, pad=7)
        ax.set_yticks(range(len(block)))
        labels = [formula_label(row["dopant"]) + ("$^{\\dagger}$" if row["dft_deep"] else "") for row in block]
        ax.set_yticklabels(labels, fontsize=7.7, color=INK)
        ax.tick_params(axis="y", length=0, pad=4)

        for yi, row in enumerate(block):
            stage = row["first_stop"]
            ax.add_patch(Rectangle((len(metrics) - 0.02, yi - 0.5), 0.82, 1.0, facecolor=STAGE_COLOR[stage], edgecolor="white", linewidth=0.8, clip_on=False))
            ax.text(len(metrics) + 0.39, yi, stage, ha="center", va="center", fontsize=6.2, color="white", fontweight="bold", clip_on=False)
        ax.text(len(metrics) + 0.39, -1.18, "First\nstop", ha="center", va="center", fontsize=7.0, color=INK, clip_on=False)
        ax.set_xlim(-0.5, len(metrics) + 0.82)
        for spine in ax.spines.values():
            spine.set_visible(False)

    fig.suptitle("The 47 candidates trade strengths across axes", fontsize=17, color=INK, y=0.965)
    fig.text(0.5, 0.925, "Alphabetical order; within-pool favorable percentiles; no composite score or winner.", ha="center", fontsize=9.5, color=MUT)
    legend = [
        Patch(facecolor=STAGE_COLOR["PASS"], label="Retained through G4 (11)"),
        Patch(facecolor=STAGE_COLOR["G4"], label="Stopped at G4 (14)"),
        Patch(facecolor=STAGE_COLOR["G3"], label="Stopped at G3 (18)"),
        Patch(facecolor=STAGE_COLOR["G2"], label="Stopped at G2 (4)"),
    ]
    fig.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, 0.895), ncol=4, frameon=False, fontsize=8.7)
    if image is not None:
        cax = fig.add_axes([0.25, 0.075, 0.50, 0.018])
        cbar = fig.colorbar(image, cax=cax, orientation="horizontal")
        cbar.set_label("Within-pool favorable percentile (descriptive only)", fontsize=8.5, color=INK)
        cbar.ax.tick_params(colors=MUT, labelsize=7.5)
        cbar.outline.set_visible(False)
    fig.text(0.5, 0.025, "$^{\\dagger}$ Existing deep DFT: B$_2$O$_3$ and Nd$_2$O$_3$ (2/47). G4 is heuristic; mechanics are roster-relative.", ha="center", fontsize=8.2, color=MUT)
    fig.subplots_adjust(top=0.84, bottom=0.12, left=0.08, right=0.94)
    save(fig, "cascade_seminar_scorecard_47")

    out_rows = []
    for index, row in enumerate(ordered, start=1):
        out_rows.append(
            {
                "display_order_alphabetical": index,
                "dopant": row["dopant"],
                "group": row["group"],
                "first_stop_posthoc_G1_G4": row["first_stop"],
                "pass_G1_G4": int(row["pass_G1_G4"]),
                "dft_deep": int(row["dft_deep"]),
                "de_relative_eV_UMA": row["de"],
                "window_V_MP_grand_potential": row["window_V"],
                "oxidation_onset_V_MP_grand_potential": row["ox_V"],
                "bvs_li_proxy_score_x005_nominal": row["bvs_x005"],
                "blocking_fraction_x005_nominal": row["blocking"],
                "E_GPa_UMA_relative": row["E_GPa"],
                "GoverB_UMA_relative": row["GoverB"],
                "stability_favorable_percentile": row["stable_pct"],
                "window_favorable_percentile": row["window_pct"],
                "oxidation_favorable_percentile": row["oxidation_pct"],
                "bvs_favorable_percentile": row["bvs_pct"],
                "blocking_favorable_percentile": row["blocking_pct"],
                "softness_favorable_percentile": row["soft_pct"],
                "ductility_favorable_percentile": row["ductile_pct"],
            }
        )
    write_csv(PROP / "cascade_seminar_scorecard_47.csv", list(out_rows[0]), out_rows)


def bvs_raw_cut(rows: list[dict]) -> float:
    values = [row["bvs_x005"] for row in rows]
    scaled_cut = (G4_TRANSPORT_CUT - 0.10) / 0.90
    return min(values) + scaled_cut * (max(values) - min(values))


def plot_oxidation_transport(rows: list[dict]) -> None:
    selected = sorted((row for row in rows if row["dopant"] in RAISED), key=lambda row: (-row["ox_V"], row["dopant"]))
    raw_cut = bvs_raw_cut(rows)
    b2o3 = next(row for row in selected if row["dopant"] == "B2O3")
    if not (b2o3["bvs_x005"] < raw_cut and b2o3["blocking"] < G4_BLOCKING_CUT):
        raise AssertionError("B2O3 must be the BVS-only failure among the oxidation-raising six")
    for row in selected:
        if row["dopant"] != "B2O3" and not (row["bvs_x005"] > raw_cut and row["blocking"] >= G4_BLOCKING_CUT):
            raise AssertionError(f"unexpected G4 failure decomposition for {row['dopant']}")

    fig, (ax, ax_note) = plt.subplots(1, 2, figsize=(12, 9), gridspec_kw={"width_ratios": [3.3, 1.0], "wspace": 0.05})
    background = [row for row in rows if row["dopant"] not in RAISED]
    retained = [row for row in background if row["pass_G1_G4"]]
    stopped = [row for row in background if not row["pass_G1_G4"]]
    ax.scatter([row["ox_V"] for row in stopped], [row["bvs_x005"] for row in stopped], s=42, color="#d1d5db", edgecolor="white", linewidth=0.5, alpha=0.75, zorder=1)
    ax.scatter([row["ox_V"] for row in retained], [row["bvs_x005"] for row in retained], s=58, marker="s", color=ELEM["Li"], edgecolor="white", linewidth=0.7, alpha=0.92, zorder=2)

    for row in selected:
        blocking_fail = row["blocking"] >= G4_BLOCKING_CUT
        marker = "X" if blocking_fail else "D"
        color = ELEM["S"] if blocking_fail else ELEM["B"]
        ax.scatter(row["ox_V"], row["bvs_x005"], s=125, marker=marker, color=color, edgecolor="white", linewidth=0.8, zorder=4)

    offsets = {
        "B2O3": (-44, -21), "Cr2O3": (8, 5), "Ga2O3": (8, -8),
        "In2O3": (8, 3), "Sc2O3": (-45, 7), "Y2O3": (8, -5),
    }
    for row in selected:
        ax.annotate(formula_label(row["dopant"]), (row["ox_V"], row["bvs_x005"]), xytext=offsets[row["dopant"]], textcoords="offset points", fontsize=9, color=INK, fontweight="bold")

    ax.axvline(HOST_OX_V, color=MUT, ls="--", lw=1.4)
    ax.axhline(raw_cut, color=ELEM["Li"], ls="--", lw=1.4)
    ax.text(HOST_OX_V + 0.006, 0.928, "Host onset = 2.14 V", fontsize=8.5, color=MUT, rotation=90, va="top")
    ax.text(1.81, raw_cut + 0.002, f"BVS-equivalent cut = {raw_cut:.3f}", fontsize=8.5, color=ELEM["Li"], va="bottom")
    apply_axes(ax, xlabel="Oxidation onset, $V_{ox}$ (V vs Li/Li$^+$)", ylabel="BVSE Li-path proxy at x005 (raw score)", title="Six oxidation-raising candidates reach the same G4 stop", fontsize=11)
    ax.set_xlim(1.76, 2.42)
    ax.set_ylim(0.812, 0.936)
    ax.grid(color="#d1d5db", lw=0.7, alpha=0.60)
    ax.legend(
        handles=[
            Line2D([0], [0], marker="s", color="none", markerfacecolor=ELEM["Li"], markeredgecolor="white", markersize=8, label="Retained through G4"),
            Line2D([0], [0], marker="o", color="none", markerfacecolor="#d1d5db", markeredgecolor="white", markersize=8, label="Other roster candidates"),
            Line2D([0], [0], marker="X", color="none", markerfacecolor=ELEM["S"], markeredgecolor="white", markersize=9, label="Oxidation gain; blocking failure"),
            Line2D([0], [0], marker="D", color="none", markerfacecolor=ELEM["B"], markeredgecolor="white", markersize=8, label="Oxidation gain; BVS-only failure"),
        ],
        loc="lower left",
        frameon=False,
        fontsize=8.2,
    )

    ax_note.axis("off")
    ax_note.text(0.50, 0.78, "6 / 6", ha="center", fontsize=34, color=ELEM["O"], fontweight="bold")
    ax_note.text(0.50, 0.70, "above host onset\nfail G4", ha="center", fontsize=12, color=INK, linespacing=1.35)
    ax_note.text(0.50, 0.49, "5", ha="center", fontsize=28, color=ELEM["S"], fontweight="bold")
    ax_note.text(0.50, 0.43, "blocking failures", ha="center", fontsize=10.5, color=INK)
    ax_note.text(0.50, 0.28, "1", ha="center", fontsize=28, color=ELEM["B"], fontweight="bold")
    ax_note.text(0.50, 0.22, "BVS-only failure\n(B$_2$O$_3$)", ha="center", fontsize=10.5, color=INK)
    ax_note.text(0.50, 0.07, "Static pathway heuristic\n$\\ne$ conductivity", ha="center", fontsize=9.5, color=MUT)

    fig.suptitle("Oxidation gains do not survive the pathway gate", fontsize=18, color=INK, y=0.96)
    fig.text(0.5, 0.025, "G4 = transport_norm > 0.30 AND blocking < 0.60. Oxidation: MP grand-potential onset; pathway: static BVSE/geometric proxy.", ha="center", fontsize=8.6, color=MUT)
    fig.subplots_adjust(top=0.87, bottom=0.11, left=0.10, right=0.96)
    save(fig, "cascade_seminar_oxidation_transport_47")

    out_rows = []
    for row in selected:
        blocking_fail = row["blocking"] >= G4_BLOCKING_CUT
        out_rows.append(
            {
                "dopant": row["dopant"],
                "oxidation_onset_V_MP_grand_potential": row["ox_V"],
                "host_oxidation_onset_V": HOST_OX_V,
                "delta_oxidation_vs_host_V": row["ox_V"] - HOST_OX_V,
                "bvs_li_proxy_score_x005_nominal": row["bvs_x005"],
                "bvs_equivalent_G4_cut": raw_cut,
                "transport_norm_BVSE_derived": row["transport_norm"],
                "blocking_fraction_x005_nominal": row["blocking"],
                "G4_pass": int(row["pass_G1_G4"]),
                "G4_fail_mode": "blocking_cut" if blocking_fail else "bvs_branch_cut",
                "dft_deep": int(row["dft_deep"]),
            }
        )
    write_csv(PROP / "cascade_seminar_oxidation_transport_47.csv", list(out_rows[0]), out_rows)


def conditional_pareto_flags(rows: list[dict]) -> dict[str, bool]:
    retained = [row for row in rows if row["pass_G1_G4"]]
    flags = {row["dopant"]: False for row in rows}
    for row in retained:
        dominated = False
        for other in retained:
            weakly_better = other["de"] <= row["de"] and other["transport_norm"] >= row["transport_norm"]
            strictly_better = other["de"] < row["de"] or other["transport_norm"] > row["transport_norm"]
            if weakly_better and strictly_better:
                dominated = True
                break
        flags[row["dopant"]] = not dominated
    front = {dopant for dopant, value in flags.items() if value}
    if front != EXPECTED_CONDITIONAL_PARETO:
        raise AssertionError(f"unexpected conditional Pareto set: {sorted(front)}")
    return flags


def plot_pareto(rows: list[dict]) -> None:
    flags = conditional_pareto_flags(rows)
    retained = [row for row in rows if row["pass_G1_G4"]]
    others = [row for row in rows if not row["pass_G1_G4"]]
    front = sorted((row for row in retained if flags[row["dopant"]]), key=lambda row: row["de"])

    fig, (ax, ax_note) = plt.subplots(1, 2, figsize=(12, 9), gridspec_kw={"width_ratios": [3.35, 1.0], "wspace": 0.08})
    ax.scatter([row["de"] for row in others], [row["transport_norm"] for row in others], s=44, color="#d1d5db", edgecolor="white", linewidth=0.5, alpha=0.72, zorder=1)
    ax.scatter([row["de"] for row in retained], [row["transport_norm"] for row in retained], s=78, marker="s", color=ELEM["Li"], edgecolor="white", linewidth=0.8, zorder=2)
    ax.plot([row["de"] for row in front], [row["transport_norm"] for row in front], color=INK, ls="--", lw=1.3, alpha=0.75, zorder=2)
    ax.scatter([row["de"] for row in front], [row["transport_norm"] for row in front], s=145, marker="s", color=ELEM["Li"], edgecolor=INK, linewidth=1.8, zorder=4)

    offsets = {"WO3": (8, 8), "SiO2": (8, -14), "CaF2": (8, 8), "CaO": (8, -14)}
    for row in front:
        ax.annotate(formula_label(row["dopant"]), (row["de"], row["transport_norm"]), xytext=offsets[row["dopant"]], textcoords="offset points", fontsize=9.5, color=INK, fontweight="bold")

    apply_axes(ax, xlabel="Mean relative $\\Delta E$ (eV; lower is favored, UMA)", ylabel="BVSE transport_norm at x005 (higher is favored)", title="Conditional 2D Pareto front within the 11 retained candidates", fontsize=11)
    ax.set_xlim(min(row["de"] for row in rows) - 0.05, max(row["de"] for row in rows) + 0.05)
    ax.set_ylim(0.0, 1.05)
    ax.grid(color="#d1d5db", lw=0.7, alpha=0.60)
    ax.legend(
        handles=[
            Line2D([0], [0], marker="o", color="none", markerfacecolor="#d1d5db", markeredgecolor="white", markersize=8, label="Stopped before/at G4"),
            Line2D([0], [0], marker="s", color="none", markerfacecolor=ELEM["Li"], markeredgecolor="white", markersize=8, label="Retained through G4 (11)"),
            Line2D([0], [0], marker="s", color="none", markerfacecolor=ELEM["Li"], markeredgecolor=INK, markeredgewidth=1.6, markersize=9, label="Conditional Pareto set (4)"),
        ],
        loc="lower left",
        frameon=False,
        fontsize=8.6,
    )

    ax_note.axis("off")
    ax_note.text(0.50, 0.79, "11 $\\rightarrow$ 4", ha="center", fontsize=29, color=INK, fontweight="bold")
    ax_note.text(0.50, 0.70, "non-dominated\ntrade-off options", ha="center", fontsize=11.5, color=MUT)
    y0 = 0.52
    for idx, name in enumerate(["WO3", "SiO2", "CaF2", "CaO"]):
        ax_note.text(0.50, y0 - idx * 0.08, formula_label(name), ha="center", fontsize=14, color=ELEM["Li"], fontweight="bold")
    ax_note.text(0.50, 0.13, "All 11 share\n$V_{ox}$ = 2.14 V", ha="center", fontsize=11, color=INK)
    ax_note.text(0.50, 0.035, "Axis-dependent;\nnot a winner set", ha="center", fontsize=9.5, color=MUT)

    fig.suptitle("No single candidate dominates after G1-G4", fontsize=18, color=INK, y=0.96)
    fig.text(0.5, 0.025, "Conditional on the post-hoc G1-G4 view. G4 is heuristic; existing deep DFT (B$_2$O$_3$, Nd$_2$O$_3$) is outside this 11-candidate set.", ha="center", fontsize=8.5, color=MUT)
    fig.subplots_adjust(top=0.87, bottom=0.11, left=0.10, right=0.96)
    save(fig, "cascade_seminar_pareto_47")

    out_rows = []
    for row in sorted(rows, key=lambda item: (not item["pass_G1_G4"], item["dopant"])):
        out_rows.append(
            {
                "dopant": row["dopant"],
                "group": row["group"],
                "de_relative_eV_UMA": row["de"],
                "transport_norm_BVSE_derived": row["transport_norm"],
                "oxidation_onset_V_MP_grand_potential": row["ox_V"],
                "blocking_fraction_x005_nominal": row["blocking"],
                "retained_through_G4": int(row["pass_G1_G4"]),
                "pareto_2d_conditional_within_retained_11": int(flags[row["dopant"]]),
                "first_stop_posthoc_G1_G4": row["first_stop"],
                "dft_deep": int(row["dft_deep"]),
            }
        )
    write_csv(PROP / "cascade_seminar_pareto_47.csv", list(out_rows[0]), out_rows)


def main() -> None:
    rows = load_rows()
    add_percentile_columns(rows)
    plot_pool_attrition(rows)
    plot_oxidation_transport(rows)
    plot_pareto(rows)
    plot_scorecard(rows)
    print("PASS: 91 curated compounds x 3 campaign labels = 273 campaign run slots")
    print("PASS: 47-species / 141-row versioned snapshot; 44 later-roster species not ingested")
    print("PASS: representative-order counts = 47 -> 43 -> 25 -> 11")
    print("PASS: six oxidation-raising candidates, 0/6 pass G4")
    print("PASS: conditional Pareto set = WO3, SiO2, CaF2, CaO")


if __name__ == "__main__":
    main()
