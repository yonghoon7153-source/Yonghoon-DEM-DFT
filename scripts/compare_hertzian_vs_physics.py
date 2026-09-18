"""
Compare Hertzian vs Physics contact-mode σ and τ_Lap_eff across all cases.

Uses already-stored fields in full_metrics.json:
  sigma_full_mScm          ← Hertzian (LIGGGHTS geometric contact area)
  sigma_full_mScm_physics  ← Physics (Tabor+volume plastic film)

Reports per-case:
  σ ratio (P/H)
  τ_Lap_eff (both modes)
  Literature match (Minnmann 2021, Wang 2023) for EACH mode

Key question: which mode gives better EIS agreement for LPSCl?
  Expected (per Mohayman 2025 DFT, B/G = 1.47 < 1.75):
  LPSCl is brittle-dominated → Hertzian should win (physics over-scales)

Usage:
  python3 scripts/compare_hertzian_vs_physics.py
"""
from __future__ import annotations
import os, json, math, csv
from collections import defaultdict


SIGMA_GRAIN = 3.0  # mS/cm, LPSCl


def _tau(phi, sig):
    if not (phi and sig and phi > 0 and sig > 0):
        return None
    return math.sqrt(phi * SIGMA_GRAIN / sig)


def load_cases():
    cases = []
    for root, _, files in os.walk('webapp'):
        if 'full_metrics.json' not in files:
            continue
        try:
            m = json.load(open(f'{root}/full_metrics.json'))
        except Exception:
            continue
        cid = os.path.basename(root)
        # Find name from meta.json
        name = cid
        for base in ('webapp/uploads', 'webapp/results'):
            mp = f'{base}/{cid}/meta.json'
            if os.path.exists(mp):
                try:
                    name = json.load(open(mp)).get('name', cid)
                except Exception:
                    pass
                break
        phi = m.get('phi_se')
        sh = m.get('sigma_full_mScm')
        sp = m.get('sigma_full_mScm_physics')
        if not (phi and sh):
            continue
        tau_h = _tau(phi, sh)
        tau_p = _tau(phi, sp) if sp else None
        cases.append({
            'case_id':  cid,
            'name':     name,
            'path':     root,
            'phi_SE':   phi,
            'sigma_H':  sh,
            'sigma_P':  sp,
            'tau_Le_H': tau_h,
            'tau_Le_P': tau_p,
            'tau_sq_H': tau_h**2 if tau_h else None,
            'tau_sq_P': tau_p**2 if tau_p else None,
            'sigma_ratio_PH': (sp/sh) if (sp and sh and sh > 0) else None,
        })
    return cases


def main():
    cases = load_cases()
    with_both = [c for c in cases if c['sigma_P'] is not None]
    print(f"Total cases: {len(cases)}   with physics σ: {len(with_both)}\n")

    #  ⛔ 데이터가 없으면 **여기서 뜻이 통하게 선다** (원장 `GAP3-38`, 2026-09-18).
    #     전에는 `Total cases: 0` 을 찍고 그냥 진행하다 한참 아래 `:111` 에서
    #     `ValueError: min() arg is an empty sequence` 로 죽었다 — 읽는 사람에게
    #     *"데이터가 없다"* 가 아니라 *"코드가 깨졌다"* 로 보인다.
    #  ⚠ 이 스크립트는 **로컬 전용**이다: 케이스는 `webapp/{uploads,results,archive}/`
    #     에 있고 그 셋은 전부 `.gitignore` 에 있다 (`.gitignore:5-7`) ⇒ 리포만 받은
    #     기계에서는 **언제나 0 건**이다.  그것은 결함이 아니라 이 스크립트의 전제다.
    if not with_both:
        print('⛔ physics σ 를 가진 케이스가 0 건이다 — 비교할 것이 없다.\n'
              '   이 스크립트는 로컬 webapp 데이터를 읽는다 '
              '(`webapp/{uploads,results,archive}/<cid>/full_metrics.json`).\n'
              '   그 폴더들은 `.gitignore:5-7` 에 있어 리포에 딸려오지 않는다.\n'
              '   ⇒ 데이터가 있는 기계에서 돌리거나, WEBAPP_*_FOLDER 를 연결할 것.')
        return 2

    # σ ratio summary
    ratios = [c['sigma_ratio_PH'] for c in with_both if c['sigma_ratio_PH']]
    if ratios:
        import statistics as S
        print(f"=== σ_Physics / σ_Hertzian ratio (n={len(ratios)}) ===")
        print(f"  median: {S.median(ratios):.3f}")
        print(f"  mean:   {S.mean(ratios):.3f}")
        print(f"  p25:    {sorted(ratios)[len(ratios)//4]:.3f}")
        print(f"  p75:    {sorted(ratios)[3*len(ratios)//4]:.3f}")
        print(f"  range:  [{min(ratios):.3f}, {max(ratios):.3f}]")

    # Literature comparison (both modes)
    print(f"\n=== LITERATURE VALIDATION — Hertzian vs Physics ===\n")
    anchors = [
        ('Minnmann 2021 42% CAM',  0.44, 4.30),
    ]
    #  ⛔ 뺀 앵커 셋 (2026-09-18, 원장 `GAP3-37`) — 값은 보존한다:
    #    ('Wang 2023 70% CAM', 0.26, 7.78) · ('Wang 2023 80% CAM', 0.16, 17.24)
    #       출처가 리포 전체에 **0 건** (litdb 정본 274 편에 `wang2023*` 없음).
    #       두 점이 porosity 를 **정확히 4.0 %** 로 함의하고(Minnmann 규약),
    #       두 점 적합 γ=0.855 가 정본 밴드 γ∈[0.32,0.67] **밖**이다.
    #    ('Dewald 2021 25% NCM', 0.65, 2.4)
    #       **Minnmann 과 같은 논문**이다 (DOI `10.1149/1945-7111/abf8d7` 동일) ⇒ 이중계상.

    # Dedup by (name, round(phi, 2))
    seen = {}
    for c in with_both:
        key = (c['name'], round(c['phi_SE'], 2))
        prefer_archive = '/archive/' in c['path']
        if key not in seen or prefer_archive:
            seen[key] = c
    dedup = list(seen.values())

    for anchor_name, phi_ref, tau2_ref in anchors:
        closest = min(dedup, key=lambda c: abs(c['phi_SE'] - phi_ref))
        dphi = abs(closest['phi_SE'] - phi_ref)
        h_err = 100 * (closest['tau_sq_H'] - tau2_ref) / tau2_ref
        p_err = (100 * (closest['tau_sq_P'] - tau2_ref) / tau2_ref) if closest['tau_sq_P'] else None
        print(f"  {anchor_name}")
        print(f"    ref  : φ_SE={phi_ref:.2f}  τ²={tau2_ref:.2f}")
        print(f"    ours : {closest['name']:25s} (φ={closest['phi_SE']:.3f}, Δφ={dphi:.3f})")
        print(f"    Hertzian : σ={closest['sigma_H']:.4f}  τ²={closest['tau_sq_H']:.2f}  err={h_err:+.0f}%")
        if p_err is not None:
            print(f"    Physics  : σ={closest['sigma_P']:.4f}  τ²={closest['tau_sq_P']:.2f}  err={p_err:+.0f}%")
            winner = "HERTZIAN" if abs(h_err) < abs(p_err) else "PHYSICS"
            print(f"    → {winner} fits better by {abs(h_err - p_err):.1f}pp")
        print()

    # Write per-case comparison CSV
    out_csv = '/tmp/hertzian_vs_physics.csv'
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(with_both[0].keys()) if with_both else [],
                           extrasaction='ignore')
        w.writeheader()
        w.writerows(with_both)
    print(f"Per-case CSV → {out_csv}")

    # Top 5 cases where Physics differs most from Hertzian
    print(f"\n=== TOP 5 CASES — largest σ_P / σ_H divergence ===")
    diff_cases = sorted([c for c in with_both if c['sigma_ratio_PH']],
                        key=lambda c: abs(c['sigma_ratio_PH'] - 1.0), reverse=True)[:5]
    print(f"  {'name':35s} {'φ_SE':>7s} {'σ_H':>8s} {'σ_P':>8s} {'P/H':>6s}")
    for c in diff_cases:
        print(f"  {c['name'][:34]:35s} {c['phi_SE']:>7.3f} "
              f"{c['sigma_H']:>8.4f} {c['sigma_P']:>8.4f} {c['sigma_ratio_PH']:>6.2f}")
    return 0


if __name__ == '__main__':
    #  ⛔ `main()` 의 반환을 **종료코드로 흘린다** (`GAP3-38`/`GAP3-39` 같은 패턴).
    #     전에는 반환을 버려서 어떤 실패도 rc=0 이 됐다.
    raise SystemExit(main())
