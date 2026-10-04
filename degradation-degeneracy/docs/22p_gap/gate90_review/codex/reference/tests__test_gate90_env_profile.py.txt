"""90차 — PyBaMM 환경 고정 라운드: C lock (현재 검증 환경의 정확 고정 · 기록 대조) + B (v4 정본 producer 기록)
(고정 표 `docs/22p_gap/PYBAMM_PIN_ROUND_SPEC.md` · 원장 §135).

사전 검토 회신 (`docs/22p_gap/PYBAMM_PIN_PREREVIEW_REPLY_20261003.md` P3): 지금은 "무엇으로 돌렸나" 는 기록되지만
(`src/io.py::env_fingerprint` · effective_solver · worker 서명 대조) "그 환경이 승인된 것인가" 를 묻는 곳이 없다. 이 라운드는
C 를 **기록 대조**로만 넣는다 — 불일치여도 어떤 실행도 막지 않고 (D3), 대조 결과를 smoke 로그 · 영수증 stamp · 게이트 증거에
남긴다. 측정하지 않은 것은 `UNMEASURED` 이고 그 칸은 `None` 이다 (빈 목록은 "불일치 없음" 으로 읽힌다 — 61차 P1-3).

node (고정 표 §8): e01 커밋된 lock · e02 합성 왕복 · e03 축마다 정확히 그 축 · e04 형식 오류 → UNMEASURED · e05 측정 예외 →
UNMEASURED · e06 실제 환경 typed · e07 핵심 module = 지문 축 · e08 CLI rc 0 · e09 smoke 정적 · e10 영수증 stamp · e11 B = 네
manifest · e12 requirements 하한 · 주석. RED 에서는 전부 빨갛다 (도구 · lock · B 기록 · smoke 단계 · stamp · 주석이 아직 없다) —
그래서 `tools.env_profile` · `make_receipt` 의 import 는 각 시험 **안에서** 한다 (수집 오류가 아니라 node 별 실패로 본다).

합성 환경은 `tmp_path` 의 가짜 site 디렉터리다 — `*.dist-info` 의 METADATA · RECORD 와 파일을 쓰고 RECORD 의 sha256 은 실제로
계산한다. 측정 경로는 함수 인자로 준다 (실제 `sys.path` 를 건드리지 않는다).
"""
from __future__ import annotations

import base64
import hashlib
import importlib
import importlib.util
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "requirements-validation-C.lock.txt"
B_PROFILE = ROOT / "docs" / "22p_gap" / "env_profile_B_v4.yaml"
SMOKE = ROOT / "scripts" / "smoke_e2e.sh"
REQ = ROOT / "requirements.txt"

#: 고정 표 §4-2 — 결과 dict 의 닫힌 키 · 수 칸 · 불일치 축.
RESULT_KEYS = {"profile", "lock_path", "lock_sha256", "status", "reason", "mismatches", "unverifiable", "counts"}
COUNT_KEYS = {"dists_locked", "dists_measured", "shadowed_locked", "shadowed_measured",
              "files_verified", "files_unhashed", "origins_verified"}
MISMATCH_KEYS = {"axis", "subject", "locked", "measured"}
AXES = {"python", "implementation", "system", "machine", "libc", "dist_missing", "dist_extra",
        "dist_version", "dist_record", "shadowed", "file", "origin"}
#: 고정 표 §4-1 — `env_fingerprint()` 의 module 축 (순서도 지문과 같다).
KEY_MODULES = ("numpy", "scipy", "pandas", "joblib", "pyarrow", "pybamm", "matplotlib", "yaml",
               "pybammsolvers", "casadi")
#: 고정 표 §3-2 — 생성 시점 이 검증 컨테이너의 핵심 배포판.
PINNED = {"pybamm": "26.8.0.0", "pybammsolvers": "0.9.1", "casadi": "3.7.2", "numpy": "2.4.6",
          "scipy": "1.17.1", "pandas": "3.0.5", "joblib": "1.6.0", "pyarrow": "25.0.1",
          "matplotlib": "3.11.2", "pyyaml": "6.0.1"}
#: 고정 표 §6 — B 의 출처 네 manifest (이 순서).
B_SOURCES = ("artifacts/grid_curves_v4/curves_manifest.yaml", "artifacts/grid_fit_v4/manifest.yaml",
             "artifacts/halfcell_fit_v4/manifest.yaml", "artifacts/paired_fixed5_v4/manifest.yaml")
#: 고정 표 §7 — 요구 줄 12 개는 바이트 그대로다 (D4: 하한 유지).
REQUIREMENT_LINES = [
    "pybamm[all]>=24.5        # [all] 이 IDAKLU solver 포함. 이거 없으면 2~5배 느림",
    "numpy>=1.24",
    "scipy>=1.11",
    "pandas>=2.0",
    "matplotlib>=3.7",
    "PyYAML>=6.0",
    "joblib>=1.3",
    "pyarrow>=14.0            # parquet",
    "tqdm>=4.65",
    "openpyxl>=3.1            # 원본 xlsx export 호환용",
    "pytest>=7.4",
    "pytest-json-report>=1.5",
]


def _ep():
    return importlib.import_module("tools.env_profile")


def _make_receipt():
    spec = importlib.util.spec_from_file_location(
        "make_receipt_gate90", ROOT / "docs" / "22p_gap" / "make_receipt.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── 합성 site ────────────────────────────────────────────────────────────────

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()


def _make_dist(site: Path, name: str, version: str, files: dict, *, record: bool = True) -> Path:
    """가짜 설치 배포판 — `files` (site 기준 상대경로 → 바이트) 를 쓰고 METADATA 와 (있으면) RECORD 를 만든다."""
    di = site / f"{name.replace('-', '_')}-{version}.dist-info"
    di.mkdir(parents=True)
    meta = f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n".encode()
    (di / "METADATA").write_bytes(meta)
    rows = []
    for rel, data in files.items():
        p = site / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        rows.append(f"{rel},sha256={_b64(data)},{len(data)}")
    if record:
        rows.append(f"{di.name}/METADATA,sha256={_b64(meta)},{len(meta)}")
        rows.append(f"{di.name}/RECORD,,")
        (di / "RECORD").write_text("\n".join(rows) + "\n", encoding="utf-8")
    return di


@pytest.fixture
def synth(tmp_path):
    """핵심 module 열 개 (yaml 은 실제처럼 RECORD 없는 PyYAML) + 다른 배포판 하나 + 뒤 경로의 가려진 항목 하나."""
    site, site2, stray = tmp_path / "site", tmp_path / "site2", tmp_path / "stray"
    for m in KEY_MODULES:
        _make_dist(site, "PyYAML" if m == "yaml" else m, "1.0",
                   {f"{m}/__init__.py": f"# fake {m}\n".encode()}, record=(m != "yaml"))
    _make_dist(site, "extra-dist", "1.0", {"extra_mod.py": b"X = 1\n", "extra_mod_data.txt": b"data\n"})
    _make_dist(site2, "extra-dist", "0.9", {"extra_mod.py": b"X = 0\n"})
    stray.mkdir()
    return SimpleNamespace(site=site, site2=site2, stray=stray, paths=[str(site), str(site2)])


def _lock_for(ep, paths, where: Path) -> tuple[Path, str]:
    text = ep.emit_lock(ep.measure(paths=paths))
    where.write_bytes(text.encode("utf-8"))
    return where, text


def _set_directive(text: str, key: str, value: str) -> str:
    out, n = re.subn(rf"^#@ {key} .*$", f"#@ {key} {json.dumps(value)}", text, count=1, flags=re.M)
    assert n == 1, key
    return out


def _dist_lines(text: str) -> list[str]:
    return re.findall(r"^[a-z0-9]+(?:-[a-z0-9]+)*==\S+  # record-sha256 (?:[0-9a-f]{64}|none)$", text, re.M)


def _flip_hex(h: str) -> str:
    return ("0" if h[0] != "0" else "1") + h[1:]


def _assert_closed(r: dict) -> None:
    assert set(r) == RESULT_KEYS, sorted(r)
    assert r["profile"] == "C"
    assert r["status"] in ("MATCH", "MISMATCH", "UNMEASURED")
    if r["status"] == "UNMEASURED":
        assert isinstance(r["reason"], str) and r["reason"], "UNMEASURED 인데 reason 이 비었다"
        assert r["mismatches"] is None and r["unverifiable"] is None and r["counts"] is None, \
            "UNMEASURED 인데 측정 칸이 None 이 아니다"
        return
    assert r["reason"] == ""
    assert set(r["counts"]) == COUNT_KEYS and all(type(v) is int for v in r["counts"].values())
    assert set(r["unverifiable"]) == {"dists_without_record", "origins"}
    for m in r["mismatches"]:
        assert set(m) == MISMATCH_KEYS and m["axis"] in AXES, sorted(m)
    keys = [(m["axis"], m["subject"]) for m in r["mismatches"]]
    assert keys == sorted(keys)
    assert (r["status"] == "MATCH") == (r["mismatches"] == [])


# ── e01 · 커밋된 lock ──────────────────────────────────────────────────────────

def test_e01_committed_lock_is_canonical_and_pinned():
    raw = LOCK.read_bytes()
    text = raw.decode("utf-8")
    assert "\r" not in text and text.endswith("\n")
    ep = _ep()
    assert ep.emit_lock(ep.parse_lock(text)) == text, "커밋된 lock 이 정규형 고정점이 아니다"
    directives = dict(re.findall(r'^#@ (profile|python|implementation|system|machine|libc) (".*")$', text, re.M))
    assert {k: json.loads(v) for k, v in directives.items()} == {
        "profile": "C", "python": "3.11.15", "implementation": "CPython", "system": "Linux",
        "machine": "x86_64", "libc": "glibc 2.39"}
    dists = re.findall(r"^([a-z0-9]+(?:-[a-z0-9]+)*)==(\S+)  # record-sha256 ([0-9a-f]{64}|none)$", text, re.M)
    names = [n for n, _, _ in dists]
    assert len(dists) == 170 and names == sorted(set(names))
    assert sum(1 for line in text.splitlines() if line and not line.startswith("#")) == 170
    got = {n: (v, rec) for n, v, rec in dists}
    assert {n: got[n][0] for n in PINNED} == PINNED
    assert got["pyyaml"][1] == "none" and got["pybamm"][1] != "none"
    shadowed = re.findall(r"^#@ shadowed ([a-z0-9]+(?:-[a-z0-9]+)*)==(\S+) record-sha256 ([0-9a-f]{64}|none)$",
                          text, re.M)
    assert sorted(shadowed) == [("cryptography", "41.0.7", "none"), ("packaging", "24.0", "none")]


# ── e02 · 합성 왕복 ───────────────────────────────────────────────────────────

def test_e02_synthetic_round_trip_matches(synth, tmp_path):
    ep = _ep()
    lock, text = _lock_for(ep, synth.paths, tmp_path / "c.lock.txt")
    assert ep.emit_lock(ep.parse_lock(text)) == text
    r = ep.compare_lock(lock, paths=synth.paths)
    _assert_closed(r)
    assert r["status"] == "MATCH", [(m["axis"], m["subject"]) for m in r["mismatches"]]
    assert r["lock_sha256"] == hashlib.sha256(lock.read_bytes()).hexdigest()
    assert r["counts"] == {"dists_locked": 11, "dists_measured": 11, "shadowed_locked": 1, "shadowed_measured": 1,
                           "files_verified": 21, "files_unhashed": 10, "origins_verified": 9}
    assert r["unverifiable"] == {"dists_without_record": ["pyyaml"], "origins": ["yaml"]}


# ── e03 · 축마다 정확히 그 축 ───────────────────────────────────────────────────

def _lock_side(change):
    return lambda text, s: (change(text), s.paths)


def _drop_line(text: str, pattern: str) -> str:
    out, n = re.subn(pattern, "", text, count=1, flags=re.M)
    assert n == 1, pattern
    return out


def _edit_extra_record(text: str) -> str:
    m = re.search(r"^extra-dist==1\.0  # record-sha256 ([0-9a-f]{64})$", text, re.M)
    return text.replace(m.group(0), m.group(0)[:-64] + _flip_hex(m.group(1)))


def _env_side(change):
    def run(text, s):
        return text, change(s)
    return run


def _touch_file(s):
    (s.site / "extra_mod_data.txt").write_bytes(b"data, changed after install\n")
    return s.paths


def _remove_file(s):
    (s.site / "extra_mod_data.txt").unlink()
    return s.paths


def _stray_copy(s):
    (s.stray / "numpy").mkdir()
    (s.stray / "numpy" / "__init__.py").write_bytes(b"# stray numpy, outside every RECORD\n")
    return [str(s.stray)] + s.paths


def _upgrade(s):
    shutil.rmtree(s.site / "extra_dist-1.0.dist-info")
    _make_dist(s.site, "extra-dist", "2.0", {"extra_mod.py": b"X = 1\n", "extra_mod_data.txt": b"data\n"})
    return s.paths


AXIS_CASES = {
    "python": (_lock_side(lambda t: _set_directive(t, "python", "0.0.0")), {"python"}),
    "implementation": (_lock_side(lambda t: _set_directive(t, "implementation", "OtherPython")), {"implementation"}),
    "system": (_lock_side(lambda t: _set_directive(t, "system", "OtherOS")), {"system"}),
    "machine": (_lock_side(lambda t: _set_directive(t, "machine", "other64")), {"machine"}),
    "libc": (_lock_side(lambda t: _set_directive(t, "libc", "otherlibc 0.0")), {"libc"}),
    "dist_missing": (_lock_side(lambda t: t + "zzz-absent==1.0  # record-sha256 none\n"), {"dist_missing"}),
    "dist_extra": (_lock_side(lambda t: _drop_line(t, r"^extra-dist==1\.0  # .*\n")), {"dist_extra"}),
    "dist_version": (_lock_side(lambda t: t.replace("\nextra-dist==1.0  #", "\nextra-dist==1.1  #")), {"dist_version"}),
    "dist_record": (_lock_side(_edit_extra_record), {"dist_record"}),
    "shadowed": (_lock_side(lambda t: _drop_line(t, r"^#@ shadowed extra-dist==0\.9 .*\n")), {"shadowed"}),
    "file_hash": (_env_side(_touch_file), {"file"}),
    "file_missing": (_env_side(_remove_file), {"file"}),
    "origin_stray": (_env_side(_stray_copy), {"origin"}),
    "env_upgrade": (_env_side(_upgrade), {"dist_version", "dist_record"}),
}


@pytest.mark.parametrize("case", sorted(AXIS_CASES))
def test_e03_each_axis_is_reported(synth, tmp_path, case):
    ep = _ep()
    _, text = _lock_for(ep, synth.paths, tmp_path / "base.lock.txt")
    change, want = AXIS_CASES[case]
    text2, paths = change(text, synth)
    lock = tmp_path / "case.lock.txt"
    lock.write_bytes(text2.encode("utf-8"))
    r = ep.compare_lock(lock, paths=paths)
    _assert_closed(r)
    assert r["status"] == "MISMATCH", f"status {r['status']}"
    got = {m["axis"] for m in r["mismatches"]}
    assert got == want, f"축 {sorted(got)}"


# ── e04 · 형식 오류 → UNMEASURED ──────────────────────────────────────────────

def _swap_first_two_dists(text: str) -> str:
    a, b = _dist_lines(text)[:2]
    return text.replace(a + "\n" + b + "\n", b + "\n" + a + "\n", 1)


def _dup_first_dist(text: str) -> str:
    a = _dist_lines(text)[0]
    return text.replace(a + "\n", a + "\n" + a + "\n", 1)


def _bad_record(text: str) -> str:
    a = _dist_lines(text)[0]
    return text.replace(a, a.rsplit(" ", 1)[0] + " XYZ", 1)


def _repeat_python(text: str) -> str:
    line = re.search(r"^#@ python .*$", text, re.M).group(0)
    return text + line + "\n"


MALFORMED = {
    "unknown_directive": lambda t: t + '#@ color "blue"\n',
    "duplicate_directive": _repeat_python,
    "missing_directive": lambda t: _drop_line(t, r"^#@ libc .*\n"),
    "bad_json_value": lambda t: re.sub(r"^#@ python .*$", "#@ python 3.11.15", t, count=1, flags=re.M),
    "profile_not_c": lambda t: t.replace('#@ profile "C"', '#@ profile "B"', 1),
    "unsorted": _swap_first_two_dists,
    "duplicate_dist": _dup_first_dist,
    "bad_record_field": _bad_record,
    "unnormalized_name": lambda t: t.replace("\nextra-dist==1.0  #", "\nExtra_Dist==1.0  #", 1),
    "garbage_line": lambda t: t + "this is not a lock line\n",
    "not_utf8": None,
    "missing_file": None,
}
NO_LINE = {"missing_directive", "not_utf8", "missing_file"}


@pytest.mark.parametrize("case", sorted(MALFORMED))
def test_e04_malformed_lock_is_unmeasured(synth, tmp_path, case):
    ep = _ep()
    _, text = _lock_for(ep, synth.paths, tmp_path / "base.lock.txt")
    lock = tmp_path / "case.lock.txt"
    if case == "not_utf8":
        lock.write_bytes(text.encode("utf-8") + b"\xff\xfe broken\n")
    elif case != "missing_file":
        bad = MALFORMED[case](text)
        assert bad != text
        lock.write_bytes(bad.encode("utf-8"))
    r = ep.compare_lock(lock, paths=synth.paths)
    _assert_closed(r)
    assert r["status"] == "UNMEASURED", f"status {r['status']}"
    if case == "missing_file":
        assert r["lock_sha256"] is None
    else:
        assert r["lock_sha256"] == hashlib.sha256(lock.read_bytes()).hexdigest()
    if case not in NO_LINE:
        assert re.search(r"줄 \d+", r["reason"]), r["reason"]


# ── e05 · 측정 예외 → UNMEASURED ─────────────────────────────────────────────

def _nameless(s, monkeypatch):
    di = s.site / "nameless-1.0.dist-info"
    di.mkdir()
    meta = b"Metadata-Version: 2.1\nVersion: 1.0\n"
    (di / "METADATA").write_bytes(meta)
    (di / "RECORD").write_text(f"{di.name}/METADATA,sha256={_b64(meta)},{len(meta)}\n{di.name}/RECORD,,\n",
                               encoding="utf-8")


def _unknown_algorithm(s, monkeypatch):
    di = s.site / "weird_dist-1.0.dist-info"
    di.mkdir()
    (s.site / "weird_mod.py").write_bytes(b"Y = 2\n")
    (di / "METADATA").write_bytes(b"Metadata-Version: 2.1\nName: weird-dist\nVersion: 1.0\n")
    (di / "RECORD").write_text(f"weird_mod.py,md77=AAAA,6\n{di.name}/RECORD,,\n", encoding="utf-8")


def _enumeration_raises(s, monkeypatch):
    import importlib.metadata as md

    def boom(*a, **k):
        raise RuntimeError("열거 실패 (시험)")
    monkeypatch.setattr(md, "distributions", boom)


MEASURE_FAILURES = {"nameless_dist": _nameless, "unknown_hash_algorithm": _unknown_algorithm,
                    "enumeration_raises": _enumeration_raises}


@pytest.mark.parametrize("case", sorted(MEASURE_FAILURES))
def test_e05_measurement_failure_is_unmeasured(synth, tmp_path, monkeypatch, case):
    ep = _ep()
    lock, _ = _lock_for(ep, synth.paths, tmp_path / "base.lock.txt")
    MEASURE_FAILURES[case](synth, monkeypatch)
    r = ep.compare_lock(lock, paths=synth.paths)
    _assert_closed(r)
    assert r["status"] == "UNMEASURED", f"status {r['status']}"
    assert r["lock_sha256"] == hashlib.sha256(lock.read_bytes()).hexdigest()


# ── e06 · 실제 환경 ─────────────────────────────────────────────────────────

def test_e06_real_environment_result_is_typed():
    ep = _ep()
    r = ep.compare_lock()
    _assert_closed(r)
    assert r["status"] in ("MATCH", "MISMATCH"), f"status {r['status']}: {r['reason']}"
    assert r["lock_path"] == "requirements-validation-C.lock.txt"
    assert r["lock_sha256"] == hashlib.sha256(LOCK.read_bytes()).hexdigest()
    assert r["counts"]["dists_locked"] == 170 and r["counts"]["shadowed_locked"] == 2
    # 고정 표 §4-1 — 측정 경로의 첫 항목 (프로젝트 root · 스크립트 디렉터리) 차이가 결과를 바꾸지 않는다는 근거.
    for d in (ROOT, ROOT / "tools", ROOT / "docs" / "22p_gap"):
        names = {p.name for p in d.iterdir()}
        assert not [n for n in names if n.endswith((".dist-info", ".egg-info"))], d
        assert not names & (set(KEY_MODULES) | {m + ".py" for m in KEY_MODULES}), d


# ── e07 · 핵심 module = 지문 축 ───────────────────────────────────────────────

def test_e07_key_modules_are_the_fingerprint_axes():
    ep = _ep()
    from src.io import env_fingerprint

    axes = [k for k in env_fingerprint() if k not in ("python", "platform", "machine", "smoothing_backend")]
    assert tuple(ep.KEY_MODULES) == tuple(axes) == KEY_MODULES


# ── e08 · CLI (기록 전용 — 세 상태 모두 rc 0) ─────────────────────────────────

def _cli(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, "-m", "tools.env_profile", *args], cwd=ROOT, env=env,
                          capture_output=True, encoding="utf-8", timeout=900)


def test_e08_cli_is_record_only(tmp_path):
    ep = _ep()
    text = LOCK.read_text(encoding="utf-8")
    off = tmp_path / "mismatch.lock.txt"
    off.write_bytes(_set_directive(text, "python", "0.0.0").encode("utf-8"))
    p = _cli("--lock", str(off))
    assert p.returncode == 0, f"rc {p.returncode} (MISMATCH) — 기록 전용이면 0"
    assert "MISMATCH" in p.stdout and re.search(r"^\s*✗ python ", p.stdout, re.M), "MISMATCH 요약 · python 축 줄 없음"
    broken = tmp_path / "broken.lock.txt"
    broken.write_bytes((text + "this is not a lock line\n").encode("utf-8"))
    p = _cli("--lock", str(broken))
    assert p.returncode == 0, f"rc {p.returncode} (UNMEASURED) — 기록 전용이면 0"
    assert "UNMEASURED" in p.stdout, "UNMEASURED 요약 없음"
    p = _cli("--json", "--lock", str(off))
    assert p.returncode == 0, f"rc {p.returncode} (--json)"
    r = json.loads(p.stdout)
    _assert_closed(r)
    assert r["status"] == "MISMATCH" and "python" in {m["axis"] for m in r["mismatches"]}
    p = _cli("--emit-lock")
    assert p.returncode == 0, f"rc {p.returncode} (--emit-lock)"
    assert ep.emit_lock(ep.parse_lock(p.stdout)) == p.stdout


# ── e09 · smoke 기록 단계 (정적) ──────────────────────────────────────────────

def test_e09_smoke_records_the_profile_once():
    lines = SMOKE.read_text(encoding="utf-8").splitlines()
    calls = [i for i, line in enumerate(lines) if "-m tools.env_profile" in line]
    assert len(calls) == 1, f"smoke 의 env_profile 호출 {len(calls)} 개"
    line = lines[calls[0]]
    assert line.lstrip().startswith('"$PY" -m tools.env_profile'), line
    assert re.search(r'\|\|\s*bad\s+"', line) and "|| true" not in line and "exit" not in line, line
    bad_def = next(i for i, x in enumerate(lines) if x.startswith("bad()"))
    step0 = next(i for i, x in enumerate(lines) if x.startswith('step "0.'))
    assert bad_def < calls[0] < step0, (bad_def, calls[0], step0)


# ── e10 · 영수증 stamp ───────────────────────────────────────────────────────

def test_e10_receipt_stamp_records_the_profile():
    mr = _make_receipt()
    st = mr._stamp()
    assert set(st) == {"_주의", "validator_commit", "validator_tree_dirty", "generated_at_utc", "runtime",
                       "environment_profile_C"}, sorted(st)
    _assert_closed(st["environment_profile_C"])
    assert st["environment_profile_C"]["lock_path"] == "requirements-validation-C.lock.txt"
    assert '"stamp": _stamp()' in inspect.getsource(mr.build)
    from tools.preserve import VERIFICATION_RECEIPT_KEYS

    assert VERIFICATION_RECEIPT_KEYS == frozenset({"schema_version", "_주의", "core_sha256", "core", "stamp"})


# ── e11 · B = 네 v4 producer manifest ────────────────────────────────────────

def _walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}.{k}" if path else str(k)
            yield p, k, v
            yield from _walk(v, p)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _walk(v, f"{path}[{i}]")


def test_e11_b_profile_is_the_v4_producer_record():
    import yaml

    b = yaml.safe_load(B_PROFILE.read_text(encoding="utf-8"))
    assert set(b) == {"profile", "kind", "sources", "env", "solver", "not_recorded", "not_claimed", "use"}
    assert b["profile"] == "B" and b["kind"] == "HISTORICAL_PRODUCER_RECORD_ONLY"
    assert [s["path"] for s in b["sources"]] == list(B_SOURCES)
    solver_seen = {}
    for s in b["sources"]:
        assert set(s) == {"path", "bytes", "sha256", "env_paths"}
        raw = (ROOT / s["path"]).read_bytes()
        assert s["bytes"] == len(raw) and s["sha256"] == hashlib.sha256(raw).hexdigest(), s["path"]
        doc = yaml.safe_load(raw)
        envs = {p: v for p, k, v in _walk(doc) if k == "env" and isinstance(v, dict)}
        assert s["env_paths"] == sorted(envs), s["path"]
        assert all(v == b["env"] for v in envs.values()), s["path"]
        for p, k, v in _walk(doc):
            if k in ("solver", "effective_solver"):
                solver_seen[f"{s['path']}:{p}"] = v
    assert b["solver"] == solver_seen
    assert list(b["env"]) == ["python", "platform", "machine", "numpy", "scipy", "pandas", "joblib", "pyarrow",
                              "pybamm", "matplotlib", "yaml", "pybammsolvers", "casadi"]
    for k in ("not_recorded", "not_claimed"):
        assert isinstance(b[k], list) and b[k] and all(isinstance(x, str) and x for x in b[k]), k
    assert isinstance(b["use"], str) and b["use"]
    # 기록 전용 — 어떤 실행 코드도 B 기록을 읽지 않는다 (고정 표 §6).
    for d in ("src", "tools", "scripts", "configs"):
        for f in (ROOT / d).rglob("*"):
            if f.is_file() and f.suffix in (".py", ".sh", ".yaml"):
                assert "env_profile_B_v4" not in f.read_text(encoding="utf-8", errors="replace"), f
    assert "env_profile_B_v4" not in (ROOT / "run.sh").read_text(encoding="utf-8")


# ── e12 · requirements 하한 유지 · 주석 정정 ───────────────────────────────────

def test_e12_requirements_bounds_kept_and_comment_corrected():
    text = REQ.read_text(encoding="utf-8")
    assert [line for line in text.split("\n") if line.strip() and not line.lstrip().startswith("#")] \
        == REQUIREMENT_LINES
    assert text.count("검증 완료 조합") == 1 and '옛 주석 "검증 완료 조합' in text
    assert "하한만" in text
    for rel in ("requirements-validation-C.lock.txt", "docs/22p_gap/env_profile_B_v4.yaml"):
        assert rel in text and (ROOT / rel).is_file(), rel
