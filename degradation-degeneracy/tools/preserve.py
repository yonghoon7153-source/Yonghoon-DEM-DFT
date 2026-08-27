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

import datetime as dt
import errno
import hashlib
import json
import os
import re
import shutil
import tempfile
import unicodedata
import uuid
from dataclasses import dataclass
from typing import ClassVar
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

    def read_pinned(self, leg_id: str, dg: str) -> bytes:
        """**pin 에서** 읽는다. `objects/` 가 비어도 회수돼야 한다."""
        p = self._pin(leg_id, dg)
        if not p.is_file():
            raise PreserveError("pin", f"pin 이 없다: {dg[:16]}")
        data = p.read_bytes()
        if hashlib.sha256(data).hexdigest() != dg:
            raise PreserveError("pin", f"pin 바이트가 digest 와 다르다: {dg[:16]}")
        return data

    def verify_pins(self, leg_id: str, digests) -> list:
        """pin 집합이 완전하고 **바이트가 맞는지** 확인한다."""
        bad = []
        for dg in sorted(set(digests)):
            try:
                self.read_pinned(leg_id, dg)
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
        lock = self.query_object_lock() or {}
        lease = {
            "schema": RETENTION_SCHEMA,
            "leg_id": leg_id,
            "store_id": self.store_id,
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
        self.lock_content_object(l_obj, until_s)
        return dict(lease, lease_digest=l_obj, lease_version=lv)

    def _existing_lease(self, leg_id: str, objs: list,
                        min_retention_days: int) -> dict | None:
        """이 leg 에 이미 있고 **같은 graph 를 같은 정책으로** 담보하는 lease.

        pin 집합에서 graph object 를 뺀 나머지가 lease 후보다. 여러 개가 남아
        있으면 이미 상태가 오염된 것이므로 `None` 을 돌려 새로 만들지 않고
        아래 검증이 그것을 잡게 둔다.
        """
        extra = sorted(self.pinned(leg_id) - set(objs))
        if len(extra) != 1:
            return None
        try:
            lease = self.read_lease(leg_id, extra[0])
        except (PreserveError, ValueError, UnicodeDecodeError):
            return None
        if lease.get("objects") != objs \
                or lease.get("min_retention_days") != min_retention_days \
                or lease.get("store_id") != self.store_id \
                or lease.get("backend_uri") != self.uri \
                or lease.get("enforcement") != self.probe_enforcement():
            return None
        try:
            # ★ 34차 P0-1 — proof 를 **provider 에서 재발견**해 넘긴다.
            #   초판은 넘기지 않아 object-lock lease 재사용이 언제나 실패했다.
            return self.verify_retention(
                leg_id, extra[0], expected=set(objs),
                lease_version=self.recover_lease_version(leg_id, extra[0]))
        except PreserveError:
            return None       # 만료됐거나 어긋났다 — 새로 만든다

    def read_lease(self, leg_id: str, lease_digest: str) -> dict:
        """lease 를 **pin 에서** 읽는다."""
        lease = load_canonical(self.read_pinned(leg_id, lease_digest))
        if not isinstance(lease, dict):
            raise PreserveError("retention", "lease 가 dict 가 아니다")
        return lease

    def verify_retention(self, leg_id: str, lease_digest: str,
                         expected: set | None = None,
                         lease: dict | None = None,
                         lease_version: str | None = None) -> dict:
        """lease 가 **이 backend 에서 지금** 유효한가.

        읽은 바이트가 아니라 **상태**를 본다 — 그래서 전수 읽기가 끝난 뒤에
        한 번 더 부르면 그 사이의 삭제가 잡힌다 (30차 P0-1 의 마지막 창).
        """
        stage = "retention"
        # `lease` 를 주면 그것을 본다 — 회귀가 lease 축만 변이할 수 있게 한다.
        lease = dict(lease) if lease is not None else self.read_lease(leg_id, lease_digest)
        lease_version = lease_version or lease.pop("lease_version", None)
        lease.pop("lease_digest", None)
        lease.pop("lease_version", None)
        want = {"schema", "leg_id", "store_id", "backend_uri", "enforcement",
                "lock_mode", "object_versions",
                "min_retention_days", "retain_until_utc", "objects", "pin_set_digest"}
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
        if lease["store_id"] != self.store_id:
            raise PreserveError(
                stage, f"lease 가 다른 store 의 것이다 — backend URI 는 같은데 "
                       f"store {lease['store_id'][:8]} ≠ {self.store_id[:8]}")
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
            if not _nonempty_str(lease["lock_mode"] or ""):
                raise PreserveError(stage, "object-lock lease 에 lock_mode 가 없다")
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
                if st.get("mode") != lease["lock_mode"]:
                    raise PreserveError(
                        stage, f"lock mode 가 lease 와 다르다: {st.get('mode')!r} "
                               f"≠ {lease['lock_mode']!r}")
                if str(st.get("retain_until") or "") < lease["retain_until_utc"]:
                    raise PreserveError(
                        stage, f"version 의 retain_until 이 lease 보다 짧다: "
                               f"{dg[:16]} {st.get('retain_until')!r} < "
                               f"{lease['retain_until_utc']}")
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
            # ★ `describe_locks` 는 **그 version 을 키로** 조회하므로 dict 가
            #   돌아온 것 자체가 version 일치를 뜻한다. 여기서 다시 비교하면
            #   같은 규칙이 두 곳에 생기고, 강한 쪽을 지워도 초록이 된다
            #   (변이로 확인했다).
            if st.get("mode") != lease["lock_mode"]:
                raise PreserveError(stage, "lease 의 lock mode 가 다르다")
            if str(st.get("retain_until") or "") < lease["retain_until_utc"]:
                raise PreserveError(stage, "lease 의 retain_until 이 짧다")
        on_disk = self.pinned(leg_id)
        want_disk = set(objs) | {lease_digest}
        if on_disk != want_disk:
            raise PreserveError(
                stage, f"pin 상태가 lease 와 다르다 — 없음 "
                       f"{sorted(want_disk - on_disk)[:2]} · 여분 "
                       f"{sorted(on_disk - want_disk)[:2]}")
        return dict(lease, lease_digest=lease_digest, lease_version=lease_version)

    # ── object-lock adapter 가 채워야 하는 자리 (★ 31차 P0-1) ───────────
    # local 은 아무 것도 잠그지 않으므로 빈 값을 돌려준다. 강제하는 backend 는
    # provider 가 만든 **immutable version ID** 를 돌려주고, 검증 때 그것을
    # 다시 조회해 살아 있는지 본다.

    def query_object_lock(self) -> dict | None:
        """provider 의 live lock 설정. local 은 잠글 provider 가 없다."""
        return None

    def lock_objects(self, leg_id: str, digests, until: str) -> dict:
        return {}

    def lock_content_object(self, dg: str, until: str) -> None:
        """CAS object 쪽도 잠근다 — pin 만 잠그면 원본이 지워질 수 있다."""
        return None

    def recover_lease_version(self, leg_id: str, lease_digest: str):
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

    def describe_locks(self, leg_id: str, versions: dict) -> dict:
        """version 별 **현재** lock 상태를 provider 에 묻는다.

        ★ 32차 P0-1 — 31차는 version **존재**만 봤다. 값이 유효한지, 지금 어떤
          mode 인지, 그 version 의 retain-until 이 언제인지 하나도 안 물었다.
          local 은 잠글 provider 가 없으므로 전부 `None` 이다.
        """
        return {dg: None for dg in versions}

    def retrieve_retained(self, lease: dict, dg: str) -> bytes:
        """lease 가 담보한 object 만 회수한다."""
        if dg not in set(lease.get("objects") or []):
            raise PreserveError("retention", f"lease 가 담보하지 않은 object: {dg[:16]}")
        return self.read_pinned(lease["leg_id"], dg)


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

    adapter 가 구현할 provider 계약 (S3 Object Lock 의 성질 그대로):

        put(key, data) -> version_id          # 잠긴 key 는 덮어쓰기 거부
        get(key, version=None) -> bytes
        delete(key, version=None)             # 잠긴 동안 거부
        lock(key, version, until)
        describe() -> {mode, min_retain_days}
        describe_object(key, version) -> {version_id, mode, retain_until} | None
        keys_under(prefix) -> [key]
    """

    ENFORCEMENT: ClassVar[str] = ENFORCEMENT_OBJECT_LOCK
    LOCK_MODES: ClassVar[frozenset] = frozenset({"COMPLIANCE", "GOVERNANCE"})

    #: 서브클래스가 붙이는 provider. 없으면 강제가 없는 것이다.
    provider: object = None

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
        try:
            rec = load_canonical(self.provider.get(key))
        except (KeyError, ValueError, UnicodeDecodeError):
            rec = None
        if isinstance(rec, dict) and _is_uuid_hex(rec.get("store_id") or ""):
            return rec["store_id"]
        # ★ 34차 P0-1 — `store.json` 은 잠기지 않은 control-plane object 였다.
        #   지우면 새 UUID 가 발급돼, content 와 lease 가 남아 있어도 기존
        #   receipt 가 복구 불가가 된다.
        vid = self.provider.put(key, canonical_bytes(
            {"schema": STORE_SCHEMA, "store_id": uuid.uuid4().hex}))
        far = (dt.datetime.now(dt.timezone.utc)
               + dt.timedelta(days=MIN_RETENTION_DAYS * 10)
               ).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.provider.lock(key, vid, far)
        return load_canonical(self.provider.get(key))["store_id"]

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

    def lock_content_object(self, dg: str, until: str) -> None:
        """CAS object 쪽도 잠근다 — pin 만 잠그면 원본을 지울 수 있다."""
        key = self._provider_obj_key(dg)
        vid = self.provider.put(key, self.read_back(dg))
        self.provider.lock(key, vid, until)

    def recover_lease_version(self, leg_id: str, lease_digest: str):
        """provider 에게 그 pin 의 **현재 version** 을 묻는다 (34차 P0-1)."""
        head = getattr(self.provider, "head_version", None)
        if not callable(head):
            raise PreserveError(
                "capability",
                "provider 가 head_version 을 주지 않는다 — lease proof 를 "
                "journal 없이 재발견할 수 없으면 재개가 새 lease 를 만든다")
        return head(self._provider_key(leg_id, lease_digest))

    def probe_enforcement(self) -> str:
        st = self.query_object_lock()
        if not isinstance(st, dict):
            return ENFORCEMENT_ADVISORY
        if st.get("mode") not in self.LOCK_MODES:
            return ENFORCEMENT_ADVISORY
        days = st.get("min_retain_days")
        if isinstance(days, bool) or not isinstance(days, int) \
                or days < MIN_RETENTION_DAYS:
            return ENFORCEMENT_ADVISORY
        return ENFORCEMENT_OBJECT_LOCK

    # ── 바이트는 provider 가 소유한다 ───────────────────────────────────
    def put_if_absent(self, data: bytes, *,
                      faults: frozenset[str] = frozenset()) -> dict:
        dg = hashlib.sha256(data).hexdigest()
        key = self._provider_obj_key(dg)
        try:
            old = self.provider.get(key)
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
            data = self.provider.get(self._provider_obj_key(dg))
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
            self.provider.get(self._provider_obj_key(dg))
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
                cur = self.provider.get(key)
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
        pre = f"pins/{leg_id}/"
        return {k[len(pre):] for k in self.provider.keys_under(pre)}

    def read_pinned(self, leg_id: str, dg: str) -> bytes:
        try:
            data = self.provider.get(self._provider_key(leg_id, dg))
        except KeyError as ex:
            raise PreserveError("pin", f"pin 이 없다: {dg[:16]}") from ex
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
            data = self.read_pinned(leg_id, dg)
            vid = self.provider.put(key, data)       # 이미 있으면 같은 version
            self.provider.lock(key, vid, until)
            out[dg] = vid
        return out

    def describe_locks(self, leg_id: str, versions: dict) -> dict:
        """version 별 **현재** lock 상태. 없으면 `None` 이 들어간다."""
        return {dg: self.provider.describe_object(self._provider_key(leg_id, dg), v)
                for dg, v in sorted(versions.items())}


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
    return backend.verify_retention(leg_id, j["lease_digest"],
                                    lease_version=j["lease_version"])


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
_JOURNAL_KEYS = frozenset({"leg_id", "receipt_object", "pin_set_digest",
                           "objects", "lease_digest", "lease_version"})


def _register(index_path: Path, leg_id: str, receipt_object: str,
              pin_digest: str, objects: list, lease_digest: str,
              lease_version: str = "") -> None:
    """durable 상태 변경. 기존 journal 이 다르면 **거부**한다.

    ★ 33차 P0-1 — `lease_version` 은 lease 자신의 lock proof 다. lease 는
      자기 digest 를 담을 수 없으므로 그 증거가 밖에 있어야 한다.
    """
    data = canonical_bytes({"leg_id": leg_id, "receipt_object": receipt_object,
                            "pin_set_digest": pin_digest,
                            "objects": sorted(set(objects)),
                            "lease_digest": lease_digest,
                            "lease_version": lease_version})
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
    lease = backend.verify_retention(leg_id, j["lease_digest"],
                                     lease_version=j["lease_version"])

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
    pbad = backend.verify_pins(leg_id, expected)
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
    backend.verify_retention(leg_id, lease["lease_digest"], expected=expected,
                             lease_version=lease.get("lease_version"))
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
              lease.get("lease_version") or "")

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
