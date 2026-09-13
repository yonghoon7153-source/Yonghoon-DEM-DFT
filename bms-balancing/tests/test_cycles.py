"""사이클별 α·β 적합 포팅 (`bms_balancing/cycles.py` · `scripts/fit_cycles.py`) — BML §9 결정 실험을 우리 하네스로.

규진팀 `main_blend_final.m` 의 사이클 루프와 같은 모델·경계·수출 공식으로, 산출은 하네스 계약(run_id · sha256 ·
행별 receipt · sidecar · `check_u14` · `check_rails`)을 지킨다. 원자료 형식은 `extractMyData` 규약
('<cycle>_capacity' / '<cycle>_voltage' 열) — 규진팀 파이프라인이 읽는 그 형식이다.
"""
from __future__ import annotations

import csv
import json
import pathlib
import subprocess
import sys

import numpy as np
import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from bms_balancing import schema as S          # noqa: E402
from bms_balancing import cycles as C          # noqa: E402
from test_r6_internal import _synth_root       # noqa: E402


def _cycle_workbook(src: pathlib.Path, path: pathlib.Path, n_cycles: int = 3):
    """합성 원자료의 풀셀 상태 열들을 '<cycle>_capacity/<cycle>_voltage' 워크북으로 — 상태 = 사이클로 본다."""
    import pandas as pd
    df = pd.read_excel(src / "data/full_cell/large_cell_033C/fullcell_states.xlsx", header=None, skiprows=2)
    cols = {}
    for k in range(n_cycles):
        cols[f"{k}_capacity"] = pd.to_numeric(df[2 * k], errors="coerce")
        cols[f"{k}_voltage"] = pd.to_numeric(df[2 * k + 1], errors="coerce")
    pd.DataFrame(cols).to_excel(path, index=False)
    return path


def test_cy_01_cycles_is_a_registered_artifact_kind():
    assert S.kind_of("cycles_L_ref1_Li.csv") == "cycles"
    assert S.required_columns("cycles") == S.CYCLES_ROW
    assert {"cell", "cycle", "C_cell", "x_cell", "a_PE", "b_PE", "a_NE", "b_NE", "gamma_Si", "c_lit",
            "LAM_PE", "LAM_NE", "LLI", "run_id", "inputs_sha", "consumed_inputs"} <= set(S.CYCLES_ROW)
    assert S.row_key("cycles")({"cycle": "3"}) == 3 and S.row_key("cycles")({"cycle": 3.0}) == 3
    assert S.meta_controls("cycles") == ("cell", "si_source", "starts", "seed")
    assert S.receipt_roles("cycles") == S.REQUIRED_ROLES


def test_cy_02_discover_and_load_cycles_from_the_extractMyData_layout(tmp_path):
    import pandas as pd
    pd.DataFrame({"0_capacity": [0.0, 1.0, 2.0], "0_voltage": [3.0, 3.5, 4.0],
                  "5_capacity": [0.0, 0.9, np.nan], "5_voltage": [3.0, 3.6, np.nan],
                  "note": ["x", "y", "z"]}).to_excel(tmp_path / "w.xlsx", index=False)
    df = C.read_workbook(tmp_path / "w.xlsx")
    assert C.discover_cycles(df) == [0, 5]
    c, v = C.load_cycle(df, 5)
    assert c.tolist() == [0.0, 0.9] and v.tolist() == [3.0, 3.6]
    with pytest.raises(KeyError):
        C.load_cycle(df, 7)


def test_cy_03_fit_cycles_end_to_end_passes_rails_and_u14(tmp_path):
    """실제 producer(`scripts/fit_cycles.py`) → `check_rails.py` rc 0 (항등식 정확) → `check_u14 --schema-only`
    계약 위반 0 (run_id · receipt · sidecar). 두 seed 의 산출은 **서로 다른 run_id** 를 가지고 같은 입력 identity 를 적는다."""
    src = _synth_root(tmp_path)
    wb = _cycle_workbook(src, tmp_path / "L_syn_cycles.xlsx", n_cycles=3)
    out = tmp_path / "out"; out.mkdir()

    def run(seed, dest):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/fit_cycles.py"), "--data-root", str(src),
                            "--half-cell", str(src / "data/half_cell/GITT/pristine.xlsx"), "--full-cell", str(wb),
                            "--cell", "L_syn", "--si-source", "Li", "--starts", "2", "--seed", str(seed),
                            "--out", str(dest)], cwd=ROOT, capture_output=True, text=True, timeout=900)
        assert r.returncode == 0, (r.stdout[-1500:], r.stderr[-1500:])
        return r.stdout

    text = run(0, out)
    art = out / "cycles_L_syn_Li.csv"
    assert art.is_file() and art.with_name(art.name + ".meta.json").is_file(), text[-800:]
    rows = list(csv.DictReader(art.open(encoding="utf-8")))
    assert [r["cycle"] for r in rows] == ["0", "1", "2"] and list(rows[0]) == list(S.CYCLES_ROW)
    assert float(rows[0]["x_cell"]) == 1.0 and float(rows[0]["LLI"]) == 0.0 and float(rows[0]["LAM_PE"]) == 0.0
    assert all(1.0 <= float(r["a_PE"]) <= 1.4 and 0.0 <= float(r["gamma_Si"]) <= 0.5 for r in rows)
    # 하네스 계약: 행별 receipt 가 유효하고 sidecar 가 본문과 묶여 있다
    assert not [q for q in S.check_rows("cycles", rows, list(rows[0]), name=art.name)], \
        S.check_rows("cycles", rows, list(rows[0]), name=art.name)
    meta = json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8"))
    assert meta["roster"] == S.body_roster(art.name, art.read_bytes()) and meta["roster"]["kind"] == "cycles"
    assert meta["cell"] == "L_syn" and meta["starts"] == 2 and meta["seed"] == 0 and meta["si_source"] == "Li"
    assert meta["lb"] == [1.0, -0.5, 1.0, -0.5, 0.0] and meta["ub"] == [1.4, 0.0, 1.4, 0.1, 0.5]
    u14 = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(out), "--schema-only"],
                         cwd=ROOT, capture_output=True, text=True, timeout=300)
    promo = json.loads(next(l for l in u14.stdout.splitlines() if l.startswith("PROMOTION "))[len("PROMOTION "):])
    b = promo["blocked_by"]
    assert all(b[k] == 0 for k in ("schema", "provenance_cols", "content", "unit")), (b, u14.stdout[-2000:])
    # 난간: 같은 검사기가 우리 산출을 읽는다 — 항등식 정확, 설정은 sidecar 에서
    rails = subprocess.run([sys.executable, str(ROOT / "scripts/check_rails.py"), str(art)],
                           cwd=ROOT, capture_output=True, text=True, timeout=300)
    j = json.loads(next(l for l in rails.stdout.splitlines() if l.startswith("RAILS "))[len("RAILS "):])
    assert rails.returncode == 0 and j["ok"] is True and j["files"][0]["settings"], rails.stdout[-1500:]
    assert "active_bound" in rails.stdout and "evidence" in rails.stdout and "rmse_pocv" in rails.stdout
    # 두 번째 seed — 다른 run_id, 같은 입력 identity
    out2 = tmp_path / "out2"; out2.mkdir()
    run(1, out2)
    rows2 = list(csv.DictReader((out2 / "cycles_L_syn_Li.csv").open(encoding="utf-8")))
    assert rows2[0]["run_id"] != rows[0]["run_id"] and rows2[0]["inputs_sha"] == rows[0]["inputs_sha"]


def test_cy_04_producer_refuses_a_workbook_without_cycle_zero(tmp_path):
    import pandas as pd
    src = _synth_root(tmp_path)
    pd.DataFrame({"3_capacity": [0.0, 1.0, 2.0], "3_voltage": [3.0, 3.5, 4.0]}).to_excel(tmp_path / "no0.xlsx", index=False)
    r = subprocess.run([sys.executable, str(ROOT / "scripts/fit_cycles.py"), "--data-root", str(src),
                        "--half-cell", str(src / "data/half_cell/GITT/pristine.xlsx"), "--full-cell", str(tmp_path / "no0.xlsx"),
                        "--cell", "L_x", "--si-source", "Li", "--starts", "1", "--out", str(tmp_path / "o")],
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    assert r.returncode == 2 and "cycle 0" in (r.stdout + r.stderr), (r.returncode, (r.stdout + r.stderr)[-600:])
    assert not (tmp_path / "o" / "cycles_L_x_Li.csv").exists()
