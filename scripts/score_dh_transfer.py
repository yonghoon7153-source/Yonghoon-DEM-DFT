#!/usr/bin/env python3
"""score_dh_transfer.py — 동결된 d_h 접힘 선으로 **새 침대**의 σ 를 예측하고 실측과 채점한다 (표본 밖 시험).

사전등록: docs/reviews/ps45_dh_transfer_prereg_20260926.md.
선 = `fit_dh_collapse.py --freeze-json` 이 쓴 JSON (ln σ[GPa] = a + b·ln d_h[µm], schema dh_frozen_line_v1).
이 스크립트는 **선을 다시 맞추지 않는다** — 새 침대 점은 적합에 들어가지 않는다 (CDX-14: 동결한 φ 로
새 침대를 예측해야 '전이' 라는 말을 쓸 수 있다).

채점 규약 (런 전 등록 — 결과를 보고 바꾸지 않는다):
  · 새 침대마다 동결 φ0 를 **감싸는** 두 점에서 σ 를 σ-선형 보간 (fit_dh_collapse.select_at_phi 그대로).
    감싸지 못하면 (외삽) 그 침대는 HOLD — 국소기울기 보정은 쓰지 않는다 (보정 자체가 표본 안 정보다).
  · d_h = V_SE/φ0 / S_AM (fit_dh_collapse.d_h_at_phi · include_se=True) — 적합 때와 같은 규약.
  · 잔차 r = ln(σ_meas / σ_pred) · 띠 = ±k·sd (k 기본 2 · sd = 동결 선의 잔차 sd).
  · 판정: TRANSFERS = 전부 띠 안 · PARTIAL = 하나만 밖 · FAILS = 둘 이상 밖 · HOLD = 외삽 침대가 하나라도 있음.
  · d_h/dx < min_cells (기본 3.5 · dx = 54.35 µm / n_grid, docs/se_curve_transfer_verdict_20260806.md 규약) 인 침대는
    '저해상' 표지 — 채점에서 빼지 않고 표지만 붙인다 (그 침대의 σ 는 하한 방향 = r < 0 이 예상 방향).

사용:
  python3 scripts/score_dh_transfer.py --frozen docs/data/dh_frozen_288_phi075_20260926.json \
      --dir ~/se_curve --kit-root ~/se_curve --kits kit_ps_0_10_r45,... --n-grid 288 --mach 0.03 --out score.json
  python3 scripts/score_dh_transfer.py --selftest
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DX_REF_UM = 54.35          # verdict 문서 규약: dx = 54.35 µm / n_grid (288 → 189 nm)
MIN_CELLS = 3.5            # d_h/dx ≳ 3.5 = SE 응력을 믿을 수 있는 최소 해상도 (verdict §⑤)
VERDICTS = ('TRANSFERS', 'PARTIAL', 'FAILS', 'HOLD')


def predict(frozen, d_h_um):
    """동결 선의 예측 σ [GPa] — d_h [µm]."""
    if not (d_h_um > 0):
        return float('nan')
    return math.exp(float(frozen['a']) + float(frozen['b']) * math.log(float(d_h_um)))


def score(frozen, beds, band_sd=2.0, dx_um=None, min_cells=MIN_CELLS):
    """beds = [{'kit','d_h_um','sigma','method'(,'phi','mach')}] → 채점 dict.  순수 함수 (파일 없음)."""
    sd = float(frozen['resid_sd'])
    band = float(band_sd) * sd
    rows, n_hold, n_out = [], 0, 0
    for bd in beds:
        r = {'kit': bd['kit'], 'd_h_um': float(bd['d_h_um']), 'sigma_meas': float(bd['sigma']),
             'method': bd.get('method'), 'phi': bd.get('phi'), 'mach': bd.get('mach')}
        r['sigma_pred'] = predict(frozen, r['d_h_um'])
        if dx_um:
            r['cells'] = r['d_h_um'] / float(dx_um)
            r['low_res'] = bool(r['cells'] < min_cells)
        if bd.get('method') != 'interp' or not (r['sigma_meas'] > 0) or not math.isfinite(r['sigma_pred']):
            r['status'] = 'HOLD'; r['resid'] = None; r['within'] = None
            n_hold += 1
        else:
            r['resid'] = math.log(r['sigma_meas'] / r['sigma_pred'])
            r['within'] = bool(abs(r['resid']) <= band)
            r['status'] = 'in' if r['within'] else 'out'
            if not r['within']:
                n_out += 1
        rows.append(r)
    if n_hold:
        verdict = 'HOLD'
    elif n_out == 0:
        verdict = 'TRANSFERS'
    elif n_out == 1:
        verdict = 'PARTIAL'
    else:
        verdict = 'FAILS'
    scored = [r for r in rows if r['resid'] is not None]
    return {
        'schema': 'dh_transfer_score_v1', 'verdict': verdict,
        'band_sd_mult': float(band_sd), 'band_ln': band, 'resid_sd_frozen': sd,
        'frozen': {k: frozen.get(k) for k in ('a', 'b', 'r2', 'resid_sd', 'n_grid', 'phi', 'mach', 'n')},
        'n_beds': len(rows), 'n_scored': len(scored), 'n_out': n_out, 'n_hold': n_hold,
        'max_abs_resid': (max(abs(r['resid']) for r in scored) if scored else None),
        'mean_resid': (sum(r['resid'] for r in scored) / len(scored) if scored else None),
        'low_res_kits': [r['kit'] for r in rows if r.get('low_res')],
        'dx_um': dx_um, 'min_cells': min_cells,
        'rows': rows,
    }


def collect(root, kit_root, kits, n_grid, mach, phi):
    """xfer JSON + 스캐폴드에서 침대별 (d_h, σ@φ) 를 모은다 — fit_dh_collapse 의 함수를 그대로 쓴다."""
    import fit_dh_collapse as fdc
    beds = []
    for k in kits:
        d = os.path.join(kit_root, k)
        fdc._kit_dir_cache[k] = d if os.path.isdir(d) else os.path.join(root, k)
        pts = fdc._mach_filter(fdc.load_kit_points(root, k, n_grid), mach)
        _v_am, v_se, _A, s_am = fdc.bed_geometry(fdc._kit_dir_cache[k])
        d_h = fdc.d_h_at_phi(v_se, s_am, phi, include_se=True)
        if not pts:
            beds.append({'kit': k, 'd_h_um': d_h, 'sigma': float('nan'), 'method': 'no_points', 'phi': None,
                         'mach': None, 'n_points': 0})
            continue
        sel = fdc.select_at_phi(pts, phi)
        beds.append({'kit': k, 'd_h_um': d_h, 'sigma': sel['sigma'], 'method': sel['method'], 'phi': sel['phi'],
                     'mach': sel['mach'], 'file': sel['file'], 'n_points': len(pts)})
    return beds


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--frozen', help='fit_dh_collapse.py --freeze-json 이 쓴 동결 선 JSON')
    ap.add_argument('--dir', default='.', help='xfer_*.json 디렉터리')
    ap.add_argument('--kit-root', default=None, help='킷 디렉터리들의 부모 (기본 --dir)')
    ap.add_argument('--kits', default='', help='쉼표 구분 새 침대 킷 이름 (동결 선의 킷과 겹치면 거부)')
    ap.add_argument('--n-grid', type=int, default=None, help='기본 = 동결 선의 n_grid')
    ap.add_argument('--mach', type=float, default=None, help='기본 = 동결 선의 mach')
    ap.add_argument('--band-sd', type=float, default=2.0, help='띠 = ±k·sd (기본 2)')
    ap.add_argument('--min-cells', type=float, default=MIN_CELLS)
    ap.add_argument('--out', default=None, help='채점 JSON 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.frozen or not a.kits:
        ap.error('--frozen 과 --kits 가 필요하다')
    frozen = json.load(open(a.frozen, encoding='utf-8'))
    if frozen.get('schema') != 'dh_frozen_line_v1':
        print(f"ABORT — 동결 선 schema 가 다르다: {frozen.get('schema')!r}"); return 2
    kits = [k for k in a.kits.split(',') if k]
    dup = sorted(set(kits) & {r['kit'] for r in frozen.get('kits', [])})
    if dup:
        print(f'ABORT — 동결 선에 들어간 킷은 표본 밖이 아니다: {dup}'); return 2
    n_grid = a.n_grid or int(frozen['n_grid'])
    mach = a.mach if a.mach is not None else frozen.get('mach')
    if n_grid != int(frozen['n_grid']):
        print(f"ABORT — n_grid {n_grid} ≠ 동결 선 {frozen['n_grid']} (격자가 다르면 선이 다르다)"); return 2
    beds = collect(a.dir, a.kit_root or a.dir, kits, n_grid, mach, float(frozen['phi']))
    res = score(frozen, beds, band_sd=a.band_sd, dx_um=DX_REF_UM / n_grid, min_cells=a.min_cells)
    res['inputs'] = {'frozen': os.path.abspath(a.frozen), 'dir': os.path.abspath(a.dir), 'kits': kits,
                     'n_grid': n_grid, 'mach': mach, 'phi': float(frozen['phi'])}
    print(f"══ d_h 전이 채점 — 동결 선 g{frozen['n_grid']} φ {frozen['phi']} · a {frozen['a']:+.4f} b {frozen['b']:+.4f} "
          f"· 띠 ±{res['band_ln']:.3f} (k={a.band_sd}·sd {res['resid_sd_frozen']:.3f}) ══")
    print(f"   {'kit':>16}{'φ':>8}{'방법':>10}{'d_h(nm)':>10}{'셀':>6}{'σ_meas':>9}{'σ_pred':>9}{'r':>8}  판정")
    for r in res['rows']:
        ph = f"{r['phi']:.4f}" if r.get('phi') is not None else '—'
        rr = f"{r['resid']:+.3f}" if r['resid'] is not None else '—'
        cells = f"{r['cells']:.2f}" if 'cells' in r else '—'
        flag = ' ⚠저해상' if r.get('low_res') else ''
        print(f"   {r['kit']:>16}{ph:>8}{str(r['method']):>10}{r['d_h_um'] * 1000:10.1f}{cells:>6}"
              f"{r['sigma_meas']:9.4f}{r['sigma_pred']:9.4f}{rr:>8}  {r['status']}{flag}")
    print(f"   ⇒ {res['verdict']}  (밖 {res['n_out']} · HOLD {res['n_hold']} · 채점 {res['n_scored']}/{res['n_beds']}"
          f"{' · 최대|r| %.3f' % res['max_abs_resid'] if res['max_abs_resid'] is not None else ''})")
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
        print(f'   → {a.out}')
    return 0


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    fz = {'schema': 'dh_frozen_line_v1', 'a': -0.683, 'b': -0.575, 'r2': 0.926, 'resid_sd': 0.077,
          'n_grid': 288, 'phi': 0.75, 'mach': 0.03, 'n': 5, 'kits': [{'kit': 'kit_ps_7_3'}]}
    dh = [0.50, 0.60, 0.70, 0.82, 1.13]

    def bed(k, d, factor=1.0, method='interp'):
        return {'kit': k, 'd_h_um': d, 'sigma': predict(fz, d) * factor, 'method': method, 'phi': 0.75, 'mach': 0.03}

    # 1 선 위의 점은 잔차 0 · TRANSFERS
    beds = [bed(f'k{i}', d) for i, d in enumerate(dh)]
    r = score(fz, beds)
    chk('선 위 5 침대 → TRANSFERS · 잔차 0', r['verdict'] == 'TRANSFERS' and r['max_abs_resid'] < 1e-12 and r['n_scored'] == 5)
    chk('띠 = 2·sd', abs(r['band_ln'] - 0.154) < 1e-9)
    # 2 하나만 3 sd 밖 → PARTIAL · 둘 → FAILS
    beds2 = [bed(f'k{i}', d, factor=(math.exp(3 * 0.077) if i == 2 else 1.0)) for i, d in enumerate(dh)]
    chk('한 침대 +3 sd → PARTIAL', score(fz, beds2)['verdict'] == 'PARTIAL')
    beds3 = [bed(f'k{i}', d, factor=(math.exp((-1) ** i * 3 * 0.077) if i in (1, 3) else 1.0)) for i, d in enumerate(dh)]
    chk('두 침대 ±3 sd → FAILS', score(fz, beds3)['verdict'] == 'FAILS')
    # 3 띠 안쪽 1.9 sd 는 통과 (경계 규약 |r| ≤ band)
    beds4 = [bed(f'k{i}', d, factor=math.exp(1.9 * 0.077)) for i, d in enumerate(dh)]
    chk('전부 +1.9 sd → 여전히 TRANSFERS (띠 안)', score(fz, beds4)['verdict'] == 'TRANSFERS')
    # 4 외삽 침대 → HOLD (다른 침대가 전부 선 위여도)
    beds5 = [bed(f'k{i}', d, method=('nearest' if i == 4 else 'interp')) for i, d in enumerate(dh)]
    r5 = score(fz, beds5)
    chk('외삽(nearest) 침대 하나 → HOLD · 그 침대 잔차 None', r5['verdict'] == 'HOLD' and r5['n_hold'] == 1
        and r5['rows'][4]['resid'] is None and r5['n_scored'] == 4)
    chk('점 없음(no_points) 도 HOLD', score(fz, [bed('x', 0.6, method='no_points')])['verdict'] == 'HOLD')
    # 5 저해상 표지 — dx 189 nm: 0.50 µm → 2.65 셀 (표지) · 1.13 → 5.98 (없음) · 채점에서 빠지지 않는다
    r6 = score(fz, beds, dx_um=DX_REF_UM / 288)
    chk('저해상 표지 = d_h/dx < 3.5 (0.50 · 0.60 µm) · 채점은 그대로 5', r6['low_res_kits'] == ['k0', 'k1'] and r6['n_scored'] == 5
        and abs(r6['rows'][0]['cells'] - 0.50 / (54.35 / 288)) < 1e-9)
    # 6 음성 대조 — 기울기 부호가 반대인 선이면 FAILS (채점기가 무엇이든 초록을 내지 않는다)
    wrong = dict(fz, b=+0.575)
    chk('부호 반대 선 → FAILS', score(wrong, beds)['verdict'] == 'FAILS')
    # 7 예측은 b<0 에서 d_h 에 단조 감소
    chk('predict 단조 감소 (b<0)', predict(fz, 0.5) > predict(fz, 1.0) > predict(fz, 1.4))
    chk('predict(1 µm) = exp(a)', abs(predict(fz, 1.0) - math.exp(-0.683)) < 1e-12)
    # 8 판정 어휘 고정
    chk('판정 어휘', all(score(fz, b_)['verdict'] in VERDICTS for b_ in (beds, beds2, beds3, beds5)))
    print(f"selftest: {ok}/{ok + len(fail)} PASS" + (f"   FAILED: {fail}" if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    sys.exit(main())
