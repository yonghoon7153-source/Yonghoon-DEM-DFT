"""Same system, same code, same thread count — does the CPU CG sigma depend on the BLAS kernel path (machine)?
Prints repr(sigma) for the step3 CG solve (production CPU path, rtol 1e-12) on the seal probe bed."""
import io, contextlib, json, os, sys
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import numpy as np
import step3_sigma as S3
import step3_conv_cert as CC
S3.GPU_SOLVE = False
S3.AMG_SOLVE = False
S3.CG_RTOL = 1e-12
S3.CG_MAXITER = 400000
out = {'coretype': os.environ.get('OPENBLAS_CORETYPE'), 'np': np.__version__}
try:
    from threadpoolctl import threadpool_info
    out['blas'] = [(d.get('internal_api'), d.get('architecture'), d.get('num_threads')) for d in threadpool_info()]
except Exception as e:  # noqa
    out['blas'] = f'threadpoolctl missing ({type(e).__name__})'
for seed in (0, 1):
    sid = CC.probe_bed(seed)
    sig = S3.electronic_sigma_table(CC.PROBE_SIGMA_AM, CC.PROBE_SIGMA_AM * 0.5, CC.PROBE_SIGMA_FIBRE, 10.0, 250.0)
    with contextlib.redirect_stdout(io.StringIO()):
        r = S3.solve_sigma_z(sid, sig, CC.PROBE_VOX, z_top_um=float(sid.shape[2]) * CC.PROBE_VOX, z_bot_um=0.0)
    out[f'seed{seed}'] = {'sigma': repr(r['sigma_eff']), 'cg_info': r.get('cg_info'), 'resid': r.get('resid')}
print(json.dumps(out))
