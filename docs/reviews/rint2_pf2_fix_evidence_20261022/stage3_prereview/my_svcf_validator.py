# 검증기 (sv_cf_problem) 괄호 칸 변이 — 정상 기록 하나에서 한 칸씩
import copy, json, math, os, sys
REPO = os.environ['PRE_REPO']; sys.path.insert(0, os.path.join(REPO, 'scripts'))
import ca_ext_svcf as SV
import rint_r_chain as RRC
cert = {'version': 'v', 'status': 'POSITIVE_SOLVED', 'ok': True, 'pass_a': True, 'pass_b': True, 'pass_c': True, 'pass_d': True}
def raw(nu=0, lo_gc=5.0, hi_gc=None, gf=10.0):
    r = {'kind': 'counterfactual_cut_sv_bridges_keep_self_v1', 'rule': 'x', 'requested': True, 'threshold': None,
         'n_sv_faces_cut': 1, 'n_unsplit_bridging_components': nu, 'G_full_code': gf, 'G_cut_code': lo_gc,
         'sv_counterfactual_ratio': gf / lo_gc, 'flag': None, 'cg_info': 0, 'resid': 1e-12, 'conv_cert': dict(cert),
         'status': 'computed', 'backend_last_solve': None, 'bracket_rule': 'lower_keep_unsplit_upper_remove_unsplit_sdcp_cells_v1'}
    if nu == 0:
        r.update(upper=None, status_hi='computed', sv_counterfactual_ratio_hi=r['sv_counterfactual_ratio'])
    else:
        up = {'status': 'computed', 'G_cut_code': hi_gc, 'sv_counterfactual_ratio': gf / hi_gc, 'cg_info': 0, 'resid': 1e-12,
              'conv_cert': dict(cert), 'backend_last_solve': None, 'why': None, 'n_components_removed': nu, 'n_cells_removed': 3,
              'n_edges_cut': 4, 'n_plate_couplings_cut': 0, 'n_sv_faces_cut': 1}
        r.update(upper=up, status_hi='computed', sv_counterfactual_ratio_hi=gf / hi_gc)
    return r
def check(tag, rec, expect_reject):
    ev = {'sv_counterfactual_request': {'threshold': None}, 'solve': {'sv_counterfactual': SV.sv_cf_record(rec)}}
    p = SV.sv_cf_problem(ev, True)
    v = SV.chain_view(ev['solve']['sv_counterfactual'])
    fl, _ = RRC.sv_assess({('1', 'P0', 'R_j0'): {'sv_cf': v}}, 2.0, 'R_j0')
    ok = (p is not None) == expect_reject
    print(f"{'OK ' if ok else 'XX '} {tag:58s} reject={p is not None} want_reject={expect_reject} flags={fl} lo={v['ratio']} hi={v['ratio_hi']} :: {str(p)[:110]}")
    return ok
res = []
res.append(check('normal nu=0', raw(), False))
res.append(check('normal nu=1 (lo 2.0 · hi 4.0)', raw(1, 5.0, 2.5), False))
m = raw(1, 5.0, 2.5); m['upper']['n_components_removed'] = 7
res.append(check('nu=1 but upper.n_components_removed=7', m, True))
m = raw(1, 5.0, 2.5); m['upper']['conv_cert'] = None
res.append(check('nu=1 upper conv_cert None (lower has cert)', m, True))
m = raw(); m['conv_cert'] = None
res.append(check('nu=0 lower conv_cert None', m, True))
m = raw(); m['conv_cert'] = 'failed'
res.append(check('nu=0 lower conv_cert = "failed" (non-dict)', m, True))
m = raw(); m['conv_cert'] = {'status': 'POSITIVE_SOLVED', 'ok': True, 'pass_a': True, 'pass_b': True, 'pass_c': True, 'pass_d': True, 'version': 'other-run'}
res.append(check('nu=0 cert from other solve (flags only)', m, False))
m = raw(1, 5.0, 2.5); m['n_unsplit_bridging_components'] = True
res.append(check('nu=True (bool)', m, True))
m = raw(1, 5.0, 2.5); m['n_unsplit_bridging_components'] = 10**400
res.append(check('nu=10**400 (upper dict present)', m, True))
m = raw(1, 5.0, 2.5); m['n_unsplit_bridging_components'] = 1.0
res.append(check('nu=1.0 float', m, True))
m = raw(1, 5.0, 5.0 * 1.00005)
res.append(check('hi slightly < lo (within floor)', m, False))
m = raw(1, 5.0, 6.0)
res.append(check('hi < lo by 17% (inverted bracket)', m, True))
m = raw(); m['G_full_code'] = 10; 
res.append(check('G_full int 10 (proj→float)', m, False))
m = raw(); m['sv_counterfactual_ratio'] = 2.0 * (1 + 3e-12); m['sv_counterfactual_ratio_hi'] = m['sv_counterfactual_ratio']
res.append(check('ratio off by 3e-12 rel', m, True))
m = raw(); m['status_hi'] = 'computed '; 
res.append(check('status_hi trailing space (nu=0)', m, True))
m = raw(1, 5.0, 2.5); m['upper']['status'] = 'no_through_without_sv'; m['upper']['G_cut_code'] = 0.0; m['upper']['sv_counterfactual_ratio'] = math.inf; m['status_hi'] = 'no_through_without_sv'; m['sv_counterfactual_ratio_hi'] = math.inf
res.append(check('upper no_through (inf) normal', m, False))
m2 = copy.deepcopy(m); m2['upper']['G_cut_code'] = 1e-300
res.append(check('upper no_through but G_cut 1e-300', m2, True))
m = raw(1, 5.0, 2.5); m['upper']['status'] = 'unsplit_census_mismatch'; m['upper']['G_cut_code'] = None; m['upper']['sv_counterfactual_ratio'] = None; m['status_hi'] = 'unsplit_census_mismatch'; m['sv_counterfactual_ratio_hi'] = None
res.append(check('upper census mismatch (expect accept, chain UNCHECKED)', m, False))
m = raw(1, 5.0, 2.5); m['status_hi'] = 'computed'; m['sv_counterfactual_ratio_hi'] = 4.0; m['upper']['sv_counterfactual_ratio'] = 4.0; m['upper']['G_cut_code'] = 2.5
res.append(check('normal again', m, False))
m = raw(1, 5.0, 2.5); m['G_full_code'] = 10.0; m['upper']['G_full_code'] = 99.0
res.append(check('upper carries its own G_full 99 (ignored?)', m, False))
m = raw(1, 5.0, 2.5); m['status'] = 'unconverged'; m['sv_counterfactual_ratio'] = None; m['G_cut_code'] = None
res.append(check('lower unconverged, hi 4.0 (chain should UNCHECKED)', m, False))
m = raw(1, 5.0, 2.5); m['status'] = 'unconverged'; m['sv_counterfactual_ratio'] = None; m['G_cut_code'] = None; m['upper']['G_cut_code']=8.0; m['upper']['sv_counterfactual_ratio']=1.25; m['sv_counterfactual_ratio_hi']=1.25
res.append(check('lower unconverged, hi 1.25 <= t', m, False))
print('n_ok', sum(res), '/', len(res))
