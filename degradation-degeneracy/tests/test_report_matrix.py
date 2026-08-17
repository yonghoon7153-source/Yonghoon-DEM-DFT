"""보고서 **문서 전체** characterization matrix.

★ 18차 Q4 방어 1층. 리뷰가 리팩터링(`P22RenderFacts`)보다 이것을 **먼저**
두라고 한 이유는 직접 증거가 있어서다 — paired 의 warm-start 인과 문장,
2종을 "4종" 이라 한 제목, 고정 boilerplate 재현 범위는 전부 helper 단위
테스트를 빠져나갔다. helper 는 옳은 값을 돌려주는데 **문서가 그 helper 를
그 조합에서 부르지 않았다**.

그래서 여기서는 helper 를 부르지 않는다. 완전한 artifact 조합에서 `build()` 로
문서를 통째로 만들고, 문서만 보고 검사한다.

검사 축 (리뷰 지정)
──────────────────
1. protocol 문구      warm/no-warm · adaptive/fixed 가 문장과 일치하는가
2. heading 수         `## 목적함수 N종 비교` 의 N 이 실제 표 행 수인가
3. emitted commands   렌더된 절과 명령이 서로를 함의하는가
4. 인용 범위          재현 범위 문구가 실제 출력 명령만 열거하는가
5. 금지 문구          철회된 주장이 **어느 조합에서도** 안 나오는가
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from tests.test_compare import (_complete_artifact, _fits, _hessian_run,
                                _scored, _wsweep_run)

OBJS = ("pocv_dvdq", "pocv_dvdq_dqdv")

#: 어느 조합에서도 나오면 안 되는 철회 명제 (claim id → 정규식)
FORBIDDEN = {
    "PRINCIPALLY_UNRECOVERABLE": re.compile(
        r"원리적으로\s*\*{0,2}\s*복원\s*불가|feasible domain"),
    "P22_ALL_EQUAL": re.compile(r"애초에\s*`?LAM_PE\s*=\s*LAM_NE"),
    "COLLAPSE_OBSERVABLE": re.compile(r"관측 가능한 범위"),
    "HESSIAN_EPS_ORDER": re.compile(r"같은\s*eps\s*에서의\s*\*{0,2}순서"),
    "SADDLE_ASSERTED": re.compile(r"최적점이 아니라\s*\*{0,2}안장점\*{0,2}에서"),
    "HESSIAN_COMMAND": re.compile(r"--mode hessian"),
}


def _set_protocol(run_dir: Path, *, adaptive: bool, warm: bool) -> None:
    """서명된 run_spec 의 optimizer protocol 을 바꾼다.

    (서명은 깨지므로 provenance 는 실패한다 — 이 matrix 가 보는 것은 **문구**이지
    초록 배지가 아니다. 배너 자체는 모든 조합에서 동일하게 뜬다.)
    """
    p = run_dir / "manifest.yaml"
    m = yaml.safe_load(p.read_text(encoding="utf-8"))
    m["run_spec"] = {**m["run_spec"], "warm_start": warm,
                     "optimizer": {**(m["run_spec"].get("optimizer") or {}),
                                   "adaptive": adaptive}}
    p.write_text(yaml.safe_dump(m, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")


def _widen_restarts(run_dir: Path) -> None:
    """무작위 restart 를 3개로 늘린다.

    ★ 이 fixture 를 처음 썼을 때 warm/no-warm 축이 **전혀 태워지지 않았다** —
    `_complete_artifact` 의 fits 에는 random restart 가 1개뿐이라
    `multistart_random_only` 블록(restart 0 을 뺀 뒤 2개 이상 필요)이 아예
    렌더되지 않았고, 그 절을 감싼 `if` 때문에 protocol 검사가 조용히 통과했다.
    뮤테이션(warm 인과를 무조건 출력)으로 잡아냈다.
    """
    import json

    import pandas as pd

    f = run_dir / "fits.parquet"
    df = pd.read_parquet(f)
    df["restarts_json"] = json.dumps(
        [{"p": [1.0, 0.0, 1.0, 0.0], "J": 0.0, "i": 0, "source": "base_init"},
         {"p": [1.1, 0.0, 1.1, 0.0], "J": 0.5, "i": 1, "source": "random"},
         {"p": [1.2, 0.0, 1.2, 0.0], "J": 0.5, "i": 2, "source": "random"},
         {"p": [1.3, 0.0, 1.3, 0.0], "J": 0.9, "i": 3, "source": "random"}])
    df.to_parquet(f, index=False)


def _render(tmp_path: Path, *, adaptive: bool, warm: bool, wsweep: bool,
            halfcell: bool, hessian: bool) -> str:
    """조합 하나를 완전한 문서로 렌더한다."""
    import pandas as pd

    from tools.compare_cases import compare
    from tools.compare_objectives import run_compare
    from tools.make_results import build

    d, _ = _complete_artifact(tmp_path / "main", objectives=OBJS)
    _set_protocol(d, adaptive=adaptive, warm=warm)
    _widen_restarts(d)

    # fits 에 없는 조건까지 렌더 경로를 태우려면 채점 map 이 필요하다
    _scored(pd.DataFrame(_fits(objectives=OBJS))).to_parquet(
        d / "degeneracy_map.parquet", index=False)

    if wsweep:
        _wsweep_run(d, optimizer={"adaptive": adaptive},
                    n_restarts=None if adaptive else 5)
    if hessian:
        _hessian_run(d, objectives=("pocv_dvdq",))
    if halfcell:
        h, _ = _complete_artifact(tmp_path / "hc", objectives=OBJS)
        res = compare(d / "fits.parquet", h / "fits.parquet")
        (d / "case_comparison.yaml").write_text(
            yaml.safe_dump(res, allow_unicode=True), encoding="utf-8")

    run_compare(d, d)
    return build(d, tmp_path / "R.md", repo_root=tmp_path).read_text(
        encoding="utf-8")


#: (id, adaptive, warm, wsweep, halfcell, hessian)
CASES = [
    ("main_adaptive_warm_full", True, True, True, True, True),
    ("paired_fixed_nowarm_bare", False, False, False, False, False),
    ("fixed_nowarm_with_sweep", False, False, True, False, False),
    ("adaptive_warm_hessian_only", True, True, False, False, True),
]


@pytest.fixture(scope="module")
def rendered(tmp_path_factory):
    """조합별 문서를 한 번씩만 만든다 (build 는 비싸다)."""
    out = {}
    for cid, adaptive, warm, ws, hc, hess in CASES:
        out[cid] = _render(tmp_path_factory.mktemp(cid), adaptive=adaptive,
                           warm=warm, wsweep=ws, halfcell=hc, hessian=hess)
    return out


@pytest.mark.parametrize("cid,adaptive,warm,ws,hc,hess", CASES)
def test_protocol_wording_matches_the_signed_run_spec(
        rendered, cid, adaptive, warm, ws, hc, hess):
    """축 1 — warm/no-warm · adaptive/fixed 문장이 run_spec 과 일치하는가.

    ★ 18차 발견 2 의 재발 방지. `multistart_random_only` 블록의 **존재**만 보고
    warm 전용 문장을 낸 것이 원인이었다 — 절이 렌더된 조합에서만 검사한다.
    """
    text = rendered[cid]

    if "무작위 restart끼리만" in text:
        if warm:
            assert "매끄러운 해를 초기값으로" in text, f"{cid}: warm 설명이 빠졌다"
        else:
            assert "매끄러운 해를 초기값으로" not in text, \
                f"{cid}: no-warm 인데 warm-start 인과를 설명한다"
            assert "base_init" in text, f"{cid}: no-warm 의 실제 초기값 설명이 없다"

    if "`agree_frac`과 `p_spread`는 인용하지 마세요" in text:
        if adaptive:
            assert "adaptive 조기 종료 때문에" in text, f"{cid}"
        else:
            assert "adaptive 조기 종료 때문에" not in text, \
                f"{cid}: 고정 예산 실행에 조기 종료 설명이 붙었다"


@pytest.mark.parametrize("cid", [c[0] for c in CASES])
def test_objective_heading_counts_the_rendered_rows(rendered, cid):
    """축 2 — 제목의 종수가 **표 행 수**와 같은가 (하드코딩 4 였다)."""
    text = rendered[cid]
    m = re.search(r"^## 목적함수 (\d+)종 비교$", text, re.M)
    assert m, f"{cid}: 목적함수 비교 절 제목이 없다"

    # 제목 다음의 **첫 표**만 센다 (사이에 설명 문단이 낀다). `### 전체 격자`
    # 이후는 다른 모집단 표이므로 경계로 삼는다.
    body = text[m.end():].split("\n### ")[0]
    rows = [ln for ln in body.splitlines()
            if ln.startswith("| ") and not ln.startswith("|---")
            and "objective |" not in ln]
    assert rows, f"{cid}: 제목 뒤에 표가 없다"
    assert int(m.group(1)) == len(rows), (
        f"{cid}: 제목 {m.group(1)}종 vs 표 {len(rows)}행")


@pytest.mark.parametrize("cid,adaptive,warm,ws,hc,hess", CASES)
def test_emitted_commands_and_rendered_sections_imply_each_other(
        rendered, cid, adaptive, warm, ws, hc, hess):
    """축 3 — 렌더된 절과 명령이 서로를 함의하는가.

    ★ 14차 2차 발견 4 의 일반화. 절은 있는데 명령이 없으면 재현이 문서와
    어긋나고, 명령만 있으면 독자가 없는 절을 기대한다.
    """
    text = rendered[cid]
    repro = text.split("## 재현")[1] if "## 재현" in text else ""

    has_sweep_sec = "weight sweep" in text or "가중치 sweep" in text
    has_sweep_cmd = "--mode wsweep" in repro
    if has_sweep_sec:
        assert has_sweep_cmd, f"{cid}: sweep 절은 있는데 명령이 없다"

    has_case_sec = "Case 1" in text
    has_case_cmd = "--compare" in repro
    assert has_case_sec == has_case_cmd, (
        f"{cid}: Case 절 {has_case_sec} vs --compare 명령 {has_case_cmd}")


@pytest.mark.parametrize("cid,adaptive,warm,ws,hc,hess", CASES)
def test_reproduction_scope_lists_only_what_was_emitted(
        rendered, cid, adaptive, warm, ws, hc, hess):
    """축 4 — ★ 18차 발견 4. 재현 범위가 고정 boilerplate 면 안 된다."""
    text = rendered[cid]
    assert "**재현 범위**" in text, f"{cid}: 재현 범위 문구가 없다"
    scope = text.split("**재현 범위**")[1].split("\n\n")[0]
    repro = text.split("## 재현")[1].split("**재현 범위**")[0]

    assert ("sweep" in scope) == ("--mode wsweep" in repro), (
        f"{cid}: 범위의 sweep 언급과 실제 명령이 다르다")
    assert ("half-cell" in scope) == ("--compare" in repro), (
        f"{cid}: 범위의 half-cell 언급과 실제 명령이 다르다")
    if hess:
        assert "Hessian 절 전체" in scope, (
            f"{cid}: Hessian 절이 있으면 명령 전체가 빠졌다고 말해야 한다")
        assert "비기본" not in scope, f"{cid}: 기본 eps 도 빠졌는데 비기본만 뺀 것처럼 쓴다"


@pytest.mark.parametrize("cid", [c[0] for c in CASES])
@pytest.mark.parametrize("claim", sorted(FORBIDDEN))
def test_retracted_claims_absent_in_every_combination(rendered, cid, claim):
    """축 5 — 철회된 주장이 **어느 조합에서도** 안 나오는가.

    ★ 16차 발견 4 / 17차 발견 3·6 / 18차 발견 1·7·10 의 재발 방지. 지금까지
    금지 문구 검사는 조합 하나(main)에서만 돌았다.
    """
    m = FORBIDDEN[claim].search(rendered[cid])
    assert not m, f"{cid}: 철회된 주장 [{claim}] 이 남아 있다 — {m.group(0)!r}"
