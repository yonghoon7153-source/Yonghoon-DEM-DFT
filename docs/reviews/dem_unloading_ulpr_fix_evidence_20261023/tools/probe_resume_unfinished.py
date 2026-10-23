#!/usr/bin/env python3
"""ULPR-01 independent before/after synthetic reproduction; no simulator or network.
python probe_resume_unfinished.py --kit PATH --baseline OLD_UL_READER.py --out DIR
The kit is only read. All synthetic observations are created under TemporaryDirectory.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import types

FIELDS = ('primary_status', 'rho_pct', 'lower_bound_pct', 'trajectory_status', 'n_superseded_rows', 'problems', 'why', 'resume_tail', 'bracket_um', 'union_bracket_um', 'nonmonotone', 'separation', 's4_status', 'surface_um', 'eps', 'w_proxy_J')

def load_reader(source, kit, name):
    mod = types.ModuleType(name)
    mod.__file__ = str(kit / 'ul_reader.py')
    exec(compile(source, mod.__file__, 'exec'), mod.__dict__)
    return mod

def save_csv(d, out):
    out.mkdir(parents=True, exist_ok=True)
    for n in ('ul_windows.csv', 'ul_steps.csv', 'ul_events.csv', 'run_manifest.txt', 'ul_summary.txt'):
        p = d / n
        if p.exists():
            (out / n).write_bytes(p.read_bytes())
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kit', type=Path, required=True)
    ap.add_argument('--baseline', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    kit, out = a.kit.resolve(), a.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(kit))
    sources = {'before': a.baseline.read_text(), 'after': (kit / 'ul_reader.py').read_text()}
    modules = {n: load_reader(s, kit, 'ulpr_' + n) for n, s in sources.items()}
    m = modules['after']
    P = m.ul_lib.load_params()
    results = {}
    for name, opts in (
        ('confirmation_timeout', {'nw': 2}),
        ('confirmation_guard', {'nw': 2, 'stop': 'GUARD'}),
        ('confirmation_moving_timeout', {'nw': 0}),
        ('confirmation_guard_same_window_count', {'nw': 4, 'stop': 'GUARD'}),
        ('precross_lower_bound', {'kr': 2, 'precross': True}),
        ('precross_ambiguous_no_new_window', {'kr': 2, 'precross': True, 'nw': 0}),
        ('precross_ambiguous_same_count', {'kr': 2, 'precross': True, 'nw': 4, 'stop': 'GUARD'}),
        ('prior_measurement_preserved', {'kr': 4, 'job': 'UB'}),
        ('prior_measurement_ambiguous_tail', {'kr': 4, 'nw': 0, 'job': 'UB'}),
    ):
        results[name] = {}
        for resumed in (False, True):
            label = 'resumed' if resumed else 'fresh'
            with tempfile.TemporaryDirectory() as td:
                m._fake_restored(td, m.B73)
                m._w(str(Path(td) / m.B73 / 'ul_base.in'), 'variable ul_S2max equal 1e-05\n')
                m._mk_arm(td, m.B73, 'UB', {'W': 5000, 'dt': 1e-6,
                    'steps': m._ladder([0.2, 0.25, 0.3, 0.35], [1.2, 0.8, 0.6, 0.4]),
                    'summary': 'DONE', 'events': [('CROSS', 2, 'first'), ('RM', 4, 'ncross2')]}, P)
                d = Path(m._unfinished_resume(td, P, resumed=resumed, **opts))
                rec = {'sha256': save_csv(d, out / name / label), 'verdicts': {}}
                for impl, r in modules.items():
                    v = r.arm_verdict(str(d), r.B73, opts.get('job', 'UT'), P, root=td)
                    rec['verdicts'][impl] = {k: v.get(k) for k in FIELDS}
                    rec['verdicts'][impl]['UVa_allowed'] = r.gate(td, r.B73, 'UVa', P)[0]
                results[name][label] = rec
    # R10: execute the actual before/after fixture setup AST, retaining the original assertion and physical observations.
    r10 = {}
    for name, src in sources.items():
        fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == 'selftest')
        block = next(n for n in fn.body if isinstance(n, ast.With) and 'R10 이어 돌림' in ast.get_source_segment(src, n))
        end = next(i for i, n in enumerate(block.body) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                   and isinstance(n.value.func, ast.Name) and n.value.func.id == 'chk')
        with tempfile.TemporaryDirectory() as td:
            ns = dict(m.__dict__, root=td, P=P)
            exec(compile(ast.Module(body=block.body[:end], type_ignores=[]), '<R10 fixture>', 'exec'), ns)
            d = Path(ns['d'])
            r10[name] = {'sha256': save_csv(d, out / 'r10' / name), 'verdicts': {}}
            for impl, r in modules.items():
                v = r.arm_verdict(str(d), r.B73, 'UB', P, root=td)
                r10[name]['verdicts'][impl] = {k: v.get(k) for k in FIELDS}
    result = {'source_sha256': {n: hashlib.sha256(s.encode()).hexdigest() for n, s in sources.items()},
              'python': sys.version, 'cases': results, 'r10': r10}
    (out / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for name, row in results.items():
        b, c = row['resumed']['verdicts']['before'], row['resumed']['verdicts']['after']
        print(name, b['primary_status'], b['rho_pct'], b['lower_bound_pct'], '->', c['primary_status'], c['rho_pct'], c['lower_bound_pct'])
    assert all(results[n]['resumed']['verdicts']['before']['primary_status'] == 'OK' and
               results[n]['resumed']['verdicts']['after']['primary_status'] == 'UNIDENTIFIED'
               for n in ('confirmation_timeout', 'confirmation_guard', 'confirmation_moving_timeout', 'confirmation_guard_same_window_count'))
    assert results['precross_lower_bound']['fresh']['verdicts']['after']['lower_bound_pct'] == results['precross_lower_bound']['resumed']['verdicts']['after']['lower_bound_pct']
    assert results['prior_measurement_preserved']['resumed']['verdicts']['after']['primary_status'] == 'OK'
    assert results['prior_measurement_ambiguous_tail']['resumed']['verdicts']['after']['primary_status'] == 'OK'
    assert results['prior_measurement_ambiguous_tail']['resumed']['verdicts']['after']['union_bracket_um'] is None
    assert r10['before']['sha256']['ul_windows.csv'] == r10['after']['sha256']['ul_windows.csv']
    assert r10['before']['sha256']['ul_steps.csv'] == r10['after']['sha256']['ul_steps.csv']
    assert r10['after']['verdicts']['before']['rho_pct'] == r10['after']['verdicts']['after']['rho_pct']
    print('PASS: four false approvals reproduced; lower bound corrected; prior measured value and corrected R10 preserved.')

if __name__ == '__main__':
    main()
