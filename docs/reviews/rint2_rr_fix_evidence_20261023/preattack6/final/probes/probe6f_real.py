#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 6 회차 마무리 (11-02 · 사슬 코드 = 4c69070ad 와 바이트 같음) — 실경로 탐침 (사슬 `rint_r_chain.main` · 시험 틀 고정물 · 가짜 러너 ·
실제 프로세스 그룹 · 실제 git 원장).  시험 파일 · 사슬은 고치지 않는다 (가짜 러너의 기존 고장 rc2 · oom_after_mark · msg_sleep_after_mark 만).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack6/final/probes/probe6f_real.py <임시 폴더 바탕> [R5,R6,R7]

R5  (중간 보고 PC6-07 실경로) — (a) 원 시도: 바닥 런 완주 · 천장 런 표지 전 rc 2 (자원 낱말 없음) (b) 재실행: 원 시도 천장 OOM (표지 뒤 · 자격) →
    재실행 시도가 바닥 복사 뒤 천장에서 표지 전 rc 2 (c) 새 시도: 첫 런 (바닥) 표지 전 rc 2 → 결과 줄 · 다음 --add 꼴
R6  (새 반례 후보) 사슬 부모 SIGKILL (표지 뒤 · 러너 그룹 삶) 뒤 recover 대신 **같은 --attempt 번호로 사다리를 다시 실행** → 옆 거부 기록 · 결과 줄
    (rejected · 결과 전) · 그때 원 그룹 삶? · 새 시도 --add · 새 시도 완주 · 판정 (그대로 · 옛 attempt_1 폴더를 옮긴 뒤)
R7  git replace — 원장 저장소에 replace 참조 하나 (정직한 결과 커밋 → 원인 · 재실행 자격만 바꾼 커밋) + 작업 파일 = 바꾼 판 → 사슬이 읽는 원장 · HEAD sha ·
    --add --resume · 판정 (결과 줄 다시 셈이 잡나)
값 · σ 를 찍지 않는다.
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.gettempdir()).resolve()
BASE.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'R5', 'R6', 'R7'}
PLAIN = '[p2] solving (probe · 보통 줄)'

DRIVER = r'''
import json, os, signal, sys
from pathlib import Path
signal.signal(signal.SIGINT, signal.default_int_handler)
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.HERE = Path(cfg['here'])
os.environ.update(cfg['env'])
sys.exit(RR.main(cfg['argv']))
'''


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def setup():
    TM.RR = RR
    TM.TD = tempfile.mkdtemp(prefix='pa6f_real_', dir=str(BASE))
    TM.fixtures()


def spawn(tag, argv, wpath):
    drv = Path(TM.TD) / 'pa6f_driver.py'
    if not drv.exists():
        drv.write_text(DRIVER, encoding='utf-8')
    cfg = Path(TM.TD) / f'{tag}_cfg.json'
    cfg.write_text(json.dumps({'scripts': str(WT / 'scripts'), 'here': str(RR.HERE), 'env': {'FAKE_WORLD': str(wpath)},
                               'argv': [str(a) for a in argv]}), encoding='utf-8')
    log = open(Path(TM.TD) / f'{tag}_chain.log', 'w', encoding='utf-8')
    return subprocess.Popen([sys.executable, '-I', str(drv), str(cfg)], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def wait_text(p, needle, t=30.0):
    t_end = time.time() + t
    while time.time() < t_end:
        try:
            if needle in Path(p).read_text(encoding='utf-8', errors='replace'):
                return True
        except OSError:
            pass
        time.sleep(0.05)
    return False


def adopt(d, target='ladder:P0'):
    ad = RR.adoption(RR.ledger_parse(TM.led_raw(d)), target)
    return {'chain': ad['chain'], 'effective': ad['effective'], 'problems': ad['problems']}


def r5():
    rows = {}
    # (a) 원 시도 — 바닥 완주 (표지 · payload) · 천장 표지 전 rc 2
    d, _rc, _so = TM.led_new('R5a')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('R5a', TM.world('R5a', dict(TM.PW, faults=[{'do': 'rc2', 'match': {'rj': '0'}}])), d, n1)
    add = TM.led_add(d, 'ladder:P0', resume=n1)
    add_new = TM.led_add(d, 'ladder:P0')
    rows['a_original'] = {'stop': TM.stop_code(a), 'result': TM.pc_res(d, n1), 'add_resume_rc': add[0], 'add_new_rc': add_new[0],
                          'add_new_tail': add_new[2].strip().splitlines()[-1][:120]}
    # (b) 재실행 — 원 시도 천장 OOM (자격) → 재실행이 바닥 복사 뒤 천장 표지 전 rc 2
    d, _rc, _so = TM.led_new('R5b')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('R5b', TM.world('R5b_a', dict(TM.PW, faults=[{'do': 'oom_after_mark', 'match': {'rj': '0'}}])), d, n1)
    r1 = TM.pc_res(d, n1)
    _r, n2, _s = TM.led_add(d, 'ladder:P0', resume=n1)
    b = TM.lad_att('R5b', TM.world('R5b_b', dict(TM.PW, faults=[{'do': 'rc2', 'match': {'rj': '0'}}])), d, n2, base=a['base'])
    add3 = TM.led_add(d, 'ladder:P0', resume=n1)
    add_new = TM.led_add(d, 'ladder:P0')
    rows['b_resume'] = {'orig': r1, 'resume_stop': TM.stop_code(b), 'resume_copied': ((b['sum'] or {}).get('resume') or {}).get('copied'),
                        'resume_result': TM.pc_res(d, n2), 'add_resume_again_rc': add3[0], 'add_resume_tail': add3[2].strip().splitlines()[-1][:120],
                        'add_new_rc': add_new[0], 'adoption': adopt(d)}
    # (c) 새 시도 — 첫 런 표지 전 rc 2
    d, _rc, _so = TM.led_new('R5c')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    c = TM.lad_att('R5c', TM.world('R5c', dict(TM.PW, faults=[{'do': 'rc2', 'match': {'rj': 'inf'}}])), d, n1)
    add_new = TM.led_add(d, 'ladder:P0')
    rows['c_first_run'] = {'stop': TM.stop_code(c), 'result': TM.pc_res(d, n1), 'add_new_rc': add_new[0]}
    out('R5', rows=rows)


def r6():
    d, _rc, _so = TM.led_new('R6')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    base = Path(TM.TD) / 'runs' / 'R6'
    w = TM.world('R6', dict(TM.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': PLAIN, 's': 25.0, 'match': {'rj': 'inf'}}]))
    pr = spawn('R6', TM.ladder_argv(base) + ['--ledger', str(d), '--attempt', str(n1)], w)
    f1 = base / f'attempt_{n1}'
    seen = wait_text(f1 / 'logs' / 'L01_floor.log', 'solving (probe')
    time.sleep(0.2)
    os.kill(pr.pid, signal.SIGKILL)
    pr.wait()
    L = json.loads((f1 / 'groups' / 'L01_floor.launch.json').read_text(encoding='utf-8'))
    tok = L.get('token')
    alive0 = TM.gr_alive(tok)
    side1 = RR.folder_side(f1)
    # 운영자가 recover 대신 같은 명령 (같은 --attempt) 을 다시 친다
    again = TM.lad_att('R6', TM.world('R6_again'), d, n1, base=base)
    sidefile = base / f'attempt_{n1}.rejected.json'
    r1 = TM.led_result(d, n1)
    alive1 = TM.gr_alive(tok)
    end_exists = (f1 / 'groups' / 'L01_floor.end.json').exists()
    add2 = TM.led_add(d, 'ladder:P0')
    alive2 = TM.gr_alive(tok)
    b = TM.lad_att('R6', TM.world('R6_b'), d, add2[1], base=base) if add2[1] else None
    alive3 = TM.gr_alive(tok)
    v1 = TM.ver_led('R6_v1', [b['out']], d) if b else None
    # 옛 attempt_1 폴더를 다른 곳으로 옮긴다 (원장 = 시도 1 은 거부 기록 파일 · 이 폴더는 "원장에 없는 시도 폴더" 라는 화면을 보고 치움)
    moved = Path(TM.TD) / 'moved_attempt_1'
    shutil.move(str(f1), str(moved))
    v2 = TM.ver_led('R6_v2', [b['out']], d) if b else None
    # 끝 정리 — 옮긴 폴더에서 recover (그룹 정리 · 결과 줄은 이미 있음)
    rc_rec, so_rec = TM.call(['--stage', 'recover', '--out', str(moved), '--ledger', str(d)], w)
    out('R6', seen=seen, chain_side_before_rerun=side1, group_alive_after_kill=bool(alive0), rerun_rc=again['rc'],
        rerun_tail=again['so'].strip().splitlines()[-1][:200] if again['so'] else None, sidefile=sidefile.exists(),
        result1={k: (r1 or {}).get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'folder', 'by')},
        group_alive_when_result_written=bool(alive1), end_record_of_attempt1=end_exists, add2_rc=add2[0], add2_n=add2[1],
        group_alive_after_add2=bool(alive2), attempt2_rc=(b or {}).get('rc'), attempt2_status=((b or {}).get('sum') or {}).get('status'),
        group_alive_after_attempt2=bool(alive3), adoption=adopt(d),
        verdict_before_move=(TM.stop_code(v1) if v1 else None),
        verdict_before_move_why=(str((((v1 or {}).get('v') or {}).get('stop') or {}).get('cause'))[:200]),
        verdict_after_move=(TM.stop_code(v2) if v2 else None),
        verdict_after_move_ledger_stop=((TM.stop_code(v2) in TM.LEDGER_STOPS) if v2 else None),
        recover_after_rc=rc_rec, recover_tail=so_rec.strip().splitlines()[-2:] if so_rec else None)


def r7():
    d, _rc, _so = TM.led_new('R7')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('R7', TM.world('R7_a', dict(TM.PW, faults=[{'do': 'illegal_driver_after_mark', 'match': {'rj': 'inf'}}])), d, n1)
    honest = TM.git_(d, 'rev-parse', 'HEAD')
    raw_h = TM.led_raw(d)
    res1 = TM.led_result(d, n1)
    forged = dict(res1, cause='resource', resume_ok=True)
    lines = raw_h.decode('utf-8').splitlines()
    lines[-1] = json.dumps(forged, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    new_raw = ('\n'.join(lines) + '\n').encode('utf-8')
    # 같은 부모 · 바꾼 원장 blob 의 커밋 객체를 만들고 replace 로 정직한 커밋 자리에 끼운다 (HEAD sha 그대로)
    blob = TM.git_(d, 'hash-object', '-w', '--stdin', inp=new_raw)
    tree_txt = f'100644 blob {blob}\t{TM.LEDGER_NAME}\n'
    tree = TM.git_(d, 'mktree', inp=tree_txt.encode('utf-8'))
    parent = TM.git_(d, 'rev-parse', 'HEAD~1')
    fc = TM.git_(d, 'commit-tree', tree, '-p', parent, '-m', 'forged (probe)')
    TM.git_(d, 'replace', honest, fc)
    (d / TM.LEDGER_NAME).write_bytes(new_raw)
    head_after = TM.git_(d, 'rev-parse', 'HEAD')
    seen_raw = RR.ledger_blob(d, RR.ledger_head(d))
    try:
        RR.ledger_now(d)
        now = 'ok'
    except RR.Stop as e:
        now = f'{e.code}'
    hist = RR.ledger_history_problem(d, RR.ledger_head(d))
    add = TM.led_add(d, 'ladder:P0', resume=n1)
    b = None
    if add[1]:
        b = TM.lad_att('R7', TM.world('R7_b'), d, add[1], base=a['base'])
    v = TM.ver_led('R7_v', [a['out']], d)
    out('R7', honest_cause=res1.get('cause'), head_same_sha=(head_after == honest), chain_reads_forged=(seen_raw == new_raw), ledger_now=now,
        history_problem=hist, add_resume_rc=add[0], add_resume_tail=add[2].strip().splitlines()[-1][:160],
        resume_attempt_rc=(b or {}).get('rc'), resume_attempt_stop=(TM.stop_code(b) if b else None),
        resume_attempt_why=(str((((b or {}).get('sum') or {}).get('stop') or {}).get('cause'))[:200] if b else None),
        verdict_stop=TM.stop_code(v), verdict_why=str((((v or {}).get('v') or {}).get('stop') or {}).get('cause'))[:200])


def r9():
    """(중간 보고 PC6-08 실경로) 옆 거부 기록 (attempt_<n>.rejected.json · 시도 폴더가 이미 있음) 을 쓰고 결과 줄 커밋 전에 죽은 꼴 → recover · 다음 --add ·
    같은 명령 다시 · 대조 = 시도 폴더 안 rejected.json (PC13 꼴)."""
    rows = {}
    for tag, side in (('side_file', True), ('in_folder', False)):
        d, _rc, _so = TM.led_new(f'R9_{tag}')
        _r, n1, _s = TM.led_add(d, 'ladder:P0')
        base = Path(TM.TD) / 'runs' / f'R9_{tag}'
        if side:
            (base / f'attempt_{n1}').mkdir(parents=True)
            (base / f'attempt_{n1}' / 'old.txt').write_text('old', encoding='utf-8')
        old = RR.ledger_append

        def dies(repo, obj, msg, expect=None, _n=n1, _old=old):
            if obj.get('kind') == 'result' and obj.get('n') == _n:
                raise RR.Stop('ATTEMPT_LEDGER_MISMATCH', '결과 줄 커밋 전 죽음 흉내 (탐침)')
            return _old(repo, obj, msg, expect=expect)
        RR.ledger_append = dies
        try:
            kw = {} if side else {'machine': 'gabia'}
            a = TM.lad_att(f'R9_{tag}', TM.world(f'R9_{tag}'), d, n1, base=base, **kw)
        finally:
            RR.ledger_append = old
        rec_rc, rec_so = TM.call(['--stage', 'recover', '--out', str(base), '--ledger', str(d)])
        r1 = TM.led_result(d, n1)
        add2 = TM.led_add(d, 'ladder:P0')
        again = TM.lad_att(f'R9_{tag}', TM.world(f'R9_{tag}_again'), d, n1, base=base)
        rows[tag] = {'attempt_rc': a['rc'], 'side_file_exists': (base / f'attempt_{n1}.rejected.json').exists(),
                     'in_folder_rejected': (base / f'attempt_{n1}' / 'rejected.json').exists(), 'recover_rc': rec_rc,
                     'recover_tail': rec_so.strip().splitlines()[-1:] if rec_so else None,
                     'result_after_recover': {k: (r1 or {}).get(k) for k in ('status', 'side', 'cause', 'by', 'folder')} if r1 else None,
                     'next_add_rc': add2[0], 'next_add_tail': add2[2].strip().splitlines()[-1][:140],
                     'rerun_same_rc': again['rc'], 'rerun_same_tail': again['so'].strip().splitlines()[-1][:140] if again['so'] else None}
    out('R9', rows=rows)


def r10():
    """(새 반례 후보 · PC5-01 의 다시 셈을 비켜 가는 길) 정직한 원장 = 항목 1 (ladder:P0) + 결과 줄 1 (잘못된 주소 · runner_rc · 재실행 자격 False · 결과 뒤 =
    채택) → 원장 clone 에서 끝 두 커밋을 되돌리고 (`reset --hard HEAD~2`) 항목 1 의 **대상만** 다른 대상 (ladder:P0:FIBRE) 으로 바꿔 다시 커밋 (결과 줄 = 그대로
    복사 · 없음 두 꼴) → 같은 대상 (ladder:P0) 새 시도 --add · 실행 → 판정 (입력 = 새 시도 · 바탕 = 시도 1 폴더가 있는 같은 바탕).  시도 1 폴더 (attempt.json
    대상 ladder:P0 · 시작 커밋 = 버린 커밋) 는 그대로."""
    rows = {}
    d, _rc, _so = TM.led_new('R10')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('R10', TM.world('R10_a', dict(TM.PW, faults=[{'do': 'illegal_driver_after_mark', 'match': {'rj': 'inf'}}])), d, n1)
    honest_res = TM.led_result(d, n1)
    honest_add = TM.led_add(TM.led_clone(d, 'R10_ctl'), 'ladder:P0')
    lines = TM.led_lines(d)
    e1 = [x for x in lines if x.get('kind') == 'entry' and x.get('n') == n1][0]
    r1 = [x for x in lines if x.get('kind') == 'result' and x.get('n') == n1][0]
    for tag, with_result in (('entry_and_result', True), ('entry_only', False)):
        dr = TM.led_clone(d, f'R10_{tag}')
        TM.git_(dr, 'reset', '-q', '--hard', 'HEAD~2')
        TM.led_hand(dr, dict(e1, target='ladder:P0:FIBRE'), msg='항목 1 대상만 바꿈 (탐침)')
        if with_result:
            TM.led_hand(dr, r1, msg='결과 줄 1 그대로 (탐침)')
        hist = RR.ledger_history_problem(dr, RR.ledger_head(dr))
        add2 = TM.led_add(dr, 'ladder:P0')
        base = TM.pc_copy_base(a['base'], f'R10_{tag}_base')
        b = TM.lad_att(f'R10_{tag}_b', TM.world(f'R10_{tag}_b'), dr, add2[1], base=base) if add2[1] else None
        v = TM.ver_led(f'R10_{tag}_v', [b['out']], dr) if b else None
        att1 = RR.read_attempt(base / f'attempt_{n1}')
        rows[tag] = {'history_problem': hist, 'add2_rc': add2[0], 'add2_n': add2[1], 'attempt2_rc': (b or {}).get('rc'),
                     'attempt2_status': ((b or {}).get('sum') or {}).get('status'),
                     'attempt1_folder_target': (att1 or {}).get('target'),
                     'attempt1_start_commit_is_ancestor': RR.ledger_is_ancestor(dr, (att1 or {}).get('ledger_commit'), RR.ledger_head(dr)),
                     'verdict_stop': (TM.stop_code(v) if v else None),
                     'verdict_ledger_stop': ((TM.stop_code(v) in TM.LEDGER_STOPS) if v else None),
                     'verdict_why': str((((v or {}).get('v') or {}).get('stop') or {}).get('cause'))[:200],
                     'verdict_ledger_targets': (((v or {}).get('v') or {}).get('ledger') or {}).get('targets')}
    out('R10', honest_result={k: honest_res.get(k) for k in ('status', 'side', 'cause', 'resume_ok')},
        control_add_same_target_rc=honest_add[0], control_add_tail=honest_add[2].strip().splitlines()[-1][:120], rows=rows)


def r11():
    """(변이 M2e 생존의 뜻) 정직한 결과 줄 = 결과 뒤 · 원인 resource (OOM 낱말) · 재실행 자격 False (검사 실패 흔적 = .unchecked/ 의 팔 payload) → 원장 clone 에서
    끝 줄의 resume_ok 만 True 로 (reset + 손 줄) → --add --resume 1 · 재실행 시도 (지금 사슬 = 다시 셈 칸에 resume_ok 가 있어 잡아야 한다)."""
    d, _rc, _so = TM.led_new('R11')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('R11', TM.world('R11_a', dict(TM.PW, faults=[{'do': 'unchecked_fail', 'oom': True, 'match': {'rj': 'inf'}}])), d, n1)
    res1 = TM.led_result(d, n1)
    dr = TM.led_clone(d, 'R11_forged')
    TM.git_(dr, 'reset', '-q', '--hard', 'HEAD~1')
    TM.led_hand(dr, dict(res1, resume_ok=True), msg='resume_ok 만 바꿈 (탐침)')
    add = TM.led_add(dr, 'ladder:P0', resume=n1)
    base = TM.pc_copy_base(a['base'], 'R11_base')
    b = TM.lad_att('R11_b', TM.world('R11_b'), dr, add[1], base=base) if add[1] else None
    rj = (b['out'] / 'rejected.json') if b else None
    rec = json.loads(rj.read_text(encoding='utf-8')) if rj is not None and rj.exists() else {}
    v = TM.ver_led('R11_v', [a['out']], dr)
    out('R11', honest={k: (res1 or {}).get(k) for k in ('status', 'side', 'cause', 'resume_ok')}, add_resume_rc=add[0],
        resume_attempt_rc=(b or {}).get('rc'), resume_rejected_code=rec.get('code'), resume_rejected_cause=str(rec.get('cause'))[:200],
        verdict_stop=TM.stop_code(v), verdict_why=str((((v or {}).get('v') or {}).get('stop') or {}).get('cause'))[:200])


if __name__ == '__main__':
    setup()
    out('env', python=sys.version.split()[0], td=TM.TD)
    for k, fn in (('R5', r5), ('R6', r6), ('R7', r7), ('R9', r9), ('R10', r10), ('R11', r11)):
        if k in ONLY:
            t0 = time.time()
            try:
                fn()
            except Exception as e:                       # noqa: BLE001 — 탐침 실패 = 기록
                import traceback
                out(k, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:])
            out(k + '_t', seconds=round(time.time() - t0, 1))
