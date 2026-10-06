"""designC2 scratch library — read-only use of HEAD snapshot modules (dfe26fcd4).

Loads a raw LIGGGHTS bed (atom + contact dump + deck), builds the HEAD network
(physics mode, legacy divide) once per channel, then swaps per-edge area / R_c for
design variants and re-solves with HEAD solve_network.  Nothing in the repo is touched.
"""
import os, sys, math, importlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HEAD_SCRIPTS = os.path.join(HERE, 'head', 'scripts')
if HEAD_SCRIPTS not in sys.path:
    sys.path.insert(0, HEAD_SCRIPTS)

import plastic_coverage as PC          # HEAD snapshot
import network_conductivity as NC      # HEAD snapshot

E_SE, E_AM = PC.E_REAL_SE, PC.E_REAL_AM
NU_SE, NU_AM = PC.POISSON_SE, PC.POISSON_AM
H_SE = PC.H_REAL_SE
ESTAR = {
    'AM_SE': PC.E_STAR_AM_SE,
    'SE_SE': 1.0 / (2 * (1 - NU_SE ** 2) / E_SE),
    'AM_AM': 1.0 / (2 * (1 - NU_AM ** 2) / E_AM),
}
PSI_FLOOR = 1e-4


def type_map_from_deck(deck):
    txt = open(deck, errors='replace').read()
    tm = {}
    for raw in txt.split('\n'):
        line = raw.split('#', 1)[0].strip()
        if 'particletemplate/sphere' not in line:
            continue
        toks = line.split()
        t = var = None
        for i, w in enumerate(toks):
            if w == 'atom_type':
                t = int(toks[i + 1])
            if w == 'radius' and toks[i + 1] == 'constant':
                var = toks[i + 2]
        u = var.upper()
        ph = 'AM_P' if 'AM_P' in u else 'AM_S' if 'AM_S' in u else 'SE' if 'SE' in u else 'AM'
        tm[t] = ph
    return tm


def plate_z_from_stl(stl):
    zs = []
    for line in open(stl):
        p = line.split()
        if p and p[0] == 'vertex':
            zs.append(float(p[3]))
    return max(zs)


def load_bed(atom, contact, deck, stl, box=None):
    ra = PC.parse_atom_dump(atom)
    rc = PC.parse_contact_dump(contact)
    atoms = {aid: {'type': int(v['type']), 'radius': float(v['r']),
                   'x': float(v['pos'][0]), 'y': float(v['pos'][1]), 'z': float(v['pos'][2])}
             for aid, v in ra.items()}
    contacts = [{'id1': int(c['id1']), 'id2': int(c['id2']),
                 'contact_area': float(c['contactArea']), 'delta': float(c['delta']),
                 'fn': c['force_normal']} for c in rc]
    tm = type_map_from_deck(deck)
    pz = plate_z_from_stl(stl)
    if box is None:
        # BOX BOUNDS line of the atom dump
        with open(atom) as f:
            lines = [next(f) for _ in range(9)]
        bx = [float(x) for x in lines[5].split()]
        by = [float(x) for x in lines[6].split()]
        box = (bx[1] - bx[0], by[1] - by[0])
    return atoms, contacts, tm, pz, box


def pair_kind(t1, t2, tm):
    a = 'SE' if tm[t1] == 'SE' else 'AM'
    b = 'SE' if tm[t2] == 'SE' else 'AM'
    return {('AM', 'AM'): 'AM_AM', ('SE', 'SE'): 'SE_SE'}.get((a, b), 'AM_SE')


# ─────────────────────────── area rules (µm in, µm² out) ───────────────────────────
def geom_disk(r1, r2, delta):
    """analytic intersection disc (what LIGGGHTS c_cpl[22] reports)."""
    d = r1 + r2 - delta
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    x = (d * d + r1 * r1 - r2 * r2) / (2 * d)
    return max(math.pi * (r1 * r1 - x * x), 0.0)


def area_variant(delta, r1, r2, ligg, pair, *, var, h_nm=5.0, um_per_m=1e6):
    """Return (A_um2, binding, cap_conflict).

    var:
      'G1'      : HEAD legacy physics, called EXACTLY as network_conductivity does (sim units = µm/1000)
      'U'       : DESC-03 only (h in the same length unit; legacy V; legacy rule + elastic branch)
      'UL'      : DESC-03 + L1-02 exact lens (legacy rule + elastic branch)
      'ULA'     : UL with rule A ('cap wins' = film_area_physics_v2 logic)
      'ULB'     : UL + rule B (single floor = A_ligg at every δ, no elastic branch) + disc cap πr_min²
      'ULBP'    : ULB + L1-03 pair rule (SE–SE E*_SE-SE · AM–AM = native A_ligg)
      'ULBPs'   : ULBP but surface cap 2πr_min² (coverage consumer)
    """
    R_star = r1 * r2 / (r1 + r2)
    R_min = min(r1, r2)
    if var == 'G1':
        s = 1e-3                       # µm -> sim (mm) exactly as build_network passes
        A, reg, comp = PC.film_area_from_overlap(delta * s, R_star * s, R_min=R_min * s,
                                                 ligg_area=ligg * s * s, mode='physics',
                                                 return_components=True)
        return A / (s * s), comp.get('binding') or reg, bool(comp.get('cap_conflict'))
    if delta <= 0:
        return ligg, 'none', False
    h = h_nm * 1e-9 * um_per_m        # µm
    dr = delta / R_star
    A_h = math.pi * R_star * delta
    if var in ('U', 'UL', 'ULA') and dr < PC.DR_YIELD_ONSET:
        return A_h, 'elastic', False
    estar = PC.E_STAR_AM_SE
    if var in ('ULBP', 'ULBPs'):
        if pair == 'AM_AM':
            return (ligg if ligg > 0 else geom_disk(r1, r2, delta)), 'native_pair', False
        estar = ESTAR[pair]
    A_tab = (4.0 / 3.0) * estar * math.sqrt(R_star) * delta ** 1.5 / H_SE
    if var == 'U':
        V = PC.legacy_v_overlap(delta, R_star)
    else:
        V = PC.lens_volume(r1, r2, delta)
    A_vol = V / h
    if var in ('ULB', 'ULBP'):
        A_geo = math.pi * R_min ** 2
    else:
        A_geo = 2 * math.pi * R_min ** 2
    U = min(A_tab, A_vol, A_geo)
    capb = 'tabor' if U == A_tab else 'volume' if U == A_vol else 'geom'
    if var == 'ULA':
        L = max(A_h, ligg)
        return U, capb, L > U
    if var in ('U', 'UL'):
        L = max(A_h, ligg)
        A = max(A_h, ligg, U)
        b = ('hertzian' if (A == A_h and A_h >= ligg and A_h >= U) else
             'liggghts' if (A == ligg and ligg >= U) else capb)
        return A, b, L > U
    # rule B: one floor at every δ
    floor = ligg if ligg > 0 else geom_disk(r1, r2, delta)
    A = max(floor, U)
    return A, ('floor' if A == floor and floor >= U else capb), floor > U


# ─────────────────────────── network helpers ───────────────────────────
CHANNELS = {
    'ionic': ('ionic', lambda tm: [t for t, v in tm.items() if v == 'SE']),
    'electronic': ('electronic', lambda tm: [t for t, v in tm.items() if 'AM' in v]),
    'thermal': ('thermal', lambda tm: list(tm.keys())),
}


def build_nets(atoms, contacts, tm, pz, box, scale=1000.0, channels=('ionic', 'electronic', 'thermal')):
    nets = {}
    for ch in channels:
        mode, pick = CHANNELS[ch]
        net = NC.build_network(atoms, contacts, pick(tm), scale, pz, box_x=box[0], box_y=box[1],
                               mode=mode, type_map=tm, contact_mode='physics',
                               psi_placement=NC.PSI_DIVIDE)
        if ch == 'thermal':
            net['is_thermal'] = True
        nets[ch] = net
    return nets


def edge_sigk(e, tm, mode):
    """σ_rel_contact · k_weight exactly as build_network computes it."""
    k = 1.0
    if mode == 'thermal':
        t1se = tm[e['type1']] == 'SE'
        t2se = tm[e['type2']] == 'SE'
        kr = NC.K_AM_THERMAL / NC.K_SE_THERMAL
        k = kr if (not t1se and not t2se) else 1.0 if (t1se and t2se) else 2 * kr / (1 + kr)
    if mode == 'electronic':
        s1 = NC.sigma_AM_relative(e['r1'], tm[e['type1']])
        s2 = NC.sigma_AM_relative(e['r2'], tm[e['type2']])
    else:
        s1 = s2 = 1.0
    return min(s1, s2) * k


def rc_from_area(A, r1, r2, sigk, placement, floor=True):
    rmin = min(r1, r2)
    a = math.sqrt(A / math.pi) if A > 0 else 0.0
    if a <= 0:
        return 1e12, 0.0, 0.0
    a_eff = min(a, rmin)
    s = a_eff / rmin
    psi = max(1.0 - s, 0.0) ** 1.5
    if floor and psi <= PSI_FLOOR:
        return 0.0, s, psi
    if placement == 'multiply':
        return psi / (sigk * 2 * a_eff), s, psi
    if psi <= 0:
        return 0.0, s, psi
    return 1.0 / (sigk * 2 * a_eff * psi), s, psi


def solve(net):
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        G, sr = NC.solve_network(net, mode='full')
    return sr
