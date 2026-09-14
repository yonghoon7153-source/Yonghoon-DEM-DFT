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
    assert S.meta_controls("cycles") == ("cell", "si_source", "starts", "seed", "scale_seed")
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


def test_cy_05_start_seed_and_scale_seed_are_separate_controls(tmp_path):
    """결정 실험의 둘째 절반은 "시작점이 정한 적합인가" 다 — 그러려면 `--seed` 는 **시작점만** 움직여야 하고
    목적함수 scale(50 표본, R5-07)은 `--scale-seed` 로 따로 고정해야 한다. 사용자 기계 첫 실행(HD_knee, seed 0/1)에서
    두 축이 한 인자에 묶여 있어 값 차이(~1e-3)가 시작점 탓인지 scale 탓인지 가를 수 없었다."""
    src = _synth_root(tmp_path)
    wb = _cycle_workbook(src, tmp_path / "L_syn_cycles.xlsx", n_cycles=2)

    def run(seed, scale_seed, dest):
        r = subprocess.run([sys.executable, str(ROOT / "scripts/fit_cycles.py"), "--data-root", str(src),
                            "--half-cell", str(src / "data/half_cell/GITT/pristine.xlsx"), "--full-cell", str(wb),
                            "--cell", "L_syn", "--si-source", "Li", "--starts", "1", "--seed", str(seed),
                            "--scale-seed", str(scale_seed), "--out", str(dest)],
                           cwd=ROOT, capture_output=True, text=True, timeout=600)
        assert r.returncode == 0, (r.stdout[-1200:], r.stderr[-1200:])
        art = dest / "cycles_L_syn_Li.csv"
        rows = list(csv.DictReader(art.open(encoding="utf-8")))
        meta = json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8"))
        return rows, meta

    a, ma = run(0, 0, tmp_path / "a")
    b, mb = run(1, 0, tmp_path / "b")                      # 시작점만 다르다
    c, mc = run(0, 1, tmp_path / "c")                      # scale 만 다르다
    for col in ("scale_pocv", "scale_dvdq", "scale_dqdv", "scale_seed"):
        assert col in S.CYCLES_ROW and [r[col] for r in a] == [r[col] for r in b], col
    assert any(a[i]["scale_pocv"] != c[i]["scale_pocv"] for i in range(len(a)))
    assert ma["scale_seed"] == 0 and mc["scale_seed"] == 1 and mb["seed"] == 1
    assert "scale_seed" in S.meta_controls("cycles") and "seed" in S.meta_controls("cycles")
    assert ma["run_id"] != mb["run_id"]


# ── 외부 문헌 파일 (pyDMA 예제 형식) — 정본 8 소스 로스터를 건드리지 않고 검증 데이터를 받는다 ────────────
def _pydma_literature(src: pathlib.Path, path: pathlib.Path):
    """pyDMA 예제의 문헌 레이아웃: 한 시트에 `Si_capacity/Si_voltage/Gr_capacity/Gr_voltage` (열마다 길이가 다르다).

    합성 원자료의 Gr/Si 를 그 모양으로 옮겨 적는다 — 열마다 NaN 꼬리가 다른 것까지 재현한다.
    """
    import pandas as pd
    gr = pd.read_excel(src / "data/literature/Si_Gr_literature_OCP.xlsx")
    si = pd.read_csv(src / "data/literature/Si_OCP_sources/Li.csv")
    n = max(len(gr), len(si))
    pad = lambda a: list(a) + [float("nan")] * (n - len(a))
    pd.DataFrame({"Si_capacity": pad(si["normalizedCapacity"]), "Si_voltage": pad(si["voltage"]),
                  "Gr_capacity": pad(gr["Gr_capacity"].dropna()), "Gr_voltage": pad(gr["Gr_voltage"].dropna())
                  }).to_excel(path, index=False)
    return path


def test_cy_06_external_literature_file_is_read_and_receipted_as_itself(tmp_path):
    """[pyDMA 검증, 2026-09-14] 검증 데이터(pyDMA 예제)는 **자기 문헌 파일**을 들고 온다 — Si·Gr 이 한 시트에 있고
    정본 8 소스 로스터에 속하지 않는다. 그 파일을 로스터 이름 하나에 밀어 넣으면 receipt 가 거짓말을 하므로
    (`literature.si` 가 `Li.csv` 라고 적히는데 실제 bytes 는 남의 파일) **외부 문헌 경로**를 따로 받는다.

    계약: 같은 receipt 역할 넷을 그대로 지키되 `literature.gr`·`literature.si` 가 **그 파일**을 가리킨다 —
    한 파일이 두 곡선을 다 주므로 두 역할의 sha256 이 같은 것이 사실이다.
    """
    src = _synth_root(tmp_path)
    lit = _pydma_literature(src, tmp_path / "pydma_lit.xlsx")
    si_c, si_v, gr_c, gr_v = C.D.load_literature_file(lit)
    assert len(si_c) == len(si_v) > 2 and len(gr_c) == len(gr_v) > 2
    assert not (np.isnan(si_c).any() or np.isnan(gr_c).any()), "열마다 NaN 꼬리를 따로 잘라야 한다"

    wb = _cycle_workbook(src, tmp_path / "cyc.xlsx", n_cycles=2)
    out = C.fit_cycles(src, src / "data/half_cell/GITT/pristine.xlsx", wb, "external",
                       cell="pydma", n_starts=2, seed=0, scale_seed=0, literature=lit)
    import hashlib
    want = hashlib.sha256(lit.read_bytes()).hexdigest()
    rec = json.loads(out["rows"][0]["consumed_inputs"])
    assert set(S.REQUIRED_ROLES) == {"full_cell", "half_cell", "literature.gr", "literature.si"}
    assert rec["literature"]["gr"]["sha256"] == want and rec["literature"]["si"]["sha256"] == want, rec
    assert pathlib.Path(rec["literature"]["si"]["path"]).name == lit.name, rec
    assert not S.validate_receipt(out["rows"][0]["consumed_inputs"], out["rows"][0]["inputs_sha"], "cy06"), "계약 위반"


def test_cy_07_external_literature_and_the_source_label_must_agree(tmp_path):
    """짝이 안 맞는 호출은 **입력 오류(rc 2)** 다 — 외부 파일을 주면서 로스터 이름을 대거나(그 이름의 데이터가
    아니다), `external` 이라 해 놓고 파일을 안 주거나(무엇을 읽었는지 말할 수 없다) 둘 다 막는다."""
    src = _synth_root(tmp_path)
    lit = _pydma_literature(src, tmp_path / "pydma_lit.xlsx")
    wb = _cycle_workbook(src, tmp_path / "cyc.xlsx", n_cycles=2)
    base = [sys.executable, str(ROOT / "scripts/fit_cycles.py"), "--data-root", str(src),
            "--half-cell", str(src / "data/half_cell/GITT/pristine.xlsx"), "--full-cell", str(wb),
            "--cell", "pydma", "--starts", "2", "--out", str(tmp_path / "o")]

    r = subprocess.run(base + ["--si-source", "Li", "--literature", str(lit)],
                       capture_output=True, text=True, cwd=ROOT, timeout=300)
    assert r.returncode == 2 and "external" in (r.stdout + r.stderr), (r.returncode, r.stdout[-400:], r.stderr[-400:])

    r = subprocess.run(base + ["--si-source", "external"], capture_output=True, text=True, cwd=ROOT, timeout=300)
    assert r.returncode == 2 and "--literature" in (r.stdout + r.stderr), (r.returncode, r.stdout[-400:], r.stderr[-400:])

    r = subprocess.run(base + ["--si-source", "external", "--literature", str(lit)],
                       capture_output=True, text=True, cwd=ROOT, timeout=600)
    assert r.returncode == 0, (r.returncode, r.stdout[-600:], r.stderr[-600:])
    assert (tmp_path / "o" / "cycles_pydma_external.csv").is_file(), list((tmp_path / "o").iterdir())
