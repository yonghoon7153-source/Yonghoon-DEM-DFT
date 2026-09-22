import json,pathlib,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
HERE=pathlib.Path(__file__).resolve().parent
j=json.loads((HERE/'full_failures.json').read_text(encoding='utf-8'))
groups=collections.defaultdict(list)
for f in j['failures']:
    text=f['trace'];name=f['test']
    if 'fcntl' in f['tags']: k='fcntl-mentioned-in-failure-trace'
    elif 'missing-executable-or-file' in f['tags'] and 'bash' in text:k='bash-command-not-found'
    elif 'WinError 1314' in text:k='symlink-privilege'
    elif 'Invalid argument' in text and 'a -> b.csv' in text:k='windows-invalid-filename'
    elif name.endswith(('test_git_state_can_exclude_the_artifact_being_rewritten','test_r5_11_git_provenance_classifies_quoted_non_ascii_paths')):k='path-separator-assertion'
    else:k='unresolved-do-not-ascribe-to-environment'
    groups[k].append(name)
out=dict(counts={k:len(v) for k,v in groups.items()},groups=groups,
         note='Observed trace categorization; not independent causal proof for every fcntl-linked failure. Unresolved cases are not passes.')
(HERE/'FULL_TEST_TRIAGE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
for f in j['failures']:
    if any(n in f['test'] for n in ['e11_10','e11_17','concurrent_profiles']):print(f['test'],f['trace'][-2500:])
