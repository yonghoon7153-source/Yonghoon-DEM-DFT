#!/usr/bin/env python3
"""Single source of truth for the network-solver schematic geometry.

Particle positions are FROZEN to explicit (x, y) coordinates stored in
network_schematic_nodes.json.  build() loads those fixed coordinates, so
the figure is byte-for-byte reproducible forever (independent of numpy /
rng version).  Regenerate the frozen coords only with:

    python3 scripts/network_schematic_data.py --freeze

Both the matplotlib preview and the editable PPTX import build(), so they
always render the identical locked layout.  Edge color is COMPUTED from
the two endpoint phases — never guessed:
  SE-SE -> yellow,  AM-SE -> blue,  AM-AM -> red.
"""
import os
import json
import numpy as np

# ── layout constants (data space, x in [0,10], y in [0,11]) ──
X0, X1 = 0.5, 9.5
SUS_Y, BULK_Y = 10.0, 1.0
SE_TOP, AM_BOT = 8.3, 2.7

# ── density knobs (used ONLY when re-freezing fresh coordinates) ──
GRID_NX, GRID_NY = 10, 10
AM_FRAC = 0.13
R_SE = 0.17
R_AM = (0.28, 0.36)
NEAR_D = 1.25
JITTER = 0.16
SEED = 3

NODES_JSON = os.path.join(os.path.dirname(__file__), 'network_schematic_nodes.json')


def _generate(rng):
    """Generate particle coordinates + backbone chains from rng (for freezing)."""
    nodes = []
    n_se = 9
    se_y = np.linspace(BULK_Y + 0.15, SE_TOP, n_se)
    se_x = 3.0 + 0.50 * np.sin(np.linspace(0.2, 3.4, n_se))
    se_chain = [(float(x), float(y)) for x, y in zip(se_x, se_y)]
    for (x, y) in se_chain:
        nodes.append((x, y, 'SE', 0.20, True))
    se_gap_x = se_chain[-1][0]

    n_am = 9
    am_y = np.linspace(SUS_Y - 0.15, AM_BOT, n_am)
    am_x = 6.7 + 0.40 * np.sin(np.linspace(0.0, 3.0, n_am))
    am_chain = [(float(x), float(y)) for x, y in zip(am_x, am_y)]
    for (x, y) in am_chain:
        nodes.append((x, y, 'AM', 0.30, True))
    am_gap_x = am_chain[-1][0]

    def clash(x, y, r, pad=0.06):
        for (nx, ny, ph, nr, bb) in nodes:
            if (x - nx) ** 2 + (y - ny) ** 2 < (r + nr + pad) ** 2:
                return True
        return False

    gx = np.linspace(X0 + 0.45, X1 - 0.45, GRID_NX)
    gy = np.linspace(BULK_Y + 0.4, SUS_Y - 0.4, GRID_NY)
    for y in gy:
        for x in gx:
            xx = float(x + rng.uniform(-JITTER, JITTER))
            yy = float(y + rng.uniform(-JITTER, JITTER))
            if yy > SE_TOP and abs(xx - se_gap_x) < 0.8:
                continue
            if yy < AM_BOT and abs(xx - am_gap_x) < 0.8:
                continue
            if yy > SE_TOP:
                is_am = True
            elif yy < AM_BOT:
                is_am = False
            else:
                is_am = rng.random() < AM_FRAC
            r = float(rng.uniform(*R_AM)) if is_am else R_SE
            if clash(xx, yy, r):
                continue
            nodes.append((xx, yy, 'AM' if is_am else 'SE', r, False))

    return nodes, se_chain, am_chain, se_gap_x, am_gap_x


def freeze():
    """Generate fresh coordinates and write them to NODES_JSON (locks layout)."""
    rng = np.random.default_rng(SEED)
    nodes, se_chain, am_chain, se_gap_x, am_gap_x = _generate(rng)
    payload = {
        'nodes': [[x, y, ph, r, bb] for (x, y, ph, r, bb) in nodes],
        'se_chain': se_chain, 'am_chain': am_chain,
        'se_gap_x': se_gap_x, 'am_gap_x': am_gap_x,
    }
    with open(NODES_JSON, 'w') as f:
        json.dump(payload, f, indent=1)
    print(f"froze {len(nodes)} particles -> {NODES_JSON}")
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
    """Load FROZEN coordinates (or generate+freeze on first run) and classify edges."""
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


def spring(p, q, amp=0.062, period=0.30):
    """Uniform resistor zigzag polyline between p and q (list of (x,y))."""
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
          f"AM-SE={len(e['AM-SE'])}  SE-SE={len(e['SE-SE'])}  (frozen={os.path.basename(NODES_JSON)})")
