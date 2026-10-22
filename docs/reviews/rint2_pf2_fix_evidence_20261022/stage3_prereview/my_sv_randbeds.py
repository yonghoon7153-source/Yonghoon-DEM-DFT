import contextlib, io, json, math, os, sys
import numpy as np
REPO = os.environ['PRE_REPO']; sys.path.insert(0, os.path.join(REPO, 'scripts'))
import step3_sigma as S3
import carbon_junction as CJ
import ca_ext_svcf as SV
import rint_r_chain as RRC
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_sv_unsplit_freq.py')).read().split('def bed(')[0].split('VOX = 0.15')[1].join(['VOX = 0.15', '']) if False else '')
VOX = 0.15; NBOX = 24; BOX = NBOX * VOX
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_sv_unsplit_freq.py')).read()
fib_src = src[src.index('def fibre(rng):'):src.index('def bed(seed')]
exec(fib_src)
from scipy.sparse.linalg import spsolve
old = S3._solve_cg
S3._solve_cg = lambda L, b, *a, **k: (spsolve(L.tocsc(), b), 0)
out = {}
for n_fib, n_sdcp, seeds in ((60, 6, range(6)), (90, 10, range(4))):
    for seed in seeds:
        rng = np.random.default_rng(seed)
        P, PH, F, K = [], [], [], []
        f = 100
        while f < 100 + n_fib:
            s = fibre(rng)
            if s is None:
                continue
            P.append(s); PH.append(np.full(len(s), 2)); F.append(np.full(len(s), f)); K.append(np.ones(len(s), int)); f += 1
        sd = rng.uniform(0.5, BOX - 0.5, (n_sdcp, 3))
        P.append(sd); PH.append(np.full(n_sdcp, 5)); F.append(np.arange(n_sdcp) + 900); K.append(np.zeros(n_sdcp, int))
        P = np.vstack(P); PH = np.concatenate(PH).astype(np.int64); F = np.concatenate(F).astype(np.int64); K = np.concatenate(K).astype(np.int64)
        sid, _ = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P, PH, (0.0, 0.0, 0.0), (BOX, BOX, BOX), VOX,
                              sdcp_sphere_d_um=1.0, add_fid=F, add_kind=K, bridge_um=0.48)
        with contextlib.redirect_stdout(io.StringIO()):
            reg = CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), VOX, P, PH, F, K, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30,
                                    r_port_um=0.30, s_min_um=0.3, tol_sj_um=0.03, r_sdcp_um=0.15)
        tag = f'fib{n_fib}_sdcp{n_sdcp}_s{seed}'
        if reg.get('rejections'):
            out[tag] = {'rejections': [x['code'] for x in reg['rejections']]}; print(tag, out[tag]); continue
        try:
            pl = CJ.cjunc_plan(reg, 1e6, unreg_law='cut', ptfe_stamp='off', sv_counterfactual={'threshold': None})
            sig = S3.electronic_sigma_table(0.0041, 0.0041 * 0.5, 7853.98, 10.0, 256.6)
            with contextlib.redirect_stdout(io.StringIO()):
                r = S3.solve_sigma_z(sid, sig, VOX, z_top_um=BOX, z_bot_um=0.0, cjunc=pl)
        except Exception as e:
            out[tag] = {'exc': f'{type(e).__name__}: {e}'[:200]}; print(tag, out[tag]); continue
        cf = (r.get('cjunc') or {}).get('sv_counterfactual') or {}
        proj = SV.sv_cf_record(cf)
        prob = SV.sv_cf_problem({'sv_counterfactual_request': {'threshold': None}, 'solve': {'sv_counterfactual': proj}}, True)
        v = SV.chain_view(proj)
        fl = RRC.sv_assess({('1', 'P0', 'R_j0'): {'sv_cf': v}}, 2.0, 'R_j0')[0]
        up = cf.get('upper') or {}
        d = {'reason': r.get('reason'), 'sigma': r.get('sigma_eff'), 'nu': cf.get('n_unsplit_bridging_components'), 'nb': cf.get('n_bridging_components'),
             'st': cf.get('status'), 'lo': cf.get('sv_counterfactual_ratio'), 'st_hi': cf.get('status_hi'), 'hi': cf.get('sv_counterfactual_ratio_hi'),
             'up_cells': up.get('n_cells_removed'), 'up_why': (up.get('why') or '')[:60], 'problem': prob, 'flags': fl}
        out[tag] = d; print(tag, d, flush=True)
S3._solve_cg = old
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_sv_randbeds.json'), 'w'), ensure_ascii=False, indent=1, default=str)
