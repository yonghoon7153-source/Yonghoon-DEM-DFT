#!/usr/bin/env python3
"""Single source of truth for the network-solver schematic geometry.

NO randomness.  Particle coordinates are fully DETERMINISTIC and fixed:
  • AM (gray) islands + the two backbones are explicit hand-set coordinates
    tracing the reference layout (left yellow SE backbone, right red AM
    backbone column, top AM cluster touching SUS, scattered AM islands).
  • SE (yellow) matrix is filled with a deterministic golden-ratio (R2)
    low-discrepancy sequence — organic-looking but reproducible, not a grid
    and not random.

Coordinates are frozen to network_schematic_nodes.json; build() loads them.
Re-author / re-emit with:  python3 scripts/network_schematic_data.py --freeze

Edge color is COMPUTED from the two endpoint phases — never guessed:
  SE-SE -> yellow,  AM-SE -> blue,  AM-AM -> red.
"""
import os
import json
import numpy as np

# ── layout constants (data space) — wider than tall, like the reference ──
X0, X1 = 0.5, 11.5
SUS_Y, BULK_Y = 10.0, 1.0
SE_TOP, AM_BOT = 8.3, 2.7

R_SE_MIN, R_SE_VAR = 0.160, 0.055     # SE radius base + deterministic variation
PAD = 0.30                            # min gap between particles (airy spacing)
NEAR_D = 1.25

NODES_JSON = os.path.join(os.path.dirname(__file__), 'network_schematic_nodes.json')

# ── explicit AM islands (gray), (x, y, r) — traced from the reference ──
AM_ISLANDS = [
    (2.4, 9.25, 0.34), (3.3, 9.00, 0.30), (5.0, 9.30, 0.36),    # top cluster (touch SUS)
    (5.9, 9.05, 0.32), (7.0, 9.05, 0.30),
    (1.45, 7.55, 0.44),                                          # large upper-left
    (2.15, 5.35, 0.34), (2.95, 5.00, 0.30),                      # mid-left pair
    (5.45, 6.05, 0.42), (5.05, 4.05, 0.34), (6.55, 4.85, 0.28),  # center
    (9.75, 6.45, 0.44), (10.5, 4.60, 0.34), (10.6, 7.55, 0.30),  # right scattered
]

# ── SE backbone (left yellow column), (x, y) bulk -> SE_TOP ──
SE_BACKBONE = [
    (3.55, 1.20), (3.65, 2.10), (3.72, 3.00), (3.60, 3.90), (3.48, 4.80),
    (3.42, 5.70), (3.50, 6.60), (3.62, 7.50), (3.52, 8.30),
]
# ── AM backbone (right red column), (x, y) SUS -> AM_BOT ──
AM_BACKBONE = [
    (8.50, 9.70), (8.60, 8.80), (8.70, 7.90), (8.58, 7.00), (8.68, 6.10),
    (8.78, 5.20), (8.66, 4.30), (8.56, 3.45), (8.66, 2.80),
]


def _generate():
    """Deterministic layout (no rng)."""
    nodes = []

    se_chain = [(float(x), float(y)) for x, y in SE_BACKBONE]
    for (x, y) in se_chain:
        nodes.append((x, y, 'SE', 0.19, True))
    se_gap_x = se_chain[-1][0]

    am_chain = [(float(x), float(y)) for x, y in AM_BACKBONE]
    for (x, y) in am_chain:
        nodes.append((x, y, 'AM', 0.33, True))
    am_gap_x = am_chain[-1][0]

    for (x, y, r) in AM_ISLANDS:
        nodes.append((float(x), float(y), 'AM', float(r), False))

    def clash(x, y, r, pad=PAD):
        for (nx, ny, ph, nr, bb) in nodes:
            if (x - nx) ** 2 + (y - ny) ** 2 < (r + nr + pad) ** 2:
                return True
        return False

    # SE matrix: deterministic golden-ratio (R2) low-discrepancy sequence
    g = 1.32471795724474602596          # plastic number
    a1, a2 = 1.0 / g, 1.0 / (g * g)
    xlo, xhi = X0 + 0.25, X1 - 0.25
    ylo, yhi = BULK_Y + 0.18, SUS_Y - 0.18
    N = 300
    for i in range(1, N + 1):
        ux = (0.5 + a1 * i) % 1.0
        uy = (0.5 + a2 * i) % 1.0
        x = xlo + ux * (xhi - xlo)
        y = ylo + uy * (yhi - ylo)
        if y > SE_TOP:                  # top zone is AM-only (touches SUS)
            continue
        r = R_SE_MIN + R_SE_VAR * ((i * 0.61803398875) % 1.0)
        if clash(x, y, r):
            continue
        nodes.append((float(x), float(y), 'SE', float(r), False))

    return nodes, se_chain, am_chain, se_gap_x, am_gap_x


def freeze():
    nodes, se_chain, am_chain, se_gap_x, am_gap_x = _generate()
    payload = {
        'nodes': [[x, y, ph, r, bb] for (x, y, ph, r, bb) in nodes],
        'se_chain': se_chain, 'am_chain': am_chain,
        'se_gap_x': se_gap_x, 'am_gap_x': am_gap_x,
    }
    with open(NODES_JSON, 'w') as f:
        json.dump(payload, f, indent=1)
    n_am = sum(1 for n in nodes if n[2] == 'AM')
    print(f"froze {len(nodes)} particles ({n_am} AM / {len(nodes)-n_am} SE) -> {NODES_JSON}")
    return payload


def _classify(nodes):
    SE = {'SE'}
    def near(a, b, d=NEAR_D):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 < d * d
    edges = {'AM-AM': [], 'AM-SE': [], 'SE-SE': []}
    for i in range(len(nodes)):
        for k in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[k]
            if not near(a, b):
                continue
            s1 = a[2] in SE; s2 = b[2] in SE
            if s1 and s2:
                edges['SE-SE'].append((a, b))
            elif (not s1) and (not s2):
                edges['AM-AM'].append((a, b))
            else:
                edges['AM-SE'].append((a, b))
    return edges


def build():
    if not os.path.exists(NODES_JSON):
        freeze()
    data = json.load(open(NODES_JSON))
    nodes = [(n[0], n[1], n[2], n[3], n[4]) for n in data['nodes']]
    se_chain = [tuple(p) for p in data['se_chain']]
    am_chain = [tuple(p) for p in data['am_chain']]
    edges = _classify(nodes)
    return {
        'nodes': nodes, 'edges': edges,
        'se_chain': se_chain, 'am_chain': am_chain,
        'se_gap_x': data['se_gap_x'], 'am_gap_x': data['am_gap_x'],
        'consts': dict(X0=X0, X1=X1, SUS_Y=SUS_Y, BULK_Y=BULK_Y,
                       SE_TOP=SE_TOP, AM_BOT=AM_BOT),
    }


def spring(p, q, amp=0.055, period=0.26):
    p = np.array(p, float); q = np.array(q, float)
    v = q - p; L = np.hypot(*v)
    if L < 1e-6:
        return [tuple(p)]
    u = v / L; perp = np.array([-u[1], u[0]])
    lead = 0.18
    n_teeth = max(3, int(round((L * (1 - 2 * lead)) / period)))
    ts = np.linspace(lead, 1 - lead, n_teeth * 2 + 1)
    pts = [tuple(p)]
    for k, t in enumerate(ts):
        off = 0.0 if (k == 0 or k == len(ts) - 1) else amp * (1 if k % 2 else -1)
        pts.append(tuple(p + v * t + perp * off))
    pts.append(tuple(q))
    return pts


if __name__ == '__main__':
    import sys
    if '--freeze' in sys.argv:
        freeze()
    d = build()
    e = d['edges']
    print(f"nodes={len(d['nodes'])}  AM-AM={len(e['AM-AM'])}  "
          f"AM-SE={len(e['AM-SE'])}  SE-SE={len(e['SE-SE'])}")
