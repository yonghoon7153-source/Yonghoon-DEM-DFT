"""고친 판 (11-06) 에서 본 같은 부류 꼴 — 관찰만 (고치지 않음 · 판정 아님).  python3 -I probe_new.py <scripts 폴더> <출력 json>"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import rint_r_chain as RR  # noqa: E402

TD = Path(tempfile.mkdtemp(prefix='pa10fix_new_'))
MARK = 'L00_prev_arm1/.unchecked/p2_SBE_vgcf100_a0.json.first_result.json'
TB = "[p2] run\nTraceback (most recent call last):\nKeyError: 'sigma'\n"
out = {'module_sha256': hashlib.sha256(Path(RR.__file__).read_bytes()).hexdigest(), 'rows': {}}


def folder(tag):
    f = TD / tag / 'attempt_1'
    (f / MARK).parent.mkdir(parents=True)
    (f / MARK).write_text('{}\n', encoding='utf-8')
    (f / 'logs').mkdir()
    (f / 'logs' / 'L01_floor.log').write_text(TB, encoding='utf-8')
    return f


def summ_row(tag, code, rec):
    f = folder(tag)
    s = {'status': 'STOPPED', 'stop': {'code': code, 'run': 'L01_floor', 'reason': None},
         'runs': [dict({'name': 'L01_floor', 'outdir': 'L01_floor_arm1'}, **rec)]}
    fl = RR.result_fields(f, s)
    return [fl['cause'], fl['resume_ok']]


R = out['rows']
# 정직한 꼴 (러너가 rc 1 · Traceback 으로 스스로 끝남 = RUNNER_RC · 런 기록 group_cause None · rc 1)
R['honest_RUNNER_RC_rc1'] = summ_row('h', 'RUNNER_RC', {'rc': 1, 'group_cause': None})
# N1 — 멈춤 코드 한 칸만 TIME_LIMIT 로 (런 기록 그대로 · 생산자 꼴 아님: TIME_LIMIT 의 그 런 기록 = group_cause timeout · rc null)
R['N1_code_TIME_LIMIT_rec_gc_none_rc1'] = summ_row('n1', 'TIME_LIMIT', {'rc': 1, 'group_cause': None})
# N2 — 런 기록 group_cause 한 칸만 timeout · signal (rc 1 그대로 · 생산자 꼴 아님: group_cause 가 None 아니면 rc null · RUNNER_RC + timeout 없음)
R['N2_RUNNER_RC_gc_timeout_rc1'] = summ_row('n2a', 'RUNNER_RC', {'rc': 1, 'group_cause': 'timeout'})
R['N2_RUNNER_RC_gc_signal_rc1'] = summ_row('n2b', 'RUNNER_RC', {'rc': 1, 'group_cause': 'signal'})
# 대조 — 생산자 꼴 (TIME_LIMIT + group_cause timeout + rc null) = 시간 초과 · 자격 (설계)
R['ctl_TIME_LIMIT_gc_timeout_rcnull'] = summ_row('c1', 'TIME_LIMIT', {'rc': None, 'group_cause': 'timeout'})


# N4 — recover --ledger 의 거부 기록이 객체 아닌 JSON (recover_ledger 는 isinstance 검사 없이 rec.get · result_recount 는 Stop)
def n4():
    f = TD / 'n4' / 'attempt_1'
    f.mkdir(parents=True)
    (f / RR.REJECTED_FILE).write_text('[1]\n', encoding='utf-8')
    try:
        RR.result_recount(f)
        r1 = 'NO_STOP'
    except RR.Stop as e:
        r1 = f'Stop {e.code}'
    src = Path(RR.__file__).read_text(encoding='utf-8')
    i = src.index('            rj = f / REJECTED_FILE')
    seg = src[i:i + 900]
    return {'result_recount': r1, 'recover_ledger_isinstance_check': 'isinstance(rec, dict)' in seg}


R['N4_rejected_list'] = n4()
Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=1))
