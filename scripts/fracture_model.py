"""NCM brittle-fracture classifier for DEM AM-AM contacts.

Auerbach (1891) cone-crack onset + Lawn (1998) multi-stage damage
progression, calibrated for NCM 양극재 (Li(Ni,Co,Mn)O₂).

Why this exists
───────────────
LIGGGHTS uses elastic Hertz contact, so when a porosity-target compaction
demands volume that real fracture would relieve, the simulator instead
drives δ/R far above any physical penetration value. We re-interpret
those over-overlapped contacts as **fracture-prone sites** rather than
literal interpenetration. This module turns (δ, R, contact_type) into a
damage stage that downstream tooling (b2_b4_diagnostic, 3D viewer,
metrics DB) can colour / count / threshold.

Material constants (ASSB cathode, NCM)
──────────────────────────────────────
  K_IC_AM_S = 1.0 MPa·m^0.5   single-crystal NCM       Liu 2020
  K_IC_AM_P = 0.3 MPa·m^0.5   polycryst secondary NCM  Quinn 2020
  E_AM      = 140 GPa         Young's modulus          Xu 2017
  NU_AM     = 0.25            Poisson ratio (ceramic)
  H_AM      = 6.0 GPa         hardness (informational) Wang 2020

Dimensionless geometric constant
────────────────────────────────
  A_AUERBACH = 200            Lawn 1998 §3.4 default for "as-prepared"
                               surface (low-flaw 50, rough 500)

Lawn multi-stage thresholds (Table 3.4, with δ ∝ P^(2/3))
─────────────────────────────────────────────────────────
  intact         δ < 1·δ_c
  microcrack     1·δ_c ≤ δ < 2·δ_c
  multicrack     2·δ_c ≤ δ < 5·δ_c
  fragmentation  5·δ_c ≤ δ < 10·δ_c
  pulverization  δ ≥ 10·δ_c

References
──────────
  Auerbach 1891  Ann. Phys. Chem. 43, 61   (cone-crack onset law)
  Lawn 1998      "Fracture of Brittle Solids" 2nd ed., Cambridge
                 (multi-stage damage progression, Table 3.4)
  Liu 2020       Nat. Energy 5, 304        (single crystal K_IC)
  Quinn 2020     Joule 4, 2466             (polycryst K_IC, fragmentation)
  de Vasconcelos 2019  Acta Mater. 178, 35 (fracture toughness method)
  Xu 2017        Phys. Rev. X 7, 041038    (NCM811 nanoindentation)
  Wang 2020      J. Power Sources 470, 228413 (NCM hardness)

Units
─────
  All inputs in SI: δ, R in metres; K_IC in Pa·m^0.5; E in Pa.
  classify_dr() also accepts dimensionless δ/R if R is given as 1.
"""
from __future__ import annotations
import math


# ── NCM material constants ──────────────────────────────────────────────
K_IC_AM_S = 1.0e6     # Pa·m^0.5 — single crystal NCM
K_IC_AM_P = 0.3e6     # Pa·m^0.5 — polycrystalline secondary NCM
E_AM      = 140e9     # Pa — Young's modulus (project-wide convention)
NU_AM     = 0.25      # Poisson ratio
H_AM      = 6.0e9     # Pa — Vickers hardness (informational)

# Auerbach surface-state geometric constant (Lawn 1998 §3.4)
A_AUERBACH = 200.0

# Damage-stage δ multipliers (Lawn 1998 Table 3.4; δ ∝ P^(2/3))
MULT_MICROCRACK    = 1.0
MULT_MULTICRACK    = 2.0
MULT_FRAGMENTATION = 5.0
MULT_PULVERIZATION = 10.0

# Stage ordering for "worst stage" comparisons
STAGE_RANK = {
    'intact':         0,
    'microcrack':     1,
    'multicrack':     2,
    'fragmentation':  3,
    'pulverization':  4,
}
ALL_STAGES = list(STAGE_RANK.keys())


# ── Helpers ─────────────────────────────────────────────────────────────

def k_ic_for_pair(contact_type: str) -> float:
    """Pick K_IC for a contact-type label like 'AM_P-AM_P', 'AM_S-AM_S',
    'AM_P-AM_S' (mixed → geometric mean).
    """
    if contact_type == 'AM_S-AM_S':
        return K_IC_AM_S
    if contact_type == 'AM_P-AM_P':
        return K_IC_AM_P
    if 'AM' in contact_type:
        return math.sqrt(K_IC_AM_S * K_IC_AM_P)
    # SE involved (or unknown): fall back to weakest = polycryst
    return K_IC_AM_P


def auerbach_delta_critical(R_min_m: float, K_IC: float,
                             E: float = E_AM, nu: float = NU_AM,
                             A: float = A_AUERBACH) -> float:
    """δ (m) at which a Hertzian cone crack initiates.

    R_min_m : the smaller of the two contact-pair radii in metres
    K_IC    : Pa·m^0.5
    Returns δ_c in metres.
    """
    if R_min_m <= 0 or K_IC <= 0:
        return float('inf')
    E_star = E / (2.0 * (1.0 - nu * nu))   # equal-sphere effective modulus
    R_star = R_min_m / 2.0                  # effective radius
    P_c    = A * K_IC * K_IC * R_min_m / E_star
    return (3.0 * P_c / (4.0 * E_star * math.sqrt(R_star))) ** (2.0 / 3.0)


def fracture_classify(delta_m: float, R_min_m: float,
                       contact_type: str = 'AM_P-AM_P'
                       ) -> tuple[str, float, float]:
    """δ-based classification (Hertzian-equivalent map).

    Applies Lawn 1998 δ-multipliers (1, 2, 5, 10) — derived from the
    Hertzian force-overlap relation P ∝ δ^(3/2). For DEM systems with a
    *non-Hertzian* contact model (e.g. our LIGGGHTS hooke/hysteresis),
    the δ threshold is interpreted as "what overlap would correspond to
    that fracture stage IF the contact were Hertzian." See
    fracture_classify_force() for the model-agnostic, force-based
    counterpart that bypasses this assumption.

    Returns (stage, delta_c_m, multiplier_m_over_dc).
    """
    K_IC = k_ic_for_pair(contact_type)
    delta_c = auerbach_delta_critical(R_min_m, K_IC)
    if delta_c <= 0 or delta_m <= 0:
        return ('intact', delta_c, 0.0)
    m = delta_m / delta_c
    if   m < MULT_MICROCRACK:    stage = 'intact'
    elif m < MULT_MULTICRACK:    stage = 'microcrack'
    elif m < MULT_FRAGMENTATION: stage = 'multicrack'
    elif m < MULT_PULVERIZATION: stage = 'fragmentation'
    else:                        stage = 'pulverization'
    return (stage, delta_c, m)


# ── Force-based classifier (model-agnostic, primary for Hooke DEM) ──────
# Lawn 1998 §3.4 force multipliers: cone-crack onset at P_c, multi-crack
# at ~3·P_c, fragmentation at ~11·P_c, pulverization at ~32·P_c. These
# are the (3/2)-power images of the δ-multipliers (1, 2, 5, 10).
MULT_FORCE_MICROCRACK    = 1.0
MULT_FORCE_MULTICRACK    = 3.0
MULT_FORCE_FRAGMENTATION = 11.0
MULT_FORCE_PULVERIZATION = 32.0


def fracture_classify_force(F_N: float, R_min_m: float,
                              contact_type: str = 'AM_P-AM_P',
                              E: float = E_AM, nu: float = NU_AM,
                              A: float = A_AUERBACH
                              ) -> tuple[str, float, float]:
    """Force-based fracture classification (recommended for Hooke DEM).

    Bypasses the Hertzian P ∝ δ^(3/2) assumption by comparing the
    DEM-measured contact force F directly against the Auerbach onset
    P_c via Lawn's *force* multipliers (1, 3, 11, 32). Internally
    consistent for AM-AM contacts because the same E_AM = 140 GPa is
    used in both DEM contact-force computation (LIGGGHTS k_n
    calibration) and Auerbach P_c calculation (this function), so the
    Hooke-vs-Hertz form-factor mismatch cancels in the ratio F/P_c.

    For E_SE = 1.35 GPa softened DEM, SE-related contacts are NOT to
    be classified for brittle fracture — SE plasticity is handled by
    the Tabor framework instead.

    Returns (stage, P_c_N, multiplier_F_over_Pc).
    """
    K_IC = k_ic_for_pair(contact_type)
    if R_min_m <= 0 or K_IC <= 0 or F_N <= 0:
        return ('intact', float('inf'), 0.0)
    E_star = E / (2.0 * (1.0 - nu * nu))
    P_c = A * K_IC * K_IC * R_min_m / E_star
    if P_c <= 0:
        return ('intact', P_c, 0.0)
    m = F_N / P_c
    if   m < MULT_FORCE_MICROCRACK:    stage = 'intact'
    elif m < MULT_FORCE_MULTICRACK:    stage = 'microcrack'
    elif m < MULT_FORCE_FRAGMENTATION: stage = 'multicrack'
    elif m < MULT_FORCE_PULVERIZATION: stage = 'fragmentation'
    else:                              stage = 'pulverization'
    return (stage, P_c, m)


def fracture_classify_force_sim(F_N_sim: float, R_min_sim: float,
                                  contact_type: str = 'AM_P-AM_P',
                                  scale: float = 1000.0,
                                  E: float = E_AM, nu: float = NU_AM,
                                  A: float = A_AUERBACH
                                  ) -> tuple[str, float, float]:
    """Sim-units wrapper for force-based classifier.

    Converts both F and R_min from DEM sim units to physical SI:
      R_min_m   = R_min_sim / scale     (length: sim mm → m)
      F_real_N  = F_N_sim   / scale     (force:  sim N  → real N,
                                         per the project DEM scaling
                                         convention real(N) = sim(N) / SCALE)
    Without the F conversion the ratio F/P_c is inflated by a factor of
    SCALE (=1000), which previously caused all contacts to land in the
    pulverization stage spuriously.
    """
    R_min_m = R_min_sim / scale
    F_real_N = F_N_sim / scale
    return fracture_classify_force(F_real_N, R_min_m, contact_type, E, nu, A)


def worse(a: str, b: str) -> str:
    """Return the more severe of two stage labels."""
    return a if STAGE_RANK.get(a, 0) >= STAGE_RANK.get(b, 0) else b


# ── Convenience: sim-units wrapper ──────────────────────────────────────

def fracture_classify_sim(delta_sim: float, R_min_sim: float,
                           contact_type: str = 'AM_P-AM_P',
                           scale: float = 1000.0
                           ) -> tuple[str, float, float]:
    """Same as fracture_classify but inputs are in sim units (e.g. mm
    when scale=1000 sim/m). Returns (stage, delta_c_sim, multiplier).
    """
    delta_m  = delta_sim / scale
    R_min_m  = R_min_sim / scale
    stage, delta_c_m, mult = fracture_classify(delta_m, R_min_m, contact_type)
    delta_c_sim = delta_c_m * scale
    return (stage, delta_c_sim, mult)


__all__ = [
    'K_IC_AM_S', 'K_IC_AM_P', 'E_AM', 'NU_AM', 'H_AM',
    'A_AUERBACH', 'STAGE_RANK', 'ALL_STAGES',
    'MULT_FORCE_MICROCRACK', 'MULT_FORCE_MULTICRACK',
    'MULT_FORCE_FRAGMENTATION', 'MULT_FORCE_PULVERIZATION',
    'k_ic_for_pair',
    'auerbach_delta_critical',
    'fracture_classify',           # δ-based (Hertzian-equivalent)
    'fracture_classify_sim',
    'fracture_classify_force',     # force-based (model-agnostic, primary)
    'fracture_classify_force_sim',
    'worse',
]
