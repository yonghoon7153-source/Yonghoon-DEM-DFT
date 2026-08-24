"""preserve.py — 다리 생성을 **트랜잭션**으로 만든다 (계약 v4 묶음 9).

왜 이것이 필요한가
──────────────────
2026-08-20 에 warm 실험 7다리를 만들고 보존 없이 끝냈다. 나흘 뒤 작업 기계가
바뀌면서 원자료가 전부 사라졌다. **도구가 없어서가 아니다** —
`tools/archive_bundle.py` 는 이미 fail-closed 였고 `paired_fixed5_v4` 에서 실제로
작동했다. 없었던 것은 **강제**다: 다리를 만들고 보존을 안 해도 아무 일도
일어나지 않았다.

그래서 이 모듈은 "보존하는 도구" 가 아니라 **"보존 없이는 끝날 수 없게 만드는
gate"** 다. 25차 리뷰가 요구한 two-phase 순서 그대로:

    planned_leg seal
    → private temp 로 실행
    → payload seal
    → CAS staging put-if-absent
    → remote read-back
    → truly empty root 복원
    → validate + score/analyze
    → immutable receipt/output manifest
    → final index 의 atomic publish
    → 그 뒤에만 execution/status/claim 등록

실패한 object 는 public index 에 들어가지 않고 orphan 으로 남는다 (GC 대상).

backend
───────
`file+cas://<root>` 만 구현한다. 실제 cloud store 는 이 브랜치에서 검증할 수
없고 (자격증명·외부 인프라), 25차 Q1 이 "fault injection 가능한 local
content-addressed backend 로 트랜잭션 의미를 완전히 검증하면 된다" 고 답했다.
실제 운영 backend 의 canary receipt 는 첫 pilot 전 **별도 gate** 다.

★ git `artifacts/` 는 legacy bundle 과 fixture 로만 쓴다. 같은 worktree 는
  독립 failure domain 이 아니고, 계약이 스스로 큰 leg 를 git 에 넣지 말라고 한다.

fault injection
───────────────
`faults` 에 이름을 넣으면 그 단계가 실패한다. 회귀가 각 실패 모드에서
**public index 가 오염되지 않는지** 를 본다. 이름 목록은 `FAULTS`.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

#: 주입 가능한 실패 모드. 회귀가 이 이름들을 그대로 쓴다.
FAULTS = frozenset({
    "member_bit_flip",        # staging 직전 member 한 바이트 변경
    "member_missing",         # manifest 에 있는 member 를 뺀다
    "member_extra",           # manifest 에 없는 파일이 run_dir 에 있다
    "stale_payload_index",    # payload manifest 가 실물보다 낡았다
    "partial_upload",         # CAS put 중간에 죽는다
    "crash_before_publish",   # 전부 성공했는데 publish 직전에 죽는다
    "crash_after_publish",    # publish 직후 등록 전에 죽는다
    "read_back_corrupt",      # backend 에서 되읽은 바이트가 다르다
    "restore_incomplete",     # 빈 root 복원이 일부만 된다
    "validator_raises",       # 검증기가 예외로 죽는다
    "validator_fails",        # 검증기가 ok=False 를 돌려준다
    "score_raises",           # 재채점이 예외로 죽는다
    "wrong_semantic_digest",  # 재채점 결과가 봉인과 다르다
    "wrong_planned_id",       # 실행이 다른 planned leg 를 가리킨다
    "wrong_source_digest",    # run_spec 의 code identity 가 계획과 다르다
    "retention_too_short",    # backend 의 보존 기간이 요구를 못 채운다
    "no_read_access",         # backend 를 되읽을 권한이 없다
})


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
    """정규 직렬화. 키 정렬 · UTF-8 · 구분자 고정 · 후행 개행 없음.

    float 는 `repr` 이 아니라 JSON 기본 표현을 쓴다 — Python 사이에서는 같고,
    다른 언어와 맞춰야 할 때는 묶음 2 의 wire schema 가 규칙을 정한다.
    """
    return json.dumps(obj, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(obj) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


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
            # 같은 digest 면 바이트도 같다. 그래도 되읽어 확인한다 —
            # 조용한 손상을 여기서 잡는다.
            if dst.read_bytes() != data:
                raise PreserveError("cas_put",
                                    f"같은 digest 인데 저장된 바이트가 다르다: {dg[:16]}")
            return {"digest": dg, "stored": False, "idempotent": True}

        staging = self.root / "staging"
        staging.mkdir(parents=True, exist_ok=True)
        tmp = staging / f"{dg}.{uuid.uuid4().hex}.part"
        tmp.write_bytes(data[: len(data) // 2] if "partial_upload" in faults else data)
        if "partial_upload" in faults:
            # 죽은 척한다 — `objects/` 로 옮기지 않는다.
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

    def orphans(self) -> list[Path]:
        st = self.root / "staging"
        return sorted(st.glob("*.part")) if st.is_dir() else []


# ─────────────────────────────────────────────────────────────────────────────
# 1단계 — planned leg seal
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class PlannedLeg:
    """실행 **전에** 못 박는 것. 이것 없이는 트랜잭션이 시작되지 않는다.

    묶음 1 의 최소 envelope 다 — 무엇을 돌리기로 했는가. 실제로 무엇이
    돌았는가는 `execution_receipt` 가 따로 적는다 (둘을 한 파일에 섞으면
    "계획대로 됐는가" 를 물을 수 없다).
    """

    leg_id: str
    protocol_generation: str
    design_id: str
    source_digest: str
    objectives: tuple[str, ...]
    total_start_budget: int
    candidate_mode: str
    notes: str = ""

    def envelope(self) -> dict:
        return {
            "schema": "planned-leg/v1",
            "leg_id": self.leg_id,
            "protocol_generation": self.protocol_generation,
            "design_id": self.design_id,
            "source_digest": self.source_digest,
            "objectives": list(self.objectives),
            "total_start_budget": int(self.total_start_budget),
            "candidate_mode": self.candidate_mode,
            "notes": self.notes,
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
# public index — atomic publish
# ─────────────────────────────────────────────────────────────────────────────

def publish(index_path: Path, entry: dict) -> dict:
    """final index 를 원자적으로 갱신한다. 같은 leg 를 다른 내용으로 덮지 않는다."""
    index_path = Path(index_path)
    idx = {"schema": "bundle-index/v1", "entries": {}}
    if index_path.is_file():
        idx = yaml.safe_load(index_path.read_text(encoding="utf-8")) or idx
    old = (idx.get("entries") or {}).get(entry["leg_id"])
    if old is not None and old != entry:
        raise PreserveError("publish",
                            f"{entry['leg_id']} 가 이미 다른 내용으로 등록돼 있다 "
                            "— immutable index 는 덮지 않는다")
    idx.setdefault("entries", {})[entry["leg_id"]] = entry
    tmp = index_path.with_suffix(index_path.suffix + f".{uuid.uuid4().hex}.tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(yaml.safe_dump(idx, allow_unicode=True, sort_keys=True),
                   encoding="utf-8")
    os.replace(tmp, index_path)          # 원자적 교체
    return idx


def index_entries(index_path: Path) -> dict:
    p = Path(index_path)
    if not p.is_file():
        return {}
    return (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("entries") or {}


# ─────────────────────────────────────────────────────────────────────────────
# 트랜잭션
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Hooks:
    """검증·재채점을 주입한다. 과학 코드를 이 모듈에 넣지 않기 위해서다.

    기본값은 아무 것도 안 하는 stub 이 아니라 **없으면 실패**다 — 검증 없이
    통과하는 경로를 만들지 않는다.
    """

    validate: object = None          # (root, run_rel) -> {"ok":…, "fail":[…]}
    rescore: object = None           # (root, run_rel) -> {"semantic_sha256": …}
    restore: object = None           # (man, src_dir, dst_root) -> None
    min_retention_days: int = 365
    expected_semantic: str | None = None


def run_transaction(planned: PlannedLeg, run_dir: Path, backend: CasBackend,
                    index_path: Path, hooks: Hooks, *,
                    faults: frozenset[str] = frozenset()) -> dict:
    """10단계를 순서대로. 어디서든 멈추면 public index 는 건드리지 않는다."""
    faults = frozenset(faults)
    unknown = faults - FAULTS
    if unknown:
        raise ValueError(f"모르는 fault: {sorted(unknown)}")
    run_dir = Path(run_dir)

    for name in ("validate", "rescore", "restore"):
        if getattr(hooks, name) is None:
            raise PreserveError("hooks", f"{name} hook 이 없다 — 검증 없이 통과할 수 없다")

    # ── 0. backend 능력 ─────────────────────────────────────────────────
    retention = 1 if "retention_too_short" in faults else backend.retention_days
    if retention < hooks.min_retention_days:
        raise PreserveError("capability",
                            f"보존 기간 {retention}일 < 요구 {hooks.min_retention_days}일")

    # ── 1. planned leg seal ─────────────────────────────────────────────
    pid = planned.planned_id()
    spec_path = run_dir / "run_spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8")) if spec_path.is_file() else {}
    claimed = "다른-계획" if "wrong_planned_id" in faults else spec.get("planned_id", pid)
    if claimed != pid:
        raise PreserveError("planned_seal",
                            f"실행이 가리키는 계획 {claimed!r} ≠ 봉인한 계획 {pid[:16]}")
    got_digest = ("다른-digest" if "wrong_source_digest" in faults
                  else spec.get("source_digest", planned.source_digest))
    if got_digest != planned.source_digest:
        raise PreserveError("planned_seal",
                            f"code identity 가 계획과 다르다: {got_digest!r}")

    # ── 2. payload seal ─────────────────────────────────────────────────
    man = seal_payload(run_dir, faults=faults)
    # ★ 봉인 **뒤** 손상 — 전송·보관 중 변조가 실제 모양이다. 봉인 전에 뒤집으면
    #   manifest 가 손상본을 그대로 기록해서 아무 것도 안 잡힌다.
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
    stored = {}
    for m in man["members"]:
        r = backend.put_if_absent((run_dir / m["path"]).read_bytes(), faults=faults)
        stored[m["path"]] = r["digest"]
    man_dg = backend.put_if_absent(canonical_bytes(man), faults=faults)["digest"]

    # ── 4. read-back — backend 에서 되읽어 다시 해시 ────────────────────
    for rel, dg in stored.items():
        backend.read_back(dg, faults=faults)
    backend.read_back(man_dg, faults=faults)

    # ── 5. truly empty root 복원 ────────────────────────────────────────
    root = Path(tempfile.mkdtemp(prefix=f"preserve_{planned.leg_id}_"))
    try:
        hooks.restore(man, run_dir, root)
        if "restore_incomplete" in faults:
            victims = [p for p in sorted(root.rglob("*")) if p.is_file()]
            if victims:
                victims[-1].unlink()
        rbad = verify_payload(root, man)
        if rbad:
            raise PreserveError("empty_root_restore", "; ".join(rbad[:4]))

        # ── 6. 검증 ─────────────────────────────────────────────────────
        if "validator_raises" in faults:
            raise PreserveError("validate", "검증기가 예외로 죽었다 (주입)")
        v = hooks.validate(root)
        if "validator_fails" in faults:
            v = {"ok": False, "fail": ["주입된 실패"]}
        if not v.get("ok"):
            raise PreserveError("validate", f"검증 실패: {v.get('fail')}")

        # ── 7. 복원본만으로 재채점 ──────────────────────────────────────
        if "score_raises" in faults:
            raise PreserveError("rescore", "재채점이 예외로 죽었다 (주입)")
        out = hooks.rescore(root)
        sem = ("다른-semantic" if "wrong_semantic_digest" in faults
               else out.get("semantic_sha256"))
        if hooks.expected_semantic is not None and sem != hooks.expected_semantic:
            raise PreserveError("rescore",
                                f"재채점 semantic digest 가 봉인과 다르다: {sem!r}")

        # ── 8. immutable receipt ────────────────────────────────────────
        receipt = {
            "schema": "execution-receipt/v1",
            "leg_id": planned.leg_id,
            "planned_id": pid,
            "planned_envelope": planned.envelope(),
            "backend_uri": backend.uri,
            "payload_root_digest": man["root_digest"],
            "payload_manifest_digest": man_dg,
            "n_members": man["n_members"],
            "total_bytes": man["total_bytes"],
            "validation": {"ok": True, "n_checks": len(v.get("checks") or {})},
            "outputs": [dict(out, semantic_sha256=sem)],
            "retention_days": retention,
        }
        receipt["receipt_digest"] = digest(receipt)

        # ── 9. atomic publish ───────────────────────────────────────────
        if "crash_before_publish" in faults:
            raise PreserveError("publish", "publish 직전에 죽었다 (주입)")
        publish(index_path, {"leg_id": planned.leg_id,
                             "planned_id": pid,
                             "receipt_digest": receipt["receipt_digest"],
                             "payload_root_digest": man["root_digest"],
                             "backend_uri": backend.uri})

        # ── 10. 등록 — publish 가 성공한 뒤에만 ─────────────────────────
        if "crash_after_publish" in faults:
            raise PreserveError("register", "publish 뒤 등록 전에 죽었다 (주입)")
        return {"ok": True, "receipt": receipt, "planned_id": pid,
                "payload_root_digest": man["root_digest"]}
    finally:
        shutil.rmtree(root, ignore_errors=True)
