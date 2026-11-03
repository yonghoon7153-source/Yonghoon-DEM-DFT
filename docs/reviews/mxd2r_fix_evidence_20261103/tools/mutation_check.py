"""Mutation check for the MXD2R-01 · 02 · 03 guards (CLAUDE.md pre-attack ③ — do the new tests fail for the right reason?).

<scripts> is a scratch copy of the fixed `scripts/` (git archive of the fix commit).  Each mutant neutralizes ONE
guard by an exact, unique string replacement; the copy's own scripts/test_mixer_d2_consumers.py is run; the file is
restored.  A mutant is 'killed' when the regression fails (rc != 0).  A surviving mutant = a guard the tests do not
pin down.

Usage: python3 -I mutation_check.py <scratch scripts dir> <out.json>
"""
import json
import os
import re
import subprocess
import sys

R, D, S = 'mixer_deck_readback.py', 'mixer_deck_diff.py', 'mixer_smoke_blind.py'
MUTANTS = [
    ('M01 run: options allowed', R, "_d2_need(len(t) == 2 and re.fullmatch(D2_RUN_COUNT, t[1]) is not None,",
     "_d2_need(True or len(t) == 2,"),
    ('M02 timestep: after first run allowed', R, "and len(commands[steps[0]]) == 2 and steps[0] < runs[0],",
     "and len(commands[steps[0]]) == 2,"),
    ('M03 timestep: extra token allowed', R, "and len(commands[steps[0]]) == 2 and steps[0] < runs[0],",
     "and steps[0] < runs[0],"),
    ('M04 insert/pack: any form', R,
     "if not (len(t)==len(D2_INSERT_FORM) and all(w is None or t[k]==w for k,w in enumerate(D2_INSERT_FORM))):", "if False:"),
    ('M05 rotation: Front/Back period free', R, "all(p==periods['Drum'] for p in periods.values())", "True"),
    ('M06 neigh_modify: any arguments', R, "neigh[0][1] == D2_NEIGH_MODIFY and ", ""),
    ('M07 neigh_modify: extra commands', R, "_d2_need(len(neigh) == 1 and", "_d2_need(len(neigh) >= 1 and"),
    ('M08 pair_style: after first run allowed', R, "box < pair[0] < coeff[0][0] < first,", "box < pair[0] < coeff[0][0],"),
    ('M09 pair_coeff: any arguments', R, "coeff[0][1] == D2_PAIR_COEFF and ", ""),
    ('M10 material: missing allowed', R, "_d2_need(not missing,", "_d2_need(True,"),
    ('M11 material: duplicate allowed', R, "_d2_need(name not in found,", "_d2_need(True,"),
    ('M12 material: constants unchecked', R, "        if constant is not None:\n", "        if False:\n"),
    ('M13 material: order unchecked', R, "box < i < pair[0] and all(i < w for w in walls),", "True,"),
    ('M14 material: unknown name skipped', R,
     "        _d2_need(name in D2_MATERIAL, f'D2 contact contract: unsupported material property",
     "        if name not in D2_MATERIAL:\n            continue\n        _d2_need(True, f'D2 contact contract: unsupported material property"),
    ('M15 bytes: CR accepted', R, "_d2_need(n_cr == 0,", "_d2_need(True,"),
    ('M16 bytes: hash of normalized text', R, "raw = deck if type(deck) is bytes else deck.encode('utf-8')",
     "raw = (deck.decode('utf-8') if type(deck) is bytes else deck).replace('\\r\\n', '\\n').encode('utf-8')"),
    ('M17 readback CLI: text-mode read', R, "with open(a.d2[0], 'rb') as stream:", "with open(a.d2[0], encoding='utf-8') as stream:"),
    ('M18 diff CLI: text-mode read', D, "old, new = (_read_bytes(path) for path in a.decks)", "old, new = (_read(path) for path in a.decks)"),
    ('M19 smoke CLI: text-mode read', S, "raw = Path(a.d2_plan).read_bytes()", "raw = Path(a.d2_plan).read_text(encoding='utf-8')"),
]


def main(scripts, out):
    test = os.path.join(scripts, 'test_mixer_d2_consumers.py')
    rows = []
    for name, fname, old, new in MUTANTS:
        path = os.path.join(scripts, fname)
        with open(path, encoding='utf-8') as f:
            original = f.read()
        assert original.count(old) == 1, (name, original.count(old))
        with open(path, 'w', encoding='utf-8') as f:
            f.write(original.replace(old, new))
        try:
            proc = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', test], capture_output=True)
        finally:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(original)
        text = (proc.stdout + proc.stderr).decode('utf-8', 'replace')
        failing = sorted({m.group(2) for m in re.finditer(r'^(FAIL|ERROR): (test_\w+)', text, re.M)})
        tail = re.search(r'^(OK|FAILED \([^)]*\))\s*$', text, re.M)
        rows.append(dict(mutant=name, file=fname, killed=proc.returncode != 0, result=tail.group(1) if tail else None,
                         failing_tests=failing))
        print(('killed  ' if proc.returncode else 'SURVIVED') + ' ' + name.ljust(42) + ' ' + ', '.join(failing))
    clean = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', test], capture_output=True)
    report = dict(tool='mutation_check.py', python=sys.version.split()[0], n=len(rows), killed=sum(r['killed'] for r in rows),
                  unmutated_rc=clean.returncode, rows=rows)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f"{report['killed']}/{report['n']} killed · unmutated rc {clean.returncode}")


if __name__ == '__main__':
    main(*sys.argv[1:])
