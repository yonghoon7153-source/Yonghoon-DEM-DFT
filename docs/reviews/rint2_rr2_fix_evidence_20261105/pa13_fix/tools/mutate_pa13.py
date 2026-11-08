"""변이 시험 (사전 공격 13 고침) — 새 조건을 하나씩 지우거나 약하게 한 rint_r_chain.py (고친 판) 로 만든 뿌리 (scripts = 작업 트리 링크 + 변이 사슬 + 고친 시험 사본 ·
docs 링크) 에서 `test_rint_r_chain.py --only PA13` → 잡힘 (실패 ≥ 1) / 놓침.  M00 = 변이 없음 (4/4 통과여야).
쓰임: python3 mutate_pa13.py <작업 트리> <결과 폴더> [일꾼 수]"""
import concurrent.futures as cf
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from mktree import make_tree  # noqa: E402

WT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
WORKERS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
ORIG = (WT / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
TEST = WT / 'scripts' / 'test_rint_r_chain.py'

MUTS = [
    #  ── P2-2 값 꼴 술어 (arm_public_value_problem) · 부르는 곳 ──
    ('V01_state_drop', "    if not (type(st) is str and st in ARM_STATES):\n        return f'state {st!r} (= {list(ARM_STATES)})'\n", ""),
    ('V02_pid_drop', "    if not (type(pid) is str and pid.startswith(RC.CA_EXT_PREFIX + '-')):\n        return f'protocol_id {pid!r} (= 글 {RC.CA_EXT_PREFIX}-…)'\n", ""),
    ('V02b_pid_prefix_drop', "    if not (type(pid) is str and pid.startswith(RC.CA_EXT_PREFIX + '-')):", "    if not (type(pid) is str):"),
    ('V03_sid_drop', "    if not (type(sid) is str and sid):\n        return f'sid_fp {sid!r} (= 비지 않은 글)'\n", ""),
    ('V03b_sid_empty_ok', "    if not (type(sid) is str and sid):", "    if not (type(sid) is str):"),
    ('V04_cp_len_drop', "    if not (type(cp) is list and len(cp) == 4):", "    if not (type(cp) is list):"),
    ('V04b_cp_type_widen', "    if not (type(cp) is list and len(cp) == 4):", "    if not (isinstance(cp, (list, dict)) and len(cp) == 4):"),
    ('V05_cp_pos_drop', "    if st == 'positive' and not all(x is True for x in cp):", "    if False:"),
    ('V06_err_finite_drop', "    if not (isinstance(e, float) and math.isfinite(e)):", "    if not (isinstance(e, float)):"),
    ('V06b_err_type_widen', "    if not (isinstance(e, float) and math.isfinite(e)):", "    if not (isinstance(e, (int, float)) and math.isfinite(e)):"),
    ('V07_err_nonneg_drop', "    if e < 0.0:\n        return f'err_rel {e!r} (≥ 0)'\n", ""),
    ('V08_err_zero_drop', "    if st == 'zero' and e != 0.0:", "    if False:"),
    ('V09_iters_cg_only', "    for k in ('cg_iters', 'resolve_iters'):\n        v = a.get(k)", "    for k in ('cg_iters',):\n        v = a.get(k)"),
    ('V09b_iters_resolve_only', "    for k in ('cg_iters', 'resolve_iters'):\n        v = a.get(k)", "    for k in ('resolve_iters',):\n        v = a.get(k)"),
    ('V10_iters_neg_ok', "        if v is not None and _int_or_none(v) is None:", "        if v is not None and type(v) is not int:"),
    ('V11_conv_drop', "    if st == 'positive':\n        ok, why = RC.conv_ok(a.get('cg_info'), False, a.get('cg_resid'))",
     "    if False:\n        ok, why = RC.conv_ok(a.get('cg_info'), False, a.get('cg_resid'))"),
    ('V12_kind_call_drop', "        why = arm_public_value_problem(a)                # ★ 11-09", "        why = None                # ★ 11-09"),
    ('V13_read_run_call_drop', "        why = arm_public_value_problem(arm)\n", "        why = None\n"),
    ('V14_states_all', "ARM_STATES = tuple(k for k, (reg, _why) in REG_STATES.items() if reg != 'NOT_COMPUTED')",
     "ARM_STATES = tuple(k for k, (reg, _why) in REG_STATES.items())"),
    #  ── P2-1 ① (resume_mismatch_problem) ──
    ('R01_rule1_call_drop', "    why = resume_mismatch_problem(s, code, run)              # ★ 11-09", "    why = None              # ★ 11-09"),
    ('R02_rule1_code_drop', "    if bad and not (code == 'RESUME_MISMATCH' and isinstance(R.get('rerun'), str) and run == R.get('rerun')):",
     "    if bad and not (isinstance(R.get('rerun'), str) and run == R.get('rerun')):"),
    ('R03_rule1_run_drop', "    if bad and not (code == 'RESUME_MISMATCH' and isinstance(R.get('rerun'), str) and run == R.get('rerun')):",
     "    if bad and not (code == 'RESUME_MISMATCH' and isinstance(R.get('rerun'), str)):"),
    ('R04_rule1_rerun_str_drop', "    if bad and not (code == 'RESUME_MISMATCH' and isinstance(R.get('rerun'), str) and run == R.get('rerun')):",
     "    if bad and not (code == 'RESUME_MISMATCH' and run == R.get('rerun')):"),
    ('R05_rule1_same_truthy', "if not (type(x) is dict and x.get('same') is True)]", "if not (type(x) is dict and x.get('same'))]"),
    ('R06_rule1_list_guard_drop', "    if not isinstance(R, dict) or type(R.get('compared')) is not list:\n        return None\n    bad =",
     "    if not isinstance(R, dict):\n        return None\n    bad ="),
    #  ── P2-1 더 굳게 (resume_rerun_problem) ──
    ('S01_nondict_ok', "        if R is not None:\n            return f'멈춤 {code} · resume 칸 = {type(R).__name__}", "        if False:\n            return f'멈춤 {code} · resume 칸 = {type(R).__name__}"),
    ('S02_resume_null_ok', "        if att is not None and att['resume_of'] is not None:", "        if False:"),
    ('S03_resume_of_type_drop', "    if not (ro is None or type(ro) is int):\n", "    if False:\n"),
    ('S04_from_range_drop', "    if not (type(frm) is int and n is not None and lo <= frm < n):", "    if not (type(frm) is int and n is not None):"),
    ('S04b_from_bool_ok', "    if not (type(frm) is int and n is not None and lo <= frm < n):", "    if not (isinstance(frm, int) and n is not None and lo <= frm < n):"),
    ('S05_copied_names_drop', "    if not (type(cop) is list and cop == [r.get('name') for r in copies] and all(",
     "    if not (type(cop) is list and all("),
    ('S05b_copied_from_drop', " and all(type(r['copied_from']) is int and r['copied_from'] == frm for r in copies)):", "):"),
    ('S06_copies_first_drop', "    if new and any('copied_from' in r for r in runs[new[0]:]):", "    if False:"),
    ('S07_first_name_drop', "    if first is not None and first.get('name') != rerun:", "    if False:"),
    ('S08_stop_in_rerun_ok', "        if cmp_ != [] or det is not None:", "        if False:"),
    ('S09_first_none_drop', "    if first is None:\n        return f'멈춤 {code} · 런 {run!r} 인데 resume 칸 rerun", "    if False:\n        return f'멈춤 {code} · 런 {run!r} 인데 resume 칸 rerun"),
    ('S10_cmp_list_drop', "    if (type(cmp_) is not list or det not in RESUME_DETERMINISM", "    if (det not in RESUME_DETERMINISM"),
    ('S11_det_member_drop', "    if (type(cmp_) is not list or det not in RESUME_DETERMINISM or (det == 'compared') != bool(cmp_)",
     "    if (type(cmp_) is not list or (det == 'compared') != bool(cmp_)"),
    ('S12_det_consistency_drop', "    if (type(cmp_) is not list or det not in RESUME_DETERMINISM or (det == 'compared') != bool(cmp_)",
     "    if (type(cmp_) is not list or det not in RESUME_DETERMINISM"),
    ('S13_elem_keys_drop', "and set(x) == set(RESUME_COMPARED_KEYS) and type(x['file']) is str", "and type(x['file']) is str"),
    ('S13b_elem_file_drop', "and set(x) == set(RESUME_COMPARED_KEYS) and type(x['file']) is str", "and set(x) == set(RESUME_COMPARED_KEYS)"),
    ('S14_od_drop', "    if not (isinstance(od, str) and RUN_DIR_RE.fullmatch(od) and (want_od is None or od == want_od)):", "    if False:"),
    ('S14b_od_exact_drop', "and RUN_DIR_RE.fullmatch(od) and (want_od is None or od == want_od)):", "and RUN_DIR_RE.fullmatch(od)):"),
    ('S15_side_file_drop', "        if os.path.lexists(str(folder.parent / f'attempt_{frm}.rejected.json')):", "        if False:"),
    ('S16_recompare_drop', "    if cmp_ != want:                                      # (determinism", "    if False:                                      # (determinism"),
    ('S17_oserror_guard_drop', "    except OSError as e:\n        return f'멈춤 {code} · resume 칸 다시 대조를 못 한다",
     "    except ImportError as e:\n        return f'멈춤 {code} · resume 칸 다시 대조를 못 한다"),
    ('S18_rerun_call_drop', "    return resume_rerun_problem(s, folder, code, run)        # ★ 11-09", "    return None        # ★ 11-09"),
    #  ── P3-2 앞자리 한 함수 ──
    ('P01_read_run_own_formula', "    pref = arm_file_prefix(req['kit'])                 # ★ 11-09", "    pref = f'p2_{req[\"kit\"][len(\"kit_\"):]}_'                 # ★ 11-09"),
    ('P02_graph_own_formula', "        pref = GRAPH_ONLY_PREFIX + arm_file_prefix(str(req.get('kit')))",
     "        pref = f'{GRAPH_ONLY_PREFIX}p2_{str(req.get(\"kit\"))[len(\"kit_\"):]}_'"),
]


def run_one(item):
    nm, old, new = item
    if old is None:
        text = ORIG
    else:
        n = ORIG.count(old)
        if n != 1:
            return nm, 'SKIP', f'old occurs {n}', []
        text = ORIG.replace(old, new)
    root = OUT / 'roots' / nm
    src = OUT / 'srcs' / f'{nm}.py'
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(text, encoding='utf-8')
    make_tree(WT, root, src, TEST)
    tmp = OUT / 'tmp' / nm
    tmp.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(tmp))
    r = subprocess.run([sys.executable, str(root / 'scripts' / 'test_rint_r_chain.py'), '--only', 'PA13'], cwd=str(tmp), env=env,
                       capture_output=True, text=True, timeout=1800)
    fails = re.findall(r'^  FAIL  (\S+)', r.stdout, re.M)
    summ = [ln for ln in r.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    shutil.rmtree(root, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)
    verdict = ('PASS_ALL' if not fails and r.returncode == 0 else 'FAILS') if old is None else ('CAUGHT' if fails else 'MISSED')
    return nm, verdict, summ[-1] if summ else (r.stdout[-300:] + r.stderr[-300:]), fails


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    first = run_one(('M00_identity', None, None))
    res[first[0]] = first[1:]
    print(*first, flush=True)
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for nm, verdict, summ, fails in ex.map(run_one, MUTS):
            res[nm] = (verdict, summ, fails)
            print(nm, verdict, fails, summ, flush=True)
    n = len(MUTS)
    caught = sum(1 for k, v in res.items() if k != 'M00_identity' and v[0] == 'CAUGHT')
    skipped = sum(1 for k, v in res.items() if v[0] == 'SKIP')
    print(f'\n변이 {n} · 잡힘 {caught} · 놓침 {n - caught - skipped} · 건너뜀 {skipped} · 변이 없음 {res["M00_identity"][0]}', flush=True)
    (OUT / 'mutation_results.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
