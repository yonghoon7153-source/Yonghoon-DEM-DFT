"""전달 매니페스트 시험 — 검증기 자신에 시험이 없었다.

v0.1.10 은 **올바른 전달에 ⛔ 를 냈다.** `CHANGELOG_<ver>.md`(받는 쪽이 splice 하고 버림)와
`MANIFEST_<ver>.md`(전달 문서 자신)를 repo 에서 찾으니 항상 MISSING 이었다.
늑대가 왔다고 매번 외치는 검사는 두세 판 안에 아무도 안 보고, 그러면 **진짜 유실이 묻힌다.**

그래서 여기서 제일 중요한 시험은 "잡는다" 가 아니라 **"멀쩡한 전달에서 조용하다"** 이다.
검사 도구는 거짓 경보 하나가 참 경보 열보다 비싸다.
"""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_manifest.py"


def _run(*args: str) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(SCRIPT), *args],
                       capture_output=True, text=True, cwd=ROOT)
    return r.returncode, r.stdout + r.stderr


@pytest.fixture
def bundle(tmp_path):
    """전달 묶음(평면 디렉터리)을 흉내낸다 — 회신문·조각·매니페스트가 한 폴더에 있다."""
    (tmp_path / "VERSION").write_text("9.9.9\n", encoding="utf-8")
    (tmp_path / "CHANGELOG_9.9.9.md").write_text("## [9.9.9]\n조각\n", encoding="utf-8")
    return tmp_path


def _build(version: str, *args: str) -> str:
    rc, out = _run(version, *args)
    assert rc == 0, out
    return out


# ------------------------------------------------------------------ 생성
def test_manifest_lists_every_attachment_including_itself():
    """표 줄 수 == 첨부 개수가 성립해야 개수 대조를 기계가 한다."""
    out = _build("9.9.9", "VERSION", "--doc", "README.md")
    assert "| `VERSION` | code |" in out
    assert "| `README.md` | doc |" in out
    assert "| `MANIFEST_9.9.9.md` | transient |" in out, "매니페스트 자신이 표에 없다"
    assert out.count("\n| `") == 3


def test_self_row_has_no_hash():
    out = _build("9.9.9", "VERSION")
    self_row = [l for l in out.splitlines()
                if l.startswith("| `MANIFEST_9.9.9.md`")][0]  # 안내문이 아니라 표 행
    assert self_row.endswith("| `—` |"), "자기 참조인데 해시를 냈다"


def test_missing_file_is_reported_before_sending():
    out = _build("9.9.9", "VERSION", "존재하지_않는_파일.py")
    assert "보내는 쪽에서 찾지 못한 파일" in out and "존재하지_않는_파일.py" in out


# ------------------------------------------------------------------ ★ 거짓 경보 없음
def test_correct_delivery_is_silent_in_repo(tmp_path):
    """★ v0.1.10 회귀 — 멀쩡한 전달에서 ⛔ 가 뜨면 안 된다.

    `transient` 는 repo 에 그 이름으로 남지 않는 것이 **정상**이다.
    """
    man = tmp_path / "MANIFEST_9.9.9.md"
    man.write_text(_build("9.9.9", "VERSION", "--transient", "CHANGELOG_0.1.10.md"
                          if (ROOT / "CHANGELOG_0.1.10.md").exists() else "VERSION"),
                   encoding="utf-8")
    rc, out = _run("--verify", str(man))
    assert rc == 0, f"올바른 전달에 경보가 떴다:\n{out}"
    assert "⛔" not in out
    assert "skip" in out and "transient" in out


def test_transient_is_checked_when_given_the_bundle(bundle):
    """`--from` 이면 transient 까지 검사한다 — 복사 전에 확인하는 자리."""
    man_text = _build("9.9.9", "VERSION", "--transient", "CHANGELOG_0.1.10.md") \
        if (ROOT / "CHANGELOG_0.1.10.md").exists() else None
    # 묶음 기준 시험은 repo 파일에 의존하지 않도록 직접 구성한다
    rows = ["# m", "", "| 파일 | kind | 줄 | 바이트 | sha256[:16] |", "|---|---|---:|---:|---|"]
    import hashlib
    for name, kind in (("VERSION", "code"), ("CHANGELOG_9.9.9.md", "transient")):
        b = (bundle / name).read_bytes()
        rows.append(f"| `{name}` | {kind} | {b.count(chr(10).encode())} | {len(b)} | "
                    f"`{hashlib.sha256(b).hexdigest()[:16]}` |")
    man = bundle / "MANIFEST_9.9.9.md"
    man.write_text("\n".join(rows) + "\n", encoding="utf-8")
    rc, out = _run("--verify", str(man), "--from", str(bundle))
    assert rc == 0, out
    assert "skip" not in out, "--from 인데 transient 를 건너뛰었다"
    assert "[transient] CHANGELOG_9.9.9.md" in out


def test_bundle_mode_catches_a_file_that_never_left(bundle):
    """★ 이게 진짜 용도 — 묶음에 없는 파일을 **복사하기 전에** 잡는다 (v0.1.8 시나리오)."""
    man = bundle / "MANIFEST_9.9.9.md"
    man.write_text("| 파일 | kind | 줄 | 바이트 | sha256[:16] |\n|---|---|---:|---:|---|\n"
                   "| `research_agent/cli.py` | code | 10 | 100 | `deadbeefdeadbeef` |\n",
                   encoding="utf-8")
    rc, out = _run("--verify", str(man), "--from", str(bundle))
    assert rc == 1 and "MISSING" in out and "cli.py" in out
    assert "병합하지 말 것" in out


# ------------------------------------------------------------------ 진짜 경보는 뜬다
def test_mismatch_is_caught(tmp_path):
    man = tmp_path / "MANIFEST_9.9.9.md"
    man.write_text("| 파일 | kind | 줄 | 바이트 | sha256[:16] |\n|---|---|---:|---:|---|\n"
                   "| `VERSION` | code | 1 | 7 | `0000000000000000` |\n", encoding="utf-8")
    rc, out = _run("--verify", str(man))
    assert rc == 1 and "MISMATCH" in out


def test_missing_code_file_is_caught(tmp_path):
    man = tmp_path / "MANIFEST_9.9.9.md"
    man.write_text("| 파일 | kind | 줄 | 바이트 | sha256[:16] |\n|---|---|---:|---:|---|\n"
                   "| `research_agent/절대없는모듈.py` | code | 1 | 1 | `abcdefabcdefabcd` |\n",
                   encoding="utf-8")
    rc, out = _run("--verify", str(man))
    assert rc == 1 and "MISSING" in out


def test_old_format_manifest_says_so_instead_of_passing(tmp_path):
    """옛 형식을 '이상 없음'으로 통과시키면 안 된다 — 조용한 통과가 제일 나쁘다."""
    man = tmp_path / "old.md"
    man.write_text("| `x.py` | 1 | 2 | `abc` |\n", encoding="utf-8")
    rc, out = _run("--verify", str(man))
    assert rc == 2 and "갱신" in out
