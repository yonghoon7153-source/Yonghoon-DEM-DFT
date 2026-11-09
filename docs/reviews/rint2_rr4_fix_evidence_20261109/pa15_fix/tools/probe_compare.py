# -*- coding: utf-8 -*-
"""사전 공격 15 탐침 출력 대조 — 원 출력 (반입 preattack15/out · 고친 판 e94f09905 사본) ↔ 고침 C 재실행 출력 (같은 탐침 바이트 · PA15_TREE = 고친 작업 트리) →
탐침 · 꼴마다 [원 = 받음 | 거부] → [새 = 받음 | 거부] 표 (받음 = 세 자리 모두 통과 · 탐침 h.accepted 와 같은 셈).  쓰임: python3 probe_compare.py <원 out> <새 out>."""
import json
import sys
from pathlib import Path

A, B = Path(sys.argv[1]), Path(sys.argv[2])


def acc(o):
    if not isinstance(o, dict):
        return None
    if 'accepted_all_three' in o:
        return o['accepted_all_three']
    if 'accepted' in o:
        return o['accepted']
    w, p, c = o.get('writer'), o.get('places'), o.get('cli')
    if w is None and p is None:
        return None
    return (isinstance(w, list) and w[0] is True and isinstance(p, list) and p[1] is None and p[2] is None and isinstance(c, list) and c[1] is True)


def short(o):
    if not isinstance(o, dict):
        return json.dumps(o, ensure_ascii=False, default=str)[:90]
    c = o.get('cli')
    p = o.get('places')
    return f'cli {json.dumps(c, ensure_ascii=False, default=str)[:60]} · places {json.dumps(p, ensure_ascii=False, default=str)[:90]}'


def load(p):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


for name in ('p1_sigafter', 'p2_orphan', 'p3_moved_source', 'p4_honest', 'p5_variants', 'p6_src_link', 'p7_orphan_types', 'p8_outdir', 'p9_rename',
             'p10_honest_more', 'p11_honest_pre', 'p13_honest_sigafter', 'p14_exceptions', 'p15_order_crash'):
    a, b = load(A / f'{name}.json'), load(B / f'{name}.json')
    print(f'## {name}')
    if a is None or b is None:
        print('  (출력 없음)', a is None, b is None)
        continue
    if name == 'p14_exceptions':
        for k in sorted(set(a) | set(b)):
            print(f'  {k} direct: 원 {str((a.get(k) or {}).get("direct"))[:110]}')
            print(f'  {" " * len(k)}         새 {str((b.get(k) or {}).get("direct"))[:110]}')
        continue
    if name in ('p3_moved_source', 'p15_order_crash', 'p6_src_link'):
        for k in sorted(set(a) | set(b)):
            print(f'  {k}: 원 {json.dumps(a.get(k), ensure_ascii=False, default=str)[:150]}')
            print(f'  {" " * len(k)}  새 {json.dumps(b.get(k), ensure_ascii=False, default=str)[:150]}')
        continue
    keys = [k for k in a if isinstance(a[k], dict) or k in b]
    for k in keys:
        va, vb = a.get(k), b.get(k)
        if isinstance(va, dict) and ('writer' in va or 'cli' in va or 'accepted_all_three' in va or 'accepted' in va):
            print(f'  {k}: 원 {"받음" if acc(va) else "거부"} → 새 {"받음" if acc(vb) else "거부"} | 새 {short(vb)}')
        elif k.startswith(('forged_accepted', 'accepted', 'honest_summary', 'found_attempts')):
            print(f'  {k}: 원 {json.dumps(va, ensure_ascii=False, default=str)[:80]} → 새 {json.dumps(vb, ensure_ascii=False, default=str)[:80]}')
