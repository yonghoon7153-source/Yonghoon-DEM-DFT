"""Compare our probe rerun outputs with the Codex bundle evidence.

Usage: python3 -I -B mv_compare.py BUNDLE_EVIDENCE OUR_OUT OUT_JSON
For every JSON pair: parsed equality, raw-byte equality (and whether the only
byte difference is CRLF), and a leaf walk recording max |abs| / max rel diff
over numeric leaves plus every non-numeric difference (keys, strings, types).
"""
import json
import math
import os
import sys

PAIRS = [
    ("mv_anchor_porosity", "mv_anchor_porosity_result.json"),
    ("mv_pressure_arithmetic", "mv_pressure_arithmetic_result.json"),
    ("mv_softening_scaling", "mv_softening_scaling_result.json"),
    ("mv_softening_frozen_reweight", "mv_softening_frozen_reweight_result.json"),
    ("mv_stress_probe", "mv_stress_arithmetic.json"),
    ("mv_stress_core_probe", "mv_stress_core_controls.json"),
    ("mv_stress_portability", "mv_stress_portability.json"),
]
STDOUTS = ["mv_anchor_porosity", "mv_pressure_arithmetic", "mv_softening_scaling",
           "mv_softening_frozen_reweight", "mv_stress_probe", "mv_stress_core_probe",
           "mv_stress_portability"]


def walk(a, b, path, acc):
    if isinstance(a, bool) or isinstance(b, bool):
        if a != b:
            acc["other"].append(dict(path=path, codex=a, ours=b))
        return
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        acc["n_numeric"] += 1
        if a == b or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b)):
            return
        d = abs(a - b)
        rel = d / max(abs(a), abs(b))
        acc["n_numeric_diff"] += 1
        if d > acc["max_abs"]:
            acc["max_abs"], acc["max_abs_path"] = d, path
        if rel > acc["max_rel"]:
            acc["max_rel"], acc["max_rel_path"] = rel, path
        acc["numeric_diffs"].append(dict(path=path, codex=a, ours=b, abs=d, rel=rel))
        return
    if type(a) is not type(b):
        acc["other"].append(dict(path=path, codex=a, ours=b, note="type differs"))
        return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                acc["other"].append(dict(path=f"{path}/{k}", note="key only in " + ("codex" if k in a else "ours")))
            else:
                walk(a[k], b[k], f"{path}/{k}", acc)
        return
    if isinstance(a, list):
        if len(a) != len(b):
            acc["other"].append(dict(path=path, note=f"list length codex {len(a)} ours {len(b)}"))
        for i, (u, v) in enumerate(zip(a, b)):
            walk(u, v, f"{path}[{i}]", acc)
        return
    if a != b:
        acc["other"].append(dict(path=path, codex=a if len(str(a)) < 300 else str(a)[:300] + "…",
                                 ours=b if len(str(b)) < 300 else str(b)[:300] + "…"))


def main():
    ev, ours, out = sys.argv[1:4]
    rows = []
    for probe, fn in PAIRS:
        pa, pb = os.path.join(ev, fn), os.path.join(ours, fn)
        ra, rb = open(pa, "rb").read(), open(pb, "rb").read()
        a, b = json.loads(ra.decode("utf-8")), json.loads(rb.decode("utf-8"))
        acc = dict(n_numeric=0, n_numeric_diff=0, max_abs=0.0, max_abs_path=None, max_rel=0.0,
                   max_rel_path=None, numeric_diffs=[], other=[])
        walk(a, b, "", acc)
        rows.append(dict(probe=probe, file=fn, bytes_codex=len(ra), bytes_ours=len(rb),
                         bytes_equal=ra == rb, bytes_equal_after_crlf_normalise=ra.replace(b"\r\n", b"\n") == rb.replace(b"\r\n", b"\n"),
                         parsed_equal=a == b, **acc))
    std = []
    for stem in STDOUTS:
        fa = os.path.join(ev, f"{stem}.stdout.txt")
        fb = os.path.join(ours, f"{stem}.stdout.txt")
        ra = open(fa, "rb").read() if os.path.isfile(fa) else None
        rb = open(fb, "rb").read()
        if ra is None:
            std.append(dict(probe=stem, codex_stdout="(번들에 없음)", ours_bytes=len(rb)))
            continue
        ta = ra.replace(b"\r\n", b"\n").decode("utf-8")
        tb = rb.replace(b"\r\n", b"\n").decode("utf-8")
        la, lb = ta.splitlines(), tb.splitlines()
        diff_lines = [(i + 1, x, y) for i, (x, y) in enumerate(zip(la, lb)) if x != y]
        std.append(dict(probe=stem, bytes_codex=len(ra), bytes_ours=len(rb), bytes_equal=ra == rb,
                        text_equal_after_crlf_normalise=ta == tb, n_lines_codex=len(la), n_lines_ours=len(lb),
                        differing_lines=[dict(line=i, codex=x, ours=y) for i, x, y in diff_lines][:20]))
    res = dict(result_json_pairs=rows, stdout_pairs=std)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    for r in rows:
        print(f"{r['probe']:<30} parsed_equal={r['parsed_equal']!s:<5} bytes_equal={r['bytes_equal']!s:<5} "
              f"crlf_only={r['bytes_equal_after_crlf_normalise']!s:<5} numeric={r['n_numeric']} "
              f"num_diff={r['n_numeric_diff']} max_abs={r['max_abs']:.3e} max_rel={r['max_rel']:.3e} other={len(r['other'])}")
        for o in r["other"][:12]:
            print("    other:", json.dumps(o, ensure_ascii=False)[:400])
        for nd in r["numeric_diffs"][:6]:
            print("    num:", json.dumps(nd, ensure_ascii=False)[:300])
    print("--- stdout")
    for s in std:
        print(json.dumps({k: v for k, v in s.items() if k != "differing_lines"}, ensure_ascii=False))
        for d in s.get("differing_lines", [])[:6]:
            print("    line", d["line"], "| codex:", d["codex"][:160], "| ours:", d["ours"][:160])


if __name__ == "__main__":
    main()
