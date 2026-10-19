"""Read-only production-function review; all generated evidence stays in review root."""
from pathlib import Path
import contextlib
import difflib
import hashlib
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import time
from unittest.mock import patch

R = Path(__file__).resolve().parents[1]
S = R / 'source'
OLD = R.parent / 'lhs214rr_recheck_20261019'
O = R / 'evidence'
PIN = '685c2bbdbbfee82898a9ec062bb9c2bc94612fc8'
DEPS = [R.parent / 'lhs_coverage_review_20260930/deps',
        R.parent / 'gen2_network_reverify3_20261007/deps', OLD / 'deps']
sys.path[:0] = list(map(str, [S / 'scripts', *DEPS]))
sys.dont_write_bytecode = True
for name in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['PYTHONPATH'] = os.pathsep.join(map(str, DEPS))
(R / 'tmp').mkdir(exist_ok=True)
tempfile.tempdir = str(R / 'tmp')
os.environ['TEMP'] = os.environ['TMP'] = str(R / 'tmp')
import supp20_input_receipt as sr
from markdown_it import MarkdownIt

MD = MarkdownIt('commonmark')
ADAPTER_CALLS = []


def git_metadata_only(*args, **kwargs):
    ADAPTER_CALLS.append('git_info: record declared source pin; no Git command')
    return dict(sha=PIN, short=PIN[:9], branch='review-snapshot', dirty=False, porcelain=[])


sr.NP.git_info = git_metadata_only


def save(name, data):
    (O / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf8')


def summarize(rec):
    return dict(rc=rec['rc'], bad=[x['id'] for x in rec['checks'] if not x['ok']],
                code_fp=rec['registration']['values']['code_fp'])


def oracle(text):
    """Use markdown-it block tokens for heading boundaries and fenced-code spans."""
    tokens = MD.parse(text)
    heads = [(t.map[0], int(t.tag[1:]), tokens[i + 1].content)
             for i, t in enumerate(tokens) if t.type == 'heading_open']
    hits = [h for h in heads if h[1] == 2 and re.match(r'3\.(\s|$)', h[2])]
    if len(hits) != 1:
        return dict(active=False, code_fp=None, heads=heads, body=None)
    i0 = hits[0][0]
    i1 = next((h[0] for h in heads if h[0] > i0 and h[1] <= 2), len(text.split('\n')))
    code = set()
    for t in tokens:
        if t.type == 'fence':
            code.update(range(*t.map))
    body = '\n'.join(ln for i, ln in enumerate(text.split('\n')) if i0 <= i < i1 and i not in code)
    vals = sorted(set(re.findall(r'`code_fp ([0-9a-f]{64})`', body)))
    return dict(active=True, code_fp=vals[0] if len(vals) == 1 else None, heads=heads, body=body)


def old_module():
    spec = importlib.util.spec_from_file_location('s01_baseline_receipt', OLD / 'source/scripts/supp20_input_receipt.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def replay():
    prior = json.loads((OLD / 'evidence/receipt_fence_matrix.json').read_text(encoding='utf8'))
    rows = []
    started = time.monotonic()
    for case in prior['cases']:
        p = OLD / 'evidence/receipt_fence_cases' / (case['name'] + '.md')
        text = p.read_text(encoding='utf8')
        expected = oracle(case['extra'])
        body, why = sr._md_section(text, 3, strip_code=True)
        rec = sr.receipt(reg_doc=str(p))
        got = summarize(rec)
        row = dict(name=case['name'], oracle=expected,
                   parser_active=body is not None, parser_reason=why, receipt=got,
                   heading_mismatch=(body is not None) != expected['active'],
                   value_mismatch=got['code_fp'] != expected['code_fp'])
        rows.append(row)
    result = dict(total=len(rows), heading_mismatches=sum(x['heading_mismatch'] for x in rows),
                  value_mismatches=sum(x['value_mismatch'] for x in rows),
                  receipts_rc0=sum(x['receipt']['rc'] == 0 for x in rows),
                  seconds=time.monotonic() - started, rows=rows)
    save('s01_replay_114.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}), flush=True)


def fence_expansion():
    fp = sr.NP.code_fp(sr.NP.code_hashes())
    mismatches = []
    count = 0
    by_purpose = dict(example_heading=0, active_value=0)
    variants = {'empty': '', 'space': ' ', 'tab': '\t', 'space_tab': ' \t',
                'nbsp': '\u00a0', 'emspace': '\u2003', 'vertical_tab': '\x0b',
                'formfeed': '\x0c', 'zero_width': '\u200b', 'text': ' x'}
    indents = ['', ' ', '  ', '   ', '    ', '\t', ' \t', '  \t', '   \t', '\t ']
    for ch in '`~':
        for width in [3, 4, 5, 8]:
            for opening_indent in ['', ' ', '  ', '   ']:
                for closing_indent in indents:
                    for tail_label, tail in variants.items():
                        for close_width in [width - 1, width, width + 1]:
                            block = (opening_indent + ch * width + 'markdown\n' +
                                     closing_indent + ch * close_width + tail + '\n')
                            examples = dict(example_heading=block + '## 3. Candidate\n`code_fp ' + fp + '`\n' + ch * width + '\n',
                                            active_value='## 3. Active section\n\n' + block + '`code_fp ' + fp + '`\n' + ch * width + '\n')
                            for purpose, extra in examples.items():
                                expect = oracle(extra)
                                body, why = sr._md_section(extra, 3, strip_code=True)
                                vals = sorted(set(re.findall(r'`code_fp ([0-9a-f]{64})`', body or '')))
                                actual_fp = vals[0] if len(vals) == 1 else None
                                count += 1
                                by_purpose[purpose] += 1
                                if (body is not None) != expect['active'] or actual_fp != expect['code_fp']:
                                    mismatches.append(dict(extra=extra, expected=expect, actual=body, why=why,
                                                           tail=tail_label, purpose=purpose, actual_fp=actual_fp))
    save('s01_new_fence_matrix.json', dict(total=count, by_purpose=by_purpose, mismatches=mismatches))
    print(json.dumps(dict(new_fences=count, mismatches=len(mismatches))), flush=True)


def boundaries():
    fp = sr.NP.code_fp(sr.NP.code_hashes())
    doc = (S / sr.REG_DOC).read_text(encoding='utf8')
    base = re.sub(r'^## 3\.', '## 30.', re.sub(r'`code_fp_pending [0-9a-f]{64}`', '(pending removed for diagnostic)', doc), flags=re.M)
    cases = {}
    for level in [1, 2]:
        for label, tail in [('empty', ''), ('space', ' '), ('tab', '\t'), ('space_tab', ' \t'),
                            ('nbsp', ' \u00a0'), ('emspace', ' \u2003'), ('normal', ' Outside')]:
            cases[f'h{level}_{label}'] = f'## 3. Active section without a value\n\n{"#" * level}{tail}\n\n`code_fp {fp}`\n'
    cases['fence_value_control'] = f'## 3. Active section\n````markdown\n`code_fp {fp}`\n````\n'
    cases['outside_and_fenced_value'] = f'## 3. Active section\n`code_fp {fp}`\n```text\n`code_fp {"0" * 64}`\n```\n'
    cases['normal_value_control'] = f'## 3. Active section\n`code_fp {fp}`\n'
    for level in [1, 2]:
        cases[f'h{level}_live_before_blank_history'] = f'## 3. Active section\n`code_fp {fp}`\n\n{"#" * level}\n\nHistorical value: `code_fp {"0" * 64}`\n'
    baseline = old_module()
    directory = O / 's01_new_cases'
    directory.mkdir(exist_ok=True)
    rows = []
    for name, extra in cases.items():
        p = directory / (name + '.md')
        p.write_text(base + '\n' + extra, encoding='utf8')
        expect = oracle(extra)
        rec = sr.receipt(reg_doc=str(p))
        before = baseline.registration_values(reg_doc=str(p))
        row = dict(name=name, extra=extra, input=str(p.relative_to(R)), oracle=expect,
                   actual=summarize(rec), baseline_code_fp=before[0]['code_fp'],
                   baseline_problems=before[1], mismatch=rec['registration']['values']['code_fp'] != expect['code_fp'])
        rows.append(row)
        save('s01_receipt_' + name + '.json', rec)
    result = dict(total=len(rows), mismatches=sum(x['mismatch'] for x in rows),
                  fail_open=sum(x['mismatch'] and x['actual']['rc'] == 0 for x in rows),
                  false_rejections=sum(x['mismatch'] and x['actual']['rc'] == 1 and x['oracle']['code_fp'] is not None for x in rows), rows=rows)
    save('s01_heading_boundary_cases.json', result)
    print(json.dumps(dict(boundaries=len(rows), mismatches=result['mismatches'],
                         rc0=[x['name'] for x in rows if x['mismatch'] and x['actual']['rc'] == 0])), flush=True)


def noimpact():
    before = old_module()
    old_values = before.registration_values(str(S / sr.REG_DOC), str(S / sr.RUNS_README))
    new_values = sr.registration_values()
    old_rec = before.receipt(reg_doc=str(S / sr.REG_DOC), readme=str(S / sr.RUNS_README),
                             r3_tgz=str(S / sr.R3_TGZ), r2_tgz=str(S / sr.R2_TGZ))
    new_rec = sr.receipt()
    # Old module's _rp also locates harvest and design; compare the actual fields, not paths.
    save('s01_actual_registration.json', dict(values_equal=old_values == new_values,
                                             before_values=old_values, after_values=new_values,
                                             before=summarize(old_rec), after=summarize(new_rec)))
    save('s01_actual_receipt.json', new_rec)
    print(json.dumps(dict(actual_registration_equal=old_values == new_values, actual_receipt=summarize(new_rec))), flush=True)


def selftest():
    original_run = sr.NP.subprocess.run
    def run(argv, *args, **kwargs):
        if isinstance(argv, (list, tuple)) and argv and str(argv[0]).lower() == 'git':
            raise AssertionError('Git commands are prohibited')
        if isinstance(argv, list) and len(argv) > 4 and argv[1:4] == ['-I', '-B', '-c'] and argv[4] == sr.NP.GEN_PROBE:
            argv = list(argv)
            argv[4] = 'import sys; sys.path[:0] = ' + repr(list(map(str, DEPS))) + '\n' + argv[4]
            ADAPTER_CALLS.append('isolated GEN_PROBE dependency roots only')
        return original_run(argv, *args, **kwargs)
    started = time.monotonic()
    with patch.object(sr.NP.subprocess, 'run', run), (O / 's01_selftest.log').open('w', encoding='utf8') as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        rc = sr._selftest()
    save('s01_selftest_adapter.json', dict(rc=rc, calls=ADAPTER_CALLS, seconds=time.monotonic() - started))
    print(json.dumps(dict(selftest_rc=rc, seconds=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    O.mkdir(exist_ok=True)
    command = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if command == 'all':
        for fn in [replay, fence_expansion, boundaries, noimpact]:
            fn()
        save('s01_adapter.json', dict(declared_source_pin=PIN,
                                     source_sha256=hashlib.sha256((S / 'scripts/supp20_input_receipt.py').read_bytes()).hexdigest(),
                                     baseline_sha256=hashlib.sha256((OLD / 'source/scripts/supp20_input_receipt.py').read_bytes()).hexdigest(),
                                     markdown_it_version=__import__('importlib.metadata').metadata.version('markdown-it-py'),
                                     git_commands_executed=False, git_info_stub_calls=len(ADAPTER_CALLS),
                                     no_production_source_changes=True))
    else:
        globals()[command]()
