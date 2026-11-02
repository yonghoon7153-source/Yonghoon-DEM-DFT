#!/usr/bin/env python3
"""원장 항목 보기 (읽기 전용) — 사전 공격 7 회차.

사용: python3 show_ledger.py <findings.json> ID [ID ...]
"""
import json
import sys


def main():
    path = sys.argv[1]
    want = set(sys.argv[2:])
    d = json.load(open(path, encoding='utf-8'))
    items = d if isinstance(d, list) else d.get('findings', d.get('items', []))
    for f in items:
        if f.get('id') in want:
            print('=====', f['id'], f.get('severity'), f.get('status'))
            for k, v in f.items():
                if k == 'id':
                    continue
                s = json.dumps(v, ensure_ascii=False)
                if len(s) > 2500:
                    s = s[:2500] + '…'
                print(f'  {k}: {s}')


if __name__ == '__main__':
    main()
