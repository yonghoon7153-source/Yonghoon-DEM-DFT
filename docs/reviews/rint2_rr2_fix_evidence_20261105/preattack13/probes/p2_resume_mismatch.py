"""P2 탐침 — 정직한 RESUME_MISMATCH 시도 (재실행 사슬 · 실제 CLI · 가짜 러너 · 천장 σ 1e-12 다른 세계 = 시험 RS02 의 'bad' 꼴) 의 요약에 RR3-01 과 같은
두 칸 편집 (stop.code RESUME_MISMATCH → TIME_LIMIT · stop.run L02_ceiling → 다음 이름 L03_point) → 앞 런 = [L01 복사 · L02 재실행 (결정성 위반)] 가 둘 다
arms_read verified → 재실행 자격 · 원장 다음 --resume 허용?  그리고 그 시도를 원천으로 한 재실행이 L02 를 (원 시도 남은 payload 대조 없이) 복사하나."""
import json, copy, shutil
from pathlib import Path
from common import RR, T, setup_fixtures

def run():
    setup_fixtures()
    r = T.s_resume_left('PXRM', dict(T.PW, faults=[{'do': 'sigma_scale', 'f': 1.0 + 1e-12, 'match': {'rj': '0'}}]))
    b = r['b'] or {}
    s0 = b.get('sum') or {}
    folder = Path(b['out'])
    runs = s0.get('runs') or []
    out = {'attempt2_stop': s0.get('stop'), 'resume_block': s0.get('resume'),
           'runs': [[x.get('name'), x.get('rc'), x.get('group_cause'), x.get('copied_from'),
                     RR.arms_read_kind(x.get('arms_read'), x)[0]] for x in runs],
           'ledger_line2_real': {k: (RR.read_ledger if False else None) for k in ()}}
    real2 = T.led_result(r['d'], 2) or {}
    out['real_result_line_2'] = {k: real2.get(k) for k in ('status', 'cause', 'resume_ok')}
    # 두 칸 편집 (사본 폴더)
    s = copy.deepcopy(s0)
    s['stop']['code'] = 'TIME_LIMIT'
    s['stop']['run'] = 'L03_point'
    s['stop']['reason'] = None
    dst = Path(T.TD) / 'p2' / 'attempt_1'
    dst.parent.mkdir(parents=True)
    shutil.copytree(folder, dst, symlinks=True)
    (dst / 'ladder_summary.json').write_bytes(RR.canon_bytes(s))
    fl = RR.result_fields(dst, s)
    prob = RR.stop_record_problem(s, dst)
    out['edited'] = {'cause': fl['cause'], 'resume_ok': fl['resume_ok'], 'stop_record_problem': prob,
                     'run_traces_L03': RR.run_traces(dst, 'L03_point'), 'side': fl['side']}
    out['edited_ledger[resume_ok, order_stop, recount]'] = T.rr3_ledger(dst, s)
    # 이 사본을 원천으로 한 재실행이 L02 를 복사할까 (`_src_done`) — 원 시도 남은 payload 대조 없이
    rn = RR.ResumeRunner('unused.sh', dst, Path(T.TD) / 'p2' / 'attempt_3', {}, None, 0, {}, parent_env={}, src=dst, src_n=2)
    out['attempt3_src_done'] = {nm: rn._src_done(nm, od) for nm, od in (('L01_floor', 'L01_floor_arm1'), ('L02_ceiling', 'L02_ceiling_arm1'))}
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))

if __name__ == '__main__':
    run()
