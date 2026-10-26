from pathlib import Path
import json
import subprocess
import hashlib

base = Path(__file__).resolve().parent
repo = base.parents[1] / 'snapshot' / 'repo'
source = repo / 'scripts' / 'resume_ckpt.sh'
source_text = source.read_text(encoding='utf-8')
lines = source_text.splitlines()
# Only exact helper definitions, status wait, G1-G3 and final submission condition.
# No original preparation/launch code is run.
functions = '\n'.join(lines[10:17])
wait_block = '\n'.join(lines[66:69])
gates = '\n'.join(lines[69:95])
submit = '\n'.join(lines[106:109])
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
results = []
for name, (state, trial) in cases.items():
    work = base / 'probe_fixtures' / name
    (work / 'work').mkdir(parents=True, exist_ok=True)
    (work / 'old').mkdir(exist_ok=True)
    (work / 'logs').mkdir(exist_ok=True)
    (work / 'work' / 'log.liggghts.ins1').write_text(original, encoding='utf-8')
    (work / 'work' / 'mode_r56.txt').write_text('settling 1 restart_kg50_d07_b40/restart_settling_1.bin\n', encoding='utf-8')
    (work / 'logs' / 'output_kg50_d07_b40_r56t_7001.out').write_text(trial, encoding='utf-8')
    script = """#!/usr/bin/env bash
# SAFE SYNTHETIC HARNESS: no scheduler executable is called.
export PATH='/usr/bin:/bin'
C=kg50_d07_b40; SFX=r56; SUF=ins1; J=7001
L=$PWD; W=$PWD/work; S=$PWD/old; REP=$PWD/report.md
capture=$PWD/stub_main_submission.txt
: > "$capture"
: > "$REP"
sacct(){ printf '%s\\n' "$terminal_state"; }
squeue(){ return 0; }
sbatch(){ printf '%s\\n' "$*" >> "$capture"; printf '9001\\n'; }
sleep(){ printf 'unexpected sleep\\n' >&2; exit 91; }
terminal_state=""" + state + '\n' + functions + '\n' + wait_block + '\n' + gates + '\n' + submit + r'''
printf 'State=%s G1=%s G2=%s G3=%s F=%s F2=%s MainSubmitStubCalls=%s\n' "$terminal_state" "$G1" "$G2" "$G3" "$F" "$F2" "$(wc -l < "$capture")"
printf 'G2T=%s\nG3T=%s\n' "$G2T" "$G3T"
'''
    (work / 'probe.sh').write_text(script, encoding='utf-8', newline='\n')
    proc = subprocess.run([r'C:\Program Files\Git\bin\bash.exe', '--noprofile', '--norc', 'probe.sh'], cwd=work, capture_output=True, text=True, encoding='utf-8')
    result = dict(case=name, terminal_state=state, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr, source_has_loop_footer='Loop time' in trial, trial_last_step=next((int(x.split()[0]) for x in reversed(trial.splitlines()) if x and x.split()[0].isdigit()), None))
    results.append(result)
    assert proc.returncode == 0, result
    expected_submit = name in {'nominal_completed','failed_setup_only','failed_after_first_regular'}
    assert ('MainSubmitStubCalls=1' in proc.stdout) == expected_submit, result

report = {
    'safety': 'Only extracted exact-source shell functions/control flow; sacct/squeue/sbatch/sleep are shell stubs. No simulation, MPI, WSL, cluster, network or real scheduler call.',
    'source': str(source),
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'extracted_source_lines': ['11-17','67-69','70-95','107-109'],
    'results': results
}
(base / 'resume_gate_probe_results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
