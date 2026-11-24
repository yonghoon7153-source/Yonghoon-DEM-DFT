"""env_profile.py — 프로필 C (현재 검증 환경의 정확 고정) 의 측정 · lock · 대조. **기록 전용.**

★ 90차 (원장 §135 · 고정 표 `docs/22p_gap/PYBAMM_PIN_ROUND_SPEC.md` §3–§5) — 사전 검토 회신 P3: 지금은 "무엇으로
  돌렸나" 는 기록되지만 (`src/io.py::env_fingerprint` · effective_solver · worker 서명 대조) "그 환경이 승인된 것인가" 를
  묻는 곳이 없었다. 이 모듈은 실행 환경을 `requirements-validation-C.lock.txt` 와 대조해 **일치 / 불일치 목록을 남긴다.**
  어떤 실행도 막지 않는다 (D3 — 불일치여도 pytest · smoke · run.sh · 영수증 생성은 그대로 돈다). C 일치 여부는 실행 gate 가
  아니나, 측정 기능을 요구하는 회귀의 지원 환경에서는 측정 불가를 시험 실패로 본다 (e06 · e08 — 91차 C1).

  · 측정은 그 프로세스의 `sys.path` 순서 그대로다 — 해석기 · 플랫폼 다섯 축 · 배포판 (정규 이름의 첫 항목 = 유효 · 뒤 항목 =
    가려진 것 · RECORD 텍스트 sha256) · 설치 파일의 RECORD 재해시 (설치 뒤 변경 감지 — RECORD 가 덮는 범위만) · 핵심
    module 열 개를 `PathFinder` 로 경로 검색한 origin 파일의 RECORD 소속 (사전 검토 Q5 를 좁힌 꼴).
  · 그 origin 은 **경로 검색 결과**다 — 이미 로드된 module 객체 (`sys.modules`) · 그 `__file__` / `__spec__.origin` · 다른
    meta-path finder 의 선택은 보지 않는다. 로드된 module origin 은 측정하지 않는다 (결과 `not_measured` · 91차 G90-N1).
  · 결과는 닫힌 dict 다. `MATCH` · `MISMATCH` · `UNMEASURED` — 측정하지 못한 칸은 `None` 이다. 빈 목록으로 쓰면
    "불일치 없음" 으로 읽힌다 (61차 P1-3). `UNMEASURED` 를 `MATCH` 로 적지 않는다.
  · 선언하지 않는 것: C 는 정본 (v4) 생산 환경이 아니다 (그것은 프로필 B — 고정 표 §6 의 기록) · 설치 처방이 아니다 ·
    다른 기계에 강제하지 않는다.

사용 (프로젝트 root 에서 — 계산 진입점 `python -m src.*` 과 같은 sys.path):
    python -m tools.env_profile                 # 대조 요약 (rc 0 — 세 상태 모두)
    python -m tools.env_profile --json          # 결과 dict
    python -m tools.env_profile --emit-lock     # 지금 환경의 정규형 lock (측정 실패면 rc 1 · 부분 lock 없음)
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib
import importlib.machinery
import importlib.metadata as md
import json
import os
import platform
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK_DEFAULT = ROOT / "requirements-validation-C.lock.txt"

#: `src/io.py::env_fingerprint()` 의 module 축 — 순서까지 같다 (e07 이 대조한다).
KEY_MODULES = ("numpy", "scipy", "pandas", "joblib", "pyarrow", "pybamm", "matplotlib", "yaml",
               "pybammsolvers", "casadi")
#: lock 지시 — 이 순서로 쓰고, 각각 정확히 한 번 있어야 한다.
DIRECTIVES = ("profile", "python", "implementation", "system", "machine", "libc")
#: 결과 `mismatches[].axis` 의 닫힌 집합 (고정 표 §4-2 · 91차 §13-3 — `origin` → `path_origin`).
AXES = ("python", "implementation", "system", "machine", "libc", "dist_missing", "dist_extra",
        "dist_version", "dist_record", "shadowed", "file", "path_origin")
#: 이 도구가 재지 않는 것 — 결과 `not_measured` 로 세 상태 모두 그대로 싣는다 (측정 칸이 아니라 범위 선언 · 91차 G90-N1).
NOT_MEASURED = ("loaded_module_origin",)

_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_VERSION = re.compile(r"[^\s#]+")
_HEX64 = re.compile(r"[0-9a-f]{64}")
_DIRECTIVE = re.compile(r"#@ (?P<key>[a-z]+) (?P<value>.+)")
_SHADOW = re.compile(r"#@ shadowed (?P<name>[^=\s#]+)==(?P<version>[^\s#]+) record-sha256 (?P<record>\S+)")
_DIST = re.compile(r"(?P<name>[^=\s#]+)==(?P<version>[^\s#]+)  # record-sha256 (?P<record>\S+)")

#: `emit_lock` 이 쓰는 머리 주석 (정규형의 일부 — 바꾸면 커밋된 lock 도 다시 낸다).
HEADER = (
    "# requirements-validation-C.lock.txt — 프로필 C: 현재 검증 환경의 정확 고정 (기록 대조 전용)",
    "#",
    "# ★ 90차 (원장 §135 · 고정 표 docs/22p_gap/PYBAMM_PIN_ROUND_SPEC.md §3) — `python -m tools.env_profile --emit-lock` 의",
    "#   출력 그대로다. 손으로 고치지 않는다 (정규형 고정점: emit_lock(parse_lock(text)) == text).",
    "# 대조: `python -m tools.env_profile` (smoke 로그 · 영수증 stamp `environment_profile_C`). 불일치여도 아무것도 막지 않는다.",
    "# 선언하지 않는 것: 정본 (v4) 생산 환경 (그것은 프로필 B — 고정 표 §6 의 기록) · C 로 만든 수치가 B 의 수치와 같다는 것 ·",
    "#   설치 처방 (리눅스 시스템 배포판을 담는다 — `pip install -r` 용이 아니다) · 다른 기계에 강제하는 것.",
    "# 문법 (닫힘): `#@ <지시> <JSON 문자열>` · `<이름>==<버전>  # record-sha256 <hex64|none>` (PEP 503 이름 · 엄격 오름차순) ·",
    "#   `#@ shadowed <이름>==<버전> record-sha256 <hex64|none>` (경로 순서로 가려진 항목). record-sha256 = 설치된 RECORD",
    "#   텍스트의 sha256 (none = RECORD 없음 — 설치 파일 대조 불가).",
)


class LockFormatError(ValueError):
    """lock 이 닫힌 문법 밖이다."""


def normalize(name: str) -> str:
    """PEP 503 정규 이름."""
    return re.sub(r"[-_.]+", "-", name).lower()


# ── 측정 ──────────────────────────────────────────────────────────────────────

def _verify_files(dist) -> tuple[int, int, list]:
    """RECORD 의 해시 있는 항목을 다시 해시한다 → (일치 수, 해시 없는 수, [(상대경로, 기대, 관측 | None)]).

    없는 파일은 불일치다 (관측 `None`). 그 밖의 읽기 오류 · 모르는 해시 알고리즘은 **측정 실패**로 올린다 —
    파일 하나를 못 읽은 것을 "그 파일은 맞다" 로도 "다르다" 로도 적지 않는다.
    """
    ok, unhashed, bad = 0, 0, []
    for f in dist.files or ():
        if f.hash is None:
            unhashed += 1
            continue
        h = hashlib.new(f.hash.mode)                     # 모르는 알고리즘 → ValueError (측정 실패)
        want = f"{f.hash.mode}={f.hash.value}"
        try:
            with open(f.locate(), "rb") as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b""):
                    h.update(chunk)
        except FileNotFoundError:
            bad.append((str(f), want, None))
            continue
        got = base64.urlsafe_b64encode(h.digest()).rstrip(b"=").decode()
        if got == f.hash.value:
            ok += 1
        else:
            bad.append((str(f), want, f"{f.hash.mode}={got}"))
    return ok, unhashed, bad


def _origin(module: str, paths: list, effective: dict, files: dict, no_record: list):
    """핵심 module 을 `PathFinder.find_spec(module, paths)` 로 경로 검색한 origin 파일의 RECORD 소속
    → ("in_record", 주인) · ("unverifiable", origin) · ("mismatch", 관측).

    이미 로드된 module 객체 (`sys.modules`) · 다른 meta-path finder 는 보지 않는다 (91차 G90-N1 — 결과 `not_measured`).
    """
    spec = importlib.machinery.PathFinder.find_spec(module, paths)
    origin = getattr(spec, "origin", None) if spec is not None else None
    if spec is None:
        return "mismatch", "<not found>"
    if not origin or not os.path.isfile(origin):
        return "mismatch", f"<{origin or 'namespace'}>"
    real = os.path.realpath(origin)
    owners = sorted(
        name for name, entries in files.items()
        if any(os.path.realpath(f.locate()) == real for f in entries
               if f.parts and f.parts[0].split(".")[0] == module))
    if len(owners) == 1:
        return "in_record", owners[0]
    if not owners:
        for name in no_record:
            base = os.path.realpath(effective[name].locate_file(""))
            if os.path.commonpath([base, real]) == base:
                return "unverifiable", real
    return "mismatch", real if not owners else f"{real} (주인 {', '.join(owners)})"


def measure(paths=None) -> dict:
    """그 프로세스의 `sys.path` (또는 주어진 경로 목록) 순서로 환경을 잰다. 실패는 예외로 올린다."""
    importlib.invalidate_caches()
    paths = [str(p) for p in (sys.path if paths is None else paths)]
    effective, meta, shadowed = {}, {}, []
    for entry in paths:
        for dist in md.distributions(path=[entry]):
            raw, version = dist.metadata["Name"], dist.version
            if not raw or not version:
                raise ValueError(f"이름 · 버전 없는 배포판 메타데이터 ({entry})")
            name = normalize(raw)
            if not _NAME.fullmatch(name) or not _VERSION.fullmatch(version):
                raise ValueError(f"lock 에 쓸 수 없는 배포판 이름 · 버전: {raw!r} {version!r} ({entry})")
            record = dist.read_text("RECORD")
            digest = "none" if record is None else hashlib.sha256(record.encode("utf-8")).hexdigest()
            if name in effective:
                shadowed.append((name, version, digest))
            else:
                effective[name], meta[name] = dist, (version, digest)
    dists, files, no_record = {}, {}, []
    verified = unhashed = 0
    file_bad = []
    for name in sorted(effective):
        version, digest = meta[name]
        dists[name] = {"version": version, "record": digest}
        if digest == "none":
            no_record.append(name)
            continue
        files[name] = list(effective[name].files or ())
        ok, un, bad = _verify_files(effective[name])
        verified += ok
        unhashed += un
        file_bad += [(name, rel, want, got) for rel, want, got in bad]
    origins, origin_unverifiable, origin_bad = {}, [], []
    for module in KEY_MODULES:
        kind, value = _origin(module, paths, effective, files, no_record)
        if kind == "in_record":
            origins[module] = value
        elif kind == "unverifiable":
            origin_unverifiable.append(module)
        else:
            origin_bad.append((module, value))
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "system": platform.system(),
        "machine": platform.machine(),
        "libc": " ".join(platform.libc_ver()).strip(),
        "dists": dists,
        "shadowed": sorted(shadowed),
        "dists_without_record": no_record,
        "files": {"verified": verified, "unhashed": unhashed, "mismatches": file_bad},
        "path_origins": {"in_record": origins, "unverifiable": origin_unverifiable, "mismatches": origin_bad},
    }


# ── lock ─────────────────────────────────────────────────────────────────────

def emit_lock(profile: dict) -> str:
    """정규형 lock 텍스트 — `measure()` 나 `parse_lock()` 의 결과에서."""
    lines = list(HEADER)
    lines += [f"#@ {k} {json.dumps('C' if k == 'profile' else profile[k], ensure_ascii=False)}" for k in DIRECTIVES]
    lines.append("")
    lines += [f"{n}=={d['version']}  # record-sha256 {d['record']}" for n, d in sorted(profile["dists"].items())]
    if profile["shadowed"]:
        lines.append("")
        lines += [f"#@ shadowed {n}=={v} record-sha256 {r}" for n, v, r in sorted(profile["shadowed"])]
    return "\n".join(lines) + "\n"


def parse_lock(text: str) -> dict:
    """닫힌 문법 (고정 표 §3-1) 으로 읽는다. 어긋나면 `LockFormatError` (줄 번호를 담는다)."""
    seen, dists, shadowed = {}, {}, []
    last, last_shadow = None, None

    def bad(no: int, why: str) -> LockFormatError:
        return LockFormatError(f"줄 {no}: {why}")

    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    for no, line in enumerate(lines, 1):
        if line == "" or (line.startswith("#") and not line.startswith("#@")):
            continue
        if line.startswith("#@ shadowed "):
            m = _SHADOW.fullmatch(line)
            if m is None:
                raise bad(no, "가려진 항목의 꼴이 아니다")
            key = (m["name"], m["version"], m["record"])
            if not _NAME.fullmatch(key[0]):
                raise bad(no, f"정규형 아닌 이름 {key[0]!r}")
            if key[2] != "none" and not _HEX64.fullmatch(key[2]):
                raise bad(no, f"record-sha256 칸 {key[2]!r}")
            if last_shadow is not None and key < last_shadow:
                raise bad(no, "가려진 항목의 정렬이 어긋났다")
            shadowed.append(key)
            last_shadow = key
            continue
        if line.startswith("#@"):
            m = _DIRECTIVE.fullmatch(line)
            if m is None or m["key"] not in DIRECTIVES:
                raise bad(no, f"모르는 지시 {line!r}")
            if m["key"] in seen:
                raise bad(no, f"지시 {m['key']} 가 두 번 있다")
            try:
                value = json.loads(m["value"])
            except ValueError as exc:
                raise bad(no, f"지시 {m['key']} 의 값이 JSON 이 아니다 ({exc})") from exc
            if not isinstance(value, str):
                raise bad(no, f"지시 {m['key']} 의 값이 문자열이 아니다")
            if m["key"] == "profile" and value != "C":
                raise bad(no, f"profile 이 C 가 아니다 ({value!r})")
            seen[m["key"]] = value
            continue
        m = _DIST.fullmatch(line)
        if m is None:
            raise bad(no, f"모르는 줄 {line[:80]!r}")
        name, version, record = m["name"], m["version"], m["record"]
        if not _NAME.fullmatch(name):
            raise bad(no, f"정규형 아닌 이름 {name!r}")
        if record != "none" and not _HEX64.fullmatch(record):
            raise bad(no, f"record-sha256 칸 {record!r}")
        if last is not None and name <= last:
            raise bad(no, f"배포판 정렬 · 중복 ({last!r} 다음 {name!r})")
        dists[name] = {"version": version, "record": record}
        last = name
    missing = [k for k in DIRECTIVES if k not in seen]
    if missing:
        raise LockFormatError(f"지시가 없다: {', '.join(missing)}")
    out = {k: seen[k] for k in DIRECTIVES}
    out.update(dists=dists, shadowed=shadowed)
    return out


# ── 대조 ─────────────────────────────────────────────────────────────────────

def _mm(axis: str, subject: str, locked, measured) -> dict:
    return {"axis": axis, "subject": subject, "locked": locked, "measured": measured}


def compare(locked: dict, measured: dict) -> list:
    """축마다 다른 것을 모은다 → (axis, subject) 순 목록. 빈 목록 = 비교한 모든 축이 같다."""
    out = []
    for k in DIRECTIVES[1:]:
        if locked[k] != measured[k]:
            out.append(_mm(k, k, locked[k], measured[k]))
    lock_d, got_d = locked["dists"], measured["dists"]
    for n in sorted(lock_d.keys() - got_d.keys()):
        out.append(_mm("dist_missing", n, lock_d[n]["version"], None))
    for n in sorted(got_d.keys() - lock_d.keys()):
        out.append(_mm("dist_extra", n, None, got_d[n]["version"]))
    for n in sorted(lock_d.keys() & got_d.keys()):
        if lock_d[n]["version"] != got_d[n]["version"]:
            out.append(_mm("dist_version", n, lock_d[n]["version"], got_d[n]["version"]))
        if lock_d[n]["record"] != got_d[n]["record"]:
            out.append(_mm("dist_record", n, lock_d[n]["record"], got_d[n]["record"]))
    lock_s = Counter(tuple(x) for x in locked["shadowed"])
    got_s = Counter(tuple(x) for x in measured["shadowed"])
    for n, v, r in sorted((lock_s - got_s).elements()):
        out.append(_mm("shadowed", f"{n}=={v}", r, None))
    for n, v, r in sorted((got_s - lock_s).elements()):
        out.append(_mm("shadowed", f"{n}=={v}", None, r))
    for n, rel, want, got in measured["files"]["mismatches"]:
        out.append(_mm("file", f"{n}:{rel}", want, got))
    for module, seen in measured["path_origins"]["mismatches"]:
        out.append(_mm("path_origin", module, "경로 검색 origin 이 RECORD 가 있는 유효 배포판 하나의 파일", seen))
    return sorted(out, key=lambda x: (x["axis"], x["subject"]))


def _display(path: Path) -> str:
    p = path.resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def compare_lock(lock_path=None, *, paths=None) -> dict:
    """lock 과 지금 환경을 대조한 닫힌 결과 dict (고정 표 §4-2 · §13-3). 예외를 내지 않는다 — 못 하면 `UNMEASURED`.

    `not_measured` 는 측정 칸이 아니라 범위 선언이라 세 상태 모두 같은 값이다 (`UNMEASURED` 에서도 `None` 이 아니다).
    """
    lp = Path(LOCK_DEFAULT if lock_path is None else lock_path)
    res = {"profile": "C", "lock_path": _display(lp), "lock_sha256": None, "status": "UNMEASURED",
           "reason": "", "mismatches": None, "unverifiable": None, "counts": None,
           "not_measured": list(NOT_MEASURED)}
    try:
        raw = lp.read_bytes()
    except OSError as exc:
        res["reason"] = f"lock 을 읽지 못했다: {exc}"
        return res
    res["lock_sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        locked = parse_lock(raw.decode("utf-8"))
    except UnicodeDecodeError as exc:
        res["reason"] = f"lock 이 UTF-8 이 아니다: {exc}"
        return res
    except LockFormatError as exc:
        res["reason"] = f"lock 형식 오류 — {exc}"
        return res
    try:
        measured = measure(paths)
    except Exception as exc:                              # noqa: BLE001 — 측정 실패는 typed UNMEASURED 다
        res["reason"] = f"측정 실패: {exc!r}"
        return res
    found = compare(locked, measured)
    res.update(
        status="MISMATCH" if found else "MATCH",
        mismatches=found,
        unverifiable={"dists_without_record": list(measured["dists_without_record"]),
                      "path_origins": list(measured["path_origins"]["unverifiable"])},
        counts={"dists_locked": len(locked["dists"]), "dists_measured": len(measured["dists"]),
                "shadowed_locked": len(locked["shadowed"]), "shadowed_measured": len(measured["shadowed"]),
                "files_verified": measured["files"]["verified"], "files_unhashed": measured["files"]["unhashed"],
                "path_origins_in_record": len(measured["path_origins"]["in_record"])})
    return res


# ── CLI ──────────────────────────────────────────────────────────────────────

def _summary(r: dict) -> str:
    head = f"환경 프로필 C 대조: {r['status']} · lock {r['lock_path']}"
    if r["lock_sha256"]:
        head += f" (sha256 {r['lock_sha256'][:16]}…)"
    if r["status"] == "UNMEASURED":
        return head + f"\n  이유: {r['reason']}\n  (기록 전용 — 아무것도 막지 않는다 · 원장 §135)"
    c = r["counts"]
    lines = [head + f" · 배포판 lock {c['dists_locked']} / 측정 {c['dists_measured']} · 가려진 {c['shadowed_locked']}"
             f" / {c['shadowed_measured']} · 설치 파일 일치 {c['files_verified']} (해시 없음 {c['files_unhashed']})"
             f" · 경로 검색 origin 의 RECORD 소속 {c['path_origins_in_record']} (로드된 module origin 미측정)"]
    u = r["unverifiable"]
    if u["dists_without_record"]:
        lines.append(f"  · 확인 불가 — RECORD 없는 배포판 {len(u['dists_without_record'])}: "
                     + ", ".join(u["dists_without_record"]))
    if u["path_origins"]:
        lines.append("  · 확인 불가 — 경로 검색 origin: " + ", ".join(u["path_origins"]))
    for m in r["mismatches"]:
        lines.append(f"  ✗ {m['axis']} {m['subject']} locked={m['locked']} measured={m['measured']}")
    lines.append("  (기록 전용 — 불일치여도 아무것도 막지 않는다 · 원장 §135)")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m tools.env_profile",
                                 description="실행 환경 ↔ 프로필 C lock 대조 (기록 전용 · 원장 §135)")
    ap.add_argument("--lock", default=None, help="대조할 lock (기본: 프로젝트 root 의 requirements-validation-C.lock.txt)")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--json", action="store_true", help="결과 dict 를 JSON 으로")
    mode.add_argument("--emit-lock", action="store_true", help="지금 환경의 정규형 lock 을 낸다")
    a = ap.parse_args(argv)
    if a.emit_lock:
        if a.lock is not None:
            ap.error("--emit-lock 은 --lock 과 함께 쓰지 않는다")
        try:
            text = emit_lock(measure())
        except Exception as exc:                          # noqa: BLE001
            print(f"✗ 측정 실패 — lock 을 내지 않는다: {exc!r}", file=sys.stderr)
            return 1
        sys.stdout.buffer.write(text.encode("utf-8"))
        sys.stdout.flush()
        return 0
    r = compare_lock(a.lock)
    if a.json:
        sys.stdout.buffer.write((json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
        sys.stdout.flush()
        return 0
    try:
        sys.stdout.reconfigure(errors="backslashreplace")
    except Exception:                                     # noqa: BLE001 — 출력 장치가 바꿀 수 없는 경우
        pass
    print(_summary(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
