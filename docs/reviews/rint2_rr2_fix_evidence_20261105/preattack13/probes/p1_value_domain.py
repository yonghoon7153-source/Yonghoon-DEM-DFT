"""P1 탐침 — 실제 생산자 (Runner._execute + 모의 run_in_group) 의 판독 실패 기록 (이름 맞는 팔 · 내용 {} → read_run ARM_UNREADABLE) 의 파일 신원 목록에
ARM_PUBLIC 나머지 11 칸을 '생산자가 결코 쓰지 않는 값' 으로 붙이고 + 요약 두 칸 (stop.code → TIME_LIMIT · stop.run → L02_ceiling) → 분류 · 재실행 자격 · 원장."""
import json, time, io, contextlib, copy
from pathlib import Path
from common import RR, T

PAY = b'{}\n'
GOODNAME = T.ct06_pub(0)['file']           # p2_SBE_vgcf100_sph_fa_cj0_c0_a0.json (킷 앞자리 · _a0 맞음)

def producer(tag):
    folder = Path(T.TD) / 'p1' / tag / 'attempt_1'
    folder.mkdir(parents=True)
    outdir = folder / 'L01_floor_arm1'
    _nm, req, _key = RR.run_request('L', 1, T.SBE_KIT, 'floor', 'P0', None, 0.0, 1, False, None)
    rn = RR.Runner('unused.sh', folder, folder, {}, None, time.time() + 60, {}, parent_env={})
    code = None
    with T.rc_patch(run_in_group=T.rr3_mock_group(outdir, {GOODNAME: PAY})), contextlib.redirect_stdout(io.StringIO()):
        try:
            rn._execute('L01_floor', req, outdir, {})
        except RR.Stop as e:
            code = e.code
    return folder, req, rn.records, code

def run():
    out = {}
    folder, req, recs, code = producer('base')
    last = recs[-1]
    out['producer'] = {'stop': code, 'rc': last.get('rc'), 'group_cause': last.get('group_cause'),
                       'arms_read': last.get('arms_read'), 'kind': RR.arms_read_kind(last.get('arms_read'), last)}
    variants = {
        'as_is': None,
        'pad_none': {k: None for k in RR.ARM_PUBLIC if k not in ('file', 'index', 'sha256')},
        'pad_impossible': {'protocol_id': 'unknown:x', 'state': 'short', 'cg_info': 'x', 'cg_resid': -1, 'imbalance': [],
                           'cert_pass': False, 'sid_fp': '', 'cg_iters': True, 'resolve_iters': 'y', 'sv_cf_status': {'a': 1},
                           'err_rel': -5.0},
        'pad_legacy_state': {'protocol_id': 'p3ca-x', 'state': 'legacy', 'cg_info': 0, 'cg_resid': 0.0, 'imbalance': 0.0,
                             'cert_pass': [True] * 4, 'sid_fp': 'f' * 16, 'cg_iters': 1, 'resolve_iters': 0, 'sv_cf_status': None,
                             'err_rel': 0.0},
    }
    for nm, pad in variants.items():
        rr = copy.deepcopy(recs)
        if pad is not None:
            rr[-1]['arms_read'] = [dict(a, **pad) for a in rr[-1]['arms_read']]
        s = T.rr3_summ('TIME_LIMIT', 'L02_ceiling', rr)
        kind = RR.arms_read_kind(rr[-1]['arms_read'], rr[-1])
        fl = RR.result_fields(folder, s)
        prob = RR.stop_record_problem(s, folder)
        # 원장: 결과 줄 → 다음 --resume 1 항목 차례
        f2 = Path(T.TD) / 'p1' / f'L_{nm}' / 'attempt_1'
        import shutil
        shutil.copytree(folder, f2, symlinks=True)
        led = T.rr3_ledger(f2, s)
        out[nm] = {'kind': kind, 'cause': fl['cause'], 'resume_ok': fl['resume_ok'],
                   'stop_record_problem': None if prob is None else prob[:120], 'ledger[resume_ok, order_stop, recount]': led}
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))

if __name__ == '__main__':
    run()
