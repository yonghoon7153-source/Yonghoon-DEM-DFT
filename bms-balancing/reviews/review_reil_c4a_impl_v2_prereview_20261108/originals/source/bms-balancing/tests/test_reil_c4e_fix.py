"""REIL C4-E · E0 한정 정정 (C4E-E0-N1 · 다섯 모듈의 신뢰 기대 sha) — 변경부의 양성 · 음성 대조 6 ID (상태 문서 §69 · 승인 요청 §3).

승인 전 고정본: `docs/REIL_C4E_E0_FIX_CONTROLS_DRAFT_20261014.py.txt`. 승인 뒤 `tests/test_reil_c4e_fix.py` 로 바이트 그대로 복사해 쓴다
(sha256 은 승인 요청문 `docs/REIL_C4E_E0_FIX_APPROVAL_REQUEST_20261014.md`). 고칠 곳 `docs/REIL_C4E_E0_FIX_PATCH_DRAFT_20261014.diff` 도 같이 고정.

검증 축 (검토 회신 N1): 정상 기대값 (n1_a) · 기대 항목 누락 · 목록 형식 · 목록 sha (n1_b) · 시작부터 틀렸으나 끝까지 같은 소스 (n1_c) · 실행 중 변화
(n1_d) · CLI 가 목록을 기본값 없이 요구 (n1_e) · 목록 작성 · plan-e 범위 (n1_f). 가짜 util · 합성 P0 · 임시 폴더 · 모듈 사본만 쓴다.
REIL xlsx · pkl · 노트북 · 네트워크 · 실제 optimizer · 보존 util 사본 · Sobol · fork 는 0 이다. 기존 시험 파일은 고치지 않는다.
각 시험 docstring 의 [RED …] 는 지금 코드 (패치 전) 에서의 예상 실패 종류다.
"""
import hashlib
import importlib.machinery
import importlib.util
import json
import time
from pathlib import Path

import pytest

from scripts import reil_c4e_run as run
from scripts import reil_c5_pilot as c5

BMS = Path(__file__).resolve().parents[1]
NEW_SEAL = BMS / "reil_c6_rebuild_20261013"
NEW_SEAL_MANIFEST = "4f12094897b53463097e78dafc0bfe5f37c1d76bb1a6266c0a907d755fb2ebdc"
#: 신뢰 소스 목록의 경로 집합 — 시험이 따로 적는다 (모듈 상수와 n1_f 에서 대조)
MODS = ("scripts/reil_c4e_run.py", "scripts/reil_c4_e3a.py", "scripts/reil_c4_monitor.py", "scripts/reil_c5_pilot.py",
        "scripts/reil_p0.py")
C4_0A_FIELDS = ("task_id", "call_id", "case", "row", "obj_selection", "algorithm", "worker",
                "n_eval", "n_nonfinite", "n_nonfinite_any_of_4", "n_out_eval_PE", "n_out_eval_NE", "n_out_eval_any",
                "n_out_unknown_eval", "n_dvdq_observed", "n_eval_x_out_of_box", "n_eval_G_violated",
                "extraction", "model_digest", "halfcell_digest", "warnings_count", "warnings_distinct_overflow",
                "success_is_evidence", "n_eval_minus_expected",
                "termination", "error", "X", "F", "G", "G_status", "n_solutions", "F_nonfinite_count", "G_violation_recomputed",
                "G_violation_exact", "box_violation_exact", "success_reported",
                "wall", "cpu", "state", "t_start_rel")


# ======================================================================== 도우미 (E0 대조와 같은 꼴 — 시험 파일끼리 import 하지 않는다)
def _fake_ident(**kw):
    return {"ok": True, "problems": [], "record": {}, "full_c6_check": "NOT_RUN"}


def _sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _real_entries():
    """다섯 모듈의 지금 바이트 — 시험이 직접 해시한다 (모듈 함수를 쓰지 않음)."""
    return {rel: {"sha256": _sha_file(BMS / rel), "bytes": (BMS / rel).stat().st_size} for rel in MODS}


def _write_sources(d, files, schema="reil-c4e-sources-v1"):
    d.mkdir(parents=True, exist_ok=True)
    p = d / "SOURCES.json"
    p.write_bytes((json.dumps({"schema": schema, "files": files}, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8"))
    return p, _sha_file(p)


def _good_row(t, wall=1.0):
    row = {k: None for k in C4_0A_FIELDS}
    row.update({k: t[k] for k in ("task_id", "call_id", "case", "row", "obj_selection", "algorithm", "worker")})
    row.update(n_eval=3, termination="returned", state="COMPLETED", wall=wall, cpu=wall, t_start_rel=1.0, X=[[0.9, 0.8, 0.2, 0.1]],
               F=[[0.1]], G=[[-0.1]], G_status="보고됨", success_is_evidence=False)
    return row


def _sup(states, n_workers=4, **kw):
    s = {"states": states, "global_stop": None, "structural": [], "samples": {"rss": [], "disk": []},
         "workers": {w: {"pid": 1, "t": 0.0} for w in range(n_workers)}, "worker_end": {w: {"t": 1.0} for w in range(n_workers)},
         "worker_deadline": {}, "exitcodes": {w: 0 for w in range(n_workers)}, "owned_alive_after": 0, "drain_ok": True,
         "t_stop": 10.0, "deadline_rel": 9000.0}
    s.update(kw)
    return s


FAKE_UTIL = '''"""가짜 util (C4-E E0 정정 대조) — 자료 파일을 열지 않고 시트 이름으로 곡선을 만든다 (REIL 자료 아님)."""
import numpy as np


class SheetData(list):
    """셀별 [Q; V] 배열 목록 — 시트 이름을 붙인다."""


def _curve(sheet_name, n_cells):
    k = (sum(ord(c) for c in sheet_name) % 89) / 89.0
    g = 1.5 if "Graphite" in sheet_name else 1.0
    out = SheetData()
    for cell in range(n_cells):
        n = 40 + int(20 * k) + cell
        q = np.linspace(0.0, (2.0 + k + 0.1 * cell) * g, n)
        v = 3.0 + 0.4 * np.sqrt(q / q[-1]) + 0.01 * cell
        out.append(np.vstack([q, v]))
    out.sheet = sheet_name
    return out


def visualize_LFP_data(data_file, sheet_name, step_idx, visualize=True):
    return _curve(sheet_name, 2)


def extract_battery_data(data, idx):
    a = data[idx]
    q, v = np.asarray(a[0], dtype=float), np.asarray(a[1], dtype=float)
    qi = np.linspace(q[0], q[-1], 30)
    vi = np.interp(qi, q, v)
    return {"Q_exp": q, "V_exp": v, "Q_exp_max": float(np.max(q)), "Q_exp_interp": qi, "V_exp_interp": vi,
            "dVdQ_exp_interp": np.gradient(vi, qi), "sheet": getattr(data, "sheet", None)}


def run_optimization(Model, halfcell, obj_selection, pop_size=50):
    raise AssertionError("N1 대조에서 optimizer 를 부르면 안 된다")
'''


def _fake_util(d):
    d.mkdir(parents=True, exist_ok=True)
    p = d / "util_LFP_fake_n1.py"
    p.write_text(FAKE_UTIL, encoding="utf-8")
    loader = importlib.machinery.SourceFileLoader(f"fake_util_c4e_n1_{d.name}", str(p))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod, p


def _fake_p0(loaded):
    ext = ([dict(r, kind="reference", status="OK") for r in loaded["references"]]
           + [dict(r, kind="analysis", status="OK") for r in loaded["rows"]])
    return {"extraction": ext, "max_q": {"float": loaded["PE"]["max_q"], "n_q_PE_hc": loaded["PE"]["n_q_PE_hc"], "status": "OK"},
            "q_NE_hc_max_record_only": loaded["NE"]["q_NE_hc_max_record_only"], "notebook_check": {"ok": True}}


def _write_p0(d, obj):
    d.mkdir(parents=True, exist_ok=True)
    p = d / "P0_RESULT.json"
    p.write_bytes((json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8"))
    return p, _sha_file(p)


def _setup(tmp_path):
    """가짜 util · 가짜 xlsx 경로 · 그 util 로 만든 합성 P0 → prepare 의 공통 인자 (자료 · optimizer 0)."""
    mod, util_p = _fake_util(tmp_path / "u")
    xlsx = tmp_path / "LFP_Data.xlsx"
    xlsx.write_bytes(b"fake workbook path - never opened")
    loaded = run.load_inputs(mod, xlsx)
    p0_p, p0_sha = _write_p0(tmp_path / "p0", _fake_p0(loaded))
    expected = {"LFP_Data.xlsx": {"sha256": _sha_file(xlsx), "bytes": xlsx.stat().st_size},
                "util_LFP.py": {"sha256": _sha_file(util_p), "bytes": util_p.stat().st_size}, "P0_RESULT.json": {"sha256": p0_sha}}
    loads = []

    def spy_load(path, sha):
        loads.append(str(path))
        return c5.load_util(path, sha)

    base = dict(venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, xlsx=xlsx, util_path=util_p, p0_result=p0_p,
                expected=expected, env_identity=_fake_ident, load_util=spy_load)
    return base, loads


def _plan_rule_sup():
    plan = run.plan()
    return plan, run.StopRule(plan), _sup([_good_row(t) for t in plan])


# ======================================================================== N1 — 신뢰 소스 목록 · 시작 / 끝 표 · 수용 판정
def test_n1_a_a_trusted_list_binds_the_five_modules_to_start_end_and_acceptance(tmp_path, monkeypatch):
    """[RED 실패 — AttributeError: 지금 load_sources 가 없다] 정상 기대값: 목록 sha 일치 · 경로 정확히 다섯 · 실제 바이트 일치 → prepare 통과
    (순서 identity → 목록 → sha → 경로 → util) · 다섯 모듈 행의 기대 = 목록 값 · 필수 행 10 · 같은 기대값으로 끝 재해시 → 실제 finalize 의
    사전 · 최종 COMPLETE · IDENTITY.json 의 끝 표에도 같은 기대값."""
    entries = _real_entries()
    src, src_sha = _write_sources(tmp_path / "src", entries)
    assert run.load_sources(src, src_sha) == entries
    base, loads = _setup(tmp_path)
    order = []
    real_sources, real_table, real_paths = run.load_sources, run.identity_table, run.check_paths
    monkeypatch.setattr(run, "load_sources", lambda *a, **k: (order.append("sources"), real_sources(*a, **k))[1])
    monkeypatch.setattr(run, "identity_table", lambda *a, **k: (order.append("sha"), real_table(*a, **k))[1])
    monkeypatch.setattr(run, "check_paths", lambda **k: (order.append("paths"), real_paths(**k))[1])

    def ident(**kw):
        order.append("identity")
        return _fake_ident()

    prep = run.prepare(out=tmp_path / "out", sources=src, sources_sha256=src_sha, **dict(base, env_identity=ident))
    assert order == ["identity", "sources", "sha", "paths"] and len(loads) == 1
    assert prep["required"] == run.REQUIRED_IDENTITY and len(set(run.REQUIRED_IDENTITY)) == 10
    assert all(prep["id_start"][rel]["expected"] == entries[rel] and prep["id_start"][rel]["sha256"] == entries[rel]["sha256"]
               for rel in MODS)
    assert prep["header"]["sources"]["sha256"] == src_sha and prep["header"]["sources"]["files"] == entries
    plan, rule, sup = _plan_rule_sup()
    out = prep["out"]
    r = run.finalize(out, plan=plan, sup=sup, rule=rule, ident_start=prep["id_start"],
                     rehash=lambda: run.identity_table(prep["files"], prep["expected"]), header=prep["header"], limits=dict(run.LIMITS),
                     roots=[out], clock=time.monotonic, t0=time.monotonic(), n_workers=4, required=prep["required"])
    assert r["pre"]["complete"] is True and r["final"]["complete"] is True
    assert r["pre"]["required_identity"] == list(run.REQUIRED_IDENTITY)
    rec = json.loads((out / "IDENTITY.json").read_text(encoding="utf-8"))
    assert all(rec["end"][rel]["expected"] == entries[rel] for rel in MODS) and rec["changed"] == []


def test_n1_b_missing_extra_or_malformed_entries_and_list_sha_mismatch_stop_before_util_import(tmp_path):
    """[RED 실패 — TypeError: 지금 prepare 에 sources 인자가 없다] 기대 항목 누락 (넷만) · 목록 밖 항목 · 형식 오류 (sha 63 자 · 대문자 · bytes 음수 ·
    schema 다름) · 목록 sha 불일치 · 목록 / sha 하나만 → 모두 E3aStop · util import 0 · 출력 폴더 없음. 수용 판정도 필수 행의 기대 누락 · 행 없음을
    INCOMPLETE 로 본다 (required 를 주지 않으면 예전 그대로)."""
    base, loads = _setup(tmp_path)
    entries = _real_entries()
    p7 = entries["scripts/reil_p0.py"]
    variants = {
        "missing": {k: v for k, v in entries.items() if k != "scripts/reil_c4_monitor.py"},
        "extra": dict(entries, **{"scripts/reil_c4_h.py": dict(p7)}),
        "short_sha": dict(entries, **{"scripts/reil_p0.py": {"sha256": p7["sha256"][:63], "bytes": p7["bytes"]}}),
        "upper_sha": dict(entries, **{"scripts/reil_p0.py": {"sha256": p7["sha256"].upper(), "bytes": p7["bytes"]}}),
        "negative_bytes": dict(entries, **{"scripts/reil_p0.py": {"sha256": p7["sha256"], "bytes": -1}}),
    }
    cases = [(name, *_write_sources(tmp_path / name, files)) for name, files in variants.items()]
    cases.append(("schema", *_write_sources(tmp_path / "schema", entries, schema="reil-c4e-sources-v0")))
    good_p, good_sha = _write_sources(tmp_path / "good", entries)
    cases.append(("list_sha", good_p, "0" * 64))
    for name, p, sha in cases:
        out = tmp_path / f"out_{name}"
        with pytest.raises(run.E3aStop):
            run.prepare(out=out, sources=p, sources_sha256=sha, **base)
        assert not out.exists(), name
    for half in ({"sources": good_p}, {"sources_sha256": good_sha}):
        with pytest.raises(run.E3aStop):
            run.prepare(out=tmp_path / "out_half", **half, **base)
    assert loads == [] and not (tmp_path / "out_half").exists()
    plan, rule, sup = _plan_rule_sup()
    agg = run.aggregate(sup, plan, rule)
    a = tmp_path / "a.bin"
    a.write_bytes(b"x")
    exp_a = {"a": {"sha256": hashlib.sha256(b"x").hexdigest(), "bytes": 1}}
    no_exp = run.identity_table({"a": a, "b": a}, exp_a)
    no_row = run.identity_table({"a": a}, exp_a)
    for t in (no_exp, no_row):
        pre = run.pre_verdict(plan, agg, sup, t, t, required=("a", "b"))
        assert pre["complete"] is False and any("b:" in r for r in pre["reasons"])
    assert run.identity_problems(no_exp) == [] and run.pre_verdict(plan, agg, sup, no_exp, no_exp)["complete"] is True


def test_n1_c_unapproved_bytes_that_stay_unchanged_from_start_to_end_are_refused(tmp_path):
    """[RED 실패 — TypeError: 지금 prepare 에 sources 인자가 없다] 목록의 한 모듈 기대값이 실제 바이트와 다르면 (시작부터 틀림 · 실행 중 변화 없음)
    prepare 가 util import · 자료 적재 전에 멈춘다 · 출력 폴더 없음 · 사유에 그 경로. 시작 표 = 끝 표여도 기대와 다르면 수용 판정 INCOMPLETE."""
    base, loads = _setup(tmp_path)
    entries = _real_entries()
    wrong = dict(entries, **{"scripts/reil_c4_e3a.py": {"sha256": hashlib.sha256(b"not the approved e3a bytes").hexdigest(),
                                                        "bytes": entries["scripts/reil_c4_e3a.py"]["bytes"]}})
    p, sha = _write_sources(tmp_path / "wrong", wrong)
    with pytest.raises(run.E3aStop) as ei:
        run.prepare(out=tmp_path / "out", sources=p, sources_sha256=sha, **base)
    assert "scripts/reil_c4_e3a.py" in str(ei.value) and loads == [] and not (tmp_path / "out").exists()
    m = tmp_path / "m.py"
    m.write_bytes(b"unapproved but unchanged")
    exp = {"m": {"sha256": hashlib.sha256(b"approved bytes").hexdigest(), "bytes": len(b"approved bytes")}}
    start, end = run.identity_table({"m": m}, exp), run.identity_table({"m": m}, exp)
    assert run.identity_changed(start, end) == []
    plan, rule, sup = _plan_rule_sup()
    pre = run.pre_verdict(plan, run.aggregate(sup, plan, rule), sup, start, end, required=("m",))
    assert pre["complete"] is False and any("m:" in r for r in pre["reasons"])
    fin = run.final_verdict(pre, {"record_state": "COMPLETE", "limit_violations": [], "problems": [], "final_snapshot_s": 1.0})
    assert fin["complete"] is False and fin["c4a_gate"] is False


def test_n1_d_a_module_changed_during_the_run_fails_acceptance_through_the_real_finalize(tmp_path):
    """[RED 실패 — TypeError: 지금 identity_problems 는 required 를 받지 않는다] 다섯 모듈 사본 (tmp) 의 목록 기대값으로 시작 표 → 끝 재해시 직전에
    사본 하나가 바뀜 → 같은 기대값으로 끝 표 → 실제 finalize: 사전 · 최종 INCOMPLETE (변화 · 끝 식별 문제) · IDENTITY.json 의 changed · 기록 파일 보존.
    바뀐 바이트를 기대값에 다시 올린 대조 (변화 없음) 는 COMPLETE."""
    copies = {}
    for rel in MODS:
        dst = tmp_path / "mods" / Path(rel).name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((BMS / rel).read_bytes())
        copies[rel] = dst

    def exp_of():
        return {rel: {"sha256": _sha_file(p), "bytes": p.stat().st_size} for rel, p in copies.items()}

    exp = exp_of()
    start = run.identity_table(copies, exp)
    assert run.identity_problems(start, MODS) == []
    plan, rule, sup = _plan_rule_sup()
    target = copies["scripts/reil_c4_monitor.py"]

    def rehash():
        target.write_bytes(target.read_bytes() + "\n# 실행 중 변경 (N1 대조)\n".encode("utf-8"))
        return run.identity_table(copies, exp)

    def fin(out, start_t, rehash_fn):
        out.mkdir()
        return run.finalize(out, plan=plan, sup=sup, rule=rule, ident_start=start_t, rehash=rehash_fn, header={"kind": "N1 대조 n1_d"},
                            limits=dict(run.LIMITS), roots=[out], clock=time.monotonic, t0=time.monotonic(), n_workers=4, required=MODS)

    out = tmp_path / "out"
    r = fin(out, start, rehash)
    assert r["pre"]["complete"] is False and r["final"]["complete"] is False and r["final_record"]["record_state"] == "COMPLETE"
    assert any("scripts/reil_c4_monitor.py" in x for x in r["pre"]["reasons"])
    rec = json.loads((out / "IDENTITY.json").read_text(encoding="utf-8"))
    assert rec["changed"] == ["scripts/reil_c4_monitor.py"] and sorted(p.name for p in out.iterdir()) == sorted(run.RECORD_FILES)
    exp2 = exp_of()
    start2 = run.identity_table(copies, exp2)
    r2 = fin(tmp_path / "out2", start2, lambda: run.identity_table(copies, exp2))
    assert r2["pre"]["complete"] is True and r2["final"]["complete"] is True


def test_n1_e_the_run_cli_requires_the_trusted_list_and_its_sha(capsys):
    """[RED 실패 — AttributeError: 지금 build_parser 가 없다] run 은 --sources · --sources-sha256 가 없으면 argparse 가 거부 (기본값 없음) · 둘 다 주면
    해석된다 · seal-sources 하위 명령이 있다 (해석만 — 실행 경로는 부르지 않는다)."""
    ap = run.build_parser()
    base = ["run", "--venv", "/v", "--seal", "s", "--seal-manifest-sha256", "h", "--xlsx", "x.xlsx", "--util", "u.py", "--out", "o",
            "--approval", "상태 문서 절"]
    for extra in ([], ["--sources", "S.json"], ["--sources-sha256", "0" * 64]):
        with pytest.raises(SystemExit):
            ap.parse_args(base + extra)
    a = ap.parse_args(base + ["--sources", "S.json", "--sources-sha256", "0" * 64])
    assert (a.cmd, a.sources, a.sources_sha256) == ("run", Path("S.json"), "0" * 64)
    assert ap.parse_args(["seal-sources", "--out", "x"]).cmd == "seal-sources"


def test_n1_f_seal_sources_writes_exactly_the_five_paths_and_round_trips(tmp_path):
    """[RED 실패 — AttributeError: 지금 seal_sources 가 없다] 새 폴더에 SOURCES.json 하나 · 경로 정확히 다섯 (= run.MODULE_RELPATHS = 시험의 목록) ·
    각 sha256 · bytes = 실제 파일 (시험이 따로 계산) · 이미 있는 폴더 거부 · load_sources 로 되읽으면 같다. plan-e 의 모듈 행은 여전히 기대 없음 —
    plan-e 의 identity_ok 를 모듈 출처 확인으로 넓히지 않는다."""
    out = tmp_path / "sources"
    r = run.seal_sources(out)
    assert [p.name for p in out.iterdir()] == ["SOURCES.json"] and r["sources_sha256"] == _sha_file(out / "SOURCES.json")
    doc = json.loads((out / "SOURCES.json").read_text(encoding="utf-8"))
    assert doc["schema"] == "reil-c4e-sources-v1" and doc["files"] == _real_entries() and run.MODULE_RELPATHS == MODS
    with pytest.raises(run.E3aStop):
        run.seal_sources(out)
    assert run.load_sources(out / "SOURCES.json", r["sources_sha256"]) == _real_entries()
    pe = tmp_path / "plan_e"
    run.plan_e(pe, venv="/v", seal=NEW_SEAL, manifest_sha256=NEW_SEAL_MANIFEST, env_identity=_fake_ident)
    table = json.loads((pe / "PLAN_E.json").read_text(encoding="utf-8"))["identity_table"]
    assert all(table[rel]["expected"] is None for rel in MODS)
