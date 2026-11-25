"""CK focused regression; stdlib + Bash/GNU tools. PACK_ONLY, no scientific jobs.
Run: python probe_pack_ck.py --source CHECKOUT --bash /bin/bash
Uses original CJ fixture driver via AST, replacing only its injected-fault table.
The checked-in runner and its MANIFEST are never changed.
"""
import ast, json, runpy, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES = {
 'mgmt_written_error': 'echo(){ builtin echo "$@"; case "$*" in run/env.txt|run/status.tsv) return 73;; esac; return 0; }\n',
 'manifest_written_error': 'echo(){ builtin echo "$@"; [ "$*" = MANIFEST.sha256 ] && return 73; return 0; }\n',
 'mgmt_silent_drop': 'echo(){ case "$*" in run/env.txt|run/status.tsv) return 0;; esac; builtin echo "$@"; }\n',
 'manifest_silent_drop': 'echo(){ [ "$*" = MANIFEST.sha256 ] && return 0; builtin echo "$@"; }\n',
 'mgmt_duplicate': 'echo(){ case "$*" in run/env.txt|run/status.tsv) builtin echo "$@"; builtin echo "$@"; return 0;; esac; builtin echo "$@"; }\n',
 'manifest_replaced': 'echo(){ if [ "$*" = MANIFEST.sha256 ]; then builtin echo run/env.txt; return 0; fi; builtin echo "$@"; }\n',
 'mgmt_replaced_same_count': 'echo(){ if [ "$*" = run/env.txt ]; then builtin echo run/status.tsv; return 0; fi; builtin echo "$@"; }\n',
 'cat_written_error': 'cat(){ command cat "$@"; r=$?; case "$*" in *mgmt*) return 73;; esac; return "$r"; }\n',
 'wc_error': 'wc(){ return 73; }\n',
 'wc_output_error': 'wc(){ command wc "$@"; return 73; }\n',
 'cut_error': 'cut(){ return 73; }\n',
 'cut_output_error': 'cut(){ command cut "$@"; return 73; }\n',
 'sha_silent_empty': 'sha256sum(){ case "$*" in *tgz.part*) return 0;; esac; command sha256sum "$@"; }\n',
 'manifest_presence_grep_error': 'grep(){ if [ "$1" = -qxF ] && [ "$2" = MANIFEST.sha256 ]; then return 2; fi; command grep "$@"; }\n',
 'mgmt_presence_grep_error': 'grep(){ if [ "$1" = -qxF ] && [ "$2" = run/env.txt ]; then return 2; fi; command grep "$@"; }\n',
 'find_complete_then_error': 'find(){ command find "$@"; return 73; }\n',
 # Not asserted as product failure: demonstrates the explicitly proposed trust boundary.
 'diagnostic_find_omits_stdout_rc0': 'find(){ command find "$@" | command grep -v "/stdout.log$"; return 0; }\n',
}

tree = ast.parse((HERE/'probe_pack_cj.py').read_text(encoding='utf-8'))
replaced = 0
for n in ast.walk(tree):
    if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'cases' for t in n.targets):
        n.value = ast.parse(repr(CASES), mode='eval').body
        replaced += 1
    # Keep CJ's result file intact; CK has its own output.
    if isinstance(n, ast.Constant) and n.value == 'pack_cj_results.json':
        n.value = 'pack_ck_results.json'
assert replaced == 1
assert '--assert-fixed' not in sys.argv, 'CK assertions are unconditional; omit --assert-fixed'
ns = {'__file__': str(HERE/'probe_pack_cj.py'), '__name__': '__main__'}
exec(compile(ast.fix_missing_locations(tree), 'CJ_driver_with_CK_faults', 'exec'), ns)
r = ns['results']
for k in CASES:
    if k.startswith('diagnostic_'):
        assert r[k]['rc'] == 0 and len(r[k]['members']) == 23 and r[k]['sha_check_rc'] == 0
        continue
    assert r[k]['rc'] == 4 and not r[k]['success_message'] and r[k]['old_pair_preserved'] and not r[k]['parts_present'], (k, r[k])
for k in ('positive','recovery'):
    assert r[k]['rc'] == 0 and len(r[k]['members']) == 25 and r[k]['sha_check_rc'] == 0, (k,r[k])
assert r['empty_run']['rc'] == 0 and sorted(r['empty_run']['members']) == ['MANIFEST.sha256','run/env.txt']
c = r['post_promotion_cleanup_error']
assert c['rc'] == 0 and c['sha_check_rc'] == 0 and len(c['members']) == 25 and '⚠' in c['log']
print('CK focused assertions PASS: 16 blocking faults; positives/recovery/empty/cleanup; 1 trust-boundary diagnostic')
