"""reil_c4_env_reseal_check.py 자체 시험 — 합성 자료 · 커밋된 10월 봉인과 원문 기록 · 지금 ensurepip 묶음 읽기만 (설치 · venv · pip · 네트워크 0).

실행: 저장소 뿌리에서 `/usr/bin/python3.11 -I -B bms-balancing/evidence/reil_c4_env_reseal_selftest_20261124/selftest.py`.
임시 파일은 TMPDIR 아래 TemporaryDirectory 에만 쓴다. 대조기는 경로로 읽어 들인다 (`-B` — 저장소에 pyc 를 쓰지 않는다).
결과: 사례마다 PASS/FAIL 한 줄 · 끝에 N/N. 하나라도 FAIL 이면 rc 1.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "bms-balancing" / "scripts" / "reil_c4_env_reseal_check.py"
spec = importlib.util.spec_from_file_location("reseal_check", TOOL)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
OLD_E = REPO / C.OLD_E
OLD_SCI, OLD_TEST, OLD_SEAL = OLD_E / "09_records", OLD_E / "10_test_tool_records", REPO / C.OLD_SEAL
RESULTS = []


def case(name: str, ok: bool, detail="") -> None:
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not ok else ""))


def has(rep: dict, needle: str) -> bool:
    return any(needle in p for p in rep["problems"])


def rec_bytes(rows, lineterminator="\r\n") -> bytes:
    buf = io.StringIO()
    csv.writer(buf, lineterminator=lineterminator).writerows(rows)
    return buf.getvalue().encode("utf-8")


# ── 합성 venv · target ────────────────────────────────────────────────────────
OB, NB = "/synthetic/old/venv/bin", "/synthetic/NEWER/venv/bin"     # 길이가 다르다 (크기 칸이 바뀌는 경우까지 시험)
BODY = b"# -*- coding: utf-8 -*-\nimport re\nimport sys\nfrom demo.cli import main\nif __name__ == '__main__':\n    sys.exit(main())\n"


def build(tmp: Path, mutate=None) -> dict:
    """옛 원문 디렉터리 둘 + 새 venv/target 을 만든다. mutate(ctx) 로 특정 부분을 망가뜨린다."""
    ctx = {"tmp": tmp, "old_sci": tmp / "old_sci", "old_test": tmp / "old_test", "venv": tmp / "venv", "target": tmp / "target"}
    for k in ("old_sci", "old_test"):
        ctx[k].mkdir()
    sp = ctx["venv"] / "lib" / "python3.11" / "site-packages"
    sp.mkdir(parents=True)
    (ctx["venv"] / "bin").mkdir()
    ctx["target"].mkdir()
    (ctx["target"] / "bin").mkdir()
    ctx["sp"] = sp
    spec_ = {   # key: (kind, distinfo, files {path: bytes}, wrappers {name: (exe, body)}, pyc [paths])
        "demo-1.0.RECORD": ("venv", "demo-1.0.dist-info", {"demo/__init__.py": b"X = 1\n", "demo/cli.py": b"def main():\n    return 0\n",
                                                            "../../../share/man/man1/demo.1": b".TH DEMO 1\n"},
                            {"demo-cli": ("python", BODY)}, ["demo/__pycache__/__init__.cpython-311.pyc"]),
        "pip-24.0.RECORD": ("venv", "pip-24.0.dist-info", {"pip/__init__.py": b"__version__ = '24.0'\n",
                                                           "pip/_vendor/certifi/cacert.pem": b"OLD-CA\n"},
                            {"pip": ("python3.11", BODY), "pip3.11": ("python3.11", BODY)}, ["pip/__pycache__/__init__.cpython-311.pyc"]),
        "about-time-4.2.1.RECORD": ("venv", "about_time-4.2.1.dist-info", {"about_time/__init__.py": b"A = 1\n",
                                                                          "../../../LICENSE": b"about-time license\n"}, {}, []),
        "alive-progress-3.3.0.RECORD": ("venv", "alive_progress-3.3.0.dist-info", {"alive_progress/__init__.py": b"B = 1\n",
                                                                                  "../../../LICENSE": b"alive-progress license\n"}, {}, []),
        "tool-1.0.dist-info.RECORD": ("target", "tool-1.0.dist-info", {"tool/__init__.py": b"T = 1\n"},
                                      {"tool": ("python", BODY)}, ["tool/__pycache__/__init__.cpython-311.pyc"]),
    }
    names = {"demo-1.0.RECORD": ("demo", "1.0"), "pip-24.0.RECORD": ("pip", "24.0"), "about-time-4.2.1.RECORD": ("about_time", "4.2.1"),
             "alive-progress-3.3.0.RECORD": ("alive-progress", "3.3.0"), "tool-1.0.dist-info.RECORD": ("tool", "1.0")}
    ctx["new_files"] = {}
    ctx["spec"] = spec_
    for key, (kind, di, files, wraps, pyc) in spec_.items():
        base = sp if kind == "venv" else ctx["target"]
        pre = C.WRAPPER_PREFIX[kind]
        nm, ver = names[key]
        meta = f"Metadata-Version: 2.1\nName: {nm}\nVersion: {ver}\n\n".encode()
        all_files = dict(files)
        all_files[f"{di}/METADATA"] = meta
        all_files[f"{di}/INSTALLER"] = b"pip\n"
        all_files[f"{di}/REQUESTED"] = b""
        old_rows, new_rows = [], []
        for path, b in all_files.items():
            old_rows.append((path, C.record_hash(b), str(len(b))))
            new_rows.append((path, C.record_hash(b), str(len(b))))
        for w, (exe, body) in wraps.items():
            ob = f"#!{OB}/{exe}\n".encode() + body
            nb = f"#!{NB}/{exe}\n".encode() + body
            old_rows.append((pre + w, C.record_hash(ob), str(len(ob))))
            new_rows.append((pre + w, C.record_hash(nb), str(len(nb))))
            all_files[pre + w] = nb
        for p in pyc:
            old_rows.append((p, "", ""))
            new_rows.append((p, "", ""))
            all_files[p] = b"\x00pyc"
        old_rows.append((f"{di}/RECORD", "", ""))
        new_rows.append((f"{di}/RECORD", "", ""))
        ctx.setdefault("old_rows", {})[key] = old_rows
        ctx.setdefault("new_rows", {})[key] = new_rows
        ctx["new_files"][key] = (kind, base, di, all_files)
    # 선언된 차이 (pip 의 cacert) — 새 쪽만 내용이 다르다
    new_ca = b"NEW-CA bundle\n"
    i = [r[0] for r in ctx["new_rows"]["pip-24.0.RECORD"]].index("pip/_vendor/certifi/cacert.pem")
    ctx["new_rows"]["pip-24.0.RECORD"][i] = ("pip/_vendor/certifi/cacert.pem", C.record_hash(new_ca), str(len(new_ca)))
    ctx["new_files"]["pip-24.0.RECORD"][3]["pip/_vendor/certifi/cacert.pem"] = new_ca
    ctx["declared"] = {("pip-24.0.RECORD", "pip/_vendor/certifi/cacert.pem"):
                       ((C.record_hash(b"OLD-CA\n"), str(len(b"OLD-CA\n"))), (C.record_hash(new_ca), str(len(new_ca))))}
    ctx["collisions"] = dict(C.COLLISIONS)
    ctx["old_raw"] = {k: rec_bytes(v) for k, v in ctx["old_rows"].items()}
    ctx["new_raw"] = {k: rec_bytes(v) for k, v in ctx["new_rows"].items()}
    if mutate:
        mutate(ctx)
    for key, (kind, base, di, all_files) in ctx["new_files"].items():
        for path, b in all_files.items():
            if kind == "target" and path.startswith(C.WRAPPER_PREFIX["target"]):
                f = ctx["target"] / "bin" / path[len(C.WRAPPER_PREFIX["target"]):]
            else:
                f = Path(C.os.path.normpath(base / path))
            f.parent.mkdir(parents=True, exist_ok=True)
            if b is not None:
                f.write_bytes(b)
        (base / di).mkdir(parents=True, exist_ok=True)
        (base / di / "RECORD").write_bytes(ctx["new_raw"][key])
        old_dir = ctx["old_sci"] if kind == "venv" else ctx["old_test"]
        (old_dir / key).write_bytes(ctx["old_raw"][key])
    # 충돌: 디스크의 LICENSE 는 나중에 깔린 alive-progress 의 것
    (ctx["venv"] / "LICENSE").write_bytes(b"alive-progress license\n")
    for fn in ctx.get("after", []):
        fn(ctx)
    return ctx


def run_records(ctx, out=None, test_out=None) -> dict:
    return C.records(venv=ctx["venv"], target=ctx["target"], old_sci=ctx["old_sci"], old_test=ctx["old_test"], old_bin=OB,
                     new_bin=NB, declared=ctx["declared"], collisions=ctx["collisions"], sci_out=out, test_out=test_out)


def fresh(name: str) -> Path:
    d = Path(tempfile.mkdtemp(prefix=f"{name}_", dir=ROOT))
    return d


def records_cases() -> None:
    ctx = build(fresh("r1"))
    out, tout = ctx["tmp"] / "out_sci", ctx["tmp"] / "out_test"
    out.mkdir()
    tout.mkdir()
    rep = run_records(ctx, out, tout)
    kinds = sorted(c["kind"] for r in rep["dists"].values() for c in r["changed_rows"])
    case("R1 깨끗한 합성 세대 → 허용 차이만 (wrapper 4 · 선언 1 · 충돌 1)", not rep["problems"] and kinds == ["declared"] + ["wrapper"] * 4
         and sum(len(r["explained_collisions"]) for r in rep["dists"].values()) == 1, rep["problems"][:3])
    case("R19 --records-out 에 새 원문이 바이트 그대로 보존", all((out / k).read_bytes() == ctx["new_raw"][k] for k in ctx["new_raw"] if k.endswith(".RECORD") and not k.startswith("tool"))
         and (tout / "tool-1.0.dist-info.RECORD").read_bytes() == ctx["new_raw"]["tool-1.0.dist-info.RECORD"])

    def m(fn):
        return build(fresh("rx"), fn)

    def lf(c): c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(c["new_rows"]["demo-1.0.RECORD"], "\n")
    case("R2 줄 끝 CRLF → LF", has(run_records(m(lf)), "줄 끝"))

    def nofinal(c): c["new_raw"]["demo-1.0.RECORD"] = c["new_raw"]["demo-1.0.RECORD"][:-2]
    case("R3 마지막 줄바꿈 없음", has(run_records(m(nofinal)), "줄 끝"))

    def dup(c):
        r = c["new_rows"]["demo-1.0.RECORD"]
        c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(r + [r[0]])
    case("R4 중복 경로 (dict 로 덮지 않음)", has(run_records(m(dup)), "중복 경로"))

    def body(c):
        nb = f"#!{NB}/python\n".encode() + BODY.replace(b"main", b"evil")
        c["new_files"]["demo-1.0.RECORD"][3]["../../../bin/demo-cli"] = nb
        r = c["new_rows"]["demo-1.0.RECORD"]
        i = [x[0] for x in r].index("../../../bin/demo-cli")
        r[i] = (r[i][0], C.record_hash(nb), str(len(nb)))
        c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(r)
    case("R5 wrapper 본문 변경 (첫 줄 밖)", has(run_records(m(body)), "본문이 다르다"))

    def third(c):
        nb = b"#!/somewhere/else/bin/python\n" + BODY
        c["new_files"]["demo-1.0.RECORD"][3]["../../../bin/demo-cli"] = nb
        r = c["new_rows"]["demo-1.0.RECORD"]
        i = [x[0] for x in r].index("../../../bin/demo-cli")
        r[i] = (r[i][0], C.record_hash(nb), str(len(nb)))
        c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(r)
    case("R6 wrapper 첫 줄이 다른 venv", has(run_records(m(third)), "새 venv interpreter 가 아님"))

    def stale(c):
        ob = f"#!{OB}/python\n".encode() + BODY
        c["new_files"]["demo-1.0.RECORD"][3]["../../../bin/demo-cli"] = ob
        r = c["new_rows"]["demo-1.0.RECORD"]
        i = [x[0] for x in r].index("../../../bin/demo-cli")
        r[i] = c["old_rows"]["demo-1.0.RECORD"][i]
        c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(r)
    case("R7 wrapper 가 옛 경로 그대로 (행이 옛것과 같아도 잡음)", has(run_records(m(stale)), "새 venv interpreter 가 아님"))

    def other(c):
        for side in ("old_rows", "new_rows"):
            r = c[side]["demo-1.0.RECORD"]
            r.insert(len(r) - 1, ("pip-24.0.dist-info/INSTALLER", C.record_hash(b"pip\n"), "4"))
        c["old_raw"]["demo-1.0.RECORD"] = rec_bytes(c["old_rows"]["demo-1.0.RECORD"])
        c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(c["new_rows"]["demo-1.0.RECORD"])
    case("R8 다른 배포판 dist-info 의 행 (옛 · 새 둘 다 있어도)", has(run_records(m(other)), "다른 dist-info"))

    def nondecl(c):
        nb = b"X = 2\n"
        c["new_files"]["demo-1.0.RECORD"][3]["demo/__init__.py"] = nb
        r = c["new_rows"]["demo-1.0.RECORD"]
        r[0] = ("demo/__init__.py", C.record_hash(nb), str(len(nb)))
        c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(r)
    case("R9 선언 밖 행 변경 (RECORD · 파일 일관)", has(run_records(m(nondecl)), "허용 밖"))

    def wrongdecl(c):
        nb = b"ANOTHER CA\n"
        c["new_files"]["pip-24.0.RECORD"][3]["pip/_vendor/certifi/cacert.pem"] = nb
        r = c["new_rows"]["pip-24.0.RECORD"]
        i = [x[0] for x in r].index("pip/_vendor/certifi/cacert.pem")
        r[i] = (r[i][0], C.record_hash(nb), str(len(nb)))
        c["new_raw"]["pip-24.0.RECORD"] = rec_bytes(r)
    rep = run_records(m(wrongdecl))
    case("R10 선언 행이 선언과 다른 값", has(rep, "허용 밖") and has(rep, "선언된 차이가 실제로 나타나지 않음"))

    def tamper(c): c.setdefault("after", []).append(lambda cc: (cc["sp"] / "demo" / "cli.py").write_bytes(b"def main():\n    return 1\n"))
    case("R11 설치 바이트 변조 (RECORD 그대로)", has(run_records(m(tamper)), "설치 바이트가 RECORD 와 다름 demo/cli.py"))

    def missing(c): c.setdefault("after", []).append(lambda cc: (cc["sp"] / "demo" / "cli.py").unlink())
    case("R12 설치 파일 없음", has(run_records(m(missing)), "파일 없음 demo/cli.py"))

    def hashless(c):
        for side in ("old_rows", "new_rows"):
            c[side]["demo-1.0.RECORD"].insert(0, ("demo/data.txt", "", ""))
        c["old_raw"]["demo-1.0.RECORD"] = rec_bytes(c["old_rows"]["demo-1.0.RECORD"])
        c["new_raw"]["demo-1.0.RECORD"] = rec_bytes(c["new_rows"]["demo-1.0.RECORD"])
    case("R13 해시 없는 행이 pyc · RECORD 가 아님", has(run_records(m(hashless)), "해시 없는 행"))

    def tbody(c):
        c.setdefault("after", []).append(lambda cc: (cc["target"] / "bin" / "tool").write_bytes(f"#!{NB}/python\n".encode() + BODY + b"#x\n"))
    case("R14 pytest_t 쪽 wrapper 본문 변조 (../../bin → target/bin)", has(run_records(m(tbody)), "test_tools/tool-1.0.dist-info.RECORD"))

    def extra(c):
        def add(cc):
            di = cc["sp"] / "zzz-9.dist-info"
            di.mkdir()
            meta = b"Metadata-Version: 2.1\nName: zzz\nVersion: 9\n\n"
            (di / "METADATA").write_bytes(meta)
            (di / "RECORD").write_bytes(rec_bytes([("zzz-9.dist-info/METADATA", C.record_hash(meta), str(len(meta))),
                                                   ("zzz-9.dist-info/RECORD", "", "")]))
        c.setdefault("after", []).append(add)
    case("R15 새 venv 에만 있는 배포판", has(run_records(m(extra)), "배포판 집합이 다름"))

    def gone(c): c.setdefault("after", []).append(lambda cc: shutil.rmtree(cc["sp"] / "demo-1.0.dist-info"))
    case("R16 옛 세대에 있던 배포판이 새 venv 에 없음", has(run_records(m(gone)), "배포판 집합이 다름"))

    def quoted(c):
        raw = c["new_raw"]["demo-1.0.RECORD"]
        c["new_raw"]["demo-1.0.RECORD"] = raw.replace(b"demo/__init__.py,", b'"demo/__init__.py",', 1)
    case("R17 CSV 다시 쓰기와 다른 원문 (불필요한 따옴표)", has(run_records(m(quoted)), "CSV 로 다시 쓴 바이트"))

    def lic(c): c.setdefault("after", []).append(lambda cc: (cc["venv"] / "LICENSE").write_bytes(b"third license\n"))
    rep = run_records(m(lic))
    case("R18 설명된 충돌 — 디스크가 주인 행과 다르면 잡음", has(rep, "설명된 충돌 ../../../LICENSE") and has(rep, "alive-progress-3.3.0.RECORD"))

    def stray(c): c.setdefault("after", []).append(lambda cc: (cc["sp"] / "stray.py").write_bytes(b"x\n"))
    rep = run_records(m(stray))
    case("R20 RECORD 밖 파일은 관측으로만 (판정 불변)", not rep["problems"] and rep["observations"]["science"]["files_not_in_any_record"] == 1)


# ── 봉인 (진짜 10월 봉인 · 원문 위에서) ─────────────────────────────────────────

def make_new_seal(tmp: Path, *, lock_edit=None, prof_edit=None, man_edit=None, npy_flip=False, extra=None, drop=None,
                  python_line=True, prof_indent=1) -> tuple[Path, Path]:
    """기대 변환을 이 파일 안에서 따로 (대조기 함수를 쓰지 않고) 구현해 '새 봉인' 을 만든다."""
    recs = tmp / "new_records"
    shutil.copytree(OLD_SCI, recs)
    raw = (recs / "numpy-2.4.6.RECORD").read_bytes()
    raw2 = raw.replace(b"../../../bin/f2py,sha256=", b"../../../bin/f2py,sha256=X", 1)
    assert raw2 != raw
    (recs / "numpy-2.4.6.RECORD").write_bytes(raw2)
    seal = tmp / "new_seal"
    shutil.copytree(OLD_SEAL, seal)
    lock = (seal / "REIL_C6.lock.txt").read_text(encoding="utf-8")
    if python_line:
        assert lock.count('#@ python "3.11.17"\n') == 1
        lock = lock.replace('#@ python "3.11.17"\n', '#@ python "3.11.18"\n')
    old_np = hashlib.sha256(raw.decode().replace("\r\n", "\n").encode()).hexdigest()
    new_np = hashlib.sha256(raw2.decode().replace("\r\n", "\n").encode()).hexdigest()
    assert lock.count(old_np) == 1
    lock = lock.replace(old_np, new_np)
    if lock_edit:
        lock = lock_edit(lock)
    (seal / "REIL_C6.lock.txt").write_text(lock, encoding="utf-8")
    prof = json.loads((seal / "PROFILE.json").read_text(encoding="utf-8"))
    prof["python"]["version"], prof["python"]["build"] = "3.11.18", ["main", "Oct 26 2026 15:28:55"]
    if prof_edit:
        prof_edit(prof)
    (seal / "PROFILE.json").write_text(json.dumps(prof, ensure_ascii=False, sort_keys=True, indent=prof_indent) + "\n", encoding="utf-8")
    if npy_flip:
        b = bytearray((seal / "sobol_unit_seed0.npy").read_bytes())
        b[-1] ^= 1
        (seal / "sobol_unit_seed0.npy").write_bytes(bytes(b))
    if extra:
        (seal / extra).write_bytes(b"x")
    if drop:
        (seal / drop).unlink()
    man = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(seal.iterdir()) if p.name != "MANIFEST.json"}
    if man_edit:
        man_edit(man)
    (seal / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, sort_keys=True, indent=1) + "\n", encoding="utf-8")
    return seal, recs


def run_seal(seal: Path, recs: Path) -> dict:
    return C.seal(old=OLD_SEAL, new=seal, old_records=OLD_SCI, new_records=recs, py_old=C.PY_OLD, py_new=C.PY_NEW)


def seal_cases() -> None:
    rep = run_seal(*make_new_seal(fresh("s1")))
    case("S1 기대 변환만 한 새 봉인 → 허용 (lock record-sha 변경 = numpy 만)", not rep["problems"] and rep["lock_record_sha_changed"] == ["numpy"],
         rep["problems"][:3])
    rep = run_seal(*make_new_seal(fresh("s2"), lock_edit=lambda t: t.replace('"verified": 7187', '"verified": 7188')))
    case("S2 lock 의 다른 줄 (#@ files) 변경", has(rep, "REIL_C6.lock.txt: 기대 바이트와 다름"))

    def cffi(t):
        i = t.index("cffi==2.1.1  # record-sha256 ")
        j = i + len("cffi==2.1.1  # record-sha256 ")
        return t[:j] + ("0" if t[j] != "0" else "1") + t[j + 1:]
    rep = run_seal(*make_new_seal(fresh("s3"), lock_edit=cffi))
    case("S3 RECORD 가 안 바뀐 배포판의 record-sha 변경", has(rep, "REIL_C6.lock.txt: 기대 바이트와 다름"))
    rep = run_seal(*make_new_seal(fresh("s4"), prof_edit=lambda p: p["platform"].update(libc="glibc 2.40")))
    case("S4 PROFILE 의 다른 값 (libc)", has(rep, "PROFILE.json: 기대 바이트와 다름"))
    rep = run_seal(*make_new_seal(fresh("s5"), prof_indent=2))
    case("S5 PROFILE 직렬화 변경 (indent 2)", has(rep, "PROFILE.json: 기대 바이트와 다름"))
    rep = run_seal(*make_new_seal(fresh("s6"), man_edit=lambda m: m.update({"SOBOL_PHASE_A.json": "0" * 64})))
    case("S6 MANIFEST 값 하나 틀림", has(rep, "MANIFEST.json: 기대 바이트와 다름") and has(rep, "새 MANIFEST 가 새 파일들과 맞지 않음"))
    rep = run_seal(*make_new_seal(fresh("s7"), npy_flip=True))
    case("S7 .npy 한 비트 (MANIFEST 는 맞춰 줌)", has(rep, "sobol_unit_seed0.npy: 기대 바이트와 다름"))
    rep = run_seal(*make_new_seal(fresh("s8"), extra="README.md"))
    case("S8 새 봉인에 파일 하나 더", has(rep, "새 봉인 파일 집합"))
    rep = run_seal(*make_new_seal(fresh("s8b"), drop="sobol_unit_seed1.npy"))
    case("S8b 새 봉인에 파일 하나 빠짐", has(rep, "새 봉인 파일 집합"))
    rep = run_seal(*make_new_seal(fresh("s9"), python_line=False))
    case("S9 lock 의 python 줄이 옛 판 그대로", has(rep, "REIL_C6.lock.txt: 기대 바이트와 다름"))
    rep = C.seal(old=OLD_SEAL, new=OLD_SEAL, old_records=OLD_SCI, new_records=OLD_SCI, py_old=C.PY_OLD, py_new=C.PY_OLD)
    case("S10 진짜 10월 봉인 ↔ 자기 자신 (옛 lock ↔ 원문 30 결속 · PROFILE · MANIFEST 왕복)", not rep["problems"]
         and rep["lock_record_sha_changed"] == [], rep["problems"][:3])


# ── ensurepip 묶음 · wheel 디렉터리 ─────────────────────────────────────────────

def fake_wheel(path: Path, members: dict, record_members: dict | None = None) -> None:
    rm = members if record_members is None else record_members
    rows = [(n, C.record_hash(b), str(len(b))) for n, b in rm.items()] + [("pip-24.0.dist-info/RECORD", "", "")]
    with zipfile.ZipFile(path, "w") as z:
        for n, b in members.items():
            z.writestr(n, b)
        z.writestr("pip-24.0.dist-info/RECORD", rec_bytes(rows))


def bundled_cases() -> None:
    rep = C.bundled(bundled_dir=Path("/usr/lib/python3.11/ensurepip/_bundled"), old_sci=OLD_SCI, expect=C.BUNDLED, declared=C.DECLARED)
    pipw = rep["wheels"].get("pip-24.0-py3-none-any.whl", {})
    case("B0 지금 ensurepip 묶음 (읽기) → 허용 · pip 는 선언 1 행만 · setuptools 는 10월 sha 와 같음",
         not rep["problems"]
         and [d["path"] for d in pipw.get("members_differing_from_october_install", [])] == ["pip/_vendor/certifi/cacert.pem"]
         and rep["wheels"]["setuptools-79.0.1-py3-none-any.whl"]["equals_october_sha256"], rep["problems"][:3])
    base = {"pip/__init__.py": b"v = 24\n", "pip/_vendor/certifi/cacert.pem": b"OLD-CA\n", "pip-24.0.dist-info/METADATA": b"Name: pip\n"}

    def setup(tmp: Path, members: dict, old_extra=(), corrupt=False, extra_file=False):
        bd = tmp / "bundled"
        bd.mkdir()
        if corrupt:   # 구성원 바이트만 바뀌고 wheel 의 RECORD 는 원래 값 그대로
            fake_wheel(bd / "pip-24.0-py3-none-any.whl", {n: b + (b"!" if n == "pip/__init__.py" else b"") for n, b in members.items()},
                       record_members=members)
        else:
            fake_wheel(bd / "pip-24.0-py3-none-any.whl", members)
        if extra_file:
            (bd / "README").write_bytes(b"x")
        old = tmp / "old"
        old.mkdir()
        rows = [(n, C.record_hash(b), str(len(b))) for n, b in base.items()]
        rows += [("../../../bin/pip", "sha256=AAAA", "10"), ("pip-24.0.dist-info/INSTALLER", C.record_hash(b"pip\n"), "4"),
                 ("pip-24.0.dist-info/REQUESTED", C.record_hash(b""), "0"), ("pip/__pycache__/__init__.cpython-311.pyc", "", ""),
                 *old_extra, ("pip-24.0.dist-info/RECORD", "", "")]
        (old / "pip-24.0.RECORD").write_bytes(rec_bytes(rows))
        size, sha = C.file_digest(bd / "pip-24.0-py3-none-any.whl")
        expect = {"pip-24.0-py3-none-any.whl": {"size": size, "sha256": sha, "oct_sha256": "0" * 64, "old_record": "pip-24.0.RECORD"}}
        declared = {("pip-24.0.RECORD", "pip/_vendor/certifi/cacert.pem"):
                    ((C.record_hash(b"OLD-CA\n"), "7"), (C.record_hash(members["pip/_vendor/certifi/cacert.pem"]),
                                                          str(len(members["pip/_vendor/certifi/cacert.pem"]))))}
        return bd, old, expect, declared

    good = dict(base, **{"pip/_vendor/certifi/cacert.pem": b"NEW-CA\n!"})
    bd, old, ex, de = setup(fresh("b1"), good)
    case("B1 합성 pip wheel — 선언 행만 다름 → 허용", not C.bundled(bundled_dir=bd, old_sci=old, expect=ex, declared=de)["problems"])
    two = dict(good, **{"pip/__init__.py": b"v = 25\n"})
    bd, old, ex, de = setup(fresh("b2"), two)
    case("B2 구성원 하나 더 다름 (선언 밖)", has(C.bundled(bundled_dir=bd, old_sci=old, expect=ex, declared=de), "선언 밖"))
    bd, old, ex, de = setup(fresh("b3"), good, corrupt=True)
    ex = {k: dict(v, **dict(zip(("size", "sha256"), C.file_digest(bd / k)))) for k, v in ex.items()}
    case("B3 구성원이 wheel 자신의 RECORD 와 다름", has(C.bundled(bundled_dir=bd, old_sci=old, expect=ex, declared=de), "wheel 자신의 RECORD"))
    bd, old, ex, de = setup(fresh("b4"), good)
    ex = {k: dict(v, sha256="1" * 64) for k, v in ex.items()}
    case("B4 wheel 파일의 sha256 이 고정값과 다름", has(C.bundled(bundled_dir=bd, old_sci=old, expect=ex, declared=de), "고정값과 다름"))
    bd, old, ex, de = setup(fresh("b5"), good, extra_file=True)
    case("B5 묶음 디렉터리에 파일 하나 더", has(C.bundled(bundled_dir=bd, old_sci=old, expect=ex, declared=de), "묶음 파일 집합"))
    bd, old, ex, de = setup(fresh("b6"), good, old_extra=[("pip/extra.py", C.record_hash(b"x"), "1")])
    case("B6 옛 설치에만 있는 행이 pip 생성 범주가 아님", has(C.bundled(bundled_dir=bd, old_sci=old, expect=ex, declared=de), "pip 생성 범주가 아님"))


def wheels_cases() -> None:
    for name in ("04_artifacts_science.json", "04_artifacts_test.json"):
        d = json.loads((OLD_E / name).read_text(encoding="utf-8"))
        n = {"04_artifacts_science.json": 28, "04_artifacts_test.json": 4}[name]
        case(f"W0 10월 기록 {name} — ok · 문제 0 · 파일 {n} (이름 · 크기 · sha256)",
             d["ok"] is True and not d["problems"] and len(d["files"]) == n and all({"name", "size", "sha256"} <= set(f) for f in d["files"]))
    tmp = fresh("w")
    wd = tmp / "wheels"
    wd.mkdir()
    files = {"a-1-py3-none-any.whl": b"A" * 10, "b-2-py3-none-any.whl": b"B" * 20}
    for n, b in files.items():
        (wd / n).write_bytes(b)
    ej = tmp / "expect.json"
    ej.write_text(json.dumps({"ok": True, "problems": [], "files": [{"name": n, "size": len(b), "sha256": C.sha256_hex(b)} for n, b in files.items()]}))
    case("W1 정확히 같은 집합 → 허용", not C.wheels(wheel_dir=wd, expect_json=ej)["problems"])
    (wd / "a-1-py3-none-any.whl").write_bytes(b"A" * 9 + b"a")
    case("W2 같은 이름 · 크기, 다른 sha256", has(C.wheels(wheel_dir=wd, expect_json=ej), "크기 · sha256 다름"))
    (wd / "a-1-py3-none-any.whl").write_bytes(b"A" * 10)
    (wd / "c-3-py3-none-any.whl").write_bytes(b"C")
    case("W3 받은 쪽에 하나 더", has(C.wheels(wheel_dir=wd, expect_json=ej), "이름 집합 다름"))
    (wd / "c-3-py3-none-any.whl").unlink()
    (wd / "b-2-py3-none-any.whl").unlink()
    case("W4 하나 빠짐", has(C.wheels(wheel_dir=wd, expect_json=ej), "이름 집합 다름"))
    (wd / "b-2-py3-none-any.whl").write_bytes(b"B" * 20)
    (wd / "sub").mkdir()
    case("W5 파일 아닌 항목", has(C.wheels(wheel_dir=wd, expect_json=ej), "파일 아닌 항목"))


def parse_cases() -> None:
    probs, ends, n = [], set(), 0
    for d in (OLD_SCI, OLD_TEST):
        for p in sorted(d.iterdir()):
            rows, e, q = C.parse_record(p.read_bytes())
            probs += q
            ends |= set(e)
            n += 1
    case("P1 10월 RECORD 원문 34 — 문제 0 · 줄 끝은 전부 CRLF (마지막 줄 포함)", n == 34 and not probs and ends == {"\r\n"}, probs[:3])
    lock = (OLD_SEAL / "REIL_C6.lock.txt").read_text(encoding="utf-8")
    m = [C._DIST.fullmatch(ln) for ln in lock.split("\n")]
    pairs = [(x["name"], x["version"], x["record"]) for x in m if x]
    ok = len(pairs) == 30 and all(C.text_sha((OLD_SCI / f"{a}-{b}.RECORD").read_bytes()) == h for a, b, h in pairs)
    case("P2 10월 lock 의 record-sha256 30 = 원문 30 의 text_sha (env_profile 의 read_text 규칙)", ok)
    raw = rec_bytes([("a,b.py", C.record_hash(b"x"), "1"), ("c.py", "", "")])
    rows, e, q = C.parse_record(raw)
    case("P3 쉼표 든 경로 (따옴표 필요한 행) 는 정상 처리", not q and rows[0][0] == "a,b.py")


def cli_cases() -> None:
    tmp = fresh("cli")
    out = tmp / "exists.json"
    out.write_text("{}")
    r = subprocess.run([sys.executable, "-I", "-B", str(TOOL), "bundled", "--bundled", "/usr/lib/python3.11/ensurepip/_bundled", "--out", str(out)],
                       capture_output=True, text=True, timeout=60)
    case("C1 --out 이 이미 있으면 rc 2 (덮어쓰지 않음)", r.returncode == 2 and out.read_text() == "{}", r.stderr[-200:])
    r = subprocess.run([sys.executable, "-I", "-B", str(TOOL), "records", "--venv", str(tmp), "--target", str(tmp), "--records-out",
                        str(tmp / "a"), "--test-records-out", str(tmp / "b"), "--out", str(tmp / "o.json")], capture_output=True, text=True, timeout=60)
    case("C2 records 의 --venv 가 고정 경로가 아니면 rc 2", r.returncode == 2 and not (tmp / "a").exists(), r.stderr[-200:])
    o2 = tmp / "real.json"
    r = subprocess.run([sys.executable, "-I", "-B", str(TOOL), "bundled", "--bundled", "/usr/lib/python3.11/ensurepip/_bundled", "--out", str(o2)],
                       capture_output=True, text=True, timeout=60)
    d = json.loads(o2.read_text(encoding="utf-8")) if o2.exists() else {}
    case("C3 CLI bundled (S0 의 argv 꼴) → rc 0 · tool_sha256 기록", r.returncode == 0 and d.get("allowed_only") is True
         and d.get("tool_sha256") == C.sha256_hex(TOOL.read_bytes()), r.stdout[-200:])


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="reseal_selftest_") as root:
        ROOT = root
        print(f"tool {TOOL.relative_to(REPO)} sha256 {C.sha256_hex(TOOL.read_bytes())}")
        print(f"python {sys.version.split()[0]} · isolated {sys.flags.isolated} · dont_write_bytecode {sys.dont_write_bytecode}")
        for fn in (parse_cases, records_cases, seal_cases, bundled_cases, wheels_cases, cli_cases):
            try:
                fn()
            except Exception as exc:          # 시험 코드 자체의 오류도 FAIL 로 남긴다
                case(f"{fn.__name__} 예외", False, f"{type(exc).__name__}: {exc}")
        n_ok = sum(ok for _, ok in RESULTS)
        print(f"{n_ok} / {len(RESULTS)} PASS")
        sys.exit(0 if n_ok == len(RESULTS) else 1)
