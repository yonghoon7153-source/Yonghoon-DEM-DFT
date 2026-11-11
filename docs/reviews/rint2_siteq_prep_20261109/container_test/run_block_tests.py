#!/usr/bin/env python3
"""Container tests for the site-qualification short block (templates of 2026-11-11).

Run ONLY inside a fresh PID namespace -- the script refuses unless it is PID 1:

    unshare -pf --mount-proc --kill-child python3 -I -B docs/reviews/rint2_siteq_prep_20261109/container_test/run_block_tests.py \\
        --work <new empty folder outside the repository> [--summary <file>] [--only S1,N2,...]

What it needs: root (chown / ACL cases), git, bash, nohup, setsid (util-linux, with -c), and a local Python 3.8 with
numpy 1.24.4 + scipy 1.10.1 (default: `uv python find 3.8`; no network is used -- `scripts/setup_kgy_py38.sh` installs it).
What it touches: reads the repository with `git archive` / `git show` only; writes only under --work and to --summary.
Signals: it never kills a process it did not start itself.  A terminal hang-up is made by closing a pty master; a direct
child that overruns its time limit is left running and reported (the namespace ends with this script).
Fake world per case: a new HOME, a fake origin repository (scripts/ + .gitignore + the probe from --src-rev, three commits
on the two branch names the templates fetch), a base clone like the site checkouts, and a venv made with
--system-site-packages from the Python 3.8 (no pip).
"""
import argparse
import glob
import hashlib
import json
import os
import re
import select
import shutil
import struct
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PREP = os.path.dirname(HERE)
PROBE_REL = 'docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py'
TMPL_REL = 'docs/reviews/rint2_siteq_prep_20261109/container_test/short_block.tmpl'
NEW_BRANCH = 'claude/stoic-knuth-NObVQ'
OLD_BRANCH = 'claude/sdcp-dem-manuscript-si-pqwtv8'
OLD_TMPL_REV = 'db86ce9b9'
OLD_TMPL_SHA = 'bc117ba6f7bdb3d6b21223e82fc5c8cf6d2654fa11310e09a75bb92f30ab40ac'
OLD_PROBE_SHA = 'a490b9adc3eeb7468b051b32bdaa0110879b71322a3a2cfb3b723505a3df8588'
KGY_UNIT = ('3.8', '1.24.4', '1.10.1')
OTHER_UID = 43219          # a uid with no account (number must never appear in the mode list)
NAMED_UID = 1              # an existing account (its name must never appear in the mode list)
FIXED_DATE = '2026-11-11T00:00:00+00:00'
CALL_PREFIX = 'python3 -I -B -u siteq_probe.py '
LAST_LINE = re.compile(r'^\[siteq\] rc (\d+) \(0 = no FAIL and no ERROR\) - send back \S+/siteq_result\.json and the sha256 line$')
RC_LINE = re.compile(r'^rc=(\d+) end_utc=\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ( stop=(.+))?$')
CLASSES_OWNER = ('self', 'root', 'other')
CLASSES_GROUP = ('self-primary', 'self-member', 'root', 'other')
DIRECT = set()             # pids this script started itself (the only ones it may wait on by pid)
OUT_LINES = []
A = None
W0 = None                  # the work root (masked as <WORK> in the summary)
MASKS = []                 # (path, replacement), longest first


# ------------------------------------------------------------------ small helpers
def say(s=''):
    OUT_LINES.append(s)
    print(mask(s), flush=True)


def mask(s):
    for p, r in MASKS:
        s = s.replace(p, r)
    return s


def add_mask(path, rep):
    for p in {os.path.abspath(path), os.path.realpath(path)}:
        MASKS.append((p, rep))
    MASKS.sort(key=lambda x: -len(x[0]))


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, 'rb') as f:
        return sha_bytes(f.read())


def rd(p, default=None):
    try:
        with open(p, encoding='utf-8', errors='replace') as f:
            return f.read()
    except OSError:
        return default


def wr(p, s, mode=None):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    if mode is not None:
        os.chmod(p, mode)


def git(*args, cwd=None, env=None, check=True):
    e = dict(os.environ) if env is None else env
    e.update(GIT_AUTHOR_DATE=FIXED_DATE, GIT_COMMITTER_DATE=FIXED_DATE)
    r = subprocess.run(['git', '-c', 'commit.gpgsign=false', '-c', 'user.name=t', '-c', 'user.email=t@t'] + list(args),
                       cwd=cwd, env=e, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and r.returncode:
        raise RuntimeError('git %s failed: %s' % (' '.join(args), r.stderr.decode('utf-8', 'replace')[-400:]))
    return r.stdout.decode('utf-8', 'replace').strip()


def env_for(home):
    return {'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': home, 'LANG': 'C.UTF-8',
            'TERM': 'xterm', 'SHELL': '/bin/bash'}


def reap():
    """Collect zombies that were re-parented to this PID 1 (never a direct child: those are waited on by Popen)."""
    for e in os.listdir('/proc'):
        if not e.isdigit():
            continue
        pid = int(e)
        if pid == 1 or pid in DIRECT:
            continue
        try:
            with open('/proc/%d/stat' % pid, 'rb') as f:
                rest = f.read().rsplit(b')', 1)[1].split()
        except (OSError, IndexError):
            continue
        if rest[0] == b'Z' and int(rest[1]) == 1:
            try:
                os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                pass


def wait_p(p, timeout):
    t = time.time() + timeout
    while time.time() < t:
        rc = p.poll()
        if rc is not None:
            return rc
        reap()
        time.sleep(0.1)
    return None


def wait_for(fn, timeout, step=0.2):
    t = time.time() + timeout
    while time.time() < t:
        reap()
        v = fn()
        if v:
            return v
        time.sleep(step)
    return None


def spawn(argv, cwd, env, log):
    with open(log, 'wb') as lf:
        p = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=lf, stderr=subprocess.STDOUT)
    DIRECT.add(p.pid)
    return p


class Pty:
    """A pty whose slave is the controlling terminal of the started process (setsid -c).  hangup() closes the master."""

    def __init__(self, argv, cwd, env, log):
        self.master, slave = os.openpty()
        self.p = subprocess.Popen(argv, cwd=cwd, env=env, stdin=slave, stdout=slave, stderr=slave)
        DIRECT.add(self.p.pid)
        os.close(slave)
        self.log, self.buf, self.stop = log, bytearray(), threading.Event()
        self.t = threading.Thread(target=self._read, daemon=True)
        self.t.start()

    def _read(self):
        while not self.stop.is_set():
            r, _, _ = select.select([self.master], [], [], 0.1)
            if not r:
                continue
            try:
                b = os.read(self.master, 4096)
            except OSError:
                break
            if not b:
                break
            self.buf += b

    def text(self):
        return bytes(self.buf).decode('utf-8', 'replace')

    def write(self, data):
        while data:
            n = os.write(self.master, data[:512])
            data = data[n:]
            time.sleep(0.005)

    def hangup(self):
        self.stop.set()
        self.t.join()
        os.close(self.master)
        with open(self.log, 'wb') as f:
            f.write(bytes(self.buf))


def proc_alive(pid):
    try:
        with open('/proc/%d/stat' % pid, 'rb') as f:
            return f.read().rsplit(b')', 1)[1].split()[0] not in (b'Z', b'X')
    except (OSError, IndexError):
        return False


def leftovers():
    n = 0
    for e in os.listdir('/proc'):
        if e.isdigit() and int(e) not in (1, os.getpid()) and proc_alive(int(e)):
            n += 1
    return n


# ------------------------------------------------------------------ fake world
def set_acl(path, name, entries):
    """entries = [(tag, perm, id or None)]  (Linux posix_acl xattr v2; ids None = undefined)."""
    b = struct.pack('<I', 2) + b''.join(struct.pack('<HHI', t, p, 0xFFFFFFFF if i is None else i) for t, p, i in entries)
    os.setxattr(path, name, b)


def build_origin(work, repo, rev):
    src = os.path.join(work, 'origin_src')
    os.makedirs(src)
    tar = subprocess.run(['git', '-C', repo, 'archive', '--format=tar', rev, '.gitignore', 'scripts', PROBE_REL],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    subprocess.run(['tar', '-x', '-C', src], input=tar, check=True)
    origin = os.path.join(work, 'origin')
    os.makedirs(origin)
    git('init', '-q', '-b', OLD_BRANCH, cwd=origin)
    shutil.copy2(os.path.join(src, '.gitignore'), os.path.join(origin, '.gitignore'))
    shutil.copytree(os.path.join(src, 'scripts'), os.path.join(origin, 'scripts'))
    git('add', '-A', cwd=origin)
    git('commit', '-q', '-m', 'O: scripts only (stands for the frozen branch)', cwd=origin)
    O = git('rev-parse', 'HEAD', cwd=origin)
    git('checkout', '-q', '-b', NEW_BRANCH, cwd=origin)
    dst = os.path.join(origin, PROBE_REL)
    os.makedirs(os.path.dirname(dst))
    shutil.copy2(os.path.join(src, PROBE_REL), dst)
    git('add', '-A', cwd=origin)
    git('commit', '-q', '-m', 'X: + probe (the PIN of the normal cases)', cwd=origin)
    X = git('rev-parse', 'HEAD', cwd=origin)
    probe = open(dst, 'rb').read()
    changed = probe.replace(b'(prepared 2026-11-09)', b'(prepared 2026-11-10)', 1)
    if changed == probe or not len(changed) == len(probe):
        raise RuntimeError('cannot make the one-byte probe change')
    with open(dst, 'wb') as f:
        f.write(changed)
    git('commit', '-q', '-am', 'Z: probe one byte changed', cwd=origin)
    Z = git('rev-parse', 'HEAD', cwd=origin)
    return {'origin': origin, 'O': O, 'X': X, 'Z': Z, 'probe_sha': sha_bytes(probe), 'probe_sha_z': sha_bytes(changed)}


def make_venvs(work, py38, py311):
    out = {}
    for tag, py in (('38', py38), ('311', py311)):
        d = os.path.join(work, 'venv' + tag)
        subprocess.run([py, '-m', 'venv', '--system-site-packages', '--without-pip', d], check=True,
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        r = subprocess.run([os.path.join(d, 'bin', 'python3'), '-I', '-c',
                            'import sys, numpy, scipy; print("%d.%d" % sys.version_info[:2], numpy.__version__, '
                            'scipy.__version__, int(sys.prefix != sys.base_prefix))'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        out[tag] = (d, tuple(r.stdout.decode().split()))
    return out


def make_plan(home):
    sd = os.path.join(home, 'sdcp')
    os.makedirs(sd)
    os.chmod(sd, 0o775)                                            # group-writable folder (like kgy 11-10)
    sc = os.path.join(sd, 'scripts')
    os.makedirs(sc)
    os.chown(sc, OTHER_UID, OTHER_UID)
    os.chmod(sc, 0o777)                                            # 777 folder, owned by an unnamed uid
    set_acl(sc, 'system.posix_acl_default', [(0x01, 7, None), (0x02, 5, OTHER_UID), (0x04, 5, None), (0x10, 5, None),
                                             (0x20, 5, None)])     # default ACL with 5 entries
    pf = os.path.join(sd, 'ca1_plan.json')
    wr(pf, '{}\n')
    os.chown(pf, NAMED_UID, NAMED_UID)
    os.chmod(pf, 0o664)
    set_acl(pf, 'system.posix_acl_access', [(0x01, 6, None), (0x02, 4, OTHER_UID), (0x04, 6, None), (0x10, 6, None),
                                            (0x20, 4, None)])      # access ACL: 2 entries beyond the base three


def group_others(gid):
    """Independent re-count for the expectation (same rule as the template: group entry members + /etc/passwd primary)."""
    import grp
    import pwd
    try:
        names = set(grp.getgrgid(gid).gr_mem)
    except KeyError:
        names = set()
    for ln in open('/etc/passwd', encoding='utf-8', errors='replace'):
        x = ln.split(':')
        if len(x) > 3 and x[3] == str(gid):
            names.add(x[0])
    names.discard(pwd.getpwuid(os.geteuid()).pw_name)
    return str(len(names))


class Case:
    def __init__(self, name, title):
        self.name, self.title = name, title
        self.dir = os.path.join(W0, 'cases', name)
        os.makedirs(self.dir)
        self.home = os.path.join(self.dir, 'home')
        os.makedirs(self.home)
        add_mask(self.home, '~')
        self.asserts = []
        self.notes = []

    def ok(self, key, cond, detail=''):
        self.asserts.append((key, bool(cond), detail))
        return bool(cond)

    def failed(self):
        return [k for k, c, _ in self.asserts if not c]


def home_setup(c, kind='kgy', venv='38', base='single'):
    if venv:
        os.symlink(VENVS[venv][0], os.path.join(c.home, 'dem-venv'))
    b = os.path.join(c.home, 'dem-ca1-89fc4' if kind == 'kgy' else 'Yonghoon-DEM-DFT')
    args = ['clone', '-q', '--no-checkout', '--no-local']
    if base == 'single':
        args += ['--single-branch', '--branch', OLD_BRANCH]
    git(*(args + [ORIGIN['origin'], b]))
    if kind == 'kgy':
        make_plan(c.home)
    return b


def vals(kind, pin):
    if kind == 'kgy':
        return {'PIN': pin, 'MACHINE': 'kgy', 'BASE': '$HOME/dem-ca1-89fc4', 'PLAN': '$HOME/sdcp',
                'LEDGER': '$HOME/sdcp/ca1_ledger', 'OUTBASE': '$HOME/sdcp/scripts', 'PLANFILE': '$HOME/sdcp/ca1_plan.json'}
    return {'PIN': pin, 'MACHINE': 'gabia', 'BASE': '$HOME/Yonghoon-DEM-DFT', 'PLAN': '', 'LEDGER': '', 'OUTBASE': '',
            'PLANFILE': ''}


def fill(t, v):
    for k, x in v.items():
        if x is not None:
            t = t.replace('@@%s@@' % k, x)
    return t


def listing(home):
    return sorted(os.listdir(home))


def run_block(c, text, umask='0022', how='plain', timeout=600):
    """how = plain (bash file) | stdin-i (bash -i < file).  Returns (rc, screen text)."""
    f = os.path.join(c.dir, 'block.sh')
    wr(f, text)
    log = os.path.join(c.dir, 'screen.log')
    inner = 'exec bash "$1"' if how == 'plain' else 'exec bash -i < "$1"'
    p = spawn(['sh', '-c', 'umask %s; %s' % (umask, inner), 'sh', f], c.home, env_for(c.home), log)
    rc = wait_p(p, timeout)
    if rc is None:
        c.notes.append('outer block did not end within %d s (left running)' % timeout)
    return rc, rd(log, '')


def one(pattern):
    g = glob.glob(pattern)
    return g[0] if len(g) == 1 else None


def find_out(home, machine, tag=''):
    """The block's result folder: rint_siteq_<machine>_<UTC date><tag> (exact form, so the two forms never mix)."""
    rx = re.compile(r'^rint_siteq_%s_\d{8}%s$' % (re.escape(machine), re.escape(tag)))
    g = [os.path.join(home, x) for x in os.listdir(home) if rx.match(x)]
    return g[0] if len(g) == 1 else None


def parse_kv(line):
    d, path = {}, None
    if ' path=' in line:
        line, path = line.split(' path=', 1)
    for tok in line.split():
        if '=' in tok:
            k, v = tok.split('=', 1)
            d[k] = v
    if path is not None:
        d['path'] = path
    return d


def read_modes(p):
    rows = {}
    for ln in (rd(p, '') or '').splitlines():
        if ln.startswith('tag='):
            d = parse_kv(ln)
            rows[d['tag']] = d
    return rows


# ------------------------------------------------------------------ shared checks
def check_full(c, rc, screen, pin, machine, umask, sighup, out=None, outer_rc_expected=0, fail_ids=(), expect_modes=True,
               strict_last=True, tag=''):
    """A block that ran the probe to the end.  strict_last: the rc line must be the last screen line (an interactive
    'bash -i < file' adds its own prompt and 'exit' after it, so there the last [siteq] line is taken)."""
    out = out or find_out(c.home, machine, tag)
    c.ok('outer_rc', rc == outer_rc_expected, 'rc %s' % rc)
    lines = [x for x in screen.splitlines() if x.strip()]
    if not strict_last:
        lines = [x for x in lines if x.startswith('[siteq] ')]
    m = LAST_LINE.match(lines[-1]) if lines else None
    c.ok('last_line', m and int(m.group(1)) == outer_rc_expected, lines[-1] if lines else '(no screen)')
    res = json.loads(rd(os.path.join(out, 'siteq_result.json'), 'null') or 'null') if out else None
    if not c.ok('result_json', isinstance(res, dict), 'siteq_result.json present'):
        return None
    bad = sorted(x['id'] for x in res['checks'] if x['status'] in ('FAIL', 'ERROR'))
    warn = sorted(x['id'] for x in res['checks'] if x['status'] == 'WARN')
    c.ok('fail_error_ids', bad == sorted(fail_ids), 'FAIL/ERROR %s' % bad)
    c.ok('warn_only_c28', set(warn) <= {'C28'}, 'WARN %s' % warn)
    c.ok('probe_and_pin', res.get('probe_sha256') == ORIGIN['probe_sha'] and res.get('pin') == pin, 'probe %s pin %s' % (
        str(res.get('probe_sha256'))[:12], str(res.get('pin'))[:12]))
    rcl = (rd(os.path.join(out, 'siteq_block_rc.txt'), '') or '').splitlines()
    mm = RC_LINE.match(rcl[0]) if len(rcl) == 1 else None
    c.ok('rc_file', mm and int(mm.group(1)) == outer_rc_expected and mm.group(3) is None, ' | '.join(rcl) or '(no rc file)')
    env = parse_kv((rd(os.path.join(out, 'siteq_block_env.txt'), '') or '').strip())
    c18 = next((x for x in res['checks'] if x['id'] == 'C18'), {}).get('data', {})
    try:
        e0, e1, u18, f18 = int(env['umask_start'], 8), int(env['umask_probe'], 8), int(c18['umask'], 8), int(c18['new_file_mode'], 8)
        same = e1 == u18 == int(umask[1], 8) and e0 == int(umask[0], 8) and f18 == 0o666 & ~u18
    except (KeyError, ValueError, TypeError):
        same = False
    c.ok('umask_record', same, 'env %s | C18 umask %s new file %s' % (env, c18.get('umask'), c18.get('new_file_mode')))
    c.ok('sighup_record', env.get('sighup_ignored') == sighup, 'sighup_ignored %s' % env.get('sighup_ignored'))
    wt = os.path.join(c.home, 'dem-siteq-%s%s' % (pin[:9], tag))
    st = git('status', '--porcelain', '--untracked-files=normal', cwd=wt, check=False)
    c.ok('worktree_clean', st == '' and git('rev-parse', 'HEAD', cwd=wt) == pin, 'status %r' % st[:80])
    stray = [p for p in glob.glob(os.path.join(c.home, '**', 'nohup.out'), recursive=True)]
    c.ok('no_nohup_out', not stray, 'nohup.out %s' % stray)
    c26 = next((x for x in res['checks'] if x['id'] == 'C26'), {})
    rows = c26.get('data') or {}
    plan = dict((k, v) for k, v in rows.items() if k.startswith('plan_dir:'))
    outdev = (rows.get('out:%s' % res.get('out')) or {}).get('st_dev')
    if machine == 'kgy':
        okc = (c26.get('status') == 'PASS' and len(plan) == 1 and 'plan dirs missing' not in (c26.get('detail') or '') and
               all(v.get('exists') is True and v.get('writable') is True and v.get('st_dev') == outdev for v in plan.values()))
    else:
        okc = c26.get('status') == 'PASS' and not plan
    c.ok('c26_plan_dir', okc, '%s %s' % (c26.get('status'), (c26.get('detail') or '')[:120]))
    c.counts = res.get('counts')
    c.ids = [x['id'] for x in res['checks']]
    c.notes.append('probe %s s' % res.get('seconds'))
    if expect_modes:
        check_modes(c, out, machine, int(umask[1], 8))
    return res


def check_modes(c, out, machine, umask_probe):
    rows = read_modes(os.path.join(out, 'siteq_block_modes.txt'))
    text = rd(os.path.join(out, 'siteq_block_modes.txt'), '') or ''
    outname = os.path.basename(out)
    dmode = '%04o' % (0o777 & ~umask_probe)
    if machine == 'kgy':
        exp = {'plan': dict(kind='dir', mode='0775', group_write='yes', other_write='no', acl_extra='0', acl_default='0',
                            link='no', path='~/sdcp'),
               'ledger': dict(kind='missing', path='~/sdcp/ca1_ledger'),
               'outbase': dict(kind='dir', mode='0777', group_write='yes', other_write='yes', acl_extra='0', acl_default='5',
                               path='~/sdcp/scripts'),
               'planfile': dict(kind='file', mode='0664', group_write='yes', other_write='no', acl_extra='2', acl_default='-',
                                path='~/sdcp/ca1_plan.json'),
               'siteq_out': dict(kind='dir', mode=dmode, other_write='no', acl_extra='0', path='~/' + outname)}
        cls = {'plan': ('self', 'self-primary', group_others(os.getegid())), 'outbase': ('other', 'other', group_others(OTHER_UID)),
               'planfile': ('other', 'other', group_others(NAMED_UID)), 'siteq_out': ('self', 'self-primary', group_others(os.getegid()))}
    else:
        exp = {t: dict(kind='not-given') for t in ('plan', 'ledger', 'outbase', 'planfile')}
        exp['siteq_out'] = dict(kind='dir', mode=dmode, other_write='no', acl_extra='0', path='~/' + outname)
        cls = {'siteq_out': ('self', 'self-primary', group_others(os.getegid()))}
    diffs = []
    for tag, want in exp.items():
        got = rows.get(tag, {})
        for k, v in want.items():
            if not got.get(k) == v:
                diffs.append('%s.%s=%s (want %s)' % (tag, k, got.get(k), v))
    c.ok('modes_rows', not diffs and set(rows) == set(exp), '; '.join(diffs) or 'rows %s' % sorted(rows))
    bad = []
    for tag, (o, g, n) in cls.items():
        got = rows.get(tag, {})
        if not (got.get('owner') == o and got.get('group') == g and got.get('group_others') == n):
            bad.append('%s owner=%s group=%s others=%s (want %s %s %s)' % (tag, got.get('owner'), got.get('group'),
                                                                          got.get('group_others'), o, g, n))
    for tag, got in rows.items():
        if got.get('kind') in ('dir', 'file', 'other') and not (got.get('owner') in CLASSES_OWNER and got.get('group') in CLASSES_GROUP):
            bad.append('%s owner/group not a class' % tag)
    import pwd
    named = pwd.getpwuid(NAMED_UID).pw_name
    for needle in (named, str(OTHER_UID), c.home, os.path.realpath(c.home), W0):
        if needle in text:
            bad.append('mode list contains %r' % mask(needle))
    c.ok('modes_no_names', not bad, '; '.join(bad) or 'owner/group are classes; no names, uid numbers or home path')
    if c.name in ('S1', 'S1b', 'S2', 'N1'):
        c.notes.extend('mode list: ' + ln for ln in text.splitlines() if ln.startswith('tag='))


def check_stop(c, rc, screen, msg_re, home_before=None, rc_file=None):
    c.ok('outer_rc', rc == 2, 'rc %s' % rc)
    stops = [x for x in screen.splitlines() if x.startswith('[siteq] STOP: ')]
    c.ok('stop_message', len(stops) == 1 and re.search(msg_re, stops[0]), stops[0] if stops else '(no STOP line)')
    if home_before is not None:
        c.ok('home_unchanged', listing(c.home) == home_before, 'home %s' % listing(c.home))
    if rc_file is not None:
        out, want = rc_file
        rcl = (rd(os.path.join(out, 'siteq_block_rc.txt'), '') or '').splitlines() if out else []
        if want is None:
            c.ok('rc_file', not rcl, 'rc file %s' % (rcl or 'absent (as wanted)'))
        else:
            mm = RC_LINE.match(rcl[0]) if len(rcl) == 1 else None
            c.ok('rc_file', mm and int(mm.group(1)) == 2 and mm.group(3) and re.search(want, mm.group(3)), ' | '.join(rcl) or '(no rc file)')


# ------------------------------------------------------------------ cases
def t0_static():
    c = Case('T0', 'static: templates, hashes, shared body')
    short = rd(os.path.join(HERE, 'short_block.tmpl'))
    nohup = rd(os.path.join(HERE, 'short_block_nohup.tmpl'))
    sums = dict((ln.split()[1], ln.split()[0]) for ln in (rd(os.path.join(PREP, 'SHA256SUMS'), '') or '').splitlines() if ln.strip())
    psha = sha_file(os.path.join(PREP, 'tools', 'siteq_probe.py'))
    m = re.search(r'^PROBE_SHA=([0-9a-f]{64})$', short, re.M)
    c.ok('probe_sha_line', m and m.group(1) == psha == sums.get('tools/siteq_probe.py') == ORIGIN['probe_sha'],
         'PROBE_SHA %s tool %s SHA256SUMS %s' % (m.group(1)[:12] if m else None, psha[:12], str(sums.get('tools/siteq_probe.py'))[:12]))
    fetch = re.findall(r'fetch -q origin (\S+)', short)
    c.ok('fetch_branch', fetch == [NEW_BRANCH], 'fetch %s' % fetch)
    for name, t in (('short', short), ('nohup', nohup)):
        c.ok(name + '_ascii_no_bang_no_tab', t.isascii() and '!' not in t and '\t' not in t, '%d lines' % len(t.splitlines()))
        c.ok(name + '_slots', all(('@@%s@@' % k) in t for k in ('PIN', 'MACHINE', 'BASE', 'PLAN', 'LEDGER', 'OUTBASE', 'PLANFILE')))
        c.ok(name + '_no_address', not re.search(r'\b\d{1,3}(\.\d{1,3}){3}\b|\bssh\b|\bscp\b|\bsudo\b', t))
    sl = short.split('\n')
    inner = sl[1:-2]
    nl = nohup.split('\n')
    i0 = [k for k, x in enumerate(nl) if x.startswith("cat > \"$L/block.sh\" <<'SITEQ_BODY' || {")]
    i0 = i0[0] if len(i0) == 1 else -1
    i1 = nl.index('SITEQ_BODY')
    c.ok('nohup_body_equals_short', sl[0] == "bash <<'SITEQ'" and sl[-2] == 'SITEQ' and nl[i0 + 1:i1] == inner,
         'body %d lines vs short inner %d lines' % (i1 - i0 - 1, len(inner)))
    calls = [[x for x in t.splitlines() if x.startswith(CALL_PREFIX)] for t in (short, nohup)]
    c.ok('same_probe_call', len(calls[0]) == 1 and calls[0] == calls[1], calls[0][0][:90] if calls[0] else '(none)')
    launch = [x for x in nl if 'bash -c ' in x]
    c.ok('nohup_launch_line', len(launch) == 1 and launch[0].startswith("SITEQ_TAG=_nohup nohup setsid bash -c 'echo $$ > nohup_pid.txt; bash block.sh;")
         and launch[0].endswith(' > nohup.log 2>&1 < /dev/null &'), launch[0][:60] if launch else '(none)')
    wo = [x for x in sl if x.startswith('W="$HOME/dem-siteq-')]
    c.ok('folders_take_tag', len(wo) == 1 and wo[0].count('${SITEQ_TAG:-}') == 2, wo[0][:70] if wo else '(none)')
    um = [x for x in sl if 'umask 022' in x]
    c.ok('form_b_line_commented', len(um) == 1 and um[0].startswith('# umask 022  # form B'), um[0][:40] if um else '(none)')
    old = subprocess.run(['git', '-C', A.repo, 'show', '%s:%s' % (A.old_tmpl_rev, TMPL_REL)], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE).stdout
    c.ok('old_template', sha_bytes(old) == OLD_TMPL_SHA and ('PROBE_SHA=' + OLD_PROBE_SHA).encode() in old and
         ('fetch -q origin ' + OLD_BRANCH).encode() in old, 'old sha %s' % sha_bytes(old)[:12])
    c.old = old.decode('ascii')
    return c


def case_full(name, title, kind, pin, umask, how='plain', tmpl=None, venv='38', expect_rc=0, fail_ids=(), form_b=False):
    c = Case(name, title)
    home_setup(c, kind, venv)
    t = tmpl if tmpl is not None else TMPL['short']
    if form_b:
        t = t.replace('\n# umask 022  # form B', '\numask 022  # form B', 1)
    rc, screen = run_block(c, fill(t, vals(kind, pin)), umask=umask, how=how)
    um = (umask, '0022' if form_b else umask)
    check_full(c, rc, screen, pin, kind, um, 'no', outer_rc_expected=expect_rc, fail_ids=fail_ids, strict_last=(how == 'plain'))
    return c


def case_s3(s1):
    c = Case('S3', 'rerun in the S1 home on the same day')
    shutil.rmtree(c.dir)
    c.dir, c.home = s1.dir + '_rerun', s1.home
    os.makedirs(c.dir)
    out = find_out(s1.home, 'kgy')
    before, rcb = listing(s1.home), sha_file(os.path.join(out, 'siteq_block_rc.txt'))
    rc, screen = run_block(c, fill(TMPL['short'], vals('kgy', ORIGIN['X'])))
    check_stop(c, rc, screen, r'dem-siteq-\w+ already exists \(nothing written\)$', home_before=before)
    c.ok('old_rc_file_unchanged', sha_file(os.path.join(out, 'siteq_block_rc.txt')) == rcb)
    return c


def case_stop(name, title, kind, pin, msg_re, venv='38', tmpl=None, base='single', rc_file=(None, None)):
    c = Case(name, title)
    home_setup(c, kind, venv, base)
    before = listing(c.home)
    t = tmpl if tmpl is not None else TMPL['short']
    rc, screen = run_block(c, fill(t, vals(kind, pin)))
    out = find_out(c.home, kind)
    check_stop(c, rc, screen, msg_re, home_before=(before if rc_file[1] is None and out is None else None),
               rc_file=(out, rc_file[1]) if rc_file[0] else None)
    if rc_file[0] == 'outfiles':
        files = sorted(os.listdir(out)) if out else []
        c.ok('out_files', files == sorted(rc_file[2]), 'result folder %s' % files)
    c.screen = screen
    for ln in screen.splitlines():
        if re.match(r'^(fatal|error): ', ln):
            c.notes.append('git said: ' + ln[:150])
    return c


def case_c5():
    """C5 of the plan: does nohup leave output in the working folder and make the pinned worktree dirty?"""
    c = Case('NO', 'nohup output file vs the pinned worktree (plan 2-2 C5)')
    b = home_setup(c, 'kgy', venv=None, base='full')
    wt = os.path.join(c.home, 'dem-siteq-c5')
    git('-C', b, 'worktree', 'add', '-q', '--detach', wt, ORIGIN['X'])
    pt = Pty(['setsid', '-c', 'nohup', 'true'], wt, env_for(c.home), os.path.join(c.dir, 'pty1.log'))
    rc = wait_p(pt.p, 30)
    time.sleep(0.3)
    pt.hangup()
    st = git('status', '--porcelain', '--untracked-files=normal', cwd=wt, check=False)
    ign = subprocess.run(['git', '-C', wt, 'check-ignore', '-q', 'nohup.out']).returncode
    c.ok('NO1_tty_stdout_writes_nohup_out', rc == 0 and os.path.exists(os.path.join(wt, 'nohup.out')),
         'rc %s; pty says %r' % (rc, pt.text().strip()[:90]))
    c.ok('NO1_worktree_dirty', st == '?? nohup.out' and ign == 1, 'status %r; check-ignore rc %s (1 = not ignored)' % (st, ign))
    os.remove(os.path.join(wt, 'nohup.out'))
    log = os.path.join(c.dir, 'redirected.log')
    p = spawn(['sh', '-c', 'exec nohup true > "$1" 2>&1 < /dev/null', 'sh', log], wt, env_for(c.home), os.path.join(c.dir, 'p2.log'))
    rc2 = wait_p(p, 30)
    st2 = git('status', '--porcelain', '--untracked-files=normal', cwd=wt, check=False)
    c.ok('NO2_redirected_no_file_clean', rc2 == 0 and st2 == '' and not os.path.exists(os.path.join(wt, 'nohup.out')),
         'rc %s status %r' % (rc2, st2))
    return c


def nohup_checks(c, pin='', umask='0022', want_done=True, timeout=420):
    L = wait_for(lambda: one(os.path.join(c.home, 'rint_siteq_nohup_*')), 30)
    c.ok('launch_folder', L is not None, 'launch folder %s' % (mask(L) if L else None))
    if not L:
        return None
    pidf = wait_for(lambda: rd(os.path.join(L, 'nohup_pid.txt')), 30)
    c.ok('pid_file', bool(pidf and pidf.strip().isdigit()), 'nohup_pid.txt %r' % (pidf or '').strip())
    rcf = wait_for(lambda: rd(os.path.join(L, 'nohup_rc.txt')), timeout if want_done else 25)
    if not want_done:
        pid = int(pidf.strip()) if pidf and pidf.strip().isdigit() else None
        dead = pid is not None and wait_for(lambda: not proc_alive(pid), 20)
        c.ok('job_completes', rcf is not None, 'nohup_rc.txt %r; wrapper pid alive %s' % ((rcf or '').strip(),
                                                                                     None if pid is None else not dead))
        return None
    mm = RC_LINE.match((rcf or '').strip())
    c.ok('job_completes', mm is not None and int(mm.group(1)) == 0, 'nohup_rc.txt %r' % (rcf or '').strip())
    screen = rd(os.path.join(L, 'nohup.log'), '') or ''
    res = check_full(c, 0, screen, pin, 'kgy', (umask, umask), 'yes', tag='_nohup')
    c.ok('nohup_files_outside_worktree', sorted(os.listdir(L)) == ['block.sh', 'nohup.log', 'nohup_pid.txt', 'nohup_rc.txt'],
         'launch folder %s' % sorted(os.listdir(L)))
    return res


def case_nohup(name, title, how, tmpl=None, want_done=True, observe=False):
    c = Case(name, title)
    home_setup(c, 'kgy')
    text = fill(tmpl if tmpl is not None else TMPL['nohup'], vals('kgy', ORIGIN['X']))
    f = os.path.join(c.dir, 'nohup_block.sh')
    wr(f, text)
    env = env_for(c.home)
    if how == 'plain':
        p = spawn(['sh', '-c', 'umask 0022; exec bash "$1"', 'sh', f], c.home, env, os.path.join(c.dir, 'launcher.log'))
        c.ok('launcher_rc', wait_p(p, 60) == 0)
        c.ok('launcher_message', '[siteq] nohup start: pid ' in (rd(os.path.join(c.dir, 'launcher.log'), '') or ''))
    elif how == 'leader':
        # the launcher is the session leader of a pty; when it exits the kernel sends SIGHUP to its process group,
        # which holds the background job -- then the master side hangs up too
        pt = Pty(['sh', '-c', 'umask 0022; exec setsid -c bash "$1"', 'sh', f], c.home, env, os.path.join(c.dir, 'pty.log'))
        c.ok('launcher_rc', wait_p(pt.p, 60) == 0)
        time.sleep(0.5)
        pt.hangup()
        c.ok('launcher_message', '[siteq] nohup start: pid ' in pt.text())
    else:
        # paste into an interactive shell on a pty, then hang the terminal up (like a dropped ssh session)
        pt = Pty(['sh', '-c', 'umask 0022; exec setsid -c bash --norc --noprofile -i'], c.home, env, os.path.join(c.dir, 'pty.log'))
        time.sleep(0.5)
        pt.write(text.encode('ascii'))
        seen = wait_for(lambda: '[siteq] nohup start: pid ' in pt.text(), 60)
        c.ok('launcher_message', seen)
        pt.hangup()
        c.ok('attached_shell_gone_after_hangup', wait_p(pt.p, 30) is not None)
    if observe:
        # no verdict: record how the job ended (the outcome depends on what the job was doing when SIGHUP came)
        L = wait_for(lambda: one(os.path.join(c.home, 'rint_siteq_nohup_*')), 30)
        rcf = wait_for(lambda: rd(os.path.join(L, 'nohup_rc.txt')), 420) if L else None
        c.notes.append('nohup_rc.txt %r' % (rcf or '').strip())
        for ln in (rd(os.path.join(L, 'nohup.log'), '') or '').splitlines() if L else []:
            if re.search(r'STOP|died of signal|error|fatal|\] rc \d', ln):
                c.notes.append('nohup.log: ' + ln[:160])
        c.asserts = []
        return c
    if want_done:
        r = nohup_checks(c, pin=ORIGIN['X'])
        c.ids = c.ids if r else []
    else:
        nohup_checks(c, pin=ORIGIN['X'], want_done=False)
    return c


def case_n4(s1):
    """Both forms on the same day in the same home: the nohup form's folders carry the _nohup suffix."""
    c = Case('N4', 'nohup form in the S1 home on the same day (folders get the _nohup suffix)')
    shutil.rmtree(c.dir)
    c.dir, c.home = s1.dir + '_nohup', s1.home
    os.makedirs(c.dir)
    out1 = find_out(s1.home, 'kgy')
    names = ('siteq_result.json', 'siteq_block_rc.txt', 'siteq_block_env.txt', 'siteq_block_modes.txt', 'siteq.log')
    before = dict((f, sha_file(os.path.join(out1, f))) for f in names)
    f = os.path.join(c.dir, 'nohup_block.sh')
    wr(f, fill(TMPL['nohup'], vals('kgy', ORIGIN['X'])))
    p = spawn(['sh', '-c', 'umask 0022; exec bash "$1"', 'sh', f], c.home, env_for(c.home), os.path.join(c.dir, 'launcher.log'))
    c.ok('launcher_rc', wait_p(p, 60) == 0)
    nohup_checks(c, pin=ORIGIN['X'])
    c.ok('short_form_files_untouched', all(sha_file(os.path.join(out1, x)) == before[x] for x in names), mask(out1))
    return c


def case_s10():
    """Control for the hang-up: the plain short block pasted into the same pty shell dies when the terminal hangs up."""
    c = Case('S10', 'control: short block pasted into a pty shell, terminal hung up while the probe runs')
    home_setup(c, 'kgy')
    text = fill(TMPL['short'], vals('kgy', ORIGIN['X']))
    pt = Pty(['sh', '-c', 'umask 0022; exec setsid -c bash --norc --noprofile -i'], c.home, env_for(c.home), os.path.join(c.dir, 'pty.log'))
    time.sleep(0.5)
    pt.write(text.encode('ascii'))

    def probe_running():
        out = find_out(c.home, 'kgy')
        log = rd(os.path.join(out, 'siteq.log'), '') if out else ''
        return out if log and log.count('[siteq] C') >= 9 else None
    out = wait_for(probe_running, 120)
    c.ok('probe_started', out is not None)
    pt.hangup()
    c.ok('attached_shell_gone_after_hangup', wait_p(pt.p, 30) is not None)
    time.sleep(30)
    reap()
    c.ok('block_killed_no_rc_file', out is not None and not os.path.exists(os.path.join(out, 'siteq_block_rc.txt')))
    c.ok('block_killed_no_result', out is not None and not os.path.exists(os.path.join(out, 'siteq_result.json')))
    return c


def mutate(t, old, new, count=1):
    if not t.count(old) == count:
        raise RuntimeError('mutation anchor not found once: %r' % old[:60])
    return t.replace(old, new)


# ------------------------------------------------------------------ main
def main():
    global A, W0, ORIGIN, VENVS, TMPL
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True)
    ap.add_argument('--repo', default=None)
    ap.add_argument('--src-rev', default='HEAD')
    ap.add_argument('--old-tmpl-rev', default=OLD_TMPL_REV)
    ap.add_argument('--py38', default=os.environ.get('KGY_PY38', ''))
    ap.add_argument('--py311', default=sys.executable)
    ap.add_argument('--summary', default=None)
    ap.add_argument('--only', default='')
    A = ap.parse_args()
    if not os.getpid() == 1:
        print('refuse: not PID 1 -- run inside a new PID namespace: unshare -pf --mount-proc --kill-child python3 -I -B %s --work <dir>'
              % os.path.relpath(__file__))
        return 2
    if not os.geteuid() == 0:
        print('refuse: root is needed (chown and ACL cases)')
        return 2
    A.repo = A.repo or subprocess.run(['git', '-C', HERE, 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE,
                                      check=True).stdout.decode().strip()
    W0 = os.path.realpath(A.work)
    if (W0 + os.sep).startswith(os.path.realpath(A.repo) + os.sep) or (os.path.exists(W0) and os.listdir(W0)):
        print('refuse: --work must be a new or empty folder outside the repository')
        return 2
    os.makedirs(W0, exist_ok=True)
    add_mask(W0, '<WORK>')
    if not A.py38:
        A.py38 = subprocess.run(['uv', 'python', 'find', '3.8'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode().strip()
    only = set(x for x in A.only.split(',') if x)
    t_start = time.time()
    ORIGIN = build_origin(W0, A.repo, A.src_rev)
    VENVS = make_venvs(W0, A.py38, A.py311)
    if not VENVS['38'][1][:3] == KGY_UNIT:
        print('refuse: the Python 3.8 venv is not the kgy unit %s: %s' % (KGY_UNIT, VENVS['38'][1]))
        return 2
    TMPL = {'short': rd(os.path.join(HERE, 'short_block.tmpl')), 'nohup': rd(os.path.join(HERE, 'short_block_nohup.tmpl'))}
    ver = lambda a: subprocess.run(a, stdout=subprocess.PIPE).stdout.decode().splitlines()[0]
    say('siteq short block container tests (templates of 2026-11-11) -- %s' % os.path.basename(__file__))
    say('env: venv38 %s | venv311 %s | %s | %s | uid %d | harness pid %d (own PID namespace)' % (
        ' '.join(VENVS['38'][1]), ' '.join(VENVS['311'][1]), ver(['git', '--version']), ver(['bash', '--version'])[:40],
        os.geteuid(), os.getpid()))
    say('templates: short_block.tmpl %s | short_block_nohup.tmpl %s | tools/siteq_probe.py %s' % (
        sha_file(os.path.join(HERE, 'short_block.tmpl'))[:16], sha_file(os.path.join(HERE, 'short_block_nohup.tmpl'))[:16],
        ORIGIN['probe_sha'][:16]))
    say('fake origin (from %s of the repository): O %s = %s (scripts only) | X %s = PIN of the normal cases (+ probe %s) | '
        'Z %s = tip of %s (probe one byte changed, %s)' % (A.src_rev, ORIGIN['O'][:12], OLD_BRANCH, ORIGIN['X'][:12],
                                                           ORIGIN['probe_sha'][:12], ORIGIN['Z'][:12], NEW_BRANCH,
                                                           ORIGIN['probe_sha_z'][:12]))
    say('base clones: --no-local --no-checkout; "single" = only %s (like a site checkout that never fetched the new branch)' % OLD_BRANCH)
    say('')
    X, Z = ORIGIN['X'], ORIGIN['Z']
    cases = []
    want = lambda n: not only or n in only
    if want('T0'):
        cases.append(t0_static())
    s1 = None
    if want('S1') or want('S3') or want('N4'):
        s1 = case_full('S1', 'kgy block, shell umask 022, plan/ledger/outbase/planfile filled', 'kgy', X, '0022')
        cases.append(s1)
    if want('S1b'):
        cases.append(case_full('S1b', 'kgy block, shell umask 002', 'kgy', X, '0002'))
    if want('S1c'):
        cases.append(case_full('S1c', 'form B shown: shell umask 002, the commented umask line enabled', 'kgy', X, '0002',
                               form_b=True))
    if want('S2'):
        cases.append(case_full('S2', 'gabia block, plan/ledger/outbase/planfile empty', 'gabia', X, '0022'))
    if want('S3') and s1 is not None:
        cases.append(case_s3(s1))
    if want('N4') and s1 is not None:
        cases.append(case_n4(s1))
    if want('S4'):
        cases.append(case_stop('S4', 'PIN placeholder left as it is', 'kgy', None, r'PIN is not a 40-hex commit \(nothing written\)$'))
    if want('S5'):
        cases.append(case_stop('S5', 'well-formed but unknown commit', 'kgy', 'deadbeef' * 5, r'git worktree add failed$'))
    if want('S6'):
        cases.append(case_stop('S6', 'venv missing', 'kgy', X, r'venv not found: \S+/dem-venv \(nothing written\)$', venv=None))
    if want('S7'):
        cases.append(case_stop('S7', 'PIN whose probe differs by one byte', 'kgy', Z, r'probe sha256 differs \(probe not run\)$',
                               rc_file=('outfiles', r'^probe sha256 differs \(probe not run\)$', ['siteq_probe.py', 'siteq_block_rc.txt'])))
    if want('S8'):
        cases.append(case_full('S8', 'venv = Python 3.11 (not the kgy unit) -> probe FAIL', 'kgy', X, '0022', venv='311',
                               expect_rc=1, fail_ids=('C02',)))
    if want('S9'):
        cases.append(case_full('S9', 'bash -i reads the block from stdin (paste-like)', 'kgy', X, '0022', how='stdin-i'))
    old = cases[0].old if cases and cases[0].name == 'T0' else None
    if old is not None and want('R1'):
        cases.append(case_stop('R1', 'OLD template (11-09), base never fetched the new branch -> stops at worktree add',
                               'kgy', X, r'git worktree add failed$', tmpl=old))
    if old is not None and want('R2'):
        cases.append(case_stop('R2', 'OLD template (11-09), base already has the PIN -> stops at the probe hash', 'kgy', X,
                               r'probe sha256 differs \(probe not run\)$', tmpl=old, base='full',
                               rc_file=('outfiles', None, ['siteq_probe.py'])))
    if want('NO'):
        cases.append(case_c5())
    if want('N1'):
        cases.append(case_nohup('N1', 'nohup form, launched without a terminal', 'plain'))
    if want('N2'):
        cases.append(case_nohup('N2', 'nohup form, launcher = pty session leader (kernel SIGHUP to the job group) + hang-up', 'leader'))
    if want('N3'):
        cases.append(case_nohup('N3', 'nohup form pasted into an interactive pty shell, terminal hung up after the start', 'paste'))
    muts = []
    if want('M1'):
        t = mutate(TMPL['short'], '\nrcfile "$RC"\n', '\n')
        c = case_full('M1', 'MUTANT: the line that writes the rc file at the end removed', 'kgy', X, '0022', tmpl=t)
        muts.append((c, ['rc_file']))
    if want('M2'):
        t = mutate(TMPL['short'], '\necho "$PROBE_SHA  $OUT/siteq_probe.py" | sha256sum -c --quiet || stop "probe sha256 differs (probe not run)"\n', '\n')
        c = case_stop('M2', 'MUTANT: the probe hash check removed (PIN = Z)', 'kgy', Z, r'probe sha256 differs \(probe not run\)$',
                      tmpl=t, rc_file=('outfiles', r'^probe sha256 differs \(probe not run\)$', ['siteq_probe.py', 'siteq_block_rc.txt']))
        muts.append((c, ['outer_rc', 'stop_message', 'rc_file', 'out_files']))
    if want('M3'):
        t = mutate(TMPL['short'], "    return 'self' if u == me else ('root' if u == 0 else 'other')\n",
                   "    return pwd.getpwuid(u).pw_name if u in [x.pw_uid for x in pwd.getpwall()] else str(u)\n")
        c = case_full('M3', 'MUTANT: the mode list prints owner names (and the number when no name)', 'kgy', X, '0022', tmpl=t)
        muts.append((c, ['modes_no_names']))
    if want('M4'):
        t = mutate(TMPL['nohup'], '\nSITEQ_TAG=_nohup nohup setsid bash -c ', '\nSITEQ_TAG=_nohup bash -c ')
        c = case_nohup('M4', 'MUTANT: nohup and setsid removed from the launch line (same pty session-leader launch as N2)',
                       'leader', tmpl=t, want_done=False)
        muts.append((c, ['job_completes']))
    if want('M5'):
        t = mutate(TMPL['nohup'], '\nSITEQ_TAG=_nohup nohup setsid bash -c ', '\nSITEQ_TAG=_nohup setsid bash -c ')
        c = case_nohup('M5', 'MUTANT: nohup removed, setsid kept (same launch as N2)', 'leader', tmpl=t)
        muts.append((c, ['sighup_record']))
    obs = []
    if want('O1'):
        t = mutate(TMPL['nohup'], '\nSITEQ_TAG=_nohup nohup setsid bash -c ', '\nSITEQ_TAG=_nohup nohup bash -c ')
        obs.append(case_nohup('O1', 'OBSERVATION (no verdict): setsid removed, nohup kept (same launch as N2: the kernel SIGHUP reaches '
                              'the job group)', 'leader', tmpl=t, observe=True))
    if want('S10'):
        cases.append(case_s10())
    # ---------------------------------------------------------------- report
    say('== cases ==')
    allok = True
    for c in cases:
        f = c.failed()
        allok = allok and not f
        say('%-4s %s  -> %s (%d/%d asserts)' % (c.name, c.title, 'PASS' if not f else 'FAIL ' + ','.join(f),
                                                 len(c.asserts) - len(f), len(c.asserts)))
        for k, ok, d in c.asserts:
            say('       %s %-34s %s' % ('ok ' if ok else 'BAD', k, mask(str(d))[:200]))
        if getattr(c, 'counts', None):
            say('       counts %s' % json.dumps(c.counts, sort_keys=True))
        for n in c.notes:
            say('       note: %s' % n)
    if want('S1') and want('N1'):
        s1c = next((c for c in cases if c.name == 'S1'), None)
        n1c = next((c for c in cases if c.name == 'N1'), None)
        same = s1c is not None and n1c is not None and getattr(s1c, 'ids', None) and s1c.ids == getattr(n1c, 'ids', None)
        allok = allok and bool(same)
        say('same check set S1 vs N1 (short vs nohup form): %s (%d ids)' % ('yes' if same else 'NO', len(getattr(s1c, 'ids', []) or [])))
    say('== mutants (each must fail exactly the listed asserts, all other asserts must hold) ==')
    for c, target in muts:
        f = c.failed()
        right = sorted(f) == sorted(target)
        allok = allok and right
        say('%-4s %s -> failed %s ; wanted %s -> %s' % (c.name, c.title, f, target, 'right reason' if right else 'WRONG'))
        for k, ok, d in c.asserts:
            if not ok:
                say('       BAD %-34s %s' % (k, mask(str(d))[:200]))
    if obs:
        say('== observations (no verdict) ==')
        for c in obs:
            say('%-4s %s' % (c.name, c.title))
            for n in c.notes:
                say('       %s' % mask(n))
    reap()
    say('== end ==')
    say('leftover processes in this namespace at the end: %d (not killed by this script; they end with the namespace)' % leftovers())
    say('elapsed %.0f s; overall %s' % (time.time() - t_start, 'PASS' if allok else 'FAIL'))
    if A.summary:
        with open(A.summary, 'w', encoding='utf-8') as f:
            f.write('\n'.join(mask(x) for x in OUT_LINES) + '\n')
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())
