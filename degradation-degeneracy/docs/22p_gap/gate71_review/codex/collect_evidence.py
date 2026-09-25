"""Data-only evidence collection and before/after preservation check."""
from pathlib import Path
import hashlib, json, subprocess
OUT = Path(__file__).resolve().parent
WT = Path('C:/Users/Administrator/Documents/Codex/g71_20260925')
DD = WT/'degradation-degeneracy'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args):
    return subprocess.check_output(['git','-c',f'safe.directory={WT.as_posix()}','-C',str(WT),*args])
excerpts = {
    'tools/preserve.py': [(4947,5038),(7380,7407),(7563,7755),(7758,7885),(8175,8221),(8269,8295)],
    'docs/22p_gap/make_receipt.py': [(135,230),(245,305),(330,358)],
    'tests/test_gate70_defensive.py': [(302,419)],
    'tests/conftest.py': [(14,104),(140,154),(258,337)],
    'run.sh': [(49,58),(196,206),(220,225),(345,376),(396,414),(487,501),(516,575)],
    'src/grid.py': [(591,612)],
    'src/fitting.py': [(1518,1545)],
    'docs/22p_gap/GATE71_REQUEST.md': [(1,45),(57,98),(101,174)],
}
dest = OUT/'source_excerpts'
dest.mkdir(exist_ok=True)
manifest = {}
for rel, spans in excerpts.items():
    raw = (DD/rel).read_bytes()
    lines = raw.decode('utf-8').splitlines()
    out = [f'SOURCE: {rel}', f'SOURCE_SHA256: {sha(raw)}', 'COMMIT: 4505b70c6e63453e0424239cac7d48488fee022a', '']
    for lo, hi in spans:
        out.append(f'### {lo}-{hi}')
        out.extend(f'{i}: {lines[i-1]}' for i in range(lo, min(hi,len(lines))+1))
        out.append('')
    name = rel.replace('/','__')+'.txt'
    (dest/name).write_text('\n'.join(out)+'\n',encoding='utf-8')
    manifest[rel] = {'source_bytes':len(raw),'source_sha256':sha(raw),'excerpt':name}
(OUT/'EXCERPT_IDENTITIES.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before = json.loads((OUT/'SOURCE_BEFORE.json').read_text(encoding='utf-8'))
after = {}
for rel in before:
    p = WT/rel
    after[rel] = {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} if p.is_file() else None
changed = [k for k in before if before[k]!=after[k]]
state = git('status','--porcelain=v1','-uall').decode()
e10_changes = git('diff','--name-only','0e6348be9ec80919e0f84ae246294cb6336e9545',
                  '4505b70c6e63453e0424239cac7d48488fee022a','--','degradation-degeneracy').decode().splitlines()
result = {'tracked_DD_files':len(before), 'changed':changed, 'git_status_after':state,
          'e10_evidence_head_to_request_changed_paths':e10_changes,
          'operational_registry_writes':0,'operational_ledger_writes':0,'COMSOL_calls':0,
          'main_grid_fit_runs':0,'restores':0,'class_changes':0,'full_pytest_or_smoke_reruns':0,
          'reviewer_selected_AST_reader_script_rc':0,
          'reader_script_tool_chunk':'0f2f90',
          'identity_tool_chunk':'959347','identity_tool_rc':0,
          'limits':'Tracks 2459 DD files in the detached review checkout, not every file on the producer PC. Reviewer output/fixtures and git checkout/fetch writes are outside product state.',
          'diagnostic_failures_retained_in_report':[
              'Identity check first stopped on missing promisor Git blob/network denial (rc 1); after turn network permission, same read-only identity check completed rc 0.',
              'Several lookup-only shell calls named non-existent guessed files; no product run occurred.'
          ]}
assert not changed and not state
(OUT/'PRESERVATION_AFTER.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
