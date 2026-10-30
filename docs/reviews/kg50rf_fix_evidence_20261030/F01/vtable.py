"""vverbose_old.log · vverbose_new.log → V 장면 표 (Markdown) — 장면 · 종류 · 고치기 전 · 고친 뒤 · 시험 판정.
   각 [-C] · [흐름] 줄 바로 뒤의 PASS/FAIL 줄이 그 장면이다 (test_vonly_verbose.py 가 찍는 순서)."""
import re
import sys


def rows(path):
    out, pend = [], None
    for l in open(path, encoding='utf-8', errors='replace'):
        l = l.rstrip('\n')
        m = re.match(r'^  \[(-C|흐름)\] (.*)$', l)
        if m:
            pend = (m.group(1), m.group(2))
            continue
        m = re.match(r'^(PASS|FAIL) (V[0-9]+[a-z]?) (.*)$', l)
        if m and pend:
            st, tid, rest = m.groups()
            kind = '본 흐름' if pend[0] == '흐름' else '-C'
            res = pend[1]
            if kind == '-C':
                mm = re.match(r'rc=([0-9]+) · 재개 덱 정적 대조: (통과|실패) \(문제 ([0-9]+)\) · KG50R-F01 문제 ([0-9]+)', res)
                res = ('rc %s · %s %s · F01 %s' % mm.groups()) if mm else res
            else:
                mm = re.match(r'시험 ([0-9]+) · 본 ([0-9]+) · (.*)$', res)
                if mm:
                    v = re.search(r'(통과|실패) \(문제 ([0-9]+)\)', mm.group(3))
                    res = '시험 %s · 본 %s · 정적 %s' % (mm.group(1), mm.group(2), ('%s %s' % v.groups()) if v else '-')
            mt = re.match(r'^(.*?)( → -C | → 본 흐름 | · 본 흐름 \(-T\))', rest)
            tag = (mt.group(1) if mt else rest)[:90]
            out.append((tid, kind, tag, res, st))
            pend = None
    return out


old, new = rows(sys.argv[1]), rows(sys.argv[2])
assert [(a[0], a[1]) for a in old] == [(b[0], b[1]) for b in new], '장면 순서가 다름'
print('| 장면 | 대조 | 내용 | 고치기 전 판 (77c24237) | 판정 | 고친 판 | 판정 |')
print('|---|---|---|---|---|---|---|')
for a, b in zip(old, new):
    print('| %s | %s | %s | %s | %s | %s | %s |' % (a[0], a[1], a[2].replace('|', '\\|'), a[3], a[4], b[3], b[4]))
print()
print('고치기 전: PASS %d · FAIL %d / 고친 판: PASS %d · FAIL %d' % (sum(x[4] == 'PASS' for x in old), sum(x[4] == 'FAIL' for x in old),
                                                              sum(x[4] == 'PASS' for x in new), sum(x[4] == 'FAIL' for x in new)))
