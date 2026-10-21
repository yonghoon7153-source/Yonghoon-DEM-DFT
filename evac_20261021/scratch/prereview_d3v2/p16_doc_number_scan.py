#!/usr/bin/env python3
"""PRE-D3V2 탐침 16 — v2 문서의 소수 · 지수 표기 숫자를 전부 뽑아, (가) V2_DOC_NUMBERS 표 · (나) 규칙 검사 최종 출력에 있는
숫자 (표기 자릿수 안 · 스크립트의 matches 규칙) 와 대조한다.  어느 쪽에도 없는 숫자 = '검사 밖 숫자' 목록 (손으로 본다).

재실행: python3 -I p16_doc_number_scan.py   (가볍다)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
doc = open(os.path.join(pcommon.REPO, 'docs/reviews/mixer_d3_se_flowability_anchor_design_v2_20261021.md'), encoding='utf-8').read()
outp = open(os.path.join(pcommon.REPO, 'docs/reviews/mixer_d3_design_v2_evidence_20261021/d3_v2_rule_checks_output.txt'), encoding='utf-8').read()
SUPMAP = str.maketrans('⁻⁰¹²³⁴⁵⁶⁷⁸⁹', '-0123456789')
num_re = re.compile(r'(?<![0-9A-Za-z_.])(\d+\.\d+)(?:\s*×\s*10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+))?')
out_vals = []
for t in re.findall(r'-?\d+\.\d+(?:e[-+]?\d+)?', outp):
    try:
        out_vals.append(float(t))
    except ValueError:
        pass
tab_vals = []
for v in c.V2_DOC_NUMBERS.values():
    tab_vals.append(v)


def typed(m):
    mant, ex = m.group(1), m.group(2)
    return f'{mant}e{ex.translate(SUPMAP)}' if ex else mant


rows = []
for m in num_re.finditer(doc):
    s = typed(m)
    in_tab = any(s == t for t in tab_vals)
    in_out = any(c.matches(s, v) for v in out_vals)
    if not (in_tab or in_out):
        line_no = doc.count('\n', 0, m.start()) + 1
        ctx = doc[max(0, m.start() - 60):m.end() + 40].replace('\n', ' ')
        rows.append(dict(line=line_no, token=s, context=ctx))
pcommon.dump('p16_doc_number_scan.json', rows)
print(f'검사 밖 소수 · 지수 숫자 {len(rows)} 개 (표 · 최종 출력 어디에도 없음):')
for r in rows:
    print(f"  L{r['line']:3d} {r['token']:>12s} | {r['context']}")
