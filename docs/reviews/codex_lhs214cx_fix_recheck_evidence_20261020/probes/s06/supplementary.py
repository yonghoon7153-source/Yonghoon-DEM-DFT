"""Read-only follow-ups: actual newline ingestion and documented out-of-scope blocks."""
from pathlib import Path
import json
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parser_audit as a

directory = a.O / "newline_cases"
directory.mkdir(exist_ok=True)
base_text = (a.S / a.sr.REG_DOC).read_text(encoding="utf-8")
base = re.sub(r"^## 3\.", "## 30.", re.sub(r"`code_fp_pending [0-9a-f]{64}`",
              "(pending removed for diagnostic)", base_text), flags=re.M)
cases = {
    "empty_h1": "## 3. Active\n#\n" + a.VAL + "\n",
    "empty_h2": "## 3. Active\n##\n" + a.VAL + "\n",
    "history": "## 3. Active\n" + a.VAL + "\n##\n" + a.OTHER + "\n",
    "fenced_empty": "## 3. Active\n````\n##\n````\n" + a.VAL + "\n",
    "fenced_value": "## 3. Active\n~~~\n" + a.VAL + "\n~~~\n",
    "mixed": "## 3. Active\n" + a.VAL + "\n```\n##\n" + a.OTHER + "\n```\n",
}
rows = []
for name, text in cases.items():
    expected = a.oracle(text)
    for newline, ending in [("lf", "\n"), ("crlf", "\r\n"), ("cr", "\r")]:
        p = directory / (name + "_" + newline + ".md")
        p.write_bytes((base + "\n" + text).replace("\n", ending).encode("utf-8"))
        rec = a.sr.receipt(reg_doc=str(p))
        got = a.summary(rec)
        want_bad = [] if expected["code_fp"] == a.FP else ["R0", "D1"]
        rows.append(dict(name=name, newline=newline, receipt=got, expected=expected,
                         match=(got["code_fp"] == expected["code_fp"]
                                and got["bad"] == want_bad and got["rc"] == bool(want_bad))))
a.save("newline_receipts.json", dict(total=len(rows), mismatches=sum(not r["match"] for r in rows),
                                   rows=rows))

# These are deliberately outside the agreed grammar; a divergence documents the
# limit and is not promoted to a new supported-scope defect.
unsupported = {
    "indented_heading": "## 3. Active\n ## Outside\n" + a.VAL + "\n",
    "setext_heading": "## 3. Active\nOutside\n---\n" + a.VAL + "\n",
    "html_empty_heading": "## 3. Active\n" + a.VAL + "\n<div>\n##\n</div>\n\n" + a.OTHER + "\n",
    "html_named_heading": "## 3. Active\n" + a.VAL + "\n<div>\n## Example\n</div>\n\n" + a.OTHER + "\n",
    "indented_code_value": "## 3. Active\n\n    " + a.VAL + "\n",
    "quoted_value": "## 3. Active\n> " + a.VAL + "\n",
}
limits = []
for name, text in unsupported.items():
    expected, before, after = a.oracle(text), a.actual(a.old, text), a.actual(a.sr, text)
    limits.append(dict(name=name, text=text, markdown_it=expected, old=before, new=after,
                       in_supported_scope=False))
a.save("unsupported_scope_controls.json", dict(cases=limits,
    interpretation="No requirement to support these constructs; retained explicit grammar limitation."))
manifest = json.loads((a.R / "source_manifest.json").read_text(encoding="utf-8"))
entry = next(x for x in manifest["files"] if x["path"] == "scripts/supp20_input_receipt.py")
got_hash = a.digest(a.S / entry["path"])
a.save("receipt_source_integrity.json", dict(path=entry["path"], expected_sha256=entry["sha256"],
                                           actual_sha256=got_hash, match=entry["sha256"] == got_hash))
print(json.dumps(dict(newline_cases=len(rows), newline_mismatch=sum(not r["match"] for r in rows),
                      unsupported_scope_cases=len(limits), receipt_source_unchanged=entry["sha256"] == got_hash)))
