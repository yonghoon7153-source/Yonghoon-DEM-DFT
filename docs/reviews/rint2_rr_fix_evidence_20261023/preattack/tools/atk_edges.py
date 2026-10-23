"""Does the certificate's own topology count bind it to the cut system?  main vs end target_n_edges / n_dof vs record cut counts."""
import json, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import carbon_junction as CJ
import step3_sigma as S3
import test_carbon_junction as T
T.CJ, T.S3 = CJ, S3
KEYS = ('target_n_edges', 'target_n_dof', 'target_n_plate_bot', 'target_n_plate_top', 'target_n_through_components', 'I_bot')
res = {}
for nm, mk in (('SVX nu=0', lambda: T._qd3_svx(cert=True)),
               ('QD2-3 nu=1', lambda: T._qd3_run([T.QD2_A3, T.QD2_B3, T.QD2_C3], T.QD2_S3, T.QD2_N3)),
               ('5-rail nu=2', lambda: T._qd3_run(T.QD4_POLYS + [[(13.5, 1.5, 0.5), (13.5, 1.5, 8.5)]], T.QD4_SDCP, (15, 3, 9)))):
    reg, pl, r, c = mk()
    full = c.get('conv_cert_full') or {}
    lo = c.get('conv_cert') or {}
    up = c.get('upper') if isinstance(c.get('upper'), dict) else {}
    upc = (up or {}).get('conv_cert') or {}
    res[nm] = {'main': {k: full.get(k) for k in KEYS}, 'lower_end': {k: lo.get(k) for k in KEYS},
               'upper_end': {k: upc.get(k) for k in KEYS},
               'rec_n_sv_faces_cut': c.get('n_sv_faces_cut'),
               'upper_counts': {k: (up or {}).get(k) for k in ('n_edges_cut', 'n_plate_couplings_cut', 'n_sv_faces_cut', 'n_cells_removed')}}
print(json.dumps(res, indent=1, default=str))
