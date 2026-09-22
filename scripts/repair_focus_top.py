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

    python3 scripts/repair_focus_top.py PAYLOAD.json [PAYLOAD2.json ...]   # 보고만
    python3 scripts/repair_focus_top.py PAYLOAD.json --write               # 제자리 수정
    python3 scripts/repair_focus_top.py DIR --csv out.csv                  # 트리 전체
    python3 scripts/repair_focus_top.py --selftest

⚠ 웹앱이 쓰는 파일 이름은 `payload.json`(`webapp/mpm_lab/<case>/payload.json`) 이고
  킷 러너가 내는 것은 `mpm_payload.json` 이다 — 기본 glob 이 **둘 다** 잡는다.

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
#  ★★ 2026-09-22 — **실제 직렬화 키를 쓴다.**  초판은 생산자의 *지역 변수* 이름
#    (`elec_field`·`ion_field`)을 적었고 그 둘은 payload 에 **없다**.  실물 키는
#    `mpm_webapp_payload.py:3189-3190` 의 `electronic_field`·`ionic_field` 이고,
#    `step3` 안이 아니라 **payload 최상위**에 있다 (`field_scale_*` 만 step3 안).
#    그대로 뒀으면 모든 실제 payload 에서 "점군 없음" 으로 **거짓 거부**했다 —
#    fail-closed 라 틀린 숫자는 안 나오지만 도구가 무용지물이 된다.
#    ⇒ 아래 `_selftest_keys()` 가 생산자 소스를 AST 로 읽어 이 이름들을 **대조**한다.
_CH = (('e', 'field_scale_e', 'electronic_field', 'n_dof'),
       ('ion', 'field_scale_ion', 'ionic_field', 'ion_n_dof'))


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


_WANT = ('field_scale_e', 'field_scale_ion', 'electronic_field', 'ionic_field',
         'n_dof', 'ion_n_dof',
         #  ★ 케이스 동정용 (어느 것이 SBE/DBE 인가) — 값만 읽고 고치지 않는다
         'sigma_e_eff_S_cm', 'sigma_ion_eff_S_cm', 'vox_um', 'thickness_um')


def find_key_paths(obj, keys=_WANT, path='', out=None, _depth=0):
    """JSON 어디에 그 키가 있는지 전수로 찾는다 → {key: [(경로, 부모 dict), …]}.

    ★★ 왜 재귀인가 (2026-09-22, 실물에서 두 번 틀린 뒤) — 초판은 `payload['step3']`
      에서, 2판은 거기 + 최상위에서 찾았다.  둘 다 실물과 달랐다 (`webapp/mpm_lab/
      <case>/payload.json` 은 또 다른 자리에 싣는다).  **소비자가 생산자의 중첩을
      외우면 생산자가 바뀔 때마다 조용히 거짓 거부한다** — 그리고 fail-closed 라
      아무 숫자도 안 나오니 "결함이 없다" 처럼 보인다.
      ⇒ 구조를 **추측하지 않고 찾는다**.  못 찾거나 후보가 둘 이상이면 **거부**하되
        어디에 무엇이 있는지 출력한다 (다음 사람이 한 번에 알 수 있게)."""
    if out is None:
        out = {k: [] for k in keys}
    if _depth > 12:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in out:
                out[k].append((path + '/' + k, obj))
            if isinstance(v, (dict, list)):
                find_key_paths(v, keys, path + '/' + k, out, _depth + 1)
    elif isinstance(obj, list):
        #  거대한 점군 리스트는 원소가 dict 가 아니므로 즉시 빠진다 (비용 0)
        for i, v in enumerate(obj[:4]):
            if isinstance(v, (dict, list)):
                find_key_paths(v, keys, path + f'[{i}]', out, _depth + 1)
    return out


def repair_channel(step3, fs_key, field_key, ndof_key, payload=None):
    """한 채널을 고친다 → dict(ok, reason, …).  payload 는 **바꾸지 않는다**.

    `field_scale_*` 는 `step3` 안에, 점군(`electronic_field`·`ionic_field`)은 payload
    **최상위**에 있다.  `payload` 를 안 주면 `step3` 안에서도 찾아본다 (잘라낸 블록 대응)."""
    fs = step3.get(fs_key)
    field = step3.get(field_key)
    if field is None and payload is not None:
        field = payload.get(field_key)
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
        #  ★★ 점 추정은 못 해도 **엄밀한 상한**은 낸다 (2026-09-22, N=26.4 M 실물에서).
        #    보존된 꼬리는 장의 상위 `hot_kept` 개와 **정확히 같다**.  값이 rank 에 대해
        #    단조 비증가이므로  참 p99.8 (rank need) ≤ 값(rank hot_kept)  이 성립한다.
        #    ⇒ 외삽이 아니라 **부등식**이다.  보고된 값이 그 상한보다 크면 그 차이는
        #      "적어도 이만큼 과대" 라고 말할 수 있다 (그 자체로 인용 가능한 문장).
        #    ⛔ 이 상한을 값으로 쓰지 말 것 — 여전히 상한이다 (rank 가 1.68 배 얕다).
        _b_norm = vals[hot_kept - 1]
        _b_A = _b_norm * float(j_top)
        _b_focus = _b_A / float(j_app)
        _pub = float(fs.get('focus_top') or 0.0)
        out['reason'] = (
            f'복원 불가 — 참 p99.8 은 상위 {need:,} 번째인데 점군이 보존한 상위는 '
            f'{hot_kept:,} 개뿐이다 (N {n_total:,} · 점군 {n_cloud:,}).  재실행 필요.\n'
            f'                    ★ 그래도 **엄밀한 상한**은 나온다 (외삽 아님, 단조성):\n'
            f'                      참 focus_top ≤ {_b_focus:.4g}  '
            f'(= 상위 {hot_kept:,} 번째, 백분위 {100.0 * (1 - hot_kept / n_total):.4f} %)\n'
            f'                      ⇒ 보고값 {_pub:.4g} 는 **최소 {_pub / max(_b_focus, 1e-30):.2f}× 과대**')
        out.update(n_total=n_total, n_cloud=n_cloud, rank_needed=need, hot_kept=hot_kept,
                   focus_top_as_published=_pub, focus_top_upper_bound=_b_focus,
                   overstatement_at_least=_pub / max(_b_focus, 1e-30),
                   j_app_A_cm2_per_V=float(j_app))
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
        #  ★ 구조를 추측하지 않고 **찾는다** (위 find_key_paths 배너).
        found = find_key_paths(payload)
        print(f'\n── {p}')
        _hits = {k: [pp for pp, _ in v] for k, v in found.items() if v}
        if not _hits.get('field_scale_e') and not _hits.get('field_scale_ion'):
            print('   ⛔ field_scale_* 가 이 파일 어디에도 없다 (STEP3 필드 스케일 이전 세대?)')
            print('      찾은 것: ' + (', '.join(f'{k}@{v[0]}' for k, v in _hits.items()) or '없음'))
            continue
        for _k, _v in sorted(_hits.items()):
            _val = found[_k][0][1].get(_k)
            _shown = ('' if isinstance(_val, (dict, list))
                      else f'  = {_val}')
            print(f'   · {_k:<19} {_v[0]}{_shown}'
                  + (f'   (+{len(_v) - 1} 곳 더)' if len(_v) > 1 else ''))
        res = []
        for _, fsk, fk, nk in _CH:
            _fs_hits = found.get(fsk) or []
            if len(_fs_hits) != 1:
                res.append({'channel': fsk, 'ok': False,
                            'reason': (f'{fsk} 후보가 {len(_fs_hits)} 개 — '
                                       + (', '.join(pp for pp, _ in _fs_hits) or '없음')
                                       + '.  하나로 정해지지 않으면 고르지 않는다')})
                continue
            _owner = _fs_hits[0][1]                      # field_scale_* 를 담은 dict = step3 격
            _cloud_hits = found.get(fk) or []
            _cloud_owner = _cloud_hits[0][1] if len(_cloud_hits) == 1 else None
            _shim = dict(_owner)
            if _cloud_owner is not None and fk not in _shim:
                _shim[fk] = _cloud_owner.get(fk)
            #  N(도체 복셀 수)도 같은 규약으로 — 다만 **후보가 하나일 때만** 쓴다.
            #  여럿이면 어느 solve 의 것인지 알 수 없으므로 채우지 않고 거부하게 둔다.
            _nd_hits = found.get(nk) or []
            if nk not in _shim and len(_nd_hits) == 1:
                _shim[nk] = _nd_hits[0][1].get(nk)
            res.append(repair_channel(_shim, fsk, fk, nk, payload=payload))
        for r in res:
            if not r['ok']:
                print(f"   {r['channel']:<16} ⛔ {r['reason']}")
                if 'focus_top_upper_bound' in r:      # 점 추정은 없어도 상한은 남긴다
                    rows.append({'payload': p, **{k: v for k, v in r.items()
                                                  if k != 'reason'}})
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


def _selftest_keys():
    """★ 계약 — 우리가 찾는 키가 **생산자가 실제로 직렬화하는 키**인가 (AST 대조).

    왜: 초판은 `mpm_webapp_payload` 의 *지역 변수* 이름 `elec_field`·`ion_field` 를 적었는데
    실제 직렬화 키는 `electronic_field`·`ionic_field` 다.  합성 payload 만으로 도는 selftest 는
    **내가 지은 이름을 나에게 다시 물어보는 것**이라 이 실수를 영원히 통과시킨다 (규율 ⑤).
    ⇒ 생산자 소스를 파싱해 **payload 조립 dict 의 문자열 키**를 직접 본다."""
    import ast
    ok = True
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mpm_webapp_payload.py')
    tree = ast.parse(open(src_path, encoding='utf-8').read())
    dicts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = {k.value for k in node.keys
                    if isinstance(k, ast.Constant) and isinstance(k.value, str)}
            if keys:
                dicts.append(keys)
    asm = [d for d in dicts if 'electronic_field' in d]
    e0 = bool(asm)
    ok &= e0
    print(f"keys-assembly-found: payload 조립 dict 를 찾았다 (검사가 헛돌지 않는다)  "
          f"{'OK' if e0 else 'FAIL'}")
    if asm:
        a = asm[0]
        for _, _, fk, _ in _CH:
            e = fk in a
            ok &= e
            print(f"keys-cloud `{fk}`: 생산자가 그 이름으로 싣는다  {'OK' if e else 'FAIL'}")
        for stale in ('elec_field', 'ion_field'):
            e = stale not in a
            ok &= e
            print(f"keys-no-stale `{stale}`: 지역 변수 이름을 키로 쓰지 않는다  "
                  f"{'OK' if e else 'FAIL'}")
    #  `field_scale_*` · `n_dof` 는 dict 리터럴의 키가 아니라 `step3['…'] = …` 로 대입된다
    #  ⇒ 모듈의 **모든 문자열 상수**를 본다 (첨자 대입의 문자열도 ast.Constant 다).
    allstr = {n.value for n in ast.walk(tree)
              if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    for _, fsk, _, nk in _CH:
        for name, what in ((fsk, 'field_scale'), (nk, '도체셀 수')):
            e = name in allstr
            ok &= e
            print(f"keys-{what} `{name}`: 생산자에 실재한다  {'OK' if e else 'FAIL'}")
    return ok


def _selftest():
    """합성 payload 로 복원이 참값을 되돌리는지 — 그리고 **거부**가 작동하는지."""
    ok = _selftest_keys()
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
             'electronic_field': [[0.0, 0.0, 0.0, v / naive] for v in cloud]}
    r = repair_channel(step3, 'field_scale_e', 'electronic_field', 'n_dof')
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
             'field_scale_e': step3['field_scale_e'],
             'electronic_field': step3['electronic_field']}
    r2 = repair_channel(small, 'field_scale_e', 'electronic_field', 'n_dof')
    e3 = (not r2['ok']) and '복원 불가' in (r2['reason'] or '')
    ok &= e3
    print(f"refuse-budget: 보존 꼬리를 넘는 rank 는 **거부**한다  {'OK' if e3 else 'FAIL'}")
    # 거부 ②: 이온 N 없음 (SELF-45 이전 payload)
    r3 = repair_channel({'field_scale_ion': {'j_top_A_cm2_per_V': 1.0,
                                             'j_mean_z_A_cm2_per_V': 1.0, 'focus_top': 1.0},
                         'ionic_field': [[0, 0, 0, 1.0]]},
                        'field_scale_ion', 'ionic_field', 'ion_n_dof')
    e4 = (not r3['ok']) and 'ion_n_dof' in (r3['reason'] or '')
    ok &= e4
    print(f"refuse-no-N: 이온 N 이 없으면 **거부**한다 (근사 금지)  {'OK' if e4 else 'FAIL'}")
    # 이미 고쳐진 payload 는 no-op
    r4 = repair_channel({'n_dof': 10, 'field_scale_e': {'percentile_basis': 'full_field',
                                                        'focus_top': 7.0}, 'electronic_field': []},
                        'field_scale_e', 'electronic_field', 'n_dof')
    e5 = r4['ok'] and r4.get('noop')
    ok &= e5
    print(f"noop-new-payload: 전수 기준 payload 는 건드리지 않는다  {'OK' if e5 else 'FAIL'}")
    # ── 재귀 탐색 — 중첩이 달라도 찾는가 · 모호하면 거부하는가 ──────────────
    _nested = {'a': {'b': {'step3': {'field_scale_e': {'focus_top': 1.0}, 'n_dof': 7}}},
               'c': {'electronic_field': [[0, 0, 0, 1.0]]}}
    _f = find_key_paths(_nested)
    e6 = ([p for p, _ in _f['field_scale_e']] == ['/a/b/step3/field_scale_e']
          and [p for p, _ in _f['electronic_field']] == ['/c/electronic_field']
          and [p for p, _ in _f['n_dof']] == ['/a/b/step3/n_dof'])
    ok &= e6
    print(f"find-nested: 중첩 2단 아래의 키를 경로째 찾는다  {'OK' if e6 else 'FAIL'}")
    _dup = {'x': {'field_scale_e': {}}, 'y': {'field_scale_e': {}}}
    e7 = len(find_key_paths(_dup)['field_scale_e']) == 2
    ok &= e7
    print(f"find-ambiguous: 후보가 둘이면 둘 다 보고한다 (호출자가 거부)  "
          f"{'OK' if e7 else 'FAIL'}")
    e8 = find_key_paths({'electronic_field': [[0, 0, 0, 0.5]] * 3})['electronic_field'] != []
    ok &= e8
    print(f"find-cheap: 거대한 점군 리스트를 파고들지 않는다 (원소가 dict 아님)  "
          f"{'OK' if e8 else 'FAIL'}")

    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='SELF-45 — payload 의 focus_top 을 장 전수 기준으로 복원')
    ap.add_argument('paths', nargs='*', help='payload JSON 또는 디렉터리')
    ap.add_argument('--glob', default='*payload*.json',
                    help="디렉터리에 쓸 glob (기본 '*payload*.json' — webapp 의 payload.json 과 "
                         "킷의 mpm_payload.json 을 둘 다 잡는다)")
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
