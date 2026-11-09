"""Generate an INACTIVE seven-stage gen2 deck candidate, never launch it.

Only an explicit synthetic configuration is accepted in this revision. Every
entry/stage gate stops. Live observation adapters and P2 ULPR serialization are
not implemented; removing a stop does NOT complete these contracts.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re

STAGES = ('insertion', 'stabilization', 'compression', 'servo',
          'relaxation', 'unloading', 'separation')
MATERIAL_KEYS = {'name', 'radius_deck', 'density', 'young_deck', 'poisson', 'mass_fraction'}
MATERIAL_DENSITIES = {'SE': 1640, 'AM_PC': 4850, 'AM_SC': 4850}
TEMPLATE_SEEDS = (32452843, 15485863, 32452867)
DISTRIBUTION_SEED = 49979687


def synthetic_config(material_count=1):
    """Fixture constants, not scientific registration or defaults for a bed."""
    if type(material_count) is not int or material_count not in (1, 2, 3):
        raise ValueError('synthetic material count must be one, two or three')
    fractions = {1: (1.,), 2: (.4, .6), 3: (.4, .35, .25)}[material_count]
    materials = [dict(name=name, radius_deck=radius, density=MATERIAL_DENSITIES[name],
                      young_deck=young, poisson=poisson, mass_fraction=fraction)
                 for (name, radius, young, poisson), fraction in zip(
                     (('SE', .0005, 1.35e6, .37), ('AM_PC', .0004, 3e6, .3),
                      ('AM_SC', .0007, 3e6, .3)), fractions)]
    return dict(purpose='SYNTHETIC_PREPARATION', case='synthetic_se' if material_count == 1 else 'synthetic_%dphase' % material_count, np=1,
                dt=1e-6, seed=78049, target_mpa=300, width=.05, depth=.05,
                compression_sign=1,
                materials=materials,
                settle_time=.01, stabilization_time=.01, control_period=.005,
                compression_budget=.05, servo_budget=.05, relaxation_time=.01,
                gamma_preparation=1e-5, gamma_compression=1e-5, gamma_hold=1e-5,
                kp=30., vmax=.01, plate_margin=.003, box_top=1.,
                insertion_lo=.005, insertion_hi=.035, insertion_fraction=.321,
                unload_step=.00005, unload_speed=.01, unload_budget=8,
                post_windows=4)


def positive_finite(value, label):
    try:
        valid = type(value) in (int, float) and math.isfinite(value) and value > 0
    except OverflowError:
        valid = False
    if not valid:
        raise ValueError('positive finite number required: ' + label)
    return value


def exact_steps(ratio):
    if ratio <= 0 or ratio.denominator != 1 or ratio > 2**31-1:
        raise ValueError('time must contain an exact positive integer step count')
    return int(ratio)


def steps(duration, dt):
    for value in (duration, dt):
        positive_finite(value, 'time')
    return exact_steps(Fraction(str(duration))/Fraction(str(dt)))


def movement_steps(config):
    # Exact decimal-token fractions: neither float nor Decimal-context rounding.
    return exact_steps(Fraction(str(config['unload_step'])) /
                       (Fraction(str(config['unload_speed'])) * Fraction(str(config['dt']))))


def prime_seed(seed):
    return (type(seed) is int and 10000 <= seed <= 2147483647
            and not any(seed % d == 0 for d in range(2, math.isqrt(seed) + 1)))


def recipe_fractions(materials):
    """Monodisperse synthetic arithmetic, never measured composition/counts."""
    volumes = [Fraction(str(m['mass_fraction'])) / Fraction(str(m['density'])) for m in materials]
    numbers = [v / Fraction(str(m['radius_deck'])) ** 3 for v, m in zip(volumes, materials)]
    return [dict(name=m['name'], atom_type=i, mass_fraction_input=m['mass_fraction'],
                 volume_fraction_derived=float(v / sum(volumes)),
                 number_fraction_derived=float(n / sum(numbers)))
            for i, (m, v, n) in enumerate(zip(materials, volumes, numbers), 1)]


def validate(config):
    if type(config) is not dict or set(config) != set(synthetic_config()):
        raise ValueError('exact configuration keys required')
    if config['purpose'] != 'SYNTHETIC_PREPARATION':
        raise ValueError('production registration and adapter not implemented')
    if type(config['case']) is not str or not re.fullmatch('[a-z][a-z0-9_]{0,39}', config['case']):
        raise ValueError('safe case token required')
    # A synthetic sign convention is required. This is NOT actual T0 evidence.
    if type(config['compression_sign']) is not int or config['compression_sign'] not in (-1, 1):
        raise ValueError('compression_sign must be exact integer -1 or +1')
    for key in set(config)-{'purpose', 'case', 'materials', 'compression_sign'}:
        positive_finite(config[key], key)
    for key in ('np', 'seed', 'unload_budget', 'post_windows'):
        if type(config[key]) is not int:
            raise ValueError('integer required: '+key)
    if config['np'] not in (1, 2) or config['target_mpa'] != 300 or config['post_windows'] != 4:
        raise ValueError('gen2 policy mismatch')
    if not prime_seed(config['seed']):
        raise ValueError('insertion seed must be an in-range prime')
    materials = config['materials']
    if type(materials) is not list or not 1 <= len(materials) <= 3:
        raise ValueError('one to three material objects required')
    names = []
    for material in materials:
        if type(material) is not dict or set(material) != MATERIAL_KEYS:
            raise ValueError('exact material keys required')
        name = material['name']
        if type(name) is not str or name not in MATERIAL_DENSITIES or name in names:
            raise ValueError('unique SE/AM_PC/AM_SC material names required')
        names.append(name)
        for key in MATERIAL_KEYS - {'name'}:
            positive_finite(material[key], 'material ' + key)
        if material['density'] != MATERIAL_DENSITIES[name]:
            raise ValueError('ratified gen2 density mismatch')
        if not 0 < material['poisson'] < .5 or material['mass_fraction'] > 1:
            raise ValueError('material poisson/mass fraction outside range')
        try:
            positive_finite((4. / 3.) * math.pi * material['radius_deck'] ** 3 * material['density'],
                            'representable synthetic sphere mass')
        except OverflowError as exc:
            raise ValueError('synthetic sphere mass overflow') from exc
    if names[0] != 'SE':
        raise ValueError('SE must be first; existing walls reuse material type one')
    if sum(Fraction(str(m['mass_fraction'])) for m in materials) != 1:
        raise ValueError('mass fractions must sum exactly to one')
    if not all(prime_seed(seed) for seed in TEMPLATE_SEEDS[:len(materials)] + (DISTRIBUTION_SEED,)):
        raise ValueError('template/distribution seeds must be in-range primes')
    rmax = max(m['radius_deck'] for m in materials)
    if not 0 < config['insertion_fraction'] < 1:
        raise ValueError('insertion fraction outside range')
    if not 2 * rmax < min(config['width'], config['depth']):
        raise ValueError('largest sphere too large for box')
    if not 0 < config['insertion_lo'] < config['insertion_hi'] < config['box_top']:
        raise ValueError('invalid insertion extents')
    if not 2 * rmax < config['insertion_hi'] - config['insertion_lo']:
        raise ValueError('largest sphere too large for insertion region')
    positive_finite(300e6 * .001 * config['width'] * config['depth'], 'synthetic target force')
    positive_finite(rmax + config['plate_margin'], 'plate offset')
    positive_finite(config['kp'] * config['vmax'], 'controller scale')
    positive_finite(config['unload_step'] * config['unload_budget'], 'bounded unload travel')
    for row in recipe_fractions(materials):
        positive_finite(row['volume_fraction_derived'], 'representable volume fraction')
        positive_finite(row['number_fraction_derived'], 'representable number fraction')
    for key in ('settle_time', 'stabilization_time', 'control_period', 'compression_budget',
                'servo_budget', 'relaxation_time'):
        steps(config[key], config['dt'])
    for key in ('compression_budget', 'servo_budget', 'relaxation_time'):
        steps(config[key], config['control_period'])
    movement_steps(config)
    if config['post_windows'] * steps(config['control_period'], config['dt']) > 2**31 - 1:
        raise ValueError('post-window step count outside range')
    return config


def bundle(config):
    c = validate(config)
    # str(float) is round-trip; do not silently truncate validated input to 15 digits.
    f = lambda key: str(c[key])
    materials = c['materials']
    ntypes = len(materials)
    rmax = max(m['radius_deck'] for m in materials)
    period = steps(c['control_period'], c['dt'])
    files = {}
    main = ['# INACTIVE GEN2 CANDIDATE; NOT A PRODUCTION DECK',
            'print "HOLD: scientific registration and live adapters unresolved"', 'quit 1']
    for i, stage in enumerate(STAGES, 1):
        main.append(f'include stages/{i:02d}_{stage}.in')
        files[f'gates/{stage}.in'] = (
            f'# {stage}: mandatory live observation/identity gate UNIMPLEMENTED\n'
            '# A boolean PASS token or file existence is not a physical gate.\n'
            f'print "HOLD: {stage} observer-to-deck adapter absent"\nquit 1\n')
    files['main.in'] = '\n'.join(main)+'\n'

    def capture_line(stage, wall=True):
        # Evaluate from the last real run BEFORE restart; the print is a scalar
        # diagnostic only, not a complete qualified boundary record.
        obs = (' raw_reaction=${g2_reaction_sample} compression_sign=${g2_compression_sign}'
               ' force=${g2_force_sample} rotation_energy=${g2_rot_live}'
               ' kinetic_energy=${g2_ke_live} zmax=${g2_zmax_live}') if wall else ''
        # Normalize the SAME frozen signed reaction, never a second live read.
        freeze = ('variable g2_reaction_sample equal ${g2_reaction_live}\n'
                  'variable g2_force_sample equal ${g2_compression_sign}*${g2_reaction_sample}\n') if wall else ''
        guard = ('\nif "${g2_force_sample} < 0" then "print \'TECH_HOLD: force polarity mismatch\'" "quit 1"') if wall else ''
        return freeze + f'print "G2_CAPTURE phase={stage} step=${{g2_step}} time=${{g2_time}} atoms=${{g2_atoms}}{obs}"' + guard

    def capture(stage, wall=True):
        return [capture_line(stage, wall),
                f'include gates/{stage}.in',
                f'write_restart restart_{stage}.bin']

    insertion = ['# SYNTHETIC ONLY: configurable material recipe; no scientific registration',
        'atom_style granular', 'atom_modify map array sort 0 0', 'boundary p p f',
        'newton off', 'soft_particles yes', 'communicate single vel yes', 'units si',
        'processors * * 1', f'timestep {f("dt")}',
        f'region g2box block 0 {f("width")} 0 {f("depth")} -0.01 {f("box_top")} units box',
        f'create_box {ntypes} g2box', f'neighbor {rmax*4} bin', 'neigh_modify delay 0 check yes']
    matrix = lambda value: ' '.join([value] * (ntypes * ntypes))
    properties = [('youngsModulus', 'peratomtype', ' '.join(str(m['young_deck']) for m in materials)),
                  ('poissonsRatio', 'peratomtype', ' '.join(str(m['poisson']) for m in materials)),
                  ('coefficientRestitution', f'peratomtypepair {ntypes}', matrix('.3')),
                  ('coefficientFriction', f'peratomtypepair {ntypes}', matrix('.5')),
                  ('coefficientRollingFriction', f'peratomtypepair {ntypes}', matrix('.1')),
                  ('coefficientMaxElasticStiffness', f'peratomtypepair {ntypes}', matrix('5')),
                  ('coefficientAdhesionStiffness', f'peratomtypepair {ntypes}', matrix('1e6')),
                  ('coefficientPlasticityDepth', f'peratomtypepair {ntypes}', matrix('.005')),
                  ('characteristicVelocity', 'scalar', '2')]
    insertion += [f'fix g2m{i} all property/global {p} {s} {v}' for i, (p, s, v) in enumerate(properties, 1)]
    contact = 'model hooke/hysteresis tangential history rolling_friction cdt'
    insertion += [f'pair_style gran {contact}', 'pair_coeff * *',
        f'fix zwall_bot all wall/gran {contact} primitive type 1 zplane 0']
    insertion += [f'fix g2pt{i} all particletemplate/sphere {seed} atom_type {i} density constant {m["density"]} radius constant {m["radius_deck"]}'
                  for i, (m, seed) in enumerate(zip(materials, TEMPLATE_SEEDS), 1)]
    insertion += ['# particledistribution/discrete inputs below are MASS fractions, not volume/number fractions.',
        f'fix g2pd all particledistribution/discrete {DISTRIBUTION_SEED} {ntypes} ' +
        ' '.join(f'g2pt{i} {m["mass_fraction"]}' for i, m in enumerate(materials, 1)),
        f'region g2mix block 0 {f("width")} 0 {f("depth")} {f("insertion_lo")} {f("insertion_hi")} units box',
        f'fix g2ins all insert/pack seed {c["seed"]} distributiontemplate g2pd maxattempt 15000 insert_every once overlapcheck yes all_in yes vel constant 0 0 -0.5 region g2mix volumefraction_region {f("insertion_fraction")}',
        'variable g2_step equal step', 'variable g2_time equal time', 'variable g2_atoms equal atoms', 'run 1',
        'unfix g2ins'] + capture('insertion', False)

    stabilize = ['fix integr all nve/sphere', 'fix gravi all gravity 98.1 vector 0 0 -1',
        f'fix damp all viscous {f("gamma_preparation")}', 'compute g2z all reduce max z',
        'compute g2rot all erotate/sphere', 'variable g2_rot_live equal c_g2rot',
        'variable g2_ke_live equal ke', 'variable g2_zmax_live equal c_g2z',
        'thermo_style custom step atoms ke c_g2rot c_g2z',
        'thermo 1', f'run {steps(c["settle_time"], c["dt"])}',
        f'variable g2_plate_z equal c_g2z+{rmax}+{f("plate_margin")}']
    stl = ['solid plate']
    for triangle in (((0, 0), (c['width'], c['depth']), (c['width'], 0)),
                     ((0, 0), (0, c['depth']), (c['width'], c['depth']))):
        stl += ['facet normal 0 0 -1', 'outer loop']
        stl += [f'vertex {x} {y} ${{g2_plate_z}}' for x, y in triangle]
        stl += ['endloop', 'endfacet']
    stl += ['endsolid plate']
    stabilize += [f'print "{line}" {"file" if i == 0 else "append"} g2_plate.stl screen no' for i, line in enumerate(stl)]
    stabilize += ['fix top_mesh all mesh/surface/stress file g2_plate.stl type 1 reference_point 0 0 0',
        f'fix zwall_top all wall/gran {contact} mesh n_meshes 1 meshes top_mesh',
        'compute g2pair all pair/gran/local pos id force force_normal force_tangential torque contactArea delta contactPoint',
        'compute g2wall all wall/gran/local id force_normal', 'compute g2stress all stress/atom',
        f'variable g2_compression_sign equal {c["compression_sign"]}',
        'variable g2_reaction_live equal f_top_mesh[3]',
        'variable g2_force_live equal v_g2_compression_sign*v_g2_reaction_live',
        'thermo_style custom step atoms ke c_g2rot c_g2z v_g2_reaction_live v_g2_force_live',
        f'dump g2atoms all custom {period} atom_*.liggghts id type x y z radius mass vx vy vz omegax omegay omegaz fx fy fz c_g2stress[1] c_g2stress[2] c_g2stress[3] c_g2stress[4] c_g2stress[5] c_g2stress[6]',
        f'dump g2pairs all local {period} pair_*.liggghts '+' '.join(f'c_g2pair[{i}]' for i in range(1, 27)),
        f'dump g2walls all local {period} wall_*.liggghts '+' '.join(f'c_g2wall[{i}]' for i in range(1, 7)),
        f'dump g2mesh all mesh/stl {period} mesh_*.stl top_mesh',
        'unfix gravi', 'fix gravi all gravity 9.81e-06 vector 0 0 -1',
        'unfix damp', f'fix damp all viscous {f("gamma_hold")}',
        f'run {steps(c["stabilization_time"], c["dt"])}'] + capture('stabilization')

    target = 300e6*.001*c['width']*c['depth']
    def controlled(stage):
        gamma = 'gamma_compression' if stage == 'compression' else 'gamma_hold'
        out = ['unfix damp', f'fix damp all viscous {f(gamma)}']
        if stage == 'compression':
            out += [f'variable g2_target equal {target}',
                    f'variable g2_velocity equal -max(-{f("vmax")},min({f("vmax")},{f("kp")}*{f("vmax")}*(v_g2_target-v_g2_force_sample)/v_g2_target))']
        out += [f'variable g2_{stage}_k loop {steps(c[stage+"_budget"], c["control_period"])}',
                f'label g2_{stage}_loop',
                'fix g2move all move/mesh mesh top_mesh linear 0 0 ${g2_velocity}',
                f'run {period}', capture_line(stage),
                'unfix g2move', f'include gates/{stage}.in',
                '# Future adapter must bind complete windows and stage state, not just g2_done.',
                f'if "${{g2_done}} == 1" then "jump SELF g2_{stage}_end"',
                f'next g2_{stage}_k', f'jump SELF g2_{stage}_loop',
                f'print "NOT_CONVERGED: {stage} budget exhausted"', 'quit 1',
                f'label g2_{stage}_end', f'write_restart restart_{stage}.bin']
        return out

    relaxation = ['# R-a: same stationary plate; no motion fix. S0_IS_RA_END.',
                  'unfix damp', f'fix damp all viscous {f("gamma_hold")}',
                  f'run {steps(c["relaxation_time"], c["dt"])}']+capture('relaxation')
    move_n = movement_steps(c)
    unloading = ['# P2 ULPR adapter absent: this is a bounded motion candidate only.',
                 '# Actual h0 scaling, A/B steps, S1-S4, primary/trajectory status and selection remain unbound.',
                 f'variable g2_unload_k loop {c["unload_budget"]}', 'label g2_unload_loop',
                 f'fix g2move all move/mesh mesh top_mesh linear 0 0 {f("unload_speed")}',
                 f'run {move_n}', capture_line('unloading'), 'unfix g2move', f'run {period}',
                 capture_line('unloading'),
                 'include gates/unloading.in',
                 'if "${g2_done} == 1" then "jump SELF g2_unload_end"',
                 'next g2_unload_k', 'jump SELF g2_unload_loop',
                 'print "NOT_CONVERGED: unloading bound exhausted"', 'quit 1',
                 'label g2_unload_end', 'write_restart restart_unloading.bin']
    separation = ['# SECOND_ZERO_WINDOW_END must be demonstrated by the future complete observer.',
                  '# Retain separated mesh/wall: no unfix and no contact-history deletion.',
                  'include gates/separation.in',
                  '# Future post-four-window S2/S4 and fixed-S0-ID/free-surface observations required.',
                  f'run {c["post_windows"]*period}']+capture('separation')
    for i, lines in enumerate((insertion, stabilize, controlled('compression'), controlled('servo'),
                               relaxation, unloading, separation), 1):
        files[f'stages/{i:02d}_{STAGES[i-1]}.in'] = '\n'.join(lines)+'\n'
    manifest = dict(schema='dem-gen2-inactive-candidate-v1', purpose=c['purpose'],
                    config=c, stages=list(STAGES), physical_ready=False, execution_go=False,
                    research_results=0, T0='NOT_RUN', T5='NOT_RUN', T11='NOT_RUN', T12='NOT_RUN',
                    synthetic_compression_sign=c['compression_sign'], actual_T0_compression_sign=None,
                    reaction_contract='Raw signed sample retained; polarity-normalized negative force stops before control',
                    live_adapter='UNIMPLEMENTED', composite_recipe='SYNTHETIC_RENDERER_ONLY',
                    distribution_fraction_basis='mass', synthetic_recipe_fractions=recipe_fractions(materials),
                    material_order=[m['name'] for m in materials], wall_material_type=1,
                    material_and_contact_parameters='SYNTHETIC_FIXTURE_NOT_REGISTERED_RECIPE',
                    scalar_capture='EXPANDED_DIAGNOSTICS_ONLY_NOT_COMPLETE_BOUNDARY_RECORD',
                    p2_ulpr_serializer='UNIMPLEMENTED', exact_boundary_frames='UNIMPLEMENTED',
                    binary_syntax='NOT_RUN', operational_seal_modified=False,
                    files={k: hashlib.sha256(v.encode()).hexdigest() for k, v in sorted(files.items())})
    files['manifest.json'] = json.dumps(manifest, indent=2, sort_keys=True)+'\n'
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--synthetic-out', type=Path, required=True)
    parser.add_argument('--synthetic-material-count', type=int, choices=(1, 2, 3), default=1)
    args = parser.parse_args()
    files = bundle(synthetic_config(material_count=args.synthetic_material_count))
    args.synthetic_out.mkdir(parents=True, exist_ok=False)
    for name, text in files.items():
        dest = args.synthetic_out/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(text)


if __name__ == '__main__':
    main()
