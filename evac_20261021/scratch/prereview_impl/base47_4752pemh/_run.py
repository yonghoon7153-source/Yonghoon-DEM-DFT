
import sys, json, numpy as np, contextlib, io, hashlib
sys.path.insert(0, sys.argv[1])
import step3_sigma as S
rng_seeds = [int(x) for x in sys.argv[2].split(',')]
out = {}
def bed(seed):
    rng = np.random.default_rng(seed)
    vox = 0.25; n = (24, 24, 32); box = np.array(n, float) * vox
    na = 90
    am_c = rng.uniform([0.5]*3, box - 0.5, (na, 3)); am_r = rng.uniform(0.9, 1.4, na); am_t = rng.integers(1, 3, na)
    P, PH, F, K = [], [], [], []
    for i in range(int(rng.integers(4, 8))):
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        p1 = np.clip(p0 + d * rng.uniform(2.0, 5.0), 0.05, box - 0.05)
        m = max(2, int(np.ceil(np.linalg.norm(p1 - p0) / 0.1)) + 1)
        pts = p0 + (p1 - p0) * np.linspace(0, 1, m)[:, None]
        P.append(pts); PH.append(np.full(m, 2)); F.append(np.full(m, 100 + i)); K.append(np.ones(m, int))
    sd = rng.uniform(0.2, box - 0.2, (int(rng.integers(10, 30)), 3))
    P.append(sd); PH.append(np.full(len(sd), 5)); F.append(np.arange(len(sd)) + 500); K.append(np.zeros(len(sd), int))
    P = np.vstack(P); PH = np.concatenate(PH); F = np.concatenate(F); K = np.concatenate(K)
    se = rng.uniform(0, box, (4000, 3))
    sid, pid = S.rasterize(am_c, am_r, am_t, P, PH, (0., 0., 0.), tuple(box), vox, se_pts=se, sdcp_sphere_d_um=0.5,
                           add_fid=F, add_kind=K, bridge_um=0.3)
    return sid, vox, box
for seed in rng_seeds:
    sid, vox, box = bed(seed)
    sig = S.electronic_sigma_table(0.0041, 0.0041 * 0.5, 7853.98, 10.0, 256.6)
    with contextlib.redirect_stdout(io.StringIO()):
        r = S.solve_sigma_z(sid, sig, vox, return_field=True, z_top_um=float(box[2]), z_bot_um=0.0)
    h = hashlib.sha256()
    for k in sorted(r):
        v = r[k]
        if isinstance(v, np.ndarray):
            h.update(k.encode()); h.update(np.ascontiguousarray(v).tobytes())
        else:
            h.update(k.encode()); h.update(repr(v).encode())
    out[str(seed)] = {'sigma_hex': float(r['sigma_eff']).hex(), 'keys': sorted(r), 'sha_all': h.hexdigest(),
                      'sid_sha': hashlib.sha256(sid.tobytes()).hexdigest(), 'cg_info': r.get('cg_info'), 'n_dof': r.get('n_dof')}
print(json.dumps(out))
