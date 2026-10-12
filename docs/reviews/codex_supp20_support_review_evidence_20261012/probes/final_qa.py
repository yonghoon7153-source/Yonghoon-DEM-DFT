from pathlib import Path
import hashlib, importlib.metadata, json, os, platform, re, sys

R = Path(__file__).resolve().parents[1]
S = R / 'source'
def readable(p):
    return Path('\\\\?\\'+str(p.resolve())) if os.name == 'nt' else p
manifest = json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
problems = []
total = 0
expected = set()
for row in manifest['files']:
    p = readable(S/row['path'])
    expected.add(row['path'])
    if not p.is_file():
        problems.append({'path':row['path'], 'error':'missing'})
        continue
    raw = p.read_bytes()
    total += len(raw)
    observed = {'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest(),
                'sha':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}
    for key in observed:
        if observed[key] != row[key]:
            problems.append({'path':row['path'], 'key':key,
                             'expected':row[key], 'observed':observed[key]})
extra = sorted(p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()
               and p.relative_to(S).as_posix() not in expected
               and '__pycache__' not in p.parts and p.suffix != '.pyc')
versions = {}
for name in ['numpy','scipy','pandas','matplotlib']:
    try: versions[name] = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError: versions[name] = None
tests = {}
for p in sorted((R/'evidence').glob('run_*.json')):
    if p.name == 'run_final_qa.json': continue
    d = json.loads(p.read_text(encoding='utf8'))
    tests[d['name']] = {'rc':d['rc'], 'seconds':d['seconds']}
release = json.loads((R/'evidence/release_probe.json').read_text(encoding='utf8'))
checks = {
    'normal_build_27':release['baseline_build']['returned']['n_files'] == 27,
    'normal_check_empty':release['baseline_check']['returned'] == [],
    'different_fp_build_refuses':release['normal_build_different_fp']['error'] == 'ReleaseError',
    'inconsistent_root_check_accepts':release['different_fp_gate_original_cross_roots']['returned'] == [],
    'bound_root_check_refuses':len(release['different_fp_gate_matching_cross_root']['returned']) == 2,
    'missing_root_check_accepts':release['different_fp_gate_missing_cross_root']['returned'] == [],
    'supp_identity_missing_accepts':release['missing_supp_code_identity']['returned'] == [],
    'primary_identity_missing_refuses':len(release['missing_primary_code_identity']['returned']) > 0,
    'original194_bytes_unchanged':all(release['original194_projection_bytes'].values()),
    'three_probes_rc0':all(tests[n]['rc']==0 for n in ['runner_probe','design_probe','release_probe']),
}
reread_log=(R/'evidence/reread.log').read_text(encoding='utf8')
out = {'pin':manifest['pin'], 'base':manifest['base'],
       'source_files_verified':len(manifest['files']), 'source_bytes_verified':total,
       'source_integrity_problems':problems, 'source_extra_noncache_files':extra,
       'environment':{'python':sys.version, 'platform':platform.platform(), 'packages':versions},
       'final_results':tests, 'evidence_checks':checks,
       'reread_checkmark_count':reread_log.count('✓'),
       'production_code_modified':False,
       'production_campaign_executed':False}
(R/'evidence/final_qa.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
assert not problems
assert not extra
assert all(checks.values())
