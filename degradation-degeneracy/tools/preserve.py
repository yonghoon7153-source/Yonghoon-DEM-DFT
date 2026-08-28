"""preserve.py — 다리 생성을 **트랜잭션**으로 만든다 (계약 v4 묶음 9).

왜 이것이 필요한가
──────────────────
2026-08-20 에 warm 실험 7다리를 만들고 보존 없이 끝냈다. 나흘 뒤 작업 기계가
바뀌면서 원자료가 전부 사라졌다. **도구가 없어서가 아니다** —
`tools/archive_bundle.py` 는 이미 fail-closed 였고 `paired_fixed5_v4` 에서 실제로
작동했다. 없었던 것은 **강제**다: 다리를 만들고 보존을 안 해도 아무 일도
일어나지 않았다.

★ 26차 리뷰가 초판을 P0 둘로 반려했다. 둘 다 **false-green** 이었다:

  P0-1  복원이 CAS 가 아니라 **원본 `run_dir` 를 복사**했다. member 와
        manifest 를 backend 에 넣고 되읽기까지 했지만 되읽은 bytes 는 해시만
        확인하고 버렸다. read-back 직후 CAS 를 통째로 비워도 publish 까지
        성공했다. "빈 root 로 복원해 검증했다" 는 주장이 거짓이었다.
        → 복원은 이제 `backend + payload_manifest_digest` 만 본다.
          `drop_source_after_seal=True` 로 원본을 지우고도 통과하는 것을
          회귀가 확인한다.

  P0-2  receipt 를 메모리에서 만들고 **digest 만** index 에 적었다. 그 digest
        로 아무 것도 회수할 수 없으니 감사가 불가능했고, "등록" 은 상태 변경이
        아니라 단순 `return` 이었다.
        → receipt bytes 를 CAS 에 넣고 되읽는다. 등록은 durable journal 이고,
          crash 뒤에는 `finalize_only()` 가 **원본 없이** 이어서 끝낸다.

두 단계 불변식 (초판의 "어느 단계에서 멈추든 index 가 깨끗하다" 는 틀렸다 —
publish 뒤 crash 는 durable 한 중간 상태를 남긴다. 그것을 숨기지 않고 적는다):

    publish **전** 실패  →  public index 에 항목이 없다
    publish **후** 실패  →  항목은 durable 하게 남고 **등록되지 않은** 상태다.
                            `finalize_only()` 로만 닫힌다 (재계산 없이).

순서
────
    planned_leg seal            내용 주소. run_spec 이 없으면 시작하지 않는다
    → private temp 로 실행 (호출자)
    → payload seal              exact member manifest + root digest
    → CAS staging put-if-absent staging → os.replace 로만 objects/ 승격
    → read-back                 backend 에서 되읽어 다시 해시
    → **CAS 에서** 빈 root 복원  원본은 이 시점에 없어도 된다
    → validate + rescore        복원본만으로. hook 없으면 시작조차 안 한다
    → receipt 를 CAS 에 저장     + read-back
    → per-leg exclusive publish  read-modify-write 가 아니다
    → durable registration

backend
───────
`file+cas://<root>` 만 구현한다. 실제 cloud store 는 이 브랜치에서 검증할 수
없고 (자격증명·외부 인프라), 25차 Q1 이 "fault injection 가능한 local
content-addressed backend 로 트랜잭션 의미를 완전히 검증하면 된다" 고 답했다.
실제 운영 backend 의 canary receipt 는 첫 pilot 전 **별도 gate** 다.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import errno
import hashlib
import json
import os
import re
import secrets
import stat
import shutil
import tempfile
import unicodedata
import uuid
from dataclasses import dataclass
from typing import ClassVar, NamedTuple
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

#: 주입 가능한 실패 모드. 회귀가 이 이름들을 그대로 쓴다.
FAULTS = frozenset({
    "member_bit_flip",        # 봉인 뒤 member 한 바이트 변경
    "member_missing",         # manifest 에 있는 member 를 뺀다
    "member_extra",           # manifest 에 없는 파일이 run_dir 에 있다
    "stale_payload_index",    # payload manifest 가 실물보다 낡았다
    "partial_upload",         # CAS put 중간에 죽는다
    "crash_before_publish",   # 전부 성공했는데 publish 직전에 죽는다
    "crash_after_publish",    # publish 직후 등록 전에 죽는다
    "read_back_corrupt",      # backend 에서 되읽은 바이트가 다르다
    "restore_incomplete",     # 복원이 일부만 된다
    "cas_drop_member",        # ★ read-back 뒤 CAS 에서 member 를 지운다
    "cas_drop_manifest",      # ★ read-back 뒤 CAS 에서 manifest 를 지운다
    "cas_drop_all",           # ★ read-back 뒤 CAS 를 통째로 비운다
    "cas_mutate_member",      # ★ CAS 안의 바이트를 바꾼다
    "validator_raises",       # 검증기가 예외로 죽는다
    "validator_fails",        # 검증기가 ok=False 를 돌려준다
    "score_raises",           # 재채점이 예외로 죽는다
    "wrong_semantic_digest",  # 재채점 결과가 봉인과 다르다
    "wrong_planned_id",       # 실행이 다른 planned leg 를 가리킨다
    "wrong_source_digest",    # run_spec 의 code identity 가 계획과 다르다
    "receipt_drop_after_readback",   # ★ receipt 를 되읽은 직후 지운다
    "receipt_mutate_after_readback",  # ★ 되읽은 직후 바이트를 바꾼다
    "receipt_drop_after_publish",     # ★ publish 뒤 등록 전에 지운다
    "retention_too_short",    # backend 의 보존 기간이 요구를 못 채운다
    "no_read_access",         # backend 를 되읽을 권한이 없다
})

_HEX64 = 64

#: opaque ID 의 허용 문자·길이. ★ 27차 P1-4 — `leg_id` 가 path component 로
#: 그대로 보간돼 `../../escaped` 가 index 디렉터리 **밖에** 파일을 만들었다.
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
#: Windows 예약 device 이름 — 파일로 만들 수 없거나 이상하게 동작한다
_RESERVED = frozenset({"con", "prn", "aux", "nul"}
                      | {f"com{i}" for i in range(1, 10)}
                      | {f"lpt{i}" for i in range(1, 10)})


def check_id(name: str, kind: str = "leg_id") -> None:
    """separator · `.`/`..` · device name · 길이를 닫는다."""
    if not isinstance(name, str) or not _ID_RE.match(name):
        raise PreserveError("id", f"{kind} 가 허용 형식이 아니다: {name!r} "
                                  "(첫 글자 영숫자, 이후 [A-Za-z0-9_.-], 64자 이내)")
    if name in (".", "..") or name.lower().split(".")[0] in _RESERVED:
        raise PreserveError("id", f"{kind} 로 쓸 수 없는 이름이다: {name!r}")


class PreserveError(RuntimeError):
    """트랜잭션이 멈춘 이유. `stage` 가 어디서 멈췄는지 들고 있다."""

    def __init__(self, stage: str, msg: str):
        super().__init__(f"[{stage}] {msg}")
        self.stage = stage
        self.msg = msg


# ─────────────────────────────────────────────────────────────────────────────
# canonical bytes — 묶음 2 와 같은 규칙을 쓴다 (한 곳에서 정의)
# ─────────────────────────────────────────────────────────────────────────────

def canonical_bytes(obj) -> bytes:
    """정규 직렬화. 키 정렬 · UTF-8 · 구분자 고정 · 후행 개행 없음."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def load_canonical(raw: bytes):
    """`canonical_bytes` 의 역. 회수한 object 를 되돌린다."""
    return json.loads(raw.decode("utf-8"))


def digest(obj) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def _is_hex64(s) -> bool:
    return isinstance(s, str) and len(s) == _HEX64 and \
        all(c in "0123456789abcdef" for c in s)


#: ★ 29차 P1-1 — Windows 에서 `O_BINARY` 가 없으면 newline 이 번역된다.
#:   리뷰 실측: `b"a\nb"` 를 넣으면 `b"a\r\nb"` 가 저장돼 digest 가 어긋났다.
_O_BIN = getattr(os, "O_BINARY", 0)


def _write_exact(path: Path, data: bytes) -> None:
    """binary 로 **전부** 쓰고 fsync 한다. zero-return 은 오류로 본다."""
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | _O_BIN, 0o644)
    try:
        n = 0
        while n < len(data):
            w = os.write(fd, data[n:])
            if w <= 0:                                    # pragma: no cover
                raise PreserveError("write", f"쓰기가 0을 돌려줬다 ({path})")
            n += w
        os.fsync(fd)
    finally:
        os.close(fd)


def _fsync_dir(d: Path) -> bool:
    """directory entry 를 flush 한다. **실패를 삼키지 않는다.**

    ★ 30차 P0-3 — 초판은 실패를 `False` 로 돌렸고 object publish 와 pin 은
      그 반환값을 **무시했다**. CAS 와 index 가 다른 filesystem 이면 power
      loss 뒤 journal 만 남는 ordering 이 그대로 가능했다. 지금은
      `_fsync_dir_strict()` 가 오류로 전파하고, capability 가 아예 없는
      filesystem 은 `dir_fsync_supported()` 가 **만들기 전에** 걸러낸다.
    """
    try:
        fd = os.open(d, os.O_RDONLY)
    except OSError:
        return False
    try:
        os.fsync(fd)
        return True
    except OSError:                                       # pragma: no cover
        return False
    finally:
        os.close(fd)


def _fsync_dir_strict(d: Path, stage: str) -> None:
    """directory entry 를 굳힌다. 못 굳히면 **그 자리에서 멈춘다**.

    ★ 31차 P0-3 — 30차판은 capability 가 없으면 조용히 `return` 했다. 주석은
      "publish 경로가 이미 막는다" 였는데, 그것은 CAS 와 index 가 **같은
      filesystem** 일 때만 참이다. CAS 에서 directory fsync 가 안 되고 index
      에서는 되는 구성이면 graph 이름은 비내구적으로 진행하고 journal 만
      durable 하게 commit 된다 — 리뷰가 지목한 ordering 이 그대로 열린다.
      (실측: 그 구성에서 `put_if_absent()` 가 그냥 성공했다.)
    """
    if not dir_fsync_supported(d):
        raise PreserveError(
            stage, f"이 filesystem 은 directory fsync 를 지원하지 않는다 ({d}) — "
                   "graph 이름이 durable 하지 않으면 journal 만 남는 ordering 이 "
                   "가능하다. backend capability 를 확인하고 멈춘다")
    if not _fsync_dir(d):
        raise PreserveError(
            stage, f"directory fsync 가 실패했다 ({d}) — 이름이 durable 하지 "
                   "않으면 crash 뒤 journal 만 남는 ordering 이 가능하다")


def _mkdir_durable(d: Path, stage: str) -> None:
    """directory 를 만들고 **새로 만들어진 모든 층의 부모 edge** 를 flush 한다.

    ★ 30차 P0-3 — 초판은 `objects/<prefix>` 와 `pins/<leg>` 를
      `mkdir(parents=True)` 로 만든 뒤 **자기 자신만** flush 했다. 그 이름을
      담는 `objects/` · `pins/` entry 는 flush 되지 않아, crash 뒤 상위
      directory 에서 이름이 사라질 수 있었다.
    """
    d = Path(d)
    # ★ 32차 P0-3 — 초판은 `d.is_dir()` 이면 즉시 return 했다. "mkdir 은
    #   성공했지만 parent fsync 가 실패한" 상태와 "이미 durable" 한 상태를
    #   구별하지 못하므로, 재시도가 edge 를 다시 굳히지 않았다. 구별할 방법이
    #   없으면 **항상 굳힌다** — fsync 는 멱등이고 비용은 재시도 때만 든다.
    missing = []
    p = d
    while not p.exists():
        missing.append(p)
        p = p.parent
    d.mkdir(parents=True, exist_ok=True)
    layers = list(reversed(missing)) or [d]
    for made in layers:               # 얕은 층부터 — 부모 entry 를 먼저 굳힌다
        _fsync_dir_strict(made.parent, stage)


def _is_uuid_hex(s) -> bool:
    return isinstance(s, str) and len(s) == 32 and all(c in "0123456789abcdef" for c in s)


#: ★ 30차 P0-1 — `ok=True` 가 durable retention 을 뜻하면 안 된다.
#:
#:   리뷰의 문장: "그 전에는 `ok=True`를 durable retention 성공으로 부르면
#:   안 된다." local filesystem 에서는 **어떤 검사를 몇 번 하든** 마지막
#:   검사와 반환 사이의 창을 닫을 수 없다. 이 환경은 uid 0 이라 directory
#:   mode bit 도 잠금이 아니다 (실측: `chmod 0o500` 뒤에도 unlink 가 성공).
#:
#:   그래서 검사를 더 두는 대신 **성공의 뜻을 좁힌다.** 강제 수준을 값으로
#:   신고하고, durable retention 을 요구하는 자리는 그 값을 보고 거부한다.
#:   비싼 본 실행을 승인하는 gate 가 그 자리다.
ENFORCEMENT_ADVISORY = "advisory_local"
ENFORCEMENT_OBJECT_LOCK = "object_lock"
RETENTION_SCHEMA = "retention-lease/v1"
STORE_SCHEMA = "cas-store/v1"

#: 최소 보존 기간 정책 — lease·receipt 가 이보다 짧다고 적으면 거부한다
MIN_RETENTION_DAYS = 365

#: ★ 36차 P0-1 — adapter 계약의 **유일한 authority**.
#:
#:   35차까지 계약은 `ObjectLockBackend` docstring 의 산문 7줄이었는데 코드는
#:   `store_uri`·`head_version` 도 불렀다. 그 문서만 보고 adapter 를 쓰면
#:   실물에서 `PreserveError("capability")` 로 죽는다. 산문과 호출이 갈라지는
#:   것을 사람이 지키게 두지 않는다 — 이 상수가 정본이고,
#:   `tests/test_preserve.py::test_the_provider_contract_is_the_only_authority`
#:   가 소스를 AST 로 읽어 **실제 호출 집합과 정확히 일치**하는지 대조한다.
PROVIDER_CONTRACT: tuple[str, ...] = (
    "describe",         # describe() -> {mode, min_retain_days}
    "describe_object",  # describe_object(key, version) -> {version_id, mode, retain_until} | None
    "get",              # get(key, version=None) -> bytes
    # list_versions(prefix) -> [(key, version_id)]
    #   ★ 40차 — 39차 주석은 "marker 를 넘는다" 였는데 구현은 **data version 만**
    #     돌려준다 (delete marker 는 제외). 실물 `ListObjectVersions` 는 marker 도
    #     함께 주지만 우리가 쓰는 것은 data version 이고, marker 뒤의 담보를 볼 수
    #     있으면 목적은 달성된다. 계약을 구현에 맞춘다 — 산문이 더 강하면 adapter
    #     작성자가 없는 보장을 믿는다.
    "list_versions",
    "lock",             # lock(key, version, until)
    "put",              # put(key, data) -> version_id — **새 version 을 만든다**
    "store_uri",        # store_uri() -> str — 재시작을 견디는 안정 식별자
    "versions",         # versions(key) -> [version_id] (최신순)
)


class VerifiedBytes(NamedTuple):
    """검증이 **읽은 바로 그것** — key·version·digest·bytes 를 함께 든다.

    ★ 42차 P1 — 41차까지 검증 phase 는 exact `(key, version)` 을 읽어 판정하고
      **digest 문자열 하나만** 다음 phase 로 넘겼다. 다음 phase 는 그 digest 로
      namespace 를 다시 뒤졌고, 그 사이 hostile locked head 하나가 있으면
      **검증에 성공한 바이트가 있는데도** 재개가 막혔다 (orphan 입양 ·
      content 수리 둘 다 그랬다).

      즉시 bool 로 끝나는 predicate 는 digest 로 충분하다. 판정이 **phase 를
      넘어가면** 그때는 locator 여야 한다 — 이것이 그 경계다.
    """

    key: str
    version: str
    digest: str
    data: bytes


class RetentionProof(NamedTuple):
    """수리가 **실제로 만든** 담보 proof — 기한까지 함께 든다 (43차 P1).

    ★ 42차까지 `repair_lease_locks()` 는 두 wrapper 가 돌려준 proof ID 를
      버리고 `None` 을 반환했다. 호출자는 곧바로 **기한 인자 없는**
      `recover_*()` 로 다시 찾았고, 같은 바이트의 더 최신·더 짧은 Compliance
      version 이 있으면 그것을 골라 검증에서 죽었다 — 기한을 덮는 v1 이
      그대로 있는데도. 찾은 것을 버리고 다시 찾으면 phase 결속이 풀린다.
    """

    lease_version: str
    content_version: str
    until: str


#: store record 의 **닫힌** schema. 남는 key 도 모자란 key 도 거부한다 (37차 P0-1).
_STORE_KEYS = {"schema", "store_id"}


def _is_store_record(rec) -> bool:
    """계약 그대로의 store record 인가.

    ★ 37차 P0-1 — 36차판은 mapping 과 32-hex `store_id` 만 봤다. exact key
      set 도 `schema` 값도 안 봐서, 남는 key 를 단 record 나 다른 schema 의
      record 가 잠겨서 canonical identity 로 받아들여졌다.
    """
    return (isinstance(rec, dict)
            and set(rec) == _STORE_KEYS
            and rec.get("schema") == STORE_SCHEMA
            and _is_uuid_hex(rec.get("store_id") or ""))


def _is_utc_stamp(v) -> bool:
    """`YYYY-MM-DDTHH:MM:SSZ` 인가 (39차 P0-1).

    ★ `_lease_expired()` 는 **문자열 비교**라 `"not-a-date"` 를 미래처럼
      받아들인다. 그 값이 provider lock 까지 흘러간 뒤에야 strict parser 가
      거부했다 — 되돌릴 수 없는 상태가 검증보다 앞섰다.
    """
    if not isinstance(v, str):
        return False
    try:
        dt.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def _horizon_covers(state, want: str, what: str, stage: str = "retention"):
    """provider 가 신고한 `retain_until` 이 `want` 를 **덮는가** (40차 P0-1).

    ★ 39차까지는 문자열 비교였다:

            str(state.get("retain_until") or "") < lease["retain_until_utc"]

      `"zzzz"` 는 어떤 ISO 문자열보다 사전식으로 크므로 "충분한 미래
      horizon" 으로 통과했다. lease record 쪽에는 문법 검사를 넣어 놓고
      **provider 응답**은 열어 뒀다. 실제 adapter 가 아직 없다는 것은 검사를
      생략할 이유가 아니라 계약을 fail-closed 로 고정할 이유다.
    """
    got = (state or {}).get("retain_until")
    if not _is_utc_stamp(got):
        raise PreserveError(
            stage, f"{what} 의 retain_until 이 UTC timestamp 가 아니다: "
                   f"{got!r} — 문자열 순서는 기한 증명이 아니다")
    if not _is_utc_stamp(want):
        raise PreserveError(stage, f"{what} 와 대조할 기한이 이상하다: {want!r}")
    if _stamp(got) < _stamp(want):
        raise PreserveError(
            stage, f"{what} 의 기한이 짧다: {got} < {want}")


def _stamp(v: str) -> dt.datetime:
    return dt.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc)


def _durable_mode(state, want_mode, what: str, modes, stage: str = "retention"):
    """그 version 의 mode 가 lease 가 신고한 mode 와 같은가.

    ★ 40차 P0-1 — 39차는 이 **동등성만** 봤고, 그 값이 허용된 담보 mode 인지는
      아무도 안 봤다. 둘 다 Governance 인 self-consistent state 가 durable
      false-green 이었다. "서로 같다" 와 "허용된 값이다" 는 다른 축이다.

      membership 은 **lease record 쪽 한 곳**에서 본다 (`lock_mode` ·
      `store_lock_mode`). lease mode 가 담보 mode 이고 모든 version 이 그것과
      같으면 모든 version 이 담보 mode 다 — 여기에 membership 을 한 번 더 두면
      같은 규칙이 두 곳에 생기고, 강한 쪽을 지워도 초록이 된다 (변이로
      확인했다). `modes` 는 호출부 호환을 위해 남기고 쓰지 않는다.
    """
    got = (state or {}).get("mode")
    if want_mode is not None and got != want_mode:
        raise PreserveError(
            stage, f"{what} 의 lock mode 가 lease 와 다르다: {got!r} ≠ {want_mode!r}")


def _lease_expired(lease: dict) -> bool:
    """lease 의 담보 기간이 지났는가 (37차 P0-1).

    "만료라서 새로 만든다" 와 "어긋나서 거부한다" 를 가르는 유일한 기준이다 —
    36차판은 둘을 같은 `None` 으로 접었다.
    """
    until = str((lease or {}).get("retain_until_utc") or "")
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return not until or until <= now


def pin_set_digest(leg_id: str, objects) -> str:
    """pin 집합의 정본 digest — journal·lease·backend 가 **같은 함수**를 쓴다.

    ★ 30차 P1-1 — 초판은 `backend.pin()` 안에만 이 계산이 있었고, journal 의
      `pin_set_digest` 는 64-hex 모양만 검사했다. 기대 graph 로 다시 계산하지
      않으니 **journal 자기 checksum** 이었다.
    """
    return digest({"leg_id": leg_id, "objects": sorted(set(objects))})


def _is_unique_hex64_list(v) -> bool:
    """정렬된 unique 64-hex 목록인가.

    ★ 30차 P1-1 — 초판은 `set(journal.objects) == expected` 만 봤다. 정상
      목록의 digest 하나를 **한 번 더** 넣어도 통과했다.
    """
    if not isinstance(v, list) or not all(_is_hex64(x) for x in v):
        return False
    return len(set(v)) == len(v) and v == sorted(v)



def _file_sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ─────────────────────────────────────────────────────────────────────────────
# content-addressed backend
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class CasBackend:
    """`file+cas://<root>` — digest 로 주소가 정해지는 object store.

    `objects/` 에는 **검증을 통과한 것만** 들어간다. 쓰기는 `staging/` 에
    임시 이름으로 하고 `os.replace` 로 원자적으로 옮긴다. 중간에 죽으면
    staging 에 orphan 이 남고 `objects/` 는 오염되지 않는다.
    """

    root: Path
    retention_days: int = 3650
    readable: bool = True

    #: 이 **클래스**가 강제할 수 있는 retention 수준. local filesystem 은
    #: object-lock 을 강제하지 못한다 — 이 저장소의 실행 환경은 uid 0 이라
    #: mode bit 조차 잠금이 아니다.
    #:
    #: ★ 31차 P0-1 — 30차판은 이것이 **dataclass field** 였다. 리뷰의 정적
    #:   반례가 그대로 통했다: `CasBackend(root=cas, enforcement="object_lock")`
    #:   하나로 구현은 그대로인 채 `durable=True` 가 나오고
    #:   `assert_durable_retention()` 이 통과했다. "durable 의 뜻을 좁혔다" 는
    #:   경계가 문자열 하나로 무너진 것이다.
    #:
    #:   이제 ClassVar 다 — 생성자 인자가 아니고, 대입도 `__setattr__` 이
    #:   막는다. 강제 수준은 **구현이 정하는 것**이지 호출자가 붙이는 이름이
    #:   아니다. `object_lock` 을 주장하려면 `probe_enforcement()` 를 실제로
    #:   통과하는 다른 클래스를 만들어야 한다.
    ENFORCEMENT: ClassVar[str] = ENFORCEMENT_ADVISORY

    #: capability 를 바꿔치기하려는 대입을 막는다 (읽기는 자유)
    _LOCKED_ATTRS: ClassVar[frozenset] = frozenset({"ENFORCEMENT", "enforcement"})

    def __post_init__(self):
        # ★ 31차 P0-2 hardening — `root` 를 **생성 시** 고정한다. 초판은
        #   `uri` property 가 호출 때마다 cwd 기준으로 다시 계산해, 같은
        #   backend 객체가 cwd 변경만으로 다른 store 를 가리켰다.
        object.__setattr__(self, "root", Path(self.root).absolute())

    def __setattr__(self, name, value):
        if name in type(self)._LOCKED_ATTRS:
            raise PreserveError(
                "capability",
                f"{name} 은 backend capability 다 — 대입으로 바꿀 수 없다. "
                "강제 수준은 구현이 정한다")
        object.__setattr__(self, name, value)

    @property
    def enforcement(self) -> str:
        return type(self).ENFORCEMENT

    def probe_enforcement(self) -> str:
        """**지금** 이 store 가 실제로 강제하는 수준을 조회한다.

        ★ 31차 P0-1 — 리뷰: "저장 문자열이 아니라 provider 의 live lock
          state 조회". local 은 조회할 provider 가 없고 강제하는 것도 없다.
          object-lock backend 는 이 자리에서 provider 에 물어 version ID ·
          lock mode · retain-until 을 확인하고 그 결과로 답해야 한다.
        """
        return ENFORCEMENT_ADVISORY

    #: ★ 38차 P0-1 — local backend 에는 version 이 없다. lease 계약을 맞추기
    #:   위한 빈 값이다 (object-lock backend 가 실제 proof 를 채운다).
    store_version_id = ""
    store_lock_mode = ""

    @property
    def uri(self) -> str:
        """★ 30차 P0-2 — 초판은 `f"file+cas://{self.root}"` 였다.

        `root=Path("cas")` 로 등록한 뒤 cwd 를 바꾸면 **다른** store 를 가리키면서
        URI 는 그대로였다. 절대 경로로 정규화한다.
        """
        return Path(self.root).resolve().as_uri().replace("file://", "file+cas://", 1)

    @property
    def store_id(self) -> str:
        """store 를 만들 때 한 번 정해지는 불변 식별자.

        ★ 30차 P0-2 — 경로는 재사용·재마운트·bind mount 로 겹칠 수 있다.
        절대 URI 만으로는 "같은 store 인가" 를 답할 수 없어서, 생성 시각에
        고정되는 UUID 를 store 안에 두고 receipt 에 결속한다.
        """
        p = Path(self.root) / "store.json"
        if p.is_file():
            rec = load_canonical(p.read_bytes())
            sid = rec.get("store_id") if isinstance(rec, dict) else None
            if not _is_hex64(sid or "") and not _is_uuid_hex(sid or ""):
                raise PreserveError("store", f"store.json 의 store_id 가 이상하다: {sid!r}")
            return sid
        # ★ 32차 P0-3 — 초판은 `mkdir(parents=True)` 만 했다. CAS root 라는
        #   **이름**을 담은 parent entry 를 굳히지 않아, power loss 뒤 CAS 가
        #   통째로 사라지고 다른 filesystem 의 journal 만 남을 수 있었다.
        _mkdir_durable(Path(self.root), "store")
        data = canonical_bytes({"schema": STORE_SCHEMA, "store_id": uuid.uuid4().hex})
        _exclusive_write(p, data)                 # 경쟁하면 먼저 쓴 쪽이 이긴다
        return load_canonical(p.read_bytes())["store_id"]

    def identity(self) -> dict:
        return {"uri": self.uri, "store_id": self.store_id,
                "enforcement": self.enforcement}

    def _obj(self, dg: str) -> Path:
        return self.root / "objects" / dg[:2] / dg

    def put_if_absent(self, data: bytes, *, faults: frozenset[str] = frozenset()) -> dict:
        dg = hashlib.sha256(data).hexdigest()
        dst = self._obj(dg)
        if dst.exists():
            if dst.read_bytes() != data:
                raise PreserveError("cas_put",
                                    f"같은 digest 인데 저장된 바이트가 다르다: {dg[:16]}")
            # ★ 32차 P0-3 — 이름이 보인다고 durable 한 것이 아니다. `os.replace`
            #   성공 뒤 fsync 가 실패해 예외가 나갔어도 final name 은 남는다.
            #   재시도가 여기로 들어와 그냥 성공하면 graph 이름은 비내구적인 채
            #   journal 만 durable 하게 commit 될 수 있다. 성공 전에 굳힌다.
            _fsync_dir_strict(dst.parent, "cas_put")
            return {"digest": dg, "stored": False, "idempotent": True}

        staging = self.root / "staging"
        _mkdir_durable(staging, "cas_put")
        tmp = staging / f"{dg}.{uuid.uuid4().hex}.part"
        payload = data[: len(data) // 2] if "partial_upload" in faults else data
        # ★ 28차 P1-2 / 29차 P1-1 — binary 로 전부 쓰고 fsync 한다.
        _write_exact(tmp, payload)
        if "partial_upload" in faults:
            raise PreserveError("cas_put", "업로드가 중간에 끊겼다 (주입)")
        # ★ 30차 P0-3 — `objects/<prefix>` 를 새로 만들면 그 이름을 담은
        #   `objects/` entry 도 굳혀야 한다. 초판은 자기 자신만 flush 했다.
        _mkdir_durable(dst.parent, "cas_put")
        os.replace(tmp, dst)
        # ★ 29차 P0-2 / 30차 P0-3 — 실패를 삼키지 않는다.
        _fsync_dir_strict(dst.parent, "cas_put")
        return {"digest": dg, "stored": True, "idempotent": False}

    def read_back(self, dg: str, *, faults: frozenset[str] = frozenset()) -> bytes:
        if "no_read_access" in faults or not self.readable:
            raise PreserveError("read_back", "backend 를 되읽을 권한이 없다")
        p = self._obj(dg)
        if not p.is_file():
            raise PreserveError("read_back", f"object 가 없다: {dg[:16]}")
        data = p.read_bytes()
        if "read_back_corrupt" in faults:
            data = data + b"\x00"
        got = hashlib.sha256(data).hexdigest()
        if got != dg:
            raise PreserveError("read_back",
                                f"되읽은 바이트가 다르다: {got[:16]} ≠ {dg[:16]}")
        return data

    def has(self, dg: str) -> bool:
        return self._obj(dg).is_file()

    # ── retention / pin ─────────────────────────────────────────────────
    # ★ 28차 P0-1 — "등록 직전 한 번 더 읽는다" 는 **또 하나의 검사 시점**일
    #   뿐 retention 구조가 아니다. 마지막 read 가 bytes 를 돌려준 직후 지우면
    #   등록이 성립하면서 receipt 가 사라졌다.
    #
    #   local 에서 object-lock 의 대응물은 **hardlink** 다. `pins/<leg>/<dg>`
    #   가 inode 를 붙들므로 `objects/` 에서 지워도 회수 가능성이 유지된다.
    #   원격 backend 에서는 object-lock / retention-until 로 구현한다.

    def _pin(self, leg_id: str, dg: str) -> Path:
        return self.root / "pins" / leg_id / dg

    def pin(self, leg_id: str, digests) -> dict:
        """도달 가능한 object 를 전부 붙든다. 하나라도 없으면 실패한다."""
        check_id(leg_id)
        made = []
        for dg in sorted(set(digests)):
            src, dst = self._obj(dg), self._pin(leg_id, dg)
            # ★ 29차 P0-4 — 초판은 `os.link` 의 **모든** OSError 를 잡아
            #   `dst.write_bytes(...)` 로 떨어졌다. `EEXIST` 도 그리로 갔고
            #   `dst` 는 CAS `src` 와 같은 inode 라 `O_TRUNC` 로 열리는 순간
            #   content-addressed **원본까지 잘렸다**. 보존 체계가 보존 대상을
            #   지우는 경로였다. 기존 경로에는 **절대 쓰지 않는다.**
            if os.path.lexists(dst):
                if dst.is_symlink():
                    raise PreserveError("pin", f"pin 자리에 symlink 가 있다: {dg[:16]}")
                got = hashlib.sha256(dst.read_bytes()).hexdigest()
                if got != dg:
                    raise PreserveError(
                        "pin", f"pin 자리에 다른 내용이 있다: {dg[:16]} ≠ {got[:16]}")
                # ★ 32차 P0-3 — object 와 같은 이유로 성공 전에 굳힌다.
                _fsync_dir_strict(dst.parent, "pin")
                made.append(dg)
                continue
            if not src.is_file():
                raise PreserveError("pin", f"pin 할 object 가 없다: {dg[:16]}")
            # ★ 30차 P0-3 — `pins/<leg>` 를 새로 만들면 `pins/` entry 도 굳힌다
            _mkdir_durable(dst.parent, "pin")
            try:
                os.link(src, dst)
            except FileExistsError:               # 경쟁 — 위와 같은 규칙으로
                got = hashlib.sha256(dst.read_bytes()).hexdigest()
                if got != dg:
                    raise PreserveError("pin", f"경쟁 pin 의 내용이 다르다: {dg[:16]}")
            except OSError:                       # hardlink 불가 FS — 안전 복사
                t = dst.parent / f".{dg}.{uuid.uuid4().hex}.tmp"
                _write_exact(t, src.read_bytes())
                try:
                    os.link(t, dst)               # no-replace commit
                except FileExistsError:
                    pass
                finally:
                    t.unlink(missing_ok=True)
            _fsync_dir_strict(dst.parent, "pin")
            made.append(dg)
        return {"leg_id": leg_id, "pinned": made,
                "pin_set_digest": pin_set_digest(leg_id, made)}

    def pinned(self, leg_id: str) -> set:
        d = self.root / "pins" / leg_id
        return {p.name for p in d.iterdir()} if d.is_dir() else set()

    def read_pinned(self, leg_id: str, dg: str, *, version=None) -> bytes:
        """**pin 에서** 읽는다. `objects/` 가 비어도 회수돼야 한다.

        local backend 에는 version 이 없으므로 `version` 은 무시한다 (계약을
        맞추기 위한 인자다 — 37차 P0-1).
        """
        p = self._pin(leg_id, dg)
        if not p.is_file():
            raise PreserveError("pin", f"pin 이 없다: {dg[:16]}")
        data = p.read_bytes()
        if hashlib.sha256(data).hexdigest() != dg:
            raise PreserveError("pin", f"pin 바이트가 digest 와 다르다: {dg[:16]}")
        return data

    def verify_pins(self, leg_id: str, digests, versions: dict | None = None) -> list:
        """pin 집합이 완전하고 **바이트가 맞는지** 확인한다.

        ★ 38차 P0-1 — `versions` 를 주면 **그 version 을** 읽는다. 37차판은
          lease 의 `object_versions` 를 버리고 최신 담보 version 을 다시
          찾았다. 그래서 적대적 새 version 하나가 등록 검증을 깼다 — 봉인된
          version 은 멀쩡한데도.
        """
        bad = []
        vs = versions or {}
        for dg in sorted(set(digests)):
            try:
                self.read_pinned(leg_id, dg, version=vs.get(dg))
            except PreserveError as e:
                bad.append(f"{dg[:16]}: {e.msg}")
        return bad

    def orphans(self) -> list[Path]:
        st = self.root / "staging"
        return sorted(st.glob("*.part")) if st.is_dir() else []

    # ── retention primitive (★ 30차 P0-1) ───────────────────────────────
    # 리뷰가 요구한 세 연산이다:
    #
    #     retain(graph, minimum_until) -> immutable retention receipt / lease
    #     verify_retention(receipt, actual_backend)
    #     retrieve_retained(receipt, digest)
    #
    # lease 자체가 CAS object 이고 pin 된다 — 그래프의 일부다. 그래서 lease 를
    # 위조하려면 graph digest 를 통째로 바꿔야 하고, 그러면 journal 과 어긋난다.

    def retain(self, leg_id: str, digests, *, min_retention_days: int) -> dict:
        """graph 를 붙들고 **lease** 를 만든다. lease 도 pin 된다."""
        check_id(leg_id)
        if not isinstance(min_retention_days, int) or isinstance(min_retention_days, bool) \
                or min_retention_days < MIN_RETENTION_DAYS:
            raise PreserveError(
                "retain", f"min_retention_days 가 정책 하한 미만이다: "
                          f"{min_retention_days!r} < {MIN_RETENTION_DAYS}")
        if self.retention_days < min_retention_days:
            raise PreserveError(
                "retain", f"backend 의 retention({self.retention_days}일)이 요구 "
                          f"하한({min_retention_days}일)보다 짧다")
        objs = sorted(set(digests))
        # ★ 30차 자체 발견 — lease 에 `retain_until_utc` 가 들어가므로 부를
        #   때마다 다른 바이트가 된다. 재실행이 초 경계를 넘으면 lease 가 하나
        #   더 pin 되어 pin 집합에 여분이 생겼다 (전체 시험이 확률적으로
        #   빨갰다). 같은 graph 를 담보하는 유효한 lease 가 이미 있으면
        #   **그것을 돌려준다** — 재시도가 상태를 늘리지 않는다.
        existing = self._existing_lease(leg_id, objs, min_retention_days)
        if existing is not None:
            return existing        # `lease_version` 은 재발견된 값이 들어 있다
        self.pin(leg_id, objs)
        live = self.probe_enforcement()
        if live != self.enforcement:
            raise PreserveError(
                "retain", f"backend 가 신고한 enforcement({self.enforcement!r}) 를 "
                          f"조회가 지지하지 않는다 ({live!r}) — 강제는 이름이 아니라 "
                          "구현이다")
        until = (dt.datetime.now(dt.timezone.utc)
                 + dt.timedelta(days=min_retention_days))
        until_s = until.strftime("%Y-%m-%dT%H:%M:%SZ")
        # ★ 35차 P0-1 — control plane 이 graph 보다 먼저 풀리면 안 된다.
        # ★ 37차 — store record 가 **먼저** 있어야 연장할 대상이 있다. 초판은
        #   record 생성 전에 `ensure_store_lock()` 을 불러, 이 경로로 처음
        #   들어오면 "store.json 의 version 을 알 수 없다" 로 죽었다.
        _ = self.store_id
        ensure = getattr(self, "ensure_store_lock", None)
        if callable(ensure):
            ensure(until_s)
        lock = self.query_object_lock() or {}
        lease = {
            "schema": RETENTION_SCHEMA,
            "leg_id": leg_id,
            "store_id": self.store_id,
            # ★ 38차 P0-1 — identity 를 **exact version 으로** 봉인한다.
            #   `store_id` 만으로는 reopen 시점의 lock census 가 답을 바꾼다.
            "store_version_id": self.store_version_id or "",
            "store_lock_mode": self.store_lock_mode or "",
            "backend_uri": self.uri,
            # ★ 31차 P0-1 — 신고값이 아니라 **조회한** 강제 수준을 적는다
            "enforcement": live,
            # ★ 31차 P0-1 — provider 가 강제하는 **모드**와 그것이 만든
            #   immutable version ID 를 lease 에 싣는다. 검증 때 다시 조회한다.
            "lock_mode": lock.get("mode"),
            "object_versions": self.lock_objects(leg_id, objs, until_s),
            "min_retention_days": min_retention_days,
            "retain_until_utc": until_s,
            "objects": objs,
            "pin_set_digest": pin_set_digest(leg_id, objs),
        }
        raw = canonical_bytes(lease)
        l_obj = self.put_if_absent(raw)["digest"]
        self.pin(leg_id, [l_obj])          # lease 도 graph 의 일부다
        # ★ 33차 P0-1 — lease 는 **durable graph 의 증거**인데 잠금 밖이었다.
        #   정확한 lease digest 는 `lock_objects()` 뒤에야 존재하므로 순서상
        #   빠져 있었다. graph 가 durable 하다는 증거만 mutable 이면 모순이다.
        #   lease 도 같은 기한까지 잠근다.
        lv = (self.lock_objects(leg_id, [l_obj], until_s) or {}).get(l_obj)
        cv = self.lock_content_object(l_obj, until_s)
        return dict(lease, lease_digest=l_obj, lease_version=lv,
                    lease_content_version=cv or "")

    def _existing_lease(self, leg_id: str, objs: list,
                        min_retention_days: int) -> dict | None:
        """이 leg 에 이미 있고 **같은 graph 를 같은 정책으로** 담보하는 lease.

        pin 집합에서 graph object 를 뺀 나머지가 lease 후보다. 여러 개가 남아
        있으면 이미 상태가 오염된 것이므로 `None` 을 돌려 새로 만들지 않고
        아래 검증이 그것을 잡게 둔다.
        """
        extra = sorted(self.pinned(leg_id) - set(objs))
        if not extra:
            # ★ 37차 P0-1 — pin 만 보면 `after_lease_put` 잔여를 못 본다.
            #   lease content 는 put 됐는데 pin 전에 죽으면 orphan 이 되고,
            #   재개가 그것을 못 보고 새 lease 를 만든다. 재시도마다 orphan 이
            #   하나씩 쌓인다 (lease 바이트가 초마다 달라져 dedup 도 안 된다).
            orphan = self._orphan_lease(leg_id, objs, min_retention_days)
            if orphan is None:
                return None             # 후보가 없다 — 새로 만드는 것이 맞다
            # ★ 42차 P1 — 검증이 읽은 **exact version/bytes** 로 입양한다.
            self.adopt_orphan(leg_id, orphan)
            extra = [orphan.digest]
        # ★ 37차 P0-1 — **후보가 하나라도 있으면 새 state 를 만들지 않는다.**
        #   36차판은 후보 손상·모호성·repair 실패를 전부 `None` 으로 접어
        #   "기존 lease 없음" 과 같이 취급했고, 그래서 두 번째 WORM lease 가
        #   생겼다. 되돌릴 수 없는 상태를 만드는 쪽이 조용한 기본값이면 안
        #   된다 — 여기서부터는 성공 아니면 **fail-closed** 다.
        if len(extra) != 1:
            raise PreserveError(
                "retention",
                f"{leg_id}: graph 밖 pin 이 {len(extra)}개다 — 어느 것이 lease "
                f"인지 정할 수 없다 ({[d[:16] for d in extra]}). 새 lease 를 "
                "만들면 지울 수 없는 WORM 잔여가 하나 더 생긴다")
        # ★ 39차 P0-1 — proof 를 **먼저 재발견**하고 그 version 으로 읽는다.
        #   38차판은 version 없이 먼저 읽어, 같은 pin key 에 wrong-bytes 의
        #   더 최신 locked version 이 있으면 온전한 후보를 못 읽었다.
        # ★ 40차 P1 — 담보 proof 가 있으면 그것으로, 아직 없으면(crash 창)
        #   **exact bytes** 로 읽는다. 39차는 proof 만 봐서 `after_lease_pin`
        #   창의 잠기지 않은 v1 을 못 읽고 hostile v2 를 읽었다.
        try:
            pv = self.recover_lease_version(leg_id, extra[0])
        except PreserveError:
            pv = None
        if pv is None:
            src = getattr(self, "_repair_source", None)
            if callable(src):
                pv = src(self._provider_key(leg_id, extra[0]), extra[0])
        try:
            lease = self.read_lease(leg_id, extra[0], version=pv)
        except (PreserveError, ValueError, UnicodeDecodeError) as ex:
            raise PreserveError(
                "retention",
                f"{leg_id}: lease 후보 {extra[0][:16]} 를 읽을 수 없다 ({ex}) — "
                "손상된 후보 위에 새 lease 를 얹지 않는다") from ex
        # ★ 38차 P0-1 — **mutation 보다 검증이 먼저다.** 37차판은 여기서
        #   `None` 을 돌려 두 번째 lease 를 만들었고 (반례: 같은 graph 에 더
        #   강한 `min_retention_days` 를 요청), 통과했을 때는 곧바로
        #   `repair_lease_locks()` 로 pin·content 를 WORM 으로 만든 뒤에야
        #   exact key/schema 를 봤다. forged candidate 를 잠근 다음 거부하는
        #   순서였다 — 거부는 맞지만 되돌릴 수 없는 상태가 앞섰다.
        #
        #   이제 순수 validator 가 **전부** 먼저 본다. 통과 못 하면 아무것도
        #   바꾸지 않고 거부한다.
        # 만료는 **다른 사건**이다 — 사람이 판단할 일이고, 메시지가 그것을
        # 말해야 한다 (아래 일반 불일치와 섞지 않는다).
        if _lease_expired(lease):
            raise PreserveError(
                "retention",
                f"{leg_id}: lease {extra[0][:16]} 의 담보 기간이 지났다. "
                "자동 갱신은 지원하지 않는다: historical WORM pin 을 퇴역시킬 수 "
                "없어 새 lease 를 만들어도 exact pin set 이 깨진다. 사람이 "
                "판단해 새 leg 로 다시 담보하라")
        if not self._matches_lease(leg_id, objs, min_retention_days, lease):
            raise PreserveError(
                "retention",
                f"{leg_id}: lease 후보 {extra[0][:16]} 가 이 요청과 맞지 않는다 "
                f"(graph·정책·store·URI·enforcement·계약 key 중 하나) — "
                "그 위에 두 번째 lease 를 얹지 않는다. 정책을 바꾸려면 사람이 "
                "판단해 새 leg 로 담보하라")
        # ★ 35차 P0-1 — 검증 **전에** 누락 잠금을 채운다. `retain()` 내부에서
        #   죽으면 pin 또는 content 한쪽만 잠긴 lease 가 남는데, 초판은 그것을
        #   "기존 lease 없음" 으로 보고 두 번째 WORM lease 를 만들었다.
        try:
            proof = self.repair_lease_locks(leg_id, extra[0],
                                            lease["retain_until_utc"])
        except (PreserveError, KeyError, TypeError) as ex:
            raise PreserveError(
                "retention",
                f"{leg_id}: lease {extra[0][:16]} 를 수리하지 못했다 ({ex}) — "
                "수리 실패는 후보 부재가 아니다") from ex
        try:
            # ★ 34차 P0-1 — proof 를 **provider 에서 재발견**해 넘긴다.
            #   초판은 넘기지 않아 object-lock lease 재사용이 언제나 실패했다.
            # ★ 38차 P0-1 — content version proof 도 **재발견**해서 넘긴다.
            #   안 넘기면 재개가 만든 journal 이 최초 등록과 달라져
            #   `_register()` 가 거부한다 (재실행이 실패한다).
            # ★ 41차 P1 — `pv` 는 **repair source** 다 (바이트를 읽으려고 잠금
            #   여부를 안 묻고 고른 version). 그것을 proof 로 넘기면 수리가
            #   만든 담보 version 대신 우회 가능한 head 를 봉인한다 — 실제로
            #   같은 바이트의 Governance head 가 있으면 그것이 넘어가서
            #   "lock mode 가 lease 와 다르다" 로 죽었다. 수리가 끝난 **뒤**
            #   proof selector 를 다시 돌린다.
            # ★ 43차 P1 — 수리가 **만든 그 proof** 를 그대로 넘긴다. 42차는
            #   버리고 기한 없는 `recover_*()` 로 다시 찾았고, 같은 바이트의
            #   더 최신·더 짧은 Compliance version 이 있으면 그것을 골라
            #   검증에서 죽었다 (기한을 덮는 v1 이 그대로 있는데도).
            # ★ 44차 P2 — `proof.until` 은 지금까지 반환만 되고 아무도 안
            #   봤다. horizon 의 정본은 검증된 lease record 이므로, 여기서
            #   **둘이 같은 값인지** 한 번 못 박는다 (그러지 않으면 필드가
            #   이름만 있고 계약은 없다 — 이 저장소가 반복해서 겪은 형태다).
            if proof.until != lease["retain_until_utc"]:
                raise PreserveError(
                    "retention",
                    f"{leg_id}: 수리 proof 의 기한이 lease 와 다르다 "
                    f"({proof.until} ≠ {lease['retain_until_utc']})")
            return self.verify_retention(
                leg_id, extra[0], expected=set(objs),
                lease_version=proof.lease_version,
                lease_content_version=proof.content_version)
        except PreserveError as ex:
            # ★ 38차 P0-1 — 37차판은 만료면 `None` 을 돌려 **자동 갱신**했다.
            #   그 갱신은 production 에서 동작한 적이 없다: 새 L1 을 만들어도
            #   `pinned()` 이 historical WORM L0 를 active 로 세므로 바로 뒤의
            #   exact pin-set 검사가 같은 호출 안에서 실패한다. 37차 시험은
            #   `retain()` 반환값만 봐서 그것을 못 봤다.
            #
            #   셋이 동시에 성립할 수 없다:
            #     · 모든 historical pin version 을 active 로 센다
            #     · `delete` 가 계약에 없다 (우리는 지우지 않는다)
            #     · 만료되면 새 lease 를 만든다
            #
            #   세 번째를 **뺀다.** 자동 갱신은 되돌릴 수 없는 WORM 잔여를
            #   남기면서 아무것도 담보하지 못하는 가짜 기능이었다. 담보 기간이
            #   지났다는 것은 사람이 판단할 사건이지 조용히 재발급할 일이 아니다.
            #
            #   언젠가 갱신이 실제로 필요해지면 필요한 것은 다음 둘 중 하나다:
            #     · active lease pointer (historical WORM 과 active 를 구분)
            #     · exact-version retirement primitive
            #   둘 다 설계 항목이지 여기서 흉내낼 것이 아니다.
            raise PreserveError(
                "retention",
                f"{leg_id}: lease {extra[0][:16]} 검증에 실패했다 ({ex})"
                + (" — 담보 기간이 지났다. 자동 갱신은 지원하지 않는다: "
                   "historical WORM pin 을 퇴역시킬 수 없어 새 lease 를 만들어도 "
                   "exact pin set 이 깨진다. 사람이 판단해 새 leg 로 다시 담보하라."
                   if _lease_expired(lease) else
                   " — 만료 전 불일치 위에 새 lease 를 얹지 않는다")) from ex

    def _orphan_lease(self, leg_id: str, objs: list,
                      min_retention_days: int) -> "VerifiedBytes | None":
        """pin 되지 않은 채 남은 lease content. local backend 에는 없다."""
        return None

    def adopt_orphan(self, leg_id: str, lease: "VerifiedBytes") -> None:
        """local backend 는 version 이 없으므로 digest 로 pin 해도 같다."""
        self.pin(leg_id, [lease.digest])

    #: lease record 의 **닫힌** 계약. `verify_retention()` 이 쓰는 것과 같은
    #: 집합이며, 여기서 먼저 본다 — 검증이 mutation 보다 앞서야 한다.
    LEASE_KEYS: ClassVar[frozenset] = frozenset({
        "schema", "leg_id", "store_id", "store_version_id", "store_lock_mode",
        "backend_uri", "enforcement", "lock_mode", "object_versions",
        "min_retention_days", "retain_until_utc", "objects", "pin_set_digest"})

    def _matches_lease(self, leg_id: str, objs: list, min_retention_days: int,
                       rec) -> bool:
        """이 record 가 **지금 만들려는 것과 같은** lease 인가.

        ★ 38차 P0-1 — 37차판은 schema·leg·objects·정책일수·만료만 봤다.
          store ID·URI·enforcement·exact key set 을 안 봐서, 남의 store 의
          lease 나 남는 key 가 있는 record 도 orphan 으로 **입양**됐다.
          입양은 pin 을 만드는 mutation 이므로, 이 판정이 느슨하면 검증 전에
          되돌릴 수 없는 상태가 생긴다.

        **순수 함수다.** provider 를 읽기만 하고 아무것도 바꾸지 않는다.
        """
        if not isinstance(rec, dict) or set(rec) != set(self.LEASE_KEYS):
            return False
        if rec.get("schema") != RETENTION_SCHEMA:
            return False
        if rec.get("leg_id") != leg_id or rec.get("objects") != objs:
            return False
        if rec.get("min_retention_days") != min_retention_days:
            return False
        if rec.get("pin_set_digest") != pin_set_digest(leg_id, objs):
            return False
        # ★ 39차 P0-1 — timestamp 는 **문법부터** 본다 (문자열 비교 전에).
        if not _is_utc_stamp(rec.get("retain_until_utc")):
            return False
        if rec.get("store_id") != self.inspect_store_id() \
                or rec.get("backend_uri") != self.uri:
            return False
        live = self.probe_enforcement()
        if rec.get("enforcement") != live:
            return False
        # ★ 39차 P0-1 — 38차 뒤에 **추가된 locator 의미**를 여기서 본다.
        #   그것을 안 보고 repair 로 넘기면 위조 candidate 를 WORM 으로 만든
        #   뒤에야 strict verifier 가 거부한다.
        if live == ENFORCEMENT_OBJECT_LOCK:
            if rec.get("lock_mode") not in self.DURABLE_MODES:
                return False
            if rec.get("store_lock_mode") not in self.DURABLE_MODES:
                return False
            if not _nonempty_str(rec.get("store_version_id") or ""):
                return False
            ov = rec.get("object_versions")
            if not isinstance(ov, dict) or set(ov) != set(objs):
                return False
            if any(not _nonempty_str(v or "") for v in ov.values()):
                return False
            # ★ 40차 P0-1 — **nonempty 는 "존재한다" 가 아니다.** 39차는
            #   모양만 봤고, 그 ID 가 provider 에 실제로 있는지·bytes 가
            #   맞는지·mode·기한이 candidate 를 지지하는지는 안 봤다. 그래서
            #   존재하지 않는 locator 를 가진 candidate 가 앞단을 통과해
            #   repair 가 WORM 을 만든 뒤에야 거부됐다.
            #
            #   여기서 **읽기만** 해서 전부 확인한다.
            # ★ 41차 P0-1 — locator 는 **두 종류**이고 결속하는 것이 다르다.
            #   40차는 하나의 `_locator_holds(key, version, dg, ...)` 로 둘을
            #   함께 봤고, store 는 `dg=None` 으로 불러 bytes 분기를 통째로
            #   건너뛰었다. 그래서 "그 version 이 존재하고 잠겨 있다" 를 "그
            #   version 이 이 candidate 의 store record 다" 라고 불렀다 —
            #   `store_id` 가 다른 record 나 record 도 아닌 바이트를 가리키는
            #   locator 가 앞단을 통과했다.
            if not self._store_locator_holds(rec["store_version_id"],
                                             rec["store_lock_mode"], rec):
                return False
            for dg, v in ov.items():
                if not self._object_locator_holds(
                        self._provider_key(leg_id, dg), v, dg,
                        rec["lock_mode"], rec):
                    return False
        elif rec.get("object_versions"):
            return False
        return not _lease_expired(rec)

    def _locator_state(self, key: str, version: str, want_mode, rec):
        """그 exact version 이 **지금 담보되어 있는가** — 상태를 준다 (없으면 `None`).

        존재 · mode 동등 · 기한 덮음까지만 본다. **여기서 끝내면 안 된다** —
        "그 version 이 담보돼 있다" 는 "그 version 이 내가 봉인한 그것이다" 가
        아니다. 무엇으로 결속하는지는 아래 두 typed 검사가 정한다.

        **읽기만 한다.**
        """
        prov = getattr(self, "provider", None)
        if prov is None:
            return None
        st = prov.describe_object(key, version)
        if not isinstance(st, dict) or st.get("mode") != want_mode:
            return None
        try:
            _horizon_covers(st, rec["retain_until_utc"], key)
        except PreserveError:
            return None
        return st

    def _object_locator_holds(self, key: str, version: str, dg: str,
                              want_mode, rec) -> bool:
        """graph pin locator — 담보 상태 **+ 그 version 의 바이트가 `dg`**."""
        if self._locator_state(key, version, want_mode, rec) is None:
            return False
        return self._bytes_match(key, version, dg)

    def _store_locator_holds(self, version: str, want_mode, rec) -> bool:
        """store locator — 담보 상태 **+ 그 version 이 이 candidate 의 store record**.

        ★ 41차 P0-1 — 40차는 store 를 `dg=None` 으로 불러 bytes 를 아예 안
          봤다. 그래서 이런 candidate 가 앞단을 통과했다::

              canonical store v1 = record(store_id=A), Compliance, 충분한 기한
              newer     store v2 = record(store_id=B) 또는 record 가 아닌 바이트
              candidate: store_id=A · store_version_id=v2

          `inspect_store_id()` 는 canonical v1 의 A 를 돌려주고 locator 검사는
          존재·mode·기한만 봤으므로 통과했다. 그 뒤 `repair_lease_locks()` 가
          pin·content 를 WORM 으로 만든 **다음에야** strict verifier 가 exact
          v2 를 읽고 거부했다 — 거부는 맞지만 되돌릴 수 없는 상태가 앞섰다.

          `store_id` 는 identity **root** 다. locator 가 그것과 결속되지 않으면
          reopen 이 남의 record 를 가리키는 receipt 를 만들 수 있다.
        """
        if self._locator_state("store.json", version, want_mode, rec) is None:
            return False
        prov = self.provider
        try:
            got = load_canonical(prov.get("store.json", version))
        except (KeyError, ValueError, UnicodeDecodeError):
            return False
        return _is_store_record(got) and got["store_id"] == rec.get("store_id")

    def inspect_store_id(self):
        """store identity 를 **읽기만** 한다. 없으면 `None` (39·41차 P0-1).

        ★ 39차 — `store_id` 는 record 가 없으면 만들고, 있으면
          `ensure_store_lock()` 으로 기한을 연장한다. "순수 validator" 가 그것을
          부르면 검증 자체가 상태를 바꾼다. inspect 와 ensure 를 가른다.

        ★ 41차 P1 — 그런데 base 구현이 `return self.store_id` 한 줄이었다.
          object-lock backend 쪽만 순수해졌고 **local backend 의 candidate
          validation 은 그대로 만들고 굳혔다** — 이름이 predicate 보다 강한
          그 형태다. 여기서 진짜로 읽기만 한다.
        """
        p = Path(self.root) / "store.json"
        if not p.is_file():
            return None
        try:
            rec = load_canonical(p.read_bytes())
        except (ValueError, UnicodeDecodeError):
            return None
        if not isinstance(rec, dict):
            return None
        sid = rec.get("store_id") or ""
        # `store_id` 가 받아들이는 것과 같은 형태만 identity 로 인정한다.
        # 이상하면 `None` — 검증 경로에서 예외를 던지면 그 자체가 부작용 있는
        # 판정이 되고, `None` 은 어느 비교와도 안 맞아 fail-closed 다.
        return sid if (_is_hex64(sid) or _is_uuid_hex(sid)) else None

    def read_lease(self, leg_id: str, lease_digest: str, *, version=None) -> dict:
        """lease 를 **pin 에서** 읽는다."""
        lease = load_canonical(
            self.read_pinned(leg_id, lease_digest, version=version))
        if not isinstance(lease, dict):
            raise PreserveError("retention", "lease 가 dict 가 아니다")
        return lease

    def verify_retention(self, leg_id: str, lease_digest: str,
                         expected: set | None = None,
                         lease: dict | None = None,
                         lease_version: str | None = None,
                         lease_content_version: str | None = None) -> dict:
        """lease 가 **이 backend 에서 지금** 유효한가.

        읽은 바이트가 아니라 **상태**를 본다 — 그래서 전수 읽기가 끝난 뒤에
        한 번 더 부르면 그 사이의 삭제가 잡힌다 (30차 P0-1 의 마지막 창).
        """
        stage = "retention"
        # `lease` 를 주면 그것을 본다 — 회귀가 lease 축만 변이할 수 있게 한다.
        # ★ 38차 P0-1 — 봉인된 lease version 으로 **바이트를 읽는다.**
        #   37차판은 version 없이 읽고 나서야 그 version 의 lock 을 조회했다.
        #   같은 pin key 에 더 최신 locked bytes 가 있으면 exact locator 를
        #   들고 있으면서도 남의 바이트를 읽고 실패했다.
        lease = (dict(lease) if lease is not None
                 else self.read_lease(leg_id, lease_digest, version=lease_version))
        lease_version = lease_version or lease.pop("lease_version", None)
        lease_content_version = (lease_content_version
                                 or lease.pop("lease_content_version", None))
        lease.pop("lease_digest", None)
        lease.pop("lease_version", None)
        lease.pop("lease_content_version", None)
        want = set(self.LEASE_KEYS)
        if set(lease) != want:
            raise PreserveError(stage, f"lease 키가 계약과 다르다: "
                                       f"{sorted(set(lease) ^ want)[:4]}")
        if lease["schema"] != RETENTION_SCHEMA:
            raise PreserveError(stage, f"lease schema 가 다르다: {lease['schema']!r}")
        if lease["leg_id"] != leg_id:
            raise PreserveError(stage, "lease 가 다른 leg 의 것이다")
        # ★ 30차 P0-2 — 두 축을 **따로** 본다. store 를 통째로 복사하면
        #   `store.json` 까지 딸려와 UUID 가 같아지므로 URI 축이 잡고,
        #   같은 경로를 재사용하면 UUID 축이 잡는다. 어느 쪽이 어긋났는지
        #   메시지가 말해야 반례를 다시 만들 수 있다.
        if lease["backend_uri"] != self.uri:
            raise PreserveError(
                stage, f"lease 가 다른 backend 의 것이다 — "
                       f"{lease['backend_uri']!r} ≠ {self.uri!r}")
        # ★ 39차 P0-1 — **검증은 수리하지 않는다.** `store_id` 는 record 가
        #   없으면 만들고 있으면 기한을 연장한다. 그것을 검증 경로에서 부르면
        #   "봉인이 풀렸다" 를 스스로 고쳐 놓고 통과시킨다 — 실제로 그랬다
        #   (담보 해제·기한 단축 반례가 둘 다 self-healing 으로 초록이었다).
        # ★ 41차 P1 — 읽은 값을 **지역변수에 담고 오류 문자열도 그것만 쓴다.**
        #   40차는 불일치를 `inspect_store_id()` 로 발견해 놓고 메시지에서
        #   `self.store_id` 를 다시 평가했다 — 오류를 설명하는 과정에서 없는
        #   store record 를 만들거나 기한을 연장할 수 있었다. read-only 경로에
        #   mutation 을 남기는 마지막 자리였다.
        live_sid = self.inspect_store_id()
        if lease["store_id"] != live_sid:
            raise PreserveError(
                stage, f"lease 가 다른 store 의 것이다 — backend URI 는 같은데 "
                       f"store {lease['store_id'][:8]} ≠ {str(live_sid)[:8]}")
        # ★ 30차 P1-3 — receipt 가 적은 숫자가 아니라 **지금 backend** 를 본다
        if self.retention_days < lease["min_retention_days"]:
            raise PreserveError(
                stage, f"backend 의 현재 retention({self.retention_days}일)이 lease 의 "
                       f"하한({lease['min_retention_days']}일)보다 짧다")
        if lease["min_retention_days"] < MIN_RETENTION_DAYS:
            raise PreserveError(stage, "lease 의 하한이 정책 하한 미만이다")
        # ★ 31차 P0-1 — lease 에 적힌 강제 수준을 **지금 backend 가 증명하는
        #   것**과 대조한다. 초판은 저장만 하고 다시 보지 않아, lease 를
        #   위조하거나 강한 backend 의 lease 를 약한 backend 에서 열어도
        #   아무 일이 없었다.
        live = self.probe_enforcement()
        if lease["enforcement"] != live:
            raise PreserveError(
                stage, f"lease 의 enforcement 가 이 backend 가 지금 증명하는 것과 "
                       f"다르다: {lease['enforcement']!r} ≠ {live!r}")
        if live != self.enforcement:
            raise PreserveError(
                stage, f"backend 가 신고한 enforcement({self.enforcement!r}) 를 "
                       f"조회가 지지하지 않는다 ({live!r})")
        # ★ 38차 P0-1 — **봉인된 version 으로** identity 를 확인한다.
        #   live-lock census 는 시간이 지나면 답이 바뀌므로 proof 가 아니다.
        sv = lease.get("store_version_id") or ""
        prov = getattr(self, "provider", None)
        if live == ENFORCEMENT_OBJECT_LOCK and prov is not None:
            # ★ 39차 P0-1 — **optional 이면 sealed locator 가 아니라 hint 다.**
            #   38차판은 `if sv and ...` 라 빈 값이 조용히 넘어갔다.
            if not _nonempty_str(sv):
                raise PreserveError(
                    stage, "object-lock lease 에 store version proof 가 없다 — "
                           "빈 값은 live 재탐색으로 돌아가는 통로다")
            if lease.get("store_lock_mode") not in self.DURABLE_MODES:
                raise PreserveError(
                    stage, f"store lock mode 가 담보 mode 가 아니다: "
                           f"{lease.get('store_lock_mode')!r}")
        if sv and prov is not None:
            st = prov.describe_object("store.json", sv)
            if not isinstance(st, dict):
                raise PreserveError(
                    stage, f"lease 가 봉인한 store version 이 담보되지 않는다: {sv}")
            _durable_mode(st, lease.get("store_lock_mode"), "store version",
                          self.DURABLE_MODES, stage)
            try:
                rec = load_canonical(prov.get("store.json", sv))
            except (KeyError, ValueError, UnicodeDecodeError) as ex:
                raise PreserveError(stage, "봉인 store record 를 읽을 수 없다") from ex
            if not _is_store_record(rec) or rec["store_id"] != lease["store_id"]:
                raise PreserveError(
                    stage, "봉인 store version 의 record 가 lease 와 다르다")
            # ★ 39차 P0-1 — identity root 가 graph 보다 **먼저 풀리면** 안 된다.
            #   exact graph version 이 살아 있어도 reopen locator 를 잃는다.
            _horizon_covers(st, lease["retain_until_utc"], "store version", stage)
        try:
            until = dt.datetime.strptime(lease["retain_until_utc"], "%Y-%m-%dT%H:%M:%SZ")
        except (TypeError, ValueError) as ex:
            raise PreserveError(stage, f"retain_until_utc 가 이상하다: "
                                       f"{lease.get('retain_until_utc')!r}") from ex
        if until.replace(tzinfo=dt.timezone.utc) <= dt.datetime.now(dt.timezone.utc):
            raise PreserveError(stage, "lease 가 이미 만료됐다")
        objs = lease["objects"]
        if not _is_unique_hex64_list(objs):
            raise PreserveError(stage, "lease 의 objects 가 unique 64-hex 목록이 아니다")
        if lease["pin_set_digest"] != pin_set_digest(leg_id, objs):
            raise PreserveError(stage, "lease 의 pin_set_digest 가 objects 와 다르다")
        if expected is not None and set(objs) != set(expected):
            raise PreserveError(
                stage, f"lease 가 유도한 graph 와 다르다 — 없음 "
                       f"{sorted(set(expected) - set(objs))[:2]}")
        # ★ 31차 P0-1 — provider 의 version ID 를 **다시 조회**한다. 등록
        #   시점에 잠겼다는 사실이 지금도 잠겨 있다는 뜻이 아니다.
        want_v = lease["object_versions"]
        if not isinstance(want_v, dict):
            raise PreserveError(stage, "lease 의 object_versions 가 dict 가 아니다")
        if live == ENFORCEMENT_OBJECT_LOCK:
            if set(want_v) != set(objs):
                raise PreserveError(
                    stage, "object-lock lease 인데 version 이 없는 object 가 있다: "
                           f"{sorted(set(objs) - set(want_v))[:2]}")
            # ★ 40차 P0-1 — 값이 **허용된 담보 mode** 여야 한다. 39차는
            #   nonempty 만 봐서 Governance 가 그대로 지나갔다.
            if lease["lock_mode"] not in self.DURABLE_MODES:
                raise PreserveError(
                    stage, f"lease 의 lock_mode 가 담보 mode 가 아니다: "
                           f"{lease['lock_mode']!r} (허용 "
                           f"{sorted(self.DURABLE_MODES)})")
            # ★ 32차 P0-1 — version **값**이 유효해야 한다. 초판은 key set 만
            #   봐서 `{digest: None}` 도 durable 로 통과했다.
            weak = sorted(d for d, v in want_v.items() if not _nonempty_str(v or ""))
            if weak:
                raise PreserveError(
                    stage, f"lease 의 object version 이 비었다: {weak[:2]}")
            # ★ 32차 P0-1 — 그 version 이 **지금도** 잠겨 있는지, 어떤 mode 로,
            #   언제까지인지 provider 에 묻는다. 초판은 셋 다 안 물었다.
            live_locks = self.describe_locks(leg_id, want_v)
            gone = sorted(d for d, st in live_locks.items() if not isinstance(st, dict))
            if gone:
                raise PreserveError(
                    stage, f"provider 에 잠긴 version 이 없다: {gone[:2]} — "
                           "더 이상 잠겨 있지 않다")
            for dg, st in sorted(live_locks.items()):
                # `describe_locks` 가 version 을 **키로** 조회하므로 dict 가
                # 돌아온 것 자체가 일치를 뜻한다 — 중복 비교를 두지 않는다.
                _durable_mode(st, lease["lock_mode"], f"graph pin {dg[:16]}",
                              self.DURABLE_MODES, stage)
                _horizon_covers(st, lease["retain_until_utc"],
                                f"graph pin {dg[:16]}", stage)
        elif want_v:
            raise PreserveError(stage, "advisory lease 인데 version 이 적혀 있다")
        # ★ 33차 P0-1 — lease **자신**도 잠겨 있어야 한다. proof 는 journal 이
        #   들고 있다 (lease 는 자기 digest 를 담을 수 없으므로 밖에 둔다).
        if live == ENFORCEMENT_OBJECT_LOCK:
            if not _nonempty_str(lease_version or ""):
                raise PreserveError(
                    stage, "lease 자신의 version proof 가 없다 — durable graph 의 "
                           "증거가 잠금 밖이면 그 증거를 지울 수 있다")
            st = (self.describe_locks(leg_id, {lease_digest: lease_version})
                  or {}).get(lease_digest)
            if not isinstance(st, dict):
                raise PreserveError(stage, "lease 가 provider 에 잠겨 있지 않다")
            # ★ 35차 P0-1 — lease **CAS content** 도 잠겨 있어야 한다. 초판은
            #   pin version 만 다시 조회해서, content lock 직전에 죽으면 한쪽이
            #   unlocked 인 채 `durable=True` 까지 갔다.
            # ★ 39차 P0-1 — content locator 도 **필수**다. 빈 값이면 live
            #   재탐색으로 돌아가므로 sealed proof 가 아니다.
            if not _nonempty_str(lease_content_version or ""):
                raise PreserveError(
                    stage, "object-lock lease 에 content version proof 가 없다")
            cst = self.describe_content_lock(
                lease_digest, version=lease_content_version)
            if not isinstance(cst, dict):
                raise PreserveError(
                    stage, "lease 의 CAS content 가 잠겨 있지 않다 — 증거의 "
                           "원본을 지울 수 있다")
            _durable_mode(cst, lease["lock_mode"], "lease content",
                          self.DURABLE_MODES, stage)
            _horizon_covers(cst, lease["retain_until_utc"], "lease content", stage)
            # ★ `describe_locks` 는 **그 version 을 키로** 조회하므로 dict 가
            #   돌아온 것 자체가 version 일치를 뜻한다. 여기서 다시 비교하면
            #   같은 규칙이 두 곳에 생기고, 강한 쪽을 지워도 초록이 된다
            #   (변이로 확인했다).
            _durable_mode(st, lease["lock_mode"], "lease pin",
                          self.DURABLE_MODES, stage)
            _horizon_covers(st, lease["retain_until_utc"], "lease pin", stage)
        # ★ 38차 P0-1 — graph pin 도 **봉인 version** 으로 되읽는다.
        pbad = self.verify_pins(leg_id, objs, versions=want_v or None)
        if pbad:
            raise PreserveError(stage, "봉인 version 의 pin 이 어긋난다: "
                                       + "; ".join(pbad[:3]))
        on_disk = self.pinned(leg_id)
        want_disk = set(objs) | {lease_digest}
        if on_disk != want_disk:
            raise PreserveError(
                stage, f"pin 상태가 lease 와 다르다 — 없음 "
                       f"{sorted(want_disk - on_disk)[:2]} · 여분 "
                       f"{sorted(on_disk - want_disk)[:2]}")
        return dict(lease, lease_digest=lease_digest, lease_version=lease_version,
                    lease_content_version=lease_content_version or "")

    # ── object-lock adapter 가 채워야 하는 자리 (★ 31차 P0-1) ───────────
    # local 은 아무 것도 잠그지 않으므로 빈 값을 돌려준다. 강제하는 backend 는
    # provider 가 만든 **immutable version ID** 를 돌려주고, 검증 때 그것을
    # 다시 조회해 살아 있는지 본다.

    def query_object_lock(self) -> dict | None:
        """provider 의 live lock 설정. local 은 잠글 provider 가 없다."""
        return None

    def lock_objects(self, leg_id: str, digests, until: str) -> dict:
        return {}

    def lock_content_object(self, dg: str, until: str, *, data: bytes = None):
        """CAS object 쪽도 잠근다 — local 에는 잠글 것이 없다."""
        return None

    def repair_lease_locks(self, leg_id: str, lease_digest: str,
                           until: str) -> "RetentionProof":
        """lease 의 **누락된 잠금**을 채우고 proof 를 준다 (advisory 는 빈 proof).

        ★ 35차 P0-1 — `retain()` 의 네 durable 단계 사이에서 죽으면 lease 의
          pin 또는 CAS content 한쪽만 잠긴 상태가 남는다. 초판은 그 상태를
          **repair 하지 않아서**, 앞 경계는 두 번째 WORM lease 를 만들고 뒤
          경계는 content 가 삭제 가능한데도 `durable=True` 까지 갔다.
          `lock` 은 멱등이므로 재개가 빠진 쪽을 채우면 된다.

        ★ 43차 P1 — advisory backend 에는 version 이 없으므로 빈 proof 다.
          `None` 을 돌려주면 호출자가 다시 분기해야 하고, 그 분기가 곧
          "찾은 것을 버리고 다시 찾는" 통로가 된다.
        """
        return RetentionProof(lease_version=None, content_version=None,
                              until=until)

    def recover_content_version(self, lease_digest: str, until: str = None):
        """local 에는 version 이 없다."""
        return None

    def recover_lease_version(self, leg_id: str, lease_digest: str,
                              until: str = None):
        """이미 잠긴 lease 의 version 을 **digest 로 재조회**한다.

        ★ 34차 P0-1 — lease version proof 는 journal 을 쓰기 전까지 메모리에만
          있었다. 그래서 기존 lease 를 재사용하려는 모든 경로(재실행,
          pre-journal crash 재개)가 proof 없이 verifier 를 불러 **반드시**
          실패했고, 그때마다 두 번째 WORM lease 가 생겨 exact pin set 이
          오염됐다. WORM 이라 지울 수도 없어 복구가 막혔다.

          불변식: **lease 가 한 번 잠겼다면 어느 지점에서 죽어도 reopen 이
          같은 lease digest 와 같은 provider version 을 재발견한다.**
        """
        return None

    def describe_content_lock(self, dg: str):
        """CAS content object 의 **현재** lock 상태. local 은 잠글 것이 없다."""
        return None

    def describe_locks(self, leg_id: str, versions: dict) -> dict:
        """version 별 **현재** lock 상태를 provider 에 묻는다.

        ★ 32차 P0-1 — 31차는 version **존재**만 봤다. 값이 유효한지, 지금 어떤
          mode 인지, 그 version 의 retain-until 이 언제인지 하나도 안 물었다.
          local 은 잠글 provider 가 없으므로 전부 `None` 이다.
        """
        return {dg: None for dg in versions}

    def retrieve_retained(self, lease: dict, dg: str) -> bytes:
        """lease 가 담보한 object 를 **봉인한 version 그대로** 회수한다.

        ★ 37차 P0-1 — 36차판은 `read_pinned()` 만 불렀고, 그것은 "가장 최신
          잠긴 version" 을 다시 골랐다. lease 가 v1 을 봉인했는데 같은 pin
          key 에 다른 바이트의 v2 가 올라와 잠기면, v1 은 그대로 durable 한데
          회수는 v2 를 읽고 digest mismatch 로 실패했다. receipt 의 목적은
          locator 재발견이 아니라 **exact immutable version 회수**다.
        """
        if dg not in set(lease.get("objects") or []):
            raise PreserveError("retention", f"lease 가 담보하지 않은 object: {dg[:16]}")
        sealed = (lease.get("object_versions") or {}).get(dg)
        return self.read_pinned(lease["leg_id"], dg, version=sealed)


class ObjectLockBackend(CasBackend):
    """provider 가 **바이트를 소유하고 강제하는** retention.

    ★ 31차 P0-1 — 타입 경계를 만들었지만, 그 backend 가 `CasBackend` 의
      저장 연산을 **그대로 상속**해서 바이트는 여전히 local `objects/`·`pins/`
      에 있었다. provider 에는 version/mode 장부만 적혔다. 32차 리뷰의 문장:

          "강제가 있는 쪽이 아니라 local bytes 와 독립된 metadata 장부가
           있는 쪽이다."

      그래서 `durable=True` 뒤에도 local pin 을 지울 수 있었다. 잠갔다는 말이
      거짓이었다.

    ★ 32차 P0-1 — **바이트의 소유자를 provider 로 옮긴다.** put·read·pin·
      read_pinned 가 전부 provider 를 지난다. local root 를 통째로 없애도
      graph 가 회수돼야 하고, 약속 기간 전 delete/overwrite 는 provider 가
      거부해야 한다.

    ★ 36차 P0-1 — **계약의 정본은 이 산문이 아니라 `PROVIDER_CONTRACT` 다.**
      35차 docstring 은 7개만 열거했는데 코드는 `store_uri`·`head_version`
      도 불렀다. 이제 상수가 authority 이고 시험이 소스와 대조한다. 아래는
      그 상수의 **의미** 설명이다 (이름 목록은 상수가 정본):

        put(key, data) -> version_id          # 언제나 **새 version** (덮어쓰기 아님)
        get(key, version=None) -> bytes       # version 생략 시 head
        versions(key) -> [version_id]         # 최신순 — per-version locator
        (delete 는 계약에 **없다** — 우리는 어떤 경로로도 지우지 않는다.
         37차: 계약은 우리가 **부르는** 것의 폐쇄이고, 안 부르는 연산을
         adapter 에게 요구할 근거가 없다.)
        lock(key, version, until)
        describe() -> {mode, min_retain_days}
        describe_object(key, version) -> {version_id, mode, retain_until} | None
        list_versions(prefix) -> [(key, version_id)]   # ListObjectVersions
                                              # ★ 37차 — 열거 primitive 는 이것
                                              #   하나다. ListObjectsV2 는 delete
                                              #   marker 뒤의 담보를 못 본다
        store_uri() -> str                    # 재시작을 견디는 안정 식별자

    ★ 36차 P0-1 — **per-version 의미.** 실물 Object Lock 은 key 가 아니라
      version 을 지킨다. 잠긴 v1 위에 잠기지 않은 v2 를 올리는 것은 실패가
      아니라 정상이고, `head_version` 을 보는 코드는 전부 그 v2 를 본다.
      35차 fake 는 그 put 을 거부해서 이 창을 통째로 가리고 있었다. 그래서
      durable 한 읽기는 전부 `protected_version()` 을 지난다.
    """

    ENFORCEMENT: ClassVar[str] = ENFORCEMENT_OBJECT_LOCK
    #: ★ 36차 P0-1 — GOVERNANCE 는 여기 없다. `s3:BypassGovernanceRetention`
    #:   을 가진 principal 이 우회 삭제할 수 있으므로, 그 모드의 담보는
    #:   저장소가 아니라 IAM **설정**에 대한 주장이다. GOVERNANCE 를 받으려면
    #:   우회가 실제로 거부되는 것을 `probe_bypass()` 로 **실측**해야 한다.
    DURABLE_MODES: ClassVar[frozenset] = frozenset({"COMPLIANCE"})
    BYPASSABLE_MODES: ClassVar[frozenset] = frozenset({"GOVERNANCE"})
    LOCK_MODES: ClassVar[frozenset] = DURABLE_MODES | BYPASSABLE_MODES

    #: 서브클래스가 붙이는 provider. 없으면 강제가 없는 것이다.
    provider: object = None

    # ── 계약 ────────────────────────────────────────────────────────────
    def assert_provider_contract(self) -> None:
        """provider 가 `PROVIDER_CONTRACT` 전부를 주는지 확인한다 (36차 P0-1).

        하나라도 없으면 durable 을 주장할 수 없다. 어느 연산이 없는지 이름을
        말한다 — adapter 작성자가 문서를 다시 읽지 않아도 되게.
        """
        missing = [op for op in PROVIDER_CONTRACT
                   if not callable(getattr(self.provider, op, None))]
        if missing:
            raise PreserveError(
                "capability",
                f"provider 가 계약 연산을 주지 않는다: {missing} — "
                "durable 은 계약 전체를 만족할 때만 주장할 수 있다")

    # ── per-version locator ─────────────────────────────────────────────
    def _version_candidates(self, key: str, required: bool = True) -> list:
        """`provider.versions(key)` 를 **검증해서** 돌려주는 유일한 통로 (46차 P0-8).

        45차까지는 `put()` 이 돌려준 VersionId 만 "비어 있지 않은 문자열" 로
        봤다. 그런데 담보 version 은 **열거**에서도 온다
        (`protected_version` · `_locked_versions` · store identity 선택).
        거기서 falsy·비문자열 후보가 들어오면 `lock(key, "", until)` 을 부르고,
        그 빈 문자열이 lease proof·receipt locator 로 굳는다 — "정확히 이
        version 을 담보했다" 가 아무것도 가리키지 않는 값이 된다.

        되돌릴 수 없는 `lock()` **앞**에서 fail-closed 한다. 후보를 조용히
        걸러내지 않는다: 이런 provider 는 계약 위반이고, 남은 후보로 계속
        진행하면 "무엇을 담보했는지" 가 provider 의 응답 순서에 달린다.
        """
        vs = getattr(self.provider, "versions", None)
        if not callable(vs):
            if required:
                raise PreserveError(
                    "capability",
                    "provider 가 versions() 를 주지 않는다 — per-version 잠금에서 "
                    "담보 version 을 찾을 수 없으면 durable 을 주장할 수 없다")
            return []
        got = vs(key)
        if got is None:
            return []
        if not isinstance(got, list):
            raise PreserveError(
                "capability",
                f"provider.versions({key!r}) 가 목록이 아니다: {type(got).__name__}")
        bad = [v for v in got if not _nonempty_str(v if isinstance(v, str) else "")]
        if bad:
            raise PreserveError(
                "capability",
                f"provider.versions({key!r}) 가 version 이 아닌 후보를 담고 있다: "
                f"{bad!r} — version locator 는 비어 있지 않은 문자열이어야 한다 "
                "(falsy locator 를 잠그면 무엇을 담보했는지 되찾을 수 없다)")
        return list(got)

    def protected_version(self, key: str):
        """그 key 에서 **지금 잠겨 있는** 가장 최신 version (36차 P0-1).

        35차는 `head_version(key)` 를 썼다. 실물에서 head 는 적대적/사고성
        put 이 올린 **잠기지 않은** version 일 수 있고, 그러면 identity 재조회
        도 lease proof 재발견도 잠금 밖의 바이트를 가리킨다. 담보를 들고 있는
        것은 head 가 아니라 잠긴 version 이다.
        """
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        for v in self._version_candidates(key):
            st = self.provider.describe_object(key, v)
            if not isinstance(st, dict):
                continue
            if st.get("mode") in self.LOCK_MODES \
                    and str(st.get("retain_until") or "") > now:
                return v
        return None

    def _locked_versions(self, key: str, modes=None, until: str | None = None) -> list:
        """그 key 에서 **지금 잠겨 있는** version 전부 (최신순).

        ★ 40차 P1 — `modes` 를 주면 그 mode 만 후보다. proof lookup 은 담보
          mode 만 봐야 한다 — 같은 바이트의 newer Governance version 이 older
          Compliance proof 를 가릴 수 있었다.
        """
        want = self.DURABLE_MODES if modes is None else modes
        cands = self._version_candidates(key, required=False)
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out = []
        for v in cands:
            st = self.provider.describe_object(key, v)
            if not (isinstance(st, dict) and st.get("mode") in want
                    and _is_utc_stamp(st.get("retain_until"))
                    and _stamp(st["retain_until"]) > _stamp(now)):
                continue
            # ★ 42차 P1 — `until` 을 주면 **그 기한을 덮는** version 만 proof 다.
            #   이것이 없으면 "이미 담보인가" 를 물을 수 없어서, 기한이 짧은
            #   version 위에 새로 잠그거나 반대로 충분한 proof 를 못 알아본다.
            if until is not None and (not _is_utc_stamp(until)
                                      or _stamp(st["retain_until"]) < _stamp(until)):
                continue
            out.append(v)
        return out

    def _bytes_match(self, key: str, version: str, dg: str) -> bool:
        try:
            return hashlib.sha256(self.provider.get(key, version)).hexdigest() == dg
        except KeyError:
            return False

    def _read_protected(self, key: str) -> bytes:
        """담보 version 을 우선 읽고, 아직 잠긴 것이 없을 때만 head 를 읽는다."""
        v = self.protected_version(key)
        return self.provider.get(key, v) if v else self.provider.get(key)

    # ── 키 공간 ─────────────────────────────────────────────────────────
    def _provider_obj_key(self, dg: str) -> str:
        return f"objects/{dg}"

    def _provider_key(self, leg_id: str, dg: str) -> str:
        return f"pins/{leg_id}/{dg}"

    @property
    def store_id(self) -> str:
        """store 식별자도 **provider 안에** 둔다.

        ★ 32차 P0-1 — 초판은 `<root>/store.json` 을 읽었다. local root 를
          지우면 정체성이 사라져 "provider 가 소유한다" 가 거짓이 됐다.
        """
        key = "store.json"
        # ★ 37차 P0-1 — canonical identity 는 "최신 잠긴 version" 이 아니라
        #   **가장 오래된 유효 잠금 version** 이다. 더 최신의 유효하고 잠긴
        #   record 하나가 생기면 reopen 이 identity 를 조용히 갈아치웠고,
        #   그 순간 예전 receipt 전부가 foreign store 가 됐다 (바이트는 다
        #   살아 있는데 locator 를 잃는다). 최초 잠금이 root-of-authority 다.
        vid = self._canonical_store_version(key)
        # ★ 39차 P0-1 — Compliance canonical 이 없는데 **잠긴 record 는 있는**
        #   상태에서 fallback 으로 읽으면, Compliance selector 를 우회해
        #   우회 가능한 identity root 로 durable 을 주장하게 된다.
        # 담보(Compliance)가 아니어도 **잠긴 것이 있으면** 그 위에 새 identity 를
        # 발급하지 않는다 — 그래서 여기서는 `LOCK_MODES` 전체를 본다.
        if vid is None and self._locked_versions(key, modes=self.LOCK_MODES):
            raise PreserveError(
                "store",
                "store.json 에 COMPLIANCE 담보 version 이 없다 (잠긴 version 은 "
                "있다) — 우회 가능한 identity root 위에 담보를 주장하지 않는다")
        try:
            raw = self.provider.get(key, vid) if vid else self._read_protected(key)
            rec = load_canonical(raw)
        except (KeyError, ValueError, UnicodeDecodeError):
            rec = None
        if _is_store_record(rec):
            # ★ 35차 P0-1 — 초판은 여기서 **즉시 반환**했다. `put` 뒤 `lock`
            #   전에 죽으면 valid 하지만 unlocked 인 record 가 남는데, reopen 이
            #   그것을 그냥 믿었다. 그 상태에서 durable 을 주장한 뒤 record 를
            #   지우면 다음 reopen 이 새 UUID 를 발급해 locator 를 잃는다.
            #   잠금이 없으면 **repair 한다** (lock 은 멱등이다).
            self.ensure_store_lock(self._store_horizon())
            return rec["store_id"]
        # ★ 34차 P0-1 — `store.json` 은 잠기지 않은 control-plane object 였다.
        #   지우면 새 UUID 가 발급돼, content 와 lease 가 남아 있어도 기존
        #   receipt 가 복구 불가가 된다.
        if vid is not None:
            raise PreserveError(
                "store",
                "store.json 의 담보 version 이 계약 record 가 아니다 — "
                "identity 를 새로 발급하면 예전 receipt 의 locator 를 잃는다")
        self.provider.put(key, canonical_bytes(
            {"schema": STORE_SCHEMA, "store_id": uuid.uuid4().hex}))
        self.ensure_store_lock(self._store_horizon())
        new = load_canonical(self.provider.get(
            key, self._canonical_store_version(key)))
        if not _is_store_record(new):
            raise PreserveError("store", "발급한 store record 가 계약이 아니다")
        return new["store_id"]

    def inspect_store_id(self):
        """만들지도 연장하지도 않고 **본다**. 없으면 `None` (39차 P0-1)."""
        vid = self._canonical_store_version()
        try:
            raw = self.provider.get("store.json", vid) if vid \
                else self.provider.get("store.json")
            rec = load_canonical(raw)
        except (KeyError, ValueError, UnicodeDecodeError):
            return None
        return rec["store_id"] if _is_store_record(rec) else None

    @property
    def store_version_id(self):
        """canonical store record 의 **exact version ID** (38차 P0-1)."""
        self.store_id                       # 없으면 만들고 잠근다
        return self._canonical_store_version()

    @property
    def store_lock_mode(self):
        v = self._canonical_store_version()
        st = self.provider.describe_object("store.json", v) if v else None
        return (st or {}).get("mode")

    def _canonical_store_version(self, key: str = "store.json"):
        """정본 store version — **가장 오래된** 유효 잠금 version (37차 P0-1).

        `protected_version()` 은 최신을 고르므로 identity 에는 쓸 수 없다.
        최초 잠금이 authority 이고, 그 뒤에 무엇이 올라오든 바뀌지 않는다.
        """
        cands = self._version_candidates(key, required=False)
        now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        oldest = None
        for v in cands:                               # 최신순 → 마지막이 가장 오래됨
            st = self.provider.describe_object(key, v)
            if not isinstance(st, dict):
                continue
            # ★ 38차 P0-1 — **Compliance 만** identity root 후보다.
            #   Governance 를 durable 에서 뺐는데 selector 는 `LOCK_MODES` 로
            #   골라서, 우회 가능한 version 이 identity root 가 될 수 있었다.
            if st.get("mode") in self.DURABLE_MODES \
                    and str(st.get("retain_until") or "") > now:
                oldest = v
        return oldest

    def _store_horizon(self) -> str:
        return (dt.datetime.now(dt.timezone.utc)
                + dt.timedelta(days=MIN_RETENTION_DAYS * 10)
                ).strftime("%Y-%m-%dT%H:%M:%SZ")

    def ensure_store_lock(self, until: str) -> None:
        """store identity 를 **적어도 `until` 까지** 잠근다 (35차 P0-1).

        기한을 graph 와 결속한다 — 초판은 생성 시 한 번 고정 기한으로 잠그고
        후속 lease 기한과 대조·연장하지 않아, 오래된 store 에 새 lease 를
        만들면 담보 기간 대부분에 identity 가 삭제 가능했다.
        """
        key = "store.json"
        # ★ 36차 P0-1 — head 가 아니라 **담보 version** 을 연장한다. head 는
        #   적대적 put 이 올린 잠기지 않은 version 일 수 있고, 그것을 잠그면
        #   identity 가 아닌 남의 바이트를 담보하게 된다. 아직 담보가 없을
        #   때(생성 직후)만 head 를 잠근다.
        # ★ 37차 P0-1 — 최신이 아니라 **정본** version 을 연장한다.
        vid = self._canonical_store_version(key)
        if vid is None:
            vs = self._version_candidates(key)
            if not vs:
                raise PreserveError("store", "store.json 의 version 을 알 수 없다")
            vid = vs[-1]                       # 아직 담보가 없다 → 가장 오래된 것
        cur = self.provider.describe_object(key, vid)
        have = str((cur or {}).get("retain_until") or "")
        if have < until:
            self.provider.lock(key, vid, until)

    @property
    def uri(self) -> str:
        """provider 가 주는 **안정 식별자**. receipt·lease 가 이것을 봉인한다.

        ★ 33차 P0-1 — 초판은 `id(provider)` 를 썼다. process-local 객체
          주소라 재시작 뒤 달라지고 재사용될 수도 있다. receipt 가 URI 를
          봉인해 대조하므로 그 기본값으로는 reopen locator 가 될 수 없었다.
          안정 식별자를 못 주는 provider 는 durable 을 주장할 수 없다.
        """
        u = getattr(self.provider, "store_uri", None)
        u = u() if callable(u) else None
        if not _nonempty_str(u or ""):
            raise PreserveError(
                "capability",
                "provider 가 안정 식별자(store_uri)를 주지 않는다 — 재시작 뒤 "
                "같은 store 를 다시 열 수 없으면 durable 을 주장할 수 없다")
        return f"objectlock+cas://{u}"

    # ── capability ──────────────────────────────────────────────────────
    def query_object_lock(self) -> dict | None:
        return self.provider.describe() if self.provider is not None else None

    def lock_content_object(self, dg: str, until: str, *, data: bytes = None):
        """CAS object 쪽도 잠근다. 잠근 **version ID** 를 돌려준다.

        ★ 42차 P1 — `data` 를 주면 **그 바이트**로 새 version 을 만든다.
          호출자가 이미 digest 검증을 지난 바이트를 들고 있는데 여기서
          namespace 를 다시 뒤지면 phase 결속이 풀린다.


        ★ 38차 P0-1 — 그 version 이 journal 에 봉인할 content proof 다.

        ★ 37차 P0-1 — 36차판은 **무조건 `put`** 했다. 실물 `PutObject` 는
          요청마다 새 version 을 만들므로, 재개·수리를 반복할 때마다 새
          version 이 생기고 그것이 WORM 으로 잠겼다. 36차 fake 가 "같은
          바이트면 같은 version" shortcut 을 갖고 있어서 이 누적이 안 보였다.
          이미 있는 version 을 **재사용**하고, 없을 때만 만든다.

        ★ 41차 P1 — target 을 `_repair_target()` 이 고르고, 잠근 뒤 proof 를
          **재유도**한다. 40차는 `_existing_version()` 이 고른 최신 same-bytes
          version 을 그대로 proof 로 돌려줬다.
        """
        return self._lock_to_proof(
            self._provider_obj_key(dg), dg, until,
            (lambda: data) if data is not None else (lambda: self.read_back(dg)))

    def _version_for(self, key: str, dg: str, until: str | None = None):
        """**담보 proof** — 잠겨 있고 mode 가 담보이고 바이트가 `dg` 인 version.

        ★ 40차 P1 — 39차는 이 하나로 proof lookup 과 **수리 source** 를 함께
          맡았다. 중복이 아니라 phase contract 가 다르다:

            proof lookup : 잠긴 담보 version 이어야 한다 (이 함수)
            repair source: **아직 안 잠긴** exact bytes 도 후보다 (아래)

          `after_lease_pin` 창에서는 올바른 v1 이 아직 안 잠겼으므로, 이 함수
          하나로는 복구 가능한 상태를 못 찾았다.
        """
        for v in self._locked_versions(key, until=until):
            if self._bytes_match(key, v, dg):
                return v
        return None

    def _repair_source(self, key: str, dg: str):
        """수리가 읽을 version — **잠금 여부를 묻지 않고** 바이트로 고른다.

        찾은 version 은 아직 proof 가 아니다. 호출자가 잠근 **뒤**
        `_version_for()` 로 다시 확인해야 proof 로 승격된다.
        """
        # ★ 47차 P0-5 — 수리 경로도 **검증된 snapshot** 만 본다. 46차는 여기서
        #   `provider.versions()` 를 직접 다시 불렀고, provider 가 호출마다 다른
        #   목록을 주면 (실물 SDK 의 재시도·eventual consistency) 검증되지 않은
        #   후보가 되돌릴 수 없는 `lock()` 까지 갔다.
        for v in self._version_candidates(key, required=False):
            if self._bytes_match(key, v, dg):
                return v
        return None

    def _repair_target(self, key: str, dg: str):
        """수리가 **담보로 만들 수 있는** version — 없으면 `None` (41차 P1).

        ★ 40차는 `_existing_version(key, data)` 하나로 골랐다. 그것은 "바이트가
          같은 **가장 최신** version" 이라, 우회 가능한 head 하나가 아래의
          수리 가능한 version 을 가렸다::

              after_lease_pin crash
              v1 = correct bytes, **unlocked**       ← 잠글 수 있다
              v2 = same bytes, **Governance**, newer ← 승격 불가능

          40차는 v2 를 target 으로 골라 잠갔고, Governance 는 Compliance 로
          승격되지 않으므로 재개가 영영 실패했다. 40차 시험은 두 성분(wrong
          bytes locked head / same-bytes Governance head)을 **따로** 봤을 뿐
          결합을 안 봤다.

          네 phase 는 각자 다른 것을 묻는다::

              proof lookup   `_version_for()`     잠긴 담보 + exact bytes
              repair source  `_repair_source()`   바이트를 **읽을** 수 있는가
              repair target  여기                 담보로 **만들** 수 있는가
              journal verify `recover_*()`        봉인된 exact ID 만 조회

          담보로 만들 수 있는 것: 아직 안 잠긴 version, 그리고 이미 담보 mode 인
          version (`lock` 은 멱등이고 기한은 연장만 된다). 우회 가능한 mode 는
          후보가 아니다 — 잠그면 되돌릴 수 없이 막힌다. 하나도 없으면 `None`
          이고 호출자가 **새 version** 을 만든다.
        """
        # ★ 47차 P0-5 — `_repair_source()` 와 같은 이유로 검증된 snapshot 만.
        for v in self._version_candidates(key, required=False):
            if not self._bytes_match(key, v, dg):
                continue
            st = self.provider.describe_object(key, v)
            mode = st.get("mode") if isinstance(st, dict) else None
            if mode is None or mode in self.DURABLE_MODES:
                return v
        return None

    def _lock_to_proof(self, key: str, dg: str, until: str, make_bytes) -> str:
        """그 key 를 `dg` 바이트로 **담보로 만들고 proof 를 재유도한다** (41차 P1).

        수리가 고른 target ID 를 그대로 proof 로 믿지 않는다 — target selector
        와 proof selector 는 묻는 것이 다르므로, 잠근 **뒤** proof selector 를
        다시 돌려 typed proof 를 얻는다. 그것이 없으면 수리가 실패한 것이다.

        ★ 42차 P1 — 순서가 틀려 있었다. 41차판은 무조건
        `repair target → lock → proof 재탐색` 이라, **요청 기한을 이미 덮는
        Compliance proof 가 있는데도** 그 위의 same-bytes unlocked head 를
        새로 WORM-lock 했다. 수리가 필요 없는 상태에서 되돌릴 수 없는 version
        을 늘리는 비멱등 경로였다.

            proof lookup(요청 기한 포함) → 없을 때만 target → 없으면 검증된
            bytes 로 새 version → lock → proof 재유도(같은 기한)

        `make_bytes` 는 **이미 digest 검증을 지난 바이트**를 줘야 한다.
        namespace 를 다시 뒤지는 callback 을 넘기면 phase 결속이 다시 풀린다
        (42차 P1: hostile locked head 하나에 수리가 막혔다).
        """
        proof = self._version_for(key, dg, until=until)
        if proof is not None:
            return proof                    # 이미 담보다 — 아무것도 만들지 않는다
        vid = self._repair_target(key, dg)
        if vid is None:
            # ★ 43차 — **되돌릴 수 없는 lock 보다 검증이 먼저다.** 42차판은
            #   `put` 한 version 을 곧바로 잠갔다. caller 의 bytes 가 digest 와
            #   다르거나 provider 가 계약을 어기고 다른 version ID 를 신고하면,
            #   먼저 WORM 잔여가 생기고 그 다음에야 proof 재탐색이 실패했다.
            data = make_bytes()
            if hashlib.sha256(data).hexdigest() != dg:
                raise PreserveError(
                    "retention",
                    f"{key} 에 넣으려는 바이트가 digest 와 다르다 — 잠그기 전에 "
                    "거부한다 (lock 은 되돌릴 수 없다)")
            vid = self.provider.put(key, data)
            # ★ 45차 — **falsy·비문자열 VersionId 를 먼저 거부한다.** provider
            #   의 `get(key, version)` 은 version 이 falsy 면 exact lookup 이
            #   아니라 **head lookup** 이 된다 (실물 adapter 도 VersionId 생략
            #   으로 매핑하기 쉽다). 그러면 read-back 은 head 를 읽어 통과하고,
            #   그 사이 head 가 바뀌면 남의 version 을 잠근다.
            if not _nonempty_str(vid if isinstance(vid, str) else ""):
                raise PreserveError(
                    "retention",
                    f"{key}: provider 가 exact version ID 를 주지 않았다 "
                    f"({vid!r}) — head 조회로 떨어지면 남의 version 을 잠근다")
            if not self._bytes_match(key, vid, dg):
                raise PreserveError(
                    "retention",
                    f"{key} 의 새 version {str(vid)[:16]} 이 방금 넣은 바이트가 "
                    "아니다 — provider 가 신고한 version 을 확인 없이 잠그지 않는다")
        self.provider.lock(key, vid, until)
        proof = self._version_for(key, dg, until=until)
        if proof is None:
            raise PreserveError(
                "retention",
                f"{key} 를 담보로 만들지 못했다 (version {str(vid)[:16]}) — "
                "잠근 뒤에도 요청 기한을 덮는 담보 proof 가 없다")
        return proof

    def repair_lease_locks(self, leg_id: str, lease_digest: str,
                           until: str) -> "RetentionProof":
        """lease 의 pin 과 CAS content **둘 다** 잠그고 그 proof 를 준다 (35차 P0-1).

        ★ 37차 P0-1 — 36차판은 `pin()` 부터 불렀고, `pin()` 은 CAS content 를
          `read_back()` 한다. lease content 가 아직 안 잠긴 창에서 그것이
          삭제됐으면 여기서 실패했고, 호출자가 그 실패를 "기존 lease 없음"
          으로 바꿔 두 번째 WORM lease 를 만들었다.

          순서를 뒤집는다: **살아남은 pin 바이트가 정본**이다. pin 은 잠겨
          있거나 최소한 남아 있고, 그 바이트로 CAS content 를 되살릴 수 있다.
          pin 도 content 도 없으면 그때야 진짜 후보 부재다.
        """
        # ★ 39차 P0-1 — 수리도 **담보 version** 에서 읽는다. 적대적 최신
        #   version 이 있으면 그것을 읽어 digest 대조에서 죽었다.
        # ★ 40차 P1 — 수리는 **잠금 여부를 묻지 않고** exact bytes 를 찾는다.
        #   담보 version 만 보면 `after_lease_pin` 창의 v1 을 못 찾는다.
        key = self._provider_key(leg_id, lease_digest)
        data = self.read_pinned(leg_id, lease_digest,
                                version=self._repair_source(key, lease_digest))
        # ★ 42차 P1 — 41차판은 여기서 `has()` 에 물어 content 존재를 판단하고,
        #   없을 때만 `put_if_absent(data)` 로 되살렸다. `has()` 는 protected
        #   version 을 **읽을 수 있으면** True 이고 바이트 hash 를 안 본다.
        #   그래서 올바른 content 가 지워지고 wrong-bytes locked head 가
        #   올라온 창에서, 방금 pin 에서 **검증해 읽은 정본 bytes 를 들고
        #   있으면서** 복원을 건너뛰고 그 head 를 다시 읽다가 죽었다.
        #   (`has()` 만 strict 하게 고쳐도 뒤이어 부를 `put_if_absent()` 가
        #    같은 protected read 로 collision 을 낸다 — 검사 하나의 문제가
        #    아니라 검증된 bytes 를 버리는 것이 문제였다.)
        #
        #   존재 판정과 복원을 함께 없앤다: `lock_content_object()` 에 **그
        #   bytes 를 직접 준다.** exact bytes version 이 없으면 그것으로 새
        #   version 을 만들고, 있으면 그것을 잠근다.
        # ★ 43차 P1 — 만든 proof 를 **그대로 돌려준다.** 42차는 버리고
        #   호출자가 기한 없는 live search 로 다시 찾게 했다.
        pinned = self.lock_objects(leg_id, [lease_digest], until)
        return RetentionProof(
            lease_version=pinned[lease_digest],
            content_version=self.lock_content_object(lease_digest, until,
                                                     data=data),
            until=until)

    def recover_content_version(self, lease_digest: str, until: str = None):
        """lease CAS content 의 **담보 version** 을 재발견한다 (38차 P0-1).

        잠긴 version 중 **바이트가 digest 와 같은** 것이다. "아무 잠긴
        version" 은 proof 가 아니다.
        """
        return self._version_for(self._provider_obj_key(lease_digest),
                                 lease_digest, until=until)

    def recover_lease_version(self, leg_id: str, lease_digest: str,
                              until: str = None):
        """lease pin 의 **담보 version** 을 재발견한다 (34차 P0-1 · 39차 P0-1).

        ★ 39차 — 38차판은 "가장 최신 담보 version" 을 돌려주고 **그 version 의
          바이트가 lease digest 와 같은지** 보지 않았다. 올바른 v1 위에 wrong
          bytes 의 locked v2 가 올라오면, v1 과 graph 가 온전한데도 재개가
          실패했다. content 쪽은 `_bytes_match()` 로 고쳤는데 pin 쪽엔 같은
          결속이 없었다.
        """
        return self._version_for(self._provider_key(leg_id, lease_digest),
                                 lease_digest, until=until)

    def _orphan_lease(self, leg_id: str, objs: list,
                      min_retention_days: int) -> "VerifiedBytes | None":
        """`objects/` 에만 남은 lease content 를 찾는다 (37차 P0-1).

        `after_lease_put` 창의 잔여다 — content 는 있고 pin 은 없다. 이것을
        못 보면 재개가 새 lease 를 만들고, 그 창을 지날 때마다 orphan 이
        하나씩 쌓인다 (lease 바이트가 초마다 달라져 CAS dedup 도 안 걸린다).

        ★ 42차 P1 — **검증한 exact version 과 그 bytes 를 함께 돌려준다.**
          41차판은 `(key, version)` 을 읽어 판정하고 digest 만 넘겼고,
          호출자의 `pin()` 이 그 digest 로 namespace 를 다시 읽었다 —
          `read_back()` 은 최신 담보 version 을 고르므로, 같은 key 에
          wrong-bytes locked head 가 하나 있으면 온전한 orphan 이 있는데도
          입양이 digest mismatch 로 죽었다.
        """
        pins = self.pinned(leg_id)
        graph = set(objs)
        found: list[VerifiedBytes] = []
        seen = {v.digest for v in found}
        for key, ver in self.provider.list_versions("objects/"):
            dg = key.split("/", 1)[1]
            if dg in pins or dg in graph or dg in seen:
                continue
            try:
                raw = self.provider.get(key, ver)
                rec = load_canonical(raw)
            except (KeyError, ValueError, UnicodeDecodeError):
                continue
            # 읽은 바이트가 정말 그 digest 인가 — locator 로 넘길 것이므로
            # 여기서 못 박는다 (다음 phase 는 다시 안 읽는다).
            if hashlib.sha256(raw).hexdigest() != dg:
                continue
            if self._matches_lease(leg_id, objs, min_retention_days, rec):
                found.append(VerifiedBytes(key, ver, dg, raw))
                seen.add(dg)
        if len(found) > 1:
            raise PreserveError(
                "retention",
                f"{leg_id}: pin 없는 lease 잔여가 {len(found)}개다 "
                f"({[v.digest[:16] for v in found]}) — 어느 것이 정본인지 정할 수 없다")
        return found[0] if found else None

    def adopt_orphan(self, leg_id: str, lease: "VerifiedBytes") -> None:
        """검증이 읽은 **바로 그 바이트**로 pin 을 만든다 (42차 P1).

        `pin()` 은 digest 로 CAS namespace 를 다시 읽으므로 hostile head 하나에
        막힌다. 여기서는 locator 가 든 bytes 를 그대로 쓴다 — 이미 digest
        검증을 지났으므로 다시 탐색할 이유가 없다.
        """
        key = self._provider_key(leg_id, lease.digest)
        if self._repair_source(key, lease.digest) is None:
            self.provider.put(key, lease.data)

    def probe_enforcement(self) -> str:
        # ★ 36차 P0-1 — 계약 전체를 만족하지 못하는 provider 는 담보가 아니다.
        #   helper 를 만들어 두고 durable 경로가 안 부르면 고친 것이 아니다.
        try:
            self.assert_provider_contract()
        except PreserveError:
            return ENFORCEMENT_ADVISORY
        st = self.query_object_lock()
        if not isinstance(st, dict):
            return ENFORCEMENT_ADVISORY
        mode = st.get("mode")
        if mode not in self.LOCK_MODES:
            return ENFORCEMENT_ADVISORY
        days = st.get("min_retain_days")
        if isinstance(days, bool) or not isinstance(days, int) \
                or days < MIN_RETENTION_DAYS:
            return ENFORCEMENT_ADVISORY
        # ★ 37차 P0-1 — GOVERNANCE 는 **어떤 probe 결과로도** 담보가 아니다.
        #   36차는 우회 삭제를 canary 로 실측해 거부되면 승격했다. 그러나 그
        #   한 요청이 증명하는 것은 "현재 credential 의 version-delete 한 경로"
        #   뿐이다. retention 단축·제거 권한, 다른 principal, 이후 IAM 변경은
        #   그 요청으로 관측되지 않는다. 31차에 local mode bit 를 uid 0 이
        #   우회할 수 있다는 이유로 durable 에서 뺐으니, 같은 잣대를 쓴다.
        #   받아들이려면 bucket policy·principal 집합·retention mutation API
        #   전체를 봉인하고 계속 재검증해야 하는데, 그것은 data-plane 9연산
        #   계약으로 표현되지 않는다.
        if mode not in self.DURABLE_MODES:
            return ENFORCEMENT_ADVISORY
        return ENFORCEMENT_OBJECT_LOCK

    # ── 바이트는 provider 가 소유한다 ───────────────────────────────────
    def put_if_absent(self, data: bytes, *,
                      faults: frozenset[str] = frozenset()) -> dict:
        dg = hashlib.sha256(data).hexdigest()
        key = self._provider_obj_key(dg)
        try:
            old = self._read_protected(key)
        except KeyError:
            old = None
        if old is not None:
            if old != data:
                raise PreserveError("cas_put",
                                    f"같은 digest 인데 저장된 바이트가 다르다: {dg[:16]}")
            return {"digest": dg, "stored": False, "idempotent": True}
        if "partial_upload" in faults:
            raise PreserveError("cas_put", "업로드가 중간에 끊겼다 (주입)")
        self.provider.put(key, data)
        return {"digest": dg, "stored": True, "idempotent": False}

    def read_back(self, dg: str, *,
                  faults: frozenset[str] = frozenset()) -> bytes:
        if "no_read_access" in faults or not self.readable:
            raise PreserveError("read_back", "backend 를 되읽을 권한이 없다")
        try:
            data = self._read_protected(self._provider_obj_key(dg))
        except KeyError as ex:
            raise PreserveError("read_back", f"object 가 없다: {dg[:16]}") from ex
        if "read_back_corrupt" in faults:
            data = data + b"\x00"
        got = hashlib.sha256(data).hexdigest()
        if got != dg:
            raise PreserveError("read_back",
                                f"되읽은 바이트가 다르다: {got[:16]} ≠ {dg[:16]}")
        return data

    def has(self, dg: str) -> bool:
        try:
            self._read_protected(self._provider_obj_key(dg))
            return True
        except KeyError:
            return False

    def pin(self, leg_id: str, digests) -> dict:
        check_id(leg_id)
        made = []
        for dg in sorted(set(digests)):
            data = self.read_back(dg)          # object 가 없으면 여기서 실패
            key = self._provider_key(leg_id, dg)
            try:
                cur = self._read_protected(key)
            except KeyError:
                cur = None
            if cur is not None and cur != data:
                raise PreserveError("pin", f"pin 자리에 다른 내용이 있다: {dg[:16]}")
            if cur is None:
                self.provider.put(key, data)
            made.append(dg)
        return {"leg_id": leg_id, "pinned": made,
                "pin_set_digest": pin_set_digest(leg_id, made)}

    def pinned(self, leg_id: str) -> set:
        """★ 37차 P0-1 — **version 층**에서 열거한다.

        `keys_under()` 는 실물 `ListObjectsV2` 이고, version 없는 DELETE 가
        얹은 delete marker 가 head 면 그 key 는 목록에서 사라진다. 담보
        version 은 살아 있는데 pin 집합만 줄어들면, 등록 직전 exact pin-set
        검사가 실패하거나 — 더 나쁘게 — 재개가 담보를 못 보고 새로 만든다.
        """
        pre = f"pins/{leg_id}/"
        return {k[len(pre):] for k, _v in self.provider.list_versions(pre)}

    def read_pinned(self, leg_id: str, dg: str, *, version=None) -> bytes:
        """★ 37차 P0-1 — `version` 이 오면 **그 version 만** 읽는다.

        lease 가 봉인한 version 을 그대로 provider 에 넘기는 자리다. 없으면
        (내부 호출) 담보 version 을 재탐색한다.
        """
        key = self._provider_key(leg_id, dg)
        try:
            data = (self.provider.get(key, version) if version
                    else self._read_protected(key))
        except KeyError as ex:
            raise PreserveError(
                "pin",
                f"pin 이 없다: {dg[:16]}"
                + (f" (봉인 version {version})" if version else "")) from ex
        if hashlib.sha256(data).hexdigest() != dg:
            raise PreserveError("pin", f"pin 바이트가 digest 와 다르다: {dg[:16]}")
        return data

    def orphans(self) -> list[Path]:
        return []

    # ── lock ────────────────────────────────────────────────────────────
    def lock_objects(self, leg_id: str, digests, until: str) -> dict:
        out = {}
        for dg in sorted(set(digests)):
            key = self._provider_key(leg_id, dg)
            # ★ 37차 P0-1 — 무조건 put 하면 재시도마다 WORM version 이 쌓인다.
            # ★ 41차 P1 — 그래서 기존 version 을 재사용하는데, 재사용 후보는
            #   "바이트가 같은 최신" 이 아니라 **담보로 만들 수 있는** 것이어야
            #   한다 (`_repair_target`). 바이트를 **읽는** 후보는 또 다르다
            #   (`_repair_source` — 잠금 여부를 묻지 않는다).
            out[dg] = self._lock_to_proof(
                key, dg, until,
                lambda dg=dg, key=key: self.read_pinned(
                    leg_id, dg, version=self._repair_source(key, dg)))
        return out

    def describe_locks(self, leg_id: str, versions: dict) -> dict:
        """version 별 **현재** lock 상태. 없으면 `None` 이 들어간다."""
        return {dg: self.provider.describe_object(self._provider_key(leg_id, dg), v)
                for dg, v in sorted(versions.items())}

    def describe_content_lock(self, dg: str, version=None):
        """lease CAS content 의 lock 상태 — **봉인 version 을 주면 그것만.**

        ★ 38차 P0-1 — 37차판은 언제나 newest live locked version 을 다시
          골랐고, 그 version 의 **바이트가 digest 와 같은지**는 보지 않았다.
          그래서 wrong bytes 를 올려 잠그면 "content 가 잠겼다" 가 통과했다.
          version 을 받으면 그것만 보고, 바이트도 digest 와 대조한다.
        """
        key = self._provider_obj_key(dg)
        cands = [version] if version else self._locked_versions(key)
        v = next((c for c in cands if c and self._bytes_match(key, c, dg)), None)
        if not v:
            return None
        # 바이트 대조는 위 후보 filter(`_bytes_match`)가 이미 한다 — 여기에
        # 한 번 더 두면 같은 규칙이 두 곳에 생기고, 강한 쪽을 지워도 초록이
        # 된다 (변이로 확인했다). 규칙은 한 곳에 둔다.
        return self.provider.describe_object(key, v) or None


class LockedCasBackend(ObjectLockBackend):
    """시험·canary 가 쓰는 구체 backend — provider 를 주입받는다."""


#: payload manifest 의 닫힌 schema#: payload manifest 의 닫힌 schema. 키가 남거나 모자라면 거부한다.
_MANIFEST_KEYS = {"schema", "n_members", "total_bytes", "members", "root_digest"}
_MEMBER_KEYS = {"path", "bytes", "sha256"}
MANIFEST_SCHEMA = "payload-manifest/v1"


def _safe_member_path(root: Path, rel: str, stage: str) -> Path:
    """member 경로를 root **안**으로 가둔다.

    ★ 27차 P1-4 — `../escaped.bin` 이 restore root 밖에 파일을 썼다. CAS
      object 의 content SHA 만 확인하고 안의 경로는 아무 것도 안 봤기 때문이다.
    """
    if not isinstance(rel, str) or not rel or rel != rel.strip():
        raise PreserveError(stage, f"member 경로가 이상하다: {rel!r}")
    if "\\" in rel or rel.startswith("/") or ":" in rel:
        raise PreserveError(stage, f"member 경로는 상대 POSIX 여야 한다: {rel!r}")
    parts = rel.split("/")
    if any(pt in ("", ".", "..") for pt in parts):
        raise PreserveError(stage, f"member 경로에 traversal 이 있다: {rel!r}")
    root = Path(root).resolve()
    out = (root / rel).resolve()
    if root not in out.parents and out != root:
        raise PreserveError(stage, f"member 경로가 root 밖이다: {rel!r}")
    return out


def check_manifest(man) -> list[str]:
    """schema · 집계 · root digest · 중복 경로를 **전부** 본다."""
    if not isinstance(man, dict):
        return [f"manifest 가 dict 가 아니다: {type(man).__name__}"]
    bad = []
    if set(man) != _MANIFEST_KEYS:
        bad.append(f"키 집합이 다르다: {sorted(set(man) ^ _MANIFEST_KEYS)}")
        return bad
    if man["schema"] != MANIFEST_SCHEMA:
        bad.append(f"schema={man['schema']!r} ≠ {MANIFEST_SCHEMA}")
    ms = man["members"]
    if not isinstance(ms, list):
        return bad + ["members 가 목록이 아니다"]
    paths = []
    for i, m in enumerate(ms):
        if not isinstance(m, dict) or set(m) != _MEMBER_KEYS:
            bad.append(f"members[{i}] 키 집합이 다르다")
            continue
        if not _is_hex64(m["sha256"]):
            bad.append(f"members[{i}].sha256 이 64-hex 가 아니다")
        if isinstance(m["bytes"], bool) or not isinstance(m["bytes"], int) \
                or m["bytes"] < 0:
            bad.append(f"members[{i}].bytes 가 음이 아닌 정수가 아니다")
        # ★ 30차 P1-2 — 초판은 member path 에 `_safe_member_path()` 를 적용하지
        #   않았다. `path=7` · `../x` · absolute · backslash · colon 을 가진
        #   self-consistent manifest 가 graph 검증을 통과하고 **실제 복원에서만**
        #   실패했다. 경로 domain 을 seal·verify 양쪽에서 같은 함수로 본다.
        try:
            _safe_member_path(Path("/__manifest_domain__"), m["path"], "manifest")
        except PreserveError as ex:
            bad.append(f"members[{i}].path: {ex.msg}")
        paths.append(m["path"])
    dup = sorted({q for q in paths if paths.count(q) > 1})
    if dup:
        bad.append(f"중복 member 경로: {dup[:3]}")
    # ★ 29차 P1-3 — exact 문자열 중복만 봤다. `A.txt`/`a.txt` 와 NFC/NFD 짝이
    #   같은 대상 파일이 되는 filesystem 이 있다. seal 전에 막는다.
    folded: dict = {}
    for q in paths:
        if not isinstance(q, str):
            continue
        key = unicodedata.normalize("NFC", q).casefold()
        folded.setdefault(key, []).append(q)
    collide = sorted(v for v in folded.values() if len(set(v)) > 1)
    if collide:
        bad.append(f"case/NFC 충돌 경로: {collide[:2]}")
    non_nfc = sorted({q for q in paths if isinstance(q, str)
                      and unicodedata.normalize("NFC", q) != q})
    if non_nfc:
        bad.append(f"NFC 가 아닌 member 경로: {non_nfc[:3]}")
    for k in ("n_members", "total_bytes"):
        if isinstance(man[k], bool) or not isinstance(man[k], int) or man[k] < 0:
            bad.append(f"{k} 가 음이 아닌 정수가 아니다: {man[k]!r} "
                       "(`True == 1` 이므로 bool 을 따로 막는다)")
    if man["n_members"] != len(ms):
        bad.append(f"n_members={man['n_members']} ≠ 실제 {len(ms)}")
    tot = sum(m["bytes"] for m in ms if isinstance(m, dict)
              and isinstance(m.get("bytes"), int))
    if man["total_bytes"] != tot:
        bad.append(f"total_bytes={man['total_bytes']} ≠ 합계 {tot}")
    want = digest({k: v for k, v in man.items() if k != "root_digest"})
    if man["root_digest"] != want:
        bad.append(f"root_digest 가 재계산과 다르다 ({man['root_digest'][:16]} "
                   f"≠ {want[:16]})")
    return bad


def restore_from_cas(backend: CasBackend, manifest_digest: str, root: Path, *,
                     faults: frozenset[str] = frozenset()) -> dict:
    """**backend 에서만** 복원한다. 원본 run_dir 은 쳐다보지 않는다.

    ★ 26차 P0-1 — 초판은 원본을 복사했다. 그래서 CAS 를 비워도 통과했다.
      여기서 원본 경로를 받지 않는 것 자체가 그 재발을 막는 구조다.
    """
    stage = "cas_restore"
    try:
        man = load_canonical(backend.read_back(manifest_digest, faults=faults))
    except PreserveError as e:
        raise PreserveError(stage, f"manifest 를 회수하지 못했다: {e.msg}") from e

    bad = check_manifest(man)
    if bad:
        raise PreserveError(stage, "manifest 가 자기 자신과 어긋난다: "
                                   + "; ".join(bad[:4]))

    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    # ★ 28차 P1-3 — 이름이 `truly empty root` 인데 기존 파일이 있어도 성공했다.
    stray = [p.name for p in root.iterdir()]
    if stray:
        raise PreserveError(stage, f"복원 root 가 비어 있지 않다: {stray[:3]}")
    written = []
    members = man["members"]
    if "restore_incomplete" in faults:
        members = members[:-1] if len(members) > 1 else members
    for m in members:
        try:
            data = backend.read_back(m["sha256"], faults=faults)
        except PreserveError as e:
            raise PreserveError(stage,
                                f"member 를 회수하지 못했다 {m['path']}: {e.msg}") from e
        out = _safe_member_path(root, m["path"], stage)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        written.append(m["path"])
    return {"manifest": man, "written": written}


# ─────────────────────────────────────────────────────────────────────────────
# 1단계 — planned leg seal
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PlannedLeg:
    """실행 **전에** 못 박는 것. 이것 없이는 트랜잭션이 시작되지 않는다.

    묶음 1 의 최소 envelope 다 — 무엇을 돌리기로 했는가. 실제로 무엇이
    돌았는가는 `execution_receipt` 가 따로 적는다.

    ★ 26차 P1-7 — `design_id` 자유문자만으로는 설계 변경이 planned_id 에
      반영되지 않는다. **정본은 `pairing_design_sha256`** 이고 `design_label`
      은 사람용 별칭이다 (계약 §4.2). label 은 hash 에 들어가지 않는다.
    """

    leg_id: str
    protocol_generation: str
    pairing_design_sha256: str
    source_digest: str
    objectives: tuple[str, ...]
    total_start_budget: int
    candidate_mode: str
    #: ★ 30차 P1-3 — 원래 요구한 retention 하한을 **봉인**한다. `Hooks` 에만
    #:   있으면 나중 verifier 가 "무엇을 요구했었나" 를 복원할 수 없다.
    min_retention_days: int = MIN_RETENTION_DAYS
    design_label: str = ""          # 사람용 — hash 밖
    notes: str = ""

    def __post_init__(self):
        # ★ 30차 P1-2 — 초판은 design SHA 하나만 봤다. `protocol_generation=7`
        #   `source_digest=7` `objectives=[7]` `total_start_budget=-1`
        #   `candidate_mode=7` 이 domain 오류 없이 transaction 에 도달했다.
        #   생성과 복구가 **같은 validator** 를 쓴다.
        bad = check_envelope(self.envelope())
        if bad:
            raise PreserveError("planned_seal", "; ".join(bad[:4]))

    def envelope(self) -> dict:
        """hash 대상. **label 과 notes 는 들어가지 않는다** (사람용)."""
        return {
            "schema": "planned-leg/v3",
            "leg_id": self.leg_id,
            "protocol_generation": self.protocol_generation,
            "pairing_design_sha256": self.pairing_design_sha256,
            "source_digest": self.source_digest,
            "objectives": list(self.objectives),
            # ★ 30차 P1-2 — 초판은 `int(...)` 로 **강제 변환**했다. `True` 가
            #   `1` 이 되어 domain 검사에 도달하지 못했다. 값을 그대로 두고
            #   validator 가 보게 한다.
            "total_start_budget": self.total_start_budget,
            "candidate_mode": self.candidate_mode,
            "min_retention_days": self.min_retention_days,
        }

    def planned_id(self) -> str:
        """계획의 내용 주소. 계획을 한 글자 고치면 다른 다리가 된다."""
        return digest(self.envelope())


# ─────────────────────────────────────────────────────────────────────────────
# 2단계 — payload seal
# ─────────────────────────────────────────────────────────────────────────────

def seal_payload(run_dir: Path, *, faults: frozenset[str] = frozenset()) -> dict:
    """run_dir 의 **exact member manifest**. 경로·바이트수·sha256."""
    run_dir = Path(run_dir)
    members = []
    for p in sorted(run_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(run_dir).as_posix()
        members.append({"path": rel, "bytes": p.stat().st_size,
                        "sha256": _file_sha(p)})
    if "member_missing" in faults and members:
        members = members[:-1]
    if "stale_payload_index" in faults and members:
        members[0] = dict(members[0], sha256="0" * 64)
    man = {"schema": "payload-manifest/v1", "n_members": len(members),
           "total_bytes": sum(m["bytes"] for m in members), "members": members}
    man["root_digest"] = digest(man)
    return man


def verify_payload(run_dir: Path, man: dict) -> list[str]:
    """manifest 와 디스크가 정확히 같은가 — 누락·추가·변조를 전부 본다."""
    run_dir = Path(run_dir)
    on_disk = {p.relative_to(run_dir).as_posix(): p
               for p in run_dir.rglob("*") if p.is_file()}
    listed = {m["path"]: m for m in man["members"]}
    bad = []
    for miss in sorted(set(on_disk) - set(listed)):
        bad.append(f"manifest 에 없는 파일: {miss}")
    for miss in sorted(set(listed) - set(on_disk)):
        bad.append(f"실물이 없는 member: {miss}")
    for rel in sorted(set(on_disk) & set(listed)):
        if _file_sha(on_disk[rel]) != listed[rel]["sha256"]:
            bad.append(f"바이트 불일치: {rel}")
        elif on_disk[rel].stat().st_size != listed[rel]["bytes"]:
            bad.append(f"크기 불일치: {rel}")
    return bad


# ─────────────────────────────────────────────────────────────────────────────
# public index — per-leg exclusive create (read-modify-write 가 아니다)
# ─────────────────────────────────────────────────────────────────────────────
#
# ★ 26차 P1-4 — 초판은 YAML 하나를 읽고·고치고·`os.replace` 했다. 파일 교체는
#   원자적이지만 **read-modify-write 전체는 아니다.** 동시 writer 둘이 같은 옛
#   index 를 읽으면 마지막 쓰기가 앞 항목을 지운다 (실측으로 재현됐다).
#
#   leg 마다 **독립 파일**을 `O_EXCL` 로 만든다. 다른 leg 끼리는 서로를 볼 일이
#   없고, 같은 leg 는 정확히 하나만 성공한다.

def _leg_file(index_path: Path, leg_id: str) -> Path:
    return Path(index_path) / "legs" / f"{leg_id}.json"


def _reg_file(index_path: Path, leg_id: str) -> Path:
    return Path(index_path) / "registered" / f"{leg_id}.json"


_DIR_FSYNC: dict[str, bool] = {}


def dir_fsync_supported(where: Path) -> bool:
    """이 filesystem 에서 directory fsync 가 되는가 — 한 번만 재 본다.

    ★ 28차 P1-2 — 초판은 final hardlink 를 만든 **뒤** parent 를
      `os.open(..., O_RDONLY)` 해 fsync 했다. Windows 는 directory open 을
      거부하므로 파일은 이미 보이는데 API 는 예외였다 — 상태를 바꿔 놓고
      실패한 것이다. capability 는 **아무 것도 만들기 전에** 확인한다.
    """
    # ★ 30차 P0-3 — 초판의 캐시 키는 `resolve().anchor` 였다. POSIX 에서는
    #   서로 다른 ext4/NFS/FUSE mount 가 전부 `/` 하나로 합쳐져, 한 mount 의
    #   capability 가 다른 mount 의 답이 됐다. mount 를 실제로 가르는 것은
    #   device number 다.
    try:
        key = f"dev:{os.stat(where).st_dev}"
    except OSError:
        key = f"path:{where}"
    if key in _DIR_FSYNC:
        return _DIR_FSYNC[key]
    ok = True
    try:
        fd = os.open(where, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError:
        ok = False
    _DIR_FSYNC[key] = ok
    return ok


def _exclusive_write(path: Path, data: bytes, *,
                     require_durable: bool = True) -> bool:
    """**완성된 파일**에만 final name 을 붙인다. 이미 있으면 False.

    ★ 27차 P1-3 — 초판은 final pathname 을 먼저 `O_EXCL` 로 만들고 `os.write`
      를 한 번 호출했다. 부분 쓰기를 확인하지 않고 parent 도 fsync 하지 않아,
      5 bytes 만 쓰이면 "생성 성공" 인데 다음 읽기가 `JSONDecodeError` 였고
      immutable 파일 때문에 재시도로도 복구가 안 됐다.

      temp 에 **전부** 쓰고 fsync 한 뒤 `os.link` 로 no-replace commit 한다
      (link 는 대상이 있으면 EEXIST 로 실패하는 원자적 연산이다).
    """
    # ★ 31차 P0-3 — 초판은 `mkdir(parents=True)` 뒤 **자기 부모만** flush 했다.
    #   새 `index/legs`·`index/registered` 를 담는 `index/` edge 와, 새 `index/`
    #   를 담는 그 부모 edge 는 굳히지 않았다. "모든 새 directory parent edge"
    #   주장이 이 경로에는 적용되지 않았던 것이다.
    _mkdir_durable(path.parent, "durability")
    # ★ capability 를 먼저 본다. 못 하면 **만들기 전에** 실패한다.
    durable = dir_fsync_supported(path.parent)
    if require_durable and not durable:
        raise PreserveError(
            "durability",
            f"이 filesystem 은 directory fsync 를 지원하지 않는다 ({path.parent}) — "
            "이름이 durable 하지 않으면 crash 뒤 pointer 가 사라질 수 있다. "
            "backend capability 를 확인하고 publish 전에 멈춘다")
    tmp = path.parent / f"{path.name}.tmp-{uuid.uuid4().hex}"
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        n = 0
        while n < len(data):
            n += os.write(fd, data[n:])
        os.fsync(fd)
    finally:
        os.close(fd)
    try:
        os.link(tmp, path)          # 원자적 · 대상이 있으면 실패
        created = True
    except FileExistsError:
        created = False
    except OSError as e:                                  # pragma: no cover
        if e.errno != errno.EEXIST:
            raise
        created = False
    finally:
        tmp.unlink(missing_ok=True)
    # ★ 31차 P0-3 — 초판은 `created` 일 때만 fsync 했다. final link 뒤 fsync 가
    #   실패해 예외가 나가도 **final pathname 은 이미 존재**하므로, 재시도는
    #   `EEXIST → created=False` 가 되어 fsync 를 건너뛰고 상위 `publish()` ·
    #   `_register()` 가 "같은 바이트" 라는 이유로 성공했다. 실패 전파가
    #   재시도까지 fail-closed 가 아니었다. 이름이 있는 한 **항상** 굳힌다.
    if durable:
        _fsync_dir_strict(path.parent, "durability")
    return created


def publish(index_path: Path, entry: dict) -> dict:
    """final index 에 leg 하나를 **배타적으로** 등재한다.

    같은 leg 를 다른 내용으로 덮지 않는다 (immutable). 같은 내용이면 멱등이다.
    """
    # ★ 27차 P1-3 — `finalize_only()` 가 무조건 쓰는 키를 필수 목록에서
    #   빠뜨렸다. publish 성공 뒤 finalize 가 KeyError 로 죽을 수 있었다.
    for k in ("leg_id", "planned_id", "receipt_digest", "receipt_object",
              "payload_root_digest", "payload_manifest_digest", "backend_uri"):
        if not entry.get(k):
            raise PreserveError("publish", f"index entry 에 {k} 가 없다")
    check_id(entry["leg_id"])
    path = _leg_file(index_path, entry["leg_id"])
    data = canonical_bytes(entry)
    if _exclusive_write(path, data):
        return {"created": True, "entry": entry}
    old = path.read_bytes()
    if old != data:
        raise PreserveError("publish",
                            f"{entry['leg_id']} 가 이미 다른 내용으로 등록돼 있다 "
                            "— immutable index 는 덮지 않는다")
    return {"created": False, "entry": entry}


def index_entries(index_path: Path) -> dict:
    d = Path(index_path) / "legs"
    if not d.is_dir():
        return {}
    return {p.stem: load_canonical(p.read_bytes()) for p in sorted(d.glob("*.json"))}


def registration(index_path: Path, leg_id: str) -> dict | None:
    """등록 journal 을 **파싱해서** 돌려준다. 깨졌으면 None.

    ★ 27차 P0-2 — `is_registered()` 가 파일 존재만 봤다. 빈 파일·잘린 JSON·
      남의 `receipt_object` 를 가진 journal 도 "등록 완료" 였다.
    """
    p = _reg_file(index_path, leg_id)
    if not p.is_file():
        return None
    try:
        rec = load_canonical(p.read_bytes())
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(rec, dict) or set(rec) != _JOURNAL_KEYS:
        # ★ 30차 P1-1 — 초판은 surplus key 를 허용했다. journal 은 등록 graph
        #   의 exact typed 표현이어야 하므로 키가 남거나 모자라면 거부한다.
        return None
    if rec.get("leg_id") != leg_id:
        return None
    if not _is_hex64(rec.get("receipt_object") or ""):
        return None
    if not _is_hex64(rec.get("lease_digest") or ""):
        return None
    # ★ 39차 P0-1 — 두 locator **모두** type 을 본다. 38차판은 content 쪽을
    #   아무것도 안 봐서 int·None·dict 가 journal 을 통과했다.
    if any(not isinstance(rec.get(k), str) for k in _JOURNAL_LOCATORS):
        return None
    if not isinstance(rec.get("lease_version"), str):
        return None
    # ★ 30차 P1-1 — 초판은 `isinstance(list)` 였다. 정상 목록의 digest 를 한 번
    #   더 넣은 duplicate journal 이 `set(...) == expected` 를 통과했다.
    if not _is_unique_hex64_list(rec.get("objects")):
        return None
    # ★ 30차 — 여기서는 **모양**만 본다. `pin_set_digest` 가 journal 자기
    #   목록과 맞는지 다시 세는 것은 자기일관성일 뿐이고, 실제 결속은
    #   `verify_registered_graph()` 가 **유도한 graph** 로 재계산한다. 같은
    #   계산을 두 곳에 두면 강한 쪽을 지워도 시험이 초록이 된다 (변이로 확인).
    if not _is_hex64(rec.get("pin_set_digest") or ""):
        return None
    return rec


def has_registration_journal(index_path: Path, leg_id: str) -> bool:
    """등록 journal 이 **있다는 주장**만 본다 — 보존 완료가 아니다.

    ★ 30차 P0-2 — 초판은 `is_registered(index, leg)` 가 backend 없이도 참을
      돌려줬다. 정상 등록 뒤 `pins/` 와 `objects/` 를 모두 지워도 참이었다.
      이름 하나가 "journal 주장" 과 "보존 완료" 두 뜻을 가졌던 것이다.
      판정 API 는 backend 를 **필수**로 받고, 주장 확인은 이 이름을 쓴다.
    """
    rec = registration(index_path, leg_id)
    if rec is None:
        return False
    e = index_entries(index_path).get(leg_id)
    return bool(e) and rec["receipt_object"] == e.get("receipt_object")


def is_registered(index_path: Path, leg_id: str, backend: CasBackend) -> bool:
    """**이 backend 에서** 등록이 지금 성립하는가.

    저장된 비트가 아니라 backend 에 대고 평가하는 술어다. `backend` 는
    필수다 (30차 P0-2).
    """
    if not has_registration_journal(index_path, leg_id):
        return False
    try:
        verify_registered_graph(backend, index_path, leg_id)
    except PreserveError:
        return False
    return True


def verified_retention(backend: CasBackend, index_path: Path,
                       leg_id: str) -> dict:
    """graph 를 검증하고 그 검증이 인정한 **lease** 를 돌려준다.

    ★ 31차 P0-1 — `enforcement` 의 권위를 한 곳에 둔다. 호출자가 다시
      `probe_enforcement()` 를 부르면 같은 판단이 두 곳에 생긴다.
    """
    verify_registered_graph(backend, index_path, leg_id)
    j = registration(index_path, leg_id)
    return backend.verify_retention(
        leg_id, j["lease_digest"], lease_version=j["lease_version"],
        lease_content_version=j.get("lease_content_version") or None)


def assert_durable_retention(backend: CasBackend, index_path: Path,
                             leg_id: str) -> dict:
    """등록이 **강제되는** retention 아래 있는지 — 아니면 거부한다.

    ★ 30차 P0-1 — local filesystem 은 object-lock 을 강제하지 못하므로
      `ok=True` 를 durable retention 성공이라고 부를 수 없다. 비싼 본 실행을
      승인하는 자리는 이 함수를 통과해야 한다.
    """
    # ★ 31차 P0-1 — 강제 수준의 권위는 **한 곳**이다: `verify_retention()` 이
    #   lease 에 적힌 값을 `probe_enforcement()` 조회 결과와 대조하고, 어긋나면
    #   거기서 실패한다. 여기서 다시 조회하면 같은 계산이 두 곳에 있게 되고,
    #   그러면 강한 쪽을 지워도 시험이 초록이 된다 (30차에 세 번 겪은 형태 —
    #   실제로 이 자리의 변이가 물지 않았다).
    lease = verified_retention(backend, index_path, leg_id)
    live = lease["enforcement"]
    if live != ENFORCEMENT_OBJECT_LOCK:
        raise PreserveError(
            "durable_retention",
            f"이 backend 는 retention 을 강제하지 못한다 (조회 결과 {live!r}). "
            "local filesystem 의 pin 은 advisory 다 — 마지막 검사와 반환 사이의 "
            "창을 닫을 수 없고, uid 0 에서는 mode bit 도 잠금이 아니다. "
            "object-lock 을 강제하는 backend 에서만 durable retention 을 주장한다")
    return lease


#: 등록 journal 의 닫힌 schema (★ 30차 P1-1)
#: ★ 38차 P0-1 — `lease_content_version` 을 더한다. 37차까지 `lease_version`
#:   은 lease **pin** version 하나뿐이었고, lease CAS content version 은
#:   어디에도 봉인되지 않았다. 그래서 content lock 검사가 `objects/<lease>` 의
#:   "아무 잠긴 version" 이나 받아들였다 — 그 version 의 바이트가 lease digest
#:   와 같은지도 안 보고.
_JOURNAL_KEYS = frozenset({"leg_id", "receipt_object", "pin_set_digest",
                           "objects", "lease_digest", "lease_version",
                           "lease_content_version"})

#: ★ 39차 P0-1 — 두 locator 는 **둘 다** typed 여야 한다. 38차판은
#:   `lease_version` 의 type 만 봤고 content 쪽은 아무것도 안 봤다.
#:   (빈 값 자체는 advisory backend 에서 정상이므로, "nonempty" 요구는
#:    object-lock 판정을 하는 `verify_retention()` 이 진다.)
_JOURNAL_LOCATORS = ("lease_version", "lease_content_version")


def _register(index_path: Path, leg_id: str, receipt_object: str,
              pin_digest: str, objects: list, lease_digest: str,
              lease_version: str = "", lease_content_version: str = "") -> None:
    """durable 상태 변경. 기존 journal 이 다르면 **거부**한다.

    ★ 33차 P0-1 — `lease_version` 은 lease 자신의 lock proof 다. lease 는
      자기 digest 를 담을 수 없으므로 그 증거가 밖에 있어야 한다.
    """
    data = canonical_bytes({"leg_id": leg_id, "receipt_object": receipt_object,
                            "pin_set_digest": pin_digest,
                            "objects": sorted(set(objects)),
                            "lease_digest": lease_digest,
                            "lease_version": lease_version,
                            "lease_content_version": lease_content_version})
    path = _reg_file(index_path, leg_id)
    if _exclusive_write(path, data):
        return
    old = path.read_bytes()
    if old != data:
        raise PreserveError(
            "register",
            f"{leg_id} 의 등록 journal 이 이미 다른 내용이다 — 남의 receipt 를 "
            f"가리키거나 잘린 파일이다 ({old[:40]!r})")


# ─────────────────────────────────────────────────────────────────────────────
# 산출 manifest schema — optional 이 아니다 (26차 P1-3)
# ─────────────────────────────────────────────────────────────────────────────

#: 산출 role 별 **필수** 필드 — tagged union 의 tag 가 `role` 이다.
#:
#: ★ 30차 P1-2 — 초판은 8개 키의 nonempty 여부만 봤다. 리뷰가 그대로 적었듯
#:   `role = 7 · canonicalizer = {} · semantic_schema = [1] · producer = False`
#:   에 실제 path/hash/size 를 붙이면 등록됐다. `measured_by`·`produced_from`
#:   ·`source_file_sha256`·`n_rows`·`semantic_view_drops` 의 role 별 필수
#:   여부와 타입은 아예 정의돼 있지 않았다.
_OUTPUT_ROLES = {
    "rescored_summary": frozenset({"measured_by", "produced_from",
                                   "source_file_sha256", "n_rows",
                                   "semantic_view_drops"}),
    "rescored_rows": frozenset({"measured_by", "produced_from",
                                "source_file_sha256", "n_rows"}),
}
#: ★ 31차 P1-2 — role 마다 **exact** key set 이다. 초판은 전체 `_OUTPUT_KEYS`
#:   의 subset 인지만 봐서, `rescored_rows` 에 summary 전용
#:   `semantic_view_drops` 를 넣어도 통과했다. tagged union 이라는 이름이
#:   실제로 하는 일보다 강했다.
#: 모든 role 이 공유하는 필수 필드
_OUTPUT_BASE = ("role", "canonicalizer", "semantic_schema", "semantic_sha256",
                "relative_path", "byte_size", "file_sha256", "producer",
                "object_digest")


#: wrapper 가 **측정해서** 붙이는 필드. hook 이 신고하는 것이 아니다 (28차 P1-1).
_OUTPUT_MEASURED = ("object_digest", "measured_by")


def check_output_claim(out) -> list[str]:
    """hook 이 신고한 descriptor — wrapper 가 측정할 필드는 아직 없다."""
    return check_output(out, measured=False)


def check_output(out, *, measured: bool = True) -> list[str]:
    """재채점 산출이 계약을 만족하는가. 비면 통과. role 별 tagged union 이다."""
    if not isinstance(out, dict):
        return [f"산출이 dict 가 아니다: {type(out).__name__}"]
    bad = []
    role0 = out.get("role")
    if role0 in _OUTPUT_ROLES:
        want = set(_OUTPUT_BASE) | set(_OUTPUT_ROLES[role0])
        if not measured:
            want -= set(_OUTPUT_MEASURED)
        if set(out) != want:
            bad.append(f"role={role0} 의 키 집합이 정확하지 않다 — 남음 "
                       f"{sorted(set(out) - want)} · 모자람 {sorted(want - set(out))}")
    elif not set(out) <= _OUTPUT_KEYS:
        bad.append(f"산출 키 집합이 닫혀 있지 않다: {sorted(set(out) - _OUTPUT_KEYS)}")
    if not measured:
        stray = [k for k in _OUTPUT_MEASURED if k in out]
        if stray:
            bad.append(f"hook 이 wrapper 측정 필드를 신고했다: {stray} — "
                       "증명과 주장의 주체가 같으면 안 된다")
    role = out.get("role")
    if role not in _OUTPUT_ROLES:
        bad.append(f"role 이 계약 enum 이 아니다: {role!r} "
                   f"(허용: {sorted(_OUTPUT_ROLES)})")
    # ★ 27차 P1-5 — semantic digest 만 요구하면 "무슨 파일을 만들었는가" 가
    #   receipt 어디에도 없다. byte 축을 함께 강제한다 (25차 Q2 는 둘 다 요구).
    # ★ 30차 P1-2 — nonempty 가 아니라 **타입**을 본다.
    # ★ 31차 P1-2 — role 을 아는 경우 위의 exact key set 비교가 "모자람" 까지
    #   말한다. 여기서 다시 세면 같은 규칙이 두 곳에 있게 되고, 그러면 강한
    #   쪽(exact 비교)을 subset 으로 되돌려도 시험이 초록이 된다 (변이로 확인).
    #   role 을 모를 때만 base 필드를 따로 본다.
    if role0 not in _OUTPUT_ROLES:
        for k in _OUTPUT_BASE:
            if (measured or k not in _OUTPUT_MEASURED) and k not in out:
                bad.append(f"산출에 {k} 가 없다")
    for k in ("canonicalizer", "semantic_schema", "producer", "relative_path"):
        if k in out and not _nonempty_str(out[k]):
            bad.append(f"{k} 가 비어 있지 않은 NFC 문자열이 아니다: {out.get(k)!r}")
    for k in ("semantic_sha256", "file_sha256", "object_digest"):
        if k in out and (measured or k not in _OUTPUT_MEASURED) \
                and not _is_hex64(out.get(k)):
            bad.append(f"{k} 이 64-hex 가 아니다: {out.get(k)!r}")
    n = out.get("byte_size")
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        bad.append(f"byte_size 가 음이 아닌 정수가 아니다: {n!r}")
    # ★ 31차 P1-2 — 생성과 복구가 **같은** path validator 를 쓴다. 초판은
    #   여기서 leading slash 와 `..` 만 봤고 `_safe_member_path()` 는 backslash·
    #   colon·빈/`.` segment 까지 거부했다. 저장된 receipt 를 검증하는 쪽이,
    #   만드는 쪽이라면 거부했을 경로를 받아들였다는 뜻이다.
    try:
        _safe_member_path(Path("/__output_domain__"), out.get("relative_path"),
                          "output")
    except PreserveError as ex:
        bad.append(f"relative_path: {ex.msg}")
    # role 별 필수 필드와 타입
    for k in sorted(_OUTPUT_ROLES.get(role, frozenset())):
        if not measured and k in _OUTPUT_MEASURED:
            continue
        if k not in out:
            bad.append(f"role={role} 에는 {k} 가 필수다")
        elif k == "n_rows":
            if isinstance(out[k], bool) or not isinstance(out[k], int) or out[k] < 0:
                bad.append(f"n_rows 가 음이 아닌 정수가 아니다: {out[k]!r}")
        elif k == "semantic_view_drops":
            v = out[k]
            if not isinstance(v, list) or not all(_nonempty_str(x) for x in v):
                bad.append(f"semantic_view_drops 가 문자열 목록이 아니다: {v!r}")
        elif k == "source_file_sha256":
            if not _is_hex64(out[k]):
                bad.append(f"source_file_sha256 이 64-hex 가 아니다: {out[k]!r}")
        elif not _nonempty_str(out[k]):
            bad.append(f"{k} 가 비어 있지 않은 NFC 문자열이 아니다: {out[k]!r}")
    return bad


# ─────────────────────────────────────────────────────────────────────────────
# 트랜잭션
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Hooks:
    """검증·재채점을 주입한다. 과학 코드를 이 모듈에 넣지 않기 위해서다.

    ★ 26차 P1-3 — `expected_semantic` 은 이제 **필수**다. `None` 이면 재채점
      결과를 아무 것도 대조하지 않으므로 검증이라 부를 수 없다.
      복원 hook 은 사라졌다 — 복원은 CAS 에서만 나온다 (P0-1).
    """

    validate: object = None          # (root) -> {"ok":…, "fail":[…], "checks":{}}
    rescore: object = None           # (root) -> 산출 manifest dict
    min_retention_days: int = 365
    expected_semantic: str | None = None


def _require_hooks(hooks: Hooks) -> None:
    for name in ("validate", "rescore"):
        if getattr(hooks, name) is None:
            raise PreserveError("hooks", f"{name} hook 이 없다 — 검증 없이 통과할 수 없다")
    if not hooks.expected_semantic:
        raise PreserveError(
            "hooks", "expected_semantic 이 없다 — 재채점 결과를 대조할 기준이 "
                     "없으면 그것은 검증이 아니다 (26차 P1-3)")


def _drop_from_cas(backend: CasBackend, man: dict, man_dg: str,
                   faults: frozenset[str]) -> None:
    """read-back 뒤 CAS 를 훼손한다 — 복원이 backend 를 보는지 확인하는 주입."""
    if "cas_drop_all" in faults:
        shutil.rmtree(backend.root / "objects", ignore_errors=True)
        return
    if "cas_drop_manifest" in faults:
        backend._obj(man_dg).unlink(missing_ok=True)
    if "cas_drop_member" in faults and man["members"]:
        backend._obj(man["members"][0]["sha256"]).unlink(missing_ok=True)
    if "cas_mutate_member" in faults and man["members"]:
        p = backend._obj(man["members"][0]["sha256"])
        if p.is_file():
            b = bytearray(p.read_bytes())
            b[0] ^= 0x01
            p.write_bytes(bytes(b))


def check_hook_validation(v) -> list[str]:
    """validator hook 이 돌려준 것이 계약인가 (★ 30차 P1-2).

    `ok` 는 **exact bool**, `checks` 는 dict, `fail` 은 문자열 목록이다.
    """
    if not isinstance(v, dict):
        return [f"검증 결과가 dict 가 아니다: {type(v).__name__}"]
    bad = []
    if set(v) != {"ok", "fail", "checks"}:
        bad.append(f"키 집합이 닫혀 있지 않다: {sorted(set(v) ^ {'ok', 'fail', 'checks'})}")
        return bad
    if v["ok"] is not True and v["ok"] is not False:
        bad.append(f"ok 가 exact bool 이 아니다: {v['ok']!r}")
    if not isinstance(v["checks"], dict) or not v["checks"]:
        bad.append(f"checks 가 비어 있지 않은 dict 가 아니다: {v['checks']!r}")
    elif not all(_nonempty_str(k) for k in v["checks"]):
        bad.append("checks 의 키가 비어 있지 않은 NFC 문자열이 아니다")
    else:
        # ★ 31차 P1-1 — 초판은 `checks` 의 **값**을 보지 않았다.
        #   `{"ok": True, "fail": [], "checks": {"payload": False}}` 가
        #   통과했고, receipt 는 `{"ok": true, "n_checks": 1}` 로 축약해
        #   false subcheck 를 지웠다. 통과한 검증에서는 모든 검사가 참이어야
        #   한다 — 아니면 그것은 `fail` 에 있어야 한다.
        wrong = sorted(k for k, x in v["checks"].items() if x is not True)
        if wrong:
            bad.append(f"통과했다는데 참이 아닌 검사가 있다: {wrong[:4]}")
    if not isinstance(v["fail"], list) or not all(isinstance(x, str) for x in v["fail"]):
        bad.append(f"fail 이 문자열 목록이 아니다: {v['fail']!r}")
    elif bool(v["fail"]) == (v["ok"] is True):
        bad.append(f"ok={v['ok']!r} 와 fail={v['fail']!r} 이 서로 모순이다")
    return bad


def _validate_and_rescore(root: Path, hooks: Hooks, backend: CasBackend,
                          faults: frozenset[str]) -> tuple[dict, dict]:
    if "validator_raises" in faults:
        raise PreserveError("validate", "검증기가 예외로 죽었다 (주입)")
    v = hooks.validate(root)
    if "validator_fails" in faults:
        v = {"ok": False, "fail": ["주입된 실패"]}
    # ★ 30차 P1-2 — 초판은 `v.get("ok")` 를 **truthiness** 로 봤고 `checks` 가
    #   dict 인지 확인하지 않았다. `{"ok": "yes", "checks": "x"}` 가 통과한 뒤
    #   receipt 에는 `{"ok": true, "n_checks": 1}` 로 정규화됐다 — 저장된
    #   nested object 가 exact 여도 그 값이 실제 validator 결과를 증명하지
    #   못한다는 뜻이다. hook 결과의 domain 을 여기서 닫는다.
    vbad = check_hook_validation(v)
    if vbad:
        raise PreserveError("validate", "검증기 결과가 계약이 아니다: "
                                        + "; ".join(vbad[:3]))
    if v["ok"] is not True:
        raise PreserveError("validate", f"검증 실패: {v.get('fail')}")

    if "score_raises" in faults:
        raise PreserveError("rescore", "재채점이 예외로 죽었다 (주입)")
    out = hooks.rescore(root)
    bad = check_output_claim(out)
    if bad:
        raise PreserveError("rescore", "; ".join(bad))
    sem = ("f" * 64 if "wrong_semantic_digest" in faults
           else out.get("semantic_sha256"))
    if sem != hooks.expected_semantic:
        raise PreserveError("rescore",
                            f"재채점 semantic digest 가 봉인과 다르다: {sem!r}")

    # ★ 28차 P1-1 — hook 이 자기 파일의 SHA·크기·producer 를 **자기신고**했다.
    #   `check_output()` 은 root 를 받지 않아 파일을 열지도 않았고, 산출은
    #   temp root 와 함께 삭제됐다. 증명과 주장이 같은 주체였다.
    #   wrapper 가 안전한 경로에서 bytes 를 **한 번 읽어** 측정하고 CAS 에 넣는다.
    fp = _safe_member_path(root, out["relative_path"], "rescore")
    if not fp.is_file():
        raise PreserveError("rescore",
                            f"산출 파일이 없다: {out['relative_path']!r}")
    data = fp.read_bytes()
    measured_sha = hashlib.sha256(data).hexdigest()
    if out["file_sha256"] != measured_sha or out["byte_size"] != len(data):
        raise PreserveError(
            "rescore",
            f"산출 descriptor 가 실물과 다르다 — 신고 "
            f"{out['file_sha256'][:16]}/{out['byte_size']} vs 실측 "
            f"{measured_sha[:16]}/{len(data)}")
    obj = backend.put_if_absent(data)["digest"]
    backend.read_back(obj)
    return v, dict(out, semantic_sha256=sem, file_sha256=measured_sha,
                   byte_size=len(data), object_digest=obj,
                   measured_by="tools.preserve")


def _hit_receipt(backend: CasBackend, r_obj: str, faults: frozenset[str],
                 when: str) -> None:
    """receipt object 를 훼손하는 주입 (27차 P0-1 의 반례를 fixture 로 고정)."""
    p = backend._obj(r_obj)
    if f"receipt_drop_{when}" in faults:
        p.unlink(missing_ok=True)
    if when == "after_readback" and "receipt_mutate_after_readback" in faults \
            and p.is_file():
        b = bytearray(p.read_bytes())
        b[0] ^= 0x01
        p.write_bytes(bytes(b))


#: receipt 의 **닫힌** 키 집합. ★ 28차 P0-2 — 초판 validator 는 일곱 키만 있는
#: self-consistent receipt 도 통과시켰다. `planned_envelope`·`outputs`·
#: `validation` 이 없어도 등록됐다.
_RECEIPT_KEYS = frozenset({
    "schema", "leg_id", "planned_id", "planned_envelope", "backend_uri",
    "backend_store_id",
    "payload_root_digest", "payload_manifest_digest", "n_members",
    "total_bytes", "validation", "outputs", "retention_days", "receipt_digest",
})


#: `planned_envelope` 의 닫힌 키 집합 (`PlannedLeg.envelope()` 와 같은 규격).
_ENVELOPE_KEYS = frozenset({
    "schema", "leg_id", "protocol_generation", "pairing_design_sha256",
    "source_digest", "objectives", "total_start_budget", "candidate_mode",
    "min_retention_days"})
_VALIDATION_KEYS = frozenset({"ok", "n_checks", "checks"})

#: planned envelope 의 **값 domain** (★ 30차 P1-2)
#:
#: 초판은 design SHA 하나만 봤다. JSON 으로 표현 가능한 다음이 오류 없이
#: transaction 에 도달했다 — 리뷰가 그대로 적었다:
#:
#:     protocol_generation = 7 · source_digest = 7 · objectives = [7]
#:     total_start_budget = -1 · candidate_mode = 7
_GENERATION_RE = re.compile(r"^v[0-9]+(_[a-z0-9]+)*$")

#: 계약 §3 의 후보 정책 표에서 mode 이름을 뽑는 정규식.
_MODE_ROW = re.compile(r"^\|\s*`([a-z][a-z0-9_]*)`\s*\|")
_CONTRACT = Path(__file__).resolve().parent.parent / "docs" / "22p_gap" \
    / "STAGE3_CONTRACT.md"
_MODE_CACHE: dict[str, frozenset] = {}


def candidate_modes() -> frozenset:
    """후보 정책 enum — **계약 §3 표가 정본**이다.

    ★ 31차 P1-3 — 30차판은 여기에 목록을 **옮겨 적었고** 그것이 계약과
      달랐다. validator 는 `warm_slot_replace · random_only · base_init_only`
      를 허용하고 계약의 `equal_start_count_base_retained · union` 을
      거부했다. 계약상 유효한 두 mode 를 거부하고 계약에 없는 세 mode 를
      허용한 것이다. 30차 회귀가 `whatever` 하나만 넣어 봐서 못 잡았다.

      값을 두 곳에 두지 않는다 (CLAUDE.md 의 "정본" 규칙). 계약을 고치면
      validator 가 따라오고, 계약을 못 읽으면 fail-closed 다.
    """
    if "modes" in _MODE_CACHE:
        return _MODE_CACHE["modes"]
    try:
        txt = _CONTRACT.read_text(encoding="utf-8")
    except OSError as ex:
        raise PreserveError("contract",
                            f"계약 문서를 읽을 수 없다 ({_CONTRACT}) — "
                            "후보 정책 enum 의 정본이 없으면 멈춘다") from ex
    sec = re.search(r"(?ms)^## 3\. 후보 정책.*?(?=^## )", txt)
    if not sec:
        raise PreserveError("contract", "계약에 §3 후보 정책 절이 없다")
    modes = frozenset(m.group(1) for m in
                      (_MODE_ROW.match(ln) for ln in sec.group(0).split("\n"))
                      if m)
    if not modes:
        raise PreserveError("contract", "계약 §3 표에서 mode 를 하나도 못 읽었다")
    _MODE_CACHE["modes"] = modes
    return modes


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != "" and v == unicodedata.normalize("NFC", v)


def _pos_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool) and v > 0


def check_envelope(env) -> list[str]:
    """planned envelope 의 키 **와 값** 을 본다. 생성·복구가 같은 함수를 쓴다."""
    if not isinstance(env, dict):
        return [f"planned_envelope 가 dict 가 아니다: {type(env).__name__}"]
    bad = []
    if set(env) != _ENVELOPE_KEYS:
        return [f"planned_envelope 가 닫혀 있지 않다: "
                f"{sorted(set(env) ^ _ENVELOPE_KEYS)}"]
    if env["schema"] != "planned-leg/v3":
        bad.append(f"planned_envelope schema: {env['schema']!r}")
    if not _nonempty_str(env["leg_id"]):
        bad.append(f"leg_id 가 비어 있지 않은 NFC 문자열이 아니다: {env['leg_id']!r}")
    if not _nonempty_str(env["protocol_generation"]) or \
            not _GENERATION_RE.match(env["protocol_generation"]):
        bad.append(f"protocol_generation 이 세대 문법이 아니다: "
                   f"{env['protocol_generation']!r}")
    if not _is_hex64(env["pairing_design_sha256"] or ""):
        bad.append("pairing_design_sha256 이 64-hex 가 아니다")
    if not _nonempty_str(env["source_digest"]) or \
            not re.fullmatch(r"[0-9a-f]{16}", env["source_digest"]):
        bad.append(f"source_digest 가 16-hex 가 아니다: {env['source_digest']!r}")
    objs = env["objectives"]
    if not isinstance(objs, list) or not objs or \
            not all(_nonempty_str(o) for o in objs) or \
            len(set(objs)) != len(objs) or objs != sorted(objs):
        bad.append(f"objectives 가 정렬된 unique 문자열 목록이 아니다: {objs!r}")
    if not _pos_int(env["total_start_budget"]):
        bad.append(f"total_start_budget 이 양의 정수가 아니다: "
                   f"{env['total_start_budget']!r}")
    if env["candidate_mode"] not in candidate_modes():
        bad.append(f"candidate_mode 가 계약 enum 이 아니다: {env['candidate_mode']!r}")
    # ★ 30차 P1-3 — 원래 요구한 하한을 envelope 에 **봉인**한다. 이것이 없으면
    #   나중 verifier 가 "무엇을 요구했었나" 를 복원할 수 없다.
    if not _pos_int(env["min_retention_days"]) or \
            env["min_retention_days"] < MIN_RETENTION_DAYS:
        bad.append(f"min_retention_days 가 정책 하한 미만이다: "
                   f"{env['min_retention_days']!r}")
    return bad
#: 산출 descriptor 의 닫힌 키 집합
_OUTPUT_KEYS = frozenset({
    "role", "canonicalizer", "semantic_schema", "semantic_sha256",
    "relative_path", "byte_size", "file_sha256", "producer",
    "object_digest", "measured_by", "produced_from", "source_file_sha256",
    "n_rows", "semantic_view_drops"})


def check_receipt(rec, entry: dict, backend: "CasBackend",
                  manifest: dict | None = None) -> list[str]:
    """receipt 를 exact schema 와 결속으로 검사한다 — run 과 finalize 가 공유.

    ★ 29차 P0-3 — 초판은 **바깥 키만** 닫았다. `planned_envelope` 가
      `{"anything": "goes"}` 여도, `validation` 에 surplus key 가 있어도,
      receipt 의 집계·root 가 실제 manifest 와 달라도, `retention_days=0`
      이어도 통과했다.
    """
    if not isinstance(rec, dict):
        return [f"receipt 가 dict 가 아니다: {type(rec).__name__}"]
    bad = []
    if set(rec) != _RECEIPT_KEYS:
        bad.append(f"키 집합이 닫혀 있지 않다: 남음 {sorted(set(rec) - _RECEIPT_KEYS)} "
                   f"· 모자람 {sorted(_RECEIPT_KEYS - set(rec))}")
        return bad
    if rec["schema"] != "execution-receipt/v1":
        bad.append(f"schema: {rec['schema']!r}")
    want = digest({k: v for k, v in rec.items() if k != "receipt_digest"})
    if rec["receipt_digest"] != want:
        bad.append("receipt 안의 digest 가 자기 내용과 다르다")
    # ★ 계획이 실제로 그 계획인가 — 내용 주소를 다시 계산한다
    env = rec["planned_envelope"]
    bad += check_envelope(env)
    if isinstance(env, dict) and set(env) == _ENVELOPE_KEYS:
        if env["leg_id"] != rec["leg_id"]:
            bad.append("planned_envelope 의 leg_id 가 receipt 와 다르다")
        if digest(env) != rec["planned_id"]:
            bad.append("planned_id 가 planned_envelope 의 digest 와 다르다")
    # ★ **손에 든 backend** 와 대조한다. receipt·index 가 서로 같은 문자열만
    #   가지면 통과하던 것이 28차 P0-2 의 반례였다.
    # ★ 30차 P0-2 — URI 문자열만으로는 부족하다. `root=Path("cas")` 로 등록한
    #   뒤 cwd 를 바꾸면 다른 store 를 가리키면서 URI 가 같았다. 생성 시각에
    #   고정된 store UUID 를 함께 본다.
    if rec["backend_uri"] != backend.uri:
        bad.append(f"receipt 의 backend_uri 가 실제 backend 와 다르다 "
                   f"({rec['backend_uri']!r} ≠ {backend.uri!r})")
    if rec["backend_store_id"] != backend.store_id:
        bad.append(f"receipt 의 backend_store_id 가 실제 store 와 다르다 "
                   f"({str(rec['backend_store_id'])[:8]} ≠ {backend.store_id[:8]})")
    v = rec["validation"]
    if not isinstance(v, dict) or set(v) != _VALIDATION_KEYS:
        bad.append(f"validation 키 집합이 닫혀 있지 않다: {v!r}")
    elif v["ok"] is not True or isinstance(v["n_checks"], bool) \
            or not isinstance(v["n_checks"], int) or v["n_checks"] <= 0:
        bad.append(f"validation 값이 이상하다: {v!r}")
    elif not isinstance(v["checks"], list) \
            or not all(_nonempty_str(x) for x in v["checks"]) \
            or v["checks"] != sorted(set(v["checks"])) \
            or len(v["checks"]) != v["n_checks"]:
        bad.append(f"validation.checks 가 정렬된 unique 이름 목록이 아니거나 "
                   f"n_checks 와 다르다: {v['checks']!r}")
    outs = rec["outputs"]
    if not isinstance(outs, list) or not outs:
        bad.append("outputs 가 비었다")
    else:
        for i, o in enumerate(outs):
            for e in check_output(o):
                bad.append(f"outputs[{i}]: {e}")
            if not isinstance(o, dict) or not set(o) <= _OUTPUT_KEYS:
                bad.append(f"outputs[{i}]: 키 집합이 닫혀 있지 않다 "
                           f"({sorted(set(o) - _OUTPUT_KEYS) if isinstance(o, dict) else o!r})")
            if not _is_hex64(o.get("object_digest") or ""):
                bad.append(f"outputs[{i}]: object_digest 가 없다")
            # ★ 29차 P0-3 — descriptor 의 파일 SHA 가 곧 그 object 의 주소다.
            elif o.get("file_sha256") != o.get("object_digest"):
                bad.append(f"outputs[{i}]: file_sha256 이 object_digest 와 다르다")
    for k in ("n_members", "total_bytes", "retention_days"):
        if isinstance(rec[k], bool) or not isinstance(rec[k], int) or rec[k] < 0:
            bad.append(f"{k} 가 음이 아닌 정수가 아니다: {rec[k]!r}")
    if isinstance(rec["retention_days"], int) and \
            not isinstance(rec["retention_days"], bool) and \
            rec["retention_days"] < MIN_RETENTION_DAYS:
        bad.append(f"retention_days={rec['retention_days']} < 정책 "
                   f"{MIN_RETENTION_DAYS}")
    # ★ 29차 P0-3 — receipt 의 집계·root 를 **실제 manifest** 와 대조한다.
    if manifest is not None:
        if manifest.get("root_digest") != rec["payload_root_digest"]:
            bad.append("payload_root_digest 가 실제 manifest 와 다르다")
        if manifest.get("n_members") != rec["n_members"]:
            bad.append(f"n_members={rec['n_members']} ≠ manifest "
                       f"{manifest.get('n_members')}")
        if manifest.get("total_bytes") != rec["total_bytes"]:
            bad.append(f"total_bytes={rec['total_bytes']} ≠ manifest "
                       f"{manifest.get('total_bytes')}")
    for k in ("leg_id", "planned_id", "payload_root_digest",
              "payload_manifest_digest", "backend_uri", "receipt_digest"):
        if rec[k] != entry.get(k):
            bad.append(f"receipt.{k} 가 index 와 다르다")
    return bad


def reachable_objects(rec: dict, manifest: dict) -> set:
    """receipt 가 도달할 수 있는 object 전부 — pin 대상이다."""
    objs = {rec["payload_manifest_digest"], rec["receipt_object"]} \
        if "receipt_object" in rec else {rec["payload_manifest_digest"]}
    objs |= {m["sha256"] for m in manifest["members"]}
    objs |= {o["object_digest"] for o in rec["outputs"]}
    return {o for o in objs if _is_hex64(o)}


def verify_registered_graph(backend: CasBackend, index_path: Path,
                            leg_id: str) -> dict:
    """등록 graph 를 **pinned receipt 에서 재유도**해 pin 집합과 대조한다.

    ★ 29차 P0-1 — 초판은 journal 이 스스로 적은 `objects` 목록과 그것으로 다시
      계산한 `pin_set_digest` 만 봤다. pinned receipt 를 열어 graph 를
      재유도하지 않으므로, receipt 하나만 적은 journal 도 자기일관되기만 하면
      "등록 완료" 였다. `pin_set_digest` 는 receipt graph 와의 결속이 아니라
      **journal 자기 checksum** 이었다.

    ★ 29차 P0-2 — 그리고 `registered` 는 저장된 비트가 아니라 **backend 에 대고
      지금 평가하는 술어**여야 한다. 성공 반환과 journal 존재가 retention 을
      뜻할 수 없다 (local filesystem 에서 검증과 commit 을 한 트랜잭션으로
      묶을 수 없기 때문이다). 그래서 이 함수가 매번 다시 본다.

    순서:
      1. actual backend 의 **pin** 에서 receipt bytes 를 읽는다
      2. closed schema · planned envelope · **손에 든 backend** · policy
      3. pin 에서 manifest 를 읽고 receipt 집계·root 와 결속
      4. member + output 을 포함한 expected graph 를 재유도
      5. expected == journal.objects == 디스크의 pin 이름 (정확히 같아야 한다)
      6. 모든 pinned bytes 와 output descriptor 를 확인
    """
    stage = "verify_graph"
    check_id(leg_id)
    e = index_entries(index_path).get(leg_id)
    if not e:
        raise PreserveError(stage, f"{leg_id} 가 public index 에 없다")
    r_obj = e.get("receipt_object")
    if not _is_hex64(r_obj or ""):
        raise PreserveError(stage, f"index 의 receipt_object 가 이상하다: {r_obj!r}")

    # 1. journal — **없으면 fail-closed**. 등록 상태 검증에 journal 은 필수다.
    #    ★ 30차 P1-1 — 초판은 journal 이 None 이면 대조를 건너뛰고 성공했다.
    #    등록 **전** graph 검증은 이름이 다른 함수를 쓴다.
    j = registration(index_path, leg_id)
    if j is None:
        raise PreserveError(stage, f"{leg_id} 의 등록 journal 이 없거나 계약을 "
                                   "만족하지 않는다")
    if j["receipt_object"] != r_obj:
        raise PreserveError(stage, "journal 이 다른 receipt 를 가리킨다")

    # 2. **retention lease 를 먼저** 본다. 성공의 근거는 읽은 바이트가 아니라
    #    상태다 (30차 P0-1).
    lease = backend.verify_retention(
        leg_id, j["lease_digest"], lease_version=j["lease_version"],
        lease_content_version=j.get("lease_content_version") or None)

    # 3. receipt·manifest 를 **lease 가 담보한 pin 에서** 읽는다
    try:
        rec = load_canonical(backend.retrieve_retained(lease, r_obj))
    except PreserveError as ex:
        raise PreserveError(stage, f"pinned receipt 를 회수하지 못했다: {ex.msg}") from ex
    if not isinstance(rec, dict) or not _is_hex64(rec.get("payload_manifest_digest") or ""):
        raise PreserveError(stage, "receipt 에 payload_manifest_digest 가 없다")
    try:
        man = load_canonical(
            backend.retrieve_retained(lease, rec["payload_manifest_digest"]))
    except PreserveError as ex:
        raise PreserveError(stage, f"pinned manifest 를 회수하지 못했다: {ex.msg}") from ex
    mbad = check_manifest(man)
    if mbad:
        raise PreserveError(stage, "manifest 가 깨졌다: " + "; ".join(mbad[:3]))

    # 4. closed schema + 결속 (manifest 를 함께 넘겨 집계까지 본다)
    bad = check_receipt(rec, e, backend, manifest=man)
    if bad:
        raise PreserveError(stage, "; ".join(bad[:4]))

    # 5. expected graph 재유도 · journal · lease · 디스크가 **정확히** 같아야
    expected = reachable_objects(dict(rec, receipt_object=r_obj), man)
    if set(j["objects"]) != expected:
        raise PreserveError(
            stage, "journal 의 objects 가 receipt 에서 유도한 graph 와 다르다 "
                   f"(journal {len(j['objects'])} · 유도 {len(expected)})")
    # ★ 30차 P1-1 — journal 의 pin_set_digest 를 **기대 graph 로 재계산**한다.
    #   초판은 64-hex 모양만 봤다 — journal 자기 checksum 이었다.
    if j["pin_set_digest"] != pin_set_digest(leg_id, expected):
        raise PreserveError(stage, "journal 의 pin_set_digest 가 유도한 graph 와 다르다")
    if set(lease["objects"]) != expected:
        raise PreserveError(stage, "lease 가 담보한 graph 가 유도한 graph 와 다르다")

    # 6. 모든 retained bytes + output object 확인
    # ★ 38차 P0-1 — lease 가 봉인한 version 으로 되읽는다 (locator 재탐색 금지)
    pbad = backend.verify_pins(leg_id, expected,
                               versions=lease.get("object_versions") or None)
    if pbad:
        raise PreserveError(stage, "pin 이 불완전하다: " + "; ".join(pbad[:3]))
    for o in rec["outputs"]:
        data = backend.retrieve_retained(lease, o["object_digest"])
        if len(data) != o["byte_size"]:
            raise PreserveError(stage, f"산출 {o['role']} 의 크기가 object 와 다르다")

    # 7. ★ 30차 P0-1 — 전수 읽기 **뒤에** lease 상태를 다시 본다.
    #    초판은 `on_disk` snapshot 이 전수 읽기 **앞**이라, 읽는 족족 지우는
    #    backend 에서 member pin 이 사라진 채 성공했다. 마지막 검사가 바이트가
    #    아니라 상태여야 그 창이 닫힌다. (그 뒤의 창은 local 에서 닫을 수
    #    없다 — 그래서 이 backend 는 `advisory_local` 이라고 신고한다.)
    backend.verify_retention(leg_id, j["lease_digest"], expected=expected,
                             lease_content_version=j.get("lease_content_version") or None,
                             lease_version=j["lease_version"])
    return rec


def verify_graph_before_registration(backend: CasBackend, index_path: Path,
                                     leg_id: str, lease: dict) -> dict:
    """등록 **전** graph 검증 — journal 이 아직 없다.

    ★ 30차 P1-1 — 초판은 `verify_registered_graph()` 하나가 두 상태를 겸했다.
      journal 이 `None` 이면 대조를 건너뛰었으므로, 이름은 "registered" 인데
      등록되지 않은 상태에도 성공했다. 이름과 API 를 가른다.
    """
    stage = "verify_before_commit"
    e = index_entries(index_path).get(leg_id)
    if not e:
        raise PreserveError(stage, f"{leg_id} 가 public index 에 없다")
    rec = load_canonical(backend.retrieve_retained(lease, e["receipt_object"]))
    man = load_canonical(backend.retrieve_retained(lease, rec["payload_manifest_digest"]))
    if check_manifest(man):
        raise PreserveError(stage, "manifest 가 깨졌다")
    bad = check_receipt(rec, e, backend, manifest=man)
    if bad:
        raise PreserveError(stage, "; ".join(bad[:4]))
    expected = reachable_objects(dict(rec, receipt_object=e["receipt_object"]), man)
    if set(lease["objects"]) != expected:
        raise PreserveError(stage, "lease 가 담보한 graph 가 유도한 graph 와 다르다")
    # ★ 39차 P0-1 — 최초 성공 판정부터 **두 locator 를 모두** 쓴다. 38차판은
    #   `retain()` 이 돌려준 content version 을 여기서 버렸다.
    backend.verify_retention(
        leg_id, lease["lease_digest"], expected=expected,
        lease_version=lease.get("lease_version"),
        lease_content_version=lease.get("lease_content_version"))
    return rec


def verify_registered_receipt(backend: CasBackend, index_path: Path,
                              leg_id: str) -> dict:
    """index 가 가리키는 receipt 를 **다시 회수해** 전 결속을 대조한다.

    ★ 27차 P0-1·P0-2 — 이것이 없으면 "등록됐다" 가 "그 순간 한 번 읽혔다" 밖에
      뜻하지 않는다. 등록 직전과 `finalize_only()` 가 같은 함수를 쓴다.
    """
    stage = "verify_before_register"
    e = index_entries(index_path).get(leg_id)
    if not e:
        raise PreserveError(stage, f"{leg_id} 가 public index 에 없다")
    r_obj = e.get("receipt_object")
    if not _is_hex64(r_obj or ""):
        raise PreserveError(stage, f"index entry 의 receipt_object 가 이상하다: {r_obj!r}")
    try:
        raw = backend.read_back(r_obj)
    except PreserveError as ex:
        raise PreserveError(stage, f"receipt 를 회수하지 못했다: {ex.msg}") from ex
    rec = load_canonical(raw)
    bad = check_receipt(rec, e, backend)
    if bad:
        raise PreserveError(stage, "; ".join(bad[:4]))
    return rec


def run_transaction(planned: PlannedLeg, run_dir: Path, backend: CasBackend,
                    index_path: Path, hooks: Hooks, *,
                    faults: frozenset[str] = frozenset(),
                    drop_source_after_seal: bool = False) -> dict:
    """10단계를 순서대로. publish 전에 멈추면 public index 는 비어 있다.

    `drop_source_after_seal` 은 회귀용이 아니라 **증명용**이다 — 업로드 뒤
    원본을 지우고도 끝까지 간다면, 복원이 backend 에서 나온 것이 확실하다.
    """
    faults = frozenset(faults)
    unknown = faults - FAULTS
    if unknown:
        raise ValueError(f"모르는 fault: {sorted(unknown)}")
    run_dir = Path(run_dir)
    _require_hooks(hooks)

    # ── 0. backend 능력 ─────────────────────────────────────────────────
    retention = 1 if "retention_too_short" in faults else backend.retention_days
    if retention < hooks.min_retention_days:
        raise PreserveError("capability",
                            f"보존 기간 {retention}일 < 요구 {hooks.min_retention_days}일")

    # ── 1. planned leg seal — run_spec 이 **있어야** 한다 (P1-3) ─────────
    pid = planned.planned_id()
    spec_path = run_dir / "run_spec.json"
    if not spec_path.is_file():
        raise PreserveError("planned_seal",
                            "run_spec.json 이 없다 — 실행이 계획을 기록했다는 "
                            "증명이 없으면 봉인값으로 채우지 않는다")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    for k in ("planned_id", "source_digest"):
        if not spec.get(k):
            raise PreserveError("planned_seal", f"run_spec 에 {k} 가 없다")
    claimed = "다른-계획" if "wrong_planned_id" in faults else spec["planned_id"]
    if claimed != pid:
        raise PreserveError("planned_seal",
                            f"실행이 가리키는 계획 {claimed[:16]!r} ≠ 봉인한 계획 {pid[:16]}")
    got = "다른-digest" if "wrong_source_digest" in faults else spec["source_digest"]
    if got != planned.source_digest:
        raise PreserveError("planned_seal", f"code identity 가 계획과 다르다: {got!r}")

    # ── 2. payload seal ─────────────────────────────────────────────────
    man = seal_payload(run_dir, faults=faults)
    # 봉인 **뒤** 손상 — 전송·보관 중 변조가 실제 모양이다
    if "member_bit_flip" in faults:
        victim = next(p for p in sorted(run_dir.rglob("*")) if p.is_file())
        b = bytearray(victim.read_bytes())
        b[0] ^= 0x01
        victim.write_bytes(bytes(b))
    if "member_extra" in faults:
        (run_dir / "__stowaway__").write_bytes(b"not in the manifest")
    bad = verify_payload(run_dir, man)
    if bad:
        raise PreserveError("payload_seal", "; ".join(bad[:4]))

    # ── 3. CAS staging put-if-absent ────────────────────────────────────
    for m in man["members"]:
        backend.put_if_absent((run_dir / m["path"]).read_bytes(), faults=faults)
    man_dg = backend.put_if_absent(canonical_bytes(man), faults=faults)["digest"]

    # ── 4. read-back ────────────────────────────────────────────────────
    for m in man["members"]:
        backend.read_back(m["sha256"], faults=faults)
    backend.read_back(man_dg, faults=faults)

    _drop_from_cas(backend, man, man_dg, faults)

    # 여기서 원본을 지운다 — 이후는 backend 만으로 가야 한다
    if drop_source_after_seal:
        shutil.rmtree(run_dir)

    # ── 5~9 ─────────────────────────────────────────────────────────────
    return _finalize(planned.leg_id, pid, planned.envelope(), man_dg,
                     man["root_digest"], backend, index_path, hooks,
                     retention, faults)


def _finalize(leg_id: str, pid: str, envelope: dict, man_dg: str,
              root_digest: str, backend: CasBackend, index_path: Path,
              hooks: Hooks, retention: int, faults: frozenset[str]) -> dict:
    """CAS 복원 → 검증 → 재채점 → receipt 저장 → publish → 등록.

    **원본 run_dir 을 받지 않는다.** `finalize_only()` 가 같은 경로를 쓴다.
    """
    root = Path(tempfile.mkdtemp(prefix=f"preserve_{leg_id}_"))
    try:
        # ── 5. CAS 에서만 복원 ──────────────────────────────────────────
        res = restore_from_cas(backend, man_dg, root, faults=faults)
        man = res["manifest"]
        rbad = verify_payload(root, man)
        if rbad:
            raise PreserveError("empty_root_restore", "; ".join(rbad[:4]))

        # ── 6~7. 검증 + 복원본만으로 재채점 ─────────────────────────────
        v, out = _validate_and_rescore(root, hooks, backend, faults)

        # ── 8. receipt 를 **CAS 에 저장**하고 되읽는다 (P0-2) ───────────
        receipt = {
            "schema": "execution-receipt/v1",
            "leg_id": leg_id,
            "planned_id": pid,
            "planned_envelope": envelope,
            "backend_uri": backend.uri,
            # ★ 30차 P0-2 — 경로는 겹칠 수 있다. store 생성 시각에 고정된
            #   UUID 를 함께 봉인해야 "같은 store 인가" 에 답할 수 있다.
            "backend_store_id": backend.store_id,
            "payload_root_digest": root_digest,
            "payload_manifest_digest": man_dg,
            "n_members": man["n_members"],
            "total_bytes": man["total_bytes"],
            # ★ 31차 P1-1 — 숫자 하나로 축약하면 **무엇을 봤는지** 사라진다.
            #   검사 이름 집합을 봉인해 검사를 바꿔치기해도 개수만 같으면
            #   통과하던 자리를 막는다.
            "validation": {"ok": True,
                           "n_checks": len(v["checks"]),
                           "checks": sorted(v["checks"])},
            "outputs": [out],
            "retention_days": retention,
        }
        receipt["receipt_digest"] = digest(receipt)   # 이 시점엔 키가 없다
        r_obj = backend.put_if_absent(canonical_bytes(receipt), faults=faults)["digest"]
        back = load_canonical(backend.read_back(r_obj, faults=faults))
        if back != receipt:
            raise PreserveError("receipt", "저장한 receipt 를 되읽었더니 다르다")

        # ★ 27차 P0-1 — 한 번의 read-back 은 **회수 가능성 불변식이 아니다.**
        #   되읽은 직후 지워도 초판은 publish 와 등록까지 갔다. 주입으로
        #   그 상황을 만들고, 등록 직전에 다시 회수해 대조한다.
        _hit_receipt(backend, r_obj, faults, "after_readback")

        # ── 9. per-leg 배타 publish ─────────────────────────────────────
        if "crash_before_publish" in faults:
            raise PreserveError("publish", "publish 직전에 죽었다 (주입)")
        publish(index_path, {"leg_id": leg_id, "planned_id": pid,
                             # ★ envelope 를 함께 싣는다 — `finalize_only` 가
                             #   **바이트 동일한** receipt 를 다시 만들려면
                             #   원본 run_dir 없이도 계획을 알아야 한다.
                             "planned_envelope": envelope,
                             "receipt_digest": receipt["receipt_digest"],
                             "receipt_object": r_obj,
                             "payload_root_digest": root_digest,
                             "payload_manifest_digest": man_dg,
                             "backend_uri": backend.uri})

        _hit_receipt(backend, r_obj, faults, "after_publish")

        # ── 10. 등록 = **object graph retention commit** ─────────────────
        if "crash_after_publish" in faults:
            raise PreserveError("register", "publish 뒤 등록 전에 죽었다 (주입)")
        lease = _commit_registration(backend, index_path, leg_id)
        # ★ 30차 P0-1 — `ok=True` 가 durable retention 을 뜻하지 않는다.
        #   강제 수준을 값으로 돌려주고, 호출자가 그것을 보고 판단한다.
        return {"ok": True, "receipt": receipt, "planned_id": pid,
                "payload_root_digest": root_digest, "receipt_object": r_obj,
                "retention": lease,
                "durable": lease["enforcement"] == ENFORCEMENT_OBJECT_LOCK}
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _commit_registration(backend: CasBackend, index_path: Path,
                         leg_id: str) -> dict:
    """도달 가능한 graph 를 **전부 pin 한 뒤**에만 등록 기록을 남긴다.

    ★ 28차 P0-1 — 초판은 receipt 를 한 번 더 읽고 journal 을 썼다. 두 연산이
      같은 retention 안에 없으므로, 마지막 read 직후 지우면 등록이 성립하면서
      회수가 불가능해졌다. 성공 불변식을 구조로 만든다:

        registered(leg) ⇒ receipt · manifest · member · 산출 전부 회수 가능
    """
    e = index_entries(index_path).get(leg_id)
    if not e:
        raise PreserveError("register", f"{leg_id} 가 public index 에 없다")
    rec = verify_registered_receipt(backend, index_path, leg_id)
    man = load_canonical(backend.read_back(rec["payload_manifest_digest"]))
    if check_manifest(man):
        raise PreserveError("register", "receipt 가 가리키는 manifest 가 깨졌다")

    objs = reachable_objects(dict(rec, receipt_object=e["receipt_object"]), man)

    # ★ 30차 P0-1 — pin 을 하나씩 만들고 나서 "다 있나" 를 세는 것이 아니라,
    #   graph 를 **하나의 retention lease** 로 붙든다. lease 자체가 CAS object
    #   이고 pin 되므로 위조하면 graph digest 가 어긋난다.
    lease = backend.retain(leg_id, objs,
                           min_retention_days=rec["planned_envelope"]["min_retention_days"])
    verify_graph_before_registration(backend, index_path, leg_id, lease)

    _register(index_path, leg_id, e["receipt_object"],
              pin_set_digest(leg_id, objs), sorted(objs), lease["lease_digest"],
              lease.get("lease_version") or "",
              lease.get("lease_content_version") or "")

    # ★ 29차 P0-2 / 30차 P0-1 — commit 뒤에 **다시** 본다. 그 검증의 마지막
    #   단계는 바이트 읽기가 아니라 lease 상태 확인이다.
    verify_registered_graph(backend, index_path, leg_id)
    return lease


def finalize_only(leg_id: str, backend: CasBackend, index_path: Path) -> dict:
    """publish 는 됐는데 등록 전에 죽은 다리를 **회수만으로** 닫는다.

    ★ 27차 P0-2 — 초판은 `_finalize()` 를 다시 호출했다. 그러면 CAS payload
      restore → validate → `hooks.rescore` → **새 receipt 생성**까지 반복한다.
      원본 12시간 fitting 을 다시 돌리지 않는다는 좁은 뜻은 맞지만, "재계산
      없이 CAS 만으로" 는 사실이 아니었다. analyzer 환경이 조금만 달라도 새
      receipt 가 달라져 immutable publish 에서 복구가 실패한다.

      이제 **hook 을 인자로 받지 않는다.** 재계산이 구조적으로 불가능하다.
      receipt 가 없거나 결속이 어긋나면 재생성하지 말고 멈춘다.
    """
    check_id(leg_id)
    e = index_entries(index_path).get(leg_id)
    if e is None:
        raise PreserveError("finalize_only",
                            f"{leg_id} 가 public index 에 없다 — 이어 붙일 것이 없다")
    # ★ 28차 P0-1 — 초판은 journal 만 보고 `already=True` 를 돌려줬다.
    #   등록된 뒤에 object 를 잃으면 그 말이 거짓이 된다. 항상 graph 를 본다.
    # ★ 29차 P0-1 — 초판은 listed pins 만 맞으면 `verify_registered_receipt()`
    #   를 부르지 않고 `already=True` 를 돌려줬다. 그래서 subset journal 과
    #   foreign backend 복사가 통과했다. 항상 graph 를 재유도한다.
    # ★ 31차 P0-1 — 초판은 두 경로 모두 `ok=True` 만 돌려줬다. "`ok=True` 의
    #   뜻을 좁혔다" 가 **모든 public 성공 경로**에 적용되지 않았다는 뜻이다.
    #   `run_transaction` 과 같은 typed retention 결과를 돌려준다.
    if registration(index_path, leg_id) is not None:
        lease = verified_retention(backend, index_path, leg_id)  # 실패하면 예외
        # ★ 32차 P0-3 — journal 이 **보인다**고 durable 한 것이 아니다.
        #   `during_journal_fsync` 에서 죽으면 이름은 보이는데 그 directory 가
        #   아직 안 굳었다. 초판은 여기서 그대로 `ok=True` 를 돌려줘
        #   interrupted commit 을 완료하지 않았다 — 뒤의 power loss 에서
        #   journal 이 사라질 수 있었다. 재개가 commit 을 **끝낸다**.
        _fsync_dir_strict(_reg_file(index_path, leg_id).parent, "register")
        return {"ok": True, "already": True, "retention": lease,
                "durable": lease["enforcement"] == ENFORCEMENT_OBJECT_LOCK,
                "receipt_object": e["receipt_object"]}
    lease = _commit_registration(backend, index_path, leg_id)
    return {"ok": True, "already": False,
            "pin_set_digest": pin_set_digest(leg_id, lease["objects"]),
            "retention": lease,
            "durable": lease["enforcement"] == ENFORCEMENT_OBJECT_LOCK,
            "receipt_object": e["receipt_object"]}


# ═════════════════════════════════════════════════════════════════════════════
# 46차 P0-11 — planned leg index (계약 §13.4 가 신고하던 "묶음 9 의 남은 절반")
#
# 왜: 보존 원장의 coverage 기준이 **커밋된 투영**이었다. 그래서 새 다리를 돌려도
#   투영을 만들기 전에는 아무 회귀도 깨지지 않았다 — 2026-08-20 에 warm 7다리를
#   그렇게 돌렸고 보존 없이 잃었다. 실행 **전에** 막으려면 계획 index 와 그것을
#   보는 gate 가 있어야 한다.
#
# 무엇이 authority 인가: 사람이 원장에 적은 `planned` 항목 하나다. 그 항목은
#   (a) 어느 다리를 (b) 어느 **active** cohort 아래 (c) **어떤 code identity 로**
#   돌려도 좋은지를 말한다. 셋 중 하나라도 다르면 실행하지 않는다.
#
# 무엇이 authority 가 아닌가: 실행기가 계산해서 넣는 값. 계획은 실행기의 출력이
#   아니라 입력이다 (자기 출력이 자기 근거가 되면 gate 가 아니다 — 37차 #9 에서
#   같은 형태를 이미 겪었다).
# ═════════════════════════════════════════════════════════════════════════════

#: 계획 항목의 **닫힌** key 집합. 빠진 key 의 `None` 은 "선언하지 않았다" 와
#: 구별되지 않는다 — 이 저장소가 pointer schema 에서 이미 겪은 형태다.
PLANNED_KEYS = ("leg_id", "cohort_id", "status", "authorization_kind",
                "authorized_source_digest", "run_spec_digest",
                "recorded_on", "근거")

#: ★ 48차 P0-5 — prospective 항목은 `run_spec:` 도 담는다. 47차는 계획이
#:   `run_spec_digest`(불투명 64hex)만 들고 있어서, 그 digest 가 **무엇의**
#:   주소인지 원장만 보고는 알 수 없었다. 사람이 승인한 내용이 기계가 읽을 수
#:   없는 형태면 gate 는 "어떤 dict 든 이 digest 를 내면 통과" 가 된다.
#:   소급 항목에는 없다 (그때는 봉인된 계획 자체가 없었다).
PLANNED_KEYS_PROSPECTIVE = PLANNED_KEYS + ("run_spec",)

#: ★ 47차 — 승인의 **종류**. 46차는 이 구분이 없어서 소급 기록 8건과 진짜
#:   실행 전 승인이 같은 schema 로 섞였고, 그래서 "실행 전 gate 가 실제로
#:   작동한 적이 있는가" 를 기계가 답할 수 없었다 (자유문자 근거 안에만
#:   있었다).
#:
#:   prospective  — 실행 **전에** 사람이 승인했다. `run_spec_digest` 가 실제
#:                  계획의 내용 주소이고 claim 이 이것만 받는다.
#:   retrospective— index 도입 **전에** 이미 돌았다. 역사 목록일 뿐이며
#:                  실행 gate 증거로 세지 않는다. claim 대상이 아니다.
AUTHORIZATION_KIND = ("prospective", "retrospective")

#: 소급 항목의 `run_spec_digest` 자리. 그때는 봉인된 계획이 없었다 — 없는 것을
#: 있는 척하는 대신 **없었다고 적는다**.
RETROSPECTIVE_SPEC = "retrospective:no-preauthorization"

#: 계획 항목의 정확한 상태 enum (47차 P0-1 — lifecycle 로 넓혔다).
#:
#:   planned   — 아직 안 돌렸다. **이것만이 claim 대상**이다.
#:   running   — claim 이 살아 있다. 재개(resume)만 가능하고 새 claim 은 못 한다.
#:   executed  — 끝났다. 기록이지 승인이 아니다.
#:   abandoned — 사람이 접었다. claim 도 finalize 도 안 된다.
PLANNED_STATUS = ("planned", "running", "executed", "abandoned")

#: lifecycle 의 phase — 둘 다 끝나야 finalize 된다.
CLAIM_PHASES = ("grid", "fit")

#: claim 파일이 담는 **닫힌** key 집합.
#:
#: ★ 49차 P0-3 — `attempt` 하나를 **공개 식별자와 비밀 credential 로 가른다.**
#:   48차는 재개 credential 을 claim 파일에 평문으로 담았다. 그러면 claims
#:   root 를 읽을 수 있는 누구나 소유 증명을 만들 수 있으므로 "소유 증명이
#:   있어야 재개한다" 는 규칙이 파일 권한 하나로 무너진다 — credential 이
#:   곧 파일 내용이었다.
#:
#:   `attempt_id`       — 공개. 원장·로그·진단 API 에 그대로 적는다.
#:   `attempt_verifier` — `sha256(token)`. 저장하는 것은 이것뿐이고 token 자체는
#:                        디스크의 이 파일에 **없다**.
CLAIM_KEYS = ("leg_id", "cohort_id", "attempt_id", "attempt_verifier",
              "run_spec_digest", "source_digest", "opened_at", "phases")

DEFAULT_LEDGER = (Path(__file__).resolve().parents[1]
                  / "docs" / "22p_gap" / "LEG_PRESERVATION.yaml")


def _load_ledger(ledger=None) -> dict:
    import yaml

    path = Path(ledger or DEFAULT_LEDGER)
    if not path.is_file():
        raise PreserveError(
            "plan", f"보존 원장이 없다: {path} — 계획 index 를 읽을 수 없으므로 "
                    "아무 것도 실행하지 않는다")
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(doc, dict):
        raise PreserveError("plan", f"보존 원장이 map 이 아니다: {path}")
    return doc


#: cohort 상태 enum — publisher(`row_projection._LEDGER_STATUS`)와 같은 값이다.
#: 두 곳에 적혀 있으므로 `test_the_two_parsers_agree_on_the_cohort_contract` 가
#: 둘이 갈라지지 않는지 본다.
COHORT_STATUS = ("active", "frozen")


def _cohort_dir_of(cohort: dict, where) -> Path:
    """cohort `dir` 을 **정규 · 저장소-상대 · 격리**로 강제한다 (47차).

    `pathlib` 의 `/` 는 오른쪽이 절대 경로면 왼쪽을 버린다. 그래서 검사 없이
    join 하면 `dir: /etc` 가 저장소 밖을 가리킨다. 같은 곳을 여러 표기로 적을
    수 있으면 중복 선언 검사도 무의미해진다.
    """
    import posixpath

    raw = cohort.get("dir")
    cid = cohort.get("cohort_id")
    if type(raw) is not str or not raw:
        raise PreserveError(
            "plan", f"cohort {cid!r} 의 `dir` 이 비어 있지 않은 문자열이 아니다: "
                    f"{raw!r} ({where})")
    if posixpath.isabs(raw) or posixpath.normpath(raw) != raw \
            or ".." in raw.split("/"):
        raise PreserveError(
            "plan", f"cohort {cid!r} 의 `dir` 이 정규 저장소-상대 경로가 아니다: "
                    f"{raw!r} — 절대 경로·`..`·`.`·중복 slash 를 쓰지 않는다")
    root = REPO_ROOT.resolve()
    got = (REPO_ROOT / raw).resolve()
    if got != root and root not in got.parents:
        raise PreserveError(
            "plan", f"cohort {cid!r} 의 `dir` 이 저장소 밖을 가리킨다: {raw!r} → {got}")
    return got


REPO_ROOT = Path(__file__).resolve().parents[1]


SMOKE_NAMESPACE = REPO_ROOT / "results" / "_smoke"


def assert_run_is_authorized(leg_id: str, phase: str, paths, run_spec: dict,
                             source_digest: str, ledger=None,
                             claims_root=None, token: str | None = None,
                             token_file=None):
    """비싼 계산 **직전**에 부르는 단 하나의 gate (47차 P0-2 조건 11-c).

    46차 gate 는 `run.sh` **안에만** 있었다. `--leg` 는 shell 이 소비했고
    `python -m src.grid` · `python -m src.fitting` 직접 호출은 계획을 전혀
    보지 않았다. gate 가 wrapper 에 있으면 wrapper 를 안 쓰면 그만이다.

    `paths` 의 **모든** 경로가 smoke namespace 안이면 면제한다 — smoke 자신이
    pipeline 을 돌아야 하기 때문이다. 판정은 어휘가 아니라
    `is_inside_namespace()` 의 정규 격리다.

    돌려주는 것은 살아 있는 claim 이다. 없으면 만들고(계획 대조 + 원자적
    발급), 있으면 같은 attempt 를 이어받는다. 두 phase(grid·fit)가 한 claim 을
    공유하므로 `all` 이 두 process 로 갈라져도 attempt 는 하나다.
    """
    real = [Path(x) for x in paths if x]
    if real and all(is_inside_namespace(x, SMOKE_NAMESPACE) for x in real):
        return None
    # ★ 49차 P0-3 — 소유 증명은 **파일 경로**로 넘어온다 (argv 는 `ps` 로
    #   새어 나간다). 파일이 있으면 그것이 곧 "이미 발급된 실행에 붙어라" 다.
    if token_file is not None and Path(token_file).is_file():
        token = read_token_file(token_file)
    path = _claim_path(leg_id, claims_root)
    if path.is_file():
        # ★ 48차 P0-3 — **자동 재개하지 않는다.** 47차는 claim 이 보이면
        #   credential 없이 이어받았고, 그래서 같은 public 호출 둘이 모두
        #   compute 에 들어갔다. 재개는 소유 증명을 든 실행만 한다.
        if not _nonempty_str(token or ""):
            raise PreserveError(
                "plan",
                f"{leg_id!r} 은 이미 실행 중이다 (claim: {path}) — 두 번째 "
                "실행을 시작할 수 없다. 중단된 실행을 이으려면 그 실행의 "
                "소유 증명(token 파일)을 주라")
        claim = resume_claim(leg_id, claims_root, token=token, ledger=ledger)
        want = run_spec_digest(run_spec)
        if claim.run_spec_digest != want:
            raise PreserveError(
                "plan",
                f"{leg_id!r} 의 살아 있는 claim 은 다른 run_spec 을 봉인했다 "
                f"({claim.run_spec_digest[:16]} ≠ {want[:16]}) — 같은 claim 으로 "
                "다른 실행을 이어붙일 수 없다")
        if claim.source_digest != source_digest:
            raise PreserveError(
                "plan",
                f"{leg_id!r} 의 claim 이 다른 code identity 로 열렸다 "
                f"({claim.source_digest} ≠ {source_digest}) — 실행 도중 "
                "RUN_SCOPE 가 바뀌었다")
        return claim
    # 아직 없다 — 지금 발급한다. `token_file` 을 준 실행은 **coordinator** 이므로
    # 그 자리에 소유 증명을 남겨 다음 phase 가 이어받게 한다.
    if token_file is not None:
        return open_leg_run(leg_id, run_spec, source_digest, token_file,
                            ledger=ledger, claims_root=claims_root)
    return claim_planned_leg(leg_id, run_spec, source_digest,
                             ledger=ledger, claims_root=claims_root)


def is_inside_namespace(path, namespace) -> bool:
    """`path` 가 `namespace` **안**인가 — 어휘가 아니라 실물로 (47차 P0-3).

    46차 gate 는 shell `case` pattern 이었다. 그래서 다음이 면제를 받았다::

        --out results/_smoke/../grid_fit_v4      # 문자열은 안, 실물은 밖
        --out results/_smoke/link/x              # link 가 밖을 가리킨다

    규칙 셋을 모두 만족해야 안이다:

      1. `..` 성분이 없다 (정규 형태)
      2. namespace 부터 마지막 **존재하는** 성분까지 어느 것도 symlink 가 아니다
      3. 그 실물 경로가 namespace 의 실물 경로 아래다

    아직 없는 하위 경로는 허용한다 (출력 디렉터리는 실행이 만든다). 다만 없는
    성분 **앞**까지는 위 규칙이 그대로 적용된다.
    """
    ns = Path(namespace)
    try:
        ns_real = ns.resolve(strict=True)
    except OSError:
        return False
    p = Path(path)
    if ".." in p.parts:
        return False
    # namespace 실물부터 한 성분씩 내려가며 symlink 를 거부한다
    try:
        rel = p.absolute().relative_to(ns.absolute())
    except ValueError:
        return False
    cur = ns_real
    for part in rel.parts:
        if part in (".", ""):
            continue
        nxt = cur / part
        try:
            st = os.stat(nxt, follow_symlinks=False)
        except FileNotFoundError:
            return True                 # 여기부터는 아직 없다 — 실행이 만든다
        except OSError:
            return False
        if stat.S_ISLNK(st.st_mode):
            return False                # alias 는 언제든 밖을 가리킬 수 있다
        cur = nxt
    try:
        return cur == ns_real or ns_real in cur.parents or cur.samefile(ns_real)
    except OSError:
        return False


#: 승격 거부의 **고유 표식**. 경로에 "smoke" 가 들어 있으므로 그 단어만으로는
#: 회귀가 거부 이유를 증명하지 못한다 — sink 는 이 문장을 낸다.
SMOKE_REFUSAL = "smoke namespace 산출은 승격 대상이 아니다"


def assert_not_smoke_provenance(paths, sink: str) -> None:
    """smoke 산출을 **정본으로 승격하지 못하게** 한다 (48차 P0-8).

    47차는 smoke 를 계획 gate 에서 **면제**했다 (계약 §13.3.3). 그 면제의 전제는
    "그 산출이 정본이 되지 않는다" 인데, 그것을 지키는 것이 아무 것도 없었다:

        REPORT_OUT=docs/RESULTS.md ./run.sh --mode report --in results/_smoke/x
        ./scripts/archive_results.sh results/_smoke/x

    둘 다 gate 를 한 번도 안 지난 실행을 인용 대상 자리에 올렸다. 면제와 승격
    금지는 **같은 경계**여야 한다 — 한쪽만 있으면 그것은 경계가 아니라 우회로다.

    판정은 `is_inside_namespace()` 로 한다. 계획 gate 의 면제를 정하는 바로 그
    함수다 — 두 규칙이 갈리면 어느 쪽이 경계인지 정할 수 없다.
    """
    bad = [str(p) for p in paths
           if p is not None and is_inside_namespace(p, SMOKE_NAMESPACE)]
    if bad:
        raise PreserveError(
            "promote",
            f"{SMOKE_REFUSAL} — {sink} 로 올리려는 입력이 {SMOKE_NAMESPACE} "
            f"아래에 있다: {bad}. smoke 는 계획 gate 를 면제받는 자리이므로 "
            "(계약 §13.3.3) 그 산출은 인용 대상이 될 수 없다. 정본을 만들려면 "
            "계획된 다리로 namespace 밖에서 다시 돌려라")


def planned_index(ledger=None) -> dict:
    """`planned:` 를 **검증해서** leg_id → 항목으로 돌려준다 (순수 함수).

    조회 **전에** 전체를 본다 — 40차 #9 에서 배운 것이다. 항목별로 lazy 하게
    검사하면 어느 소비자를 부르냐에 따라 판정이 달라진다.
    """
    doc = _load_ledger(ledger)
    path = Path(ledger or DEFAULT_LEDGER)
    raw = doc.get("planned")
    if raw is None:
        raise PreserveError(
            "plan", "보존 원장에 `planned:` 계획 index 가 없다 — 실행 전 gate 의 "
                    "근거가 없으므로 새 다리를 돌리지 않는다 (계약 §13.4)")
    if not isinstance(raw, list) or not raw:
        raise PreserveError("plan", f"`planned:` 이 비어 있지 않은 목록이 아니다: {raw!r}")

    # ★ 47차 — cohort record 를 **publisher 와 같은 규칙**으로 본다. 46차의
    #   계획 parser 는 cohort 목록을 따로 약하게 읽어서 저장소 **밖** `dir` 을
    #   가진 cohort 와 enum 밖 `status` 를 승인했다. 같은 원장을 두 parser 가
    #   다르게 읽으면 어느 쪽이 authority 인지 정할 수 없다.
    cohorts = {}
    dirs = {}
    for c in (doc.get("cohorts") or []):
        cid = c.get("cohort_id")
        if not _nonempty_str(cid if isinstance(cid, str) else ""):
            raise PreserveError("plan", f"cohort_id 가 문자열이 아니다: {cid!r}")
        if cid in cohorts:
            raise PreserveError("plan", f"cohort_id 가 중복이다: {cid!r}")
        st = c.get("status")
        if st not in COHORT_STATUS:
            raise PreserveError(
                "plan", f"cohort {cid!r} 의 status 가 계약 enum 이 아니다: "
                        f"{st!r} — {list(COHORT_STATUS)} 중 하나여야 한다")
        resolved = _cohort_dir_of(c, path)
        if resolved in dirs:
            raise PreserveError(
                "plan", f"cohort {cid!r} 과 {dirs[resolved]!r} 이 같은 "
                        f"디렉터리를 선언한다: {resolved}")
        dirs[resolved] = cid
        cohorts[cid] = c

    out: dict = {}
    for e in raw:
        # ★ 48차 P0-5 — 승인 종류마다 닫힌 schema 가 다르다. prospective 는
        #   `run_spec:` 을 담아야 하고 retrospective 는 담을 수 없다.
        kinds = {"retrospective": PLANNED_KEYS,
                 "prospective": PLANNED_KEYS_PROSPECTIVE}
        want_keys = kinds.get(
            e.get("authorization_kind") if isinstance(e, dict) else None)
        if want_keys is None:
            raise PreserveError(
                "plan", f"계획 항목의 `authorization_kind` 가 계약 enum 이 "
                        f"아니다: {(e.get('authorization_kind') if isinstance(e, dict) else e)!r}"
                        f" — {list(AUTHORIZATION_KIND)} 중 하나여야 한다")
        if set(e) != set(want_keys):
            raise PreserveError(
                "plan",
                f"계획 항목이 닫힌 schema 가 아니다: "
                f"{sorted(e) if isinstance(e, dict) else e!r} — "
                f"{e.get('authorization_kind')} 항목은 {sorted(want_keys)} 를 "
                "정확히 담아야 한다")
        for k in PLANNED_KEYS:
            if not _nonempty_str(e[k] if isinstance(e[k], str) else ""):
                raise PreserveError(
                    "plan", f"계획 항목의 `{k}` 가 비어 있지 않은 문자열이 "
                            f"아니다: {e[k]!r}")
        if e["status"] not in PLANNED_STATUS:
            raise PreserveError(
                "plan", f"계획 항목의 `status` 가 계약 enum 이 아니다: "
                        f"{e['status']!r} — {list(PLANNED_STATUS)} 중 하나여야 한다")
        if e["leg_id"] in out:
            raise PreserveError(
                "plan", f"계획 index 에 같은 다리가 두 번 있다: {e['leg_id']!r} — "
                        "어느 항목이 승인인지 정할 수 없다")
        if e["cohort_id"] not in cohorts:
            raise PreserveError(
                "plan", f"계획 항목 {e['leg_id']!r} 이 원장에 없는 cohort 를 "
                        f"가리킨다: {e['cohort_id']!r}")
        if e["authorization_kind"] not in AUTHORIZATION_KIND:
            raise PreserveError(
                "plan", f"계획 항목 {e['leg_id']!r} 의 `authorization_kind` 가 "
                        f"계약 enum 이 아니다: {e['authorization_kind']!r} — "
                        f"{list(AUTHORIZATION_KIND)} 중 하나여야 한다")
        if e["authorization_kind"] == "retrospective":
            if e["status"] != "executed":
                raise PreserveError(
                    "plan", f"소급 항목 {e['leg_id']!r} 의 status 가 executed 가 "
                            f"아니다: {e['status']!r} — 소급은 이미 돌아간 것의 "
                            "기록이다")
            if e["run_spec_digest"] != RETROSPECTIVE_SPEC:
                raise PreserveError(
                    "plan", f"소급 항목 {e['leg_id']!r} 의 `run_spec_digest` 는 "
                            f"{RETROSPECTIVE_SPEC!r} 여야 한다 — 그때는 봉인된 "
                            "계획이 없었고, 없는 것을 있는 척하지 않는다")
        else:
            if len(e["run_spec_digest"]) != 64 or \
                    any(c not in "0123456789abcdef" for c in e["run_spec_digest"]):
                raise PreserveError(
                    "plan", f"계획 항목 {e['leg_id']!r} 의 `run_spec_digest` 가 "
                            f"64자리 hex 가 아니다: {e['run_spec_digest']!r}")
            # ★ 48차 P0-5 — 선언한 spec 과 그 주소가 **서로 맞아야** 한다.
            #   안 맞으면 원장에 적힌 계획과 gate 가 대조하는 것이 다른 것이다.
            spec = e["run_spec"]
            if not isinstance(spec, dict):
                raise PreserveError(
                    "plan", f"계획 항목 {e['leg_id']!r} 의 `run_spec` 이 mapping 이 "
                            f"아니다: {type(spec).__name__}")
            got = run_spec_digest(spec)
            if got != e["run_spec_digest"]:
                raise PreserveError(
                    "plan",
                    f"계획 항목 {e['leg_id']!r} 의 `run_spec_digest` 가 선언한 "
                    f"`run_spec` 의 주소가 아니다 ({e['run_spec_digest'][:16]} ≠ "
                    f"{got[:16]}) — 승인 문서와 승인 주소가 다르다")
            if spec.get("leg_id") != e["leg_id"]:
                raise PreserveError(
                    "plan", f"계획 항목 {e['leg_id']!r} 의 `run_spec.leg_id` 가 "
                            f"다르다: {spec.get('leg_id')!r}")
        # ★ 47차 P0-1 — **계획 roster 와 실행 roster 를 분리한다.** 46차는
        #   실행 roster 하나뿐이라, 계획된 leg 를 어디에 두든 gate·lint·
        #   publisher 중 하나가 반드시 깨졌다 (리뷰어의 4행 표). 계획 중인
        #   leg 는 `prospective_legs` 에, 끝난 leg 는 `legs` 에 있는다.
        coh = cohorts[e["cohort_id"]]
        want = "prospective_legs" if e["status"] in ("planned", "running") \
            else "legs"
        roster = coh.get(want) or []
        if not isinstance(roster, list) or e["leg_id"] not in roster:
            raise PreserveError(
                "plan",
                f"계획 항목 {e['leg_id']!r}(status={e['status']}) 이 cohort "
                f"{e['cohort_id']!r} 의 `{want}` 에 없다: {roster!r} — 계획 "
                "roster 와 실행 roster 는 분리돼 있고 둘 다 원장이 정본이다")
        out[e["leg_id"]] = dict(e, _cohort=coh)
    return out


def assert_planned_leg(leg_id: str, source_digest: str, ledger=None,
                       allow: tuple = ("planned",)) -> dict:
    """이 다리를 **지금 이 코드로** 돌려도 되는가 — 비싼 실행 앞의 gate.

    ★ 48차 P0-6 — `allow` 는 **어느 계획 상태를 승인으로 볼 것인가** 다.
      새 claim 은 `planned` 만 (`running` 이면 이미 누가 돌고 있다), 재개는
      `running` 도 (자기가 그 상태로 옮겨 놓았으니까). 기본값은 좁은 쪽이다.
    """
    idx = planned_index(ledger)
    e = idx.get(leg_id)
    if e is None:
        raise PreserveError(
            "plan",
            f"계획 index 에 없는 다리다: {leg_id!r} — 실행 전에 "
            "`LEG_PRESERVATION.yaml` 의 `planned:` 에 사람이 적어야 한다 "
            f"(현재 계획: {sorted(idx)})")
    if e["status"] not in allow:
        raise PreserveError(
            "plan",
            f"{leg_id!r} 의 계획 상태가 {e['status']!r} 이라 승인이 아니다 "
            f"(허용 {list(allow)}) — 실행 기록은 다음 실행의 승인이 아니고, "
            "이미 running 인 다리를 새로 시작할 수도 없다. 다시 돌리려면 새 "
            "계획 항목을 적어라")
    coh = e["_cohort"]
    if coh.get("status") != "active":
        raise PreserveError(
            "plan",
            f"{leg_id!r} 의 cohort {e['cohort_id']!r} 가 active 가 아니다 "
            f"({coh.get('status')!r}) — frozen cohort 에 새 다리를 더할 수 없다")
    if e["authorized_source_digest"] != source_digest:
        raise PreserveError(
            "plan",
            f"{leg_id!r} 의 승인 code identity 가 지금과 다르다 "
            f"(승인 source_digest {e['authorized_source_digest']} ≠ 현재 "
            f"{source_digest}) — 승인 이후 RUN_SCOPE 가 바뀌었다. 사람이 다시 "
            "승인해야 한다")
    return e


#: 한 다리의 승인 spec — **결과를 바꾸는 축만** 담는다 (48차 P0-5).
#:
#:   47차 grid gate 의 spec 은 `{leg_id, mode, dry_run, config_digest}` 넷뿐이라
#:   `--lli`·`--lam-pe`·`--noise`(=조건 집합)와 `--out`(=결과가 놓일 자리)을
#:   승인 뒤에 통째로 갈아도 같은 digest 가 나왔다. 그러면 승인한 것은 실행이
#:   아니라 다리 **이름**이다.
#:
#:   반대로 `nproc`·`chunk_size`·`resume` 은 **넣지 않는다.** 결과를 바꾸지
#:   않고(서명 검사가 resume 혼합을 따로 막는다), 넣으면 grid 와 fit 이 서로
#:   다른 spec 을 만들어 **하나의 claim 아래 두 phase 를 묶을 수 없게** 된다.
LEG_SPEC_GRID_KEYS = ("config_digest", "condition_ids_sha256",
                      "n_conditions", "out")
LEG_SPEC_FIT_KEYS = ("config_digest", "objectives", "out")


def leg_run_spec(leg_id: str, grid: dict, fit: dict) -> dict:
    """한 다리 **전체**의 승인 spec — 두 phase 가 같은 값을 만든다 (48차 P0-5).

    `claim_planned_leg()` 은 `run_spec_digest` 로 승인을 내용 주소화한다. 그
    주소가 phase 마다 다르면 grid 와 fit 은 서로 다른 claim 을 갖게 되고, 그러면
    "이 다리 하나가 승인 아래 돌았다" 를 말할 수 없다. 그래서 spec 은 **다리
    단위**이고 각 phase 는 자기 몫을 채운 뒤 나머지는 계획에서 읽어 온다.

    key 집합은 **닫혀 있다** — 새 CLI 축이 생기면 여기 적히거나 거부되거나
    둘 중 하나다. 열려 있으면 축이 조용히 승인 밖으로 나간다.
    """
    check_id(leg_id)
    for name, got, want in (("grid", grid, LEG_SPEC_GRID_KEYS),
                            ("fit", fit, LEG_SPEC_FIT_KEYS)):
        if not isinstance(got, dict) or set(got) != set(want):
            raise PreserveError(
                "plan",
                f"leg run spec 의 {name} 축이 계약과 다르다 — 있어야 {sorted(want)}, "
                f"받은 것 {sorted(got) if isinstance(got, dict) else type(got).__name__}")
    spec = {"leg_spec_version": 1, "leg_id": leg_id,
            "grid": {k: grid[k] for k in LEG_SPEC_GRID_KEYS},
            "fit": {k: fit[k] for k in LEG_SPEC_FIT_KEYS}}
    _assert_json_domain(spec, "leg_run_spec")
    return spec


def declared_leg_run_spec(leg_id: str, ledger=None) -> dict:
    """계획이 **선언한** spec 을 읽는다 (48차 P0-5).

    한 phase 는 자기 축만 안다 — grid 는 fit config 를, fit 은 조건 집합을
    모른다. 그래서 각자 자기 몫을 살아 있는 입력에서 만들고 나머지는 여기서
    읽는다. 살아 있는 몫이 선언과 다르면 digest 가 달라져 claim 이 거부한다.
    """
    idx = planned_index(ledger)
    e = idx.get(leg_id)
    if e is None:
        raise PreserveError(
            "plan", f"계획 index 에 없는 다리다: {leg_id!r} (현재 계획: {sorted(idx)})")
    spec = e.get("run_spec")
    if not isinstance(spec, dict):
        raise PreserveError(
            "plan",
            f"{leg_id!r} 의 계획에 `run_spec:` 이 없다 — 승인은 이름이 아니라 "
            "**무엇을 실행할지**를 담아야 한다 (48차 P0-5)")
    return spec


def run_spec_digest(run_spec: dict) -> str:
    """실행 계획의 **내용 주소** (47차 P0-2).

    46차 planned row 는 leg·cohort·source digest 만 담았다. 그래서 같은 이름이
    `--objective A --n-restarts 1` 과 `--objective B --n-restarts 999` 를
    똑같이 승인했다 — allowlist 였지 계획이 아니었다.
    """
    _assert_json_domain(run_spec, "run_spec")
    body = json.dumps(run_spec, sort_keys=True, ensure_ascii=False,
                      allow_nan=False, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def _assert_json_domain(node, where: str) -> None:
    """canonicalizer 가 접을 수 있는 값을 거부한다 (publisher seal 과 같은 규칙)."""
    t = type(node)
    if t is float:
        if node != node or node in (float("inf"), float("-inf")):
            raise PreserveError("plan", f"{where} 에 유한하지 않은 수가 있다")
        return
    if t in (str, int, bool, type(None)):
        return
    if t is dict:
        for k, v in node.items():
            if type(k) is not str:
                raise PreserveError(
                    "plan", f"{where} 의 key 가 문자열이 아니다: {type(k).__name__}")
            _assert_json_domain(v, f"{where}.{k}")
        return
    if t is list:
        for i, v in enumerate(node):
            _assert_json_domain(v, f"{where}[{i}]")
        return
    raise PreserveError(
        "plan", f"{where} 의 값 타입이 봉인 가능하지 않다: {type(node).__name__}")


class LegClaim:
    """살아 있는 실행 권한 하나 — **원자적으로** 하나만 존재한다 (47차 P0-2)."""

    __slots__ = ("leg_id", "cohort_id", "attempt_id", "run_spec_digest",
                 "source_digest", "path", "_token")

    def __init__(self, leg_id, cohort_id, attempt_id, run_spec_digest,
                 source_digest, path, token: str | None = None):
        self.leg_id = leg_id
        self.cohort_id = cohort_id
        #: **공개** 실행 식별자. 원장·로그·진단에 그대로 적어도 된다.
        self.attempt_id = attempt_id
        self.run_spec_digest = run_spec_digest
        self.source_digest = source_digest
        self.path = Path(path)
        #: 비밀 소유 증명. 메모리에만 있고 claim 파일에는 verifier 만 남는다.
        self._token = token

    @property
    def readonly(self) -> bool:
        """소유 증명 없이 열린 claim — 진단용 읽기만 가능하다 (48차 P0-3)."""
        return self._token is None

    @property
    def token(self) -> str:
        """★ 49차 P0-3 — 소유 증명을 **가진 실행만** 꺼낼 수 있다.

        진단용으로 연 claim 에서 이 속성을 읽으면 거부한다. 48차는 readonly
        claim 의 `.attempt` 에 평문 credential 이 그대로 실려 있었다 — 쓰기를
        막아도 credential 을 내주면 그 다음 호출에서 쓰기가 열린다.
        """
        if self._token is None:
            raise PreserveError(
                "plan", f"{self.leg_id!r} 의 claim 을 소유 증명 없이 열었다 — "
                        "진단용 읽기에는 재개 credential 이 없다")
        return self._token

    def _read(self) -> dict:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def phases_done(self) -> tuple:
        rec = self._read()
        return tuple(p for p in CLAIM_PHASES if p in (rec.get("phases") or {}))

    def phase_done(self, phase: str, receipt: dict) -> None:
        """한 phase 를 **durable 하게** 닫는다. 중단 뒤 재개가 여기서 이어진다."""
        if self._token is None:
            raise PreserveError(
                "plan", f"{self.leg_id!r} 의 claim 을 소유 증명 없이 열었다 — "
                        "phase 를 기록할 수 없다 (진단용 읽기다)")
        if phase not in CLAIM_PHASES:
            raise PreserveError(
                "plan", f"모르는 phase: {phase!r} — {list(CLAIM_PHASES)} 중 하나")
        _assert_json_domain(receipt, f"phase[{phase}]")
        # ★ 48차 P0-6 — read-modify-write 를 **임계 구역** 안에서 한다. 47차는
        #   `grid` 와 `fit` 을 동시에 닫으면 둘 다 `phases` 가 빈 record 를 읽고
        #   각자 자기 것만 담아 덮어써서 하나가 사라졌다 (실측). 그러면
        #   `finalize_leg()` 이 "phase 가 남았다" 며 거부하고, 이미 끝난 10시간
        #   계산을 다시 돌리게 된다.
        with _ledger_lock(self.path):
            rec = self._read()
            if rec["attempt_id"] != self.attempt_id:
                raise PreserveError(
                    "plan", f"claim 이 다른 attempt 로 바뀌었다 "
                            f"({rec['attempt_id']} ≠ {self.attempt_id}) — 이 "
                            "실행은 더 이상 권한이 없다")
            rec.setdefault("phases", {})[phase] = {
                "at": dt.datetime.now(dt.timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"),
                "receipt": receipt}
            _atomic_write_json(self.path, rec)


@contextlib.contextmanager
def _ledger_lock(path: Path):
    """원장 전이의 **임계 구역** (48차 P0-6).

    47차 `finalize_leg()` 는 원장을 read-modify-write 했다: `yaml.safe_load` →
    dict 수정 → `write_text` 로 통째 덮어쓰기. 두 다리를 동시에 닫으면 둘 다
    같은 `doc` 을 읽고 각자 자기 항목만 더해 덮으므로 **나중 쓰기가 먼저 쓰기를
    지운다** — 그리고 두 호출 모두 성공을 돌려준다. 실측했다 (M 이 사라졌다).

    원장은 "이 실행이 있었다" 의 유일한 증거이므로 lost update 는 증거 소실이다.
    `flock` 은 같은 기계의 process·thread 사이에서 상호배제를 준다 (네트워크
    파일시스템은 계약 §13.3.1 의 전제 밖이다).
    """
    import fcntl

    lp = Path(path).with_name(Path(path).name + ".lock")
    lp.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lp, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _atomic_write_text(path: Path, text: str) -> None:
    """원장을 **원자적으로** 굳힌다 — 부분 쓰기가 보이지 않게 (48차 P0-6)."""
    path = Path(path)
    tmp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    tmp.write_text(text, encoding="utf-8")
    fd = os.open(tmp, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)
    dfd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)


def _atomic_write_json(path: Path, rec: dict) -> None:
    tmp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    tmp.write_text(json.dumps(rec, sort_keys=True, ensure_ascii=False,
                              separators=(",", ":")) + "\n", encoding="utf-8")
    fd = os.open(tmp, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)
    dfd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)


DEFAULT_CLAIMS_ROOT = (Path(__file__).resolve().parents[1] / "results" / "_claims")


def _claim_path(leg_id: str, claims_root=None) -> Path:
    """★ 48차 P0-6 — ID 도메인은 **한 곳**이다.

    47차는 `"/" in leg_id` 만 봤다. Windows separator(`..\\..\\outside`)·device
    이름(`nul`)·길이는 다 통과했다. 이 저장소는 27차 P1-4 에 정확히 그 반례로
    `check_id()` 를 만들었는데 claim 경로만 따로 약하게 검사하고 있었다 — 같은
    도메인을 두 곳에서 다르게 정하면 **약한 쪽이 실효 규칙**이다.
    """
    check_id(leg_id)
    return Path(claims_root or DEFAULT_CLAIMS_ROOT) / f"{leg_id}.claim"


def _mark_plan_running(leg_id: str, ledger=None) -> None:
    """계획을 `planned → running` 으로 옮긴다 (48차 P0-6).

    47차는 `PLANNED_STATUS` 에 `running` 을 선언만 해 두고 **어떤 코드도 그
    값을 쓰지 않았다.** 그래서 원장만 보고 "지금 도는 다리가 있는가" 를 답할 수
    없었고, claim 파일이 사라진 crash 뒤에 계획은 여전히 `planned` 이라 다른
    실행이 태연히 새 claim 을 땄다. 선언만 있고 전이가 없으면 상태 기계가 아니다.
    """
    import yaml

    path = Path(ledger or DEFAULT_LEDGER)
    with _ledger_lock(path):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        row = next((e for e in doc.get("planned") or []
                    if e.get("leg_id") == leg_id), None)
        if row is None:
            raise PreserveError("plan", f"계획 index 에 {leg_id!r} 이 없다")
        if row.get("status") != "planned":
            raise PreserveError(
                "plan", f"{leg_id!r} 의 계획 상태가 {row.get('status')!r} 이라 "
                        "running 으로 옮길 수 없다")
        row["status"] = "running"
        _atomic_write_text(path, yaml.safe_dump(doc, allow_unicode=True,
                                                sort_keys=False))


def claim_planned_leg(leg_id: str, run_spec: dict, source_digest: str,
                      ledger=None, claims_root=None) -> LegClaim:
    """실행 권한을 **원자적으로 하나만** 발급한다 (47차 P0-1 · P0-2).

    46차 `assert_planned_leg()` 는 read-only predicate 였다. 같은 row 로 몇
    번이고 통과했고 동시 실행 둘도 모두 계산에 들어갔다. 승인은 상태 전이여야
    한다.

    검사 순서 — **전체 원장 일관성이 먼저다.** 46차는 target predicate 만
    봤으므로 다른 leg 때문에 원장이 깨져 있어도 이 leg 의 계산이 시작됐다.
    """
    assert_planned_index_consistent(ledger)          # 전체가 먼저
    e = assert_planned_leg(leg_id, source_digest, ledger=ledger)
    # ★ 47차 — "소급은 승인이 아니다" 를 여기서 **다시 검사하지 않는다.**
    #   `planned_index()` 가 이미 `retrospective ⇒ status == executed` 를
    #   강제하고 `assert_planned_leg()` 는 `status == planned` 만 통과시키므로,
    #   claim 에 도달하는 retrospective 항목은 **표현할 수 없다.** 변이로
    #   확인했다: 여기 검사를 지워도 아무 시험이 빨개지지 않았다 — 중복이라는
    #   뜻이다 (도달 불가능한 검사는 방어가 아니라 소음이다).

    want = run_spec_digest(run_spec)
    if e["run_spec_digest"] != want:
        raise PreserveError(
            "plan",
            f"{leg_id!r} 의 run_spec 이 승인된 계획과 다르다 "
            f"(계획 {e['run_spec_digest'][:16]} ≠ 지금 {want[:16]}) — 계획은 "
            "이름이 아니라 **무엇을 실행할지**를 승인한다")

    path = _claim_path(leg_id, claims_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    attempt_id = uuid.uuid4().hex
    token = _new_token()
    rec = {"leg_id": leg_id, "cohort_id": e["cohort_id"],
           "attempt_id": attempt_id, "attempt_verifier": _token_verifier(token),
           "run_spec_digest": want, "source_digest": source_digest,
           "opened_at": dt.datetime.now(dt.timezone.utc).strftime(
               "%Y-%m-%dT%H:%M:%SZ"),
           "phases": {}}
    body = json.dumps(rec, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")) + "\n"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError as exc:
        raise PreserveError(
            "plan",
            f"{leg_id!r} 의 claim 이 이미 열려 있다: {path} — 같은 다리를 두 번 "
            "시작할 수 없다. 중단된 실행이면 `resume_claim()` 으로 이어라") from exc
    try:
        os.write(fd, body.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    dfd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    # ★ 48차 P0-6 — claim 파일을 굳힌 **뒤** 계획을 running 으로 옮긴다.
    #   순서가 중요하다: 파일이 먼저여야 `O_EXCL` 이 상호배제의 authority 로
    #   남는다. 원장 전이가 실패하면 claim 을 되돌린다 — 잡아만 놓고 원장에는
    #   안 보이는 다리를 남기지 않는다.
    try:
        _mark_plan_running(leg_id, ledger=ledger)
    except BaseException:
        path.unlink(missing_ok=True)
        raise
    return LegClaim(leg_id, e["cohort_id"], attempt_id, want, source_digest,
                    path, token=token)


def _read_claim_record(leg_id: str, claims_root=None) -> tuple[Path, dict]:
    path = _claim_path(leg_id, claims_root)
    if not path.is_file():
        raise PreserveError("plan", f"이어받을 claim 이 없다: {path}")
    rec = json.loads(path.read_text(encoding="utf-8"))
    if set(rec) != set(CLAIM_KEYS):
        raise PreserveError(
            "plan", f"claim schema 가 계약과 다르다: {sorted(rec)}")
    return path, rec


def resume_claim(leg_id: str, claims_root=None, token: str | None = None,
                 ledger=None) -> LegClaim:
    """중단된 실행을 **같은 attempt 로** 이어받는다 (재계산 없이 finalize).

    ★ 48차 P0-3 — `token` 은 **소유 증명**이다. 47차는 claim 파일이 보이면
      누구든 이어받을 수 있었고, public gate 가 그것을 자동으로 했다. 그래서
      같은 public 호출 둘이 모두 같은 attempt 로 compute 에 들어갔다 —
      `O_EXCL` 은 파일 최초 생성만 배타적이었지 **실행권**은 배타적이지
      않았다. 이름과 spec 만으로 이어받을 수 있으면 그것은 재개가 아니라
      두 번째 발급이다.

    ★ 49차 P0-3 — 대조는 claim 파일에 적힌 평문이 아니라 `sha256` verifier 와
      한다. 48차는 credential 을 그 파일 안에 그대로 뒀으므로, 파일을 읽을 수
      있는 주체에게는 "소유 증명" 이 아무 것도 요구하지 않는 것과 같았다.

      `token=None` 은 **진단용 읽기**이며 phase 를 쓸 수 없고 credential 도
      들고 있지 않은 claim 을 돌려준다.
    """
    path, rec = _read_claim_record(leg_id, claims_root)
    if token is not None:
        if not secrets.compare_digest(_token_verifier(token),
                                      str(rec["attempt_verifier"])):
            raise PreserveError(
                "plan",
                f"{leg_id!r} 의 claim 소유 증명이 맞지 않는다 — 이 실행은 그 "
                "attempt 를 갖고 있지 않다. 다른 실행이 이미 이 다리를 잡고 있다")
        # ★ 48차 — 재개할 때마다 **살아 있는 원장 authority** 를 다시 본다.
        #   47차 existing-claim 분기는 원장을 읽지 않아, claim 뒤 계획에서 L 을
        #   지우거나 cohort 를 frozen 으로 바꿔도 계속 승인됐다.
        e = assert_planned_leg(rec["leg_id"], rec["source_digest"],
                               ledger=ledger, allow=("planned", "running"))
        if e["cohort_id"] != rec["cohort_id"]:
            raise PreserveError(
                "plan", f"{leg_id!r} 의 cohort 가 claim 이후 바뀌었다 "
                        f"({rec['cohort_id']} → {e['cohort_id']})")
        if e["run_spec_digest"] != rec["run_spec_digest"]:
            raise PreserveError(
                "plan", f"{leg_id!r} 의 승인된 run_spec 이 claim 이후 바뀌었다")
    return LegClaim(rec["leg_id"], rec["cohort_id"], rec["attempt_id"],
                    rec["run_spec_digest"], rec["source_digest"], path,
                    token=token)


# ─────────────────────────────────────────────────────────────────────────────
# 49차 P0-3 — 실행권을 **process 경계 너머로** 넘기는 coordinator
#
# 48차의 두 규칙은 각각 옳았지만 함께 두면 production 을 막았다: claim 을 따면
# 계획이 `running` 으로 가고(P0-6), claim 이 있으면 소유 증명 없이는 못 이어받는다
# (P0-3). 그런데 grid 가 딴 실행권을 fit 에 **넘길 경로가 없었다.** 그래서
# `run.sh --mode all --leg L` 은 grid 직후 반드시 거부됐다 (리뷰어 실측).
#
# 규칙 둘 사이에 있어야 하는 것은 예외가 아니라 **전달**이다. 한 coordinator 가
# 한 번 발급하고, 소유 증명을 0600 파일로 넘기고, 각 phase process 가 그 파일로
# 같은 실행에 붙고, 마지막에 같은 증명으로 닫는다.
# ─────────────────────────────────────────────────────────────────────────────

#: 소유 증명의 길이 (hex 문자 수). 128bit.
TOKEN_HEX = 32

_TOKEN_RE = re.compile(r"^[0-9a-f]{%d}$" % TOKEN_HEX)


def _new_token() -> str:
    """추측 불가능한 소유 증명. `uuid4().hex` 가 아니라 CSPRNG 를 쓴다."""
    return secrets.token_hex(TOKEN_HEX // 2)


def _token_verifier(token: str) -> str:
    return hashlib.sha256(str(token).encode("utf-8")).hexdigest()


def write_token_file(path, token: str) -> Path:
    """소유 증명을 **소유자만 읽을 수 있게** 굳힌다 (0600).

    argv 로 넘기지 않는다 — `ps` 와 `/proc/<pid>/cmdline` 은 같은 기계의 다른
    주체에게 열려 있다. 넘기는 것은 **경로**이고 내용은 파일 권한이 지킨다.
    한계: 같은 uid 의 다른 process 는 읽을 수 있다 (계약 §13.3.1 의 전제와
    같은 경계다 — flock 도 같은 기계·같은 주체를 가정한다).
    """
    if not _TOKEN_RE.match(str(token)):
        raise PreserveError("plan", "소유 증명의 형식이 계약과 다르다")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(f".{p.name}.{uuid.uuid4().hex}.tmp")
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.write(fd, (str(token) + "\n").encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, p)
    dfd = os.open(p.parent, os.O_RDONLY)
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)
    return p


def read_token_file(path) -> str:
    p = Path(path)
    if not p.is_file():
        raise PreserveError("plan", f"소유 증명 파일이 없다: {p}")
    tok = p.read_text(encoding="utf-8").strip()
    if not _TOKEN_RE.match(tok):
        raise PreserveError(
            "plan", f"소유 증명 파일의 형식이 계약과 다르다: {p}")
    return tok


def open_leg_run(leg_id: str, run_spec: dict, source_digest: str, token_file,
                 ledger=None, claims_root=None) -> LegClaim:
    """coordinator 가 실행권을 **한 번** 발급하고 소유 증명을 파일로 내놓는다.

    발급 자체는 `claim_planned_leg()` 이다 — 계획 대조·원자적 `O_EXCL`·원장
    `running` 전이가 전부 거기 있다. 여기서 더하는 것은 **전달 경로** 하나다.
    """
    claim = claim_planned_leg(leg_id, run_spec, source_digest, ledger=ledger,
                              claims_root=claims_root)
    try:
        write_token_file(token_file, claim.token)
    except BaseException:
        # 넘길 수 없는 실행권은 잡아 둘 이유가 없다 — 되돌린다. 그러지 않으면
        # 계획이 `running` 인 채 아무도 못 이어받는 상태로 굳는다.
        _abandon_claim(claim, ledger=ledger)
        raise
    return claim


def attach_leg_run(leg_id: str, token_file, ledger=None,
                   claims_root=None) -> LegClaim:
    """넘겨받은 소유 증명으로 **같은 실행**에 붙는다 (phase process 가 쓴다)."""
    return resume_claim(leg_id, claims_root=claims_root,
                        token=read_token_file(token_file), ledger=ledger)


def inspect_leg_run(leg_id: str, claims_root=None) -> dict:
    """살아 있는 실행을 **공개 필드만으로** 들여다본다 (진단용).

    ★ 49차 P0-3 — verifier 도 credential 도 내보내지 않는다. 48차 진단 경로는
      readonly claim 객체를 그대로 돌려줬고 그 객체의 `.attempt` 가 평문
      credential 이었다.
    """
    _, rec = _read_claim_record(leg_id, claims_root)
    return {"leg_id": rec["leg_id"], "cohort_id": rec["cohort_id"],
            "attempt_id": rec["attempt_id"],
            "run_spec_digest": rec["run_spec_digest"],
            "source_digest": rec["source_digest"],
            "opened_at": rec["opened_at"],
            "phases_done": sorted(p for p in CLAIM_PHASES
                                  if p in (rec.get("phases") or {}))}


def release_leg_run(leg_id: str, token=None, token_file=None, ledger=None,
                    claims_root=None) -> dict:
    """실행권을 **되돌린다** — 계획을 `planned` 로 돌리고 claim 을 지운다.

    ★ 49차 P0-3 — 48차에는 이 방향이 없었다. `--dry-run` 은 claim 을 따고
      계획을 `running` 으로 옮긴 뒤 아무 phase 도 닫지 않고 끝난다. finalize 는
      "phase 가 남았다" 며 거부하므로 그 다리는 **다시 시작할 수도 닫을 수도
      없는** terminal 상태로 굳었다. 47차가 dry-run 면제를 없앤 것은 옳았고
      (dry-run 도 solver 를 부른다), 그 대가는 면제가 아니라 되돌림이다.

      crash 로 남은 claim 을 사람이 정리하는 통로이기도 하다. 소유 증명을
      요구하므로 남의 실행을 취소할 수는 없다.
    """
    if (token is None) == (token_file is None):
        raise TypeError(
            "release_leg_run() 는 `token` 또는 `token_file` 중 정확히 하나를 "
            "요구한다 — 소유 증명 없이 남의 실행권을 취소할 수 없다")
    if token is None:
        token = read_token_file(token_file)
    claim = resume_claim(leg_id, claims_root, token=token, ledger=ledger)
    _abandon_claim(claim, ledger=ledger)
    if token_file is not None:
        Path(token_file).unlink(missing_ok=True)
    return {"leg_id": leg_id, "attempt_id": claim.attempt_id,
            "status": "planned"}


def _abandon_claim(claim: LegClaim, ledger=None) -> None:
    """발급을 되돌린다 — claim 파일을 지우고 계획을 `planned` 로 돌린다."""
    import yaml

    claim.path.unlink(missing_ok=True)
    path = Path(ledger or DEFAULT_LEDGER)
    with _ledger_lock(path):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        row = next((e for e in doc.get("planned") or []
                    if e.get("leg_id") == claim.leg_id), None)
        if row is not None and row.get("status") == "running":
            row["status"] = "planned"
            _atomic_write_text(path, yaml.safe_dump(doc, allow_unicode=True,
                                                    sort_keys=False))


def precheck_leg_run(leg_id: str, source_digest: str, token_file=None,
                     ledger=None, claims_root=None) -> dict:
    """실행 **전** 사전 점검 — 새 발급인가, 내가 가진 재개인가 (49차 P0-3).

    48차 `run.sh` 사전검사는 `assert_planned_leg()` 만 불렀고 그것은 `planned`
    만 통과시켰다. 그래서 grid 가 계획을 `running` 으로 옮긴 뒤 **같은
    pipeline 의** fit 사전검사가 자기 자신 때문에 거부됐다. 사전검사가 두
    경우를 구분하지 못하면 사전검사가 곧 pipeline 을 막는 장치가 된다.

    아무 것도 바꾸지 않는다 — 발급은 실제 계산 직전
    (`assert_run_is_authorized()`)에서만 일어난다.
    """
    path = _claim_path(leg_id, claims_root)
    if path.is_file():
        if token_file is None:
            raise PreserveError(
                "plan",
                f"{leg_id!r} 은 이미 실행 중이다 (claim: {path}) — 두 번째 "
                "실행을 시작할 수 없다. 중단된 실행을 이으려면 그 실행의 "
                "소유 증명 파일을 주라")
        claim = resume_claim(leg_id, claims_root=claims_root,
                             token=read_token_file(token_file), ledger=ledger)
        if claim.source_digest != source_digest:
            raise PreserveError(
                "plan",
                f"{leg_id!r} 의 claim 이 다른 code identity 로 열렸다 "
                f"({claim.source_digest} ≠ {source_digest}) — 실행 도중 "
                "RUN_SCOPE 가 바뀌었다")
        return {"kind": "resume", "leg_id": leg_id,
                "cohort_id": claim.cohort_id, "attempt_id": claim.attempt_id,
                "phases_done": list(claim.phases_done())}
    e = assert_planned_leg(leg_id, source_digest, ledger=ledger)
    return {"kind": "new", "leg_id": leg_id, "cohort_id": e["cohort_id"],
            "recorded_on": e["recorded_on"], "phases_done": []}


#: 실행 기록의 보존 상태. **검증한 만큼만** 적는다 (48차 P0-4).
#:
#:   full_bundle          — clone 한 사람이 검증할 수 있는 묶음이 **실재한다**.
#:                          `_verify_declared_bundle()` 이 디스크에서 확인한
#:                          경우에만 붙는다.
#:   recorded_projection  — 투영·요약은 남았고 원자료 묶음은 없다.
#:   preservation_pending — 계산은 끝났고 보존 묶음을 **아직 만들지 않았다.**
#:   missing              — 원자료가 있었는데 잃었다.
#:
#: ★ 49차 P0-4 — 48차의 `no_bundle` 은 계약 §8 축 enum 에 **없는 값**이었다.
#:   즉 production `finalize_leg()` 이 원장에 쓰는 값을 이 저장소 자신의
#:   lint(`test_registry_rejects_impossible_status_tuples`)가 거부한다. 어휘의
#:   정본은 계약 하나이고, runtime 은 그 부분집합이어야 한다
#:   (`test_the_runtime_preservation_enum_is_inside_the_contract`).
PRESERVATION_STATUS = ("full_bundle", "recorded_projection",
                       "preservation_pending", "missing")

#: 아직 묶지 않은 다리의 나머지 두 축. **바닥값**이며 올리는 것은 사람이
#: 증거를 보고 한다 (계약 §8 제약이 `canonical` 에 `full_bundle +
#: current_validated` 를 요구하므로 여기서 올릴 방법도 없다).
PENDING_VALIDATION_STATUS = "unvalidated"
PENDING_INFERENCE_ROLE = "diagnostic"

#: 묶음 주장이 담아야 할 필드. 하나라도 있으면 **전부** 있어야 하고, 전부
#: 디스크에서 다시 계산해 맞아야 한다.
BUNDLE_EVIDENCE_KEYS = ("bundle_uri", "bundle_files", "payload_bytes",
                        "payload_index", "payload_index_sha256")


def _verify_declared_bundle(evidence: dict, repo_root=None) -> list:
    """선언한 묶음을 **디스크에서** 확인한다 (48차 P0-4).

    47차 `finalize_leg()` 은 caller 의 dict 를 그대로 옮겨 적고
    `preservation_status: full_bundle` 을 붙였다. 그 상태의 뜻은 "clone 한
    사람이 이 결과를 검증할 수 있는 묶음이 실재한다"(계약 §8)인데 디스크를
    보지 않았다 — 아무 dict 나 주면 원장에 완전 묶음이 생겼다.

    원장은 이 저장소에서 **증거의 정본**이다. 거기에 검증되지 않은 주장을 쓰는
    함수는 증거를 만드는 것이 아니라 증거를 오염시킨다.

    회귀(`test_full_bundle_claims_are_backed_by_a_real_bundle`)가 원장 전체에
    대고 같은 검사를 한다 — 여기서 막지 않으면 그 회귀가 **나중에** 빨개진다.
    """
    root = Path(repo_root or Path(__file__).resolve().parents[1])
    bad: list = []
    present = [k for k in BUNDLE_EVIDENCE_KEYS if k in evidence]
    if not present:
        return bad                       # 묶음을 주장하지 않았다 — 그것도 사실이다
    missing = [k for k in BUNDLE_EVIDENCE_KEYS if k not in evidence]
    if missing:
        return [f"묶음 주장이 불완전하다 — 없는 필드 {missing}"]

    d = root / str(evidence["bundle_uri"])
    if not d.is_dir():
        return [f"묶음 경로가 없다: {evidence['bundle_uri']}"]
    files = sorted(x for x in d.rglob("*") if x.is_file())
    if len(files) != evidence["bundle_files"]:
        bad.append(f"묶음 파일 수 {len(files)} ≠ 선언 {evidence['bundle_files']}")
    nbytes = sum(x.stat().st_size for x in files)
    if nbytes != evidence["payload_bytes"]:
        bad.append(f"묶음 바이트 {nbytes} ≠ 선언 {evidence['payload_bytes']}")
    idx = root / str(evidence["payload_index"])
    if not idx.is_file():
        bad.append(f"payload index 가 없다: {evidence['payload_index']}")
    else:
        got = hashlib.sha256(idx.read_bytes()).hexdigest()
        if got != evidence["payload_index_sha256"]:
            bad.append(f"payload index sha {got[:16]} ≠ 선언 "
                       f"{str(evidence['payload_index_sha256'])[:16]}")
    return bad


def finalize_leg(leg_id: str, evidence: dict, ledger=None,
                 claims_root=None, *, token: str | None = None,
                 token_file=None) -> dict:
    """모든 phase 가 끝난 claim 을 **executed 로 닫는다** (47차 P0-1).

    계획 roster 에서 빼고 실행 roster 와 실행 기록에 넣는다. 이 전이가 없으면
    "실행 전 승인" 은 사람이 나중에 원장 여러 필드를 한꺼번에 고치는 일이 되고,
    그것은 실행 **뒤** authority 선택이지 gate 가 아니다.

    ★ 49차 P0-3 — 소유 증명은 **필수**다. 48차 `attempt` 는 기본값 `None`
      이었고, `resume_claim(None)` 은 readonly claim 을 돌려주는데 finalize 는
      그것으로도 원장을 닫았다 — 즉 다리 **이름만** 알면 남의 실행을 executed
      로 닫을 수 있었다. 원장을 닫는 것은 진단이 아니다.
    """
    import yaml

    if (token is None) == (token_file is None):
        raise TypeError(
            "finalize_leg() 는 `token` 또는 `token_file` 중 정확히 하나를 "
            "요구한다 — 소유 증명 없이 원장을 닫을 수 없다")
    if token is None:
        token = read_token_file(token_file)
    claim = resume_claim(leg_id, claims_root, token=token, ledger=ledger)
    missing = [p for p in CLAIM_PHASES if p not in claim.phases_done()]
    if missing:
        raise PreserveError(
            "plan", f"{leg_id!r} 의 phase 가 남았다: {missing} — 모든 phase 가 "
                    "끝나야 executed 로 닫는다")
    _assert_json_domain(evidence, "evidence")
    # ★ 48차 P0-4 — 묶음 주장을 **디스크에서** 확인한다. 확인 전에는 아무 것도
    #   쓰지 않는다 (거부하면서 기록을 남기면 그것이 곧 오염이다).
    bundle_bad = _verify_declared_bundle(evidence)
    if bundle_bad:
        raise PreserveError(
            "plan",
            f"{leg_id!r} 의 묶음 주장이 실물과 다르다 — 검증되지 않은 보존 "
            "상태를 원장에 쓸 수 없다:\n  " + "\n  ".join(bundle_bad))
    claimed_bundle = all(k in evidence for k in BUNDLE_EVIDENCE_KEYS)
    if not _nonempty_str(evidence.get("leg_source_digest") or ""):
        raise PreserveError(
            "plan", "evidence.leg_source_digest 가 없다 — 실행 기록을 실물에 "
                    "결속할 수 없다")
    if evidence["leg_source_digest"] != claim.source_digest:
        raise PreserveError(
            "plan",
            f"실행 기록의 code identity 가 claim 과 다르다 "
            f"({evidence['leg_source_digest']} ≠ {claim.source_digest})")

    path = Path(ledger or DEFAULT_LEDGER)
    # ★ 48차 P0-6 — 읽기·수정·쓰기 **전체**가 임계 구역 안이다. 밖에서 읽고
    #   안에서 쓰면 읽은 값이 이미 낡았을 수 있으므로 의미가 없다.
    with _ledger_lock(path):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        plan = next((e for e in doc.get("planned") or []
                     if e.get("leg_id") == leg_id), None)
        if plan is None:
            raise PreserveError("plan", f"계획 index 에 {leg_id!r} 이 없다")
        if plan.get("status") not in ("planned", "running"):
            raise PreserveError(
                "plan", f"{leg_id!r} 의 계획 상태가 {plan.get('status')!r} 이라 "
                        "executed 로 닫을 수 없다")
        coh = next((c for c in doc.get("cohorts") or []
                    if c.get("cohort_id") == claim.cohort_id), None)
        if coh is None:
            raise PreserveError("plan", f"원장에 cohort {claim.cohort_id!r} 이 없다")
        if any(e.get("leg_id") == leg_id for e in doc.get("legs") or []):
            raise PreserveError(
                "plan", f"{leg_id!r} 의 실행 기록이 이미 있다 — 같은 다리를 두 번 "
                        "닫을 수 없다")

        plan["status"] = "executed"
        coh["prospective_legs"] = sorted(
            x for x in (coh.get("prospective_legs") or []) if x != leg_id)
        coh["legs"] = sorted(set(coh.get("legs") or []) | {leg_id})
        # ★ 48차 P0-4 — **검증한 만큼만** 적고, lifecycle 이 실제로 남긴
        #   증거(phase receipt)를 기록에 넣는다. 47차는 phase receipt 를 다
        #   버리고 caller 의 주장만 옮겼다 — 그러면 원장에 남는 것은 "누가
        #   그렇다고 했다" 뿐이고 "무엇이 실제로 돌았다" 가 아니다.
        rec_evidence = dict(evidence)
        rec_evidence["phases"] = {
            ph: claim._read()["phases"][ph] for ph in CLAIM_PHASES}
        rec_evidence["attempt_id"] = claim.attempt_id
        rec_evidence["run_spec_digest"] = claim.run_spec_digest
        # ★ 49차 P0-4 — 계약 §8 은 **세 축의 튜플**을 요구한다. 48차는
        #   `preservation_status` 하나만 적고 나머지를 비웠으므로 그 기록은
        #   `test_registry_rejects_impossible_status_tuples` 를 통과할 수
        #   없었다 — production 이 쓴 원장을 자기 lint 가 거부하는 상태였다.
        #   묶음을 확인하지 못한 다리는 `preservation_pending` 이고, 나머지 두
        #   축은 계약 제약이 강제하는 바닥값이다.
        doc.setdefault("legs", []).append(
            {"leg_id": leg_id,
             "preservation_status": "full_bundle" if claimed_bundle
             else "preservation_pending",
             # 묶음을 확인했어도 **검증**은 별개 단계다 (validator 가 복원해
             # 재채점한다). finalize 는 그것을 하지 않았으므로 unvalidated 다.
             "validation_status": PENDING_VALIDATION_STATUS,
             "inference_role": PENDING_INFERENCE_ROLE,
             "evidence": rec_evidence})
        _atomic_write_text(path, yaml.safe_dump(doc, allow_unicode=True,
                                                sort_keys=False))
    claim.path.unlink(missing_ok=True)
    # 실행권이 닫혔으므로 소유 증명도 남길 이유가 없다 — 쓸모를 잃은
    # credential 을 디스크에 두는 것은 그 자체가 노출면이다.
    if token_file is not None:
        Path(token_file).unlink(missing_ok=True)
    return {"leg_id": leg_id, "attempt_id": claim.attempt_id,
            "status": "executed"}


def planned_coverage(ledger=None) -> dict:
    """계획 index 를 **종류별로** 센다 (47차 — 소급을 gate 증거로 세지 않게).

    요청문·계약이 "실행 전 gate 가 몇 번 실제로 작동했는가" 를 인용할 때 이
    함수의 값을 쓴다. 자유문자 근거를 읽고 사람이 세는 대신.
    """
    idx = planned_index(ledger)
    out = {"prospective": 0, "retrospective": 0}
    for e in idx.values():
        out[e["authorization_kind"]] += 1
    out["gate_backed_executions"] = sum(
        1 for e in idx.values()
        if e["authorization_kind"] == "prospective" and e["status"] == "executed")
    return out


def assert_planned_index_consistent(ledger=None) -> bool:
    """실행 기록이 계획 index 를 **덮는가** (반대 방향).

    이것이 없으면 index 는 장식이다: 계획에 없이 돌린 다리가 나중에 `legs:`
    에만 나타나도 아무 검사도 깨지지 않는다 — §13.4 가 신고하던 그 구멍이다.
    """
    idx = planned_index(ledger)
    doc = _load_ledger(ledger)
    executed = []
    for leg in (doc.get("legs") or []):
        lid = (leg or {}).get("leg_id")
        if not _nonempty_str(lid if isinstance(lid, str) else ""):
            raise PreserveError("plan", f"`legs:` 항목의 leg_id 가 없다: {leg!r}")
        executed.append(lid)
    missing = sorted(set(executed) - set(idx))
    if missing:
        raise PreserveError(
            "plan",
            f"실행 기록에만 있고 계획 index 에 없는 다리: {missing} — 계획 없이 "
            "돌렸거나 index 를 안 적었다. 둘 다 실행 전 gate 가 없었다는 뜻이다")
    wrong = sorted(l for l in executed if idx[l]["status"] != "executed")
    if wrong:
        raise PreserveError(
            "plan",
            f"실행 기록이 있는데 계획 상태가 executed 가 아닌 다리: {wrong}")
    # ★ 47차 — **exact equality** 다. 46차는 "실행 기록 ⊆ 계획" 만 봤으므로
    #   실행 기록이 없는 executed 계획 항목(phantom)이 조용히 통과했다.
    phantom = sorted(l for l, e in idx.items()
                     if e["status"] == "executed" and l not in set(executed))
    if phantom:
        raise PreserveError(
            "plan",
            f"executed 로 기록됐는데 실행 기록이 없는 다리: {phantom} — 계획과 "
            "실행 기록은 executed 에 대해 **정확히 같은 집합**이어야 한다")
    # ★ 46차 P0-11 — 계획 항목을 **실물 원장 기록**에 결속한다. 이것이 없으면
    #   `planned:` 는 자기 자신만 참조하는 목록이고, 아무 digest 나 적어도
    #   일관되다. 실행 기록이 있는 다리는 그 다리가 **실제로 돌았던** code
    #   identity 를 계획이 그대로 담아야 한다.
    for leg in (doc.get("legs") or []):
        lid = leg["leg_id"]
        e = idx[lid]
        ev = leg.get("evidence") or {}
        real = ev.get("leg_source_digest")
        if not _nonempty_str(real if isinstance(real, str) else ""):
            raise PreserveError(
                "plan", f"{lid!r} 의 실행 기록에 `evidence.leg_source_digest` 가 "
                        "없다 — 계획을 실물에 결속할 수 없다")
        if e["authorized_source_digest"] != real:
            raise PreserveError(
                "plan",
                f"{lid!r} 의 계획 digest 가 실행 기록과 다르다 "
                f"(계획 {e['authorized_source_digest']} ≠ 기록 {real}) — "
                "계획 index 가 실물을 가리키지 않으면 장식이다")
        coh = ev.get("cohorts") or []
        if isinstance(coh, list) and coh and e["cohort_id"] not in coh:
            raise PreserveError(
                "plan",
                f"{lid!r} 의 계획 cohort {e['cohort_id']!r} 가 실행 기록의 "
                f"cohort {coh} 에 없다")
    return True
