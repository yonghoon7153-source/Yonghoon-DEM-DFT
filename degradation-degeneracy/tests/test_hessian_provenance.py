"""Hessian 의 입력 provenance 와 부작용 (★ 18차 A · A' · B).

세 결함을 고정한다.

A   분리 배치(producer 와 fit 이 다른 디렉터리)에서 `curves.parquet` 을 못 찾아
    `FileNotFoundError` 로 죽는다. v4 는 그 배치이므로 문서가 제시하던 재현
    명령이 애초에 돌지 않았다.
A'  half-cell 기준은 **live** `configs/base.yaml` 과 **live** `.cache` 를 읽는다.
    봉인된 입력이 있는데도 실행 시점 파일을 보므로, 그 사이 바뀌면 다른 기준
    곡선으로 곡률을 잰다.
B   `degeneracy_summary.yaml` 을 **덮어쓴다**. `score → hessian → report` 순서면
    보고서가 stale 로 판정된다 — 채점 산출물을 곡률 진단이 변이시키기 때문이다.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from tests.test_fitting import _tiny_curves


def _fit_run(tmp_path: Path, *, split: bool, reference: str = "grid") -> Path:
    """Hessian 을 태울 수 있는 최소 fit 디렉터리.

    `split=True` 면 곡선을 fit 디렉터리에 두지 않고 **봉인 스냅샷**
    (`_inputs/<digest12>_curves.parquet`)으로만 둔다 — v4 의 실제 배치다.
    """
    from src.io import file_digest

    prod = _tiny_curves(tmp_path / "prod")
    curves = Path(prod) / "curves.parquet" if not str(prod).endswith(".parquet") \
        else Path(prod)
    if not curves.exists():                       # helper 가 디렉터리를 주는 경우
        curves = Path(prod) / "curves.parquet"
    cdf = pd.read_parquet(curves)

    run = tmp_path / "fit"
    run.mkdir(parents=True, exist_ok=True)

    conds = sorted(cdf["cond_id"].unique())
    fits = pd.DataFrame([{
        "cond_id": c, "objective": "pocv_dvdq", "reference": reference,
        "noise": 0.0, "lli": 0.05, "lam_pe": 0.05, "lam_ne": 0.05,
        "a_pe": 1.0, "b_pe": 0.0, "a_ne": 1.0, "b_ne": 0.0,
    } for c in conds])
    fits.to_parquet(run / "fits.parquet", index=False)

    if split:
        snap = run / "_inputs"
        snap.mkdir(exist_ok=True)
        dig = file_digest(curves)
        (snap / f"{str(dig)[:12]}_curves.parquet").write_bytes(curves.read_bytes())
        sealed = {"results/prod/curves.parquet": dig}
    else:
        (run / "curves.parquet").write_bytes(curves.read_bytes())
        sealed = {}

    (run / "manifest.yaml").write_text(yaml.safe_dump(
        {"run_spec": {"sealed_inputs": sealed, "reference": reference}},
        allow_unicode=True), encoding="utf-8")
    (run / "degeneracy_summary.yaml").write_text(
        yaml.safe_dump({"n_rows": 3, "표시용": "채점 산출물"}, allow_unicode=True),
        encoding="utf-8")
    return run


def test_a_hessian_resolves_curves_from_the_sealed_snapshot(tmp_path):
    """★ A — 분리 배치에서 봉인 `_inputs` 곡선을 스스로 찾아야 한다."""
    from src.hessian import run_hessian

    run = _fit_run(tmp_path, split=True)
    assert not (run / "curves.parquet").exists(), "fixture 가 분리 배치가 아니다"

    s = run_hessian(run, n_sample=3)
    assert s["n"] >= 1, s


def test_a_hessian_accepts_an_explicit_curves_path(tmp_path):
    """★ A — `--curves` 로 명시할 수도 있어야 한다."""
    from src.hessian import run_hessian

    run = _fit_run(tmp_path, split=True)
    sealed = next((run / "_inputs").glob("*_curves.parquet"))

    s = run_hessian(run, n_sample=3, curves=sealed)
    assert s["n"] >= 1, s


def test_a_hessian_says_what_is_missing_when_it_cannot_resolve(tmp_path):
    """★ A — 못 찾으면 `FileNotFoundError` 가 아니라 무엇이 없는지 말해야 한다."""
    from src.hessian import run_hessian

    run = _fit_run(tmp_path, split=True)
    for p in (run / "_inputs").glob("*"):
        p.unlink()

    with pytest.raises(SystemExit, match="곡선"):
        run_hessian(run, n_sample=3)


def test_b_hessian_does_not_mutate_the_scoring_summary(tmp_path):
    """★ B — 곡률 진단이 채점 산출물을 변이시키면 안 된다.

    `score → hessian → report` 순서에서 보고서가 stale 로 찍히던 원인이다.
    """
    from src.hessian import run_hessian

    run = _fit_run(tmp_path, split=True)
    ds = run / "degeneracy_summary.yaml"
    before = ds.read_bytes()

    run_hessian(run, n_sample=3)

    assert ds.read_bytes() == before, "Hessian 이 degeneracy_summary.yaml 을 바꿨다"


def test_b_hessian_writes_its_own_sidecar(tmp_path):
    """★ B — 대신 자기 sidecar 에 쓴다 (인용 범위 밖임을 함께 적는다)."""
    from src.hessian import run_hessian

    run = _fit_run(tmp_path, split=True)
    run_hessian(run, n_sample=3)

    side = run / "hessian_summary.yaml"
    assert side.exists(), "hessian_summary.yaml 이 없다"
    doc = yaml.safe_load(side.read_text(encoding="utf-8"))
    assert "pocv_dvdq" in doc
    assert doc["pocv_dvdq"]["eps"] == pytest.approx(1e-4)
    assert "_주의" in doc


def test_b_sidecar_does_not_claim_eps_stable_ordering(tmp_path):
    """★ 18차 발견 7 — "같은 eps 에서 목적함수끼리 비교" 주장은 철회됐다."""
    from src.hessian import run_hessian

    run = _fit_run(tmp_path, split=True)
    run_hessian(run, n_sample=3)

    doc = yaml.safe_load((run / "hessian_summary.yaml").read_text(encoding="utf-8"))
    blob = json.dumps(doc, ensure_ascii=False)
    assert "같은 eps에서 목적함수끼리만" not in blob, blob


def test_aprime_halfcell_uses_the_sealed_config_and_cache(tmp_path, monkeypatch):
    """★ A' — half-cell 기준을 live 파일이 아니라 **봉인 입력**에서 만들어야 한다."""
    import src.hessian as H

    run = _fit_run(tmp_path, split=True, reference="halfcell")
    snap = run / "_inputs"
    # 봉인된 base.yaml 과 half-cell 캐시를 스냅샷에 놓는다
    (snap / "26fe6c7cc2a2_base.yaml").write_text("dummy: 1\n", encoding="utf-8")
    (snap / "aaaaaaaaaaaa_k_ocp_v.json").write_text("{}", encoding="utf-8")

    seen: dict = {}

    def spy(cfg, cache_dir=None, force=False, method="ocp", **kw):
        seen["cache_dir"] = cache_dir
        seen["cfg"] = cfg

        class _R:
            def as_dict(self):
                return {"x": [0.0, 1.0], "pe": [4.0, 3.0], "ne": [0.1, 0.2]}
        return _R()

    monkeypatch.setattr("src.halfcell.get_halfcell_reference", spy)

    # 더미 기준곡선이라 곡률 계산 자체는 실패할 수 있다 — 검사 대상은
    # **어떤 config·cache 로 기준을 만들었는가** 뿐이다.
    try:
        H.run_hessian(run, n_sample=3)
    except Exception:  # noqa: BLE001
        pass

    assert seen, "half-cell 기준 생성 자체가 호출되지 않았다"
    assert seen.get("cache_dir") is not None, \
        "half-cell 기준을 live cache 로 만들었다 (cache_dir 미지정)"
    assert "hessian_sealed_hc_" in str(seen["cache_dir"]), \
        f"봉인 스냅샷이 아닌 곳을 캐시로 썼다: {seen['cache_dir']}"
