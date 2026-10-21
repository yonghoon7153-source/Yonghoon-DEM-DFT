"""HEAD blob vs test-first snapshot — changed lines inside / outside the selftest function (scratch).  usage: python3 head_vs_snap.py"""
import ast
import difflib
import subprocess

W = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a09115c89f930642a'
S = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/mxd2fix/snap_before'
FILES = ['scripts/make_mixer_deck.py', 'scripts/mixer_deck_readback.py', 'scripts/mixer_deck_diff.py', 'scripts/mixer_contact_reader.py',
         'scripts/mixer_smoke_blind.py', 'dem_scripts/mixer_20260921/test_launcher.sh', 'dem_scripts/mixer_20260921/run_all.sh',
         'dem_scripts/mixer_20260921/resume_all.sh', 'docs/mixer_devlog/v16_20261014.md']


def span(src):
    try:
        t = ast.parse(src)
    except SyntaxError:
        return None
    for n in t.body:
        if isinstance(n, ast.FunctionDef) and n.name == '_selftest':
            return n.lineno, n.end_lineno
    return None


for f in FILES:
    head = subprocess.run(['git', '-C', W, 'show', f'055ddd04e:{f}'], capture_output=True, text=True).stdout.split('\n')
    try:
        snap = open(f'{S}/{f}', encoding='utf-8').read().split('\n')
    except FileNotFoundError:
        print(f'{f:50s} (not in snapshot)')
        continue
    sa, sb = (span('\n'.join(x)) if f.endswith('.py') else None for x in (head, snap))
    sm = difflib.SequenceMatcher(a=head, b=snap, autojunk=False)
    ins = out = 0
    out_examples = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        for i in range(i1, i2):
            if sa and sa[0] <= i + 1 <= sa[1]:
                ins += 1
            else:
                out += 1
                out_examples.append('-' + head[i][:100])
        for j in range(j1, j2):
            if sb and sb[0] <= j + 1 <= sb[1]:
                ins += 1
            else:
                out += 1
                out_examples.append('+' + snap[j][:100])
    print(f'{f:50s} HEAD→snapshot changed lines: inside selftest {ins} · outside {out}')
    for e in out_examples[:6]:
        print('     ', e)
