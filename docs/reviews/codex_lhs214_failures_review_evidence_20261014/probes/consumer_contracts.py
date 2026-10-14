"""Read-only pinned consumer probes; no solver, publication, seal, or ledger writes.

App functions are compiled from their exact AST nodes to avoid Flask startup.
Only module-import adapters (_tau_flux / _se_material) are provided externally.
JSON outputs are review evidence, and model-limit mutations are synthetic copies.
"""
from pathlib import Path
import ast
import copy
import json
import math
import sys

R = Path(__file__).resolve().parents[1]
S = R / 'source'
sys.dont_write_bytecode = True
for p in (R.parent / 'lhs_coverage_review_20260930/deps',
          R.parent / 'gen2_network_reverify3_20261007/deps', S / 'scripts', S / 'webapp'):
    sys.path.insert(0, str(p))
import tau_flux as tf
import pipeline_service as ps
import lhs_release_build as lrb
import se_material as sm
import network_conductivity as nc

src = S / 'webapp/app.py'
tree = ast.parse(src.read_text(encoding='utf-8'))
function_names = {'_pct_delta', '_dual_row', '_same_row', '_dual_row_strict', '_tau_block_rows',
                  '_sigma_grain_context', '_sigma_grain_mS_cm', 'transform_network_summary_4col',
                  '_ion_net_state_text', '_ion_handover_rows', '_network_state_rows'}
assignment_prefixes = ('TAU', 'ION_HANDOVER_', 'ION_NET_', 'NET_')
nodes = []
for node in tree.body:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in function_names:
        nodes.append(node)
    elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) for t in node.targets):
        if any(t.id.startswith(assignment_prefixes) for t in node.targets):
            try:
                ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            nodes.append(node)
app = {'_tau_flux': lambda: tf, '_se_material': lambda: sm}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(src), 'exec'), app)

d = R / 'submitted/lhs214_run_evidence_1014_1520/diag_lhsx054'
h = json.loads((d / 'network_conductivity_hertzian.json').read_text())
p = json.loads((d / 'network_conductivity_physics.json').read_text())
proposal = copy.deepcopy(p)
proposal.update(sigma_full_status='not_computed', sigma_full_reason='full_over_conduction',
                ionic_status='not_computed', ionic_status_reason='full_over_conduction')
dual = {'hertzian': h, 'physics': proposal}
ledger = {'thickness_um': 35.9624, 'thickness_mass_conserving_um': 36.0,
          'phi_se_mass_conserving': 0.65}
row = tf.ion_columns(dual, ledger, 100.0)

metrics = {'sigma_full_mScm': 0.6, 'sigma_full_mScm_physics': None,
           'sigma_full_status': 'computed', 'sigma_full_status_physics': 'not_computed',
           'sigma_full_reason_physics': 'full_over_conduction', 'network_solver_status': 'success',
           'sigma_ratio': 0.4, 'phi_se': 0.5, 'sigma_bulk_net_mScm': 1.0,
           'electronic_sigma_full_mScm': 2.0, 'electronic_sigma_full_mScm_physics': None}
tables = {'network_summary': {'data': []}}
app['transform_network_summary_4col'](tables, metrics, {})
selected = [r for r in tables['network_summary']['data']
            if r[0].startswith(('σ_ionic', 'σ_electronic', 'σ_brug /', 'tau2 =', 'τ_Lap,eff'))]
tables_existing = {'network_summary': {'data': [['── Network Solver (old CSV) ──', '', '', '']]}}
app['transform_network_summary_4col'](tables_existing, metrics, {})
selected_existing = [r for r in tables_existing['network_summary']['data'] if r[0].startswith('σ_brug /')]

corrupt = copy.deepcopy(proposal)
corrupt['solve_certificate_bulk_net']['residual_rel'] = 1.0
corrupt['sigma_bulk_net_status'] = 'computed'
missing_labels = copy.deepcopy(proposal)
del missing_labels['bulk_model']

diagnostic_cert = copy.deepcopy(proposal['solve_certificate_full'])
q_diag = diagnostic_cert['I_bottom'] * diagnostic_cert['g_to_q'] / diagnostic_cert['delta_V']
cert_as_numerical = copy.deepcopy(diagnostic_cert)
cert_as_numerical['status'] = 'computed'

primary_model_limit = {'case_id': 'synthetic_H0_limit', 'ion_net_status_hertz': 'NOT_COMPUTED',
                       'ion_net_status_reason_hertz': 'full_over_conduction', 'percolation_pct': '100.0'}
cols = ['case_id', 'f_ion_physics', 'tau2_ion_physics', 'tau_ion_physics',
        'ion_net_status_physics', 'ion_net_status_reason_physics']
appendix_model_limit = {'case_id': 'synthetic_P_limit', 'f_ion_physics': '', 'tau2_ion_physics': '',
                       'tau_ion_physics': '', 'ion_net_status_physics': 'NOT_COMPUTED',
                       'ion_net_status_reason_physics': 'full_over_conduction'}

result = {
    'scope': 'Actual pinned consumer functions. Synthetic post-proposal records are not production observations.',
    'ast_functions': sorted(function_names),
    'current_diagnostic_case': {'physics_sigma_status': p['sigma_full_status'],
        'physics_sigma_reason': p['sigma_full_reason'], 'physics_cert_status': diagnostic_cert['status'],
        'q_reconstructed_from_certificate': q_diag,
        'numeric_certificate_check_after_category_only_normalization': nc.certificate_problem(cert_as_numerical)},
    'proposal_on_current_consumers': {'ion_record_problem': tf.ion_record_problem(proposal),
        'channel_verdict': ps.channel_verdict(proposal, 'ionic'),
        'tau_generation': row['ion_net_generation'],
        'tau_statuses': {m: [row[f'ion_net_status_{m}'], row[f'ion_net_status_reason_{m}']] for m in tf.MODES},
        'stop_allows_sigma_status': proposal['sigma_full_status'] in ps.NETWORK_STOP_SIGMA_OK,
        'stop_allows_tau_status': row['ion_net_status_physics'] in ps.NETWORK_STOP_TAU_OK},
    'old_failure_exemptions_not_safe_for_publishable_model_limit': {
        'corrupt_CF_certificate_binding_problems': tf.certificate_binding_problems('physics', corrupt),
        'missing_bulk_model_role_problems': tf._g2_mode_problems('physics', missing_labels),
        'full_numerical_certificate_conflicts_with_unpublished_contract': tf._cert_unpublished_problem(
            'full', 'not_computed', 'full_over_conduction', diagnostic_cert)},
    'ui_new_section_rows': selected,
    'ui_existing_section_ratio_rows': selected_existing,
    'ui_model_limit_status_text': app['_ion_handover_rows'](row)[0],
    'release': {'physics_appendix_blank_check': lrb.v13_blank_problems([appendix_model_limit], cols),
        'physics_blank_definition': lrb.V13_BLANK_CODES['NOT_COMPUTED'],
        'primary_classification_with_known_percolation': lrb._v13_class(primary_model_limit)},
}
assert q_diag > 1.5
assert nc.certificate_problem(cert_as_numerical) is None
assert result['old_failure_exemptions_not_safe_for_publishable_model_limit']['corrupt_CF_certificate_binding_problems'] == []
assert result['old_failure_exemptions_not_safe_for_publishable_model_limit']['missing_bulk_model_role_problems'] == []
assert any(r[0].startswith('σ_ionic') and r[1] == r[2] == 0.6 for r in selected)
assert any(r[0].startswith('σ_electronic') and r[1] == r[2] == 2.0 for r in selected)
assert any(r[0].startswith('tau2 =') and r[2] == '—' for r in selected)
assert result['release']['physics_appendix_blank_check'] == []
(R / 'evidence/consumer_contracts.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
