"""Assemble verification.json for one review from the saved check outputs.

Usage: python3 -I assemble_verification.py <tag d2|d3> <work_root> <ligg_clone_or_-> <out.json>
Reads (under <work_root>/out): safety_<tag>.json, man_<tag>_top.json, [man_d2_liggghts.json],
snapcheck_<tag>.json, import_<tag>.json, gatediff_<tag>.txt, z_<tag>pin.bin, z_<tag>gate.bin,
[lstree_486a57cf.txt]; and the extracted bundle under <work_root>/x_<tag>.
Recomputes the cheap identities (tree listings, baseline blob ids, LIGGGHTS copies).
"""
import hashlib
import json
import os
import sys

PINS = {"d2": ("045e0b3098e8fe5a64d6eb0da310da776e68f995", "34782a1874435e317f44c9d8f2045d53ceaf4dcc"),
        "d3": ("e0daf7b234bcc7935259d786e270268372abe2a2", "9c2f7b47fd4559ee4c08f23e667cdae92badbb04")}
ZIPS = {"d2": "codex_mixer_d2_independent_review_20261027.zip",
        "d3": "codex_mixer_d3_independent_review_20261027.zip"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def blob_id(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def lsz(p):
    d = {}
    for rec in open(p, "rb").read().split(b"\0"):
        if rec:
            m, path = rec.split(b"\t", 1)
            mode, t, o = m.decode().split()
            d[path.decode("utf-8")] = (mode, t, o)
    return d


def main(tag, root, ligg, outp):
    out = os.path.join(root, "out")
    x = os.path.join(root, "x_" + tag)
    J = lambda n: json.load(open(os.path.join(out, n), encoding="utf-8"))
    pin, gate = PINS[tag]
    safety = J("safety_%s.json" % tag)
    v = {"schema": "import_verification/1", "review": tag, "pin": pin, "gate_candidate": gate,
         "received_zip": {"name": ZIPS[tag], "bytes": os.path.getsize(safety["zip"]),
                          "sha256": sha(open(safety["zip"], "rb").read())},
         "zip_safety": {k: safety[k] for k in ("n_entries", "n_files", "n_dirs", "total_uncompressed",
                                               "duplicates", "case_duplicates", "bad_paths", "symlinks",
                                               "encrypted", "testzip_first_bad")}}
    mt = J("man_%s_top.json" % tag)
    v["codex_manifest_top"] = {k: (mt[k] if not isinstance(mt[k], list) else mt[k]) for k in mt}
    if tag == "d2":
        v["codex_manifest_liggghts"] = J("man_d2_liggghts.json")
    sc = J("snapcheck_%s.json" % tag)
    v["snapshot_vs_pin_blobs"] = {
        "method": "git ls-tree -r <pin> blob id of local bytes + raw bytes from git cat-file --batch <pin>:<path>; "
                  "pin blob id vs base tree (4c69070ad)",
        "snapshot_files": sc["snapshot_files"], "not_in_pin": sc["not_in_pin"],
        "blob_id_equal": sc["blobid_ok"], "raw_bytes_equal": sc["bytes_ok"],
        "blob_id_mismatch": sc["blobid_mismatch"], "raw_bytes_mismatch": sc["bytes_mismatch"],
        "pin_blob_equal_to_base_tree": sc["pin_vs_base_same"], "pin_vs_base_diff": sc["pin_vs_base_diff"],
        "not_in_base": sc["not_in_base"], "mode_counts": sc["mode_counts"]}
    tl = {}
    for name, ref in (("tree.json", "z_%spin.bin" % tag), ("gate_candidate_tree.json", "z_%sgate.bin" % tag)):
        t = json.load(open(os.path.join(x, tag, name), encoding="utf-8"))
        L = lsz(os.path.join(out, ref))
        Jt = {e["path"]: (e["mode"], e["type"], e["sha"]) for e in t["tree"] if e["type"] != "tree"}
        tl[name] = {"commit": t["sha"], "nontree_entries": len(Jt), "local_ls_tree_entries": len(L),
                    "identical_to_git_ls_tree_r": Jt == L, "truncated": t["truncated"],
                    "sha256": sha(open(os.path.join(x, tag, name), "rb").read())}
    v["github_tree_listings_vs_local_ls_tree"] = tl
    changed = open(os.path.join(out, "gatediff_%s.txt" % tag), encoding="utf-8").read().split()
    code = [p for p in changed if p.split("/")[0] in ("scripts", "webapp", "dem_scripts", ".github")]
    gp = json.load(open(os.path.join(x, "gate_pin_comparison.json"), encoding="utf-8"))
    gp = [g for g in gp if g["tag"] == tag][0]
    v["gate_candidate_vs_pin_git_diff"] = {"changed": len(changed), "code_changed": code,
                                          "codex_all_changed_count": gp["all_changed_count"],
                                          "codex_code_changed": gp["code_changed"],
                                          "agree": len(changed) == gp["all_changed_count"] and code == gp["code_changed"]}
    if tag == "d2":
        base = {}
        for ln in open(os.path.join(out, "lstree_486a57cf.txt"), encoding="utf-8").read().splitlines():
            m, p = ln.split("\t", 1)
            base[p.split("/")[-1]] = m.split()[2]
        res = {}
        for f in sorted(os.listdir(os.path.join(x, "d2", "baseline"))):
            b = open(os.path.join(x, "d2", "baseline", f), "rb").read()
            res[f] = {"blob_id": blob_id(b), "commit_486a57cf_blob": base.get(f),
                      "equal": blob_id(b) == base.get(f)}
        v["baseline_vs_486a57cf"] = res
        if ligg != "-":
            head = open(os.path.join(ligg, ".git", "HEAD"), encoding="utf-8").read().strip()
            m = json.load(open(os.path.join(x, "liggghts", "manifest.json"), encoding="utf-8"))
            same = {e["path"]: open(os.path.join(x, "liggghts", e["path"]), "rb").read()
                    == open(os.path.join(ligg, e["path"]), "rb").read() for e in m}
            v["liggghts_copies_vs_local_clone"] = {
                "local_clone_head": head, "equal": sum(same.values()), "of": len(same),
                "note": "local LIGGGHTS-PUBLIC clone in the session scratch (FETCH_HEAD = 3d5c00f of "
                        "github.com/CFDEMproject/LIGGGHTS-PUBLIC); its work tree cleanliness was not checked with git"}
    imp = J("import_%s.json" % tag)
    v["import"] = {"imported_files": len(imp["imported"]), "excluded_files": len(imp["excluded"]),
                   "imported_bytes": imp["bytes_imported"], "excluded_bytes": imp["bytes_excluded"],
                   "imported_verified_against_codex_manifest": imp["manifest_ok"],
                   "manifest_mismatch": imp["manifest_bad"], "not_in_manifest": imp["not_in_manifest"],
                   "imported_files_with_cr_bytes": sum(1 for i in imp["imported"] if i["cr"]),
                   "excluded": imp["excluded"]}
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(json.dumps({k: (v[k] if k in ("received_zip",) else "ok") for k in v}, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main(*sys.argv[1:5])
