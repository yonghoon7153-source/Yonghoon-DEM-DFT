#!/usr/bin/env python3
"""A 트랙 판정기 — `A = 1 − |u|/|v|` (개정 A3, 2026-08-28).

★★ 왜 이 파일이 생겼나 — **A1 의 식이 원 사전등록과 달랐다** (Codex R9 Q1 [P1]).
  원 사전등록(`sdcp_bridge_prereg_20260825.md`)은 격자 효과를 **절댓값**으로 정의하는데
  개정 A1 §3 은 **부호 있는 비율** `A = 1 − u/v` 를 등록했다.  둘은 같지 않다:

      u = −v  (브리지가 격자 의존을 **뒤집었다**)
        A1 :  A = 1 − (−v)/v = 2      → `A − 1.96q ≥ 0.70` 통과 → **h1**
        원등록: A = 1 − |−v|/|v| = 0   → `A + 1.96q < 0.30`  → **h0**

  ⇒ A1 대로 두면 **브리지가 격자 의존을 없앤 것이 아니라 부호만 뒤집어도 "고쳤다" 로
    판정된다.**  회귀시험 `regr-sign-flip` 이 이것을 문다.

★ 통계 표기 (R9 Q1) — **여기 나오는 q 는 표준오차가 아니다.**
  8 origin 은 고정 침대·고정 factorial 에 대한 **완전한 유한 집합**이라 표본추출 기반
  추론의 대상이 아니다 (R8 Q1).  그러나 사전등록이 이미 `q = SD/√8` 과 `1.96q` 로
  판정선을 **동결**했으므로 값을 바꾸지 않고 **이름만** 정확히 붙인다:
      q = **deterministic origin-sensitivity guard** (결정론적 origin 민감도 가드)
  ⇒ `95 % CI` · `표준오차` · `±` 로 부르지 않는다.  모집단 추론이 아니다.

사용:
    python3 scripts/bridge_grid_verdict.py \
        --off-coarse DIR --off-fine DIR --on-coarse DIR --on-fine DIR
    python3 scripts/bridge_grid_verdict.py --selftest
"""
import argparse
import glob
import json
import math
import os
import sys

H1_MIN = 0.70          # 사전등록 §4 — **동결**.  이 파일은 문턱을 바꾸지 않는다.
H0_MAX = 0.30
Z = 1.96
DENOM_K = 3.0          # |v| < K·q_x → 분모가 origin 산포에 묻힘
N_ARMS = 8


def _bits(shift, vox):
    """origin 을 **정규화 비트 튜플** `{0,½}³` 로 (A1 §1) — µm 로 짝지으면 격자마다 달라진다."""
    if shift is None:
        return None
    h = vox / 2.0
    out = []
    for s in shift:
        s = float(s)
        if abs(s) < h * 0.25:
            out.append(0)
        elif abs(s - h) < h * 0.25:
            out.append(1)
        else:
            return None                      # {0, ½} 밖 = 짝지을 수 없다
    return tuple(out)


def read_dir(d):
    """디렉터리 → {(bed, bits): sigma_e}.  `.rejected_*` 가 있으면 예외."""
    if glob.glob(os.path.join(d, '.rejected_*')):
        raise SystemExit(f'HOLD — {d} 에 기각 receipt 가 있다.  판정 대상이 아니다')
    out, vox = {}, None
    for p in sorted(glob.glob(os.path.join(d, 'p2_*.json'))):
        j = json.load(open(p, encoding='utf-8'))
        s = j.get('step3') or (j.get('mpm_metrics') or {}).get('step3') or {}
        m = s.get('manifest') or {}
        v = m.get('vox_um') or s.get('vox_um')
        if v is None:
            raise SystemExit(f'HOLD — {os.path.basename(p)} 에 vox 가 없다')
        vox = float(v) if vox is None else vox
        if abs(float(v) - vox) > 1e-12:
            raise SystemExit(f'HOLD — {d} 안에서 vox 가 섞였다')
        if s.get('cg_info') not in (0, None) or s.get('unconverged'):
            raise SystemExit(f'HOLD — {os.path.basename(p)} 미수렴 (cg_info={s.get("cg_info")})')
        b = _bits(m.get('origin_shift_um'), vox)
        if b is None:
            raise SystemExit(f'HOLD — {os.path.basename(p)} origin 이 {{0,½}}³ 밖이다')
        bed = 'SBE' if '_SBE_' in os.path.basename(p) else 'DBE'
        out[(bed, b)] = float(s['sigma_e_eff_S_cm'])
    return out, vox


def ratios(cells):
    """{(bed,bits): σ} → {bits: R = σ(DBE)/σ(SBE)}.  8 origin 완비를 요구한다."""
    bits = sorted({b for (_, b) in cells})
    if len(bits) != N_ARMS:
        raise SystemExit(f'HOLD — origin {len(bits)}/{N_ARMS} (완전 factorial 아님)')
    r = {}
    for b in bits:
        if ('SBE', b) not in cells or ('DBE', b) not in cells:
            raise SystemExit(f'HOLD — origin {b} 에 침대 한 쪽이 없다')
        r[b] = cells[('DBE', b)] / cells[('SBE', b)]
    return r


def _mean(a):
    return sum(a) / len(a)


def _var(a):
    m = _mean(a)
    return sum((x - m) ** 2 for x in a) / (len(a) - 1)


def _cov(a, b):
    ma, mb = _mean(a), _mean(b)
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (len(a) - 1)


def judge(x, y):
    """x_i = ΔR_i(off) · y_i = ΔR_i(on)  →  판정 dict.

    ★ `A = 1 − |u|/|v|` — **절댓값** (원 사전등록 정의, R9 Q1).
    """
    v, u = _mean(x), _mean(y)
    var_v, var_u, cov = _var(x) / len(x), _var(y) / len(y), _cov(x, y) / len(x)
    q_x = math.sqrt(var_v)                      # origin 민감도 가드 (표준오차 아님)
    q_y = math.sqrt(var_u)

    res = {'x': list(x), 'y': list(y), 'v': v, 'u': u, 'D_off': abs(v), 'D_on': abs(u),
           'q_x': q_x, 'q_y': q_y,
           'sign_flip': (v * u) < 0,           # 브리지가 격자 효과의 **부호**를 뒤집었나
           'x_range': (min(x), max(x)), 'y_range': (min(y), max(y)),
           'x_all_same_sign': all(t > 0 for t in x) or all(t < 0 for t in x),
           'y_all_same_sign': all(t > 0 for t in y) or all(t < 0 for t in y)}

    #  ★ 분모 gate 를 **먼저** 본다 — |v| 가 origin 산포에 묻히면 A 는 정의되지 않는다.
    #    ⚠ 이름이 바뀌었다 (R9 Q1): "격자 효과가 없다" 가 아니라 **"off 대비가 origin
    #      산포에 대해 불안정하다"** 다.  전자는 물리 주장이고 후자는 측정 한계다.
    if abs(v) < DENOM_K * q_x:
        res.update(A=None, decision='INDETERMINATE_OFF_GRID_CONTRAST_ORIGIN_UNSTABLE',
                   reason=f'|v| = {abs(v):.6g} < {DENOM_K}·q_x = {DENOM_K * q_x:.6g}')
        return res

    A = 1.0 - abs(u) / abs(v)
    #  델타법 — A = 1 − |u|/|v| 의 편도함수 (부호 함수가 들어간다)
    su, sv = (1.0 if u >= 0 else -1.0), (1.0 if v >= 0 else -1.0)
    dA_du = -su / abs(v)
    dA_dv = abs(u) * sv / (v * v)
    var_A = (dA_du ** 2) * var_u + (dA_dv ** 2) * var_v + 2 * dA_du * dA_dv * cov
    q_A = math.sqrt(max(var_A, 0.0))
    lo, hi = A - Z * q_A, A + Z * q_A

    if lo >= H1_MIN:
        dec, why = 'h1', f'{lo:.4f} ≥ {H1_MIN}'
    elif hi < H0_MAX:
        dec, why = 'h0', f'{hi:.4f} < {H0_MAX}'
    elif lo > H0_MAX and hi < H1_MIN:
        dec, why = 'BOTH_REJECTED', f'[{lo:.4f}, {hi:.4f}] ⊂ ({H0_MAX}, {H1_MIN})'
    else:
        dec, why = 'INDETERMINATE_PRECISION', f'[{lo:.4f}, {hi:.4f}] 이 문턱을 걸친다'
    res.update(A=A, q_A=q_A, guard_lo=lo, guard_hi=hi, decision=dec, reason=why)
    return res


def report(res, vox_c, vox_f):
    print(f'\n══ A 트랙 판정 (개정 A3 · A = 1 − |u|/|v|) ══')
    print(f'  격자  거친 {vox_c} → 고운 {vox_f}\n')
    print('  origin      ΔR(off)=x_i      ΔR(on)=y_i')
    for i, (a, b) in enumerate(zip(res['x'], res['y'])):
        print(f'   arm {i}     {a:+.6f}       {b:+.6f}')
    print(f'\n  v = mean(x) = {res["v"]:+.6f}   |v| = {res["D_off"]:.6f}   q_x = {res["q_x"]:.6f}')
    print(f'  u = mean(y) = {res["u"]:+.6f}   |u| = {res["D_on"]:.6f}   q_y = {res["q_y"]:.6f}')
    print(f'  x 범위 [{res["x_range"][0]:+.6f}, {res["x_range"][1]:+.6f}]  '
          f'전부 같은 부호 {res["x_all_same_sign"]}')
    print(f'  y 범위 [{res["y_range"][0]:+.6f}, {res["y_range"][1]:+.6f}]  '
          f'전부 같은 부호 {res["y_all_same_sign"]}')
    if res['sign_flip']:
        print('  ⚠⚠ **부호 반전** — 브리지가 격자 효과의 방향을 뒤집었다 (u·v < 0).')
        print('     A1 의 옛 식 `1 − u/v` 이었다면 A > 1 로 h1 이 나왔을 자리다.')
    if res['A'] is not None:
        print(f'\n  A = 1 − |u|/|v| = {res["A"]:.6f}   q_A = {res["q_A"]:.6f}')
        print(f'  가드 구간 [{res["guard_lo"]:.4f}, {res["guard_hi"]:.4f}]')
        print('  ⚠ 이 구간은 **95 % CI 가 아니다** — 8 origin 은 고정 유한 집합이고,')
        print('    이것은 동결된 결정론적 origin 민감도 가드다 (R8 Q1 · R9 Q1).')
    print(f'\n  ▸ 판정: **{res["decision"]}**   ({res["reason"]})')
    print('  ⚠ 문턱 0.30 / 0.70 은 원 사전등록 §4 에서 동결됐다 — 이 도구는 바꾸지 않는다.')


def main(argv=None):
    ap = argparse.ArgumentParser(description='A 트랙 판정 — A = 1 − |u|/|v| (개정 A3)')
    ap.add_argument('--off-coarse', help='브리지 off · 거친 격자 (vox 0.15)')
    ap.add_argument('--off-fine', help='브리지 off · 고운 격자 (vox 0.125)')
    ap.add_argument('--on-coarse', help='브리지 on · 거친 격자')
    ap.add_argument('--on-fine', help='브리지 on · 고운 격자')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    need = (a.off_coarse, a.off_fine, a.on_coarse, a.on_fine)
    if not all(need):
        ap.error('네 디렉터리가 전부 필요하다 (또는 --selftest)')

    oc, vc1 = read_dir(a.off_coarse)
    of, vf1 = read_dir(a.off_fine)
    nc, vc2 = read_dir(a.on_coarse)
    nf, vf2 = read_dir(a.on_fine)
    if abs(vc1 - vc2) > 1e-12 or abs(vf1 - vf2) > 1e-12:
        raise SystemExit('HOLD — off/on 의 격자가 짝이 안 맞는다')
    if vf1 >= vc1:
        raise SystemExit('HOLD — --*-fine 이 --*-coarse 보다 곱지 않다')

    r_oc, r_of, r_nc, r_nf = (ratios(oc), ratios(of), ratios(nc), ratios(nf))
    bits = sorted(r_oc)
    for nm, r in (('off-fine', r_of), ('on-coarse', r_nc), ('on-fine', r_nf)):
        if sorted(r) != bits:
            raise SystemExit(f'HOLD — {nm} 의 origin 집합이 다르다 (비트 튜플 짝짓기 실패)')
    x = [r_of[b] - r_oc[b] for b in bits]
    y = [r_nf[b] - r_nc[b] for b in bits]
    report(judge(x, y), vc1, vf1)
    return 0


def _selftest():
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        ok = ok and bool(cond)

    #  ★★★ 핵심 회귀 — **부호 반전이 h1 로 새면 안 된다** (R9 Q1 [P1]).
    #    옛 A1 식 `1 − u/v` 는 u = −v 에서 A = 2 를 내어 h1 을 통과시켰다.
    x = [0.0100, 0.0102, 0.0098, 0.0101, 0.0099, 0.0100, 0.0101, 0.0099]
    y = [-t for t in x]                                     # 정확히 뒤집힘
    r = judge(x, y)
    chk('regr-sign-flip  u = −v → A = 0 (h1 아님)', abs(r['A'] - 0.0) < 1e-12)
    chk('regr-sign-flip  판정이 h0', r['decision'] == 'h0')
    chk('regr-sign-flip  부호 반전을 보고한다', r['sign_flip'] is True)
    #  ★ 음성 대조 — 옛 식이었다면 h1 이었음을 명시적으로 확인 (검사가 무는지 보여 준다)
    chk('regr-sign-flip  옛 식 `1−u/v` 는 2.0 을 냈을 것', abs((1 - _mean(y) / _mean(x)) - 2.0) < 1e-9)

    #  브리지가 격자 의존을 거의 없앤 경우 → h1
    y2 = [t * 0.05 for t in x]
    r2 = judge(x, y2)
    chk('h1  |u|/|v| = 0.05 → A ≈ 0.95', r2['decision'] == 'h1' and r2['A'] > 0.9)

    #  브리지가 거의 못 줄인 경우 → h0
    y3 = [t * 0.95 for t in x]
    r3 = judge(x, y3)
    chk('h0  |u|/|v| = 0.95 → A ≈ 0.05', r3['decision'] == 'h0' and r3['A'] < 0.1)

    #  분모가 origin 산포에 묻히면 A 를 내지 않는다 (이름도 확인)
    x4 = [0.0001, -0.0002, 0.0003, -0.0001, 0.0002, -0.0003, 0.0001, -0.0001]
    r4 = judge(x4, y2)
    chk('분모 gate → INDETERMINATE_OFF_GRID_CONTRAST_ORIGIN_UNSTABLE',
        r4['decision'] == 'INDETERMINATE_OFF_GRID_CONTRAST_ORIGIN_UNSTABLE'
        and r4['A'] is None)

    #  ★ 문턱이 동결돼 있다 (이 파일이 사전등록을 바꾸지 않는다)
    chk('문턱 동결 0.30 / 0.70', (H0_MAX, H1_MIN) == (0.30, 0.70))

    #  ★ 비트 튜플 짝짓기 — 다른 격자의 같은 팔이 같은 키를 받아야 한다 (A1 §1)
    chk('origin 짝짓기: 0.075@vox0.15 ↔ 0.0625@vox0.125 가 같은 비트',
        _bits([0.0, 0.075, 0.075], 0.15) == _bits([0.0, 0.0625, 0.0625], 0.125) == (0, 1, 1))
    chk('origin 짝짓기: {0,½} 밖은 거부', _bits([0.0, 0.03, 0.0], 0.15) is None)

    #  기각 receipt 가 있으면 판정 대상이 아니다 (R9 Q5 와 같은 부류)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, '.rejected_20260828'), 'w').close()
        try:
            read_dir(td)
            chk('.rejected_* → HOLD', False)
        except SystemExit as ex:
            chk('.rejected_* → HOLD', '기각 receipt' in str(ex))

    print('\n✓ bridge_grid_verdict selftest PASS' if ok
          else '\n✗ bridge_grid_verdict selftest FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
