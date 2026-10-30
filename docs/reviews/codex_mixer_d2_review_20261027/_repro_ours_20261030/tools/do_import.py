"""Copy a selected subset of an extracted Codex review bundle into the repo folder.

Usage: python3 -I do_import.py <extract_root> <dest_dir> <plan.json> <report.json>
plan.json = {"include_globs": [...], "exclude_globs": [...]} (fnmatch on bundle-relative
paths, '/' separators).  A file is imported iff it matches an include glob and no
exclude glob.  Every imported file is checked against the bundle MANIFEST.sha256.
The report lists imported / excluded paths, sizes, CR-byte counts and manifest status.
"""
import fnmatch
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


def manifest(root):
    m = {}
    for ln in open(os.path.join(root, "MANIFEST.sha256"), encoding="utf-8").read().splitlines():
        if ln.strip():
            h, p = ln.split("  ", 1)
            m[p] = h
    return m


def main(src, dest, planp, repp):
    plan = json.load(open(planp, encoding="utf-8"))
    man = manifest(src)
    rep = {"imported": [], "excluded": [], "manifest_ok": 0, "manifest_bad": [],
           "not_in_manifest": [], "bytes_imported": 0, "bytes_excluded": 0}
    for rel in files_under(src):
        inc = any(fnmatch.fnmatchcase(rel, g) for g in plan["include_globs"])
        exc = any(fnmatch.fnmatchcase(rel, g) for g in plan["exclude_globs"])
        size = os.path.getsize(os.path.join(src, rel))
        if inc and not exc:
            data = open(os.path.join(src, rel), "rb").read()
            dst = os.path.join(dest, rel)
            if os.path.exists(dst):
                raise SystemExit("refusing to overwrite " + dst)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(os.path.join(src, rel), dst)
            h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
            if rel == "MANIFEST.sha256":
                pass
            elif rel not in man:
                rep["not_in_manifest"].append(rel)
            elif man[rel] == h:
                rep["manifest_ok"] += 1
            else:
                rep["manifest_bad"].append(rel)
            rep["imported"].append({"path": rel, "bytes": size, "cr": data.count(b"\r")})
            rep["bytes_imported"] += size
        else:
            rep["excluded"].append(rel)
            rep["bytes_excluded"] += size
    with open(repp, "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    print(json.dumps({"n_imported": len(rep["imported"]), "n_excluded": len(rep["excluded"]),
                      "manifest_ok": rep["manifest_ok"], "manifest_bad": rep["manifest_bad"],
                      "not_in_manifest": rep["not_in_manifest"],
                      "bytes_imported": rep["bytes_imported"], "bytes_excluded": rep["bytes_excluded"],
                      "files_with_cr": sum(1 for x in rep["imported"] if x["cr"])},
                     ensure_ascii=False))


if __name__ == "__main__":
    main(*sys.argv[1:5])
