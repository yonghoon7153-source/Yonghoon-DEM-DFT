#!/usr/bin/env python3
"""phase_a_pair_e_arms.py — Phase A 재현 런의 **짝 비교** 판정기.

같은 (vgcf_wt, vox, origin) 팔을 두 산출물 집합 A · B (예: VGCF E 100 GPa ↔ 같은 기계의 10 GPa 대조군,
또는 10 GPa 대조군 ↔ 09-21 원판) 에서 짝지어 d = ln(σ_A/σ_B) 를 낸다.

사전등록: docs/reviews/phase_a_replication_vgcf100_prereg_20260926.md §4.
· **순서 판정 (ORDER-ROBUST) 은 이 스크립트가 하지 않는다** — scripts/phase_a_order_verdict.py 가 세대마다 따로 돈다.
· 여기서는 등록한 띠 하나로 h0 (max |d| ≤ 띠) 대 h1 (띠 초과) 만 가른다.  띠는 런 전에 등록한다 — 결과를 보고 넓히지 않는다.
· 짝이 하나라도 빠지면 HOLD — 있는 것만으로 판정하지 않는다.  --expect-pairs 로 짝 개수도 고정한다.
· 팔 JSON 은 phase_a_arms_from_payload.py 산출이고 phase_a_order_verdict.load_arms 로 읽는다 (같은 검증 · 거부 규칙).
· role 은 primary 만 짝짓는다 (qc_replay 는 exact replay 게이트의 몫).

사용:
  python3 scripts/phase_a_pair_e_arms.py --a arms_v015_E100 --b arms_v015_E010 --label-a E100 --label-b E010 \
      --band-pct 1.0 --expect-pairs 32 --out pair_E100_vs_E010.json
  python3 scripts/phase_a_pair_e_arms.py --selftest
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VERDICTS = ('h0_secondary_input', 'h1_e_matters', 'HOLD')


def key(a):
    return (round(float(a['vgcf_wt']), 6), round(float(a['vox']), 6), int(a['origin']))


def pair_arms(arms_a, arms_b, band_pct, expect_pairs=None, label_a='A', label_b='B'):
    """순수 함수 — 팔 dict 목록 둘 → 판정 dict.  파일을 읽지 않는다."""
    band = math.log1p(float(band_pct) / 100.0)
    ia = {key(a): a for a in arms_a if a.get('role') == 'primary'}
    ib = {key(a): a for a in arms_b if a.get('role') == 'primary'}
    if len(ia) != sum(1 for a in arms_a if a.get('role') == 'primary'):
        raise SystemExit(f'⛔ {label_a}: 같은 (wt, vox, origin) 키가 둘 이상 — 짝을 정할 수 없다')
    if len(ib) != sum(1 for a in arms_b if a.get('role') == 'primary'):
        raise SystemExit(f'⛔ {label_b}: 같은 (wt, vox, origin) 키가 둘 이상 — 짝을 정할 수 없다')
    common = sorted(set(ia) & set(ib))
    only_a = sorted(set(ia) - set(ib)); only_b = sorted(set(ib) - set(ia))
    rows = []
    for k in common:
        a, b = ia[k], ib[k]
        pa, pb = a.get('ptfe_wt'), b.get('ptfe_wt')
        if pa is not None and pb is not None and abs(float(pa) - float(pb)) > 1e-9:
            raise SystemExit(f'⛔ {k}: ptfe_wt 가 다르다 ({pa} vs {pb}) — 같은 침대 설계가 아니다')
        d = math.log(float(a['sigma_e']) / float(b['sigma_e']))
        rows.append({'vgcf_wt': k[0], 'vox': k[1], 'origin': k[2], 'sigma_a': float(a['sigma_e']),
                     'sigma_b': float(b['sigma_e']), 'd_ln': d, 'd_pct': 100.0 * (math.exp(d) - 1.0),
                     'within': bool(abs(d) <= band + 1e-12),        # 경계 = 띠 위 (부동소수 1e-12 여유)
                     'file_a': a.get('_file'), 'file_b': b.get('_file')})
    hold = []
    if only_a or only_b:
        hold.append(f'짝 없는 팔 — {label_a} 만 {len(only_a)} · {label_b} 만 {len(only_b)}')
    if expect_pairs is not None and len(common) != int(expect_pairs):
        hold.append(f'짝 {len(common)} ≠ 등록 {expect_pairs}')
    if not common:
        hold.append('짝이 없다')
    per_wt = {}
    for r in rows:
        g = per_wt.setdefault(str(r['vgcf_wt']), {'n': 0, 'max_abs_d_ln': 0.0, 'sum_d_ln': 0.0})
        g['n'] += 1; g['sum_d_ln'] += r['d_ln']; g['max_abs_d_ln'] = max(g['max_abs_d_ln'], abs(r['d_ln']))
    for g in per_wt.values():
        g['mean_d_ln'] = g['sum_d_ln'] / g['n']; del g['sum_d_ln']
    max_abs = max((abs(r['d_ln']) for r in rows), default=None)
    if hold:
        verdict = 'HOLD'
    else:
        verdict = 'h0_secondary_input' if max_abs <= band + 1e-12 else 'h1_e_matters'   # 경계 = 띠 위 (within 과 같은 여유)
    return {
        'schema': 'phase_a_pair_e_v1', 'verdict': verdict, 'hold_reasons': hold,
        'label_a': label_a, 'label_b': label_b, 'band_pct': float(band_pct), 'band_ln': band,
        'n_pairs': len(common), 'expect_pairs': expect_pairs, 'n_only_a': len(only_a), 'n_only_b': len(only_b),
        'max_abs_d_ln': max_abs, 'max_abs_d_pct': (100.0 * (math.exp(max_abs) - 1.0) if max_abs is not None else None),
        'mean_d_ln': (sum(r['d_ln'] for r in rows) / len(rows) if rows else None),
        'n_outside': sum(1 for r in rows if not r['within']),
        'per_wt': per_wt, 'rows': rows,
        'only_a': [list(k) for k in only_a], 'only_b': [list(k) for k in only_b],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--a', help='팔 JSON 디렉터리 A (분자)')
    ap.add_argument('--b', help='팔 JSON 디렉터리 B (분모)')
    ap.add_argument('--label-a', default='A'); ap.add_argument('--label-b', default='B')
    ap.add_argument('--band-pct', type=float, default=1.0, help='h0 띠 (%%, 런 전 등록값)')
    ap.add_argument('--expect-pairs', type=int, default=None, help='등록한 짝 개수 (다르면 HOLD)')
    ap.add_argument('--out', default=None)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.a or not a.b:
        ap.error('--a 와 --b 가 필요하다')
    from phase_a_order_verdict import load_arms
    res = pair_arms(load_arms(a.a), load_arms(a.b), a.band_pct, a.expect_pairs, a.label_a, a.label_b)
    res['inputs'] = {'a': os.path.abspath(a.a), 'b': os.path.abspath(a.b)}
    print(f"══ 짝 비교 {a.label_a} / {a.label_b} — 띠 ±{a.band_pct} % · 짝 {res['n_pairs']}"
          f"{' / 등록 %d' % a.expect_pairs if a.expect_pairs is not None else ''} ══")
    for w, g in sorted(res['per_wt'].items(), key=lambda kv: float(kv[0])):
        print(f"   wt {w:>4}: n {g['n']:2d} · mean d {g['mean_d_ln'] * 100:+.3f} % · max |d| {g['max_abs_d_ln'] * 100:.3f} %")
    if res['max_abs_d_ln'] is not None:
        print(f"   전체: max |d| {res['max_abs_d_pct']:.3f} % · mean {res['mean_d_ln'] * 100:+.3f} % · 띠 밖 {res['n_outside']}")
    print(f"   ⇒ {res['verdict']}" + (f"  ({'; '.join(res['hold_reasons'])})" if res['hold_reasons'] else ''))
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
        print(f'   → {a.out}')
    return 0


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    def mk(w, v, o, s, role='primary', ptfe=1.0):
        return {'role': role, 'vgcf_wt': w, 'ptfe_wt': ptfe, 'vox': v, 'origin': o, 'sigma_e': s, '_file': f'w{w}_v{v}_o{o}'}

    base = [mk(w, 0.15, o, 0.002 * (1 + 3 * (w - 1)) ** 2 * (1 + 0.001 * o)) for w in (1, 2, 3, 4) for o in range(8)]
    # 1 동일 → h0 · max 0 · 짝 32
    r = pair_arms(base, [dict(a) for a in base], 1.0, 32)
    chk('동일 집합 → h0 · max |d| 0 · 짝 32', r['verdict'] == 'h0_secondary_input' and r['max_abs_d_ln'] == 0.0 and r['n_pairs'] == 32)
    chk('per_wt 4 묶음 · n 8', set(r['per_wt']) == {'1.0', '2.0', '3.0', '4.0'} and all(g['n'] == 8 for g in r['per_wt'].values()))
    # 2 +0.5 % 전체 이동 → 띠 1 % 안 h0 · +2 % → h1
    up05 = [dict(a, sigma_e=a['sigma_e'] * 1.005) for a in base]
    up2 = [dict(a, sigma_e=a['sigma_e'] * 1.02) for a in base]
    chk('+0.5 % → h0 (띠 1 %)', pair_arms(up05, base, 1.0, 32)['verdict'] == 'h0_secondary_input')
    r2 = pair_arms(up2, base, 1.0, 32)
    chk('+2 % → h1 · 띠 밖 32 · max_abs_d_pct ≈ 2', r2['verdict'] == 'h1_e_matters' and r2['n_outside'] == 32
        and abs(r2['max_abs_d_pct'] - 2.0) < 1e-9)
    # 3 한 팔만 띠 밖 → h1 (전부가 아니라 하나라도)
    one = [dict(a, sigma_e=a['sigma_e'] * (1.015 if a['origin'] == 3 and a['vgcf_wt'] == 2 else 1.0)) for a in base]
    r3 = pair_arms(one, base, 1.0, 32)
    chk('한 팔 +1.5 % → h1 · 밖 1 · 그 wt 의 max 만 오름', r3['verdict'] == 'h1_e_matters' and r3['n_outside'] == 1
        and r3['per_wt']['2.0']['max_abs_d_ln'] > 0.01 and r3['per_wt']['1.0']['max_abs_d_ln'] == 0.0)
    # 4 짝 빠짐 → HOLD (있는 것만으로 판정하지 않는다)
    r4 = pair_arms(base[:-1], base, 1.0, 32)
    chk('짝 하나 빠짐 → HOLD · n_only_b 1', r4['verdict'] == 'HOLD' and r4['n_only_b'] == 1 and r4['n_pairs'] == 31)
    chk('expect_pairs 불일치 → HOLD', pair_arms(base, base, 1.0, 96)['verdict'] == 'HOLD')
    # 5 qc_replay 는 짝에서 제외
    withqc = base + [mk(1, 0.15, o, 0.002, role='qc_replay') for o in range(8)]
    chk('qc_replay 팔은 짝에 안 들어간다', pair_arms(withqc, base, 1.0, 32)['n_pairs'] == 32)
    # 6 ptfe_wt 다르면 거부 · 중복 키 거부
    try:
        pair_arms([dict(base[0], ptfe_wt=0.5)], [base[0]], 1.0); chk('ptfe_wt 불일치 → 거부', False)
    except SystemExit:
        chk('ptfe_wt 불일치 → 거부', True)
    try:
        pair_arms(base + [dict(base[0])], base, 1.0); chk('중복 키 → 거부', False)
    except SystemExit:
        chk('중복 키 → 거부', True)
    # 7 띠 경계 — 정확히 띠 위는 안 (|d| ≤ band)
    edge = [dict(a, sigma_e=a['sigma_e'] * 1.01) for a in base]
    chk('정확히 +1.0 % 는 띠 안 (≤)', pair_arms(edge, base, 1.0, 32)['verdict'] == 'h0_secondary_input')
    # 8 방향 — A/B 를 바꾸면 d 부호가 바뀐다
    chk('A/B 교환 → d 부호 반전', pair_arms(base, up2, 1.0, 32)['mean_d_ln'] < 0 < r2['mean_d_ln'])
    # 9 격자가 다른 집합 (vox 0.20 vs 0.15) 은 짝이 없다 → HOLD
    v20 = [dict(a, vox=0.20) for a in base]
    chk('vox 가 다른 집합 → HOLD (짝 0)', pair_arms(v20, base, 1.0)['verdict'] == 'HOLD')
    chk('판정 어휘', all(x['verdict'] in VERDICTS for x in (r, r2, r3, r4)))
    print(f"selftest: {ok}/{ok + len(fail)} PASS" + (f"   FAILED: {fail}" if fail else ''))
    return 0 if not fail else 1


if __name__ == '__main__':
    sys.exit(main())
