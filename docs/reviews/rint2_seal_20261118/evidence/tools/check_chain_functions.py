#!/usr/bin/env python3
"""봉인 꼴 트리의 봉인본 · 원본 자리 · 계획 · S0 계획을 핀 사슬 함수로 대조 — 리포 무변경 · 결과 0 건 · σ 없음 · 러너 없음.

argv: <봉인 꼴 트리 (scripts · docs)> <봉인 날짜 (8 자리 · 봉인본 · 계획 자리)> [candidate | final]  (v2.1 · 리뷰 P3-9 = 날짜를 인자로)
  candidate (기본 · v2.1 후보) = 결과 전 등록 넷 null → require_plan_numbers 가 PLAN_NUMBER_UNREGISTERED 로 멈춰야 OK
  final (봉인 · 20261118 판에서 더함) = 넷이 채워진 봉인 계획 → require_plan_numbers 가 멈추지 않아야 OK (그 밖 판정 = 같다)
"""
import hashlib
import os
import sys

T, DATE = sys.argv[1:3]
MODE = sys.argv[3] if len(sys.argv) > 3 else 'candidate'
assert MODE in ('candidate', 'final'), MODE
RPN = 'require_plan_numbers (후보 계획)' if MODE == 'candidate' else 'require_plan_numbers (봉인 계획)'
assert len(DATE) == 8 and DATE.isascii() and DATE.isdigit(), DATE
sys.path.insert(0, os.path.join(T, 'scripts'))
import rint_r_chain as R  # noqa: E402

SEALED = os.path.join(T, f'docs/reviews/rint2_seal_{DATE}/registration_R_sealed.md')
ORIG = os.path.join(T, 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md')
PLAN = os.path.join(T, f'docs/data/rint2_r_plan_{DATE}/ca1_plan.json')
S0 = os.path.join(T, 'docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json')
s0sha = hashlib.sha256(open(S0, 'rb').read()).hexdigest()
res = {}


def tri(name, fn):
    try:
        v = fn()
        res[name] = ('ok', v)
    except R.Stop as e:
        res[name] = ('stop', f'{e.code}: {str(e.cause)[:150]}')
    print(f'{name}: {res[name][0]} · {res[name][1] if not isinstance(res[name][1], tuple) else res[name][1][0]}')


plan, psha = R.load_plan(PLAN)
print(f'load_plan sha256 {psha} · plan_form_problems {R.plan_form_problems(plan)}')
tri('봉인본 registration_plan_hash', lambda: R.registration_plan_hash(SEALED))
tri('봉인본 registration_s0_hash', lambda: R.registration_s0_hash(SEALED))
tri('원본 자리 registration_plan_hash', lambda: R.registration_plan_hash(ORIG))
tri('원본 자리 registration_s0_hash', lambda: R.registration_s0_hash(ORIG))
print(f'봉인본 plan_doc_problem {R.plan_doc_problem(SEALED, plan)}')
print(f'원본 자리 plan_doc_problem {(R.plan_doc_problem(ORIG, plan) or "")[:90]}')
tri('봉인본 check_plan_registered', lambda: sorted(R.check_plan_registered(psha, SEALED)))
tri('원본 자리 check_plan_registered', lambda: sorted(R.check_plan_registered(psha, ORIG)))
tri('봉인본 load_s0_plan (S0 해시 줄 · 두 계획 대조)', lambda: R.load_s0_plan(S0, SEALED, plan)['sha256'])
print(f'plans_cross_problems {R.plans_cross_problems(plan, R._json_strict(open(S0, "rb").read(), "ascii"))}')
print(f'plan_env {R.plan_env(plan)}')
tri(RPN, lambda: R.require_plan_numbers(plan))
rpn_ok = (res[RPN][0] == 'stop' and res[RPN][1].startswith('PLAN_NUMBER_UNREGISTERED')) if MODE == 'candidate' else (res[RPN] == ('ok', None))
ok = (res['봉인본 registration_plan_hash'][0] == 'ok' and res['봉인본 registration_plan_hash'][1][0] == psha
      and res['봉인본 registration_s0_hash'][0] == 'ok' and res['봉인본 registration_s0_hash'][1][0] == s0sha
      and res['원본 자리 registration_plan_hash'] [1].startswith('PLAN_HASH_UNREGISTERED')
      and res['원본 자리 registration_s0_hash'][1].startswith('S0_PLAN_HASH_UNREGISTERED')
      and R.plan_doc_problem(SEALED, plan) is None and R.plan_doc_problem(ORIG, plan) is not None
      and res['봉인본 load_s0_plan (S0 해시 줄 · 두 계획 대조)'] == ('ok', s0sha)
      and rpn_ok)
print('결과', MODE, 'OK' if ok else 'NOT OK')
sys.exit(0 if ok else 1)
