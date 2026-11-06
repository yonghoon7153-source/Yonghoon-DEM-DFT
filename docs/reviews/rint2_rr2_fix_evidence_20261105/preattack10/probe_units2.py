#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 10 회차 (독립) 단위 탐침 2 — ① FIFO 그룹 기록 · attempt.json 이 orphan_cause · attempt_groups_problem · read_attempt 를 막는가
(포크한 자식 · 시간 상한 6 s) ② 요약 있는 길 GROUP_UNCONFIRMED · 그 런 기록 없음 + Traceback 로그 → 재실행 자격 ③ 요약 있는 길 GROUP_UNCONFIRMED · 런 기록
group_cause 칸 없음 (옛 판 꼴) · rc null ④ result_fields 가 꼴 틀린 요약 칸 (stop = 목록 · runs = 글) 에서 내는 예외 이름.

쓰는 법: python3 -I probe_units2.py <rint_r_chain.py 폴더> <scripts 폴더> <출력 json>
"""
import hashlib
import json
import os
import select
import signal
import sys
import tempfile
import time
from pathlib import Path

MOD_DIR, SCRIPTS_DIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, MOD_DIR)
import rint_r_chain as RR  # noqa: E402

TD = Path(tempfile.mkdtemp(prefix='pa10_u2_'))
MARK = 'L01_floor_arm1/.unchecked/p2_SBE_vgcf100_a0.json.first_result.json'
TB = "[p2] run\nTraceback (most recent call last):\nKeyError: 'sigma'\n"
R = {}


def child(fn, timeout=6.0):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        try:
            os.close(r)
            out = fn()
        except BaseException as e:  # noqa: BLE001
            out = {'error': f'{type(e).__name__}: {e}'[:200]}
        buf = json.dumps(out, default=repr).encode('utf-8')
        while buf:
            buf = buf[os.write(w, buf):]
        os._exit(0)
    os.close(w)
    chunks, done, t_end = [], False, time.time() + timeout
    while time.time() < t_end:
        rl, _w, _x = select.select([r], [], [], 0.2)
        if rl:
            x = os.read(r, 65536)
            if not x:
                done = True
                break
            chunks.append(x)
    os.close(r)
    if not done:
        os.kill(pid, signal.SIGKILL)
    os.waitpid(pid, 0)
    return json.loads(b''.join(chunks).decode('utf-8') or '{}') if done else {'blocked_timeout_s': timeout}


def folder(tag):
    f = TD / tag / 'attempt_1'
    (f / MARK).parent.mkdir(parents=True)
    (f / MARK).write_text('{}\n', encoding='utf-8')
    return f


def group(f, name, end, log=TB, fifo=None):
    (f / 'groups').mkdir(parents=True, exist_ok=True)
    tok = hashlib.sha256(f'{f}|{name}'.encode()).hexdigest()[:32]
    L = {'schema': 'rint-r-group-v1', 'name': name, 'token': tok, 'pid': 4194305, 'pgid': 4194305, 'argv': ['bash'], 'host': RR.host_ident(),
         'started_utc': '2026-11-06T00:00:00Z', 'by': 'chain', 'chain_pid': 4194305}
    E = dict({'schema': 'rint-r-group-v1', 'name': name, 'token': tok, 'rc': None, 'cause': None, 'signal': None, 'confirmed': True, 'left': [],
              'left_after_exit': None, 'killed': 0, 'by': 'chain', 'ended_utc': '2026-11-06T00:00:00Z'}, **end)
    for nm, obj in (('launch', L), ('end', E)):
        p = f / 'groups' / f'{name}.{nm}.json'
        if fifo == nm:
            os.mkfifo(str(p))
        else:
            p.write_text(json.dumps(obj), encoding='utf-8')
    if log is not None:
        (f / 'logs').mkdir(parents=True, exist_ok=True)
        (f / 'logs' / f'{name}.log').write_text(log, encoding='utf-8')


# ① FIFO
f1 = folder('F_end')
group(f1, 'L01_floor', {'rc': 0}, fifo='end')
R['F1_orphan_cause_fifo_end'] = child(lambda: list(RR.orphan_cause(f1)))
R['F2_attempt_groups_problem_fifo_end'] = child(lambda: [RR.attempt_groups_problem(f1)])
f3 = folder('F_launch')
group(f3, 'L01_floor', {'rc': 0}, fifo='launch')
R['F3_orphan_cause_fifo_launch'] = child(lambda: list(RR.orphan_cause(f3)))
f4 = TD / 'F_att' / 'attempt_1'
f4.mkdir(parents=True)
os.mkfifo(str(f4 / 'attempt.json'))
R['F4_read_attempt_fifo'] = child(lambda: [RR.read_attempt(f4)])
f5 = folder('F_summary')
os.mkfifo(str(f5 / 'ladder_summary.json'))
R['F5_stage_summary_read_fifo'] = child(lambda: list(RR.stage_summary_read(f5)) if hasattr(RR, 'stage_summary_read') else
                                       [RR.read_summary(f5, 'ladder_summary.json')])


# ② · ③ 요약 있는 길 GROUP_UNCONFIRMED
def gu(tag, rec, log=TB):
    f = folder(tag)
    group(f, 'L01_floor', {'rc': 1, 'confirmed': True}, log)
    s = {'status': 'STOPPED', 'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L01_floor', 'reason': None},
         'runs': [] if rec is None else [dict({'name': 'L01_floor', 'outdir': 'L01_floor_arm1'}, **rec)]}
    rf = RR.result_fields(f, s)
    return {'cause': rf['cause'], 'resume_ok': rf['resume_ok']}


R['G5_gu_no_run_record_traceback'] = gu('G5', None)
R['G6_gu_rec_no_group_cause_key_rcnull'] = gu('G6', {'rc': None})
R['G7_gu_rec_rc1_ctl'] = gu('G7', {'rc': 1, 'group_cause': None})


# ④ 꼴 틀린 요약 칸
def shape(tag, s):
    f = folder(tag)
    group(f, 'L01_floor', {'rc': 1}, TB)
    try:
        rf = RR.result_fields(f, s)
        return {'cause': rf['cause'], 'resume_ok': rf['resume_ok']}
    except Exception as e:  # noqa: BLE001
        return {'exc': type(e).__name__}


R['S1_stop_list'] = shape('S1', {'status': 'STOPPED', 'stop': ['TIME_LIMIT'], 'runs': []})
R['S2_runs_str'] = shape('S2', {'status': 'STOPPED', 'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L01_floor'}, 'runs': 'x'})
R['S3_runs_list_of_str'] = shape('S3', {'status': 'STOPPED', 'stop': {'code': 'GROUP_UNCONFIRMED', 'run': 'L01_floor'}, 'runs': ['x']})

out = {'module_sha256': hashlib.sha256(Path(RR.__file__).read_bytes()).hexdigest(), 'td': str(TD), 'rows': R}
Path(OUT).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
for k, v in R.items():
    print(k.ljust(40), json.dumps(v, ensure_ascii=False)[:160])
