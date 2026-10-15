#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K7 — 복원 관문 비교기 (REG §3-2 · §12-1 · CX1 Q1 · CX2 §5).  표준 라이브러리만 · 읽기 전용.

    python3 ul_gates.py --selftest
    python3 ul_gates.py g0 <원 마지막 조각 덱> <언로딩 덱> [--arm-dt]          # G0 (실행 전 · ibb 에서 원 덱 사본으로)
    python3 ul_gates.py g2 <시험 atom_S0> <원 atom_S0>                         # G2 원자 (id 정렬 · 글자 그대로)
    python3 ul_gates.py g2c <시험 contact_S0> <원 contact_S0>                  # G2c 쌍 접촉 (무순서 키 · 방향 · 주기 정규화)

G0  원 덱이 S0 (마지막 run 안) 에 켜 둔 정의 ↔ 언로딩 덱 머리 (read_restart ~ 첫 run 앞) 의 정의 — fix · compute · pair · 일반 설정 ·
    timestep (변수 풀어서) · fix 순서 (동역학 fix) · fix_modify.  다른 줄 = 위반.  명시 허용목록 (ALLOWED) 만 통과:
    출력 (dump 경로 · 주기 · 열 · thermo · restart) · 판 STL 경로 (메시 자료는 restart 에서) · 새 관측 compute / fix (ul_ 접두 · ave/time) ·
    원 덱의 관측 전용 compute (zmax — r2 꼴 · 정착 높이) 없음 · 등록된 팔 dt (UT · UVb — read_restart 뒤 timestep).
    ⚠ 초기 정착 중력 98.1 · 압축 감쇠 0.5 를 복제하면 위반 (§12-1 · CX1 Q1(e) — "마지막 정의" 를 본다).
G1  재개 첫 setup 줄 (step = S0 · 원자 수 = 원 로그 · KE 상대 1e-6) — 표의 G1 줄 (재개 절차 그대로).
G2  시험이 다시 쓴 atom_S0 (id 정렬 · id type x y z radius vx vy vz) = 원 atom_S0 글자 그대로 · mesh_S0 md5 = 원.
    omega 는 원 덤프에 없다 → "과거 직접 비교 미확보" 로 적고 새 덤프에는 출력한다 (CX2 §6).
G2c 쌍 접촉 (원 덤프 꼴 26 열) — 무순서 키 (작은 id, 큰 id) · 방향 바뀐 행은 힘 부호 · 두 위치를 바꿔서 · 주기 플래그 c_cpl[9] · 토크 제외 ·
    위치는 상자 길이로 감아 대조 (주기 image) · 중복 키 (같은 값 = 수 · 다른 값 = 위반) · 허용폭 |차| ≤ 1e-5 × max(|원 값|, 그 열 |값| 중앙값) ·
    판별력 = 원 덤프의 접선 힘 0 아닌 접촉 몫 (함께 적는다).  = 초기 접촉 힘 재현 검사 (숨은 이력 동일성의 단독 증명 아님 · §12-1).
G3  첫 정규 thermo 줄: 원자 수 + 판 압력 5 % (원 로그의 같은 step 줄).
판 z  창 끝 mesh 덤프 꼭짓점 ↔ 덱 공식 (≤ 1e-6 덱 m · 넘으면 TECH).
S0′  10:0 연장 — S0′ ± 5,000 정규 줄 각각 ↔ 그 런 마지막 25 줄 평균 1 % (§11-2 awk 와 같은 셈) · KE 기준 = 5 줄 창 평균 다섯의 중앙값.
복원 판정 (§12-1 ⑤): RESTORED · UNCONFIRMED · SYNTAX_FAIL · VALUE_MISMATCH — RESTORED 일 때만 U.
"""
from __future__ import annotations

import hashlib
import math
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ul_lib  # noqa: E402

SETTINGS = ('atom_style', 'atom_modify', 'boundary', 'newton', 'soft_particles', 'communicate', 'units', 'processors', 'neighbor',
            'neigh_modify', 'pair_style', 'pair_coeff')
OUTPUT_ONLY = ('thermo', 'thermo_style', 'thermo_modify', 'restart', 'print', 'shell', 'dump', 'dump_modify', 'undump', 'write_dump')
OBSERVER_COMPUTES_ORIG = {'zmax': 'r2 꼴 정착 높이 관측 (compute reduce max z) — 동역학 없음'}
INSERTION_STYLES = ('particletemplate/sphere', 'particledistribution/discrete', 'insert/pack', 'insert/stream', 'insert/rate/region')
OBS_FIX_STYLES = ('ave/time',)


def _subst(line, var):
    """${이름} 을 그 변수의 글자 값으로 (값이 한 낱말 상수일 때만 — 아니면 그대로 둔다)."""
    def rep(m):
        v = var.get(m.group(1))
        return v if v is not None and re.fullmatch(r'[-+0-9.eE]+', v) else m.group(0)
    return re.sub(r'\$\{(\w+)\}', rep, line)


def active_definitions(text, cut='last_run'):
    """덱 → 그 자리 (cut = last_run: 마지막 run 앞 = S0 가 든 이완 run · first_run: 첫 run 앞 = 언로딩 머리) 에서 켜져 있는 정의.
    fix 를 같은 ID 로 다시 정의하면 제자리 교체 (LAMMPS) · unfix 뒤 정의는 끝에 붙는다 (dict 순서 = fix 목록 순서)."""
    L = ul_lib.logical_lines(text)
    runs = [i for i, ln in enumerate(L) if ln.split()[0] == 'run']
    end = (runs[-1] if cut == 'last_run' else runs[0]) if runs else len(L)
    var, st = {}, {'settings': {}, 'fixes': {}, 'fix_modify': {}, 'computes': {}, 'dumps': {}, 'timestep': None, 'output': []}
    for ln in L[:end]:
        w = ul_lib.words(ln)
        c = w[0]
        if c == 'variable' and len(w) >= 4:
            var[w[1]] = w[3] if len(w) == 4 else None
            continue
        w = ul_lib.words(_subst(ln, var))
        if c in SETTINGS:
            st['settings'][c] = ' '.join(w[1:])
        elif c == 'timestep':
            try:
                st['timestep'] = float(w[1])
            except ValueError:
                st['timestep'] = w[1]
        elif c == 'fix' and len(w) >= 4:
            st['fixes'][w[1]] = tuple(w[2:])
        elif c == 'unfix':
            st['fixes'].pop(w[1], None)
            st['fix_modify'].pop(w[1], None)
        elif c == 'fix_modify':
            st['fix_modify'].setdefault(w[1], []).append(' '.join(w[2:]))
        elif c == 'compute':
            st['computes'][w[1]] = tuple(w[2:])
        elif c == 'uncompute':
            st['computes'].pop(w[1], None)
        elif c == 'dump':
            st['dumps'][w[1]] = tuple(w[2:])
        elif c == 'undump':
            st['dumps'].pop(w[1], None)
        elif c in OUTPUT_ONLY:
            st['output'].append(ln)
    return st


def _fix_diff(a, b):
    """두 fix 정의 (group, style, args …) → (같은가, 허용된 차이 설명 | None)."""
    if a == b:
        return True, None
    if len(a) == len(b) and a[1] == b[1] and a[1].startswith('mesh/surface') and 'file' in a:
        i = a.index('file')
        if a[:i + 1] == b[:i + 1] and a[i + 2:] == b[i + 2:]:
            return True, f'판 STL 경로 {a[i + 1]} → {b[i + 1]} (메시 자료는 restart 에서 — 분기 키트 §8)'
    return False, None


def g0_compare(orig_text, unload_text, arm_dt=None):
    A = active_definitions(orig_text, 'last_run')
    B = active_definitions(unload_text, 'first_run')
    viol, allowed = [], []
    for k in SETTINGS:
        if A['settings'].get(k) != B['settings'].get(k):
            viol.append(f'{k}: 원 {A["settings"].get(k)!r} ↔ 언로딩 {B["settings"].get(k)!r}')
    if A['timestep'] != B['timestep']:
        if arm_dt is not None and isinstance(B['timestep'], float) and B['timestep'] == arm_dt:
            allowed.append(f'timestep dt {A["timestep"]} → {B["timestep"]} (등록된 팔 dt · read_restart 뒤)')
        else:
            viol.append(f'timestep: 원 {A["timestep"]} ↔ 언로딩 {B["timestep"]}')
    for fid, a in A['fixes'].items():
        if fid not in B['fixes']:
            if a[1] in INSERTION_STYLES:
                allowed.append(f'fix {fid} ({a[1]}) 없음 — 삽입 템플릿 (동역학 없음)')
            else:
                viol.append(f'fix {fid} ({" ".join(a)}) 가 언로딩 머리에 없다')
            continue
        same, why = _fix_diff(a, B['fixes'][fid])
        if not same:
            viol.append(f'fix {fid}: 원 {" ".join(a)!r} ↔ 언로딩 {" ".join(B["fixes"][fid])!r}')
        elif why:
            allowed.append(why)
    for fid, b in B['fixes'].items():
        if fid in A['fixes']:
            continue
        if fid.startswith('ul_') and b[1] in OBS_FIX_STYLES:
            allowed.append(f'새 관측 fix {fid} ({b[1]})')
        else:
            viol.append(f'새 fix {fid} ({" ".join(b)}) — 머리에 새 동역학 fix 금지 (새 ID 는 언로딩 블록에만)')
    oa = [f for f in A['fixes'] if f in B['fixes']]
    ob = [f for f in B['fixes'] if f in A['fixes']]
    if oa != ob:
        viol.append(f'fix 순서 (힘 합산 순서): 원 {oa} ↔ 언로딩 {ob}')
    for fid in set(A['fix_modify']) | set(B['fix_modify']):
        if fid in A['fixes'] and A['fix_modify'].get(fid) != B['fix_modify'].get(fid):
            viol.append(f'fix_modify {fid}: 원 {A["fix_modify"].get(fid)} ↔ 언로딩 {B["fix_modify"].get(fid)}')
    for cid, a in A['computes'].items():
        if cid not in B['computes']:
            if cid in OBSERVER_COMPUTES_ORIG:
                allowed.append(f'compute {cid} 없음 — {OBSERVER_COMPUTES_ORIG[cid]}')
            else:
                viol.append(f'compute {cid} 가 언로딩 머리에 없다')
        elif a != B['computes'][cid]:
            viol.append(f'compute {cid}: 원 {" ".join(a)!r} ↔ 언로딩 {" ".join(B["computes"][cid])!r}')
    for cid in B['computes']:
        if cid not in A['computes']:
            (allowed if cid.startswith('ul_') else viol).append(f'새 compute {cid} ({" ".join(B["computes"][cid])})'
                                                                + ('' if cid.startswith('ul_') else ' — ul_ 접두가 아니다'))
    if A['dumps'] != B['dumps']:
        allowed.append(f'dump 정의 (출력 경로 · 주기 · 열) — 원 {sorted(A["dumps"])} · 언로딩 {sorted(B["dumps"])}')
    if A['output'] != B['output']:
        allowed.append('thermo · restart · print (출력)')
    return {'status': 'PASS' if not viol else 'FAIL', 'violations': viol, 'allowed': allowed,
            'n_fixes': len(A['fixes']), 'fix_order': oa}


def _ref_fields(line):
    t = line.split()
    return int(t[0]), int(t[1]), float(t[2])


def g1_check(screen_text, g1_line, s0):
    T = ul_lib.parse_thermo(screen_text)
    out = {'status': 'FAIL', 'why': []}
    if not T['setup']:
        out['why'].append('setup 줄 없음')
        return out
    step, row = T['setup'][0]
    rs, ra, rk = _ref_fields(g1_line)
    ke = row.get('KinEng')
    rel = abs(ke / rk - 1.0) if ke is not None and rk else None
    out.update(step=step, atoms=int(row.get('Atoms', -1)), ke=ke, rel=rel)
    if step != s0 or rs != s0:
        out['why'].append(f'setup step {step} ≠ S0 {s0}')
    if int(row.get('Atoms', -1)) != ra:
        out['why'].append(f'원자 {row.get("Atoms")} ≠ {ra}')
    if rel is None or not rel <= 1e-6:
        out['why'].append(f'KE 상대 {rel} > 1e-6')
    out['status'] = 'PASS' if not out['why'] else 'FAIL'
    return out


def g3_check(screen_text, orig_log_text, s0, tol=0.05):
    T = ul_lib.parse_thermo(screen_text)
    O = ul_lib.parse_thermo(orig_log_text)
    out = {'status': 'FAIL', 'why': []}
    after = sorted(s for s in T['regular'] if s > s0)
    if not after:
        out['why'].append('S0 뒤 정규 줄 없음')
        return out
    s = after[0]
    if s not in O['regular']:
        out['why'].append(f'원 로그에 step {s} 정규 줄 없음')
        return out
    a, b = T['regular'][s], O['regular'][s]
    pa, pb = a.get('pressMPa'), b.get('pressMPa')
    rel = abs(pa / pb - 1.0) if pa is not None and pb else None
    out.update(step=s, atoms=(a.get('Atoms'), b.get('Atoms')), press=(pa, pb), rel=rel)
    if a.get('Atoms') != b.get('Atoms'):
        out['why'].append(f'원자 {a.get("Atoms")} ≠ {b.get("Atoms")}')
    if rel is None or not rel <= tol:
        out['why'].append(f'판 압력 상대 {rel} > {tol}')
    out['status'] = 'PASS' if not out['why'] else 'FAIL'
    return out


def _dump_tokens(path, cols):
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    k = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ATOMS'))
    head = lines[k].split()[2:]
    idx = [head.index(c) for c in cols]
    out = {}
    for ln in lines[k + 1:]:
        t = ln.split()
        if len(t) == len(head):
            out[int(t[head.index('id')])] = tuple(t[i] for i in idx)
    return out


def g2_compare(test_atom_path, orig_atom_path, cols=('id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz')):
    out = {'status': 'FAIL', 'why': []}
    try:
        a, b = _dump_tokens(test_atom_path, cols), _dump_tokens(orig_atom_path, cols)
    except (OSError, StopIteration, ValueError) as e:
        out['why'].append(f'덤프 읽기 실패: {type(e).__name__}: {e}')
        return out
    miss, extra = sorted(set(b) - set(a)), sorted(set(a) - set(b))
    bad = [i for i in set(a) & set(b) if a[i] != b[i]]
    out.update(n_atoms=len(b), n_mismatch=len(bad), missing=miss[:10], extra=extra[:10], example=sorted(bad)[:5],
               note='omega 는 원 덤프에 없다 — 과거 직접 비교 미확보 (새 덤프에는 출력)')
    out['status'] = 'PASS' if not (miss or extra or bad) else 'FAIL'
    return out


def mesh_md5_equal(a, b):
    return hashlib.md5(open(a, 'rb').read()).hexdigest() == hashlib.md5(open(b, 'rb').read()).hexdigest()


_POS = (0, 1, 2, 3, 4, 5)
_FORCE = tuple(range(9, 18))
_SYM = (21, 22, 23, 24, 25)


def _contacts(path, box):
    d = ul_lib.read_dump(path, 'local', [f'c_cpl[{i}]' for i in range(1, 27)])
    rows, dup, conflicts = {}, 0, []
    if not d['ok']:   # ULKRF-03 — 파서 · 필수 열 문제 (예: 머리 c_cpl[7] 결손) 를 먼저 돌려준다 → g2c_compare 의 FAIL + 사유 (열을 읽지 않는다 · 채우지 · 지우지 않는다)
        return d, rows, dup, conflicts
    for r in d['rows']:
        v = [r[f'c_cpl[{i}]'] for i in range(1, 27)]
        i, j = ul_lib.exact_id(v[6]), ul_lib.exact_id(v[7])
        if i is None or j is None:   # ULKRR-04 — 쌍 참조 소수 ID 를 정수로 잘라 같은 키로 만들지 않는다
            d['ok'] = False
            d['problems'].append(f'쌍 참조 ID ({v[6]!r} · {v[7]!r}) 가 유한 · 양의 정확한 정수가 아니다')
            continue
        if i > j:
            v = v[3:6] + v[0:3] + v[6:9] + [-x for x in v[9:18]] + v[18:]
        key = (min(i, j), max(i, j))
        if key in rows:
            if all(abs(x - y) <= 1e-12 * max(1.0, abs(x)) for x, y in zip(_cmpvals(rows[key], box), _cmpvals(v, box))):
                dup += 1
            else:
                conflicts.append(key)
            continue
        rows[key] = v
    return d, rows, dup, conflicts


def _wrap(x, L):
    return x % L


def _cmpvals(v, box):
    lx, ly = box
    pos = [_wrap(v[0], lx), _wrap(v[1], ly), v[2], _wrap(v[3], lx), _wrap(v[4], ly), v[5]]
    return pos + list(v[9:18]) + [v[21], v[22], _wrap(v[23], lx), _wrap(v[24], ly), v[25]]


def g2c_compare(test_contact_path, orig_contact_path, box=(0.05, 0.05), rel=1e-5):
    out = {'status': 'FAIL', 'why': []}
    dt, T, dupt, ct = _contacts(test_contact_path, box)
    do, O, dupo, co = _contacts(orig_contact_path, box)
    if not (dt['ok'] and do['ok']):
        out['why'] += dt['problems'][:3] + do['problems'][:3]
        return out
    miss, extra = sorted(set(O) - set(T)), sorted(set(T) - set(O))
    ov = {k: _cmpvals(v, box) for k, v in O.items()}
    tv = {k: _cmpvals(v, box) for k, v in T.items()}
    ncol = len(next(iter(ov.values()))) if ov else 0
    med = [statistics.median(abs(x[c]) for x in ov.values()) for c in range(ncol)] if ov else []
    lengths = [box[0], box[1], None, box[0], box[1], None] + [None] * 9 + [None, None, box[0], box[1], None]
    bad = []
    for k in set(O) & set(T):
        for c, (a, b) in enumerate(zip(ov[k], tv[k])):
            d = abs(a - b)
            if lengths[c]:
                d = min(d, lengths[c] - d)
            if d > rel * max(abs(a), med[c]):
                bad.append((k, c))
                break
    ft = [math.sqrt(sum(O[k][c] ** 2 for c in (15, 16, 17))) for k in O]
    out.update(n_orig=len(O), n_test=len(T), n_mismatch=len(bad), missing=miss[:5], extra=extra[:5], n_dup_consistent=dupt + dupo,
               dup_conflicts=(ct + co)[:5], discriminating_frac=(sum(1 for x in ft if x > 0) / len(ft)) if ft else None,
               note='초기 접촉 힘 재현 검사 — 숨은 이력 동일성의 단독 증명 아님 (§12-1) · 토크 · 주기 플래그 제외')
    out['status'] = 'PASS' if not (miss or extra or bad or ct or co) else 'FAIL'
    return out


def plate_z_check(mesh_paths_and_formula, tol=1e-6):
    out = {'status': 'PASS', 'n': 0, 'max_diff': 0.0, 'bad': []}
    for path, zf in mesh_paths_and_formula:
        try:
            zs = {float(x) for x in re.findall(r'vertex\s+\S+\s+\S+\s+(\S+)', open(path).read())}
        except (OSError, ValueError):
            zs = set()
        out['n'] += 1
        if len(zs) != 1:
            out['bad'].append((path, '평평한 판이 아니다 · 읽기 실패'))
            continue
        d = abs(zs.pop() - zf)
        out['max_diff'] = max(out['max_diff'], d)
        if d > tol:
            out['bad'].append((path, d))
    if out['bad']:
        out['status'] = 'FAIL'
    return out


def s0p_condition(log_text, s0p, window=5000, frac=0.01, tail=25, col_p='pressMPa', col_ke='KinEng'):
    T = ul_lib.parse_thermo(log_text)
    steps = sorted(T['regular'])
    out = {'status': 'NOT_COMPUTED', 'n_window': 0, 'max_rel': None, 'tail_mean': None, 'ke_base': None}
    if not steps or steps[-1] < s0p + window or len(steps) < tail:
        out['why'] = f'정규 줄이 S0′ + {window} 까지 없다 (마지막 {steps[-1] if steps else None})'
        return out
    last = steps[-tail:]
    mean = sum(T['regular'][s][col_p] for s in last) / tail
    win = [s for s in steps if s0p - window <= s <= s0p + window]
    rels = [abs(T['regular'][s][col_p] - mean) / mean for s in win]
    kes = [T['regular'][s][col_ke] for s in last]
    wm = [sum(kes[5 * j:5 * j + 5]) / 5 for j in range(tail // 5)]
    out.update(n_window=len(win), max_rel=max(rels) if rels else None, tail_mean=mean, ke_base=statistics.median(wm) if wm else None,
               status='PASS' if rels and max(rels) <= frac else 'FAIL')
    return out


def restoration_verdict(reset_ok, g0_ok, obs_syntax_ok, prepost_equal, history_test_pass, un_erasure_seen):
    """§12-1 ⑤ · 개정 3 §14-10 — 문법 · 기술 실패 · 값 불일치 · 미확인을 따로 적는다 · RESTORED 일 때만 본 U (미확인을 표지만 달아 넘기지 않는다).
    prepost_equal · un_erasure_seen = True / False / None (None = 관측 결손으로 비교 미계산 → 미확인 · 수치 불일치와 섞지 않는다)."""
    if obs_syntax_ok is not True:
        return 'SYNTAX_FAIL'
    if reset_ok is not True or g0_ok is not True or prepost_equal is False:
        return 'VALUE_MISMATCH'
    if prepost_equal is not True or history_test_pass is not True or un_erasure_seen is not True:
        return 'UNCONFIRMED'
    return 'RESTORED'


# ── selftest ─────────────────────────────────────────────────────────────────

def _unload_head_from_r8(r8):
    """시험용 최소 언로딩 머리 — r8 글자에서 프로그램으로 (생성기와 독립 · G0 판별력 시험 전용)."""
    out, skip = [], False
    for ln in r8.splitlines():
        s = ln.strip()
        if s.startswith('read_restart'):
            out.append('read_restart ${ckpt}')
            continue
        if s.startswith('shell mkdir'):
            continue
        if s.startswith('fix damp all viscous 0.5'):
            continue
        if s.startswith('fix top_mesh'):
            out.append(s.replace('plate_ps_7_3_r45_r8.stl', '${plate_stl}'))
            continue
        if s.startswith('print "====== PHASE 3'):
            skip = True
        if skip:
            continue
        out.append(ln)
    out += ['fix damp all viscous 1.0e-5', 'fix_modify zwall_top energy yes', 'compute ul_erot all erotate/sphere',
            'fix ul_av all ave/time 100 50 5000 v_pressMPa c_ul_erot',
            'dump dmp_atom all custom 5000 ${out}/post/atom_*.liggghts id type x y z radius vx vy vz omegax omegay omegaz fx fy fz',
            'thermo_style custom step atoms ke c_ul_erot v_pressMPa cpu', 'thermo 500', 'run 5000']
    return '\n'.join(out) + '\n'


def selftest():
    import tempfile
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    P = ul_lib.load_params()
    r8, r2 = ul_lib.r8_text(P), ul_lib.r2_text(P)
    U = _unload_head_from_r8(r8)
    chk('A1 원 r8 의 S0 정의: 감쇠 1.0e-5 (압축 0.5 아님) · move_press 없음 · fix 순서 … zwall_top → damp',
        lambda: (lambda a: a['fixes']['damp'][1:] == ('viscous', '1.0e-5') and 'move_press' not in a['fixes']
                 and list(a['fixes'])[-3:] == ['top_mesh', 'zwall_top', 'damp'])(active_definitions(r8)))
    chk('A2 원 r2 (원 덱 꼴 · 10:0 과 같은 생성기) 의 S0 정의: 중력 9.81 (정착 98.1 은 덮였다) · 감쇠 1.0e-5 · zmax compute 있음',
        lambda: (lambda a: a['fixes']['gravi'][1:] == ('gravity', '9.81', 'vector', '0.0', '0.0', '-1.0') and a['fixes']['damp'][2] == '1.0e-5'
                 and 'zmax' in a['computes'])(active_definitions(r2)))
    chk('A3 G0 r8 ↔ 시험 머리 = PASS (허용: 출력 · 판 STL 경로 · 새 관측 ul_ compute / ave/time)',
        lambda: (lambda g: g['status'] == 'PASS' and not g['violations'] and g['allowed'])(g0_compare(r8, U)))
    chk('A4 G0 r2 ↔ 시험 머리 = PASS (허용: zmax 없음 · restart 이름)', lambda: g0_compare(r2, U)['status'] == 'PASS')
    muts = {
        '압축 감쇠 0.5 복제': ('fix damp all viscous 1.0e-5', 'fix damp all viscous 0.5'),
        '정착 중력 98.1 복제': ('fix gravi all gravity 9.81', 'fix gravi all gravity 98.1'),
        '재료 m6 한 값': ('3.0 3.0 5.0', '3.0 3.0 4.0'),
        '바닥 벽 자리': ('zplane 0.0', 'zplane 0.001'),
        'pair 모델': ('rolling_friction cdt\npair_coeff', 'rolling_friction epsd2\npair_coeff'),
        '판 벽 빠짐': ('fix zwall_top all wall/gran', '# fix zwall_top all wall/gran'),
        '머리에 판 이동 fix': ('fix_modify zwall_top energy yes', 'fix_modify zwall_top energy yes\nfix move_press all move/mesh mesh top_mesh linear 0.0 0.0 0.01'),
        'timestep 5e-7 (dt₀ 팔)': ('variable dt      equal 1.0e-6', 'variable dt      equal 5.0e-7'),
    }
    for name, (a, b) in muts.items():
        chk(f'A5 G0 반례 — {name} = FAIL', lambda a=a, b=b: a in U and g0_compare(r8, U.replace(a, b, 1))['status'] == 'FAIL')
    order = U.replace('fix damp all viscous 1.0e-5\n', '').replace('fix integr all nve/sphere', 'fix integr all nve/sphere\nfix damp all viscous 1.0e-5')
    chk('A5 G0 반례 — 동역학 fix 순서 (damp 를 top_mesh 앞으로) = FAIL (힘 합산 순서)', lambda: g0_compare(r8, order)['status'] == 'FAIL')
    chk('A6 G0 등록 팔 dt (UT · dt₀/2 · read_restart 뒤) = 허용 · 표지',
        lambda: (lambda g: g['status'] == 'PASS' and any('dt' in x for x in g['allowed']))(
            g0_compare(r8, U.replace('read_restart ${ckpt}', 'read_restart ${ckpt}\nvariable dt equal 5e-07\ntimestep ${dt}'), arm_dt=5e-07)))
    # G1 · G3
    g1 = P['beds']['ps_7_3_r45']['g1']
    scr = ('    Step    Atoms         KinEng            CPU       pressMPa \n'
           ' 3200000   160417  1.3419507e-06              0     0.33 \nLoop time of 0 on 6 procs for 0 steps\n'
           '    Step    Atoms         KinEng            CPU       pressMPa \n'
           ' 3200000   160417  1.3419507e-06              0     0.33 \n 3201000   160417  1.5e-06  35  0.16600 \n 3202000 160417 1.4e-6 70 0.1655\n'
           'Loop time of 70 on 6 procs for 2000 steps\n')
    log = open(_r8log(P), encoding='utf-8', errors='replace').read()
    chk('B1 G1 setup 줄 = 표 (step · 원자 · KE 1e-6) = PASS', lambda: g1_check(scr, g1, 3200000)['status'] == 'PASS')
    chk('B1 G1 KE 상대 2e-6 어긋남 = FAIL', lambda: g1_check(scr.replace('1.3419507e-06', '1.3419534e-06', 1), g1, 3200000)['status'] == 'FAIL')
    chk('B1 G1 원자 하나 차 = FAIL', lambda: g1_check(scr.replace('160417', '160416', 1), g1, 3200000)['status'] == 'FAIL')
    chk('B2 G3 첫 정규 줄 (3,201,000) 판 압력 · 원자 = 원 r8 로그 5 % 안 = PASS', lambda: g3_check(scr, log, 3200000)['status'] == 'PASS')
    chk('B2 G3 판 압력 6 % 어긋남 = FAIL', lambda: g3_check(scr.replace('0.16600', '0.17600'), log, 3200000)['status'] == 'FAIL')
    with tempfile.TemporaryDirectory() as td:
        cols = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz', 'c_strs[1]', 'c_strs[2]', 'c_strs[3]', 'c_ke']
        rows = [{'id': i, 'type': 3, 'x': 0.001 * i, 'y': 0.002, 'z': 0.003, 'radius': 0.0005, 'vx': 1e-6, 'vy': 0.0, 'vz': -2e-6,
                 'c_strs[1]': -1.0, 'c_strs[2]': -2.0, 'c_strs[3]': -3.0, 'c_ke': 0.0} for i in range(1, 6)]
        fmt = lambda v: f'{v:g}'  # noqa: E731 — 원 덤프 기본 형식 (%g)
        ul_lib.write_custom(os.path.join(td, 'o.a'), 3200000, cols, rows, fmt=fmt)
        ul_lib.write_custom(os.path.join(td, 't.a'), 3200000, cols, list(reversed([dict(r, **{'c_strs[1]': -1.0000001}) for r in rows])), fmt=fmt)
        chk('C1 G2 같은 상태 (행 순서 · c_strs 끝자리 무관) = PASS · 다른 원자 0 / 5', lambda: (lambda g: g['status'] == 'PASS' and g['n_mismatch'] == 0
                                                                                      and g['n_atoms'] == 5)(g2_compare(os.path.join(td, 't.a'), os.path.join(td, 'o.a'))))
        r2_ = [dict(r) for r in rows]
        r2_[2]['z'] = 0.0030001
        ul_lib.write_custom(os.path.join(td, 'm.a'), 3200000, cols, r2_, fmt=fmt)
        chk('C1 G2 위치 하나 다름 = FAIL (1 / 5)', lambda: (lambda g: g['status'] == 'FAIL' and g['n_mismatch'] == 1)(
            g2_compare(os.path.join(td, 'm.a'), os.path.join(td, 'o.a'))))
        ccols = [f'c_cpl[{i}]' for i in range(1, 27)]

        def crow(i, j, f, ft, x1=0.001, x2=0.0015, pflag=0.0):
            v = [x1, 0.01, 0.01, x2, 0.01, 0.01, i, j, pflag, f, 0.0, 0.0, f, 0.0, 0.0, 0.0, ft, 0.0, 0.0, 0.0, 0.0, 1e-8, 1e-5, 0.00125, 0.01, 0.01]
            return dict(zip(ccols, v))
        base = [crow(1, 2, -0.5, 0.01), crow(2, 3, -0.4, 0.0), crow(4, 5, -0.3, 0.02, x1=0.0495, x2=0.0003)]
        ul_lib.write_local(os.path.join(td, 'o.c'), 3200000, ccols, base)
        swapped = [crow(2, 1, 0.5, -0.01, x1=0.0015, x2=0.001), base[1], crow(4, 5, -0.3, 0.02, x1=0.0495, x2=0.0503, pflag=1.0)]
        ul_lib.write_local(os.path.join(td, 's.c'), 3200000, ccols, swapped)
        chk('C2 G2c 방향 바뀐 행 (힘 부호 · 두 위치 바꿈) · 주기 image (x + L) · 주기 플래그 다름 = PASS · 판별력 = 접선 0 아닌 몫 2/3',
            lambda: (lambda g: g['status'] == 'PASS' and abs(g['discriminating_frac'] - 2.0 / 3.0) < 1e-12)(
                g2c_compare(os.path.join(td, 's.c'), os.path.join(td, 'o.c'))))
        bad = [crow(1, 2, -0.5, 0.0100002), base[1], base[2]]
        ul_lib.write_local(os.path.join(td, 'b.c'), 3200000, ccols, bad)
        chk('C2 G2c 접선 힘 상대 2e-5 차 (허용 1e-5 밖) = FAIL', lambda: g2c_compare(os.path.join(td, 'b.c'), os.path.join(td, 'o.c'))['status'] == 'FAIL')
        ul_lib.write_local(os.path.join(td, 'x.c'), 3200000, ccols, base[:2])
        chk('C2 G2c 접촉 하나 빠짐 = FAIL (집합 차를 MPI 끝자리로 면제하지 않는다)', lambda: g2c_compare(os.path.join(td, 'x.c'), os.path.join(td, 'o.c'))['status'] == 'FAIL')
        ul_lib.write_local(os.path.join(td, 'd.c'), 3200000, ccols, base + [base[0]])
        chk('C2 G2c 같은 값 중복 키 = PASS · 중복 수 1', lambda: (lambda g: g['status'] == 'PASS' and g['n_dup_consistent'] == 1)(
            g2c_compare(os.path.join(td, 'd.c'), os.path.join(td, 'o.c'))))
        ul_lib.write_local(os.path.join(td, 'e.c'), 3200000, ccols, base + [crow(1, 2, -0.6, 0.01)])
        chk('C2 G2c 다른 값 중복 키 = FAIL', lambda: g2c_compare(os.path.join(td, 'e.c'), os.path.join(td, 'o.c'))['status'] == 'FAIL')
        ul_lib.write_local(os.path.join(td, 'f.c'), 3200000, ccols, [crow(1, 2.5, -0.5, 0.01), base[1], base[2]])
        chk('C3 ULKRR-04 G2c 쌍 참조 소수 ID (2 → 2.5 — 정수 2 로 잘려 같은 키가 되지 않는다) = FAIL',
            lambda: g2c_compare(os.path.join(td, 'f.c'), os.path.join(td, 'o.c'))['status'] == 'FAIL')
        fa = os.path.join(td, 'f.a')
        ul_lib.write_custom(fa, 3200000, cols, rows, fmt=fmt)
        fa_text = open(fa).read().replace('\n2 3 ', '\n2.5 3 ', 1)
        open(fa, 'w').write(fa_text)
        chk('C3 ULKRR-04 G2 원자 ID 소수 (2 → 2.5) = FAIL (글자 그대로 정수 변환 — 잘라서 같은 원자로 보지 않는다)',
            lambda: '\n2.5 3 ' in open(fa).read() and g2_compare(fa, os.path.join(td, 'o.a'))['status'] == 'FAIL')
        # ── ULKRF-03 (Codex 수정 재확인 10-15 · g2c_c_cpl7_missing · g2c_c_cpl8_missing) — 필수 열 결손 = 파서 ok 거짓을 먼저 → FAIL + 사유 (KeyError 아님) ──
        for col in ('c_cpl[7]', 'c_cpl[8]'):
            for side in ('test', 'orig'):
                nc = os.path.join(td, f'nc_{side}_{col[6]}.c')
                ul_lib.write_local(nc, 3200000, ccols, base)
                txt = open(nc).read().replace(f' {col} ', f' not_{col} ', 1)   # 머리의 열 이름 하나만 · 숫자 행은 그대로
                with open(nc, 'w', newline='\n') as f:
                    f.write(txt)
                pair = (nc, os.path.join(td, 'o.c')) if side == 'test' else (os.path.join(td, 's.c'), nc)
                chk(f'C4 ULKRF-03 G2c {"시험" if side == "test" else "원"} 쪽 쌍 덤프 머리 {col} → not_{col} (필수 열 결손) = 예외 없이 FAIL + 사유 '
                    '(파서 ok 거짓을 먼저 · 숫자를 채우거나 행을 지우지 않는다)',
                    lambda pair=pair, nc=nc, col=col: (lambda g: g['status'] == 'FAIL' and any('열 이름' in w for w in g['why'])
                                                       and f'not_{col}' in open(nc).read())(g2c_compare(*pair)))
        stl = 'solid x\n  facet normal 0 0 -1\n    outer loop\n      vertex 0 0 {z}\n      vertex 0 0.05 {z}\n      vertex 0.05 0.05 {z}\n'
        for name, z in (('m1.stl', '0.111252'), ('m2.stl', '0.111254')):
            open(os.path.join(td, name), 'w').write(stl.format(z=z))
        chk('D1 판 z: 메시 0.111252 ↔ 공식 0.11125200001 = PASS · 0.111254 ↔ 0.111252 = FAIL (2e-6 > 1e-6)',
            lambda: plate_z_check([(os.path.join(td, 'm1.stl'), 0.11125200001)])['status'] == 'PASS'
            and plate_z_check([(os.path.join(td, 'm2.stl'), 0.111252)])['status'] == 'FAIL')
    # S0′ 조건 (10:0 연장) — §11-2 awk 와 같은 셈
    lines = ['    Step    Atoms         KinEng            CPU       pressMPa ', ' 3600000 159152 3.5e-06 0 0.30']
    lines += [f' {3600000 + 1000 * k} 159152 {1e-7 * (1 + (k % 5))} {k} 0.17400' for k in range(1, 61)]
    lines.append('Loop time of 1 on 6 procs for 60000 steps')
    ok_log = '\n'.join(lines) + '\n'
    spike = ok_log.replace(' 3652000 159152 3e-07 52 0.17400', ' 3652000 159152 3e-07 52 0.17700')
    chk('E1 S0′ = 3,650,000 · ±5,000 정규 줄 11 개 · 차 0 = PASS · KE 기준 = 5 줄 창 평균 다섯의 중앙값',
        lambda: (lambda s: s['status'] == 'PASS' and s['n_window'] == 11 and abs(s['ke_base'] - 3e-7) < 1e-18)(s0p_condition(ok_log, 3650000)))
    chk('E1 S0′ 창 안 한 줄 1.7 % 튐 = FAIL (S0″ 로)', lambda: s0p_condition(spike, 3650000)['status'] == 'FAIL')
    chk('E1 S0′ 창이 런 밖 (마지막 줄 3,660,000 < 3,705,000) = NOT_COMPUTED', lambda: s0p_condition(ok_log, 3700000)['status'] == 'NOT_COMPUTED')
    # 복원 판정 (§12-1 ⑤)
    chk('F1 복원 판정: 다 참 = RESTORED', lambda: restoration_verdict(True, True, True, True, True, True) == 'RESTORED')
    chk('F1 이력 시험 미통과 · 미실행 = UNCONFIRMED (표지만 달아 U 로 넘기지 않는다)', lambda: restoration_verdict(True, True, True, True, None, True) == 'UNCONFIRMED'
        and restoration_verdict(True, True, True, True, False, True) == 'UNCONFIRMED')
    chk('F1 관측 문법 실패 = SYNTAX_FAIL · reset 로그 결손 · G0 위반 · PRE ≠ POST = VALUE_MISMATCH',
        lambda: restoration_verdict(True, True, False, True, True, True) == 'SYNTAX_FAIL'
        and restoration_verdict(False, True, True, True, True, True) == 'VALUE_MISMATCH'
        and restoration_verdict(True, False, True, True, True, True) == 'VALUE_MISMATCH'
        and restoration_verdict(True, True, True, False, True, True) == 'VALUE_MISMATCH')
    chk('F1 보조 소거 진단 (UN) 이 아무 차이도 못 봄 = UNCONFIRMED (판별력 없음)', lambda: restoration_verdict(True, True, True, True, True, False) == 'UNCONFIRMED')
    chk('F2 ULKR-05 PRE · POST 관측 결손 (비교 미계산 = None) = UNCONFIRMED — 수치 불일치 (False = VALUE_MISMATCH) 와 따로 · 소거 진단 미계산 (None) 도 UNCONFIRMED',
        lambda: restoration_verdict(True, True, True, None, True, True) == 'UNCONFIRMED'
        and restoration_verdict(True, True, True, True, True, None) == 'UNCONFIRMED'
        and restoration_verdict(False, True, True, None, True, True) == 'VALUE_MISMATCH')
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def _r8log(P):
    import tempfile
    raw = ul_lib.tgz_member(P['head_source']['r8_log_suffix'], None, P)
    p = os.path.join(tempfile.gettempdir(), 'ul_gates_r8log_' + hashlib.sha256(raw).hexdigest()[:12] + '.out')
    if not os.path.exists(p):
        with open(p, 'wb') as f:
            f.write(raw)
    return p


def main(argv=None):
    import argparse
    import json
    ap = argparse.ArgumentParser(description='DEM 언로딩 키트 K7 복원 관문 비교기')
    ap.add_argument('cmd', nargs='?', choices=['g0', 'g2', 'g2c'])
    ap.add_argument('a', nargs='?')
    ap.add_argument('b', nargs='?')
    ap.add_argument('--arm-dt', type=float)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.cmd and a.a and a.b):
        ap.error('명령 · 두 파일 (또는 --selftest)')
    if a.cmd == 'g0':
        r = g0_compare(open(a.a, encoding='utf-8').read(), open(a.b, encoding='utf-8').read(), arm_dt=a.arm_dt)
    elif a.cmd == 'g2':
        r = g2_compare(a.a, a.b)
    else:
        r = g2c_compare(a.a, a.b)
    print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
    return 0 if r.get('status') == 'PASS' else 2


if __name__ == '__main__':
    sys.exit(main())
