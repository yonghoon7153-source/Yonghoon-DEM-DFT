"""
Plastic coverage estimation from DEM contact dumps.

Physics: In DEM with hooke/hysteresis + reduced E_SE (porosity-calibrated),
the resulting particle overlap δ/R* already mimics real plastic-deformed state.
At each AM-SE contact we classify the regime by overlap_ratio = δ/R*:
  δ/R* < 0.003    → elastic (Hertzian point contact, a² = R*·δ)
  0.003-0.01      → elastic-plastic transition
  δ/R* > 0.01     → fully plastic (film formation, larger a)
Integrate film area per AM particle → plastic coverage fraction.

LIGGGHTS contact dump column layout (26 cols, compute cpl with
  pos id force force_normal force_tangential torque contactArea delta contactPoint):
  1-3   : pos1 (x1,y1,z1)
  4-6   : pos2 (x2,y2,z2)
  7-8   : id1, id2
  9     : periodic / ghost flag (ignore)
  10-12 : force (total)
  13-15 : force_normal
  16-18 : force_tangential
  19-21 : torque
  22    : contactArea
  23    : delta            ← key input
  24-26 : contactPoint
"""

from __future__ import annotations
import numpy as np
import os, sys, glob, argparse, json
from collections import defaultdict


# ---------- Physical constants (from literature + lab assumption) ----------
E_REAL_SE     = 24.0e9    # Pa, LPSCl Young's modulus (LAB VALUE: 24 GPa)
E_REAL_AM     = 140.0e9   # Pa, NCM Young's modulus
POISSON_SE    = 0.30
POISSON_AM    = 0.25
SIGMA_Y_SE    = 0.30e9    # Pa, LPSCl yield stress (H/2.8, H≈0.85 GPa)
H_REAL_SE     = 0.85e9    # Pa, LPSCl hardness (Tabor H ≈ 2.8 σ_y)

# Reduced modulus E* for AM-SE contact (dominated by softer SE)
#   1/E* = (1-ν₁²)/E₁ + (1-ν₂²)/E₂
_inv_Estar = (1 - POISSON_AM**2) / E_REAL_AM + (1 - POISSON_SE**2) / E_REAL_SE
E_STAR_AM_SE = 1.0 / _inv_Estar     # ≈ 22.4 GPa
E_STAR_AM_SE_REAL = E_STAR_AM_SE    # alias: 'physics' mode uses real E (same value here)

# Plastic film thickness (for volume-conservation in 'physics' mode)
# Sulfide glass plastic flow: film thickness ~few nm (Sakuda 2013 discussion).
# Anchored 5 nm as physical minimum for LPSCl at RT pressure sintering.
H_FILM_MIN = 5.0e-9   # 5 nm

# Plastic regime thresholds on δ/R* derived from Hertzian + Tabor
#   P_max = (2E*/π) · √(δ/R*)         [Hertzian peak contact pressure]
#   Yield onset:      P_max = 1.6 σ_y  → δ/R* = (0.8π σ_y/E*)²
#   Fully plastic:    P_mean = 2.8 σ_y → δ/R* = (2.1π σ_y/E*)²
_ratio = SIGMA_Y_SE / E_STAR_AM_SE   # ≈ 0.0134
DR_YIELD_ONSET    = (0.8 * np.pi * _ratio) ** 2   # ≈ 0.0011  (0.11%)
DR_FULLY_PLASTIC  = (2.1 * np.pi * _ratio) ** 2   # ≈ 0.0078  (0.78%)

# SE = solid electrolyte atom type in the DEM setup
SE_ATOM_TYPE = 3  # thin6/9 = 3 types (1 AM_P, 2 AM_S, 3 SE);  particulate12 = 2 types → override via CLI


# =============================================================
#   Parsers
# =============================================================
def parse_atom_dump(path: str) -> dict[int, dict]:
    """Parse LIGGGHTS atom dump. Returns {atom_id: {type, r, pos(np.ndarray)}}."""
    atoms: dict[int, dict] = {}
    with open(path) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("ITEM: ATOMS"):
            cols = line.strip().split()[2:]
            idx = {c: j for j, c in enumerate(cols)}
            for dl in lines[i + 1:]:
                v = dl.strip().split()
                if len(v) < len(cols):
                    break
                aid = int(v[idx["id"]])
                atoms[aid] = {
                    "type": int(v[idx["type"]]),
                    "r":    float(v[idx["radius"]]),
                    "pos":  np.array([float(v[idx["x"]]),
                                      float(v[idx["y"]]),
                                      float(v[idx["z"]])]),
                }
            break
    return atoms


def parse_contact_dump(path: str) -> list[dict]:
    """Parse LIGGGHTS contact dump (pair/gran/local). Returns list of contact dicts."""
    contacts: list[dict] = []
    with open(path) as f:
        lines = f.readlines()
    entries_start = None
    for i, line in enumerate(lines):
        if line.startswith("ITEM: ENTRIES"):
            entries_start = i + 1
            break
    if entries_start is None:
        return contacts
    for dl in lines[entries_start:]:
        v = dl.strip().split()
        if len(v) < 26:
            continue
        try:
            contacts.append({
                "id1":          int(float(v[6])),
                "id2":          int(float(v[7])),
                "force_normal": np.array([float(v[12]), float(v[13]), float(v[14])]),
                "contactArea":  float(v[21]),
                "delta":        float(v[22]),
            })
        except ValueError:
            continue
    return contacts


def parse_atoms_csv(path: str) -> dict[int, dict]:
    """Parse atoms.csv (output of parse_liggghts.py). Same schema as parse_atom_dump.
    Expected columns: id, type, radius, x, y, z (order may vary)."""
    import csv as _csv
    atoms: dict[int, dict] = {}
    with open(path, newline='') as f:
        reader = _csv.DictReader(f)
        for row in reader:
            try:
                aid = int(float(row.get("id", row.get("atom_id", 0))))
                atoms[aid] = {
                    "type":   int(float(row.get("type", 0))),
                    "r":      float(row.get("radius", row.get("r", 0.0))),
                    "pos":    np.array([float(row.get("x", 0)),
                                        float(row.get("y", 0)),
                                        float(row.get("z", 0))]),
                }
            except (ValueError, TypeError):
                continue
    return atoms


def parse_contacts_csv(path: str) -> list[dict]:
    """Parse contacts.csv (output of parse_liggghts.py). Same schema as parse_contact_dump.
    Expected columns: id1, id2, fn_x, fn_y, fn_z, contact_area, delta (order may vary)."""
    import csv as _csv
    contacts: list[dict] = []
    with open(path, newline='') as f:
        reader = _csv.DictReader(f)
        for row in reader:
            try:
                contacts.append({
                    "id1":          int(float(row.get("id1", 0))),
                    "id2":          int(float(row.get("id2", 0))),
                    "force_normal": np.array([float(row.get("fn_x", 0)),
                                              float(row.get("fn_y", 0)),
                                              float(row.get("fn_z", 0))]),
                    "contactArea":  float(row.get("contact_area", row.get("contactArea", 0))),
                    "delta":        float(row.get("delta", 0)),
                })
            except (ValueError, TypeError):
                continue
    return contacts


def parse_atoms_auto(path: str) -> dict:
    """Auto-detect atoms file format (LIGGGHTS dump vs CSV)."""
    if path.endswith(".csv") or path.endswith(".CSV"):
        return parse_atoms_csv(path)
    # Try sniffing: LIGGGHTS files have "ITEM:" header in first few lines
    try:
        with open(path) as f:
            head = f.read(1024)
        if "ITEM: ATOMS" in head or "ITEM:" in head:
            return parse_atom_dump(path)
        # Otherwise assume CSV (has 'id,type,radius' header)
        if "id" in head.lower() and ("type" in head.lower() or "radius" in head.lower()):
            return parse_atoms_csv(path)
    except Exception:
        pass
    # Fallback: try LIGGGHTS
    return parse_atom_dump(path)


def parse_contacts_auto(path: str) -> list:
    """Auto-detect contacts file format (LIGGGHTS dump vs CSV)."""
    if path.endswith(".csv") or path.endswith(".CSV"):
        return parse_contacts_csv(path)
    try:
        with open(path) as f:
            head = f.read(1024)
        if "ITEM: ENTRIES" in head or "ITEM:" in head:
            return parse_contact_dump(path)
        if "id1" in head.lower() and "delta" in head.lower():
            return parse_contacts_csv(path)
    except Exception:
        pass
    return parse_contact_dump(path)


# =============================================================
#   Plastic coverage computation
# =============================================================
def film_area_from_overlap(delta: float, R_star: float,
                            R_min: float = None,
                            ligg_area: float = None,
                            mode: str = "capped",
                            k_spread: float = 1.0) -> tuple[float, str]:
    """Return (contact film area in m², regime label).
    mode:
      'hertzian'  — pure elastic Hertzian (π R* δ). Underestimates plastic.
      'liggghts'  — use LIGGGHTS-reported contactArea directly. DEM-native.
      'capped'    — geometric cap a² ≤ R_min². k_spread scales pre-cap (legacy).
      'physics'   — literature-anchored, no free parameters. Uses:
                    * Tabor: A_plastic = F_real / H  (where F_real from E_real)
                    * Volume conservation: A ≤ V_overlap / h_film_min
                    * Geometric hemisphere cap: A ≤ 2π R_min²
                    All constants anchored by DB entries #11 (Sakuda), #12 (Koerver Table 1).
    k_spread: only applies to 'capped' mode (legacy post-hoc calibration).
      1.00 = raw DEM | 1.65 = Minnmann 2021 match (recommended for 'capped')
    """
    dr = delta / R_star if R_star > 0 else 0.0
    if dr <= 0:
        return 0.0, "none"

    elastic_area = np.pi * R_star * delta   # Hertzian point contact (small overlap)

    if mode == "hertzian":
        regime = ("elastic" if dr < DR_YIELD_ONSET else
                  "transition" if dr < DR_FULLY_PLASTIC else "plastic")
        return elastic_area, regime

    if mode == "liggghts":
        regime = ("elastic" if dr < DR_YIELD_ONSET else
                  "transition" if dr < DR_FULLY_PLASTIC else "plastic")
        if ligg_area is not None and ligg_area > 0:
            return ligg_area, regime
        return elastic_area, regime

    if mode == "physics":
        # Literature-first physics model — NO free parameters.
        # Constants from DB entries (Sakuda 2013 #11, Koerver 2018 Table 1 #12).
        # E_real: Young's modulus of LPSCl (24 GPa experimental consensus)
        # H: Tabor hardness (0.85 GPa, sulfide glass range 0.5-1.0 per Sakuda)
        # h_film_min: min plastic film thickness (5 nm, sulfide flow characteristic)
        # Cap (hemisphere): 2π R_min² — lateral spread limit
        # Rationale: DEM overlap (δ/R) is E-independent geometric data. Compute
        # real contact force using E_real (not reduced E_eff used in DEM),
        # then apply Tabor hardness relation A = F/H. Volume conservation
        # prevents unphysical thin films. Hemisphere cap prevents wraparound.
        if dr < DR_YIELD_ONSET:
            return elastic_area, "elastic"

        # Real Hertzian force (using E_real, bypassing DEM's reduced E_eff)
        F_real = (4.0/3.0) * E_STAR_AM_SE_REAL * np.sqrt(R_star) * (delta ** 1.5)

        # Tabor plastic contact area: A = F/H
        A_tabor = F_real / H_REAL_SE

        # Volume-conservation constraint
        # V_overlap (lens): (π/6) δ² (3R* - δ) ≈ π R* δ² /2 for small δ
        V_overlap = (np.pi / 6.0) * (delta ** 2) * (3.0 * R_star - delta)
        A_volume = V_overlap / H_FILM_MIN if H_FILM_MIN > 0 else float('inf')

        # Geometric cap: hemisphere of smallest particle (lateral spread ≤ 2πR²)
        r_min_eff = R_min if R_min else R_star
        A_geom = 2.0 * np.pi * (r_min_eff ** 2)

        A_plastic = min(A_tabor, A_volume, A_geom)
        regime = "plastic" if dr >= DR_FULLY_PLASTIC else "transition"
        return A_plastic, regime

    # Default: 'capped' physics model
    # Geometric ceiling: film radius² can't exceed smaller particle's projected area
    cap_a2 = (R_min * R_min) if R_min else (R_star * R_star)
    k2 = k_spread * k_spread

    if dr < DR_YIELD_ONSET:
        return elastic_area, "elastic"

    if dr < DR_FULLY_PLASTIC:
        # Smooth transition: interpolate elastic → capped plastic (with k_spread)
        f = (dr - DR_YIELD_ONSET) / (DR_FULLY_PLASTIC - DR_YIELD_ONSET)
        plastic_a2_raw = R_star * R_star * dr / DR_FULLY_PLASTIC
        plastic_a2 = min(plastic_a2_raw * k2, cap_a2)
        return (1 - f) * elastic_area + f * np.pi * plastic_a2, "transition"

    # Fully plastic: area grows linearly with dr BEYOND threshold, spread × k², capped
    scale = dr / DR_FULLY_PLASTIC
    plastic_a2_raw = R_star * R_star * scale
    plastic_a2 = min(plastic_a2_raw * k2, cap_a2)
    return np.pi * plastic_a2, "plastic"


def compute_coverage(atom_path: str, contact_path: str,
                     se_type: int = SE_ATOM_TYPE,
                     mode: str = "capped",
                     dump_contacts: bool = False,
                     k_spread_list: list = None) -> dict:
    """Compute elastic + plastic coverage per AM particle for a single snapshot.
    dump_contacts=True: per-contact list (for network solver input + raw CSV dump).
    k_spread_list: list of k_spread values for sweep (default [1.0]).
      Recommended for paper: [1.0, 1.3, 1.5, 1.65, 1.8]
      Output includes plastic_cov_mean_kX for each k + literature anchor match.
    """
    if k_spread_list is None:
        k_spread_list = [1.0]

    atoms    = parse_atoms_auto(atom_path)
    contacts = parse_contacts_auto(contact_path)

    if not atoms or not contacts:
        return {"error": "empty atom or contact dump", "atom_path": atom_path}

    am_surface: dict[int, float] = {}
    for aid, a in atoms.items():
        if a["type"] != se_type:
            am_surface[aid] = 4.0 * np.pi * a["r"] ** 2  # full sphere surface

    elastic_sum  = defaultdict(float)
    plastic_sum_by_k = {k: defaultdict(float) for k in k_spread_list}
    regime_count = defaultdict(int)
    delta_stats  = []
    per_contact: list[dict] = []   # only populated if dump_contacts

    for c in contacts:
        a1, a2 = atoms.get(c["id1"]), atoms.get(c["id2"])
        if a1 is None or a2 is None:
            continue
        t1, t2 = a1["type"], a2["type"]
        is_se1, is_se2 = (t1 == se_type), (t2 == se_type)
        if is_se1 == is_se2:
            continue

        am_atom = a2 if is_se1 else a1
        am_id   = c["id2"] if is_se1 else c["id1"]
        am_type = am_atom["type"]
        se_atom = a1 if is_se1 else a2
        se_id   = c["id1"] if is_se1 else c["id2"]

        R_star = (am_atom["r"] * se_atom["r"]) / (am_atom["r"] + se_atom["r"])
        R_min  = min(am_atom["r"], se_atom["r"])
        delta  = c["delta"]
        if delta <= 0 or R_star <= 0:
            continue

        dr = delta / R_star
        delta_stats.append(dr)

        elastic_area = np.pi * R_star * delta  # Hertzian baseline

        # Compute plastic area for each k_spread value
        plastic_by_k = {}
        regime = None
        for k in k_spread_list:
            pa, rg = film_area_from_overlap(
                delta, R_star, R_min=R_min,
                ligg_area=c.get("contactArea"), mode=mode, k_spread=k)
            plastic_by_k[k] = pa
            if regime is None:
                regime = rg  # regime labels are k-independent (based on δ/R only)

        elastic_sum[am_id] += elastic_area
        for k in k_spread_list:
            plastic_sum_by_k[k][am_id] += plastic_by_k[k]
        regime_count[regime] += 1

        if dump_contacts:
            rec = {
                "am_id": am_id, "se_id": se_id, "am_type": am_type,
                "R_am": am_atom["r"], "R_se": se_atom["r"],
                "R_star": R_star, "R_min": R_min,
                "delta": delta, "delta_over_R": dr,
                "regime": regime,
                "elastic_area": elastic_area,
                "ligg_area":    c.get("contactArea", 0.0),
            }
            for k in k_spread_list:
                kstr = str(k).replace('.', '_')
                rec[f"plastic_area_k{kstr}"] = plastic_by_k[k]
            per_contact.append(rec)

    # Per-AM coverage
    elastic_cov = []
    plastic_cov_by_k = {k: [] for k in k_spread_list}
    for aid, surf in am_surface.items():
        if aid in elastic_sum:
            elastic_cov.append(min(elastic_sum[aid] / surf, 1.0))
            for k in k_spread_list:
                plastic_cov_by_k[k].append(min(plastic_sum_by_k[k][aid] / surf, 1.0))

    # Percentile summary of δ/R distribution
    dr_arr = np.asarray(delta_stats) if delta_stats else np.array([0.0])
    pct = lambda p: float(np.percentile(dr_arr, p))

    out = {
        "mode":               mode,
        "n_am":               len(am_surface),
        "n_am_with_contact":  len(elastic_cov),
        "n_contacts_am_se":   sum(regime_count.values()),
        "regime_counts":      dict(regime_count),
        # δ/R distribution — full percentile set for correlation analysis
        "delta_over_R_mean":  float(np.mean(dr_arr)),
        "delta_over_R_std":   float(np.std(dr_arr)),
        "delta_over_R_p01":   pct(1),
        "delta_over_R_p05":   pct(5),
        "delta_over_R_p25":   pct(25),
        "delta_over_R_p50":   pct(50),
        "delta_over_R_p75":   pct(75),
        "delta_over_R_p90":   pct(90),
        "delta_over_R_p95":   pct(95),
        "delta_over_R_p99":   pct(99),
        "delta_over_R_med":   pct(50),  # alias of p50 (backward compat)
        "delta_over_R_max":   float(np.max(dr_arr)),
        "elastic_cov_mean":   float(np.mean(elastic_cov))   if elastic_cov else 0.0,
        "elastic_cov_med":    float(np.median(elastic_cov)) if elastic_cov else 0.0,
    }
    # k_spread sweep results
    for k in k_spread_list:
        kstr = str(k).replace('.', '_')
        cov_k = plastic_cov_by_k[k]
        out[f"plastic_cov_mean_k{kstr}"] = float(np.mean(cov_k)) if cov_k else 0.0
        out[f"plastic_cov_med_k{kstr}"]  = float(np.median(cov_k)) if cov_k else 0.0
        amp = (np.mean(cov_k) / np.mean(elastic_cov)) if (cov_k and np.mean(elastic_cov) > 0) else 0.0
        out[f"cov_amp_k{kstr}"] = float(amp)

    # Backward compat: expose k=1.0 results under legacy keys
    if 1.0 in k_spread_list:
        out["plastic_cov_mean"] = out["plastic_cov_mean_k1_0"]
        out["plastic_cov_med"]  = out["plastic_cov_med_k1_0"]
        out["cov_amplification"] = out["cov_amp_k1_0"]

    if dump_contacts:
        out["contacts"] = per_contact
    return out


def dump_raw_delta_r_csv(atom_path: str, contact_path: str, csv_out: str,
                        se_type: int = SE_ATOM_TYPE, mode: str = "capped",
                        k_spread_list: list = None) -> int:
    """Option C: per-contact CSV dump for correlation analysis.
    Columns: am_id, se_id, am_type, R_am, R_se, R_star, R_min,
             delta, delta_over_R, regime, elastic_area, ligg_area,
             plastic_area_k{values}
    Returns number of contact rows written.
    """
    if k_spread_list is None:
        k_spread_list = [1.0, 1.3, 1.5, 1.65, 1.8]
    res = compute_coverage(atom_path, contact_path, se_type=se_type,
                           mode=mode, dump_contacts=True,
                           k_spread_list=k_spread_list)
    if "error" in res:
        return 0
    records = res.get("contacts", [])
    if not records:
        return 0
    import csv as _csv
    keys = list(records[0].keys())
    with open(csv_out, "w", newline="") as f:
        w = _csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(records)
    return len(records)


# =============================================================
#   CLI (step-by-step verification)
# =============================================================
def _pick_latest(dirpath: str, pattern: str) -> str | None:
    files = sorted(glob.glob(os.path.join(dirpath, pattern)),
                   key=lambda p: int(''.join(c for c in os.path.basename(p)
                                              if c.isdigit()) or '0'))
    return files[-1] if files else None


def _find_case_files(case_dir: str) -> tuple[str | None, str | None]:
    """Resolve (atom_path, contact_path) in a case dir, supporting both
    LIGGGHTS dumps (atom_*.liggghts + contact_*.liggghts) and
    pre-parsed CSVs (atoms.csv + contacts.csv). CSV fallback enables
    archive-migrated cases where raw dumps are no longer present."""
    atom_f    = _pick_latest(case_dir, "atom_*.liggghts")
    contact_f = _pick_latest(case_dir, "contact_*.liggghts")
    if atom_f and contact_f:
        return atom_f, contact_f
    # CSV fallback
    atoms_csv    = os.path.join(case_dir, "atoms.csv")
    contacts_csv = os.path.join(case_dir, "contacts.csv")
    if os.path.exists(atoms_csv) and os.path.exists(contacts_csv):
        return atoms_csv, contacts_csv
    return atom_f, contact_f  # may be None, None — caller handles


def detect_se_type(atom_path: str, case_dir: str = None) -> int:
    """Auto-detect SE atom type. Priority:
      1. meta.json type_map: find the key mapped to 'SE'
      2. input_params.json r_SE presence (not used directly but confirms bimodal)
      3. Fallback: max type number in atoms file (3 for bimodal, 2 for standard)
    """
    # Priority 1: meta.json (webapp-style)
    if case_dir:
        meta_path = os.path.join(case_dir, "meta.json")
        if os.path.exists(meta_path):
            try:
                with open(meta_path) as f:
                    meta = json.load(f)
                tm = meta.get("type_map", "")
                if tm:
                    # format: "1:AM_P,2:AM_S,3:SE" or "1:AM_S,2:SE"
                    for pair in tm.split(","):
                        if ":" in pair:
                            k, v = pair.split(":", 1)
                            if v.strip().upper() == "SE":
                                return int(k.strip())
            except Exception:
                pass

    # Priority 3: scan atoms file for max type
    try:
        atoms = parse_atoms_auto(atom_path)
        if atoms:
            types = set(a["type"] for a in atoms.values())
            return max(types)  # SE is always last type by convention
    except Exception:
        pass
    return 2  # default standard mode


def main_inspect(contact_path: str, n_show: int = 5) -> None:
    """Step 1: verify contact dump column mapping. Print first n contacts + stats."""
    contacts = parse_contacts_auto(contact_path)
    print(f"=== Contact dump inspection: {contact_path} ===")
    print(f"Total contacts parsed: {len(contacts)}")
    if not contacts:
        print("  (nothing parsed — check column layout!)")
        return
    print(f"\nFirst {n_show} entries:")
    for i, c in enumerate(contacts[:n_show]):
        F_n = float(np.linalg.norm(c["force_normal"]))
        print(f"  [{i}] id1={c['id1']:5d}  id2={c['id2']:5d}  "
              f"|F_n|={F_n:.4e}  area={c['contactArea']:.4e}  delta={c['delta']:.4e}")
    deltas = np.array([c["delta"] for c in contacts if c["delta"] > 0])
    print(f"\nDelta statistics (N = {len(deltas)}):")
    print(f"  min = {deltas.min():.3e}")
    print(f"  med = {np.median(deltas):.3e}")
    print(f"  max = {deltas.max():.3e}")


def main_case(case_dir: str, se_type: int = SE_ATOM_TYPE,
              mode: str = "capped",
              k_spread_list: list = None,
              dump_raw_csv: str = None) -> None:
    """Step 2: compute plastic coverage for one case (latest snapshot).
    mode: 'capped' | 'physics' | 'hertzian' | 'liggghts' (see film_area_from_overlap)
    k_spread_list: if provided, sweep multiple k values (only affects 'capped' mode).
    dump_raw_csv: if provided, write per-contact CSV to this path (Option C).
    se_type: -1 means auto-detect from meta.json or atom file."""
    atom_f, contact_f = _find_case_files(case_dir)
    if not atom_f or not contact_f:
        print(f"!! No atom/contact dump or CSV found in {case_dir}")
        return
    # Auto-detect se_type if requested
    if se_type is None or se_type < 0:
        se_type = detect_se_type(atom_f, case_dir=case_dir)
        print(f"  [auto-detect] se_type = {se_type}")
    print(f"=== Plastic coverage for {case_dir} ===")
    print(f"  atom    : {os.path.basename(atom_f)}")
    print(f"  contact : {os.path.basename(contact_f)}")
    print(f"  se_type : {se_type}")
    print(f"  mode    : {mode}")
    if k_spread_list and mode == "capped":
        print(f"  k_spread: {k_spread_list}")
    res = compute_coverage(atom_f, contact_f, se_type=se_type,
                           mode=mode,
                           dump_contacts=bool(dump_raw_csv),
                           k_spread_list=k_spread_list)
    # Don't print full contact list (could be huge)
    if "contacts" in res:
        res_print = {k: v for k, v in res.items() if k != "contacts"}
    else:
        res_print = res
    print(json.dumps(res_print, indent=2))
    # Dump raw CSV if requested
    if dump_raw_csv and "contacts" in res:
        import csv as _csv
        recs = res["contacts"]
        if recs:
            with open(dump_raw_csv, "w", newline="") as f:
                w = _csv.DictWriter(f, fieldnames=list(recs[0].keys()))
                w.writeheader()
                w.writerows(recs)
            print(f"\nRaw per-contact CSV written: {dump_raw_csv} ({len(recs)} rows)")


def main_batch(root: str, pattern: str = "post_*",
               se_type: int = SE_ATOM_TYPE,
               csv_out: str = "plastic_coverage.csv",
               mode: str = "capped",
               k_spread_list: list = None,
               dump_raw_dir: str = None) -> None:
    """Step 3: batch over all cases matching pattern under root, write CSV.
    mode: 'capped' | 'physics' | 'hertzian' | 'liggghts'
    k_spread_list: if provided, CSV includes plastic_cov_mean_kX (only 'capped').
    dump_raw_dir: if provided, write per-case raw δ/R CSVs to this dir (Option C)."""
    if k_spread_list is None:
        k_spread_list = [1.0]
    if dump_raw_dir:
        os.makedirs(dump_raw_dir, exist_ok=True)

    dirs = sorted(glob.glob(os.path.join(root, pattern)))
    print(f"=== Batch plastic coverage: {len(dirs)} directories ===")
    print(f"  mode          : {mode}")
    if mode == "capped":
        print(f"  k_spread sweep: {k_spread_list}")
    print(f"  raw CSV dir   : {dump_raw_dir or '(skipped)'}")
    results = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        atom_f, contact_f = _find_case_files(d)
        if not atom_f or not contact_f:
            print(f"  SKIP {os.path.basename(d)} — missing dump/CSV")
            continue
        try:
            case_name = os.path.basename(d)
            # Per-case se_type: if caller passed se_type=-1 (auto), detect now
            eff_se_type = se_type
            if eff_se_type is None or eff_se_type < 0:
                eff_se_type = detect_se_type(atom_f, case_dir=d)
            dump_contacts = bool(dump_raw_dir)
            res = compute_coverage(atom_f, contact_f, se_type=eff_se_type,
                                   mode=mode,
                                   dump_contacts=dump_contacts,
                                   k_spread_list=k_spread_list)
            res["se_type_used"] = eff_se_type
            # Write raw per-contact CSV (Option C) BEFORE stripping contacts from res
            if dump_raw_dir and "contacts" in res:
                raw_csv = os.path.join(dump_raw_dir, f"raw_delta_r_{case_name}.csv")
                recs = res["contacts"]
                if recs:
                    import csv as _csv
                    with open(raw_csv, "w", newline="") as f:
                        w = _csv.DictWriter(f, fieldnames=list(recs[0].keys()))
                        w.writeheader()
                        w.writerows(recs)
            # Strip contacts list from summary to keep memory down
            if "contacts" in res:
                del res["contacts"]
        except Exception as e:
            print(f"  FAIL {os.path.basename(d)}  {e}")
            continue
        res["case"] = os.path.basename(d)
        results.append(res)
        amp_k1 = res.get('cov_amp_k1_0', res.get('cov_amplification', 0))
        print(f"  OK  {res['case']:30s}  "
              f"elastic={res['elastic_cov_mean']:.3f}  "
              f"plastic_k1.0={res['plastic_cov_mean_k1_0']:.3f}  "
              f"amp={amp_k1:.2f}x  "
              f"dR_mean={res['delta_over_R_mean']:.3f}")

    # Write CSV with ALL columns (k sweep + percentiles)
    if results:
        import csv
        base_keys = ["case", "mode", "n_am", "n_am_with_contact", "n_contacts_am_se",
                     "delta_over_R_mean", "delta_over_R_std",
                     "delta_over_R_p01", "delta_over_R_p05", "delta_over_R_p25",
                     "delta_over_R_p50", "delta_over_R_p75", "delta_over_R_p90",
                     "delta_over_R_p95", "delta_over_R_p99", "delta_over_R_max",
                     "elastic_cov_mean", "elastic_cov_med"]
        # k-specific columns
        for k in k_spread_list:
            kstr = str(k).replace('.', '_')
            base_keys += [f"plastic_cov_mean_k{kstr}",
                          f"plastic_cov_med_k{kstr}",
                          f"cov_amp_k{kstr}"]
        with open(csv_out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=base_keys, extrasaction='ignore')
            w.writeheader()
            for r in results:
                w.writerow({k: r.get(k, "") for k in base_keys})
        print(f"\nWrote {csv_out} ({len(results)} rows, {len(base_keys)} cols)")


def _parse_k_spread(s: str) -> list:
    """Parse '1.0,1.3,1.5,1.65,1.8' → [1.0, 1.3, 1.5, 1.65, 1.8]"""
    if not s:
        return [1.0]
    return [float(x.strip()) for x in s.split(',') if x.strip()]


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="DEM plastic coverage estimator (k_spread sweep + Option C raw CSV)")
    sub = ap.add_subparsers(dest="cmd")

    p1 = sub.add_parser("inspect", help="verify contact dump parsing")
    p1.add_argument("contact_file")
    p1.add_argument("--n-show", type=int, default=5)

    p2 = sub.add_parser("case", help="coverage for single case directory")
    p2.add_argument("case_dir")
    p2.add_argument("--se-type", type=str, default=str(SE_ATOM_TYPE),
                    help="SE atom type (integer) or 'auto' to detect from meta.json / atoms")
    p2.add_argument("--mode", choices=["capped", "physics", "hertzian", "liggghts"],
                    default="capped",
                    help="Plastic film model: 'capped' (k_spread calibration), 'physics' (Tabor+volume, 0 free params, recommended)")
    p2.add_argument("--k-spread", type=str, default="1.0,1.3,1.5,1.65,1.8",
                    help="Comma-separated k_spread values (only applies to 'capped' mode)")
    p2.add_argument("--dump-raw-csv", type=str, default=None,
                    help="Write per-contact CSV to this path (Option C)")

    p3 = sub.add_parser("batch", help="coverage for all cases under a root")
    p3.add_argument("root")
    p3.add_argument("--pattern", default="post_*")
    p3.add_argument("--se-type", type=str, default=str(SE_ATOM_TYPE),
                    help="SE atom type (integer) or 'auto' to detect per-case (recommended for mixed archive)")
    p3.add_argument("--mode", choices=["capped", "physics", "hertzian", "liggghts"],
                    default="capped",
                    help="Plastic film model. 'physics' = Tabor + volume conservation (no free params)")
    p3.add_argument("--csv-out", default="plastic_coverage.csv")
    p3.add_argument("--k-spread", type=str, default="1.0,1.3,1.5,1.65,1.8",
                    help="Comma-separated k_spread values (only applies to 'capped' mode)")
    p3.add_argument("--dump-raw-dir", type=str, default=None,
                    help="Dir to write per-case raw δ/R CSVs (Option C)")

    def _parse_se_type(s):
        """Accept int or 'auto' (returns -1 sentinel for auto-detection)."""
        if s and str(s).lower() == "auto":
            return -1
        try:
            return int(s)
        except (ValueError, TypeError):
            return SE_ATOM_TYPE

    args = ap.parse_args()
    if args.cmd == "inspect":
        main_inspect(args.contact_file, args.n_show)
    elif args.cmd == "case":
        main_case(args.case_dir, _parse_se_type(args.se_type),
                  mode=args.mode,
                  k_spread_list=_parse_k_spread(args.k_spread),
                  dump_raw_csv=args.dump_raw_csv)
    elif args.cmd == "batch":
        main_batch(args.root, args.pattern, _parse_se_type(args.se_type), args.csv_out,
                   mode=args.mode,
                   k_spread_list=_parse_k_spread(args.k_spread),
                   dump_raw_dir=args.dump_raw_dir)
    else:
        ap.print_help()
