"""63차 — 방어적 검토 F1~F4 · 증거 공백 E1·E2.

리뷰어의 `test_gate62_defensive_contracts.py` 7건을 이 저장소 경로로 옮겨
**그대로** 고정한다 (모의 자원 · 무해한 입력 · 우회 재현물 없음). 그 위에
F2 의 정상 사례(정상 선택적 import 실패) 와 E1 의 3.11 합성 AST 판, E2 의
실제 planned lifecycle 관측을 더한다.

  F1  두 lock 의 부분 취득·해제 오류를 정리하지 못한다 (list comprehension 뒤
      try · finally 의 단순 for).
  F2  `-X importtime` 의 이름을 성공한 import 로 취급 → `site` 의 실패한
      선택적 import 를 "올렸다 지운 module" 로 오분류 → 정상 환경이 failed.
  F3  부모 customization 탐색이 package(`sitecustomize/__init__.py`)를 안 본다.
  F4  `_HEX16` 을 `re.match` + `$` 로 검사 → 후행 LF 17자 통과.
  E1  3.12 `type_params` 의 bound 가 scoped walker 밖.
  E2  "receipt 까지 held" 시험이 경로 exists 와 smoke namespace 위의 관측이라
      실제 planned phase 기록 중 커널 배타를 본 적이 없다.
"""
from __future__ import annotations

import ast
import fcntl
import hashlib
import importlib.machinery
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
if str(REPO / "docs" / "22p_gap") not in sys.path:
    sys.path.insert(0, str(REPO / "docs" / "22p_gap"))
sys.path.insert(0, str(Path(__file__).resolve().parent))


# ── F1 ──────────────────────────────────────────────────────────────────────
def test_partial_archive_acquisition_releases_prior_mock_resource(monkeypatch):
    """★ F1-a (리뷰어 원문) — 둘째 acquire 가 실패하면 이미 얻은 첫 자원을
    해제한 뒤 오류를 전달해야 한다."""
    import src.io as io
    import tools.archive_bundle as ab
    first = object()
    acquired, released = [], []

    def acquire(path, name):
        acquired.append(name)
        if len(acquired) == 2:
            raise RuntimeError("ordinary second resource busy")
        return first

    monkeypatch.setattr(io, "acquire_run_lock", acquire)
    monkeypatch.setattr(io, "release_run_lock", released.append)
    with pytest.raises(RuntimeError, match="ordinary second resource busy"):
        ab.main(["bundle", "unused-source", "unused-destination"])
    assert released == [first], (
        "first acquired resource was not released after second acquisition failed")


def test_archive_cleanup_attempts_every_mock_release(monkeypatch):
    """★ F1-b (리뷰어 원문) — 첫 release 가 OSError 를 내도 둘째 자원의 해제를
    반드시 시도한다."""
    import src.io as io
    import tools.archive_bundle as ab
    import tools.preserve as preserve
    first, second = object(), object()
    tokens = iter([first, second])
    released = []

    def release(token):
        released.append(token)
        if token is first:
            raise OSError("ordinary first cleanup failure")

    monkeypatch.setattr(io, "acquire_run_lock", lambda *args: next(tokens))
    monkeypatch.setattr(io, "release_run_lock", release)
    monkeypatch.setattr(preserve, "assert_promotable", lambda *args, **kw: None)
    monkeypatch.setattr(ab, "bundle", lambda *args: {"copied": 0, "nested": [],
                                                    "external": [], "missing": []})
    with pytest.raises(OSError, match="ordinary first cleanup failure"):
        ab.main(["bundle", "unused-source", "unused-destination"])
    assert released == [first, second], (
        "a cleanup exception prevented release of the second resource")


def test_archive_body_error_survives_a_cleanup_error(monkeypatch):
    """★ F1-c — 본문(승격 판정)이 올린 오류가 정리 중 오류에 **덮이지 않는다**.
    둘 다 시도하고, 원래 오류가 전달된다."""
    import src.io as io
    import tools.archive_bundle as ab
    import tools.preserve as preserve
    first, second = "tok-first", "tok-second"        # repr 이 결정적이어야 증인이 된다
    tokens = iter([first, second])
    released = []

    def release(token):
        released.append(token)
        if token is first:
            raise OSError("ordinary first cleanup failure")

    monkeypatch.setattr(io, "acquire_run_lock", lambda *args: next(tokens))
    monkeypatch.setattr(io, "release_run_lock", release)

    def _refuse(*args, **kw):
        raise preserve.PreserveError("promote", "ordinary promotion refusal")

    monkeypatch.setattr(preserve, "assert_promotable", _refuse)
    with pytest.raises(preserve.PreserveError, match="ordinary promotion refusal"):
        ab.main(["bundle", "unused-source", "unused-destination"])
    assert released == [first, second], (
        f"본문 오류 뒤 정리가 {len(released)}개만 시도됐다 (기대 2) — 63차 F1")


# ── F3 ──────────────────────────────────────────────────────────────────────
def test_parent_customization_lookup_supports_a_normal_package(tmp_path, monkeypatch):
    """★ F3 (리뷰어 원문) — 앞선 PYTHONPATH 의 `sitecustomize/__init__.py`
    package 를 Python 은 찾는다. 부모 측 함수도 같은 바이트를 돌려줘야 한다."""
    import mutation_replay as mr
    package = tmp_path / "sitecustomize"
    package.mkdir()
    init = package / "__init__.py"
    init.write_text("# Empty, valid customization package.\n", encoding="utf-8")
    spec = importlib.machinery.PathFinder.find_spec("sitecustomize", [str(tmp_path)])
    assert spec is not None and Path(spec.origin) == init
    monkeypatch.setattr(mr, "replay_env", lambda: {"PYTHONPATH": str(tmp_path)})
    view = mr._parent_customization_view()
    expected = hashlib.sha256(init.read_bytes()).hexdigest()[:16]
    assert view["sitecustomize"] == expected, (
        "parent lookup disagrees with Python on an ordinary package")


def test_parent_customization_lookup_prefers_the_earlier_path_entry(tmp_path, monkeypatch):
    """F3 대조군 — 앞 root 의 `.py` 와 뒤 root 의 package 가 같이 있으면 Python
    처럼 **앞 것**이다."""
    import mutation_replay as mr
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    (a / "sitecustomize.py").write_text("A = 1\n", encoding="utf-8")
    (b / "sitecustomize").mkdir()
    (b / "sitecustomize" / "__init__.py").write_text("B = 1\n", encoding="utf-8")
    monkeypatch.setattr(mr, "replay_env",
                        lambda: {"PYTHONPATH": os.pathsep.join([str(a), str(b)])})
    view = mr._parent_customization_view()
    assert view["sitecustomize"] == hashlib.sha256(
        (a / "sitecustomize.py").read_bytes()).hexdigest()[:16]


# ── F4 ──────────────────────────────────────────────────────────────────────
def test_hex16_scalar_does_not_accept_a_trailing_newline():
    """★ F4 (리뷰어 원문)"""
    import mutation_replay as mr
    value = "0123456789abcdef\n"
    assert len(value) == 17
    error = mr._schema_mismatch(value, mr._HEX16, "digest")
    assert error is not None, "hex16 scalar validator accepted a 17-character string"


def test_hex16_scalar_positive_control():
    import mutation_replay as mr
    assert mr._schema_mismatch("0123456789abcdef", mr._HEX16, "digest") is None


@pytest.mark.parametrize("bad", ["0123456789abcdef\r\n", "0123456789abcdef ",
                                 " 0123456789abcdef", "0123456789ABCDEF",
                                 "0123456789abcde", "0123456789abcdef0"])
def test_hex16_scalar_refuses_other_near_misses(bad):
    import mutation_replay as mr
    assert mr._schema_mismatch(bad, mr._HEX16, "digest") is not None, repr(bad)


# ── F2 ──────────────────────────────────────────────────────────────────────
def _receipt_in(env_extra: dict, cwd: Path) -> dict:
    """탐침 본문을 그대로 돌려 `_receipt_facts` 를 한 번 잰다 (frame 없이)."""
    import mutation_replay as mr
    src = mr._ENV_PROBE_BODY + (
        "\nimport json\n"
        f"print(json.dumps(_receipt_facts({mr._probe_names()!r}, [], "
        f"{str(cwd)!r}), sort_keys=True, ensure_ascii=False))\n")
    env = dict(os.environ)
    env.update(env_extra)
    r = subprocess.run([sys.executable, "-c", src], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_an_ordinary_failed_optional_import_keeps_startup_measured(tmp_path):
    """★ F2 (리뷰어 발견의 재현) — `site` 계열 코드가 `try: import X / except
    ImportError: pass` 를 하면 importtime 에는 X 가 남지만 X 는 올라온 적이
    없다. 그것을 "올렸다 지운 module" 로 단정하면 기본 환경이 failed 다."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(
        "try:\n    import nope_optional_63\nexcept ImportError:\n    pass\n",
        encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path)
    hist = got["startup"]["startup_history"]
    assert hist.get("status") == "measured", hist
    assert "nope_optional_63" in hist.get("attempted_not_loaded", []), hist
    assert "nope_optional_63" not in hist["modules"]
    assert "sitecustomize" in hist["modules"]           # 성공한 로드는 잰다


def test_a_module_loaded_then_dropped_from_sys_modules_is_still_measured(tmp_path):
    """F2 대조군 — 올렸다가 `sys.modules` 에서만 지운 module 은 파일이 남아
    있으므로 **잰다** (증거: `-v` 로드 줄 + 지금 찾은 바이트)."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "kept63.py").write_text("VALUE = 1\n", encoding="utf-8")
    (site / "sitecustomize.py").write_text(
        "import sys\nimport kept63\ndel sys.modules['kept63']\n", encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path)
    hist = got["startup"]["startup_history"]
    assert hist["status"] == "measured", hist
    assert hist["modules"].get("kept63") == hashlib.sha256(
        (site / "kept63.py").read_bytes()).hexdigest()[:16]
    assert "kept63" not in hist.get("attempted_not_loaded", [])


def test_a_startup_module_removed_after_import_is_still_a_failed_measurement(tmp_path):
    """62차 자체 리뷰 F2 의 성질은 그대로 — 올렸다 **파일까지** 지운 module 은
    `-v` 가 로드를 증언하는데 지금 못 찾으므로 failed 다."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(
        "import os, sys\n"
        "p = os.path.join(os.path.dirname(__file__), 'ghost63.py')\n"
        "open(p, 'w').write('VALUE = 1\\n')\n"
        "import ghost63\n"
        "del sys.modules['ghost63']\n"
        "os.remove(p)\n", encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path)
    hist = got["startup"]["startup_history"]
    assert hist.get("status") == "failed", hist
    assert "ghost63" in hist.get("reason", "")


def test_the_schema_carries_the_attempted_list():
    """F2 — 시도만 한 이름 목록은 영수증 **안**이다 (digest 에 묶인다)."""
    import mutation_replay as mr
    from receipt_fixture import full_receipt
    rec = full_receipt()
    mr._assert_receipt_is_complete(rec)
    assert "attempted_not_loaded" in rec["startup"]["startup_history"]
    rec["startup"]["startup_history"]["attempted_not_loaded"] = [1]     # str 아님
    with pytest.raises(mr._ReplayError):
        mr._assert_receipt_is_complete(rec)


# ── E1 ──────────────────────────────────────────────────────────────────────
def _generic_function_node():
    """`def plain[T: int](value: T) -> T` 의 AST. 3.12+ 는 실제 파싱, 3.11 은
    같은 모양을 합성한다 (`type_params` 속성 + `bound` 가 `ast.Name`)."""
    if sys.version_info >= (3, 12):
        node = ast.parse("def plain[T: int](value: T) -> T:\n    return value\n").body[0]
        return node, node.type_params[0].bound
    node = ast.parse("def plain(value: T) -> T:\n    return value\n").body[0]
    bound = ast.Name(id="int", ctx=ast.Load())
    node.type_params = [types.SimpleNamespace(name="T", bound=bound,
                                              default_value=None)]
    return node, bound


def test_scope_walk_covers_the_bound_of_an_ordinary_generic_function():
    """★ E1 (리뷰어 원문의 성질) — type parameter 의 bound 는 정의 시점의
    식이다. scoped walker 가 그 node 를 방문해야 한다."""
    import row_projection as rp
    node, bound = _generic_function_node()
    assert isinstance(bound, ast.Name) and bound.id == "int"
    visited = {id(n) for n, scope in rp._scoped_shadows(node)}
    assert id(bound) in visited, "type parameter bound was omitted by the scoped traversal"


def test_scope_walk_ordinary_annotation_positive_control():
    import row_projection as rp
    node = ast.parse("def plain(value: int) -> int:\n    return value\n").body[0]
    visited = {id(n) for n, scope in rp._scoped_shadows(node)}
    assert id(node.args.args[0].annotation) in visited
    assert id(node.returns) in visited


def test_a_type_parameter_bound_is_evaluated_outside_the_parameters():
    """E1 의 scope 의미 — bound 는 매개변수를 못 본다. 매개변수 이름이 `getattr`
    이어도 bound 자리의 `getattr` 은 바깥(builtin)이다."""
    import row_projection as rp
    node, bound = _generic_function_node()
    node.args.args[0].arg = "getattr"                 # 매개변수 이름을 갈아 끼움
    scope_at_bound = next((s for n, s in rp._scoped_shadows(node) if n is bound),
                          None)
    assert scope_at_bound is not None, "bound node 를 walker 가 방문하지 않았다 (63차 E1)"
    assert "getattr" not in scope_at_bound, (
        "bound 자리에 매개변수 shadow 가 적용됐다 — bound 는 매개변수를 못 본다 (63차 E1)")


# ── E2 ──────────────────────────────────────────────────────────────────────
def _flock_reports_held(fd) -> bool:
    """**하나뿐인 판정** — 이 fd 로 non-blocking 배타 flock 을 시도해 커널이 거절하면
    True(누가 쥐고 있다), 받아 주면 즉시 풀고 False. token 판과 경로 판은 **여는 방식만**
    다르고 판정은 이 함수 하나를 공유한다 (65차 E2-R 후속 — 두 wrapper 가 판정을 따로
    갖고 있으면 한쪽만 양방향으로 시험돼도 다른 쪽은 밖이다)."""
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return True
    fcntl.flock(fd, fcntl.LOCK_UN)
    return False


def _kernel_lock_held(tok) -> bool:
    """token 의 lock 파일을 **따로 열어** flock 을 시도한다 — 커널이 배타를
    쥐고 있으면 BlockingIOError 다. 경로 exists 가 아니라 커널의 답이다."""
    fd = os.open(tok.name, os.O_RDWR, dir_fd=tok.dir_fd)
    try:
        return _flock_reports_held(fd)
    finally:
        os.close(fd)


def _kernel_lock_held_at(path) -> bool:
    """같은 물음을 **경로로** 묻는다 — release 는 token 의 `dir_fd` 를 닫으므로
    놓은 뒤의 음성 대조군은 token 으로 열 수 없다 (64차 E2-R). 여는 방식만
    다르고 묻는 것은 같다: 커널이 배타를 쥐고 있는가."""
    fd = os.open(str(path), os.O_RDWR)
    try:
        return _flock_reports_held(fd)
    finally:
        os.close(fd)


def test_the_kernel_lock_probe_itself_is_not_vacuous(tmp_path):
    """E2 탐침의 대조군 — 잡으면 True, 놓으면 False. 이것이 안 갈리면 아래
    시험의 True 는 증거가 아니다.

    ★ 64차 E2-R — 전 판은 `is True` 만 고정하고 finally 에서 놓기만 했다.
      원장은 "잡으면 True · 놓으면 False" 라고 적었으니 **문구가 시험보다
      강했다.** 음성 쪽을 여기서 실제로 관측한다 — 독립 open 둘 다로.
    """
    import src.io as io
    d = tmp_path / "d"
    d.mkdir()
    p = d / ".fit.lock"
    tok = io.acquire_run_lock(d, ".fit.lock")
    try:
        assert _kernel_lock_held(tok) is True
        assert _kernel_lock_held_at(p) is True       # 같은 자리를 경로로 봐도 잡혀 있다
        # ★ 65차 E2-R 후속 — 실제 lifecycle 이 부르는 것은 **token 판**이다. 그 음성을
        #   같은 token · 같은 inode 에서 관측한다: 밖에서 풀면 False, 다시 쥐면 True.
        #   경로 판의 음성만 있던 64차 판은 token 판을 상수 True 로 바꿔도 통과했다
        #   (리뷰어 후속 스크립트, 이 기계 실측).
        fcntl.flock(tok.fd, fcntl.LOCK_UN)
        assert _kernel_lock_held(tok) is False       # ★ token 판의 음성 (65차)
        fcntl.flock(tok.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        assert _kernel_lock_held(tok) is True
    finally:
        io.release_run_lock(tok)
    # release 는 lock 파일을 **지운다** — 그것부터 관측으로 고정한다 (그래서 놓은 뒤의
    # 음성 대조군은 token 으로도, 지워진 경로로도 열 수 없다).
    assert not p.exists(), "release 뒤에도 lock 파일이 남아 있다"
    p.touch()                                        # 같은 자리를 아무도 안 잡은 상태로
    assert _kernel_lock_held_at(p) is False          # ★ 음성 대조군 (64차 E2-R)


def _planned_root(monkeypatch) -> Path:
    """smoke namespace **밖**이되 저장소 **안**인 자리 (`results/` 아래). 밖이면
    §0 ⑦ 에 걸려 staging 에서 죽는다 — 아래 xfail 시험이 그것을 고정한다.
    끝나면 지운다."""
    base = REPO / "results"
    base.mkdir(exist_ok=True)
    return Path(tempfile.mkdtemp(prefix="_unit63-planned-", dir=base))


# ★ 64차 (리뷰어 후속 정리 제안) — `raises=Exception` 은 **다른 이유로 죽어도** 이
#   축으로 분류한다. §0 ⑦ 이 주장하는 오류는 하나다: staging 이 원본 자신 위에
#   복사하려다 나는 `shutil.SameFileError`. 이름을 좁혀 축을 또렷하게 한다 —
#   다른 예외가 나면 그것은 이 신고가 아니라 **새 발견**이어야 한다.
@pytest.mark.xfail(strict=True, raises=shutil.SameFileError,
                   reason="§0 ⑦ (62차 신고 · 63차 재확인): 저장소 밖 절대 경로 "
                          "입력은 staging 이 자기 자신 위에 복사하려다 죽는다")
def test_staging_an_input_outside_the_repo_is_still_unsupported(monkeypatch):
    """§0 ⑦ 을 **관측으로** 고정한다 — 고쳐지면 이 시험이 XPASS 로 빨개져서
    신고를 내리게 만든다. E2 의 첫 판이 여기서 죽었다 (`shutil.SameFileError`)."""
    import src.fitting as F
    from test_fitting import _tiny_curves

    root = Path(tempfile.mkdtemp(prefix="dd63-outside-"))
    in_dir = _tiny_curves(root / "in")
    F._stage_fit_inputs(in_dir, None, "grid", "ocp", None)


def test_fit_phase_receipt_is_written_while_the_kernel_lock_is_held(monkeypatch):
    """★ E2 — smoke namespace **밖**의 실제 planned lifecycle, production 과 같은
    모양 (`run.sh --mode all`): 계획 원장 → grid 가 `may_open` 으로 발급받아
    **진짜 solver** 로 조건 1개를 돌리고 phase 를 닫는다 → fit 이 token 으로
    같은 claim 을 이어받아 compute → commit → `claim.phase_done("fit")` durable
    기록 → release. phase 기록이 **쓰이는 순간** 커널이 `.fit.lock` 을 쥐고
    있고, release 시점에는 이미 그 기록이 디스크에 있다.

    경로 exists 가 아니라 커널의 답(`flock` 재시도 → BlockingIOError)이고, claim
    이 `None` 이 아니라 원장이 발급한 것이다 — 62차 시험의 두 공백이 여기서
    닫힌다. 탐침의 대조군은 위 시험이다."""
    import shutil

    import yaml

    import src.fitting as F
    import src.grid as G
    import src.io as io
    import tools.preserve as P
    from src.config import load_config
    from src.io import source_digest
    from test_lock_lifetime_62 import _BOUNDS, _OBJ_CFG

    # 진짜 producer 는 git 상태를 적고, fit 의 producer 검증(F74/F85)은 dirty
    # worktree 에서 난 곡선을 거부한다 — smoke 와 같은 "clean 커밋에서만"
    # 규칙이다. 이 시험은 그 규칙을 우회하지 않는다 (git 상태를 위조하면 검증이
    # 재는 것이 바뀐다).
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"],
                           cwd=REPO, capture_output=True, text=True).stdout.strip()
    if dirty:
        pytest.skip("dirty worktree — 진짜 grid 의 곡선을 fit 이 거부한다 (F74/F85). "
                    "clean 커밋에서 돈다 (smoke 와 같은 규칙)")

    root = _planned_root(monkeypatch)
    try:
        led = root / "ledger" / "LEG_PRESERVATION.yaml"
        led.parent.mkdir(parents=True)
        monkeypatch.setattr(P, "DEFAULT_LEDGER", led)
        monkeypatch.setattr(P, "DEFAULT_CLAIMS_ROOT", P.claims_root_for_ledger(led))

        cfg = load_config("configs/base.yaml")
        conds = G.conditions_from_config(
            cfg, {"lli": "0", "lam_pe": "0", "lam_ne": "0", "noise": "0"})
        assert len(conds) == 1
        grid_out, fit_out = root / "grid", root / "fit"
        objectives = {"a": {"w_pocv": 1.0}}
        G.get_discharged_state(cfg)              # 캐시를 계획 **앞에** 만든다
        grid_axis = G.live_grid_axis(cfg, conds, grid_out)
        fit_axis = dict(
            F.live_fit_axis(objectives, _OBJ_CFG, _BOUNDS, "expanded", 1, True,
                            None, None, "grid", True, True, "Nelder-Mead", "ocp",
                            None, grid_out, fit_out,
                            base_config="configs/base.yaml", bytes_root=REPO),
            in_digest=None)                      # 이 다리의 grid 가 만든다
        spec = P.leg_run_spec("L63", grid_axis, fit_axis)
        led.write_text(yaml.safe_dump({
            "schema_version": 4,
            "cohorts": [{"cohort_id": "g63", "dir": "docs/22p_gap/coh",
                         "status": "active", "legs": [],
                         "prospective_legs": ["L63"],
                         "cross_leg_comparison": "allowed_within_cohort",
                         "pin": {"schema_version": 3, "compute_sha256": "a" * 16,
                                 "row_projection_py_sha256": "b" * 16,
                                 "src_scoring_py_sha256": "c" * 16,
                                 "analysis_spec_sha256": "d" * 16,
                                 "producer_semantic_sha256": "e" * 16}}],
            "planned": [{"leg_id": "L63", "cohort_id": "g63",
                         "status": "planned",
                         "authorization_kind": "prospective",
                         "authorized_source_digest": source_digest(),
                         "run_spec_digest": P.run_spec_digest(spec),
                         "run_spec": spec, "recorded_on": "2026-09-15",
                         "근거": "시험용 — 63차 E2 planned lifecycle",
                         "claim_scope": "active_claims"}],       # 74차 G74-3
            "legs": []}, allow_unicode=True, sort_keys=False), encoding="utf-8")

        # grid phase — production 진입점, 진짜 solver, 조건 1개
        G.run_grid(cfg, conds, nproc=1, chunk_size=1, out_dir=grid_out,
                   leg="L63", may_open=True)
        claim_file = P.claims_root_for_ledger(led) / "L63.claim"
        assert "grid" in (json.loads(claim_file.read_text(encoding="utf-8"))
                          .get("phases") or {}), "grid phase 가 안 닫혔다"

        seq: list = []
        holder: dict = {}
        real_acquire = io.acquire_run_lock
        real_phase_done = P.LegClaim.phase_done
        real_release = io.release_run_lock

        def _acquire(*a, **k):
            tok = real_acquire(*a, **k)
            holder["tok"] = tok
            return tok

        def _phase_done(self, phase, receipt):
            seq.append(("phase_done", phase, _kernel_lock_held(holder["tok"])))
            real_phase_done(self, phase, receipt)
            rec = json.loads(self.path.read_text(encoding="utf-8"))
            seq.append(("phase_written", "fit" in (rec.get("phases") or {})))

        def _release(tok, *a, **k):
            rec = json.loads(claim_file.read_text(encoding="utf-8"))
            seq.append(("release", "fit" in (rec.get("phases") or {}),
                        _kernel_lock_held(tok)))
            return real_release(tok, *a, **k)

        monkeypatch.setattr(io, "acquire_run_lock", _acquire)
        monkeypatch.setattr(P.LegClaim, "phase_done", _phase_done)
        monkeypatch.setattr(io, "release_run_lock", _release)

        # fit phase — token 파일로 같은 claim 을 이어받는다 (may_open 아님)
        F.run_fit(grid_out, fit_out, _OBJ_CFG, objectives, _BOUNDS, "expanded",
                  1, nproc=1, leg="L63")

        assert seq == [("phase_done", "fit", True), ("phase_written", True),
                       ("release", True, True)], seq
        assert not (fit_out / ".fit.lock").exists()
    finally:
        shutil.rmtree(root, ignore_errors=True)
