"""62차 β′ (P0-2 · P1-1) — **잠금은 문자열이 아니라 커널이 판정한다.**

리뷰어 반례 (정상 interleaving 이다, 공격이 아니다):

    acquired_count 2
    contenders      [{pid: 31561, acquired}, {pid: 31560, acquired}]
    final_lock_body 한 PID만 남음

`[해석]` `acquire_run_lock()` 은 `path.exists()` 를 본 뒤 plain `write_text()`
를 했다 — check-then-overwrite 다. 두 contender 가 둘 다 "없다" 를 관측한 직후
쓰면 둘 다 성공하고, 파일에는 나중 것만 남는다. 청크·manifest 의 단일 writer
불변식이 그 순간 사라진다.

그리고 P1-1: `release_run_lock()` 은 **PID 문자열을 다시 읽어** 자기 것인지
추정했다. 읽을 수 없거나 비었으면 조용히 돌아갔고, "없는 lock·남의 lock 은
조용히" 가 규칙이었다. 리뷰어: 소유권을 문자열 재독으로 추정하지 말고
**acquire 가 돌려준 inode/nonce-bound handle 을 release 가 소비**해야 하며,
명시적 foreign owner 이외의 missing/replaced/malformed 는 own release 에서
fail-closed 여야 한다.

`[고침]` 잠금을 **token** 으로 바꾼다.

  · acquire: `O_CREAT` 로 열고 `flock(LOCK_EX|LOCK_NB)` — 배타는 커널의 한
    연산이 정한다. 죽은 프로세스의 lock 은 커널이 이미 풀어 뒀으므로 "stale
    회수" 라는 경쟁 구간 자체가 없다. `O_EXCL` 만 쓰면 stale 파일을 지우고 다시
    만드는 사이에 경쟁이 남는다 — 그래서 EXCL 이 아니라 flock 이다.
  · token 이 든 것: 디렉터리 fd · 이름 · lock 파일의 (dev, ino) · nonce.
    디렉터리 fd 를 들고 있으므로 `/proc/self/fd/N` 경로가 죽어도 놓을 수 있다
    — 그것이 P0-3(commit 뒤에 놓기)의 전제다.
  · release(token): 이름이 지금 가리키는 inode 가 token 의 것과 같을 때만
    unlink 한다. 없어졌거나(git clean) 바뀌었으면 **올린다**. 본문은 안 읽는다
    — 본문은 사람을 위한 정보이지 소유권이 아니다.
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


# ── P0-2 ──────────────────────────────────────────────────────────────────
def test_two_contenders_that_both_observe_absence_do_not_both_acquire(
        tmp_path, monkeypatch):
    """★ P0-2 — 리뷰어의 interleaving 을 그대로 고정한다.

    두 contender 가 **둘 다 "lock 이 없다" 를 관측한 직후** 쓴다. 옛 구현은
    `Path.exists()` 를 그 관측으로 썼으므로, 그 자리에 barrier 를 걸어 둘을
    같은 순간에 통과시킨다. 고친 구현은 `exists()` 를 아예 안 보므로 barrier
    는 걸리지 않고 — 그래도 하나만 성공해야 한다.
    """
    import src.io as io_mod

    barrier = threading.Barrier(2, timeout=5)
    real_cls = type(Path())

    class _RacyPath(real_cls):
        def exists(self, *a, **k):
            ok = super().exists(*a, **k)
            if self.name == ".run.lock":
                try:
                    barrier.wait()
                except threading.BrokenBarrierError:
                    pass
            return ok

    monkeypatch.setattr(io_mod, "Path", _RacyPath)
    results: list = []

    def _try():
        try:
            tok = io_mod.acquire_run_lock(tmp_path)
            results.append(("acquired", tok))
        except RuntimeError as e:
            results.append(("refused", str(e)))
        except Exception as e:                            # noqa: BLE001
            results.append(("error", repr(e)))

    ts = [threading.Thread(target=_try) for _ in range(2)]
    for t in ts:
        t.start()
    for t in ts:
        t.join(timeout=10)
    kinds = sorted(k for k, _ in results)
    assert kinds == ["acquired", "refused"], (
        f"두 contender 의 결과가 {kinds} — 정확히 하나만 잡아야 한다 (62차 P0-2): "
        f"{results}")
    for k, v in results:
        if k == "acquired":
            io_mod.release_run_lock(v)


def test_eight_processes_racing_for_one_lock_yield_exactly_one_holder(tmp_path):
    """★ P0-2 — 프로세스 경계를 넘는 실제 경쟁. 시간에 기대지 않고 **동시에 잡고
    있는 수**를 센다: 잡은 프로세스는 잡은 사실을 파일에 적고 잠깐 붙들고 있다.
    """
    prog = r"""
import sys, time, os
sys.path.insert(0, sys.argv[1])
from src.io import acquire_run_lock, release_run_lock
d = sys.argv[2]
try:
    tok = acquire_run_lock(d)
except RuntimeError:
    print("refused"); sys.exit(0)
with open(os.path.join(d, "holders.log"), "a") as fh:
    fh.write(f"in {os.getpid()} {time.monotonic_ns()}\n")
time.sleep(0.3)
with open(os.path.join(d, "holders.log"), "a") as fh:
    fh.write(f"out {os.getpid()} {time.monotonic_ns()}\n")
release_run_lock(tok)
print("held")
"""
    procs = [subprocess.Popen([sys.executable, "-c", prog, str(REPO), str(tmp_path)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True) for _ in range(8)]
    outs = [p.communicate(timeout=60)[0].strip() for p in procs]
    held = outs.count("held")
    assert held >= 1, f"아무도 못 잡았다: {outs} / {[p.returncode for p in procs]}"
    # 겹친 보유 구간이 있으면 두 프로세스가 동시에 lock 을 잡은 것이다
    log = (tmp_path / "holders.log").read_text(encoding="utf-8").splitlines()
    active = 0
    peak = 0
    for line in sorted(log, key=lambda s: int(s.split()[2])):
        active += 1 if line.startswith("in ") else -1
        peak = max(peak, active)
    assert peak == 1, f"동시에 잡은 프로세스가 {peak} 개다 (62차 P0-2): {log}"


# ── P1-1 ──────────────────────────────────────────────────────────────────
def test_acquire_returns_an_ownership_token_bound_to_the_inode(tmp_path):
    """★ P1-1 — release 가 소비하는 것은 경로가 아니라 **token** 이다."""
    from src.io import acquire_run_lock, release_run_lock

    tok = acquire_run_lock(tmp_path, ".x.lock")
    st = os.stat(tmp_path / ".x.lock")
    assert getattr(tok, "ino", None) == st.st_ino, "token 이 inode 를 안 들고 있다"
    assert getattr(tok, "dev", None) == st.st_dev
    assert getattr(tok, "nonce", None), "token 에 nonce 가 없다"
    body = (tmp_path / ".x.lock").read_text(encoding="utf-8")
    assert str(os.getpid()) in body and tok.nonce in body, (
        "lock 본문에 pid·nonce 가 없다 — 본문은 사람을 위한 정보다")
    release_run_lock(tok)
    assert not (tmp_path / ".x.lock").exists()


def test_release_refuses_a_lock_whose_name_now_points_at_another_inode(tmp_path):
    """★ P1-1 — 내 이름 아래 **다른 inode** 가 있으면 남의 것이다. 지우지 않고
    올린다 (조용히 돌아가지 않는다)."""
    from src.io import acquire_run_lock, release_run_lock

    tok = acquire_run_lock(tmp_path, ".x.lock")
    os.unlink(tmp_path / ".x.lock")                      # git clean 이 한 일
    (tmp_path / ".x.lock").write_text("999999 2026-01-01T00:00:00 deadbeef\n",
                                      encoding="utf-8")   # 남이 새로 만든 것
    with pytest.raises(RuntimeError, match="inode|바뀌|남의|replaced"):
        release_run_lock(tok)
    assert (tmp_path / ".x.lock").exists(), "남의 lock 을 지웠다"


def test_release_refuses_when_its_own_lock_has_vanished(tmp_path):
    """★ P1-1 — 내 lock 이 사라졌으면 배타가 이미 사라진 것이다. 그 사실은
    소리가 나야 한다 (옛 규칙 "없는 lock 은 조용히" 를 뒤집는다)."""
    from src.io import acquire_run_lock, release_run_lock

    tok = acquire_run_lock(tmp_path, ".x.lock")
    os.unlink(tmp_path / ".x.lock")
    with pytest.raises(RuntimeError, match="사라|missing|없"):
        release_run_lock(tok)


def test_a_truncated_body_does_not_change_who_owns_the_lock(tmp_path):
    """★ P1-1 — 소유권은 inode 다. 본문이 비어도(malformed) 내 inode 면 내 것이고,
    release 는 그것을 지운다. 옛 구현은 빈 본문에서 `IndexError` 를 삼키고
    "내 것이라 말할 수 없다" 며 **lock 을 남겼다**."""
    from src.io import acquire_run_lock, release_run_lock

    tok = acquire_run_lock(tmp_path, ".x.lock")
    with open(tmp_path / ".x.lock", "r+b") as fh:
        fh.truncate(0)
    release_run_lock(tok)
    assert not (tmp_path / ".x.lock").exists()


def test_the_path_based_release_is_gone(tmp_path):
    """★ P1-1 — 경로만 받고 문자열로 소유를 추정하는 release 경로는 **없어야**
    한다. 남겨 두면 그것이 조용한 우회로다."""
    from src.io import release_run_lock

    # `TypeError` **만** — 넓히면 isinstance 검사를 뺀 변이가 `AttributeError`
    # 로 통과한다 (변이 축을 심다 실측).
    with pytest.raises(TypeError, match="token"):
        release_run_lock(tmp_path, ".x.lock")


# ── stale · live ──────────────────────────────────────────────────────────
def test_a_dead_holders_lock_is_reclaimed_without_a_pid_string(tmp_path):
    """죽은 프로세스의 lock 은 커널이 이미 풀었다 — 본문의 PID 가 무엇이든."""
    from src.io import acquire_run_lock, release_run_lock

    (tmp_path / ".run.lock").write_text("garbage-not-a-pid\n", encoding="utf-8")
    tok = acquire_run_lock(tmp_path)
    release_run_lock(tok)


def test_a_live_holder_in_another_process_is_refused_by_pid(tmp_path):
    """살아 있는 보유자는 커널이 막고, 오류 문구는 그 PID 를 말한다."""
    from src.io import acquire_run_lock

    prog = r"""
import sys, os
sys.path.insert(0, sys.argv[1])
from src.io import acquire_run_lock, release_run_lock
tok = acquire_run_lock(sys.argv[2])
print(os.getpid(), flush=True)
sys.stdin.readline()
release_run_lock(tok)
"""
    p = subprocess.Popen([sys.executable, "-c", prog, str(REPO), str(tmp_path)],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        holder = p.stdout.readline().strip()
        assert holder.isdigit(), holder
        with pytest.raises(RuntimeError) as ei:
            acquire_run_lock(tmp_path)
        assert holder in str(ei.value), (
            f"오류 문구가 보유자 PID {holder} 를 안 말한다: {ei.value}")
    finally:
        p.stdin.write("\n")
        p.stdin.flush()
        p.wait(timeout=20)
    # 보유자가 놓은 뒤에는 잡힌다
    from src.io import release_run_lock
    tok = acquire_run_lock(tmp_path)
    release_run_lock(tok)


def test_lock_names_are_ignored_by_git(tmp_path):
    """서브 브랜치 R6 F06 의 교훈 — `git clean -fd` 가 lock 파일을 지우면 다음
    시도가 새 inode 를 잠가 배타가 사라진다. ignore 목록이 그것을 막는다."""
    ign = (REPO / ".gitignore").read_text(encoding="utf-8")
    for name in (".run.lock", ".fit.lock"):
        assert name in ign, f"{name} 이 .gitignore 에 없다 (62차 P0-2 · R6 F06)"
