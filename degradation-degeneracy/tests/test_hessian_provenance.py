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
    # ★ 19차 심층 — 실제 봉인 캐시 이름 규칙을 써야 한다. 예전 fixture 는
    #   아무 이름이나 썼고, staging glob 이 넓어서 그래도 통과했다.
    _stem = "a8e262f7d6aa4beb_ocp_b5009f515fb8"
    (snap / f"636a425ace2d_{_stem}.json").write_text("{}", encoding="utf-8")
    (snap / f"116a14dcf77d_{_stem}.meta.yaml").write_text("r: 1\n", encoding="utf-8")

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


# ── 19차 심층 리뷰 자체 발견 — A' staging 이 너무 넓게 집는다 ────────────────

def test_aprime_staging_only_takes_halfcell_cache_files(tmp_path):
    """★ 19차 심층 — `*_*.json` 은 **아무 봉인 json** 이나 집는다.

    half-cell 캐시가 아닌 봉인 입력(json)이 하나라도 있으면 staging 이
    non-None 이 되어, 정작 캐시는 없는데도 "봉인 입력을 찾지 못했다" 경고가
    안 뜨고 조용히 캐시 미스로 **재계산**된다. 봉인 recipe 를 쓴다는 A' 의
    목적이 무너진다.
    """
    from src.hessian import _sealed_halfcell_staging

    run = _fit_run(tmp_path, split=True)
    snap = run / "_inputs"
    (snap / "abcdef012345_grid_spec.json").write_text("{}", encoding="utf-8")

    assert _sealed_halfcell_staging(run) is None, \
        "half-cell 캐시가 없는데 staging 을 만들었다"


def test_aprime_staging_picks_the_halfcell_cache_when_present(tmp_path):
    """★ 19차 심층 — 실제 캐시 이름(`<16hex>_<method>_<16hex>`)이면 집는다."""
    from src.hessian import _sealed_halfcell_staging

    run = _fit_run(tmp_path, split=True)
    snap = run / "_inputs"
    stem = "a8e262f7d6aa4beb_ocp_b5009f515fb8"
    (snap / f"636a425ace2d_{stem}.json").write_text("{}", encoding="utf-8")
    (snap / f"116a14dcf77d_{stem}.meta.yaml").write_text("r: 1\n", encoding="utf-8")
    (snap / "abcdef012345_grid_spec.json").write_text("{}", encoding="utf-8")

    staging = _sealed_halfcell_staging(run)
    assert staging is not None
    names = sorted(p.name for p in staging.iterdir())
    assert names == [f"{stem}.json", f"{stem}.meta.yaml"], names


def test_aprime_staging_matches_the_real_v4_artifact_names():
    """★ 19차 심층 — 이름 규칙이 **실제 v4 묶음**과 맞는지 직접 확인한다.

    fixture 이름만 맞추면 패턴이 현실과 어긋나도 통과한다. 묶음 안에서는
    평문 이름(`<baseline>_<method>_<recipe>.json`)이고, 복원되면 앞에
    `<digest12>_` 가 붙는다 — staging 패턴은 그 복원형을 본다. 여기서는
    **평문 부분**이 규칙과 맞는지 실물로 고정한다.
    """
    import re
    import subprocess

    root = Path(__file__).resolve().parent.parent
    listing = subprocess.run(
        ["git", "ls-files", "artifacts/halfcell_fit_v4"], cwd=root,
        capture_output=True, text=True, check=True).stdout.split()
    names = [Path(x).name for x in listing if "/inputs/" in x]
    if not names:
        pytest.skip("halfcell 묶음의 봉인 입력 목록을 찾지 못했다")

    stem = re.compile(r"^[0-9a-f]{8,32}_[a-z]+_[0-9a-f]{8,32}\.(json|meta\.yaml)$")
    hits = [n for n in names if stem.match(n)]
    assert hits, f"실제 묶음의 half-cell 캐시 이름이 규칙과 안 맞는다: {names}"

    # 복원형(`<digest12>_<평문>`)도 staging 패턴에 걸려야 한다
    from src.hessian import _sealed_halfcell_staging  # noqa: F401  (경로 확인용)
    restored = re.compile(r"^[0-9a-f]{12}_([0-9a-f]{8,32}_[a-z]+_[0-9a-f]{8,32})"
                          r"\.(json|meta\.yaml)$")
    for n in hits:
        assert restored.match("aabbccddeeff_" + n), n


# ── 봉인 recipe 를 staging 만 하고 조회는 기본 method 로 하던 구멍 ──────────
#
# ★ 13차 게이트 자체 리뷰(archive 렌즈)가 실측으로 잡았다. `run_hessian` 은
#   `get_halfcell_reference(cfg, cache_dir=_cache)` 를 **method 없이** 불러
#   항상 `_ocp_<recipe>` 경로를 찾는다. ocpbias 실행의 봉인 캐시는
#   `_ocpbias_<recipe>` 라 staging 에 정확히 복사돼 있는데도 **미스**가 되고,
#   캐시 미스는 예외 없이 조용히 재계산된다 — 즉 왜곡 실행의 곡률을 **무왜곡
#   기준으로** 잰다. staging 이 non-None 이라 A' 의 "봉인 입력을 찾지 못했다"
#   경고조차 안 뜬다.
#
#   실측 (ocpbias fit 산출물):
#     staging  : a8e262f7d6aa4beb_ocpbias_582189af471c.json
#     조회 경로: a8e262f7d6aa4beb_ocp_b5009f515fb8.json   존재? False

def test_aprime_reads_the_sealed_halfcell_recipe(tmp_path):
    """★ 봉인 manifest 의 recipe 에서 method·왜곡을 읽어와야 한다."""
    import yaml

    from src.hessian import _sealed_halfcell_recipe

    run = _fit_run(tmp_path, split=True)
    m = yaml.safe_load((run / "manifest.yaml").read_text(encoding="utf-8"))
    m.setdefault("run_spec", {})["halfcell_recipe"] = {
        "method": "ocpbias", "n_points": 400, "branch": "delithiation",
        "pe_offset_mv": 10.0, "ne_offset_mv": 0.0,
        "pe_stretch": 1.0, "ne_stretch": 1.0}
    (run / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    method, kw = _sealed_halfcell_recipe(run)
    assert method == "ocpbias", method
    assert kw["pe_offset_mv"] == 10.0, kw
    # method 는 recipe 의 키가 아니라 별도 축이다 — kw 에 섞이면 recipe_of 가 죽는다
    assert "method" not in kw, kw


def test_aprime_lookup_path_matches_the_staged_ocpbias_cache(tmp_path):
    """★ 조회 경로가 staging 에 **실제로 있는 파일**이어야 한다.

    이 테스트가 없으면 "staging 은 맞는데 조회는 딴 데" 를 아무도 못 잡는다.
    """
    import yaml

    from src.halfcell import halfcell_cache_path
    from src.hessian import _sealed_halfcell_recipe, _sealed_halfcell_staging

    run = _fit_run(tmp_path, split=True)
    m = yaml.safe_load((run / "manifest.yaml").read_text(encoding="utf-8"))
    m.setdefault("run_spec", {})["halfcell_recipe"] = {
        "method": "ocpbias", "n_points": 400, "branch": "delithiation",
        "pe_offset_mv": 10.0, "ne_offset_mv": 0.0,
        "pe_stretch": 1.0, "ne_stretch": 1.0}
    (run / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    from src.config import load_config
    cfg = load_config("configs/base.yaml")
    method, kw = _sealed_halfcell_recipe(run)
    want = halfcell_cache_path(cfg, None, method, **kw).name

    snap = run / "_inputs"
    (snap / f"636a425ace2d_{want}").write_text("{}", encoding="utf-8")
    (snap / f"116a14dcf77d_{want[:-5]}.meta.yaml").write_text("r: 1\n",
                                                              encoding="utf-8")
    staging = _sealed_halfcell_staging(run)
    assert staging is not None
    assert (staging / want).is_file(), \
        f"조회 경로 {want} 가 staging 에 없다: {sorted(p.name for p in staging.iterdir())}"


def test_aprime_passes_the_sealed_method_to_the_reference_builder(tmp_path,
                                                                  monkeypatch):
    """★ 변이 M55 로 발견 — 헬퍼·경로 테스트만으로는 **호출부**가 안 잡힌다.

    `_sealed_halfcell_recipe` 가 ocpbias 를 정확히 돌려줘도, 호출부가 그 값을
    `get_halfcell_reference` 에 안 넘기면 여전히 기본 ocp 경로를 찾는다.
    실제로 호출 인자를 가로채 고정한다.
    """
    import yaml

    import src.hessian as H

    run = _fit_run(tmp_path, split=True, reference="halfcell")
    snap = run / "_inputs"
    (snap / "26fe6c7cc2a2_base.yaml").write_text("dummy: 1\n", encoding="utf-8")
    _stem = "a8e262f7d6aa4beb_ocpbias_582189af471c"
    (snap / f"636a425ace2d_{_stem}.json").write_text("{}", encoding="utf-8")
    (snap / f"116a14dcf77d_{_stem}.meta.yaml").write_text("r: 1\n", encoding="utf-8")

    m = yaml.safe_load((run / "manifest.yaml").read_text(encoding="utf-8"))
    m.setdefault("run_spec", {})["halfcell_recipe"] = {
        "method": "ocpbias", "n_points": 400, "branch": "delithiation",
        "pe_offset_mv": 10.0, "ne_offset_mv": 0.0,
        "pe_stretch": 1.0, "ne_stretch": 1.0}
    (run / "manifest.yaml").write_text(yaml.safe_dump(m), encoding="utf-8")

    seen: dict = {}

    def spy(cfg, cache_dir=None, force=False, method="ocp", **kw):
        seen["method"] = method
        seen["kw"] = kw

        class _R:
            def as_dict(self):
                return {"x": [0.0, 1.0], "pe": [4.0, 3.0], "ne": [0.1, 0.2]}
        return _R()

    monkeypatch.setattr("src.halfcell.get_halfcell_reference", spy)
    try:
        H.run_hessian(run, n_sample=3)
    except Exception:  # noqa: BLE001
        pass

    assert seen, "half-cell 기준 생성 자체가 호출되지 않았다"
    assert seen["method"] == "ocpbias", \
        f"봉인 recipe 의 method 를 안 넘겼다 (넘긴 값: {seen['method']})"
    assert seen["kw"].get("pe_offset_mv") == 10.0, \
        f"왜곡 인자를 안 넘겼다: {seen['kw']}"
