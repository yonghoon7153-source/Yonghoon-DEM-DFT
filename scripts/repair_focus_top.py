#!/usr/bin/env python3
"""`SELF-45` — 이미 만들어진 payload 의 `focus_top` 을 **재실행 없이** 고친다.

## 무엇이 틀렸나 (2026-09-22, 리뷰어 A-2 가 촉발)

`mpm_webapp_payload` 는 `field_scale_{e,ion}.focus_top` 을 이렇게 만들었다:

    focus_top = np.percentile(점군, 99.8) / (σ_eff·ΔV/L)

그런데 그 **점군**은 `step3_sigma.field_point_cloud` 의 렌더링용 부분추출이고,
상위 `hot_budget_frac`(0.35)×`max_points` 셀을 **전수 보존**한다.  그래서 백분위가
장(field)의 99.8 % 가 아니라 **위에서 `0.002·max_points` 번째 셀**을 집는다 ⇒ 보고값이
`--field-max-points`(그림 예산)의 함수였다.  실측 (AM 협착 픽스처, N=157,889):

    max_points   5,000 → ×201.2 │ 40,000 → ×118.6 │ 90,000 → ×71.6 │ 전수 → ×52.9

⚠ 편향 크기는 **꼬리 모양에 걸린다** — 같은 격자라도 탄소 도선이 있는 침대는 상위가
고원이라 1.00× 였다.  ⇒ **침대 간·채널 간 비에서 상쇄되지 않는다.**

## 왜 재실행이 필요 없나

상위 `0.35·max_points` 가 **전수 보존**되므로 점군은 장의 상위 꼬리를 **그대로** 들고 있다.
장의 참 p99.8 은 위에서 `ceil/round(0.002·N)` 번째 값이므로

    0.002·N ≤ 0.35·len(점군)      (= max_points, 부분추출된 경우)

이면 저장된 점군만으로 **정확히** 복원된다.  픽스처 검증: 복원 52.89 vs 전수 참값 52.87
(오차 +0.037 %, payload 의 4자리 반올림 포함).  조건을 못 넘으면 **거부**한다 (fail-closed) —
근사로 채우지 않는다.

    N (도체 복셀 수) = 전자 `step3.n_dof` · 이온 `step3.ion_n_dof`
    ⚠ `ion_n_dof` 는 SELF-45 에서 신설됐다.  그 이전 payload 는 이온 N 을 모르므로
      이온 채널을 **거부**한다 (전자 채널은 고쳐진다).

## 쓰는 법

    python3 scripts/repair_focus_top.py <payload.json> [...]           # 보고만
    python3 scripts/repair_focus_top.py <payload.json> --write         # 제자리 수정
    python3 scripts/repair_focus_top.py <dir> --glob 'mpm_payload*.json' --csv out.csv
    python3 scripts/repair_focus_top.py --selftest

`--write` 는 `field_scale_*` 에 `focus_top_repaired` · `focus_over_local_mean` ·
`percentile_basis` 등을 **추가**하고 원래 `focus_top` 은 `focus_top_as_published` 로
보존한다 (⛔ 원자료를 덮지 않는다 — 이 리포의 규약).
"""
import argparse
import csv as _csv
import glob as _glob
import json
import math
import os
import sys

HOT_BUDGET_FRAC = 0.35                      # step3_sigma.field_point_cloud 의 기본값
_CH = (('e', 'field_scale_e', 'elec_field', 'n_dof'),
       ('ion', 'field_scale_ion', 'ion_field', 'ion_n_dof'))


def _rank_for(n_total):
    """장의 p99.8 이 내림차순에서 몇 번째인가 — `np.percentile(linear)` 규약과 같게.

    numpy 는 오름차순 위치 `q·(n−1)` 에서 선형보간한다.  내림차순 rank(1-기반)로 옮기면
    `n − q·(n−1)` 이고, 우리는 **보수적으로** 그 위를 덮는 정수 rank 를 쓴다
    (보간 두 점 중 위쪽)."""
    if n_total <= 1:
        return 1
    pos = 0.998 * (n_total - 1)             # 오름차순 실수 위치
    lo = math.floor(pos)
    return max(1, n_total - (lo + 1) + 1)   # 위쪽 이웃의 내림차순 rank


def _p998_from_cloud(vals_desc, n_total):
    """정확한 선형보간 재현 — 두 이웃을 모두 갖고 있을 때만."""
    pos = 0.998 * (n_total - 1)
    lo, frac = math.floor(pos), pos - math.floor(pos)
    r_lo = n_total - lo                     # 오름차순 index lo 의 내림차순 rank (1-기반)
    r_hi = max(1, r_lo - 1)                 # index lo+1
    if r_lo > len(vals_desc):
        return None
    v_lo = vals_desc[r_lo - 1]
    v_hi = vals_desc[r_hi - 1]
    return v_lo + (v_hi - v_lo) * frac


def repair_channel(step3, fs_key, field_key, ndof_key):
    """한 채널을 고친다 → dict(ok, reason, …).  payload 는 **바꾸지 않는다**."""
    fs = step3.get(fs_key)
    field = step3.get(field_key)
    out = {'channel': fs_key, 'ok': False, 'reason': None}
    if not fs:
        out['reason'] = f'{fs_key} 없음'
        return out
    if fs.get('percentile_basis') == 'full_field':
        out['reason'] = '이미 전수 기준 (SELF-45 이후 payload) — 할 일 없음'
        out['focus_top_as_published'] = fs.get('focus_top')
        out['focus_top_repaired'] = fs.get('focus_top')
        out['ok'] = True
        out['noop'] = True
        return out
    if not field:
        out['reason'] = f'{field_key} 점군이 payload 에 없다 (--no-field 런?)'
        return out
    n_total = step3.get(ndof_key)
    if not n_total:
        out['reason'] = (f'`{ndof_key}` 가 없다 — 도체 복셀 수 N 을 모르면 참 백분위의 '
                         f'rank 를 정할 수 없다 (SELF-45 이전 payload 의 이온 채널)')
        return out
    n_total = int(n_total)
    j_top = fs.get('j_top_A_cm2_per_V')     # = 점군 p99.8 (A/cm²) — 저장된 정규화의 분모
    j_app = fs.get('j_mean_z_A_cm2_per_V')
    if not j_top or not j_app:
        out['reason'] = 'j_top / j_mean_z 가 없다'
        return out

    vals = sorted((float(p[3]) for p in field), reverse=True)   # 정규화 값 (0..1 부근)
    n_cloud = len(vals)
    subsampled = n_cloud < n_total
    hot_kept = int(n_cloud * HOT_BUDGET_FRAC) if subsampled else n_cloud
    need = _rank_for(n_total)
    if need > hot_kept:
        out['reason'] = (f'복원 불가 — 참 p99.8 은 상위 {need:,} 번째인데 점군이 보존한 상위는 '
                         f'{hot_kept:,} 개뿐이다 (N {n_total:,} · 점군 {n_cloud:,}).  재실행 필요')
        out.update(n_total=n_total, n_cloud=n_cloud, rank_needed=need, hot_kept=hot_kept)
        return out

    p998_norm = _p998_from_cloud(vals, n_total)
    if p998_norm is None:
        out['reason'] = '보간 이웃이 점군 밖이다 — 거부'
        return out
    p998_A = p998_norm * float(j_top)                   # 정규화 → A/cm² (저장 분모를 되곱한다)
    focus_rep = p998_A / float(j_app)
    focus_pub = float(fs.get('focus_top') or 0.0)
    out.update(ok=True, noop=False, n_total=n_total, n_cloud=n_cloud,
               subsampled=subsampled, rank_needed=need, hot_kept=hot_kept,
               j_app_A_cm2_per_V=float(j_app),
               j_top_as_published_A_cm2_per_V=float(j_top),
               j_top_repaired_A_cm2_per_V=p998_A,
               focus_top_as_published=focus_pub,
               focus_top_repaired=focus_rep,
               overstatement=(focus_pub / focus_rep) if focus_rep else None)
    #  ⟨|J|⟩ 는 상위 hot 전수 + 균일 배경의 가중평균으로 복원된다 (배경이 균일추출이므로
    #  그 평균이 나머지 모집단의 불편추정).  ⚠ 점군이 전수면 그냥 평균이다.
    if subsampled and n_cloud > hot_kept:
        bg = vals[hot_kept:]
        mean_norm = (sum(vals[:hot_kept]) + (sum(bg) / len(bg)) * (n_total - hot_kept)) / n_total
    else:
        mean_norm = sum(vals) / len(vals)
    mean_A = mean_norm * float(j_top)
    out['j_mean_local_A_cm2_per_V'] = mean_A
    out['local_mean_over_j_app'] = mean_A / float(j_app)
    out['focus_over_local_mean'] = p998_A / mean_A if mean_A else None
    out['markov_ok'] = bool(out['focus_over_local_mean'] is not None
                            and out['focus_over_local_mean'] <= 500.0 + 1e-9)
    return out


def apply_to_payload(payload, results):
    """`--write` — 원값을 보존한 채 고친 값을 **추가**한다."""
    step3 = payload.get('step3') or {}
    for r in results:
        if not r.get('ok') or r.get('noop'):
            continue
        fs = step3.get(r['channel'])
        if not fs:
            continue
        fs['focus_top_as_published'] = fs.get('focus_top')
        fs['focus_top'] = float(f"{r['focus_top_repaired']:.4g}")
        fs['j_top_A_cm2_per_V'] = float(f"{r['j_top_repaired_A_cm2_per_V']:.4g}")
        fs['j_mean_local_A_cm2_per_V'] = float(f"{r['j_mean_local_A_cm2_per_V']:.4g}")
        fs['focus_over_local_mean'] = float(f"{r['focus_over_local_mean']:.4g}")
        fs['local_mean_over_j_app'] = float(f"{r['local_mean_over_j_app']:.4g}")
        fs['n_conducting_voxels'] = int(r['n_total'])
        fs['percentile_basis'] = 'full_field_repaired'
        fs['repair'] = ('SELF-45 (2026-09-22): focus_top 을 렌더 점군 백분위에서 **장 전수** '
                        'p99.8 로 복원했다.  원값은 focus_top_as_published 에 보존.  '
                        f"과대 배율 {r['overstatement']:.3f}×.  "
                        '⚠ 점군의 정규화 값(4번째 성분)은 **옛 분모**로 나눈 그대로다 — '
                        'j_top_A_cm2_per_V 로 곱해 읽지 말고 j_top_as_published 를 쓸 것.')
        fs['j_top_as_published_A_cm2_per_V'] = float(f"{r['j_top_as_published_A_cm2_per_V']:.4g}")
    return payload


def run(paths, write=False, csv_out=None):
    rows, bad = [], 0
    for p in paths:
        try:
            with open(p, encoding='utf-8') as fh:
                payload = json.load(fh)
        except Exception as e:                                   # noqa: BLE001
            print(f'⛔ {p}: 읽기 실패 — {e}')
            bad += 1
            continue
        #  전체 payload 든 잘라낸 step3 블록이든 받는다 (리포의 `step3_*.json` 은 후자다).
        step3 = payload.get('step3') if isinstance(payload.get('step3'), dict) else None
        if step3 is None:
            step3 = payload if ('field_scale_e' in payload or 'field_scale_ion' in payload) else {}
        res = [repair_channel(step3, fsk, fk, nk) for _, fsk, fk, nk in _CH]
        print(f'\n── {p}')
        for r in res:
            if not r['ok']:
                print(f"   {r['channel']:<16} ⛔ {r['reason']}")
                continue
            if r.get('noop'):
                print(f"   {r['channel']:<16} ✅ {r['reason']}")
                continue
            print(f"   {r['channel']:<16} focus_top {r['focus_top_as_published']:>10.4g}"
                  f"  →  {r['focus_top_repaired']:>10.4g}   "
                  f"({r['overstatement']:.2f}× 과대)")
            print(f"   {'':<16} N {r['n_total']:,} · 점군 {r['n_cloud']:,} · "
                  f"참 rank {r['rank_needed']:,} ≤ 보존 {r['hot_kept']:,}")
            print(f"   {'':<16} ⟨|J|⟩/J_app {r['local_mean_over_j_app']:.3f} · "
                  f"p99.8/⟨|J|⟩ {r['focus_over_local_mean']:.1f} "
                  f"(Markov 500 {'통과' if r['markov_ok'] else '★위반 — 버그'})")
            rows.append({'payload': p, **{k: v for k, v in r.items() if k != 'reason'}})
        if write and any(x.get('ok') and not x.get('noop') for x in res):
            apply_to_payload(payload, res)
            with open(p, 'w', encoding='utf-8') as fh:
                json.dump(payload, fh, ensure_ascii=False)
            print(f'   ✍ 기록함 (원값은 focus_top_as_published 에 보존)')
    if csv_out and rows:
        keys = sorted({k for r in rows for k in r})
        with open(csv_out, 'w', newline='', encoding='utf-8') as fh:
            w = _csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        print(f'\nCSV → {csv_out}  ({len(rows)} 행)')
    return 1 if bad else 0


def _selftest():
    """합성 payload 로 복원이 참값을 되돌리는지 — 그리고 **거부**가 작동하는지."""
    ok = True
    n_total, n_cloud = 50_000, 4_000
    hot = int(n_cloud * HOT_BUDGET_FRAC)                 # 1,400
    # 멱법칙 꼬리 J(rank) = rank^-0.5 (실측 픽스처와 같은 모양)
    full = [float((r + 1) ** -0.5) for r in range(n_total)]
    need = _rank_for(n_total)
    truth = _p998_from_cloud(full, n_total)
    # 점군: 상위 hot 전수 + 나머지 균일추출 (결정적으로 매 k 번째)
    rest = full[hot:]
    step = max(1, len(rest) // (n_cloud - hot))
    cloud = full[:hot] + rest[::step][:n_cloud - hot]
    j_top_pub = max(cloud)                               # 임의 스케일 — 정규화 분모 역할
    fld = [[0.0, 0.0, 0.0, v / j_top_pub] for v in cloud]
    # 옛 규약이 내던 값 = 점군의 p99.8
    cl = sorted((p[3] for p in fld), reverse=True)
    pos = 0.998 * (len(cl) - 1)
    lo, fr = math.floor(pos), pos - math.floor(pos)
    r_lo = len(cl) - lo
    naive = (cl[r_lo - 1] + (cl[max(1, r_lo - 1) - 1] - cl[r_lo - 1]) * fr) * j_top_pub

    step3 = {'n_dof': n_total,
             'field_scale_e': {'j_top_A_cm2_per_V': naive, 'j_mean_z_A_cm2_per_V': 1.0,
                               'focus_top': naive},
             'elec_field': [[0.0, 0.0, 0.0, v / naive] for v in cloud]}
    r = repair_channel(step3, 'field_scale_e', 'elec_field', 'n_dof')
    e1 = r['ok'] and abs(r['focus_top_repaired'] - truth) <= 1e-9 * max(truth, 1e-30)
    ok &= e1
    print(f"repair-exact: 복원 {r.get('focus_top_repaired', float('nan')):.8g} vs "
          f"참값 {truth:.8g}  (rank {need:,} ≤ 보존 {hot:,})  {'OK' if e1 else 'FAIL'}")
    e2 = r['ok'] and r['overstatement'] > 1.05
    ok &= e2
    print(f"repair-nonvacuous: 옛 규약이 실제로 과대하다 ({r.get('overstatement', 0):.3f}×)  "
          f"{'OK' if e2 else 'FAIL'}")
    # ⟨|J|⟩ 복원
    truth_mean = sum(full) / n_total
    e2b = r['ok'] and abs(r['j_mean_local_A_cm2_per_V'] - truth_mean) <= 0.02 * truth_mean
    ok &= e2b
    print(f"repair-mean: ⟨|J|⟩ 복원 {r.get('j_mean_local_A_cm2_per_V', 0):.6g} vs "
          f"{truth_mean:.6g} (≤2 %)  {'OK' if e2b else 'FAIL'}")
    # 거부 ①: 예산이 너무 작아 참 rank 가 보존 밖
    small = {'n_dof': 5_000_000,
             'field_scale_e': step3['field_scale_e'], 'elec_field': step3['elec_field']}
    r2 = repair_channel(small, 'field_scale_e', 'elec_field', 'n_dof')
    e3 = (not r2['ok']) and '복원 불가' in (r2['reason'] or '')
    ok &= e3
    print(f"refuse-budget: 보존 꼬리를 넘는 rank 는 **거부**한다  {'OK' if e3 else 'FAIL'}")
    # 거부 ②: 이온 N 없음 (SELF-45 이전 payload)
    r3 = repair_channel({'field_scale_ion': {'j_top_A_cm2_per_V': 1.0,
                                             'j_mean_z_A_cm2_per_V': 1.0, 'focus_top': 1.0},
                         'ion_field': [[0, 0, 0, 1.0]]},
                        'field_scale_ion', 'ion_field', 'ion_n_dof')
    e4 = (not r3['ok']) and 'ion_n_dof' in (r3['reason'] or '')
    ok &= e4
    print(f"refuse-no-N: 이온 N 이 없으면 **거부**한다 (근사 금지)  {'OK' if e4 else 'FAIL'}")
    # 이미 고쳐진 payload 는 no-op
    r4 = repair_channel({'n_dof': 10, 'field_scale_e': {'percentile_basis': 'full_field',
                                                        'focus_top': 7.0}, 'elec_field': []},
                        'field_scale_e', 'elec_field', 'n_dof')
    e5 = r4['ok'] and r4.get('noop')
    ok &= e5
    print(f"noop-new-payload: 전수 기준 payload 는 건드리지 않는다  {'OK' if e5 else 'FAIL'}")
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='SELF-45 — payload 의 focus_top 을 장 전수 기준으로 복원')
    ap.add_argument('paths', nargs='*', help='payload JSON 또는 디렉터리')
    ap.add_argument('--glob', default='mpm_payload*.json', help='디렉터리에 쓸 glob')
    ap.add_argument('--write', action='store_true', help='제자리 수정 (원값 보존)')
    ap.add_argument('--csv', help='결과 CSV')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    files = []
    for p in a.paths:
        if os.path.isdir(p):
            files += sorted(_glob.glob(os.path.join(p, '**', a.glob), recursive=True))
        else:
            files.append(p)
    if not files:
        ap.error('payload 를 못 찾았다')
    return run(files, write=a.write, csv_out=a.csv)


if __name__ == '__main__':
    sys.exit(main())
