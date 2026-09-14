"""62차 ζ′ (P0-8) — **파생 freshness 는 승격 primitive 안에 있다.**

리뷰어: `python -m tools.archive_bundle bundle <run> <out>` 을 직접 부르면
`scripts/archive_results.sh:124-138` 의 `check_derived_fresh` 를 지나지 않는다.
검사가 shell wrapper 에만 있으면 wrapper 를 안 쓰는 호출이 그대로 우회로다
(48차 P0-8 이 smoke 승격 금지에서 낸 것과 같은 결론 — "면제와 승격 금지는
같은 경계여야 한다").

`[고침]` `tools.preserve.assert_promotable()` 이 smoke 판정 **과** 파생
freshness 를 한 자리에서 한다. `archive_bundle.main` 의 `bundle` 은 그것을
지난다. shell wrapper 의 검사는 남긴다 (중복은 비용이고 우회로는 구멍이다).
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


def _committed_fit_run(d: Path, ledger: Path) -> Path:
    d.mkdir(parents=True, exist_ok=True)
    (d / "curves_manifest_start.yaml").write_text("seed: 1\n", encoding="utf-8")
    (d / "curves_manifest.yaml").write_text("curves_sha256: aaaa\n",
                                            encoding="utf-8")
    (d / "manifest_start.yaml").write_text("bounds: preset\n", encoding="utf-8")
    (d / "manifest.yaml").write_text("fits_sha256: first\n", encoding="utf-8")
    (d / "objective_comparison.yaml").write_text("n: 1\n", encoding="utf-8")
    cap = P.issue_execution_class(d, "L", "fit", ledger=ledger)
    P.commit_run_outputs(cap, [d])
    return d


def test_direct_bundle_refuses_a_stale_derived_artifact(tmp_path, ledger,
                                                        monkeypatch):
    """★ P0-8 — wrapper 없이 `archive_bundle.main(["bundle", …])` 을 불러도
    stale 파생은 **묶이지 않는다**."""
    import tools.archive_bundle as AB
    import tools.compare_objectives as CO

    run = _committed_fit_run(tmp_path / "results" / "run", ledger)
    monkeypatch.setattr(CO, "verify_derived_freshness",
                        lambda run_dir, tol=0.02: {"ok": False,
                                                   "fail": ["시험이 만든 stale"]})
    calls: list = []
    monkeypatch.setattr(AB, "bundle",
                        lambda *a, **k: calls.append(a) or {
                            "copied": 0, "external": [], "missing": [],
                            "nested": []})
    out = tmp_path / "artifacts" / "run"
    with pytest.raises(P.PreserveError, match="stale|파생|freshness"):
        AB.main(["bundle", str(run), str(out)])
    assert calls == [], "stale 파생인데 bundle 이 불렸다 (62차 P0-8)"


def test_direct_bundle_proceeds_when_derived_is_fresh(tmp_path, ledger,
                                                      monkeypatch):
    import tools.archive_bundle as AB
    import tools.compare_objectives as CO

    run = _committed_fit_run(tmp_path / "results" / "run", ledger)
    monkeypatch.setattr(CO, "verify_derived_freshness",
                        lambda run_dir, tol=0.02: {"ok": True, "fail": []})
    calls: list = []
    monkeypatch.setattr(AB, "bundle",
                        lambda *a, **k: calls.append(a) or {
                            "copied": 1, "external": [], "missing": [],
                            "nested": []})
    out = tmp_path / "artifacts" / "run"
    assert AB.main(["bundle", str(run), str(out)]) == 0
    assert len(calls) == 1


def test_a_run_without_derived_artifacts_is_not_gated_on_freshness(
        tmp_path, ledger, monkeypatch):
    """곡선 producer 처럼 파생이 없는 run 은 이 게이트 대상이 아니다 (wrapper 의
    `check_derived_fresh` 와 같은 규칙)."""
    import tools.archive_bundle as AB
    import tools.compare_objectives as CO

    run = _committed_fit_run(tmp_path / "results" / "run", ledger)
    (run / "objective_comparison.yaml").unlink()
    # 봉인은 identity member 만 담으므로 파생 파일 삭제는 identity 를 안 흔든다
    monkeypatch.setattr(CO, "verify_derived_freshness",
                        lambda *a, **k: (_ for _ in ()).throw(
                            AssertionError("파생이 없는데 freshness 를 쟀다")))
    monkeypatch.setattr(AB, "bundle",
                        lambda *a, **k: {"copied": 1, "external": [],
                                         "missing": [], "nested": []})
    assert AB.main(["bundle", str(run), str(tmp_path / "artifacts" / "r")]) == 0


def test_the_promotion_primitive_is_one_function():
    """`archive_bundle.main` 의 bundle 분기가 smoke 판정과 freshness 를 **따로**
    부르지 않고 한 primitive 를 지난다 — 두 검사가 갈리면 하나가 또 빠진다."""
    import ast

    import tools.archive_bundle as AB

    src = Path(AB.__file__).read_text(encoding="utf-8")
    fn = next(n for n in ast.walk(ast.parse(src))
              if isinstance(n, ast.FunctionDef) and n.name == "main")
    names = {(n.func.attr if isinstance(n.func, ast.Attribute)
              else getattr(n.func, "id", None))
             for n in ast.walk(fn) if isinstance(n, ast.Call)}
    assert "assert_promotable" in names, (
        "archive_bundle.main 이 assert_promotable() 을 안 지난다 (62차 P0-8)")
    assert "assert_not_smoke_provenance" not in names, (
        "smoke 판정을 primitive 밖에서 따로 부른다 — 두 검사가 갈린다")
