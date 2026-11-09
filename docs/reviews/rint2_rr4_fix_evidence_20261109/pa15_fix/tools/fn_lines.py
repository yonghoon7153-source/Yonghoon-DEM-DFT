"""고침 C (사전 공격 15 처분) — rint_r_chain.py 의 바꾼 · 새 함수 · 상수 · 클래스 줄 범위 (ast) · 새 가드 줄.  쓰임: python3 fn_lines.py <rint_r_chain.py>"""
import ast
import sys

src = open(sys.argv[1], encoding='utf-8').read()
t = ast.parse(src)
want = {'resume_rerun_problem', 'resume_recompare', 'run_dirs', 'resume_recompare_run', 'run_end_ok', 'resume_disk_rerun', '_src_run_done',
        'resume_boundary_problem', 'resume_first_new_problem', 'resume_provenance_problem', 'resume_chain_provenance_problem', 'summary_shape_problem',
        'result_fields_ledger', 'resume_prov_unconfirmed', 'attempt_result', 'attempt_close', 'attempt_entry_diff', 'found_attempts_problem',
        'recover_ledger', 'attempt_order_problem', 'resume_chain_problem'}
for n in t.body:
    if isinstance(n, ast.FunctionDef) and n.name in want:
        print(n.name, n.lineno, n.end_lineno)
    if isinstance(n, ast.Assign):
        for tg in n.targets:
            if isinstance(tg, ast.Name) and tg.id in ('RESUME_PROV', 'RUN_ORDER_RE', 'ATTEMPT_ENTRY_FIELDS'):
                print(tg.id, n.lineno, n.end_lineno)
    if isinstance(n, ast.ClassDef) and n.name in ('ResultHeld',):
        print(f'class {n.name}', n.lineno, n.end_lineno)
    if isinstance(n, ast.ClassDef) and n.name == 'ResumeRunner':
        for m in n.body:
            if isinstance(m, ast.FunctionDef) and m.name in ('_src_done', '_copy', 'run'):
                print(f'ResumeRunner.{m.name}', m.lineno, m.end_lineno)
lines = src.splitlines()
for pat in ('# ⓐ 지킴', '# ★ 11-09 사전 공격 15 PC15-05 — 꼴 지킴', '# ⓑ 지킴', '요약 없는 재실행 시도 = 원장의 그 시점 유효 사슬 끝', '# 원천 지킴', '# ⓒ 지킴',
            '# ⓓ 지킴', "if rerun is not None and R.get('rerun') != rerun:", 'if not seen_new and nm != rerun:', '— 새 런 기록 ↔ 이 시도 groups 시작 · 끝 기록',
            'if any(d != od for d in dirs):', 'if r is not last and not (run_end_ok(folder, nm) and od in dirs):', "last = runs[-1] if runs and runs[-1]",
            '런 이름 꼴 밖 시작 기록', "post = R is not None and", 'done = rerun is not None and run_end_ok', 'want = resume_recompare_run(src, folder, rerun)',
            'if resume_prov_unconfirmed(why):', 'except ResultHeld as e:', 'if not (type(a[f]) is type(e[f]) and a[f] == e[f])'):
    print(repr(pat), [i for i, line in enumerate(lines, 1) if pat in line])
