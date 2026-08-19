"""savgol 행렬 캐시가 scipy와 **같은 값**을 주는지 (F22).

이건 속도 최적화지 근사가 아니다. 값이 달라지면 지금까지의 모든 결과와
비교가 깨지므로, 기계 정밀도로 고정한다.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.signal import savgol_filter

import src.objective as O


@pytest.fixture(autouse=True)
def _clear_cache():
    O._SMOOTH_KERNEL.clear()
    yield
    O._SMOOTH_KERNEL.clear()


@pytest.mark.parametrize("n", [23, 51, 100, 298, 299, 300])
@pytest.mark.parametrize("window,polyorder", [(21, 3), (11, 2), (31, 4)])
def test_matrix_smoothing_matches_scipy(n, window, polyorder):
    rng = np.random.default_rng(n * 7 + window)
    y = np.cumsum(rng.normal(size=n))

    got = O._smooth(y, window, polyorder)
    # _smooth의 창 보정 규칙을 그대로 재현해 scipy 기준값을 만든다
    w = min(window, n if n % 2 else n - 1)
    if w % 2 == 0:
        w -= 1
    want = y if w <= polyorder + 1 else savgol_filter(y, w, polyorder)

    assert got.shape == want.shape
    scale = max(float(np.ptp(want)), 1.0)
    assert np.max(np.abs(got - want)) < 1e-11 * scale


def test_kernel_is_shared_across_lengths():
    """★ 가장자리 연산자는 n에 의존하지 않는다 — 길이가 달라도 캐시는 하나."""
    rng = np.random.default_rng(0)
    for n in (120, 200, 299, 300):
        O._smooth(np.cumsum(rng.normal(size=n)), 21, 3)
    assert len(O._SMOOTH_KERNEL) == 1, "길이마다 커널을 새로 만들었다"
    O._smooth(np.cumsum(rng.normal(size=200)), 11, 2)
    assert len(O._SMOOTH_KERNEL) == 2, "(창,차수)가 다르면 별도 커널이어야 한다"


def test_kernel_memory_is_small():
    """조밀 n×n(698 KB)이 아니라 띠(수 KB)여야 한다 — 대역폭이 병목이므로."""
    O._smooth(np.cumsum(np.random.default_rng(0).normal(size=299)), 21, 3)
    coef, top, bot, _ = next(iter(O._SMOOTH_KERNEL.values()))
    total = coef.nbytes + top.nbytes + bot.nbytes
    assert total < 20_000, f"커널이 {total}바이트 — 띠 구조가 깨졌다"


def test_linearity_holds():
    """선형 연산자이므로 M(a·y1 + y2) == a·M(y1) + M(y2) 여야 한다."""
    rng = np.random.default_rng(3)
    y1, y2 = rng.normal(size=200), rng.normal(size=200)
    lhs = O._smooth(2.5 * y1 + y2, 21, 3)
    rhs = 2.5 * O._smooth(y1, 21, 3) + O._smooth(y2, 21, 3)
    assert np.allclose(lhs, rhs, atol=1e-12)


def test_can_be_disabled_and_matches_scipy(monkeypatch):
    """캐시를 끄면 scipy 경로로 가고 값은 그대로여야 한다 (동등성 검증용 스위치)."""
    monkeypatch.setattr(O, "_SMOOTH_CACHE_ENABLED", False)
    y = np.cumsum(np.random.default_rng(1).normal(size=150))
    got = O._smooth(y, 21, 3)
    assert not O._SMOOTH_KERNEL, "꺼져 있는데 커널을 만들었다"
    assert np.allclose(got, savgol_filter(y, 21, 3), atol=1e-12)


def test_short_signal_returns_unchanged():
    y = np.arange(4.0)
    assert np.array_equal(O._smooth(y, 21, 3), y)


@pytest.mark.parametrize("n", [60, 299])
def test_features_identical_to_scipy_path(n, monkeypatch):
    """★ 실제 사용 경로(compute_features)에서 두 구현이 같은 값을 내는가."""
    cfg = {"dqdv": {"window": 21, "polyorder": 3}}
    x = np.linspace(0, 1, n)
    v = 4.2 - 1.5 * x + 0.05 * np.sin(18 * x)

    fast = O.compute_features(x, v, cfg, with_peaks=True)
    O._SMOOTH_KERNEL.clear()
    monkeypatch.setattr(O, "_SMOOTH_CACHE_ENABLED", False)   # scipy 경로 강제
    slow = O.compute_features(x, v, cfg, with_peaks=True)

    for name in ("dvdq", "dqdv"):
        a, b = getattr(fast, name), getattr(slow, name)
        m = np.isfinite(a) & np.isfinite(b)
        assert np.array_equal(np.isfinite(a), np.isfinite(b)), f"{name} NaN 위치가 다름"
        assert np.max(np.abs(a[m] - b[m])) < 1e-9 * max(float(np.ptp(b[m])), 1.0)


# ── OCP 모델 오차 민감도 (한계 4) ──────────────────────────────────────────
#
# ★ 이 연구의 결론 전체가 "half-cell OCP 함수가 정확하다" 는 가정 위에 있다.
#   합성 truth 를 만든 바로 그 OCP 로 fit 했기 때문이다. 실측에서는 우리 모델과
#   실제 전극이 어긋나고, 어긋난 만큼 half-cell 기준의 우위가 깎인다. 그래서
#   기준 곡선에만 계통 왜곡을 넣을 수 있어야 한다 — truth 는 그대로 두고.
#
#   왜곡을 `ocp` recipe 에 끼우면 기존 v4 half-cell 묶음의 recipe_hash 가 바뀌어
#   검증이 깨진다. **별도 method `ocpbias`** 로 둬서 기존 identity 를 건드리지
#   않는다.

def _base_cfg():
    from src.config import load_config
    return load_config("configs/base.yaml")


def test_ocpbias_is_a_separate_method_leaving_ocp_untouched():
    """★ 기존 `ocp` recipe 는 한 글자도 안 바뀌어야 한다 (v4 묶음 보호)."""
    from src.halfcell import RECIPE_DEFAULTS

    assert RECIPE_DEFAULTS["ocp"] == {"n_points": 400, "branch": "delithiation"}
    assert "ocpbias" in RECIPE_DEFAULTS
    for k in ("pe_offset_mv", "ne_offset_mv", "pe_stretch", "ne_stretch"):
        assert k in RECIPE_DEFAULTS["ocpbias"], k


def test_ocpbias_with_zero_perturbation_equals_ocp():
    """★ 왜곡 0 이면 `ocp` 와 **배열이 같아야** 한다 (엄밀한 일반화)."""
    import numpy as np
    from src.halfcell import compute_halfcell_from_ocp

    cfg = _base_cfg()
    a = compute_halfcell_from_ocp(cfg, n_points=64)
    b = compute_halfcell_from_ocp(cfg, n_points=64, pe_offset_mv=0.0,
                                  ne_offset_mv=0.0, pe_stretch=1.0,
                                  ne_stretch=1.0)
    for k in ("y_pe", "u_pe", "z_ne", "u_ne"):
        np.testing.assert_allclose(getattr(a, k), getattr(b, k), rtol=0, atol=0)


def test_ocpbias_offset_shifts_voltage_and_stretch_remaps_it():
    """★ 두 왜곡이 각각 의도한 대로 움직여야 한다.

    ★ 갱신 — stretch 의 표현을 바꿨다. 예전에는 화학량론 **축을 잘라서**
      `y_pe.max()` 가 줄었고 `u_pe` 는 그대로였다. 그 표현은 전 범위 coverage
      전제(F11)와 충돌해 1% 넘는 왜곡을 못 쟀다. 지금은 정의역을 유지하고
      전압을 재매핑한다 — 축은 불변, 값이 바뀐다 (아래 stretch 절 참조).
    """
    import numpy as np
    from src.halfcell import compute_halfcell_from_ocp

    cfg = _base_cfg()
    a = compute_halfcell_from_ocp(cfg, n_points=64)
    off = compute_halfcell_from_ocp(cfg, n_points=64, pe_offset_mv=10.0)
    np.testing.assert_allclose(off.u_pe, a.u_pe + 0.010, atol=1e-12)
    np.testing.assert_allclose(off.u_ne, a.u_ne, atol=1e-12)

    st = compute_halfcell_from_ocp(cfg, n_points=64, pe_stretch=0.95)
    np.testing.assert_allclose(st.y_pe, a.y_pe, rtol=0, atol=0)   # 축 불변
    assert not np.allclose(st.u_pe, a.u_pe), "PE 전압이 재매핑되지 않았다"
    np.testing.assert_allclose(st.u_ne, a.u_ne, atol=1e-12)       # NE 는 불변


def test_ocpbias_perturbation_changes_the_cache_key():
    """★ 왜곡은 recipe 서명에 들어가야 한다 — 다른 캐시 파일이 되어야 한다."""
    from src.halfcell import halfcell_cache_path, recipe_hash

    cfg = _base_cfg()
    h0 = recipe_hash(cfg, "ocpbias")
    h1 = recipe_hash(cfg, "ocpbias", pe_offset_mv=10.0)
    assert h0 != h1, "왜곡이 recipe 해시에 안 들어갔다"
    assert halfcell_cache_path(cfg, None, "ocpbias") \
        != halfcell_cache_path(cfg, None, "ocpbias", pe_offset_mv=10.0)


def test_ocpbias_rejects_unknown_perturbation_args():
    """★ 모르는 인자는 조용히 무시되면 안 된다 (서명 밖 변수)."""
    import pytest as _pt
    from src.halfcell import recipe_of

    with _pt.raises(ValueError, match="모르는 인자"):
        recipe_of("ocpbias", pe_offset_volt=0.01)


def test_ocpbias_method_name_matches_the_sealed_cache_pattern():
    """★ hessian 의 봉인 staging 정규식이 `[a-z]+` 라 밑줄이 들어가면 안 된다."""
    import re

    assert re.fullmatch(r"[a-z]+", "ocpbias"), "method 이름에 밑줄·숫자 금지"


def test_halfcell_cli_exposes_the_bias_knobs():
    """★ 왜곡을 라이브러리에만 넣고 CLI 에 안 붙이면 쓸 수가 없다.

    실측: `python -m src.halfcell --method ocpbias --pe-offset-mv 10` 이
    "알 수 없는 인자" 로 죽어 민감도 스윕 8회분이 통째로 헛돌았다.
    """
    import subprocess
    import sys as _s
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    out = subprocess.run([_s.executable, "-m", "src.halfcell", "--help"],
                         cwd=root, capture_output=True, text=True).stdout
    for flag in ("--pe-offset-mv", "--ne-offset-mv", "--pe-stretch", "--ne-stretch"):
        assert flag in out, f"{flag} 가 CLI 에 없다\n{out}"
    assert "ocpbias" in out, "method 선택지에 ocpbias 가 없다"


def test_run_sh_passes_halfcell_method_to_fit():
    """★ run.sh 가 --halfcell-method 를 fit 까지 넘겨야 한다.

    src/fitting.py 는 이미 인자를 받는데 run.sh 가 안 받아서, 왜곡 기준으로
    fit 을 돌릴 방법이 없었다 (실측: "알 수 없는 인자: --halfcell-method").
    """
    import subprocess
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    r = subprocess.run(
        ["bash", "run.sh", "--mode", "fit", "--in", "results/x", "--out", "results/y",
         "--reference", "halfcell", "--halfcell-method", "ocpbias"],
        cwd=root, capture_output=True, text=True,
        env={**__import__("os").environ, "RUN_SH_DRY": "1"})
    assert r.returncode == 0, r.stdout + r.stderr
    assert "--halfcell-method ocpbias" in r.stdout, r.stdout


def test_fitting_cli_accepts_ocpbias_method():
    """★ M39 로 발견 — run.sh dry-run 은 src.fitting 을 안 태운다.

    run.sh 가 `--halfcell-method ocpbias` 를 조립해도 fitting.py 의 choices 에
    ocpbias 가 없으면 실행 순간 죽는다. 실측으로 그랬다:
      fitting.py: error: argument --halfcell-method: invalid choice: 'ocpbias'
    dry-run 테스트만으로는 이 층이 안 잡혀서 별도로 고정한다.
    """
    import subprocess
    import sys as _s
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    out = subprocess.run([_s.executable, "-m", "src.fitting", "--help"],
                         cwd=root, capture_output=True, text=True).stdout
    assert "ocpbias" in out, f"fitting CLI 가 ocpbias 를 안 받는다\n{out}"


# ── 왜곡 값이 **fit 까지** 가야 한다 (배선 2차 구멍) ────────────────────────
#
# ★ CLI 를 붙인 직후 경로를 손으로 따라가 발견. fitting 은 half-cell 캐시
#   경로를 `halfcell_cache_path(base_cfg, method=halfcell_method)` 로 —
#   **왜곡 인자 없이** — 계산한다 (src/fitting.py:591·711). 그런데 왜곡은
#   recipe_hash 에 들어가므로 경로를 바꾼다. 따라서
#   `--method ocpbias --pe-offset-mv 10` 으로 만든 캐시는 fitting 이 절대
#   들여다보지 않는 파일이 되고, fitting 은 왜곡 0 인 기본 ocpbias 경로를 읽는다.
#
#   실패 방식이 최악이다: 대조(0mV)를 먼저 돌려 기본 경로를 채워두면 이후
#   **모든** 왜곡 실행이 그 대조 캐시를 읽어 민감도 0 을 보고한다. 스윕 전체가
#   "모델 오차는 이 결론을 안 흔든다" 는 거짓말이 되고, 파일·해시·서명은 전부
#   정합하므로 F74 도 안 울린다.
#
#   막는 방법 두 가지를 같이 넣는다.
#     (a) 왜곡 값을 fit 까지 관통시킨다 (`--halfcell-arg k=v`).
#     (b) 왜곡 없는 ocpbias 는 `ocp` 와 배열이 같으므로 **쓸 이유가 없다** —
#         기본값 그대로의 ocpbias 는 양쪽에서 거절한다. 그러면 (a) 를 잊었을 때
#         조용히 대조를 읽는 대신 멈춘다. 대조는 `--method ocp` 로 돌린다.

def test_fitting_cli_takes_the_perturbation_values():
    """★ (a) — fit 쪽에 왜곡 값을 넘길 문법이 있어야 한다."""
    import subprocess
    import sys as _s
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    out = subprocess.run([_s.executable, "-m", "src.fitting", "--help"],
                         cwd=root, capture_output=True, text=True).stdout
    assert "--halfcell-arg" in out, f"왜곡 값을 fit 에 넘길 방법이 없다\n{out}"


def test_halfcell_kw_from_cli_selects_the_perturbed_cache_path():
    """★ (a) 의 핵심 — 파싱된 값이 **다른 캐시 경로**를 골라야 한다.

    이게 깨지면 fitting 이 대조 캐시를 읽고 민감도 0 을 보고한다.
    """
    from src.fitting import parse_halfcell_kw
    from src.halfcell import halfcell_cache_path

    kw = parse_halfcell_kw(["pe_offset_mv=10", "pe_stretch=0.97"])
    assert kw == {"pe_offset_mv": 10.0, "pe_stretch": 0.97}, kw

    cfg = _base_cfg()
    assert halfcell_cache_path(cfg, None, "ocpbias", **kw) \
        != halfcell_cache_path(cfg, None, "ocpbias"), \
        "왜곡 값이 경로에 반영되지 않았다 — fitting 이 대조 캐시를 읽는다"


def test_parse_halfcell_kw_rejects_malformed_and_unknown_keys():
    """★ 조용히 무시되는 오타는 '왜곡을 줬다고 믿는' 실행을 만든다."""
    import pytest as _pt

    from src.fitting import parse_halfcell_kw

    with _pt.raises(SystemExit):
        parse_halfcell_kw(["pe_offset_mv"])          # = 없음
    with _pt.raises(SystemExit):
        parse_halfcell_kw(["pe_offset_mv=abc"])      # 숫자 아님
    with _pt.raises(SystemExit):
        parse_halfcell_kw(["pe_offset_volts=1"])     # recipe 에 없는 키


def test_fitting_refuses_ocpbias_without_perturbation_values():
    """★ (b) — 왜곡 없는 ocpbias 로 fit 하려 하면 **입력을 보기도 전에** 멈춘다."""
    import subprocess
    import sys as _s
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    r = subprocess.run(
        [_s.executable, "-m", "src.fitting", "--in", "results/__nonexistent__",
         "--reference", "halfcell", "--halfcell-method", "ocpbias"],
        cwd=root, capture_output=True, text=True)
    assert r.returncode != 0
    both = r.stdout + r.stderr
    assert "--halfcell-arg" in both, f"거절 이유가 왜곡 값 누락이 아니다\n{both}"


def test_run_sh_passes_halfcell_arg_to_fit():
    """★ (a) — run.sh 도 관통시켜야 한다. 여러 개를 줄 수 있어야 한다."""
    import os as _os
    import subprocess
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    r = subprocess.run(
        ["bash", "run.sh", "--mode", "fit", "--in", "results/x", "--out", "results/y",
         "--reference", "halfcell", "--halfcell-method", "ocpbias",
         "--halfcell-arg", "pe_offset_mv=10", "--halfcell-arg", "pe_stretch=0.97"],
        cwd=root, capture_output=True, text=True,
        env={**_os.environ, "RUN_SH_DRY": "1"})
    assert r.returncode == 0, r.stdout + r.stderr
    assert "--halfcell-arg pe_offset_mv=10" in r.stdout, r.stdout
    assert "--halfcell-arg pe_stretch=0.97" in r.stdout, r.stdout


def test_halfcell_cli_refuses_a_no_op_ocpbias_cache():
    """★ (b) 의 나머지 절반 — 대조 캐시를 **애초에 만들지 못하게** 한다.

    기본값 그대로의 ocpbias 캐시가 디스크에 없으면, (a) 를 잊은 fit 은 캐시
    부재로 F63 에 걸려 멈춘다. 즉 함정의 미끼 자체를 없앤다.
    """
    import subprocess
    import sys as _s
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    for extra in ([], ["--pe-offset-mv", "0", "--pe-stretch", "1.0"]):
        r = subprocess.run(
            [_s.executable, "-m", "src.halfcell", "--config", "configs/base.yaml",
             "--method", "ocpbias", *extra],
            cwd=root, capture_output=True, text=True)
        assert r.returncode != 0, f"왜곡 0 인 ocpbias 가 통과했다 (extra={extra})"
        assert "ocp" in (r.stdout + r.stderr)


def test_fitting_looks_up_the_perturbed_cache_path(tmp_path):
    """★ 위 두 테스트가 못 잡는 층 — **fitting 안에서** 경로를 계산하는 곳.

    변이 시험(M40)으로 확인: `halfcell_cache_path(..., **halfcell_kw)` 에서
    kwargs 를 빼도 위의 경로 테스트들은 전부 통과한다. 그 상태가 바로 왜곡을
    줬는데 왜곡 0 캐시를 읽는 실행이다. 여기서는 캐시가 없을 때 F63 이 부르는
    **경로 이름**으로 fitting 이 무엇을 찾았는지 못 박는다.
    """
    import pytest as _pt

    import src.fitting as F
    from src.halfcell import halfcell_cache_path

    cfg = _base_cfg()
    kw = {"pe_offset_mv": 10.0}
    want = halfcell_cache_path(cfg, None, "ocpbias", **kw)
    plain = halfcell_cache_path(cfg, None, "ocpbias")
    assert want.name != plain.name

    from tests.test_fitting import _tiny_curves
    in_dir = _tiny_curves(tmp_path / "in", n=16, n_cond=2)

    # F63(캐시 없음)이 경로를 말해주게 하려면 두 경로 모두 **없어야** 한다.
    # 있으면 밀어두고 끝나면 되돌린다 — 저장소 .cache 를 건드리지 않는다.
    moved = []
    for q in (want, plain, want.with_name(want.stem + ".meta.yaml"),
              plain.with_name(plain.stem + ".meta.yaml")):
        if q.exists():
            b = q.with_suffix(q.suffix + ".pytest-aside")
            q.rename(b)
            moved.append((b, q))

    try:
        _run_and_check(F, in_dir, tmp_path, kw, want, plain)
    finally:
        for b, q in moved:
            b.rename(q)


def _run_and_check(F, in_dir, tmp_path, kw, want, plain):
    import pytest as _pt

    with _pt.raises(RuntimeError) as e:
        F.run_fit(in_dir, tmp_path / "out",
                  {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                              "peak_weight": 1.0},
                   "scaling": {"method": "reference_rmse"}},
                  {"a": {"w_pocv": 1.0}},
                  {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
                   "ub": [2.0, 1.0, 2.0, 1.0]},
                  "expanded", 1, nproc=1, reference="halfcell",
                  halfcell_method="ocpbias", halfcell_kw=kw)
    msg = str(e.value)
    assert want.name in msg, f"왜곡 캐시를 안 찾았다\n{msg}"
    assert plain.name not in msg, f"왜곡 0 캐시를 찾고 있다\n{msg}"


# ── 배선 3차 구멍 + 값 수준 거절 (13차 자체 리뷰) ──────────────────────────
#
# ★ (1) run.sh `all` 모드는 half-cell 플래그를 **조용히 버렸다**. top-level
#   파서는 받아들이므로 오류가 없고, 하위 fit 은 method 기본값 ocp 로 기존
#   무왜곡 캐시를 읽어 **끝까지 성공**한다 — 어느 가드에도 안 걸린다.
#   실측(RUN_SH_DRY): `--mode all ... --halfcell-method ocpbias --halfcell-arg
#   pe_offset_mv=10` 의 하위 fit 명령에 두 플래그가 없었다. 10시간짜리 본
#   실행을 "민감도를 쟀다" 고 믿으며 왜곡 0 으로 태울 수 있는 경로다.
#   기존 회귀는 fit 모드만 고정해서 이 층을 못 봤다.
#
# ★ (2) 왜곡 0 거절이 **형식**만 봤다 — `not halfcell_kw` 는 빈 dict 만 잡는다.
#   `--halfcell-arg pe_offset_mv=0` 은 통과하고, recipe 는 기본값과 같아져
#   왜곡 0 캐시를 읽는다. `for mv in 0 5 10 20` 스타일 스윕의 첫 다리가 바로
#   이 형태다. 값 수준으로 — recipe 기본값과 합쳐 **실효 왜곡이 0 이면** 거절.

def test_run_sh_all_mode_passes_halfcell_flags_to_the_fit_step():
    """★ (1) — all 모드의 하위 fit 명령에도 두 플래그가 있어야 한다."""
    import os as _os
    import subprocess
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    r = subprocess.run(
        ["bash", "run.sh", "--mode", "all", "--out", "results/x",
         "--reference", "halfcell", "--halfcell-method", "ocpbias",
         "--halfcell-arg", "pe_offset_mv=10"],
        cwd=root, capture_output=True, text=True,
        env={**_os.environ, "RUN_SH_DRY": "1"})
    assert r.returncode == 0, r.stdout + r.stderr
    fit_line = [ln for ln in r.stdout.splitlines() if "--mode fit" in ln]
    assert fit_line, f"dry-run 에 fit 명령이 없다\n{r.stdout}"
    assert "--halfcell-method ocpbias" in fit_line[0], fit_line[0]
    assert "--halfcell-arg pe_offset_mv=10" in fit_line[0], fit_line[0]


def test_fitting_refuses_an_effectively_zero_perturbation():
    """★ (2) — 명시적 0 도 거절해야 한다 (값 수준 판정)."""
    import subprocess
    import sys as _s
    from pathlib import Path as _P

    root = _P(__file__).resolve().parent.parent
    for arg in ("pe_offset_mv=0", "pe_stretch=1.0"):
        r = subprocess.run(
            [_s.executable, "-m", "src.fitting", "--in", "results/__nonexistent__",
             "--reference", "halfcell", "--halfcell-method", "ocpbias",
             "--halfcell-arg", arg],
            cwd=root, capture_output=True, text=True)
        assert r.returncode != 0, f"{arg} 가 통과했다"
        both = r.stdout + r.stderr
        assert "ocp" in both, f"{arg}: 거절 사유가 왜곡 0 이 아니다\n{both}"


def test_halfcell_library_refuses_to_build_a_zero_perturbation_cache(tmp_path):
    """★ (2) 의 나머지 — 미끼 생성 거절이 CLI 에만 있으면 라이브러리로 뚫린다.

    실측: `get_halfcell_reference(cfg, method="ocpbias")` 가 왜곡 0 캐시를
    거절 없이 만들었다. 그 미끼가 있으면 명시적 0 fit 이 끝까지 완주한다.
    """
    import pytest as _pt

    from src.halfcell import get_halfcell_reference

    cfg = _base_cfg()
    with _pt.raises(ValueError, match="왜곡"):
        get_halfcell_reference(cfg, cache_dir=tmp_path, method="ocpbias",
                               force=True)
    # 왜곡이 있으면 정상 생성된다 (음성 대조)
    ref = get_halfcell_reference(cfg, cache_dir=tmp_path, method="ocpbias",
                                 force=True, pe_offset_mv=10.0)
    assert ref.u_pe is not None


def test_verify_failure_message_names_the_actual_cause():
    """★ --verify 실패 사유가 구조검사인지 배열 불일치인지 구분해야 한다.

    실측(당시 stretch 0.97): `구조검사_실패: ["전범위_coverage"]`·
    `재생성_배열일치: true` 인데 메시지는 "캐시가 recipe 재생성 결과와 다르다"
    였다 — 배열은 같은데 다르다고 말해 원인을 엉뚱한 데서 찾게 했다.

    ★ 그 재현 경로(stretch)는 이제 사라졌다 — stretch 가 정의역을 안 자르므로
      coverage 를 깨지 않는다. 사유 판정을 순수 함수로 빼서 직접 고정한다.
    """
    from src.halfcell import verify_failure_reason

    # ① 배열이 다르면 그렇게 말한다
    assert "재생성 결과와 다르다" in verify_failure_reason([], False)
    # ② 배열은 같고 구조검사만 실패하면 **구조검사**라고 말한다
    why = verify_failure_reason(["전범위_coverage"], True)
    assert "재생성 결과와 다르다" not in why, why
    assert "전범위_coverage" in why, why
    assert "F11" in why and "sim" in why, f"원인·대처 안내가 없다\n{why}"
    # ③ 배열 불일치가 구조검사 실패를 가리지 않는다 (우선순위)
    assert "재생성 결과와 다르다" in verify_failure_reason(["전범위_coverage"], False)


# ── stretch 축을 실제로 잴 수 있게 한다 (13차 자체 리뷰 R7 후속) ──────────
#
# ★ 예전 구현은 화학량론 **정의역을 잘랐다**: `x = clip(x*s, 0, 1)`. s<1 이면
#   y_pe 최대가 0.9999·s 가 되어 전 범위 coverage 검사(≥0.99)에 걸린다. 쓸 수
#   있는 창이 `s ≥ 0.9901`(≈1% 이내)뿐이라, "실측에서 가장 큰 오차원" 이라 부른
#   축을 1% 넘게 흔들 수 없었다 — 준비 단계는 성공하고 fit 에서 죽는다.
#
#   coverage 전제(F11 — LLI 환산식은 전 범위 테이블에서만 성립)는 옳다. 틀린
#   것은 왜곡의 표현이었다. stoichiometry window 오차의 물리는 "정의역이
#   줄어든다"가 아니라 **"같은 z 에서 우리 모델이 다른 전압을 준다"** 이다:
#       U_biased(y) = U(clip(y·s, 0, 1))
#   정의역 [0,1] 은 그대로 두고 값만 재매핑한다. coverage 는 유지되고 왜곡
#   크기에 제한이 없다.

def test_stretch_keeps_the_full_range_domain():
    """★ stretch 가 정의역을 자르면 안 된다 — coverage 는 왜곡과 무관해야."""
    import numpy as np

    from src.halfcell import compute_halfcell_from_ocp

    base = compute_halfcell_from_ocp(_base_cfg(), n_points=64)
    for s in (0.90, 0.97, 1.03, 1.10):
        r = compute_halfcell_from_ocp(_base_cfg(), n_points=64, pe_stretch=s)
        np.testing.assert_allclose(r.y_pe, base.y_pe, rtol=0, atol=0)
        assert r.y_pe.max() >= 0.99, f"pe_stretch={s} 가 정의역을 잘랐다"
        n = compute_halfcell_from_ocp(_base_cfg(), n_points=64, ne_stretch=s)
        assert n.z_ne.max() >= 0.99, f"ne_stretch={s} 가 정의역을 잘랐다"


def test_stretch_remaps_the_voltage_not_the_axis():
    """★ 그러면서도 곡선은 실제로 바뀌어야 한다 (무왜곡과 같으면 무의미)."""
    import numpy as np

    from src.halfcell import compute_halfcell_from_ocp

    base = compute_halfcell_from_ocp(_base_cfg(), n_points=256)
    st = compute_halfcell_from_ocp(_base_cfg(), n_points=256, pe_stretch=0.90)
    assert not np.allclose(st.u_pe, base.u_pe), "pe_stretch 가 아무것도 안 했다"
    # U_biased(y) == U(y·s) — 중간 지점에서 직접 대조
    y = 0.5
    want = float(np.interp(y * 0.90, base.y_pe, base.u_pe))
    got = float(np.interp(y, st.y_pe, st.u_pe))
    assert abs(got - want) < 2e-3, f"재매핑이 U(y·s) 가 아니다: {got} vs {want}"

    ne = compute_halfcell_from_ocp(_base_cfg(), n_points=256, ne_stretch=0.90)
    assert not np.allclose(ne.u_ne, base.u_ne), "ne_stretch 가 아무것도 안 했다"


def test_stretch_one_is_bit_identical_to_no_stretch():
    """★ s=1.0 은 불변이어야 한다 — 기존 오프셋 다리의 재현성이 걸려 있다.

    §7.10 의 여섯 다리는 recipe 에 `pe_stretch: 1.0` 을 갖고 있다. 이 구현
    변경이 s=1 경로를 건드리면 그 캐시들이 다른 배열이 되어 재현이 깨진다.
    """
    import numpy as np

    from src.halfcell import compute_halfcell_from_ocp

    a = compute_halfcell_from_ocp(_base_cfg(), n_points=128)
    b = compute_halfcell_from_ocp(_base_cfg(), n_points=128,
                                  pe_stretch=1.0, ne_stretch=1.0)
    for k in ("y_pe", "u_pe", "z_ne", "u_ne"):
        np.testing.assert_allclose(getattr(a, k), getattr(b, k), rtol=0, atol=0)


def test_stretch_survives_the_cache_validator():
    """★ 끝까지 — 왜곡 캐시가 F74 구조검사(전범위 coverage)를 통과해야 한다."""
    from src.halfcell import get_halfcell_reference, validate_halfcell_cache
    from src.halfcell import halfcell_cache_path

    cfg = _base_cfg()
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        get_halfcell_reference(cfg, cache_dir=d, method="ocpbias", force=True,
                               pe_stretch=0.90)
        path = halfcell_cache_path(cfg, d, "ocpbias", pe_stretch=0.90)
        v = validate_halfcell_cache(cfg, path)
        assert v["ok"], f"stretch 0.90 캐시가 검증에 걸렸다: {v['fail']}"
