"""Per-file identity check of the Codex bundle source/ against git revisions.

Usage: python3 -I -B mv_source_identity.py BUNDLE_ROOT REPO OUT_JSON
Reads only; writes OUT_JSON.  Compares each source/<path> byte-for-byte with
`git show <rev>:<path>` for rev in (pin 61ebd181b, HEAD 50ec7273b) and checks
the bundle's own source_manifest.json (git blob sha, sha256, bytes),
source_plan.json and BUNDLE_MANIFEST.json for internal consistency.
"""
import hashlib
import json
import os
import subprocess
import sys

PIN = "61ebd181b1ae5b47a76fe69d4400e4a3950dc8a3"
HEAD = "50ec7273b962ee6f63807bfbba75429cedea4f45"


def git_blob(repo, rev, path):
    p = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                       capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout


def git_blob_sha(data):
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def main():
    root, repo, out = sys.argv[1], sys.argv[2], sys.argv[3]
    src_root = os.path.join(root, "source")
    manifest = json.load(open(os.path.join(root, "source_manifest.json"), encoding="utf-8"))
    plan = json.load(open(os.path.join(root, "source_plan.json"), encoding="utf-8"))
    bundle = json.load(open(os.path.join(root, "BUNDLE_MANIFEST.json"), encoding="utf-8"))
    on_disk = []
    for dp, _dn, fns in os.walk(src_root):
        for fn in fns:
            on_disk.append(os.path.relpath(os.path.join(dp, fn), src_root).replace(os.sep, "/"))
    on_disk.sort()
    man_paths = sorted(e["path"] for e in manifest)
    plan_paths = sorted(e["path"] for e in plan["files"])
    rows = []
    n_pin = n_head = n_man = 0
    for path in on_disk:
        data = open(os.path.join(src_root, path), "rb").read()
        sha256 = hashlib.sha256(data).hexdigest()
        bsha = git_blob_sha(data)
        pin = git_blob(repo, PIN, path)
        head = git_blob(repo, HEAD, path)
        m = next((e for e in manifest if e["path"] == path), None)
        pl = next((e for e in plan["files"] if e["path"] == path), None)
        same_pin = pin is not None and pin == data
        same_head = head is not None and head == data
        man_ok = (m is not None and m["sha256"] == sha256 and m["sha"] == bsha
                  and m["bytes"] == len(data) and m["ref"] == PIN)
        plan_ok = pl is not None and pl["sha"] == bsha and pl["size"] == len(data)
        n_pin += same_pin
        n_head += same_head
        n_man += man_ok and plan_ok
        rows.append({
            "path": path, "bytes": len(data), "sha256": sha256, "git_blob": bsha,
            "identical_to_pin_61ebd181b": same_pin,
            "identical_to_head_50ec7273b": same_head,
            "head_blob": git_blob_sha(head) if head is not None else None,
            "manifest_and_plan_consistent": bool(man_ok and plan_ok),
        })
    # BUNDLE_MANIFEST consistency over all bundle files except itself
    bm_rows = []
    bm_ok = 0
    for e in bundle["files"]:
        p = os.path.join(root, e["path"])
        data = open(p, "rb").read() if os.path.isfile(p) else None
        ok = data is not None and len(data) == e["bytes"] and hashlib.sha256(data).hexdigest() == e["sha256"]
        bm_ok += ok
        if not ok:
            bm_rows.append(e["path"])
    all_bundle = []
    for dp, _dn, fns in os.walk(root):
        for fn in fns:
            all_bundle.append(os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/"))
    listed = {e["path"] for e in bundle["files"]}
    unlisted = sorted(set(all_bundle) - listed)
    res = {
        "pin": PIN, "head": HEAD,
        "n_source_files_on_disk": len(on_disk),
        "n_manifest_entries": len(manifest),
        "n_plan_entries": len(plan["files"]),
        "manifest_paths_equal_disk": man_paths == on_disk,
        "plan_paths_equal_disk": plan_paths == on_disk,
        "n_identical_to_pin": n_pin,
        "n_identical_to_head": n_head,
        "n_manifest_plan_consistent": n_man,
        "differs_from_head": [r["path"] for r in rows if not r["identical_to_head_50ec7273b"]],
        "differs_from_pin": [r["path"] for r in rows if not r["identical_to_pin_61ebd181b"]],
        "bundle_manifest_entries": len(bundle["files"]),
        "bundle_manifest_ok": bm_ok,
        "bundle_manifest_bad": bm_rows,
        "bundle_files_not_in_bundle_manifest": unlisted,
        "files": rows,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(json.dumps({k: v for k, v in res.items() if k != "files"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
