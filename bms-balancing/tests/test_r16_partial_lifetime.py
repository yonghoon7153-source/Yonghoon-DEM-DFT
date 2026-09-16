"""R16 — 조건 8 축 ④: partial 산출의 **수명** (2026-09-16).

리뷰어(R12 §5 답변 5)가 남긴 것: *"`partial/<producer>/<attempt-id>/` immutable unit + retention/GC/index.
**미구현.** 지금은 같은 이름의 다음 부분 실행이 그 자리를 덮는다."*

지금 무엇이 문제인가: `publish_target` 이 `out.parent/partial/<이름>` 하나를 쓴다. 두 번째 부분 실행이
첫 번째를 **말없이 덮는다** — 부분 실행의 역사가 사라지고, "언제 무엇을 시도해서 무엇이 나왔나" 를
나중에 말할 수 없다. canonical 은 안 건드리므로 과학 값은 안전하지만, **부분의 기록 자체가 증거**다.

### attempt-id 인가 content-id 인가 (R12 Q4, 답이 안 왔다 — 우리가 정하고 근거를 적는다)

**attempt-id(`run_id`) 를 정본으로 한다.**

- 이 저장소의 provenance 모델 전체가 산출을 **시도**에 묶는다 (행마다 `run_id`, `LAST_RUN_ID`,
  자체 리뷰 C02: "`run_id` 는 시도마다 uuid4 이므로 독립 실행이면 같을 수 없다").
- content-id 로 하면 **같은 bytes 를 낸 두 시도가 한 디렉터리로 합쳐진다** — 그런데 "두 번 시도했다" 는
  사실이야말로 이 축이 남기려는 것이다.
- R12 가 걱정한 "같은 bytes 가 여러 번 쌓인다" 는 받아들인다. 대신 index 가 digest 를 적으므로
  소비자가 중복을 **볼 수 있다** (숨기지 않고 드러낸다).

### 이 라운드가 세우는 계약

  ① 경로는 `partial/<종류>/<attempt-id>/<이름>` — 종류와 시도가 경로에 있다
  ② **immutable** — 같은 자리에 두 번 쓰지 않는다 (덮어쓰기는 버그이지 정상 경로가 아니다)
  ③ **index** — `partial/index.json` 이 시도마다 한 줄 (wildcard 로 훑지 않는다, R10 P2-2)
  ④ **retention/GC** — `scripts/gc_partial.py` 가 기본 **dry-run**, canonical 은 절대 안 건드린다
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from bms_balancing import verify as V          # noqa: E402


def test_r16_51_a_partial_lands_under_its_producer_and_attempt(tmp_path):
    """[R16-51 · ①] 부분 산출의 자리에 **종류와 시도**가 들어간다 — canonical 은 그대로다."""
    out = tmp_path / "out" / "matrix_100.csv"
    out.parent.mkdir(parents=True)
    dest = V.publish_target(out, "partial", run_id="att-1")
    assert dest.parent.name == "att-1" and dest.parent.parent.name == "matrix", dest
    assert dest.name == out.name and dest != out, dest
    assert V.publish_target(out, "complete", run_id="att-1") == out, "complete 는 canonical 자리 그대로다"


def test_r16_52_two_attempts_do_not_overwrite_each_other(tmp_path):
    """[R16-52 · ②] 두 부분 실행이 **서로를 덮지 않는다** — 이것이 이 축의 본론이다."""
    out = tmp_path / "out" / "matrix_100.csv"
    out.parent.mkdir(parents=True)
    a = V.publish_target(out, "partial", run_id="att-1")
    b = V.publish_target(out, "subset", run_id="att-2")
    assert a != b, (a, b)
    a.write_text("first\n", encoding="utf-8")
    b.write_text("second\n", encoding="utf-8")
    assert a.read_text(encoding="utf-8") == "first\n", "첫 시도가 덮였다"


def test_r16_53_the_same_attempt_is_never_written_twice(tmp_path):
    """[R16-53 · ②] 같은 시도 자리에 두 번 쓰는 것은 **버그다** — 조용히 덮지 않고 멈춘다.

    immutable unit 이라는 말이 실제로 무엇이든 막지 않으면 그것은 이름뿐이다.
    """
    out = tmp_path / "out" / "profile_gamma_100_Li.csv"
    out.parent.mkdir(parents=True)
    dest = V.publish_target(out, "partial", run_id="att-1")
    dest.write_text("x\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        V.publish_target(out, "partial", run_id="att-1")


def test_r16_54_the_index_records_every_attempt_without_globbing(tmp_path):
    """[R16-54 · ③] 시도마다 index 에 한 줄 — 소비자가 wildcard 로 훑지 않아도 된다 (R10 P2-2).

    digest 를 같이 적는다: attempt-id 를 정본으로 했으므로 **같은 bytes 의 중복**이 생길 수 있고,
    그것을 숨기지 않고 드러내는 것이 이 선택의 조건이다.
    """
    out = tmp_path / "out" / "matrix_100.csv"
    out.parent.mkdir(parents=True)
    for rid, body in (("att-1", "a\n"), ("att-2", "b\n"), ("att-3", "a\n")):
        d = V.publish_target(out, "partial", run_id=rid)
        d.write_text(body, encoding="utf-8")
        V.record_partial(out, d, status="partial", run_id=rid)

    idx = json.loads((tmp_path / "out" / "partial" / "index.json").read_text(encoding="utf-8"))
    assert [e["attempt"] for e in idx["attempts"]] == ["att-1", "att-2", "att-3"], idx
    assert all(e["artifact"] == "matrix_100.csv" and e["kind"] == "matrix" for e in idx["attempts"]), idx
    assert all(len(e["sha256"]) == 64 and e.get("recorded_utc") for e in idx["attempts"]), idx
    same = [e["attempt"] for e in idx["attempts"] if e["sha256"] == idx["attempts"][0]["sha256"]]
    assert same == ["att-1", "att-3"], ("같은 bytes 의 중복이 드러나야 한다", same)


def _gc(*args, cwd):
    return subprocess.run([sys.executable, str(ROOT / "scripts/gc_partial.py"), *map(str, args)],
                          cwd=cwd, capture_output=True, text=True, timeout=300)


def test_r16_55_gc_is_dry_run_by_default_and_never_touches_canonical(tmp_path):
    """[R16-55 · ④] 보관 정책은 **기본이 dry-run** 이고 canonical 은 절대 안 건드린다.

    지우는 도구의 기본값이 "지운다" 이면 사고는 되돌릴 수 없다. 그리고 이 도구가 canonical 을 건드리면
    과학 산출이 사라진다 — 그 경계를 시험이 고정한다.
    """
    out = tmp_path / "out" / "matrix_100.csv"
    out.parent.mkdir(parents=True)
    out.write_text("canonical\n", encoding="utf-8")
    for rid in ("att-1", "att-2", "att-3"):
        d = V.publish_target(out, "partial", run_id=rid)
        d.write_text(rid + "\n", encoding="utf-8")
        V.record_partial(out, d, status="partial", run_id=rid)

    r = _gc("--root", tmp_path / "out", "--keep", 1, cwd=ROOT)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert "att-1" in r.stdout and ("지우지 않았다" in r.stdout or "dry" in r.stdout.lower()), r.stdout
    assert (tmp_path / "out" / "partial" / "matrix" / "att-1").exists(), "dry-run 이 지웠다"

    r = _gc("--root", tmp_path / "out", "--keep", 1, "--apply", cwd=ROOT)
    assert r.returncode == 0, (r.returncode, r.stdout, r.stderr)
    assert not (tmp_path / "out" / "partial" / "matrix" / "att-1").exists(), r.stdout
    assert (tmp_path / "out" / "partial" / "matrix" / "att-3").exists(), "가장 최근 시도는 남는다"
    assert out.read_text(encoding="utf-8") == "canonical\n", "canonical 을 건드렸다"

    idx = json.loads((tmp_path / "out" / "partial" / "index.json").read_text(encoding="utf-8"))
    assert [e["attempt"] for e in idx["attempts"]] == ["att-3"], ("index 도 같이 정리돼야 한다", idx)


def test_r16_56_gc_refuses_when_the_index_and_the_disk_disagree(tmp_path):
    """[R16-56 · ④] index 와 디스크가 어긋나면 **지우지 않는다** — 모르는 상태에서 삭제하지 않는다.

    index 를 정본으로 삼아 지우는 도구가 index 밖의 디렉터리를 만나면, 그것은 이 도구가 모르는 무엇이다.
    지우고 나서 "몰랐다" 는 되돌릴 수 없다 (fail-closed).
    """
    out = tmp_path / "out" / "matrix_100.csv"
    out.parent.mkdir(parents=True)
    d = V.publish_target(out, "partial", run_id="att-1")
    d.write_text("x\n", encoding="utf-8")
    V.record_partial(out, d, status="partial", run_id="att-1")
    (tmp_path / "out" / "partial" / "matrix" / "몰래-생긴-시도").mkdir(parents=True)

    r = _gc("--root", tmp_path / "out", "--keep", 1, "--apply", cwd=ROOT)
    assert r.returncode == 2, (r.returncode, r.stdout, r.stderr)
    assert (tmp_path / "out" / "partial" / "matrix" / "몰래-생긴-시도").exists(), "모르는 것을 지웠다"
    assert "몰래-생긴-시도" in (r.stdout + r.stderr), (r.stdout, r.stderr)
