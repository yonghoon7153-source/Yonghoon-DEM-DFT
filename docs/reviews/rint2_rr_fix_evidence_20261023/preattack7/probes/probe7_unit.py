#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 7 회차 (11-02 · 대상 0658c0ac6) — 단위 탐침 (가짜 /proc · 합성 시도 폴더 · 실제 사슬 함수).  사슬 · 시험 파일은 고치지 않는다.

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/probe7_unit.py <임시 폴더 바탕> [U1,U2,U3,U4,U5,U6,U7]

U1  (PC6-01 _run_kin 계보 끝의 가지) — 러너 세션 · 그룹 밖 · environ 못 읽는 프로세스: ⓐ 부모 칸 (stat 4 째) 못 읽음 (stat 줄 짧음) ⓑ 부모 pid 가
    /proc 에 없음 (hidepid=2 꼴 · 사라짐) ⓒ 부모 = pid 0 (이름공간 밖 부모 · docker exec 꼴) ⓓ 부모 stat = 폴더 (EACCES 대신 IsADirectoryError ·
    주 루프가 부모 자신을 확인 불가로 셈) → group_members 결과
U2  (PC6-13 chain_end 의 원인 칸) — recover 끝 기록 chain_end 원인 exception (사슬이 기다리는 동안 예외 · SIGINT) · rc −9 → orphan_cause / 결과 줄 ·
    같은 끝 기록이 by chain 으로 남아 있을 때 (recover 전 · 그룹 확인) 와 비교
U3  runner_rc_failed 값 표 (0 · None · 1 · −9 · 137 · True · False · 0.0 · "0" · 2**64)
U4  (PC6-09 창) 시도 폴더를 만든 뒤 attempt.json 을 쓰기 전에 사슬 사망 (빈 attempt_1) → 같은 --attempt 다시 · 그 뒤 같은 대상 새 시도 · 판정
U5  (PC6-13 · PC6-02 차례) 그룹 미확인 + 러너 rc 1 + 로그 = 앞서 받아 넘긴 메모리 부족 줄 (GPU → CPU 폴백 문구) + 뒤 파이썬 KeyError traceback → 원인
U6  (PC6-13 recover) 끝 기록의 표지 (token) ≠ 시작 기록 표지 (다른 런의 끝 기록) → chain_end 를 그대로 옮기나
U7  (PC6-12) 찾은 시도 폴더의 attempt.json = 심볼릭 링크 · 폴더 = 심볼릭 링크 → found_attempts_problem
값 · σ 를 찍지 않는다.
"""
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

WT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.gettempdir()).resolve()
BASE.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U7'}


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def setup():
    TM.RR = RR
    TM.TD = tempfile.mkdtemp(prefix='pa7_unit_', dir=str(BASE))
    TM.fixtures()


def fake(root, pid, ppid=1, pgrp=None, sid=None, start=10 ** 9, environ=b'', stat_raw=None, stat_dir=False):
    """가짜 /proc 항목 — TM.pd_fake_proc 꼴 + stat 줄 그대로 (stat_raw) · stat = 폴더 (stat_dir)."""
    p = Path(root) / str(pid)
    p.mkdir(parents=True)
    if stat_dir:
        (p / 'stat').mkdir()
    elif stat_raw is not None:
        (p / 'stat').write_text(stat_raw, encoding='ascii')
    else:
        rest = ['S', str(ppid), str(pid if pgrp is None else pgrp), str(pid if sid is None else sid), '0', '-1'] + ['0'] * 13 + [str(start)] + ['0'] * 20
        (p / 'stat').write_text(f'{pid} (fake) ' + ' '.join(rest) + '\n', encoding='ascii')
    u = os.getuid()
    (p / 'status').write_text(f'Name:\tfake\nUid:\t{u}\t{u}\t{u}\t{u}\n', encoding='ascii')
    if environ is None:
        (p / 'environ').mkdir()
    else:
        (p / 'environ').write_bytes(environ)


def u1():
    tok = 'd' * 32
    S, SST = 911000, 5000
    run = {'pid': S, 'start': SST}
    fp = Path(TM.TD) / 'u1'
    old = RR.PROC_DIR
    got = {}

    def table(name, rows):
        (fp / name).mkdir(parents=True)
        for kw in rows:
            fake(fp / name, **kw)
        RR.PROC_DIR = str(fp / name)
        try:
            return RR.group_members(tok, run=run), RR.GROUP_SCAN.get(tok)
        finally:
            RR.GROUP_SCAN.pop(tok, None)
    try:
        #  ⓐ 부모 칸 못 읽음 — stat 줄이 상태 칸에서 끝남 (실제 /proc 에선 안 나오는 꼴 · 합성)
        got['a_ppid_unreadable'] = table('a', [dict(pid=911101, environ=None, stat_raw='911101 (fake) S\n')])
        #  ⓑ 부모 pid 가 /proc 에 없음 (hidepid=2 의 숨은 조상 · 그 사이 사라짐 꼴)
        got['b_parent_absent'] = table('b', [dict(pid=911201, ppid=911200, environ=None)])
        #  ⓒ 부모 = 0 (이름공간 밖에서 들어온 프로세스 · nsenter · docker exec 꼴)
        got['c_parent_zero'] = table('c', [dict(pid=911301, ppid=0, environ=None)])
        #  ⓓ 부모 stat = 폴더 (읽기 오류 · 주 루프가 부모 자신도 본다)
        got['d_parent_stat_err'] = table('d', [dict(pid=911400, stat_dir=True, environ=b'A=1\0'), dict(pid=911401, ppid=911400, environ=None)])
        #  ⓔ 대조 — 부모가 러너 세션 안 (확인 불가 기대)
        got['e_parent_in_session'] = table('e', [dict(pid=911500, sid=S, environ=b'A=1\0'), dict(pid=911501, ppid=911500, environ=None)])
    finally:
        RR.PROC_DIR = old
    out('U1', rows=got, note='반환 (group_members, GROUP_SCAN) · None = 확인 불가 · [] = 표지 프로세스 없음 (확인)')


def u2():
    rows = {}
    log = '[p2] run\n'
    mark = {TM.PC_MARK: '{}\n'}
    rec_ce = {'by': 'recover', 'cause': 'parent_dead', 'rc': None, 'confirmed': True,
              'chain_end': {'rc': -9, 'cause': 'exception', 'confirmed': False, 'ended_utc': '2026-11-02T00:00:00Z'}}
    by_chain = {'by': 'chain', 'cause': 'exception', 'rc': -9, 'confirmed': True}
    by_chain_unconf = {'by': 'chain', 'cause': 'exception', 'rc': -9, 'confirmed': False}
    for nm, end in (('recover_chain_end_exception', rec_ce), ('by_chain_exception_confirmed', by_chain),
                    ('by_chain_exception_unconfirmed', by_chain_unconf)):
        f = TM.pc_folder(f'U2_{nm}', mark)
        TM.pc_group(f, 'L01_floor', end, log)
        r = RR.attempt_result_line(1, f, None, 'recover')
        rows[nm] = {'status': r['status'], 'side': r['side'], 'cause': r['cause'], 'resume_ok': r['resume_ok'],
                    'groups_problem': RR.attempt_groups_problem(f)}
    #  recover_group 이 by chain (원인 exception · 미확인) 끝 기록을 갈아 쓰는 꼴 (그룹 = 가짜 /proc 비어 있음 → 확인)
    out_dir, _tok = TM.gr_fake_launch('U2_recover')
    lp = out_dir / 'groups' / 'L01_floor.launch.json'
    lp.with_name('L01_floor.end.json').write_text(json.dumps(dict(by_chain_unconf, schema='rint-r-group-v1', name='L01_floor',
                                                                    ended_utc='2026-11-02T00:00:01Z')), encoding='utf-8')
    end, held = RR.recover_group(lp, RR.host_ident())
    rows['recover_group_rewrite'] = {'held': held, 'by': (end or {}).get('by'), 'cause': (end or {}).get('cause'),
                                     'confirmed': (end or {}).get('confirmed'), 'chain_end': (end or {}).get('chain_end'),
                                     'chain_end_failed': RR.chain_end_failed(end or {})}
    out('U2', rows=rows)


def u3():
    vals = [0, None, 1, -9, 137, True, False, 0.0, '0', 2 ** 64]
    out('U3', table={repr(v): RR.runner_rc_failed(v) for v in vals})


def u4():
    d, _rc, _so = TM.led_new('U4')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    base = Path(TM.TD) / 'runs' / 'U4'
    (base / f'attempt_{n1}').mkdir(parents=True)            # 사슬이 폴더를 만든 직후 · attempt.json 전에 죽은 꼴
    raw0 = TM.led_raw(d)
    again = TM.lad_att('U4', TM.world('U4_again'), d, n1, base=base)
    r1 = TM.led_result(d, n1)
    side = (base / f'attempt_{n1}{RR.REJECTED_SIDE}').exists()
    add2 = TM.led_add(d, 'ladder:P0')
    b = TM.lad_att('U4_b', TM.world('U4_b'), d, add2[1], base=base) if add2[1] else None
    v = TM.ver_led('U4_v', [b['out']], d) if b else None
    out('U4', rerun_rc=again['rc'], rerun_tail=(again['so'].strip().splitlines() or [''])[-1][:200], ledger_changed=TM.led_raw(d) != raw0,
        result1={k: (r1 or {}).get(k) for k in ('status', 'side', 'cause', 'folder', 'by')}, side_file=side,
        add2_rc=add2[0], b_status=((b or {}).get('sum') or {}).get('status'), verdict_stop=TM.stop_code(v) if v else None,
        verdict_why=str((((v or {}).get('v') or {}).get('stop') or {}).get('cause'))[:220])


def u5():
    py = "Traceback (most recent call last):\nKeyError: 'sigma'"
    fb = '    STEP3 GPU solve unavailable (OutOfMemoryError: out of memory allocating 8589934592 bytes) → CPU fallback'
    rows = {}
    for nm, log in (('fallback_then_bug', fb + '\n' + py), ('bug_only', py)):
        got = TM.pd_cause(f'U5_{nm}', '[p2] run\n' + log + '\n', ('gu', ('GROUP_UNCONFIRMED', None, 1), None, None))
        got_rc = TM.pd_cause(f'U5_{nm}_rc', '[p2] run\n' + log + '\n', ('rc1', ('RUNNER_RC', None, 1), None, None))
        rows[nm] = {'group_unconfirmed_rc1': got, 'runner_rc_path': got_rc}
    out('U5', rows=rows, note='(원인, 결과 전 · 뒤, 재실행 자격)')


def u6():
    out_dir, tok = TM.gr_fake_launch('U6')
    lp = out_dir / 'groups' / 'L01_floor.launch.json'
    other = {'schema': 'rint-r-group-v1', 'name': 'L01_floor', 'token': 'e' * 32, 'rc': 0, 'cause': None, 'confirmed': False, 'by': 'chain',
             'ended_utc': '2026-11-02T00:00:02Z'}
    lp.with_name('L01_floor.end.json').write_text(json.dumps(other), encoding='utf-8')
    end, held = RR.recover_group(lp, RR.host_ident())
    out('U6', launch_token=tok, prev_end_token=other['token'], held=held, new_end_token=(end or {}).get('token'),
        chain_end=(end or {}).get('chain_end'))


def u7():
    root = Path(TM.TD) / 'u7'
    real = root / 'real' / 'attempt_1'
    real.mkdir(parents=True)
    aj = {'schema': 'rint-r-attempt-v1', 'n': 1, 'target': 'ladder:P0', 'machine': TM.MACH, 'resume_of': None, 'ledger_commit': 'a' * 40}
    (real / 'attempt.json').write_text(json.dumps(aj), encoding='utf-8')
    st = {'entries': {1: {'target': 'ladder:P0:FIBRE', 'machine': TM.MACH, 'resume_of': None}}}
    lk = root / 'lnk' / 'attempt_1'
    lk.mkdir(parents=True)
    (lk / 'attempt.json').symlink_to(real / 'attempt.json')
    dl = root / 'dirlink'
    dl.mkdir(parents=True)
    (dl / 'attempt_1').symlink_to(real, target_is_directory=True)
    got = {'real_folder': RR.found_attempts_problem(st, RR._attempt_folders([root / 'real'])),
           'attempt_json_symlink': RR.found_attempts_problem(st, RR._attempt_folders([root / 'lnk'])),
           'folder_symlink': RR.found_attempts_problem(st, RR._attempt_folders([dl]))}
    out('U7', rows={k: (v[:120] if isinstance(v, str) else v) for k, v in got.items()})


def u8():
    """(등록 R ⑦ PC6-13 문장 "정리 중 신호 = 런 기록 rc None = group_unconfirmed 그대로") — 요약 있는 길 (멈춤 GROUP_UNCONFIRMED · 그룹 원인 signal_after ·
    런 기록 rc None) ↔ 요약 없는 길 (사슬 끝 기록 = 디스크 원인 None · rc 1 · 미확인 → recover 가 chain_end 로 옮김)."""
    rows = {}
    rows['summary_gu_signal_after'] = TM.pd_cause('U8_sum', '[p2] run\n', ('gu', ('GROUP_UNCONFIRMED', 'signal_after', None), None, None))
    f = TM.pc_folder('U8_orphan', {TM.PC_MARK: '{}\n'})
    TM.pc_group(f, 'L01_floor', {'by': 'recover', 'cause': 'parent_dead', 'rc': None, 'confirmed': True,
                                 'chain_end': {'rc': 1, 'cause': None, 'confirmed': False, 'ended_utc': '2026-11-02T00:00:00Z'}}, '[p2] run\n')
    r = RR.attempt_result_line(1, f, None, 'recover')
    rows['orphan_chain_end_rc1_cause_none'] = [r['cause'], r['side'], r['resume_ok']]
    out('U8', rows=rows, note='signal_after 의 디스크 끝 기록 원인 = None (run_in_group 설명문) → chain_end 로는 정리 중 신호를 가를 수 없다')


if __name__ == '__main__':
    setup()
    out('env', python=sys.version.split()[0], td=TM.TD)
    for k, fn in (('U1', u1), ('U2', u2), ('U3', u3), ('U4', u4), ('U5', u5), ('U6', u6), ('U7', u7), ('U8', u8)):
        if k in ONLY:
            t0 = time.time()
            try:
                fn()
            except Exception as e:                       # noqa: BLE001 — 탐침 실패 = 기록
                import traceback
                out(k, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:])
            out(k + '_t', seconds=round(time.time() - t0, 1))
