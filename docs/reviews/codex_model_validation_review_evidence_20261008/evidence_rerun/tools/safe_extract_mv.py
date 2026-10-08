"""Safe ZIP extractor for the untrusted Codex model-validation bundle.

Rejects absolute paths, '..' components, backslash paths, drive letters,
symlinks (by external_attr mode), duplicate names, and anything that would
resolve outside the destination.  Destination must be a NEW empty directory.
Usage: python3 -I safe_extract_mv.py ZIP DEST
"""
import binascii
import hashlib
import os
import stat
import sys
import zipfile


def main():
    zpath, dest = sys.argv[1], sys.argv[2]
    if os.path.exists(dest):
        if os.listdir(dest):
            sys.exit(f"REFUSE: dest not empty: {dest}")
    else:
        os.makedirs(dest)
    dest_real = os.path.realpath(dest)
    seen = set()
    n_files = 0
    n_dirs = 0
    with zipfile.ZipFile(zpath) as zf:
        infos = zf.infolist()
        print(f"entries={len(infos)}")
        for zi in infos:
            name = zi.filename
            if name in seen:
                sys.exit(f"REFUSE duplicate: {name!r}")
            seen.add(name)
            if "\\" in name or name.startswith("/") or (len(name) > 1 and name[1] == ":"):
                sys.exit(f"REFUSE abs/backslash/drive: {name!r}")
            parts = [p for p in name.split("/") if p not in ("",)]
            if any(p in ("..", ".") for p in parts):
                sys.exit(f"REFUSE dot component: {name!r}")
            mode = (zi.external_attr >> 16) & 0xFFFF
            if mode and stat.S_ISLNK(mode):
                sys.exit(f"REFUSE symlink: {name!r}")
            target = os.path.realpath(os.path.join(dest_real, *parts)) if parts else dest_real
            if not (target == dest_real or target.startswith(dest_real + os.sep)):
                sys.exit(f"REFUSE escapes dest: {name!r}")
            if name.endswith("/"):
                os.makedirs(target, exist_ok=True)
                n_dirs += 1
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if os.path.lexists(target):
                sys.exit(f"REFUSE pre-existing target: {name!r}")
            data = zf.read(zi)
            if zi.CRC != (binascii.crc32(data) & 0xFFFFFFFF):
                sys.exit(f"REFUSE crc: {name!r}")
            with open(target, "xb") as fh:
                fh.write(data)
            os.chmod(target, 0o644)
            n_files += 1
            print(f"{hashlib.sha256(data).hexdigest()}  {len(data):>9}  {name}")
    print(f"extracted files={n_files} dirs={n_dirs}")


if __name__ == "__main__":
    main()
