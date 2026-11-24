"""REIL C4-ENV 새 세대 (2026-11-24 · CPython 3.11.18) 대조기 — stdlib 만 · 시스템 python 을 `-I -B` 로 · 과학 패키지 import 0.

요청서 `bms-balancing/docs/REIL_C4_ENV_RESEAL_REQUEST_20261124.md` §1-8 · §2 (S0 · S4 · S9) 가 부른다. 옛 (수용) 세대 =
2026-10-13 봉인 `reil_c6_rebuild_20261013/` (MANIFEST 4f120948… · 상태 문서 §38) 와 그 원문 기록 `evidence/reil_c4_env_20261013/`.
10월 도구 `reil_c4_env_compare.py` 는 고치지 않는다 (그 실행의 증거다). 이 파일은 그 자리를 잇는 새 도구다.

  bundled  ensurepip 묶음 wheel 2 를 이름 · 크기 · sha256 로 · wheel 안 구성원을 옛 설치 RECORD 원문과 행 단위로 (선언된 행만 다름)
  wheels   내려받은 wheel 디렉터리를 옛 기록 (04_artifacts_*.json) 과 이름 · 크기 · sha256 의 정확 집합으로
  records  새 venv · pytest_t 의 RECORD 원문 30 + 4 를 옛 원문 30 + 4 와 바이트 · 행 단위로 + 해시 있는 행 = 실제 설치 바이트 · 크기
  seal     새 봉인 11 파일을, 옛 봉인에서 정해진 자리만 바꿔 정확한 바이트로 다시 만든 기대값과

rc 0 = 허용 차이만 · 1 = 미허용 하나 이상 (보고서에 전부 적는다) · 2 = 사용 · 입력 오류 (덮어쓰기 거부 포함) · 3 = 도구 오류
(예상 밖 예외 — 보고서를 쓰지 않는다). 어느 쪽이든 0 이 아니면 실행기는 그 자리에서 멈춘다.
검토 ENV-P2-02 의 네 약점을 닫는 자리 — 줄바꿈 종류 · 마지막 줄바꿈: parse_record 의 줄 끝 목록 대조 · 중복 경로: parse_record 거부 ·
bin 결속: wrapper_check (새 파일의 첫 줄만 옛 경로로 되돌린 바이트가 옛 RECORD 행의 해시 · 크기와 같아야 함) · 다른 dist-info 행:
compare_record 의 own_distinfo 규칙. 쓰는 곳은 `--out` 과 `--records-out` · `--test-records-out` 뿐이고, 이미 있으면 쓰지 않는다.
"""
from __future__ import annotations

import argparse
import base64
import csv
import email.parser
import hashlib
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

SP = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad"
OLD_VENV = SP + "/reil_c4env/venv"          # 2026-10-13 세대 (shebang 119 · 123 B)
NEW_VENV = SP + "/reil_env18/venv"          # 이 세대 — 뿌리 이름 길이를 옛것과 같게 (shebang 길이 · bin 크기 칸 불변)
OLD_E = "bms-balancing/evidence/reil_c4_env_20261013"
OLD_SEAL = "bms-balancing/reil_c6_rebuild_20261013"
PY_OLD = ("3.11.17", ["main", "Oct  1 2026 15:41:07"])
PY_NEW = ("3.11.18", ["main", "Oct 26 2026 15:28:55"])

#: ensurepip 묶음 — 2026-11-24 읽기 관측값. setuptools 는 10월 S0 기록과 sha 가 같다. pip 는 다르다 (요청서 §1-2):
#: wheel 안 구성원 524 중 `pip/_vendor/certifi/cacert.pem` 하나만 다르고 (wheel 의 RECORD 도 그에 맞게 다시 쓰여 있다),
#: `dpkg -V python3.11-venv` 가 이 파일의 md5 불일치 (`??5??????`) 를 보고한다 = deb 설치 뒤에 바뀌었다.
BUNDLED = {
    "pip-24.0-py3-none-any.whl": {"size": 2106360,
                                  "sha256": "9c51d6ade96c424e64356a9337fe15be2cce412b3ddb962f3efb61f63001d118",
                                  "oct_sha256": "ba0d021a166865d2265246961bec0152ff124de910c5cc39f1156ce3fa7c69dc",
                                  "old_record": "pip-24.0.RECORD"},
    "setuptools-79.0.1-py3-none-any.whl": {"size": 1256281,
                                           "sha256": "e147c0549f27767ba362f9da434eab9c5dc0045d5304feb602a0af001089fc51",
                                           "oct_sha256": "e147c0549f27767ba362f9da434eab9c5dc0045d5304feb602a0af001089fc51",
                                           "old_record": "setuptools-79.0.1.RECORD"},
}
#: 바이트가 달라도 되는 "bin 아닌" 행 — 이것 하나뿐 (옛 값 → 새 값 · 정확 일치만 통과)
DECLARED = {("pip-24.0.RECORD", "pip/_vendor/certifi/cacert.pem"):
            (("sha256=eU0Dn_3yd8BH4m8sfVj4Glhl2KDrcCSg-sEWT-pNJ88", "281617"),
             ("sha256=EtCzPV1HGcSG65jK42uCJO7zOhjjTOo_q8vcC6Q8Btk", "273525"))}
SEAL_FILES = ("COBYQA_OPTIONS.json", "MANIFEST.json", "PROFILE.json", "REIL_C6.lock.txt", "SOBOL_PHASE_A.json",
              "sobol_A0_their_box_seed0.npy", "sobol_A0_their_box_seed1.npy", "sobol_A1_A2_wide_box_seed0.npy",
              "sobol_A1_A2_wide_box_seed1.npy", "sobol_unit_seed0.npy", "sobol_unit_seed1.npy")
#: 설명된 충돌 — reil_c6_profile.EXPLAINED_COLLISIONS 와 같은 한 건 (pymoo → alive-progress → about-time 의 두 wheel 이 venv 꼭대기
#: LICENSE 를 함께 주장하고 나중에 깔린 alive-progress 가 덮었다). 이 행의 디스크 바이트는 주인 배포판 RECORD 의 같은 경로 행과 같아야 한다.
COLLISIONS = {("about-time-4.2.1.RECORD", "../../../LICENSE"): "alive-progress-3.3.0.RECORD"}
NEW_TARGET = SP + "/reil_env18/pytest_t"
#: RECORD 의 생성 wrapper 행 접두 — venv (site-packages 기준) · `pip install --target` (target 기준, 실제 파일은 target/bin/)
WRAPPER_PREFIX = {"venv": "../../../bin/", "target": "../../bin/"}
INTERPRETERS = ("python", "python3.11")
#: v2 (검토 §137 Q5): RECORD 밖 파일 가운데 실행 경로에 닿을 수 있는 것 — 자동 실패가 아니라 채택 보류 표지 (adoption_hold) 로 올린다
#: (.pth 의 import 줄은 시작 때 실행될 수 있다 · sitecustomize / usercustomize 는 .py 로 잡힌다)
EXEC_SUFFIXES = (".pth", ".py", ".pyc", ".pyo", ".so", ".pyd")
_LINE = re.compile(rb"([^\r\n]*)(\r\n|\n|\r|)")
_DIST = re.compile(r"(?P<name>[^=\s#]+)==(?P<version>[^\s#]+)  # record-sha256 (?P<record>[0-9a-f]{64}|none)")


class UsageError(Exception):
    pass


# ── 공통 ─────────────────────────────────────────────────────────────────────

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def record_hash(b: bytes) -> str:
    """RECORD 의 해시 칸 형식 (PEP 376/627: sha256= + urlsafe base64 · 채움 없음)."""
    return "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b"=").decode()


def text_sha(raw: bytes) -> str:
    """env_profile.measure() 의 record-sha256 와 같은 값 — `dist.read_text("RECORD")` (utf-8 · universal newline) 의 utf-8 sha256."""
    return sha256_hex(raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))


def dump_json(obj) -> str:
    """reil_c6_profile._dump 와 같은 직렬화 (PROFILE · MANIFEST 재구성에 쓴다)."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n"


def file_digest(p: Path) -> tuple[int, str]:
    b = p.read_bytes()
    return len(b), sha256_hex(b)


def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


# ── RECORD 원문 ───────────────────────────────────────────────────────────────

def parse_record(raw: bytes) -> tuple[list, list, list]:
    """RECORD 원문 → (행 [(경로, 해시, 크기)], 줄 끝 목록, 문제). 다시 쓴 CSV 가 원문 줄과 바이트로 같을 때만 그 행을 받는다.

    줄 끝은 버리지 않고 목록으로 돌려준다 (CRLF · LF · CR · 마지막 줄의 '없음' 까지) — 옛 원문과 그대로 대조한다.
    같은 경로가 두 번 나오면 문제다 (dict 로 덮지 않는다)."""
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [], [], [f"utf-8 아님: {exc}"]
    rows, ends, probs, seen = [], [], [], set()
    pos = 0
    while pos < len(raw):
        m = _LINE.match(raw, pos)
        body, end = m.group(1), m.group(2)
        pos = m.end()
        ends.append(end.decode("ascii"))
        no = len(ends)
        parsed = list(csv.reader([body.decode("utf-8")], strict=True))
        if len(parsed) != 1 or len(parsed[0]) != 3:
            probs.append(f"{no} 행: 칸 3 개가 아님 ({body[:80]!r})")
            continue
        row = tuple(parsed[0])
        buf = io.StringIO()
        csv.writer(buf, lineterminator="").writerow(row)
        if buf.getvalue().encode("utf-8") != body:
            probs.append(f"{no} 행: CSV 로 다시 쓴 바이트가 원문과 다름 ({body[:80]!r})")
        if row[0] in seen:
            probs.append(f"{no} 행: 중복 경로 {row[0]!r}")
        seen.add(row[0])
        rows.append(row)
    return rows, ends, probs


def own_distinfo(rows: list) -> str | None:
    recs = [r[0] for r in rows if re.fullmatch(r"[^/]+\.dist-info/RECORD", r[0])]
    return recs[0].split("/")[0] if len(recs) == 1 else None


def resolve(kind: str, base: Path, root: Path, rel: str) -> Path | None:
    """RECORD 경로 → 실제 파일. venv 는 site-packages 기준 (bin 은 ../../../bin) · target 은 `../../bin/X` → target/bin/X
    (pip `--target` 은 RECORD 를 고쳐 쓰지 않고 bin 을 target 아래로 옮긴다). 뿌리 밖을 가리키면 None."""
    if kind == "target" and rel.startswith(WRAPPER_PREFIX["target"]):
        p = Path(os.path.normpath(root / "bin" / rel[len(WRAPPER_PREFIX["target"]):]))
    else:
        p = Path(os.path.normpath(base / rel))
    r = Path(os.path.normpath(root))
    return p if os.path.commonpath([str(p), str(r)]) == str(r) else None


def wrapper_check(old_row, new_row, data: bytes, old_bin: str, new_bin: str) -> str | None:
    """생성 wrapper 결속: 첫 줄이 `#!<새 venv>/bin/<python|python3.11>\\n` 이고, 그 첫 줄만 옛 venv 경로로 되돌린 바이트가
    옛 RECORD 행의 해시 · 크기와 같아야 한다 (본문 · 이름 · 판정 범주가 옛것과 같다는 뜻). 새 행의 값은 새 파일 바이트와 같아야 한다."""
    nl = data.find(b"\n")
    first, rest = (data[:nl + 1], data[nl + 1:]) if nl >= 0 else (data, b"")
    for exe in INTERPRETERS:
        if first == f"#!{new_bin}/{exe}\n".encode():
            back = f"#!{old_bin}/{exe}\n".encode() + rest
            if (record_hash(back), str(len(back))) != (old_row[1], old_row[2]):
                return f"첫 줄을 옛 경로로 되돌린 바이트가 옛 행과 다름 (본문이 다르다) — {new_row[0]}"
            if (record_hash(data), str(len(data))) != (new_row[1], new_row[2]):
                return f"새 RECORD 행이 새 파일 바이트와 다름 — {new_row[0]}"
            return None
    return f"첫 줄이 새 venv interpreter 가 아님 ({first[:140]!r}) — {new_row[0]}"


def compare_record(key: str, old_raw: bytes, new_raw: bytes, *, kind: str, base: Path, root: Path,
                   old_bin: str, new_bin: str, declared: dict, collisions: dict | None = None) -> dict:
    """한 배포판의 RECORD 원문 둘을 대조한다. `collisions` = {(key, 경로): (주인 해시, 주인 크기)} — 그 행만 디스크 바이트를
    자기 행이 아니라 주인 배포판의 행과 대조한다 (설명된 충돌). 나머지 해시 있는 행은 전부 자기 행과 같아야 한다."""
    P, changed, coll = [], [], []
    collisions = collisions or {}
    o_rows, o_ends, op = parse_record(old_raw)
    n_rows, n_ends, nq = parse_record(new_raw)
    P += [f"옛 원문 {x}" for x in op] + [f"새 원문 {x}" for x in nq]
    if o_ends != n_ends:
        P.append(f"줄 수 · 줄 끝이 다름 (옛 {len(o_ends)} 줄 {sorted(set(o_ends))} · 새 {len(n_ends)} 줄 {sorted(set(n_ends))})")
    if [r[0] for r in o_rows] != [r[0] for r in n_rows]:
        so, sn = [r[0] for r in o_rows], [r[0] for r in n_rows]
        P.append(f"행 경로 · 순서가 다름 (옛에만 {sorted(set(so) - set(sn))[:5]} · 새에만 {sorted(set(sn) - set(so))[:5]})")
    own = own_distinfo(n_rows)
    if own is None:
        P.append("자기 dist-info/RECORD 행이 정확히 하나가 아님")
    for rows, side in ((o_rows, "옛"), (n_rows, "새")):
        for r in rows:
            top = r[0].split("/")[0]
            if top.endswith(".dist-info") and top != own:
                P.append(f"{side} RECORD 에 다른 dist-info 의 행 {r[0]!r}")
    prefix = WRAPPER_PREFIX[kind]
    for o, n in zip(o_rows, n_rows):
        if o[0] != n[0]:
            continue                                   # 위에서 이미 보고
        if n[0].startswith(prefix):                    # wrapper 는 같아 보여도 항상 결속 검사 (옛 경로가 남은 파일을 잡는다)
            f = resolve(kind, base, root, n[0])
            if f is None or not f.is_file():
                P.append(f"wrapper 파일 없음 {n[0]}")
                continue
            why = wrapper_check(o, n, f.read_bytes(), old_bin, new_bin)
            if why:
                P.append(why)
            elif o != n:
                changed.append({"path": n[0], "kind": "wrapper", "old": list(o[1:]), "new": list(n[1:])})
            continue
        if o == n:
            continue
        want = declared.get((key, n[0]))
        if want and (o[1], o[2]) == want[0] and (n[1], n[2]) == want[1]:
            changed.append({"path": n[0], "kind": "declared", "old": list(o[1:]), "new": list(n[1:])})
        else:
            P.append(f"행 다름 (허용 밖) {n[0]}: 옛 {o[1:]} · 새 {n[1:]}")
    hashed = 0
    for path, h, size in n_rows:
        if not h:
            if size or not (path == f"{own}/RECORD" or (path.endswith(".pyc") and "/__pycache__/" in "/" + path)):
                P.append(f"해시 없는 행이 pyc · RECORD 가 아님 {path!r}")
            continue
        f = resolve(kind, base, root, path)
        if f is None or not f.is_file():
            P.append(f"해시 있는 행의 파일 없음 {path}")
            continue
        b = f.read_bytes()
        hashed += 1
        got = (record_hash(b), str(len(b)))
        owner = collisions.get((key, path))
        if owner is not None:
            coll.append({"path": path, "disk": list(got), "own_row": [h, size], "owner_row": list(owner)})
            if got != tuple(owner):
                P.append(f"설명된 충돌 {path}: 디스크 바이트가 주인 배포판의 행과 다름")
        elif got != (h, size):
            P.append(f"설치 바이트가 RECORD 와 다름 {path}")
    return {"key": key, "rows": len(n_rows), "hashed_rows_checked": hashed, "old_raw_sha256": sha256_hex(old_raw),
            "new_raw_sha256": sha256_hex(new_raw), "old_text_sha256": text_sha(old_raw), "new_text_sha256": text_sha(new_raw),
            "raw_identical": old_raw == new_raw, "changed_rows": changed, "explained_collisions": coll, "problems": P}


def metadata_key(distinfo: Path) -> str:
    msg = email.parser.HeaderParser().parsestr((distinfo / "METADATA").read_text(encoding="utf-8"))
    if not msg["Name"] or not msg["Version"]:
        raise UsageError(f"METADATA 에 Name · Version 없음: {distinfo}")
    return f"{normalize(msg['Name'])}-{msg['Version']}.RECORD"


def covered_files(kind: str, base: Path, root: Path, rows_by_key: dict) -> set:
    out = set()
    for rows in rows_by_key.values():
        for r in rows:
            p = resolve(kind, base, root, r[0])
            if p is not None:
                out.add(str(p))
    return out


def records(*, venv: Path, target: Path, old_sci: Path, old_test: Path, old_bin: str, new_bin: str, declared: dict,
            collisions: dict, sci_out: Path | None = None, test_out: Path | None = None) -> dict:
    sp = venv / "lib" / "python3.11" / "site-packages"
    if not sp.is_dir() or not target.is_dir():
        raise UsageError(f"site-packages 또는 target 없음: {sp} · {target}")
    groups = []
    report = {"dists": {}, "problems": [], "observations": {}}
    sci_dirs, test_dirs = sorted(sp.glob("*.dist-info")), sorted(target.glob("*.dist-info"))
    # v2 (검토 §137 ENV18-C2): 사전 (dict) 에 넣기 **전에** 배포판 식별 (METADATA 의 정규화 Name + Version) 중복을 거부한다 —
    # 서로 다른 dist-info 디렉터리가 같은 식별을 내면 하나가 다른 하나를 덮어, 가짜가 대조에서 빠지고 관측에만 남을 수 있었다.
    for label, dirs in (("science", sci_dirs), ("test_tools", test_dirs)):
        seen = {}
        for d in dirs:
            seen.setdefault(metadata_key(d), []).append(d.name)
        for k, names in sorted(seen.items()):
            if len(names) > 1:
                report["problems"].append(f"{label}: 같은 배포판 식별 ({k[:-len('.RECORD')]}) 을 내는 dist-info 가 둘 이상 — {names}")
    new_sci = {}
    for d in sci_dirs:
        new_sci.setdefault(metadata_key(d), d / "RECORD")      # 중복은 위에서 이미 미허용 — 덮어쓰지 않는다
    new_test = {f"{d.name}.RECORD": d / "RECORD" for d in test_dirs}
    for label, kind, base, root, old_dir, new_map, out in (
            ("science", "venv", sp, venv, old_sci, new_sci, sci_out),
            ("test_tools", "target", target, target, old_test, new_test, test_out)):
        old_keys = sorted(p.name for p in old_dir.iterdir() if p.name.endswith(".RECORD"))
        if sorted(new_map) != old_keys:
            report["problems"].append(f"{label}: 배포판 집합이 다름 — 옛에만 {sorted(set(old_keys) - set(new_map))} · "
                                      f"새에만 {sorted(set(new_map) - set(old_keys))}")
        raws = {key: new_map[key].read_bytes() for key in sorted(set(old_keys) & set(new_map))}
        rows_by_key = {key: parse_record(raw)[0] for key, raw in raws.items()}
        coll_rows = {}
        for (key, path), owner in collisions.items():
            if key in raws:
                hit = [r for r in rows_by_key.get(owner, []) if r[0] == path]
                if len(hit) != 1 or not any(r[0] == path for r in rows_by_key[key]):
                    report["problems"].append(f"{label}: 설명된 충돌 {key} {path} — 두 RECORD 가 모두 그 경로를 주장해야 한다")
                    continue
                coll_rows[(key, path)] = hit[0][1:]
        for key, new_raw in raws.items():
            r = compare_record(key, (old_dir / key).read_bytes(), new_raw, kind=kind, base=base, root=root,
                               old_bin=old_bin, new_bin=new_bin, declared=declared, collisions=coll_rows)
            report["dists"][f"{label}/{key}"] = r
            report["problems"] += [f"{label}/{key}: {x}" for x in r["problems"]]
            if out is not None:
                (out / key).write_bytes(new_raw)
        if label == "science":
            used_c = {(k.split("/", 1)[1], c["path"]) for k, r in report["dists"].items() for c in r["explained_collisions"]}
            if used_c != set(collisions):
                report["problems"].append(f"설명된 충돌이 선언과 다름 — 선언 {sorted(collisions)} · 관측 {sorted(used_c)}")
        groups.append((label, kind, base, root, rows_by_key))
    hold = []
    for label, kind, base, root, rows_by_key in groups:     # 관측 (rc 판정에 쓰지 않음): RECORD 어디에도 없는 파일 — v2 는 전체 목록 · 크기 · sha
        cov = covered_files(kind, base, root, rows_by_key)
        scan = base if kind == "venv" else root
        unlisted = []
        for p in sorted(scan.rglob("*")):
            if p.is_file() and str(p) not in cov:
                b, rel = p.read_bytes(), str(p.relative_to(scan))
                ex = p.suffix in EXEC_SUFFIXES
                unlisted.append({"path": rel, "size": len(b), "sha256": sha256_hex(b), "execution_relevant": ex})
                if ex:
                    hold.append(f"{label}/{rel}")
        report["observations"][label] = {
            "scanned": str(scan), "files_not_in_any_record": len(unlisted), "unlisted": unlisted,
            "note": "관측 — rc 판정에 쓰지 않는다 (옛 세대에 같은 관측이 없어 기준이 없다). 실행 경로 관련 (" + " ".join(EXEC_SUFFIXES)
                    + ") 은 adoption_hold 로 올린다 — 결과 검토에서 처분하고, 일반 잉여 파일로 묵인하지 않는다"}
    report["adoption_hold"] = bool(hold)
    report["adoption_hold_reasons"] = hold
    used = {(k.split("/", 1)[1], c["path"]) for k, r in report["dists"].items() for c in r["changed_rows"] if c["kind"] == "declared"}
    missing = sorted(set(declared) - used)
    if missing:
        report["problems"].append(f"선언된 차이가 실제로 나타나지 않음 {missing} (선언과 관측이 다르다)")
    report["wrapper_rows_changed"] = sum(1 for r in report["dists"].values() for c in r["changed_rows"] if c["kind"] == "wrapper")
    report["dists_with_changed_rows"] = sorted(k for k, r in report["dists"].items() if r["changed_rows"])
    return report


# ── ensurepip 묶음 · 내려받은 wheel ───────────────────────────────────────────

def bundled(*, bundled_dir: Path, old_sci: Path, expect: dict, declared: dict) -> dict:
    rep = {"wheels": {}, "problems": []}
    names = sorted(p.name for p in bundled_dir.iterdir())
    if names != sorted(expect):
        rep["problems"].append(f"묶음 파일 집합이 다름 {names}")
    for name in sorted(set(names) & set(expect)):
        p, want = bundled_dir / name, expect[name]
        size, sha = file_digest(p)
        w = {"size": size, "sha256": sha, "equals_october_sha256": sha == want["oct_sha256"]}
        if (size, sha) != (want["size"], want["sha256"]):
            rep["problems"].append(f"{name}: 크기 · sha256 이 고정값과 다름 ({size} · {sha})")
        key = want["old_record"]
        with zipfile.ZipFile(p) as z:
            members = z.namelist()
            if len(members) != len(set(members)):
                rep["problems"].append(f"{name}: 같은 이름의 구성원이 둘 이상")
            recs = [m for m in members if re.fullmatch(r"[^/]+\.dist-info/RECORD", m)]
            if len(recs) != 1:
                rep["problems"].append(f"{name}: RECORD 가 하나가 아님 {recs}")
                rep["wheels"][name] = w
                continue
            w_rows, _, wq = parse_record(z.read(recs[0]))
            rep["problems"] += [f"{name}: wheel RECORD {x}" for x in wq]
            listed = {r[0]: r for r in w_rows}
            if set(listed) != set(members):
                rep["problems"].append(f"{name}: 구성원 ↔ wheel RECORD 집합 다름")
            for m in members:
                if m == recs[0] or m not in listed:
                    continue
                b = z.read(m)
                if (record_hash(b), str(len(b))) != listed[m][1:]:
                    rep["problems"].append(f"{name}: 구성원 {m} 가 wheel 자신의 RECORD 와 다름")
        o_rows, _, oq = parse_record((old_sci / key).read_bytes())
        rep["problems"] += [f"{name}: 옛 설치 RECORD {x}" for x in oq]
        o = {r[0]: r for r in o_rows}
        own = recs[0].split("/")[0]
        diff = []
        for path, r in listed.items():
            if path == recs[0]:
                continue
            if path not in o:
                rep["problems"].append(f"{name}: wheel 행 {path} 이 옛 설치 RECORD 에 없음")
            elif o[path] != r:
                want_d = declared.get((key, path))
                if want_d and o[path][1:] == want_d[0] and r[1:] == want_d[1]:
                    diff.append({"path": path, "old": list(o[path][1:]), "new": list(r[1:]), "declared": True})
                else:
                    rep["problems"].append(f"{name}: 구성원 {path} 가 옛 설치 RECORD 와 다름 (선언 밖)")
        for path, r in o.items():                     # 옛 설치에만 있는 행 = pip 가 만든 것뿐이어야 한다
            if path in listed:
                continue
            ok = (path.startswith(WRAPPER_PREFIX["venv"]) or path in (f"{own}/INSTALLER", f"{own}/REQUESTED", f"{own}/RECORD")
                  or (not r[1] and path.endswith(".pyc") and "/__pycache__/" in "/" + path))
            if not ok:
                rep["problems"].append(f"{name}: 옛 설치 RECORD 에만 있는 행이 pip 생성 범주가 아님 {path}")
        used = {k[1] for k in declared if k[0] == key}
        if used - {d["path"] for d in diff}:
            rep["problems"].append(f"{name}: 선언된 차이가 wheel 에 없음 {sorted(used - {d['path'] for d in diff})}")
        w["members_differing_from_october_install"] = diff
        rep["wheels"][name] = w
    return rep


def wheels(*, wheel_dir: Path, expect_json: Path) -> dict:
    exp = json.loads(expect_json.read_text(encoding="utf-8"))
    rep = {"dir": str(wheel_dir), "expect": str(expect_json), "expect_sha256": sha256_hex(expect_json.read_bytes()), "problems": []}
    if exp.get("ok") is not True or exp.get("problems"):
        rep["problems"].append("기대 기록 자체가 ok 가 아니다")
    want = {f["name"]: (f["size"], f["sha256"]) for f in exp["files"]}
    if len(want) != len(exp["files"]):
        rep["problems"].append("기대 기록에 같은 이름이 둘 이상")
    entries = sorted(wheel_dir.iterdir())
    if any(not p.is_file() for p in entries):
        rep["problems"].append(f"파일 아닌 항목 {[p.name for p in entries if not p.is_file()]}")
    got = {p.name: file_digest(p) for p in entries if p.is_file()}
    rep["files"] = [{"name": n, "size": s, "sha256": h} for n, (s, h) in sorted(got.items())]
    if sorted(got) != sorted(want):
        rep["problems"].append(f"이름 집합 다름 — 기대에만 {sorted(set(want) - set(got))} · 받은 것에만 {sorted(set(got) - set(want))}")
    rep["problems"] += [f"{n}: 크기 · sha256 다름 (기대 {want[n]} · 받음 {got[n]})" for n in sorted(set(got) & set(want)) if got[n] != want[n]]
    rep["n_files"] = len(got)
    return rep


# ── 봉인 ─────────────────────────────────────────────────────────────────────

def expected_lock(old: bytes, *, old_records: Path, new_records: Path, py_old: str, py_new: str) -> tuple[bytes | None, list, list]:
    """옛 lock 에서 정해진 자리만 바꾼 기대 바이트 — python 줄 하나 · RECORD 가 바뀐 배포판의 record-sha256 칸.
    옛 lock 의 record-sha256 은 옛 RECORD 원문의 text_sha 와 같아야 한다 (옛 결속). 그 밖의 줄은 한 바이트도 바꾸지 않는다."""
    P, changed = [], []
    lines = old.decode("utf-8").split("\n")
    py_line = f"#@ python {json.dumps(py_old)}"
    idx = [i for i, ln in enumerate(lines) if ln == py_line]
    if len(idx) != 1:
        return None, [f"옛 lock 에 {py_line!r} 줄이 정확히 하나가 아님"], []
    lines[idx[0]] = f"#@ python {json.dumps(py_new)}"
    for i, ln in enumerate(lines):
        m = _DIST.fullmatch(ln)
        if not m:
            continue
        key = f"{m['name']}-{m['version']}.RECORD"
        if not (old_records / key).is_file() or not (new_records / key).is_file():
            P.append(f"{key}: 옛 · 새 RECORD 원문이 둘 다 있어야 한다")
            continue
        if text_sha((old_records / key).read_bytes()) != m["record"]:
            P.append(f"{key}: 옛 lock 의 record-sha256 이 옛 원문과 결속되지 않음")
        new_sha = text_sha((new_records / key).read_bytes())
        if new_sha != m["record"]:
            lines[i] = f"{m['name']}=={m['version']}  # record-sha256 {new_sha}"
            changed.append(m["name"])
    return "\n".join(lines).encode("utf-8"), P, changed


def seal(*, old: Path, new: Path, old_records: Path, new_records: Path, py_old: tuple, py_new: tuple, records_report: Path) -> dict:
    """v2 (검토 §137 Q3): seal 은 S9a (records) 가 허용만으로 끝나고 그 보고의 원문 sha 와 보존 RECORD 가 같을 때만 RECORD 를 받는다 —
    seal 단독 통과를 RECORD 수용으로 쓰지 않는다."""
    rep = {"old": str(old), "new": str(new), "files": {}, "problems": []}
    rr_bytes = Path(records_report).read_bytes()
    rr = json.loads(rr_bytes.decode("utf-8"))
    rep["records_report_sha256"] = sha256_hex(rr_bytes)
    if rr.get("allowed_only") is not True:
        rep["problems"].append("S9a 가 허용만이 아니다 — seal 대조를 RECORD 수용으로 쓰지 않는다")
    want = {k.split("/", 1)[1]: v.get("new_raw_sha256") for k, v in rr.get("dists", {}).items() if k.startswith("science/")}
    got = {p.name: sha256_hex(p.read_bytes()) for p in sorted(Path(new_records).iterdir())}
    if want != got:
        bad = sorted(k for k in set(want) | set(got) if want.get(k) != got.get(k))
        rep["problems"].append(f"보존 RECORD 가 S9a 보고와 다름 — {bad[:5]}")
    for d, side in ((old, "옛"), (new, "새")):
        names = sorted(p.name for p in d.iterdir())
        if names != sorted(SEAL_FILES):
            rep["problems"].append(f"{side} 봉인 파일 집합이 11 개 고정 목록과 다름: {names}")
    if rep["problems"]:
        return rep
    rd = {n: (old / n).read_bytes() for n in SEAL_FILES}
    nd = {n: (new / n).read_bytes() for n in SEAL_FILES}
    exp = {}
    lock, lp, rep["lock_record_sha_changed"] = expected_lock(rd["REIL_C6.lock.txt"], old_records=old_records,
                                                             new_records=new_records, py_old=py_old[0], py_new=py_new[0])
    rep["problems"] += lp
    exp["REIL_C6.lock.txt"] = lock
    prof = json.loads(rd["PROFILE.json"].decode("utf-8"))
    if dump_json(prof).encode("utf-8") != rd["PROFILE.json"]:
        rep["problems"].append("옛 PROFILE 이 같은 직렬화로 되돌아오지 않는다")
    if prof.get("python", {}).get("version") != py_old[0] or prof.get("python", {}).get("build") != py_old[1]:
        rep["problems"].append("옛 PROFILE 의 python 판 · 빌드가 고정값과 다름")
    prof["python"]["version"], prof["python"]["build"] = py_new[0], list(py_new[1])
    exp["PROFILE.json"] = dump_json(prof).encode("utf-8")
    for n in SEAL_FILES:
        if n not in ("REIL_C6.lock.txt", "PROFILE.json", "MANIFEST.json"):
            exp[n] = rd[n]
    man = json.loads(rd["MANIFEST.json"].decode("utf-8"))
    if dump_json(man).encode("utf-8") != rd["MANIFEST.json"] or sorted(man) != sorted(set(SEAL_FILES) - {"MANIFEST.json"}):
        rep["problems"].append("옛 MANIFEST 의 직렬화 · 항목 집합이 고정값과 다름")
    if any(man.get(n) != sha256_hex(rd[n]) for n in man):
        rep["problems"].append("옛 MANIFEST 가 옛 파일들과 맞지 않음")
    if exp["REIL_C6.lock.txt"] is not None:
        man.update({n: sha256_hex(exp[n]) for n in ("REIL_C6.lock.txt", "PROFILE.json")})
        exp["MANIFEST.json"] = dump_json(man).encode("utf-8")
    for n in SEAL_FILES:
        e = exp.get(n)
        same = e is not None and nd[n] == e
        rep["files"][n] = {"old_sha256": sha256_hex(rd[n]), "new_sha256": sha256_hex(nd[n]),
                           "expected_sha256": None if e is None else sha256_hex(e), "equals_expected": same,
                           "byte_identical_to_old": nd[n] == rd[n]}
        if not same:
            rep["problems"].append(f"{n}: 기대 바이트와 다름")
    new_man = json.loads(nd["MANIFEST.json"].decode("utf-8")) if nd["MANIFEST.json"] else {}
    if any(new_man.get(n) != sha256_hex(nd[n]) for n in set(SEAL_FILES) - {"MANIFEST.json"}):
        rep["problems"].append("새 MANIFEST 가 새 파일들과 맞지 않음")
    return rep


# ── CLI (요청서 §2 의 argv) ────────────────────────────────────────────────────

def _write_new(path: Path, obj) -> None:
    if path.exists():
        raise UsageError(f"이미 있다 — 덮어쓰지 않는다: {path}")
    path.write_text(dump_json(obj), encoding="utf-8")


def _new_dir(path: Path | None) -> Path | None:
    if path is None:
        return None
    if path.exists():
        raise UsageError(f"이미 있다 — 덮어쓰지 않는다: {path}")
    path.mkdir()
    return path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="mode", required=True)
    b = sub.add_parser("bundled")
    b.add_argument("--bundled", required=True, type=Path)
    w = sub.add_parser("wheels")
    w.add_argument("--wheels", required=True, type=Path)
    w.add_argument("--expect", required=True, type=Path)
    r = sub.add_parser("records")
    r.add_argument("--venv", required=True, type=Path)
    r.add_argument("--target", required=True, type=Path)
    r.add_argument("--records-out", required=True, type=Path)
    r.add_argument("--test-records-out", required=True, type=Path)
    s = sub.add_parser("seal")
    s.add_argument("--new", required=True, type=Path)
    s.add_argument("--new-records", required=True, type=Path)
    s.add_argument("--records-report", required=True, type=Path)
    for x in (b, w, r, s):
        x.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    repo = Path(__file__).resolve().parents[2]
    old_sci, old_test = repo / OLD_E / "09_records", repo / OLD_E / "10_test_tool_records"
    try:
        if a.out.exists():
            raise UsageError(f"이미 있다 — 덮어쓰지 않는다: {a.out}")
        if a.mode == "bundled":
            rep = bundled(bundled_dir=a.bundled, old_sci=old_sci, expect=BUNDLED, declared=DECLARED)
        elif a.mode == "wheels":
            rep = wheels(wheel_dir=a.wheels, expect_json=a.expect)
        elif a.mode == "records":
            if (os.path.normpath(a.venv), os.path.normpath(a.target)) != (NEW_VENV, NEW_TARGET):
                raise UsageError(f"--venv · --target 는 고정 경로 {NEW_VENV} · {NEW_TARGET} 여야 한다")
            rep = records(venv=a.venv, target=a.target, old_sci=old_sci, old_test=old_test, old_bin=OLD_VENV + "/bin",
                          new_bin=NEW_VENV + "/bin", declared=DECLARED, collisions=COLLISIONS,
                          sci_out=_new_dir(a.records_out), test_out=_new_dir(a.test_records_out))
        else:
            rep = seal(old=repo / OLD_SEAL, new=a.new, old_records=old_sci, new_records=a.new_records, py_old=PY_OLD, py_new=PY_NEW,
                       records_report=a.records_report)
    except UsageError as exc:
        print(f"사용 오류: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:                      # 도구 자신의 오류는 '미허용 (1)' 과 섞지 않는다
        print(f"도구 오류: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3
    rep["mode"], rep["tool_sha256"] = a.mode, sha256_hex(Path(__file__).read_bytes())
    rep["allowed_only"] = not rep["problems"]
    _write_new(a.out, rep)
    print(f"{a.mode}: {'allowed_only' if rep['allowed_only'] else 'NOT ALLOWED'} · 문제 {len(rep['problems'])}")
    for x in rep["problems"][:40]:
        print(" -", x)
    return 0 if rep["allowed_only"] else 1


if __name__ == "__main__":
    sys.exit(main())
