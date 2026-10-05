"""Physics 수송 tortuosity < 1 (MODEL_BELOW_CONTINUUM_BOUND 10 건) 의 원인 점검 — 커밋된 merged/*/metrics_flat.csv 만 읽는다 (계산 0).

수송 tortuosity = φ_sphere / σ_ratio  (= tau_flux 의 φ_mc / f_mc · L 비는 약분된다) — 1 이 연속체 하한 (Wiener 병렬 상한 σ_eff ≤ φ·σ₀).
같은 망의 CONTACT_FREE 해 (`sigma_bulk_net` = 협착 항 0 · 간선 · R_bulk 는 두 모드 같음) 를 같은 식에 넣어 본다.

    python3 docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/tau_below1_check.py
"""
import csv
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(os.path.dirname(HERE), 'merged')
K = 'network_dual.{}.{}'


def num(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def rng(v, nd=3):
    v = [x for x in v if x is not None]
    return f'{min(v):.{nd}f}–{max(v):.{nd}f}' if v else '—'


for coh in ('lhs', 'lhsx'):
    rows = list(csv.DictReader(open(os.path.join(MERGED, coh, 'metrics_flat.csv'), encoding='utf-8')))
    P = []
    for r in rows:
        phi = num(r['phi_se'])
        sH, sP, sC = (num(r[K.format('hertzian', 'sigma_full')]), num(r[K.format('physics', 'sigma_full')]),
                      num(r[K.format('hertzian', 'sigma_bulk_net')]))
        cP = num(r[K.format('physics', 'sigma_bulk_net')])
        if not sH:
            continue                                            # 비관통 (σ = 0) — 수송 tortuosity 없음
        assert sC == cP, (r['case'], sC, cP)                  # CONTACT_FREE 해는 두 모드 같다 (협착 항만 다르다)
        P.append(dict(case=r['case'], phi=phi, phi_mc=num(r['phi_se_mass_conserving']), tH=phi / sH, tP=phi / sP, sC=sC,
                      shH=num(r['constriction_power_share_ion_hertz']), shP=num(r['constriction_power_share_ion_physics']),
                      cn=num(r['se_se_cn']), pss=num(r['porosity_spheresum']), pu=num(r['porosity_union'])))
    C = [x for x in P if x['sC'] is not None]
    blank = [x for x in P if x['sC'] is None]
    print(f'== {coh} · 관통 {len(P)}')
    print(f'   수송 tortuosity Hertz {rng([x["tH"] for x in P])} · Physics {rng([x["tP"] for x in P])} · Physics < 1 = {sum(x["tP"] < 1 for x in P)} · '
          f'Physics 1.00–1.15 = {sum(1 <= x["tP"] < 1.15 for x in P)} · Hertz < 1 = {sum(x["tH"] < 1 for x in P)}')
    print(f'   σ_ion Physics/Hertz < 1 = {sum(x["tP"] > x["tH"] for x in P)} / {len(P)}')
    print(f'   CONTACT_FREE 계산 {len(C)} · σ_cf > φ (= 접촉 저항 없는 해가 이미 1 아래) {sum(x["sC"] > x["phi"] for x in C)} · '
          f'σ_cf > 1 (고체 SE 펠릿보다 큼) {sum(x["sC"] > 1 for x in C)} · 최대 {max((x["sC"] for x in C), default=float("nan")):.3f} · '
          f'빈칸 {len(blank)} (φ_mc {rng([x["phi_mc"] for x in blank])})')
    B = [x for x in P if x['tP'] < 1]
    if B:
        print(f'   Physics < 1: {[x["case"] for x in B]}')
        print(f'     φ_mc {rng([x["phi_mc"] for x in B])} · Physics {rng([x["tP"] for x in B])} · Hertz {rng([x["tH"] for x in B], 2)} · '
              f'등방 HS 한계 (3−φ_mc)/2 {rng([(3 - x["phi_mc"]) / 2 for x in B])}')
        print(f'     협착 전력 몫 Hertz {rng([100 * x["shH"] for x in B], 1)} % · Physics {rng([100 * x["shP"] for x in B], 1)} % · '
              f'SE–SE 이웃 {rng([x["cn"] for x in B], 1)} · porosity_spheresum {rng([x["pss"] for x in B], 2)} % · porosity_union {rng([x["pu"] for x in B], 2)} %')
