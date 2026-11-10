"""Synthetic S0 contract suite, Q-S0-1/2 assumptions, synthetic data only.

The LIVE fixture/dependency must first be fixed and verified by its own task.
Install exact source copies and the agreed audit guard before running tests.
No real atom/contact/restart file is read and no engine or host is invoked.
"""
import base64
import copy
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest

source_dir = Path(__file__).parent
fixture_module = types.ModuleType('synthetic_live_fixture')
fixture_module.__file__ = str(source_dir / 'test_dem_gen2_live_contract.py')
exec(compile(Path(fixture_module.__file__).read_bytes(), fixture_module.__file__, 'exec'), fixture_module.__dict__)
live = sys.modules['dem_gen2_live_contract']
s0 = types.ModuleType('dem_gen2_s0_contract')
s0.__file__ = str(source_dir / 'dem_gen2_s0_contract.py')
exec(compile(Path(s0.__file__).read_bytes(), s0.__file__, 'exec'), s0.__dict__)

ROLES = ('atom', 'pair', 'wall', 'mesh', 'restart', 'state')
ATOM_COLUMNS = ['id', 'type', 'x', 'y', 'z', 'radius', 'mass', 'vx', 'vy', 'vz',
                'omegax', 'omegay', 'omegaz', 'fx', 'fy', 'fz']
ATOM_UNITS = ['identity', 'type_identity', 'length', 'length', 'length', 'length',
              'mass', 'velocity', 'velocity', 'velocity', 'angular_velocity',
              'angular_velocity', 'angular_velocity', 'force', 'force', 'force']
PAIR_COLUMNS = ['c_cpl[%d]' % i for i in range(1,27)]
WALL_U = ['mesh', 'tri', 'id', 'fnx', 'fny', 'fnz']
WALL_R = WALL_U + ['delta_max', 'shear_x', 'shear_y', 'shear_z']


def independent_bytes(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def mapping(role, wall_profile):
    columns = PAIR_COLUMNS if role == 'pair' else (WALL_U if wall_profile == 'WALL_U' else WALL_R)
    meanings = ['declared_slot_%02d' % (i+1) for i in range(len(columns))]
    if role == 'pair': meanings[22] = 'current_overlap'
    return dict(schema='SYNTHETIC_S0_MAPPING_REFERENCE_V1',
        mapping_id='synthetic_'+role+'_mapping', source_pin='4c29705fa1c4ba94737a858b206fa4f4c5bb2bde',
        scope='DECLARED_SYNTHETIC_MAPPING_ONLY', profile='PAIR26' if role == 'pair' else wall_profile,
        columns=list(columns), units=['declared_unit_%02d' % (i+1) for i in range(len(columns))],
        meanings=meanings, overlap_semantics='CURRENT_OVERLAP_ONLY' if role == 'pair'
        else 'DECLARED_OBSERVABLES_NOT_HIDDEN_HISTORY_PROOF', hidden_history_qualified=False)


def replace_payload(obj, data):
    obj.update(payload_base64=base64.b64encode(data).decode('ascii'),
               payload_bytes=len(data), payload_sha256=digest(data))


def rechain(envelope):
    previous = digest(independent_bytes(envelope['boundary_candidate']))
    for index, obj in enumerate(envelope['objects']):
        obj['generation_ordinal'] = index
        obj['parent_sha256'] = previous
        previous = digest(independent_bytes(obj))


def fixture(wall_profile='WALL_U', grid_choice='coarse'):
    """Declared semantic slots are toy references, not an actual P2 mapping."""
    plan, servo, ra = fixture_module.fixture(grid_choice=grid_choice)
    result = live.diagnose_live_ra(plan, servo, ra)
    if result['status'] != 'SYNTHETIC_RA_END_CANDIDATE':
        raise AssertionError('LIVE dependency is not a fixed passing fixture: '+result['status'])
    boundary = result['boundary_candidate']
    boundary_hash = digest(independent_bytes(boundary))
    contract = dict(schema='SYNTHETIC_S0_CONTRACT_V1', purpose='SYNTHETIC_PREPARATION',
        s0_id='synthetic_s0', assumptions=['Q-S0-1', 'Q-S0-2'], boundary_sha256=boundary_hash,
        pair_reference=mapping('pair', wall_profile), wall_reference=mapping('wall', wall_profile))
    atom_rows = [[p['id'], p['type'], float(p['id']), 0., 1., p['radius'], p['mass'],
        0., 0., 0., .1, .2, .3, 0., 0., 0.] for p in boundary['reference_inventory']]
    first_particle = boundary['reference_inventory'][0]['id']
    objects = []
    for index, role in enumerate(ROLES):
        obj = dict(role=role, format_revision=1, boundary_sha256=boundary_hash,
            step=boundary['end_step'], mesh_id=boundary['plate']['mesh_id'],
            wall_id=boundary['plate']['wall_id'], history_id=boundary['plate']['history_id'],
            inventory_id=boundary['inventory_id'], generation_ordinal=index, parent_sha256='0'*64)
        if role == 'atom':
            reference = dict(schema='SYNTHETIC_ATOM16_MAPPING_V1', columns=list(ATOM_COLUMNS), units=list(ATOM_UNITS))
            obj.update(media_type='application/json', columns=list(ATOM_COLUMNS), units=list(ATOM_UNITS))
            data = independent_bytes(dict(schema='SYNTHETIC_S0_ATOM_PAYLOAD_V1', rows=atom_rows))
        elif role in ('pair', 'wall'):
            reference = contract[role+'_reference']
            obj.update(media_type='application/json', columns=list(reference['columns']), units=list(reference['units']))
            row = [0.]*26 if role == 'pair' else [0, 0, first_particle, 0., 0., 0.]
            if role == 'wall' and wall_profile == 'WALL_R': row += [0., 0., 0., 0.]
            data = independent_bytes(dict(schema='SYNTHETIC_S0_'+role.upper()+'_PAYLOAD_V1', rows=[row]))
        else:
            reference = dict(schema='OPAQUE_SYNTHETIC_BYTES_ONLY', role=role)
            obj.update(media_type='application/octet-stream', columns=[], units=[])
            data = ('synthetic_'+role+'_bytes').encode('ascii')
        obj['semantic_mapping_sha256'] = digest(independent_bytes(reference))
        replace_payload(obj, data)
        objects.append(obj)
    envelope = dict(schema='SYNTHETIC_S0_ENVELOPE_V1', purpose='SYNTHETIC_PREPARATION',
        s0_id='synthetic_s0', boundary_candidate=copy.deepcopy(boundary), objects=objects)
    rechain(envelope)
    return contract, envelope, plan, servo, ra


def payload_json(obj):
    return json.loads(base64.b64decode(obj['payload_base64']).decode('utf-8'))


def archive_bytes(envelope):
    body = independent_bytes(envelope)
    return independent_bytes(dict(schema='SYNTHETIC_S0_ARCHIVE_V1', body=envelope,
                                  body_bytes=len(body), body_sha256=digest(body)))


class S0Contract(unittest.TestCase):
    def authority_off(self, result):
        for key in ('physical_ready', 'execution_go', 'transition_authorized', 'gate_write',
                    'operational_seal_modified', 'registration_complete', 'source_authenticated',
                    'hidden_history_qualified'):
            self.assertIs(result[key], False)
        for key in ('actual_T0', 'actual_T11', 'actual_T12'):
            self.assertEqual(result[key], 'NOT_RUN')
        self.assertIsNone(result['actual_S0'])
        self.assertEqual(result['research_results'], 0)
        self.assertEqual(result['assumptions'], ['Q-S0-1', 'Q-S0-2'])
        self.assertEqual(result['whole_status'], 'HOLD')

    def accepted(self, args):
        result = s0.validate_s0_envelope(*args)
        self.assertEqual(result['status'], 'SYNTHETIC_S0_CONSISTENT', result)
        self.assertEqual(result['checked_objects'], 6)
        self.authority_off(result)
        return result

    def refused(self, args, expected=None):
        result = s0.validate_s0_envelope(*args)
        self.assertIn(result['status'], ('REJECTED', 'NOT_COMPUTED'), result)
        if expected: self.assertEqual(result['status'], expected)
        self.assertEqual(result['checked_objects'], 0)
        self.authority_off(result)
        return result

    def test_01_six_objects_at_full_live_boundary_are_synthetic_only(self):
        for profile in ('WALL_U', 'WALL_R'):
            with self.subTest(profile=profile): self.accepted(fixture(profile))

    def test_02_serialization_matches_independent_canonical_body_bytes(self):
        args = fixture()
        encoded = s0.serialize_s0(*args)
        self.assertIs(type(encoded), bytes)
        self.assertEqual(encoded, archive_bytes(args[1]))
        decoded = s0.decode_s0(encoded, args[0], *args[2:])
        self.assertEqual(decoded, args[1])
        self.assertEqual(s0.serialize_s0(args[0], decoded, *args[2:]), encoded)

    def test_03_live_original_inputs_are_rechecked_not_candidate_or_status(self):
        args = fixture()
        args[-1][-1]['channels']['plate']['values']['velocity'][2] = 1.
        result = self.refused(args, 'NOT_COMPUTED')
        self.assertEqual(result['reason'], 'LIVE_RA_BOUNDARY_NOT_AVAILABLE')
        args = fixture()
        fake_receipt = {'status': 'SYNTHETIC_RA_END_CANDIDATE', 'boundary_candidate': args[1]['boundary_candidate']}
        self.refused((args[0], args[1], fake_receipt, [], []), 'NOT_COMPUTED')

    def test_04_missing_ra_budget_cannot_be_replaced_by_s0_metadata(self):
        args = fixture()
        self.refused((*args[:-1], args[-1][:-1]), 'NOT_COMPUTED')
        self.refused((*args[:-1], []), 'NOT_COMPUTED')

    def test_05_complete_boundary_comparison_includes_identity_and_all_digests(self):
        for field in ('end_step', 'end_sample_id', 'end_tick', 'end_window_index',
                      'plan_sha256', 'servo_trace_sha256', 'ra_trace_sha256', 'end_frame_sha256'):
            args = fixture()
            old = args[1]['boundary_candidate'][field]
            args[1]['boundary_candidate'][field] = old+1 if type(old) is int else 'e'*64
            rechain(args[1])
            with self.subTest(field=field): self.refused(args)
        for section, field in (('identity', 'attempt_id'), ('source_identity', 'case_id'), ('plate', 'history_id')):
            args = fixture()
            args[1]['boundary_candidate'][section][field] = 'other_token'
            rechain(args[1])
            with self.subTest(section=section): self.refused(args)

    def test_06_new_consistent_boundary_cannot_reuse_old_frozen_digest(self):
        args = fixture()
        old_contract = copy.deepcopy(args[0])
        changed = fixture(grid_choice='half')
        self.refused((old_contract, *changed[1:]))
        self.accepted(changed)

    def test_07_each_object_requires_same_step_history_and_inventory(self):
        for index in range(6):
            for key, value in (('step', 1), ('history_id', 'other_history'),
                               ('inventory_id', 'other_inventory'), ('mesh_id', 'other_mesh')):
                args = fixture()
                args[1]['objects'][index][key] = value
                rechain(args[1])
                with self.subTest(index=index, key=key): self.refused(args)

    def test_08_exact_six_roles_and_parent_chain_are_required(self):
        for mutation in ('missing', 'extra', 'reorder', 'ordinal', 'parent'):
            args = fixture()
            objects = args[1]['objects']
            if mutation == 'missing': objects.pop()
            elif mutation == 'extra': objects.append(copy.deepcopy(objects[-1]))
            elif mutation == 'reorder': objects[0], objects[1] = objects[1], objects[0]
            elif mutation == 'ordinal': objects[-1]['generation_ordinal'] = 3
            else: objects[-1]['parent_sha256'] = 'e'*64
            with self.subTest(mutation=mutation): self.refused(args)

    def test_09_atom_mass_type_radius_inventory_changes_are_not_coordinate_equivalence(self):
        for column, value in ((1, 3), (5, .75), (6, 9.)):
            args = fixture()
            atom = args[1]['objects'][0]
            payload = payload_json(atom)
            payload['rows'][0][column] = value
            replace_payload(atom, independent_bytes(payload))
            rechain(args[1])
            with self.subTest(column=column): self.refused(args)

    def test_10_atom_omega_and_all_sixteen_columns_are_mandatory(self):
        for mutation in ('column', 'row', 'unit'):
            args = fixture()
            atom = args[1]['objects'][0]
            if mutation == 'column': atom['columns'].pop(10)
            elif mutation == 'unit': atom['units'].pop(10)
            else:
                payload = payload_json(atom)
                payload['rows'][0].pop(10)
                replace_payload(atom, independent_bytes(payload))
            rechain(args[1])
            with self.subTest(mutation=mutation): self.refused(args, 'NOT_COMPUTED')

    def test_11_exact_unique_positive_atom_ids_and_full_inventory(self):
        for mutation in ('fraction', 'bool', 'duplicate', 'unknown', 'missing'):
            args = fixture()
            atom = args[1]['objects'][0]
            payload = payload_json(atom)
            if mutation == 'missing': payload['rows'].pop()
            else: payload['rows'][0][0] = {'fraction':1.5, 'bool':True, 'duplicate':2, 'unknown':99}[mutation]
            replace_payload(atom, independent_bytes(payload))
            rechain(args[1])
            with self.subTest(mutation=mutation): self.refused(args)

    def test_12_pair26_names_order_units_and_mapping_digest_are_bound(self):
        for mutation in ('missing_column', 'reorder_column', 'unit', 'mapping', 'row_width'):
            args = fixture()
            pair = args[1]['objects'][1]
            if mutation == 'missing_column': pair['columns'].pop()
            elif mutation == 'reorder_column': pair['columns'][0], pair['columns'][1] = pair['columns'][1], pair['columns'][0]
            elif mutation == 'unit': pair['units'][0] = 'wrong_unit'
            elif mutation == 'mapping': pair['semantic_mapping_sha256'] = 'e'*64
            else:
                payload = payload_json(pair)
                payload['rows'][0].pop()
                replace_payload(pair, independent_bytes(payload))
            rechain(args[1])
            with self.subTest(mutation=mutation): self.refused(args)

    def test_13_current_overlap_cannot_claim_hidden_history_qualification(self):
        for mutation in ('meaning', 'claim'):
            args = fixture()
            reference = args[0]['pair_reference']
            if mutation == 'meaning': reference['meanings'][22] = 'hidden_delta_max'
            else: reference['hidden_history_qualified'] = True
            args[1]['objects'][1]['semantic_mapping_sha256'] = digest(independent_bytes(reference))
            rechain(args[1])
            with self.subTest(mutation=mutation): self.refused(args)

    def test_14_wall_u_and_r_profiles_are_not_silently_interchanged(self):
        args = fixture('WALL_U')
        args[0]['wall_reference'] = mapping('wall', 'WALL_R')
        self.refused(args)
        args = fixture('WALL_R')
        wall = args[1]['objects'][2]
        payload = payload_json(wall)
        payload['rows'][0] = payload['rows'][0][:6]
        replace_payload(wall, independent_bytes(payload))
        rechain(args[1])
        self.refused(args, 'NOT_COMPUTED')

    def test_15_opaque_payload_length_and_digest_are_recomputed(self):
        for index in (3,4,5):
            for mutation in ('payload', 'length', 'digest'):
                args = fixture()
                obj = args[1]['objects'][index]
                if mutation == 'payload': obj['payload_base64'] = base64.b64encode(b'changed_bytes').decode('ascii')
                elif mutation == 'length': obj['payload_bytes'] += 1
                else: obj['payload_sha256'] = 'e'*64
                rechain(args[1])
                with self.subTest(index=index, mutation=mutation): self.refused(args)

    def test_16_base64_requires_canonical_padding_and_alphabet(self):
        for encoded in ('YQ', 'YQ==\n', 'YR==', '!!!!'):
            args = fixture()
            obj = args[1]['objects'][4]
            obj.update(payload_base64=encoded, payload_bytes=1, payload_sha256=digest(b'a'))
            rechain(args[1])
            with self.subTest(encoded=encoded): self.refused(args)

    def test_17_inner_json_duplicate_key_nonfinite_and_noncanonical_bytes_reject(self):
        for data in (b'{"rows":[],"rows":[],"schema":"SYNTHETIC_S0_PAIR_PAYLOAD_V1"}',
                     b'{"rows":[[NaN]],"schema":"SYNTHETIC_S0_PAIR_PAYLOAD_V1"}',
                     b'{"rows": [[0]], "schema": "SYNTHETIC_S0_PAIR_PAYLOAD_V1"}'):
            args = fixture()
            replace_payload(args[1]['objects'][1], data)
            rechain(args[1])
            self.refused(args)

    def test_18_outer_json_duplicate_nonfinite_whitespace_and_body_hash_reject(self):
        args = fixture()
        encoded = archive_bytes(args[1])
        bad = [b' '+encoded, encoded+b'\n', b'{"schema":"x","schema":"y"}', b'{"value":NaN}']
        wrapper = json.loads(encoded.decode('utf-8'))
        wrapper['body_sha256'] = 'e'*64
        bad.append(independent_bytes(wrapper))
        for data in bad:
            with self.subTest(length=len(data)):
                with self.assertRaises(ValueError): s0.decode_s0(data, args[0], *args[2:])

    def test_19_decoder_revalidates_live_and_rejects_actual_unknown_fields(self):
        args = fixture()
        data = archive_bytes(args[1])
        args[-1][-1]['channels']['plate']['values']['velocity'][2] = 1.
        with self.assertRaises(ValueError): s0.decode_s0(data, args[0], *args[2:])
        for location in ('contract', 'envelope', 'object', 'reference'):
            args = fixture()
            obj = {'contract':args[0], 'envelope':args[1], 'object':args[1]['objects'][0],
                   'reference':args[0]['pair_reference']}[location]
            obj['execution_go'] = True
            self.refused(args)
            with self.assertRaises(ValueError): s0.serialize_s0(*args)

    def test_20_fixed_small_synthetic_byte_budgets(self):
        args = fixture()
        replace_payload(args[1]['objects'][4], b'x'*65537)
        rechain(args[1])
        self.refused(args)
        args = fixture()
        with self.assertRaises(ValueError): s0.decode_s0(b'x'*1048577, args[0], *args[2:])

    def test_21_nonbuiltin_containers_and_numbers_do_not_call_hooks(self):
        calls = []
        class TrapDict(dict):
            def items(self): calls.append('items'); raise AssertionError('hook')
        class TrapList(list):
            def __iter__(self): calls.append('iter'); raise AssertionError('hook')
        class TrapInt(int):
            def __int__(self): calls.append('int'); raise AssertionError('hook')
        class TrapString(str):
            def __str__(self): calls.append('str'); raise AssertionError('hook')
        for location in ('contract', 'envelope', 'objects', 'step', 'payload'):
            args = list(fixture())
            if location == 'contract': args[0] = TrapDict(args[0])
            elif location == 'envelope': args[1] = TrapDict(args[1])
            elif location == 'objects': args[1]['objects'] = TrapList(args[1]['objects'])
            elif location == 'step': args[1]['objects'][0]['step'] = TrapInt(96)
            else: args[1]['objects'][0]['payload_base64'] = TrapString(args[1]['objects'][0]['payload_base64'])
            self.refused(args)
        self.assertEqual(calls, [])

    def test_22_no_input_mutation_and_no_partial_acceptance(self):
        for invalid in (False, True):
            args = fixture()
            if invalid: args[1]['objects'][-1]['payload_sha256'] = 'e'*64
            before = copy.deepcopy(args)
            if invalid: self.refused(args)
            else: self.accepted(args)
            self.assertEqual(args, before)


if __name__ == '__main__':
    unittest.main()
