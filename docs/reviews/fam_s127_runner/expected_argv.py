#!/usr/bin/env python3
"""Expected argv of the four FAM s12-7 arms, built from the registration text itself.

Two sources in the prereg doc are parsed independently and must agree:
  (1) the registration block  (COMMON / COMMON7 + four `$PY -u ...` lines, s12-7 "런 넷 · argv")
  (2) the dry-run lines 19-1..19-4 (hand-expanded by the authors, `--frames 1` appended)
Then the s12-7-2 amendment is applied: corner arms `--platen-mach 0.01` -> `0.0099999`.

usage: expected_argv.py PREREG PY OUT OUTDIR   ->  OUTDIR/<arm>.argv (NUL separated), table on stdout
"""
import os
import shlex
import sys

ARMS = ['confirm_fb', 'corner_fb', 'corner_fa', 'corner_f0']
AMEND_FROM, AMEND_TO = '0.01', '0.0099999'
AMEND_LINE = '`--platen-mach 0.01` → **`--platen-mach 0.0099999`**'


def arm_of(tokens):
    base = os.path.basename(tokens[tokens.index('--save-metrics') + 1])
    assert base.startswith('fam_s127_') and base.endswith('.json'), base
    return base[len('fam_s127_'):-len('.json')]


def amend(tokens):
    if not any('case15' in t for t in tokens):
        return list(tokens)
    idx = [i for i, t in enumerate(tokens) if t == '--platen-mach']
    assert len(idx) == 1, idx
    assert tokens[idx[0] + 1] == AMEND_FROM, tokens[idx[0] + 1]
    out = list(tokens)
    out[idx[0] + 1] = AMEND_TO
    return out


def from_block(lines, py, out):
    head = next(i for i, l in enumerate(lines) if l.startswith('**런 넷 · argv'))
    b0 = next(i for i in range(head, len(lines)) if lines[i].strip() == '```bash')
    b1 = next(i for i in range(b0 + 1, len(lines)) if lines[i].strip() == '```')
    env, cmds, cur = {}, [], ''
    for raw in lines[b0 + 1:b1]:
        s = raw.rstrip('\n')
        if s.lstrip().startswith('#'):
            continue
        for k in ('COMMON7', 'COMMON'):
            if s.startswith(k + '="') and s.endswith('"'):
                env[k] = s[len(k) + 2:-1]
                break
        else:
            if cur or s.startswith('$PY'):
                if s.endswith('\\'):
                    cur += s[:-1] + ' '
                else:
                    cmds.append(cur + s)
                    cur = ''
    assert set(env) == {'COMMON', 'COMMON7'}, env
    assert len(cmds) == 4, cmds
    res = {}
    for c in cmds:
        c = c.replace('$COMMON7', env['COMMON7']).replace('$COMMON', env['COMMON'])
        t = shlex.split(c)
        k = t.index('>')
        argv, redir = t[:k], t[k:]
        assert argv[0] == '$PY', argv[0]
        argv[0] = py
        argv = [a.replace('<OUT>', out) for a in argv]
        arm = arm_of(argv)
        assert redir == ['>', '<OUT>/fam_s127_%s.log' % arm, '2>&1'], redir
        res[arm] = amend(argv)
    return res, env, (head + 1, b0 + 1, b1 + 1)


def from_dryrun(lines, py, out):
    key = 'cd ~/fam-wt && ~/fam-mpm310/bin/python -u scripts/mpm3d_compaction.py'
    res = {}
    for i, raw in enumerate(lines):
        if key not in raw:
            continue
        seg = raw.strip().split('cd ~/fam-wt && ', 1)[1]
        t = shlex.split(seg)
        k = t.index('>')
        argv = t[:k]
        assert argv[0] == '~/fam-mpm310/bin/python'
        argv[0] = py
        argv = [a.replace('~/fam_s127/dryrun/', out + '/') for a in argv]
        assert argv[-2:] == ['--frames', '1'], argv[-2:]
        argv = argv[:-2]
        arm = arm_of(argv)
        assert t[k + 1] == '~/fam_s127/dryrun/fam_s127_%s.log' % arm and t[k + 2] == '2>&1;', t[k:k + 3]
        res[arm] = amend(argv)
    return res


def main():
    prereg, py, out, outdir = sys.argv[1:5]
    with open(prereg, encoding='utf-8') as fh:
        lines = fh.readlines()
    blk, env, where = from_block(lines, py, out)
    dry = from_dryrun(lines, py, out)
    assert sorted(blk) == sorted(ARMS), sorted(blk)
    assert sorted(dry) == sorted(ARMS), sorted(dry)
    for a in ARMS:
        assert blk[a] == dry[a], (a, blk[a], dry[a])
    assert any(AMEND_LINE in l for l in lines), 'amendment line not found in prereg'
    # the only registered difference between COMMON and COMMON7 is --frames 400 -> 3000
    c, c7 = env['COMMON'].split(), env['COMMON7'].split()
    diff = [(x, y) for x, y in zip(c, c7) if x != y]
    assert len(c) == len(c7) and diff == [('400', '3000')], diff
    os.makedirs(outdir, exist_ok=True)
    for a in ARMS:
        with open(os.path.join(outdir, a + '.argv'), 'wb') as fh:
            fh.write(b''.join(x.encode() + b'\0' for x in blk[a]))
        print('%-10s %s' % (a, ' '.join(shlex.quote(x) for x in blk[a])))
    print('# block lines (heading, ```bash, ```) = %s · dry-run cross-check = equal for %d arms' % (where, len(ARMS)))


if __name__ == '__main__':
    main()
