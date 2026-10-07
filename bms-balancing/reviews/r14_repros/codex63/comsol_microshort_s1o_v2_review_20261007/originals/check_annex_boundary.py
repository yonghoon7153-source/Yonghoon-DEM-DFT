"""Resolve the code-fence boundary without editing the first comparison record."""
from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent
v2=Path("C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_SEND_TO_CODEX_v2_20261007.md").read_bytes()
annex=(ROOT.parent/"microshort_s1o_prereview_20261007"/"S1O_CLARIFICATION_ADDENDUM_KO.md").read_bytes()
start=v2.index(b"````markdown\n")+len(b"````markdown\n")
closing_newline=v2.index(b"\n````",start)
included=v2[start:closing_newline+1]
original_check=json.loads((ROOT/"STATIC_COMPARISON.json").read_text(encoding="utf-8"))
other_checks={k:v for k,v in original_check["checks"].items() if k!="embedded_annex_exact_original_bytes"}
result={
    "kind":"REVIEWER_FENCE_BOUNDARY_CORRECTION",
    "first_result_preserved":"STATIC_COMPARISON.json",
    "cause":"Initial extraction omitted the LF immediately before the closing fence. That LF belongs to the quoted source's final newline.",
    "original_annex_bytes":len(annex),
    "included_span_bytes":len(included),
    "full_original_annex_present_byte_for_byte":included==annex,
    "original_sha256":hashlib.sha256(annex).hexdigest(),
    "included_span_sha256":hashlib.sha256(included).hexdigest(),
    "prior_other_checks_all_true":all(other_checks.values()),
    "source_files_modified":False,
    "candidate_tests_or_execution":0,
}
with (ROOT/"ANNEX_BOUNDARY_CHECK.json").open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps(result,ensure_ascii=False))
assert included==annex and all(other_checks.values())

