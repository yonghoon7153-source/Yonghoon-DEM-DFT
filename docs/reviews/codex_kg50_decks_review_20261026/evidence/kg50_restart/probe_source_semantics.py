from pathlib import Path
import json, re, hashlib, math

base = Path(__file__).resolve().parent
repo = base.parents[1] / 'snapshot' / 'repo'
src = repo / 'scripts' / 'resume_ckpt.sh'
s = src.read_text(encoding='utf-8')
# Explicit source assertions guard the interpretation and line numbers.
checks = {
    'status_list_has_failed': "COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF|NODE_FAIL",
    'no_error_token_is_only_error_gate': '[ "$E" = 0 ]',
    'settling_no_dump_fallback': '[ $nc = 0 ] && [ "$M" = settling ] && G2T=',
    'no_shared_regular_row_passes': 'if [ -z "$F2" ]; then G3=1;',
    'main_submit_predicate': 'if [ $G1 = 1 ] && [ $G2 = 1 ] && [ $G3 = 1 ]; then',
}
for label, fragment in checks.items():
    assert fragment in s, (label, fragment)

def rows(text):
    h = None
    out = []
    for line in text.splitlines():
        words = line.split()
        if re.match(r'^ *Step +Atoms', line):
            h = words
            continue
        if h and len(words) == len(h) and re.fullmatch('[0-9]+', words[0]):
            out.append(dict(zip(h, words)))
    return out

def tl(step, text):
    result = []
    for row in rows(text):
        if int(row['Step']) == step:
            result = [(k,v) for k,v in row.items() if k not in ('CPU','pressMPa')]
    return result

def same(a,b,t):
    if len(a)<3 or len(a)!=len(b): return False
    for (p,v),(q,w) in zip(a,b):
        if p!=q: return False
        if not all(re.fullmatch(r'[-+]?[0-9.]+([eE][-+]?[0-9]+)?',x) for x in (v,w)): return False
        if p in ('Step','Atoms'):
            if float(v)!=float(w): return False
        elif abs(float(v)-float(w))>t*abs(float(v)) and abs(float(v)-float(w))>1e-12: return False
    return True

def regular(text):
    return {int(r['Step']) for r in rows(text) if 'CPU' in r and float(r['CPU'])>0}

def tr2(step,text):
    result={}
    for r in rows(text):
        if int(r['Step'])==step and float(r.get('CPU','0'))>0:
            result={k:v for k,v in r.items() if k!='CPU'}
    return result

def sane(a,b):
    if len(a)<3 or len(a)!=len(b): return False
    if float(a.get('Atoms','0'))!=float(b.get('Atoms','0')): return False
    k = 'pressMPa' if 'pressMPa' in a and float(a['pressMPa'])>1e-6 else 'KinEng'
    if k not in a: return False
    d=abs(float(a[k])-float(b.get(k,'0')))
    return not (d>0.05*abs(float(a[k])) and d>1e-12)

original = """Step Atoms KinEng CPU
1 312506 0.116 0
1000 312506 0.14 1
2000 312506 0.17 2
2001 312506 0.17003 2.001
Loop time of 2.001 on 1 procs for 2000 steps with 312506 atoms
"""
cases = {
    'nominal_completed': ('COMPLETED', original),
    'failed_setup_only': ('FAILED', 'Step Atoms KinEng CPU\n1 312506 0.116 0\nMPI process exited on signal 11\n'),
    'failed_after_first_regular': ('FAILED', 'Step Atoms KinEng CPU\n1 312506 0.116 0\n1000 312506 0.14 1\nMPI process exited on signal 11\n'),
    'wrong_first_regular_rejected': ('COMPLETED', original.replace('1000 312506 0.14 1', '1000 312506 0.28 1')),
    'liggghts_ERROR_rejected': ('FAILED', 'Step Atoms KinEng CPU\n1 312506 0.116 0\nERROR: test failure\n'),
}
out=[]
for name,(state,trial) in cases.items():
    # Original code only uses this terminal-state predicate to leave the wait.
    wait_breaks = any(t in state for t in ('COMPLETED','FAILED','CANCELLED','TIMEOUT','OUT_OF','NODE_FAIL'))
    f=int(rows(trial)[0]['Step']) if rows(trial) else None
    g1=f is not None and f==1 and 'ERROR' not in trial and same(tl(f,original),tl(f,trial),1e-6)
    g2=True  # exact source: M=settling, no original step-1 dumps => nc=0 leaves G2=1
    shared=sorted(n for n in regular(original)&regular(trial) if n>f)
    f2=shared[0] if shared else None
    g3=True if f2 is None else sane(tr2(f2,original),tr2(f2,trial))
    result=dict(case=name,state=state,wait_breaks=wait_breaks,G1=g1,G2=g2,G3=g3,F=f,F2=f2,original_regular_steps=sorted(regular(original)),trial_regular_steps=sorted(regular(trial)),loop_footer_present='Loop time' in trial,final_step=max(int(r['Step']) for r in rows(trial)),would_take_source_main_submission_branch=all((g1,g2,g3)))
    out.append(result)
    assert result['would_take_source_main_submission_branch'] == (name in ('nominal_completed','failed_setup_only','failed_after_first_regular'))

# Math reproduction of upstream TWO-template exact_number allocation.
# Source floors each n*w then gives the sole missing slot to template0 iff U <= remainder0.
up = (base/'upstream_src_fix_particledistribution_discrete.cpp').read_text(encoding='utf-8')
for fragment in ('parttogen[i] = static_cast<int>(static_cast<double>(ninsert) * distweight[i]);','r = random->uniform() * static_cast<double>(ninsert_gap);','parttogen[j]++;'):
    assert fragment in up
am_mass=4850*(4*math.pi/3)*(0.003**3)
se_mass=1640*(4*math.pi/3)*(0.00035**3)
p=(0.85/am_mass)/(0.85/am_mass+0.15/se_mass)
n=312506
local_sizes=[n//56+int(i<n%56) for i in range(56)]
rounding = {
    'N':n,'AM_number_fraction':p,'expected_AM':n*p,
    'NP1_AM_floor':math.floor(n*p),'NP1_AM_ceil':math.ceil(n*p),
    'NP56_local_sizes':sorted(set(local_sizes)),
    'NP56_all_local_floors_AM':sum(math.floor(x*p) for x in local_sizes),
    'NP56_all_local_ceils_AM':sum(math.ceil(x*p) for x in local_sizes),
    'explanation':'With two templates and total inserted, each local AM is floor(n_local*p) or ceil(n_local*p), selected by random remainder. E[N_AM]=sum(n_local*p) under uniform remainders. This is an algorithmic counterexample to a compulsory downward bias, not a reproduction of a specific PRNG seed or physical insertion.'
}
report={
 'method':'SOURCE-GUARDED PYTHON SEMANTIC REPRODUCTION; not executed Bash, AWK or LIGGGHTS.',
 'shell_execution_limit':'Exact extracted-source Bash harness was prepared but Git Bash failed before script execution with NtCreateDirectoryObject0xC0000022 in sandbox. No actual scheduler or simulation command executed.',
 'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'source_assertions':checks,'gate_cases':out,'two_template_rounding':rounding}
(base/'semantic_probe_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
