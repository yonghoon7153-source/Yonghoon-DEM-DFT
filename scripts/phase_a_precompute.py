#!/usr/bin/env python3
"""Phase A (6 mAh VGCF+PTFE) **런 전 사전계산** — GPU 불요, 스캐폴드 파일 불요.

    python3 scripts/phase_a_precompute.py --out docs/data/phase_a_6mah/precompute.json
    python3 scripts/phase_a_precompute.py --selftest

━━ 왜 스캐폴드 파일 없이 되나 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`d_h` 와 첨가제 객체 수는 **총량**만 필요하다 (V_AM · S_AM · V_SE · 상자).  입자 **위치**가
필요한 것은 각도 선별(`step4_angular_risk.py`)뿐이고 그건 스캐폴드 CSV 를 기다린다.

침대 상수는 `docs/session_20260906_progress.md` §8-2 에서 온다 (옛 6 mAh 캠페인 case_master):
AM_P 126 · AM_S 1,372 · p_frac 0.7 · SE/solid 33.23 vol% · 상자 50.01 × 50.01 × 112.87 µm.

★ **반경은 가정이 아니라 교차검증된다** — 12:4:1 규약의 R_P=6 · R_S=2 를 넣으면
`V_P/(V_P+V_S) = 0.713` 이 기록된 `p_frac 0.70` 과 맞고(±2 %), `V_AM + V_SE` 가 기록된
`V_solid 241,953 µm³` 와 **0.65 %** 안에서 닫힌다.  둘 다 어긋나면 이 스크립트는 **거부한다**
(조용히 진행하지 않는다).

━━ 무엇을 내나 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
① **`d_h/dx` 게이트** (STEP2 MPM) — `d_h = V_free/S_AM`, 규칙 `d_h/dx ≳ 3.5`.
   ⚠⚠ 이 게이트는 **MPM 의 SE 응력**에 대한 것이다.  STEP3 의 σ 격자와 **다른 질문**이고,
   통과한다고 STEP3 가 안전하다는 뜻이 **전혀 아니다** — STEP3 쪽은 SE neck 해상도가 따로
   있고 `h = 0.20 · 0.25` 에서 neck 의 85.6 % · 97.4 % 가 2 셀 미만이다 (CL-72).
② **첨가제 객체 수** — 프로덕션 경로 `additives.recipe_counts_real` 을 그대로 부른다
   (실물 scaffold 질량 기준; `--add-recipe` 가 AM:SE 를 무시하는 것과 같은 규약).
   ⚠ 옛 손계산(세션 §8-4)은 3.7 % 어긋났다.  이 경로는 옛 캠페인 4행을 **0.58 %** 로 재현한다.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  ── 침대 상수 (세션 §8-2, 옛 6 mAh 캠페인 case_master) ─────────────────────────
BED = {
    'case': 'input_6mAh_real_4',
    'n_am_p': 126, 'n_am_s': 1372,
    'r_am_p_um': 6.0, 'r_am_s_um': 2.0,       # 12:4:1 규약 — 아래에서 p_frac 으로 교차검증
    'p_frac': 0.70,                            # 기록값 (AM_P 부피 몫)
    'se_frac_of_solid': 0.3323,
    'v_solid_um3': 241953.0,
    'lateral_um': 50.01, 'thickness_um': 112.87,
    'porosity_dem': 0.1428,
}
DH_GATE = 3.5                                  # CLAUDE.md 실용 규칙 (MPM SE 응력)
TOL_PFRAC, TOL_CLOSE = 0.02, 0.02              # 교차검증 허용오차
#: ★ 옛 캠페인 대조 (④ · validate_against_campaign) 의 밀도 세대 — 그 캠페인 침대가 만들어진 세대 (gen1 = AM 4.80 · SE 2.00).
#  `--dens-gen` 으로 새 세대를 골라도 이 대조는 **gen1 에 고정**한다: 대조 대상이 gen1 에서 센 개수이기 때문이다
#  (docs/density_generations_20261014.md · 범위 (가) 앞으로만 — 옛 결과는 만든 때의 밀도 그대로).
CAMPAIGN_DENS_GEN = 'gen1'


def bed_totals_measured(am_csv, se_csv, thickness_um, lateral_um):
    """★ 스캐폴드에서 **직접** 잰다 (2026-09-07 — 실물 덤프가 생긴 뒤로 이쪽이 정본).

    아래 `bed_totals()` 는 침대 파일이 없던 시절의 **역사적 경로**다: 옛 캠페인 요약치와
    12:4:1 반경 가설로 총량을 세웠다.  이제는 가정할 이유가 없다 — 원자 좌표가 있다.
    ⚠ 두 경로의 값이 다르면 그것은 **다른 realization** 이라는 뜻이지 오류가 아니다.
    """
    am = np.loadtxt(am_csv, delimiter=',')
    se = np.loadtxt(se_csv, delimiter=',')
    r_am, r_se = am[:, 4], se[:, 4]
    V_AM = float((4.0 / 3.0 * np.pi * r_am ** 3).sum()) * 1000.0 ** 3      # CSV 단위 → µm³
    S_AM = float((4.0 * np.pi * r_am ** 2).sum()) * 1000.0 ** 2
    V_SE = float((4.0 / 3.0 * np.pi * r_se ** 3).sum()) * 1000.0 ** 3
    Ah = lateral_um ** 2 * thickness_um
    return {'V_AM_um3': V_AM, 'S_AM_um2': S_AM, 'V_SE_um3': V_SE, 'Ah_um3': Ah,
            'phi_se_local': V_SE / (Ah - V_AM),
            'porosity': 1.0 - (V_AM + V_SE) / Ah,
            'se_frac_of_solid': V_SE / (V_AM + V_SE),
            'n_am': int(len(am)), 'n_se': int(len(se)),
            'source': 'measured_from_scaffold'}


def bed_totals(bed=BED):
    """총량 + **교차검증**.  어긋나면 예외 — 조용히 진행하지 않는다.

    ⚠ 2026-09-07 부로 이것은 **대비 경로**다 — 실물 스캐폴드가 있으면
    `bed_totals_measured()` 를 쓴다 (`--am/--se`).
    """
    nP, nS = bed['n_am_p'], bed['n_am_s']
    RP, RS = bed['r_am_p_um'], bed['r_am_s_um']
    V_P = nP * 4.0 / 3.0 * np.pi * RP ** 3
    V_S = nS * 4.0 / 3.0 * np.pi * RS ** 3
    V_AM = V_P + V_S
    S_AM = nP * 4.0 * np.pi * RP ** 2 + nS * 4.0 * np.pi * RS ** 2
    V_SE = bed['v_solid_um3'] * bed['se_frac_of_solid']
    p_meas = V_P / V_AM
    if abs(p_meas - bed['p_frac']) > TOL_PFRAC:
        raise SystemExit(f'⛔ p_frac 불일치: 계산 {p_meas:.4f} vs 기록 {bed["p_frac"]} '
                         f'⇒ 반경 가정 (R_P {RP}, R_S {RS}) 이 이 침대의 것이 아니다')
    close = (V_AM + V_SE) / bed['v_solid_um3'] - 1.0
    if abs(close) > TOL_CLOSE:
        raise SystemExit(f'⛔ V_solid 닫힘 실패: V_AM+V_SE 가 기록값과 {100 * close:+.2f} % 어긋난다')
    Ah = bed['lateral_um'] ** 2 * bed['thickness_um']
    return {'V_AM_um3': V_AM, 'S_AM_um2': S_AM, 'V_SE_um3': V_SE, 'Ah_um3': Ah,
            'phi_se_local': V_SE / (Ah - V_AM),
            'check_p_frac': p_meas, 'check_v_solid_rel': close}


def dh_gate(tot, lateral_um=BED['lateral_um'], n_grids=(192, 256, 288, 320, 384, 448, 512)):
    """① `d_h/dx` — dx = lateral_box / n_grid (real14 @384 → dx 0.141 µm 로 검증된 규약)."""
    from fit_dh_collapse import d_h_at_phi                       # 정본 공식을 그대로 쓴다
    dh = d_h_at_phi(tot['V_SE_um3'], tot['S_AM_um2'], tot['phi_se_local'], include_se=True)
    dh_void = d_h_at_phi(tot['V_SE_um3'], tot['S_AM_um2'], tot['phi_se_local'], include_se=False)
    rows = [{'n_grid': int(n), 'dx_um': lateral_um / n,
             'dh_over_dx': dh / (lateral_um / n),
             'pass': bool(dh / (lateral_um / n) >= DH_GATE)} for n in n_grids]
    return {'d_h_um': dh, 'd_h_void_only_um': dh_void, 'gate': DH_GATE,
            'n_grid_min_pass': int(math.ceil(DH_GATE * lateral_um / dh)), 'rows': rows,
            'scope': ('이 게이트는 **MPM 의 SE 응력** 해상도다.  STEP3 σ 격자와 다른 질문이고, '
                      '통과가 STEP3 안전을 뜻하지 **않는다** (STEP3 쪽은 SE neck — CL-72).')}


def additive_counts(tot, vgcf_wts=(1.0, 2.0, 3.0, 4.0), ptfe_wt=1.0, dens_gen=None):
    """② 프로덕션 경로를 그대로 부른다 (손계산 금지 — 옛 손계산은 3.7 % 틀렸다).
    `dens_gen` (2026-10-14 밤) — 밀도 세대 (None = gen1 · 옛 수 그대로).  행에는 세대 키를 넣지 않는다 (기록은 출력 JSON 최상위)."""
    from additives import recipe_counts_real
    out = []
    for v in vgcf_wts:
        r = recipe_counts_real({'VGCF': float(v), 'PTFE': float(ptfe_wt)},
                               tot['V_AM_um3'], tot['V_SE_um3'], dens_gen=dens_gen)
        out.append({'vgcf_wt_pct': float(v), 'ptfe_wt_pct': float(ptfe_wt),
                    'n_vgcf': r['VGCF']['n'], 'n_ptfe': r['PTFE']['n'],
                    'vgcf_vol_pct_of_solid': r['VGCF']['vol_pct_of_solid'],
                    'ptfe_vol_pct_of_solid': r['PTFE']['vol_pct_of_solid'],
                    'am_wt_pct': r['am_wt_pct'], 'se_wt_pct': r['se_wt_pct']})
    return out


def validate_against_campaign(tot, measured=((0.5, 13281), (1.0, 26696), (2.0, 53529), (4.0, 110120))):
    """옛 캠페인 실측 n_objects 와 대조 — 이 경로가 그 침대를 재현하는지 (VGCF 만, PTFE 없음).
    ★ 밀도 세대는 그 캠페인의 세대 (`CAMPAIGN_DENS_GEN` = gen1) 에 고정 — `--dens-gen` 과 무관하다."""
    from additives import recipe_counts_real
    rows = []
    for wt, meas in measured:
        n = recipe_counts_real({'VGCF': float(wt)}, tot['V_AM_um3'], tot['V_SE_um3'],
                               dens_gen=CAMPAIGN_DENS_GEN)['VGCF']['n']
        rows.append({'vgcf_wt_pct': wt, 'n_computed': int(n), 'n_measured': int(meas),
                     'rel_pct': 100.0 * (n / meas - 1.0)})
    return {'rows': rows, 'max_abs_rel_pct': max(abs(r['rel_pct']) for r in rows)}


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    tot = bed_totals()
    chk(f'① p_frac 교차검증 {tot["check_p_frac"]:.4f} ≈ 0.70', abs(tot['check_p_frac'] - 0.70) < TOL_PFRAC)
    chk(f'① V_solid 닫힘 {100 * tot["check_v_solid_rel"]:+.2f} %', abs(tot['check_v_solid_rel']) < TOL_CLOSE)
    # ② 반경이 틀리면 **거부**해야 한다 (조용한 통과 금지)
    bad = dict(BED, r_am_p_um=3.0)
    try:
        bed_totals(bad); raised = False
    except SystemExit:
        raised = True
    chk('② 반경이 틀리면 p_frac 검증이 거부한다 (조용히 통과 금지)', raised)
    g = dh_gate(tot)
    chk(f'③ d_h = {g["d_h_um"]:.4f} µm — 킷/real14 밴드(0.5~1.5 µm) 안', 0.4 < g['d_h_um'] < 1.6)
    chk(f'③ 최소 통과 n_grid = {g["n_grid_min_pass"]} · 288 통과', g['rows'][2]['pass'])
    chk('③ d_h/dx 는 n_grid 에 단조 증가', all(a['dh_over_dx'] < b['dh_over_dx']
                                                for a, b in zip(g['rows'], g['rows'][1:])))
    v = validate_against_campaign(tot)
    chk(f'④ 옛 캠페인 4행 재현 (최대 |Δ| {v["max_abs_rel_pct"]:.2f} % < 1 %)', v['max_abs_rel_pct'] < 1.0)
    c = additive_counts(tot)
    chk('⑤ VGCF 개수가 wt% 에 단조 증가', all(a['n_vgcf'] < b['n_vgcf'] for a, b in zip(c, c[1:])))
    chk('⑤ PTFE 는 1 wt% 고정인데 개수가 조금 는다 (총질량이 늘기 때문 — 규약 확인)',
        c[0]['n_ptfe'] < c[-1]['n_ptfe'] and (c[-1]['n_ptfe'] / c[0]['n_ptfe'] - 1) < 0.10)
    #  ── ★ 밀도 세대 (2026-10-14 밤 · 1저자 결정 · docs/density_generations_20261014.md) — 시험 먼저 ──────────────────
    #     옛 코드: additive_counts 에 dens_gen 이 없고 (gen1 고정) · --dens-gen 없음 → ⑥–⑨ FAIL.
    #     계약: 미지정 = 옛 수 그대로 · 기록 없음 / 지정 = 그 세대 밀도로 개수 + 출력 JSON 에 기록 / 옛 캠페인 대조 (④) 는
    #     그 캠페인이 만들어진 세대 (gen1) 에 **고정** — 랩 세대를 고르면 대조가 깨지는 것이 아니라 대조 대상이 gen1 임을 적는다.
    def _ok(fn):
        try:
            return bool(fn())
        except (Exception, SystemExit):                                   # noqa: BLE001 — 옛 코드의 TypeError 도 FAIL
            return False

    def _rej(fn):
        try:
            fn()
            return False
        except SystemExit:
            return True
    LAB = 'lab20261014'
    chk('⑥ additive_counts 미지정 = gen1 명시 (같은 수) · 기록 키 없음',
        _ok(lambda: additive_counts(tot) == additive_counts(tot, dens_gen=None) == c
            and additive_counts(tot, dens_gen='gen1') == c
            and not any('dens_gen' in r for r in c)))

    def _six():
        cl = additive_counts(tot, dens_gen=LAB)
        m_g = tot['V_AM_um3'] * 4.80 + tot['V_SE_um3'] * 2.00          # 독립 산술 — 고체 질량 (gen1 · lab)
        m_l = tot['V_AM_um3'] * 4.85 + tot['V_SE_um3'] * 1.64
        return (all(abs(l_['n_vgcf'] / g_['n_vgcf'] - m_l / m_g) < 2.0 / g_['n_vgcf'] + 1e-12
                    and l_['am_wt_pct'] > g_['am_wt_pct'] and l_['se_wt_pct'] < g_['se_wt_pct'] for l_, g_ in zip(cl, c))
                and m_l < m_g)
    chk('⑦ lab = 랩 밀도 (AM 4.85 · SE 1.64) 로 개수 — VGCF 개수 비 = 고체 질량 비 (±반올림) · AM wt% ↑ · SE wt% ↓', _ok(_six))
    chk('⑧ 옛 캠페인 대조는 gen1 고정 (CAMPAIGN_DENS_GEN) — 같은 1 % 안 · 모르는 세대 = 거부',
        _ok(lambda: CAMPAIGN_DENS_GEN == 'gen1' and validate_against_campaign(tot)['max_abs_rel_pct'] < 1.0
            and _rej(lambda: additive_counts(tot, dens_gen='nope'))))

    def _cli():
        import subprocess as _sp
        import tempfile as _tf
        me = os.path.abspath(__file__)
        with _tf.TemporaryDirectory() as td:
            o0, ol = os.path.join(td, 'a.json'), os.path.join(td, 'b.json')
            r0 = _sp.run([sys.executable, me, '--out', o0], capture_output=True, text=True)
            rl = _sp.run([sys.executable, me, '--out', ol, '--dens-gen', LAB], capture_output=True, text=True)
            rb = _sp.run([sys.executable, me, '--dens-gen', 'nope'], capture_output=True, text=True)
            if r0.returncode or rl.returncode:
                return False
            j0, jl = json.load(open(o0)), json.load(open(ol))
        keys = ('dens_gen', 'dens_g_cm3', 'dens_carried_from_gen1')
        return (not any(k in j0 for k in keys) and 'dens_gen' not in r0.stdout and jl.get('dens_gen') == LAB
                and jl.get('dens_g_cm3', {}).get('SE') == 1.64 and jl.get('campaign_validation_dens_gen') == 'gen1'
                and 'campaign_validation_dens_gen' not in j0 and f'dens_gen = {LAB}' in rl.stdout and rb.returncode != 0
                and jl['campaign_validation'] == j0['campaign_validation'] and jl['additive_counts'] != j0['additive_counts'])
    chk('⑨ CLI --dens-gen: 미지정 JSON · 화면에 세대 키 없음 · 지정 = 세대 · 실제 값 · 캠페인 대조 세대 (gen1) 기록 · 개수만 바뀜 · 모르는 이름 rc ≠ 0',
        _ok(_cli))
    print(f'\nphase_a_precompute selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Phase A 런 전 사전계산 (GPU·스캐폴드 파일 불요)')
    ap.add_argument('--am', default='', help='AM 스캐폴드 CSV (있으면 **실측** 경로)')
    ap.add_argument('--se', default='', help='SE 스캐폴드 CSV')
    ap.add_argument('--thickness-um', type=float, default=BED['thickness_um'])
    ap.add_argument('--lateral-um', type=float, default=BED['lateral_um'])
    ap.add_argument('--out', default='')
    ap.add_argument('--dens-gen', default=None,
                    help='밀도 세대 (additives.DENS_GENERATIONS 의 키 — gen1 · lab20261014 …).  생략 = gen1 (옛 출력 그대로 · 기록 없음).  '
                         '주면 ② 첨가제 개수를 그 세대 밀도로 내고 화면 · JSON 에 dens_gen · 실제 값 · 옮긴 상을 기록한다.  '
                         '③ 옛 캠페인 대조는 gen1 고정 (그 캠페인의 세대 · campaign_validation_dens_gen).  '
                         'docs/density_generations_20261014.md')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    _dens_rec = None
    if a.dens_gen is not None:                       # 지정했을 때만 — 모르는 이름은 additives.dens_record 가 거부 (계산 전)
        from additives import dens_record
        _dens_rec = dens_record(a.dens_gen)
        print(f"밀도 세대 dens_gen = {a.dens_gen}  (AM {_dens_rec['dens_g_cm3']['AM']:g} · SE {_dens_rec['dens_g_cm3']['SE']:g} g/cm³ "
              f"· gen1 값을 옮긴 상: {' · '.join(_dens_rec['dens_carried_from_gen1']) or '없음'} · 옛 캠페인 대조 = {CAMPAIGN_DENS_GEN} 고정)")

    if a.am and a.se:
        tot = bed_totals_measured(a.am, a.se, a.thickness_um, a.lateral_um)
        print(f'★ 실측 경로 — 스캐폴드에서 직접 (AM {tot["n_am"]:,} · SE {tot["n_se"]:,})')
        print(f'  porosity {100 * tot["porosity"]:.3f} %  ·  SE/solid {100 * tot["se_frac_of_solid"]:.2f} vol%')
    else:
        tot = bed_totals()
        print('⚠ 대비 경로 — 옛 캠페인 요약치 + 반경 가설 (스캐폴드를 주면 실측한다)')
    g = dh_gate(tot, lateral_um=a.lateral_um)
    cts = additive_counts(tot, dens_gen=a.dens_gen)
    val = validate_against_campaign(tot)

    if 'check_p_frac' in tot:
        print(f"침대 {BED['case']}  ·  AM_P {BED['n_am_p']} (R {BED['r_am_p_um']} µm) · "
              f"AM_S {BED['n_am_s']} (R {BED['r_am_s_um']}) · 상자 "
              f"{BED['lateral_um']}² × {BED['thickness_um']} µm")
        print(f"  교차검증  p_frac {tot['check_p_frac']:.4f} (기록 {BED['p_frac']}) · "
              f"V_solid 닫힘 {100 * tot['check_v_solid_rel']:+.2f} %\n")
    else:
        print(f"  상자 {a.lateral_um}² × {a.thickness_um} µm  ·  "
              f"V_AM {tot['V_AM_um3']:,.0f} µm³ · S_AM {tot['S_AM_um2']:,.0f} µm² · "
              f"V_SE {tot['V_SE_um3']:,.0f}\n")
    print(f"① d_h = {g['d_h_um']:.4f} µm (잔여공극만 {g['d_h_void_only_um']:.4f}) · "
          f"φ_SE_local {tot['phi_se_local']:.4f}")
    print(f"   게이트 d_h/dx ≥ {DH_GATE}   ★ 최소 통과 n_grid = {g['n_grid_min_pass']}")
    print('   n_grid    dx(µm)   d_h/dx   판정')
    for r in g['rows']:
        print(f"     {r['n_grid']:4}   {r['dx_um']:.4f}   {r['dh_over_dx']:6.2f}   "
              f"{'✅' if r['pass'] else '⚠ 미달 → 하한 라벨'}")
    print(f"   ⚠ {g['scope']}\n")
    print('② 첨가제 객체 수 (프로덕션 경로 recipe_counts_real)')
    print('   레시피             VGCF n     PTFE n   VGCF vol%  PTFE vol%   AM wt%  SE wt%')
    for c in cts:
        print(f"   VGCF {c['vgcf_wt_pct']:.0f} + PTFE 1  {c['n_vgcf']:8,}  {c['n_ptfe']:7,}   "
              f"{c['vgcf_vol_pct_of_solid']:7.3f}   {c['ptfe_vol_pct_of_solid']:7.3f}   "
              f"{c['am_wt_pct']:6.2f}  {c['se_wt_pct']:6.2f}")
    print(f"\n③ 옛 캠페인 대조 (VGCF 만) — 최대 |Δ| {val['max_abs_rel_pct']:.2f} %")
    for r in val['rows']:
        print(f"   VGCF {r['vgcf_wt_pct']:<4} 계산 {r['n_computed']:7,}  실측 {r['n_measured']:7,}  "
              f"Δ {r['rel_pct']:+6.2f} %")
    print('\n★ 각도 선별은 별도 도구다 (입자 위치 필요):  python3 scripts/step4_angular_risk.py --am <am> --se <se>')

    if a.out:
        from measure_provenance import provenance
        os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
        d = {'bed': BED, 'totals': tot, 'dh_gate': g, 'additive_counts': cts,
             'campaign_validation': val,
             'angular_screen': 'scripts/step4_angular_risk.py (별도 산출물)',
             **({} if _dens_rec is None else {**_dens_rec, 'campaign_validation_dens_gen': CAMPAIGN_DENS_GEN}),
             **provenance()}
        json.dump(d, open(a.out, 'w'), ensure_ascii=False, indent=1, default=float)
        print(f'\n  → {a.out}')
