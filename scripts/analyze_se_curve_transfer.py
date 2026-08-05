#!/usr/bin/env python3
"""SE 응답곡선 σ(φ) — 재현 · 해상도 · 재하율 · 베드-전이 4판정.

`am_load_balance_jam.REAL14_SE_CURVE` 는 real_14 베드에서 잰 11점이고, 색인을
두께가 아니라 φ_SE_local = V_SE/(A·h − V_AM) 로 두어 "다른 베드에도 쓸 수 있다"고
전제한다.  이 스크립트는 그 전제를 mpm3d_compaction 산출 json 으로 판정한다.

═══ ★ 재하율 게이트 (2026-08-06 교훈) ═══════════════════════════════════════════
mpm3d 의 기본 기하 규칙 vmax = 0.008·(WALL0−FLOOR) 은 플래튼 속도를 **베드 높이에
비례**시킨다 → 두께가 다른 두 베드는 재료·해상도가 같아도 재하율이 다르다.
실측: real_14(31.3 µm) V/c_P 0.031 vs kit_ps_7_3(113.9 µm) 0.105 (3.4배; 후자는
V/c_S=0.75 = 전단파속의 75 % 로 준정적이 전혀 아니다).  소성은 전단 지배라 그
wallP 에는 관성이 크게 섞이고, 이 상태로 잰 σ 차이는 **베드 기전과 분리되지 않는다**.

→ 그래서 이 도구는 두 베드를 비교하기 전에 json 의 platen_mach_V_over_cP 를 읽어
  **재하율이 안 맞으면 비교를 거부한다** (경고가 아니라 거부 — 조용히 틀린 답이
  나오는 게 이 실수의 본질이었다).  --allow-rate-mismatch 로만 강제 통과.

사용:
  python3 scripts/analyze_se_curve_transfer.py --dir ~/Yonghoon-DEM-DFT/se_curve \\
      --ref-kit  ~/Yonghoon-DEM-DFT/se_curve/kit_real14  --ref-glob  'xfer_kit_real14_g192_e*.json' \\
      --test-kit ~/Yonghoon-DEM-DFT/kit_ps_7_3           --test-glob 'xfer_kitm03_g192_e*.json'
  python3 scripts/analyze_se_curve_transfer.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

#: 두 베드의 V/c_P 가 이 비율 안이면 "같은 재하율"로 본다.  0.03 vs 0.031 = 1.03 통과,
#: 0.031 vs 0.105 = 3.4 거부.  관성 응력이 속도에 강하게 의존하므로 넉넉하게 두지 않는다.
RATE_TOL_RATIO = 1.15

#: 사전등록 판정 문턱 (φ 축에서 겹친 σ 상대차).
PASS_PCT, FAIL_PCT = 10.0, 25.0


def bed_volumes(kit_dir):
    """킷의 (V_AM, V_SE, A, lateral) — plan_se_curve_targets 와 같은 규약."""
    from plan_se_curve_targets import bed_volumes as _bv
    return _bv(kit_dir)


def phi_se_local(h_um, v_am, v_se, area):
    """φ = V_SE / (A·h − V_AM).  자유공간이 0 이하면 nan (물리적으로 도달 불가)."""
    free = area * float(h_um) - v_am
    return float(v_se) / free if free > 0 else float('nan')


def load_points(pattern, kit_dir, root='.'):
    """glob → [(φ, σ, mach_cP, path)] (φ 오름차순).  두께·응력이 없는 json 은 건너뛴다."""
    v_am, v_se, area, _ = bed_volumes(kit_dir)
    out = []
    for p in sorted(glob.glob(os.path.join(root, pattern))):
        d = json.load(open(p))
        h, s = d.get('thickness_um'), d.get('final_stress_GPa')
        if h is None or s is None:
            continue
        out.append((phi_se_local(h, v_am, v_se, area), float(s),
                    d.get('platen_mach_V_over_cP'), p))
    return sorted(out, key=lambda r: r[0]), (v_am, v_se, area)


def _rate_of(points, label):
    """점들의 V/c_P 대푯값.  런마다 다르면(설정 실수) 즉시 알린다."""
    vals = [m for *_, m, _ in [(0, 0, m, p) for _, _, m, p in points] if m is not None]
    if not vals:
        return None, f'{label}: json 에 platen_mach_V_over_cP 없음 (구 산출물)'
    lo, hi = min(vals), max(vals)
    if hi > 0 and hi / max(lo, 1e-12) > 1.02:
        return float(np.median(vals)), f'{label}: 런마다 재하율이 다름 ({lo:.3f}..{hi:.3f})'
    return float(np.median(vals)), None


def compare(ref_pts, test_pts, ref_label='ref', test_label='test'):
    """test 의 각 φ 에서 ref 를 보간해 상대차.  ref 범위 밖은 외삽으로 표시."""
    rp = np.array([p for p, _, _, _ in ref_pts])
    rs = np.array([s for _, s, _, _ in ref_pts])
    rows = []
    for phi, s, _, path in test_pts:
        s_ref = float(np.interp(phi, rp, rs))
        rows.append({'phi': phi, 's_test': s, 's_ref': s_ref,
                     'pct': (100.0 * (s - s_ref) / s_ref) if s_ref > 0 else float('nan'),
                     'ratio': (s / s_ref) if s_ref > 0 else float('inf'),
                     'extrap': bool(phi < rp[0] or phi > rp[-1]),
                     'file': os.path.basename(path)})
    return rows


def print_table(rows, ref_label, test_label):
    print(f'   {"φ":>8}{"σ_" + test_label:>12}{"σ_" + ref_label:>12}{"Δ%":>9}{"배수":>8}')
    for r in rows:
        d = '   nan' if not np.isfinite(r['pct']) else f"{r['pct']:8.1f}"
        rat = '   —  ' if not np.isfinite(r['ratio']) else f"{r['ratio']:7.2f}×"
        print(f"   {r['phi']:8.4f}{r['s_test']:12.4f}{r['s_ref']:12.4f}{d}{rat}"
              + ('  ← 외삽' if r['extrap'] else ''))


def verdict(rows, what):
    """사전등록 문턱으로 판정.  σ→0 근방(ref<0.01)은 상대차가 발산하므로 제외하고 별도 표시."""
    usable = [r for r in rows if np.isfinite(r['pct']) and r['s_ref'] >= 0.01]
    skipped = len(rows) - len(usable)
    if not usable:
        print(f'   판정 불가 — 비교 가능한 점 없음 (σ_ref < 0.01 제외 {skipped})')
        return None
    a = [abs(r['pct']) for r in usable]
    med, mx = float(np.median(a)), float(max(a))
    tag = ('통과 (전이 성립)' if mx < PASS_PCT else
           '회색 — 밴드로 실어야 함' if mx < FAIL_PCT else '★ 기각')
    print(f'   → |Δ| 중앙 {med:.1f} % · 최대 {mx:.1f} %  ⇒ **{tag}**'
          + (f'   (σ_ref<0.01 인 {skipped}점 제외)' if skipped else ''))
    return {'what': what, 'median_abs_pct': med, 'max_abs_pct': mx, 'verdict': tag}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default='.', help='json 들이 있는 디렉토리 (se_curve)')
    ap.add_argument('--ref-kit', help='기준 베드 킷 (am/se_scaffold.csv)')
    ap.add_argument('--ref-glob', default='xfer_kit_real14_g192_e*.json')
    ap.add_argument('--test-kit', help='대상 베드 킷')
    ap.add_argument('--test-glob', default='xfer_kitm03_g192_e*.json')
    ap.add_argument('--repro', nargs=2, metavar=('NEW', 'STORED'),
                    default=['xfer_repro_g384_e1087.json', 'se_e1087.json'],
                    help='재현 대조 쌍 (없으면 건너뜀)')
    ap.add_argument('--rate', nargs=2, metavar=('SLOW', 'BASE'),
                    default=['xfer_rate_g192_e1170.json', 'xfer_kit_real14_g192_e1170.json'],
                    help='재하율 대조 쌍 (같은 베드·같은 ε, 마하만 다름)')
    ap.add_argument('--allow-rate-mismatch', action='store_true',
                    help='재하율 불일치에도 전이 판정을 강행 (결과는 교란됨 — 진단 전용)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not (a.ref_kit and a.test_kit):
        ap.error('--ref-kit 과 --test-kit 이 필요합니다 (또는 --selftest)')

    R = a.dir
    # ── ① 재현 ──────────────────────────────────────────────────────────────
    new_p, old_p = (os.path.join(R, f) for f in a.repro)
    if os.path.exists(new_p) and os.path.exists(old_p):
        n, o = json.load(open(new_p)), json.load(open(old_p))
        print('══ ① 재현 — 현재 코드가 기준곡선을 재현하는가 ══')
        worst = 0.0
        for k in ('thickness_um', 'final_stress_GPa'):
            x, y = o.get(k), n.get(k)
            if isinstance(x, (int, float)) and x:
                p = 100.0 * (y - x) / x
                worst = max(worst, abs(p))
                print(f'   {k:18s} 저장 {x:.4f}  재현 {y:.4f}   Δ {p:+.2f} %')
        print(f'   → 최대 |Δ| {worst:.2f} %  ⇒ '
              + ('**통과** (코드 동일)' if worst < 1.0 else '**★ 불일치 — 곡선 정본 재측정 필요**'))
    else:
        print('══ ① 재현 — 대조 파일 없음 (건너뜀)')

    # ── ② 해상도 (같은 베드, 192 vs 곡선 384) ────────────────────────────────
    ref_pts, (v_am, v_se, area) = load_points(a.ref_glob, a.ref_kit, R)
    print(f'\n══ ② 해상도 — 기준베드 @192 vs REAL14_SE_CURVE @384 ══')
    if not ref_pts:
        print(f'   {a.ref_glob} 매치 없음 — 건너뜀')
    else:
        from am_load_balance_jam import REAL14_SE_CURVE as C
        c_pts = [(float(p), float(s), None, '384curve') for p, s in C]
        rows = compare(c_pts, ref_pts, ref_label='384', test_label='192')
        print(f'   기준베드: V_AM {v_am:,.0f} · V_SE {v_se:,.0f} µm³ · A {area:,.0f} µm²')
        print_table(rows, '384', '192')
        # 곡선이 가파른 구간은 σ 상대차가 부풀려지므로 φ-등가 편차도 같이 낸다
        cp, cs = np.array([p for p, _ in C]), np.array([s for _, s in C])
        dphi = [float(np.interp(r['s_test'], cs, cp)) - r['phi'] for r in rows]
        print('   φ-등가 편차: ' + ' '.join(f'{d:+.4f}' for d in dphi)
              + f'   (|max| {max(abs(d) for d in dphi):.4f})')
        verdict(rows, 'resolution')

    # ── ③ 재하율 (같은 베드·같은 ε, 마하만 다름) ─────────────────────────────
    slow_p, base_p = (os.path.join(R, f) for f in a.rate)
    print('\n══ ③ 재하율 — 관성이 σ 에 얼마나 섞였나 (같은 베드·같은 ε) ══')
    if os.path.exists(slow_p) and os.path.exists(base_p):
        s_, b_ = json.load(open(slow_p)), json.load(open(base_p))
        for k in ('thickness_um', 'final_stress_GPa'):
            x, y = b_.get(k), s_.get(k)
            if isinstance(x, (int, float)) and x:
                print(f'   {k:18s} 기본 {x:.4f} (V/c_P {b_.get("platen_mach_V_over_cP")}) '
                      f' 준정적 {y:.4f} (V/c_P {s_.get("platen_mach_V_over_cP")})   '
                      f'Δ {100 * (y - x) / x:+.1f} %')
        ds = abs(100 * (s_['final_stress_GPa'] - b_['final_stress_GPa']) / b_['final_stress_GPa'])
        print(f'   → σ 변화 {ds:.1f} %  ⇒ '
              + ('**관성 무시 가능** — 곡선 절대값을 실험과 대조 가능' if ds <= 5 else
                 '**곡선은 상대비교 전용** — 실험 대조 시 준정적 재측정 필요' if ds >= 15 else
                 '중간 — 절대값에 이 폭을 밴드로 얹을 것'))
    else:
        print('   대조 파일 없음 (건너뜀)')

    # ── ④ 베드-전이 (★ 재하율 게이트) ────────────────────────────────────────
    test_pts, (tv_am, tv_se, t_area) = load_points(a.test_glob, a.test_kit, R)
    print('\n══ ④ 베드-전이 — 곡선을 다른 베드에 쓸 수 있는가 ══')
    if not (ref_pts and test_pts):
        print('   점이 부족해 건너뜀')
        return 0
    r_rate, r_warn = _rate_of(ref_pts, 'ref')
    t_rate, t_warn = _rate_of(test_pts, 'test')
    for w in (r_warn, t_warn):
        if w:
            print(f'   ⚠ {w}')
    print(f'   재하율  기준 V/c_P {r_rate}   대상 V/c_P {t_rate}')
    if r_rate and t_rate:
        ratio = max(r_rate, t_rate) / max(min(r_rate, t_rate), 1e-12)
        if ratio > RATE_TOL_RATIO and not a.allow_rate_mismatch:
            print(f'   ★★ 비교 거부 — 재하율이 {ratio:.2f}배 다르다 (허용 {RATE_TOL_RATIO}).')
            print('       이 상태의 σ 차이는 베드 기전과 관성이 분리되지 않는다.')
            print('       --platen-mach 로 두 베드의 마하수를 맞춰 다시 재거나,')
            print('       진단 목적이면 --allow-rate-mismatch 로 강행할 것.')
            return 2
        if ratio > RATE_TOL_RATIO:
            print(f'   ⚠ 재하율 {ratio:.2f}배 불일치를 강행 중 — 결과는 교란되어 있다.')
    print(f'   대상베드: V_AM {tv_am:,.0f} · V_SE {tv_se:,.0f} µm³ · A {t_area:,.0f} µm²')
    rows = compare(ref_pts, test_pts, ref_label='ref', test_label='test')
    print_table(rows, 'ref', 'test')
    v = verdict(rows, 'transfer')
    if v and rows:
        low = [r for r in rows if np.isfinite(r['pct']) and r['s_ref'] >= 0.01][:2]
        if low:
            print('   ※ 판정 무게는 낮은 φ 쪽에 — 높은 φ 는 σ_y 포화라 두 베드가 자동으로 붙는다:'
                  + ' ' + ', '.join(f"φ {r['phi']:.3f} {r['pct']:+.0f}%" for r in low))
    return 0


def _selftest():
    ok_n = [0, 0]

    def ok(name, cond):
        ok_n[1] += 1
        ok_n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    ok('1) φ 정의: V_SE/(A·h − V_AM)',
       abs(phi_se_local(30.0, 1000.0, 500.0, 100.0) - 500.0 / (100 * 30 - 1000)) < 1e-12)
    ok('2) φ 자유공간 ≤ 0 → nan', not np.isfinite(phi_se_local(1.0, 1000.0, 500.0, 100.0)))
    # 베드를 통째로 k배 하면 φ 는 정확히 불변 (전이 가정의 수학적 뼈대)
    k = 2.0
    ok('3) 상사 스케일에 φ 불변',
       abs(phi_se_local(30.0, 1000.0, 500.0, 100.0)
           - phi_se_local(30.0 * k, 1000.0 * k ** 3, 500.0 * k ** 3, 100.0 * k ** 2)) < 1e-12)
    ref = [(0.60, 0.10, 0.031, 'a'), (0.70, 0.20, 0.031, 'b'), (0.80, 0.30, 0.031, 'c')]
    same = [(0.65, 0.15, 0.030, 'x')]                      # ref 보간과 정확히 일치
    rows = compare(ref, same)
    ok('4) 보간 일치 → Δ 0 %', abs(rows[0]['pct']) < 1e-9)
    ok('5) 외삽 표시', compare(ref, [(0.90, 0.4, 0.03, 'y')])[0]['extrap'] is True)
    hi = [(0.65, 0.45, 0.030, 'x')]                        # 3배
    ok('6) 3배 차 → 기각 판정', '기각' in (verdict(compare(ref, hi), 't') or {}).get('verdict', ''))
    ok('7) σ_ref<0.01 점은 판정에서 제외 (jamming 전 구간에서 상대차가 발산)',
       verdict(compare([(0.6, 0.001, 0, 'a'), (0.8, 0.30, 0, 'c')],
                       [(0.60, 0.5, 0, 'x')]), 't') is None)
    r, w = _rate_of([(0.6, 0.1, 0.031, 'a'), (0.7, 0.2, 0.031, 'b')], 'ref')
    ok('8) 재하율 대푯값 + 일관성 검사', abs(r - 0.031) < 1e-9 and w is None)
    r2, w2 = _rate_of([(0.6, 0.1, 0.031, 'a'), (0.7, 0.2, 0.105, 'b')], 'ref')
    ok('9) 런마다 재하율 다르면 경고', w2 is not None and '다름' in w2)
    ok('10) 게이트 문턱: 0.031 vs 0.105 는 거부 · 0.030 vs 0.031 은 통과',
       (0.105 / 0.031) > RATE_TOL_RATIO and (0.031 / 0.030) <= RATE_TOL_RATIO)
    print(f'\nselftest: {ok_n[0]}/{ok_n[1]} PASS')
    return 0 if ok_n[0] == ok_n[1] else 1


if __name__ == '__main__':
    sys.exit(main())
