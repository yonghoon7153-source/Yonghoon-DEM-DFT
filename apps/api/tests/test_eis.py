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


def test_the_original_mpr_comes_back_out_byte_for_byte(client):
    """올린 바이트 그대로 다시 받을 수 있어야 한다 (CLAUDE.md §0.2).

    중앙에 모아 두는 이유가 "각자 노트북에서 원본이 사라지지 않게" 인데, 다시
    못 받으면 올리는 것이 편도 여행이 되고 아무도 유일본을 안 맡긴다.
    충방전 `.wrd` 는 처음부터 이 길이 있었고 EIS·GITT 만 없었다.
    """
    content = mpr()
    out = client.post("/api/eis/spectra/upload",
                      params={"kind": "solid", "cell_config": "sym"},
                      files={"file": ("sym_01.mpr", content,
                                      "application/octet-stream")}).json()
    got = client.get(f"/api/export/spectra/{out['id']}/original")
    assert got.status_code == 200
    assert got.content == content
    assert "sym_01.mpr" in got.headers["content-disposition"]

    # `.mps` 를 안 올렸으면 없다고 말한다 — 빈 파일을 주지 않는다.
    assert client.get(f"/api/export/spectra/{out['id']}/settings").status_code == 404
    assert client.get("/api/export/spectra/9999/original").status_code == 404


def test_upload_can_fit_on_the_way_in(client):
    """올리면서 회로를 골라 맞춘다 — 목록에 저항이 빈 줄로 쌓이지 않게.

    빈 줄은 "이 셀은 안 맞는다" 와 "아직 아무도 안 눌러 봤다" 를 구분해 주지
    않는다.  기본은 꺼져 있고 (요청 하나가 20 초씩 서 있는 것은 화면이
    기다릴 때나 괜찮다) 업로드 화면이 켜서 보낸다.
    """
    out = client.post("/api/eis/spectra/upload",
                      params={"kind": "liquid", "fit": "auto"},
                      files={"file": ("cell_01.mpr", mpr(),
                                      "application/octet-stream")}).json()
    detail = client.get(f"/api/eis/spectra/{out['id']}").json()
    assert detail["fits"], "올리면서 맞춘 결과가 없다"
    assert any(f["converged"] for f in detail["fits"])

    # 안 켜면 안 맞춘다.
    plain = client.post("/api/eis/spectra/upload",
                        params={"kind": "liquid"},
                        files={"file": ("cell_02.mpr", mpr(rs=7.0),
                                        "application/octet-stream")}).json()
    assert client.get(f"/api/eis/spectra/{plain['id']}").json()["fits"] == []


def test_the_cell_library_carries_the_impedance(client, sample_id):
    """셀 목록에서 임피던스가 있다/없다조차 안 보였다.

    빈 칸을 셋으로 가른다: 안 쟀다 · 쟀는데 안 맞췄다 · 맞췄다.  가운데를
    "—" 로 뭉뚱그리면 다음에 할 일이 안 보인다.
    """
    def cell():
        rows = client.get("/api/samples").json()
        return next(row for row in rows if row["id"] == sample_id)

    assert cell()["spectrum_count"] == 0
    assert cell()["impedance_ohm"] is None

    out = client.post("/api/eis/spectra/upload",
                      params={"kind": "liquid", "sample_id": sample_id},
                      files={"file": ("cell_01.mpr", mpr(),
                                      "application/octet-stream")}).json()
    # 쟀지만 아직 안 맞췄다.
    assert cell()["spectrum_count"] == 1
    assert cell()["impedance_ohm"] is None

    client.post(f"/api/eis/spectra/{out['id']}/fit",
                params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"})
    # R0 + R1 + R2 = 5 + 20 + 40.
    assert cell()["impedance_ohm"] == pytest.approx(65.0, rel=0.02)


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
    """전고체의 기본 회로는 전송선이고 액체는 아크다 (ADR 0028).

    복합전극의 저주파는 계면 하나가 아니라 두께 전체에 퍼진 반응이다 -- 랩이
    실제로 쓰는 모델이 전송선이고, 아크 회로는 그것을 숫자가 아무 뜻도 없는
    값으로만 흉내낸다.
    """
    liquid = upload(client, name="a.mpr", kind="liquid")
    solid = upload(client, name="b.mpr", kind="solid", rs=6.0)
    liquid_fit = client.post(f"/api/eis/spectra/{liquid['id']}/fit").json()
    solid_fit = client.post(f"/api/eis/spectra/{solid['id']}/fit").json()
    assert "TL" not in liquid_fit["circuit"]
    assert "TL" in solid_fit["circuit"]


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


def test_the_curve_stops_where_the_fit_stopped(client):
    """맞춘 구간 **밖**에는 곡선을 그리지 않는다.

    한때 저장된 전체 주파수 위에서 그렸다.  창을 좁혀 맞추면 그 밖은 외삽이고
    모델은 거기서 무엇이든 할 수 있다 — 실측 전고체 풀셀에서 저주파 일곱 점을
    빼고 맞췄더니 그 일곱 점 위의 곡선이 되돌아 나와 갈고리를 그렸다.  맞춤이
    터진 것처럼 보이지만 아무 점도 없는 곳의 그림이었다.
    """
    out = upload(client, kind="liquid")
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)",
                              "frequency_low_hz": 1.0}).json()
    assert fit["converged"]
    drawn = fit["fitted_frequency_hz"]
    assert min(drawn) >= 1.0
    assert len(drawn) < out["n_points"]
    assert len(drawn) == out["n_points"] - fit["dropped_out_of_range"]
    # 그리고 화면이 쓰는 세 배열의 길이는 늘 같아야 한다.
    assert len(fit["fitted_z_re"]) == len(drawn)
    assert len(fit["fitted_z_im"]) == len(drawn)


def test_the_fit_suggests_the_bounds_to_type(client):
    """추천 상한은 늘 있고(유도성만 보면 된다), 하한은 몰렸을 때만 있다."""
    out = upload(client, kind="liquid")
    fit = client.post(f"/api/eis/spectra/{out['id']}/fit",
                      params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"}).json()
    points = client.get(f"/api/eis/spectra/{out['id']}/points").json()
    assert fit["suggested_high_hz"] == pytest.approx(max(points["frequency_hz"]))
    # 이 합성 스펙트럼은 회로 그대로라 저주파 끝에 몰릴 것이 없다.
    assert fit["suggested_low_hz"] is None
    assert fit["suggested_low_drops"] == 0


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


def test_the_mps_original_survives_verbatim(client):
    """파서가 모르는 설정 줄은 원문 바이트에서만 되찾는다 (§0.2 정신, #21).

    settings_json 은 이해한 부분집합일 뿐이다 — 파서를 고친 뒤 되찾을 바이트가
    없으면 그 설정은 영영 사라진 것이다.
    """
    from app import storage
    raw = (b"EC-LAB SETTING FILE\r\n"
           b"Custom correction ENABLED\r\n"
           b"Safety limit 99\r\n")
    out = client.post(
        "/api/eis/spectra/upload", params={"kind": "solid"},
        files={"file": ("A_C01.mpr", mpr(), "application/octet-stream"),
               "settings_file": ("A.mps", raw, "application/octet-stream")}).json()
    assert out["id"]
    import hashlib
    sha = hashlib.sha256(raw).hexdigest()
    stored = storage.spectrum_upload_path(sha, "mps")
    assert stored.exists()
    assert stored.read_bytes() == raw                      # 바이트 그대로


def test_clear_refuses_instrument_facts(client):
    """clear 는 사람이 넣은 것만 비운다 (#24).  주파수 범위는 파일에서 온
    사실이라, 지우면 dedup 재업로드로도 안 돌아온다."""
    out = upload(client)
    response = client.patch(f"/api/eis/spectra/{out['id']}",
                            json={"clear": ["frequency_start_hz"]})
    assert response.status_code == 422
    assert "비울 수 없습니다" in response.json()["detail"]
    # 사람이 넣는 두께는 비울 수 있다.
    client.patch(f"/api/eis/spectra/{out['id']}", json={"thickness_um": 70})
    ok = client.patch(f"/api/eis/spectra/{out['id']}",
                      json={"clear": ["thickness_um"]})
    assert ok.status_code == 200
    assert ok.json()["thickness_um"] is None


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


# --- SOC 스캔: 한 업로드가 스펙트럼 여럿을 만든다 (ADR 0022) -----------------

def scan_mpr(**overrides) -> bytes:
    return S.build_mpr_soc_scan(**overrides)


def test_a_soc_scan_upload_becomes_one_spectrum_per_sweep(client):
    response = client.post(
        "/api/eis/spectra/upload", params={"kind": "liquid", "cell_config": "half"},
        files={"file": ("scan.mpr", scan_mpr(sweeps=4), "application/octet-stream")})
    assert response.status_code == 201
    body = response.json()
    assert body["sweep_count"] == 4
    assert body["sweep_index"] == 1

    listed = client.get("/api/eis/spectra", params={"kind": "liquid"}).json()
    assert len(listed) == 4
    # 같은 파일에서 나온 넷이 이름으로 구별돼야 목록에서 고를 수 있다.
    assert len({row["name"] for row in listed}) == 4
    # SOC 스캔의 x축은 스윕마다 다른 전위·용량이다.
    assert len({round(row["potential_v"], 4) for row in listed}) == 4


def test_a_scan_lists_its_sweeps_in_measurement_order(client):
    """SOC 스캔의 행들은 사이클 번호가 없고 시각도 같다 — 스윕 번호가 순서다.

    없으면 DB 가 주는 대로 나오는데, SOC 순서로 안 보이면 21행을 훑어야 한다.
    """
    client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                files={"file": ("scan.mpr", scan_mpr(sweeps=5),
                                "application/octet-stream")})
    rows = client.get("/api/eis/spectra").json()
    assert [row["sweep_index"] for row in rows] == [1, 2, 3, 4, 5]
    capacities = [row["capacity_mah"] for row in rows]
    assert capacities == sorted(capacities)      # SOC 가 단조로 증가한다


def test_a_scan_names_its_own_purpose(client):
    """계측기가 아는 것을 사람에게 다시 묻지 않는다 (§0.3).

    스윕이 여럿이고 용량이 스윕마다 다르면 그것이 SOC 스캔이다.
    """
    out = client.post(
        "/api/eis/spectra/upload", params={"kind": "liquid"},
        files={"file": ("scan.mpr", scan_mpr(sweeps=3), "application/octet-stream")}).json()
    assert out["purpose"] == "SOC별"


def test_a_typed_purpose_wins_over_the_guess(client):
    out = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "liquid", "purpose": "200 사이클"},
        files={"file": ("scan.mpr", scan_mpr(sweeps=3), "application/octet-stream")}).json()
    assert out["purpose"] == "200 사이클"


def test_a_single_sweep_file_is_not_given_a_purpose(client):
    """한 장짜리 측정에 목적을 지어내지 않는다 (§0.4)."""
    assert upload(client)["purpose"] == ""
    assert upload(client, name="b.mpr", rs=9.0)["sweep_count"] == 1


def test_the_purpose_can_be_typed_later(client):
    out = upload(client)
    patched = client.patch(f"/api/eis/spectra/{out['id']}",
                           json={"purpose": "온도별"})
    assert patched.status_code == 200
    assert patched.json()["purpose"] == "온도별"


def test_each_sweep_of_a_scan_plots_on_its_own(client):
    """스윕마다 캐시가 따로 있어야 겹쳐 그릴 수 있다."""
    client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                files={"file": ("scan.mpr", scan_mpr(sweeps=3),
                                "application/octet-stream")})
    rows = client.get("/api/eis/spectra").json()
    ids = ",".join(str(row["id"]) for row in rows)
    points = client.get("/api/eis/points", params={"ids": ids}).json()
    assert len(points) == 3
    for item in points:
        assert len(item["frequency_hz"]) == 8
        assert item["frequency_hz"][0] > item["frequency_hz"][-1]


# --- 대시보드: 셀 한 줄 -----------------------------------------------------

def test_the_dashboard_counts_scans_by_file_not_by_sweep(client, sample_id):
    """스윕 21개는 스캔 **1개**다.

    스윕으로 세면 이 셀이 스물한 번 측정한 것처럼 보인다 -- 실제로는 파일
    하나를 SOC 를 훑으며 한 번 잰 것이다 (ADR 0022).
    """
    client.post("/api/eis/spectra/upload",
                params={"kind": "liquid", "sample_id": sample_id},
                files={"file": ("scan.mpr", scan_mpr(sweeps=4),
                                "application/octet-stream")})
    upload(client, sample_id=sample_id)

    rows = client.get("/api/eis/dashboard").json()["rows"]
    assert len(rows) == 1
    assert rows[0]["spectra"] == 5           # 스윕 4 + 단일 1
    assert rows[0]["scans"] == 1             # 파일 하나
    assert rows[0]["sample_name"] == "TEST-01"


def test_the_dashboard_leaves_resistance_blank_until_something_is_fitted(client,
                                                                         sample_id):
    """§0.4 — 안 맞췄다는 것과 저항이 0 이라는 것은 다른 말이다."""
    made = upload(client, sample_id=sample_id)
    row = client.get("/api/eis/dashboard").json()["rows"][0]
    assert row["fitted"] == 0
    assert row["series_resistance_ohm"] is None
    assert row["total_resistance_ohm"] is None
    assert row["last_circuit"] == ""

    client.post(f"/api/eis/spectra/{made['id']}/fit",
                params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)"})
    row = client.get("/api/eis/dashboard").json()["rows"][0]
    assert row["fitted"] == 1
    assert row["series_resistance_ohm"] == pytest.approx(5.0, rel=0.1)
    assert row["total_resistance_ohm"] == pytest.approx(65.0, rel=0.1)


def test_a_cell_with_both_kinds_says_neither(client, sample_id):
    """액체와 전고체의 아크는 이름부터 다르다 (ADR 0019).

    둘을 한 줄로 요약하면 그 줄이 거짓말을 한다 -- 종류 칸을 비우는 편이 맞다.
    """
    upload(client, sample_id=sample_id)                       # solid
    upload(client, name="b.mpr", rs=9.0, kind="liquid", cell_config="half",
           sample_id=sample_id)
    row = client.get("/api/eis/dashboard").json()["rows"][0]
    assert row["kind"] == ""
    # 셀 구성도 갈리면 같은 이유로 비운다.
    assert row["cell_config"] == ""


def test_the_dashboard_shows_what_is_not_attached_yet_as_its_own_row(client, sample_id):
    """붙이는 것은 일이고, 그 일이 **무엇에** 남아 있는지가 여기서 보여야 한다.

    수만 세면 "하나 있습니다" 까지만 알고 그게 어느 파일인지는 다른 화면에
    가야 안다.  줄로 내고, 셀 칸이 비어 있는 것 자체를 정보로 쓴다.
    """
    upload(client)                                  # 안 붙임
    upload(client, name="b.mpr", rs=9.0, sample_id=sample_id)
    body = client.get("/api/eis/dashboard").json()
    assert body["unattached"] == 1
    assert len(body["rows"]) == 2

    # 여기서 b.mpr 이 먼저인 것은 **나중에 올렸기** 때문이다 (아래 정렬 테스트).
    # 한때는 "붙은 줄이 먼저" 라는 규칙이 따로 있었는데, 그 규칙이 정확히 방금
    # 올린 줄(= 아직 안 붙은 줄)을 아래로 밀어내서 뺐다.
    attached, loose = body["rows"]
    assert attached["attached"] is True
    assert attached["sample_id"] == sample_id
    assert attached["name"] == "b.mpr"      # 셀 이름 말고 그 측정의 원래 이름
    assert loose["attached"] is False
    assert loose["sample_id"] is None
    assert loose["name"]


def test_an_unattached_row_still_shows_its_own_group(client):
    """측정은 셀 없이도 그룹을 가진다 (ADR 0027).

    셀을 통해서만 그룹을 읽으면 이 줄의 그룹 칸이 늘 비고, 화면은 "그룹 없는
    측정" 이라고 말하게 된다 -- 적혀 있는데 읽는 길이 없었을 뿐이다.
    """
    parent = client.post("/api/groups", json={"name": "전고체"}).json()
    child = client.post("/api/groups",
                        json={"name": "3차", "parent_id": parent["id"]}).json()
    out = upload(client)
    client.patch(f"/api/eis/spectra/{out['id']}", json={"group_id": child["id"]})

    row = client.get("/api/eis/dashboard").json()["rows"][0]
    assert row["attached"] is False
    assert row["group_id"] == child["id"]
    assert row["group_name"] == "3차"
    assert row["group_parent_name"] == "전고체"


def test_one_unattached_scan_is_one_row_not_twenty(client):
    """스윕이 스물인 SOC 스캔 하나가 스무 줄이 되면 표가 그것만으로 덮인다."""
    client.post("/api/eis/spectra/upload",
                params={"kind": "liquid"},
                files={"file": ("scan.mpr", scan_mpr(sweeps=4),
                                "application/octet-stream")})
    body = client.get("/api/eis/dashboard").json()
    assert body["unattached"] == 4
    assert len(body["rows"]) == 1
    assert body["rows"][0]["spectra"] == 4
    assert body["rows"][0]["scans"] == 1


# --- 스캔 섹션: 파일 하나를 SOC 축으로 (ADR 0022) ---------------------------

def _scan_with_fits(client, sweeps=4, circuit="R0-p(R1,CPE1)"):
    client.post("/api/eis/spectra/upload",
                params={"kind": "liquid", "cell_config": "half"},
                files={"file": ("scan.mpr", scan_mpr(sweeps=sweeps),
                                "application/octet-stream")})
    rows = client.get("/api/eis/spectra").json()
    client.post("/api/eis/fit-batch",
                json=[row["id"] for row in rows],
                params={"circuit": circuit})
    return rows


def test_only_a_file_with_several_sweeps_is_a_scan(client):
    """전·후 두 장은 스캔이 아니다 — 그건 목록 화면이 이미 하는 일이다."""
    upload(client)                                     # 한 장짜리
    client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                files={"file": ("two.mpr", scan_mpr(sweeps=2),
                                "application/octet-stream")})
    assert client.get("/api/eis/scans").json() == []

    client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                files={"file": ("scan.mpr", scan_mpr(sweeps=3, points=8),
                                "application/octet-stream")})
    scans = client.get("/api/eis/scans").json()
    assert len(scans) == 1
    assert scans[0]["sweeps"] == 3


def test_a_scan_lists_without_carrying_every_point(client):
    """목록은 목록이다.  스무 스윕의 값을 다 실어 보내면 목록이 무거워진다."""
    _scan_with_fits(client)
    scans = client.get("/api/eis/scans").json()
    assert scans[0]["points"] == []
    assert scans[0]["sweeps"] == 4
    assert scans[0]["fitted"] == 4
    assert scans[0]["purpose"] == "SOC별"


def test_a_scan_reads_back_as_an_soc_axis(client):
    rows = _scan_with_fits(client)
    scan = client.get(f"/api/eis/scans/{rows[0]['sha256']}").json()

    assert [p["sweep_index"] for p in scan["points"]] == [1, 2, 3, 4]
    capacities = [p["capacity_mah"] for p in scan["points"]]
    assert capacities == sorted(capacities)
    assert "R0" in scan["parameters"]
    assert all("R0" in p["values"] for p in scan["points"])
    # 저항이 이 셀에서 무엇인지도 같이 온다 -- 화면이 이름을 지어내지 않도록.
    assert scan["points"][0]["labels"].get("R1")


def test_an_unfitted_scan_says_so_instead_of_guessing(client):
    """§0.4 — 맞춘 적이 없으면 값이 없는 것이지, 0 이 아니다."""
    client.post("/api/eis/spectra/upload", params={"kind": "liquid"},
                files={"file": ("scan.mpr", scan_mpr(sweeps=3),
                                "application/octet-stream")})
    rows = client.get("/api/eis/spectra").json()
    scan = client.get(f"/api/eis/scans/{rows[0]['sha256']}").json()
    assert scan["fitted"] == 0
    assert scan["parameters"] == []
    assert all(p["fit_id"] is None and p["values"] == {} for p in scan["points"])
    # x 축은 여전히 있다 -- 스캔을 열어서 무엇을 잰 것인지는 볼 수 있어야 한다.
    assert all(p["potential_v"] is not None for p in scan["points"])


def test_the_best_fit_is_the_one_on_the_trend_not_the_latest(client):
    """SOC 스캔은 몇 점을 회로를 바꿔 다시 맞춘다.  추세선에는 잘 맞은 것이."""
    rows = _scan_with_fits(client)
    target = rows[1]["id"]
    good = client.get(f"/api/eis/spectra/{target}").json()["fits"][0]

    # 일부러 안 맞는 회로로 한 번 더 -- 이것이 '가장 최근' 이 된다.
    client.post(f"/api/eis/spectra/{target}/fit", params={"circuit": "R0"})

    scan = client.get(f"/api/eis/scans/{rows[0]['sha256']}").json()
    point = next(p for p in scan["points"] if p["spectrum_id"] == target)
    assert point["fit_id"] == good["id"]
    assert point["chi_squared"] == good["chi_squared"]


def test_a_missing_scan_is_a_404_not_an_empty_scan(client):
    assert client.get("/api/eis/scans/" + "f" * 64).status_code == 404


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


# --- 회로 자동 고르기 ---------------------------------------------------------


def test_auto_fits_every_preset_and_returns_the_best(client):
    """사람이 하던 일이 그대로 이것이다 — 회로를 바꿔 가며 맞춰 보고 χ² 를 본다.

    기본 회로 하나만 돌리면 그 회로가 이 셀에 안 맞을 때 "피팅이 이상하다" 로만
    보이는데, 실제로는 **회로가 틀린 것**이다.
    """
    made = upload(client, kind="solid", cell_config="full")
    presets = client.get("/api/eis/circuits").json()["combinations"]
    wanted = next(entry for entry in presets
                  if entry["kind"] == "solid" and entry["cell_config"] == "full")

    reply = client.post(f"/api/eis/spectra/{made['id']}/fit",
                        params={"circuit": "auto", "restarts": 2})
    assert reply.status_code == 201, reply.text
    best = reply.json()

    detail = client.get(f"/api/eis/spectra/{made['id']}").json()
    tried = {fit["circuit"] for fit in detail["fits"]}
    # 전부 저장한다 -- 안 맞는 회로도 발견이고, 버리면 다음 사람이 같은 것을
    # 다시 시도하고 같은 답을 기다린다.
    assert tried == {preset["circuit"] for preset in wanted["presets"]}

    converged = [fit for fit in detail["fits"]
                 if fit["converged"] and fit["chi_squared"] is not None]
    assert best["circuit"] in {fit["circuit"] for fit in converged}
    assert best["chi_squared"] == min(fit["chi_squared"] for fit in converged)


def test_auto_is_not_a_circuit_name(client):
    """`auto` 는 회로가 아니라 지시다 -- 회로로 읽히면 파서가 422 를 낸다."""
    made = upload(client)
    reply = client.post(f"/api/eis/spectra/{made['id']}/fit",
                        params={"circuit": "AUTO", "restarts": 1})
    assert reply.status_code == 201, reply.text
    assert reply.json()["circuit"] != "AUTO"


# --- 지름과 면적 --------------------------------------------------------------


def test_the_area_comes_from_the_diameter_when_it_is_blank(client):
    """캘리퍼로 재는 것은 지름이다.  면적만 물으면 매번 손으로 πd²/4 를 한다."""
    made = upload(client, kind="solid", cell_config="sym")
    client.patch(f"/api/eis/spectra/{made['id']}",
                 json={"diameter_mm": 10.0, "thickness_um": 500.0})
    detail = client.get(f"/api/eis/spectra/{made['id']}").json()
    assert detail["diameter_mm"] == 10.0
    # π (0.5 cm)² = 0.7854 cm²
    assert detail["area_cm2_effective"] == pytest.approx(0.785398, rel=1e-4)


def test_a_written_area_beats_the_diameter(client):
    """원이 아닌 전극이 있고, 그때 지름은 잴 수 있는 값이 아니다."""
    made = upload(client, kind="solid", cell_config="sym")
    client.patch(f"/api/eis/spectra/{made['id']}",
                 json={"diameter_mm": 10.0, "area_cm2": 1.33})
    detail = client.get(f"/api/eis/spectra/{made['id']}").json()
    assert detail["area_cm2_effective"] == pytest.approx(1.33)
    # 지름은 지워지지 않는다 -- 둘 다 사람이 적은 값이다.
    assert detail["diameter_mm"] == 10.0


def test_the_diameter_can_be_cleared(client):
    made = upload(client)
    client.patch(f"/api/eis/spectra/{made['id']}", json={"diameter_mm": 10.0})
    cleared = client.patch(f"/api/eis/spectra/{made['id']}",
                           json={"clear": ["diameter_mm"]}).json()
    assert cleared["diameter_mm"] is None


# --- 측정 자신의 조건 (ADR 0027) ------------------------------------------------


def test_a_spectrum_carries_its_own_conditions_without_a_cell(client):
    """셀에 안 붙은 측정이 많다 — EIS 만 보려고 잰 것, 셀을 만들기 전에 올린 것.

    그때도 "언제, 무엇을, 몇 도에서" 는 있다.  적을 데가 없던 것이 문제였다.
    """
    made = upload(client)
    patched = client.patch(f"/api/eis/spectra/{made['id']}", json={
        "test_date": "2026-08-20", "cathode_type": "High-Ni",
        "process": "dry", "temperature_c": 60.0,
    }).json()
    assert patched["sample_id"] is None
    assert patched["test_date_effective"] == "2026-08-20"
    assert patched["temperature_c_effective"] == 60.0
    # 빌려 온 것이 없다 -- 붙은 셀이 없으니 당연하다.
    assert patched["inherited"] == []


def test_a_blank_field_borrows_from_the_cell_and_says_so(client, sample_id):
    client.patch(f"/api/samples/{sample_id}",
                 json={"process": "wet", "temperature_c": 25.0})
    made = upload(client, sample_id=sample_id)
    out = client.get(f"/api/eis/spectra/{made['id']}").json()
    assert out["process_effective"] == "wet"
    assert out["temperature_c_effective"] == 25.0
    # 화면이 회색으로 그리려면 어디서 왔는지를 알아야 한다 (§0.4).
    assert set(out["inherited"]) >= {"process", "temperature_c"}


def test_what_is_written_here_beats_the_cell(client, sample_id):
    """같은 셀의 임피던스를 다른 온도에서 재는 일이 실제로 있다."""
    client.patch(f"/api/samples/{sample_id}", json={"temperature_c": 25.0})
    made = upload(client, sample_id=sample_id)
    out = client.patch(f"/api/eis/spectra/{made['id']}",
                       json={"temperature_c": -10.0}).json()
    assert out["temperature_c_effective"] == -10.0
    assert "temperature_c" not in out["inherited"]
    # 비우면 셀의 값이 도로 비쳐 보인다 -- 그것이 이 칸의 뜻이다.
    cleared = client.patch(f"/api/eis/spectra/{made['id']}",
                           json={"clear": ["temperature_c"]}).json()
    assert cleared["temperature_c_effective"] == 25.0
    assert "temperature_c" in cleared["inherited"]


def test_a_spectrum_can_sit_in_a_group_without_a_cell(client):
    """EIS 만 보려고 잰 묶음이 있다 — 셀이 없어도 그룹으로 모을 수 있어야 한다."""
    group = client.post("/api/groups", json={"name": "SOC 스캔 묶음"}).json()
    made = upload(client)
    out = client.patch(f"/api/eis/spectra/{made['id']}",
                       json={"group_id": group["id"]}).json()
    assert out["group_id_effective"] == group["id"]
    assert out["group_label"] == "SOC 스캔 묶음"


def test_a_subgroup_label_carries_its_parent(client):
    parent = client.post("/api/groups", json={"name": "건식"}).json()
    child = client.post("/api/groups",
                        json={"name": "80wt%", "parent_id": parent["id"]}).json()
    made = upload(client)
    out = client.patch(f"/api/eis/spectra/{made['id']}",
                       json={"group_id": child["id"]}).json()
    assert out["group_label"] == "건식 · 80wt%"


def test_a_group_that_does_not_exist_is_refused(client):
    made = upload(client)
    reply = client.patch(f"/api/eis/spectra/{made['id']}", json={"group_id": 9999})
    assert reply.status_code == 404


def test_the_dashboard_puts_the_newest_upload_on_top(client, sample_id):
    """이 표를 여는 가장 흔한 이유가 "방금 올린 것을 본다" 이다.

    그때 그것을 표에서 찾아야 하면 표가 일을 안 한 셈이다.  **잰 때가 아니라
    올린 때**로 센다 -- 지난달에 잰 파일을 오늘 올리는 일이 흔하고, 그때 사람이
    찾는 것은 "방금 올린 것" 이지 "가장 최근에 잰 것" 이 아니다.
    """
    upload(client, name="first.mpr", sample_id=sample_id)
    second = client.post("/api/samples", json={"name": "둘째 셀"}).json()["id"]
    upload(client, name="second.mpr", rs=9.0, sample_id=second)
    upload(client, name="third.mpr", rs=11.0)       # 안 붙임 -- 그래도 맨 위다

    rows = client.get("/api/eis/dashboard").json()["rows"]
    assert [r["name"] for r in rows] == ["third.mpr", "second.mpr", "first.mpr"]
    # 안 붙은 줄이 맨 위에 설 수 있어야 한다.  올린 직후가 바로 그 상태라,
    # 붙은 것을 위로 올리면 방금 올린 줄이 매번 아래로 밀린다.
    assert rows[0]["attached"] is False


def test_the_whole_library_is_newest_first(client):
    """전체 목록에서 사람이 찾는 것은 늘 **방금 올린 것**이다.

    사이클 번호로 정렬하면 서로 다른 셀의 1번들이 위에 모이고, 방금 올린
    200번은 한참 아래에 묻힌다 — 실측으로 그렇게 됐다.
    """
    old_one = upload(client, name="옛것")
    client.patch(f"/api/eis/spectra/{old_one['id']}", json={"at_cycle": 1})
    # 같은 바이트는 sha256 으로 하나로 묶인다 — 스윕 수를 바꿔 다른 파일로.
    new_one = upload(client, name="새것", rs=5.5)
    client.patch(f"/api/eis/spectra/{new_one['id']}", json={"at_cycle": 200})

    names = [row["name"] for row in client.get("/api/eis/spectra").json()]
    assert names[0] == "새것", names


def test_one_cells_spectra_stay_in_cycle_order(client):
    """한 셀 안에서는 사이클 번호가 사람이 보고 싶은 순서다 (ADR 0022).

    3번 다음이 200번이지 올린 순서가 아니다.  SOC 스캔의 스윕도 마찬가지다.
    """
    sample = client.post("/api/samples", json={"name": "순서 셀"}).json()
    late = upload(client, name="200번", sample_id=sample["id"])
    early = upload(client, name="3번", sample_id=sample["id"], rs=5.5)
    client.patch(f"/api/eis/spectra/{late['id']}", json={"at_cycle": 200})
    client.patch(f"/api/eis/spectra/{early['id']}", json={"at_cycle": 3})

    names = [row["name"] for row in
             client.get("/api/eis/spectra", params={"sample_id": sample["id"]}).json()]
    assert names == ["3번", "200번"], names
