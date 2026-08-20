"""Samples, groups, and the cell spec that drives normalisation."""


def test_a_sample_resolves_its_cell_spec(client, sample_id):
    sample = client.get(f"/api/samples/{sample_id}").json()
    cell = sample["resolved_cell"]
    assert cell["active_mass_g"] == 0.02528          # 31.6 mg x 80 wt%
    assert round(cell["area_cm2"], 4) == 1.3273      # 13 mm punch
    assert round(cell["loading_mg_cm2"], 2) == 19.05
    assert round(cell["nominal_capacity_mah"], 4) == 5.2052
    assert set(cell["available_bases"]) == {"mAh", "mAh/g", "mAh/cm2", "%"}


def test_an_unavailable_basis_says_what_is_missing(client):
    created = client.post("/api/samples", json={"name": "bare"}).json()
    cell = client.get(f"/api/samples/{created['id']}").json()["resolved_cell"]
    assert cell["available_bases"] == ["mAh"]
    assert cell["unavailable"]["mAh/g"] == "active mass not set"
    assert cell["unavailable"]["mAh/cm2"] == "electrode area not set"


def test_the_spec_explains_how_each_number_was_derived(client, sample_id):
    notes = client.get(f"/api/samples/{sample_id}").json()["resolved_cell"]["notes"]
    assert "80 wt%" in notes["active_mass"]
    assert "13 mm" in notes["area"]


def test_correcting_the_mass_renormalises_without_reparsing(client, sample_id, wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    before = client.get(f"/api/samples/{sample_id}/cycles",
                        params={"basis": "mAh/g"}).json()["cycles"][0]

    client.patch(f"/api/samples/{sample_id}", json={"total_mass_mg": 15.8})
    after = client.get(f"/api/samples/{sample_id}/cycles",
                       params={"basis": "mAh/g"}).json()["cycles"][0]

    # Halving the mass doubles mAh/g; the raw mAh is untouched.
    assert after["discharge_capacity"] == before["discharge_capacity"] * 2
    assert after["discharge_capacity_mah"] == before["discharge_capacity_mah"]


def test_a_patch_only_touches_the_fields_it_names(client, sample_id):
    client.patch(f"/api/samples/{sample_id}", json={"notes": "재측정"})
    sample = client.get(f"/api/samples/{sample_id}").json()
    assert sample["notes"] == "재측정"
    assert sample["total_mass_mg"] == 31.6
    assert sample["cathode_detail"] == "NCM811"


def test_clear_removes_a_numeric_field(client, sample_id):
    client.patch(f"/api/samples/{sample_id}", json={"clear": ["diameter_mm"]})
    sample = client.get(f"/api/samples/{sample_id}").json()
    assert sample["diameter_mm"] is None
    assert "mAh/cm2" not in sample["resolved_cell"]["available_bases"]


def test_an_invalid_declared_state_is_rejected(client, sample_id):
    response = client.patch(f"/api/samples/{sample_id}",
                            json={"declared_state": "maybe"})
    assert response.status_code == 422


def test_a_reference_cycle_below_one_is_rejected(client, sample_id):
    assert client.patch(f"/api/samples/{sample_id}",
                        json={"reference_cycle": 0}).status_code == 422


def test_samples_can_be_filtered_the_way_the_bench_asks(client):
    client.post("/api/samples", json={"name": "A", "cathode_type": "High-Ni",
                                      "process": "dry", "test_date": "2026-02-01",
                                      "c_rate": 0.2})
    client.post("/api/samples", json={"name": "B", "cathode_type": "Mid-Ni",
                                      "process": "wet", "test_date": "2026-03-01",
                                      "c_rate": 0.5})
    high = client.get("/api/samples", params={"cathode_type": "High-Ni"}).json()
    assert [s["name"] for s in high] == ["A"]
    march = client.get("/api/samples", params={"date_from": "2026-02-15"}).json()
    assert [s["name"] for s in march] == ["B"]
    fast = client.get("/api/samples", params={"c_rate": 0.5}).json()
    assert [s["name"] for s in fast] == ["B"]


def test_facets_list_the_values_actually_present(client, sample_id):
    facets = client.get("/api/samples/facets").json()
    assert facets["cathode_type"] == ["High-Ni"]
    assert facets["process"] == ["dry"]
    assert "mAh/g" in facets["bases"]


def test_a_group_counts_its_samples_and_runs(client, sample_id, wrd_bytes):
    group = client.post("/api/groups", json={"name": "건식 80wt%",
                                             "color": "#3b6"}).json()
    client.patch(f"/api/samples/{sample_id}", json={"group_id": group["id"]})
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    refreshed = client.get(f"/api/groups/{group['id']}").json()
    assert refreshed["sample_count"] == 1
    assert refreshed["run_count"] == 1


def test_deleting_a_group_leaves_its_samples_ungrouped(client, sample_id):
    group = client.post("/api/groups", json={"name": "temp"}).json()
    client.patch(f"/api/samples/{sample_id}", json={"group_id": group["id"]})
    assert client.delete(f"/api/groups/{group['id']}").status_code == 204
    assert client.get(f"/api/samples/{sample_id}").json()["group_id"] is None


def test_deleting_a_sample_keeps_its_files_by_default(client, sample_id, wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    assert client.delete(f"/api/samples/{sample_id}").status_code == 204
    runs = client.get("/api/runs").json()
    assert len(runs) == 1
    assert runs[0]["sample_id"] is None


def test_deleting_a_sample_with_its_files_drops_their_parse_cache(client, sample_id,
                                                                  wrd_bytes):
    from app import storage

    run = client.post("/api/runs/upload", params={"sample_id": sample_id},
                      files={"file": ("c_012.wrd", wrd_bytes,
                                      "application/octet-stream")}).json()
    assert storage.columns_path(run["id"]).exists()

    assert client.delete(f"/api/samples/{sample_id}",
                         params={"delete_runs": True}).status_code == 204
    # Nothing can reach that run id again, so the npz would leak for good.
    assert not storage.columns_path(run["id"]).exists()
    assert storage.upload_path(run["sha256"]).exists()


def test_an_empty_sample_name_is_rejected(client):
    assert client.post("/api/samples", json={"name": "   "}).status_code == 422
