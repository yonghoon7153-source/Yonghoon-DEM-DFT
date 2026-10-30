"""Deep-compare two JSON files (or two case folders) and report differing leaves.

Usage:
  python3 -I deepcmp.py json <a.json> <b.json>
  python3 -I deepcmp.py cases <a_cases_dir> <b_cases_dir>
For 'cases': per file, .in compared as bytes; .json compared parsed; .log compared
after CRLF->LF normalisation and with absolute paths masked.
Paths/interpreter/timestamp-like strings are reported separately as 'volatile'.
"""
import json
import os
import re
import sys

VOLATILE_KEYS = {"cwd", "python", "executable", "sys_executable", "started", "finished",
                 "timestamp", "time", "elapsed_s", "duration_s", "host", "user", "platform"}
PATHISH = re.compile(r"([A-Za-z]:\\|/tmp/|/home/|\\\\|Users\\)")


def walk(a, b, path, out):
    if type(a) != type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        out.append((path, "type", repr(a)[:120], repr(b)[:120]))
        return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((path + "/" + str(k), "missing", k in a, k in b))
            else:
                walk(a[k], b[k], path + "/" + str(k), out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((path, "len", len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, "%s[%d]" % (path, i), out)
    else:
        if a != b:
            out.append((path, "value", repr(a)[:160], repr(b)[:160]))


def classify(diffs):
    vol, real = [], []
    for d in diffs:
        p = d[0]
        leaf = p.rsplit("/", 1)[-1].split("[")[0]
        s = " ".join(str(x) for x in d[2:])
        if leaf in VOLATILE_KEYS or PATHISH.search(s):
            vol.append(d)
        else:
            real.append(d)
    return vol, real


def cmp_json(a, b):
    A = json.load(open(a, encoding="utf-8"))
    B = json.load(open(b, encoding="utf-8"))
    out = []
    walk(A, B, "", out)
    return classify(out)


def norm_log(raw, root_hint):
    t = raw.decode("utf-8", "replace").replace("\r\n", "\n")
    t = re.sub(r"[A-Za-z]:\\[^\s'\"]*", "<PATH>", t)
    t = re.sub(r"/(tmp|home|root)/[^\s'\"]*", "<PATH>", t)
    return t


def cmp_cases(da, db):
    rep = {}
    names = sorted(set(os.listdir(da)) | set(os.listdir(db)))
    for n in names:
        pa, pb = os.path.join(da, n), os.path.join(db, n)
        if not (os.path.isdir(pa) and os.path.isdir(pb)):
            rep[n] = {"only_in": "a" if os.path.isdir(pa) else "b"}
            continue
        files = sorted(set(os.listdir(pa)) | set(os.listdir(pb)))
        r = {}
        for f in files:
            fa, fb = os.path.join(pa, f), os.path.join(pb, f)
            if not (os.path.isfile(fa) and os.path.isfile(fb)):
                r[f] = "only_in_" + ("a" if os.path.isfile(fa) else "b")
                continue
            ra, rb = open(fa, "rb").read(), open(fb, "rb").read()
            if ra == rb:
                r[f] = "bytes_equal"
            elif f.endswith(".json"):
                vol, real = cmp_json(fa, fb)
                if not real and not vol:
                    r[f] = "json_equal(newline/format only)"
                elif not real:
                    r[f] = {"json_volatile_only": [list(map(str, v)) for v in vol[:5]]}
                else:
                    r[f] = {"json_real_diffs": [list(map(str, v)) for v in real[:8]],
                            "n_real": len(real), "n_volatile": len(vol)}
            elif f.endswith(".log"):
                if norm_log(ra, da) == norm_log(rb, db):
                    r[f] = "log_equal_after_newline_and_path_masking"
                else:
                    r[f] = {"log_differs": True, "a": norm_log(ra, da)[:300], "b": norm_log(rb, db)[:300]}
            else:
                r[f] = {"bytes_differ": True, "len_a": len(ra), "len_b": len(rb),
                        "equal_after_crlf_norm": ra.replace(b"\r\n", b"\n") == rb.replace(b"\r\n", b"\n")}
        rep[n] = r
    return rep


if __name__ == "__main__":
    if sys.argv[1] == "json":
        vol, real = cmp_json(sys.argv[2], sys.argv[3])
        print(json.dumps({"n_real_diffs": len(real), "n_volatile_diffs": len(vol),
                          "real": [list(map(str, d)) for d in real[:40]],
                          "volatile": [list(map(str, d)) for d in vol[:40]]},
                         ensure_ascii=False, indent=1))
    else:
        print(json.dumps(cmp_cases(sys.argv[2], sys.argv[3]), ensure_ascii=False, indent=1))
