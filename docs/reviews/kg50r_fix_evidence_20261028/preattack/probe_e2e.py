#!/usr/bin/env python3
"""End-to-end probes with the test module's fake SLURM harness (read-only import of the worktree test file).
usage: python3 -I probe_e2e.py <tool.sh> [names...]"""
import os, sys
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T  # noqa: E402

tool = sys.argv[1]
only = set(sys.argv[2:])
C = T.C


def show(name, r):
    g = [l for l in r['rep'].splitlines() if l.startswith('- G') or '본 제출' in l or '거부' in l]
    print('== %-28s rc=%s trial=%d main=%d' % (name, r['rc'], r['ntrial'], r['nmain']))
    for l in g[:12]:
        print('    ' + l[:230])
    if not r['trial']:
        for l in r['out'].splitlines():
            if '⛔' in l or '✗' in l:
                print('    out: ' + l.strip()[:230])


def want(n):
    return not only or n in only


TMPL_ANCHOR = 'read_restart %s\n' % T.CKPT
# A: variable redefinition around ${dt} immediate substitution (after read_restart) -> actual dt 2e-6
if want('A_dt'):
    g = T.res_good()
    assert g.count(TMPL_ANCHOR) == 1
    bad = g.replace(TMPL_ANCHOR, TMPL_ANCHOR + 'variable dt      equal 2.0e-6\ntimestep        ${dt}\nvariable dt      equal 1.0e-6\n')
    show('A_dt (new full check)', T.run_case1(tool, None, 'ok', res_text=bad))

# NaN in the G3 comparison line (21000 KE = nan) -- last line finite
if want('NaN_G3'):
    rows = T.T_OK[:]
    rows[2] = rows[2].replace('0.0955', '   nan')
    show('NaN_G3 trial 21000 KE=nan', T.run_case1(tool, 'good', None, trial_text='\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n'))
if want('NaN_G3_orig'):
    orig = T.ORIG_LOG.replace('   21000   312506         0.0950', '   21000   312506            nan')
    assert orig != T.ORIG_LOG
    show('NaN_G3 orig 21000 KE=nan', T.run_case1(tool, 'good', 'ok', orig_log=orig))
if want('INF_G3'):
    rows = T.T_OK[:]
    rows[2] = rows[2].replace('0.0955', '   inf')
    show('INF_G3 trial 21000 KE=inf', T.run_case1(tool, 'good', None, trial_text='\n'.join(['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)'] + rows) + '\n'))

# main sbatch prints a non-numeric message and exits 1 -> report?
if want('MAIN_SBATCH_TEXT'):
    stub = T.STUB_SBATCH.replace('  *) echo "main $f" >> "$CAPTURE"; echo $((9000 + $(grep -c \'^main\' "$CAPTURE")));;',
                                 '  *) echo "main $f" >> "$CAPTURE"; echo "sbatch: error: QOSMaxSubmitJobPerUserLimit"; exit 1;;')
    assert stub != T.STUB_SBATCH
    old = T.STUB_SBATCH
    T.STUB_SBATCH = stub
    try:
        r = T.run_case1(tool, 'good', 'ok')
    finally:
        T.STUB_SBATCH = old
    show('MAIN_SBATCH_TEXT', r)
    print('    attempt files:', sorted(k for k in r['att'] if 'main_job' in k or 'result' in k))
    for k in sorted(r['att']):
        if k.endswith('main_job.txt') or k.endswith('result.txt'):
            print('    %s = %r' % (k, r['att'][k][:200]))
