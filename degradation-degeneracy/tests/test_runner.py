"""runner 테스트 — C2(전역 오염 없음) 검증.

slow: 동일 overrides 2회 실행 결과가 완전 일치해야 하며,
      사이에 다른 조건을 끼워도 오염되지 않아야 한다.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.curves import extract_curves
from src.modes import Baseline, single_mode_overrides
from src.runner import build_param, run_one


def test_build_param_is_fresh_each_time(cfg):
    """build_param은 매번 새 객체 — 한쪽을 변형해도 다른 쪽 불변 (병렬 안전의 전제)."""
    p1 = build_param(cfg)
    p2 = build_param(cfg)
    assert p1 is not p2
    key = "Negative electrode porosity"
    p1.update({key: 0.5})
    assert p2[key] == 0.25


def test_run_one_failure_is_isolated(cfg):
    """말이 안 되는 override로도 예외가 밖으로 새지 않고 error로 반환."""
    res = run_one(cfg, {"Negative electrode porosity": -1.0}, "charge_first")
    assert not res.ok
    assert res.error


@pytest.mark.slow
def test_no_global_pollution(cfg, baseline):
    """A → B(LLI=0.2) → A 순서 실행 시 A 두 번의 곡선이 완전 일치해야 한다.

    원본 코드에서 initialization() 누락 시 발생하던 오염(C2)의 회귀 테스트.
    """
    from src.baseline import get_discharged_state

    d = get_discharged_state(cfg)
    n_trim = cfg["postprocess"]["n_trim"]
    n_interp = cfg["postprocess"]["n_interp"]

    a1 = run_one(cfg, None, "charge_first")
    assert a1.ok, a1.error
    b = run_one(cfg, single_mode_overrides("lli", 0.2, baseline, d), "discharge_first")
    assert b.ok, b.error
    a2 = run_one(cfg, None, "charge_first")
    assert a2.ok, a2.error

    c1 = extract_curves(a1.solution, n_trim, n_interp)
    c2 = extract_curves(a2.solution, n_trim, n_interp)
    assert c1["q_mah"] == pytest.approx(c2["q_mah"], abs=1e-6)
    np.testing.assert_allclose(c1["v_full"], c2["v_full"], rtol=0, atol=1e-9)


# ── 18차 C — `run.sh --mode all` 의 옵션 전파 ────────────────────────────────

def _dry_all(tmp_path, *extra):
    """`--mode all` 이 만들 하위 명령을 실제 실행 없이 받아온다."""
    import os
    import subprocess
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    env = {**os.environ, "RUN_SH_DRY": "1"}
    r = subprocess.run(["bash", str(root / "run.sh"), "--mode", "all",
                        "--out", str(tmp_path / "o"), *extra],
                       cwd=root, capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    return [ln for ln in r.stdout.splitlines() if ln.startswith("--mode")]


def test_mode_all_propagates_the_fit_protocol_flags(tmp_path):
    """★ 18차 C — `all` 이 protocol 옵션을 하위 단계로 넘기지 않았다.

    `--objective`, `--n-restarts`, `--clean`, `--no-adaptive`, `--no-warm-start`
    를 주고 `all` 을 돌리면 **기본 protocol 로** fit 이 돌아, 사용자가 지정한
    것과 다른 실행이 나온다 — 그리고 그 사실이 아무 데도 안 적힌다.
    """
    lines = _dry_all(tmp_path, "--objective", "pocv_dvdq", "--n-restarts", "7",
                     "--clean", "--no-adaptive", "--no-warm-start")
    fit = [ln for ln in lines if ln.startswith("--mode fit")]
    assert fit, lines
    for flag in ("--objective pocv_dvdq", "--n-restarts 7", "--clean",
                 "--no-adaptive", "--no-warm-start"):
        assert flag in fit[0], f"`all` 이 {flag} 를 fit 으로 넘기지 않았다: {fit[0]}"


def test_mode_all_propagates_the_grid_axis_flags(tmp_path):
    """★ 18차 C — noise 축도 곡선 생성 단계로 넘어가야 한다."""
    lines = _dry_all(tmp_path, "--noise", "0,0.005", "--noise-seed", "7")
    grid = [ln for ln in lines if ln.startswith("--mode grid")]
    assert grid, lines
    assert "--noise 0,0.005" in grid[0], grid[0]
    assert "--noise-seed 7" in grid[0], grid[0]


def test_mode_all_does_not_run_hessian_in_the_default_chain(tmp_path):
    """★ 18차 발견 7 — Hessian 은 인용 범위 밖 부록이다.

    기본 체인에 넣으면 문서가 "재현 명령이 이 문서를 만든다" 고 말하면서
    실제로는 인용 불가 산출물까지 만든다.
    """
    lines = _dry_all(tmp_path)
    assert not any(ln.startswith("--mode hessian") for ln in lines), lines


def test_report_mode_does_not_overwrite_the_canonical_doc_from_a_scratch_run(tmp_path):
    """★ 18차 C 부수 발견 — `--mode report` 의 기본 출력이 커밋된 정본이다.

    이 회차에 실제로 당했다: 중단된 `--mode all` 테스트가 임시 디렉터리에서
    돌다가 report 단계에서 `docs/RESULTS.md` 를 scratch 수치로 덮어썼다.
    정본 경로(`results/…`)가 아닌 입력이면 정본에 쓰지 않아야 한다.
    """
    import os
    import subprocess
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    canon = root / "docs" / "RESULTS.md"
    before = canon.read_bytes() if canon.exists() else None

    scratch = tmp_path / "scratch_run"
    scratch.mkdir()
    r = subprocess.run(["bash", str(root / "run.sh"), "--mode", "report",
                        "--in", str(scratch)],
                       cwd=root, capture_output=True, text=True,
                       env={**os.environ})

    # 입력이 비어 있으므로 실패해도 좋다 — 검사 대상은 **정본을 건드렸는가** 다
    assert canon.read_bytes() == before if before is not None else True, (
        "scratch 실행이 커밋된 docs/RESULTS.md 를 덮어썼다\n" + r.stdout[-500:])
