#!/usr/bin/env python3
"""Independent D2 command-lifecycle counterexamples; synthetic text only."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve(strict=True)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(repo / 'scripts'))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import make_mixer_deck as gen
    import mixer_deck_readback as rb
    import mixer_deck_diff as dd
    import mixer_smoke_blind as smoke
    import attack_consumers as helper

    def fixture(coated):
        old = gen.TYPES
        try:
            gen.set_phases(('AM_P', 'AM_S', 'SE'))
            gen.register_arm('INDEPENDENT_LIFECYCLE', gen.gm_arm(
                {'AM_P': 1. if coated else .25, 'AM_S': 1. if coated else .25, 'SE': 1.},
                gamma_wall=.0064, bo_se=1.125, layered=True, rho_uncoated_ncm=.25))
            plan = gen.plan(100003, cgf=125., stiffen_se=20., dens_gen='lab20261014')
            rpm = gen.resolve_rpm(plan['R'])
            text = gen.deck(plan, rpm, 2, seed=49979687, arm='INDEPENDENT_LIFECYCLE', hold_bo_pairwise=True)
            meta = gen.deck_meta(plan, rpm, 2, 49979687, 'INDEPENDENT_LIFECYCLE', text, hold_bo_pairwise=True)
            return text, meta
        finally:
            gen.ARMS.pop('INDEPENDENT_LIFECYCLE', None)
            gen.set_phases(old)

    a, am = fixture(False)
    b, bm = fixture(True)

    def unfix_before(rows):
        i = next(i for i, row in enumerate(rows) if row == ['unfix', 'insA'])
        command = rows.pop(i)
        j = next(i for i, row in enumerate(rows) if row[0] == 'run')
        rows.insert(j, command)

    def remove_integrator(rows):
        rows[:] = [row for row in rows if not (row[0] == 'fix' and row[3] == 'nve/sphere')]

    def remove_meshes(rows):
        rows[:] = [row for row in rows if not (row[0] == 'fix' and row[3] == 'mesh/surface')]

    def early_rotation(rows):
        moves = [row for row in rows if row[0] == 'fix' and row[3] == 'move/mesh']
        rows[:] = [row for row in rows if row not in moves]
        j = next(i for i, row in enumerate(rows) if row[0] == 'run')
        rows[j:j] = moves

    def missing_region(rows):
        command = next(row for row in rows if row[0] == 'fix' and row[3] == 'insert/pack')
        command[command.index('region') + 1] = 'no_such_region'

    cases = [
        ('positive', lambda _: None, 'PASS'),
        ('unfix_insA_before_first_run', unfix_before, 'FAIL'),
        ('remove_integrator', remove_integrator, 'FAIL'),
        ('remove_meshes', remove_meshes, 'FAIL'),
        ('rotation_before_fill', early_rotation, 'FAIL'),
        ('missing_insert_region', missing_region, 'FAIL'),
    ]
    results = []
    for name, mutate, expected in cases:
        ac, bc = helper.logical(a), helper.logical(b)
        mutate(ac)
        mutate(bc)
        aa, bb = helper.render(ac), helper.render(bc)
        aam, bbm = helper.rebound(aa, am), helper.rebound(bb, bm)
        calls = {'readback': rb.read_d2(aa, aam), 'pair': dd.diff_d2_decks(aa, bb, aam, bbm),
                 'plan': smoke.d2_plan_check(aa, aam)}
        result = {'name': name, 'expected': expected, 'calls': calls,
                  'expectations_met': all(call['verdict'] == expected for call in calls.values())}
        results.append(result)
        folder = out / name
        folder.mkdir()
        for label, text, meta in [('reference', aa, aam), ('new', bb, bbm)]:
            (folder / (label + '.in')).write_text(text)
            (folder / (label + '_meta.json')).write_text(json.dumps(meta, indent=2) + '\n')
    summary = {'source_hashes': {name: hashlib.sha256((repo / 'scripts' / name).read_bytes()).hexdigest()
                               for name in ('make_mixer_deck.py', 'mixer_deck_readback.py', 'mixer_deck_diff.py', 'mixer_smoke_blind.py')},
               'results': results, 'failed_cases': [r['name'] for r in results if not r['expectations_met']],
               'scope': 'text-only planned-deck contract; no simulator, physical result, registration or execution authority'}
    (out / 'results.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps({'source_hashes': summary['source_hashes'], 'failed_cases': summary['failed_cases'],
                      'cases': len(results), 'calls': 3 * len(results)}, indent=2))
    return int(bool(summary['failed_cases']))


if __name__ == '__main__':
    raise SystemExit(main())
