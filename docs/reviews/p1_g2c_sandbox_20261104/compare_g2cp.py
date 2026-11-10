#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G2c′ 샌드박스 대조기 (읽기만 · 표준 라이브러리) — 2026-11-10 · 결과 0 건 상태에서 씀.

    python3 -I compare_g2cp.py OUT N     → OUT/compare_g2cp.json + 화면 표
    rc 0 = 대조 끝 (맞음 · 틀림 · 해당 없음 은 JSON 에) · rc 2 = '계산 못 함' 이 하나라도 (입력 결손 · 읽기 문제 · 인자)

등록 = 메모 docs/reviews/p1_g2c_compare_definition_20261105.md §0 (11-10 개정 · 결과 전 · Codex Q6 답 반영) — 예측마다
맞음 / 틀림 / 해당 없음 / 계산 못 함 + 등록 판정 (§3 · 허용폭 1e-5 · 열 중앙값 floor 그대로 · 키트 ul_gates.g2c_compare 와 같은 식).
팔 = 실행기 run_g2cp.sh 의 OUT/<팔>/post/c_N.txt · atom_N.txt (A · A2 = cpre_{N-1}.txt 도) · rst/*.bin.

쌍 덤프 30 열 (compute pair/gran/local 순서 · 11-04 probe) = pos 6 · id 3 (i j 주기 표지) · force 3 · force_normal 3 · force_tangential 3 ·
torque 3 · history 4 (deltaMax · shear 3) · contactArea · delta · contactPoint 3.
정규화 = 무순서 쌍 키 (작은 id, 큰 id) · 방향 바뀐 행 (id1 > id2) = pos 두 묶음 맞바꿈 · force · force_normal · force_tangential 9 열 ·
shear 3 열 부호 반전 · 주기 표지 · deltaMax · torque 그대로 (torque 는 같은 방향 행만 비교).
값 같음 = %.17g 글자에서 읽은 float 가 정확히 같음 (−0 = 0) · 바이트 같음 = 파일 sha256 같음 (행 순서 · 글자 꼴 포함).
"""
from __future__ import annotations

import decimal
import hashlib
import json
import math
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EPS = 2.0 ** -52
REL = 1e-5            # 등록 허용폭 (메모 §3 · 키트 g2c_compare rel) — 바꾸지 않는다
MARGIN = 1e-9         # 바 — 고착 · 미끄럼 분류 여유 (결과 전 고정)
E_REL = 1e-9          # 바 — 허용 E 의 상대 몫 (kt 를 다시 계산한 끝자리 차이 몫)
E_ABS_K = 64          # 바 — 허용 E 의 끝자리 몫 (ε 배 · |F_B|+|F_C|+kt|s_B|+kt|s_C| 에 곱함)
ULP_K = 4             # 예외 ① · ② — deltaMax ↔ delta 비교 (ulp · 두 코드 자리의 같은 식이라 정확 일치가 예상 · FMA 여유)
CIRCLE_REL = 1e-9     # 바 보고 — 미끄럼 쌍 |F_t,model| = μ|Fn| 상대
ID_MAX = 2 ** 53
ARMS = ('A', 'A2', 'B', 'B2', 'C', 'BW', 'BR', 'CW', 'CR')
SETUP_ARMS = ('B', 'B2', 'C', 'BW', 'BR', 'CW', 'CR')
PERIODIC_SIDE = ('B', 'B2', 'BW')
DECKS7 = ('head.inc', 'mat.inc', 'fresh.inc', 'outA.inc', 'A.liggghts', 'A2.liggghts', 'R.liggghts')
ATOM_COLS = ('id', 'type', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'omegax', 'omegay', 'omegaz', 'radius')
REF_N = 40000         # run_40000 (11-04) 의 N

_L = dict(pos=(0, 1, 2, 3, 4, 5), ids=(6, 7), flag=8, force=(9, 10, 11), fn=(12, 13, 14), ft=(15, 16, 17), tq=(18, 19, 20))
LAYOUT = {30: dict(_L, dm=21, sh=(22, 23, 24), area=25, delta=26, cp=(27, 28, 29), ncol=30),
          26: dict(_L, dm=None, sh=None, area=21, delta=22, cp=(23, 24, 25), ncol=26)}


def _groups(lay):
    g = [('pos', lay['pos']), ('flag', (lay['flag'],)), ('force', lay['force']), ('force_normal', lay['fn']),
         ('force_tangential', lay['ft']), ('torque', lay['tq'])]
    if lay['dm'] is not None:
        g += [('deltaMax', (lay['dm'],)), ('shear', lay['sh'])]
    g += [('contactArea', (lay['area'],)), ('delta', (lay['delta'],)), ('contactPoint', lay['cp'])]
    return g


def _flip(v, lay):
    """방향 바뀐 행 → 작은 id 쪽 행 (pos 맞바꿈 · 힘 9 열 · shear 3 열 부호 반전)."""
    w = list(v[3:6]) + list(v[0:3]) + list(v[6:])
    for c in lay['force'] + lay['fn'] + lay['ft'] + (lay['sh'] or ()):
        w[c] = -w[c]
    return w


# ── 읽기 ─────────────────────────────────────────────────────────────────────────────────
_INT = re.compile(r'[+-]?[0-9]+')


def _id_tok(tok):
    """ID 토큰 → (int | None, 문제 | None) — 키트 ul_lib._id_value · exact_id 와 같은 규칙 (정수 토큰 = int · 소수 꼴은 정확히 정수일 때만 ·
    0 < id ≤ 2^53 · 소수 ID 를 정수로 자르지 않는다)."""
    if _INT.fullmatch(tok):
        v = int(tok)
    else:
        try:
            f = float(tok)
        except ValueError:
            return None, f'ID 숫자 아님 {tok!r}'
        if not (math.isfinite(f) and f.is_integer()):
            return None, f'ID 정수 아님 {tok!r}'
        try:
            if decimal.Decimal(tok) != decimal.Decimal(int(f)):
                return None, f'ID 정확한 정수 아님 {tok!r}'
        except decimal.InvalidOperation:
            return None, f'ID 토큰 {tok!r}'
        v = int(f)
    if not (0 < v <= ID_MAX):
        return None, f'ID 범위 밖 {tok!r}'
    return v, None


def _head(lines, nhead, pr):
    step = n_decl = box = None
    try:
        step = int(lines[lines.index('ITEM: TIMESTEP') + 1].strip())
    except (ValueError, IndexError):
        pr.append('TIMESTEP 머리 없음')
    try:
        n_decl = int(lines[lines.index(nhead) + 1].strip())
    except (ValueError, IndexError):
        pr.append(f'{nhead} 머리 없음')
    kb = next((i for i, x in enumerate(lines) if x.startswith('ITEM: BOX BOUNDS')), None)
    if kb is None or lines[kb].split()[:3] != ['ITEM:', 'BOX', 'BOUNDS']:
        pr.append('BOX BOUNDS 머리 없음')
    else:
        try:
            b = []
            for j in (1, 2, 3):
                t = lines[kb + j].split()
                if len(t) != 2:
                    raise ValueError('두 값 아님')
                lo, hi = float(t[0]), float(t[1])
                if not (math.isfinite(lo) and math.isfinite(hi) and lo < hi):
                    raise ValueError('비유한 · lo ≥ hi')
                b.append((lo, hi))
            box = b
        except (ValueError, IndexError) as e:
            pr.append(f'BOX BOUNDS 꼴 오류 ({e})')
    return step, n_decl, box


def read_local(path, ncol=30):
    """쌍 덤프 한 장 → dict(ok · problems · missing_required · step · box · box_xy · by_key{키: v · flipped · idx} · dups · n_rows)."""
    lay = LAYOUT[ncol]
    out = dict(ok=False, path=path, ncol=ncol, problems=[], missing_required=False, step=None, box=None, box_xy=None,
               cols=None, by_key={}, dups=[], n_rows=0, n_flag_bad=0)
    pr = out['problems']
    if not path or not os.path.isfile(path):
        pr.append(f'파일 없음: {path}')
        return out
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    out['step'], n_decl, out['box'] = _head(lines, 'ITEM: NUMBER OF ENTRIES', pr)
    if out['box']:
        out['box_xy'] = (out['box'][0][1] - out['box'][0][0], out['box'][1][1] - out['box'][1][0])
    kh = next((i for i, x in enumerate(lines) if x.startswith('ITEM: ENTRIES')), None)
    if kh is None or lines[kh].split()[:2] != ['ITEM:', 'ENTRIES']:
        pr.append('ENTRIES 머리 없음')
        out['missing_required'] = True
        return out
    cols = lines[kh].split()[2:]
    out['cols'] = cols
    req = ['c_cpl[%d]' % i for i in range(1, ncol + 1)]
    if cols != req:
        pr.append(f'열 이름 {len(cols)} 개 ≠ 기대 c_cpl[1..{ncol}]')
        if not set(req) <= set(cols):
            out['missing_required'] = True
        return out
    rows, rowprob = [], False
    for ln in lines[kh + 1:]:
        if not ln.strip():
            continue
        if ln.startswith('ITEM:'):
            pr.append('한 파일에 프레임이 둘 이상')
            break
        t = ln.split()
        if len(t) != ncol:
            pr.append(f'열 수 {len(t)} ≠ {ncol}')
            rowprob = True
            continue
        vals, bad = [], None
        for c, tok in enumerate(t):
            if c in lay['ids']:
                v, p_ = _id_tok(tok)
                if v is None:
                    bad = p_
                    break
                vals.append(v)
            else:
                try:
                    f = float(tok)
                except ValueError:
                    bad = f'숫자 아님 {tok!r}'
                    break
                if not math.isfinite(f):
                    bad = f'비유한 {tok!r}'
                    break
                vals.append(f)
        if bad:
            pr.append(bad + f' — {ln[:60]}')
            rowprob = True
            continue
        rows.append(vals)
    if n_decl is not None and n_decl != len(rows) and not rowprob:
        pr.append(f'행 수 {len(rows)} ≠ 머리 {n_decl}')
    out['n_rows'] = len(rows)
    for idx, v in enumerate(rows):
        i, j = v[6], v[7]
        if v[lay['flag']] not in (0.0, 1.0):
            out['n_flag_bad'] += 1
        flipped = i > j
        w = _flip(v, lay) if flipped else [float(x) for x in v]
        w[6], w[7] = float(v[6]), float(v[7])
        key = (min(i, j), max(i, j))
        if key in out['by_key']:
            out['dups'].append((key, w, flipped, idx))
            continue
        out['by_key'][key] = dict(v=w, flipped=flipped, idx=idx)
    out['ok'] = not pr
    return out


def read_atoms(path):
    """원자 덤프 (id type x y z vx vy vz omegax omegay omegaz radius) → dict(ok · problems · by_id{id: (type, [x … radius])} · step · box)."""
    out = dict(ok=False, path=path, problems=[], missing_required=False, step=None, box=None, by_id={}, n_rows=0)
    pr = out['problems']
    if not path or not os.path.isfile(path):
        pr.append(f'파일 없음: {path}')
        return out
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    out['step'], n_decl, out['box'] = _head(lines, 'ITEM: NUMBER OF ATOMS', pr)
    kh = next((i for i, x in enumerate(lines) if x.startswith('ITEM: ATOMS')), None)
    if kh is None or lines[kh].split()[:2] != ['ITEM:', 'ATOMS']:
        pr.append('ATOMS 머리 없음')
        out['missing_required'] = True
        return out
    cols = tuple(lines[kh].split()[2:])
    if cols != ATOM_COLS:
        pr.append(f'원자 열 {cols} ≠ {ATOM_COLS}')
        out['missing_required'] = not set(ATOM_COLS) <= set(cols)
        return out
    rowprob, n = False, 0
    for ln in lines[kh + 1:]:
        if not ln.strip():
            continue
        if ln.startswith('ITEM:'):
            pr.append('한 파일에 프레임이 둘 이상')
            break
        t = ln.split()
        if len(t) != len(ATOM_COLS):
            pr.append(f'원자 열 수 {len(t)}')
            rowprob = True
            continue
        aid, p_ = _id_tok(t[0])
        ty = int(t[1]) if _INT.fullmatch(t[1]) and int(t[1]) >= 1 else None
        try:
            vals = [float(x) for x in t[2:]]
        except ValueError:
            vals = None
        if aid is None or ty is None or vals is None or not all(math.isfinite(x) for x in vals):
            pr.append(f'원자 줄 오류 — {ln[:60]}')
            rowprob = True
            continue
        if aid in out['by_id']:
            pr.append(f'원자 ID 중복 {aid}')
            continue
        out['by_id'][aid] = (ty, vals)
        n += 1
    if n_decl is not None and n_decl != n and not rowprob:
        pr.append(f'원자 수 {n} ≠ 머리 {n_decl}')
    out['n_rows'] = n
    out['ok'] = not pr
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def file_bytes_equal(a, b):
    return bool(a and b and os.path.isfile(a) and os.path.isfile(b) and sha256(a) == sha256(b))


def read_md5_list(path):
    """md5sum 꼴 → [(hash, name)] (없으면 [])."""
    out = []
    if path and os.path.isfile(path):
        for ln in open(path, encoding='utf-8', errors='replace').read().splitlines():
            t = ln.split(None, 1)
            if len(t) == 2 and re.fullmatch(r'[0-9a-f]{32}', t[0]):
                out.append((t[0], t[1].strip()))
    return out


def read_kv(path):
    out = {}
    if path and os.path.isfile(path):
        for ln in open(path, encoding='utf-8', errors='replace').read().splitlines():
            t = ln.split(None, 1)
            if t:
                out[t[0]] = t[1].strip() if len(t) > 1 else ''
    return out


# ── 값 · 바이트 ──────────────────────────────────────────────────────────────────────────
def pairs_value(D1, D2):
    """값 동일성 (Q6-1 앞 문장) — ID · 방향을 맞춘 30 열 · 쌍 집합 · TIMESTEP · 상자 · 중복 0."""
    out = dict(equal=False, computed=False, why=[])
    if not (D1['ok'] and D2['ok']):
        out['why'] = (D1['problems'][:2] + D2['problems'][:2]) or ['읽기 실패']
        return out
    lay = LAYOUT[D1['ncol']]
    out['computed'] = True
    k1, k2 = D1['by_key'], D2['by_key']
    common = sorted(set(k1) & set(k2))
    only1, only2 = sorted(set(k1) - set(k2)), sorted(set(k2) - set(k1))
    bg = {g: 0 for g, _ in _groups(lay)}
    ndiff, ex, orient = 0, [], 0
    for k in common:
        a, b = k1[k], k2[k]
        if a['flipped'] != b['flipped']:
            orient += 1
        d = False
        for g, cols in _groups(lay):
            if g == 'torque' and a['flipped'] != b['flipped']:
                continue
            if any(a['v'][c] != b['v'][c] for c in cols):
                bg[g] += 1
                d = True
        if d:
            ndiff += 1
            if len(ex) < 5:
                ex.append(list(k))
    out.update(n1=len(k1), n2=len(k2), n_common=len(common), only1=len(only1), only2=len(only2), orientation_differs=orient,
               dup1=len(D1['dups']), dup2=len(D2['dups']), n_pairs_differ=ndiff, by_group=bg, examples=ex,
               step=(D1['step'], D2['step']), box_equal=D1['box'] == D2['box'])
    w = out['why']
    if D1['step'] != D2['step']:
        w.append(f'TIMESTEP {D1["step"]} ≠ {D2["step"]}')
    if D1['box'] != D2['box']:
        w.append('상자 다름')
    if only1 or only2:
        w.append(f'쌍 집합 다름 (D1 만 {len(only1)} · D2 만 {len(only2)})')
    if D1['dups'] or D2['dups']:
        w.append(f'중복 키 {len(D1["dups"])} · {len(D2["dups"])}')
    if ndiff:
        w.append(f'값 다른 쌍 {ndiff} ({", ".join(g for g, n in bg.items() if n)})')
    out['equal'] = not w
    return out


def atoms_value(A1, A2):
    out = dict(equal=False, computed=False, why=[])
    if not (A1['ok'] and A2['ok']):
        out['why'] = (A1['problems'][:2] + A2['problems'][:2]) or ['읽기 실패']
        return out
    out['computed'] = True
    a, b = A1['by_id'], A2['by_id']
    common = sorted(set(a) & set(b))
    nd = sum(1 for i in common if a[i] != b[i])
    o1, o2 = len(set(a) - set(b)), len(set(b) - set(a))
    out.update(n1=len(a), n2=len(b), n_common=len(common), only1=o1, only2=o2, n_differ=nd)
    if A1['step'] != A2['step']:
        out['why'].append(f'TIMESTEP {A1["step"]} ≠ {A2["step"]}')
    if o1 or o2:
        out['why'].append(f'원자 집합 다름 ({o1} · {o2})')
    if nd:
        out['why'].append(f'값 다른 원자 {nd}')
    out['equal'] = not out['why']
    return out


# ── 판정 (등록 §3 · 키트 g2c_compare 와 같은 식) ─────────────────────────────────────────
def _cmpvals(v, lay, box, hist):
    lx, ly = box
    out = [v[0] % lx, v[1] % ly, v[2], v[3] % lx, v[4] % ly, v[5]] + [v[c] for c in lay['force'] + lay['fn'] + lay['ft']]
    if hist:
        out += [v[lay['dm']]] + [v[c] for c in lay['sh']]
    cp = lay['cp']
    return out + [v[lay['area']], v[lay['delta']], v[cp[0]] % lx, v[cp[1]] % ly, v[cp[2]]]


def judge(ref, test, expected_step=None, mode='g2cp'):
    """G2c′ 판정 — 쌍 집합 같음 · 같은 값 중복 = 수 · 다른 값 = 위반 · TIMESTEP = 요청 · 열마다 |차| ≤ 1e-5 × max(|기준 값|, 그 열 |기준 값| 중앙값)
    (위치 · 접점 x y = 상자로 감음) · torque · 주기 표지 = 판정 밖 · mode g2cp = 이력 4 열 포함 (메모 Q2) · kit26 = 키트 26 열 (이력 없음)."""
    out = dict(status='FAIL', why=[], mode=mode)
    if not (ref['ok'] and test['ok']):
        out['why'] = ref['problems'][:3] + test['problems'][:3]
        if ref.get('missing_required') or test.get('missing_required'):
            out['status'] = 'NOT_COMPUTED'
        return out
    if ref['step'] != test['step'] or (expected_step is not None and ref['step'] != expected_step):
        out['why'].append(f'쌍 덤프 TIMESTEP {test["step"]} · {ref["step"]} ≠ 요청 {expected_step if expected_step is not None else ref["step"]}')
        return out
    lay = LAYOUT[ref['ncol']]
    hist = mode == 'g2cp' and lay['dm'] is not None
    box = ref['box_xy']
    conflicts, ndup = [], 0
    for D in (test, ref):
        for key, w, _f, _i in D['dups']:
            first = _cmpvals(D['by_key'][key]['v'], lay, box, hist)
            if all(abs(x - y) <= 1e-12 * max(1.0, abs(x)) for x, y in zip(first, _cmpvals(w, lay, box, hist))):
                ndup += 1
            else:
                conflicts.append(list(key))
    O, T = ref['by_key'], test['by_key']
    miss, extra = sorted(set(O) - set(T)), sorted(set(T) - set(O))
    ov = {k: _cmpvals(e['v'], lay, box, hist) for k, e in O.items()}
    tv = {k: _cmpvals(e['v'], lay, box, hist) for k, e in T.items()}
    ncol = len(next(iter(ov.values()))) if ov else 0
    med = [statistics.median(abs(x[c]) for x in ov.values()) for c in range(ncol)] if ov else []
    lengths = [box[0], box[1], None, box[0], box[1], None] + [None] * 9 + ([None] * 4 if hist else []) + [None, None, box[0], box[1], None]
    bad, nbit = [], 0
    for k in sorted(set(O) & set(T)):
        if O[k]['v'] == T[k]['v']:
            nbit += 1
        for c, (a, b) in enumerate(zip(ov[k], tv[k])):
            d = abs(a - b)
            if lengths[c]:
                d = min(d, lengths[c] - d)
            if d > REL * max(abs(a), med[c]):
                bad.append((list(k), c))
                break
    ftc = lay['ft']
    ft = [math.sqrt(sum(O[k]['v'][c] ** 2 for c in ftc)) for k in O]
    sh = [math.sqrt(sum(O[k]['v'][c] ** 2 for c in lay['sh'])) for k in O] if lay['sh'] else []
    out.update(n_ref=len(O), n_test=len(T), n_mismatch=len(bad), missing=[list(x) for x in miss[:5]], extra=[list(x) for x in extra[:5]],
               n_dup_consistent=ndup, dup_conflicts=conflicts[:5], n_bit_equal=nbit, first_bad=bad[:5],
               discriminating_frac=(sum(1 for x in ft if x > 0) / len(ft)) if ft else None,
               shear_nonzero_frac=(sum(1 for x in sh if x > 0) / len(sh)) if sh else None,
               n_periodic=sum(1 for k in O if O[k]['v'][lay['flag']] != 0.0))
    out['status'] = 'PASS' if not (miss or extra or bad or conflicts) else 'FAIL'
    return out


# ── 덱 물성 · kt ─────────────────────────────────────────────────────────────────────────
def material(here=HERE):
    """mat.inc · fresh.inc → 물성 (빠지면 ValueError — 대조기는 값을 짐작하지 않는다)."""
    mat = open(os.path.join(here, 'mat.inc'), encoding='utf-8').read()
    fresh = open(os.path.join(here, 'fresh.inc'), encoding='utf-8').read()

    def pg(name, kind):
        m = re.search(r'^\s*fix\s+\S+\s+all\s+property/global\s+' + re.escape(name) + r'\s+' + kind + r'\s+(.+?)\s*$', mat, re.M)
        if not m:
            raise ValueError(f'mat.inc 에 {name} {kind} 없음')
        return [float(x) for x in m.group(1).split()]

    nb = re.search(r'^\s*create_box\s+(\d+)\s', fresh, re.M)
    if not nb:
        raise ValueError('fresh.inc 에 create_box 없음')
    nt = int(nb.group(1))
    E, nu = pg('youngsModulus', 'peratomtype'), pg('poissonsRatio', 'peratomtype')
    fr, vc = pg('coefficientFriction', 'peratomtypepair'), pg('characteristicVelocity', 'scalar')
    if len(E) != nt or len(nu) != nt or len(vc) != 1 or len(fr) != 1 + nt * nt or int(fr[0]) != nt:
        raise ValueError('물성 값 수가 형 수와 다르다')
    tpl = re.findall(r'^\s*fix\s+\S+\s+all\s+particletemplate/sphere\s+\d+\s+atom_type\s+(\d+)\s+density\s+constant\s+(\S+)\s+radius\s+constant\s+(\S+)',
                     fresh, re.M)
    rho, rad = {}, {}
    for t, d, r in tpl:
        rho[int(t)], rad[int(t)] = float(d), float(r)
    if sorted(rho) != list(range(1, nt + 1)):
        raise ValueError('particletemplate 형이 1..n 이 아니다')
    dt = re.search(r'^\s*timestep\s+(\S+)', fresh, re.M)
    skin = re.search(r'^\s*neighbor\s+(\S+)\s+bin', mat, re.M)
    box = re.search(r'^\s*region\s+reg_box\s+block\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', fresh, re.M)
    wall = re.search(r'primitive\s+type\s+\d+\s+zplane\s+(\S+)', mat)
    if not (dt and skin and box and wall):
        raise ValueError('timestep · neighbor · reg_box · zplane 중 없음')
    bx = [float(x) for x in box.groups()]
    mu = {(i, j): fr[1 + (i - 1) * nt + (j - 1)] for i in range(1, nt + 1) for j in range(1, nt + 1)}
    return dict(ntypes=nt, E={i + 1: E[i] for i in range(nt)}, nu={i + 1: nu[i] for i in range(nt)}, rho=rho, rad=rad, mu=mu, vc=vc[0],
                dt=float(dt.group(1)), skin=float(skin.group(1)), box_xy=(bx[1] - bx[0], bx[3] - bx[2]), wall_z=float(wall.group(1)),
                src_md5={f: md5(os.path.join(here, f)) for f in ('mat.inc', 'fresh.inc')})


def kt(mat, ti, tj, ri, rj):
    """kt = kn (normal_model_hooke_hysteresis.h 139–146 · SI → nktv2p 1) · Y* (global_properties.cpp 432) · R* (117) · m* (pair_gran_base.h 384) ·
    m = ρ·4πr³/3 (particletemplate density constant)."""
    Ei, Ej, vi, vj = mat['E'][ti], mat['E'][tj], mat['nu'][ti], mat['nu'][tj]
    Y = 1. / ((1. - math.pow(vi, 2.)) / Ei + (1. - math.pow(vj, 2.)) / Ej)
    reff = ri * rj / (ri + rj)
    mi = mat['rho'][ti] * 4.0 / 3.0 * math.pi * ri ** 3
    mj = mat['rho'][tj] * 4.0 / 3.0 * math.pi * rj ** 3
    meff = mi * mj / (mi + mj)
    sq = math.sqrt(reff)
    cv = mat['vc']
    return 16. / 15. * sq * Y * math.pow(15. * meff * cv * cv / (16. * sq * Y), 0.2)


def _sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _nrm(a):
    return math.sqrt(_dot(a, a))


def _en(v, box):
    """작은 id 쪽 단위 중심선 en = (x_작은 − x_큰)/r (덤프 pos · x y 최소상)."""
    d = _sub(v[0:3], v[3:6])
    for c in (0, 1):
        L = box[c]
        d[c] -= L * round(d[c] / L)
    r = _nrm(d)
    return [x / r for x in d], r, d


# ── 예측 ─────────────────────────────────────────────────────────────────────────────────
def pred_ba(B, C, atoms, mat):
    """바 (Q6-3 사영식) — 양쪽 고착 쌍: ΔF = −kt Δs · ΔF_n,dump = −kt (n·Δs) n · ΔF_t,dump = −kt [Δs − (n·Δs) n] (ΔX = X_B − X_C) 이
    E = 1e-9·kt|Δs| + 64ε(|F_B|+|F_C|+kt|s_B|+kt|s_C|) 안.  고착 = kt|s| ≤ (1−1e-9) μ|Fn| (둘 다) · Fn = F_C·en (C 의 shear ⊥ en)."""
    out = dict(status='계산 못 함', why=[], n_common=0, n_stick_both=0, n_slip_any=0, n_slip_both=0, n_slip_both_on_circle=0,
               n_boundary=0, n_dm_differ=0, n_missing_atom=0, n_fail=0, fail_by_eq={'바-1': 0, '바-2': 0, '바-3': 0},
               n_discriminating=0, by_flag={'0': dict(n_stick_both=0, n_fail=0, n_dm_differ=0), '1': dict(n_stick_both=0, n_fail=0, n_dm_differ=0)},
               worst=None, kappa_over_kt=None)
    if not (B['ok'] and C['ok'] and atoms['ok']):
        out['why'] = (B['problems'][:2] + C['problems'][:2] + atoms['problems'][:2]) or ['읽기 실패']
        return out
    if LAYOUT[B['ncol']]['sh'] is None:
        out['why'] = ['이력 열 없음']
        return out
    box = C['box_xy']
    worst, kap = (0.0, None), []
    for k in sorted(set(B['by_key']) & set(C['by_key'])):
        out['n_common'] += 1
        vb, vc = B['by_key'][k]['v'], C['by_key'][k]['v']
        ai, aj = atoms['by_id'].get(k[0]), atoms['by_id'].get(k[1])
        fl = '1' if vc[8] != 0.0 else '0'
        if ai is None or aj is None:
            out['n_missing_atom'] += 1
            continue
        if vb[21] != vc[21]:
            out['n_dm_differ'] += 1
            out['by_flag'][fl]['n_dm_differ'] += 1
            continue
        k_t = kt(mat, ai[0], aj[0], ai[1][9], aj[1][9])
        en, _r, _d = _en(vc, box)
        Fb, Fc, Fnb, Fnc, Ftb, Ftc = vb[9:12], vc[9:12], vb[12:15], vc[12:15], vb[15:18], vc[15:18]
        sb, sc = vb[22:25], vc[22:25]
        Fn = _dot(Fc, en)
        lim = mat['mu'][(ai[0], aj[0])] * abs(Fn)

        def cls(s):
            x = k_t * _nrm(s)
            return 'stick' if x <= (1 - MARGIN) * lim else ('slip' if x > (1 + MARGIN) * lim else 'boundary')
        cb, cc = cls(sb), cls(sc)
        if 'boundary' in (cb, cc):
            out['n_boundary'] += 1
            continue
        if 'slip' in (cb, cc):
            out['n_slip_any'] += 1
            if cb == cc == 'slip':
                out['n_slip_both'] += 1
                on = all(abs(_nrm(_sub(F, [Fn * e for e in en])) - lim) <= CIRCLE_REL * lim for F in (Fb, Fc))
                out['n_slip_both_on_circle'] += int(on)
            continue
        out['n_stick_both'] += 1
        out['by_flag'][fl]['n_stick_both'] += 1
        dF, ds, dFn, dFt = _sub(Fb, Fc), _sub(sb, sc), _sub(Fnb, Fnc), _sub(Ftb, Ftc)
        nds = _dot(en, ds)
        E = E_REL * k_t * _nrm(ds) + E_ABS_K * EPS * (_nrm(Fb) + _nrm(Fc) + k_t * _nrm(sb) + k_t * _nrm(sc))
        r1 = _nrm([dF[c] + k_t * ds[c] for c in range(3)])
        r2 = _nrm([dFn[c] + k_t * nds * en[c] for c in range(3)])
        r3 = _nrm([dFt[c] + k_t * (ds[c] - nds * en[c]) for c in range(3)])
        fails = [q for q, rr in (('바-1', r1), ('바-2', r2), ('바-3', r3)) if not rr <= E]
        for q in fails:
            out['fail_by_eq'][q] += 1
        if fails:
            out['n_fail'] += 1
            out['by_flag'][fl]['n_fail'] += 1
        rat = max(r1, r2, r3) / E if E > 0 else math.inf
        if rat > worst[0]:
            worst = (rat, dict(key=list(k), r=[r1, r2, r3], E=E, kt=k_t))
        if _nrm(_sub(dFt, dF)) > E:
            out['n_discriminating'] += 1
        if _dot(ds, ds) > 0:
            kap.append(-_dot(dF, ds) / _dot(ds, ds) / k_t)
    out['worst'] = worst[1]
    if kap:
        out['kappa_over_kt'] = dict(n=len(kap), min=min(kap), median=statistics.median(kap), max=max(kap))
    if out['n_stick_both'] == 0:
        out['status'], out['why'] = '해당 없음', ['양쪽 고착 쌍 0 — 가르지 못함']
    else:
        out['status'] = '맞음' if out['n_fail'] == 0 else '틀림'
        if out['n_fail']:
            out['why'].append(f'E 밖 고착 쌍 {out["n_fail"]} / {out["n_stick_both"]} ({out["fail_by_eq"]})')
    if out['n_discriminating'] == 0 and out['n_stick_both']:
        out['note'] = '판별력 없음 — 옛 연쇄등식 (ΔF_t,dump = ΔF) 과 사영식을 이 침대에서 가르지 못함 (틀림 아님)'
    return out


def _eq_ulp(a, b):
    m = max(abs(a), abs(b))
    return abs(a - b) <= ULP_K * EPS * m


def exc1(D, ANm1, AN):
    """예외 ① deltaMax 올림 (normal_model_hooke_hysteresis.h 156–158 · 조건 없음) — (a) 모든 setup 덤프 deltaMax ≥ delta ·
    (b) 주기 파일 쪽 (B · B2 · BW): A(N−1) 에도 있는 쌍마다 deltaMax = max(A(N−1) deltaMax, 그 쌍 delta) · (c) 명령 · 왕복 둘째 쪽 = 바뀐 쌍 0."""
    out = dict(status='계산 못 함', why=[], viol_a={}, exact_a={}, viol_b={}, exact_b={}, n_raise={}, changed_c={},
               n_raise_periodic_side=None, n_cohesion_guarded_A=None, cohesion_keys=[])
    need = [D[a] for a in SETUP_ARMS] + [ANm1, AN]
    if not all(x['ok'] for x in need):
        out['why'] = ['읽기 실패: ' + ', '.join(a for a in SETUP_ARMS if not D[a]['ok'])] + ([] if ANm1['ok'] and AN['ok'] else ['A 덤프'])
        return out
    for a in SETUP_ARMS:
        va = ex = 0
        for k, e in D[a]['by_key'].items():
            dm, dl = e['v'][21], e['v'][26]
            if dm < dl:
                ex += 1
                if not _eq_ulp(dm, dl):
                    va += 1
        out['viol_a'][a], out['exact_a'][a] = va, ex
    for a in PERIODIC_SIDE:
        vb = exb = nr = 0
        for k, e in D[a]['by_key'].items():
            if k not in ANm1['by_key']:
                continue
            old = ANm1['by_key'][k]['v'][21]
            want = max(old, e['v'][26])
            if e['v'][21] != want:
                exb += 1
                if not _eq_ulp(e['v'][21], want):
                    vb += 1
            nr += int(e['v'][21] != old)
        out['viol_b'][a], out['exact_b'][a], out['n_raise'][a] = vb, exb, nr
    for x, y, lab in (('C', None, 'C↔A(N)'), ('CW', None, 'CW↔A(N)'), ('BR', 'BW', 'BR↔BW'), ('CR', 'CW', 'CR↔CW')):
        X = D[x]['by_key']
        Y = AN['by_key'] if y is None else D[y]['by_key']
        out['changed_c'][lab] = sum(1 for k in set(X) & set(Y) if X[k]['v'][21] != Y[k]['v'][21])
    coh = [list(k) for k, e in AN['by_key'].items() if k in ANm1['by_key']
           and not _eq_ulp(e['v'][21], max(ANm1['by_key'][k]['v'][21], e['v'][26]))]
    out['n_cohesion_guarded_A'], out['cohesion_keys'] = len(coh), coh[:10]
    out['n_raise_periodic_side'] = out['n_raise'].get('B')
    w = out['why']
    if any(out['viol_a'].values()):
        w.append(f'(a) deltaMax < delta 쌍 {out["viol_a"]}')
    if any(out['viol_b'].values()):
        w.append(f'(b) 주기 파일 쪽 deltaMax ≠ max(A(N−1), delta) {out["viol_b"]}')
    if any(out['changed_c'].values()):
        w.append(f'(c) 바뀐 쌍 {out["changed_c"]}')
    out['status'] = '맞음' if not w else '틀림'
    return out


def exc2(D, ANm1, AN):
    """예외 ② 이웃 재구성 (neigh_gran.cpp 587–615) — 새 쌍 (A(N−1) 덤프에 없던 setup 쌍) 을 shear 0 / 0 아님 으로 · 사라진 쌍 수 ·
    shear 0 인 새 쌍은 deltaMax = delta (0 에서 올림) · 새 쌍도 왕복 같음 (BW ↔ BR · CW ↔ CR)."""
    out = dict(status='계산 못 함', why=[], n_new=None, n_new_zero=None, n_new_restored=None, n_gone=None, n_gone_B=None,
               viol_new_zero_dm=None, n_new_rt_differ=None, new_keys=[])
    if not all(x['ok'] for x in (D['B'], D['BW'], D['BR'], D['CW'], D['CR'], ANm1, AN)):
        out['why'] = ['읽기 실패']
        return out
    Bk, Pk = D['B']['by_key'], ANm1['by_key']
    new = sorted(set(Bk) - set(Pk))
    zero = [k for k in new if Bk[k]['v'][22:25] == [0.0, 0.0, 0.0]]
    out.update(n_new=len(new), n_new_zero=len(zero), n_new_restored=len(new) - len(zero), new_keys=[list(k) for k in new[:10]],
               n_gone=len(set(Pk) - set(AN['by_key'])), n_gone_B=len(set(Pk) - set(Bk)))
    out['viol_new_zero_dm'] = sum(1 for k in zero if not _eq_ulp(Bk[k]['v'][21], Bk[k]['v'][26]))
    nd = 0
    for x, y in (('BW', 'BR'), ('CW', 'CR')):
        X, Y = D[x]['by_key'], D[y]['by_key']
        for k in new:
            if k in X and k in Y and X[k]['v'] != Y[k]['v']:
                nd += 1
            elif (k in X) != (k in Y):
                nd += 1
    out['n_new_rt_differ'] = nd
    if out['viol_new_zero_dm']:
        out['why'].append(f'shear 0 인 새 쌍 중 deltaMax ≠ delta {out["viol_new_zero_dm"]}')
    if nd:
        out['why'].append(f'새 쌍 왕복 다름 {nd}')
    if out['n_gone'] != out['n_gone_B']:
        out['why'].append(f'사라진 쌍 수 A {out["n_gone"]} ≠ B {out["n_gone_B"]}')
    out['status'] = '맞음' if not out['why'] else '틀림'
    return out


def wall_scale(atoms, mat):
    """예외 ③ 바닥 primitive 벽 — 규모만 (벽 이력 = 원자별 · 쌍 · 원자 덤프 열에 없음 → 이 대조가 보지 않는다)."""
    out = dict(n_atoms=None, n_wall_touch=None, n_wall_near=None, note='벽 이력은 덤프에 없다 — 쌍 30 열 · 원자 12 열 일치 = 벽 이력 인증 아님')
    if not atoms['ok']:
        out['why'] = atoms['problems'][:2]
        return out
    t = n = 0
    for _id, (_ty, v) in atoms['by_id'].items():
        gap = (v[2] - mat['wall_z']) - v[9]
        if gap <= 0:
            t += 1
        elif gap <= mat['skin']:
            n += 1
    out.update(n_atoms=len(atoms['by_id']), n_wall_touch=t, n_wall_near=n)
    return out


def _cmp_groups(X, Y, keys, names):
    lay = LAYOUT[30]
    gd = dict(_groups(lay))
    cnt = {g: 0 for g in names}
    for k in keys:
        a, b = X[k], Y[k]
        for g in names:
            if g == 'torque' and a['flipped'] != b['flipped']:
                continue
            if any(a['v'][c] != b['v'][c] for c in gd[g]):
                cnt[g] += 1
    return cnt


def pred_ma(D, AT, ANm1, AN, coh_keys):
    """마 [내용] B ↔ C (둘 다 setup · 같은 x · v · ω)."""
    res = {}
    if not all(x['ok'] for x in (D['B'], D['C'], ANm1, AN, AT['B'], AT['C'])):
        bad = dict(status='계산 못 함', why=['읽기 실패'])
        return {'마-1': dict(bad), '마-2': dict(bad), '마-3': dict(bad)}
    Bk, Ck, Pk, Nk = D['B']['by_key'], D['C']['by_key'], ANm1['by_key'], AN['by_key']
    coh = {tuple(k) for k in coh_keys}
    common = sorted(set(Bk) & set(Ck))
    names = ['pos', 'flag', 'contactArea', 'delta', 'contactPoint']
    cnt = _cmp_groups(Bk, Ck, common, names)
    cnt['deltaMax'] = sum(1 for k in common if k not in coh and Bk[k]['v'][21] != Ck[k]['v'][21])
    av = atoms_value(AT['B'], AT['C'])
    w = []
    if set(Bk) != set(Ck):
        w.append(f'쌍 집합 다름 ({len(set(Bk) - set(Ck))} · {len(set(Ck) - set(Bk))})')
    if any(cnt.values()):
        w.append(f'다른 쌍 {cnt}')
    if not av['equal']:
        w.append('원자 ' + '; '.join(av['why']))
    res['마-1'] = dict(status='맞음' if not w else '틀림', why=w, n_common=len(common), differ=cnt, n_cohesion_excluded=len(coh & set(common)),
                      atoms=dict(n=av.get('n_common'), n_differ=av.get('n_differ')))
    K = sorted(set(Bk) & set(Ck) & set(Pk) & set(Nk))
    vb = sum(1 for k in K if Bk[k]['v'][22:25] != Pk[k]['v'][22:25])
    vc = sum(1 for k in K if Ck[k]['v'][22:25] != Nk[k]['v'][22:25])
    sBC = {k for k in K if Bk[k]['v'][22:25] != Ck[k]['v'][22:25]}
    sA = {k for k in K if Pk[k]['v'][22:25] != Nk[k]['v'][22:25]}
    w = []
    if vb:
        w.append(f'B shear ≠ A(N−1) {vb}')
    if vc:
        w.append(f'C shear ≠ A(N) {vc}')
    if sBC != sA:
        w.append(f'B≠C 집합 ({len(sBC)}) ≠ A(N−1)≠A(N) 집합 ({len(sA)})')
    res['마-2'] = dict(status='맞음' if not w else '틀림', why=w, n_keys=len(K), n_set_BC=len(sBC), n_set_A=len(sA),
                      n_B_ne_Anm1=vb, n_C_ne_AN=vc, n_new=len(set(Bk) - set(Pk)))
    cN = sorted(set(Ck) & set(Nk))
    all_names = [g for g, _ in _groups(LAYOUT[30])]
    f0 = [k for k in cN if Ck[k]['v'][8] == 0.0]
    f1 = [k for k in cN if Ck[k]['v'][8] != 0.0]
    c0 = _cmp_groups(Ck, Nk, f0, all_names)
    n0 = sum(1 for k in f0 if any(n for n in _cmp_groups(Ck, Nk, [k], all_names).values()))
    force_g = ['force', 'force_normal', 'force_tangential']
    n1f = sum(1 for k in f1 if any(n for n in _cmp_groups(Ck, Nk, [k], force_g).values()))
    other = [g for g in all_names if g not in force_g + ['torque']]
    n1o = sum(1 for k in f1 if any(n for n in _cmp_groups(Ck, Nk, [k], other).values()))
    w = []
    if set(Ck) != set(Nk):
        w.append('C ↔ A(N) 쌍 집합 다름')
    if n0:
        w.append(f'주기 표지 0 쌍 다름 {n0} ({ {g: n for g, n in c0.items() if n} })')
    if n1o:
        w.append(f'주기 표지 1 쌍의 힘 · 토크 밖 열 다름 {n1o}')
    res['마-3'] = dict(status='맞음' if not w else '틀림', why=w, n_flag0=len(f0), n_flag0_differ=n0, n_flag1=len(f1),
                      n_flag1_force_differ=n1f, n_flag1_other_differ=n1o)
    return res


def pred_sa(D, AN):
    """사 [이력] C · CW 이력 4 열 ↔ A(N) (공통 쌍 · 정확)."""
    if not all(x['ok'] for x in (D['C'], D['CW'], AN)):
        return dict(status='계산 못 함', why=['읽기 실패'])
    Nk, w, det = AN['by_key'], [], {}
    for a in ('C', 'CW'):
        X = D[a]['by_key']
        nd = sum(1 for k in set(X) & set(Nk) if X[k]['v'][21:25] != Nk[k]['v'][21:25])
        det[a] = dict(n_common=len(set(X) & set(Nk)), n_differ=nd, same_set=set(X) == set(Nk))
        if nd:
            w.append(f'{a} 이력 다른 쌍 {nd}')
        if set(X) != set(Nk):
            w.append(f'{a} ↔ A(N) 쌍 집합 다름')
    return dict(status='맞음' if not w else '틀림', why=w, detail=det)


def _ref_tables(ref):
    rin = read_md5_list(os.path.join(ref, 'inputs.md5')) if ref else []
    rout = dict((n, h) for h, n in read_md5_list(os.path.join(ref, 'outputs.md5'))) if ref else {}
    return (rin[0][0] if rin else None), dict((n, h) for h, n in rin), rout


def _decks_same(O, rin):
    oin = dict((n, h) for h, n in read_md5_list(os.path.join(O, 'inputs.md5')))
    return all(oin.get(d) is not None and oin.get(d) == rin.get(d) for d in DECKS7), oin


def pred_ga(O, N, ref, ident):
    """가 — 11-04 다섯 팔 출력 md5 (run_40000/outputs.md5) · 판정 조건 = 같은 실행 파일 md5 ∧ 덱 일곱 md5 ∧ N = 40000."""
    rlmp, rin, rout = _ref_tables(ref)
    same_decks, _ = _decks_same(O, rin)
    same_lmp = bool(rlmp) and ident.get('lmp_md5') == rlmp
    eq, ne, absent = [], [], []
    for name, h in sorted(rout.items()):
        p = os.path.join(O, name)
        if not os.path.isfile(p):
            absent.append(name)
        elif md5(p) == h:
            eq.append(name)
        else:
            ne.append(name)
    det = dict(n_ref=len(rout), n_equal=len(eq), differ=ne[:15], absent=absent[:15], same_lmp=same_lmp, same_decks=same_decks,
               ref_lmp_md5=rlmp, lmp_md5=ident.get('lmp_md5'))
    if not rout:
        return dict(status='계산 못 함', why=['11-04 출력 기록 없음'], **det)
    if not (same_lmp and same_decks and N == REF_N):
        why = [x for x, c in (('실행 파일 md5 다름', not same_lmp), ('덱 md5 다름', not same_decks), (f'N ≠ {REF_N}', N != REF_N)) if c]
        return dict(status='해당 없음', why=why + [f'관찰만: 같은 파일 {len(eq)} / {len(rout)}'], **det)
    return dict(status='맞음' if len(eq) == len(rout) else '틀림', why=[] if len(eq) == len(rout) else [f'다른 파일 {ne + absent}'], **det)


def pred_na(O, N):
    """나 [재생] B ↔ BW 쌍 · 원자 덤프 바이트 같음 (보조 = B ↔ B2 · A · A2 주기 파일 md5)."""
    c = lambda a: os.path.join(O, a, 'post', 'c_%d.txt' % N)
    t = lambda a: os.path.join(O, a, 'post', 'atom_%d.txt' % N)
    if not all(os.path.isfile(p) for p in (c('B'), c('BW'), t('B'), t('BW'))):
        return dict(status='계산 못 함', why=['B · BW 덤프 없음'])
    pe, ae = file_bytes_equal(c('B'), c('BW')), file_bytes_equal(t('B'), t('BW'))
    ra, rb = os.path.join(O, 'A', 'rst', 'restart_%d.bin' % N), os.path.join(O, 'A2', 'rst', 'restart_%d.bin' % N)
    aux = dict(restart_A_eq_A2=file_bytes_equal(ra, rb), B_eq_B2_pairs=file_bytes_equal(c('B'), c('B2')),
               B_eq_B2_atoms=file_bytes_equal(t('B'), t('B2')))
    w = [x for x, ok in (('쌍 덤프 바이트 다름', pe), ('원자 덤프 바이트 다름', ae)) if not ok]
    return dict(status='맞음' if not w else '틀림', why=w, pairs_equal=pe, atoms_equal=ae, aux=aux)


def pred_round(O, N, D, AT, x, y):
    """[왕복] x (D1) ↔ y (D2) — 값 · 바이트 따로."""
    pv, av = pairs_value(D[x], D[y]), atoms_value(AT[x], AT[y])
    cpx, cpy = os.path.join(O, x, 'post', 'c_%d.txt' % N), os.path.join(O, y, 'post', 'c_%d.txt' % N)
    apx, apy = os.path.join(O, x, 'post', 'atom_%d.txt' % N), os.path.join(O, y, 'post', 'atom_%d.txt' % N)
    if not (pv['computed'] and av['computed']):
        bad = dict(status='계산 못 함', why=pv['why'] + av['why'])
        return dict(bad), dict(bad)
    w = list(pv['why']) + ['원자 ' + s for s in av['why']]
    val = dict(status='맞음' if not w else '틀림', why=w, pairs={k: pv[k] for k in ('n1', 'n2', 'n_common', 'only1', 'only2',
               'orientation_differs', 'dup1', 'dup2', 'n_pairs_differ', 'by_group')},
               atoms={k: av.get(k) for k in ('n_common', 'only1', 'only2', 'n_differ')})
    pe, ae = file_bytes_equal(cpx, cpy), file_bytes_equal(apx, apy)
    wb = [s for s, ok in (('쌍 덤프 바이트 다름', pe), ('원자 덤프 바이트 다름', ae)) if not ok]
    byt = dict(status='맞음' if not wb else '틀림', why=wb, pairs_equal=pe, atoms_equal=ae)
    return val, byt


def pred_ra_repro(O, N, ref, ident):
    """라-재현 (Q6-2 따로) — (가) 새 C ↔ 새 CW 바이트 · (나) 새 C · CW ↔ 11-04 C md5 (같은 실행 파일 ∧ 같은 명령 파일 ∧ 덱 일곱 ∧ N 40000)."""
    c = lambda a: os.path.join(O, a, 'post', 'c_%d.txt' % N)
    t = lambda a: os.path.join(O, a, 'post', 'atom_%d.txt' % N)
    if not all(os.path.isfile(p) for p in (c('C'), c('CW'), t('C'), t('CW'))):
        bad = dict(status='계산 못 함', why=['C · CW 덤프 없음'])
        return dict(bad), dict(bad)
    pe, ae = file_bytes_equal(c('C'), c('CW')), file_bytes_equal(t('C'), t('CW'))
    w = [s for s, ok in (('쌍 덤프 바이트 다름', pe), ('원자 덤프 바이트 다름', ae)) if not ok]
    ga = dict(status='맞음' if not w else '틀림', why=w, pairs_equal=pe, atoms_equal=ae)
    rlmp, rin, rout = _ref_tables(ref)
    same_decks, _ = _decks_same(O, rin)
    cmd = os.path.join(O, 'A2', 'rst', 'restart_cmd.bin')
    rc_ = rout.get('C/post/c_%d.txt' % REF_N)
    ra_ = rout.get('C/post/atom_%d.txt' % REF_N)
    same_lmp = bool(rlmp) and ident.get('lmp_md5') == rlmp
    same_cmd = os.path.isfile(cmd) and rout.get('A2/rst/restart_cmd.bin') == md5(cmd)
    det = dict(same_lmp=same_lmp, same_cmd_file=same_cmd, same_decks=same_decks, ref_C_md5=rc_)
    if not (rc_ and ra_):
        na = dict(status='계산 못 함', why=['11-04 C md5 기록 없음'], **det)
    elif not (same_lmp and same_cmd and same_decks and N == REF_N):
        why = [x for x, cnd in (('실행 파일 md5 다름', not same_lmp), ('명령 파일 md5 다름', not same_cmd), ('덱 md5 다름', not same_decks),
                                (f'N ≠ {REF_N}', N != REF_N)) if cnd]
        na = dict(status='해당 없음', why=why, **det)
    else:
        ok = md5(c('C')) == rc_ and md5(c('CW')) == rc_ and md5(t('C')) == ra_ and md5(t('CW')) == ra_
        na = dict(status='맞음' if ok else '틀림', why=[] if ok else ['C · CW md5 ≠ 11-04 C'], **det)
    return ga, na


def report_a(AN, ANm1, atomsA, mat):
    """아 보고 — Δs = A(N) shear − A(N−1) shear ↔ v_tr(N)·dt (A 의 원자 덤프 v · ω · 회전 사영) · 값 미리 안 정함 · 꼴만."""
    if not (AN['ok'] and ANm1['ok'] and atomsA['ok']):
        return dict(status='계산 못 함')
    box, dt = AN['box_xy'], mat['dt']
    obs, mod, rel = [], [], []
    for k in sorted(set(AN['by_key']) & set(ANm1['by_key'])):
        v, p = AN['by_key'][k]['v'], ANm1['by_key'][k]['v']
        ai, aj = atomsA['by_id'].get(k[0]), atomsA['by_id'].get(k[1])
        if ai is None or aj is None:
            continue
        en, r, d = _en(v, box)
        ri, rj = ai[1][9], aj[1][9]
        dn = (ri + rj) - r
        vr = _sub(ai[1][3:6], aj[1][3:6])
        vn = _dot(vr, en)
        vt = [vr[c] - vn * en[c] for c in range(3)]
        cri, crj = ri - 0.5 * dn, rj - 0.5 * dn
        wr = [(cri * ai[1][6 + c] + crj * aj[1][6 + c]) / r for c in range(3)]
        vtr = [vt[0] - (d[2] * wr[1] - d[1] * wr[2]), vt[1] - (d[0] * wr[2] - d[2] * wr[0]), vt[2] - (d[1] * wr[0] - d[0] * wr[1])]
        u = [p[22 + c] + vtr[c] * dt for c in range(3)]
        rs = _dot(u, en)
        dm_ = [vtr[c] * dt - rs * en[c] for c in range(3)]
        do = _sub(v[22:25], p[22:25])
        obs += do
        mod += dm_
        if _nrm(do) > 0:
            rel.append(_nrm(_sub(do, dm_)) / _nrm(do))
    if not obs:
        return dict(status='보고', n=0)
    smm = sum(m * m for m in mod)
    slope = sum(o * m for o, m in zip(obs, mod)) / smm if smm > 0 else None
    mo = sum(obs) / len(obs)
    sst = sum((o - mo) ** 2 for o in obs)
    r2 = (1 - sum((o - slope * m) ** 2 for o, m in zip(obs, mod)) / sst) if (slope is not None and sst > 0) else None
    return dict(status='보고', n=len(obs) // 3, slope=slope, r2=r2, median_rel=statistics.median(rel) if rel else None,
                note='A 의 in-run 증분은 반 step 속도 (v(N−½)) 로 계산 · 여기 모형은 덤프의 v(N) — 판정 아님')


def report_yeonsok(AN, D):
    """[연속] 보고 — 원 런 스텝 끝 덤프 A(N) ↔ setup 덤프 (B · C) · 옛 식 (키트 26 열 · 이력 빼고) · 같다고 주장하지 않는다."""
    out = {}
    for a in ('B', 'C'):
        if not (AN['ok'] and D[a]['ok']):
            out[a] = dict(status='계산 못 함')
            continue
        j = judge(AN, D[a], mode='kit26')
        pv = pairs_value(AN, D[a])
        bg = pv.get('by_group', {})
        keys = sorted(set(AN['by_key']) & set(D[a]['by_key']))
        nfd = sum(1 for k in keys if any(AN['by_key'][k]['v'][c] != D[a]['by_key'][k]['v'][c] for c in range(9, 18)))
        out[a] = dict(judge_kit26=j['status'], n_mismatch=j.get('n_mismatch'), n_pairs_force_differ=nfd, by_group=bg)
    return out


def compare_all(O, N, here=HERE, ref=None):
    """→ (결과 dict, rc) · OUT 이 있으면 OUT/compare_g2cp.json 을 쓴다."""
    ref = ref if ref is not None else os.path.join(here, 'run_40000')
    res = dict(N=N, out=O, here=here, ref=ref, predictions={}, judgment={}, exceptions={}, reports={},
               thresholds=dict(REL=REL, MARGIN=MARGIN, E_REL=E_REL, E_ABS_K=E_ABS_K, ULP_K=ULP_K, CIRCLE_REL=CIRCLE_REL),
               memo='docs/reviews/p1_g2c_compare_definition_20261105.md §0 (11-10 개정 · 결과 전)')
    P = res['predictions']
    if not os.path.isdir(O):
        P['입력'] = dict(status='계산 못 함', why=[f'OUT 없음: {O}'])
        return res, 2
    ident = read_kv(os.path.join(O, 'lmp_identity.txt'))
    res['lmp'] = ident
    c = lambda a: os.path.join(O, a, 'post', 'c_%d.txt' % N)
    D = {a: read_local(c(a)) for a in ARMS}
    AT = {a: read_atoms(os.path.join(O, a, 'post', 'atom_%d.txt' % N)) for a in ARMS}
    ANm1 = read_local(os.path.join(O, 'A', 'post', 'cpre_%d.txt' % (N - 1)))
    AN = D['A']
    try:
        mat = material(here)
        res['material'] = {k: (v if not isinstance(v, dict) else {str(kk): vv for kk, vv in v.items()}) for k, v in mat.items()}
    except (OSError, ValueError) as e:
        mat = None
        res['material'] = dict(error=str(e))

    def guard(name, fn):
        try:
            return fn()
        except Exception as e:   # noqa: BLE001 — 한 예측의 예외 = 그 예측 '계산 못 함' (다른 예측은 그대로)
            return dict(status='계산 못 함', why=[f'{name}: {type(e).__name__}: {e}'])

    P['가'] = guard('가', lambda: pred_ga(O, N, ref, ident))
    P['나'] = guard('나', lambda: pred_na(O, N))
    for lab, x, y in (('다', 'BW', 'BR'), ('라', 'CW', 'CR')):
        try:
            v, b = pred_round(O, N, D, AT, x, y)
        except Exception as e:   # noqa: BLE001
            v = b = dict(status='계산 못 함', why=[f'{type(e).__name__}: {e}'])
        P[lab + '-값'], P[lab + '-바이트'] = v, b
        res['judgment'][lab] = judge(D[x], D[y], expected_step=N, mode='g2cp')
    try:
        ga, na = pred_ra_repro(O, N, ref, ident)
    except Exception as e:   # noqa: BLE001
        ga = na = dict(status='계산 못 함', why=[f'{type(e).__name__}: {e}'])
    P['라-재현가'], P['라-재현나'] = ga, na
    e1 = guard('예외①', lambda: exc1(D, ANm1, AN))
    coh = e1.get('cohesion_keys', []) if isinstance(e1, dict) else []
    ma = guard('마', lambda: pred_ma(D, AT, ANm1, AN, coh))
    if 'status' in ma:          # 예외 — 세 칸 모두 '계산 못 함'
        ma = {k: dict(ma) for k in ('마-1', '마-2', '마-3')}
    P.update(ma)
    if mat is None:
        P['바'] = dict(status='계산 못 함', why=['덱 물성 읽기 실패: ' + res['material'].get('error', '')])
    else:
        P['바'] = guard('바', lambda: pred_ba(D['B'], D['C'], AT['C'], mat))
    P['사'] = guard('사', lambda: pred_sa(D, AN))
    P['예외①'] = e1
    e2 = guard('예외②', lambda: exc2(D, ANm1, AN))
    P['예외②'] = e2
    res['exceptions']['①'] = e1
    res['exceptions']['②'] = e2
    res['exceptions']['③'] = wall_scale(AT['BW'], mat) if mat else dict(why=['덱 물성 없음'])
    res['reports']['아'] = guard('아', lambda: report_a(AN, ANm1, AT['A'], mat)) if mat else dict(status='계산 못 함')
    res['reports']['연속'] = guard('연속', lambda: report_yeonsok(AN, D))
    for k in ('마-1', '마-2', '마-3'):
        P.setdefault(k, dict(status='계산 못 함', why=['마 계산 실패']))
    rc = 2 if any(isinstance(v, dict) and v.get('status') == '계산 못 함' for v in P.values()) else 0
    res['rc'] = rc
    with open(os.path.join(O, 'compare_g2cp.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=str)
        f.write('\n')
    return res, rc


def _line(name, p):
    st = p.get('status', '?')
    why = '; '.join(str(x) for x in (p.get('why') or [])[:2])
    return f'{name:<10} {st:<6} {why}'[:220]


def main(argv):
    if len(argv) != 3 or not re.fullmatch(r'[1-9][0-9]{0,8}', argv[2]):
        print('사용: python3 -I compare_g2cp.py OUT N', file=sys.stderr)
        return 2
    O, N = argv[1], int(argv[2])
    res, rc = compare_all(O, N)
    for name, p in res['predictions'].items():
        print(_line(name, p))
    for lab, j in res.get('judgment', {}).items():
        print(f'판정 {lab:<5} {j.get("status")} (n_mismatch {j.get("n_mismatch")} · 비트 같은 쌍 {j.get("n_bit_equal")}/{j.get("n_ref")})')
    e = res.get('exceptions', {})
    if e:
        e1, e2, e3 = e.get('①', {}), e.get('②', {}), e.get('③', {})
        print(f'예외 ① 올림 쌍 (B) {e1.get("n_raise_periodic_side")} · cohesion 가드 (A) {e1.get("n_cohesion_guarded_A")}')
        print(f'예외 ② 새 쌍 {e2.get("n_new")} (shear 0 {e2.get("n_new_zero")} · 복원 {e2.get("n_new_restored")}) · 사라진 쌍 {e2.get("n_gone")}')
        print(f'예외 ③ 바닥 닿음 {e3.get("n_wall_touch")} · 근처 {e3.get("n_wall_near")} — {e3.get("note", "")}')
    print(f'rc {rc} · JSON {os.path.join(O, "compare_g2cp.json") if os.path.isdir(O) else "(OUT 없음)"}')
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv))
