"""Rint ② 사전 공격 10 회차 고침 (11-06 · PB-01 · 02 · 03 · 04 · 06) 변이 — 고친 트리 사본 (git 없는 사본 · 리포 밖) 에서 한 번에 변이 하나 · 그 가드를 끄거나
옛 꼴로 되돌리면 새 시험이 옳은 까닭으로 실패하는지 (잡힘 = 시험 rc ≠ 0 + 기대한 검사 이름이 FAIL) 본다 · 매번 원 바이트로 되돌린다 · 끝나면 사본 코드 ·
시험 sha256 = 시작 때와 같음을 확인한다 (`docs/reviews/rint2_rr2_fix_evidence_20261105/mutate_rr2fix.py` 꼴 그대로).

  python3 -I mutate_pa10fix.py <사본 트리> <출력.json> [변이 이름 쉼표]
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
P01 = 'RN,RC04,PE03u,PD13,LG01'

# (이름, 고침 항목, [(파일, 옛 글, 새 글) …], --only 접두, 잡아야 할 검사 (하나 이상 FAIL))
M = [
    # ── PB-01 rc null 한 읽기 ──
    ('B1', 'PB-01', [(RRF, "return isinstance(ce, dict) and ce.get('cause') is None and not rc_success(ce.get('rc'))",
                      "return isinstance(ce, dict) and ce.get('cause') is None and runner_rc_failed(ce.get('rc'))")], P01,
     ['RN01', 'RN02', 'RC04', 'PE03u', 'PD13o']),
    ('B2', 'PB-01', [(RRF, "        if runner_rc_failed(rc) or ('group_cause' in rec and rec['group_cause'] is None and not rc_success(rc)):",
                      "        if runner_rc_failed(rc):")], P01, ['RN01', 'RN02', 'RC04', 'PD13']),
    ('B3', 'PB-01', [(RRF, "    if not isinstance(rr, dict) or 'group_cause' not in rr:\n        return False\n    gc = rr['group_cause']\n"
                           "    return gc is None or (type(gc) is str and gc in RUN_KILLED_CAUSES)", "    return True")], P01, ['RN01', 'RN02', 'LG01']),
    ('B4', 'PB-01', [(RRF, "    if not isinstance(rr, dict) or 'group_cause' not in rr:\n        return False\n    gc = rr['group_cause']\n",
                      "    if not isinstance(rr, dict):\n        return False\n    gc = rr.get('group_cause')\n")], P01, ['RN01', 'RN02']),
    ('B5', 'PB-01', [(RRF, "    return gc is None or (type(gc) is str and gc in RUN_KILLED_CAUSES)", "    return gc is None or isinstance(gc, str)")], P01,
     ['RN01', 'RN02']),
    ('B6', 'PB-01', [(RRF, "            readable = stop_log_readable(s, folder, lst) and stop_record_readable(s, folder)",
                      "            readable = stop_log_readable(s, folder, lst)")], P01, ['RN01', 'RN02', 'LG01']),
    ('B7', 'PB-01', [(RRF, "RUN_KILLED_CAUSES = ('timeout', 'signal', 'signal_after')", "RUN_KILLED_CAUSES = ('timeout', 'signal')")], P01, ['RN01']),
    ('B8', 'PB-01', [(RRF, "('group_cause' in rec and rec['group_cause'] is None and not rc_success(rc))",
                      "(rec.get('group_cause') is None and not rc_success(rc))")], P01, ['RN01', 'RN02']),
    # ── PB-02 판정 입력 · 합치기 남은 런 목록 ──
    ('C1', 'PB-02', [(RRF, "        if unread:\n", "        if False:\n")], 'SU03,SU04', ['SU03']),
    ('C2', 'PB-02', [(RRF, "                if sst == 'unreadable' or (sst == 'ok' and not isinstance(su.get('status'), str)):",
                      "                if False:")], 'SU03,SU04', ['SU04']),
    ('C3', 'PB-02', [(RRF, "                if sst == 'unreadable' or (sst == 'ok' and not isinstance(su.get('status'), str)):",
                      "                if sst == 'unreadable':")], 'SU03,SU04', ['SU04']),
    # ── PB-03 FIFO 에 막히지 않는 읽기 ──
    ('D1', 'PB-03', [(RRF, "    raw, st = read_regular_file(p)\n    if st != 'ok':\n        return None\n    try:\n        v = json.loads(raw.decode('utf-8'))\n"
                           "    except (UnicodeDecodeError, ValueError, RecursionError):\n        return None\n    return v if isinstance(v, dict) else None",
                      "    try:\n        v = json.loads(Path(p).read_text(encoding='utf-8'))\n    except (OSError, UnicodeDecodeError, ValueError, RecursionError):\n"
                      "        return None\n    return v if isinstance(v, dict) else None")], 'FF01', ['FF01']),
    ('D2', 'PB-03', [(RRF, "        raw, st = (None, 'link') if p.is_symlink() else read_regular_file(p)\n        a = _json_strict(raw) if st == 'ok' else None",
                      "        a = _json_strict(p.read_bytes()) if not p.is_symlink() else None")], 'FF01', ['FF01']),
    ('D3', 'PB-03', [(RRF, "        raw, rst = read_regular_file(rj)                      # ★ 11-06 PB-03",
                      "        raw, rst = rj.read_bytes(), 'ok'                      # ★ 11-06 PB-03")], 'FF01', ['FF01']),
    ('D4', 'PB-03', [(RRF, "                raw_rj, rst = read_regular_file(rj)             # ★ 11-06 PB-03",
                      "                raw_rj, rst = rj.read_bytes(), 'ok'             # ★ 11-06 PB-03")], 'FF01', ['FF01']),
    # ── PB-04 RC01 스캐너 (시험 쪽 가드 끄기 · 원천에 반례 꼴 넣기) ──
    ('E1', 'PB-04', [(TST, "            elif isinstance(node, ast.Attribute) and node.attr == 'rc':\n                hits = [('bad', 'attribute')]",
                      "            elif isinstance(node, ast.Attribute) and node.attr == 'rc':\n                hits = []")], 'RC01', ['RC01']),
    ('E2', 'PB-04', [(TST, "                elif RC_QUOTED.search(v):\n                    hits = [('bad', 'json_text')]",
                      "                elif RC_QUOTED.search(v):\n                    hits = []")], 'RC01', ['RC01']),
    ('E3', 'PB-04', [(TST, "                return [('ok', 'record_value') if k is not None and is_rc_const(k) else ('bad', 'launder_dict_value')]",
                      "                return [('ok', 'record_value')]")], 'RC01', ['RC01']),
    ('E4', 'PB-04', [(TST, "        return any(n.id in table.get(f, ()) for f in fchain.get(n, ()) + (None,))",
                      "        return any(n.id in table.get(f, ()) for f in fchain.get(n, ())[-1:] + (None,))")], 'RC01', ['RC01']),
    ('E5', 'PB-04', [(TST, "            return [('bad', 'message_use')]", "            return [('ok', 'message')]")], 'RC01', ['RC01']),
    ('E6', 'PB-04', [(TST, "        return [('bad', 'const')]", "        return []")], 'RC01', ['RC01']),
    ('E7', 'PB-04', [(TST, "p.func.attr == 'get' and len(p.args) == 1 and p.args[0] is n", "p.func.attr == 'get' and bool(p.args) and p.args[0] is n")],
     'RC01', ['RC01']),
    ('E8', 'PB-04', [(RRF, "return bound and rc_success(er.get('rc')) and (self.src / outdir_name).is_dir()",
                      "return bound and dict.get(er, 'rc') == 0 and (self.src / outdir_name).is_dir()")], 'RC01', ['RC01']),
    ('E9', 'PB-04', [(RRF, "        rc = rec.get('rc')\n", "        rc = rec.get('rc', 0)\n")], 'RC01', ['RC01']),
    # ── PB-06 런 전 TIME_LIMIT 예외 = 그 런 흔적 없음 ──
    ('F1', 'PB-06', [(RRF, "(base / GROUPS_DIR / f'{run}.launch.json', base / GROUPS_DIR / f'{run}.end.json',",
                      "(base / GROUPS_DIR / f'{run}.launch.json',")], 'LG01', ['LG01']),
    ('F2', 'PB-06', [(RRF, "                                            base / 'logs' / f'{run}.log')):", "                                            )):")],
     'LG01', ['LG01']),
    ('F3', 'PB-06', [(RRF, "    return not any(nm == run or nm.startswith(run + '_arm') for nm in names)", "    return True")], 'LG01', ['LG01']),
    ('F4', 'PB-06', [(RRF, "    return not any(nm == run or nm.startswith(run + '_arm') for nm in names)", "    return not any(nm == run for nm in names)")],
     'LG01', ['LG01']),
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
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
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
