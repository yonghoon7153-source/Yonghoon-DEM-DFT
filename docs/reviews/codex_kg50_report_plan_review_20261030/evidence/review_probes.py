"""Arithmetic and exact toy-network counterexamples, NOT DEM/research runs.
Only Python standard library. No repository modules, external services, or raw campaign data.
"""
import argparse, hashlib, json, math
from pathlib import Path

def gini(x):
    return sum(abs(a-b) for a in x for b in x)/(2*len(x)*sum(x))

def run():
    phi=(.15/1.64)/(.85/4.85+.15/1.64)
    gap=2/math.sqrt(3)-1
    results={
      'scope':'reviewer synthetic arithmetic; no campaign observations; no production-function verification',
      'throat':{'diameter_ratio':gap,'D_AM_um':6,'throat_um':6*gap,'D_AM_over_D_SE':[6/d for d in [3,2,1,.7]]},
      'composition':{'phi_SE_solid':phi,'phi_AM_solid':1-phi,'phi_SE_bulk_at_published_sphere_porosity_18_95pct':phi*(1-.1895),
        'phi_implied_by_rounded_D3_table':13.47*.06191/3,'tau_from_wrong_solid_phi':phi/(.06191/3),
        'solid_phi_vs_bulk_phi_bias_pct':(1/(1-.1895)-1)*100},
      'identity':{'fixed_phi':.3,'f':[.1,.2],'transport_tortuosity':[.3/.1,.3/.2],
        'variable_phi_counterexample':{'phi':[.2,.1],'f':[.04,.03],'transport_tortuosity':[.2/.04,.1/.03]}},
      'series_current':{'uniform_R_ohm':[1,1,1],'bottleneck_R_ohm':[1,98,1],
        'uniform_current_A':1/3,'bottleneck_current_A':.01,'bottleneck_all_cut_currents_A':[.01,.01,.01],
        'both_internal_node_current_gini':0.0,'bottleneck_power_fraction':.98,'sigma_ratio_same_geometry':.03},
      'edge_80pct':{'chain_edges':10,'R_each_ohm':1,'terminal_V':1,'terminal_current_A':.1,
        'sum_edge_magnitudes_A':1.,'selected_edges':8,'selected_sum_fraction':.8,'selected_subgraph_terminal_flow_A':0.},
      'node_weight':{'before_node_currents':[.8,.2],'after_second_branch_subdivision':[.8]+[.2]*9,
        'before_gini':gini([.8,.2]),'after_gini':gini([.8]+[.2]*9),'terminal_current_before_after':1.},
      'sigma_product':{'threshold_f_1_over_f_3':5.1/2.3,'threshold_f_07_over_f_3_if_sample_identity':5.1/2.25,
        'threshold_f_07_over_f_1_if_sample_identity':2.3/2.25,
        'pellet_reference_counterexample':{'intrinsic_mScm':10,'pellet_factor':.5,'measured_pellet_mScm':5,
        'same_pellet_network_fed_pellet_sigma_mScm':2.5}},
      'unknown_d2':{'synthetic_f_1_2_3':[.1,.09,.08],'sigma_scenario_low':[2.3,2.4,5.1],
        'sigma_scenario_high':[2.3,4.9,5.1],'effective_low':[.23,.216,.408],'effective_high':[.23,.441,.408],
        'max_d_low_um':3,'max_d_high_um':2},
      'surface_map':{'a_over_R':.8,'disc_over_4piR2':.8**2/4,'cap_over_4piR2':(1-math.sqrt(1-.8**2))/2,
        'cap_over_disc':2*(1-math.sqrt(1-.8**2))/.8**2},
      'overlap_union_counterexample':{'three_coincident_unit_spheres':True,'exact_union':4*math.pi/3,'sum_spheres_minus_pair_lenses':0.},
      'contact_total_area_identity':{'count':[10,20],'mean_area_um2':[.1,.05],'total_area_um2':[1.,1.]},
      'published_E_ratio_not_verified_deck_ratio':22/1.35,
      'hydrostatic_stress_counterexample':{'pressure_MPa':[10,300],'von_Mises_MPa':[0,0],'axial_compression_magnitude_MPa':[10,300]},
      'fixed_interface_counterexample':{'sigma_scale':[1,2],'R_equals_1_over_sigma_plus_1':[2,1.5],'conductance':[.5,2/3],'conductance_ratio':4/3},
    }
    checks={
      'throat_between_07_and_1':.7<6*gap<1,
      'solid_composition_closes':math.isclose(phi+(1-phi),1),
      'rounded_D3_phi_compatible_to_0001':abs(results['composition']['phi_implied_by_rounded_D3_table']-phi*(1-.1895))<.0001,
      'tortuosity_identity_inverts_f':all(math.isclose(x,y) for x,y in zip(results['identity']['transport_tortuosity'],[3,1.5])),
      'series_kcl_same_cuts':len(set(results['series_current']['bottleneck_all_cut_currents_A']))==1,
      'series_power_identity':math.isclose(.01**2*100,1*.01),
      'lorenz_same_despite_33fold_resistance':gini([1/3,1/3])==gini([.01,.01])==0,
      'edge_sum_not_terminal_flow':results['edge_80pct']['selected_sum_fraction']==.8 and results['edge_80pct']['selected_subgraph_terminal_flow_A']==0,
      'node_segmentation_changes_count_gini':not math.isclose(gini([.8,.2]),gini([.8]+[.2]*9)),
      'unknown_d2_changes_argmax':max(range(3),key=lambda i:results['unknown_d2']['effective_low'][i])!=max(range(3),key=lambda i:results['unknown_d2']['effective_high'][i]),
      'both_sigma_scenarios_monotone':all(x==sorted(x) for x in [results['unknown_d2']['sigma_scenario_low'],results['unknown_d2']['sigma_scenario_high']]),
      'sphere_cap_not_projected_disc':math.isclose(results['surface_map']['cap_over_disc'],1.25),
      'pair_lenses_not_general_union':results['overlap_union_counterexample']['exact_union']>results['overlap_union_counterexample']['sum_spheres_minus_pair_lenses'],
      'count_mean_not_independent_total':10*.1==20*.05,
      'hydrostatic_VM_does_not_measure_load':results['hydrostatic_stress_counterexample']['von_Mises_MPa'][0]==results['hydrostatic_stress_counterexample']['von_Mises_MPa'][1] and 10!=300,
      'fixed_interface_breaks_common_sigma_scaling':not math.isclose((2/3)/.5,2),
    }
    assert all(checks.values()), checks
    results['checks']=checks
    return results

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out');args=parser.parse_args()
    data=run();payload=json.dumps(data,indent=2,ensure_ascii=False)+'\n'
    if args.out:Path(args.out).write_text(payload,encoding='utf-8')
    print(payload)
