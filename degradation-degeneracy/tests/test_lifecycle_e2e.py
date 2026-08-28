"""49차 P0-3 — **정상 lifecycle 이 완주하는가** (process 경계를 진짜로 넘어서).

48차 리뷰가 NO-GO 를 낸 첫 번째 이유는 단위 시험이 잡지 못하는 자리에 있었다:

    정상 `run.sh --mode all --leg L` 은 grid 가 계획을 `running` 으로 바꾼
    직후 fit 의 사전검사에서 거부된다. shell 을 건너뛰어도 attempt 를 fit 에
    전달할 CLI/API 경로가 없다. production `grid → fit → finalize` 는
    완주할 수 없다.

두 규칙(claim 이 원장을 `running` 으로 옮긴다 · claim 이 있으면 소유 증명 없이
못 이어받는다)은 각각 단위 시험이 다 통과했다. 깨진 것은 **그 사이의 전달**
이고, 그것은 한 process 안에서는 보이지 않는다.

그래서 이 시험은 mock 을 쓰지 않는다. RUN_SCOPE 를 통째로 복사한 별도 tree 에
계획 원장을 심고, 진짜 `run.sh` 를 세 번 **따로** 띄워 grid → fit → finalize 를
돌린다. `DEFAULT_LEDGER` 는 `tools/preserve.py` 의 위치에서 유도되므로, tree 를
복사하면 원장 우회 통로를 새로 만들지 않고도 격리된다 (환경변수 우회를 두면
그것이 곧 gate 의 구멍이 된다).

느리다 (PyBaMM 2조건 + fit 1목적함수). `-m slow` 로 걸러 쓸 수 있다.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

#: RUN_SCOPE (`src/io.py::_SCOPE_DIRS` + file globs) 와 같은 목록. 이 tree 를
#: 바이트 그대로 복사하면 `source_digest()` 가 원본과 같은 값을 낸다.
_SCOPE = ("src", "tools", "configs", "scripts", "run.sh")

#: 2조건짜리 격자. `--mode all` 은 `--lli` 류를 하위로 넘기지 않으므로 축을
#: 줄이는 유일한 방법이 config 다.
_TINY_CONFIG = """\
extends: base.yaml

grid:
  lli:    {start: 0.0, stop: 0.05, step: 0.05}
  lam_pe: {start: 0.0, stop: 0.0,  step: 0.05, type: de}
  lam_ne: {start: 0.0, stop: 0.0,  step: 0.05, type: de}
  noise:  [0.0]

run:
  chunk_size: 50
  save_full_timeseries: false
"""

_LEG = "e2e49"
_OUT_REL = "results/e2e49"

#: 복사한 tree 안에서 계획 원장을 만드는 스크립트. **거기서** 돌아야 한다 —
#: `leg_out_key()` 와 `source_digest()` 가 그 tree 의 위치에서 유도되기 때문이다.
_MAKE_PLAN = r'''
import json, sys, hashlib, yaml
from pathlib import Path

from src.config import load_config
from src.grid import _cfg_digest, conditions_from_config, leg_out_key
from src.io import source_digest
from tools.preserve import leg_run_spec, run_spec_digest

leg, cfg_path, out_rel, objective = sys.argv[1:5]
root = Path(__file__).resolve().parent

cfg = load_config(cfg_path)
cfg.setdefault("grid", {})["noise_seed"] = int(cfg["grid"].get("noise_seed", 42))
conds = conditions_from_config(cfg, cli={
    "lli": None, "lam_pe": None, "lam_ne": None,
    "lam_pe_type": None, "lam_ne_type": None, "noise": None})
cond_ids = sorted(c.cond_id for c in conds)
grid_axis = {
    "config_digest": _cfg_digest(cfg),
    "condition_ids_sha256": hashlib.sha256(
        "\n".join(cond_ids).encode("utf-8")).hexdigest()[:16],
    "n_conditions": len(cond_ids),
    "out": leg_out_key(root / out_rel)}

ocfg = load_config("configs/objectives.yaml")
objectives = {objective: ocfg["objectives"][objective]}
fit_axis = {
    "config_digest": hashlib.sha256(
        json.dumps(ocfg, sort_keys=True, ensure_ascii=False,
                   default=str).encode("utf-8")).hexdigest()[:16],
    "objectives": sorted(objectives),
    "out": leg_out_key(root / out_rel)}

spec = leg_run_spec(leg, grid_axis, fit_axis)
doc = {
    "schema_version": 4,
    "cohorts": [{"cohort_id": "g49e", "dir": "docs/22p_gap/coh",
                 "status": "active", "legs": [], "prospective_legs": [leg],
                 "cross_leg_comparison": "allowed_within_cohort",
                 "pin": {"schema_version": 3,
                         "compute_sha256": "a" * 16,
                         "row_projection_py_sha256": "b" * 16,
                         "src_scoring_py_sha256": "c" * 16,
                         "analysis_spec_sha256": "d" * 16,
                         "producer_semantic_sha256": "e" * 16}}],
    "planned": [{"leg_id": leg, "cohort_id": "g49e", "status": "planned",
                 "authorization_kind": "prospective",
                 "authorized_source_digest": source_digest(),
                 "run_spec_digest": run_spec_digest(spec),
                 "run_spec": spec,
                 "recorded_on": "2026-08-28",
                 "근거": "49차 lifecycle e2e"}],
    "legs": []}
p = root / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False),
             encoding="utf-8")
print(json.dumps({"n_conditions": len(cond_ids),
                  "source_digest": source_digest()}))
'''

_READ_PLAN = r'''
import json, sys, yaml
from pathlib import Path
doc = yaml.safe_load((Path(__file__).resolve().parent / "docs" / "22p_gap"
                      / "LEG_PRESERVATION.yaml").read_text(encoding="utf-8"))
print(json.dumps({
    "planned": {e["leg_id"]: e["status"] for e in doc.get("planned") or []},
    "legs": {e["leg_id"]: {k: v for k, v in e.items() if k != "evidence"}
             for e in doc.get("legs") or []},
    "evidence": {e["leg_id"]: e.get("evidence") or {}
                 for e in doc.get("legs") or []},
    "cohorts": {c["cohort_id"]: {"legs": c.get("legs") or [],
                                 "prospective": c.get("prospective_legs") or []}
                for c in doc.get("cohorts") or []}}))
'''


@pytest.fixture(scope="module")
def tree():
    """RUN_SCOPE 를 바이트 그대로 복사한 격리 tree."""
    root = Path(tempfile.mkdtemp(prefix="dd49-e2e-"))
    for name in _SCOPE:
        src = REPO / name
        if src.is_dir():
            shutil.copytree(src, root / name,
                            ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy2(src, root / name)
    for g in REPO.glob("requirements*.txt"):      # RUN_SCOPE 의 file glob 그대로
        shutil.copy2(g, root / g.name)
    # 계약은 RUN_SCOPE 밖이지만 `candidate_modes()` 가 읽는다
    (root / "docs" / "22p_gap").mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO / "docs" / "22p_gap" / "STAGE3_CONTRACT.md",
                 root / "docs" / "22p_gap" / "STAGE3_CONTRACT.md")
    # 완방상태·반쪽셀 캐시는 재계산하면 몇 분이 더 든다 — 원본을 그대로 쓴다
    if (REPO / ".cache").is_dir():
        os.symlink(REPO / ".cache", root / ".cache")
    (root / "configs" / "_e2e49.yaml").write_text(_TINY_CONFIG, encoding="utf-8")
    yield root
    shutil.rmtree(root, ignore_errors=True)


def _run(root: Path, *args, expect_rc=0, timeout=900):
    env = dict(os.environ, PYTHONPATH=str(root), MPLBACKEND="Agg",
               CANONICAL_RUN="never_canonical_here")
    env.pop("LEG", None)
    env.pop("VIRTUAL_ENV", None)
    p = subprocess.run(["bash", str(root / "run.sh"), *args], cwd=root,
                       env=env, capture_output=True, text=True, timeout=timeout)
    if expect_rc is not None and p.returncode != expect_rc:
        raise AssertionError(
            f"run.sh {' '.join(args)} → rc={p.returncode} (기대 {expect_rc})\n"
            f"--- stdout ---\n{p.stdout[-4000:]}\n--- stderr ---\n{p.stderr[-4000:]}")
    return p


def _py(root: Path, script: str, *args) -> dict:
    f = root / "_probe.py"
    f.write_text(script, encoding="utf-8")
    p = subprocess.run([sys.executable, str(f), *args], cwd=root, text=True,
                       capture_output=True,
                       env=dict(os.environ, PYTHONPATH=str(root)))
    assert p.returncode == 0, f"probe 실패:\n{p.stdout}\n{p.stderr}"
    return json.loads(p.stdout.strip().splitlines()[-1])


@pytest.mark.slow
def test_grid_then_fit_then_finalize_completes_across_processes(tree):
    """★ 49차 P0-3 — 정상 lifecycle 이 **세 process 를 건너** 완주한다.

    48차 실측(리뷰어 probe): grid 가 계획을 `running` 으로 옮긴 직후 fit 이
    `"e2e49 은 이미 실행 중이다"` 로 거부됐다. 여기서 확인하는 것은 그 지점을
    지나 `executed` 까지 간다는 것 하나다.
    """
    root = tree
    made = _py(root, _MAKE_PLAN, _LEG, "configs/_e2e49.yaml", _OUT_REL, "pocv")
    assert made["n_conditions"] == 2, made

    tok = root / "results" / "_claims" / f"{_LEG}.token"

    # ── ① grid process — 실행권을 발급하고 소유 증명을 남긴다
    g = _run(root, "--mode", "grid", "--leg", _LEG,
             "--config", "configs/_e2e49.yaml", "--out", _OUT_REL,
             "--nproc", "2")
    assert "새 발급" in g.stdout, g.stdout
    assert tok.is_file(), "grid 가 소유 증명을 남기지 않았다 — fit 이 못 잇는다"
    assert (tok.stat().st_mode & 0o077) == 0, (
        f"소유 증명 파일이 남에게 열려 있다: {oct(tok.stat().st_mode)}")

    state = _py(root, _READ_PLAN)
    assert state["planned"][_LEG] == "running", state["planned"]

    # ── ② 난입 셋을 모두 막는다 (crash 뒤 두 번째 시작 방지)
    #   ②-a shell 을 건너뛰고 모듈을 직접 부른다 — 소유 증명이 아예 없다
    direct = subprocess.run(
        [sys.executable, "-m", "src.fitting", "--leg", _LEG,
         "--in", _OUT_REL, "--objective", "pocv", "--nproc", "2"],
        cwd=root, text=True, capture_output=True, timeout=900,
        env=dict(os.environ, PYTHONPATH=str(root), MPLBACKEND="Agg"))
    assert direct.returncode != 0, direct.stdout[-2000:]
    assert "이미 실행 중" in (direct.stdout + direct.stderr), (
        "모듈을 직접 부르면 소유 증명 없이도 들어간다 — gate 가 wrapper 에만 "
        "있는 것과 같다\n" + (direct.stdout + direct.stderr)[-2000:])

    #   ②-b **틀린** 소유 증명 — 파일은 있는데 내용이 다르다
    forged = root / "forged.token"
    forged.write_text("0" * 32 + "\n", encoding="utf-8")
    bad = _run(root, "--mode", "fit", "--leg", _LEG, "--in", _OUT_REL,
               "--attempt-file", str(forged),
               "--objective", "pocv", "--nproc", "2", expect_rc=1)
    assert "소유 증명이 맞지 않는다" in (bad.stdout + bad.stderr), (
        bad.stdout + bad.stderr)

    #   ②-c 없는 파일
    gone = _run(root, "--mode", "fit", "--leg", _LEG, "--in", _OUT_REL,
                "--attempt-file", str(root / "없는.token"),
                "--objective", "pocv", "--nproc", "2", expect_rc=1)
    assert "소유 증명 파일이 없다" in (gone.stdout + gone.stderr), (
        gone.stdout + gone.stderr)

    # ── ③ fit process — 넘겨받은 증명으로 **같은 실행**에 붙는다
    f = _run(root, "--mode", "fit", "--leg", _LEG, "--in", _OUT_REL,
             "--objective", "pocv", "--nproc", "2")
    assert "소유한 재개" in f.stdout, f.stdout

    # ── ④ finalize — 같은 증명으로 닫는다
    fin = _run(root, "--mode", "finalize", "--leg", _LEG, "--in", _OUT_REL)
    assert "실행 기록을 닫았다" in fin.stdout, fin.stdout
    assert not tok.exists(), "닫은 뒤에도 소유 증명이 남았다"

    state = _py(root, _READ_PLAN)
    assert state["planned"][_LEG] == "executed", state["planned"]
    rec = state["legs"][_LEG]
    assert rec["preservation_status"] == "preservation_pending", rec
    assert rec["validation_status"] == "unvalidated", rec
    # lifecycle 이 **실제로 남긴** 증거가 기록에 들어간다
    assert set(state["evidence"][_LEG]["phases"]) == {"grid", "fit"}, (
        state["evidence"][_LEG].get("phases"))
    coh = state["cohorts"]["g49e"]
    assert coh["legs"] == [_LEG] and coh["prospective"] == [], coh


@pytest.mark.slow
def test_a_released_leg_can_be_started_again(tree):
    """★ 49차 P0-3 — 중단된 실행권을 되돌리면 그 다리를 **다시** 시작할 수 있다.

    48차에는 이 방향이 없었다. 계산 도중 죽으면 계획은 `running` 이고 phase 는
    모자라 finalize 도 못 하므로, 그 다리는 영영 못 돌리는 상태로 굳었다.
    """
    root = tree
    leg = "e2e49b"
    out_rel = "results/e2e49b"
    _py(root, _MAKE_PLAN, leg, "configs/_e2e49.yaml", out_rel, "pocv")
    tok = root / "results" / "_claims" / f"{leg}.token"

    _run(root, "--mode", "grid", "--leg", leg,
         "--config", "configs/_e2e49.yaml", "--out", out_rel, "--nproc", "2")
    assert _py(root, _READ_PLAN)["planned"][leg] == "running"

    rel = _run(root, "--mode", "release", "--leg", leg)
    assert "되돌렸다" in rel.stdout, rel.stdout
    assert not tok.exists()
    assert _py(root, _READ_PLAN)["planned"][leg] == "planned"

    # 되돌림의 유일한 증명 — 다시 시작된다
    _run(root, "--mode", "grid", "--leg", leg, "--resume",
         "--config", "configs/_e2e49.yaml", "--out", out_rel, "--nproc", "2")
    assert _py(root, _READ_PLAN)["planned"][leg] == "running"
