"""Mutation runner for preattack 8 — applies one textual mutation at a time to a scratch copy of the tree, runs the selected tests,
restores the file, records killed / survived per mutant.

  python3 -I mutate8.py <mut_tree> <out.json> [mutant ids comma]   (sequential · restores the original bytes after every mutant)
"""
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
CJF = 'scripts/carbon_junction.py'
TRR = ['scripts/test_rint_r_chain.py', '--only']
TCJ = ['scripts/test_carbon_junction.py', '--only']
TE2E = ['scripts/test_rint_r_chain_e2e.py', '--only']

# (id, file, old, new, test argv, tests that should catch it)
M = [
    ('M01', RRF, "        s0 = st['starts'].get(n)\n        if s0 is not None:\n", "        s0 = None\n        if s0 is not None:\n",
     TRR + ['PE01'], 'PE01 · PE01h · PE01r'),
    ('M02', RRF, "        ledger_append(repo, start, f'rint-r attempt {n} start {e[\"target\"]} {e[\"machine\"]}', expect=raw)\n",
     "        pass\n", TRR + ['PE01'], 'PE01 (start record count)'),
    ('M03', RRF, "            if n in st['starts']:\n", "            if False:\n", TRR + ['PE01p'], 'PE01p start_twice'),
    ('M04', RRF, "            if n in st['results']:\n                bad(f'항목 {n} 의 시작 기록이 결과 줄 뒤에", "            if False:\n                bad(f'항목 {n} 의 시작 기록이 결과 줄 뒤에",
     TRR + ['PE01p'], 'PE01p start_after_result'),
    ('M05', RRF, "isinstance(b, str) and b and os.path.isabs(b) and '\\0' not in b", "isinstance(b, str) and b and '\\0' not in b", TRR + ['PE01p'],
     'PE01p start_base_relative'),
    ('M06', RRF, "    if not (isinstance(h, dict) and set(h) == START_HOST_KEYS and all(v is None or isinstance(v, str) for v in h.values())):",
     "    if False:", TRR + ['PE01p'], 'PE01p host rows'),
    ('M07', RRF, "    if s['folder'] != f'attempt_{s[\"n\"]}':", "    if False:", TRR + ['PE01p'], 'PE01p folder rows'),
    ('M08', RRF, "            if s0 is not None and s0['base'] != fb:", "            if False:", TRR + ['PE01'], 'PE01 row_copy'),
    ('M09', RRF, "                if r0['folder'] != f.name or dg != r0['folder_sha256']:", "                if False:", TRR + ['PE01'], 'PE01 row_copy2 · PE01c'),
    ('M10', RRF, "                                                   f'--ledger {repo} 뒤 다음 시도 (★ 11-02 PC7-01)'))\n        return 3\n",
     "                                                   f'--ledger {repo} 뒤 다음 시도 (★ 11-02 PC7-01)'))\n", TRR + ['PE01f'], 'PE01f'),
    ('M11', RRF, "'base': str(base.resolve())", "'base': str(base.absolute())", TRR + ['PE01s'], 'PE01s'),
    ('M12', RRF, "            if a is None:\n                if r is not None and r.get('status') == 'rejected'",
     "            if a is None:\n                continue\n                if r is not None and r.get('status') == 'rejected'", TRR + ['PE02,PD12u,PE02x'],
     'PE02 · PD12u'),
    ('M13', RRF, "if r is not None and r.get('status') == 'rejected' and (Path(p).parent / f'attempt_{k}{REJECTED_SIDE}').is_file():",
     "if r is not None and r.get('status') == 'rejected':", TRR + ['PD12u,PE02x'], 'PD12u rejected_no_side · PE02x v2'),
    ('M14', RRF, "if r is not None and r.get('status') == 'rejected' and (Path(p).parent / f'attempt_{k}{REJECTED_SIDE}').is_file():",
     "if (Path(p).parent / f'attempt_{k}{REJECTED_SIDE}').is_file():", TRR + ['PD12u'], 'PD12u stopped_side'),
    ('M15', RRF, "            c = chain_end_fixed(er) or words_cause(", "            c = None or words_cause(", TRR + ['PE03'], 'PE03 · PE03u'),
    ('M16', RRF, "CHAIN_END_FIXED = {'exception': 'chain_exception'}", "CHAIN_END_FIXED = {'exception': 'parent_dead'}", TRR + ['PE03'],
     'PE03 · PE03u'),
    ('M17', RRF, "        if prev.get('token') != tok or prev.get('name') != lname:", "        if False:", TRR + ['PE04,PD13g'], 'PE04'),
    ('M18', RRF, "        if prev.get('token') != tok or prev.get('name') != lname:", "        if prev.get('token') != tok:", TRR + ['PE04'],
     'PE04 name_chain'),
    ('M19', RRF, "    if other is not None:                                  # ★ 11-02 PC7-04 — 정리", "    if False:                                  # ★ 11-02 PC7-04 — 정리",
     TRR + ['PE04'], 'PE04'),
    ('M20', RRF, "    if _key_seq(v0) != _key_seq(v1):\n        k.add('key_order')", "    if False:\n        k.add('key_order')", TRR + ['RV05,RV06'], 'RV05 key_order · RV06 order'),
    ('M21', RRF, "    if b'\\r' in s:", "    if False:", TRR + ['RV05,RV06'], 'RV05 crlf · RV06 crlf'),
    ('M22', RRF, "    off = next((i for i in range(n) if old[i] != new[i]), n)", "    off = next((i + 1 for i in range(n) if old[i] != new[i]), n)",
     TRR + ['RV05'], 'RV05 offsets'),
    ('M23', RRF, "            'public_bytes': (byte_diff_view(old_pub, new_pub if new_pub is not None else canon_bytes(pc)) if old_pub is not None else None),",
     "            'public_bytes': None,", TRR + ['RV06'], 'RV06 pub_nl'),
    ('M24', RRF, "    print(f'  바이트 까닭 — 판정 JSON", "    (lambda *_a, **_k: None)(f'  바이트 까닭 — 판정 JSON", TRR + ['RV06'], 'RV06 screen'),
    ('M25', RRF, "        k.add('whitespace' if _json_min(body) == _json_min(tr) else 'format')",
     "        k.add('format' if _json_min(body) == _json_min(tr) else 'whitespace')", TRR + ['RV05'], 'RV05 indent2 · ascii_esc'),
    ('M26', RRF, "    if canon_bytes(v0) != new:                               # 값은 같은데", "    if False:                               # 값은 같은데",
     TRR + ['RV05'], 'RV05 int_float'),
    ('M27', RRF, "        view['kinds'] = ['value']", "        view['kinds'] = ['format']", TRR + ['RV05'], 'RV05 value'),
    ('M28', RRF, "        if tail.replace(b'\\n', b'') != tail_r.replace(b'\\n', b''):\n            k.add('trailing_whitespace')",
     "        if False:\n            k.add('trailing_whitespace')", TRR + ['RV05'], 'RV05 trail_space'),
    ('M29', RRF, "    same = new_pub == old_pub and new_res == old_res", "    same = new_pub == old_pub", TRR + ['RV06'], 'RV06 crlf/order'),
    ('M30', RRF, "        if tail.count(b'\\n') != tail_r.count(b'\\n'):\n            k.add('newline')", "        if False:\n            k.add('newline')",
     TRR + ['RV05,RV06'], 'RV05 extra_nl/no_nl · RV06 pub_nl'),
    ('B01', CJF, "        t = (j + 0.5) * L / k", "        t = (j + 0.25) * L / k", TCJ + ['BAN8'], 'BAN8 ②③'),
    ('B02', CJF, "    return max(2, int(math.ceil(r - CJUNC_LPAR_RTOL)))", "    return max(2, int(math.ceil(r - CJUNC_LPAR_RTOL))) + 1", TCJ + ['BAN8'],
     'BAN8 ②'),
    ('B03', CJF, "    return np.where(np.isnan(r), np.nan, np.where(r > 1.0 + CJUNC_LPAR_RTOL, r, 1.0))",
     "    return np.where(np.isnan(r), np.nan, np.where(r > 1.0 + CJUNC_LPAR_RTOL, r ** 0.9, 1.0))", TCJ + ['BAN8'], 'BAN8 ②③④'),
    ('E01', RRF, "    same = new_pub == old_pub and new_res == old_res", "    same = new_pub == old_pub", TE2E + ['E18'], 'E18i · E18j'),
    ('E02', RRF, "        if tail.replace(b'\\n', b'') != tail_r.replace(b'\\n', b''):\n            k.add('trailing_whitespace')",
     "        if False:\n            k.add('trailing_whitespace')", TE2E + ['E18'], 'E18j'),
]


def run(argv):
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    t0 = time.time()
    p = subprocess.run([sys.executable] + argv, cwd=str(MT), capture_output=True, text=True, env=env, timeout=3600)
    return p.returncode, p.stdout + p.stderr, time.time() - t0


res = json.loads(OUT.read_text()) if OUT.exists() else {}
for mid, f, old, new, argv, catch in M:
    if SEL is not None and mid not in SEL:
        continue
    fp = MT / f
    src = fp.read_bytes()
    txt = src.decode('utf-8')
    cnt = txt.count(old)
    if cnt != 1:
        res[mid] = {'error': f'old string occurs {cnt} times'}
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(mid, 'SKIP', cnt, flush=True)
        continue
    try:
        fp.write_bytes(txt.replace(old, new).encode('utf-8'))
        rc, out, dt = run(argv)
    finally:
        fp.write_bytes(src)
    fails = re.findall(r'^\s*FAIL\s+(\S+)', out, re.M)
    summ = [ln for ln in out.splitlines() if re.search(r'test_rint_r_chain(_e2e)?:|== test_carbon_junction', ln)]
    res[mid] = {'file': f, 'tests': argv[-1], 'expected_catch': catch, 'rc': rc, 'killed': rc != 0, 'failed_ids': sorted(set(fails))[:40],
                'summary': summ[-1:] if summ else out.strip().splitlines()[-2:], 'seconds': round(dt, 1)}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(mid, 'killed' if rc != 0 else 'SURVIVED', sorted(set(fails))[:10], round(dt, 1), flush=True)
