"""REIL C4-ENV — 새 환경 세대의 내려받기 식별과 old→new 대조 (`docs/REIL_C4_ENV_APPROVAL_REQUEST_20261013.md` §1-8 · §2 S4 · S9).

읽기 · 해시만 한다. stdlib 만 쓰고 과학 패키지를 import 하지 않는다 — venv 가 아니라 시스템 python 으로 실행한다.

    /usr/bin/python3.11 -I bms-balancing/scripts/reil_c4_env_compare.py artifacts --wheels <dir> (--expect-log <P0 설치 stdout> | --expect-dists 이름==판,…) --out <json>
    /usr/bin/python3.11 -I bms-balancing/scripts/reil_c4_env_compare.py compare --old <옛 봉인> --new <새 봉인> --venv <venv 절대 경로>
        --wheels <dir> [--wheels <dir> …] --python-version <판> --python-build '<빌드 이름>|<빌드 시각>' --records-out <dir> --out <json>

허용 차이 밖이면 rc 1 이다. 채택 판단은 하지 않는다 — 허용 차이만 있어도 새 봉인은 검토 수용 전까지 C4 환경이 아니다.
허용하는 것 (요청문 §1-8 그대로): lock 의 `#@ python` 한 줄 · 콘솔 스크립트 (`../../../bin/`) 가 있는 배포판의 RECORD sha · PROFILE 의
`python.version` · `python.build` 두 값 · 그 결과인 MANIFEST 두 항목. RECORD sha 차이는 RECORD 행을 wheel 안 RECORD 와 행 단위로 맞춰
'pip 가 만든 행 (bin · INSTALLER · REQUESTED · 해시 없는 pyc · RECORD) 말고는 wheel 과 같다' 가 보일 때만 허용한다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

#: 봉인 밖 사람용 기록 (`reil_c6_profile.HUMAN_RECORDS` 와 같다 — import 하지 않고 값으로 둔다)
HUMAN_RECORDS = ("README.md", "C6_RUN.log")
LOCK, PROFILE, MANIFEST = "REIL_C6.lock.txt", "PROFILE.json", "MANIFEST.json"
#: P0 설치 로그의 "Using cached X.whl[.metadata]" · "Downloading X.whl[.metadata]"
LOG_WHEEL = re.compile(r"(?:Using cached|Downloading) (\S+?\.whl)(?:\.metadata)?\s")
LOCK_BODY = re.compile(r"^(\S+)==(\S+)  # record-sha256 ([0-9a-f]{64}|none)$")
LOCK_PYTHON = re.compile(r'^#@ python "[^"]*"$')
PIP_MADE = ("INSTALLER", "REQUESTED", "RECORD")


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _norm(name: str) -> str:
    """PEP 503 — `degradation-degeneracy/tools/env_profile.normalize` 와 같은 식 (lock 의 이름과 맞춘다)."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _dump(obj) -> bytes:
    """`reil_c6_profile._dump` 와 같은 직렬화 (+ utf-8) — PROFILE 을 다시 만들어 바이트로 대조하려고."""
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8")


def _write(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")


# ── S4 내려받기 식별 ───────────────────────────────────────────────────────────

def log_wheel_names(text: str) -> list[str]:
    return sorted(set(LOG_WHEEL.findall(text)))


def _wheel_dist(filename: str) -> str:
    name, version = filename.split("-")[:2]
    return f"{_norm(name)}=={version}"


def artifacts(wheels: Path, expected: list[str], by: str = "filename") -> dict:
    """by="filename": 파일 이름 집합이 정확히 같아야 한다 (옛 이름이 기록된 과학 28). by="dist": `이름==판` 집합 (정규 이름) 이 같고
    전부 .whl 이어야 한다 (옛 파일 이름 기록이 없는 시험 도구 — 이름 표기 차이로 헛되이 멈추지 않게)."""
    entries = sorted(wheels.iterdir())
    files = [{"name": p.name, "size": p.stat().st_size, "sha256": _sha(p.read_bytes())} for p in entries if p.is_file()]
    problems = []
    if any(not p.is_file() for p in entries):
        problems.append({"not_a_file": sorted(p.name for p in entries if not p.is_file())})
    if by == "filename":
        got, want = sorted(p.name for p in entries), sorted(expected)
    else:
        if any(not p.name.endswith(".whl") for p in entries):
            problems.append({"not_a_wheel": sorted(p.name for p in entries if not p.name.endswith(".whl"))})
        got = sorted(_wheel_dist(p.name) for p in entries if p.name.endswith(".whl"))
        want = sorted(f"{_norm(e.split('==')[0])}=={e.split('==')[1]}" for e in expected)
    if got != want:
        problems.append({"missing": sorted(set(want) - set(got)), "extra": sorted(set(got) - set(want)),
                         "duplicates": sorted({g for g in got if got.count(g) > 1})})
    return {"dir": str(wheels), "by": by, "expected": want, "files": files, "problems": problems, "ok": not problems}


# ── S9 봉인 파일 대조 ──────────────────────────────────────────────────────────

def lock_diff(old: bytes, new: bytes, version: str) -> dict:
    lo, ln = old.decode("utf-8").splitlines(), new.decode("utf-8").splitlines()
    if len(lo) != len(ln):
        return {"allowed": False, "reason": f"줄 수 다름 {len(lo)} → {len(ln)}", "lines": [], "record_sha_differs": []}
    lines, differs, allowed = [], [], True
    for i, (x, y) in enumerate(zip(lo, ln), 1):
        if x == y:
            continue
        mx, my = LOCK_BODY.match(x), LOCK_BODY.match(y)
        if LOCK_PYTHON.match(x) and y == f"#@ python {json.dumps(version)}":
            kind = "python"
        elif mx and my and mx.group(1, 2) == my.group(1, 2):
            kind = "record_sha"
            differs.append(_norm(mx.group(1)))
        else:
            kind, allowed = "disallowed", False
        lines.append({"line": i, "kind": kind, "old": x, "new": y})
    return {"allowed": allowed, "lines": lines, "record_sha_differs": sorted(differs)}


def _flat(obj, prefix=""):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out.update(_flat(v, f"{prefix}/{k}"))
        return out
    return {prefix: obj}


def profile_diff(old: bytes, new: bytes, version: str, build: list[str]) -> dict:
    po, pn = json.loads(old), json.loads(new)
    fo, fn = _flat(po), _flat(pn)
    changed = [{"path": k, "old": fo.get(k), "new": fn.get(k)} for k in sorted(set(fo) | set(fn)) if fo.get(k) != fn.get(k)]
    want = json.loads(old)
    want["python"]["version"], want["python"]["build"] = version, build
    regenerated_equal = _dump(want) == new           # 두 값만 바꾼 옛 PROFILE 을 같은 직렬화로 다시 만들면 새 파일과 바이트 동일해야 한다
    return {"allowed": regenerated_equal, "changed": changed, "regenerated_equal": regenerated_equal}


def manifest_diff(old: bytes, new: bytes, new_dir: Path) -> dict:
    mo, mn = json.loads(old), json.loads(new)
    changed = sorted(k for k in set(mo) | set(mn) if mo.get(k) != mn.get(k))
    stale = sorted(k for k, h in mn.items() if not (new_dir / k).is_file() or _sha((new_dir / k).read_bytes()) != h)
    allowed = set(mo) == set(mn) and set(changed) <= {LOCK, PROFILE} and not stale
    return {"allowed": allowed, "changed": changed, "manifest_vs_files_mismatch": stale}


# ── S9 RECORD 행 대조 ──────────────────────────────────────────────────────────

def _rows(text: str) -> list[list[str]]:
    return [r for r in csv.reader(io.StringIO(text)) if r]


def _meta(dist_info: Path) -> tuple[str, str]:
    name = version = None
    for ln in (dist_info / "METADATA").read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            break                                    # 머리 끝 — 본문의 "Name:" 같은 줄을 읽지 않는다
        if ln.startswith("Name:") and name is None:
            name = ln.split(":", 1)[1].strip()
        elif ln.startswith("Version:") and version is None:
            version = ln.split(":", 1)[1].strip()
    if not name or not version:
        raise SystemExit(f"METADATA 에 Name · Version 이 없다: {dist_info}")
    return name, version


def _wheel_index(dirs: list[Path]) -> dict:
    index = {}
    for d in dirs:
        for p in sorted(d.glob("*.whl")):
            name, version = p.name.split("-")[:2]
            key = (_norm(name), version)
            if key in index:
                raise SystemExit(f"같은 배포판 · 판의 wheel 이 둘: {index[key].name} · {p.name}")
            index[key] = p
    return index


def _shebang_ok(line: str, venv: str) -> bool:
    return re.fullmatch("#!" + re.escape(venv) + r"/bin/python(3(\.11)?)?", line) is not None


def record_rows(site: Path, venv: str, wheel_dirs: list[Path], records_out: Path) -> dict:
    """배포판마다: wheel 안 RECORD 의 행 (RECORD 자신 제외) 이 설치 RECORD 에 같은 경로 · 해시 · 크기로 있는가 (`.data/` 는 옮겨진 자리 ·
    scripts 는 bin) · 설치 RECORD 의 나머지 행이 pip 가 만든 것뿐인가 · bin 스크립트 첫 줄이 이 venv 의 python 인가. RECORD 원문을 보존한다."""
    wheels = _wheel_index(wheel_dirs)
    records_out.mkdir(parents=True, exist_ok=False)
    out = {}
    for di in sorted(site.glob("*.dist-info")):
        name, version = _meta(di)
        key = (_norm(name), version)
        raw = (di / "RECORD").read_bytes()
        (records_out / f"{key[0]}-{version}.RECORD").write_bytes(raw)
        text = (di / "RECORD").read_text(encoding="utf-8")          # env_profile 와 같은 읽기 (줄바꿈 정규화) → lock 의 record-sha256
        res = {"dist_info": di.name, "version": version, "record_raw_sha256": _sha(raw),
               "record_text_sha256": _sha(text.encode("utf-8")), "wheel": None, "bin_rows": [], "shebangs": {}, "problems": []}
        out[key[0]] = res
        wheel = wheels.get(key)
        if wheel is None:
            res["problems"].append("대응 wheel 없음")
            continue
        res["wheel"] = wheel.name
        with zipfile.ZipFile(wheel) as z:
            recs = [n for n in z.namelist() if n.count("/") == 1 and n.endswith(".dist-info/RECORD")]
            if len(recs) != 1:
                res["problems"].append(f"wheel 안 RECORD 가 하나가 아님: {recs}")
                continue
            wrows = _rows(z.read(recs[0]).decode("utf-8"))
        inst = {}
        for r in _rows(text):
            inst[r[0]] = (r[1] if len(r) > 1 else "", r[2] if len(r) > 2 else "")
        matched = set()
        for r in wrows:
            path, h, size = r[0], (r[1] if len(r) > 1 else ""), (r[2] if len(r) > 2 else "")
            if path == recs[0]:
                continue
            top, _, rest = path.partition("/")
            if top.endswith(".data"):
                kind, _, sub = rest.partition("/")
                if kind == "scripts":                 # 설치 때 첫 줄이 바뀐다 — 해시가 아니라 자리로 맞춘다
                    target = f"../../../bin/{sub}"
                    if target in inst:
                        matched.add(target)
                        res["bin_rows"].append(target)
                    else:
                        res["problems"].append({"wheel_script_missing": path})
                    continue
                if kind in ("purelib", "platlib") and inst.get(sub) == (h, size):
                    matched.add(sub)
                    continue
                cand = [p for p, v in inst.items() if p.startswith("../") and v == (h, size) and p not in matched]
                if cand:
                    matched.add(cand[0])
                else:
                    res["problems"].append({"wheel_data_row_missing": path})
                continue
            if inst.get(path) == (h, size):
                matched.add(path)
            else:
                res["problems"].append({"wheel_row_mismatch": path, "wheel": [h, size], "installed": inst.get(path)})
        for path, (h, size) in sorted(inst.items()):
            if path in matched:
                continue
            if path.startswith("../../../bin/"):
                res["bin_rows"].append(path)
            elif path.endswith(".pyc") and "/__pycache__/" in f"/{path}" and h == "":
                continue
            elif path.count("/") == 1 and path.split("/")[0].endswith(".dist-info") and path.split("/")[1] in PIP_MADE:
                continue
            else:
                res["problems"].append({"installed_row_unexplained": path})
        res["bin_rows"] = sorted(set(res["bin_rows"]))
        for path in res["bin_rows"]:
            line = Path(os.path.normpath(site / path)).read_bytes().split(b"\n", 1)[0].decode("utf-8", "replace")
            res["shebangs"][path] = line
            if not _shebang_ok(line, venv):
                res["problems"].append({"shebang_not_this_venv": path, "line": line})
    return out


def compare(old: Path, new: Path, venv: str, wheel_dirs: list[Path], version: str, build: list[str], records_out: Path) -> dict:
    disallowed = []
    names_old = {p.name for p in old.iterdir() if p.is_file()} - set(HUMAN_RECORDS)
    names_new = {p.name for p in new.iterdir() if p.is_file()} - set(HUMAN_RECORDS)
    if names_old != names_new or any(p.is_dir() for p in new.iterdir()):
        disallowed.append({"file_set": {"only_old": sorted(names_old - names_new), "only_new": sorted(names_new - names_old),
                                        "dirs_in_new": sorted(p.name for p in new.iterdir() if p.is_dir())}})
    files = {}
    for n in sorted(names_old & names_new):
        bo, bn = (old / n).read_bytes(), (new / n).read_bytes()
        e = {"old_sha256": _sha(bo), "new_sha256": _sha(bn), "identical": bo == bn}
        if bo != bn:
            if n == LOCK:
                e.update(lock_diff(bo, bn, version))
            elif n == PROFILE:
                e.update(profile_diff(bo, bn, version, build))
            elif n == MANIFEST:
                e.update(manifest_diff(bo, bn, new))
            else:
                e["allowed"] = False
            if not e["allowed"]:
                disallowed.append(n)
        files[n] = e
    sps = sorted(Path(venv).glob("lib/python3*/site-packages"))
    if len(sps) != 1:
        raise SystemExit(f"venv site-packages 를 하나로 정하지 못했다: {sps}")
    rows = record_rows(sps[0], venv, wheel_dirs, records_out)
    bin_set = sorted(d for d, r in rows.items() if r["bin_rows"])
    differs = files.get(LOCK, {}).get("record_sha_differs", [])
    if differs != bin_set:
        disallowed.append({"record_sha_differs_vs_bin_set": {"record_sha_differs": differs, "bin_set": bin_set}})
    disallowed += [{"record_rows": d, "problems": r["problems"]} for d, r in rows.items() if r["problems"]]
    lock_new = {m.group(1): m.group(3) for m in map(LOCK_BODY.match, (new / LOCK).read_text(encoding="utf-8").splitlines()) if m}
    unbound = sorted(d for d, r in rows.items() if lock_new.get(d) != r["record_text_sha256"]) + sorted(set(lock_new) - set(rows))
    if unbound:                                      # 보존한 RECORD 원문이 새 lock 의 그 배포판과 결속되지 않음
        disallowed.append({"records_not_bound_to_new_lock": unbound})
    return {"old": str(old), "new": str(new), "venv": venv, "python_version": version, "python_build": build,
            "files": files, "record_rows": rows, "bin_set": bin_set, "disallowed": disallowed, "allowed_only": not disallowed,
            "note": "allowed_only 는 '허용 차이 밖 없음' 일 뿐 — 채택은 검토 수용 뒤 (요청문 §4)"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("artifacts")
    a1.add_argument("--wheels", required=True, type=Path)
    g = a1.add_mutually_exclusive_group(required=True)
    g.add_argument("--expect-log", type=Path)
    g.add_argument("--expect-dists")
    a1.add_argument("--out", required=True, type=Path)
    a2 = sub.add_parser("compare")
    a2.add_argument("--old", required=True, type=Path)
    a2.add_argument("--new", required=True, type=Path)
    a2.add_argument("--venv", required=True)
    a2.add_argument("--wheels", required=True, type=Path, action="append")
    a2.add_argument("--python-version", required=True)
    a2.add_argument("--python-build", required=True)
    a2.add_argument("--records-out", required=True, type=Path)
    a2.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    if a.out.exists():
        raise SystemExit(f"{a.out} 가 이미 있다 — 덮어쓰지 않는다")
    if a.cmd == "artifacts":
        if a.expect_log:
            rep = artifacts(a.wheels, log_wheel_names(a.expect_log.read_text(encoding="utf-8")), by="filename")
        else:
            rep = artifacts(a.wheels, a.expect_dists.split(","), by="dist")
        ok = rep["ok"]
    else:
        if not os.path.isabs(a.venv):
            raise SystemExit("--venv 는 절대 경로 (bin 스크립트 첫 줄과 그대로 대조한다)")
        build = a.python_build.split("|")
        if len(build) != 2:
            raise SystemExit("--python-build 는 '<이름>|<시각>'")
        rep = compare(a.old, a.new, a.venv, a.wheels, a.python_version, build, a.records_out)
        ok = rep["allowed_only"]
    _write(a.out, rep)
    print(a.cmd, "OK" if ok else "FAIL", a.out)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
