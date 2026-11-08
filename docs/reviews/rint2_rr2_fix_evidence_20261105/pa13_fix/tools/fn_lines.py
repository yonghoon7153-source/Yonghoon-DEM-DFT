"""고친 판 rint_r_chain.py 의 바꾼 함수 · 상수 줄 범위 (ast) · 머리말 ★ 11-09 줄."""
import ast
import sys

src = open(sys.argv[1], encoding='utf-8').read()
t = ast.parse(src)
want = {'arm_file_prefix', 'arm_public_value_problem', 'arms_read_kind', 'read_run', 'stop_record_problem', 'resume_mismatch_problem',
        'resume_rerun_problem', 'prior_runs_problem'}
for n in t.body:
    if isinstance(n, ast.FunctionDef) and n.name in want:
        print(n.name, n.lineno, n.end_lineno)
    if isinstance(n, ast.Assign):
        for tg in n.targets:
            if isinstance(tg, ast.Name) and tg.id in ('ARM_STATES', 'RESUME_DETERMINISM', 'RESUME_COMPARED_KEYS'):
                print(tg.id, n.lineno, n.end_lineno)
    if isinstance(n, ast.ClassDef) and n.name == 'RunnerGraphSource':
        for m in n.body:
            if isinstance(m, ast.FunctionDef) and m.name == '_run':
                print('RunnerGraphSource._run', m.lineno, m.end_lineno)
for i, line in enumerate(src.splitlines()[:400], 1):
    if '11-09' in line:
        print('header', i)
