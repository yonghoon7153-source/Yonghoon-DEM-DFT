#!/usr/bin/env python3
"""scratch 원 출력 (evidence/raw/) → 봉인 기록에 넣을 사본 (evidence/) — 긴 시험 · 규율 검사 출력은 요약 · 철회값 등록부 글자는 ‹등록부 CL-nn› 로 가림.
원 출력은 scratch 에 그대로 둔다 (이 사본은 리포에 넣는 판 · 등록부 원문을 다시 옮기지 않는다 = 철회값 스윕 규율).

argv: <raw 폴더> <사본 폴더> <등록부 claims.json>
"""
import json
import os
import re
import sys

RAW, OUT, CLAIMS = sys.argv[1:4]
bans = [(b['pattern'], b.get('claim', '?')) for b in json.load(open(CLAIMS, encoding='utf-8')).get('quotation_ban', []) if b.get('pattern')]
os.makedirs(OUT, exist_ok=True)


def summarize_test(lines):
    keep = [ln for ln in lines if ln.startswith('#') or ln.startswith('test_rint_r_chain') or ln.startswith('  FAIL') or ln.startswith('real')
            or ln.startswith('rc=')]
    npass = sum(ln.startswith('  PASS') for ln in lines)
    nfail = sum(ln.startswith('  FAIL') for ln in lines)
    return keep + [f'(요약 · PASS 줄 {npass} · FAIL 줄 {nfail} · 원 출력 {len(lines)} 줄 = scratch evidence/raw/)']


def summarize_disc(lines):
    keep = [ln for ln in lines if ln.startswith('#') or '방법론 규율' in ln or ln.startswith('  ✗') or ln.startswith('ERR') or ln.startswith('real')
            or ln.startswith('rc=')]
    nok = sum(ln.startswith('  OK') for ln in lines)
    nw = sum(ln.startswith('  ⚠') for ln in lines)
    return keep + [f'(요약 · OK 줄 {nok} · ⚠ 경고 줄 {nw} · 원 출력 {len(lines)} 줄 = scratch evidence/raw/ · 등록부 원문 인용이 있어 리포에 옮기지 않음)']


rep = []
for name in sorted(os.listdir(RAW)):
    src = os.path.join(RAW, name)
    if not os.path.isfile(src):
        continue
    text = open(src, encoding='utf-8').read()
    lines = text.split('\n')
    if name.startswith('e1_'):
        lines = summarize_test(lines)
    elif name.startswith('e7_'):
        lines = summarize_disc(lines)
    out = '\n'.join(lines)
    n = 0
    for pat, cl in bans:
        if pat in out:
            n += out.count(pat)
            out = out.replace(pat, f'‹등록부 {cl}›')
    if n:
        out = f'# (리포 사본 · 철회값 등록부 글자 {n} 곳을 ‹등록부 CL-nn› 로 가림 · 원 출력 = scratch evidence/raw/{name})\n' + out
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(out if out.endswith('\n') else out + '\n')
    left = [p for p, _ in bans if p in out]
    rep.append((name, len(text.encode("utf-8")), len(out.encode("utf-8")), n, left))
for r in rep:
    print(f'{r[0]}: 원 {r[1]} B → 사본 {r[2]} B · 가림 {r[3]} · 남은 등록부 글자 {r[4] if r[4] else "없음"}')
sys.exit(1 if any(r[4] for r in rep) else 0)
