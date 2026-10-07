"""S1-O own static parameter arithmetic and JSON authoring; no candidate imports/tests.
Read only S0 Java text, copy constants as documented below, write own contracts.
This is NOT a COMSOL validator or a synthetic functional test runner.
"""
from decimal import Decimal, getcontext
from pathlib import Path
import hashlib
import json

getcontext().prec = 50
D = Decimal
ROOT = Path(__file__).resolve().parent
JAVA = ROOT / 'reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt'
SOURCE = 'reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt'
source_bytes = JAVA.read_bytes()
source_hash = hashlib.sha256(source_bytes).hexdigest()
LN, LS, LP = D('52e-6'), D('25e-6'), D('44e-6')
epsN = D('.63122') * (1-D('.0257219788'))
epsP = D('.58803') * (1-D('.0296398242'))
epsEN, epsEP = 1-D('.1')-epsN, 1-D('.1')-epsP
AN, AP = epsN * LN * D('31507'), epsP * LP * D('50707.7')
F = D('96485.33212')
stock0 = D('.58803')*LP*D('50707.7')*D('.927') + D('.63122')*LN*D('31507')*D('.01172068149')
dLLI = D('.003765381')*3600*D('.0439355')/F/D('1.53938e-4')
stock = stock0-dLLI
xN = D('.445')
xP = (stock-AN*xN)/AP
nN, nP = AN*xN, AP*xP
nE = (epsEN*LN+D('.45')*LS+epsEP*LP)*1200
num = lambda x: str(x)

def row(name, target, unit, absolute, relative, expression, domain, lines):
    return {'name':name,'target':num(target),'unit':unit,'abs_tol':absolute,'rel_tol':relative,
            'expression':expression,'domain_or_selection':domain,'source':f'{SOURCE}:{lines}'}

targets = [
 row('Li_N_mol_m2',nN,'mol/m^2','1e-9','1e-6','comp1.intd1(comp1.liion.epss*comp1.liion.cs_average)',[1],448),
 row('Li_P_mol_m2',nP,'mol/m^2','1e-9','1e-6','comp1.intd3(comp1.liion.epss*comp1.liion.cs_average)',[3],448),
 row('Li_electrolyte_mol_m2',nE,'mol/m^2','1e-9','1e-6','comp1.intd1(comp1.liion.epsl*comp1.cl)+comp1.intd2(comp1.liion.epsl*comp1.cl)+comp1.intd3(comp1.liion.epsl*comp1.cl)',[1,2,3],449),
 row('xavg_N',xN,'1','1e-8','1e-6','comp1.intd1(comp1.liion.cs_average)/(L_el*cs_Gr_max)',[1],450),
 row('xavg_P',xP,'1','1e-8','1e-6','comp1.intd3(comp1.liion.cs_average)/(L_pos*cs_NCM_max)',[3],450),
 row('xsurf_N_min',xN,'1','1e-8','1e-6','comp1.minsurf1(comp1.liion.socloc_surface)',[1],397),
 row('xsurf_N_max',xN,'1','1e-8','1e-6','comp1.maxsurf1(comp1.liion.socloc_surface)',[1],397),
 row('xsurf_P_min',xP,'1','1e-8','1e-6','comp1.minsurf3(comp1.liion.socloc_surface)',[3],398),
 row('xsurf_P_max',xP,'1','1e-8','1e-6','comp1.maxsurf3(comp1.liion.socloc_surface)',[3],398),
 row('ce_min',D('1200'),'mol/m^3','1e-5','1e-8','comp1.minguardall(comp1.cl)',[1,2,3],374),
 row('ce_max',D('1200'),'mol/m^3','1e-5','1e-8','cl; MaxLine over domains 1,2,3',[1,2,3],470),
 row('phis_ground_V',D('0'),'V','1e-9','1','phis at boundary 1',[1],466)
]

init = {
 'schema':'S1O_INITIALIZATION_V1','status':'OFFLINE_PROPOSAL_PARTIAL','native_ready':False,
 'source_java_sha256':source_hash,'approved':False,'usable':False,
 'purpose':'Same uniform concentration/inventory initial-value problem across sigma; finite sigma is not equilibrium.',
 'parameters_from_source':{'LAM_NE':'0.0257219788','LAM_PE':'0.0296398242','LLI':'0.0439355','T_K':'298.15','A_c_m2':'1','A_cell_m2':'0.000153938','xN':num(xN),'xP':num(xP),'ce_mol_m3':'1200','epss_N':num(epsN),'epss_P':num(epsP),'epss_short':'.55','epsl_N':num(epsEN),'epsl_P':num(epsEP),'epsl_sep':'.45'},
 'initial_stocks':{'nN_mol_m2':num(nN),'nP_mol_m2':num(nP),'nE_mol_m2':num(nE),'solid_total_mol_m2':num(stock),'all_total_mol_m2':num(stock+nE)},
 'consumer_projection':{'function':'compare_initialization','targets':targets,'comparison':'abs(observed-target)<=abs_tol AND abs(observed-target)/max(abs(target),abs_tol)<=rel_tol','all_targets_required':True},
 'paired_initial_comparison':{'nearzero_sigma_S_m':'1e-20','finite_sigmas_S_m':['1.7e-8','1.7e-7','1.7e-6'],'same_target_per_run':True,'pairwise_li_abs_tol_mol_m2':'1e-9','pairwise_x_abs_tol':'1e-8','pairwise_ce_abs_tol_mol_m3':'1e-5','pairwise_required':True,'potential_equality_required':False,'why':'Each run passes target and pairwise concentration/inventory; individual target limits do not license twice the pairwise mismatch.'},
 'profile_initial_uniformity':{'count_per_electrode':241,'N_coordinate_m':['0','0.000052'],'P_coordinate_m':['0.000077','0.000121'],'domains':{'N':1,'P':3},'fields':['x_surface','x_particle_average'],'same_target_as_electrode':True,'abs_tol':'1e-8','time_interpolation':False,'arbitrary_spatial_arithmetic_mean_is_not_electrode_average':True},
 'potential_current_observations':[
  {'name':'phis_sep_left_V','expression':'phis','selection_boundary':2,'coordinate_m':'0.000052','unit':'V','expected':'finite; sigma-specific algebraic result','source':f'{SOURCE}:460'},
  {'name':'phis_sep_right_V','expression':'phis','selection_boundary':3,'coordinate_m':'0.000077','unit':'V','expected':'finite; sigma-specific algebraic result','source':f'{SOURCE}:460'},
  {'name':'I_leak_model_A','expression':'-A_c*comp1.intd2(comp1.liion.Isx)/L_sep','unit':'A','expected':'not preset from S0 OCV; current/charge contract determines balance and resolution','source':f'{SOURCE}:457'},
  {'name':'reaction_N_A_m2','expression':'comp1.intd1(comp1.liion.ivtot)','unit':'A/m^2','expected':'RN≈j within CHARGE_BALANCE current tolerance','source':f'{SOURCE}:457'},
  {'name':'reaction_P_A_m2','expression':'comp1.intd3(comp1.liion.ivtot)','unit':'A/m^2','expected':'RP≈-j within CHARGE_BALANCE current tolerance','source':f'{SOURCE}:457'}],
 'readback_phases':[
  {'phase':'configured_pre_solve','required':['raw CDI feature properties and feature type','solver Time consistent property','CellSOCandInitialChargeInventory=0','pin1.csinit for N/P','init1.cl','resolved parameters+SI units','all three guard strings and domain selections','auto-generated solver tree identity'],'claim':'configuration only; does not prove initialization or actual effective coefficients'},
  {'phase':'consistent_initialization','time_s':'0','required':['native provenance proving consistency completed before positive integration','all consumer targets','241-point surface/particle profiles','sigma-specific potentials/currents'],'substitute_first_positive_time':False,'positive_time_only_status':'OPEN_INITIAL_STATE_NOT_OBSERVED'},
  {'phase':'completed_result','required':['actual stored time vector','native accepted steps and start/stop reason','all guard values','final fields and external completion/budget evidence'],'claim':'cannot retrospectively label input settings as observed t0'}],
 'zero_plus_policy':{'record_actual_time':True,'not_renamed_to_zero':True,'may_report_changes':True,'does_not_replace_t0_target_comparison':True,'why':'Finite-sigma state may physically change before a positive-time sample; no automatic tolerance enlargement or extrapolation.'},
 'call_budget':{'future_native_batch_max':1,'future_runAll_max':1,'CDI_generated_inside_declared_sequence':'must list solver phases and time under that call','additional_initialization_or_solve_approved':False,'if_t0_requires_extra_call':'STOP_AND_REQUEST_EXPLICIT_CALL_BUDGET_CHANGE'},
 'tolerance_status':'PROPOSED_NUMERIC_LIMITS_FOR_REVIEW_NOT_NATIVE_PASS; Li abs1e-9 and total drift1e-6 preserve prior ceilings; new init x/ce tighter limits are pre-result proposals.',
 'open_items':[{'id':'INIT_CDI_TYPE','reason':'Source creates CurrentDistributionInitialization but does not set/read actual installed CDI type. Do not invent property key.'},{'id':'INIT_CONSISTENT_STAGE','reason':'Time consistent setting getter is source evidence; successful post-consistency t0 solution extraction/provenance under one runAll is unobserved.'},{'id':'INIT_ELECTROLYTE_MAX','reason':'MaxLine configured expression exists; actual initialized all-domain maximum is not observed.'}],
 'failure_actions':'Keep first reason and stop next native phase; no modifying CDI, initial stock, sigma, or tolerances to pass.'
}

fN = epsEN ** D('2.5'); fP = epsEP ** D('2.2'); fS = D('.45') ** D('1.5')
coeff = {
 'schema':'S1O_COEFFICIENT_READBACK_V1','status':'OFFLINE_CONTRACT_ACTUAL_CONSUMPTION_OPEN','native_ready':False,'approved':False,'usable':False,
 'source_java_sha256':source_hash,
 'evidence_levels':['SOURCE_CONFIGURED','NATIVE_SETTING_READBACK','GENERATED_EQUATION_LINKED','ACTUAL_COEFFICIENT_EVALUATED'],
 'no_level_implied_by_lower_level':True,
 'adapter_projection':None,
 'adapter_projection_status':'OPEN_NOT_DIRECT_INPUT_TO_verify_coefficient_evidence',
 'configured_electronic':[
  {'feature':'comp1.liion.pcb1','domain':2,'epss':'.55','epsl':'.45','ElectricCorrModel':'NoCorr','sigma_mat':'userdef','sigma_expression':'diag(sigma_short)','sigma_unit':'S/m','proposed_multiplier':'1','expected_effective_sigma':'sigma_short','forbidden_double_factors':['.55^1.5','.45^1.5'],'actual_consumed_expression':None,'actual_consumed_variable':None,'status':'OPEN','source':f'{SOURCE}:682'},
  {'feature':'comp1.liion.pce1','domain':1,'ElectricCorrModel':'userdef','fs_expression':'epsl_el^2.5','sigma_expression':'K_gr','sigma_S_m':'100','inferred_effective_sigma_S_m':num(100*fN),'status':'FORMULA_CANDIDATE_PENDING_GENERATED_EQUATION','source':f'{SOURCE}:98'},
  {'feature':'comp1.liion.pce2','domain':3,'ElectricCorrModel':'userdef','fs_expression':'epsl_pos^b_PE_brugg','sigma_expression':'K_NCM','sigma_S_m':'.17','inferred_effective_sigma_S_m':num(D('.17')*fP),'status':'FORMULA_CANDIDATE_PENDING_GENERATED_EQUATION','source':f'{SOURCE}:98'}],
 'configured_electrolyte':[
  {'feature':'pce1','domain':1,'epsl':num(epsEN),'factor_expression':'epsl_el^2.5','factor_expected':num(fN)},
  {'feature':'pcb1','domain':2,'epsl':'.45','factor_expression':'epsl_sep^b_sep','factor_expected':num(fS)},
  {'feature':'pce2','domain':3,'epsl':num(epsEP),'factor_expression':'epsl_pos^b_PE_brugg','factor_expected':num(fP)}],
 'electrolyte_properties':{'IonicCorrModel':'userdef','fl':'factor_expression [1]','DiffusionCorrModel':'userdef','fDl':'factor_expression [1]','Migration':'userdef','fmob':'factor_expression [1]','Dl_mat':'userdef','D_e_m2_s':'7.5e-11','transpNum_mat':'userdef','t_plus':'.363','temperature_K':'298.15','ionic_material_conductivity_expression':'sigmal_int1(c/1[mol/m^3])*exp(4000/8.314*(1/(T_ref2/1[K])-1/(T3/1[K])))','ionic_material_unit':'S/m','material_reference_source':f'{SOURCE}:227','configuration_source':f'{SOURCE}:75'},
 'candidate_transport_values':[{'domain':d,'D_e_times_fDl_m2_s':num(D('7.5e-11')*factor),'D_dynamic_if_divided_by_epsl_m2_s':num(D('7.5e-11')*factor/ep),'claim':'arithmetic candidate only; generated equation determines placement and storage epsl, no extra epsl assumption'} for d,factor,ep in [(1,fN,epsEN),(2,fS,D('.45')),(3,fP,epsEP)]],
 'required_observation_record':{'phase':['configured_pre_solve','consistent_initialization','completed_result'],'fields':['run_id','variant','source_manifest_sha256','domain','feature_tag','raw_property','raw_expression','evaluated_value','unit','coefficient_symbol','equation_or_weak_term','equation_export_sha256','dependency_chain','observation_time_s','native_evaluation_source'],'missing':'OPEN_COEFFICIENT_BINDING_NOT_PASS'},
 'units_required':{'epss':'1','epsl':'1','fl':'1','fDl':'1','fmob':'1','sigma':'S/m','D_transport':'m^2/s','cl':'mol/m^3','phis':'V','Isx':'A/m^2','ivtot':'A/m^3'},
 'equality_proposals':{'factor_abs':'1e-12','factor_rel':'1e-10','sigma_abs_S_m':'1e-16','sigma_rel':'1e-6','relative_rule':'max(abs(expected), abs_floor), AND absolute/relative appropriate scale threshold; no arbitrary unit conversion','source_literal_strings':'exact and SI numeric comparison'},
 'separator_flux_crosscheck':{'formula':'j_expected = sigma_short*(phis_boundary3-phis_boundary2)/L_sep','status':'INFERRED_CONSTITUTIVE_CROSSCHECK_NOT_GENERATED_EQUATION_PROOF','current_tolerance_ref':'CHARGE_BALANCE.json/current_balance','scope':'source-free separator, uniform fixed sigma, NoCorr; actual generated equation and settings must agree','never_substitute_terminal_voltage':True,'inverse_sigma_not_research_output':True},
 'installed_api_mapping':{'audit_featureInfo_existing_source':f'{SOURCE}:114','source_audited_features':'original preflightAudit currently exports reaction per1, not whole pcb1 transport; cannot claim existing export proves binder coefficient','complete_electrolyte_and_binder_equation_export_available':False,'actual_installed_variable_names':None,'actual_cdi_property_key':None,'status':'OPEN_REQUIRES_PINNED_INSTALLED_EQUATION_OR_API_EVIDENCE_BEFORE_NATIVE_READY'},
 'mismatch_action':'STOP_AND_PRESERVE, no correction factor edits, no treating configured readback as actual consumption.'
}

charge = {
 'schema':'S1O_CHARGE_BALANCE_V1','status':'PROPOSED_LIMITS_AND_CONSUMER_RULES','native_ready':False,'approved':False,'usable':False,
 'adapter_note':'Scalar quadrature bound must cover every saved prefix for j, RN and -RP with approved raw provenance; otherwise null/INCONCLUSIVE.',
 'source_java_sha256':source_hash,'F_C_mol':num(F),'A_c_m2':'1','L_sep_m':num(LS),
 'normalized_series_schema':{'required':['time_s','j','RN','RP','I','LiN','LiP','LiE'],'units':{'time_s':'s','j':'A/m^2','RN':'A/m^2','RP':'A/m^2','I':'A','LiN':'mol/m^2','LiP':'mol/m^2','LiE':'mol/m^2'},'time':'actual exact native stored times, strictly increasing, finite, initial0 and endpoint required; no interpolation, no duplicate or invented samples'},
 'source_expressions':{'j':'-comp1.intd2(comp1.liion.Isx)/L_sep','I':'-A_c*comp1.intd2(comp1.liion.Isx)/L_sep','RN':'comp1.intd1(comp1.liion.ivtot)','RP':'comp1.intd3(comp1.liion.ivtot)','LiN':'comp1.intd1(comp1.liion.epss*comp1.liion.cs_average)','LiP':'comp1.intd3(comp1.liion.epss*comp1.liion.cs_average)','LiE':'sum domains1,2,3 comp1.intd*(comp1.liion.epsl*comp1.cl)'},
 'source_lines':f'{SOURCE}:448-458','sign_derivation':'reference/s0/notes/PHYSICS_CANDIDATE.md:28-35',
 'current_balance':{'identities':['RN-j=0','RP+j=0','RN+RP=0','I-A_c*j=0'],'absolute_A_m2':'1e-8','relative':'1e-4','scale':'max(abs(RN),abs(RP),abs(j)); never divide by nearzero j','acceptance':'abs(residual) <= 1e-8 A/m2 + 1e-4*scale; total-current threshold multiply A_c','scope':'all exact stored times including initialized0; finite units/identity required separately'},
 'charge_definitions':{'qI':'sum_i (j[i]+j[i-1])/2 * (t[i]-t[i-1])','qRN':'same actual-grid trapezoid of RN','qRP':'same actual-grid trapezoid of -RP','qN':'F_ref*(LiN[0]-LiN[t])','qP':'F_ref*(LiP[t]-LiP[0])','unit_all':'C/m^2','total_charge_conversion':'Q_model_C=A_c*q_C_m2','external_rest_charge':'0; do not compute rest coulombic efficiency from external0','experimental_current_or_capacity_conversion':'not authorized; A_cell is inventory calibration, not confirmed experimental area'},
 'charge_balance':{'identities':['qN-qP=0','qI-qN=0','qI-qP=0','qRN-qN=0','qRP-qP=0'],'absolute_C_m2':'2e-4','relative':'1e-4','scale':'max(abs(qI),abs(qN),abs(qP),abs(qRN),abs(qRP))','acceptance':'abs(residual)<=2e-4 C/m2 + 1e-4*scale AND independent quadrature adequacy for integral-dependent identities','absolute_basis':'2*F_ref*1e-9 mol/m2 = '+num(2*F*D('1e-9'))+' C/m2; rounded upward to2e-4 before results','relative_basis':'proposed1e-4 consistency allocation; not previously validated, to be fixed by reviewer before tests/main results'},
 'total_li':{'formula':'LiN+LiP+LiE','initial_targets_ref':'INITIALIZATION.json','relative_drift_limit':'1e-6','denominator':'abs(initial total Li), strictly positive, finite; no nearzero leakage denominator','failure':'LI_BALANCE_EXCEEDED distinct from quadrature uncertainty'},
 'sign_deadbands':{'current_A_m2':'1e-8','charge_C_m2':'2e-4','N_inventory_mol_m2':num(D('2e-4')/F),'P_inventory_mol_m2':num(D('2e-4')/F),'orientation':{'j':'positive leftward conventional leak','RN':'positive N oxidation/deintercalation','RP':'negative P reduction/intercalation','qN':'positive N loss','qP':'positive P gain'},'classification':{'greater_than_deadband':'RESOLVED_EXPECTED_DIRECTION','within_inclusive_deadband':'RESOLUTION_LIMITED','less_than_negative_deadband':'REVERSED_BEYOND_DEADBAND'},'zero_time':'all q exactly algebraic0; sign NOT_APPLICABLE_AT_T0, not PASS of leakage','nearzero':'may be RESOLUTION_LIMITED even with good conservation; never assert absent short from unresolved current','monotonicity':'apply to signed increment over stated actual interval with same deadband; finite-time reverse beyondband preserved, no strict monotone assertion for rounding-scale increments'},
 'quadrature':{'grid':'all actually stored times of that run, including event pre/post and exact endpoints','method':'composite trapezoid with each actual delta_t','coarsening_diagnostic':'Q_full vs every-second retained-index grid with endpoints; absolute difference is heuristic estimator only, not rigorous bound','accepted_bound_source':['independent derivative/curvature bound on every integration interval documented with units and provenance; trapezoid sum M_i*h_i^3/12','separate approved dense reference comparison with matched physics/time policy; reports empirical envelope only over checked window and no extrapolation beyond it'],'bound_allocation':'quadrature_bound <= (2e-4+1e-4*charge_scale)/4','combined_acceptance':'abs(qI-qN)+quadrature_bound <= charge_limit AND same for qP; do not enlarge limit by estimated error','unavailable_bound':'INCONCLUSIVE_QUADRATURE, not zero error/PASS','large_quadrature_proxy_with_good_inventory':'INCONCLUSIVE_QUADRATURE_NOT_PROVEN_LI_FAILURE','P0_P1_scope':'can quantify storage-induced quadrature sensitivity at common checked window only after trajectory comparison; not a bound for >120s','future_source_ODE_integral':'not automatically added; new model state changes require distinct source scope/validation/approval'},
 'states_separate':['native_completion','evidence_validity','initialization_match','current_balance','inventory_balance','quadrature_adequacy','charge_balance','direction_resolution','numerical_comparison'],
 'threshold_change_policy':'Never fitted to S0 predictions or native results; exceedances remain measured outcomes, no auto rerun.',
 'scientific_limits':'Uniform finite-sigma conductivity model; balance not proof of true Fe filament physics, experimental cell validity or spatial/temporal convergence.'
}

arithmetic = {'kind':'STATIC_PARAMETER_ARITHMETIC_NOT_MODEL_EVALUATION','decimal_precision':50,'source_sha256':source_hash,'source_parameter_lines':[623,624,625,626,627,628,629,630,631,634,636,637,638,639], 'results':{'epssN':num(epsN),'epssP':num(epsP),'epslN':num(epsEN),'epslP':num(epsEP),'AN':num(AN),'AP':num(AP),'stock0':num(stock0),'LLI_removed':num(dLLI),'stock_solid':num(stock),'xN':num(xN),'xP':num(xP),'nN':num(nN),'nP':num(nP),'nE':num(nE),'total':num(stock+nE),'flN':num(fN),'flP':num(fP),'flSep':num(fS),'charge_abs_from_two_inventory_abs':num(2*F*D('1e-9'))},'candidate_imports':0,'native_calls':0,'tests':0}
(ROOT/'contracts').mkdir(exist_ok=True)
for filename,payload in [('INITIALIZATION.json',init),('COEFFICIENT_READBACK.json',coeff),('CHARGE_BALANCE.json',charge)]:
    path=ROOT/'contracts'/filename
    if path.exists(): raise RuntimeError('Refuse overwrite: '+str(path))
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
out=ROOT/'PHYSICS_ARITHMETIC.json'
if out.exists(): raise RuntimeError('Refuse overwrite: '+str(out))
out.write_text(json.dumps(arithmetic,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(arithmetic,ensure_ascii=False))
