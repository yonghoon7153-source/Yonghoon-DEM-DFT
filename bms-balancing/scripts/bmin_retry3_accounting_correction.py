"""B-min r2 retry3 — `FINAL_INPUT_ACCOUNTING.json` 의 준비 단계 boolean 정정표 (수신 검토 BMIN-R3-C1 · COMSOL SPEC §59-3 의 1).

    python3 bms-balancing/scripts/bmin_retry3_accounting_correction.py <결과 ZIP> <출력 JSON>

결과 ZIP 을 **데이터로만** 읽는다 (안의 .py · .ps1 · Java 는 import · 실행하지 않는다 · 표준 라이브러리만). 원 ZIP · 그 안의 파일은 고치지 않는다.
행마다 (ID, input_index) 에 대해: 원래 두 값 (`fixture_created` · `actual_call_bound`) 과 준비 단계 `INPUT_CASE_MAP.json` 의 같은 값 · 상태를 함께 적어
"준비 시점 값의 복사" 임을 보이고, 그 행의 실제 근거 (fixture · 결과 · 엔진 stdout 의 줄) 를 ZIP 안 경로 + sha256 / 줄 번호로 결속한다. 두 값을 true 로
덮어쓰지 않는다 — 대신 `superseded_by_evidence` 에 근거를 둔다. 근거 하나라도 어긋나면 출력하지 않고 rc 1.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

EXPECTED_ZIP_SHA256 = "ed0138b90cf2dc4e42f22ec18d8719ff56906780f74b4139850d604b096bb470"
EXPECTED_MANIFEST_SHA256 = "97f51112bd6c4e0ae502e56db99eba5fb56026c7b7c79d0639661cf44727b91a"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _rows_by_key(rows, where):
    out = {}
    for r in rows:
        k = (r["id"], r["input_index"])
        if k in out:
            raise SystemExit(f"{where}: (ID, input_index) 중복 {k}")
        out[k] = r
    return out


def build(zip_path: Path) -> dict:
    raw = zip_path.read_bytes()
    if _sha(raw) != EXPECTED_ZIP_SHA256:
        raise SystemExit(f"ZIP sha256 이 수신 검토가 본 값이 아니다: {_sha(raw)}")
    z = zipfile.ZipFile(zip_path)
    names = set(z.namelist())
    mb = z.read("PACKAGE_MANIFEST.json")
    if _sha(mb) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("PACKAGE_MANIFEST.json sha256 불일치")
    manifest = {f["file"]: f["sha256"] for f in json.loads(mb)["files"]}
    for f, s in manifest.items():
        if _sha(z.read(f)) != s:
            raise SystemExit(f"payload sha256 불일치: {f}")

    def ref(path):
        if path not in manifest:
            raise SystemExit(f"manifest 밖의 근거를 쓰려 했다: {path}")
        return {"path": path, "sha256": manifest[path]}

    def stdout_lines(path):
        return z.read(path).decode("utf-8").splitlines()

    final = json.loads(z.read("FINAL_INPUT_ACCOUNTING.json"))
    prep = _rows_by_key(json.loads(z.read("INPUT_CASE_MAP.json")), "INPUT_CASE_MAP")
    final_by = _rows_by_key(final, "FINAL_INPUT_ACCOUNTING")
    if set(final_by) != set(prep) or len(final_by) != 77:
        raise SystemExit(f"집합 불일치: final {len(final_by)} · prep {len(prep)}")

    py_out = stdout_lines("engine_returns/Python_stdout.txt")
    ps_out = stdout_lines("engine_returns/PS51_stdout.txt")
    jv_out = stdout_lines("engine_returns/Java_stub_stdout.txt")
    ps_results = json.loads(z.read("results/PS_RESULTS.json"))["results"]
    ps_bind = _rows_by_key(json.loads(z.read("PS_INPUT_BINDINGS.json"))["inputs"], "PS_INPUT_BINDINGS")
    prepared = _rows_by_key(json.loads(z.read("PREPARED_PYTHON_INPUTS.json")), "PREPARED_PYTHON_INPUTS")

    rows = []
    for idx, r in enumerate(final):
        key = (r["id"], r["input_index"])
        p = prep[key]
        for fld in ("fixture_created", "actual_call_bound"):
            if r[fld] is not False or p[fld] is not False:
                raise SystemExit(f"{key}: {fld} 가 예상한 준비 단계 false 가 아니다 (final {r[fld]!r} · prep {p[fld]!r})")
        if r["status"] != "PASS" or p["status"] != "NOT_RUN":
            raise SystemExit(f"{key}: 상태가 예상과 다르다 (final {r['status']} · prep {p['status']})")
        eng = r["engine"]
        if eng == "Python":
            base = f"{key[0]}_{key[1]}"
            fixtures = sorted(n for n in manifest if n.startswith(f"fixtures/{base}/"))
            result_path = f"results/{base}.json"
            # stdout 의 줄 = harness 판정 (= 최종 집계의 observed) · results/<ID>_<idx>.json = 실제 candidate_entry 가 낸 산출 (있을 때만 —
            # 거부 사례는 산출 전에 멈출 수 있다). 둘은 다른 객체라 따로 결속한다.
            hits = [i for i, ln in enumerate(py_out, 1) if json.loads(ln) == r["observed"]]
            if not fixtures or len(hits) != 1 or key not in prepared:
                raise SystemExit(f"{key}: Python 근거 결속 실패 (fixture {len(fixtures)} · stdout 일치 {hits})")
            evidence = {"input_generation": "Python harness 가 시험 임시 위치에 fixture 를 만들어 실제 consumer → candidate_entry 로 호출 (PREPARED_PYTHON_INPUTS.json 행 · fixture 파일 아래)",
                        "fixture_files": [ref(f) for f in fixtures],
                        "prepared_input_row": {"file": ref("PREPARED_PYTHON_INPUTS.json"), "key": list(key)},
                        "entry_output": ref(result_path) if result_path in manifest else None,
                        "harness_verdict": {**ref("engine_returns/Python_stdout.txt"), "line": hits[0]},
                        "engine_return": ref("engine_returns/Python_RETURN.json")}
        elif eng.startswith("Windows PowerShell"):
            # 같은 ID 에 입력이 여럿일 수 있다 (예: PS01-07) — ID 가 아니라 행 전체로 찾는다
            res = [i for i, x in enumerate(ps_results) if x == r["observed"]]
            hits = [i for i, ln in enumerate(ps_out, 1) if json.loads(ln) == r["observed"]]
            if len(res) != 1 or len(hits) != 1 or key not in ps_bind:
                raise SystemExit(f"{key}: PowerShell 근거 결속 실패 (결과 {len(res)} · stdout 일치 {hits})")
            evidence = {"input_generation": "PS_INPUT_BINDINGS.json 의 입력 결속 (Python 이 만든 결과 JSON · 자식 반환 기록) 을 봉인 PARENT_COMMAND.ps1 에서 추출한 GDecision / GNativeAxis / GFields 에 넣어 Windows PowerShell 5.1 로 호출",
                        "input_binding_row": {"file": ref("PS_INPUT_BINDINGS.json"), "key": list(key)},
                        "result": {"file": ref("results/PS_RESULTS.json"), "results_index": res[0]},
                        "harness_verdict": {**ref("engine_returns/PS51_stdout.txt"), "line": hits[0]},
                        "engine_return": ref("engine_returns/PS51_RETURN.json")}
        elif eng.startswith("Java helper"):
            want = f"{key[0]}|{r['observed']['status']}|{r['observed']['reason']}"
            hits = [i for i, ln in enumerate(jv_out, 1) if ln == want]
            if len(hits) != 1:
                raise SystemExit(f"{key}: Java 근거 결속 실패 (stdout 일치 {hits})")
            evidence = {"input_generation": "harness/ShapeHarness.java 가 봉인 Java 에서 추출한 checkShape · TIMES 를 호출 (COMSOL jar · 모델 없음)",
                        "harness": ref("harness/ShapeHarness.java"),
                        "extracted": [ref("extracted/checkShape.java.txt"), ref("extracted/TIMES.java.txt")],
                        "harness_verdict": {**ref("engine_returns/Java_stub_stdout.txt"), "line": hits[0]},
                        "engine_return": ref("engine_returns/Java_stub_RETURN.json")}
        else:
            raise SystemExit(f"{key}: 모르는 엔진 {eng!r}")
        rows.append({"id": key[0], "input_index": key[1], "engine": eng,
                     "final_accounting_row": idx,
                     "original": {"status": r["status"], "fixture_created": False, "actual_call_bound": False},
                     "pretest_template": {"file": "INPUT_CASE_MAP.json", "status": p["status"],
                                          "fixture_created": False, "actual_call_bound": False},
                     "interpretation": "두 boolean 은 준비 단계 (status NOT_RUN) 템플릿 값이 최종 집계에 복사된 것 — 최종 판정 권위 없음. 최종 근거는 superseded_by_evidence",
                     "superseded_by_evidence": evidence})
    counts = {}
    for row in rows:
        k = row["engine"].split(" ")[0]
        counts[k] = counts.get(k, 0) + 1
    return {"schema": "bmin-r2-retry3-accounting-correction/v1",
            "finding": "BMIN-R3-C1 (수신 검토 BMIN_R2_RETRY3_REVIEW_20261006 §5)",
            "source": {"zip": "BMIN_R2_LIMITED_VALIDATION_RETRY3_RESULT_20261005.zip", "zip_sha256": EXPECTED_ZIP_SHA256,
                       "manifest_sha256": EXPECTED_MANIFEST_SHA256, "corrected_file": ref("FINAL_INPUT_ACCOUNTING.json"),
                       "pretest_file": ref("INPUT_CASE_MAP.json")},
            "rule": "원 ZIP · 원 집계는 고치지 않는다 · 두 값을 true 로 덮어쓰지 않는다 · 행마다 실제 근거를 경로 + sha256 / 줄로 결속한다",
            "counts": {"rows": len(rows), **counts},
            "not_claimed": ["PS01-16 의 TryParse 내부 분기 (UNOBSERVED — §59-3 의 2 · 승인권자 결정 대기)",
                            "PY04-02 = 실제 NORMAL240 교체 (baseline identity 거부에 한정한 대체 증거)",
                            "PY05-03 = tlist · tables 동시 변조 (RUNTIME_TLIST 거부에 한정한 대체 증거)",
                            "원 CSV 값의 독립 재검산 (대형 fixture 원 CSV 는 ZIP 에 없음)"],
            "rows": rows}


def main(argv) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    out = build(Path(argv[1]))
    Path(argv[2]).write_text(json.dumps(out, ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")
    print(f"rows {out['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
