

def test_the_circuit_s_exact_degeneracy_is_applied_to_old_rows_too(client):
    """맞바꿔도 같은 곡선이라는 것은 **식의 성질**이라 소급할 수 있다.

    `alias_of` 는 새로 맞출 때만 붙는다.  그래서 이 수정 전에 맞춘 TL 행은
    화면에서 계속 "이온 레일 / 전자 레일 측정값" 으로 남았고, 같은 셀을 다시
    맞춘 것만 미결정이 됐다 — 같은 사실이 DB 안에서 작성 시점에 따라 달라졌다
    (Codex 판정 리뷰 #3).  통계 문턱과 달리 이것은 데이터가 필요 없다.
    """
    import json

    from sqlmodel import Session

    from app.db import engine
    from app.models import SpectrumFit, SpectrumRecord

    with Session(engine) as session:
        record = SpectrumRecord(sha256="a" * 64, original_name="old.mpr",
                                name="옛 셀", kind="solid", n_points=40)
        session.add(record)
        session.commit()
        session.refresh(record)
        spectrum_id = record.id
    # 옛 모양: 진단 없이 `determined` 불리언만.
    with Session(engine) as session:
        session.add(SpectrumFit(
            spectrum_id=spectrum_id, circuit="R0-TL1", kind="solid", converged=True,
            chi_squared=1e-4, reason="",
            parameters_json=json.dumps([
                {"name": "R0", "value": 5.0, "unit": "Ω", "stderr": 0.1,
                 "determined": True, "relative_error": 0.02},
                {"name": "TL1_Ri", "value": 40.0, "unit": "Ω", "stderr": 1e-12,
                 "determined": True, "relative_error": 0.0},
                {"name": "TL1_Re", "value": 12.0, "unit": "Ω", "stderr": 1e-12,
                 "determined": True, "relative_error": 0.0},
            ]),
        ))
        session.commit()

    got = client.get(f"/api/eis/fits?ids={spectrum_id}").json()
    assert got, got
    rails = {p["name"]: p for p in got[0]["parameters"]
             if p["name"].startswith("TL1_")}
    assert set(rails) == {"TL1_Ri", "TL1_Re"}
    for name, parameter in rails.items():
        assert parameter["determined"] is False, name
        # 축퇴는 식의 성질이라 옛 행에도 **이름 붙은 사유**로 소급된다.
        assert parameter["reason"] == "structural_alias", name

    # 축퇴와 무관한 파라미터도 측정값은 아니다: 이 행에는 진단이 없어서
    # 저 `determined: true` 가 흩어짐을 통과한 것인지 검사를 아예 못 한
    # 것인지 알 수가 없다 (Codex 판정 리뷰 #6).  값은 보이되 총저항·전도도로는
    # 안 간다.  다시 맞추면 (`POST /api/eis/refit`) 사라지는 표시다.
    r0 = next(p for p in got[0]["parameters"] if p["name"] == "R0")
    assert r0["determined"] is False
    assert r0["reason"] == "legacy_no_diagnostics"
    assert r0["value"] == 5.0          # 값 자체는 그대로 보인다


def test_an_old_exponent_is_judged_again_by_how_far_apart_its_answers_can_be(client):
    """ADR 0045 보완 9: 지수는 흩어짐을 비가 아니라 차이로 본다.  v1 행은 비(r)와
    값(v)만 남겼지만, 값이 두 끝 사이에 있으니 차이는 v(r−1)/r … v(r−1) 이다.
    행은 그대로 두고 읽을 때 씌운다 — `bml reparse` 는 옛 맞춤을 지워 되돌리기
    길을 없앤다."""
    import json

    from sqlmodel import Session

    from app.db import engine
    from app.models import SpectrumFit, SpectrumRecord

    def row(name, value, spread, unit="", policy="eis-ident-v1", **extra):
        return {"name": name, "value": value, "unit": unit, "stderr": abs(value) * 0.01,
                "determined": True, "relative_error": 0.01, "status": "determined",
                "reason": "", "spread": spread, "alias_of": "", "policy": policy, **extra}

    with Session(engine) as session:
        record = SpectrumRecord(sha256="c" * 64, original_name="v1.mpr",
                                name="v1 셀", kind="solid", n_points=40)
        session.add(record)
        session.commit()
        session.refresh(record)
        spectrum_id = record.id
    with Session(engine) as session:
        session.add(SpectrumFit(
            spectrum_id=spectrum_id, circuit="R0-p(R1,CPE1)-p(R2,CPE2)-CPE3",
            kind="solid", converged=True, chi_squared=1e-4, reason="",
            parameters_json=json.dumps([
                row("R0", 5.0, 1.1, "Ω"),
                row("R1", 20.0, 2.9, "Ω"),                 # 저항은 전처럼 비로
                row("CPE1_Q", 1e-6, 1.1, "S·sⁿ"),
                row("CPE1_n", 0.33, 2.94),                 # #33: 0.33 과 0.97
                row("R2", 50.0, 1.1, "Ω"),
                row("CPE2_Q", 1e-5, 1.1, "S·sⁿ"),
                row("CPE2_n", 0.9, 1.2),                   # 차이 ≤ 0.18
                row("CPE3_Q", 1e-4, 1.1, "S·sⁿ"),
                row("CPE3_n", 0.9, 1.25),                  # 0.18–0.225 — 모른다
            ]),
        ))
        session.commit()

    got = client.get(f"/api/eis/fits?ids={spectrum_id}").json()
    by_name = {p["name"]: p for p in got[0]["parameters"]}
    assert by_name["CPE1_n"]["determined"] is False
    assert by_name["CPE1_n"]["reason"] == "seed_spread"
    assert by_name["CPE2_n"]["determined"] is True
    assert by_name["CPE3_n"]["determined"] is False
    assert by_name["R1"]["determined"] is True
    assert by_name["CPE1_n"]["value"] == 0.33          # 값은 그대로 보인다


def test_refit_all_replaces_legacy_rows_and_clears_the_demotion(client):
    """강등만 하고 끝내면 올려 둔 셀의 전도도·추세가 통째로 빈다.

    `POST /api/eis/refit` 이 되돌리는 길이다: 저장된 맞춤을 그 회로·그 창으로
    다시 하고, 새 규칙의 진단과 함께 갈아 끼운다.  다시 맞춘 뒤에는
    `legacy_no_diagnostics` 가 사라져야 한다 (Codex 판정 리뷰 #6).
    """
    import json

    import numpy as np
    from sqlmodel import Session, select

    from app import storage
    from app.db import engine
    from app.models import SpectrumFit, SpectrumRecord

    frequency = np.logspace(5, -1, 40)
    omega = 2 * np.pi * frequency
    z = 5.0 + 1 / (1 / 20.0 + 1e-5 * (1j * omega) ** 0.9)

    with Session(engine) as session:
        record = SpectrumRecord(sha256="b" * 64, original_name="legacy.mpr",
                                name="옛 셀", kind="liquid", n_points=len(frequency))
        session.add(record)
        session.commit()
        session.refresh(record)
        spectrum_id = record.id
    from wrdkit.eis import Spectrum
    storage.cache_spectrum(spectrum_id, Spectrum(frequency, z.real, z.imag),
                           "b" * 64)
    with Session(engine) as session:
        session.add(SpectrumFit(
            spectrum_id=spectrum_id, circuit="R0-p(R1,CPE1)", kind="liquid",
            converged=True, chi_squared=1e-3, reason="",
            frequency_low_hz=float(frequency.min()),
            frequency_high_hz=float(frequency.max()),
            parameters_json=json.dumps([
                {"name": "R0", "value": 5.0, "unit": "Ω", "stderr": 0.1,
                 "determined": True, "relative_error": 0.02},
            ]),
        ))
        session.commit()

    # 강등되어 있다.
    before = client.get(f"/api/eis/fits?ids={spectrum_id}").json()
    assert before[0]["parameters"][0]["reason"] == "legacy_no_diagnostics"
    assert before[0]["parameters"][0]["determined"] is False

    out = client.post("/api/eis/refit").json()
    assert out["refitted"] == 1, out
    assert out["failed"] == []

    after = client.get(f"/api/eis/fits?ids={spectrum_id}").json()
    names = {p["name"] for p in after[0]["parameters"]}
    assert {"R0", "R1", "CPE1_Q", "CPE1_n"} <= names
    for parameter in after[0]["parameters"]:
        assert parameter["reason"] != "legacy_no_diagnostics", parameter
        assert parameter.get("status"), parameter      # 진단이 실려 있다
    # 옛 행은 갈아 끼웠다 — 하나만 남는다.
    with Session(engine) as session:
        rows = session.exec(select(SpectrumFit).where(
            SpectrumFit.spectrum_id == spectrum_id)).all()
    assert len(rows) == 1
