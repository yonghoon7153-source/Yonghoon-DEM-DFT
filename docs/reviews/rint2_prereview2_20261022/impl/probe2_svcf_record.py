# -*- coding: utf-8 -*-
"""탐침 2-B (B 결합 옆 자리) — SV 반사실 기록 검증기 (`ca_ext_svcf.sv_cf_problem`) 가 기록 안 수의 일관성을 다시 보나.
정상 기록 (producer 꼴) 에서 칸 하나씩 바꾼 사본: 비 ≠ G_full/G_cut · 증서 ok False 인데 computed · G_full ≠ 주 해 · n_unsplit > 0.
기대 (규율 '플래그를 믿지 않는다') = 문제 문자열.  실제 = None 이면 받음."""
import copy
import json
import os
import sys
REPO = os.environ.get('PRE_REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d')
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import ca_ext_svcf as SV     # noqa: E402

raw = {'kind': 'counterfactual_cut_sv_bridges_keep_self_v1', 'rule': 'x', 'requested': True, 'threshold': None,
       'n_sv_faces_cut': 3, 'n_sdcp_components_touching': 1, 'n_bridging_components': 1, 'n_sv_faces_kept_self': 0,
       'n_unsplit_bridging_components': 0, 'G_full_code': 10.0, 'G_cut_code': 5.0, 'sv_counterfactual_ratio': 2.0,
       'flag': None, 'cg_info': 0, 'resid': 1e-14, 'status': 'computed',
       'conv_cert': {'version': 'conv-cert-v2', 'status': 'POSITIVE_SOLVED', 'ok': True, 'pass_a': True, 'pass_b': True,
                     'pass_c': True, 'pass_d': True}, 'backend_last_solve': None}


def ev_of(rec):
    return {'sv_counterfactual_request': {'threshold': None}, 'solve': {'sv_counterfactual': SV.sv_cf_record(rec)}}


out = {}
cases = {
    'normal': {},
    'ratio_not_Gfull_over_Gcut (2.0 → 1.0)': {'sv_counterfactual_ratio': 1.0},
    'computed_but_cf_cert_not_ok': {'conv_cert': dict(raw['conv_cert'], ok=False, pass_d=False)},
    'computed_but_G_cut_None': {'G_cut_code': None},
    'computed_with_unsplit_bridges=1': {'n_unsplit_bridging_components': 1},
    'computed_ratio_below_1 (0.5)': {'sv_counterfactual_ratio': 0.5},
}
for tag, ch in cases.items():
    rec = copy.deepcopy(raw)
    rec.update(ch)
    why = SV.sv_cf_problem(ev_of(rec), True)
    view = SV.chain_view(SV.sv_cf_record(rec))
    out[tag] = {'problem': why, 'chain_view': view}
    print(f'{tag:44s} problem={why!r} chain={view}')
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_svcf_record.json'), 'w'), ensure_ascii=False, indent=1)
