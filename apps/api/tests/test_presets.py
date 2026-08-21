"""저장된 프리셋 — 조성과 셀 설정을 한 번에 옮기는 물건.

여기서 틀리면 A 셀의 설정이 B 셀의 mAh/g 분모가 되고, 화면에는 아무 표시도
남지 않는다.  그래서 담는 것과 담지 않는 것을 테스트로 못 박는다 (ADR 0010).
"""

from __future__ import annotations


def _save(client, **body):
    return client.post("/api/composition-presets", json=body)


def test_a_preset_is_saved_and_listed_with_name_and_ratio(client):
    created = _save(client, name="건식 80", composition=[
        {"name": "NCM811", "wt_percent": 80, "role": "active"},
        {"name": "LPSCl", "wt_percent": 17, "role": "electrolyte"},
        {"name": "VGCF", "wt_percent": 3, "role": "conductive"},
    ])
    assert created.status_code == 201, created.text
    preset = created.json()
    assert preset["text"] == "NCM811:LPSCl:VGCF = 80:17:3"
    # 드롭박스는 이름만으로는 무엇인지 말해 주지 못한다.  비율이 고르는 대상이다.
    assert preset["label"] == "건식 80 · NCM811:LPSCl:VGCF = 80:17:3"

    listed = client.get("/api/composition-presets").json()
    assert [p["name"] for p in listed] == ["건식 80"]


def test_the_built_in_list_is_gone(client):
    """빈 목록으로 시작한다 — 쓰지도 않는 배합이 먼저 보이지 않는다."""
    assert client.get("/api/composition-presets").json() == []


def test_a_preset_carries_the_cell_settings_that_belong_to_a_build(client):
    preset = _save(client, name="13pi Li-In", composition=[
        {"name": "AM", "wt_percent": 80, "role": "active"},
        {"name": "SE", "wt_percent": 20, "role": "electrolyte"},
    ], settings={
        "diameter_mm": 13,
        "nominal_specific_capacity_mah_g": 205.9,
        "reference_electrode": "Li-In",
        "reference_offset_v": 0.62,
    }).json()
    assert preset["settings"]["diameter_mm"] == 13
    assert preset["settings"]["reference_electrode"] == "Li-In"
    assert preset["settings"]["nominal_specific_capacity_mah_g"] == 205.9
    assert preset["settings"]["reference_offset_v"] == 0.62
    # 채우지 않은 칸은 프리셋이 모르는 칸이다.  적용할 때 건드리면 안 된다.
    assert preset["settings"]["thickness_um"] is None


def test_a_preset_cannot_carry_a_mass(client):
    """질량은 셀 하나하나의 실측값이다.  실려 다니면 조용히 틀린다."""
    preset = _save(client, name="질량 시도", composition=[
        {"name": "AM", "wt_percent": 100, "role": "active"},
    ], settings={"diameter_mm": 13, "total_mass_mg": 31.6}).json()
    assert "total_mass_mg" not in preset["settings"]
    assert "active_mass_mg" not in preset["settings"]


def test_roles_survive_the_round_trip(client):
    """텍스트로 저장했으면 역할 추론이 다시 돌아 손으로 고친 값을 덮는다.

    `Zzz9` 는 이름으로는 알아볼 수 없는 물질이라 파싱하면 `other` 가 된다.
    사람이 활물질이라고 지정했으면 그대로 나와야 한다 — 이 값이 mAh/g 분모다.
    """
    preset = _save(client, name="사내 물질", composition=[
        {"name": "Zzz9", "wt_percent": 80, "role": "active"},
        {"name": "LPSCl", "wt_percent": 20, "role": "electrolyte"},
    ]).json()
    assert [c["role"] for c in preset["composition"]] == ["active", "electrolyte"]


def test_a_zero_percent_component_is_kept(client):
    """"이 배치엔 PTFE 없음" 은 공백이 아니라 기록이다 (ADR 0007)."""
    preset = _save(client, name="PTFE 0", composition=[
        {"name": "AM", "wt_percent": 80, "role": "active"},
        {"name": "SE", "wt_percent": 20, "role": "electrolyte"},
        {"name": "PTFE", "wt_percent": 0, "role": "binder"},
    ]).json()
    assert preset["text"] == "AM:SE:PTFE = 80:20:0"


def test_saving_over_a_name_needs_saying_so(client):
    _save(client, name="같은 이름", composition=[
        {"name": "AM", "wt_percent": 80, "role": "active"},
        {"name": "SE", "wt_percent": 20, "role": "electrolyte"},
    ])
    clash = _save(client, name="같은 이름", composition=[
        {"name": "AM", "wt_percent": 70, "role": "active"},
        {"name": "SE", "wt_percent": 30, "role": "electrolyte"},
    ])
    assert clash.status_code == 409
    assert "같은 이름" in clash.json()["detail"]
    # 원본은 그대로다.
    assert client.get("/api/composition-presets").json()[0]["text"] == "AM:SE = 80:20"

    replaced = _save(client, name="같은 이름", overwrite=True, composition=[
        {"name": "AM", "wt_percent": 70, "role": "active"},
        {"name": "SE", "wt_percent": 30, "role": "electrolyte"},
    ])
    assert replaced.status_code == 201
    assert replaced.json()["text"] == "AM:SE = 70:30"
    assert len(client.get("/api/composition-presets").json()) == 1


def test_an_empty_preset_is_refused(client):
    assert _save(client, name="빈 것").status_code == 422
    assert _save(client, name="   ", composition=[
        {"name": "AM", "wt_percent": 100, "role": "active"}]).status_code == 422


def test_a_setting_only_preset_is_allowed(client):
    """조성 없이 지름·기준전극만 저장하는 것도 쓸모가 있다."""
    preset = _save(client, name="13pi 셀", settings={"diameter_mm": 13}).json()
    assert preset["text"] == ""
    assert preset["label"] == "13pi 셀"
    assert preset["settings"]["diameter_mm"] == 13


def test_a_preset_is_deleted(client):
    preset = _save(client, name="지울 것", composition=[
        {"name": "AM", "wt_percent": 100, "role": "active"},
        {"name": "SE", "wt_percent": 0, "role": "electrolyte"},
    ]).json()
    assert client.delete(f"/api/composition-presets/{preset['id']}").status_code == 204
    assert client.get("/api/composition-presets").json() == []
    assert client.delete(f"/api/composition-presets/{preset['id']}").status_code == 404


def test_applying_a_preset_sets_the_sample_in_one_patch(client, sample_id):
    """화면이 실제로 보내는 요청.  프리셋 하나가 칸 여럿을 채운다."""
    preset = _save(client, name="적용", composition=[
        {"name": "NCM811", "wt_percent": 80, "role": "active"},
        {"name": "LPSCl", "wt_percent": 17, "role": "electrolyte"},
        {"name": "VGCF", "wt_percent": 3, "role": "conductive"},
    ], settings={
        "diameter_mm": 13,
        "nominal_specific_capacity_mah_g": 205.9,
        "reference_electrode": "Li-In",
    }).json()

    body = {"composition": preset["composition"],
            "clear": ["active_wt_percent"],
            **{k: v for k, v in preset["settings"].items() if v is not None}}
    sample = client.patch(f"/api/samples/{sample_id}", json=body).json()

    assert sample["diameter_mm"] == 13
    assert sample["nominal_specific_capacity_mah_g"] == 205.9
    assert sample["reference_electrode"] == "Li-In"
    # 조성이 활물질 wt% 를 도로 몰고 온다.
    assert sample["resolved_cell"]["active_wt_percent"] == 80
    assert sample["composition_label"] == "NCM811:LPSCl:VGCF = 80:17:3"


def test_an_unreadable_settings_blob_does_not_hide_the_other_presets(client):
    """한 줄이 깨졌다고 목록 전체가 500 이 되면 안 된다."""
    from sqlmodel import Session, select

    from app.db import engine
    from app.models import CompositionPreset

    _save(client, name="멀쩡한 것", settings={"diameter_mm": 13})
    _save(client, name="깨진 것", settings={"diameter_mm": 13})
    with Session(engine) as session:
        broken = session.exec(
            select(CompositionPreset).where(CompositionPreset.name == "깨진 것")).one()
        broken.settings_json = "{not json"
        session.add(broken)
        session.commit()

    listed = client.get("/api/composition-presets").json()
    assert {p["name"] for p in listed} == {"멀쩡한 것", "깨진 것"}
    broken_out = next(p for p in listed if p["name"] == "깨진 것")
    assert broken_out["settings"]["diameter_mm"] is None
