"""Compare every file under a snapshot folder with a git tree listing.

Usage:
  python3 -I snap_vs_pin.py prep <snapshot_dir> <pin_sha> <batch_request_out>
      writes "<pin>:<path>" lines (one per snapshot file) for `git cat-file --batch`
  python3 -I snap_vs_pin.py check <snapshot_dir> <lstree_pin> <lstree_base> <batch_out> <report_json>
      compares (a) git blob id of local bytes vs pin ls-tree, (b) local bytes vs the
      raw blob bytes returned by `git cat-file --batch`, (c) pin blob id vs base tree.
"""
import hashlib
import json
import os
import sys


def files_under(root):
    out = []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            out.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/"))
    return sorted(out)


def lstree(path):
    d = {}
    with open(path, "rb") as f:
        for ln in f.read().decode("utf-8").splitlines():
            meta, p = ln.split("\t", 1)
            mode, typ, oid = meta.split()
            d[p] = (mode, typ, oid)
    return d


def git_blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def prep(snap, pin, outp):
    with open(outp, "w", encoding="utf-8", newline="\n") as f:
        for rel in files_under(snap):
            f.write("%s:%s\n" % (pin, rel))


def parse_batch(path, requested):
    raw = open(path, "rb").read()
    i = 0
    out = {}
    for req in requested:
        nl = raw.index(b"\n", i)
        head = raw[i:nl].decode("utf-8")
        i = nl + 1
        if head.endswith(" missing"):
            out[req] = None
            continue
        oid, typ, size = head.split()
        size = int(size)
        out[req] = (oid, typ, raw[i:i + size])
        i += size + 1  # trailing LF
    return out


def check(snap, ls_pin, ls_base, batch_out, rep_out):
    pin = lstree(ls_pin)
    base = lstree(ls_base)
    rels = files_under(snap)
    batch = parse_batch(batch_out, rels)
    rep = {"snapshot_files": len(rels), "not_in_pin": [], "blobid_ok": 0,
           "blobid_mismatch": [], "bytes_ok": 0, "bytes_mismatch": [],
           "mode_counts": {}, "pin_vs_base_same": 0, "pin_vs_base_diff": [],
           "not_in_base": [], "symlink_in_pin": []}
    for rel in rels:
        data = open(os.path.join(snap, rel), "rb").read()
        if rel not in pin:
            rep["not_in_pin"].append(rel)
            continue
        mode, typ, oid = pin[rel]
        rep["mode_counts"][mode] = rep["mode_counts"].get(mode, 0) + 1
        if mode == "120000":
            rep["symlink_in_pin"].append(rel)
        if git_blob_id(data) == oid:
            rep["blobid_ok"] += 1
        else:
            rep["blobid_mismatch"].append(rel)
        b = batch.get(rel)
        if b is not None and b[2] == data:
            rep["bytes_ok"] += 1
        else:
            rep["bytes_mismatch"].append(rel)
        if rel in base:
            if base[rel][2] == oid:
                rep["pin_vs_base_same"] += 1
            else:
                rep["pin_vs_base_diff"].append(rel)
        else:
            rep["not_in_base"].append(rel)
    with open(rep_out, "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    summ = {k: (v if not isinstance(v, list) else len(v)) for k, v in rep.items()}
    print(json.dumps(summ, ensure_ascii=False))
    for k in ("not_in_pin", "blobid_mismatch", "bytes_mismatch", "pin_vs_base_diff", "not_in_base"):
        if rep[k]:
            print(k, rep[k][:20])


if __name__ == "__main__":
    if sys.argv[1] == "prep":
        prep(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        check(*sys.argv[2:7])
