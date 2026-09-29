"""Round 9 document audit only: bytes, supplied diff, and reference policy examples.

No production imports, simulation, network, Git commands, or scheduler access.
The policy functions below are reviewer-authored interpretations, NOT tests of
a submitted launcher or detector. They do not certify implementation.
"""
from pathlib import Path
import hashlib
import json
import math
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
checks = []
def sha(data):
    return hashlib.sha256(data).hexdigest()
def check(label, result):
    if not result:
        raise AssertionError(label)
    checks.append(label)

raw = (ROOT / "bundle_original.md").read_bytes()
lf = raw.replace(b"\r\n", b"\n")
text = lf.decode("utf-8-sig")
(ROOT / "bundle_lf.md").write_bytes(text.encode("utf-8"))
expected_req = "504c97f5bc5c6e6c64e0fd1e2fe2f1edc0477e4de94705920af49caf504573b8"
expected_pre = "e7311197509268b9302708847ac00d19daa68fa4fb09232e74908524cada080c"
def extract(start_marker, end_marker, expected, dest):
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    between = text[start:end].encode("utf-8")
    variants = {
        "raw_between_markers": between,
        "separator_blanks_excluded_one_final_LF": between.rstrip(b"\n") + b"\n",
    }
    hashes = {k: sha(v) for k,v in variants.items()}
    names = [k for k,v in variants.items() if sha(v) == expected]
    check(dest + " exact declared SHA256", bool(names))
    selected = variants[names[0]]
    (ROOT / dest).write_bytes(selected)
    return selected, {
        "sha256": sha(selected), "bytes": len(selected),
        "lines": len(selected.splitlines()),
        "starts_at_bundle_line": text[:start].count("\n") + 1,
        "selection": names[0], "candidate_hashes": hashes,
    }

req, req_pin = extract("# Codex 9 차 요청서", "# PART 2", expected_req,
                       "request_extracted.md")
pre, pre_pin = extract("# 믹서 고-Bo 확장 `LH` — D-1", "# PART 3", expected_pre,
                       "prereg_v23_extracted.md")
check("v2.3 has 294 physical lines", pre_pin["lines"] == 294)
check("prereg line 1 is bundle line 68", pre_pin["starts_at_bundle_line"] == 68)
old = (ROOT / "baseline/prereg_v22.md").read_bytes()
check("prior v2.2 pin", sha(old) ==
      "ab20ef775f3e6bdb660f82f36a15b18a3c7cb0d0f85a6881d840b1b2171dff44")

diff_start = text.index("```diff\n") + len("```diff\n")
diff_end = text.index("\n```", diff_start)
patch = text[diff_start:diff_end] + "\n"
(ROOT / "submitted_v22_to_v23.diff").write_text(patch, encoding="utf-8")
old_lines = old.decode("utf-8").splitlines(keepends=True)
patch_lines = patch.splitlines(keepends=True)
cursor = 0
rebuilt = []
hunks = []
i = 0
while i < len(patch_lines):
    m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", patch_lines[i])
    if not m:
        i += 1
        continue
    a, na, b, nb = [int(x) if x is not None else 1 for x in m.groups()]
    old_chunk, new_chunk = [], []
    i += 1
    while i < len(patch_lines) and not patch_lines[i].startswith("@@"):
        line = patch_lines[i]
        if line.startswith(" "):
            old_chunk.append(line[1:]); new_chunk.append(line[1:])
        elif line.startswith("-"):
            old_chunk.append(line[1:])
        elif line.startswith("+"):
            new_chunk.append(line[1:])
        else:
            raise AssertionError("Unsupported patch line: " + repr(line))
        i += 1
    if len(old_chunk) != na or len(new_chunk) != nb:
        raise AssertionError("Hunk count mismatch")
    if old_lines[a-1:a-1+na] != old_chunk:
        raise AssertionError("Hunk context mismatch")
    rebuilt.extend(old_lines[cursor:a-1])
    if len(rebuilt) != b-1:
        raise AssertionError("New hunk position mismatch")
    rebuilt.extend(new_chunk)
    cursor = a-1+na
    hunks.append({"old_line": a, "old_count": na, "new_line": b, "new_count": nb})
rebuilt.extend(old_lines[cursor:])
applied = "".join(rebuilt).encode("utf-8")
check("supplied diff applies to independently preserved v2.2", bool(hunks))
check("applying supplied diff reproduces v2.3 byte for byte", applied == pre)

# Unchanged operative sections/parameters; document matching is not runtime proof.
p23 = pre.decode("utf-8")
p22 = old.decode("utf-8")
def section(s, a, b):
    return s[s.index(a):s.index(b)]
unchanged = {}
for label, a, b in [
    ("estimands", "## 1.", "## 2."),
    ("pairwise_stiffness", "## 3.", "## 4."),
    ("error_budget_and_decision", "## 5.", "## 6."),
    ("contact_contract", "## 6.", "## 7."),
    ("seeds_and_holdout", "## 7.", "## 8."),
    ("terminal_policy", "### 8-4.", "## 9."),
]:
    same = section(p23, a, b) == section(p22, a, b)
    unchanged[label] = same
    check("unchanged operative section: " + label, same)

# These are specified plan cells, not submitted/executed jobs.
dev = [("E0_ref", s, "ref") for s in (32452843,49979687,67867967)]
dev += [("LC_ref",32452843,"ref"),("LH_ref",32452843,"ref"),
        ("E0_ref2",32452843,"ref2"),("E0_ref_dt_half",32452843,"ref")]
check("listed seven development cells contain no soft role",
      len(dev)==7 and all(level != "soft" for _,_,level in dev))

# Reviewer reference interpretation of the post-diagnostic state table.
# Even known one-component exceedance with missing other component is incomplete;
# record the exceedance rather than silently claiming combined PASS.
def post_state(r=None, t=None, planned=True):
    if not planned:
        return {"state":"NOT_RUN","keep_primary":True,"combined_pass":False,
                "change_completed_level":False,"known_exceedance":[]}
    vals = {"r":r, "t":t}
    finite = {k:isinstance(v,(int,float)) and math.isfinite(v) for k,v in vals.items()}
    exceed = [k for k,v in vals.items() if finite[k] and abs(v) > .05 + 1e-12]
    if not all(finite.values()):
        state = "INCOMPLETE"
    elif exceed:
        state = "EXCEEDS"
    else:
        state = "WITHIN"
    return {"state":state,"keep_primary":True,"combined_pass":state=="WITHIN",
            "change_completed_level":False,"known_exceedance":exceed}
cases = {
    "requested_counterexample":post_state(.06,.01),
    "within":post_state(.049,.049),
    "negative_exceedance":post_state(-.06,.01),
    "r_only":post_state(.049,None),
    "known_exceedance_but_incomplete":post_state(.06,None),
    "nonfinite":post_state(float("nan"),.01),
    "not_run":post_state(planned=False),
    "equality":post_state(.05,.05),
    "inside_numerical_slack":post_state(.05+5e-13,.01),
    "outside_numerical_slack":post_state(.05+2e-12,.01),
}
check("r=.06 t=.01 retains old primary; no retroactive reselection",
      cases["requested_counterexample"]["state"]=="EXCEEDS"
      and cases["requested_counterexample"]["keep_primary"]
      and not cases["requested_counterexample"]["change_completed_level"])
check("partial or nonfinite never combined PASS",
      all(not cases[k]["combined_pass"] for k in
          ("r_only","known_exceedance_but_incomplete","nonfinite","not_run")))
check("numerical threshold examples implement <= .05 + 1e-12",
      cases["equality"]["combined_pass"] and
      cases["inside_numerical_slack"]["combined_pass"] and
      not cases["outside_numerical_slack"]["combined_pass"])

# A QC-only, M-blind result can still determine which threshold is selected.
# Numbers are synthetic, not a recommendation for a soft bound.
soft_example = {
    "observed_holdout_overlap_pct":6.2,
    "threshold_chosen_before_pct":6.0,
    "threshold_chosen_after_pct":6.3,
    "M_was_read":False,
    "before":"OUT_OF_RANGE",
    "after":"ADMITTED",
}
check("M-blind alone cannot prevent result-dependent range selection",
      soft_example["threshold_chosen_before_pct"] <
      soft_example["observed_holdout_overlap_pct"] <=
      soft_example["threshold_chosen_after_pct"])

# Same observed 5.5%: original 1% eligibility and proposed diagnostic range differ.
# 6% is hypothetical and not being registered here.
same_point = {
    "observed_overlap_pct":5.5, "original_limit_pct":1.0,
    "illustrative_diagnostic_limit_pct":6.0,
    "original_contract":"NOT_MET", "diagnostic_range":"WITHIN",
}
check("diagnostic admissibility does not retroactively change original contract",
      1.0 < 5.5 <= 6.0)

# Temporal consequence of dropping only runs already scheduled after confirmation.
cost = {"confirmation_long_runs_lower_h":(6*41+6*92)/3,
        "deadline_window_h":240,
        "optional_post_runs_removed":6,
        "confirmation_lower_h_after_removal":(6*41+6*92)/3}
check("dropping optional post runs does not shorten confirmation critical work",
      cost["confirmation_long_runs_lower_h"] ==
      cost["confirmation_lower_h_after_removal"] > cost["deadline_window_h"])

# Surface leftovers are captured for human semantic review, not used as automatic verdicts.
patterns = ["나쁜 reference 로 확인 18 런을 태우는 것을 막는다",
            "큰 오차 탈락 검사", "reference 자격화",
            "예: 저장 프레임 최대 ≤ 6 %"]
residual_lines = {}
for pattern in patterns:
    residual_lines[pattern] = [
        {"P":i,"B":i+67,"text":line}
        for i,line in enumerate(p23.splitlines(),1) if pattern in line]
out = {
    "scope":"document bytes/diff and reviewer reference models; no submitted production-code test",
    "pin":{"bundle_sha256":sha(raw),"bundle_bytes":len(raw),
           "request":req_pin,"prereg":pre_pin,
           "claimed_content_commit":"88a58ec02",
           "remote_commit_independently_verified":False},
    "diff":{"hunks":hunks,"reconstructed_sha256":sha(applied),"matches":applied==pre},
    "unchanged_sections":unchanged,"development_plan_cells":dev,
    "reference_post_states":cases,
    "soft_bound_selection_counterexample":soft_example,
    "separate_contract_axes":same_point,
    "cost_temporal_counterexample":cost,
    "residual_lines_for_human_review":residual_lines,
    "assertions":{"passed":len(checks),"failed":0,"labels":checks},
}
(ROOT / "audit_results.json").write_text(
    json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False))

