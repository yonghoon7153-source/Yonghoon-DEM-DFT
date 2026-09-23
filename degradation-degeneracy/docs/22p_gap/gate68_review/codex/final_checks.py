"""Final read-only identity audit plus the committed T1 entry, not a product fix."""
import contextlib, hashlib, importlib.util, io, json, os, pathlib, sys
from run_checks import HERE, REPO, BMS, DD, run, dump

out = HERE / 'final_checks'
out.mkdir(exist_ok=False)
short = pathlib.Path('C:/Users/Administrator/Documents/Codex/r68_20260924')
temp = pathlib.Path('C:/Users/Administrator/Documents/Codex/g68_20260924_outer')
temp.mkdir(exist_ok=False)
os.environ.update(TMP=str(temp), TEMP=str(temp), PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
spec = importlib.util.spec_from_file_location('reviewed_gate66_outer', short/'degradation-degeneracy/tests/test_gate66_defensive.py')
tm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tm)
observations = []
for name, extra in [('clean', {}), ('setup_only', {'PYTEST_ADDOPTS':'--setup-only'}), ('collect_only', {'PYTEST_ADDOPTS':'--collect-only'})]:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            tm.test_g66_08_the_premise_test_does_not_fail_on_an_inherited_env(extra)
        row = dict(case=name, env_extra=extra, returned_normally=True)
    except Exception as exc:
        row = dict(case=name, env_extra=extra, returned_normally=False, error=type(exc).__name__, message=str(exc))
    row['stdout']=buf.getvalue()
    observations.append(row)
dump(out/'COMMITTED_ENTRY_RESULTS.json', observations)

for name, rev, paths in [
    ('r17_unchanged_claim', 'fcb54da3', ['bms-balancing/bms_balancing','bms-balancing/reviews']),
    ('gate_unchanged_claim', 'a31be7a9', ['degradation-degeneracy']),
    ('r17_executable_unchanged', 'fcb54da3', ['bms-balancing/bms_balancing','bms-balancing/scripts/gc_partial.py','bms-balancing/scripts/width_report.py','bms-balancing/scripts/verify_run_receipt.py']),
    ('gate_executable_unchanged', 'a31be7a9', ['degradation-degeneracy',':!degradation-degeneracy/docs/22p_gap/GATE68_REQUEST.md'])]:
    run(name, ['git','diff','--quiet',rev,'HEAD','--',*paths], REPO)
for label, repo in [('long', REPO), ('short',short)]:
    run('status_after_'+label, ['git','status','--porcelain'], repo)
    run('head_after_'+label, ['git','rev-parse','HEAD'], repo)
run('registry_tracked', ['git','ls-files','degradation-degeneracy/results/_exec_class'],REPO)

selected = [
    'CLAUDE.md',
    'bms-balancing/reviews/R17_FOLLOWUP3_RESPONSE.md',
    'bms-balancing/scripts/gc_partial.py','bms-balancing/scripts/width_report.py',
    'bms-balancing/scripts/verify_run_receipt.py','bms-balancing/bms_balancing/schema.py',
    'bms-balancing/bms_balancing/verify.py','bms-balancing/tests/test_r17_followup3.py',
    'degradation-degeneracy/docs/22p_gap/GATE68_REQUEST.md',
    'degradation-degeneracy/docs/22p_gap/mutation_replay.py',
    'degradation-degeneracy/tests/test_gate64_defensive.py',
    'degradation-degeneracy/tests/test_gate65_defensive.py',
    'degradation-degeneracy/tests/test_gate66_defensive.py',
    'degradation-degeneracy/tests/test_gate67_defensive.py',
]
identities=[]
for rel in selected:
    b=(REPO/rel).read_bytes()
    dest=out/'source_snapshots'/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(b)
    other=short/rel
    identities.append(dict(path=rel,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),short_identical=other.read_bytes()==b))
dump(out/'SOURCE_IDENTITIES.json',identities)
dump(out/'ENVIRONMENT.json',dict(python=sys.version,executable=sys.executable,os_name=os.name,
    platform=sys.platform,head='a1979cdf5b9f04234b6a441150e161bd4f0a3ced',
    scope='Portable Windows review. No Linux native/full-suite/strict-smoke/main-run/COMSOL certification.'))
print(json.dumps(observations,ensure_ascii=False))
