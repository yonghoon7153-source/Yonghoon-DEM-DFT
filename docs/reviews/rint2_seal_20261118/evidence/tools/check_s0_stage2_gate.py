#!/usr/bin/env python3
"""S0 단계 2 관문 (`ca_s0_census.verify_plan_commit`) 을 봉인 꼴 커밋으로 — 리포 무변경 · 결과 0 건 · 킷 · 풀이 · σ 없음.

argv: <봉인 꼴 사본 (git · HEAD = 봉인 꼴 커밋)> <고정물 값 봉인본 (make_sealed_copy 출력 폴더)> <둘째 사본 자리 (없어야)> <봉인 날짜 (8 자리)>  (v2.1 · 리뷰 P3-9)
  ① 사본 HEAD (후보 · 넷 null) — r_doc = 봉인본 → 거부 · 사유 = 결과 전 등록 넷뿐 · r_doc = 기본 (원본 자리) → 거부 (S0 해시 줄 ⬜)
  ② 둘째 사본 (`git clone --shared --no-checkout` · 작업 트리 없음) 에 커밋 C = HEAD + 고정물 계획 (시험 값 · 등록 숫자 아님) + 그 계획으로
     도구가 다시 만든 봉인본 (read-tree · update-index · write-tree · commit-tree = 그 사본의 자기 색인 · GIT_* 환경 변수 없음) → r_doc = 봉인본 → 통과
GIT_DIR · GIT_WORK_TREE · GIT_INDEX_FILE 은 쓰지 않는다 (git -C <사본> 만 · 신원 = -c user.name · user.email).
"""
import hashlib
import os
import subprocess
import sys

REPO, FIX, REPO2, DATE = sys.argv[1:5]
assert len(DATE) == 8 and DATE.isascii() and DATE.isdigit(), DATE
assert not os.path.exists(REPO2), REPO2
SEALED = f'docs/reviews/rint2_seal_{DATE}/registration_R_sealed.md'
ORIG = 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'
PLAN = f'docs/data/rint2_r_plan_{DATE}/ca1_plan.json'
S0 = 'docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json'
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
ID = ('-c', 'user.name=scratch', '-c', 'user.email=scratch@invalid', '-c', 'commit.gpgsign=false')


def git(repo, *a, inp=None):
    r = subprocess.run(['git', '-C', repo] + list(ID) + list(a), capture_output=True, env=ENV, input=inp)
    if r.returncode != 0:
        raise SystemExit(f'git {a[:3]} rc {r.returncode}: {r.stderr.decode()[:300]}')
    return r.stdout.decode().strip()


sys.path.insert(0, os.path.join(REPO, 'scripts'))
import ca_s0_census as S0m  # noqa: E402
import rint_r_chain as RR  # noqa: E402

A = git(REPO, 'rev-parse', 'HEAD')
print(f'# 사본 HEAD (후보) {A} · S0 계획 sha256 {hashlib.sha256(open(os.path.join(REPO, S0), "rb").read()).hexdigest()}')


def gate(repo, sha, r_doc, label):
    try:
        plan, h, full, rinfo = S0m.verify_plan_commit(repo, sha, S0, r_doc, r_plan_path=PLAN)
        print(f'[{label}] PASS · S0 sha {h[:16]}… · 커밋 {full[:12]} · R 계획 {rinfo["sha256"][:16]}… · s_min {rinfo["s_min_um"]} · '
              f'tol_ff {rinfo["tol_ff_um"]} · {rinfo["checked"]}')
        return 'PASS', ''
    except S0m.S0Error as e:
        print(f'[{label}] REJECT · {e}')
        return 'REJECT', str(e)


v1, m1 = gate(REPO, A, SEALED, '① 후보 커밋 · r_doc = 봉인본')
four = ['max_ladder_points', 'calib_rj_ratio_max', 'sv_cf_threshold', 'sv_cf_scope']
import re  # noqa: E402
_lst = re.search(r"\[([^\]]*)\]", m1)
named = sorted(x.strip().strip("'") for x in _lst.group(1).split(',')) if _lst else None
only_four = v1 == 'REJECT' and 'PLAN_NUMBER_UNREGISTERED' in m1 and named == sorted(four)
print(f'   → 거부 사유 = 결과 전 등록 넷뿐: {only_four}')
v2, m2 = gate(REPO, A, ORIG, '① 후보 커밋 · r_doc = 기본 (원본 자리)')
# ② 고정물 값 커밋 C (둘째 사본 · 작업 트리 없음)
git(os.path.dirname(REPO2) or '.', 'clone', '-q', '--shared', '--no-checkout', REPO, REPO2)
git(REPO2, 'read-tree', A)
fix_plan = open(os.path.join(FIX, PLAN), 'rb').read()
fix_sealed = open(os.path.join(FIX, SEALED), 'rb').read()
for rel, b in ((PLAN, fix_plan), (SEALED, fix_sealed)):
    blob = git(REPO2, 'hash-object', '-w', '--stdin', inp=b)
    git(REPO2, 'update-index', '--cacheinfo', f'100644,{blob},{rel}')
tree = git(REPO2, 'write-tree')
C = git(REPO2, 'commit-tree', tree, '-p', A, '-m', 'scratch fixture values (test values · NOT registered numbers)')
git(REPO2, 'update-ref', 'refs/heads/fixture-scratch', C)
git(REPO2, 'symbolic-ref', 'HEAD', 'refs/heads/fixture-scratch')
print(f'# 둘째 사본 HEAD = C {C} (부모 {A[:12]}) · 고정물 계획 sha256 {hashlib.sha256(fix_plan).hexdigest()} · 바뀐 경로 '
      f'{git(REPO2, "diff-tree", "--no-commit-id", "--name-only", "-r", A, C).split()}')
v3, m3 = gate(REPO2, C, SEALED, '② 고정물 값 커밋 C · r_doc = 봉인본')
v4, m4 = gate(REPO2, A, SEALED, '② (C 가 HEAD 일 때) 후보 커밋 A · r_doc = 봉인본')
#  사슬 함수 — C 의 봉인본 (블록 · 해시 = 고정물 계획)
import tempfile  # noqa: E402


def _rpn(plan):
    try:
        RR.require_plan_numbers(plan)
        return True
    except RR.Stop as e:
        return f'멈춤 {e.code}'
with tempfile.TemporaryDirectory(prefix='s0g_') as td:
    sp = os.path.join(td, 'sealed.md')
    pp = os.path.join(td, 'plan.json')
    open(sp, 'wb').write(fix_sealed)
    open(pp, 'wb').write(fix_plan)
    plan, psha = RR.load_plan(pp)
    print(f'# C 봉인본: registration_plan_hash = 고정물 계획 sha256 {RR.registration_plan_hash(sp)[0] == psha} · plan_doc_problem {RR.plan_doc_problem(sp, plan)} · '
          f'require_plan_numbers 통과 {_rpn(plan)}')
ok = only_four and v2 == 'REJECT' and v3 == 'PASS' and v4 == 'REJECT'
print('결과', 'OK (후보 = 넷 때문에만 거부 · 기본 경로 = 거부 · 고정물 값 = 통과)' if ok else 'NOT OK')
sys.exit(0 if ok else 1)
