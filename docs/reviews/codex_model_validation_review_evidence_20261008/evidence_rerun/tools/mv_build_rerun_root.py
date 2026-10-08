"""Build a rerun root for the Codex model-validation probes using OUR tree.

Usage: python3 -I -B mv_build_rerun_root.py BUNDLE_ROOT OUR_TREE RERUN_ROOT
 - source/<path> for every path in BUNDLE_ROOT/source_manifest.json is copied
   from OUR_TREE/<path> (our worktree HEAD), NOT from the bundle.
 - probes/ is copied byte-exact from the bundle (all read before use).
 - evidence/ starts empty (probes write their own outputs there).
Refuses if RERUN_ROOT exists and is non-empty, or if a sibling
'lhs_coverage_review_20260930/deps' exists (probe would add it to sys.path).
"""
import hashlib
import json
import os
import shutil
import sys


def main():
    bundle, tree, root = sys.argv[1:4]
    if os.path.exists(root) and os.listdir(root):
        sys.exit(f"REFUSE: rerun root not empty: {root}")
    sib = os.path.join(os.path.dirname(os.path.abspath(root)), "lhs_coverage_review_20260930", "deps")
    if os.path.exists(sib):
        sys.exit(f"REFUSE: sibling dependency cache exists: {sib}")
    os.makedirs(os.path.join(root, "evidence"), exist_ok=True)
    manifest = json.load(open(os.path.join(bundle, "source_manifest.json"), encoding="utf-8"))
    rows = []
    for e in manifest:
        src = os.path.join(tree, e["path"])
        dst = os.path.join(root, "source", e["path"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        data = open(dst, "rb").read()
        rows.append((e["path"], hashlib.sha256(data).hexdigest() == e["sha256"]))
    os.makedirs(os.path.join(root, "probes"))
    for fn in sorted(os.listdir(os.path.join(bundle, "probes"))):
        shutil.copyfile(os.path.join(bundle, "probes", fn), os.path.join(root, "probes", fn))
    same = sum(ok for _p, ok in rows)
    print(f"source copied from our tree: {len(rows)} files; sha256 equal to Codex manifest: {same}")
    for p, ok in rows:
        if not ok:
            print(f"  differs from Codex pin copy: {p}")


if __name__ == "__main__":
    main()
