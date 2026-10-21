#!/usr/bin/env python3
"""P07 — 영수증 도구 selftest 를 실물 자리에서 (도구 판 × 등록 문서 상태 × 변이) 다시 돌린다 (증거 로그를 믿지 않고 직접).
각 경우: 작업 트리의 scripts/supp20_input_receipt.py · 두 등록 문서를 그 경우의 바이트로 잠시 바꾸고 → `python3 -I scripts/supp20_input_receipt.py --selftest`
→ PASS/FAIL 수 · 실패 이름 · S0 · S0b · S11g 줄 · rc · 초 → 끝나면 (예외여도) `git checkout HEAD -- <세 파일>` 로 되돌리고 git status 깨끗한지 본다.
재실행 (기계 잠금 아래 · 한 번에 하나): cd <worktree> && bash <SCRATCH>/heavy.sh python3 -I p07_insitu.py <worktree> <out.json> [경우 이름 …]"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
WT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
ONLY = set(sys.argv[3:])
TOOL = 'scripts/supp20_input_receipt.py'
SUPP = 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md'
B194 = 'docs/reviews/lhs_network_batch_registration_20261007_g2.md'
FILES = (TOOL, SUPP, B194)
OLD_TOOL_REV = 'a6996396774064fa159d360da0e1d26877b66c33'      # 고치기 전 (= a76f59d0d = 34713ac96 판 · sha256 2c7e0b81…)
PRE_DOC_REV = 'fe23f2b839f0a49adb077348fec6d4c85443b62a'       # 비준 전 문서 (pending)
RAT_COMMIT = 'f82929b0644be39b44e9fba9ea04cf9d60de9146'        # 비준 커밋 문서 (대화 원문 ⬜)


def git(*a, check=True):
    return subprocess.run(['git', *a], cwd=WT, capture_output=True, check=check)


def show(rev, f):
    return git('show', f'{rev}:{f}').stdout


HEAD_TOOL = show('HEAD', TOOL).decode('utf-8')
X1 = hashlib.sha256(b'prereview lhs214 x1').hexdigest()
X2 = hashlib.sha256(b'prereview lhs214 x2').hexdigest()


def mut(src, old, new):
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new)


# 옛 S0b 식 (고치기 전 판 그대로의 판정) 을 s0b_fp 몸에 — "새 시험 + 옛 식" (시험 먼저의 고치기 전)
OLD_EXPR_BODY = ("        r_, p_ = reg_.get('code_fp'), reg_.get('code_fp_pending')\n"
                 "        return (str(r_ or '').startswith('e8b2496b') and (p_ is None or str(p_).startswith('2149f873'))), 'old prefix expression'\n")


def old_expr_tool(src):
    i = src.index('    def s0b_fp(reg_, base_, base_probs=()):')
    j = src.index("        return True, f'상태 {st_}'\n", i) + len("        return True, f'상태 {st_}'\n")
    head = src[i:src.index('        r_, p_ = reg_.get', i)]
    return src[:i] + head + OLD_EXPR_BODY + src[j:]


MUTS = {
    'm1_leftover_off': lambda s: mut(s, "        if st_ == 'registered' and p_ is not None:", "        if False and st_ == 'registered' and p_ is not None:"),
    'm2_crossdoc_off': lambda s: mut(s, "        if (r_, p_) != b_:", "        if False and (r_, p_) != b_:"),
    'm3_baseprobs_off': lambda s: mut(s, "        if bp_:", "        if False and bp_:"),
    'm4_undeclared_ok': lambda s: mut(s, "        if st_ == 'undeclared':\n            return False, f'상태 undeclared — {why_}'",
                                       "        if False and st_ == 'undeclared':\n            return False, f'상태 undeclared — {why_}'"),
    'm5_crossdoc_R_only': lambda s: mut(s, "        if (r_, p_) != b_:", "        if r_ != b_[0]:"),
    'm6_crossdoc_prefix12': lambda s: mut(s, "        if (r_, p_) != b_:", "        if (str(r_)[:12], str(p_)[:12]) != (str(b_[0])[:12], str(b_[1])[:12]):"),
    'm7_state_prefix12': lambda s: mut(mut(s, "        if now is not None and now == r_:", "        if now is not None and str(now)[:12] == str(r_)[:12]:"),
                                       "        if p_ and p_ != r_ and now == p_:", "        if p_ and p_ != r_ and str(now)[:12] == str(p_)[:12]:"),
    'm9_reg194_is_supp': lambda s: mut(s, "    REG194 = 'docs/reviews/lhs_network_batch_registration_20261007_g2.md'", "    REG194 = REG_DOC"),
    'm10_no_p194_passed': lambda s: mut(s, "    fp0_ok, fp0_why = s0b_fp(reg, v194, p194)", "    fp0_ok, fp0_why = s0b_fp(reg, v194, ())"),
    'm11_S0b_ignores_fp0': lambda s: mut(s, "and str((dg0.get('cohort_tsv_sha256') or {}).get(COHORT)).startswith('69d3f913') and fp0_ok,",
                                          "and str((dg0.get('cohort_tsv_sha256') or {}).get(COHORT)).startswith('69d3f913') and True,"),
}


def s9_append(t, line):
    return t + '\n' + line + '\n'


HEAD_SUPP, HEAD_194 = show('HEAD', SUPP).decode('utf-8'), show('HEAD', B194).decode('utf-8')
PRE_SUPP, PRE_194 = show(PRE_DOC_REV, SUPP).decode('utf-8'), show(PRE_DOC_REV, B194).decode('utf-8')
OLD_TOOL = show(OLD_TOOL_REV, TOOL).decode('utf-8')

CASES = {
    # 이름: (도구 글, 보충 글, 194 글, 설명)
    'new_head_ratified': (HEAD_TOOL, HEAD_SUPP, HEAD_194, '고친 판 · HEAD 문서 (registered)'),
    'new_pending_docs': (HEAD_TOOL, PRE_SUPP, PRE_194, '고친 판 · 비준 전 문서 (pending)'),
    'new_ratify_commit_docs': (HEAD_TOOL, show(RAT_COMMIT, SUPP).decode('utf-8'), show(RAT_COMMIT, B194).decode('utf-8'), '고친 판 · 비준 커밋 문서'),
    'new_supp_only_ratified': (HEAD_TOOL, HEAD_SUPP, PRE_194, '고친 판 · 보충만 비준'),
    'new_194_only_ratified': (HEAD_TOOL, PRE_SUPP, HEAD_194, '고친 판 · 194 만 비준'),
    'old_pending_docs': (OLD_TOOL, PRE_SUPP, PRE_194, '고치기 전 판 · 비준 전 문서'),
    'old_ratified_docs': (OLD_TOOL, HEAD_SUPP, HEAD_194, '고치기 전 판 · HEAD 문서'),
    'old_194_only_ratified': (OLD_TOOL, PRE_SUPP, HEAD_194, '고치기 전 판 · 194 만 비준'),
    'oldexpr_pending_docs': (old_expr_tool(HEAD_TOOL), PRE_SUPP, PRE_194, '새 시험 + 옛 S0b 식 · 비준 전 문서'),
    'oldexpr_ratified_docs': (old_expr_tool(HEAD_TOOL), HEAD_SUPP, HEAD_194, '새 시험 + 옛 S0b 식 · HEAD 문서'),
    'T08_supp_two_pendings': (HEAD_TOOL, s9_append(s9_append(HEAD_SUPP, f'| 대기 | `code_fp_pending {X1}` |'), f'| 대기 | `code_fp_pending {X2}` |'), HEAD_194,
                              '고친 판 · 보충 registered + 상충 대기 둘 · 194 깨끗'),
    'T10_supp_pending_eq_reg': (HEAD_TOOL, None, HEAD_194, '고친 판 · 보충 registered + 대기 = 등록 · 194 깨끗'),
    'T07_194_leftover_pending': (HEAD_TOOL, HEAD_SUPP, s9_append(HEAD_194, f'| 대기 | `code_fp_pending {X1}` |'), '고친 판 · 194 에만 남은 대기 (보충 깨끗)'),
}
for k, f in MUTS.items():
    CASES[f'mut_{k}'] = (f(HEAD_TOOL), HEAD_SUPP, HEAD_194, f'변이 {k} · HEAD 문서 (registered)')
CASES['mut_m1_pending_docs'] = (MUTS['m1_leftover_off'](HEAD_TOOL), PRE_SUPP, PRE_194, '변이 m1 · 비준 전 문서 (pending)')
CASES['mut_m2_pending_docs'] = (MUTS['m2_crossdoc_off'](HEAD_TOOL), PRE_SUPP, PRE_194, '변이 m2 · 비준 전 문서 (pending)')


def fp_now():
    r = subprocess.run([sys.executable, '-I', '-c', "import sys; sys.path.insert(0, 'scripts'); import run_network_194_parallel as N; print(N.code_fp(N.code_hashes()))"],
                       cwd=WT, capture_output=True, text=True)
    return r.stdout.strip()


FP = fp_now()
CASES['T10_supp_pending_eq_reg'] = (HEAD_TOOL, s9_append(HEAD_SUPP, f'| 대기 | `code_fp_pending {FP}` |'), HEAD_194, CASES['T10_supp_pending_eq_reg'][3])


def restore():
    git('checkout', 'HEAD', '--', *FILES)
    st = git('status', '--porcelain', '--untracked-files=no').stdout.decode()
    return st.strip() == ''


res = {}
env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
names = [n for n in CASES if not ONLY or n in ONLY]
try:
    for name in names:
        tool, supp, b194, desc = CASES[name]
        (WT / TOOL).write_text(tool, encoding='utf-8')
        (WT / SUPP).write_text(supp, encoding='utf-8')
        (WT / B194).write_text(b194, encoding='utf-8')
        for pyc in (WT / 'scripts/__pycache__').glob('supp20_input_receipt*.pyc'):
            pyc.unlink()
        t0 = time.time()
        r = subprocess.run(['nice', '-n', '19', sys.executable, '-I', '-B', TOOL, '--selftest'], cwd=WT, capture_output=True, text=True, env=env)
        dt = round(time.time() - t0, 1)
        lines = r.stdout.splitlines()
        fails = [ln.strip()[6:].split(' ')[0] for ln in lines if ln.startswith('  FAIL  ')]
        npass = sum(ln.startswith('  PASS  ') for ln in lines)
        last = [ln for ln in lines if 'supp20_input_receipt selftest:' in ln]
        key = {}
        for tag in ('S0 ', 'S0b ', 'S11g '):
            hit = [ln for ln in lines if ln.strip()[6:].startswith(tag)]
            key[tag.strip()] = [h[:8].strip() + ' ' + h[8:].strip()[:60] + (' … ' + h[h.rfind('('):][:600] if 'FAIL' in h[:8] else '') for h in hit]
        state = [ln.strip() for ln in lines if '봉인 지문 상태 =' in ln]
        res[name] = dict(desc=desc, rc=r.returncode, secs=dt, n_pass=npass, n_fail=len(fails), fails=fails, last=last, key=key, state=state,
                         tool_sha256=hashlib.sha256(tool.encode('utf-8')).hexdigest(), stderr_tail=r.stderr[-400:])
        print(name, r.returncode, f'{npass}/{npass + len(fails)}', fails, dt, 's', flush=True)
        if not restore():
            res[name]['restore'] = 'DIRTY after restore'
            break
finally:
    ok = restore()
    res['_final_clean'] = ok
    res['_fp_now'] = FP
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print('final clean', ok)
