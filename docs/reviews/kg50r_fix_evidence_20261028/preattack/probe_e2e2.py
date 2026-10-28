#!/usr/bin/env python3
"""More e2e probes (fake SLURM from the worktree test module; read-only import).
usage: python3 -I probe_e2e2.py <tool.sh> [names...]"""
import os, sys
WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/kg50fix-1028'
sys.path.insert(0, os.path.join(WT, 'scripts'))
import test_resume_ckpt as T  # noqa: E402

tool = sys.argv[1]
only = set(sys.argv[2:])


def want(n):
    return not only or n in only


def show(name, r, extra=()):
    g = [l for l in r['rep'].splitlines() if l.startswith('- G0 시험') or '본 제출' in l or '거부' in l]
    print('== %-34s rc=%s trial=%d main=%d calls=%s' % (name, r['rc'], r['ntrial'], r['nmain'], r['calls']))
    for l in g[:8]:
        print('    ' + l[:220])
    if not r['trial']:
        for l in r['out'].splitlines():
            if '⛔' in l or '✗' in l:
                print('    out: ' + l.strip()[:220])
    for e in extra:
        print('    ' + e)


# (1) resume deck in the work folder changed between trial submission and main submission (sbatch hook edits it)
if want('deck_changed_after_trial'):
    old = T.STUB_SBATCH
    T.STUB_SBATCH = old.replace('[ -n "$FAKE_TOUCH_HELPER" ] && echo "# 시험 제출 뒤 바뀜" >> "$FAKE_TOUCH_HELPER"',
                                '[ -n "$FAKE_EDIT_DECK" ] && sed -i "s/^run 180000$/run 900000/" "$FAKE_EDIT_DECK"')
    assert T.STUB_SBATCH != old
    try:
        ctx = T.make_root()
        try:
            W = os.path.join(ctx['L'], T.C)
            r = T.invoke(ctx, tool, T.res_good(), T.trial_log('ok'),
                         env_more={'FAKE_EDIT_DECK': os.path.join(W, 'input_%s_%s.liggghts' % (T.C, T.SFX))})
            d = r['w_decks'].get('input_%s_%s.liggghts' % (T.C, T.SFX), b'').decode()
            att = [k for k in r['att'] if k.endswith('input_%s_%s.liggghts' % (T.C, T.SFX))]
            show('deck_changed_after_trial', r, ['W deck first long run now: %s' % [l for l in d.splitlines() if l.startswith('run 9')][:1],
                                                 'attempt copy has run 180000: %s' % (att and 'run 180000' in r['att'][att[0]])])
        finally:
            import shutil
            shutil.rmtree(ctx['tmp'], ignore_errors=True)
    finally:
        T.STUB_SBATCH = old

# (2) runner changed between trial and main (e.g. -in points elsewhere)
if want('runner_changed_after_trial'):
    old = T.STUB_SBATCH
    T.STUB_SBATCH = old.replace('[ -n "$FAKE_TOUCH_HELPER" ] && echo "# 시험 제출 뒤 바뀜" >> "$FAKE_TOUCH_HELPER"',
                                '[ -n "$FAKE_EDIT_RUN" ] && sed -i "s/-in input_[A-Za-z0-9_]*\\.liggghts/-in other.liggghts/" "$FAKE_EDIT_RUN"')
    try:
        ctx = T.make_root()
        try:
            W = os.path.join(ctx['L'], T.C)
            rn = os.path.join(W, 'run_%s_%s.sh' % (T.C, T.SFX))
            r = T.invoke(ctx, tool, T.res_good(), T.trial_log('ok'), env_more={'FAKE_EDIT_RUN': rn})
            show('runner_changed_after_trial', r, ['main runner -in line: %s' % [l for l in open(rn) if 'lmp_mpi' in l]])
        finally:
            import shutil
            shutil.rmtree(ctx['tmp'], ignore_errors=True)
    finally:
        T.STUB_SBATCH = old

# (3) a running main job of the same case under a custom suffix (earlier call used -x foo) -> busy check misses it
if want('custom_suffix_busy'):
    r = T.run_case1(tool, 'good', 'ok', squeue='%s_foo' % T.C)
    show('custom_suffix_busy (squeue: C_foo)', r)

# (4) same case under two spellings
if want('two_spellings'):
    r = T.run_case1(tool, 'good', 'ok', cases=[T.C, './' + T.C])
    show('two_spellings C ./C', r)
