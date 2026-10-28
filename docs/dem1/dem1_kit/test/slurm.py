#!/usr/bin/env python3
# Slurm 흉내 v2: sbatch(--parsable --hold --dependency=afterany) · squeue · scancel · scontrol release · sacct · 스케줄러(의존·보류·QoS 코어 상한·시간제한 TIMEOUT)
import sys, os, json, re, time, signal, subprocess, fcntl
ST = os.environ.get('MOCK_SLURM_STATE') or sys.exit('MOCK_SLURM_STATE 없음')
DB = os.path.join(ST, 'jobs.json'); CAP = int(os.environ.get('MOCK_QOS_CAP', '60'))
TERM = ('COMPLETED', 'FAILED', 'CANCELLED', 'TIMEOUT')
def load():
    if not os.path.exists(DB): return {'next': 410001, 'jobs': []}
    return json.load(open(DB))
def save(d):
    tmp = DB + '.tmp'; json.dump(d, open(tmp, 'w'), indent=1); os.replace(tmp, DB)
def lock():
    f = open(os.path.join(ST, 'lock'), 'w'); fcntl.flock(f, fcntl.LOCK_EX); return f
def alive(pid):
    try:
        with open(f'/proc/{pid}/stat') as f: s = f.read()
        return s.split(')')[-1].split()[0] != 'Z'
    except Exception: return False
def group_alive(pgid):
    for p in os.listdir('/proc'):
        if p.isdigit():
            try:
                if os.getpgid(int(p)) == pgid and alive(int(p)): return True
            except Exception: pass
    return False
def killpg(pg, sig):
    try: os.killpg(pg, sig)
    except Exception: pass
def tsec(s):
    m = re.match(r'(?:(\d+)-)?(\d+):(\d+):(\d+)$', s)
    if m: return int(m.group(1) or 0) * 86400 + int(m.group(2)) * 3600 + int(m.group(3)) * 60 + int(m.group(4))
    return int(s) * 60
def sched(d):
    now = time.time()
    for j in d['jobs']:
        if j['state'] == 'RUNNING':
            if group_alive(j['pgid']):
                if now - j['start'] > j['limit'] and not j.get('tl'):
                    j['tl'] = now; killpg(j['pgid'], signal.SIGTERM); killpg(j['pgid'], signal.SIGCONT)
                elif j.get('tl') and now - j['tl'] > 2: killpg(j['pgid'], signal.SIGKILL)
                continue
            rcf = os.path.join(ST, f"{j['id']}.rc")
            if j.get('killed'): fin = 'CANCELLED'
            elif j.get('tl'): fin = 'TIMEOUT'
            elif os.path.exists(rcf): fin = 'COMPLETED' if open(rcf).read().strip() == '0' else 'FAILED'
            else: fin = 'FAILED'
            j['state'] = 'COMPLETING'; j['final'] = fin; j['cg_until'] = now + 2; j['end'] = now
        elif j['state'] == 'COMPLETING' and now >= j['cg_until']:
            j['state'] = j['final']
    used = sum(j['cores'] for j in d['jobs'] if j['state'] in ('RUNNING', 'COMPLETING'))
    for j in sorted(d['jobs'], key=lambda x: x['id']):
        if j['state'] != 'PENDING': continue
        if j.get('held'): j['reason'] = 'JobHeldUser'; continue
        st = {x['id']: x['state'] for x in d['jobs']}
        if any(st.get(dp) not in TERM for dp in j['deps']): j['reason'] = 'Dependency'; continue
        if used + j['cores'] > CAP: j['reason'] = 'QOSMaxCpuPerUserLimit'; continue
        used += j['cores']; launch(j)
    return d
def launch(j):
    env = json.load(open(os.path.join(ST, f"{j['id']}.env")))
    env.update(SLURM_JOB_ID=str(j['id']), SLURM_JOBID=str(j['id']), SLURM_JOB_NAME=j['name'], SLURM_NTASKS=str(j['cores']), SLURM_NPROCS=str(j['cores']),
               SLURM_JOB_NODELIST='node01', SLURM_SUBMIT_DIR=j['workdir'], SLURMD_NODENAME='node01', SLURM_CONF='/etc/slurm/slurm.conf', MOCKJOB=str(j['id']))
    sc = os.path.join(ST, f"{j['id']}.batch"); rcf = os.path.join(ST, f"{j['id']}.rc")
    p = subprocess.Popen(['bash', '-c', f'bash "{sc}" > "{j["out"]}" 2>&1; echo $? > "{rcf}"'], cwd=j['workdir'], env=env, start_new_session=True,
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    j['state'] = 'RUNNING'; j['pgid'] = p.pid; j['start'] = time.time(); j['reason'] = 'node01'
def hms(s):
    s = max(0, int(s)); dd, s = divmod(s, 86400); h, s = divmod(s, 3600); m, s = divmod(s, 60)
    return f'{dd}-{h:02d}:{m:02d}:{s:02d}' if dd else (f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}')
SHORT = {'RUNNING': 'R', 'PENDING': 'PD', 'COMPLETING': 'CG', 'COMPLETED': 'CD', 'CANCELLED': 'CA', 'FAILED': 'F', 'TIMEOUT': 'TO'}
def fmt(spec, j):
    out = ''; pos = 0; now = time.time()
    for m in re.finditer(r'%(\.?)(-?)(\d*)([a-zA-Z])', spec):
        out += spec[pos:m.start()]; pos = m.end(); k = m.group(4)
        run = j['state'] in ('RUNNING', 'COMPLETING')
        el = ((j.get('end') or now) - j['start']) if run else 0
        v = {'i': str(j['id']), 'j': j['name'], 'T': j['state'], 't': SHORT.get(j['state'], j['state']), 'C': str(j['cores']), 'M': hms(el),
             'L': hms(j['limit'] - el), 'S': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(j['start'])) if run else 'N/A',
             'R': j.get('reason', '') if run else '(' + j.get('reason', 'None') + ')', 'P': 'cpu', 'u': 'yonghoon', 'D': '1'}.get(k, '?')
        w = int(m.group(3)) if m.group(3) else 0
        if w: v = v[:w].ljust(w) if m.group(2) else v[:w].rjust(w)
        out += v
    return out + spec[pos:]
def squeue(a):
    lk = lock(); d = sched(load()); save(d); del lk
    o = '%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R'; hdr = True; jid = None; name = None; states = None; i = 0
    while i < len(a):
        x = a[i]
        if x == '-h': hdr = False
        elif x in ('-o', '--format'): o = a[i+1]; i += 1
        elif x.startswith('--format='): o = x.split('=', 1)[1]
        elif x in ('-j', '--jobs'): jid = a[i+1].split(','); i += 1
        elif x in ('-n', '--name'): name = a[i+1]; i += 1
        elif x in ('-u', '--user', '-p'): i += 1
        elif x in ('-t', '--states'): states = a[i+1].upper().split(','); i += 1
        i += 1
    if hdr: print(re.sub(r'%\.?-?\d*([a-zA-Z])', lambda m: {'i': 'JOBID', 'j': 'NAME', 'T': 'STATE', 't': 'ST', 'C': 'CPUS', 'M': 'TIME', 'R': 'NODELIST(REASON)', 'P': 'PARTITION', 'u': 'USER', 'D': 'NODES', 'L': 'TIME_LEFT', 'S': 'START_TIME'}.get(m.group(1), '?'), o))
    for j in d['jobs']:
        if j['state'] not in ('RUNNING', 'PENDING', 'COMPLETING'): continue
        if jid and str(j['id']) not in jid: continue
        if name and j['name'] != name: continue
        if states and j['state'] not in states and SHORT.get(j['state']) not in states: continue
        print(fmt(o, j))
def sbatch(a):
    parsable = hold = False; deps = []; i = 0; script = None
    while i < len(a):
        x = a[i]
        if x == '--parsable': parsable = True
        elif x in ('--hold', '-H'): hold = True
        elif x.startswith('--dependency=') or x == '-d':
            v = x.split('=', 1)[1] if '=' in x else a[i + 1]
            if x == '-d': i += 1
            m = re.match(r'afterany:([\d:]+)$', v)
            if not m: print(f'sbatch: error: mock 은 afterany 만 ({v})', file=sys.stderr); sys.exit(1)
            deps += [int(t) for t in m.group(1).split(':')]
        elif x.startswith('-'): print(f'sbatch: error: mock 모르는 옵션 {x}', file=sys.stderr); sys.exit(1)
        else: script = x
        i += 1
    if os.environ.get('MOCK_REQUIRE_CONF') and os.environ.get('MOCKJOB') and 'SLURM_CONF' not in os.environ:
        print('sbatch: error: s_p_parse_file: unable to status file /etc/slurm/slurm.conf', file=sys.stderr); sys.exit(1)
    if os.environ.get('MOCK_SBATCH_FAIL_IN_JOB') and os.environ.get('MOCKJOB'):
        print('sbatch: error: Batch job submission failed: mock 계산노드 제출 막힘', file=sys.stderr); sys.exit(1)
    txt = open(script).read(); name = os.path.basename(script).rsplit('.', 1)[0]; out = 'slurm-%j.out'; n = 1; lim = 3600
    for l in txt.splitlines():
        if not l.startswith('#SBATCH'): continue
        t = l.split()[1:]
        for k, opt in enumerate(t):
            if opt.startswith('--job-name='): name = opt.split('=', 1)[1]
            elif opt == '-J': name = t[k+1]
            elif opt.startswith('--output='): out = opt.split('=', 1)[1]
            elif opt == '-o': out = t[k+1]
            elif opt.startswith('--ntasks='): n = int(opt.split('=', 1)[1])
            elif opt == '-n': n = int(t[k+1])
            elif opt.startswith('--time='): lim = tsec(opt.split('=', 1)[1])
    if os.environ.get('MOCK_TLIMIT'): lim = int(os.environ['MOCK_TLIMIT'])
    lk = lock(); d = sched(load())
    ids = {j['id'] for j in d['jobs']}
    for dp in deps:
        if dp not in ids: print(f'sbatch: error: Batch job submission failed: Job dependency problem ({dp})', file=sys.stderr); sys.exit(1)
    jid = d['next']; d['next'] += 1
    outp = os.path.join(os.getcwd(), out.replace('%x', name).replace('%j', str(jid)))
    open(os.path.join(ST, f'{jid}.batch'), 'w').write(txt)
    json.dump(dict(os.environ), open(os.path.join(ST, f'{jid}.env'), 'w'))
    d['jobs'].append({'id': jid, 'name': name, 'state': 'PENDING', 'cores': n, 'workdir': os.getcwd(), 'script': os.path.abspath(script), 'deps': deps, 'held': hold,
                      'limit': lim, 'out': outp, 'start': 0, 'submit': time.time(), 'nested': os.environ.get('MOCKJOB', ''), 'had_jobid': 'SLURM_JOB_ID' in os.environ, 'sub_conf': 'SLURM_CONF' in os.environ,
                      'sub_parent': os.environ.get('SLURM_JOB_ID', '')})
    d = sched(d); save(d)
    print(jid if parsable else f'Submitted batch job {jid}')
def scancel(a):
    sig = None; ids = []; i = 0
    while i < len(a):
        if a[i] in ('-s', '--signal'): sig = a[i+1]; i += 1
        elif a[i].startswith('--signal='): sig = a[i].split('=', 1)[1]
        else: ids.append(a[i])
        i += 1
    lk = lock(); d = sched(load()); noop = os.environ.get('MOCK_KILL_NOOP', '').split(',')
    for j in d['jobs']:
        if str(j['id']) not in ids: continue
        if j['state'] == 'PENDING': j['state'] = 'CANCELLED'; j['end'] = time.time(); j['killed'] = True
        elif j['state'] == 'RUNNING':
            if sig and sig.upper() in ('KILL', '9', 'SIGKILL'):
                if j['name'] in noop: continue
                killpg(j['pgid'], signal.SIGKILL)
            else: killpg(j['pgid'], signal.SIGTERM); killpg(j['pgid'], signal.SIGCONT)
            j['killed'] = True
    save(d)
def scontrol(a):
    if a[:1] == ['release']:
        lk = lock(); d = load(); ok = False
        for j in d['jobs']:
            if str(j['id']) in a[1].split(',') and j['state'] == 'PENDING': j['held'] = False; ok = True
        d = sched(d); save(d)
        if not ok: print('scontrol: error: Invalid job id specified', file=sys.stderr); sys.exit(1)
    else: print('scontrol: mock 미지원', file=sys.stderr); sys.exit(1)
def sacct(a):
    lk = lock(); d = sched(load()); save(d); del lk
    for j in d['jobs']: print('|'.join([str(j['id']), j['name'], j['state'], str(j['cores']), ('in-job:' + j['nested']) if j.get('nested') else 'login', 'conf' if j.get('sub_conf') else 'noconf', 'JOBID-LEAK' if j.get('had_jobid') else 'clean', 'held' if j.get('held') else '-', 'deps=' + ','.join(map(str, j['deps']))]))
def daemon(a):
    stopf = os.path.join(ST, 'daemon.stop')
    while not os.path.exists(stopf):
        lk = lock(); d = sched(load()); save(d); del lk; time.sleep(0.5)
cmd = os.path.basename(sys.argv[0])
if cmd == 'slurm.py': cmd = sys.argv[1]; sys.argv = sys.argv[1:]
{'squeue': squeue, 'sbatch': sbatch, 'scancel': scancel, 'scontrol': scontrol, 'sacct': sacct, '_daemon': daemon}[cmd](sys.argv[1:])
