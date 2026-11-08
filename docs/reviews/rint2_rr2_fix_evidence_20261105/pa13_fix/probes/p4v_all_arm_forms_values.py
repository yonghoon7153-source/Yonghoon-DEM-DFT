"""P4v (사전 공격 13 고침 확인 · 탐침 p4 의 값 판) — 모든 요청 꼴 (arms 1..8 · 팔 고르기 = 0..7 의 비지 않은 부분집합 중 접두 아님 · 킷 둘 = 510) 에 대해 생산자 성공 기록
(`arms_read_record` · 팔 = read_run 성공 값 꼴 (positive · protocol p3ca- · sid · cert_pass 넷 True · err_rel · 반복 수 · 수렴 계약) · 파일 = 러너 이름 꼴) → verified ·
판독 실패 꼴 (파일 신원) = file_ids · 탐침 p4 원판 (나머지 칸 전부 null) = 탐침 p1 pad_none 꼴 → 고친 뒤 bad (값 꼴) 가 옳다."""
import hashlib
import itertools
import json

from common import RR

HONEST = {'protocol_id': 'p3ca-0123456789abcdef', 'state': 'positive', 'cg_info': 0, 'cg_resid': 1e-12, 'imbalance': 1e-9,
          'cert_pass': [True, True, True, True], 'sid_fp': '0123456789abcdef0123456789abcdef', 'cg_iters': 10, 'resolve_iters': 2,
          'sv_cf_status': None, 'err_rel': 1e-6}


def arm(kit, i, values):
    a = {k: None for k in RR.ARM_PUBLIC}
    if values:
        a.update(HONEST)
    a.update(file=f'p2_{kit[4:]}_sph_fa_cj0_c0_a{i}.json', index=i, sha256=hashlib.sha256(f'{kit}{i}'.encode()).hexdigest(), sigma=1.0)
    return a


def run(values):
    res = {'n': 0, 'verified': 0, 'kinds': {}, 'fail_kind_bad': 0}
    for kit in ('kit_SBE_vgcf100', 'kit_DBE_sdcp1um_vgcf100'):
        subsets = [tuple(c) for r in range(1, 9) for c in itertools.combinations(range(8), r) if list(c) != list(range(len(c)))]
        for arms in list(range(1, 9)) + subsets:
            name, req, _ = RR.run_request('L', 1, kit, 'floor', 'P0', '0', 'inf', arms, False, None)
            rec = dict(req, outdir=name + RR.run_outdir_suffix(req['arms'], req['arm_list']), rc=0, seconds=1.0, arms_read=[], machine='kgy',
                       group_cause=None)
            arms_ = [arm(kit, i, values) for i in RR.arm_indices(req)]
            rec['arms_read'] = RR.arms_read_record(arms_)
            rec = json.loads(RR.canon_bytes(rec).decode('utf-8'))
            k, _why = RR.arms_read_kind(rec['arms_read'], rec)
            res['n'] += 1
            res['kinds'][k] = res['kinds'].get(k, 0) + 1
            ids = [{'file': a['file'], 'index': a['index'], 'sha256': a['sha256']} for a in arms_]
            if RR.arms_read_kind(ids, rec)[0] != 'file_ids':
                res['fail_kind_bad'] += 1
    res['verified'] = res['kinds'].get('verified', 0)
    return res


print(json.dumps({'p4_original_values_null': run(False), 'p4v_read_run_success_values': run(True)}, ensure_ascii=False, indent=1))
