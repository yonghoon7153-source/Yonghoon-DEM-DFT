"""Actual deck generation in memory + algebraic counterexamples; no DEM launch or deck write."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
import make_mixer_deck as g

p = g.plan(100000, cgf=151.4)
rpm = g.resolve_rpm(p['R'])
decks = {}
for arm in ('LC', 'LH'):
    text = g.deck(p, rpm, 8, seed=32452843, arm=arm)
    rows = text.splitlines()
    indexed = [(i + 1, s.strip()) for i, s in enumerate(rows) if s.strip() and not s.lstrip().startswith('#')]
    ced = next(i for i,s in indexed if s.startswith('fix mC '))
    first_run = next(i for i,s in indexed if s.startswith('run '))
    second_insert = next(i for i,s in indexed if s.startswith('fix insB '))
    checkpoint = next(i for i,s in indexed if s.startswith('write_restart '))
    rotation = next(i for i,s in indexed if s.startswith('fix mvD '))
    decks[arm] = {'in_memory_deck_sha256': hashlib.sha256(text.encode()).hexdigest(),
                  'CED_line': ced, 'first_run_line': first_run,
                  'second_phase_insertion_line': second_insert,
                  'settled_checkpoint_line': checkpoint, 'rotation_start_line': rotation,
                  'CED_precedes_first_run': ced < first_run,
                  'order_insert_then_checkpoint_then_rotation': second_insert < checkpoint < rotation,
                  'runs': [(i,s) for i,s in indexed if s.startswith('run ')],
                  'CED_matrix_J_m3': g.ced_matrix(arm, p['d'])}
assert all(d['CED_precedes_first_run'] and d['order_insert_then_checkpoint_then_rotation'] for d in decks.values())
# Per-arm errors do not bound the contrast by the same number.
soft = {'LC': .60, 'LH': .50}
ref = {'LC': .58, 'LH': .52}
eLC, eLH = soft['LC'] - ref['LC'], soft['LH'] - ref['LH']
effect_error = (soft['LC'] - soft['LH']) - (ref['LC'] - ref['LH'])
# Same E0 denominator changes the effect; it does not algebraically cancel.
s0, sLC, sLH = .20, .04, .06
shared_reference = []
for sr in (.01, .03):
    mLC, mLH = (s0-sLC)/(s0-sr), (s0-sLH)/(s0-sr)
    shared_reference.append({'S0_sq':s0,'S_LC_sq':sLC,'S_LH_sq':sLH,'SR_sq':sr,
                             'M_LC':mLC,'M_LH':mLH,'difference':mLC-mLH})
print(json.dumps({'scope':'Actual generator in memory; synthetic algebra, not campaign measurements',
                  'decks':decks,'per_arm_budget_counterexample': {'LC_error':eLC,'LH_error':eLH,
                  'contrast_error':effect_error},'shared_E0_does_not_cancel':shared_reference}, indent=2))
