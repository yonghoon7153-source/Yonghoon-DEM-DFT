"""62차 ε′ (P1-3 · P1-4 · P1-5 · P1-6 · P2-1) — **증거 영수증의 다섯 구멍.**

리뷰어 발견 (전부 `docs/22p_gap/mutation_replay.py` 의 영수증 층):

  P1-3  startup 코드(`sitecustomize` 의 `atexit`)가 stdout 의 **마지막 줄**로
        영수증을 위조한다 — reader 가 `splitlines()[-1]` 을 영수증으로 받는다.
  P1-4  zip 에서 올라온 module 은 `find_spec().origin` 이 파일이 아니라
        `unfiled` 로 세고, 읽기 실패는 `"<unreadable>"` 이라는 정상 문자열로
        적힌다 — 둘 다 `measured` 로 세탁된다.
  P1-5  `packages` 가 같은 이름의 distribution 을 **뒤 root 가 앞을 덮는**
        순서로 담는다. Python 은 `sys.path` 앞이 이긴다.
  P1-6  한 재생 안에서 영수증을 **여러 번** 잰다 — 표식/선택(`environment_tag()`),
        본문(`_execution_receipt()`), digest(`_execution_receipt_digest()`)가
        각각 탐침을 다시 띄우므로 그 사이에 환경이 바뀌면 서로 다른 것을 적는다.
  P2-1  completeness reader 가 `status` discriminator 만 본다 — 본문이 무엇이든
        `measured` 라 적혀 있으면 받는다.

`[고침]`
  · 영수증은 **frame** 으로 감싸 찍고, reader 는 stdout 이 정확히 그 frame
    하나일 때만 받는다 (앞뒤에 무엇이든 더 있으면 거부).
  · `_d()` 는 실패를 **올리고** 그 섹션이 `failed` 가 된다. zip origin 은
    loader 의 `get_data` 로 바이트를 읽어 해시한다 — 못 읽으면 `failed`.
  · `packages` 는 `sys.path` 순서로 훑어 **처음 것**을 담고, 가려진 것은
    `shadowed` 에 위치와 함께 남긴다.
  · 재생은 영수증을 **한 번** 재서 `ReceiptSnapshot` 으로 들고 간다 — 표식
    tag · 본문 · digest 가 전부 그 한 스냅샷에서 나온다.
  · reader 는 재귀 exact schema 로 본다 — 키 집합·타입·hex16 까지.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO / "docs" / "22p_gap") not in sys.path:
    sys.path.insert(0, str(REPO / "docs" / "22p_gap"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from receipt_fixture import full_receipt                        # noqa: E402

_H16 = "0123456789abcdef"


def _mr():
    import mutation_replay as mr

    return mr


def _receipt_in(env_extra: dict, cwd: Path) -> dict:
    """탐침 본문을 그대로 돌려 `_receipt_facts` 를 한 번 잰다 (frame 없이)."""
    mr = _mr()
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


# ── P1-3 frame ────────────────────────────────────────────────────────────
def test_the_framed_parser_accepts_exactly_one_frame():
    mr = _mr()
    f = "DD-RECEIPT-abcd"
    body = json.dumps({"a": 1})
    assert mr._parse_framed_receipt(f + body + f + "\n", f) == {"a": 1}


@pytest.mark.parametrize("stdout", [
    'DD-RECEIPT-abcd{"a": 1}DD-RECEIPT-abcd\n{"forged": true}\n',     # 뒤에 한 줄
    '{"forged": true}\nDD-RECEIPT-abcd{"a": 1}DD-RECEIPT-abcd\n',     # 앞에 한 줄
    'DD-RECEIPT-abcd{"a": 1}DD-RECEIPT-abcd\n'
    'DD-RECEIPT-abcd{"b": 2}DD-RECEIPT-abcd\n',                       # frame 둘
    '{"a": 1}\n',                                                     # frame 없음
    'DD-RECEIPT-abcd{"a": 1}\n',                                      # 닫는 frame 없음
])
def test_the_framed_parser_refuses_anything_but_one_frame(stdout):
    mr = _mr()
    with pytest.raises(ValueError, match="frame"):
        mr._parse_framed_receipt(stdout, "DD-RECEIPT-abcd")


def test_an_atexit_forgery_in_sitecustomize_is_refused(tmp_path, monkeypatch):
    """★ P1-3 — 리뷰어의 형태 그대로: `sitecustomize` 가 atexit 에서 영수증
    모양의 JSON 을 stdout 마지막 줄로 찍는다. reader 는 그것을 받으면 안 된다."""
    mr = _mr()
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(
        "import atexit, json\n"
        "atexit.register(lambda: print(json.dumps({'forged': True})))\n",
        encoding="utf-8")
    real_env = mr.replay_env

    def _env():
        e = dict(real_env())
        e["PYTHONPATH"] = str(site) + (os.pathsep + e["PYTHONPATH"]
                                       if e.get("PYTHONPATH") else "")
        return e

    monkeypatch.setattr(mr, "replay_env", _env)
    with pytest.raises(mr._ReplayError, match="frame"):
        mr._observed_receipt()


def test_the_attestation_node_parses_a_frame_not_the_last_line(tmp_path):
    """심어 놓은 증언 node 도 같은 규칙이다 — 규칙이 두 곳이면 갈린다."""
    mr = _mr()
    (tmp_path / "tests").mkdir()
    mr._write_env_attestation(tmp_path, "0123456789abcdef")
    node = next((tmp_path / "tests").glob("test_mutation_env_*.py")).read_text(
        encoding="utf-8")
    assert "splitlines()[-1]" not in node, "증언 node 가 아직 마지막 줄을 받는다"
    assert "_parse_framed_receipt" in node and "DD-RECEIPT-" in node


# ── P1-4 unreadable · zip ─────────────────────────────────────────────────
def test_a_zip_imported_startup_module_is_hashed_not_unfiled(tmp_path):
    """★ P1-4 — zip 에서 올라온 startup module 의 바이트는 **잰다**."""
    site = tmp_path / "site"
    site.mkdir()
    z = tmp_path / "mods.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("zipmod_62.py", "VALUE = 'FROM_ZIP'\n")
    (site / "sitecustomize.py").write_text("import zipmod_62\n", encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(site) + os.pathsep + str(z)}, tmp_path)
    hist = got["startup"]["startup_history"]
    assert hist["status"] == "measured", hist
    assert "zipmod_62" in hist["modules"], (
        f"zip 에서 올라온 module 이 unfiled 로 세탁됐다: "
        f"{sorted(hist['modules'])[:5]}… unfiled={hist.get('unfiled')} (62차 P1-4)")


def test_an_unreadable_startup_byte_makes_the_section_failed(tmp_path):
    """★ P1-4 — `.pth` 자리에 읽을 수 없는 것(디렉터리)이 있으면 `startup` 은
    `failed` 다 — `"<unreadable>"` 이라는 정상 문자열이 아니다."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "weird.pth").mkdir()                    # open() 이 실패한다
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path)
    assert "<unreadable>" not in json.dumps(got), "읽기 실패가 정상 값으로 적혔다"
    assert got["startup"].get("status") == "failed", got["startup"].get("status")
    assert "weird.pth" in got["startup"].get("reason", "")


def test_a_failed_startup_section_is_refused_by_the_reader(monkeypatch):
    mr = _mr()
    bad = full_receipt(startup={"status": "failed", "reason": "시험"})
    monkeypatch.setattr(mr, "_observed_receipt", lambda: bad)
    with pytest.raises(mr._ReplayError, match="불완전|실패"):
        mr._execution_receipt()


# ── P1-5 duplicate distributions ─────────────────────────────────────────
def _dist(root: Path, version: str) -> None:
    d = root / f"dup62-{version}.dist-info"
    d.mkdir(parents=True)
    (d / "METADATA").write_text(f"Metadata-Version: 2.1\nName: dup62\n"
                                f"Version: {version}\n", encoding="utf-8")


def test_python_really_picks_the_first_distribution_on_sys_path(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    _dist(a, "1.0")
    _dist(b, "2.0")
    r = subprocess.run(
        [sys.executable, "-c",
         "from importlib import metadata; print(metadata.version('dup62'))"],
        env={**os.environ, "PYTHONPATH": f"{a}{os.pathsep}{b}"},
        capture_output=True, text=True, timeout=120)
    assert r.stdout.strip() == "1.0", r.stderr[-500:]


def test_duplicate_distributions_keep_the_first_and_record_the_rest(tmp_path):
    """★ P1-5 — 영수증은 Python 이 고를 것을 적고, 가려진 것은 위치와 함께."""
    a, b = tmp_path / "a", tmp_path / "b"
    _dist(a, "1.0")
    _dist(b, "2.0")
    got = _receipt_in({"PYTHONPATH": f"{a}{os.pathsep}{b}"}, tmp_path)["packages"]
    assert got["status"] == "measured"
    assert got["dists"]["dup62"] == "1.0", (
        f"뒤 root 가 앞 root 를 덮었다: {got['dists'].get('dup62')} (62차 P1-5)")
    assert any(s[0] == "dup62" and s[2] == "2.0" for s in got.get("shadowed", [])), (
        f"가려진 distribution 이 기록되지 않았다: {got.get('shadowed')}")
    assert got["positions"]["dup62"] < [s for s in got["shadowed"]
                                        if s[0] == "dup62"][0][1]
    rev = _receipt_in({"PYTHONPATH": f"{b}{os.pathsep}{a}"}, tmp_path)["packages"]
    assert rev["dists"]["dup62"] == "2.0", "순서를 뒤집었는데 같은 것을 골랐다"


# ── P1-6 single snapshot ─────────────────────────────────────────────────
def test_a_snapshot_is_measured_once_and_its_parts_agree(monkeypatch):
    mr = _mr()
    n = {"calls": 0}

    def _once():
        n["calls"] += 1
        r = full_receipt()
        r["inputs"]["files"] = {"configs/base.yaml": _H16, "n.txt": _H16[:15] + str(n["calls"])}
        return r                                            # 부를 때마다 다르다

    monkeypatch.setattr(mr, "_observed_receipt", _once)
    snap = mr.take_receipt_snapshot()
    assert n["calls"] == 1
    body = snap.body()
    assert body["inputs"]["files"]["n.txt"].endswith("1")
    assert snap.digest == mr._execution_receipt_digest(body)
    assert snap.tag == mr.environment_tag(body)
    assert snap.tag == snap.digest[:16], "tag 와 digest 가 같은 직렬화에서 나오지 않았다"
    # 스냅샷은 불변이다 — body() 는 사본을 준다
    snap.body()["interpreter"] = "x"
    assert snap.body()["interpreter"] != "x"


def _calls_in(fn_name: str) -> set:
    mr = _mr()
    tree = ast.parse(Path(mr.__file__).read_text(encoding="utf-8"))
    fn = next(n for n in ast.walk(tree)
              if isinstance(n, ast.FunctionDef) and n.name == fn_name)
    out = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Call):
            f = n.func
            out.add(f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None))
    return out


@pytest.mark.parametrize("fn", ["_replay", "_write_coverage",
                                "_assert_execution_is_current"])
def test_the_runner_and_checker_do_not_remeasure_the_receipt(fn):
    """★ P1-6 — 표식·본문·digest 는 **한 스냅샷**에서 나온다. 이 함수들 안에서
    탐침을 다시 띄우는 호출(`environment_tag()` 무인자 · `_execution_receipt()` ·
    `_execution_receipt_digest()` 무인자)은 없어야 한다."""
    calls = _calls_in(fn)
    assert "take_receipt_snapshot" in calls or fn == "_write_coverage", (
        f"{fn} 이 스냅샷을 안 쓴다")
    forbidden = {"_execution_receipt", "_execution_receipt_digest",
                 "environment_tag"} & calls
    # `_write_coverage` 는 스냅샷을 인자로 받는다 — 무엇도 다시 재면 안 된다
    assert not forbidden, f"{fn} 이 영수증을 다시 잰다: {sorted(forbidden)} (62차 P1-6)"


def test_write_coverage_records_exactly_the_snapshot(tmp_path, monkeypatch):
    mr = _mr()
    rec = full_receipt()
    monkeypatch.setattr(mr, "_observed_receipt", lambda: rec)
    snap = mr.take_receipt_snapshot()
    monkeypatch.setattr(mr, "_observed_receipt",
                        lambda: (_ for _ in ()).throw(AssertionError("다시 쟀다")))
    p = tmp_path / "s1.json"
    mr._write_coverage(p, "", [], [], [], {}, receipts=None, snapshot=snap)
    got = json.loads(p.read_text(encoding="utf-8"))["binding"]
    assert got["execution"] == snap.body()
    assert got["execution_digest"] == snap.digest


# ── P2-1 exact schema ────────────────────────────────────────────────────
def test_a_full_receipt_matches_the_schema():
    mr = _mr()
    mr._assert_receipt_is_complete(full_receipt())


@pytest.mark.parametrize("mutate,why", [
    (lambda r: r.__setitem__("extra", 1), "최상위에 모르는 키"),
    (lambda r: r["startup"]["startup_history"].__setitem__("unfiled", "3"),
     "unfiled 가 문자열"),
    (lambda r: r["startup"]["startup_modules"].__setitem__("os", "not-hex"),
     "digest 가 hex16 이 아니다"),
    (lambda r: r["startup"].pop("pth"), "startup.pth 가 없다"),
    (lambda r: r["packages"].__setitem__("dists", ["numpy"]), "dists 가 list"),
    (lambda r: r["startup"]["startup_history"].__setitem__("extra", {}),
     "history 에 모르는 키"),
    (lambda r: r["inputs"].__setitem__("files", {"x": "<unreadable>"}),
     "inputs 에 sentinel 문자열"),
])
def test_a_receipt_that_only_says_measured_is_still_refused(mutate, why):
    """★ P2-1 — `status: measured` 라고 적혀 있어도 본문이 schema 밖이면 거부."""
    mr = _mr()
    rec = full_receipt()
    mutate(rec)
    with pytest.raises(mr._ReplayError, match="불완전|실패|schema"):
        mr._assert_receipt_is_complete(rec)
    _ = why


def test_the_real_probe_output_matches_the_schema(tmp_path):
    """이 기계의 실제 탐침 출력이 schema 에 맞아야 한다 — schema 가 현실보다
    좁으면 층이 마비된다 (거부가 넓어지는 것도 결함이다)."""
    mr = _mr()
    got = _receipt_in({}, tmp_path)
    mr._assert_receipt_is_complete(got)


# ── 62차 자체 리뷰 (영수증 위조 렌즈) ─────────────────────────────────────
#
# F2  `find_spec → None` 을 `unfiled` 로 셌다 — startup 에 올렸다 **지운** module
#     (파일도 지움) 이 영수증 밖 (importtime 로그엔 남는데 spec 이 None).
#     헤더 줄 `imported package` 와 실패한 `usercustomize` 시도가 그 경로의
#     정상 사례라 `unfiled=22` 에 둘이 섞여 있었다.
# F3  PYTHONPATH root 의 `*.dist-info/entry_points.txt` 가 영수증 밖 — 같은
#     digest 로 pytest plugin 이 로드되거나 안 되거나.
# F4  Name 없는 dist-info 는 조용히 건너뜀 (Python 은 디렉터리 stem 으로 찾는다).
# F5  schema 가 전부 빈 영수증·교차 필드 불일치를 받는다.
# F1  frame 의 한계: child 의 startup 코드 전부 (sys.stdout 교체 · fd 층 ·
#     builtins.print) 는 못 막는다. 부모가 **자기 프로세스에서** customization
#     (site/sitecustomize/usercustomize 바이트)을 재서 child 의 값과 대조하면
#     "<absent>" 세탁은 잡힌다.
def test_a_startup_module_removed_after_import_is_a_failed_measurement(tmp_path):
    """★ F2 — 올렸다 지운 module: 로그에 이름이 남고 spec 은 None → failed."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(
        "import os, sys\n"
        "p = os.path.join(os.path.dirname(__file__), 'ghost62.py')\n"
        "open(p, 'w').write('VALUE = 1\\n')\n"
        "import ghost62\n"
        "del sys.modules['ghost62']\n"
        "os.remove(p)\n", encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(site)}, tmp_path)
    hist = got["startup"]["startup_history"]
    assert hist.get("status") == "failed", (   # 증인 문구에 기계별 개수를 싣지 않는다
        f"올렸다 지운 module 이 unfiled 로 세탁됐다: {hist.get('status')} "
        "(62차 자체 리뷰 F2)")
    assert "ghost62" in hist.get("reason", "")


def test_the_importtime_header_line_is_not_a_module(tmp_path):
    """F2 의 정상 사례 — 헤더 줄 `imported package` 와 실패한 `usercustomize`
    시도는 module 이 아니다. 기본 환경은 여전히 measured 여야 한다."""
    got = _receipt_in({}, tmp_path)
    hist = got["startup"]["startup_history"]
    assert hist["status"] == "measured", hist
    assert "imported package" not in hist["modules"]


def test_dist_info_files_on_pythonpath_are_inside_the_receipt(tmp_path):
    """★ F3 — `entry_points.txt` 의 바이트가 바뀌면 영수증이 움직여야 한다."""
    root = tmp_path / "root"
    _dist(root, "1.0")
    ep = root / "dup62-1.0.dist-info" / "entry_points.txt"
    ep.write_text("[pytest11]\nevil = evilplug\n", encoding="utf-8")
    a = _receipt_in({"PYTHONPATH": str(root)}, tmp_path)
    ep.write_text("", encoding="utf-8")
    b = _receipt_in({"PYTHONPATH": str(root)}, tmp_path)
    assert a["startup"]["importable_roots"] != b["startup"]["importable_roots"], (
        "entry_points.txt 를 바꿨는데 importable_roots 가 그대로다 (62차 자체 리뷰 F3)")
    assert any(k.endswith("entry_points.txt") for k in a["startup"]["importable_roots"])


def test_a_distribution_without_a_name_is_keyed_by_its_stem(tmp_path):
    """★ F4 — Python 은 `noname-1.0.dist-info` 를 `noname` 으로 찾는다."""
    root = tmp_path / "root"
    d = root / "noname62-1.0.dist-info"
    d.mkdir(parents=True)
    (d / "METADATA").write_text("Metadata-Version: 2.1\nVersion: 1.0\n",
                                encoding="utf-8")
    got = _receipt_in({"PYTHONPATH": str(root)}, tmp_path)["packages"]
    assert got["dists"].get("noname62") == "1.0", (
        f"Name 없는 dist 가 사라졌다: {sorted(got['dists'])[:5]} (62차 자체 리뷰 F4)")


@pytest.mark.parametrize("mutate,why", [
    (lambda r: r["startup"].__setitem__("customization", {"whatever": "<absent>"}),
     "customization 키 집합"),
    (lambda r: r["startup"].__setitem__("startup_modules", {}), "빈 startup_modules"),
    (lambda r: (r.__setitem__("env", {}), r["startup"].__setitem__("env", {})),
     "빈 env"),
    (lambda r: r["startup"].__setitem__("version", "9.9.9"), "startup.version ≠ interpreter"),
    (lambda r: r["startup"].__setitem__("env", {"PYTHONHASHSEED": "1"}),
     "startup.env ≠ env"),
    (lambda r: r["startup"]["startup_history"].__setitem__("unfiled", -5), "음수 int"),
])
def test_the_schema_refuses_empty_or_inconsistent_receipts(mutate, why):
    """★ F5 — "아무것도 안 잰" 영수증과 교차 필드 불일치는 measured 가 아니다."""
    mr = _mr()
    rec = full_receipt()
    mutate(rec)
    with pytest.raises(mr._ReplayError, match="불완전|실패|schema"):
        mr._assert_receipt_is_complete(rec)
    _ = why


def test_the_parent_cross_checks_the_customization_bytes(tmp_path, monkeypatch):
    """★ F1 — child 가 `sitecustomize` 를 `<absent>` 로 세탁하면 부모가 자기
    프로세스에서 잰 값과 어긋나 거부한다."""
    mr = _mr()
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text("X = 1\n", encoding="utf-8")
    real_env = mr.replay_env

    def _env():
        e = dict(real_env())
        e["PYTHONPATH"] = str(site)
        return e

    monkeypatch.setattr(mr, "replay_env", _env)
    rec = full_receipt()
    rec["startup"]["customization"]["sitecustomize"] = "<absent>"   # 세탁본
    monkeypatch.setattr(mr, "_observed_receipt", lambda: rec)
    with pytest.raises(mr._ReplayError, match="sitecustomize"):
        mr._execution_receipt()
    honest = full_receipt()
    honest["startup"]["customization"] = mr._parent_customization_view()
    monkeypatch.setattr(mr, "_observed_receipt", lambda: honest)
    assert mr._execution_receipt() == honest


def test_the_real_probe_agrees_with_the_parent_view(tmp_path):
    mr = _mr()
    got = _receipt_in({}, tmp_path)
    child, parent = got["startup"]["customization"], mr._parent_customization_view()
    diff = sorted(k for k in set(child) | set(parent) if child.get(k) != parent.get(k))
    assert not diff, (   # 증인 문구에 기계별 digest 를 싣지 않는다 (63차 변이 재생)
        f"child 와 부모의 customization 이 {diff} 에서 다르다 (62차 자체 리뷰 F1)")
