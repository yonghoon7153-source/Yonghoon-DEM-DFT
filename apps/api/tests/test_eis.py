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
    # n=1 로 만들면 아크마다 이완 시간이 정확히 하나라 DRT 의 봉우리 위치를
    # 닫힌 값과 대조할 수 있다.  기본값은 실제에 가까운 찌그러진 아크다.
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


def test_the_fit_response_carries_the_curve_the_server_computed(client):
    """화면은 회로를 다시 해석하지 않는다 (#6).

    브라우저의 근사 재구성은 L·Ws·Wo·중첩을 못 그렸고 — 서버 R0-L1 이
    1 kHz 에서 1+j6.283 인데 화면은 1+j0 — preset 밖 회로 문자열로 바로
    도달하는 경로였다.  이제 서버가 같은 AST 로 계산한 곡선이 응답에 실린다.
    """
    out = upload(client, kind="liquid")
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"}).json()
    assert fit["converged"]
    assert len(fit["fitted_frequency_hz"]) == out["n_points"]
    assert len(fit["fitted_z_re"]) == out["n_points"]
    # 수렴한 적합의 곡선은 측정과 닿아 있어야 한다 — 고주파 첫 점에서 비교.
    points = client.get(f"/api/eis/spectra/{out['id']}/points").json()
    assert fit["fitted_z_re"][0] == pytest.approx(points["z_re"][0], rel=0.05)


def test_the_curve_is_right_even_when_parallel_members_are_swapped(client):
    """`p(CPE1,R1)` 표기 — 저장 순서가 회로의 파라미터 순서와 다르다 (#2).

    이름으로 짝지어 평가해야 한다; 위치로 넣으면 Q 가 R 자리로 들어간 곡선이
    "맞춤" 으로 그려진다.
    """
    import numpy as np

    out = upload(client, kind="liquid")
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(CPE1,R1)-p(CPE2,R2)"}).json()
    assert fit["converged"]
    points = client.get(f"/api/eis/spectra/{out['id']}/points").json()
    measured = np.array(points["z_re"]) + 1j * np.array(points["z_im"])
    fitted = np.array(fit["fitted_z_re"]) + 1j * np.array(fit["fitted_z_im"])
    residual = float(np.median(np.abs(fitted - measured) / np.abs(measured)))
    assert residual < 1e-2, residual


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


# --- 무결성: 캐시·원본·재귀속 (리뷰 #9·#12·#22·#23) --------------------------

def test_a_swapped_cache_is_not_served_as_this_spectrum(client):
    """캐시는 id 폴더에 살지만 내용은 해시로 자신을 증명해야 한다.

    리뷰 재현: B 의 points.npz 를 A 자리에 복사하면 A 조회가 B 의 임피던스를
    A 의 이름으로 돌려줬다.  이제 해시가 다르면 캐시를 버리고 불변 원본에서
    다시 파싱한다 — 답은 A 의 숫자다.
    """
    import shutil

    from app import storage
    a = upload(client, name="a.mpr", rs=5.0)
    b = upload(client, name="b.mpr", rs=50.0)
    shutil.copyfile(storage.spectrum_points_path(b["id"]),
                    storage.spectrum_points_path(a["id"]))

    points = client.get(f"/api/eis/spectra/{a['id']}/points").json()
    assert points["z_re"][0] == pytest.approx(5.0, abs=1.0)      # A 의 R_s


def test_a_lost_cache_heals_from_the_immutable_original(client):
    from app import storage
    out = upload(client)
    storage.drop_spectrum_cache(out["id"])
    assert not storage.spectrum_points_path(out["id"]).exists()

    points = client.get(f"/api/eis/spectra/{out['id']}/points")
    assert points.status_code == 200
    assert storage.spectrum_points_path(out["id"]).exists()      # 다시 캐시됨


def test_reuploading_known_bytes_restores_a_lost_original(client):
    """"다시 올려 주세요" 라는 안내가 실제로 통해야 한다 (#23).

    dedup 이 저장 전에 반환하면 안내대로 해도 영원히 409 다.
    """
    from app import storage
    out = upload(client)
    storage.drop_spectrum_cache(out["id"])
    storage.spectrum_upload_path(out["sha256"], "mpr").unlink()
    assert client.get(f"/api/eis/spectra/{out['id']}/points").status_code == 409

    again = client.post("/api/eis/spectra/upload", params={"kind": "solid"},
                        files={"file": ("copy.mpr", mpr(),
                                        "application/octet-stream")})
    assert again.status_code == 201
    assert again.json()["duplicate"] is True
    assert client.get(f"/api/eis/spectra/{out['id']}/points").status_code == 200


def test_a_duplicate_upload_fills_blanks_and_overwrites_nothing(client, sample_id):
    """빈 칸은 나중 업로드가 채울 수 있지만, 채워진 칸은 그대로다 (#22)."""
    first = upload(client, cell_config="")
    assert first["cell_config"] == ""

    again = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "solid", "cell_config": "sym", "sample_id": sample_id,
                "at_cycle": 200},
        files={"file": ("copy.mpr", mpr(), "application/octet-stream")})
    body = again.json()
    assert body["duplicate"] is True
    assert body["cell_config"] == "sym"
    assert body["sample_id"] == sample_id
    assert body["at_cycle"] == 200

    conflicting = client.post(
        "/api/eis/spectra/upload", params={"kind": "solid", "cell_config": "full"},
        files={"file": ("copy2.mpr", mpr(), "application/octet-stream")})
    assert conflicting.json()["cell_config"] == "sym"            # 안 덮인다


def test_a_settings_file_for_another_experiment_is_refused(client):
    """EC-Lab 접미사(_C01)를 뗀 실험 이름이 달라야 남의 조건이다 (#13).

    "하나씩이면 그냥 붙인다" 는 클라이언트 예비 규칙이 B 실험의 진폭·장비를
    A 의 측정 조건으로 저장했다.  서버도 이름 불일치를 독립적으로 거절한다.
    """
    response = client.post(
        "/api/eis/spectra/upload", params={"kind": "solid"},
        files={"file": ("A_C01.mpr", mpr(), "application/octet-stream"),
               "settings_file": ("B.mps", b"EC-LAB SETTING FILE\r\n",
                                 "application/octet-stream")})
    assert response.status_code == 422
    assert "짝이 아닙니다" in response.json()["detail"]


def test_a_channel_suffix_does_not_break_the_settings_pair(client):
    """`A_C01.mpr` 의 짝은 `A.mps` 다 — 접미사는 데이터 파일에만 붙는다."""
    response = client.post(
        "/api/eis/spectra/upload", params={"kind": "solid"},
        files={"file": ("A_C01.mpr", mpr(), "application/octet-stream"),
               "settings_file": ("A.mps", b"EC-LAB SETTING FILE\r\n",
                                 "application/octet-stream")})
    assert response.status_code == 201


def test_a_fresh_upload_is_not_marked_duplicate(client):
    assert upload(client)["duplicate"] is False


def test_deleting_a_sample_detaches_its_spectra(client):
    """SQLite 는 행 id 를 재사용한다.  붙은 채 남으면 다음에 만든 셀이 죽은
    셀의 임피던스를 자기 측정으로 물려받는다 (#9)."""
    created = client.post("/api/samples", json={"name": "EIS-DEAD"}).json()
    spectrum = upload(client, sample_id=created["id"])
    assert client.delete(f"/api/samples/{created['id']}").status_code == 204

    detail = client.get(f"/api/eis/spectra/{spectrum['id']}").json()
    assert detail["sample_id"] is None

    reborn = client.post("/api/samples", json={"name": "EIS-REBORN"}).json()
    assert reborn["id"] == created["id"]                          # id 재사용 확인
    attached = client.get("/api/eis/spectra",
                          params={"sample_id": reborn["id"]}).json()
    assert attached == []


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


# --- DRT --------------------------------------------------------------------
#
# 등가회로는 아크가 몇 개인지를 회로를 그린 사람이 미리 정한다.  DRT 는 정하지
# 않으므로 두 방법이 같은 답을 내면 그 아크는 가정이 아니라 스펙트럼 안에 있다.

def test_the_drt_finds_the_processes_the_file_was_built_from(client):
    out = upload(client, kind="solid", n1=1.0, n2=1.0)
    body = client.get(f"/api/eis/spectra/{out['id']}/drt",
                      params={"regularisation": 1e-3}).json()
    big = [peak for peak in body["peaks"] if peak["resistance_ohm"] > 1.0]
    assert len(big) == 2
    assert big[0]["frequency_hz"] > big[1]["frequency_hz"]
    assert body["r_inf_ohm"] == pytest.approx(5.0, rel=0.1)


def test_the_peak_areas_are_the_resistances(client):
    out = upload(client, kind="solid", n1=1.0, n2=1.0)
    body = client.get(f"/api/eis/spectra/{out['id']}/drt",
                      params={"regularisation": 1e-3}).json()
    big = sorted((peak for peak in body["peaks"] if peak["resistance_ohm"] > 1.0),
                 key=lambda peak: -peak["frequency_hz"])
    assert big[0]["resistance_ohm"] == pytest.approx(20.0, rel=0.15)
    assert big[1]["resistance_ohm"] == pytest.approx(40.0, rel=0.15)


def test_the_regularisation_is_part_of_the_answer(client):
    """λ 가 답을 정한다.  결과에 그 값이 없으면 그림이 무엇인지 알 수 없다."""
    out = upload(client, kind="solid")
    body = client.get(f"/api/eis/spectra/{out['id']}/drt",
                      params={"regularisation": 0.05}).json()
    assert body["regularisation"] == pytest.approx(0.05)


def test_the_sweep_shows_both_failure_modes_and_names_a_corner(client):
    out = upload(client, kind="solid", n1=1.0, n2=1.0)
    body = client.get(f"/api/eis/spectra/{out['id']}/drt/sweep").json()
    lambdas = [row["regularisation"] for row in body["results"]]
    assert len(lambdas) >= 5
    assert lambdas == sorted(lambdas)
    # 큰 λ 에서는 봉우리가 뭉친다 — 벌점이 일을 하고 있다는 뜻이다.
    assert len(body["results"][-1]["peaks"]) < len(body["results"][0]["peaks"]) + 1
    assert body["suggested_index"] >= 0
    assert "λ=" in body["suggested_reason"]


def test_an_impossible_regularisation_is_refused(client):
    out = upload(client)
    assert client.get(f"/api/eis/spectra/{out['id']}/drt",
                      params={"regularisation": 0}).status_code == 422


# --- 셀에 붙이기 ------------------------------------------------------------
#
# API 는 처음부터 됐는데 화면이 읽기만 해서, 셀 상세의 임피던스 카드가 영영
# 비어 있었다 -- 붙일 방법이 없었기 때문이다.

def test_a_spectrum_can_be_attached_after_the_fact(client, sample_id):
    out = upload(client)
    assert out["sample_id"] is None
    attached = client.patch(f"/api/eis/spectra/{out['id']}",
                            json={"sample_id": sample_id})
    assert attached.status_code == 200, attached.text
    assert attached.json()["sample_name"] == "TEST-01"
    assert len(client.get("/api/eis/spectra",
                          params={"sample_id": sample_id}).json()) == 1


def test_a_spectrum_can_be_detached(client, sample_id):
    out = upload(client, sample_id=sample_id)
    detached = client.patch(f"/api/eis/spectra/{out['id']}",
                            json={"clear": ["sample_id"]})
    assert detached.status_code == 200, detached.text
    assert detached.json()["sample_id"] is None


def test_uploading_onto_a_cell_that_does_not_exist_is_refused(client):
    """조용히 안 붙은 채 저장되면, 붙였다고 생각한 사람에게는 사라진 것과 같다."""
    response = client.post("/api/eis/spectra/upload",
                           params={"kind": "solid", "sample_id": 9999},
                           files={"file": ("s.mpr", mpr(),
                                           "application/octet-stream")})
    assert response.status_code == 404
