"""Codex R6 probe 를 **닫힌 트리에 맞게 고쳐** 다시 돌린다 — hook 이 빗나간 것을 닫힘으로 읽지 않으려고.

원본 probe 는 우리가 고친 자리에 hook 을 건다 (`Path.read_text` · `compare_states._unit_ok` ·
`load_full_cell(root, state, workbook=None)`). 고친 뒤에는 그 hook 이 **안 걸려서** 실패한다 — 그것은 "발견이 닫혔다" 가
아니라 "이 probe 로는 더 못 잰다" 이다. 그래서 hook 지점만 현행 코드에 맞추고 **판정은 뒤집어** 건다: 원본이 "섞인 것을
소비했다" 를 assert 했다면 여기서는 "섞인 것을 소비하지 않는다" 를 assert 한다. 나머지 fixture·입력·경쟁 순서는 원본 그대로다.

    python3 replay_codex_r6_adapted.py --target <bms-balancing> [--output <json>]

상태: `닫힘` = 고친 판정이 성립 · `열림` = 성립 안 함(발견이 남았다) — 둘 다 세부에 실측치를 남긴다.
"""
from __future__ import annotations
import argparse, contextlib, hashlib, importlib.util, io, json, os, pathlib, subprocess, sys, tempfile, traceback
from unittest.mock import patch

HERE = pathlib.Path(__file__).resolve().parent


def baseline_from_env(env=None):
    """`R6_OLD_OUT` → 과거 baseline 디렉터리. **없거나 빈 문자열이면 None** 이다 (Codex R7-05).

    전 판은 `Path(os.environ.get("R6_OLD_OUT", ""))` 였다 — 빈 문자열은 `Path("")` = `.` 이고 그 디렉터리는 늘
    존재하므로 **현재 트리를 과거 baseline 으로** 삼아 full 재생을 불렀다 (요청문에 적은 기본 호출이 5/6·rc 1).
    """
    env = os.environ if env is None else env
    raw = (env.get("R6_OLD_OUT") or "").strip()
    if not raw:
        return None
    p = pathlib.Path(raw).expanduser()
    return p.resolve() if p.is_dir() else None


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _guard(fn):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            detail = fn()
        return "닫힘", detail
    except BaseException:                                        # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return "열림", {"error": tb[-1][:400], "stdio": buf.getvalue()[-300:]}


# ── R6-01 · 독자가 소비하는 묶음 ────────────────────────────────────────────────────────
def a1_degeneracy_snapshot(ex, target, root, v, pv, reader):
    """원본 `snapshot_metadata_mix` 와 같은 순서 — hook 만 `Path.read_bytes` 로 (현행 독자가 쓰는 읽기)."""
    ex.fixture_repo(target, root)
    art = root / "out/degeneracy_100_Li.json"
    v.atomic_write_json(art, ex.deg("attempt-A", 1.0))
    ex.write_meta(target, root, art, "attempt-A", starts=4)
    assert pv.verify_unit(art)[0] is True
    original, switched = pathlib.Path.read_bytes, []

    def scheduled(p, *a, **k):
        data = original(p, *a, **k)
        if p == art and not switched:                            # A 의 bytes 가 독자 손에 들어간 직후 B/B 가 정상 게시
            switched.append(True)
            v.atomic_write_json(art, ex.deg("attempt-B", 20.0))
            ex.write_meta(target, root, art, "attempt-B", starts=24)
        return data

    with patch.object(pathlib.Path, "read_bytes", scheduled):
        loaded = reader.load_degeneracy(root / "out")
    disk = pv.verify_unit(art)
    assert switched and disk[0] is True, (switched, disk)        # 디스크는 B/B 로 온전하다
    e = loaded.get("100")
    if e is None:                                                # 미완으로 걸러낸 경우도 허용 (섞어 쓰지만 않으면 된다)
        first = {"consumed": None, "disk_unit": disk, "why": "읽은 bytes 와 meta 가 안 맞아 표에서 뺐다"}
    else:
        assert e["j"]["run_id"] == e["meta"]["run_id"], (e["j"]["run_id"], e["meta"]["run_id"])
        first = {"data_run_id": e["j"]["run_id"], "meta_run_id": e["meta"]["run_id"],
                 "value": e["j"]["best_modes_percent"]["LLI"], "disk_unit": disk}

    # ② 검증이 **끝난 뒤** 게시가 끼는 순서 — 묶음 검사는 A/A 로 통과하고, 그 뒤 다시 읽으면 B 를 소비하게 된다.
    #    ①의 순서만으로는 "검증 뒤 재읽기" 를 못 잰다 (검사가 먼저 깨져서 어차피 빠진다).
    root2 = root.parent / (root.name + "-after")
    root2.mkdir()
    ex.fixture_repo(target, root2)
    art2 = root2 / "out/degeneracy_100_Li.json"
    v.atomic_write_json(art2, ex.deg("attempt-A", 1.0))
    ex.write_meta(target, root2, art2, "attempt-A", starts=4)
    meta_path, published = str(art2) + ".meta.json", []
    original_text = pathlib.Path.read_text

    def after_meta(p, *a, **k):
        text = original_text(p, *a, **k)
        if str(p) == meta_path and not published:                # A 의 meta 까지 읽은 직후 B/B 가 정상 게시
            published.append(True)
            v.atomic_write_json(art2, ex.deg("attempt-B", 20.0))
            ex.write_meta(target, root2, art2, "attempt-B", starts=24)
        return text

    with patch.object(pathlib.Path, "read_text", after_meta):
        loaded2 = reader.load_degeneracy(root2 / "out")
    assert published, "meta 를 안 읽었다 — 이 순서를 못 쟀다"
    e2 = loaded2.get("100")
    assert e2 is not None, loaded2                               # A/A 는 온전했으니 표에 있어야 한다
    assert e2["j"]["run_id"] == "attempt-A" and e2["meta"]["run_id"] == "attempt-A", e2["meta"]["run_id"]
    assert e2["j"]["best_modes_percent"]["LLI"] == 1.0, e2["j"]["best_modes_percent"]
    return {"검증_중_게시": first,
            "검증_후_게시": {"data_run_id": e2["j"]["run_id"], "meta_run_id": e2["meta"]["run_id"],
                          "value": e2["j"]["best_modes_percent"]["LLI"], "disk_unit": pv.verify_unit(art2)}}


def a2_matrix_snapshot(ex, target, root, v, pv, reader):
    """원본 `matrix_after_verification` 과 같은 순서 — hook 을 현행 `_read_unit`(검증+읽기 한 자리) 로."""
    ex.fixture_repo(target, root)
    art = root / "out/matrix_100.csv"
    rows_a, rows_b = ex.mx("attempt-A", 1.0), ex.mx("attempt-B", 20.0)
    rows_b[1]["LLI_pct"] = 99.0                                  # B 의 폭을 다르게 (공통 오프셋이 아니라)
    v.atomic_write_csv(art, rows_a, list(rows_a[0]))
    ex.write_meta(target, root, art, "attempt-A")
    original, switched = reader._read_unit, []

    def scheduled(p, *a, **k):                                   # `_read_unit(f, excluded)` 로 늘었다 (Codex R7-01)
        out = original(p, *a, **k)
        if p == art and not switched:                            # A 를 검증·스냅샷한 직후 B 의 데이터만 먼저 게시
            switched.append(True)
            v.atomic_write_csv(art, rows_b, list(rows_b[0]))
        return out

    with patch.object(reader, "_read_unit", scheduled):
        loaded = reader.load_matrix_axis(root / "out")
    final = pv.verify_unit(art)
    assert switched and final[0] is False, (switched, final)     # 디스크는 B 데이터 + A meta = 미완
    e = loaded.get("100")
    assert e is not None and e["per"]["GITT"]["LLI"] == 3.0, e   # 검증한 A 만 소비 (B 의 79 가 아니다)
    return {"A_verified_span": 3.0, "consumed_span": e["per"]["GITT"]["LLI"],
            "consumed_run_id": e["run_id"], "unit_after_publication": final}


def a3_modern_without_meta(ex, target, root, v, pv, reader, shape):
    """원본 `missing_modern_metadata` 의 fixture 그대로 — 판정만 '받아들인다' → '미완으로 거절한다'."""
    ex.fixture_repo(target, root)
    dfile, mfile = root / "out/degeneracy_100_Li.json", root / "out/matrix_100.csv"
    v.atomic_write_json(dfile, ex.deg("fresh-production-attempt", 7.0))
    rows = ex.mx("fresh-production-attempt", 5.0)
    v.atomic_write_csv(mfile, rows, list(rows[0]))               # write_meta 전에 중단된 첫 게시
    dcheck, mcheck = pv.verify_unit(dfile), pv.verify_unit(mfile)
    assert dcheck[0] is False and mcheck[0] is False, (dcheck, mcheck)
    ds, ms = reader.load_degeneracy(root / "out"), reader.load_matrix_axis(root / "out")
    assert ds == {} and ms == {}, (ds, ms)
    try:
        shape.fitted_pair_info(root / "out", "100", "GITT", "Li")
        raise AssertionError("ne_shape 가 미완 산출을 소비했다")
    except RuntimeError as e:
        refused = str(e)[:160]
    # 대조: run_id 없는 **옛** 산출은 호환 경로로 그대로 읽힌다
    legacy = root / "out/degeneracy_200_Li.json"
    legacy.write_text(json.dumps({"best_modes_percent": {k: 1.0 for k in reader.MODES},
                                  **{f"{k}_percent": {"span": 1.0} for k in reader.MODES}}), encoding="utf-8")
    assert pv.verify_unit(legacy)[0] is None and "200" in reader.load_degeneracy(root / "out")
    return {"modern_json_check": dcheck, "modern_csv_check": mcheck, "readers_excluded": True,
            "ne_shape_refused": refused, "legacy_without_run_id_still_read": True}


def a4_half_cell_late_identity(cl, target):
    """원본 `shape_and_matrix` 의 마지막 절 — 반쪽전지를 늦게 해시하던 자리. matrix 에 meta 를 붙여 (현행 규약) 진행한다."""
    ns = cl.load("r6_adapted_ne_shape", target / "scripts/ne_shape.py")
    with tempfile.TemporaryDirectory(prefix="bms-r6-adapted-shape-") as temp:
        base = pathlib.Path(temp)
        data, blend = cl.shape_inputs(base)
        selected = base / "out/matrix_100.csv"
        # ⚠ Codex R11 P1-7 뒤: production reader 가 checker 와 **같은** validator 를 exact header 로 돌린다. 원본
        #   helper(`cl.matrix`)는 여섯 열짜리라 이제 그 검사에서 먼저 멈춘다 — 그것은 이 발견(늦은 해시)의 닫힘이
        #   아니라 "이 fixture 로는 더 못 잰다" 이다. 값(γ 0.16 / ref 0.15)은 그대로 두고 열만 온전하게 쓴다.
        _full_matrix(selected, .16)
        _sign(selected)                                          # 현행 규약: run_id 열이 있으면 meta 가 있어야 한다
        half = data / "data/half_cell/GITT/100.xlsx"
        half_A = cl.sha(half)
        real_load = ns.D.load_literature

        def finish_new_half_export(root, source, **kw):           # 문헌 배열을 읽은 뒤 반쪽전지 B 를 재-export
            arrays = real_load(root, source, **kw)
            cl.write_half(half, blend, .45, pe_offset=.02)
            return arrays

        # ⚠ R9-04 뒤 requested 명부는 파일 존재가 아니라 **선언**(`D.HALF_FILE[source] ∩ D.STATES`)에서 온다. 이 합성 소스는
        #   pristine·100 만 있으므로 선언을 그 둘로 명시한다 — 아니면 200·300_* 이 missing_input 이 되어 status partial(rc 3),
        #   산출은 `out/partial/` 에 가고 원본 helper(`cl.run_shape`: rc 0 + canonical 경로)의 전제가 깨진다 (hook 만의 적응).
        with patch.object(ns.D, "STATES", ["pristine", "100"]), \
                patch.object(ns.D, "load_literature", side_effect=finish_new_half_export):
            raced, raced_meta = cl.run_shape(ns, base, data)
        with patch.object(ns.D, "STATES", ["pristine", "100"]):
            normal_B, meta_B = cl.run_shape(ns, base, data)
        rec = raced_meta["consumed_inputs"]["100"]["half_cell"]
        pe_raced, pe_B = float(raced["pe_shape_max_mV"]), float(normal_B["pe_shape_max_mV"])
        assert pe_raced == 0. and pe_B == 20., (pe_raced, pe_B)   # 값은 A 로 계산됐다 (원본과 같은 관측)
        assert rec["sha256"] == half_A != cl.sha(half), (rec["sha256"][:12], half_A[:12])   # 서명도 A 여야 한다
        assert rec != meta_B["consumed_inputs"]["100"]["half_cell"]
        return {"A_value_PE_change_mV": pe_raced, "B_value_PE_change_mV": pe_B,
                "recorded_sha_is_A": True, "A_hash": half_A[:16], "disk_now": cl.sha(half)[:16]}


def a5_full_cell_build_signature(cl, target):
    """원본 `fullcell_build_signature` — mock 이 현행 `identity=` 를 받게만 고치고, 판정을 'A값이면 A서명' 으로."""
    import numpy as np, pandas as pd
    from bms_balancing import verify
    with tempfile.TemporaryDirectory(prefix="bms-r6-adapted-build-") as temp:
        data = pathlib.Path(temp)
        subprocess.run([sys.executable, str(target / "matlab/tests/gen_synth_xlsx.py"), str(data)],
                       check=True, capture_output=True, text=True)
        original = verify.build(data, "GITT", "200", "Li", w_dqdv=1., scale_seed=0)
        workbook = verify.D.full_cell_workbook(data)
        A_hash = cl.sha(workbook)
        real_load = verify.D.load_full_cell

        def finish_new_fullcell_export(root, state, workbook=None, **kw):
            arrays = real_load(root, state, workbook=workbook, **kw)
            frame = pd.read_excel(workbook, header=None)
            col = 2 * verify.D.FULL_COL[state] + 1
            frame.iloc[2:, col] = pd.to_numeric(frame.iloc[2:, col], errors="coerce") + .020
            tmp = workbook.with_name(workbook.stem + ".new.xlsx")
            frame.to_excel(tmp, header=False, index=False)
            os.replace(tmp, workbook)
            return arrays

        with patch.object(verify.D, "load_full_cell", side_effect=finish_new_fullcell_export):
            raced = verify.build(data, "GITT", "200", "Li", w_dqdv=1., scale_seed=0)
        normal_B = verify.build(data, "GITT", "200", "Li", w_dqdv=1., scale_seed=0)
        assert np.array_equal(raced.voltage, original.voltage)                  # 값은 A (원본과 같은 관측)
        assert raced.consumed_inputs["full_cell"]["sha256"] == A_hash != cl.sha(workbook)
        assert raced.inputs_sha == original.inputs_sha != normal_B.inputs_sha   # 서명도 A
        return {"raced_arrays_match_A": True, "recorded_full_cell_is_A": True,
                "A_hash": A_hash[:16], "disk_now": cl.sha(workbook)[:16],
                "inputs_sha_raced": raced.inputs_sha[:16], "inputs_sha_B": normal_B.inputs_sha[:16]}


def a6_inference_closure(target):
    """받은 `inference` 스크립트는 `degeneracy_300_0009_Li_v2.json` 이 **있어야** 돈다 (R6-04 로 archive 로 옮겼다).
    없는 이름은 건너뛰도록 **한 줄만** 고친 사본으로 돌려, §3-4 격자·U14 대조·문턱 표가 정본 이름에서도 그대로인지 본다."""
    src = (HERE / "harness_r6_final_inference_repros.py").read_text(encoding="utf-8")
    old = '    for filename in ("degeneracy_300_0009_Li_v2.json", "degeneracy_300_0009_Li.json"):'
    assert src.count(old) == 1
    new = (old + "\n"
           '        if not (root / "out" / filename).is_file():\n'
           "            continue                                  # 적응: `_vN` 은 out/archive/ 로 갔다 (Codex R6-04)")
    # 적응 ②: 이 스크립트는 **옛 리비전의 out/** 을 읽는다 → 정본 선택은 historical 규칙이다. `baseline_for` 의
    #   기본값이 current 로 바뀌어(Codex R7-04) 그대로 부르면 그 시절 정본(`_v2`)이 아니라 v1 을 짝지어 버린다.
    import re as _re
    src, n_calls = _re.subn(r"check\.baseline_for\((new_[a-z]), old\)",
                            r'check.baseline_for(\1, old, "historical")', src)
    assert n_calls == 3, n_calls
    # 적응 ③: Codex R11 P1-2 뒤 `only_source`·`only_wdqdv` 로 **좁힌** matrix 실행은 subset 이라 canonical 이 아니라
    #   `partial/` 에 게시된다. 이 probe 의 관측(대상·기준 축이 독립인가)은 그대로 두고 **읽는 자리만** 맞춘다 —
    #   자리를 안 맞추면 관측 전에 FileNotFoundError 로 죽어 "이 probe 로는 더 못 잰다" 가 된다.
    old_read = '            with out.open(encoding="utf-8") as stream:'
    assert src.count(old_read) == 1
    src = src.replace(old_read,
                      '            with verify.publish_target(out, "subset").open(encoding="utf-8") as stream:')
    baseline = baseline_from_env()
    with tempfile.TemporaryDirectory(prefix="r6-adapted-inference-") as tmp:
        copy = pathlib.Path(tmp) / "inference_adapted.py"
        copy.write_text(src.replace(old, new), encoding="utf-8")
        cmd = [sys.executable, str(copy), "--target", str(target)]
        if baseline is not None:
            cmd += ["--old", str(baseline)]
        else:
            cmd += ["--case", "derived"]                          # baseline 없이는 u14/table 을 못 돈다 → **부분**
        r = subprocess.run(cmd, capture_output=True, text=True)
        assert r.returncode == 0, (r.returncode, r.stderr.strip().splitlines()[-3:])
        keys = [l.split(" ", 1)[0] for l in r.stdout.splitlines() if l and not l.startswith(" ")]
        return {"rc": 0, "cases": keys, "baseline_used": baseline is not None, "partial": baseline is None,
                "note": ("두 줄 적응: 없는 `_vN` 이름은 건너뛴다 · 옛 리비전 baseline 은 historical 정책으로 짝짓는다"
                 if baseline is not None else
                         "한 줄 적응 + **부분 재생** — `R6_OLD_OUT=<bfc4623^ 의 out>` 이 없어 derived 만 돌렸다 "
                         "(full 6/6 이 아니다, Codex R7-05)")}


def _full_matrix(path, gamma, ref=.15, rid="synthetic-matrix"):
    """`schema.MATRIX_ROW` 를 전부 채운 한 행 (진짜 역할 receipt 포함) — 원본 `cl.matrix` 의 값과 같되 열이 온전하다."""
    import csv as _csv
    from bms_balancing import schema as _S
    ci = {"half_cell": {"path": "half.xlsx", "sha256": "1" * 64}, "full_cell": {"path": "full.xlsx", "sha256": "2" * 64},
          "literature": {"gr": {"path": "gr.xlsx", "sha256": "3" * 64}, "si": {"path": "si.csv", "sha256": "4" * 64}}}
    rci = {"half_cell": {"path": "pristine.xlsx", "sha256": "5" * 64}, "full_cell": ci["full_cell"],
           "literature": ci["literature"]}
    row = {k: "1.0" for k in _S.MATRIX_ROW}
    # 자체 리뷰 C05: matrix 도 모집단을 행에 봉인한다 (이 fixture 는 행이 곧 모집단이다)
    # ⚠ Codex R13 (열한 번째 fixture 감사): 1 행이 canonical 을 주장하던 것을 정직한 subset 으로, 감사는 실물로.
    from bms_balancing import schema as _S2
    row["combo_roster"] = json.dumps({"authority": len(_S2.canonical_combo_keys("100")), "requested": 1,
                                      "succeeded": 1, "missing_input": [], "failed": [], "absent": []})
    _audit = json.dumps({m: {"n": 50, "n_finite": 50, "n_inf": 0, "n_nan": 0, "n_exception": 0, "raw_lower_half_mean": 1.0, "scale": 1.0, "eps_rel": 1e-15, "equivalent_within_rel": True} for m in ("pocv", "dvdq", "dqdv")})
    row.update(half_cell="GITT", si="Li", w_dqdv="0", run_id=rid, bounds="-", ref_bounds="-",
               gamma_Si=str(gamma), ref_gamma_Si=str(ref), scale_audit_target=_audit, scale_audit_ref=_audit,
               consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(rci),
               inputs_sha=_S.inputs_digest(ci), ref_inputs_sha=_S.inputs_digest(rci))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".new")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = _csv.DictWriter(f, fieldnames=list(_S.MATRIX_ROW), lineterminator="\n")
        w.writeheader(); w.writerow({k: row[k] for k in _S.MATRIX_ROW})
    os.replace(tmp, path)


def _sign(path):
    """현행 규약의 최소 meta 사이드카 (run_id 열이 있는 산출은 meta 가 있어야 소비된다)."""
    import csv as _csv
    rid = next(iter({r.get("run_id") for r in _csv.DictReader(path.open(encoding="utf-8-sig"))} - {None, ""}), None)
    meta = {"run_id": rid, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "artifact": path.name,
            "env": {}, "started_utc": "", "git_commit_at_start": "", "git_state_changed_during_run": False}
    path.with_name(path.name + ".meta.json").write_text(json.dumps(meta), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=pathlib.Path, required=True)
    ap.add_argument("--output", type=pathlib.Path)
    a = ap.parse_args()
    target = a.target.resolve()
    sys.path.insert(0, str(target)); sys.path.insert(0, str(target / "scripts"))
    head = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
    ex = _load("r6_codex_exec", HERE / "harness_r6_final_execution_repros.py")
    cl = _load("r6_codex_claims", HERE / "harness_r6_final_claims_repros.py")
    from bms_balancing import verify as v                        # noqa: E402
    import provenance as pv                                      # noqa: E402
    reader = ex.load("r6_reader", target / "scripts/compare_states.py")
    shape = ex.load("r6_shape", target / "scripts/ne_shape.py")
    out = {"target_head": head, "probes": {}}
    with tempfile.TemporaryDirectory(prefix="r6-adapted-") as tmp:
        mk = lambda n: (pathlib.Path(tmp) / n, (pathlib.Path(tmp) / n).mkdir())[0]
        for name, fn in (
            ("R6-01a 독자는 자기가 검증한 묶음만 (degeneracy)", lambda: a1_degeneracy_snapshot(ex, target, mk("a1"), v, pv, reader)),
            ("R6-01b 검증 뒤 게시된 B 를 안 읽는다 (matrix)", lambda: a2_matrix_snapshot(ex, target, mk("a2"), v, pv, reader)),
            ("R6-02 현행 산출 + meta 없음 = 미완 거절", lambda: a3_modern_without_meta(ex, target, mk("a3"), v, pv, reader, shape)),
            ("R6-03a 반쪽전지: A값이면 A서명", lambda: a4_half_cell_late_identity(cl, target)),
            ("R6-03b 풀셀 build: A값이면 A서명", lambda: a5_full_cell_build_signature(cl, target)),
            ("R6-04 inference 닫힘 확인(정본 이름으로)", lambda: a6_inference_closure(target)),
        ):
            st, detail = _guard(fn)
            if st == "닫힘" and isinstance(detail, dict) and detail.get("partial"):
                st = "부분"                                       # full 재생과 구분한다 (Codex R7-05)
            out["probes"][name] = {"상태": st, "세부": detail}
    out["baseline"] = str(baseline_from_env() or "") or None
    out["mode"] = "full" if all(p["상태"] == "닫힘" for p in out["probes"].values()) else (
        "부분 (R6_OLD_OUT 미지정 — `R6_OLD_OUT=<bfc4623^ 의 out>` 을 주면 full)"
        if all(p["상태"] in ("닫힘", "부분") for p in out["probes"].values()) else "실패")
    text = json.dumps(out, ensure_ascii=False, indent=2)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    return 0 if out["mode"] != "실패" else 1


if __name__ == "__main__":
    sys.exit(main())
