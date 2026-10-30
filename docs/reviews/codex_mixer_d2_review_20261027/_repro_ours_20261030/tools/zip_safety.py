"""Safety listing of a ZIP without extracting it.

Usage: python3 -I zip_safety.py <zip> <out.json>
Reports: entry count, files/dirs, total uncompressed size, duplicates,
case-insensitive duplicates, absolute / traversal paths, backslashes,
symlinks (unix mode in external_attr), encrypted entries, CRC test.
"""
import json
import stat
import sys
import zipfile
from collections import Counter


def main(zpath, outp):
    rep = {"zip": zpath}
    with zipfile.ZipFile(zpath) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        rep["n_entries"] = len(infos)
        rep["n_dirs"] = sum(1 for i in infos if i.is_dir())
        rep["n_files"] = sum(1 for i in infos if not i.is_dir())
        rep["total_uncompressed"] = sum(i.file_size for i in infos)
        rep["total_compressed"] = sum(i.compress_size for i in infos)
        c = Counter(names)
        rep["duplicates"] = sorted(n for n, k in c.items() if k > 1)
        cl = Counter(n.lower() for n in names)
        rep["case_duplicates"] = sorted(n for n, k in cl.items() if k > 1)
        bad = []
        for n in names:
            parts = n.replace("\\", "/").split("/")
            if n.startswith("/") or n.startswith("\\") or (len(n) > 1 and n[1] == ":"):
                bad.append(("absolute", n))
            if ".." in parts:
                bad.append(("traversal", n))
            if "\\" in n:
                bad.append(("backslash", n))
            if any(ord(ch) < 32 for ch in n):
                bad.append(("control_char", n))
        rep["bad_paths"] = bad
        links = []
        enc = []
        for i in infos:
            mode = (i.external_attr >> 16) & 0xFFFF
            if mode and stat.S_ISLNK(mode):
                links.append(i.filename)
            if i.flag_bits & 0x1:
                enc.append(i.filename)
        rep["symlinks"] = links
        rep["encrypted"] = enc
        rep["create_systems"] = sorted(Counter(i.create_system for i in infos).items())
        rep["testzip_first_bad"] = z.testzip()
        # top-level layout
        tops = Counter(n.split("/")[0] for n in names)
        rep["top_level"] = sorted(tops.items())
        rep["largest"] = sorted(((i.file_size, i.filename) for i in infos), reverse=True)[:15]
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: rep[k] for k in (
        "n_entries", "n_files", "n_dirs", "total_uncompressed", "duplicates",
        "case_duplicates", "bad_paths", "symlinks", "encrypted",
        "testzip_first_bad", "top_level", "create_systems")}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
