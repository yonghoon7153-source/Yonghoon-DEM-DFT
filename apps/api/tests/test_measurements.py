"""한 셀의 세 측정이 서로를 찾는다.

세 섹션은 독립이지만 셀은 하나다.  붙어 있는 것만 여기 나오고, 이름이
비슷하다고 같은 셀로 묶지 않는다 -- 이름은 기록이지 관계가 아니다.
"""

import synthetic_eis as S

import synthetic


def gitt_wrd() -> bytes:
    return synthetic.build_wrd(synthetic.make_gitt())


def _attach_cycling(client, sample_id, wrd_bytes):
    return client.post("/api/runs/upload", params={"sample_id": sample_id},
                       files={"file": ("cyc.wrd", wrd_bytes,
                                       "application/octet-stream")}).json()


def _attach_eis(client, sample_id):
    frequency = S.log_sweep(1e5, 1e-1, 6)
    blob = S.build_mpr(S.spectrum_columns(frequency, S.randles(frequency)))
    return client.post("/api/eis/spectra/upload",
                       params={"kind": "liquid", "sample_id": sample_id},
                       files={"file": ("z.mpr", blob,
                                       "application/octet-stream")}).json()


def _upload_gitt(client, sample_id=None):
    params = {} if sample_id is None else {"sample_id": sample_id}
    return client.post("/api/gitt/runs/upload", params=params,
                       files={"file": ("g.wrd", gitt_wrd(),
                                       "application/octet-stream")})


def test_a_cell_lists_all_three_kinds(client, sample_id, wrd_bytes):
    _attach_cycling(client, sample_id, wrd_bytes)
    _attach_eis(client, sample_id)
    assert _upload_gitt(client, sample_id).status_code == 201

    body = client.get(f"/api/samples/{sample_id}/measurements").json()
    assert body["sample_id"] == sample_id
    assert len(body["cycling"]) == 1
    assert len(body["eis"]) == 1
    assert len(body["gitt"]) == 1
    # 각 줄은 그 종류에서만 뜻이 있는 한 줄을 들고 온다.
    assert "사이클" in body["cycling"][0]["detail"]
    assert "Hz" in body["eis"][0]["detail"]
    assert "펄스" in body["gitt"][0]["detail"]


def test_an_unattached_measurement_belongs_to_nobody(client, sample_id):
    """셀을 만들기 전에 파일부터 올리는 순서가 흔하다 -- 그 상태가 정상이다."""
    made = _upload_gitt(client).json()
    assert made["sample_id"] is None
    assert made["sample_name"] is None
    assert client.get(f"/api/samples/{sample_id}/measurements").json()["gitt"] == []


def test_a_gitt_record_can_be_attached_later(client, sample_id):
    made = _upload_gitt(client).json()
    patched = client.patch(f"/api/gitt/runs/{made['id']}",
                           json={"sample_id": sample_id})
    assert patched.status_code == 200
    assert patched.json()["sample_id"] == sample_id
    # 이름도 같이 온다 -- 목록이 셀을 한 번 더 묻지 않도록.
    assert patched.json()["sample_name"] == "TEST-01"

    body = client.get(f"/api/samples/{sample_id}/measurements").json()
    assert [m["id"] for m in body["gitt"]] == [made["id"]]


def test_a_gitt_record_can_be_detached(client, sample_id):
    made = _upload_gitt(client, sample_id).json()
    # `sample_id: null` 은 "안 보냄" 과 구별되지 않으므로 clear 를 쓴다.
    out = client.patch(f"/api/gitt/runs/{made['id']}",
                       json={"clear": ["sample_id"]}).json()
    assert out["sample_id"] is None
    assert client.get(f"/api/samples/{sample_id}/measurements").json()["gitt"] == []


def test_attaching_to_a_cell_that_is_not_there_is_refused(client):
    """없는 셀에 붙이면 어느 화면에도 안 나온다 -- 지워진 것처럼 보인다."""
    assert _upload_gitt(client, 9999).status_code == 404
    made = _upload_gitt(client).json()
    assert client.patch(f"/api/gitt/runs/{made['id']}",
                        json={"sample_id": 9999}).status_code == 404


def test_re_uploading_the_same_file_attaches_it_but_never_moves_it(client,
                                                                   sample_id):
    """파일부터 올려 두고 나중에 셀을 만드는 순서를 받아 준다.

    다만 이미 붙어 있으면 옮기지 않는다 -- 남의 셀에서 떼어 오는 것이 된다.
    """
    made = _upload_gitt(client).json()
    again = _upload_gitt(client, sample_id).json()
    assert again["id"] == made["id"]
    assert again["sample_id"] == sample_id

    other = client.post("/api/samples", json={"name": "OTHER"}).json()["id"]
    third = _upload_gitt(client, other).json()
    assert third["sample_id"] == sample_id      # 그대로다


def test_the_gitt_list_can_be_narrowed_to_one_cell(client, sample_id):
    _upload_gitt(client, sample_id)
    assert len(client.get("/api/gitt/runs",
                          params={"sample_id": sample_id}).json()) == 1
    other = client.post("/api/samples", json={"name": "OTHER"}).json()["id"]
    assert client.get("/api/gitt/runs", params={"sample_id": other}).json() == []


def test_a_missing_cell_is_a_404_not_an_empty_list(client):
    assert client.get("/api/samples/9999/measurements").status_code == 404
