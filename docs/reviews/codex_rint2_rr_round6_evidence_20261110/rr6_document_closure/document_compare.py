"""Independent, read-only document comparison for round6 Q1-Q3.

This imports no project module and runs no research, host or project test.
Usage: python document_compare.py --repo PATH --prior-verdict PATH --out PATH
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--repo', required=True, type=Path)
p.add_argument('--prior-verdict', required=True, type=Path)
p.add_argument('--out', required=True, type=Path)
a = p.parse_args()

paths = {
    'prior': 'docs/reviews/codex_review_rint2_rr_round5_20261109.md',
    'fix': 'docs/reviews/rint2_rr5_fix_plan_20261109.md',
    'registration': 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md',
    'old_request': 'docs/reviews/codex_rint2_rr_round5_request_20261109.md',
    'request': 'docs/reviews/codex_rint2_rr_round6_request_20261109.md',
    'rules': 'CLAUDE.md',
    'ledger': 'docs/reviews/findings.json',
}
raw = {key: (a.repo / path).read_bytes() for key, path in paths.items()}
lines = {key: data.decode('utf-8-sig').splitlines() for key, data in raw.items()}

def find_line(key, token):
    found = [(i + 1, x) for i, x in enumerate(lines[key]) if token in x]
    if len(found) != 1:
        raise ValueError((key, token, len(found)))
    return found[0]

prior_narrow = find_line('prior', '> PC14-02/03, RR4-01')[1].strip()[2:]
new_narrow = find_line('fix', '> PC14-02/03, RR4-01')[1].strip()[2:]
prior_min = find_line('prior', '> s_min은 자기')[1].strip()[2:]
new_min_line = find_line('registration', '⑤′ (11-09')
new_min = re.search(r'\*"(s_min은 자기.+?)"\*', new_min_line[1]).group(1)

selected = {
    'prior': [95, 105, 124, 130, 146, 156, 160, 162, 163, 165, 208, 212, 214],
    'fix': [4, 12, 13, 14, 15, 22, 23, 25, 31, 32, 36, 40, 41, 42, 53],
    'registration': [101, 102, 105, 106, 107, 109],
    'old_request': [86, 139],
    'request': [11, 12, 13, 46, 47, 48],
    'rules': [114],
    'ledger': [12454, 12456, 12461, 16569, 16571, 16585, 16804, 16806, 16811],
}

checks = {
    'packet_prior_verdict_bytes_equal_independently_saved_round5': raw['prior'] == a.prior_verdict.read_bytes(),
    'narrow_acceptance_quote_literal_equal': prior_narrow == new_narrow,
    'minimal_smin_quote_literal_equal': prior_min == new_min,
    'minimal_smin_quote_equal_ignoring_whitespace': re.sub(r'\s+', '', prior_min) == re.sub(r'\s+', '', new_min),
    '19_9_conditions_present': all(t in lines['registration'][104] for t in ('축방향 경로가 살아 있고', '이상 원통 근사가 맞을 때', '작은 상한을 증명하지 못한다')),
    'unreg_conditions_present': all(t in lines['registration'][104] for t in ('같은 그래프', '같은 R_j', '다른 설정 고정', '부분 융합', '다시 보정한 예측 상한으로 옮기지 않는다')),
    'old_bad_technical_report_in_strikethrough': '~~0 이면 (가)–(다) 가 DBE 에서도 같은 동작이었다는 자료 · 0 이 아니면 한정어로 적는다~~' in lines['registration'][106],
    's0_manual_source_finalrc_scope_present': all(t in lines['fix'][40] for t in ('사람이', '정확한 `rss.log` 하나', '종결 위치', '생산자 `run2.sh` 결속', '자동 생산자 / 최종 rc 인증기로 쓰지 않는다')),
}

result = {
    'review_pin': 'aec8ca2f6cbc24d43e2ed447c61ce6b62dd19f1e',
    'scope': 'Q1/Q2/Q3 document comparison only; no project module imported or executed',
    'file_hashes': {paths[k]: hashlib.sha256(v).hexdigest() for k, v in raw.items()},
    'checks': checks,
    'literal_difference_note': 'The s_min quote differs only by spaces (그 수가0 vs 그 수가 0; s_min=0 vs s_min = 0). No substantive difference. The narrow acceptance quote is literally identical.',
    'source_extracts': {paths[k]: [{'line': n, 'text': lines[k][n-1]} for n in ns] for k, ns in selected.items()},
    'verdict': {'Q1_RR5_01': 'closed_document_correction_only', 'Q2': 'accepted_narrow_wording_only', 'Q3': 'accepted_manual_review_boundary_only'},
    'new_findings': [],
    'not_certified': ['RCA-11 entire closure', 'actual R plan s_min seal', 'summaryless copied-prefix integrity', 'automatic S0 producer/final-rc certification', 'host qualification', 'research or production GO'],
}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'checks': checks, 'out': str(a.out)}, ensure_ascii=False, indent=2))
expected = {k: True for k in checks}
expected['minimal_smin_quote_literal_equal'] = False
raise SystemExit(0 if checks == expected else 1)
