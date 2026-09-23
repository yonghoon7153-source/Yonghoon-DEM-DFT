"""`bml refit` — 검수가 권한 회로로 한꺼번에 다시 맞춘다 (ADR 0045).

두 합성 펠릿이 이 기능의 전부다.  꼬리를 아크로 흉내 낸 맞춤은 권한 회로로
바뀌고, 옛 맞춤은 남고, 되돌리면 돌아간다.  아크가 정말 보이는 펠릿은 아크 없는
회로로 바꾸지 않고, 그 까닭을 검수의 문장으로 적는다.
"""

import numpy as np
import synthetic_eis as S

from wrdkit.eis.circuit import parse_circuit

FREQUENCY = S.log_sweep(7e6, 10.0, 10)


def pellet_mpr(circuit: str, values: dict[str, float]) -> bytes:
    model = parse_circuit(circuit)
    z = model.impedance([values[name] for name in model.parameter_names], FREQUENCY)
    return S.build_mpr(S.spectrum_columns(FREQUENCY, z))


#: 황화물 블로킹 펠릿 — 배선 L + 전해질 R + 이중층 CPE (실측 B15 #2 의 쌍둥이).
BLOCKING = ("L1-R0-CPE1", {"L1": 1.73e-6, "R0": 8.3, "CPE1_Q": 1.9e-6, "CPE1_n": 0.86})
#: 전극 크기 아크가 정말 보이는 펠릿.
VISIBLE_ARC = ("L1-R0-p(R1,CPE1)-CPE2",
               {"L1": 1.7e-6, "R0": 8.0, "R1": 200.0, "CPE1_Q": 2e-6, "CPE1_n": 0.9,
                "CPE2_Q": 1e-5, "CPE2_n": 0.9})


def pellet(client, name, truth, fitted_with):
    """올리고, 두께·면적을 적고, ``fitted_with`` 로 맞춘다."""
    created = client.post("/api/eis/spectra/upload",
                          params={"kind": "solid", "cell_config": "sym"},
                          files={"file": (name, pellet_mpr(*truth),
                                          "application/octet-stream")})
    assert created.status_code == 201, created.text
    spectrum_id = created.json()["id"]
    client.patch(f"/api/eis/spectra/{spectrum_id}",
                 json={"thickness_um": 700, "area_cm2": 0.785})
    fit = client.post(f"/api/eis/spectra/{spectrum_id}/fit",
                      params={"circuit": fitted_with}).json()
    assert fit["converged"], fit["reason"]
    return spectrum_id, fit


def fits_of(client, spectrum_id):
    return client.get(f"/api/eis/spectra/{spectrum_id}").json()["fits"]


def audit_codes(client, spectrum_id):
    report = client.get("/api/eis/audit").json()
    one = next(item for item in report["spectra"] if item["id"] == spectrum_id)
    return one, [finding["code"] for finding in one["findings"]]


def test_the_audit_refits_what_it_can_and_the_old_fit_stays(client):
    spectrum_id, old = pellet(client, "B15_pellet.mpr", BLOCKING, "R0-p(R1,CPE1)")
    before, codes = audit_codes(client, spectrum_id)
    assert "tail_mimicked_by_arc" in codes
    # 판정이 회로를 구조로 싣는다 — `bml refit` 은 문장을 긁지 않는다.
    tail = next(f for f in before["findings"] if f["code"] == "tail_mimicked_by_arc")
    assert tail["circuits"][0] == "L1-R0-CPE1"

    # 맞춰 보기만 — 아무것도 저장하지 않는다.
    dry = client.post("/api/eis/audit/refit", params={"dry_run": True}).json()
    assert (dry["targets"], dry["changed"], dry["kept"]) == (1, 1, 0)
    assert dry["spectra"][0]["new_circuit"] == "L1-R0-CPE1"
    assert dry["spectra"][0]["new_fit_id"] is None
    assert len(fits_of(client, spectrum_id)) == 1

    done = client.post("/api/eis/audit/refit").json()
    assert done["origin"].startswith("refit-")
    (one,) = done["spectra"]
    assert one["old_fit_id"] == old["id"]
    assert [p["code"] for p in one["problems"]] == ["tail_mimicked_by_arc"]
    assert one["new_problems"] == []
    assert one["tries"][0]["start"] == "seeded" and one["tries"][0]["accepted"]

    fits = fits_of(client, spectrum_id)
    assert len(fits) == 2, "옛 맞춤은 지우지 않는다"
    (used,) = [fit for fit in fits if fit["in_use"]]
    assert used["id"] == one["new_fit_id"]
    assert used["circuit"] == "L1-R0-CPE1" and used["origin"] == done["origin"]
    assert used["chosen_at"] is not None
    # 다음 검수에서도 받아들여진 그대로다 — 같은 길로 검수했으므로.
    after, codes = audit_codes(client, spectrum_id)
    assert after["circuit"] == "L1-R0-CPE1"
    assert "tail_mimicked_by_arc" not in codes
    assert client.get("/api/eis/spectra").json()[0]["last_circuit"] == "L1-R0-CPE1"
    # 풀린 것은 다시 대상이 되지 않는다.
    assert client.post("/api/eis/audit/refit").json()["targets"] == 0

    undone = client.post("/api/eis/audit/refit/undo").json()
    assert (undone["origin"], undone["removed"]) == (done["origin"], 1)
    assert undone["spectra"][0]["now_circuit"] == "R0-p(R1,CPE1)"
    (used,) = [fit for fit in fits_of(client, spectrum_id) if fit["in_use"]]
    assert used["id"] == old["id"]
    assert client.get("/api/eis/spectra").json()[0]["last_circuit"] == "R0-p(R1,CPE1)"
    assert client.post("/api/eis/audit/refit/undo").json()["origin"] == ""


def test_an_arc_that_is_really_there_is_kept_with_the_reason(client):
    """아크 없는 회로는 보이는 아크를 못 그린다.  이름을 고치려고 모양을 버리지
    않는다 — 그대로 두고 검수의 문장으로 까닭을 적는다."""
    spectrum_id, _ = pellet(client, "B14_arc.mpr", VISIBLE_ARC, VISIBLE_ARC[0])
    body = client.post("/api/eis/audit/refit").json()
    assert (body["targets"], body["changed"], body["kept"]) == (1, 0, 1)
    (one,) = body["spectra"]
    assert [p["code"] for p in one["problems"]] == ["arcs_are_electrode"]
    assert one["new_circuit"] == ""
    # 쓰던 값에서, 그다음 기본 시작점에서 — 둘 다 모양을 못 그린다.
    assert [t["start"] for t in one["tries"]] == ["seeded", "default"]
    assert all("모양을 못 그립니다" in t["reason"] for t in one["tries"])
    assert len(fits_of(client, spectrum_id)) == 1


def test_the_text_streams_a_line_per_spectrum_and_ends_with_the_way_back(client):
    pellet(client, "B15_pellet.mpr", BLOCKING, "R0-p(R1,CPE1)")
    pellet(client, "B14_arc.mpr", VISIBLE_ARC, VISIBLE_ARC[0])

    dry = client.post("/api/eis/audit/refit", params={"dry_run": True, "format": "text"})
    assert dry.headers["content-type"].startswith("text/plain")
    assert "맞춰 보기만 했습니다 — 아무것도 저장하지 않았습니다" in dry.text
    assert "bml refit --undo" not in dry.text

    text = client.post("/api/eis/audit/refit", params={"format": "text"}).text
    assert "맞춘 스펙트럼 2개 중 대상 2개" in text
    assert "[1/2] #1  B15_pellet  바꿈  R0-p(R1,CPE1) → L1-R0-CPE1 · 문제 1 → 0" in text
    assert "[2/2] #2  B14_arc  그대로  (L1-R0-CPE1 · 기본 시작점에서 — 맞춤이" in text
    assert "━━ 바꾼 것 (1)" in text and "━━ 그대로 둔 것 (1)" in text
    assert "풀린 문제: 꼬리를 흉내 낸 아크" in text
    assert "풀려던 문제: 전극 크기 아크를 벌크·입계로 부름" in text
    assert "대상 2 · 바꾼 것 1 · 그대로 1 · 건너뜀 0" in text
    assert "`bml refit --undo`" in text

    undo = client.post("/api/eis/audit/refit/undo", params={"format": "text"}).text
    assert "의 맞춤 1개를 지웠습니다" in undo
    assert "#1  B15_pellet — L1-R0-CPE1 → R0-p(R1,CPE1)" in undo
    assert "되돌릴 묶음이 없습니다" in client.post(
        "/api/eis/audit/refit/undo", params={"format": "text"}).text


def test_one_spectrum_that_breaks_does_not_stop_the_batch(client, monkeypatch):
    """스무 분짜리 묶음이 한 스펙트럼의 예외로 멈추면 나머지를 다시 기다려야 한다.
    멈춘 것은 이름과 까닭을 적고 넘어간다."""
    from app.routers import eis_refit

    first, _ = pellet(client, "B15_pellet.mpr", BLOCKING, "R0-p(R1,CPE1)")
    second, _ = pellet(client, "B15_again.mpr",
                       (BLOCKING[0], {**BLOCKING[1], "R0": 9.1}), "R0-p(R1,CPE1)")
    real = eis_refit._fit_row

    def broken(record, *args, **kwargs):
        if record.id == first:
            raise np.linalg.LinAlgError("SVD did not converge")
        return real(record, *args, **kwargs)

    monkeypatch.setattr(eis_refit, "_fit_row", broken)
    body = client.post("/api/eis/audit/refit").json()
    assert body["changed"] == 1
    assert [one["id"] for one in body["spectra"]] == [second]
    (skip,) = body["skipped"]
    assert skip["id"] == first
    assert skip["reason"] == "다시 맞추다 멈췄습니다 — LinAlgError: SVD did not converge"
