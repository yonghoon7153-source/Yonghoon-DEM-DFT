"""GITT — 준평형 곡선과 확산계수 (ADR 0020).

pOCV 는 재료 상수 없이 나오고 확산계수는 안 나온다.  두 가지를 나란히 두되
비어 있는 이유가 다르다는 것이 보여야 하므로, 그 차이를 시험이 고정한다.
"""

import pytest

import synthetic


def gitt_bytes(**overrides) -> bytes:
    return synthetic.build_wrd(synthetic.make_gitt(**overrides))


def upload(client, name="gitt_01.wrd", **overrides):
    response = client.post("/api/gitt/runs/upload",
                           files={"file": (name, gitt_bytes(**overrides),
                                           "application/octet-stream")})
    assert response.status_code == 201, response.text
    return response.json()


MATERIAL = {"molar_volume_cm3": 20.0, "molar_mass_g": 96.0,
            "active_mass_g": 0.02, "area_cm2": 1.33}


def test_the_original_wrd_comes_back_out_byte_for_byte(client):
    """EIS 와 같은 이유, 같은 길 (CLAUDE.md §0.2)."""
    content = gitt_bytes(n_pulses=6)
    out = client.post("/api/gitt/runs/upload",
                      files={"file": ("gitt_01.wrd", content,
                                      "application/octet-stream")}).json()
    got = client.get(f"/api/export/gitt/{out['id']}/original")
    assert got.status_code == 200
    assert got.content == content
    assert "gitt_01.wrd" in got.headers["content-disposition"]
    assert client.get("/api/export/gitt/9999/original").status_code == 404


# --- 올리기 -----------------------------------------------------------------

def test_a_gitt_wrd_becomes_its_own_record(client):
    out = upload(client, n_pulses=6)
    assert out["n_pulses"] == 6
    assert out["n_points"] > 100
    assert out["name"] == "gitt_01"


def test_it_does_not_land_in_the_cycling_library(client):
    """사이클링처럼 요약하면 아무 뜻 없는 사이클 수백 개가 진짜 옆에 앉는다."""
    upload(client)
    assert client.get("/api/runs").json() == []
    assert client.get("/api/samples").json() == []


def test_a_cycling_file_is_not_refused_but_is_remarked_on(client, wrd_bytes):
    """`.wrd` 안에 사이클링과 GITT 를 가르는 표식은 없다.

    둘 다 충전·방전·휴지로 이루어져 있고 차이는 "몇 번이나" 뿐이다.  그래서
    거절하지 않고 무엇을 봤는지만 적는다 — 펄스가 셋인 GITT 화면은 그 자체로
    잘못 올렸다는 신호이고, 그 판단은 올린 사람이 훨씬 잘 한다 (§0.4).
    """
    response = client.post("/api/gitt/runs/upload",
                           files={"file": ("cycling.wrd", wrd_bytes,
                                           "application/octet-stream")})
    assert response.status_code == 201
    assert "GITT 기록이 맞는지" in response.json()["pulse_note"]


def test_a_real_gitt_record_gets_no_such_remark(client):
    assert upload(client, n_pulses=8)["pulse_note"] == ""


def test_the_same_bytes_twice_is_the_same_record(client):
    first = upload(client)
    again = client.post("/api/gitt/runs/upload",
                        files={"file": ("copy.wrd", gitt_bytes(),
                                        "application/octet-stream")})
    assert again.status_code == 201
    assert again.json()["id"] == first["id"]
    assert len(client.get("/api/gitt/runs").json()) == 1


# --- pseudo-OCV -------------------------------------------------------------

def test_the_pocv_needs_nothing_typed_in(client):
    """파일만 있으면 나온다.  확산계수와 비어 있는 이유가 다르다."""
    out = upload(client, n_pulses=5, dv_per_pulse=0.05, v_start=3.0)
    body = client.get(f"/api/gitt/runs/{out['id']}/pocv").json()
    assert len(body["charge"]) == 5
    for index, point in enumerate(body["charge"]):
        assert point["voltage_v"] == pytest.approx(3.0 + 0.05 * (index + 1), abs=2e-3)


def test_the_pocv_capacity_starts_at_zero_and_climbs(client):
    out = upload(client, n_pulses=4, capacity_per_pulse_mah=0.5)
    body = client.get(f"/api/gitt/runs/{out['id']}/pocv").json()
    capacities = [point["capacity_mah"] for point in body["charge"]]
    assert capacities[0] == pytest.approx(0.0, abs=1e-6)
    assert capacities[-1] == pytest.approx(1.5, abs=1e-3)


def test_a_pulse_with_no_rest_is_counted_not_dropped(client):
    out = upload(client, n_pulses=4, trailing_rest=False)
    body = client.get(f"/api/gitt/runs/{out['id']}/pocv").json()
    assert len(body["charge"]) == 3
    assert body["skipped_charge"] == 1
    assert body["skipped_reasons"]


def test_each_point_says_how_relaxed_it_was(client):
    out = upload(client, n_pulses=3, rest_s=600.0)
    body = client.get(f"/api/gitt/runs/{out['id']}/pocv").json()
    assert all(point["rest_s"] == pytest.approx(600.0, rel=0.01)
               for point in body["charge"])
    assert all(point["drift_mv"] >= 0 for point in body["charge"])


def test_a_minimum_rest_can_be_set_and_it_drops_points(client):
    out = upload(client, n_pulses=4, rest_s=60.0)
    client.patch(f"/api/gitt/runs/{out['id']}", json={"min_rest_s": 600})
    body = client.get(f"/api/gitt/runs/{out['id']}/pocv").json()
    assert body["charge"] == []
    assert body["skipped_charge"] == 4


# --- 확산계수 ---------------------------------------------------------------

def test_the_diffusion_names_what_is_missing(client):
    """추정한 몰부피로 계산한 D 는 그 추정의 제곱만큼 틀린다 (§0.4)."""
    out = upload(client)
    assert set(out["missing_for_diffusion"]) == {
        "몰부피 V_M", "몰질량 M_B", "활물질 질량", "계면 면적 S"}
    body = client.get(f"/api/gitt/runs/{out['id']}/diffusion").json()
    assert body["usable"] == 0
    assert "몰부피 V_M" in body["missing"]


def test_filling_the_constants_makes_the_numbers_appear(client):
    out = upload(client, n_pulses=4)
    patched = client.patch(f"/api/gitt/runs/{out['id']}", json=MATERIAL)
    assert patched.status_code == 200, patched.text
    assert patched.json()["missing_for_diffusion"] == []

    body = client.get(f"/api/gitt/runs/{out['id']}/diffusion").json()
    assert body["missing"] == []
    assert body["usable"] == body["total"] - 1     # 첫 펄스는 ΔE_s 가 없다
    values = [point["d_cm2_s"] for point in body["points"] if point["d_cm2_s"]]
    assert all(value > 0 for value in values)
    assert values[0] == pytest.approx(values[-1], rel=0.05)


def test_the_area_can_come_from_the_diameter(client):
    """캘리퍼가 읽는 것은 지름이다.  면적을 두 번 재게 하지 않는다."""
    out = upload(client, n_pulses=4)
    values = dict(MATERIAL)
    values.pop("area_cm2")
    values["diameter_mm"] = 13.0
    patched = client.patch(f"/api/gitt/runs/{out['id']}", json=values).json()

    assert patched["area_cm2"] is None            # 적은 적이 없다
    assert patched["area_cm2_effective"] == pytest.approx(1.3273, rel=1e-3)
    assert patched["missing_for_diffusion"] == []  # 그래도 D 가 나온다

    body = client.get(f"/api/gitt/runs/{out['id']}/diffusion").json()
    assert body["area_cm2"] == pytest.approx(1.3273, rel=1e-3)
    assert body["usable"] > 0


def test_a_written_area_beats_the_diameter(client):
    """원이 아닌 전극이 있고, 그때 지름은 잴 수 있는 값이 아니다."""
    out = upload(client, n_pulses=3)
    patched = client.patch(f"/api/gitt/runs/{out['id']}",
                           json={**MATERIAL, "diameter_mm": 13.0}).json()
    assert patched["area_cm2_effective"] == pytest.approx(1.33)


def test_the_active_mass_can_come_from_the_electrode_mass_and_wt_percent(client):
    """저울이 읽는 것은 전극 전체다 (§3).  분모는 활물질이어야 한다."""
    out = upload(client, n_pulses=4)
    values = dict(MATERIAL)
    values.pop("active_mass_g")
    values["electrode_mass_g"] = 0.025
    values["active_wt_percent"] = 80.0
    patched = client.patch(f"/api/gitt/runs/{out['id']}", json=values).json()

    assert patched["active_mass_g"] is None
    assert patched["active_mass_g_effective"] == pytest.approx(0.02)
    assert patched["missing_for_diffusion"] == []

    body = client.get(f"/api/gitt/runs/{out['id']}/diffusion").json()
    assert body["mass_g"] == pytest.approx(0.02)


def test_a_written_active_mass_beats_the_electrode_mass(client):
    """활물질만 따로 단 경우가 있다 -- 계산값이 이기면 잰 값이 조용히 버려진다."""
    out = upload(client, n_pulses=3)
    patched = client.patch(
        f"/api/gitt/runs/{out['id']}",
        json={**MATERIAL, "electrode_mass_g": 0.05, "active_wt_percent": 50.0},
    ).json()
    assert patched["active_mass_g_effective"] == pytest.approx(0.02)


def test_half_of_a_derived_pair_is_still_missing(client):
    """wt% 없이 전극 질량만 있으면 활물질 질량을 모른다 -- 지어내지 않는다."""
    out = upload(client, n_pulses=3)
    values = dict(MATERIAL)
    values.pop("active_mass_g")
    values["electrode_mass_g"] = 0.025
    patched = client.patch(f"/api/gitt/runs/{out['id']}", json=values).json()
    assert patched["active_mass_g_effective"] is None
    assert patched["missing_for_diffusion"] == ["활물질 질량"]


def test_the_first_pulse_says_why_it_has_no_number(client):
    out = upload(client, n_pulses=3)
    client.patch(f"/api/gitt/runs/{out['id']}", json=MATERIAL)
    body = client.get(f"/api/gitt/runs/{out['id']}/diffusion").json()
    assert body["points"][0]["d_cm2_s"] is None
    assert "첫 펄스" in body["points"][0]["reason"]


def test_every_point_carries_its_own_linearity(client):
    """√t 직선성이 곧 Weppner-Huggins 의 가정이다.  점마다 함께 낸다."""
    out = upload(client, n_pulses=3)
    client.patch(f"/api/gitt/runs/{out['id']}", json=MATERIAL)
    body = client.get(f"/api/gitt/runs/{out['id']}/diffusion").json()
    assert all(point["sqrt_t_r_squared"] > 0.99 for point in body["points"])


def test_a_negative_material_constant_is_refused(client):
    out = upload(client)
    assert client.patch(f"/api/gitt/runs/{out['id']}",
                        json={"area_cm2": -1}).status_code == 422


def test_clear_refuses_file_facts(client):
    """duration·start_time 은 파일에서 온 사실이다 (#24) — 재료 상수만 비운다."""
    out = upload(client)
    refused = client.patch(f"/api/gitt/runs/{out['id']}",
                           json={"clear": ["duration_h"]})
    assert refused.status_code == 422
    client.patch(f"/api/gitt/runs/{out['id']}", json={"molar_mass_g": 96.0})
    ok = client.patch(f"/api/gitt/runs/{out['id']}",
                      json={"clear": ["molar_mass_g"]})
    assert ok.status_code == 200
    assert ok.json()["molar_mass_g"] is None


def test_reuploading_known_bytes_restores_a_lost_original(client):
    """pOCV 는 불변 원본을 재파싱한다.  원본이 사라졌을 때 화면은 "다시 올려
    주세요" 라고 하는데, dedup 이 저장 전에 반환하면 그 안내는 거짓이다 (#23)."""
    from app import storage
    out = upload(client)
    # 캐시까지 없어야 진짜 "다시 올려 주세요" 상황이다 — 캐시가 남아 있으면
    # 원본이 사라져도 분석은 계속 답한다 (그쪽이 옳은 동작이다).
    storage.drop_gitt_cache(out["sha256"])
    storage.upload_path(out["sha256"]).unlink()
    assert client.get(f"/api/gitt/runs/{out['id']}/pocv").status_code == 409

    again = client.post("/api/gitt/runs/upload",
                        files={"file": ("copy.wrd", gitt_bytes(),
                                        "application/octet-stream")})
    assert again.status_code == 201
    assert again.json()["id"] == out["id"]
    assert client.get(f"/api/gitt/runs/{out['id']}/pocv").status_code == 200


def test_the_analysis_is_served_from_a_cache_that_proves_itself(client):
    """파싱이 요청 비용의 전부다 — 실측 108 MB 에서 읽기 0.06s, 파싱 1.31s.

    캐시는 원본 해시와 컬럼 목록으로 자신을 증명하고, 증명 못 하면 불변
    원본에서 다시 만든다 (ADR 0020 이 미뤄 둔 결정).
    """
    from app import storage
    out = upload(client)
    first = client.get(f"/api/gitt/runs/{out['id']}/pocv")
    assert first.status_code == 200
    assert storage.gitt_cache_path(out["sha256"]).exists()

    # 남의 해시로 만든 캐시는 자신을 증명하지 못한다.
    import numpy as np
    path = storage.gitt_cache_path(out["sha256"])
    with np.load(path, allow_pickle=False) as archive:
        payload = {name: archive[name] for name in archive.files}
    payload["meta::sha256"] = np.array("0" * 64)
    np.savez_compressed(path, **payload)
    again = client.get(f"/api/gitt/runs/{out['id']}/pocv")
    assert again.status_code == 200                    # 원본에서 되살렸다
    assert again.json() == first.json()


def test_deleting_forgets_the_record_but_not_the_original(client):
    from app import storage
    out = upload(client)
    original = storage.upload_path(out["sha256"])
    assert original.exists()
    assert client.delete(f"/api/gitt/runs/{out['id']}").status_code == 204
    assert client.get(f"/api/gitt/runs/{out['id']}").status_code == 404
    assert original.exists()


# --- 대시보드: 셀 한 줄 -----------------------------------------------------

def _attach(client, name="g.wrd", **overrides):
    sample_id = client.post("/api/samples", json={"name": "CELL"}).json()["id"]
    made = client.post("/api/gitt/runs/upload", params={"sample_id": sample_id},
                       files={"file": (name, gitt_bytes(**overrides),
                                       "application/octet-stream")}).json()
    return sample_id, made


def test_the_dashboard_says_what_is_missing_rather_than_a_number(client):
    """§0.4 — 재료 상수가 없으면 D 가 없는 것이지 0 이 아니다.

    그리고 **무엇이** 없는지가 곧 이 셀에서 다음에 할 일이다 (ADR 0020).
    """
    _attach(client)
    row = client.get("/api/gitt/dashboard").json()["rows"][0]
    assert row["records"] == 1
    assert row["ready"] == 0
    assert row["diffusion_low"] is None
    assert row["diffusion_high"] is None
    assert len(row["missing"]) == 4


def test_the_dashboard_gives_a_range_not_an_average(client):
    """D 는 SOC 를 따라 자릿수로 움직인다.

    평균을 내면 그 숫자가 아무 SOC 도 뜻하지 않는다 -- 최소와 최대는 적어도
    둘 다 실제로 나온 값이다.
    """
    _sample, made = _attach(client)
    client.patch(f"/api/gitt/runs/{made['id']}", json={
        "molar_volume_cm3": 20.0, "molar_mass_g": 96.0,
        "active_mass_g": 0.01, "area_cm2": 1.3})

    row = client.get("/api/gitt/dashboard").json()["rows"][0]
    assert row["ready"] == 1
    assert row["missing"] == []
    assert row["diffusion_low"] is not None
    assert row["diffusion_low"] <= row["diffusion_high"]
    # 확산계수는 자릿수가 아주 작다 -- 값이 뒤집혀 나오면 여기서 걸린다.
    assert 0 < row["diffusion_low"] < 1e-3


def test_the_dashboard_shows_what_is_not_attached_yet_as_its_own_row(client):
    """안 붙은 기록도 이름으로 한 줄.  EIS 대시보드와 같은 규칙이다."""
    client.post("/api/gitt/runs/upload",
                files={"file": ("loose.wrd", gitt_bytes(),
                                "application/octet-stream")})
    body = client.get("/api/gitt/dashboard").json()
    assert body["unattached"] == 1
    assert len(body["rows"]) == 1
    row = body["rows"][0]
    assert row["attached"] is False
    assert row["sample_id"] is None
    assert row["name"] == "loose.wrd"
    # 재료 상수가 없으므로 D 는 빈칸이고, 무엇이 없는지가 그 자리에 온다 (§0.4).
    assert row["diffusion_low"] is None
    assert len(row["missing"]) == 4


def test_an_attached_row_carries_the_files_own_name_too(client):
    """셀 이름만으로는 어느 측정인지 모른다 -- 파일 이름에 조건이 적혀 있다."""
    sample_id, _ = _attach(client, name="0.1C_25C.wrd")
    row = client.get("/api/gitt/dashboard").json()["rows"][0]
    assert row["sample_id"] == sample_id
    assert row["attached"] is True
    assert row["name"] == "0.1C_25C.wrd"


# --- 목적: 무엇을 보려고 잰 기록인가 ------------------------------------------


def test_a_purpose_typed_at_upload_stays_on_the_record(client):
    made = client.post("/api/gitt/runs/upload", params={"purpose": "SOC별"},
                       files={"file": ("g.wrd", gitt_bytes(),
                                       "application/octet-stream")}).json()
    assert made["purpose"] == "SOC별"
    assert client.get(f"/api/gitt/runs/{made['id']}").json()["purpose"] == "SOC별"


def test_reuploading_does_not_wipe_a_purpose_already_written(client):
    """빈 칸으로 다시 올린 것은 '지워라' 가 아니다 — 셀 붙이기와 같은 규칙."""
    first = client.post("/api/gitt/runs/upload", params={"purpose": "저온"},
                        files={"file": ("g.wrd", gitt_bytes(),
                                        "application/octet-stream")}).json()
    again = client.post("/api/gitt/runs/upload",
                        files={"file": ("g.wrd", gitt_bytes(),
                                        "application/octet-stream")}).json()
    assert again["id"] == first["id"]
    assert again["purpose"] == "저온"


def test_a_purpose_can_be_edited_and_cleared(client):
    made = upload(client)
    patched = client.patch(f"/api/gitt/runs/{made['id']}",
                           json={"purpose": "코팅 전후"}).json()
    assert patched["purpose"] == "코팅 전후"
    cleared = client.patch(f"/api/gitt/runs/{made['id']}",
                           json={"clear": ["purpose"]}).json()
    assert cleared["purpose"] == ""


# --- 측정 자신의 조건 (ADR 0027) ------------------------------------------------


def test_a_gitt_record_carries_its_own_conditions(client):
    """EIS 와 같은 규칙이다 — 셀이 없어도 조건은 있다."""
    made = upload(client)
    out = client.patch(f"/api/gitt/runs/{made['id']}", json={
        "test_date": "2026-08-20", "process": "dry", "temperature_c": 45.0,
    }).json()
    assert out["sample_id"] is None
    assert out["process_effective"] == "dry"
    assert out["temperature_c_effective"] == 45.0
    assert out["inherited"] == []


def test_a_blank_gitt_field_borrows_from_the_cell(client):
    sample_id, made = _attach(client)
    client.patch(f"/api/samples/{sample_id}", json={"temperature_c": 25.0})
    out = client.get(f"/api/gitt/runs/{made['id']}").json()
    assert out["temperature_c_effective"] == 25.0
    assert "temperature_c" in out["inherited"]


def test_a_gitt_record_can_sit_in_a_group_without_a_cell(client):
    group = client.post("/api/groups", json={"name": "GITT 묶음"}).json()
    made = upload(client)
    out = client.patch(f"/api/gitt/runs/{made['id']}",
                       json={"group_id": group["id"]}).json()
    assert out["group_id_effective"] == group["id"]
    assert out["group_label"] == "GITT 묶음"
