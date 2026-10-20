"""Our S06 check without markdown-it-py (the Codex oracle dependency is missing here).

usage: python3 -I -X utf8 -B s06_nooracle.py <repo_root> <baseline_receipt_py> <bundle_root> <out_dir>

What it does (all reads; writes only into <out_dir>):
  A  133 prior docs (19 heading + 114 fence, inputs already in the repo) -> our new tool,
     the 685c2bbdb tool, and full receipt() for both; compared with Codex's recorded
     rows in evidence/s06/prior_133_replay.json (its oracle 'expected' is reused as data).
  B  the 8,736-document matrix (generation copied verbatim from probes/s06/parser_audit.py
     new_boundaries) -> count documents where the old and new tools decide differently.
     If the new tool equals the oracle everywhere (Codex: 0 mismatches) this count must
     equal Codex's old-tool mismatch count (608).  Necessary condition only.
     + the 12 representative full receipts, docs regenerated from our registration file
     and compared (CRLF-normalised) with the bundle's new_cases/*.md.
  C  the 30,000 random documents (seed 20261020, generation copied verbatim from
     randomized) -> same old/new difference count (Codex old mismatches 2,212).
  D  18 newline receipts (supplementary.py cases) -> compared with Codex rows; doc bytes
     compared with the bundle's newline_cases/*.md.
  E  6 documented out-of-scope controls -> our old/new decisions vs Codex's recorded ones.
  F  the actual registration document: old/new _md_section vs Codex actual_noimpact.json.
The metadata adapter (git_info -> declared pin) is the same in-memory one Codex used, so
no git subprocess runs; it does not change check results (see our CLI receipt).
Second in-memory adapter: the baseline (685c2bbdb) tool file sits alone in a scratch
folder, so its module global REPO is pointed at our tree (it resolves the registration,
README, tarballs, design / adapter / cohort / union / harvest paths through _rp()).
"""
import hashlib
import importlib.util
import itertools
import json
import random
import re
import sys
import time
from pathlib import Path

REPO = Path(sys.argv[1])
BASE_RECEIPT = Path(sys.argv[2])
BUNDLE = Path(sys.argv[3])
OUT = Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)
sys.path[:0] = [str(REPO / 'scripts'), str(REPO / 'webapp')]
sys.dont_write_bytecode = True
import supp20_input_receipt as sr  # noqa: E402

spec = importlib.util.spec_from_file_location('s06_baseline_receipt', BASE_RECEIPT)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
OLD_REPO_WAS = str(old.REPO)
old.REPO = REPO  # adapter: relative data paths of the baseline tool -> our tree (see old_receipt)
PIN = '34713ac9650ece7c8d59b7c4d9a2aefccee693ea'
ADAPTER = []


def metadata_only(*args, **kwargs):
    ADAPTER.append(1)
    return dict(sha=PIN, short=PIN[:9], branch='review-snapshot', dirty=None, porcelain=[])


sr.NP.git_info = metadata_only
FP = sr.NP.code_fp(sr.NP.code_hashes())
VAL = '`code_fp ' + FP + '`'
OTHER = '`code_fp ' + '0' * 64 + '`'
CX = BUNDLE / 'evidence/s06'


def cxload(name):
    return json.loads((CX / name).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def old_receipt(path):
    # Same call as Codex's replay (reg_doc only).  The baseline file sits alone in a
    # scratch folder, so its module global REPO (read by _rp() at call time) is pointed
    # at our tree below - in Codex's run it was the complete 685c2bbdb snapshot.
    return old.receipt(reg_doc=str(path))


def actual(mod, doc):  # verbatim from parser_audit.actual
    body, reason = mod._md_section(doc, 3, strip_code=True)
    values = set(re.findall(r'`code_fp ([0-9a-f]{64})`', body or ''))
    return dict(active=body is not None, code_fp=next(iter(values)) if len(values) == 1 else None,
                body=body, reason=reason)


def summary(rec):  # verbatim from parser_audit.summary
    return dict(rc=rec['rc'], bad=[x['id'] for x in rec['checks'] if not x['ok']],
                code_fp=rec['registration']['values']['code_fp'])


def verdict(a, b):  # verbatim from parser_audit.verdict
    return all(a[k] == b[k] for k in ('active', 'code_fp'))


RES = dict(fp=FP, fp_expected=FP == '2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb',
           new_tool_sha256=digest(REPO / 'scripts/supp20_input_receipt.py'),
           baseline_tool_sha256=digest(BASE_RECEIPT), parts={},
           adapters=dict(old_REPO=dict(was=OLD_REPO_WAS, now=str(REPO)),
                         git_info='in-memory declared pin (same as Codex metadata_only)'))
T0 = time.monotonic()

# ---- A: 133 prior documents -------------------------------------------------------
prev = REPO / 'docs/reviews/codex_lhs214s_fix_recheck_evidence_20261019/lhs214s_recheck_20261019'
rrdir = REPO / 'docs/reviews/codex_lhs214rr_fix_recheck_evidence_20261019'
headings = json.loads((prev / 'evidence/s01_heading_boundary_cases.json').read_text(encoding='utf-8'))
fences = json.loads((rrdir / 'evidence/receipt_fence_matrix.json').read_text(encoding='utf-8'))
cases = [('heading', c['name'], prev / c['input'].replace('\\', '/')) for c in headings['rows']]
cases += [('fence', c['name'], rrdir / 'evidence/receipt_fence_cases' / (c['name'] + '.md')) for c in fences['cases']]
cx = {(r['group'], r['name']): r for r in cxload('prior_133_replay.json')['rows']}
rows = []
t = time.monotonic()
for group, name, path in cases:
    c = cx[(group, name)]
    doc = path.read_text(encoding='utf-8')
    before, after = actual(old, doc), actual(sr, doc)
    ro, rn = summary(old_receipt(path)), summary(sr.receipt(reg_doc=str(path)))
    exp = c['expected']
    rows.append(dict(
        group=group, name=name, sha_same=digest(path) == c['sha256'],
        old_same_as_codex=verdict(before, c['old']), new_same_as_codex=verdict(after, c['new']),
        old_receipt_same=ro == c['old_receipt'], new_receipt_same=rn == c['new_receipt'],
        old_match=verdict(before, exp), new_match=verdict(after, exp),
        new_receipt_match=rn['code_fp'] == exp['code_fp'], old_rc0=ro['rc'] == 0, new_rc0=rn['rc'] == 0))
tot = {}
for group in ('heading', 'fence'):
    g = [r for r in rows if r['group'] == group]
    tot[group] = dict(total=len(g), old_mismatch=sum(not r['old_match'] for r in g),
                      new_mismatch=sum(not r['new_match'] for r in g),
                      new_receipt_mismatch=sum(not r['new_receipt_match'] for r in g),
                      old_rc0=sum(r['old_rc0'] for r in g), new_rc0=sum(r['new_rc0'] for r in g),
                      inputs_same_sha=sum(r['sha_same'] for r in g),
                      decisions_same_as_codex=sum(r['old_same_as_codex'] and r['new_same_as_codex'] for r in g),
                      receipts_same_as_codex=sum(r['old_receipt_same'] and r['new_receipt_same'] for r in g))
RES['parts']['A_prior_133'] = dict(totals=tot, codex_totals=cxload('prior_133_replay.json')['totals'],
                                   totals_equal_codex={k: {kk: tot[k][kk] == cxload('prior_133_replay.json')['totals'][k][kk]
                                                           for kk in cxload('prior_133_replay.json')['totals'][k]} for k in tot},
                                   seconds=round(time.monotonic() - t, 1))
print('A', json.dumps(RES['parts']['A_prior_133']['totals'], ensure_ascii=False), flush=True)

# ---- B: 8,736 matrix (generation verbatim from new_boundaries) -------------------------
t = time.monotonic()
tails = ["", " ", "\t", " \t", "  ", "  ", " \x0b", " \x0c",
         " #", "\t####\t", " \\#", " ", "not-a-heading"]
closers = ["```", "````", "`````", "~~~", " ```", "   ````", "\t````", "```` ",
           "````\t", "```` ", "```` ", "```` x", "```` `", ""]
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
        before, after = actual(old, doc), actual(sr, doc)
        records.append(dict(name=f"{pattern}_{level}_{tails.index(tail)}_{closers.index(close)}_{int(history)}",
                            text=doc, differ=not verdict(before, after), new=after))
mat = cxload('new_boundary_matrix.json')
partB = dict(total=len(records), old_new_differ=sum(r['differ'] for r in records),
             codex_total=mat['total'], codex_old_mismatch=mat['old_mismatch'], codex_new_mismatch=mat['new_mismatch'],
             consistent=len(records) == mat['total'] and sum(r['differ'] for r in records) == mat['old_mismatch'])
# 12 representative full receipts
named = ["outside_1_0_0_0", "outside_2_0_0_1", "fenced_2_0_0_0", "fenced_2_0_1_0", "after_closer_2_0_1_1",
         "after_closer_3_0_1_0", "outside_2_8_0_0", "outside_2_9_0_1", "outside_7_0_0_0", "outside_2_11_0_0",
         "fenced_2_0_6_0", "fenced_2_0_9_0"]
registered = (REPO / sr.REG_DOC).read_text(encoding='utf-8')
base = re.sub(r"^## 3\.", "## 30.", re.sub(r"`code_fp_pending [0-9a-f]{64}`",
              "(pending removed for diagnostic)", registered), flags=re.M)
cxrec = {r['name']: r for r in cxload('new_boundary_receipts.json')['rows']}
d_new = OUT / 'new_cases'
d_new.mkdir(exist_ok=True)
rec_rows = []
byname = {r['name']: r for r in records}
for name in named:
    p = d_new / (name + '.md')
    p.write_text(base + "\n" + byname[name]['text'], encoding='utf-8')
    got = summary(sr.receipt(reg_doc=str(p)))
    bundle_doc = (CX / 'new_cases' / (name + '.md')).read_bytes().replace(b'\r\n', b'\n')
    rec_rows.append(dict(name=name, receipt=got, same_as_codex=got == cxrec[name]['actual'],
                         match_codex_expected=got['code_fp'] == cxrec[name]['expected']['code_fp'],
                         doc_same_as_bundle_lf=p.read_bytes() == bundle_doc))
partB['receipts12'] = dict(total=len(rec_rows), same_as_codex=sum(r['same_as_codex'] for r in rec_rows),
                           match_expected=sum(r['match_codex_expected'] for r in rec_rows),
                           docs_same_as_bundle=sum(r['doc_same_as_bundle_lf'] for r in rec_rows), rows=rec_rows)
partB['seconds'] = round(time.monotonic() - t, 1)
RES['parts']['B_matrix_8736'] = partB
print('B', json.dumps({k: v for k, v in partB.items() if k != 'receipts12'}, ensure_ascii=False),
      json.dumps({k: v for k, v in partB['receipts12'].items() if k != 'rows'}), flush=True)

# ---- C: 30,000 random documents (generation verbatim from randomized) ------------------
t = time.monotonic()
rng = random.Random(20261020)
lines = ["", "plain text", "#", "##", "###", "######", "#######",
         "# ", "##\t", "#  ", "##  ", "## ###", "# \\###",
         "## 3. Active", "## 3.\t#", "## 3.##", "## 4. Next",
         VAL, OTHER, "```", "~~~~", "``````", "```text", "~~~info`",
         "```x`", " ````", "   ~~~", "\t~~~", "```  ", "~~~~ x",
         "\\## 3. Escaped", "##not-heading"]
count, differ = 0, 0
for _ in range(30000):
    pool = [ln for ln in lines if not ln.startswith("\t")]
    doc = "\n".join(["## 3. Active", *rng.choices(pool, k=rng.randrange(1, 17)), VAL]) + "\n"
    before, after = actual(old, doc), actual(sr, doc)
    count += 1
    differ += not verdict(before, after)
rt = cxload('random_transitions.json')
RES['parts']['C_random_30000'] = dict(total=count, old_new_differ=differ, codex_total=rt['total'],
                                      codex_old_mismatch=rt['old_mismatch'], codex_new_mismatch=rt['new_mismatch'],
                                      consistent=count == rt['total'] and differ == rt['old_mismatch'],
                                      seconds=round(time.monotonic() - t, 1))
print('C', json.dumps(RES['parts']['C_random_30000']), flush=True)

# ---- D: 18 newline receipts (cases verbatim from supplementary.py) ---------------------
t = time.monotonic()
ncases = {
    "empty_h1": "## 3. Active\n#\n" + VAL + "\n",
    "empty_h2": "## 3. Active\n##\n" + VAL + "\n",
    "history": "## 3. Active\n" + VAL + "\n##\n" + OTHER + "\n",
    "fenced_empty": "## 3. Active\n````\n##\n````\n" + VAL + "\n",
    "fenced_value": "## 3. Active\n~~~\n" + VAL + "\n~~~\n",
    "mixed": "## 3. Active\n" + VAL + "\n```\n##\n" + OTHER + "\n```\n",
}
cxn = {(r['name'], r['newline']): r for r in cxload('newline_receipts.json')['rows']}
d_nl = OUT / 'newline_cases'
d_nl.mkdir(exist_ok=True)
nrows = []
for name, text in ncases.items():
    for newline, ending in [("lf", "\n"), ("crlf", "\r\n"), ("cr", "\r")]:
        p = d_nl / (name + "_" + newline + ".md")
        p.write_bytes((base + "\n" + text).replace("\n", ending).encode("utf-8"))
        got = summary(sr.receipt(reg_doc=str(p)))
        c = cxn[(name, newline)]
        want_bad = [] if c['expected']['code_fp'] == FP else ["R0", "D1"]
        nrows.append(dict(name=name, newline=newline, receipt=got, same_as_codex=got == c['receipt'],
                          match=(got['code_fp'] == c['expected']['code_fp'] and got['bad'] == want_bad
                                 and got['rc'] == bool(want_bad)),
                          doc_same_as_bundle=digest(p) == digest(CX / 'newline_cases' / p.name)))
RES['parts']['D_newline_18'] = dict(total=len(nrows), match=sum(r['match'] for r in nrows),
                                    same_as_codex=sum(r['same_as_codex'] for r in nrows),
                                    docs_same_as_bundle=sum(r['doc_same_as_bundle'] for r in nrows),
                                    seconds=round(time.monotonic() - t, 1), rows=nrows)
print('D', json.dumps({k: v for k, v in RES['parts']['D_newline_18'].items() if k != 'rows'}), flush=True)

# ---- E: 6 out-of-scope controls (verbatim from supplementary.py) -----------------------
unsupported = {
    "indented_heading": "## 3. Active\n ## Outside\n" + VAL + "\n",
    "setext_heading": "## 3. Active\nOutside\n---\n" + VAL + "\n",
    "html_empty_heading": "## 3. Active\n" + VAL + "\n<div>\n##\n</div>\n\n" + OTHER + "\n",
    "html_named_heading": "## 3. Active\n" + VAL + "\n<div>\n## Example\n</div>\n\n" + OTHER + "\n",
    "indented_code_value": "## 3. Active\n\n    " + VAL + "\n",
    "quoted_value": "## 3. Active\n> " + VAL + "\n",
}
cxu = {r['name']: r for r in cxload('unsupported_scope_controls.json')['cases']}
urows = []
for name, text in unsupported.items():
    before, after = actual(old, text), actual(sr, text)
    c = cxu[name]
    urows.append(dict(name=name, text_same=text == c['text'], old_same_as_codex=before == c['old'],
                      new_same_as_codex=after == c['new'], new=dict(active=after['active'], code_fp=after['code_fp']),
                      markdown_it_codex=dict(active=c['markdown_it']['active'], code_fp=c['markdown_it']['code_fp'])))
RES['parts']['E_unsupported_6'] = dict(total=len(urows), same_as_codex=sum(r['old_same_as_codex'] and r['new_same_as_codex'] for r in urows),
                                       rows=urows)
print('E', RES['parts']['E_unsupported_6']['same_as_codex'], '/', len(urows), flush=True)

# ---- F: actual registration document sections ----------------------------------------
noimp = cxload('actual_noimpact.json')
reg_text = (REPO / sr.REG_DOC).read_text(encoding='utf-8')
o_sec, n_sec = old._md_section(reg_text, 3, True), sr._md_section(reg_text, 3, True)
RES['parts']['F_actual_sections'] = dict(old_same_as_codex=list(o_sec) == noimp['old_section'],
                                         new_same_as_codex=list(n_sec) == noimp['new_section'],
                                         old_eq_new=o_sec == n_sec)
print('F', json.dumps(RES['parts']['F_actual_sections']), flush=True)
RES['adapter_calls'] = len(ADAPTER)
RES['seconds'] = round(time.monotonic() - T0, 1)
(OUT / 's06_nooracle.json').write_text(json.dumps(RES, ensure_ascii=False, indent=2), encoding='utf-8')
print('done', RES['seconds'], 's', flush=True)
