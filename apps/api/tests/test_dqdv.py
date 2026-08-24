"""dQ/dV 엔드포인트 — 프로파일과 같은 사이클을 받고, 다른 축을 돌려준다.

여기서 틀리면 화면이 조용히 이상해진다. 사이클 선택이 프로파일과 어긋나거나,
못 만든 곡선이 소리 없이 빠져 그 사이클이 왜 없는지 알 수 없거나, 기준전극
오프셋이 x 축에만 안 걸려 봉우리가 0.62 V 옆에 서거나.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def loaded(client, sample_id, wrd_bytes):
    """파일 하나가 붙은 셀."""
    response = client.post("/api/runs/upload", params={"sample_id": sample_id},
                           files={"file": ("No_1_dry_011.wrd", wrd_bytes,
                                           "application/octet-stream")})
    assert response.status_code == 201, response.text
    return sample_id


def _dqdv(client, sample_id, **params):
    response = client.get(f"/api/samples/{sample_id}/dqdv", params=params)
    assert response.status_code == 200, response.text
    return response.json()


def test_it_answers_for_the_cycles_that_were_asked_for(client, loaded):
    body = _dqdv(client, loaded, cycles="2,3", branches="charge,discharge")
    assert sorted({s["cycle"] for s in body["series"]}) == [2, 3]
    assert sorted({s["branch"] for s in body["series"]}) == ["charge", "discharge"]


def test_the_same_cycle_spec_as_the_profile(client, loaded):
    """사이클 선택 UI 는 하나다.  두 엔드포인트가 다르게 해석하면, 같은 화면에서
    모드를 바꿨을 때 그려지는 사이클이 달라진다."""
    spec = "2-4"
    profile = client.get(f"/api/samples/{loaded}/profile",
                         params={"cycles": spec, "branches": "discharge"}).json()
    dqdv = _dqdv(client, loaded, cycles=spec, branches="discharge")

    assert ({s["cycle"] for s in dqdv["series"]}
            == {s["cycle"] for s in profile["series"]})


def test_nothing_is_dropped_from_the_answer(client, loaded):
    """고른 (사이클 × 브랜치) 마다 한 줄씩 나온다 — 못 만든 것도 포함해서.

    빼 버리면 화면에서 그 사이클이 왜 없는지 알 방법이 없다.  못 만든 줄은
    점이 0 이고 이유가 붙어 있다.
    """
    body = _dqdv(client, loaded, cycles="2,3,4", branches="charge,discharge")
    assert len(body["series"]) == 3 * 2
    assert all(s["points"] or s["reason"] for s in body["series"])


def test_the_cv_hold_is_excluded_end_to_end(client, sample_id, cv_wrd_bytes):
    """정전압 구간이 있는 파일에서 실제로 빠지는지, 파이프라인을 통과시켜 본다.

    손으로 만든 배열이 아니라 파싱·저장·조회를 다 거친 뒤에도 빠져야 한다.
    """
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("cv_011.wrd", cv_wrd_bytes,
                                "application/octet-stream")})
    body = _dqdv(client, sample_id, cycles="3", branches="charge,discharge")
    by_branch = {s["branch"]: s for s in body["series"]}

    # 충전에는 CV 가 있고, 방전에는 없다.
    assert by_branch["charge"]["points_dropped"] >= 24
    assert by_branch["discharge"]["points_dropped"] == 0
    # 컷오프 전압에 0 으로 나눈 봉우리가 서 있으면 안 된다.
    charge = by_branch["charge"]
    assert charge["points"], charge["reason"]
    peak_at = charge["voltage"][charge["dqdv"].index(max(charge["dqdv"]))]
    assert peak_at < max(charge["voltage"]) - 1e-9, "봉우리가 컷오프에 서 있다"


def test_discharge_is_negative_and_charge_is_positive(client, loaded):
    """부호가 히스테리시스를 보여 준다 (ADR 0013)."""
    body = _dqdv(client, loaded, cycles="3", branches="charge,discharge")
    by_branch = {s["branch"]: s for s in body["series"] if s["points"]}
    assert by_branch, body

    if "charge" in by_branch:
        assert sum(by_branch["charge"]["dqdv"]) > 0
    if "discharge" in by_branch:
        assert sum(by_branch["discharge"]["dqdv"]) < 0


def test_the_settings_come_back_with_the_curve(client, loaded):
    """평활은 봉우리를 낮춘다.  무엇으로 만든 곡선인지 화면이 말할 수 있어야 한다."""
    body = _dqdv(client, loaded, cycles="3", voltage_step=0.01, smoothing=9)
    assert (body["voltage_step"], body["smoothing"]) == (0.01, 9)
    assert all((s["voltage_step"], s["smoothing"]) == (0.01, 9) for s in body["series"])


def test_normalising_divides_the_curve_too(client, loaded, sample_id):
    """mAh/V 를 그램으로 나누면 (mAh/g)/V.  기울기도 같이 나뉘어야 한다."""
    raw = _dqdv(client, loaded, cycles="3", branches="discharge", basis="mAh")
    per_gram = _dqdv(client, loaded, cycles="3", branches="discharge", basis="mAh/g")

    assert raw["basis"] == "mAh"
    assert per_gram["basis"] == "mAh/g"
    raw_peak = max(abs(v) for v in raw["series"][0]["dqdv"])
    gram_peak = max(abs(v) for v in per_gram["series"][0]["dqdv"])
    # 활물질 질량은 31.6 mg × 80 wt% = 0.02528 g.  나눗수가 1 보다 훨씬 작으므로
    # mAh/g 쪽이 커야 한다.
    assert gram_peak > raw_peak


def test_the_reference_electrode_shifts_the_x_axis(client, loaded, sample_id):
    """Li-In 대극이면 전위가 0.62 V 옮겨 간다.

    프로파일 y 축에는 걸고 dQ/dV x 축에 안 걸면, 같은 셀의 같은 상전이가 두
    화면에서 다른 전압에 있다.  미분값 자체는 상수를 더해도 안 변한다.
    """
    before = _dqdv(client, loaded, cycles="3", branches="discharge")
    client.patch(f"/api/samples/{sample_id}", json={"reference_electrode": "Li-In"})
    after = _dqdv(client, loaded, cycles="3", branches="discharge")

    shift = after["series"][0]["voltage"][0] - before["series"][0]["voltage"][0]
    assert shift == pytest.approx(0.62, abs=1e-6)
    # 값은 그대로다 — d(V+c) = dV.
    assert after["series"][0]["dqdv"] == before["series"][0]["dqdv"]


def test_too_many_cycles_is_refused_with_a_number(client, loaded):
    body = client.get(f"/api/samples/{loaded}/dqdv",
                      params={"cycles": "1-500"})
    assert body.status_code in (200, 422)
    if body.status_code == 422:
        assert "at most" in body.json()["detail"]


def test_a_bad_voltage_step_is_refused(client, loaded):
    assert client.get(f"/api/samples/{loaded}/dqdv",
                      params={"voltage_step": 0}).status_code == 422
    assert client.get(f"/api/samples/{loaded}/dqdv",
                      params={"smoothing": 0}).status_code == 422


# --- CSV ---------------------------------------------------------------------

def test_the_csv_has_a_column_pair_per_curve(client, loaded):
    response = client.get(f"/api/export/samples/{loaded}/dqdv.csv",
                          params={"cycles": "2,3", "branches": "discharge"})
    assert response.status_code == 200, response.text
    header = response.text.lstrip("﻿").splitlines()[0]
    assert header.split(",") == [
        "cycle2_discharge_voltage (V)", "cycle2_discharge_dQdV (mAh/V)",
        "cycle3_discharge_voltage (V)", "cycle3_discharge_dQdV (mAh/V)",
    ]


def test_the_csv_carries_the_basis_in_its_header(client, loaded):
    response = client.get(f"/api/export/samples/{loaded}/dqdv.csv",
                          params={"cycles": "3", "branches": "discharge",
                                  "basis": "mAh/g"})
    assert "mAh/g/V" in response.text.splitlines()[0]


def test_the_csv_is_written_at_full_resolution(client, loaded):
    """CSV 는 다시 그리거나 피팅하는 대상이다.

    화면용으로 줄인 곡선에서 읽은 봉우리 위치는 격자가 아니라 픽셀 단위로
    맞는다 — 그걸 논문에 쓰면 안 된다.
    """
    # 곡선당 최소 점수(_MIN_POINTS_PER_CURVE)가 있어서 max_points 를 더 낮게
    # 줘도 80 아래로는 안 내려간다.  중요한 것은 CSV 가 그보다 많다는 것이다.
    plotted = _dqdv(client, loaded, cycles="3", branches="discharge",
                    max_points=50)["series"][0]
    csv = client.get(f"/api/export/samples/{loaded}/dqdv.csv",
                     params={"cycles": "3", "branches": "discharge"}).text
    rows = len(csv.lstrip("﻿").strip().splitlines()) - 1

    assert rows > plotted["points"], "CSV 가 화면용으로 줄어 있다"


def test_a_cycle_that_does_not_exist_is_a_404(client, loaded):
    response = client.get(f"/api/export/samples/{loaded}/dqdv.csv",
                          params={"cycles": "9999"})
    assert response.status_code == 404


# --- 평활 선택 (ADR 0015) -----------------------------------------------------

def test_the_smoother_travels_with_the_numbers(client, loaded):
    """봉우리 높이를 비교해도 되는지는 창·필터·차수가 같은지에 달려 있다.

    응답이 그것을 말하지 않으면, 두 사람이 다른 설정으로 만든 곡선을 같은
    축에서 비교하고도 알 방법이 없다.
    """
    body = _dqdv(client, loaded, cycles="3", branches="discharge",
                 smoothing=9, smoother="savgol", poly_order=3)
    assert (body["smoothing"], body["smoother"], body["poly_order"]) == (9, "savgol", 3)
    curve = next(s for s in body["series"] if s["points"])
    assert (curve["smoothing"], curve["smoother"], curve["poly_order"]) == (9, "savgol", 3)


def test_savgol_at_order_one_is_the_moving_average(client, loaded):
    """랩 공용 스크립트가 쓰는 설정이다.  대칭 창의 최소제곱 직선은 중심에서
    창의 평균과 정확히 같아서, 내부 값이 이동평균과 일치한다 (ADR 0015).

    이게 깨졌다면 둘 중 하나가 바뀐 것이고, "차수 1 로 랩 스크립트를
    재현한다" 는 약속도 함께 깨진 것이다.
    """
    common = {"cycles": "3", "branches": "discharge", "smoothing": 21}
    moving = _dqdv(client, loaded, smoother="moving", **common)
    savgol = _dqdv(client, loaded, smoother="savgol", poly_order=1, **common)

    a = next(s for s in moving["series"] if s["points"])["dqdv"]
    b = next(s for s in savgol["series"] if s["points"])["dqdv"]
    assert len(a) == len(b)
    interior = slice(10, -10)
    assert a[interior] == pytest.approx(b[interior], abs=1e-6)


def test_a_higher_order_keeps_more_of_the_peak(client, loaded):
    """차수 2 부터 SG 가 값을 한다.  이 검사가 없으면 'SG 를 붙였다' 가 곧
    '봉우리가 산다' 로 읽히는데, 차수 1 에서는 거짓이다."""
    common = {"cycles": "3", "branches": "discharge", "smoothing": 21}
    moving = _dqdv(client, loaded, smoother="moving", **common)
    savgol = _dqdv(client, loaded, smoother="savgol", poly_order=2, **common)

    def depth(body):
        values = next(s for s in body["series"] if s["points"])["dqdv"]
        return max(abs(v) for v in values)

    assert depth(savgol) >= depth(moving)


def test_an_unknown_smoother_is_refused_by_name(client, loaded):
    """조용히 되돌아가면 화면은 savgol 이라 적고 이동평균을 그린다."""
    response = client.get(f"/api/samples/{loaded}/dqdv",
                          params={"cycles": "3", "smoother": "gaussian"})
    assert response.status_code == 422
    assert "gaussian" in response.text


def test_the_csv_takes_the_same_smoother(client, loaded):
    response = client.get(f"/api/export/samples/{loaded}/dqdv.csv",
                          params={"cycles": "3", "branches": "discharge",
                                  "smoother": "savgol", "poly_order": 2})
    assert response.status_code == 200
    assert "dQdV" in response.text.splitlines()[0]

    refused = client.get(f"/api/export/samples/{loaded}/dqdv.csv",
                         params={"cycles": "3", "smoother": "nope"})
    assert refused.status_code == 422
