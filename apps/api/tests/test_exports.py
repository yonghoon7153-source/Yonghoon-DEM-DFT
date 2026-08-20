"""CSV and XLSX downloads."""

import csv
import io

import pytest

from app.routers import exports


@pytest.fixture
def two_files(client, sample_id, wrd_bytes, finished_wrd_bytes):
    """One experiment split the way Smart Interface splits it."""
    for name, content in (("c_011.wrd", finished_wrd_bytes),
                          ("c_012.wrd", wrd_bytes)):
        response = client.post("/api/runs/upload", params={"sample_id": sample_id},
                               files={"file": (name, content,
                                               "application/octet-stream")})
        assert response.status_code in (200, 201), response.text
    return sample_id


@pytest.fixture
def loaded(client, sample_id, wrd_bytes):
    run = client.post("/api/runs/upload", params={"sample_id": sample_id},
                      files={"file": ("c_012.wrd", wrd_bytes,
                                      "application/octet-stream")}).json()
    return sample_id, run["id"]


def _rows(response):
    text = response.content.decode("utf-8-sig")
    return list(csv.reader(io.StringIO(text)))


def test_raw_csv_has_a_row_per_sample(client, loaded):
    _, run_id = loaded
    response = client.get(f"/api/export/runs/{run_id}/raw.csv")
    assert response.status_code == 200
    rows = _rows(response)
    assert rows[0][:2] == ["timestamp", "test_time_s"]
    assert len(rows) > 100


def test_csv_is_utf8_with_a_bom_so_excel_reads_it(client, loaded):
    _, run_id = loaded
    response = client.get(f"/api/export/runs/{run_id}/raw.csv")
    assert response.content.startswith(b"\xef\xbb\xbf")
    assert "charset=utf-8" in response.headers["content-type"]


def test_the_download_filename_is_safe(client, loaded):
    sample_id, _ = loaded
    client.patch(f"/api/samples/{sample_id}", json={"name": "안용훈/셀 1: 건식"})
    response = client.get(f"/api/export/samples/{sample_id}/cycles.csv")
    disposition = response.headers["content-disposition"]
    assert "/" not in disposition.split("filename=")[1]
    assert ":" not in disposition.split("filename=")[1]


def test_cycles_csv_uses_the_requested_basis(client, loaded):
    sample_id, _ = loaded
    rows = _rows(client.get(f"/api/export/samples/{sample_id}/cycles.csv",
                            params={"basis": "mAh/g"}))
    assert "discharge_capacity (mAh/g)" in rows[0]
    assert len(rows) == 8   # header + 7 complete cycles


def test_profiles_csv_has_a_column_pair_per_branch(client, loaded):
    sample_id, _ = loaded
    rows = _rows(client.get(f"/api/export/samples/{sample_id}/profiles.csv",
                            params={"cycles": "1,2", "basis": "mAh/g"}))
    assert rows[0][0] == "cycle1_charge_capacity (mAh/g)"
    assert len(rows[0]) == 8     # 2 cycles x 2 branches x (capacity, voltage)


def test_profiles_csv_reports_an_empty_selection(client, loaded):
    sample_id, _ = loaded
    response = client.get(f"/api/export/samples/{sample_id}/profiles.csv",
                          params={"cycles": "900"})
    assert response.status_code == 404


def test_workbook_has_metadata_cycles_and_profiles(client, loaded):
    openpyxl = pytest.importorskip("openpyxl")
    sample_id, _ = loaded
    response = client.get(f"/api/export/samples/{sample_id}/workbook.xlsx",
                          params={"cycles": "1,2", "basis": "mAh/g"})
    assert response.status_code == 200
    book = openpyxl.load_workbook(io.BytesIO(response.content))
    assert book.sheetnames == ["metadata", "cycles", "profiles"]
    labels = [row[0] for row in book["metadata"].iter_rows(values_only=True)]
    assert "active mass (mg)" in labels
    assert "loading (mg/cm2)" in labels


def test_the_raw_sheet_carries_every_file_of_a_split_experiment(client, two_files):
    """Exporting only the last file would drop half the experiment silently."""
    openpyxl = pytest.importorskip("openpyxl")
    runs = client.get("/api/runs").json()
    total_rows = sum(run["row_count"] for run in runs)

    response = client.get(f"/api/export/samples/{two_files}/workbook.xlsx",
                          params={"cycles": "1", "include_raw": "true"})
    assert response.status_code == 200
    book = openpyxl.load_workbook(io.BytesIO(response.content))

    raw = book["raw"]
    assert raw.max_row == total_rows + 1          # header
    sources = {row[0] for row in raw.iter_rows(min_col=raw.max_column,
                                               max_col=raw.max_column,
                                               min_row=2, values_only=True)}
    assert sources == {"c_011.wrd", "c_012.wrd"}

    metadata = dict(row[:2] for row in book["metadata"].iter_rows(values_only=True))
    assert metadata["samples"] == total_rows


def test_a_profile_export_reads_each_file_once(client, two_files, monkeypatch):
    """The cache is one compressed archive per file; re-reading it per cycle
    turned a long experiment's export into minutes of decompression."""
    loads = []
    original = exports.load_wrd_columns
    monkeypatch.setattr(exports, "load_wrd_columns",
                        lambda run: (loads.append(run.id), original(run))[1])

    response = client.get(f"/api/export/samples/{two_files}/profiles.csv")
    assert response.status_code == 200
    assert sorted(loads) == sorted(set(loads))
    assert len(loads) == 2
