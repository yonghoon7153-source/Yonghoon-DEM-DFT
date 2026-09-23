"""EIS 검수와 재파싱 — 저장된 것 전부를 한 번에 (ADR 0040).

검수는 **읽기만** 한다는 약속과, 재파싱은 **파생 데이터만** 바꾼다는 약속을
시험한다.  판정 규칙 하나하나는 `packages/wrdkit/tests/test_eis_audit.py` 에
있다 — 여기는 DB 에서 그 규칙까지 값이 제대로 오는지를 본다.
"""

import numpy as np
import pytest
import synthetic_eis as S

#: 실측 `2600922_No1_55_sym_60um_#1_C01` 의 맞춤값 — 블로킹 꼬리가 없다.
USER = {"rs": 4.897, "r1": 10.42, "q1": 3.06e-5, "n1": 0.658,
        "r2": 6.635, "q2": 1.36e-3, "n2": 0.757}
BLOCKING_TAIL = "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"


def mpr(q_block=None, **values) -> bytes:
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, q_block=q_block, **values)
    return S.build_mpr(S.spectrum_columns(frequency, z))


def upload(client, content: bytes, name: str, **params) -> dict:
    params = {"kind": "solid", "cell_config": "sym", **params}
    response = client.post("/api/eis/spectra/upload", params=params,
                           files={"file": (name, content,
                                           "application/octet-stream")})
    assert response.status_code == 201, response.text
    return response.json()


def fit(client, spectrum_id: int, circuit: str) -> dict:
    response = client.post(f"/api/eis/spectra/{spectrum_id}/fit",
                           params={"circuit": circuit})
    assert response.status_code == 201, response.text
    return response.json()


def audit(client) -> dict:
    response = client.get("/api/eis/audit")
    assert response.status_code == 200, response.text
    return response.json()


def entry(report: dict, spectrum_id: int) -> dict:
    return next(one for one in report["spectra"] if one["id"] == spectrum_id)


def codes(item: dict, severity: str | None = None) -> list[str]:
    return [f["code"] for f in item["findings"]
            if severity is None or f["severity"] == severity]


def user_cell(client) -> dict:
    out = upload(client, mpr(**USER), "2600922_No1_55_sym_60um_#1_C01.mpr")
    client.patch(f"/api/eis/spectra/{out['id']}",
                 json={"thickness_um": 60.0, "diameter_mm": 10.0})
    fit(client, out["id"], BLOCKING_TAIL)
    return out


def test_the_cell_that_started_it_is_named_a_problem(client):
    out = user_cell(client)
    item = entry(audit(client), out["id"])
    assert item["worst"] == "problem"
    assert "blocking_element_on_open_cell" in codes(item, "problem")
    assert "symmetric_cell_does_not_block" in codes(item, "check")
    assert item["blocking"]["blocking"] is False
    assert item["circuit"] == BLOCKING_TAIL
    # 두께와 지름이 커패시턴스 판정까지 온다 (지름 → 면적).
    assert item["thickness_um"] == pytest.approx(60.0)
    assert item["area_cm2"] == pytest.approx(np.pi / 4)
    arcs = {arc["resistor"]: arc for arc in item["arcs"]}
    assert set(arcs) == {"R1", "R2"}
    assert all(arc["capacitance_f"] for arc in arcs.values())


def test_a_real_blocking_cell_fitted_right_has_no_problem(client):
    """산화물 펠릿처럼 두 아크가 다 보이는 블로킹 셀 (700 µm, 10 mm).

    벌크 C_eff ≈ 3e-11 F (C·l/A ≈ 2.7e-12, 꼭지 ≈ 540 kHz), 입계 ≈ 3e-9 F
    (C·l/A ≈ 2.7e-10, 꼭지 ≈ 2.6 kHz).  처음 픽스처는 벌크에 3.9e-10 F 를
    줬는데, 이 두께에서 그것은 C·l/A 3.5e-11 — **입계의 크기**라 검수가
    옳게 잡았다.  벌크의 커패시턴스는 두께가 두꺼울수록 더 작아야 한다."""
    out = upload(client, mpr(q_block=1e-6, rs=2.0, r1=1e4, q1=6.3e-11, n1=0.95,
                             r2=2e4, q2=1.3e-8, n2=0.85),
                 "SS_LLZO_SS_sym_700um.mpr")
    client.patch(f"/api/eis/spectra/{out['id']}",
                 json={"thickness_um": 700.0, "diameter_mm": 10.0})
    fit(client, out["id"], BLOCKING_TAIL)
    item = entry(audit(client), out["id"])
    assert item["blocking"]["blocking"] is True
    assert "problem" not in [f["severity"] for f in item["findings"]], item["findings"]


def test_the_audit_writes_nothing(client):
    """캐시가 없으면 원본에서 읽되 **쓰지 않는다** — 검수가 고치면 무엇이
    틀려 있었는지가 지워진다."""
    from app import storage
    out = user_cell(client)
    storage.drop_spectrum_cache(out["id"])
    fits_before = client.get("/api/eis/fits", params={"ids": out["id"]}).json()

    item = entry(audit(client), out["id"])
    assert "cache_missing" in codes(item, "note")
    # 모양은 원본에서 읽어서 여전히 본다.
    assert item["blocking"]["blocking"] is False
    assert not storage.spectrum_points_path(out["id"]).exists()
    assert client.get("/api/eis/fits", params={"ids": out["id"]}).json() == fits_before


def test_a_lost_original_is_a_problem(client):
    from app import storage
    out = upload(client, mpr(**USER), "lonely_sym_60um.mpr")
    storage.spectrum_upload_path(out["sha256"], "mpr").unlink()
    item = entry(audit(client), out["id"])
    assert "original_missing" in codes(item, "problem")


def test_an_unfitted_spectrum_is_only_noted(client):
    out = upload(client, mpr(**USER), "unfitted.mpr", cell_config="full")
    item = entry(audit(client), out["id"])
    assert codes(item) == ["not_fitted"]
    assert item["worst"] == "note"


def test_the_counts_add_up_to_the_spectra(client):
    user_cell(client)
    # 같은 바이트면 중복으로 합쳐진다 — 다른 셀이어야 둘이다.
    upload(client, mpr(**dict(USER, rs=6.0)), "unfitted.mpr", cell_config="full")
    report = audit(client)
    assert report["total"] == 2
    assert sum(report["counts"].values()) == 2
    assert report["counts"]["problem"] == 1


def test_the_text_report_is_what_bml_prints(client):
    out = user_cell(client)
    response = client.get("/api/eis/audit", params={"format": "text"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    text = response.text
    assert text.startswith("EIS 검수 — ")
    assert "━━ 문제 (1)" in text
    assert f"#{out['id']}" in text and "2600922_No1_55_sym_60um_#1_C01" in text
    assert "[문제]" in text and "`R0-p(R1,CPE1)-p(R2,CPE2)`" in text
    assert "아크 R1" in text                  # 다시 따져 볼 수 있는 수들


def test_an_unknown_format_is_refused(client):
    assert client.get("/api/eis/audit", params={"format": "xml"}).status_code == 422


# -- 온도 스캔 ---------------------------------------------------------------------

def upload_scan(client, resistances) -> str:
    text = S.build_mpt_temperature_scan(resistances=resistances)
    out = client.post(
        "/api/eis/spectra/upload",
        params={"kind": "solid", "cell_config": "sym", "purpose": "이온전도도"},
        files={"file": ("B12_activationE.mpt", text.encode("utf-8"),
                        "text/plain")}).json()
    return out["sha256"]


def test_a_decimal_slip_in_a_temperature_scan_is_caught(client):
    true = [9.69, 14.56, 34.66, 94.30, 300.0]
    sha = upload_scan(client, true)
    typed = [9.69, 14.56, 346.6, 94.30, 300.0]           # 스윕 3: 소수점
    client.put(f"/api/eis/scans/{sha}/temperature",
               json={"temperature_c": [60, 40, 20, 0, -20]})
    client.put(f"/api/eis/scans/{sha}/resistance", json={"resistance_ohm": typed})
    report = audit(client)
    (scan,) = [one for one in report["scans"] if one["sha256"] == sha]
    assert scan["symmetric"] is True
    assert [row["typed_ohm"] for row in scan["rows"]] == typed
    slips = [f for f in scan["findings"] if f["code"] == "typed_outside_spectrum"]
    assert len(slips) == 1 and "스윕 3" in slips[0]["message"]


def test_reading_the_arc_end_in_a_temperature_scan_is_not_a_slip(client):
    """이 합성 파일의 실수축 교점은 약 2 Ω 이고 맞게 읽은 값은 9.69 Ω 이다 —
    교점과의 비로 보면 오경보가 난다."""
    true = [9.69, 14.56, 34.66]
    sha = upload_scan(client, true)
    client.put(f"/api/eis/scans/{sha}/temperature", json={"temperature_c": [60, 40, 20]})
    client.put(f"/api/eis/scans/{sha}/resistance", json={"resistance_ohm": true})
    (scan,) = [one for one in audit(client)["scans"] if one["sha256"] == sha]
    assert scan["rows"][0]["crossing_ohm"] < true[0] / 3
    assert "typed_outside_spectrum" not in [f["code"] for f in scan["findings"]]


# -- 재파싱 -------------------------------------------------------------------------

def test_reparse_rewrites_stale_points_and_names_them(client):
    """옛 파서가 캐시에 남긴 점 — 여기서는 손으로 비튼 것으로 흉내낸다."""
    from app import storage
    from wrdkit.eis import Spectrum
    out = upload(client, mpr(**USER), "stale.mpr")
    good = storage.load_spectrum(out["id"], out["sha256"])
    bent = Spectrum(good.frequency_hz, good.z_re * 1.02, good.z_im)
    storage.cache_spectrum(out["id"], bent, out["sha256"])

    response = client.post("/api/eis/reparse")
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["total"] == 1 and body["reparsed"] == 1
    (changed,) = body["changed"]
    assert changed["id"] == out["id"] and "%" in changed["detail"]
    fresh = storage.load_spectrum(out["id"], out["sha256"])
    assert np.allclose(fresh.z_re, good.z_re)


def test_reparse_of_unchanged_points_reports_no_change(client):
    upload(client, mpr(**USER), "same.mpr")
    body = client.post("/api/eis/reparse").json()
    assert body["reparsed"] == 1 and body["changed"] == [] and body["failed"] == []


def test_reparse_does_not_touch_a_scan_whose_sweep_count_moved(client):
    """번호가 가리키는 스윕이 바뀌었을 수 있다 — 조용히 덮으면 다른 온도의
    점이 그 온도 이름으로 들어간다."""
    from sqlmodel import Session, select

    from app import storage
    from app.db import engine
    from app.models import SpectrumRecord
    sha = upload_scan(client, [9.69, 14.56, 34.66])
    with Session(engine) as session:
        rows = session.exec(select(SpectrumRecord).where(
            SpectrumRecord.sha256 == sha)).all()
        for row in rows:
            row.sweep_count = 4                     # 옛 분할이 넷으로 셌다고 치자
            session.add(row)
        session.commit()
        ids = [row.id for row in rows]
    before = {i: storage.load_spectrum(i, sha).z_re.copy() for i in ids}

    body = client.post("/api/eis/reparse").json()
    assert body["reparsed"] == 0
    assert len(body["failed"]) == 3
    assert "3개 읽히는데 기록은 4개" in body["failed"][0]["reason"]
    for i in ids:
        assert np.array_equal(storage.load_spectrum(i, sha).z_re, before[i])


def test_reparse_names_a_missing_original(client):
    from app import storage
    out = upload(client, mpr(**USER), "gone.mpr")
    storage.spectrum_upload_path(out["sha256"], "mpr").unlink()
    body = client.post("/api/eis/reparse").json()
    assert body["reparsed"] == 0
    assert body["failed"][0]["reason"] == "원본 파일이 없습니다"


def test_reparse_speaks_text_for_bml(client):
    """`bml reparse` 는 이 글을 그대로 찍는다 — 셸에서 JSON 을 깎지 않는다."""
    from app import storage
    from wrdkit.eis import Spectrum
    out = upload(client, mpr(**USER), "stale.mpr")
    good = storage.load_spectrum(out["id"], out["sha256"])
    storage.cache_spectrum(out["id"], Spectrum(good.frequency_hz, good.z_re * 1.5,
                                               good.z_im), out["sha256"])
    gone = upload(client, mpr(**dict(USER, rs=7.0)), "gone.mpr")
    storage.spectrum_upload_path(gone["sha256"], "mpr").unlink()

    response = client.post("/api/eis/reparse", params={"format": "text"})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    lines = response.text.splitlines()
    assert lines[0] == "EIS 원본 1/2 개를 다시 읽었습니다."
    assert any(line.startswith(f"    #{out['id']} stale") for line in lines)
    assert any("원본 파일이 없습니다" in line for line in lines)


def test_a_scan_without_caches_is_read_from_its_original_once(client, monkeypatch):
    """스윕 셋이 한 원본이다 — 캐시가 다 사라져도 원본은 **한 번만** 파싱한다.
    바이트를 들고 있지도 않는다: 52 MB `.mpt` 열 개가 검수 내내 메모리에
    남으면 랩 PC 의 WSL 이 먼저 지친다."""
    from app import storage
    from app.routers import eis_audit
    sha = upload_scan(client, [9.69, 14.56, 34.66])
    rows = [row for row in client.get("/api/eis/spectra").json()
            if row["sha256"] == sha]
    for row in rows:
        storage.drop_spectrum_cache(row["id"])
    calls = []
    real = eis_audit._parse_sweeps

    def counting(content, name):
        calls.append(name)
        return real(content, name)

    monkeypatch.setattr(eis_audit, "_parse_sweeps", counting)
    report = audit(client)
    assert len(calls) == 1
    for row in rows:
        assert "cache_missing" in codes(entry(report, row["id"]), "note")
    (scan,) = [one for one in report["scans"] if one["sha256"] == sha]
    assert all(line["crossing_ohm"] is not None for line in scan["rows"])


def test_a_scan_row_carries_its_verdict_and_when_it_was_measured(client):
    """온도 스캔의 첫 스윕 문제(실측 9개 중 5개)를 가르려면 각 스윕이 언제
    쟀는지, 앞에서 얼마나 쉬었는지가 보여야 한다 — 캐시의 `time/s` 에서."""
    sha = upload_scan(client, [9.69, 14.56, 34.66])
    (scan,) = [one for one in audit(client)["scans"] if one["sha256"] == sha]
    first, second = scan["rows"][:2]
    assert first["blocking"] is not None and first["phase_deg"] is not None
    # 합성 파일: 스윕마다 앞에 1 h 휴지 네 줄 — 두 번째 스윕은 앞 스윕 끝에서
    # 네 시간 뒤에 시작한다.
    assert second["start_s"] - first["end_s"] == pytest.approx(4 * 3600, rel=0.01)
    text = client.get("/api/eis/audit", params={"format": "text"}).text
    assert "앞에서 쉰 시간" in text and "4.0 h" in text


def test_the_offered_circuits_reach_the_suggestion(client):
    """대칭셀 보기에는 복합전극 모델 `R0-TL1` 이 있다 — 안 막는 셀에 블로킹
    꼬리를 단 맞춤에는 그것도 권한다."""
    out = user_cell(client)
    item = entry(audit(client), out["id"])
    (finding,) = [f for f in item["findings"]
                  if f["code"] == "blocking_element_on_open_cell"]
    assert "`R0-TL1`" in finding["message"]


def test_the_file_name_is_not_taken_for_the_shown_name(client):
    """화면 이름은 대칭셀인데 파일 이름이 풀셀 — "이름은 풀셀" 이라고 하면 틀린
    말이다 (실측 260831_Poly(L&F)_60um_sym 두 셀)."""
    out = upload(client, mpr(**dict(USER, rs=5.5)), "Poly_60um_full_01.mpr")
    client.patch(f"/api/eis/spectra/{out['id']}", json={"name": "Poly_60um_sym_01"})
    item = entry(audit(client), out["id"])
    notes = [f for f in item["findings"] if f["code"] == "file_name_differs"]
    assert notes and "Poly_60um_full_01.mpr" in notes[0]["message"]
    assert "config_differs_from_name" not in codes(item)
