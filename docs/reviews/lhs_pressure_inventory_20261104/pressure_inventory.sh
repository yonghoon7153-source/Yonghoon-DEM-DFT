#!/bin/sh
# Inventory only. Run as a file: sh pressure_inventory.sh ibb|wsl
# No heredoc (shells can spill large heredocs to temporary files).
# Python isolated mode and -B prevent environment imports and bytecode writes.
exec python3 -I -B -c '
import errno
import io
import json
import os
import platform
import pwd
import re
import stat
import sys

B7_SOURCE_SHA256 = "34eb74142884489505590501840ccc6423a014a508989c82f135020146283ad3"
PRESS_LINE = re.compile(r"^\s*Current Pressure:\s*(\S+)\s*MPa\s*\(Target:\s*(\S+)\s*\)\s*$")
PRESS_PREFIX = re.compile(r"^\s*Current Pressure:")
RESTART_ECHO = re.compile(r"^\s*read_restart\s")
RESTART_MESSAGE = re.compile(r"^\s*Reading restart file\b")
MAX_LINE = 1024 * 1024
MAX_LOG_BYTES = 512 * 1024 * 1024
ROOTS = {"base": "/home/yonghoon/dem_test/lhs",
         "supp": "/home/yonghoon/lhs_supp_20261006",
         "local": "/home/yonghoon71/lhs_local"}


class Refusal(Exception):
    def __init__(self, code):
        self.code = code


def error_code(exc):
    if isinstance(exc, Refusal):
        return exc.code
    if isinstance(exc, OSError):
        if exc.errno == errno.ENOENT:
            return "MISSING"
        if exc.errno == errno.ELOOP:
            return "SYMLINK"
        if exc.errno == errno.ENOTDIR:
            return "NONREGULAR"
    return "UNREADABLE"


def stamp(st):
    return (st.st_dev, st.st_ino, st.st_mode, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns, st.st_uid, st.st_gid)


def open_dir(parent, name):
    before = os.stat(name, dir_fd=parent, follow_symlinks=False)
    if stat.S_ISLNK(before.st_mode):
        raise Refusal("SYMLINK")
    if not stat.S_ISDIR(before.st_mode):
        raise Refusal("NONREGULAR")
    fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)
    if stamp(before) != stamp(os.fstat(fd)):
        os.close(fd)
        raise Refusal("CHANGED")
    return fd, before


def verify_dir(parent, name, fd, before):
    try:
        if stamp(before) != stamp(os.fstat(fd)) or stamp(before) != stamp(os.stat(name, dir_fd=parent, follow_symlinks=False)):
            raise Refusal("CHANGED")
    except OSError:
        raise Refusal("CHANGED")


def root_alias_allowed(requested, resolved):
    if requested == resolved:
        return True
    return (requested.startswith("/home/yonghoon/") and
            resolved == "/lustre" + requested)


def open_root(path):
    path = os.fspath(path)
    resolved = os.path.realpath(path)
    if not root_alias_allowed(path, resolved):
        raise Refusal("ROOT_ALIAS_REFUSED")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for part in resolved.split("/"):
            if not part:
                continue
            child, unused = open_dir(fd, part)
            os.close(fd)
            fd = child
        return fd, resolved, os.fstat(fd)
    except BaseException:
        os.close(fd)
        raise


def count_text(stream):
    result = {"b7_matches": 0, "pressure_prefix_malformed": 0,
              "read_restart_echo_lines": 0, "reading_restart_message_lines": 0}
    consumed = 0
    while True:
        physical = stream.readline(MAX_LINE + 1)
        if not physical:
            break
        consumed += len(physical)
        if len(physical) > MAX_LINE or consumed > MAX_LOG_BYTES:
            raise Refusal("LIMIT")
        # B7 uses text.splitlines(), including Unicode line separators.
        for line in physical.splitlines():
            matched = PRESS_LINE.match(line) is not None
            result["b7_matches"] += int(matched)
            result["pressure_prefix_malformed"] += int(bool(PRESS_PREFIX.match(line)) and not matched)
            result["read_restart_echo_lines"] += int(RESTART_ECHO.match(line) is not None)
            result["reading_restart_message_lines"] += int(RESTART_MESSAGE.match(line) is not None)
    return result


def scan_log(parent, name):
    fd = None
    try:
        before = os.stat(name, dir_fd=parent, follow_symlinks=False)
        if stat.S_ISLNK(before.st_mode):
            raise Refusal("SYMLINK")
        if not stat.S_ISREG(before.st_mode):
            raise Refusal("NONREGULAR")
        if before.st_size > MAX_LOG_BYTES:
            raise Refusal("LIMIT")
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
        opened = os.fstat(fd)
        if not stat.S_ISREG(opened.st_mode) or stamp(before) != stamp(opened):
            raise Refusal("CHANGED")
        with io.open(fd, "r", encoding="utf-8", errors="replace", newline=None, closefd=True) as stream:
            fd = None
            result = count_text(stream)
            after = os.fstat(stream.fileno())
        try:
            named = os.stat(name, dir_fd=parent, follow_symlinks=False)
        except OSError:
            raise Refusal("CHANGED")
        if stamp(before) != stamp(after) or stamp(before) != stamp(named):
            raise Refusal("CHANGED")
        result.update(status="COUNTED", bytes=before.st_size)
        return result
    except (OSError, Refusal, UnicodeError):
        return {"status": error_code(sys.exc_info()[1])}
    finally:
        if fd is not None:
            os.close(fd)


def count_out(parent, prefix):
    fd = None
    try:
        try:
            fd, before = open_dir(parent, "logs")
        except FileNotFoundError:
            return {"status": "ABSENT", "regular_files": 0}
        count = 0
        for name in os.listdir(fd):
            if not (name.startswith(prefix) and name.endswith(".out")):
                continue
            first = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISLNK(first.st_mode):
                raise Refusal("SYMLINK")
            if not stat.S_ISREG(first.st_mode):
                raise Refusal("NONREGULAR")
            if stamp(first) != stamp(os.stat(name, dir_fd=fd, follow_symlinks=False)):
                raise Refusal("CHANGED")
            count += 1
        verify_dir(parent, "logs", fd, before)
        return {"status": "COUNTED", "regular_files": count}
    except (OSError, Refusal):
        return {"status": error_code(sys.exc_info()[1])}
    finally:
        if fd is not None:
            os.close(fd)


def plan(mode):
    if mode == "ibb":
        return ([("base", "lhs00_%03d" % n) for n in range(100)] +
                [("base", "lhsx_%03d" % n) for n in range(1, 65)] +
                [("supp", "lhss_%03d" % n) for n in range(1, 21)])
    if mode == "wsl":
        return [("local", "lhs00_%03d" % n) for n in range(100, 130)]
    raise Refusal("MODE_REFUSED")


def inventory(mode, roots):
    layout = plan(mode)
    opened, root_status, rows = {}, {}, []
    try:
        for key in sorted(set(k for k, case in layout)):
            try:
                opened[key] = open_root(roots[key])
                root_status[key] = "COUNTED"
            except (OSError, Refusal):
                root_status[key] = error_code(sys.exc_info()[1])
        for key, case in layout:
            row = {"case": case, "root": key, "status": "NOT_ESTABLISHED"}
            rows.append(row)
            if key not in opened:
                row["reason"] = root_status[key]
                continue
            parent = opened[key][0]
            fd = None
            try:
                fd, before = open_dir(parent, case)
                names = ["log.liggghts", "log.txt"] if mode == "wsl" else ["log.liggghts"]
                row["logs"] = {name: scan_log(fd, name) for name in names}
                row["case_out"] = count_out(fd, "")
                row["root_out"] = count_out(parent, "output_" + case + "_")
                verify_dir(parent, case, fd, before)
                if (all(r["status"] == "COUNTED" for r in row["logs"].values()) and
                    all(row[k]["status"] in ("COUNTED", "ABSENT") for k in ("case_out", "root_out"))):
                    row["logs_with_b7_matches"] = sum(r["b7_matches"] > 0 for r in row["logs"].values())
                    row["status"] = "COUNTED"
            except (OSError, Refusal):
                row.clear()
                row.update(case=case, root=key, status="NOT_ESTABLISHED", reason=error_code(sys.exc_info()[1]))
            finally:
                if fd is not None:
                    os.close(fd)
        for key, (fd, resolved, before) in opened.items():
            try:
                if (os.path.realpath(roots[key]) != resolved or
                    stamp(before) != stamp(os.fstat(fd)) or
                    stamp(before) != stamp(os.stat(resolved, follow_symlinks=False))):
                    root_status[key] = "CHANGED"
            except OSError:
                root_status[key] = "CHANGED"
        complete = all(r["status"] == "COUNTED" for r in rows) and all(s == "COUNTED" for s in root_status.values())
        return {"schema": "lhs_pressure_inventory/v1", "mode": mode,
                "status": "INVENTORY_COMPLETE" if complete else "NOT_ESTABLISHED",
                "rc": 0 if complete else 2, "expected_cases": len(layout),
                "counted_cases": sum(r["status"] == "COUNTED" for r in rows),
                "b7_source_sha256": B7_SOURCE_SHA256, "roots": root_status, "cases": rows}
    finally:
        for fd, resolved, before in opened.values():
            os.close(fd)


def runtime_identity():
    return (platform.system(), platform.node().split(".")[0], platform.release(),
            pwd.getpwuid(os.geteuid()).pw_name, os.getuid(), os.geteuid())


def identity_allowed(mode, identity):
    system, host, release, user, uid, euid = identity
    if system != "Linux" or uid != euid:
        return False
    if mode == "ibb":
        return host == "ibb-master" and user == "yonghoon" and "microsoft" not in release.lower()
    return mode == "wsl" and user == "yonghoon71" and "microsoft" in release.lower()


def main(argv):
    failure = {"schema": "lhs_pressure_inventory/v1", "status": "NOT_ESTABLISHED", "rc": 2}
    try:
        if len(argv) != 1 or argv[0] not in ("ibb", "wsl"):
            result = dict(failure, reason="MODE_REFUSED")
        elif not identity_allowed(argv[0], runtime_identity()):
            result = dict(failure, reason="IDENTITY_REFUSED")
        else:
            result = inventory(argv[0], ROOTS)
        payload = json.dumps(result, ensure_ascii=True, separators=(",", ":")) + "\n"
        rc = result["rc"]
    except BaseException:
        payload = json.dumps(dict(failure, reason="INVENTORY_ERROR"), separators=(",", ":")) + "\n"
        rc = 2
    # Once output starts, do not turn a write/flush error into a second JSON.
    # A single write is not atomic; the caller must also require process rc 0.
    try:
        if sys.stdout.write(payload) != len(payload):
            return 2
        sys.stdout.flush()
    except BaseException:
        return 2
    return rc


if __name__ == "__main__":
    # main flushes successful output. Immediate exit prevents a failed buffer
    # from being flushed again during interpreter shutdown. This is a CLI.
    os._exit(main(sys.argv[1:]))
' "$@" 2>/dev/null
