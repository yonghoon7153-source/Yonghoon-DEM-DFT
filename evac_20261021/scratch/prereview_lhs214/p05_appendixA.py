#!/usr/bin/env python3
"""P05 — 요청서 부록 A 의 명령을 그대로 (git 은 subprocess · 파이썬 블록은 같은 식) — HEAD 작업 트리에서.
재실행: cd <worktree> && python3 -I p05_appendixA.py <worktree>"""
import hashlib, json, subprocess, sys
WT = sys.argv[1]
sys.path.insert(0, f'{WT}/scripts')
import run_network_194_parallel as N          # noqa: E402
import supp20_input_receipt as S              # noqa: E402

C = 'fe23f2b839f0a49adb077348fec6d4c85443b62a'
R = 'f82929b0644be39b44e9fba9ea04cf9d60de9146'


def git(*a):
    r = subprocess.run(['git', *a], cwd=WT, capture_output=True)
    return r.returncode, r.stdout


out = {}
FILES = list(N.CODE_FILES)
out['n_code_files'] = len(FILES)
for tag, rev in (('R', R), ('HEAD', 'HEAD')):
    out[f'sealed32_rc_{tag}'] = git('diff', '--quiet', '34713ac96', rev, '--', *FILES)[0]
    out[f'tools_rc_{tag}'] = git('diff', '--quiet', '34713ac96', rev, '--', 'scripts/lhs_design_dataset.py', 'scripts/g2_network_reread.py',
                                 'scripts/lhs_release_build.py', 'scripts/run_network_194_parallel.py', 'scripts/wsl_network_smoke.py')[0]
out['C_changed'] = git('diff', '--name-only', f'{C}^', C)[1].decode().split()
out['R_changed'] = git('diff', '--name-only', f'{R}^', R)[1].decode().split()
out['C_parent'] = git('rev-parse', f'{C}^')[1].decode().strip()
out['R_parent'] = git('rev-parse', f'{R}^')[1].decode().strip()
for d in ('docs/reviews/lhs_network_batch_registration_20261007_g2.md', 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md'):
    out[f'sha256 {d.split("_")[-1]}'] = {rev: hashlib.sha256(git('show', f'{rev}:{d}')[1]).hexdigest() for rev in (R, '34713ac96', 'HEAD')}
out['tool_sha256'] = {rev: hashlib.sha256(git('show', f'{rev}:scripts/supp20_input_receipt.py')[1]).hexdigest() for rev in (C, 'a76f59d0d', 'HEAD')}
# 기준 머리 ↔ 메인 부모 사이 넷
out['a76f_vs_a699_four_rc'] = git('diff', '--quiet', 'a76f59d0d', 'a6996396774064fa159d360da0e1d26877b66c33', '--', 'scripts/supp20_input_receipt.py',
                                  'docs/reviews/lhs_network_batch_registration_20261007_g2.md', 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md',
                                  'scripts/run_network_194_parallel.py')[0]
# 파이썬 블록 (요청서 그대로)
out['code_fp'] = N.code_fp(N.code_hashes())
v, p = S.registration_values()
out['supp'] = [v['code_fp'], v['code_fp_pending'], p]
v1, p1 = S.registration_values(reg_doc='docs/reviews/lhs_network_batch_registration_20261007_g2.md')
out['194'] = [v1['code_fp'], v1['code_fp_pending'], [x for x in p1 if x.startswith('등록 문서 code_fp')]]
out['194_all_problems'] = p1
r = S.receipt()
out['receipt'] = [r['rc'], sorted(c['id'] for c in r['checks'] if not c['ok']), len(r['checks']), [c['id'] for c in r['checks']]]
out['receipt_recorded_git'] = r['recorded']['git']
print(json.dumps(out, ensure_ascii=False, indent=1))
