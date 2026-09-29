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
import math
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
    #  ⚠ P2-R2-05 부록: `r_max ≥ r_min` 이므로 `R* = r_min·r_max/(r_min+r_max) ≥ R_min/2` 가
    #    **필요조건**이다.  이 guard 가 없으면 (R*=.1, R_min=.5) 가 (.5, .125) 를 돌려준다 —
    #    r_max < r_min 인 불가능 쌍.  지원 범위: `R_min/2 ≤ R* < R_min`, 반경비 ≲ 1e6
    #    (반경비 5e14 에서는 역산 반경의 lens 부피가 고정밀 대비 1.553배 어긋난다 — 보증 밖).
    if R_star < 0.5 * R_min * (1.0 - 1e-12):
        return None
    den = R_min - R_star
    if den <= 1e-15 * R_min:
        return None
    r_max = float(R_star * R_min / den)
    if r_max / R_min > 1e6:
        return None
    return float(R_min), r_max


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


# =============================================================
#   physics v2 — legacy 'physics' 와 **나란히** (2026-09-29, 1저자 결정 *"권고대로"*)
# =============================================================
#: v2 규칙 한 줄 — coverage 산출물 (`rule_physics_v2`) 에 그대로 실린다.
PHYSICS_V2_RULE = (
    'physics_v2 (2026-09-29): δ/R* < DR_YIELD_ONSET → A = πR*δ (Hertz, legacy 와 같다) · '
    '그 위 → A = U = min(A_tabor, A_volume, A_geom) = cap 은 **전체 접촉면적**의 한계 '
    '(L = max(πR*δ, A_LIGG) > U 면 cap_conflict 로 세고 U 를 낸다 — A 는 A_LIGG · πR*δ 보다 작을 수 있다) · '
    'A_volume = 정확한 전체 lens(r1, r2, δ) / (H_FILM_MIN × length_scale) · '
    '모든 상 쌍에 AM–SE E* · SE H 를 쓴다 (L1-03 은 그대로 열려 있다)')


def _v2_real(name: str, v) -> float:
    """v2 입력 검사 — 실수 · 유한만 받는다 (bool · 문자열 · None · NaN · inf 는 예외)."""
    if isinstance(v, bool) or not isinstance(v, (int, float, np.integer, np.floating)):
        raise TypeError(f'{name}: 실수가 아니다 ({type(v).__name__}: {v!r})')
    x = float(v)
    if not math.isfinite(x):
        raise ValueError(f'{name} 비유한 ({v!r})')
    return x


def film_area_physics_v2(delta, r1, r2, *, length_scale, ligg_area=None):
    """Physics 접촉면적 **v2** → `(A, components)`.  legacy `film_area_from_overlap(mode='physics')` 는
    **그대로** 두고 옆에 선다 (코퍼스 physics σ · Stage E · σ_thermal T1 타깃이 legacy 위에 서 있다).

    ★ 왜 새 함수인가 (새 mode 가 아니라): ① 입력이 다르다 — lens 는 **두 반경**이 필요하고 옛 서명의
      `(R*, R_min)` 역산은 guard (`R* ≥ R_min/2` · 반경비 ≤ 1e6) 를 지나야 한다 (`radii_from_rstar_rmin`) ·
      길이 단위 `length_scale` 은 **필수 키워드**다 (빠뜨리면 `DESC-03` 을 다시 부른다) ② legacy 함수의
      코드를 한 줄도 안 건드려야 기본 동작이 **구성상** 비트 동일하다 (selftest ⑨ 의 핀) ③ 뜻이 다르다
      (하한 max 를 버린다) — 같은 이름 아래 두 계약을 두지 않는다.

    규칙 (1저자 결정 2026-09-29):
      • `δ ≤ 0` → A = 0, binding `'none'` (겹침 없음 = 겹침 모델의 답).
      • `δ/R* < DR_YIELD_ONSET` → A = πR*δ (Hertz 탄성, legacy 탄성 반환과 **비트 동일**), binding `'elastic'`.
      • 그 위 (전이 · 소성) → **A = U = min(A_tabor, A_volume, A_geom)** — cap 은 **전체 접촉면적**의 한계다.
        L = max(πR*δ, A_LIGG) > U 이면 만족하는 면적이 없다 (`L1-01`) ⇒ **cap 이 이긴다** — U 를 내고
        `cap_conflict=True` 로 표시한다 (호출자가 센다).  binding = U 를 준 cap (동률은 tabor → volume → geom).
      • A_tabor = F/H, F = (4/3)E*√R* δ^1.5 (legacy 와 같은 식 · 같은 상수).
      • A_volume = V_lens / h — **V_lens = 두 구의 정확한 교집합** (`lens_volume(r1, r2, δ)` · `L1-02`),
        **h = H_FILM_MIN × length_scale** = δ · r 과 **같은 길이 단위**의 5 nm (`DESC-03`; 상수 자체는 안 바꾼다).
      • A_geom = 2π R_min².

    단위: δ · r1 · r2 는 **1 m = `length_scale` 단위**인 길이 (웹앱 덤프 규약 `scale=1000` ⇒ 덤프 = SI × 1000;
    SI 입력이면 1.0).  `ligg_area` (LIGGGHTS `contact_area` = 기하 교차원판, `L1-04`) 는 그 단위의 제곱이고
    **하한 L 의 판정에만** 쓴다 — 면적 값에는 안 들어간다.  반환 면적도 그 단위의 제곱이다.
    ⇒ 길이 단위를 바꾸면 binding · 충돌은 그대로이고 면적은 정확히 `length_scale²` 배다 (selftest ⑫b·⑫d).

    ⚠⚠ 귀결 (문서에 적으라는 1저자 지시 — 수치는 selftest ⑬b·⑭·⑯ 이 핀으로 문다):
      ① **A_v2 는 LIGGGHTS 기하면적보다 작을 수 있다** — 그리고 πR*δ (Hertz) 보다도 작을 수 있다.
         판정문 기하 (r = 0.5 µm 동일 반경 · δ/R* = 0.01 · SI): A_v2 = 0.4996 πR*δ = 0.2501 A_LIGG
         (legacy 는 A_LIGG 를 냈다).  얕은 lens 는 V_lens ≈ πR*δ² 라 A_volume/πR*δ ≈ δ/h — **δ < 5 nm 인
         모든 cap 가지 접촉에서 부피 cap 이 Hertz 아래로 내려간다**.
      ② 전이 구간 하단에서는 A_tabor 자체가 Hertz 보다 작다: A_tabor/πR*δ = (4E*/3πH)√(δ/R*) =
         11.19·√(δ/R*) < 1  ⟺  δ/R* < 0.00798 (≈ DR_FULLY_PLASTIC).
      ③ 따라서 **DR_YIELD_ONSET 에서 면적이 불연속으로 떨어진다** — r = 0.5 µm SE–SE 면
         πR*δ → 0.0566 πR*δ (부피 cap), 크기와 무관한 Tabor 만 보면 → 0.376 πR*δ.
      ④ 모든 상 쌍 (AM–AM · SE–SE 포함) 에 AM–SE E* · SE 경도를 쓴다 — `L1-03` 은 이 함수로 닫히지 않는다.

    정의역 밖 입력 (실수 아님 · NaN/inf · 반경 ≤ 0 · `length_scale` ≤ 0 · `ligg_area` < 0 ·
    `δ ≥ r1+r2` · 비유한 결과) 은 **예외**다 — 조용히 면적을 내지 않는다.  호출자가 세고 그 침대의 v2 를
    빈칸으로 둔다 (`coverage_physics_vs_hertzian.compute_case`).

    components: `rule` · `A_final` · `A_hertzian` · `A_ligg` · `A_tabor` · `A_volume` · `A_geom` ·
    `A_lower` (L) · `A_upper` (U) · `V_lens` · `h_film` · `binding` · `regime` · `cap_conflict`
    (cap 가지가 아니면 None).
    """
    delta = _v2_real('delta', delta)
    r1 = _v2_real('r1', r1)
    r2 = _v2_real('r2', r2)
    ls = _v2_real('length_scale', length_scale)
    if r1 <= 0 or r2 <= 0:
        raise ValueError(f'반경 ≤ 0 (r1={r1!r}, r2={r2!r})')
    if ls <= 0:
        raise ValueError(f'length_scale ≤ 0 ({ls!r})')
    ligg = None
    if ligg_area is not None:
        ligg = _v2_real('ligg_area', ligg_area)
        if ligg < 0:
            raise ValueError(f'ligg_area < 0 ({ligg!r})')
    if delta >= r1 + r2:
        raise ValueError(f'δ ≥ r1+r2 — 중심거리 ≤ 0, 접촉 기하가 아니다 (δ={delta!r}, r1+r2={r1 + r2!r})')

    R_star = (r1 * r2) / (r1 + r2)          # compute_case 와 같은 식 ⇒ 탄성 가지가 legacy 와 비트 동일
    R_min = min(r1, r2)
    h_film = H_FILM_MIN * ls                 # 5 nm 를 δ · r 과 같은 단위로 (DESC-03)
    comp = dict(rule='physics_v2', A_final=0.0, A_hertzian=None, A_ligg=ligg, A_tabor=None,
                A_volume=None, A_geom=None, A_lower=None, A_upper=None, V_lens=None,
                h_film=h_film, binding='none', regime='none', cap_conflict=None)
    if delta <= 0:
        return 0.0, comp

    A_hertz = np.pi * R_star * delta
    comp['A_hertzian'] = A_hertz
    dr = delta / R_star
    if dr < DR_YIELD_ONSET:
        comp.update(A_final=A_hertz, binding='elastic', regime='elastic')
        return A_hertz, comp

    F_real = (4.0 / 3.0) * E_STAR_AM_SE_REAL * np.sqrt(R_star) * (delta ** 1.5)
    A_tabor = F_real / H_REAL_SE
    V_lens = lens_volume(r1, r2, delta)       # 정확한 전체 교집합 (L1-02)
    A_volume = V_lens / h_film
    A_geom = 2.0 * np.pi * (R_min ** 2)
    U = min(A_tabor, A_volume, A_geom)
    if U == A_tabor:
        binding = 'tabor'
    elif U == A_volume:
        binding = 'volume'
    else:
        binding = 'geom'
    L = max(A_hertz, ligg if ligg is not None else 0.0)
    for _n, _v in (('A_tabor', A_tabor), ('A_volume', A_volume), ('A_geom', A_geom), ('A_lower', L)):
        if not math.isfinite(_v):
            raise ValueError(f'{_n} 비유한 ({_v!r}) — δ={delta!r}, r1={r1!r}, r2={r2!r}')
    comp.update(A_final=float(U), A_tabor=float(A_tabor), A_volume=float(A_volume),
                A_geom=float(A_geom), A_lower=float(L), A_upper=float(U), V_lens=float(V_lens),
                binding=binding, regime=('plastic' if dr >= DR_FULLY_PLASTIC else 'transition'),
                cap_conflict=bool(L > U))
    return float(U), comp


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
    chk('⑥c R* < R_min/2 도 기하 불가 ⇒ None (Codex: (.1,.5) 가 (.5,.125) 를 돌려줬다)',
        radii_from_rstar_rmin(0.1, 0.5) is None and radii_from_rstar_rmin(0.25, 0.5) == (0.5, 0.5))
    chk('⑥d 지원 반경비 밖(> 1e6)은 None (반경비 5e14 에서 lens 1.553배 어긋남 — 보증 밖)',
        radii_from_rstar_rmin(0.5 * (1 - 1e-8), 0.5) is None)

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
    #      열한 핀이 결속 여섯 가지를 전부 덮는다 — ⑨b 가 집합으로 강제한다.
    #    ⚠ 2차 정정: 처음 다섯 핀에 **volume 결속 핀이 없었다** — L1-02 가 건드리는 바로 그
    #      자리를 ⑨ 가 안 보고 있었다 (Codex 요청서 §5 에 적고 바로 고쳤다).  두 개 추가.
    #    3차: **liggghts 결속 핀**도 없었다 (Codex 요청서 §5 에 스스로 적어 둔 구멍) — 교차원판을
    #      `ligg_area` 로 넣은 얕은 겹침 2개 추가.  핀 값은 역시 계측 전 코드에서 실측.
    #      ⇒ 열한 핀이 결속 **여섯 가지 전부**를 덮는다 (⑨b 가 집합으로 강제): hertzian · tabor ·
    #         elastic · volume · liggghts · geom.
    pins = [((1.0e-6, 1.0e-6, 0.010, None), 7.853981633974482e-15),    # hertzian · plastic
            ((0.5e-6, 6.0e-6, 0.200, None), 6.699127524369602e-13),    # tabor · plastic
            ((2.0e-6, 2.0e-6, 0.001, None), 3.141592653589793e-15),    # elastic · elastic
            ((0.5e-6, 6.0e-6, 0.002, None), 1.338430006263107e-15),    # hertzian · transition
            ((3.0e-6, 0.8e-6, 0.050, None), 1.568078326341361e-13),    # tabor · plastic (역순 반경)
            ((0.5e-6, 0.5e-6, 0.050, None), 1.2067315531367042e-14),   # **volume** · plastic (동일 반경)
            ((0.5e-6, 6.0e-6, 0.030, None), 2.7520180051856025e-14),   # **volume** · plastic (SE↔AM)
            ((0.5e-6, 0.5e-6, 0.010, 3.9220820784660005e-15), 3.9220820784660005e-15),  # **liggghts** · plastic
            ((0.5e-6, 6.0e-6, 0.005, 6.678979268489997e-15), 6.678979268489997e-15),   # **liggghts** · transition
            ((0.5e-6, 0.5e-6, 0.900, None), 1.5707963267948965e-12),   # **geom** · plastic (= 2πR_min²)
            ((0.5e-6, 6.0e-6, 0.500, None), 1.5707963267948965e-12)]   # **geom** · plastic (SE↔AM)
    bad = []
    seen_bindings = set()
    for (ra, rb, dratio, lg), want in pins:
        Rs_ = ra * rb / (ra + rb)
        got_A, _g, _gc = film_area_from_overlap(dratio * Rs_, Rs_, R_min=min(ra, rb),
                                                ligg_area=lg, mode='physics',
                                                return_components=True)
        seen_bindings.add(_gc['binding'])
        if abs(got_A - want) > 1e-12 * max(abs(want), 1e-30):
            bad.append((ra, rb, dratio, got_A, want))
    chk('⑨ 기본 동작 불변: A_final 이 계측 추가 전 값과 같다', not bad, f'{bad}')
    chk('⑨b 핀이 결속 여섯 가지를 **전부** 덮는다 (덮지 않는 결속은 ⑨ 가 안 본 자리다)',
        seen_bindings == {'hertzian', 'tabor', 'elastic', 'volume', 'liggghts', 'geom'},
        f'{sorted(seen_bindings)}')

    # ⑩ 판별력 — 계측이 **실제로 다른 값**을 들고 있다 (legacy ≠ exact)
    Rs_ = 0.25e-6
    _A3, _r3, c3 = film_area_from_overlap(0.05 * Rs_, Rs_, R_min=0.5e-6,
                                          mode='physics', return_components=True)
    chk('⑩ 판별력: V_lens_exact 가 legacy 와 실제로 다르다 (약 2배)',
        c3['V_lens_exact'] is not None
        and 1.9 < c3['V_lens_exact'] / c3['V_overlap_legacy'] < 2.1,
        f"{c3['V_overlap_legacy']:.6e} → {c3['V_lens_exact']:.6e} "
        f"({c3['V_lens_exact'] / c3['V_overlap_legacy']:.4f}배)")

    ok = _selftest_v2(chk) and ok

    print('plastic_coverage SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _v2_contract_area(delta, r1, r2, ligg, length_scale):
    """⑪–⑱ 계약 시험의 어댑터 — **coverage 가 쓰는 Physics 면적 경로**를 부른다.

    `film_area_physics_v2` 가 있으면 그것을, 없으면 **옛 생산 경로** (`compute_case` 가 부르는
    그대로: `film_area_from_overlap(mode='physics')`, `length_scale` 는 읽지 않는다) 를 부른다.
    ⇒ 같은 계약 시험이 옛 코드에서는 **판정문 숫자로 실패**하고 (반례 먼저), v2 에서 통과한다.
    """
    fn = globals().get('film_area_physics_v2')
    if fn is not None:
        A, c = fn(delta, r1, r2, ligg_area=ligg, length_scale=length_scale)
        return dict(src='v2', A=A, binding=c['binding'], conflict=c['cap_conflict'],
                    V=c['V_lens'], U=c['A_upper'], L=c['A_lower'], A_hertz=c['A_hertzian'])
    R_star = (r1 * r2) / (r1 + r2)
    A, _reg, c = film_area_from_overlap(delta, R_star, R_min=min(r1, r2), ligg_area=ligg,
                                        mode='physics', return_components=True)
    return dict(src='legacy', A=A, binding=c['binding'], conflict=c['cap_conflict'],
                V=c['V_overlap_legacy'], U=c['A_upper'], L=c['A_lower'], A_hertz=c['A_hertzian'])


def _selftest_v2(chk) -> bool:
    """physics **v2** 계약 (2026-09-29 1저자 결정 *"권고대로"*) — `DESC-03` · `L1-01` · `L1-02` 를 판정문 숫자로.

    계약: ① cap 은 **전체 접촉면적**의 한계 — 소성/전이 가지에서 A = U = min(Tabor, 부피, 기하),
    L = max(πR*δ, A_ligg) > U 면 **U 를 내고** 충돌을 기록 ② 부피 = **정확한 전체 lens** (두 반경)
    ③ 막 두께 = δ · r 과 **같은 길이 단위** (`H_FILM_MIN × length_scale`) ④ 항복 전 = Hertz (legacy 그대로)
    ⑤ 정의역 밖 입력은 조용히 값을 내지 않고 **예외** (호출자가 세고 침대를 빈칸으로 둔다).
    """
    ok = True

    def c2(name, cond, extra=''):
        nonlocal ok
        chk(name, cond, extra)
        ok = ok and bool(cond)

    def _safe(f):
        try:
            return f(), None
        except Exception as e:                       # noqa: BLE001 — 계약 시험: 예외도 결과다
            return None, f'{type(e).__name__}: {e}'

    print('plastic_coverage physics v2 (DESC-03 · L1-01 · L1-02 — 1저자 결정 2026-09-29)')

    # ⑪ L1-02 — v2 의 부피 = 정확한 전체 lens (판정문: r=0.5 µm · δ=0.0125 µm, legacy 는 그 0.493724 배)
    r, dlt = 0.5, 0.0125                               # µm 단위 ⇒ length_scale = 1e6 (1 m = 1e6 µm)
    got, err = _safe(lambda: _v2_contract_area(dlt, r, r, None, 1e6))
    ex = lens_volume(r, r, dlt)
    ok11 = (got is not None and got['V'] is not None and abs(got['V'] - ex) <= 1e-12 * ex
            and abs(legacy_v_overlap(dlt, r / 2.0) / ex - 0.493724) < 1e-6)
    c2('⑪ ★ L1-02: coverage Physics 경로의 부피 = 정확한 lens (legacy 는 그 0.493724 배)', ok11,
       (f"[{got['src']}] V={got['V']:.12e} · lens={ex:.12e} · V/lens={got['V'] / ex:.6f}") if got else err)

    # ⑫ DESC-03 — 길이 단위 공변: 같은 기하를 SI(m) 와 덤프 단위(×1000) 로 넣으면 결속이 같고 면적은 정확히 1e6 배.
    #    판정문 재현 (옛 경로): 덤프 단위 tabor · A/A_H = 2.502607 ↔ SI volume · 1.229167 (결속이 **뒤집힌다**).
    r_si, dr = 0.5e-6, 0.05
    Rs_si = r_si / 2.0
    d_si = dr * Rs_si
    _Al, _rl, cl_si = film_area_from_overlap(d_si, Rs_si, R_min=r_si, mode='physics', return_components=True)
    _Ad, _rd, cl_dm = film_area_from_overlap(d_si * 1e3, Rs_si * 1e3, R_min=r_si * 1e3, mode='physics',
                                             return_components=True)
    c2('⑫a DESC-03 재현 (옛 경로 — 바꾸지 않았다): 덤프 단위 tabor 2.502607 ↔ SI volume 1.229167',
       cl_dm['binding'] == 'tabor' and cl_si['binding'] == 'volume'
       and abs(_Ad / cl_dm['A_hertzian'] - 2.502607) < 5e-7 and abs(_Al / cl_si['A_hertzian'] - 1.229167) < 5e-7,
       f"dump={cl_dm['binding']} {_Ad / cl_dm['A_hertzian']:.6f} · SI={cl_si['binding']} {_Al / cl_si['A_hertzian']:.6f}")
    g_si, e1 = _safe(lambda: _v2_contract_area(d_si, r_si, r_si, None, 1.0))
    g_dm, e2 = _safe(lambda: _v2_contract_area(d_si * 1e3, r_si * 1e3, r_si * 1e3, None, 1e3))
    c2('⑫b ★ DESC-03: 단위를 바꿔도 결속이 같고 면적은 정확히 (1e3)² 배 — 단위 교정 뒤 volume cap 이 결속한다',
       g_si is not None and g_dm is not None and g_si['binding'] == g_dm['binding'] == 'volume'
       and abs(g_dm['A'] / (g_si['A'] * 1e6) - 1.0) < 1e-12,
       (f"[{g_si['src']}] SI={g_si['binding']} · dump={g_dm['binding']} · "
        f"A_dump/(A_SI·1e6)={g_dm['A'] / (g_si['A'] * 1e6):.12f}") if (g_si and g_dm) else (e1 or e2))
    c2('⑫c v2 값 = 정확 lens / 5 nm: A/A_H = (δ/h)(1 − δ/(6r)) = 2.489583 (옛 1.229167 · 2.502607 과 다르다)',
       g_si is not None and abs(g_si['A'] / g_si['A_hertz'] - 2.5 * (1.0 - 0.025 / 6.0)) < 1e-9,
       f"{g_si['A'] / g_si['A_hertz']:.9f}" if g_si else e1)
    #    공변 스윕 — 결속 세 가지 모두에서 (tabor · volume · geom)
    bad = []
    for (ra, rb, drr) in ((5.0e-6, 5.0e-6, 0.01), (0.5e-6, 0.5e-6, 0.05), (0.5e-6, 0.5e-6, 0.9),
                          (0.5e-6, 6.0e-6, 0.03), (3.0e-6, 0.8e-6, 0.2), (0.5e-6, 6.0e-6, 0.004)):
        Rs_ = ra * rb / (ra + rb)
        a, ea = _safe(lambda: _v2_contract_area(drr * Rs_, ra, rb, None, 1.0))
        b, eb = _safe(lambda: _v2_contract_area(drr * Rs_ * 1e3, ra * 1e3, rb * 1e3, None, 1e3))
        if a is None or b is None or a['binding'] != b['binding'] or abs(b['A'] / (a['A'] * 1e6) - 1.0) > 1e-12:
            bad.append((ra, rb, drr, (a or {}).get('binding'), (b or {}).get('binding'), ea or eb))
    c2('⑫d ★ 공변 스윕 6 기하 (소성 · 전이 · 역순 반경 · 깊은 겹침): 결속 · 면적 비 전부 일치', not bad, f'{bad}')

    # ⑬ L1-01 — 하한 > 상한이면 **상한(U)을 낸다** + 충돌 기록 (판정문 기하: SI r=0.5 µm · δ/R*=0.01 · ligg=교차원판)
    r = 0.5e-6
    Rs = r / 2.0
    dlt = 0.01 * Rs
    lgg = _intersection_disc_area(r, r, dlt)
    got, err = _safe(lambda: _v2_contract_area(dlt, r, r, lgg, 1.0))
    c2('⑬ ★ L1-01: L > U 이면 U 를 낸다 (cap = 전체 면적 한계) · cap_conflict=True · 결속 volume',
       got is not None and got['conflict'] is True and got['A'] == got['U'] and got['A'] < got['L']
       and got['binding'] == 'volume',
       (f"[{got['src']}] A/U={got['A'] / got['U']:.6f} · L/U={got['L'] / got['U']:.6f} · "
        f"binding={got['binding']} · conflict={got['conflict']}") if got else err)
    c2('⑬b L1-01 값: A/A_H = (δ/h)(1 − δ/(6r)) = 0.4995833 · L/U = 1.9975/0.4995833',
       got is not None and abs(got['A'] / got['A_hertz'] - 0.5 * (1.0 - 0.0025 / 3.0)) < 1e-9
       and abs(got['L'] / got['U'] - 1.9975 / (0.5 * (1.0 - 0.0025 / 3.0))) < 1e-9,
       (f"A/A_H={got['A'] / got['A_hertz']:.9f} · L/U={got['L'] / got['U']:.9f}") if got else err)
    # ⑭ 귀결 핀 (저자에게 알릴 것): v2 면적은 LIGGGHTS 기하면적보다 — 여기서는 Hertz 면적보다도 — **작을 수 있다**
    c2('⑭ 귀결: A_v2 < A_LIGG (기하 교차원판) 이고 A_v2 < πR*δ 이기도 하다 (⑬ 의 기하)',
       got is not None and got['A'] < lgg and got['A'] < got['A_hertz'],
       (f"A_v2/A_LIGG={got['A'] / lgg:.6f} · A_v2/A_H={got['A'] / got['A_hertz']:.6f}") if got else err)

    # ⑮ 항복 전 = Hertz 탄성 면적 (legacy 'physics' 탄성 반환과 **비트 동일**)
    bad = []
    for (ra, rb, drr) in ((0.5e-6, 0.5e-6, 0.001), (2.0e-6, 2.0e-6, 0.0005), (0.5e-6, 6.0e-6, 0.00099)):
        Rs_ = ra * rb / (ra + rb)
        a, ea = _safe(lambda: _v2_contract_area(drr * Rs_, ra, rb, None, 1.0))
        Al, _r0, cl = film_area_from_overlap(drr * Rs_, Rs_, R_min=min(ra, rb), mode='physics', return_components=True)
        if a is None or a['A'] != Al or a['binding'] != 'elastic' or cl['binding'] != 'elastic':
            bad.append((ra, rb, drr, (a or {}).get('A'), Al, ea))
    c2('⑮ δ/R* < DR_YIELD_ONSET: A = πR*δ — legacy physics 탄성 반환과 비트 동일', not bad, f'{bad}')

    # ⑯ 귀결 핀: DR_YIELD_ONSET 에서 면적이 **불연속**으로 떨어진다 (얕은 lens 가 5 nm 막보다 얇다).
    #    기대값은 닫힌 lens 식이 아니라 **독립 수치적분**으로 만든다 (동어반복 금지).
    r = 0.5e-6
    Rs = r / 2.0
    lo = _safe(lambda: _v2_contract_area(DR_YIELD_ONSET * (1 - 1e-9) * Rs, r, r, None, 1.0))[0]
    hi = _safe(lambda: _v2_contract_area(DR_YIELD_ONSET * (1 + 1e-9) * Rs, r, r, None, 1.0))[0]
    d_hi = DR_YIELD_ONSET * (1 + 1e-9) * Rs
    want = (_lens_volume_quadrature(r, r, d_hi) / H_FILM_MIN) / (np.pi * Rs * d_hi)
    c2('⑯ 귀결: 항복 개시에서 A 가 πR*δ → V_lens/h 로 떨어진다 (r=0.5 µm SE–SE: 약 0.0566 배 · 독립 적분 대조)',
       lo is not None and hi is not None and lo['binding'] == 'elastic' and hi['binding'] == 'volume'
       and abs((hi['A'] / hi['A_hertz']) / want - 1.0) < 1e-6,
       (f"[{hi['src']}] 위 {hi['A'] / hi['A_hertz']:.6f} · 기대 {want:.6f} · 아래 {lo['A'] / lo['A_hertz']:.6f}")
       if (lo and hi) else '')

    # ⑰ 정의역 밖은 **예외** (옛 경로는 NaN 을 조용히 면적으로 냈다) · δ ≤ 0 은 면적 0 ('none')
    raised = []
    for label, args in (('δ=NaN', (float('nan'), 0.5e-6, 0.5e-6, None, 1.0)),
                        ('δ=inf', (float('inf'), 0.5e-6, 0.5e-6, None, 1.0)),
                        ('r1=0', (1e-9, 0.0, 0.5e-6, None, 1.0)),
                        ('r2=NaN', (1e-9, 0.5e-6, float('nan'), None, 1.0)),
                        ('ligg<0', (1e-9, 0.5e-6, 0.5e-6, -1e-18, 1.0)),
                        ('ligg=NaN', (1e-9, 0.5e-6, 0.5e-6, float('nan'), 1.0)),
                        ('scale=0', (1e-9, 0.5e-6, 0.5e-6, None, 0.0)),
                        ('scale=NaN', (1e-9, 0.5e-6, 0.5e-6, None, float('nan'))),
                        ('δ≥r1+r2', (1.0e-6, 0.5e-6, 0.5e-6, None, 1.0))):
        g, e = _safe(lambda: _v2_contract_area(*args))
        if e is None:
            raised.append(f'{label}→{g["A"]!r}({g["src"]})')
    c2('⑰ ★ 정의역 밖 입력 9 가지 → 예외 (조용히 면적을 내지 않는다)', not raised, f'{raised}')
    z0, e0 = _safe(lambda: _v2_contract_area(0.0, 0.5e-6, 0.5e-6, 1e-15, 1.0))
    zn, en = _safe(lambda: _v2_contract_area(-1e-10, 0.5e-6, 0.5e-6, None, 1.0))
    c2('⑰b δ ≤ 0 → 면적 0 · binding none (겹침 없음 = 겹침 모델의 답)',
       z0 is not None and zn is not None and z0['A'] == 0.0 == zn['A']
       and z0['binding'] == 'none' == zn['binding'],
       f"{(z0 or {}).get('binding')} {(zn or {}).get('binding')} {e0 or ''}{en or ''}")

    # ⑱ 판별력 — 결속 다섯 가지 (elastic · tabor · volume · geom · none) 가 전부 실제로 나온다
    seen = set()
    for (ra, rb, drr) in ((0.5e-6, 0.5e-6, 0.0005), (5.0e-6, 5.0e-6, 0.01), (0.5e-6, 0.5e-6, 0.05),
                          (0.5e-6, 0.5e-6, 0.9), (0.5e-6, 0.5e-6, 0.0)):
        Rs_ = ra * rb / (ra + rb)
        g, _e = _safe(lambda: _v2_contract_area(drr * Rs_, ra, rb, None, 1.0))
        if g is not None:
            seen.add(g['binding'])
    c2('⑱ 결속 다섯 가지가 전부 나온다 (elastic · tabor · volume · geom · none)',
       seen == {'elastic', 'tabor', 'volume', 'geom', 'none'}, f'{sorted(map(str, seen))}')
    return ok


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
