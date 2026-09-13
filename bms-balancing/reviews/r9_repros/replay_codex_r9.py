"""R9 패키지 probe 의 **닫힘 재생기** — 보관한 원본 probe(`codex/`) 는 SHA(29ef505) 를 고정해 두어 현재 트리에서는 `main`
이 rc 1 이다. 이 러너는 원본 probe **함수**를 직접 불러(pin 우회) R7 러너와 같은 세 가지를 기록한다:

  · 도달   — 대상 검증·fixture 를 지나 실제 반례 case 에 닿았는가 (probe 별 반례 assertion 줄로 판정)
  · 상태   — `재현`(반례가 아직 있다) · `반례 소멸`(자기 반례 assertion 에서 멈췄다 / positive closure 가 섰다) · `오류`
  · 멈춘_곳 — 실패한 소스 줄 (있으면)

원본 probe 가 **옛 게시 위치**(partial 이 canonical 을 덮던 시절)나 **옛 러너 출력**(거부 대신 빈 JSON)을 전제해 반례
assertion 앞에서 죽는 것(R9-04 · P2-1 · P2-5)은 hook 만 현행 계약(`<write>/partial/`, 거부 rc 2)으로 옮긴 **적응** probe 로
positive closure 를 잰다 (`적응` 필드 True). 원본 파일은 건드리지 않는다. P2-4·P2-5 는 패키지에 probe 가 없어 회귀
테스트(`tests/test_r9_codex.py::test_d9_10`·`::test_d9_11`)에 위임하고 그 결과를 기록한다.

Codex R9 P2-1·2 의 계약을 그대로 적용한다: `--expected-head` 필수(불일치면 돌지 않는다), dirty 트리는 기본 거부
(`--allow-dirty` 는 목록을 기록), 패키지 bytes 는 `HARNESS_R9_29EF5058_SHA256SUMS.txt` 와 대조, `--probes` 는 빈/오타/
중복을 거부하고 출력 key == 요청 집합. 종료 코드는 재현·오류·mismatch·digest 불일치 중 하나라도 있으면 0 이 아니다.

    python3 reviews/r9_repros/replay_codex_r9.py --target <bms-balancing> --expected-head <sha> [--probes R9-01,…] [--output x.json]
"""
from __future__ import annotations

# ⚠ Codex R13 P1-4: 재실행은 **어떤 앱 의존성 import 보다 앞**이다. 전 판은 아래 `import argparse, …`
#   가 먼저 돌았고 `sys.path[0]` 이 저장소 안이라 untracked 모듈 하나가 봉인 앞에서 실행될 수 있었다
#   (C08 의 남은 절반). `os`·`sys` 는 인터프리터 시작 때 이미 로드돼 sys.path 로 가로챌 수 없다.
import os
import sys

if globals().get("__name__") == "__main__" and not sys.flags.safe_path:
    # ⚠ `-E` 는 `PYTHONOPTIMIZE` 도 무시한다 — 그냥 재실행하면 R10 P2-4 의 "`-O` 에서는 증거를 만들지 않는다" 가
    #   **조용히 사라진다** (거부도 준수도 아닌 정규화). 재실행 **전에** 그 요청을 보고 거부한다.
    if sys.flags.optimize or os.environ.get("PYTHONOPTIMIZE"):
        print("! 이 러너는 `python -O`(PYTHONOPTIMIZE) 에서 증거를 만들지 않는다 — 보관한 probe 의 반례는 "
              "`assert` 로 쓰여 있고 optimize 모드는 그것을 통째로 지운다 (Codex R10 P2-4)", file=sys.stderr)
        raise SystemExit(2)
    os.environ.pop("PYTHONPATH", None)
    os.execv(sys.executable, [sys.executable, "-P", "-E", "-B", os.path.abspath(__file__), *sys.argv[1:]])

import argparse, contextlib, csv, hashlib, importlib.util, io, json, os, pathlib, shutil, subprocess, sys, tempfile, traceback

# ⚠ Codex R11 P1-10 반례 A: gate 를 **import 하기 전에** bytecode 캐시를 돌린다. 전 판은 gate 안에서
#   `isolate_bytecode()` 를 불렀는데, 그때는 이미 ignored `reviews/__pycache__/evidence_gate…pyc` (timestamp·size 를
#   맞춘 위조본)가 load 된 뒤였다 — 봉인 함수 자체가 위조본이었고 결과는 eligible true 였다.
#
# ⚠ 자체 리뷰 C08: 그것은 **bytecode 만** 막았다. 그보다 먼저 위의 `import argparse, …, traceback` 이 돌고
#   `sys.path[0]` 은 이 러너가 든 **저장소 안 디렉터리**다 — untracked `traceback.py` 하나면 gate 보다 먼저 실행되고
#   `INSTRUMENT` 밖이라 봉인에 안 걸린다. shim 이 gate 를 `sys.modules` 에 선주입하면 tracked 러너가 수정된
#   채로도 `dirty_paths: []` · `instrument: ok` · eligible true 가 나왔다 (실측). 봉인을 import 보다 앞에 두는
#   방법은 하나뿐이다 — `-P`(sys.path[0] 삽입 끔) · `-E`(PYTHON* 환경변수 무시)로 **한 번 재실행**한다.
# ⚠ 재실행은 **스크립트로 직접 돌 때만** 한다. 회귀(`test_e11_11`·`test_e11_12`)는 이 파일을 `exec` 해서
#   `child_ok`·`_classify` 를 직접 부르는데, module level 에서 `execv` 하면 **그 테스트 프로세스가 갈아치워진다**
#   (실측: pytest 가 26 번째 항목에서 조용히 죽었다).

_PYC = tempfile.mkdtemp(prefix="evidence-pycache-")
sys.pycache_prefix = _PYC
os.environ["PYTHONPYCACHEPREFIX"] = _PYC
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import evidence_gate as gate                                              # noqa: E402  — 증거 gate 는 한 자리 (R10 P2-4·P2-5)
HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE / "codex"
PINNED = "29ef5058e68c0c64dba840ecc5a7495644cb092e"
PKG_REL = "reviews/r9_repros/codex"
SUMS_NAME = "HARNESS_R9_29EF5058_SHA256SUMS.txt"
SUMS = PKG / SUMS_NAME
#: 증거를 만드는 **도구** — 이 파일들이 expected commit 과 같아야 그 증거가 그 커밋의 것이다 (Codex R10 P2-5)
INSTRUMENT = ("reviews/r9_repros/replay_codex_r9.py", "reviews/evidence_gate.py")
KNOWN_PROBES = ("R9-01", "R9-02", "R9-03", "R9-04", "R9-05", "R9-06", "R9-07", "P2-1", "P2-2", "P2-3", "P2-4", "P2-5")

# 원본 probe 의 "반례 assertion" 조각 — 이 줄에서 멈추면 case 에 **도달**한 것이다
COUNTEREXAMPLE_LINES = {
    "R9-01": ("assert missing_first.returncode == 0",),
    "R9-03": ('assert checked.returncode == 0 and "전부 갖췄다" in checked.stdout',),
    "R9-06": ('assert rc2 == 3 and meta2["pairing"]["missing"] == ["200"]',),
}


def parse_probes(text):
    return gate.parse_probes(text, KNOWN_PROBES)


def package_digest():
    return gate.package_digest(PKG, SUMS)


def dirty_paths(target):
    return gate.dirty_paths(target)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _run_probe(pid, fn):
    """원본 probe: 자기 반례 assertion 에서 멈추면 반례 소멸, 끝까지 가면 재현, 다른 곳에서 죽으면 오류."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            detail = fn()
        return {"도달": True, "상태": "재현", "멈춘_곳": None, "세부": str(detail)[:400]}
    except AssertionError:
        tb = traceback.extract_tb(sys.exc_info()[2])
        frames = [f for f in tb if str(PKG) in (f.filename or "")]
        line = (frames[-1].line or "").strip() if frames else ""
        reached = any(sn in line for sn in COUNTEREXAMPLE_LINES.get(pid, ()))
        return {"도달": reached, "상태": "반례 소멸" if reached else "오류",
                "멈춘_곳": f"{pathlib.Path(frames[-1].filename).name}:{frames[-1].lineno}: {line}" if frames else "?",
                "세부": ("자기 반례 assertion 에서 멈췄다" if reached else "반례 case 전에 assertion 이 깨졌다 — 원본 probe 의 전제가 현행 트리와 다르다")}
    except BaseException:                                              # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return {"도달": False, "상태": "오류", "멈춘_곳": tb[-1][:300], "세부": "도달 전에 예외"}


def _run_adapted(fn):
    """적응 probe: positive-closure assert 가 **서면** 반례 소멸, 깨지면 재현, 그 밖의 예외는 오류."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            d = fn()
        return {"도달": True, "상태": "반례 소멸", "멈춘_곳": d.pop("closure_assert", None), "세부": d}
    except AssertionError as e:
        return {"도달": True, "상태": "재현", "멈춘_곳": "positive-closure assert 가 깨졌다", "세부": str(e)[:600]}
    except BaseException:                                              # noqa: BLE001
        tb = traceback.format_exc().strip().splitlines()
        return {"도달": False, "상태": "오류", "멈춘_곳": tb[-1][:300], "세부": "도달 전에 예외"}


def _workspace(target: pathlib.Path) -> pathlib.Path:
    """aggregation·provenance 스크립트는 `<ws>/work/harness-r9-target-wsl/bms-balancing` 을 하드코딩한다 — symlink 로 맞춘다."""
    ws = pathlib.Path(tempfile.mkdtemp(prefix="r9-closure-ws-"))
    (ws / "work" / "harness-r9-target-wsl").mkdir(parents=True)
    (ws / "work" / "harness-r9-target-wsl" / "bms-balancing").symlink_to(target)
    (ws / "outputs").mkdir()
    for name in ("r9_aggregation_repros.py", "r9_provenance_repro.py"):
        shutil.copy(PKG / name, ws / "outputs" / name)
    return ws


# ── 적응 probe (hook 만 현행 계약으로) ──────────────────────────────────────────────────────
def _shape_partial_run(ns, mp, matrix, out):
    old_argv = sys.argv
    buf = io.StringIO()
    try:
        mp.setattr(sys, "argv", ["ne_shape.py", "--out-dir", str(matrix), "--write", str(out)])
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = ns.main()
    finally:
        sys.argv = old_argv
    canon = out / "ne_shape_GITT_Li.csv"
    art = canon if canon.is_file() else out / "partial" / "ne_shape_GITT_Li.csv"
    meta = json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8")) if art.is_file() else None
    return rc, buf.getvalue(), canon, art, meta


def r9_04_adapted(_shape_harness, _pair):
    """R9-04: 원본은 canonical CSV 를 읽다 죽는다(partial 은 이제 `<write>/partial/`). 같은 fixture 로 requested/missing_input 을 본다."""
    import pytest
    with tempfile.TemporaryDirectory(prefix="r9-adapt-roster-") as td:
        base = pathlib.Path(td); matrix = base / "matrix"; out = base / "shape"; matrix.mkdir()
        mp = pytest.MonkeyPatch()
        try:
            ns = _shape_harness(mp, base, {"pristine": 0.0, "100": 0.01, "200": 0.10})
            class P:
                def __init__(self, state): self.state = state
                def is_file(self): return self.state != "200"
            mp.setattr(ns.D, "half_cell_path", lambda root, src, state: P(state))
            mp.setattr(ns.D, "HALF_FILE", {"GITT": {"pristine": "p", "100": "a", "200": "b"}})
            _pair(matrix, "100")
            rc, text, canon, art, meta = _shape_partial_run(ns, mp, matrix, out)
            pr = (meta or {}).get("pairing", {})
            closure = 'assert rc == 3 and not canon.exists() and pr["requested"] == ["100","200"] and pr["missing_input"] == ["200"] and pr["paired"] == ["100"]'
            gate.need(rc == 3 and not canon.exists() and pr.get("requested") == ["100", "200"]
                      and pr.get("missing_input") == ["200"] and pr.get("paired") == ["100"],
                      "R9-04 닫힘 조건이 서지 않는다", (rc, canon.exists(), pr))
            return {"rc": rc, "status": meta.get("status"), "pairing": {k: pr.get(k) for k in ("requested", "available", "missing_input", "paired", "missing")},
                    "artifact": str(art.relative_to(base)), "closure_assert": closure}
        finally:
            mp.undo()


def _full_fields():
    from bms_balancing import schema as _S
    return list(_S.MATRIX_ROW)


def _full_row(agg, rid, gamma):
    """`schema.MATRIX_ROW` 를 전부 채운 행 — 원본 helper 의 값(역할 receipt 포함)을 그 위에 얹는다."""
    from bms_balancing import schema as _S
    ci = {"half_cell": {"path": "half.xlsx", "sha256": "1" * 64}, "full_cell": {"path": "full.xlsx", "sha256": "2" * 64},
          "literature": {"gr": {"path": "gr.xlsx", "sha256": "3" * 64}, "si": {"path": "si.csv", "sha256": "4" * 64}}}
    rci = {"half_cell": {"path": "pristine.xlsx", "sha256": "5" * 64}, "full_cell": ci["full_cell"],
           "literature": ci["literature"]}
    row = {k: "1.0" for k in _S.MATRIX_ROW}
    # 자체 리뷰 C05: matrix 도 모집단을 행에 봉인한다 (이 fixture 는 행이 곧 모집단이다)
    row["combo_roster"] = json.dumps({"authority": 1, "requested": 1, "succeeded": 1,
                                      "missing_input": [], "failed": [], "absent": []})
    row.update(half_cell="GITT", si="Li", w_dqdv="0", run_id=rid, bounds="-", ref_bounds="-",
               gamma_Si=gamma, ref_gamma_Si="0.2", scale_audit_target="{}", scale_audit_ref="{}",
               consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(rci),
               inputs_sha=_S.inputs_digest(ci), ref_inputs_sha=_S.inputs_digest(rci))
    return {k: row[k] for k in _S.MATRIX_ROW}


def r9_05_adapted(agg, _shape_harness, _pair):
    """R9-05: 원본 `run_shape` 는 `ns.main()` 이 예외를 올리면 그대로 전파한다 — 중복 key 두 순서 모두 RuntimeError(중복) 여야 한다."""
    results = {}
    for order in ("forward", "reversed"):
        with tempfile.TemporaryDirectory(prefix="r9-adapt-dup-") as td:
            base = pathlib.Path(td); matrix = base / "matrix"; matrix.mkdir()
            # ⚠ Codex R11 P1-7 뒤: reader 가 checker 와 **같은** validator 를 exact header 로 돌린다. 원본 helper
            #   (`agg.matrix_row`)는 열의 부분집합이라 중복 판정에 닿기 전에 스키마에서 멈춘다 — 그것은 이 발견의
            #   닫힘이 아니라 "이 fixture 로는 더 못 잰다" 이다. 중복 key(γ 0.10 ↔ 0.40)는 그대로, 열만 온전히 쓴다.
            rows = [_full_row(agg, "shape-dup", "0.10"), _full_row(agg, "shape-dup", "0.40")]
            combo = json.dumps({"authority": 2, "requested": 2, "succeeded": 2,
                                "missing_input": [], "failed": [], "absent": []})
            rows = [dict(r, combo_roster=combo) for r in rows]     # 행 수와 맞춘다 (자체 리뷰 C05)
            if order == "reversed":
                rows = list(reversed(rows))
            agg.write_csv_unit(matrix / "matrix_100.csv", _full_fields(), rows, "shape-dup")
            ns = agg.load_ne_shape()
            # ⚠ 자체 리뷰 C17 뒤: reader 의 거부가 `main()` 에서 잡혀 그 상태의 **짝 없음**으로 기록된다
            #   (예외가 밖으로 나가면 산출에 이유가 안 남고 wrapper 메시지가 원인을 안 가렸다). 그래서 이
            #   probe 는 wrapper 대신 **reader 자체**를 부른다 — 재는 축(중복 key 를 소비하는가)은 그대로다.
            try:
                got = ns.fitted_pair_info(matrix, "100", "GITT", "Li")
                results[order] = f"소비했다 (예외 없음): {got}"
            except RuntimeError as e:
                results[order] = f"RuntimeError: {str(e)[:120]}"
    closure = 'assert all("중복" in v for v in results.values())'
    gate.need(all("중복" in v for v in results.values()), "중복 key 를 거부하지 않는다", results)
    return {"orders": results, "closure_assert": closure}


def p2_5_adapted(_shape_harness):
    """P2-5: 짝 0 은 rc 1 + typed status none, `<write>/partial/` 에만 (canonical 없음)."""
    import pytest
    with tempfile.TemporaryDirectory(prefix="r9-adapt-none-") as td:
        base = pathlib.Path(td); matrix = base / "matrix"; out = base / "shape"; matrix.mkdir()
        mp = pytest.MonkeyPatch()
        try:
            ns = _shape_harness(mp, base, {"pristine": 0.0, "100": 0.01})
            rc, text, canon, art, meta = _shape_partial_run(ns, mp, matrix, out)
            closure = 'assert rc == 1 and not canon.exists() and meta["status"] == "none" and meta["pairing"]["paired"] == []'
            gate.need(rc == 1 and not canon.exists() and (meta or {}).get("status") == "none"
                      and meta["pairing"]["paired"] == [], "zero-pair 가 typed none 이 아니다", (rc, meta))
            return {"rc": rc, "status": meta["status"], "closure_assert": closure}
        finally:
            mp.undo()


def p2_1_adapted(target, head):
    """P2-1: `--probes DOES_NOT_EXIST` / 빈 / 중복 / valid+unknown 은 거부 rc 2, JSON 을 내지 않는다."""
    runner = target / "reviews" / "r7_repros" / "replay_codex_r7.py"
    out = {}
    for bad in ("DOES_NOT_EXIST", "", "R7-01,R7-01", "R7-01,NOPE"):
        p = subprocess.run([sys.executable, str(runner), "--target", str(target), "--probes", bad, "--expected-head", head,
                            "--allow-dirty"], cwd=target, capture_output=True, text=True, timeout=180)
        out[bad or "<빈>"] = {"rc": p.returncode, "stdout_json": p.stdout.strip().startswith("{"), "stderr": p.stderr.strip()[-160:]}
    closure = 'assert all(v["rc"] != 0 and not v["stdout_json"] for v in out.values())'
    gate.need(all(v["rc"] != 0 and not v["stdout_json"] for v in out.values()), "probe 이름 거부가 서지 않는다", out)
    return {"cases": out, "closure_assert": closure}


def p2_2_adapted(target, head):
    """P2-2: expected-head 없음 / 불일치 / dirty(허용 없이) 는 돌지 않는다; 패키지 digest 를 결과에 적는다."""
    runner = target / "reviews" / "r7_repros" / "replay_codex_r7.py"
    def run(*extra):
        p = subprocess.run([sys.executable, str(runner), "--target", str(target), "--probes", "R7-06", *extra],
                           cwd=target, capture_output=True, text=True, timeout=180)
        return p.returncode, (p.stdout + p.stderr)
    no_head = run()
    wrong = run("--expected-head", "0" * 40)
    out = {"no_expected_head": {"rc": no_head[0], "msg": no_head[1].strip()[-140:]},
           "wrong_head": {"rc": wrong[0], "msg": wrong[1].strip()[-160:]}}
    if dirty_paths(target):
        strict = run("--expected-head", head)
        out["dirty_without_allow"] = {"rc": strict[0], "msg": strict[1].strip()[:160], "names_dirty": "dirty" in strict[1]}
    src = (target / "reviews" / "r7_repros" / "replay_codex_r7.py").read_text(encoding="utf-8")
    out["records_package_digest"] = "package_digest_ok" in src and "SHA256SUMS" in src
    closure = 'assert no_head rc != 0 and "expected-head" in msg; wrong rc != 0 and "mismatch" in msg; dirty rc != 0 (if dirty); digest recorded'
    gate.need(out["no_expected_head"]["rc"] != 0 and "expected-head" in no_head[1], "expected-head 가 필수가 아니다", out)
    gate.need(out["wrong_head"]["rc"] != 0 and "mismatch" in wrong[1], "SHA 불일치를 거부하지 않는다", out)
    gate.need(all(v["rc"] != 0 and v["names_dirty"] for k, v in out.items() if k == "dirty_without_allow"),
              "dirty 트리를 기본에서 거부하지 않는다", out)
    gate.need(out["records_package_digest"], "패키지 digest 를 기록하지 않는다", out)
    return {**out, "closure_assert": closure}


def p2_3_adapted(target):
    """P2-3: 같은 `1 failed` summary 에 rc 2·3·4·5 는 오류, rc 1 만 CAUGHT."""
    audit = _load("r9_closure_audit", target / "reviews" / "r6_repros" / "codex_r6_mutation_audit.py")
    s = "1 failed, 51 deselected in 1.4s"
    got = {rc: audit.classify(rc, s) for rc in (1, 2, 3, 4, 5)}
    got["0 passed-summary"] = audit.classify(0, "1 passed, 51 deselected in 1.4s")
    closure = 'assert got == {1: "CAUGHT", 2: "오류", 3: "오류", 4: "오류", 5: "오류", "0 passed-summary": "MISSED"}'
    gate.need(got == {1: "CAUGHT", 2: "오류", 3: "오류", 4: "오류", 5: "오류", "0 passed-summary": "MISSED"},
              "rc 분류가 계약과 다르다", got)
    return {"classify": {str(k): v for k, v in got.items()}, "closure_assert": closure}


def delegated(target, node):
    """패키지에 probe 가 없는 항목 — 회귀 테스트 노드에 위임하고 결과를 그대로 기록한다."""
    p = subprocess.run([sys.executable, "-m", "pytest", node, "-q", "--no-header", "-p", "no:cacheprovider"],
                       cwd=target, capture_output=True, text=True, timeout=600)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:]
    closure = f"pytest {node} → rc 0 · '1 passed'"
    # ⚠ Codex R10 P2-4: 위임한 pytest 의 **rc 를 값으로** 최종 술어에 묶는다 (전 판은 assert 라 `-O` 에서 사라졌고
    #   usage error 가 "반례 소멸" 로 인증됐다).
    passed = p.returncode == 0 and "1 passed" in last
    gate.need(passed, f"위임한 회귀가 통과하지 않았다 ({node})", (p.returncode, last))
    return {"node": node, "summary": last, "rc": p.returncode, "passed": passed, "closure_assert": closure}


def r9_02_03_agg(agg, target):
    """aggregation 패키지의 U18 case 를 helper 그대로 다시 만든다 — 이제 전부 rc ≠ 0 이어야 한다."""
    u14 = str(target / "scripts" / "check_u14.py")
    cases = {}
    root = pathlib.Path(tempfile.mkdtemp(prefix="r9-adapt-u18-"))
    old, new = root / "roster" / "old", root / "roster" / "new"
    agg.write_json_unit(old / "degeneracy_100_Li.json", "old-100", "100")
    agg.write_json_unit(old / "degeneracy_200_Li.json", "old-200", "200")
    agg.write_json_unit(new / "degeneracy_100_Li.json", "new-100", "100")
    r = agg.run_cli(u14, "--new", str(new), "--old", str(old)); cases["u14_missing_new_artifact"] = (r["rc"], "명부(roster)" in r["stdout"] and "degeneracy_200_Li.json" in r["stdout"])
    old, new = root / "drop" / "old", root / "drop" / "new"
    old_row, new_row = agg.matrix_row("old-drop"), agg.matrix_row("new-drop")
    agg.write_csv_unit(old / "matrix_100.csv", agg.MATRIX_FIELDS, [old_row], "old-drop")
    new_row.pop("LLI_pct")
    agg.write_csv_unit(new / "matrix_100.csv", [x for x in agg.MATRIX_FIELDS if x != "LLI_pct"], [new_row], "new-drop")
    r = agg.run_cli(u14, "--new", str(new), "--old", str(old), "--max-show", "200")     # 패키지 행은 열 부분집합이라 누락 목록이 길다
    cases["u14_dropped_numeric_column"] = (r["rc"], "LLI_pct" in r["stdout"])
    old, new = root / "blank" / "old", root / "blank" / "new"
    for d, rid in ((old, "old-blank"), (new, "new-blank")):
        row = agg.matrix_row(rid, provenance=""); row["ref_inputs_sha"] = ""
        agg.write_csv_unit(d / "matrix_100.csv", agg.MATRIX_FIELDS, [row], rid)
    r = agg.run_cli(u14, "--new", str(new), "--old", str(old)); cases["u14_blank_provenance"] = (r["rc"], "비어 있다" in r["stdout"])
    old, new = root / "dup" / "old", root / "dup" / "new"
    agg.write_csv_unit(old / "matrix_100.csv", agg.MATRIX_FIELDS, [agg.matrix_row("old-dup")], "old-dup")
    agg.write_csv_unit(new / "matrix_100.csv", agg.MATRIX_FIELDS,
                       [agg.matrix_row("new-dup", gamma="0.10", lli="1.0"), agg.matrix_row("new-dup", gamma="0.40", lli="8.0")], "new-dup")
    r = agg.run_cli(u14, "--new", str(new), "--schema-only"); cases["u14_duplicate_schema_only"] = (r["rc"], "중복" in r["stdout"])
    shutil.rmtree(root, ignore_errors=True)
    closure = "assert all(rc != 0 and msg for rc, msg in cases.values())"
    gate.need(all(rc != 0 and msg for rc, msg in cases.values()), "U18 gate 가 아직 통과시킨다", cases)
    return {"cases": {k: {"rc": v[0], "names_the_defect": v[1]} for k, v in cases.items()}, "closure_assert": closure}


def r9_07_prov(provm):
    """R9-07: 패키지의 race 함수 그대로 — 이제 경로를 한 번 읽고 A 로 판정(invalid)해야 한다."""
    d = provm.eval_verified_bytes_race()
    closure = 'assert d["read_count"] == 1 and d["raced_status"] == "invalid" and d["control_same_malformed_bytes"] == "invalid"'
    gate.need(d["read_count"] == 1 and d["raced_status"] == "invalid"
              and d["control_same_malformed_bytes"] == "invalid", "dd_eval 이 아직 경로를 다시 읽는다", d)
    return {**{k: v for k, v in d.items() if k != "read_sha256"}, "closure_assert": closure}


def u18_prov(provm):
    """R9-02·03 (provenance 패키지의 U18 gate): 1/12 · 빈 receipt · 조건 변경이 전부 rc ≠ 0 이어야 한다."""
    d = provm.u18_roster_and_receipt()
    got = {k: d[k]["returncode"] for k in ("one_of_twelve", "blank_receipts", "config_mismatch") if k in d}
    closure = 'assert all(rc != 0 for rc in got.values())'
    gate.need(bool(got) and all(rc != 0 for rc in got.values()), "U18 gate 세 case 가 아직 rc 0 이다", got)
    return {"rc": got, "current_out_schema_rc": d.get("current_out_schema", {}).get("returncode"), "closure_assert": closure}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=pathlib.Path, required=True)
    ap.add_argument("--probes", default=",".join(KNOWN_PROBES))
    ap.add_argument("--expected-head", required=True, metavar="SHA")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="격리 snapshot 을 만들지 않고 **현재 working tree 에서** 돌린다 (개발용). 그 결과는 "
                         "`evidence_eligible: false` 로 표시되고 증거로 세지 않는다 (Codex R10 Q4)")
    ap.add_argument("--keep-materialized", type=pathlib.Path, default=None, metavar="DIR",
                    help="격리 snapshot 을 지우지 않고 이 자리에 남긴다 (회귀가 들여다본다)")
    ap.add_argument("--output", type=pathlib.Path)
    a = ap.parse_args()
    try:
        gate.require_assertions()                       # Codex R10 P2-4: `-O` 에서는 증거를 만들지 않는다
        target = a.target.resolve()
        want, problems = parse_probes(a.probes)
        if problems:
            print("! --probes 거부: " + "; ".join(problems) + " — 아무것도 돌리지 않았다 (Codex R9 P2-1)", file=sys.stderr)
            return 2
        head = gate.git_head(target)                    # Codex R10 P2-5: git 의 rc 를 본다
        # ⚠ Codex R11 P2-6: full 40 자 object id 만 받는다 (prefix 는 커밋 하나를 지목하지 못한다)
        exp = gate.full_head(target, a.expected_head)
        if head != exp:
            print(f"! HEAD mismatch — expected {exp}, 실제 {head} (다르다) — 돌리지 않았다 (Codex R9 P2-2)",
                  file=sys.stderr)
            return 2
        tree = gate.tree_of(target, head)
        dirty = gate.dirty_paths(target)
        skipped = gate.index_skip_flags(target)
        if skipped:
            print(f"! index 에 skip flag(assume-unchanged/skip-worktree)가 걸린 tracked 파일이 있다 — 그 bytes 는 "
                  f"status 에 안 잡힌다: {skipped[:10]} (Codex R10 P2-5)", file=sys.stderr)
            return 2
        gate.isolate_bytecode()                         # 이미 놓인 __pycache__ 를 읽지 않는다 (P2-5 반례 C)
        sealed, seal_detail = gate.instrument_sealed(target, INSTRUMENT)
        snapshot = None
        if not a.allow_dirty:
            # ⚠ Codex R10 P2-5: **대상 bytes 를 expected commit 에서 새로 materialize** 한다. working tree 를 그대로
            #   쓰면 `assume-unchanged` 로 고친 module 도 ignored `__pycache__` 의 위조 bytecode 도 clean 으로 보이면서
            #   실행됐다. 아래부터 probe·패키지·production 코드는 전부 이 snapshot 것이다.
            snapshot, cleanup = gate.materialize(target, head, keep=a.keep_materialized)
            # ⚠ Codex R11 P1-10 반례 B: checkout 은 filter(smudge)·eol 을 거친다 — 풀린 bytes 를 blob 과 다시 댄다
            drift = gate.verify_snapshot_bytes(snapshot, head)
            if drift:
                raise gate.EvidenceError("snapshot 의 bytes 가 expected commit 의 blob 과 다르다 "
                                         f"(checkout filter/smudge?): {drift[:5]}")
            target = snapshot
            globals()["PKG"] = snapshot / PKG_REL
            globals()["SUMS"] = snapshot / PKG_REL / SUMS_NAME
    except gate.EvidenceError as e:
        print(f"! {e}", file=sys.stderr)
        return 2
    digest_ok, digest = package_digest()
    out = {"target_head": head, "expected_head": exp, "expected_tree": tree, "head_ok": True,
           "dirty": bool(dirty), "dirty_allowed": bool(a.allow_dirty), "dirty_paths": dirty[:50],
           # ⚠ Codex R10 P2-5 · Q4: 증거로 셀 수 있는 실행은 **expected commit 의 격리 snapshot 안에서** 돈 것뿐이다.
           #   `--allow-dirty` 는 개발용이고 그 결과는 구조적으로 증거가 아니다.
           #   도구(러너·gate)도 그 커밋의 bytes 여야 한다 — 대상만 봉인하고 도구가 수정돼 있으면 그 증거는 그 커밋의 것이 아니다.
           "evidence_eligible": bool(snapshot) and digest_ok and sealed,
           "instrument_sealed": sealed, "instrument": seal_detail,
           "materialized": ({"path": str(snapshot), "head": head, "mode": "sparse detached worktree",
                             "kept": bool(a.keep_materialized)} if snapshot else None),
           "ran_in": "격리 snapshot" if snapshot else "working tree (--allow-dirty)",
           "package_digest_ok": digest_ok, "package_digest": digest, "pinned_sha": PINNED, "pin_bypassed": True,
           "설명": "원본 probe 함수를 직접 불러 SHA pin 을 우회한다 — 도달·상태·멈춘_곳을 따로 적는다; 옛 게시 위치/옛 러너 출력을 전제한 "
                 "probe 는 hook 만 현행 계약으로 옮긴 적응판(적응 True)", "requested": want, "probes": {}}
    if not digest_ok:
        out["오류"] = "패키지 bytes 가 SHA256SUMS 와 다르다 — probe 를 돌리지 않았다"
        print(json.dumps(out, ensure_ascii=False, indent=2)); return 2
    os.environ["PATH"] = str(pathlib.Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")
    root = _load("r9c_root", PKG / "r9_root_repros.py")
    target, verify, _prov, _deg, _sign, _full_matrix_rows, _shape_harness, _pair = root.boot(target)
    ws = _workspace(target)
    agg = _load("r9c_agg", ws / "outputs" / "r9_aggregation_repros.py")
    provm = _load("r9c_prov", ws / "outputs" / "r9_provenance_repro.py")
    R = out["probes"]
    for pid in want:
        if pid == "R9-01":
            R[pid] = {"probe": "root_alias", "적응": False, **_run_probe(pid, lambda: root.root_alias(target, verify, _deg, _sign))}
        elif pid == "R9-02":
            R[pid] = {"probe": "u18_roster_and_receipt + aggregation u14 cases (적응: 패키지 helper 그대로, 판정만 뒤집음)", "적응": True,
                      **_run_adapted(lambda: {"provenance": u18_prov(provm), "aggregation": r9_02_03_agg(agg, target),
                                              "closure_assert": "u18 gate 3 case rc≠0 ∧ aggregation 4 case rc≠0 이고 결함 이름을 찍는다"})}
        elif pid == "R9-03":
            R[pid] = {"probe": "blank_provenance", "적응": False, **_run_probe(pid, lambda: root.blank_provenance(target, verify, _prov, _sign, _full_matrix_rows))}
        elif pid == "R9-04":
            R[pid] = {"probe": "shape_missing_halfcell(적응: partial 위치)", "적응": True, **_run_adapted(lambda: r9_04_adapted(_shape_harness, _pair))}
        elif pid == "R9-05":
            R[pid] = {"probe": "shape_duplicate_matrix_rows(+reversed)(적응: 예외를 닫힘으로)", "적응": True, **_run_adapted(lambda: r9_05_adapted(agg, _shape_harness, _pair))}
        elif pid == "R9-06":
            R[pid] = {"probe": "shape_partial_overwrites_complete", "적응": False, **_run_probe(pid, lambda: root.shape_partial_overwrites_complete(target, _prov, _shape_harness, _pair))}
        elif pid == "R9-07":
            R[pid] = {"probe": "eval_verified_bytes_race(적응: 패키지 함수 그대로, 판정만 뒤집음)", "적응": True, **_run_adapted(lambda: r9_07_prov(provm))}
        elif pid == "P2-1":
            R[pid] = {"probe": "replay_vacuity(적응: 거부 rc·JSON 없음)", "적응": True, **_run_adapted(lambda: p2_1_adapted(target, head))}
        elif pid == "P2-2":
            R[pid] = {"probe": "runner identity(적응)", "적응": True, **_run_adapted(lambda: p2_2_adapted(target, head))}
        elif pid == "P2-3":
            R[pid] = {"probe": "r9_evidence_classify_probe(적응: 판정만 뒤집음)", "적응": True, **_run_adapted(lambda: p2_3_adapted(target))}
        elif pid == "P2-4":
            R[pid] = {"probe": "delegated → tests/test_r9_codex.py::test_d9_10", "적응": True,
                      **_run_adapted(lambda: delegated(target, "tests/test_r9_codex.py::test_d9_10_matrix_sidecar_seals_the_exact_roster_and_argv"))}
        elif pid == "P2-5":
            R[pid] = {"probe": "zero-pair typed none(적응) + test_d9_11", "적응": True,
                      **_run_adapted(lambda: {"none": p2_5_adapted(_shape_harness),
                                              "test": delegated(target, "tests/test_r9_codex.py::test_d9_11_zero_pair_and_partial_are_distinct_typed_states"),
                                              "closure_assert": "짝 0 → rc 1 · status none · canonical 없음 ∧ test_d9_11 passed"})}
    shutil.rmtree(ws, ignore_errors=True)
    if snapshot is not None and not a.keep_materialized:
        cleanup()
    statuses = {pid: r["상태"] for pid, r in R.items()}
    out["closed"] = list(R) == want and all(s == "반례 소멸" for s in statuses.values())
    out["rc_reason"] = ("모든 요청 probe 가 자기 반례 assertion 에서 멈췄다 / positive closure 가 섰다" if out["closed"]
                        else f"닫히지 않음: { {p: s for p, s in statuses.items() if s != '반례 소멸'} }")
    text = json.dumps(out, ensure_ascii=False, indent=2, default=str)
    print(text)
    if a.output:
        a.output.write_text(text + "\n", encoding="utf-8")
    # ⚠ 자체 리뷰 C19: `evidence_eligible: false` 인 실행이 rc 0 으로 끝났다 — P1-11 이 자식에게 요구한 규율
    #   ("payload 를 읽기 전에 rc 를 본다")을 러너 자신이 어긴 것이다. 증거가 아닌 실행은 성공 코드로 끝나지 않는다.
    if not out["evidence_eligible"]:
        return 3
    return 0 if out["closed"] else 1


if __name__ == "__main__":
    sys.exit(main())
