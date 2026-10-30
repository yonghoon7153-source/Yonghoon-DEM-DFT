#!/usr/bin/env python3
"""PAI probe — Codex 10-30 recheck program cases (received ZIP at e46bda9ec · independent/program/cases · 43) through the
current tool's -C.  Reads the extracted folder as data only (paths passed as arguments · no code from it is run).
For each case: Codex's 'expected', Codex's observed static_rc on 77c24237, and our rc on 2dc7f693 (work folder = a scratch copy
of the case folder, like Codex used the case folder).
usage: python3 codex_cases.py <extracted root containing independent/program> <scratch>
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../..'))
TOOL = os.path.join(REPO, 'scripts/resume_ckpt.sh')


def main():
    root, sp = sys.argv[1], sys.argv[2]
    prog = os.path.join(root, 'independent', 'program')
    res = json.load(open(os.path.join(prog, 'results.json'), encoding='utf-8'))
    print('| 사례 | Codex 기대 | Codex rc (77c24237) | 우리 rc (2dc7f693) | 판정 줄 | 첫 문제 |\n|---|---|---|---|---|---|')
    tally = {}
    for c in res['cases']:
        name = c['name']
        cmd = c.get('command') or []
        if len(cmd) < 5:
            print('| %s | %s | - | (명령 없음) | | |' % (name, c.get('expected')))
            continue
        ck, s0 = cmd[-3], cmd[-2]
        cd = os.path.join(prog, 'cases', name)
        if not os.path.isdir(cd):
            print('| %s | %s | %s | (폴더 없음) | | |' % (name, c.get('expected'), c.get('static_rc')))
            continue
        W = os.path.join(sp, 'cx_w', name)
        shutil.rmtree(W, ignore_errors=True)
        shutil.copytree(cd, W)
        p = subprocess.run(['bash', TOOL, '-C', os.path.join(W, 'main.liggghts'), os.path.join(W, 'resume.liggghts'), ck, s0, W],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
        out = p.stdout.decode('utf-8', 'replace')
        last = [l.strip() for l in out.splitlines() if '재개 덱 정적 대조:' in l]
        first = [l.strip()[:110] for l in out.splitlines() if l.strip().startswith('✗')][:1]
        exp = c.get('expected')
        ok = (exp == 'accept') == (p.returncode == 0) if exp in ('accept', 'reject') else None
        tally[(exp, p.returncode == 0)] = tally.get((exp, p.returncode == 0), 0) + 1
        print('| %s | %s | %s | %d%s | %s | %s |' % (name, exp, c.get('static_rc'), p.returncode,
                                                   '' if ok is None else (' ✓' if ok else ' ✗'), (last or ['?'])[0], (first or [''])[0]))
    print('\n기대 · 우리 통과 여부별 수:', {('%s·%s' % (k[0], 'rc0' if k[1] else 'rc1')): v for k, v in sorted(tally.items(), key=str)})


if __name__ == '__main__':
    main()
