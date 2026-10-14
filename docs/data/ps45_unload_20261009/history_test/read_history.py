#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 — 작은 침대 이력 시험 (H0–H5) 읽는 쪽.  표준 라이브러리만 · 읽기 전용.

    python3 read_history.py <런 폴더 hist_*> [--params history_params.json] [--out verdict.json]
    python3 read_history.py --grammar <런 폴더 gram_*> [--out grammar_verdict.json]   # 문법 fixture (Q8 · 등록 개정 3 §14-9)
    python3 read_history.py --selftest
    python3 read_history.py --mock-stage <단계> <폴더> [--scenario good]   # 러너 모의 시험용 (LIGGGHTS 대신 덤프 · 화면을 흉내)

판정 (정본 = ../README.md §1 · Codex 판정문 10-12 §5-2 표 · 노트 history.md §3)
  H0 문법   : 단계마다 rc 0 · 배너 3.8.0 / 3d5c00f · ERROR 없음 · 'Loop time … on N procs' 의 N = 그 단계 NP · 덤프 머리 · 열 · 행 ·
              내부 이력 fix 의 restart reset 로그 (소비자 = 다섯 fix 의 global · per-atom) · 생산자 write_dump 묶음 = in-run 덤프.
              ⚠ 성공했다고 값 보존까지 통과시키지 않는다.
  H1 · H2   : 생산자 끝 (in-run 마지막 step) ↔ 소비자 (같은 NP · 다른 NP) — 원자 상태 · primitive PRE_SETUP (정확히 같음) ·
              primitive · mesh · pair POST_SETUP (허용폭) · 행 순서 무시 · pair 는 무순서 키 + 방향 바뀐 shear 부호 정규화.
  H3 · H4   : 한 벽만 소거한 진단 사본 → 새 프로세스.  소거한 벽: sentinel 의 비영 shear → 0 · 저장 deltaMax > 현재 δ 이던 sentinel 은
              deltaMax 감소 (POST 에서는 현재 겹침으로 다시 찰 수 있다 — "setup 뒤 4 열 0" 을 기대하지 않는다) · 손대지 않은 벽 · pair 는 그대로 ·
              양성 대조 (같은 직렬화 횟수 · unfix 없음) = 생산자와 같음.
  H5        : 잘못된 내부 ID = TECH (관측 문법 실패) 로 분류되어야 · 0 뿐 fixture = INCONCLUSIVE (0/0 PASS 아님) 로 분류되어야.
  비퇴화    : sentinel (저장 deltaMax − 현재 δ ≥ 1e-9 · |shear| ≥ 1e-9 덱 m) 이 그 종류 (primitive · mesh · pair) 에 하나도 없으면 그 종류는
              INCONCLUSIVE — 값이 같아도 PASS 가 아니다.
  정보 (판정 밖): H0b run 끝 자동 restart 유무 (10:0 연장 3,660,000 질문) · 총힘 출력 시점 (접촉 없는 입자 fz = −m g) · SYN 문법 미리 지나가기.
  문법 fixture (--grammar · 등록 개정 3 §14-9 · Q8 · 검사 전부 참 = PASS): P → GA (빈 상태 파일 · 창 → 이동 → 창 → 이동 → 창) → GB (GA 마지막 단 끝
              restart + 상태 파일 · 새 프로세스 · 이동 → 창) — 기술 · 화면 표지 · 변수 주기 덤프 = 창 끝만 · 판 z (mesh/stl) 누적 · 새 프로세스 복원 ·
              상태 파일 값 · 영역 판 접촉 ↔ 판 local · GB 입력 = GA 마지막.  짧은 문법 런 = 물리 검증 아님 (C19).
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PARAMS = os.path.join(HERE, 'history_params.json')
G = 9.81
STAGES = ('P', 'C6', 'C4', 'Ebot', 'Cbot', 'Etop', 'Ctop', 'Enone', 'Cnone', 'BAD', 'SYN', 'PZ', 'CZ')


def load_params(path=PARAMS):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ── 구현 (아래 selftest 를 먼저 썼다 — 시험 먼저 기록 = ../README.md §9) ───────────────────────────────

def _num(s):
    v = float(s)
    return v


def read_dump(path, kind, cols_expected):
    """LIGGGHTS 덤프 한 장 → {'ok', 'step', 'cols', 'rows' (list of dict), 'box', 'problems'} (kind = custom | local)."""
    out = {'ok': False, 'path': path, 'step': None, 'cols': None, 'rows': [], 'box': None, 'problems': []}
    if not path or not os.path.exists(path):
        out['problems'].append(f'파일 없음: {path}')
        return out
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    pr = out['problems']
    try:
        out['step'] = int(lines[lines.index('ITEM: TIMESTEP') + 1].strip())
    except (ValueError, IndexError):
        pr.append('TIMESTEP 머리 없음')
    head = 'ITEM: ATOMS' if kind == 'custom' else 'ITEM: ENTRIES'
    nhead = 'ITEM: NUMBER OF ATOMS' if kind == 'custom' else 'ITEM: NUMBER OF ENTRIES'
    try:
        n_decl = int(lines[lines.index(nhead) + 1].strip())
    except (ValueError, IndexError):
        n_decl = None
        pr.append(f'{nhead} 머리 없음')
    try:
        kb = next(i for i, x in enumerate(lines) if x.startswith('ITEM: BOX BOUNDS'))
        out['box'] = [tuple(float(v) for v in lines[kb + j].split()[:2]) for j in (1, 2, 3)]
    except (StopIteration, ValueError, IndexError):
        pr.append('BOX BOUNDS 머리 없음')
    k = next((i for i, x in enumerate(lines) if x.startswith(head)), None)
    if k is None:
        pr.append(f'{head} 머리 없음')
        return out
    cols = lines[k].split()[2:]
    out['cols'] = cols
    if cols != list(cols_expected):
        pr.append(f'열 이름 {cols} ≠ 기대 {list(cols_expected)}')
    for ln in lines[k + 1:]:
        if not ln.strip():
            continue
        if ln.startswith('ITEM:'):
            pr.append('한 파일에 프레임이 둘 이상')
            break
        vals = ln.split()
        if len(vals) != len(cols):
            pr.append(f'열 수 {len(vals)} ≠ {len(cols)}: {ln[:80]}')
            continue
        try:
            row = {c: _num(v) for c, v in zip(cols, vals)}
        except ValueError:
            pr.append(f'숫자가 아닌 값: {ln[:80]}')
            continue
        if not all(math.isfinite(v) for v in row.values()):
            pr.append(f'비유한 값: {ln[:80]}')
            continue
        out['rows'].append(row)
    if n_decl is not None and n_decl != len(out['rows']) and not any(p.startswith(('비유한', '숫자가', '열 수')) for p in pr):
        pr.append(f'행 수 {len(out["rows"])} ≠ 머리 {n_decl}')
    out['ok'] = not pr
    return out


def _one(d, pattern):
    hits = sorted(glob.glob(os.path.join(d, pattern)))
    return hits[-1] if hits else None, len(hits)


def screen_info(d):
    path = os.path.join(d, 'screen.out')
    info = {'exists': os.path.exists(path), 'banner': False, 'git': False, 'errors': [], 'loops': [], 'resets': set(), 'markers': []}
    if not info['exists']:
        return info
    for ln in open(path, encoding='utf-8', errors='replace').read().splitlines():
        if 'LIGGGHTS-PUBLIC 3.8.0' in ln:
            info['banner'] = True
            info['git'] = info['git'] or '3d5c00f' in ln
        if ln.startswith('ERROR') or 'Segmentation fault' in ln or 'MPI_ABORT' in ln:
            info['errors'].append(ln.strip())
        m = re.search(r'Loop time of [0-9.eE+-]+ on (\d+) procs', ln)
        if m:
            info['loops'].append(int(m.group(1)))
        m = re.match(r'Resetting (global|per-atom) state of Fix (\S+) Style (\S+) from restart file info', ln.strip())
        if m:
            info['resets'].add((m.group(2), m.group(3), m.group(1)))
        if ln.startswith(('HIST_', 'SYN_', 'GRAM_')):
            info['markers'].append(ln.strip())
    return info


def _readf(path):
    try:
        return open(path, encoding='utf-8').read().strip()
    except OSError:
        return None


def load_stage(run_dir, name, P):
    """한 단계 폴더 → 기술 점검 + 덤프 (없으면 problems)."""
    d = os.path.join(run_dir, name)
    O = P['observers']
    st = {'name': name, 'dir': d, 'exists': os.path.isdir(d), 'problems': [], 'tech_ok': False}
    if not st['exists']:
        st['problems'].append('단계 폴더 없음')
        return st
    rc, np_ = _readf(os.path.join(d, 'rc')), _readf(os.path.join(d, 'np.txt'))
    st['rc'] = rc
    st['np'] = int(np_) if np_ and np_.isdigit() else None
    S = screen_info(d)
    st['screen'] = S
    if name == 'BAD':
        return st
    pr = st['problems']
    if rc != '0':
        pr.append(f'rc = {rc}')
    if not S['banner'] or not S['git']:
        pr.append('배너 LIGGGHTS-PUBLIC 3.8.0 · 3d5c00f 없음')
    if S['errors']:
        pr.append('ERROR: ' + ' | '.join(S['errors'][:2]))
    if not S['loops'] or any(n != st['np'] for n in S['loops']):
        pr.append(f'Loop time 의 procs {S["loops"]} ≠ 단계 NP {st["np"]}')
    if name in ('P', 'PZ'):
        pa, n1 = _one(d, os.path.join('producer', 'atoms_*.dump'))
        st['atoms'] = read_dump(pa, 'custom', O['atoms_post'])
        st['pack'] = read_dump(os.path.join(d, 'producer', 'end_pack.dump'), 'custom', O['atoms_pre'])
        st['mesh'] = read_dump(_one(d, os.path.join('producer', 'mesh_*.dump'))[0], 'local', O['mesh_local'])
        st['pair'] = read_dump(_one(d, os.path.join('producer', 'pair_*.dump'))[0], 'local', O['pair_local'])
        if n1 != 1:
            pr.append(f'producer/atoms_*.dump {n1} 장 (기대 1 — 마지막 step 만)')
        if not any(m.startswith('HIST_PRODUCER_DONE') for m in S['markers']):
            pr.append('HIST_PRODUCER_DONE 없음')
        if not os.path.exists(os.path.join(d, 'fixture.bin')):
            pr.append('fixture.bin 없음')
        st['auto'] = sorted(int(re.search(r'auto_(\d+)\.bin$', p).group(1)) for p in glob.glob(os.path.join(d, 'restart', 'auto_*.bin')))
        dumps = ('atoms', 'pack', 'mesh', 'pair')
    elif name == 'SYN':
        st['tech_ok'] = not pr
        return st
    else:
        st['pre'] = read_dump(os.path.join(d, 'pre_atoms.dump'), 'custom', O['atoms_pre'])
        st['atoms'] = read_dump(_one(d, 'post_atoms_*.dump')[0], 'custom', O['atoms_post'])
        st['mesh'] = read_dump(_one(d, 'post_mesh_*.dump')[0], 'local', O['mesh_local'])
        st['pair'] = read_dump(_one(d, 'post_pair_*.dump')[0], 'local', O['pair_local'])
        want = 'HIST_ERASE_DONE' if name.startswith('E') else 'HIST_CONSUMER_DONE'
        if not any(m.startswith(want) for m in S['markers']):
            pr.append(f'{want} 없음')
        if name.startswith('E') and not os.path.exists(os.path.join(d, 'erased.bin')):
            pr.append('erased.bin 없음')
        dumps = ('pre', 'atoms', 'mesh', 'pair')
        #  내부 이력 fix 의 restart reset 로그 (판정문 §5-1 — 첫 초기화 뒤 판정 · 소거 단계는 그 벽 것이 없어야)
        exp = {(f, s, k) for f, s, kinds in P['expected_reset_fixes'] for k in kinds}
        absent = set()
        optional = set()
        if name == 'Cbot':
            absent = {x for x in exp if x[0] == 'history_zwall_bot'}
        if name == 'Ctop':
            absent = {x for x in exp if x[0] == 'tracker_top_mesh'}
            optional = {x for x in exp if x[0] == 'n_neighs_mesh_top_mesh'}
        miss = sorted(exp - absent - optional - S['resets'])
        bad = sorted(absent & S['resets'])
        if miss:
            pr.append(f'reset 로그 없음: {miss}')
        if bad:
            pr.append(f'소거한 이력의 reset 로그가 있다 (소거 안 됨?): {bad}')
    for k in dumps:
        for p in st[k]['problems']:
            pr.append(f'{k}: {p}')
    st['tech_ok'] = not pr
    return st


def _close(a, b, rel, ab):
    return abs(a - b) <= max(ab, rel * max(abs(a), abs(b)))


def _hcols(P):
    return [f'f_history_zwall_bot[{k}]' for k in range(1, P['observers']['history_cols'] + 1)]


def atom_map(d):
    out, dup = {}, []
    for r in d['rows']:
        i = int(r['id'])
        if i in out:
            dup.append(i)
        out[i] = r
    return out, dup


def prim_map(d, P):
    cols = _hcols(P)
    return {int(r['id']): [r[c] for c in cols] for r in d['rows']}


def local_map(d, kind, atom_ids, P):
    """mesh: (mesh index, 삼각형, 입자) 키 · pair: 무순서 (작은 id, 큰 id) 키 + 방향 바뀐 shear 부호 정규화.
    → (지도 {키: [deltaMax, sx, sy, sz]}, 같은 값 중복 수, 문제 목록)."""
    out, ndup, pr = {}, 0, []
    tol = P['tolerances']
    meshes = set()
    for r in d['rows']:
        v = list(r.values())
        ids = v[:3]
        h = v[3:7]
        if any(abs(x - round(x)) > 0 for x in ids):
            pr.append(f'id 열이 정수가 아니다 (열 의미 불일치?): {ids}')
            continue
        a, b, c = (int(round(x)) for x in ids)
        if kind == 'mesh':
            if c not in atom_ids or b < 0:
                pr.append(f'mesh 행의 입자 id {c} · 삼각형 {b} 가 이상하다 (열 의미 불일치?)')
                continue
            meshes.add(a)
            key = (a, b, c)
        else:
            if a not in atom_ids or b not in atom_ids or a == b or c not in (0, 1):
                pr.append(f'pair 행 ({a}, {b}, 표지 {c}) 가 이상하다 (열 의미 불일치?)')
                continue
            if a > b:
                h = [h[0], -h[1], -h[2], -h[3]]
            key = (min(a, b), max(a, b))
        if key in out:
            if all(_close(x, y, tol['post_rel'], tol['post_abs']) for x, y in zip(out[key], h)):
                ndup += 1
            else:
                pr.append(f'중복 키 {key} 값이 다르다: {out[key]} ↔ {h}')
            continue
        out[key] = h
    if len(meshes) > 1:
        pr.append(f'mesh index 가 여럿: {sorted(meshes)}')
    return out, ndup, pr


def _lbox(d):
    b = d.get('box') or [(0.0, 0.05), (0.0, 0.05), (-0.01, 0.1)]
    return b[0][1] - b[0][0], b[1][1] - b[1][0]


def current_overlaps(A, P, box):
    """현재 겹침 — 바닥 (r − z) · 판 (z + r − z_plate · 중심이 판 아래) · 쌍 (r_i + r_j − 최소 영상 거리)."""
    zp = P['z_plate']
    lx, ly = box
    bot = {i: a['radius'] - a['z'] for i, a in A.items() if a['z'] - a['radius'] < 0}
    top = {i: a['z'] + a['radius'] - zp for i, a in A.items() if a['z'] < zp and a['z'] + a['radius'] > zp}

    def pair(i, j):
        a, b = A[i], A[j]
        dx = (a['x'] - b['x'] + lx / 2) % lx - lx / 2
        dy = (a['y'] - b['y'] + ly / 2) % ly - ly / 2
        return a['radius'] + b['radius'] - math.sqrt(dx * dx + dy * dy + (a['z'] - b['z']) ** 2)
    return bot, top, pair


def sentinels(prod, P):
    """생산자 끝 자료의 sentinel (저장 deltaMax − 현재 δ ≥ gap · |shear| ≥ s) — 종류별 키 집합."""
    T = P['tolerances']
    A, _ = atom_map(prod['atoms'])
    bot, top, pair = current_overlaps(A, P, _lbox(prod['atoms']))
    pm = prim_map(prod['atoms'], P)
    mm, _, _ = local_map(prod['mesh'], 'mesh', set(A), P)
    qm, _, _ = local_map(prod['pair'], 'pair', set(A), P)

    def ok(h, dcur):
        return h[0] - dcur >= T['sentinel_dmax_gap'] and math.sqrt(h[1] ** 2 + h[2] ** 2 + h[3] ** 2) >= T['sentinel_shear']
    return {'primitive': {i for i, h in pm.items() if i in bot and ok(h, bot[i])},
            'mesh': {k for k, h in mm.items() if k[2] in top and ok(h, top[k[2]])},
            'pair': {k for k, h in qm.items() if ok(h, pair(*k))}}


def _cmp_maps(ref, got, rel, ab, exact=False):
    miss = sorted(set(ref) - set(got))
    extra = sorted(set(got) - set(ref))
    bad = []
    for k in sorted(set(ref) & set(got)):
        if exact:
            if list(ref[k]) != list(got[k]):
                bad.append((k, ref[k], got[k]))
        elif not all(_close(x, y, rel, ab) for x, y in zip(ref[k], got[k])):
            bad.append((k, ref[k], got[k]))
    return miss, extra, bad


def _status(problems, mism, nsent):
    if problems:
        return 'TECH'
    if mism:
        return 'FAIL'
    if nsent == 0:
        return 'INCONCLUSIVE'
    return 'PASS'


def _fold(statuses):
    for s in ('TECH', 'FAIL', 'INCONCLUSIVE'):
        if s in statuses:
            return s
    return 'PASS'


def roundtrip(prod, cons, P):
    """생산자 끝 ↔ 소비자 (H1 · H2 · 양성 대조 · 0 fixture)."""
    T = P['tolerances']
    out = {'classes': {}, 'dup_consistent': 0, 'problems': []}
    if not (prod['tech_ok'] and cons['tech_ok']):
        out['problems'] = [f'{s["name"]}: {p}' for s in (prod, cons) for p in s['problems']] or ['단계 기술 실패']
        out['status'] = 'TECH'
        return out
    A, _ = atom_map(prod['atoms'])
    pre, _ = atom_map(cons['pre'])
    sent = sentinels(prod, P)
    out['sentinels'] = {k: len(v) for k, v in sent.items()}
    # 원자 상태 (PRE · write_dump = 배열 그대로) — atoms_pre 열 전부 정확히
    cols = [c for c in P['observers']['atoms_pre'] if c != 'id']
    bad_atoms = [i for i in A if i not in pre or any(A[i][c] != pre[i][c] for c in cols)]
    extra_atoms = sorted(set(pre) - set(A))
    out['atoms_pre'] = {'mismatch': bad_atoms[:10], 'n_mismatch': len(bad_atoms), 'extra': extra_atoms}
    # primitive: PRE 정확 · POST 허용폭
    pm_ref = prim_map(prod['atoms'], P)
    m1 = _cmp_maps(pm_ref, prim_map(cons['pre'], P), 0, 0, exact=True)
    m2 = _cmp_maps(pm_ref, prim_map(cons['atoms'], P), T['post_rel'], T['post_abs'])
    probs = [f'원자 키 {m}' for m in (m1[0] + m1[1])][:5]
    out['classes']['primitive'] = {'status': _status(probs, m1[2] or m2[2] or bad_atoms or extra_atoms, len(sent['primitive'])),
                                   'pre_mismatch': m1[2][:5], 'post_mismatch': m2[2][:5]}
    for kind in ('mesh', 'pair'):
        ref, nd1, p1 = local_map(prod[kind], kind, set(A), P)
        got, nd2, p2 = local_map(cons[kind], kind, set(A), P)
        out['dup_consistent'] += nd1 + nd2
        miss, extra, bad = _cmp_maps(ref, got, T['post_rel'], T['post_abs'])
        probs = p1 + p2 + ([f'키 빠짐 {miss[:3]}'] if miss else []) + ([f'키 더 있음 {extra[:3]}'] if extra else [])
        out['classes'][kind] = {'status': _status(probs, bad, len(sent[kind])), 'problems': probs[:5], 'mismatch': bad[:5],
                                'n_keys': len(ref)}
    out['status'] = _fold([c['status'] for c in out['classes'].values()])
    return out


def erasure(prod, ers, cons, ctrl_rt, wall, P):
    """한 벽 소거 (H3 = primitive · H4 = mesh) — 소거한 벽: sentinel shear → 0 · deltaMax 감소 (POST = 현재 겹침) ·
    손대지 않은 벽 · pair = 생산자 · 양성 대조 = PASS."""
    T = P['tolerances']
    out = {'wall': wall, 'checks': {}, 'problems': []}
    stages = (prod, ers, cons)
    if not all(s['tech_ok'] for s in stages):
        out['problems'] = [f'{s["name"]}: {p}' for s in stages for p in s['problems']] or ['단계 기술 실패']
        out['status'] = 'TECH'
        return out
    A, _ = atom_map(prod['atoms'])
    sent = sentinels(prod, P)
    out['sentinels'] = {k: len(v) for k, v in sent.items()}
    bot, top, _ = current_overlaps(A, P, _lbox(prod['atoms']))
    fails = []
    pm_ref = prim_map(prod['atoms'], P)
    pre_p, post_p = prim_map(cons['pre'], P), prim_map(cons['atoms'], P)
    mm_ref, _, p1 = local_map(prod['mesh'], 'mesh', set(A), P)
    mm_got, _, p2 = local_map(cons['mesh'], 'mesh', set(A), P)
    qm_ref, _, p3 = local_map(prod['pair'], 'pair', set(A), P)
    qm_got, _, p4 = local_map(cons['pair'], 'pair', set(A), P)
    probs = p1 + p2 + p3 + p4
    #  소거 전 관측 (진단 사본의 run 0) = 생산자 — 소거 전에 이미 달랐다면 소거 시험이 아니다
    pre_erase = roundtrip(prod, ers, P)
    out['checks']['pre_erase_observation'] = pre_erase['status']
    if pre_erase['status'] in ('TECH', 'FAIL'):
        fails.append(f'소거 전 관측 ≠ 생산자 ({pre_erase["status"]})')
    if wall == 'primitive':
        nz_pre = [i for i, h in pre_p.items() if any(h)]
        out['checks']['pre_all_zero'] = not nz_pre
        if nz_pre:
            fails.append(f'PRE 에 옛 바닥 이력이 남았다 (소거 안 됨): id {nz_pre[:5]}')
        regen_bad = [i for i, h in post_p.items() if any(h[1:]) or not _close(h[0], max(0.0, bot.get(i, 0.0)), 0, T['regen_dmax_abs'])]
        out['checks']['post_regen_ok'] = not regen_bad
        if regen_bad:
            fails.append(f'POST 바닥: shear ≠ 0 또는 deltaMax ≠ 현재 겹침 — id {regen_bad[:5]}')
        vis = [i for i in sent['primitive'] if post_p.get(i, [0])[0] < pm_ref[i][0] - T['sentinel_dmax_gap']
               and not any(post_p.get(i, [0, 1, 1, 1])[1:])]
        out['checks']['sentinel_erased'] = f'{len(vis)} / {len(sent["primitive"])}'
        if len(vis) != len(sent['primitive']):
            fails.append('sentinel 중 소거가 안 보이는 것이 있다')
        mi, ex, bad = _cmp_maps(mm_ref, mm_got, T['post_rel'], T['post_abs'])
        if mi or ex or bad:
            fails.append(f'손대지 않은 판 (mesh) 이력이 바뀌었다: {bad[:2] or mi[:2] or ex[:2]}')
        nsent = len(sent['primitive'])
    else:
        mi, ex, _ = _cmp_maps(mm_ref, mm_got, 0, 0)
        if mi or ex:
            probs.append(f'소거 뒤 mesh 접촉 키가 다르다: 빠짐 {mi[:3]} · 더 {ex[:3]}')
        regen_bad = [k for k, h in mm_got.items() if any(h[1:]) or not _close(h[0], top.get(k[2], 0.0), 0, T['regen_dmax_abs'])]
        out['checks']['post_regen_ok'] = not regen_bad
        if regen_bad:
            fails.append(f'POST 판: shear ≠ 0 또는 deltaMax ≠ 현재 겹침 — {regen_bad[:3]}')
        vis = [k for k in sent['mesh'] if k in mm_got and mm_got[k][0] < mm_ref[k][0] - T['sentinel_dmax_gap'] and not any(mm_got[k][1:])]
        out['checks']['sentinel_erased'] = f'{len(vis)} / {len(sent["mesh"])}'
        if len(vis) != len(sent['mesh']):
            fails.append('sentinel 중 소거가 안 보이는 것이 있다')
        m1 = _cmp_maps(pm_ref, pre_p, 0, 0, exact=True)
        m2 = _cmp_maps(pm_ref, post_p, T['post_rel'], T['post_abs'])
        if any(m1) or any(m2):
            fails.append(f'손대지 않은 바닥 (primitive) 이력이 바뀌었다: {(m1[2] or m2[2])[:2]}')
        nsent = len(sent['mesh'])
    mi, ex, bad = _cmp_maps(qm_ref, qm_got, T['post_rel'], T['post_abs'])
    if mi or ex or bad:
        fails.append(f'pair 이력이 바뀌었다: {bad[:2] or mi[:2] or ex[:2]}')
    out['checks']['control'] = ctrl_rt['status']
    if ctrl_rt['status'] != 'PASS':
        fails.append(f'양성 대조 (같은 직렬화 · unfix 없음) = {ctrl_rt["status"]}')
    out['problems'] = probs
    out['fails'] = fails
    out['status'] = _status(probs, fails, nsent)
    return out


def syn_info(run_dir, prod, P):
    d = os.path.join(run_dir, 'SYN')
    out = {'status': 'NOT_RUN', 'checks': {}, 'plate_fn_sign': None}
    if not os.path.isdir(d):
        return out
    S = screen_info(d)
    Y = P['syntax_probe']
    zp = P['z_plate']
    lift = Y['lift_v'] * Y['dt'] * Y['lift_steps']
    c = out['checks']
    c['rc0_no_error'] = _readf(os.path.join(d, 'rc')) == '0' and not S['errors']
    W = {}
    for m in S['markers']:
        mm = re.match(r'SYN_(W[01]) (.*)$', m)
        if mm:
            W[mm.group(1)] = dict(kv.split('=', 1) for kv in mm.group(2).split())
    c['markers'] = sorted(W) == ['W0', 'W1'] and any(m == 'SYN_DONE' for m in S['markers'])
    if not c['markers'] or not prod.get('tech_ok'):
        out['status'] = 'FAIL'
        return out
    A, _ = atom_map(prod['atoms'])
    try:
        c['dt_after_read_restart'] = float(W['W0']['dt']) == Y['dt'] and float(W['W1']['dt']) == Y['dt']
        c['Ps_signed_positive'] = float(W['W0']['Ps_avg']) > 0
        wcols = [f'c_u_wh[{i}]' for i in range(1, 7)]
        for tag, z in (('W0', zp), ('W1', zp + lift)):
            s = int(W[tag]['step'])
            dm = read_dump(os.path.join(d, 'probe', f'mesh_{s}.dump'), 'local', wcols)
            pids = {int(r['c_u_wh[3]']) for r in dm['rows']}
            below = {i for i in pids if A[i]['z'] < z}
            c[f'count_{tag}'] = dm['ok'] and int(W[tag]['n_contact_geo']) == len(below)
            c[f'n_{tag}'] = len(below)
            if tag == 'W0':
                fz = [r['c_u_wh[6]'] for r in dm['rows'] if int(r['c_u_wh[3]']) in below]
                sign = (-1 if fz and all(v < 0 for v in fz) else 1 if fz and all(v > 0 for v in fz) else ('MIXED' if fz else None))
                out['plate_fn_sign'] = sign
                c['fn_sign_uniform'] = sign in (-1, 1)
        sl = int(W['W1']['step']) - Y['window']
        stl = os.path.join(d, 'probe', f'plate_{sl}.stl')
        zs = {float(x) for x in re.findall(r'vertex\s+\S+\s+\S+\s+(\S+)', open(stl).read())} if os.path.exists(stl) else set()
        c['lift_mesh_z'] = len(zs) == 1 and abs(zs.pop() - (zp + lift)) <= 1e-6
        c['plate_z_formula'] = abs(float(W['W1']['plate_z']) - (zp + lift)) <= 1e-12
        c['restart_end_written'] = os.path.exists(os.path.join(d, 'probe_end.bin'))
    except (KeyError, ValueError, OSError) as e:
        c['parse'] = f'{type(e).__name__}: {e}'
        out['status'] = 'FAIL'
        return out
    out['status'] = 'PASS' if all(v is True for k, v in c.items() if not k.startswith('n_')) else 'FAIL'
    out['plate_fn_note'] = ('판 접촉에서 입자가 받는 법선력 fn_z 의 부호 (압축 상태) — 본 키트 unload_params.json 의 plate_fn_compressive_sign 과 '
                            '대조한다 (다르면 표를 고친다 · 결과 0 건에서)')
    return out


def evaluate(run_dir, P=None):
    P = P or load_params()
    st = {s: load_stage(run_dir, s, P) for s in STAGES}
    rows, info = {}, {}
    # H0 — 문법 · 기술 (BAD · SYN 빼고)
    h0p = []
    for s in STAGES:
        if s in ('BAD', 'SYN'):
            continue
        h0p += [f'{s}: {p}' for p in st[s]['problems']]
    pack_ok = None
    if st['P']['tech_ok']:
        A, _ = atom_map(st['P']['atoms'])
        K, _ = atom_map(st['P']['pack'])
        cols = [c for c in P['observers']['atoms_pre'] if c != 'id']
        pack_ok = set(A) == set(K) and all(A[i][c] == K[i][c] for i in A for c in cols)
        if not pack_ok:
            h0p.append('P: 끝 write_dump 묶음 ≠ in-run 마지막 덤프 (write_dump 경로)')
    rows['H0'] = {'status': 'TECH' if h0p else 'PASS', 'problems': h0p[:12], 'producer_pack_equals_inrun': pack_ok}
    # H1 · H2
    for row, cname in (('H1', 'C6'), ('H2', 'C4')):
        rt = roundtrip(st['P'], st[cname], P)
        rows[row] = {'status': rt['status'], 'stage': cname, 'np': st[cname].get('np'), 'classes': rt.get('classes'),
                     'sentinels': rt.get('sentinels'), 'dup_consistent': rt.get('dup_consistent'), 'problems': rt.get('problems', [])[:8]}
    # H3 · H4 (양성 대조 = Cnone)
    ctrl = roundtrip(st['P'], st['Cnone'], P)
    for row, e, cname, wall in (('H3', 'Ebot', 'Cbot', 'primitive'), ('H4', 'Etop', 'Ctop', 'mesh')):
        if not st['Enone']['tech_ok']:
            ctrl = dict(ctrl, status='TECH')
        er = erasure(st['P'], st[e], st[cname], ctrl, wall, P)
        rows[row] = {'status': er['status'], 'wall': wall, 'checks': er.get('checks'), 'fails': er.get('fails', [])[:6],
                     'problems': er.get('problems', [])[:6], 'sentinels': er.get('sentinels')}
    # H5 — 잘못된 ID = TECH 로 · 0 뿐 = INCONCLUSIVE 로 분류되는가
    b = st['BAD']
    if not b['exists']:
        bad_cls = 'NOT_RUN'
    else:
        err = b['screen']['errors']
        if b.get('rc') not in (None, '0') and any(('fix ID' in x) or ('history_zwallbot' in x) for x in err):
            bad_cls = 'TECH'
        elif b.get('rc') == '0' and not err:
            bad_cls = 'ACCEPTED'
        else:
            bad_cls = 'TECH_OTHER'
    zr = roundtrip(st['PZ'], st['CZ'], P)
    zero_cls = zr['status']
    if zero_cls == 'INCONCLUSIVE' and st['PZ']['tech_ok']:
        pm = prim_map(st['PZ']['atoms'], P)
        if any(any(h) for h in pm.values()) or st['PZ']['mesh']['rows'] or st['PZ']['pair']['rows']:
            zero_cls = 'NOT_ZERO'
    if bad_cls == 'TECH' and zero_cls == 'INCONCLUSIVE':
        h5 = 'PASS'
    elif bad_cls in ('NOT_RUN', 'TECH_OTHER') or zero_cls == 'TECH':
        h5 = 'TECH'
    else:
        h5 = 'FAIL'
    rows['H5'] = {'status': h5, 'bad_id_class': bad_cls, 'zero_class': zero_cls,
                  'bad_id_error': (b.get('screen') or {}).get('errors', [])[:2]}
    #  생산자 단계가 없으면 모든 행 TECH (판정 근거 없음)
    if not st['P']['tech_ok']:
        for r in rows.values():
            r['status'] = 'TECH'
    # 정보 (판정 밖)
    S = P['steps']
    ends = {S['load'], S['load'] + S['shear'], S['load'] + S['shear'] + S['hold']}
    auto = st['P'].get('auto', [])
    info['auto_restart_steps'] = auto
    info['auto_end_of_run_restart'] = any(s in ends and s % S['auto_restart_every'] for s in auto) if st['P']['exists'] else None
    info['auto_note'] = ('run 끝 step (주기 배수 아님) 에 자동 restart 가 생겼다' if info['auto_end_of_run_restart']
                         else 'run 끝 자동 restart 없음 — 주기 배수만 (10:0 연장 끝 3,660,000 은 명시 write_restart 가 필요)')
    ft = None
    if st['P']['tech_ok']:
        A, _ = atom_map(st['P']['atoms'])
        zids = [i for i, p in enumerate(P['particles'], start=1) if p['set'] == 'Z']
        ft = 'PASS' if all(A[i]['fx'] == 0 and A[i]['fy'] == 0 and _close(A[i]['fz'], -A[i]['mass'] * G, P['tolerances']['gravity_rel'], 0)
                           for i in zids) else 'FAIL'
    info['force_timing'] = ft
    info['force_timing_note'] = '접촉 없는 입자 (Z) 의 덤프 fz = −m g · fx = fy = 0 → 덤프 f 는 중력까지 더한 총힘 (출력 = post_force 뒤 · S3 함수 입력)'
    info['syn'] = syn_info(run_dir, st['P'], P)
    info['stage_np'] = {s: st[s].get('np') for s in STAGES if st[s]['exists']}
    v = {'schema': 'ps45_unload_history_verdict_v1', 'run_dir': os.path.abspath(run_dir), 'rows': rows, 'info': info}
    v['exit_code'] = 0 if all(rows[f'H{i}']['status'] == 'PASS' for i in range(6)) else 2
    return v


# ── 문법 fixture (Q8 · 등록 개정 3 §14-9 · Codex 판정문 10-14 §6) — P → GA (처음) → GB (이어 돌림 · 새 프로세스) ──────────────────

def grammar_expect(P):
    """문법 fixture 기대 (표에서 · 결과 전 고정) — 창 끝 step · 판 z · run 꼴 · 판 mesh/stl 을 볼 step (이동 앞 · 반 · 끝 · 창 끝)."""
    Y, S = P['grammar_probe'], P['steps']
    s0 = S['load'] + S['shear'] + S['hold']
    W, n, kf = Y['window'], Y['n_move'], Y['k_fresh']
    dz = Y['v'] * Y['dt'] * n
    zp = P['z_plate']
    ends = [s0 + W + k * (n + W) for k in range(kf + 2)]
    z = [zp + k * dz for k in range(kf + 2)]

    def mesh(start, z_start, ks):
        m = {start: z_start}
        for k in ks:
            a = ends[k - 1]
            m[a] = z[k - 1]
            m[a + n // 2] = z[k - 1] + dz / 2.0
            m[a + n] = z[k]
            m[ends[k]] = z[k]
        return m
    ga_mesh = mesh(s0, zp, range(1, kf + 1))
    ga_mesh[ends[0]] = z[0]
    ga = {'start': s0, 'z0': zp, 'ks': list(range(kf + 1)), 'ends': ends[:kf + 1], 'z': z[:kf + 1], 'mesh': ga_mesh,
          'runs': [(s0, W, False)] + [r for k in range(1, kf + 1) for r in ((ends[k - 1], n, True), (ends[k - 1] + n, W, False))]}
    gb = {'start': ends[kf], 'z0': z[kf], 'ks': [kf + 1], 'ends': [ends[kf + 1]], 'z': [z[kf + 1]], 'mesh': mesh(ends[kf], z[kf], [kf + 1]),
          'runs': [(ends[kf], n, True), (ends[kf] + n, W, False)]}
    return {'GA': ga, 'GB': gb, 'dz': dz}


def _kv(line):
    return dict(x.split('=', 1) for x in line.split()[1:] if '=' in x)


def _int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def _fl(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def gram_markers_ok(lines, e, resumed):
    """화면 표지 (GRAM_*) ↔ 기대 → 문제 목록 (빈 목록 = 맞음).  생성기 모의기 시험 (make_history_decks ⑯) 도 같은 함수를 쓴다.
    처음 (GA) = GRAM_START (S0 · k 0 · 판 z₀) · 이어 돌림 (GB) = GRAM_RESUMED (상태 파일의 step · k · 판 z) — 다른 쪽 표지가 있으면 그 경로가 아니다."""
    pr = []
    M = [ln.strip() for ln in lines if ln.strip().startswith('GRAM_')]
    head, other = ('GRAM_RESUMED', 'GRAM_START') if resumed else ('GRAM_START', 'GRAM_RESUMED')
    hs = [_kv(m) for m in M if m.split()[0] == head]
    k0 = e['ks'][0] - 1 if resumed else 0
    if len(hs) != 1:
        pr.append(f'{head} {len(hs)} 개 (기대 1)')
    elif _int(hs[0].get('step')) != e['start'] or _int(hs[0].get('k')) != k0 or _fl(hs[0].get('plate_z')) is None \
            or abs(_fl(hs[0].get('plate_z')) - e['z0']) > 1e-12:
        pr.append(f'{head} {hs[0]} ≠ 기대 step {e["start"]} · k {k0} · 판 {e["z0"]!r}')
    if any(m.split()[0] == other for m in M):
        pr.append(f'{other} 가 있다 (다른 경로)')
    if any(m.split()[0] == 'GRAM_ABORT' for m in M):
        pr.append('GRAM_ABORT')
    steps = [_kv(m) for m in M if m.split()[0] == 'GRAM_STEP']
    if [(_int(s.get('k')), _int(s.get('step'))) for s in steps] != list(zip(e['ks'], e['ends'])):
        pr.append(f'GRAM_STEP (k · step) {[(s.get("k"), s.get("step")) for s in steps]} ≠ {list(zip(e["ks"], e["ends"]))}')
    for s, z in zip(steps, e['z']):
        if _fl(s.get('plate_z')) is None or abs(_fl(s.get('plate_z')) - z) > 1e-12 or _fl(s.get('Ps_avg')) is None \
                or _int(s.get('n_contact_geo')) is None or _int(s.get('n_contact_geo')) < 0:
            pr.append(f'GRAM_STEP {s} — 판 z ≠ {z!r} · 또는 Ps · 접촉 수 비유한')
    sw = [_kv(m) for m in M if m.split()[0] == 'GRAM_STATE_WRITTEN']
    if [(_int(s.get('k')), _int(s.get('step'))) for s in sw] != list(zip(e['ks'], e['ends'])):
        pr.append(f'GRAM_STATE_WRITTEN {[(s.get("k"), s.get("step")) for s in sw]}')
    dn = [_kv(m) for m in M if m.split()[0] == 'GRAM_DONE']
    if len(dn) != 1 or _int(dn[0].get('step')) != e['ends'][-1] or _int(dn[0].get('k')) != e['ks'][-1] \
            or _fl(dn[0].get('plate_z')) is None or abs(_fl(dn[0].get('plate_z')) - e['z'][-1]) > 1e-12:
        pr.append(f'GRAM_DONE {dn} ≠ step {e["ends"][-1]} · k {e["ks"][-1]}')
    return pr


def _stl_z(path):
    if not os.path.exists(path):
        return None
    zs = [_fl(x) for x in re.findall(r'vertex\s+\S+\s+\S+\s+(\S+)', open(path, encoding='utf-8', errors='replace').read())]
    return zs if zs and all(z is not None for z in zs) else None


def _vars(d):
    t = _readf(os.path.join(d, 'vars.txt')) or ''
    return dict(ln.split('=', 1) for ln in t.splitlines() if '=' in ln)


def _same(a, b):
    return bool(a) and bool(b) and os.path.realpath(a) == os.path.realpath(b)


def _gram_stage(run_dir, name, e, P):
    """GA · GB 한 단계 → 검사 (모두 참이어야) · 문제."""
    d = os.path.join(run_dir, name)
    out = {'exists': os.path.isdir(d), 'checks': {}, 'problems': []}
    if not out['exists']:
        return out
    Y = P['grammar_probe']
    c, pr = out['checks'], out['problems']
    rc, np_ = _readf(os.path.join(d, 'rc')), _readf(os.path.join(d, 'np.txt'))
    S = screen_info(d)
    npi = int(np_) if np_ and np_.isdigit() else None
    c[f'{name}_tech'] = (rc == '0' and S['banner'] and S['git'] and not S['errors'] and npi is not None and len(S['loops']) == len(e['runs'])
                         and all(x == npi for x in S['loops']))
    if not c[f'{name}_tech']:
        pr.append(f'{name} 기술: rc {rc} · 배너 {S["banner"]} · ERROR {S["errors"][:2]} · Loop procs {S["loops"]} (기대 run {len(e["runs"])} · NP {npi})')
    mp = gram_markers_ok(S['markers'], e, resumed=(name == 'GB'))
    c[f'{name}_markers'] = not mp
    pr += [f'{name} 표지: {x}' for x in mp]
    # 변수 주기 덤프 (dump_modify every v_) — 창 끝만 · setup · 이동 중 없음 · 머리 step = 파일 step · 전부 읽힘
    frames = {}
    for kind, cols, style in (('atom', Y['atom_cols'], 'custom'), ('wall', [f'c_gr_wh[{i}]' for i in range(1, 7)], 'local')):
        fs = sorted(glob.glob(os.path.join(d, 'probe', f'{kind}_*.dump')))
        steps = sorted(int(re.search(r'_(\d+)\.dump$', p).group(1)) for p in fs)
        ok = steps == e['ends']
        for p in fs:
            s = int(re.search(r'_(\d+)\.dump$', p).group(1))
            dd = read_dump(p, style, cols)
            frames[(kind, s)] = dd
            if not dd['ok'] or dd['step'] != s or (kind == 'atom' and len(dd['rows']) != len(P['particles'])):
                ok = False
                pr.append(f'{name} {os.path.basename(p)}: {dd["problems"][:2]} · 머리 step {dd["step"]}')
        c[f'{name}_{kind}_dump_steps'] = ok
        if steps != e['ends']:
            pr.append(f'{name} {kind} 덤프 step {steps} ≠ 창 끝 {e["ends"]} (setup · 이동 중 덤프?)')
    # 판 z (mesh/stl 고정 주기) — 이동 앞 · 반 · 끝 · 창 끝 · 새 프로세스 첫 setup (복원)
    bad = []
    for s, z in sorted(e['mesh'].items()):
        zs = _stl_z(os.path.join(d, 'probe', f'mesh_{s}.stl'))
        if zs is None or any(abs(x - z) > Y['z_tol'] for x in zs):
            bad.append((s, z, (zs or [None])[0]))
    c[f'{name}_mesh_z'] = not bad
    if bad:
        pr.append(f'{name} 판 z (step · 기대 · 실제) {bad[:4]}')
    # 단 끝 restart + 상태 파일 (file · append — rstep · k · pz)
    rs = sorted(int(re.search(r'restart_g_(\d+)\.bin$', p).group(1)) for p in glob.glob(os.path.join(d, 'restart', 'restart_g_*.bin')))
    ok = rs == e['ends']
    for k, s, z in zip(e['ks'], e['ends'], e['z']):
        t = _readf(os.path.join(d, 'restart', f'state_g_{s}.in')) or ''
        L = [ln.split() for ln in t.splitlines() if ln.strip()]
        want = [('gr_rstep', s), ('gr_k', k), ('gr_pz', z)]
        if len(L) != 3 or any(len(w) != 4 or w[:3] != ['variable', nm, 'equal'] or _fl(w[3]) is None or abs(_fl(w[3]) - v) > 1e-12
                              for w, (nm, v) in zip(L, want)):
            ok = False
            pr.append(f'{name} 상태 파일 state_g_{s}.in = {t!r} ≠ {want}')
    c[f'{name}_restart_state'] = ok
    if rs != e['ends']:
        pr.append(f'{name} restart_g step {rs} ≠ {e["ends"]}')
    # 판 접촉 개수 (영역 공식 · 덱) ↔ 판 local 덤프 (판 아래 중심) — 단마다 영역을 다시 만든 것이 맞는가 (본 키트 ul_c1–3 꼴)
    ok = True
    for m in S['markers']:
        if m.split()[0] != 'GRAM_STEP':
            continue
        kv = _kv(m)
        s, pz, ng = _int(kv.get('step')), _fl(kv.get('plate_z')), _int(kv.get('n_contact_geo'))
        A, Wl = frames.get(('atom', s)), frames.get(('wall', s))
        if A is None or Wl is None or pz is None or ng is None:
            ok = False
            continue
        zs = {int(r['id']): r['z'] for r in A['rows']}
        below = {int(r['c_gr_wh[3]']) for r in Wl['rows'] if zs.get(int(r['c_gr_wh[3]']), math.inf) < pz}
        if ng != len(below):
            ok = False
            pr.append(f'{name} step {s}: 영역 판 접촉 {ng} ≠ 판 local 덤프 {len(below)}')
    c[f'{name}_contact_geo'] = ok
    return out


def grammar_info(run_dir, P=None):
    """문법 fixture 판정 (Q8 · 등록 개정 3 §14-9) — 검사 전부 참 = PASS · 하나라도 아니면 FAIL · GA 없음 = NOT_RUN.  짧은 문법 런 = 물리 검증 아님 (C19)."""
    P = P or load_params()
    e = grammar_expect(P)
    out = {'schema': 'ps45_unload_grammar_verdict_v1', 'run_dir': os.path.abspath(run_dir), 'status': 'NOT_RUN', 'checks': {}, 'problems': [],
           'expect': {s: {'start': e[s]['start'], 'ends': e[s]['ends'], 'z': e[s]['z']} for s in ('GA', 'GB')}}
    if not os.path.isdir(os.path.join(run_dir, 'GA')):
        out['problems'].append('GA 단계 폴더 없음')
        out['exit_code'] = 2
        return out
    c = out['checks']
    prod = load_stage(run_dir, 'P', P)
    c['P_tech'] = bool(prod.get('tech_ok'))
    if not c['P_tech']:
        out['problems'] += [f'P: {p}' for p in prod.get('problems', [])[:4]]
    for name in ('GA', 'GB'):
        st = _gram_stage(run_dir, name, e[name], P)
        c[f'{name}_exists'] = st['exists']
        if not st['exists']:
            out['problems'].append(f'{name} 단계 폴더 없음 (이어 돌림 경로 미시험)' if name == 'GB' else f'{name} 없음')
            continue
        c.update(st['checks'])
        out['problems'] += st['problems']
    ga, gb = os.path.join(run_dir, 'GA'), os.path.join(run_dir, 'GB')
    va, vb = _vars(ga), _vars(gb)
    last = e['GA']['ends'][-1]
    fresh = va.get('gr_state', '')
    c['GA_args'] = (va.get('gr_resume') == '0' and _same(_readf(os.path.join(ga, 'ckpt.txt')), os.path.join(run_dir, 'P', 'fixture.bin'))
                    and os.path.exists(fresh) and not re.search(r'^\s*variable', open(fresh, encoding='utf-8').read(), re.M))
    if c['GB_exists']:
        c['GB_args'] = (vb.get('gr_resume') == '1' and _same(_readf(os.path.join(gb, 'ckpt.txt')), os.path.join(ga, 'restart', f'restart_g_{last}.bin'))
                        and _same(vb.get('gr_state'), os.path.join(ga, 'restart', f'state_g_{last}.in')))
        if not c['GB_args']:
            out['problems'].append(f'GB 입력 ≠ GA 마지막 단 끝 restart_g_{last}.bin + state_g_{last}.in · gr_resume 1 ({vb} · ckpt {_readf(os.path.join(gb, "ckpt.txt"))})')
    out['status'] = 'PASS' if all(v is True for v in c.values()) else 'FAIL'
    out['exit_code'] = 0 if out['status'] == 'PASS' else 2
    return out


def grammar_text(v):
    L = [f'GRAMMAR_VERDICT status={v["status"]} (0 = 맨 바깥 include 이어 돌림 · 변수 주기 덤프 · move/mesh 여러 번 · 상태 파일 복귀 전부 기대대로)']
    for k, ok in v['checks'].items():
        L.append(f'  {"✓" if ok is True else "✗"} {k}')
    for p in v['problems'][:12]:
        L.append(f'      · {p}')
    L.append(f'  rc = {v["exit_code"]} · 짧은 문법 런 = 물리 검증 아님 (C19)')
    return '\n'.join(L)


# ── 합성 단계 (selftest · 러너 모의 시험) — 덱이 쓰는 덤프 · 화면 꼴 그대로 ─────────────────────────────

def _design(P):
    """생성기의 설계 (자리 · 반경 · 밀도) — selftest · 모의 시험에서만 부른다 (판정 경로는 덤프 · 표만 읽는다)."""
    sys.path.insert(0, HERE)
    import make_history_decks as M  # noqa: E402 — 같은 폴더 생성기 (합성 자료 전용)
    D = M.fixture_design(P)
    H = M.extract_head(P)
    return D, H


def _state(P, zero=False):
    """생산자 끝 상태 (설계대로) → {'atoms': {id: dict}, 'mesh': [rows], 'pair': [rows], 'step': 2000}."""
    D, H = _design(P)
    if zero:
        sys.path.insert(0, HERE)
        import make_history_decks as M  # noqa: E402
        D = M.fixture_design(P, zero=True)
    S = P['steps']
    step = S['load'] + S['shear'] + S['hold']
    dt = D['dt']
    atoms, mesh, pair = {}, [], []
    names = {q['name']: q for q in D['parts']}
    for q in D['parts']:
        r = q['r']
        rho = H['density'][q['type']]
        m = rho * 4.0 / 3.0 * math.pi * r ** 3
        x, y, z = q['unl']
        a = dict(id=q['id'], type=q['type'], x=x, y=y, z=z, radius=r, mass=m, vx=0.0, vy=0.0, vz=0.0, omegax=0.0, omegay=0.0, omegaz=0.0,
                 fx=0.0, fy=0.0, fz=-m * G, h=[0.0, 0.0, 0.0, 0.0])
        s = [c * S['shear'] * dt for c in q['v']]
        if not zero and q['set'] == 'B':
            a['h'] = [q['dmax'], s[0], s[1], s[2]]
            a['fz'] += 1.0
        if not zero and q['set'] == 'T':
            tri = 0 if x > y else 1
            mesh.append([0.0, float(tri), float(q['id']), q['dmax'], s[0], s[1], s[2]])
        if not zero and q.get('role') == 'mover':
            an = names[[n for n, v in names.items() if v.get('pair') == q['pair'] and v.get('role') == 'anchor'][0]]
            pair.append([float(an['id']), float(q['id']), 0.0, q['dmax'], -s[0], -s[1], -s[2]])
        atoms[q['id']] = a
    return {'atoms': atoms, 'mesh': mesh, 'pair': pair, 'step': step}


def _wcustom(path, step, cols, atoms, box=(0.0, 0.05, 0.0, 0.05, -0.01, 0.1), order=None, mutate=None):
    ids = order or sorted(atoms)
    lines = ['ITEM: TIMESTEP', str(step), 'ITEM: NUMBER OF ATOMS', str(len(ids)), 'ITEM: BOX BOUNDS pp pp ff',
             f'{box[0]!r} {box[1]!r}', f'{box[2]!r} {box[3]!r}', f'{box[4]!r} {box[5]!r}', 'ITEM: ATOMS ' + ' '.join(cols)]
    for i in ids:
        a = atoms[i]
        row = []
        for c in cols:
            if c in ('id', 'type'):
                row.append(str(int(a[c])))
            elif c.startswith('f_history'):
                k = int(c[c.index('[') + 1:-1])
                row.append(repr(float(a['h'][k - 1])))
            else:
                row.append(repr(float(a[c])))
        lines.append(' '.join(row))
    if mutate:
        lines = mutate(lines)
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def _wlocal(path, step, cols, rows, box=(0.0, 0.05, 0.0, 0.05, -0.01, 0.1)):
    lines = ['ITEM: TIMESTEP', str(step), 'ITEM: NUMBER OF ENTRIES', str(len(rows)), 'ITEM: BOX BOUNDS pp pp ff',
             f'{box[0]!r} {box[1]!r}', f'{box[2]!r} {box[3]!r}', f'{box[4]!r} {box[5]!r}', 'ITEM: ENTRIES ' + ' '.join(cols)]
    lines += [' '.join(repr(float(v)) for v in r) for r in rows]
    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


RESET_LINE = 'Resetting {kind} state of Fix {fid} Style {style} from restart file info'


def _wscreen(path, np_, resets=(), markers=(), error=None, banner=True, loops=1):
    L = []
    if banner:
        L.append('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2026-03-26-14:37:06 by user, git commit '
                 '3d5c00f20519e6bb6eb6756f51f1ad36564e649d)')
    for fid, style, kinds in resets:
        for k in kinds:
            L.append(RESET_LINE.format(kind=k, fid=fid, style=style))
    L += list(markers)
    for _ in range(loops):
        L.append(f'Loop time of 0.001 on {np_} procs for 0 steps with 20 atoms')
    if error:
        L.append(error)
    with open(path, 'w') as f:
        f.write('\n'.join(L) + '\n')


def synth_stage(stage, d, P=None, scenario='good', np_override=None, write_meta=True):
    """한 단계 폴더에 덱이 쓸 파일을 흉내 낸다 (scenario = 반례 이름 · selftest 표) → rc.
    write_meta = np.txt · rc 도 쓴다 (selftest) · 러너 모의 (--mock-stage) 는 러너가 쓴다."""
    P = P or load_params()
    O = P['observers']
    os.makedirs(os.path.join(d, 'producer'), exist_ok=True)
    os.makedirs(os.path.join(d, 'restart'), exist_ok=True)
    os.makedirs(os.path.join(d, 'probe'), exist_ok=True)
    np_ = np_override or (P['np_alt'] if stage == 'C4' else P['np_main'])
    if write_meta:
        with open(os.path.join(d, 'np.txt'), 'w') as f:
            f.write(f'{np_}\n')
    zero = stage in ('PZ', 'CZ')
    st = _state(P, zero=zero)
    A, step = st['atoms'], st['step']
    allreset = [tuple(x[:2]) + (x[2],) for x in P['expected_reset_fixes']]
    rc = 0
    loop_np = np_ if scenario != 'loop_np_wrong' or stage != 'C6' else 1
    if stage in ('P', 'PZ'):
        _wcustom(os.path.join(d, 'producer', f'atoms_{step}.dump'), step, O['atoms_post'], A)
        pack = {k: dict(v) for k, v in A.items()}
        if scenario == 'pack_mismatch' and stage == 'P':
            pack[1]['h'] = [pack[1]['h'][0] * (1 + 1e-6)] + pack[1]['h'][1:]
        _wcustom(os.path.join(d, 'producer', 'end_pack.dump'), step, O['atoms_pre'], pack)
        if scenario == 'gravity_off' and stage == 'P':
            G2 = {k: dict(v, fz=0.0) for k, v in A.items()}
            _wcustom(os.path.join(d, 'producer', f'atoms_{step}.dump'), step, O['atoms_post'], G2)
        _wlocal(os.path.join(d, 'producer', f'mesh_{step}.dump'), step, O['mesh_local'], st['mesh'])
        _wlocal(os.path.join(d, 'producer', f'pair_{step}.dump'), step, O['pair_local'], st['pair'])
        open(os.path.join(d, 'fixture.bin'), 'wb').write(b'\0' * 64)
        for s in (1500,) + ((2000,) if scenario == 'auto_end' else ()):
            open(os.path.join(d, 'restart', f'auto_{s}.bin'), 'wb').write(b'\0')
        _wscreen(os.path.join(d, 'screen.out'), loop_np, markers=['HIST_PRODUCER_DONE step=2000 atoms=20'], loops=3)
    elif stage in ('C6', 'C4', 'Cbot', 'Ctop', 'Cnone', 'CZ', 'Ebot', 'Etop', 'Enone', 'BAD'):
        pre = {k: dict(v) for k, v in A.items()}
        post = {k: dict(v) for k, v in A.items()}
        mesh = [list(r) for r in st['mesh']]
        pair = [list(r) for r in st['pair']]
        resets = list(allreset)
        if stage == 'Cbot':
            resets = [x for x in resets if x[0] != 'history_zwall_bot']
            if scenario != 'erase_bot_ineffective':
                for a in pre.values():
                    a['h'] = [0.0, 0.0, 0.0, 0.0]
                for a in post.values():
                    a['h'] = [max(0.0, a['radius'] - a['z']), 0.0, 0.0, 0.0]
                    if scenario == 'post_all_zero':
                        a['h'] = [0.0, 0.0, 0.0, 0.0]
        if stage == 'Ctop':
            resets = [x for x in resets if x[0] != 'tracker_top_mesh']
            if scenario != 'erase_top_ineffective':
                zp = P['z_plate']
                for r in mesh:
                    a = A[int(r[2])]
                    r[3:7] = [a['z'] + a['radius'] - zp, 0.0, 0.0, 0.0]
            if scenario == 'erase_top_touches_bot':
                for a in pre.values():
                    a['h'] = [0.0, 0.0, 0.0, 0.0]
        if stage == 'C6' and scenario == 'h1_dmax_mismatch':
            pre[1]['h'] = [pre[1]['h'][0] * 0.999] + pre[1]['h'][1:]
        if stage == 'C6' and scenario == 'missing_reset':
            resets = [x for x in resets if x[0] != 'tracker_top_mesh']
        if stage == 'C4' and scenario in ('h2_pair_reversed', 'h2_pair_reversed_no_neg'):
            sign = -1.0 if scenario == 'h2_pair_reversed' else 1.0
            pair = [[r[1], r[0], r[2], r[3], sign * r[4], sign * r[5], sign * r[6]] for r in pair]
        if stage == 'C4' and scenario in ('dup_consistent', 'dup_conflict'):
            extra = list(pair[0])
            if scenario == 'dup_conflict':
                extra[3] *= 2.0             # 같은 키 · 다른 deltaMax
            pair.append(extra)
        if stage == 'C4' and scenario == 'order_shuffle':
            pair = list(reversed(pair))
            mesh = list(reversed(mesh))
        order = sorted(A, reverse=(stage == 'C4' and scenario == 'order_shuffle'))
        def _drop_last_col(lines):
            k = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ATOMS'))
            return lines[:k] + [lines[k].rsplit(' ', 1)[0]] + [x.rsplit(' ', 1)[0] for x in lines[k + 1:]]

        def _nan_first(lines):
            k = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ATOMS'))
            lines[k + 1] = lines[k + 1].rsplit(' ', 1)[0] + ' nan'
            return lines
        mutate = {'missing_col': _drop_last_col, 'nan': _nan_first}.get(scenario) if stage == 'C6' else None
        if stage == 'BAD':
            ok = scenario == 'bad_ok'
            if ok:
                _wcustom(os.path.join(d, 'pre_atoms.dump'), step, O['atoms_pre'], pre)
            _wscreen(os.path.join(d, 'screen.out'), np_, resets=resets[:1],
                     error=None if ok else 'ERROR: Could not find dump custom fix ID history_zwallbot (../dump_custom.cpp:1386)',
                     loops=1 if ok else 0)
            rc = 0 if ok else 1
        else:
            _wcustom(os.path.join(d, 'pre_atoms.dump'), step, O['atoms_pre'], pre, order=order, mutate=mutate)
            _wcustom(os.path.join(d, f'post_atoms_{step}.dump'), step, O['atoms_post'], post, order=order)
            _wlocal(os.path.join(d, f'post_mesh_{step}.dump'), step, O['mesh_local'], mesh)
            _wlocal(os.path.join(d, f'post_pair_{step}.dump'), step, O['pair_local'], pair)
            marks = ['HIST_CONSUMER_START step=2000 atoms=20']
            if stage.startswith('E'):
                open(os.path.join(d, 'erased.bin'), 'wb').write(b'\0' * 32)
                marks.append(f'HIST_ERASE_DONE mode={stage[1:]} step=2000')
            else:
                marks.append('HIST_CONSUMER_DONE step=2000 atoms=20')
            _wscreen(os.path.join(d, 'screen.out'), loop_np, resets=resets, markers=marks)
    elif stage == 'SYN':
        zp = P['z_plate']
        Y = P['syntax_probe']
        lift = Y['lift_v'] * Y['dt'] * Y['lift_steps']
        T = [a for a in A.values() if a['z'] < zp and a['z'] + a['radius'] > zp]
        s0, s1 = step + Y['window'], step + Y['window'] + Y['lift_steps'] + Y['window']
        T1 = [a for a in T if a['z'] + a['radius'] > zp + lift]
        wcols = [f'c_u_wh[{i}]' for i in range(1, 7)]
        sg = {'syn_fn_positive': [1.0], 'syn_fn_mixed': [-1.0, 1.0]}.get(scenario, [-1.0])
        _wlocal(os.path.join(d, 'probe', f'mesh_{s0}.dump'), s0, wcols,
                [[0.0, 0.0, float(a['id']), 0.0, 0.0, sg[j % len(sg)] * 0.5] for j, a in enumerate(T)])
        _wlocal(os.path.join(d, 'probe', f'mesh_{s1}.dump'), s1, wcols,
                [[0.0, 0.0, float(a['id']), 0.0, 0.0, sg[j % len(sg)] * 0.3] for j, a in enumerate(T1)])
        for s, z in ((s0, zp), (s1 - Y['window'], zp + lift)):
            with open(os.path.join(d, 'probe', f'plate_{s}.stl'), 'w') as f:
                f.write('solid LIGGGHTS_STL_EXPORT\n' + ''.join(f'      vertex 0 0 {z:g}\n' for _ in range(6)) + 'endsolid LIGGGHTS_STL_EXPORT\n')
        open(os.path.join(d, 'probe_end.bin'), 'wb').write(b'\0')
        n0 = len(T) if scenario != 'syn_count_wrong' else len(T) + 1
        marks = [f'SYN_W0 step={s0} Ps_avg=0.004 ke_avg=0 erot_avg=0 n_contact_geo={n0} plate_z={zp!r} dt=5e-07',
                 f'SYN_W1 step={s1} Ps_avg=0.003 ke_avg=0 erot_avg=0 n_contact_geo={len(T1)} plate_z={zp + lift!r} dt=5e-07', 'SYN_DONE']
        _wscreen(os.path.join(d, 'screen.out'), np_, resets=allreset, markers=marks, loops=3)
    elif stage in ('GA', 'GB'):
        rc = _synth_gram(stage, d, P, scenario, np_, A, write_meta)
    else:
        raise KeyError(stage)
    if write_meta:
        with open(os.path.join(d, 'rc'), 'w') as f:
            f.write(f'{rc}\n')
    return rc


def synth_run(root, P=None, scenario='good', skip=()):
    P = P or load_params()
    for s in STAGES:
        if s in skip:
            continue
        synth_stage(s, os.path.join(root, s), P, scenario)


def _g(x):
    return '%.15g' % x


def _synth_gram(stage, d, P, scenario, np_, A, write_meta):
    """문법 fixture 단계 (GA · GB) 가 쓸 파일 (덱 in.hist_grammar 꼴 그대로) — 판 z = 선형 이동 모형 · 덤프 = 창 끝 · 상태 파일 · 화면 표지.
    scenario = 반례 (selftest 표) · write_meta = 러너가 쓰는 np.txt · rc · vars.txt · ckpt.txt 도 쓴다 (selftest)."""
    E = grammar_expect(P)
    e = E[stage]
    Y = P['grammar_probe']
    W, vdt = Y['window'], Y['v'] * Y['dt']
    zp = P['z_plate']
    for sub in ('probe', 'restart'):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    # 판 z — run 마다 (이동이면 v · dt · Δstep) · mesh/stl = 창 배수 step 전부
    ztab, z = {}, e['z0']
    for i, (s, n, mv) in enumerate(e['runs']):
        base = z
        if scenario == 'gram_rewind' and stage == 'GA' and mv and i > 1:
            base = zp                                    # 두 번째 이동이 원점에서 다시 (되감김 반례)
        for t in range(s, s + n + 1, W):
            ztab.setdefault(t, base + (vdt * (t - s) if mv else 0.0))
        z = base + (vdt * n if mv else 0.0)
    if scenario == 'gram_not_restored' and stage == 'GB':
        ztab[e['start']] = zp                            # 새 프로세스 첫 setup 에서 판이 원 자리
    for t, zz in ztab.items():
        with open(os.path.join(d, 'probe', f'mesh_{t}.stl'), 'w') as f:
            f.write('solid LIGGGHTS_STL_EXPORT\n' + ''.join(f'      vertex 0 0 {zz:g}\n' for _ in range(6)) + 'endsolid LIGGGHTS_STL_EXPORT\n')
    # 변수 주기 덤프 (원자 · 판 local) — 창 끝
    dsteps = list(e['ends'])
    if stage == 'GA' and scenario == 'gram_setup_dump':
        dsteps = [e['start']] + dsteps
    if stage == 'GA' and scenario == 'gram_move_dump':
        dsteps.append(e['ends'][0] + Y['n_move'] // 2)
    ncon = {}
    for t in dsteps:
        pz = ztab.get(t, e['z0'])
        _wcustom(os.path.join(d, 'probe', f'atom_{t}.dump'), t, Y['atom_cols'], A)
        rows = [[0.0, 0.0 if a['x'] > a['y'] else 1.0, float(i), 0.0, 0.0, -0.5] for i, a in sorted(A.items()) if a['z'] < pz < a['z'] + a['radius']]
        _wlocal(os.path.join(d, 'probe', f'wall_{t}.dump'), t, [f'c_gr_wh[{i}]' for i in range(1, 7)], rows)
        ncon[t] = len(rows)
    # 단 끝 restart + 상태 파일
    for k, t, zk in zip(e['ks'], e['ends'], e['z']):
        open(os.path.join(d, 'restart', f'restart_g_{t}.bin'), 'wb').write(b'\0' * 16)
        zw = zp if (scenario == 'gram_state_bad' and stage == 'GA' and t == e['ends'][-1]) else zk
        with open(os.path.join(d, 'restart', f'state_g_{t}.in'), 'w') as f:
            f.write(f'variable gr_rstep equal {t}\nvariable gr_k equal {k}\nvariable gr_pz equal {_g(zw)}\n')
    # 화면 표지
    fresh = stage == 'GA' or scenario == 'gram_resume_fresh'
    marks = ([f'GRAM_START step={e["start"]} k=0 plate_z={_g(e["z0"])}'] if fresh
             else [f'GRAM_RESUMED step={e["start"]} k={e["ks"][0] - 1} plate_z={_g(e["z0"])}'])
    for k, t, zk in zip(e['ks'], e['ends'], e['z']):
        marks += [f'GRAM_STEP k={k} step={t} plate_z={_g(zk)} Ps_avg=0.001 n_contact_geo={ncon[t]}', f'GRAM_STATE_WRITTEN step={t} k={k}']
    marks.append(f'GRAM_DONE step={e["ends"][-1]} k={e["ks"][-1]} plate_z={_g(e["z"][-1])}')
    bad_rc = stage == 'GB' and scenario == 'gram_gb_rc'
    nloop = len(e['runs']) - (1 if (stage == 'GA' and scenario == 'gram_runs') else 0)
    _wscreen(os.path.join(d, 'screen.out'), np_, markers=marks, loops=nloop, error='ERROR: mock grammar failure' if bad_rc else None)
    if write_meta:   # 러너가 쓰는 입력 기록 (selftest 에서 흉내 — GA = 생산자 fixture · 빈 상태 · GB = GA 마지막 단 끝)
        root = os.path.dirname(d)
        last = E['GA']['ends'][-1]
        if stage == 'GA':
            st = os.path.join(d, 'state_fresh.in')
            open(st, 'w').write('# 처음 (빈 상태 파일)\n')
            ck, res = os.path.join(root, 'P', 'fixture.bin'), '0'
        else:
            ckstep = E['GA']['ends'][-2] if scenario == 'gram_wrong_ckpt' else last
            ck, st, res = (os.path.join(root, 'GA', 'restart', f'restart_g_{ckstep}.bin'), os.path.join(root, 'GA', 'restart', f'state_g_{ckstep}.in'), '1')
        open(os.path.join(d, 'ckpt.txt'), 'w').write(ck + '\n')
        open(os.path.join(d, 'vars.txt'), 'w').write(f'gr_state={st}\ngr_resume={res}\n')
    return 1 if bad_rc else 0


def synth_gram_run(root, P=None, scenario='good', skip=()):
    """문법 fixture 합성 런 (P → GA → GB) — selftest 전용."""
    P = P or load_params()
    for s in ('P', 'GA', 'GB'):
        if s not in skip:
            synth_stage(s, os.path.join(root, s), P, scenario)


# ── selftest ─────────────────────────────────────────────────────────────────

def selftest() -> int:
    P = load_params()
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001 — 빈 구현 · 예외도 실패로 센다
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    def run(scenario='good', skip=(), edit=None):
        td = tempfile.mkdtemp(prefix='hist_selftest_')
        try:
            synth_run(td, P, scenario, skip)
            if edit:
                edit(td)
            return evaluate(td, P)
        finally:
            shutil.rmtree(td, ignore_errors=True)

    def rows(v):
        return {k: v['rows'][k]['status'] for k in v['rows']}

    V = {}
    chk('S1 정상 = H0–H5 전부 PASS · rc 0', lambda: V.update(run()) or (rows(V) == {f'H{i}': 'PASS' for i in range(6)} and V['exit_code'] == 0))
    chk('S1 정상: H5 안에서 잘못된 ID = TECH · 0 뿐 = INCONCLUSIVE 로 분류됐다',
        lambda: V['rows']['H5']['bad_id_class'] == 'TECH' and V['rows']['H5']['zero_class'] == 'INCONCLUSIVE')
    chk('S1 정상: sentinel 종류마다 있다 (primitive 4 · mesh 4 · pair 5)', lambda: V['rows']['H1']['sentinels'] == {'primitive': 4, 'mesh': 4, 'pair': 5})
    chk('S1 정상: 정보 — 자동 run 끝 restart 없음 (1500 만) · 총힘 출력 시점 OK · SYN 문법 OK',
        lambda: V['info']['auto_end_of_run_restart'] is False and V['info']['auto_restart_steps'] == [1500]
        and V['info']['force_timing'] == 'PASS' and V['info']['syn']['status'] == 'PASS')
    chk('S2 H1 deltaMax 하나 다름 (C6 PRE) = H1 FAIL', lambda: rows(run('h1_dmax_mismatch'))['H1'] == 'FAIL')
    chk('S3 H2 pair 방향 바뀜 + shear 부호 바뀜 = 정규화로 PASS', lambda: rows(run('h2_pair_reversed'))['H2'] == 'PASS')
    chk('S4 H2 pair 방향 바뀜 · shear 부호 그대로 = FAIL (부호 정규화가 실제로 대조한다)', lambda: rows(run('h2_pair_reversed_no_neg'))['H2'] == 'FAIL')
    chk('S5 H2 같은 값 중복 키 = PASS (중복 수 기록)', lambda: (lambda v: rows(v)['H2'] == 'PASS' and v['rows']['H2']['dup_consistent'] >= 1)(run('dup_consistent')))
    chk('S6 H2 다른 값 중복 키 = TECH', lambda: rows(run('dup_conflict'))['H2'] == 'TECH')
    chk('S7 열 하나 빠짐 (C6 PRE) = H1 TECH (H0 도 TECH)', lambda: (lambda r: r['H1'] == 'TECH' and r['H0'] == 'TECH')(rows(run('missing_col'))))
    chk('S8 비유한 값 (nan) = H1 TECH', lambda: rows(run('nan'))['H1'] == 'TECH')
    chk('S9 reset 로그 하나 빠짐 (C6 tracker) = H0 TECH', lambda: rows(run('missing_reset'))['H0'] == 'TECH')
    chk('S10 Loop time NP ≠ 단계 NP (C6 on 1 procs) = H0 TECH', lambda: rows(run('loop_np_wrong'))['H0'] == 'TECH')
    chk('S11 바닥 소거가 안 보임 (Cbot = 생산자) = H3 FAIL', lambda: rows(run('erase_bot_ineffective'))['H3'] == 'FAIL')
    chk('S12 바닥 소거 뒤 POST deltaMax = 현재 겹침 (다시 참) = H3 PASS — "setup 뒤 4 열 0" 을 기대하지 않는다',
        lambda: rows(run('good'))['H3'] == 'PASS')
    chk('S13 바닥 소거 뒤 POST deltaMax 가 접촉 중인데 0 = H3 FAIL (현재 겹침 재평가와 모순)', lambda: rows(run('post_all_zero'))['H3'] == 'FAIL')
    chk('S14 판 소거가 안 보임 (Ctop = 생산자) = H4 FAIL', lambda: rows(run('erase_top_ineffective'))['H4'] == 'FAIL')
    chk('S15 판 소거가 바닥 이력도 지움 = H4 FAIL (손대지 않은 벽 유지)', lambda: rows(run('erase_top_touches_bot'))['H4'] == 'FAIL')
    chk('S16 잘못된 ID 가 통과 (BAD rc 0) = H5 FAIL', lambda: rows(run('bad_ok'))['H5'] == 'FAIL')
    chk('S17 생산자 write_dump 묶음 ≠ in-run 덤프 = H0 TECH', lambda: rows(run('pack_mismatch'))['H0'] == 'TECH')
    chk('S18 총힘에 중력 없음 (접촉 없는 입자 fz = 0) = 정보 force_timing FAIL (H0–H5 와 따로)',
        lambda: (lambda v: v['info']['force_timing'] == 'FAIL' and rows(v)['H1'] == 'PASS')(run('gravity_off')))
    chk('S19 C4 단계 폴더 없음 = H2 TECH (나머지는 판정)', lambda: (lambda r: r['H2'] == 'TECH' and r['H1'] == 'PASS')(rows(run(skip=('C4',)))))
    chk('S20 행 순서 섞임 = PASS', lambda: rows(run('order_shuffle'))['H2'] == 'PASS')
    chk('S21 0 뿐 fixture 를 주 소비자 자리 (C6) 에 넣으면 H1 = INCONCLUSIVE (PASS 아님)',
        lambda: rows(run(edit=lambda td: (shutil.rmtree(os.path.join(td, 'P')), shutil.copytree(os.path.join(td, 'PZ'), os.path.join(td, 'P')),
                                           shutil.rmtree(os.path.join(td, 'C6')), shutil.copytree(os.path.join(td, 'CZ'), os.path.join(td, 'C6')))))['H1']
        == 'INCONCLUSIVE')
    chk('S22 run 끝 자동 restart (auto_2000) = 정보 auto_end_of_run_restart True', lambda: run('auto_end')['info']['auto_end_of_run_restart'] is True)
    chk('S23 SYN 판 접촉 개수 (영역) ≠ 벽 local 덤프 = 정보 SYN FAIL (판정 밖)',
        lambda: (lambda v: v['info']['syn']['status'] == 'FAIL' and v['exit_code'] == 0)(run('syn_count_wrong')))
    chk('S30 SYN 판 접촉 법선력 (입자가 받는 힘) 이 모두 −z = 정보 plate_fn_sign −1 (압축 = 음수 약속)',
        lambda: (lambda s: s['plate_fn_sign'] == -1 and s['status'] == 'PASS')(run()['info']['syn']))
    chk('S31 SYN 판 접촉 법선력이 모두 +z = 정보 plate_fn_sign +1 (약속을 거꾸로 — 본 키트 표를 고칠 근거 · SYN 은 PASS)',
        lambda: (lambda s: s['plate_fn_sign'] == 1 and s['status'] == 'PASS')(run('syn_fn_positive')['info']['syn']))
    chk('S32 SYN 판 접촉 법선력 부호가 섞임 = 정보 MIXED · SYN FAIL', lambda: (lambda s: s['plate_fn_sign'] == 'MIXED' and s['status'] == 'FAIL')(run('syn_fn_mixed')['info']['syn']))
    chk('S24 생산자 폴더 없음 = H0–H5 TECH · rc ≠ 0', lambda: (lambda v: all(s == 'TECH' for s in rows(v).values()) and v['exit_code'] != 0)(run(skip=('P',))))
    # 문법 fixture (Q8 · 등록 개정 3 §14-9) — P → GA (처음 · 이동 둘) → GB (GA 마지막 단 끝 restart + 상태 파일 · 새 프로세스 · 이동 하나)
    def grun(scenario='good', skip=()):
        td = tempfile.mkdtemp(prefix='gram_selftest_')
        try:
            synth_gram_run(td, P, scenario, skip)
            return grammar_info(td, P)
        finally:
            shutil.rmtree(td, ignore_errors=True)
    G = {}
    chk('S33 문법 fixture 정상 = PASS (맨 바깥 include 이어 돌림 · 변수 주기 덤프 = 창 끝만 · move/mesh 셋 판 z 누적 · 상태 파일 복귀 · 새 프로세스 판 z 복원)',
        lambda: G.update(grun()) or (G['status'] == 'PASS' and G['exit_code'] == 0 and all(v is True for v in G['checks'].values())))
    for sc, what in (('gram_setup_dump', 'GA 첫 run 시작 (2000) 에 원자 · 판 덤프 (setup 쓰기)'), ('gram_move_dump', 'GA 이동 중 (2600) 원자 덤프'),
                     ('gram_rewind', '두 번째 이동이 원점에서 다시 (판 z 0.03001 에서 멈춤 · 되감김)'), ('gram_resume_fresh', 'GB 가 처음 경로 (GRAM_START · 이어 돌림 아님)'),
                     ('gram_not_restored', 'GB 새 프로세스 판 z 복원 안 됨 (4300 = 0.03)'), ('gram_state_bad', 'GA 마지막 상태 파일 gr_pz 틀림'),
                     ('gram_wrong_ckpt', 'GB 가 GA 마지막이 아닌 restart (3200) 에서'), ('gram_runs', 'GA run 수 ≠ 5 (Loop time 넷)'),
                     ('gram_gb_rc', 'GB rc 1 · ERROR')):
        chk(f'S34 문법 fixture 반례 — {what} = FAIL (rc 2)', lambda sc=sc: (lambda v: v['status'] == 'FAIL' and v['exit_code'] == 2)(grun(sc)))
    chk('S35 문법 fixture GB 폴더 없음 = FAIL (이어 돌림 경로 미시험 — PASS 아님)', lambda: grun(skip=('GB',))['status'] == 'FAIL')
    chk('S36 문법 fixture 런 폴더에 GA 없음 = NOT_RUN (rc 2)', lambda: (lambda v: v['status'] == 'NOT_RUN' and v['exit_code'] == 2)(grun(skip=('GA', 'GB'))))
    # 러너 모의 (LIGGGHTS 대신 가짜 mpirun · lmp — 덤프 · 화면은 synth_stage) — 러너 흐름 · 단계 순서 · NP · 보고 묶음
    M = {}
    chk('S25 러너 모의: 전 단계 → 읽는 쪽 rc 0 · H0–H5 PASS · 보고 묶음 + sha256', lambda: M.update(_runner_mock()) or
        (M['rc'] == 0 and M['verdict_rows'] == {f'H{i}': 'PASS' for i in range(6)} and M['report'] and M['sha_line']))
    chk('S25 러너 모의: 단계 순서 = P · C6 · C4 · Ebot · Cbot · Etop · Ctop · Enone · Cnone · BAD · SYN · PZ · CZ',
        lambda: M['order'] == ['P', 'C6', 'C4', 'Ebot', 'Cbot', 'Etop', 'Ctop', 'Enone', 'Cnone', 'BAD', 'SYN', 'PZ', 'CZ'])
    chk('S25 러너 모의: 단계 NP = 6 (C4 만 4) · mpirun 인자 --oversubscribe --bind-to none',
        lambda: M['np'] == {s: (4 if s == 'C4' else 6) for s in M['order']} and M['flags_ok'])
    chk('S25 러너 모의: run_manifest 에 이탈 (allow_other_lmp=1) 기록 · kit 사본', lambda: M['manifest_other'] and M['kit_copy'])
    chk('S26 러너 모의: 등록 빌드가 아닌 LMP (ALLOW_OTHER_LMP 없음) = 사전 점검에서 멈춤 · 런 폴더 없음',
        lambda: (lambda r: r['rc'] != 0 and 'LMP sha256' in r['out'] and not r['run_dirs'])(_runner_mock(allow_other=False)))
    chk('S27 러너 모의: 생산자 실패 = 뒤 소비 단계 없음 · 0 fixture 는 돈다 · 읽는 쪽 rc 2',
        lambda: (lambda r: r['rc'] == 2 and r['order'] == ['P', 'PZ', 'CZ'])(_runner_mock(fail_stage='P')))
    chk('S28 러너 모의: NP_ALT = NP 거부 (H2 가 시험되지 않는다)', lambda: (lambda r: r['rc'] != 0 and 'NP_ALT = NP' in r['out'])(_runner_mock(np_alt=6)))
    chk('S29 러너 모의: --preflight-only = 런 · kit 사본 없음', lambda: (lambda r: r['rc'] == 0 and not r['run_dirs'] and not r['kit_copy'])(_runner_mock(preflight=True)))
    GM = {}
    chk('S37 러너 모의 --grammar-only: 단계 = P → GA → GB (H0–H5 단계 없음) · NP 6 · 판정 grammar_verdict PASS · rc 0 · 보고 묶음 gram_*.report.tgz',
        lambda: GM.update(_runner_mock(grammar=True)) or (GM['rc'] == 0 and GM['order'] == ['P', 'GA', 'GB'] and GM['np'] == {'P': 6, 'GA': 6, 'GB': 6}
                                                          and GM['grammar_status'] == 'PASS' and GM['report'] and GM['sha_line']))
    chk('S37 러너 모의 --grammar-only: GA = 생산자 fixture.bin · 빈 상태 파일 · gr_resume 0 / GB = GA 마지막 단 끝 restart + 짝 상태 파일 · gr_resume 1',
        lambda: (lambda a, b: a.get('ckpt', '').endswith('/P/fixture.bin') and a.get('gr_resume') == '0' and a.get('gr_state', '').endswith('/GA/state_fresh.in')
                 and b.get('gr_resume') == '1' and b.get('ckpt', '').endswith(f'/GA/restart/restart_g_{grammar_expect(P)["GA"]["ends"][-1]}.bin')
                 and b.get('gr_state', '').endswith(f'/GA/restart/state_g_{grammar_expect(P)["GA"]["ends"][-1]}.in'))(GM['args'].get('GA', {}), GM['args'].get('GB', {})))
    chk('S37 러너 모의 --grammar-only: GA 실패 = GB 없음 · rc 2', lambda: (lambda r: r['rc'] == 2 and r['order'] == ['P', 'GA'])(_runner_mock(grammar=True, fail_stage='GA')))
    # Q4 (나) — 선행 단계 rc 0 **과** 파일 둘 다 있어야 다음 단계 (파일을 다 쓴 뒤 실패한 단계 = 다음 단계 없음 · Codex 판정문 §6-2)
    chk('S38 러너 모의 --grammar-only: GA 가 restart · 상태 파일을 다 쓴 뒤 rc 1 = GB 없음 (파일이 있어도) · 판정 PASS 아님 · rc 2',
        lambda: (lambda r: r['rc'] == 2 and r['order'] == ['P', 'GA'] and r['grammar_status'] != 'PASS')(_runner_mock(grammar=True, fail_after='GA')))
    chk('S39 러너 모의 --grammar-only: 생산자 P 가 fixture.bin 을 쓴 뒤 rc 1 = GA · GB 없음 · rc 2',
        lambda: (lambda r: r['rc'] == 2 and r['order'] == ['P'])(_runner_mock(grammar=True, fail_after='P')))
    chk('S40 러너 모의 (H0–H5): 생산자 P 가 fixture.bin 을 쓴 뒤 rc 1 = 뒤 소비 단계 없음 (0 fixture PZ → CZ 만) · rc 2',
        lambda: (lambda r: r['rc'] == 2 and r['order'] == ['P', 'PZ', 'CZ'])(_runner_mock(fail_after='P')))
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def _runner_mock(allow_other=True, fail_stage='', np_alt=4, preflight=False, grammar=False, fail_after=''):
    """가짜 mpirun (인자에서 -np 를 MOCK_NP 로) · 가짜 lmp (-var out 폴더 이름 = 단계 → --mock-stage) 로 run_history.sh 를 돌린다.
    grammar = --grammar-only (P → GA → GB · 런 폴더 gram_* · grammar_verdict.json) · fail_stage = 파일 없이 실패 · fail_after = 파일을 다 쓴 뒤 실패."""
    import subprocess
    td = tempfile.mkdtemp(prefix='hist_runner_mock_')
    try:
        work, binr = os.path.join(td, 'work'), os.path.join(td, 'bin')
        os.makedirs(work)
        os.makedirs(binr)
        log = os.path.join(td, 'calls.log')
        with open(os.path.join(binr, 'mpirun'), 'w') as f:
            f.write('#!/bin/bash\nflags=""; np=""\nwhile [ $# -gt 0 ]; do case "$1" in\n'
                    '  --oversubscribe) flags="$flags o"; shift;; --bind-to) flags="$flags b:$2"; shift 2;; -np) np=$2; shift 2;;\n'
                    '  *) break;; esac; done\n'
                    f'echo "np=$np flags=$flags" >> {log}\nMOCK_NP=$np exec "$@"\n')
        with open(os.path.join(binr, 'lmp'), 'w') as f:
            f.write('#!/bin/bash\nout=""; args=""; while [ $# -gt 0 ]; do case "$1" in -var) args="$args $2=$3"; [ "$2" = out ] && out=$3; shift 3;; '
                    '*) shift;; esac; done\n'
                    f'st=$(basename "$out"); echo "stage=$st np=$MOCK_NP$args" >> {log}\n'
                    'echo "LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f)"\n'
                    f'exec python3 {os.path.join(HERE, "read_history.py")} --mock-stage "$st" "$out"\n')
        for b in ('mpirun', 'lmp'):
            os.chmod(os.path.join(binr, b), 0o755)
        env = dict(os.environ, WORK_ROOT=work, MPIRUN=os.path.join(binr, 'mpirun'), LMP=os.path.join(binr, 'lmp'), NP='6', NP_ALT=str(np_alt),
                   HIST_STAMP='20261013_000000', PY=sys.executable, ALLOW_CONCURRENT='1', MOCK_FAIL_STAGE=fail_stage, MOCK_FAIL_AFTER_STAGE=fail_after)
        if allow_other:
            env['ALLOW_OTHER_LMP'] = '1'
        else:
            env.pop('ALLOW_OTHER_LMP', None)
        args = ['bash', os.path.join(HERE, 'run_history.sh')] + (['--preflight-only'] if preflight else []) + (['--grammar-only'] if grammar else [])
        p = subprocess.run(args, env=env, capture_output=True, text=True, timeout=900)
        out = p.stdout + p.stderr
        pre = 'gram' if grammar else 'hist'
        run_dirs = sorted(glob.glob(os.path.join(work, f'{pre}_*/')))
        calls = open(log).read().splitlines() if os.path.exists(log) else []
        order = [c.split()[0].split('=')[1] for c in calls if c.startswith('stage=')]
        npm = {c.split()[0].split('=')[1]: int(c.split()[1].split('=')[1]) for c in calls if c.startswith('stage=')}
        sargs = {c.split()[0].split('=')[1]: dict(x.split('=', 1) for x in c.split()[2:] if '=' in x) for c in calls if c.startswith('stage=')}
        flags_ok = all(c.split(' ', 1)[1].strip() == 'flags= o b:none' for c in calls if c.startswith('np=')) and any(c.startswith('np=') for c in calls)
        vpath = os.path.join(run_dirs[0], 'history_verdict.json') if run_dirs else ''
        vrows = {k: r['status'] for k, r in json.load(open(vpath))['rows'].items()} if vpath and os.path.exists(vpath) else {}
        gpath = os.path.join(run_dirs[0], 'grammar_verdict.json') if run_dirs else ''
        gstat = json.load(open(gpath)).get('status') if gpath and os.path.exists(gpath) else None
        man = open(os.path.join(run_dirs[0], 'run_manifest.txt')).read() if run_dirs else ''
        return {'rc': p.returncode, 'out': out, 'run_dirs': run_dirs, 'order': order, 'np': npm, 'flags_ok': flags_ok, 'args': sargs,
                'verdict_rows': vrows, 'grammar_status': gstat, 'report': bool(glob.glob(os.path.join(work, f'{pre}_*.report.tgz'))),
                'sha_line': '보낼 것:' in out and 'sha256' in out, 'manifest_other': 'allow_other_lmp=1' in man,
                'kit_copy': bool(glob.glob(os.path.join(work, 'kit_*')))}
    finally:
        shutil.rmtree(td, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description='DEM 언로딩 키트 — 작은 침대 이력 시험 (H0–H5) 읽는 쪽')
    ap.add_argument('run_dir', nargs='?')
    ap.add_argument('--params', default=PARAMS)
    ap.add_argument('--out')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--mock-stage', nargs=2, metavar=('STAGE', 'DIR'))
    ap.add_argument('--scenario', default='good')
    ap.add_argument('--grammar', action='store_true', help='문법 fixture 판정 (런 폴더 gram_* — P → GA → GB · 등록 개정 3 §14-9)')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    P = load_params(a.params)
    if a.mock_stage:
        npo = int(os.environ['MOCK_NP']) if os.environ.get('MOCK_NP', '').isdigit() else None
        fail = os.environ.get('MOCK_FAIL_STAGE', '')
        if a.mock_stage[0] == fail:
            print('ERROR: mock failure (모의 — 이 단계는 실패한다)')
            return 1
        rc = synth_stage(a.mock_stage[0], a.mock_stage[1], P, a.scenario, np_override=npo, write_meta=False)
        if a.mock_stage[0] == os.environ.get('MOCK_FAIL_AFTER_STAGE', ''):   # 파일을 다 쓴 뒤 실패 (Q4 나 · 판정문 §6-2)
            print('ERROR: mock failure after writing all files (모의 — 산출물은 남기고 rc 1)')
            return 1
        return rc
    if not a.run_dir:
        ap.error('런 폴더 (또는 --selftest)')
    if a.grammar:
        v = grammar_info(a.run_dir, P)
        if a.out:
            with open(a.out, 'w', encoding='utf-8') as f:
                json.dump(v, f, ensure_ascii=False, indent=2)
        print(grammar_text(v))
        return v['exit_code']
    v = evaluate(a.run_dir, P)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump(v, f, ensure_ascii=False, indent=2)
    print(report_text(v))
    return v['exit_code']


def report_text(v):
    R = v['rows']
    L = ['HISTORY_VERDICT ' + ' '.join(f'H{i}={R[f"H{i}"]["status"]}' for i in range(6))]
    names = {'H0': '문법 · 기술 (rc · 배너 · NP · 덤프 · reset 로그)', 'H1': '같은 NP round-trip', 'H2': 'NP 바꿈 round-trip',
             'H3': '바닥 (primitive) 만 소거', 'H4': '판 (mesh) 만 소거', 'H5': '결손 · 0 뿐 분류'}
    for k in sorted(R):
        r = R[k]
        L.append(f'  {k} {r["status"]:<13} {names[k]}')
        for key in ('problems', 'fails'):
            for p in (r.get(key) or [])[:4]:
                L.append(f'      · {p}')
        if k in ('H1', 'H2') and r.get('classes'):
            L.append('      ' + ' · '.join(f'{c} {d["status"]}' for c, d in r['classes'].items())
                     + f' · sentinel {r.get("sentinels")} · 같은 값 중복 {r.get("dup_consistent")}')
        if k in ('H3', 'H4') and r.get('checks'):
            L.append('      ' + ' · '.join(f'{a}={b}' for a, b in r['checks'].items()))
        if k == 'H5':
            L.append(f'      잘못된 ID → {r["bad_id_class"]} (기대 TECH) · 0 뿐 → {r["zero_class"]} (기대 INCONCLUSIVE)')
    I = v['info']
    L.append(f'  정보: 자동 restart step {I["auto_restart_steps"]} — {I["auto_note"]}')
    L.append(f'  정보: 총힘 출력 시점 (Z 입자 fz = −m g) = {I["force_timing"]}')
    L.append(f'  정보: SYN 문법 미리 지나가기 = {I["syn"]["status"]} {I["syn"].get("checks", {})}')
    L.append(f'  rc = {v["exit_code"]} (0 = H0–H5 전부 기대대로)')
    return '\n'.join(L)


if __name__ == '__main__':
    sys.exit(main())
