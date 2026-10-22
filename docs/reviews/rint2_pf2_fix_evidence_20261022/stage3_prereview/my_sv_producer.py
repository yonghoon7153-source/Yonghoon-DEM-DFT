# SV 반사실 괄호 생산자 탐침 — 손 회로와 대조
import copy, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import rint_r_chain as RRC
import ca_ext_svcf as SVCF
rj = 1e3
def run(tag, polys, sdcp_pts, N, sig=None, tamper=None, pts_lists=None):
    P = rows(polys) if pts_lists is None else rows_pts(pts_lists)
    if sdcp_pts:
        P = cat_rows(P, rows([[p] for p in sdcp_pts], phase=5, kind=0, fid0=700))
    sid, _ = bed(P, N, sdcp_sphere_d_um=0.0)
    reg = registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
    if tamper:
        tamper(reg)
    pl = plan(reg, rj, sv_counterfactual={'threshold': None})
    r = solve(sid, sig if sig is not None else sig_e(), N, pl)
    cj = r.get('cjunc') or {}
    cf = cj.get('sv_counterfactual') or {}
    proj = SVCF.sv_cf_record(cf)
    ev = {'sv_counterfactual_request': {'threshold': None}, 'solve': {'sv_counterfactual': proj}}
    prob = SVCF.sv_cf_problem(ev, True)
    view = SVCF.chain_view(proj)
    flags, _ = RRC.sv_assess({('1', 'P0', 'R_j0'): {'sv_cf': view}}, 2.0, 'R_j0')
    up = cf.get('upper') or {}
    d = {'I_full': I_of(r, N), 'reason': r.get('reason'), 'st': cf.get('status'), 'lo': cf.get('sv_counterfactual_ratio'),
         'st_hi': cf.get('status_hi'), 'hi': cf.get('sv_counterfactual_ratio_hi'), 'nu': cf.get('n_unsplit_bridging_components'),
         'up_n_cells': up.get('n_cells_removed'), 'up_edges': up.get('n_edges_cut'), 'up_plate': up.get('n_plate_couplings_cut'),
         'up_why': up.get('why'), 'Gc_lo': cf.get('G_cut_code'), 'Gc_hi': up.get('G_cut_code'), 'problem': prob, 'flags_t2': flags}
    print(tag, d)
    return d, sid, reg
# S1: two fibres share SDCP (unsplit) + independent fibre C (alternative path)
N = (5, 5, 9)
SD = [(1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (3.5, 1.5, 4.5)]
A = [(1.5, 1.5, 0.5), (1.5, 1.5, 6.5)]
B = [(3.5, 1.5, 2.5), (3.5, 1.5, 8.5)]
C = [(2.5, 4.0, 0.5), (2.5, 4.0, 8.5)]
d, sid, reg = run('S1 unsplit + alt fibre C', [A, B, C], SD, N)
# hand: chain A-SDCP-B: plate g = 200 (SV*H*H/(0.5H)), axial 100 per face; SDCP-VGCF face harmonic: 2*100*250/(350)=142.857; SDCP-SDCP 250
gA = [200.0] + [100.0]*3 + [1/(1/100.0)]  # placeholder not used
chainAB = chain_I([200.0, 100/3.0*1.0 if False else 1/(3/100.0), 142.857142857, 250/2.0, 142.857142857, 1/(3/100.0), 200.0])
chainC = chain_I([200.0, 1/(8/100.0), 200.0])
print('  hand: I_AB', chainAB, ' I_C', chainC, ' I_full_hand', chainAB + chainC, ' hi_hand', (chainAB + chainC)/chainC)
# S2: unsplit component touching top plate (A and B both pass up through SDCP at top layer)
N2 = (5, 3, 6)
SD2 = [(1.5, 1.5, 5.5), (2.5, 1.5, 5.5), (3.5, 1.5, 5.5)]
A2 = [(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)]
B2 = [(3.5, 1.5, 0.5), (3.5, 1.5, 5.5)]
run('S2 unsplit at top plate (A,B both reach top only via SDCP)', [A2, B2], SD2, N2)
# S3: census tamper (n_unsplit 0 -> 1 and 1 -> 0)
def t_up(reg): reg['census']['n_unsplit_bridging_components'] = 0
def t_dn(reg): reg['census']['n_unsplit_bridging_components'] = 2
run('S3a census says 0 (true 1)', [A, B], [(1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (3.5, 1.5, 4.5)], (5, 3, 9), tamper=t_up)
run('S3b census says 2 (true 1)', [A, B], [(1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (3.5, 1.5, 4.5)], (5, 3, 9), tamper=t_dn)
# S4: sigma_SDCP = 0 (SDCP non-conductor) -> remove dofs empty
run('S4 sigma_SDCP=0', [A, B, C], SD, N, sig=sig_e(s_sdcp=0.0))
# S5: dead-end unsplit component: A,B full-height through-fibres both passing an SDCP blob; plus they are each complete paths
A5 = [(1.5, 1.5, 0.5), (1.5, 1.5, 8.5)]
B5 = [(3.5, 1.5, 0.5), (3.5, 1.5, 8.5)]
run('S5 both fibres through-going, share SDCP (true ratio = 1 exactly?)', [A5, B5], SD, (5, 3, 9))
