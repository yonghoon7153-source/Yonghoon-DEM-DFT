#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 10 회차 (독립) 단위 탐침 — scripts/rint_r_chain.py 의 고친 판 (f5b00a838) ↔ 바탕 (18bb6a2e4) 을 같은 손 입력으로.

쓰는 법 (리포 밖 임시 폴더에서 · python3 -I):
  python3 -I probe_units.py <rint_r_chain.py 가 있는 폴더> <scripts 폴더 (형제 모듈)> <출력 json>
- 원장 · git · 러너 없음 — 함수 직접 호출 (orphan_cause · result_fields · run_log_text · stop_log_readable · stage_summary_read ·
  read_summary · _verdict_compute 입구 · write_summary 바이트).  막힐 수 있는 칸 (FIFO) 은 포크한 자식 + 시간 상한.
- 판정 아님 · 관찰 기록.
"""
import hashlib
import json
import os
import signal
import socket
import sys
import tempfile
from pathlib import Path

MOD_DIR, SCRIPTS_DIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, MOD_DIR)
import rint_r_chain as RR  # noqa: E402

assert Path(RR.__file__).resolve().parent == Path(MOD_DIR).resolve(), RR.__file__
TD = Path(tempfile.mkdtemp(prefix='pa10_units_'))
MARK = 'L01_floor_arm1/.unchecked/p2_SBE_vgcf100_a0.json.first_result.json'
TB = "[p2] run\nTraceback (most recent call last):\nKeyError: 'sigma'\n"
NEW = hasattr(RR, 'rc_kind')
out = {'module': str(Path(RR.__file__).resolve()), 'module_sha256': hashlib.sha256(Path(RR.__file__).read_bytes()).hexdigest(),
       'is_new': NEW, 'rows': {}}


def folder(tag, mark=True):
    f = TD / tag / 'attempt_1'
    f.mkdir(parents=True)
    if mark:
        (f / MARK).parent.mkdir(parents=True, exist_ok=True)
        (f / MARK).write_text('{}\n', encoding='utf-8')
    return f


def group(f, name, end, log=TB):
    (f / 'groups').mkdir(parents=True, exist_ok=True)
    tok = hashlib.sha256(f'{f}|{name}'.encode()).hexdigest()[:32]
    L = {'schema': 'rint-r-group-v1', 'name': name, 'token': tok, 'pid': 4194305, 'pgid': 4194305, 'argv': ['bash'], 'host': RR.host_ident(),
         'started_utc': '2026-11-06T00:00:00Z', 'by': 'chain', 'chain_pid': 4194305}
    E = dict({'schema': 'rint-r-group-v1', 'name': name, 'token': tok, 'rc': None, 'cause': None, 'signal': None, 'confirmed': True, 'left': [],
              'left_after_exit': None, 'killed': 0, 'by': 'chain', 'ended_utc': '2026-11-06T00:00:00Z'}, **end)
    (f / 'groups' / f'{name}.launch.json').write_text(json.dumps(L), encoding='utf-8')
    (f / 'groups' / f'{name}.end.json').write_text(json.dumps(E), encoding='utf-8')
    if log is not None:
        (f / 'logs').mkdir(parents=True, exist_ok=True)
        (f / 'logs' / f'{name}.log').write_text(log, encoding='utf-8')


def rec_end(chain_end):
    return {'by': 'recover', 'cause': 'parent_dead', 'rc': None, 'confirmed': True, 'chain_end': chain_end}


def ce(rc, cause=None):
    return {'rc': rc, 'cause': cause, 'confirmed': False, 'ended_utc': '2026-11-06T00:00:00Z'}


def orphan_row(tag, end, log=TB):
    f = folder(tag)
    group(f, 'L01_floor', end, log)
    try:
        c, ok = RR.orphan_cause(f)
        rf = RR.result_fields(f, None)
        return {'cause': c, 'readable': ok, 'resume_ok': rf['resume_ok'], 'result_cause': rf['cause']}
    except Exception as e:  # noqa: BLE001
        return {'exc': f'{type(e).__name__}: {e}'[:200]}


R = out['rows']
# ── R: rc null 을 두 길이 다르게 읽는가 (끝 기록 cause None · rc null) ──
R['R1_bychain_conf_rcnull'] = orphan_row('R1', {'cause': None, 'rc': None, 'confirmed': True})
R['R2_recover_chainend_rcnull'] = orphan_row('R2', rec_end(ce(None)))
R['R3_recover_chainend_rc1'] = orphan_row('R3', rec_end(ce(1)))
R['R4_recover_chainend_rc0'] = orphan_row('R4', rec_end(ce(0)))
R['R5_bychain_conf_rc0'] = orphan_row('R5', {'cause': None, 'rc': 0, 'confirmed': True})
R['R6_recover_chainend_rcfalse'] = orphan_row('R6', rec_end(ce(False)))
R['R7_recover_chainend_rc_str0'] = orphan_row('R7', rec_end(ce('0')))
R['R8_recover_no_chainend'] = orphan_row('R8', {'by': 'recover', 'cause': 'parent_dead', 'rc': None, 'confirmed': True})
# ── C: 모르는 원인 + 자원 낱말 로그 — 두 길의 원인 글 ──
MEM = TB + 'MemoryError\n'
R['C1_bychain_weird_mem'] = orphan_row('C1', {'cause': 'weird', 'rc': 1, 'confirmed': True}, MEM)
R['C2_recover_weird_mem'] = orphan_row('C2', rec_end(ce(1, 'weird')), MEM)
ILL = TB + 'CUDA_ERROR_ILLEGAL_ADDRESS\n'
R['C3_bychain_weird_ill'] = orphan_row('C3', {'cause': 'weird', 'rc': 1, 'confirmed': True}, ILL)
R['C4_recover_weird_ill'] = orphan_row('C4', rec_end(ce(1, 'weird')), ILL)


# ── G: 요약 있는 길 GROUP_UNCONFIRMED · 런 기록 rc null + group_cause null (러너 스스로 끝남인데 rc 모름 = 모순) ──
def summ(code, rc, gcause, run='L01_floor', with_rec=True):
    s = {'status': 'STOPPED', 'stop': {'code': code, 'what': code, 'cause': 'x', 'run': run, 'reason': None}, 'runs': []}
    if with_rec:
        s['runs'] = [{'name': run, 'outdir': f'{run}_arm1', 'rc': rc, 'group_cause': gcause}]
    return s


def summ_row(tag, s, log=TB, launch=True, end=None):
    f = folder(tag)
    if launch:
        group(f, 'L01_floor', end or {'cause': None, 'rc': 1, 'confirmed': True}, log)
    elif log is not None:
        (f / 'logs').mkdir(parents=True, exist_ok=True)
        (f / 'logs' / 'L01_floor.log').write_text(log, encoding='utf-8')
    try:
        rf = RR.result_fields(f, s)
        return {'cause': rf['cause'], 'resume_ok': rf['resume_ok'], 'status': rf['status']}
    except Exception as e:  # noqa: BLE001
        return {'exc': f'{type(e).__name__}: {e}'[:200]}


R['G1_gu_rc1_gc_none'] = summ_row('G1', summ('GROUP_UNCONFIRMED', 1, None))
R['G2_gu_rcnull_gc_none'] = summ_row('G2', summ('GROUP_UNCONFIRMED', None, None))
R['G3_gu_rcnull_gc_timeout'] = summ_row('G3', summ('GROUP_UNCONFIRMED', None, 'timeout'))
R['G4_gu_rcfalse_gc_none'] = summ_row('G4', summ('GROUP_UNCONFIRMED', False, None))
# ── T: TIME_LIMIT 예외 (런 전 시간 상한) ──
R['T1_tl_norec_nolaunch_nolog'] = summ_row('T1', summ('TIME_LIMIT', None, None, with_rec=False), log=None, launch=False)
R['T2_tl_rec_nolog'] = summ_row('T2', summ('TIME_LIMIT', None, 'timeout'), log=None, launch=False)


def t3():
    f = folder('T3')
    (f / 'groups').mkdir(parents=True)
    os.symlink(str(f / 'nowhere'), str(f / 'groups' / 'L01_floor.launch.json'))
    rf = RR.result_fields(f, summ('TIME_LIMIT', None, None, with_rec=False))
    return {'cause': rf['cause'], 'resume_ok': rf['resume_ok']}


def t4():
    """끝 기록만 있고 시작 기록 없음 (생산자 차례상 없음 = 손) — 예외가 시작 기록 자리만 본다."""
    f = folder('T4')
    group(f, 'L01_floor', {'cause': 'timeout', 'rc': -9, 'confirmed': True}, log=None)
    (f / 'groups' / 'L01_floor.launch.json').unlink()
    rf = RR.result_fields(f, summ('TIME_LIMIT', None, None, with_rec=False))
    return {'cause': rf['cause'], 'resume_ok': rf['resume_ok']}


for k, fn in (('T3_tl_dangling_launch', t3), ('T4_tl_end_without_launch', t4)):
    try:
        R[k] = fn()
    except Exception as e:  # noqa: BLE001
        R[k] = {'exc': f'{type(e).__name__}: {e}'[:200]}

# ── L: run_log_text 상태 (새 판만 · 옛 판 = 글 하나) ──
lf = folder('L', mark=False)
(lf / 'logs').mkdir()
(lf / 'logs' / 'reg.log').write_text('hello', encoding='utf-8')
(lf / 'logs' / 'empty.log').write_text('', encoding='utf-8')
(lf / 'logs' / 'dir.log').mkdir()
os.symlink('/dev/null', str(lf / 'logs' / 'devnull.log'))
os.symlink('/dev/zero', str(lf / 'logs' / 'devzero.log'))
(TD / 'outside.txt').write_text('outside', encoding='utf-8')
os.symlink(str(TD / 'outside.txt'), str(lf / 'logs' / 'linkout.log'))
os.symlink(str(lf / 'logs' / 'nowhere'), str(lf / 'logs' / 'dangling.log'))
os.symlink(str(lf / 'logs' / 'loop2.log'), str(lf / 'logs' / 'loop1.log'))
os.symlink(str(lf / 'logs' / 'loop1.log'), str(lf / 'logs' / 'loop2.log'))
sk = socket.socket(socket.AF_UNIX)
try:
    sk.bind(str(lf / 'logs' / 'sock.log'))
except OSError:
    pass
names = ['reg', 'empty', 'dir', 'devnull', 'devzero', 'linkout', 'dangling', 'loop1', 'sock', 'absent', 'a' * 300, '١', 'L01_floor\n',
         '', None, 5, '.hidden', '-x', 'x/../reg']
lt = {}
for nm in names:
    key = repr(nm)[:40]
    try:
        r = RR.run_log_text(lf, nm)
        lt[key] = list(r) if isinstance(r, tuple) else [r]
    except Exception as e:  # noqa: BLE001
        lt[key] = [f'EXC {type(e).__name__}']
R['L_run_log_text'] = lt

# ── SU: stage_summary_read · read_summary (객체 아닌 JSON) ──
su = {}
for nm, body in (('list', b'[]'), ('zero', b'0'), ('false', b'false'), ('null', b'null'), ('str', b'"x"'), ('obj_nostatus', b'{}'),
                 ('obj_status_empty', b'{"status": ""}'), ('obj_status_int', b'{"status": 1}'), ('trunc', b'{"status": "STOP'),
                 ('bom', b'\xef\xbb\xbf{"status": "STOPPED"}'), ('nan', b'{"status": "STOPPED", "x": NaN}'),
                 ('dupkey', b'{"status": "STOPPED", "status": "CALIBRATED"}')):
    d = TD / 'su' / nm
    d.mkdir(parents=True)
    (d / 'ladder_summary.json').write_bytes(body)
    rs = RR.read_summary(d, 'ladder_summary.json')
    row = {'read_summary_value': repr(rs[0])[:60]}
    if NEW:
        v, st = RR.stage_summary_read(d)
        row['stage_summary_read'] = [repr(v)[:60], st]
    su[nm] = row
R['SU_read'] = su


# ── V: 판정 입력 단계 요약 개수 검사 (_verdict_compute 입구) — 예측 요약 (이 사슬 꼴) + 사다리 요약 = 객체 아닌 JSON ──
def vrow(tag, ladder_body):
    d = TD / 'v' / tag
    d.mkdir(parents=True)
    (d / 'predict_summary.json').write_text(json.dumps({'tool': RR.TOOL, 'schema': RR.SCHEMA, 'stage': 'predict', 'status': 'PREDICTED'}),
                                             encoding='utf-8')
    if ladder_body is not None:
        (d / 'ladder_summary.json').write_bytes(ladder_body)
    try:
        RR._verdict_compute([str(d)], str(TD / 'no_such_reg.md'), None, str(TD), object())
        return 'NO_EXCEPTION'
    except RR.Stop as e:
        return f'Stop {e.code}: {e.cause[:80]}'
    except Exception as e:  # noqa: BLE001
        return f'{type(e).__name__}: {str(e)[:80]}'


R['V0_predict_only'] = vrow('V0', None)
R['V1_extra_ladder_list'] = vrow('V1', b'[]')
R['V2_extra_ladder_zero'] = vrow('V2', b'0')
R['V3_extra_ladder_trunc'] = vrow('V3', b'{"status": "STOP')
R['V4_extra_ladder_true'] = vrow('V4', b'true')

# ── W: write_summary 바이트 = write_json ──
if NEW:
    s = {'status': 'STOPPED', 'x': [1, 2.5, float('inf'), float('nan')], 'u': '한글 ü', 'n': {'b': None, 'a': True}}
    p1, p2 = TD / 'w1.json', TD / 'w2.json'
    RR.write_json(p1, s)
    RR.write_summary(p2, s)
    left = sorted(x.name for x in TD.iterdir() if '.tmp.' in x.name)
    R['W_bytes_equal'] = {'equal': p1.read_bytes() == p2.read_bytes(), 'sha': hashlib.sha256(p2.read_bytes()).hexdigest()[:16], 'tmp_left': left}

out['td'] = str(TD)
Path(OUT).write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, sort_keys=True)[:6000])
