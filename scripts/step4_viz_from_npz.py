#!/usr/bin/env python3
"""STEP4 결과 npz → 뷰어 viz JSON 오프라인 복원 (GPU 재실행 불필요).

왜 필요한가: 2026-07-22~28 사이의 런들은 viz 내보내기 단계에서 죽었다(배열 진리값 버그,
77fa751 잠복 → 9644261 수정).  곡선 npz 는 그 **직전에** 저장돼 무사하고, 뷰어가 쓰는 데이터
(체크포인트 셸-SOC · 면별 반응전류 · φ(z))도 **전부 npz 안에 이미 들어 있다** — 빠진 것은
JSON 으로 옮기는 마지막 한 단계뿐이다.  이 스크립트가 그 한 단계만 오프라인으로 수행한다.

면 좌표/입자 id 는 npz 에 없으므로 그리드에서 CellSystem 을 **재구성**해 얻는다(솔브 없음,
그래프 구성만).  재구성이 원 런과 같은 면 집합을 주도록 npz meta 의 solver_env(prune/cap/
periodic)를 그대로 재적용하고, 면 개수가 다르면 **거부**한다(조용한 불일치 금지).

사용:
  python3 scripts/step4_viz_from_npz.py --grid step4_grid.npz --npz step4_sched00n1_chg_c0.2.npz
  python3 scripts/step4_viz_from_npz.py --dir <런폴더>          # viz 없는 npz 전부 일괄 변환
  python3 scripts/step4_viz_from_npz.py --selftest
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step4_dyn as s4                                       # noqa: E402


def _meta(npz):
    return json.loads(str(npz['params_json'])) if 'params_json' in npz.files else {}


def _build_system(grid_path, meta, verbose=True):
    """원 런과 같은 면 집합을 얻도록 solver_env 를 재적용해 CellSystem 재구성 (솔브 없음).
    반환 sysm 에 vox_um 을 부착 (CellSystem 은 vox_m 만 보관)."""
    g = np.load(grid_path, allow_pickle=False)
    env = (meta.get('solver_env') or {})
    # cap 은 면 집합을 안 바꾸지만(전도도 값만), prune 은 바꾼다 → 원 런 값으로 맞춘다.
    os.environ['MPM_S4_CONTRAST_CAP'] = f"{float(env.get('contrast_cap', 0.0)):g}"
    os.environ['MPM_S4_PRUNE_FLOAT'] = '1' if (env.get('prune_float_comp', 0)
                                               or env.get('prune_float_vox', 0)) else \
                                       os.environ.get('MPM_S4_PRUNE_FLOAT', '1')
    per = bool(np.asarray(g['periodic_xy']).ravel()[0]) if 'periodic_xy' in g.files else False
    sysm = s4.CellSystem(g['sid'], g['sig_e_S_cm'], g['sig_i_S_cm'], g['pid'],
                         len(g['am_r_um']), float(g['vox_um']),
                         z_top_um=float(g['z_top_um']), z_bot_um=0.0, periodic_xy=per)
    sysm.vox_um_grid = float(g['vox_um'])
    if verbose:
        print(f'  그리드 재구성: BV 면 {sysm.n_bv:,} · dof {sysm.N:,} · periodic={per} '
              f'· cap={os.environ["MPM_S4_CONTRAST_CAP"]}', flush=True)
    return sysm


def convert(npz_path, sysm, out_path, viz_max_faces=120000, verbose=True):
    """npz + 재구성 CellSystem → 뷰어 JSON.  반환 (ok, 메시지)."""
    d = np.load(npz_path, allow_pickle=False)
    m = _meta(d)
    if m.get('mode') == 'rest':                              # 정상 — rest 는 애초에 viz 대상이 아님
        return False, 'rest 런 — viz 대상 아님 (뷰어 애니메이션은 전기 스텝만)'
    if 'viz_t' not in d.files or not len(d['viz_t']):
        return False, 'viz 체크포인트 없음 (첫 스텝서 실패한 런)'
    nb = sysm.n_bv
    If_full = d['viz_I_face']                                # (n_chk, n_bv)
    if If_full.shape[1] != nb:
        return False, (f'면 개수 불일치: npz {If_full.shape[1]:,} vs 재구성 {nb:,} — '
                       '그리드/solver_env 가 원 런과 다름 (변환 거부)')
    idx = np.arange(nb)
    if nb > viz_max_faces:                                   # 원 코드와 동일 규약 (seed 0 결정론)
        idx = np.random.default_rng(0).choice(nb, viz_max_faces, replace=False)
        idx.sort()
    m_abs = np.array([max(float(np.mean(np.abs(r_[np.abs(r_) > 0]))) if (np.abs(r_) > 0).any()
                          else 0.0, 1e-30) for r_ in If_full])
    i_rel = If_full[:, idx] / m_abs[:, None]
    # charge: 2026-07-28 부터 params 에 기록.  옛 npz 는 전류 부호로 복원(방전 +, 충전 −).
    _I = d['I']
    charge = bool(m['charge']) if 'charge' in m else bool(_I.size and float(_I[0]) < 0)
    viz = {
        'kind': 'step4_viz', 'c_rate': m.get('c_rate'), 'charge': charge,
        'v_min': m.get('v_min'), 'v_max': m.get('v_max'), 'cv_hold': bool(m.get('cv_hold', False)),
        # i_cut_frac 은 2026-07-28 이전 npz 엔 기록이 없다 → **추측하지 않고 null**
        #   (코드 기본값 0.05 를 채우면 실제 0.1/1 런에 조용한 오라벨이 붙는다 — §F1)
        'i_cut_frac': m.get('i_cut_frac'), 'r_int_ohm_cm2': m.get('r_int_ohm_cm2', 0.0),
        'am_electro_split': m.get('am_electro_split'),
        'x0': m.get('x0'), 'x100': m.get('x100'), 'nr': m.get('nr'),
        'vox_um': getattr(sysm, 'vox_um_grid', None),
        'x_init': m.get('x_init'), 'chained': bool(m.get('chained', False)),
        'c_max_mol_m3': m.get('c_max'),
        'i_1c_a': float(d['I_1C_A']), 'i_mean_abs_a': [float(f'{v:.4g}') for v in m_abs],
        'end_reason': m.get('end_reason'), 'test_only': bool(m.get('test_only', False)),
        'provenance': m.get('ocp_provenance', ''),
        'conv': {'worst_resid': round(float(max(d['newton_resid'])) if d['newton_resid'].size else 0.0, 6),
                 'worst_kcl': round(float(max(d['kcl_rel'])) if d['kcl_rel'].size else 0.0, 6),
                 # rate_relax 는 런타임 속성이라 npz 에 없음 → simulate 와 같은 식으로 재산출
                 'rate_relax': round(float(min(max(1.0, 1.0 / max(float(m.get('c_rate') or 1.0), 0.05)), 10.0)), 2)},
        'curve': {'t_s': [round(float(v), 1) for v in d['t']],
                  'V': [round(float(v), 4) for v in d['V']],
                  'V_terminal': [round(float(v), 4) for v in d['V_terminal']],
                  'x_mean': [round(float(v), 5) for v in d['x_mean']],
                  'eta_kin_mV': [round(float(v) * 1e3, 2) for v in d['eta_kin_mean']],
                  'eta_diff_mV': [round(float(v) * 1e3, 2) for v in d['eta_diff_mean']],
                  'eta_diff_iw_mV': [round(float(v) * 1e3, 2) for v in d['eta_diff_mean_iw']],
                  'I_A': [float(f'{v:.4g}') for v in d['I']],
                  'Q_ohm_e_W': [float(f'{v:.4g}') for v in d['Q_ohm_e_W']],
                  'Q_ohm_i_W': [float(f'{v:.4g}') for v in d['Q_ohm_i_W']],
                  'Q_rint_W': [float(f'{v:.4g}') for v in d['Q_rint_W']],
                  'Q_ct_W': [float(f'{v:.4g}') for v in d['Q_ct_W']]},
        'phi_z': {'z_um': [round(float(v), 2) for v in d['viz_z_um']],
                  'phi_e_V': [[(None if not np.isfinite(v) else round(float(v), 9)) for v in row]
                              for row in d['viz_phi_e_z']],
                  'phi_i_V': [[(None if not np.isfinite(v) else round(float(v), 6)) for v in row]
                              for row in d['viz_phi_i_z']],
                  'note': 'OPERATING z-layer mean potentials per checkpoint — NOT the STEP3 '
                          'unit-ΔV per-network profile'},
        't_s': [round(float(v), 1) for v in d['viz_t']],
        'x_mean': [round(float(v), 4) for v in d['viz_x_mean']],
        'x_shell': np.round(d['viz_x_shell'].astype(np.float64), 4).tolist(),
        'faces': {'n_total': int(nb), 'n_kept': int(len(idx)),
                  'pos_um': np.round(sysm.f_pos_um[idx].astype(np.float64), 1).tolist(),
                  'pid': sysm.f_pid[idx].astype(int).tolist(),
                  'i_rel': np.round(i_rel, 3).tolist()},
        # 출처 표기 — 런 중 생성분과 구별 (뷰어/감사에서 혼동 금지)
        'restored_from_npz': os.path.basename(npz_path),
        # npz 에 없어서 채우지 못한 필드 (추측 금지 → null 로 두고 여기에 명시)
        'restored_missing': [k for k in ('i_cut_frac', 'charge', 'dx_max', 'dt_max') if k not in m],
    }
    with open(out_path, 'w') as fh:
        json.dump(viz, fh, separators=(',', ':'))
    mb = os.path.getsize(out_path) / 1e6
    miss = viz['restored_missing']
    return True, (f'{mb:.1f} MB — chk {len(viz["t_s"])}, faces {len(idx):,}/{nb:,}'
                  + (f'  ⚠미기록 필드 {miss} → null' if miss else ''))


def _viz_name(npz_path):
    """step4_sched00n1_chg_c0.2_....npz → step4_sched00n1_viz_chg_c0.2_....json (킷 규약 미러)."""
    b = os.path.basename(npz_path)
    stem = b[:-4] if b.endswith('.npz') else b
    parts = stem.split('_')
    for i, p in enumerate(parts):                            # sched 태그 뒤에 viz 삽입
        if p.startswith('sched'):
            parts.insert(i + 1, 'viz')
            break
    else:                                                    # 스케줄 아닌 런: step4_ 뒤에
        parts.insert(1, 'viz')
    return os.path.join(os.path.dirname(npz_path), '_'.join(parts) + '.json')


def _selftest():
    """미니 격자로 런 → viz 지운 뒤 복원 → 런-중 생성분과 동일한지 대조."""
    import subprocess
    import tempfile
    ok = True
    here = os.path.dirname(os.path.abspath(__file__))
    with tempfile.TemporaryDirectory() as td:
        sid, pid, vox = s4._build_sandwich(nxy=4, nz=8)
        gp = os.path.join(td, 'g.npz')
        np.savez_compressed(gp, sid=sid, pid=pid, vox_um=vox, z_top_um=8 * 0.5,
                            sig_e_S_cm=np.array([0., 1., 0., 0., 0., 0., 0.]),
                            sig_i_S_cm=np.array([0., 0., 0., 0., 0., 0., 2.]),
                            am_r_um=np.array([10.0]))
        npz, vjs = os.path.join(td, 'r.npz'), os.path.join(td, 'r_viz.json')
        r = subprocess.run([sys.executable, os.path.join(here, 'step4_dyn.py'),
                            '--grid', gp, '--ocp-test', '--c-rate', '1', '--v-min', '2.8',
                            '--t-max', '120', '--nr', '15', '--out', npz, '--viz-out', vjs],
                           capture_output=True, text=True, timeout=600)
        if r.returncode != 0 or not os.path.exists(vjs):
            print('  ✗ 기준 런 실패\n' + r.stdout[-800:] + r.stderr[-800:])
            return False
        ref = json.load(open(vjs))
        sysm = _build_system(gp, _meta(np.load(npz, allow_pickle=False)), verbose=False)
        got_p = os.path.join(td, 'restored.json')
        good, msg = convert(npz, sysm, got_p, verbose=False)
        if not good:
            print(f'  ✗ 복원 실패: {msg}'); return False
        got = json.load(open(got_p))
        skip = {'restored_from_npz'}
        diff = [k for k in ref if k not in skip and ref[k] != got.get(k)]
        ok &= not diff
        print(f'  복원 ≡ 런-중 생성 (키 {len(ref)}개 전수 대조): '
              f'{"OK" if not diff else "FAIL — 불일치 " + str(diff)}')
        # 면-불일치 거부 가드
        bad = os.path.join(td, 'bad.json')
        sysm.n_bv += 1
        good2, msg2 = convert(npz, sysm, bad, verbose=False)
        ok &= (not good2 and '면 개수 불일치' in msg2)
        print(f'  면 개수 불일치 거부: {"OK" if not good2 else "FAIL"}')
        # 이름 규약 미러 (킷이 만드는 이름과 정확히 같아야 뷰어/회수 스크립트가 짝을 찾는다)
        n1 = _viz_name('/x/step4_sched04n2_chg_c2_rint50.npz')
        n2 = _viz_name('/x/step4_c1_rint46.npz')
        okn = (n1.endswith('step4_sched04n2_viz_chg_c2_rint50.json')
               and n2.endswith('step4_viz_c1_rint46.json'))
        ok &= okn
        print(f'  이름 규약: {os.path.basename(n1)} · {os.path.basename(n2)}  '
              f'{"OK" if okn else "FAIL"}')
    print('VIZ-RESTORE SELFTEST', 'PASS' if ok else 'FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(description='STEP4 npz → 뷰어 viz JSON 오프라인 복원')
    ap.add_argument('--grid', default='', help='step4_grid.npz (--dir 면 그 폴더서 자동)')
    ap.add_argument('--npz', default='', help='변환할 결과 npz 하나')
    ap.add_argument('--dir', default='', help='런 폴더 — viz 없는 step4 npz 전부 일괄 변환')
    ap.add_argument('--out', default='', help='출력 JSON (기본: 킷 이름 규약 자동)')
    ap.add_argument('--viz-max-faces', type=int, default=120000)
    ap.add_argument('--force', action='store_true', help='이미 viz JSON 이 있어도 덮어씀')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if not (a.npz or a.dir):
        ap.error('--npz 또는 --dir 필요')

    targets = ([a.npz] if a.npz else
               sorted(p for p in glob.glob(os.path.join(a.dir, 'step4_*.npz'))
                      if not os.path.basename(p).startswith('s4state_')
                      and 'grid' not in os.path.basename(p)))
    if not targets:
        print('변환할 npz 없음'); sys.exit(1)
    grid = a.grid or os.path.join(a.dir or os.path.dirname(targets[0]), 'step4_grid.npz')
    if not os.path.exists(grid):
        print(f'그리드 없음: {grid} (--grid 로 지정)'); sys.exit(1)

    sysm, n_ok, n_skip = None, 0, 0
    for p in targets:
        out = a.out if (a.npz and a.out) else _viz_name(p)
        if os.path.exists(out) and not a.force:
            print(f'· {os.path.basename(p)} → 이미 있음 (건너뜀, --force 로 덮어쓰기)'); n_skip += 1
            continue
        if sysm is None:                                     # 그리드 재구성은 1회만 (여러 npz 공유)
            sysm = _build_system(grid, _meta(np.load(p, allow_pickle=False)))
        good, msg = convert(p, sysm, out, viz_max_faces=a.viz_max_faces)
        print(f'{"✓" if good else "✗"} {os.path.basename(p)} → '
              f'{os.path.basename(out) if good else msg}' + (f'  ({msg})' if good else ''))
        n_ok += int(good)
        if not good and os.path.exists(out):
            os.remove(out)
    print(f'\n복원 {n_ok}개 · 건너뜀 {n_skip}개 · 대상 {len(targets)}개')


if __name__ == '__main__':
    main()
