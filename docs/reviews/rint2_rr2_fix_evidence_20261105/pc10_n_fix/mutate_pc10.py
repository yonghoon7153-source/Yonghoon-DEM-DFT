"""Rint ② PC10-08 · 09 · 10 고침 (11-06 · N1 · N2 · N4 · 같은 부류) 변이 — 고친 트리 사본 (git 없는 사본 · 리포 밖) 에서 한 번에 변이 하나 · 새 가드를 끄거나
약하게 하면 새 시험 (그리고 기대값을 고친 기존 시험) 이 옳은 까닭으로 실패하는지 (잡힘 = 시험 rc ≠ 0 + 기대한 검사 이름이 FAIL) 본다 · 매번 원 바이트로
되돌린다 · 끝나면 사본 코드 · 시험 sha256 = 시작 때와 같음을 확인한다 (`preattack10_fix/mutate_pa10fix.py` 꼴 그대로).

  python3 -I mutate_pc10.py <사본 트리> <출력.json> [변이 이름 쉼표]
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

MT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
SEL = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
RRF = 'scripts/rint_r_chain.py'
TST = 'scripts/test_rint_r_chain.py'
ONLY = 'CT,RN,RC0,PE03,PD13,PD02,LG,FF'

# (이름, 고침 항목, [(파일, 옛 글, 새 글) …], 잡아야 할 검사 (하나 이상 FAIL))
M = [
    # ── PC10-08 · 09 요약 있는 길 — 멈춤 코드 ↔ 멈춘 런 기록 꼴 (생산자 표) ──
    ('G1', 'N1·N2 표 통째로', [(RRF, '    return stop_record_problem(s, folder) is None', '    return True')], ['CT01', 'CT04', 'LG01', 'PD02', 'PD13', 'RN01']),
    ('G2', 'N1 TIME_LIMIT 표에 exit_fail', [(RRF, "STOP_RUN_SHAPES = {'TIME_LIMIT': frozenset({'none', 'killed:timeout'}),",
                                           "STOP_RUN_SHAPES = {'TIME_LIMIT': frozenset({'none', 'killed:timeout', 'exit_fail'}),")], ['CT01', 'CT04']),
    ('G3', 'N2 RUNNER_RC 표에 killed:timeout', [(RRF, "                   'RUNNER_RC': frozenset({'killed:signal', 'killed:signal_after', 'exit_fail'}),",
                                                "                   'RUNNER_RC': frozenset({'killed:signal', 'killed:signal_after', 'exit_fail', 'killed:timeout'}),")],
     ['CT01', 'LG01', 'PD02']),
    ('G4', 'N2 사슬이 죽인 원인 + rc 있음 허용', [(RRF, "    if type(gc) is str and gc in RUN_KILLED_CAUSES and k == 'none':",
                                              "    if type(gc) is str and gc in RUN_KILLED_CAUSES:")], ['CT01', 'CT04']),
    ('G5', 'group_cause None + rc null 허용', [(RRF, "        return {'ok': 'exit_ok', 'fail': 'exit_fail'}.get(k, 'bad')",
                                            "        return {'ok': 'exit_ok', 'fail': 'exit_fail', 'none': 'exit_fail'}.get(k, 'bad')")], ['CT01', 'PD13', 'RN01']),
    ('G6', 'group_cause None + 꼴 틀린 rc 허용', [(RRF, "        return {'ok': 'exit_ok', 'fail': 'exit_fail'}.get(k, 'bad')",
                                              "        return {'ok': 'exit_ok', 'fail': 'exit_fail', 'bad': 'exit_fail'}.get(k, 'bad')")], ['CT01', 'PD13', 'RN01']),
    ('G7', '런 기록 없는 TIME_LIMIT 흔적 판독 뺌', [(RRF, "    if shape == 'none' and (not (isinstance(run, str) and RUN_DIR_RE.fullmatch(run)) or run_traces(folder, run)):",
                                                "    if shape == 'none' and not (isinstance(run, str) and RUN_DIR_RE.fullmatch(run)):")], ['CT01', 'LG01']),
    ('G8', 'N1 원인 (TIME_LIMIT 러너 rc 길) 뺌', [(RRF, "        if run_exit_failed(rr if isinstance(rr, dict) else {}):\n            return words_cause(txt, 'runner_rc')\n", '')],
     ['CT01', 'CT04']),
    ('G9', 'group_cause 칸 없음 = None', [(RRF, "    if not isinstance(rr, dict) or 'group_cause' not in rr:\n        return 'bad'\n    gc, k = rr['group_cause'], rc_kind(rr.get('rc'))",
                                         "    if not isinstance(rr, dict):\n        return 'bad'\n    gc, k = rr.get('group_cause'), rc_kind(rr.get('rc'))")],
     ['CT01', 'RN01', 'RN02']),
    ('G10', 'result_fields 가 표를 안 봄', [(RRF, '            readable = stop_log_readable(s, folder, lst) and stop_record_readable(s, folder)',
                                          '            readable = stop_log_readable(s, folder, lst)')], ['CT01', 'CT04', 'LG01', 'PD02', 'PD13', 'RN01']),
    ('G11', 'run_exit_failed = 늘 False', [(RRF, "    return 'group_cause' in rec and rec['group_cause'] is None and not rc_success(rec.get('rc'))", '    return False')],
     ['CT01', 'CT04', 'PD13', 'RN01', 'RC04']),
    # ── PC10 같은 부류 — 요약 없는 길 끝 기록 (원인, rc) ──
    ('H1', 'by chain (원인, rc) 판독 뺌', [(RRF, "        if by == 'chain' and not end_record_known(er):", '        if False:')], ['CT02', 'RN01', 'RC02']),
    ('H2', 'chain_end (원인, rc) 판독 뺌', [(RRF, "chain_cause_known(ce.get('cause')) and end_record_known(ce)):", "chain_cause_known(ce.get('cause'))):")],
     ['CT02', 'RN01', 'PE03u']),
    ('H3', '원인 None + rc null 허용', [(RRF, "    return k in ('ok', 'fail') or (k == 'none' and er.get('cause') is not None)", "    return k in ('ok', 'fail', 'none')")],
     ['CT02', 'RN01', 'RC02', 'PE03u']),
    ('H4', '꼴 틀린 rc 허용', [(RRF, "    return k in ('ok', 'fail') or (k == 'none' and er.get('cause') is not None)",
                              "    return k != 'none' or er.get('cause') is not None")], ['CT02', 'RN01', 'RC02']),
    # ── PC10-10 (N4) 거부 기록 읽기 한 함수 ──
    ('J1', '객체 검사 뺌', [(RRF, "    if not isinstance(rec, dict):\n        raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{label}: 거부 기록 꼴')\n    return rec",
                           '    return rec')], ['CT03', 'CT04']),
    ('J2', '예외 = ValueError 만 (RecursionError 샘)', [(RRF, '    except Exception as e:                                    # noqa: BLE001 — 못 읽음 = 대조 실패 (RecursionError 포함)',
                                                     '    except ValueError as e:                                   # noqa: BLE001 — 못 읽음 = 대조 실패 (RecursionError 포함)')],
     ['CT03']),
    ('J3', 'recover 옛 읽기로', [(RRF, '                rec = rejected_record(rj, f.name)', '                rec = _json_strict(read_regular_file(rj)[0])')],
     ['CT03', 'CT04']),
    # ── 지난 회차 변이 (`preattack10_fix/mutate_pa10fix.py`) 중 글자가 옮겨져 건너뛴 열 (B2–B5 · B8 · D3 · D4 · E9 · F3 · F4) 의 새 자리 짝 — B2 ≈ G11 · B3 ≈ G1 ·
    #    B4 ≈ G9 · D4 ≈ J3 는 위에 있다 · 나머지 여섯 ──
    #  K1 = 동등 변이 (살아남는 것이 맞다): run_record_shape 이 모르는 글을 'killed:<글>' 로 내도 STOP_RUN_SHAPES 어느 집합에도 없어 같은 읽음 False — 같은
    #    가드가 두 겹 (꼴 이름 · 허용 집합).  B5 의 뜻 (모르는 글 group_cause = 자격) 의 짝 = K1b (허용 집합 대조를 약하게)
    ('K1', 'B5 짝 — 모르는 글 group_cause 를 죽인 원인으로 (동등 변이)', [(RRF, "    if type(gc) is str and gc in RUN_KILLED_CAUSES and k == 'none':",
                                                                "    if isinstance(gc, str) and k == 'none':")], ['CT01', 'RN01', 'RN02']),
    ('K1b', 'B5 짝 — 허용 집합이 모든 killed:<글> 을 받음', [(RRF, '    if shape not in allowed:\n',
                                                      "    if shape not in allowed and not shape.startswith('killed:'):\n")], ['CT01', 'RN01', 'RN02']),
    #  K1b 만으로는 모르는 글이 여전히 run_record_shape 의 'bad' 로 막힌다 (잡힌 까닭 = RUNNER_RC + timeout · TIME_LIMIT + signal 이 열림) → 두 겹을 함께 걷은 K1c
    ('K1c', 'B5 짝 — 두 겹 함께 (모르는 글 group_cause = 자격)', [(RRF, "    if type(gc) is str and gc in RUN_KILLED_CAUSES and k == 'none':",
                                                          "    if isinstance(gc, str) and k == 'none':"),
                                                         (RRF, '    if shape not in allowed:\n',
                                                          "    if shape not in allowed and not shape.startswith('killed:'):\n")], ['CT01', 'RN01', 'RN02']),
    ('K2', 'D3 짝 — 거부 기록 읽기 = read_bytes (FIFO 막힘)', [(RRF, '    raw, rst = read_regular_file(rj)                          # ★ 11-06 PB-03',
                                                        "    raw, rst = Path(rj).read_bytes(), 'ok'                     # ★ 11-06 PB-03")], ['FF01']),
    ('K3', 'F3 짝 — 런 폴더 흔적 = 늘 없음', [(RRF, "    return any(nm == run or nm.startswith(run + '_arm') for nm in names)", '    return False')], ['LG01']),
    ('K4', 'F4 짝 — 런 폴더 흔적 = 이름만 (_arm 꼴 놓침)', [(RRF, "    return any(nm == run or nm.startswith(run + '_arm') for nm in names)",
                                                     '    return any(nm == run for nm in names)')], ['LG01']),
    ('K5', 'E9 짝 — rc 읽기에 기본값 (RC01 허용 문맥 밖)', [(RRF, "        if runner_rc_failed(rec.get('rc')) or run_exit_failed(rec):",
                                                      "        if runner_rc_failed(rec.get('rc', 0)) or run_exit_failed(rec):")], ['RC01']),
    ('K6', 'B8 짝 — group_cause 칸 없음을 None 으로 (run_exit_failed)', [(RRF, "    return 'group_cause' in rec and rec['group_cause'] is None and not rc_success(rec.get('rc'))",
                                                                  "    return rec.get('group_cause') is None and not rc_success(rec.get('rc'))")],
     ['CT01', 'RN01', 'RN02']),
]


def sha(f):
    return hashlib.sha256((MT / f).read_bytes()).hexdigest()


def run(only):
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', TST, '--only', only], cwd=str(MT), capture_output=True, text=True, env=env, timeout=3600)
    return p.returncode, p.stdout + p.stderr, time.time() - t0


start = {f: sha(f) for f in (RRF, TST)}
res = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}
for mid in ['BASE'] + [m[0] for m in M]:
    if SEL is not None and mid not in SEL:
        continue
    if mid == 'BASE':
        rc, out, dt = run(ONLY)
        res['BASE'] = {'rc': rc, 'only': ONLY, 'summary': (re.findall(r'test_rint_r_chain: .*', out) or [''])[-1], 'seconds': round(dt, 1), 'clean': rc == 0}
        print(f"BASE {'clean' if rc == 0 else 'NOT CLEAN'} {res['BASE']['summary']}", flush=True)
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
        continue
    _mid, item, reps, catch = [m for m in M if m[0] == mid][0]
    orig, bad = {}, None
    for f, old, _new in reps:
        txt = orig.get(f) or (MT / f).read_bytes().decode('utf-8')
        orig.setdefault(f, txt)
        if txt.count(old) != 1:
            bad = f'옛 글이 {txt.count(old)} 번 ({f})'
    if bad:
        res[mid] = {'item': item, 'status': 'SKIP', 'why': bad}
        print(f'{mid} SKIP {bad}', flush=True)
        continue
    cur = dict(orig)
    for f, old, new in reps:
        cur[f] = cur[f].replace(old, new)
    try:
        for f, t in cur.items():
            (MT / f).write_bytes(t.encode('utf-8'))
        rc, out, dt = run(ONLY)
    finally:
        for f, t in orig.items():
            (MT / f).write_bytes(t.encode('utf-8'))
    failed = sorted(set(re.findall(r'^  FAIL  (\S+)', out, re.M)))
    hit = [c for c in catch if c in failed]
    status = 'KILLED' if rc != 0 and hit else ('KILLED_OTHER' if rc != 0 else 'SURVIVED')
    res[mid] = {'item': item, 'status': status, 'rc': rc, 'only': ONLY, 'failed': failed, 'expected_any': catch, 'expected_hit': hit,
                'summary': (re.findall(r'test_rint_r_chain: .*', out) or [''])[-1][:300], 'seconds': round(dt, 1)}
    print(f'{mid} {item} {status} rc={rc} failed={failed} ({dt:.1f} s)', flush=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
end = {f: sha(f) for f in (RRF, TST)}
res['_tree'] = {'start_sha256': start, 'end_sha256': end, 'restored': start == end}
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
st = [v.get('status') for k, v in res.items() if not k.startswith('_') and k != 'BASE']
print(f"변이 {len(st)} · 잡힘 {st.count('KILLED')} · 다른 검사로 잡힘 {st.count('KILLED_OTHER')} · 생존 {st.count('SURVIVED')} · 건너뜀 {st.count('SKIP')} · "
      f"사본 되돌림 {res['_tree']['restored']}")
