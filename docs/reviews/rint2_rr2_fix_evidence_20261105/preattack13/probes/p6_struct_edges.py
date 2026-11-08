"""P6 — 구조 칸 가장자리: 생산자가 쓰지 않는 꼴인데 verified 가 되는가 (파일 이름 가운데 글자 · arm_list 칸 없음 · REQ_KEYS 결손) · 정직 꼴 대조."""
import json, copy
from common import RR, T

def rec(arms_read, **kw):
    r = {'name': 'L01_floor', 'role': 'floor', 'kit': T.SBE_KIT, 'law': 'P0', 'c': '0', 'rj': 'inf', 'arms': 1, 'arm_list': None, 'variant': None,
         'sv_cf': False, 'outdir': 'L01_floor_arm1', 'rc': 0, 'seconds': 1.0, 'machine': 'kgy', 'group_cause': None, 'arms_read': arms_read}
    r.update(kw)
    return r

P = T.ct06_pub
cases = {
    'honest': rec([P(0)]),
    'file_newline_mid': rec([dict(P(0), file='p2_SBE_vgcf100_\n_a0.json')]),
    'file_nul_mid': rec([dict(P(0), file='p2_SBE_vgcf100_\x00_a0.json')]),
    'file_dotdot_mid': rec([dict(P(0), file='p2_SBE_vgcf100_..\\x_a0.json')]),
    'file_bare': rec([dict(P(0), file='p2_SBE_vgcf100_a0.json')]),
    'no_arm_list_key': {k: v for k, v in rec([P(0)]).items() if k != 'arm_list'},
    'no_law_role_rj': {k: v for k, v in rec([P(0)]).items() if k not in ('law', 'role', 'rj', 'c', 'variant', 'sv_cf', 'name')},
    'outdir_elsewhere': rec([P(0)], outdir='../../elsewhere'),
}
out = {}
for nm, r in cases.items():
    r = json.loads(RR.canon_bytes(r).decode('utf-8'))
    out[nm] = RR.arms_read_kind(r['arms_read'], r)[0]
    s = T.rr3_summ('TIME_LIMIT', 'L02_ceiling', [r])
    out[nm] = [out[nm], RR.prior_runs_problem(s, 'TIME_LIMIT', 'L02_ceiling', None) is None]
print(json.dumps(out, ensure_ascii=False, indent=1))
