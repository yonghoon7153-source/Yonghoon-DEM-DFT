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
def radii_from_rstar_rmin(R_star: float, R_min: float):
    """`(R_star, R_min)` 에서 두 반경을 복원한다 → `(r_min, r_max)` 또는 `None`.

    `R* = r₁r₂/(r₁+r₂)` 이고 `R_min = min(r₁,r₂)` 이면
        `r_max = R*·R_min / (R_min − R*)`   (R_min > R* 일 때만 유효)
    ⚠ `R_min ≤ R*` 는 기하적으로 불가능하다 (`R* < min(r₁,r₂)` 가 항상 성립) ⇒ `None`.
    ⚠ `R_min == R*` 는 `r_max → ∞` (평면) 의 극한이다 ⇒ `None`.
    """
    if not (R_star and R_min) or R_star <= 0 or R_min <= 0:
        return None
    den = R_min - R_star
    if den <= 1e-15 * R_min:
        return None
    return float(R_min), float(R_star * R_min / den)


def lens_volume(r1: float, r2: float, delta: float) -> float:
    """두 구의 **정확한 교집합(lens) 부피**.  `delta = r₁+r₂−d` (중심거리 d).

    `|r₁−r₂| < d < r₁+r₂` 에서
        `V = π (r₁+r₂−d)² · (d² + 2d(r₁+r₂) − 3(r₁−r₂)²) / (12 d)`
    `d ≤ |r₁−r₂|` 이면 작은 구가 큰 구 **안에** 있다 ⇒ `V = (4/3)π·min(r₁,r₂)³`.
    `d ≥ r₁+r₂` 이면 `0`.

    ★ 동일 반경 검산: `d = 2r−δ` 를 넣으면 `V = π δ²(6r − δ)/12` (교과서 형태).
    ★ 얕은 극한: `V → π R* δ²` (`R* = r₁r₂/(r₁+r₂)`).
      ⚠ `plastic_coverage` 의 legacy `V_code = (π/6)δ²(3R*−δ)` 는 그 극한이 **π R* δ²/2**
        = **정확히 절반**이다 (단일 구면 cap 공식에 `R*` 를 넣은 것).  `L1-02`.
    """
    r1 = float(r1); r2 = float(r2); delta = float(delta)
    if r1 <= 0 or r2 <= 0 or delta <= 0:
        return 0.0
    d = r1 + r2 - delta
    if d <= abs(r1 - r2):
        rm = min(r1, r2)
        return float(4.0 / 3.0 * np.pi * rm ** 3)
    if d >= r1 + r2:
        return 0.0
    return float(np.pi * (r1 + r2 - d) ** 2
                 * (d * d + 2.0 * d * (r1 + r2) - 3.0 * (r1 - r2) ** 2) / (12.0 * d))


def legacy_v_overlap(delta: float, R_star: float) -> float:
    """`plastic_coverage.py` 의 **현행(세대 1)** 체적식 — 이름과 달리 lens 가 아니다.

    `V = (π/6)·δ²·(3R* − δ)`.  ⚠ 얕으면 정확 lens 의 **절반**, `δ > 3R*` 이면 **음수**다
    (`L1-02`).  ⛔ **바꾸지 않는다** — 세대 1 산출물이 이 값 위에 서 있다.  올바른 값은
    `lens_volume()` 로 **나란히** 낸다 (계약: 저자 결정 전까지 기본 동작 불변).
    """
    return float(np.pi / 6.0 * (delta ** 2) * (3.0 * R_star - delta))


def film_area_from_overlap(delta: float, R_star: float,
                            R_min: float = None,
                            ligg_area: float = None,
                            mode: str = "capped",
                            k_spread: float = 1.0,
                            return_components: bool = False):
    """Return (contact film area in m², regime label).

    If ``return_components=True`` the third element is a dict with all
    five candidate areas (Hertzian, LIGGGHTS, Tabor, volume, geometric
    cap) plus which cap bound the result. Components for non-physics
    modes are filled with the same scalars where applicable.
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
    elastic_area = np.pi * R_star * delta if R_star > 0 else 0.0

    def _pack(area, regime, *,
              A_hertzian=None, A_ligg=None,
              A_tabor=None, A_volume=None, A_geom=None,
              binding=None, cap_conflict=None,
              A_lower=None, A_upper=None,
              V_legacy=None, V_exact=None, A_vol_exact=None):
        if not return_components:
            return area, regime
        return area, regime, {
            'A_final':    float(area),
            'A_hertzian': float(elastic_area if A_hertzian is None else A_hertzian),
            'A_ligg':     None if A_ligg is None or A_ligg <= 0 else float(A_ligg),
            'A_tabor':    None if A_tabor is None else float(A_tabor),
            'A_volume':   None if A_volume is None or A_volume == float('inf') else float(A_volume),
            'A_geom':     None if A_geom is None else float(A_geom),
            'binding':    binding,    # 'tabor'|'volume'|'geom'|'lower'|'elastic'|None
            'regime':     regime,
            # ── L1-01 · L1-02 계측 (2026-09-13).  ⛔ `A_final` 은 **안 바꾼다** ──
            'cap_conflict':   cap_conflict,      # L > U 라 만족하는 A 가 없다 (L1-01)
            'A_lower':        None if A_lower is None else float(A_lower),
            'A_upper':        None if A_upper is None else float(A_upper),
            'V_overlap_legacy': None if V_legacy is None else float(V_legacy),
            'V_lens_exact':     None if V_exact is None else float(V_exact),
            'A_volume_exact':   None if A_vol_exact is None else float(A_vol_exact),
            'volume_formula': 'legacy_cap_with_Rstar',   # 세대 1 규약 (L1-02 미결)
        }

    if dr <= 0:
        return _pack(0.0, "none")

    if mode == "hertzian":
        regime = ("elastic" if dr < DR_YIELD_ONSET else
                  "transition" if dr < DR_FULLY_PLASTIC else "plastic")
        return _pack(elastic_area, regime, A_ligg=ligg_area)

    if mode == "liggghts":
        regime = ("elastic" if dr < DR_YIELD_ONSET else
                  "transition" if dr < DR_FULLY_PLASTIC else "plastic")
        chosen = ligg_area if (ligg_area is not None and ligg_area > 0) else elastic_area
        return _pack(chosen, regime, A_ligg=ligg_area)

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
            return _pack(elastic_area, "elastic", A_ligg=ligg_area, binding='elastic')

        # Real Hertzian force (using E_real, bypassing DEM's reduced E_eff)
        F_real = (4.0/3.0) * E_STAR_AM_SE_REAL * np.sqrt(R_star) * (delta ** 1.5)

        # Tabor plastic contact area: A = F/H
        A_tabor = F_real / H_REAL_SE

        # Volume-conservation constraint
        # ⚠⚠ `V_overlap` 은 **이름과 달리 구 교집합(lens) 이 아니다** (`L1-02`) —
        #    단일 구면 cap 공식 `(π/6)h²(3R−h)` 에 `R*` 를 넣은 것이라 얕은 극한에서
        #    정확 lens 의 **절반**(`πR*δ²/2` vs `πR*δ²`)이고 `δ > 3R*` 이면 **음수**다.
        #    ⛔ **여기서 바꾸지 않는다** — 세대 1 산출물 전체가 이 값 위에 서 있고,
        #    판정문이 *"기계적으로 전체 lens 로 치환하라는 물리 승인이 아니다"* 라고
        #    못 박았다 (전체 교집합인지 **한 상에 할당된 몫**인지가 저자 결정이다).
        #    정확값은 `V_lens_exact` / `A_volume_exact` 로 **나란히** 보고만 한다.
        V_overlap = legacy_v_overlap(delta, R_star)
        A_volume = V_overlap / H_FILM_MIN if H_FILM_MIN > 0 else float('inf')
        _rr = radii_from_rstar_rmin(R_star, R_min)
        V_lens_exact = lens_volume(_rr[0], _rr[1], delta) if _rr else None
        A_volume_exact = (V_lens_exact / H_FILM_MIN
                          if (V_lens_exact is not None and H_FILM_MIN > 0) else None)

        # Geometric cap: hemisphere of smallest particle (lateral spread ≤ 2πR²)
        r_min_eff = R_min if R_min else R_star
        A_geom = 2.0 * np.pi * (r_min_eff ** 2)

        # Plastic area from Tabor/volume/geometry caps
        A_cap = min(A_tabor, A_volume, A_geom)
        # Identify which cap binds (smallest of the three upper bounds)
        if A_cap == A_tabor:
            cap_binding = 'tabor'
        elif A_cap == A_volume:
            cap_binding = 'volume'
        else:
            cap_binding = 'geom'
        # PHYSICAL LOWER BOUND: plastic area must be ≥ both
        #   (a) the pure-elastic Hertzian point-contact area (π R* δ), AND
        #   (b) the LIGGGHTS-reported contact_area (DEM already accounts for its
        #       internal hooke/hysteresis plasticity — refined physics model
        #       cannot claim LESS contact area than the DEM baseline).
        # Clamping to this max avoids non-physical Physics < Hertzian results.
        ligg_val = ligg_area or 0.0
        # ── L1-01: 하한 > 상한이면 **모든 조건을 만족하는 A 가 없다**.
        #    ⛔ 값을 바꾸지 않는다 (min/max 순서를 뒤집으면 하한을 깨뜨릴 뿐이고,
        #    caps 가 *전체 접촉면적* 의 한계인지 *추가로 퍼진 막* 의 한계인지가 먼저다).
        #    최소 방어 = **기록하고, 검증된 Physics 값으로 승격하지 않기**.
        A_lower_bound = max(elastic_area, ligg_val)
        cap_conflict_flag = bool(A_lower_bound > A_cap)
        A_plastic = max(elastic_area, ligg_val, A_cap)
        # Per-contact binding label = which of the five cases ended up
        # selected. Uses strict equality on the chosen value so the label
        # correctly attributes every contact to exactly one category.
        if A_plastic == elastic_area and elastic_area >= ligg_val and elastic_area >= A_cap:
            binding = 'hertzian'
        elif A_plastic == ligg_val and ligg_val >= A_cap:
            binding = 'liggghts'
        else:
            binding = cap_binding
        regime = "plastic" if dr >= DR_FULLY_PLASTIC else "transition"
        return _pack(A_plastic, regime,
                     A_ligg=ligg_area, A_tabor=A_tabor,
                     A_volume=A_volume, A_geom=A_geom, binding=binding,
                     cap_conflict=cap_conflict_flag,
                     A_lower=A_lower_bound, A_upper=A_cap,
                     V_legacy=V_overlap, V_exact=V_lens_exact,
                     A_vol_exact=A_volume_exact)

    # Default: 'capped' physics model
    # Geometric ceiling: film radius² can't exceed smaller particle's projected area
    cap_a2 = (R_min * R_min) if R_min else (R_star * R_star)
    k2 = k_spread * k_spread

    if dr < DR_YIELD_ONSET:
        return _pack(elastic_area, "elastic", A_ligg=ligg_area)

    if dr < DR_FULLY_PLASTIC:
        # Smooth transition: interpolate elastic → capped plastic (with k_spread)
        f = (dr - DR_YIELD_ONSET) / (DR_FULLY_PLASTIC - DR_YIELD_ONSET)
        plastic_a2_raw = R_star * R_star * dr / DR_FULLY_PLASTIC
        plastic_a2 = min(plastic_a2_raw * k2, cap_a2)
        return _pack((1 - f) * elastic_area + f * np.pi * plastic_a2, "transition",
                     A_ligg=ligg_area)

    # Fully plastic: area grows linearly with dr BEYOND threshold, spread × k², capped
    scale = dr / DR_FULLY_PLASTIC
    plastic_a2_raw = R_star * R_star * scale
    plastic_a2 = min(plastic_a2_raw * k2, cap_a2)
    return _pack(np.pi * plastic_a2, "plastic", A_ligg=ligg_area)


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



# ─── selftest (L1-01 · L1-02) ────────────────────────────────────────────────
def _intersection_disc_area(r1, r2, delta):
    """두 구의 **교차 원판** 면적 (판정문이 `ligg_area` 로 쓴 규약).

    중심거리 `d = r₁+r₂−δ` 일 때 교차원 반지름 a 는
        `a² = [4d²r₁² − (d² − r₂² + r₁²)²] / (4d²)`
    ★ 동일 반경 검산: `A = π δ(4r − δ)/4`, 얕은 극한에서 Hertz(`πR*δ`)의 **2배**
      (`A_LIGG/A_Hertz = 2 − δ/(2r)` = `L1-04` 의 형태).
    """
    d = r1 + r2 - delta
    if d <= 0 or delta <= 0:
        return 0.0
    a2 = (4.0 * d * d * r1 * r1 - (d * d - r2 * r2 + r1 * r1) ** 2) / (4.0 * d * d)
    return float(np.pi * max(a2, 0.0))


def _lens_volume_quadrature(r1, r2, delta, n=400001):
    """정확 lens 를 **독립 수치적분**으로 구한다 (닫힌 식의 교차검증).

    구1 = 원점 반경 r₁ · 구2 = x=d 반경 r₂.  x 단면의 반지름은
    `min(√(r₁²−x²), √(r₂²−(x−d)²))` 이고 그 원 면적을 x 로 적분한다.
    ⚠ 닫힌 식을 **다시 쓰지 않는다** — 그러면 검산이 아니라 동어반복이다.
    """
    d = r1 + r2 - delta
    if d <= 0:
        return float(4.0 / 3.0 * np.pi * min(r1, r2) ** 3)
    lo = max(-r1, d - r2)
    hi = min(r1, d + r2)
    if hi <= lo:
        return 0.0
    x = np.linspace(lo, hi, n)
    a1 = np.sqrt(np.maximum(r1 * r1 - x * x, 0.0))
    a2 = np.sqrt(np.maximum(r2 * r2 - (x - d) ** 2, 0.0))
    a = np.minimum(a1, a2)
    return float(np.trapezoid(np.pi * a * a, x))



def _audit_l1(n=200000, seed=0, dr_lo=-4.0, dr_hi=-0.5):
    """`L1-01` 의 발생률과 `L1-02` 가 사다리를 바꾸는 비율을 **잰다**.

    ⚠⚠ **합성 스윕이다** — 실제 침대의 δ/R* 분포가 아니다.  legacy 169 의 원자료는
       유실됐고 LHS 원자료는 이 컨테이너에 없다 (`SELF-28` 절).  ⇒ 여기 나오는 비율은
       **이 스윕 안에서의 비율**이지 코퍼스 발생률이 아니다.  코퍼스 값은 원자료가 있는
       기계에서 다시 재야 한다.
    δ/R* 는 log-uniform, 반경은 0.25~8 µm log-uniform, `ligg_area` 는 {없음, 0, 교차원판}.

    ★ 비교는 **같은 것끼리** 한다 — 초판이 "최종 결속 라벨"(하한이 이기면 volume 이
      아니다)과 "가장 작은 cap" 을 섞어 세어 *정확 lens 에서 volume 이 더 자주 결속* 이라는
      **불가능한 결과**(정확 lens ≥ legacy 라 덜 결속해야 한다)를 냈다.  두 사다리를
      명시적으로 다시 계산해 (i) 가장 작은 cap 의 정체 (ii) 최종 면적을 각각 비교한다.
    """
    rng = np.random.default_rng(seed)
    n_ladder = 0
    n_conf = 0
    n_neg_legacy = 0
    n_cap_legacy = {'tabor': 0, 'volume': 0, 'geom': 0}
    n_cap_exact = {'tabor': 0, 'volume': 0, 'geom': 0}
    n_cap_changed = 0
    n_final_changed = 0
    rel = []
    for _ in range(n):
        r1 = float(10.0 ** rng.uniform(-0.6, 0.9)) * 1e-6
        r2 = float(10.0 ** rng.uniform(-0.6, 0.9)) * 1e-6
        R_star = r1 * r2 / (r1 + r2)
        R_min = min(r1, r2)
        dr = float(10.0 ** rng.uniform(dr_lo, dr_hi))
        delta = dr * R_star
        pick = rng.integers(0, 3)
        lg = (None if pick == 0 else 0.0 if pick == 1
              else _intersection_disc_area(r1, r2, delta))
        _A, _reg, c = film_area_from_overlap(delta, R_star, R_min=R_min, ligg_area=lg,
                                             mode='physics', return_components=True)
        if c['cap_conflict'] is None:
            continue                       # 탄성 조기반환 — 사다리에 안 온다
        n_ladder += 1
        if c['cap_conflict']:
            n_conf += 1
        if c['V_overlap_legacy'] < 0:
            n_neg_legacy += 1
        if c['A_volume_exact'] is None:
            continue
        lower = c['A_lower']
        caps_l = {'tabor': c['A_tabor'], 'volume': c['A_volume'], 'geom': c['A_geom']}
        caps_e = {'tabor': c['A_tabor'], 'volume': c['A_volume_exact'], 'geom': c['A_geom']}
        wl = min(caps_l, key=lambda k: caps_l[k])
        we = min(caps_e, key=lambda k: caps_e[k])
        n_cap_legacy[wl] += 1
        n_cap_exact[we] += 1
        if wl != we:
            n_cap_changed += 1
        A_l = max(lower, caps_l[wl])
        A_e = max(lower, caps_e[we])
        assert A_l == c['A_final'], (A_l, c['A_final'])      # 사다리 재구성 = 생산값
        if A_e != A_l:
            n_final_changed += 1
            rel.append(A_e / A_l)
    rel = np.asarray(rel) if rel else np.zeros(0)
    pc = lambda k: 100.0 * k / max(n_ladder, 1)
    print(f'합성 접촉 {n:,} (seed {seed}, δ/R* log-uniform 1e{dr_lo:g}~1e{dr_hi:g}) · '
          f'사다리 도달 {n_ladder:,}')
    print(f'  L1-01  cap_conflict (하한 > 상한)         : {n_conf:,} ({pc(n_conf):.3f} % of 사다리)')
    print(f'  L1-02  legacy V_overlap < 0               : {n_neg_legacy:,} ({pc(n_neg_legacy):.3f} %)')
    print(f'  가장 작은 cap — legacy : tabor {n_cap_legacy["tabor"]:,} · '
          f'volume {n_cap_legacy["volume"]:,} · geom {n_cap_legacy["geom"]:,}')
    print(f'  가장 작은 cap — 정확   : tabor {n_cap_exact["tabor"]:,} · '
          f'volume {n_cap_exact["volume"]:,} · geom {n_cap_exact["geom"]:,}')
    print(f'  정확 lens 로 **가장 작은 cap 이 바뀐** 접촉 : {n_cap_changed:,} ({pc(n_cap_changed):.3f} %)')
    print(f'  정확 lens 로 **최종 면적이 바뀐** 접촉      : {n_final_changed:,} ({pc(n_final_changed):.3f} %)')
    if rel.size:
        print(f'    바뀐 접촉의 A_exact/A_legacy: 중앙값 {np.median(rel):.4f} · '
              f'최소 {rel.min():.4f} · 최대 {rel.max():.4f}')
    print()
    print('⚠ 합성 스윕이다 — 코퍼스 발생률이 아니다.  원자료가 있는 기계에서 다시 잴 것.')
    print('⚠ 정확 lens ≥ legacy 이므로 volume 결속은 **줄기만** 해야 한다 (검산 포인트).')
    return 0


def _selftest() -> int:
    """`L1-01`(feasibility) · `L1-02`(lens) 를 판정문 숫자로 못박는다.

    ⚠ 이 검사는 **고쳐졌는지**를 보지 않는다 — 둘 다 저자 결정이 선행이라 값을 안
    바꿨다.  보는 것은 ① 결함이 **계측되는가** ② 계측을 붙였는데 **기본 동작이
    안 바뀌었는가** ③ 검사에 **판별력이 있는가** 셋이다.
    """
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('plastic_coverage (L1-01 · L1-02)')

    # ① L1-02 얕은 극한 — legacy 가 정확 lens 의 **절반**
    r, dlt = 0.5, 0.0125
    lg, ex = legacy_v_overlap(dlt, r / 2.0), lens_volume(r, r, dlt)
    chk('① L1-02 얕은 겹침: legacy = 정확 lens 의 0.493724배 (판정문)',
        abs(lg - 6.0336578e-05) < 1e-11 and abs(ex - 1.22207136e-04) < 1e-11
        and abs(lg / ex - 0.493724) < 1e-6,
        f'{lg:+.12f} vs {ex:+.12f} = {lg / ex:.6f}')

    # ② L1-02 깊은 겹침 — legacy 가 **음수**인데 정확 lens 는 양수
    r, dlt = 0.5, 0.95
    lg, ex = legacy_v_overlap(dlt, r / 2.0), lens_volume(r, r, dlt)
    chk('② L1-02 깊은 겹침: legacy < 0 인데 정확 lens > 0 (판정문)',
        abs(lg + 0.094509578995) < 1e-11 and abs(ex - 0.484361592352) < 1e-11,
        f'{lg:+.12f} vs {ex:+.12f}')

    # ③ 동일 반경 폐형 검산 — πδ²(6r−δ)/12
    for r, dlt in ((1.0, 0.3), (2.5, 1.1), (0.4, 0.79)):
        want = np.pi * dlt ** 2 * (6.0 * r - dlt) / 12.0
        if abs(lens_volume(r, r, dlt) - want) > 1e-12 * max(want, 1e-12):
            ok = False
    chk('③ 동일 반경 폐형: lens_volume = πδ²(6r−δ)/12', ok)

    # ④ **독립 수치적분**과 일치 (비대칭 반경 포함) — 닫힌 식의 교차검증
    worst = 0.0
    for r1, r2, dlt in ((0.5, 6.0, 0.05), (1.0, 1.0, 0.4), (0.3, 2.0, 0.25),
                        (4.0, 0.6, 0.9), (1.5, 1.5, 2.4)):
        a = lens_volume(r1, r2, dlt)
        b = _lens_volume_quadrature(r1, r2, dlt)
        worst = max(worst, abs(a - b) / max(b, 1e-30))
    chk('④ 독립 수치적분과 일치 (비대칭 반경 5쌍, 상대차 < 1e-5)', worst < 1e-5,
        f'최대 상대차 {worst:.3e}')

    # ⑤ 내포 — d ≤ |r₁−r₂| 이면 작은 구 전체
    v = lens_volume(1.0, 5.0, 5.5)          # d = 0.5 < 4
    chk('⑤ 내포(d ≤ |r₁−r₂|): 작은 구 부피 그대로',
        abs(v - 4.0 / 3.0 * np.pi) < 1e-12, f'{v:.12f}')

    # ⑥ 반경 복원 왕복
    r1, r2 = 0.5, 6.0
    got = radii_from_rstar_rmin(r1 * r2 / (r1 + r2), min(r1, r2))
    chk('⑥ (R*, R_min) → (r₁, r₂) 왕복', got is not None
        and abs(got[0] - 0.5) < 1e-12 and abs(got[1] - 6.0) < 1e-9, f'{got}')
    chk('⑥b R_min ≤ R* 는 기하 불가 ⇒ None',
        radii_from_rstar_rmin(0.5, 0.5) is None
        and radii_from_rstar_rmin(0.6, 0.5) is None)

    # ⑦ L1-01 재현 — 얕은 겹침에서 하한 > 상한인데 정상 Physics 면적이 나온다
    r = 0.5e-6
    Rs = r / 2.0
    dlt = 0.01 * Rs
    lgg = _intersection_disc_area(r, r, dlt)
    A, _reg, c = film_area_from_overlap(dlt, Rs, R_min=r, ligg_area=lgg,
                                        mode='physics', return_components=True)
    chk('⑦ L1-01: 하한 > 상한인데 값이 나온다 — 비 1.784757 / 8.016722 (판정문)',
        c['binding'] == 'liggghts' and c['cap_conflict'] is True
        and abs(c['A_final'] / c['A_tabor'] - 1.784757) < 5e-6
        and abs(c['A_final'] / c['A_volume'] - 8.016722) < 5e-6,
        f"binding={c['binding']} conflict={c['cap_conflict']} "
        f"{c['A_final'] / c['A_tabor']:.6f} / {c['A_final'] / c['A_volume']:.6f}")

    # ⑧ 판별력 — 정상 접촉에서는 cap_conflict 가 **안** 켜진다 (⑦ 이 공허하지 않다)
    dlt2 = 0.5 * Rs                          # 깊은 소성 겹침
    _A2, _r2, c2 = film_area_from_overlap(dlt2, Rs, R_min=r,
                                          ligg_area=_intersection_disc_area(r, r, dlt2),
                                          mode='physics', return_components=True)
    chk('⑧ 대조: 깊은 겹침에서는 cap_conflict = False (검사가 공허하지 않다)',
        c2['cap_conflict'] is False, f"binding={c2['binding']}")

    # ⑨ **기본 동작 불변** — 계측을 붙였는데 A_final 이 움직이면 안 된다.
    #    회귀값은 계측 추가 **전** 코드(HEAD~)에서 뜬 것이다.
    #    ⚠ 이 핀들은 **추측이 아니라 실측**이다 — `git show HEAD:scripts/plastic_coverage.py`
    #      를 격리 로드해 찍었다.  초판에서 내가 값을 눈대중으로 적었다가 ⑨ 가 빨간불을
    #      냈다 (π/2 꼴을 그럴듯하게 적은 것).  **회귀 핀을 손으로 짓지 않는다.**
    #      일곱 핀이 결속을 전부 덮는다: hertzian · tabor(양쪽 비대칭) · elastic · transition · **volume ×2**.
    #    ⚠ 2차 정정: 처음 다섯 핀에 **volume 결속 핀이 없었다** — L1-02 가 건드리는 바로 그
    #      자리를 ⑨ 가 안 보고 있었다 (Codex 요청서 §5 에 적고 바로 고쳤다).  두 개 추가.
    pins = [((1.0e-6, 1.0e-6, 0.010), 7.853981633974482e-15),    # hertzian · plastic
            ((0.5e-6, 6.0e-6, 0.200), 6.699127524369602e-13),    # tabor · plastic
            ((2.0e-6, 2.0e-6, 0.001), 3.141592653589793e-15),    # elastic · elastic
            ((0.5e-6, 6.0e-6, 0.002), 1.338430006263107e-15),    # hertzian · transition
            ((3.0e-6, 0.8e-6, 0.050), 1.568078326341361e-13),    # tabor · plastic (역순 반경)
            ((0.5e-6, 0.5e-6, 0.050), 1.2067315531367042e-14),   # **volume** · plastic (동일 반경)
            ((0.5e-6, 6.0e-6, 0.030), 2.7520180051856025e-14)]   # **volume** · plastic (SE↔AM)
    bad = []
    for (ra, rb, dratio), want in pins:
        Rs_ = ra * rb / (ra + rb)
        got_A, _g, _gc = film_area_from_overlap(dratio * Rs_, Rs_, R_min=min(ra, rb),
                                                ligg_area=None, mode='physics',
                                                return_components=True)
        if abs(got_A - want) > 1e-12 * max(abs(want), 1e-30):
            bad.append((ra, rb, dratio, got_A, want))
    chk('⑨ 기본 동작 불변: A_final 이 계측 추가 전 값과 같다', not bad, f'{bad}')

    # ⑩ 판별력 — 계측이 **실제로 다른 값**을 들고 있다 (legacy ≠ exact)
    Rs_ = 0.25e-6
    _A3, _r3, c3 = film_area_from_overlap(0.05 * Rs_, Rs_, R_min=0.5e-6,
                                          mode='physics', return_components=True)
    chk('⑩ 판별력: V_lens_exact 가 legacy 와 실제로 다르다 (약 2배)',
        c3['V_lens_exact'] is not None
        and 1.9 < c3['V_lens_exact'] / c3['V_overlap_legacy'] < 2.1,
        f"{c3['V_overlap_legacy']:.6e} → {c3['V_lens_exact']:.6e} "
        f"({c3['V_lens_exact'] / c3['V_overlap_legacy']:.4f}배)")

    print('plastic_coverage SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="DEM plastic coverage estimator (k_spread sweep + Option C raw CSV)")
    ap.add_argument("--selftest", action="store_true",
                    help="L1-01(feasibility) · L1-02(lens) 회귀")
    ap.add_argument("--audit-l1", action="store_true",
                    help="L1-01 발생률 · L1-02 가 결속을 바꾸는 비율 (합성 스윕)")
    ap.add_argument("--audit-n", type=int, default=200000)
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
    if getattr(args, "selftest", False):
        sys.exit(_selftest())
    if getattr(args, "audit_l1", False):
        sys.exit(_audit_l1(n=args.audit_n))
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
