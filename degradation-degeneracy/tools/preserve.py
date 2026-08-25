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

import errno
import hashlib
import json
import os
import re
import shutil
import tempfile
import uuid
from dataclasses import dataclass
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

    @property
    def uri(self) -> str:
        return f"file+cas://{self.root}"

    def _obj(self, dg: str) -> Path:
        return self.root / "objects" / dg[:2] / dg

    def put_if_absent(self, data: bytes, *, faults: frozenset[str] = frozenset()) -> dict:
        dg = hashlib.sha256(data).hexdigest()
        dst = self._obj(dg)
        if dst.exists():
            if dst.read_bytes() != data:
                raise PreserveError("cas_put",
                                    f"같은 digest 인데 저장된 바이트가 다르다: {dg[:16]}")
            return {"digest": dg, "stored": False, "idempotent": True}

        staging = self.root / "staging"
        staging.mkdir(parents=True, exist_ok=True)
        tmp = staging / f"{dg}.{uuid.uuid4().hex}.part"
        tmp.write_bytes(data[: len(data) // 2] if "partial_upload" in faults else data)
        if "partial_upload" in faults:
            raise PreserveError("cas_put", "업로드가 중간에 끊겼다 (주입)")
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.replace(tmp, dst)
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

    def orphans(self) -> list[Path]:
        st = self.root / "staging"
        return sorted(st.glob("*.part")) if st.is_dir() else []


#: payload manifest 의 닫힌 schema. 키가 남거나 모자라면 거부한다.
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
        paths.append(m["path"])
    dup = sorted({q for q in paths if paths.count(q) > 1})
    if dup:
        bad.append(f"중복 member 경로: {dup[:3]}")
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
    design_label: str = ""          # 사람용 — hash 밖
    notes: str = ""

    def __post_init__(self):
        if not _is_hex64(self.pairing_design_sha256):
            raise PreserveError(
                "planned_seal",
                f"pairing_design_sha256 이 64-hex 가 아니다: "
                f"{self.pairing_design_sha256!r} — 자유문자 label 을 정본으로 "
                "쓰면 설계가 바뀌어도 planned_id 가 안 움직인다")

    def envelope(self) -> dict:
        """hash 대상. **label 과 notes 는 들어가지 않는다** (사람용)."""
        return {
            "schema": "planned-leg/v2",
            "leg_id": self.leg_id,
            "protocol_generation": self.protocol_generation,
            "pairing_design_sha256": self.pairing_design_sha256,
            "source_digest": self.source_digest,
            "objectives": list(self.objectives),
            "total_start_budget": int(self.total_start_budget),
            "candidate_mode": self.candidate_mode,
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


def _exclusive_write(path: Path, data: bytes) -> bool:
    """**완성된 파일**에만 final name 을 붙인다. 이미 있으면 False.

    ★ 27차 P1-3 — 초판은 final pathname 을 먼저 `O_EXCL` 로 만들고 `os.write`
      를 한 번 호출했다. 부분 쓰기를 확인하지 않고 parent 도 fsync 하지 않아,
      5 bytes 만 쓰이면 "생성 성공" 인데 다음 읽기가 `JSONDecodeError` 였고
      immutable 파일 때문에 재시도로도 복구가 안 됐다.

      temp 에 **전부** 쓰고 fsync 한 뒤 `os.link` 로 no-replace commit 한다
      (link 는 대상이 있으면 EEXIST 로 실패하는 원자적 연산이다).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
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
    if created:
        dfd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(dfd)           # 이름이 durable 해야 crash 뒤에도 보인다
        finally:
            os.close(dfd)
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
    if not isinstance(rec, dict) or rec.get("leg_id") != leg_id:
        return None
    if not _is_hex64(rec.get("receipt_object") or ""):
        return None
    return rec


def is_registered(index_path: Path, leg_id: str) -> bool:
    """등록됐는가 — journal 이 **index 가 가리키는 receipt 와 같아야** 한다."""
    rec = registration(index_path, leg_id)
    if rec is None:
        return False
    e = index_entries(index_path).get(leg_id)
    return bool(e) and rec["receipt_object"] == e.get("receipt_object")


def _register(index_path: Path, leg_id: str, receipt_object: str) -> None:
    """durable 상태 변경. 기존 journal 이 다르면 **거부**한다."""
    data = canonical_bytes({"leg_id": leg_id, "receipt_object": receipt_object})
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

def check_output(out) -> list[str]:
    """재채점 산출이 계약을 만족하는가. 비면 통과."""
    if not isinstance(out, dict):
        return [f"산출이 dict 가 아니다: {type(out).__name__}"]
    bad = []
    # ★ 27차 P1-5 — semantic digest 만 요구하면 "무슨 파일을 만들었는가" 가
    #   receipt 어디에도 없다. byte 축을 함께 강제한다 (25차 Q2 는 둘 다 요구).
    for k in ("role", "canonicalizer", "semantic_schema", "semantic_sha256",
              "relative_path", "byte_size", "file_sha256", "producer"):
        if out.get(k) in (None, "", []):
            bad.append(f"산출에 {k} 가 없다")
    for k in ("semantic_sha256", "file_sha256"):
        if out.get(k) is not None and not _is_hex64(out.get(k)):
            bad.append(f"{k} 이 64-hex 가 아니다: {out.get(k)!r}")
    n = out.get("byte_size")
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        bad.append(f"byte_size 가 음이 아닌 정수가 아니다: {n!r}")
    rp = out.get("relative_path")
    if isinstance(rp, str) and (rp.startswith("/") or ".." in rp.split("/")):
        bad.append(f"relative_path 가 상대 경로가 아니다: {rp!r}")
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


def _validate_and_rescore(root: Path, hooks: Hooks,
                          faults: frozenset[str]) -> tuple[dict, dict]:
    if "validator_raises" in faults:
        raise PreserveError("validate", "검증기가 예외로 죽었다 (주입)")
    v = hooks.validate(root)
    if "validator_fails" in faults:
        v = {"ok": False, "fail": ["주입된 실패"]}
    if not v.get("ok"):
        raise PreserveError("validate", f"검증 실패: {v.get('fail')}")

    if "score_raises" in faults:
        raise PreserveError("rescore", "재채점이 예외로 죽었다 (주입)")
    out = hooks.rescore(root)
    bad = check_output(out)
    if bad:
        raise PreserveError("rescore", "; ".join(bad))
    sem = ("f" * 64 if "wrong_semantic_digest" in faults
           else out.get("semantic_sha256"))
    if sem != hooks.expected_semantic:
        raise PreserveError("rescore",
                            f"재채점 semantic digest 가 봉인과 다르다: {sem!r}")
    return v, dict(out, semantic_sha256=sem)


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
    if not isinstance(rec, dict):
        raise PreserveError(stage, "receipt 가 dict 가 아니다")
    if rec.get("schema") != "execution-receipt/v1":
        raise PreserveError(stage, f"receipt schema: {rec.get('schema')!r}")
    want = digest({k: v for k, v in rec.items() if k != "receipt_digest"})
    if rec.get("receipt_digest") != want:
        raise PreserveError(stage, "receipt 안의 digest 가 자기 내용과 다르다")
    for k, ik in (("leg_id", "leg_id"), ("planned_id", "planned_id"),
                  ("payload_root_digest", "payload_root_digest"),
                  ("payload_manifest_digest", "payload_manifest_digest"),
                  ("backend_uri", "backend_uri")):
        if rec.get(k) != e.get(ik):
            raise PreserveError(stage, f"receipt.{k} 가 index 와 다르다")
    if rec.get("receipt_digest") != e.get("receipt_digest"):
        raise PreserveError(stage, "receipt_digest 가 index 와 다르다")
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
        v, out = _validate_and_rescore(root, hooks, faults)

        # ── 8. receipt 를 **CAS 에 저장**하고 되읽는다 (P0-2) ───────────
        receipt = {
            "schema": "execution-receipt/v1",
            "leg_id": leg_id,
            "planned_id": pid,
            "planned_envelope": envelope,
            "backend_uri": backend.uri,
            "payload_root_digest": root_digest,
            "payload_manifest_digest": man_dg,
            "n_members": man["n_members"],
            "total_bytes": man["total_bytes"],
            "validation": {"ok": True, "n_checks": len(v.get("checks") or {})},
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

        # ── 10. 등록 **직전** 재회수 대조 → durable 등록 ─────────────────
        if "crash_after_publish" in faults:
            raise PreserveError("register", "publish 뒤 등록 전에 죽었다 (주입)")
        verify_registered_receipt(backend, index_path, leg_id)
        _register(index_path, leg_id, r_obj)
        return {"ok": True, "receipt": receipt, "planned_id": pid,
                "payload_root_digest": root_digest, "receipt_object": r_obj}
    finally:
        shutil.rmtree(root, ignore_errors=True)


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
    if is_registered(index_path, leg_id):
        return {"ok": True, "already": True}
    rec = verify_registered_receipt(backend, index_path, leg_id)
    _register(index_path, leg_id, e["receipt_object"])
    return {"ok": True, "already": False, "receipt": rec,
            "receipt_object": e["receipt_object"]}
