"""P4 — 모든 요청 꼴 (arms 1..8 = range · 팔 고르기 = 0..7 의 비지 않은 부분집합 중 접두 아님) 에 대해 run_request (생산자 요청) → 생산자 성공 기록
(arms_read_record · 팔 = read_run 이 쓰는 칸 꼴 · 파일 = 러너 이름 꼴 p2_<줄기><SD><NG>_a<i>.json) → arms_read_kind = verified 인가 · 실패 꼴 = file_ids 인가."""
import hashlib, itertools, json
from common import RR

def fake_arm(kit, i, tag='_sph_fa_cj0_c0'):
    a = {k: None for k in RR.ARM_PUBLIC}
    a.update(file=f'p2_{kit[4:]}{tag}_a{i}.json', index=i, sha256=hashlib.sha256(f'{kit}{i}'.encode()).hexdigest(), sigma=1.0)
    return a

res = {'n': 0, 'verified': 0, 'bad': [], 'fail_kind_bad': []}
for kit in ('kit_SBE_vgcf100', 'kit_DBE_sdcp1um_vgcf100'):
    reqs = [n for n in range(1, 9)]
    subsets = [tuple(c) for r in range(1, 9) for c in itertools.combinations(range(8), r) if list(c) != list(range(len(c)))]
    for arms in reqs + subsets:
        try:
            name, req, _ = RR.run_request('L', 1, kit, 'floor', 'P0', '0', 'inf', arms, False, None)
        except RR.Stop as e:
            res['bad'].append(('run_request', arms, e.code)); continue
        rec = dict(req, outdir=name + RR.run_outdir_suffix(req['arms'], req['arm_list']), rc=0, seconds=1.0, arms_read=[], machine='kgy', group_cause=None)
        arms_ = [fake_arm(kit, i) for i in RR.arm_indices(req)]
        rec['arms_read'] = RR.arms_read_record(arms_)
        # JSON 왕복 (요약 = 정준 JSON)
        rec = json.loads(RR.canon_bytes(rec).decode('utf-8'))
        k, why = RR.arms_read_kind(rec['arms_read'], rec)
        res['n'] += 1
        if k == 'verified':
            res['verified'] += 1
        else:
            res['bad'].append((kit, arms, k, why))
        ids = [{'file': a['file'], 'index': a['index'], 'sha256': a['sha256']} for a in arms_]
        k2, _ = RR.arms_read_kind(ids, rec)
        if k2 != 'file_ids':
            res['fail_kind_bad'].append((kit, arms, k2))
print(json.dumps(res, ensure_ascii=False, indent=1)[:2000])
