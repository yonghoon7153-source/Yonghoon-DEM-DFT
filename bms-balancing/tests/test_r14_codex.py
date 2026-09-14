"""Codex R14 (대상 `1bb45b3`) — P2 세 건의 반례를 회귀로 고정한다.

리뷰어 스크립트(`reviews/r14_repros/codex/pkg/r14_nested_output_check.py` ·
`r14_env_schema_checks.py`)를 그대로 옮긴 것이다. 우리 코드를 고치기 전에 **먼저 실패를 봤다**.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from bms_balancing import schema as S          # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _prov():
    import importlib.util
    spec = importlib.util.spec_from_file_location("r14_provenance", ROOT / "scripts/provenance.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


# ── P2-1 ─────────────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("out_root,sibling,want_dirty", [
    ("out_alt", False, False),              # 얕은 OUT — 전 판도 맞았다 (test_g28 이 재는 것)
    ("reports/out_u18", False, False),      # ★ 중첩 OUT — 전 판은 True 였다 (Codex R14 P2-1)
    ("reports/out_u18", True, True),        # 중첩 OUT + 그 **밖** sibling — 계속 감지해야 한다
])
def test_h01_nested_output_root_is_not_code(tmp_path, out_root, sibling, want_dirty):
    """[Codex R14 P2-1] `git status --untracked-files=normal` 은 untracked 디렉터리를 상위 하나(`reports/`)로
    **접어서** 준다. 분류기는 그 상위가 지정 root(`reports/out_u18`) 안에 없으므로 **코드 변경**으로 셌다 —
    정상 산출 경로인데 `git_dirty: true`. 시작·끝에 같은 OUT 을 넘겨도(U18-02 의 고침) 이 축은 안 닫힌다.

    반례는 리뷰어 것 그대로: 새 합성 저장소에 README 만 commit 하고 산출 CSV 하나를 만든다.
    sibling 케이스는 **root 밖** 파일이므로 계속 dirty 여야 하고, 그때 `git_modified_code` 는 접힌
    `reports/` 가 아니라 **실제 파일**을 지목해야 한다 (접힌 이름은 무엇이 바뀌었는지 말하지 않는다).
    """
    fixture = tmp_path / "repo"; fixture.mkdir()

    def git(*argv):
        return subprocess.check_output(["git", *argv], cwd=fixture, text=True)

    git("init", "-q"); git("config", "user.name", "t"); git("config", "user.email", "t@t")
    (fixture / "README.txt").write_text("fixture\n", encoding="utf-8")
    git("add", "README.txt"); git("commit", "-qm", "base")

    art = fixture / out_root / "matrix_100.csv"
    art.parent.mkdir(parents=True)
    art.write_text("a,b\n1,2\n", encoding="utf-8")
    if sibling:
        (fixture / "reports/notes.txt").write_text("밖\n", encoding="utf-8")

    pv = _prov().git_provenance(cwd=str(fixture), artifact=str(art), output_roots=(out_root, "out"))
    assert pv["git_dirty"] is want_dirty, (out_root, sibling, pv)
    assert pv["git_modified_outputs"] == [], pv
    if not want_dirty:
        assert pv["git_modified_code"] == [], pv
    else:
        assert "reports/notes.txt" in pv["git_modified_code"], (
            "접힌 `reports/` 가 아니라 실제 파일을 지목해야 한다", pv)
        assert not any(c.rstrip("/") == "reports" for c in pv["git_modified_code"]), pv


# ── P2-2 ─────────────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("name", ["matrix_100.csv", "profile_gamma_100_Li.csv",
                                  "ne_shape_GITT_Li.csv", "degeneracy_100_Li.json"])
def test_h02_partial_env_in_a_new_sidecar_is_a_contract_violation(tmp_path, name):
    """[Codex R14 P2-2] sidecar 의 `env` 를 `{"python": …}` 하나만 남겨도 `--schema-only` 가 **rc 0** 이었다.
    검사가 "비어 있지 않은 dict 인가" 까지만 봤고, `ENV_KEYS` 다섯 축 검사는 **baseline 비교 경로**에만 있었다.

    그래서 U18-03 의 논리("새 산출의 환경 계약은 schema-only 가 독립적으로 강제한다")가 미완이었다.
    정본 bytes 는 건드리지 않고 사본에서 env 만 깎는다 — 과학 본문·sha256·receipt 는 그대로다.
    """
    src = ROOT / "out" / name
    if not src.is_file():
        pytest.skip(f"{name} 이 정본에 없다")
    d = tmp_path / "fix"; d.mkdir()
    data = src.read_bytes(); (d / name).write_bytes(data)
    meta = json.loads((src.with_name(name + ".meta.json")).read_text(encoding="utf-8"))
    full = dict(meta)

    def run(m):
        (d / (name + ".meta.json")).write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), "--new", str(d),
                            "--schema-only"], cwd=ROOT, capture_output=True, text=True, timeout=180)
        return r.returncode, r.stdout + r.stderr

    rc, out = run(full)
    assert rc == 0, ("대조군: 온전한 env 는 통과해야 한다", rc, out[-900:])
    assert isinstance(full.get("env"), dict) and set(S.ENV_KEYS) <= set(full["env"]), full.get("env")

    for k in S.ENV_KEYS:                                  # 한 축씩 빼도 전부 걸려야 한다
        partial = dict(full, env={x: v for x, v in full["env"].items() if x != k})
        rc, out = run(partial)
        assert rc == 2 and "env" in out, (f"{k} 를 뺐는데 통과했다", rc, out[-900:])

    only_python = dict(full, env={"python": full["env"]["python"]})   # 리뷰어 반례 그대로
    rc, out = run(only_python)
    assert rc == 2 and "env" in out, ("python 하나만 남겨도 통과했다 (R14 P2-2)", rc, out[-900:])

    rc, out = run({k: v for k, v in full.items() if k != "env"})      # 전부 없으면 원래도 rc 2
    assert rc == 2, (rc, out[-900:])
