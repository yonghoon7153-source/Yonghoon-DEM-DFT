#!/usr/bin/env python3
"""A-3 캘리브 훅: MPM 앵커로 ledger의 SE-재유동 회복(reflow) DOF 회귀 (real_degrading_electrode §3 A-3).

빠른 근사(cycle_contact_ledger, 강체구+기하)는 SC 수축→접촉개구 손실을 기하대로 다 잃는다.  정확한
MPM(A-1 --cycle-deform)은 말랑 SE가 흘러들어(plastic 재유동, frame[5] = ledger엔 없는 것) 손실의
일부를 회복 → 실제 손실 < 기하.  그 회복분(reflow)을 MPM 앵커에 회귀해 ledger에 심는다(--reflow-recover).

★비교 지표: SC(AM_S)-SE 접촉면적 손실 (Hertz A ∝ R·ov).
  MPM = coverage_AM_S 손실 (앵커 metrics), ledger = √(R·ov) 기하 손실 (build_contacts + 앵커 ΔV).
  reflow = 1 − MPM/ledger.  ★2+ 충전앵커면 단일 reflow의 일반화 + LOAO(blind) 오차를 리포트(정직).

⚠ 이건 ε(가역 변형)-DOF 캘리브만 — 영구 열화(δcr, rewet_frac)는 반복사이클 MPM(v2) 필요.
⚠ ASSUMED-FORM: MPM voxel-coverage ↔ ledger Hertz-area 지표차이가 reflow에 일부 섞임(순수 재유동 아님).

사용:
  python3 scripts/calibrate_ledger_reflow.py --atoms real14_atoms.csv --type-map 1:AM_P,2:AM_S,3:SE \
      --pristine a1_anchors/m_N0.json --charged a1_anchors/m_charged.json a1_anchors/m_charged_deep.json
  python3 scripts/calibrate_ledger_reflow.py --from-scaffold docs/data/real14   # *_am/se_scaffold.csv → atoms
  python3 scripts/calibrate_ledger_reflow.py --selftest
"""
import argparse
import importlib.util
import json
import os
import sys

import numpy as np


def _load_ledger():
    s = importlib.util.spec_from_file_location('_L', os.path.join(os.path.dirname(__file__), 'cycle_contact_ledger.py'))
    L = importlib.util.module_from_spec(s)
    _argv = sys.argv
    sys.argv = ['_L']
    s.loader.exec_module(L)
    sys.argv = _argv
    return L


def _atoms_from_scaffold(prefix):
    """docs/data/real14 → real14_am_scaffold.csv + real14_se_scaffold.csv (박스단위) → atoms (µm, ×1000)."""
    def rd(p):
        return [ln.strip().split(',') for ln in open(p) if ln.strip() and not ln.startswith('#')]
    am = rd(prefix + '_am_scaffold.csv')
    se = rd(prefix + '_se_scaffold.csv')
    typ = []
    xyz = []
    rad = []
    for r in am:
        typ.append(int(float(r[0])))
        xyz.append([float(r[1]) * 1000, float(r[2]) * 1000, float(r[3]) * 1000])
        rad.append(float(r[4]) * 1000)
    for r in se:
        typ.append(3)
        xyz.append([float(r[1]) * 1000, float(r[2]) * 1000, float(r[3]) * 1000])
        rad.append(float(r[4]) * 1000)
    return np.array(typ), np.array(xyz, float), np.array(rad, float)


def _atoms_from_csv(path, type_map):
    tm = {}
    for kv in type_map.split(','):
        k, v = kv.split(':')
        tm[int(k)] = v
    typ_raw = []
    xyz = []
    rad = []
    for ln in open(path):
        ln = ln.strip()
        if not ln or ln.lower().startswith('id') or ln.startswith('#'):
            continue
        c = ln.split(',')
        typ_raw.append(int(float(c[1])))
        xyz.append([float(c[2]), float(c[3]), float(c[4])])
        rad.append(float(c[5]))
    # map to canonical 1=AM_P,2=AM_S,3=SE for the SC-SE selector below
    canon = {'AM_P': 1, 'AM_S': 2, 'SE': 3}
    typ = np.array([canon.get(tm.get(t, ''), t) for t in typ_raw])
    return typ, np.array(xyz, float), np.array(rad, float)


def _sc_area_loss(L, typ, xyz, rad, dv_pct, reflow):
    """ledger 기하로 SC(AM_S=2)-SE 접촉면적(Hertz R·ov) 손실 %  (reflow 적용, 개구만 (1-R)배)."""
    ci, cj, d, ov0 = L.build_contacts(xyz, rad)
    is_am = (typ[ci] == 1) | (typ[ci] == 2)
    is_am_j = (typ[cj] == 1) | (typ[cj] == 2)
    sc_se = ((typ[ci] == 2) & (typ[cj] == 3)) | ((typ[cj] == 2) & (typ[ci] == 3))
    if not sc_se.any():
        return None
    Rstar = rad[ci] * rad[cj] / (rad[ci] + rad[cj])
    eps = dv_pct / 100.0 / 3.0
    move = np.where(is_am, rad[ci] * eps, 0.0) + np.where(is_am_j, rad[cj] * eps, 0.0)
    move = np.where(move > 0, (1.0 - reflow) * move, move)
    A0 = Rstar * ov0
    Ach = Rstar * np.maximum(0.0, ov0 - move)
    return 100.0 * (1.0 - Ach[sc_se].sum() / max(A0[sc_se].sum(), 1e-30))


def _mpm_sc_loss(pristine, charged):
    """MPM 앵커 metrics → SC(AM_S) coverage 상대손실 % + 앵커 ΔV(SC) %."""
    p = pristine if isinstance(pristine, dict) else json.load(open(pristine))
    c = charged if isinstance(charged, dict) else json.load(open(charged))
    cs0 = p.get('coverage_AM_S_pct')
    cs1 = c.get('coverage_AM_S_pct')
    dv = abs(float((c.get('cycle_deform') or {}).get('dv_sc', 0.0))) * 100.0   # 0.051 → 5.1 %
    loss = 100.0 * (1.0 - cs1 / cs0) if (cs0 and cs1 is not None) else None
    return loss, dv


def calibrate(typ, xyz, rad, pristine, charged_list):
    L = _load_ledger()
    rows = []
    for ch in charged_list:
        mpm_loss, dv = _mpm_sc_loss(pristine, ch)
        led_loss = _sc_area_loss(L, typ, xyz, rad, dv, 0.0)
        if mpm_loss is None or led_loss is None or led_loss <= 0:
            continue
        rows.append({'dv': dv, 'mpm': mpm_loss, 'ledger_geom': led_loss, 'reflow': 1.0 - mpm_loss / led_loss})
    if not rows:
        return {'error': 'no valid anchors (coverage_AM_S/cycle_deform 결측?)'}
    reflow_mean = float(np.mean([r['reflow'] for r in rows]))
    out = {'reflow_recover': round(reflow_mean, 3), 'n_anchors': len(rows), 'per_anchor': rows,
           'reflow_spread': round(float(np.ptp([r['reflow'] for r in rows])), 3) if len(rows) > 1 else None}
    # LOAO (2+ 앵커): 한 앵커로 fit → 나머지 blind 예측 오차
    if len(rows) >= 2:
        loao = []
        for i, held in enumerate(rows):
            others = [r for j, r in enumerate(rows) if j != i]
            R_fit = float(np.mean([r['reflow'] for r in others]))
            pred = _sc_area_loss(L, typ, xyz, rad, held['dv'], R_fit)
            loao.append({'held_dv': held['dv'], 'R_fit': round(R_fit, 3),
                         'pred': round(pred, 1), 'actual': round(held['mpm'], 1),
                         'blind_err_pp': round(abs(pred - held['mpm']), 1)})
        out['loao'] = loao
        out['loao_max_err_pp'] = round(max(x['blind_err_pp'] for x in loao), 1)
    return out


def _report(out):
    if 'error' in out:
        print('❌', out['error'])
        return
    print('=' * 84)
    print('A-3 reflow 캘리브 (MPM 앵커 → ledger SE-재유동 회복 DOF)')
    print('  ⚠ ε(가역 변형)-DOF만; 영구열화(δcr,rewet)=반복사이클 MPM(v2).  지표차이 일부 혼입(ASSUMED-FORM).')
    print('-' * 84)
    print(f"  {'ΔV(SC)':>8} {'MPM손실%':>9} {'ledger기하%':>11} {'reflow':>8}")
    for r in out['per_anchor']:
        print(f"  {r['dv']:7.1f}% {r['mpm']:9.1f} {r['ledger_geom']:11.1f} {r['reflow']:8.3f}")
    print('-' * 84)
    print(f"  ★ 캘리브 reflow-recover = {out['reflow_recover']}  "
          f"(SE plastic 재유동이 기하 접촉손실의 {out['reflow_recover']*100:.0f}% 회복)")
    if out.get('reflow_spread') is not None:
        print(f"    앵커간 reflow 산포 = {out['reflow_spread']}  "
              f"({'✅ 일반화(단일계수)' if out['reflow_spread'] < 0.05 else '⚠ ΔV-의존'})")
    if 'loao' in out:
        print('  LOAO (한 앵커 fit → 나머지 blind 예측):')
        for x in out['loao']:
            print(f"    ΔV={x['held_dv']}% held: R={x['R_fit']} → pred {x['pred']}% vs 실측 {x['actual']}%  "
                  f"(blind 오차 {x['blind_err_pp']}%p)")
        print(f"    → LOAO 최대 blind 오차 = {out['loao_max_err_pp']}%p")
    print(f"\n  적용: cycle_contact_ledger.py --reflow-recover {out['reflow_recover']} (+ --poly-mode expand-void)")
    print('=' * 84)


def _selftest():
    """합성: ledger 기하 30%가 나오는 접촉 + MPM 20% 앵커 → reflow≈0.33 회귀 확인."""
    L = _load_ledger()
    # 6µm AM_S(type2 취급 위해 반경<split? — selftest는 2µm) + SE 겹침 여러 개
    rng = np.random.default_rng(0)
    typ = [2] * 20 + [3] * 20
    xyz = []
    rad = []
    for i in range(20):                                       # AM_S 2µm 격자
        xyz.append([i * 3.5, 0, 0])
        rad.append(2.0)
    for i in range(20):                                       # SE 0.5µm, AM_S와 겹치게
        xyz.append([i * 3.5, 2.3, 0])
        rad.append(0.5)
    typ = np.array(typ)
    xyz = np.array(xyz, float)
    rad = np.array(rad, float)
    geom = _sc_area_loss(L, typ, xyz, rad, 5.1, 0.0)
    ok = geom is not None and geom > 0
    print(f"  [{'PASS' if ok else 'FAIL'}] SC-SE 기하 손실 계산됨: {geom}")
    if ok:
        # MPM 앵커 합성: MPM 손실 < 기하 손실이 되게(양수 reflow) SC coverage 손실 = geom·0.7 로 세팅
        mpm_loss = geom * 0.7                                  # 기하의 70% = reflow 0.30 기대
        pri = {'coverage_AM_S_pct': 40.0, 'coverage_AM_P_pct': 30.0}
        chg = {'coverage_AM_S_pct': 40.0 * (1 - mpm_loss / 100.0), 'coverage_AM_P_pct': 33.0,
               'cycle_deform': {'dv_sc': -0.051}}
        out = calibrate(typ, xyz, rad, pri, [chg])
        r = out['per_anchor'][0]['reflow']                    # unrounded (round 오차 회피)
        exp = 1.0 - mpm_loss / geom                           # = 0.30
        ok2 = abs(r - exp) < 1e-6 and abs(r - 0.30) < 1e-6
        print(f"  [{'PASS' if ok2 else 'FAIL'}] reflow 회귀 = {r:.4f} (기대 {exp:.4f} = 0.30)")
        ok = ok and ok2
    print('CALIBRATE-REFLOW SELFTEST', 'PASS' if ok else 'FAIL')
    return ok


def main(argv):
    ap = argparse.ArgumentParser(description='A-3 reflow 캘리브 (MPM 앵커 → ledger)')
    ap.add_argument('--atoms', help='ledger용 atoms.csv (id,type,x,y,z,radius; µm)')
    ap.add_argument('--from-scaffold', help='<prefix> → <prefix>_am_scaffold.csv/_se_scaffold.csv (박스단위→µm)')
    ap.add_argument('--type-map', default='1:AM_P,2:AM_S,3:SE')
    ap.add_argument('--pristine', help='MPM N0 앵커 metrics JSON')
    ap.add_argument('--charged', nargs='+', help='MPM 충전 앵커 metrics JSON (1개 이상)')
    ap.add_argument('--out', default='', help='캘리브 결과 JSON 저장 경로 (선택)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if not (a.pristine and a.charged):
        ap.error('--pristine + --charged 필요 (또는 --selftest)')
    if a.from_scaffold:
        typ, xyz, rad = _atoms_from_scaffold(a.from_scaffold)
    elif a.atoms:
        typ, xyz, rad = _atoms_from_csv(a.atoms, a.type_map)
    else:
        ap.error('--atoms 또는 --from-scaffold 필요')
    out = calibrate(typ, xyz, rad, a.pristine, a.charged)
    _report(out)
    if a.out:
        json.dump(out, open(a.out, 'w'), indent=2, ensure_ascii=False)
        print(f'  saved → {a.out}')


if __name__ == '__main__':
    main(sys.argv[1:])
