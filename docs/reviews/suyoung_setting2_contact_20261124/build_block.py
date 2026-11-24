"""Build a standalone CPU1 WSL block from committed candidate and archived setting-2 sources."""
import argparse
import base64
import gzip
import hashlib
import io
from pathlib import Path, PurePosixPath
import subprocess
import tarfile


BASE = "9012b2492fb33d05eaa19bb2abe6c5ba98057a4f"
BASELINE_PIN = "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112"
BASELINE_BLOCK = "1b5a76a30c55e9fd45ec6b7a1ed6a708891b8abc11aa488abef788c363f19ed7"
BASELINE_TAR = "db385a40dcb12c8a17046af810bcf948b0e2436c4561d98bcba9378ed2a6545e"
BASELINE_MANIFEST = "7d698c085e250be40fd7d2bfdad7ae84233ddaa847bed4939d69d0ac343834b3"
RULE_PIN = "c858862722bf6e5eb587ccbd54e1eef7dd59aa27"
GATE = "suyoung_u6a_setting2_return_20261123/verify_setting2.py"
RULES = {
    GATE: "d2f203e23b56fbeb1609d02f249b9bd0099d1962b2720b5b635789c83be380e3",
    "suyoung_u6c_force_rule_20261122/force_rule.py": "145b5fe6f456e8b66c2a8cc422ff88648c82d07c4420482f06bc6da7a5b1b6db",
    "suyoung_u6c_force_rule_20261122/rule.json": "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4",
    "suyoung_u6c_doubling_readback_20261122/doubling.py": "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda",
}
CANDIDATE = "docs/reviews/suyoung_setting2_contact_20261124/"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sums(files):
    return "".join(f"{digest(raw)}  {name}\n" for name, raw in sorted(files.items())).encode("ascii")


def pack(files):
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=buf, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w|") as tar:
            for name, raw in sorted(files.items()):
                info = tarfile.TarInfo(name)
                info.size = len(raw)
                tar.addfile(info, io.BytesIO(raw))
    return buf.getvalue()


def unpack_verified(raw):
    files = {}
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        for item in tar:
            name = item.name
            p = PurePosixPath(name)
            if (not item.isfile() or not p.parts or p.is_absolute() or p.as_posix() != name
                    or ".." in p.parts or any(c in name for c in "\\\x00:\n\r") or name.casefold() in seen
                    or item.size > 16*1024**2):
                raise ValueError("unsafe or duplicate member")
            files[name] = tar.extractfile(item).read()
            seen.add(name.casefold())
    manifest = files.pop("SOURCE_SHA256SUMS", None)
    if sums(files) != manifest:
        raise ValueError("incomplete inner manifest")
    files["SOURCE_SHA256SUMS"] = manifest
    return files


def baseline(block):
    if digest(block) != BASELINE_BLOCK:
        raise ValueError("wrong baseline operator identity")
    encoded = block.split(b"<<'SETTING2_SOURCES'\n", 1)[1].split(b"\nSETTING2_SOURCES\n", 1)[0]
    raw = base64.b64decode(b"".join(encoded.splitlines()), validate=True)
    if digest(raw) != BASELINE_TAR:
        raise ValueError("wrong baseline source tar")
    files = unpack_verified(raw)
    if (files["RELEASE"].decode("ascii").strip() != BASELINE_PIN
            or digest(files["SOURCE_SHA256SUMS"]) != BASELINE_MANIFEST):
        raise ValueError("wrong baseline manifest or release")
    return {"baseline/" + name: raw for name, raw in files.items()}


def write_once(path, raw):
    if path.exists():
        if path.read_bytes() != raw:
            raise FileExistsError(path)
    else:
        with path.open("xb") as out:
            out.write(raw)


def build(repo, prior_block, out):
    git = ["git", "-c", "safe.directory=" + repo.as_posix(), "-C", str(repo)]
    pin = subprocess.check_output([*git, "rev-parse", "--verify", "HEAD^{commit}"]).decode().strip()
    subprocess.run([*git, "merge-base", "--is-ancestor", BASE, pin], check=True)
    files = baseline(prior_block.read_bytes())
    for name, threshold in RULES.items():
        raw = subprocess.check_output([*git, "show", RULE_PIN + ":docs/reviews/" + name])
        if digest(raw) != threshold:
            raise ValueError("historical reader differs: " + name)
        files["rule/" + ("gate.py" if name == GATE else name)] = raw
    for name in ("app.py", "correction.py", "run.sh"):
        files[name] = subprocess.check_output([*git, "show", pin + ":" + CANDIDATE + name])
    files["RELEASE"] = (pin + "\n").encode("ascii")
    files["SOURCE_SHA256SUMS"] = sums(files)
    archive = pack(files)
    if unpack_verified(archive) != files:
        raise ValueError("package round trip")
    preamble = b"""#!/usr/bin/env bash
set -euo pipefail
umask 077
[[ $# == 2 ]] || { echo 'Expected mode and original setting-2 F return directory' >&2; exit 2; }
case "$1" in CHECK_ONLY|GO_SUYOUNG_SETTING2_CONTACT_ONCE) ;; *) echo 'Unknown mode' >&2; exit 2 ;; esac
prior=$(realpath -e -- "$2")
[[ -d "$prior" ]]
pkg=$(mktemp -d)
cd -- "$pkg"
base64 -d > source.tar.gz <<'SETTING2_CONTACT_SOURCES'
"""
    trailer = f"""SETTING2_CONTACT_SOURCES
printf '%s  source.tar.gz\\n' '{digest(archive)}' | sha256sum --strict --check -
tar -xzf source.tar.gz
[[ $(cat RELEASE) == '{pin}' ]]
exec bash run.sh "$1" "$prior"
""".encode("ascii")
    name = "PASTE_SUYOUNG_SETTING2_CONTACT_" + pin[:12] + "_1124.txt"
    data = preamble + base64.encodebytes(archive) + trailer
    out.mkdir(parents=True, exist_ok=True)
    write_once(out / name, data)
    write_once(out / (name + ".sha256"), sums({name: data}))
    print(name, digest(data), digest(archive), len(files))


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for param in ("repo", "baseline_block", "output"):
        p.add_argument(param, type=Path)
    args = p.parse_args()
    build(args.repo.resolve(), args.baseline_block, args.output)
