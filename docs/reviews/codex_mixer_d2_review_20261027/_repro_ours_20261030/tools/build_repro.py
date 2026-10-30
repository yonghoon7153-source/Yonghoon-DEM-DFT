"""Build a fresh reproduction tree from OUR worktree using a snapshot's path list.

Usage: python3 -I build_repro.py <zip_snapshot_dir> <worktree_root> <dest_snapshot_dir>
Copies every file listed under the ZIP snapshot (except PIN.txt) from the worktree
(our base commit) into dest, then confirms the copied bytes equal the ZIP snapshot
bytes. Refuses to write into a non-empty destination.
"""
import hashlib
import json
import os
import shutil
import sys


def files_under(root):
    out = []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            out.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/"))
    return sorted(out)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(snap, wt, dest):
    if os.path.exists(dest) and os.listdir(dest):
        raise SystemExit("destination not empty: " + dest)
    rels = [r for r in files_under(snap) if r != "PIN.txt"]
    same = 0
    diff = []
    for rel in rels:
        src = os.path.join(wt, rel)
        dst = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        if sha(dst) == sha(os.path.join(snap, rel)):
            same += 1
        else:
            diff.append(rel)
    print(json.dumps({"copied_from_worktree": len(rels), "equal_to_zip_snapshot": same,
                      "differ": diff}, ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:4])
