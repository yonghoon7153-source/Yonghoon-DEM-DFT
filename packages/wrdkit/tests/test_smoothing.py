"""평활 — 정의로부터 검증한다.

Savitzky-Golay 는 "창 안의 점들에 최소제곱으로 다항식을 맞추고 그 중심값을
취하는 것" 이다. 그 정의에서 검사 두 개가 곧바로 나오고, 둘 다 통과하지 않으면
구현이 틀린 것이다.

1. 차수 이하의 다항식은 **그대로** 나와야 한다 (맞출 것이 이미 다항식이므로).
2. 창 5·차수 2 의 계수는 교과서 값 (-3, 12, 17, 12, -3)/35 여야 한다.

여기에 이 저장소에만 있는 사실 하나를 더 고정한다: **차수 1 의 SG 는 내부에서
이동평균과 완전히 같다.** 대칭 창에서 1차 항이 홀함수라 상쇄되기 때문이다.
랩 공용 스크립트가 `polyorder=1` 을 쓰므로, 그 스크립트의 "Smoothed" 곡선은
21점 이동평균이다. 이 사실이 코드에서 사라지면 "SG 로 바꿨으니 봉우리가
살아났겠지" 라는 잘못된 안심이 생긴다.
"""

from __future__ import annotations

import numpy as np
import pytest

from wrdkit.ica import (
    DEFAULT_POLY_ORDER,
    LAB_SCRIPT_POLY_ORDER,
    LAB_SCRIPT_WINDOW,
    SMOOTHERS,
    _savgol,
    smooth,
)


def _gaussian(n=401, centre=2.0, width=0.08, span=4.0):
    x = np.linspace(0.0, span, n)
    return x, np.exp(-((x - centre) ** 2) / (2 * width**2))


# --- 정의대로인가 ------------------------------------------------------------

@pytest.mark.parametrize("order", [0, 1, 2, 3, 4])
def test_a_polynomial_of_that_order_passes_through_untouched(order):
    """차수 이하의 다항식은 손대지 않는다 — SG 의 정의가 그것이다."""
    i = np.arange(61, dtype=float)
    coeffs = [1.5, -0.3, 0.02, -4e-4, 3e-6][: order + 1]
    poly = sum(c * i**k for k, c in enumerate(coeffs))
    out = smooth(poly, 21, method="savgol", poly_order=order)
    assert np.abs(out - poly).max() < 1e-9


def test_the_kernel_is_the_textbook_one():
    """창 5·차수 2 → (-3, 12, 17, 12, -3)/35. 임펄스를 넣으면 커널이 나온다."""
    impulse = np.zeros(41)
    impulse[20] = 1.0
    kernel = _savgol(impulse, 5, 2)[18:23]
    assert np.allclose(kernel * 35, [-3, 12, 17, 12, -3])


def test_order_one_is_a_moving_average_in_disguise():
    """랩 스크립트가 쓰는 설정이 실제로 무엇인지 고정한다.

    이게 깨지면 SG 구현이 바뀐 것이거나 이동평균이 바뀐 것이다. 어느 쪽이든
    "차수 1 로 랩 스크립트를 재현한다" 는 문서의 약속이 깨진 것이다.
    """
    _, y = _gaussian()
    sg = smooth(y, LAB_SCRIPT_WINDOW, method="savgol",
                poly_order=LAB_SCRIPT_POLY_ORDER)
    mv = smooth(y, LAB_SCRIPT_WINDOW, method="moving")
    half = LAB_SCRIPT_WINDOW // 2
    assert np.allclose(sg[half:-half], mv[half:-half], atol=1e-12)


def test_order_two_is_where_savgol_starts_paying_for_itself():
    """차수를 올리면 같은 창에서 봉우리를 덜 깎는다.

    문서(ADR 0015)가 숫자로 약속한 것이라 숫자로 지킨다. 이 검사가 없으면
    "SG 를 붙였다" 가 곧 "봉우리가 산다" 로 읽히는데, 차수 1 에서는 거짓이다.
    """
    _, y = _gaussian()
    mv = smooth(y, 21, method="moving").max()
    sg2 = smooth(y, 21, method="savgol", poly_order=2).max()
    assert mv < 0.80          # 이동평균은 1.00 → 0.77 로 깎는다
    assert sg2 > 0.95         # 2차는 0.98 근처를 지킨다
    assert sg2 > mv


def test_the_default_order_is_the_one_that_helps():
    """기본값이 조용히 1 로 되돌아가면 SG 를 고른 의미가 없어진다."""
    assert DEFAULT_POLY_ORDER >= 2


# --- 봉우리 위치는 답이다 ----------------------------------------------------

@pytest.mark.parametrize("method,order", [("moving", 2), ("savgol", 1),
                                          ("savgol", 2), ("savgol", 3)])
def test_no_smoother_moves_the_peak(method, order):
    """봉우리 *위치* 가 곧 답인 분석이다. 어떤 평활도 그것을 옮기면 안 된다."""
    x, y = _gaussian()
    out = smooth(y, 21, method=method, poly_order=order)
    assert abs(x[int(out.argmax())] - x[int(y.argmax())]) < 1e-9


def test_savgol_does_not_flatten_a_sloped_end():
    """끝단을 반사로 채우면 기울기가 0 이 된다 — 컷오프 전압이 있는 자리다.

    dQ/dV 곡선의 양 끝은 사람이 "셀이 컷오프까지 갔는가" 를 보는 곳이라,
    거기서 곡선이 눕는 것은 없는 사실을 만드는 것이다.
    """
    ramp = 3.0 * np.arange(40, dtype=float)
    sg = smooth(ramp, 11, method="savgol", poly_order=1)
    mv = smooth(ramp, 11, method="moving")
    assert np.allclose(sg, ramp)              # 직선은 직선으로
    assert abs(mv[-1] - ramp[-1]) > 1.0       # 이동평균은 끝을 끌어내린다


# --- 부서지지 않는가 ---------------------------------------------------------

def test_a_window_wider_than_the_data_is_narrowed_not_fatal():
    values = np.arange(4, dtype=float)
    assert np.allclose(smooth(values, 21, method="savgol", poly_order=1), values)


def test_an_even_window_is_made_odd():
    """짝수 창은 결과를 반 칸 민다. 봉우리 위치가 답이므로 공짜가 아니다."""
    values = np.arange(10, dtype=float)
    assert np.allclose(smooth(values, 6, method="savgol", poly_order=1), values)


def test_a_window_that_cannot_support_the_order_drops_the_order():
    """창보다 높은 차수를 요구해도 죽지 않는다 — 차수를 창에 맞춰 낮춘다.

    낮춘 결과가 **항등이 되는 것이 옳다**: 창 3 은 차수 2 까지 담을 수 있고,
    3점을 지나는 2차 곡선은 하나뿐이라 그 점들을 정확히 통과한다. 낮추지
    않으면 설계행렬이 rank-deficient 가 되어 경고나 쓰레기 값이 나온다.
    평활이 실제로 일어나는 것은 차수가 창보다 충분히 낮을 때다 (아래).
    """
    rng = np.random.default_rng(0)
    values = rng.normal(size=30)
    out = smooth(values, 3, method="savgol", poly_order=5)
    assert np.all(np.isfinite(out))
    assert np.allclose(out, values)          # 3점 · 2차 = 정확히 통과

    # 차수가 창보다 낮아지는 순간부터 실제로 평활된다.
    smoothed = smooth(values, 9, method="savgol", poly_order=2)
    assert np.all(np.isfinite(smoothed))
    assert not np.allclose(smoothed, values)
    assert smoothed.std() < values.std()


def test_an_empty_array_survives():
    assert len(smooth(np.empty(0), 21, method="savgol", poly_order=2)) == 0


def test_an_unknown_smoother_is_refused_by_name():
    with pytest.raises(ValueError, match="unknown smoother"):
        smooth(np.arange(10.0), 5, method="gaussian")


def test_the_smoother_names_are_the_ones_the_api_offers():
    assert SMOOTHERS == ("moving", "savgol")
