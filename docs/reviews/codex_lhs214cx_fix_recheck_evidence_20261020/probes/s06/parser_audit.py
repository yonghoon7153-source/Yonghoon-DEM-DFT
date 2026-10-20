"""Independent S06 review. Snapshot reads only; generated files stay in evidence/s06."""
from pathlib import Path
import contextlib
import hashlib
import importlib.util
import itertools
import json
import os
import random
import re
import sys
import tempfile
import time
from unittest.mock import patch

R = Path(__file__).resolve().parents[2]
W = R.parent
S = R / "source"
B = W / "lhs214s_recheck_20261019/source"
O = R / "evidence/s06"
DEPS = [W / "lhs_coverage_review_20260930/deps",
        W / "gen2_network_reverify3_20261007/deps",
        W / "lhs214rr_recheck_20261019/deps"]
sys.path[:0] = [str(S / "scripts"), *map(str, DEPS)]
sys.dont_write_bytecode = True
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[key] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONPATH"] = os.pathsep.join(map(str, DEPS))
O.mkdir(parents=True, exist_ok=True)
(O / "tmp").mkdir(exist_ok=True)
tempfile.tempdir = str(O / "tmp")
os.environ["TEMP"] = os.environ["TMP"] = str(O / "tmp")
import supp20_input_receipt as sr
from markdown_it import MarkdownIt
import markdown_it

spec = importlib.util.spec_from_file_location("s06_baseline_receipt", B / "scripts/supp20_input_receipt.py")
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
MD = MarkdownIt("commonmark")
PIN = "34713ac9650ece7c8d59b7c4d9a2aefccee693ea"
ADAPTER = []


def metadata_only(*args, **kwargs):
    ADAPTER.append("git_info: no repository, declared review pin only; no clean-tree certification")
    return dict(sha=PIN, short=PIN[:9], branch="review-snapshot", dirty=None, porcelain=[])


sr.NP.git_info = metadata_only
FP = sr.NP.code_fp(sr.NP.code_hashes())
VAL = "`code_fp " + FP + "`"
OTHER = "`code_fp " + "0" * 64 + "`"


def save(name, value):
    (O / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def oracle(doc):
    """Independent block tokens; inputs have no unsupported block constructs."""
    toks = MD.parse(doc)
    heads = [(t.map[0], int(t.tag[1:]), toks[i + 1].content)
             for i, t in enumerate(toks) if t.type == "heading_open" and t.level == 0]
    active = [h for h in heads if h[1] == 2 and re.match(r"3\.(\s|$)", h[2])]
    if len(active) != 1:
        return dict(active=False, code_fp=None, body=None, heads=heads)
    start = active[0][0]
    end = next((h[0] for h in heads if h[0] > start and h[1] <= 2), len(doc.split("\n")))
    excluded = set()
    for t in toks:
        if t.type in ("fence", "code_block"):
            excluded.update(range(*t.map))
    body = "\n".join(line for n, line in enumerate(doc.split("\n"))
                     if start <= n < end and n not in excluded)
    values = set(re.findall(r"`code_fp ([0-9a-f]{64})`", body))
    return dict(active=True, code_fp=next(iter(values)) if len(values) == 1 else None,
                body=body, heads=heads)


def actual(mod, doc):
    body, reason = mod._md_section(doc, 3, strip_code=True)
    values = set(re.findall(r"`code_fp ([0-9a-f]{64})`", body or ""))
    return dict(active=body is not None, code_fp=next(iter(values)) if len(values) == 1 else None,
                body=body, reason=reason)


def summary(rec):
    return dict(rc=rec["rc"], bad=[x["id"] for x in rec["checks"] if not x["ok"]],
                code_fp=rec["registration"]["values"]["code_fp"])


def verdict(a, b):
    return all(a[k] == b[k] for k in ("active", "code_fp"))


def replay():
    rows = []
    previous = W / "lhs214s_recheck_20261019"
    rr = W / "lhs214rr_recheck_20261019"
    headings = json.loads((previous / "evidence/s01_heading_boundary_cases.json").read_text(encoding="utf-8"))
    fences = json.loads((rr / "evidence/receipt_fence_matrix.json").read_text(encoding="utf-8"))
    cases = [("heading", c["name"], previous / c["input"], c["extra"]) for c in headings["rows"]]
    cases += [("fence", c["name"], rr / "evidence/receipt_fence_cases" / (c["name"] + ".md"), c["extra"])
              for c in fences["cases"]]
    started = time.monotonic()
    for group, name, path, extra in cases:
        doc = path.read_text(encoding="utf-8")
        expected = oracle(extra)
        before, after = actual(old, doc), actual(sr, doc)
        rec_old, rec_new = old.receipt(reg_doc=str(path)), sr.receipt(reg_doc=str(path))
        row = dict(group=group, name=name, path=str(path), sha256=digest(path),
                   expected=expected, old=before, new=after,
                   old_receipt=summary(rec_old), new_receipt=summary(rec_new),
                   old_match=verdict(before, expected), new_match=verdict(after, expected),
                   new_receipt_match=rec_new["registration"]["values"]["code_fp"] == expected["code_fp"])
        rows.append(row)
        if group == "heading":
            save("replay_receipt_" + name + ".json", rec_new)
    totals = {}
    for group in ("heading", "fence"):
        rr_ = [r for r in rows if r["group"] == group]
        totals[group] = dict(total=len(rr_), old_mismatch=sum(not r["old_match"] for r in rr_),
                            new_mismatch=sum(not r["new_match"] for r in rr_),
                            new_receipt_mismatch=sum(not r["new_receipt_match"] for r in rr_),
                            old_rc0=sum(r["old_receipt"]["rc"] == 0 for r in rr_),
                            new_rc0=sum(r["new_receipt"]["rc"] == 0 for r in rr_))
    save("prior_133_replay.json", dict(totals=totals, seconds=time.monotonic() - started, rows=rows))
    print(json.dumps(totals), flush=True)


def new_boundaries():
    """Empty headings crossed with outside/in-fence and candidate/history placement."""
    tails = ["", " ", "\t", " \t", " \u00a0", " \u2003", " \x0b", " \x0c",
             " #", "\t####\t", " \\#", "\u00a0", "not-a-heading"]
    closers = ["```", "````", "`````", "~~~", " ```", "   ````", "\t````", "```` ",
               "````\t", "````\u00a0", "````\u2003", "```` x", "```` `", ""]
    records = []
    for level, tail, close, history in itertools.product(range(1, 9), tails, closers, (False, True)):
        boundary = "#" * level + tail
        prefix = "## 3. Active\n" + (VAL + "\n" if history else "")
        value = OTHER if history else VAL
        for pattern, middle in [
            ("outside", boundary + "\n"),
            ("fenced", "````markdown\n" + boundary + "\n" + close + "\n"),
            ("after_closer", "````markdown\n" + close + "\n" + boundary + "\n"),
        ]:
            doc = prefix + middle + value + "\n"
            expected, before, after = oracle(doc), actual(old, doc), actual(sr, doc)
            records.append(dict(name=f"{pattern}_{level}_{tails.index(tail)}_{closers.index(close)}_{int(history)}",
                                text=doc, expected=expected, before=before, after=after,
                                new_match=verdict(after, expected), old_match=verdict(before, expected)))
    mismatch = [r for r in records if not r["new_match"]]
    result = dict(total=len(records), old_mismatch=sum(not r["old_match"] for r in records),
                  new_mismatch=len(mismatch), mismatches=mismatch,
                  scope="column-zero ATX, fences with 0-3 space opening indentation; malformed closers are content")
    save("new_boundary_matrix.json", result)
    # Full receipt path for every found mismatch and representative passing cases.
    chosen = mismatch[:50]
    chosen += [next(r for r in records if r["name"] == name) for name in [
        "outside_1_0_0_0", "outside_2_0_0_1", "fenced_2_0_0_0",
        "fenced_2_0_1_0", "after_closer_2_0_1_1", "after_closer_3_0_1_0",
        "outside_2_8_0_0", "outside_2_9_0_1", "outside_7_0_0_0",
        "outside_2_11_0_0", "fenced_2_0_6_0", "fenced_2_0_9_0"]]
    registered = (S / sr.REG_DOC).read_text(encoding="utf-8")
    base = re.sub(r"^## 3\.", "## 30.", re.sub(r"`code_fp_pending [0-9a-f]{64}`",
                  "(pending removed for diagnostic)", registered), flags=re.M)
    directory = O / "new_cases"
    directory.mkdir(exist_ok=True)
    receipt_rows = []
    for case in chosen:
        p = directory / (case["name"] + ".md")
        p.write_text(base + "\n" + case["text"], encoding="utf-8")
        rec = sr.receipt(reg_doc=str(p))
        receipt_rows.append(dict(name=case["name"], expected=case["expected"], actual=summary(rec),
                                 match=rec["registration"]["values"]["code_fp"] == case["expected"]["code_fp"]))
        save("new_receipt_" + case["name"] + ".json", rec)
    save("new_boundary_receipts.json", dict(total=len(receipt_rows),
         mismatches=sum(not r["match"] for r in receipt_rows), rows=receipt_rows))
    print(json.dumps({k: v for k, v in result.items() if k != "mismatches"}), flush=True)


def randomized():
    """Independent deterministic transitions, including duplicate candidate headings."""
    rng = random.Random(20261020)
    lines = ["", "plain text", "#", "##", "###", "######", "#######",
             "# ", "##\t", "# \u00a0", "## \u2003", "## ###", "# \\###",
             "## 3. Active", "## 3.\t#", "## 3.##", "## 4. Next",
             VAL, OTHER, "```", "~~~~", "``````", "```text", "~~~info`",
             "```x`", " ````", "   ~~~", "\t~~~", "``` \u00a0", "~~~~ x",
             "\\## 3. Escaped", "##not-heading"]
    count, before_bad, mismatches = 0, 0, []
    for _ in range(30000):
        # Blank preceding a 4-column fence-like line would create unsupported
        # indented code. Such lines are used only as active-fence malformed closers
        # in new_boundaries(), so remove them here.
        pool = [ln for ln in lines if not ln.startswith("\t")]
        doc = "\n".join(["## 3. Active", *rng.choices(pool, k=rng.randrange(1, 17)), VAL]) + "\n"
        expected, before, after = oracle(doc), actual(old, doc), actual(sr, doc)
        count += 1
        before_bad += not verdict(before, expected)
        if not verdict(after, expected):
            mismatches.append(dict(text=doc, expected=expected, new=after))
    save("random_transitions.json", dict(total=count, seed=20261020, old_mismatch=before_bad,
                                       new_mismatch=len(mismatches), mismatches=mismatches[:100]))
    print(json.dumps(dict(random_docs=count, new_mismatches=len(mismatches))), flush=True)


def noimpact():
    before = old.receipt(reg_doc=str(S / sr.REG_DOC), readme=str(S / sr.RUNS_README),
                         r3_tgz=str(S / sr.R3_TGZ), r2_tgz=str(S / sr.R2_TGZ))
    after = sr.receipt()
    save("actual_receipt_old.json", before)
    save("actual_receipt_new.json", after)
    result = dict(old=summary(before), new=summary(after),
                  values_equal=before["registration"]["values"] == after["registration"]["values"],
                  checks_equal=before["checks"] == after["checks"],
                  old_section=old._md_section((S / sr.REG_DOC).read_text(encoding="utf-8"), 3, True),
                  new_section=sr._md_section((S / sr.REG_DOC).read_text(encoding="utf-8"), 3, True))
    save("actual_noimpact.json", result)
    print(json.dumps({k: v for k, v in result.items() if "section" not in k}), flush=True)


def selftest():
    original = sr.NP.subprocess.run
    def run(argv, *args, **kwargs):
        if isinstance(argv, (list, tuple)) and argv and str(argv[0]).lower() == "git":
            raise AssertionError("Git commands prohibited")
        if isinstance(argv, list) and len(argv) > 4 and argv[1:4] == ["-I", "-B", "-c"] and argv[4] == sr.NP.GEN_PROBE:
            argv = list(argv)
            argv[4] = "import sys; sys.path[:0] = " + repr(list(map(str, DEPS))) + "\n" + argv[4]
            ADAPTER.append("isolated GEN_PROBE: dependency path only")
        return original(argv, *args, **kwargs)
    started = time.monotonic()
    with patch.object(sr.NP.subprocess, "run", run), (O / "selftest.log").open("w", encoding="utf-8") as log:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            rc = sr._selftest()
    save("selftest_result.json", dict(rc=rc, seconds=time.monotonic() - started, adapters=ADAPTER))
    print(json.dumps(dict(selftest_rc=rc)), flush=True)


def metadata():
    save("metadata.json", dict(pin=PIN, python=sys.version, markdown_it_version=markdown_it.__version__,
         source_sha256=digest(S / "scripts/supp20_input_receipt.py"),
         baseline_sha256=digest(B / "scripts/supp20_input_receipt.py"),
         fp=FP, dependency_paths=list(map(str, DEPS)), metadata_adapter_calls=len(ADAPTER),
         source_files_modified=False, git_commands_executed=False,
         caveat="Snapshot metadata adapter is not real clean-tree or author-approval evidence."))


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "all"
    funcs = [replay, new_boundaries, randomized, noimpact] if action == "all" else [globals()[action]]
    for fn in funcs:
        fn()
    metadata()
