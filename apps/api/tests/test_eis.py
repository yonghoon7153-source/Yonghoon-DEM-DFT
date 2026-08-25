"""임피던스: 올리고, 맞추고, 파라미터를 읽는다 (ADR 0019).

지금 랩의 절차는 EC-Lab 으로 열어 `.mpt` 로 내보내고, ZView 로 열어 회로를
그리고, 초기값 여섯 개를 손으로 넣고, 맞추고, 클립보드로 복사해 엑셀에 붙이는
것이다. 여기 있는 것은 그 순서에서 사람만 뺀 것이고, 그것이 정직하려면 실패가
성공만큼 잘 보여야 한다.
"""

import numpy as np
import pytest
import synthetic_eis as S


def mpr(**overrides) -> bytes:
    values = {"rs": 5.0, "r1": 20.0, "q1": 1e-5, "n1": 0.9,
              "r2": 40.0, "q2": 1e-3, "n2": 0.8}
    values.update(overrides)
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, **values)
    return S.build_mpr(S.spectrum_columns(frequency, z))


def upload(client, name="sym_01.mpr", kind="solid", sample_id=None,
           cell_config="sym", **overrides):
    params = {"kind": kind, "cell_config": cell_config}
    if sample_id is not None:
        params["sample_id"] = sample_id
    response = client.post("/api/eis/spectra/upload", params=params,
                           files={"file": (name, mpr(**overrides),
                                           "application/octet-stream")})
    assert response.status_code == 201, response.text
    return response.json()


# --- 올리기 ----------------------------------------------------------------

def test_an_mpr_becomes_a_spectrum(client):
    out = upload(client)
    assert out["n_points"] > 50
    assert out["source_format"] == "mpr"
    assert out["frequency_start_hz"] > out["frequency_end_hz"]
    assert out["name"] == "sym_01"


def test_the_same_bytes_twice_is_the_same_spectrum(client):
    """같은 측정이 장비 PC 와 노트북에서 각각 올라온다."""
    first = upload(client)
    again = client.post("/api/eis/spectra/upload", params={"kind": "solid"},
                        files={"file": ("copy.mpr", mpr(),
                                        "application/octet-stream")})
    assert again.status_code == 201
    assert again.json()["id"] == first["id"]
    assert len(client.get("/api/eis/spectra").json()) == 1


def test_a_text_export_works_too(client):
    """랩에 이미 `.mpt` 로 쌓아 둔 폴더가 있다."""
    frequency = S.log_sweep(1e5, 1e-1, 10)
    z = S.randles(frequency)
    text = S.build_mpt(S.spectrum_columns(frequency, z))
    response = client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                           files={"file": ("old.mpt", text.encode("latin-1"),
                                           "text/plain")})
    assert response.status_code == 201, response.text
    assert response.json()["source_format"] == "mpt"


def test_a_cycling_file_is_refused_with_a_reason(client, wrd_bytes):
    """`.wrd` 를 여기 올리는 일은 반드시 생긴다.  무엇을 올려야 하는지 말한다."""
    response = client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                           files={"file": ("cycling.wrd", wrd_bytes,
                                           "application/octet-stream")})
    assert response.status_code == 422
    assert ".mpr" in response.json()["detail"]


def test_an_unknown_kind_is_refused(client):
    response = client.post("/api/eis/spectra/upload", params={"kind": "gitt"},
                           files={"file": ("s.mpr", mpr(),
                                           "application/octet-stream")})
    assert response.status_code == 422


def test_the_settings_file_fills_in_what_the_data_cannot_say(client):
    """진폭도 장비 이름도 스펙트럼 안에는 없다 (§0.3)."""
    mps = ("EC-LAB SETTING FILE\r\n\r\nDevice : VSP-300\r\n\r\n"
           "Technique : 1\r\nPotentio Electrochemical Impedance Spectroscopy\r\n"
           "fi                  7.000\r\nunit fi             MHz\r\n"
           "Va (mV)             5.0\r\n")
    response = client.post(
        "/api/eis/spectra/upload", params={"kind": "solid"},
        files={"file": ("s.mpr", mpr(), "application/octet-stream"),
               "settings_file": ("s.mps", mps.encode("latin-1"), "text/plain")})
    assert response.status_code == 201, response.text
    out = response.json()
    assert out["device"] == "VSP-300"
    assert out["amplitude_mv"] == pytest.approx(5.0)
    assert "Impedance" in out["technique"]


def test_the_points_come_back_as_ohms_and_hertz(client):
    """정규화된 값은 저장하지도 내보내지도 않는다 (ADR 0001)."""
    out = upload(client)
    points = client.get(f"/api/eis/spectra/{out['id']}/points").json()
    assert len(points["frequency_hz"]) == out["n_points"]
    # 용량성 아크는 허수부가 음수다 — 부호를 뒤집어 읽었으면 여기서 걸린다.
    assert min(points["z_im"]) < 0
    assert points["magnitude"][0] == pytest.approx(
        np.hypot(points["z_re"][0], points["z_im"][0]))


# --- 맞추기 ----------------------------------------------------------------

def test_fitting_recovers_the_circuit_the_file_was_built_from(client):
    out = upload(client, kind="liquid")
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"}).json()
    assert fit["converged"]
    values = {p["name"]: p["value"] for p in fit["parameters"]}
    assert values["R0"] == pytest.approx(5.0, rel=1e-2)
    assert values["R1"] == pytest.approx(20.0, rel=1e-2)
    assert values["R2"] == pytest.approx(40.0, rel=1e-2)
    assert fit["chi_squared"] < 1e-6


def test_the_default_circuit_follows_the_kind(client):
    """전고체의 기본 회로에는 블로킹 CPE 가 있고 액체에는 없다."""
    liquid = upload(client, name="a.mpr", kind="liquid")
    solid = upload(client, name="b.mpr", kind="solid", rs=6.0)
    liquid_fit = client.post(f"/api/eis/spectra/{liquid['id']}/fit").json()
    solid_fit = client.post(f"/api/eis/spectra/{solid['id']}/fit").json()
    assert "CPE3" not in liquid_fit["circuit"]
    assert "CPE3" in solid_fit["circuit"]


def test_the_same_numbers_get_different_names_by_kind(client):
    """같은 두 아크가 액체 풀셀에서는 SEI·전하이동, 전고체 대칭셀에서는 벌크·입계다."""
    out = upload(client, kind="liquid", cell_config="full")
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"}).json()
    labels = {arc["parameter"]: arc["label"] for arc in fit["arcs"]}
    assert labels["R1"] == "SEI 저항"

    client.patch(f"/api/eis/spectra/{out['id']}",
                 json={"kind": "solid", "cell_config": "sym"})
    detail = client.get(f"/api/eis/spectra/{out['id']}").json()
    relabelled = {arc["parameter"]: arc["label"] for arc in detail["fits"][0]["arcs"]}
    assert relabelled["R1"] == "벌크 저항"
    # 다시 맞추지 않았다는 사실은 남는다.
    assert detail["fits"][0]["kind"] == "liquid"
    assert detail["fits"][0]["kind_now"] == "solid"


def test_a_full_cell_is_offered_no_conductivity(client):
    """풀셀의 저주파 아크는 계면이지 전해질이 아니다.

    거기에 두께를 나누면 단위는 S/cm 이고 뜻은 전도도가 아니다.  두께가 있어도
    내지 않는다 — 없어서 못 내는 것과 내면 안 되는 것은 다른 일이다.
    """
    out = upload(client, kind="solid", cell_config="full")
    client.patch(f"/api/eis/spectra/{out['id']}",
                 json={"thickness_um": 70, "area_cm2": 0.785})
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"}).json()
    assert fit["conductivity"]["total_s_cm"] is None
    assert fit["conductivity"]["missing"]
    labels = {arc["parameter"]: arc["label"] for arc in fit["arcs"]}
    assert labels["R2"] == "계면 저항"


def test_an_unknown_cell_configuration_is_refused(client):
    response = client.post("/api/eis/spectra/upload",
                           params={"kind": "solid", "cell_config": "coin"},
                           files={"file": ("s.mpr", mpr(),
                                           "application/octet-stream")})
    assert response.status_code == 422


def test_conductivity_needs_a_thickness_and_says_so(client):
    out = upload(client, kind="solid")
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"}).json()
    assert fit["conductivity"]["total_s_cm"] is None
    assert "두께" in fit["conductivity"]["missing"]

    client.patch(f"/api/eis/spectra/{out['id']}",
                 json={"thickness_um": 70, "area_cm2": 0.785})
    detail = client.get(f"/api/eis/spectra/{out['id']}").json()
    conductivity = detail["fits"][0]["conductivity"]
    assert conductivity["missing"] == []
    expected = 0.007 / ((20.0 + 40.0) * 0.785)
    assert conductivity["total_s_cm"] == pytest.approx(expected, rel=0.02)


def test_a_circuit_that_cannot_be_read_is_a_422_not_a_500(client):
    out = upload(client)
    response = client.post(f"/api/eis/spectra/{out['id']}/fit",
                           params={"circuit": "R0-p(R1,CPE1"})
    assert response.status_code == 422
    assert "회로" in response.json()["detail"]


def test_a_failed_fit_is_stored_rather_than_hidden(client):
    """맞지 않는다는 것도 발견이다.  숨기면 다음 사람이 같은 것을 또 해 본다."""
    out = upload(client)
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-W1"}).json()
    detail = client.get(f"/api/eis/spectra/{out['id']}").json()
    assert len(detail["fits"]) == 1
    assert detail["fits"][0]["id"] == fit["id"]


def test_the_dropped_points_are_reported(client):
    """유도성 꼬리를 조용히 자르면 R0 이 달라지고 아무도 이유를 모른다."""
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency) + 1j * np.where(frequency > 3e5, 8.0, 0.0)
    data = S.build_mpr(S.spectrum_columns(frequency, z))
    created = client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                          files={"file": ("ind.mpr", data,
                                          "application/octet-stream")}).json()
    fit = client.post(f"/api/eis/spectra/{created['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"}).json()
    assert fit["dropped_inductive"] > 0
    assert fit["frequency_high_hz"] < 3e5


def test_a_batch_reports_each_spectrum_separately(client):
    """하나가 안 맞는다고 나머지 스무 개가 멈추면 자동화가 아니다."""
    first = upload(client, name="a.mpr", kind="liquid")
    second = upload(client, name="b.mpr", kind="liquid", rs=7.0)
    response = client.post("/api/eis/fit-batch",
                           params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"},
                           json=[first["id"], second["id"], 9999])
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["requested"] == 3
    assert body["converged"] == 2
    assert len(body["failed"]) == 1
    assert body["failed"][0]["spectrum_id"] == 9999


# --- 정리 ------------------------------------------------------------------

def test_a_spectrum_can_be_attached_to_a_cell(client, sample_id):
    out = upload(client, sample_id=sample_id)
    assert out["sample_id"] == sample_id
    assert out["sample_name"] == "TEST-01"
    assert len(client.get("/api/eis/spectra",
                          params={"sample_id": sample_id}).json()) == 1


def test_a_blank_name_is_refused_like_everywhere_else(client):
    out = upload(client)
    assert client.patch(f"/api/eis/spectra/{out['id']}",
                        json={"name": "  "}).status_code == 422


def test_deleting_forgets_the_points_but_not_the_original(client):
    from app import storage
    out = upload(client)
    original = storage.spectrum_upload_path(out["sha256"], "mpr")
    assert original.exists()
    assert storage.spectrum_points_path(out["id"]).exists()

    assert client.delete(f"/api/eis/spectra/{out['id']}").status_code == 204
    assert not storage.spectrum_points_path(out["id"]).exists()
    # 원본 파일은 절대 지우지 않는다 (CLAUDE.md §0.2).
    assert original.exists()


def test_the_circuit_presets_say_what_each_one_is_for(client):
    body = client.get("/api/eis/circuits").json()
    kinds = {entry["kind"]: entry for entry in body["kinds"]}
    assert set(kinds) == {"liquid", "solid"}
    assert kinds["solid"]["presets"][0]["circuit"].endswith("CPE3")
    assert all(preset["note"] for entry in body["kinds"]
               for preset in entry["presets"])


# --- 같은 셀의 여러 시점 (초기 · 200 사이클) --------------------------------
#
# 전고체 과제는 구동 전과 200 사이클 뒤를 재서 **둘을 비교**한다.  그 비교가
# 목적이므로 몇 번째 사이클인지가 데이터의 일부이고, 없으면 올린 순서로 정렬돼
# 누가 파일을 어떤 순으로 끌어다 놓았는지가 그림의 순서가 된다.

def test_a_spectrum_can_say_which_cycle_it_belongs_to(client, sample_id):
    before = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "solid", "cell_config": "full", "sample_id": sample_id,
                "at_cycle": 0},
        files={"file": ("before.mpr", mpr(), "application/octet-stream")}).json()
    assert before["at_cycle"] == 0


def test_the_list_is_ordered_by_cycle_not_by_upload_time(client, sample_id):
    late = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "solid", "sample_id": sample_id, "at_cycle": 200},
        files={"file": ("after.mpr", mpr(rs=9.0), "application/octet-stream")}).json()
    early = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "solid", "sample_id": sample_id, "at_cycle": 0},
        files={"file": ("before.mpr", mpr(rs=5.0), "application/octet-stream")}).json()
    # 200 사이클 것을 먼저 올렸지만 0 이 먼저 나와야 한다.
    listed = client.get("/api/eis/spectra", params={"sample_id": sample_id}).json()
    assert [row["id"] for row in listed] == [early["id"], late["id"]]


def test_a_spectrum_with_no_cycle_number_sorts_last(client, sample_id):
    unnumbered = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "solid", "sample_id": sample_id},
        files={"file": ("x.mpr", mpr(rs=3.0), "application/octet-stream")}).json()
    numbered = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "solid", "sample_id": sample_id, "at_cycle": 200},
        files={"file": ("y.mpr", mpr(rs=4.0), "application/octet-stream")}).json()
    listed = client.get("/api/eis/spectra", params={"sample_id": sample_id}).json()
    assert [row["id"] for row in listed] == [numbered["id"], unnumbered["id"]]


def test_the_cycle_number_can_be_set_afterwards(client):
    out = upload(client)
    patched = client.patch(f"/api/eis/spectra/{out['id']}", json={"at_cycle": 200})
    assert patched.status_code == 200, patched.text
    assert patched.json()["at_cycle"] == 200


def test_a_negative_cycle_number_is_refused(client):
    out = upload(client)
    assert client.patch(f"/api/eis/spectra/{out['id']}",
                        json={"at_cycle": -1}).status_code == 422


def test_several_spectra_come_back_in_one_request(client, sample_id):
    """겹쳐 그리려면 동시에 필요하다.  하나씩 부르면 축이 두 번 다시 잡힌다."""
    first = upload(client, name="a.mpr", sample_id=sample_id)
    second = upload(client, name="b.mpr", sample_id=sample_id, rs=9.0)
    body = client.get("/api/eis/points",
                      params={"ids": f"{first['id']},{second['id']}"}).json()
    assert [row["id"] for row in body] == [first["id"], second["id"]]
    assert all(len(row["z_re"]) > 10 for row in body)


def test_a_missing_spectrum_in_a_batch_is_an_error_not_a_gap(client):
    """곡선 하나가 빠진 그림은 안 빠진 그림과 구분되지 않는다."""
    out = upload(client)
    response = client.get("/api/eis/points", params={"ids": f"{out['id']},9999"})
    assert response.status_code == 404


def test_a_batch_refuses_nonsense_ids(client):
    assert client.get("/api/eis/points", params={"ids": "1,abc"}).status_code == 422
    assert client.get("/api/eis/points", params={"ids": " "}).status_code == 422
