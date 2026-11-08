"""변이 시험 — arms_read_kind · prior_runs_problem · 생산자 새 조건을 하나씩 지우거나 약하게 → 변이 루트 (scripts = 원본 심볼릭 링크 + 변이
rint_r_chain.py + 시험 파일 사본 · docs 링크) 에서 `test_rint_r_chain.py --only RR3,PC12,CT06` → 잡힘 (실패 ≥ 1) / 놓침."""
import json, os, shutil, subprocess, sys, re
from pathlib import Path

SRC = Path('/home/user/pa13')
BASE = Path(__file__).resolve().parent.parent / 'mut'
ORIG = (SRC / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')

MUTS = [
    ('M01_list_type', "    if type(ar) is not list:\n        return 'bad', f'목록 아님", "    if not isinstance(ar, (list, tuple)):\n        return 'bad', f'목록 아님"),
    ('M02_empty_branch_drop', "    if not ar:\n        return 'empty', None\n", ""),
    ('M03_elem_dict_drop', "    if any(type(a) is not dict for a in ar):\n        return 'bad', '원소가 객체가 아님'\n", ""),
    ('M04_fileids_branch_drop', "    if all(set(a) == set(ARM_FILE_ID_KEYS) for a in ar):\n        return 'file_ids', f'파일 신원 {len(ar)} = 판독 실패 때 남긴 꼴'\n", ""),
    ('M05_pubkeys_superset', "    if any(set(a) != set(ARM_PUBLIC) for a in ar):", "    if any(not set(ARM_FILE_ID_KEYS) <= set(a) for a in ar):"),
    ('M05b_pubkeys_drop', "    if any(set(a) != set(ARM_PUBLIC) for a in ar):\n        return 'bad', '칸 집합 ≠ ARM_PUBLIC (판독 완료 꼴) · ≠ 파일 신원'\n", ""),
    ('M06a_no_arms_guard', "    if type(rec) is not dict or 'arms' not in rec or request_fields_problem(rec):", "    if type(rec) is not dict or request_fields_problem(rec):"),
    ('M06b_no_reqfields', "    if type(rec) is not dict or 'arms' not in rec or request_fields_problem(rec):", "    if type(rec) is not dict or 'arms' not in rec:"),
    ('M07_kit_type_drop', "    if type(kit) is not str:\n        return 'bad', f'kit {kit!r}'\n", "    kit = kit if type(kit) is str else 'kit_SBE_vgcf100'\n"),
    ('M08_count_drop', "    if len(ar) != len(idx):\n        return 'bad', f'팔 {len(ar)} ≠ 요청 팔 {len(idx)}'\n", ""),
    ('M09a_index_type_drop', "        if type(x) is not int or x != i:", "        if x != i:"),
    ('M09b_index_eq_drop', "        if type(x) is not int or x != i:", "        if type(x) is not int:"),
    ('M10a_basename_drop', "type(f) is str and os.path.basename(f) == f and f.startswith(pref)", "type(f) is str and f.startswith(pref)"),
    ('M10b_prefix_drop', "os.path.basename(f) == f and f.startswith(pref) and f.endswith", "os.path.basename(f) == f and f.endswith"),
    ('M10c_suffix_drop', " and f.endswith(f'_a{i}.json')):", "):"),
    ('M10d_suffix_any_arm', " and f.endswith(f'_a{i}.json')):", " and re.search(r'_a\\d+\\.json$', f)):"),
    ('M11a_sha_drop', "        if not (type(h) is str and ARM_SHA256_RE.fullmatch(h)):\n            return 'bad'", "        if False:\n            return 'bad'"),
    ('M11b_sha_case', "ARM_SHA256_RE = re.compile(r'[0-9a-f]{64}')", "ARM_SHA256_RE = re.compile(r'[0-9a-fA-F]{64}')"),
    ('M11c_sha_match', "ARM_SHA256_RE.fullmatch(h)", "ARM_SHA256_RE.match(h)"),
    ('M11d_sha_plus', "ARM_SHA256_RE = re.compile(r'[0-9a-f]{64}')", "ARM_SHA256_RE = re.compile(r'[0-9a-f]+')"),
    ('M11e_sha_unicode_digit', "ARM_SHA256_RE = re.compile(r'[0-9a-f]{64}')", "ARM_SHA256_RE = re.compile(r'[\\da-f]{64}')"),
    ('M12_prior_accept_fileids', "        if sh != 'exit_ok' or kind != 'verified':", "        if sh != 'exit_ok' or kind not in ('verified', 'file_ids'):"),
    ('M12b_prior_old_rule', "        if sh != 'exit_ok' or kind != 'verified':", "        if sh != 'exit_ok' or kind == 'empty' or (kind == 'bad' and not (type(r.get('arms_read')) is list and r.get('arms_read'))):"),
    ('M13a_exec_fail_writes_pub', "            rec['arms_read'] = arms_read_record(outdir=outdir)\n            raise\n        rec['arms_read'] = arms_read_record(arms_)\n        a0 = arms_[0]",
     "            rec['arms_read'] = [dict(x, protocol_id=None, state=None, cg_info=None, cg_resid=None, imbalance=None, cert_pass=None, sid_fp=None, cg_iters=None, resolve_iters=None, sv_cf_status=None, err_rel=None) for x in arm_file_shas(outdir)]\n            raise\n        rec['arms_read'] = arms_read_record(arms_)\n        a0 = arms_[0]"),
    ('M13b_copy_fail_writes_pub', "            rec['arms_read'] = arms_read_record(outdir=outdir)    # ★ 11-08 RR3-01 — 생성 한 함수 (복사 다시 읽기 실패 = 파일 신원)",
     "            rec['arms_read'] = [dict(x, protocol_id=None, state=None, cg_info=None, cg_resid=None, imbalance=None, cert_pass=None, sid_fp=None, cg_iters=None, resolve_iters=None, sv_cf_status=None, err_rel=None) for x in arm_file_shas(outdir)]"),
    ('M13c_merge_fail_writes_pub', "            rec['arms_read'] = arms_read_record(outdir=outdir)    # ★ 11-08 RR3-01 — 생성 한 함수 (사본 다시 읽기 실패 = 파일 신원)",
     "            rec['arms_read'] = [dict(x, protocol_id=None, state=None, cg_info=None, cg_resid=None, imbalance=None, cert_pass=None, sid_fp=None, cg_iters=None, resolve_iters=None, sv_cf_status=None, err_rel=None) for x in arm_file_shas(outdir)]"),
    ('M14_prefix_fn', "    return f'p2_{kit[len(\"kit_\"):]}_'", "    return f'p2_{kit}_'"),
]

def make_root(tag, text):
    root = BASE / tag
    if root.exists():
        shutil.rmtree(root)
    sd = root / 'scripts'
    sd.mkdir(parents=True)
    for p in (SRC / 'scripts').iterdir():
        if p.name in ('rint_r_chain.py', 'test_rint_r_chain.py', '__pycache__'):
            continue
        os.symlink(p, sd / p.name)
    (sd / 'rint_r_chain.py').write_text(text, encoding='utf-8')
    shutil.copy2(SRC / 'scripts' / 'test_rint_r_chain.py', sd / 'test_rint_r_chain.py')
    os.symlink(SRC / 'docs', root / 'docs')
    shutil.copy2(SRC / '.gitignore', root / '.gitignore')
    return root

def run_tests(root, only):
    r = subprocess.run([sys.executable, str(root / 'scripts' / 'test_rint_r_chain.py'), '--only', only], cwd=str(BASE),
                       capture_output=True, text=True, timeout=1800)
    fails = re.findall(r'^  FAIL  (\S+)', r.stdout, re.M)
    summ = [l for l in r.stdout.splitlines() if l.startswith('test_rint_r_chain:')]
    return r.returncode, fails, summ[-1] if summ else r.stdout[-300:] + r.stderr[-300:]

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else 'RR3,PC12,CT06'
    res = {}
    root = make_root('M00_identity', ORIG)
    res['M00_identity'] = run_tests(root, only)
    print('M00_identity', res['M00_identity'], flush=True)
    for nm, old, new in MUTS:
        n = ORIG.count(old)
        if n != 1:
            res[nm] = ('SKIP', f'old occurs {n}', '')
            print(nm, res[nm], flush=True)
            continue
        root = make_root(nm, ORIG.replace(old, new))
        rc, fails, summ = run_tests(root, only)
        res[nm] = (rc, fails, summ)
        print(nm, 'CAUGHT' if fails else 'MISSED', fails, summ, flush=True)
        shutil.rmtree(root, ignore_errors=True)
    (BASE / 'mutation_results.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')

if __name__ == '__main__':
    main()
