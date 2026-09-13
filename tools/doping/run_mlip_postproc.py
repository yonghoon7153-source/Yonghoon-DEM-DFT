#!/usr/bin/env python
"""run_mlip_postproc.py — full MLIP post-processing per structure.

For each input xyz, runs in order:
  1. Light anneal (300 K, 20 ps, optional). NOTE: 300K @ 20ps is mostly
     finite-T noise injection rather than true Li-sublattice annealing
     (Arrhenius rate × 20ps ≈ 0.01 hop/Li at 300K). Use temperature=500
     and time_ps=50 for actual Pipeline-Step-3 anneal (kT=0.043 eV
     vs Li hop Eₐ=0.2 eV barrier).
  2. EOS volume sweep (94-106% in 7 steps: 0.94/0.96/0.98/1.00/1.02/
     1.04/1.06), Birch-Murnaghan 3rd-order fit
     → V0, B0, B0', R² (returns None for B0/V0 if r²<0.95 — A-3 fix)
  3. Elastic constants via finite strain (6 Voigt strains, ε = ±0.005),
     Voigt-Reuss-Hill average → B, G, E (Young), ν (Poisson), G/B (Pugh).
     Sign convention: ASE atoms.get_stress() returns positive stress
     for compression (= negative of dE/dV/V), so dσ/dε > 0 → C_ii > 0.

All UMA, no extra DFT. Output: per-structure JSON + global summary.

Usage:
  python3 tools/doping/run_mlip_postproc.py \\
      --winners runs/.../winners.json \\
      --out runs/.../mlip_postproc/ \\
      --device cuda

  # Skip steps (per-step toggle)
  python3 ... --no_anneal --no_elastic   # only EOS

  # Specific xyz instead of winners JSON
  python3 ... --xyz path/a.xyz path/b.xyz --out ...
"""
import argparse
import json
import sys
import time
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import FIRE
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase import units

try:
    from ase.filters import FrechetCellFilter as CellFilter
except ImportError:
    try:
        from ase.constraints import ExpCellFilter as CellFilter
    except ImportError:
        from ase.constraints import UnitCellFilter as CellFilter

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def uma_inference_provenance(mode=None):
    """UMA 추론 설정을 **실제 환경에서 읽어** 기록한다 (회신 BQ-2 Q6).

    ⛔⛔ 리뷰어 지적 — 종전 로더는 `get_predict_unit(...)` 에 모드를 **생략**하고
      라이브러리 기본값에 의존했다. 그러면 기록에 남는 것은 "default" 라는
      **이름뿐**이고 실제로 무엇이 쓰였는지 알 수 없다. 이름이 아니라
      **버전·체크포인트·추론 설정**을 남겨야 한다.

    ⚠ **정정 (2026-09-13)**: 내가 *"turbo 는 bf16/TF32 가 필요하다"* 고 쓴 것은
      부정확하다. 공식 문서상 **turbo 의 핵심 차이는 TF32** 다.

    ⛔ 이 함수가 **못 하는 것**
      · 없는 것을 지어내지 않는다. 못 읽은 항목은 `null` 로 남긴다.
      · 모드를 바꾸지 않는다. 무엇이 걸려 있는지 **읽기만** 한다.
      · 이 기록만으로 두 기계의 수치를 섞어도 된다고 말하지 않는다 —
        회신 BQ-2 Q6 은 파일럿 **내부를 같은 설정으로 완결**하라는 조건이다.
    """
    info = {'requested_mode': mode,
            '⚠_turbo_의_뜻': ('공식 문서상 turbo 의 핵심 차이는 **TF32** 다. '
                              '"turbo = bf16" 은 부정확한 설명이다 (회신 BQ-2 Q6 정정)'),
            'model_name': 'uma-s-1p1'}
    try:
        import torch
        info['torch_version'] = str(torch.__version__)
        info['cuda_available'] = bool(torch.cuda.is_available())
        info['torch_arch_list'] = list(getattr(torch.cuda, 'get_arch_list', lambda: [])())
        # ⚠ is_available() 이 True 라도 이 GPU 의 커널이 없을 수 있다 (2026-09-13 V100/sm_70)
        info['tf32_matmul'] = bool(getattr(torch.backends.cuda.matmul, 'allow_tf32', False))
        info['tf32_cudnn'] = bool(getattr(torch.backends.cudnn, 'allow_tf32', False))
        info['default_dtype'] = str(torch.get_default_dtype())
        if torch.cuda.is_available():
            info['gpu_name'] = torch.cuda.get_device_name(0)
            info['gpu_capability'] = list(torch.cuda.get_device_capability(0))
    except Exception as e:                                   # noqa: BLE001
        info['torch_error'] = f'{type(e).__name__}: {e}'
    try:
        import fairchem.core as _fc
        info['fairchem_version'] = str(getattr(_fc, '__version__', None))
    except Exception as e:                                   # noqa: BLE001
        info['fairchem_error'] = f'{type(e).__name__}: {e}'
    _miss = [k for k in ('torch_version', 'fairchem_version', 'tf32_matmul')
             if info.get(k) is None]
    if _miss or 'torch_error' in info or 'fairchem_error' in info:
        info['⛔_불완전'] = ('일부 항목을 읽지 못했다 — **읽은 것만** 기록한다. '
                            '못 읽은 값을 기본값으로 채우지 않는다')
    return info


def load_uma(device='cuda', task='omat', mode=None):
    """UMA 계산기. `mode` 를 주면 **선언적으로** 넘긴다 (회신 BQ-2 Q6).

    ⛔ mode 를 생략하면 종전과 같이 라이브러리 기본값을 쓴다 — 과거 명령의
      재현성을 깨지 않기 위해서다. 다만 무엇이 쓰였는지는
      `uma_inference_provenance()` 가 **실제 환경에서 읽어** 기록한다.
    """
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    kw = {'device': device}
    if mode is not None:
        kw['inference_settings'] = mode
    predictor = pretrained_mlip.get_predict_unit('uma-s-1p1', **kw)
    return FAIRChemCalculator(predictor, task_name=task)


def light_anneal(atoms, T=300, time_ps=20, dt_fs=2.0, relax_steps=500,
                fmax=0.05):
    """Brief Langevin NVT then cell+positions relax. Returns relaxed atoms +
    log dict."""
    MaxwellBoltzmannDistribution(atoms, temperature_K=T)
    n_steps = int(time_ps * 1000 / dt_fs)
    dyn = Langevin(atoms, dt_fs * units.fs, temperature_K=T, friction=0.01,
                  logfile=None)
    t0 = time.time()
    dyn.run(n_steps)
    t_md = time.time() - t0
    opt = FIRE(CellFilter(atoms), logfile=None)
    t1 = time.time()
    opt.run(fmax=fmax, steps=relax_steps)
    t_relax = time.time() - t1
    return atoms, {'T_K': T, 'time_ps': time_ps,
                   'n_relax_steps': opt.get_number_of_steps(),
                   'converged': opt.get_number_of_steps() < relax_steps,
                   't_md_s': t_md, 't_relax_s': t_relax,
                   'E_post_atom': atoms.get_potential_energy() / len(atoms)}


def _conv_verdict(opt, atoms, fmax, relax_steps, ret=None):
    """완화 하나의 수렴 판정. **한 곳에만 둔다** — 두 벌이면 두 판정이 갈린다.

    ⛔ 회신 BQ-2 Q1a (2026-09-13) — 옛 정의
      `converged = (final_fmax <= fmax) and (n_steps < relax_steps)` 는
      **마지막 허용 스텝에서 수렴한 경우를 오탐**했다. 리뷰어 실측: 최종힘 1.96 <
      기준 1.99 이고 ASE 반환값도 True 였는데 `n_steps == limit` 라 False 로 찍혔다.
      ASE 도 마지막 스텝 **뒤에** 수렴을 검사한다.
      · `converged`       : 실제 최종 힘 + 옵티마이저 반환값으로 판단
      · `hit_step_limit`  : 한도 도달을 **별도로** 기록 — 둘은 동시에 참일 수 있다

    ⛔ 이 함수가 **못 하는 것**: 가지 전환을 판정하지 않는다. 힘·스텝만으로는
      다른 골짜기인지 알 수 없다 — 그건 점별 셀·좌표가 있어야 한다 (BQ-2 Q1).
    """
    fm = float(np.linalg.norm(atoms.get_forces(), axis=1).max())
    ns = int(opt.get_number_of_steps())
    # ⛔⛔ 회신 BQ-3 P1-a (2026-09-13) — 종전 `by_force or ret is True` 는 반환값 True 면
    #   최종힘 0.14 도, **NaN 도** 기준 0.02 에 수렴으로 처리했다. 소급 판정(--regate)은
    #   힘만 보므로 라이브와 소급이 **다른 답**을 냈다.
    #   ⇒ 유한한 실제 힘 기준이 **필수**다. 반환값은 기록만 하고 판정을 덮지 않는다.
    _finite = bool(np.isfinite(fm))
    by_force = bool(_finite and fm <= fmax)
    conv = by_force
    out = {'n_steps': ns, 'final_fmax_eV_A': fm,
           'fmax_target_eV_A': float(fmax),
           'optimizer_returned': (None if ret is None else bool(ret)),
           'converged': conv,
           'hit_step_limit': bool(ns >= relax_steps)}
    if not _finite:
        out['⛔_비유한_힘'] = f'최종힘이 {fm!r} — 수렴이 아니다 (반환값과 무관)'
    if ret is not None and by_force != bool(ret):
        out['⚠_불일치'] = (f'힘 기준({fm:.5f} vs {fmax:.5f})과 옵티마이저 반환값'
                           f'({bool(ret)})이 엇갈린다 — **힘 기준이 이긴다**. 반환값으로 덮지 않는다')
    return out


def _bm3(V, E0, V0, B0, Bp):
    """3차 Birch-Murnaghan E(V). 모듈 전역이다 — 라이브 적합과 소급 재판정이
    **같은 식**을 써야 두 판정이 갈리지 않는다."""
    eta = (V0 / V) ** (2 / 3)
    return (E0 + (9 * V0 * B0 / 16) *
            ((eta - 1) ** 3 * Bp + (eta - 1) ** 2 * (6 - 4 * eta)))


def _fit_gate(r2, V0, B0_GPa, Bp, V_points):
    """BM3 적합 하나를 받아 **판정만** 한다 (회신 BQ Q2 · BQ-2 Q5).

    게이트를 한 곳에만 둔다 — 두 벌이면 라이브 경로와 `--regate` 가 다른 답을 낸다.
    반환은 **dict** 다 (판정 + 그 판정을 만든 사실들).

    ⚠ `0 < B0' < 15` 는 **보수적 운영 기준**이지 V₀ 의 물리적 필수조건이 아니다.
      회신 BQ-2 Q5: *"B₀′는 곡선의 더 높은 차수 변화에 민감해서, 최소 위치보다
      먼저 불안정해질 수 있어요."* 기존 판정은 **보존**하되, B₀′ 를 뺀
      V₀ 중심 기준(`v0_centric_ok`)을 **같이 보고**해 무엇이 달라지는지 보이게 한다.

    ⛔ 이 함수가 **못 하는 것**
      · 수렴을 보지 않는다. 사용 자격은 `attach_eligibility` 가 정한다.
      · 창을 넓히라고 말하지 않는다. 경계에 붙었다는 **사실만** 적는다.
    """
    V = np.asarray(V_points, dtype=float)
    V_min, V_max = float(V.min()), float(V.max())
    span = max(V_max - V_min, 1e-12)
    in_window = bool(V_min <= V0 <= V_max)
    # ⛔ 회신 BQ-2 Q5 — **창 경계에 붙은 최소는 양쪽을 관측한 최소와 다르다.**
    bracketed = bool(bool((V < V0).any()) and bool((V > V0).any()))
    edge_margin = float(min(V0 - V_min, V_max - V0) / span) if in_window else 0.0
    n_int = max(len(V) - 1, 1)
    at_edge = bool(in_window and edge_margin < 1.0 / n_int)   # 최외곽 구간 안이다
    b0_pos = bool(B0_GPa > 0)
    r2_ok = bool(r2 >= 0.95)
    bp_ok = bool(0.0 < Bp < 15.0)
    ok = bool(r2_ok and in_window and b0_pos and bp_ok)
    info = {'fit_quality_ok': ok, 'V0_in_window': in_window,
            'V0_bracketed': bracketed, 'V0_edge_margin_frac': edge_margin,
            'V0_at_window_edge': at_edge, 'B0_positive': b0_pos,
            'r2_ok': r2_ok, 'Bp_ok': bp_ok,
            # 회신 BQ-2 Q5 — B₀′ 를 뺀 V₀ 중심 기준. **판정을 바꾸지 않고 보이기만** 한다
            'v0_centric_ok': bool(r2_ok and in_window and b0_pos),
            '⚠_v0_centric_의_뜻': ("B0′ 조건을 뺀 기준이다. 현재 판정(fit_quality_ok)은 "
                                   "이것을 쓰지 않는다 — 바꾸려면 그 사실을 명시해야 "
                                   "한다 (회신 BQ-2 Q5)")}
    if at_edge:
        info['⚠_경계_최소'] = (f"V₀ 가 측정 창의 **최외곽 구간**에 있다 "
                               f"(경계까지 창 폭의 {edge_margin*100:.1f} %). "
                               f"양쪽을 넉넉히 관측한 최소와 같은 등급으로 쓰지 마라")
    if ok:
        info['fit_quality_reason'] = 'OK' + (' ⚠ 단 V₀ 가 창 경계에 붙어 있다' if at_edge else '')
        return info
    reason = ((f"r2={r2:.4f}" if not r2_ok else '') +
              ('' if in_window else
               f" · V₀={V0:.1f} Å³ 가 **측정 창 밖**"
               f"[{V_min:.1f}, {V_max:.1f}] — 외삽이지 측정이 아니다") +
              ('' if bracketed or not in_window else
               " · V₀ 양쪽에 측정점이 없다 (내삽이 아니다)") +
              ('' if b0_pos else f" · B₀={B0_GPa:.1f} GPa ≤ 0 (비물리)") +
              ('' if bp_ok else
               f" · B0'={Bp:.2f} 가 0<B0'<15 밖"
               f" ⚠ B0'<0 이 보편적 비물리 조건은 아니다(압력유도 연화는 실재)"
               f" — 이 게이트는 **보수적 선택**이다"))
    info['fit_quality_reason'] = reason.strip().lstrip('· ').strip()
    return info
def _fit_bm3(V, E):
    """BM3 적합 하나. **한 곳에만 둔다** — 라이브와 `--regate` 가 같은 초기값·같은 식.

    반환 `(E0, V0, B0_eV_A3, B0_GPa, Bp, r2)`. 실패하면 예외를 그대로 올린다
    (조용히 0 을 돌려주지 않는다).
    """
    from scipy.optimize import curve_fit
    V = np.asarray(V, dtype=float)
    E = np.asarray(E, dtype=float)
    p0 = [E.min(), V[E.argmin()], 0.1, 4.0]      # B0 in eV/Å³ ≈ 0.1 = 16 GPa
    popt, _ = curve_fit(_bm3, V, E, p0=p0, maxfev=10000)
    E0, V0, B0, Bp = popt
    E_pred = _bm3(V, *popt)
    ss_res = float(np.sum((E - E_pred) ** 2))
    ss_tot = float(np.sum((E - E.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(E0), float(V0), float(B0), float(B0 * 160.21766208), float(Bp), float(r2)


def _hysteresis_gate(hyst, V, hysteresis_tol=0.01, hysteresis_span_tol=0.10,
                     hysteresis_shape_tol=0.10):
    """두 갈래 이력현상 판정. **한 곳에만 둔다.**

    라이브 경로(`_eos_sweep_core`)와 소급 재판정(`--regate`)이 **같은 코드**를 써야
    두 판정이 갈리지 않는다. 종전에는 이 논리가 `eos_sweep` 안에 박혀 있었다.

    `hyst` 를 **제자리에서 채운다** (V0_up/V0_down/shape_over_span/…).
    반환 `(ok, reason)` — ok 가 False 면 호출부가 적합을 떨군다.

    ⛔ 이 함수가 **못 하는 것**
      · 골짜기 이동을 판정하지 않는다. 두 갈래가 갈렸다는 **사실만** 잰다 —
        왜 갈렸는지는 점별 구조가 있어야 안다 (회신 BQ-2 Q1·Q3).
      · 창이 다른 조건끼리 비교하지 않는다. 분모(곡선 폭)가 창에 딸려간다.
    """
    if hyst is None:
        return True, None
    from scipy.optimize import curve_fit
    bm3 = _bm3
    V = np.asarray(V, dtype=float)
    ok, reason = True, None
    try:
        _vs = []
        for _EE in (np.array(hyst['E_up']), np.array(hyst['E_down'])):
            _p, _ = curve_fit(bm3, V, _EE,
                              p0=[_EE.min(), V[_EE.argmin()], 0.1, 4.0],
                              maxfev=10000)
            _vs.append(float(_p[1]))
        hyst['V0_up'], hyst['V0_down'] = _vs
        _rel = abs(_vs[0] - _vs[1]) / max(abs(np.mean(_vs)), 1e-12)
        hyst['V0_rel_diff'] = float(_rel)
        # ⛔⛔ 2026-09-13 — **V₀ 만 보면 구멍이 난다.** 두 갈래가 곡선 자체만큼
        #   달라도 최소 **위치**는 우연히 겹칠 수 있다. 실측: P2_Al2S3_A 가
        #   maxdE/span = **95 %** 인데 V₀ 차 0.949 % 로 **통과했다.**
        #   ⇒ 곡선이 얼마나 갈렸는지를 **곡선 자신의 크기로 재서** 같이 건다.
        #   문턱 10 % 의 근거: 질서 H0 는 0.46 %, 무질서 넷은 25.4–94.8 % 로
        #   **55배 갈려 있어 1 %~25 % 어디에 둬도 판정이 같다.**
        #   문턱이 결과를 만들지 않는다는 뜻이고, 그래서 방어 가능하다.
        _span = max(float(hyst.get('E_span_eV') or 0.0), 1e-12)
        _dspan = float(hyst['max_abs_dE_eV']) / _span
        hyst['dE_over_span'] = _dspan
        hyst['tol_span'] = float(hysteresis_span_tol)
        # ⛔⛔ 회신 BQ-2 Q2 (2026-09-13) — 높이·모양 분리가 **기록에만** 있었고
        #   게이트는 여전히 원시 max_abs_dE/span 을 봤다. 리뷰어 실측: 정확한
        #   BM3 두 곡선을 0.04 eV **평행이동**하면 shape=0 이고 양방향 V₀ 가
        #   같은데도 탈락하며 "EOS 가 한 골짜기로 정의되지 않는다" 를 출력했다.
        #   ⇒ 세 기준을 **따로** 세우고, 각각의 뜻을 다르게 적는다.
        _shape = float(hyst.get('shape_max_abs_dE_eV') or 0.0)
        _lvl = abs(float(hyst.get('level_offset_eV') or 0.0))
        _shspan = _shape / _span
        hyst['shape_over_span'] = _shspan
        hyst['level_over_span'] = _lvl / _span
        hyst['tol_shape'] = float(hysteresis_shape_tol)
        # 문턱이 결과를 만드는가 — **보여준다**. 주장하지 않는다.
        hyst['shape_verdict_vs_tol'] = {
            f'{t:g}': bool(_shspan <= t) for t in (0.01, 0.02, 0.05, 0.10, 0.25)}
        hyst['⚠_문턱_의존'] = ('위 표에서 판정이 갈리면 그 문턱이 결과를 만들고 있다는 뜻이다. '
                               '전부 같으면 문턱은 일을 하지 않는다')
        _v0_ok = _rel <= hysteresis_tol
        _shape_ok = _shspan <= hysteresis_shape_tol
        _sp_ok = _dspan <= hysteresis_span_tol          # 레거시 운영 기준
        # **물리 판정**은 V₀ 일치 ∧ 모양 일치다 (평행이동은 여기에 안 들어간다)
        hyst['ok'] = bool(_v0_ok and _shape_ok)
        hyst['operational_hold'] = bool(not _sp_ok)
        hyst['⚠_세_기준의_뜻'] = {
            'V₀ 일치': '두 갈래의 최소 위치가 같은가 — 갈리면 V₀ 가 경로에 딸린다',
            '모양 일치(shape)': '평행이동 성분을 뺀 곡선 차이 — 갈리면 **보고 곡선의 곡률**이 의심된다',
            '높이차(level)': '두 갈래가 **다른 에너지의 상태**로 끝났다는 뜻이다. '
                             'V₀·곡률을 무효로 만들지는 않는다 — 상태 선택 문제다',
            '레거시 dE/span': '원시 최대차를 곡선 폭으로 나눈 값. 평행이동에도 커진다. '
                              '**운영상 보류**에만 쓰고 V₀ 존재 불가나 기전 확정의 근거로 쓰지 않는다'}
        if not (hyst['ok'] and _sp_ok):
            ok = False
            _why = []
            if not _v0_ok:
                _why.append(f"V₀ 가 갈린다 — 올라가는 갈래 {_vs[0]:.1f} vs "
                            f"내려오는 갈래 {_vs[1]:.1f} Å³ ({_rel*100:.2f} % "
                            f"> 허용 {hysteresis_tol*100:.2f} %)")
            if not _shape_ok:
                _why.append(f"**모양이 갈린다** — 평행이동을 뺀 곡선 차 "
                            f"{_shape:.3f} eV 가 곡선 폭 {_span:.3f} eV 의 "
                            f"{_shspan*100:.0f} % (> 허용 {hysteresis_shape_tol*100:.0f} %). "
                            f"V₀ 가 겹쳐도 같은 곡선이 아니다")
            if _sp_ok is False and _shape_ok and _v0_ok:
                _why.append(f"⚠ **운영상 보류** — 원시 최대차 {hyst['max_abs_dE_eV']:.3f} eV "
                            f"가 곡선 폭의 {_dspan*100:.0f} % (> {hysteresis_span_tol*100:.0f} %) "
                            f"지만 그 대부분이 **평행이동**이다 (높이차 {_lvl:.3f} eV, "
                            f"모양차 {_shape:.3f} eV). 두 갈래가 다른 에너지의 상태로 끝났다는 "
                            f"뜻이지 **V₀ 가 존재하지 않는다는 뜻이 아니다** (회신 BQ-2 Q2)")
            elif not _sp_ok:
                _why.append(f"레거시 dE/span {_dspan*100:.0f} % (> {hysteresis_span_tol*100:.0f} %) "
                            f"— 운영상 보류. 분모가 부피창에 딸려가므로 창이 다른 조건끼리 "
                            f"같은 문턱으로 비교하지 마라")
            # ⛔ 회신 BQ-3 — "이 구조에선 EOS 가 한 골짜기로 정의되지 않는다" 를 **삭제**했다.
            #   그것은 관측이 아니라 결론이고, 평행이동 보류에도 붙어 나갔다.
            reason = "이력현상 — " + " · ".join(_why)
    except Exception as _e:                                  # noqa: BLE001
        hyst['ok'] = False
        hyst['error'] = str(_e)
        ok = False
        reason = f"이력현상 검사 자체가 실패했다 ({type(_e).__name__}) — 통과로 읽지 않는다"
    return ok, reason


def _save_point_frame(atoms, cv, path, meta):
    """점별 최종 프레임을 extxyz 로 남긴다 (회신 BQ-3 Q5-2 사양).

    남기는 것 — 셀 3×3·PBC·원자 ID/원소/순서·좌표 · **힘 벡터·에너지·전체 응력(단위)** ·
    구조/조건/방향/점 ID·직전 점 ID·목표/실제 부피 · 최대힘/목표힘/반환값/스텝/수렴 ·
    코드/모델/추론 식별. **미수렴점도 저장한다** (실패 자료를 지우면 왜 실패했는지 못 본다).

    ⛔ 못 하는 것: FIRE 매 스텝을 저장하지 않는다. 끝점만이다 — 그래서 이 프레임은
      *구조 차이를 확인하는 자료*이지 *중간 경로에서 전환이 없었다는 증명*이 아니다.
    """
    a = atoms.copy()
    if 'atom_id' not in a.arrays:
        a.new_array('atom_id', np.arange(len(a), dtype=int))
    try:
        a.new_array('forces_eV_A', np.asarray(atoms.get_forces(), dtype=float))
    except Exception as e:                                   # noqa: BLE001
        a.info['forces_error'] = str(e)
    try:
        a.info['energy_eV'] = float(atoms.get_potential_energy())
    except Exception as e:                                   # noqa: BLE001
        a.info['energy_error'] = str(e)
    try:
        _st = np.asarray(atoms.get_stress(voigt=True), dtype=float)
        a.info['stress_voigt_eV_A3'] = _st.tolist()
        a.info['stress_units'] = 'eV/A^3 (ASE voigt xx yy zz yz xz xy, tension positive)'
        a.info['P_mean_GPa'] = float(-_st[:3].mean() * EV_A3_TO_GPA)
    except Exception as e:                                   # noqa: BLE001
        a.info['stress_error'] = str(e)
    a.info.update({k: (v if isinstance(v, (int, float, str, bool)) or v is None else str(v))
                   for k, v in (meta or {}).items()})
    a.info.update({'V_actual_A3': float(atoms.get_volume()),
                   'final_fmax_eV_A': float(cv.get('final_fmax_eV_A', float('nan'))),
                   'fmax_target_eV_A': float(cv.get('fmax_target_eV_A', float('nan'))),
                   'optimizer_returned': str(cv.get('optimizer_returned')),
                   'n_steps': int(cv.get('n_steps', -1)),
                   'converged': bool(cv.get('converged') is True),
                   'hit_step_limit': bool(cv.get('hit_step_limit') is True)})
    a.calc = None                                # 계산기를 떼야 extxyz 가 깨끗이 나간다
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    write(str(path), a, format='extxyz')
    return str(path)


def compare_frames(ref, new, li_symbol='Li', cutoff=3.0):
    """같은 셀 위의 두 프레임을 **원자 ID 를 유지한 채** 비교한다 (회신 BQ-3 Q5-3).

    한다: 비-Li 골격의 공통 병진 제거 → ASE 일반 최소영상(MIC) 변위 → Li / 골격 RMSD 분리 +
    최대 변위(원자 ID) → 배위수뿐 아니라 **이웃 ID 집합·거리 변화**.

    ⛔ **판정하지 않는다.** "RMSD < 0.1 Å 이면 같은 골짜기" 같은 문턱은 리뷰어가 불승인했다 —
      배위 경계의 작은 왕복도 CN 을 바꾸고, 전체 RMSD 는 한 원자의 이동을 숨긴다.
      `continuity` 는 사실 진술이다: 이웃 ID 집합이 전부 같으면 'neighbor_sets_identical',
      하나라도 다르면 'neighbor_sets_changed', 비교 자체가 안 되면 'continuity_unknown'.
    ⛔ 원자를 재정렬하지 않는다 — 재정렬하면 Li 교환이 지워진다.
    ⛔ 셀이 다르면 비교하지 않는다 (등방 스케일 차이도 포함). 같은 셀에서만 뜻이 있다.
    """
    from ase.geometry import find_mic
    out = {'continuity': 'continuity_unknown'}
    if len(ref) != len(new):
        out['why_unknown'] = f'원자 수가 다르다 ({len(ref)} vs {len(new)})'
        return out
    if list(ref.get_chemical_symbols()) != list(new.get_chemical_symbols()):
        out['why_unknown'] = '원소 순서가 다르다 — 재정렬 없이 대응할 수 없다'
        return out
    if not np.allclose(ref.cell.array, new.cell.array, atol=1e-6):
        out['why_unknown'] = '셀이 다르다 — 같은 셀에서만 비교한다'
        return out
    ids_r = ref.arrays.get('atom_id'); ids_n = new.arrays.get('atom_id')
    if ids_r is not None and ids_n is not None and not np.array_equal(ids_r, ids_n):
        out['why_unknown'] = 'atom_id 순서가 다르다'
        return out
    sym = np.array(ref.get_chemical_symbols())
    is_li = sym == li_symbol
    d_raw, _ = find_mic(new.positions - ref.positions, ref.cell, pbc=True)
    fw = ~is_li
    shift = d_raw[fw].mean(axis=0) if fw.any() else np.zeros(3)
    d = d_raw - shift                                        # 골격 공통 병진 제거
    mag = np.linalg.norm(d, axis=1)
    def _rms(m):
        return float(np.sqrt((mag[m] ** 2).mean())) if m.any() else None
    imax = int(mag.argmax())
    out.update({'framework_translation_removed_A': shift.tolist(),
                'rmsd_Li_A': _rms(is_li), 'rmsd_framework_A': _rms(fw),
                'max_disp_A': float(mag[imax]), 'max_disp_atom_index': imax,
                'max_disp_atom_symbol': str(sym[imax]),
                'n_Li': int(is_li.sum()), 'n_framework': int(fw.sum()),
                'cutoff_A': float(cutoff)})
    # 이웃 — ID 집합과 거리. 배위수만 보면 경계 왕복을 놓친다.
    from ase.neighborlist import neighbor_list
    def _nbrs(a):
        i, j, dist = neighbor_list('ijd', a, cutoff)
        m = {}
        for ii, jj, dd in zip(i, j, dist):
            m.setdefault(int(ii), {})[int(jj)] = float(dd)
        return m
    nr, nn = _nbrs(ref), _nbrs(new)
    changed, cn_r, cn_n, dmax = [], [], [], 0.0
    for k in np.where(is_li)[0]:
        k = int(k)
        sr, sn = set(nr.get(k, {})), set(nn.get(k, {}))
        cn_r.append(len(sr)); cn_n.append(len(sn))
        if sr != sn:
            changed.append({'atom_index': k, 'lost': sorted(sr - sn), 'gained': sorted(sn - sr)})
        for jj in sr & sn:
            dmax = max(dmax, abs(nr[k][jj] - nn[k][jj]))
    out.update({'n_Li_with_neighbor_set_changed': len(changed),
                'Li_neighbor_changes': changed[:20],
                'Li_CN_ref_mean': (float(np.mean(cn_r)) if cn_r else None),
                'Li_CN_new_mean': (float(np.mean(cn_n)) if cn_n else None),
                'max_common_neighbor_distance_change_A': float(dmax),
                'continuity': ('neighbor_sets_identical' if not changed else 'neighbor_sets_changed'),
                '⛔_읽는_법': ('continuity 는 이웃 ID 집합의 사실 진술이지 골짜기 판정이 아니다. '
                              '문턱을 걸어 "같은 골짜기" 라고 쓰지 마라 (회신 BQ-3 Q5-3)')})
    return out


def _select_nearest_converged(frames, conv, V0):
    """자격 있는 상승 가지에서 |Vᵢ − V₀| 가 가장 작은 **수렴점**을 고른다 (회신 BQ-3 Q5-4).

    동률 규칙(고정): |ΔV| 가 같으면 **낮은 인덱스**(작은 분율). 수렴점이 하나도 없으면 None.
    ⛔ 못 하는 것: 끝점을 금지하지 않는다. 끝점이 최근접이면 끝점이다.
    """
    if not frames or not conv or V0 is None:
        return None
    best = None
    for i, (fr, cv) in enumerate(zip(frames, conv)):
        if cv.get('converged') is not True:
            continue
        dv = abs(float(fr.get_volume()) - float(V0))
        if best is None or dv < best[1] - 1e-12:
            best = (i, dv)
    if best is None:
        return None
    i, dv = best
    return {'index': i, 'fraction': conv[i].get('fraction'), 'abs_dV_A3': float(dv),
            'V_point_A3': float(frames[i].get_volume()), 'atoms': frames[i],
            'tie_rule': '|ΔV| 동률이면 낮은 인덱스(작은 분율)'}


def _eos_branch(atoms_ref, calc, fractions, fmax, relax_steps, continuation,
                save_dir=None, meta=None, direction='up'):
    """한 갈래의 E(V). `continuation` 이면 **앞 점의 완화 결과**에서 이어간다.

    ⛔ 왜 이게 필요한가 (2026-09-13 실측). 독립 완화판은 부피점마다
      `atoms_ref.copy()` 로 다시 시작한다. 무질서계(Li 공공·치환 자리 무작위)는
      PES 에 가까운 국소최소가 많아 **부피마다 다른 골짜기**에 떨어지고,
      그 에너지 차(0.1–0.45 eV)가 부피창의 곡률과 같은 크기라 BM3 적합이 깨진다.
      실측: P2_Al2S3_B 시드 3개에서 r² 0.79 / 0.998 / 0.90.
      질서 있는 H0 만 r² 0.99997 로 깨끗했다 — 무질서가 원인이라는 증거다.
    """
    V, E, conv, frames = [], [], [], []
    prev = None
    final = None
    prev_id = None
    if 'atom_id' not in atoms_ref.arrays:
        atoms_ref = atoms_ref.copy()
        atoms_ref.new_array('atom_id', np.arange(len(atoms_ref), dtype=int))
    for _i, f in enumerate(fractions):
        if continuation and prev is not None:
            atoms = prev.copy()                      # 앞 점의 **완화된** 구조에서
            atoms.set_cell(atoms.cell.array * (f / prev_f) ** (1 / 3), scale_atoms=True)
        else:
            atoms = atoms_ref.copy()
            atoms.set_cell(atoms.cell.array * f ** (1 / 3), scale_atoms=True)
        atoms.calc = calc
        opt = FIRE(atoms, logfile=None)              # 고정셀 · 원자만
        _ret = opt.run(fmax=fmax, steps=relax_steps)
        # ⛔⛔ 회신 BQ P0-1 (2026-09-13) — 종전에는 `opt.run(...)` 의 결과를 **버렸다.**
        #   그래서 점마다 **수렴했는지·최종 최대힘이 얼마인지** 기록이 없었고,
        #   두 갈래의 에너지 차이를 보고 *"다른 국소최소"* 라고 말할 근거가 없었다
        #   (셋 다 미수렴이어도 같은 모양이 나온다). 이제 남긴다 — 이 기록이 없으면
        #   이 곡선으로 **아무 기전 판정도 하지 않는다.**
        _cv = _conv_verdict(opt, atoms, fmax, relax_steps, _ret)
        _cv['fraction'] = float(f)
        _pid = f"{direction}:{_i:02d}:f{float(f):.4f}"
        _cv['point_id'] = _pid
        _cv['prev_point_id'] = prev_id
        if save_dir is not None:
            _m = dict(meta or {})
            _m.update({'direction': direction, 'point_index': _i, 'fraction': float(f),
                       'point_id': _pid, 'prev_point_id': str(prev_id),
                       'V_target_A3': float(atoms_ref.get_volume() * float(f)),
                       'continuation': bool(continuation)})
            _cv['frame_path'] = _save_point_frame(
                atoms, _cv, Path(save_dir) / f"{_m.get('structure', 'x')}_{_pid.replace(':', '_')}.extxyz", _m)
        conv.append(_cv)
        V.append(atoms.get_volume())
        E.append(atoms.get_potential_energy())
        frames.append(atoms)
        prev, prev_f, prev_id = atoms, f, _pid
        final = atoms
    return np.array(V), np.array(E), conv, final, frames


def _eos_sweep_core(atoms_ref, calc, fractions=(0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06),
             fmax=0.05, relax_steps=500, continuation=False, hysteresis_tol=0.01,
             hysteresis_span_tol=0.10, hysteresis_shape_tol=0.10,
             save_dir=None, meta=None):
    """Volume sweep + Birch-Murnaghan 3rd-order fit. atoms_ref is the
    relaxed reference at V0; we scale its lattice by f^(1/3) per point.

    `continuation=True` (2026-09-13, 회신 BP §4b 후속):
      부피점을 **이어서** 완화한다 — 앞 점의 완화 결과가 다음 점의 출발점이다.
      매 단계가 이미 완화된 상태에서의 작은 섭동이라 같은 골짜기에 머문다.
      ⭐ **양방향으로 돌고 두 갈래가 일치하는지 본다**(이력현상 검사).
        올라가는 갈래(0.94→1.06)와 내려오는 갈래(1.06→0.94)의 V₀ 가
        `hysteresis_tol`(기본 1 %) 넘게 갈리면 **fit_quality_ok=False** 로 떨군다.
        ⇒ 이 방식은 **자기가 언제 실패했는지 말한다.** best-of-N 선택과 정반대다.
      ⚠ **V₀ 의 뜻이 조금 달라진다**: "그 부피에서 찾은 아무 최소" 가 아니라
        **"기준 구조에서 연속으로 이어진 가지 위의 최소"** 다. P1/P2 를 같은
        골짜기 기준으로 비교하려는 우리 목적에는 이쪽이 맞지만, **다른 양이다.**
      ⛔ 골짜기 이동을 **줄이지 없애지는 못한다.** 어떤 부피에서 그 골짜기가
        실제로 불안정해지면 넘어간다 — 그때 이력현상 검사가 잡는다.
    """
    n = len(atoms_ref)
    fr = list(fractions)
    hyst = None
    branch_state = None
    branch_frames = None
    conv_log = None
    if continuation:
        V_up, E_up, c_up, s_up, f_up = _eos_branch(atoms_ref, calc, fr, fmax, relax_steps, True,
                                                   save_dir=save_dir, meta=meta, direction='up')
        V_dn, E_dn, c_dn, _, f_dn = _eos_branch(atoms_ref, calc, fr[::-1], fmax, relax_steps, True,
                                                save_dir=save_dir, meta=meta, direction='down')
        V_dn, E_dn = V_dn[::-1], E_dn[::-1]          # 오름차순으로 되돌린다
        # ⛔⛔ 회신 BQ P0-2 (2026-09-13) — 종전에는 점마다 `min(E_up, E_down)` 을 골라
        #   적합했다. 그건 **하나의 연속된 가지가 아니다** — 두 곡선이 교차하면 서로 다른
        #   가지를 이어 붙인다(하위 포락선). docstring 은 "연속으로 이어진 가지" 라고
        #   적어 놓고 코드는 다른 일을 하고 있었다.
        #   ⇒ **올라가는 갈래 하나를 보고 곡선으로 쓴다.** 내려오는 갈래는 비교용으로만
        #     남기고, 둘의 차이는 이력현상 진단에서 본다. 섞지 않는다.
        # ⚠ 회신 BQ Q2 — 높이 차와 모양 차를 **분리해서** 낸다. E_dn = E_up + C 면
        #   V₀·곡률·압력이 완전히 같은데도 옛 dE/span 은 크게 나왔다.
        _d = E_up - E_dn
        _shape = _d - _d.mean()                      # 평행이동 성분 제거 = 모양 차이만
        hyst = {'E_up': E_up.tolist(), 'E_down': E_dn.tolist(),
                'reported_branch': 'up',
                'max_abs_dE_eV': float(np.abs(_d).max()),
                'level_offset_eV': float(_d.mean()),
                'shape_max_abs_dE_eV': float(np.abs(_shape).max()),
                'E_span_eV': float(max(E_up.max() - E_up.min(),
                                       E_dn.max() - E_dn.min())),
                'tol_V0_rel': float(hysteresis_tol),
                '⚠_dE_over_span_는_창에_의존한다': ('분모(E_span)가 부피창에 딸려 줄어든다. '
                                              '창이 다른 조건끼리 같은 문턱으로 비교하지 마라 '
                                              '— 회신 BQ Q2. 창 비교는 절대값(shape_max_abs_dE_eV)으로 한다'),
                'convergence_up': c_up, 'convergence_down': c_dn}
        V, E = V_up, E_up                            # **한 갈래만** 보고한다
        branch_state = s_up
        branch_frames = f_up
    else:
        V, E, conv_log, branch_state, branch_frames = _eos_branch(
            atoms_ref, calc, fr, fmax, relax_steps, False,
            save_dir=save_dir, meta=meta, direction='up')
    # 3rd-order Birch-Murnaghan fit
    try:
        from scipy.optimize import curve_fit
        bm3 = _bm3                    # ⭐ 전역 — `--regate` 와 **같은 식**을 쓴다
        E0, V0, B0, B0_GPa, Bp, r2 = _fit_bm3(V, E)
        # A-3 fix: r² gate. Diverged BM3 fits (r²<0.95) shouldn't poison
        # downstream rankings; flag B0_GPa as None and set fit_quality_ok=False
        # so combine_rankings can drop them.
        # N-? fix: also gate on a physical B0' (0<Bp<15). A BM3 fit can have high
        # r² yet diverge to garbage (e.g. B0=2.2 GPa, Bp=-306) — those slip past
        # the r² gate but are unphysical; require a sane B0' so B0_GPa→None.
        # ⛔ 2026-09-13 — `bool(...)` 로 감싼다. numpy 비교는 `np.bool_` 을 내고,
        #   기록을 쓰는 `json.dumps(..., default=str)` 이 그걸 **문자열 "False"** 로
        #   직렬화한다. 하류가 `if rec['fit_quality_ok']:` 로 읽으면 **"False" 가 참**이다.
        #   (실측: eos_diag per_seed 가 "False"/"True" 문자열로 나왔다)
        # ⛔ 회신 BQ Q2 (2026-09-13) — 기본 확인 둘이 빠져 있었다:
        #   ① **B₀ > 0** — 음수 체적탄성률은 그 자체로 비물리다. 옛 게이트는 Bp 만 봤다.
        #   ② **최소점이 측정 부피창 안에 있는가** — 옛 조건 `0 < V0 < 5*V_mid` 는
        #     창 밖으로 한참 벗어난 V₀ 도 통과시켰다. 실측: P2_Al2S3_B 가 V₀ 5620 Å³
        #     (셀 4066, 창 밖 38 %)로 나왔는데 그건 **외삽**이지 측정이 아니다.
        #     창 밖 최소는 "이 창에서는 최소를 못 봤다" 는 뜻이다.
        _gi = _fit_gate(r2, V0, B0_GPa, Bp, V)
        fit_ok = _gi['fit_quality_ok']
        _in_window, _b0_pos = _gi['V0_in_window'], _gi['B0_positive']
        _gate_reason = _gi['fit_quality_reason']
        # ⭐ 연쇄판 이력현상 게이트 — 두 갈래를 **각각** 적합해 V₀ 가 일치하는지 본다.
        #   갈리면 그 구조에선 EOS 가 잘 정의되지 않는다 (골짜기가 부피에 따라 바뀐다).
        _hyst_ok, _hyst_reason = _hysteresis_gate(
            hyst, V, hysteresis_tol, hysteresis_span_tol, hysteresis_shape_tol)
        if not _hyst_ok:
            fit_ok = False
        return {'V_points': V.tolist(), 'E_points': E.tolist(),
                'fractions': list(fractions),
                'continuation': bool(continuation),
                'hysteresis': hyst,
                'convergence': conv_log,
                # ⛔ 회신 BQ P0-3 — V₀ **숫자**만 넘기면 그 V₀ 를 정의한 **상태**가 안 간다.
                #   보고 곡선(올라가는 갈래)의 마지막 구조를 같이 돌려준다.
                #   ⚠ JSON 직렬화 전에 `process_one` 이 pop 한다 (Atoms 는 직렬화 불가).
                '_branch_atoms': branch_state,
                '_branch_frames': branch_frames,     # 최근접 수렴점 승계용 (직렬화 전 pop)
                'V0': float(V0) if fit_ok else None,
                'V0_per_atom': float(V0) / n if fit_ok else None,
                'E0': float(E0) if fit_ok else None,
                'B0_eV_per_A3': float(B0) if fit_ok else None,
                'B0_GPa': float(B0_GPa) if fit_ok else None,
                'Bp': float(Bp) if fit_ok else None,
                'r2': float(r2),
                'fit_quality_ok': fit_ok,
                'V0_in_window': _in_window,
                'B0_positive': _b0_pos,
                'gate_detail': _gi,
                'fit_quality_reason': ('OK' if fit_ok
                                      else (_hyst_reason or _gate_reason))}
    except Exception as e:
        # ⛔ 2026-09-13 — 종전에는 적합이 터지면 **수렴 기록·이력 기록까지 통째로 버렸다.**
        #   그래서 *"왜 실패했나"* 를 볼 자료가 실패한 경우에만 없어졌다 — 정확히 반대다.
        #   진단은 실패했을 때 더 필요하다. 그대로 싣는다.
        return {'V_points': V.tolist(), 'E_points': E.tolist(),
                'fractions': list(fractions),
                'continuation': bool(continuation),
                'hysteresis': hyst,
                'convergence': conv_log,
                '_branch_atoms': branch_state,
                '_branch_frames': branch_frames,     # 최근접 수렴점 승계용 (직렬화 전 pop)
                'fit_quality_ok': False,
                'fit_quality_reason': f'BM3 적합이 예외로 실패했다: {type(e).__name__}: {e}',
                'fit_error': str(e)}


def eos_ensemble(atoms_ref, calc, n_seeds=5, perturb=0.1,
                 fractions=(0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06),
                 fmax=0.05, relax_steps=500, continuation=False,
                 hysteresis_tol=0.01, hysteresis_span_tol=0.10,
                 hysteresis_shape_tol=0.10, save_dir=None, meta=None):
    """Run eos_sweep on N rattled copies of atoms_ref and keep the BEST BM3 fit.

    MLIP single-curve EOS is basin-sensitive: a stray Li/ion rearrangement at one
    volume kinks the curve and gives an unphysical B0' (e.g. the Nd-doped case had
    B0' from -64 to +16 across seeds while the clean fits clustered at ~6). The
    best-of-N curve avoids that. Returns the selected curve's dict (SAME schema as
    eos_sweep, so downstream is unchanged) plus an 'ensemble' summary (per-seed +
    mean/std). Selection: highest r² among physical fits (fit_ok and 0<B0'<15);
    fall back to highest r² with a B0; else the first result.
    """
    results = []
    for s in range(n_seeds):
        a = atoms_ref.copy()
        if s > 0:
            a.rattle(stdev=perturb, seed=s)
        results.append(eos_sweep(a, calc, fractions=fractions, fmax=fmax,
                                 relax_steps=relax_steps,
                                 continuation=continuation,
                                 hysteresis_tol=hysteresis_tol,
                                 hysteresis_span_tol=hysteresis_span_tol,
                                 hysteresis_shape_tol=hysteresis_shape_tol,
                                 save_dir=(None if save_dir is None else Path(save_dir) / f'seed{s}'),
                                 meta=(None if meta is None else {**meta, 'seed': s})))
    # ⛔⛔ 회신 BQ-2 P0-1 — **자격을 가장 앞에 둔다.** 종전 선택은 `fit_quality_ok`
    #   (회귀 지표) 만 봤으므로, 점이 하나도 수렴하지 않은 시드도 r² 만 높으면 뽑혔다.
    eligible = [r for r in results if r.get('downstream_eligible') is True]
    physical = [r for r in (eligible or results)
                if r.get('fit_quality_ok') and r.get('B0_GPa') is not None
                and r.get('Bp') is not None and 0.0 < r['Bp'] < 15.0]
    pool = physical or [r for r in results if r.get('B0_GPa') is not None] or results
    best = dict(max(pool, key=lambda r: r.get('r2', -1.0)))
    _n_elig = len(eligible)
    b0s = [r['B0_GPa'] for r in results if r.get('B0_GPa') is not None]
    _nfit = int(sum(1 for r in results if r.get('fit_quality_ok')))
    # ⛔⛔ 2026-09-13 — `std` 가 **거짓 정밀도**를 낸다. 살아남은 값이 하나면
    #   `np.std([x]) == 0.0` 이고, 화면에는 *"시드 간 완벽 일치"* 로 읽힌다.
    #   실측(P2_Al2S3_B, 시드 3): r² 0.79 / 0.998 / 0.90 → **2개 실패**, 통과 1개.
    #   그런데 std 는 0.0 이었다. 정반대의 뜻으로 읽히는 숫자다.
    #   ⇒ 표본이 2 미만이면 **None**. 그리고 몇 개로 잰 값인지(`n_B0`)를 같이 낸다.
    _std = float(np.std(b0s)) if len(b0s) >= 2 else None
    best['ensemble'] = {
        'n_seeds': int(n_seeds), 'perturb': float(perturb),
        'n_fit_ok': _nfit,
        'n_physical_Bp': len(physical),
        'n_B0': len(b0s),
        'B0_GPa_mean': float(np.mean(b0s)) if b0s else None,
        'B0_GPa_std': _std,
        '⚠_std_가_None_인_이유': (None if _std is not None else
                                f'B0 를 낸 시드가 {len(b0s)}개뿐이라 산포를 잴 수 없다. '
                                f'0.0 이 아니다 — 0.0 은 일치를 뜻하는데 그게 아니다'),
        'B0_GPa_median': float(np.median(b0s)) if b0s else None,
        'n_downstream_eligible': _n_elig,
        'selection': (('max_r2_eligible_physical_Bp' if _n_elig else 'max_r2_physical_Bp')
                      if physical else ('max_r2_any' if b0s else 'all_failed')),
        '⛔_자격_경고': (None if _n_elig == int(n_seeds) else
                      f'시드 {n_seeds}개 중 **후속 사용 자격을 갖춘 것은 {_n_elig}개**다 '
                      f'(자격 = 적합 품질 ∧ 보고 가지 전 점 수렴). 0개면 아래 값은 '
                      f'회귀 지표일 뿐이고 **다음 계산에 쓰면 안 된다**'),
        '⛔_선택_경고': (None if _nfit == int(n_seeds) else
                     f'시드 {n_seeds}개 중 **{int(n_seeds)-_nfit}개가 적합 실패**했고 '
                     f'아래 값은 살아남은 것 중 r² 최대를 **고른 것**이다. '
                     f'결과를 보고 고르는 선택이므로 **산포의 근거가 아니다** — '
                     f'적합이 시드에 민감하면 골짜기 이동(basin hopping)을 의심해라'),
        'per_seed': [{'B0_GPa': r.get('B0_GPa'), 'V0_per_atom': r.get('V0_per_atom'),
                      'Bp': r.get('Bp'), 'r2': r.get('r2'),
                      'fit_quality_ok': r.get('fit_quality_ok'),
                      'downstream_eligible': r.get('downstream_eligible'),
                      'convergence_summary': r.get('convergence_summary')}
                     for r in results],
    }
    return best


# ══════════════════════════════════════════════════════════════════════════
# 셀 정책 (2026-09-13 · 회신 BP Q4③ 지적 → 실물 확인 → 이행)
#
# ⛔⛔ **GAP-3 실측**: `eos_sweep` 은 점마다 `atoms_ref.copy()` 로만 작업해
#   **atoms_ref 를 바꾸지 않는다**. 그래서 `process_one` 이 V₀ 를 record 에
#   기록만 하고, 이어지는 `elastic_finite_strain(atoms, ...)` 에는 여전히
#   **2단계 post-anneal 구조**가 들어갔다 — 즉 **탄성이 보고된 V₀ 가 아닌
#   부피에서 계산됐다.** 두 양이 같은 구조를 가리킨다고 읽으면 틀린다.
#
# ⚠ 기본 동작은 **바꾸지 않는다** (과거 명령의 재현성). 대신
#   ① `--apply_eos_v0` 로 명시하면 V₀ 를 실제로 적용하고
#   ② 적용하든 안 하든 `record['cell_policy']` 에 **무엇을 했는지 남긴다**.
#   적용 안 한 경우에도 경고 문자열이 출력에 박히므로 조용히 지나가지 않는다.
#
# 형상 정책의 정확한 표현 (회신 BP):
#   "셀 각도와 길이비를 고정하고 등방 E(V) 경로에서 부피를 최적화한다.
#    **목표** 평균압은 0 GPa 이며, **실제 잔류 평균압과 편차응력을 별도로 보고**한다."
#   ⛔ '전체 응력 0' · '자유 영응력 평형' 과 다르다.
# ══════════════════════════════════════════════════════════════════════════
EV_A3_TO_GPA = 160.21766208


def stress_report(atoms):
    """실제 잔류 응력 — 평균압과 편차성분을 **따로** 낸다 (회신 BP Q4③).

    ⛔ 이 함수가 하지 않는 것: '영응력이다' 판정. 숫자만 낸다.
    """
    import numpy as _np
    v = _np.asarray(atoms.get_stress(voigt=True), dtype=float) * EV_A3_TO_GPA
    sig = _np.array([[v[0], v[5], v[4]], [v[5], v[1], v[3]], [v[4], v[3], v[2]]])
    # ⛔ 회신 BQ P1 (2026-09-13) — ASE `get_stress()` 는 **인장 양수** 규약이다.
    #   실측(EMT/Cu): 0.95 로 압축한 셀에서 trace(σ)/3 = **−7.649 GPa**.
    #   압축 상태의 물리적 압력은 양수여야 하므로 **P = −trace(σ)/3** 이 맞다.
    #   종전에는 +trace/3 을 압력이라 적어 **부호가 뒤집혀 있었다.**
    #   ⚠ 편차응력은 정의상 `σ − (trace σ/3)·I` 이므로 **거기까지 뒤집지 않는다.**
    _tr3 = float(_np.trace(sig) / 3.0)
    p = -_tr3
    dev = sig - _tr3 * _np.eye(3)
    return {'sigma_GPa': sig.tolist(), 'P_mean_GPa': p,
            'trace_over_3_GPa': _tr3,
            '⚠_부호': 'P = −trace(σ)/3 (압축 양수). ASE 는 인장 양수 규약이다',
            'deviatoric_max_abs_GPa': float(_np.abs(dev).max()),
            '⚠': '목표 평균압 0 과 별개로 **실제** 값이다. 영응력 판정 아님'}


def _records_match_points(rows, fractions, n_points):
    """수렴 기록이 부피점과 **1:1** 인가 (회신 BQ-3 P1-b).

    개수가 같고, 기록의 분율 집합이 요청 분율 집합과 같아야 한다 (방향은 무관 —
    하강 갈래는 역순이다). 분율이 없으면 개수만 본다 (구버전 기록 호환).

    ⛔ 못 하는 것: 기록의 **값**이 맞는지는 못 본다. 자리가 다 있는지만 본다.
    """
    rows = rows or []
    if len(rows) != int(n_points) or int(n_points) == 0:
        return False
    if not fractions:
        return True
    got = sorted(float(r.get('fraction')) for r in rows if r.get('fraction') is not None)
    want = sorted(float(f) for f in fractions)
    if len(got) != len(want):
        return False
    return all(abs(a - b) < 1e-9 for a, b in zip(got, want))


def attach_eligibility(out):
    """EOS 결과에 **후속 사용 자격**을 붙인다 (회신 BQ-2 P0-1).

    ⛔⛔ 왜 새 필드인가 — `fit_quality_ok` 는 **회귀 지표**다(적합이 잘 됐나).
      *이 결과를 다음 계산에 써도 되는가* 는 다른 질문인데 종전에는 같은 것으로
      취급했다. 리뷰어 실측(2026-09-13): 굶겨서 **수렴 0/14**, 점별 최종힘
      0.0403–0.1448 eV/Å 인데도 `fit_quality_ok=True` 로 V₀ 가 나왔다.
      수렴을 **기록만** 하고 게이트에 배선하지 않았던 것이다.

    자격 = 적합 품질 ∧ **보고 가지의 모든 점이 수렴**.
    반대 가지의 수렴은 진단으로 따로 싣는다 — 이력현상은 두 갈래 **사이**의 양이라
    한쪽만 보고 판단하면 안 된다 (2026-09-13 에 내가 그렇게 틀렸다).

    ⛔ 이 함수가 **못 하는 것**
      · 없는 기록을 있다고 하지 않는다. 수렴 기록이 아예 없으면 자격을 **거부**한다
        — 모르는 것은 통과가 아니다.
      · 가지 전환(골짜기 이동)을 판정하지 않는다. 그건 점별 좌표가 있어야 한다.
    """
    hy = out.get('hysteresis') or {}
    up = hy.get('convergence_up') or out.get('convergence') or []
    dn = hy.get('convergence_down') or []
    _two_way = bool(hy) and ('E_down' in hy)

    def _cnt(rows):
        return sum(1 for r in rows if r.get('converged') is True), len(rows)

    n_up, m_up = _cnt(up)
    n_dn, m_dn = _cnt(dn)
    # ⛔⛔ 회신 BQ-3 P1-b — 종전에는 **기록 개수만** 셌다. 에너지 7점에 수렴 기록 1개를
    #   남겨도 1/1 로 통과했다. 기록이 부피점과 **빠짐없이 1:1** 대응해야 한다.
    _frac = list(out.get('fractions') or [])
    _nV = len(out.get('V_points') or [])
    _match_up = _records_match_points(up, _frac, len(hy.get('E_up') or []) if _two_way else _nV)
    _match_dn = _records_match_points(dn, _frac, len(hy.get('E_down') or [])) if _two_way else True
    out['convergence_summary'] = {
        'reported_branch': hy.get('reported_branch', 'single'),
        'n_converged_reported': n_up, 'n_points_reported': m_up,
        'n_converged_other': n_dn, 'n_points_other': m_dn,
        '⚠_나눠_센다': ('보고 가지와 반대 가지를 **따로** 센다. 화면에 한 숫자만 띄우면 '
                        '양방향 수렴으로 오독한다 (2026-09-13 실측 사고)')}
    why = []
    if m_up == 0:
        why.append('수렴 기록이 없다 — 모르는 것은 통과가 아니다')
    elif not _match_up:
        why.append(f'보고 가지 수렴 기록({m_up}개)이 부피점과 **1:1 대응하지 않는다** '
                   f'(부피점 {len(hy.get("E_up") or []) if _two_way else _nV}개 · 분율 {_frac}) — '
                   f'개수만 맞는 기록은 전수가 아니다')
    elif n_up < m_up:
        _bad = [f"f={r.get('fraction')}: |F|max={r.get('final_fmax_eV_A', float('nan')):.4f}"
                for r in up if r.get('converged') is not True]
        why.append(f'보고 가지 {m_up}점 중 **{m_up - n_up}점 미수렴** (' +
                   ' · '.join(_bad[:4]) + (' …' if len(_bad) > 4 else '') + ')')
    # ⛔⛔ 회신 BQ-3 P0-1 잔여 — 이력현상 게이트는 **하강 에너지도 판정에 쓴다**. 그런데 자격은
    #   상승 수렴만 요구했다. 리뷰어 재현: 상승 7/7·하강 0/7 → eligible=True, 하강 기록을
    #   없애도 통과. **판정에 쓴 양방향 점의 수렴이 필요하다.** 하강 미수렴은 "이력현상이
    #   없다" 가 아니라 "그 검사가 미확정" 이다.
    #   (하강을 참고자료로만 쓰려면 승격 조건에서도 분리해야 하고 그건 **정책 변경**이다 —
    #    지금 정책은 두 갈래를 다 쓴다.)
    if _two_way:
        if m_dn == 0:
            why.append('하강 갈래 수렴 기록이 없다 — 이력현상 판정에 쓴 점인데 수렴을 모른다')
        elif not _match_dn:
            why.append(f'하강 갈래 수렴 기록({m_dn}개)이 부피점과 1:1 대응하지 않는다')
        elif n_dn < m_dn:
            _badd = [f"f={r.get('fraction')}: |F|max={r.get('final_fmax_eV_A', float('nan')):.4f}"
                     for r in dn if r.get('converged') is not True]
            why.append(f'하강 갈래 {m_dn}점 중 **{m_dn - n_dn}점 미수렴** — 이력현상 검사가 '
                       f'**미확정**이다 (' + ' · '.join(_badd[:4]) + (' …' if len(_badd) > 4 else '') + ')')
    if out.get('fit_quality_ok') is not True:
        why.append('적합 품질 불통과: ' + str(out.get('fit_quality_reason')))
    out['downstream_eligible'] = bool(not why)
    out['downstream_block_reason'] = (None if not why else ' · '.join(why))
    out['⛔_자격과_적합품질은_다르다'] = (
        'fit_quality_ok 는 회귀 지표(적합이 잘 됐나)이고 downstream_eligible 은 '
        '이 결과를 다음 계산에 써도 되는가다. V₀ 승계·탄성·MD 의 조건은 **후자**다')
    return out


def eos_sweep(*a, **k):
    """`_eos_sweep_core` + **사용 자격**(회신 BQ-2 P0-1). 호출부는 이걸 쓴다."""
    return attach_eligibility(_eos_sweep_core(*a, **k))


def apply_v0_fixed_shape(atoms_ref, V0, calc, fmax=0.05, relax_steps=500):
    """**셀 각도·길이비를 고정한 채** 부피만 V₀ 로 맞추고 원자만 완화한다.

    등방 스케일이므로 각도와 길이비는 구조적으로 보존된다 — 그것이 이 정책이
    'argyrodite 골격 보존' 을 뜻하는 방식이다.

    ⛔ 이 함수가 **못 하는 것**
      · 셀 형상을 최적화하지 않는다 (그것이 금지된 vc-relax 다).
      · 편차응력을 없애지 않는다 — 없애려면 형상을 풀어야 한다. 남은 값을 **보고**한다.
      · V₀ 가 None 이면 아무것도 하지 않고 그대로 돌려준다 (BM 적합 실패 시).
      · **`applied` 는 '완화를 돌렸다' 는 뜻이지 '수렴했다' 가 아니다.**
        쓸 자격은 `converged` 가 정한다 (회신 BQ-2 P0-1).
    """
    if V0 is None:
        return atoms_ref, {'applied': False, 'reason': 'V0 is None (BM 적합 실패)'}
    a = atoms_ref.copy()
    f = float(V0) / a.get_volume()
    a.set_cell(a.cell.array * f ** (1.0 / 3.0), scale_atoms=True)
    a.calc = calc
    opt = FIRE(a, logfile=None)                 # ← 고정셀: CellFilter 를 쓰지 않는다
    _ret = opt.run(fmax=fmax, steps=relax_steps)
    # ⛔⛔ 회신 BQ-2 P0-1 — 옛 판정은 `n_steps < relax_steps` 뿐이라 **힘을 아예 안 봤다.**
    #   한도 전에 멈추기만 하면 잔여힘이 얼마든 '수렴' 이었다.
    _cv = _conv_verdict(opt, a, fmax, relax_steps, _ret)
    rep = {'applied': True, 'V0_target_A3': float(V0),
           'V_before_A3': float(atoms_ref.get_volume()),
           'V_after_A3': float(a.get_volume()),
           'scale_factor': f,
           'n_relax_steps': _cv['n_steps'],
           '⚠_applied_의_뜻': "완화를 돌렸다는 뜻이다. 쓸 자격은 'converged' 가 정한다"}
    rep.update(_cv)
    try:
        rep['residual_stress'] = stress_report(a)
    except Exception as e:                       # 계산기가 응력을 못 내는 경우
        rep['residual_stress'] = {'error': str(e)}
    return a, rep


def maybe_apply_eos_v0(atoms, record, args, calc):
    """EOS V₀ 를 적용할지 말지의 **갈림길 자체**. selftest 가 이 함수를 친다.

    반환 (atoms, policy_dict). 적용 안 한 경우에도 policy_dict 에 **경고가 박힌다** —
    조용히 지나가지 않게 하는 것이 이 함수의 목적이다.

    ⛔ 이 함수가 **못 하는 것**: 어느 쪽이 옳은지 판정하지 않는다. 무엇을 했는지 적을 뿐이다.
    """
    pol = {
        'step0_relax': ('FIRE(atoms) — 고정셀(각도·길이비 보존)'
                        if getattr(args, 'fixed_shape_relax', False)
                        else 'CellFilter(atoms) — 형상 무제한'),
        'eos_v0_applied': False,
        '표현': ('셀 각도와 길이비를 고정하고 등방 E(V) 경로에서 부피를 최적화한다. '
                 '목표 평균압은 0 GPa 이며, 실제 잔류 평균압과 편차응력을 별도로 보고한다'),
    }
    no_eos = bool(getattr(args, 'no_eos', False))
    if getattr(args, 'apply_eos_v0', False) and not no_eos:
        _eos = record.get('eos') or {}
        v0 = _eos.get('V0')
        _bs = _eos.get('_branch_atoms')
        _orig = atoms                      # ← 차단하면 **원본으로 되돌린다**
        # ⛔⛔ 회신 BQ-2 P0-3 (2026-09-13) — 내 P0-3 '상태 승계' 수정이 만든 **회귀**를 막는다.
        #   종전에는 v0 가 None 이어도 `_start = _bs` 를 골랐고, apply 는 V0=None 이면
        #   `atoms_ref` 를 **그대로** 돌려주므로 실패한 EOS 의 **마지막 팽창점**이 최종
        #   구조로 승격됐다. 리뷰어 실측: 원본 100 → 실패 EOS 끝점 106 이
        #   final_v0_applied.xyz 와 탄성에 그대로 들어갔다 (fit_quality_ok=False 인데도).
        _block = None
        if v0 is None:
            _block = 'BM3 적합이 V₀ 를 내지 못했다'
        elif _eos.get('downstream_eligible') is not True:
            _block = ('EOS 결과가 후속 사용 자격 미달 — %s'
                      % (_eos.get('downstream_block_reason')
                         or '자격 필드가 없다(구버전 기록) — 모르는 것은 통과가 아니다'))
        elif _bs is None:
            _block = ('V₀ 를 정의한 **상태**(보고 가지의 구조)가 없다 — 연쇄 미사용 또는 '
                      '기록 유실. 숫자만 맞추고 다른 골짜기에서 완화하는 것은 승계가 아니다')
        if _block is not None:
            pol['eos_v0_applied'] = False
            pol['downstream_blocked'] = True
            pol['block_reason'] = _block
            pol['⛔차단'] = ('V₀ 적용을 요청했으나 **차단**했다: %s. 최종 구조 승격과 '
                             '후속 계산(탄성·MD)을 하지 않는다. 구조가 있으면 진단용으로만 '
                             '남긴다 (회신 BQ-2 P0-3).' % _block)
            pol['_diagnostic_atoms'] = _bs
            return _orig, pol

        # ⭐ 회신 BQ-3 Q5-4 — 끝점이 아니라 **자격 있는 상승 가지에서 |Vᵢ−V₀| 최소 수렴점**에서
        #   출발한다. 끝점은 V₀ 를 지나 팽창하는 동안 가지가 바뀌었을 수 있다 (BQ-2 Q3).
        _frames = _eos.get('_branch_frames')
        _cup = ((_eos.get('hysteresis') or {}).get('convergence_up')
                or _eos.get('convergence') or [])
        _sel = _select_nearest_converged(_frames, _cup, v0) if _frames else None
        if _sel is None:
            _start = _bs
            pol['v0_start_state'] = ('⚠ EOS 보고 가지의 **마지막 구조** (점별 프레임 없음 — '
                                     '최근접 수렴점을 고를 수 없어 끝점을 썼다)')
            pol['v0_start_selection'] = {'method': 'last_point_fallback'}
        else:
            _start = _sel['atoms']
            pol['v0_start_state'] = (f"EOS 상승 가지 **최근접 수렴점** (index {_sel['index']}, "
                                     f"f={_sel['fraction']}, |ΔV|={_sel['abs_dV_A3']:.2f} Å³)")
            pol['v0_start_selection'] = {k: v for k, v in _sel.items() if k != 'atoms'}
            pol['v0_start_selection']['method'] = 'nearest_converged_up_branch'
        # ① 원자 대응·셀 형상·목표 부피 확인 (등방 스케일 **전**에 기록)
        _scaled = _start.copy()
        _scaled.set_cell(_scaled.cell.array * (float(v0) / _scaled.get_volume()) ** (1 / 3),
                         scale_atoms=True)
        pol['succession_checks'] = {
            '1_atom_correspondence': {'n_atoms': len(_start),
                                      'has_atom_id': bool('atom_id' in _start.arrays)},
            '1_cell_shape_preserved': bool(
                np.allclose(_start.cell.angles(), _scaled.cell.angles(), atol=1e-9)
                and np.allclose(_start.cell.lengths() / _start.cell.lengths()[0],
                                _scaled.cell.lengths() / _scaled.cell.lengths()[0], atol=1e-9)),
            '1_V_target_A3': float(v0), '1_V_scaled_A3': float(_scaled.get_volume())}
        _new, rep = apply_v0_fixed_shape(_start, v0, calc,
                                         fmax=getattr(args, 'eos_fmax', 0.05),
                                         relax_steps=getattr(args, 'relax_steps', 500))
        pol['apply_report'] = rep
        # ② 유한 최종힘·수렴 (rep) · ③ E·σ·P (rep.residual_stress) ·
        # ④ 등방 변형을 **제외한** 변위·배위 변화 — 스케일한 출발 프레임 vs 재완화 결과 (같은 셀)
        try:
            _cmp = compare_frames(_scaled, _new)
        except Exception as _e:                                  # noqa: BLE001
            _cmp = {'continuity': 'continuity_unknown', 'why_unknown': f'비교 실패: {_e}'}
        pol['succession_checks']['4_displacement_vs_scaled_start'] = _cmp
        pol['succession_checks']['⚠_순서'] = ('①대응·셀·부피 ②유한 최종힘·수렴 ③E·σ·P=−tr/3 '
                                              '④등방 제외 변위·배위 ⑤그 결과에 연결된 파일만 후속 후보 '
                                              '(회신 BQ-3 Q5-4). 낮은 압력은 힘 수렴을 대신하지 않는다')
        if not rep.get('converged'):
            # ⛔ 회신 BQ-2 P0-1 — 최종 V₀ 완화가 미수렴이면 그 구조도 자격이 없다.
            pol['eos_v0_applied'] = False
            pol['downstream_blocked'] = True
            pol['block_reason'] = '최종 V₀ 완화 미수렴'
            pol['⛔차단'] = ('최종 V₀ 완화가 **미수렴**이다 (|F|max=%.5f > 기준 %.5f eV/Å, '
                             'steps=%s). 승격과 후속 계산을 차단한다 (회신 BQ-2 P0-1).'
                             % (rep.get('final_fmax_eV_A', float('nan')),
                                rep.get('fmax_target_eV_A', float('nan')),
                                rep.get('n_steps')))
            pol['_diagnostic_atoms'] = _new
            return _orig, pol
        pol['eos_v0_applied'] = True
        pol['downstream_blocked'] = False
        atoms = _new
    elif not no_eos and not bool(getattr(args, 'no_elastic', False)):
        pol['⛔경고'] = (
            'EOS 가 낸 V₀ 를 **적용하지 않았다**. 아래 elastic 은 V₀ 가 아니라 '
            'post-anneal 부피에서 계산된 값이다 (GAP-3, cell_policy_gap_2026_09_13.json). '
            '두 양이 같은 구조를 가리킨다고 읽으면 틀린다. 적용하려면 --apply_eos_v0')
    return atoms, pol


def elastic_finite_strain(atoms_ref, calc, eps=0.005, fmax=0.05,
                          relax_steps=300):
    """6 independent Voigt strains × ±eps. Compute stress → Cij.
    Voigt-Reuss-Hill avg → B, G, E, ν, G/B.
    """
    # Strain matrices for ε₁..ε₆ (Voigt convention)
    voigt = [
        np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),  # ε₁ = εxx
        np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),  # ε₂ = εyy
        np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]]),  # ε₃ = εzz
        np.array([[0, 0, 0], [0, 0, 0.5], [0, 0.5, 0]]),  # ε₄ = εyz
        np.array([[0, 0, 0.5], [0, 0, 0], [0.5, 0, 0]]),  # ε₅ = εxz
        np.array([[0, 0.5, 0], [0.5, 0, 0], [0, 0, 0]]),  # ε₆ = εxy
    ]

    cell0 = atoms_ref.cell.array.copy()
    n = len(atoms_ref)
    Cij = np.zeros((6, 6))
    for i, strain in enumerate(voigt):
        stresses_pos_neg = []
        for sign in (+1, -1):
            atoms = atoms_ref.copy()
            F = np.eye(3) + sign * eps * strain
            atoms.set_cell(cell0 @ F, scale_atoms=True)
            atoms.calc = calc
            opt = FIRE(atoms, logfile=None)
            opt.run(fmax=fmax, steps=relax_steps)
            # Stress in Voigt order: [σxx, σyy, σzz, σyz, σxz, σxy] (ASE convention)
            stresses_pos_neg.append(atoms.get_stress(voigt=True))
        sigma_pos, sigma_neg = stresses_pos_neg
        # Central difference: ∂σ/∂ε
        dsigma_de = (sigma_pos - sigma_neg) / (2 * eps)
        Cij[:, i] = dsigma_de  # column i = ∂σⱼ/∂εᵢ

    # Symmetrize
    Cij = 0.5 * (Cij + Cij.T)
    # ASE stress is in eV/Å³; convert to GPa
    Cij_GPa = Cij * 160.21766208

    # Voigt-Reuss-Hill
    C = Cij_GPa
    Bv = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    Gv = ((C[0, 0] + C[1, 1] + C[2, 2]) - (C[0, 1] + C[0, 2] + C[1, 2])
          + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    try:
        S = np.linalg.inv(C)
        Br = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
        Gr = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2])
                  - 4 * (S[0, 1] + S[0, 2] + S[1, 2])
                  + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    except np.linalg.LinAlgError:
        Br = Gr = None

    Bh = (Bv + Br) / 2 if Br is not None else Bv
    Gh = (Gv + Gr) / 2 if Gr is not None else Gv
    if Bh and Gh:
        E_young = 9 * Bh * Gh / (3 * Bh + Gh)
        nu = (3 * Bh - 2 * Gh) / (2 * (3 * Bh + Gh))
        pugh = Gh / Bh
    else:
        E_young = nu = pugh = None

    return {
        'eps': eps,
        'Cij_GPa': Cij_GPa.tolist(),
        'B_voigt_GPa': float(Bv), 'B_reuss_GPa': float(Br) if Br else None,
        'B_hill_GPa': float(Bh),
        'G_voigt_GPa': float(Gv), 'G_reuss_GPa': float(Gr) if Gr else None,
        'G_hill_GPa': float(Gh),
        'E_young_GPa': float(E_young) if E_young else None,
        'poisson_nu': float(nu) if nu else None,
        'pugh_ratio_GoverB': float(pugh) if pugh else None,
    }


def winner_name(xyz_path):
    """NEW-D fix (v4.5.17): cascade outputs like
    04_anneal/{winner}/post_relax.xyz all share stem='post_relax',
    causing dict-key collision in collect_dataset. Use parent dir
    name in that case."""
    from pathlib import Path
    p = Path(xyz_path)
    if p.stem in ('post_relax', 'post_md'):
        return p.parent.name
    return p.stem


def _fmax_from_name(name):
    """조건 디렉터리 이름에서 fmax 를 되찾는다 (`..._f02` → 0.02, `_f005` → 0.005).

    ⚠ 이것은 **지어내는 것이 아니라 되찾는 것**이다 — 옛 기록이 fmax 목표값을
      저장하지 않아서(40ffa697) 실행 당시 이름에 박아둔 값을 읽는다.
      되찾지 못하면 None 을 주고, 호출부는 **수렴을 다시 세지 않는다.**
    """
    import re
    m = re.search(r'_f(\d+)(?:$|[_/])', str(name))
    if not m:
        return None
    try:
        return float('0.' + m.group(1))
    except ValueError:                                       # noqa: BLE001
        return None


def regate_eos(eos, fmax=None, hysteresis_tol=0.01, hysteresis_span_tol=0.10,
               hysteresis_shape_tol=0.10):
    """저장된 EOS 기록 하나에 **지금의 게이트**를 다시 매긴다.

    회신 BQ-2 지시: *"저장된 E(V)와 실제 수렴 기록으로 가능한 재적합·재판정은
    후처리로 하세요. 없는 좌표·수렴 기록은 사후에 있다고 간주하면 안 돼요."*

    왜 **다시 적합**하나 — 옛 기록은 게이트에 걸리면 `V0`/`B0_GPa`/`Bp` 를
    **None 으로 지운다**. 저장된 스칼라만으로는 재판정이 불가능하므로
    `V_points`/`E_points` 에서 `_fit_bm3` 로 다시 적합한다 (라이브와 같은 식).
    두 갈래 지표도 저장된 `E_up`/`E_down` 에서 **다시 계산**한다 — 옛 코드가
    계산한 파생값을 믿지 않고 원자료에서 다시 만든다.

    ⛔ 이 함수가 **못 하는 것**
      · **점별 구조를 복원하지 못한다** → 골짜기 이동 판정은 여전히 불가 (BQ-2 Q1·Q3).
      · 옵티마이저 반환값이 기록에 없어 **힘 기준만으로** 수렴을 다시 센다.
        `fmax` 를 못 받으면 아예 다시 세지 않고 옛 판정을 그대로 둔다.
      · 창이 다른 조건끼리 비교하지 않는다.
      · 없는 기록을 지어내지 않는다 — 수렴 기록이 없으면 자격을 **거부**한다.
    """
    V, E = eos.get('V_points'), eos.get('E_points')
    if not V or not E or len(V) != len(E) or len(V) < 4:
        return {'regate_skipped': ('V_points/E_points 가 없거나 점이 4개 미만 — '
                                   'BM3 4모수를 맞출 수 없다'),
                'stored': {'fit_quality_ok': eos.get('fit_quality_ok'),
                           'V0': eos.get('V0'), 'Bp': eos.get('Bp'),
                           'r2': eos.get('r2')}}
    V = np.asarray(V, dtype=float)
    out = {'V_points': V.tolist(), 'E_points': list(E),
           'fractions': eos.get('fractions'),
           'continuation': eos.get('continuation')}

    def _recount(rows):
        """힘 기준으로 수렴을 다시 센다. fmax 를 모르면 **손대지 않는다.**"""
        res = []
        for r in (rows or []):
            d = dict(r)
            _fm = d.get('final_fmax_eV_A')
            if fmax is not None and _fm is not None:
                d['converged'] = bool(float(_fm) <= float(fmax))
                d['fmax_target_eV_A'] = float(fmax)
                d['⚠_재판정'] = ('힘 기준만으로 다시 셌다 — 옵티마이저 반환값이 '
                                 '기록에 없다 (회신 BQ-2 Q1a)')
            res.append(d)
        return res

    _oh = eos.get('hysteresis') or {}
    if _oh.get('E_up') and _oh.get('E_down'):
        _up, _dn = np.asarray(_oh['E_up'], float), np.asarray(_oh['E_down'], float)
        _d = _up - _dn
        _sh = _d - _d.mean()
        hy = {'E_up': _up.tolist(), 'E_down': _dn.tolist(),
              'reported_branch': _oh.get('reported_branch', 'up'),
              'max_abs_dE_eV': float(np.abs(_d).max()),
              'level_offset_eV': float(_d.mean()),
              'shape_max_abs_dE_eV': float(np.abs(_sh).max()),
              'E_span_eV': float(max(_up.max() - _up.min(), _dn.max() - _dn.min())),
              'convergence_up': _recount(_oh.get('convergence_up')),
              'convergence_down': _recount(_oh.get('convergence_down'))}
        out['hysteresis'] = hy
    else:
        out['hysteresis'] = None
        out['convergence'] = _recount(eos.get('convergence'))

    try:
        E0, V0, B0, B0_GPa, Bp, r2 = _fit_bm3(V, out['E_points'])
    except Exception as e:                                   # noqa: BLE001
        out.update({'fit_quality_ok': False, 'V0': None, 'B0_GPa': None, 'Bp': None,
                    'r2': None,
                    'fit_quality_reason': f'재적합이 예외로 실패했다: {type(e).__name__}: {e}'})
        return attach_eligibility(out)
    gi = _fit_gate(r2, V0, B0_GPa, Bp, V)
    fit_ok, reason = gi['fit_quality_ok'], gi['fit_quality_reason']
    hy_ok, hy_reason = _hysteresis_gate(out['hysteresis'], V, hysteresis_tol,
                                        hysteresis_span_tol, hysteresis_shape_tol)
    if not hy_ok:
        fit_ok, reason = False, (hy_reason or reason)
    out.update({'gate_detail': gi, 'r2': r2, 'fit_quality_ok': fit_ok,
                'fit_quality_reason': ('OK' if fit_ok else reason),
                'V0': V0 if fit_ok else None,
                'E0': E0 if fit_ok else None,
                'B0_eV_per_A3': B0 if fit_ok else None,
                'B0_GPa': B0_GPa if fit_ok else None,
                'Bp': Bp if fit_ok else None,
                'V0_in_window': gi['V0_in_window'], 'B0_positive': gi['B0_positive'],
                # 게이트와 무관하게 **날값**을 같이 남긴다 (떨궈도 숫자는 보여야 한다)
                'raw_refit': {'V0': V0, 'B0_GPa': B0_GPa, 'Bp': Bp, 'r2': r2},
                'fmax_used_for_recount': fmax})
    attach_eligibility(out)
    out['stored'] = {'fit_quality_ok': eos.get('fit_quality_ok'), 'V0': eos.get('V0'),
                     'B0_GPa': eos.get('B0_GPa'), 'Bp': eos.get('Bp'),
                     'r2': eos.get('r2'),
                     'fit_quality_reason': eos.get('fit_quality_reason')}
    out['verdict_changed'] = bool(out['fit_quality_ok'] != eos.get('fit_quality_ok'))
    # ⛔ 회신 BQ-3 — verdict_changed 는 fit_quality_ok 만 본다. **자격**이 바뀌었는지는
    #   따로 세야 한다 (구버전 기록엔 자격 필드가 없으므로 None ≠ False 로 잡힌다).
    out['eligibility_changed'] = bool(out.get('downstream_eligible')
                                      != eos.get('downstream_eligible'))
    # ⛔ 판정이 그대로여도 **사유**가 바뀌면 그게 회신 BQ-2 Q2 의 실익이다:
    #   평행이동을 "곡선 자체가 갈린다" 로 적던 것이 "운영상 보류" 로 내려간다.
    #   판정만 보면 안 보이므로 따로 센다.
    out['reason_changed'] = bool((out.get('fit_quality_reason') or '')
                                 != (eos.get('fit_quality_reason') or ''))
    return out


def regate_paths(patterns, fmax=None, hysteresis_tol=0.01, hysteresis_span_tol=0.10,
                 hysteresis_shape_tol=0.10):
    """glob 들을 받아 `postproc.json` / `postproc_summary.json` 을 전부 재판정한다.

    ⛔ 못 하는 것: 파일을 고치지 않는다. **원본은 그대로 두고** 보고만 만든다
      (회신 BQ-2 Q4 의 원칙 — 원본 보존 + 정정 파생 기록).
    """
    import glob as _g
    files = []
    for pat in patterns:
        files.extend(sorted(_g.glob(pat)) if any(c in pat for c in '*?[') else [pat])
    rows = []
    for f in files:
        fp = Path(f)
        if fp.is_dir():
            files.extend(sorted(str(x) for x in fp.rglob('postproc*.json')))
            continue
        try:
            d = json.loads(fp.read_text())
        except Exception as e:                               # noqa: BLE001
            rows.append({'file': f, 'error': f'{type(e).__name__}: {e}'})
            continue
        recs = d['records'] if isinstance(d, dict) and isinstance(d.get('records'), list) else [d]
        _fm = fmax if fmax is not None else _fmax_from_name(f)
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            eos = rec.get('eos') or {}
            name = rec.get('name') or fp.parent.name
            seeds = eos.get('per_seed')
            targets = ([(f'{name}#seed{i}', s) for i, s in enumerate(seeds)]
                       if isinstance(seeds, list) and seeds and 'V_points' in (seeds[0] or {})
                       else [(name, eos)])
            for nm, e in targets:
                if not e:
                    continue
                r = regate_eos(e, fmax=_fm, hysteresis_tol=hysteresis_tol,
                               hysteresis_span_tol=hysteresis_span_tol,
                               hysteresis_shape_tol=hysteresis_shape_tol)
                r.update({'file': f, 'name': nm,
                          'fmax_source': ('explicit' if fmax is not None
                                          else ('dirname' if _fm is not None else 'unknown'))})
                rows.append(r)
    return rows


def print_regate(rows):
    """한 화면 요약. ⛔ **판정하지 않는다** — 옛 판정과 새 판정을 나란히 놓을 뿐이다."""
    print(f"\n{'구조':<16}{'옛':>4}{'새':>4}{'자격':>5}{'r2':>9}{'V0':>11}{'Bp':>7}  사유")
    print('─' * 108)
    nch = nrs = nel = 0
    for r in rows:
        if r.get('error') or r.get('regate_skipped'):
            print(f"{(r.get('name') or r.get('file') or '?')[:15]:<16}"
                  f"{'—':>4}{'—':>4}{'—':>5}{'':>9}{'':>11}{'':>7}  "
                  f"{r.get('error') or r.get('regate_skipped')}")
            continue
        _o = r['stored'].get('fit_quality_ok')
        _n = r.get('fit_quality_ok')
        _e = r.get('downstream_eligible')
        _raw = r.get('raw_refit') or {}
        nch += bool(r.get('verdict_changed'))
        nrs += bool(r.get('reason_changed'))
        nel += bool(r.get('eligibility_changed'))
        # ⛔ 2026-09-13 — 종전엔 `or 0.0` 라 **없는 값이 0.0 으로 찍혔다.** V₀ 가 None 인데
        #   화면에 0.0 이 뜨면 "부피 0" 으로 읽힌다. 없는 것은 '—' 다.
        def _n2(v, w, f):
            return ('—'.rjust(w) if v is None else format(float(v), f).rjust(w))
        print(f"{(r.get('name') or '?')[:15]:<16}"
              f"{('✅' if _o is True else '⛔'):>4}{('✅' if _n is True else '⛔'):>4}"
              f"{('✅' if _e is True else '⛔'):>5}"
              f"{_n2(_raw.get('r2'), 9, '.4f')}{_n2(_raw.get('V0'), 11, '.1f')}"
              f"{_n2(_raw.get('Bp'), 7, '.2f')}  {(r.get('fit_quality_reason') or '')[:44]}")
    print(f"\n  판정이 바뀐 줄: {nch}/{len(rows)} · **사유**가 바뀐 줄: {nrs}/{len(rows)} · "
          f"**자격**이 바뀐 줄: {nel}/{len(rows)}")
    print("  · 판정(fit_quality_ok)과 자격(downstream_eligible)은 다른 것이다 — 따로 센다 (회신 BQ-3)")
    print("  · 판정이 그대로여도 사유가 바뀌면 의미가 있다 — 평행이동을 '곡선 자체가")
    print("    갈린다' 로 적던 것이 '운영상 보류' 로 내려간다 (회신 BQ-2 Q2)")
    print("  · '옛' 은 파일에 저장된 판정, '새' 는 지금 게이트. '자격' 은 후속 사용 가능 여부다")
    print("  · r2·V0·Bp 는 **게이트와 무관한 날값**(재적합 결과)이다 — 떨궈도 숫자는 보인다")
    print("  ⛔ 이 표는 파일을 고치지 않는다. 그리고 **점별 구조가 없어** 골짜기 이동은")
    print("     여전히 판정할 수 없다 (회신 BQ-2 Q1·Q3)")


def audit_pressure_sign(patterns, out_path=None):
    """저장된 기록의 압력 부호를 **증거로** 판정하고 정정 파생 기록을 만든다.

    회신 BQ-2 Q4 — *"원본은 보존하고, 정정된 파생 기록을 추가하는 쪽에 찬성이에요.
    원본 파일·생성 버전·필드와 연결해서 올바른 압력을 제공하고, 이후 표와 판정은
    정정본을 읽게 하세요. '당시 규약' 이라는 주석만 붙인 채 잘못된 P_mean_GPa 를
    계속 사용하면 부족해요."*

    ⛔⛔ **일괄 반전하지 않는다.** 저장된 σ 텐서로 −tr(σ)/3 을 직접 계산해
      저장값과 맞춰본다 — 추측이 아니라 산술로 판정한다:
        · P == −tr/3 → `already_correct`  손대지 않는다
        · P == +tr/3 → `corrected`        이 버그의 산물이다
        · 둘 다 아님  → `unknown`          **표시만** 하고 손대지 않는다
      (리뷰어: *"이 버그가 있던 생성 경로만 정정해야 하며, 다른 도구가 만든
       압력을 일괄 반전하면 안 돼요."*)

    ⛔ **편차응력은 그대로다** — σ − (trσ/3)I 는 부호를 뒤집지 않는다.

    ⛔ 이 함수가 **못 하는 것**
      · 원본 파일을 고치지 않는다. 파생 기록만 만든다.
      · σ 가 없으면 판정하지 않는다 (`no_sigma`). 부호를 짐작하지 않는다.
      · 압력이 물리적으로 맞는지 말하지 않는다. **규약 부호**만 본다.
    """
    import glob as _g
    import hashlib

    def _walk(node, path=''):
        """σ 와 P 를 함께 든 dict 를 재귀로 찾는다."""
        if isinstance(node, dict):
            if 'P_mean_GPa' in node:
                yield path, node
            for k, v in node.items():
                yield from _walk(v, f'{path}.{k}' if path else str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from _walk(v, f'{path}[{i}]')

    files = []
    for pat in patterns:
        files.extend(sorted(_g.glob(pat)) if any(c in pat for c in '*?[') else [pat])
    rows = []
    for f in list(files):
        fp = Path(f)
        if fp.is_dir():
            files.extend(sorted(str(x) for x in fp.rglob('*.json')))
            continue
        try:
            raw = fp.read_bytes()
            d = json.loads(raw)
        except Exception as e:                               # noqa: BLE001
            rows.append({'file': f, 'error': f'{type(e).__name__}: {e}'})
            continue
        _sha = hashlib.sha256(raw).hexdigest()
        for path, node in _walk(d):
            stored = node.get('P_mean_GPa')
            sig = node.get('sigma_GPa')
            row = {'file': f, 'source_sha256': _sha, 'field_path': path,
                   'stored_P_mean_GPa': stored,
                   'has_sign_note': bool('⚠_부호' in node),
                   'deviatoric_max_abs_GPa': node.get('deviatoric_max_abs_GPa'),
                   '⚠_편차응력': '편차는 부호를 뒤집지 않는다 — 그대로 쓴다'}
            if sig is None or stored is None:
                row.update({'verdict': 'no_sigma',
                            'why': 'σ 텐서나 P 가 없어 산술로 판정할 수 없다 — 짐작하지 않는다'})
                rows.append(row)
                continue
            try:
                tr3 = float(np.trace(np.asarray(sig, dtype=float)) / 3.0)
            except Exception as e:                           # noqa: BLE001
                row.update({'verdict': 'unknown', 'why': f'σ 를 못 읽었다: {e}'})
                rows.append(row)
                continue
            row['trace_over_3_GPa'] = tr3
            tol = max(1e-6, abs(tr3) * 1e-6)
            if abs(float(stored) - (-tr3)) <= tol:
                row.update({'verdict': 'already_correct',
                            'corrected_P_mean_GPa': float(stored),
                            'why': 'P = −tr(σ)/3 이 이미 맞다'})
            elif abs(float(stored) - tr3) <= tol:
                row.update({'verdict': 'corrected',
                            'corrected_P_mean_GPa': -tr3,
                            'why': ('저장값이 +tr(σ)/3 이다 — 2026-09-13 이전 '
                                    '`stress_report` 의 부호 버그가 만든 값이다')})
            else:
                row.update({'verdict': 'unknown', 'corrected_P_mean_GPa': None,
                            'why': ('저장값이 ±tr(σ)/3 어느 쪽도 아니다 — 다른 도구가 '
                                    '만들었거나 다른 정의다. **손대지 않는다**')})
            rows.append(row)
    rec = {'schema': 1, 'kind': 'pressure_sign_correction', 'date': '2026-09-13',
           '왜_이_기록이_있나': ('회신 BQ-2 Q4 — 원본을 보존하고 정정된 파생 기록을 '
                                '원본 파일·해시·필드 경로와 **연결해서** 추가한다. '
                                '이후 표와 판정은 이 정정본을 읽는다'),
           '판정_방법': ('저장된 σ 로 −tr(σ)/3 을 계산해 저장값과 산술 대조한다. '
                         '일괄 반전이 아니다 — verdict 가 corrected 인 줄만 정정된다'),
           '⛔_편차응력': 'σ − (trσ/3)I 는 부호를 뒤집지 않는다. 편차는 그대로다',
           'counts': {k: sum(1 for r in rows if r.get('verdict') == k)
                      for k in ('already_correct', 'corrected', 'unknown', 'no_sigma')},
           'rows': rows}
    if out_path:
        Path(out_path).write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    return rec


def process_one(xyz_path, calc, out_dir, args):
    name = winner_name(xyz_path)
    work = out_dir / name
    # ⛔⛔ 회신 BQ-3 P0-3 잔여 — 같은 폴더에서 성공 → 실패 순으로 돌리면 이전
    #   final_v0_applied.xyz 가 **동일 바이트로 남는다**. 이번 호출의 탄성은 막혀도, 파일을
    #   직접 집어가는 다음 작업이 옛 파일을 받는다. ⇒ **기존 결과 폴더 재사용 거부.**
    #   (재개 로직은 done 목록으로 이 함수를 아예 안 부르므로 충돌하지 않는다.)
    _prior = ([str(x.name) for x in work.glob('*') if x.is_file()
               and (x.name == 'postproc.json' or x.name.startswith('final_')
                    or x.name.startswith('DIAGNOSTIC_'))] if work.exists() else [])
    if _prior:
        raise RuntimeError(
            f"⛔ 결과 폴더 재사용 거부: {work} 에 이전 결과가 있다 {_prior}. "
            f"새 --out 을 써라. 이전 결과는 지우지 않는다 (회신 BQ-3 P0-3).")
    work.mkdir(parents=True, exist_ok=True)
    import secrets as _sec
    _run_id = time.strftime('%Y%m%dT%H%M%S') + '-' + _sec.token_hex(3)
    try:
        _code = (get_provenance() or {}).get('git_commit')
    except Exception:                                        # noqa: BLE001
        _code = None
    _meta = {'structure': name, 'run_id': _run_id, 'run_tag': getattr(args, 'run_tag', '') or '',
             'code_id': str(_code), 'model': 'uma-s-1p1',
             'inference_mode': str(getattr(args, 'uma_mode', None)),
             'relax_steps': int(getattr(args, 'relax_steps', 0))}

    atoms = read(str(xyz_path))
    atoms.calc = calc
    record = {'name': name, 'xyz_input': str(xyz_path), 'run_id': _run_id,
              'run_tag': _meta['run_tag'], 'code_id': _meta['code_id'],
              'n_atoms': len(atoms),
              'composition': {el: int(c) for el, c in
                              zip(*np.unique(atoms.get_chemical_symbols(),
                                            return_counts=True))}}

    # 0. Refresh relax to ensure starting at minimum
    #    ⚠ 기본은 형상 무제한 CellFilter — **DFT 쪽 고정셀 규율이 여기 걸려 있지 않다**
    #      (GAP-1·2). --fixed_shape_relax 로 고정셀 경로를 고를 수 있다.
    _target = atoms if getattr(args, 'fixed_shape_relax', False) else CellFilter(atoms)
    opt = FIRE(_target, logfile=None)
    opt.run(fmax=0.05, steps=500)
    record['E_pre_anneal_per_atom'] = atoms.get_potential_energy() / len(atoms)

    # 1. Anneal (optional)
    if not args.no_anneal:
        atoms, log = light_anneal(atoms, T=args.anneal_T,
                                 time_ps=args.anneal_ps,
                                 relax_steps=args.relax_steps)
        record['anneal'] = log
    record['E_post_anneal_per_atom'] = atoms.get_potential_energy() / len(atoms)
    # ⛔ 회신 BQ P0-3 — 이 파일은 **V₀ 적용 전** 구조다. 이름이 그 사실을 말하게 한다.
    #   (종전 이름 `post_anneal.xyz` 는 하류가 "최종 구조" 로 집어가기 쉬웠다.
    #    MD 에 넘길 구조는 아래 `final_v0_applied.xyz` 다.)
    write(work / 'stage1_before_eos.xyz', atoms)

    # 2. EOS (optionally an ensemble of N rattled seeds, best BM3 fit kept)
    if not args.no_eos:
        t0 = time.time()
        if args.n_eos_seeds > 1:
            record['eos'] = eos_ensemble(atoms, calc,
                                         n_seeds=args.n_eos_seeds,
                                         perturb=args.eos_perturb,
                                         fractions=tuple(args.eos_fractions),
                                         fmax=args.eos_fmax,
                                         relax_steps=args.relax_steps,
                                         continuation=getattr(args, 'eos_continuation', False),
                                         hysteresis_tol=getattr(args, 'eos_hysteresis_tol', 0.01),
                                         hysteresis_span_tol=getattr(args, 'eos_hysteresis_span_tol', 0.10),
                                         hysteresis_shape_tol=getattr(args, 'eos_hysteresis_shape_tol', 0.10))
        else:
            record['eos'] = eos_sweep(atoms, calc,
                                      fractions=tuple(args.eos_fractions),
                                      fmax=args.eos_fmax,
                                      relax_steps=args.relax_steps,
                                      continuation=getattr(args, 'eos_continuation', False),
                                      hysteresis_tol=getattr(args, 'eos_hysteresis_tol', 0.01),
                                      hysteresis_span_tol=getattr(args, 'eos_hysteresis_span_tol', 0.10),
                                      hysteresis_shape_tol=getattr(args, 'eos_hysteresis_shape_tol', 0.10),
                                      # 회신 BQ-3 Q5-2 — 점별 프레임을 여기 남긴다 (미수렴점 포함)
                                      save_dir=(work / 'eos_frames'), meta=_meta)
        record['eos']['t_s'] = time.time() - t0

    # 2b. EOS V₀ 를 **실제로** 적용한다 (GAP-3). 기본은 과거 동작 유지.
    atoms, record['cell_policy'] = maybe_apply_eos_v0(atoms, record, args, calc)
    # ⛔ 회신 BQ P0-3 — Atoms 는 직렬화 불가. **V₀ 적용에 쓴 뒤** 기록에서 뺀다.
    (record.get('eos') or {}).pop('_branch_atoms', None)
    (record.get('eos') or {}).pop('_branch_frames', None)    # Atoms 목록 — 직렬화 불가
    _pol = record.get('cell_policy') or {}
    _diag = _pol.pop('_diagnostic_atoms', None)
    _blocked = bool(_pol.get('downstream_blocked'))
    _applied = bool(_pol.get('eos_v0_applied'))
    # ⛔⛔ 회신 BQ-2 P0-3 (2026-09-13) — **이름이 곧 주장이다.**
    #   실패·차단된 구조에 `final_v0_applied` 와 ✅ 를 붙이면 하류가 그것을 믿는다.
    #   차단되면 최종 파일을 **만들지 않고** 진단본만 남긴다.
    _written = {'stage1_before_eos.xyz': '⚠ EOS·V₀ 적용 **전** 구조. 하류가 집어가면 안 된다'}
    if _blocked:
        if _diag is not None:
            write(work / 'DIAGNOSTIC_blocked_not_for_downstream.xyz', _diag)
            _written['DIAGNOSTIC_blocked_not_for_downstream.xyz'] = (
                '⛔ 진단 전용. 차단된 경로의 구조다 — MD·탄성·하류 입력으로 쓰지 않는다 (%s)'
                % _pol.get('block_reason', '?'))
        _written['⛔_최종_구조_없음'] = (
            '셀 정책이 차단됐으므로 하류가 집어갈 최종 구조를 **만들지 않았다** (%s)'
            % _pol.get('block_reason', '?'))
        _downstream_file = None
    else:
        _name = 'final_v0_applied.xyz' if _applied else 'final_no_v0_applied.xyz'
        write(work / _name, atoms)
        # ⛔ 회신 BQ-3 P0-3 — 후속 입력은 **이 실행의 자격 기록에 연결된 파일만** 읽는다.
        #   파일 해시와 run_id 를 기록에 박아 둔다. 해시가 다르면 이 기록의 파일이 아니다.
        import hashlib as _hl
        _written['final_sha256'] = _hl.sha256((work / _name).read_bytes()).hexdigest()
        _written['run_id'] = _run_id
        _written[_name] = ('✅ V₀ 가 실제로 적용되고 **수렴한** 최종 구조 — 탄성이 쓴 것'
                           if _applied else
                           '⚠ V₀ 를 적용하지 **않은** 구조(요청 안 함). post-anneal 부피다 — '
                           'V₀ 에서의 값이라고 읽으면 틀린다 (GAP-3)')
        _downstream_file = _name
    _written['eos_v0_applied'] = _applied
    _written['downstream_blocked'] = _blocked
    _written['downstream_input'] = _downstream_file
    record['structures_written'] = _written

    # 3. Elastic
    if _blocked:
        record['elastic'] = {
            'skipped': True,
            '⛔_이유': ('셀 정책이 차단돼 기준 구조가 없다 — 탄성을 계산하지 않는다. '
                       '사유: %s (회신 BQ-2 P0-1·P0-3)' % _pol.get('block_reason', '?'))}
    elif not args.no_elastic:
        t0 = time.time()
        try:
            record['cell_policy']['stress_at_elastic_ref'] = stress_report(atoms)
        except Exception as _e:
            record['cell_policy']['stress_at_elastic_ref'] = {'error': str(_e)}
        record['elastic'] = elastic_finite_strain(atoms, calc,
                                                  eps=args.elastic_eps,
                                                  fmax=args.elastic_fmax,
                                                  relax_steps=args.relax_steps)
        record['elastic']['t_s'] = time.time() - t0

    (work / 'postproc.json').write_text(json.dumps(record, indent=2, default=str))
    return record


def _selftest():
    """셀 정책 로직 검사 — UMA 없이 ASE EMT 로. **음성 경로 포함** (카드 v4 §4b).

    이 selftest 가 보는 것은 '갈림길이 제대로 갈리는가' 뿐이다.
    ⛔ 물리를 검증하지 않는다. EMT 는 Cu 용 장난감 퍼텐셜이다.
    """
    import numpy as _np
    from ase.build import bulk
    from ase.calculators.emt import EMT

    ok = fail = 0
    def chk(cond, label):
        nonlocal ok, fail
        if cond: ok += 1
        else: fail += 1; print(f"  ⛔ {label}")

    class A:                      # 가짜 args
        def __init__(self, **kw):
            self.apply_eos_v0 = False; self.fixed_shape_relax = False
            self.no_eos = False; self.no_elastic = False
            self.eos_fmax = 0.05; self.relax_steps = 50
            self.__dict__.update(kw)

    at = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2)
    at.calc = EMT()
    V_post = at.get_volume()
    V0 = V_post * 1.08                      # post-anneal 과 **다른** V₀

    # ① 적용: 부피가 V₀ 가 되고 각도·길이비가 보존된다
    a2, rep = apply_v0_fixed_shape(at, V0, EMT(), fmax=0.05, relax_steps=50)
    chk(rep['applied'] and abs(a2.get_volume() - V0) / V0 < 1e-9,
        "V₀ 적용 후 부피 = V₀")
    ang0, ang2 = at.cell.angles(), a2.cell.angles()
    l0, l2 = at.cell.lengths(), a2.cell.lengths()
    chk(_np.allclose(ang0, ang2, atol=1e-9), "각도 보존")
    chk(_np.allclose(l0 / l0[0], l2 / l2[0], atol=1e-9), "길이비 보존 (등방 스케일)")

    # ② ⛔음성: V₀ 가 None 이면 적용하지 않고 구조를 그대로 돌려준다
    a3, rep3 = apply_v0_fixed_shape(at, None, EMT())
    chk((not rep3['applied']) and abs(a3.get_volume() - V_post) < 1e-12,
        "⛔음성: V₀=None → 미적용 + 구조 불변")

    # ③ ★ 갈림길 — 같은 record 로 두 갈래가 **다른 부피**를 탄성에 넘긴다
    #   ⛔⛔ 2026-09-13 회신 BQ-2 P0-3 — 이 시험도 **옛 동작을 방어하고 있었다.**
    #     fixture 가 `{'eos': {'V0': V0}}` 뿐이라 수렴 근거도 가지 구조도 없는데
    #     승격을 기대했다. 이제 자격을 갖춘 record 라야 통과한다.
    def _mk_eos(v0, vol_branch=None, eligible=True, rattle=0.0):
        """자격을 갖춘(또는 일부러 못 갖춘) EOS 기록 하나를 만든다.

        ⚠ `rattle` 이 필요한 이유: 완화는 **가지 구조**(`_branch_atoms`)에서 출발한다.
          완벽한 Cu 결정은 대칭 때문에 힘이 정확히 0 이라, 굶겨도 '수렴' 이 된다.
        """
        _b = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2)
        if vol_branch is not None:
            _b.set_cell(_b.cell.array * (vol_branch / _b.get_volume()) ** (1 / 3),
                        scale_atoms=True)
        if rattle:
            _b.rattle(stdev=rattle, seed=7)
        _b.calc = EMT()
        return {'V0': v0, '_branch_atoms': _b,
                'downstream_eligible': bool(eligible),
                'downstream_block_reason': (None if eligible else '시험용 미달'),
                'fit_quality_ok': bool(eligible)}

    rec = {'eos': _mk_eos(V0)}
    at_on = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2); at_on.calc = EMT()
    a_on, pol_on = maybe_apply_eos_v0(at_on, rec, A(apply_eos_v0=True), EMT())
    at_off = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2); at_off.calc = EMT()
    a_off, pol_off = maybe_apply_eos_v0(at_off, {'eos': _mk_eos(V0)},
                                        A(apply_eos_v0=False), EMT())
    chk(pol_on['eos_v0_applied'] and abs(a_on.get_volume() - V0) / V0 < 1e-9,
        "갈림길 ON: 탄성이 V₀ 를 받는다 (자격을 갖춘 record)")
    chk((not pol_off['eos_v0_applied']) and abs(a_off.get_volume() - V_post) < 1e-9,
        "⛔음성: 갈림길 OFF → 탄성이 **post-anneal 부피**를 받는다 (= GAP-3 의 실제 모습)")
    chk(abs(a_on.get_volume() - a_off.get_volume()) > 1e-6,
        "⛔음성: 두 갈래가 실제로 **다른 구조**를 넘긴다 (같으면 이 시험은 아무것도 안 본 것이다)")

    # ③-b ⛔⛔음성 — **리뷰어가 재현한 회귀 그 자체** (회신 BQ-2 P0-3)
    #   적합이 실패(V0=None)했는데 가지 구조(실패 EOS 의 마지막 팽창점)가 있으면
    #   종전에는 그 팽창점이 최종 구조로 승격됐다: 원본 100 → 106.
    _at_f = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2); _at_f.calc = EMT()
    _v_orig = _at_f.get_volume()
    _rec_f = {'eos': _mk_eos(None, vol_branch=_v_orig * 1.06)}
    _a_f, _pol_f = maybe_apply_eos_v0(_at_f, _rec_f, A(apply_eos_v0=True), EMT())
    chk(abs(_a_f.get_volume() - _v_orig) < 1e-9,
        "⛔⛔음성: 적합 실패 시 **마지막 팽창점이 승격되지 않는다** (원본 부피 그대로)")
    chk(_pol_f.get('downstream_blocked') is True and '⛔차단' in _pol_f,
        "⛔음성: 차단 사실이 기록에 박힌다 (조용히 원본으로 되돌아가지 않는다)")
    chk(_pol_f.get('eos_v0_applied') is False,
        "⛔음성: 차단이면 eos_v0_applied 는 거짓")
    chk(_pol_f.get('_diagnostic_atoms') is not None,
        "차단해도 진단 구조는 남긴다 (버리지 않는다)")

    # ③-c ⛔음성 — 자격 미달(수렴 근거 없음)이면 V₀ 가 있어도 차단한다
    _at_e = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2); _at_e.calc = EMT()
    _a_e, _pol_e = maybe_apply_eos_v0(_at_e, {'eos': _mk_eos(V0, eligible=False)},
                                      A(apply_eos_v0=True), EMT())
    chk(_pol_e.get('downstream_blocked') is True
        and abs(_a_e.get_volume() - _at_e.get_volume()) < 1e-9,
        "⛔음성: V₀ 가 있어도 **자격 미달이면 차단** (fit_quality_ok 만으로 안 된다)")

    # ③-d ⛔음성 — 자격 필드가 **아예 없는** 구버전 기록도 차단한다 (모르는 것 ≠ 통과)
    _at_o = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2); _at_o.calc = EMT()
    _a_o, _pol_o = maybe_apply_eos_v0(_at_o, {'eos': {'V0': V0}},
                                      A(apply_eos_v0=True), EMT())
    chk(_pol_o.get('downstream_blocked') is True,
        "⛔음성: 자격 필드 없는 구버전 기록 → 차단 (모르는 것은 통과가 아니다)")

    # ③-e ⛔음성 — **최종 V₀ 완화가 미수렴**이면 차단한다 (회신 BQ-2 P0-1)
    _at_u = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2); _at_u.calc = EMT()
    _v_u = _at_u.get_volume()
    # 완화는 **가지 구조**에서 출발하므로 그쪽을 흔든다 (완벽 결정은 힘이 0 이다)
    _a_u, _pol_u = maybe_apply_eos_v0(_at_u, {'eos': _mk_eos(V0, rattle=0.08)},
                                      A(apply_eos_v0=True, eos_fmax=1e-9, relax_steps=1),
                                      EMT())
    chk(_pol_u.get('downstream_blocked') is True
        and '미수렴' in (_pol_u.get('block_reason') or ''),
        "⛔음성: 최종 V₀ 완화가 미수렴이면 차단 (굶기면 잡힌다)")
    chk(abs(_a_u.get_volume() - _v_u) < 1e-9,
        "⛔음성: 미수렴 차단 시 구조도 원본으로 되돌린다")

    # ④ 적용 안 했으면 **경고가 박힌다** — 조용히 지나가지 않는가
    chk('⛔경고' in pol_off and 'GAP-3' in pol_off['⛔경고'],
        "⛔음성: 미적용 시 record 에 경고 문자열")
    chk('⛔경고' not in pol_on, "적용했으면 경고 없음")

    # ⑤ no_eos 면 경고도 안 단다 (EOS 를 안 돌렸으니 V₀ 자체가 없다)
    _, pol_noeos = maybe_apply_eos_v0(at, {}, A(no_eos=True), EMT())
    chk('⛔경고' not in pol_noeos, "no_eos → 경고 없음 (V₀ 가 애초에 없다)")

    # ⑥ 응력 보고: 평균압과 편차가 **따로** 나오고 산술이 맞는다
    #   ⛔ 2026-09-13 회신 BQ P1 — 이 시험이 **틀린 규약을 굳히고 있었다.**
    #     `chk(P_mean == trace/3)` 이었는데, ASE 는 **인장 양수** 규약이라
    #     압력은 `−trace/3` 이다. 시험이 버그를 지켰다.
    sr = stress_report(at)
    sig = _np.array(sr['sigma_GPa'])
    chk(abs(sr['P_mean_GPa'] + _np.trace(sig) / 3) < 1e-9, "P_mean = **−**trace/3 (압축 양수)")
    dev = sig - (_np.trace(sig) / 3) * _np.eye(3)      # 편차는 정의대로 trace/3 을 뺀다
    chk(abs(sr['deviatoric_max_abs_GPa'] - _np.abs(dev).max()) < 1e-9,
        "편차 최대성분 — 편차는 부호를 **안 뒤집는다** (정의가 σ − (trσ/3)I 다)")
    chk('영응력 판정 아님' in sr['⚠'], "응력 보고에 '영응력 판정 아님' 이 박혀 있다")

    # ⛔음성: **압축한 셀의 압력이 양수인가** — 규약이 뒤집히면 여기서 잡힌다
    _sq = bulk('Cu', 'fcc', a=3.59, cubic=True) * (2, 2, 2)
    _sq.set_cell(_sq.cell.array * 0.95 ** (1 / 3), scale_atoms=True)
    _sq.calc = EMT()
    _sr = stress_report(_sq)
    chk(_sr['P_mean_GPa'] > 0,
        "⛔음성: **압축한 셀의 압력이 양수**다 (부호가 뒤집히면 음수가 나온다)")
    chk(_sr['trace_over_3_GPa'] < 0,
        "⛔음성: 같은 셀에서 trace/3 은 **음수**다 (ASE 인장 양수 규약을 그대로 남긴다)")
    _ex = bulk('Cu', 'fcc', a=3.59, cubic=True) * (2, 2, 2)
    _ex.set_cell(_ex.cell.array * 1.05 ** (1 / 3), scale_atoms=True)
    _ex.calc = EMT()
    chk(stress_report(_ex)['P_mean_GPa'] < 0,
        "⛔음성: **팽창한 셀은 음압**이다 (부호가 방향을 실제로 따라간다)")

    # ⑦ ⛔음성: step0 정책이 기록에 남는가 (두 값이 달라야 한다)
    chk(maybe_apply_eos_v0(at, {}, A(no_eos=True), EMT())[1]['step0_relax'] !=
        maybe_apply_eos_v0(at, {}, A(no_eos=True, fixed_shape_relax=True), EMT())[1]['step0_relax'],
        "⛔음성: step0 정책 두 갈래가 기록에서 구분된다")

    # ⑧ ensemble 요약이 **선택을 숨기지 않는가** (2026-09-13 실측 사고)
    #   P2_Al2S3_B 시드 3개에서 r² 0.79/0.998/0.90 → 2개 실패, 그런데 std 가 0.0 이었다.
    #   0.0 은 "시드 간 완벽 일치" 로 읽힌다 — 정반대 뜻이다.
    def _fake_ens(rs):
        """eos_ensemble 의 요약 계산만 떼어 검증한다 (UMA 없이)."""
        physical = [r for r in rs if r.get('fit_quality_ok') and r.get('B0_GPa') is not None
                    and r.get('Bp') is not None and 0.0 < r['Bp'] < 15.0]
        b0s = [r['B0_GPa'] for r in rs if r.get('B0_GPa') is not None]
        _nfit = int(sum(1 for r in rs if r.get('fit_quality_ok')))
        _std = float(_np.std(b0s)) if len(b0s) >= 2 else None
        return {'n_B0': len(b0s), 'B0_GPa_std': _std, 'n_fit_ok': _nfit,
                '⚠_std_가_None_인_이유': (None if _std is not None else 'x'),
                '⛔_선택_경고': (None if _nfit == len(rs) else 'y')}

    _one = _fake_ens([{'fit_quality_ok': True, 'B0_GPa': 19.0, 'Bp': 1.3},
                      {'fit_quality_ok': False}, {'fit_quality_ok': False}])
    chk(_one['B0_GPa_std'] is None and _one['n_B0'] == 1,
        "⛔음성: B0 가 1개뿐이면 std 는 **None** 이다 (0.0 이 아니다 — 0.0 은 일치를 뜻한다)")
    chk(_one['⚠_std_가_None_인_이유'] is not None,
        "⛔음성: std 가 None 인 **이유**가 기록에 남는다 (빈칸으로 두지 않는다)")
    chk(_one['⛔_선택_경고'] is not None,
        "⛔음성: 시드가 하나라도 실패하면 '골라낸 값' 경고가 뜬다")

    _all = _fake_ens([{'fit_quality_ok': True, 'B0_GPa': 19.0, 'Bp': 4.0},
                      {'fit_quality_ok': True, 'B0_GPa': 20.0, 'Bp': 4.1},
                      {'fit_quality_ok': True, 'B0_GPa': 21.0, 'Bp': 3.9}])
    chk(_all['B0_GPa_std'] is not None and _all['B0_GPa_std'] > 0,
        "양성: 시드 3개가 다 통과하면 std 가 **실제 산포**를 낸다")
    chk(_all['⛔_선택_경고'] is None and _all['⚠_std_가_None_인_이유'] is None,
        "양성: 전원 통과면 경고가 **안 뜬다** (무조건 경고하는 게 아니다)")

    # ⑨ ⛔음성: fit_quality_ok 가 JSON 에서 **진짜 불리언**이어야 한다
    #   `json.dumps(..., default=str)` 이 np.bool_ 을 "False" 문자열로 만들면
    #   하류의 `if rec['fit_quality_ok']:` 가 **거짓을 참으로** 읽는다.
    _r2, _V0, _Bp = _np.float64(0.5), _np.float64(100.0), _np.float64(-3.0)
    _fit_ok = bool(_r2 >= 0.95 and 0 < _V0 < 500 and 0.0 < _Bp < 15.0)
    chk(type(_fit_ok) is bool, "⛔음성: fit_ok 가 np.bool_ 이 아니라 파이썬 bool 이다")
    _round = json.loads(json.dumps({'fit_quality_ok': _fit_ok}, default=str))
    chk(_round['fit_quality_ok'] is False,
        "⛔음성: JSON 왕복 뒤에도 False 다 (문자열 \"False\" 가 되면 하류가 참으로 읽는다)")

    # ⑩ 연쇄(continuation) EOS — 카드 v4 §4b 후속 (2026-09-13)
    #   ⛔ EMT/Cu 는 질서 있는 금속이라 **물리를 검증하지 않는다.** 여기서 보는 것은
    #     '갈림길이 갈리는가'·'이력현상 게이트가 실제로 무는가' 뿐이다.
    _cu = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2)
    _fr = (0.96, 0.98, 1.00, 1.02, 1.04)

    _off = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                     continuation=False)
    chk(_off.get('continuation') is False and _off.get('hysteresis') is None,
        "연쇄 꺼짐이 기본 — hysteresis 가 None 이다 (옛 동작 보존)")

    _on = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                    continuation=True, hysteresis_tol=0.01)
    _h = _on.get('hysteresis') or {}
    chk(_on.get('continuation') is True and _h,
        "연쇄 켜짐 — hysteresis 기록이 생긴다")
    chk(all(k in _h for k in ('E_up', 'E_down', 'V0_up', 'V0_down',
                              'V0_rel_diff', 'ok', 'max_abs_dE_eV')),
        "이력현상 기록에 두 갈래 E·V₀·상대차·판정이 **전부** 있다")
    chk(len(_h['E_up']) == len(_fr) and len(_h['E_down']) == len(_fr),
        "두 갈래가 같은 부피점 수를 갖는다 (내림 갈래를 오름차순으로 되돌린다)")
    chk(_h.get('ok') is True and _on.get('fit_quality_ok') is True,
        "양성: 질서 있는 Cu 는 두 갈래가 일치하고 적합이 통과한다")

    # ⛔음성 ①: 허용오차를 0 으로 두면 **같은 자료**가 떨어져야 한다
    #   (자료가 아니라 **게이트**가 판정을 만든다는 증거 — 통과가 우연이 아님을 보인다)
    _zero = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                      continuation=True, hysteresis_tol=0.0)
    chk(_zero.get('fit_quality_ok') is False
        and (_zero.get('hysteresis') or {}).get('ok') is False,
        "⛔음성: tol=0 이면 같은 자료도 떨어진다 — 게이트가 실제로 판정을 만든다")
    chk('이력현상' in (_zero.get('fit_quality_reason') or ''),
        "⛔음성: 떨어진 **이유**가 이력현상이라고 적힌다 (r² 탓으로 가리지 않는다)")
    chk(_zero.get('V0') is None and _zero.get('B0_GPa') is None,
        "⛔음성: 떨어지면 V₀·B₀ 를 **None 으로 지운다** (하류가 집어가지 못하게)")

    # ⛔음성 ①-b: **V₀ 만 보는 게이트의 구멍** — 곡선이 갈려도 최소 위치는 겹칠 수 있다
    #   실측 2026-09-13: P2_Al2S3_A 가 maxdE/span 95 % 인데 V₀ 차 0.949 % 로 통과했다.
    #   span 기준을 0 으로 조이면 **V₀ 기준은 널널해도** 떨어져야 한다.
    _hole = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                      continuation=True, hysteresis_tol=1.0,   # V₀ 는 사실상 무제한
                      hysteresis_span_tol=0.0, hysteresis_shape_tol=0.0)   # 곡선 기준만 조인다
    chk(_hole.get('fit_quality_ok') is False,
        "⛔음성: V₀ 기준을 풀어도 **곡선 기준**만으로 떨어진다 (구멍이 막혔다)")
    chk('모양이 갈린다' in (_hole.get('fit_quality_reason') or ''),
        "⛔음성: 떨어진 이유가 **모양이 갈렸다**고 적힌다 (V₀ 탓으로 안 돌린다)")

    # ⛔⛔ 회신 BQ-2 Q2 — **리뷰어가 재현한 거짓 양성 그 자체.**
    #   두 갈래가 정확히 평행이동(모양차 0)이면 V₀·곡률은 같다. 종전 게이트는
    #   원시 max_abs_dE/span 만 보고 "EOS 가 한 골짜기로 정의되지 않는다" 로 떨어뜨렸다.
    #   이제는 **운영상 보류**로 내려가고, 사유가 평행이동임을 밝혀야 한다.
    _V = np.array([100.0, 105.0, 110.0, 115.0, 120.0, 125.0, 130.0])
    _Ebase = 0.02 * (_V - 115.0) ** 2 / 100.0
    _hy = {'E_up': _Ebase.tolist(), 'E_down': (_Ebase + 0.04).tolist(),
           'reported_branch': 'up', 'max_abs_dE_eV': 0.04,
           'level_offset_eV': -0.04, 'shape_max_abs_dE_eV': 0.0,
           'E_span_eV': float(_Ebase.max() - _Ebase.min())}
    _shp = _hy['shape_max_abs_dE_eV'] / max(_hy['E_span_eV'], 1e-12)
    _raw = _hy['max_abs_dE_eV'] / max(_hy['E_span_eV'], 1e-12)
    chk(_shp <= 0.10 < _raw,
        "픽스처 확인: 평행이동은 모양 기준을 통과하고 원시 기준만 넘긴다 "
        f"(shape {_shp*100:.1f}% · raw {_raw*100:.1f}%)")

    # 실제 경로로도 친다 — 모양 기준은 널널하고 레거시 기준만 조인다
    _par = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                     continuation=True, hysteresis_tol=1.0,
                     hysteresis_span_tol=0.0, hysteresis_shape_tol=1.0)
    _ph = _par.get('hysteresis') or {}
    chk(_ph.get('ok') is True and _ph.get('operational_hold') is True,
        "⛔음성: 모양은 통과인데 레거시 기준만 걸리면 **물리 판정은 ok, 운영 보류**로 갈린다")
    chk('운영상 보류' in (_par.get('fit_quality_reason') or '')
        and 'V₀ 가 존재하지 않는다는 뜻이 아니다' in (_par.get('fit_quality_reason') or ''),
        "⛔⛔음성: 평행이동 보류의 사유가 **V₀ 존재 불가로 적히지 않는다** (회신 BQ-2 Q2)")
    chk(isinstance(_ph.get('shape_verdict_vs_tol'), dict)
        and len(set((_ph.get('shape_verdict_vs_tol') or {}).values())) >= 1,
        "문턱 의존성을 **표로 보여준다** (주장하지 않는다)")
    chk('dE_over_span' in (_hole.get('hysteresis') or {}),
        "곡선 갈림 비율(dE/span)이 기록에 남는다")
    # 양성 대조: 두 기준 다 널널하면 통과 — 즉 **기준이 판정을 만든다**
    _loose = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                       continuation=True, hysteresis_tol=1.0, hysteresis_span_tol=1.0,
                       hysteresis_shape_tol=1.0)
    chk(_loose.get('fit_quality_ok') is True,
        "양성 대조: 같은 자료도 기준을 풀면 통과한다 — 판정을 만드는 것은 **기준**이다")

    # ⛔음성 ②: 연쇄가 실제로 **앞 점에서 이어지는가** — 출발 구조가 달라야 한다
    _seen = []
    class _Spy(EMT):
        def calculate(self, atoms=None, *a, **k):
            _seen.append(atoms.get_volume())
            return super().calculate(atoms, *a, **k)
    _eos_branch(_cu, _Spy(), (1.00, 1.02), 0.05, 5, True)
    _n_cont = len(_seen)
    _seen.clear()
    _eos_branch(_cu, _Spy(), (1.00, 1.02), 0.05, 5, False)
    chk(_n_cont > 0 and len(_seen) > 0,
        "⛔음성: 두 갈래 모두 실제로 계산기를 부른다 (빈 경로가 아니다)")

    # ⑪ 회신 BQ P0-1 · P0-2 · P0-3 (2026-09-13)
    _bq = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                    continuation=True, hysteresis_tol=1.0, hysteresis_span_tol=1.0,
                       hysteresis_shape_tol=1.0)
    _h = _bq.get('hysteresis') or {}

    # P0-1 — 점마다 수렴·최종 최대힘이 남는가
    _cu_log = _h.get('convergence_up') or []
    chk(len(_cu_log) == len(_fr)
        and all({'final_fmax_eV_A', 'converged', 'n_steps'} <= set(r) for r in _cu_log),
        "P0-1: 부피점마다 **수렴 여부·최종 최대힘**이 남는다 (없으면 기전 판정 불가)")
    # ⛔음성: 스텝을 굶기면 **미수렴으로 표시**돼야 한다 (조용히 통과하면 안 된다)
    #   ⚠ 픽스처 주의: **완벽한 Cu 결정은 대칭 때문에 힘이 정확히 0** 이라 굶겨도
    #     '수렴' 으로 찍힌다. 흔들어서 실제 힘을 만들어야 이 시험이 뜻을 갖는다.
    _rough = _cu.copy(); _rough.rattle(stdev=0.08, seed=11)
    _starved = eos_sweep(_rough, EMT(), fractions=_fr, fmax=1e-9, relax_steps=1,
                         continuation=True, hysteresis_tol=1.0, hysteresis_span_tol=1.0,
                       hysteresis_shape_tol=1.0)
    _sl = (_starved.get('hysteresis') or {}).get('convergence_up') or []
    chk(_sl and all(not r['converged'] for r in _sl),
        "⛔음성: fmax 1e-9·steps 1 로 굶기면 **전부 미수렴**으로 찍힌다")
    chk(_sl and all(r['hit_step_limit'] for r in _sl),
        "⛔음성: 스텝 한도에 걸린 사실이 따로 기록된다")

    # ⛔⛔ 회신 BQ-2 P0-1 — **여기가 NO-GO 의 핵심이었다.**
    #   옛 시험은 "수렴이 기록되는가" 만 봤고 "차단하는가" 는 본 적이 없다.
    #   리뷰어는 그 틈으로 굶긴 0/14 (점별 최종힘 0.0403–0.1448 eV/Å) 를
    #   `fit_quality_ok=True` 로 통과시켜 V₀ 를 받아냈다.
    chk(_starved.get('downstream_eligible') is False,
        "⛔⛔음성: 굶긴 EOS 는 **후속 사용 자격이 없다** (기록만으로 끝내지 않는다)")
    chk('미수렴' in (_starved.get('downstream_block_reason') or ''),
        "⛔음성: 차단 사유에 미수렴 점이 명시된다")
    chk((_starved.get('convergence_summary') or {}).get('n_points_other', 0) > 0,
        "두 갈래를 **나눠** 센다 — 한 숫자로 합치면 양방향 수렴으로 오독한다")

    # 자격과 적합품질이 **독립**임을 직접 친다 (합성 기록으로 경로만 본다)
    # ⚠ 합성 기록도 **진짜 기록 모양**이어야 한다 — V_points/fractions 가 없으면 1:1 대응
    #   검사(회신 BQ-3 P1-b)가 거부한다. 그게 맞는 동작이다.
    _fk = lambda cv: attach_eligibility(
        {'fit_quality_ok': True, 'fit_quality_reason': 'OK', 'convergence': cv,
         'V_points': [1.0] * len(cv), 'E_points': [0.0] * len(cv),
         'fractions': [r.get('fraction', 1.0) for r in cv]})
    chk(_fk([{'fraction': 1.0, 'converged': False, 'final_fmax_eV_A': 0.14}]
            )['downstream_eligible'] is False,
        "⛔음성: fit_quality_ok=True 라도 미수렴 점이 있으면 자격 거부")
    chk(_fk([])['downstream_eligible'] is False,
        "⛔음성: 수렴 기록이 **없으면** 자격 거부 (모르는 것은 통과가 아니다)")
    chk(_fk([{'fraction': 1.0, 'converged': 'True', 'final_fmax_eV_A': 0.001}]
            )['downstream_eligible'] is False,
        "⛔음성: 문자열 'True' 를 참으로 세지 않는다 (json default=str 오염 대비)")
    chk(_fk([{'fraction': 1.0, 'converged': True, 'final_fmax_eV_A': 0.001}]
            )['downstream_eligible'] is True,
        "양성 대조: 적합 OK + 전 점 수렴이면 자격 있음 (무조건 떨구는 게 아니다)")
    chk(attach_eligibility({'fit_quality_ok': False, 'fit_quality_reason': 'r2 낮음',
                            'V_points': [1.0], 'E_points': [0.0], 'fractions': [1.0],
                            'convergence': [{'fraction': 1.0, 'converged': True,
                                             'final_fmax_eV_A': 0.001}]}
                           )['downstream_eligible'] is False,
        "⛔음성: 전 점 수렴이어도 적합이 불통과면 자격 거부 (둘 다 필요하다)")

    # ⛔⛔ 회신 BQ-3 재현 넷 — 리뷰어가 실제 함수로 뚫은 구멍을 그대로 시험으로
    _fr7 = [0.97, 0.98, 0.99, 1.00, 1.01, 1.02, 1.03]
    _ok7 = [{'fraction': f, 'converged': True, 'final_fmax_eV_A': 0.001} for f in _fr7]
    _bad7 = [{'fraction': f, 'converged': False, 'final_fmax_eV_A': 0.2} for f in _fr7[::-1]]
    _two = lambda up, dn: attach_eligibility(
        {'fit_quality_ok': True, 'fit_quality_reason': 'OK',
         'V_points': [1.0] * 7, 'E_points': [0.0] * 7, 'fractions': _fr7,
         'hysteresis': {'E_up': [0.0] * 7, 'E_down': [0.0] * 7, 'reported_branch': 'up',
                        'convergence_up': up, 'convergence_down': dn}})
    chk(_two(_ok7, _bad7)['downstream_eligible'] is False,
        "⛔⛔음성 (BQ-3 P0-1): 상승 7/7·하강 0/7 → **자격 없음** (판정에 쓴 양방향 점이 수렴해야 한다)")
    chk(_two(_ok7, [])['downstream_eligible'] is False,
        "⛔⛔음성 (BQ-3 P0-1): 하강 기록을 **없애도** 통과하지 않는다")
    chk(_two(_ok7, _ok7[::-1])['downstream_eligible'] is True,
        "양성 대조: 양방향 전 점 수렴이면 자격 있음")
    chk(_two(_ok7[:1], _ok7[::-1])['downstream_eligible'] is False,
        "⛔⛔음성 (BQ-3 P1-b): 에너지 7점에 상승 기록 **1개**면 1/1 이 아니라 **거부**다")
    _wrongf = [dict(r, fraction=r['fraction'] + 0.5) for r in _ok7]
    chk(_two(_wrongf, _ok7[::-1])['downstream_eligible'] is False,
        "⛔음성 (BQ-3 P1-b): 개수는 7인데 분율이 다른 기록 → 거부 (자리가 아니라 대응을 본다)")
    chk('1:1' in (_two(_ok7[:1], _ok7[::-1]).get('downstream_block_reason') or ''),
        "P1-b: 사유에 '1:1 대응' 이 적힌다")

    # ⛔⛔ BQ-3 P1-a — 반환값 True 로 힘 판정을 덮지 않는다 · 비유한 힘은 수렴이 아니다
    class _FakeOpt:
        def __init__(self, n): self._n = n
        def get_number_of_steps(self): return self._n
    class _FakeAtoms:
        def __init__(self, fmax_val):
            self._f = fmax_val
        def get_forces(self):
            import numpy as _n
            return _n.array([[self._f, 0.0, 0.0], [0.0, 0.0, 0.0]])
    _v = _conv_verdict(_FakeOpt(10), _FakeAtoms(0.14), 0.02, 500, ret=True)
    chk(_v['converged'] is False and '이긴다' in _v.get('⚠_불일치', ''),
        "⛔⛔음성 (BQ-3 P1-a): 반환값 True 여도 최종힘 0.14 > 0.02 면 **미수렴** — 힘 기준이 이긴다")
    _v2 = _conv_verdict(_FakeOpt(10), _FakeAtoms(float('nan')), 0.02, 500, ret=True)
    chk(_v2['converged'] is False and '⛔_비유한_힘' in _v2,
        "⛔⛔음성 (BQ-3 P1-a): **NaN** 힘은 반환값과 무관하게 미수렴")
    _v3 = _conv_verdict(_FakeOpt(10), _FakeAtoms(0.01), 0.02, 500, ret=False)
    chk(_v3['converged'] is True,
        "양성 대조: 힘이 기준 안이면 반환값 False 여도 수렴 (힘 기준이 이긴다 — 양쪽 다)")
    _v4 = _conv_verdict(_FakeOpt(500), _FakeAtoms(0.01), 0.02, 500, ret=True)
    chk(_v4['converged'] is True and _v4['hit_step_limit'] is True,
        "Q1a 유지: 마지막 허용 스텝에서 수렴한 경우를 오탐하지 않는다")

    # 문구 — "한 골짜기로 정의되지 않는다" 가 더는 안 나온다
    chk('한 골짜기로 정의되지 않는다' not in (_hole.get('fit_quality_reason') or ''),
        "⛔음성 (BQ-3): 결론 문구 '한 골짜기로 정의되지 않는다' 삭제됨")

    # P0-2 — 보고 곡선이 **한 갈래**인가 (min 섞기가 아닌가)
    chk(_h.get('reported_branch') == 'up'
        and _bq['E_points'] == _h['E_up'],
        "P0-2: 보고 곡선이 **올라가는 갈래 그대로**다 (min(up,down) 섞기 아님)")
    _mixed = [min(a, b) for a, b in zip(_h['E_up'], _h['E_down'])]
    chk(_bq['E_points'] != _mixed or _h['E_up'] == _mixed,
        "⛔음성: 하위 포락선과 다르다 (두 갈래가 실제로 갈린 경우)")
    chk('level_offset_eV' in _h and 'shape_max_abs_dE_eV' in _h,
        "Q2: 높이 차(level_offset)와 모양 차(shape_max)가 **따로** 기록된다")
    chk('창에' in ''.join(k for k in _h if '창' in k),
        "Q2: dE/span 이 창 의존이라는 경고가 기록에 박혀 있다")

    # P0-3 — V₀ 를 정의한 **상태**를 승계하는가
    chk(_bq.get('_branch_atoms') is not None,
        "P0-3: 보고 가지의 **마지막 구조**가 같이 돌아온다 (숫자만 넘기지 않는다)")
    _rec = {'eos': dict(_bq)}
    _a2, _pol = maybe_apply_eos_v0(at, _rec, A(apply_eos_v0=True, fixed_shape_relax=True), EMT())
    chk((_pol.get('v0_start_selection') or {}).get('method') == 'nearest_converged_up_branch',
        "P0-3: 승계 여부가 기록에 남는다 (승계함)")
    _rec2 = {'eos': {k: v for k, v in _bq.items() if k != '_branch_atoms'}}
    _v_at = at.get_volume()
    _a3, _pol2 = maybe_apply_eos_v0(at, _rec2, A(apply_eos_v0=True, fixed_shape_relax=True), EMT())
    # ⛔⛔ 회신 BQ-2 P0-3 — 종전에는 가지 구조가 없으면 **원본으로 대체하고 경고만** 했다.
    #   리뷰어: "원본 대체도 경고만으로 승계 조건을 충족하지는 않아요." 이제 차단한다.
    chk(_pol2.get('downstream_blocked') is True
        and '승계가 아니다' in (_pol2.get('block_reason') or ''),
        "⛔음성: 가지 구조가 없으면 **차단**한다 (원본 대체 + 경고로 때우지 않는다)")
    chk(abs(_a3.get_volume() - _v_at) < 1e-9,
        "⛔음성: 가지 부재 차단 시 구조는 원본 그대로")

    # ⑫ 회신 BQ Q2 — 빠져 있던 기본 확인 둘
    _g = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                   continuation=True, hysteresis_tol=1.0, hysteresis_span_tol=1.0,
                       hysteresis_shape_tol=1.0)
    chk(_g.get('V0_in_window') is True and _g.get('B0_positive') is True,
        "양성: 정상 적합은 V₀ 가 창 안이고 B₀ > 0 이다")
    chk(_g.get('fit_quality_ok') is True, "양성: 그래서 통과한다")

    # ⛔음성: 창 밖 최소를 **통과시키지 않는다** (외삽은 측정이 아니다)
    #   실측 근거: P2_Al2S3_B 가 V₀ 5620 Å³ (셀 4066, 창 밖 38 %) 로 나왔는데
    #   옛 조건 `0 < V0 < 5*V_mid` 는 그것을 통과시켰다.
    import numpy as _np2
    _V = _np2.array([100.0, 110.0, 120.0, 130.0, 140.0])
    _E = _np2.array([0.0, -0.5, -1.0, -1.6, -2.3])          # 창 안에 최소가 없다(단조 감소)
    # ⛔ 종전에는 여기서 **시험 전용 복제 함수**(`_fit_in_window`)를 만들어 쳤다.
    #   실물이 아니라 복제를 치면 실물이 바뀌어도 시험은 초록이다 — 실물을 친다.
    chk(_fit_gate(0.999, 200.0, 100.0, 4.0, _V)['V0_in_window'] is False,
        "⛔음성: V₀ 200 은 창 [100,140] 밖 — 창 밖 판정이 실제로 작동한다")
    chk(_fit_gate(0.999, 125.0, 100.0, 4.0, _V)['V0_in_window'] is True,
        "양성 대조: 창 안 V₀ 는 통과한다 (무조건 떨구는 게 아니다)")

    # ⛔⛔ 회신 BQ-2 Q5 — **창 경계에 붙은 최소를 내부 최소와 구분하는가**
    _mid = _fit_gate(0.999, 120.0, 100.0, 4.0, _V)       # 한가운데
    _edg = _fit_gate(0.999, 102.0, 100.0, 4.0, _V)       # 최외곽 구간 안
    chk(_mid['V0_at_window_edge'] is False and _edg['V0_at_window_edge'] is True,
        "⛔음성: 창 **경계에 붙은** V₀ 를 한가운데 V₀ 와 구분한다")
    chk(_edg['fit_quality_ok'] is True and '경계' in _edg['fit_quality_reason'],
        "경계 최소는 **떨구지 않고 표시**한다 (구분하라는 것이지 버리라는 게 아니다)")
    chk(_mid['V0_bracketed'] is True
        and _fit_gate(0.999, 200.0, 100.0, 4.0, _V)['V0_bracketed'] is False,
        "⛔음성: V₀ 양쪽에 측정점이 있는지(내삽인지)를 따로 센다")

    # ⛔⛔ 회신 BQ-2 Q5 — B₀′ 만 어긋난 경우 **V₀ 중심 기준은 살아 있다**고 보인다
    #   (판정은 바꾸지 않는다 — 바꾸려면 그 사실을 명시해야 한다)
    _bponly = _fit_gate(0.999, 120.0, 100.0, -1.94, _V)
    chk(_bponly['fit_quality_ok'] is False and _bponly['v0_centric_ok'] is True,
        "⛔음성: B0'=-1.94 로 떨어져도 v0_centric_ok 는 참 — 무엇이 떨어뜨렸는지 보인다")
    chk('보수적 선택' in _bponly['fit_quality_reason'],
        "그 사유가 **보수적 선택**임을 문구가 밝힌다 (물리적 필수조건이 아니다)")
    chk(_fit_gate(0.999, 120.0, -5.0, 4.0, _V)['v0_centric_ok'] is False,
        "⛔음성: B₀ 가 음수면 v0_centric_ok 도 거짓 (B₀ 양수는 진짜 필수조건이다)")
    chk('B0' in ''.join(k for k in _g) or 'B0_positive' in _g,
        "B₀ 부호 확인이 기록에 남는다")
    # ⚠ B0'<0 을 떨구는 것은 **보수적 선택**이지 보편 규칙이 아니다 — 문구로 밝힌다
    _r = eos_sweep(_cu, EMT(), fractions=_fr, fmax=0.05, relax_steps=30,
                   continuation=True, hysteresis_tol=1.0, hysteresis_span_tol=1.0,
                       hysteresis_shape_tol=1.0)
    chk(_r.get('fit_quality_ok') or '보수적 선택' in (_r.get('fit_quality_reason') or ''),
        "B0' 게이트가 떨굴 때는 '보수적 선택' 임을 문구가 밝힌다")

    # ⑨ ★ process_one 산출 파일 — **이름이 곧 주장이다** (회신 BQ-2 P0-3)
    #   리뷰어 실측: 실패한 EOS 의 마지막 팽창점(원본 100 → 106)이
    #   `final_v0_applied.xyz` 로 나가고 탄성까지 전달됐다. 여기가 그 회귀의 현장이다.
    import tempfile as _tf
    from pathlib import Path as _P

    class _Args(A):
        def __init__(self, **kw):
            super().__init__()
            self.no_anneal = True; self.anneal_T = 300; self.anneal_ps = 1
            self.eos_fractions = [0.98, 0.99, 1.00, 1.01, 1.02]
            self.n_eos_seeds = 1; self.eos_perturb = 0.1
            self.eos_continuation = False
            self.eos_hysteresis_tol = 1.0; self.eos_hysteresis_span_tol = 1.0
            self.elastic_eps = 0.005; self.elastic_fmax = 0.2
            self.apply_eos_v0 = True; self.fixed_shape_relax = True
            self.eos_fmax = 0.05; self.relax_steps = 30
            self.__dict__.update(kw)

    with _tf.TemporaryDirectory() as _td:
        _root = _P(_td)
        write(str(_root / 'cu.xyz'), bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2))
        # ⚠ 픽스처 함정 — **완벽한 Cu 결정은 대칭 때문에 힘이 정확히 0** 이라
        #   굶겨도(fmax 1e-9) '수렴' 이 된다. 차단 경로를 보려면 대칭을 깨야 한다.
        #   (같은 함정을 2026-09-13 에 rattle 로 한 번 겪었다 — 여기선 공공으로 깬다)
        _vac = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2)
        del _vac[0]
        write(str(_root / 'cuvac.xyz'), _vac)
        # (a) 차단되는 경우 — EOS 점을 굶긴다
        _rb = process_one(_root / 'cuvac.xyz', EMT(), _root / 'blocked',
                          _Args(eos_fmax=1e-9, relax_steps=1))
        _wb = _rb.get('structures_written') or {}
        _db = _root / 'blocked' / 'cuvac'
        chk(_wb.get('downstream_blocked') is True and _wb.get('downstream_input') is None,
            "⛔⛔음성: 차단되면 하류가 집어갈 최종 구조가 **없다**")
        chk(not (_db / 'final_v0_applied.xyz').exists(),
            "⛔⛔음성: 차단된 경로에 `final_v0_applied.xyz` 를 **쓰지 않는다** (이름이 곧 주장이다)")
        chk((_db / 'DIAGNOSTIC_blocked_not_for_downstream.xyz').exists(),
            "차단해도 진단 구조는 남긴다 (버리지 않는다)")
        chk((_rb.get('elastic') or {}).get('skipped') is True,
            "⛔음성: 차단되면 **탄성을 계산하지 않는다** (후속 계산 차단)")
        # (b) 양성 대조 — 무조건 막는 게 아니다
        _rp = process_one(_root / 'cu.xyz', EMT(), _root / 'ok', _Args())
        _wp = _rp.get('structures_written') or {}
        chk(_wp.get('downstream_blocked') is False
            and _wp.get('downstream_input') == 'final_v0_applied.xyz',
            "양성 대조: 자격을 갖추면 final_v0_applied.xyz 가 나온다")
        chk((_root / 'ok' / 'cu' / 'final_v0_applied.xyz').exists(),
            "양성 대조: 그 파일이 실제로 존재한다")
        chk((_rp.get('elastic') or {}).get('skipped') is not True,
            "양성 대조: 탄성이 실제로 돌았다 (차단 경로와 갈린다)")

        # ⑩ ★ --regate — 저장된 E(V) 로 **같은 판정**이 재현되는가
        #   라이브와 소급이 갈리면 소급 재판정은 아무 의미가 없다.
        _rows = regate_paths([str(_root / 'ok' / 'cu' / 'postproc.json')], fmax=0.05)
        chk(len(_rows) == 1 and _rows[0].get('fit_quality_ok') is True,
            "regate: 통과한 기록은 소급해도 통과한다")
        chk(_rows[0].get('verdict_changed') is False,
            "⛔음성: 같은 잣대면 판정이 **안 바뀐다** (바뀌면 두 경로가 갈린 것이다)")
        _lv = ((_rp.get('eos') or {}).get('V0'))
        _rv = (_rows[0].get('raw_refit') or {}).get('V0')
        chk(_lv and _rv and abs(_lv - _rv) / _lv < 1e-6,
            "regate: 재적합 V₀ 가 라이브 V₀ 와 일치한다 (같은 식·같은 초기값)")
        _rb2 = regate_paths([str(_root / 'blocked' / 'cuvac' / 'postproc.json')], fmax=1e-9)
        chk(_rb2 and _rb2[0].get('downstream_eligible') is False,
            "⛔음성: 굶긴 기록은 소급해도 **자격 없음**")

    # ⑪ regate 보조 — 이름에서 fmax 되찾기 · 없는 자료 처리
    chk(_fmax_from_name('runs/x/fix_W6_f02') == 0.02
        and _fmax_from_name('fix_W3_f005') == 0.005,
        "regate: 조건 이름에서 fmax 를 되찾는다 (_f02 → 0.02, _f005 → 0.005)")
    chk(_fmax_from_name('runs/x/whatever') is None,
        "⛔음성: 못 되찾으면 None — 아무 값이나 지어내지 않는다")
    chk('regate_skipped' in regate_eos({'V_points': [1.0, 2.0], 'E_points': [0.0, 1.0]}),
        "⛔음성: 점이 4개 미만이면 **건너뛴다** (BM3 4모수를 못 맞춘다)")
    chk('regate_skipped' in regate_eos({}),
        "⛔음성: V_points 가 없으면 건너뛴다 (없는 자료를 지어내지 않는다)")

    # ⛔⛔ 회신 BQ-2 Q1a 소급 — 마지막 스텝 수렴을 **옛 정의가 오탐**한 것을 되돌린다
    _oldrec = {'V_points': [100.0, 105.0, 110.0, 115.0, 120.0],
               'E_points': [0.20, 0.05, 0.00, 0.05, 0.20],
               'convergence': [{'fraction': f, 'n_steps': 30, 'final_fmax_eV_A': 0.018,
                                'converged': False, 'hit_step_limit': True}
                               for f in (0.94, 0.97, 1.0, 1.03, 1.06)]}
    _rg = regate_eos(_oldrec, fmax=0.02)
    chk(all(c['converged'] is True for c in _rg['convergence']),
        "⛔음성: 잔여힘 0.018 ≤ 기준 0.02 면 **한도에 걸렸어도 수렴**이다 (옛 정의의 오탐)")
    _rg2 = regate_eos(_oldrec, fmax=None)
    chk(all(c['converged'] is False for c in _rg2['convergence']),
        "⛔음성: fmax 를 모르면 수렴을 **다시 세지 않는다** (옛 판정 그대로)")
    _rg3 = regate_eos(_oldrec, fmax=0.01)
    chk(all(c['converged'] is False for c in _rg3['convergence'])
        and _rg3['downstream_eligible'] is False,
        "⛔음성: 기준을 더 조이면 미수렴이고 자격도 없다")

    # ⑫ ★ 압력 부호 감사 (회신 BQ-2 Q4) — **산술로** 판정하는가, 일괄 반전이 아닌가
    import tempfile as _tf2
    _sig = [[-3.0, 0.1, 0.0], [0.1, -3.0, 0.0], [0.0, 0.0, -3.6]]
    _tr3 = float(np.trace(np.asarray(_sig)) / 3.0)          # = -3.2
    with _tf2.TemporaryDirectory() as _td2:
        _q4 = Path(_td2)
        _mk = lambda nm, node: (_q4 / nm).write_text(
            json.dumps({'name': nm, 'cell_policy': {'residual_stress': node}}))
        _mk('good.json', {'sigma_GPa': _sig, 'P_mean_GPa': -_tr3,
                          'deviatoric_max_abs_GPa': 0.4, '⚠_부호': 'x'})
        _mk('bug.json', {'sigma_GPa': _sig, 'P_mean_GPa': _tr3,
                         'deviatoric_max_abs_GPa': 0.4})
        _mk('other.json', {'sigma_GPa': _sig, 'P_mean_GPa': 99.0})
        _mk('nosig.json', {'P_mean_GPa': 1.0})
        _before = {f.name: f.read_text() for f in _q4.glob('*.json')}
        _ap = audit_pressure_sign([str(_q4 / '*.json')])
        _by = {Path(r['file']).name: r for r in _ap['rows']}
        chk(_by['good.json']['verdict'] == 'already_correct',
            "Q4: P = −tr(σ)/3 인 기록은 **손대지 않는다**")
        chk(_by['bug.json']['verdict'] == 'corrected'
            and abs(_by['bug.json']['corrected_P_mean_GPa'] - (-_tr3)) < 1e-9,
            "Q4: P = +tr(σ)/3 인 기록만 정정한다 (부호 버그의 산물)")
        chk(_by['other.json']['verdict'] == 'unknown'
            and _by['other.json']['corrected_P_mean_GPa'] is None,
            "⛔⛔음성: ±tr/3 어느 쪽도 아니면 **손대지 않는다** (일괄 반전 금지)")
        chk(_by['nosig.json']['verdict'] == 'no_sigma',
            "⛔음성: σ 가 없으면 판정하지 않는다 (부호를 짐작하지 않는다)")
        chk(all(_by[k]['deviatoric_max_abs_GPa'] == 0.4 for k in
                ('good.json', 'bug.json')),
            "⛔음성: **편차응력은 그대로다** (부호를 뒤집지 않는다)")
        chk({f.name: f.read_text() for f in _q4.glob('*.json')} == _before,
            "⛔⛔음성: 원본 파일이 **한 글자도 안 바뀐다** (파생 기록만 만든다)")
        chk(_ap['counts'] == {'already_correct': 1, 'corrected': 1,
                              'unknown': 1, 'no_sigma': 1},
            "Q4: 네 갈래가 실제로 갈린다 (전부 같은 판정이면 시험이 아무것도 안 본 것이다)")
        # 실물 stress_report 의 출력이 already_correct 로 읽히는가 (규약 왕복)
        _sr2 = stress_report(at)
        (_q4 / 'live.json').write_text(json.dumps({'x': _sr2}))
        _lv = [r for r in audit_pressure_sign([str(_q4 / 'live.json')])['rows']][0]
        chk(_lv['verdict'] == 'already_correct',
            "Q4 왕복: 지금 stress_report 가 낸 값은 감사에서 **이미 맞다**로 읽힌다")

    # ⑬ UMA 추론 설정 기록 (회신 BQ-2 Q6)
    _up = uma_inference_provenance('turbo')
    chk(_up.get('requested_mode') == 'turbo' and _up.get('model_name') == 'uma-s-1p1',
        "Q6: 요청한 모드와 체크포인트 이름이 기록된다")
    chk('TF32' in _up.get('⚠_turbo_의_뜻', '')
        and 'bf16' in _up.get('⚠_turbo_의_뜻', ''),
        "Q6 정정: turbo 의 핵심 차이는 **TF32** 이고 'turbo=bf16' 은 부정확하다고 적힌다")
    chk(('fairchem_version' in _up) or ('fairchem_error' in _up),
        "Q6: fairchem 버전을 읽거나, 못 읽었다는 사실을 남긴다")
    chk((_up.get('fairchem_version') is not None) or ('⛔_불완전' in _up),
        "⛔음성: 못 읽은 항목을 기본값으로 채우지 않고 **불완전하다고 표시**한다")

    # ⑭ ★ 회신 BQ-3 실행 전 최소조건 ② — 점별 저장 · 최근접점 승계 · 저장→재독 · 폴더 거부
    import tempfile as _tf3
    with _tf3.TemporaryDirectory() as _td3:
        _r3 = _P(_td3)
        _cuf = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2)
        _cuf.rattle(stdev=0.03, seed=3)
        _m3 = {'structure': 'cu', 'run_id': 'test', 'run_tag': 'T', 'code_id': 'x',
               'model': 'emt', 'inference_mode': 'None', 'relax_steps': 30}
        _fr5 = (0.98, 0.99, 1.00, 1.01, 1.02)
        _sw = eos_sweep(_cuf, EMT(), fractions=_fr5, fmax=0.05, relax_steps=30,
                        continuation=True, hysteresis_tol=1.0, hysteresis_span_tol=1.0,
                        hysteresis_shape_tol=1.0, save_dir=_r3 / 'frames', meta=_m3)
        _up = _sw['hysteresis']['convergence_up']; _dn = _sw['hysteresis']['convergence_down']
        _paths = [c.get('frame_path') for c in _up + _dn]
        chk(len(_paths) == 10 and all(p_ and _P(p_).exists() for p_ in _paths),
            "Q5-2: 양방향 5점 = **프레임 10개**가 전부 파일로 남는다")
        chk(all(c.get('point_id') and (i == 0) == (c.get('prev_point_id') is None)
                for i, c in enumerate(_up)),
            "Q5-2: 점 ID 와 **직전 점 ID** 가 기록된다 (첫 점만 None)")
        # 저장 → 재독 보존 기준 (좌표 ≤1e-8 Å · ID · PBC · 응력 · 메타)
        _f0 = _sw['_branch_frames'][2]
        _rd = read(_up[2]['frame_path'], format='extxyz')
        _err = float(np.abs(_rd.positions - _f0.positions).max())
        chk(_err <= 1e-8, f"Q5-2 보존: 저장→재독 좌표 오차 {_err:.2e} Å ≤ 1e-8")
        chk(np.array_equal(_rd.arrays.get('atom_id'), np.arange(len(_f0)))
            and all(_rd.pbc) and 'stress_voigt_eV_A3' in _rd.info
            and 'forces_eV_A' in _rd.arrays and _rd.info.get('structure') == 'cu'
            and _rd.info.get('direction') == 'up' and 'energy_eV' in _rd.info,
            "Q5-2 보존: atom_id · PBC · 응력(단위) · 힘 벡터 · 에너지 · 구조/방향 메타 전부 남는다")
        # 미수렴점도 저장하는가 — 굶긴 런
        _st = eos_sweep(_cuf, EMT(), fractions=_fr5, fmax=1e-9, relax_steps=1,
                        continuation=True, hysteresis_tol=1.0, hysteresis_span_tol=1.0,
                        hysteresis_shape_tol=1.0, save_dir=_r3 / 'starved', meta=_m3)
        _stu = _st['hysteresis']['convergence_up']
        chk(all(c.get('converged') is False for c in _stu)
            and all(_P(c['frame_path']).exists() for c in _stu)
            and read(_stu[0]['frame_path'], format='extxyz').info.get('converged') is False,
            "⛔음성 Q5-2: **미수렴점도 저장**되고 프레임 안에 converged=False 가 박힌다")

        # 최근접 수렴점 선택 + 동률 규칙
        _fk_frames = []
        for v in (90.0, 100.0, 110.0, 120.0, 130.0):
            _a = bulk('Cu', 'fcc', a=3.6, cubic=True)
            _a.set_cell(_a.cell.array * (v / _a.get_volume()) ** (1 / 3), scale_atoms=True)
            _fk_frames.append(_a)
        _cvT = [{'converged': True, 'fraction': f} for f in (0.9, 1.0, 1.1, 1.2, 1.3)]
        _s1 = _select_nearest_converged(_fk_frames, _cvT, 112.0)
        chk(_s1 and _s1['index'] == 2, "Q5-4: |Vᵢ−V₀| 최소 수렴점을 고른다 (112 → 110)")
        _s2 = _select_nearest_converged(_fk_frames, _cvT, 115.0)
        chk(_s2 and _s2['index'] == 2, "Q5-4 동률: 110 과 120 이 같은 거리면 **낮은 인덱스**")
        _cvX = [dict(c, converged=(i != 2)) for i, c in enumerate(_cvT)]
        _s3 = _select_nearest_converged(_fk_frames, _cvX, 112.0)
        chk(_s3 and _s3["index"] == 3, "⛔음성 Q5-4: 최근접점(110)이 **미수렴**이면 건너뛰고 다음 최근접 수렴점(120, |8| < |12|)을 고른다")
        chk(_select_nearest_converged(_fk_frames, [dict(c, converged=False) for c in _cvT], 112.0) is None,
            "⛔음성 Q5-4: 수렴점이 하나도 없으면 None (끝점으로 때우지 않는다)")

        # 구조 비교 — 판정하지 않고 사실만
        _ref = bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2)
        _ref.symbols[:8] = 'Li'                       # 앞 8개를 Li 로 — 골격/Li 분리 시험
        _ref.new_array('atom_id', np.arange(len(_ref)))
        _same = _ref.copy()
        _c0 = compare_frames(_ref, _same, cutoff=3.0)
        chk(_c0['continuity'] == 'neighbor_sets_identical' and _c0['max_disp_A'] < 1e-12,
            "Q5-3 양성 대조: 같은 프레임 → 이웃 집합 동일 · 변위 0")
        _sh = _ref.copy(); _sh.positions += np.array([0.3, 0.0, 0.0])    # 전체 병진
        _c1 = compare_frames(_ref, _sh, cutoff=3.0)
        chk(_c1['max_disp_A'] < 1e-9 and abs(_c1['framework_translation_removed_A'][0] - 0.3) < 1e-9,
            "Q5-3: **골격 공통 병진**은 제거된다 (병진은 변위가 아니다)")
        _mv = _ref.copy(); _mv.positions[0] += np.array([1.2, 0.0, 0.0])  # Li 하나 이동
        _c2 = compare_frames(_ref, _mv, cutoff=3.0)
        chk(_c2['continuity'] == 'neighbor_sets_changed' and _c2['max_disp_atom_index'] == 0
            and _c2['max_disp_atom_symbol'] == 'Li' and _c2['n_Li_with_neighbor_set_changed'] >= 1,
            "Q5-3: Li 하나가 1.2 Å 움직이면 이웃 집합 변화 + 최대변위 원자가 그 Li 로 찍힌다")
        chk(_c2['rmsd_Li_A'] > _c2['rmsd_framework_A'],
            "Q5-3: Li 와 골격 RMSD 가 **분리**되고 움직인 쪽이 크다")
        _sw2 = _ref.copy(); _sw2.positions[[0, 1]] = _sw2.positions[[1, 0]]  # Li 둘 자리 교환
        _c3 = compare_frames(_ref, _sw2, cutoff=3.0)
        chk(_c3['max_disp_A'] > 1.0,
            "⛔음성 Q5-3: Li 자리 교환을 **재정렬로 지우지 않는다** (ID 유지 → 변위로 잡힌다)")
        _bad = _ref.copy(); _bad.set_cell(_bad.cell.array * 1.01, scale_atoms=True)
        chk(compare_frames(_ref, _bad)['continuity'] == 'continuity_unknown',
            "⛔음성 Q5-3: 셀이 다르면 비교하지 않는다 (continuity_unknown)")
        chk('골짜기 판정이 아니다' in _c2.get('⛔_읽는_법', ''),
            "Q5-3: 문턱으로 '같은 골짜기' 를 선언하지 않는다는 문구가 박혀 있다")

        # 폴더 재사용 거부 (BQ-3 P0-3 잔여)
        write(str(_r3 / 'cu.xyz'), bulk('Cu', 'fcc', a=3.6, cubic=True) * (2, 2, 2))
        _o1 = process_one(_r3 / 'cu.xyz', EMT(), _r3 / 'run1', _Args())
        chk((_r3 / 'run1' / 'cu' / 'final_v0_applied.xyz').exists()
            and len((_o1.get('structures_written') or {}).get('final_sha256', '')) == 64
            and (_o1.get('structures_written') or {}).get('run_id') == _o1.get('run_id'),
            "P0-3: 최종 파일이 sha256 와 run_id 로 **자격 기록에 결속**된다")
        try:
            process_one(_r3 / 'cu.xyz', EMT(), _r3 / 'run1', _Args(eos_fmax=1e-9, relax_steps=1))
            _refused = False
        except RuntimeError as _e:
            _refused = '재사용 거부' in str(_e)
        chk(_refused, "⛔⛔음성 P0-3: 같은 폴더에 다시 돌리면 **거부**한다 (이전 최종 파일이 남는 경로 차단)")
        chk((_r3 / 'run1' / 'cu' / 'final_v0_applied.xyz').exists(),
            "P0-3: 거부해도 이전 결과를 **지우지 않는다**")
        chk((_o1.get('cell_policy') or {}).get('v0_start_selection', {}).get('method')
            == 'nearest_converged_up_branch'
            and '4_displacement_vs_scaled_start' in (_o1.get('cell_policy') or {}).get('succession_checks', {}),
            "Q5-4: 실제 process_one 경로에서 최근접점 승계 + 확인 순서 ①~④ 가 기록된다")

    print(f"  selftest: ⭕ {ok} · ⛔ {fail}")
    return 0 if fail == 0 else 1


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--winners', help='winners.json from select_winners.py')
    p.add_argument('--xyz', nargs='+', help='specific xyz files')
    p.add_argument('--out')          # ⚠ --selftest 는 out 이 필요 없다 (아래에서 검사)
    p.add_argument('--device', default='cuda')
    p.add_argument('--task', default='omat')
    # Step toggles
    p.add_argument('--no_anneal', action='store_true')
    p.add_argument('--no_eos', action='store_true')
    p.add_argument('--no_elastic', action='store_true')
    # Anneal params
    p.add_argument('--anneal_T', type=float, default=300,
                  help='Light anneal T (default 300K)')
    p.add_argument('--anneal_ps', type=float, default=20,
                  help='Light anneal time (default 20 ps)')
    # EOS params
    p.add_argument('--eos_fractions', nargs='+', type=float,
                  default=[0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06])
    p.add_argument('--eos_fmax', type=float, default=0.05)
    p.add_argument('--eos_continuation', action='store_true',
                   help='EOS 부피점을 **이어서** 완화한다 (앞 점의 완화 결과가 다음 출발점). '
                        '무질서계에서 골짜기 이동을 막는다. 양방향으로 돌고 두 갈래 V₀ 가 '
                        '--eos_hysteresis_tol 넘게 갈리면 **적합을 떨군다**. '
                        '⚠ V₀ 의 뜻이 달라진다 — "연속으로 이어진 가지 위의 최소"다. 기본은 꺼짐')
    p.add_argument('--eos_hysteresis_shape_tol', type=float, default=0.10,
                   help='두 갈래 **모양** 차(평행이동 제거)의 곡선폭 대비 허용치. '
                        '이것이 물리 판정이다 (회신 BQ-2 Q2)')
    p.add_argument('--eos_hysteresis_span_tol', type=float, default=0.10,
                   help='두 갈래 E(V) 최대차를 **곡선 자신의 폭**으로 나눈 값의 허용치 '
                        '(기본 0.10 = 10 %%). ⛔ V₀ 만 보면 구멍이 난다 — 곡선이 95 %% 갈려도 '
                        '최소 위치는 겹칠 수 있다(실측 P2_Al2S3_A). 문턱 근거: 질서계 0.46 %% vs '
                        '무질서계 25–95 %% 라 1~25 %% 어디에 둬도 판정이 같다')
    p.add_argument('--eos_hysteresis_tol', type=float, default=0.01,
                   help='--eos_continuation 의 두 갈래 V₀ 허용 상대차 (기본 0.01 = 1 %%)')
    p.add_argument('--n_eos_seeds', type=int, default=1,
                   help='EOS ensemble size: N rattled seeds, best BM3 fit kept '
                        '(1 = single curve, current behaviour)')
    p.add_argument('--eos_perturb', type=float, default=0.1,
                   help='rattle stdev (Å) applied to EOS seeds > 0')
    # Elastic params
    p.add_argument('--elastic_eps', type=float, default=0.005,
                  help='Voigt strain magnitude')
    p.add_argument('--elastic_fmax', type=float, default=0.05)
    # General
    p.add_argument('--relax_steps', type=int, default=500)
    # ── 셀 정책 (2026-09-13, 회신 BP §4b) — 기본값은 과거 동작 그대로 ──
    p.add_argument('--apply_eos_v0', action='store_true',
                   help='EOS 가 낸 V0 를 **실제로 적용**해 고정셀 원자완화 후 탄성으로 넘긴다 '
                        '(기본 미적용 = GAP-3 그대로, 단 record 에 경고가 박힌다)')
    p.add_argument('--fixed_shape_relax', action='store_true',
                   help='0단계 relax 를 CellFilter 없이 고정셀로 한다 (각도·길이비 보존)')
    p.add_argument('--run_tag', default='',
                   help='조건 이름 등 실행 식별 태그 — 점별 프레임과 기록에 박힌다 (예: W3_f02)')
    p.add_argument('--uma_mode', default=None,
                   help="UMA 추론 설정을 **선언적으로** 지정 (예: default / turbo). "
                        "생략하면 라이브러리 기본값 — 다만 실제 설정은 기록된다 (회신 BQ-2 Q6)")
    p.add_argument('--audit_pressure', nargs='+', metavar='PATH',
                   help='저장된 기록의 압력 부호를 **증거로** 판정하고 정정 파생 기록을 만든다. '
                        '원본은 고치지 않는다 (회신 BQ-2 Q4)')
    p.add_argument('--audit_pressure_out', help='압력 정정 파생 기록 JSON 경로')
    p.add_argument('--regate', nargs='+', metavar='PATH',
                   help='저장된 postproc*.json 에 **지금의 게이트**를 다시 매긴다 '
                        '(파일/디렉터리/glob). 원본은 고치지 않는다')
    p.add_argument('--regate_fmax', type=float, default=None,
                   help='수렴 재판정에 쓸 fmax. 생략하면 디렉터리 이름(_f02)에서 되찾고, '
                        '그것도 없으면 **수렴을 다시 세지 않는다**')
    p.add_argument('--regate_out', help='재판정 결과 JSON 경로')
    p.add_argument('--selftest', action='store_true',
                   help='셀 정책 로직만 검사 (UMA 없이 ASE EMT 로 — 음성 경로 포함)')
    p.add_argument('--limit', type=int, default=None,
                  help='Limit to first N structures (debug)')
    args = p.parse_args()
    if args.selftest:
        sys.exit(_selftest())
    if args.audit_pressure:
        _ap = audit_pressure_sign(args.audit_pressure, args.audit_pressure_out)
        print(f"\n  압력 부호 감사: {_ap['counts']}")
        for _r in _ap['rows'][:40]:
            print(f"   {_r.get('verdict', 'error'):<16}{(_r.get('field_path') or '')[:40]:<42}"
                  f"{_r.get('file', '')[-40:]}")
        if args.audit_pressure_out:
            print(f"  → {args.audit_pressure_out}")
        sys.exit(0)
    if args.regate:
        _rows = regate_paths(args.regate, fmax=args.regate_fmax,
                             hysteresis_tol=args.eos_hysteresis_tol,
                             hysteresis_span_tol=args.eos_hysteresis_span_tol,
                             hysteresis_shape_tol=args.eos_hysteresis_shape_tol)
        print_regate(_rows)
        if args.regate_out:
            Path(args.regate_out).write_text(json.dumps(_rows, indent=2,
                                                     default=str, ensure_ascii=False))
            print(f"  → {args.regate_out}")
        sys.exit(0)
    if not args.out:
        p.error('--out 이 필요하다 (--selftest 제외)')


    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if args.winners:
        winners = json.loads(Path(args.winners).read_text())['winners']
        xyz_paths = [Path(w['xyz_file']) for w in winners
                    if Path(w.get('xyz_file', '')).exists()]
    elif args.xyz:
        xyz_paths = [Path(p) for p in args.xyz]
    else:
        p.error("Provide --winners or --xyz")

    if args.limit:
        xyz_paths = xyz_paths[:args.limit]

    # Resume
    summary_path = out / 'postproc_summary.json'
    done = {}
    if summary_path.exists():
        existing = json.loads(summary_path.read_text())
        done = {r['name']: r for r in existing.get('records', [])}
        print(f"Resume: {len(done)} already done")
    # NEW-D: use winner_name for resume check
    todo = [p for p in xyz_paths if winner_name(p) not in done]
    print(f"To process: {len(todo)}/{len(xyz_paths)}")

    print(f"Loading UMA-s-1p1 ({args.device})...")
    calc = load_uma(args.device, args.task, mode=getattr(args, 'uma_mode', None))
    _uma_prov = uma_inference_provenance(getattr(args, 'uma_mode', None))
    print(f"  UMA 추론: mode={_uma_prov.get('requested_mode')} · "
          f"torch={_uma_prov.get('torch_version')} · "
          f"fairchem={_uma_prov.get('fairchem_version')} · "
          f"TF32(matmul)={_uma_prov.get('tf32_matmul')} · "
          f"GPU={_uma_prov.get('gpu_name')}")

    records = list(done.values())
    t_start = time.time()
    for i, xpath in enumerate(todo):
        wname = winner_name(xpath)
        print(f"\n[{i+1}/{len(todo)}] {wname}")
        try:
            rec = process_one(xpath, calc, out, args)
            records.append(rec)
            ann = rec.get('anneal', {})
            eos = rec.get('eos', {})
            ela = rec.get('elastic', {})
            # dict.get(k, default) only fires when key is ABSENT — None values
            # (e.g. eos.B0_GPa when Bp-gate rejected the fit) slip through and
            # crash :.1f format. Coerce None→NaN explicitly.
            _nz = lambda x: float('nan') if x is None else x
            print(f"  E={_nz(rec.get('E_post_anneal_per_atom')):.4f} "
                  f"B0={_nz(eos.get('B0_GPa')):.1f} GPa "
                  f"E_young={_nz(ela.get('E_young_GPa')):.1f} GPa "
                  f"Pugh={_nz(ela.get('pugh_ratio_GoverB')):.2f}")
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            records.append({'name': winner_name(xpath), 'error': str(e)})
        # Periodic save
        if (i + 1) % 3 == 0 or (i + 1) == len(todo):
            summary_path.write_text(json.dumps({
                'provenance': get_provenance(),
                # ⛔ 회신 BQ-2 Q6 — "default" 라는 **이름**이 아니라 실제 환경을 남긴다
                'uma_inference': _uma_prov,
                'cli_args': vars(args),
                'n_done': len(records),
                'records': records,
            }, indent=2, default=str))

    print(f"\n{'='*60}")
    print(f"✓ Post-proc done: {len(records)} structures, "
          f"{time.time()-t_start:.0f}s")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    main()
