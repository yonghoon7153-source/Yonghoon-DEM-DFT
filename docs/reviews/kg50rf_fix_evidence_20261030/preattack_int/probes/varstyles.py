#!/usr/bin/env python3
"""PAI probe — variable styles whose ${} value does not come from the deck text, on the D0.7 pair (-C).
Both decks get the same lines before the setup-segment gravity fix, and the gravity fix uses ${g}.
LIGGGHTS semantics (doc/variable.txt): index/loop/world/universe/uloop = a re-definition is IGNORED (first wins) ·
getenv = value from the job environment · file/atomfile = value from a file · format = formatted equal value.
usage: python3 varstyles.py <scratch with d07/>
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
TOOL = os.path.join(REPO, 'scripts/resume_ckpt.sh')
MAIN = os.path.join(REPO, 'docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts')
CK = 'restart_kg50_d07_b50/restart_settling_20001.bin'
G = 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n'
GV = 'fix gravi all gravity ${g} vector 0.0 0.0 -1.0\n'

CASES = [
    ('equal (control)', 'variable g equal 98.1\n', 'variable g equal 98.1\n', 0),
    ('getenv', 'variable g getenv KG50_G\n', 'variable g getenv KG50_G\n', 1),
    ('index first-wins (main 98.1 then 196.2 ignored · resume 196.2 only)',
     'variable g index 98.1\nvariable g index 196.2\n', 'variable g index 196.2\n', 1),
    ('index same', 'variable g index 98.1\n', 'variable g index 98.1\n', 1),
    ('string redefined (main 98.1 → 196.2 · resume 196.2)', 'variable g string 98.1\nvariable g string 196.2\n',
     'variable g string 196.2\n', 0),
    ('file', 'variable g file g.txt\n', 'variable g file g.txt\n', 1),
    ('format', 'variable gg equal 98.1\nvariable g format gg %.1f\n', 'variable gg equal 98.1\nvariable g format gg %.1f\n', 1),
    ('loop', 'variable g loop 98\n', 'variable g loop 98\n', 1),
    ('world', 'variable g world 98.1\n', 'variable g world 98.1\n', 1),
]


def main():
    sp = sys.argv[1]
    base = open(os.path.join(sp, 'd07', 'd07_tool_r56.liggghts'), encoding='utf-8').read()
    main_txt = open(MAIN, encoding='utf-8').read()
    assert main_txt.count(G) == 1 and base.count(G) == 1
    W = os.path.join(sp, 'w_vs')
    os.makedirs(W, exist_ok=True)
    open(os.path.join(W, 'g.txt'), 'w').write('98.1\n')
    print('| 꼴 | 본 덱 준비 줄 | 재개 덱 준비 줄 | -C rc | 판정 줄 | 기대 (거부=1) |\n|---|---|---|---|---|---|')
    for tag, mdef, rdef, want in CASES:
        mp, rp = os.path.join(sp, 'vs_main.liggghts'), os.path.join(sp, 'vs_res.liggghts')
        open(mp, 'w', encoding='utf-8').write(main_txt.replace(G, mdef + GV))
        open(rp, 'w', encoding='utf-8').write(base.replace(G, rdef + GV))
        p = subprocess.run(['bash', TOOL, '-C', mp, rp, CK, '20001', W], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out = p.stdout.decode('utf-8', 'replace')
        last = [l for l in out.splitlines() if '재개 덱 정적 대조:' in l]
        first = [l.strip()[:150] for l in out.splitlines() if l.strip().startswith('✗')][:1]
        print('| %s | `%s` | `%s` | %d | %s %s | %s |' % (tag, mdef.strip().replace('\n', ' ⏎ '), rdef.strip().replace('\n', ' ⏎ '),
                                                   p.returncode, (last or ['?'])[0].strip(), (first or [''])[0], want))


if __name__ == '__main__':
    main()
