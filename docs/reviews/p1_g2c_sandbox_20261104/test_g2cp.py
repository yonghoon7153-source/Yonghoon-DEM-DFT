#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G2c′ 샌드박스 대조기 · 실행기 시험 (2026-11-10 · 시험 먼저 · LIGGGHTS · MPI · 네트워크 없이 · 표준 라이브러리만).

    python3 -I docs/reviews/p1_g2c_sandbox_20261104/test_g2cp.py
    → 시험 (함수) 마다 PASS / FAIL / SKIP 한 줄 · 마지막 줄 `G2CP_TEST pass=… fail=… skip=… total=…` · rc 0 = fail 0

대상 = 같은 폴더의 compare_g2cp.py (대조기) · run_g2cp.sh (실행기) · BW.liggghts (덱 꼴).
등록 = 메모 docs/reviews/p1_g2c_compare_definition_20261105.md §0 (11-10 개정 · 결과 전).

가. 합성 침대 — LIGGGHTS-PUBLIC 3d5c00f 소스 줄을 옮긴 작은 모형 (hooke kt 식 · 고착 / 미끄럼 · 덤프 사영 열 ·
    주기 고스트 속도 · deltaMax 올림 · 이웃 재구성 이력 0) 으로 팔 아홉의 덤프를 만든다.  정상 침대 = 대조기 예측 전부 맞음
    (가 · 라-재현 (나) = 해당 없음 — 가짜 실행 파일) · 한 곳씩 깨면 그 예측만 틀림.  모형은 대조기 코드를 쓰지 않는다 (독립).
나. 실행기 — 가짜 lmp (-h 머리 줄 · 고정 덤프 복사 · 부른 인자 기록) 로 차례 · 인자 · 멈춤 · nice · 기록.
    실행기 시험은 `unshare -pf --mount-proc --kill-child` 안에서 돈다 (못 쓰면 감싸지 않고 돌리되 시간 초과 kill 없음 ·
    시간 한도 시험 = 신호 시험이라 건너뜀 · 건너뜀 수를 마지막 줄에 적는다).  kill 은 직접 만든 자식 (unshare) 에만 · pid > 1 · 자기 · 부모 아님.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True   # 리포 폴더에 __pycache__ 를 만들지 않는다

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
KIT = os.path.join(REPO, 'docs', 'data', 'ps45_unload_20261009')
RUNNER = 'run_g2cp.sh'
CMPFILE = 'compare_g2cp.py'

# ── 덱 물성 (mat.inc · fresh.inc 를 손으로 옮김 — 대조기 해석기와 독립) ──────────────────────────────
E = {1: 1.4e8, 2: 1.4e8, 3: 0.135e7}
NU = {1: 0.25, 2: 0.25, 3: 0.30}
RHO = {1: 4800.0, 2: 4800.0, 3: 2000.0}
RAD = {1: 2.0e-3, 2: 1.0e-3, 3: 0.5e-3}
MU = 0.5
VC = 2.0
DT = 1.0e-6
SKIN = 0.0005
BOXB = ((0.0, 0.012), (0.0, 0.012), (-0.001, 0.04))
LX = BOXB[0][1] - BOXB[0][0]
NSTEP = 40000
ARMS = ('A', 'A2', 'B', 'B2', 'C', 'BW', 'BR', 'CW', 'CR')
DECKS7 = ('head.inc', 'mat.inc', 'fresh.inc', 'outA.inc', 'A.liggghts', 'A2.liggghts', 'R.liggghts')


def load_cmp():
    spec = importlib.util.spec_from_file_location('compare_g2cp', os.path.join(HERE, CMPFILE))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_kit():
    spec = importlib.util.spec_from_file_location('ul_gates_ro', os.path.join(KIT, 'ul_gates.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ── 벡터 ─────────────────────────────────────────────────────────────────────────────────
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vnorm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    m = vnorm(a)
    return [c / m for c in a]


def remap(x):
    """Domain::remap — x · y 주기 (z 고정)."""
    out = list(x)
    for d in (0, 1):
        lo, hi = BOXB[d]
        L = hi - lo
        while out[d] < lo:
            out[d] += L
        while out[d] >= hi:
            out[d] -= L
        out[d] = max(out[d], lo)
    return out


def mass(t, r):
    return RHO[t] * 4.0 / 3.0 * math.pi * r ** 3


def kt_ref(ti, tj, ri, rj):
    """normal_model_hooke_hysteresis.h 139–146 (kt = kn · SI 라 nktv2p = 1) · global_properties.cpp 432 (Y*)."""
    Y = 1. / ((1. - NU[ti] ** 2) / E[ti] + (1. - NU[tj] ** 2) / E[tj])
    reff = ri * rj / (ri + rj)
    mi, mj = mass(ti, ri), mass(tj, rj)
    meff = mi * mj / (mi + mj)
    sq = math.sqrt(reff)
    return 16. / 15. * sq * Y * (15. * meff * VC * VC / (16. * sq * Y)) ** 0.2


# ── 합성 침대 ────────────────────────────────────────────────────────────────────────────
class Bed:
    """쌍마다 원자 둘 (공유 없음).  kind:
    stick · stick_flip (행 id1 > id2) · periodic (주기 표지 1 · 고스트 j · id1 > id2) · edge (B 에서 kt|s| = μ|Fn|(1+1e-10) · 경계) ·
    slip (B 미끄럼 · C 고착) · slip2 (둘 다 미끄럼) · slipC (B 고착 · C 미끄럼) — 반 step 법선 속도를 en 으로 비껴 in-run Fn 을 C 와 다르게 ·
    loading (N 에 겹침이 커짐 → setup 올림) ·
    cohesion (in-run 가드 갱신으로 A(N) deltaMax ≠ max(old, δ)) · new0 (N 에 새 접촉 · 파일 이력 0) · newstale (옛 이력 복원) · gone (N 에 떨어짐)."""
    KINDS = ('stick', 'stick', 'stick', 'stick_flip', 'stick_flip', 'periodic', 'periodic', 'periodic',
             'slip', 'loading', 'loading', 'cohesion', 'new0', 'newstale', 'gone', 'stick', 'edge', 'slip2', 'slipC')
    TYPES = ((1, 1), (1, 2), (2, 3), (3, 3), (1, 3), (2, 2))

    def __init__(self, seed=11, kt_scale_B=1.0, decompose_by_model_B=False, no_raise_B=False):
        R = random.Random(seed)
        self.kt_scale_B = kt_scale_B
        self.decompose_by_model_B = decompose_by_model_B
        self.no_raise_B = no_raise_B
        self.atoms, self.pairs = {}, []
        tag = 0
        for k, kind in enumerate(self.KINDS):
            ti, tj = self.TYPES[k % len(self.TYPES)]
            ri, rj = RAD[ti], RAD[tj]
            a, b = tag + 1, tag + 2
            tag += 2
            i_tag, j_tag = (b, a) if kind in ('periodic', 'stick_flip') else (a, b)
            if kind == 'periodic':
                en = unit([R.uniform(0.80, 0.95), R.uniform(-0.25, 0.25), R.uniform(-0.25, 0.25)])
                xi = [0.0006 + R.uniform(0.0, 0.0002), R.uniform(0.004, 0.008), R.uniform(0.008, 0.03)]
            else:
                en = unit([R.uniform(-1, 1) for _ in range(3)])
                xi = [R.uniform(0.004, 0.008), R.uniform(0.004, 0.008), R.uniform(0.008, 0.03)]
            frac = -0.002 if kind == 'gone' else 0.002
            r0 = (ri + rj) * (1.0 - frac)
            ximg0 = [xi[d] - en[d] * r0 for d in range(3)]
            img = -1 if (kind == 'periodic' and ximg0[0] < 0.0) else 0
            xj = [ximg0[0] - img * LX, ximg0[1], ximg0[2]]
            for t, ty, rr, xx in ((i_tag, ti, ri, xi), (j_tag, tj, rj, xj)):
                v = [R.uniform(-2e-3, 2e-3) for _ in range(3)]
                w = [R.uniform(-2.0, 2.0) for _ in range(3)]
                self.atoms[t] = dict(t=ty, r=rr, x=xx, v=v, w=w,
                                     vh=[c + R.uniform(-5e-6, 5e-6) for c in v], wh=[c + R.uniform(-5e-3, 5e-3) for c in w])
            p = dict(i=i_tag, j=j_tag, kind=kind, img=img, flag=1 if img else 0)
            kt = kt_ref(ti, tj, ri, rj)
            g = self.geom(p, 'full')
            fn0 = kt * g['deltan']
            rnd = [R.uniform(-1, 1) for _ in range(3)]
            gen = g['en']
            tan = [rnd[d] - dot(rnd, gen) * gen[d] for d in range(3)]
            tan = unit(tan)
            mag = {'slip': 3.0, 'slip2': 3.0, 'newstale': 0.1}.get(kind, 0.2) * MU * fn0 / kt
            sgn = 1.0 if R.random() < 0.5 else -1.0
            s_old = [tan[d] * mag + sgn * 3e-4 * mag * gen[d] for d in range(3)]
            dlt = g['deltan']
            dm_old = {'loading': dlt * 0.999, 'cohesion': dlt * 1.5, 'newstale': dlt * 1.3}.get(kind, dlt * 1.01)
            if kind == 'new0':
                s_old, dm_old = [0.0, 0.0, 0.0], 0.0
            if kind == 'gone':
                dm_old = abs(dlt) * 1.01
            if kind == 'edge':      # B 쪽 (full 속도 · 올린 deltaMax) 법선력에 맞춰 kt|s| = μ|Fn|·(1 + 1e-10)
                fnB = self.normal(g, max(dm_old, dlt))
                sc = MU * abs(fnB) * (1.0 + 1e-10) / (kt * vnorm(s_old))
                s_old = [c * sc for c in s_old]
            if kind in ('slip', 'slip2', 'slipC'):
                fnB = self.normal(g, max(dm_old, dlt))
                rel = {'slip': -1e-4, 'slip2': 1e-4, 'slipC': 1e-7}[kind]   # Fn_h = Fn_B·(1 + rel)
                alpha = -rel * fnB / g['gn']
                ai_, aj_ = self.atoms[i_tag], self.atoms[j_tag]
                ai_['vh'] = [ai_['v'][d] + alpha * gen[d] for d in range(3)]
                ai_['wh'] = list(ai_['w'])
                aj_['vh'], aj_['wh'] = list(aj_['v']), list(aj_['w'])
                if kind == 'slipC':  # B 고착 (1e-6 안) · in-run 에서 미끄럼 → 원 위 (Fn_h) = C 에서 미끄럼 (1e-7 밖)
                    vt_ = unit(g['vtr'])
                    s_old = [vt_[d] * MU * abs(fnB) * (1.0 - 1e-6) / kt for d in range(3)]
            p.update(s_old=s_old, dm_old=dm_old)
            self.pairs.append(p)
        for p in self.pairs:
            self._inrun(p)

    # surface_model_default.h 150–194 · pair_gran_base.h 279–320 (geometry) · ghost_v = full | half_all | half_ghost
    def geom(self, p, ghost_v):
        ai, aj = self.atoms[p['i']], self.atoms[p['j']]
        xi = list(ai['x'])
        xj = [aj['x'][0] + p['img'] * LX, aj['x'][1], aj['x'][2]]
        delx, dely, delz = xi[0] - xj[0], xi[1] - xj[1], xi[2] - xj[2]
        rsq = delx * delx + dely * dely + delz * delz
        r = math.sqrt(rsq)
        rinv = 1.0 / r
        en = [delx * rinv, dely * rinv, delz * rinv]
        ri, rj = ai['r'], aj['r']
        deltan = (ri + rj) - r
        half_i = ghost_v == 'half_all'
        half_j = ghost_v == 'half_all' or (ghost_v == 'half_ghost' and p['img'] != 0)
        vi, wi = (ai['vh'], ai['wh']) if half_i else (ai['v'], ai['w'])
        vj, wj = (aj['vh'], aj['wh']) if half_j else (aj['v'], aj['w'])
        vr = [vi[k] - vj[k] for k in range(3)]
        vn = vr[0] * en[0] + vr[1] * en[1] + vr[2] * en[2]
        vt = [vr[k] - vn * en[k] for k in range(3)]
        cri, crj = ri - 0.5 * deltan, rj - 0.5 * deltan
        wr = [(cri * wi[k] + crj * wj[k]) * rinv for k in range(3)]
        vtr = [vt[0] - (delz * wr[1] - dely * wr[2]), vt[1] - (delx * wr[2] - delz * wr[0]), vt[2] - (dely * wr[0] - delx * wr[1])]
        ti, tj = ai['t'], aj['t']
        kt = kt_ref(ti, tj, ri, rj)
        meff = mass(ti, ri) * mass(tj, rj) / (mass(ti, ri) + mass(tj, rj))
        return dict(xi=xi, xj=xj, en=en, r=r, rsq=rsq, deltan=deltan, vn=vn, vtr=vtr, cri=cri, crj=crj, kt=kt, kn=kt,
                    gn=0.5 * math.sqrt(meff * kt), ri=ri, rj=rj)

    @staticmethod
    def normal(g, dm):
        # 합성 법선 모형 (deltaMax 가 힘에 들어가게) — 대조기는 이 식을 쓰지 않는다 (Fn = C 힘의 en 사영)
        return g['kn'] * g['deltan'] + 0.3 * g['kn'] * (dm - g['deltan']) - g['gn'] * g['vn']

    @staticmethod
    def tangential(g, s, Fn, kt):
        """tangential_model_history.h 161–217 (갱신 없는 쪽) → (Ft, slip)."""
        shrmag = math.sqrt(s[0] * s[0] + s[1] * s[1] + s[2] * s[2])
        Ft = [-(kt * s[0]), -(kt * s[1]), -(kt * s[2])]
        Ft_shear = kt * shrmag
        Ft_friction = MU * abs(Fn)
        if Ft_shear > Ft_friction:
            if shrmag != 0.0:
                ratio = Ft_friction / Ft_shear
                Ft = [c * ratio for c in Ft]
            else:
                Ft = [0.0, 0.0, 0.0]
            return Ft, True
        gt = g['gn']
        return [Ft[k] - gt * g['vtr'][k] for k in range(3)], False

    def force(self, g, dm, s, kt=None):
        kt = g['kt'] if kt is None else kt
        Fn = self.normal(g, dm)
        Ft, slip = self.tangential(g, s, Fn, kt)
        en = g['en']
        F = [Fn * en[k] + Ft[k] for k in range(3)]
        tor = [en[1] * Ft[2] - en[2] * Ft[1], en[2] * Ft[0] - en[0] * Ft[2], en[0] * Ft[1] - en[1] * Ft[0]]
        tq = [-g['cri'] * c for c in tor]
        return F, tq, Fn, Ft, slip

    def _inrun(self, p):
        """A 의 step N 힘 계산 (갱신 있음 · 반 step 속도) → H(N)."""
        if p['kind'] == 'gone':
            p['dmN'], p['sN'] = None, None
            return
        g = self.geom(p, 'half_all')
        dmN = max(p['dm_old'], g['deltan'])
        if p['kind'] == 'cohesion':
            dmN = g['deltan'] * 1.2
        s = [p['s_old'][k] + g['vtr'][k] * DT for k in range(3)]
        rsht = s[0] * g['en'][0] + s[1] * g['en'][1] + s[2] * g['en'][2]
        s = [s[k] - rsht * g['en'][k] for k in range(3)]
        Fn = self.normal(g, dmN)
        Ft, slip = self.tangential(g, s, Fn, g['kt'])
        if slip:
            s = [-Ft[k] / g['kt'] for k in range(3)]
        p['dmN'], p['sN'] = dmN, s

    def row(self, p, g, F, tq, dm, s, model_split=None):
        xi, xj = g['xi'], g['xj']
        pos1, pos2 = remap(xi), remap(xj)
        if model_split is None:
            nrm = [xj[k] - xi[k] for k in range(3)]
            inv = 1.0 / math.sqrt(nrm[0] * nrm[0] + nrm[1] * nrm[1] + nrm[2] * nrm[2])
            nrm = [c * inv for c in nrm]
            fnmag = F[0] * nrm[0] + F[1] * nrm[1] + F[2] * nrm[2]
            fn = [nrm[k] * fnmag for k in range(3)]
            ft = [F[k] - fn[k] for k in range(3)]
        else:
            fn, ft = model_split
        de = [xi[k] - xj[k] for k in range(3)]
        rsq = de[0] * de[0] + de[1] * de[1] + de[2] * de[2]
        r = math.sqrt(rsq)
        ri, rj = g['ri'], g['rj']
        area = -math.pi / 4 * ((r - ri - rj) * (r + ri - rj) * (r - ri + rj) * (r + ri + rj)) / rsq
        delta = ri + rj - math.sqrt(de[0] * de[0] + de[1] * de[1] + de[2] * de[2])
        cp = [(xi[k] * rj + xj[k] * ri) / (ri + rj) for k in range(3)]
        return pos1 + pos2 + [float(p['i']), float(p['j']), float(p['flag'])] + F + fn + ft + tq + [dm] + list(s) + [area, delta] + cp

    def rows(self, arm):
        out = []
        for p in self.pairs:
            k = p['kind']
            if arm == 'cpre':
                if k in ('new0', 'newstale'):
                    continue
                g = self.geom(p, 'half_ghost')
                F, tq, *_ = self.force(g, p['dm_old'], p['s_old'])
                out.append(self.row(p, g, F, tq, p['dm_old'], p['s_old']))
                continue
            if k == 'gone':
                continue
            if arm in ('A', 'A2'):
                g = self.geom(p, 'half_ghost')
                F, tq, *_ = self.force(g, p['dmN'], p['sN'])
                out.append(self.row(p, g, F, tq, p['dmN'], p['sN']))
            elif arm in ('C', 'CW', 'CR'):
                g = self.geom(p, 'full')
                F, tq, *_ = self.force(g, p['dmN'], p['sN'])
                out.append(self.row(p, g, F, tq, p['dmN'], p['sN']))
            else:   # B B2 BW BR — 주기 파일 = H(N−1) · setup 이 deltaMax 만 올림
                g = self.geom(p, 'full')
                dmB = p['dm_old'] if self.no_raise_B else max(p['dm_old'], g['deltan'])
                kt = g['kt'] * self.kt_scale_B
                F, tq, Fn, Ft, _ = self.force(g, dmB, p['s_old'], kt=kt)
                split = ([Fn * g['en'][k] for k in range(3)], list(Ft)) if self.decompose_by_model_B else None
                out.append(self.row(p, g, F, tq, dmB, p['s_old'], model_split=split))
        return out

    def atom_rows(self):
        return [[float(t), float(a['t'])] + a['x'] + a['v'] + a['w'] + [a['r']] for t, a in sorted(self.atoms.items())]


# ── 덤프 쓰기 (LIGGGHTS 꼴 · %.17g) ─────────────────────────────────────────────────────────
def fmt_local(step, rows, ncol=30, box=BOXB, tokfmt='%.17g'):
    L = ['ITEM: TIMESTEP', str(step), 'ITEM: NUMBER OF ENTRIES', str(len(rows)), 'ITEM: BOX BOUNDS pp pp ff']
    L += ['%-1.16e %-1.16e' % b for b in box]
    L += ['ITEM: ENTRIES ' + ' '.join('c_cpl[%d]' % i for i in range(1, ncol + 1))]
    L += [' '.join(tokfmt % v for v in r[:ncol]) for r in rows]
    return '\n'.join(L) + '\n'


def fmt_atoms(step, rows, box=BOXB, tokfmt='%.17g'):
    L = ['ITEM: TIMESTEP', str(step), 'ITEM: NUMBER OF ATOMS', str(len(rows)), 'ITEM: BOX BOUNDS pp pp ff']
    L += ['%-1.16e %-1.16e' % b for b in box]
    L += ['ITEM: ATOMS id type x y z vx vy vz omegax omegay omegaz radius']
    L += ['%d %d ' % (int(r[0]), int(r[1])) + ' '.join(tokfmt % v for v in r[2:]) for r in rows]
    return '\n'.join(L) + '\n'


def wtxt(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(text)


def md5f(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def flip_row(r):
    """행 방향 바꾸기 (같은 쌍을 j 쪽에서 본 줄) — pos 맞바꿈 · id 맞바꿈 · 힘 9 열 · shear 3 열 부호 · torque 는 다른 값 (j 쪽) 이라 바꿔 둠."""
    v = list(r)
    v[0:3], v[3:6] = r[3:6], r[0:3]
    v[6], v[7] = r[7], r[6]
    for c in list(range(9, 18)) + [22, 23, 24]:
        v[c] = -r[c]
    v[18:21] = [x * 0.5 for x in r[18:21]]
    return v


def write_fixture(root, N=NSTEP, bed=None, lmp_md5='0' * 32, mutate=None):
    """팔 아홉 출력 + lmp_identity.txt · inputs.md5 · outputs.md5 (실행기가 쓰는 꼴).  mutate(arm, kind, rows) → rows (덤프 바꾸기)."""
    bed = bed or Bed()
    arows = bed.atom_rows()
    for arm in ARMS:
        rows = bed.rows(arm)
        if mutate:
            rows = mutate(arm, 'c', rows)
        wtxt(os.path.join(root, arm, 'post', 'c_%d.txt' % N), fmt_local(N, rows))
        at = mutate(arm, 'atom', arows) if mutate else arows
        wtxt(os.path.join(root, arm, 'post', 'atom_%d.txt' % N), fmt_atoms(N, at))
        if arm in ('A', 'A2'):
            wtxt(os.path.join(root, arm, 'post', 'cpre_%d.txt' % (N - 1)), fmt_local(N - 1, bed.rows('cpre')))
            wtxt(os.path.join(root, arm, 'rst', 'restart_%d.bin' % N), 'FAKE_RESTART kind=periodic step=%d\n' % N)
        if arm == 'A2':
            wtxt(os.path.join(root, arm, 'rst', 'restart_cmd.bin'), 'FAKE_RESTART kind=cmd step=%d\n' % N)
        if arm in ('BW', 'CW'):
            wtxt(os.path.join(root, arm, 'rst', 'restart_rt.bin'), 'FAKE_RESTART kind=rt src=%s step=%d\n' % (arm, N))
    with open(os.path.join(root, 'lmp_identity.txt'), 'w') as f:
        f.write('lmp_path /fake/lmp\nlmp_md5 %s\nlmp_sha256 %s\nlmp_banner LIGGGHTS (가짜)\nN %d\n' % (lmp_md5, '0' * 64, N))
    with open(os.path.join(root, 'inputs.md5'), 'w') as f:
        f.write('%s  lmp\n' % lmp_md5)
        for d in DECKS7 + ('BW.liggghts',):
            p = os.path.join(HERE, d)
            if os.path.exists(p):
                f.write('%s  %s\n' % (md5f(p), d))
    lines = []
    for arm in ARMS:
        for sub in ('post', 'rst'):
            d = os.path.join(root, arm, sub)
            if os.path.isdir(d):
                for fn in sorted(os.listdir(d)):
                    lines.append('%s  %s/%s/%s' % (md5f(os.path.join(d, fn)), arm, sub, fn))
    with open(os.path.join(root, 'outputs.md5'), 'w') as f:
        f.write('\n'.join(lines) + '\n')
    return bed


# ── 시험 틀 ──────────────────────────────────────────────────────────────────────────────
TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


class Skip(Exception):
    pass


class T:
    def __init__(self):
        self.bad = []

    def ok(self, name, cond, detail=''):
        if not cond:
            self.bad.append('%s %s' % (name, detail))


_TMP = []


def tmpdir():
    d = tempfile.mkdtemp(prefix='g2cp_t_')
    _TMP.append(d)
    return d


def argmax_abs(rows, col):
    return max(range(len(rows)), key=lambda i: abs(rows[i][col]))


def status_of(res, key):
    return (res.get('predictions', {}).get(key) or {}).get('status')


# ═══ 대조기 ═════════════════════════════════════════════════════════════════════════════
@test
def t01_material_from_decks():
    c = load_cmp()
    m = c.material(HERE)
    t = T()
    for ty in (1, 2, 3):
        t.ok('E', m['E'][ty] == E[ty], (ty, m['E'].get(ty)))
        t.ok('nu', m['nu'][ty] == NU[ty])
        t.ok('rho', m['rho'][ty] == RHO[ty])
        t.ok('rad', m['rad'][ty] == RAD[ty])
        for tj in (1, 2, 3):
            t.ok('mu', m['mu'][(ty, tj)] == MU)
    t.ok('vc', m['vc'] == VC)
    t.ok('dt', m['dt'] == DT)
    t.ok('skin', m['skin'] == SKIN)
    t.ok('box', tuple(m['box_xy']) == (LX, LX), m.get('box_xy'))
    t.ok('wall', m['wall_z'] == 0.0)
    return t


@test
def t02_kt_formula():
    c = load_cmp()
    m = c.material(HERE)
    t = T()
    for ti, tj in ((1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)):
        ri, rj = RAD[ti], RAD[tj]
        a = c.kt(m, ti, tj, ri, rj)
        b = kt_ref(ti, tj, ri, rj)
        t.ok('kt %d%d' % (ti, tj), abs(a - b) <= 1e-13 * b, (a, b))
    k11 = kt_ref(1, 1, RAD[1], RAD[1])
    t.ok('kt11 자릿수 (손셈 ≈ 2.6e4 N/m)', 2.0e4 < k11 < 3.5e4, k11)
    return t


@test
def t03_read_local_normalizes():
    c = load_cmp()
    d = tmpdir()
    bed = Bed()
    rows = bed.rows('B')
    p = os.path.join(d, 'c.txt')
    wtxt(p, fmt_local(NSTEP, rows))
    D = c.read_local(p)
    t = T()
    t.ok('ok', D['ok'], D['problems'][:3])
    t.ok('step', D['step'] == NSTEP)
    t.ok('n', len(D['by_key']) == len(rows))
    fl = [r for r in rows if r[6] > r[7]]
    t.ok('flip rows 있음', len(fl) >= 5, len(fl))
    r0 = fl[0]
    key = (int(r0[7]), int(r0[6]))
    e = D['by_key'][key]
    t.ok('flipped', e['flipped'])
    t.ok('pos 맞바꿈', e['v'][0:3] == r0[3:6] and e['v'][3:6] == r0[0:3])
    t.ok('force 부호', e['v'][9:18] == [-x for x in r0[9:18]])
    t.ok('shear 부호', e['v'][22:25] == [-x for x in r0[22:25]])
    t.ok('deltaMax 그대로', e['v'][21] == r0[21])
    t.ok('box', D['box_xy'] == (LX, LX))
    return t


@test
def t04_read_local_problems():
    c = load_cmp()
    d = tmpdir()
    rows = Bed().rows('B')
    t = T()
    base = fmt_local(NSTEP, rows)
    L = base.splitlines()
    k = next(i for i, x in enumerate(L) if x.startswith('ITEM: ENTRIES'))
    cases = {
        'id 2.5': '\n'.join(L[:k + 1] + [' '.join(['2.5' if j == 6 else tok for j, tok in enumerate(L[k + 1].split())])] + L[k + 2:]) + '\n',
        'NaN': '\n'.join(L[:k + 1] + [' '.join(['nan' if j == 12 else tok for j, tok in enumerate(L[k + 1].split())])] + L[k + 2:]) + '\n',
        'id 2^53+1': '\n'.join(L[:k + 1] + [' '.join(['9007199254740993' if j == 7 else tok for j, tok in enumerate(L[k + 1].split())])] + L[k + 2:]) + '\n',
        '행 수': base.replace('ITEM: NUMBER OF ENTRIES\n%d' % len(rows), 'ITEM: NUMBER OF ENTRIES\n%d' % (len(rows) + 1)),
        '두 프레임': base + base,
        '열 수': '\n'.join(L[:k + 1] + [' '.join(L[k + 1].split()[:29])] + L[k + 2:]) + '\n',
        'BOX': base.replace('%-1.16e %-1.16e' % BOXB[0], '%-1.16e' % BOXB[0][0]),
    }
    for name, text in cases.items():
        p = os.path.join(d, name.replace(' ', '_').replace('^', '') + '.txt')
        wtxt(p, text)
        D = c.read_local(p)
        t.ok(name + ' → 문제', not D['ok'], D['problems'][:2])
    p26 = os.path.join(d, 'c26.txt')
    wtxt(p26, fmt_local(NSTEP, [r[:21] + r[25:] for r in rows], ncol=26))
    D26 = c.read_local(p26)
    t.ok('26 열 → 필수 열 결손', not D26['ok'] and D26.get('missing_required'), D26['problems'][:2])
    t.ok('없는 파일 → 문제', not c.read_local(os.path.join(d, 'none.txt'))['ok'])
    return t


def _pair(c, d, rows1, rows2, step1=NSTEP, step2=NSTEP, tok2='%.17g'):
    p1, p2 = os.path.join(d, 'd1.txt'), os.path.join(d, 'd2.txt')
    wtxt(p1, fmt_local(step1, rows1))
    wtxt(p2, fmt_local(step2, rows2, tokfmt=tok2))
    return p1, p2


@test
def t05_value_vs_bytes():
    c = load_cmp()
    d = tmpdir()
    rows = Bed().rows('BW')
    t = T()

    def go(r2, name, val, byt, tok2='%.17g', **kw):
        p1, p2 = _pair(c, d, rows, r2, tok2=tok2, **kw)
        v = c.pairs_value(c.read_local(p1), c.read_local(p2))
        b = c.file_bytes_equal(p1, p2)
        t.ok(name + ' 값', v['equal'] == val, v.get('why'))
        t.ok(name + ' 바이트', b == byt)
        return v

    go(rows, '같음', True, True)
    go(list(reversed(rows)), '순서', True, False)
    fr = [flip_row(r) if i == 1 else r for i, r in enumerate(rows)]
    v = go(fr, '방향', True, False)
    t.ok('방향 수', v.get('orientation_differs') == 1, v.get('orientation_differs'))
    u = [list(r) for r in rows]
    u[2][22] = math.nextafter(u[2][22], math.inf)
    v = go(u, '1 ulp shear', False, False)
    t.ok('1 ulp 다른 쌍 1', v.get('n_pairs_differ') == 1, v.get('n_pairs_differ'))
    z = [list(r) for r in rows]
    z[0][9] = 0.0
    z2 = [list(r) for r in z]
    p1, p2 = os.path.join(d, 'z1.txt'), os.path.join(d, 'z2.txt')
    wtxt(p1, fmt_local(NSTEP, z))
    wtxt(p2, fmt_local(NSTEP, z2).replace(' 0 ', ' -0 ', 1))
    vz = c.pairs_value(c.read_local(p1), c.read_local(p2))
    t.ok('-0 = 0 값 같음', vz['equal'], vz.get('why'))
    t.ok('-0 바이트 다름', not c.file_bytes_equal(p1, p2))
    go(rows, '다른 TIMESTEP', False, False, step2=NSTEP + 1)
    p1, p2 = os.path.join(d, 'b1.txt'), os.path.join(d, 'b2.txt')
    wtxt(p1, fmt_local(NSTEP, rows))
    wtxt(p2, fmt_local(NSTEP, rows, box=(BOXB[0], BOXB[1], (-0.001, 0.05))))
    t.ok('상자 다름 → 값 다름', not c.pairs_value(c.read_local(p1), c.read_local(p2))['equal'])
    go(rows[:-1], '한 쌍 빠짐', False, False)
    go(rows + [rows[0]], '중복 키 (같은 값)', False, False)
    return t


@test
def t06_judgment_rules():
    """메모 §5-1 목록: shear 0 · 힘 상대 2e-5 · 쌍 하나 빠짐 · 다른 TIMESTEP = FAIL / 같은 덤프 · 방향 바뀐 행 = PASS (+ 중복 · 26 열)."""
    c = load_cmp()
    d = tmpdir()
    rows = Bed().rows('BW')
    t = T()

    def J(r2, step2=NSTEP, ncol2=30):
        p1, p2 = os.path.join(d, 'j1.txt'), os.path.join(d, 'j2.txt')
        wtxt(p1, fmt_local(NSTEP, rows))
        wtxt(p2, fmt_local(step2, r2, ncol=ncol2))
        return c.judge(c.read_local(p1), c.read_local(p2), expected_step=NSTEP)

    t.ok('같음 PASS', J(rows)['status'] == 'PASS')
    t.ok('방향 PASS', J([flip_row(r) if i % 3 == 0 else r for i, r in enumerate(rows)])['status'] == 'PASS')
    sz = [list(r) for r in rows]
    for r in sz:
        r[22:25] = [0.0, 0.0, 0.0]
    t.ok('shear 0 FAIL', J(sz)['status'] == 'FAIL')
    ia = argmax_abs(rows, 9)
    f2 = [list(r) for r in rows]
    f2[ia][9] *= (1 + 2e-5)
    j = J(f2)
    t.ok('힘 2e-5 FAIL', j['status'] == 'FAIL' and j['n_mismatch'] == 1, j)
    f1 = [list(r) for r in rows]
    f1[ia][9] *= (1 + 0.5e-5)
    t.ok('힘 0.5e-5 PASS', J(f1)['status'] == 'PASS')
    t.ok('쌍 빠짐 FAIL', J(rows[1:])['status'] == 'FAIL')
    t.ok('TIMESTEP FAIL', J(rows, step2=NSTEP + 100)['status'] == 'FAIL')
    t.ok('중복 같은 값 PASS', J(rows + [rows[0]])['status'] == 'PASS')
    dc = [list(rows[0])]
    dc[0][9] *= 1.01
    t.ok('중복 다른 값 FAIL', J(rows + dc)['status'] == 'FAIL')
    tq = [list(r) for r in rows]
    tq[0][18] *= 2.0
    tq[0][8] = 1.0 - tq[0][8]
    t.ok('torque · 주기 표지만 = 판정 밖 PASS', J(tq)['status'] == 'PASS')
    t.ok('26 열 NOT_COMPUTED', J([r[:21] + r[25:] for r in rows], ncol2=26)['status'] == 'NOT_COMPUTED')
    wr = [list(r) for r in rows]
    wr[0][3] += LX                       # 같은 자리 · 주기 상 (감지 않은 꼴)
    wr[0][27] -= LX
    t.ok('주기 위치 · 접점 감음 PASS', J(wr)['status'] == 'PASS')
    p1, p2 = os.path.join(d, 'w1.txt'), os.path.join(d, 'w2.txt')
    wtxt(p1, fmt_local(NSTEP, rows))
    wtxt(p2, fmt_local(NSTEP, wr))
    t.ok('감음 = 값은 다름', not c.pairs_value(c.read_local(p1), c.read_local(p2))['equal'])
    wd = [list(r) for r in rows]
    wd[0][3] += LX + 1e-6                # 주기 상 + 허용폭 밖 실제 차이 → 감은 뒤에도 FAIL
    t.ok('감음 + 실제 차이 FAIL', J(wd)['status'] == 'FAIL')
    fr = [list(r) for r in rows]
    fr[0][9] = sorted(abs(r[9]) for r in rows)[len(rows) // 2] * 1e-6   # 작은 값 — 열 중앙값 floor 가 허용폭을 정한다
    med = statistics.median(abs(r[9]) for r in fr)                     # 기준 (D1) 열의 중앙값 (판정식과 같은 셈)
    ft = [list(r) for r in fr]
    ft[0][9] += 0.5e-5 * med
    p1, p2 = os.path.join(d, 'f1.txt'), os.path.join(d, 'f2.txt')
    wtxt(p1, fmt_local(NSTEP, fr))
    wtxt(p2, fmt_local(NSTEP, ft))
    t.ok('중앙값 floor 안 PASS', c.judge(c.read_local(p1), c.read_local(p2), expected_step=NSTEP)['status'] == 'PASS')
    ft[0][9] = fr[0][9] + 3e-5 * med
    wtxt(p2, fmt_local(NSTEP, ft))
    t.ok('중앙값 floor 밖 FAIL', c.judge(c.read_local(p1), c.read_local(p2), expected_step=NSTEP)['status'] == 'FAIL')
    hd = [list(r) for r in rows]
    hd[argmax_abs(rows, 21)][21] *= (1 + 2e-5)
    t.ok('deltaMax 2e-5 FAIL (이력 열도 같은 식)', J(hd)['status'] == 'FAIL')
    return t


@test
def t07_judgment_matches_kit():
    """26 열 사영에서 대조기 판정 (kit26) = 키트 ul_gates.g2c_compare (상태 · n_mismatch) — 등록 §3 '같은 식'."""
    c = load_cmp()
    kit = load_kit()
    d = tmpdir()
    rows = Bed().rows('BW')
    t = T()
    f = [list(r) for r in rows]
    f[argmax_abs(rows, 9)][9] *= (1 + 2e-5)
    g = [list(r) for r in rows]
    g[4][24] = 0.0          # 이력 열만 — 26 열에는 안 보임
    dc = [list(rows[0])]
    dc[0][9] *= 1.01
    wr = [list(r) for r in rows]
    wr[1][3] += LX
    wr[1][27] -= LX
    med = sorted(abs(r[9]) for r in rows)[len(rows) // 2]
    fl = [list(r) for r in rows]
    fl[0][9] = rows[0][9] + 0.5e-5 * med if abs(rows[0][9]) < 0.5 * med else rows[0][9] * (1 + 0.5e-5)
    cases = {'같음': rows, '방향': [flip_row(r) if i % 2 else r for i, r in enumerate(rows)], '2e-5': f,
             '이력만': g, '빠짐': rows[2:], '중복': rows + [rows[1]], '충돌': rows + dc, '감음': wr, 'floor': fl}
    for name, r2 in cases.items():
        p1, p2 = os.path.join(d, 'k1.txt'), os.path.join(d, 'k2.txt')
        wtxt(p1, fmt_local(NSTEP, [r[:21] + r[25:] for r in rows], ncol=26))
        wtxt(p2, fmt_local(NSTEP, [r[:21] + r[25:] for r in r2], ncol=26))
        a = kit.g2c_compare(p2, p1, box=(LX, LX), expected_step=NSTEP)
        b = c.judge(c.read_local(p1, ncol=26), c.read_local(p2, ncol=26), expected_step=NSTEP, mode='kit26')
        t.ok(name + ' 상태', a['status'] == b['status'], (a['status'], b['status']))
        t.ok(name + ' n_mismatch', a.get('n_mismatch') == b.get('n_mismatch'), (a.get('n_mismatch'), b.get('n_mismatch')))
    return t


@test
def t08_atoms_compare():
    c = load_cmp()
    d = tmpdir()
    ar = Bed().atom_rows()
    t = T()

    def go(a2, name, val, byt):
        p1, p2 = os.path.join(d, 'a1.txt'), os.path.join(d, 'a2.txt')
        wtxt(p1, fmt_atoms(NSTEP, ar))
        wtxt(p2, fmt_atoms(NSTEP, a2))
        v = c.atoms_value(c.read_atoms(p1), c.read_atoms(p2))
        t.ok(name + ' 값', v['equal'] == val, v.get('why'))
        t.ok(name + ' 바이트', c.file_bytes_equal(p1, p2) == byt)

    go(ar, '같음', True, True)
    go(list(reversed(ar)), '순서', True, False)
    u = [list(r) for r in ar]
    u[3][10] = math.nextafter(u[3][10], -math.inf)
    go(u, 'omega 1 ulp', False, False)
    go(ar[1:], '원자 빠짐', False, False)
    ty = [list(r) for r in ar]
    ty[0][1] = 3.0 if ty[0][1] != 3.0 else 1.0
    go(ty, '형 다름', False, False)
    p = os.path.join(d, 'bad.txt')
    wtxt(p, fmt_atoms(NSTEP, ar).replace('omegaz radius', 'omegaz'))
    t.ok('열 결손 → 문제', not c.read_atoms(p)['ok'])
    L = fmt_atoms(NSTEP, ar).splitlines()
    tk = L[-1].split()
    tk[5] = 'nan'
    L[-1] = ' '.join(tk)
    wtxt(p, '\n'.join(L) + '\n')
    t.ok('원자 NaN → 문제', not c.read_atoms(p)['ok'])
    return t


def _bc(bedB=None, bedC=None):
    bedB = bedB or Bed()
    bedC = bedC or Bed()
    return bedB, bedC


def _files(d, bedB, bedC):
    pB, pC, pa = os.path.join(d, 'B.txt'), os.path.join(d, 'C.txt'), os.path.join(d, 'atom.txt')
    wtxt(pB, fmt_local(NSTEP, bedB.rows('B')))
    wtxt(pC, fmt_local(NSTEP, bedC.rows('C')))
    wtxt(pa, fmt_atoms(NSTEP, bedC.atom_rows()))
    return pB, pC, pa


@test
def t09_ba_projection_positive():
    c = load_cmp()
    d = tmpdir()
    bedB, bedC = _bc()
    pB, pC, pa = _files(d, bedB, bedC)
    r = c.pred_ba(c.read_local(pB), c.read_local(pC), c.read_atoms(pa), c.material(HERE))
    t = T()
    t.ok('맞음', r['status'] == '맞음', r)
    t.ok('양쪽 고착 ≥ 8', r['n_stick_both'] >= 8, r['n_stick_both'])
    t.ok('미끄럼 ≥ 1', r['n_slip_any'] >= 1, r['n_slip_any'])
    t.ok('deltaMax 다른 쌍 제외 1', r['n_dm_differ'] == 1, r['n_dm_differ'])
    t.ok('판별력 ≥ 1', r['n_discriminating'] >= 1, r['n_discriminating'])
    t.ok('경계 쌍 1 (edge)', r['n_boundary'] == 1, r['n_boundary'])
    t.ok('미끄럼 셋 (B · 둘 다 · C)', r['n_slip_any'] == 3, r['n_slip_any'])
    t.ok('둘 다 미끄럼 1 · 원 위', r['n_slip_both'] == 1 and r['n_slip_both_on_circle'] == 1, (r['n_slip_both'], r['n_slip_both_on_circle']))
    t.ok('주기 쌍 포함', r['by_flag']['1']['n_stick_both'] >= 1 and r['by_flag']['1']['n_fail'] == 0, r['by_flag'])
    return t


@test
def t10_ba_old_chain_negative():
    """B 의 force_normal · force_tangential 을 사영이 아니라 모형 성분 (Fn·en · Ft) 으로 적으면 → 바-2 · 3 틀림 · 바-1 맞음."""
    c = load_cmp()
    d = tmpdir()
    bedB, bedC = Bed(decompose_by_model_B=True), Bed()
    pB, pC, pa = _files(d, bedB, bedC)
    r = c.pred_ba(c.read_local(pB), c.read_local(pC), c.read_atoms(pa), c.material(HERE))
    t = T()
    t.ok('틀림', r['status'] == '틀림', r['status'])
    t.ok('바-1 실패 0', r['fail_by_eq']['바-1'] == 0, r['fail_by_eq'])
    t.ok('바-2 · 3 실패 > 0', r['fail_by_eq']['바-2'] > 0 and r['fail_by_eq']['바-3'] > 0, r['fail_by_eq'])
    return t


@test
def t11_ba_kt_negative():
    c = load_cmp()
    d = tmpdir()
    bedB, bedC = Bed(kt_scale_B=1.001), Bed()
    pB, pC, pa = _files(d, bedB, bedC)
    r = c.pred_ba(c.read_local(pB), c.read_local(pC), c.read_atoms(pa), c.material(HERE))
    t = T()
    t.ok('틀림', r['status'] == '틀림', r['status'])
    t.ok('바-1 실패 > 0', r['fail_by_eq']['바-1'] > 0, r['fail_by_eq'])
    return t


def _full(d, bed=None, mutate=None, N=NSTEP, lmp_md5='0' * 32):
    O = os.path.join(d, 'out')
    write_fixture(O, N=N, bed=bed, mutate=mutate, lmp_md5=lmp_md5)
    return O


@test
def t12_end_to_end_positive():
    c = load_cmp()
    d = tmpdir()
    O = _full(d)
    res, rc = c.compare_all(O, NSTEP, here=HERE, ref=os.path.join(HERE, 'run_40000'))
    t = T()
    want = {'가': '해당 없음', '나': '맞음', '다-값': '맞음', '다-바이트': '맞음', '라-값': '맞음', '라-바이트': '맞음',
            '라-재현가': '맞음', '라-재현나': '해당 없음', '마-1': '맞음', '마-2': '맞음', '마-3': '맞음', '바': '맞음',
            '사': '맞음', '예외①': '맞음', '예외②': '맞음'}
    for k, v in want.items():
        t.ok(k, status_of(res, k) == v, (k, status_of(res, k), (res.get('predictions', {}).get(k) or {}).get('why')))
    t.ok('판정 다 PASS', res['judgment']['다']['status'] == 'PASS', res['judgment']['다'])
    t.ok('판정 라 PASS', res['judgment']['라']['status'] == 'PASS')
    t.ok('rc 0', rc == 0, rc)
    e1 = res['exceptions']['①']
    t.ok('올림 쌍 = loading 2', e1['n_raise_periodic_side'] == 2, e1)
    t.ok('cohesion 가드 1', e1['n_cohesion_guarded_A'] == 1, e1)
    e2 = res['exceptions']['②']
    t.ok('새 쌍 0 / 복원', e2['n_new_zero'] == 1 and e2['n_new_restored'] == 1 and e2['n_gone'] == 1, e2)
    t.ok('벽 규모 적음', 'n_wall_touch' in res['exceptions']['③'])
    t.ok('JSON 파일', os.path.exists(os.path.join(O, 'compare_g2cp.json')))
    t.ok('연속 보고', res['reports']['연속']['B']['n_pairs_force_differ'] >= 1, res['reports'].get('연속'))
    return t


@test
def t13_end_to_end_negatives():
    c = load_cmp()
    t = T()

    def run(mutate=None, bed=None):
        d = tmpdir()
        O = _full(d, bed=bed, mutate=mutate)
        return c.compare_all(O, NSTEP, here=HERE, ref=os.path.join(HERE, 'run_40000'))

    def m_ulp(arm, kind, rows):
        if arm == 'BR' and kind == 'c':
            rows = [list(r) for r in rows]
            rows[0][23] = math.nextafter(rows[0][23], math.inf)
        return rows
    r, rc = run(m_ulp)
    t.ok('BR 1 ulp → 다-값 틀림', status_of(r, '다-값') == '틀림')
    t.ok('BR 1 ulp → 다-바이트 틀림', status_of(r, '다-바이트') == '틀림')
    t.ok('BR 1 ulp → 판정 PASS', r['judgment']['다']['status'] == 'PASS')
    t.ok('BR 1 ulp → 라 그대로 맞음', status_of(r, '라-값') == '맞음')

    def m_rev(arm, kind, rows):
        return list(reversed(rows)) if (arm == 'CR' and kind == 'c') else rows
    r, rc = run(m_rev)
    t.ok('CR 순서 → 라-값 맞음', status_of(r, '라-값') == '맞음')
    t.ok('CR 순서 → 라-바이트 틀림', status_of(r, '라-바이트') == '틀림')

    def m_bwfmt(arm, kind, rows):
        if arm == 'BW' and kind == 'atom':
            rows = [list(rr) for rr in rows]
            rows[0][2] = math.nextafter(rows[0][2], math.inf)
        return rows
    r, rc = run(m_bwfmt)
    t.ok('BW 원자 1 ulp → 나 틀림', status_of(r, '나') == '틀림')

    def m_force(arm, kind, rows):
        if arm == 'BR' and kind == 'c':
            rows = [list(rr) for rr in rows]
            rows[argmax_abs(rows, 10)][10] *= (1 + 2e-5)
        return rows
    r, rc = run(m_force)
    t.ok('BR 힘 2e-5 → 판정 FAIL', r['judgment']['다']['status'] == 'FAIL')

    def m_cdelta(arm, kind, rows):
        if arm == 'B' and kind == 'c':
            rows = [list(rr) for rr in rows]
            rows[0][26] = math.nextafter(rows[0][26], math.inf)
        return rows
    r, rc = run(m_cdelta)
    t.ok('B delta 1 ulp → 마-1 틀림', status_of(r, '마-1') == '틀림')

    def m_csh(arm, kind, rows):
        if arm == 'C' and kind == 'c':
            rows = [list(rr) for rr in rows]
            rows[2][22] = math.nextafter(rows[2][22], math.inf)
        return rows
    r, rc = run(m_csh)
    t.ok('C shear 1 ulp → 사 틀림', status_of(r, '사') == '틀림')
    t.ok('C shear 1 ulp → 마-3 틀림 (비주기)', status_of(r, '마-3') == '틀림')

    r, rc = run(bed=Bed(no_raise_B=True))
    t.ok('B 올림 없음 → 예외① 틀림', status_of(r, '예외①') == '틀림')

    def m_new0(arm, kind, rows):
        if arm in ('B', 'B2', 'BW', 'BR') and kind == 'c':
            rows = [list(rr) for rr in rows]
            for rr in rows:
                if rr[22:25] == [0.0, 0.0, 0.0]:
                    rr[21] *= 1.5
        return rows
    r, rc = run(m_new0)
    t.ok('새 쌍 shear 0 인데 deltaMax ≠ delta → 예외② 틀림', status_of(r, '예외②') == '틀림')

    def m_new_low(arm, kind, rows):
        if arm in ('B', 'B2', 'BW', 'BR') and kind == 'c':
            rows = [list(rr) for rr in rows]
            for rr in rows:
                if rr[22:25] == [0.0, 0.0, 0.0]:
                    rr[21] = rr[26] * 0.5
        return rows
    r, rc = run(m_new_low)
    e1 = r['predictions'].get('예외①') or {}
    t.ok('새 쌍 deltaMax < delta → 예외① 틀림 (a)', status_of(r, '예외①') == '틀림' and any('(a)' in w for w in e1.get('why', [])), e1.get('why'))

    def m_cdm(arm, kind, rows):
        if arm == 'C' and kind == 'c':
            rows = [list(rr) for rr in rows]
            rows[0][21] *= 1.01
        return rows
    r, rc = run(m_cdm)
    e1 = r['predictions'].get('예외①') or {}
    t.ok('C deltaMax ≠ A(N) → 예외① 틀림 (c)', status_of(r, '예외①') == '틀림' and any('(c)' in w for w in e1.get('why', [])), e1.get('why'))

    def m_bdrop(arm, kind, rows):
        return rows[1:] if (arm in ('B', 'B2', 'BW', 'BR') and kind == 'c') else rows
    r, rc = run(m_bdrop)
    e2 = r['predictions'].get('예외②') or {}
    t.ok('B 쌍 하나 없음 → 예외② 틀림 (사라진 쌍 A ≠ B)', status_of(r, '예외②') == '틀림' and any('사라진' in w for w in e2.get('why', [])), e2.get('why'))

    def m_ratoms(arm, kind, rows):
        return list(reversed(rows)) if (arm == 'BR' and kind == 'atom') else rows
    r, rc = run(m_ratoms)
    t.ok('BR 원자 순서 → 다-값 맞음', status_of(r, '다-값') == '맞음', r['predictions'].get('다-값'))
    t.ok('BR 원자 순서 → 다-바이트 틀림', status_of(r, '다-바이트') == '틀림')

    d = tmpdir()
    O = _full(d)
    os.remove(os.path.join(O, 'BR', 'post', 'c_%d.txt' % NSTEP))
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=os.path.join(HERE, 'run_40000'))
    t.ok('BR 파일 없음 → 다-값 계산 못 함', status_of(r, '다-값') == '계산 못 함')
    t.ok('BR 파일 없음 → 판정 NOT_COMPUTED 아니면 FAIL', r['judgment']['다']['status'] in ('FAIL', 'NOT_COMPUTED'))
    t.ok('BR 파일 없음 → rc 2', rc == 2, rc)
    return t


@test
def t14_ga_applicability():
    """가 · 라-재현 (나): 11-04 실행 파일 md5 · 명령 파일 md5 · 덱 md5 가 맞을 때만 판정 · 아니면 해당 없음."""
    c = load_cmp()
    t = T()
    d = tmpdir()
    O = _full(d)
    ref = os.path.join(d, 'ref')
    os.makedirs(ref)
    lm = 'f' * 32
    with open(os.path.join(ref, 'inputs.md5'), 'w') as f:
        f.write('%s  lmp_serialnovtk\n' % lm)
        for dk in DECKS7:
            f.write('%s  %s\n' % (md5f(os.path.join(HERE, dk)), dk))
    names = ['A/rst/restart_%d.bin' % NSTEP, 'A2/rst/restart_%d.bin' % NSTEP, 'A2/rst/restart_cmd.bin']
    names += ['%s/post/c_%d.txt' % (a, NSTEP) for a in ('A', 'A2', 'B', 'B2', 'C')]
    names += ['A/post/cpre_%d.txt' % (NSTEP - 1), 'A2/post/cpre_%d.txt' % (NSTEP - 1)]
    names += ['%s/post/atom_%d.txt' % (a, NSTEP) for a in ('A', 'A2', 'B', 'B2', 'C')]
    with open(os.path.join(ref, 'outputs.md5'), 'w') as f:
        for n in names:
            f.write('%s  %s\n' % (md5f(os.path.join(O, n)), n))
    r, _ = c.compare_all(O, NSTEP, here=HERE, ref=ref)
    t.ok('실행 파일 다름 → 가 해당 없음', status_of(r, '가') == '해당 없음')
    d2 = tmpdir()
    O2 = _full(d2, lmp_md5=lm)
    r, _ = c.compare_all(O2, NSTEP, here=HERE, ref=ref)
    t.ok('같은 실행 파일 · 같은 출력 → 가 맞음', status_of(r, '가') == '맞음', (r['predictions'].get('가')))
    t.ok('라-재현나 맞음', status_of(r, '라-재현나') == '맞음', r['predictions'].get('라-재현나'))
    p = os.path.join(O2, 'C', 'post', 'c_%d.txt' % NSTEP)
    lines = open(p).read().splitlines()
    lines[-1] = lines[-1] + ' '
    wtxt(p, '\n'.join(lines) + '\n')
    _rewrite_outputs(O2)
    r, _ = c.compare_all(O2, NSTEP, here=HERE, ref=ref)
    t.ok('C 바이트 다름 → 가 틀림', status_of(r, '가') == '틀림')
    t.ok('C 바이트 다름 → 라-재현나 틀림', status_of(r, '라-재현나') == '틀림')
    return t


def _rewrite_outputs(O):
    lines = []
    for arm in ARMS:
        for sub in ('post', 'rst'):
            dd = os.path.join(O, arm, sub)
            if os.path.isdir(dd):
                for fn in sorted(os.listdir(dd)):
                    lines.append('%s  %s/%s/%s' % (md5f(os.path.join(dd, fn)), arm, sub, fn))
    with open(os.path.join(O, 'outputs.md5'), 'w') as f:
        f.write('\n'.join(lines) + '\n')


@test
def t15_wall_scale():
    c = load_cmp()
    d = tmpdir()
    ar = Bed().atom_rows()
    ar = [list(r) for r in ar]
    ar[0][4] = ar[0][11] * 0.999          # z < r → 닿음
    ar[1][4] = ar[1][11]                  # z = r → 닿음 (≤ 0)
    ar[2][4] = ar[2][11] + 0.0003         # 근처 (skin 안)
    p = os.path.join(d, 'a.txt')
    wtxt(p, fmt_atoms(NSTEP, ar))
    w = c.wall_scale(c.read_atoms(p), c.material(HERE))
    t = T()
    t.ok('닿음 2', w['n_wall_touch'] == 2, w)
    t.ok('근처 1', w['n_wall_near'] == 1, w)
    return t


@test
def t16_cli_rc():
    d = tmpdir()
    p = subprocess.run([sys.executable, '-I', os.path.join(HERE, CMPFILE), os.path.join(d, 'none'), str(NSTEP)],
                       capture_output=True, text=True, timeout=120)
    t = T()
    t.ok('없는 OUT → rc 2', p.returncode == 2, (p.returncode, p.stderr[-300:]))
    O = _full(d)
    p = subprocess.run([sys.executable, '-I', os.path.join(HERE, CMPFILE), O, str(NSTEP)], capture_output=True, text=True, timeout=300)
    t.ok('정상 → rc 0', p.returncode == 0, (p.returncode, p.stderr[-500:]))
    t.ok('화면에 예측 줄', '다-값' in p.stdout and '바' in p.stdout, p.stdout[-300:])
    return t


@test
def t17_ma_sets():
    """마-2: B ≠ C 인 쌍 = A(N−1) ≠ A(N) 인 쌍 · 새 쌍 따로 — 정상 침대에서 집합이 맞고 수가 0 이 아님."""
    c = load_cmp()
    d = tmpdir()
    O = _full(d)
    r, _ = c.compare_all(O, NSTEP, here=HERE, ref=os.path.join(HERE, 'run_40000'))
    m2 = r['predictions']['마-2']
    t = T()
    t.ok('집합 크기 > 0', m2['n_set_BC'] > 0 and m2['n_set_BC'] == m2['n_set_A'], m2)
    t.ok('새 쌍 따로', m2['n_new'] == 2, m2)
    m3 = r['predictions']['마-3']
    t.ok('주기 쌍 힘 다름 = 주기 쌍 수', m3['n_flag1_force_differ'] == 3, m3)
    return t


# ═══ 덱 · 실행기 ════════════════════════════════════════════════════════════════════════
@test
def t20_bw_deck_shape():
    t = T()
    p = os.path.join(HERE, 'BW.liggghts')
    t.ok('BW 있음', os.path.exists(p))
    if os.path.exists(p):
        L = [x.strip() for x in open(p).read().splitlines() if x.strip() and not x.strip().startswith('#')]
        t.ok('꼴 = include R + write_restart', L == ['include R.liggghts', 'write_restart ${RST}/restart_rt.bin'], L)
    ref = {}
    for ln in open(os.path.join(HERE, 'run_40000', 'inputs.md5')).read().splitlines():
        h, n = ln.split()
        ref[n] = h
    for dk in DECKS7:
        t.ok(dk + ' = 11-04', md5f(os.path.join(HERE, dk)) == ref.get(dk), dk)
    return t


FAKE = r'''#!{PY}
import json, os, shutil, sys, time
a = sys.argv[1:]
mode = os.environ.get('FAKE_MODE', 'ok')
if '-h' in a:
    if mode != 'nobanner':
        print('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f · 가짜 lmp)')
    print('\nCommand line options:\n')
    sys.exit(0)
args, var = {}, {}
i = 0
while i < len(a):
    if a[i] == '-var':
        var[a[i + 1]] = a[i + 2]
        i += 3
    elif a[i] in ('-in', '-log'):
        args[a[i]] = a[i + 1]
        i += 2
    else:
        i += 1
post = var.get('POST', '')
arm = os.path.basename(os.path.dirname(post))
rec = dict(arm=arm, deck=args.get('-in'), deck_exists=os.path.exists(args.get('-in') or ''), var=var, cwd=os.getcwd(), nice=os.nice(0))
with open(os.environ['FAKE_LOG'], 'a') as f:
    f.write(json.dumps(rec) + '\n')
def at(kind):
    p = mode.split(':')
    return p[0] == kind and len(p) > 1 and p[1] == arm
if at('sleep'):
    time.sleep(float(mode.split(':')[2]))
if 'RFILE' in var and not os.path.exists(var['RFILE']):
    print('ERROR: Cannot open restart file ' + var['RFILE'])
    sys.exit(1)
store = os.environ['FAKE_STORE']
for sub, key in (('post', 'POST'), ('rst', 'RST')):
    src = os.path.join(store, arm, sub)
    if key in var and os.path.isdir(src):
        for fn in sorted(os.listdir(src)):
            if at('nofile') and sub == 'rst':
                continue
            shutil.copy(os.path.join(src, fn), os.path.join(var[key], fn))
with open(args['-log'], 'w') as f:
    f.write('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, git commit 3d5c00f · 가짜 lmp)\n')
    if at('error'):
        f.write('ERROR: 가짜 오류\n')
    if not at('noloop'):
        f.write('Loop time of 0.01 on 1 procs for 0 steps with 32 atoms\n')
sys.exit(1 if at('fail') else 0)
'''

_UNSHARE = None


def unshare_ok():
    global _UNSHARE
    if _UNSHARE is None:
        try:
            p = subprocess.run(['unshare', '-pf', '--mount-proc', '--kill-child', 'true'], capture_output=True, timeout=30)
            _UNSHARE = p.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            _UNSHARE = False
    return _UNSHARE


def safe_kill(p):
    """직접 만든 자식만 · pid > 1 · 자기 · 부모 아님 (unshare --kill-child 가 이름공간을 거둔다)."""
    pid = p.pid
    if not (isinstance(pid, int) and pid > 1 and pid != os.getpid() and pid != os.getppid()):
        raise RuntimeError('kill 대상 거부: %r' % pid)
    p.kill()
    p.wait()


def sandbox_copy(d):
    """실행기 시험용 사본 (리포 밖 · git 아님) — 덱 · 실행기 · 대조기 · 11-04 기록."""
    S = os.path.join(d, 'sandbox')
    os.makedirs(os.path.join(S, 'run_40000'))
    for fn in os.listdir(HERE):
        p = os.path.join(HERE, fn)
        if os.path.isfile(p):
            shutil.copy2(p, os.path.join(S, fn))
    for fn in ('inputs.md5', 'outputs.md5'):
        shutil.copy2(os.path.join(HERE, 'run_40000', fn), os.path.join(S, 'run_40000', fn))
    return S


def fake_env(d, mode='ok', store=None):
    fb = os.path.join(d, 'fakebin')
    os.makedirs(fb, exist_ok=True)
    lmp = os.path.join(fb, 'lmp_fake')
    with open(lmp, 'w') as f:
        f.write(FAKE.replace('{PY}', sys.executable))
    os.chmod(lmp, 0o755)
    if store is None:
        store = os.path.join(d, 'store')
        write_fixture(store)
    env = {k: v for k, v in os.environ.items() if k not in ('LMP', 'G2CP_TLONG', 'G2CP_TSHORT')}
    env.update(LMP=lmp, FAKE_MODE=mode, FAKE_STORE=store, FAKE_LOG=os.path.join(d, 'fake.jsonl'))
    return env


def run_runner(S, args, env, limit=180):
    cmd = ['bash', os.path.join(S, RUNNER)] + list(args)
    wrap = unshare_ok()
    if wrap:
        cmd = ['unshare', '-pf', '--mount-proc', '--kill-child'] + cmd
    p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        out, err = p.communicate(timeout=limit if wrap else None)
    except subprocess.TimeoutExpired:
        safe_kill(p)
        return 'TIMEOUT', '', ''
    return p.returncode, out, err


def fake_calls(d):
    p = os.path.join(d, 'fake.jsonl')
    if not os.path.exists(p):
        return []
    return [json.loads(x) for x in open(p).read().splitlines() if x.strip()]


def listing(S):
    out = []
    for r, ds, fs in os.walk(S):
        for f in fs:
            out.append(os.path.relpath(os.path.join(r, f), S))
    return sorted(out)


@test
def t21_runner_no_lmp():
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d)
    del env['LMP']
    O = os.path.join(d, 'O')
    rc, out, err = run_runner(S, [str(NSTEP), O], env)
    t = T()
    t.ok('rc 3', rc == 3, (rc, err[-300:]))
    t.ok('이유 LMP', 'LMP' in err, err[-300:])
    t.ok('OUT 안 만듦', not os.path.exists(O))
    t.ok('가짜 안 불림', fake_calls(d) == [])
    return t


@test
def t22_runner_lmp_bad():
    t = T()
    for case in ('없는 파일', '실행 권한 없음', '배너 없음', '폴더'):
        d = tmpdir()
        S = sandbox_copy(d)
        env = fake_env(d, mode='nobanner' if case == '배너 없음' else 'ok')
        if case == '없는 파일':
            env['LMP'] = os.path.join(d, 'nope')
        elif case == '실행 권한 없음':
            os.chmod(env['LMP'], 0o644)
        elif case == '폴더':
            env['LMP'] = d
        O = os.path.join(d, 'O')
        rc, out, err = run_runner(S, [str(NSTEP), O], env)
        t.ok(case + ' rc 3', rc == 3, (rc, err[-200:]))
        t.ok(case + ' OUT 없음', not os.path.exists(O))
        t.ok(case + ' 팔 안 돎', [c for c in fake_calls(d) if c.get('arm')] == [])
    return t


@test
def t23_runner_args_out():
    t = T()
    for N in ('abc', '150', '0', '40050', '-100'):
        d = tmpdir()
        S = sandbox_copy(d)
        env = fake_env(d)
        rc, out, err = run_runner(S, [N, os.path.join(d, 'O')], env)
        t.ok('N=%s rc 3' % N, rc == 3, (rc, err[-200:]))
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d)
    O = os.path.join(d, 'O')
    os.makedirs(O)
    wtxt(os.path.join(O, 'keep.txt'), 'x')
    rc, out, err = run_runner(S, [str(NSTEP), O], env)
    t.ok('비지 않은 OUT rc 3', rc == 3, (rc, err[-200:]))
    t.ok('비지 않은 OUT 그대로', os.listdir(O) == ['keep.txt'])
    rc, out, err = run_runner(S, [str(NSTEP)], env)
    t.ok('인자 하나 rc 3', rc == 3)
    return t


@test
def t24_runner_deck_guards():
    t = T()
    d = tmpdir()
    S = sandbox_copy(d)
    with open(os.path.join(S, 'mat.inc'), 'a') as f:
        f.write('# 바뀜\n')
    env = fake_env(d)
    rc, out, err = run_runner(S, [str(NSTEP), os.path.join(d, 'O')], env)
    t.ok('mat.inc 바뀜 rc 3', rc == 3, (rc, err[-200:]))
    t.ok('mat.inc 이유', 'mat.inc' in err)
    d = tmpdir()
    S = sandbox_copy(d)
    with open(os.path.join(S, 'BW.liggghts'), 'a') as f:
        f.write('run 10\n')
    env = fake_env(d)
    rc, out, err = run_runner(S, [str(NSTEP), os.path.join(d, 'O')], env)
    t.ok('BW 꼴 바뀜 rc 3', rc == 3, (rc, err[-200:]))
    t.ok('BW 이유', 'BW' in err)
    return t


@test
def t25_runner_git_dirty():
    t = T()
    if shutil.which('git') is None:
        raise Skip('git 없음')
    d = tmpdir()
    S = sandbox_copy(d)
    g = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
    for cmd in (['git', 'init', '-q'], ['git', 'add', '-A'], ['git', 'commit', '-q', '-m', 'x']):
        subprocess.run(cmd, cwd=S, env=g, check=True, capture_output=True)
    env = fake_env(d)
    O1 = os.path.join(d, 'O1')
    rc, out, err = run_runner(S, [str(NSTEP), O1], env)
    t.ok('깨끗 → rc 0', rc == 0, (rc, err[-300:]))
    wtxt(os.path.join(S, 'new_untracked.txt'), 'x')
    d2 = tmpdir()
    env2 = fake_env(d2)
    rc, out, err = run_runner(S, [str(NSTEP), os.path.join(d2, 'O2')], env2)
    t.ok('더러움 → rc 3', rc == 3, (rc, err[-300:]))
    t.ok('더러움 이유', '커밋' in err, err[-300:])
    return t


@test
def t26_runner_ok_fake():
    t = T()
    d = tmpdir()
    S = sandbox_copy(d)
    before = listing(S)
    env = fake_env(d)
    O = os.path.join(d, 'O')
    rc, out, err = run_runner(S, [str(NSTEP), O], env)
    t.ok('rc 0', rc == 0, (rc, err[-500:]))
    calls = fake_calls(d)
    arms = [c['arm'] for c in calls if c.get('arm')]
    t.ok('차례 9 팔', arms == list(ARMS), arms)
    by = {c['arm']: c for c in calls if c.get('arm')}
    t.ok('nice 19', all(c['nice'] == 19 for c in by.values()), [c['nice'] for c in by.values()])
    t.ok('덱 cwd 기준 있음', all(c['deck_exists'] for c in by.values()))
    rf = {a: by[a]['var'].get('RFILE') for a in ('B', 'B2', 'C', 'BW', 'BR', 'CW', 'CR')}
    want = {'B': 'A/rst/restart_%d.bin' % NSTEP, 'B2': 'A2/rst/restart_%d.bin' % NSTEP, 'C': 'A2/rst/restart_cmd.bin',
            'BW': 'A/rst/restart_%d.bin' % NSTEP, 'BR': 'BW/rst/restart_rt.bin', 'CW': 'A2/rst/restart_cmd.bin',
            'CR': 'CW/rst/restart_rt.bin'}
    for a, w in want.items():
        t.ok(a + ' RFILE', (rf[a] or '').endswith('/' + w), (a, rf[a]))
    decks = {a: by[a]['deck'] for a in ARMS}
    t.ok('덱 이름', decks == {'A': 'A.liggghts', 'A2': 'A2.liggghts', 'B': 'R.liggghts', 'B2': 'R.liggghts', 'C': 'R.liggghts',
                           'BW': 'BW.liggghts', 'BR': 'R.liggghts', 'CW': 'BW.liggghts', 'CR': 'R.liggghts'}, decks)
    t.ok('A 변수', by['A']['var'].get('N') == str(NSTEP) and by['A']['var'].get('NM1') == str(NSTEP - 1)
         and by['A']['var'].get('RA') == str(NSTEP + 999), by['A']['var'])
    t.ok('A2 변수', by['A2']['var'].get('R2') == str(NSTEP - 1))
    t.ok('BW RST', by['BW']['var'].get('RST', '').endswith('/BW/rst') and by['CW']['var'].get('RST', '').endswith('/CW/rst'))
    for fn in ('lmp_identity.txt', 'inputs.md5', 'outputs.md5', 'rc.txt'):
        t.ok(fn, os.path.exists(os.path.join(O, fn)))
    if os.path.exists(os.path.join(O, 'rc.txt')):
        rcl = open(os.path.join(O, 'rc.txt')).read().split('\n')
        t.ok('rc.txt 9 줄 rc 0', len([x for x in rcl if ' rc 0 ' in x + ' ']) == 9, rcl)
    if os.path.exists(os.path.join(O, 'lmp_identity.txt')):
        ident = open(os.path.join(O, 'lmp_identity.txt')).read()
        t.ok('배너 기록', 'LIGGGHTS (Version' in ident)
        t.ok('md5 · sha256 기록', md5f(env['LMP']) in ident and hashlib.sha256(open(env['LMP'], 'rb').read()).hexdigest() in ident)
    if os.path.exists(os.path.join(O, 'outputs.md5')):
        om = open(os.path.join(O, 'outputs.md5')).read()
        t.ok('outputs 경로 꼴', ('BR/post/c_%d.txt' % NSTEP) in om and './' not in om, om[:200])
    t.ok('사본 폴더 그대로', listing(S) == before, sorted(set(listing(S)) ^ set(before))[:5])
    t.ok('STOP 없음', not os.path.exists(os.path.join(O, 'STOP.txt')))
    return t


@test
def t27_runner_stops():
    t = T()
    for mode, arm, why in (('fail:BW', 'BW', 'rc 1'), ('nofile:BW', 'BW', 'restart_rt.bin'), ('error:B', 'B', 'ERROR'),
                           ('noloop:C', 'C', 'Loop time')):
        d = tmpdir()
        S = sandbox_copy(d)
        env = fake_env(d, mode=mode)
        O = os.path.join(d, 'O')
        rc, out, err = run_runner(S, [str(NSTEP), O], env)
        t.ok(mode + ' rc 4', rc == 4, (rc, err[-300:]))
        arms = [c['arm'] for c in fake_calls(d) if c.get('arm')]
        t.ok(mode + ' 거기서 멈춤', arms == list(ARMS[:ARMS.index(arm) + 1]), arms)
        st = os.path.join(O, 'STOP.txt')
        t.ok(mode + ' STOP 이유', os.path.exists(st) and why in open(st).read(), open(st).read() if os.path.exists(st) else None)
    return t


@test
def t28_runner_timeout_in_namespace():
    """시간 한도 = 신호 시험 → unshare -pf --mount-proc --kill-child 안에서만."""
    if not unshare_ok():
        raise Skip('unshare -pf --mount-proc 못 씀 — 신호 시험 건너뜀')
    t = T()
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d, mode='sleep:B:30')
    env['G2CP_TSHORT'] = '2'
    O = os.path.join(d, 'O')
    t0 = time.time()
    rc, out, err = run_runner(S, [str(NSTEP), O], env, limit=90)
    dt = time.time() - t0
    t.ok('rc 4', rc == 4, (rc, err[-300:]))
    t.ok('25 s 안', dt < 25, dt)
    rcl = open(os.path.join(O, 'rc.txt')).read() if os.path.exists(os.path.join(O, 'rc.txt')) else ''
    t.ok('B rc 124', 'B rc 124' in rcl, rcl)
    st = os.path.join(O, 'STOP.txt')
    t.ok('STOP 시간 한도', os.path.exists(st) and '시간 한도' in open(st).read())
    return t


@test
def t29_runner_then_compare():
    """끝-끝 배관: 가짜 lmp 실행기 → 대조기 CLI (rc 0 · 예측 표)."""
    t = T()
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d)
    O = os.path.join(d, 'O')
    rc, out, err = run_runner(S, [str(NSTEP), O], env)
    t.ok('실행기 rc 0', rc == 0, (rc, err[-300:]))
    p = subprocess.run([sys.executable, '-I', os.path.join(S, CMPFILE), O, str(NSTEP)], capture_output=True, text=True, timeout=300)
    t.ok('대조기 rc 0', p.returncode == 0, (p.returncode, p.stderr[-500:]))
    j = os.path.join(O, 'compare_g2cp.json')
    if os.path.exists(j):
        r = json.load(open(j))
        t.ok('다-값 맞음', status_of(r, '다-값') == '맞음', r['predictions'].get('다-값'))
        t.ok('바 맞음', status_of(r, '바') == '맞음')
        t.ok('가 해당 없음 (가짜 실행 파일)', status_of(r, '가') == '해당 없음')
    else:
        t.ok('JSON', False)
    return t


# ═══ 돌리기 ═════════════════════════════════════════════════════════════════════════════
def main():
    npass = nfail = nskip = 0
    for fn in TESTS:
        try:
            r = fn()
            if r.bad:
                nfail += 1
                print('FAIL %s — %s' % (fn.__name__, ' | '.join(str(x)[:300] for x in r.bad[:4])))
            else:
                npass += 1
                print('PASS %s' % fn.__name__)
        except Skip as e:
            nskip += 1
            print('SKIP %s — %s' % (fn.__name__, e))
        except Exception as e:  # noqa: BLE001 — 시험 하나의 예외는 그 시험의 실패다
            nfail += 1
            print('FAIL %s — 예외 %s: %s' % (fn.__name__, type(e).__name__, str(e)[:300]))
    for d in _TMP:
        shutil.rmtree(d, ignore_errors=True)
    print('G2CP_TEST pass=%d fail=%d skip=%d total=%d' % (npass, nfail, nskip, len(TESTS)))
    return 0 if nfail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
