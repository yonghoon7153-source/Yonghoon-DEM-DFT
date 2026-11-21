"""Install the pinned 7:3 development tools and detach or inspect the controller."""
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inventory(raw):
    entries = {}
    for line in raw.decode("ascii").splitlines():
        sha, name = line.split("  ", 1)
        require(len(sha) == 64 and all(c in "0123456789abcdef" for c in sha), "bad SHA")
        require(name not in entries and name[0].isalnum()
                and all(c.isalnum() or c in "._-" for c in name), "bad source name")
        entries[name] = sha
    require({"phase_controller.py", "run_arm.sh", "ps73_node.py", "ps73_sequence.py",
             "phase_arm.sbatch", "collect_ps73.py"} <= set(entries), "missing source")
    return entries


def check_installed(root, expected):
    require(root.is_dir() and not root.is_symlink(), "deployment not found or not a directory")
    p = root / "SOURCE_SHA256SUMS"
    require(not p.is_symlink() and p.is_file(), "source manifest missing")
    raw = p.read_bytes()
    require(digest(raw) == expected, "different release at deployment site")
    for name, sha in inventory(raw).items():
        p = root / name
        require(p.is_file() and not p.is_symlink() and digest(p.read_bytes()) == sha,
                "deployed source differs: " + name)


def install(root, data, package_hash, sums_hash):
    require(digest(data) == package_hash, "deployment ZIP hash mismatch")
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        raw = z.read("SOURCE_SHA256SUMS")
        require(digest(raw) == sums_hash, "manifest mismatch")
        sums = inventory(raw)
        names = z.namelist()
        require(len(set(names)) == len(names) and set(names) == set(sums) | {"SOURCE_SHA256SUMS"},
                "unexpected package member")
        parts = {}
        for name, sha in sums.items():
            require(z.getinfo(name).file_size <= 2000000, "source too large")
            parts[name] = z.read(name)
            require(digest(parts[name]) == sha, "source content mismatch")
    try:
        root.mkdir(mode=0o700)
    except FileExistsError:
        check_installed(root, sums_hash)
        return
    for name, content in list(parts.items()) + [("SOURCE_SHA256SUMS", raw)]:
        path = root / name
        with path.open("xb") as out:
            out.write(content)
            out.flush()
            os.fsync(out.fileno())
        if name.endswith((".sbatch", ".sh")):
            path.chmod(0o700)
    check_installed(root, sums_hash)


def invoke(root, mode, expected):
    require(socket.gethostname().split(".")[0] == "ibb-master", "wrong login host")
    require(not any(k.startswith(("SLURM_", "SBATCH_")) for k in os.environ),
            "unexpected scheduler login environment")
    if mode in ("GO_UB_ONCE", "GO_PS73_SEQUENCE_ONCE"):
        package_hash, sums_hash = expected
        install(root, sys.stdin.buffer.read(2097153), package_hash, sums_hash)
    else:
        if not root.exists() and not root.is_symlink() and mode == "STATUS":
            print("NO_DEPLOYMENT")
            return 0
        check_installed(root, expected[1])
    env = os.environ.copy()
    for name in ("BASH_ENV", "ENV", "PYTHONPATH", "PYTHONHOME", "CDPATH"):
        env.pop(name, None)
    # Selection rereads the original frozen reader, including its numerical dependencies.
    py = Path.home() / ".conda" / "envs" / "myenv" / "bin" / "python3"
    require(py.is_file() and digest(py.read_bytes()) ==
            "561c350efec08f1712162c4d649f4b668bacceb68388e973efec964f0073cd92", "field Python changed")
    py = str(py)
    if mode == "RETURN":
        return subprocess.call([py, "-I", "-B", str(root / "collect_ps73.py")], cwd=root, env=env)
    command = [py, "-I", "-B", str(root / "phase_controller.py")]
    if mode == "STATUS":
        return subprocess.call(command + ["status"], cwd=root, env=env)
    if mode == "RESUME_ACKNOWLEDGED":
        command += ["resume"]
    elif mode in ("GO_UB_ONCE", "GO_PS73_SEQUENCE_ONCE"):
        command += ["run", mode]
    else:
        raise ValueError("unknown action")
    key = "driver_%d_%d.log" % (time.time_ns(), os.getpid())
    with (root / key).open("xb") as log:
        p = subprocess.Popen(command, cwd=root, env=env, start_new_session=True,
                             stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
    print(json.dumps({"action": "DETACHED_CONTROLLER", "pid": p.pid, "mode": mode,
                      "log": key, "submission_status": "USE_STATUS"}))
    return 0


def main():
    os.umask(0o077)
    require(len(sys.argv) == 4, "mode and release hashes required")
    return invoke(Path.home() / "ps73_dev_ops_20261121", sys.argv[1], sys.argv[2:])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as err:
        print("NOT_STARTED_OR_INCOMPLETE:", err, file=sys.stderr)
        sys.exit(2)
