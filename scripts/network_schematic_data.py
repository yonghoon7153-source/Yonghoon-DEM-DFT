#!/usr/bin/env python3
"""Single source of truth for the network-solver schematic geometry.

Particle coordinates are taken DIRECTLY from network_ref_coords.json — the
positions traced from the reference figure (leftmost = x0, y up, px/10).
They are rescaled to a convenient drawing range and reused by both the
matplotlib preview and the editable PPTX, so the two outputs are identical.

Edges are CLASSIFIED from the two endpoint phases — never guessed:
  SE-SE -> yellow,  AM-SE -> blue,  AM-AM -> red.
Backbones are auto-selected from the traced particles:
  yellow = a left SE column (Li+ path toward bulk),
  red    = the right AM column (e- path toward SUS).
"""
import os
import json

COORDS_JSON = os.path.join(os.path.dirname(__file__), 'network_ref_coords.json')

SCALE_DIV = 5.0          # px/10 -> drawing units (x ~0-11, y ~0-7.6)
NEAR_FACTOR = 1.8        # contact reach = (r_a+r_b)*FACTOR + GAP
NEAR_GAP = 0.60


def _load_particles():
    raw = json.load(open(COORDS_JSON))
    parts = []
    for o in raw:
        parts.append((o['x'] / SCALE_DIV, o['y'] / SCALE_DIV,
                      o['type'], o['r'] / SCALE_DIV))
    return parts


def _near(a, b):
    d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    reach = (a[3] + b[3]) * NEAR_FACTOR + NEAR_GAP
    return d2 < reach * reach


def _classify(nodes):
    SE = {'SE'}
    edges = {'AM-AM': [], 'AM-SE': [], 'SE-SE': []}
    for i in range(len(nodes)):
        for k in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[k]
            if not _near(a, b):
                continue
            s1 = a[2] in SE; s2 = b[2] in SE
            if s1 and s2:
                edges['SE-SE'].append((a, b))
            elif (not s1) and (not s2):
                edges['AM-AM'].append((a, b))
            else:
                edges['AM-SE'].append((a, b))
    return edges


def _pick_backbones(parts, xmin, xmax, ymin, ymax):
    se = [(x, y, r) for (x, y, t, r) in parts if t == 'SE']
    am = [(x, y, r) for (x, y, t, r) in parts if t == 'AM']

    # red AM backbone: AM in the right zone, ordered top -> bottom
    am_right = sorted([(x, y) for (x, y, r) in am if x > xmin + 0.58 * (xmax - xmin)],
                      key=lambda p: -p[1])
    am_chain = [(float(x), float(y)) for x, y in am_right]

    # yellow SE backbone: pick the SE nearest a left target line per y-band
    tx = xmin + 0.16 * (xmax - xmin)
    nb = 8
    se_chain = []
    for j in range(nb):
        ylo = ymin + (ymax - ymin) * j / nb
        yhi = ymin + (ymax - ymin) * (j + 1) / nb
        band = [(x, y) for (x, y, r) in se if ylo <= y < yhi]
        if not band:
            continue
        bx, by = min(band, key=lambda p: abs(p[0] - tx))
        se_chain.append((float(bx), float(by)))
    se_chain.sort(key=lambda p: p[1])     # bottom -> top
    return se_chain, am_chain


def build():
    parts = _load_particles()
    xs = [p[0] for p in parts]; ys = [p[1] for p in parts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    se_chain, am_chain = _pick_backbones(parts, xmin, xmax, ymin, ymax)
    bb_set = set(se_chain) | set(am_chain)

    nodes = [(x, y, t, r, ((x, y) in bb_set)) for (x, y, t, r) in parts]
    edges = _classify(nodes)

    X0, X1 = xmin - 0.5, xmax + 0.5
    BULK_Y = ymin - 0.45
    SUS_Y = ymax + 0.45
    consts = dict(X0=X0, X1=X1, XMIN=xmin, XMAX=xmax, YMIN=ymin, YMAX=ymax,
                  BULK_Y=BULK_Y, SUS_Y=SUS_Y,
                  TOP=SUS_Y + 0.95, BOT=BULK_Y - 0.95,
                  SE_TOP=ymax, AM_BOT=ymin)
    return {
        'nodes': nodes, 'edges': edges,
        'se_chain': se_chain, 'am_chain': am_chain,
        'se_gap_x': se_chain[-1][0] if se_chain else 0,
        'am_gap_x': am_chain[-1][0] if am_chain else 0,
        'consts': consts,
    }


def spring(p, q, amp=0.05, period=0.24):
    import numpy as np
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
    d = build()
    e = d['edges']
    c = d['consts']
    print(f"nodes={len(d['nodes'])}  AM-AM={len(e['AM-AM'])}  "
          f"AM-SE={len(e['AM-SE'])}  SE-SE={len(e['SE-SE'])}")
    print(f"se_backbone={len(d['se_chain'])} pts, am_backbone={len(d['am_chain'])} pts")
    print(f"x[{c['XMIN']:.2f},{c['XMAX']:.2f}] y[{c['YMIN']:.2f},{c['YMAX']:.2f}]")
