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


def test_each_finding_says_which_paper_it_rests_on(client):
    """판정이 기대는 논문 기록 (ADR 0042) — 판정은 id 를, 보고서는 쪽까지."""
    out = user_cell(client)
    report = audit(client)
    item = entry(report, out["id"])
    (open_cell,) = [f for f in item["findings"]
                    if f["code"] == "blocking_element_on_open_cell"]
    assert "ISW1990.no-spike-means-electronic" in open_cell["refs"]
    cited = {ref["id"]: ref for ref in report["references"]}
    assert cited["ISW1990.no-spike-means-electronic"]["citation"].startswith(
        "Irvine–Sinclair–West 1990, p. 135")
    assert cited["ISW1990.no-spike-means-electronic"]["quote"]
    # 같은 기록은 한 번만.
    assert len(cited) == len(report["references"])

    text = client.get("/api/eis/audit", params={"format": "text"}).text
    assert "KK 잔차 최대" in text
    assert "[근거 1" in text
    assert "━━ 근거 (" in text
    assert "[1] " in text.split("━━ 근거 (")[1]


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
    # 합성 점은 KK 를 만족한다 — 검사가 돌았고 아무 말도 하지 않는다 (ADR 0043).
    assert item["kk"]["judged"] is True
    assert item["kk"]["max_residual"] < 0.02
    assert not [f for f in item["findings"] if f["code"].startswith("kk_")]


def test_a_current_range_switch_is_named_on_the_kk_line(client):
    """EC-Lab 의 ``I Range`` 가 스윕 중에 바뀐 자리에서 이득이 4 % 뛴 펠릿 —
    검수가 그 주파수를 적고, 옆의 KK 어긋남을 셀이 아니라 기기 쪽으로 읽는다
    (실측 두 번째 검수: 황화물 펠릿 11 개가 64–410 Hz 에서 함께 어긋났다)."""
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, q_block=1e-6, rs=2.0, r1=1e4, q1=6.3e-11, n1=0.95,
                  r2=2e4, q2=1.3e-8, n2=0.85)
    below = frequency < 90
    columns = S.spectrum_columns(frequency, np.where(below, z * 1.04, z))
    columns["I Range"] = np.where(below, 36, 37)
    out = upload(client, S.build_mpr(columns), "SS_LLZO_SS_sym_700um.mpr")
    client.patch(f"/api/eis/spectra/{out['id']}",
                 json={"thickness_um": 700.0, "diameter_mm": 10.0})
    fit(client, out["id"], BLOCKING_TAIL)
    item = entry(audit(client), out["id"])
    edge = int(np.argmax(below))
    expected = float(np.sqrt(frequency[edge] * frequency[edge - 1]))
    assert item["kk"]["range_switches_hz"] == [pytest.approx(expected, rel=1e-4)]
    assert "kk_range_switch" in codes(item, "note")
    assert "kk_violation" not in codes(item)
    text = client.get("/api/eis/audit", params={"format": "text"}).text
    assert f"전류 범위가 {expected:.3g} Hz 에서 바뀐 자리" in text

    # 자세히 적는 스펙트럼(확인·문제)은 KK 줄에도 그 자리를 적는다 — 셀 구성을
    # 비워 둔 전고체 스펙트럼은 확인이다 (실측 B18).
    columns["time/s"] = columns["time/s"] + 1.0        # 다른 파일 (sha256 이 같으면 같은 기록)
    blank = upload(client, S.build_mpr(columns), "B18_like.mpr", cell_config="")
    assert blank["id"] != out["id"]
    assert "config_missing" in codes(entry(audit(client), blank["id"]), "check")
    text = client.get("/api/eis/audit", params={"format": "text"}).text
    assert f"· 전류 범위 바뀜 {expected:.3g} Hz" in text


def test_a_point_the_kk_test_cannot_draw_is_not_held_against_the_circuit(client):
    """맞춤 검수가 같은 스펙트럼의 KK 결과를 받는다 — 맞는 회로로 맞춘 셀에서 튄
    점 하나(33 Hz, +14 %)를 "그 주파수의 모양을 회로가 못 그립니다" 로 적지 않는다
    (실측 mid_Ni #37)."""
    frequency = S.log_sweep(1e6, 1e-2, 12)
    z = S.randles(frequency, **USER)
    z[int(np.argmin(np.abs(frequency - 33)))] *= 1.14
    out = upload(client, S.build_mpr(S.spectrum_columns(frequency, z)),
                 "flying_point_sym_60um.mpr")
    fit(client, out["id"], "R0-p(R1,CPE1)-p(R2,CPE2)")
    item = entry(audit(client), out["id"])
    assert item["misfit_max"] > 0.10                   # 맞춤은 그 점에서 10 % 넘게 빗나간다
    assert [one for one in codes(item) if one.startswith("kk_")]
    assert not [one for one in codes(item) if one.startswith("misfit")]


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


def test_a_wrong_way_first_step_is_said_once_in_a_scan(client):
    """실측 B13·B15·B18: 60→50 °C 만 거꾸로인 스캔에 "다시 읽어 주세요" (확인) 와
    "첫 스윕만 거꾸로 갑니다" (참고) 가 같은 사실로 함께 떴다 — 이제 참고 하나."""
    typed = [9.0, 8.5, 14.56, 34.66, 94.30]
    sha = upload_scan(client, typed)
    for point in client.get(f"/api/eis/scans/{sha}").json()["points"]:
        client.patch(f"/api/eis/spectra/{point['spectrum_id']}",
                     json={"thickness_um": 700.0, "diameter_mm": 10.0})
    client.put(f"/api/eis/scans/{sha}/temperature",
               json={"temperature_c": [60, 50, 40, 20, 0]})
    client.put(f"/api/eis/scans/{sha}/resistance", json={"resistance_ohm": typed})
    (scan,) = [one for one in audit(client)["scans"] if one["sha256"] == sha]
    assert "first_sweep_suspect" in codes(scan)
    assert not [f for f in scan["findings"] if "안 내려가는 구간" in f["message"]]


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
    """대칭셀 보기의 배선 L 이 든 블로킹 회로가 권하는 회로로 온다 — 꼬리를
    아크로 흉내 낸 펠릿에 `L1-R0-CPE1` 은 보기에만 있는 회로다.  보기의 첫 줄
    `R0-TL1` 은 끝이 막아도 권하지 않는다 (펠릿에 복합전극 모델)."""
    out = upload(client, mpr(q_block=2e-6, rs=8.0, r1=1e-3, q1=1e-12, n1=0.9,
                             r2=1e-3, q2=1e-12, n2=0.9),
                 "SS_sulfide_SS_sym_700um.mpr")
    client.patch(f"/api/eis/spectra/{out['id']}",
                 json={"thickness_um": 700.0, "diameter_mm": 10.0})
    fit(client, out["id"], "R0-p(R1,CPE1)")
    item = entry(audit(client), out["id"])
    (finding,) = [f for f in item["findings"] if f["code"] == "tail_mimicked_by_arc"]
    assert "`L1-R0-CPE1`" in finding["message"]
    assert "TL1" not in finding["message"]


def test_the_file_name_is_not_taken_for_the_shown_name(client):
    """화면 이름은 대칭셀인데 파일 이름이 풀셀 — "이름은 풀셀" 이라고 하면 틀린
    말이다 (실측 260831_Poly(L&F)_60um_sym 두 셀)."""
    out = upload(client, mpr(**dict(USER, rs=5.5)), "Poly_60um_full_01.mpr")
    client.patch(f"/api/eis/spectra/{out['id']}", json={"name": "Poly_60um_sym_01"})
    item = entry(audit(client), out["id"])
    notes = [f for f in item["findings"] if f["code"] == "file_name_differs"]
    assert notes and "Poly_60um_full_01.mpr" in notes[0]["message"]
    assert "config_differs_from_name" not in codes(item)


def test_the_headline_names_the_tail_when_the_tail_decided():
    """실측 풀셀 #7 이 "저주파 위상 -5° (막음)" 으로 찍혔다 — 판정은 꼬리(≥ 60°)가
    냈는데 줄에는 위상만 있어, 수와 판정이 서로 어긋나 보였다."""
    from app.routers.eis_audit import _block, _Numbers
    from app.schemas import AuditSpectrumOut

    def headline(**blocking):
        one = AuditSpectrumOut(id=7, name="Dcell17", kind="solid", sha256="0" * 64,
                               blocking=blocking)
        return "\n".join(_block(one, _Numbers()))

    assert "저주파 위상 -5°, 꼬리 72° (막음)" in headline(
        blocking=True, phase_deg=-5.2, tail_deg=72.4)
    assert "저주파 위상 -9°, 꼬리 45° (애매)" in headline(
        blocking=None, phase_deg=-9.0, tail_deg=44.6)
    # 위상만으로 막는 셀에는 꼬리를 적지 않는다 — 판정을 낸 수 하나면 된다.
    assert "저주파 위상 -74° (막음)" in headline(
        blocking=True, phase_deg=-74.0, tail_deg=80.0)
    assert "저주파 위상 0° (안 막음)" in headline(blocking=False, phase_deg=0.2)
