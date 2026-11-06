"""Codex 회차 ② 탐침 `runtime_review/probe_runtime.py` 를 고치지 않고 다시 — 탐침이 읽는 received/repo 자리에 이 작업 트리의 고친 판 (scripts/ 전부 +
탐침이 읽는 문서 둘) 을 넣은 스크래치 폴더 (리포 밖) 에서 돌리고, Codex 가 남긴 결과 (results.json · candidate_fix_results.json · residual_rc*.json) 와 대조한다.

  python3 -I rerun_codex_probe.py <작업 트리> <스크래치 폴더> <출력 비교.json>
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
OUT = Path(sys.argv[3])
CDX = TREE / 'docs/reviews/codex_rint2_rr_round2_evidence_20261105/runtime_review'
PROBE_SHA = '12f3b4c9d3b37d18888ea4c5b9e89c2ce710f19dee943a436efedf9ebf98c9ee'   # 반입 기록 build_record.json 의 탐침 sha256


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


if WORK.exists():
    sys.exit(f'{WORK} 가 이미 있다 (새 폴더여야)')
(WORK / 'runtime_review').mkdir(parents=True)
shutil.copy2(CDX / 'probe_runtime.py', WORK / 'runtime_review' / 'probe_runtime.py')
assert sha(WORK / 'runtime_review' / 'probe_runtime.py') == PROBE_SHA
repo = WORK / 'received' / 'repo'
shutil.copytree(TREE / 'scripts', repo / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
ev = 'docs/reviews/rint2_rr_fix_evidence_20261023'
shutil.copytree(TREE / ev / 'report_c_raw', repo / ev / 'report_c_raw')
shutil.copy2(TREE / ev / 'q9_time_budget.json', repo / ev / 'q9_time_budget.json')
p = subprocess.run([sys.executable, '-I', '-B', str(WORK / 'runtime_review' / 'probe_runtime.py')], cwd=str(WORK), capture_output=True, text=True,
                   timeout=1800)
(WORK / 'run.log').write_text(p.stdout + p.stderr, encoding='utf-8')
rr = WORK / 'runtime_review'


def load(d, nm):
    return json.loads((d / nm).read_text(encoding='utf-8'))


ours, theirs = load(rr, 'results.json'), load(CDX, 'results.json')
oc = {c['name']: c for c in ours['checks']}
tc = {c['name']: c for c in theirs['checks']}
diff = []
for nm in sorted(set(oc) | set(tc)):
    a, b = oc.get(nm), tc.get(nm)
    if a is None or b is None or a['pass'] != b['pass'] or a['got'] != b['got'] or a['expected'] != b['expected']:
        diff.append({'name': nm, 'ours': a, 'codex': b})
cand_o, cand_t = load(rr, 'candidate_fix_results.json'), load(CDX, 'candidate_fix_results.json')
resid_o, resid_t = load(rr, 'residual_rc.json'), load(CDX, 'residual_rc.json')
integ_o, integ_t = load(rr, 'residual_rc_integration.json'), load(CDX, 'residual_rc_integration.json')
cand_by_rc = {json.dumps(c['rc']): c['fields'] for c in cand_t}
keys = ('status', 'side', 'cause', 'resume_ok', 'by')
out = {
    'probe_sha256': PROBE_SHA,
    'tested_sha256': {f: sha(repo / f) for f in ('scripts/rint_r_chain.py', 'scripts/rint_first_result.py')},
    'probe_rc': p.returncode,
    'probe_tail': (p.stdout.strip().splitlines() or [''])[-1][:400],
    'results': {'ours': [ours['passed'], ours['total']], 'codex': [theirs['passed'], theirs['total']], 'rows_differ': diff},
    'candidate_fix_identical': cand_o == cand_t,
    'residual_fields_equal_candidate_table': {json.dumps(r['rc']): r['fields'] == cand_by_rc.get(json.dumps(r['rc'])) for r in resid_o},
    'residual_orphan': {json.dumps(r['rc']): r['orphan'] for r in resid_o},
    'residual_orphan_codex': {json.dumps(r['rc']): r['orphan'] for r in resid_t},
    'integration': {r['label']: {'result': {k: r['result'].get(k) for k in keys}, 'next_resume_problem': (r['next_resume_problem'] or [None])[0]}
                    for r in integ_o},
    'integration_codex': {r['label']: {'result': {k: r['result'].get(k) for k in keys}, 'next_resume_problem': (r['next_resume_problem'] or [None])[0]}
                          for r in integ_t},
}
OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
print(json.dumps({k: out[k] for k in ('probe_rc', 'probe_tail', 'candidate_fix_identical')}, ensure_ascii=False))
print('rows differ:', [d['name'] for d in diff])
