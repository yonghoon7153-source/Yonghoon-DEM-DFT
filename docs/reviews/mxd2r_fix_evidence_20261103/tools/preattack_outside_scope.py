"""Pre-attack, part 2 — common-mode edits OUTSIDE the ratified MXD2R items (time · insertion · rotation ·
contact exclusion · material fixes · physical bytes).  Purpose: state honestly which other command edits the
fixed development consumers still accept, so the request can list them as 'not closed' (not fixed here —
1저자 11-02 비준 범위 밖).  Same harness as preattack_probe.py: both decks edited, metadata rebound, three APIs.

Usage: python3 -I preattack_outside_scope.py <repo>/scripts <out.json>
"""
import json
import re
import sys


def main(scripts, out):
    sys.path.insert(0, scripts)
    import test_mixer_d2_consumers as t

    def rep(old, new):
        return lambda s: s.replace(old, new, 1)
    cases = [
        ('boundary_periodic', rep('boundary        f f f', 'boundary        p p p'), 'global setting'),
        ('newton_on', rep('newton          off', 'newton          on'), 'global setting'),
        ('atom_style_sphere', rep('atom_style      granular', 'atom_style      sphere'), 'global setting'),
        ('communicate_cutoff', rep('communicate     single vel yes', 'communicate     single cutoff 0.001 vel yes'), 'global setting'),
        ('hard_particles_no', rep('hard_particles  yes', 'hard_particles  no'), 'global setting'),
        ('atom_modify_sort', rep('atom_modify     map array sort 0 0', 'atom_modify     map array sort 1000 0.0'), 'global setting'),
        ('thermo_lost_error', rep('thermo_modify lost ignore norm no', 'thermo_modify lost error norm no'), 'output/lost-atom policy'),
        ('neighbor_nsq', lambda s: re.sub(r'(?m)^(neighbor\s+\S+) bin$', r'\1 nsq', s), 'neighbor build style'),
        ('template_extra_option', lambda s: re.sub(r'(?m)^(fix pt1 [^\n]*radius constant \S+)$', r'\1 volume_limit 1e-30', s),
         'particletemplate/sphere trailing option'),
        ('template_quote_hash', lambda s: re.sub(r'(?m)^(fix pt1 [^\n]*radius constant \S+)$', r'\1 "#" volume_limit 1e-30', s),
         'particletemplate/sphere quoted # (unpinned line)'),
        ('pdd_seed', rep('particledistribution/discrete 32452867', 'particledistribution/discrete 15485863'), 'RNG seed (distribution)'),
        ('insert_b_seed', lambda s: re.sub(r'(fix insB all insert/pack seed )\d+', r'\g<1>15485867', s), 'RNG seed (2nd insertion)'),
        ('insert_region_geometry', lambda s: re.sub(r'(region ins_reg cylinder x 0\.0 0\.0 )(\S+)', r'\g<1>0.0100000', s), 'geometry (supplied input)'),
        ('mesh_scale', lambda s: s.replace('scale 0.0251665', 'scale 0.0250000'), 'geometry (supplied input)'),
        ('dump_modify_added', rep('\n# ① 채우고 정착', '\ndump_modify dmp sort id\n# ① 채우고 정착'), 'output only'),
        ('thermo_every', rep('thermo 5000', 'thermo 1000'), 'output only'),
        ('write_restart_removed', rep('write_restart restart/settled.bin\n', ''), 'checkpoint only'),
    ]
    a0, am0, _ = t.fixture()
    b0, bm0, _ = t.fixture(coated=True)
    rows = []
    for name, transform, kind in cases:
        a, b = transform(a0), transform(b0)
        assert a != a0 and b != b0, name
        ma, mb = t.rebound(a, am0), t.rebound(b, bm0)
        res = {'readback': t.rb.read_d2(a, ma), 'pair': t.dd.diff_d2_decks(a, b, ma, mb), 'plan': t.smoke.d2_plan_check(a, ma)}
        rows.append(dict(case=name, kind=kind, verdicts={k: v['verdict'] for k, v in res.items()},
                         first_failure=(res['readback']['failures'] or [''])[0][:200]))
        print(name.ljust(26), kind.ljust(40), rows[-1]['verdicts'])
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(dict(tool='preattack_outside_scope.py', python=sys.version.split()[0], rows=rows), f, ensure_ascii=False, indent=1)
        f.write('\n')


if __name__ == '__main__':
    main(*sys.argv[1:])
