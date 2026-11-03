"""Pure evidence reconstruction + event model for final request timing.

No shell, scheduler, DEM or cancellation command is run. The model is not a
claim that an unapproved main actually ran; it proves the documented ordering
permits it. Source line anchors are checked against the final pinned file.
"""
from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
PACKAGE = BASE.parent / "received_zip"
script = (PACKAGE / "repo/scripts/resume_ckpt.sh").read_text(encoding="utf-8")
source_lines = script.splitlines()
request = (PACKAGE / "REQUEST.md").read_text(encoding="utf-8")
assert "# ② ~/d07_cmp_main.log 에 '✅ 본 제출 job' 줄이 나온 뒤" in request
evidence = (PACKAGE / "repo/docs/50kg/d07_guard/t_test_20261103/t_output_grep.txt").read_text(encoding="utf-8")
receipt_lines = [s for s in evidence.splitlines() if re.fullmatch(r"[0-9a-f]{64}  /lustre/home/yonghoon/dem_test/kg50_d07_b50/.+", s)]
assert len(receipt_lines) == 5
receipt = "\n".join(receipt_lines) + "\n"
receipt_sha = hashlib.sha256(receipt.encode()).hexdigest()
expected = "cff47c44385a95529ed2c6e97438985a56e6e2ede194e05f7541c14788570176"
assert receipt_sha == expected
(BASE / "final_receipt.reconstructed.sha256").write_text(receipt, encoding="utf-8", newline="\n")

anchors = {
    1933: 'echo "도구 신원',
    2324: 'if ! sha256sum',
    2327: 'MIS=$(sha256sum',
    2340: 'J=$(sbatch --parsable',
    2454: '[ -z "$BLK" ] && [ "$(sha256sum',
    2456: '[ -z "$BLK" ] && ! CKO=$(sha256sum',
    2461: 'JM=$(sbatch --parsable',
    2463: 'echo "- ✅ 본 제출 job',
    2478: 'cat $REP;',
}
for line, fragment in anchors.items():
    assert fragment in source_lines[line - 1], (line, fragment)

def model(changed_since_approved_trial):
    old_receipt = expected
    new_receipt = "b" * 64 if changed_since_approved_trial else old_receipt
    events = [
        {"source_line": 1933, "event": "new attempt identifier available on stdout"},
        {"source_line": 2324, "event": "write current five-line receipt", "hash": new_receipt},
        {"source_line": 2327, "event": "save same-call MIS", "hash": new_receipt},
        {"source_line": 2340, "event": "submit new trial"},
        {"source_line": 2441, "event": "assume current trial G0-G3 pass"},
        {"source_line": 2454, "event": "receipt hash == same-call MIS", "pass": True},
        {"source_line": 2456, "event": "current five inputs == current receipt", "pass": True},
        {"source_line": 2461, "event": "submit main"},
        {"source_line": None, "event": "main may start (scheduler ordering not constrained by protocol)"},
        {"source_line": 2463, "event": "append main-success line to report file"},
        {"source_line": 2478, "event": "copy report to redirected main.log; requested trigger now visible"},
        {"request_line": 82, "event": "first manual approved-receipt comparison", "match": new_receipt == old_receipt},
    ]
    assert next(i for i, x in enumerate(events) if x["event"] == "submit main") < len(events) - 1
    return {"changed_since_approved_trial": changed_since_approved_trial, "new_receipt_matches_approved": new_receipt == old_receipt, "main_submitted_before_first_documented_manual_check": True, "events": events}

result = {
    "pin": (PACKAGE / "PIN.txt").read_text(encoding="utf-8").splitlines()[0],
    "kind": "pure schedule model; no real commands executed",
    "source_sha256": hashlib.sha256((PACKAGE / "repo/scripts/resume_ckpt.sh").read_bytes()).hexdigest(),
    "receipt_reconstruction_sha256": receipt_sha,
    "receipt_rows": len(receipt_lines),
    "tool_code_contains_previous_approved_receipt_literal": expected in script,
    "cases": [model(False), model(True)],
    "assertions": "PASS",
}
out = json.dumps(result, ensure_ascii=False, indent=2)
(BASE / "probe_final_schedule.json").write_text(out + "\n", encoding="utf-8")
print(out)
