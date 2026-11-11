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
    시간 한도 · 사람 멈춤 시험 = 신호 시험이라 건너뜀 · 건너뜀 수를 마지막 줄에 적는다).  kill 은 직접 만든 자식에만 · pid > 1 · 자기 · 부모 아님 —
    사람 멈춤 시험 (t31) 은 이름공간 안 드라이버 (`--sigdriver` · 이름공간 PID 1) 가 실행기 bash (직접 자식) 에만 보낸다.
다. 메모 등록문 (t30) — §0 의 등록 문장이 §4 · 소스 · Codex 답과 어긋나지 않는지 (11-10 내부 반박 리뷰 G2CPR-02 · 09).
11-10 (2) 내부 반박 리뷰 G2CPR-01–11 고침 = 시험 먼저 (t04 · t07 · t08 · t13 · t25 보강 · t30–t39 새로 · 고치기 전 실패 → 뒤 통과).
11-11 2 회차 내부 반박 리뷰 G2CPR2-01–05 고침 = 시험 먼저 (t40 완료 문 · t41 실행기 OUT 자리 · t42 표기 새로 · t08 · t16 · t34 · t37 보강 ·
합성 fixture 가 실행기 꼴대로 rc.txt 도 쓴다).
11-11 3 회차 내부 반박 리뷰 G2CPR3-01–04 고침 = 시험 먼저 (t43 완료 문의 outputs.md5 ↔ 실제 출력 대조 새로 · t39 dry/ · t41 자리 문 두 경계 ·
t42 표기 보강 · t13 = 덤프를 바꾼 fixture 는 outputs.md5 도 실행기 꼴대로 다시 쓴다).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import random
import re
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True   # 리포 폴더에 __pycache__ 를 만들지 않는다

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
KIT = os.path.join(REPO, 'docs', 'data', 'ps45_unload_20261009')
MEMO = os.path.join(REPO, 'docs', 'reviews', 'p1_g2c_compare_definition_20261105.md')
REF40 = os.path.join(HERE, 'run_40000')
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
    with open(os.path.join(root, 'rc.txt'), 'w') as f:      # 실행기가 팔마다 한 줄 (`<팔> rc <rc> sec <초>`) — 끝난 실행 = 아홉 줄 rc 0 (G2CPR2-01)
        f.write(rc_lines())
    return bed


def rc_lines(arms=ARMS, sec=0):
    """실행기 rc.txt 꼴 — 끝난 팔마다 `<팔> rc 0 sec <초>` 한 줄 (run_g2cp.sh 의 go)."""
    return ''.join('%s rc 0 sec %d\n' % (a, sec) for a in arms)


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

    def tok_at(col, new):
        return '\n'.join(L[:k + 1] + [' '.join([new if j == col else tok for j, tok in enumerate(L[k + 1].split())])] + L[k + 2:]) + '\n'
    cases = {
        'id 2.5': '\n'.join(L[:k + 1] + [' '.join(['2.5' if j == 6 else tok for j, tok in enumerate(L[k + 1].split())])] + L[k + 2:]) + '\n',
        'NaN': '\n'.join(L[:k + 1] + [' '.join(['nan' if j == 12 else tok for j, tok in enumerate(L[k + 1].split())])] + L[k + 2:]) + '\n',
        'id 2^53+1': '\n'.join(L[:k + 1] + [' '.join(['9007199254740993' if j == 7 else tok for j, tok in enumerate(L[k + 1].split())])] + L[k + 2:]) + '\n',
        # G2CPR-04 — 숫자 토큰 = ASCII · 밑줄 없음 (float() · Decimal() 이 받는 '1_0' · 전각 · 아라비아-인도 숫자를 거부)
        '값 1_0': tok_at(12, '1_0'),
        '값 전각 숫자': tok_at(12, '１２'),
        'id 1_0': tok_at(7, '1_0'),
        'id 아라비아-인도 숫자': tok_at(6, '١٢'),
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
    Dn = c.read_local(os.path.join(d, 'none.txt'))
    t.ok('없는 파일 → 문제', not Dn['ok'])
    t.ok('없는 파일 → 필수 열 결손 (G2CPR-03 · 키트 cols None 과 같음)', Dn.get('missing_required') is True, Dn.get('missing_required'))
    An = c.read_atoms(os.path.join(d, 'none_atoms.txt'))
    t.ok('없는 원자 파일 → 필수 열 결손', not An['ok'] and An.get('missing_required') is True, An.get('missing_required'))
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
             '이력만': g, '빠짐': rows[2:], '중복': rows + [rows[1]], '충돌': rows + dc, '감음': wr, 'floor': fl,
             '파일 없음': None}           # G2CPR-03 — 키트 = NOT_COMPUTED (cols None) · 대조기도 같아야 한다
    for name, r2 in cases.items():
        p1, p2 = os.path.join(d, 'k1.txt'), os.path.join(d, 'k2.txt')
        wtxt(p1, fmt_local(NSTEP, [r[:21] + r[25:] for r in rows], ncol=26))
        if r2 is None:
            p2 = os.path.join(d, 'k2_none.txt')
        else:
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
    # G2CPR-04 — 원자 상자도 값 같음에 든다 (§0-2 "상자 같음")
    p1, p2 = os.path.join(d, 'a1.txt'), os.path.join(d, 'a2.txt')
    wtxt(p1, fmt_atoms(NSTEP, ar))
    wtxt(p2, fmt_atoms(NSTEP, ar, box=(BOXB[0], BOXB[1], (-0.001, 0.05))))
    v = c.atoms_value(c.read_atoms(p1), c.read_atoms(p2))
    t.ok('원자 상자 다름 → 값 다름', v.get('computed') and not v['equal'], v)
    # G2CPR-04 — 숫자 토큰 ASCII (전각 숫자 = 읽기 문제) · 꼴 (type '01' = %d 꼴 아님 → 값 같음 계산 못 함)
    L = fmt_atoms(NSTEP, ar).splitlines()
    tk = L[-1].split()
    tk[4] = '０.００５'
    L[-1] = ' '.join(tk)
    wtxt(p, '\n'.join(L) + '\n')
    t.ok('원자 전각 숫자 → 문제', not c.read_atoms(p)['ok'])
    L = fmt_atoms(NSTEP, ar).splitlines()
    tk = L[-1].split()
    tk[1] = '0' + tk[1]
    L[-1] = ' '.join(tk)
    wtxt(p2, '\n'.join(L) + '\n')
    v = c.atoms_value(c.read_atoms(p1), c.read_atoms(p2))
    t.ok("원자 type '0n' → 꼴 아님 → 값 계산 못 함", not v.get('computed'), v)
    # G2CPR2-04 — 원자 id 토큰도 `%d` 꼴이어야 한다 ('+n' · 'n.0' = 같은 정수 값이지만 등록 덱 출력 꼴이 아님 → 값 같음 = 계산 못 함)
    for name, mk in (("'+n'", lambda s: '+' + s), ("'n.0'", lambda s: s + '.0')):
        L = fmt_atoms(NSTEP, ar).splitlines()
        tk = L[-1].split()
        tk[0] = mk(tk[0])
        L[-1] = ' '.join(tk)
        wtxt(p2, '\n'.join(L) + '\n')
        A2 = c.read_atoms(p2)
        t.ok('원자 id %s → 읽기는 됨 (같은 정수)' % name, A2['ok'] and len(A2['by_id']) == len(ar), A2['problems'][:2])
        t.ok('원자 id %s → 꼴 아님 (form17 False)' % name, A2.get('form17') is False and A2.get('n_nonform') == 1, (A2.get('form17'), A2.get('n_nonform')))
        v = c.atoms_value(c.read_atoms(p1), A2)
        t.ok('원자 id %s → 값 계산 못 함' % name, not v.get('computed'), v)
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
    # 기록 (outputs.md5) 이 실제 출력과 맞는 채로 덤프가 없는 꼴 — 규칙 ⑧ (파일 없음 = 필수 열 결손) 자체를 본다 (실행기 need 가 막는 꼴이라
    # 실제로는 못 생긴다 · 끝난 뒤 빠진 꼴 = outputs.md5 에 적혔는데 없음 은 t43 · 완료 문 출력 손상 · G2CPR3-01)
    _rewrite_outputs(O)
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=os.path.join(HERE, 'run_40000'))
    t.ok('BR 파일 없음 → 완료 문 지남 (기록 = 실제 출력)', (r.get('run_gate') or {}).get('ok') is True, r.get('run_gate'))
    t.ok('BR 파일 없음 → 다-값 계산 못 함', status_of(r, '다-값') == '계산 못 함')
    t.ok('BR 파일 없음 → 판정 NOT_COMPUTED (G2CPR-03 · 키트와 같음 · 기술 실패를 값 불일치로 적지 않는다)',
         r['judgment']['다']['status'] == 'NOT_COMPUTED', r['judgment']['다'].get('status'))
    t.ok('BR 파일 없음 → rc 2', rc == 2, rc)
    # G2CPR-10 — BW · BR 같은 자리에 같은 nan (두 파일 바이트 같음) → 바이트 = sha256 만으로 맞음 · 값 = 계산 못 함 · 판정 FAIL (키트와 같음)
    d = tmpdir()
    O = _full(d)
    for arm in ('BW', 'BR'):
        p = os.path.join(O, arm, 'post', 'c_%d.txt' % NSTEP)
        L = open(p).read().splitlines()
        k = next(i for i, x in enumerate(L) if x.startswith('ITEM: ENTRIES'))
        tk = L[k + 1].split()
        tk[18] = 'nan'
        L[k + 1] = ' '.join(tk)
        wtxt(p, '\n'.join(L) + '\n')
    _rewrite_outputs(O)     # 실행기가 그 덤프를 쓴 꼴 — outputs.md5 = 실제 출력 (완료 문이 대조한다 · G2CPR3-01)
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=os.path.join(HERE, 'run_40000'))
    t.ok('같은 nan → 다-바이트 맞음 (값 실패와 따로)', status_of(r, '다-바이트') == '맞음', r['predictions'].get('다-바이트'))
    t.ok('같은 nan → 다-값 계산 못 함', status_of(r, '다-값') == '계산 못 함')
    t.ok('같은 nan → 판정 FAIL', r['judgment']['다']['status'] == 'FAIL', r['judgment']['다'].get('status'))
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
    t.ok('화면에 완료 문 지남 줄 (G2CPR2-01)', [ln for ln in p.stdout.splitlines() if ln.startswith('완료 문 ')] == ['완료 문 지남'], p.stdout[-300:])
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
import json, os, shutil, signal, sys, time
a = sys.argv[1:]
mode = os.environ.get('FAKE_MODE', 'ok')
if os.environ.get('FAKE_TERM_DELAY'):      # 느린 종료 흉내 (TERM 뒤 몇 초 더 살아 있음) — 실행기가 거둔 뒤 끝나는지 가르게
    def _late(_s, _f):
        time.sleep(float(os.environ['FAKE_TERM_DELAY']))
        os._exit(143)
    signal.signal(signal.SIGTERM, _late)
if '-h' in a:
    if mode.startswith('hsleep:'):      # 실행 전 (-h 머리 줄 확인 중) 사람 멈춤 시험 — 시작을 적고 잠든다
        with open(os.environ['FAKE_LOG'], 'a') as f:
            f.write(json.dumps(dict(h=1)) + '\n')
        time.sleep(float(mode.split(':')[1]))
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


def run_runner(S, args, env, limit=180, cwd=None):
    cmd = ['bash', os.path.join(S, RUNNER)] + list(args)
    wrap = unshare_ok()
    if wrap:
        cmd = ['unshare', '-pf', '--mount-proc', '--kill-child'] + cmd
    p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)
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
    # 시험 위생 (11-10 리뷰): 서명 · 훅이 켜진 기계에서도 버리는 임시 커밋이 서명 프로그램 · 훅을 부르지 않는다 —
    # 서명을 강제하고 서명 프로그램 = false 인 전역 설정을 일부러 씌워 그 길이 닫혔는지 본다
    gc = os.path.join(d, 'gitconfig_sign_trap')
    wtxt(gc, '[commit]\n\tgpgsign = true\n[gpg]\n\tprogram = false\n')
    g = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t',
             GIT_CONFIG_GLOBAL=gc, GIT_CONFIG_NOSYSTEM='1')
    for cmd in (['git', 'init', '-q'], ['git', 'add', '-A'],
                ['git', '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null', 'commit', '-q', '-m', 'x']):
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


# ═══ 11-10 (2) 내부 반박 리뷰 G2CPR-01–11 — 시험 먼저 ════════════════════════════════════════
def _memo_section(txt, start, end):
    a = txt.index(start)
    return txt[a:txt.index(end, a + len(start))]


def _table_cells(row):
    return [c.strip() for c in re.split(r'(?<!\\)\|', row.strip())][1:-1]


def _pkey(r):
    return (min(int(r[6]), int(r[7])), max(int(r[6]), int(r[7])))


@test
def t30_memo_registration_text():
    """메모 §0 등록문 — G2CPR-02 (바 '틀리면' = §4 문구 그대로 · 좁히지 않음) · G2CPR-09 (가) 다-바이트 근거의 pbc 문장 = domain.cpp 그대로 ·
    (나) §0-5 에 Codex Q6-1 원자 12 열 한정 (힘 합산 순서로 원자 12 열 차이를 설명하지 않는다)."""
    t = T()
    txt = open(MEMO, encoding='utf-8').read()
    s0 = _memo_section(txt, '\n## 0. ', '\n## 1. ')
    s4 = _memo_section(txt, '\n## 4. ', '\n## 5. ')
    t.ok('§4 틀리면 규칙 원문 그대로', '마 · 바 ✗ = "주기 ↔ 명령 차이 = 저장 shear 뿐" 서술을 거두고 다시 본다' in s4)
    rows = {}
    for ln in s0.splitlines():
        if ln.startswith('| ') and not ln.startswith('|---'):
            cells = _table_cells(ln)
            if cells:
                rows.setdefault(cells[0], cells)
    ba = rows.get('바')
    t.ok('§0-3 바 행', ba is not None and len(ba) == 5, ba)
    if ba and len(ba) == 5:
        t.ok("바 '틀리면' = §4 문구 ('저장 shear 뿐' · §4 그대로)", '저장 shear 뿐' in ba[3] and '§4 그대로' in ba[3], ba[3])
    db = rows.get('다-바이트')
    t.ok('§0-3 다-바이트 행', db is not None and len(db) == 5, db)
    if db and len(db) == 5:
        t.ok('pbc 문장 = 소스 (domain.cpp 562–564 · MAX(x, lo))', 'hi 쪽 가드가 없어' not in db[4] and '562' in db[4] and 'MAX' in db[4], db[4])
    s05 = _memo_section(txt, '\n### 0-5. ', '\n### 0-6. ')
    t.ok('§0-5 Q6-1 원자 12 열 한정', '원자 12 열' in s05 and '힘 합산 순서' in s05, s05[-300:])
    return t


def _sig_driver(argv):
    """t31 의 이름공간 안 드라이버 (`unshare -pf --mount-proc --kill-child` 아래 · 이 프로세스 = 이름공간 PID 1).
    실행기 bash 를 직접 자식으로 띄우고 · 가짜 lmp 팔 A 가 시작한 뒤 · 그 자식 (pid > 1 · 자기 · 부모 아님) 에만 신호를 보낸다."""
    S, O, sig, d, wait_for = argv
    p = subprocess.Popen(['bash', os.path.join(S, RUNNER), str(NSTEP), O], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    t0 = time.time()

    def started():
        return any((c.get('arm') == 'A') if wait_for == 'A' else c.get('h') for c in fake_calls(d))
    while time.time() - t0 < 30 and p.poll() is None and not started():
        time.sleep(0.05)
    time.sleep(0.5)
    pid = p.pid
    if not (isinstance(pid, int) and pid > 1 and pid != os.getpid() and pid != os.getppid()):
        raise RuntimeError('신호 대상 거부: %r' % pid)
    sent = p.poll() is None
    ts = time.time()
    if sent:
        os.kill(pid, getattr(signal, sig))
    try:
        _out, err = p.communicate(timeout=60)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        safe_kill(p)
        rc, err = 'TIMEOUT', ''
    dt = time.time() - ts
    time.sleep(0.3)
    left = []
    for q in os.listdir('/proc'):
        if q.isdigit():
            try:
                cl = open('/proc/%s/cmdline' % q, 'rb').read().replace(b'\0', b' ').decode('utf-8', 'replace')
            except OSError:
                continue
            if 'lmp_fake' in cl:
                left.append(cl[:120])
    print(json.dumps(dict(rc=rc, dt=dt, sent=sent, left=left, err=(err or '')[-400:]), ensure_ascii=False))
    return 0


@test
def t31_runner_signal_stops():
    """G2CPR-08 — 사람이 멈춤 (INT = Ctrl-C · TERM · HUP = 터미널 닫힘) → 실행기가 도는 팔의 timeout 에만 TERM → 가짜 LIGGGHTS 멈춤 ·
    rc.txt · STOP.txt · rc 4 · 남은 팔 안 돎 · 실행기가 끝난 뒤 남은 LIGGGHTS 0 · 실행 전 (-h 중) INT = rc 3 · OUT 안 만듦.
    신호 시험 = 이름공간 안 (드라이버 = PID 1 · 신호 = 직접 자식 실행기 bash 에만)."""
    if not unshare_ok():
        raise Skip('unshare -pf --mount-proc 못 씀 — 신호 시험 건너뜀')
    t = T()
    for sig in ('SIGINT', 'SIGTERM', 'SIGHUP', 'pre-SIGINT'):
        pre = sig.startswith('pre-')
        sg = sig[4:] if pre else sig
        d = tmpdir()
        S = sandbox_copy(d)
        env = fake_env(d, mode='hsleep:15' if pre else 'sleep:A:15')
        env['FAKE_TERM_DELAY'] = '2'          # 가짜 LIGGGHTS 가 TERM 뒤 2 s 더 산다 → 실행기가 거두지 않고 나가면 남은 lmp 로 잡힌다
        O = os.path.join(d, 'O')
        p = subprocess.run(['unshare', '-pf', '--mount-proc', '--kill-child', sys.executable, '-I', os.path.abspath(__file__),
                            '--sigdriver', S, O, sg, d, 'h' if pre else 'A'], env=env, capture_output=True, text=True, timeout=150)
        try:
            r = json.loads(p.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            t.ok(sig + ' 드라이버 출력', False, (p.returncode, p.stdout[-300:], p.stderr[-300:]))
            continue
        t.ok(sig + ' 보냄', r['sent'], r)
        if pre:   # 실행 전 (-h 중) 멈춤 = rc 3 · OUT 안 만듦 · 팔 안 돎 · -h 의 가짜 lmp 도 거둠
            t.ok(sig + ' 실행기 rc 3', r['rc'] == 3, r)
            t.ok(sig + ' 10 s 안에 멈춤', isinstance(r['dt'], (int, float)) and r['dt'] < 10, r['dt'])
            t.ok(sig + ' 남은 가짜 lmp 0', r['left'] == [], r['left'])
            t.ok(sig + ' OUT 안 만듦', not os.path.exists(O))
            t.ok(sig + ' 팔 안 돎', [c for c in fake_calls(d) if c.get('arm')] == [])
            continue
        t.ok(sig + ' 실행기 rc 4', r['rc'] == 4, r)
        t.ok(sig + ' 10 s 안에 멈춤', isinstance(r['dt'], (int, float)) and r['dt'] < 10, r['dt'])
        t.ok(sig + ' 남은 가짜 lmp 0', r['left'] == [], r['left'])
        arms = [c['arm'] for c in fake_calls(d) if c.get('arm')]
        t.ok(sig + ' 팔 A 만 돎', arms == ['A'], arms)
        st = os.path.join(O, 'STOP.txt')
        t.ok(sig + ' STOP 이유 = 신호', os.path.exists(st) and '신호' in open(st).read(), open(st).read() if os.path.exists(st) else None)
        rcl = open(os.path.join(O, 'rc.txt')).read() if os.path.exists(os.path.join(O, 'rc.txt')) else ''
        t.ok(sig + ' rc.txt 신호 줄', ('A 신호 ' + sig[3:]) in rcl, rcl)
    return t


class _BedCoh(Bed):
    KINDS = Bed.KINDS + ('cohesion',) * 11


class _Bed0(Bed):
    KINDS = ()


@test
def t32_cohesion_guard_full_set():
    """G2CPR-01 — cohesion 가드 쌍 12 (보여주기 10 개보다 많음) 도 마-1 deltaMax 비교에서 전부 뺀다 · 예외① 이 계산 못 함이어도 같다."""
    c = load_cmp()
    t = T()
    d = tmpdir()
    O = _full(d, bed=_BedCoh())
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    t.ok('가드 쌍 12', r['exceptions']['①'].get('n_cohesion_guarded_A') == 12, r['exceptions']['①'].get('n_cohesion_guarded_A'))
    t.ok('마-1 맞음', status_of(r, '마-1') == '맞음', r['predictions'].get('마-1'))
    t.ok('마-1 뺀 수 12', (r['predictions'].get('마-1') or {}).get('n_cohesion_excluded') == 12, r['predictions'].get('마-1'))
    t.ok('rc 0', rc == 0, rc)

    def m_cr_nan(arm, kind, rows):
        if arm == 'CR' and kind == 'c':
            rows = [list(rr) for rr in rows]
            rows[0][12] = float('nan')
        return rows
    d2 = tmpdir()
    O2 = _full(d2, mutate=m_cr_nan)
    r2, _ = c.compare_all(O2, NSTEP, here=HERE, ref=REF40)
    t.ok('예외① 계산 못 함 (CR 읽기 문제)', status_of(r2, '예외①') == '계산 못 함', r2['predictions'].get('예외①'))
    t.ok('그래도 마-1 맞음 (가드 쌍 = 마-1 이 직접 셈)', status_of(r2, '마-1') == '맞음', r2['predictions'].get('마-1'))
    return t


@test
def t33_value_needs_17g_form():
    """G2CPR-04 (나) — 값 같음은 `%.17g` 꼴 토큰에서만 — 6 자리 %g 덤프 (3e-9 차이가 글자로 같아짐) = 값 · 바이트 예측 계산 못 함 ·
    판정 = 키트 식 그대로 (허용폭 · 6 자리 덤프에 맞춘 식)."""
    c = load_cmp()
    t = T()
    d = tmpdir()
    rows = Bed().rows('BW')
    rowsR = [list(r) for r in rows]
    for r in rowsR:
        for col in (9, 10, 11, 22, 23, 24):
            r[col] = r[col] * (1 + 3e-9)
    p1, p2 = os.path.join(d, 'g1.txt'), os.path.join(d, 'g2.txt')
    wtxt(p1, fmt_local(NSTEP, rows, tokfmt='%g'))
    wtxt(p2, fmt_local(NSTEP, rowsR, tokfmt='%g'))
    D1, D2 = c.read_local(p1), c.read_local(p2)
    t.ok('읽기 ok (판정은 그대로 돈다)', D1['ok'] and D2['ok'], (D1['problems'][:2], D2['problems'][:2]))
    v = c.pairs_value(D1, D2)
    t.ok('값 같음 = 계산 못 함 (꼴)', not v.get('computed'), v)
    t.ok('판정 = PASS (키트 식)', c.judge(D1, D2, expected_step=NSTEP)['status'] == 'PASS')
    O = _full(d)

    def g_rows(rr):
        return [list(x) for x in rr]
    for arm, rr in (('BW', g_rows(rows)), ('BR', g_rows(rowsR))):
        wtxt(os.path.join(O, arm, 'post', 'c_%d.txt' % NSTEP), fmt_local(NSTEP, rr, tokfmt='%g'))
    _rewrite_outputs(O)
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    t.ok('다-값 계산 못 함', status_of(r, '다-값') == '계산 못 함', r['predictions'].get('다-값'))
    t.ok('다-바이트 계산 못 함 (등록 덱 덤프 꼴 아님)', status_of(r, '다-바이트') == '계산 못 함', r['predictions'].get('다-바이트'))
    t.ok('라 그대로 맞음', status_of(r, '라-값') == '맞음')
    t.ok('rc 2', rc == 2, rc)
    return t


@test
def t34_registered_deck_gate():
    """G2CPR-04 (라) — OUT/inputs.md5 의 덱 여덟 (11-04 일곱 + BW) md5 가 이 폴더 파일과 같을 때만 등록 예측을 판독한다 —
    아니면 (가 · 라-재현 (나) 빼고) 계산 못 함 · 판정 NOT_COMPUTED · rc 2."""
    c = load_cmp()
    t = T()
    gated = ('나', '다-값', '다-바이트', '라-값', '라-바이트', '라-재현가', '마-1', '마-2', '마-3', '바', '사', '예외①', '예외②')
    unknown_cases = ('inputs 없음', 'R 중복 줄', 'R 꼴 밖 중복 줄 (대문자 16 진)', 'R 꼴 밖 중복 줄 (짧은 값)', '이름 없는 줄')
    for case in ('R 다름', 'BW 빠짐') + unknown_cases:
        d = tmpdir()
        O = _full(d)
        p = os.path.join(O, 'inputs.md5')
        if case == 'inputs 없음':
            os.remove(p)
        else:
            L = open(p).read().splitlines()
            if case == 'R 다름':
                L = [('0' * 32 + '  R.liggghts') if ln.endswith('  R.liggghts') else ln for ln in L]
            elif case == 'R 중복 줄':     # 모호한 기록 (앞 = 틀린 md5 · 뒤 = 맞는 md5) — 한 줄만 골라 읽지 않는다
                L = [('0' * 32 + '  R.liggghts') for ln in L if ln.endswith('  R.liggghts')] + L
            elif case == 'R 꼴 밖 중복 줄 (대문자 16 진)':   # G2CPR2-02 — 같은 이름 줄은 hash 꼴 (32 자리 소문자 16 진) 이 아니어도 센다 (말없이 버리지 않는다)
                L = L + ['ABCDEF0123456789ABCDEF0123456789  R.liggghts']
            elif case == 'R 꼴 밖 중복 줄 (짧은 값)':
                L = ['89c4a85c2f9ec763c37f  R.liggghts'] + L
            elif case == '이름 없는 줄':                    # 어느 이름의 줄인지 못 읽는 줄 (잘린 줄) = 기록 전체 모름
                L = L + ['89c4a85c2f9ec763c37fdb5c3aa3f664']
            else:
                L = [ln for ln in L if not ln.endswith('  BW.liggghts')]
            wtxt(p, '\n'.join(L) + '\n')
        r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
        bad = [(k, status_of(r, k)) for k in gated if status_of(r, k) != '계산 못 함']
        t.ok(case + ' 등록 예측 = 계산 못 함', not bad, bad[:4])
        js = [r.get('judgment', {}).get(x, {}).get('status') for x in ('다', '라')]
        t.ok(case + ' 판정 NOT_COMPUTED', js == ['NOT_COMPUTED', 'NOT_COMPUTED'], js)
        t.ok(case + ' rc 2', rc == 2, rc)
        if case in unknown_cases:   # 덱 기록을 모름 → 가 · 라-재현 (나) 의 조건도 모름 = 계산 못 함 ('다름' 아님)
            t.ok(case + ' 가 · 라-재현나 계산 못 함', status_of(r, '가') == '계산 못 함' and status_of(r, '라-재현나') == '계산 못 함',
                 (status_of(r, '가'), status_of(r, '라-재현나')))
    return t


@test
def t35_empty_and_atom_id_mismatch():
    """G2CPR-05 — (가) 쌍 0 침대 (건식 N = 200 꼴) = 예측 해당 없음 (맞음 아님) · 판정 = 키트 식 PASS + 쌍 0 표지 ·
    (나) C 원자 덤프 ID 가 쌍 ID 와 안 맞으면 바 = 계산 못 함 (조용히 건너뛰어 해당 없음 아님)."""
    c = load_cmp()
    t = T()
    d = tmpdir()
    O = _full(d, bed=_Bed0())
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    for k in ('나', '다-값', '다-바이트', '라-값', '라-바이트', '라-재현가', '마-1', '마-2', '마-3', '바', '사', '예외①', '예외②'):
        t.ok(k + ' 해당 없음', status_of(r, k) == '해당 없음', (k, status_of(r, k), (r['predictions'].get(k) or {}).get('why')))
    jd = r['judgment']['다']
    t.ok('판정 다 PASS + 쌍 0 표지', jd['status'] == 'PASS' and jd.get('n_ref') == 0 and '쌍 0' in str(jd.get('note', '')), jd)
    t.ok('rc 0', rc == 0, rc)

    def m5(arm, kind, rows):
        if kind == 'atom' and arm == 'C':
            rows = [list(rr) for rr in rows]
            for rr in rows:
                rr[0] = rr[0] + 1000
        return rows
    d2 = tmpdir()
    O2 = _full(d2, mutate=m5)
    r2, rc2 = c.compare_all(O2, NSTEP, here=HERE, ref=REF40)
    t.ok('바 계산 못 함 (쌍 원자가 원자 덤프에 없음)', status_of(r2, '바') == '계산 못 함', r2['predictions'].get('바'))
    t.ok('rc 2', rc2 == 2, rc2)
    return t


@test
def t36_exc2_sets_and_orientation():
    """G2CPR-06 — 예외② (가) 사라진 쌍 = 집합 비교 (B 에서 다른 쌍 하나를 빼고 사라진 쌍을 넣어 수만 같음 = 틀림) ·
    (나) 새 쌍 왕복 = §0-2 값 규칙 (BR 에서 새 쌍 행 방향만 바뀜 = 맞음 · torque 는 같은 방향 행만)."""
    c = load_cmp()
    t = T()
    bed = Bed()
    cpre = bed.rows('cpre')

    def m4(arm, kind, rows):
        if arm == 'B' and kind == 'c':
            now = {_pkey(rr) for rr in rows}
            gone = [rr for rr in cpre if _pkey(rr) not in now]
            rows = [list(rr) for rr in rows[1:]] + [list(gone[0])]
        return rows
    d = tmpdir()
    O = _full(d, bed=bed, mutate=m4)
    r, _ = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    e2 = r['predictions'].get('예외②') or {}
    t.ok('바꿔치기 → 예외② 틀림 (사라진 쌍 집합)', e2.get('status') == '틀림' and any('사라진' in w for w in e2.get('why', [])), e2)
    bed2 = Bed()
    newkeys = {(min(p['i'], p['j']), max(p['i'], p['j'])) for p in bed2.pairs if p['kind'] in ('new0', 'newstale')}

    def m8(arm, kind, rows):
        if arm == 'BR' and kind == 'c':
            rows = [flip_row(rr) if _pkey(rr) in newkeys else list(rr) for rr in rows]
        return rows
    d2 = tmpdir()
    O2 = _full(d2, bed=bed2, mutate=m8)
    r2, _ = c.compare_all(O2, NSTEP, here=HERE, ref=REF40)
    t.ok('새 쌍 방향만 → 예외② 맞음', status_of(r2, '예외②') == '맞음', r2['predictions'].get('예외②'))
    t.ok('새 쌍 방향만 → 다-값 맞음', status_of(r2, '다-값') == '맞음', r2['predictions'].get('다-값'))
    return t


@test
def t37_identity_unknown_is_not_computed():
    """G2CPR-07 — 실행 파일 신원 (lmp_md5) · 입력 덱 기록을 모르면 가 · 라-재현 (나) = 계산 못 함 (모르는 것을 '다르다' 로 적지 않는다) ·
    같은 이름 두 줄 = 모호한 기록 = 모름 (11-11 작은 반례)."""
    c = load_cmp()
    t = T()
    for case in ('lmp_md5 줄 없음', 'lmp_md5 꼴 아님', 'lmp_md5 두 줄'):
        d = tmpdir()
        O = _full(d)
        p = os.path.join(O, 'lmp_identity.txt')
        L = [ln for ln in open(p).read().splitlines() if not ln.startswith('lmp_md5 ')]
        if case == 'lmp_md5 꼴 아님':
            L.append('lmp_md5 xyz')
        elif case == 'lmp_md5 두 줄':     # 모호한 기록 (뒤 줄 = 11-04 실행 파일 md5) — 마지막 줄만 골라 읽지 않는다
            L += ['lmp_md5 ' + '0' * 32, 'lmp_md5 f4ba3ec04933d70b641421e39e6cb283']
        wtxt(p, '\n'.join(L) + '\n')
        r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
        t.ok(case + ' → 가 계산 못 함', status_of(r, '가') == '계산 못 함', r['predictions'].get('가'))
        t.ok(case + ' → 라-재현나 계산 못 함', status_of(r, '라-재현나') == '계산 못 함', r['predictions'].get('라-재현나'))
        t.ok(case + ' → 다른 예측 그대로', status_of(r, '다-값') == '맞음' and status_of(r, '바') == '맞음')
        t.ok(case + ' → rc 2', rc == 2, rc)
    d = tmpdir()
    O = _full(d)
    os.remove(os.path.join(O, 'inputs.md5'))
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    t.ok('inputs.md5 없음 → 가 계산 못 함', status_of(r, '가') == '계산 못 함', r['predictions'].get('가'))
    t.ok('inputs.md5 없음 → 라-재현나 계산 못 함', status_of(r, '라-재현나') == '계산 못 함', r['predictions'].get('라-재현나'))
    # G2CPR2-02 — 실행 파일 md5 는 두 곳에 적힌다 (lmp_identity.txt 의 lmp_md5 · OUT/inputs.md5 첫 줄 = 실행기가 맨 앞에 쓰는 실행 파일 줄) —
    # 둘이 어긋나면 신원 = 모름 (한 기록만 골라 '11-04 와 같은 실행 파일' 로 판정하지 않는다)
    ref_lmp = open(os.path.join(REF40, 'inputs.md5')).read().split()[0]
    d = tmpdir()
    O = _full(d, lmp_md5=ref_lmp)
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    t.ok('대조 — 두 기록 같음 (11-04 실행 파일 md5) → 가 · 라-재현나 판정됨 (계산 못 함 아님)',
         status_of(r, '가') in ('맞음', '틀림') and status_of(r, '라-재현나') in ('맞음', '틀림', '해당 없음'),
         (status_of(r, '가'), status_of(r, '라-재현나'), (r['predictions'].get('가') or {}).get('why')))
    for case in ('inputs.md5 첫 줄 = 다른 값', 'inputs.md5 첫 줄 꼴 아님', 'inputs.md5 첫 줄 = 덱 줄 (실행 파일 줄 없음)',
                 'inputs.md5 실행 파일 줄 두 번 (첫 줄 = 같은 값 · 둘째 = 다른 값)'):
        d = tmpdir()
        O = _full(d, lmp_md5=ref_lmp)
        p = os.path.join(O, 'inputs.md5')
        L = open(p).read().splitlines()
        if case == 'inputs.md5 첫 줄 = 다른 값':
            L[0] = '0' * 32 + '  lmp'
        elif case == 'inputs.md5 첫 줄 꼴 아님':
            L[0] = ref_lmp.upper() + '  lmp'
        elif case.startswith('inputs.md5 실행 파일 줄 두 번'):     # 규칙 ⑩ — 같은 이름 두 줄 = 모호 (맞는 첫 줄만 골라 읽지 않는다)
            L = [L[0], '0' * 32 + '  lmp'] + L[1:]
        else:
            L = L[1:]
        wtxt(p, '\n'.join(L) + '\n')
        r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
        t.ok(case + ' → 가 계산 못 함', status_of(r, '가') == '계산 못 함', r['predictions'].get('가'))
        t.ok(case + ' → 라-재현나 계산 못 함', status_of(r, '라-재현나') == '계산 못 함', r['predictions'].get('라-재현나'))
        t.ok(case + ' → 다른 예측 그대로', status_of(r, '다-값') == '맞음' and status_of(r, '바') == '맞음')
        t.ok(case + ' → rc 2', rc == 2, rc)
    return t


@test
def t38_runner_identity_records():
    """G2CPR-07 (실행기) — LMP 가 심볼릭 링크여도 lmp_bytes = 대상 파일 크기 (stat -L) · lmp_realpath · glibc 줄 ·
    공유 라이브러리 기록 (lmp_ldd.txt · lmp_libs.md5 — 기록만 · 판정 조건 아님)."""
    t = T()
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d)
    target = env['LMP']
    link = os.path.join(d, 'lmp_link')
    os.symlink(target, link)
    env['LMP'] = link
    O = os.path.join(d, 'O')
    rc, out, err = run_runner(S, [str(NSTEP), O], env)
    t.ok('rc 0', rc == 0, (rc, err[-300:]))
    p = os.path.join(O, 'lmp_identity.txt')
    ident = {}
    if os.path.exists(p):
        for ln in open(p).read().splitlines():
            k, _, v = ln.partition(' ')
            ident[k] = v
    t.ok('lmp_bytes = 대상 크기', ident.get('lmp_bytes') == str(os.path.getsize(target)), (ident.get('lmp_bytes'), os.path.getsize(target)))
    t.ok('lmp_realpath = 대상', ident.get('lmp_realpath') == os.path.realpath(link), ident.get('lmp_realpath'))
    t.ok('glibc 줄', 'glibc' in ident, sorted(ident))
    pl = os.path.join(O, 'lmp_ldd.txt')
    t.ok('lmp_ldd.txt', os.path.exists(pl))
    t.ok('lmp_libs.md5', os.path.exists(os.path.join(O, 'lmp_libs.md5')))
    if shutil.which('ldd') and os.path.exists(pl):     # ldd 가 있는 기계 = 원문 + rc 를 실제로 적었나 (가짜 lmp 는 스크립트라 라이브러리 줄은 없다)
        t.ok('ldd 원문 · rc 기록', any(ln.startswith('ldd_rc ') for ln in open(pl).read().splitlines()), open(pl).read()[-200:])
    return t


@test
def t39_compare_out_guard():
    """G2CPR-11 — 대조기는 실행기 출력 (lmp_identity.txt + 팔 폴더 아홉) 에만 JSON 을 쓴다 · OUT = 샌드박스 폴더 · 11-04 기록 폴더 ·
    샌드박스의 조상 = 거부 (쓰지 않음 · rc 2)."""
    c = load_cmp()
    t = T()
    d = tmpdir()
    S = sandbox_copy(d)
    ref = os.path.join(S, 'run_40000')
    before = listing(S)
    for name, O in (('샌드박스 폴더', S), ('11-04 기록 폴더', ref), ('조상 폴더', d)):
        r, rc = c.compare_all(O, NSTEP, here=S, ref=ref)
        t.ok(name + ' rc 2', rc == 2, rc)
        t.ok(name + ' JSON 안 씀', not os.path.exists(os.path.join(O, 'compare_g2cp.json')))
    t.ok('샌드박스 사본 그대로', listing(S) == before, sorted(set(listing(S)) ^ set(before))[:5])
    O2 = os.path.join(d, 'plain')
    os.makedirs(O2)
    wtxt(os.path.join(O2, 'x.txt'), 'x')
    r, rc = c.compare_all(O2, NSTEP, here=S, ref=ref)
    t.ok('실행기 출력 아님 → rc 2 · JSON 안 씀', rc == 2 and not os.path.exists(os.path.join(O2, 'compare_g2cp.json')), rc)
    d3 = tmpdir()
    O3 = _full(d3)
    os.remove(os.path.join(O3, 'lmp_identity.txt'))
    r, rc = c.compare_all(O3, NSTEP, here=HERE, ref=REF40)
    t.ok('신원 파일 없음 → rc 2 · JSON 안 씀', rc == 2 and not os.path.exists(os.path.join(O3, 'compare_g2cp.json')), rc)
    # 검사 하나가 다른 검사 뒤에 숨지 않게 (11-11 변이: 조상 · 기록 폴더 검사를 빼도 다른 검사가 대신 잡던 틈)
    d4 = tmpdir()
    S4 = sandbox_copy(d4)
    ref_out = os.path.join(tmpdir(), 'ref_elsewhere')       # 기록 폴더가 샌드박스 밖 — 조상 거부를 샌드박스 검사 혼자 해야 한다
    shutil.copytree(os.path.join(S4, 'run_40000'), ref_out)
    for a in ARMS:                                           # d4 를 실행기 꼴로 (신원 파일 + 팔 폴더) — 그래도 샌드박스의 조상이라 거부
        os.makedirs(os.path.join(d4, a), exist_ok=True)
    wtxt(os.path.join(d4, 'lmp_identity.txt'), 'lmp_md5 ' + '0' * 32 + '\n')
    r, rc = c.compare_all(d4, NSTEP, here=S4, ref=ref_out)
    t.ok('조상 (기록 폴더 밖) → rc 2 · JSON 안 씀', rc == 2 and not os.path.exists(os.path.join(d4, 'compare_g2cp.json')), rc)
    inner = os.path.join(S4, 'run_40000', 'runner_shaped')    # 기록 폴더 안의 실행기 꼴 OUT — 실행기 출력 검사로는 못 막는다
    write_fixture(inner)
    r, rc = c.compare_all(inner, NSTEP, here=os.path.join(d4, 'other_here'), ref=os.path.join(S4, 'run_40000'))
    t.ok('기록 폴더 안 실행기 꼴 → rc 2 · JSON 안 씀', rc == 2 and not os.path.exists(os.path.join(inner, 'compare_g2cp.json')), rc)
    # G2CPR3-02 — 11-04 기록 폴더 = run_40000/ · dry/ (규칙 ⑨) — dry/ 안의 실행기 꼴 출력 (옛 실행기 · 손으로 옮긴 출력) 도 거부
    # (고치기 전 = rc 0 · dry/ 안에 JSON) · 실제 경로로 본다 (dry 가 링크면 그 대상 안 · 그 조상도 거부 — run_40000 과 같은 규칙)
    d5 = tmpdir()
    S5 = sandbox_copy(d5)
    O5 = os.path.join(S5, 'dry', 'oldrun')
    write_fixture(O5)
    before5 = listing(S5)

    def refused5(name, O, here):
        r, rc = c.compare_all(O, NSTEP, here=here, ref=os.path.join(here, 'run_40000'))
        why = ' '.join((r['predictions'].get('입력') or {}).get('why', []))
        t.ok(name + ' → rc 2 · JSON 안 씀', rc == 2 and not os.path.exists(os.path.join(O, 'compare_g2cp.json')), (rc, why[:160]))
        t.ok(name + " → 이유 '11-04 기록 폴더 dry/'", '11-04 기록 폴더 dry/' in why, why[:200])
    refused5('dry/ 안 실행기 꼴 (dry/oldrun)', O5, S5)
    refused5('dry/ 자신', os.path.join(S5, 'dry'), S5)
    t.ok('dry/ → 샌드박스 사본 그대로', listing(S5) == before5, sorted(set(listing(S5)) ^ set(before5))[:5])
    d6 = tmpdir()
    S6 = sandbox_copy(d6)
    ext = tmpdir()                                            # 샌드박스 밖 — dry 링크의 대상
    os.makedirs(os.path.join(ext, 'dry_real'))
    os.symlink(os.path.join(ext, 'dry_real'), os.path.join(S6, 'dry'))
    O6 = os.path.join(ext, 'dry_real', 'oldrun')
    write_fixture(O6)
    refused5('dry 링크 대상 안 (실제 경로 · ext/dry_real/oldrun)', O6, S6)
    write_fixture(ext)                                        # dry 링크 대상의 조상을 실행기 꼴로 — 샌드박스의 조상은 아니다
    refused5('dry 링크 대상의 조상 (ext)', ext, S6)
    return t


# ═══ 11-11 2 회차 내부 반박 리뷰 G2CPR2-01–05 — 시험 먼저 ══════════════════════════════════════
ALL15 = ('가', '나', '다-값', '다-바이트', '라-값', '라-바이트', '라-재현가', '라-재현나', '마-1', '마-2', '마-3', '바', '사', '예외①', '예외②')


@test
def t40_compare_completion_gate():
    """G2CPR2-01 (메모 §0-3 규칙 ⑪ 완료 문) — 대조기는 **끝난** 실행기 출력만 판독한다: OUT/outputs.md5 있음 ∧ OUT/STOP.txt 없음 ∧
    OUT/rc.txt = 팔 아홉이 차례대로 한 줄씩 `<팔> rc 0 sec <초>`.  멈춘 OUT (리뷰 재현 A1 = CR 시간 한도 · 덤프 반쯤 · A2 = 덤프는 다 쓰고
    ERROR 로 멈춤) · 도는 중인 OUT = 예측 15 모두 계산 못 함 · 판정 NOT_COMPUTED + 기술 실패 표지 · rc 2 — 기술 실패를 FAIL (값 불일치) 이나
    PASS · 맞음으로 적지 않는다.  세 조건은 따로 선다 (하나만 어긋나도 막힘)."""
    c = load_cmp()
    t = T()

    def blocked(name, O):
        r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
        bad = [(k, status_of(r, k)) for k in ALL15 if status_of(r, k) != '계산 못 함']
        t.ok(name + ' → 예측 15 모두 계산 못 함', not bad, bad[:4])
        js = [r.get('judgment', {}).get(x, {}).get('status') for x in ('다', '라')]
        t.ok(name + ' → 판정 NOT_COMPUTED', js == ['NOT_COMPUTED', 'NOT_COMPUTED'], js)
        t.ok(name + ' → 판정에 기술 실패 표지', all(r.get('judgment', {}).get(x, {}).get('technical_failure') is True for x in ('다', '라')),
             r.get('judgment'))
        t.ok(name + ' → rc 2', rc == 2, rc)
        t.ok(name + ' → 완료 문 막힘', (r.get('run_gate') or {}).get('ok') is False, r.get('run_gate'))
        # G2CPR3-01 뒤 — 끝나지 않은 실행 (멈춤 · 도는 중) 은 '끝난 뒤 출력 손상' 과 다른 사유로 적는다 (t43)
        t.ok(name + ' → 사유 = 끝나지 않음 (출력 손상 아님)',
             all('끝나지 않' in ' '.join(r.get('judgment', {}).get(x, {}).get('why', [])) and '출력 손상' not in str(r.get('judgment', {}).get(x, {}).get('note', ''))
                 for x in ('다', '라')), [r.get('judgment', {}).get(x, {}).get('note') for x in ('다', '라')])
        return r

    # 리뷰 재현 A1 — CR 이 시간 한도 (rc 124) 로 멈춤: CR 쌍 덤프 반쯤 · STOP.txt · outputs.md5 없음 (고치기 전 = 판정 라 FAIL · 마 · 바 · 사 맞음)
    d = tmpdir()
    O = _full(d)
    p = os.path.join(O, 'CR', 'post', 'c_%d.txt' % NSTEP)
    L = open(p).read().splitlines()
    wtxt(p, '\n'.join(L[:-5]) + '\n')
    os.remove(os.path.join(O, 'outputs.md5'))
    wtxt(os.path.join(O, 'STOP.txt'), 'CR rc 124 (시간 한도 600 s 넘음)\n')
    wtxt(os.path.join(O, 'rc.txt'), rc_lines(ARMS[:-1]) + 'CR rc 124 sec 600\n')
    r = blocked('A1 (CR 시간 한도 · 덤프 반쯤)', O)
    jp = os.path.join(O, 'compare_g2cp.json')
    t.ok('A1 → JSON 에도 완료 문 막힘 (JSON 만 봐도 가른다)', os.path.exists(jp) and (json.load(open(jp)).get('run_gate') or {}).get('ok') is False)
    t.ok('A1 → 이유에 STOP.txt · outputs.md5 · rc.txt', all(any(s in w for w in (r.get('run_gate') or {}).get('why', []))
                                                       for s in ('STOP.txt', 'outputs.md5', 'rc.txt')), (r.get('run_gate') or {}).get('why'))
    # 리뷰 재현 A2 — CR 덤프까지 다 쓴 뒤 로그 ERROR → 실행기 rc 4 · STOP.txt (고치기 전 = 예측 맞음 · 판정 PASS · rc 0)
    d = tmpdir()
    O = _full(d)
    os.remove(os.path.join(O, 'outputs.md5'))
    wtxt(os.path.join(O, 'STOP.txt'), 'CR 로그 · 화면에 ERROR 줄\n')
    blocked('A2 (덤프 다 쓴 뒤 ERROR 로 멈춤)', O)

    # 세 조건이 따로 서는지 — 하나만 어긋난 OUT
    def one(name, fn):
        d = tmpdir()
        O = _full(d)
        fn(O)
        blocked(name, O)

    one('outputs.md5 만 없음 (도는 중 · 끝 단계 전에 죽음)', lambda O: os.remove(os.path.join(O, 'outputs.md5')))
    one('STOP.txt 만 있음 (끝 단계 outputs.md5 쓰다 멈춤)', lambda O: wtxt(os.path.join(O, 'STOP.txt'), 'outputs.md5 쓰기 실패\n'))
    one('STOP.txt 가 빈 파일이어도', lambda O: wtxt(os.path.join(O, 'STOP.txt'), ''))
    one('rc.txt 없음', lambda O: os.remove(os.path.join(O, 'rc.txt')))
    one('rc.txt 여덟 줄 (CR 줄 없음)', lambda O: wtxt(os.path.join(O, 'rc.txt'), rc_lines(ARMS[:-1])))
    one('rc.txt B rc 1', lambda O: wtxt(os.path.join(O, 'rc.txt'), rc_lines().replace('B rc 0 ', 'B rc 1 ')))
    one('rc.txt 끝에 신호 줄', lambda O: wtxt(os.path.join(O, 'rc.txt'), rc_lines() + 'CR 신호 TERM\n'))
    one('rc.txt 같은 팔 두 줄', lambda O: wtxt(os.path.join(O, 'rc.txt'), 'A rc 0 sec 0\n' + rc_lines()))
    one('rc.txt 차례 바뀜', lambda O: wtxt(os.path.join(O, 'rc.txt'), rc_lines(('A2', 'A') + ARMS[2:])))
    one('rc.txt rc 값 꼴 아님 (rc 00)', lambda O: wtxt(os.path.join(O, 'rc.txt'), rc_lines().replace('C rc 0 ', 'C rc 00 ')))

    # 대조 — 끝난 실행 = 완료 문 지남 · 판독함 (초 값은 무엇이든 · 시계가 뒤로 가 음수여도 끝난 실행이다)
    d = tmpdir()
    O = _full(d)
    wtxt(os.path.join(O, 'rc.txt'), rc_lines(ARMS[:2], sec=20) + rc_lines(ARMS[2:-1]) + 'CR rc 0 sec -1\n')
    r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    t.ok('끝난 실행 → 완료 문 지남', (r.get('run_gate') or {}).get('ok') is True, r.get('run_gate'))
    t.ok('끝난 실행 → 판독함 (다-값 맞음 · 판정 PASS · rc 0)',
         status_of(r, '다-값') == '맞음' and r['judgment']['다']['status'] == 'PASS' and rc == 0, (status_of(r, '다-값'), rc))
    t.ok('끝난 실행 → 판정에 기술 실패 표지 없음', not r['judgment']['다'].get('technical_failure'))

    # 끝-끝 (실제 실행기 · 가짜 lmp) — 팔 CR 이 덤프를 다 쓰고 ERROR → 실행기 rc 4 · STOP.txt → 대조기 CLI = rc 2 · 계산 못 함
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d, mode='error:CR')
    O = os.path.join(d, 'O')
    rc, out, err = run_runner(S, [str(NSTEP), O], env)
    t.ok('실행기 error:CR → rc 4 · STOP.txt', rc == 4 and os.path.exists(os.path.join(O, 'STOP.txt')), (rc, err[-300:]))
    t.ok('실행기 error:CR → CR 덤프는 다 있음 (판독하면 맞음으로 나올 꼴)', os.path.exists(os.path.join(O, 'CR', 'post', 'c_%d.txt' % NSTEP)))
    p = subprocess.run([sys.executable, '-I', os.path.join(S, CMPFILE), O, str(NSTEP)], capture_output=True, text=True, timeout=300)
    t.ok('멈춘 실행기 출력 → 대조기 CLI rc 2', p.returncode == 2, (p.returncode, p.stdout[-300:], p.stderr[-300:]))
    gl = [ln for ln in p.stdout.splitlines() if ln.startswith('완료 문 ')]      # 예측 줄의 사유 글자와 섞이지 않게 줄 머리로 가른다
    t.ok('멈춘 실행기 출력 → 화면에 완료 문 막힘 줄 하나 (사유에 STOP.txt)',
         len(gl) == 1 and gl[0].startswith('완료 문 막힘') and 'STOP.txt' in gl[0], (gl, p.stdout[-300:]))
    jp = os.path.join(O, 'compare_g2cp.json')
    if os.path.exists(jp):
        j = json.load(open(jp))
        bad = [(k, status_of(j, k)) for k in ALL15 if status_of(j, k) != '계산 못 함']
        t.ok('멈춘 실행기 출력 → JSON 예측 15 계산 못 함', not bad, bad[:4])
        t.ok('멈춘 실행기 출력 → JSON 판정 NOT_COMPUTED',
             [j.get('judgment', {}).get(x, {}).get('status') for x in ('다', '라')] == ['NOT_COMPUTED', 'NOT_COMPUTED'], j.get('judgment'))
    else:
        t.ok('멈춘 실행기 출력 → JSON (표지를 담아 씀)', False)
    return t


RUN_MARKS = ('lmp_identity.txt', 'inputs.md5')     # 런 표지 = 실행기가 OUT 에 맨 먼저 쓰는 파일 (run_g2cp.sh · 11-04 run_arms.sh)


@test
def t41_runner_out_location():
    """G2CPR2-05 — 실행기가 OUT 자리를 시작 전에 본다 (대조기 out_guard 의 자리 규칙 + dry/ · 기존 런 폴더 안): 11-04 기록 폴더 (run_40000 · dry) 안 ·
    다른 런의 출력 폴더 안 (OUT 의 조상에 런 표지 파일) · 심볼릭 링크로 돌아 들어가는 길 = rc 3 · 아무것도 안 만듦 · 팔 안 돎.
    샌드박스 안 새 폴더 = 그대로 받는다 (대조기 규칙 ⑨ 와 같음).  고치기 전 = 기록 폴더 안에 팔 아홉을 쓰고 rc 0."""
    t = T()
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d)
    os.makedirs(os.path.join(S, 'dry'))      # sandbox_copy 는 dry/ 를 안 옮긴다 — 빈 폴더 (런 표지 없음) 로 두어 '기록 폴더' 규칙 혼자 막는지 본다

    def arms_run():
        return len([c for c in fake_calls(d) if c.get('arm')])

    def tree():                               # 파일 + 폴더 (빈 폴더 하나도 새로 생기면 안 된다)
        out = []
        for r, ds, fs in os.walk(d):
            out += [os.path.relpath(os.path.join(r, x), d) for x in ds + fs]
        return sorted(out)

    def refused(name, O, why, new=True, cwd=None):      # new = 없던 자리 (아무것도 안 만듦) · False = 이미 있는 폴더 (그대로 둠) · cwd = 상대 경로 OUT 의 기준
        n0, before = arms_run(), tree()
        rc, out, err = run_runner(S, [str(NSTEP), O], env, limit=60, cwd=cwd)
        t.ok(name + ' → rc 3', rc == 3, (rc, err[-300:]))
        t.ok(name + " → 이유 '%s'" % why, why in err, err[-300:])
        t.ok(name + (' → 아무것도 안 만듦' if new else ' → 그대로'),
             (not new or not os.path.lexists(os.path.normpath(os.path.join(cwd or '', O)))) and tree() == before,
             sorted(set(tree()) ^ set(before))[:5])
        t.ok(name + ' → 팔 안 돎', arms_run() == n0, arms_run() - n0)

    def accepted(name, O, cwd=None):          # 받는 자리 — rc 0 · 그 자리에 팔 아홉 (실제 경로 = cwd 기준)
        n0 = arms_run()
        rc, out, err = run_runner(S, [str(NSTEP), O], env, limit=60, cwd=cwd)
        real = os.path.normpath(os.path.join(cwd or '', O))
        t.ok(name + ' → rc 0 (받음) · 팔 아홉 · 그 자리에 끝난 출력', rc == 0 and arms_run() - n0 == 9 and os.path.isfile(os.path.join(real, 'outputs.md5')),
             (rc, arms_run() - n0, err[-300:]))

    def refused_existing(name, O, why):       # 이미 있는 (비지 않은) 폴더 — 자리 이유가 '비어 있지 않다' 보다 먼저 나온다
        refused(name, O, why, new=False)

    refused_existing('샌드박스 폴더 자신', S, '샌드박스')
    refused_existing('샌드박스의 조상', d, '샌드박스')
    refused('기록 폴더 안 (run_40000/newrun)', os.path.join(S, 'run_40000', 'newrun'), '기록 폴더')
    refused('기록 폴더 안 깊이 (run_40000/a/b)', os.path.join(S, 'run_40000', 'a', 'b'), '기록 폴더')
    refused_existing('기록 폴더 자신 (run_40000)', os.path.join(S, 'run_40000'), '기록 폴더')
    refused('기록 폴더 안 (dry/newrun)', os.path.join(S, 'dry', 'newrun'), '기록 폴더')
    lnk = os.path.join(d, 'lnk')
    os.symlink(os.path.join(S, 'run_40000'), lnk)
    refused('링크로 기록 폴더 안 (lnk → run_40000 · lnk/new)', os.path.join(lnk, 'new'), '기록 폴더')
    refused('.. 로 돌아 기록 폴더 안 (x/../run_40000/new)', os.path.join(S, 'x', '..', 'run_40000', 'new'), '기록 폴더')

    # 샌드박스 안 새 폴더 = 받음 (규칙 ⑨ 와 같음 · 고침이 받던 자리를 막지 않는다) → 그 런 폴더 안의 새 OUT = 거부
    O1 = os.path.join(S, 'newrun_ok')
    rc, out, err = run_runner(S, [str(NSTEP), O1], env)
    t.ok('샌드박스 안 새 폴더 → rc 0 (받음)', rc == 0, (rc, err[-300:]))
    t.ok('샌드박스 안 새 폴더 → 팔 아홉', arms_run() == 9, arms_run())
    refused('기존 런 폴더 안 (끝난 런/again)', os.path.join(O1, 'again'), '기존 런 폴더')
    refused('기존 런 폴더 안 깊이 (끝난 런/BW/post/x)', os.path.join(O1, 'BW', 'post', 'x'), '기존 런 폴더')
    for m in RUN_MARKS:                       # 런 표지 하나만 있는 폴더 (시작하자마자 멈춘 런 · 옛 실행기 run_arms.sh 출력) 안도 같다 · 조상 두 단계 위여도
        dm = os.path.join(d, 'mark_' + m.replace('.', '_'))
        wtxt(os.path.join(dm, m), 'x\n')
        refused('런 표지 %s 있는 폴더 안 (두 단계 아래)' % m, os.path.join(dm, 'sub', 'new'), '기존 런 폴더')

    # G2CPR3-04 — 자리 문의 두 경계를 시험에 묶는다 (코드는 그대로 · 리뷰 변이 K11 · K12 가 이 시험을 지났다):
    # (가) 입력 글자 ↔ 실제 경로 — 런 표지는 OUT 의 실제 경로의 조상에서 찾는다 (K11 = 글자 그대로 $O 의 dirname → 상대 경로는 '.' 에서 돌고 ·
    #      없는 폴더 + .. 길은 표지를 못 본다)
    rel = os.path.join(d, 'rel_cwd')
    os.makedirs(rel)
    accepted('상대 경로 OUT (cwd = 런 밖 새 폴더 · rel_out)', 'rel_out', cwd=rel)
    refused('상대 경로 OUT (cwd = 끝난 런 · new_rel)', 'new_rel', '기존 런 폴더', cwd=O1)
    refused('없는 폴더 + .. 로 끝난 런 안 (no_such_dir/../sandbox/newrun_ok/new)',
            os.path.join(d, 'no_such_dir', '..', os.path.basename(S), os.path.basename(O1), 'new'), '기존 런 폴더')
    # (나) 형제 이름 — 기록 폴더 이름을 앞머리로 가진 샌드박스 안 새 폴더는 기록 폴더 안이 아니다 (K12 = 슬래시 없는 앞머리 → 과하게 막음)
    for sib in ('run_40000_g2cp', 'dry_run2'):
        accepted('형제 이름 %s (샌드박스 안 새 폴더)' % sib, os.path.join(S, sib))
    return t


@test
def t42_round2_notation():
    """G2CPR2-03 표기 셋 + 01 · 05 의 등록 · 사용 문서 — (가) '§3 판정 규칙은 그대로' 가 아니라 판정 식 · 허용폭 그대로 + NOT_COMPUTED 사유 더함 ·
    (나) 리뷰 권고 밖에서 더한 거부 쪽 규칙을 '같은 비준' 으로 뭉뚱그리지 않는다 · (다) 변이 3 회차 수 = 돌린 기록대로 (그 판 18 중 16) ·
    규칙 ⑪ (완료 문) 이 등록문에 있다 · 문서의 시험 함수 수 = 이 파일의 실제 수 · (G2CPR3-03) 같은 주장이 남은 세 자리 (README '하지 않는 것' ·
    메모 §0 '범위' · 메모 머리 '상태') 도 판정 식 · 허용폭 그대로 + NOT_COMPUTED 사유 ① · ⑪ · 기준 날짜."""
    t = T()
    txt = open(MEMO, encoding='utf-8').read()
    s0 = _memo_section(txt, '\n## 0. ', '\n## 1. ')
    head = s0[:s0.index('\n### 0-1. ')]
    t.ok("(가) 메모 §0 머리 — '§3 판정 규칙은 그대로' 문구 없음", '§3 판정 규칙은 그대로' not in head)
    t.ok('(가) 메모 §0 머리 — 판정 식 · 허용폭 그대로 + NOT_COMPUTED 사유 더함', '판정 식' in head and 'NOT_COMPUTED 사유' in head and '등록 덱 아님' in head,
         head[-600:])
    t.ok("(나) 메모 §0 머리 — '같은 비준' 으로 뭉뚱그리지 않음 · 권고 밖에서 더한 것을 따로 적음", '같은 비준' not in head and '권고 밖' in head)
    s03 = _memo_section(txt, '\n### 0-3. ', '\n#### 0-3-1. ')
    rule = s03[s03.index('**공통 규칙'):]
    k11 = rule.find('⑪')
    t.ok('메모 §0-3 공통 규칙 ⑪ = 완료 문 (outputs.md5 · STOP.txt · rc.txt)',
         k11 >= 0 and all(s in rule[k11:] for s in ('outputs.md5', 'STOP.txt', 'rc.txt')), rule[-400:])
    s04 = _memo_section(txt, '\n### 0-4. ', '\n### 0-5. ')
    t.ok('(다) 메모 §0-4 — 변이 3 회차 = 돌린 기록대로 (그 판 18 중 16 · 섞인 수 "3 회차 … 18 중 17 잡음" 없음)',
         '18 중 16' in s04 and '기록 중복) 18 중 17 잡음' not in s04)
    nfun = '%d 함수' % len(TESTS)
    row = next((ln for ln in s04.splitlines() if ln.startswith('| `docs/reviews/p1_g2c_sandbox_20261104/test_g2cp.py`')), '')
    t.ok('메모 §0-4 표의 시험 함수 수 = 실제 (%s)' % nfun, nfun in row, row[:200])
    t.ok('메모 §0-4 실행기 줄 — 실행 전 멈춤에 OUT 자리',
         'OUT 자리' in next((ln for ln in s04.splitlines() if ln.startswith('| `docs/reviews/p1_g2c_sandbox_20261104/run_g2cp.sh`')), ''))
    rd = open(os.path.join(HERE, 'README_g2cp.md'), encoding='utf-8').read()
    t.ok('README — 시험 함수 수 = 실제 (%s)' % nfun, nfun in rd)
    t.ok('README — 멈춘 OUT 은 대조기 판독 대상 아님', '멈춘 OUT' in rd and '완료 문' in rd)
    r3 = next((ln for ln in rd.splitlines() if ln.startswith('| 3 |')), '')
    t.ok('README — rc 3 줄에 OUT 자리 (기록 폴더 안 · 기존 런 폴더 안)', 'OUT 자리' in r3 and '기록 폴더' in r3 and '기존 런 폴더' in r3, r3[:300])
    t.ok('README — 변이 3 회차 = 돌린 기록대로 (그 판 18 중 16 · 섞인 수 "3 회차 18 중 17" 없음)', '18 중 16' in rd and '3 회차 18 중 17' not in rd)
    src = open(os.path.join(HERE, CMPFILE), encoding='utf-8').read()
    t.ok("(가) 대조기 머리글 — '판정 규칙 · 허용폭 그대로' 문구 없음", '판정 규칙 · 허용폭 그대로' not in src)
    # G2CPR3-03 — 같은 주장이 남은 세 자리 (README '하지 않는 것' · 메모 §0 '범위' · 메모 머리 '상태') = 판정 식 · 허용폭 그대로 +
    # 판정의 NOT_COMPUTED 사유 ① · ⑪ 더함 (§0-3) · 범위 · 상태 줄 = 기준 날짜 (11-10 개정 · 11-05 등록)
    def claims_fixed(s):
        return '판정 규칙' not in s and '판정 식' in s and 'NOT_COMPUTED 사유' in s and '①' in s and '⑪' in s
    nd = rd[rd.index('\n## 하지 않는 것'):] if '\n## 하지 않는 것' in rd else ''
    t.ok("(G2CPR3-03) README '하지 않는 것' — '판정 규칙' 대신 판정 식 · 허용폭 그대로 + NOT_COMPUTED 사유 ① · ⑪", nd and claims_fixed(nd), nd[-300:])
    scope = next((ln for ln in s0.splitlines() if ln.startswith('> **범위')), '')
    t.ok("(G2CPR3-03) 메모 §0 '범위' — 11-10 개정 표지 · '§3 판정 규칙' 대신 판정 식 + NOT_COMPUTED 사유 ① · ⑪",
         scope.startswith('> **범위 (11-10 개정') and claims_fixed(scope), scope[:300])
    pre = txt[:txt.index('\n## 0. ')]
    st = next((ln for ln in pre.splitlines() if ln.startswith('> **상태')), '')
    t.ok("(G2CPR3-03) 메모 머리 '상태' — 11-05 등록 때 표지 · '판정 규칙' 대신 판정 식 + NOT_COMPUTED 사유 ① · ⑪",
         st.startswith('> **상태 (11-05') and claims_fixed(st), st[:300])
    return t


# ═══ 11-11 3 회차 내부 반박 리뷰 G2CPR3-01–04 — 시험 먼저 ══════════════════════════════════════
@test
def t43_completion_gate_outputs_md5():
    """G2CPR3-01 (메모 §0-3 규칙 ⑪ 보강) — 완료 문은 OUT/outputs.md5 (실행기가 끝 단계에서 쓴 기록) 에 적힌 파일마다 md5 를 다시 계산해
    실제 파일과 대조한다: 줄 꼴 = 실행기 꼴 (`<md5 32 자리 소문자 16 진>  <이름>`) · 같은 이름 두 줄 = 모호 (규칙 ⑩) · 적힌 파일 모두 있음 ∧ md5 같음 ·
    적힌 집합 = 실제 출력 집합 (실행기와 같은 정의 — 깊이 3 의 `<폴더>/post/*` · `<폴더>/rst/*` 보통 파일 · 링크를 따라가지 않음).
    어긋나면 (끝난 뒤 덤프 · restart 잘림 · 빠짐 · 더해짐 · 손댐 · 옮기다 · 복사하다 끊김) 판정하지 않는다 — 예측 15 모두 계산 못 함 ·
    판정 NOT_COMPUTED + 기술 실패 표지 · rc 2 · 사유 = 출력 손상.  정직한 흐름 (끝난 출력을 그대로 둠 · 그대로 복사함 · 실제 실행기 출력을
    복사함) = 결과가 바뀌지 않는다.  고치기 전 = 리뷰 재현 F1 · F2 (CR 쌍 덤프 잘림) 가 완료 문을 지나 판정 라 FAIL · 라-바이트 틀림."""
    c = load_cmp()
    t = T()

    def dump(O, a, k='c'):
        return os.path.join(O, a, 'post', ('c_%d.txt' if k == 'c' else 'atom_%d.txt') % NSTEP)

    def cut_rows(p, k):
        L = open(p).read().splitlines()
        wtxt(p, '\n'.join(L[:-k]) + '\n')

    def cut_bytes(p, frac):
        b = open(p, 'rb').read()
        with open(p, 'wb') as f:
            f.write(b[:int(len(b) * frac)])

    def flip_digit(p):                       # 같은 크기 · 마지막 숫자 한 글자만 바꿈 (손댐)
        b = bytearray(open(p, 'rb').read())
        i = max(k for k in range(len(b)) if 48 <= b[k] <= 57)
        b[i] = 48 if b[i] != 48 else 49
        with open(p, 'wb') as f:
            f.write(bytes(b))

    def edit_outputs(O, fn, tail='\n'):
        p = os.path.join(O, 'outputs.md5')
        L = fn(open(p).read().splitlines())
        with open(p, 'w') as f:
            f.write(''.join(x + '\n' for x in L[:-1]) + (L[-1] + tail if L else ''))

    def append_bytes(p, b):
        with open(p, 'ab') as f:
            f.write(b)

    def to_symlink(O):                       # 같은 내용 파일 (OUT 밖) 로 가는 링크 — 실행기 출력에는 링크가 없다
        p = dump(O, 'CR')
        q = os.path.join(os.path.dirname(O), 'elsewhere_' + os.path.basename(p))
        shutil.copy2(p, q)
        os.remove(p)
        os.symlink(q, p)

    def blocked(name, O, must):
        r, rc = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
        bad = [(k, status_of(r, k)) for k in ALL15 if status_of(r, k) != '계산 못 함']
        t.ok(name + ' → 예측 15 모두 계산 못 함', not bad, bad[:4])
        J = r.get('judgment', {})
        t.ok(name + ' → 판정 NOT_COMPUTED + 기술 실패 표지', [J.get(x, {}).get('status') for x in ('다', '라')] == ['NOT_COMPUTED'] * 2
             and all(J.get(x, {}).get('technical_failure') is True for x in ('다', '라')), J)
        t.ok(name + ' → 판정 사유 · 표지 = 출력 손상 (끝나지 않음과 가름)',
             all('출력 손상' in ' '.join(J.get(x, {}).get('why', [])) and '출력 손상' in str(J.get(x, {}).get('note', '')) for x in ('다', '라')),
             [((J.get(x, {}).get('why') or [''])[0][:100], J.get(x, {}).get('note')) for x in ('다', '라')])
        t.ok(name + ' → rc 2', rc == 2, rc)
        g = r.get('run_gate') or {}
        why = ' '.join(g.get('why', []))
        t.ok(name + ' → 완료 문 막힘 (outputs.md5 ↔ 실제 출력 · %s)' % ' · '.join(must),
             g.get('ok') is False and 'outputs.md5' in why and '출력 손상' in why and all(m in why for m in must), g.get('why'))
        return r

    N = NSTEP
    cases = (
        ('F1 CR 쌍 덤프 끝 5 행 잘림 (줄 경계 · 리뷰 재현)', lambda O: cut_rows(dump(O, 'CR'), 5), ('md5 다름', 'CR/post/c_%d.txt' % N)),
        ('F2 CR 쌍 덤프 바이트 0.9 에서 잘림 (줄 가운데 · 리뷰 재현)', lambda O: cut_bytes(dump(O, 'CR'), 0.9), ('md5 다름',)),
        ('F3 CR 쌍 덤프 0 바이트', lambda O: cut_bytes(dump(O, 'CR'), 0.0), ('md5 다름',)),
        ('F4 CR 원자 덤프 끝 3 행 잘림', lambda O: cut_rows(dump(O, 'CR', 'atom'), 3), ('md5 다름', 'CR/post/atom_%d.txt' % N)),
        ('F5 BR 쌍 덤프 빠짐 (옮기다 끊김)', lambda O: os.remove(dump(O, 'BR')), ('적혔는데 없음', 'BR/post/c_%d.txt' % N)),
        ('F6 A2 명령 restart 파일 반쯤 잘림', lambda O: cut_bytes(os.path.join(O, 'A2', 'rst', 'restart_cmd.bin'), 0.5),
         ('md5 다름', 'A2/rst/restart_cmd.bin')),
        ('F7 CR 쌍 덤프 숫자 한 글자 바뀜 (같은 크기 · 손댐)', lambda O: flip_digit(dump(O, 'CR')), ('md5 다름',)),
        ('F8 적히지 않은 파일 더함 (A/post/extra.txt)', lambda O: wtxt(os.path.join(O, 'A', 'post', 'extra.txt'), 'x\n'),
         ('적히지 않음', 'A/post/extra.txt')),
        ('F9 outputs.md5 끝 줄 빠짐 (기록 잘림 · 줄 경계)', lambda O: edit_outputs(O, lambda L: L[:-1]), ('적히지 않음',)),
        ('F10 outputs.md5 끝 줄 md5 가운데 잘림 (줄 끝 없음)', lambda O: edit_outputs(O, lambda L: L[:-1] + [L[-1][:20]], tail=''), ('꼴 밖 줄',)),
        ('F11 outputs.md5 = 빈 파일 (실행기가 끝 단계에서 쓰는 중)', lambda O: wtxt(os.path.join(O, 'outputs.md5'), ''), ('적히지 않음',)),
        ('F12 outputs.md5 에 꼴 밖 줄 하나 더함 (나머지 다 맞음)', lambda O: edit_outputs(O, lambda L: L + ['손으로 적은 줄']), ('꼴 밖 줄',)),
        ('F13 outputs.md5 같은 이름 두 줄 (앞 = 틀린 md5 · 뒤 = 맞는 md5)',
         lambda O: edit_outputs(O, lambda L: ['0' * 32 + '  ' + L[-1].split('  ', 1)[1]] + L), ('같은 이름',)),
        ('F14 CR 쌍 덤프 = 같은 내용 파일로 가는 심볼릭 링크', to_symlink, ('적혔는데 없음', 'CR/post/c_%d.txt' % N)),
        ('F15 outputs.md5 비UTF-8 바이트 (옮기다 깨짐)', lambda O: append_bytes(os.path.join(O, 'outputs.md5'), b'\xff\xfe\n'), ('읽기 문제',)),
    )
    for name, fn, must in cases:
        d = tmpdir()
        O = _full(d)
        fn(O)
        blocked(name, O, must)
        if name.startswith('F1 '):
            jp = os.path.join(O, 'compare_g2cp.json')
            t.ok('F1 → JSON 에도 완료 문 막힘 (JSON 만 봐도 가른다)', os.path.exists(jp) and (json.load(open(jp)).get('run_gate') or {}).get('ok') is False)
            p = subprocess.run([sys.executable, '-I', os.path.join(HERE, CMPFILE), O, str(NSTEP)], capture_output=True, text=True, timeout=300)
            gl = [ln for ln in p.stdout.splitlines() if ln.startswith('완료 문 ')]
            t.ok('F1 → 대조기 CLI rc 2 · 화면에 완료 문 막힘 줄 하나 (끝난 그대로가 아님 · outputs.md5)',
                 p.returncode == 2 and len(gl) == 1 and gl[0].startswith('완료 문 막힘 — 실행기 출력이 끝난 그대로가 아니다') and 'outputs.md5' in gl[0],
                 (p.returncode, gl, p.stdout[-300:]))

    # 정직한 흐름 — 끝난 출력을 그대로 둠 · 그대로 복사함 (내용만 · 시각 바뀜 · 원 OUT 의 compare_g2cp.json 도 함께) = 결과가 같다
    def sig(r, rc):
        J = r.get('judgment', {})
        return ([status_of(r, k) for k in ALL15], [(J.get(x, {}).get('status'), J.get(x, {}).get('n_mismatch'), J.get(x, {}).get('n_bit_equal'))
                                                    for x in ('다', '라')], rc)
    d = tmpdir()
    O = _full(d)
    r0, rc0 = c.compare_all(O, NSTEP, here=HERE, ref=REF40)
    g0 = r0.get('run_gate') or {}
    t.ok('P0 손대지 않음 → 완료 문 지남 · 판독 (다-값 맞음 · 판정 PASS · rc 0)',
         g0.get('ok') is True and status_of(r0, '다-값') == '맞음' and r0['judgment']['라']['status'] == 'PASS' and rc0 == 0, (g0, rc0))
    og = g0.get('outputs') or {}
    t.ok('P0 → 적힌 파일 모두 md5 대조 (적힌 수 = 실제 수 = md5 같은 수 > 0)',
         og.get('n_listed', 0) > 0 and og.get('n_listed') == og.get('n_actual') == og.get('n_md5_equal'), og)
    O2 = os.path.join(d, 'copied')
    shutil.copytree(O, O2, copy_function=shutil.copy)
    r1, rc1 = c.compare_all(O2, NSTEP, here=HERE, ref=REF40)
    t.ok('P1 그대로 복사 (copytree · 시각 바뀜) → 결과 같음 (예측 15 · 판정 · rc)', sig(r1, rc1) == sig(r0, rc0), (sig(r1, rc1), sig(r0, rc0)))
    t.ok('P1 → 완료 문 지남', (r1.get('run_gate') or {}).get('ok') is True, r1.get('run_gate'))

    # 실제 실행기 (가짜 lmp) 출력 — 실행기가 쓴 outputs.md5 (find · sort · md5sum 꼴) 를 그대로 대조 · 복사한 곳도 같음
    d = tmpdir()
    S = sandbox_copy(d)
    env = fake_env(d)
    O = os.path.join(d, 'O')
    rc, out, err = run_runner(S, [str(NSTEP), O], env)
    t.ok('P2 실행기 (가짜 lmp) rc 0', rc == 0, (rc, err[-300:]))
    O2 = os.path.join(d, 'O_moved')
    shutil.copytree(O, O2, copy_function=shutil.copy)
    js = []
    for X in (O, O2):
        p = subprocess.run([sys.executable, '-I', os.path.join(S, CMPFILE), X, str(NSTEP)], capture_output=True, text=True, timeout=300)
        gl = [ln for ln in p.stdout.splitlines() if ln.startswith('완료 문 ')]
        t.ok('P2 %s → 대조기 CLI rc 0 · 완료 문 지남' % ('원래 OUT' if X == O else '복사한 OUT'), p.returncode == 0 and gl == ['완료 문 지남'],
             (p.returncode, gl, p.stdout[-300:], p.stderr[-300:]))
        jp = os.path.join(X, 'compare_g2cp.json')
        js.append(json.load(open(jp)) if os.path.exists(jp) else {})
    og = (js[1].get('run_gate') or {}).get('outputs') or {}
    t.ok('P2 복사한 OUT → 실행기 기록의 파일 모두 md5 대조 (적힌 수 = 실제 수 = md5 같은 수 > 0)',
         og.get('n_listed', 0) > 0 and og.get('n_listed') == og.get('n_actual') == og.get('n_md5_equal'), og)
    t.ok('P2 → 원래 · 복사한 OUT 예측 15 같음 (다-값 맞음)',
         [status_of(js[1], k) for k in ALL15] == [status_of(js[0], k) for k in ALL15] and status_of(js[1], '다-값') == '맞음',
         [[status_of(jj, k) for k in ('다-값', '바')] for jj in js])
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
    if len(sys.argv) > 1 and sys.argv[1] == '--sigdriver':     # t31 이름공간 안 드라이버 (시험을 돌리지 않는다)
        sys.exit(_sig_driver(sys.argv[2:]))
    sys.exit(main())
