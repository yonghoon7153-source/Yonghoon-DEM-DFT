"""Mutation harness — weaken each new condition (exact single replace) in a mutant copy, run test_rint_r_chain.py --only <sel>."""
import os, sys, shutil, subprocess, json, re, time
from pathlib import Path
SRC = Path('/home/user/pa14/scripts')
SCR = Path('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14')
MROOT = SCR / 'mutroot'
MUT = MROOT / 'scripts'
orig = (SRC / 'rint_r_chain.py').read_text(encoding='utf-8')
M = [
 ('M01_same_truthy', "x.get('same') is True)]", "x.get('same'))]"),
 ('M02_drop_code', "if bad and not (code == 'RESUME_MISMATCH' and ", "if bad and not ("),
 ('M03_drop_run_eq', " and run == R.get('rerun')):", "):"),
 ('M04_drop_rerun_str', "isinstance(R.get('rerun'), str) and run ==", "run =="),
 ('M05_no_mismatch_call', "why = resume_mismatch_problem(s, code, run)", "why = None"),
 ('M06_no_rerun_call', "return resume_rerun_problem(s, folder, code, run)", "return None"),
 ('M07_nondict_resume_ok', "        if R is not None:\n            return f'멈춤 {code} · resume 칸 = {type(R).__name__}", "        if False:\n            return f'멈춤 {code} · resume 칸 = {type(R).__name__}"),
 ('M08_null_resume_ok', "if att is not None and att['resume_of'] is not None:", "if False:"),
 ('M09_ro_type', "if not (ro is None or type(ro) is int):", "if False:"),
 ('M10_drop_lo', "lo <= frm < n)", "frm < n)"),
 ('M11_drop_n', "lo <= frm < n)", "lo <= frm)"),
 ('M12_frm_isinstance', "if not (type(frm) is int and n is not None", "if not (isinstance(frm, int) and n is not None"),
 ('M13_copied_names', "cop == [r.get('name') for r in copies] and ", ""),
 ('M14_copiedfrom_type', "type(r['copied_from']) is int and r['copied_from'] == frm", "r['copied_from'] == frm"),
 ('M15_copiedfrom_eq', "type(r['copied_from']) is int and r['copied_from'] == frm", "type(r['copied_from']) is int"),
 ('M16_copy_after_new', "if new and any('copied_from' in r for r in runs[new[0]:]):", "if False:"),
 ('M17_first_name', "if first is not None and first.get('name') != rerun:", "if False:"),
 ('M18_rr_det_only', "if cmp_ != [] or det is not None:", "if det is not None:"),
 ('M19_rr_cmp_only', "if cmp_ != [] or det is not None:", "if cmp_ != []:"),
 ('M20_first_none', "    if first is None:\n        return f'멈춤 {code} · 런 {run!r} 인데 resume 칸 rerun", "    if False:\n        return f'멈춤 {code} · 런 {run!r} 인데 resume 칸 rerun"),
 ('M21_det_domain', "det not in RESUME_DETERMINISM or ", ""),
 ('M22_det_iff', "or (det == 'compared') != bool(cmp_)", ""),
 ('M23_cmp_keys', "set(x) == set(RESUME_COMPARED_KEYS) and ", ""),
 ('M24_cmp_file_str', " and type(x['file']) is str) for x in cmp_)", ") for x in cmp_)"),
 ('M25_od_want', "(want_od is None or od == want_od)", "True"),
 ('M26_side_rej', "if os.path.lexists(str(folder.parent / f'attempt_{frm}.rejected.json')):", "if False:"),
 ('M27_recompare', "    if cmp_ != want:", "    if False:"),
 ('M28_oserror_open', "        return f'멈춤 {code} · resume 칸 다시 대조를 못 한다", "        return None\n        return f'멈춤 {code} · resume 칸 다시 대조를 못 한다"),
 ('M29_state', "if not (type(st) is str and st in ARM_STATES):", "if False:"),
 ('M30_pid', "if not (type(pid) is str and pid.startswith(RC.CA_EXT_PREFIX + '-')):", "if False:"),
 ('M31_pid_nodash', "pid.startswith(RC.CA_EXT_PREFIX + '-')):", "pid.startswith(RC.CA_EXT_PREFIX)):"),
 ('M32_sid', "if not (type(sid) is str and sid):", "if False:"),
 ('M33_cp_len', "if not (type(cp) is list and len(cp) == 4):", "if not (type(cp) is list):"),
 ('M34_cp_pos', "if st == 'positive' and not all(x is True for x in cp):", "if False:"),
 ('M35_err_float', "if not (isinstance(e, float) and math.isfinite(e)):", "if False:"),
 ('M36_err_neg', "    if e < 0.0:", "    if False:"),
 ('M37_err_zero', "if st == 'zero' and e != 0.0:", "if False:"),
 ('M38_iters', "if v is not None and _int_or_none(v) is None:", "if False:"),
 ('M39_conv', "        if not ok:\n            return f'cg_info {a.get(\"cg_info\")!r}", "        if False:\n            return f'cg_info {a.get(\"cg_info\")!r}"),
 ('M40_kind_call', "why = arm_public_value_problem(a)                #", "why = None                #"),
 ('M41_readrun_call', "why = arm_public_value_problem(arm)", "why = None"),
 ('M42_arm_states_all', "if reg != 'NOT_COMPUTED')", "if True)"),
 ('M43_readrun_pref', "pref = arm_file_prefix(req['kit'])", "pref = 'p2_'"),
 ('M44_gsrc_pref', "pref = GRAPH_ONLY_PREFIX + arm_file_prefix(str(req.get('kit')))", "pref = GRAPH_ONLY_PREFIX"),
 ('M45_cp_type', "if not (type(cp) is list and len(cp) == 4):", "if not (len(cp) == 4):"),
 ('M46_pid_type', "if not (type(pid) is str and pid.startswith", "if not (str(pid).startswith"),
 ('M47_mm_elem_type', "if not (type(x) is dict and x.get('same') is True)]", "if not (x.get('same') is True)]"),
 ('M51_det_allow_none', "RESUME_DETERMINISM = ('compared', 'assumed')", "RESUME_DETERMINISM = ('compared', 'assumed', None)"),
 ('M52_cmp_keys_file_only', "RESUME_COMPARED_KEYS = ('file', 'same')", "RESUME_COMPARED_KEYS = ('file', 'same', 'x')"),
 ('M54_lo_one', "lo = ro if ro is not None else 1", "lo = 1"),
 ('M56_side_rej_dir', "    if not src.is_dir():", "    if not src.exists():"),
]
sel = sys.argv[1] if len(sys.argv) > 1 else 'PA13'
only = sys.argv[2].split(',') if len(sys.argv) > 2 else None
# mutant dir: symlink everything except the two files
if MROOT.exists():
    shutil.rmtree(MROOT)
MUT.mkdir(parents=True)
os.symlink(SRC.parent / 'docs', MROOT / 'docs')
os.symlink(SRC.parent / '.gitignore', MROOT / '.gitignore')
for p in SRC.iterdir():
    if p.name in ('rint_r_chain.py', 'test_rint_r_chain.py', '__pycache__'):
        continue
    os.symlink(p, MUT / p.name)
shutil.copy2(SRC / 'test_rint_r_chain.py', MUT / 'test_rint_r_chain.py')
res = {}
for nm, old, new in M:
    if only and nm not in only:
        continue
    c = orig.count(old)
    if c != 1:
        res[nm] = f'BAD_PATTERN count={c}'
        print(nm, res[nm], flush=True)
        continue
    (MUT / 'rint_r_chain.py').write_text(orig.replace(old, new), encoding='utf-8')
    shutil.rmtree(MUT / '__pycache__', ignore_errors=True)
    t0 = time.time()
    p = subprocess.run([sys.executable, str(MUT / 'test_rint_r_chain.py'), '--only', sel], capture_output=True, text=True, timeout=1800, cwd=str(MUT))
    last = [l for l in p.stdout.splitlines() if l.startswith('test_rint_r_chain:')]
    fails = re.findall(r'FAIL  (\S+)', p.stdout)
    res[nm] = {'killed': p.returncode != 0, 'fails': fails, 'summary': last[-1] if last else p.stdout[-200:] + p.stderr[-300:], 's': round(time.time() - t0, 1)}
    print(nm, 'KILLED' if res[nm]['killed'] else 'SURVIVED', fails, flush=True)
(SCR / 'out' / f'mutation_{sel}.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
k = sum(1 for v in res.values() if isinstance(v, dict) and v['killed'])
n = sum(1 for v in res.values() if isinstance(v, dict))
print(f'killed {k}/{n}')
