#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""11-12 2 회차 (Rint ② 코드 묶음 · 내부 반박 리뷰 재확인 RCP2-06 · Codex 아님) — git 을 부르는 selftest · 시험 고정물 · 생산 읽기가 부르는 쪽 환경의
`GIT_*` (GIT_DIR · GIT_WORK_TREE · GIT_INDEX_FILE · GIT_OBJECT_DIRECTORY · GIT_ALTERNATE_OBJECT_DIRECTORIES · GIT_COMMON_DIR …) 를 물려받지 않는가.

11-12 밤 실제 사고: 리뷰 조수가 `GIT_DIR=<본 리포>/.git` 을 명령 앞에 붙여 `run_contract.py --selftest` 를 돌렸고, 그 selftest (RCPT-sha) 의 임시 폴더
`git init · add -A · commit` 이 임시 폴더 대신 본 리포 가지에 커밋을 만들었다 (본 세션이 되돌림).  git 훅 (pre-commit · pre-push) 안에서 게이트를 돌려도
git 이 이 변수들을 넣는다 (정직한 흐름).  ⇒ 이 시험은 **이 시험이 만든 일회용 임시 저장소** (피해 저장소 V) 만 가리키는 적대 환경을 **자식 프로세스에만**
넘긴다 — 이 프로세스의 환경은 바꾸지 않는다 · 본 리포 · 작업 트리 저장소를 가리키지 않는다.  적대 꼴 셋: GIT_DIR (사고 꼴) · GIT_DIR + GIT_WORK_TREE +
GIT_INDEX_FILE (훅 꼴) · GIT_OBJECT_DIRECTORY + GIT_COMMON_DIR.  V 상태 = HEAD · ref 전부 · index · config · HEAD reflog · worktrees · stash · 객체 목록.

  G1  run_contract.git_env · drop_git_env — GIT_ 로 시작하는 이름 전부 뺀 사본 (넘긴 사전 그대로) · 제자리 지움 (지운 이름 돌려줌) · 그 밖 이름 그대로
  G2  `run_contract.py --selftest` (RCPT-sha 의 임시 저장소 init · add · commit + payload `_code_sha` 읽기) — 적대 셋에서 V 그대로 · rc · PASS/FAIL 줄 =
      깨끗한 환경과 같음 (고치기 전 = V 에 커밋 · RCPT-sha 둘 FAIL — 11-12 밤 사고 그대로)
  G3  payload `_code_sha` · `_exec_env` (생산 읽기 · 고정물 저장소 F) — 적대 = 깨끗 (V 의 HEAD 를 읽지 않는다) · V 그대로
  G4  `test_step3_gpu_precond.load_base` (기반 판 git show · 시험 모듈 불러오기 = 그 모듈의 GIT_* 지움) — 적대 = 깨끗 = 기준 git show 바이트 · V 그대로
  G5  사슬 `rint_r_chain.git_identity` · `ledger_repo_problem` (생산 읽기) — 적대 = 깨끗 · V 그대로
  G6  이 묶음이 고친 시험 모듈 넷 (test_rint_r_chain `git_` · test_probe6_read `git` · test_cjunc_store_e2e · test_cjunc_store) — 적대 환경에서 그 모듈을
      불러 고정물 저장소를 만들면 (init · add · commit) V 그대로 · 고정물 저장소에 커밋 하나 · 불러온 뒤 그 프로세스 환경에 GIT_* 없음
⚠ 고치기 전 판 = V 에 커밋 · index · 객체가 생기거나 V 의 값을 읽는다 (실패를 기록) — 그 V 는 이 시험이 만든 일회용이다.

  python3 scripts/test_git_env_isolation.py
  python3 scripts/test_git_env_isolation.py --only G2,G6 --keep
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
TOOLS6 = os.path.join(ROOT, 'docs', 'reviews', 'rint2_probe6_prep_20261110', 'tools')
sys.path.insert(0, SCRIPTS)

#: 시험 쪽 기준 (검사 대상 모듈의 도우미를 쓰지 않는다 — 대상과 기준을 가른다): GIT_ 로 시작하는 이름을 뺀 환경
CLEAN = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
GCFG = ['-c', 'user.email=t@t', '-c', 'user.name=t', '-c', 'commit.gpgsign=false', '-c', 'init.defaultBranch=main']
#: 기반 판 (test_step3_gpu_precond.BASE_COMMIT 과 같은 값 — 기준 git show)
PRECOND_BASE = '11a794674'
ARGS = None
TD = None
_ok, _fail = 0, []
CASES = []


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:700]})' if why != '' else ''))
    return cond


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def g(repo, *a, check=True):
    """기준 git (깨끗한 환경 · 고정 신원 · 서명 없음) → stdout."""
    r = subprocess.run(['git', '-C', repo, *GCFG, *a], capture_output=True, text=True, env=CLEAN, stdin=subprocess.DEVNULL)
    if check and r.returncode != 0:
        raise RuntimeError(f'기준 git {a[:2]} rc {r.returncode}: {r.stderr[:300]}')
    return r.stdout


def make_repo(name, files):
    """일회용 저장소 (깨끗한 환경 · 커밋 하나) → 경로."""
    p = os.path.join(TD, name)
    os.makedirs(p)
    g(p, 'init', '-q')
    for rel, text in files.items():
        q = os.path.join(p, rel)
        os.makedirs(os.path.dirname(q), exist_ok=True)
        with open(q, 'w', encoding='utf-8') as f:
            f.write(text)
    g(p, 'add', '-A')
    g(p, 'commit', '-qm', 'fixture')
    return p


def repo_state(v):
    """피해 저장소 V 의 상태 (깨끗한 환경으로 읽음) — HEAD · ref 전부 · index · config · HEAD reflog · worktrees · stash · 객체 목록."""
    gd = os.path.join(v, '.git')

    def fh(rel):
        q = os.path.join(gd, rel)
        return hashlib.sha256(open(q, 'rb').read()).hexdigest() if os.path.isfile(q) else None
    objs = []
    for r, _ds, fs in os.walk(os.path.join(gd, 'objects')):
        objs += [os.path.relpath(os.path.join(r, f), gd) for f in fs]
    wt = os.path.join(gd, 'worktrees')
    return {'head': g(v, 'rev-parse', 'HEAD').strip(), 'refs': g(v, 'for-each-ref', '--format=%(refname) %(objectname)'),
            'index': fh('index'), 'config': fh('config'), 'reflog': fh(os.path.join('logs', 'HEAD')),
            'worktrees': sorted(os.listdir(wt)) if os.path.isdir(wt) else [], 'stash': g(v, 'stash', 'list'),
            'n_objects': len(objs), 'objects': hashlib.sha256('\n'.join(sorted(objs)).encode('utf-8')).hexdigest()}


def victim(tag):
    """새 피해 저장소 V (커밋 하나) → (경로, 상태)."""
    v = make_repo(f'victim_{tag}_{len(os.listdir(TD))}', {'v.txt': 'victim\n'})
    return v, repo_state(v)


def hostile_envs(v):
    """적대 환경 셋 (모두 V 만 가리킨다 · 자식 프로세스에만 넘긴다)."""
    gd = os.path.join(v, '.git')
    base = dict(CLEAN, TMPDIR=TD)
    return {'GIT_DIR': dict(base, GIT_DIR=gd),
            'GIT_DIR+GIT_WORK_TREE+GIT_INDEX_FILE': dict(base, GIT_DIR=gd, GIT_WORK_TREE=v, GIT_INDEX_FILE=os.path.join(gd, 'index')),
            'GIT_OBJECT_DIRECTORY+GIT_COMMON_DIR': dict(base, GIT_OBJECT_DIRECTORY=os.path.join(gd, 'objects'), GIT_COMMON_DIR=gd)}


def run_py(code, args, env, timeout=300):
    """자식 파이썬 (-c) → (rc, stdout, stderr)."""
    r = subprocess.run([sys.executable, '-c', code, *args], capture_output=True, text=True, env=env, timeout=timeout, cwd=TD,
                       stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout or '', r.stderr or ''


def tagged(out, tag):
    m = [ln for ln in out.splitlines() if ln.startswith(tag + ' ')]
    return m[-1][len(tag) + 1:] if m else None


def per_variant(tag, fn):
    """적대 꼴마다 새 V 로 fn(env, v) → (값, rc, stderr 끝) 을 돌려 V 상태를 견준다 → {꼴: (V 그대로, 값, rc, 사유)}."""
    out = {}
    for nm in ('GIT_DIR', 'GIT_DIR+GIT_WORK_TREE+GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY+GIT_COMMON_DIR'):
        v, s0 = victim(tag)
        val, rc, err = fn(hostile_envs(v)[nm], v)
        s1 = repo_state(v)
        diff = sorted(k for k in s0 if s0[k] != s1[k])
        out[nm] = (not diff, val, rc, (diff, err[-240:]))
    return out


# ═════════════════════════ G1 ═════════════════════════
@case('G1 run_contract.git_env · drop_git_env')
def g1():
    import run_contract as RC
    fn, dr = getattr(RC, 'git_env', None), getattr(RC, 'drop_git_env', None)
    if fn is None or dr is None:
        chk('G1 run_contract 에 git_env · drop_git_env 가 있다', False, '고치기 전 판 — 도우미 없음')
        return
    base = {'GIT_DIR': '/x', 'GIT_WORK_TREE': '/y', 'GIT_INDEX_FILE': '/z', 'GIT_OBJECT_DIRECTORY': '/o', 'GIT_ALTERNATE_OBJECT_DIRECTORIES': '/a',
            'GIT_COMMON_DIR': '/c', 'GIT_CONFIG_COUNT': '1', 'GIT_NAMESPACE': 'n', 'PATH': '/bin', 'HOME': '/h', 'XGIT_DIR': 'keep', 'git_dir': 'keep'}
    snap = dict(base)
    out = fn(base)
    keep = {'PATH': '/bin', 'HOME': '/h', 'XGIT_DIR': 'keep', 'git_dir': 'keep'}
    e2 = dict(base)
    removed = dr(e2)
    os_before = dict(os.environ)
    dflt = fn()
    chk('G1 git_env(사전) = GIT_ 로 시작하는 이름 전부 뺀 새 사전 (GIT_DIR · WORK_TREE · INDEX_FILE · OBJECT_DIRECTORY · ALTERNATE · COMMON_DIR · CONFIG_COUNT · '
        'NAMESPACE) · 그 밖 이름 그대로 (XGIT_DIR · 소문자 git_dir 포함) · 넘긴 사전 그대로 · drop_git_env(사전) = 제자리 지움 + 지운 이름 (정렬) · '
        'git_env() = os.environ 기준 · os.environ 그대로',
        out == keep and base == snap and out is not base and e2 == keep and removed == sorted(k for k in base if k.startswith('GIT_'))
        and dflt == {k: v for k, v in os.environ.items() if not k.startswith('GIT_')} and dict(os.environ) == os_before,
        (out, removed, e2))


# ═════════════════════════ G2 ═════════════════════════
def selftest_lines(env):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'run_contract.py'), '--selftest'], capture_output=True, text=True, env=env,
                       timeout=600, cwd=TD, stdin=subprocess.DEVNULL)
    lines = sorted(ln.strip() for ln in (r.stdout or '').splitlines() if ln.startswith('  PASS  ') or ln.startswith('  FAIL  '))
    return r.returncode, lines, (r.stdout or '') + (r.stderr or '')


@case('G2 run_contract --selftest (RCPT-sha 임시 저장소 쓰기 · 11-12 밤 사고)')
def g2():
    rc0, ref, log0 = selftest_lines(dict(CLEAN, TMPDIR=TD))
    rcpt = [ln for ln in ref if 'RCPT-sha' in ln]
    names = {ln.split()[1] for ln in rcpt}
    chk('G2 기준 — 깨끗한 환경의 selftest rc 0 · RCPT-sha 줄 (clean · untracked · shadow · modified 넷 포함) 전부 PASS (기준이 선다)',
        rc0 == 0 and {'RCPT-sha-clean', 'RCPT-sha-untracked', 'RCPT-sha-shadow', 'RCPT-sha-modified'} <= names
        and all(ln.startswith('PASS') for ln in rcpt), (rc0, rcpt, log0[-300:]))

    def run(env, _v):
        rc, lines, log = selftest_lines(env)
        return lines, rc, log
    res = per_variant('g2', run)
    bad = {nm: (same, rc, why[0], [ln for ln in (val or []) if ln.startswith('FAIL')][:4], why[1])
           for nm, (same, val, rc, why) in res.items() if not (same and rc == rc0 and val == ref)}
    chk('G2 적대 환경 셋 (GIT_DIR · +WORK_TREE+INDEX_FILE · OBJECT_DIRECTORY+COMMON_DIR → 일회용 V) 에서 run_contract --selftest — V 그대로 (HEAD · ref · index · '
        'config · reflog · worktrees · stash · 객체) · rc · PASS/FAIL 줄 = 깨끗한 환경과 같음 (고치기 전 = V 에 커밋 · RCPT-sha FAIL · 11-12 밤 사고 꼴)',
        not bad, bad)


# ═════════════════════════ G3 ═════════════════════════
G3_CODE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import mpm_webapp_payload as P
sd = sys.argv[2]
e = P._exec_env(sd)
print('G3 ' + json.dumps({'sha': P._code_sha(sd), 'untracked': e.get('untracked_codelike')}))
'''


@case('G3 payload _code_sha · _exec_env (생산 읽기)')
def g3():
    f = make_repo('g3_fixture', {'scripts/x.py': 'A = 1\n'})
    with open(os.path.join(f, 'scripts', 'u.py'), 'w', encoding='utf-8') as fh:
        fh.write('U = 1\n')                                         # scripts/ 안 untracked = dirty · untracked_codelike
    sd = os.path.join(f, 'scripts')
    want_sha = g(f, 'rev-parse', '--short', 'HEAD').strip()
    rc0, out0, err0 = run_py(G3_CODE, [SCRIPTS, sd], dict(CLEAN, TMPDIR=TD))
    ref = json.loads(tagged(out0, 'G3') or 'null')
    chk('G3 기준 — 깨끗한 환경 = F 의 HEAD + dirty (scripts/ 안 untracked) · untracked_codelike = u.py (scripts/ 기준 상대 경로 — `git -C scripts ls-files`)',
        rc0 == 0 and isinstance(ref, dict) and ref.get('sha') == want_sha + '+dirty' and ref.get('untracked') == ['u.py'], (rc0, ref, err0[-300:]))

    def run(env, _v):
        rc, out, err = run_py(G3_CODE, [SCRIPTS, sd], env)
        return json.loads(tagged(out, 'G3') or 'null'), rc, err
    res = per_variant('g3', run)
    bad = {nm: (same, rc, val, why) for nm, (same, val, rc, why) in res.items() if not (same and rc == 0 and val == ref)}
    chk('G3 적대 환경 셋에서 payload `_code_sha` · `_exec_env` 가 F 를 읽는다 (= 깨끗한 환경 값 · V 의 HEAD 가 아님) · V 그대로', not bad, bad)


# ═════════════════════════ G4 ═════════════════════════
G4_CODE = r'''
import hashlib, sys
sys.path.insert(0, sys.argv[1])
import test_step3_gpu_precond as T
m = T.load_base()
print('G4 ' + hashlib.sha256(open(m.__file__, 'rb').read()).hexdigest())
'''


@case('G4 test_step3_gpu_precond.load_base (기반 판 git show)')
def g4():
    want = hashlib.sha256(subprocess.run(['git', '-C', ROOT, 'show', f'{PRECOND_BASE}:scripts/step3_sigma.py'], capture_output=True, env=CLEAN,
                                         check=True).stdout).hexdigest()
    rc0, out0, err0 = run_py(G4_CODE, [SCRIPTS], dict(CLEAN, TMPDIR=TD))
    ref = tagged(out0, 'G4')
    chk('G4 기준 — 깨끗한 환경의 load_base = 기준 git show 바이트', rc0 == 0 and ref == want, (rc0, ref, want, err0[-300:]))

    def run(env, _v):
        rc, out, err = run_py(G4_CODE, [SCRIPTS], env)
        return tagged(out, 'G4'), rc, err
    res = per_variant('g4', run)
    bad = {nm: (same, rc, val, why) for nm, (same, val, rc, why) in res.items() if not (same and rc == 0 and val == want)}
    chk('G4 적대 환경 셋에서 load_base 가 이 리포의 기반 판을 읽는다 (= 기준 git show 바이트 · 고치기 전 = V 에서 찾다 실패) · V 그대로', not bad, bad)


# ═════════════════════════ G5 ═════════════════════════
G5_CODE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import rint_r_chain as RR
print('G5 ' + json.dumps({'id': RR.git_identity(sys.argv[2]), 'ledger': RR.ledger_repo_problem(sys.argv[3])}))
'''


@case('G5 사슬 git_identity · ledger_repo_problem (생산 읽기)')
def g5():
    f = make_repo('g5_fixture', {'scripts/x.py': 'A = 1\n'})
    led = make_repo('g5_ledger', {'l.txt': 'l\n'})
    xp = os.path.join(f, 'scripts', 'x.py')
    want_head = g(f, 'rev-parse', 'HEAD').strip()
    rc0, out0, err0 = run_py(G5_CODE, [SCRIPTS, xp, led], dict(CLEAN, TMPDIR=TD))
    ref = json.loads(tagged(out0, 'G5') or 'null')
    chk('G5 기준 — 깨끗한 환경 = F 의 HEAD · 깨끗 · 상대 경로 scripts/x.py · 원장 저장소 꼴 문제 없음',
        rc0 == 0 and isinstance(ref, dict) and ref['id'].get('head') == want_head and ref['id'].get('dirty') is False
        and ref['id'].get('rel') == 'scripts/x.py' and ref.get('ledger') is None, (rc0, ref, err0[-300:]))

    def run(env, _v):
        rc, out, err = run_py(G5_CODE, [SCRIPTS, xp, led], env)
        return json.loads(tagged(out, 'G5') or 'null'), rc, err
    res = per_variant('g5', run)
    bad = {nm: (same, rc, val, why) for nm, (same, val, rc, why) in res.items() if not (same and rc == 0 and val == ref)}
    chk('G5 적대 환경 셋에서 사슬 git_identity (HEAD · dirty · rel) · ledger_repo_problem = 깨끗한 환경 값 (V 를 읽지 않는다) · V 그대로', not bad, bad)


# ═════════════════════════ G6 ═════════════════════════
G6_CODE = r'''
import json, os, subprocess, sys
which, scripts, tools6, fx = sys.argv[1:5]
sys.path.insert(0, scripts)
CFG = ['-c', 'user.email=t@t', '-c', 'user.name=t', '-c', 'commit.gpgsign=false', '-c', 'init.defaultBranch=main']
if which == 'test_rint_r_chain':
    import test_rint_r_chain as T

    def git(*a):
        T.git_(fx, *a)
elif which == 'test_probe6_read':
    sys.path.insert(0, tools6)
    import test_probe6_read as T

    def git(*a):
        T.git(fx, *a)
else:
    if which == 'test_cjunc_store_e2e':
        import test_cjunc_store_e2e as T                  # noqa: F401
    else:
        import test_cjunc_store as T                      # noqa: F401

    def git(*a):                                          # 그 모듈의 꼴 (env 없이 · 이 프로세스 환경을 물려받는다 — e2e flow() 의 git init 꼴)
        if a[0] == 'init':
            subprocess.run(['git', 'init', '-q', fx], check=True, capture_output=True)
        else:
            subprocess.run(['git', '-C', fx, *CFG, *a], check=True, capture_output=True)
os.makedirs(fx, exist_ok=True)
left = sorted(k for k in os.environ if k.startswith('GIT_'))
git('init', '-q')
with open(os.path.join(fx, 'a.txt'), 'w') as f:
    f.write('a')
git('add', '-A')
git('commit', '-qm', 'x')
print('G6 ' + json.dumps({'left_git_env': left}))
'''


@case('G6 이 묶음이 고친 시험 모듈 넷 — 불러오면 GIT_* 를 지운다 (고정물 git 쓰기)')
def g6():
    bad = {}
    for which in ('test_rint_r_chain', 'test_probe6_read', 'test_cjunc_store_e2e', 'test_cjunc_store'):
        k = [0]

        def run(env, _v, which=which):
            k[0] += 1
            fx = os.path.join(TD, f'g6_{which}_{k[0]}')
            rc, out, err = run_py(G6_CODE, [which, SCRIPTS, TOOLS6, fx], env)
            n = None
            if os.path.isdir(os.path.join(fx, '.git')):
                n = g(fx, 'rev-list', '--count', 'HEAD', check=False).strip()
            return (json.loads(tagged(out, 'G6') or 'null'), n), rc, err
        for nm, (same, val, rc, why) in per_variant('g6_' + which, run).items():
            got, n = val
            if not (same and rc == 0 and isinstance(got, dict) and got.get('left_git_env') == [] and n == '1'):
                bad[f'{which} · {nm}'] = (same, rc, got, n, why)
    chk('G6 이 묶음이 고친 시험 모듈 넷 (test_rint_r_chain · test_probe6_read · test_cjunc_store_e2e · test_cjunc_store) 을 적대 환경 셋에서 불러 고정물 저장소를 '
        '만든다 (init · add · commit) → V 그대로 · 고정물에 커밋 하나 · 불러온 뒤 GIT_* 없음 (고치기 전 = V 에 커밋)', not bad, bad)


def main():
    global ARGS, TD
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--only', default='', help='쉼표로 이름 접두 (예: G2,G6)')
    ap.add_argument('--keep', action='store_true', help='임시 폴더를 남긴다')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='git_env_t_')
    t0 = time.time()
    sel = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    try:
        for tag, fn in CASES:
            if sel and not any(tag.startswith(s) for s in sel):
                continue
            print(f'\n── {tag}')
            try:
                fn()
            except Exception as e:                                 # noqa: BLE001 — 시험 안의 예외 = 그 묶음 실패
                import traceback
                chk(f'{tag.split()[0]} 예외 없이', False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:300]}')
    finally:
        if ARGS.keep:
            print(f'  (임시 폴더 남김: {TD})')
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\ntest_git_env_isolation: {_ok} PASS · {len(_fail)} FAIL ({time.time() - t0:.1f} s)')
    for n in _fail:
        print(f'  - {n}')
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
