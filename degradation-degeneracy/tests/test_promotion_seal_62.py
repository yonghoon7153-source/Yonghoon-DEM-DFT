"""62차 α′ (P0-1) — **승격 판정과 transition 조회를 가른다.**

리뷰어 판정문의 첫 문장: temporal seal 이 "등록된 실행의 고정 identity" 가
아니라 **현재 디렉터리에 우연히 남은, 과거에 등록된 prefix** 로 되돌아간다.

`[해석]` `_sealed_manifest_parts()` 는 낡은 봉인을 `None` 으로 돌려주고
`run_content_id()` 는 그때 **지금 있는 것**으로 identity 를 만든다 (60차가
cross-process e2e 를 살리려고 택한 규칙). 그리고 봉인은 자기가 담은 이름만
검증하므로, 봉인 뒤에 **더 생긴** 실행 manifest 는 보지 않는다 (61차가 grid →
fit 전이를 살리려고 택한 규칙). 두 규칙은 **전이**에는 옳다 — 다음 phase 의
gate 는 아직 아무것도 안 굳혔고, commit 이 다시 봉인한다. 그러나 **승격**에서
같은 규칙을 쓰면:

  · grid 가 굳힌 자리에서 fit 이 **진행 중**(manifest_start 만 있음)이거나
    죽었어도, 봉인은 grid 의 목록만 검증해 통과하고 → identity = grid 의 것 →
    canonical → 승격.
  · fit 이 굳힌 뒤 fit member 를 지우면 봉인이 낡아 무시되고 → 지금 있는 것
    = grid 의 목록 → grid 의 identity → canonical → 승격.
  · 봉인 파일 자체를 지워도 같은 길로 간다.

`[고침]` 승격 경로(`assert_not_smoke_provenance` → `resolve_execution_class(…,
for_promotion=True)`)는 **봉인이 지금 있는 실행 manifest 전부를 정확히 담고
바이트가 맞을 때만** identity 를 만든다. 낡았거나(stale) 모자라면(subset)
거부. 봉인 없이 등록된 legacy 레코드만 봉인 없는 승격을 허용하고, commit 이
만든 레코드는 `sealed: true` 를 달아 봉인 없이는 닿을 수 없게 한다.
전이 조회(`run_content_id`·`issue_execution_class`)는 그대로다.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import tools.preserve as P                                      # noqa: E402


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    led = tmp_path / "authority" / "LEG_PRESERVATION.yaml"
    led.parent.mkdir(parents=True)
    led.write_text("planned: []\nlegs: []\ncohorts: []\n", encoding="utf-8")
    monkeypatch.setattr(P, "canonical_ledger", lambda x=None: led)
    return led


def _grid_outputs(d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "curves_manifest_start.yaml").write_text("seed: 1\n", encoding="utf-8")
    (d / "curves_manifest.yaml").write_text("curves_sha256: aaaa\n",
                                            encoding="utf-8")


def _fit_starts(d: Path) -> None:
    """fit 이 **시작하며** 쓰는 것 — 아직 끝나지 않았다."""
    (d / "manifest_start.yaml").write_text("bounds: preset\n", encoding="utf-8")


def _fit_finishes(d: Path, tag: str = "first") -> None:
    (d / "manifest.yaml").write_text(f"fits_sha256: {tag}\n", encoding="utf-8")
    (d / "manifest_grid.yaml").write_text("curves_sha256: aaaa\n",
                                          encoding="utf-8")


def _commit(out: Path, ledger: Path, phase: str) -> None:
    cap = P.issue_execution_class(out, "L", phase, ledger=ledger)
    P.commit_run_outputs(cap, [out])


def _promote(out: Path) -> None:
    """production 승격 검사 그대로 — `archive_bundle bundle` · `make_results` 가
    부르는 문장. `dest=None` 은 "namespace 밖으로 나간다" 다."""
    P.assert_not_smoke_provenance([out], "보관 묶음")


# ── 진행 중 fit (subset seal) ──────────────────────────────────────────────
def test_an_in_progress_fit_in_a_committed_grid_dir_is_not_promotable(
        tmp_path, ledger):
    """★ P0-1 — grid 가 굳힌 자리에서 fit 이 시작만 했다. 봉인은 grid 의 목록만
    검증해 통과하고, 그 identity 는 canonical 로 등록돼 있다. 승격이 그것을
    받으면 **끝나지 않은 fit** 이 정본이 된다."""
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _commit(out, ledger, "grid")
    _fit_starts(out)                                   # 굳히지 않았다

    # 전이 조회는 그대로 살아 있어야 한다 (61차 α 의 성질)
    assert P.read_execution_class(P.run_content_id(out), ledger=ledger) \
        is not None, "전이 조회가 죽었다 — 그러면 cross-process e2e 가 죽는다"

    with pytest.raises(P.PreserveError, match="봉인"):
        _promote(out)


# ── fit member 삭제 (stale seal) ───────────────────────────────────────────
def test_deleting_fit_members_after_a_fit_commit_is_not_promotable(
        tmp_path, ledger):
    """★ P0-1 — fit 이 굳힌 뒤 fit member 를 지운다. 봉인은 낡았고, 지금 있는
    것은 grid 의 목록 = 과거에 등록된 grid identity. 그 prefix 로 되돌아가면
    "fit 이 지워진 상태" 가 canonical 이다."""
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _commit(out, ledger, "grid")
    _fit_starts(out)
    _fit_finishes(out)
    _commit(out, ledger, "fit")
    _promote(out)                                      # 온전한 상태는 승격된다

    for name in ("manifest.yaml", "manifest_start.yaml", "manifest_grid.yaml"):
        (out / name).unlink()

    with pytest.raises(P.PreserveError, match="봉인"):
        _promote(out)


def test_deleting_the_seal_does_not_reopen_the_prefix(tmp_path, ledger):
    """★ P0-1 — 봉인 파일까지 지우면 "봉인 없음" 이 되고 옛 규칙은 지금 있는
    것으로 identity 를 만들었다. commit 이 만든 레코드는 봉인과 함께 등록됐다는
    사실을 스스로 말해야 하고, 승격은 그것을 봉인 없이 받지 않는다."""
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _commit(out, ledger, "grid")
    _fit_starts(out)
    _fit_finishes(out)
    _commit(out, ledger, "fit")

    for name in ("manifest.yaml", "manifest_start.yaml", "manifest_grid.yaml",
                 P.RUN_SEAL_NAME):
        (out / name).unlink()

    with pytest.raises(P.PreserveError, match="봉인"):
        _promote(out)


# ── 양성 대조 — 가용성이 죽지 않았는가 ────────────────────────────────────
def test_a_complete_seal_still_promotes(tmp_path, ledger):
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _commit(out, ledger, "grid")
    _fit_starts(out)
    _fit_finishes(out)
    _commit(out, ledger, "fit")
    _promote(out)                                      # 예외 없음


def test_a_derived_refresh_after_the_commit_still_promotes(tmp_path, ledger):
    """61차 α 의 성질 — 파생 manifest 는 identity 밖이므로 승격도 안 흔든다."""
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _fit_starts(out)
    _fit_finishes(out)
    _commit(out, ledger, "fit")
    (out / "analysis_manifest.yaml").write_text("objectives: [x]\n",
                                                encoding="utf-8")
    _promote(out)
    (out / "analysis_manifest.yaml").write_text("objectives: [y]\n",
                                                encoding="utf-8")
    _promote(out)


def test_a_legacy_record_without_a_seal_still_promotes(tmp_path, ledger):
    """봉인 이전에 분류된 산출(legacy)은 봉인이 없다 — 그 레코드는 `sealed` 가
    아니므로 지금 있는 것으로 identity 를 만들고 승격된다."""
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _fit_starts(out)
    _fit_finishes(out)
    P._record_execution_class(out, P.EXEC_CLASS_CANONICAL,
                              evidence="시험이 흉내 낸 legacy 분류",
                              ledger=ledger)
    assert not (out / P.RUN_SEAL_NAME).exists()
    _promote(out)


def test_commit_records_say_they_were_sealed(tmp_path, ledger):
    out = tmp_path / "results" / "run"
    _grid_outputs(out)
    _commit(out, ledger, "grid")
    rec = P.read_execution_class(P.run_content_id(out), ledger=ledger)
    assert rec.get("sealed") is True, (
        f"commit 이 만든 레코드가 봉인 사실을 안 말한다: {rec}")
