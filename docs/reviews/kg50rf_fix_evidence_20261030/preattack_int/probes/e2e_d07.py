#!/usr/bin/env python3
"""PAI probe — real D0.7 (v3 50x50) decks end to end through resume_ckpt.sh with the repo's fake SLURM harness.

Layout mirrors the real command (-r ~/dem_test · helper ~/dem_test/dem_restart.py in the same root):
  ~/dem_test/kg50_d07_b50.ins1/  main deck · insertion deck · the two original runners · log.liggghts (synthetic) ·
                                  restart_kg50_d07_b50/restart_settling_20001.bin (64 zero bytes) · post_kg50_d07_b50/
  fake dem_restart.py = the harness's (copies FAKE_RES as the resume deck · writes FAKE_RUNNER as the helper runner)
  FAKE_RES = d07_raw_r56.liggghts (make_d07_resume.py) · FAKE_RUNNER = d07_helper_runner_r56.sh (D2 r4 form)
Scenes (argv[2:] picks; default all):
  T      -T -n 56 -s ins1 -r ~/dem_test kg50_d07_b50
  M      -n 56 -s ins1 -r ~/dem_test -x r56 -t 2000 -A <tool> -H <helper> kg50_d07_b50   (fresh root)
Each scene prints rc · sbatch calls · what the fake mpirun saw (cwd · -in · sha256 of what it read) against the
sha256 of the deck the tool checked (= the attempt folder copy) · G0–G3 · decision lines · attempt files.
usage: python3 e2e_d07.py <scratch> [T] [M]
"""
import hashlib, importlib.util, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
spec = importlib.util.spec_from_file_location('trc', os.path.join(REPO, 'scripts/test_resume_ckpt.py'))
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
D07 = os.path.join(REPO, 'docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50')
C = 'kg50_d07_b50'
CK = 'restart_%s/restart_settling_20001.bin' % C


def sha(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def rb(p):
    with open(p, 'rb') as f:
        return f.read()


def make_ctx(sp):
    tmp = tempfile.mkdtemp(prefix='pai_e2e_', dir=sp)
    home, stub = os.path.join(tmp, 'home'), os.path.join(tmp, 'bin')
    L = os.path.join(home, 'dem_test')
    S = os.path.join(L, '%s.ins1' % C)
    for d in (os.path.join(S, 'restart_' + C), os.path.join(S, 'post_' + C), stub):
        os.makedirs(d)
    for n in ('input_%s.liggghts' % C, 'input_%s_insert.liggghts' % C, 'run_%s.sh' % C, 'run_%s_insert.sh' % C):
        shutil.copy(os.path.join(D07, n), os.path.join(S, n))
    with open(os.path.join(S, 'log.liggghts'), 'w') as f:
        f.write(t.ORIG_LOG)
    with open(os.path.join(S, CK), 'wb') as f:
        f.write(b'\x00' * 64)
    for name, body in (('sbatch', t.STUB_SBATCH), ('sacct', t.STUB_SACCT), ('squeue', t.STUB_SQUEUE), ('sleep', '#!/bin/sh\nexit 0\n'),
                       ('mpirun', t.STUB_MPIRUN), ('conda', '#!/bin/sh\nexit 0\n')):
        p = os.path.join(stub, name)
        with open(p, 'w') as f:
            f.write(body)
        os.chmod(p, 0o755)
    open(os.path.join(home, '.bashrc'), 'w').close()
    helper = os.path.join(L, 'dem_restart.py')
    with open(helper, 'w') as f:
        f.write(t.FAKE_DEM_RESTART)
    cap = os.path.join(tmp, 'capture.txt')
    open(cap, 'w').close()
    return dict(tmp=tmp, L=L, home=home, stub=stub, S=S, cap=cap, helper=helper)


def scene(sp, name, extra, approve, trial_kind='ok', res_edit=None):
    t.C, t.SFX, t.NP = C, 'r56', 56
    ctx = make_ctx(sp)
    res = rb(os.path.join(sp, 'd07', 'd07_raw_r56.liggghts')).decode()
    if res_edit:
        res = res_edit(ctx, res)
    runner = os.path.join(sp, 'd07', 'd07_helper_runner_r56.sh')
    r = t.invoke(ctx, t.SCRIPT, res, t.trial_log(trial_kind), extra=extra, ckpt=CK, approve=approve,
                 env_more={'FAKE_RUNNER': runner}, root=ctx['L'])
    W = os.path.join(ctx['L'], C)
    att = sorted(d for d in os.listdir(W) if d.startswith('attempt_')) if os.path.isdir(W) else []
    AD = os.path.join(W, att[-1]) if att else None
    print('=' * 100)
    print('scene %s · rc %s · sbatch calls %s' % (name, r['rc'], r['calls']))
    checked = {}
    if AD:
        for n in ('input_%s_r56.liggghts' % C, 'input_%s_r56t.liggghts' % C):
            if os.path.isfile(os.path.join(AD, n)):
                checked[n] = sha(os.path.join(AD, n))
        print('attempt files:', sorted(os.listdir(AD)))
        for n in ('runner_check.txt', 'main_inputs.sha256', 'result.txt', 'reject.txt'):
            p = os.path.join(AD, n)
            if os.path.isfile(p):
                print('--- %s\n%s' % (n, open(p, encoding='utf-8').read().rstrip()))
    print('checked deck sha256 (attempt copies):', json.dumps(checked, indent=1))
    for m in r['mp']:
        dk = m['args'][m['args'].index('-in') + 1] if '-in' in m['args'] else None
        print('mpirun %s job %s cwd %s -in %s read sha256 %s = checked? %s' % (
            m['kind'], m['job'], m['cwd'], dk, m['in_sha'], m['in_sha'] in checked.values()))
    for l in r['out'].splitlines():
        if any(k in l for k in ('✗', '⛔', '▶', '재개 덱 정적 대조:', '헬퍼 러너', '시험 덱 (10-28', '본 제출')):
            print('OUT', l[:400])
    for l in r['rep'].splitlines():
        if l.startswith('- G') or '본 제출' in l or '신원 줄' in l or '시험만' in l:
            print('REP', l[:400])
    if os.path.isdir(W):
        for n in sorted(os.listdir(W)):
            if n.startswith('run_') and n.endswith('.sh'):
                print('--- work folder runner %s (sha256 %s)\n%s' % (n, sha(os.path.join(W, n))[:16], open(os.path.join(W, n)).read().rstrip()))
    return r, ctx


def main():
    sp = sys.argv[1]
    which = sys.argv[2:] or ['T', 'M']
    keep = os.environ.get('PAI_KEEP')
    for w in which:
        if w == 'T':
            r, ctx = scene(sp, 'T (-T · real D0.7 command)', ('-T',), None)
        elif w == 'M':
            r, ctx = scene(sp, 'M (main · -x r56 -t 2000 -A -H)', ('-x', 'r56', '-t', '2000'), 'auto')
        elif w == 'MX':
            # PAI-01: same main command · the resume deck's post-checkpoint plate mesh reads another case's STL by absolute path
            def edit(ctx, res):
                other = os.path.join(ctx['home'], 'dem_test', 'kg50_d2_b50', 'plate_kg50_d2_b50.stl')
                os.makedirs(os.path.dirname(other), exist_ok=True)
                with open(other, 'w') as f:
                    f.write('solid plate\nendsolid plate\n')
                old = 'fix top_mesh all mesh/surface/stress file plate_kg50_d07_b50.stl type 1'
                assert res.count(old) == 1
                return res.replace(old, 'fix top_mesh all mesh/surface/stress file %s type 1' % other)
            r, ctx = scene(sp, 'MX (main · plate mesh = other case STL by absolute path)', ('-x', 'r56', '-t', '2000'), 'auto',
                           res_edit=edit)
            W = os.path.join(ctx['L'], C)
            for n in sorted(os.listdir(W)):
                if n.startswith('attempt_'):
                    print('deckcheck notes:', [l for l in open(os.path.join(W, n, 'deckcheck_r56.txt'), encoding='utf-8')
                                               if '판 메시' in l or '정적 대조:' in l])
            print('main runner -in deck contains other-case plate:',
                  any('kg50_d2_b50/plate_kg50_d2_b50.stl' in l for l in open(os.path.join(W, 'input_%s_r56.liggghts' % C))))
        elif w == 'SUF':
            # PAI-08: -s is not validated (unlike -x · -n) — '-s ins1/../decoy' makes S = <root>/kg50_d07_b50.ins1/../decoy = <root>/decoy
            t.C, t.SFX, t.NP = C, 'r56', 56
            ctx = make_ctx(sp)
            decoy = os.path.join(ctx['L'], 'decoy')
            shutil.copytree(ctx['S'], decoy, symlinks=True)
            with open(os.path.join(decoy, 'DECOY_MARKER'), 'w') as f:
                f.write('this folder is not kg50_d07_b50.ins1\n')
            raw = rb(os.path.join(sp, 'd07', 'd07_raw_r56.liggghts')).decode()
            runner = os.path.join(sp, 'd07', 'd07_helper_runner_r56.sh')
            r = t.invoke(ctx, t.SCRIPT, raw, t.trial_log('ok'), extra=('-T',), ckpt=CK, approve=None, suf='ins1/../decoy',
                         env_more={'FAKE_RUNNER': runner}, root=ctx['L'])
            W = os.path.join(ctx['L'], C)
            print('=' * 100)
            print('-s ins1/../decoy · rc %d · sbatch calls %s' % (r['rc'], [c.split()[0] for c in r['calls']]))
            print('work folder copied from the decoy (DECOY_MARKER present):', os.path.isfile(os.path.join(W, 'DECOY_MARKER')))
            print('report head:', [l for l in r['rep'].splitlines() if l.startswith('명령') or '멈춘 폴더' in l][:3])
        elif w == 'TM2':
            # PAI-02: reviewed -T, then the stopped folder's main deck changes (press_speed 0.01 -> 0.02, compression phase only) and the
            #   helper regenerates the resume deck from it; the main call printed by -T (-A tool -H helper) still runs a new trial + main.
            t.C, t.SFX, t.NP = C, 'r56', 56
            ctx = make_ctx(sp)
            raw = rb(os.path.join(sp, 'd07', 'd07_raw_r56.liggghts')).decode()
            runner = os.path.join(sp, 'd07', 'd07_helper_runner_r56.sh')
            r1 = t.invoke(ctx, t.SCRIPT, raw, t.trial_log('ok'), extra=('-T',), ckpt=CK, approve=None,
                          env_more={'FAKE_RUNNER': runner}, root=ctx['L'])
            W = os.path.join(ctx['L'], C)
            a1 = [d for d in os.listdir(W) if d.startswith('attempt_')][0]
            rec1 = open(os.path.join(W, a1, 'main_inputs.sha256')).read().split('\n')[0][:64]
            f1 = t.sha256f(os.path.join(W, a1, 'main_inputs.sha256'))
            cmdline = [l for l in r1['rep'].splitlines() if '본 제출 명령' in l]
            old, new = 'variable press_speed equal 0.01', 'variable press_speed equal 0.02'
            if os.environ.get('PAI_NOCHANGE'):
                new = old                       # control: nothing changes between -T and main
            mp = os.path.join(ctx['S'], 'input_%s.liggghts' % C)
            mt = open(mp, encoding='utf-8').read()
            assert mt.count(old) == 1 and raw.count(old) == 1
            open(mp, 'w', encoding='utf-8').write(mt.replace(old, new))
            r2 = t.invoke(ctx, t.SCRIPT, raw.replace(old, new), t.trial_log('ok'), extra=('-x', 'r56', '-t', '2000'), ckpt=CK,
                          approve='auto', env_more={'FAKE_RUNNER': runner}, root=ctx['L'])
            a2 = [d for d in os.listdir(W) if d.startswith('attempt_')][0]
            rec2 = open(os.path.join(W, a2, 'main_inputs.sha256')).read().split('\n')[0][:64]
            print('=' * 100)
            print('-T rc %d calls %s · printed main command present: %s' % (r1['rc'], [c.split()[0] for c in r1['calls']], bool(cmdline)))
            print('-T receipt resume deck sha256 %s' % rec1)
            print('main rc %d calls %s · receipt resume deck sha256 %s · same as -T? %s' % (
                r2['rc'], [c.split()[0] for c in r2['calls']], rec2, rec1 == rec2))
            print('main deck run reads press_speed 0.02:', any('press_speed equal 0.02' in l for l in open(os.path.join(W, 'input_%s_r56.liggghts' % C))))
            f2 = t.sha256f(os.path.join(W, a2, 'main_inputs.sha256'))
            print('whole receipt sha256 -T %s · main %s · identical %s' % (f1[:16], f2[:16], f1 == f2))
            print('main report decision:', [l for l in r2['rep'].splitlines() if '본 제출 job' in l or '본 제출 안 함' in l])
        else:
            continue
        if not keep:
            shutil.rmtree(ctx['tmp'], ignore_errors=True)
        else:
            print('kept', ctx['tmp'])


if __name__ == '__main__':
    main()
