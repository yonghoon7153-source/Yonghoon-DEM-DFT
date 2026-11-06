"""Pre-attack 11 own mutations (scratch copy only) — weaken / break each new guard, run selected checks, restore bytes.

usage: python3 -I mutate_pa11.py <copy tree> <out.json> [names]
"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

MT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
SEL = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
RRF = 'scripts/rint_r_chain.py'
ONLY = 'CT,RN,RC0,PE03,PD13,PD02,LG,FF,CE,SU,AL19,RS02'

M = [
    # legit-shape removal (would be false fail-closed) — tests must catch
    ('X1', 'GU table drops exit_ok', "'GROUP_UNCONFIRMED': frozenset({'killed:timeout', 'killed:signal', 'killed:signal_after', 'exit_ok', 'exit_fail'})}",
     "'GROUP_UNCONFIRMED': frozenset({'killed:timeout', 'killed:signal', 'killed:signal_after', 'exit_fail'})}"),
    ('X2', 'TL table drops killed:timeout', "STOP_RUN_SHAPES = {'TIME_LIMIT': frozenset({'none', 'killed:timeout'}),",
     "STOP_RUN_SHAPES = {'TIME_LIMIT': frozenset({'none'}),"),
    ('X3', 'RUNNER_RC table drops killed:signal_after', "'RUNNER_RC': frozenset({'killed:signal', 'killed:signal_after', 'exit_fail'}),",
     "'RUNNER_RC': frozenset({'killed:signal', 'exit_fail'}),"),
    ('X4', 'TL table drops none (pre-run gate)', "STOP_RUN_SHAPES = {'TIME_LIMIT': frozenset({'none', 'killed:timeout'}),",
     "STOP_RUN_SHAPES = {'TIME_LIMIT': frozenset({'killed:timeout'}),"),
    ('X4b', 'RUNNER_RC table drops killed:signal', "'RUNNER_RC': frozenset({'killed:signal', 'killed:signal_after', 'exit_fail'}),",
     "'RUNNER_RC': frozenset({'killed:signal_after', 'exit_fail'}),"),
    ('X4c', 'GU table drops killed:timeout', "'GROUP_UNCONFIRMED': frozenset({'killed:timeout', 'killed:signal', 'killed:signal_after', 'exit_ok', 'exit_fail'})}",
     "'GROUP_UNCONFIRMED': frozenset({'killed:signal', 'killed:signal_after', 'exit_ok', 'exit_fail'})}"),
    # weaken new guards
    ('X5', 'TL none: drop RUN_DIR_RE name check',
     "    if shape == 'none' and (not (isinstance(run, str) and RUN_DIR_RE.fullmatch(run)) or run_traces(folder, run)):",
     "    if shape == 'none' and run_traces(folder, run):"),
    ('X6', 'run_traces: unreadable folder = no traces', "    except OSError:\n        return True\n    return any(nm == run",
     "    except OSError:\n        return False\n    return any(nm == run"),
    ('X8', 'orphan by chain (cause, rc) check only when cause None', "        if by == 'chain' and not end_record_known(er):",
     "        if by == 'chain' and gc is None and not end_record_known(er):"),
    ('X10', 'rejected_record json.loads (dup key / NaN accepted)', '        rec = _json_strict(raw)\n    except Exception as e:                                    # noqa: BLE001 — 못 읽음 = 대조 실패 (RecursionError 포함)',
     '        rec = json.loads(raw)\n    except Exception as e:                                    # noqa: BLE001 — 못 읽음 = 대조 실패 (RecursionError 포함)'),
    ('X12', 'run_record_shape: falsy group_cause = None', "    if gc is None:\n        return {'ok': 'exit_ok', 'fail': 'exit_fail'}.get(k, 'bad')",
     "    if not gc:\n        return {'ok': 'exit_ok', 'fail': 'exit_fail'}.get(k, 'bad')"),
    ('X13', 'killed cause + rc 0 accepted', "    if type(gc) is str and gc in RUN_KILLED_CAUSES and k == 'none':",
     "    if type(gc) is str and gc in RUN_KILLED_CAUSES and k in ('none', 'ok'):"),
    ('X16', 'record table only for GU (old PB-01 scope)', '    return stop_record_problem(s, folder) is None\n',
     "    return stop_record_problem(s, folder) is None if ((s.get('stop') or {}).get('code') or s.get('status')) == 'GROUP_UNCONFIRMED' else True\n"),
    ('X17', 'end_record_known accepts bool rc', "    return k in ('ok', 'fail') or (k == 'none' and er.get('cause') is not None)",
     "    return k in ('ok', 'fail') or type(er.get('rc')) is bool or (k == 'none' and er.get('cause') is not None)"),
]


def sha(f):
    return hashlib.sha256((MT / f).read_bytes()).hexdigest()


def run(only):
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', 'scripts/test_rint_r_chain.py', '--only', only], cwd=str(MT), capture_output=True, text=True, env=env,
                       timeout=3600)
    return p.returncode, p.stdout + p.stderr, time.time() - t0


start = sha(RRF)
res = {}
rc, out, dt = run(ONLY)
res['BASE'] = {'rc': rc, 'summary': (re.findall(r'test_rint_r_chain: .*', out) or [''])[-1], 'seconds': round(dt, 1)}
print('BASE', res['BASE'], flush=True)
for mid, item, old, new in M:
    if SEL is not None and mid not in SEL:
        continue
    txt = (MT / RRF).read_bytes().decode('utf-8')
    if txt.count(old) != 1:
        res[mid] = {'item': item, 'status': 'SKIP', 'why': f'count {txt.count(old)}'}
        print(mid, 'SKIP', txt.count(old), flush=True)
        continue
    try:
        (MT / RRF).write_bytes(txt.replace(old, new).encode('utf-8'))
        rc, out, dt = run(ONLY)
    finally:
        (MT / RRF).write_bytes(txt.encode('utf-8'))
    failed = sorted(set(re.findall(r'^  FAIL  (\S+)', out, re.M)))
    res[mid] = {'item': item, 'status': 'KILLED' if rc != 0 else 'SURVIVED', 'failed': failed, 'seconds': round(dt, 1)}
    print(mid, item, res[mid]['status'], failed, f'{dt:.1f}s', flush=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
res['_restored'] = sha(RRF) == start
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('restored', res['_restored'])
