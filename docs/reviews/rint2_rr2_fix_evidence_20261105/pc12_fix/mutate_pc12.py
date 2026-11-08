"""변이 대조 — 새 가드를 하나씩 끄고 (사본 트리 · 한 번에 하나 · 매번 원 바이트로 되돌림) PC12A–E 가 어느 검사로 잡는지 본다.
python3 mutate_pc12.py <사본 scripts 폴더> <out.json>"""
import hashlib
import json
import pathlib
import subprocess
import sys

COPY = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
DUMP = pathlib.Path(__file__).with_name('dump_pc12.py')
chain = COPY / 'rint_r_chain.py'
orig = chain.read_bytes()
sha0 = hashlib.sha256(orig).hexdigest()

MUTANTS = [
    ('M1_range_off', 'F1 요청 칸 범위 (request_fields_problem)', 'PC12A',
     [("    if type(n) is not int or not (ARMS_RANGE[0] <= n <= ARMS_RANGE[1]):", "    if type(n) is not int:"),
      ("    if (al != sorted(al) or len(set(al)) != len(al) or al[0] < ARM_INDEX_RANGE[0] or al[-1] > ARM_INDEX_RANGE[1] or al == list(range(len(al)))\n"
       "            or len(al) != n):", "    if False:")]),
    ('M1b_trace_od_only', 'F1 흔적 = od 하나 (stop_trace 옛 꼴)', 'PC12A',
     [("    if check_trace(folder, od):\n        return True\n    if not isinstance(run, str):\n        return False",
       "    if check_trace(folder, od):\n        return True\n    if True:\n        return False")]),
    ('M2a_side_shapes_off', 'F2 (원인 · rc) 대응표 (CHAIN_SIDE_SHAPES)', 'PC12B',
     [("CHAIN_SIDE_SHAPES = {'exit_ok': (None, 'same'), 'exit_fail': (None, 'same'), 'killed:signal_after': (None, 'int'),\n"
       "                     'killed:timeout': ('timeout', 'any'), 'killed:signal': ('signal', 'any')}", "CHAIN_SIDE_SHAPES = {}")]),
    ('M2b_confirmed_gu_only', 'F2 멈춤 코드 ↔ 확인 (STOP_CONFIRMED 옛 = GU 만)', 'PC12B',
     [("STOP_CONFIRMED = {'GROUP_UNCONFIRMED': False, 'TIME_LIMIT': True, 'RUNNER_RC': True}", "STOP_CONFIRMED = {'GROUP_UNCONFIRMED': False}")]),
    ('M3_prior_off', 'F3 앞 런 기록 (prior_runs_problem)', 'PC12C',
     [("    runs = s.get('runs')\n    if not isinstance(runs, list):\n        return None\n    prior = runs if rr is None else runs[:-1]",
       "    return None\n    runs = s.get('runs')\n    if not isinstance(runs, list):\n        return None\n    prior = runs if rr is None else runs[:-1]")]),
    ('M4_lenient_json', 'F4 요약 읽기 = json.loads (read_summary_state 옛 꼴)', 'PC12D',
     [("        v = _json_strict(raw)                                # ★ 11-08 PC12-04", "        v = json.loads(raw.decode('utf-8'))                  # ★ 11-08 PC12-04")]),
    ('M5_code_shape_only', 'F5 거부 기록 code = 글자 꼴만 (rejected_form_problem 옛 꼴)', 'PC12E',
     [("STOP_CODE_RE.fullmatch(rec['code']) and rec['code'] in STOPS):", "STOP_CODE_RE.fullmatch(rec['code'])):")]),
]

res = {'chain_sha256_original': sha0, 'mutants': []}
for name, guard, want_fail, edits in MUTANTS:
    src = orig.decode('utf-8')
    for old, new in edits:
        assert src.count(old) == 1, (name, src.count(old), old[:80])
        src = src.replace(old, new)
    compile(src, str(chain), 'exec')
    chain.write_text(src, encoding='utf-8')
    out_json = OUT.with_name(f'mut_{name}.json')
    try:
        p = subprocess.run([sys.executable, str(DUMP), str(COPY), str(out_json)], capture_output=True, text=True, timeout=900)
        rows = json.loads(out_json.read_text(encoding='utf-8')) if out_json.is_file() else {}
    finally:
        chain.write_bytes(orig)
    failed = sorted(k for k, v in rows.items() if not k.startswith('_') and not v.get('ok'))
    bad_rows = {k: sorted((v.get('why') or {}).get('bad', {})) if isinstance(v.get('why'), dict) else v.get('why') for k, v in rows.items()
                if not k.startswith('_') and not v.get('ok')}
    res['mutants'].append({'name': name, 'guard': guard, 'expect_fail': want_fail, 'failed': failed, 'caught': failed == [want_fail],
                           'bad_rows': bad_rows, 'rc': p.returncode, 'stderr_tail': p.stderr[-300:]})
    print(f'{name:24s} expect {want_fail} → failed {failed}  {"✓ caught" if failed == [want_fail] else "✗"}')
assert hashlib.sha256(chain.read_bytes()).hexdigest() == sha0
res['chain_sha256_restored'] = hashlib.sha256(chain.read_bytes()).hexdigest()
res['all_caught'] = all(m['caught'] for m in res['mutants'])
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('all_caught', res['all_caught'], '· restored', res['chain_sha256_restored'] == sha0)
