#!/usr/bin/env python3
"""P07b — 변이가 살아남을 때 실제로 받아들여지는 나쁜 상태 (변이 × 문서 상태 짝) — p07 과 같은 방식 (실물 자리 · 끝나면 git checkout 으로 되돌림).
  T09 (194 에 상충 대기 둘 · 보충 깨끗) 고친 판 그대로 / m10 (p194 전달 끔) · combo_m5_T07 (교차 대조 = §3 만) · combo_m9_T07 (REG194 = 보충 문서) ·
  combo_m7_twin (상태 판정 접두 12 자리 · 두 등록 §3 = 체크아웃과 앞 12 자리만 같은 쌍둥이 값) · combo_m11_T07 (S0b 가 fp0_ok 를 안 씀)
재실행: cd <worktree> && bash <SCRATCH>/heavy.sh python3 -I -B p07b_combos.py <worktree> <out.json>"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path
WT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
TOOL = 'scripts/supp20_input_receipt.py'
SUPP = 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md'
B194 = 'docs/reviews/lhs_network_batch_registration_20261007_g2.md'
FILES = (TOOL, SUPP, B194)


def git(*a, check=True):
    return subprocess.run(['git', *a], cwd=WT, capture_output=True, check=check)


def show(rev, f):
    return git('show', f'{rev}:{f}').stdout.decode('utf-8')


def mut(src, old, new):
    assert src.count(old) == 1, (old, src.count(old))
    return src.replace(old, new)


HEAD_TOOL, HEAD_SUPP, HEAD_194 = show('HEAD', TOOL), show('HEAD', SUPP), show('HEAD', B194)
X1 = hashlib.sha256(b'prereview lhs214 x1').hexdigest()
X2 = hashlib.sha256(b'prereview lhs214 x2').hexdigest()
FP = subprocess.run([sys.executable, '-I', '-c', "import sys; sys.path.insert(0, 'scripts'); import run_network_194_parallel as N; print(N.code_fp(N.code_hashes()))"],
                    cwd=WT, capture_output=True, text=True).stdout.strip()
TWIN = FP[:12] + X1[12:]
assert TWIN != FP and len(TWIN) == 64


def s9_append(t, line):
    return t + '\n' + line + '\n'


def s3_sub(t, new_tok):
    i = t.find('\n## 3.')
    j = t.find('\n## ', i + 1)
    j = j if j >= 0 else len(t)
    m = re.search(r'`code_fp [0-9a-f]{64}`', t[i:j])
    a = i + m.start()
    return t[:a] + new_tok + t[a + len(m.group(0)):]


M5 = mut(HEAD_TOOL, "        if (r_, p_) != b_:", "        if r_ != b_[0]:")
M7 = mut(mut(HEAD_TOOL, "        if now is not None and now == r_:", "        if now is not None and str(now)[:12] == str(r_)[:12]:"),
         "        if p_ and p_ != r_ and now == p_:", "        if p_ and p_ != r_ and str(now)[:12] == str(p_)[:12]:")
M9 = mut(HEAD_TOOL, "    REG194 = 'docs/reviews/lhs_network_batch_registration_20261007_g2.md'", "    REG194 = REG_DOC")
M10 = mut(HEAD_TOOL, "    fp0_ok, fp0_why = s0b_fp(reg, v194, p194)", "    fp0_ok, fp0_why = s0b_fp(reg, v194, ())")
M11 = mut(HEAD_TOOL, "and str((dg0.get('cohort_tsv_sha256') or {}).get(COHORT)).startswith('69d3f913') and fp0_ok,",
          "and str((dg0.get('cohort_tsv_sha256') or {}).get(COHORT)).startswith('69d3f913') and True,")
T07_194 = s9_append(HEAD_194, f'| 대기 | `code_fp_pending {X1}` |')
T09_194 = s9_append(s9_append(HEAD_194, f'| 대기 | `code_fp_pending {X1}` |'), f'| 대기 | `code_fp_pending {X2}` |')
CASES = {
    'T09_194_two_pendings': (HEAD_TOOL, HEAD_SUPP, T09_194, '고친 판 · 194 에 상충 대기 둘 (보충 깨끗) — S0b 거짓 기대'),
    'combo_m10_T09': (M10, HEAD_SUPP, T09_194, '변이 m10 (p194 전달 끔) · 같은 문서 — 변이가 살면 S0b 참'),
    'combo_m5_T07': (M5, HEAD_SUPP, T07_194, '변이 m5 (교차 대조 §3 만) · 194 에만 남은 대기 — 변이가 살면 S0b 참'),
    'combo_m9_T07': (M9, HEAD_SUPP, T07_194, '변이 m9 (REG194 = 보충) · 194 에만 남은 대기 — 변이가 살면 S0b 참'),
    'combo_m11_T07': (M11, HEAD_SUPP, T07_194, '변이 m11 (S0b 가 fp0_ok 안 씀) · 194 에만 남은 대기'),
    'twin_unmutated': (HEAD_TOOL, s3_sub(HEAD_SUPP, f'`code_fp {TWIN}`'), s3_sub(HEAD_194, f'`code_fp {TWIN}`'), '고친 판 · 두 등록 §3 = 앞 12 자리 쌍둥이'),
    'combo_m7_twin': (M7, s3_sub(HEAD_SUPP, f'`code_fp {TWIN}`'), s3_sub(HEAD_194, f'`code_fp {TWIN}`'), '변이 m7 (상태 접두 12) · 쌍둥이 — S0 (D1 전체 비교) 가 잡나'),
}
#  변이 m1–m4 를 다시 (S11g 실패 상세 전체를 남기려고 — p07 은 마지막 괄호만 남겼다)
for _k, _old, _new in (('m1_leftover_off', "        if st_ == 'registered' and p_ is not None:", "        if False and st_ == 'registered' and p_ is not None:"),
                       ('m2_crossdoc_off', "        if (r_, p_) != b_:", "        if False and (r_, p_) != b_:"),
                       ('m3_baseprobs_off', "        if bp_:", "        if False and bp_:"),
                       ('m4_undeclared_ok', "        if st_ == 'undeclared':\n            return False", "        if False and st_ == 'undeclared':\n            return False")):
    CASES[f'mut_{_k}_full'] = (mut(HEAD_TOOL, _old, _new), HEAD_SUPP, HEAD_194, f'변이 {_k} · HEAD 문서 (S11g 상세 전체)')


def restore():
    git('checkout', 'HEAD', '--', *FILES)
    return git('status', '--porcelain', '--untracked-files=no').stdout.decode().strip() == ''


res = dict(_fp_now=FP, _twin=TWIN)
env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
try:
    for name, (tool, supp, b194, desc) in CASES.items():
        (WT / TOOL).write_text(tool, encoding='utf-8')
        (WT / SUPP).write_text(supp, encoding='utf-8')
        (WT / B194).write_text(b194, encoding='utf-8')
        for pyc in (WT / 'scripts/__pycache__').glob('supp20_input_receipt*.pyc'):
            pyc.unlink()
        t0 = time.time()
        r = subprocess.run(['nice', '-n', '19', sys.executable, '-I', '-B', TOOL, '--selftest'], cwd=WT, capture_output=True, text=True, env=env)
        lines = r.stdout.splitlines()
        fails = [ln.strip()[6:].split(' ')[0] for ln in lines if ln.startswith('  FAIL  ')]
        npass = sum(ln.startswith('  PASS  ') for ln in lines)
        key = {t: [h.strip()[:4] for h in lines if h.strip()[6:].startswith(t + ' ')] for t in ('S0', 'S0b', 'S11g')}
        res[name] = dict(desc=desc, rc=r.returncode, secs=round(time.time() - t0, 1), n_pass=npass, n_fail=len(fails), fails=fails, key=key,
                         state=[ln.strip() for ln in lines if '봉인 지문 상태 =' in ln], s0b_line=[ln[:400] for ln in lines if ln.strip()[6:].startswith('S0b ')],
                         fail_lines=[ln for ln in lines if ln.startswith('  FAIL  ')], last=[ln for ln in lines if 'supp20_input_receipt selftest:' in ln],
                         tool_sha256=hashlib.sha256(tool.encode('utf-8')).hexdigest())
        print(name, r.returncode, f'{npass}/{npass + len(fails)}', fails, key, flush=True)
        if not restore():
            res[name]['restore'] = 'DIRTY'
            break
finally:
    res['_final_clean'] = restore()
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print('final clean', res['_final_clean'], flush=True)
