"""P3 시험 — (a) truth 패치 동치 · (b) γ0 고정 F5 목적값 = F4 목적값. 진단 전용.

승인 문서 `followups/phantom-pocv/P3_APPROVAL_REQUEST.md` §2 "시험 먼저 (RED → GREEN)".
환경변수:
  P3_COPY        저장소 밖 사본의 degradation-degeneracy 경로 (패치 대상)
  P3_REPO_MODES  저장소의 원래 src/modes.py (읽기만 · 기준값)
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import numpy as np
import pytest

COPY = Path(os.environ["P3_COPY"]).resolve()
REPO_MODES = Path(os.environ["P3_REPO_MODES"]).resolve()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(COPY))
sys.path.insert(0, str(HERE))

from src.baseline import DischargedState  # noqa: E402
from src.config import load_config  # noqa: E402
from src.modes import (P_NE1_INIT, P_NE1_VF, P_NE2_INIT, P_NE2_VF,  # noqa: E402
                       P_NE_POR, Baseline, build_overrides)

CFG = load_config(COPY / "configs" / "base.yaml")
B = Baseline.from_config(CFG)
# 대수 시험용 완방 농도 (물리 값이 아니어도 된다 — 원래 함수와 같은 입력이면 충분)
D = DischargedState(ne_primary=36.7, ne_secondary=3446.3, pe=58439.9)
GUARDS = CFG.get("guards", {})

CASES = [
    (0.0, 0.0, 0.0, "de", "de"),
    (0.05, 0.05, 0.05, "de", "de"),
    (0.15, 0.15, 0.15, "de", "de"),
    (0.10, 0.05, 0.20, "li", "li"),
    (0.17, 0.13, 0.13, "de", "li"),
]


def _orig():
    m = sys.modules.get("p3_modes_orig")
    if m is None:
        spec = importlib.util.spec_from_file_location("p3_modes_orig", REPO_MODES)
        m = importlib.util.module_from_spec(spec)
        sys.modules["p3_modes_orig"] = m      # dataclass 가 sys.modules 로 자기 모듈을 찾는다 (01_red 의 시험 결함)
        spec.loader.exec_module(m)
    return m.build_overrides


@pytest.mark.parametrize("case", CASES)
def test_a1_default_path_unchanged(case):
    lli, lpe, lne, tpe, tne = case
    assert build_overrides(lli, lpe, lne, tpe, tne, B, D, GUARDS) == \
        _orig()(lli, lpe, lne, tpe, tne, B, D, GUARDS)


@pytest.mark.parametrize("case", CASES)
def test_a2_equal_split_is_identical(case):
    lli, lpe, lne, tpe, tne = case
    got = build_overrides(lli, lpe, lne, tpe, tne, B, D, GUARDS, lam_gr=lne, lam_si=lne)
    assert got == _orig()(lli, lpe, lne, tpe, tne, B, D, GUARDS)


def test_a3_split_per_phase():
    lli, lpe, lgr, lsi = 0.05, 0.05, 0.05, 0.60
    lne_tot = 0.1408                      # 기록용 값 — 분리 경로에서는 vf 에 쓰이지 않는다
    ov = build_overrides(lli, lpe, lne_tot, "de", "de", B, D, GUARDS, lam_gr=lgr, lam_si=lsi)
    assert ov[P_NE1_VF] == pytest.approx(B.ne_primary_vf * (1 - lgr), rel=1e-14)
    assert ov[P_NE2_VF] == pytest.approx(B.ne_secondary_vf * (1 - lsi), rel=1e-14)
    assert ov[P_NE_POR] == pytest.approx(
        B.ne_porosity + B.ne_primary_vf * lgr + B.ne_secondary_vf * lsi, rel=1e-14)
    assert ov[P_NE1_INIT] == pytest.approx(D.ne_primary / (1 - lgr) * (1 - lli), rel=1e-14)
    assert ov[P_NE2_INIT] == pytest.approx(D.ne_secondary / (1 - lsi) * (1 - lli), rel=1e-14)


def test_a4_half_split_rejected():
    with pytest.raises(ValueError):
        build_overrides(0.05, 0.05, 0.05, "de", "de", B, D, GUARDS, lam_gr=0.05)


# ---------------------------------------------------------------- (b)

def _b_setup():
    import p3_fit5 as P
    from src.halfcell import compute_halfcell_from_ocp
    from src.fitting import build_reference_interps, reconstruct, window_shortfall
    from src.objective import compute_features, default_scales, make_objective

    obj_cfg = load_config(COPY / "configs" / "objectives.yaml")
    hc = compute_halfcell_from_ocp(CFG, n_points=400, branch="delithiation").as_dict()
    ref_pe, ref_ne4 = build_reference_interps("halfcell", None, hc)
    tab = P.ne_blend_tables(CFG, branch="delithiation", n_points=400)
    return P, obj_cfg, hc, ref_pe, ref_ne4, tab, reconstruct, window_shortfall, \
        compute_features, default_scales, make_objective


def test_b1_gamma0_matches_f4():
    (P, obj_cfg, hc, ref_pe, ref_ne4, tab, reconstruct, window_shortfall,
     compute_features, default_scales, make_objective) = _b_setup()
    g0 = P.gamma0(CFG)
    ref_ne5 = P.ne_ref_interp(tab, g0)
    s = np.linspace(0.0, 1.0, 2001)
    assert np.max(np.abs(ref_ne5(s) - ref_ne4(s))) < 1e-9

    x = np.linspace(0.0, 1.0, 300)
    p_trues = ([1.05, -0.05, 1.40, -0.40], [1.10, -0.08, 1.35, -0.30], [1.00, -0.03, 1.45, -0.45])
    _, _, v_ref = reconstruct(p_trues[0], ref_pe, ref_ne4, x)
    scales = default_scales(compute_features(x, v_ref, obj_cfg))
    n_checked = 0
    for p_true in p_trues:
        _, _, v_t = reconstruct(p_true, ref_pe, ref_ne4, x)
        target = compute_features(x, v_t, obj_cfg, with_peaks=True)
        obs = np.isfinite(target.v)
        lo, hi = float(x[obs].min()), float(x[obs].max())
        for name in ("pocv", "pocv_dvdq"):
            w = obj_cfg["objectives"][name]
            j4 = make_objective(target, lambda p: (x, reconstruct(p, ref_pe, ref_ne4, x)[2]),
                                w, scales, obj_cfg, lambda p: window_shortfall(p, lo, hi))
            j5 = P.make_j5(target, ref_pe, tab, x, w, scales, obj_cfg, lo, hi)
            for dp in ([0, 0, 0, 0], [0.01, -0.01, 0.02, 0.01], [-0.02, 0.01, -0.03, 0.02]):
                p = list(np.add(p_true, dp))
                a, b = j4(p), j5(p + [g0])
                assert abs(a - b) <= 1e-12 * max(1.0, abs(a)), (name, p_true, dp, a, b)
                n_checked += 1
    assert n_checked == 18


def test_b2_gamma_actually_moves_j():
    """음성 대조 — γ 가 목적값을 실제로 바꾸지 않으면 (b1) 은 공허하다."""
    (P, obj_cfg, hc, ref_pe, ref_ne4, tab, reconstruct, window_shortfall,
     compute_features, default_scales, make_objective) = _b_setup()
    g0 = P.gamma0(CFG)
    x = np.linspace(0.0, 1.0, 300)
    p_true = [1.05, -0.05, 1.40, -0.40]
    _, _, v_t = reconstruct(p_true, ref_pe, ref_ne4, x)
    target = compute_features(x, v_t, obj_cfg, with_peaks=True)
    scales = default_scales(compute_features(x, v_t, obj_cfg))
    j5 = P.make_j5(target, ref_pe, tab, x, obj_cfg["objectives"]["pocv"], scales, obj_cfg, 0.0, 1.0)
    assert j5(p_true + [g0]) < 1e-12
    assert j5(p_true + [g0 + 0.02]) > 1e-6
