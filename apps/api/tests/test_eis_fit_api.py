

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
    # 축퇴와 무관한 파라미터는 저장된 그대로다 — 표시가 회로 전체로 번지면 안 된다.
    r0 = next(p for p in got[0]["parameters"] if p["name"] == "R0")
    assert r0["determined"] is True
