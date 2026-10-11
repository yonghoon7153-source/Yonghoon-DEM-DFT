"""언로딩 검토 (10-11) 핵심 수치 — 우리 트리에서 독립 재확인 (읽기 전용 · DEM 실행 없음).
사용: python3 -I -B ul_checks_ours.py <repo> <out_json>"""
import importlib.util, json, math, sys, hashlib
from pathlib import Path
import site
sys.path.append(site.getusersitepackages())
import numpy as np
repo, out = Path(sys.argv[1]), Path(sys.argv[2])
p = repo / 'scripts/plane_load_share.py'
spec = importlib.util.spec_from_file_location('pls_ours', p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# UL-02: 중력과 정확히 평형인 5 구 사슬 (Codex 와 같은 입력을 우리 코드로 다시 씀)
n, r, rho, g = 5, 0.00051, 2000.0, 9.81
w = rho * 4 * math.pi * r**3 / 3 * g
atoms = dict(id=np.arange(1, n + 1), type=np.full(n, 3), z=(np.arange(n) + .5) * .001, radius=np.full(n, r))
fz = w * np.array([14., 13., 12., 11.])
f = np.column_stack([np.zeros(4), np.zeros(4), -fz])
res = m.compute(atoms, dict(id1=np.arange(1, 5), id2=np.arange(2, 6), f=f, fn=f), {3: 'SE'}, .005, (.05, .05, 'x'), 1000)
net = np.zeros((n, 3)); np.add.at(net, np.arange(4), f); np.add.at(net, np.arange(1, 5), -f)
inner = (atoms['z'] >= 2 * r) & (atoms['z'] <= .005 - 2 * r)
tot = net[inner].copy(); tot[:, 2] -= w
ul02 = dict(source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(), weight_N=w, balance_residual=res['balance_residual'],
            total_force_max_N=float(np.abs(tot).max()), S3_pass=res['balance_residual'] <= 1e-3)
# UL-03: 첫 교차 괄호 0.20 µm vs 등록 분해능 0.05 µm (7:3 h0 111.052 µm)
ul03 = dict(A_bracket_pct=100 * 0.20 / 111.052, B_bracket_pct=100 * 0.05 / 111.052)
# Q3 축척: 명목 개수 (덱 머리 주석 282 · 1,375 · 158,765) · 덱 면적 0.0025 m²
mass = sum(c * d * 4 * math.pi / 3 * rr**3 for c, d, rr in ((282, 4800., 4.5e-3), (1375, 4800., 2e-3), (158765, 2000., .5e-3)))
q3 = dict(mass_deck_kg=mass, weight_pressure_reported_MPa=mass * 9.81 / .0025 / 1e-3 / 1e6, g_aux_m_s2=9.81 * 1e-3 * 1e6 / 1e9)
# Q6: δ_lim 표 (덱 m6 · m7 · m8 · 반지름 µm) — δ_lim = a/(a-1)·φF·2R*
def dl(a, phi, reff): return a / (a - 1) * phi * 2 * reff
q6 = {k: dl(a, ph, re) for k, (a, ph, re) in dict(SE_SE=(5., .005, .25), AMS_SE=(3., .01, 2 * .5 / 2.5), AMP_SE=(3., .01, 4.5 * .5 / 5),
                                                  wall_SE=(3., .01, .5), AMS_AMS=(1.5, .05, 1.), AMP_AMS=(1.5, .05, 4.5 * 2 / 6.5),
                                                  AMP_AMP=(1.5, .05, 2.25)).items()}
d = dict(ul02=ul02, ul03=ul03, q3=q3, q6_delta_lim_um=q6)
out.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding='utf-8'); print(json.dumps(d, indent=1, ensure_ascii=False))
