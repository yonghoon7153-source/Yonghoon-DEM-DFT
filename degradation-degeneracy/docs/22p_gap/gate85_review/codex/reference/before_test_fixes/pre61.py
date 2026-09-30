"""61차 γ (P1-2·P1-3) — **증언의 키 공간과 실패 전파.**

리뷰어 반례 둘.

    P1-2  두 `PYTHONPATH` root 에 서로 다른 `same_name.py` 를 둬도
          `same_name_entry_count: 1`. root 순서를 뒤집으면 그 한 digest 가
          반대로 바뀐다:
              first_then_second: 683e0c976d318490
              second_then_first: dc4827e56cde2943

    P1-3  history 손자를 띄울 수 없는 **정상 측정 실패**를 만들어도 바깥
          child 는 rc 0 으로 끝나고 다음을 돌려준다:
              history_probe_failure_child_rc: 0
              history_after_measurement_failure: {"<unmeasured>": "1"}

`[해석]` 둘 다 같은 형태다 — **증언이 자기가 못 잰 것을 잰 것처럼 말한다.**

  · P1-2 는 **키가 손실적**이다. `reachable[basename]` 은 여러 root 를 한
    자리에 접어 넣고, 뒤 root 가 앞 root 를 덮는다. Python 의 import 는
    **앞 root 가 이긴다** — 즉 증언이 실제로 import 될 바이트의 반대를
    적는다. 그리고 순서가 사라지므로 순서를 바꾼 환경이 같은 값을 낸다.

  · P1-3 은 **실패가 성공 sentinel 이 된다.** child rc 를 안 보고, 해석
    실패를 안 세고, 예외를 정상 dict 로 바꾼다. 바깥 reader 는 JSON 이
    있으면 유효하게 받는다. 그러면 "환경을 쟀다" 는 주장이 "재려다 실패했다"
    와 구별되지 않는다 — 그것은 fail-closed 가 아니다.

`[고침]`

  · 키를 `"<검색 순서>/<이름>"` 으로 만든다. 같은 이름이 여러 root 에 있어도
    각각 남고, 순서를 바꾸면 값이 바뀐다. root 문자열 자체는 이미 영수증의
    `env.PYTHONPATH` 에 있으므로 여기서 두 번 담지 않는다.
  · 측정 결과를 **typed** 로 만든다: `{"status": "measured"|"failed", ...}`.
    rc·timeout·해석 실패·예외가 전부 `failed` 로 흐르고, 영수증을 받는 쪽이
    불완전하면 **거부한다.** 파일이 없는 builtin/frozen 은 실패가 아니라
    별도 상태(`unfiled`)로 센다.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO / "docs" / "22p_gap") not in sys.path:
    sys.path.insert(0, str(REPO / "docs" / "22p_gap"))


def _mr():
    import mutation_replay as mr

    return mr


def _facts(env_extra: dict, cwd: Path) -> dict:
    """탐침 본문을 그대로 돌려 `_env_facts` 를 한 번 잰다."""
    mr = _mr()
    src = mr._ENV_PROBE_BODY + (
        "\nimport json\n"
        f"print(json.dumps(_env_facts({mr._probe_names()!r}), "
        "sort_keys=True, ensure_ascii=False))\n")
    env = dict(os.environ)
    env.update(env_extra)
    r = subprocess.run([sys.executable, "-c", src], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


# ── P1-2 ──────────────────────────────────────────────────────────────────
@pytest.fixture
def two_roots(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "same_name.py").write_text("VALUE = 'IN_A'\n", encoding="utf-8")
    (b / "same_name.py").write_text("VALUE = 'IN_B'\n", encoding="utf-8")
    return a, b


def test_same_named_modules_in_two_roots_are_both_recorded(two_roots, tmp_path):
    """★ P1-2 — 두 root 의 동명 module 이 **둘 다** 남아야 한다.

    하나로 접히면 증언은 "이 자리에서 무엇이 import 될 수 있는가" 를 잘못
    답한다. Python 은 **앞 root** 를 고르는데, 접는 쪽은 뒤 root 로 덮는다.
    """
    a, b = two_roots
    got = _facts({"PYTHONPATH": os.pathsep.join([str(a), str(b)])}, tmp_path)
    roots = got["importable_roots"]
    hits = [k for k in roots if k.endswith("same_name.py")]
    assert len(hits) == 2, (
        f"두 root 의 동명 module 이 {len(hits)}개로 접혔다: {hits} — 뒤 root 가 "
        "앞 root 를 덮는다 (61차 P1-2)")
    assert len({roots[k] for k in hits}) == 2, (
        "두 항목이 같은 digest 다 — 여전히 한 파일만 봤다 (61차 P1-2)")


def test_the_receipt_says_which_root_python_would_import_from(two_roots,
                                                              tmp_path):
    """★ P1-2 — 증언에서 **실제로 import 될 바이트**를 되찾을 수 있어야 한다.

    "순서를 뒤집으면 값이 바뀐다" 만 물으면 안 된다 — 접는 구현도 그 시험은
    통과한다 (뒤 root 가 덮으므로 값이 바뀌긴 한다). 접는 구현이 틀린 이유는
    값이 안 바뀌어서가 아니라 **반대**를 적기 때문이다: Python 은 앞 root 를
    고르는데 그것은 뒤 root 를 적는다.

    그래서 검색 **첫 자리**의 항목을 집어 그것이 앞 root 의 바이트인지 본다.
    """
    import hashlib

    a, b = two_roots
    got = _facts({"PYTHONPATH": os.pathsep.join([str(a), str(b)])},
                 tmp_path)["importable_roots"]
    first = [k for k in got if k.startswith("0/") and k.endswith("same_name.py")]
    assert len(first) == 1, (
        f"검색 첫 자리의 항목을 못 찾겠다: {sorted(got)} — 키에 순서가 없다 "
        "(61차 P1-2)")
    # 탐침의 `_d()` 는 앞 16자리만 남긴다 — 같은 규칙으로 비교한다.
    want = hashlib.sha256((a / "same_name.py").read_bytes()).hexdigest()
    assert want.startswith(got[first[0]]) and got[first[0]], (
        "첫 자리 항목이 앞 root 의 바이트가 아니다 — 증언이 Python 의 검색 "
        "규칙과 반대를 적는다 (61차 P1-2)")


def test_a_single_root_still_records_its_modules(tmp_path):
    """★ 반대 방향 — 평범한 한 root 는 그대로 담긴다 (키만 바뀐다)."""
    d = tmp_path / "lib"
    d.mkdir()
    (d / "plain.py").write_text("VALUE = 1\n", encoding="utf-8")
    (d / "pkg").mkdir()
    (d / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    got = _facts({"PYTHONPATH": str(d)}, tmp_path)["importable_roots"]
    assert any(k.endswith("plain.py") for k in got), got
    assert any(k.endswith("pkg/__init__.py") for k in got), got


# ── P1-3 ──────────────────────────────────────────────────────────────────
def _history_of(env_extra: dict, cwd: Path) -> dict:
    return _facts(env_extra, cwd)["startup_history"]


def test_a_measured_history_says_so(tmp_path):
    """★ P1-3 — 정상 측정은 `measured` 라고 말한다 (형식이 typed 여야 한다)."""
    got = _history_of({}, tmp_path)
    assert isinstance(got, dict) and got.get("status") == "measured", got
    assert isinstance(got.get("modules"), dict) and got["modules"], got


def test_a_history_measurement_failure_is_not_a_success(tmp_path):
    """★ P1-3 — 손자를 못 띄우면 그 사실이 **영수증에 남아야** 한다.

    리뷰어는 history child 를 시작할 수 없는 정상 실패를 만들고도 바깥 child 가
    rc 0 으로 `{"<unmeasured>": "1"}` 을 돌려주는 것을 실측했다. 그 값은
    "쟀다" 와 형식이 같아서 읽는 쪽이 구별할 수 없다.

    여기서는 손자가 쓰는 인터프리터를 없는 경로로 바꿔 같은 실패를 만든다.
    """
    got = _history_of({"DD_HISTORY_PROBE_PYTHON": "/nonexistent/python"},
                      tmp_path)
    assert got.get("status") == "failed", (
        f"측정이 실패했는데 영수증이 성공처럼 보인다: {got} (61차 P1-3)")
    assert got.get("reason"), "왜 실패했는지가 없다"
    assert "<unmeasured>" not in json.dumps(got), (
        "실패를 정상 module 이름처럼 적었다 (61차 P1-3)")


def test_a_nonzero_history_child_is_a_failure(tmp_path):
    """★ P1-3 — child 의 **return code** 를 본다.

    예전 판은 rc 를 아예 안 봤다. rc 가 0 이 아닌데 stderr 가 파싱 가능하면
    부분 이력을 완전한 것처럼 담았다.

    ★ 이 자리를 겨누려면 **로그는 정상이고 rc 만 0 이 아닌** 손자가 필요하다.
      첫 판은 없는 flag 를 줬는데, 그러면 인터프리터가 시작도 못 해서 로그가
      비고 "이름을 하나도 해석 못 했다" 분기가 먼저 문다 — rc 규칙을 지워도
      안 빨개졌다 (실측). `exit(7)` 은 startup 을 다 마친 뒤 nonzero 로 끝나므로
      importtime 로그는 정상이고 rc 만 다르다.
    """
    got = _history_of({"DD_HISTORY_PROBE_ARGS": "-c exit(7)"}, tmp_path)
    assert got.get("status") == "failed", (
        f"손자가 nonzero 로 끝났는데 성공으로 적었다: {got} (61차 P1-3)")


def test_an_incomplete_receipt_is_refused_by_the_reader(tmp_path, monkeypatch):
    """★ P1-3 — 불완전한 영수증으로는 **증거를 만들 수 없다.**

    영수증에 실패가 적혀도 읽는 쪽이 그냥 받으면 층이 없는 것과 같다.
    """
    # ★ 62차 마감 — 영수증은 **그 항목만** 실패한 완전한 것이어야 한다. 최소
    #   dict 는 62차의 schema·부모 대조 층이 먼저 거부해 이 시험이 완전성
    #   reader 의 증인이 아니게 됐다 (12조각 재생 실측: 변이가 안 물었다).
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from receipt_fixture import full_receipt

    mr = _mr()
    bad = full_receipt()
    bad["startup"]["startup_history"] = {"status": "failed", "reason": "시험"}
    monkeypatch.setattr(mr, "_observed_receipt", lambda: bad)
    with pytest.raises(mr._ReplayError) as ei:
        mr._execution_receipt()
    assert "불완전" in str(ei.value) or "실패" in str(ei.value), str(ei.value)


def test_a_complete_receipt_is_accepted(tmp_path, monkeypatch):
    """★ 반대 방향 — 잰 영수증은 그대로 통과한다."""
    # ★ 62차 P2-1 — reader 가 재귀 exact schema 가 되면서 옛 최소 dict 는
    #   더 이상 "완전한 영수증" 이 아니다 (fixture 가 진실을 가리고 있었다).
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from receipt_fixture import full_receipt

    mr = _mr()
    ok = full_receipt()
    monkeypatch.setattr(mr, "_observed_receipt", lambda: ok)
    assert mr._execution_receipt() == ok


def test_modules_without_a_file_are_counted_not_failed(tmp_path):
    """★ P1-3 — builtin/frozen 은 **실패가 아니다.**

    파일이 없는 것은 정상이고, 그것을 실패로 세면 영수증이 언제나 실패다
    (거부가 넓어져 층이 마비된다 — 이 라운드에 이미 두 번 겪은 형태다).
    """
    got = _history_of({}, tmp_path)
    assert got["status"] == "measured"
    assert isinstance(got.get("unfiled"), int) and got["unfiled"] >= 0, got


def test_a_failed_package_listing_is_also_refused(monkeypatch):
    """★ P1-3 의 같은 형태 — **설치 목록 실패도** 성공 sentinel 이었다.

    리뷰어는 history 만 짚었지만 `packages` 는 실패를
    `{"<unavailable>": ""}` 라는 정상 dict 로 바꿨다. 규칙이 한 자리에 있지
    않으면 남은 중복이 곧 다음 반례다 — 이 저장소가 반복해서 겪은 형태다.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from receipt_fixture import full_receipt

    mr = _mr()
    bad = full_receipt(packages={"status": "failed", "reason": "시험"})
    monkeypatch.setattr(mr, "_observed_receipt", lambda: bad)
    with pytest.raises(mr._ReplayError):
        mr._execution_receipt()
