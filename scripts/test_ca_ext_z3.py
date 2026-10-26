#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② Z3 — 사슬이 실제 런을 돌 수 있게 (시험 먼저 · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §3 (S1 face_alpha · α 는 `couple()` 에서 융합 면에 먼저) ·
§4 (S2 탄소 접합 · P0/P1 = PTFE–접합 끝 법칙 · J6 극한 · J11 단락) · §6 (수렴 증서) · §7 (세대 · 영수증) · 등록 R 초안
`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3-1 (바닥 R_j → ∞ · 천장 R_j → 0 = 정확한 축약) · §3-3 · §4-2
(origin arm 1 · 2) · §10 (명령 꼴 `PTFE_STAMP=face_alpha` + 접합 + P0/P1).

  python3 scripts/test_ca_ext_z3.py                       # 전부 (payload · 러너 끝-끝 포함)
  python3 scripts/test_ca_ext_z3.py --only A,B            # 이름 접두로 고르기
  python3 scripts/test_ca_ext_z3.py --skip-payload        # payload · 러너 끝-끝 빼고 (솔브 · 기록 수준만)
  python3 scripts/test_ca_ext_z3.py --old-scripts DIR     # O — 끈 경로 비트 대조 (DIR = 기반 커밋 scripts/ 사본)

묶음:
  A  face_alpha (S1) + 탄소 접합 (S2) 한 런 (+ P1) — 솔브 수준 (직접 풀이 · 생산 단위 vox 0.15 · r_f 0.075 · rope 0.124):
     (i) PTFE 0 → 조합 = 접합만 비트 같음 (ii) 접합 끔 = face_alpha 만 (O 묶음이 기반 코드와 대조) (iii) α 는 융합 면에 먼저 ·
     α = 0 면 제거 · 면별 배열 압축 일관 · 접합이 끊은 면에 α 없음 (iv) PTFE 캡슐이 접합 끝을 덮음: P0 = 간선 그대로 · P1 = 절단 ·
     α 는 접합 간선에 안 걸림 (v) Rayleigh — PTFE 늘리면 σ 증가 없음 · σ(P1) ≤ σ(P0) (vi) 순열 · 원점 이동 불변
     (vii) 원장 · 소산 항등식 · payload 끝-끝 (ca_ext 두 하위 블록 · p3ca- · ca_ext_record_ok) · 러너 · 계약 함수
  B  극한 런 — 손계산 (두 섬유 + 접합 하나 + 우회 섬유: 바닥 = 접합 없는 회로 · 천장 = 접합 양 끝을 한 노드로) · 기록 꼴
     (`R_j_ohm` null + `rj_limit` 'inf' · `R_j_ohm` 0.0 + 'zero' · `quantitative` False · `allow_rj_limits` True) · 러너 env
     (`CJUNC_RJ=inf` · `0`) · 영수증 · payload · 검증기 (바닥 n_none_inf · 천장 축약 S3 없이) · 바닥 + c 1 NaN 없음
  C  러너 `ARM_LIST` (예 `1,2`) — 팔 이름 · OUTDIR · 영수증 (arm_list) · 봉인 없음 (진단) · 중복 · 범위 밖 · ARMS 동시 = 거부 ·
     팔 origin ↔ 영수증 arm_list 대조
  D  off 격자 sid 지문 `ca_ext.ptfe_face.evidence.fp.sid_off` — 같은 킷 같은 래스터 = 같다 · 조합 런 = 접합 원장 sid 지문과 같다 ·
     검증기 (없음 · 모양 · 조합 불일치 = 거부)
  E  CG 반복 수 기록 — 수렴했을 때도 (주 · 보조 · ⓒ 이어 풀기) · 증서 켤 때만 (끔 = 옛 키 그대로) · 독립 셈과 같음
  O  (--old-scripts) 끈 경로 비트 대조 — 새 노브 끔 = 기반 코드와 매니페스트 (code_sha · exec_env 빼고) · step3 값 같음 ·
     face_alpha 만 (접합 끔) 솔브 비트 같음.  ★ 10-21 (D · 브리프 묶음 5): payload 대조는 b6 의 한 표 (`OLD_DIFF_ALLOW` · 켠 노브의
     새 칸만 · 끈 경우 차이 0) · `--expect-identical` (기반 = 바로 앞 커밋) = 차이 0 · 기반 사본 옆에 docs/ 링크 · ★ 10-25 묶음 B (결정 11)
     SV 켬 꼴 셋 (b6 B 와 같은 꼴 · 경우 표지 sv_cf · 허용 행 세대 RR)
⚠ PASS 는 배선 · 계약 · 구현의 증거이지 R_j 값 · 판정 (R) 의 물리 검증이 아니다.
"""
import argparse
import contextlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

S3 = CJ = FA = CW = RC = None
ARGS = None
_ok, _fail = 0, []
CASES = []
TD = None


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:600]})' if why != '' else ''))
    return cond


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def raises(fn, exc=(ValueError, TypeError)):
    try:
        quiet(fn)
    except exc:
        return True
    except Exception:                                      # noqa: BLE001 — 다른 예외 = 거부 계약 위반
        return False
    return False


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


_CG = [0]


@contextlib.contextmanager
def direct_solver():
    """작은 픽스처 = 직접 풀이 (기계 정밀도) — 조립 · 항등식을 CG 허용오차 없이 본다.  생산 경로 아님."""
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg

    def _direct(L, b, *a, **k):
        _CG[0] += 1
        return spsolve(L.tocsc(), b), 0
    S3._solve_cg = _direct
    try:
        yield
    finally:
        S3._solve_cg = old


# ═════════════════════════ 생산 단위 픽스처 (vox 0.15 · r_f 0.075 · rope 0.124) ═════════════════════════
H = 0.15
RF = 0.075
TOL = 0.05
LPAR = 0.30
RPORT = 0.30
SMIN = 0.6
SIG_V = 7853.98
G_AX = SIG_V * H                         # 축방향 면 g (코드 단위 S/cm·µm) = σ·h
G_PL = SIG_V * H * H / (0.5 * H)         # 판 결합 g (셀 중심이 판에서 h/2) = 2σh


def sig_e():
    return S3.electronic_sigma_table(0.0041, 0.0041, SIG_V, 10.0, 256.6)


def densify(verts, step=H / 3.0):
    V = np.asarray(verts, np.float64)
    out = [V[0]]
    for a, b in zip(V[:-1], V[1:]):
        n = max(1, int(math.ceil(np.linalg.norm(b - a) / step - 1e-12)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * (i / n))
    return np.asarray(out)


def block(polys, phase, kind, fids, step=H / 3.0):
    P, PH, F, K = [], [], [], []
    for v, f in zip(polys, fids):
        pts = densify(v, step) if len(v) > 1 else np.asarray(v, np.float64)
        P.append(pts); PH.append(np.full(len(pts), phase)); F.append(np.full(len(pts), f)); K.append(np.full(len(pts), kind))
    return (np.vstack(P), np.concatenate(PH).astype(np.int64), np.concatenate(F).astype(np.int64),
            np.concatenate(K).astype(np.int64))


def cat(*rs):
    rs = [r for r in rs if r is not None and len(r[0])]
    return tuple(np.concatenate([r[i] for r in rs]) for i in range(4))


def c(ix, iy, iz, sh=(0.0, 0.0, 0.0)):
    """셀 (ix, iy, iz) 의 중심 (µm) — 상자 원점 sh (원점 이동 시험)."""
    return (sh[0] + (ix + 0.5) * H, sh[1] + (iy + 0.5) * H, sh[2] + (iz + 0.5) * H)


# ── FC: 한 기둥 위 두 섬유 A (z 0..7) · B (z 8..15) 가 끝–끝으로 닿는다 (접합 instance 하나 · 면 (2,2,7)|(2,2,8) 절단 자리) +
#    옆 기둥 SDCP (3,2,0..15 · 병렬 경로 = SV 융합 면) + PTFE 캡슐 셋:
#      cap1 = y 방향 · x = 3h (VGCF|SDCP 면의 평면) · z = 4.5h → 층 4 면 α = 0 (절단) · 층 3 · 5 면 0 < α < 1
#      cap3 = cap1 과 같은 꼴 · z = 11.5h (층 11 α = 0 · 10 · 12 부분)
#      cap2 = x 방향 · y = 2.5h + 0.20 · z = 8h (접합 최근접점에서 0.20 µm ≤ r_P + r_f + tol_P = 0.249 → 덮임) · 어떤 자격 면도 안 가린다
FC_N = (6, 6, 16)


def fc_caps(names, sh=(0.0, 0.0, 0.0)):
    out = []
    for nm in names:
        if nm == 'cap1':
            out.append([(sh[0] + 3 * H, sh[1] + 0.25 * H, sh[2] + 4.5 * H), (sh[0] + 3 * H, sh[1] + 5.75 * H, sh[2] + 4.5 * H)])
        elif nm == 'cap3':
            out.append([(sh[0] + 3 * H, sh[1] + 0.25 * H, sh[2] + 11.5 * H), (sh[0] + 3 * H, sh[1] + 5.75 * H, sh[2] + 11.5 * H)])
        elif nm == 'cap2':
            y = 2.5 * H + 0.20
            out.append([(sh[0] + 0.25 * H, sh[1] + y, sh[2] + 8.0 * H), (sh[0] + 5.75 * H, sh[1] + y, sh[2] + 8.0 * H)])
        else:
            raise KeyError(nm)
    return out


def fc_rows(caps=(), sh=(0.0, 0.0, 0.0), swap=False, rev_ptfe=False, sdcp=True):
    A = [c(2, 2, 0, sh), c(2, 2, 7, sh)]
    B = [c(2, 2, 8, sh), c(2, 2, 15, sh)]
    fibres = [A, B] if not swap else [B, A]
    fids = [10, 20] if not swap else [20, 10]
    v = block(fibres, 2, 1, fids)
    s = block([[c(3, 2, k, sh)] for k in range(16)], 5, 0, [-1] * 16) if sdcp else None
    polys = fc_caps(caps, sh)
    if rev_ptfe:
        polys = polys[::-1]
    p = block(polys, 4, 1, [900 + i for i in range(len(polys))]) if polys else None
    return cat(v, s, p)


def bed(addr, n, lo=(0.0, 0.0, 0.0), vox=H):
    P, PH, F, K = addr
    m = PH != 4                                             # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    lo = tuple(float(x) for x in lo)
    hi = tuple(lo[i] + n[i] * vox for i in range(3))
    sid, pid = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P[m], PH[m], lo, hi, vox,
                            add_fid=F[m], add_kind=K[m])
    return sid, pid


def registry(sid, addr, lo=(0.0, 0.0, 0.0), vox=H, **kw):
    P, PH, F, K = addr
    k = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, s_min_um=SMIN, gap_tol=2.0)
    k.update(kw)
    return quiet(CJ.cjunc_registry, sid, tuple(float(x) for x in lo), vox, P, PH, F, K, **k)


def fa_plan(sid, pid, addr, lo=(0.0, 0.0, 0.0), vox=H, sig=None):
    P, PH, F, K = addr
    m4 = PH == 4
    caps = FA.build_capsules(P[m4], F[m4], K[m4], dia_law='rope')
    return FA.build_plan(sid, sig if sig is not None else sig_e(), caps, lo=lo, vox=vox, channel='electronic', pid=pid)


def solve(sid, n, cj=None, fa=None, pid=None, vox=H, sig=None):
    kw = {}
    if cj is not None:
        kw['cjunc'] = cj
    if fa is not None:
        kw['face_alpha'] = fa
        kw['pid'] = pid
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig if sig is not None else sig_e(), vox, z_top_um=float(n[2]) * vox,
                     z_bot_um=0.0, **kw)


def I_of(res, n, vox=H):
    zb, zt = res['plate_z_um']
    return res['sigma_eff'] * (n[0] * n[1] * vox * vox) / (zt - zb)


def chain_I(gs):
    return 1.0 / sum(1.0 / g for g in gs)


def fc_case(caps=(), law='P0', rj=1.0e6, combo=True, sh=(0.0, 0.0, 0.0), swap=False, rev_ptfe=False, cj_on=True):
    """FC 침대 하나 → (해, 원장, 접합 계획, face_alpha 계획, sid, pid)."""
    addr = fc_rows(caps, sh=sh, swap=swap, rev_ptfe=rev_ptfe)
    sid, pid = bed(addr, FC_N, lo=sh)
    reg = registry(sid, addr, lo=sh)
    cjp = CJ.cjunc_plan(reg, rj, unreg_law='cut', ptfe_stamp='face_alpha', ptfe_jlaw=law) if cj_on else None
    fap = fa_plan(sid, pid, addr, lo=sh) if combo else None
    res = solve(sid, FC_N, cj=cjp, fa=fap, pid=pid)
    return res, reg, cjp, fap, sid, pid


def _canon_record(d):
    return json.dumps(d, sort_keys=True, default=lambda o: (o.tolist() if hasattr(o, 'tolist') else repr(o)))


# ═════════════════════════ A — face_alpha + 접합 한 런 (+ P1) ═════════════════════════
@case('A face_alpha (S1) + 탄소 접합 (S2) 한 솔브 (+ P1) — 솔브 수준')
def t_A():
    #  ── (i) PTFE 0 → 조합 = 접합만 (같은 침대 · 같은 R_j · 비트) ──
    try:
        r_cj, reg0, cj0, _f, sid0, pid0 = fc_case((), combo=False)
        r_co, _r, _c, fa0, _s, _p = fc_case((), combo=True)
        same = (r_co['sigma_eff'] == r_cj['sigma_eff'] and r_co['n_dof'] == r_cj['n_dof']
                and _canon_record({k: v for k, v in r_co['cjunc'].items()}) == _canon_record(r_cj['cjunc']))
        chk('A1 (i) PTFE 0 → face_alpha + 접합 = 접합만 (σ · n_dof · 접합 기록 비트 같음 · α 행 0)',
            same and fa0['n_rows'] == 0 and r_co['face_alpha']['n_rows_used'] == 0 and r_cj['sigma_eff'] > 0,
            (r_co.get('sigma_eff'), r_cj.get('sigma_eff')))
    except Exception as e:                                  # noqa: BLE001 — 옛 코드 = 조합 거부 (시험 단위 실패)
        chk('A1 (i) PTFE 0 → face_alpha + 접합 = 접합만', False, f'{type(e).__name__}: {e}')
    #  ── (iii) α 는 couple() 에서 먼저 · α = 0 면 제거 · 면별 배열 압축 일관 · 접합이 끊은 면에 α 없음 ──
    seen = []
    real = CJ.CjuncAssembler.add_faces

    def spy(self, axis, a2, b2, g):
        seen.append((int(axis), self.cells_lin[np.asarray(a2, np.int64)].copy(), self.cells_lin[np.asarray(b2, np.int64)].copy(),
                     np.asarray(g, np.float64).copy(), len(a2), len(b2), len(g)))
        return real(self, axis, a2, b2, g)
    CJ.CjuncAssembler.add_faces = spy
    try:
        try:
            r1, reg1, cj1, fa1, sid1, pid1 = fc_case(('cap1', 'cap3'))
            err = None
        except Exception as e:                              # noqa: BLE001
            err = e
    finally:
        CJ.CjuncAssembler.add_faces = real
    if err is not None:
        chk('A2 (iii) 조합 솔브가 돈다 (α 계획 + 접합 계획)', False, f'{type(err).__name__}: {err}')
    else:
        sig = sig_e()
        sf = S3.sigma_field(sig, sid1).reshape(-1)
        shp = sid1.shape
        stride = (shp[1] * shp[2], shp[2], 1)
        alpha = {}
        for ax, a in enumerate(fa1['axes']):
            for ln, al in zip(np.asarray(a['lin']).tolist(), np.asarray(a['alpha']).tolist()):
                alpha[(ax, int(ln))] = float(al)
        n_cut_plan = sum(1 for v in alpha.values() if v == 0.0)
        lens_ok = all(x[4] == x[5] == x[6] for x in seen)
        bad_g, dropped_seen, n_alpha_hit = [], [], 0
        got = set()
        for ax, la, lb, g, *_n in seen:
            for i in range(len(la)):
                key = (ax, int(la[i]))
                got.add(key)
                if int(lb[i]) != int(la[i]) + stride[ax]:
                    bad_g.append(('not-lower', key))
                    continue
                sa, sb = sf[la[i]], sf[lb[i]]
                g0 = (2.0 * sa * sb / (sa + sb)) * H
                al = alpha.get(key, 1.0)
                if al == 0.0:
                    dropped_seen.append(key)
                if al < 1.0:
                    n_alpha_hit += 1
                if g[i] != g0 * al:
                    bad_g.append((key, g[i], g0, al))
        want = set()
        cond = sf > 0
        for ax in range(3):
            for ln in np.flatnonzero(cond).tolist():
                ijk = np.unravel_index(ln, shp)
                if ijk[ax] >= shp[ax] - 1:
                    continue
                up = ln + stride[ax]
                if cond[up] and alpha.get((ax, ln), 1.0) != 0.0:
                    want.add((ax, ln))
        chk('A2 (iii) 조립기가 받는 면 = 이 채널의 도체 면 전부 − α = 0 면 (α 0 면은 행렬에서 빠진다 · 다른 면은 안 빠진다)',
            got == want and not dropped_seen and n_cut_plan >= 2, (len(got), len(want), len(got ^ want), dropped_seen[:3], n_cut_plan))
        chk('A3 (iii) 면별 배열 압축 일관 — a2 · b2 · g 길이 같음 · g = α·g0 (계획 행) · g = g0 (그 밖) · 정확히 (같은 연산)',
            lens_ok and not bad_g and n_alpha_hit >= 4, (lens_ok, bad_g[:3], n_alpha_hit))
        ft = reg1['faces']
        cut_keys = {(int(a), int(l)) for l, a, k in zip(ft['lin'].tolist(), ft['ax'].tolist(), ft['kind'].tolist())
                    if k in (CJ.K_CUT_SITE, CJ.K_CUT_SELF, CJ.K_UNREG)}
        used = r1.get('_face_alpha', {}).get('axes') or ()
        used_keys = {(ax, int(l)) for ax, u in enumerate(used) for l in np.asarray(u.get('lin', ())).tolist()}
        chk('A4 (iii) 접합이 끊은 면 (자리 · 자기 · 미등록) 에 α 가 남지 않는다 — face_alpha 가 쓴 행 ∩ 접합 tombstone = ∅ (VV 면 = 같은 탄소 면제)',
            cut_keys and used_keys and not (cut_keys & used_keys) and not (cut_keys & set(alpha)),
            (len(cut_keys), len(used_keys), sorted(cut_keys & used_keys)[:3]))
        chk('A5 (iii) 조합 해의 기록 — face_alpha (n_rows_used = 계획 행 중 행렬에 든 것 · 절단 수) · 접합 (풀림 · 간선 1)',
            r1['face_alpha']['n_rows_used'] == fa1['n_rows'] and r1['face_alpha']['n_cut_used'] == n_cut_plan
            and r1['cjunc']['solved'] is True and r1['cjunc']['n_junction_edges'] == 1 and r1['sigma_eff'] > 0,
            (r1.get('face_alpha'), {k: r1.get('cjunc', {}).get(k) for k in ('solved', 'n_junction_edges')}))
    #  ── (iv) PTFE 캡슐이 접합 끝을 덮는다 — P0 = 간선 그대로 · P1 = 절단 · α 는 접합 간선에 안 걸림 ──
    try:
        rp0, regp, cjp0, fap, sidp, pidp = fc_case(('cap2',), law='P0')
        rp1, _r, cjp1, _f, _s, _p = fc_case(('cap2',), law='P1')
        rc0, _r2, cjc0, _f2, _s2, _p2 = fc_case(('cap2',), law='P0', combo=False)
        cov = regp['instances']['ptfe_cov']
        sysd = rp0['_cjunc']['sys']
        jmask = sysd['CAT'] == CJ._CAT['vv_junction']
        e = np.flatnonzero(cjp0['mode'] == CJ.MODE_EDGE)
        jG = np.sort(sysd['G'][jmask])
        jG_cj = np.sort(rc0['_cjunc']['sys']['G'][rc0['_cjunc']['sys']['CAT'] == CJ._CAT['vv_junction']])
        chk('A6 (iv) cap2 가 접합 끝을 덮는다 (최근접점 ↔ PTFE 중심선 0.20 µm ≤ r_P + r_f + tol_P) · α 행은 0 (어떤 자격 면도 안 가린다)',
            len(cov) == 1 and bool(cov[0]) and fap['n_rows'] == 0, (cov, fap['n_rows']))
        chk('A7 (iv) P0 — 덮인 접합 간선 그대로 · g = 1e4·m/R_j (계획 값 정확히 · α 곱 없음) = 접합만 해의 간선',
            len(e) == 1 and np.array_equal(jG, np.sort(cjp0['g_code'][e])) and np.array_equal(jG, jG_cj)
            and rp0['cjunc']['n_cut_p1'] == 0, (jG, cjp0['g_code'][e], jG_cj))
        chk('A8 (iv) P1 — 덮인 접합 = 절단 (간선 없음 · 절단 1) · σ(P1) < σ(P0) (SDCP 우회로 유한)',
            rp1['cjunc']['n_cut_p1'] == 1 and rp1['cjunc']['n_junction_edges'] == 0 and 0 < rp1['sigma_eff'] < rp0['sigma_eff'],
            (rp1['cjunc'].get('n_cut_p1'), rp1['sigma_eff'], rp0['sigma_eff']))
    except Exception as e:                                  # noqa: BLE001
        chk('A6–A8 (iv) P0 / P1 조합 솔브', False, f'{type(e).__name__}: {e}')
    #  ── (v) Rayleigh — PTFE 늘리면 σ 증가 없음 · σ(P1) ≤ σ(P0) (같은 그래프 · 같은 R_j) ──
    try:
        sets = [(), ('cap1',), ('cap1', 'cap3'), ('cap1', 'cap3', 'cap2')]
        sg = {law: [fc_case(s, law=law)[0]['sigma_eff'] for s in sets] for law in ('P0', 'P1')}
        mono = all(sg[law][i + 1] <= sg[law][i] * (1 + 1e-12) for law in sg for i in range(len(sets) - 1))
        p1le = all(sg['P1'][i] <= sg['P0'][i] * (1 + 1e-12) for i in range(len(sets)))
        strict = sg['P0'][1] < sg['P0'][0] and sg['P1'][3] < sg['P0'][3]
        chk('A9 (v) Rayleigh — 캡슐 집합 ∅ ⊂ {1} ⊂ {1,3} ⊂ {1,3,2} 마다 σ 비증가 (P0 · P1) · σ(P1) ≤ σ(P0) · α 와 P1 이 실제로 깎는다',
            mono and p1le and strict, sg)
    except Exception as e:                                  # noqa: BLE001
        chk('A9 (v) Rayleigh', False, f'{type(e).__name__}: {e}')
    #  ── (vi) 순열 · 원점 이동 불변 ──
    try:
        base = fc_case(('cap1', 'cap3', 'cap2'), law='P1')
        perm = fc_case(('cap1', 'cap3', 'cap2'), law='P1', swap=True, rev_ptfe=True)
        sh = (0.37, -0.21, 0.5)
        shf = fc_case(('cap1', 'cap3', 'cap2'), law='P1', sh=sh)
        ok = True
        why = []
        for nm, r in (('순열', perm), ('원점', shf)):
            s_ok = np.array_equal(r[4], base[4])
            v_ok = rel(r[0]['sigma_eff'], base[0]['sigma_eff']) <= 1e-12
            n_ok = r[0]['n_dof'] == base[0]['n_dof'] and r[0]['cjunc']['n_cut_p1'] == base[0]['cjunc']['n_cut_p1'] \
                and r[0]['face_alpha']['n_rows_used'] == base[0]['face_alpha']['n_rows_used']
            ok = ok and s_ok and v_ok and n_ok
            why.append((nm, s_ok, r[0]['sigma_eff'], base[0]['sigma_eff'], n_ok))
        chk('A10 (vi) 섬유 순서 · fid · PTFE 경로 순서 바꿈 · 원점 이동 (0.37, −0.21, 0.5 µm) → sid · σ (1e-12) · 수 같음', ok, why)
    except Exception as e:                                  # noqa: BLE001
        chk('A10 (vi) 순열 · 원점 이동 불변', False, f'{type(e).__name__}: {e}')
    #  ── (vii) 원장 · 소산 항등식 (조합 해 · 직접 풀이) ──
    try:
        r = fc_case(('cap1', 'cap3'), law='P0')[0]
        cj = r['cjunc']
        I = I_of(r, FC_N)
        sh_ = cj['dissipation_share']
        chk('A11 (vii) 조합 해 — Σ P (면 + 접합 + 판) = I·ΔV (1e-10) · 소산 몫 합 = 1 (1e-12) · I_bot 기록 = I',
            rel(cj['P_total_code'], I) < 1e-10 and abs(sum(sh_.values()) - 1.0) < 1e-12 and rel(cj['I_bot_code'], I) < 1e-12,
            (cj['P_total_code'], I, sum(sh_.values())))
    except Exception as e:                                  # noqa: BLE001
        chk('A11 (vii) 원장 · 소산 항등식', False, f'{type(e).__name__}: {e}')
    #  ── 계약 함수 (payload 없이) — 조합 · P1 = face_alpha 에서만 · centerline + P1 거부 그대로 ──
    #  ★ 10-21 (사전 리뷰 PRE-impl-03 · 1저자 Q-C) — 접합 + centerline = P0 도 거부 (centerline 이 접점 셀을 sid 7 로 덮으면 옛 판은 포트를
    #    옆 셀로 옮겨 절연체를 더해 σ 가 올랐다 · Rayleigh 위반) — 접합은 off · face_alpha 에서만
    req = {'R_j_ohm': 1e6, 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.5, 'tol_ff_um': 0.5}
    okp = []
    for ps, law, want_ok in (('face_alpha', 'P0', True), ('face_alpha', 'P1', True), ('off', 'P1', False),
                             ('centerline', 'P1', False), ('off', 'P0', True), ('centerline', 'P0', False)):
        try:
            CW.cjunc_protocol_record(ptfe_stamp=ps, ptfe_jlaw=law, **req)
            got_ok = True
        except (ValueError, TypeError):
            got_ok = False
        okp.append((ps, law, got_ok == want_ok))
    chk('A12 cjunc_protocol_record — face_alpha + 접합 (P0 · P1) 받음 · off · centerline + P1 = 거부 · off + P0 받음 · '
        'centerline + P0 = 거부 (★ 10-21 Q-C)',
        all(x[2] for x in okp), okp)
    rq = {'cjunc': dict(req, ptfe_jlaw='P1')}
    try:
        p_fa = RC.ca_ext_request_problem(rq, ptfe_stamp='face_alpha')
    except TypeError as e:
        p_fa = f'TypeError: {e}'
    chk('A13 ca_ext_request_problem — P1 요청 = face_alpha 에서 통과 · 기본 (off) 은 거부 그대로',
        p_fa is None and RC.ca_ext_request_problem(rq) is not None, p_fa)
    env = {'CJUNC': '1', 'CJUNC_RJ': '1e6', 'CJUNC_LEN_LAW': 'len_scaled_v0', 'CJUNC_UNREG_LAW': 'cut', 'CJUNC_S_MIN_UM': '0.5',
           'CJUNC_TOL_FF_UM': '0.5', 'CJUNC_PTFE_JLAW': 'P0', 'STEP3_RTOL': '1e-12'}
    r0 = RC.runner_ca_ext(env, ptfe_stamp='face_alpha', lean='2')
    r1_ = RC.runner_ca_ext(dict(env, CJUNC_PTFE_JLAW='P1'), ptfe_stamp='face_alpha', lean='2')
    r2_ = RC.runner_ca_ext(dict(env, CJUNC_PTFE_JLAW='P1'), ptfe_stamp='off', lean='2')
    chk('A14 runner_ca_ext — PTFE_STAMP=face_alpha + CJUNC=1 (P0 · P1) = 문제 없음 · off + P1 = REQUEST 거부',
        not r0['problems'] and not r1_['problems'] and any('REQUEST' in p for p in r2_['problems']),
        (r0['problems'], r1_['problems'], r2_['problems']))
    try:
        v = RC.runner_ca_ext_view(dict(r1_['receipt'], ptfe_stamp='face_alpha'))
        chk('A15 runner_ca_ext_view — 조합 영수증 → 팔 태그 `_fa_cj…` · payload 인자 P1 · 선언 칸 P1',
            v['arm_tag'].startswith('_fa_cj1000000_') and '--step3-cjunc-ptfe-jlaw P1' in v['flags']
            and ',ca_ext.cjunc.ptfe_jlaw=P1' in v['expect'], v)
    except Exception as e:                                  # noqa: BLE001
        chk('A15 runner_ca_ext_view (조합 영수증)', False, f'{type(e).__name__}: {e}')


# ── payload 끝-끝 (b6 픽스처 꼴 · vox 1.0 · 접합 옆을 지나는 PTFE 선 하나 더) ──
def make_fixture_pj(d, sdcp=False, near=True):
    import test_ca_ext_b6 as B6
    B6.make_fixture(d, sdcp=sdcp)
    if not near:
        return d
    pts, ph = np.load(os.path.join(d, 'se.npy')), np.load(os.path.join(d, 'phase.npy'))
    fid, kind = np.load(os.path.join(d, 'fibre.npy')), np.load(os.path.join(d, 'fibre_kind.npy'))
    #  접합 최근접점 (24.5, 24.5, 12.5) µm 에서 0.40 µm 떨어진 x 방향 PTFE 선 (덮임 문턱 r_P + r_f + tol_P = 0.124 + 0.075 + 0.5)
    near_line = B6._box(B6.line((12.5, 24.9, 12.5), (36.5, 24.9, 12.5), 97))
    pts = np.vstack([pts, near_line])
    ph = np.concatenate([ph, np.full(len(near_line), 4, ph.dtype)])
    fid = np.concatenate([fid, np.full(len(near_line), 3, fid.dtype)])
    kind = np.concatenate([kind, np.full(len(near_line), 1, kind.dtype)])
    np.save(os.path.join(d, 'se.npy'), pts)
    np.save(os.path.join(d, 'phase.npy'), ph)
    np.save(os.path.join(d, 'fibre.npy'), fid)
    np.save(os.path.join(d, 'fibre_kind.npy'), kind)
    np.save(os.path.join(d, 'fibre_dia.npy'), np.ones(len(pts)))
    return d


def _b6():
    import test_ca_ext_b6 as B6
    B6.ARGS = argparse.Namespace(skip_payload=False, old_scripts='', only='')
    return B6


@case('A-P payload 끝-끝 — face_alpha + 접합 (+ P1) · 두 하위 블록 · p3ca · ca_ext_record_ok · 원장 항등식')
def t_A_payload():
    if ARGS.skip_payload:
        print('    (--skip-payload — 건너뜀)')
        return
    B6 = _b6()
    d = os.path.join(TD, 'ap')
    os.makedirs(d)
    make_fixture_pj(d)
    FA_ = ['--ptfe-stamp', 'face_alpha']
    RT = ['--step3-rtol', '1e-12']
    rc0, log0, p0 = B6.run_payload(d, FA_ + B6.LEAN2 + B6.CJ + RT, out='fa_cj_p0.json')
    rc1, log1, p1 = B6.run_payload(d, FA_ + B6.LEAN2 + B6.cj_with(ptfe_jlaw='P1') + RT, out='fa_cj_p1.json')
    m0, m1 = B6.man_of(p0), B6.man_of(p1)
    ca0 = m0.get('ca_ext') or {}
    chk('AP1 payload face_alpha + 접합 (P0) + rtol = rc 0 · ca_ext 하위 블록 = ptfe_face + cjunc · 요청 칸 [cjunc] · p3ca · '
        'protocol_ok · ca_ext_record_ok · 게시 조건 (증서)',
        rc0 == 0 and sorted(ca0) == ['cjunc', 'ptfe_face', 'schema'] and m0.get('ca_ext_requested') == ['cjunc']
        and str(m0.get('physics_protocol_id', '')).startswith('p3ca-') and RC.protocol_ok(m0) == (True, None)
        and RC.ca_ext_record_ok(m0) == (True, None) and RC.next_gen_cert_ok(B6.s3_of(p0))[0],
        (rc0, log0.strip()[-400:], sorted(ca0), RC.ca_ext_record_ok(m0) if m0 else None))
    ev = ((ca0.get('cjunc') or {}).get('evidence') or {})
    sv = ev.get('solve') or {}
    shs = sv.get('dissipation_share') or {}
    chk('AP2 원장 · 소산 항등식 (조합 런) — P_total = I_bot (ΔV = 1 · CG 1e-12 · 1e-8) · 몫 합 = 1 · 접합 간선 1',
        isinstance(sv.get('P_total_code'), float) and rel(sv['P_total_code'], sv['I_bot_code']) < 1e-8
        and abs(sum(shs.values()) - 1.0) < 1e-9 and sv.get('n_junction_edges') == 1, sv)
    cnt1 = ((((m1.get('ca_ext') or {}).get('cjunc') or {}).get('evidence') or {}).get('counts') or {})
    s0, s1 = (B6.s3_of(p).get('sigma_e_eff_S_cm') or 0.0 for p in (p0, p1))
    chk('AP3 payload P1 (face_alpha) = rc 0 · 덮인 접합 절단 1 · σ(P1) ≤ σ(P0) · ca_ext_record_ok · id ≠ P0 (protocol 이 다르다)',
        rc1 == 0 and cnt1.get('n_cut_p1') == 1 and cnt1.get('n_ptfe_cov') == 1 and 0 < s1 <= s0 * (1 + 1e-9)
        and RC.ca_ext_record_ok(m1) == (True, None) and m1.get('physics_protocol_id') != m0.get('physics_protocol_id'),
        (rc1, log1.strip()[-300:], cnt1, s0, s1))
    for nm, extra, code in (('off + P1', ['--ptfe-stamp', 'off'] + B6.LEAN2 + B6.cj_with(ptfe_jlaw='P1') + RT, 'P1_NEEDS_FACE_ALPHA'),
                            ('centerline + P1', ['--ptfe-stamp', 'centerline'] + B6.LEAN2 + B6.cj_with(ptfe_jlaw='P1') + RT,
                             'P1_NEEDS_FACE_ALPHA')):
        rc, log, _p = B6.run_payload(d, extra, out=f'ref_{code}_{nm[:3]}.json')
        chk(f'AP4 payload [{nm}] = 거부 그대로 (S2_CJUNC_REFUSED|{code}|)', rc != 0 and f'S2_CJUNC_REFUSED|{code}|' in log,
            (rc, log.strip()[-200:]))
    #  ── 검증기 — 조합 매니페스트의 변조 ──
    if m0 and RC.ca_ext_record_ok(m0)[0]:
        def mut(fn):
            x = json.loads(json.dumps(m0))
            fn(x)
            x['physics_protocol_id'] = RC.physics_protocol_id(x)
            return RC.ca_ext_record_ok(x)[0]
        bad = {
            'ptfe_face 블록 지움 (face_alpha 도장 그대로)': lambda x: x['ca_ext'].pop('ptfe_face'),
            '접합 protocol 의 ptfe_stamp = off (매니페스트 face_alpha)': lambda x: x['ca_ext']['cjunc']['protocol'].update(ptfe_stamp='off'),
            'P0 인데 절단 수 > 0': lambda x: x['ca_ext']['cjunc']['evidence']['counts'].update(
                n_cut_p1=1, n_edge=x['ca_ext']['cjunc']['evidence']['counts']['n_edge'] - 1),
        }
        for nm, fn in bad.items():
            chk(f'AP5 ca_ext_record_ok 거부 [{nm}]', not mut(fn))


# ═════════════════════════ B — 극한 런 (바닥 R_j → ∞ · 천장 R_j → 0) ═════════════════════════
#  LIM: 섬유 A (1,1,0..3) 위 끝 ↔ 섬유 B (2,1,3..7) 아래 끝 (x 로 h · 접합 instance 하나 · 자리 면 (1,1,3)|(2,1,3)) +
#       우회 섬유 C (4,1,0..7 · 다른 섬유와 2h 이상 = instance 없음).  A 는 아래 판에만 · B 는 위 판에만 닿는다.
LIM_N = (6, 3, 8)


def lim_rows():
    A = [c(1, 1, 0), c(1, 1, 3)]
    B = [c(2, 1, 3), c(2, 1, 7)]
    C = [c(4, 1, 0), c(4, 1, 7)]
    return block([A, B, C], 2, 1, [10, 20, 30])


CJ_REQ = {'R_j_ohm': 1.0e6, 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': SMIN, 'tol_ff_um': TOL, 'ptfe_jlaw': 'P0'}


def lim_prep(req, sdcp_mod=None, addr=None, n=LIM_N):
    addr = addr if addr is not None else lim_rows()
    sid, pid = bed(addr, n)
    P, PH, F, K = addr
    prep = quiet(CW.payload_prepare, sid, lo=(0.0, 0.0, 0.0), vox=H, pts=P, phase=PH, fid=F, kind=K, cjunc=req,
                 sdcp_mod=sdcp_mod, ptfe_stamp='off')
    return prep, sid, pid


@case('B 극한 런 — 손계산 · 기록 꼴 · 러너 · payload · 검증기')
def t_B():
    I_C = chain_I([G_PL] + [G_AX] * 7 + [G_PL])
    I_AB = lambda gj: chain_I([G_PL] + [G_AX] * 3 + ([gj] if gj is not None else []) + [G_AX] * 4 + [G_PL])  # noqa: E731
    #  ── 손계산 — 배선 함수 (ca_ext_cjunc.payload_prepare) 가 만든 계획으로 ──
    for nm, req, want in (('바닥 (R_j = ∞ · 간선 없음 · 자리 면 절단)', dict(CJ_REQ, R_j_ohm=None, rj_limit='inf'), I_C),
                          ('천장 (R_j = 0 · 접합 양 끝 = 한 노드)', dict(CJ_REQ, R_j_ohm=0.0, rj_limit='zero'), I_C + I_AB(None)),
                          ('정량 R_j 1e6 (대조 · 같은 회로)', dict(CJ_REQ), I_C + I_AB(1e4 / 1e6))):
        try:
            prep, sid, pid = lim_prep(req)
            r = solve(sid, LIM_N, cj=prep['plan'])
            I = I_of(r, LIM_N)
            chk(f'B1 손계산 [{nm}] — 해 전류 = 손으로 세운 회로 (1e-12 · 직접 풀이)', rel(I, want) < 1e-12, (I, want, r.get('reason')))
        except Exception as e:                              # noqa: BLE001
            chk(f'B1 손계산 [{nm}]', False, f'{type(e).__name__}: {e}')
    #  ── 기록 꼴 (매니페스트 protocol · 한 꼴 — 수 칸 null/0.0 + 문자열 표지) ──
    try:
        pf = CW.cjunc_protocol_record(ptfe_stamp='off', rj_limit='inf', **dict(CJ_REQ, R_j_ohm=None))
        pz = CW.cjunc_protocol_record(ptfe_stamp='off', rj_limit='zero', **dict(CJ_REQ, R_j_ohm=0.0))
        pf_cli = CW.cjunc_protocol_record(ptfe_stamp='off', rj_limit='inf', **dict(CJ_REQ, R_j_ohm=float('inf')))
        pq = CW.cjunc_protocol_record(ptfe_stamp='off', **CJ_REQ)
        js = json.dumps(pf, allow_nan=False) and json.dumps(pz, allow_nan=False)
        chk('B2 극한 protocol — 바닥 R_j_ohm null + rj_limit inf · 천장 0.0 + zero · quantitative False · allow_rj_limits True · '
            'CLI 의 float inf 도 같은 꼴 (null) · JSON (allow_nan=False) 직렬화 · 정량 protocol 에는 rj_limit 칸 없음',
            pf['R_j_ohm'] is None and pf['rj_limit'] == 'inf' and pf['quantitative'] is False and pf['allow_rj_limits'] is True
            and pz['R_j_ohm'] == 0.0 and pz['rj_limit'] == 'zero' and pz['quantitative'] is False and pf_cli == pf
            and bool(js) and 'rj_limit' not in pq and pq['quantitative'] is True and pq['allow_rj_limits'] is False,
            (pf, pz))
    except Exception as e:                                  # noqa: BLE001
        chk('B2 극한 protocol 기록 꼴', False, f'{type(e).__name__}: {e}')
    bad = {'inf 표지 + 유한 R_j': (1e6, 'inf'), 'zero 표지 + 양수 R_j': (1e6, 'zero'), 'zero 표지 + null': (None, 'zero'),
           '표지 없이 R_j inf': (float('inf'), None), '표지 없이 R_j 0': (0.0, None), '표지 없이 null': (None, None),
           '대문자 INF': (None, 'INF'), 'infinity': (None, 'infinity'), '표지 bool': (None, True), 'NaN + inf 표지': (float('nan'), 'inf'),
           '음수 + zero': (-0.0 - 1.0, 'zero'), 'bool R_j False + zero': (False, 'zero')}
    res = []
    for nm, (rv, lim) in bad.items():
        try:
            CW.cjunc_protocol_record(ptfe_stamp='off', rj_limit=lim, **dict(CJ_REQ, R_j_ohm=rv))
            res.append((nm, False))
        except (ValueError, TypeError):
            res.append((nm, True))
    chk('B3 극한 protocol 거부 — 표지 ↔ 값 모순 · 표지 없는 극한 · 모르는 표지 (대소문자 · 다른 낱말 · bool) · NaN · 음수',
        all(x[1] for x in res), [x for x in res if not x[1]])
    #  ── 러너 env → 영수증 요청 · payload 인자 · 선언 · 태그 ──
    env = {'CJUNC': '1', 'CJUNC_RJ': 'inf', 'CJUNC_LEN_LAW': 'len_scaled_v0', 'CJUNC_UNREG_LAW': 'cut', 'CJUNC_S_MIN_UM': '0.6',
           'CJUNC_TOL_FF_UM': '0.05', 'CJUNC_PTFE_JLAW': 'P0', 'STEP3_RTOL': '1e-12'}
    rf = RC.runner_ca_ext(env, ptfe_stamp='face_alpha', lean='2')
    rz = RC.runner_ca_ext(dict(env, CJUNC_RJ='0'), ptfe_stamp='face_alpha', lean='2')
    rq = (rf['receipt'] or {}).get('ca_ext_request', {}).get('cjunc', {})
    rqz = (rz['receipt'] or {}).get('ca_ext_request', {}).get('cjunc', {})
    chk('B4 러너 CJUNC_RJ=inf · 0 → 문제 없음 · 영수증 요청 R_j_ohm null + rj_limit inf · 0.0 + zero (한 꼴)',
        not rf['problems'] and not rz['problems'] and rq.get('R_j_ohm', 'x') is None and rq.get('rj_limit') == 'inf'
        and rqz.get('R_j_ohm') == 0.0 and rqz.get('rj_limit') == 'zero', (rf['problems'], rz['problems'], rq, rqz))
    refused = []
    for v in ('INF', 'Inf', 'infinity', '+inf', '1e999', 'nan', '-0', ' inf', 'inf ', '∞'):
        r = RC.runner_ca_ext(dict(env, CJUNC_RJ=v), ptfe_stamp='face_alpha', lean='2')
        refused.append((v, bool(r['problems'])))
    chk('B5 러너 극한 표기는 둘만 (`inf` 낱말 · ASCII 10 진 0) — INF · Infinity · +inf · 1e999 · nan · -0 · 공백 · ∞ = 거부',
        all(x[1] for x in refused), [x for x in refused if not x[1]])
    #  B5b — 천장 = **글자 그대로 0** 인 10 진 표기만 (0 · 0.0 · 00 · 0e0 = 같은 물리 = 같은 요청) · 0 이 아닌 글자가 float 에서 0 으로
    #    떨어지는 것 (1e-400 · 언더플로) 은 천장이 아니라 거부 (검사 전 정규화로 극한 런이 되지 않게)
    zs = {v: RC.runner_ca_ext(dict(env, CJUNC_RJ=v), ptfe_stamp='face_alpha', lean='2') for v in ('0.0', '00', '0e0', '0.000')}
    uf = {v: RC.runner_ca_ext(dict(env, CJUNC_RJ=v), ptfe_stamp='face_alpha', lean='2') for v in ('1e-400', '0.1e-330', '5e-324e')}
    chk('B5b 러너 천장 = 글자 그대로 0 (0.0 · 00 · 0e0 · 0.000 → 0 과 같은 영수증) · 언더플로로 0 이 되는 0 아닌 글자 (1e-400 · 0.1e-330) = 거부',
        all(not r['problems'] and r['receipt'] == rz['receipt'] for r in zs.values())
        and all(r['problems'] for r in uf.values()),
        ({v: r['problems'][:1] for v, r in zs.items()}, {v: (r['problems'][:1], r['receipt']) for v, r in uf.items()}))
    try:
        vf = RC.runner_ca_ext_view(dict(rf['receipt'], ptfe_stamp='face_alpha'))
        vz = RC.runner_ca_ext_view(dict(rz['receipt'], ptfe_stamp='face_alpha'))
        fl = vf['flags'].split()
        chk('B6 runner_ca_ext_view — 바닥 인자 `--step3-cjunc-rj inf --step3-cjunc-rj-limit inf` · 선언 R_j_ohm=None · rj_limit=inf · '
            '태그 `_fa_cjinf_<h8>` · 천장 `0.0` · zero · `_fa_cj0_<h8>` · 둘의 태그 다름',
            fl[fl.index('--step3-cjunc-rj') + 1] == 'inf' and fl[fl.index('--step3-cjunc-rj-limit') + 1] == 'inf'
            and ',ca_ext.cjunc.R_j_ohm=None' in vf['expect'] and ',ca_ext.cjunc.rj_limit=inf' in vf['expect']
            and re.match(r'^_fa_cjinf_[0-9a-f]{8}_rt1em12$', vf['arm_tag'])
            and '--step3-cjunc-rj 0.0' in vz['flags'] and '--step3-cjunc-rj-limit zero' in vz['flags']
            and ',ca_ext.cjunc.rj_limit=zero' in vz['expect'] and re.match(r'^_fa_cj0_[0-9a-f]{8}_rt1em12$', vz['arm_tag']),
            (vf, vz))
    except Exception as e:                                  # noqa: BLE001
        chk('B6 runner_ca_ext_view (극한)', False, f'{type(e).__name__}: {e}')
    for nm, rq_ in (('요청 rj_limit inf + R_j 1e6', dict(CJ_REQ, rj_limit='inf')),
                    ('요청 R_j null 표지 없음', dict(CJ_REQ, R_j_ohm=None)),
                    ('요청 모르는 표지', dict(CJ_REQ, R_j_ohm=None, rj_limit='floor'))):
        chk(f'B7 ca_ext_request_problem 거부 [{nm}]', RC.ca_ext_request_problem({'cjunc': rq_}) is not None)
    chk('B7 ca_ext_request_problem — 바닥 · 천장 요청 통과',
        RC.ca_ext_request_problem({'cjunc': dict(CJ_REQ, R_j_ohm=None, rj_limit='inf')}) is None
        and RC.ca_ext_request_problem({'cjunc': dict(CJ_REQ, R_j_ohm=0.0, rj_limit='zero')}) is None)
    #  ── 바닥 + S3 c = 1 = NaN 없음 (근접 instance R_j' = 0 = 축약 · 그 밖 = ∞) ──
    try:
        addr = cat(lim_rows(), block([[c(1, 2, 3)]], 5, 0, [-1]))          # SDCP 점 하나가 접합 옆 (근접)
        sid, pid = bed(addr, LIM_N)
        reg = registry(sid, addr, r_sdcp_um=0.15, tol_sj_um=0.1)
        pl = CJ.cjunc_plan(reg, math.inf, unreg_law='cut', ptfe_stamp='off', ptfe_jlaw='P0', sdcp_mod={'c': 1.0},
                           quantitative=False, allow_rj_limits=True)
        a = reg['instances']['a_sdcp']
        chk('B8 바닥 (R_j = ∞) + c = 1 — 근접 instance = 축약 (∞·0 = NaN 아님) · g 유한 · 비근접 = 극한 (none_inf)',
            bool(a.any()) and np.isfinite(pl['g_code']).all() and not np.isnan(pl['rj_eff'][pl['mode'] != CJ.MODE_UNREALIZED]).any()
            and all(int(m) == (CJ.MODE_CONTRACT if a[k] else CJ.MODE_NONE_INF) for k, m in enumerate(pl['mode'])),
            (a, pl['mode'], pl['rj_eff']))
    except Exception as e:                                  # noqa: BLE001
        chk('B8 바닥 + c = 1', False, f'{type(e).__name__}: {e}')
    if ARGS.skip_payload:
        print('    (--skip-payload — B payload 끝-끝 건너뜀)')
        return
    B6 = _b6()
    d = os.path.join(TD, 'bp')
    os.makedirs(d)
    B6.make_fixture(d, sdcp=False)
    RT = ['--step3-rtol', '1e-12']
    FL = B6.cj_with(rj='inf') + ['--step3-cjunc-rj-limit', 'inf']
    CE = B6.cj_with(rj='0') + ['--step3-cjunc-rj-limit', 'zero']
    out = {}
    for nm, ex in (('floor', FL), ('ceiling', CE), ('quant', B6.CJ)):
        out[nm] = B6.run_payload(d, B6.OFF + B6.LEAN2 + ex + RT, out=f'lim_{nm}.json')
    mf, mz, mq = (B6.man_of(out[k][2]) for k in ('floor', 'ceiling', 'quant'))
    pf_, pz_ = (((m.get('ca_ext') or {}).get('cjunc') or {}).get('protocol') or {} for m in (mf, mz))
    cf_, cz_ = ((((m.get('ca_ext') or {}).get('cjunc') or {}).get('evidence') or {}).get('counts') or {} for m in (mf, mz))
    chk('B9 payload 바닥 · 천장 + rtol = rc 0 · 표지 (null + inf · 0.0 + zero · quantitative False · allow_rj_limits True) · '
        'p3ca · ca_ext_record_ok · 게시 조건 (증서)',
        out['floor'][0] == 0 and out['ceiling'][0] == 0 and pf_.get('R_j_ohm', 'x') is None and pf_.get('rj_limit') == 'inf'
        and pz_.get('R_j_ohm') == 0.0 and pz_.get('rj_limit') == 'zero' and pf_.get('quantitative') is False
        and pz_.get('allow_rj_limits') is True
        and all(str(m.get('physics_protocol_id', '')).startswith('p3ca-') and RC.ca_ext_record_ok(m) == (True, None)
                for m in (mf, mz)),
        (out['floor'][0], out['floor'][1].strip()[-300:], out['ceiling'][0], out['ceiling'][1].strip()[-300:], pf_, pz_))
    chk('B10 payload 극한 원장 — 바닥 = 간선 0 · none_inf = instance · 천장 = 간선 0 · 축약 = instance (S3 없이)',
        cf_.get('n_edge') == 0 and cf_.get('n_none_inf') == cf_.get('n_instances') == 1
        and cz_.get('n_edge') == 0 and cz_.get('n_contract') == cz_.get('n_instances') == 1 and cz_.get('n_none_inf') == 0,
        (cf_, cz_))
    sf, sz, sq = (B6.s3_of(out[k][2]).get('sigma_e_eff_S_cm') or 0.0 for k in ('floor', 'ceiling', 'quant'))
    ids = {m.get('physics_protocol_id') for m in (mf, mz, mq)}
    chk('B11 σ 순서 바닥 ≤ 정량 (1e6) ≤ 천장 (같은 침대 · Rayleigh) · id 셋 다 다르다', 0 < sf <= sq * (1 + 1e-9)
        and sq <= sz * (1 + 1e-9) and len(ids) == 3, (sf, sq, sz, ids))
    for nm, ex, code in (('R_j inf 표지 없이', B6.cj_with(rj='inf'), 'VALUE'), ('R_j 0 표지 없이', B6.cj_with(rj='0'), 'VALUE'),
                         ('표지 inf + R_j 1e6', B6.CJ + ['--step3-cjunc-rj-limit', 'inf'], 'VALUE'),
                         ('표지 zero + R_j inf', B6.cj_with(rj='inf') + ['--step3-cjunc-rj-limit', 'zero'], 'VALUE')):
        rc, log, _p = B6.run_payload(d, B6.OFF + B6.LEAN2 + ex + RT, out=f'limref_{abs(hash(nm)) % 997}.json')
        chk(f'B12 payload 극한 거부 [{nm}] → S2_CJUNC_REFUSED|{code}|', rc != 0 and f'S2_CJUNC_REFUSED|{code}|' in log,
            (rc, log.strip()[-200:]))
    rc, log, _p = B6.run_payload(d, B6.OFF + B6.LEAN2 + ['--step3-cjunc-rj-limit', 'inf'], out='limref_nocj.json')
    chk('B12 payload 극한 표지만 (접합 끔) → S2_CJUNC_REFUSED|FLAG_WITHOUT_CJUNC|', rc != 0 and 'FLAG_WITHOUT_CJUNC' in log,
        (rc, log.strip()[-200:]))
    #  ── 검증기 변조 (극한 매니페스트) ──
    if mf and RC.ca_ext_record_ok(mf)[0] and mz and RC.ca_ext_record_ok(mz)[0]:
        def mut(m, fn):
            x = json.loads(json.dumps(m))
            fn(x)
            x['physics_protocol_id'] = RC.physics_protocol_id(x)
            return RC.ca_ext_record_ok(x)[0]
        CP = lambda x: x['ca_ext']['cjunc']['protocol']        # noqa: E731
        CC = lambda x: x['ca_ext']['cjunc']['evidence']['counts']   # noqa: E731
        bad = {
            '바닥인데 간선 > 0': (mf, lambda x: CC(x).update(n_edge=1, n_none_inf=CC(x)['n_none_inf'] - 1)),
            '바닥 표지 지움 (R_j null 남음)': (mf, lambda x: CP(x).pop('rj_limit')),
            '바닥 quantitative True 로': (mf, lambda x: CP(x).update(quantitative=True)),
            '천장인데 극한 instance': (mz, lambda x: CC(x).update(n_none_inf=1, n_contract=CC(x)['n_contract'] - 1)),
            '천장 표지 inf 로 (R_j 0.0 남음)': (mz, lambda x: CP(x).update(rj_limit='inf')),
            '천장 R_j 1e6 으로 (표지 zero 남음)': (mz, lambda x: CP(x).update(R_j_ohm=1e6)),
        }
        for nm, (m, fn) in bad.items():
            chk(f'B13 ca_ext_record_ok 거부 [{nm}]', not mut(m, fn))
        rec = {'ca_ext_request': {'cjunc': dict(CJ_REQ, R_j_ohm=1e6, s_min_um=0.5, tol_ff_um=0.5)}}
        chk('B14 receipt_match — 정량 요청 영수증 ↔ 바닥 팔 = 거부 (요청 ↔ 결과)',
            RC._receipt_ext_problem(rec, mf) is not None)


# ═════════════════════════ C — 러너 ARM_LIST ═════════════════════════
def _tr():
    import test_ca_ext_runner as TR
    if TR.TD is None:
        TR.TD = os.path.join(TD, 'tr')
        os.makedirs(TR.TD)
        TR.SHIMDIR = os.path.join(TR.TD, '_bin')
        os.makedirs(TR.SHIMDIR)
        with open(os.path.join(TR.SHIMDIR, 'python3'), 'w', encoding='utf-8') as f:
            f.write(TR.SHIM.replace('__REAL__', os.path.realpath(sys.executable)))
        os.chmod(os.path.join(TR.SHIMDIR, 'python3'), 0o755)
        os.makedirs(os.path.join(TR.TD, '_probe'))
        TR.ARGS = argparse.Namespace(old_runner='', only='', keep=False)
    return TR


@case('C 러너 ARM_LIST — 팔 고르기 · 이름 · OUTDIR · 영수증 · 거부')
def t_C():
    TR = _tr()
    keys = ('OUTDIR', 'ARMS', 'ARM_LIST', 'AR_TAG', 'NG_TAG')
    p12 = TR.probe({'ARMS': None, 'ARM_LIST': '1,2'}, keys=keys)
    p2 = TR.probe({'ARMS': '2'}, keys=keys)
    p21 = TR.probe({'ARMS': None, 'ARM_LIST': '2,1'}, keys=keys)
    p8 = TR.probe({'ARMS': None}, keys=keys)
    chk('C1 설정부 — ARM_LIST=1,2 → 중단 없음 · ARMS = 2 (팔 수) · OUTDIR 에 `_arm2` + 목록 태그 `_arml1-2` · ARMS=2 와 다른 OUTDIR · '
        '2,1 = 같은 정규 목록 (같은 OUTDIR)',
        p12['_rc'] == 0 and p12.get('ARMS') == '2' and '_arm2' in (p12.get('OUTDIR') or '') and '_arml1-2' in (p12.get('OUTDIR') or '')
        and p12.get('OUTDIR') != p2.get('OUTDIR') and p21.get('OUTDIR') == p12.get('OUTDIR'),
        (p12, p2.get('OUTDIR'), p21.get('OUTDIR')))
    chk('C2 끔 (ARM_LIST 없음) — ARMS 기본 8 · OUTDIR 에 목록 태그 없음', p8['_rc'] == 0 and p8.get('ARMS') == '8'
        and '_arml' not in (p8.get('OUTDIR') or ''), p8)
    refuse = [('중복 1,1', {'ARMS': None, 'ARM_LIST': '1,1'}), ('범위 밖 8', {'ARMS': None, 'ARM_LIST': '1,8'}),
              ('음수', {'ARMS': None, 'ARM_LIST': '-1,2'}), ('빈 칸 1,,2', {'ARMS': None, 'ARM_LIST': '1,,2'}),
              ('글자', {'ARMS': None, 'ARM_LIST': 'a'}), ('공백', {'ARMS': None, 'ARM_LIST': '1, 2'}),
              ('빈 문자열', {'ARMS': None, 'ARM_LIST': ''}), ('ARMS 와 동시', {'ARMS': '3', 'ARM_LIST': '1,2'}),
              ('0..N−1 접두 = ARMS 로 (이름 하나)', {'ARMS': None, 'ARM_LIST': '0,1'}),
              ('전부 = ARMS=8 로', {'ARMS': None, 'ARM_LIST': '0,1,2,3,4,5,6,7'}), ('유니코드 숫자', {'ARMS': None, 'ARM_LIST': '١'}),
              ('앞 0 (01)', {'ARMS': None, 'ARM_LIST': '01,2'})]
    for nm, over in refuse:
        r = TR.probe(over, keys=keys)
        chk(f'C3 ARM_LIST 거부 [{nm}] → 설정부 중단 (rc ≠ 0 · 디렉터리 만들기 전)', r['_rc'] != 0 and 'ARM_LIST' in r['_log'],
            (r['_rc'], r['_log'][-200:]))
    if ARGS.skip_payload:
        print('    (--skip-payload — C 러너 끝-끝 건너뜀)')
        return
    ws = TR.make_ws('c_al')
    r = TR.run_runner(ws, {'ARMS': None, 'ARM_LIST': '1,2'})
    rc = r.receipt or {}
    chk('C4 러너 끝-끝 ARM_LIST=1,2 → rc 0 · 팔 = a1 · a2 만 (a0 없음) · 킷 둘 · 영수증 arms 2 · arm_list [1, 2] · origin 일정 8',
        r.rc == 0 and r.arms == ['p2_DBE_a1.json', 'p2_DBE_a2.json', 'p2_SBE_a1.json', 'p2_SBE_a2.json']
        and rc.get('arms') == 2 and rc.get('arm_list') == [1, 2] and len(rc.get('origins') or []) == 8,
        (r.rc, r.arms, rc.get('arms'), rc.get('arm_list'), r.log[-600:]))
    ok_or = []
    for a in r.arms:
        s3, m = TR.manifest_of(os.path.join(r.outdir, a))
        i = int(re.search(r'_a(\d+)\.json$', a).group(1))
        want = RC.expected_origins_for(1.0)[i]
        ok_or.append(tuple(round(x, 9) for x in m.get('origin_shift_um') or ()) == tuple(round(x, 9) for x in want))
    chk('C5 팔 i 의 origin = 영수증 origin 일정의 i 번째 (러너 SHIFTS 순서) — a1 · a2', ok_or and all(ok_or), ok_or)
    import sr01_stamp_compare as SC
    a1 = os.path.join(r.outdir, 'p2_SBE_a1.json')
    chk('C6 check_arm (영수증 대조) — 고른 팔 통과', SC.check_arm(a1, 'segment', expect_backend='cpu',
                                                      receipt=rc) is None, SC.check_arm(a1, 'segment', expect_backend='cpu', receipt=rc))
    s3, m = TR.manifest_of(a1)
    m0 = dict(m, origin_shift_um=list(RC.expected_origins_for(1.0)[0]))
    chk('C7 receipt_match — 목록 밖 팔 (a0 의 origin) = 거부 (같은 OUTDIR 에 섞이지 않게)', not RC.receipt_match(rc, m0, origin=m0['origin_shift_um'])[0],
        RC.receipt_match(rc, m0, origin=m0['origin_shift_um']))
    chk('C8 진단 런 = 생산 봉인 없음 (ARMS ≠ 8 와 같은 길)', 'seal-only' not in r.log and '계약 봉인 —' not in r.log, r.log[-300:])
    #  영수증 digest — 목록이 다르면 다르다 · 목록 없는 옛 영수증 digest 는 그대로 (선택 칸)
    base = {k: v for k, v in rc.items() if k not in ('arm_list', 'receipt_digest')}
    chk('C9 receipt_digest — arm_list 는 선택 칸 (있을 때만 · 목록이 다르면 digest 다름 · 없으면 옛 본문)',
        RC.receipt_digest(dict(base, arm_list=[1, 2])) != RC.receipt_digest(dict(base, arm_list=[1, 3]))
        and RC.receipt_digest(dict(base, arm_list=[1, 2])) != RC.receipt_digest(base), '')


# ═════════════════════════ D — off 격자 sid 지문 ═════════════════════════
@case('D off 격자 sid 지문 ca_ext.ptfe_face.evidence.fp.sid_off')
def t_D():
    #  솔브 수준 — payload_prepare 가 sid 격자 (= off 격자) 의 지문을 싣는다 (같은 함수 step3_sigma._grid_fp)
    addr = fc_rows(('cap1',))
    sid, pid = bed(addr, FC_N)
    P, PH, F, K = addr
    m4 = PH == 4
    try:
        prep = FA.payload_prepare(sid, pid, lo=(0.0, 0.0, 0.0), vox=H, sig_e=sig_e(), sig_i=S3.ionic_sigma_table(0.3e-3, 3e-3),
                                  pts=P[m4], fid=F[m4], kind=K[m4], channels=('electronic', 'ionic'), dia_law='rope',
                                  true_volume_um3=None, build_ionic=False)
        blk = FA.payload_block(prep, {})
        so = blk['evidence']['fp'].get('sid_off')
        chk('D1 payload_block — evidence.fp.sid_off = step3_sigma._grid_fp(sid) (off 격자 = face_alpha 의 sid 격자)',
            isinstance(so, str) and so == S3._grid_fp(sid) and re.fullmatch(r'[0-9a-f]{32}', so), so)
    except Exception as e:                                  # noqa: BLE001
        chk('D1 payload_block sid_off', False, f'{type(e).__name__}: {e}')
    if ARGS.skip_payload:
        print('    (--skip-payload — D payload 끝-끝 건너뜀)')
        return
    B6 = _b6()
    d = os.path.join(TD, 'dp')
    os.makedirs(d)
    make_fixture_pj(d)
    FA_ = ['--ptfe-stamp', 'face_alpha']
    RT = ['--step3-rtol', '1e-12']
    ra = B6.run_payload(d, FA_ + B6.LEAN2 + RT, out='d_fa1.json')
    rb = B6.run_payload(d, FA_ + B6.LEAN2 + RT, out='d_fa2.json')
    rcj = B6.run_payload(d, FA_ + B6.LEAN2 + B6.CJ + RT, out='d_facj.json')
    rv = B6.run_payload(d, FA_ + B6.LEAN2 + RT + ['--step3-vox', '0.9'], out='d_fa_vox09.json')

    def so_of(p):
        return ((((B6.man_of(p).get('ca_ext') or {}).get('ptfe_face') or {}).get('evidence') or {}).get('fp') or {}).get('sid_off')
    sa, sb, sc, sv = (so_of(x[2]) for x in (ra, rb, rcj, rv))
    cjs = (((((B6.man_of(rcj[2]).get('ca_ext') or {}).get('cjunc') or {}).get('evidence') or {}).get('fp') or {}).get('sid'))
    chk('D2 같은 킷 · 같은 래스터 두 런 = 같은 sid_off · 접합을 켜도 같다 (래스터 불변) · 조합 런 = 접합 원장 sid 지문 · vox 다르면 다르다',
        all(x[0] == 0 for x in (ra, rb, rcj, rv)) and isinstance(sa, str) and sa == sb == sc == cjs and sv and sv != sa,
        (sa, sb, sc, cjs, sv, ra[1].strip()[-200:]))
    m = B6.man_of(rcj[2])
    if m and RC.ca_ext_record_ok(m)[0]:
        def mut(fn):
            x = json.loads(json.dumps(m))
            fn(x)
            return RC.ca_ext_record_ok(x)[0]
        FP = lambda x: x['ca_ext']['ptfe_face']['evidence']['fp']      # noqa: E731
        for nm, fn in (('sid_off 지움', lambda x: FP(x).pop('sid_off')), ('sid_off 모양 (대문자)', lambda x: FP(x).update(sid_off=sa.upper())),
                       ('sid_off ≠ 접합 원장 sid', lambda x: FP(x).update(sid_off='0' * 32))):
            chk(f'D3 ca_ext_record_ok 거부 [{nm}]', not mut(fn))


# ═════════════════════════ E — CG 반복 수 ═════════════════════════
@case('E CG 반복 수 — 증서 켤 때 주 · 이어 풀기 · 보조 솔브 · 끔 = 옛 키')
def t_E():
    addr = fc_rows(())
    sid, pid = bed(addr, FC_N)
    sig = sig_e()
    old_cc, old_rt = S3.CONV_CERT, S3.CG_RTOL
    cnt = {'n': 0, 'kw': []}
    real_cg = S3.cg

    def spy_cg(A, b, *a, **k):
        cnt['kw'].append(sorted(k))
        return real_cg(A, b, *a, **k)
    try:
        S3.cg = spy_cg
        S3.CONV_CERT, S3.CG_RTOL = False, 1e-8
        r_off = quiet(S3.solve_sigma_z, sid, sig, H, z_top_um=FC_N[2] * H, z_bot_um=0.0)
        kw_off = list(cnt['kw'])
        cnt['kw'].clear()
        S3.CONV_CERT, S3.CG_RTOL = True, 1e-12
        r_on = quiet(S3.solve_sigma_z, sid, sig, H, z_top_um=FC_N[2] * H, z_bot_um=0.0)
    finally:
        S3.cg = real_cg
        S3.CONV_CERT, S3.CG_RTOL = old_cc, old_rt
    chk('E1 증서 끔 (옛 꼴) — 결과에 cg_iters 칸 없음 · CG 호출에 callback 없음 (옛 호출 그대로)',
        'cg_iters' not in r_off and all('callback' not in k for k in kw_off) and kw_off, (sorted(r_off), kw_off))
    cert = r_on.get('conv_cert') or {}
    it = r_on.get('cg_iters')
    chk('E2 증서 켬 — 주 솔브 반복 수 (int ≥ 1) · 증서에 iters = 주 · resolve_iters (int ≥ 0) · 수렴 (info 0)',
        type(it) is int and it >= 1 and cert.get('iters') == it and type(cert.get('resolve_iters')) is int
        and cert.get('resolve_iters') >= 0 and r_on.get('cg_info') == 0, (it, {k: cert.get(k) for k in ('iters', 'resolve_iters')}))
    #  독립 셈 — 같은 행렬 · 같은 b · 같은 전처리 (Jacobi) · scipy cg callback
    cap = {}
    real_solve = S3._solve_cg

    def grab(L, b, *a, **k):
        cap.setdefault('L', L)
        cap.setdefault('b', b)
        return real_solve(L, b, *a, **k)
    try:
        S3._solve_cg = grab
        S3.CONV_CERT, S3.CG_RTOL = True, 1e-12
        quiet(S3.solve_sigma_z, sid, sig, H, z_top_um=FC_N[2] * H, z_bot_um=0.0)
    finally:
        S3._solve_cg = real_solve
        S3.CONV_CERT, S3.CG_RTOL = old_cc, old_rt
    n = [0]
    from scipy import sparse
    from scipy.sparse.linalg import cg as _cg
    L = cap['L']
    Minv = sparse.diags(1.0 / L.diagonal())
    try:
        _cg(L, cap['b'], rtol=1e-12, maxiter=S3.CG_MAXITER, M=Minv, callback=lambda xk: n.__setitem__(0, n[0] + 1))
    except TypeError:
        _cg(L, cap['b'], tol=1e-12, maxiter=S3.CG_MAXITER, M=Minv, callback=lambda xk: n.__setitem__(0, n[0] + 1))
    chk('E3 반복 수 = 독립 셈 (같은 행렬 · scipy cg callback)', it == n[0], (it, n[0]))
    if ARGS.skip_payload:
        print('    (--skip-payload — E payload 끝-끝 건너뜀)')
        return
    B6 = _b6()
    d = os.path.join(TD, 'ep')
    os.makedirs(d)
    B6.make_fixture(d, sdcp=False)
    LC = [x for x in B6.LEAN2 if x != '--no-collector']                  # 집전체 두 솔브 (wetted · bare) 도 돈다
    r1 = B6.run_payload(d, B6.OFF + B6.LEAN2 + ['--step3-rtol', '1e-12'], out='e_rt.json')
    r3 = B6.run_payload(d, B6.OFF + B6.LEAN3 + ['--step3-rtol', '1e-12'], out='e_rt3.json')
    rc_ = B6.run_payload(d, B6.OFF + LC + ['--step3-rtol', '1e-12'], out='e_rtc.json')
    r0 = B6.run_payload(d, B6.OFF + B6.LEAN2, out='e_off.json')
    s1, s3_, sc_, s0 = (B6.s3_of(x[2]) for x in (r1, r3, rc_, r0))

    def _int(v):
        return type(v) is int and v >= 1
    chk('E4 payload rtol — step3.cg_iters · conv_cert.iters = 같은 값 · resolve_iters (수렴했어도 남긴다)',
        r1[0] == 0 and _int(s1.get('cg_iters')) and (s1.get('conv_cert') or {}).get('iters') == s1.get('cg_iters')
        and type((s1.get('conv_cert') or {}).get('resolve_iters')) is int, (r1[0], s1.get('cg_iters'), s1.get('conv_cert')))
    chk('E5 payload rtol LEAN 3 — 이온 솔브 반복 수 (ion_cg_iters · ion_conv_cert.iters)', r3[0] == 0 and _int(s3_.get('ion_cg_iters'))
        and (s3_.get('ion_conv_cert') or {}).get('iters') == s3_.get('ion_cg_iters'), (r3[0], s3_.get('ion_cg_iters')))
    cg_ = sc_.get('collector_geometric') or {}
    chk('E6 payload rtol + 집전체 — 보조 솔브 반복 수 (collector_geometric.wetted_cg_iters · bare_cg_iters · 수렴 칸 옆)', rc_[0] == 0
        and _int(cg_.get('wetted_cg_iters')) and _int(cg_.get('bare_cg_iters')),
        (rc_[0], {k: cg_.get(k) for k in ('wetted_cg_iters', 'bare_cg_iters')}, rc_[1].strip()[-300:]))
    chk('E7 payload rtol 없음 (옛 꼴) — 반복 수 칸 없음 (매니페스트 · step3 옛 키 그대로)', r0[0] == 0
        and not [k for k in s0 if k.endswith('cg_iters')], sorted(k for k in s0 if 'iters' in k))


# ═════════════════════════ O — 끈 경로 비트 대조 (기반 코드) ═════════════════════════
DRIVER = r'''
import json, sys, contextlib, io
sys.path.insert(0, sys.argv[1])
import numpy as np
import step3_sigma as S3
import ptfe_face_alpha as FA
from scipy.sparse.linalg import spsolve
S3._solve_cg = lambda L, b, *a, **k: (spsolve(L.tocsc(), b), 0)
z = np.load(sys.argv[2])
sid, pid, sig = z['sid'], z['pid'], z['sig']
P, PH, F, K = z['P'], z['PH'], z['F'], z['K']
m4 = PH == 4
caps = FA.build_capsules(P[m4], F[m4], K[m4], dia_law='rope')
fa = FA.build_plan(sid, sig, caps, lo=(0.0, 0.0, 0.0), vox=float(z['vox']), channel='electronic', pid=pid)
with contextlib.redirect_stdout(io.StringIO()):
    r = S3.solve_sigma_z(sid, sig, float(z['vox']), z_top_um=float(sid.shape[2]) * float(z['vox']), z_bot_um=0.0,
                         face_alpha=fa, pid=pid)
out = {'sigma': repr(r['sigma_eff']), 'n_dof': r['n_dof'], 'cg_info': r['cg_info'], 'resid': repr(r['resid']),
       'fa': {k: v for k, v in r['face_alpha'].items() if k != 'plate_cross_columns'}, 'plate': r['face_alpha']['plate_cross_columns']}
print(json.dumps(out, sort_keys=True))
'''


@case('O 끈 경로 비트 대조 (--old-scripts = 기반 커밋 scripts/)')
def t_O():
    if not ARGS.old_scripts:
        print('    (--old-scripts 없음 — 건너뜀 · 커밋 증거는 그 인자로 돌린 기록)')
        return
    old = os.path.abspath(ARGS.old_scripts)
    #  ── (ii) 접합 끔 = face_alpha 만 — 새 코드 ↔ 기반 코드 솔브 비트 같음 (조합 경로가 끈 쪽을 안 건드린다) ──
    addr = fc_rows(('cap1', 'cap3', 'cap2'))
    sid, pid = bed(addr, FC_N)
    npz = os.path.join(TD, 'o_fc.npz')
    np.savez(npz, sid=sid, pid=pid, sig=sig_e(), P=addr[0], PH=addr[1], F=addr[2], K=addr[3], vox=H)
    drv = os.path.join(TD, 'o_driver.py')
    with open(drv, 'w', encoding='utf-8') as f:
        f.write(DRIVER)
    outs = {}
    for nm, sdir in (('old', old), ('new', SCRIPTS)):
        p = subprocess.run([sys.executable, '-I', drv, sdir, npz], capture_output=True, text=True, timeout=300)
        outs[nm] = (p.returncode, p.stdout.strip(), p.stderr[-300:])
    chk('O1 (ii) face_alpha 만 (접합 끔) — 기반 코드 ↔ 새 코드 σ · n_dof · cg_info · resid · face_alpha 기록 비트 같음',
        outs['old'][0] == 0 and outs['new'][0] == 0 and outs['old'][1] == outs['new'][1] and outs['new'][1], outs)
    #  ── payload 매니페스트 · step3 값 — 새 노브 끔 ──
    if ARGS.skip_payload:
        return
    B6 = _b6()
    d = os.path.join(TD, 'op')
    os.makedirs(d)
    B6.make_fixture(d, sdcp=True)
    du = os.path.join(TD, 'op_svu')                        # ★ 10-25 묶음 B (결정 11) — 못 가른 덩어리 1 (위 끝 풀이 기록)
    os.makedirs(du)
    B6.make_fixture_sv_unsplit(du, 6.5)
    SVF, RT = ['--step3-cjunc-sv-cf'], ['--step3-rtol', '1e-12']
    #  새 기록 칸 (설계 · 브리프 항목 4 · 5) — 증서 켠 런의 반복 수 · face_alpha 런의 sid_off.  이것 말고는 바이트 같아야 한다.
    NEW_S3 = ('cg_iters', 'ion_cg_iters')
    for nm, dd, extra, allow in (('off LEAN2', d, B6.OFF + B6.LEAN2, ()),
                                 ('centerline LEAN2', d, ['--ptfe-stamp', 'centerline'] + B6.LEAN2, ()),
                                 ('off LEAN3', d, B6.OFF + B6.LEAN3, ()),
                                 ('off LEAN2 + 접합 (정량)', d, B6.OFF + B6.LEAN2 + B6.CJ, ()),
                                 ('off LEAN2 + rtol', d, B6.OFF + B6.LEAN2 + RT, ('iters',)),
                                 ('face_alpha LEAN2 + rtol', d, ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2 + RT, ('iters', 'sid_off')),
                                 #  ★ 10-25 묶음 B (결정 11) SV 켬 꼴 셋 (b6 B 와 같은 꼴)
                                 ('off LEAN2 + 접합 + SV (rtol 없음)', d, B6.OFF + B6.LEAN2 + B6.CJ + SVF, ()),
                                 ('off LEAN2 + 접합 + SV + rtol', d, B6.OFF + B6.LEAN2 + B6.CJ + SVF + RT, ('iters',)),
                                 ('두 섬유 덩어리 + 접합 + SV + rtol', du, B6.OFF + B6.LEAN2 + B6.CJ + SVF + RT, ('iters',))):
        ro = B6.run_payload(dd, extra, out=f'old_{len(nm)}_{sum(map(ord, nm)) % 99991}.json',
                            payload=os.path.join(old, 'mpm_webapp_payload.py'))
        rn = B6.run_payload(dd, extra, out=f'new_{len(nm)}_{sum(map(ord, nm)) % 99991}.json')
        sn = {k: v for k, v in B6.s3_of(rn[2]).items() if k != 'manifest'}
        if 'iters' not in allow:
            chk(f'O2 [{nm}] 새 기록 칸 없음 (반복 수 · sid_off 는 켠 노브에서만)', not [k for k in sn if k in NEW_S3],
                sorted(k for k in sn if k in NEW_S3))
        #  ★ 10-21 (D · 브리프 묶음 5) — 옛 판은 Z3 새 칸을 새 쪽에서만 빼서 Z3 이전 기반에서만 맞았다 → b6 의 한 표 (OLD_DIFF_ALLOW ·
        #    켠 노브 표지의 칸만 · 끈 경우 차이 0) · --expect-identical (바로 앞 기반) = 차이 0
        diffs = B6.old_tree_diff(B6.payload_tree(ro[2]), B6.payload_tree(rn[2]))
        tags = B6.case_tags(extra)
        probs, seen = B6.old_diff_problems(diffs, tags, expect_identical=bool(getattr(ARGS, 'expect_identical', False)))
        chk(f'O2 payload [{nm}] — 기반 ↔ 새: 차이가 허용 목록 (경우 표지 {sorted(tags) or "끔"}) 안'
            + (' · --expect-identical = 차이 0' if getattr(ARGS, 'expect_identical', False)
               else f' · 허용된 칸 {len(seen)} (세대 {sorted({g for g, _o, _p in seen}) or "-"})'),
            ro[0] == 0 and rn[0] == 0 and not probs, (ro[0], rn[0], probs[:6]))


def main():
    global S3, CJ, FA, CW, RC, ARGS, TD
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: A,B)')
    ap.add_argument('--skip-payload', action='store_true', help='payload · 러너 끝-끝 빼고')
    ap.add_argument('--old-scripts', default='', help='O 묶음 — 기반 커밋 scripts/ 사본 (사본 옆에 docs/ 링크)')
    ap.add_argument('--expect-identical', action='store_true',
                    help='O 묶음 — 허용 목록 (test_ca_ext_b6.OLD_DIFF_ALLOW) 을 쓰지 않고 차이 0 만 통과 (기반 = 바로 앞 커밋)')
    ap.add_argument('--keep', action='store_true')
    ARGS = ap.parse_args()
    import step3_sigma as _s3
    import carbon_junction as _cj
    import ptfe_face_alpha as _fa
    import ca_ext_cjunc as _cw
    import run_contract as _rc
    S3, CJ, FA, CW, RC = _s3, _cj, _fa, _cw, _rc
    TD = tempfile.mkdtemp(prefix='ca_ext_z3_')
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    import time
    t0 = time.time()
    try:
        for tag, fn in CASES:
            if only and not any(tag.startswith(o) for o in only):
                continue
            print(f'\n── {tag}')
            try:
                fn()
            except Exception as e:                          # noqa: BLE001 — 옛 코드 (API 없음) 도 시험 단위로 기록
                import traceback
                chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e} @ {traceback.format_exc().splitlines()[-3].strip()[:200]}')
    finally:
        if ARGS.keep:
            print(f'\n  (임시 디렉터리 남김: {TD})')
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\ntest_ca_ext_z3: {_ok} PASS · {len(_fail)} FAIL ({time.time() - t0:.1f} s)')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
