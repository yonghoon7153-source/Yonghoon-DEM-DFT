"""Mutation check v3 — the MXD2R-01 · 02 · 03 mutants (M01–M19, imported unchanged from ../../tools/mutation_check.py) plus
the MXD2R-04 guards (M20–M47): does the regression fail for the right reason when ONE guard is neutralized?

<scripts> is a scratch copy of `scripts/` (git archive of the commit under test).  Each mutant = one exact, unique string
replacement in a scratch file; the copy's own scripts/test_mixer_d2_consumers.py is run; the file is restored.  'killed' =
the regression fails (rc != 0).  Two kinds of MXD2R-04 mutants:
  weaken  — the guard accepts what it should reject (a slot copied from the deck itself, a check turned off);
            must be killed by a counterexample test.
  tighten — the guard rejects generator output (a copied constant changed); must be killed by a positive test.

Usage: python3 -I mutation_check_v3.py <scratch scripts dir> <out.json> [mutant-id-prefix …]
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True                              # 증거 폴더에 __pycache__ 를 남기지 않는다
_spec = importlib.util.spec_from_file_location('mutation_check_v1', os.path.join(_HERE, '..', '..', 'tools', 'mutation_check.py'))
_v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v1)
R = _v1.R
DECK = "next(t for t in commands if t[:2] == {})"          # 'weaken' — expected tokens copied from the deck itself
NEW = [
    # ── _d2_text_form ──
    ('M20 weaken text: no final newline accepted', R, "_d2_need(text.endswith('\\n'), 'D2 generator form: deck must end",
     "_d2_need(True, 'D2 generator form: deck must end"),
    ('M21 weaken text: control characters accepted', R, "_d2_need(not controls,", "_d2_need(True,"),
    ('M22 weaken text: any command characters', R, "_d2_need(all(' ' <= c <= '~' and c not in '\"\\'$' for c in code),",
     "_d2_need(True,"),
    ('M23 weaken text: quotes and $ accepted (ASCII kept)', R, "' ' <= c <= '~' and c not in '\"\\'$' for c in code", "' ' <= c <= '~' for c in code"),
    ('M24 weaken text: continuation unchecked', R, "_d2_need(line.endswith(' &') and '#' not in line and line[:-2].strip() != '',",
     "_d2_need(True,"),
    ('M25 weaken text: continuation on comment lines accepted', R, "line.endswith(' &') and '#' not in line and", "line.endswith(' &') and"),
    ('M26 weaken text: continuation spelling free (comment rule kept)', R, "_d2_need(line.endswith(' &') and '#' not in line",
     "_d2_need('#' not in line"),
    ('M27 tighten text: no dump_modify exemption', R, "        if line == dump_line:\n            continue", "        if False:\n            continue"),
    ('M28 weaken text: metadata dump format unchecked', R, "_d2_need(fmt == D2_DUMP_FORMAT,", "_d2_need(True,"),
    # ── _d2_generator_form: comparison machinery ──
    ('M29 weaken form: no command comparison', R, "for index, (got, want) in enumerate(zip(commands, seq), 1):",
     "for index, (got, want) in enumerate(zip([], seq), 1):"),
    ('M30 weaken form: command count unchecked', R, "_d2_need(len(commands) == len(seq),", "_d2_need(True,"),
    ('M31 weaken form: skin token unchecked', R, "_d2_number(_d2_float_token(g, 'neighbor skin'), 'neighbor skin')", "pass"),
    ('M32 weaken form: seed prime / bound unchecked', R, "_d2_need(seed <= D2_SEED_MAX and _d2_next_prime(seed) == seed,", "_d2_need(True,"),
    ('M33 weaken form: steps k-multiple unchecked', R, "_d2_need(F % k == 0 and n_run % k == 0 and F // k >= 1000,", "_d2_need(True,"),
    ('M34 weaken form: dump interval from deck', R, "dump_every = k * max(1000, (n_run // k) // 200)", "dump_every = D['dump_every']"),
    ('M35 weaken form: restart interval from deck', R, "restart_every = max(50_000, min(200_000, (n_run or 2 * F) // 20))",
     "restart_every = D['restart_every']"),
    ('M36 weaken form: dt spelling from deck', R,
     "dt_tok = format(D['dt'], '.4g') if k == 1 else repr(float(format(D['dt'] * k, '.4g')) / k)", "dt_tok = D['dt_txt']"),
    # ── _d2_generator_form: pinned lines copied from the deck (weaken) ──
    ('M37 weaken form: global settings from deck', R, "seq = [list(t) for t in D2_GLOBAL_FORM]", "seq = [list(t) for t in commands[:7]]"),
    ('M38 weaken form: box region from deck', R,
     "seq += [['region', 'reg', 'block', neg(box), f6(box), neg(box), f6(box), neg(box), f6(box), 'units', 'box'],",
     "seq += [" + DECK.format("['region', 'reg']") + ","),
    ('M39 weaken form: youngsModulus tokens from deck', R,
     "+ [format(1e7 * stiff if p == 'SE' else REG_E_FIXED[p], '.4g') for p in order],",
     "+ " + DECK.format("['fix', 'm1']") + "[6:],"),
    ('M40 weaken form: CED spelling from deck', R, "+ [format(D['ced'][(i, j)], 'g') for i in range(1, N + 1) for j in range(1, N + 1)],",
     "+ " + DECK.format("['fix', 'mC']") + "[7:],"),
    ('M41 weaken form: mesh scale from deck', R, "'type', str(N), 'scale', scale] for mesh in D2_MESHES]",
     "'type', str(N), 'scale', " + DECK.format("['fix', mesh]") + "[9]] for mesh in D2_MESHES]"),
    ('M42 weaken form: template tail from deck', R, "'radius', 'constant', f6(d[p] / 2)]",
     "'radius', 'constant'] + " + DECK.format("['fix', f'pt{i}']") + "[12:]"),
    ('M43 weaken form: distribution entries from deck', R,
     "+ [x for p in group for x in (f'pt{phases.index(p) + 1}', format(mf[p] / share if layered else mf[p], '.6f'))])",
     "+ " + DECK.format("['fix', fid]") + "[6:])"),
    ('M44 weaken form: distribution seed from deck', R, "'particledistribution/discrete', str(dist_seed),",
     "'particledistribution/discrete', " + DECK.format("['fix', fid]") + "[4],"),
    ('M45 weaken form: insertion region from deck', R,
     "seq += [['region', 'ins_reg', 'cylinder', 'x', '0.0', '0.0', f6(R * 0.9), neg(L * 0.45), f6(L * 0.45), 'units', 'box'],",
     "seq += [" + DECK.format("['region', 'ins_reg']") + ","),
    ('M46 weaken form: second insertion seed from deck', R, "insert('insB', 'pddB', 'ins_hi', totals[1], _d2_next_prime(seed + 2))",
     "insert('insB', 'pddB', 'ins_hi', totals[1], " + DECK.format("['fix', 'insB']") + "[5])"),
    ('M47 weaken form: thermo interval from deck', R, "['thermo', '5000'],", DECK.format("['thermo', '5000']").replace(
        "t[:2] == ['thermo', '5000']", "t[0] == 'thermo'") + ","),
    ('M48 weaken form: rotation period from deck', R, "period = f6(meta['period_s'])", "period = " + DECK.format("['fix', 'mvD']") + "[16]"),
    ('M49 weaken form: upper insertion block from deck', R,
     "seq += [['region', 'ins_hi', 'block', neg(L * 0.45), f6(L * 0.45), neg(R * 0.6), f6(R * 0.6), f6(z_lo), f6(0.78 * R), 'units', 'box'],",
     "seq += [" + DECK.format("['region', 'ins_hi']") + ","),
    # ── tighten (copied constants changed — positive tests must catch) ──
    ('M50 tighten form: drum box factor 1.15 → 1.16', R, "box, scale = R * 1.15, f6(R / 0.5)", "box, scale = R * 1.16, f6(R / 0.5)"),
    ('M51 tighten form: drum fill 0.30 → 0.31', R, "D2_DRUM = dict(fill=0.30,", "D2_DRUM = dict(fill=0.31,"),
    ('M52 tighten form: pddB seed constant', R, "D2_DIST_SEED = (32452867, 32452883)", "D2_DIST_SEED = (32452867, 32452869)"),
    ('M53 tighten form: layered bed pack 0.60 → 0.61', R, "area = v_am / 0.60 / L", "area = v_am / 0.61 / L"),
    ('M54 tighten form: dump full-precision format', R, "D2_DUMP_FORMAT = '%d %d' + ' %.17g' * 10", "D2_DUMP_FORMAT = '%d %d' + ' %.16g' * 10"),
]
MUTANTS = list(_v1.MUTANTS) + NEW


def main(scripts, out, *prefixes):
    test = os.path.join(scripts, 'test_mixer_d2_consumers.py')
    rows = []
    for name, fname, old, new in MUTANTS:
        if prefixes and not any(name.startswith(p) for p in prefixes):
            continue
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
        print(('killed  ' if proc.returncode else 'SURVIVED') + ' ' + name.ljust(58) + ' ' + ', '.join(failing), flush=True)
    clean = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', test], capture_output=True)
    report = dict(tool='mutation_check_v3.py', python=sys.version.split()[0], selection=list(prefixes) or 'all', n=len(rows),
                  killed=sum(r['killed'] for r in rows), unmutated_rc=clean.returncode, rows=rows)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f"{report['killed']}/{report['n']} killed · unmutated rc {clean.returncode}")


if __name__ == '__main__':
    main(*sys.argv[1:])
