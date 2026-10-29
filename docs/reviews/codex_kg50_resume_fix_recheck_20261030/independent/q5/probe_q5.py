"""Independent Q5/D2 review, pinned repository read-only; no Bash/DEM/SLURM.

Runs production Python functions. The sole adapter replaces G.static_check's
Bash launch with the byte-identical Python heredoc extracted from that wrapper.
No guard is disabled and no production file is modified. Synthetic data is
explicitly labelled and cannot establish real-run provenance.
"""
from pathlib import Path
import contextlib
import difflib
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent / 'repo'
TMP = OUT / 'tmp'
TMP.mkdir(exist_ok=True)
tempfile.tempdir = str(TMP)
sys.path.insert(0, str(ROOT / 'scripts'))
import kg50_q5_branches as G
import kg50_q5_verdict as V

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

wrapper = ROOT / 'scripts/resume_ckpt.sh'
wb = wrapper.read_bytes()
marker = b'deckcheck(){ python3 - "$@" <<\'PY\'\n'
embedded = wb.split(marker, 1)[1].split(b'\nPY\n', 1)[0] + b'\n'
CLI = OUT / 'pinned_embedded_cli.py'
CLI.write_bytes(embedded)

def python_static(main_path, deck_path, case, tool=None, ckpt=None, s0=G.S0):
    assert tool is None or Path(tool).resolve() == wrapper.resolve(), tool
    ckpt = ckpt or f'restart_{case}/restart_after_settling.bin'
    with tempfile.TemporaryDirectory(prefix='python_static_') as work:
        r = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(CLI), str(main_path), str(deck_path), ckpt, str(s0), work],
                           capture_output=True, text=True, encoding='utf-8', timeout=30)
    lines = r.stdout.splitlines()
    return dict(rc=r.returncode, problems=[x[4:] for x in lines if x.startswith('  ✗ ')],
                notes=[x[4:] for x in lines if x.startswith('  · ')], tool='scripts/resume_ckpt.sh',
                tool_sha256=sha(wb), stdout=r.stdout, stderr=r.stderr)

G.static_check = python_static
results = dict(scope='Production Python only; no Bash/AWK, scheduler, helper, DEM, WSL, or actual run',
               wrapper_sha256=sha(wb), embedded_python_sha256=sha(embedded),
               source_hashes={f: sha((ROOT / f).read_bytes()) for f in ['scripts/kg50_q5_branches.py', 'scripts/kg50_q5_verdict.py',
                            'docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md']},
               registration={'generator': G.registration_check(), 'verdict': V.registration_check()},
               cases={}, mutations={})

GEN = OUT / 'generated'
assert not GEN.exists(), 'Use a fresh evidence directory; existing artifacts are not overwritten'
manifests = {}
for case in ('kg50_d07_b50', 'kg50_d3_b50_s1'):
    for branch in G.CASES[case]['branches']:
        man = G.build_branch(case, branch, G.NP[branch], str(GEN))
        manifests[branch] = man
        folder = GEN / man['folder']
        results['cases']['W1_' + branch] = dict(verify=G.verify_folder(str(folder)),
            static=man['static_check'], runs=man['runs'], end_step=man['end_step'], dt=man['dt'])

case = 'kg50_d07_b50'
logpath = OUT / 'SYNTHETIC_main_w2.log'
logpath.write_text(G.synth_main_log(case, 712000, 820000), encoding='utf-8')
W2 = OUT / 'generated_w2_draft'
w2mans = {}
for branch in ('A', 'B', 'C', 'F'):
    man = G.build_branch(case, branch, G.NP[branch], str(W2), 'W2', main_log=str(logpath))
    w2mans[branch] = man
    folder = W2 / man['folder']
    try:
        V.read_branch(str(folder), branch)
        verdict_refusal = None
    except V.Refused as e:
        verdict_refusal = str(e)
    results['cases']['W2_' + branch] = dict(verify=G.verify_folder(str(folder)), static=man['static_check'],
        s0=man['s0'], runs=man['runs'], dt=man['dt'], end_step=man['end_step'], amendment=man['amendment'],
        operator_commands=man['operator_commands'], verdict_refusal=verdict_refusal)

# Independent explicit registration transformation: no generator edit/drop lists.
def independent_body(main, branch, window, n=None):
    case = 'kg50_d07_b50'
    ls = main.splitlines()
    drop = {50, *range(116,151), 167,170}
    if window == 'W1':
        drop |= set(range(214,258))
    else:
        drop |= {*range(172,198),213,*range(225,258)}
    edits = {49: f'read_restart restart_{case}/' + ('restart_after_settling.bin' if window=='W1' else f'restart_compress_{n}.bin'),
             165: 'restart 0'}
    if window == 'W2':
        edits[222]='restart 0'; edits[224]='run ' + ('600000' if branch=='B' else '300000')
    if branch == 'B':
        edits[43]='variable dt equal 5.0e-7'
        edits[203]=f'dump dmp_mesh all mesh/stl 10000 post_{case}/mesh_*.stl top_mesh'
        edits[212]='thermo 2000'
        if window == 'W1':
            edits.update({173:'thermo 2',174:'run 2',213:'run 400000'})
        else:
            edits[217]=f'dump dmp_atom all custom 100000 post_{case}/atom_*.liggghts id type x y z radius vx vy vz c_strs[1] c_strs[2] c_strs[3] c_ke'
    if branch == 'C':
        edits[208]='fix damp all viscous 0.5 scale 3 5.3696e-4'
    everya,everyc=(66667,200001) if window=='W1' else (10000,100000)
    atom=f'dump dq5a all custom {everya} post_{case}/q5atom_*.liggghts id type x y z radius vx vy vz'
    contact=f'dump dq5c all local {everyc} post_{case}/q5contact_*.liggghts '+' '.join(f'c_cpl[{i}]' for i in range(1,27))
    out=[]
    for i,raw in enumerate(ls,1):
        if i in drop: continue
        out.append((raw[:len(raw)-len(raw.lstrip())]+edits[i]) if i in edits else raw)
        if i==171: out += [atom,contact]
        if i==(213 if window=='W1' else 224): out += ['undump dq5a','undump dq5c']
    return '\n'.join(out)+'\n'

main_path = ROOT / G.CASES[case]['deck']
main_text = main_path.read_text(encoding='utf-8')
results['independent_registration_body']={}
for window,base,mans in [('W1',GEN,manifests),('W2',W2,w2mans)]:
    for br in ('A','B','C','F'):
        man=mans[br]
        text=(base/man['folder']/man['deck']['file']).read_text(encoding='utf-8')
        body=text.split('# ===== (q5 머리 끝) =====\n',1)[1]
        expected=independent_body(main_text, br, window, 800000)
        results['independent_registration_body'][window+'_'+br]=dict(equal=body==expected,
             independent_sha256=sha(expected.encode()), body_sha256=sha(body.encode()),
             delta=list(difflib.unified_diff(expected.splitlines(),body.splitlines()))[:20])

base_man=w2mans['A']; base_path=W2/base_man['folder']/base_man['deck']['file']
base_text=base_path.read_text(encoding='utf-8')
MUT = OUT / 'mutations'; MUT.mkdir()
mutators={
    'extra_velocity_before_run':lambda s:s.replace('run 300000\n','velocity all set 1.0 0.0 0.0\nrun 300000\n'),
    'damping_double':lambda s:s.replace('fix damp all viscous 0.5\n','fix damp all viscous 1.0\n'),
    'speed_double':lambda s:s.replace('variable press_speed equal 0.01\n','variable press_speed equal 0.02\n'),
    'early_variable_restore':lambda s:s.replace('fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}',
        'variable press_speed equal 0.02\nfix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}\nvariable press_speed equal 0.01'),
    'swap_damping_order':lambda s:s.replace('unfix damp\nfix damp all viscous 0.5','fix damp all viscous 0.5\nunfix damp'),
}
for name,mutator in mutators.items():
    changed=mutator(base_text); assert changed!=base_text,name
    fp=MUT/(name+'.liggghts'); fp.write_text(changed,encoding='utf-8')
    st=python_static(main_path,fp,case,ckpt=base_man['checkpoint']['rel_path'],s0=base_man['s0'])
    probs=G.verify_branch_deck(main_text,changed,case,'A','W2',800000)
    results['mutations'][name]=dict(static=st, static_identical_to_registered=st['rc']==1 and st['problems']==G.expected_static('W2',case,800000),
        allowlist_problems=probs)

# D2 raw receipt integrity and command schedule, direct from tar bytes.
d2=ROOT/'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942'
tgz=d2/'received_d2_resume_1028.tgz'
archive=[]
with tarfile.open(tgz) as t:
    for m in t.getmembers():
        b=t.extractfile(m).read()
        local=(d2.parent/m.name) if '/' not in m.name else (d2/Path(m.name).name)
        archive.append(dict(member=m.name,size=m.size,sha256=sha(b),local_equal=local.read_bytes()==b))
dm=d2/'input_kg50_d2_b50.liggghts'; dr=d2/'input_kg50_d2_b50_r4.liggghts'; dt=d2/'input_kg50_d2_b50_r4t.liggghts'
# For these concrete supplied decks, a simple independent parser joins '&' lines,
# strips comments outside quotes, and normalizes whitespace.
def cmds(text):
    out=[]; buf=''
    for line in text.splitlines():
        line=line.rstrip()
        if line.endswith('&'):buf+=line[:-1]+' ';continue
        line=buf+line;buf=''; q=None; acc=''
        for c in line:
            if c in '\"\'' and q==c:q=None
            elif c in '\"\'' and q is None:q=c
            elif c=='#' and q is None:break
            acc+=c
        acc=' '.join(acc.split())
        if acc:out.append(acc)
    return out
cm,cr,ct=(cmds(f.read_text(encoding='utf-8')) for f in (dm,dr,dt))
mi=cm.index('run 200000'); ri=cr.index('run 180000')
trial_runs=[int(c.split()[1]) for c in ct if c.startswith('run ')]
results['d2']=dict(archive_sha256=sha(tgz.read_bytes()),archive_size=tgz.stat().st_size,members=archive,
    main_sha256=sha(dm.read_bytes()),main_matches_registered=dm.read_bytes()==(ROOT/'docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50/input_kg50_d2_b50.liggghts').read_bytes(),
    command_counts=[len(cm),len(cr),len(ct)],suffix_equal=cm[mi+1:]==cr[ri+1:],
    run_commands_resume=[c for c in cr if c.startswith('run ')],trial_runs=trial_runs,
    trial_expected_end=20001+sum(trial_runs),remaining=1+200000-20001,
    new_prefix=[c for c in cr[:ri] if c not in cm],
    production_static=python_static(dm,dr,'kg50_d2_b50',ckpt='restart_kg50_d2_b50/restart_settling_20001.bin',s0=20001))

# Provenance diagnostic: the production reader checks expected command subsequence.
# Same exact generated W1 artifacts and synthetic outputs, with an additional
# state-changing command echoed immediately before the long run.
S=V.Synth(str(GEN),manifests)
roles=S.prepare('extra_runtime_command')
baseline=V.run(roles)
rp=Path(roles['A'])/'log.liggghts'
original=rp.read_text(encoding='utf-8')
replacement=original.replace('run 200000\n','velocity all set 1.0 0.0 0.0\nrun 200000\n')
assert replacement!=original
rp.write_text(replacement,encoding='utf-8')
try:
    modified=V.run(roles)
    provenance=dict(accepted=True, baseline_a=baseline['a'], baseline_b=baseline['b'],
                    modified_a=modified['a'],modified_b=modified['b'], repo_verify={r:x['repo_verify'] for r,x in modified['branches'].items()})
except V.Refused as e:
    provenance=dict(accepted=False, refusal=str(e))
results['extra_echo_provenance']=provenance

results['repo_sources_unchanged']={f:sha((ROOT/f).read_bytes())==h for f,h in results['source_hashes'].items()}
write_json(OUT/'results.json',results)
print(json.dumps({k:results[k] for k in ('wrapper_sha256','embedded_python_sha256','registration','independent_registration_body','extra_echo_provenance','repo_sources_unchanged')},ensure_ascii=False,indent=2))
print('W2 mutation summary:',json.dumps({k:dict(static_same=v['static_identical_to_registered'],allowlist_rejected=bool(v['allowlist_problems'])) for k,v in results['mutations'].items()},ensure_ascii=False))
print('D2: archive members',len(archive),'all equal',all(x['local_equal'] for x in archive),'production static rc',results['d2']['production_static']['rc'])
