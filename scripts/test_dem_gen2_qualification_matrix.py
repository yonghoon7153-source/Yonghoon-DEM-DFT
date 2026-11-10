"""Tests-first qualification matrix specification; not executed at authoring.

Only the public fail-closed scaffold exists for this new module. All source and
definition values below are synthetic declarations apart from fixed dependency
pins. Freeze the P2 pin and exact dependency copies before the first red run.
No new implementation body, actual data reader, engine or authority is present.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest

source_dir = Path(__file__).parent
p2_fixture_module = types.ModuleType('fixed_synthetic_p2_fixture')
p2_fixture_module.__file__ = str(source_dir / 'test_dem_gen2_p2_contract.py')
exec(compile(Path(p2_fixture_module.__file__).read_bytes(),
    p2_fixture_module.__file__, 'exec'), p2_fixture_module.__dict__)
sys.modules['dem_gen2_p2_contract'] = p2_fixture_module.p2
matrix = types.ModuleType('dem_gen2_qualification_matrix')
matrix.__file__ = str(source_dir / 'dem_gen2_qualification_matrix.py')
exec(compile(Path(matrix.__file__).read_bytes(), matrix.__file__, 'exec'), matrix.__dict__)

# The only pending dependency pin, to be replaced before freezing the red suite.
P2_PIN = 'c571a27119ace92ca34d3d6f2b61135219a3f1b4'
S0_PIN = 'f4647f2b7c218a6df7def3292c092273f9d4e35f'


def encoded(value, ascii_only=False):
    return json.dumps(value, sort_keys=True, ensure_ascii=ascii_only,
        separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(value).hexdigest()


def _change_attempt(value, attempt):
    """Fixture setup only: change every nested declaration before freezing."""
    if type(value) is dict:
        for key in value:
            if key == 'attempt_id': value[key] = attempt
            else: _change_attempt(value[key], attempt)
    elif type(value) is list:
        for member in value: _change_attempt(member, attempt)


def p2_fixture(grid, attempt):
    """Rebind invented inputs in dependency order; do not invent observations.

Changing attempt labels requires original T0/T11/LIVE/S0 bytes to be rebound.
The already fixed LIVE/S0 contracts provide the boundary, not the new matrix.
"""
    plan, archive, context, trace = p2_fixture_module.fixture(grid_choice=grid)
    _change_attempt(plan, attempt)
    _change_attempt(context, attempt)
    _change_attempt(trace, attempt)
    live_plan = context['live_plan']
    t11 = live_plan['t11_plan']
    t11_context = live_plan['t11_context']
    t0_hash = digest(encoded(dict(synthetic_plan=t11_context['t0_plan'],
        synthetic_controls=t11_context['t0_controls']), ascii_only=True))
    t11_context['expected_t0_packet_sha256'] = t0_hash
    t11['t0_binding']['packet_sha256'] = t0_hash
    t11_hash = digest(encoded(t11, ascii_only=True))
    t11_context['expected_plan_sha256'] = t11_hash
    for frame in context['servo_frames'] + context['ra_frames']:
        frame['source_identity'].update(t0_packet_sha256=t0_hash, t11_plan_sha256=t11_hash)
    live = p2_fixture_module.s0_fixture_module.live
    result = live.diagnose_live_ra(live_plan, context['servo_frames'], context['ra_frames'])
    if result['status'] != 'SYNTHETIC_RA_END_CANDIDATE':
        raise AssertionError('Fixed LIVE dependency fixture failed during input setup')
    boundary = result['boundary_candidate']
    envelope = json.loads(archive.decode('utf-8'))['body']
    envelope['boundary_candidate'] = boundary
    boundary_hash = digest(encoded(boundary))
    context['s0_contract']['boundary_sha256'] = boundary_hash
    for obj in envelope['objects']: obj['boundary_sha256'] = boundary_hash
    p2_fixture_module.s0_fixture_module.rechain(envelope)
    archive = p2_fixture_module.s0_fixture_module.archive_bytes(envelope)
    archive_hash = digest(archive)
    context['expected_s0_sha256'] = archive_hash
    plan['header']['s0_sha256'] = archive_hash
    p2_fixture_module.refreeze(plan, context)
    for record in trace:
        record.update(s0_sha256=archive_hash, plan_sha256=context['expected_plan_sha256'])
    return plan, archive, context, trace


def refreeze(plan, context):
    """Synthetic plan setup before observations; not an operating seal."""
    context['expected_plan_sha256'] = digest(encoded(plan))


def fixture():
    source = dict(evidence_kind='SYNTHETIC_SOURCE_DECLARATIONS', p2_contract_pin=P2_PIN,
        s0_contract_pin=S0_PIN, producer_pin='a'*40, consumer_definition_pin='e'*40,
        qualification_definition_id='toy_qualification_definition')
    rows = [('coarse_complete', 'coarse', 'toy_attempt_coarse', 'POSITIVE'),
            ('half_complete', 'half', 'toy_attempt_half', 'POSITIVE'),
            ('partial_control', 'coarse', 'toy_attempt_partial', 'EXPECTED_NEGATIVE')]
    packets, cases, attempts = [], [], []
    initial = None
    for case_id, grid, attempt, role in rows:
        p, b, c, trace = p2_fixture(grid, attempt)
        envelope = json.loads(b.decode('utf-8'))['body']
        boundary = envelope['boundary_candidate']
        objects = {obj['role']: obj for obj in envelope['objects']}
        if initial is None:
            initial = dict(scope='ATOM_MESH_RESTART_DECLARED_BYTES_V1',
                atom_payload_sha256=objects['atom']['payload_sha256'],
                mesh_payload_sha256=objects['mesh']['payload_sha256'],
                restart_payload_sha256=objects['restart']['payload_sha256'],
                history_id=boundary['plate']['history_id'])
        if role == 'EXPECTED_NEGATIVE': trace.pop()
        packets.append(dict(case_id=case_id, source_manifest=copy.deepcopy(source),
            p2_plan=p, s0_bytes=b, p2_context=c, trace=trace))
        cases.append(dict(case_id=case_id, role=role, expected_attempt_id=attempt,
            expected_grid_choice=grid, expected_run_id=p['identity']['run_id'],
            expected_definition_id=p['identity']['definition_id'],
            expected_plan_sha256=c['expected_plan_sha256'], expected_s0_sha256=digest(b),
            expected_status='SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE' if role=='POSITIVE' else 'INCOMPLETE',
            expected_reason='SYNTHETIC_SEQUENCE_AND_TOY_LIMITS_ONLY' if role=='POSITIVE'
                            else 'SEPARATION_OR_POST_BUDGET_INCOMPLETE'))
        parent = 'toy_attempt_coarse' if role=='EXPECTED_NEGATIVE' else None
        attempts.append(dict(attempt_id=attempt, case_id=case_id,
            parent_attempt_id=parent,
            parent_checkpoint_sha256=initial['restart_payload_sha256'] if parent else None,
            parent_checkpoint_step=96 if parent else None,
            checkpoint_sha256=objects['restart']['payload_sha256'],
            checkpoint_step=boundary['end_step'], stage='RA_END',
            start_step=boundary['end_step'], planned_end_step=208 if grid=='coarse' else 416,
            dt_seconds=[1,8] if grid=='coarse' else [1,16],
            terminal_state='DECLARED_COMPLETE' if role=='POSITIVE' else 'DECLARED_PARTIAL'))
    plan = dict(schema='DEM_GEN2_QUALIFICATION_MATRIX_V1', purpose='SYNTHETIC_PREPARATION',
        evidence_kind='SYNTHETIC_CASE_MATRIX', assumptions=['Q-QUAL-A', 'Q-QUAL-B'],
        plan_id='toy_qualification_matrix', revision=1, source_manifest=source,
        cases=cases, attempts=attempts,
        time_pair=dict(coarse_case_id='coarse_complete', half_case_id='half_complete',
            start_seconds=[12,1], end_seconds=[26,1], window_seconds=[2,1],
            initial_state=initial))
    context = dict(schema='FROZEN_SYNTHETIC_QUALIFICATION_CONTEXT_V1',
        p2_contract_pin=P2_PIN, expected_source_manifest=copy.deepcopy(source),
        expected_plan_sha256=digest(encoded(plan)), freeze_ordinal=10, first_observation_ordinal=11)
    return plan, packets, context


class QualificationMatrix(unittest.TestCase):
    def authority_off(self, result):
        for key in ('physical_ready','execution_go','transition_authorized','gate_write',
                    'operational_seal_modified','registration_complete','source_authenticated',
                    'hidden_history_qualified'):
            self.assertIs(result[key], False)
        for key in ('actual_qualification','actual_T0','actual_T2','actual_T5','actual_T10',
                    'actual_T11','actual_T12','actual_T13'):
            self.assertEqual(result[key], 'NOT_RUN')
        self.assertIsNone(result['actual_binary_identity'])
        self.assertIsNone(result['actual_S0'])
        self.assertEqual(result['review_status'], 'NOT_RECEIVED')
        self.assertEqual(result['research_results'], 0)
        self.assertEqual(result['whole_status'], 'HOLD')
        self.assertEqual(result['assumptions'], ['Q-QUAL-A','Q-QUAL-B'])

    def check(self, args, status):
        result = matrix.validate_qualification_matrix(*args)
        self.assertEqual(result['status'], status, result)
        self.authority_off(result)
        return result

    def test_01_complete_fixed_case_matrix_is_only_synthetic(self):
        result = self.check(fixture(), 'SYNTHETIC_MATRIX_CONSISTENT')
        self.assertEqual((result['planned_cases'], result['received_cases'],
            result['checked_cases'], result['matched_expectations']), (3,3,3,3))
        self.assertEqual(result['missing_case_ids'], [])
        self.assertEqual(result['lineage_status'], 'SYNTHETIC_LINEAGE_CONSISTENT')
        self.assertEqual(result['dt_pair_status'], 'SYNTHETIC_TIME_PAIR_CONSISTENT')
        negative = next(row for row in result['case_results'] if row['case_id']=='partial_control')
        self.assertEqual(negative['observed_status'], 'INCOMPLETE')
        self.assertTrue(negative['meets_expectation'])
        self.assertFalse(negative['synthetic_case_complete'])

    def test_02_input_unchanged_and_packet_order_does_not_choose_winner(self):
        args = fixture()
        args[1].reverse()
        before = copy.deepcopy(args)
        result = self.check(args, 'SYNTHETIC_MATRIX_CONSISTENT')
        self.assertEqual([row['case_id'] for row in result['case_results']],
                         ['coarse_complete','half_complete','partial_control'])
        self.assertEqual(args, before)

    def test_03_packet_source_pin_cannot_be_stale(self):
        for key in ('p2_contract_pin','s0_contract_pin','producer_pin','consumer_definition_pin'):
            args = fixture()
            args[1][0]['source_manifest'][key] = 'f'*40
            with self.subTest(key=key): self.check(args, 'REJECTED')

    def test_04_refreezing_plan_does_not_replace_external_source_manifest(self):
        args = fixture()
        args[0]['source_manifest']['consumer_definition_pin'] = 'f'*40
        for packet in args[1]: packet['source_manifest']['consumer_definition_pin'] = 'f'*40
        refreeze(args[0], args[2])
        self.check(args, 'REJECTED')

    def test_05_case_identity_and_definition_are_bound_to_original_p2(self):
        for key in ('expected_attempt_id','expected_run_id','expected_definition_id'):
            args = fixture()
            args[0]['cases'][0][key] = 'other_identity'
            refreeze(args[0], args[2])
            with self.subTest(key=key): self.check(args, 'REJECTED')

    def test_06_original_live_input_is_rechecked(self):
        args = fixture()
        args[1][0]['p2_context']['ra_frames'][-1]['channels']['plate']['values']['velocity'][2] = 1.
        self.check(args, 'REJECTED')

    def test_07_original_s0_bytes_are_rechecked(self):
        args = fixture()
        args[1][0]['s0_bytes'] += b'\n'
        self.check(args, 'REJECTED')

    def test_08_pass_receipt_cannot_replace_original_p2_inputs(self):
        args = fixture()
        args[1][0]['p2_plan'] = dict(status='PASS', rc=0, physical_ready=True)
        self.check(args, 'REJECTED')
        args = fixture()
        args[1][0]['status'] = 'PASS'
        self.check(args, 'REJECTED')

    def test_09_missing_cases_keep_the_complete_planned_denominator(self):
        for count in (0,2):
            plan, packets, context = fixture()
            result = self.check((plan, packets[:count], context), 'INCOMPLETE')
            self.assertEqual(result['planned_cases'], 3)
            self.assertEqual(result['received_cases'], count)
            self.assertEqual(len(result['missing_case_ids']), 3-count)

    def test_10_duplicate_or_unknown_case_is_not_selected_away(self):
        for mutation in ('duplicate','unknown'):
            args = fixture()
            if mutation=='duplicate': args[1].append(copy.deepcopy(args[1][0]))
            else: args[1][0]['case_id'] = 'unplanned_case'
            with self.subTest(mutation=mutation): self.check(args, 'REJECTED')

    def test_11_partial_positive_is_not_completed_by_rc_or_end_label(self):
        args = fixture()
        args[1][0]['trace'].pop()
        result = self.check(args, 'INCOMPLETE')
        self.assertEqual(result['planned_cases'], 3)
        row = next(r for r in result['case_results'] if r['case_id']=='coarse_complete')
        self.assertEqual(row['observed_status'], 'INCOMPLETE')
        self.assertFalse(row['meets_expectation'])

    def test_12_technical_failure_is_not_expected_partial_control_success(self):
        args = fixture()
        args[1][2]['trace'][0]['identity']['attempt_id'] = 'other_attempt'
        self.check(args, 'REJECTED')

    def test_13_expected_negative_cannot_silently_become_full_positive(self):
        args = fixture()
        unused_plan, unused_archive, unused_context, full_trace = p2_fixture('coarse','toy_attempt_partial')
        args[1][2]['trace'] = full_trace
        self.check(args, 'REJECTED')

    def test_14_parent_checkpoint_hash_and_step_are_required(self):
        for key, value in (('parent_checkpoint_sha256','f'*64), ('parent_checkpoint_step',95)):
            args = fixture()
            args[0]['attempts'][2][key] = value
            refreeze(args[0], args[2])
            with self.subTest(key=key): self.check(args, 'REJECTED')

    def test_15_parent_cycles_unknown_parent_and_duplicate_attempt_refuse(self):
        for mutation in ('cycle','unknown','duplicate'):
            args = fixture()
            if mutation=='cycle': args[0]['attempts'][2]['parent_attempt_id'] = 'toy_attempt_partial'
            elif mutation=='unknown': args[0]['attempts'][2]['parent_attempt_id'] = 'unknown_attempt'
            else: args[0]['attempts'].append(copy.deepcopy(args[0]['attempts'][0]))
            refreeze(args[0], args[2])
            with self.subTest(mutation=mutation): self.check(args, 'REJECTED')

    def test_16_failed_parent_keeps_valid_checkpoint_and_failure_separate(self):
        args = fixture()
        args[0]['attempts'][0]['terminal_state'] = 'DECLARED_FAILED'
        refreeze(args[0], args[2])
        result = self.check(args, 'INCOMPLETE')
        self.assertEqual(result['lineage_status'], 'SYNTHETIC_LINEAGE_CONSISTENT')
        parent = next(r for r in result['case_results'] if r['case_id']=='coarse_complete')
        self.assertEqual(parent['attempt_terminal_state'], 'DECLARED_FAILED')
        self.assertFalse(parent['synthetic_case_complete'])

    def test_17_restart_start_and_current_checkpoint_bind_to_s0(self):
        for key, value in (('checkpoint_sha256','f'*64), ('checkpoint_step',95),
                           ('start_step',95), ('stage','SERVO_END')):
            args = fixture()
            args[0]['attempts'][2][key] = value
            refreeze(args[0], args[2])
            with self.subTest(key=key): self.check(args, 'REJECTED')

    def test_18_old_attempt_observations_do_not_complete_new_attempt(self):
        args = fixture()
        args[1][2]['trace'] = copy.deepcopy(args[1][0]['trace'])
        self.check(args, 'REJECTED')

    def test_19_declared_half_dt_must_match_inner_grid(self):
        args = fixture()
        args[0]['attempts'][1]['dt_seconds'] = [1,8]
        refreeze(args[0], args[2])
        self.check(args, 'REJECTED')

    def test_20_same_physical_time_is_not_same_step_count(self):
        for mutation in ('same_steps','wrong_physical_end','wrong_window'):
            args = fixture()
            if mutation=='same_steps': args[0]['attempts'][1]['planned_end_step'] = 208
            elif mutation=='wrong_physical_end': args[0]['time_pair']['end_seconds'] = [13,1]
            else: args[0]['time_pair']['window_seconds'] = [1,1]
            refreeze(args[0], args[2])
            with self.subTest(mutation=mutation): self.check(args, 'REJECTED')

    def test_21_initial_state_scope_is_explicit_not_whole_archive_equality(self):
        args = fixture()
        self.assertNotEqual(args[1][0]['s0_bytes'], args[1][1]['s0_bytes'])
        self.check(args, 'SYNTHETIC_MATRIX_CONSISTENT')
        for key in ('atom_payload_sha256','mesh_payload_sha256','restart_payload_sha256','history_id'):
            args = fixture()
            args[0]['time_pair']['initial_state'][key] = 'other_history' if key=='history_id' else 'f'*64
            refreeze(args[0], args[2])
            with self.subTest(key=key): self.check(args, 'REJECTED')

    def test_22_frozen_plan_and_preobservation_order_cannot_be_bypassed(self):
        args = fixture()
        args[0]['revision'] = 2
        self.check(args, 'REJECTED')
        args = fixture()
        args[2]['freeze_ordinal'] = args[2]['first_observation_ordinal']
        self.check(args, 'REJECTED')

    def test_23_exact_types_and_no_object_hooks(self):
        calls = []
        class TrapInt(int):
            def __int__(self): calls.append('int'); raise AssertionError('hook')
            def __eq__(self, other): calls.append('eq'); raise AssertionError('hook')
        class TrapDict(dict):
            def items(self): calls.append('items'); raise AssertionError('hook')
        for value in (True, 1., TrapInt(1)):
            args = fixture()
            args[0]['attempts'][0]['start_step'] = value
            with self.subTest(kind=type(value).__name__): self.check(args, 'REJECTED')
        args = list(fixture())
        args[0] = TrapDict(args[0])
        self.check(args, 'REJECTED')
        self.assertEqual(calls, [])

    def test_24_actual_evidence_or_authority_claims_are_not_synthetic_go(self):
        args = fixture()
        args[0]['evidence_kind'] = 'ACTUAL_QUALIFICATION_RECEIPT'
        refreeze(args[0], args[2])
        self.check(args, 'REJECTED')
        for key in ('execution_go','registration_complete','hidden_history_qualified'):
            args = fixture()
            args[0][key] = True
            with self.subTest(key=key): self.check(args, 'REJECTED')

    def test_25_declared_failed_or_partial_attempt_is_never_complete(self):
        for state in ('DECLARED_PARTIAL','DECLARED_FAILED'):
            args = fixture()
            args[0]['attempts'][1]['terminal_state'] = state
            refreeze(args[0], args[2])
            result = self.check(args, 'INCOMPLETE')
            row = next(r for r in result['case_results'] if r['case_id']=='half_complete')
            self.assertFalse(row['synthetic_case_complete'])


if __name__ == '__main__':
    unittest.main()
