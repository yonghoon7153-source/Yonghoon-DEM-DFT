"""Compare our actual registration receipt with Codex's (S06 noimpact / scope raw).

usage: python3 -I cmp_receipt.py <ours.json> <codex_receipt.json> [<codex_receipt2.json> ...]
Compares rc, failing check ids, per-check ok flags and registration values.
"""
import json
import sys


def summ(rec):
    return dict(rc=rec.get('rc'),
                bad=[c['id'] for c in rec.get('checks', []) if not c.get('ok')],
                checks={c['id']: bool(c.get('ok')) for c in rec.get('checks', [])},
                values=rec.get('registration', {}).get('values'))


def main():
    ours = summ(json.load(open(sys.argv[1], encoding='utf-8')))
    print('ours rc', ours['rc'], 'bad', ours['bad'], 'n_checks', len(ours['checks']))
    print('ours values', json.dumps(ours['values'], ensure_ascii=False)[:600])
    for p in sys.argv[2:]:
        c = summ(json.load(open(p, encoding='utf-8')))
        print('---', p.split('/')[-2] + '/' + p.split('/')[-1])
        print(' rc same', ours['rc'] == c['rc'], '| bad same', ours['bad'] == c['bad'], c['bad'],
              '| checks same', ours['checks'] == c['checks'], '| values same', ours['values'] == c['values'])
        if ours['values'] != c['values']:
            for k in sorted(set(ours['values'] or {}) | set(c['values'] or {})):
                a, b = (ours['values'] or {}).get(k), (c['values'] or {}).get(k)
                if a != b:
                    print('   diff', k, repr(a)[:120], '|', repr(b)[:120])


if __name__ == '__main__':
    main()
