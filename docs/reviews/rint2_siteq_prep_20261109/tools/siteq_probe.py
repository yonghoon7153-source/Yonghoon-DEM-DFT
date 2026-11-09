# siteq_probe.py - Rint-2 R chain "site qualification" probe (prepared 2026-11-09).
# ASCII only and free of the bang character on purpose: it is pasted inside an interactive bash heredoc.
# Writes only under --out (plus, as a side effect of the chain's own env_record(), possibly .pyc files in the
# venv site-packages).  Never runs LIGGGHTS / MPM / payload solves, never submits jobs, no network.
# Exit code: 0 = no FAIL and no ERROR, 1 = at least one FAIL or ERROR, 2 = setup problem.
import argparse
import hashlib
import json
import os
import platform
import shutil
import signal
import stat
import subprocess
import sys
import time

sys.dont_write_bytecode = True
os.environ['GIT_OPTIONAL_LOCKS'] = '0'   # git status must not refresh the index of the pinned checkout

PROBE = 'rint-siteq-probe-v1'
RESULT_SCHEMA = 'rint-siteq-result-v1'
RES = []
KIDS = []          # Popen objects started with start_new_session=True (pgid == pid)
TOKENS = {}        # chain group token -> (since_ticks, run dict or None)
A = None
RR = None
NETFS = ('nfs', 'nfs4', 'cifs', 'smb3', 'smbfs', '9p', 'v9fs', 'drvfs', 'ceph', 'glusterfs', 'lustre', 'gpfs', 'beegfs',
         'afs', 'sshfs', 'fuse')
OPT_KEEP = ('ro', 'rw', 'nosuid', 'nodev', 'noexec', 'relatime', 'noatime', 'strictatime', 'sync', 'async', 'lock', 'nolock',
            'local_lock', 'vers', 'nfsvers', 'hard', 'soft', 'hidepid', 'subset', 'metadata', 'case', 'acl', 'noacl', 'uid',
            'gid', 'umask', 'fmask', 'dmask', 'sec', 'lookupcache', 'actimeo', 'noac', 'nocto', 'cache', 'data')
UNIT_SNIPPET = ('import json, sys\n'
                'u = {"python_minor": "%d.%d" % tuple(sys.version_info[:2]), "numpy": None, "scipy": None,'
                ' "executable": sys.executable}\n'
                'try:\n    import numpy\n    u["numpy"] = numpy.__version__\nexcept Exception:\n    pass\n'
                'try:\n    import scipy\n    u["scipy"] = scipy.__version__\nexcept Exception:\n    pass\n'
                'print(json.dumps(u))\n')
ENC_SNIPPET = ('import sys\n'
               's = "\\ud55c\\uae00 \\u00b7 \\u2192 \\u2260 \\u2713 \\u03c3 \\u2605 \\u24d0"\n'
               'sys.stdout.write(s + "\\n")\n'
               'sys.stdout.write("encoding=%s utf8_mode=%d\\n" % (sys.stdout.encoding, sys.flags.utf8_mode))\n')
# runner pids: the runner itself ($$) and its background jobs (jobs -p, synchronous) -> pids.txt (independent liveness check)
RUNNER_LEFTOVER = ('echo $$ >> pids.txt\n'
                   '"$SITEQ_PY" -I -B -c "import os, time; os.setsid(); time.sleep(60)" &\n'
                   'sleep 60 &\n'
                   '( sleep 3; echo late > late.txt ) &\n'
                   'jobs -p >> pids.txt\n'
                   'exit 0\n')
RUNNER_SLEEP = ('echo $$ >> pids.txt\n'
                '"$SITEQ_PY" -I -B -c "import os, time; os.setsid(); time.sleep(120)" &\n'
                'jobs -p >> pids.txt\n'
                'sleep 120\n')
CHILD_CHAIN = ('import json, os, sys\n'
               'sys.dont_write_bytecode = True\n'
               'sys.path.insert(0, sys.argv[1])\n'
               'import rint_r_chain as RR\n'
               'd, name, tmo = sys.argv[2], sys.argv[3], float(sys.argv[4])\n'
               'env = dict(os.environ, SITEQ_PY=sys.executable)\n'
               'os.makedirs(os.path.join(d, "logs"), exist_ok=True)\n'
               'with open(os.path.join(d, "logs", name + ".log"), "w", encoding="utf-8") as lf:\n'
               '    rc, cause, end = RR.run_in_group(["bash", os.path.join(d, "runner.sh")], d, env, lf, tmo,'
               ' os.path.join(d, "groups"), name)\n'
               'with open(os.path.join(d, "child_result.json"), "w", encoding="utf-8") as f:\n'
               '    json.dump({"rc": rc, "cause": cause, "end": end}, f)\n')
CHILD_LOCK = ('import sys, time\n'
              'sys.dont_write_bytecode = True\n'
              'sys.path.insert(0, sys.argv[1])\n'
              'import rint_r_chain as RR\n'
              'with RR.ledger_lock(sys.argv[2], exclusive=(sys.argv[3] == "ex"), wait=10.0):\n'
              '    with open(sys.argv[4], "w") as f:\n'
              '        f.write("held")\n'
              '    time.sleep(120)\n')
CHILD_FILES = ('import json, os, sys\n'
               'sys.dont_write_bytecode = True\n'
               'sys.path.insert(0, sys.argv[1])\n'
               'import rint_r_chain as RR\n'
               'd = sys.argv[2]\n'
               'out = {}\n'
               'for nm in ("reg", "empty", "missing", "dangling", "dir", "fifo", "mode000"):\n'
               '    raw, st = RR.read_regular_file(os.path.join(d, nm))\n'
               '    out[nm] = [st, None if raw is None else len(raw)]\n'
               'raw, st = RR.read_regular_file("/dev/null")\n'
               'out["devnull"] = [st, None if raw is None else len(raw)]\n'
               'for key, run in (("log_fifo", "R01_fifo"), ("log_reg", "R02_reg"), ("log_badname", "../x")):\n'
               '    txt, st = RR.run_log_text(d, run)\n'
               '    out[key] = [st, len(txt)]\n'
               'out["group_json_fifo"] = RR._read_group_json(os.path.join(d, "fifo"))\n'
               'out["summary_fifo"] = RR.read_summary_state(d, "fifo")[2]\n'
               'out["attempt_fifo"] = RR.read_attempt(os.path.join(d, "att_fifo"))\n'
               'out["digest_with_fifo"] = RR.folder_digest(os.path.join(d, "dig_fifo"))\n'
               'out["digest_plain"] = RR.folder_digest(os.path.join(d, "dig_plain"))\n'
               'print(json.dumps(out, sort_keys=True))\n')


class Alarm(BaseException):
    pass


def _on_alarm(signum, frame):
    raise Alarm()


def utc():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def add(cid, title, status, detail='', data=None, sec=None):
    rec = {'id': cid, 'title': title, 'status': status, 'detail': detail, 'data': {} if data is None else data}
    if sec is not None:
        rec['seconds'] = round(sec, 3)
    RES.append(rec)
    print('[siteq] %-4s %-5s %s%s' % (cid, status, title, (' -- ' + detail) if detail else ''), flush=True)
    return rec


def check(cid, title, fn, budget=180):
    t = time.time()
    old = signal.signal(signal.SIGALRM, _on_alarm)
    signal.alarm(int(budget))
    try:
        try:
            st, detail, data = fn()
        finally:
            signal.alarm(0)
    except Alarm:
        st, detail, data = 'FAIL', 'no answer within %d s (hang on this site?)' % budget, {}
    except Exception as e:                                    # noqa: BLE001 -- probe or site problem, cause unknown
        st, detail, data = 'ERROR', '%s: %s' % (type(e).__name__, str(e)[:400]), {}
    finally:
        signal.signal(signal.SIGALRM, old)
    return add(cid, title, st, detail, data, time.time() - t)


def mkd(name):
    d = os.path.join(A.out, name)
    os.makedirs(d)
    return d


def wtext(p, s, mode=None):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)
    if mode is not None:
        os.chmod(p, mode)
    return p


def spawn(argv, logpath):
    with open(logpath, 'wb') as lf:
        p = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
    KIDS.append(p)
    return p


def kill_kid(p):
    if p.poll() is None:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
    try:
        p.wait(timeout=15)
    except Exception:                                         # noqa: BLE001
        pass


def wait_file(p, limit):
    t = time.time() + limit
    while time.time() < t:
        if os.path.exists(p):
            return True
        time.sleep(0.05)
    return False


def wait_launch(d, name, limit=30.0):
    p = os.path.join(d, 'groups', name + '.launch.json')
    t = time.time() + limit
    while time.time() < t:
        try:
            with open(p, encoding='utf-8') as f:
                L = json.load(f)
            if isinstance(L.get('pid'), int):
                return L
        except (OSError, ValueError):
            pass
        time.sleep(0.05)
    return None


def remember(L):
    run = {'pid': L['pid'], 'start': L.get('runner_start')} if isinstance(L.get('pid'), int) else None
    TOKENS[L['token']] = (L.get('since_ticks'), run)


def members(tok):
    since, run = TOKENS.get(tok, (None, None))
    try:
        return RR.group_members(tok, since=since, run=run)
    finally:
        RR.GROUP_SCAN.pop(tok, None)


def still_alive(d, tok):
    """Independent of the token scanner: pids the runner wrote to pids.txt that are still running and still carry the token
    (an unreadable environ counts as alive -- conservative)."""
    try:
        with open(os.path.join(d, 'pids.txt'), encoding='ascii') as f:
            pids = [int(x) for x in f.read().split() if x.isdigit()]
    except OSError:
        return None, []
    needle = ('%s=%s' % (RR.GROUP_TOKEN_ENV, tok)).encode('ascii')
    alive = []
    for pid in pids:
        try:
            st = RR.proc_stat(pid)
        except OSError:
            st = None
        if st is None or st[0] in (b'Z', b'X', b'x'):
            continue
        try:
            with open('/proc/%d/environ' % pid, 'rb') as f:
                if needle in f.read().split(b'\0'):
                    alive.append(pid)
        except OSError:
            alive.append(pid)                                 # cannot tell -> count as alive (conservative)
    return pids, alive


def own_sweep(tokens, rounds=5):
    """Final cleanup, independent of the chain's scanner: SIGKILL every process whose readable environ carries one of our tokens
    (positive match only -- unreadable or unrelated processes are never touched).  Returns the number of kills."""
    needles = [('%s=%s' % (RR.GROUP_TOKEN_ENV, t)).encode('ascii') for t in tokens]
    n = 0
    for _ in range(rounds):
        hit = []
        for e in os.listdir('/proc'):
            if not e.isdigit() or int(e) == os.getpid():
                continue
            try:
                with open('/proc/%s/environ' % e, 'rb') as f:
                    env = f.read().split(b'\0')
            except OSError:
                continue
            if any(x in env for x in needles):
                hit.append(int(e))
        if not hit:
            break
        for pid in hit:
            try:
                os.kill(pid, signal.SIGKILL)
                n += 1
            except OSError:
                pass
        time.sleep(0.2)
    return n


def read_json(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def comm(pid):
    try:
        with open('/proc/%d/comm' % pid, encoding='utf-8', errors='replace') as f:
            return f.read().strip()
    except OSError:
        return None


# ------------------------------------------------------------------ filesystem facts (no mount sources: they may hold host names)
def _unesc(s):
    return s.replace('\\040', ' ').replace('\\011', ' ').replace('\\012', ' ').replace('\\134', '\\')


def _opts(s):
    keep = []
    for o in s.split(','):
        k = o.split('=', 1)[0]
        if k in OPT_KEEP:
            keep.append(o)
    return ','.join(keep)


def mount_of(path):
    rp = os.path.realpath(path)
    try:
        st = os.stat(rp)
    except OSError as e:
        return {'path': path, 'exists': False, 'error': type(e).__name__}
    dev = '%d:%d' % (os.major(st.st_dev), os.minor(st.st_dev))
    best = None
    try:
        with open('/proc/self/mountinfo', encoding='utf-8', errors='replace') as f:
            for ln in f:
                left, sep, right = ln.partition(' - ')
                if not sep:
                    continue
                a, b = left.split(), right.split()
                if len(a) < 6 or len(b) < 3:
                    continue
                mp = _unesc(a[4])
                if not (rp == mp or rp.startswith(mp.rstrip('/') + '/') or mp == '/'):
                    continue
                score = (a[2] == dev, len(mp))
                if best is None or score > best[0]:
                    best = (score, {'mount_point': mp, 'fstype': b[0], 'dev_match': a[2] == dev,
                                    'mount_opts': _opts(a[5]), 'super_opts': _opts(b[2])})
    except OSError as e:
        return {'path': path, 'exists': True, 'error': 'mountinfo ' + type(e).__name__}
    out = {'path': path, 'realpath': rp, 'exists': True, 'st_dev': dev}
    if best:
        out.update(best[1])
    try:
        du = shutil.disk_usage(rp)
        vf = os.statvfs(rp)
        out.update(free_bytes=du.free, total_bytes=du.total, inodes_free=vf.f_favail, inodes_total=vf.f_files,
                   writable=os.access(rp, os.W_OK))
    except OSError as e:
        out['statvfs_error'] = type(e).__name__
    return out


def is_netfs(fstype):
    t = (fstype or '').lower()
    return any(t == x or t.startswith(x + '.') or t.startswith(x) for x in NETFS)


# ------------------------------------------------------------------ checks
def c01():
    pyc = os.path.join(A.repo, 'scripts', '__pycache__')
    A.pyc_before = os.stat(pyc).st_mtime_ns if os.path.isdir(pyc) else None
    global RR
    sd = os.path.join(A.repo, 'scripts')
    if sd not in sys.path:
        sys.path.insert(0, sd)
    import rint_r_chain as rr_mod
    RR = rr_mod
    here = os.path.realpath(str(RR.HERE))
    ok = here == os.path.realpath(sd)
    return ('PASS' if ok else 'FAIL', 'imported %s' % RR.__file__,
            {'here': here, 'schema': RR.SCHEMA, 'run_contract': getattr(RR.RC, '__file__', None)})


def c02():
    rec = RR.env_record()
    want = {'python_minor': A.expect_py, 'numpy': A.expect_numpy, 'scipy': A.expect_scipy}
    unit = rec.get('unit')
    ok = unit == want
    ro = rec.get('record_only') or {}
    data = {'unit': unit, 'expected': want, 'record_only': ro, 'in_venv': not (sys.prefix == sys.base_prefix),
            'sys_executable': sys.executable}
    return ('PASS' if ok else 'FAIL', 'env unit %s vs expected %s' % (json.dumps(unit, sort_keys=True), json.dumps(want, sort_keys=True)),
            data)


def c02b():
    which = shutil.which('python3')
    data = {'path_python3': which, 'sys_executable': sys.executable}
    if which is None:
        return 'FAIL', 'python3 not on PATH (the runner starts the payload as python3 from PATH, MPM_NO_VENV=1)', data
    r = subprocess.run([which, '-I', '-c', UNIT_SNIPPET], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=120)
    try:
        u = json.loads(r.stdout.decode('utf-8', 'replace'))
    except ValueError:
        u = None
    data['path_python3_unit'] = u
    mine = RR.env_record().get('unit')
    same = isinstance(u, dict) and all(u.get(k) == (mine or {}).get(k) for k in ('python_minor', 'numpy', 'scipy'))
    data['same_path_as_sys_executable'] = os.path.abspath(which) == os.path.abspath(sys.executable)
    return ('PASS' if same else 'FAIL', 'PATH python3 env unit %s (probe %s)' % (json.dumps(u, sort_keys=True),
                                                                              json.dumps(mine, sort_keys=True)), data)


def c03():
    g = RR.git_identity(os.path.join(A.repo, 'scripts', 'rint_r_chain.py'))
    ok = g.get('head') == A.pin and g.get('dirty') is False and g.get('rel') == 'scripts/rint_r_chain.py' and g.get('error') is None
    return ('PASS' if ok else 'FAIL', 'head %s dirty %s rel %s error %s' % (g.get('head'), g.get('dirty'), g.get('rel'),
                                                                          g.get('error')), {'git_identity': g})


def c04():
    rec = RR.code_record(os.path.join(A.repo, 'scripts', RR.RUNNER_NAME))
    why = RR.code_dirty_problem(rec)
    missing = [x['file'] for x in rec.get('files') or [] if x.get('sha256') is None]
    ksha = RR.code_key_sha(rec)
    ok = why is None and not missing
    det = 'code_key_sha256 %s' % ksha if ok else ('problem: %s; missing %s' % (why, missing))
    return ('PASS' if ok else 'FAIL', det, {'code_key_sha256': ksha, 'missing_code_files': missing, 'problem': why,
                                            'n_code_files': len(rec.get('files') or [])})


def c05():
    h = RR.host_ident()
    seen, what = RR.host_seen(h, RR.host_ident())
    if not h.get('boot_id') or not h.get('pidns'):
        st = 'FAIL'
        det = 'boot_id or pid namespace unreadable -> recover can never confirm a group here (host_seen needs both)'
    elif not h.get('machine_id'):
        st, det = 'WARN', 'machine_id unreadable (recover then compares None == None)'
    else:
        st, det = ('PASS', 'machine_id, boot_id, pidns readable') if seen else ('FAIL', 'host_seen(self, self) False: ' + what)
    return st, det, {'host': h}


def c06():
    clk = os.sysconf('SC_CLK_TCK')
    ps = RR.proc_stat(os.getpid())
    pt = RR.proc_stat(os.getpid(), os.getpid())
    bt = RR.boot_ticks()
    ru = RR._proc_ruid('/proc/self')
    ok = (ps is not None and pt is not None and isinstance(ps[1], int) and isinstance(bt, int) and bt >= ps[1]
          and ps[2] == os.getppid() and ps[3] == os.getpgrp() and ps[4] == os.getsid(0) and ru == os.getuid())
    data = {'clk_tck': clk, 'stat': None if ps is None else [ps[0].decode('ascii', 'replace')] + list(ps[1:]), 'boot_ticks': bt,
            'ruid': ru, 'uid': os.getuid(), 'euid': os.geteuid()}
    return ('PASS' if ok else 'FAIL', 'proc_stat/boot_ticks/_proc_ruid consistent' if ok else 'inconsistent /proc readings', data)


def c07():
    pp = RR.proc_stat(os.getppid())
    alive = RR.chain_parent_alive({'chain_pid': os.getppid(), 'chain_start': pp[1] if pp else None})
    reused = RR.chain_parent_alive({'chain_pid': os.getppid(), 'chain_start': (pp[1] + 1) if pp and isinstance(pp[1], int) else None})
    p = subprocess.Popen([sys.executable, '-I', '-B', '-c', 'pass'], stdin=subprocess.DEVNULL)
    st = RR.proc_stat(p.pid)
    p.wait()
    dead = RR.chain_parent_alive({'chain_pid': p.pid, 'chain_start': st[1] if st else None})
    ok = alive is True and dead is False and reused is False and st is not None
    return ('PASS' if ok else 'FAIL', 'live parent %s, reaped child %s, parent with other start tick %s' % (alive, dead, reused),
            {'alive': alive, 'dead': dead, 'reused': reused})


def c08():
    clk = os.sysconf('SC_CLK_TCK')
    tok = os.urandom(16).hex()
    dummy = subprocess.Popen([sys.executable, '-I', '-B', '-c', 'pass'], stdin=subprocess.DEVNULL)
    dst = RR.proc_stat(dummy.pid)
    dummy.wait()
    run = {'pid': dummy.pid, 'start': dst[1] if dst else None}     # production-like: a (finished) runner session is known
    t = time.time()
    m_new = RR.group_members(tok, since=RR.boot_ticks() - 2 * clk, run=run)
    s_new = time.time() - t
    RR.GROUP_SCAN.pop(tok, None)
    m_old = RR.group_members(tok, since=None)
    uns = list((RR.GROUP_SCAN.get(tok) or {}).get('unsure') or [])
    RR.GROUP_SCAN.pop(tok, None)
    nproc = sum(1 for e in os.listdir('/proc') if e.isdigit())
    data = {'members_since_now': m_new, 'scan_seconds': round(s_new, 3), 'processes_visible': nproc,
            'old_rule_result': m_old, 'old_rule_unsure_n': len(uns),
            'old_rule_unsure_sample': [[p, comm(p)] for p in uns[:20]]}
    ok = m_new == []
    det = 'fresh token -> %s in %.2f s (%d processes); old rule (no since, no runner) unsure %d' % (m_new, s_new, nproc, len(uns))
    return ('PASS' if ok else 'FAIL'), det, data


def c09():
    d = mkd('c09_leftover')
    wtext(os.path.join(d, 'runner.sh'), RUNNER_LEFTOVER)
    os.makedirs(os.path.join(d, 'logs'))
    env = dict(os.environ, SITEQ_PY=sys.executable)
    with open(os.path.join(d, 'logs', 'S09_run.log'), 'w', encoding='utf-8') as lf:
        rc, cause, end = RR.run_in_group(['bash', os.path.join(d, 'runner.sh')], d, env, lf, 60.0, os.path.join(d, 'groups'), 'S09_run')
    L = read_json(os.path.join(d, 'groups', 'S09_run.launch.json'))
    remember(L)
    time.sleep(4.5)
    late = os.path.exists(os.path.join(d, 'late.txt'))
    left = members(L['token'])
    pids, alive = still_alive(d, L['token'])
    ok = (rc == 0 and cause is None and end.get('confirmed') is True and end.get('left') == [] and (end.get('killed') or 0) >= 2
          and L.get('pgid') == L.get('pid') and not late and left == [] and pids and len(pids) == 4 and alive == [])
    det = 'rc %s cause %s confirmed %s killed %s pgid==pid %s late_file %s left_now %s; runner-reported pids %s still alive %s' % (
        rc, cause, end.get('confirmed'), end.get('killed'), L.get('pgid') == L.get('pid'), late, left, pids, alive)
    return ('PASS' if ok else 'FAIL'), det, {'end': end}


def c10():
    d = mkd('c10_timeout')
    wtext(os.path.join(d, 'runner.sh'), RUNNER_SLEEP)
    os.makedirs(os.path.join(d, 'logs'))
    env = dict(os.environ, SITEQ_PY=sys.executable)
    t = time.time()
    with open(os.path.join(d, 'logs', 'S10_run.log'), 'w', encoding='utf-8') as lf:
        rc, cause, end = RR.run_in_group(['bash', os.path.join(d, 'runner.sh')], d, env, lf, 2.0, os.path.join(d, 'groups'), 'S10_run')
    el = time.time() - t
    L = read_json(os.path.join(d, 'groups', 'S10_run.launch.json'))
    remember(L)
    left = members(L['token'])
    pids, alive = still_alive(d, L['token'])
    ok = (cause == 'timeout' and end.get('confirmed') is True and end.get('left') == [] and (end.get('killed') or 0) >= 1 and left == []
          and pids and len(pids) == 2 and alive == [])
    return (('PASS' if ok else 'FAIL'), 'cause %s rc %s confirmed %s killed %s left_now %s elapsed %.1f s; pids %s still alive %s' % (
        cause, rc, end.get('confirmed'), end.get('killed'), left, el, pids, alive), {'end': end})


def _child_chain(d, name, tmo):
    wtext(os.path.join(d, 'runner.sh'), RUNNER_SLEEP)
    wtext(os.path.join(d, 'child_chain.py'), CHILD_CHAIN)
    p = spawn([sys.executable, '-I', '-B', os.path.join(d, 'child_chain.py'), os.path.join(A.repo, 'scripts'), d, name, str(tmo)],
              os.path.join(d, 'child_stdout.log'))
    L = wait_launch(d, name)
    return p, L


def c11():
    d = mkd('c11_sigterm')
    p, L = _child_chain(d, 'S11_run', 120.0)
    if L is None:
        kill_kid(p)
        return 'FAIL', 'launch record with runner pid did not appear within 30 s', {}
    remember(L)
    time.sleep(0.5)
    os.kill(p.pid, signal.SIGTERM)
    try:
        p.wait(timeout=90)
    except subprocess.TimeoutExpired:
        kill_kid(p)
        return 'FAIL', 'chain-like child did not finish within 90 s after SIGTERM', {}
    res = read_json(os.path.join(d, 'child_result.json'))
    end = res.get('end') or {}
    left = members(L['token'])
    pids, alive = still_alive(d, L['token'])
    ok = (p.returncode == 0 and res.get('cause') == 'signal' and end.get('signal') == 'SIGTERM' and end.get('confirmed') is True
          and (end.get('killed') or 0) >= 1 and left == [] and pids and len(pids) == 2 and alive == [])
    return (('PASS' if ok else 'FAIL'), 'child rc %s cause %s signal %s confirmed %s killed %s left_now %s; pids %s still alive %s' % (
        p.returncode, res.get('cause'), end.get('signal'), end.get('confirmed'), end.get('killed'), left, pids, alive), {'end': end})


def c12():
    d = mkd('c12_sigkill_recover')
    p, L = _child_chain(d, 'S12_run', 300.0)
    if L is None:
        kill_kid(p)
        return 'FAIL', 'launch record with runner pid did not appear within 30 s', {}
    remember(L)
    time.sleep(0.5)
    os.kill(p.pid, signal.SIGKILL)
    p.wait(timeout=30)
    endp = os.path.join(d, 'groups', 'S12_run.end.json')
    end_before = os.path.exists(endp)
    alive = members(L['token'])
    r = subprocess.run([sys.executable, '-I', '-B', os.path.join(A.repo, 'scripts', 'rint_r_chain.py'), '--stage', 'recover',
                        '--out', d], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
    with open(os.path.join(d, 'recover_output.log'), 'wb') as f:
        f.write(r.stdout)
    er = read_json(endp) if os.path.exists(endp) else {}
    left = members(L['token'])
    pids, still = still_alive(d, L['token'])
    ok = (not end_before and isinstance(alive, list) and len(alive) >= 1 and r.returncode == 0 and er.get('by') == 'recover'
          and er.get('cause') == 'parent_dead' and er.get('confirmed') is True and left == [] and pids and len(pids) == 2
          and still == [])
    det = ('end record before recover %s; group alive after parent SIGKILL %s; recover rc %s; end by %s cause %s confirmed %s '
           'killed %s unsure %s; left_now %s; pids %s still alive %s' % (
               end_before, None if alive is None else len(alive), r.returncode, er.get('by'), er.get('cause'), er.get('confirmed'),
               er.get('killed'), er.get('unsure'), left, pids, still))
    return ('PASS' if ok else 'FAIL'), det, {'end': er}


def _lock_holder(d, repo, mode, tag):
    ready = os.path.join(d, 'ready_' + tag)
    p = spawn([sys.executable, '-I', '-B', os.path.join(d, 'child_lock.py'), os.path.join(A.repo, 'scripts'), repo, mode, ready],
              os.path.join(d, 'holder_%s.log' % tag))
    if not wait_file(ready, 20.0):
        kill_kid(p)
        raise RuntimeError('lock holder (%s) did not report within 20 s' % tag)
    return p


def _try_lock(repo, exclusive, wait):
    t = time.time()
    try:
        with RR.ledger_lock(repo, exclusive=exclusive, wait=wait):
            got = 'acquired'
    except RR.Stop as e:
        got = 'stop:' + e.code
    except OSError as e:                                      # e.g. ENOLCK / EOPNOTSUPP: flock not supported here
        got = 'oserror:%s' % e.errno
    return got, round(time.time() - t, 2)


def c13():
    d = mkd('c13_flock')
    repo = os.path.join(d, 'scratch_ledger_lock')
    os.makedirs(repo)
    RR.ledger_git(repo, 'init', '-q')
    wtext(os.path.join(d, 'child_lock.py'), CHILD_LOCK)
    lp = str(RR._ledger_lock_path(repo))
    out = {'lock_path_in_git_dir': lp.startswith(os.path.join(repo, '.git'))}
    p = _lock_holder(d, repo, 'ex', 'ex1')
    out['ex_vs_ex'] = _try_lock(repo, True, 1.0)
    out['sh_vs_ex'] = _try_lock(repo, False, 1.0)
    os.killpg(p.pid, signal.SIGKILL)
    p.wait(timeout=15)
    out['ex_after_holder_sigkill'] = _try_lock(repo, True, 5.0)
    p2 = _lock_holder(d, repo, 'sh', 'sh1')
    out['sh_vs_sh'] = _try_lock(repo, False, 1.0)
    out['ex_vs_sh'] = _try_lock(repo, True, 1.0)
    kill_kid(p2)
    stop = 'stop:ATTEMPT_LEDGER_MISMATCH'
    ok = (out['lock_path_in_git_dir'] and out['ex_vs_ex'][0] == stop and out['ex_vs_ex'][1] >= 0.9 and out['sh_vs_ex'][0] == stop
          and out['ex_after_holder_sigkill'][0] == 'acquired' and out['sh_vs_sh'][0] == 'acquired' and out['ex_vs_sh'][0] == stop)
    return ('PASS' if ok else 'FAIL'), ' '.join('%s=%s' % (k, v[0] if isinstance(v, tuple) else v) for k, v in out.items()), out


def c13b():
    d = mkd('c13b_readonly_ledger')
    repo = os.path.join(d, 'scratch_ledger_ro')
    os.makedirs(repo)
    RR.ledger_git(repo, 'init', '-q')
    g = os.path.join(repo, '.git')
    os.chmod(g, 0o555)
    try:
        can_write = os.access(g, os.W_OK)
        ex = _try_lock(repo, True, 1.0)[0]
        sh = _try_lock(repo, False, 1.0)[0]
    finally:
        os.chmod(g, 0o755)
    if can_write:
        return 'INFO', 'read-only .git is still writable for this user (root or FS ignores modes): ex=%s sh=%s' % (ex, sh), {
            'can_write': True, 'ex': ex, 'sh': sh}
    ok = ex == 'stop:ATTEMPT_LEDGER_MISMATCH' and sh == 'acquired'
    return ('PASS' if ok else 'FAIL'), 'exclusive=%s shared=%s (expected stop / acquired-without-lock)' % (ex, sh), {
        'can_write': False, 'ex': ex, 'sh': sh}


def c14():
    d = mkd('c14_ledger_git')
    repo = os.path.join(d, 'scratch_ledger_NOT_PRODUCTION')
    os.makedirs(repo)
    RR.ledger_git(repo, 'init', '-q')
    data = {'repo_problem': RR.ledger_repo_problem(repo)}
    head = {'kind': 'header', 'schema': RR.LEDGER_SCHEMA, 'plan_sha256': hashlib.sha256(b'siteq-scratch-not-a-plan').hexdigest(),
            'utc': RR._utc()}
    hb = RR.ledger_line(head).encode('utf-8')
    RR.ledger_parse(hb)
    lp = os.path.join(repo, RR.LEDGER_FILE)
    with RR.ledger_lock(repo, exclusive=True):
        with open(lp, 'xb') as f:
            f.write(hb)
            f.flush()
            os.fsync(f.fileno())
        RR.ledger_git(repo, 'add', '--', RR.LEDGER_FILE)
        RR.ledger_git(repo, 'commit', '-q', '-m', 'siteq scratch header (not a production ledger)', '--', RR.LEDGER_FILE)
    h0, raw0 = RR.ledger_now(repo)
    e1 = {'kind': 'entry', 'n': 1, 'target': 'ladder:P0', 'machine': A.machine, 'resume_of': None, 'plan_sha256': head['plan_sha256'],
          'code_key_sha256': hashlib.sha256(b'siteq').hexdigest(), 'env': {'siteq': 'scratch'}, 'bed': {'siteq': 'scratch'},
          'utc': RR._utc()}
    h1 = RR.ledger_append(repo, e1, 'siteq scratch entry (not a production ledger)', expect=raw0)
    e2 = dict(e1, n=2, target='ladder:P1')
    try:
        RR.ledger_append(repo, e2, 'siteq stale append (must be refused)', expect=raw0)
        stale = 'appended'
    except RR.Stop as e:
        stale = 'stop:' + e.code
    h_after, _raw = RR.ledger_now(repo)
    data.update(head0=h0, head1=h1, history_problem=RR.ledger_history_problem(repo, h1),
                is_ancestor=RR.ledger_is_ancestor(repo, h0, h1), stale_append=stale, head_after_stale=h_after)
    data['bundle_sha256'] = RR.ledger_bundle(repo, h1, os.path.join(d, 'scratch_ledger.bundle'))
    hooks = []
    hd = os.path.join(repo, '.git', 'hooks')
    if os.path.isdir(hd):
        hooks = sorted(n for n in os.listdir(hd) if not n.endswith('.sample') and os.access(os.path.join(hd, n), os.X_OK))
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    gl = subprocess.run(['git', 'config', '--global', '--get', 'core.hooksPath'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, env=env, timeout=30)
    data['active_hooks_in_template'] = hooks
    data['global_core_hooksPath'] = gl.stdout.decode('utf-8', 'replace').strip() or None
    ok = (data['repo_problem'] is None and RR._hex40(h1) and not (h1 == h0) and data['history_problem'] is None
          and data['is_ancestor'] is True and stale == 'stop:ATTEMPT_LEDGER_MISMATCH' and h_after == h1
          and isinstance(data['bundle_sha256'], str) and len(data['bundle_sha256']) == 64)
    st = 'PASS' if ok else 'FAIL'
    det = 'init/commit/append/history/ancestor/stale-refusal/bundle ok' if ok else json.dumps(data, sort_keys=True)[:300]
    if ok and (hooks or data['global_core_hooksPath']):
        st, det = 'WARN', 'git hooks would run on ledger commits: template %s, core.hooksPath %s' % (hooks, data['global_core_hooksPath'])
    return st, det, data


def c15():
    d = mkd('c15_atomic')
    p = os.path.join(d, 'x.json')
    RR.write_json_atomic(p, {'k': 'siteq', 'v': 1})
    first = open(p, 'rb').read() == RR.canon_bytes({'k': 'siteq', 'v': 1})
    RR.write_json_atomic(p, {'k': 'siteq', 'v': 2})
    second = open(p, 'rb').read() == RR.canon_bytes({'k': 'siteq', 'v': 2})
    leftovers = [n for n in os.listdir(d) if '.tmp.' in n]
    try:
        RR._write_new_json(p, {'k': 'again'})
        excl = 'overwrote'
    except FileExistsError:
        excl = 'FileExistsError'
    try:
        fd = os.open(d, os.O_RDONLY)
        try:
            os.fsync(fd)
            dsync = 'ok'
        finally:
            os.close(fd)
    except OSError as e:
        dsync = 'errno %s' % e.errno
    ok = first and second and not leftovers and excl == 'FileExistsError'
    st = 'PASS' if ok else 'FAIL'
    det = 'write/replace ok, no temp leftovers, new-file refusal ok, directory fsync %s' % dsync
    if ok and not dsync == 'ok':
        st, det = 'WARN', det + ' (rint_first_result.write_mark tolerates this; durability of the rename is then not forced)'
    return st, det if ok else 'first %s second %s leftovers %s excl %s' % (first, second, leftovers, excl), {'dir_fsync': dsync}


def c16():
    d = mkd('c16_special_files')
    wtext(os.path.join(d, 'reg'), 'abc')
    wtext(os.path.join(d, 'empty'), '')
    os.symlink(os.path.join(d, 'no_such_target'), os.path.join(d, 'dangling'))
    os.makedirs(os.path.join(d, 'dir'))
    wtext(os.path.join(d, 'mode000'), 'abc', 0o000)
    os.makedirs(os.path.join(d, 'logs'))
    wtext(os.path.join(d, 'logs', 'R02_reg.log'), 'hello')
    os.makedirs(os.path.join(d, 'att_fifo'))
    os.makedirs(os.path.join(d, 'dig_fifo'))
    os.makedirs(os.path.join(d, 'dig_plain'))
    wtext(os.path.join(d, 'dig_plain', 'a.txt'), 'a')
    wtext(os.path.join(d, 'dig_fifo', 'a.txt'), 'a')
    fifo_ok = True
    try:
        for f in ('fifo', os.path.join('logs', 'R01_fifo.log'), os.path.join('att_fifo', 'attempt.json'), os.path.join('dig_fifo', 'b')):
            os.mkfifo(os.path.join(d, f))
    except OSError as e:
        fifo_ok = 'mkfifo failed: errno %s' % e.errno
    wtext(os.path.join(d, 'child_files.py'), CHILD_FILES)
    can_read_000 = os.access(os.path.join(d, 'mode000'), os.R_OK)
    try:
        r = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, 'child_files.py'), os.path.join(A.repo, 'scripts'), d],
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    except subprocess.TimeoutExpired:
        os.chmod(os.path.join(d, 'mode000'), 0o600)
        return 'FAIL', 'reader blocked for 30 s (FIFO / special file opened in blocking mode on this site?)', {}
    os.chmod(os.path.join(d, 'mode000'), 0o600)
    if not r.returncode == 0:
        return 'ERROR', 'child rc %s: %s' % (r.returncode, r.stderr.decode('utf-8', 'replace')[-300:]), {}
    got = json.loads(r.stdout.decode('utf-8'))
    m000 = 'ok' if can_read_000 else 'unreadable'
    want = {'reg': ['ok', 3], 'empty': ['ok', 0], 'missing': ['missing', None], 'dangling': ['missing', None],
            'dir': ['unreadable', None], 'devnull': ['unreadable', None], 'mode000': [m000, 3 if m000 == 'ok' else None],
            'log_reg': ['ok', 5], 'log_badname': ['no_run', 0], 'digest_plain': got.get('digest_plain')}
    if fifo_ok is True:
        want.update({'fifo': ['unreadable', None], 'log_fifo': ['unreadable', 0], 'group_json_fifo': None, 'summary_fifo': 'unreadable',
                     'attempt_fifo': None, 'digest_with_fifo': None})
    bad = sorted(k for k in want if not (got.get(k) == want[k]))
    plain_ok = isinstance(got.get('digest_plain'), str) and len(got['digest_plain']) == 64
    ok = not bad and plain_ok
    st = 'PASS' if ok else 'FAIL'
    det = 'all special-file cases as expected' if ok else 'mismatch %s' % bad
    if ok and fifo_ok is not True:
        st, det = 'SKIP', 'FIFO cases skipped (%s); other cases as expected' % fifo_ok
    return st, det, {'got': got, 'expected': want, 'mode000_expected': m000, 'fifo': fifo_ok}


def c16b():
    d = mkd('c16b_unlink_open')
    p = os.path.join(d, 'victim')
    f = open(p, 'w')
    f.write('x')
    f.flush()
    os.unlink(p)
    seen = sorted(os.listdir(d))
    f.close()
    time.sleep(0.2)
    after = sorted(os.listdir(d))
    nfs_like = [n for n in seen + after if n.startswith('.nfs')]
    if nfs_like:
        return ('WARN', 'unlink of an open file left %s (NFS silly-rename): such files would change folder_digest / '
                        'outdir-empty checks while a process holds them' % nfs_like[:3], {'seen': seen, 'after': after})
    return 'PASS', 'unlink of an open file leaves no visible entry', {'seen': seen, 'after': after}


def c17():
    d = mkd('c17_chmod')
    p = wtext(os.path.join(d, 'verdict_results_like.json'), '{}')
    os.chmod(p, 0o600)
    mode = stat.S_IMODE(os.stat(p).st_mode)
    ok = mode == 0o600
    return ('PASS' if ok else 'FAIL'), 'mode after chmod 0600 = %o (verdict_results.json value seal relies on it)' % mode, {'mode': '%o' % mode}


def c18():
    old = os.umask(0o022)
    os.umask(old)
    d = mkd('c18_umask')
    p = wtext(os.path.join(d, 'new.json'), '{}')
    mode = stat.S_IMODE(os.stat(p).st_mode)
    return 'INFO', 'umask %03o, new file mode %o (chain writes records and logs with the process umask)' % (old, mode), {
        'umask': '%03o' % old, 'new_file_mode': '%o' % mode}


def c19():
    d = mkd('c19_copy')
    src = os.path.join(d, 'src')
    os.makedirs(os.path.join(src, 'sub'))
    wtext(os.path.join(src, 'a.txt'), 'alpha\n')
    with open(os.path.join(src, 'sub', 'b.bin'), 'wb') as f:
        f.write(os.urandom(4096))
    dst = os.path.join(d, 'dst')
    shutil.copytree(src, dst, symlinks=True)
    os.makedirs(os.path.join(d, 'dst2'))
    shutil.copy2(os.path.join(src, 'a.txt'), os.path.join(d, 'dst2', 'a.txt'))
    a, b = RR.folder_digest(src), RR.folder_digest(dst)
    mt = os.stat(os.path.join(src, 'a.txt')).st_mtime_ns == os.stat(os.path.join(d, 'dst2', 'a.txt')).st_mtime_ns
    ok = a is not None and a == b
    return ('PASS' if ok else 'FAIL'), 'copytree/copy2 ok, folder_digest equal %s, copy2 mtime preserved %s' % (a == b, mt), {
        'digest_src': a, 'digest_dst': b, 'mtime_preserved': mt}


def c20():
    import tempfile
    td = tempfile.gettempdir()
    info = mount_of(td)
    ok = os.path.isdir(td) and os.access(td, os.W_OK | os.X_OK)
    st = 'INFO' if ok else 'FAIL'
    return st, 'TMPDIR %s fstype %s free %s bytes (verdict/reverify graph source uses mkdtemp here; not written by this probe)' % (
        td, info.get('fstype'), info.get('free_bytes')), info


def c21():
    old = RR._signal_handlers(RR._raise_chain_signal)
    got = sorted(signal.Signals(s).name for s in (old or {}))
    RR._signal_restore(old)
    restored = signal.getsignal(signal.SIGTERM) is (old or {}).get(signal.SIGTERM)
    ok = got == ['SIGHUP', 'SIGTERM'] and restored
    return ('PASS' if ok else 'FAIL'), 'handlers installed for %s, restored %s' % (got, restored), {}


def c22():
    out = {}
    t = time.time()
    out['nvidia_smi'] = RR._try(RR._env_gpu)
    out['nvidia_smi_seconds'] = round(time.time() - t, 2)
    t = time.time()
    np_ = None
    try:
        import numpy as np_
    except Exception:                                         # noqa: BLE001
        np_ = None
    blas = RR._try(lambda: RR._env_blas(np_))
    out['blas_probe_seconds'] = round(time.time() - t, 2)
    out['blas_kind'] = type(blas).__name__
    t = time.time()
    r = subprocess.run(['git', '-C', A.repo, 'rev-parse', 'HEAD'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=60)
    out['git_rev_parse_seconds'] = round(time.time() - t, 2)
    out['git_rev_parse_rc'] = r.returncode
    out['git_top'] = RR._git_top(A.repo)
    gv = subprocess.run(['git', '--version'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, timeout=30)
    out['git_version'] = gv.stdout.decode('ascii', 'replace').strip()
    bv = subprocess.run(['bash', '-c', 'echo $BASH_VERSION'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, timeout=30)
    out['bash_version'] = bv.stdout.decode('ascii', 'replace').strip()
    out['usr_bin_time'] = os.access('/usr/bin/time', os.X_OK)
    slow = out['nvidia_smi_seconds'] > 15 or out['blas_probe_seconds'] > 100
    st = 'WARN' if slow else 'INFO'
    det = 'nvidia-smi %.2f s (timeout 20), BLAS probe %.2f s (timeout 120), git rev-parse %.2f s, %s, bash %s' % (
        out['nvidia_smi_seconds'], out['blas_probe_seconds'], out['git_rev_parse_seconds'], out['git_version'], out['bash_version'])
    return st, det, out


def c23():
    import locale
    data = {'stdout_encoding': sys.stdout.encoding, 'utf8_mode': sys.flags.utf8_mode,
            'preferred': locale.getpreferredencoding(False),
            'LANG': os.environ.get('LANG'), 'LC_ALL': os.environ.get('LC_ALL'), 'LC_CTYPE': os.environ.get('LC_CTYPE'),
            'PYTHONIOENCODING': os.environ.get('PYTHONIOENCODING'), 'PYTHONUTF8': os.environ.get('PYTHONUTF8')}
    res = {}
    for tag, argv in (('isolated', [sys.executable, '-I', '-B', '-c', ENC_SNIPPET]), ('production_like', [sys.executable, '-B', '-c', ENC_SNIPPET])):
        r = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        res[tag] = {'rc': r.returncode, 'tail': r.stdout.decode('utf-8', 'replace').strip().splitlines()[-1:],
                    'err': r.stderr.decode('utf-8', 'replace').strip()[-200:]}
    data['children'] = res
    ok = all(v['rc'] == 0 for v in res.values())
    det = 'chain-style non-ASCII text to a pipe: isolated rc %s, production-like rc %s (%s)' % (
        res['isolated']['rc'], res['production_like']['rc'], (res['production_like']['tail'] or [''])[0])
    return ('PASS' if ok else 'FAIL'), det, data


def c24():
    import resource
    out = {}
    for nm in ('RLIMIT_NOFILE', 'RLIMIT_NPROC', 'RLIMIT_AS', 'RLIMIT_DATA', 'RLIMIT_CORE', 'RLIMIT_CPU', 'RLIMIT_FSIZE'):
        if hasattr(resource, nm):
            s, h = resource.getrlimit(getattr(resource, nm))
            out[nm] = [None if s == resource.RLIM_INFINITY else s, None if h == resource.RLIM_INFINITY else h]
    capped = [k for k in ('RLIMIT_AS', 'RLIMIT_DATA', 'RLIMIT_CPU', 'RLIMIT_FSIZE') if out.get(k, [None])[0] is not None]
    st = 'WARN' if capped else 'INFO'
    return st, 'limits (soft, hard; None = unlimited) %s' % json.dumps(out, sort_keys=True) + (
        '; capped: %s' % capped if capped else ''), out


def _readf(p):
    try:
        with open(p, encoding='ascii', errors='replace') as f:
            return f.read().strip()
    except OSError:
        return None


def c25():
    mi = {}
    for ln in (_readf('/proc/meminfo') or '').splitlines():
        k, _sep, v = ln.partition(':')
        if k in ('MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree'):
            mi[k + '_kB'] = int(v.split()[0])
    cg = {'self_cgroup': (_readf('/proc/self/cgroup') or '').splitlines()[:6]}
    for ln in cg['self_cgroup']:
        parts = ln.split(':', 2)
        if len(parts) == 3 and parts[0] == '0':
            base = '/sys/fs/cgroup' + parts[2]
            for nm in ('memory.max', 'memory.high', 'memory.swap.max', 'memory.oom.group', 'pids.max'):
                cg[nm] = _readf(os.path.join(base, nm))
        elif len(parts) == 3 and 'memory' in parts[1].split(','):
            cg['v1_memory.limit_in_bytes'] = _readf('/sys/fs/cgroup/memory' + parts[2] + '/memory.limit_in_bytes')
    cg['vm.overcommit_memory'] = _readf('/proc/sys/vm/overcommit_memory')
    cg['kernel.pid_max'] = _readf('/proc/sys/kernel/pid_max')
    return 'INFO', 'MemTotal %s kB, MemAvailable %s kB, swap %s kB, cgroup memory.max %s' % (
        mi.get('MemTotal_kB'), mi.get('MemAvailable_kB'), mi.get('SwapTotal_kB'), cg.get('memory.max')), {'meminfo': mi, 'cgroup': cg}


def c26():
    paths = [('out', A.out), ('repo', A.repo), ('home', os.path.expanduser('~'))]
    paths += [('plan_dir', p) for p in A.plan_dirs.split(':') if p]
    rows = {}
    for tag, p in paths:
        rows['%s:%s' % (tag, p)] = mount_of(p)
    net = [k for k, v in rows.items() if is_netfs(v.get('fstype'))]
    vol = [k for k, v in rows.items() if (v.get('fstype') or '') in ('tmpfs', 'ramfs')]
    outdev = rows['out:%s' % A.out].get('st_dev')
    other = [k for k, v in rows.items() if k.startswith('plan_dir:') and v.get('exists') and not (v.get('st_dev') == outdev)]
    ro = [k for k, v in rows.items() if k.startswith('plan_dir:') and v.get('exists') and v.get('writable') is False]
    missing = [k for k, v in rows.items() if k.startswith('plan_dir:') and not v.get('exists')]
    st, notes = 'PASS', []
    if net:
        st = 'WARN'
        notes.append('network/FUSE filesystem: %s (flock across hosts, silly-rename, attribute caching not provable here)' % net)
    if other:
        st = 'WARN'
        notes.append('plan dirs on another filesystem than the siteq folder: %s -> rerun with SITEQ_BASE on that filesystem' % other)
    if vol:
        st = 'WARN'
        notes.append('volatile filesystem (contents lost on reboot): %s' % vol)
    if ro:
        st = 'WARN'
        notes.append('plan dirs not writable: %s' % ro)
    if missing:
        notes.append('plan dirs missing (not created yet?): %s' % missing)
    summ = ', '.join('%s=%s' % (k.split(':', 1)[0], v.get('fstype')) for k, v in rows.items())
    return st, summ + ('; ' + '; '.join(notes) if notes else ''), rows


def c27():
    pm = mount_of('/proc')
    pidmax = _readf('/proc/sys/kernel/pid_max')
    hp = [o for o in (pm.get('mount_opts', '') + ',' + pm.get('super_opts', '')).split(',') if o.startswith('hidepid') or o.startswith('subset')]
    return 'INFO', '/proc options %s, pid_max %s' % (hp or 'default', pidmax), {'proc': pm, 'pid_max': pidmax}


def c28():
    out = {'nvidia_smi_path': shutil.which('nvidia-smi')}
    if out['nvidia_smi_path']:
        try:
            r = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version,memory.total', '--format=csv,noheader'],
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
            out['rc'] = r.returncode
            out['gpus'] = [x.strip() for x in r.stdout.decode('utf-8', 'replace').splitlines() if x.strip()]
        except subprocess.TimeoutExpired:
            out['rc'] = 'timeout'
    try:
        import importlib.metadata as md
        out['cupy_dists'] = sorted('%s %s' % (x.metadata.get('Name'), x.version) for x in md.distributions()
                                   if str(x.metadata.get('Name') or '').lower().startswith('cupy'))
    except Exception as e:                                    # noqa: BLE001
        out['cupy_dists'] = 'error %s' % type(e).__name__
    gpus = out.get('gpus') or []
    st = 'INFO' if gpus and out.get('cupy_dists') else 'WARN'
    return st, 'GPUs %s, cupy %s (R runs use EXPECT_BACKEND=gpu; the chain only records this)' % (gpus, out.get('cupy_dists')), out


def c29():
    out = {'cpu_count': os.cpu_count(), 'affinity': len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None,
           'platform': platform.platform(), 'kernel': platform.release(), 'machine': platform.machine(),
           'os_release': None, 'ntp_synchronized': None,
           'launch_tools': {k: bool(shutil.which(k)) for k in ('tmux', 'screen', 'setsid', 'nohup')}}
    for ln in (_readf('/etc/os-release') or '').splitlines():
        if ln.startswith('PRETTY_NAME='):
            out['os_release'] = ln.split('=', 1)[1].strip('"')
    if shutil.which('timedatectl'):
        try:
            r = subprocess.run(['timedatectl', 'show', '-p', 'NTPSynchronized', '--value'], stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10)
            out['ntp_synchronized'] = r.stdout.decode('ascii', 'replace').strip() or None
        except subprocess.TimeoutExpired:
            out['ntp_synchronized'] = 'timeout'
    return 'INFO', '%s, cpus %s (affinity %s), NTP synchronized %s, launch tools %s' % (
        out['os_release'], out['cpu_count'], out['affinity'], out['ntp_synchronized'],
        ','.join(k for k, v in sorted(out['launch_tools'].items()) if v) or 'none'), out


def c99():
    r = subprocess.run(['git', '-C', A.repo, 'rev-parse', 'HEAD'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=60)
    head = r.stdout.decode('ascii', 'replace').strip()
    s = subprocess.run(['git', '-C', A.repo, 'status', '--porcelain', '--untracked-files=normal'], stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    dirty = s.stdout.decode('utf-8', 'replace').strip()
    pyc = os.path.join(A.repo, 'scripts', '__pycache__')
    after = os.stat(pyc).st_mtime_ns if os.path.isdir(pyc) else None
    ok = head == A.pin and r.returncode == 0 and s.returncode == 0 and not dirty
    st = 'PASS' if ok else 'FAIL'
    det = 'checkout still at pin and clean' if ok else 'head %s rc %s status rc %s dirty %r' % (head, r.returncode, s.returncode, dirty[:200])
    if ok and not (after == A.pyc_before):
        st, det = 'WARN', det + ('; scripts/__pycache__ changed during the probe (ignored files; this probe runs python with -B, '
                                 'so another process on this machine probably wrote them)')
    return st, det, {'head': head, 'pycache_mtime_before': A.pyc_before, 'pycache_mtime_after': after}


CHECKS = [
    ('C01', 'import scripts/rint_r_chain.py from the pinned checkout', c01, 120),
    ('C02', 'environment unit (python minor, numpy, scipy) vs kgy reference', c02, 240),
    ('C02b', 'PATH python3 (used by runner -> payload) has the same env unit', c02b, 180),
    ('C03', 'git_identity: HEAD == PIN, dirty False, repo-relative path', c03, 180),
    ('C04', 'code_record + code_dirty_problem (same-code gate) and code_key_sha256', c04, 180),
    ('C05', 'host_ident: machine_id, boot_id, pid namespace', c05, 60),
    ('C06', '/proc/<pid>/stat, /proc/uptime ticks, /proc/self/status uid', c06, 60),
    ('C07', 'chain_parent_alive on a live parent, a reaped child, a reused pid', c07, 60),
    ('C08', 'group_members scan of the real process table (fresh token)', c08, 120),
    ('C09', 'run_in_group: runner exits 0 leaving same-group and setsid children', c09, 120),
    ('C10', 'run_in_group: timeout -> killpg + token sweep', c10, 120),
    ('C11', 'chain-like child gets SIGTERM while waiting -> group killed, end record', c11, 180),
    ('C12', 'chain-like child SIGKILLed -> group survives -> --stage recover kills and confirms', c12, 300),
    ('C13', 'ledger_lock flock semantics on the siteq filesystem (2 processes)', c13, 180),
    ('C13b', 'ledger_lock on a read-only ledger .git', c13b, 60),
    ('C14', 'scratch ledger git ops (init, commit, append, history, stale refusal, bundle)', c14, 240),
    ('C15', 'write_json_atomic (temp + fsync + os.replace), new-file refusal, directory fsync', c15, 60),
    ('C16', 'read_regular_file & co on regular/empty/missing/dangling/dir/FIFO/device/mode-000 files', c16, 90),
    ('C16b', 'unlink of an open file (NFS silly-rename detector)', c16b, 30),
    ('C17', 'chmod 0600 takes effect (verdict_results.json value seal)', c17, 30),
    ('C18', 'process umask and resulting file mode', c18, 30),
    ('C19', 'shutil.copytree/copy2 (resume and merge copies) + folder_digest equality', c19, 60),
    ('C20', 'TMPDIR facts (no write)', c20, 30),
    ('C21', 'SIGTERM/SIGHUP handler install and restore (main thread)', c21, 30),
    ('C22', 'timings of chain subprocess helpers (nvidia-smi, BLAS probe, git), git/bash versions', c22, 240),
    ('C23', 'stdout encoding for the chain prints (non-ASCII text to a pipe)', c23, 120),
    ('C24', 'resource limits', c24, 30),
    ('C25', 'memory, swap, cgroup limits (no allocation)', c25, 30),
    ('C26', 'filesystem type, free space, inodes, writability (siteq, repo, home, plan dirs)', c26, 60),
    ('C27', '/proc mount options and pid_max', c27, 30),
    ('C28', 'GPU and cupy presence (record only, no CUDA context)', c28, 60),
    ('C29', 'OS, CPUs, clock sync (record only)', c29, 60),
    ('C99', 'pinned checkout untouched after the probe', c99, 180),
]


def main():
    global A
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--pin', required=True)
    ap.add_argument('--machine', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--expect-py', required=True)
    ap.add_argument('--expect-numpy', required=True)
    ap.add_argument('--expect-scipy', required=True)
    ap.add_argument('--plan-dirs', default='')
    A = ap.parse_args()
    A.repo = os.path.abspath(A.repo)
    A.out = os.path.abspath(A.out)
    A.pyc_before = None
    try:
        sys.stdout.reconfigure(errors='backslashreplace', line_buffering=True)
    except (AttributeError, ValueError):
        pass
    here = os.path.dirname(os.path.realpath(__file__))
    inside = (os.path.realpath(A.out) + os.sep).startswith(os.path.realpath(A.repo) + os.sep)
    if not here == os.path.realpath(A.out) or inside or not os.path.isdir(os.path.join(A.repo, 'scripts')):
        print('[siteq] setup problem: --out must be the new folder that holds this probe (outside the checkout), '
              '--repo must hold scripts/')
        return 2
    t0 = time.time()
    started = utc()
    print('[siteq] %s  machine %s  pin %s  uid %d  python %s' % (PROBE, A.machine, A.pin, os.getuid(), platform.python_version()),
          flush=True)
    rc = 0
    try:
        for cid, title, fn, budget in CHECKS:
            if RR is None and not cid == 'C01':
                add(cid, title, 'SKIP', 'chain module not imported')
                continue
            check(cid, title, fn, budget)
    except KeyboardInterrupt:
        add('C00', 'interrupted', 'ERROR', 'KeyboardInterrupt (partial result)')
    finally:
        for p in KIDS:
            kill_kid(p)
        if RR is not None:
            for tok, (since, run) in list(TOKENS.items()):
                RR.GROUP_SINCE[tok] = since
                if run:
                    RR.GROUP_RUN[tok] = run
                try:
                    RR.group_settle(tok)
                except Exception:                             # noqa: BLE001
                    pass
                finally:
                    RR.GROUP_SINCE.pop(tok, None)
                    RR.GROUP_RUN.pop(tok, None)
                    RR.GROUP_SCAN.pop(tok, None)
            swept = own_sweep(list(TOKENS))                   # scanner-independent: only processes positively carrying our tokens
            if swept:
                add('C98', 'final cleanup found processes the chain sweep had left', 'WARN',
                    '%d process(es) with a probe token were still alive at the end and were killed now' % swept)
        counts = {}
        for r in RES:
            counts[r['status']] = counts.get(r['status'], 0) + 1
        res = {'schema': RESULT_SCHEMA, 'probe': PROBE, 'probe_sha256': sha_file(os.path.abspath(__file__)), 'machine': A.machine,
               'pin': A.pin, 'repo': A.repo, 'out': A.out, 'uid': os.getuid(), 'euid': os.geteuid(),
               'expect': {'python_minor': A.expect_py, 'numpy': A.expect_numpy, 'scipy': A.expect_scipy}, 'plan_dirs': A.plan_dirs,
               'utc_start': started, 'utc_end': utc(), 'seconds': round(time.time() - t0, 1), 'counts': counts, 'checks': RES}
        tmp = os.path.join(A.out, 'siteq_result.json.tmp')
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(json.dumps(res, sort_keys=True, indent=1, ensure_ascii=True, default=str) + '\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, os.path.join(A.out, 'siteq_result.json'))
        bad = [r for r in RES if r['status'] in ('FAIL', 'ERROR')]
        warn = [r for r in RES if r['status'] == 'WARN']
        print('[siteq] ---- summary: %s  (%.1f s)' % (json.dumps(counts, sort_keys=True), time.time() - t0))
        for r in bad + warn:
            print('[siteq] %s %s: %s' % (r['status'], r['id'], r['detail'][:240]))
        rc = 1 if bad else 0
    return rc


if __name__ == '__main__':
    sys.exit(main())
