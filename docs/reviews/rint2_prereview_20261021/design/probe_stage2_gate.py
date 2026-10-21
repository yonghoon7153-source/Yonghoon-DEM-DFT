"""Does S0 stage 2 (DBE geometry) open before s_min / the R-run plan are sealed?

Builds a throwaway git repo in this folder: a valid S0 plan (made by the tool's own make_plan), and a copy of the
HEAD registration where ONLY the S0-plan sha256 is written into the `| S0 계획 해시 |` row; the R-run
`| 계획 해시 |` row (which binds s_min_um) stays ⬜.  Then calls the tool's real stage-2 gate verify_plan_commit, and the
chain's real registration_plan_hash on the same document.

Usage: python3 -I probe_stage2_gate.py <worktree_root>
"""
import json
import os
import shutil
import subprocess
import sys

wt = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(wt, 'scripts'))
import ca_s0_census as s0          # noqa: E402  (read-only import of the HEAD tool)
import rint_r_chain as chain       # noqa: E402

here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.join(here, 'stage2_gate_repo')
shutil.rmtree(repo, ignore_errors=True)
os.makedirs(os.path.join(repo, 'docs', 'reviews'))
os.makedirs(os.path.join(repo, 'docs', 'data', 'rint2_s0_sbe_test'))
env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')


def g(*a):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, env=env, check=True).stdout.strip()


g('init', '-q')
plan, pb, h = s0.make_plan(0.05, s0.R_F_UM if s0.R_F_UM is not None else 0.075, s0.GAP_TOL_PRODUCTION,
                           {'note': 'probe', 'inputs_sha256': {}})
plan_rel = 'docs/data/rint2_s0_sbe_test/cjunc_plan.json'
open(os.path.join(repo, plan_rel), 'wb').write(pb)
reg_src = open(os.path.join(wt, s0.R_DOC_DEFAULT), encoding='utf-8').read()
lines = reg_src.splitlines(keepends=True)
out, n_s0 = [], 0
for ln in lines:
    if ln.startswith('| S0 계획 해시 |'):
        cells = ln.rstrip('\n').split('|')
        cells[-2] = f' {h} '            # last cell = the value column
        ln = '|'.join(cells) + '\n'
        n_s0 += 1
    out.append(ln)
open(os.path.join(repo, s0.R_DOC_DEFAULT), 'w', encoding='utf-8').write(''.join(out))
g('add', '-A')
g('commit', '-q', '-m', 'S0 plan hash only (R-run plan hash + s_min still blank)')
sha = g('rev-parse', 'HEAD')
res = {'s0_rows_filled': n_s0, 'commit': sha}
try:
    p2, h2, full = s0.verify_plan_commit(repo, sha, plan_rel, r_doc=s0.R_DOC_DEFAULT)
    res['stage2_gate'] = 'PASSED (DBE geometry may be opened)'
except s0.S0Error as e:
    res['stage2_gate'] = f'REFUSED: {e}'
try:
    chain.registration_plan_hash(os.path.join(repo, s0.R_DOC_DEFAULT))
    res['chain_R_plan_hash'] = 'registered'
except chain.Stop as e:
    res['chain_R_plan_hash'] = f'Stop {e.code if hasattr(e, "code") else e}'
except Exception as e:                       # noqa: BLE001
    res['chain_R_plan_hash'] = f'{type(e).__name__}: {e}'
s_min_rows = [ln.strip()[:160] for ln in out if 's_min = ⬜' in ln or 'S0 단계 1 의 s_min' in ln]
res['registration_s_min_still_blank_rows'] = s_min_rows[:3]
print(json.dumps(res, ensure_ascii=False, indent=1))
json.dump(res, open(os.path.join(here, 'probe_stage2_gate.json'), 'w'), ensure_ascii=False, indent=1)
