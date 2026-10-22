# -*- coding: utf-8 -*-
"""탐침 2-G (Q-G) — R 런 계획 꼴 · 결과 전 등록 숫자 관문 (`rint_r_chain.load_plan` · `require_plan_numbers`).
null · NaN 토큰 · 1e400 (→ inf) · 음수 · 문자열 · bool · 큰 정수 (10**400) · 정상.  기대 = 구조화 멈춤 (Stop PLAN_INVALID · PLAN_NUMBER_UNREGISTERED)."""
import json
import os
import sys
import tempfile
REPO = os.environ.get('PRE_REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d')
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import rint_r_chain as RRC     # noqa: E402

BASE = {'schema': 'rint-r-plan-v2', 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.6, 'tol_ff_um': 0.05,
        'step3_rtol': 1e-12, 'p2_extra': '', 'max_ladder_points': 14, 'calib_rj_ratio_max': 'none', 'sv_cf_threshold': 2.0,
        'sv_cf_scope': 'R_j0'}
BIG = '1' + '0' * 400


def run(tag, text):
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'plan.json')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(text)
        try:
            obj, _sha = RRC.load_plan(p)
            RRC.require_plan_numbers(obj)
            res = 'ACCEPTED'
        except RRC.Stop as e:
            res = f'Stop {e.code}'
        except Exception as e:          # noqa: BLE001
            res = f'UNCAUGHT {type(e).__name__}: {str(e)[:80]}'
    print(f'{tag:42s} → {res}')
    return res


def variant(**kw):
    d = dict(BASE)
    d.update(kw)
    return json.dumps(d)


out = {}
out['base'] = run('base (정상)', variant())
for k in ('max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope'):
    out[f'{k}=null'] = run(f'{k}=null', variant(**{k: None}))
for k in ('calib_rj_ratio_max', 'sv_cf_threshold', 's_min_um'):
    out[f'{k}=NaN'] = run(f'{k}=NaN (토큰)', variant(**{k: 0.5}).replace(f'"{k}": 0.5', f'"{k}": NaN'))
    out[f'{k}=1e400'] = run(f'{k}=1e400 (→ inf)', variant(**{k: 0.5}).replace(f'"{k}": 0.5', f'"{k}": 1e400'))
    out[f'{k}=bigint'] = run(f'{k}=10**400 (정수)', variant(**{k: 0.5}).replace(f'"{k}": 0.5', f'"{k}": {BIG}'))
    out[f'{k}=-1'] = run(f'{k}=-1', variant(**{k: -1}))
    out[f'{k}="2"'] = run(f'{k}="2" (문자열)', variant(**{k: '2'}))
    out[f'{k}=true'] = run(f'{k}=true', variant(**{k: True}))
out['max_ladder_points=bigint'] = run('max_ladder_points=10**400', variant(max_ladder_points=0).replace('"max_ladder_points": 0', f'"max_ladder_points": {BIG}'))
out['max_ladder_points=12.0'] = run('max_ladder_points=12.0', variant(max_ladder_points=12.0))
out['sv_cf_threshold=0.99'] = run('sv_cf_threshold=0.99', variant(sv_cf_threshold=0.99))
out['calib_rj_ratio_max=1.0'] = run('calib_rj_ratio_max=1.0', variant(calib_rj_ratio_max=1.0))
out['dup_key'] = run('중복 칸 (sv_cf_threshold 두 번)', variant().replace('"sv_cf_scope"', '"sv_cf_threshold": 50.0, "sv_cf_scope"'))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_plan_gate.json'), 'w'), ensure_ascii=False, indent=1)
