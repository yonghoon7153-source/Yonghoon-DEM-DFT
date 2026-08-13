#!/usr/bin/env python3
"""Build the fail-closed Cascade audit figures and their Origin-ready CSVs.

This is deliberately not a 90-species leaderboard builder.  The recovered
90-species pool has not yet been re-ranked with a single approved G3/G4
contract.  The outputs here expose what is verified now: campaign lineage,
phase-set sensitivity, the historical G4 construction, post-hoc interface
axes, and the present ML validation boundary.
"""

from __future__ import annotations

import csv
import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools.figures.house_style import INK, MUT  # noqa: E402

DB = ROOT / "db" / "properties"
FIG = ROOT / "docs" / "figures" / "cascade"
PINNED_SOURCE_COMMIT = "9abe5105cacafa22ab3e185f09e2a4c37118b9a9"
RECOVERED_REF = PINNED_SOURCE_COMMIT
RECOVERED_GP = "db/properties/oxidation_stability_cascade_v2.json"
RECOVERED_POOL = "db/properties/cascade_v23_all.csv"
HIST_GP = "db/properties/oxidation_stability_cascade.json"
RECOVERED_DERIVED = [
    "db/properties/cascade_v23_champions_v2.csv",
    "db/properties/cascade_v23_litransport_v2.csv",
    "db/properties/oxidation_stability_cascade_v2.csv",
    # ⛔ 2026-08-14 (Codex Round-3 P0-2) — ranked_v2 를 뺐다. **어느 패널도 안 읽는다.**
    #   그런데 여기 있었기 때문에 Na2S 정정으로 그 파일만 뒤 커밋 산출물이 되자
    #   "top-level source_commit 은 9abe5105 인데 한 파일만 922332c0" 이라는 mixed pin 이
    #   생겼고, --materialize-recovered 는 9abe blob 을 읽어 922 해시를 기대해 실패했다.
    #   다운로드 artifact 로서의 지위는 원장(cascade_audit_manifest.json)이 관리한다 —
    #   거기엔 artifact 별 source_commit·derived_from·override_reason 이 있다.
]

# These are hashes of bytes committed at PINNED_SOURCE_COMMIT.  The generator
# must fail before reading or materializing a moving or silently changed input.
EXPECTED_SOURCE = {
    RECOVERED_GP: ("9ef15dcb83de7f1cd08b4fca57ec3610eb6947cc7a4aca865d53c95c9388cca8", 134513),
    RECOVERED_POOL: ("a9e37f31ecf017bad6dd456b624c6af96252644d67aae6ef4dc51e1ca06eb3ba", 1436260),
    HIST_GP: ("70b269c254f9001c1e7d070d7d884f4b5a5290483a07a4dffe6f65bd3ffbbba8", 71306),
    "db/properties/cascade_v23_champions_v2.csv": ("15114e95ed90c62c51cc4917245f8abef3db827ebf7853b88cf36d5333b7852d", 57541),
    "db/properties/cascade_v23_litransport_v2.csv": ("113b2466b8a4099bc829976ae0071eab7f52f5d64ea13950e6928789546aa2f9", 22903),
    "db/properties/oxidation_stability_cascade_v2.csv": ("2f351cdaedee8b1504efb56fcbb975ee1b5fe2ad35f049e9c2ed7dddde0f06e2", 4456),
}
#: pin 이동 기록 — 이제 **원장**(cascade_audit_manifest.json)의 artifact 별
#: source_commit·derived_from·override_reason 이 정본이다. 여기는 이력용 사본.
PIN_OVERRIDES = [
    {"path": "db/properties/cascade_v23_ranked_v2.csv",
     "was": "2c930ebbd4715d4afe6168a6b349ffef0a1b1b56c622d14962659e04eb637d4f",
     "now": "1995ce8d95d746db61bbc23d5804acd0f0a9784851525d4b913cb042077344f9",
     "on": "2026-08-14", "by": "commit 922332c0",
     "why": ("Na2S ductility retraction — Na2S_x100 has B_hill = -36.27 GPa (failed elastic "
             "calculation) and was averaged in, producing a false B/G = 2.50. "
             "plot_cascade_insights.py now drops non-positive Hill moduli; Na2S is B/G 1.22. "
             "Only unphysical row in 270; the five audit panels do not read this column.")},
]

BLUE = "#2563eb"
TEAL = "#0d9488"
AMBER = "#d97706"
RED = "#be123c"
GREEN = "#15803d"
PALE = "#e5e7eb"


def _git_bytes(path: str) -> bytes:
    data = subprocess.check_output(
        ["git", "show", f"{RECOVERED_REF}:{path}"], cwd=ROOT
    )
    expected = EXPECTED_SOURCE.get(path)
    if expected and (_sha(data), len(data)) != expected:
        raise RuntimeError(
            f"Pinned source changed for {path}: "
            f"sha256={_sha(data)} bytes={len(data)} expected={expected}"
        )
    return data


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _csv_bytes(path: str) -> list[dict[str, str]]:
    text = _git_bytes(path).decode("utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


def _local_csv(path: Path) -> list[dict[str, str]]:
    lines = [
        line
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line and not line.startswith("#")
    ]
    return list(csv.DictReader(lines))


def _write_csv(name: str, rows: list[dict], fields: list[str]) -> Path:
    out = DB / name
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return out


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    face = "arialbd.ttf" if bold else "arial.ttf"
    path = Path("C:/Windows/Fonts") / face
    return ImageFont.truetype(str(path), size=size)


def _canvas(title: str, subtitle: str = "") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (1800, 940), "white")
    draw = ImageDraw.Draw(image)
    draw.text((70, 42), title, fill=INK, font=_font(44, True))
    if subtitle:
        draw.text((72, 100), subtitle, fill=MUT, font=_font(24))
    return image, draw


def _panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str) -> None:
    draw.rounded_rectangle(box, radius=22, fill="#f8fafc", outline="#d1d5db", width=2)
    draw.text((box[0] + 28, box[1] + 22), title, fill=INK, font=_font(29, True))


def _save(image: Image.Image, name: str) -> Path:
    out = FIG / name
    image.save(out, dpi=(300, 300), optimize=True)
    return out


def _read_recovered() -> tuple[dict, list[dict], dict]:
    gp_bytes = _git_bytes(RECOVERED_GP)
    pool_bytes = _git_bytes(RECOVERED_POOL)
    hist_bytes = _git_bytes(HIST_GP)
    gp = json.loads(gp_bytes)
    hist = json.loads(hist_bytes)
    pool = list(csv.DictReader(io.StringIO(pool_bytes.decode("utf-8-sig"))))
    records = gp.get("results", gp)
    old_records = hist.get("results", hist)
    if len(records) != 270:
        raise RuntimeError(f"Recovered GP record count changed: {len(records)} != 270")
    if len(pool) != 3615:
        raise RuntimeError(f"Recovered pool row count changed: {len(pool)} != 3615")
    champions = [row for row in pool if row.get("rank_combined") == "1"]
    species = {row.get("compound_id") for row in champions if row.get("compound_id")}
    if len(champions) != 270 or len(species) != 90:
        raise RuntimeError(
            f"Recovered pool changed: champions={len(champions)}, species={len(species)}"
        )
    def normalized_key(key: str, rec: dict) -> tuple[str, int] | None:
        match = re.search(r"_x(\d+)", key)
        if not match:
            return None
        pct = {"002": 2, "005": 5, "010": 10, "020": 2, "050": 5, "100": 10}.get(match.group(1))
        dopant = str(rec.get("dopant") or key.split("_x", 1)[0]).split("+", 1)[0]
        return (dopant, pct) if pct is not None else None

    old_v = {
        normalized_key(key, rec): rec.get("oxidation_limit_V", rec.get("ox_V"))
        for key, rec in old_records.items()
        if normalized_key(key, rec)
    }
    new_v = {
        normalized_key(key, rec): rec.get("oxidation_limit_V", rec.get("ox_V"))
        for key, rec in records.items()
        if normalized_key(key, rec)
    }
    overlap = set(old_v) & set(new_v)
    drift = sum(
        old_v[key] != new_v[key]
        for key in overlap
    )
    if len(overlap) != 141 or drift != 0:
        raise RuntimeError(f"GP overlap audit changed: overlap={len(overlap)}, drift={drift}")
    hashes = {
        "recovered_gp_sha256": _sha(gp_bytes),
        "recovered_pool_sha256": _sha(pool_bytes),
        "historical_gp_sha256": _sha(hist_bytes),
    }
    return records, champions, hashes


def _materialize_recovered_v2() -> dict[str, dict]:
    """Copy the reviewed side-by-side v2 artifacts from the recovery branch.

    They remain status-labelled as recovered/incomplete.  Materializing them
    only makes the full 90-species evidence downloadable in dftweb; it does not
    promote the 89-row ranking or legacy transport proxy to canonical status.
    """
    status = {}
    for rel in RECOVERED_DERIVED:
        data = _git_bytes(rel)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        item = {"sha256": _sha(data), "bytes": len(data)}
        if rel.endswith(".csv"):
            lines = [x for x in data.decode("utf-8-sig").splitlines() if x and not x.startswith("#")]
            item["rows"] = len(list(csv.DictReader(lines)))
        status[rel] = item
    return status


def _validate_local_recovered_v2() -> dict[str, dict]:
    """Validate exact local copies without falling back to another pool."""
    status = {}
    for rel in RECOVERED_DERIVED:
        data = (ROOT / rel).read_bytes()
        expected = EXPECTED_SOURCE[rel]
        if (_sha(data), len(data)) != expected:
            raise RuntimeError(
                f"Local recovered artifact differs from pinned source: {rel}; "
                "run with --materialize-recovered in a reviewed workspace"
            )
        item = {"sha256": expected[0], "bytes": expected[1]}
        if rel.endswith(".csv"):
            lines = [x for x in data.decode("utf-8-sig").splitlines() if x and not x.startswith("#")]
            item["rows"] = len(list(csv.DictReader(lines)))
        status[rel] = item
    return status


def _validate_release_manifest() -> None:
    manifest_path = DB / "cascade_audit_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 2:
        raise RuntimeError("cascade audit manifest schema_version must be 2")
    if manifest.get("source_commit") != PINNED_SOURCE_COMMIT:
        raise RuntimeError("cascade audit manifest is not pinned to the reviewed commit")
    expected_headline = {
        "planned_slots": 273, "completed_slots": 270, "completed_species": 90,
        "historical_snapshot_species": 47,
        "approved_current_leaderboard_species": 0,
        "explicit_pair_property_labels": 0,
    }
    if manifest.get("headline") != expected_headline:
        raise RuntimeError(f"manifest headline changed: {manifest.get('headline')}")
    for item in manifest.get("figures", []):
        image = ROOT / item["image"]
        table = ROOT / item["csv"]
        im = _file_meta(image)
        tab = _file_meta(table, csv_rows=True)
        if (im["sha256"], im["bytes"]) != (item.get("image_sha256"), item.get("image_bytes")):
            raise RuntimeError(f"audit image integrity failed: {item['image']}")
        if (tab["sha256"], tab["bytes"], tab["rows"]) != (
            item.get("csv_sha256"), item.get("csv_bytes"), item.get("csv_rows")
        ):
            raise RuntimeError(f"audit CSV integrity failed: {item['csv']}")
    if len(manifest.get("figures", [])) != 5:
        raise RuntimeError("exactly five audit figure/CSV pairs are required")
    for item in manifest.get("supporting_tables", []):
        tab = _file_meta(ROOT / item["path"], csv_rows=True)
        if (tab["sha256"], tab["bytes"], tab["rows"]) != (
            item.get("sha256"), item.get("bytes"), item.get("rows")
        ):
            raise RuntimeError(f"supporting-table integrity failed: {item['path']}")


def campaign_figure() -> tuple[Path, Path]:
    rows = [
        {"layer": "Run slots", "state": "Planned", "count": 273, "status": "design"},
        {"layer": "Run slots", "state": "Completed", "count": 270, "status": "verified"},
        {"layer": "Run slots", "state": "As2S3 stopped", "count": 3, "status": "verified"},
        {"layer": "Species", "state": "Completed", "count": 90, "status": "verified"},
        {"layer": "Species", "state": "Historical snapshot", "count": 47, "status": "superseded"},
        {"layer": "Species", "state": "Approved current leaderboard", "count": 0, "status": "unavailable"},
    ]
    csv_path = _write_csv(
        "cascade_audit_campaign_status.csv", rows, ["layer", "state", "count", "status"]
    )

    image, draw = _canvas(
        "Compute completed; canonical decision products did not",
        "Recovered outputs are not an approved 90-species ranking.",
    )
    panels = [(55, 160, 870, 850), (930, 160, 1745, 850)]
    _panel(draw, panels[0], "Campaign execution")
    _panel(draw, panels[1], "Evidence registration")

    for box, values, labels, colors, maxv, unit in (
        (panels[0], [273, 270, 3], ["Planned", "Completed", "As2S3 stopped"], [PALE, TEAL, RED], 300, "Top-level run slots"),
        (panels[1], [90, 47, 0], ["Completed species", "Historical snapshot", "Approved leaderboard"], [TEAL, AMBER, RED], 100, "Unique base species"),
    ):
        x0, y0, x1, y1 = box
        bar_left = x0 + 245
        bar_right = x1 - 70
        for i, (value, label, color) in enumerate(zip(values, labels, colors)):
            cy = y0 + 150 + i * 150
            draw.text((x0 + 30, cy - 18), label, fill=INK, font=_font(25))
            draw.rounded_rectangle((bar_left, cy - 22, bar_right, cy + 28), radius=12, fill="#e5e7eb")
            width = max(4, int((bar_right - bar_left) * value / maxv))
            draw.rounded_rectangle((bar_left, cy - 22, bar_left + width, cy + 28), radius=12, fill=color)
            draw.text((min(bar_left + width + 14, bar_right + 8), cy - 22), str(value), fill=INK, font=_font(27, True))
        draw.text((bar_left, y1 - 55), unit, fill=MUT, font=_font(21))
    return _save(image, "cascade_audit_campaign_status.png"), csv_path


def g3_figure(records: dict) -> tuple[Path, Path]:
    li_s4 = []
    for rec in records.values():
        rxn = str(rec.get("oxidation_onset_rxn", ""))
        if "LiS4" in rxn:
            li_s4.append(float(rec.get("oxidation_limit_V")))
    rows = [
        {
            "system": "LPSCl host",
            "phase_set_id": "mp-gga-gga-u__lis4-included",
            "oxidation_onset_V": 2.140,
            "delta_vs_included_V": 0.000,
            "status": "historical",
            "note": "Candidate and host must use this same phase set",
        },
        {
            "system": "LPSCl host",
            "phase_set_id": "mp-gga-gga-u__lis4-excluded",
            "oxidation_onset_V": 2.256,
            "delta_vs_included_V": 0.116,
            "status": "sensitivity-only",
            "note": "Do not apply this threshold to included-phase-set candidates",
        },
        {
            "system": "Recovered candidate records",
            "phase_set_id": "mp-gga-gga-u__lis4-included",
            "oxidation_onset_V": "",
            "delta_vs_included_V": "",
            "status": "recovered_unvalidated",
            "note": f"{len(li_s4)}/270 onset reactions contain LiS4",
        },
    ]
    csv_path = _write_csv(
        "cascade_audit_g3_phase_set.csv",
        rows,
        ["system", "phase_set_id", "oxidation_onset_V", "delta_vs_included_V", "status", "note"],
    )
    image, draw = _canvas(
        "G3 changes when the competing phase set changes",
        "Candidate and host must be compared within the same phase_set_id.",
    )
    _panel(draw, (120, 165, 1680, 835), "LPSCl host oxidation onset")
    base_y = 730
    top_y = 275
    vals = [2.140, 2.256]
    labels = ["LiS4 included", "LiS4 excluded"]
    colors = [TEAL, AMBER]
    vmin, vmax = 1.95, 2.46
    for i, (label, value, color) in enumerate(zip(labels, vals, colors)):
        x0 = 470 + i * 570
        x1 = x0 + 260
        height = int((value - vmin) / (vmax - vmin) * (base_y - top_y))
        draw.rounded_rectangle((x0, base_y - height, x1, base_y), radius=18, fill=color)
        draw.text((x0 + 130, base_y - height - 55), f"{value:.3f} V", anchor="mm", fill=INK, font=_font(31, True))
        draw.text((x0 + 130, base_y + 42), label, anchor="mm", fill=INK, font=_font(25))
    draw.line((860, 445, 1080, 350), fill=RED, width=5)
    draw.polygon([(1080, 350), (1053, 354), (1068, 377)], fill=RED)
    draw.text((795, 400), "+0.116 V", fill=RED, font=_font(30, True))
    draw.text((155, 785), f"LiS4 appears in {len(li_s4)}/270 recovered onset reactions", fill=MUT, font=_font(23))
    return _save(image, "cascade_audit_g3_phase_set.png"), csv_path


def g4_figure() -> tuple[Path, Path]:
    source = _local_csv(DB / "cascade_v23_litransport.csv")
    x005 = [row for row in source if row["_dir"].endswith("_x005")]
    vals = [float(row["bvs_li_proxy_score"]) for row in x005]
    lo, hi = min(vals), max(vals)
    focus = ["B2O3", "Cr2O3", "Ga2O3", "In2O3", "Sc2O3", "Y2O3"]
    rows = []
    for species in focus:
        rec = next(row for row in x005 if row["_dir"] == f"{species}_x005")
        raw = float(rec["bvs_li_proxy_score"])
        blocking = float(rec["tier2_dopant_blocking_fraction"])
        bvs_only = 0.10 + 0.90 * ((raw - lo) / (hi - lo))
        composite = bvs_only if blocking < 0.60 else 0.05
        rows.append(
            {
                "species": species,
                "legacy_bvs_raw": f"{raw:.6f}",
                "blocking_4A_fraction": f"{blocking:.6f}",
                "historical_composite_score": f"{composite:.4f}",
                "bvs_only_rescore": f"{bvs_only:.4f}",
                "historical_pass_gt_0p30": "Y" if composite > 0.30 else "N",
                "bvs_only_pass_gt_0p30": "Y" if bvs_only > 0.30 else "N",
                "status": "historical_gate_audit",
            }
        )
    csv_path = _write_csv(
        "cascade_audit_g4_rescore.csv",
        rows,
        [
            "species",
            "legacy_bvs_raw",
            "blocking_4A_fraction",
            "historical_composite_score",
            "bvs_only_rescore",
            "historical_pass_gt_0p30",
            "bvs_only_pass_gt_0p30",
            "status",
        ],
    )
    image, draw = _canvas(
        "The historical 6/6 stop is not a physical transport verdict",
        "The composite gate forces blocking failures to 0.05; the teal points remove that floor.",
    )
    plot_left, plot_right = 330, 1660
    plot_top, row_gap = 215, 92
    cutoff_x = plot_left + int(0.30 * (plot_right - plot_left))
    draw.line((cutoff_x, 185, cutoff_x, 770), fill=AMBER, width=4)
    draw.text((cutoff_x + 8, 180), "Historical cutoff 0.30", fill=AMBER, font=_font(22, True))
    for tick in [0.0, 0.25, 0.5, 0.75, 1.0]:
        x = plot_left + int(tick * (plot_right - plot_left))
        draw.line((x, 760, x, 775), fill=MUT, width=2)
        draw.text((x, 790), f"{tick:.2f}", anchor="ma", fill=MUT, font=_font(20))
    for i, row in enumerate(rows):
        cy = plot_top + i * row_gap
        comp = float(row["historical_composite_score"])
        bvs = float(row["bvs_only_rescore"])
        x_comp = plot_left + int(comp * (plot_right - plot_left))
        x_bvs = plot_left + int(bvs * (plot_right - plot_left))
        draw.text((75, cy), row["species"], anchor="lm", fill=INK, font=_font(26, True))
        draw.line((x_comp, cy, x_bvs, cy), fill="#9ca3af", width=5)
        draw.line((x_comp - 11, cy - 11, x_comp + 11, cy + 11), fill=RED, width=5)
        draw.line((x_comp - 11, cy + 11, x_comp + 11, cy - 11), fill=RED, width=5)
        draw.ellipse((x_bvs - 11, cy - 11, x_bvs + 11, cy + 11), fill=TEAL, outline="white", width=2)
        draw.text((x_bvs + 16, cy - 14), f"{bvs:.2f}", fill=TEAL, font=_font(19, True))
    draw.line((80, 870, 110, 870), fill=RED, width=5)
    draw.text((125, 870), "Historical composite G4", anchor="lm", fill=INK, font=_font(21))
    draw.ellipse((515, 858, 539, 882), fill=TEAL)
    draw.text((555, 870), "Legacy BVS-only rescore", anchor="lm", fill=INK, font=_font(21))
    draw.text((1720, 870), "5/6 pass after removing the 4 Å floor", anchor="rm", fill=GREEN, font=_font(23, True))
    return _save(image, "cascade_audit_g4_rescore.png"), csv_path


def interface_figure() -> tuple[Path, Path]:
    verdict = json.loads((DB / "cascade_stability_axes_verdict.json").read_text(encoding="utf-8"))
    gates = verdict["T9_interface_axes"]["gates"]
    labels = ["Cathode full", "Cathode half", "LPSCl SE", "Li metal"]
    keys = ["cathode_full", "cathode_half", "SE_LPSCl", "Li_anode"]
    rows = []
    for label, key in zip(labels, keys):
        item = gates[key]
        rows.append(
            {
                "axis": label,
                "pass_count": item["pass"],
                "kill_count": item["kill"],
                "pool_count": item["n"],
                "cutoff_meV_atom": 100,
                "status": "historical_post_hoc",
                "application_caveat": "Li-metal axis applies only when modified SE contacts Li" if key == "Li_anode" else "",
            }
        )
    csv_path = _write_csv(
        "cascade_audit_interface_axes.csv",
        rows,
        ["axis", "pass_count", "kill_count", "pool_count", "cutoff_meV_atom", "status", "application_caveat"],
    )
    image, draw = _canvas(
        "Interface axes were computed post hoc, not integrated into the core funnel",
        "Historical 47-species snapshot · 100 meV/atom cutoff · geometry and cutoff sensitivity remain open.",
    )
    bar_left, bar_right = 390, 1660
    for i, row in enumerate(rows):
        cy = 245 + i * 135
        p = int(row["pass_count"])
        k = int(row["kill_count"])
        split = bar_left + int((bar_right - bar_left) * p / 47)
        draw.text((70, cy), row["axis"], anchor="lm", fill=INK, font=_font(27, True))
        draw.rounded_rectangle((bar_left, cy - 34, split, cy + 34), radius=14, fill=TEAL)
        draw.rounded_rectangle((split, cy - 34, bar_right, cy + 34), radius=14, fill=RED)
        draw.text(((bar_left + split) // 2, cy), str(p), anchor="mm", fill="white", font=_font(25, True))
        draw.text(((split + bar_right) // 2, cy), str(k), anchor="mm", fill="white", font=_font(25, True))
    draw.rounded_rectangle((1180, 820, 1220, 850), radius=8, fill=TEAL)
    draw.text((1235, 835), "Pass", anchor="lm", fill=INK, font=_font(21))
    draw.rounded_rectangle((1370, 820, 1410, 850), radius=8, fill=RED)
    draw.text((1425, 835), "Fail", anchor="lm", fill=INK, font=_font(21))
    return _save(image, "cascade_audit_interface_axes.png"), csv_path


def ml_figure() -> tuple[Path, Path]:
    meta = json.loads((DB / "codoping_ml_v2_meta.json").read_text(encoding="utf-8"))
    defense = meta["sendek2017_small_sample_defenses"]
    cv = defense["cv_leakage_leave_one_dopant_out"]
    s3 = defense["stage3_interaction_distillation"]
    rows = [
        {"panel": "generalization", "metric": "pair LOOCV weighted R2", "value": cv["pair_LOOCV"]["weighted_r2"], "p_value": "", "interpretation": "dopant leakage"},
        {"panel": "generalization", "metric": "LODO weighted R2", "value": cv["leave_one_dopant_out"]["weighted_r2"], "p_value": "", "interpretation": "worse than mean"},
        {"panel": "generalization", "metric": "L2DO weighted R2", "value": cv["leave_both_dopants_out"]["weighted_r2"], "p_value": "", "interpretation": "worse than mean"},
        {"panel": "acquisition", "metric": "global discovery enrichment", "value": s3["stage3_rank_enrichment_vs_label_shuffle"], "p_value": s3["label_shuffle_p_value_precision"], "interpretation": "not significant"},
        {"panel": "acquisition", "metric": "ordering enrichment within listed 40", "value": s3["spearman_enrichment_vs_label_shuffle"], "p_value": s3["label_shuffle_p_value_spearman"], "interpretation": "retrospective signal"},
    ]
    csv_path = _write_csv(
        "cascade_audit_ml_validation.csv", rows, ["panel", "metric", "value", "p_value", "interpretation"]
    )
    image, draw = _canvas(
        "Use ML to schedule evidence, not predict truth",
        "Explicit co-doped property labels = 0",
    )
    left = (60, 165, 875, 850)
    right = (925, 165, 1740, 850)
    _panel(draw, left, "New-dopant generalization")
    _panel(draw, right, "Acquisition evidence")

    zero_y = 465
    draw.line((120, zero_y, 820, zero_y), fill=INK, width=3)
    labels = ["pair-CV", "LODO", "L2DO"]
    vals = [float(rows[i]["value"]) for i in range(3)]
    for i, (label, value, color) in enumerate(zip(labels, vals, [AMBER, RED, RED])):
        x0 = 185 + i * 205
        x1 = x0 + 120
        y1 = zero_y - int(value * 720)
        draw.rectangle((x0, min(zero_y, y1), x1, max(zero_y, y1)), fill=color)
        draw.text(((x0 + x1) // 2, y1 - 28 if value >= 0 else y1 + 28), f"{value:+.3f}", anchor="mm", fill=INK, font=_font(24, True))
        draw.text(((x0 + x1) // 2, 760), label, anchor="mm", fill=INK, font=_font(23))
    draw.text((95, 820), "Weighted R2 < 0: worse than predicting the mean", fill=MUT, font=_font(21))

    baseline_y = 700
    draw.line((1000, baseline_y - 130, 1670, baseline_y - 130), fill=MUT, width=2)
    labels = ["Global discovery", "Order within listed 40"]
    vals = [float(rows[3]["value"]), float(rows[4]["value"])]
    pvals = [float(rows[3]["p_value"]), float(rows[4]["p_value"])]
    for i, (label, value, pv, color) in enumerate(zip(labels, vals, pvals, [RED, TEAL])):
        x0 = 1070 + i * 335
        x1 = x0 + 170
        height = int(value / 3.9 * 420)
        draw.rounded_rectangle((x0, baseline_y - height, x1, baseline_y), radius=14, fill=color)
        draw.text(((x0 + x1) // 2, baseline_y - height - 48), f"{value:.2f}x\np={pv:.3f}", anchor="mm", fill=INK, font=_font(24, True), spacing=4, align="center")
        draw.multiline_text(((x0 + x1) // 2, 770), label.replace(" ", "\n", 1), anchor="mm", align="center", fill=INK, font=_font(21), spacing=4)
    draw.text((960, 820), "Only retrospective ordering is significant; property discovery is unvalidated.", fill=MUT, font=_font(20))
    return _save(image, "cascade_audit_ml_validation.png"), csv_path


def artifact_status_csv() -> Path:
    rows = [
        {"artifact": "historical 47 ranked/funnel", "status": "superseded", "web_default": "N", "reason": "campaign coverage stops at 47"},
        {"artifact": "recovered 90 GP records", "status": "recovered_unvalidated", "web_default": "status-only", "reason": "270 records recovered; phase-set/branch comparability remains open"},
        {"artifact": "ranked/themes/funnel v2", "status": "recovered_diagnostic", "web_default": "N", "reason": "89-species derived product; AlI3 absent, MgI2 axis-specific missingness, stale 47-era prose"},
        {"artifact": "cascade_pool_audit_v2.json", "status": "invalid_as_gate_audit", "web_default": "N", "reason": "requires unused B0 and omits the Pugh input used by G5"},
        {"artifact": "legacy Cascade figure family", "status": "archive_only", "web_default": "N", "reason": "O/F-only parsers, fail-open pool fallback, and source-overwrite hazards"},
        {"artifact": "sei_product_gaps.json", "status": "invalid", "web_default": "N", "reason": "stable E_hull=0 entries were treated as falsy"},
        {"artifact": "esw_lpscl_profile.json summary", "status": "invalid", "web_default": "N", "reason": "stored summary disagrees with raw profile"},
        {"artifact": "constrained ESW K>0", "status": "exploratory", "web_default": "N", "reason": "leading/relax/hybrid modes conflict"},
        {"artifact": "interface axes historical 47", "status": "historical_post_hoc", "web_default": "audit-only", "reason": "not integrated; cutoff and geometry sensitive"},
        {"artifact": "co-doping ML queue", "status": "hypothesis_only", "web_default": "audit-only", "reason": "explicit pair property labels = 0"},
    ]
    return _write_csv(
        "cascade_audit_artifact_status.csv", rows, ["artifact", "status", "web_default", "reason"]
    )


def gate_completeness_csv() -> Path:
    """Write the axis-specific presence audit used by the web status page.

    This intentionally does not reuse cascade_pool_audit_v2.json: that file
    requires unused B0 and omits the Pugh input that G5 actually consumes.
    """
    fields = [
        "gate", "estimator", "required_fields", "all_label_complete_species",
        "partial_species", "dropped_species", "usable_under_legacy_aggregator",
        "approved_for_current_ranking", "method_status", "note",
    ]
    rows = [
        {"gate": "G1", "estimator": "UMA host-relative energy", "required_fields": "rerank_de_post_anneal", "all_label_complete_species": 88, "partial_species": "MgI2", "dropped_species": "AlI3", "usable_under_legacy_aggregator": 89, "approved_for_current_ranking": 0, "method_status": "recovered_diagnostic", "note": "All three directory labels have actual_x=0.25; MgI2 is silently averaged from two labels in the legacy aggregator."},
        {"gate": "G2", "estimator": "MP grand-potential window", "required_fields": "red_V|ox_V|window_V", "all_label_complete_species": 90, "partial_species": "", "dropped_species": "", "usable_under_legacy_aggregator": 90, "approved_for_current_ranking": 0, "method_status": "recovered_unvalidated", "note": "Record presence is complete, but branch and phase-set identity are not carried into the species-level table."},
        {"gate": "G3", "estimator": "MP phase-set onset", "required_fields": "ox_V|host_anchor_V|phase_set_id", "all_label_complete_species": 0, "partial_species": "", "dropped_species": "method identity unavailable for all 90", "usable_under_legacy_aggregator": 90, "approved_for_current_ranking": 0, "method_status": "blocked_method_contract", "note": "Ninety species have an onset record, but the derived table strips phase_set_id and mixes plain/Cl-rich support; record presence is not method-complete comparability."},
        {"gate": "G4", "estimator": "legacy BVS plus 4A foreign-center composite", "required_fields": "bvs_li_proxy_score@x005|tier2_dopant_blocking_fraction@x005", "all_label_complete_species": 88, "partial_species": "", "dropped_species": "AlI3|MgI2", "usable_under_legacy_aggregator": 88, "approved_for_current_ranking": 0, "method_status": "historical_only", "note": "Missing x005 input must stay missing, not fail. The score is not canonical BVSE, a barrier, diffusivity, or conductivity."},
        {"gate": "G5", "estimator": "UMA relaxed-ion elastic screen", "required_fields": "elastic_E_young_GPa|elastic_pugh_GoverB", "all_label_complete_species": 88, "partial_species": "MgI2", "dropped_species": "AlI3", "usable_under_legacy_aggregator": 89, "approved_for_current_ranking": 0, "method_status": "recovered_diagnostic", "note": "MgI2 is silently averaged from two labels; the median and final ranking are pool-relative."},
    ]
    return _write_csv("cascade_audit_gate_completeness.csv", rows, fields)


def _file_meta(path: Path, csv_rows: bool = False) -> dict:
    data = path.read_bytes()
    item = {"sha256": _sha(data), "bytes": len(data)}
    if csv_rows:
        lines = [x for x in data.decode("utf-8-sig").splitlines() if x and not x.startswith("#")]
        item["rows"] = len(list(csv.DictReader(lines)))
    return item


def write_manifest(  # noqa: D401  — ⛔ 2026-08-14 이후 **호출 금지**
    # Codex Round-3 P0-1: 이 함수가 cascade_audit_manifest.json 을 통째로 덮어써서
    # rebuild_pool_inputs 의 artifacts 블록을 지웠다(그 반대도 일어났다). 원장의 단독
    # 소유자는 tools/cascade/build_cascade_audit_manifest.py 다. 이 함수는 sidecar
    # (cascade_audit_manifest_plotter_sidecar.json) 로만 쓴다.

    hashes: dict,
    outputs: list[tuple[Path, Path]],
    records: dict,
    recovered_artifacts: dict[str, dict],
) -> Path:
    manifest = {
        "schema_version": 2,
        "artifact_id": "cascade-audit-2026-08-14",
        "generated_at": "2026-08-14",
        "status": "audit_current__leaderboard_unavailable",
        "source_commit": PINNED_SOURCE_COMMIT,
        "headline": {
            "planned_slots": 273,
            "completed_slots": 270,
            "completed_species": 90,
            "historical_snapshot_species": 47,
            "approved_current_leaderboard_species": 0,
            "explicit_pair_property_labels": 0,
        },
        "datasets": {
            "historical_47": {
                "status": "superseded",
                "species_count": 47,
                "slot_count": 141,
                "actual_x": 0.25,
                "pool_id": "cascade-v23-o37-f10-2026-06",
                "phase_set_id": "mp-gga-gga-u__lis4-included",
                "limitations": ["historical campaign snapshot", "pool-relative ranks", "not current campaign coverage"],
            },
            "recovered_90_gp": {
                "status": "recovered_unvalidated",
                "species_count": 90,
                "slot_count": len(records),
                "actual_x": 0.25,
                "pool_id": "cascade-v23-completed-90-2026-07",
                "phase_set_id": "mp-gga-gga-u__lis4-included",
                "source_ref": f"{RECOVERED_REF}:{RECOVERED_GP}",
                "source_commit": PINNED_SOURCE_COMMIT,
                "overlap_with_historical": 141,
                "overlap_oxidation_drift_count": 0,
                "limitations": ["not fully re-ranked or re-gated", "G3 phase-set sensitivity open", "G4 must be rebuilt with canonical softBV"],
            },
            "recovered_90_sidecar": {
                "status": "recovered_unvalidated",
                "species_count": 90,
                "champion_rows": 270,
                "gp_species_rows": 90,
                "ranked_rows": 89,
                "ranked_missing_species": ["AlI3"],
                "funnel_status": "recovered_diagnostic__release_blocked",
                "field_presence": {
                    "G1": "88 all-label complete; MgI2 partial; AlI3 absent",
                    "G2_G3": "90 records present; phase-set and branch comparability not preserved",
                    "G4": "88 x005 inputs present; MgI2 and AlI3 missing",
                    "G5": "88 all-label complete; MgI2 partial; AlI3 absent",
                },
                "limitations": [
                    "ranking is incomplete 89/90",
                    "litransport_v2 is the legacy BVS/4A proxy",
                    "the 71/18/1 audit is selected-field ingestion completeness, not gate completeness",
                    "no approved 90-species funnel or Pareto set",
                ],
            },
            "current_approved_leaderboard": {"status": "unavailable", "species_count": 0},
        },
        "metric_contract": {
            "G3": {
                "display_name": "MP phase-set onset",
                "historical_host_onset_V": 2.140,
                "alternate_host_onset_V": 2.256,
                "rule": "compare candidate and host within the same phase_set_id",
            },
            "G4": {
                "display_name": "legacy BVS + 4A foreign-center composite",
                "blocking_definition": "fraction of Li within 4 A of atoms outside {Li,P,S,Cl}",
                "historical_rule": "blocking<0.60 ? 0.10+0.90*minmax(BVS) : 0.05",
                "not_equivalent_to": ["canonical BVSE", "migration barrier", "diffusivity", "conductivity"],
            },
        },
        "source_hashes": hashes,
        "recovered_artifacts": recovered_artifacts,
        "figures": [],
        "source_of_truth": "docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md",
    }
    for img, csv_path in outputs:
        im = _file_meta(img)
        tab = _file_meta(csv_path, csv_rows=True)
        manifest["figures"].append({
            "image": f"docs/figures/cascade/{img.name}",
            "csv": f"db/properties/{csv_path.name}",
            "status": "audit-current",
            "image_sha256": im["sha256"], "image_bytes": im["bytes"],
            "csv_sha256": tab["sha256"], "csv_bytes": tab["bytes"], "csv_rows": tab["rows"],
        })
    support = [gate_completeness_csv(), artifact_status_csv()]
    manifest["supporting_tables"] = []
    for path in support:
        item = _file_meta(path, csv_rows=True)
        manifest["supporting_tables"].append({
            "path": f"db/properties/{path.name}", "status": "audit-current",
            "sha256": item["sha256"], "bytes": item["bytes"], "rows": item["rows"],
        })
    out = DB / "cascade_audit_manifest_plotter_sidecar.json"   # ← 원장 아님 (sidecar)
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--materialize-recovered",
        action="store_true",
        help="copy only hash-pinned recovered sidecars from the frozen commit",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate pinned inputs/local sidecars without regenerating figures",
    )
    args = parser.parse_args()
    FIG.mkdir(parents=True, exist_ok=True)
    DB.mkdir(parents=True, exist_ok=True)
    records, _champions, hashes = _read_recovered()
    recovered_artifacts = (
        _materialize_recovered_v2()
        if args.materialize_recovered
        else _validate_local_recovered_v2()
    )
    if args.validate_only:
        _validate_release_manifest()
        print(
            f"Validated pinned source {PINNED_SOURCE_COMMIT[:8]}: "
            f"records={len(records)}, sidecars={len(recovered_artifacts)}"
        )
        return
    outputs = [
        campaign_figure(),
        g3_figure(records),
        g4_figure(),
        interface_figure(),
        ml_figure(),
    ]
    manifest = write_manifest(hashes, outputs, records, recovered_artifacts)
    print(f"Wrote {len(outputs)} PNG/CSV pairs and {manifest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
