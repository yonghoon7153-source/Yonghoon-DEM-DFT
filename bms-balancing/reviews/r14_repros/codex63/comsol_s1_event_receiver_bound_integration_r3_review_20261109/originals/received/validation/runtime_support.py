"""R3 sealed bootstrap. Scope guard, not a security or real-time guarantee."""
import __future__
import ast
import builtins
import dataclasses
import encodings.utf_8
from fractions import Fraction
import hashlib
import json
import locale
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
import traceback
import types
import typing

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent
SOURCE = TASK / "source"
ARENA = TASK / "arena"
RESULTS = TASK / "results"
NAMES = ("exact_time", "event_clock_core", "state_owner", "snapshot_codec",
         "file_ports", "receiver_protocol", "evidence_admission", "deadline_receive",
         "bound_ack_session", "receiver_session", "receiver_bridge",
         "receiver_finish", "live_file_transport", "receiver_worker_candidate")
CHILD_NAMES = ("exact_time", "event_clock_core", "state_owner", "snapshot_codec",
               "receiver_protocol", "receiver_finish", "receiver_worker_candidate")
IMPORTS = {"__future__", "dataclasses", "fractions", "typing", "hashlib", "json",
           "pathlib", "re", "stat", "time", "os", "subprocess", *NAMES}
GUARD_EVENTS = []
IO_EVENTS = []
_ROLE = None
_READ = set()
_EXPECTED_ARGV = None
_POPEN_COUNT = 0
_DEVNULL_COUNT = 0

def norm(path):
    return os.path.normcase(os.path.abspath(os.fspath(path)))

def inside(path, base):
    p, b = norm(path), norm(base)
    return p == b or p.startswith(b + os.sep)

def deny(reason):
    GUARD_EVENTS.append(reason)
    raise RuntimeError(reason)

def audit(event, args):
    global _POPEN_COUNT, _DEVNULL_COUNT
    if event == "subprocess.Popen":
        executable, argv, cwd, env = args
        ok = (argv == subprocess.list2cmdline(_EXPECTED_ARGV) if isinstance(argv, str)
              else isinstance(argv, (list, tuple)) and list(argv) == _EXPECTED_ARGV)
        if (_ROLE != "parent" or _POPEN_COUNT or not ok or
                norm(executable) != norm(_EXPECTED_ARGV[0]) or norm(cwd) != norm(TASK)
                or env is not None):
            deny("UNAUTHORIZED_PROCESS_CREATION")
        _POPEN_COUNT += 1
        return
    if event.startswith(("socket.", "ctypes.", "winreg.", "os.exec", "os.spawn", "os.posix_spawn")) or event in {
        "os.system", "os.startfile", "os.startfile/2", "os.fork", "os.kill", "os.killpg",
        "os.remove", "os.rmdir", "os.symlink", "os.link", "os.chmod", "os.utime",
        "os.truncate", "os.putenv", "os.unsetenv", "builtins.input", "builtins.input/result",
        "os.rename", "os.replace"}:
        deny("FORBIDDEN_ACTIVITY:" + event)
    if event == "open":
        path, mode, flags = args
        if not isinstance(path, (str, bytes, os.PathLike)):
            deny("DIRECT_DESCRIPTOR_OPEN_DENIED")
        path = os.fsdecode(path)
        writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if (_ROLE == "parent" and not _POPEN_COUNT and not _DEVNULL_COUNT
                and path.lower() == os.devnull.lower() and (flags & 3) == os.O_RDWR
                and not flags & (os.O_CREAT | os.O_TRUNC | os.O_APPEND | os.O_EXCL)):
            _DEVNULL_COUNT += 1
            return
        allowed_area = inside(path, ARENA) or (_ROLE == "parent" and inside(path, RESULTS))
        if not (allowed_area or (not writing and norm(path) in _READ)):
            deny("FILE_ACCESS_OUTSIDE_SCOPE:" + path)
        IO_EVENTS.append({"event": "open", "path": norm(path), "writing": writing})
    elif event in ("os.mkdir", "os.scandir", "os.listdir"):
        if not (inside(args[0], ARENA) or (_ROLE == "parent" and inside(args[0], RESULTS))):
            deny("DIRECTORY_ACCESS_OUTSIDE_SCOPE")

def target_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level or name not in IMPORTS or name not in sys.modules:
        deny("TARGET_IMPORT_DENIED:" + name)
    return builtins.__import__(name, globals, locals, fromlist, level)

def blocked(*args, **kwargs):
    deny("TARGET_DYNAMIC_OR_CONSOLE_DENIED")

def load_target(name):
    path = SOURCE / (name + ".py.inactive.txt")
    tree = ast.parse(path.read_bytes(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                deny("RELATIVE_TARGET_IMPORT")
            names = [node.module]
        else:
            continue
        if any(n not in IMPORTS for n in names):
            deny("STATIC_TARGET_IMPORT_DENIED")
    safe = dict(vars(builtins))
    safe["__import__"] = target_import
    for key in ("open", "input", "eval", "exec", "compile", "breakpoint", "print"):
        safe[key] = blocked
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__dict__["__builtins__"] = safe
    sys.modules[name] = module
    exec(compile(tree, str(path), "exec"), module.__dict__)
    return module

def initialize(role):
    global _ROLE, _READ, _EXPECTED_ARGV
    if _ROLE is not None or role not in ("parent", "child"):
        raise RuntimeError("ROLE_REPEATED_OR_INVALID")
    _ROLE = role
    seal = json.loads((TASK / "PRESEAL.json").read_text(encoding="utf-8"))
    records = seal["files"] + [seal["engine"]]
    _READ = {norm(row["path"]) for row in records}
    _READ.add(norm(TASK / "PRESEAL.json"))
    config = json.loads((TASK / "CONFIG.json").read_text(encoding="utf-8"))
    _EXPECTED_ARGV = [seal["engine"]["path"], "-I", "-B", str(ROOT / "receiver_entry.py"),
                      config["session_ref"], seal["source_manifest_sha256"]]
    sys.addaudithook(audit)
    builtins.input = blocked
    if norm(sys.executable) != norm(seal["engine"]["path"]) or sys.flags.isolated != 1 or not sys.dont_write_bytecode:
        raise RuntimeError("ENGINE_OR_FLAGS_MISMATCH")
    expected = [str(ROOT / "run.py")] if role == "parent" else _EXPECTED_ARGV[3:]
    if [norm(sys.argv[0]), *sys.argv[1:]] != [norm(expected[0]), *expected[1:]]:
        raise RuntimeError("ROLE_ARGV_MISMATCH")
    for row in records:
        raw = Path(row["path"]).read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise RuntimeError("SEALED_IDENTITY_CHANGED:" + row["path"])
    if hashlib.sha256((TASK / "SOURCE_MANIFEST.json").read_bytes()).hexdigest() != seal["source_manifest_sha256"]:
        raise RuntimeError("SOURCE_MANIFEST_MISMATCH")
    names = CHILD_NAMES if role == "child" else tuple(n for n in NAMES if n != "receiver_worker_candidate")
    modules = {name: load_target(name) for name in names}
    return {"modules": modules, "config": config, "seal": seal,
            "engine": seal["engine"]["path"], "child_entry": str(ROOT / "receiver_entry.py"),
            "session_ref": config["session_ref"], "source_manifest_sha256": seal["source_manifest_sha256"]}

def write_new(path, value):
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    with Path(path).open("xb") as stream:
        if stream.write(raw) != len(raw):
            raise RuntimeError("EVIDENCE_SHORT_WRITE")
    if Path(path).read_bytes() != raw:
        raise RuntimeError("EVIDENCE_READBACK_MISMATCH")

def plain(value):
    if dataclasses.is_dataclass(value):
        return {f.name: plain(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, bytes):
        return {"bytes": len(value), "sha256": hashlib.sha256(value).hexdigest(), "utf8": value.decode("utf-8")}
    if isinstance(value, (tuple, list)):
        return [plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    return value

