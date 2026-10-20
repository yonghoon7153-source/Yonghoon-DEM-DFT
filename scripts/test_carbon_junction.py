#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② S2 탄소 접합 R_j v0 (VGCF–VGCF) + S3 SDCP 접합 수정자 — 시험 먼저 (규율 ② · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §4 · §5 (+ 계약 v2 §3-8 J1–J8 · v3 §5 J2a–J12 · v3.1) ·
1저자 10-20 N1–N18 = 권고대로.  ⚠ 이 시험의 PASS 는 **계약 · 구현의 증거**이지 R_j 값 · 판정 (R) 의 증거가 아니다.
기대값은 **모듈 밖에서** 손으로 세운 회로 (직렬 사슬 · 사다리) 를 직접 풀어 만든다 — 같은 함수로 정답을 다시 만들지 않는다.

  python3 scripts/test_carbon_junction.py            # 현 구현
  python3 scripts/test_carbon_junction.py --quick    # 끔 비트 동일 (C0) 의 무작위 침대 수를 줄인다

픽스처 단위: h = 1 µm · r_f = 0.5 µm (섬유 지름 = 1 복셀 — 생산 Ø0.15 @ vox 0.15 와 같은 비) · tol_ff = 0.1 · L_par = 2(r_fi + r_fj) = 2.0 ·
r_port = 2.0 (= 2h) · gap_tol 2.0 · σ_VGCF = 100 S/cm → 축방향 면 g = σ·h = 100 · 판 결합 g = σ·h²/(h/2) = 200 (코드 단위 S/cm·µm) ·
접합 간선 g = 1e4/R_j (설계 §4-1 J5).

묶음 (설계 §4-4 · §5-4 · 브리프 B):
  C0     끔 = 옛 경로 비트 동일 (기준 = 커밋 d1768cf0c 의 step3_sigma · 무작위 침대 16 입력 · σ · φ · n_dof · cg_info · resid · sid)
  C1     cross_shared — 판 ↔ A ↔ 교차 셀 (멤버십 dof 둘) ↔ B ↔ 판 = 해석 직렬 사슬 (1e-12) · R_j 스윕 Rayleigh 단조
  T1-7   R_j → 0 = 축약 그래프 (C1 = 옛 융합 · C2a = 포트 병합 회로) · R_j = ∞ = 가닥 사이 전류 0 · 가닥 안 연속
  C2     cross_face (옛 융합 면 절단 + 간선 하나) · cross_edge (옛 단절 → 접합으로 연결 · 가지치기가 안 지움 = J12)
  C3     pass_through — 교차 셀을 지나는 가닥은 R_j 와 무관 (J6 · J12)
  C4     series_chain — R = 기저 + (N−1)·R_j (기울기 정확) · 단위 변이 (1e4 빠짐 · ×1e8) 실패
  C5     instance — 같은 접촉을 조각 더 잘게 · 섬유 순서 · 점 역순 = instance 수 · σ 불변 (J2c) · 같은 쌍 두 곳 = instance 둘
  T1-6   junction_multi — 두 자리 사다리 회로 (1e-12) · 등전위 극한 R → R_j/2
  T1-8   crossing_k3 / J9 — 한 셀 세 가닥 → dof 셋 · instance 셋 · 포트 dof 서로 다름
  T1-9   fiber_sphere_threshold (J2b) — r_f 0.075 · R_AM 2 · d 2.12 µm = 접촉 아님 (문자식 2.15 오판 아님)
  T1-10  self_contact — 같은 fid 비연속 두 셀 면 → 자기 접합 instance 하나 · 0 저항 지름길 없음
  T1-11  port_tie — 등거리 두 후보 → 정준 방향 경로 번호가 작은 셀 · 동률 수 · 점 역순 · 섬유 순서에 σ 불변
  T1-12  site_cut — 같은 쌍 두 자리 중 한 자리만 instance → 그 발자국 면만 절단 · 다른 자리 = 미등록 법칙 (cut ≤ fused)
  T1-5′  lead_reference — 단자 기준 R_j · 리드 빼기 · 음수 = 거부 (v0 = 모형 내부값만)
  J8     long_contact — 긴 평행 접촉 = 정량 거부 · 시험 모드 = 기록
  J11    electrode_short — 축약 무리가 두 판에 다 닿으면 단락 상태 (유한 σ 로 위장하지 않는다)
  C6     energy — Σ P (면 + 접합 + 판) = I·ΔV · 접합 몫 = −∂lnσ/∂lnR_j (중심 FD)
  C8     guards — r1 · ①′ · 주기 · return_field · 다른 vox · sid · 계획 · 원장 변조 · NaN · 길이 불일치 · 떨어진 같은 fid · kind 없음 ·
         VGCF 절연 채널 · 법칙 미선언 · R_j 극한 → 조립 전 거부 (CG 호출 0)
  P-1/2  PTFE–접합 법칙 — P1 = 덮인 instance 만 절단 · P0 = 영향 없음 · 경계 = 정확히 tol_P 포함 · centerline + P1 = 거부 ·
         (P1, c = 1) = 절단 먼저 (N18)
  S3-1…11 SDCP 접합 수정자 (c = 0 비트 같음 · SBE no-op · c 단조 · c = 1 축약 · 순열 · 경계 · 펠릿 no-op · 변이 · S2 없이 거부 ·
         sid 불변 · 우선순위)
  SV     SV 면 · SDCP 셀 소산 몫 · SV_DOMINANT 표지 · SDCP 경유 섬유 연결 수
  PIECE  멤버십 셀 = `_fibre_segment_ijk` 의 VGCF 셀 (같은 끊기 규칙 · 복제 + 동등 시험)
"""
import argparse
import contextlib
import importlib.util
import io
import math
import os
import subprocess
import sys
import tempfile

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

BASE_COMMIT = 'd1768cf0c'          # 끔 비트 동일의 기준 (이 묶음 전 원격 HEAD)

S3 = None
CJ = None
QUICK = False
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return bool(cond)


CASES = []


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


_CG_CALLS = [0]


@contextlib.contextmanager
def direct_solver():
    """작은 픽스처 = 직접 풀이 (기계 정밀도) — 조립 · 항등식을 CG 허용오차 없이 본다.  생산 경로 아님."""
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg

    def _direct(L, b, *a, **k):
        _CG_CALLS[0] += 1
        return spsolve(L.tocsc(), b), 0
    S3._solve_cg = _direct
    try:
        yield
    finally:
        S3._solve_cg = old


def raises(fn, exc=(ValueError, TypeError)):
    try:
        quiet(fn)
    except exc:
        return True
    except Exception:                                      # noqa: BLE001 — 다른 예외 = 거부 계약 위반
        return False
    return False


# ═════════════════════════ 픽스처 도구 ═════════════════════════
H = 1.0
RF = 0.5
TOL = 0.1
LPAR = 2.0 * (RF + RF)
RPORT = 2.0
SV = 100.0                       # σ_VGCF (S/cm)
G_AX = SV * H                    # 축방향 면 g (코드 단위)
G_PL = SV * H * H / (0.5 * H)    # 판 결합 g (셀 중심이 판에서 h/2)


def sig_e(s_vgcf=SV, s_am=0.010, s_sdcp=250.0):
    return S3.electronic_sigma_table(s_am, s_am * 0.5, s_vgcf, 10.0, s_sdcp)


def densify(verts, step=0.25):
    """꼭짓점 폴리라인 → 간격 ≤ step 인 점열 (끊기 규칙 gap_tol·중앙값 에 걸리지 않게 거의 고른 간격)."""
    V = np.asarray(verts, np.float64)
    out = [V[0]]
    for a, b in zip(V[:-1], V[1:]):
        n = max(1, int(math.ceil(np.linalg.norm(b - a) / step - 1e-12)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * (i / n))
    return np.asarray(out)


def rows(polys, phase=2, kind=1, fid0=10, fid_step=10, step=0.25, fids=None):
    """폴리라인들 → (add_pts, add_phase, add_fid, add_kind) — fid 마다 행이 붙어 있다 (생산 규약)."""
    P, PH, F, K = [], [], [], []
    for i, v in enumerate(polys):
        pts = densify(v, step) if len(v) > 1 else np.asarray(v, np.float64)
        f = fids[i] if fids is not None else fid0 + fid_step * i
        P.append(pts); PH.append(np.full(len(pts), phase)); F.append(np.full(len(pts), f)); K.append(np.full(len(pts), kind))
    return (np.vstack(P), np.concatenate(PH).astype(np.int64), np.concatenate(F).astype(np.int64),
            np.concatenate(K).astype(np.int64))


def cat_rows(*rs):
    return tuple(np.concatenate([r[i] for r in rs]) for i in range(4))


NO_AM = (np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64))


def bed(addr, n, am=NO_AM, stamp=None, vox=H, **kw):
    """격자 (sid, pid) — 생산 `rasterize` (선분 스탬프).  stamp = 스탬프할 행 마스크 (None = 전부) — face_alpha 침대는 PTFE 를 뺀다."""
    P, PH, F, K = addr
    m = np.ones(len(P), bool) if stamp is None else stamp
    lo = (0.0, 0.0, 0.0)
    hi = tuple(float(x) * vox for x in n)
    sid, pid = S3.rasterize(am[0], am[1], am[2], P[m], PH[m], lo, hi, vox, add_fid=F[m], add_kind=K[m], **kw)
    return sid, pid


def registry(sid, addr, vox=H, **kw):
    P, PH, F, K = addr
    k = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0)
    k.update(kw)
    return quiet(CJ.cjunc_registry, sid, (0.0, 0.0, 0.0), vox, P, PH, F, K, **k)


def plan(reg, rj, **kw):
    k = dict(unreg_law='cut', ptfe_stamp='off')
    k.update(kw)
    return CJ.cjunc_plan(reg, rj, **k)


def solve(sid, sig, n, cj=None, vox=H, **kw):
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(n[2]) * vox, z_bot_um=0.0, cjunc=cj, **kw)


def solve_legacy(sid, sig, n, vox=H, **kw):
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(n[2]) * vox, z_bot_um=0.0, **kw)


def I_of(res, n, vox=H):
    """해 → 단자 전류 (코드 단위 · ΔV = 1) = σ_eff · A / L."""
    zb, zt = res['plate_z_um']
    return res['sigma_eff'] * (n[0] * n[1] * vox * vox) / (zt - zb)


def chain_I(gs):
    return 1.0 / sum(1.0 / g for g in gs)


def ref_I(nn, edges, bot, top):
    """손으로 세운 회로 (독립 기준) — 노드 nn 개 · edges = [(i, j, g)] · bot/top = [(i, g)] · ΔV = 1 → 아래 판 전류."""
    L = np.zeros((nn, nn)); b = np.zeros(nn)
    for i, j, g in edges:
        L[i, i] += g; L[j, j] += g; L[i, j] -= g; L[j, i] -= g
    for i, g in bot:
        L[i, i] += g; b[i] += g
    for i, g in top:
        L[i, i] += g
    phi = np.linalg.solve(L, b)
    return float(sum(g * (1.0 - phi[i]) for i, g in bot))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def rjc(rj):
    """R_j [Ω] → 코드 단위 저항 (1/g · g = 1e4/R_j)."""
    return rj / 1.0e4


# ── 픽스처 정의 (꼭짓점 = 셀 중심 · µm) ──
#  F1 cross_shared: A 위로 (1,1,0..3) 끝 · B 는 A 끝점에서 +x 로 (1..4,1,3) 뒤 +z 로 (4,1,4..7) → 교차 셀 (1,1,3) = 멤버십 둘
F1_N = (6, 3, 8)
F1 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)],
      [(1.5, 1.5, 3.5), (4.5, 1.5, 3.5), (4.5, 1.5, 7.5)]]
F1_I = lambda rj: chain_I([G_PL] + [G_AX] * 3 + ([1e4 / rj] if rj != 0 else []) + [G_AX] * 7 + [G_PL])   # noqa: E731
#  F2 cross_face: A (1,1,0..3) · B (2,1,3..7) — A 끝 ↔ B 시작 중심선 거리 1.0 (= r_A + r_B) · 면 (1,1,3)|(2,1,3)
F2_N = (5, 3, 8)
F2 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(2.5, 1.5, 3.5), (2.5, 1.5, 7.5)]]
#  F3 cross_edge: A 기둥 (1,1) · B 기둥 (2,2) — 모서리 인접 (옛 단절) · 중심선 거리 0.1414
F3_N = (4, 4, 8)
F3 = [[(1.95, 1.95, 0.5), (1.95, 1.95, 3.5)], [(2.05, 2.05, 3.5), (2.05, 2.05, 7.5)]]
#  F4 pass_through: A 전 높이 (1,1,0..7) · B 가로 (0..4,1,3) 가 교차 셀 (1,1,3) 을 지난다 (B = 매달린 가지)
F4_N = (6, 3, 8)
F4 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)], [(0.5, 1.5, 3.5), (4.5, 1.5, 3.5)]]
#  F5 series: A (1,1,0..2) → B (2,2,2..4) → C (1,1,4..7) — 접합 둘 (모서리 인접 끝–끝)
F5_N = (4, 4, 8)
F5 = [[(1.95, 1.95, 0.5), (1.95, 1.95, 2.5)], [(2.05, 2.05, 2.5), (2.05, 2.05, 4.5)],
      [(1.95, 1.95, 4.5), (1.95, 1.95, 7.5)]]
#  F6 two_sites: A (1,1,0..4) 아래 판 · B 는 (2,1,1) 에서 A 에 닿고 돌아 (2,1,4) 에서 다시 닿은 뒤 위로 (2,1,4..8) 위 판
F6_N = (6, 3, 9)
F6 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)],
      [(2.5, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 4.5), (2.5, 1.5, 4.5), (2.5, 1.5, 8.5)]]
#  F10 site_cut: F6 의 둘째 자리를 x 2.9 로 — 셀은 면 인접 (2,1,4)|(1,1,4) 인데 중심선 거리 1.4 > 1.1 (미등록)
F10 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)],
       [(2.5, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 4.5), (2.9, 1.5, 4.5), (2.9, 1.5, 8.5)]]


def seq_cells(verts, vox=H):
    """폴리라인 → 셀 열 (연속 중복 제거) — 기대 회로를 세우는 독립 도구 (생산 스탬프와 같은 원시 함수 `segment_cells`)."""
    from fibre_segment_raster import segment_cells
    pts = densify(verts)
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool)
    keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


# ═════════════════════════ C0 — 끔 비트 동일 ═════════════════════════
def _load_base():
    try:
        src = subprocess.run(['git', '-C', ROOT, 'show', f'{BASE_COMMIT}:scripts/step3_sigma.py'],
                             capture_output=True, check=True).stdout
    except Exception as e:                                 # noqa: BLE001
        return None, f'git show 실패 {type(e).__name__}: {e}'
    d = tempfile.mkdtemp(prefix='s3base_')
    p = os.path.join(d, 'step3_sigma_base_d1768.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('step3_sigma_base_d1768', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, ''


def _random_bed(seed, mod, vox=0.25, n=(24, 24, 32)):
    rng = np.random.default_rng(seed)
    box = np.array(n, float) * vox
    na = int(rng.integers(5, 10))
    am_c = rng.uniform([0.5, 0.5, 0.5], box - 0.5, (na, 3)); am_r = rng.uniform(0.7, 1.4, na)
    am_t = rng.integers(1, 3, na)
    polys, ph = [], []
    for _ in range(int(rng.integers(4, 8))):                       # VGCF 경로
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        p1 = np.clip(p0 + d * rng.uniform(2.0, 5.0), 0.05, box - 0.05)
        polys.append([p0, p1]); ph.append(2)
    for _ in range(2):                                              # PTFE 경로 (centerline 스탬프)
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        polys.append([p0, np.clip(p0 + 3.0 * d, 0.05, box - 0.05)]); ph.append(4)
    P, PH, F, K = [], [], [], []
    for i, (v, p) in enumerate(zip(polys, ph)):
        pts = densify(v, 0.1)
        P.append(pts); PH.append(np.full(len(pts), p)); F.append(np.full(len(pts), 100 + i)); K.append(np.full(len(pts), 1))
    sd = rng.uniform(0.2, box - 0.2, (int(rng.integers(10, 30)), 3))    # SDCP 점 (구 스탬프)
    P.append(sd); PH.append(np.full(len(sd), 5)); F.append(np.arange(len(sd)) + 500); K.append(np.zeros(len(sd), int))
    P = np.vstack(P); PH = np.concatenate(PH); F = np.concatenate(F); K = np.concatenate(K)
    se = rng.uniform(0, box, (4000, 3))
    sid, pid = mod.rasterize(am_c, am_r, am_t, P, PH, (0., 0., 0.), tuple(box), vox, se_pts=se,
                             sdcp_sphere_d_um=0.5, add_fid=F, add_kind=K, bridge_um=0.3)
    return sid, pid, box


@case('C0')
def t_c0_off_bitid():
    base, why = _load_base()
    if not chk('C0 기준 모듈 (커밋 d1768cf0c 의 step3_sigma) 을 읽었다', base is not None, why):
        return
    nbed = 4 if QUICK else 8
    allsame, n_in = True, 0
    for s in range(nbed):
        sid_b, pid_b, box = quiet(_random_bed, 1000 + s, base)
        sid_c, pid_c, _ = quiet(_random_bed, 1000 + s, S3)
        same_raster = sid_b.tobytes() == sid_c.tobytes() and pid_b.tobytes() == pid_c.tobytes()
        allsame &= same_raster
        te_b = base.electronic_sigma_table(0.010, 0.005, 100.0, 10.0, 250.0)
        ti_b = base.ionic_sigma_table(0.3e-3, 3.0e-3)
        for tab, per in ((te_b, False), (ti_b, False) if s % 2 == 0 else (te_b, True)):
            n_in += 1
            rb = quiet(base.solve_sigma_z, sid_b, tab, 0.25, return_field=True, z_top_um=float(box[2]), z_bot_um=0.0,
                       periodic_xy=per)
            rc = quiet(S3.solve_sigma_z, sid_c, tab, 0.25, return_field=True, z_top_um=float(box[2]), z_bot_um=0.0,
                       periodic_xy=per)
            same = (np.float64(rb['sigma_eff']).tobytes() == np.float64(rc['sigma_eff']).tobytes()
                    and rb['n_dof'] == rc['n_dof'] and rb.get('cg_info') == rc.get('cg_info')
                    and np.float64(rb.get('resid', 0.0)).tobytes() == np.float64(rc.get('resid', 0.0)).tobytes()
                    and (('phi' not in rb and 'phi' not in rc) or rb['phi'].tobytes() == rc['phi'].tobytes())
                    and sorted(rb) == sorted(rc))
            if not same:
                print(f'    C0 차이 seed {1000 + s} per {per}: σ {rb["sigma_eff"]!r} ↔ {rc["sigma_eff"]!r} · '
                      f'키 {sorted(set(rb) ^ set(rc))}')
            allsame &= same
    chk(f'C0 끔 (cjunc=None · 수렴 증서 끔) = 옛 경로 비트 동일 — raster · σ · φ · n_dof · cg_info · resid · 결과 키 ({n_in} 입력)',
        allsame)


# ═════════════════════════ PIECE — 멤버십 셀 = 생산 스탬프 셀 ═════════════════════════
@case('PIECE')
def t_piece():
    rng = np.random.default_rng(7)
    allok = True
    for trial in range(12):
        n = (16, 16, 16); box = np.array(n, float) * 0.5
        polys = []
        for _ in range(5):
            p = [rng.uniform(1, box - 1)]
            for _ in range(int(rng.integers(1, 5))):
                d = rng.normal(size=3); d /= np.linalg.norm(d)
                p.append(np.clip(p[-1] + d * rng.uniform(0.5, 2.5), 0.01, box - 0.01))
            polys.append(p)
        P, PH, F, K = rows(polys, step=0.12)
        if trial % 3 == 0:                                  # 끊기 (gap) 가 걸리는 경로 하나
            m = F == F[0]
            idx = np.flatnonzero(m)
            if len(idx) > 6:
                keep = np.ones(len(P), bool); keep[idx[2:4]] = False
                P, PH, F, K = P[keep], PH[keep], F[keep], K[keep]
        sid, _ = S3.rasterize(*NO_AM, P, PH, (0., 0., 0.), tuple(box), 0.5, add_fid=F, add_kind=K)
        ijk, ph = S3._fibre_segment_ijk(P, PH, F, np.zeros(3), 0.5, np.array(n), 2.0, add_kind=K)
        want = {tuple(c) for c in ijk[ph == 2]}
        try:
            reg = quiet(CJ.cjunc_registry, sid, (0., 0., 0.), 0.5, P, PH, F, K, r_f_um=0.25, tol_ff_um=0.05,
                        L_par_um=1.0, r_port_um=1.0, gap_tol=2.0)
            pos = reg['positions']
            inb = pos['lin'] >= 0
            got = {tuple(int(v) for v in np.unravel_index(int(l), n)) for l in pos['lin'][inb]}
        except Exception as e:                             # noqa: BLE001
            got = None
            print(f'    PIECE trial {trial}: {type(e).__name__}: {e}')
        allok &= (got == want)
    chk('PIECE 멤버십 셀 (상자 안 위치 전부) = `_fibre_segment_ijk` 의 VGCF 셀 (12 무작위 · 끊기 포함 · 같은 끊기 규칙)', allok)


# ═════════════════════════ C1 · T1-7 ═════════════════════════
@case('C1')
def t_c1_cross_shared():
    P = rows(F1)
    sid, _ = bed(P, F1_N)
    reg = registry(sid, P)
    inst = reg['instances']
    chk('C1 instance 하나 (A–B · 교차 셀) · 교차 셀 = 멤버십 둘 (추가 dof 1)',
        len(inst['fi']) == 1 and reg['n_extra_dofs'] == 1, f"n {len(inst['fi'])} extra {reg['n_extra_dofs']}")
    errs, Is = [], []
    for rj in (1.0e1, 1.0e3, 1.0e5):
        r = solve(sid, sig_e(), F1_N, plan(reg, rj))
        Is.append(I_of(r, F1_N)); errs.append(rel(Is[-1], F1_I(rj)))
    chk('C1 σ = 해석 직렬 사슬 판 + A 3 면 + R_j + B 7 면 + 판 (R_j 10 · 1e3 · 1e5 Ω · 1e-12)', max(errs) < 1e-12, f'{errs}')
    chk('C1 Rayleigh — R_j 가 커지면 σ 엄격히 줄어든다 (같은 그래프)', Is[0] > Is[1] > Is[2], f'{Is}')
    pe = r['plate_edges']
    chk('C1 판 간선 원장 = 남은 결합만 (좌표 · g 길이 같음 · 해의 판 전류와 같은 계)',
        all(len(pe[s][0][0]) == len(pe[s][1]) for s in ('bot', 'top')) and r['cjunc']['solved'] is True)
    r0 = solve(sid, sig_e(), F1_N, plan(reg, 0.0, allow_rj_limits=True))
    rl = solve_legacy(sid, sig_e(), F1_N)
    chk('T1-7 R_j → 0 (축약) = 축약 그래프 = 옛 융합 교차 셀 (1e-12)', rel(I_of(r0, F1_N), I_of(rl, F1_N)) < 1e-12
        and rel(I_of(r0, F1_N), F1_I(0)) < 1e-12, f'{I_of(r0, F1_N)} ↔ {I_of(rl, F1_N)}')
    ri = solve(sid, sig_e(), F1_N, plan(reg, math.inf, allow_rj_limits=True))
    chk('T1-7 R_j = ∞ → 가닥 사이 전류 0 (A–B 가 접합으로만 이어진다 → 관통 없음)',
        ri['sigma_eff'] == 0.0 and ri.get('reason') == 'no_through_component', f"{ri.get('reason')} σ {ri['sigma_eff']}")


@case('C2')
def t_c2_face_edge():
    P = rows(F2)
    sid, _ = bed(P, F2_N)
    reg = registry(sid, P)
    rj = 2.0e3
    r = solve(sid, sig_e(), F2_N, plan(reg, rj))
    want = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    chk('C2a cross_face — 옛 융합 면 절단 + 접합 간선 하나 (해석 사슬 1e-12)', rel(I_of(r, F2_N), want) < 1e-12,
        f'{I_of(r, F2_N)} ↔ {want}')
    rl = solve_legacy(sid, sig_e(), F2_N)
    chk('C2a 옛 경로 = 융합 면 g (대조 · 다른 값)', rel(I_of(rl, F2_N), chain_I([G_PL] + [G_AX] * 8 + [G_PL])) < 1e-12)
    r0 = solve(sid, sig_e(), F2_N, plan(reg, 0.0, allow_rj_limits=True))
    want0 = chain_I([G_PL] + [G_AX] * 3 + [G_AX] * 4 + [G_PL])          # 포트 두 dof 병합 = 그 면이 사라진 사슬
    chk('T1-7 R_j → 0 = 포트 병합 회로 (옛 융합보다 강하다 · 1e-12)', rel(I_of(r0, F2_N), want0) < 1e-12,
        f'{I_of(r0, F2_N)} ↔ {want0}')
    P3 = rows(F3)
    sid3, _ = bed(P3, F3_N)
    reg3 = registry(sid3, P3)
    r3 = solve(sid3, sig_e(), F3_N, plan(reg3, rj))
    rl3 = solve_legacy(sid3, sig_e(), F3_N)
    want3 = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    chk('C2b cross_edge — 옛 경로 단절 (관통 없음)', rl3['sigma_eff'] == 0.0)
    chk('C2b · J12 접합으로만 이어진 성분을 가지치기가 안 지운다 (해석 사슬 1e-12)', rel(I_of(r3, F3_N), want3) < 1e-12,
        f'{I_of(r3, F3_N)} ↔ {want3}')


@case('C3')
def t_c3_pass_through():
    P = rows(F4)
    sid, _ = bed(P, F4_N)
    reg = registry(sid, P)
    want = chain_I([G_PL] + [G_AX] * 7 + [G_PL])
    Is = [I_of(solve(sid, sig_e(), F4_N, plan(reg, rj, allow_rj_limits=True)), F4_N) for rj in (10.0, 1.0e5, math.inf)]
    chk('C3 · J6 교차 셀을 지나는 가닥 A 는 R_j 와 무관 · R_j = ∞ 에서도 연속 (1e-12)', max(rel(x, want) for x in Is) < 1e-12,
        f'{Is} ↔ {want}')
    chk('C3 교차 셀 = dof 둘 (A · B 각자 축방향 연결)', reg['n_extra_dofs'] == 1, f"{reg['n_extra_dofs']}")


@case('C4')
def t_c4_series_units():
    P = rows(F5)
    sid, _ = bed(P, F5_N)
    reg = registry(sid, P)
    base = [G_PL] + [G_AX] * 2 + [G_AX] * 2 + [G_AX] * 3 + [G_PL]
    rA, rB = 1.0e3, 5.0e3
    IA = I_of(solve(sid, sig_e(), F5_N, plan(reg, rA)), F5_N)
    IB = I_of(solve(sid, sig_e(), F5_N, plan(reg, rB)), F5_N)
    wA = chain_I(base + [1e4 / rA] * 2); wB = chain_I(base + [1e4 / rB] * 2)
    chk('C4 series_chain N = 3 · 접합 둘 — 해석 (1e-12) · 기울기 dR/dR_j = N − 1', rel(IA, wA) < 1e-12 and rel(IB, wB) < 1e-12
        and abs(((1 / IB - 1 / IA) / (rjc(rB) - rjc(rA))) - 2.0) < 1e-9, f'{IA} {wA} · {IB} {wB}')
    old = CJ.junction_g_code
    detected = []
    for nm, fn in (('1e4 빠짐', lambda r: 1.0 / r), ('×1e8', lambda r: 1.0e12 / r)):
        CJ.junction_g_code = fn
        try:
            Im = I_of(solve(sid, sig_e(), F5_N, plan(reg, rA)), F5_N)
            detected.append(rel(Im, wA) > 1e-6)
        except Exception:                                  # noqa: BLE001
            detected.append(True)
        finally:
            CJ.junction_g_code = old
    chk('C4 단위 변이 (1e4 빠짐 · ×1e8) 를 해석 대조가 잡는다', all(detected), f'{detected}')


@case('C5')
def t_c5_instances():
    P = rows(F5)
    sid, _ = bed(P, F5_N)
    reg = registry(sid, P)
    I0 = I_of(solve(sid, sig_e(), F5_N, plan(reg, 1e3)), F5_N)
    Pf = rows(F5, step=0.11)                                       # 같은 접촉을 더 잘게 (조각 수 ↑)
    sidf, _ = bed(Pf, F5_N)
    regf = registry(sidf, Pf)
    If = I_of(solve(sidf, sig_e(), F5_N, plan(regf, 1e3)), F5_N)
    chk('C5 · J2c 조각을 잘게 해도 instance 수 · σ 같다', len(regf['instances']['fi']) == len(reg['instances']['fi']) == 2
        and rel(If, I0) < 1e-12 and sidf.tobytes() == sid.tobytes(), f"{len(regf['instances']['fi'])} {If} {I0}")
    Pr = rows([F5[2], F5[0], F5[1]], fids=[30, 10, 20])            # 섬유 순서 바꿈 (fid 그대로)
    sidr, _ = bed(Pr, F5_N)
    regr = registry(sidr, Pr)
    Ir = I_of(solve(sidr, sig_e(), F5_N, plan(regr, 1e3)), F5_N)
    Pv = rows([v[::-1] for v in F5])                               # 점 역순
    sidv, _ = bed(Pv, F5_N)
    regv = registry(sidv, Pv)
    Iv = I_of(solve(sidv, sig_e(), F5_N, plan(regv, 1e3)), F5_N)
    chk('C5 · J2c 섬유 순서 · 점 역순에 instance 수 · σ 불변 (1e-12)',
        len(regr['instances']['fi']) == 2 and len(regv['instances']['fi']) == 2 and rel(Ir, I0) < 1e-12 and rel(Iv, I0) < 1e-12,
        f'{Ir} {Iv} {I0}')
    P6 = rows(F6)
    sid6, _ = bed(P6, F6_N)
    reg6 = registry(sid6, P6)
    chk('C5 같은 쌍 떨어진 두 곳 = instance 둘 (쌍 ID 로 접지 않는다)', len(reg6['instances']['fi']) == 2
        and len(set(zip(reg6['instances']['fi'].tolist(), reg6['instances']['fj'].tolist()))) == 1, f"{reg6['instances']['fi']}")


def _f6_reference(rj, sv=SV, second_site=True, fused_second=False):
    """F6/F10 사다리 — 노드: A (1,1,0..4) = 0..4 · B 셀 열 = 5.. · 접합 자리 1: A1 ↔ B0 · 자리 2: A4 ↔ B (2,1,4)."""
    A = [(1, 1, k) for k in range(5)]
    Bc = seq_cells(F6[1] if not fused_second else F10[1])
    nA = len(A)
    gax = sv * H; gpl = sv * H * H / (0.5 * H)
    E = [(i, i + 1, gax) for i in range(nA - 1)] + [(nA + i, nA + i + 1, gax) for i in range(len(Bc) - 1)]
    jB0 = nA + Bc.index((2, 1, 1)); jB4 = nA + Bc.index((2, 1, 4))
    E.append((1, jB0, 1e4 / rj))
    if second_site:
        E.append((4, jB4, gax if fused_second else 1e4 / rj))
    bot = [(0, gpl)]; top = [(nA + len(Bc) - 1, gpl)]
    return ref_I(nA + len(Bc), E, bot, top)


@case('T1-6')
def t_t16_multi():
    P = rows(F6)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    rj = 3.0e3
    r6 = solve(sid, sig_e(), F6_N, plan(reg, rj))
    I = I_of(r6, F6_N)
    want = _f6_reference(rj)
    chk('T1-6 두 자리 사다리 회로 (손으로 세운 기준 · 1e-12)', rel(I, want) < 1e-12, f'{I} ↔ {want}')
    jI = r6['_cjunc']['junction_current_code']
    chk('T1-6 원장 — instance 마다 접합 전류 · 두 자리 합 = 단자 전류 (A → B 는 접합으로만 · 1e-10)',
        len(jI) == 2 and np.all(np.isfinite(jI)) and rel(float(np.sum(np.abs(jI))), I) < 1e-10, f'{jI} {I}')
    big = sig_e(s_vgcf=1.0e9)
    Ib = I_of(solve(sid, big, F6_N, plan(reg, rj)), F6_N)
    chk('T1-6 등전위 극한 (σ 1e9) — R → R_j/2 (상대 1e-5)', rel(1.0 / Ib, rjc(rj) / 2.0) < 1e-5, f'{1 / Ib} ↔ {rjc(rj) / 2}')


@case('T1-8')
def t_t18_k3():
    n = (5, 5, 5)
    polys = [[(2.5, 2.5, 0.5), (2.5, 2.5, 4.5)], [(0.5, 2.5, 2.5), (4.5, 2.5, 2.5)], [(2.5, 0.5, 2.5), (2.5, 4.5, 2.5)]]
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    pos = reg['positions']
    ok_ports = True
    for k in range(len(inst['fi'])):
        pi, pj = int(inst['port_i'][k]), int(inst['port_j'][k])
        ok_ports &= (pi >= 0 and pj >= 0 and pi != pj and pos['lin'][pi] == pos['lin'][pj])
    chk('T1-8 한 셀 세 가닥 → 추가 dof 2 · instance 3 (쌍마다) · J9 포트 = 같은 셀 · 서로 다른 dof',
        reg['n_extra_dofs'] == 2 and len(inst['fi']) == 3 and ok_ports, f"extra {reg['n_extra_dofs']} n {len(inst['fi'])}")
    want = chain_I([G_PL] + [G_AX] * 4 + [G_PL])
    Is = [I_of(solve(sid, sig_e(), n, plan(reg, rj, allow_rj_limits=True)), n) for rj in (1.0, 1e6, math.inf)]
    chk('T1-8 축 연결이 각자 fid 로 — 세로 가닥 σ 가 R_j 와 무관 (1e-12)', max(rel(x, want) for x in Is) < 1e-12, f'{Is} {want}')


@case('T1-9')
def t_t19_fiber_sphere():
    P = rows([[(0.0, 0.0, -1.0), (0.0, 0.0, 1.0)]], step=0.1)
    am_c = np.array([[2.12, 0.0, 0.0]]); am_r = np.array([2.0])
    n0 = CJ.va_census(P[0], P[1], P[2], P[3], am_c, am_r, r_f_um=0.075, tol_fs_um=0.0, gap_tol=2.0)
    am_c2 = np.array([[2.07, 0.0, 0.0]])
    n1 = CJ.va_census(P[0], P[1], P[2], P[3], am_c2, am_r, r_f_um=0.075, tol_fs_um=0.0, gap_tol=2.0)
    chk('T1-9 J2b 섬유–구 = 중심선 ↔ 구 중심 ≤ r_f + R_AM + tol_fs — d 2.12 = 접촉 아님 (2.15 문자식 오판 아님) · d 2.07 = 접촉',
        n0 == 0 and n1 == 1, f'{n0} {n1}')


@case('T1-10')
def t_t110_self():
    n = (5, 5, 8)
    poly = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5), (3.5, 1.5, 3.5), (3.5, 1.5, 1.5), (2.5, 1.5, 1.5), (2.5, 3.5, 1.5),
             (2.5, 3.5, 7.5)]]
    P = rows(poly)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    nself = int(np.sum(inst['self']))
    chk('T1-10 같은 fid 비연속 두 셀 면 → 자기 접합 instance (f, f) 하나', nself == 1 and len(inst['fi']) == 1,
        f"self {nself} n {len(inst['fi'])}")
    seq = seq_cells(poly[0])
    k1, k8 = seq.index((1, 1, 1)), seq.index((2, 1, 1))
    rj = 4.0e3
    E = [(i, i + 1, G_AX) for i in range(len(seq) - 1)] + [(k1, k8, 1e4 / rj)]
    want = ref_I(len(seq), E, [(0, G_PL)], [(len(seq) - 1, G_PL)])
    I = I_of(solve(sid, sig_e(), n, plan(reg, rj)), n)
    chk('T1-10 자기 접합 = R_j 간선 (0 저항 지름길 아님 · 사다리 기준 1e-12)', rel(I, want) < 1e-12, f'{I} ↔ {want}')
    Ii = I_of(solve(sid, sig_e(), n, plan(reg, math.inf, allow_rj_limits=True)), n)
    wi = chain_I([G_PL] + [G_AX] * (len(seq) - 1) + [G_PL])
    chk('T1-10 R_j = ∞ → 우회로 전부 (면 지름길 없음 · 1e-12)', rel(Ii, wi) < 1e-12, f'{Ii} ↔ {wi}')


@case('T1-11')
def t_t111_tie():
    #  A 아래 판 (1,1,0..5) · B 는 A 옆 x 2.5 · z = 3.0 (셀 경계) 에서 시작해 +x 뒤 위 판 — A 의 접점 (1.5,1.5,3.0) 은 A 의 두 셀
    #  (1,1,2) · (1,1,3) 중심에서 등거리 (0.5) → 동률.  B 가 전류를 나르므로 어느 포트냐가 회로를 바꾼다 (판별력).
    n = (6, 3, 8)
    polys = [[(1.5, 1.5, 0.5), (1.5, 1.5, 5.5)], [(2.5, 1.5, 3.0), (4.5, 1.5, 3.0), (4.5, 1.5, 7.5)]]
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    inst = reg['instances']
    pos = reg['positions']
    ok = len(inst['fi']) == 1
    tie = int(reg['census'].get('n_port_ties', -1))
    pa = int(inst['port_i'][0]) if ok else -1
    cell = tuple(int(v) for v in np.unravel_index(int(pos['lin'][pa]), n)) if pa >= 0 else None
    chk('T1-11 등거리 두 후보 포트 → 정준 방향 경로 번호가 작은 셀 (1,1,2) · 동률 수 1 기록', ok and tie == 1 and cell == (1, 1, 2),
        f'tie {tie} cell {cell}')
    rj = 1e3
    I0 = I_of(solve(sid, sig_e(), n, plan(reg, rj)), n)
    want = chain_I([G_PL] + [G_AX] * 2 + [1e4 / rj] + [G_AX] * 6 + [G_PL])
    chk('T1-11 포트 (1,1,2) 회로 = 해석 사슬 (A 2 면 + R_j + B 6 면 · 1e-12)', rel(I0, want) < 1e-12, f'{I0} ↔ {want}')
    Pv = rows([polys[0][::-1], polys[1][::-1]])
    sidv = bed(Pv, n)[0]
    Iv = I_of(solve(sidv, sig_e(), n, plan(registry(sidv, Pv), rj)), n)
    Pr = rows([polys[1], polys[0]], fids=[20, 10])
    sidr = bed(Pr, n)[0]
    Ir = I_of(solve(sidr, sig_e(), n, plan(registry(sidr, Pr), rj)), n)
    chk('T1-11 점 역순 · 섬유 순서에 σ 불변 (동률 규칙이 방향 · 행 순서와 무관 · 1e-12)', rel(Iv, I0) < 1e-12 and rel(Ir, I0) < 1e-12,
        f'{I0} {Iv} {Ir}')


@case('T1-12')
def t_t112_site():
    P = rows(F10)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    chk('T1-12 같은 쌍 두 자리 중 한 자리만 instance', len(reg['instances']['fi']) == 1, f"{len(reg['instances']['fi'])}")
    rj = 3.0e3
    Ic = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj, unreg_law='cut')), F6_N)
    If = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj, unreg_law='fused')), F6_N)
    wc = _f6_reference(rj, second_site=False, fused_second=True)
    wf = _f6_reference(rj, second_site=True, fused_second=True)
    chk('T1-12 미등록 자리 cut = 첫 자리 접합만 (1e-12) · fused = 첫 자리 접합 + 둘째 자리 융합 면 (1e-12)',
        rel(Ic, wc) < 1e-12 and rel(If, wf) < 1e-12, f'{Ic} {wc} · {If} {wf}')
    chk('T1-12 같은 그래프 Rayleigh: cut ≤ fused', Ic <= If * (1 + 1e-12))
    chk('T1-12 법칙 미선언 = 거부 (자동 fallback 없음)', raises(lambda: CJ.cjunc_plan(reg, rj, unreg_law=None, ptfe_stamp='off')))


@case('T1-5p')
def t_t15_lead():
    P = rows(F1)
    sid, _ = bed(P, F1_N)
    reg = registry(sid, P)
    chk("T1-5′ 단자 기준 R_j (리드 빼기 기록 없음) = 거부", raises(lambda: plan(reg, 1e3, rj_reference='terminal_two_probe')))
    chk("T1-5′ 리드 빼기 기록이 와도 v0 = 거부 (모형 내부값만)", raises(lambda: plan(reg, 1e3, lead_subtraction={'R_leads_ohm': 2.0})))
    chk('T1-5′ 음수 · NaN R_j = 거부', raises(lambda: plan(reg, -1.0)) and raises(lambda: plan(reg, float('nan'))))
    chk('T1-5′ R_j 극한 (0 · ∞) = 사다리 천장 · 바닥 표지 없이 정량 거부', raises(lambda: plan(reg, 0.0)) and raises(lambda: plan(reg, math.inf)))


@case('J8')
def t_j8_long():
    n = (5, 3, 9)
    polys = [[(1.5, 1.5, 0.5), (1.5, 1.5, 6.5)], [(2.5, 1.5, 2.5), (2.5, 1.5, 8.5)]]   # 4 µm 나란히 (거리 1.0)
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    nl = int(np.sum(reg['instances']['long']))
    chk('J8 긴 평행 접촉 (L_c > L_par) = 수 기록', nl >= 1, f'{nl}')
    chk('J8 정량 모드 = 거부 (계획 · 솔브 둘 다)', raises(lambda: solve(sid, sig_e(), n, plan(reg, 1e3)))
        or any(x['code'] == 'long_contact' for x in plan(reg, 1e3)['rejections']))
    p_t = plan(reg, 1e3, quantitative=False)
    r = solve(sid, sig_e(), n, p_t)
    chk('J8 시험 모드 (quantitative=False) = 진행 · 기록 (긴 접촉 수 영수증)', r['sigma_eff'] > 0 and r['cjunc']['n_long'] >= 1)


@case('J11')
def t_j11_short():
    n = (5, 5, 2)
    polys = [[(0.5, 2.5, 0.5), (4.5, 2.5, 0.5)], [(2.5, 0.5, 1.5), (2.5, 4.5, 1.5)]]   # 아래 층 · 위 층 십자 (거리 1.0)
    P = rows(polys)
    sid, _ = bed(P, n)
    reg = registry(sid, P)
    r0 = solve(sid, sig_e(), n, plan(reg, 0.0, allow_rj_limits=True))
    chk('J11 축약 무리가 두 판에 다 닿음 = 단락 상태 (유한 σ 로 위장 안 함 · 게시 안 함)',
        r0.get('reason') == 'cjunc_electrode_short' and r0['sigma_eff'] == 0.0, f"{r0.get('reason')}")
    r1 = solve(sid, sig_e(), n, plan(reg, 1e3))
    chk('J11 R_j > 0 = 정상 σ (단락 아님)', r1['sigma_eff'] > 0 and not r1.get('reason'))


@case('C6')
def t_c6_energy():
    P = rows(F6)
    sid, _ = bed(P, F6_N)
    reg = registry(sid, P)
    rj = 3.0e3
    r = solve(sid, sig_e(), F6_N, plan(reg, rj))
    cj = r['cjunc']
    I = I_of(r, F6_N)
    sh = cj['dissipation_share']
    chk('C6 에너지 항등식 Σ P (면 + 접합 + 판) = I·ΔV (코드 단위 · 1e-10)', rel(cj['P_total_code'], I) < 1e-10,
        f"{cj['P_total_code']} ↔ {I}")
    d = 1e-4
    Ip = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj * (1 + d))), F6_N)
    Im = I_of(solve(sid, sig_e(), F6_N, plan(reg, rj * (1 - d))), F6_N)
    fd = -(math.log(Ip) - math.log(Im)) / (math.log(1 + d) - math.log(1 - d))
    chk('C6 접합 소산 몫 = −∂lnσ/∂lnR_j (중심 FD · 1e-6)', abs(sh['vv_junction'] - fd) < 1e-6, f"{sh['vv_junction']} ↔ {fd}")
    chk('C6 소산 몫 합 = 1', abs(sum(v for k, v in sh.items()) - 1.0) < 1e-12, f'{sh}')


@case('C8')
def t_c8_guards():
    P = rows(F1)
    sid, pid = bed(P, F1_N)
    reg = registry(sid, P)
    pl = plan(reg, 1e3)
    _CG_CALLS[0] = 0
    g = []
    g.append(('r1 표 동시', raises(lambda: solve(sid, sig_e(), F1_N, pl, rint={(3, 3): 1e-3}, pid=pid))))
    g.append(('주기', raises(lambda: solve(sid, sig_e(), F1_N, pl, periodic_xy=True))))
    g.append(('return_field (장 진단은 원장을 안 읽는다)', raises(lambda: solve(sid, sig_e(), F1_N, pl, return_field=True))))
    g.append(('솔버 vox ×2', raises(lambda: solve(sid, sig_e(), F1_N, pl, vox=2.0))))
    sid2 = sid.copy(); sid2[0, 0, 0] = 1
    g.append(('다른 sid', raises(lambda: solve(sid2, sig_e(), F1_N, pl))))
    pt = dict(pl); pt['g_code'] = pl['g_code'] * 2.0
    g.append(('계획 행 변조 (지문)', raises(lambda: solve(sid, sig_e(), F1_N, pt))))
    pt2 = dict(pl); pt2['g_code'] = np.full_like(pl['g_code'], np.nan)
    pt2['fp_rows'] = CJ.plan_rows_fp(pt2)
    g.append(('계획 g NaN (지문 다시 만든 변이 · Q7 불변량)', raises(lambda: solve(sid, sig_e(), F1_N, pt2))))
    rt = dict(reg); rt['instances'] = dict(reg['instances'])
    rt['instances']['port_i'] = reg['instances']['port_j'].copy()           # 포트를 다른 위치로 (값이 실제로 바뀐다)
    g.append(('원장 변조 (지문)', bool(np.any(rt['instances']['port_i'] != reg['instances']['port_i']))
              and raises(lambda: plan(rt, 1e3))))
    g.append(('VGCF 절연 채널 (이온 표)', raises(lambda: solve(sid, S3.ionic_sigma_table(0.3e-3, 3e-3), F1_N, pl))))
    cg_before = _CG_CALLS[0]
    Pn = (P[0].copy(), P[1], P[2], P[3]); Pn[0][3, 1] = np.nan
    g.append(('NaN 좌표', raises(lambda: registry(sid, Pn))))
    Pl = (P[0], P[1], P[2][:-1], P[3])
    g.append(('길이 불일치 (fid 한 줄 모자람)', raises(lambda: registry(sid, Pl))))
    g.append(('kind 없음 (연속 중심선 아님)', raises(lambda: quiet(CJ.cjunc_registry, sid, (0., 0., 0.), H, P[0], P[1], P[2], None,
                                                              r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT))))
    Fs = P[2].copy(); i0 = np.flatnonzero(Fs == 10)[2]; Fs[i0] = 20
    Ps = (P[0], P[1], Fs, P[3])
    rs = registry(sid, Ps)
    g.append(('떨어진 같은 fid = 정량 거부', any(x['code'] == 'fid_noncontiguous' for x in rs['rejections'])))
    pts_only = rows(F1, kind=0)
    sid_pt, _ = bed(pts_only, F1_N)
    rpt = registry(sid_pt, pts_only)
    g.append(('점 스탬프 VGCF (kind 0) = 정량 거부', any(x['code'] in ('vgcf_nonpath_fid', 'vgcf_orphan_cells')
                                                         for x in rpt['rejections'])))
    for nm, okk in g:
        chk(f'C8 거부 — {nm}', okk)
    chk('C8 거부 경로에서 CG 호출 0 (솔브 관문 아홉 · 조립 전)', cg_before == 0, f'{cg_before}')
    chk('C8 계획 · 기록 = 기구 표지 (mechanism_only · 모형 내부 R_j · 반셀 없음 · SDCP–VGCF 접촉 저항 0 가정)',
        pl['record']['status'].startswith('mechanism_only') and pl['record']['rj_reference_plane'] == 'model_internal_port_centre'
        and pl['record']['half_cell_in_edge'] is False
        and any('SDCP–VGCF 접촉 저항 0' in q for q in pl['record']['qualifiers']))


def _ptfe_rows(polys, fid0=900):
    return rows(polys, phase=4, fid0=fid0)


@case('P-junc')
def t_pjunc():
    P = rows(F1)
    #  PTFE 피브릴이 접점 (1.5,1.5,3.5) 근처를 지난다 — 중심선 거리 = r_P + r_f + tol_P 정확히 (경계 = 포함).
    #  경계값이 이진 정확 (0.25 + 0.5 + 0.25 = 1.0 · 좌표 2.5 − 1.5) 이어야 경계 시험이 반올림이 아닌 규칙을 본다.
    rP, tP = 0.25, 0.25
    dist = rP + RF + tP
    pt = _ptfe_rows([[(0.5, 1.5 + dist, 3.5), (5.5, 1.5 + dist, 3.5)]])
    allr = cat_rows(P, pt)
    sid, _ = bed(allr, F1_N, stamp=allr[1] != 4)                    # face_alpha 침대 = PTFE 셀 없음 (off 격자)
    reg = registry(sid, allr, tol_P_um=tP, r_ptfe_um=rP)
    cov = reg['instances']['ptfe_cov']
    chk('P-1 덮임 경계 = 정확히 tol_P 포함 (≤)', len(cov) == 1 and bool(cov[0]), f'{cov}')
    I0 = I_of(solve(sid, sig_e(), F1_N, plan(reg, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P0')), F1_N)
    r1 = solve(sid, sig_e(), F1_N, plan(reg, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P1'))
    chk('P-1 P0 = 영향 없음 (해석 사슬) · P1 = 덮인 instance 절단 (관통 없음)',
        rel(I0, F1_I(1e3)) < 1e-12 and r1['sigma_eff'] == 0.0 and r1['cjunc']['n_cut_p1'] == 1, f"{I0} {r1.get('reason')}")
    pt_far = _ptfe_rows([[(0.5, 1.5 + dist + 1e-9, 3.5), (5.5, 1.5 + dist + 1e-9, 3.5)]])
    allf = cat_rows(P, pt_far)
    regf = registry(sid, allf, tol_P_um=tP, r_ptfe_um=rP)
    chk('P-1 경계 밖 (+1e-9 µm) = 덮이지 않음', not bool(regf['instances']['ptfe_cov'][0]))
    chk('P-1 centerline + P1 = 거부 (centerline 이 이미 VGCF 셀을 sid 7 로 자른다)',
        raises(lambda: plan(reg, 1e3, ptfe_stamp='centerline', ptfe_jlaw='P1')))
    chk('P-1 off + P1 = 거부 (face_alpha 에서만)', raises(lambda: plan(reg, 1e3, ptfe_stamp='off', ptfe_jlaw='P1')))
    sd = rows([[(1.5, 2.5, 3.5)]], phase=5, kind=0, fid0=700)            # SDCP 점이 접점에 근접 (면 이웃 빈 셀)
    alls = cat_rows(P, pt, sd)
    sids, _ = bed(alls, F1_N, stamp=alls[1] != 4)
    regs = registry(sids, alls, tol_P_um=tP, r_ptfe_um=rP, tol_sj_um=0.5, r_sdcp_um=0.5)
    pp = plan(regs, 1e3, ptfe_stamp='face_alpha', ptfe_jlaw='P1', sdcp_mod={'c': 1.0})
    chk('P-2 PTFE 덮임 ∧ SDCP 근접 · (P1, c = 1) → 절단 먼저 (축약 아님 · N18)',
        int(pp['mode'][0]) == CJ.MODE_CUT_P1 and bool(regs['instances']['a_sdcp'][0]), f"{pp['mode']}")


# ═════════════════════════ S3 ═════════════════════════
def _s3_fixture(with_sdcp=True, sdcp_pos=(1.5, 2.5, 3.5)):
    P = rows(F1)
    parts = [P]
    if with_sdcp:
        parts.append(rows([[sdcp_pos]], phase=5, kind=0, fid0=700))
    allr = cat_rows(*parts)
    sid, _ = bed(allr, F1_N)                                       # SDCP 점 스탬프 (h 1 에서 구 스탬프는 d/vox ≥ 2 게이트)
    reg = registry(sid, allr, tol_sj_um=0.5, r_sdcp_um=0.5)
    return sid, reg, allr


def _rows_sig(p):
    return (p['mode'].tobytes(), p['g_code'].tobytes(), p['rj_eff'].tobytes())


@case('S3')
def t_s3():
    sid, reg, allr = _s3_fixture()
    chk('S3 근접 판정 (SDCP 1 차 입자 표면 ↔ 접점 ≤ tol_sj)', bool(reg['instances']['a_sdcp'][0]))
    p_s2 = plan(reg, 1e3)
    p_c0 = plan(reg, 1e3, sdcp_mod={'c': 0.0})
    r_s2 = solve(sid, sig_e(), F1_N, p_s2)
    r_c0 = solve(sid, sig_e(), F1_N, p_c0)
    chk('S3-1 c = 0 → 계획 행 · σ 가 S2 와 비트 같음', _rows_sig(p_s2) == _rows_sig(p_c0)
        and np.float64(r_s2['sigma_eff']).tobytes() == np.float64(r_c0['sigma_eff']).tobytes())
    sid_n, reg_n, _ = _s3_fixture(with_sdcp=False)
    s2n = plan(reg_n, 1e3)
    same = True
    for c in (0.0, 0.5, 1.0):
        pc = plan(reg_n, 1e3, sdcp_mod={'c': c}, quantitative=(c in (0.0, 1.0)))
        same &= _rows_sig(pc) == _rows_sig(s2n)
        rc = solve(sid_n, sig_e(), F1_N, pc)
        same &= np.float64(rc['sigma_eff']).tobytes() == np.float64(solve(sid_n, sig_e(), F1_N, s2n)['sigma_eff']).tobytes()
    chk('S3-2 SBE (SDCP 없음) — 모든 c 에서 계획 행 · σ 비트 같음 (셀 · 원장 단위 no-op)', same)
    Is = [I_of(solve(sid, sig_e(), F1_N, plan(reg, 1e3, sdcp_mod={'c': c}, quantitative=False)), F1_N)
          for c in (0.0, 0.5, 0.9, 0.99)]
    TAU = 1e-12                                                    # 봉인 (직접 풀이 · 같은 그래프 = Rayleigh 정확)
    chk(f'S3-3 c 단조 — σ(c) 비감소 (c 격자 0 · 0.5 · 0.9 · 0.99 · 허용폭 {TAU} 봉인)',
        all(Is[i + 1] >= Is[i] * (1 - TAU) for i in range(len(Is) - 1)) and Is[-1] > Is[0], f'{Is}')
    want_c = [F1_I(1e3 * (1 - c)) for c in (0.0, 0.5, 0.9, 0.99)]
    chk('S3-3 R_j′ = R_j,0·(1 − c·a_j) — 해석 사슬 (1e-12)', max(rel(a, b) for a, b in zip(Is, want_c)) < 1e-12, f'{Is} {want_c}')
    p1 = plan(reg, 1e3, sdcp_mod={'c': 1.0})
    r1 = solve(sid, sig_e(), F1_N, p1)
    chk('S3-4 c = 1 = 근접 instance 축약 (축약 경로 · 정량 허용 예외 · 축약 수 기록 · 옛 융합과 같음 1e-12)',
        int(p1['mode'][0]) == CJ.MODE_CONTRACT and r1['cjunc']['n_contracted'] == 1
        and rel(I_of(r1, F1_N), F1_I(0)) < 1e-12, f"{p1['mode']} {r1['cjunc'].get('n_contracted')}")
    chk('S3 정량 모드 c ∈ {0, 1} 만 (0.5 = 거부)', raises(lambda: plan(reg, 1e3, sdcp_mod={'c': 0.5})))
    chk('S3 c 범위 밖 · NaN = 거부', raises(lambda: plan(reg, 1e3, sdcp_mod={'c': 1.5}, quantitative=False))
        and raises(lambda: plan(reg, 1e3, sdcp_mod={'c': float('nan')}, quantitative=False)))
    P, PH, F, K = allr
    m5 = np.flatnonzero(PH == 5)
    order = np.arange(len(P)); order[m5] = m5[::-1]
    regp = registry(sid, (P[order], PH[order], F[order], K[order]), tol_sj_um=0.5, r_sdcp_um=0.5)
    chk('S3-5 SDCP 점 순열 불변 (근접 · 계획 행 비트 같음)', _rows_sig(plan(regp, 1e3, sdcp_mod={'c': 1.0})) == _rows_sig(p1))
    d_edge = 0.5 + 0.5                                             # 접점 (1.5,1.5,3.5) ↔ SDCP 중심 = r_s + tol_sj 정확히
    sid_e, reg_e, _ = _s3_fixture(sdcp_pos=(1.5, 1.5 + d_edge, 3.5))
    sid_o, reg_o, _ = _s3_fixture(sdcp_pos=(1.5, 1.5 + d_edge + 1e-9, 3.5))
    chk('S3-6 근접 문턱 경계 = 포함 (≤) · +1e-9 µm = 밖', bool(reg_e['instances']['a_sdcp'][0])
        and not bool(reg_o['instances']['a_sdcp'][0]))
    #  S3-7 원고 펠릿 LPSCl:SDCP 9:1 (탄소 없음) — v0 의 S3 은 구성상 no-op (판별력 없음 · 그렇게 기록)
    rng = np.random.default_rng(3)
    n = (12, 12, 12); box = np.array(n, float) * 0.5
    sd = rng.uniform(0.2, box - 0.2, (60, 3))
    rp = (sd, np.full(len(sd), 5), np.arange(len(sd)) + 1, np.zeros(len(sd), int))
    sidp, _ = S3.rasterize(*NO_AM, rp[0], rp[1], (0., 0., 0.), tuple(box), 0.5, se_pts=rng.uniform(0, box, (20000, 3)),
                           sdcp_sphere_d_um=1.0, add_fid=rp[2], add_kind=rp[3])
    regp = quiet(CJ.cjunc_registry, sidp, (0., 0., 0.), 0.5, *rp, r_f_um=0.25, tol_ff_um=0.05, L_par_um=1.0, r_port_um=1.0,
                 tol_sj_um=0.05, r_sdcp_um=0.5)
    pc0 = plan(regp, 1e3, sdcp_mod={'c': 0.0}); pc1 = plan(regp, 1e3, sdcp_mod={'c': 1.0})
    rc0 = solve(sidp, sig_e(), n, pc0, vox=0.5); rc1 = solve(sidp, sig_e(), n, pc1, vox=0.5)
    chk('S3-7 펠릿 9:1 (탄소 없음) — c 0 ↔ 1 σ_e 비트 같음 = 구성상 no-op (판별력 없음 기록)',
        len(regp['instances']['fi']) == 0 and np.float64(rc0['sigma_eff']).tobytes() == np.float64(rc1['sigma_eff']).tobytes()
        and rc1['cjunc'].get('s3_discriminating') is False)
    #  S3-8 변이 — 비근접에 c · (1 − c) 뒤집힘 · G 에 곱함 · c = 1 을 큰 g 로 = 실패해야
    old = CJ.sdcp_rj_eff
    det = []
    muts = (('비근접에 c', lambda r0, c, a: r0 * (1.0 - c)),
            ('(1 − c) 뒤집힘', lambda r0, c, a: r0 * (c * a if a else 1.0)),
            ('G 에 곱함', lambda r0, c, a: r0 / (1.0 - c * a) if c * a < 1 else math.inf),
            ('c = 1 을 큰 g 로', lambda r0, c, a: r0 * (1.0 - c * a) if c * a < 1 else 1e-12))
    for nm, fn in muts:
        CJ.sdcp_rj_eff = fn
        try:
            bad = False
            pm = plan(reg, 1e3, sdcp_mod={'c': 1.0})
            if int(pm['mode'][0]) != CJ.MODE_CONTRACT:
                bad = True
            pmh = plan(reg, 1e3, sdcp_mod={'c': 0.5}, quantitative=False)
            Im = I_of(solve(sid, sig_e(), F1_N, pmh), F1_N)
            if rel(Im, F1_I(500.0)) > 1e-12:
                bad = True
            pn = plan(reg_n, 1e3, sdcp_mod={'c': 1.0})
            if _rows_sig(pn) != _rows_sig(s2n):
                bad = True
            det.append(bad)
        except Exception:                                  # noqa: BLE001
            det.append(True)
        finally:
            CJ.sdcp_rj_eff = old
    chk('S3-8 변이 넷 (비근접에 c · 뒤집힘 · G 곱 · c = 1 큰 g) 을 시험이 잡는다', all(det), f'{det}')
    chk('S3-9 S2 없이 (원장 없이) = 거부', raises(lambda: CJ.cjunc_plan(None, 1e3, unreg_law='cut', ptfe_stamp='off',
                                                                     sdcp_mod={'c': 1.0}))
        and raises(lambda: solve(sid, sig_e(), F1_N, {'c': 1.0})))
    fp0 = reg['fp']['sid']
    chk('S3-10 sid 불변 — 모든 c 에서 원장의 sid 지문 = 솔브 sid', all(plan(reg, 1e3, sdcp_mod={'c': c}, quantitative=False)
                                                                    ['registry']['fp']['sid'] == fp0 for c in (0.0, 0.5, 1.0))
        and fp0 == S3._grid_fp(sid))


@case('SV')
def t_sv():
    #  SV 면 우회: A 와 B 사이에 SDCP 덩어리가 끼어 SV 면 (융합) 으로 이어진다 — 접합 저항이 크면 SV 경로가 소산을 지배
    n = (7, 3, 8)
    polys = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(3.5, 1.5, 3.5), (3.5, 1.5, 7.5)]]   # A–B 중심선 거리 2.0 (접합 아님)
    P = rows(polys)
    sd = rows([[(2.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700)
    allr = cat_rows(P, sd)
    sid, _ = bed(allr, n)                                          # SDCP 점 스탬프 → 셀 (2,1,3) = A 와 B 사이
    reg = registry(sid, allr, tol_sj_um=0.1, r_sdcp_um=0.5)
    chk('SV SDCP 경유 섬유 연결 수 (S0 꼴 · σ 전) = 1 성분 · fid 쌍 1', reg['census'].get('n_sdcp_bridging_components') == 1
        and reg['census'].get('n_sdcp_bridged_fid_pairs') == 1, f"{reg['census']}")
    r = solve(sid, sig_e(), n, plan(reg, 1e3))
    cj = r['cjunc']
    chk('SV 접합 instance 0 → 소산 = SV 면 + SDCP 셀 몫 > 0 · SV_DOMINANT 표지 (PASS 문장 금지)',
        cj['n_instances'] == 0 and cj['dissipation_share']['sv_face'] + cj['dissipation_share']['sdcp_cell'] > 0
        and cj['sv_dominant'] is True, f"{cj.get('dissipation_share')} {cj.get('sv_dominant')}")
    P2 = rows(F1)
    sid2, _ = bed(P2, F1_N)
    r2 = solve(sid2, sig_e(), F1_N, plan(registry(sid2, P2), 1e3))
    chk('SV SDCP 없음 → SV 몫 0 · SV_DOMINANT 아님', r2['cjunc']['dissipation_share']['sv_face'] == 0.0
        and r2['cjunc']['sv_dominant'] is False)


@case('MUT')
def t_mutants():
    """설계 §4-4 변이 — 조립기를 바꿔 끼운 변이가 위 시험 (해석 회로) 에 **걸려야** 한다 (판별력 · 안 걸리면 시험 무효)."""
    base_cls = CJ.CjuncAssembler

    class SingleWinner(base_cls):                          # 멤버십 단일 승자 — 교차 셀의 추가 dof 를 주 dof 로 접는다
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            pos = self.reg['positions']
            ex = np.flatnonzero(pos['live'] & ~pos['primary'])
            prim_of = {int(pos['lin'][p]): int(self.pos_dof[p]) for p in np.flatnonzero(pos['primary'])}
            for p in ex:
                self.pos_dof[p] = prim_of[int(pos['lin'][p])]

    class KeepTomb(base_cls):                              # tombstone 삭제 — 접합 자리 면을 옛 융합으로 남긴다
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            ft = dict(self.ft)
            ft['kind'] = np.where(ft['kind'] == CJ.K_CUT_SITE, CJ.K_AXIAL, ft['kind'])
            self.ft = ft

    class WrongDof(base_cls):                              # 간선을 다른 dof 에 — 포트 j 를 그 경로의 다음 위치로
        def build(self, *a, **k):
            inst = self.reg['instances']
            pj = inst['port_j'].copy()
            self.reg = dict(self.reg)
            self.reg['instances'] = dict(inst)
            self.reg['instances']['port_j'] = np.minimum(pj + 1, len(self.reg['positions']['lin']) - 1)
            return super().build(*a, **k)

    class PairCut(base_cls):                               # 쌍 단위 절단 — 미등록 자리도 그 쌍이면 절단
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            ft = dict(self.ft)
            ft['kind'] = np.where(ft['kind'] == CJ.K_UNREG, CJ.K_CUT_SITE, ft['kind'])
            self.ft = ft

    def run_with(cls, fn):
        CJ.CjuncAssembler = cls
        try:
            v = fn()
            print(f'    MUT {cls.__name__}: σ 기반 전류 {v!r}')
            return v
        except Exception as e:                             # noqa: BLE001 — 변이가 예외로 끝나도 '걸렸다' (기록한다)
            print(f'    MUT {cls.__name__}: 예외 {type(e).__name__}: {e}')
            return None
        finally:
            CJ.CjuncAssembler = base_cls

    P1_ = rows(F1); sid1, _ = bed(P1_, F1_N); reg1 = registry(sid1, P1_)
    P2_ = rows(F2); sid2, _ = bed(P2_, F2_N); reg2 = registry(sid2, P2_)
    P10 = rows(F10); sid10, _ = bed(P10, F6_N); reg10 = registry(sid10, P10)
    rj = 1e3
    I1 = run_with(SingleWinner, lambda: I_of(solve(sid1, sig_e(), F1_N, plan(reg1, rj)), F1_N))
    chk('MUT 멤버십 단일 승자 → C1 해석 사슬에서 벗어난다 (R_j 가 사라짐)', I1 is None or rel(I1, F1_I(rj)) > 1e-6, f'{I1}')
    w2 = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
    I2 = run_with(KeepTomb, lambda: I_of(solve(sid2, sig_e(), F2_N, plan(reg2, rj)), F2_N))
    chk('MUT tombstone 삭제 (옛 융합 면이 접합을 우회) → C2a 해석에서 벗어난다', I2 is None or rel(I2, w2) > 1e-6, f'{I2} {w2}')
    I3 = run_with(WrongDof, lambda: I_of(solve(sid1, sig_e(), F1_N, plan(reg1, rj)), F1_N))
    chk('MUT 접합 간선을 다른 dof 에 → C1 해석에서 벗어난다', I3 is None or rel(I3, F1_I(rj)) > 1e-6, f'{I3}')
    I4 = run_with(PairCut, lambda: I_of(solve(sid10, sig_e(), F6_N, plan(reg10, 3e3, unreg_law='fused')), F6_N))
    wf = _f6_reference(3e3, second_site=True, fused_second=True)
    chk('MUT 쌍 단위 절단 (미등록 자리까지 자름) → T1-12 fused 기준에서 벗어난다', I4 is None or rel(I4, wf) > 1e-6, f'{I4} {wf}')


def main():
    global S3, CJ, QUICK
    ap = argparse.ArgumentParser(description='Rint ② S2/S3 시험 (시험 먼저)')
    ap.add_argument('--quick', action='store_true', help='C0 무작위 침대 수를 줄인다')
    ap.add_argument('--only', default='', help='쉼표로 묶음 태그만 (예: C1,S3)')
    a = ap.parse_args()
    QUICK = a.quick
    import step3_sigma as _s3
    S3 = _s3
    try:
        import carbon_junction as _cj
        CJ = _cj
    except Exception as e:                                 # noqa: BLE001
        print(f'  ⚠ carbon_junction import 실패: {type(e).__name__}: {e}')
        CJ = None
    only = {x.strip() for x in a.only.split(',') if x.strip()}
    for tag, fn in CASES:
        if only and tag not in only:
            continue
        print(f'── {tag}')
        try:
            fn()
        except Exception as e:                             # noqa: BLE001 — 묶음 하나의 예외 = 그 묶음 실패 (다음 묶음은 계속)
            import traceback
            traceback.print_exc(limit=2)
            chk(f'{tag} 묶음 예외 없이 끝남', False, f'{type(e).__name__}: {e}')
    print(f'\n== test_carbon_junction: {_ok}/{_ok + len(_fail)} PASS')
    if _fail:
        print('FAIL: ' + ' · '.join(_fail))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
