"""Verify sha256sum-style manifests and a JSON [{path, sha256}] manifest.

Usage:
  python3 -I verify_manifest.py sums <root> <manifest_relpath> [--exclude-self] [--complete]
  python3 -I verify_manifest.py json <root> <manifest_relpath>
Prints a JSON report: entries, ok, mismatch, missing, (with --complete) files under
root that the manifest does not list (excluding the manifest itself).
"""
import hashlib
import json
import os
import re
import sys

LINE = re.compile(r"^([0-9a-fA-F]{64}) [ *](.+)$")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def all_files(root):
    out = set()
    for dp, dn, fn in os.walk(root):
        for f in fn:
            out.add(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/"))
    return out


def sums(root, mrel, complete):
    mpath = os.path.join(root, mrel)
    base = os.path.dirname(mpath)
    raw = open(mpath, "rb").read()
    rep = {"manifest": mrel, "manifest_sha256": hashlib.sha256(raw).hexdigest(),
           "crlf_lines": raw.count(b"\r\n"), "bad_lines": [], "entries": 0,
           "ok": 0, "mismatch": [], "missing": [], "dup_paths": []}
    seen = set()
    for ln in raw.decode("utf-8").splitlines():
        if not ln.strip():
            continue
        m = LINE.match(ln)
        if not m:
            rep["bad_lines"].append(ln[:120])
            continue
        h, rel = m.group(1).lower(), m.group(2)
        rep["entries"] += 1
        if rel in seen:
            rep["dup_paths"].append(rel)
        seen.add(rel)
        p = os.path.join(base, rel)
        if not os.path.isfile(p):
            rep["missing"].append(rel)
            continue
        if sha(p) == h:
            rep["ok"] += 1
        else:
            rep["mismatch"].append(rel)
    if complete:
        files = all_files(base)
        me = os.path.relpath(mpath, base).replace(os.sep, "/")
        files.discard(me)
        rep["unlisted"] = sorted(files - seen)
    return rep


def jsonman(root, mrel):
    mpath = os.path.join(root, mrel)
    base = os.path.dirname(mpath)
    items = json.load(open(mpath, encoding="utf-8"))
    rep = {"manifest": mrel, "entries": len(items), "ok": 0, "mismatch": [], "missing": []}
    listed = set()
    for it in items:
        rel = it["path"]
        listed.add(rel)
        p = os.path.join(base, rel)
        if not os.path.isfile(p):
            rep["missing"].append(rel)
        elif sha(p) == it["sha256"].lower():
            rep["ok"] += 1
        else:
            rep["mismatch"].append(rel)
    files = all_files(base)
    files.discard(os.path.basename(mpath))
    rep["unlisted"] = sorted(files - listed)
    return rep


if __name__ == "__main__":
    mode, root, mrel = sys.argv[1], sys.argv[2], sys.argv[3]
    if mode == "sums":
        r = sums(root, mrel, "--complete" in sys.argv)
    else:
        r = jsonman(root, mrel)
    print(json.dumps(r, ensure_ascii=False, indent=1))
