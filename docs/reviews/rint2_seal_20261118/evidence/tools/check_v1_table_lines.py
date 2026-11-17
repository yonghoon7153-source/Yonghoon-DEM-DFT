#!/usr/bin/env python3
"""v1 README (가) 표가 적은 줄 번호를 핀 판 파일에서 다시 대조 — 그 줄 (또는 적은 범위) 에 기대 글자가 있나.
argv: <scripts 가 핀 판인 트리> <git 사본 (핀 판 문서를 git show 로 읽는다)> <핀 rev>"""
import sys, os, subprocess
T, G, PIN = sys.argv[1:4]
CH, REG = 'scripts/rint_r_chain.py', 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'
FIX = 'docs/reviews/rint2_rereview_fix_plan_20261022.md'
rows = [(CH, 301, 301, 'PLAN_SCHEMA'), (CH, 302, 302, 'PLAN_KEYS'), (CH, 311, 312, 'EXEC_POLICY_RULES'), (CH, 320, 320, "'none'"),
        (CH, 321, 321, 'R_j0'), (CH, 322, 322, 'PLAN_UNREG_MAIN'), (CH, 1214, 1214, 'EXEC_POLICY_RULES'), (CH, 1215, 1217, 'max_hours'),
        (CH, 1218, 1220, 'max_attempts'), (CH, 1221, 1224, 'allowed_machines'), (CH, 1225, 1228, 'env_unit'), (CH, 1238, 1239, 'PLAN_SCHEMA'),
        (CH, 1240, 1241, 'len_law'), (CH, 1242, 1243, 'unreg_law'), (CH, 1244, 1247, 's_min_um'), (CH, 1248, 1249, 'p2_extra'),
        (CH, 1250, 1252, 'max_ladder_points'), (CH, 1253, 1255, 'calib_rj_ratio_max'), (CH, 1256, 1258, 'sv_cf_threshold'),
        (CH, 1259, 1260, 'sv_cf_scope'), (CH, 1265, 1265, 'def load_plan'), (CH, 1287, 1287, 'def require_plan_numbers'),
        (CH, 1303, 1303, 'max_hours'), (CH, 1306, 1306, 'allowed_machines'), (CH, 1308, 1308, 'env_seal_problem'),
        (CH, 1313, 1313, 'def env_seal_problem'), (CH, 1339, 1339, 'def plan_doc_problem'), (CH, 1367, 1367, 'def stage_machine_problem'),
        (CH, 1386, 1386, 'def ladder_cap'), (CH, 1391, 1391, 'def plan_env'), (CH, 1395, 1395, 'P2_EXTRA'),
        (CH, 1399, 1399, 'def check_plan_registered'), (CH, 1419, 1419, 'tol_ff'), (CH, 1425, 1425, 'step3_rtol'), (CH, 1426, 1427, 'len_law'),
        (CH, 1428, 1429, 'unreg_law'), (CH, 1145, 1145, 'def registration_row_hash'), (CH, 1167, 1167, 'def registration_s0_hash'),
        (CH, 3562, 3562, 'def attempt_limit_problem'), (CH, 6657, 6657, 'plan_doc_or_stop'), (CH, 6683, 6683, 'max_hours'), (CH, 6881, 6881, 'plan_doc_or_stop'),
        (CH, 6887, 6887, 'sv_cf'), (CH, 6895, 6895, 'max_hours'), (CH, 7348, 7348, 'plan_doc_or_stop'), (CH, 7356, 7356, 'sv_cf'),
        (CH, 7392, 7392, 'max_hours'), ('scripts/carbon_junction.py', 90, 90, 'CJUNC_LEN_LAW'), ('scripts/step3_conv_cert.py', 66, 66, 'CERT_RTOL_MAX'),
        ('scripts/run_contract.py', 1597, 1597, 'ENV_UNIT_KEYS'), (REG, 80, 80, '| 계획 해시 |'), (REG, 81, 81, '| S0 계획 해시 |'),
        (REG, 83, 83, '계획 숫자 블록 = 이 줄 바로 아래'), (REG, 86, 86, 'unreg'), (REG, 108, 108, '§2-1b'), (REG, 127, 127, '점 수 상한 12'),
        (REG, 135, 135, '폭 상한'), (REG, 216, 216, '비 문턱'), (REG, 336, 336, '--step3-rtol'), (REG, 573, 573, 'Q5'), (REG, 584, 584, 'all3'),
        (REG, 589, 589, 'v100'), (REG, 634, 634, '세 R'), (FIX, 55, 56, 'all3'), (FIX, 96, 96, 'Q1–Q8')]
ok = 0
for f, a, b, tok in rows:
    if f.startswith('docs/'):
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        L = subprocess.run(['git', '-C', G, 'show', f'{PIN}:{f}'], capture_output=True, env=env).stdout.decode('utf-8').split('\n')
    else:
        L = open(os.path.join(T, f), encoding='utf-8').read().split('\n')
    hit = any(tok in L[i - 1] for i in range(a, b + 1))
    ok += hit
    if not hit:
        print(f'MISS {f}:{a}-{b} ~ {tok!r} :: {L[a - 1][:110]!r}')
print(f'v1 (가) 표 줄 번호 대조: {ok}/{len(rows)} 맞음')
sys.exit(0 if ok == len(rows) else 1)
