# -*- coding: utf-8 -*-
"""탐침 2-A″ (PRE2-impl-01 · payload 끝-끝) — 실제 `mpm_webapp_payload.py` (b6 고정물 꼴 · vox 1 µm · SE 절연 채움 · AM 작은 구 둘 · 판 밖)
에 '두 섬유가 같은 SDCP 성분을 지나는' 침대를 넣고 `--step3-cjunc-sv-cf` 로 돌린다 → 매니페스트 증거의 반사실 기록 → `ca_ext_record_ok` →
`next_gen_state` → 사슬 `chain_view` · `sv_assess` (문턱 2.0 · R_j,0).
  A = (24.5, 24.5) 아래 판 z 0.3 → z 18.5 (위 판에 안 닿음) · B = (26.5, 24.5) z 6.5 → 위 판 z 23.2 · A ↔ B 2 µm (> D = 0.15 + tol_ff 0.5)
  SDCP 점 셋 (24.5 · 25.5 · 26.5, 24.5, 12.5) = 셀 (24 · 25 · 26, 24, 12) — A · B 의 z 12 셀을 덮고 둘을 잇는다 → 아래 → 위 길 = A → SDCP → B 뿐.
  대조 = B 가 성분 안에서 시작 (z 12.5 → 23.2 · 한 섬유만 지남).  기대 (등록 R 4판 §5-6): 두 경우 모두 비 +∞ (다른 섬유로 넘어가는 길을 끊으면 G 0)."""
import json
import os
import subprocess
import sys
import tempfile
import numpy as np
REPO = os.environ.get('PRE_REPO')
SCRIPTS = os.path.join(REPO, 'scripts')
sys.path.insert(0, SCRIPTS)
import run_contract as RC        # noqa: E402
import ca_ext_svcf as SV         # noqa: E402
import rint_r_chain as RRC       # noqa: E402

UM_BOX = 1000.0 / ((0.96 - 0.04) / 0.05)
SW0, FLOOR = 0.04, 0.05


def _box(P_um):
    P = np.asarray(P_um, np.float64)
    return np.column_stack([SW0 + P[:, 0] / UM_BOX, SW0 + P[:, 1] / UM_BOX, FLOOR + P[:, 2] / UM_BOX])


def line(a, b, n):
    a = np.asarray(a, np.float64); b = np.asarray(b, np.float64)
    return a[None] + np.linspace(0.0, 1.0, n)[:, None] * (b - a)[None]


def fixture(d, b_start_z):
    with open(os.path.join(d, 'am.csv'), 'w', encoding='utf-8') as f:
        #  2 회차 수정 — payload 상자 z 위끝 = AM 꼭대기 + 0.01 (정규) → AM 작은 구 둘을 위쪽 모서리 (z 23 µm) 에 둔다 (섬유 · SDCP 와 먼 자리)
        #  3 판 — b6 고정물 (`test_ca_ext_b6.make_fixture`) 의 AM 기둥 줄 그대로 (그 시험의 상자 · 판이 섬유 0.3–23.2 µm 를 관통으로 푼다)
        rows = ['# type,x,y,z,r']
        for ix in range(2):
            for iy in range(2):
                for k in range(3):
                    rows.append('2,%.6f,%.6f,%.6f,%.6f' % (0.020 + 0.008 * ix, 0.020 + 0.008 * iy, 0.004 + 0.0075 * k, 0.004))
        f.write('\n'.join(rows) + '\n')
    #  2 회차 수정 — SE 점을 섬유 (x 24.5 · 26.5) 에서 멀리 (x 12–18) 둔다: 첫 판은 SE 가 섬유 셀 대부분을 덮어 의도한 기하가 아니었다
    g = np.arange(12.0, 18.01, 0.75)
    gy = np.arange(12.0, 36.01, 0.75)
    gz = np.arange(0.3, 23.2, 0.75)
    se = np.array([[x, y, z] for x in g for y in gy for z in gz], np.float64)
    blocks = [(_box(se), 1, -1, 0),
              (_box(line((24.5, 24.5, 0.3), (24.5, 24.5, 18.5), 73)), 2, 0, 1),
              (_box(line((26.5, 24.5, b_start_z), (26.5, 24.5, 23.2), 69)), 2, 1, 1),
              (_box(np.array([[24.5, 24.5, 12.5], [25.5, 24.5, 12.5], [26.5, 24.5, 12.5]])), 5, -1, 0)]
    pts = np.vstack([b[0] for b in blocks])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), np.concatenate([np.full(len(b[0]), b[1], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre.npy'), np.concatenate([np.full(len(b[0]), b[2], np.int32) for b in blocks]))
    np.save(os.path.join(d, 'fibre_kind.npy'), np.concatenate([np.full(len(b[0]), b[3], np.int8) for b in blocks]))
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))


CJ = ['--step3-cjunc', '--step3-cjunc-rj', '1e6', '--step3-cjunc-len-law', 'len_scaled_v0', '--step3-cjunc-unreg-law', 'cut',
      '--step3-cjunc-s-min-um', '0.5', '--step3-cjunc-tol-ff-um', '0.5', '--step3-cjunc-ptfe-jlaw', 'P0']
LEAN2 = ['--no-step4', '--no-thermal', '--no-trackb', '--no-field', '--no-ion', '--no-pore', '--no-collector']


def run(tag, b_start_z):
    d = tempfile.mkdtemp(prefix='p2svp_', dir=os.path.dirname(os.path.abspath(__file__)))
    fixture(d, b_start_z)
    cmd = [sys.executable, os.path.join(SCRIPTS, 'mpm_webapp_payload.py'), '--scaffold', 'am.csv', '--se', 'se.npy', '--phase', 'phase.npy',
           '--fibre', 'fibre.npy', '--fibre-dia', 'fibre_dia.npy', '--n-vox', '24', '--step3-vox', '1.0', '--step3-fibre-stamp', 'segment',
           '--out', 'p.json', '--show-results', '--ptfe-stamp', 'off', *LEAN2, *CJ, '--step3-rtol', '1e-12', '--step3-cjunc-sv-cf']
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900, cwd=d, stdin=subprocess.DEVNULL)
    data = json.load(open(os.path.join(d, 'p.json'), encoding='utf-8')) if os.path.exists(os.path.join(d, 'p.json')) else None
    s3 = ((data or {}).get('mpm_metrics') or {}).get('step3') or {}
    man = s3.get('manifest') or {}
    ev = (((man.get('ca_ext') or {}).get('cjunc') or {}).get('evidence') or {})
    cf = (ev.get('solve') or {}).get('sv_counterfactual')
    view = SV.chain_view(cf) if isinstance(cf, dict) else None
    flags, _det = RRC.sv_assess({('1', 'P0', 'R_j0'): {'sv_cf': view}}, 2.0, 'R_j0')
    out = {'rc': r.returncode, 'sigma_e': s3.get('sigma_e_eff_S_cm'), 'next_gen_state': RC.next_gen_state(s3) if s3 else None,
           'ca_ext_record_ok': RC.ca_ext_record_ok(man) if man else None,
           'cf': ({k: cf.get(k) for k in ('status', 'sv_counterfactual_ratio', 'ratio_limit', 'n_sv_faces_cut', 'n_bridging_components',
                                          'n_unsplit_bridging_components', 'G_full_code', 'G_cut_code')} if isinstance(cf, dict) else None),
           'chain_view': view, 'chain_sv_flags_threshold2': flags, 'log_tail': (r.stdout + r.stderr).splitlines()[-3:] if r.returncode else None}
    print(tag, json.dumps(out, ensure_ascii=False, default=str))
    return out


res = {'two_fibres_pass (truth ratio +inf)': run('two_fibres_pass', 6.5),
       'control_only_A_passes (truth ratio +inf)': run('control_only_A', 12.5)}
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_sv_unsplit_payload.json'), 'w'), ensure_ascii=False,
          indent=1, default=str)
