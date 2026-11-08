"""고친 판 rint_r_chain.py 의 바꾼 함수 · 상수 줄 범위 (ast) · 머리말 ★ 11-09 사전 공격 14 줄 · 새 조건 줄.  쓰임: python3 fn_lines.py <rint_r_chain.py>"""
import ast
import sys

src = open(sys.argv[1], encoding='utf-8').read()
t = ast.parse(src)
want = {'arm_public_value_problem', 'arms_read_kind', 'read_run', 'resume_rerun_problem', 'resume_mismatch_problem', 'stop_record_problem', '_num', '_show'}
for n in t.body:
    if isinstance(n, ast.FunctionDef) and n.name in want:
        print(n.name, n.lineno, n.end_lineno)
    if isinstance(n, ast.Assign):
        for tg in n.targets:
            if isinstance(tg, ast.Name) and tg.id in ('ARM_STATES', 'ARM_PID_RE', 'ARM_SID_RE', 'RESUME_DETERMINISM', 'RESUME_COMPARED_KEYS', 'RESUME_KEYS'):
                print(tg.id, n.lineno, n.end_lineno)
    if isinstance(n, ast.ClassDef) and n.name == 'ResumeRunner':
        for m in n.body:
            if isinstance(m, ast.FunctionDef) and m.name == '__init__':
                print('ResumeRunner.__init__', m.lineno, m.end_lineno)
lines = src.splitlines()
for i, line in enumerate(lines, 1):
    if i <= 400 and '사전 공격 14' in line:
        print('header', i)
for pat in ('ARM_PID_RE.fullmatch(pid)', 'ARM_SID_RE.fullmatch(sid)', 'e > SVCF.CERT_TARGET_TOL', 'if not _num(r):', "{_show(v)} (= null",
            '_show(a.get("cg_info"))', 'set(R) != set(RESUME_KEYS)', "s['resume'] = getattr(rn, 'resume', None)"):
    print(repr(pat), [i for i, line in enumerate(lines, 1) if pat in line])
