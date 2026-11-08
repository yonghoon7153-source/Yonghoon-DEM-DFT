"""P2c (사전 공격 13 고침 확인 · 새 탐침) — 정직 RESUME_MISMATCH 재실행 요약 (시도 2) 편집 칸 수별 (두 칸 · same → true 세 칸 · compared [] + assumed · + null ·
from = 자기 · rerun null · resume null) → 원인 · 재실행 자격 · stop_record_problem 사유 · 정직 대조 (천장 대조 같음 뒤 L03 메모리 부족 = 자격 True · 원천이 다른 곳 =
그대로) · 선언된 한정 (원천 시도 폴더가 같은 바탕에 없으면 바이트 다시 대조 안 함 → same → true 세 칸 편집 + 원천 치움 = recover 결과 줄 자격 True · 그러나 실제
재실행 풀기 전 대조 (같은 바탕 · 원천 있음) 의 결과 줄 다시 셈 = 대조 실패)."""
import copy
import json
import shutil
from pathlib import Path

from common import RR, T, setup_fixtures

MM = dict(T.PW, faults=[{'do': 'sigma_scale', 'f': 1.0 + 1e-12, 'match': {'rj': '0'}}])
L3 = dict(T.PW, faults=[{'do': 'oom_after_mark', 'match': {'rj': '10000.0'}}])


def base_copy(res, tag, drop=False):
    dst = Path(T.TD) / 'p2c' / tag
    shutil.copytree(Path(res['b']['out']).parent, dst, symlinks=True)
    if drop:
        shutil.rmtree(dst / 'attempt_1')
    return dst / 'attempt_2'


def ed(s0, stop=None, rs=None, same=None, runs=None, resume='keep'):
    s = copy.deepcopy(s0)
    if stop:
        s['stop'].update(stop, reason=None)
    if resume != 'keep':
        s['resume'] = resume
    if rs:
        s['resume'].update(rs)
    if same is not None:
        s['resume']['compared'] = [dict(x, same=same) for x in s['resume']['compared']]
    for nm, kw in (runs or {}).items():
        [r for r in s['runs'] if r.get('name') == nm][0].update(kw)
    return s


def row(f, s):
    fl = RR.result_fields(f, s)
    prob = RR.stop_record_problem(s, f)
    return {'cause': fl['cause'], 'resume_ok': fl['resume_ok'], 'reason': None if prob is None else prob[:140]}


def main():
    setup_fixtures()
    mm = T.s_resume_left('P2C_mm', MM)
    l3 = T.s_resume_left('P2C_l3', L3)
    smm, sl3 = mm['b']['sum'], l3['b']['sum']
    TL = {'code': 'TIME_LIMIT', 'run': 'L03_point'}
    out = {'scen': {'mm_stop': T.stop_code(mm['b']), 'l3_stop': T.stop_code(l3['b']), 'mm_resume': smm.get('resume'), 'l3_resume': sl3.get('resume')}}
    cases = {
        'honest_mismatch': (mm, smm, False),
        'e2_two_fields': (mm, ed(smm, stop=TL), False),
        'e3_same_true': (mm, ed(smm, stop=TL, same=True), False),
        'e4_compared_empty_assumed': (mm, ed(smm, stop=TL, rs={'compared': [], 'determinism': 'assumed'}), False),
        'e4_compared_empty_null': (mm, ed(smm, stop=TL, rs={'compared': [], 'determinism': None}), False),
        'e4_from_self': (mm, ed(smm, stop=TL, same=True, rs={'from': 2}, runs={'L01_floor': {'copied_from': 2}}), False),
        'e5_rerun_null': (mm, ed(smm, stop=TL, rs={'rerun': None, 'compared': [], 'determinism': None}), False),
        'e3_resume_null': (mm, ed(smm, stop=TL, resume=None), False),
        'honest_same_then_oom': (l3, sl3, False),
        'honest_same_then_oom_src_elsewhere': (l3, sl3, True),
        'LIMIT_e3_same_true_src_elsewhere': (mm, ed(smm, stop=TL, same=True), True),
    }
    for nm, (res, s, drop) in cases.items():
        out[nm] = row(base_copy(res, nm, drop=drop), s)
    #  선언된 한정의 실제 재실행 길 — 원천을 치운 채 recover 결과 줄 (자격 True) → 같은 바탕 (원천 있음) 에서 결과 줄 다시 셈 (resume_chain_problem 의 대조)
    s3 = ed(smm, stop=TL, same=True)
    f_nosrc = base_copy(mm, 'limit_nosrc', drop=True)
    (f_nosrc / 'ladder_summary.json').write_bytes(RR.canon_bytes(s3))
    res2 = RR.attempt_result_line(2, f_nosrc, s3, 'recover')
    f_src = base_copy(mm, 'limit_src')
    (f_src / 'ladder_summary.json').write_bytes(RR.canon_bytes(s3))
    out['LIMIT_resume_chain_recount'] = {'result_line_resume_ok_src_elsewhere': res2['resume_ok'],
                                         'recount_same_base_with_src': (RR.result_line_problem(2, f_src, res2) or '')[:200] or None}
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == '__main__':
    main()
