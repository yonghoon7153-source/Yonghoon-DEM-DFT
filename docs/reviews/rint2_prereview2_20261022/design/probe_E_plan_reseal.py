"""Probe E — registration R §2-1b · §11 ④ ⑥ : the R-run plan sealed before S0 stage 2 (s_min · four pre-result numbers) vs the plan the
chain actually runs with.

Registered order: ④ S0 stage 2 needs the amendment commit whose `| 계획 해시 |` row = sha256(R plan A) → ⑥ numerical probe decides
maxiter · preconditioner (registration §11 ⑥ · §10-1 (2) P2_EXTRA="--step3-maxiter <탐침 뒤>") → those can only reach the runner through
the R plan's p2_extra (chain plan_env · parent P2_EXTRA is scrubbed) → plan B must be registered AFTER stage 2.
Question: does the chain (ladder stage) notice that plan B also changed s_min / SV threshold / point cap sealed by stage 2?
Uses the repository fake-runner harness (scripts/test_rint_r_chain.py).  Nothing in the repository is written.
Run:  python3 -I probe_E_plan_reseal.py <worktree>      (writes probe_E_plan_reseal.json)
"""
import json
import os
import shutil
import sys
import tempfile

WT = sys.argv[1]
sys.path.insert(0, os.path.join(WT, 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

TM.RR = RR
TM.TD = tempfile.mkdtemp(prefix='probeE_')
OUT = {}
try:
    TM.fixtures()
    A = dict(TM.FX['plan_obj'])
    pB, shaB, regB = TM.plan_set('planB', s_min_um=0.9, sv_cf_threshold=3.0, max_ladder_points=20, p2_extra='--step3-maxiter 90000')
    #  the fake runner's record templates are built (lazily, once) from FX['plan_obj'] → build them from plan B so the fake arms
    #  carry plan B's s_min (a fake-world consistency step, not a chain check)
    TM.FX['plan_obj'] = json.loads(open(pB, encoding='utf-8').read())
    TM.FX.pop('tpl', None)
    r = TM.ladder('E_planB_P0', TM.world('E_planB_P0'), law='P0', plan=pB, reg=regB)
    s = r['sum'] or {}
    OUT['plan_A_sealed_at_stage2 (fixture)'] = {k: A[k] for k in ('s_min_um', 'sv_cf_threshold', 'max_ladder_points', 'p2_extra')}
    OUT['plan_B_registered_later'] = {k: (s.get('plan') or {}).get('content', {}).get(k) for k in ('s_min_um', 'sv_cf_threshold', 'max_ladder_points', 'p2_extra')}
    OUT['ladder_with_plan_B'] = {'rc': r['rc'], 'status': s.get('status'), 'stop': (s.get('stop') or {}).get('code')}
    OUT['chain_cli_options'] = sorted(o for a in RR.main.__code__.co_consts if isinstance(a, str) and a.startswith('--') for o in [a])
    OUT['chain_reads_s0_stage2_report'] = any(k in open(os.path.join(WT, 'scripts', 'rint_r_chain.py'), encoding='utf-8').read()
                                              for k in ('s0_stage2', 'threshold_commit', "'r_plan'"))
finally:
    shutil.rmtree(TM.TD, ignore_errors=True)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_E_plan_reseal.json')
json.dump(OUT, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print(json.dumps(OUT, ensure_ascii=False, indent=1, default=str)[:2500])
