#!/usr/bin/env python3
"""사전등록 v2 판정기 — `docs/reviews/sdcp_gain_prereg_v2_20260816.md` §5 순서를 **코드로** 박는다.

★ 왜 별도 스크립트인가: 판정선을 사람이 눈으로 보고 적용하면 결과를 본 뒤 창이 움직인다
  (Codex CDX-13 이 지적한 실사고).  판정 순서·문턱을 **런 전에 코드로 고정**해 두면
  결과가 무엇이든 같은 함수가 같은 답을 낸다.

★ 판정 순서 (prereg §5, 여기서 바꾸면 사전등록 위반):
  1. 미수렴 팔(cg_info ≠ 0)이 하나라도 → **판정 보류**
  2. 8 팔 표준오차 > 1.17 %p       → **판정 보류**, origin 16 으로
  3. 비 ≥ 1.05                      → h0 채택
  4. 비 ≤ 1.025                     → h1 채택 ⇒ SDCP 전자 이득 원고에서 철회
  5. 그 사이                        → 둘 다 기각, 제3 기전

사용:
  python3 scripts/sdcp_gain_verdict.py --dir prereg_v2_vox015
  python3 scripts/sdcp_gain_verdict.py --dir ... --collect-only   # 수집만, 판정 안 함
  python3 scripts/sdcp_gain_verdict.py --selftest
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys

# ── prereg §3/§4 에서 **런 전에** 고정된 상수.  바꾸면 사전등록이 무효다 ─────────────
H0_MIN_RATIO = 1.05          # h0 (이득은 물리)
H1_RATIO = 1.015             # h1 (SDCP 부피 인공물)
UNDECIDED_LO, UNDECIDED_HI = 1.025, 1.05
SE_MAX_PCT = 1.17            # 이보다 크면 판정 보류하고 origin 을 늘린다
PREREG = 'docs/reviews/sdcp_gain_prereg_v2_20260816.md'


def _read(path):
    d = json.load(open(path, encoding='utf-8'))
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
    man = s.get('manifest') or {}
    return {'file': os.path.basename(path),
            'sigma_e': s.get('sigma_e_eff_S_cm'),
            'sigma_ion': s.get('sigma_ion_eff_S_cm'),
            'n_dof': s.get('n_dof'),
            'cg_info': s.get('cg_info', (s.get('solve') or {}).get('cg_info')),
            'origin_shift_um': man.get('origin_shift_um'),
            'vox': man.get('vox_um') or s.get('vox_um'),
            'bridge_um': man.get('bridge_um'),
            'fibre_stamp': man.get('fibre_stamp')}


def collect(d):
    rows = [_read(p) for p in sorted(glob.glob(os.path.join(d, 'p2_*.json')))]
    arms = {'SBE': [r for r in rows if '_SBE_' in r['file']],
            'DBE': [r for r in rows if '_DBE_' in r['file']]}
    return rows, arms


def _stats(vals):
    n = len(vals)
    if n == 0:
        return None
    m = sum(vals) / n
    if n == 1:
        return {'n': 1, 'mean': m, 'sd': None, 'se': None}
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1))
    return {'n': n, 'mean': m, 'sd': sd, 'se': sd / math.sqrt(n)}


def verdict(arms):
    """prereg §5 판정.  **순서를 바꾸지 말 것.**"""
    out = {'prereg': PREREG, 'thresholds': {
        'h0_min_ratio': H0_MIN_RATIO, 'h1_ratio': H1_RATIO,
        'undecided': [UNDECIDED_LO, UNDECIDED_HI], 'se_max_pct': SE_MAX_PCT}}
    # ① 미수렴 — 하나라도 있으면 보류
    unconv = [r['file'] for k in arms for r in arms[k]
              if r['cg_info'] not in (0, None)]
    if unconv:
        return dict(out, decision='HOLD',
                    reason=f'미수렴 팔 {len(unconv)}개 — prereg §5-1 (판정 보류)',
                    unconverged=unconv)
    st = {k: _stats([r['sigma_e'] for r in arms[k] if r['sigma_e']]) for k in ('SBE', 'DBE')}
    out['arms'] = st
    if not st['SBE'] or not st['DBE'] or st['SBE']['n'] != st['DBE']['n']:
        return dict(out, decision='HOLD',
                    reason=f'팔 수 불일치/부족 (SBE {st["SBE"] and st["SBE"]["n"]} · '
                           f'DBE {st["DBE"] and st["DBE"]["n"]}) — 판정 불가')
    ratio = st['DBE']['mean'] / st['SBE']['mean']
    out['ratio'] = round(ratio, 6)
    # ② 표준오차 게이트
    if st['SBE']['se'] is None:
        return dict(out, decision='HOLD', reason='팔이 1 개 — 표준오차를 못 낸다')
    se_ratio_pct = 100.0 * math.hypot(st['SBE']['se'] / st['SBE']['mean'],
                                      st['DBE']['se'] / st['DBE']['mean'])
    out['se_ratio_pct'] = round(se_ratio_pct, 4)
    if se_ratio_pct > SE_MAX_PCT:
        return dict(out, decision='HOLD',
                    reason=f'비의 표준오차 {se_ratio_pct:.2f} %p > {SE_MAX_PCT} — '
                           f'prereg §5-2 (origin 16 으로 늘릴 것)')
    # ③④⑤ 본 판정
    if ratio >= H0_MIN_RATIO:
        return dict(out, decision='h0', reason=f'비 {ratio:.4f} ≥ {H0_MIN_RATIO} — 이득은 물리')
    if ratio <= UNDECIDED_LO:
        return dict(out, decision='h1',
                    reason=f'비 {ratio:.4f} ≤ {UNDECIDED_LO} — SDCP 부피 인공물.  '
                           f'⇒ **원고에서 SDCP 전자 이득 철회**')
    return dict(out, decision='BOTH_REJECTED',
                reason=f'비 {ratio:.4f} 가 중간대 ({UNDECIDED_LO}, {UNDECIDED_HI}) — '
                       f'둘 다 기각, 제3 기전 조사 (prereg §5-5)')


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    def mk(sbe, dbe, cg=0):
        return {'SBE': [{'file': f'p2_SBE_a{i}.json', 'sigma_e': v, 'cg_info': cg}
                        for i, v in enumerate(sbe)],
                'DBE': [{'file': f'p2_DBE_a{i}.json', 'sigma_e': v, 'cg_info': cg}
                        for i, v in enumerate(dbe)]}

    base = [1.0000, 1.0020, 0.9980, 1.0010, 0.9990, 1.0005, 0.9995, 1.0000]
    chk('① 미수렴이 하나라도 있으면 HOLD (숫자를 내지 않는다)',
        verdict(mk(base, base, cg=1))['decision'] == 'HOLD')
    chk('② 비 1.08 → h0', verdict(mk(base, [v * 1.08 for v in base]))['decision'] == 'h0')
    v1 = verdict(mk(base, [v * 1.015 for v in base]))
    chk(f'③ 비 1.015 → h1 ({v1["ratio"]})', v1['decision'] == 'h1')
    chk('④ 비 1.035 (중간대) → 둘 다 기각',
        verdict(mk(base, [v * 1.035 for v in base]))['decision'] == 'BOTH_REJECTED')
    noisy = [1.0, 1.10, 0.90, 1.08, 0.92, 1.06, 0.94, 1.0]      # SE 큼
    chk('⑤ 표준오차가 크면 판정 보류 (origin 을 늘리라고 말한다)',
        verdict(mk(noisy, [v * 1.08 for v in noisy]))['decision'] == 'HOLD')
    chk('⑥ 팔 수가 다르면 HOLD',
        verdict(mk(base, base[:4]))['decision'] == 'HOLD')
    chk('⑦ 문턱이 prereg 값과 같다 (코드가 사전등록이다)',
        (H0_MIN_RATIO, H1_RATIO, SE_MAX_PCT) == (1.05, 1.015, 1.17))
    print(f'\nsdcp_gain_verdict selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='')
    ap.add_argument('--collect-only', action='store_true')
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dir:
        raise SystemExit('사용: --dir <결과 디렉터리>')
    rows, arms = collect(a.dir)
    print(f'{"파일":<28} {"σ_e":>12} {"σ_ion":>12} {"dof":>12} {"origin shift":>22} {"cg":>4}')
    for r in rows:
        print(f'{r["file"]:<28} {str(r["sigma_e"]):>12} {str(r["sigma_ion"]):>12} '
              f'{str(r["n_dof"]):>12} {str(r["origin_shift_um"]):>22} {str(r["cg_info"]):>4}')
    print(f'\n  수집: SBE {len(arms["SBE"])} 팔 · DBE {len(arms["DBE"])} 팔')
    if a.collect_only:
        print('  (--collect-only — 판정하지 않는다)')
        raise SystemExit(0)
    v = verdict(arms)
    print(f'\n══ 판정 (prereg §5) ══\n  결정: **{v["decision"]}**\n  근거: {v["reason"]}')
    if 'ratio' in v:
        print(f'  σ_e 비 = {v["ratio"]}   (h0 ≥ {H0_MIN_RATIO} · h1 = {H1_RATIO})')
    if 'se_ratio_pct' in v:
        print(f'  비의 표준오차 = {v["se_ratio_pct"]} %p (문턱 {SE_MAX_PCT})')
    if a.out:
        json.dump({'rows': rows, 'verdict': v}, open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')
    raise SystemExit(0 if v['decision'] in ('h0', 'h1') else 1)
