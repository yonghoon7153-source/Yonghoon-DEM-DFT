#!/usr/bin/env python3
"""γ 사전 적합이 **왜** 그 값에 앉았는지 본다 — `fit_gamma_si` 의 60 점 스캔을 그대로 펼친다.

    python3 scripts/gamma_prefit_report.py --data-root <루트> --half-cell <pristine.xlsx> --si-source Li
    python3 scripts/gamma_prefit_report.py --data-root <루트> --half-cell <pristine.xlsx> \\
        --si-source external --literature <pyDMA 예제.xlsx>

왜 스크립트인가: §13-5 의 열린 항목("우리 γ 사전 적합이 0.224 가 아니라 **하한 0.02 에 붙는다**,
RMSE 0.473923")을 가르는 관측이 **스캔의 모양** 하나다. 적합값 한 개만 보면 "국소 최소에 빠졌나"
와 "자료가 그 방향을 원한다" 를 구별할 수 없는데, 60 점을 펼치면 바로 갈린다:

  · 스캔이 **단조 증가** (최소가 왼쪽 끝)  → 최적화 실패가 아니다. 이 반쪽전지·이 문헌 곡선 조합은
    Si 분율이 **하한보다 더 작기를** 원한다. 그러면 의심할 것은 optimizer 가 아니라 **입력**이다
    (어느 반쪽전지를 넣었나 · 문헌 곡선이 그 셀의 Si 인가).
  · 스캔에 **안쪽 최소**가 있는데 보고값이 하한이다 → 그때는 고를 때의 결함이다 (production 은 이미
    스캔 최소가 더 좋으면 그것을 쓰므로, 이 경우가 나오면 그 자체가 발견이다).
  · 스캔이 거의 **평평**하다 (RMSE 변동이 값에 비해 작다) → γ 가 이 자료에서 식별되지 않는 것이고,
    사전 적합 값을 초기값으로 쓰든 말든 5 파라미터 적합은 같은 곳에 앉는다 (§12-5 가 실측한 그것).

2026-09-15 합성 실측 — 어떤 손상이 어떤 서명을 내는가 (`tests/test_cycles.py::test_cy_12`):

  대조군(정상)            γ 0.2256  RMSE 2.8e-05     ← 참값 0.224 를 되찾는다
  Si 용량축 뒤집힘         γ 0.0769  RMSE 5.04        ← RMSE 가 5 자리 튄다
  Gr 용량축 뒤집힘         γ 0.1897  RMSE 4.30        ← 같음
  Si·Gr 역할 교환         γ 0.5000  RMSE 1.07        ← **상**한에 붙는다
  측정 전압 구간이 좁다     γ 0.5000  RMSE 0.400       ← **상**한에 붙는다

**넷 중 어느 것도 "하한 0.02 · RMSE 0.47" 을 내지 않는다.** 그래서 §13-5 의 세 의심(문헌 곡선 방향
규약 · 반쪽전지 선택 · 재정규화 구간) 중 **방향 규약은 이 서명과 안 맞는다** — 뒤집히면 RMSE 가
훨씬 크게 튄다. 남는 둘을 이 스크립트의 출력이 가른다.

이 스크립트는 **읽기만 한다** — 게시하지 않고 산출도 안 만든다. 종료 코드: 0 정상 · 2 입력 문제.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
REPO_DIR = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(REPO_DIR))
from bms_balancing import data as D          # noqa: E402
from bms_balancing import model as M         # noqa: E402


def measured_dvdq_rms(ne_c, ne_v, si_c, si_v, gr_c, gr_v, window: int = 9, poly_order: int = 1) -> float:
    """측정 dV/dQ **자신의** RMS — "아무것도 예측하지 않는" 모델의 RMSE 다.

    왜 필요한가: RMSE 0.47 이 큰지 작은지는 **그것만 보면 모른다.** 합성 대조군은 6.5e-4 이고 실데이터는
    0.47~0.50 이다 — 세 자릿수 차이인데, 자가 없으면 "하한에 붙었다" 만 보이고 "어디서도 안 맞는다" 는
    안 보인다. 비율이 1 에 가까우면 그 γ 는 **잘 맞는 값이 아니라 덜 나쁜 값**이다.

    ⚠ `fit_gamma_si` 의 전처리를 그대로 따라간다 (같은 공통 구간 · 같은 1000 점 · 같은 재정규화 ·
      같은 `differential` 인자). 한쪽만 바뀌면 이 자가 조용히 틀려지므로 회귀가 둘을 같이 건다.
    """
    ne_v2, ne_c2 = M._unique_first(np.asarray(ne_v, float), np.asarray(ne_c, float))
    si_v2, _ = M._unique_first(np.asarray(si_v, float), np.asarray(si_c, float))
    gr_v2, _ = M._unique_first(np.asarray(gr_v, float), np.asarray(gr_c, float))
    v_common = np.linspace(max(ne_v2.min(), si_v2.min(), gr_v2.min()),
                           min(ne_v2.max(), si_v2.max(), gr_v2.max()), 1000)
    q = M._pchip(ne_v2, ne_c2, v_common)
    q = (q - q.min()) / (q.max() - q.min())
    return float(np.sqrt(np.mean(M.differential(q, v_common, window, poly_order).dvdq ** 2)))


def band(scan, rmse, tol: float) -> tuple[float, float, int]:
    """RMSE ≤ 최소·(1+tol) 인 γ 의 **바깥 범위**와 그 점 수 — 폭 작업의 `--width-tol` 과 같은 자다.

    왜 필요한가: 적합값 하나를 보면 "γ = 0.28" 이지만, 그 둘레가 평평하면 **그 값은 자료가 정한 것이
    아니다.** 눈으로 스캔을 보고 "평평해 보인다" 고 말하면 그 판단은 문서에만 있는 주장이 된다 —
    기계가 세게 한다. 격자 위의 값이므로 이 띠도 **하한**이다 (격자 사이는 안 본다).
    """
    lim = float(np.min(rmse)) * (1.0 + float(tol))
    hits = np.asarray(scan, float)[np.asarray(rmse, float) <= lim]
    return float(hits.min()), float(hits.max()), int(hits.size)


def _shape(scan, rmse) -> tuple[str, str]:
    """스캔의 모양 → (판정, 한 줄 설명). **여기서 값을 고치지 않는다 — 읽기만 한다.**"""
    j = int(np.argmin(rmse))
    rel = float((rmse.max() - rmse.min()) / max(abs(rmse.min()), 1e-30))
    if rel < 0.01:
        return ("FLAT", f"스캔 전체의 RMSE 변동이 최소값 대비 {rel:.3%} — γ 가 이 자료에서 식별되지 않는다")
    if j == 0:
        return ("MONOTONE_AT_LB", "최소가 **왼쪽 끝**이다 — 최적화 실패가 아니라 자료가 하한보다 작은 Si 를 "
                                  "원한다. 의심할 것은 optimizer 가 아니라 입력(반쪽전지 선택·문헌 곡선)이다")
    if j == len(scan) - 1:
        return ("MONOTONE_AT_UB", "최소가 **오른쪽 끝**이다 — 합성 실측에서 역할 교환·좁은 측정 구간이 "
                                  "이 서명을 냈다 (스크립트 머리말 표)")
    return ("INTERIOR", f"안쪽 최소가 있다 (γ≈{scan[j]:.4f}) — 보고값이 하한이면 그것 자체가 발견이다")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-root", default=None, help="data/literature 가 있는 루트 (없으면 BMS_DATA_ROOT)")
    ap.add_argument("--half-cell", required=True, type=pathlib.Path, help="기준(pristine) 반쪽전지 xlsx")
    ap.add_argument("--si-source", default="Li", help=f"정본 소스 하나, 또는 '{D.EXTERNAL_SI_SOURCE}'")
    ap.add_argument("--literature", default=None, type=pathlib.Path,
                    help=f"정본 로스터 밖 문헌 파일 — 주면 --si-source 는 '{D.EXTERNAL_SI_SOURCE}' 여야 한다")
    ap.add_argument("--gamma-lb", type=float, default=0.02, help="스캔 하한 (기본 0.02 = Track C)")
    ap.add_argument("--gamma-ub", type=float, default=0.5, help="스캔 상한 (기본 0.5)")
    ap.add_argument("--no-dv", action="store_true", help="dV/dQ 대신 Q(U) 로 맞춘다 (원본 use_dv=false)")
    ap.add_argument("--band-tol", type=float, default=0.01,
                    help="식별 띠의 허용 — 최소 RMSE 대비 분수 (기본 0.01 = 1%%). 폭 작업의 --width-tol 과 같은 자")
    ap.add_argument("--json", action="store_true", help="스캔 60 점을 JSON 으로도 찍는다")
    a = ap.parse_args(argv)

    if not a.half_cell.is_file():
        print(f"! 반쪽전지 파일이 없다: {a.half_cell}", file=sys.stderr); return 2
    try:
        root = D.data_root(a.data_root)
        lit_id: dict = {}
        if a.literature is not None:
            if a.si_source != D.EXTERNAL_SI_SOURCE:
                print(f"! --literature 를 주면 --si-source 는 '{D.EXTERNAL_SI_SOURCE}' 여야 한다", file=sys.stderr)
                return 2
            si_c, si_v, gr_c, gr_v = D.load_literature_file(a.literature, identity=lit_id)
        else:
            if a.si_source == D.EXTERNAL_SI_SOURCE:
                print("! --si-source external 인데 --literature 가 없다", file=sys.stderr); return 2
            si_c, si_v, gr_c, gr_v = D.load_literature(root, a.si_source, identity=lit_id)
        hb = D.read_input(a.half_cell)
        half = M.HalfCell(hb.stream(), window=11, poly_order=3)
    except Exception as e:                                   # noqa: BLE001
        print(f"! 입력을 못 읽었다 ({type(e).__name__}: {e})", file=sys.stderr); return 2

    ne_c, ne_v = half.ne_capacity, half.ne_voltage
    r = M.fit_gamma_si(ne_c, ne_v, si_c, si_v, gr_c, gr_v,
                       gamma_range=(a.gamma_lb, a.gamma_ub), use_dv=not a.no_dv)
    scan, rmse = np.asarray(r.gamma_scan, float), np.asarray(r.rmse_scan, float)
    verdict, why = _shape(scan, rmse)

    print(f"\n══ γ 사전 적합 진단 — 반쪽전지 {a.half_cell.name} · Si 소스 {a.si_source} "
          f"· {'Q(U)' if a.no_dv else 'dV/dQ'} ══")
    print(f"  보고값  γ = {r.gamma_Si_fit:.6f}   RMSE = {r.rmse:.6g}")
    print(f"  스캔    [{a.gamma_lb}, {a.gamma_ub}] 60 점 · 최소 γ = {scan[int(np.argmin(rmse))]:.6f} "
          f"· RMSE {rmse.min():.6g} ~ {rmse.max():.6g}")
    print(f"  판정    **{verdict}** — {why}")
    b_lo, b_hi, b_n = band(scan, rmse, a.band_tol)
    print(f"  식별 띠  RMSE ≤ 최소·(1+{a.band_tol:g}) 인 γ = [{b_lo:.4f}, {b_hi:.4f}]  "
          f"(폭 {b_hi - b_lo:.4f} · 격자 {b_n}/{len(scan)} 점)")
    rms0 = measured_dvdq_rms(ne_c, ne_v, si_c, si_v, gr_c, gr_v) if not a.no_dv else float("nan")
    if np.isfinite(rms0) and rms0 > 0:
        ratio = float(np.min(rmse)) / rms0
        print(f"  맞춤 정도  최소 RMSE {np.min(rmse):.6g} ÷ 측정 dV/dQ 자신의 RMS {rms0:.6g} = **{ratio:.3f}**")
        if ratio > 0.5:
            print("           → 1 에 가깝다. **어느 γ 에서도 안 맞는다** — 보고된 γ 는 잘 맞는 값이 아니라 "
                  "덜 나쁜 값이다. 끝에 붙었든 안쪽이든 그 값을 자료가 정한 값처럼 쓰지 않는다.")
    if b_hi - b_lo > 0.05:
        print("           → 이 띠가 넓다 — γ 는 **약하게만 식별된다.** 적합값 한 개를 자료가 정한 값처럼 "
              "쓰지 않는다 (§12-5 와 같은 결).")

    # 전압 구간은 세 곡선의 **교집합**이다 — 여기가 좁으면 상한에 붙는 서명이 나온다 (머리말 표)
    lo = max(float(np.min(ne_v)), float(np.min(si_v)), float(np.min(gr_v)))
    hi = min(float(np.max(ne_v)), float(np.max(si_v)), float(np.max(gr_v)))
    print(f"\n  전압 구간 (V)  측정 [{np.min(ne_v):.4f}, {np.max(ne_v):.4f}] · "
          f"Si [{np.min(si_v):.4f}, {np.max(si_v):.4f}] · Gr [{np.min(gr_v):.4f}, {np.max(gr_v):.4f}]")
    print(f"                 → 공통 [{lo:.4f}, {hi:.4f}]  (폭 {hi - lo:.4f} V)")

    step = max(1, len(scan) // 20)
    print("\n  스캔 (일부)")
    for i in range(0, len(scan), step):
        bar = "█" * int(40 * (rmse[i] - rmse.min()) / max(rmse.max() - rmse.min(), 1e-30))
        print(f"    γ {scan[i]:6.4f}  RMSE {rmse[i]:12.6g}  {bar}")
    if a.json:
        print("\nGAMMA_SCAN " + json.dumps(
            {"gamma_fit": r.gamma_Si_fit, "rmse": r.rmse, "verdict": verdict,
             "band_tol": a.band_tol, "band": [b_lo, b_hi], "band_n": b_n,
             "measured_dvdq_rms": rms0, "misfit_ratio": (float(np.min(rmse)) / rms0
                                                        if np.isfinite(rms0) and rms0 > 0 else None),
             "voltage_common": [lo, hi], "literature": lit_id,
             "scan": [[float(g), float(v)] for g, v in zip(scan, rmse)]}, ensure_ascii=False))

    print("\n  ⚠ 이 스크립트는 읽기만 한다 — 게시하지 않고 값을 고치지도 않는다.")
    print("  ⚠ γ 사전 적합은 **초기값**을 정할 뿐이다. §12-5 실측: γ 초기값을 0.25→0.02 로, 하한을 0→0.02 로")
    print("     바꿔도 5 파라미터 적합의 네 값이 표시 자리까지 같았다 — 이 항목은 LAM 결론을 바꾸지 않는다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
