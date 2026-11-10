"""Read-only audit of packaged, redacted siteq evidence; never imports target code."""
import argparse
import ast
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re


def sha(data):
    return hashlib.sha256(data).hexdigest()


def manifest_check(manifest, wanted=None):
    rows = []
    for n, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        digest, name = line.split(None, 1)
        name = name.lstrip("*")
        if wanted is not None and name not in wanted:
            continue
        path = (manifest.parent / name).resolve()
        assert path.is_relative_to(manifest.parent.resolve()), name
        data = path.read_bytes()
        rows.append({"file": name, "bytes": len(data), "expected": digest,
                     "actual": sha(data), "ok": digest == sha(data), "line": n})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", required=True)
    ap.add_argument("--code-repo", help="Optional fixed repository with unchanged 19 scripts; read bytes only")
    ap.add_argument("--code-scripts", help="Optional direct scripts directory; otherwise use sibling ../codekey_sources/scripts when present")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    package = Path(args.package).resolve()
    repo = package / "repo"
    target = repo / "docs/data/rint2_siteq_20261109"
    prep = repo / "docs/reviews/rint2_siteq_prep_20261109"
    source = prep / "tools/siteq_probe.py"
    sb = source.read_bytes()
    tree = ast.parse(sb)
    checks_assign = next(n for n in tree.body if isinstance(n, ast.Assign)
                         and any(isinstance(t, ast.Name) and t.id == "CHECKS" for t in n.targets))
    spec = [(ast.literal_eval(n.elts[0]), ast.literal_eval(n.elts[1])) for n in checks_assign.value.elts]
    pin = package.joinpath("PIN.txt").read_text(encoding="utf-8").splitlines()[0]
    result = {"review_pin": pin, "scope": "packaged redacted bytes only; target code not executed",
              "source": {"sha256": sha(sb), "bytes": len(sb), "CHECKS_ast_count": len(spec)},
              "manifests": {}, "hosts": {}, "comparisons": {}, "limitations": []}
    result["manifests"]["data"] = manifest_check(target / "SHA256SUMS")
    result["manifests"]["prep"] = manifest_check(prep / "SHA256SUMS")
    wanted = {str(p.relative_to(package)).replace("\\", "/")
              for folder in (target, prep) for p in folder.rglob("*") if p.is_file()}
    result["manifests"]["outer_subset"] = manifest_check(package / "SHA256SUMS", wanted)
    all_ok = all(r["ok"] for group in result["manifests"].values() for r in group)
    blobs = {}
    for host in ("kgy", "gabia"):
        jp, lp = target / host / "siteq_result.json", target / host / "siteq.log"
        jb, lb = jp.read_bytes(), lp.read_bytes()
        data = json.loads(jb)
        blobs[host] = data
        checks = data["checks"]
        cmap = {r["id"]: r for r in checks}
        counts = dict(sorted(collections.Counter(r["status"] for r in checks).items()))
        lines = lb.decode("utf-8").splitlines()
        logged = []
        for lineno, line in enumerate(lines, 1):
            m = re.fullmatch(r"\[siteq\] (C\d+[a-z]?)\s+(PASS|INFO|WARN|FAIL|ERROR)\s+(.*?) -- (.*)", line)
            if m:
                cid, status, title, detail = m.groups()
                logged.append({"id": cid, "status": status, "title": title,
                               "detail": detail, "log_line": lineno})
        row_match = len(logged) == len(checks) and all(
            all(l[k] == r[k] for k in ("id", "status", "title", "detail"))
            for l, r in zip(logged, checks))
        summary = re.fullmatch(r"\[siteq\] ---- summary: (\{.*\})  \(([\d.]+) s\)", lines[-1])
        header = re.fullmatch(r"\[siteq\] (\S+)  machine (\S+)  pin ([a-f0-9]{40})  uid (\d+)  python (\S+)", lines[0])
        assert summary and header
        logcounts = json.loads(summary.group(1))
        hs = header.groups()
        delta = (datetime.datetime.fromisoformat(data["utc_end"].replace("Z", "+00:00"))
                 - datetime.datetime.fromisoformat(data["utc_start"].replace("Z", "+00:00"))).total_seconds()
        invariants = {
            "all_declared_ids_and_titles_match_source_CHECKS": [(r["id"], r["title"]) for r in checks] == spec,
            "unique_ids": len(cmap) == len(checks),
            "log_rows_exactly_match_json": row_match,
            "counts_recomputed_equal_json_and_log": counts == data["counts"] == logcounts,
            "header_matches": hs[:3] == (data["probe"], host, data["pin"]) and int(hs[3]) == data["uid"],
            "summary_seconds_match": float(summary.group(2)) == data["seconds"],
            "utc_rounding_consistent": abs(delta - data["seconds"]) < 1.1,
            "source_hash_matches_result": sha(sb) == data["probe_sha256"],
            "C02_env_matches_expect": cmap["C02"]["data"]["unit"] == cmap["C02"]["data"]["expected"] == data["expect"],
            "C03_head_matches_result": cmap["C03"]["data"]["git_identity"]["head"] == data["pin"],
            "expected_info_C28": cmap["C28"]["status"] == "INFO",
            "expected_C13b": cmap["C13b"]["status"] == ("INFO" if host == "gabia" else "PASS"),
            "expected_C02_and_C26": cmap["C02"]["status"] == cmap["C26"]["status"] == "PASS",
        }
        all_ok = all_ok and all(invariants.values())
        result["hosts"][host] = {
            "json_bytes": len(jb), "json_sha256": sha(jb), "log_bytes": len(lb), "log_sha256": sha(lb),
            "json_checks": len(checks), "log_check_rows": len(logged), "total_log_lines": len(lines),
            "counts_recomputed": counts, "invariants": invariants,
            "home_token_counts": {"json": jb.count(b"<HOME>"), "log": lb.count(b"<HOME>")},
            "reported_pin": data["pin"], "env_unit": cmap["C02"]["data"]["unit"],
            "C04": cmap["C04"]["data"], "C26_present_paths": list(cmap["C26"]["data"]),
            "plan_dirs": data["plan_dirs"], "uid": data["uid"], "seconds": data["seconds"],
            "expected_exit_from_source_rule_not_observed_receipt": 1 if counts.get("FAIL", 0) or counts.get("ERROR", 0) else 0,
            "log_row_checks": logged,
        }
    k, g = result["hosts"]["kgy"], result["hosts"]["gabia"]
    for name, left, right in (("pin", k["reported_pin"], g["reported_pin"]),
                              ("env_unit_C02", k["env_unit"], g["env_unit"]),
                              ("code_key_C04", k["C04"]["code_key_sha256"], g["C04"]["code_key_sha256"])):
        result["comparisons"][name] = {"same": left == right, "left": left, "right": right}
        all_ok = all_ok and left == right
    code_scripts = Path(args.code_scripts).resolve() if args.code_scripts else (
        Path(args.code_repo).resolve() / "scripts" if args.code_repo else
        Path(__file__).resolve().parent.parent / "codekey_sources/scripts")
    if code_scripts.is_dir():
        scripts = code_scripts
        chainbytes = (scripts / "rint_r_chain.py").read_bytes()
        chain_ast = ast.parse(chainbytes)
        names = next(ast.literal_eval(n.value) for n in chain_ast.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "CODE_FILES" for t in n.targets))
        file_records = [{"file": name, "sha256": sha((scripts / name).read_bytes())} for name in names]
        runner = next(r["sha256"] for r in file_records if r["file"] == "sdcp_gain_vox015_8arm.sh")
        # Independently transcribed schema of rint_r_chain.code_key, lines 1902-1913;
        # no import, target function execution, git command, or environment discovery.
        key_record = {"chain_head": k["reported_pin"], "runner_head": k["reported_pin"],
                      "chain_rel": "scripts/rint_r_chain.py", "runner_rel": "scripts/sdcp_gain_vox015_8arm.sh",
                      "files": file_records, "runner_files": file_records, "runner_sha256": runner,
                      "env_unit": k["env_unit"]}
        key_bytes = json.dumps(key_record, sort_keys=True, ensure_ascii=False, default=repr).encode("utf-8")
        key_sha = sha(key_bytes)
        result["code_key_reconstruction"] = {"method": "static schema; direct read_bytes/hashlib/json; target not imported",
                                             "source_root": str(scripts), "file_count": len(file_records),
                                             "key_record": key_record, "recomputed": key_sha,
                                             "matches_both_reports": key_sha == k["C04"]["code_key_sha256"] == g["C04"]["code_key_sha256"],
                                             "limit": "Uses the provided unchanged script bytes and reported siteq HEAD/env; does not retrieve original host checkout."}
        all_ok = all_ok and result["code_key_reconstruction"]["matches_both_reports"]
    result["limitations"] = [
        "Original host tgz, pre-redaction JSON/log bytes are absent: original SHA and substitution-only claims not independently verified.",
        "C04 omits the original host code_record/per-file hashes. Optional static expected-key reconstruction checks consistency with supplied script bytes, not authenticity of host checkout.",
        "Exit rc0 is a user screen report in README; JSON/log imply expected rc0 but contain no independent exit-code receipt.",
        "gabia plan_dirs is empty: C26 covers home/out/repo only; a future plan folder is not qualified.",
        "C02 equality concerns python-minor/numpy/scipy version unit only, not full host/numerical/runtime equivalence.",
        "This audit does not execute a probe, establish host authenticity, qualify production, or authorize runs.",
    ]
    result["all_packaged_byte_and_consistency_checks_pass"] = all_ok
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"all_packaged_checks_pass": all_ok,
                      "nested_data_manifest": len(result["manifests"]["data"]),
                      "nested_prep_manifest": len(result["manifests"]["prep"]),
                      "outer_subset": len(result["manifests"]["outer_subset"]),
                      "counts": {h: r["counts_recomputed"] for h, r in result["hosts"].items()}}, ensure_ascii=False))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
