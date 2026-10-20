"""Read-only source, scope and receipt audit; generated evidence stays in this review."""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import os
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT.parent
OLD = WORK / "lhs214s_recheck_20261019"
OUT = ROOT / "evidence" / "scope"
OUT.mkdir(parents=True, exist_ok=True)
TMP = ROOT / "tmp" / "scope"
TMP.mkdir(parents=True, exist_ok=True)
MODE = sys.argv[1] if len(sys.argv) > 1 else "metadata"
LABEL = sys.argv[2] if len(sys.argv) > 2 else "new"
SRC = (ROOT if LABEL == "new" else OLD) / "source"
sys.dont_write_bytecode = True
deps = [WORK / "lhs_coverage_review_20260930/deps",
        WORK / "gen2_network_reverify3_20261007/deps"]
sys.path[:0] = list(map(str, [SRC / "scripts", SRC / "webapp", *deps]))
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
os.environ.update(PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1",
                  PYTHONIOENCODING="utf-8", TEMP=str(TMP), TMP=str(TMP),
                  SUPABASE_URL="", SUPABASE_KEY="")
for key, name in (("WEBAPP_UPLOAD_FOLDER", "uploads"), ("WEBAPP_RESULTS_FOLDER", "results"),
                  ("WEBAPP_ARCHIVE_FOLDER", "archive"), ("WEBAPP_MPM_LAB_FOLDER", "mpm_lab"),
                  ("MPLCONFIGDIR", "mpl")):
    os.environ[key] = str(TMP / name)
tempfile.tempdir = str(TMP)


def native(p):
    s = str(p.resolve())
    return Path("\\\\?\\" + s) if os.name == "nt" and not s.startswith("\\\\?\\") else Path(s)


def read(p):
    return native(p).read_bytes()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def blob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def load(p):
    return json.loads(read(p))


def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf8")


def assigned(path, names):
    source = read(path).decode("utf8")
    tree = ast.parse(source)
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    try:
                        value = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        value = dict(expression=ast.get_source_segment(source, node.value))
                    values[target.id] = dict(value=value, line=node.lineno)
    return values


def metadata():
    trees = {label: load(root / "evidence/tree.json") for label, root in (("old", OLD), ("new", ROOT))}
    entries = {label: {e["path"]: e for e in tree["tree"] if e["type"] == "blob"}
               for label, tree in trees.items()}
    a, b = entries["old"], entries["new"]
    modified = sorted(p for p in a.keys() & b.keys() if a[p]["sha"] != b[p]["sha"])
    added, deleted = sorted(b.keys() - a.keys()), sorted(a.keys() - b.keys())
    listed = load(ROOT / "evidence/tree_diff.json")
    integrity = {}
    for label, root in (("old", OLD), ("new", ROOT)):
        manifest = load(root / "source_manifest.json")
        bad, total = [], 0
        for row in manifest["files"]:
            data = read(root / "source" / row["path"])
            total += len(data)
            sha, git_blob = sha_bytes(data), blob(data)
            tree_blob = entries[label][row["path"]]["sha"]
            if not (sha == row["sha256"] and git_blob == row["git_blob"] == tree_blob and len(data) == row["bytes"]):
                bad.append(dict(path=row["path"], sha256=sha, git_blob=git_blob, tree_blob=tree_blob))
        integrity[label] = dict(pin=manifest["pin"], files=len(manifest["files"]),
                                bytes=total, problems=bad, tree_truncated=trees[label].get("truncated"))
    scopes = {}
    constants = {}
    for label, root in (("old", OLD), ("new", ROOT)):
        source = root / "source"
        v = assigned(source / "scripts/run_network_194_parallel.py", {"CODE_FILES", "HANDOVER_FILES"})
        hashes = {name: {p: sha_bytes(read(source / p)) for p in v[name]["value"]} for name in v}
        fp = hashlib.sha256(json.dumps(sorted(hashes["CODE_FILES"].items()),
                                      separators=(",", ":")).encode("utf8")).hexdigest()
        tools = ("scripts/run_network_194_parallel.py", "scripts/lhs_release_build.py",
                 "scripts/supp20_input_receipt.py", *v["HANDOVER_FILES"]["value"])
        scopes[label] = dict(declarations=v, hashes=hashes, independently_rederived_code_fp=fp,
                             tool_hashes={p: sha_bytes(read(source / p)) for p in tools},
                             registration_hashes={p: sha_bytes(read(source / p)) for p in (
                                 "docs/reviews/lhs_network_batch_registration_20261007_g2.md",
                                 "docs/reviews/lhs_network_batch_registration_20261012_supp20.md")})
        constants[label] = dict(
            registered_fixture=assigned(source / "scripts/test_l214r_r01_restored_full.py", {"E_AREA", "E_BX", "E_BY"}),
            production=assigned(source / "scripts/network_conductivity.py",
                                {"FULL_Q_GUARD_MAX", "MODEL_LIMIT_POLICY", "_Q_REC_REL_TOL"}))
    diffs = {}
    for p in modified:
        if p.startswith(("scripts/", "webapp/")) or p in (
            "CLAUDE.md", "docs/reviews/findings.json", "docs/reviews/doc_refs_allowlist.tsv",
            "docs/reviews/selftest_inventory.tsv", "docs/session_20260923_progress.md",
            "docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md"):
            if (OLD / "source" / p).exists() and (ROOT / "source" / p).exists():
                diffs[p] = "".join(difflib.unified_diff(
                    read(OLD / "source" / p).decode("utf8").splitlines(True),
                    read(ROOT / "source" / p).decode("utf8").splitlines(True),
                    fromfile="685c2bbdb/" + p, tofile="34713ac96/" + p))
    save("diffs.json", diffs)
    sent = read(ROOT / "submitted/codex_lhs214cx_fix_recheck_request_20261019_send.md").decode("utf8").splitlines(True)
    repo = read(ROOT / "source/docs/reviews/codex_lhs214cx_fix_recheck_request_20261019.md").decode("utf8").splitlines(True)
    result = dict(
        integrity=integrity, entire_tree=dict(old_blobs=len(a), new_blobs=len(b),
        modified=modified, added=added, deleted=deleted,
        submitted_diff_matches=sorted(modified + added) == listed["changed"] and deleted == listed["deleted"]),
        scopes=scopes, constants=constants,
        sealed_32_bytes_same=scopes["old"]["hashes"]["CODE_FILES"] == scopes["new"]["hashes"]["CODE_FILES"],
        handover_bytes_same=scopes["old"]["hashes"]["HANDOVER_FILES"] == scopes["new"]["hashes"]["HANDOVER_FILES"],
        production_registration_bytes_same=scopes["old"]["registration_hashes"] == scopes["new"]["registration_hashes"],
        registered_fixture_values_same={k: v["value"] for k, v in constants["old"]["registered_fixture"].items()} ==
                                      {k: v["value"] for k, v in constants["new"]["registered_fixture"].items()},
        sent_request_delta=list(difflib.unified_diff(repo, sent, fromfile="repo", tofile="sent")))
    save("metadata.json", result)
    print(json.dumps(dict(integrity=integrity, modified=len(modified), added=len(added), deleted=len(deleted),
                          modified_paths=modified, sealed_same=result["sealed_32_bytes_same"],
                          handover_same=result["handover_bytes_same"], fixture_same=result["registered_fixture_values_same"],
                          code_fp=scopes["new"]["independently_rederived_code_fp"],
                          entire_diff_matches=result["entire_tree"]["submitted_diff_matches"]), ensure_ascii=False))


def receipt():
    import supp20_input_receipt as sr
    raw = sr.receipt()
    save("receipt_" + LABEL + "_raw.json", raw)
    sr.NP.git_info = lambda: dict(sha=None, branch=None, dirty=None, porcelain=[])
    adapted = sr.receipt(notes={"git_metadata_adapter": "Extracted source snapshot without .git; sha and dirty explicitly None. No clean tree or launch approval asserted."})
    save("receipt_" + LABEL + "_metadata_none.json", adapted)
    def compact(rec):
        return dict(rc=rec["rc"], scope=rec["scope"], bad=[c["id"] for c in rec["checks"] if not c["ok"]],
                    registration=rec["registration"], recorded=rec["recorded"], manual=rec["manual"])
    summary = dict(label=LABEL, raw=compact(raw), metadata_none=compact(adapted),
                   checks_unchanged=raw["checks"] == adapted["checks"])
    save("receipt_" + LABEL + "_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False))


def doc_metadata():
    remote = load(OUT / "doc_refs_remote.json")
    remote_integrity = {}
    for label, root in (("old", OLD), ("new", ROOT)):
        raw = remote[label]["content"].encode("utf8")
        tree = {e["path"]: e for e in load(root / "evidence/tree.json")["tree"]}
        expect = tree["docs/reviews/doc_refs_allowlist.tsv"]["sha"]
        remote_integrity[label] = dict(bytes=len(raw), sha256=sha_bytes(raw),
                                       blob=blob(raw), tree_blob=expect, verified=blob(raw) == expect == remote[label]["sha"])
    docrefs_diff = "".join(difflib.unified_diff(
        remote["old"]["content"].splitlines(True), remote["new"]["content"].splitlines(True),
        fromfile="685c2bbdb/docs/reviews/doc_refs_allowlist.tsv",
        tofile="34713ac96/docs/reviews/doc_refs_allowlist.tsv"))
    text_old = read(OLD / "source/CLAUDE.md").decode("utf8")
    text_new = read(ROOT / "source/CLAUDE.md").decode("utf8")
    lines_old, lines_new = text_old.splitlines(), text_new.splitlines()
    matcher = difflib.SequenceMatcher(None, lines_old, lines_new, autojunk=False)
    changed_claude_chunks = []
    for op, a0, a1, b0, b1 in matcher.get_opcodes():
        if op != "equal":
            pairs = list(zip(lines_old[a0:a1], lines_new[b0:b1])) if a1-a0 == b1-b0 else [
                ("\n".join(lines_old[a0:a1]), "\n".join(lines_new[b0:b1]))]
            for index, (before, after) in enumerate(pairs):
                prefix = 0
                while prefix < min(len(before), len(after)) and before[prefix] == after[prefix]:
                    prefix += 1
                suffix = 0
                while suffix < min(len(before), len(after)) - prefix and before[-1-suffix] == after[-1-suffix]:
                    suffix += 1
                ae, be = len(before)-suffix, len(after)-suffix
                changed_claude_chunks.append(dict(
                    op=op, old_line=a0 + index + 1, new_line=b0 + index + 1,
                    before=before[prefix:ae], after=after[prefix:be],
                    new_context=after[max(0, prefix-150):min(len(after), be+150)]))
    finding_ids = {"L214R-R03", "L214R-S01", "L214R-S02", "L214R-S03", "L214R-S04", "L214R-S05", "L214R-S06"}
    findings = {}
    for label, root in (("old", OLD), ("new", ROOT)):
        data = load(root / "source/docs/reviews/findings.json")
        rows = data if isinstance(data, list) else data["findings"]
        findings[label] = [{k: row.get(k) for k in (
            "id", "status", "claimed_fixed_sha", "verified_sha", "verified_in", "verified_scope")}
            for row in rows if row.get("id") in finding_ids]
    result = dict(doc_refs_integrity=remote_integrity, doc_refs_diff=docrefs_diff,
                  changed_claude_chunks=changed_claude_chunks, findings=findings)
    save("doc_metadata.json", result)
    print(json.dumps(result, ensure_ascii=False))


def manifest_audit():
    import supp20_input_receipt as sr
    entries = {e["path"]: e for e in load(ROOT / "evidence/tree.json")["tree"] if e["type"] == "blob"}
    rows = []
    downloaded = load(ROOT / "source_manifest.json")["files"]
    for file in downloaded:
        p = file["path"]
        if not p.endswith("manifest.json"):
            continue
        obj = load(ROOT / "source" / p)
        if not isinstance(obj, dict) or obj.get("schema") != sr.NP.SCHEMA:
            continue
        ch, hh = obj.get("code_hashes"), obj.get("handover_code_hashes")
        seal = obj.get("seal") or {}
        fp = (hashlib.sha256(json.dumps(sorted(ch.items()), separators=(",", ":")).encode("utf8")).hexdigest()
              if isinstance(ch, dict) and ch and all(ch.values()) else None)
        rows.append(dict(
            path=p, sha256=file["sha256"], context=("historical repository data" if p.startswith("docs/data/") else "archived review probe fixture"),
            git=obj.get("git"), launch_format=obj.get("launch_format"), code_files=len(ch or {}),
            code_keys_match_current=isinstance(ch, dict) and set(ch) == set(sr.NP.CODE_FILES),
            independently_rederived_code_fp=fp, declared_seal=seal,
            seal_fp_matches_hashes=bool(seal) and seal.get("code_fp") == fp,
            handover_code_hashes=hh,
            handover_keys_match_current=isinstance(hh, dict) and set(hh) == set(sr.NP.HANDOVER_FILES),
            launch_eligibility=sr.NP.launch_eligibility(obj)))
    prefix = "docs/reviews/codex_lhs214s_fix_recheck_evidence_20261019/lhs214s_recheck_20261019/"
    imported = []
    for path, entry in entries.items():
        if path.startswith(prefix):
            relative = path[len(prefix):]
            local = native(OLD / relative)
            data = local.read_bytes() if local.is_file() else None
            imported.append(dict(path=path, original=str(OLD / relative), original_exists=data is not None,
                                 tree_blob=entry["sha"], local_original_blob=blob(data) if data is not None else None,
                                 original_matches_tree=data is not None and blob(data) == entry["sha"]))
    report = ROOT / "source/docs/reviews/codex_review_lhs214s_fix_recheck_20261019.md"
    original_report = OLD / "codex_review_lhs214s_fix_recheck_20261019.md"
    result = dict(
        downloaded_launcher_manifests=rows,
        observation="Downloaded launcher manifests belong to historical data or archived probe fixtures. No fresh 34713ac production194/supp20 launch pair or approved-sha verification is supplied by this review.",
        imported_prior_files=imported, prior_report_same=read(report) == read(original_report),
        prior_report_sha256=sha_bytes(read(report)))
    save("manifest_audit.json", result)
    print(json.dumps(dict(manifests=[{k: v for k, v in row.items() if k in (
        "path", "context", "code_files", "code_keys_match_current", "handover_keys_match_current", "launch_eligibility")}
        for row in rows], imported_count=len(imported),
        imported_bad=[row for row in imported if not row["original_matches_tree"]],
        prior_report_same=result["prior_report_same"], prior_report_sha256=result["prior_report_sha256"]),
        ensure_ascii=False))


if __name__ == "__main__":
    {"metadata": metadata, "receipt": receipt, "doc_metadata": doc_metadata, "manifest_audit": manifest_audit}[MODE]()
