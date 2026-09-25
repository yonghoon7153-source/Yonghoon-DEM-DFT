"""`bml refit` — 검수가 권한 회로로 한꺼번에 다시 맞춘다 (ADR 0045).

두 합성 펠릿이 이 기능의 전부다.  꼬리를 아크로 흉내 낸 맞춤은 권한 회로로
바뀌고, 옛 맞춤은 남고, 되돌리면 돌아간다.  아크가 정말 보이는 펠릿은 대상이
아니다 — 그 아크는 커패시턴스대로 "전극 계면" 이라 불린다 (ADR 0047).  권한
회로가 모양을 못 그리는 길은 후보를 직접 넣어 본다.
"""

import numpy as np
import pytest
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


def offer_anyway(monkeypatch, circuit="L1-R0-CPE1"):
    """검수가 권할 것이 없는 스펙트럼에도 ``circuit`` 을 권하게 한다 — 권한 회로가
    모양을 못 그리거나 σ 의 저항을 옮기는 길을 보려고.  권할 것이 있으면 그대로."""
    from app.routers import eis_refit
    from wrdkit.eis.refit import Candidate

    original = eis_refit.refit_candidates
    monkeypatch.setattr(eis_refit, "refit_candidates", lambda findings, **kw: (
        original(findings, **kw) or [Candidate(circuit, ())]))


def test_an_arc_that_is_really_there_is_not_a_target(client):
    """실측 `bml refit` (2026-09-25): 전극 아크가 보이는 펠릿 여덟에 아크 없는
    `L1-R0-CPE1` 을 맞춰 모두 3.1–5.9 % 어긋나 그대로 두었다 — 돌릴 때마다.
    이제 그 아크는 "전극 계면 저항" 이고 (ADR 0047) 고칠 것이 없으니 대상이
    아니다."""
    spectrum_id, _ = pellet(client, "B14_arc.mpr", VISIBLE_ARC, VISIBLE_ARC[0])
    body = client.post("/api/eis/audit/refit").json()
    assert (body["targets"], body["changed"], body["kept"], body["unoffered"]) == (
        0, 0, 0, 0)
    one, _ = audit_codes(client, spectrum_id)
    assert [f for f in one["findings"] if f["severity"] == "problem"] == []
    (arc,) = one["arcs"]
    assert arc["label"] == "전극 계면 저항"
    assert len(fits_of(client, spectrum_id)) == 1


def test_a_circuit_that_cannot_draw_the_arc_is_kept_with_the_reason(client, monkeypatch):
    """아크 없는 회로는 보이는 아크를 못 그린다 — 그대로 두고 까닭을 적는다.
    쓰던 값에서, 그다음 기본 시작점에서 둘 다 해 본다."""
    spectrum_id, _ = pellet(client, "B14_arc.mpr", VISIBLE_ARC, VISIBLE_ARC[0])
    offer_anyway(monkeypatch)
    body = client.post("/api/eis/audit/refit").json()
    assert (body["targets"], body["changed"], body["kept"]) == (1, 0, 1)
    (one,) = body["spectra"]
    assert one["new_circuit"] == ""
    assert [t["start"] for t in one["tries"]] == ["seeded", "default"]
    assert all("모양을 못 그립니다" in t["reason"] for t in one["tries"])
    assert len(fits_of(client, spectrum_id)) == 1


def test_the_undo_shows_what_it_would_remove_before_removing_it(client):
    """첫 실측 `--dry-run` 뒤에 랩이 `--undo` 를 불렀다 — 저장한 묶음이 없었으니
    마지막 묶음은 전날의 펠릿 묶음이었다.  되돌리기는 무엇을 지울지 먼저 보여 준다
    (`GET`).  보여 주기는 같은 코드를 한 트랜잭션 안에서 돌리고 되돌린다."""
    spectrum_id, old = pellet(client, "B15_pellet.mpr", BLOCKING, "R0-p(R1,CPE1)")
    assert client.get("/api/eis/audit/refit/undo", params={"format": "text"}).text == (
        "되돌릴 묶음이 없습니다 — `bml refit` 이 저장한 맞춤이 없습니다.\n")
    done = client.post("/api/eis/audit/refit").json()

    seen = client.get("/api/eis/audit/refit/undo").json()
    assert seen["dry_run"] and (seen["origin"], seen["removed"]) == (done["origin"], 1)
    (one,) = seen["spectra"]
    assert (one["removed_circuit"], one["now_circuit"]) == ("L1-R0-CPE1", "R0-p(R1,CPE1)")
    # 아무것도 안 지웠다 — 새 맞춤이 그대로 쓰는 맞춤이다.
    fits = fits_of(client, spectrum_id)
    assert len(fits) == 2
    assert next(fit for fit in fits if fit["in_use"])["circuit"] == "L1-R0-CPE1"
    assert client.get("/api/eis/spectra").json()[0]["last_circuit"] == "L1-R0-CPE1"
    text = client.get("/api/eis/audit/refit/undo", params={"format": "text"}).text
    when = done["origin"][len("refit-"):]
    assert text.startswith(f"되돌리면 묶음 {done['origin']} ({when[:4]}-{when[4:6]}-"
                           f"{when[6:8]} {when[9:11]}:{when[11:13]} UTC) 의 맞춤 1개를 지웁니다")
    assert "아직 아무것도 지우지 않았습니다" in text
    assert "#1  B15_pellet — L1-R0-CPE1 → R0-p(R1,CPE1)" in text

    gone = client.post("/api/eis/audit/refit/undo").json()
    assert not gone["dry_run"] and gone["spectra"] == seen["spectra"]
    assert next(fit for fit in fits_of(client, spectrum_id) if fit["in_use"])["id"] == old["id"]


def test_the_text_streams_a_line_per_spectrum_and_ends_with_the_way_back(client,
                                                                         monkeypatch):
    pellet(client, "B15_pellet.mpr", BLOCKING, "R0-p(R1,CPE1)")
    pellet(client, "B14_arc.mpr", VISIBLE_ARC, VISIBLE_ARC[0])
    offer_anyway(monkeypatch)

    dry = client.post("/api/eis/audit/refit", params={"dry_run": True, "format": "text"})
    assert dry.headers["content-type"].startswith("text/plain")
    assert "맞춰 보기만 했습니다 — 아무것도 저장하지 않았습니다" in dry.text
    assert "bml refit --undo" not in dry.text

    text = client.post("/api/eis/audit/refit", params={"format": "text"}).text
    assert "맞춘 스펙트럼 2개 중 대상 2개" in text
    # σ 에 쓰는 저항도 옛것 → 새것으로 — 랩이 쓰는 것은 수다.  L 없이 맞춘 옛
    # 맞춤이라 배선 판정도 있었다 (보완 8) — 그림이 어떻게 됐는지도 적는다.
    assert ("[1/2] #1  B15_pellet  바꿈  R0-p(R1,CPE1) → L1-R0-CPE1 · 문제 1 → 0 · "
            "오차 평균 3.2 % → < 0.01 % · σ 저항 8.4") in text
    assert "    풀린 확인: 배선 인덕턴스 없음\n" in text
    assert "[2/2] #2  B14_arc  그대로  (L1-R0-CPE1 · 기본 시작점에서 — 맞춤이" in text
    assert "━━ 바꾼 것 (1)" in text and "━━ 그대로 둔 것 (1)" in text
    assert "풀린 문제: 꼬리를 흉내 낸 아크" in text
    assert "대상 2 · 바꾼 것 1 · 그대로 1 · 건너뜀 0" in text
    assert "`bml refit --undo`" in text

    undo = client.post("/api/eis/audit/refit/undo", params={"format": "text"}).text
    assert "의 맞춤 1개를 지웠습니다" in undo
    assert "#1  B15_pellet — L1-R0-CPE1 → R0-p(R1,CPE1)" in undo
    assert "되돌릴 묶음이 없습니다" in client.post(
        "/api/eis/audit/refit/undo", params={"format": "text"}).text


#: 막지 않는 풀셀 — 아크 둘.  0.1 Hz 아래에서 셀이 decade 당 20 % 변한다: 쉬지 않은
#: 채 잰 셀 (실측 풀셀 열 개 — 200 사이클 뒤 SOC 100, ADR 0045 보완 4).
FULL = ("L1-R0-p(R1,CPE1)-p(R2,CPE2)",
        {"L1": 5e-7, "R0": 10.0, "R1": 120.0, "CPE1_Q": 1e-5, "CPE1_n": 0.8,
         "R2": 300.0, "CPE2_Q": 5e-3, "CPE2_n": 0.7})
FULL_SWEEP = S.log_sweep(1e6, 0.01, 10)


def drifting_full_cell(client, name="Dcell_drift_C01.mpr"):
    """올리고 모든 점으로 맞춘다 — 드리프트한 저주파 끝까지."""
    model = parse_circuit(FULL[0])
    z = model.impedance([FULL[1][name_] for name_ in model.parameter_names], FULL_SWEEP)
    z = z * (1 + np.clip(np.log10(0.1 / FULL_SWEEP), 0, None) * 0.20)
    created = client.post("/api/eis/spectra/upload",
                          params={"kind": "solid", "cell_config": "full"},
                          files={"file": (name, S.build_mpr(S.spectrum_columns(FULL_SWEEP, z)),
                                          "application/octet-stream")})
    assert created.status_code == 201, created.text
    spectrum_id = created.json()["id"]
    fit = client.post(f"/api/eis/spectra/{spectrum_id}/fit",
                      params={"circuit": FULL[0]}).json()
    assert fit["converged"], fit["reason"]
    return spectrum_id, fit


def test_a_drifting_low_end_is_fitted_again_from_the_bound_the_audit_asks(client):
    """보완 4: KK 가 저주파 끝을 짚고 하한을 권했다.  같은 회로를 그 하한부터 다시
    맞추면 드리프트가 끌어올린 R2 (참값 300 Ω) 가 돌아온다.  그 뒤 검수는 참고로
    내려가 다시 대상이 되지 않고, 되돌리면 옛 창으로 돌아간다."""
    spectrum_id, old = drifting_full_cell(client)
    before, _ = audit_codes(client, spectrum_id)
    (kk,) = [f for f in before["findings"] if f["code"] == "kk_violation"]
    assert kk["severity"] == "check" and kk["scope"] == "points"
    bound = kk["low_hz"]
    assert 0.5 < bound < 1.0
    assert f"하한을 {bound:.3g} Hz 로 두고 다시 맞추세요" in kk["message"]

    dry = client.post("/api/eis/audit/refit", params={"dry_run": True}).json()
    assert (dry["targets"], dry["windows"], dry["changed"]) == (1, 1, 1)
    assert dry["spectra"][0]["new_fit_id"] is None
    assert len(fits_of(client, spectrum_id)) == 1

    done = client.post("/api/eis/audit/refit").json()
    (one,) = done["spectra"]
    assert one["old_fit_id"] == old["id"] and one["problems"] == []
    assert one["new_circuit"] == one["old_circuit"] == FULL[0]
    assert one["low_hz"] == pytest.approx(bound)
    assert one["new_low_hz"] == pytest.approx(bound)
    assert one["old_low_hz"] == pytest.approx(0.01)
    sweep = FULL_SWEEP
    gone = sweep[sweep < bound]
    assert one["dropped_points"] == gone.size
    assert one["dropped_band_hz"] == pytest.approx([gone.min(), gone.max()])
    assert all(t["low_hz"] == pytest.approx(bound) for t in one["tries"])
    r2 = next(v for v in one["values"] if v["name"] == "R2")
    assert r2["old"] > 320                           # 드리프트가 끌어올린 값
    assert r2["new"] == pytest.approx(300, rel=0.01) and r2["determined"]

    (used,) = [fit for fit in fits_of(client, spectrum_id) if fit["in_use"]]
    assert used["id"] == one["new_fit_id"] and used["origin"] == done["origin"]
    assert used["frequency_low_hz"] == pytest.approx(bound)
    after, _ = audit_codes(client, spectrum_id)
    (note,) = [f for f in after["findings"] if f["code"] == "kk_violation"]
    assert note["severity"] == "note" and note["low_hz"] is None
    assert f"쓰는 맞춤은 {bound:.3g} Hz 부터 맞춰 그 점들을 쓰지 않았습니다" in note["message"]
    # 할 일이 끝났다 — 다음 묶음의 대상이 아니다.
    assert client.post("/api/eis/audit/refit").json()["targets"] == 0

    undone = client.post("/api/eis/audit/refit/undo").json()
    (back,) = undone["spectra"]
    assert back["removed_circuit"] == back["now_circuit"] == FULL[0]
    assert back["removed_low_hz"] == pytest.approx(bound)
    assert back["now_low_hz"] == pytest.approx(0.01)
    again, _ = audit_codes(client, spectrum_id)
    assert [f["severity"] for f in again["findings"] if f["code"] == "kk_violation"] == [
        "check"]


def test_the_text_says_which_points_went_and_what_the_values_did(client):
    drifting_full_cell(client)
    text = client.post("/api/eis/audit/refit", params={"format": "text"}).text
    assert "맞춘 스펙트럼 1개 중 대상 1개 — 회로를 권한 문제 판정이 있거나, 저주파 끝이" in text
    assert "하한이 권해진 1개는 그 하한부터 맞춥니다" in text
    assert "[1/1] #1  Dcell_drift_C01  바꿈  하한 0.01 → 0.794 Hz · 회로 그대로 · 오차 평균 " in text
    assert "    하한 0.01 → 0.794 Hz · 회로 그대로 L1-R0-p(R1,CPE1)-p(R2,CPE2) (쓰던 값에서)" in text
    assert "    뺀 점: 0.01–0.631 Hz 의 점 19개 — 저주파 끝이 KK 를 어긴 곳" in text
    assert "풀린 문제:" not in text
    (values,) = [line for line in text.splitlines() if line.startswith("    값: ")]
    # 1 % 넘게 움직인 것만 — 드리프트가 끌어올린 R2 가 참값으로 돌아왔다.
    assert "R2 358 → 300 (-16 %)" in values and "R1 " not in values
    assert values.endswith("개는 1 % 안")
    undo = client.post("/api/eis/audit/refit/undo", params={"format": "text"}).text
    assert ("    #1  Dcell_drift_C01 — 하한 0.794 → 0.01 Hz "
            "(L1-R0-p(R1,CPE1)-p(R2,CPE2))") in undo


def test_a_value_the_window_leaves_undetermined_is_named_without_a_guessed_cause():
    """첫 실측 맞춰 보기 (2026-09-24 14:41 UTC): #33 의 R0 가 "뺀 점들이 정하던
    값입니다" 로 적혔다.  고주파 절편은 저주파 점이 정하던 값이 아니다 — 아크와 TL 이
    역할을 바꿔 미결정이 됐다.  까닭은 짐작하지 않고 사실만 적는다."""
    from app.routers.eis_refit import _value_lines
    from app.schemas import RefitSpectrumOut, RefitValueOut

    one = RefitSpectrumOut(
        id=33, name="260903_Poly(L&F)_60um_full_#01_C01", old_fit_id=1,
        old_circuit=FULL[0], new_circuit=FULL[0],
        values=[RefitValueOut(name="R0", old=3.02, new=2.9, determined=False),
                RefitValueOut(name="R1", old=5.94, new=0.841),
                RefitValueOut(name="CPE1_Q", old=0.0101, new=0.0101)])
    assert _value_lines(one) == [
        "    값: R1 5.94 → 0.841 (-86 %) · 나머지 1개는 1 % 안",
        "    새로 미결정: R0 — 하한 위의 점만으로는 정해지지 않습니다"]
    # 맞춤이 저장한 사유는 옮긴다 — 쓰던 값과 데이터의 두 골짜기 (보완 5).
    one.values[0].reason = "seed_spread"
    assert _value_lines(one)[1] == (
        "    새로 미결정: R0 (같은 χ² 에 시작점마다 다른 값) — 하한 위의 점만으로는 "
        "정해지지 않습니다")


def test_a_value_that_was_not_measured_before_is_not_said_to_have_moved():
    """두 번째 실측 맞춰 보기: #13 의 R0 가 "0.000372 → 19 (+5101431 %)" 로 찍혔다.
    옛 R0 는 0 에 붙은 미결정 값이었다 — 측정이 아닌 수에서 몇 % 움직였다고 하지
    않고, 새로 정해진 값으로 따로 적는다."""
    from app.routers.eis_refit import _value_lines
    from app.schemas import RefitSpectrumOut, RefitValueOut

    one = RefitSpectrumOut(
        id=13, name="Dcell11_4_2V_after400_rest_1h_0_C01", old_fit_id=1,
        old_circuit=FULL[0], new_circuit=FULL[0],
        values=[RefitValueOut(name="R0", old=0.000372, new=19.0, was_determined=False),
                RefitValueOut(name="R1", old=258.0, new=262.0),
                RefitValueOut(name="TL1_Q", old=1.73e-05, new=3.0e-05, determined=False,
                              reason="relative_stderr")])
    assert _value_lines(one) == [
        "    값: R1 258 → 262 (+2 %)",
        "    새로 정해짐: R0 19 — 옛 맞춤에서는 미결정이었습니다",
        "    새로 미결정: TL1_Q (오차 막대가 값의 절반 넘음) — 하한 위의 점만으로는 "
        "정해지지 않습니다"]


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


def test_open_screens_hear_about_the_saved_fits_when_the_batch_ends(client):
    """흘려 보내는 창구는 요청 머리에서 한 번 알린다 — 그때는 저장한 것이 없다.
    끝에 한 번 더 알려야 열린 화면이 새 맞춤을 다시 읽는다.  맞춰 보기만 했으면
    알릴 것이 없다."""
    pellet(client, "B15_pellet.mpr", BLOCKING, "R0-p(R1,CPE1)")

    def revision():
        return client.get("/api/revision").json()["revision"]

    before = revision()
    client.post("/api/eis/audit/refit", params={"dry_run": True, "format": "text"})
    assert revision() == before + 1
    before = revision()
    client.post("/api/eis/audit/refit", params={"format": "text"})
    assert revision() == before + 2


def test_the_announcement_is_made_on_the_event_loop_not_the_worker_thread():
    """묶음은 일꾼 스레드에서 돈다.  거기서 `revision.bump` 를 바로 부르면 asyncio 의
    Event 를 남의 스레드에서 켜게 된다 — 디버그 모드에서 예외가 나고, 기다리던
    화면은 제 시간 제한도 못 지키고 멈췄다.  시나리오를 따로 스레드에서 돌려,
    되돌아가면 시험이 멈추는 대신 실패하게 한다."""
    import threading

    import anyio

    from app.live import revision
    from app.routers.eis_refit import _announce

    async def scenario():
        revision.bump()                  # 앞의 시험의 루프에 묶이지 않은 새 Event
        seen = revision.value
        woke: list[int] = []

        async def screen():
            woke.append(await revision.wait_past(seen, timeout=2))

        async with anyio.create_task_group() as group:
            group.start_soon(screen)
            await anyio.sleep(0.05)
            await anyio.to_thread.run_sync(_announce)
        return seen, woke

    result: dict = {}
    runner = threading.Thread(daemon=True, target=lambda: result.update(
        out=anyio.run(scenario, backend_options={"debug": True})))
    runner.start()
    runner.join(10)
    assert not runner.is_alive(), "기다리던 화면이 안 깼다 — 루프 밖에서 알렸다"
    seen, woke = result["out"]
    assert woke == [seen + 1]


def test_a_problem_with_no_circuit_to_offer_is_counted_not_touched(client, monkeypatch):
    """검수의 "문제" 수와 여기의 "대상" 수가 왜 다른지 글 머리가 말한다."""
    from app.routers import eis_refit

    spectrum_id, _ = pellet(client, "B15_pellet.mpr", BLOCKING, "R0-p(R1,CPE1)")
    monkeypatch.setattr(eis_refit, "refit_candidates", lambda findings, **_: [])
    body = client.post("/api/eis/audit/refit").json()
    assert (body["targets"], body["unoffered"]) == (0, 1)
    text = client.post("/api/eis/audit/refit", params={"format": "text"}).text
    assert "권할 회로가 없는 1개는 건드리지 않습니다" in text
    assert len(fits_of(client, spectrum_id)) == 1


def test_the_progress_line_counts_every_problem_not_only_the_one_that_offered_a_circuit():
    """첫 실측 맞춰 보기는 "문제 1 → 2" 라고 적었다: 회로를 실은 판정 하나만 세고,
    원래 있던 판정 둘은 새로 생긴 것처럼 셌다.  사실은 3 → 2 다."""
    from app.routers.eis_refit import _Progress, _progress_line
    from app.schemas import AuditFindingOut, RefitSpectrumOut

    def problem(code):
        return AuditFindingOut(severity="problem", label="문제", code=code, message=code)

    offered, other = problem("blocking_element_on_open_cell"), problem("other")
    one = RefitSpectrumOut(id=31, name="sym", old_fit_id=1, old_circuit="A",
                           new_circuit="B", problems=[offered],
                           old_problems=[offered, other, other],
                           new_problems=[other, other])
    assert _progress_line(_Progress(1, 1, spectrum=one)) == (
        "[1/1] #31  sym  바꿈  A → B · 문제 3 → 2")


def test_an_open_cell_counts_every_problem_not_only_the_one_that_offered_a_circuit(client):
    """실측 #31 의 쌍둥이 — 막지 않는 대칭셀에 쓸데없는 막는 CPE3.  두 아크의
    이름은 이제 커패시턴스를 따르니 (ADR 0047) 문제는 그 CPE3 하나다."""
    frequency = S.log_sweep(1e6, 1e-2, 12)
    created = client.post("/api/eis/spectra/upload",
                          params={"kind": "solid", "cell_config": "sym"},
                          files={"file": ("260831_sym_#01.mpr",
                                          S.build_mpr(S.spectrum_columns(
                                              frequency, S.randles(frequency))),
                                          "application/octet-stream")}).json()
    client.patch(f"/api/eis/spectra/{created['id']}",
                 json={"thickness_um": 60, "area_cm2": 0.785})
    client.post(f"/api/eis/spectra/{created['id']}/fit",
                params={"circuit": "R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"})

    text = client.post("/api/eis/audit/refit", params={"dry_run": True, "format": "text"}).text
    assert ("바꿈  R0-p(R1,CPE1)-p(R2,CPE2)-CPE3 → R0-p(R1,CPE1)-p(R2,CPE2) · 문제 1 → 0"
            in text)
    assert "    풀린 문제: 안 막는 셀에 막는 소자\n" in text
    assert "남은 문제" not in text
    # 막지 않는 셀은 σ 를 안 낸다 — 적을 저항이 없다.
    assert "σ 저항" not in text


def test_a_refit_that_draws_worse_does_not_move_the_resistance_behind_sigma(client,
                                                                          monkeypatch):
    """전극 크기 아크(2 Ω)가 구간 안에 보이는 펠릿.  아크 없는 회로는 그것을 R0 로
    삼키고도 평균 2.5 % 로 맞아 검수는 받아들인다 — σ 에 쓰는 저항은 8 → 9.65 Ω
    (+21 %) 로 간다.  수가 틀려지는 경우라 받지 않는다.  (ADR 0047 뒤로 검수는
    이 펠릿에 아크 없는 회로를 권하지 않는다 — 후보를 직접 넣는다.)"""
    truth = ("L1-R0-p(R1,CPE1)-CPE2", {"L1": 1.7e-6, "R0": 8.0, "R1": 2.0, "CPE1_Q": 1e-5,
                                        "CPE1_n": 0.85, "CPE2_Q": 1e-4, "CPE2_n": 0.9})
    spectrum_id, _ = pellet(client, "B14_small_arc.mpr", truth, truth[0])
    offer_anyway(monkeypatch)
    body = client.post("/api/eis/audit/refit").json()
    assert (body["targets"], body["changed"], body["kept"]) == (1, 0, 1)
    (one,) = body["spectra"]
    assert one["old_sigma_ohm"] == pytest.approx(8.0, rel=1e-3)
    assert [t["start"] for t in one["tries"]] == ["seeded", "default"]
    for attempt in one["tries"]:
        assert not attempt["accepted"]
        assert attempt["sigma_ohm"] == pytest.approx(9.65, rel=1e-2)
        assert attempt["reason"].startswith("σ 에 쓰는 저항이 8 → 9.651 Ω (+21 %) 로 옮겨 가는데")
        assert "(오차 평균 < 0.01 → 2.5 %)" in attempt["reason"]
    assert len(fits_of(client, spectrum_id)) == 1


def test_only_the_problems_that_went_away_are_called_solved():
    """실측 B17_ACTI E C01 #2 #3: 꼬리 흉내만 풀고 전극 크기 아크는 남은 맞춤이
    받아들여졌는데, 글은 둘 다 "풀린 문제" 에 적고 하나를 다시 "남은 문제" 에 적었다."""
    from datetime import datetime, timezone

    from app.routers.eis_refit import render_refit_summary
    from app.schemas import AuditFindingOut, EisRefitOut, RefitSpectrumOut

    def finding(code, circuits=()):
        return AuditFindingOut(severity="problem", label="문제", code=code,
                               message=f"{code} 의 문장", circuits=list(circuits))

    tail = finding("tail_mimicked_by_arc", ["L1-R0-p(R1,CPE1)-p(R2,CPE2)-CPE3"])
    electrode = finding("arcs_are_electrode", ["L1-R0-CPE1"])
    one = RefitSpectrumOut(
        id=145, name="B17_ACTI E_C01 #2", old_fit_id=1,
        old_circuit="R0-p(R1,CPE1)-p(R2,CPE2)", problems=[tail, electrode],
        old_problems=[tail, electrode],
        new_circuit="L1-R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
        new_problems=[finding("arcs_are_electrode")])
    text = render_refit_summary(EisRefitOut(
        origin="refit-20260923T163007", dry_run=True,
        generated_at=datetime.now(timezone.utc), total=1, targets=1, changed=1,
        spectra=[one]))
    assert "    풀린 문제: 꼬리를 흉내 낸 아크\n" in text
    assert "    남은 문제: 전극 크기 아크를 벌크·입계로 부름 — arcs_are_electrode 의 문장" in text


def test_the_same_model_named_right_is_not_refused_for_a_shape_the_old_fit_missed_too(client):
    """실측 B15 #9 · B16 #9 의 쌍둥이 — 꼬리가 CPE 하나로 안 그려지는 막는 펠릿.
    `R0-p(R1,CPE1)` 로 맞추면 R1 이 10⁹ Ω 로 가 곧 `R0-CPE1` 이고 모양을 못
    그린다 (3.7 %).  새 `L1-R0-CPE1` 도 못 그리지만 (3.4 %) 같은 모양을 이름만 바로
    그린 것이다.  첫 적용은 이것을 모양 탓으로 막아, 꼬리 흉내가 그대로 남았다."""
    truth = ("L1-R0-CPE1-CPE2", {"L1": 1.7e-6, "R0": 120.0, "CPE1_Q": 6e-7, "CPE1_n": 0.92,
                                   "CPE2_Q": 1e-6, "CPE2_n": 0.65})
    spectrum_id, old = pellet(client, "B15_cold.mpr", truth, "R0-p(R1,CPE1)")
    assert old["parameters"][1]["value"] > 1e8                 # R1 이 벽에 붙었다
    before, codes = audit_codes(client, spectrum_id)
    assert {"tail_mimicked_by_arc", "misfit_everywhere"} <= set(codes)

    (one,) = client.post("/api/eis/audit/refit").json()["spectra"]
    assert one["new_circuit"] == "L1-R0-CPE1"
    assert one["old_misfit_mean"] > 0.03 and one["new_misfit_mean"] > 0.03
    assert one["new_misfit_mean"] <= one["old_misfit_mean"]
    after, codes = audit_codes(client, spectrum_id)
    assert "tail_mimicked_by_arc" not in codes
    assert "misfit_everywhere" in codes                          # 그대로 적는다


def test_a_fit_without_the_cable_is_refitted_with_l1_in_front(client):
    """보완 8: 배선 L 이 빠졌다는 판정은 확인인데도 `bml refit` 이 맞춘다 — 실측
    08:07 검수의 스물셋 (mid_Ni #38–#48, B18 #133–#138, 대칭셀 일곱)."""
    spectrum_id, old = pellet(client, "B18_pellet.mpr", BLOCKING, "R0-CPE1")
    before, codes = audit_codes(client, spectrum_id)
    cable = next(f for f in before["findings"] if f["code"] == "inductance_missing")
    assert cable["severity"] == "check" and cable["circuits"] == ["L1-R0-CPE1"]

    done = client.post("/api/eis/audit/refit").json()
    assert (done["targets"], done["wiring"], done["changed"]) == (1, 1, 1)
    (one,) = done["spectra"]
    assert one["new_circuit"] == "L1-R0-CPE1"
    assert [p["code"] for p in one["checks"]] == ["inductance_missing"]
    assert one["new_checks"] == []
    assert one["new_misfit_mean"] < one["old_misfit_mean"]
    after, codes = audit_codes(client, spectrum_id)
    assert after["circuit"] == "L1-R0-CPE1" and "inductance_missing" not in codes
    assert client.post("/api/eis/audit/refit").json()["targets"] == 0


def test_the_text_says_what_the_cable_refit_did(client):
    """문제 판정이 없으니 "문제 0 → 0" 은 읽을 거리가 아니다 — 그림이 어떻게 됐는지
    적는다.  풀린 것은 확인이라 "풀린 확인" 이다."""
    pellet(client, "B18_pellet.mpr", BLOCKING, "R0-CPE1")
    text = client.post("/api/eis/audit/refit", params={"format": "text"}).text
    assert "배선 L 이 빠진 1개는 쓰던 회로 앞에 `L1-` 를 붙여 맞춥니다" in text
    assert "바꿈  R0-CPE1 → L1-R0-CPE1 · 오차 평균 " in text
    assert "문제 0 → 0" not in text
    assert "    풀린 확인: 배선 인덕턴스 없음\n" in text
    assert "풀린 문제:" not in text


#: 식은 황화물 펠릿 — 전해질 아크가 잰 주파수 안으로 내려왔다 (실측 B15 #9 의 쌍둥이,
#: 꼭지 300 kHz).  전해질 저항은 90 + 46 = 136 Ω 이다.
COLD = ("L1-R0-p(R1,CPE1)-CPE2",
        {"L1": 2e-6, "R0": 90.0, "R1": 46.0,
         "CPE1_Q": (1 / (2 * np.pi * 3e5)) ** 0.9 / 46.0, "CPE1_n": 0.9,
         "CPE2_Q": 6.3e-7, "CPE2_n": 0.87})


def test_a_cold_pellet_is_refitted_with_the_arc_the_audit_offers(client):
    """보완 10: 아크 없는 `L1-R0-CPE1` 은 L1 을 0 으로 보내고 R0 를 교점 위에 둔다
    (`arc_above_window`, 확인).  `bml refit` 이 아크 하나를 더한 회로로 맞추고, σ 는
    R0 + R1 — 참값 136 Ω 이다.  실측 10:24 검수의 일곱 (#77 #95 #103 #113 #114 #122
    #123)."""
    spectrum_id, _ = pellet(client, "B15_cold.mpr", COLD, "L1-R0-CPE1")
    before, _ = audit_codes(client, spectrum_id)
    arc = next(f for f in before["findings"] if f["code"] == "arc_above_window")
    assert arc["severity"] == "check" and arc["circuits"] == ["L1-R0-p(R1,CPE1)-CPE2"]

    done = client.post("/api/eis/audit/refit").json()
    assert (done["targets"], done["arcs"], done["wiring"], done["changed"]) == (1, 1, 0, 1)
    (one,) = done["spectra"]
    assert one["new_circuit"] == "L1-R0-p(R1,CPE1)-CPE2"
    assert [p["code"] for p in one["checks"]] == ["arc_above_window"]
    assert one["new_checks"] == []
    chosen = next(t for t in one["tries"] if t["accepted"])
    assert chosen["start"] == "arc"
    assert one["new_sigma_ohm"] == pytest.approx(136.0, rel=0.002)
    assert one["old_sigma_ohm"] < one["new_sigma_ohm"]
    assert one["new_misfit_mean"] < one["old_misfit_mean"]
    after, codes = audit_codes(client, spectrum_id)
    assert after["circuit"] == "L1-R0-p(R1,CPE1)-CPE2" and "arc_above_window" not in codes
    assert client.post("/api/eis/audit/refit").json()["targets"] == 0


def test_the_text_says_what_the_arc_refit_did(client):
    """σ 가 바뀌는 다시 맞추기다 — 머리에 그렇게 적고, 줄마다 σ 저항이 어떻게 됐는지
    적는다.  더한 아크는 "교점에서" 시작했다."""
    pellet(client, "B15_cold.mpr", COLD, "L1-R0-CPE1")
    text = client.post("/api/eis/audit/refit", params={"format": "text"}).text
    assert ("구간 위 아크가 걸친 1개는 아크 하나를 더한 회로로 맞춥니다 — σ 저항이 R0 에서 "
            "R0 + R1 로 바뀝니다") in text
    assert "바꿈  L1-R0-CPE1 → L1-R0-p(R1,CPE1)-CPE2 · 오차 평균 " in text
    assert "문제 0 → 0" not in text
    assert " (교점에서) · χ² " in text
    assert "    풀린 확인: 구간 위 아크\n" in text
    assert "· σ 저항 " in text


def test_an_arc_refit_whose_sigma_falls_short_of_the_crossing_is_kept(client, monkeypatch):
    """σ 저항이 교점에 못 미치거나 σ 를 못 내면 받지 않는다 — 판정의 까닭(그 아크가
    전해질)을 새 맞춤에서 확인하지 못했다."""
    from app.routers import eis_refit

    spectrum_id, _ = pellet(client, "B15_cold.mpr", COLD, "L1-R0-CPE1")
    monkeypatch.setattr(eis_refit, "electrolyte_short",
                        lambda crossing, sigma, missing=(): "σ 저항이 교점보다 작습니다")
    body = client.post("/api/eis/audit/refit").json()
    assert (body["targets"], body["changed"], body["kept"]) == (1, 0, 1)
    (one,) = body["spectra"]
    assert one["new_circuit"] == ""
    arc = next(t for t in one["tries"] if t["start"] == "arc")
    assert arc["converged"] and not arc["accepted"]
    assert arc["reason"] == "σ 저항이 교점보다 작습니다"
    assert arc["sigma_ohm"] == pytest.approx(136.0, rel=0.002)
    assert len(fits_of(client, spectrum_id)) == 1
