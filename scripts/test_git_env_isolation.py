#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""11-12 2 회차 (Rint ② 코드 묶음 · 내부 반박 리뷰 재확인 RCP2-06 · Codex 아님) — git 을 부르는 selftest · 시험 고정물 · 생산 읽기가 부르는 쪽 환경의
`GIT_*` (GIT_DIR · GIT_WORK_TREE · GIT_INDEX_FILE · GIT_OBJECT_DIRECTORY · GIT_ALTERNATE_OBJECT_DIRECTORIES · GIT_COMMON_DIR …) 를 물려받지 않는가.

11-12 밤 실제 사고: 리뷰 조수가 `GIT_DIR=<본 리포>/.git` 을 명령 앞에 붙여 `run_contract.py --selftest` 를 돌렸고, 그 selftest (RCPT-sha) 의 임시 폴더
`git init · add -A · commit` 이 임시 폴더 대신 본 리포 가지에 커밋을 만들었다 (본 세션이 되돌림).  git 훅 (pre-commit · pre-push) 안에서 게이트를 돌려도
git 이 이 변수들을 넣는다 (정직한 흐름).  ⇒ 이 시험은 **이 시험이 만든 일회용 임시 저장소** (피해 저장소 V) 만 가리키는 적대 환경을 **자식 프로세스에만**
넘긴다 — 이 프로세스의 환경은 바꾸지 않는다 · 본 리포 · 작업 트리 저장소를 가리키지 않는다.  적대 꼴 넷: GIT_DIR (사고 꼴) · GIT_DIR + GIT_WORK_TREE +
GIT_INDEX_FILE · GIT_OBJECT_DIRECTORY + GIT_COMMON_DIR · ★ 3 회차 (재확인 2 RCP3-01) 훅 꼴 = GIT_INDEX_FILE 하나 (`<V>/.git/index.lock` 절대 경로 — git 2.43
pre-commit 훅 env 실측 · V 에 commit 도중 꼴의 index.lock 사본을 둔다).  V 상태 = HEAD · ref 전부 · index · index.lock · config · HEAD reflog · worktrees ·
stash · 객체 목록.

  G1  run_contract.git_env · drop_git_env — ★ 3 회차 (재확인 2 RCP3-04 · 본 세션 결정) 지우는 이름 = 저장소 위치 · 색인 · 객체 (GIT_DIR · GIT_WORK_TREE ·
      GIT_INDEX_FILE · GIT_OBJECT_DIRECTORY · GIT_ALTERNATE_OBJECT_DIRECTORIES · GIT_COMMON_DIR · GIT_NAMESPACE · GIT_PREFIX) + 설정 주입 (GIT_CONFIG_PARAMETERS ·
      GIT_CONFIG_COUNT · GIT_CONFIG_KEY_<n> · GIT_CONFIG_VALUE_<n>) 뿐 — 격리 변수 (GIT_CEILING_DIRECTORIES · GIT_CONFIG_NOSYSTEM · GIT_CONFIG_GLOBAL) 와
      그 밖 GIT_ 이름 (신원 · 편집기 · 실행 자리 · 인증서 · 추적 …) 은 남긴다 (옛 2 회차 판 = GIT_ 전부) · 넘긴 사전 그대로 · 제자리 지움 (지운 이름 돌려줌)
  G2  `run_contract.py --selftest` (RCPT-sha 의 임시 저장소 init · add · commit + payload `_code_sha` 읽기) — 적대 셋에서 V 그대로 · rc · PASS/FAIL 줄 =
      깨끗한 환경과 같음 (고치기 전 = V 에 커밋 · RCPT-sha 둘 FAIL — 11-12 밤 사고 그대로)
  G3  payload `_code_sha` · `_exec_env` (생산 읽기 · 고정물 저장소 F) — 적대 = 깨끗 (V 의 HEAD 를 읽지 않는다) · V 그대로
  G4  `test_step3_gpu_precond.load_base` (기반 판 git show · 시험 모듈 불러오기 = 그 모듈의 GIT_* 지움) — 적대 = 깨끗 = 기준 git show 바이트 · V 그대로
  G5  사슬 `rint_r_chain.git_identity` · `ledger_repo_problem` · `plan_commit_problem` (F5 계획 출처 커밋 = 이 리포의 기반 판 커밋 · blob 맞음 /
      틀림) (생산 읽기) — 적대 = 깨끗 · V 그대로 (★ 11-12 2 회차 변이 보강 — F5 의 git 둘에 env 를 안 넘긴 변이가 G1–G6 에서 안 잡혔다)
  G6  시험 모듈 여덟 — 이 묶음이 고친 넷 (test_rint_r_chain `git_` · test_probe6_read `git` · test_cjunc_store_e2e · test_cjunc_store) + 같은 부류 셋
      (★ 본 세션 결정 11-12 밤: test_rint_r_chain_e2e `_git` · test_rint_r_chain_e2e12 `git` · test_step3_conv_cert) + ★ 3 회차 (재확인 2 RCP3-01)
      test_ca_s0_census `_git` (S0 계획 고정물 저장소 · 게이트 · kgy 묶음) — 적대 환경에서 그 모듈을 불러 고정물 저장소를 만들면 (init · add · commit)
      V 그대로 · 고정물 저장소에 커밋 하나 · 불러온 뒤 그 프로세스 환경에 GIT_* 없음
  G7  ★ 3 회차 (재확인 2 RCP3-04) — 부르는 쪽 격리가 산다 · 시험 고정물은 스스로 끊는다: (a) 천장 (GIT_CEILING_DIRECTORIES) 안 git 아닌 사본 = payload
      `_code_sha` None (옛 판처럼 · 2 회차 판 = 바깥 저장소 HEAD) (b) 부르는 쪽 GIT_CONFIG_GLOBAL=/dev/null + HOME 전역 core.hooksPath → run_contract
      --selftest 훅 0 회 (옛 판처럼 · 2 회차 판 = 1 회씩) (c) 부르는 쪽 격리 없이 전역 설정 셋 (HOME core.hooksPath · XDG_CONFIG_HOME core.hooksPath ·
      HOME init.templateDir) → selftest 임시 저장소 · 시험 모듈 고정물 도우미 다섯 (git_ · _git · e2e12 git · probe6 git · s0 census _git) 의 commit 에서
      훅 0 회 (고정물 git = GIT_CONFIG_NOSYSTEM=1 · GIT_CONFIG_GLOBAL=/dev/null · HOME 임시) · ★ 3 회차 변이 보강: (d) `git_fixture_env(넘긴 env)` 꼴
      (XDG_CONFIG_HOME · 넘긴 HOME 을 뺀다 · 지울 이름 뺌 · 천장 · PATH 남김) (e) 시험 모듈 여덟의 git 부르는 자리 (정적 · subprocess · 첫 낱말 git) 가
      모두 env 를 넘긴다 (예외 = 이 리포를 읽기만 하는 자리 셋 · 도우미 다섯 밖의 고정물 init · pull · clone · git_rc 를 본다)
  G8  ★ 3 회차 (재확인 2 RCP3-05) — 게이트 수준: (a) `check_all.sh` · `check_kgy_py38.sh` 머리 · 러너 기각 영수증 code_sha 줄 · S0 블록 heredoc 머리가
      같은 셸 꼴 (`run_contract.GIT_DROP_SH` 글자 그대로 · 자리 = 첫 단계 · 첫 git 앞) · 그 셸 꼴을 bash 로 돌린 뒤 남는 GIT_ 이름 = 파이썬 규칙 (b)
      `check_review_findings.py --selftest` (매달린 커밋 commit-tree = 쓰기) — 적대 환경 넷에서 V 그대로 · 그 커밋은 자기 저장소 (일회용 사본 F) 에
      (c) `ca_s0_census._code_info` (S0 보고 git_head · git_dirty) — 적대 = 깨끗 · V 그대로
  G7f–h ★ 11-13 Codex 반박 1/2 RCPX-02 · §3 — 고정물 git 의 남은 주입 셋: (f) 부르는 쪽 GIT_TEMPLATE_DIR (훅 든 틀) → selftest · 도우미 다섯 훅 0 회 ·
      고정물 GIT_TEMPLATE_DIR = 빈 전용 틀 (g) 고정물 저장소 .git/hooks 에 훅을 넣어도 안 돈다 (core.hooksPath = 빈 전용 폴더 · 부르는 쪽
      GIT_CONFIG_PARAMETERS 는 이 값으로 바뀐다) (h) 부르는 쪽 GIT_QUARANTINE_PATH (pre-receive 꼴) → 도우미 commit rc 0
  G9  ★ 11-13 Codex 반박 1/2 §3 — 봉인용 git 객체 · 이력: (a) 바꿔치기 객체 (refs/replace · GIT_REPLACE_REF_BASE) 가 있어도 계획 출처 대조 · dirty ·
      code_sha · S0 git show 가 원래 객체를 읽는다 (GIT_NO_REPLACE_OBJECTS=1) (b) 깨끗한 기준 (c) graft · shallow (GIT_GRAFT_FILE · 없는 파일 포함 ·
      GIT_SHALLOW_FILE · info/grafts · shallow 저장소) = 계획 출처 · 원장 조상 대조 · S0 단계 2 관문이 사유와 함께 닫는다 ('unshallow 하라')
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
            'index': fh('index'), 'index_lock': fh('index.lock'), 'config': fh('config'), 'reflog': fh(os.path.join('logs', 'HEAD')),
            'worktrees': sorted(os.listdir(wt)) if os.path.isdir(wt) else [], 'stash': g(v, 'stash', 'list'),
            'n_objects': len(objs), 'objects': hashlib.sha256('\n'.join(sorted(objs)).encode('utf-8')).hexdigest()}


def victim(tag):
    """새 피해 저장소 V (커밋 하나) → (경로, 상태)."""
    v = make_repo(f'victim_{tag}_{len(os.listdir(TD))}', {'v.txt': 'victim\n'})
    return v, repo_state(v)


#: ★ 3 회차 (재확인 2 RCP3-01) — 정직한 훅 꼴 (git 2.43 pre-commit 훅 env 실측: GIT_INDEX_FILE=<저장소>/.git/index.lock 절대 경로 하나 · GIT_DIR 없음)
HOOK_FORM = 'GIT_INDEX_FILE(훅 꼴 · index.lock)'
VARIANTS = ('GIT_DIR', 'GIT_DIR+GIT_WORK_TREE+GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY+GIT_COMMON_DIR', HOOK_FORM)


def hostile_envs(v):
    """적대 환경 넷 (모두 V 만 가리킨다 · 자식 프로세스에만 넘긴다)."""
    gd = os.path.join(v, '.git')
    base = dict(CLEAN, TMPDIR=TD)
    return {'GIT_DIR': dict(base, GIT_DIR=gd),
            'GIT_DIR+GIT_WORK_TREE+GIT_INDEX_FILE': dict(base, GIT_DIR=gd, GIT_WORK_TREE=v, GIT_INDEX_FILE=os.path.join(gd, 'index')),
            'GIT_OBJECT_DIRECTORY+GIT_COMMON_DIR': dict(base, GIT_OBJECT_DIRECTORY=os.path.join(gd, 'objects'), GIT_COMMON_DIR=gd),
            HOOK_FORM: dict(base, GIT_INDEX_FILE=os.path.join(gd, 'index.lock'))}


def run_py(code, args, env, timeout=300):
    """자식 파이썬 (-c) → (rc, stdout, stderr)."""
    r = subprocess.run([sys.executable, '-c', code, *args], capture_output=True, text=True, env=env, timeout=timeout, cwd=TD,
                       stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout or '', r.stderr or ''


def tagged(out, tag):
    m = [ln for ln in out.splitlines() if ln.startswith(tag + ' ')]
    return m[-1][len(tag) + 1:] if m else None


def per_variant(tag, fn):
    """적대 꼴마다 새 V 로 fn(env, v) → (값, rc, stderr 끝) 을 돌려 V 상태를 견준다 → {꼴: (V 그대로, 값, rc, 사유)}.
    훅 꼴 = V 의 index 를 index.lock 으로 복사해 둔다 (commit 도중 꼴 — 그 커밋의 색인) · 그 파일도 V 상태에 든다."""
    out = {}
    for nm in VARIANTS:
        v, _s = victim(tag)
        if nm == HOOK_FORM:
            shutil.copyfile(os.path.join(v, '.git', 'index'), os.path.join(v, '.git', 'index.lock'))
        s0 = repo_state(v)
        val, rc, err = fn(hostile_envs(v)[nm], v)
        s1 = repo_state(v)
        diff = sorted(k for k in s0 if s0[k] != s1[k])
        out[nm] = (not diff, val, rc, (diff, err[-240:]))
    return out


# ═════════════════════════ G1 ═════════════════════════
#: ★ 3 회차 (재확인 2 RCP3-04 · 본 세션 결정 11-12 밤) — 지울 이름 (시험 쪽 기준 · 대상 모듈의 상수를 쓰지 않는다)
DROP_EXPECT = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_COMMON_DIR', 'GIT_NAMESPACE',
               'GIT_PREFIX', 'GIT_CONFIG_PARAMETERS', 'GIT_CONFIG_COUNT')
DROP_EXPECT_PREFIX = ('GIT_CONFIG_KEY_', 'GIT_CONFIG_VALUE_')


#: ★ 11-13 (Codex 반박 1/2 §3) — git_env 가 늘 넣는 값 (대체 객체 끔 · 시험 쪽 기준 글자)
SET_EXPECT = {'GIT_NO_REPLACE_OBJECTS': '1'}


def dropped(k):
    return k in DROP_EXPECT or k.startswith(DROP_EXPECT_PREFIX)


@case('G1 run_contract.git_env · drop_git_env (지우는 이름 = 저장소 위치 · 색인 · 객체 + 설정 주입 — 3 회차 RCP3-04)')
def g1():
    import run_contract as RC
    fn, dr = getattr(RC, 'git_env', None), getattr(RC, 'drop_git_env', None)
    if fn is None or dr is None:
        chk('G1 run_contract 에 git_env · drop_git_env 가 있다', False, '고치기 전 판 — 도우미 없음')
        return
    gone = {k: '/x' for k in DROP_EXPECT}
    gone.update({'GIT_CONFIG_KEY_0': 'core.hooksPath', 'GIT_CONFIG_VALUE_0': '/h', 'GIT_CONFIG_KEY_12': 'a.b', 'GIT_CONFIG_VALUE_12': 'c'})
    keep_git = {'GIT_CEILING_DIRECTORIES': '/o', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_SYSTEM': '/s',
                'GIT_DISCOVERY_ACROSS_FILESYSTEM': '1', 'GIT_AUTHOR_NAME': 'a', 'GIT_COMMITTER_EMAIL': 'c@c', 'GIT_EDITOR': ':',
                'GIT_EXEC_PATH': '/usr/lib/git-core', 'GIT_SSL_CAINFO': '/ca', 'GIT_TERMINAL_PROMPT': '0', 'GIT_ASKPASS': '/a', 'GIT_TRACE': '0'}
    keep = dict(keep_git, PATH='/bin', HOME='/h', XGIT_DIR='keep', git_dir='keep')
    base = dict(keep, **gone)
    snap = dict(base)
    out = fn(base)
    e2 = dict(base)
    removed = dr(e2)
    os_before = dict(os.environ)
    dflt = fn()
    chk('G1 git_env(사전) = 저장소 위치 · 색인 · 객체 여덟 + 설정 주입 (CONFIG_PARAMETERS · CONFIG_COUNT · CONFIG_KEY_<n> · CONFIG_VALUE_<n>) 만 뺀 새 사전 · '
        '격리 변수 (CEILING · NOSYSTEM · GLOBAL) · 그 밖 GIT_ (CONFIG_SYSTEM · DISCOVERY · 신원 · 편집기 · 실행 자리 · 인증서 · 프롬프트 · 추적) · GIT_ 아닌 '
        '이름 그대로 · 넘긴 사전 그대로 · drop_git_env(사전) = 제자리 지움 + 지운 이름 (정렬) · git_env() = os.environ 기준 · os.environ 그대로 · ★ 11-13 '
        'git_env 는 GIT_NO_REPLACE_OBJECTS=1 을 늘 넣는다 (부르는 쪽 값 0 도 1 로 · 대체 객체 끔 §3 · drop_git_env 는 넣지 않는다)',
        out == dict(keep, **SET_EXPECT) and base == snap and out is not base and e2 == keep and removed == sorted(gone)
        and dflt == dict({k: v for k, v in os.environ.items() if not dropped(k)}, **SET_EXPECT) and dict(os.environ) == os_before
        and fn(dict(base, GIT_NO_REPLACE_OBJECTS='0')).get('GIT_NO_REPLACE_OBJECTS') == '1',
        (sorted(set(keep) ^ set(out or {})), removed))


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
    chk('G2 적대 환경 넷 (GIT_DIR · +WORK_TREE+INDEX_FILE · OBJECT_DIRECTORY+COMMON_DIR · 훅 꼴 GIT_INDEX_FILE 하나 → 일회용 V) 에서 run_contract --selftest — V 그대로 (HEAD · ref · index · '
        'config · reflog · worktrees · stash · 객체 · index.lock) · rc · PASS/FAIL 줄 = 깨끗한 환경과 같음 (고치기 전 = V 에 커밋 · RCPT-sha FAIL · 11-12 밤 사고 꼴)',
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
    chk('G3 적대 환경 넷 (훅 꼴 포함) 에서 payload `_code_sha` · `_exec_env` 가 F 를 읽는다 (= 깨끗한 환경 값 · V 의 HEAD 가 아님) · V 그대로', not bad, bad)


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
    chk('G4 적대 환경 넷 (훅 꼴 포함) 에서 load_base 가 이 리포의 기반 판을 읽는다 (= 기준 git show 바이트 · 고치기 전 = V 에서 찾다 실패) · V 그대로', not bad, bad)


# ═════════════════════════ G5 ═════════════════════════
G5_CODE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import rint_r_chain as RR
base, blob = sys.argv[4], sys.argv[5]
print('G5 ' + json.dumps({'id': RR.git_identity(sys.argv[2]), 'ledger': RR.ledger_repo_problem(sys.argv[3]),
                          'plan': RR.plan_commit_problem('commit:' + base, 'scripts/step3_sigma.py', blob),
                          'plan_wrong_blob': RR.plan_commit_problem('commit:' + base, 'scripts/step3_sigma.py', '0' * 64)}))
'''


@case('G5 사슬 git_identity · ledger_repo_problem · plan_commit_problem (생산 읽기)')
def g5():
    f = make_repo('g5_fixture', {'scripts/x.py': 'A = 1\n'})
    led = make_repo('g5_ledger', {'l.txt': 'l\n'})
    xp = os.path.join(f, 'scripts', 'x.py')
    want_head = g(f, 'rev-parse', 'HEAD').strip()
    #  F5 (계획 출처 커밋) — 사슬은 자기 저장소 (scripts 의 git) 에서 커밋 · blob 을 찾는다 → 이 리포의 기반 판 커밋 (G4 와 같은 앞 조건) · 그 판
    #  scripts/step3_sigma.py 의 blob sha256 = 맞는 계획 · 0 × 64 = 틀린 계획 (판별 — 맞음 = None · 틀림 = 사유 글)
    base = g(ROOT, 'rev-parse', '--verify', f'{PRECOND_BASE}^{{commit}}').strip()
    blob = hashlib.sha256(subprocess.run(['git', '-C', ROOT, 'show', f'{base}:scripts/step3_sigma.py'], capture_output=True, env=CLEAN,
                                         check=True).stdout).hexdigest()
    argv = [SCRIPTS, xp, led, base, blob]
    rc0, out0, err0 = run_py(G5_CODE, argv, dict(CLEAN, TMPDIR=TD))
    ref = json.loads(tagged(out0, 'G5') or 'null')
    chk('G5 기준 — 깨끗한 환경 = F 의 HEAD · 깨끗 · 상대 경로 scripts/x.py · 원장 저장소 꼴 문제 없음 · 계획 출처 커밋 (이 리포의 기반 판 · '
        'blob 맞음) 문제 없음 · blob 틀림 = 사유 (판별)',
        rc0 == 0 and isinstance(ref, dict) and ref['id'].get('head') == want_head and ref['id'].get('dirty') is False
        and ref['id'].get('rel') == 'scripts/x.py' and ref.get('ledger') is None and ref.get('plan') is None
        and isinstance(ref.get('plan_wrong_blob'), str) and 'blob sha256' in ref['plan_wrong_blob'], (rc0, ref, err0[-300:]))

    def run(env, _v):
        rc, out, err = run_py(G5_CODE, argv, env)
        return json.loads(tagged(out, 'G5') or 'null'), rc, err
    res = per_variant('g5', run)
    bad = {nm: (same, rc, val, why) for nm, (same, val, rc, why) in res.items() if not (same and rc == 0 and val == ref)}
    chk('G5 적대 환경 넷 (훅 꼴 포함) 에서 사슬 git_identity (HEAD · dirty · rel) · ledger_repo_problem · plan_commit_problem (F5 · 맞음 / 틀림) = 깨끗한 '
        '환경 값 (V 를 읽지 않는다) · V 그대로', not bad, bad)


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
elif which == 'test_ca_s0_census':                      # ★ 3 회차 (재확인 2 RCP3-01) — S0 계획 고정물 저장소의 도우미 (make_plan_repo 가 쓰는 _git)
    import test_ca_s0_census as T

    def git(*a):
        T._git(fx, *a)
elif which in ('test_rint_r_chain_e2e', 'test_rint_r_chain_e2e12'):
    import importlib
    T = importlib.import_module(which)

    def git(*a):                                          # 그 모듈의 꼴 (_git · e2e12 git = E._git · env 기본 None = 이 프로세스 환경)
        (T._git if which == 'test_rint_r_chain_e2e' else T.git)(fx, *a)
else:
    if which == 'test_cjunc_store_e2e':
        import test_cjunc_store_e2e as T                  # noqa: F401
    elif which == 'test_step3_conv_cert':
        import test_step3_conv_cert as T                  # noqa: F401 — 그 모듈의 git = 읽기 (기반 판 git show · env 없이)
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


@case('G6 시험 모듈 여덟 (이 묶음이 고친 넷 + 같은 부류 셋 + test_ca_s0_census) — 불러오면 GIT_* 를 지운다 (고정물 git 쓰기)')
def g6():
    bad = {}
    for which in G6_MODULES:                                       # 같은 부류 셋 (본 세션 결정 11-12 밤) · ★ 3 회차 (재확인 2 RCP3-01) test_ca_s0_census
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
    chk('G6 시험 모듈 여덟 (test_rint_r_chain · test_probe6_read · test_cjunc_store_e2e · test_cjunc_store + 같은 부류 test_rint_r_chain_e2e · '
        'test_rint_r_chain_e2e12 · test_step3_conv_cert + test_ca_s0_census) 을 적대 환경 넷 (훅 꼴 포함) 에서 불러 고정물 저장소를 만든다 (init · add · '
        'commit) → V 그대로 (index.lock 포함) · 고정물에 커밋 하나 · 불러온 뒤 GIT_* 없음 (고치기 전 = V 에 커밋 · 훅 꼴 = V 의 index.lock 이 고정물 항목으로)',
        not bad, {k: (v[0], v[1], v[2], v[3], v[4][0]) for k, v in bad.items()})


# ═════════════════════════ G7 (★ 3 회차 · 재확인 2 RCP3-04) ═════════════════════════
G7A_CODE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import mpm_webapp_payload as P
print('G7A ' + json.dumps({'sha': P._code_sha(sys.argv[2])}))
'''
#: 시험 모듈 고정물 도우미 다섯 (모듈 · 도우미 이름) — 그 도우미로 고정물 저장소를 만든다 (init · add · commit)
G7_HELPERS = (('test_rint_r_chain', 'git_'), ('test_rint_r_chain_e2e', '_git'), ('test_rint_r_chain_e2e12', 'git'),
              ('test_probe6_read', 'git'), ('test_ca_s0_census', '_git'))
#: G6 의 시험 모듈 여덟 (★ 3 회차 변이 보강 — G6 · G7e 가 같이 쓴다) · 이 리포를 읽기만 하는 git 자리 (모듈 · 하위 명령) · 모듈마다 git 자리 수 하한
#  (훑기가 빈손이 아님)
G6_MODULES = ('test_rint_r_chain', 'test_probe6_read', 'test_cjunc_store_e2e', 'test_cjunc_store', 'test_rint_r_chain_e2e', 'test_rint_r_chain_e2e12',
              'test_step3_conv_cert', 'test_ca_s0_census')
G7E_READ_ROOT = {('test_rint_r_chain', 'check-ignore'), ('test_ca_s0_census', 'show'), ('test_step3_conv_cert', 'show')}
G7E_MIN_SITES = {m: 1 for m in G6_MODULES if m != 'test_cjunc_store'}        # test_cjunc_store = git 을 직접 부르지 않는다 (불러올 때 지움만)
G7E_RUN = ('run', 'check_output', 'check_call', 'call', 'Popen')


def g7e_git_sites(path):
    """파일 하나의 git 부르는 자리 → [(줄 · env 넘김 · 문자열 낱말 · ROOT 를 가리킴)] — subprocess 꼴 함수 (G7E_RUN) 의 첫 인자가 'git' 으로 시작하는
    목록 · 튜플 (또는 그것 + …).  env 넘김 = env= 낱말 또는 `**kw` + 감싼 함수 안 `….setdefault('env', …)`."""
    import ast
    tree = ast.parse(open(path, encoding='utf-8').read())

    def argv(call):
        a = call.args[0] if call.args else None
        while isinstance(a, ast.BinOp) and isinstance(a.op, ast.Add):
            a = a.left
        if isinstance(a, (ast.List, ast.Tuple)) and a.elts and isinstance(a.elts[0], ast.Constant) and a.elts[0].value == 'git':
            return a.elts
        return None

    def fname(f):
        return f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)

    def sets_env(fn):
        return fn is not None and any(isinstance(n, ast.Call) and fname(n.func) == 'setdefault' and n.args and isinstance(n.args[0], ast.Constant)
                                      and n.args[0].value == 'env' for n in ast.walk(fn))

    def is_root(e):
        return (isinstance(e, ast.Name) and e.id == 'ROOT') or (isinstance(e, ast.Call) and any(isinstance(x, ast.Name) and x.id == 'ROOT' for x in e.args))

    out = []

    def walk(node, fn):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Call) and fname(ch.func) in G7E_RUN:
                el = argv(ch)
                if el is not None:
                    kws = [k.arg for k in ch.keywords]
                    has_env = 'env' in kws or (None in kws and sets_env(fn))
                    consts = [e.value for e in el if isinstance(e, ast.Constant) and isinstance(e.value, str)]
                    out.append((ch.lineno, has_env, consts, any(is_root(e) for e in el)))
            walk(ch, ch if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) else fn)
    walk(tree, None)
    return out


G7C_CODE = r'''
import importlib, os, sys
which, attr, scripts, tools6, fx = sys.argv[1:6]
sys.path.insert(0, scripts)
if which == 'test_probe6_read':
    sys.path.insert(0, tools6)
T = importlib.import_module(which)
git = getattr(T, attr)
os.makedirs(fx, exist_ok=True)
git(fx, 'init', '-q')
with open(os.path.join(fx, 'a.txt'), 'w') as f:
    f.write('a')
git(fx, 'add', '-A')
git(fx, 'commit', '-qm', 'x')
print('G7C ok')
'''


def hook_kit():
    """가짜 전역 설정 셋 + 훅 (pre-commit · post-commit · post-checkout · post-merge = 표지 파일에 한 줄) → ({꼴: env 덧칸}, 표지 폴더, hooksPath 를 둔
    HOME).  꼴 = HOME/.gitconfig core.hooksPath · XDG_CONFIG_HOME/git/config core.hooksPath (HOME = 빈 폴더) · HOME/.gitconfig init.templateDir."""
    root = os.path.join(TD, 'g7_kit')
    marks, hooks, tpl = (os.path.join(root, x) for x in ('marks', 'hooks', os.path.join('tpl', 'hooks')))
    for d in (marks, hooks, tpl):
        os.makedirs(d)
    for d in (hooks, tpl):
        for hk in ('pre-commit', 'post-commit', 'post-checkout', 'post-merge'):
            q = os.path.join(d, hk)
            with open(q, 'w', encoding='utf-8') as f:
                f.write('#!/bin/sh\necho x >> "%s/%s"\nexit 0\n' % (marks, hk))
            os.chmod(q, 0o755)
    homes = {}
    for nm, rel, text in (('home_hooks', '.gitconfig', '[core]\n\thooksPath = %s\n' % hooks),
                          ('xdg', os.path.join('git', 'config'), '[core]\n\thooksPath = %s\n' % hooks),
                          ('home_tpl', '.gitconfig', '[init]\n\ttemplateDir = %s\n' % os.path.dirname(tpl)),
                          ('home_empty', None, None)):
        d = os.path.join(root, nm)
        os.makedirs(d)
        if rel:
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            with open(os.path.join(d, rel), 'w', encoding='utf-8') as f:
                f.write(text)
        homes[nm] = d
    kinds = {'HOME core.hooksPath': {'HOME': homes['home_hooks']},
             'XDG_CONFIG_HOME core.hooksPath': {'HOME': homes['home_empty'], 'XDG_CONFIG_HOME': homes['xdg']},
             'HOME init.templateDir': {'HOME': homes['home_tpl']}}
    return kinds, marks, homes['home_hooks']


def marks_count(marks):
    """표지 폴더의 훅 실행 수 (훅 이름 → 줄 수) 를 세고 비운다."""
    n = {}
    for m in sorted(os.listdir(marks)):
        with open(os.path.join(marks, m), encoding='utf-8') as f:
            n[m] = len(f.read().splitlines())
        os.unlink(os.path.join(marks, m))
    return n


@case('G7 부르는 쪽 격리가 산다 · 시험 고정물은 스스로 끊는다 (3 회차 RCP3-04)')
def g7():
    import run_contract as RC
    #  (a) 천장 — 바깥 저장소 O 안의 git 아닌 사본 (O/kit/scripts · 추적 안 됨)
    o = make_repo('g7_outer', {'README': 'outer\n'})
    kit = os.path.join(o, 'kit', 'scripts')
    os.makedirs(kit)
    with open(os.path.join(kit, 'm.py'), 'w', encoding='utf-8') as f:
        f.write('A = 1\n')
    o_short = g(o, 'rev-parse', '--short', 'HEAD').strip()
    got = {}
    for lab, extra in (('천장 없음', {}), ('천장 = 바깥 저장소', {'GIT_CEILING_DIRECTORIES': o})):
        rc, out, err = run_py(G7A_CODE, [SCRIPTS, kit], dict(CLEAN, TMPDIR=TD, **extra))
        got[lab] = (rc, json.loads(tagged(out, 'G7A') or 'null'), err[-200:])
    chk('G7a 부르는 쪽 천장 (GIT_CEILING_DIRECTORIES = 바깥 저장소) 안의 git 아닌 사본 → payload `_code_sha` = None (출처 없음 · 옛 판처럼) · 천장 없음 = 바깥 '
        '저장소 HEAD +dirty (대조 — 천장이 판별한다 · 2 회차 판 = 천장을 지워 늘 바깥 HEAD · 재확인 2 ce06 C)',
        got['천장 없음'][0] == 0 and (got['천장 없음'][1] or {}).get('sha') == o_short + '+dirty'
        and got['천장 = 바깥 저장소'][0] == 0 and isinstance(got['천장 = 바깥 저장소'][1], dict) and got['천장 = 바깥 저장소'][1].get('sha', 'x') is None, got)
    kinds, marks, home_hooks = hook_kit()
    #  (b) 부르는 쪽이 GIT_CONFIG_GLOBAL=/dev/null 로 전역 설정을 끈 채 (HOME 에 전역 core.hooksPath) → selftest 의 임시 commit 에서 훅 0
    rc, lines, log = selftest_lines(dict(CLEAN, TMPDIR=TD, HOME=home_hooks, GIT_CONFIG_GLOBAL=os.devnull))
    nb = marks_count(marks)
    chk('G7b 부르는 쪽 GIT_CONFIG_GLOBAL=/dev/null (+ HOME 전역 core.hooksPath) 에서 run_contract --selftest → rc 0 · 전역 훅 0 회 (부르는 쪽 격리가 산다 · '
        '옛 판처럼 — 2 회차 판 = 그 변수를 지워 pre · post 1 회씩 · 재확인 2 ce06b)',
        rc == 0 and nb == {}, (rc, nb, [ln for ln in lines if ln.startswith('FAIL')][:3], log[-200:]))
    #  (c) 부르는 쪽 격리 없이 전역 설정 셋 → selftest 임시 저장소 · 시험 모듈 고정물 도우미 다섯 = 훅 0 · 고정물 커밋 하나
    bad = {}
    for kn, extra in kinds.items():
        rc, lines, log = selftest_lines(dict(CLEAN, TMPDIR=TD, **extra))
        n = marks_count(marks)
        if not (rc == 0 and n == {}):
            bad[f'selftest · {kn}'] = (rc, n, [ln for ln in lines if ln.startswith('FAIL')][:2])
        for mod, attr in G7_HELPERS:
            fx = os.path.join(TD, f'g7c_{mod}_{len(os.listdir(TD))}')
            rc, out, err = run_py(G7C_CODE, [mod, attr, SCRIPTS, TOOLS6, fx], dict(CLEAN, TMPDIR=TD, **extra))
            n = marks_count(marks)
            cnt = g(fx, 'rev-list', '--count', 'HEAD', check=False).strip() if os.path.isdir(os.path.join(fx, '.git')) else None
            if not (rc == 0 and n == {} and cnt == '1' and tagged(out, 'G7C') == 'ok'):
                bad[f'{mod}.{attr} · {kn}'] = (rc, n, cnt, err[-160:])
    fx_env = getattr(RC, 'git_fixture_env', None)
    fe = fx_env() if fx_env else {}
    chk('G7c 부르는 쪽 격리 없이 전역 설정 셋 (HOME core.hooksPath · XDG_CONFIG_HOME core.hooksPath · HOME init.templateDir) → run_contract --selftest '
        '(RCPT-sha 임시 저장소) · 시험 모듈 고정물 도우미 다섯 (test_rint_r_chain.git_ · e2e._git · e2e12.git · probe6.git · test_ca_s0_census._git) 의 '
        'commit 에서 훅 0 회 · 고정물 커밋 하나 · `run_contract.git_fixture_env` = GIT_CONFIG_NOSYSTEM=1 · GIT_CONFIG_GLOBAL=/dev/null · HOME = 빈 임시 폴더 · '
        'XDG_CONFIG_HOME 없음 · 지울 이름 없음 (고치기 전 = 훅이 돈다)',
        not bad and fe.get('GIT_CONFIG_NOSYSTEM') == '1' and fe.get('GIT_CONFIG_GLOBAL') == os.devnull and 'XDG_CONFIG_HOME' not in fe
        and os.path.isdir(fe.get('HOME') or '') and os.listdir(fe['HOME']) == [] and fe.get('HOME') != os.environ.get('HOME')
        and not any(dropped(k) for k in fe if k != 'GIT_CONFIG_PARAMETERS'),    # ★ 11-13 RCPX-02 — 고정물 자신의 hooksPath 고정 한 줄만 (G7g 가 값을 본다)
        (bad, {k: fe.get(k) for k in ('GIT_CONFIG_NOSYSTEM', 'GIT_CONFIG_GLOBAL', 'HOME')} if fe else '고치기 전 판 — git_fixture_env 없음'))
    #  (d) ★ 3 회차 변이 보강 — 넘긴 env 의 꼴 (XDG_CONFIG_HOME · HOME 을 넘겨도 뺀다 · 이 시험 프로세스 env 에는 XDG 가 없어 (c) 꼴로는 못 가린다)
    fe2 = fx_env({'XDG_CONFIG_HOME': '/x', 'HOME': '/h', 'GIT_DIR': '/v', 'GIT_CONFIG_KEY_0': 'k', 'GIT_CEILING_DIRECTORIES': '/o', 'PATH': '/bin'}) if fx_env else {}
    chk('G7d git_fixture_env(넘긴 env) — XDG_CONFIG_HOME 뺌 · HOME = 빈 임시 폴더 (넘긴 /h 아님) · 지울 이름 (GIT_DIR · CONFIG_KEY_0) 뺌 · 천장 · PATH 남김 · '
        'NOSYSTEM=1 · GLOBAL=/dev/null (3 회차 변이 보강 — XDG 뺌 · HOME 줄을 지운 변이가 (c) 에서 안 잡혔다)',
        'XDG_CONFIG_HOME' not in fe2 and fe2.get('HOME') not in (None, '/h') and os.path.isdir(fe2.get('HOME') or '') and 'GIT_DIR' not in fe2
        and 'GIT_CONFIG_KEY_0' not in fe2 and fe2.get('GIT_CEILING_DIRECTORIES') == '/o' and fe2.get('PATH') == '/bin'
        and fe2.get('GIT_CONFIG_NOSYSTEM') == '1' and fe2.get('GIT_CONFIG_GLOBAL') == os.devnull, fe2)
    #  (e) ★ 3 회차 변이 보강 — 시험 모듈 여덟 (G6) 에서 git 을 부르는 자리 (subprocess 의 run · check_output · check_call · call · Popen · 첫 낱말 'git')
    #      는 env 를 넘긴다 (고정물 env · 넘긴 env · 도우미의 `kw.setdefault('env', …)` + `**kw`) — 예외 = 이 리포 (ROOT) 를 읽기만 하는 자리 셋.
    #      정적 훑기 (ast · 3.8 에서도 · 불러오지 않는다) — 도우미 다섯 밖의 고정물 git (init · pull · clone · git_rc) 을 지운 변이를 (c) 가 못 본다
    miss, found, ro_seen = [], {}, set()
    for mod in G6_MODULES:
        path = os.path.join(TOOLS6 if mod == 'test_probe6_read' else SCRIPTS, mod + '.py')
        sites = g7e_git_sites(path)
        found[mod] = len(sites)
        for line, has_env, consts, reads_root in sites:
            ro = [s for (m_, s) in G7E_READ_ROOT if m_ == mod and s in consts and reads_root]
            if ro:
                ro_seen.add((mod, ro[0]))
            elif not has_env:
                miss.append(f'{mod}:{line} {consts[:4]}')
    chk('G7e 시험 모듈 여덟의 git 부르는 자리 (정적 · subprocess · 첫 낱말 git) 가 모두 env 를 넘긴다 — 예외 = 이 리포를 읽기만 하는 자리 셋 '
        '(test_rint_r_chain check-ignore · test_ca_s0_census show · test_step3_conv_cert show) · 훑기가 빈손 아님 (모듈마다 자리 수 ≥ 기대) '
        '(3 회차 변이 보강 — 도우미 밖 고정물 git 의 env 를 지운 변이가 (c) 에서 안 잡혔다)',
        not miss and ro_seen == set(G7E_READ_ROOT) and all(found.get(m_, 0) >= n_ for m_, n_ in G7E_MIN_SITES.items()),
        (miss, sorted(ro_seen), found))
    #  (f) ★ 11-13 Codex 반박 1/2 RCPX-02 — 부르는 쪽 GIT_TEMPLATE_DIR (훅을 담은 template) 이 고정물 git init 에 들어와 commit 에서 훅이 돌았다 (HOME · XDG ·
    #      전역 · 시스템 설정을 끊어도 남는 길 · 옛 HOME init.templateDir 갈래는 이 길을 덮지 않는다) → 고정물 = 시험 전용 빈 private template
    tpl_dir = os.path.join(TD, 'g7_kit', 'tpl')
    home_empty = os.path.join(TD, 'g7_kit', 'home_empty')
    envf = {'HOME': home_empty, 'GIT_TEMPLATE_DIR': tpl_dir}
    bad_f = {}
    rc, lines, log = selftest_lines(dict(CLEAN, TMPDIR=TD, **envf))
    n = marks_count(marks)
    if not (rc == 0 and n == {}):
        bad_f['selftest'] = (rc, n, [ln for ln in lines if ln.startswith('FAIL')][:2])
    for mod, attr in G7_HELPERS:
        fx = os.path.join(TD, f'g7f_{mod}_{len(os.listdir(TD))}')
        rc, out, err = run_py(G7C_CODE, [mod, attr, SCRIPTS, TOOLS6, fx], dict(CLEAN, TMPDIR=TD, **envf))
        n = marks_count(marks)
        cnt = g(fx, 'rev-list', '--count', 'HEAD', check=False).strip() if os.path.isdir(os.path.join(fx, '.git')) else None
        if not (rc == 0 and n == {} and cnt == '1' and tagged(out, 'G7C') == 'ok'):
            bad_f[f'{mod}.{attr}'] = (rc, n, cnt, err[-160:])
    td_ = fe.get('GIT_TEMPLATE_DIR')
    chk('G7f 부르는 쪽 GIT_TEMPLATE_DIR (훅 넷을 담은 template · HOME 빈 폴더) → run_contract --selftest · 고정물 도우미 다섯의 commit 에서 훅 0 회 · 고정물 커밋 '
        '하나 · git_fixture_env 의 GIT_TEMPLATE_DIR = 시험 전용 빈 private 폴더 (부르는 쪽 값 아님 · RCPX-02 · 고치기 전 = 훅이 돈다)',
        not bad_f and isinstance(td_, str) and os.path.isdir(td_) and os.listdir(td_) == [] and td_ != tpl_dir
        and (fx_env(dict(envf)) or {}).get('GIT_TEMPLATE_DIR') == td_, (bad_f, td_))
    #  (g) ★ RCPX-02 — hooksPath 고정 (빈 폴더): 고정물 저장소의 .git/hooks 에 훅이 있어도 (다른 꼴로 만든 저장소 · 손으로 넣은 훅) 고정물 commit 에서 돌지
    #      않는다 · 부르는 쪽이 env 로 넣은 설정 주입은 고정물 자신의 한 줄로 바뀐다
    fxg = os.path.join(TD, 'g7g_repo')
    os.makedirs(fxg)
    genv = fx_env() if fx_env else dict(CLEAN)
    subprocess.run(['git', 'init', '-q', fxg], check=True, capture_output=True, env=genv)
    hk = os.path.join(fxg, '.git', 'hooks')
    os.makedirs(hk, exist_ok=True)
    for nm_ in ('pre-commit', 'post-commit'):
        q = os.path.join(hk, nm_)
        with open(q, 'w', encoding='utf-8') as f:
            f.write('#!/bin/sh\necho x >> "%s/%s"\nexit 0\n' % (marks, nm_))
        os.chmod(q, 0o755)
    with open(os.path.join(fxg, 'a.txt'), 'w', encoding='utf-8') as f:
        f.write('a')
    rg1 = subprocess.run(['git', '-C', fxg, *GCFG, 'add', '-A'], capture_output=True, env=genv)
    rg2 = subprocess.run(['git', '-C', fxg, *GCFG, 'commit', '-qm', 'x'], capture_output=True, env=genv)
    ng = marks_count(marks)
    hp = subprocess.run(['git', '-C', fxg, 'config', '--get', 'core.hookspath'], capture_output=True, text=True, env=genv)
    hpath = (hp.stdout or '').strip()
    inj = fx_env({'GIT_CONFIG_PARAMETERS': "'core.hookspath=/evil'", 'PATH': '/bin'}) if fx_env else {}
    chk('G7g 고정물 hooksPath = 시험 전용 빈 폴더 — 고정물 저장소 .git/hooks 의 pre · post-commit 훅이 고정물 commit 에서 0 회 (rc 0) · git config core.hookspath = '
        '그 빈 폴더 · 부르는 쪽 GIT_CONFIG_PARAMETERS (core.hookspath=/evil) 는 고정물 자신의 한 줄로 바뀐다 (RCPX-02 · 고치기 전 = .git/hooks 훅이 돈다)',
        rg1.returncode == 0 and rg2.returncode == 0 and ng == {} and hpath and os.path.isdir(hpath) and os.listdir(hpath) == []
        and '/evil' not in str(inj.get('GIT_CONFIG_PARAMETERS')) and inj.get('GIT_CONFIG_PARAMETERS') == genv.get('GIT_CONFIG_PARAMETERS'),
        (rg2.returncode, ng, hpath, inj.get('GIT_CONFIG_PARAMETERS'), (rg2.stderr or b'')[-200:]))
    #  (h) ★ 11-13 Codex 반박 1/2 §3 — 부르는 쪽 GIT_QUARANTINE_PATH (pre-receive 훅 안 꼴) 가 고정물 commit 의 ref 갱신을 막았다 (rc 128 · 거짓 멈춤) →
    #      고정물 env 에서 지운다
    qdir = os.path.join(TD, 'g7h_quarantine')
    os.makedirs(qdir)
    fxh = os.path.join(TD, 'g7h_repo')
    rc, out, err = run_py(G7C_CODE, ['test_ca_s0_census', '_git', SCRIPTS, TOOLS6, fxh], dict(CLEAN, TMPDIR=TD, GIT_QUARANTINE_PATH=qdir))
    cnt = g(fxh, 'rev-list', '--count', 'HEAD', check=False).strip() if os.path.isdir(os.path.join(fxh, '.git')) else None
    chk('G7h 부르는 쪽 GIT_QUARANTINE_PATH → 고정물 도우미 commit rc 0 · 고정물 커밋 하나 · git_fixture_env 에 GIT_QUARANTINE_PATH 없음 (§3 · 고치기 전 = ref 갱신 '
        '거부 rc 128)', rc == 0 and tagged(out, 'G7C') == 'ok' and cnt == '1' and 'GIT_QUARANTINE_PATH' not in (fx_env({'GIT_QUARANTINE_PATH': qdir}) or {}),
        (rc, cnt, err[-200:]))


# ═════════════════════════ G9 (★ 11-13 Codex 반박 1/2 §3 — 봉인용 git 객체 · 이력) ═════════════════════════
G9_CODE = r'''
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import rint_r_chain as RR
import mpm_webapp_payload as P
import ca_s0_census as S0
mode, args = sys.argv[2], json.loads(sys.argv[3])
out = {}
if mode == 'objects':
    RR.HERE = Path(args['repo'])                          # 사슬 저장소 = 고정물 F (F5 는 HERE 의 git 을 읽는다)
    out['plan_B'] = RR.plan_commit_problem('commit:' + args['A'], 'plan.json', args['shaB'])
    out['plan_A'] = RR.plan_commit_problem('commit:' + args['A'], 'plan.json', args['shaA'])
    out['ident'] = RR.git_identity(args['x'])
    out['code_sha'] = P._code_sha(args['sd'])
    out['s0_show'] = S0._git(args['repo'], 'show', args['A'] + ':plan.json').stdout
else:
    led = Path(args['led'])
    out['hist'] = RR.ledger_history_problem(led, args['head'])
    out['repo'] = RR.ledger_repo_problem(led)
    out['anc'] = bool(RR.ledger_is_ancestor(led, args['side'], args['head']))
    try:
        S0.verify_plan_commit(str(led), args['side'], 'plan.json', r_plan_path='rplan.json')
        out['s0'] = None
    except S0.S0Error as e:
        out['s0'] = str(e)
print('G9 ' + json.dumps(out, ensure_ascii=False))
'''
#: graft · shallow 사유 글에 들어갈 낱말 (고친 판의 사유 = 'shallow' · 'graft' · unshallow 안내)
G9_HIST_WORDS = ('shallow', 'graft')
#: 원장 파일 이름 (= `rint_r_chain.LEDGER_FILE` · 시험 쪽 기준 글자)
RR_LEDGER = 'rint_r_attempts.jsonl'


def g9_run(mode, args, env):
    rc, out, err = run_py(G9_CODE, [SCRIPTS, mode, json.dumps(args)], env)
    return json.loads(tagged(out, 'G9') or 'null'), rc, err


def g9_hist_reason(s):
    return isinstance(s, str) and any(w in s for w in G9_HIST_WORDS)


@case('G9 봉인용 git 객체 · 이력 — replacement · graft · shallow (11-13 Codex 반박 1/2 §3)')
def g9():
    import hashlib as _h
    nr = dict(CLEAN, GIT_NO_REPLACE_OBJECTS='1')               # 시험 쪽 기준 git (대체 객체를 따르지 않는다)

    def gn(repo, *a, check=True):
        r = subprocess.run(['git', '-C', repo, *GCFG, *a], capture_output=True, text=True, env=nr, stdin=subprocess.DEVNULL)
        if check and r.returncode != 0:
            raise RuntimeError(f'기준 git {a[:2]} rc {r.returncode}: {r.stderr[:300]}')
        return r.stdout
    #  ── 객체 (replacement): 고정물 F — 커밋 A (plan A · x 1) · 커밋 B (plan B · x 2) · HEAD = A (떨어진 HEAD) · 작업 트리 · 색인 = B 의 트리 (dirty ·
    #     A → B 대체 아래에서는 HEAD 트리가 B 로 보여 깨끗해진다 = 판정문 §3 꼴)
    def make_f(name):
        f = make_repo(name, {'plan.json': 'A-plan\n', 'scripts/x.py': 'X = 1\n'})
        a_ = gn(f, 'rev-parse', 'HEAD').strip()
        for rel, txt in (('plan.json', 'B-plan\n'), ('scripts/x.py', 'X = 2\n')):
            with open(os.path.join(f, rel), 'w', encoding='utf-8') as fh:
                fh.write(txt)
        gn(f, 'add', '-A')
        gn(f, 'commit', '-qm', 'B')
        b_ = gn(f, 'rev-parse', 'HEAD').strip()
        gn(f, 'checkout', '-q', a_)
        for rel, txt in (('plan.json', 'B-plan\n'), ('scripts/x.py', 'X = 2\n')):      # 작업 트리 · 색인 = B 의 트리 (A 와 다름 = dirty)
            with open(os.path.join(f, rel), 'w', encoding='utf-8') as fh:
                fh.write(txt)
        gn(f, 'add', '-A')
        return f, a_, b_
    sha_a = _h.sha256(b'A-plan\n').hexdigest()
    sha_b = _h.sha256(b'B-plan\n').hexdigest()
    res = {}
    for form in ('clean', 'GIT_REPLACE_REF_BASE', 'refs/replace (기본)'):
        f, a_, b_ = make_f('g9_obj_' + str(len(res)))
        env = dict(CLEAN, TMPDIR=TD)
        if form == 'GIT_REPLACE_REF_BASE':
            gn(f, 'update-ref', 'refs/zzrep/' + a_, b_)
            env['GIT_REPLACE_REF_BASE'] = 'refs/zzrep/'
        elif form == 'refs/replace (기본)':
            gn(f, 'replace', a_, b_)
        args = {'repo': f, 'A': a_, 'shaA': sha_a, 'shaB': sha_b, 'x': os.path.join(f, 'scripts', 'x.py'), 'sd': os.path.join(f, 'scripts')}
        res[form] = g9_run('objects', args, env) + (a_,)
    ok_o, why_o = True, {}
    for form, (val, rc, err, a_) in res.items():
        good = (rc == 0 and isinstance(val, dict) and val.get('plan_A') is None and isinstance(val.get('plan_B'), str)
                and (val.get('ident') or {}).get('head') == a_ and (val.get('ident') or {}).get('dirty') is True
                and str(val.get('code_sha')).endswith('+dirty') and val.get('s0_show') == 'A-plan\n')
        if not good:
            ok_o = False
            why_o[form] = (rc, val, err[-200:])
    chk('G9a 대체 객체 (replacement) — 깨끗 · GIT_REPLACE_REF_BASE (refs/zzrep/<A> = B) · 기본 refs/replace/<A> = B 세 꼴 모두: F5 plan_commit_problem 은 A 의 '
        '원 blob 을 읽는다 (A 해시 = None · B 해시 = 사유) · 사슬 git_identity HEAD = A · dirty True · payload _code_sha = +dirty · S0 _git show = A 내용 '
        '(GIT_NO_REPLACE_OBJECTS=1 · 고치기 전 = B 바이트를 받고 dirty 가 사라진다)', ok_o, why_o)
    #  ── 이력 (graft · shallow): 원장 저장소 L — c1 'a' → c2 'b' (줄 바꿈 = 덧붙이기 아님) → c3 'b c' · 곁가지 d (L 의 HEAD 조상 아님)
    def make_l(name):
        led = make_repo(name, {RR_LEDGER: 'a\n'})
        c1 = gn(led, 'rev-parse', 'HEAD').strip()
        gn(led, 'checkout', '-q', '-b', 'side')
        with open(os.path.join(led, 'side.txt'), 'w', encoding='utf-8') as fh:
            fh.write('s\n')
        gn(led, 'add', '-A')
        gn(led, 'commit', '-qm', 'side')
        d_ = gn(led, 'rev-parse', 'HEAD').strip()
        gn(led, 'checkout', '-q', 'main')
        for txt in ('b\n', 'b\nc\n'):
            with open(os.path.join(led, RR_LEDGER), 'w', encoding='utf-8') as fh:
                fh.write(txt)
            gn(led, 'commit', '-qam', 'l')
        c3 = gn(led, 'rev-parse', 'HEAD').strip()
        return led, c1, d_, c3
    hres = {}
    for form in ('clean', 'GIT_SHALLOW_FILE', 'GIT_GRAFT_FILE', 'GIT_GRAFT_FILE (없는 파일)', 'info/grafts', 'shallow clone'):
        led, c1, d_, c3 = make_l('g9_led_' + str(len(hres)))
        env = dict(CLEAN, TMPDIR=TD)
        if form == 'GIT_GRAFT_FILE (없는 파일)':                    # env 가 있기만 해도 닫힘 (값 무관 · 겹 방어 판별 — git 경로 검사로는 못 본다)
            env['GIT_GRAFT_FILE'] = os.path.join(TD, 'g9_no_such_graft')
        if form == 'GIT_SHALLOW_FILE':
            q = os.path.join(TD, f'g9_shallow_{len(hres)}')
            with open(q, 'w') as fh:
                fh.write(c3 + '\n')
            env['GIT_SHALLOW_FILE'] = q
        elif form == 'GIT_GRAFT_FILE':
            q = os.path.join(TD, f'g9_graft_{len(hres)}')
            with open(q, 'w') as fh:
                fh.write(f'{c3} {d_}\n')                           # c3 의 부모 = 곁가지 d (원장 역사 잘림 · d 가 조상처럼)
            env['GIT_GRAFT_FILE'] = q
        elif form == 'info/grafts':
            os.makedirs(os.path.join(led, '.git', 'info'), exist_ok=True)
            with open(os.path.join(led, '.git', 'info', 'grafts'), 'w') as fh:
                fh.write(f'{c3}\n')                                  # c3 = 뿌리 (원장 역사 잘림 · 줄 바꾼 c2 가 안 보인다)
        elif form == 'shallow clone':
            cl = os.path.join(TD, f'g9_led_shallow_{len(hres)}')
            subprocess.run(['git', 'clone', '-q', '--depth', '1', '--no-single-branch', 'file://' + led, cl], check=True, capture_output=True, env=CLEAN)
            led = cl
            gn(led, 'fetch', '-q', '--depth', '1', 'origin', 'side')
        args = {'led': led, 'head': c3, 'side': d_}
        hres[form] = g9_run('history', args, env)
    v0 = hres['clean'][0] or {}
    ok_c = (hres['clean'][1] == 0 and isinstance(v0.get('hist'), str) and not g9_hist_reason(v0.get('hist')) and v0.get('repo') is None
            and v0.get('anc') is False and isinstance(v0.get('s0'), str) and not g9_hist_reason(v0.get('s0')))
    chk('G9b 기준 — 깨끗한 원장 저장소: 원장 역사 = 줄 바꿈 사유 (graft · shallow 낱말 없음) · 저장소 꼴 문제 없음 · 곁가지 d 는 조상 아님 · S0 단계 2 관문 = 조상 아님 '
        '사유 (판별이 선다)', ok_c, hres['clean'])
    bad_h = {}
    for form in ('GIT_SHALLOW_FILE', 'GIT_GRAFT_FILE', 'GIT_GRAFT_FILE (없는 파일)', 'info/grafts', 'shallow clone'):
        val, rc, err = hres[form]
        v = val or {}
        if not (rc == 0 and g9_hist_reason(v.get('hist')) and g9_hist_reason(v.get('repo')) and v.get('anc') is False and g9_hist_reason(v.get('s0'))):
            bad_h[form] = (rc, v, err[-160:])
    chk('G9c graft · shallow 가 걸린 이력 — GIT_SHALLOW_FILE (HEAD 만) · GIT_GRAFT_FILE (c3 의 부모 = 곁가지) · GIT_GRAFT_FILE (없는 파일 · env 만으로 닫힘) · '
        '.git/info/grafts (c3 = 뿌리) · 실제 얕은 복제 다섯 모두: 원장 역사 = '
        'graft · shallow 사유 (unshallow 안내 · 잘린 역사를 통과시키지 않는다) · 원장 저장소 꼴 = 같은 사유 · 곁가지 조상 대조 = False · S0 단계 2 관문 = 같은 사유 '
        '(닫힘 · 고치기 전 = 잘린 역사 통과 · 곁가지가 조상)', not bad_h, bad_h)


# ═════════════════════════ G8 (★ 3 회차 · 재확인 2 RCP3-05) ═════════════════════════
#: 같은 셸 꼴 (`run_contract.GIT_DROP_SH` 글자 그대로) 을 둘 자리 — head = 첫 단계 (`run `) 앞 줄 하나 · code_sha = 러너 기각 영수증 code_sha 줄 안 ·
#  s0q = S0 블록 heredoc (`bash <<'S0Q'`) 안 첫 `git -C` 앞 줄 하나
SH_FILES = (('scripts/check_all.sh', 'head'), ('scripts/check_kgy_py38.sh', 'head'), ('scripts/sdcp_gain_vox015_8arm.sh', 'code_sha'),
            ('docs/reviews/rint2_s0_store_probe_20261112/s0_rerun_probe_block.txt', 's0q'))


def sh_place_problem(kind, text, sh):
    """셸 꼴 sh 가 그 파일의 제자리에 글자 그대로 (한 번) 있는가 → 사유 | None."""
    lines = text.splitlines()
    hit = [i for i, ln in enumerate(lines) if sh in ln]
    if len(hit) != 1:
        return f'셸 꼴 줄 수 {len(hit)} (1 이어야)'
    i = hit[0]
    if kind == 'head':
        first = [j for j, ln in enumerate(lines) if ln.startswith('run ')]
        if not first or i > first[0] or lines[i].strip() != sh:
            return f'첫 단계 앞 줄 하나가 아니다 (줄 {i + 1} · 첫 run {first[0] + 1 if first else None})'
    elif kind == 'code_sha':
        if 'code_sha=' not in lines[i] or 'rev-parse --short=8 HEAD' not in lines[i]:
            return '기각 영수증 code_sha 줄이 아니다'
    elif kind == 's0q':
        h = [j for j, ln in enumerate(lines) if ln.strip() == "bash <<'S0Q'"]
        g0 = [j for j, ln in enumerate(lines) if h and j > h[0] and 'git -C' in ln]
        if not (h and g0 and h[0] < i < g0[0] and lines[i].strip() == sh):
            return f'S0Q 안 첫 git 앞 줄 하나가 아니다 (줄 {i + 1})'
    return None


G8C_CODE = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import ca_s0_census as S0
ci = S0._code_info()
print('G8C ' + json.dumps({'head': ci.get('git_head'), 'dirty': ci.get('git_dirty')}))
'''


@case('G8 게이트 수준 — 셸 꼴 넷 · check_review_findings --selftest · ca_s0_census (3 회차 RCP3-05)')
def g8():
    import run_contract as RC
    #  (a) 셸 꼴 — 자리 · 글자 · 동작 (bash 로 돌린 뒤 남는 GIT_ 이름 = 파이썬 규칙)
    sh = getattr(RC, 'GIT_DROP_SH', None)
    if not isinstance(sh, str):
        chk('G8a run_contract.GIT_DROP_SH (셸 꼴) 이 있고 게이트 머리 둘 · 러너 code_sha 줄 · S0 블록 머리에 같은 글자로 있다', False, '고치기 전 판 — 없음')
    else:
        probs = {}
        for rel, kind in SH_FILES:
            with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
                pr = sh_place_problem(kind, f.read(), sh)
            if pr:
                probs[rel] = pr
        synth = {k: 'x' for k in DROP_EXPECT}
        synth.update({'GIT_CONFIG_KEY_0': 'k', 'GIT_CONFIG_VALUE_0': 'v', 'GIT_CONFIG_KEY_7': 'k', 'GIT_CONFIG_VALUE_7': 'v',
                      'GIT_CEILING_DIRECTORIES': '/o', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_SYSTEM': '/s',
                      'GIT_AUTHOR_NAME': 'a', 'GIT_EXEC_PATH': '/e', 'GIT_EDITOR': ':', 'XGIT_DIR': 'k'})
        r = subprocess.run(['bash', '-c', sh + '\ncompgen -e'], env=dict(synth, PATH=os.environ.get('PATH', '/usr/bin:/bin')), capture_output=True,
                           text=True, timeout=60, stdin=subprocess.DEVNULL)
        left = sorted(x for x in (r.stdout or '').split() if x in synth)
        want = sorted(k for k in synth if not dropped(k))
        chk('G8a 셸 꼴 (`run_contract.GIT_DROP_SH`) 이 check_all.sh · check_kgy_py38.sh 머리 (첫 단계 앞) · 러너 기각 영수증 code_sha 줄 · S0 블록 heredoc '
            '머리 (첫 git 앞) 에 같은 글자로 한 번씩 · bash 로 돌린 뒤 남는 이름 = 파이썬 규칙 (격리 변수 · 신원 · 실행 자리 · GIT_ 아닌 이름은 남고 저장소 '
            '고르는 이름 · 설정 주입은 사라짐) = `git_env` 결과 (★ 11-13 — git_env 가 더 넣는 GIT_NO_REPLACE_OBJECTS=1 빼고 · 셸 꼴은 이름 지우기만 = 한정)',
            not probs and r.returncode == 0 and left == want and sorted(k for k in RC.git_env(synth) if k not in SET_EXPECT) == want
            and all(RC.git_env(synth).get(k) == v for k, v in SET_EXPECT.items()), (probs, r.returncode, left, want, (r.stderr or '')[-160:]))
    #  (b) check_review_findings --selftest — 매달린 커밋 (commit-tree = 쓰기) 이 자기 저장소 (일회용 사본 F) 에 · V 그대로
    src = {}
    for rel in ('scripts/check_review_findings.py', 'scripts/run_contract.py'):
        with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
            src[rel] = f.read()

    def crf(env, _v=None):
        fr = make_repo(f'g8b_F_{len(os.listdir(TD))}', src)
        n0 = repo_state(fr)['n_objects']
        r = subprocess.run([sys.executable, os.path.join(fr, 'scripts', 'check_review_findings.py'), '--selftest'], capture_output=True, text=True,
                           env=env, timeout=600, cwd=TD, stdin=subprocess.DEVNULL)
        return repo_state(fr)['n_objects'] - n0, r.returncode, (r.stderr or '') + (r.stdout or '')[-200:]
    d0, rc0, log0 = crf(dict(CLEAN, TMPDIR=TD))
    res = per_variant('g8b', crf)
    bad = {nm: (same, val, rc, why[0]) for nm, (same, val, rc, why) in res.items() if not (same and isinstance(val, int) and val >= 1)}
    chk('G8b check_review_findings --selftest (19b 매달린 커밋 · commit-tree = 쓰기) — 깨끗한 환경 = 자기 저장소 (일회용 사본 F) 에 객체가 생긴다 (판별) · '
        '적대 환경 넷에서도 F 에 생기고 V 그대로 (고치기 전 = GIT_DIR · OBJECT_DIRECTORY 꼴에서 V 에 객체 · 재확인 2 ce06 B)',
        d0 >= 1 and not bad, (d0, rc0, bad, log0[-200:] if d0 < 1 else ''))
    #  (c) ca_s0_census._code_info — S0 보고 git_head · git_dirty (이 리포를 읽는다)
    want_head = g(ROOT, 'rev-parse', 'HEAD').strip()
    rc0, out0, err0 = run_py(G8C_CODE, [SCRIPTS], dict(CLEAN, TMPDIR=TD))
    ref = json.loads(tagged(out0, 'G8C') or 'null')
    chk('G8c 기준 — 깨끗한 환경의 ca_s0_census._code_info = 이 리포 HEAD · dirty 칸 bool', rc0 == 0 and isinstance(ref, dict)
        and ref.get('head') == want_head and isinstance(ref.get('dirty'), bool), (rc0, ref, err0[-300:]))

    def run_c(env, _v):
        rc, out, err = run_py(G8C_CODE, [SCRIPTS], env)
        return json.loads(tagged(out, 'G8C') or 'null'), rc, err
    res = per_variant('g8c', run_c)
    bad = {nm: (same, rc, val, why[0]) for nm, (same, val, rc, why) in res.items() if not (same and rc == 0 and val == ref)}
    chk('G8c 적대 환경 넷에서 ca_s0_census._code_info (git_head · git_dirty) = 깨끗한 환경 값 (V 의 HEAD · 색인을 읽지 않는다) · V 그대로 (index.lock 포함 · '
        '고치기 전 = GIT_DIR 꼴 둘 = V 의 HEAD · 객체 꼴 · 훅 꼴 = dirty 모름 (None))', not bad, bad)


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
