#!/usr/bin/env python3
"""Independent scratch mutations of verified marker guards, observed by actual arm CLI."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--expanded',type=Path,required=True)
ap.add_argument('--single',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
a=ap.parse_args(); source=a.source.resolve(); out=a.output.resolve(); out.mkdir(parents=True)
rel=Path('docs/data/ps45_unload_20261009/ul_reader.py')
original=(source/rel).read_text(); source_sha=hashlib.sha256((source/rel).read_bytes()).hexdigest()

def once(text,old,new):
    assert text.count(old)==1,(old,text.count(old))
    return text.replace(old,new,1)

def no_raw(text):
    return once(text,'    if os.path.isfile(event_path):','    if False:')

def no_auth_poison(text):
    return once(text,'auth, apr = ([], []) if pr or marker_pr else _resume_auth(d, events)',
                'auth, apr = ([], []) if pr else _resume_auth(d, events)')

def normalize_event(text):
    start,end=text.index('def read_run('),text.index('def parent_sums(')
    body=no_raw(text[start:end])
    body=once(body,'    for r in ev or []:\n','    for r in ev or []:\n        r["event"] = r["event"].strip()\n')
    return text[:start]+body+text[end:]

def key_filter_first(text):
    return once(text,"            if any(c in ln for c in '\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'):",
                "            if ln.lstrip(' \\t').startswith('resume_from=') and any(c in ln for c in '\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'):")

def drop_nel(text):
    start,end=text.index('def _resume_auth('),text.index('def _supersede(')
    body=once(text[start:end],"'\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'","'\\v\\f\\x1c\\x1d\\x1e\\u2028\\u2029'")
    return text[:start]+body+text[end:]

def normalize_lines(text):
    start,end=text.index('def _resume_auth('),text.index('def _supersede(')
    body=once(text[start:end],".read().split('\\n'):",'.read().splitlines():')
    return text[:start]+body+text[end:]

mutants=[
    ('remove_raw_event_scan',no_raw,a.single/'2028_prefix'),
    ('do_not_poison_auth',no_auth_poison,a.expanded/'event_00a0_suffix_1p49'),
    ('normalize_event_instead_of_reject',normalize_event,a.single/'00a0_suffix'),
    ('filter_manifest_key_first',key_filter_first,a.expanded/'manifest_2028_between_text_key'),
    ('omit_nel_separator',drop_nel,a.expanded/'manifest_0085_between_text_key'),
    ('normalize_manifest_lines',normalize_lines,a.expanded/'manifest_2028_after_key'),
]
child='''
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,sys.argv[1]);import ul_reader as u
d=Path(sys.argv[2]);r=u.read_run(str(d));print(json.dumps({'auth':r['resume_auth'],'dropped':r['n_superseded_rows'],'problems':r['problems']}))
'''
results=[]
for name,mutate,fixture in mutants:
    root=out/name; repo=root/'source'; root.mkdir();repo.mkdir()
    for relative in (Path('docs/data/ps45_unload_20261009'),
                     Path('docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz'),
                     Path('scripts/plane_load_share.py')):
        target=repo/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if (source/relative).is_dir():
            shutil.copytree(source/relative,target)
        else:
            shutil.copyfile(source/relative,target)
    (repo/rel).write_text(mutate(original))
    case=root/'case';shutil.copytree(fixture.resolve(),case)
    d=case/'ps_7_3_r45/UT';kit=(repo/rel).parent
    files=[d/f'ul_{n}.csv' for n in ('events','windows','steps')]
    hashes={str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    read=subprocess.run([sys.executable,'-I','-B','-c',child,str(kit),str(d)],capture_output=True,text=True,timeout=60)
    assert read.returncode==0,read.stderr
    observed=json.loads(read.stdout)
    cli=subprocess.run([sys.executable,'-I','-B',str(kit/'ul_reader.py'),'arm',str(case),'ps_7_3_r45','UT'],capture_output=True,text=True,timeout=60)
    (root/'cli.log').write_text(cli.stdout+cli.stderr)
    verdict=json.loads((d/'arm_verdict.json').read_text())
    unchanged=hashes=={str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    expected=(observed['auth']==[] and observed['dropped']==0 and bool(observed['problems'])
              and verdict['primary_status']=='UNIDENTIFIED' and verdict['rho_pct'] is None and verdict['rank_eligible'] is False)
    result={'mutation':name,'source_verified_sha256':source_sha,'mutant_sha256':hashlib.sha256((repo/rel).read_bytes()).hexdigest(),
            'fixture_name':fixture.name,'observed_read_run':observed,'primary_status':verdict['primary_status'],
            'rho_pct':verdict['rho_pct'],'rank_eligible':verdict['rank_eligible'],'csv_unchanged':unchanged,
            'cli_rc':cli.returncode,'detected':not expected and unchanged and cli.returncode==0}
    results.append(result)
report={'source_reader_sha256':source_sha,'scope':'Deliberately altered scratch source; not a certified consumer',
        'mutants':results,'detected':sum(r['detected'] for r in results),'count':len(results),'physical_runs':0}
(out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('detected','count')}))
raise SystemExit(0 if all(r['detected'] for r in results) else 1)
