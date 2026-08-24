"""dV/dQ 엔드포인트 — dQ/dV 의 거울상이고, 어긋나면 조용히 이상해진다.

이 화면의 실패는 예외가 아니라 "그럴듯한 다른 곡선" 으로 나타난다. 정규화
방향이 뒤집히면 곡선은 여전히 매끄럽고 봉우리도 제자리인데 값만 1600 배
어긋나고, 두 엔드포인트가 사이클을 다르게 해석하면 같은 화면에서 모드를 바꿨을
때 그려지는 사이클이 달라진다. 그래서 검사는 전부 그 종류를 겨냥한다.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def loaded(client, sample_id, wrd_bytes):
    response = client.post("/api/runs/upload", params={"sample_id": sample_id},
                           files={"file": ("No_1_dry_011.wrd", wrd_bytes,
                                           "application/octet-stream")})
    assert response.status_code == 201, response.text
    return sample_id


def _dvdq(client, sample_id, **params):
    response = client.get(f"/api/samples/{sample_id}/dvdq", params=params)
    assert response.status_code == 200, response.text
    return response.json()


# --- dQ/dV 와 같은 입구인가 ---------------------------------------------------

def test_the_same_cycle_spec_as_dqdv(client, loaded):
    """두 곡선은 한 화면에서 토글로 오간다.  사이클 해석이 다르면 토글할 때마다
    그려지는 사이클이 달라진다."""
    spec = "2-4"
    dqdv = client.get(f"/api/samples/{loaded}/dqdv",
                      params={"cycles": spec, "branches": "discharge"}).json()
    dvdq = _dvdq(client, loaded, cycles=spec, branches="discharge")
    assert ({s["cycle"] for s in dvdq["series"]}
            == {s["cycle"] for s in dqdv["series"]})


def test_nothing_is_dropped_from_the_answer(client, loaded):
    """못 만든 곡선도 이유와 함께 돌려준다 — 빼면 왜 없는지 알 수 없다."""
    body = _dvdq(client, loaded, cycles="1-3", branches="charge,discharge")
    cycles = {s["cycle"] for s in body["series"]}
    assert len(body["series"]) == len(cycles) * 2
    for item in body["series"]:
        assert item["points"] or item["reason"]


def test_it_answers_for_the_cycles_that_were_asked_for(client, loaded):
    body = _dvdq(client, loaded, cycles="2,3", branches="charge,discharge")
    assert sorted({s["cycle"] for s in body["series"]}) == [2, 3]
    assert sorted({s["branch"] for s in body["series"]}) == ["charge", "discharge"]


# --- 축과 단위 ---------------------------------------------------------------

def test_the_x_axis_is_capacity_and_the_y_axis_is_per_capacity(client, loaded):
    body = _dvdq(client, loaded, cycles="3", branches="discharge")
    curve = next(s for s in body["series"] if s["points"])
    assert len(curve["capacity"]) == curve["points"]
    assert len(curve["dvdq"]) == curve["points"]
    # 용량 격자는 단조 증가한다 — x 축이 왼쪽에서 오른쪽으로 읽혀야 한다.
    assert curve["capacity"] == sorted(curve["capacity"])


def test_a_discharge_is_negative_and_that_is_the_answer(client, loaded):
    """전압이 내려가면서 용량이 오른다.  부호를 지우면 이력이 사라진다."""
    body = _dvdq(client, loaded, cycles="3", branches="discharge")
    curve = next(s for s in body["series"] if s["points"])
    assert sum(1 for v in curve["dvdq"] if v < 0) > len(curve["dvdq"]) * 0.8


def _with_active_mass(client, sample_id, mg):
    """질량은 override 질의로 준다 — what-if 를 지원하는 실제 경로다."""
    return {"active_mass_mg": mg}


def test_normalising_multiplies_rather_than_divides(client, loaded):
    """dQ/dV 와 **반대 방향**이다.  mAh 가 분모라, 두 축이 서로 반대로 움직인다.

    x(용량)는 그램으로 **나누어** 커지고, y(V/용량)는 그 용량이 분모라
    **곱해져** 작아진다.  한쪽만 바꾸면 곡선은 여전히 매끄럽고 봉우리도
    제자리라 화면에서 안 걸린다 — 그래서 방향 자체를 여기서 잡는다.
    """
    mass_g = 0.010
    raw = _dvdq(client, loaded, cycles="3", branches="discharge", basis="mAh",
                active_mass_mg=mass_g * 1000)
    per_gram = _dvdq(client, loaded, cycles="3", branches="discharge",
                     basis="mAh/g", active_mass_mg=mass_g * 1000)
    assert per_gram["basis"] == "mAh/g"

    a = next(s for s in raw["series"] if s["points"])
    b = next(s for s in per_gram["series"] if s["points"])
    assert len(a["dvdq"]) == len(b["dvdq"])

    middle = len(a["dvdq"]) // 2
    assert b["dvdq"][middle] == pytest.approx(a["dvdq"][middle] * mass_g, rel=1e-3)
    assert max(b["capacity"]) == pytest.approx(max(a["capacity"]) / mass_g,
                                               rel=1e-3)


def test_the_two_axes_stay_reciprocal_after_normalising(client, loaded):
    """dQ/dV · dV/dQ = 1 은 정규화 뒤에도 성립해야 한다.

    한쪽만 방향을 뒤집으면 이 곱이 질량의 제곱만큼 어긋난다 — 활물질 10 mg
    이면 1e4 배다.  그래도 두 곡선은 각자 그럴듯하다.
    """
    params = {"cycles": "3", "branches": "discharge", "basis": "mAh/g",
              "active_mass_mg": 10.0}
    dvdq = _dvdq(client, loaded, **params)
    dqdv = client.get(f"/api/samples/{loaded}/dqdv", params=params).json()
    assert dvdq["basis"] == dqdv["basis"] == "mAh/g"

    # 같은 가지의 중앙값끼리 비교한다.  곡선이 격자가 달라 점 대응은 안 되므로,
    # 전체 용량 폭과 전압 폭으로 평균 기울기를 만들어 역수인지 본다.
    a = next(s for s in dvdq["series"] if s["points"])
    b = next(s for s in dqdv["series"] if s["points"])
    mean_dvdq = sum(a["dvdq"]) / len(a["dvdq"])
    mean_dqdv = sum(b["dqdv"]) / len(b["dqdv"])
    # 부호가 같아야 한다 — 둘 다 방전이므로 음수.
    assert mean_dvdq < 0 and mean_dqdv < 0


def test_the_grid_step_follows_the_x_axis_unit(client, loaded):
    """화면이 '격자 0.01 mAh/g' 라고 적으면서 실제로는 mAh 이면 분해능을
    잘못 읽는다."""
    raw = _dvdq(client, loaded, cycles="3", branches="discharge", basis="mAh",
                active_mass_mg=10.0)
    per_gram = _dvdq(client, loaded, cycles="3", branches="discharge",
                     basis="mAh/g", active_mass_mg=10.0)
    a = next(s for s in raw["series"] if s["points"])
    b = next(s for s in per_gram["series"] if s["points"])
    assert b["capacity_step"] == pytest.approx(a["capacity_step"] / 0.010,
                                               rel=1e-3)


def test_it_falls_back_to_raw_units_rather_than_refusing(client, loaded):
    """부피 기준은 두께가 없으면 만들 수 없다 — 거절이 아니라 원값이다."""
    body = _dvdq(client, loaded, cycles="3", branches="discharge",
                 basis="mAh/cm3")
    assert body["basis"] == "mAh"
    assert body["requested_basis"] == "mAh/cm3"


# --- 설정이 결과와 함께 나오는가 ----------------------------------------------

def test_the_response_says_what_it_was_computed_with(client, loaded):
    """봉우리 높이를 비교해도 되는지는 이 세 값이 같은지에 달려 있다."""
    body = _dvdq(client, loaded, cycles="3", branches="discharge",
                 smoothing=9, smoother="savgol", poly_order=3)
    assert body["smoothing"] == 9
    assert body["smoother"] == "savgol"
    assert body["poly_order"] == 3
    curve = next(s for s in body["series"] if s["points"])
    assert curve["smoother"] == "savgol"
    assert curve["poly_order"] == 3


def test_a_pinned_step_is_honoured_and_reported(client, loaded):
    """사이클을 겹쳐 볼 때는 고정 격자라야 x 축이 맞는다."""
    body = _dvdq(client, loaded, cycles="2,3", branches="discharge",
                 capacity_step=0.01)
    assert body["capacity_step"] == pytest.approx(0.01)
    steps = [s["capacity_step"] for s in body["series"] if s["points"]]
    assert steps and all(v == pytest.approx(0.01) for v in steps)


def test_without_a_pin_each_branch_grids_to_its_own_span(client, loaded):
    """기본은 상대 격자다 — 셀 크기가 달라도 같은 점 수를 받는다."""
    body = _dvdq(client, loaded, cycles="2,3", branches="discharge")
    assert body["capacity_step"] is None
    usable = [s for s in body["series"] if s["points"]]
    assert usable and all(s["capacity_step"] > 0 for s in usable)


def test_an_unknown_smoother_is_refused_by_name(client, loaded):
    """조용히 되돌아가면 화면은 savgol 이라 적고 이동평균을 그린다."""
    response = client.get(f"/api/samples/{loaded}/dvdq",
                          params={"cycles": "3", "smoother": "gaussian"})
    assert response.status_code == 422
    assert "gaussian" in response.text


# --- CSV ----------------------------------------------------------------------

def test_the_csv_is_full_resolution_not_the_thinned_plot(client, loaded):
    """CSV 는 다시 그리거나 봉우리 간격을 재는 데 쓴다 — 화면용 축약이 아니다."""
    plotted = _dvdq(client, loaded, cycles="3", branches="discharge",
                    max_points=120)
    curve = next(s for s in plotted["series"] if s["points"])
    assert curve["points"] <= 120

    response = client.get(f"/api/export/samples/{loaded}/dvdq.csv",
                          params={"cycles": "3", "branches": "discharge"})
    assert response.status_code == 200
    rows = response.text.strip().splitlines()
    assert "dVdQ" in rows[0]
    assert len(rows) - 1 > curve["points"]


def test_the_csv_says_no_cycle_matched_rather_than_writing_nothing(client, loaded):
    response = client.get(f"/api/export/samples/{loaded}/dvdq.csv",
                          params={"cycles": "9999"})
    assert response.status_code == 404


# --- 비교 ---------------------------------------------------------------------

def _second_cell(client, name, payload):
    """두 번째 셀.  **다른 바이트여야 한다** — 같은 파일은 sha256 으로 중복
    판정되어 두 번째 셀에 붙지 않는다 (CLAUDE.md §0.2)."""
    created = client.post("/api/samples", json={"name": name})
    assert created.status_code == 201, created.text
    other = created.json()["id"]
    upload = client.post("/api/runs/upload", params={"sample_id": other},
                         files={"file": (f"{name}.wrd", payload,
                                         "application/octet-stream")})
    assert upload.status_code == 201, upload.text
    return other


def test_compare_overlays_the_same_cycle_from_several_cells(client, loaded,
                                                            finished_wrd_bytes):
    other = _second_cell(client, "비교용셀", finished_wrd_bytes)

    for endpoint in ("dqdv", "dvdq"):
        response = client.get(f"/api/compare/{endpoint}",
                              params={"sample_ids": f"{loaded},{other}",
                                      "cycle": 3, "branches": "discharge"})
        assert response.status_code == 200, response.text
        body = response.json()
        assert len(body["series"]) == 2, endpoint
        # 비교 화면은 빈 곡선을 싣지 않는다 — 서른 셀의 빈 항목이 범례를 덮는다.
        assert all(s["points"] for s in body["series"]), endpoint
        assert len({s["label"] for s in body["series"]}) == 2, endpoint


def test_compare_uses_one_grid_for_every_cell(client, loaded,
                                              finished_wrd_bytes):
    """봉우리 *높이* 는 같은 격자·같은 창에서만 비교할 수 있다 (ADR 0013).

    비교 화면이 바로 사람이 높이를 눈으로 재는 곳이다.
    """
    other = _second_cell(client, "두번째", finished_wrd_bytes)

    body = client.get("/api/compare/dqdv",
                      params={"sample_ids": f"{loaded},{other}", "cycle": 3,
                              "branches": "discharge", "voltage_step": 0.01,
                              "smoothing": 7, "smoother": "savgol",
                              "poly_order": 2}).json()
    assert {s["voltage_step"] for s in body["series"]} == {0.01}
    assert {s["smoothing"] for s in body["series"]} == {7}
    assert {(s["smoother"], s["poly_order"]) for s in body["series"]} == {("savgol", 2)}


def test_compare_refuses_an_unknown_smoother_too(client, loaded):
    response = client.get("/api/compare/dvdq",
                          params={"sample_ids": str(loaded), "cycle": 3,
                                  "smoother": "gaussian"})
    assert response.status_code == 422
