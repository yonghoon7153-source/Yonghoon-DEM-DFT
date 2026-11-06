"""Rint ② 회차 ② 고침 (11-05 · RR2-01 · A1b · PC6-05 · A2b) 변이 — 고친 트리 사본 (git 없는 사본 · 리포 밖) 에서 한 번에 변이 하나 · 그 가드를 끄거나 옛 꼴로
되돌리면 새 시험이 옳은 까닭으로 실패하는지 (잡힘 = 시험 rc ≠ 0 + 기대한 검사 이름이 FAIL) 본다 · 매번 원 바이트로 되돌린다 · 끝나면 사본 코드 · 시험 sha256
= 시작 때와 같음을 확인한다.

  python3 -I mutate_rr2fix.py <사본 트리> <출력.json> [변이 이름 쉼표]
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

# (이름, 고침 항목, [(파일, 옛 글, 새 글) …], --only 접두, 잡아야 할 검사 (하나 이상 FAIL))
M = [
    # ── A1 RR2-01 rc 판독 한 함수 ──
    ('K1', 'A1', [(RRF, "    if type(rc) is int:\n        return 'ok' if rc == 0 else 'fail'",
                   "    if isinstance(rc, int):\n        return 'ok' if rc == 0 else 'fail'")], 'RC', ['RC02', 'RC05']),
    ('K2', 'A1', [(RRF, "    if rc is None:\n        return 'none'\n    if type(rc) is int:",
                   "    if rc is None:\n        return 'none'\n    if isinstance(rc, float) and rc == 0:\n        return 'ok'\n    if type(rc) is int:")],
     'RC', ['RC02', 'RC05']),
    ('K3', 'A1', [(RRF, "        if by == 'chain' and gc is None and rc_success(rc):", "        if by == 'chain' and gc is None and rc == 0:")],
     'RC', ['RC01', 'RC02']),
    ('K4', 'A1', [(RRF, "if want != got or not rc_success(r.get('rc')) or", "if want != got or r.get('rc') != 0 or")], 'RC', ['RC01', 'RC03']),
    ('K5', 'A1', [(RRF, "and rc_success(x.get('rc')) and runs[-1]", "and x.get('rc') == 0 and runs[-1]")], 'RC', ['RC01', 'RC03']),
    ('K6', 'A1', [(RRF, "        if not rc_success(rec0.get('rc')):", "        if rec0.get('rc') != 0:")], 'RC', ['RC01', 'RC03']),
    ('K7', 'A1', [(RRF, "        if not rc_success(rc):                                # ★ 11-05 RR2-01 — 판독 한 함수 (생산 값",
                   "        if rc != 0:                                # ★ 11-05 RR2-01 — 판독 한 함수 (생산 값")], 'RC', ['RC01', 'RC04']),
    ('K8', 'A1', [(RRF, "        if not rc_success(rc):                                # ★ 11-05 RR2-01 — 판독 한 함수\n",
                   "        if rc != 0:\n")], 'RC', ['RC01', 'RC04']),
    ('K9', 'A1', [(RRF, "return bound and rc_success(er.get('rc')) and", "return bound and er.get('rc') == 0 and")], 'RC,PE06', ['RC01', 'RC04', 'PE06']),
    ('K10', 'A1', [(RRF, "        if not rc_success(r.get('rc')):                    # ★ 11-05 RR2-01 — 그 런 기록의 rc 도",
                    "        if False:                    # ★ 11-05 RR2-01 — 그 런 기록의 rc 도")], 'RC', ['RC01', 'RC03']),
    ('K11', 'A1', [(RRF, "    return rc_kind(rc) in ('fail', 'bad')", "    return rc is not None and rc != 0")], 'RC', ['RC01', 'RC05']),
    # ── A1b 끝 기록 사슬 원인 칸 한 읽기 ──
    ('E1', 'A1b', [(RRF, "            if 'chain_end' in er and not (isinstance(ce, dict) and chain_cause_known(ce.get('cause'))):", "            if False:")],
     'CE,PE03u', ['CE01', 'CE02', 'PE03u']),
    ('E2', 'A1b', [(RRF, "            if 'chain_end' in er and not (isinstance(ce, dict) and chain_cause_known(ce.get('cause'))):",
                    "            if isinstance(ce, dict) and not chain_cause_known(ce.get('cause')):")], 'CE', ['CE01']),
    ('E3', 'A1b', [(RRF, "CHAIN_END_CAUSES = (None, 'timeout', 'signal', 'signal_after', 'exception')",
                    "CHAIN_END_CAUSES = (None, 'timeout', 'signal', 'exception')")], 'CE,PD02,PE03u', ['CE01', 'PD02', 'PE03u']),
    ('E4', 'A1b', [(RRF, "    return gc is None or (type(gc) is str and gc in CHAIN_END_CAUSES)", "    return gc is None or isinstance(gc, str)")],
     'CE', ['CE01']),
    ('E5', 'A1b', [(RRF, "        elif not chain_cause_known(gc):\n            c, ok = 'parent_dead', False",
                    "        elif False:\n            c, ok = 'parent_dead', False")], 'CE', ['CE01']),
    # ── A2 PC6-05 런 로그 (글, 상태) ──
    ('G1', 'A2', [(RRF, "        if not stat.S_ISREG(os.fstat(fd).st_mode):", "        if False:")], 'LG', ['LG03']),
    ('G2', 'A2', [(RRF, "    except FileNotFoundError:\n        return None, 'missing'\n    except OSError:\n        return None, 'unreadable'",
                   "    except FileNotFoundError:\n        return None, 'missing'\n    except OSError:\n        return None, 'missing'")], 'LG', ['LG01']),
    ('G2b', 'A2', [(RRF, "        return b''.join(chunks), 'ok'\n    except OSError:\n        return None, 'unreadable'",
                    "        return b''.join(chunks), 'ok'\n    except OSError:\n        return None, 'missing'")], 'LG', ['LG03']),
    ('G3', 'A2', [(RRF, "return rr is None and not os.path.lexists(str(Path(folder) / GROUPS_DIR / f'{sr.get(\"run\")}.launch.json'))",
                   "return rr is None and not (Path(folder) / GROUPS_DIR / f'{sr.get(\"run\")}.launch.json').is_file()")], 'LG', ['LG01']),
    ('G3b', 'A2', [(RRF, "return rr is None and not os.path.lexists(str(", "return rr is None and not os.path.exists(str(")], 'LG', ['LG01']),
    ('G4', 'A2', [(RRF, "os.O_RDONLY | os.O_NONBLOCK | getattr(os, 'O_NOCTTY', 0)", "os.O_RDONLY | getattr(os, 'O_NOCTTY', 0)")], 'LG,SU', ['LG03']),
    ('G5', 'A2', [(RRF, "            readable = stop_log_readable(s, folder, lst)", "            readable = True")], 'LG', ['LG01', 'LG02', 'LG03']),
    ('G6', 'A2', [(RRF, "return rr is None and not os.path.lexists(", "return not os.path.lexists(")], 'LG', ['LG01']),
    ('G7', 'A2', [(RRF, "    if state != 'missing' or (sr.get('code') or s.get('status')) != 'TIME_LIMIT':",
                   "    if (sr.get('code') or s.get('status')) != 'TIME_LIMIT':")], 'LG', ['LG01']),
    ('G8', 'A2', [(RRF, "    if not (isinstance(run, str) and RUN_DIR_RE.fullmatch(run)):", "    if not isinstance(run, str):")], 'LG', ['LG01']),
    ('G9', 'A2', [(RRF, "        if lst != 'ok':\n            ok = False", "        if False:\n            ok = False")], 'LG', ['LG01', 'LG03']),
    ('G10', 'A2', [(RRF, "    if state != 'missing' or (sr.get('code') or s.get('status')) != 'TIME_LIMIT':", "    if state != 'missing':")], 'LG', ['LG01']),
    # ── A2b 있는데 못 읽는 단계 요약 · 원자적 쓰기 ──
    ('H1', 'A2b', [(RRF, "    if not isinstance(v, dict):\n        return None, None, 'unreadable'", "    if False:\n        return None, None, 'unreadable'")],
     'SU', ['SU01']),
    ('H2', 'A2b', [(RRF, "        v = json.loads(raw.decode('utf-8'))\n    except (UnicodeDecodeError, ValueError, RecursionError):",
                    "        v = json.loads(raw.decode('utf-8'))\n    except (UnicodeDecodeError, ValueError):")], 'SU', ['SU01']),
    ('H3', 'A2b', [(RRF, "        if st == 'unreadable' or (st == 'ok' and not isinstance(v.get('status'), str)):",
                    "        if st == 'ok' and not isinstance(v.get('status'), str):")], 'SU', ['SU01']),
    ('H4', 'A2b', [(RRF, "        if st == 'unreadable' or (st == 'ok' and not isinstance(v.get('status'), str)):", "        if st == 'unreadable':")],
     'SU', ['SU01']),
    ('H5', 'A2b', [(RRF, "    if unreadable:\n        status, stop, cause, readable", "    if False:\n        status, stop, cause, readable")], 'SU', ['SU01']),
    ('H6', 'A2b', [(RRF, "res = attempt_result_line(n, f, s, 'recover', unreadable=(sst == 'unreadable'))", "res = attempt_result_line(n, f, s, 'recover')")],
     'SU', ['SU01']),
    ('H7', 'A2b', [(RRF, "    return result_fields(p, s, unreadable=(sst == 'unreadable'))", "    return result_fields(p, s)")], 'SU', ['SU01']),
    ('H8', 'A2b', [(RRF, "    write_summary(out / 'ladder_summary.json', s)", "    write_json(out / 'ladder_summary.json', s)")], 'SU', ['SU02']),
    ('H9', 'A2b', [(RRF, "    write_json_atomic(path, _clean(s))", "    write_json(path, s)")], 'SU', ['SU02']),
    ('H10', 'A2b', [(RRF, "    write_summary(out / sname, s)", "    write_json(out / sname, s)")], 'SU', ['SU02']),
    ('H11', 'A2b', [(RRF, "    write_summary(out / 'predict_summary.json', s)", "    write_json(out / 'predict_summary.json', s)")], 'SU', ['SU02']),
    ('H12', 'A2b', [(RRF, "        write_summary(out / MERGE_SUMMARY, s)", "        write_json(out / MERGE_SUMMARY, s)")], 'SU', ['SU02']),
]


def sha(f):
    return hashlib.sha256((MT / f).read_bytes()).hexdigest()


def run(only):
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    t0 = time.time()
    p = subprocess.run([sys.executable, '-B', TST, '--only', only], cwd=str(MT), capture_output=True, text=True, env=env, timeout=3600)
    out = p.stdout + p.stderr
    return p.returncode, out, time.time() - t0


start = {f: sha(f) for f in (RRF, TST)}
res = json.loads(OUT.read_text(encoding='utf-8')) if OUT.exists() else {}
names = ['BASE'] + [m[0] for m in M]
for mid in names:
    if SEL is not None and mid not in SEL:
        continue
    if mid == 'BASE':
        prefixes = sorted({m[3] for m in M})
        rows = []
        for pr in prefixes:
            rc, out, dt = run(pr)
            rows.append({'only': pr, 'rc': rc, 'summary': (re.findall(r'test_rint_r_chain: .*', out) or [''])[-1], 'seconds': round(dt, 1)})
        res['BASE'] = {'rows': rows, 'clean': all(r['rc'] == 0 for r in rows)}
        print(f"BASE {'clean' if res['BASE']['clean'] else 'NOT CLEAN'} {[r['summary'] for r in rows]}", flush=True)
        continue
    _mid, item, reps, only, catch = [m for m in M if m[0] == mid][0]
    orig = {}
    bad = None
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
        rc, out, dt = run(only)
    finally:
        for f, t in orig.items():
            (MT / f).write_bytes(t.encode('utf-8'))
    failed = sorted(set(re.findall(r'^  FAIL  (\S+)', out, re.M)))
    hit = [c for c in catch if c in failed]
    status = 'KILLED' if rc != 0 and hit else ('KILLED_OTHER' if rc != 0 else 'SURVIVED')
    res[mid] = {'item': item, 'status': status, 'rc': rc, 'only': only, 'failed': failed, 'expected_any': catch, 'expected_hit': hit,
                'summary': (re.findall(r'test_rint_r_chain: .*', out) or [''])[-1][:300], 'seconds': round(dt, 1)}
    print(f'{mid} {item} {status} rc={rc} failed={failed} ({dt:.1f} s)', flush=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
end = {f: sha(f) for f in (RRF, TST)}
res['_tree'] = {'start_sha256': start, 'end_sha256': end, 'restored': start == end}
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
st = [v.get('status') for k, v in res.items() if not k.startswith('_') and k != 'BASE']
print(f"변이 {len(st)} · 잡힘 {st.count('KILLED')} · 다른 검사로 잡힘 {st.count('KILLED_OTHER')} · 생존 {st.count('SURVIVED')} · 건너뜀 {st.count('SKIP')} · "
      f"사본 되돌림 {res['_tree']['restored']}")
