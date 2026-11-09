"""Inactive producer tests. No engine, scheduler, research data, or network."""
import copy
import json
import math
from pathlib import Path
import unittest
import types

source_path = Path(__file__).with_name('make_dem_gen2_decks.py')
d = types.ModuleType('g2d')
d.__file__ = str(source_path)
exec(compile(source_path.read_bytes(), str(source_path), 'exec'), d.__dict__)


class Producer(unittest.TestCase):
    def test_seven_stages_and_hold(self):
        files = d.bundle(d.synthetic_config())
        self.assertEqual(len([k for k in files if k.startswith('stages/')]), 7)
        self.assertTrue(files['main.in'].startswith('# INACTIVE'))
        self.assertIn('quit 1', files['main.in'].split('include')[0])
        self.assertEqual(sum('fix top_mesh all ' in v for k, v in files.items() if k.startswith('stages/')), 1)
        self.assertEqual(sum('fix zwall_top all ' in v for k, v in files.items() if k.startswith('stages/')), 1)
        self.assertNotIn('unfix top_mesh', ''.join(files.values()))
        self.assertNotIn('unfix zwall_top', ''.join(files.values()))

    def test_all_boundaries_fail_closed(self):
        files = d.bundle(d.synthetic_config())
        self.assertEqual(len([k for k in files if k.startswith('gates/')]), 7)
        for key, text in files.items():
            if key.startswith('gates/'):
                self.assertIn('quit 1', text)
        self.assertIn('S0_IS_RA_END', files['stages/05_relaxation.in'])
        self.assertIn('SECOND_ZERO_WINDOW_END', files['stages/07_separation.in'])

    def test_no_recomputed_pressure_after_restart(self):
        for key, text in d.bundle(d.synthetic_config()).items():
            if key.startswith('stages/'):
                self.assertNotIn('run 0', text)
                if 'write_restart' in text:
                    self.assertLess(text.index('G2_CAPTURE'), text.index('write_restart'))

    def test_policy_units_and_no_prep_damping_leak(self):
        files = d.bundle(d.synthetic_config())
        comp = files['stages/03_compression.in']
        self.assertIn('variable g2_target equal 750', comp)
        self.assertIn('unfix damp', comp)
        self.assertIn('fix damp all viscous 1e-05', comp)
        self.assertIn('gravity 9.81e-06', files['stages/02_stabilization.in'])
        self.assertIn('processors * * 1', files['stages/01_insertion.in'])
        self.assertNotIn('viscous 0.5', ''.join(files.values()))

    def test_input_refusal(self):
        for key, val in [('purpose', 'PRODUCTION'), ('np', 20), ('dt', None),
                         ('seed', True), ('case', '../escape'), ('gamma_compression', None),
                         ('control_period', .00000015), ('target_mpa', 299)]:
            with self.assertRaises(ValueError, msg=key):
                d.bundle({**d.synthetic_config(), key: val})
        with self.assertRaises(ValueError):
            d.bundle({**d.synthetic_config(), 'unregistered_extra': 1})

    def test_dt_half_preserves_physical_window(self):
        a = d.synthetic_config()
        b = {**a, 'dt': a['dt']/2}
        self.assertEqual(d.steps(b['control_period'], b['dt']), 2*d.steps(a['control_period'], a['dt']))
        self.assertEqual(d.steps(b['relaxation_time'], b['dt']), 2*d.steps(a['relaxation_time'], a['dt']))

    def test_composite_recipe_rendering(self):
        for count in (1, 2, 3):
            with self.subTest(material_count=count):
                config = d.synthetic_config(material_count=count)
                files = d.bundle(config)
                insertion = files['stages/01_insertion.in']
                self.assertIn('create_box %d g2box' % count, insertion)
                templates = [line.split() for line in insertion.splitlines()
                             if ' particletemplate/sphere ' in line]
                self.assertEqual(len(templates), count)
                for index, (tokens, material) in enumerate(zip(templates, config['materials']), 1):
                    seed = int(tokens[tokens.index('particletemplate/sphere') + 1])
                    self.assertGreaterEqual(seed, 10000)
                    self.assertLessEqual(seed, 2147483647)
                    self.assertFalse(any(seed % divisor == 0 for divisor in range(2, math.isqrt(seed) + 1)))
                    self.assertEqual(int(tokens[tokens.index('atom_type') + 1]), index)
                    self.assertEqual(float(tokens[tokens.index('density') + 2]), material['density'])
                    self.assertEqual(float(tokens[tokens.index('radius') + 2]), material['radius_deck'])
                matrix_lines = [line.split() for line in insertion.splitlines()
                                if ' peratomtypepair ' in line]
                self.assertEqual(len(matrix_lines), 6)
                for tokens in matrix_lines:
                    offset = tokens.index('peratomtypepair')
                    self.assertEqual(int(tokens[offset + 1]), count)
                    self.assertEqual(len(tokens[offset + 2:]), count * count)
                pdd = next(line.split() for line in insertion.splitlines()
                           if line.startswith('fix ') and ' particledistribution/discrete ' in line)
                offset = pdd.index('particledistribution/discrete')
                self.assertEqual(int(pdd[offset + 2]), count)
                self.assertEqual([float(x) for x in pdd[offset + 4::2]],
                                 [m['mass_fraction'] for m in config['materials']])
                manifest = json.loads(files['manifest.json'])
                self.assertEqual(manifest['composite_recipe'], 'SYNTHETIC_RENDERER_ONLY')
                self.assertFalse(manifest['physical_ready'])
                self.assertFalse(manifest['execution_go'])
                self.assertIn('quit 1', files['main.in'].split('include')[0])

    def test_mass_volume_and_number_fractions_are_distinct(self):
        config = d.synthetic_config(material_count=3)
        manifest = json.loads(d.bundle(config)['manifest.json'])
        rows = manifest['synthetic_recipe_fractions']
        materials = config['materials']
        volumes = [m['mass_fraction'] / m['density'] for m in materials]
        numbers = [v / m['radius_deck'] ** 3 for v, m in zip(volumes, materials)]
        for row, material, volume, number in zip(rows, materials, volumes, numbers):
            self.assertEqual(row['mass_fraction_input'], material['mass_fraction'])
            self.assertAlmostEqual(row['volume_fraction_derived'], volume / sum(volumes))
            self.assertAlmostEqual(row['number_fraction_derived'], number / sum(numbers))
        self.assertNotAlmostEqual(rows[0]['mass_fraction_input'], rows[0]['volume_fraction_derived'])
        self.assertNotAlmostEqual(rows[0]['volume_fraction_derived'], rows[0]['number_fraction_derived'])
        self.assertEqual([m['density'] for m in materials], [1640, 4850, 4850])
        self.assertEqual(manifest['distribution_fraction_basis'], 'mass')

    def test_invalid_material_recipes_are_refused(self):
        base = d.synthetic_config(material_count=3)
        mutations = [lambda c: c.update(materials=[]), lambda c: c.update(materials=()),
                     lambda c: c['materials'].append(copy.deepcopy(c['materials'][0])),
                     lambda c: c['materials'][0].update(name='AM_PC'),
                     lambda c: c['materials'][1].update(name='../AM_PC'),
                     lambda c: c['materials'][1].update(name='AM_SC'),
                     lambda c: c['materials'][0].update(density=4850),
                     lambda c: c['materials'][1].update(density=1640),
                     lambda c: c['materials'][0].update(mass_fraction=0),
                     lambda c: c['materials'][0].update(mass_fraction=.41),
                     lambda c: c['materials'][0].update(radius_deck=1e-200),
                     lambda c: c['materials'][0].update(poisson=.5),
                     lambda c: c['materials'][0].update(unregistered_extra=1)]
        for key in ('radius_deck', 'density', 'young_deck', 'poisson', 'mass_fraction'):
            for value in (True, None, '1', float('nan'), float('inf'), -1, 10 ** 1000):
                mutations.append(lambda c, key=key, value=value: c['materials'][0].update({key: value}))
        for index, mutate in enumerate(mutations):
            config = copy.deepcopy(base)
            mutate(config)
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                d.bundle(config)
        for bad_count in (True, 0, 4, 2.0):
            with self.assertRaises(ValueError):
                d.synthetic_config(material_count=bad_count)

    def test_largest_radius_drives_geometry(self):
        config = d.synthetic_config(material_count=3)
        config['materials'][2]['radius_deck'] = .001
        files = d.bundle(config)
        self.assertIn('neighbor 0.004 bin', files['stages/01_insertion.in'])
        self.assertIn('variable g2_plate_z equal c_g2z+0.001+0.003', files['stages/02_stabilization.in'])
        for field, value in (('width', .002), ('depth', .002), ('insertion_hi', .006)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                d.bundle({**config, field: value})
        self.assertEqual(sum('fix top_mesh all ' in v for k, v in files.items() if k.startswith('stages/')), 1)
        self.assertEqual(sum('fix zwall_top all ' in v for k, v in files.items() if k.startswith('stages/')), 1)

    def test_capture_expands_live_scalar_fields(self):
        files = d.bundle(d.synthetic_config())
        stabilization = files['stages/02_stabilization.in']
        self.assertIn('variable g2_rot_live equal c_g2rot', stabilization)
        self.assertIn('variable g2_ke_live equal ke', stabilization)
        self.assertIn('variable g2_zmax_live equal c_g2z', stabilization)
        for name, text in files.items():
            if name.startswith('stages/'):
                for line in text.splitlines():
                    if line.startswith('print "G2_CAPTURE'):
                        self.assertIn('step=${g2_step}', line)
                        self.assertIn('time=${g2_time}', line)
                        self.assertIn('atoms=${g2_atoms}', line)
                        self.assertNotIn('c_g2rot', line)
                        if 'phase=insertion ' not in line:
                            self.assertIn('rotation_energy=${g2_rot_live}', line)
                            self.assertIn('kinetic_energy=${g2_ke_live}', line)
                            self.assertIn('zmax=${g2_zmax_live}', line)

    def test_derived_numeric_failures_are_refused(self):
        for delta in ({'width': 1e200, 'depth': 1e200},
                      {'unload_step': 2.333333333333333e-06, 'unload_speed': .3333333333333333}):
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                d.bundle({**d.synthetic_config(), **delta})

    def test_serialized_numbers_preserve_input_precision(self):
        config = d.synthetic_config()
        config['gamma_hold'] = .12345678901234567
        files = d.bundle(config)
        self.assertIn('fix damp all viscous ' + str(config['gamma_hold']), files['stages/02_stabilization.in'])

    def test_active_thermo_keeps_capture_computes_current(self):
        stabilization = d.bundle(d.synthetic_config())['stages/02_stabilization.in']
        active_thermo = [line.split() for line in stabilization.splitlines()
                        if line.startswith('thermo_style custom ')][-1]
        for token in ('ke', 'c_g2rot', 'c_g2z', 'v_g2_force_live'):
            self.assertIn(token, active_thermo)

    def test_control_reads_frozen_force_after_restart(self):
        files = d.bundle(d.synthetic_config())
        velocity = next(line for line in files['stages/03_compression.in'].splitlines()
                        if line.startswith('variable g2_velocity '))
        self.assertIn('v_g2_force_sample', velocity)
        self.assertNotIn('v_g2_force_live', velocity)
        for name, text in files.items():
            if not name.startswith('stages/') or name.endswith('01_insertion.in'):
                continue
            live_force_available = not name.endswith('02_stabilization.in')
            lines = text.splitlines()
            for index, line in enumerate(lines):
                if line.startswith('variable g2_force_live '):
                    live_force_available = True
                if line.startswith('run ') and live_force_available:
                    with self.subTest(stage=name, run=line):
                        self.assertEqual(lines[index + 1], 'variable g2_force_sample equal ${g2_force_live}')
                        self.assertTrue(lines[index + 2].startswith('print "G2_CAPTURE '))
                        self.assertIn('force=${g2_force_sample}', lines[index + 2])


if __name__ == '__main__':
    unittest.main()
