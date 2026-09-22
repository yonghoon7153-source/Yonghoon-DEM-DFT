"""R17 후속 **2차** 재검토 (대상 `a4c311ef`) — NO-GO · P1 4 · P2 2.

리뷰어가 닫혔다고 인정한 것: GC 의 escape/duplicate, 행 결속의 version/mixed/tol/cell/run_id·
소수 cycle, 최상위 `null` identity/settings, 상자 밖 seed 와 stale best 의 RuntimeError,
receipt 최상위 타입 다섯, **package 내용 digest 분리**.

받지 못한 것 — 한 줄로: **실패 입력을 막는 검사가 계약을 닫지는 않는다.**

| ID | 무엇이 틀렸나 | 자리 |
|---|---|---|
| F2-01 (P1) | GC 의 **재귀 삭제 범위**. 항목이 선언한 `kind/attempt` 와 실제 `path` 가 달라도 통과하고, 그 선언으로 만든 디렉터리를 `rmtree` 해 **보존 index 가 가리키는 payload** 와 **미등록 파일**까지 지운다 | `scripts/gc_partial.py:80,131,139,153-157` |
| F2-02 (P1) | 행의 `scale_seed`·`n_starts` 가 sidecar 와 **결속되지 않는다**. 행만 99/999 로 바꿔도 rc 0 | `scripts/width_report.py:59` · `bms_balancing/cycles.py:216,218` |
| F2-03 (P1) | `null` 을 **객체 한 단계 안으로** 옮기면 다시 "동일 확인" 이다. env 여섯 축이 전부 null/공백, `dataset_manifest` 가 공백 문자열, `lb=[NaN]*5`, `width_starts=null` 이 전부 rc 0 | `scripts/width_report.py:71-100` |
| F2-04 (P1) | **정상 producer 의 cycle 별 receipt 를 reader 가 거부한다.** 행은 `full_cell.cycle=k` 를 달고 sidecar 는 공통 receipt 인데, reader 는 통째로 같기를 요구한다 | `bms_balancing/cycles.py:206` · `scripts/width_report.py:151-160` |
| F2-05 (P2) | `best` 만 **유한성 술어 밖**이다. `best[0]=NaN` 이 `measured` · NaN 끝점 · `is_lower_bound=true` 를 낸다 | `bms_balancing/verify.py:443` |
| F2-06 (P2) | receipt 의 nested schema 가 **바깥 컨테이너에서 멈춘다**. `runtime={"python":null,"platform":null}` · `{"irrelevant":true}` · `materialized={"mode":17}` 가 전부 `verified=true` | `scripts/verify_run_receipt.py:74-78` |

리뷰어가 정한 순서를 따른다: **F2-04 정상 생산 경로를 양성 fixture 로 확보 → F2-01 보존 범위 →
F2-02/03/05/06 공통 계약.**

리뷰어 재현기 둘(`reviews/r17_followup2/codex/repro_followup2.py` · `repro_producer_reader.py`)을
이 Linux 에서 **수정 없이** 먼저 돌려 여섯 건이 모두 재현되는 것을 확인했다. 리뷰어는 Windows 라
`fcntl` 부재로 디스크 직렬화를 손으로 했지만, **이 기계에서는 실제 게시 CLI(`scripts/fit_cycles.py`)가
돈다** — 그래서 아래 F2-04 양성 경로는 리뷰어 재현기보다 한 단계 더 실물이다 (잠금·원자적 게시 포함).
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bms_balancing import schema as S          # noqa: E402
from bms_balancing import verify as V          # noqa: E402


def _run(script, *args, cwd=ROOT):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)], cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", timeout=900)


def _rows(art: Path) -> list:
    return list(csv.DictReader(art.open(encoding="utf-8", newline="")))


def _meta(art: Path) -> dict:
    return json.loads(art.with_name(art.name + ".meta.json").read_text(encoding="utf-8"))


def _save(art: Path, rows: list, meta: dict) -> None:
    """본문과 sidecar 를 같이 다시 쓴다 — **sha256 은 언제나 맞춘다** (이 시험이 흔드는 축이
    본문/sidecar 결속이 아니라 그 안의 의미이기 때문이다. 결속 자체는 ③ 이 이미 잡는다)."""
    with art.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(S.CYCLES_ROW), lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    meta = dict(meta, sha256=hashlib.sha256(art.read_bytes()).hexdigest())
    art.with_name(art.name + ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F2-04 — 정상 producer → sidecar → reader (양성 경로가 먼저다)
# ══════════════════════════════════════════════════════════════════════════════════════════════

def _produce(tmp_path: Path) -> Path:
    """**실제 게시 CLI** 로 2사이클 폭 산출 한 벌을 만든다 (합성 원자료 → `fit_cycles.py`).

    리뷰어는 `fcntl` 이 없어 `fit_cycles` **API** 만 부르고 CSV/sidecar 는 손으로 썼다.
    이 기계에서는 `publish_lock` 이 돌아 **원자적 게시까지** 실물이다 — 양성 경로를 합성
    fixture 로 대신하지 않는다는 것이 F2-04 의 요점이므로 가능한 만큼 실물로 간다.
    """
    sys.path.insert(0, str(ROOT / "tests"))
    from test_r6_internal import _synth_root                     # noqa: PLC0415
    from test_cycles import _cycle_workbook                      # noqa: PLC0415
    src = _synth_root(tmp_path)
    wb = _cycle_workbook(src, tmp_path / "syn.xlsx", n_cycles=2)
    out = tmp_path / "out"
    r = _run("scripts/fit_cycles.py", "--data-root", src,
             "--half-cell", src / "data/half_cell/GITT/pristine.xlsx", "--full-cell", wb,
             "--cell", "syn", "--si-source", "Li", "--objective-version", "legacy_matlab",
             "--starts", 1, "--seed", 0, "--scale-seed", 0,
             "--widths", "--width-tol", 0.01, "--width-starts", 0, "--width-grid", 0,
             "--run-id", "synthetic-production", "--out", out)
    assert r.returncode == 0, ("합성 입력으로도 게시가 안 됐다 — 이 시험의 전제가 깨졌다",
                               r.returncode, r.stdout[-2000:], r.stderr[-2000:])
    art = out / "cycles_syn_Li.csv"
    assert art.is_file(), (r.stdout[-1000:], r.stderr[-1000:])
    return art


@pytest.fixture(scope="module")
def produced(tmp_path_factory):
    """적합은 비싸다(≈20초) — 한 번 만들어 여러 시험이 **각자 사본**을 흔든다."""
    return _produce(tmp_path_factory.mktemp("produced"))


def _copy(produced: Path, d: Path) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    art = d / produced.name
    art.write_bytes(produced.read_bytes())
    art.with_name(art.name + ".meta.json").write_bytes(
        produced.with_name(produced.name + ".meta.json").read_bytes())
    return art


def test_fu2_01_the_real_producer_output_is_accepted_by_the_reader(produced):
    """★ F2-04 — **정상 생산 경로가 통과해야 한다.** 행은 `full_cell.cycle=k` 를 달고 sidecar 는
    공통 receipt 다. 전 판 reader 는 두 JSON 이 통째로 같기를 요구해 rc 2 였다 (리뷰어 실측).

    이 양성 경로가 없으면 "더 강한 검사" 가 올바른 산출까지 막는지 판단할 수 없다 — 리뷰어 §8.
    """
    rows = _rows(produced)
    meta = _meta(produced)
    # 전제: 생산자가 실제로 **cycle 별** receipt 를 쓴다 (이것이 F2-04 의 충돌 원인이다)
    per = [json.loads(r["consumed_inputs"])["full_cell"].get("cycle") for r in rows]
    assert per == [0, 1], ("생산자가 cycle 별 receipt 를 쓰지 않는다 — 이 시험의 전제가 바뀌었다", per)
    assert "cycle" not in meta["consumed_inputs"]["full_cell"], \
        "sidecar 의 공통 receipt 에 cycle 이 들어 있다 — 공통/사이클별 구분이 사라졌다"
    r = _run("scripts/width_report.py", produced)
    assert r.returncode == 0, ("정상 생산자의 산출을 reader 가 거부한다 (F2-04)",
                               r.returncode, r.stdout[-1500:], r.stderr[-1500:])


def test_fu2_02_a_row_receipt_carrying_another_rows_cycle_is_rejected(produced, tmp_path):
    """★ F2-04 음성 — 행 0 의 receipt 가 **행 1 의 cycle** 을 말하면 거부. 양성을 열면서 이것까지
    열리면 결속이 사라진 것이다."""
    art = _copy(produced, tmp_path / "swap")
    rows, meta = _rows(art), _meta(art)
    rec = json.loads(rows[0]["consumed_inputs"])
    rec["full_cell"]["cycle"] = 1
    rows[0]["consumed_inputs"] = json.dumps(rec, ensure_ascii=False, sort_keys=True)
    rows[0]["inputs_sha"] = S.inputs_digest(rec)
    _save(art, rows, meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, ("행의 cycle 과 receipt 의 cycle 이 어긋났는데 통과했다",
                               r.returncode, r.stdout[-800:])


def test_fu2_03_a_row_receipt_without_its_cycle_is_rejected(produced, tmp_path):
    """★ F2-04 음성 — 리뷰어의 **축 분리 대조군**(행 receipt 의 `cycle` 만 제거)은 현재 rc 0 이다.
    그것은 수정 제안이 아니라 "지금 검사가 더 적은 정상 산출을 거부한다" 는 확인이었다.
    공통/사이클별을 명시적으로 가른 뒤에는 **이쪽이 거부**돼야 한다 — 행이 어느 cycle 의 것인지
    말하지 않는 receipt 는 그 행의 것이 아니다."""
    art = _copy(produced, tmp_path / "stripped")
    rows, meta = _rows(art), _meta(art)
    for row in rows:
        rec = json.loads(row["consumed_inputs"])
        rec["full_cell"].pop("cycle", None)
        row["consumed_inputs"] = json.dumps(rec, ensure_ascii=False, sort_keys=True)
        row["inputs_sha"] = S.inputs_digest(rec)
    _save(art, rows, meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, ("cycle 을 말하지 않는 receipt 가 통과했다 (F2-04 축 분리 대조군)",
                               r.returncode, r.stdout[-800:])


def test_fu2_04_a_row_receipt_pointing_at_another_workbook_is_rejected(produced, tmp_path):
    """★ F2-04 음성 — cycle 은 맞는데 **입력 bytes** 가 다른 receipt. 이것은 전 판도 잡았다
    (대조군으로 고정한다 — 양성을 여는 수정이 이 축까지 열지 않는지)."""
    art = _copy(produced, tmp_path / "otherwb")
    rows, meta = _rows(art), _meta(art)
    rec = json.loads(rows[0]["consumed_inputs"])
    rec["full_cell"]["sha256"] = "b" * 64
    rows[0]["consumed_inputs"] = json.dumps(rec, ensure_ascii=False, sort_keys=True)
    rows[0]["inputs_sha"] = S.inputs_digest(rec)
    _save(art, rows, meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (r.returncode, r.stdout[-800:])


def test_fu2_05_a_missing_cycle_row_is_still_rejected(produced, tmp_path):
    """대조군 — 행 하나를 빼면 sidecar 의 `cycles` 선언과 어긋난다 (⑤). 계속 거부돼야 한다."""
    art = _copy(produced, tmp_path / "missing")
    rows, meta = _rows(art), _meta(art)
    _save(art, rows[:1], meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (r.returncode, r.stdout[-800:])


def test_fu2_06_a_duplicated_cycle_row_is_still_rejected(produced, tmp_path):
    """대조군 — 같은 cycle 이 두 번. `check_rows` 의 (cell, cycle) 중복 검사가 계속 물어야 한다."""
    art = _copy(produced, tmp_path / "dup")
    rows, meta = _rows(art), _meta(art)
    _save(art, [rows[0], dict(rows[0])], meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (r.returncode, r.stdout[-800:])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F2-01 — GC 의 재귀 삭제 범위
# ══════════════════════════════════════════════════════════════════════════════════════════════

def _gc_index(root: Path, entries: list) -> None:
    (root / "partial").mkdir(parents=True, exist_ok=True)
    (root / "partial" / "index.json").write_text(
        json.dumps({"index_version": 1, "attempts": entries}, ensure_ascii=False), encoding="utf-8")


def _entry(kind, attempt, artifact, path, body_sha="0" * 64, when="2026-09-22T00:00:00Z"):
    return {"kind": kind, "attempt": attempt, "artifact": artifact, "status": "partial",
            "path": path, "sha256": body_sha, "recorded_utc": when}


def test_fu2_07_gc_refuses_an_index_whose_declared_dir_is_not_the_payloads_dir(tmp_path):
    """★ F2-01 A (`gc_retained_path_alias`) — 항목의 `path` 는 `matrix/A/matrix_200.csv` 인데
    `kind/attempt` 는 `matrix/C` 라고 선언한다. 모든 성분이 평범한 문자열이고 경로도 partial 안이라
    전 판의 성분 검사·containment 검사를 전부 통과했다. 그 다음 `rmtree(A)` 가 **보존 index 가
    가리키는 A/matrix_200.csv** 를 지웠다 (리뷰어 실측 rc 0 · `watched_exists=false`).

    모순된 index 는 **첫 삭제 전에** 거부한다 — 손상된 index 를 받아들여도 된다는 뜻이 아니다."""
    out = tmp_path / "out"
    for d in ("A", "B", "C"):
        (out / "partial" / "matrix" / d).mkdir(parents=True)
    (out / "partial" / "matrix" / "A" / "matrix_100.csv").write_text("old-100", encoding="utf-8")
    watched = out / "partial" / "matrix" / "A" / "matrix_200.csv"
    watched.write_text("유일한 200 — 보존 index 가 가리킨다", encoding="utf-8")
    (out / "partial" / "matrix" / "B" / "matrix_100.csv").write_text("new-100", encoding="utf-8")
    _gc_index(out, [
        _entry("matrix", "A", "matrix_100.csv", "matrix/A/matrix_100.csv"),
        _entry("matrix", "B", "matrix_100.csv", "matrix/B/matrix_100.csv",
               when="2026-09-22T01:00:00Z"),
        # ★ 선언(C)과 실제 payload(A) 가 다르다 — 이것이 반례의 전부다
        _entry("matrix", "C", "matrix_200.csv", "matrix/A/matrix_200.csv"),
    ])
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert watched.exists(), ("보존 index 가 가리키는 payload 를 GC 가 지웠다 (F2-01 A)",
                              r.returncode, r.stdout[-600:], r.stderr[-600:])
    assert r.returncode == 2, ("선언과 payload 가 모순인 index 를 거부하지 않았다 (F2-01 A)",
                               r.returncode, r.stderr[-600:])


def test_fu2_08_gc_does_not_delete_an_unindexed_file_inside_an_attempt_dir(tmp_path):
    """★ F2-01 B (`gc_unknown_file`) — index 는 정상(A/100 · B/100)이고 A 안에 **원장에 없는
    파일**이 하나 더 있다. 전 판은 `rmtree(A)` 로 그것까지 지웠다 (rc 0). `unknown` 검사가 시도
    **디렉터리**만 열거해 그 안의 파일을 보지 않았기 때문이다 — 회신 §5 의 "원장에 없는 파일도
    rc 2" 는 코드와 달랐다.

    `③ 모르면 안 지운다` 를 **파일 단위까지** 내린다."""
    out = tmp_path / "out"
    (out / "partial" / "matrix" / "A").mkdir(parents=True)
    (out / "partial" / "matrix" / "B").mkdir(parents=True)
    (out / "partial" / "matrix" / "A" / "matrix_100.csv").write_text("old-100", encoding="utf-8")
    (out / "partial" / "matrix" / "B" / "matrix_100.csv").write_text("new-100", encoding="utf-8")
    stray = out / "partial" / "matrix" / "A" / "unindexed.txt"
    stray.write_text("원장에 없는 바이트", encoding="utf-8")
    _gc_index(out, [
        _entry("matrix", "A", "matrix_100.csv", "matrix/A/matrix_100.csv"),
        _entry("matrix", "B", "matrix_100.csv", "matrix/B/matrix_100.csv",
               when="2026-09-22T01:00:00Z"),
    ])
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert stray.exists(), ("원장에 없는 파일을 GC 가 지웠다 (F2-01 B)",
                            r.returncode, r.stdout[-600:], r.stderr[-600:])
    assert r.returncode == 2, ("모르는 파일을 보고도 rc 0 이었다 (F2-01 B)",
                               r.returncode, r.stderr[-600:])


def test_fu2_09_gc_keeps_the_reviewer_accepted_original_case(tmp_path):
    """대조군 — 리뷰어가 **닫혔다고 인정한** 원 반례(A/100 · A/200 · B/100)는 계속 rc 0 이고
    A/200 이 남아야 한다. 삭제 단위를 파일로 내리는 이번 수정이 그것을 되돌리면 여기서 잡힌다."""
    out = tmp_path / "gc-safe"; out.mkdir()
    for name, rid, body in [("matrix_100.csv", "A", "100-old"), ("matrix_200.csv", "A", "200-only"),
                            ("matrix_100.csv", "B", "100-new")]:
        canonical = out / name
        d = V.publish_target(canonical, "partial", run_id=rid)
        d.write_text(body, encoding="utf-8")
        V.record_partial(canonical, d, status="partial", run_id=rid)
    survivor = out / "partial" / "matrix" / "A" / "matrix_200.csv"
    doomed = out / "partial" / "matrix" / "A" / "matrix_100.csv"
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert r.returncode == 0, (r.returncode, r.stdout[-600:], r.stderr[-600:])
    assert survivor.exists(), "A/200 이 사라졌다 — R17 P1-01 의 수정이 되돌아갔다"
    assert not doomed.exists(), "버려야 할 A/100 이 남았다 — GC 가 아무것도 안 했다"


def test_fu2_10_gc_removes_the_attempt_dir_when_every_file_in_it_is_doomed(tmp_path):
    """대조군 — 시도 디렉터리 전체가 버려지면 **빈 디렉터리는 정리**돼야 한다 (보존 우선이
    "아무것도 안 지운다" 로 넘어가지 않는지). 정상 producer 로만 만든다."""
    out = tmp_path / "gc-empty"; out.mkdir()
    for name, rid, body in [("matrix_100.csv", "A", "old"), ("matrix_100.csv", "B", "new")]:
        canonical = out / name
        d = V.publish_target(canonical, "partial", run_id=rid)
        d.write_text(body, encoding="utf-8")
        V.record_partial(canonical, d, status="partial", run_id=rid)
    r = _run("scripts/gc_partial.py", "--root", out, "--keep", "1", "--apply")
    assert r.returncode == 0, (r.returncode, r.stderr[-600:])
    assert not (out / "partial" / "matrix" / "A").exists(), \
        "전부 버려진 시도 디렉터리가 남았다 — 빈 디렉터리 정리가 사라졌다"
    assert (out / "partial" / "matrix" / "B" / "matrix_100.csv").exists()


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F2-02 — 행에 남은 실행 조건 두 개 (scale_seed · n_starts)
# ══════════════════════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("col,bad", [("scale_seed", "99"), ("n_starts", "999")])
def test_fu2_11_a_row_only_execution_condition_must_match_the_sidecar(produced, tmp_path, col, bad):
    """★ F2-02 — 행의 `scale_seed`/`n_starts` 는 **생산자가 행에 적는 실행 조건**인데
    `BODY_META_BOUND` 에 없어 sidecar 와 대조되지 않았다. 전부 바꿔도 rc 0 이었다."""
    art = _copy(produced, tmp_path / f"all-{col}")
    rows, meta = _rows(art), _meta(art)
    for row in rows:
        row[col] = bad
    _save(art, rows, meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (f"행의 `{col}` 이 sidecar 와 달라도 통과했다 (F2-02)",
                               r.returncode, r.stdout[-800:])


@pytest.mark.parametrize("col,bad", [("scale_seed", "99"), ("n_starts", "999")])
def test_fu2_12_a_mixed_execution_condition_inside_one_file_is_rejected(produced, tmp_path, col, bad):
    """★ F2-02 — 한 파일 안에서 **일부 행만** 바꾼 것(`width_row_scale_mixed`). 비교 조건은
    파일당 하나여야 한다."""
    art = _copy(produced, tmp_path / f"mixed-{col}")
    rows, meta = _rows(art), _meta(art)
    rows[0][col] = bad
    _save(art, rows, meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (f"한 파일 안에서 `{col}` 이 섞여도 통과했다 (F2-02)",
                               r.returncode, r.stdout[-800:])


def test_fu2_13_the_sidecar_two_starts_declarations_must_agree(produced, tmp_path):
    """★ F2-02 — sidecar 는 `starts` 와 `n_multistart` 로 **같은 것을 두 번** 적는다. 둘이 다르면
    어느 쪽이 실행 조건인지 말할 수 없다 (리뷰어: "sidecar 의 두 starts 선언 사이 관계")."""
    art = _copy(produced, tmp_path / "starts")
    rows, meta = _rows(art), _meta(art)
    meta["starts"] = int(meta["n_multistart"]) + 5
    _save(art, rows, meta)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, ("sidecar 의 두 starts 선언이 달라도 통과했다 (F2-02)",
                               r.returncode, r.stdout[-800:])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F2-03 — null·공백·불법 값이 **객체 안**에 있을 때
# ══════════════════════════════════════════════════════════════════════════════════════════════

_ENV_OK = {"python": "3.11.9", "numpy": "1.26.4", "scipy": "1.13.1", "pandas": "2.2.2",
           "openpyxl": "3.1.2", "platform": "Linux-x86_64"}


def _patch_meta(produced, d: Path, **patch) -> Path:
    art = _copy(produced, d)
    rows, meta = _rows(art), _meta(art)
    meta.update(patch)
    _save(art, rows, meta)
    return art


@pytest.mark.parametrize("name,patch", [
    ("env_python_only", {"env": {"python": "3.11.9"}}),
    ("env_null_values", {"env": {k: None for k in _ENV_OK}}),
    ("env_whitespace", {"env": {k: " \t " for k in _ENV_OK}}),
    ("manifest_whitespace", {"dataset_manifest": "   "}),
    ("manifest_shapeless", {"dataset_manifest": {"id": "no-version-no-sha"}}),
    ("bounds_singleton", {"lb": [0.0], "ub": [0.0], "initial": [0.0]}),
    ("bounds_nan", {"lb": [float("nan")] * 5}),
    ("bounds_inverted", {"lb": [1.4, 0.0, 1.4, 0.1, 0.5], "ub": [1.0, -0.5, 1.0, -0.5, 0.0]}),
    ("initial_outside_box", {"initial": [99.0, 0.0, 1.1, 0.0, 0.25]}),
    ("untyped_width_starts", {"width_starts": None}),
    ("untyped_width_grid", {"width_grid": None}),
])
def test_fu2_14_an_invalid_value_inside_a_required_object_is_rejected(produced, tmp_path, name, patch):
    """★ F2-03 — 최상위 `null` 을 닫았더니 **한 단계 안**으로 옮겨 갔다. 양쪽 값이 같다는 사실이
    유효성을 대신하지 않는다 — 각 파일의 유효성을 **먼저** 본다.

    `nan` 은 JSON 표준 밖이지만 Python 의 `json` 이 `NaN` 으로 쓰고 읽는다 — 리뷰어가 낸 그 입력
    그대로다 (`REPRO_RESULTS.json` 의 NaN 도 같은 성격이라고 밝혔다)."""
    art = _patch_meta(produced, tmp_path / name, **patch)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (f"{name}: 필수 객체 안의 불법 값이 통과했다 (F2-03)",
                               r.returncode, r.stdout[-900:])


@pytest.mark.parametrize("name,patch", [
    ("gamma_lb_null", {"gamma_lb": None}),
    ("gamma_init_null", {"gamma_init": None}),
    ("literature_null", {"literature": None}),
])
def test_fu2_15_a_legitimately_nullable_setting_still_passes(produced, tmp_path, name, patch):
    """대조군 — **합법적으로 nullable 한** 항목은 계속 통과해야 한다. "null 이면 전부 거부" 로
    넓히면 정상 산출이 막힌다 (리뷰어: "합법 nullable 인 gamma_lb 등과 미기록을 구분한다")."""
    art = _patch_meta(produced, tmp_path / name, **patch)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 0, (f"{name}: 정상 nullable 이 막혔다", r.returncode, r.stdout[-900:])


def test_fu2_16_a_legacy_env_without_the_added_axis_is_named_not_silently_accepted(produced, tmp_path):
    """★ F2-03 — 나중에 더해진 축(`openpyxl`)이 **키째 없는** 옛 sidecar. `env_axes_missing` 의
    규칙 그대로 위반으로 세되, 메시지가 그것을 **나이**라고 말해야 한다 (조용히 통과시키지 않는다)."""
    env = {k: v for k, v in _ENV_OK.items() if k != "openpyxl"}
    art = _patch_meta(produced, tmp_path / "legacy-env", env=env)
    r = _run("scripts/width_report.py", art)
    assert r.returncode == 2, (r.returncode, r.stdout[-900:])
    both = r.stdout + r.stderr
    assert "openpyxl" in both, ("빠진 축의 이름이 출력에 없다", both[-900:])


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F2-05 — best 만 유한성 술어 밖이다
# ══════════════════════════════════════════════════════════════════════════════════════════════

def _mid_box():
    from bms_balancing import model                                  # noqa: PLC0415
    return (np.asarray(model.LB5, float) + np.asarray(model.UB5, float)) / 2.0, model


def test_fu2_17_a_non_finite_best_is_refused_before_any_width_is_measured():
    """★ F2-05 — `best[0]=NaN` 이면 선행 비교 두 부등식이 **둘 다 false** 라 상자 검사를 통과했다.
    `_in_box` 는 유한성을 보는데 `best` 만 그 술어를 안 거쳤다 — "모든 후보에 같은 술어" 가
    여전히 아니었다. 결과는 예외 없이 NaN min/max/span + `is_lower_bound=true` (리뷰어 실측)."""
    bp, model = _mid_box()
    best = bp.copy(); best[0] = float("nan")
    with pytest.raises(ValueError, match="유한"):
        V.near_optimal_extrema(lambda p: 1.0, bp, 1.0, 1.0, best, 1.0, tol=0.01, seeds=[],
                               n_starts=0, seed=0, lb=model.LB5, ub=model.UB5)


def test_fu2_18_a_non_finite_best_makes_the_row_say_failed_not_measured():
    """★ F2-05 — 실제 행 helper 까지. 값을 지어내지 않고 `width_status='failed'` 여야 한다
    (안 잼/실패/빈 집합은 0 이 아니다 — W-10)."""
    from bms_balancing import cycles as C                             # noqa: PLC0415
    bp, model = _mid_box()
    best = bp.copy(); best[0] = float("nan")

    class _Obj:
        def __call__(self, p):
            return 1.0

    out = C._width_fields(True, _Obj(), bp, 1.0, 1.0, best, 1.0, 0.01, 0, 0,
                          np.asarray(model.LB5, float), lambda s: None, grid=0)
    assert out["width_status"] == "failed", out
    assert all(out[f"{m}_lo"] in ("", None) for m in ("LAM_PE", "LAM_NE", "LLI")), out


def test_fu2_19_a_finite_best_still_measures_a_width():
    """대조군 — 정상 입력은 계속 `measured` 여야 한다 (유한성 검사를 넓혀 정상 계산을 막지 않았는지)."""
    from bms_balancing import cycles as C                             # noqa: PLC0415
    bp, model = _mid_box()

    class _Obj:
        def __call__(self, p):
            return 1.0 + float((np.asarray(p, float)[0] - bp[0]) ** 2)

    out = C._width_fields(True, _Obj(), bp, 1.0, 1.0, bp.copy(), 1.0, 0.01, 0, 0,
                          np.asarray(model.LB5, float), lambda s: None, grid=0)
    assert out["width_status"] == "measured", out
    assert all(np.isfinite(float(out[f"{m}_lo"])) and np.isfinite(float(out[f"{m}_hi"]))
               for m in ("LAM_PE", "LAM_NE", "LLI")), out


def test_fu2_20_an_out_of_box_seed_is_still_refused():
    """대조군 — 리뷰어가 닫혔다고 인정한 축(상자 밖 seed)이 계속 물어야 한다."""
    bp, model = _mid_box()
    lo = np.asarray(model.LB5, float)
    far = lo.copy(); far[0] = lo[0] - 100.0
    ext = V.near_optimal_extrema(lambda p: 1.0, bp, 1.0, 1.0, bp.copy(), 1.0, tol=0.01,
                                 seeds=[far], n_starts=1, seed=0, lb=model.LB5, ub=model.UB5)
    assert all(np.isfinite(ext[k]["min"]) and np.isfinite(ext[k]["max"]) for k in ext), ext


# ══════════════════════════════════════════════════════════════════════════════════════════════
# F2-06 — receipt 의 nested schema 가 내부 필드에서 멈춘다
# ══════════════════════════════════════════════════════════════════════════════════════════════

def _receipt(tmp_path: Path, **over) -> Path:
    """실제 HEAD/tree/instrument blob 을 쓰고 공개 `receipt_signature` 로 checksum 을 **다시**
    계산한다 — 암호학적 위조가 아니라 **입력 schema** 시험이다 (리뷰어 §4 와 같은 전제)."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as gate                                      # noqa: PLC0415
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    tree = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD^{tree}"],
                                   text=True).strip()
    blob = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{head}:./scripts/verify_run_receipt.py"],
        text=True).strip()
    r = {"receipt_version": gate.RUN_RECEIPT_VERSION,
         "code": {"commit": head, "tree": tree},
         "instrument": {"scripts/verify_run_receipt.py": blob},
         "package": {"digest": "a" * 64},
         "materialized": None,
         "runtime": {"python": sys.version.split()[0], "platform": sys.platform},
         "produced_utc": "2026-09-22T00:00:00+00:00"}
    r.update(over)
    r["signature"] = gate.receipt_signature(r)
    p = tmp_path / "receipt.json"
    p.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


@pytest.mark.parametrize("name,over", [
    ("runtime_python_null", {"runtime": {"python": None, "platform": None}}),
    ("runtime_wrong_keys", {"runtime": {"irrelevant": True}}),
    ("runtime_whitespace", {"runtime": {"python": "  ", "platform": "\t"}}),
    ("materialized_wrong_fields", {"materialized": {"mode": 17}}),
])
def test_fu2_21_a_receipt_whose_inner_fields_are_meaningless_is_not_verified(tmp_path, name, over):
    """★ F2-06 — `runtime` 은 `bool(dict)` 만, `materialized` 는 `isinstance(dict)` 만 봤다.
    발행자가 실제로 쓰는 `{python, platform}` 문자열과 `materialized.mode` 의 뜻을 확인하지
    않는다 — 세 경우 모두 rc 0 · `complete=true` · `verified=true` 였다 (리뷰어 실측)."""
    p = _receipt(tmp_path, **over)
    r = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    assert r.returncode == 3, (f"{name}: 내부 필드가 뜻이 없는 receipt 가 verified 였다 (F2-06)",
                               r.returncode, r.stdout[-900:])


def test_fu2_22_a_receipt_from_the_real_producer_is_verified(tmp_path):
    """대조군 — **실제 생산자**(`evidence_gate.run_receipt`)가 내는 모양은 계속 통과해야 한다.
    schema 를 조이면서 정본 발행을 막으면 여기서 잡힌다 (F2-04 와 같은 교훈)."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as gate                                      # noqa: PLC0415
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    tree = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD^{tree}"],
                                   text=True).strip()
    blob = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{head}:./scripts/verify_run_receipt.py"],
        text=True).strip()
    r = gate.run_receipt(head=head, tree=tree,
                         instrument={"scripts/verify_run_receipt.py": blob},
                         package_digest="a" * 64,
                         materialized={"mode": "sparse detached worktree"},
                         runtime={"python": sys.version.split()[0], "platform": sys.platform})
    p = tmp_path / "real.json"
    p.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    out = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    assert out.returncode == 0, ("정본 발행 모양이 거부됐다", out.returncode, out.stdout[-900:])


def test_fu2_23_materialized_none_is_still_legal(tmp_path):
    """대조군 — `materialized=None` 은 생산자가 실제로 내는 상태다. 금지하지 않는다."""
    p = _receipt(tmp_path, materialized=None)
    r = _run("scripts/verify_run_receipt.py", "--receipt", p, "--target", ROOT)
    assert r.returncode == 0, (r.returncode, r.stdout[-900:])


def test_fu2_24_the_producer_refuses_to_sign_a_meaningless_runtime():
    """★ F2-06 — 계약을 **생산자와 소비자가 공유**한다. 뜻 없는 runtime 은 서명 단계에서 멈춘다
    (소비자만 조이면 "발행은 되는데 아무도 못 읽는" 영수증이 생긴다)."""
    sys.path.insert(0, str(ROOT / "reviews"))
    import evidence_gate as gate                                      # noqa: PLC0415
    with pytest.raises(ValueError, match="runtime"):
        gate.run_receipt(head="0" * 40, tree="1" * 40, instrument={"x": "2" * 40},
                         package_digest="a" * 64, materialized=None,
                         runtime={"python": None, "platform": None})
