"""Reviewer-owned, read-only parser for captured text evidence; never imports target code."""
import ast
import collections
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
BMS = SOURCE / 'bms-balancing'
E = BMS / 'evidence/reil_c4e1_0b_20261103'
DOC = BMS / 'docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md'
stdout = (E / '01_red_e1_0b.stdout.log').read_text(encoding='utf-8')
lines = stdout.splitlines()
doc = DOC.read_text(encoding='utf-8')
doclines = doc.splitlines()
meta = json.loads((E / '01_red_e1_0b.meta.json').read_text(encoding='utf-8'))
end = json.loads((E / '03_end.json').read_text(encoding='utf-8'))

expected = []
for i, line in enumerate(doclines, 1):
    m = re.fullmatch(r'\| (\d) \| `(test_\w+)` \| (AssertionError|AttributeError) \| (정확히|접두) `(.*)` \| (\d+) \|', line)
    if m:
        number, name, exc, mode, message, predicted_line = m.groups()
        expected.append(dict(number=int(number), name=name, nodeid='tests/test_reil_c4e1_launch.py::'+name,
                             expected_exception=exc, message_match_mode='exact' if mode == '정확히' else 'prefix',
                             expected_message=message, predicted_line_reference_only=int(predicted_line), approval_line=i))
assert len(expected) == 9
passed_doc = doc.split('- **통과 24 (`PASSED`, `tests/test_reil_c4e1_launch.py::` 뒤):**', 1)[1].split('**GREEN (`02_green_e1_0b`):**', 1)[0]
expected_pass = ['tests/test_reil_c4e1_launch.py::'+n for n in re.findall(r'`(test_\w+)`', passed_doc)]
assert len(expected_pass) == 24
summary_at = next(i for i, line in enumerate(lines) if 'short test summary info' in line)
actual_sets = {}
set_checks = {}
for status, exp in [('FAILED', [x['nodeid'] for x in expected]), ('PASSED', expected_pass)]:
    actual = [line.split()[1] for line in lines[summary_at+1:] if line.startswith(status+' ')]
    actual_sets[status] = actual
    count = collections.Counter(actual)
    set_checks[status] = dict(expected_count=len(exp), actual_count=len(actual), missing=sorted(set(exp)-set(actual)),
                             extra=sorted(set(actual)-set(exp)), duplicates={k:v for k,v in count.items() if v>1},
                             match=set(exp)==set(actual) and len(actual)==len(set(actual)))

failure_end = next(i for i, line in enumerate(lines) if re.fullmatch(r'=+ PASSES =+', line))
headers = [(i, re.fullmatch(r'_+ (test_\w+) _+', line).group(1)) for i, line in enumerate(lines[:failure_end]) if re.fullmatch(r'_+ (test_\w+) _+', line)]
failure_checks = []
for expectation in expected:
    matches = [(n, pos) for n, (pos, name) in enumerate(headers) if name == expectation['name']]
    item = dict(expectation, matching_failure_section_count=len(matches))
    if len(matches)==1:
        n,pos = matches[0]
        finish = headers[n+1][0] if n+1<len(headers) else failure_end
        block = lines[pos+1:finish]
        traces = [(j+pos+2, line) for j,line in enumerate(block) if re.match(r'.+:\d+: in ',line)]
        errors = [(j+pos+2, line) for j,line in enumerate(block) if line.startswith('E   ')]
        explicit = [(lineno, line) for lineno,line in errors if re.fullmatch(r'E   [\w.]+(?:Error|Exception):.*',line)]
        chained = any(s in '\n'.join(block) for s in ['The above exception was the direct cause','During handling of the above exception'])
        first = traces[0] if traces else (None,None)
        trace_re = re.fullmatch(r'tests/test_reil_c4e1_launch.py:(\d+): in (test_\w+)',first[1] or '')
        actual_exception = actual_message = None
        if len(explicit)==1:
            actual_exception,actual_message = explicit[0][1][4:].split(': ',1)
        message_ok = (actual_message == expectation['expected_message'] if expectation['message_match_mode']=='exact'
                      else actual_message is not None and actual_message.startswith(expectation['expected_message']))
        trace_ok = trace_re is not None and trace_re.group(2)==expectation['name']
        item.update(stdout_header_line=pos+1, first_traceback_stdout_line=first[0], first_traceback=first[1],
                    actual_test_source_line=int(trace_re.group(1)) if trace_re else None, first_traceback_matches=trace_ok,
                    actual_exception_header_count=len(explicit), actual_exception=actual_exception, actual_message=actual_message,
                    exception_message_matches=message_ok and actual_exception==expectation['expected_exception'],
                    chained_exception_markers=chained, exception_block_raw=[{'line':n,'text':s} for n,s in errors],
                    match=trace_ok and len(explicit)==1 and not chained and message_ok and actual_exception==expectation['expected_exception'])
    failure_checks.append(item)

literal_names = {'LAUNCH', '_FIXED', 'RED_LAUNCH'}
literal_values = {}
runner_text = (E/'00_step_runner.py').read_text(encoding='utf-8')
for node in ast.parse(runner_text).body:
    if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in literal_names:
        literal_values[node.targets[0].id] = ast.literal_eval(node.value)
expected_hashes = {literal_values['LAUNCH']:literal_values['RED_LAUNCH'], **literal_values['_FIXED']}
sha_logs = {}
for name in ['01_red_e1_0b.source_sha256.txt','01_red_e1_0b.source_sha256_end.txt']:
    sha_logs[name] = dict((path,digest) for digest,path in re.findall(r'^([0-9a-f]{64})  (.+)$',(E/name).read_text(encoding='utf-8'),re.M))
available = {}
for path, expected_entry in expected_hashes.items():
    p = SOURCE/path
    if p.exists():
        b=p.read_bytes()
        measured={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
        available[path] = {'measured':measured,'matches':measured==expected_entry}
evidence_files = [{'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(E.iterdir()) if p.is_file()]
start_lines=(E/'00_start.txt').read_text(encoding='utf-8').splitlines()
parse_time=lambda s:datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
start_end_seconds=(parse_time(end['utc'])-parse_time(start_lines[0])).total_seconds()
common_checks = {
    'started_true':meta['started'] is True, 'timed_out_false':meta['timed_out'] is False,
    'cleanup_status_empty':meta['cleanup']['status']=='empty','cleanup_deadline_hit_false':meta['cleanup']['deadline_hit'] is False,
    'cleanup_errors_empty':meta['cleanup']['errors']==[], 'end_problems_empty':meta['end_problems']==[],
    'errors_empty':meta['errors']==[], 'runner_ok_true':meta['runner_ok'] is True,
    'meta_rc_1':meta['rc']==1,'outer_rc_1':(E/'01_red_e1_0b.outer_rc.txt').read_bytes()==b'1\n',
    'all_record_rc_0':all(v['rc']==0 for v in meta['records'].values()),
    'head_unchanged':meta['records']['head_start']['out']==meta['records']['head_end']['out'],
    'source_start_equals_fixed_RED_EXPECT':meta['source_start']==expected_hashes,
    'source_end_equals_fixed_RED_EXPECT':meta['source_end']==expected_hashes,
    'source_hash_logs_match_meta':all(values=={k:v['sha256'] for k,v in expected_hashes.items()} for values in sha_logs.values()),
    'stderr_empty':(E/'01_red_e1_0b.stderr.log').stat().st_size==0,
}
report = {
 'kind':'REIL_C4E1_0B_RED_STATIC_RESULT_REVIEW', 'captured_commit':'a38c878ff0055f588143288707d8b5f46646bf63',
 'method':'Reviewer-owned standard-library text/JSON parsing, AST literal extraction, and SHA-256 only. No target imports, target calls, tests, probes, Git fixtures, or target-code execution.',
 'verdict':'RED_EXPECTATION_MISMATCH_STOP_REQUIRED',
 'node_sets':set_checks,'observed_summary_nodes':actual_sets,
 'failure_checks':failure_checks,
 'matching_failures':[re.match(r'test_(l\d+)_',x['name']).group(1) for x in failure_checks if x.get('match')],
 'all_claimed_eight_match':sum(x.get('match',False) for x in failure_checks)==8 and not failure_checks[-1]['match'],
 'l33':{
   'required_message':expected[-1]['expected_message'],
   'actual':'Baseline assert post()["problems"] == [] fails at tests/test_reil_c4e1_launch.py:1063, before the deadline test.',
   'raw_exception_header_present':False,
   'raw_observed_problem_count':2,
   'first_fully_rendered_problem':lines[61],
   'second_problem_fully_rendered':False,
   'line_number_rule':'1065 is only a prediction/reference under §4-3. The rejection is based on the missing required exception/message, not line-number inequality alone.',
   'source_inference_boundary':'The second problem and why both arise can be inferred from captured source, but the raw log does not independently expose its complete text. This report does not reconstruct omitted raw output.'
 },
 'summary_and_errors':{
   'summary_heading_line':summary_at+1,'last_line_number':len(lines),'last_line':lines[-1],
   'matches_required_counts_only':lines[-1]=='9 failed, 24 passed in 14.25s',
   'warning_count_reported':0,'unexpected_red_cause_occurrences':stdout.count('UNEXPECTED_RED_CAUSE'),
   'ERROR_lines':[{'line':i+1,'text':s} for i,s in enumerate(lines) if re.match(r'^ERROR(?:\s|$)',s)],
   'INTERNALERROR_occurrences':stdout.count('INTERNALERROR'),
   'Interrupted_occurrences':stdout.count('Interrupted'),'bang_interrupt_markers':stdout.count('!!!!'),
   'summary_other_lines':[{'line':i+1,'text':s} for i,s in enumerate(lines) if i>summary_at and not s.startswith(('FAILED ','PASSED '))],
   'falseextra_judgment':'The sole non-node line in the summary section is the required terminal count/time summary (line 138). Counting it as a prohibited extra line is an author-judge false positive. §4-3 forbids extra nodeids and error/interruption/result categories, not this mandatory summary line; it is not another RED mismatch.',
   'author_judge_script_available':False,
   'author_judge_limit':'The reported judge implementation is outside the repository and not captured. This review independently verifies only that the alleged extra line is permitted by the request.'
 },
 'common_checks':common_checks,'common_checks_all_pass':all(common_checks.values()),
 'cleanup':meta['cleanup'],'problems':meta['problems'],'end_problems':meta['end_problems'],'errors':meta['errors'],'first_error':meta['first_error'],
 'records':{'head_start':meta['records']['head_start']['out'],'head_end':meta['records']['head_end']['out'],
            'porcelain_start':(E/'01_red_e1_0b.porcelain_start.txt').read_text(encoding='utf-8').splitlines(),
            'porcelain_end':(E/'01_red_e1_0b.porcelain_end.txt').read_text(encoding='utf-8').splitlines(),
            'interpretation':'The two snapshots show only untracked files created for this evidence. They do not independently prove absence of transient activity between snapshots.'},
 'timing':{'start_record_utc':start_lines[0],'runner_start_utc':meta['start_utc'],'runner_end_utc':meta['end_utc'],
           'end_record_utc':end['utc'],'start_record_to_end_record_seconds':start_end_seconds,'runner_times':meta['times'],
           'child_timeout_seconds':meta['timeout_s'],'cleanup_budget_seconds':meta['cleanup_s'],
           'child_within_timeout':meta['times']['child_s']<meta['timeout_s'],
           'cleanup_within_budget':meta['times']['cleanup_s']<meta['cleanup_s'],
           'recorded_interval_within_two_hours':start_end_seconds<7200,
           'limits':'The 193-second interval begins at 00_start (step b) and ends at e; it excludes step a and post-e commits/push/documentation. The evidence alone therefore is not an independently complete a-to-e wall-clock measurement.'},
 'hashes':{'source_expected_count':len(expected_hashes),'source_start_count':len(meta['source_start']),
           'source_end_count':len(meta['source_end']),'independently_measured_available_source_files':available,
           'unavailable_source_files_in_this_capture':sorted(set(expected_hashes)-set(available)),
           'runner_record_sha_matches_file':meta['runner']['sha256']==hashlib.sha256((E/'00_step_runner.py').read_bytes()).hexdigest(),
           'copies_end_sha_match_available_files':all(hashlib.sha256((SOURCE/k).read_bytes()).hexdigest()==v for k,v in end['copies_sha256'].items()),
           'source_start_and_end_log_bytes_equal':(E/'01_red_e1_0b.source_sha256.txt').read_bytes()==(E/'01_red_e1_0b.source_sha256_end.txt').read_bytes()},
 'end_record':{'green_meta_missing_recorded':end['steps']['02_green_e1_0b'],'copies_sha256':end['copies_sha256'],
               'current_launcher_remains_v5':end['copies_sha256']['bms-balancing/scripts/reil_c4e1_launch.py']==literal_values['RED_LAUNCH']['sha256'],
               'no_green_files_in_captured_evidence':not any(p.name.startswith('02_green') for p in E.iterdir())},
 'evidence_file_count':len(evidence_files),'evidence_total_bytes':sum(x['bytes'] for x in evidence_files),'evidence_files':evidence_files,
 'limitations':[
   'Original pytest --tb=short/saferepr output abbreviates l23/l29 tuple tails, assertion diffs, and l33 second problem. Required l23/l29 prefixes are fully present and match; no full raw child meta or fixture files are present here.',
   'The full captured stdout is 138 lines and contains a final summary; all lines were parsed directly from disk. Earlier tool-display truncation does not affect these results. Pytest-originated abbreviation remains irrecoverable from these raw artifacts.',
   'All eight matching failures establish only the executed failing path. Multi-case functions stop at the first failure (l23 rewrite; l30 localtls), and interface-level l28/l31/l32 do not exercise missing v6 behavior.',
   'runner_ok=true validates outer execution/cleanup/recording conditions; it does not validate the RED expectation matrix.',
   'This is not E1-0b success or authorization to continue. Eight matches may be retained as historical evidence, but the fixed 9-failure gate failed and cannot be turned into partial acceptance.'
 ]
}
(ROOT/'RED_RESULT_REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['verdict','node_sets','all_claimed_eight_match','common_checks_all_pass','evidence_file_count','evidence_total_bytes']},ensure_ascii=False,indent=2))
