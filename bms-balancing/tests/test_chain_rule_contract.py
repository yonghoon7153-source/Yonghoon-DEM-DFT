"""chain rule 계약 (⑥ · Codex R17 §4 답 · `R17_RESPONSE.md` §4) — `objective_version` 명시 선택 (2026-09-22).

`Objective.dv_cell` 은 `d/dx [E_PE((x−b)/a)]` 를 `dv_PE((x−b)/a)` 로 두어 **`1/a` 를 빠뜨렸다** (`FINDINGS.md` §1-2 —
원본 MATLAB 도 같으므로 포팅은 충실하고 결함은 그들 모델의 것이다). 리뷰어(R17 §4) 의 답: **수학적으로 고치되 충실
포팅은 명시 legacy 모드로 보존**하고, 신규 실행에 알려진 잘못된 미분을 침묵 기본값으로 권하지 않는다.

계약 — 이 파일이 RED 로 고정한다 (구현 전에는 전부 빨개야 한다):
  ① `Objective(..., objective_version=...)` 는 **필수 키워드**다 (기본값 없음). 값은 `legacy_matlab` | `chain_rule_v2`.
  ② `chain_rule_v2` 의 `dv_cell` 은 각 항을 `a_PE`·`a_NE` 로 나눈다 — analytic 항등식으로 확인 (a≠1 에서 legacy 는
     틀리고 v2 는 맞으며, a=1 대조군에서는 둘이 같다). "200 배" 같은 특정 optimizer 오차비는 계약이 아니다.
  ③ 값이 **행·sidecar·controls·비교기**에 실린다: `CYCLES_ROW`/`CYCLES_NON_NUMERIC`/`CYCLES_META_CONTROLS` 에 있고
     `check_rows` 가 빈 값·모르는 값을 거부하며 `width_report.COMPARED_SETTINGS` 가 견준다 (축으로 고르면 비교 가능,
     아니면 같아야 한다).
  ④ CLI `fit_cycles.py` 는 `--objective-version` 이 **필수**다.
  ⑤ 회수 정확도: 정답을 심은 합성 두 상태에서 v2 가 LAM/LLI 를 **절대 허용 안**으로 되찾는다 (복수 truth · 잡음 하나).
     legacy 의 오차는 **기록만** 한다 — 리뷰어 답 ②: 오차비를 계약으로 못 박지 않는다.
"""
from __future__ import annotations

import inspect
import pathlib
import subprocess
import sys

import numpy as np
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from bms_balancing import data as D, schema as S, verify as V                       # noqa: E402
from bms_balancing.model import LB5, UB5, Blend, HalfCell, Objective, degradation_modes  # noqa: E402
from test_r6_internal import _synth_root                                             # noqa: E402

VERSIONS = ("legacy_matlab", "chain_rule_v2")


# ── ① 필수 키워드 · 값 검사 ─────────────────────────────────────────────────────────────

def test_cr_01_objective_version_is_a_required_keyword_with_no_default():
    """[①] 침묵 기본값이 없다 — 부르는 쪽이 어느 미분을 쓰는지 **적어야** 한다."""
    prm = inspect.signature(Objective.__init__).parameters
    assert "objective_version" in prm, "Objective 에 objective_version 이 없다"
    assert prm["objective_version"].default is inspect.Parameter.empty, "기본값이 있다 — 침묵 선택이다"


def _synthetic_pair(tmp_path):
    src = _synth_root(tmp_path)
    half = HalfCell(src / "data/half_cell/GITT/pristine.xlsx")
    si_c, si_v, gr_c, gr_v = D.load_literature(src, "Li")
    return half, Blend(si_c, si_v, gr_c, gr_v)


def _e_true(half, blend, p, x):
    return half.E_PE((x - p[1]) / p[0]) - blend.E(np.atleast_1d((x - p[3]) / p[2]), p[4])


def test_cr_02_unknown_version_is_rejected_before_any_fit(tmp_path):
    """[①] 모르는 값은 생성 시점에 `ValueError` — 적합 뒤에 "어느 판이었나" 를 묻게 두지 않는다."""
    half, blend = _synthetic_pair(tmp_path)
    x = np.linspace(0.0, 1.0, 200)
    p = np.array([1.10, -0.06, 1.05, 0.00, 0.25])
    v = _e_true(half, blend, p, x)
    with pytest.raises(ValueError):
        Objective(half, blend, x * 70.0, v, w_pocv=1.0, w_dvdq=1.0, w_dqdv=0.0, objective_version="banana")
    for ver in VERSIONS:
        o = Objective(half, blend, x * 70.0, v, w_pocv=1.0, w_dvdq=1.0, w_dqdv=0.0, objective_version=ver)
        assert o.objective_version == ver


# ── ② analytic 항등식 (리뷰어 science_repro 그대로) ─────────────────────────────────────

class _Half:
    E_PE = staticmethod(lambda x: 3.0 + np.asarray(x) ** 2)
    dv_PE = staticmethod(lambda x: 2.0 * np.asarray(x))


class _Blend:
    E = staticmethod(lambda x, g: 0.2 + 0.3 * np.asarray(x) ** 2)
    dv = staticmethod(lambda x, g: 0.6 * np.asarray(x))


def _bare(version):
    o = Objective.__new__(Objective)
    o.half, o.blend, o.objective_version = _Half(), _Blend(), version
    return o


def _dv_error(o, p):
    x = np.linspace(0.2, 0.6, 101); h = 1e-6
    fd = (o.E_cell(p, x + h) - o.E_cell(p, x - h)) / (2 * h)
    return float(np.max(np.abs(fd - o.dv_cell(p, x))))


def test_cr_03_v2_matches_the_derivative_of_E_cell_and_legacy_does_not_when_a_is_not_one():
    """[②] a≠1: legacy 최대 오차 > 0.1 (리뷰어 실측 0.370833), v2 < 1e−8 (4.03e−10). a=1 대조군: 둘 다 < 1e−8."""
    p_a = np.array([0.8, 0.1, 1.2, -0.1, 0.2])            # a_PE=0.8 · a_NE=1.2
    p_1 = np.array([1.0, 0.1, 1.0, -0.1, 0.2])            # a=1 — 1/a 가 항등이라 두 판이 같아야 한다
    assert _dv_error(_bare("legacy_matlab"), p_a) > 0.1, "legacy 가 a≠1 에서 맞는다? — 이 시험의 전제가 틀렸다"
    assert _dv_error(_bare("chain_rule_v2"), p_a) < 1e-8
    assert _dv_error(_bare("legacy_matlab"), p_1) < 1e-8 and _dv_error(_bare("chain_rule_v2"), p_1) < 1e-8


# ── ③ 행 · sidecar · controls · 비교기 ─────────────────────────────────────────────────

def test_cr_05_the_version_rides_in_row_schema_controls_and_is_validated():
    """[③] 열·비숫자·controls 에 있고, `check_rows` 가 빈 값과 모르는 값을 거부한다."""
    assert "objective_version" in S.CYCLES_ROW
    assert "objective_version" in S.CYCLES_NON_NUMERIC
    assert "objective_version" in S.meta_controls("cycles"), "controls 에 없으면 두 판의 차이가 '설명 없는 숫자 변화' 로 나간다"
    from test_r17_codex import _base_row                   # noqa: PLC0415  — 완전한 production 행
    for ver in VERSIONS:
        row = dict(_base_row(), objective_version=ver)
        assert S.check_rows("cycles", [row], list(S.CYCLES_ROW), "cycles_syn.csv") == []
    for bad in ("", "banana", "1"):
        row = dict(_base_row(), objective_version=bad)
        assert S.check_rows("cycles", [row], list(S.CYCLES_ROW), "cycles_syn.csv"), f"{bad!r} 가 통과했다"


def test_cr_06_cli_requires_the_flag():
    """[④] `fit_cycles.py` 는 `--objective-version` 없이 돌지 않는다 (argparse 필수 인자 → rc 2)."""
    r = subprocess.run([sys.executable, str(ROOT / "scripts/fit_cycles.py")], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 2 and "objective-version" in r.stderr, r.stderr[-600:]


def test_cr_07_width_report_compares_the_version_like_any_other_setting(tmp_path):
    """[③] 두 판이 다르면 `--axis w_dqdv` 비교는 거부(rc 2)하고, `--axis objective_version` 으로 고르면 비교한다(rc 0)."""
    from test_widths import _fake_widths_csv, _report      # noqa: PLC0415
    a = _fake_widths_csv(tmp_path / "A", "cycles_syn_Li.csv", w_dqdv=0, objective_version="legacy_matlab")
    # 축(w_dqdv)은 정당하게 바뀌었는데 **판도 다르다** → 그 비교는 축 하나의 것이 아니다 → 거부, 무엇이 다른지 짚는다
    b = _fake_widths_csv(tmp_path / "B", "cycles_syn_Li.csv", w_dqdv=1, objective_version="chain_rule_v2")
    r = _report(a, b, "--axis", "w_dqdv")
    assert r.returncode == 2 and "objective_version" in r.stderr, (r.returncode, r.stderr[-500:])
    # 판 자체를 축으로 고르면 (다른 설정은 전부 같게) 두 판을 견줄 수 있다 — 이것이 A/B 비교의 정식 경로다
    c = _fake_widths_csv(tmp_path / "C", "cycles_syn_Li.csv", w_dqdv=0, objective_version="chain_rule_v2")
    r = _report(a, c, "--axis", "objective_version")
    assert r.returncode == 0, (r.returncode, r.stdout[-400:], r.stderr[-400:])
    assert "legacy_matlab" in r.stdout and "chain_rule_v2" in r.stdout, r.stdout[-600:]


# ── ⑤ 회수 정확도 (p2_modes.py 의 실험을 계약으로) ────────────────────────────────────

_TRUTHS = [
    # (p_ref, C_ref, p_age, C_age, noise_mV, tol_pp)
    pytest.param(np.array([1.10, -0.06, 1.05, 0.00, 0.25]), 70.0,
                 np.array([1.06, -0.09, 1.02, -0.02, 0.25]), 61.0, 0.0, 0.5, id="truth-A-noiseless"),
    pytest.param(np.array([1.20, -0.03, 1.10, 0.01, 0.30]), 68.0,
                 np.array([1.12, -0.07, 1.00, -0.03, 0.30]), 58.0, 0.0, 0.5, id="truth-B-noiseless"),
    pytest.param(np.array([1.10, -0.06, 1.05, 0.00, 0.25]), 70.0,
                 np.array([1.06, -0.09, 1.02, -0.02, 0.25]), 61.0, 1.0, 1.0, id="truth-A-1mV-noise"),
]


@pytest.mark.parametrize("p_ref,c_ref,p_age,c_age,noise_mv,tol_pp", _TRUTHS)
def test_cr_04_v2_recovers_injected_modes_within_tolerance_legacy_error_is_recorded_only(
        tmp_path, p_ref, c_ref, p_age, c_age, noise_mv, tol_pp):
    """[⑤] 정답을 심은 두 상태 → 두 판으로 적합 → 보고 LAM/LLI 를 정답과 댄다.

    v2 는 **절대 허용 안**(`tol_pp` %p)이어야 한다. legacy 의 오차는 **출력에 기록만** 한다 — 리뷰어 답 ②:
    특정 optimizer 의 오차비(우리 200 배 관측)는 환경 의존이라 계약으로 못 박지 않는다.
    """
    half, blend = _synthetic_pair(tmp_path)
    rng = np.random.default_rng(0)
    x = np.linspace(0.0, 1.0, 400)

    def make(p, c):
        v = _e_true(half, blend, p, x)
        assert v[0] < v[-1], "증가 분기 가정이 깨졌다"
        if noise_mv:
            v = v + rng.normal(0.0, noise_mv * 1e-3, v.shape)
        return x * c, v

    # ⚠ Codex R17 후속: 전 판은 `fit()` 안에서 `make()` 를 불렀다 — 그러면 버전 루프마다 RNG 를
    #   다시 소비해 legacy 와 v2 가 **서로 다른 잡음 실현**을 적합한다. v2 의 절대 허용 시험은
    #   그래도 유효하지만, 두 오차의 차이를 "한 축(1/a)의 효과" 로 읽을 수 없다. 입력 배열을
    #   **먼저 한 번 만들어 두 버전이 공유**한다.
    data = {"ref": make(p_ref, c_ref), "age": make(p_age, c_age)}

    def fit(version, which):
        cap, vol = data[which]
        o = Objective(half, blend, cap, vol, w_pocv=1.0, w_dvdq=1.0, w_dqdv=0.0, objective_version=version)
        best, val, _ = V.multistart(o, n_starts=6, seed=0, lb=LB5, ub=UB5)
        assert best is not None, f"{version}: 채택된 적합이 없다"
        return np.asarray(best, float)

    truth = degradation_modes(p_ref, c_ref, p_age, c_age)
    got = {}
    for ver in VERSIONS:
        a, b = fit(ver, "ref"), fit(ver, "age")
        got[ver] = degradation_modes(a, c_ref, b, c_age)
    err = {ver: {k: (got[ver][k] - truth[k]) * 100.0 for k in truth} for ver in VERSIONS}
    print("\n  회수 오차 (%p):", {v: {k: f"{e:+.4f}" for k, e in d.items()} for v, d in err.items()})   # legacy 는 기록만
    for k in ("LAM_PE", "LAM_NE", "LLI"):
        assert abs(err["chain_rule_v2"][k]) < tol_pp, f"v2 가 {k} 를 {tol_pp} %p 안에서 되찾지 못했다: {err['chain_rule_v2']}"
