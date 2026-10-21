# -*- coding: utf-8 -*-
"""탐침 C1 — 새 노브를 다 끄면 (cjunc · face_alpha · CONV_CERT 끔) solve_sigma_z 결과가 기반 47d23baba 와 바이트 같은가.
기반 판 step3_sigma · carbon_junction · step3_conv_cert · ptfe_face_alpha 를 git show 로 따로 모듈화해 같은 프로세스에서 비교.
CG = 생산 `_solve_cg` (CPU Jacobi) 그대로 — 같은 행렬 · 같은 BLAS 면 같은 비트여야 한다.  + face_alpha 켬 (계획 지문 · σ) 대조."""
import importlib.util
import os
import subprocess
import sys
import tempfile
REPO = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
import json

BASE = 'a76f59d0d'
tmpd = tempfile.mkdtemp(prefix='a2base_', dir='/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2')
arc = subprocess.run(['git', '-C', REPO, 'archive', BASE, 'scripts'], capture_output=True, check=True).stdout
import io as _io, tarfile as _tf
with _tf.open(fileobj=_io.BytesIO(arc)) as t:
    t.extractall(tmpd, filter='data')
base_scripts = os.path.join(tmpd, 'scripts')
# 기반 모듈은 자기 이름으로 서로 import 하므로 별도 프로세스 없이 이름 충돌을 피하려 하위 프로세스에서 기반을 돌린다
CODE = r'''
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
'''
code_path = os.path.join(tmpd, '_run.py')
with open(code_path, 'w', encoding='utf-8') as fh:
    fh.write(CODE)
seeds = '1,2,3,4,5'
env = dict(os.environ)
res = {}
for tag, d in (('base_a76f59d0d', base_scripts), ('head', os.path.join(REPO, 'scripts'))):
    p = subprocess.run([sys.executable, '-I', code_path, d, seeds], capture_output=True, text=True, env=env, timeout=600)
    res[tag] = json.loads(p.stdout.strip().splitlines()[-1]) if p.returncode == 0 else {'err': p.stderr[-2000:]}
same = {s: res['base_a76f59d0d'].get(s) == res['head'].get(s) for s in seeds.split(',')}
print('base', res['base_a76f59d0d'])
print('head', res['head'])
print('byte-same per seed (모든 결과 칸 sha · σ hex · sid sha):', same)
json.dump({'res': res, 'same': same}, open('/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/logs/off_bitid.json', 'w'), indent=1)
import shutil
shutil.rmtree(tmpd, ignore_errors=True)
