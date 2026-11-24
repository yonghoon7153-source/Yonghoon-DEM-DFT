"""Replay only the registered reader from the shipped block and verify both file sets."""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile


PIN = "182be9d50d5838e1dbfeb246eaf6e9c13dab4bc2"
BLOCK = "d1ca3349811614ce7c78779c9391525970c28b094e4055d2096ed0371e81388d"
SOURCES = "f4629c60b3823f25ca48177998b361f82e91a03e0a43142c5074bea27577ec89"
TAR = "suyoung_setting2_contact_result.tar.gz"
EXPECTED = {
    TAR: "fc8e3d67a775eef6c67f171b64e382aba589949d5c8ece82e6a32c6d6546e669",
    "screen.txt": "56b52d23a531baafc8ab93e8615a56039d6cddbd2769fd866d0b9f3308b6835d",
}


def verify(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checksum_rows(raw):
    entries = {}
    for line in raw.decode("ascii").splitlines():
        value, name = line.split("  ", 1)
        name = name.removeprefix("./")
        verify(name not in entries, "duplicate checksum entry")
        entries[name] = value
    return entries


def extract_pinned(data, folder):
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for m in archive:
            p = PurePosixPath(m.name)
            verify(m.name not in seen and not p.is_absolute() and ".." not in p.parts and
                   p.as_posix() == m.name and not any(c in m.name for c in ":\\"),
                   "unsafe or duplicate archive member")
            seen.add(m.name)
            dest = folder.joinpath(*p.parts)
            if m.isdir():
                dest.mkdir(parents=True, exist_ok=True)
                continue
            verify(m.isfile() and 0 <= m.size <= 16*1024**2, "unexpected TAR entry")
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open("xb") as output:
                output.write(archive.extractfile(m).read())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("operator_block", "old_return", "new_return"):
        parser.add_argument(key, type=Path)
    args = parser.parse_args()
    block = args.operator_block.read_bytes()
    verify(digest(block) == BLOCK, "wrong delivered operator")
    marker = b"<<'SETTING2_CONTACT_SOURCES'\n"
    encoded = block.split(marker)[1].split(b"\nSETTING2_CONTACT_SOURCES\n")[0]
    source = base64.b64decode(b"".join(encoded.splitlines()), validate=True)
    verify(digest(source) == SOURCES, "wrong source tar")
    sums = checksum_rows((args.new_return/"SHA256SUMS").read_bytes())
    verify(sums == EXPECTED, "outer manifest mismatch")
    raw = {n:(args.new_return/n).read_bytes() for n in sums}
    verify({n:digest(b) for n,b in raw.items()} == sums, "outer artifact changed")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        pkg, result = root/"package", root/"result"
        extract_pinned(source, pkg)
        extract_pinned(raw[TAR], result)
        run = result/"run"
        checks = checksum_rows((run/"SHA256SUMS").read_bytes())
        current = {p.relative_to(run).as_posix():digest(p.read_bytes())
                   for p in run.rglob("*") if p.is_file() and p != run/"SHA256SUMS"}
        verify(current == checks and (run/"screen.txt").read_bytes() == raw["screen.txt"],
               "native file set or screen mismatch")
        verify((run/"RELEASE").read_text("ascii").strip() == PIN, "wrong release")
        subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(pkg/"app.py"), "recheck",
                        "--root", str(pkg), "--prior", str(args.old_return.resolve()), "--run", str(run)],
                       check=True)
        report = json.loads((run/"summary.json").read_bytes())
        print(f"OUTER_HASHES={len(sums)} INNER_HASHES={len(checks)}")
        print(f"PHI_DIFFERENCE={report['candidate_phi_m_abs_delta']} RETRIES={report['automatic_retries']}")


if __name__ == "__main__":
    main()
