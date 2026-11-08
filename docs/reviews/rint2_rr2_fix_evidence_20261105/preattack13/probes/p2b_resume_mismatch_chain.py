"""P2b — RESUME_MISMATCH 두 칸 편집을 재실행 사슬 원장 (시도 1 = 원 시도 · 시도 2 = 재실행 · 그 결과 줄 = 편집 요약에서 recover 로 셈) 에 넣고 다음
`--add --resume 1` 차례 (attempt_order_problem) · 결과 줄 다시 셈 (result_line_problem) 을 본다 — 원천 = 사슬 끝 시도 2 (L01 · L02 복사)."""
import json, copy, shutil
from pathlib import Path
from common import RR, T, setup_fixtures

def main():
    setup_fixtures()
    r = T.s_resume_left('PXRM2', dict(T.PW, faults=[{'do': 'sigma_scale', 'f': 1.0 + 1e-12, 'match': {'rj': '0'}}]))
    a, b = r['a'], r['b']
    base = Path(T.TD) / 'p2b' / 'base'
    f1, f2 = base / 'attempt_1', base / 'attempt_2'
    shutil.copytree(a['out'], f1, symlinks=True)
    shutil.copytree(b['out'], f2, symlinks=True)
    s1 = json.loads((f1 / 'ladder_summary.json').read_text(encoding='utf-8')) if (f1 / 'ladder_summary.json').exists() else None
    s2 = json.loads((f2 / 'ladder_summary.json').read_text(encoding='utf-8'))
    s2e = copy.deepcopy(s2)
    s2e['stop'].update(code='TIME_LIMIT', run='L03_point', reason=None)
    (f2 / 'ladder_summary.json').write_bytes(RR.canon_bytes(s2e))
    head = {'kind': 'header', 'schema': RR.LEDGER_SCHEMA, 'plan_sha256': 'b' * 64, 'utc': 'synthetic'}
    ent1 = {'kind': 'entry', 'n': 1, 'target': 'ladder:P0', 'machine': 'synthetic', 'resume_of': None, 'plan_sha256': 'b' * 64,
            'code_key_sha256': 'c' * 64, 'env': {}, 'bed': {}, 'utc': 'synthetic'}
    ent2 = dict(ent1, n=2, resume_of=1)
    def start(n, f):
        return {'kind': 'start', 'n': n, 'base': str(base.resolve()), 'folder': f.name, 'host': {'machine_id': None, 'boot_id': None, 'pidns': None},
                'utc': 'synthetic', 'chain_pid': 1, 'chain_start': None}
    res1 = RR.attempt_result_line(1, f1, s1, 'recover')
    res2_real = RR.attempt_result_line(2, f2, s2, 'chain') if False else None
    res2 = RR.attempt_result_line(2, f2, s2e, 'recover')
    st = RR.ledger_parse(''.join(RR.ledger_line(x) for x in (head, ent1, start(1, f1), res1, ent2, start(2, f2), res2)).encode('utf-8'))
    order = RR.attempt_order_problem(st, dict(ent1, n=3, resume_of=1), {'exec_policy': {'max_attempts': 3}})
    out = {'res1': {k: res1.get(k) for k in ('status', 'cause', 'resume_ok')},
           'res2_from_edited': {k: res2.get(k) for k in ('status', 'cause', 'resume_ok')},
           'adoption': RR.adoption(st, 'ladder:P0', upto=3),
           'next_resume_1_order_problem': order,
           'recount_2': RR.result_line_problem(2, f2, res2),
           'stop_record_problem_edited': RR.stop_record_problem(s2e, f2)}
    # 실제 재실행 원천 = 사슬 끝 (시도 2) — 복사 대상
    rn = RR.ResumeRunner('unused.sh', f2, base / 'attempt_3', {}, None, 0, {}, parent_env={}, src=f2, src_n=2)
    out['src_done_attempt2'] = {nm: rn._src_done(nm, od) for nm, od in (('L01_floor', 'L01_floor_arm1'), ('L02_ceiling', 'L02_ceiling_arm1'))}
    # 복사될 L02 payload 는 시도 1 의 남은 payload 와 다르다 (결정성 위반의 그 바이트)
    left = dict(RR.resume_leftovers(f1 / 'L02_ceiling_arm1'))
    now = {p.name: p.read_bytes() for p in (f2 / 'L02_ceiling_arm1').glob('p2_*.json')}
    out['L02_payload_same_as_attempt1_leftover'] = {nm: (now.get(nm) == raw) for nm, raw in left.items()}
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))

if __name__ == '__main__':
    main()
