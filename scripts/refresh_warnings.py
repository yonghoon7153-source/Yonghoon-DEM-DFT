#!/usr/bin/env python3
"""
Backfill warnings field on all already-persisted full_metrics.json files.

Why: analyze_contacts.py checked electronic_active_fraction BEFORE the
network solver ran, so the warning was never stored. The app-level fix
(_refresh_post_network_warnings in webapp/app.py) only applies to newly
analysed cases. This script replays the same warning logic over the 59
existing results to backfill.

Rules applied:
  • <10%  → critical  electronic_dead       (AM-AM percolation 없음)
  • <50%  → critical  electronic_low        (대량 dead AM)
  • <80%  → warning   electronic_marginal   (일부 dead AM)

Preserves:
  • any existing warnings (dedup by type)
  • disabled_warnings filter
  • warnings emitted by analyze_contacts.py for porosity/CN/tau/etc.

Usage:
  python3 scripts/refresh_warnings.py                     # all cases
  python3 scripts/refresh_warnings.py 260421_213656_78ec86  # selected
"""
from __future__ import annotations
import os, sys, json, glob


RESULTS = 'webapp/results'


def refresh_one(case_id: str) -> tuple[str, int]:
    fm_path = os.path.join(RESULTS, case_id, 'full_metrics.json')
    if not os.path.exists(fm_path):
        return 'no_full_metrics', 0
    try:
        with open(fm_path) as f:
            m = json.load(f)
    except Exception as e:
        return f'parse_error:{e}', 0

    existing = list(m.get('warnings') or [])
    known_types = {w.get('type') for w in existing if isinstance(w, dict)}
    disabled = set(m.get('disabled_warnings') or [])
    new_w: list[dict] = []

    def _add(tag, severity, msg):
        if tag not in known_types:
            new_w.append({'type': tag, 'severity': severity, 'msg': msg})

    # Electronic Active AM (AM-AM percolation)
    el_active = m.get('electronic_active_fraction')
    if el_active is not None:
        pct = el_active * 100
        if pct < 10:
            _add('electronic_dead', 'critical',
                 f"Electronic Active AM={pct:.0f}% (<10%): 도전재 필수! AM-AM percolation 없음")
        elif pct < 50:
            _add('electronic_low', 'critical',
                 f"Electronic Active AM={pct:.0f}% (<50%): 대량 dead AM, 도전재 강력 권장")
        elif pct < 80:
            _add('electronic_marginal', 'warning',
                 f"Electronic Active AM={pct:.0f}% (<80%): 일부 dead AM, 도전재 권장")

    # σ_ionic
    sig = m.get('sigma_full_mScm')
    if sig is not None:
        if sig < 0.005:
            _add('sigma_ionic_too_low', 'critical',
                 f"σ_ionic={sig*1000:.2f} μS/cm (<5 μS/cm): 네트워크 거의 비전도 — 병목 극단 또는 솔버 이상")
        elif sig < 0.03:
            _add('sigma_ionic_low', 'warning',
                 f"σ_ionic={sig:.3f} mS/cm (<0.03): 낮은 이온전도도 — bottleneck regime 의심")

    # τ_Lap_eff
    tau_le = m.get('tortuosity_lap_eff') or m.get('tau_lap_eff')
    if tau_le is not None:
        if tau_le > 15:
            _add('tau_lap_eff_extreme', 'critical',
                 f"τ_Lap_eff={tau_le:.1f} (>15): 극단 bottleneck regime, Wang 70% CAM 레짐 상당")
        elif tau_le > 8:
            _add('tau_lap_eff_high', 'warning',
                 f"τ_Lap_eff={tau_le:.1f} (>8): bottleneck regime, scaling law ±20% 범위 밖 가능성")

    # Constriction ratio
    cstr = m.get('constriction_pct') or m.get('constriction_fraction_pct')
    if cstr is not None and cstr > 90:
        _add('constriction_dominant', 'warning',
             f"Constriction 비율={cstr:.0f}% (>90%): 접촉 저항이 bulk 저항을 10배 이상 지배")

    # τ_Lap_eff / τ_Dij gap
    tau_dij = m.get('tortuosity_mean') or m.get('tau_dij')
    if tau_le is not None and tau_dij is not None and tau_dij > 0:
        ratio = tau_le / tau_dij
        if ratio > 10:
            _add('tau_ratio_extreme', 'warning',
                 f"τ_Lap_eff/τ_Dij={ratio:.1f}× (>10×): 기하 경로와 실제 전도도 경로 완전 분리")

    # Physics vs Hertzian divergence
    sig_h = m.get('sigma_full_mScm')
    sig_p = m.get('sigma_full_mScm_physics')
    if sig_h and sig_p and sig_h > 0:
        rel = abs(sig_p - sig_h) / sig_h
        if rel > 0.5:
            _add('physics_hertzian_divergence', 'warning',
                 f"Physics σ / Hertzian σ = {sig_p/sig_h:.2f}× (|Δ|>50%): "
                 "접촉 모델 민감도 큼 — upper bound 해석 권장")

    # Porosity range
    poro = m.get('porosity')
    if poro is not None:
        if poro < 8:
            _add('porosity_too_low', 'critical',
                 f"Porosity={poro:.1f}% (<8%): 과압축 — 물리적 한계 근접")
        elif poro > 30:
            _add('porosity_too_high', 'warning',
                 f"Porosity={poro:.1f}% (>30%): 압축 미완료 — DEM settling 재확인")

    merged = [w for w in (existing + new_w) if w.get('type') not in disabled]
    m['warnings'] = merged
    m['warning_count'] = len(merged)

    with open(fm_path, 'w') as f:
        json.dump(m, f, indent=2, default=str)

    return 'ok', len(new_w)


def main():
    if not os.path.isdir(RESULTS):
        print(f'ERROR: {RESULTS} not found (run from project root)')
        sys.exit(1)

    if len(sys.argv) > 1:
        case_ids = sys.argv[1:]
    else:
        case_ids = sorted(os.listdir(RESULTS))

    stats = {'ok': 0, 'no_full_metrics': 0}
    added_total = 0
    print(f'Refreshing warnings for {len(case_ids)} case(s)...\n')
    for cid in case_ids:
        status, added = refresh_one(cid)
        stats[status] = stats.get(status, 0) + 1
        added_total += added
        if added > 0:
            # Reload to show which warning was added
            fm = os.path.join(RESULTS, cid, 'full_metrics.json')
            try:
                wm = json.load(open(fm)).get('warnings', [])
                tags = ','.join(w.get('type', '?') for w in wm) or '—'
            except Exception:
                tags = '?'
            print(f'  [{status:16s}]  +{added}  {cid}  [{tags}]')

    print()
    print(f'Summary:')
    print(f'  Cases processed:  {stats.get("ok", 0)}')
    print(f'  No full_metrics:  {stats.get("no_full_metrics", 0)}')
    print(f'  New warnings:     {added_total}')


if __name__ == '__main__':
    main()
