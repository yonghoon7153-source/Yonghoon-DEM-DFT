#!/usr/bin/env python3
"""Smoke-test the literature-anchored additive what-if (grade_engine.whatif_additives).

Asserts the FIVE validated literature directions (no sim, pure analytic) so a
regression in the model is caught before it reaches the webapp:

  1. PTFE        → porosity ↓  AND σ_ion ↓        (Hong 2026, LPSCl+NCM)
  2. carbon bulk → σ_e ↑       AND σ_ion ↓        (Reisacher p_c; Kim2025 σ_ion)
  3. Super P blocks σ_ion MORE than VGCF (same wt) (our voxel 1.8×; Kim2025)
  4. thinky+Super P → σ_e COLLAPSE, but bulk Super P → σ_e ↑ (POSITION FLIP, Kim2025)
  5. thinky: VGCF σ_e > Super P σ_e               (fiber embeds, sphere blocks; Kim2025)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from grade_engine import whatif_additives

# synthetic base metrics (a typical bimodal composite case)
BASE = {'electronic_sigma_full_mScm': 5.0,     # mS/cm
        'ionic_sigma_full_mScm': 0.10,         # mS/cm
        'porosity_pct': 15.0}

def w(**kw):
    return whatif_additives(BASE, **kw)

fails = []
def check(name, cond, detail=''):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}{('  — ' + detail) if detail else ''}")
    if not cond:
        fails.append(name)

print("=== whatif_additives literature-direction smoke-test ===")

# 1. PTFE → porosity ↓ AND σ_ion ↓
r = w(ptfe_wt=1.0)
check("1a PTFE 1wt% porosity ↓ (≈−6.4%p)", r['porosity_delta_pp'] < -5.0,
      f"Δ={r['porosity_delta_pp']}%p")
check("1b PTFE 1wt% σ_ion ↓ (≈×0.74)", r['sigma_ion_ratio'] < 0.85,
      f"×{r['sigma_ion_ratio']}")

# 2. carbon bulk → σ_e ↑ AND σ_ion ↓
r = w(superp_wt=1.0, mixing='ballmill')
check("2a Super P 1wt% bulk σ_e ↑", r['sigma_e_ratio'] > 1.0, f"×{r['sigma_e_ratio']}")
check("2b Super P 1wt% bulk σ_ion ↓", r['sigma_ion_ratio'] < 1.0, f"×{r['sigma_ion_ratio']}")

# 3. Super P blocks σ_ion MORE than VGCF (same wt, bulk)
rs = w(superp_wt=2.0, mixing='ballmill')
rv = w(vgcf_wt=2.0, mixing='ballmill')
check("3 Super P σ_ion-block > VGCF (2wt%)", rs['sigma_ion_ratio'] < rv['sigma_ion_ratio'],
      f"SP ×{rs['sigma_ion_ratio']} < VGCF ×{rv['sigma_ion_ratio']}")

# 4. POSITION FLIP: thinky+Super P collapses σ_e, bulk Super P boosts σ_e
rt = w(superp_wt=2.9, mixing='thinky')
rb = w(superp_wt=2.9, mixing='ballmill')
check("4a thinky Super P 2.9wt% σ_e COLLAPSE (<1)", rt['sigma_e_ratio'] < 1.0,
      f"×{rt['sigma_e_ratio']}")
check("4b thinky collapse ≈3 decades", rt['flags'].get('superp_coating_collapse', 1) < 2e-3,
      f"block={rt['flags'].get('superp_coating_collapse')}")
check("4c bulk Super P 2.9wt% σ_e ↑ (>1) [flip vs 4a]", rb['sigma_e_ratio'] > 1.0,
      f"×{rb['sigma_e_ratio']}")

# 5. thinky: VGCF σ_e > Super P σ_e
rtv = w(vgcf_wt=2.9, mixing='thinky')
check("5 thinky VGCF σ_e > Super P σ_e", rtv['sigma_e_new'] > rt['sigma_e_new'],
      f"VGCF {rtv['sigma_e_new']} > SP {rt['sigma_e_new']}")

print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
