"""고친 판 rint_r_chain.py 의 바꾼 · 새 함수 · 상수 줄 범위 (ast) · 머리말 ★ 11-09 Codex 회차 ④ 줄 · 지킴 · 부르는 자리 줄.  쓰임: python3 fn_lines.py <rint_r_chain.py>"""
import ast
import sys

src = open(sys.argv[1], encoding='utf-8').read()
t = ast.parse(src)
want = {'attempt_order_problem', 'resume_chain_problem', 'resume_rerun_problem', 'resume_recompare', 'resume_from_problem', 'resume_source_locate',
        '_src_run_done', 'resume_boundary_problem', 'resume_first_new_problem', 'resume_provenance_problem', 'resume_chain_provenance_problem',
        'result_fields', 'result_fields_ledger', '_result_line', 'attempt_result_line', 'attempt_result', '_result_recount', 'result_recount',
        'result_line_problem', 'attempt_close', 'attempt_entry_diff', 'found_attempts_problem', 'ledger_inputs_check', 'target_ledger_problem',
        'recover_ledger'}
for n in t.body:
    if isinstance(n, ast.FunctionDef) and n.name in want:
        print(n.name, n.lineno, n.end_lineno)
    if isinstance(n, ast.Assign):
        for tg in n.targets:
            if isinstance(tg, ast.Name) and tg.id in ('RESUME_PROV', 'ATTEMPT_ENTRY_FIELDS'):
                print(tg.id, n.lineno, n.end_lineno)
    if isinstance(n, ast.ClassDef) and n.name == 'ResumeRunner':
        for m in n.body:
            if isinstance(m, ast.FunctionDef) and m.name in ('_src_done', '_copy', 'run'):
                print(f'ResumeRunner.{m.name}', m.lineno, m.end_lineno)
lines = src.splitlines()
print('header', [i for i, line in enumerate(lines, 1) if i <= 400 and 'Codex 회차 ④' in line])
for pat in ('# ⓐ 지킴', '# ⓑ 지킴', '# 원천 지킴', '# ⓒ 지킴', '# ⓓ 지킴', 'if not src.is_dir():', 'resume_chain_provenance_problem(st, ad[',
            "if r['resume_ok'] is True and cand[0].is_dir():", 'result_line_problem(k, cand[0], r, st=st, found=found)',
            'attempt_result(att.n, att.folder', "attempt_result(n, f, s, 'recover', st", 'result_line_problem(n, d, r, st=st, found=found)',
            'result_line_problem(k, p, r, st=st, found=found)', 'd = attempt_entry_diff(a, k, e)'):
    print(repr(pat), [i for i, line in enumerate(lines, 1) if pat in line])
