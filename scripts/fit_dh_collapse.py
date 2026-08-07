#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""d_h 색인 적합 — "다섯 침대의 σ(φ) 를 채널폭 하나로 접을 수 있는가".

═══ 무엇을 재는가 ════════════════════════════════════════════════════════════════
`docs/se_curve_transfer_verdict_20260806.md` 가 확정한 것:
  ① 같은 φ 에서 σ 가 P:S 조성 순서대로 **완벽 단조** (φ0.72 서 1.87배) — 계통이지 잡음이 아님
  ② 그 조성 의존이 **d_h = V_free/S_AM (자유공간의 수력반경)** 하나로 접힌다
     — n_grid 192·φ0.72 서 log σ vs log d_h **기울기 −0.541 · R² 0.935**
쓸모는 지수 절대값이 아니라 **접힌다는 것 자체**다: 새 전극마다 5점을 재는 대신
스캐폴드 CSV 에서 d_h 를 계산해 곡선을 옮기면 된다.

이 스크립트는 그 적합을 **아무 n_grid 에서나** 재현한다 (288 검증이 첫 고객).

═══ ★ 왜 φ 보정이 필요한가 ══════════════════════════════════════════════════════
`--compact-to` 는 **ε** 을 맞추지 φ 를 맞추지 않는다.  같은 ε 이라도 n_grid 가 다르면
두께가 미세하게 달라 φ 가 어긋나 착지한다 (실측: 128 에서 두 점이 φ 0.7577 / 0.7429).
σ(φ) 는 이 구간에서 가파르므로, **착지 φ 가 흩어진 채로 적합하면 조성 신호에 φ 신호가
섞인다**.  → 착지 φ 를 읽어 흩어졌으면 **같은 킷의 다른 해상도 곡선에서 잰 국소기울기**
dlnσ/dφ 로 공통 φ 에 맞춘 뒤 적합한다 (128 비교에 쓴 것과 같은 방법).

═══ ⚠ 지수를 물리상수로 인용하지 말 것 ═════════════════════════════════════════
같은 문서 ④: 128→192→288 겉보기 수렴차수 ≈ 0.10 = **사실상 수렴하지 않음**.
|기울기| 는 격자를 조일수록 계속 커진다 (0.541@192 → 0.663@288, 양 끝 2점 기준).
미해상 협착이 격자에서 사라져 재료를 통과시키기 때문이며, 501 nm 채널을 8~10셀로
풀려면 n_grid ≈ 900 이 필요해 이 방법으로는 도달 불가.  ⇒ **기울기는 항상 하한으로,
쓰는 해상도를 명시해서** 보고한다.  R² (=접히는가) 만이 해상도에 걸쳐 뜻이 있다.

═══ ★ 재하율 선택이 φ 선택보다 먼저다 (--mach) ══════════════════════════════════
한 킷에 **옛 기하-규칙 런**(vmax=0.008·높이 → 두꺼운 kit_ps 침대에서 V/c_P ≈ 0.105)과
**--platen-mach 런**(0.03)이 같은 φ 에 겹쳐 있을 수 있다.  φ 로만 고르면 킷마다 다른
재하율이 뽑혀 조성 신호에 관성이 섞인다 — 2026-08-07 에 192 corpus 에서 실제로
**3.49 배 섞임**이 나왔고 재하율 게이트가 적합을 거부했다.
→ 섞인 해상도에서는 **`--mach 0.03`** 으로 쓸 런을 먼저 고른다.  무엇이 있는지는
  `--list` 로 본다 (적합 없이 킷별 후보점 φ·σ·V/c_P·파일명을 나열).

사용:
  python3 scripts/fit_dh_collapse.py --dir ~/Yonghoon-DEM-DFT/se_curve \\
      --kit-root ~/Yonghoon-DEM-DFT --n-grid 288 --phi 0.72 --slope-grid 192
  python3 scripts/fit_dh_collapse.py --n-grid 192 --mach 0.03 --list     # 섞임 진단
  python3 scripts/fit_dh_collapse.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def _reexec_in_venv():
    """numpy 가 없으면 venv 의 python 으로 **자기 자신을 재실행**한다.

    ★ 왜: run_se_curve_batch.sh 는 venv 를 자동 탐색하는데 이 스크립트를 손으로 부를 땐
      안 그래서, 배치가 6.6 시간 돌아 끝난 직후 `ModuleNotFoundError: numpy` 로 판정이
      한 사이클 밀렸다 (2026-08-07 실제 발생).  분석 도구는 런 직후에 부르는 물건이라
      그 순간의 마찰이 제일 비싸다.
    _DEM_VENV_REEXEC 로 한 번만 시도한다 (venv 에도 numpy 가 없으면 무한루프 방지).
    """
    if os.environ.get('_DEM_VENV_REEXEC'):
        return
    here = os.path.dirname(_HERE)
    cands = [os.path.join(here, 'venv', 'bin', 'python3'),
             os.path.expanduser('~/Yonghoon-DEM-DFT/venv/bin/python3'),
             os.path.expanduser('~/.venv/bin/python3')]
    for py in cands:
        if os.path.exists(py) and os.path.realpath(py) != os.path.realpath(sys.executable):
            os.environ['_DEM_VENV_REEXEC'] = '1'
            sys.stderr.write(f'· numpy 없음 → venv 로 재실행: {py}\n')
            try:
                os.execv(py, [py] + sys.argv)
            except OSError:
                del os.environ['_DEM_VENV_REEXEC']


try:
    import numpy as np
except ModuleNotFoundError:
    _reexec_in_venv()
    sys.exit('★ numpy 를 못 찾았습니다 — venv 를 활성화하고 다시 실행하세요:\n'
             '    . venv/bin/activate   (또는 . ~/Yonghoon-DEM-DFT/venv/bin/activate)')

#: 다섯 대조군 — 두께 ±1.4 % · SE/solid ±0.5 %p 로 맞춘 채 P:S 만 다르다.
KITS_DEFAULT = ('kit_ps_0_10', 'kit_ps_3_7', 'kit_ps_5_5', 'kit_ps_7_3', 'kit_ps_10_0')

#: 착지 φ 가 이보다 더 흩어지면 보정 없이는 적합하지 않는다 (σ(φ) 가 가파른 구간이라).
PHI_TOL = 0.005

#: 재하율은 러너가 --platen-mach 로 고정하지만, 옛 산출물이 섞이면 조용히 틀린다.
RATE_TOL_RATIO = 1.15


def _read_scaffold(path):
    from plan_se_curve_targets import read_scaffold
    return read_scaffold(path)


def bed_geometry(kit_dir):
    """(V_AM, V_SE, A, S_AM) [µm³, µm², µm²] — planner 와 같은 스캐폴드 규약.

    S_AM = Σ 4πr² (AM 젖은 표면).  구가 겹쳐도 보정하지 않는다 — 다섯 킷이 같은
    관례를 쓰므로 **상대 비교에는 공통모드로 상쇄**되고, d_h 의 절대값만 그만큼
    과소평가된다 (겹침이 표면을 가리므로 실제 S_AM 은 이보다 작다 → 실제 d_h 는 더 큼).
    """
    from plan_se_curve_targets import bed_volumes
    v_am, v_se, area, _lat = bed_volumes(kit_dir)
    _c, r = _read_scaffold(os.path.join(kit_dir, 'am_scaffold.csv'))
    return float(v_am), float(v_se), float(area), float(np.sum(4.0 * np.pi * r ** 2))


def d_h_at_phi(v_se, s_am, phi, include_se=True):
    """자유공간의 수력반경 [µm]  d_h = V_free / S_AM.

    φ = V_SE/(A·h − V_AM) 이므로 **고정 φ 에서 A·h − V_AM = V_SE/φ** 는 킷 상수다.
      include_se=True : V_free = A·h − V_AM        = V_SE/φ          (AM 사이 공간 전체)
      include_se=False: V_free = A·h − V_AM − V_SE = V_SE·(1/φ − 1)  (잔여 공극만)
    ★ 고정 φ 에서 둘은 상수배 (1−φ) 차이라 **기울기와 R² 는 완전히 동일**하고
      d_h 의 절대값만 달라진다 (selftest 5).  기본은 AM 배치의 기하량인 전자.
    """
    if not (phi > 0 and s_am > 0):
        return float('nan')
    free = v_se / phi
    if not include_se:
        free -= v_se
    return free / s_am


def load_kit_points(root, kit, n_grid):
    """xfer_*<kit>_g<n>_e*.json → [(φ, σ, mach, path)] (φ 오름차순)."""
    from analyze_se_curve_transfer import phi_se_local
    kit_dir = _kit_dir_cache[kit]
    v_am, v_se, area, _s = bed_geometry(kit_dir)
    out = []
    for p in sorted(glob.glob(os.path.join(root, f'xfer_*{kit}_g{n_grid}_e*.json'))):
        d = json.load(open(p))
        h, s = d.get('thickness_um'), d.get('final_stress_GPa')
        if h is None or s is None:
            continue
        out.append((phi_se_local(h, v_am, v_se, area), float(s),
                    d.get('platen_mach_V_over_cP'), os.path.basename(p)))
    return sorted(out, key=lambda r: r[0])


_kit_dir_cache: dict = {}


def local_dlnsigma_dphi(points, phi0):
    """φ0 를 감싸는 두 점의 (ln σ) 기울기.  점이 부족하거나 σ≤0 이면 None.

    ★ 국소기울기는 **같은 킷·다른 해상도**(보통 192, φ 3점)에서 잰다 — 보정하려는
      해상도 자체에는 φ 격자가 1점뿐이라 기울기를 못 낸다.  해상도가 바뀌면 σ 절대값은
      변하지만 곡선 **모양**은 유지된다는 가정이고, 보정량이 작을 때만 쓴다.
    """
    p = [(a, b) for a, b, *_ in points if b > 0 and np.isfinite(a)]
    if len(p) < 2:
        return None
    xs = np.array([a for a, _ in p]); ys = np.log(np.array([b for _, b in p]))
    j = int(np.clip(np.searchsorted(xs, phi0), 1, len(xs) - 1))
    dx = xs[j] - xs[j - 1]
    return float((ys[j] - ys[j - 1]) / dx) if abs(dx) > 1e-9 else None


def _rate_ok(mach, target, tol=None):
    """두 재하율이 '같다'고 볼 수 있는가 (RATE_TOL_RATIO 비율 안)."""
    tol = RATE_TOL_RATIO if tol is None else tol
    if mach is None or target is None or mach <= 0 or target <= 0:
        return False
    return max(mach, target) / min(mach, target) <= tol


def loglog_fit(d_h, sigma):
    """log σ = a + b·log d_h → (b, a, R², resid_sd, LOO_maxΔb).

    n=5 에 2 파라미터라 R² 하나로는 약하다 → **한 점씩 빼 기울기가 얼마나 흔들리는지**
    (LOO) 를 같이 낸다.  한 점이 결론을 만드는지 바로 보인다.
    """
    x, y = np.log(np.asarray(d_h, float)), np.log(np.asarray(sigma, float))
    b, a = np.polyfit(x, y, 1)
    pred = a + b * x
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    sd = float(np.sqrt(ss_res / max(len(x) - 2, 1)))
    loo = 0.0
    for i in range(len(x)):
        m = np.arange(len(x)) != i
        loo = max(loo, abs(float(np.polyfit(x[m], y[m], 1)[0]) - b))
    return float(b), float(a), r2, sd, loo


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dir', default='.', help='xfer_*.json 이 있는 디렉토리 (se_curve)')
    ap.add_argument('--kit-root', default='.', help='킷 디렉토리들의 부모')
    ap.add_argument('--kits', default=','.join(KITS_DEFAULT))
    ap.add_argument('--n-grid', type=int, default=288)
    ap.add_argument('--phi', type=float, default=0.72, help='적합할 공통 φ')
    ap.add_argument('--slope-grid', type=int, default=192,
                    help='φ 보정용 국소기울기를 잴 해상도 (φ 3점이 있는 쪽)')
    ap.add_argument('--void-free', action='store_true',
                    help='V_free 에서 SE 를 빼 잔여공극으로 (기울기·R² 는 불변)')
    ap.add_argument('--mach', type=float, default=None,
                    help='이 V/c_P 인 런만 쓴다 (한 킷에 옛 기하-규칙 런과 --platen-mach 런이 '
                         '섞여 있을 때 필수 — φ 만 보고 고르면 재하율이 섞인다)')
    ap.add_argument('--list', dest='list_points', action='store_true',
                    help='적합 없이 킷별 후보점(φ·σ·V/c_P·파일)만 나열 — 섞임 진단용')
    ap.add_argument('--allow-rate-mismatch', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()

    kits = [k.strip() for k in a.kits.split(',') if k.strip()]
    for k in kits:
        d = os.path.join(a.kit_root, k)
        _kit_dir_cache[k] = d if os.path.isdir(d) else os.path.join(a.dir, k)

    # ── 진단 나열 (--list) ────────────────────────────────────────────────────
    if a.list_points:
        print(f'══ 후보점 나열 — n_grid {a.n_grid}'
              + (f' · --mach {a.mach} 통과 여부 표시' if a.mach else '') + ' ══')
        for k in kits:
            pts = load_kit_points(a.dir, k, a.n_grid)
            print(f'  {k}  ({len(pts)}점)')
            for phi, sig, mach, f in pts:
                mk = ''
                if a.mach is not None:
                    mk = ('  ✓' if (mach is not None and _rate_ok(mach, a.mach)) else '  ✗ 재하율')
                print(f'     φ {phi:.4f}  σ {sig:8.4f}  V/c_P '
                      + (f'{mach:.4f}' if mach is not None else '  없음') + f'  {f}{mk}')
        return 0

    print(f'══ d_h 색인 적합 — n_grid {a.n_grid} · 공통 φ {a.phi} ══')
    rows, missing, dropped = [], [], 0
    for k in kits:
        pts = load_kit_points(a.dir, k, a.n_grid)
        # ★ 재하율 선택은 φ 선택보다 먼저 — 한 킷에 옛 기하-규칙 런(두꺼운 침대서 V/c_P
        #   ≈0.105)과 --platen-mach 런(0.03)이 같이 있으면, φ 로만 고르면 킷마다 다른
        #   재하율이 뽑혀 조성 신호에 관성이 섞인다 (2026-08-07 192 에서 실제 발생: 3.49배).
        if a.mach is not None:
            keep = [p for p in pts if p[2] is not None and _rate_ok(p[2], a.mach)]
            dropped += len(pts) - len(keep)
            pts = keep
        if not pts:
            missing.append(k)
            continue
        i = int(np.argmin([abs(p - a.phi) for p, *_ in pts]))
        phi, sig, mach, f = pts[i]
        _v_am, v_se, _A, s_am = bed_geometry(_kit_dir_cache[k])
        rows.append({'kit': k, 'phi': phi, 'sigma_raw': sig, 'mach': mach, 'file': f,
                     'd_h_um': d_h_at_phi(v_se, s_am, a.phi, include_se=not a.void_free),
                     'S_AM': s_am, 'V_SE': v_se})
    if dropped:
        print(f'   --mach {a.mach}: 재하율이 다른 {dropped}점 제외 (옛 기하-규칙 런)')
    if missing:
        print('   ⚠ 쓸 점 없음: ' + ', '.join(missing)
              + (f'  ← --mach {a.mach} 인 런이 이 킷엔 없다' if a.mach is not None else ''))
    if len(rows) < 3:
        print('   ★ 점이 3개 미만 — 적합 불가')
        return 1

    # ── 재하율 게이트 (러너가 고정하지만 옛 산출물이 섞일 수 있다) ──────────────
    ms = [r['mach'] for r in rows if r['mach'] is not None]
    if len(ms) >= 2:
        ratio = max(ms) / max(min(ms), 1e-12)
        print(f'   재하율 V/c_P {min(ms):.4f}..{max(ms):.4f} ({ratio:.2f}배)')
        if ratio > RATE_TOL_RATIO and not a.allow_rate_mismatch:
            print(f'   ★★ 적합 거부 — 재하율이 {ratio:.2f}배 다르다 (허용 {RATE_TOL_RATIO}).')
            print('       조성 신호와 관성이 분리되지 않는다.  --allow-rate-mismatch 로만 강행.')
            return 2
    if len(ms) < len(rows):
        print(f'   ⚠ {len(rows) - len(ms)}개 json 에 platen_mach 없음 (구 산출물)')

    # ── φ 보정 ────────────────────────────────────────────────────────────────
    phis = [r['phi'] for r in rows]
    spread = max(phis) - min(phis)
    print(f'   착지 φ {min(phis):.4f}..{max(phis):.4f}  (폭 {spread:.4f}, 문턱 {PHI_TOL})')
    corrected = False
    if spread > PHI_TOL:
        print(f'   → 흩어짐 — g{a.slope_grid} 국소기울기로 φ {a.phi} 에 맞춘다')
        for r in rows:
            sl = local_dlnsigma_dphi(load_kit_points(a.dir, r['kit'], a.slope_grid), a.phi)
            r['slope'] = sl
            if sl is None:
                r['sigma'] = r['sigma_raw']
                print(f"      ⚠ {r['kit']}: g{a.slope_grid} 점 부족 — 보정 못 함 (생값 사용)")
            else:
                r['sigma'] = r['sigma_raw'] * float(np.exp(sl * (a.phi - r['phi'])))
                corrected = True
    else:
        print('   → 문턱 안 — 보정 없이 생값으로 적합')
        for r in rows:
            r['slope'], r['sigma'] = None, r['sigma_raw']

    hdr = f'   {"kit":>14}{"착지φ":>9}{"σ_raw":>10}{"σ_corr":>10}{"d_h(nm)":>10}{"dlnσ/dφ":>10}'
    print(hdr)
    for r in sorted(rows, key=lambda z: z['d_h_um']):
        sl = '     —   ' if r['slope'] is None else f"{r['slope']:9.2f}"
        print(f"   {r['kit']:>14}{r['phi']:9.4f}{r['sigma_raw']:10.4f}"
              f"{r['sigma']:10.4f}{r['d_h_um'] * 1000:10.1f}{sl}")

    # ── 적합 ──────────────────────────────────────────────────────────────────
    good = [r for r in rows if r['sigma'] > 0 and np.isfinite(r['d_h_um'])]
    if len(good) < 3:
        print('   ★ σ>0 인 점이 3개 미만 — 적합 불가')
        return 1
    b, _a0, r2, sd, loo = loglog_fit([r['d_h_um'] for r in good], [r['sigma'] for r in good])
    print(f'\n   log σ vs log d_h   기울기 {b:+.3f} · R² {r2:.3f} · 잔차sd {sd:.3f} (n={len(good)})')
    print(f'   LOO: 한 점을 빼면 기울기가 최대 {loo:.3f} 움직임 '
          f'({"한 점이 결론을 만들지 않음" if loo < 0.15 * abs(b) else "★ 한 점 의존 — 결론 약함"})')
    print(f'   ⇒ 접힘 {"성립" if r2 >= 0.85 else "약함" if r2 >= 0.6 else "★ 깨짐"}'
          + ('' if corrected else '  (φ 보정 없음)'))
    print(f'   ⚠ |기울기| {abs(b):.3f} 은 n_grid {a.n_grid} 에서의 **하한** — 수렴 안 함'
          '(차수 ≈0.10).  물리상수로 인용 금지; R² 만 해상도에 걸쳐 뜻이 있다.')
    return 0


def _selftest():
    n = [0, 0]

    def ok(name, cond):
        n[1] += 1
        n[0] += bool(cond)
        print(f'  {"PASS" if cond else "FAIL"}  {name}')

    # 1-2) d_h 정의
    ok('1) d_h = (V_SE/φ)/S_AM', abs(d_h_at_phi(720.0, 100.0, 0.72) - 10.0) < 1e-12)
    ok('2) φ↑ → 자유공간↓ → d_h↓', d_h_at_phi(720.0, 100.0, 0.86) < d_h_at_phi(720.0, 100.0, 0.72))
    ok('3) S_AM↑ (작은 AM 많음) → d_h↓ = 좁은 채널',
       d_h_at_phi(720.0, 200.0, 0.72) < d_h_at_phi(720.0, 100.0, 0.72))
    ok('4) φ≤0 또는 S_AM≤0 → nan',
       not np.isfinite(d_h_at_phi(720.0, 0.0, 0.72)) and not np.isfinite(d_h_at_phi(720.0, 1.0, 0.0)))
    # 5) include_se 는 고정 φ 에서 상수배 → 기울기·R² 불변 (문서화한 성질)
    sam = [100.0, 140.0, 200.0, 260.0, 320.0]
    dh_a = [d_h_at_phi(720.0, s, 0.72, True) for s in sam]
    dh_b = [d_h_at_phi(720.0, s, 0.72, False) for s in sam]
    sig = [1.0 / d ** 0.5 for d in dh_a]
    fa, fb = loglog_fit(dh_a, sig), loglog_fit(dh_b, sig)
    ok('5) include_se 여부가 기울기·R² 를 바꾸지 않는다 (상수배)',
       abs(fa[0] - fb[0]) < 1e-9 and abs(fa[2] - fb[2]) < 1e-9 and abs(dh_a[0] / dh_b[0] - 1 / (1 - 0.72)) < 1e-9)
    # 6-7) 적합기
    ok('6) 완전 멱함수 → 기울기 −0.5 · R² 1', abs(fa[0] + 0.5) < 1e-9 and abs(fa[2] - 1.0) < 1e-9)
    ok('7) 잡음 없는 멱함수는 LOO 흔들림 0', fa[4] < 1e-9)
    noisy = [s * (1.0 + 0.30 * (i == 2)) for i, s in enumerate(sig)]
    fn = loglog_fit(dh_a, noisy)
    ok('8) 한 점을 30 % 튀기면 R² 하락 + LOO 감지', fn[2] < 0.99 and fn[4] > 1e-3)
    # 9-10) φ 보정
    pts = [(0.66, 0.30, 0.03, 'a'), (0.72, 0.50, 0.03, 'b'), (0.81, 0.70, 0.03, 'c')]
    sl = local_dlnsigma_dphi(pts, 0.72)
    ok('9) 국소기울기 = 감싸는 두 점의 dlnσ/dφ',
       sl is not None and abs(sl - (np.log(0.50) - np.log(0.30)) / 0.06) < 1e-9)
    ok('10) 점 1개 / σ≤0 이면 기울기 None',
       local_dlnsigma_dphi([(0.72, 0.5, 0.03, 'b')], 0.72) is None
       and local_dlnsigma_dphi([(0.66, 0.0, 0.03, 'a'), (0.72, -1.0, 0.03, 'b')], 0.72) is None)
    # 11) 보정이 착지 어긋남을 되돌리는가 (합성: 참 σ(φ)=exp(k·φ) 에서 φ 가 밀려 착지)
    k, phi_t, phi_l = 5.0, 0.72, 0.7429
    ok('11) φ 보정이 착지 어긋남을 되돌린다',
       abs(np.exp(k * phi_l) * np.exp(k * (phi_t - phi_l)) - np.exp(k * phi_t)) < 1e-9)
    ok('12) PHI_TOL 은 실측 착지 어긋남(0.7577 vs 0.7429 = 0.0148)을 잡는다',
       (0.7577 - 0.7429) > PHI_TOL)
    # 13-15) 재하율 선택 (--mach) — 192 에서 실제로 3.49배 섞여 있었다
    ok('13) _rate_ok: 0.030 vs 0.0300 통과 · 0.030 vs 0.1048 거부',
       _rate_ok(0.0300, 0.03) and not _rate_ok(0.1048, 0.03))
    ok('14) _rate_ok: mach 없음/0 이하는 통과시키지 않는다',
       not _rate_ok(None, 0.03) and not _rate_ok(0.0, 0.03) and not _rate_ok(0.03, None))
    # 한 킷에 옛 기하-규칙 런과 0.03 런이 같은 φ 에 겹쳐 있을 때 올바른 쪽을 고르는가
    mixed = [(0.7200, 9.99, 0.1048, 'old'), (0.7201, 0.50, 0.0300, 'new')]
    picked_phi_only = mixed[int(np.argmin([abs(p - 0.72) for p, *_ in mixed]))][3]
    kept = [p for p in mixed if _rate_ok(p[2], 0.03)]
    ok('15) φ 로만 고르면 옛 런을 집지만 --mach 로 거르면 0.03 런이 남는다',
       picked_phi_only == 'old' and len(kept) == 1 and kept[0][3] == 'new')
    print(f'\nselftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    sys.exit(main())
