"""Does the fixed working tree differ from the test-first snapshot inside the selftest functions? (scratch)
Prints, per file, the number of differing lines inside / outside `def _selftest` (or the test file itself)."""
import ast
import difflib
import sys

W = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a09115c89f930642a'
S = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/mxd2fix/snap_before'
FILES = ['scripts/make_mixer_deck.py', 'scripts/mixer_deck_readback.py', 'scripts/mixer_deck_diff.py', 'scripts/mixer_contact_reader.py',
         'scripts/mixer_smoke_blind.py', 'dem_scripts/mixer_20260921/test_launcher.sh', 'dem_scripts/mixer_20260921/run_all.sh',
         'dem_scripts/mixer_20260921/resume_all.sh']


def selftest_span(src):
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ('_selftest', 'selftest'):
            return node.lineno, node.end_lineno
    return None


for f in FILES:
    a = open(f'{S}/{f}', encoding='utf-8').read().split('\n')
    b = open(f'{W}/{f}', encoding='utf-8').read().split('\n')
    span_a = selftest_span('\n'.join(a)) if f.endswith('.py') else None
    span_b = selftest_span('\n'.join(b)) if f.endswith('.py') else None
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    inside, outside = 0, 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        for i in range(i1, i2):
            if span_a and span_a[0] <= i + 1 <= span_a[1]:
                inside += 1
            else:
                outside += 1
        for j in range(j1, j2):
            if span_b and span_b[0] <= j + 1 <= span_b[1]:
                inside += 1
            else:
                outside += 1
    print(f'{f:50s} snapshot→fixed changed lines: inside selftest {inside} · outside {outside} · spans {span_a} {span_b}')
    if inside and '--show' in sys.argv:
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'equal':
                continue
            if (span_a and any(span_a[0] <= i + 1 <= span_a[1] for i in range(i1, i2))) or (span_b and any(span_b[0] <= j + 1 <= span_b[1] for j in range(j1, j2))):
                print('   -', a[i1:i2][:4])
                print('   +', b[j1:j2][:4])
