"""62차 β′ (P0-3 · P1-2) · γ′ (P0-4 · P0-5) — production 진입점을 **끝까지** 태운다.

리뷰어 반례 셋 (전부 정상 production 순서다):

  P0-3   second_acquired_before_first_commit true
         first_commit_succeeded              true
         first_commit_sealed_second_writer   true
         → fit 은 lock 을 놓은 **뒤에** commit 한다. 그 사이 둘째가 같은
           manifest.yaml 을 바꾸면 첫 capability 가 둘째 bytes 를 canonical 로
           봉인한다. grid 는 더 넓다 — merge·manifest·commit 이 전부 lock 밖.

  P1-2   dry_run_returned true · new_live_capability_count 1 ·
         new_open_directory_fd_count 1
         → grid dry-run 과 fit 의 pre-commit 실패가 capability 와 fd 를 안
           버린다. production 에 `discard_execution_capability()` 호출자가 0.

  P0-4   manifest_grid_curves_parquet /proc/self/fd/3/curves.parquet ·
         path_exists_after_success false · manifest_grid_is_sealed true
         → grid 의 일반 `manifest.yaml` 이 handle 경로를 적고, fit 이 그것을
           `manifest_grid.yaml` 로 보존해 identity member 로 봉인한다.

  P0-5   first_run_signature 01b0d9e00f76 · second_run_signature 8d8a42b7766a
         same_logical_execution_has_same_signature false
         → 매번 새 `fit-stage-*` 경로가 run_spec 에 들어가 run_sig 가 바뀌고,
           정상 resume 가 자기 completed journal 을 못 찾는다.

`[고침]`
  · 순서: compute → merge → manifest → commit(seal·class) → phase receipt →
    **release**. lock 이 dirfd+inode token 이라 commit 이 fd 를 닫은 뒤에도
    놓을 수 있다 (61차 P1-1 이 commit 을 뒤로 옮긴 이유가 그것이었다).
  · commit 에 도달하지 못하는 **모든** 종료(dry-run · 예외)에서 capability 폐기.
  · grid 의 durable locator 는 `named_out` 기준. 서명에는 staged pathname 대신
    origin 의 논리 key 와 내용 digest.
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_fitting import _tiny_curves                           # noqa: E402

_OBJ_CFG = {"objectives": {}, "dqdv": {"window": 7, "polyorder": 2,
                                       "peak_weight": 1.0},
            "scaling": {"method": "reference_rmse"}}
_BOUNDS = {"init": [1.0, 0.0, 1.0, 0.0], "lb": [0.5, -1.0, 0.5, -1.0],
           "ub": [2.0, 1.0, 2.0, 1.0]}


def _live_caps() -> int:
    import tools.preserve as P
    return len(P._ISSUED_EXEC_CAPS)


def _open_dir_fds() -> int:
    n = 0
    for fd in os.listdir("/proc/self/fd"):
        try:
            if os.path.isdir(f"/proc/self/fd/{fd}"):
                n += 1
        except OSError:
            pass
    return n


# ── P0-3 ──────────────────────────────────────────────────────────────────
def test_fit_releases_the_lock_only_after_commit_and_receipt(tmp_path, monkeypatch):
    """★ P0-3 — 순서를 **관측**한다: commit 시점과 receipt 시점에 lock 이 아직
    잡혀 있어야 하고, release 는 그 둘 뒤여야 한다."""
    import src.fitting as F
    import src.io as io_mod
    import tools.preserve as P

    seq: list[str] = []
    real_commit = P.commit_run_outputs
    real_receipt = F._record_phase
    real_release = io_mod.release_run_lock

    def _lock_held(out: Path) -> bool:
        return (out / ".fit.lock").exists()

    out = tmp_path / "out"

    def _commit(cap, paths):
        seq.append("commit:" + ("held" if _lock_held(out) else "free"))
        return real_commit(cap, paths)

    def _receipt(claim, phase, summary, out_dir):
        seq.append("receipt:" + ("held" if _lock_held(out) else "free"))
        return real_receipt(claim, phase, summary, out_dir)

    def _release(tok, *a, **k):
        seq.append("release")
        return real_release(tok, *a, **k)

    # 입력 fixture(`sign_producer`)도 grid 쪽 권한으로 commit 한다 — 그 호출은
    # 관측 대상이 아니므로 spy 를 걸기 **전에** 만든다.
    in_dir = _tiny_curves(tmp_path / "in")
    monkeypatch.setattr(P, "commit_run_outputs", _commit)
    monkeypatch.setattr(F, "_record_phase", _receipt)
    monkeypatch.setattr(io_mod, "release_run_lock", _release)

    F.run_fit(in_dir, out, _OBJ_CFG, {"a": {"w_pocv": 1.0}}, _BOUNDS,
              "expanded", 1, nproc=1)
    assert seq == ["commit:held", "receipt:held", "release"], (
        f"fit 의 순서가 {seq} — commit·receipt 가 lock 안에 있고 release 가 "
        "마지막이어야 한다 (62차 P0-3)")
    assert not (out / ".fit.lock").exists()


def test_grid_source_releases_the_lock_after_merge_manifest_commit_and_receipt():
    """★ P0-3 (grid) — `run_grid` 안에서 `release_run_lock` 호출이 merge ·
    manifest · `write_curves_manifest`(commit) · `phase_done` **뒤**에 온다.

    grid 를 실제로 태우려면 solver 가 필요하므로 여기서는 **소스 순서**를 본다.
    실제 순서는 마감의 순서 전체 e2e 가 태운다.
    """
    import src.grid as G

    src = Path(G.__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == "run_grid")
    calls: dict[str, list[int]] = {}
    for n in ast.walk(fn):
        if isinstance(n, ast.Call):
            f = n.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
            if name:
                calls.setdefault(name, []).append(n.lineno)
    for needed in ("release_run_lock", "merge_chunks", "write_manifest",
                   "write_curves_manifest", "phase_done"):
        assert needed in calls, f"run_grid 에 {needed} 호출이 없다"
    # **첫** release 가 마지막 단계 뒤여야 한다 — `max` 로 재면 앞에 끼워 넣은
    # 조기 release 가 finally 의 것에 가려진다 (변이 축을 심다 실측).
    rel = min(calls["release_run_lock"])
    for before in ("merge_chunks", "write_manifest", "write_curves_manifest",
                   "phase_done"):
        assert max(calls[before]) < rel, (
            f"run_grid 가 {before}(line {max(calls[before])}) 보다 먼저 "
            f"lock 을 놓는다 (line {rel}) — 임계구역이 commit 을 못 덮는다 "
            "(62차 P0-3)")


# ── P1-2 ──────────────────────────────────────────────────────────────────
def test_fit_failure_before_commit_discards_the_capability(tmp_path, monkeypatch):
    """★ P1-2 — 계산이 죽으면 capability 와 그 dir fd 도 죽어야 한다."""
    import src.fitting as F

    def _boom(*a, **k):
        raise RuntimeError("시험이 만든 계산 실패")

    monkeypatch.setattr(F, "_run_fit_locked", _boom)
    n_caps, n_fds = _live_caps(), _open_dir_fds()
    in_dir = _tiny_curves(tmp_path / "in")
    with pytest.raises(RuntimeError, match="시험이 만든"):
        F.run_fit(in_dir, tmp_path / "out", _OBJ_CFG, {"a": {"w_pocv": 1.0}},
                  _BOUNDS, "expanded", 1, nproc=1)
    assert _live_caps() == n_caps, (
        f"실패한 fit 이 capability 를 살려 뒀다: {_live_caps()} vs {n_caps} "
        "(62차 P1-2)")
    assert _open_dir_fds() == n_fds, (
        f"실패한 fit 이 디렉터리 fd 를 열어 뒀다: {_open_dir_fds()} vs {n_fds}")
    assert not (tmp_path / "out" / ".fit.lock").exists()


def test_grid_dry_run_discards_the_capability(tmp_path, monkeypatch):
    """★ P1-2 — 리뷰어가 실제 empty dry-run 으로 잰 것을 그대로 고정한다:
    `new_live_capability_count 1 · new_open_directory_fd_count 1` 이 0 이어야."""
    from dataclasses import dataclass

    import src.grid as G

    @dataclass
    class _D:
        x: float = 0.0

    class _B:
        @staticmethod
        def from_config(cfg):
            return object()

    monkeypatch.setattr(G, "get_discharged_state", lambda cfg, **kw: _D())
    monkeypatch.setattr(G, "_discharged_kw", lambda cfg, claim: {})
    monkeypatch.setattr(G, "Baseline", _B)

    cfg = {"leg": "smoke-leg", "solver": "fake", "seed": 1,
           "postprocess": {"n_interp": 10}}
    out = tmp_path / "results" / "_smoke" / "grid_dry"
    n_caps, n_fds = _live_caps(), _open_dir_fds()
    s = G.run_grid(cfg, [], nproc=1, chunk_size=1, out_dir=out, dry_run=True)
    assert s.get("dry_run") is True
    assert _live_caps() == n_caps, (
        f"dry-run 이 capability 를 살려 뒀다: {_live_caps()} vs {n_caps} (62차 P1-2)")
    assert _open_dir_fds() == n_fds, (
        f"dry-run 이 디렉터리 fd 를 열어 뒀다: {_open_dir_fds()} vs {n_fds}")


# ── P0-4 ──────────────────────────────────────────────────────────────────
def test_grid_manifest_payload_records_the_logical_curves_path(tmp_path):
    """★ P0-4 — grid 의 `manifest.yaml` 이 적는 `curves_parquet` 은 **이름**
    (`named_out`) 기준이어야 한다. staged 경로를 받아도 그것을 안 적는다."""
    import src.grid as G

    named = tmp_path / "results" / "run"
    staged = Path("/proc/self/fd/3")
    payload = G._grid_manifest_payload(named, staged / "curves.parquet",
                                       n_ok=1, n_failed=0, n_done_total=1,
                                       n_failed_total=0, elapsed=1.0)
    got = payload["curves_parquet"]
    assert "/proc/self/fd/" not in got, f"handle 경로를 적었다: {got} (62차 P0-4)"
    assert Path(got) == named / "curves.parquet"


def test_grid_manifest_payload_with_no_merge_records_none(tmp_path):
    import src.grid as G
    payload = G._grid_manifest_payload(tmp_path, None, n_ok=0, n_failed=0,
                                       n_done_total=0, n_failed_total=0,
                                       elapsed=0.0)
    assert payload["curves_parquet"] is None


# ── P0-5 ──────────────────────────────────────────────────────────────────
def test_the_same_logical_fit_resumed_keeps_one_run_signature(tmp_path):
    """★ P0-5 — 같은 입력을 resume 하면 **같은 서명**이어야 한다. 서명이 매번
    바뀌면 completed journal 이 둘이 되고 resume 은 아무것도 재사용 못 한다."""
    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    objs = {"a": {"w_pocv": 1.0}}
    F.run_fit(in_dir, out, _OBJ_CFG, objs, _BOUNDS, "expanded", 1, nproc=1)
    F.run_fit(in_dir, out, _OBJ_CFG, objs, _BOUNDS, "expanded", 1, nproc=1,
              resume=True)
    journals = sorted(p.name for p in out.glob("fit_completed_*.jsonl"))
    assert len(journals) == 1, (
        f"같은 논리 실행이 서명을 {len(journals)} 개 만들었다: {journals} — "
        "random staging pathname 이 run_spec 에 들어갔다 (62차 P0-5)")


def test_the_run_spec_does_not_carry_a_staging_pathname(tmp_path):
    """★ P0-5 — 굳은 manifest 의 run_spec 에 `fit-stage-` 가 없어야 한다."""
    import yaml

    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    F.run_fit(in_dir, out, _OBJ_CFG, {"a": {"w_pocv": 1.0}}, _BOUNDS,
              "expanded", 1, nproc=1)
    body = (out / "manifest.yaml").read_text(encoding="utf-8")
    assert "fit-stage-" not in body, (
        "manifest 에 staging 경로가 굳었다 (62차 P0-5)")
    m = yaml.safe_load(body)
    spec = m.get("run_spec") or {}
    bc = str(spec.get("base_config", ""))
    assert "fit-stage-" not in bc and bc, f"run_spec.base_config = {bc!r}"


# ── 62차 자체 리뷰 (순서-TOCTOU 렌즈) — capability 는 lock **앞에서** 발행된다 ──
#
# 실측: lock 이 살아 있는 보유자에게 거부되거나, 발행과 lock 사이(입력 승인 ·
# discharged state · dry-run 표본 solve)에서 예외가 나면 `discard_capability_on_abort`
# 를 지나지 않아 capability 와 dir fd 가 남았다 (`live_caps 0→1 · open_dir_fds
# 0→1`). 리뷰어의 P1-2 계측을 둘째 contender 로 다시 재면 그대로 1/1 이다.
# "commit 에 도달하지 못한 **모든** 종료" 가 되려면 try 가 발행 직후에 열려야 한다.
_HOLDER = r"""
import sys, os
sys.path.insert(0, sys.argv[1])
from src.io import acquire_run_lock, release_run_lock
tok = acquire_run_lock(sys.argv[2], sys.argv[3])
print(os.getpid(), flush=True)
sys.stdin.readline()
release_run_lock(tok)
"""


def _hold(d: Path, name: str):
    import subprocess
    p = subprocess.Popen([sys.executable, "-c", _HOLDER, str(REPO), str(d), name],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    assert p.stdout.readline().strip().isdigit()
    return p


def _release(p) -> None:
    p.stdin.write("\n")
    p.stdin.flush()
    p.wait(timeout=20)


def test_fit_refused_by_a_live_lock_holder_discards_the_capability(tmp_path):
    import src.fitting as F

    in_dir = _tiny_curves(tmp_path / "in")
    out = tmp_path / "out"
    out.mkdir()
    p = _hold(out, ".fit.lock")
    n_caps, n_fds = _live_caps(), _open_dir_fds()
    try:
        with pytest.raises(RuntimeError, match="이미 실행 중"):
            F.run_fit(in_dir, out, _OBJ_CFG, {"a": {"w_pocv": 1.0}}, _BOUNDS,
                      "expanded", 1, nproc=1)
    finally:
        _release(p)
    assert (_live_caps(), _open_dir_fds()) == (n_caps, n_fds), (
        "lock 에 거부된 fit 이 capability/fd 를 살려 뒀다 (62차 자체 리뷰 F1)")


def test_fit_failure_before_the_lock_discards_the_capability(tmp_path, monkeypatch):
    import src.fitting as F

    def _boom(*a, **k):
        raise RuntimeError("시험이 만든 입력 승인 실패")

    monkeypatch.setattr(F, "_assert_fit_input_is_authorized", _boom)
    in_dir = _tiny_curves(tmp_path / "in")
    n_caps, n_fds = _live_caps(), _open_dir_fds()
    with pytest.raises(RuntimeError, match="시험이 만든"):
        F.run_fit(in_dir, tmp_path / "out", _OBJ_CFG, {"a": {"w_pocv": 1.0}},
                  _BOUNDS, "expanded", 1, nproc=1)
    assert (_live_caps(), _open_dir_fds()) == (n_caps, n_fds), (
        "lock 앞에서 죽은 fit 이 capability/fd 를 살려 뒀다 (62차 자체 리뷰 F1)")


def _grid_mocks(monkeypatch, discharged):
    import src.grid as G

    class _B:
        @staticmethod
        def from_config(cfg):
            return object()

    monkeypatch.setattr(G, "get_discharged_state", discharged)
    monkeypatch.setattr(G, "_discharged_kw", lambda cfg, claim: {})
    monkeypatch.setattr(G, "Baseline", _B)
    return G


_CFG = {"leg": "smoke-leg", "solver": "fake", "seed": 1,
        "postprocess": {"n_interp": 10}}


@pytest.mark.parametrize("dry_run", [False, True])
def test_grid_failure_before_the_lock_discards_the_capability(tmp_path, monkeypatch,
                                                              dry_run):
    def _boom(cfg, **kw):
        raise RuntimeError("시험이 만든 완방상태 실패")

    G = _grid_mocks(monkeypatch, _boom)
    out = tmp_path / "results" / "_smoke" / "grid_pre"
    n_caps, n_fds = _live_caps(), _open_dir_fds()
    with pytest.raises(RuntimeError, match="시험이 만든"):
        G.run_grid(_CFG, [], nproc=1, chunk_size=1, out_dir=out, dry_run=dry_run)
    assert (_live_caps(), _open_dir_fds()) == (n_caps, n_fds), (
        f"lock 앞에서 죽은 grid(dry_run={dry_run}) 가 capability/fd 를 살려 뒀다 "
        "(62차 자체 리뷰 F1)")


def test_grid_refused_by_a_live_lock_holder_discards_the_capability(tmp_path,
                                                                    monkeypatch):
    from dataclasses import dataclass

    @dataclass
    class _D:
        x: float = 0.0

    G = _grid_mocks(monkeypatch, lambda cfg, **kw: _D())
    out = tmp_path / "results" / "_smoke" / "grid_held"
    out.mkdir(parents=True)
    p = _hold(out, ".run.lock")
    n_caps, n_fds = _live_caps(), _open_dir_fds()
    try:
        with pytest.raises(RuntimeError, match="이미 실행 중"):
            G.run_grid(_CFG, [], nproc=1, chunk_size=1, out_dir=out)
    finally:
        _release(p)
    assert (_live_caps(), _open_dir_fds()) == (n_caps, n_fds), (
        "lock 에 거부된 grid 가 capability/fd 를 살려 뒀다 (62차 자체 리뷰 F1)")
