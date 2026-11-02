#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 7 회차 (11-02 · 대상 0658c0ac6) — 실경로 탐침.  사슬 · 시험 파일은 고치지 않는다 (시험 틀 고정물 · 가짜 러너 · 실제 git 원장을 불러 씀).

  python3 -I docs/reviews/rint2_rr_fix_evidence_20261023/preattack7/probes/probe7_real.py <임시 폴더 바탕> [A,B]

A  (PC6-12 닫힘 주장 · found_attempts_problem 의 범위) — 6 회차 R10 (끝 두 커밋 reset + 항목 1 의 대상만 ladder:P0:FIBRE · 결과 줄 그대로) 위에
   시도 1 폴더 쪽 손 하나: a0 = 손 없음 (대조 · 고친 사슬 = 멈춤 기대) · a1 = attempt.json 지움 · a2 = attempt.json 에 칸 하나 더 (꼴 틀림) ·
   a3 = 폴더 이름을 attempt_1.old 로 (같은 바탕 안) → 같은 대상 새 시도 2 · 판정 (입력 = 시도 2) · 예측 입력 대조 (P1 사다리 + 예측).
B  (PC6-13 의 chain_end · 요약 없는 길) — 사슬이 러너를 기다리는 동안 SIGINT (KeyboardInterrupt = 그룹 원인 exception) · 그룹 미확인 (group_settle =
   진짜 정리 뒤 미확인으로 알림 · PD13 구동기 꼴) → 끝 기록 by chain (원인 exception) · 요약 없음 → recover --ledger → 결과 줄 · --add --resume 1.
   대조 b_conf = 같은 SIGINT · 그룹 확인 (구동기 바꿈 없음).
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

WT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

BASE = Path(sys.argv[1] if len(sys.argv) > 1 else tempfile.gettempdir()).resolve()
BASE.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else {'A', 'B'}

DRIVER_B = r'''
import json, os, signal, sys
from pathlib import Path
signal.signal(signal.SIGINT, signal.default_int_handler)
cfg = json.load(open(sys.argv[1], encoding='utf-8'))
sys.path.insert(0, cfg['scripts'])
import rint_r_chain as RR
RR.HERE = Path(cfg['here'])
os.environ.update(cfg['env'])
if cfg.get('unconfirmed'):
    _settle = RR.group_settle

    def settle(token, limit=None):
        _c, _left, n = _settle(token, limit)
        return False, [999987], n
    RR.group_settle = settle
sys.exit(RR.main(cfg['argv']))
'''


def out(tag, **kw):
    print(json.dumps(dict(probe=tag, **kw), ensure_ascii=False, sort_keys=True, default=str), flush=True)


def setup():
    TM.RR = RR
    TM.TD = tempfile.mkdtemp(prefix='pa7_real_', dir=str(BASE))
    TM.fixtures()


def vwhy(v):
    return str((((v or {}).get('v') or {}).get('stop') or {}).get('cause'))[:220]


def probe_a():
    d, _rc, _so = TM.led_new('A')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    a = TM.lad_att('A', TM.world('A_a', dict(TM.PW, faults=[{'do': 'illegal_driver_after_mark', 'match': {'rj': 'inf'}}])), d, n1)
    honest = TM.pc_res(d, n1)
    lines = TM.led_lines(d)
    e1 = [x for x in lines if x.get('kind') == 'entry' and x.get('n') == n1][0]
    r1 = [x for x in lines if x.get('kind') == 'result' and x.get('n') == n1][0]
    rows = {}
    for tag in ('a0_control', 'a1_rm_attempt_json', 'a2_extra_key', 'a3_rename_in_base'):
        dr = TM.led_clone(d, f'A_{tag}')
        TM.git_(dr, 'reset', '-q', '--hard', 'HEAD~2')
        TM.led_hand(dr, dict(e1, target='ladder:P0:FIBRE'), msg='항목 1 대상만 바꿈 (탐침 7)')
        TM.led_hand(dr, r1, msg='결과 줄 1 그대로 (탐침 7)')
        base = TM.pc_copy_base(a['base'], f'A_{tag}_base')
        f1 = base / f'attempt_{n1}'
        hand = None
        if tag == 'a1_rm_attempt_json':
            (f1 / 'attempt.json').unlink()
            hand = 'rm attempt_1/attempt.json'
        elif tag == 'a2_extra_key':
            aj = json.loads((f1 / 'attempt.json').read_text(encoding='utf-8'))
            aj['note'] = 'x'
            (f1 / 'attempt.json').write_text(json.dumps(aj), encoding='utf-8')
            hand = 'attempt.json += {"note": "x"}'
        elif tag == 'a3_rename_in_base':
            f1.rename(base / f'attempt_{n1}.old')
            hand = 'mv attempt_1 attempt_1.old (같은 바탕)'
        add2 = TM.led_add(dr, 'ladder:P0')
        b = TM.lad_att(f'A_{tag}_b', TM.world(f'A_{tag}_b'), dr, add2[1], base=base) if add2[1] else None
        v = TM.ver_led(f'A_{tag}_v', [b['out']], dr) if b else None
        row = {'hand': hand, 'add2_rc': add2[0], 'b_status': ((b or {}).get('sum') or {}).get('status'),
               'verdict_stop': TM.stop_code(v) if v else None,
               'verdict_is_ledger_stop': (TM.stop_code(v) in TM.LEDGER_STOPS) if v else None, 'verdict_why': vwhy(v),
               'ledger_targets': ((((v or {}).get('v') or {}).get('ledger') or {}).get('targets'))}
        # 예측 입력 대조 (사다리 바탕의 시도 1 폴더) — P1 사다리 + 예측
        _r3, n3, _s3 = TM.led_add(dr, 'ladder:P1')
        c = TM.lad_att(f'A_{tag}_P1', TM.world(f'A_{tag}_c'), dr, n3, law='P1')
        _r4, n4, _s4 = TM.led_add(dr, 'predict')
        wp = TM.world(f'A_{tag}_p')
        p = TM.pred_att(f'A_{tag}_pred', wp, dr, n4, [b['out'], c['out']]) if b else None
        row.update(predict_stop=TM.stop_code(p) if p else None, predict_calls=TM.n_calls(wp),
                   predict_result=TM.pc_res(dr, n4, keys=('status', 'side', 'cause')),
                   predict_why=str((((p or {}).get('sum') or {}).get('stop') or {}).get('cause'))[:220] if p else None)
        rows[tag] = row
    out('A', honest=honest, rows=rows)


def spawn_b(tag, argv, wpath, unconfirmed):
    drv = Path(TM.TD) / 'pa7_driver_b.py'
    if not drv.exists():
        drv.write_text(DRIVER_B, encoding='utf-8')
    cfg = Path(TM.TD) / f'{tag}_cfg.json'
    cfg.write_text(json.dumps({'scripts': str(WT / 'scripts'), 'here': str(RR.HERE), 'env': {'FAKE_WORLD': str(wpath)},
                               'argv': [str(x) for x in argv], 'unconfirmed': unconfirmed}), encoding='utf-8')
    log = open(Path(TM.TD) / f'{tag}_chain.log', 'w', encoding='utf-8')
    return subprocess.Popen([sys.executable, '-I', str(drv), str(cfg)], stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def probe_b():
    rows = {}
    for tag, unconfirmed in (('b_unconf', True), ('b_conf', False)):
        d, _rc, _so = TM.led_new(f'B_{tag}')
        _r, n1, _s = TM.led_add(d, 'ladder:P0')
        base = Path(TM.TD) / 'runs' / f'B_{tag}'
        w = TM.world(f'B_{tag}', dict(TM.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': '[p2] solving (probe7 B)', 's': 25.0,
                                                       'match': {'rj': 'inf'}}]))
        pr = spawn_b(f'B_{tag}', TM.ladder_argv(base) + ['--ledger', str(d), '--attempt', str(n1)], w, unconfirmed)
        f1 = base / f'attempt_{n1}'
        t_end, seen = time.time() + 40, False
        while time.time() < t_end and not seen:
            try:
                seen = 'solving (probe7 B)' in (f1 / 'logs' / 'L01_floor.log').read_text(encoding='utf-8', errors='replace')
            except OSError:
                pass
            time.sleep(0.05)
        time.sleep(0.2)
        os.kill(pr.pid, signal.SIGINT)
        try:
            prc = pr.wait(timeout=120)
        except subprocess.TimeoutExpired:
            pr.kill()
            prc = 'timeout'
        ep = f1 / 'groups' / 'L01_floor.end.json'
        e0 = json.loads(ep.read_text(encoding='utf-8')) if ep.exists() else {}
        had_sum = (f1 / 'ladder_summary.json').exists()
        res0 = TM.led_result(d, n1)
        rc_rec, so_rec = TM.call(['--stage', 'recover', '--out', str(f1), '--ledger', str(d)], w)
        e1 = json.loads(ep.read_text(encoding='utf-8')) if ep.exists() else {}
        r1 = TM.pc_res(d, n1)
        raw = TM.led_raw(d)
        rc_add, n2, so_add = TM.led_add(d, 'ladder:P0', resume=n1)
        ks = ('by', 'rc', 'cause', 'confirmed')
        rows[tag] = {'seen': seen, 'chain_rc': prc, 'end_before_recover': {k: e0.get(k) for k in ks}, 'summary_written': had_sum,
                     'result_before_recover': res0, 'recover_rc': rc_rec, 'recover_tail': so_rec.strip().splitlines()[-2:] if so_rec else None,
                     'end_after_recover': {k: e1.get(k) for k in ks}, 'chain_end': e1.get('chain_end'), 'result': r1,
                     'add_resume_rc': rc_add, 'add_resume_tail': so_add.strip().splitlines()[-1][:160], 'ledger_changed_by_add': TM.led_raw(d) != raw}
    out('B', rows=rows)


def probe_c():
    """(PC6-09 범위) 사슬 부모 SIGKILL (표지 뒤 · 러너 그룹 삶) 뒤 같은 --attempt 1 을 **다른 --out** 으로 다시 → 그 시도가 처음부터 다시 도나 · 결과 줄 ·
    그동안 옛 그룹 삶 · 판정 (입력 = 새 바탕의 시도 1).  c2 = 재실행 항목 (--resume) 꼴 — 원 시도 OOM (자격) 뒤 재실행 2 를 바탕 1 에서 띄우고 부모 SIGKILL →
    같은 --attempt 2 를 다른 --out 으로."""
    rows = {}
    d, _rc, _so = TM.led_new('C1')
    _r, n1, _s = TM.led_add(d, 'ladder:P0')
    b1 = Path(TM.TD) / 'runs' / 'C1_base1'
    b2 = Path(TM.TD) / 'runs' / 'C1_base2'
    w = TM.world('C1', dict(TM.PW, faults=[{'do': 'msg_sleep_after_mark', 'msg': '[p2] solving (probe7 C)', 's': 25.0, 'match': {'rj': 'inf'}}]))
    pr = spawn_b('C1', TM.ladder_argv(b1) + ['--ledger', str(d), '--attempt', str(n1)], w, False)
    f1 = b1 / f'attempt_{n1}'
    t_end, seen = time.time() + 40, False
    while time.time() < t_end and not seen:
        try:
            seen = 'solving (probe7 C)' in (f1 / 'logs' / 'L01_floor.log').read_text(encoding='utf-8', errors='replace')
        except OSError:
            pass
        time.sleep(0.05)
    time.sleep(0.2)
    os.kill(pr.pid, signal.SIGKILL)
    pr.wait()
    L = json.loads((f1 / 'groups' / 'L01_floor.launch.json').read_text(encoding='utf-8'))
    tok = L.get('token')
    alive0 = bool(TM.gr_alive(tok))
    side1 = RR.folder_side(f1)
    again = TM.lad_att('C1_again', TM.world('C1_again'), d, n1, base=b2)
    alive1 = bool(TM.gr_alive(tok))
    r1 = TM.led_result(d, n1)
    v = TM.ver_led('C1_v', [again['out']], d)
    rows['c1_same_entry_other_out'] = {
        'seen': seen, 'orig_side': side1, 'orig_group_alive_after_kill': alive0, 'rerun_rc': again['rc'],
        'rerun_status': ((again['sum'] or {}).get('status')), 'rerun_tail': (again['so'].strip().splitlines() or [''])[-1][:200],
        'orig_group_alive_after_rerun': alive1, 'result1': {k: (r1 or {}).get(k) for k in ('status', 'side', 'cause', 'resume_ok', 'folder', 'by')},
        'verdict_stop': TM.stop_code(v), 'verdict_is_ledger_stop': TM.stop_code(v) in TM.LEDGER_STOPS, 'verdict_why': vwhy(v),
        'ledger_targets': ((((v or {}).get('v') or {}).get('ledger') or {}).get('targets'))}
    #  정리 — 옛 바탕 recover (고아 그룹 죽임 · 결과 줄은 이미 있음)
    rc_rec, so_rec = TM.call(['--stage', 'recover', '--out', str(f1), '--ledger', str(d)], w)
    rows['c1_cleanup_recover'] = {'rc': rc_rec, 'tail': so_rec.strip().splitlines()[-2:] if so_rec else None, 'alive_after': bool(TM.gr_alive(tok))}
    out('C', rows=rows)


if __name__ == '__main__':
    setup()
    out('env', python=sys.version.split()[0], td=TM.TD, head=subprocess.run(['git', '-C', str(WT), 'rev-parse', 'HEAD'], capture_output=True,
                                                                               text=True).stdout.strip())
    for k, fn in (('A', probe_a), ('B', probe_b), ('C', probe_c)):
        if k in ONLY:
            t0 = time.time()
            try:
                fn()
            except Exception as e:                       # noqa: BLE001 — 탐침 실패 = 기록
                import traceback
                out(k, error=f'{type(e).__name__}: {e}', tb=traceback.format_exc()[-1500:])
            out(k + '_t', seconds=round(time.time() - t0, 1))
