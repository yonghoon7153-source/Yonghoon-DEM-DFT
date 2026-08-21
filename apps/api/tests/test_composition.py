"""Electrode composition through the API, and the mass it produces."""

import pytest


def test_a_composition_string_sets_the_active_fraction(client):
    sample = client.post("/api/samples", json={
        "name": "comp-1",
        "total_mass_mg": 31.6,
        "diameter_mm": 13,
        "composition_text": "AM:SE:VGCF = 80:17:3",
    }).json()
    assert sample["active_wt_percent"] == 80
    assert sample["composition_label"] == "AM:SE:VGCF = 80:17:3"
    assert sample["resolved_cell"]["active_mass_g"] == pytest.approx(0.02528)


def test_components_can_be_sent_structured(client):
    sample = client.post("/api/samples", json={
        "name": "comp-2",
        "total_mass_mg": 20.0,
        "composition": [
            {"name": "NCM811", "wt_percent": 78, "role": "active"},
            {"name": "LPSCl", "wt_percent": 17, "role": "electrolyte"},
            {"name": "VGCF", "wt_percent": 3, "role": "conductive"},
            {"name": "PTFE", "wt_percent": 2, "role": "binder"},
        ],
    }).json()
    assert sample["active_wt_percent"] == 78
    assert [c["name"] for c in sample["composition"]] == [
        "NCM811", "LPSCl", "VGCF", "PTFE"]
    assert sample["resolved_cell"]["active_mass_g"] == pytest.approx(0.0156)


def test_a_zero_weight_binder_is_kept_and_changes_nothing(client):
    """A PTFE-free batch is a deliberate record, not a blank."""
    sample = client.post("/api/samples", json={
        "name": "no-binder",
        "total_mass_mg": 31.6,
        "composition_text": "AM:SE:VGCF:PTFE = 80:17:3:0",
    }).json()
    assert sample["active_wt_percent"] == 80
    assert len(sample["composition"]) == 4
    assert sample["composition"][-1]["wt_percent"] == 0
    cell = sample["resolved_cell"]
    assert cell["active_mass_g"] == pytest.approx(0.02528)
    assert cell["composition_problems"] == []
    # The one-line form drops the zero, the full record keeps it.
    assert cell["composition_compact_label"] == "AM:SE:VGCF = 80:17:3"
    assert cell["composition_label"] == "AM:SE:VGCF:PTFE = 80:17:3:0"


def test_a_composition_that_does_not_add_to_100_is_flagged_not_rejected(client):
    sample = client.post("/api/samples", json={
        "name": "off-by-two",
        "total_mass_mg": 31.6,
        "composition_text": "AM:SE:VGCF = 80:17:5",
    }).json()
    problems = sample["resolved_cell"]["composition_problems"]
    assert problems and "102" in problems[0]
    # It still normalises -- the researcher may have meant parts, not percent.
    assert sample["resolved_cell"]["active_mass_g"] is not None


def test_an_explicit_weight_percent_wins_in_the_same_request(client):
    sample = client.post("/api/samples", json={
        "name": "override",
        "total_mass_mg": 31.6,
        "active_wt_percent": 70,
        "composition_text": "AM:SE:VGCF = 80:17:3",
    }).json()
    assert sample["active_wt_percent"] == 70
    assert sample["composition_label"] == "AM:SE:VGCF = 80:17:3"


def test_editing_the_composition_renormalises_every_capacity(client, wrd_bytes):
    sample = client.post("/api/samples", json={
        "name": "edit-me", "total_mass_mg": 31.6, "diameter_mm": 13,
        "composition_text": "AM:SE:VGCF = 80:17:3",
    }).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("c.wrd", wrd_bytes, "application/octet-stream")})
    before = client.get(f"/api/samples/{sample['id']}/cycles",
                        params={"basis": "mAh/g"}).json()["cycles"][0]

    client.patch(f"/api/samples/{sample['id']}",
                 json={"composition_text": "AM:SE:VGCF = 40:57:3"})
    after = client.get(f"/api/samples/{sample['id']}/cycles",
                       params={"basis": "mAh/g"}).json()["cycles"][0]

    assert after["discharge_capacity"] == pytest.approx(
        before["discharge_capacity"] * 2)
    assert after["discharge_capacity_mah"] == before["discharge_capacity_mah"]


def test_clearing_the_composition_leaves_the_sample_usable(client):
    sample = client.post("/api/samples", json={
        "name": "clear-me", "total_mass_mg": 31.6,
        "composition_text": "AM:SE:VGCF = 80:17:3",
    }).json()
    cleared = client.patch(f"/api/samples/{sample['id']}",
                           json={"clear": ["composition", "active_wt_percent"]}).json()
    assert cleared["composition"] == []
    # With no composition the whole film counts, and the note says so.
    assert cleared["resolved_cell"]["active_mass_g"] == pytest.approx(0.0316)
    assert "assuming the whole electrode" in cleared["resolved_cell"]["notes"]["active_mass"]


def test_unreadable_text_does_not_silently_invent_a_composition(client):
    sample = client.post("/api/samples", json={
        "name": "junk", "total_mass_mg": 31.6,
        "composition_text": "어제 만든 그 전극",
    }).json()
    assert sample["composition"] == []
    assert sample["active_wt_percent"] is None


def test_roles_are_offered_by_the_api(client):
    meta = client.get("/api/meta").json()
    assert {r["value"] for r in meta["component_roles"]} == {
        "active", "electrolyte", "conductive", "binder", "other"}
    # Presets are rows now, saved by whoever is at the bench (ADR 0010).  A
    # list baked into /api/meta could not be added to without a restart.
    assert "composition_presets" not in meta


def test_an_unknown_material_never_becomes_active_material(client):
    """It would silently enter the mAh/g denominator."""
    sample = client.post("/api/samples", json={
        "name": "mystery", "total_mass_mg": 31.6,
        "composition_text": "Zzz9:SE = 80:20",
    }).json()
    assert sample["active_wt_percent"] is None
    problems = sample["resolved_cell"]["composition_problems"]
    assert any("active material" in p for p in problems)
