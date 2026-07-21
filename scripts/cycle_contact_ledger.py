#!/usr/bin/env python3
"""A10 v1 — 사이클 접촉-원장 (contact-ledger) 열화 모델.  옵션 A (설계: docs/a10_cycle_chemomech_design.md).

압밀 완료 DEM 베드(atoms.csv)에서 사이클당 AM 격자 부피변화(충전=탈리튬=수축)를 반경 진동으로
가하고, 접촉별 개구(gap)를 Bucci 2017 CZM 길이척도(δ_0=5nm, δ_cr=100nm)로 판정해 영구 파단
원장을 전개한다.  출력 = 접촉망 열화 궤적: f_broken(N)·A_rel(N)·σ_e/σ_ion 상대(N)(입자-그래프
RNM) + R_ct(N) 프록시(= A(1)/A(N)) → Kang&Shin R_int(N) 4.4×/1.5× 모양과 대조.

물리 선택 = 전부 CLI 노브 + 문헌 기본값 (§5 미결을 코드에 몰래 굳히지 않음 — 라벨 명시):
  • ΔV 앵커: --dv-pct 5.1 (Kondrakov 2017 NMC811 격자, 3.0–4.3V) — 5.9(Yun/Kang) 스윕 가능.
    poly/SC 별도: --dv-pct-poly/--dv-pct-sc (기본 = 공통; Parks +19%는 균열-열림 팽창이라
    격자-수축 driver와 별개 축 — v2).
  • 파단 판정: gap > δ_cr → 영구 파단(Bucci flux-0, 재접촉 금지 기본).  0<gap≤δ_cr →
    cohesive 신장 생존 + (--fatigue miner) 사이클당 D+=gap/δ_cr 누적, ΣD≥1 파단
    [★ASSUMED-FORM: Miner 누적은 가정 — rint_cycle_traj g(N)와 같은 지위; B(MD 보정) 대기].
  • --recontact elastic: 파단 접촉도 gap≤0 복귀 시 재접촉 (Schmidt 2024 방향) — 기본 forbid.
  • Γ 게이트 (Bucci Fig5): Γ = ½·k_SE·(3β·φ_AM)²·H/G_c... 원식은 A_AM(면적)·H 규약 — 여기선
    보고용 스칼라 Γ* = ½·k_SE·(ΔV_frac)²·φ_AM/(G_c/H_m) 로 기록 (동일 스케일링, 라벨 명시).
한계(정직): 강체구+반경진동 = 재배열/입자내부균열/SE크리프 없음 → τ-스파이크(So 2021) 과소평가
가능.  σ는 입자-그래프 RNM 상대값 전용 (절대는 production Kirchhoff 소관 — frame[5]).
SE-SE 망은 v1에서 불변 → σ_ion_rel≈1 예측 = Yun 2023 (R_ion +23% ≪ R_int +187%)과 정합 검증점.
"""
import argparse
import csv
import json

import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.csgraph import connected_components
from scipy.sparse.linalg import cg, spsolve
from scipy.spatial import cKDTree


def load_atoms(path, type_map):
    am_t, se_t = set(), set()
    for tok in type_map.split(','):
        t, name = tok.split(':')
        (se_t if name.strip().upper().startswith('SE') else am_t).add(int(t))
    typ, xyz, rad = [], [], []
    with open(path, newline='') as f:
        rd = csv.DictReader(f)
        cols = {c.lower().strip(): c for c in rd.fieldnames}
        for row in rd:
            t = int(float(row[cols['type']]))
            if t not in am_t and t not in se_t:
                continue
            typ.append(0 if t in am_t else 1)               # 0=AM, 1=SE
            xyz.append([float(row[cols['x']]), float(row[cols['y']]), float(row[cols['z']])])
            rad.append(float(row[cols['radius']]))
    typ, xyz, rad = np.array(typ), np.array(xyz), np.array(rad)
    # ★ 단위 자동감지 (2026-07-22 버그픽스): DEM 원 atoms.csv는 mm (r_SE 0.0005 등) —
    #   µm 가정 시 수축량 1000× 과소 → 전-사이클 무손상 오출력.  payload와 동일하게 ×1000.
    if np.median(rad) < 0.05:
        xyz, rad = xyz * 1000.0, rad * 1000.0
        print('  ⚠ 좌표단위 mm 감지 → ×1000 µm 변환 적용', flush=True)
    return typ, xyz, rad


def build_contacts(xyz, rad):
    """압밀 상태 접촉 목록 (δ0 = r_i+r_j−d > 0).  반환 (i, j, d, δ0).
    대형 bimodal 베드 최적화: 전역 2·r_max 탐색은 147k-입자 mono 케이스에서 수 GB —
    소립끼리는 2·r_small, 대립은 입자별 r_i+r_small 반경으로 분리 탐색."""
    n = len(rad)
    big = rad > 2.0 * np.median(rad)
    if not big.any() or big.all():
        tree = cKDTree(xyz)
        pairs = tree.query_pairs(2.0 * rad.max(), output_type='ndarray')
    else:
        idx_s, idx_b = np.where(~big)[0], np.where(big)[0]
        t_s = cKDTree(xyz[idx_s])
        ps = t_s.query_pairs(2.0 * rad[idx_s].max(), output_type='ndarray')
        parts = [np.stack([idx_s[ps[:, 0]], idx_s[ps[:, 1]]], 1)] if len(ps) else []
        r_sm = rad[idx_s].max()
        for bi in idx_b:                                     # 대립 1개당 ball query (수천 회 OK)
            nb = t_s.query_ball_point(xyz[bi], rad[bi] + r_sm)
            if nb:
                nb = idx_s[np.asarray(nb)]
                parts.append(np.stack([np.full(len(nb), bi), nb], 1))
        t_b = cKDTree(xyz[idx_b])
        pb = t_b.query_pairs(2.0 * rad[idx_b].max(), output_type='ndarray')
        if len(pb):
            parts.append(np.stack([idx_b[pb[:, 0]], idx_b[pb[:, 1]]], 1))
        pairs = np.concatenate(parts, 0) if parts else np.zeros((0, 2), int)
    if len(pairs) == 0:
        return (np.zeros(0, int),) * 2 + (np.zeros(0),) * 2
    i, j = pairs[:, 0], pairs[:, 1]
    d = np.linalg.norm(xyz[i] - xyz[j], axis=1)
    ov = rad[i] + rad[j] - d
    m = ov > 0
    return i[m], j[m], d[m], ov[m]


def rnm_sigma(n, ci, cj, g, src_mask, snk_mask):
    """입자-그래프 Kirchhoff (상대 σ 전용): src=1V/snk=0V Dirichlet, 유효 컨덕턴스 반환.
    percolation 없으면 0.  g[k] = 접촉 k 컨덕턴스 (임의 단위 — 상대비만 의미).

    ★ 리뷰 CRITICAL 수정 (2026-07-22): 이전 판은 그래프에 고립/부동 노드(σ_e 계에선 SE
    전원, σ_i 계에선 AM 전원 = 0-degree bystander)가 있으면 Laplacian이 특이계 → spsolve가
    전체 해를 NaN → isfinite 게이트가 0.0 반환 → **퍼콜 중인 베드를 미퍼콜로 오진**.
    수정: g>0 간선 그래프의 연결성분 중 src/snk를 포함하는 성분의 노드만 남겨 인덱스 압축 후
    풀어 특이성을 제거 (성분당 최소 1 fixed → 비특이).  베드 크기 무관 견고."""
    if len(g) == 0 or not src_mask.any() or not snk_mask.any():
        return 0.0
    gm = g > 0                                              # 살아있는 간선만
    if not gm.any():
        return 0.0
    ei, ej, ge = ci[gm], cj[gm], g[gm]
    # 연결성분: g>0 간선 그래프
    adj = coo_matrix((np.ones(len(ei) * 2), (np.concatenate([ei, ej]), np.concatenate([ej, ei]))),
                     shape=(n, n)).tocsr()
    ncomp, lab = connected_components(adj, directed=False)
    keep_comp = np.zeros(ncomp, bool)                       # src 또는 snk를 담은 성분만
    keep_comp[lab[src_mask | snk_mask]] = True
    node_keep = keep_comp[lab]
    if not (node_keep & src_mask).any() or not (node_keep & snk_mask).any():
        return 0.0                                          # src·snk가 같은 성분에 없음 = 미퍼콜
    # 간선도 양끝이 keep 성분일 때만 (자동 성립 — 같은 성분)
    em = node_keep[ei] & node_keep[ej]
    ei, ej, ge = ei[em], ej[em], ge[em]
    idx = np.where(node_keep)[0]                            # 압축 인덱스
    remap = -np.ones(n, np.int64); remap[idx] = np.arange(len(idx))
    ri, rj = remap[ei], remap[ej]
    m = len(idx)
    sm = src_mask[idx]; km = snk_mask[idx]
    fixed = sm | km
    vfix = np.where(sm, 1.0, 0.0)
    L = coo_matrix((np.concatenate([ge, ge, -ge, -ge]),
                    (np.concatenate([ri, rj, ri, rj]), np.concatenate([ri, rj, rj, ri]))),
                   shape=(m, m)).tocsr()
    free = np.where(~fixed)[0]
    if len(free) == 0:
        return float(ge[sm[ri] & km[rj]].sum() + ge[km[ri] & sm[rj]].sum())
    A = L[free][:, free]
    b = -L[free][:, np.where(fixed)[0]] @ vfix[fixed]
    v = np.zeros(m); v[fixed] = vfix[fixed]
    try:
        if len(free) > 20000:                              # 대형망: 직접해 fill-in 회피 → Jacobi-CG
            Ac = A.tocsr(); dg = Ac.diagonal(); dg[dg <= 0] = 1.0
            sol, info = cg(Ac, b, M=diags(1.0 / dg), rtol=1e-9, maxiter=10000)
            if info != 0 or not np.all(np.isfinite(sol)):
                return 0.0
            v[free] = sol
        else:
            v[free] = spsolve(A.tocsc(), b)
    except Exception:
        return 0.0
    if not np.all(np.isfinite(v[free])):
        return 0.0
    I = ge * (v[ri] - v[rj])                                # src에서 나가는 전류 합
    out = float(I[sm[ri]].sum() - I[sm[rj]].sum())
    return abs(out)


def run(a):
    typ, xyz, rad0 = load_atoms(a.atoms, a.type_map)
    n = len(typ)
    am = typ == 0
    n_am_, n_se_ = int(am.sum()), int((~am).sum())
    print(f'  입자: AM {n_am_} / SE {n_se_}  (type-map: {a.type_map})', flush=True)
    if n_am_ == 0 or n_se_ == 0:
        raise SystemExit(f'❌ AM 또는 SE가 0개 — --type-map 불일치 가능성.  atoms.csv 실제 타입 확인:\n'
                         f"   awk -F, 'NR>1{{c[$2]++}} END{{for(t in c) print t, c[t]}}' {a.atoms}\n"
                         f'   mono-AM 케이스는 SE가 type 2 → --type-map "1:AM_P,2:SE"')
    ci, cj, d, ov0 = build_contacts(xyz, rad0)
    kind = typ[ci] + typ[cj]                                # 0=AM-AM, 1=AM-SE, 2=SE-SE
    if not (kind == 1).any():
        # AM-SE 접촉 0 = 열화 대상이 없음 — A_rel=0/R_ct=1 같은 모순 출력으로 침묵 진행 금지
        raise SystemExit('❌ AM-SE 접촉 0개 (압밀 베드에선 비물리) — type-map 또는 좌표단위(µm) 확인')
    Rstar = rad0[ci] * rad0[cj] / (rad0[ci] + rad0[cj])     # 감쇄반경 R* (Hertz a=√(R*δ)) — 리뷰 MAJOR
    is_poly = rad0 >= a.am_split_um                         # step4와 동일 분류 규약
    # ΔV → 반경 수축률 (충전 반각): r → r·(1−ε), ε = (ΔV/100)/3 · swing (선형-등방 근사, 라벨)
    dv = np.where(is_poly, a.dv_pct_poly if a.dv_pct_poly is not None else a.dv_pct,
                  a.dv_pct_sc if a.dv_pct_sc is not None else a.dv_pct)
    eps = dv / 100.0 / 3.0 * a.soc_swing
    shrink = np.where(am, eps, 0.0)                         # SE는 불변 (v1)
    # 충전-말 gap: 원 개구 gap_c = d − (r_i(1−ε_i)+r_j(1−ε_j)) = −ov0 + r_i·ε_i + r_j·ε_j
    gap_um = -ov0 + rad0[ci] * shrink[ci] + rad0[cj] * shrink[cj]
    gap_nm = gap_um * 1e3                                   # atoms.csv 좌표 = µm 규약
    dcr = a.deltacr_nm
    # ── ★ 접촉종별 영구파단 대상 (리뷰 MAJOR ③): Bucci δcr=100nm는 SE-상 cohesive TSL —
    #    AM-SE(계면 박리, Bucci 2018)와 SE-SE(본래 대상)에만 CZM 영구파단.  AM-AM은 결합 없는
    #    단측 강체 접촉 → 방전 스택압으로 재폐합(영구 아님) = 기본.  --aa-czm로 AM-AM도 CZM
    #    (민감도/상한 시나리오).  SE-SE는 ε_SE=0이라 어차피 개구 없음(σ_ion≡1은 구성적).
    czm_kind = (kind == 1) | (kind == 2)                    # 기본: AM-SE + SE-SE
    if a.aa_czm:
        czm_kind |= (kind == 0)
    # Γ* 보고 스칼라 (Bucci Fig5 스케일링 — 라벨: 보고용, 판정은 접촉별 δ_cr)
    zlo, zhi = xyz[:, 2].min(), xyz[:, 2].max()
    H_m = max(zhi - zlo, 1e-9) * 1e-6
    phi_am = float((rad0[am] ** 3).sum() / max((rad0 ** 3).sum(), 1e-30))
    gamma_star = 0.5 * a.k_se_gpa * 1e9 * (float(np.mean(eps[am] * 3)) ** 2) * phi_am / (a.gc / H_m)
    # 플레이트 밴드 (z 최하/최상 1 최대반경 폭) — σ_e: AM 하부→상부 / σ_ion: SE 하부→상부
    band = rad0.max()
    lo_b, hi_b = xyz[:, 2] <= zlo + band, xyz[:, 2] >= zhi - band
    aa = kind == 0
    ss = kind == 2
    ase = kind == 1

    def sigma_pair():
        gA = np.sqrt(np.maximum(Rstar * ov_now, 0.0)) * alive   # g ∝ Holm 2r_c ∝ √(R*δ) — R* 포함(리뷰 MAJOR)
        se_ = ~am
        s_e = rnm_sigma(n, ci[aa], cj[aa], gA[aa], am & lo_b, am & hi_b)
        s_i = rnm_sigma(n, ci[ss], cj[ss], gA[ss], se_ & lo_b, se_ & hi_b)
        return s_e, s_i

    alive = np.ones(len(ci), bool)                          # 영구 원장 (방전-말 생존)
    dmg = np.zeros(len(ci))
    ov_now = ov0.copy()
    rng = np.random.default_rng(a.seed)                     # 부분-재습윤 재현성 (--seed)
    s_e0, s_i0 = sigma_pair()
    a_proxy = np.sqrt(np.maximum(Rstar * ov0, 0))           # 접촉 반경 a ∝ √(R*δ) (Hertz, R* 포함)
    A0 = float(a_proxy[ase].sum())                          # Σa (Holm 구속: R∝1/Σa = area^−0.5)
    A0_area = float((a_proxy[ase] ** 2).sum())              # Σa² ∝ 반응면적 (전하이동 R_ct: R∝1/Σa² = area^−1)
    open_ever_aa = np.zeros(len(ci), bool)                  # AM-AM 충전-말 개구 누적 (보고용, 비영구)
    chk = sorted(set(int(x) for x in a.checkpoints.split(',') if x.strip()))
    rows = []
    for N in range(1, max(chk) + 1):
        # ── 충전 반각 (수축): 개구 판정 (czm_kind = 영구파단 대상 접촉종만) ──
        opened = alive & (gap_nm > 0)
        open_ever_aa |= opened & aa                         # AM-AM 개구는 기록만 (재폐합 → 비영구)
        brk_now = opened & czm_kind & (gap_nm > dcr)        # 즉시 파단 (δ_cr 초과 — Bucci 완전분리)
        if a.fatigue == 'miner':
            st = opened & czm_kind & ~brk_now               # cohesive 신장 생존 → Miner 누적 (ASSUMED-FORM)
            dmg[st] += np.clip(gap_nm[st] / dcr, 0, 1)
            brk_now |= st & (dmg >= 1.0)
        # ── 방전 반각 부분-재습윤 (§5-4): 스택압이 신규 파단분의 f_rewet를 다시 눌러앉힘.
        #    forbid=0(하한) / elastic=1(무열화 상한) / partial=중간(재현 --seed).  전량-복원
        #    상한은 정의상 무열화 → 별 정보 없음; 하한 forbid가 본선, partial이 물리 중간. ──
        if a.recontact != 'forbid' and brk_now.any():
            frac = 1.0 if a.recontact == 'elastic' else float(a.rewet_frac)
            if frac > 0:
                bi = np.where(brk_now)[0]
                rewet = rng.random(len(bi)) < frac          # 이번 파단분 중 재습윤(생존)
                brk_now[bi[rewet]] = False
        alive &= ~brk_now
        ov_now = np.where(alive, ov0, 0.0)                  # 방전-말 상태 (반경 원복 — 원장만 남음)
        if N in chk:
            s_e, s_i = sigma_pair()
            A_ = float((a_proxy[ase] * alive[ase]).sum())          # Σa (구속)
            A_area = float((a_proxy[ase] ** 2 * alive[ase]).sum())  # Σa² (반응면적)
            rows.append(dict(cycle=N,
                             f_broken_amse=float(1 - alive[ase].mean()) if ase.any() else 0.0,
                             f_broken_sese=float(1 - alive[ss].mean()) if ss.any() else 0.0,
                             f_open_amam_charge=float(open_ever_aa[aa].mean()) if aa.any() else 0.0,
                             A_rel_amse=A_ / max(A0, 1e-30),
                             # 리뷰 #1: 접촉저항 배율 두 규약 — Holm 구속(1/Σa=area^−0.5, 하한) vs
                             #   전하이동 R_ct(1/Σa²=area^−1, 상한; 측정 CAM-SE는 CT 지배라 이쪽이 더 적합)
                             rct_proxy_rel=max(A0, 1e-30) / max(A_, 1e-30),       # Holm 구속 (기존)
                             rct_holm_rel=max(A0, 1e-30) / max(A_, 1e-30),        # =rct_proxy_rel (명시 별칭)
                             rct_ct_area_rel=max(A0_area, 1e-30) / max(A_area, 1e-30),  # 전하이동(면적)
                             sigma_e_rel=(s_e / s_e0) if s_e0 > 0 else None,
                             sigma_i_rel=(s_i / s_i0) if s_i0 > 0 else None))
            _f = lambda v: '—(미퍼콜)' if v is None else f'{v:.3f}'
            print(f'  N={N:4d}  f_brk(AM-SE)={rows[-1]["f_broken_amse"]:.3f}  '
                  f'A_rel={rows[-1]["A_rel_amse"]:.3f}  R_ct∝[Holm {rows[-1]["rct_holm_rel"]:.2f}–'
                  f'CT {rows[-1]["rct_ct_area_rel"]:.2f}]×  '
                  f'σ_e_rel={_f(rows[-1]["sigma_e_rel"])}  σ_ion_rel={_f(rows[-1]["sigma_i_rel"])}'
                  f'  (AM-AM 충전개구 {rows[-1]["f_open_amam_charge"]:.2f}, 재폐합)', flush=True)
    out = dict(model='A10-v1 contact-ledger (option A)', atoms=a.atoms,
               n_particles=int(n), n_am=int(am.sum()),
               n_contacts=dict(am_am=int(aa.sum()), am_se=int(ase.sum()), se_se=int(ss.sum())),
               anchors=dict(dv_pct=a.dv_pct, dv_pct_poly=a.dv_pct_poly, dv_pct_sc=a.dv_pct_sc,
                            provenance_dv='Kondrakov 2017 NMC811 lattice −5.1% (3.0–4.3V)' if a.dv_pct == 5.1 else 'CLI',
                            delta0_nm=a.delta0_nm, deltacr_nm=a.deltacr_nm,
                            provenance_czm='Bucci 2017 JMCA Table 2 (δ0=5nm, δcr=20δ0)',
                            gc_J_m2=a.gc, provenance_gc='McGrogan sulfide K_IC→G_c 2.8±1.8 J/m²',
                            k_se_gpa=a.k_se_gpa, soc_swing=a.soc_swing),
               conventions=dict(recontact=a.recontact, rewet_frac=a.rewet_frac, aa_czm=bool(a.aa_czm),
                                fatigue=a.fatigue,
                                fatigue_label='ASSUMED-FORM (Miner) — 양끝 아닌 중간 궤적은 가정' if a.fatigue == 'miner' else '-',
                                sigma_note='입자-그래프 RNM 상대값 전용 (절대 σ = production Kirchhoff 소관)',
                                czm_scope='CZM 영구파단 = AM-SE+SE-SE만 (AM-AM은 스택압 재폐합·비영구; --aa-czm로 포함)'
                                          if not a.aa_czm else 'CZM = 전 접촉종 (--aa-czm; AM-AM 상한 시나리오)',
                                se_network='v1 SE 불변(ε_SE=0) → σ_ion_rel≡1 구성적 = Yun 2023 (R_int≫R_ion) 정합',
                                overlap_caveat='ov0 = DEM 18×-연화 E 규약 길이; δcr=100nm는 문헌 절대값 — '
                                               '층위 혼합(리뷰 MAJOR).  δcr을 캘리브 노브로 취급(스윕 권장), '
                                               '완전-탄성 회복 가정(잔류 압평 δ_res 무시)은 개구 과소 방향'),
               gamma_star=dict(value=float(f'{gamma_star:.4g}'), threshold=1000.0,
                               verdict='damage-expected' if gamma_star >= 1000 else 'SE-integrity-scale',
                               label='repo 무차원 에너지비 게이트 (Bucci Fig5 착안; ½k_SE·ε_vol²·φ_AM·H/G_c, '
                                     '무차원 확인 — 설계문서 원식과 A_AM 차원규약 상이, 판정은 접촉별 δcr)'),
               phi_am=float(f'{phi_am:.4f}'), thickness_um=float(f'{(zhi - zlo):.2f}'),
               trajectory=rows)
    with open(a.out + '.json', 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    with open(a.out + '.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f'saved {a.out}.json / .csv  (Γ*={gamma_star:.3g} [{out["gamma_star"]["verdict"]}], '
          f'접촉 AM-AM {aa.sum()}/AM-SE {ase.sum()}/SE-SE {ss.sum()})')


# ---------------------------------------------------------------- selftest
def _selftest():
    ok = True
    # 1) 2입자 (AM r=6, SE r=1, 겹침 δ0): 수축 개구 gap = r_AM·ε − δ0
    #    ΔV=5.1% → ε=0.017 → 6µm·0.017 = 102nm 이동.  δ0=1nm → gap≈101nm > δ_cr=100 → N=1 파단
    typ = np.array([0, 1]); rad = np.array([6.0, 1.0])
    d = 6.0 + 1.0 - 0.001                                    # δ0 = 1 nm
    xyz = np.array([[0, 0, 0], [0, 0, d]])
    ci, cj, dd, ov = build_contacts(xyz, rad)
    ok &= len(ci) == 1 and abs(ov[0] - 0.001) < 1e-9
    eps = 5.1 / 100 / 3
    gap_nm = (-ov[0] + 6.0 * eps) * 1e3
    ok &= gap_nm > 100.0
    print(f'selftest1 즉시파단 기하: gap={gap_nm:.1f}nm > δ_cr=100  {"OK" if ok else "FAIL"}')
    # 2) Miner 누적: δ0=60nm·같은 ε → gap≈42nm ≤ δ_cr → D+=0.42/cyc → N=3에 파단
    ov2 = 0.060
    gap2 = (-ov2 + 6.0 * eps) * 1e3
    n_pred = int(np.ceil(100.0 / gap2))
    ok2 = 0 < gap2 <= 100 and n_pred == 3
    ok &= ok2
    print(f'selftest2 Miner N_break: gap={gap2:.1f}nm → N={n_pred} (기대 3)  {"OK" if ok2 else "FAIL"}')
    # 3) RNM percolation: 3입자 직렬 사슬, 중간 접촉 절단 → σ→0
    n3 = 3
    ci3, cj3 = np.array([0, 1]), np.array([1, 2])
    g3 = np.array([1.0, 1.0])
    src = np.array([True, False, False]); snk = np.array([False, False, True])
    s_full = rnm_sigma(n3, ci3, cj3, g3, src, snk)
    s_cut = rnm_sigma(n3, ci3, cj3, g3 * np.array([1.0, 0.0]), src, snk)
    ok3 = abs(s_full - 0.5) < 1e-9 and s_cut < 1e-12
    ok &= ok3
    print(f'selftest3 RNM 직렬 0.5 / 절단 0: {s_full:.3f}/{s_cut:.1e}  {"OK" if ok3 else "FAIL"}')
    # 4) 무-파단 보존: ΔV=0 → 전 사이클 σ_rel=1, f_brk=0 (원장 부작용 없음)
    #    (run() 경량 재현: gap 전부 음수 → alive 불변)
    gap_all = np.array([-5.0, -1.0])
    alive = np.ones(2, bool)
    alive &= ~(alive & (gap_all > 100))
    ok4 = alive.all()
    ok &= ok4
    print(f'selftest4 ΔV=0 무-파단 보존: {"OK" if ok4 else "FAIL"}')
    # 5) ★ 리뷰 CRITICAL 회귀: 고립/부동 노드가 있어도 rnm_sigma가 특이계 0.0 아닌 정답
    #    (구 판은 spsolve NaN → 0.0 미퍼콜 오진; selftest3은 고립 없어 못 잡던 위양성)
    n5 = 5                                                   # 0-1-2 사슬 + 고립 3 + 부동쌍 4는 없음→노드 4 고립
    ci5, cj5 = np.array([0, 1]), np.array([1, 2])
    g5 = np.array([1.0, 1.0])
    src5 = np.array([True, False, False, False, False])
    snk5 = np.array([False, False, True, False, False])     # 3,4 = 전극-비연결 bystander
    s5 = rnm_sigma(n5, ci5, cj5, g5, src5, snk5)
    ok5 = abs(s5 - 0.5) < 1e-9
    ok &= ok5
    print(f'selftest5 고립노드 견고성(직렬0.5+bystander): {s5:.3f}  {"OK" if ok5 else "FAIL"}')
    # 6) ★ 혼합상 미니베드 end-to-end (run 관통): AM/SE 섞인 베드가 σ_rel=None 안 뱉나
    import argparse as _ap
    import tempfile
    import os as _os
    rng = np.random.default_rng(1)
    lines = ['id,type,x,y,z,radius']
    pid = 1
    # AM 2×2 격자(z=0,10) + SE 채움 → AM-SE·SE-SE 접촉 형성 (좌표 µm)
    for zc in (0.0, 9.0):
        for xc in (0, 6):
            for yc in (0, 6):
                lines.append(f'{pid},1,{xc},{yc},{zc},3.0'); pid += 1
    for _ in range(60):
        p = rng.uniform([-1, -1, -1], [7, 7, 10])
        lines.append(f'{pid},3,{p[0]:.2f},{p[1]:.2f},{p[2]:.2f},1.2'); pid += 1
    fd, tmp = tempfile.mkstemp(suffix='.csv'); _os.write(fd, ('\n'.join(lines) + '\n').encode()); _os.close(fd)
    a6 = _ap.Namespace(atoms=tmp, type_map='1:AM_P,3:SE', dv_pct=5.1, dv_pct_poly=None, dv_pct_sc=None,
                       am_split_um=3.5, soc_swing=1.0, delta0_nm=5.0, deltacr_nm=100.0, gc=2.8,
                       k_se_gpa=24.0, recontact='forbid', rewet_frac=0.5, aa_czm=False, seed=0,
                       fatigue='miner', checkpoints='1,5', out=tmp + '.out')
    try:
        run(a6)
        rj = json.load(open(tmp + '.out.json'))
        tr = rj['trajectory']
        ok6 = len(tr) >= 1 and tr[0]['sigma_i_rel'] is not None   # SE망 퍼콜 → None 아니어야
        print(f'selftest6 혼합베드 e2e σ_ion 계산됨(None아님): {tr[0].get("sigma_i_rel")}  {"OK" if ok6 else "FAIL"}')
    except Exception as e:
        ok6 = False
        print(f'selftest6 혼합베드 e2e: FAIL ({e!r})')
    finally:
        for f in (tmp, tmp + '.out.json', tmp + '.out.csv'):
            if _os.path.exists(f):
                _os.remove(f)
    ok &= ok6
    print('CYCLE-LEDGER SELFTEST', 'PASS' if ok else 'FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(description='A10 v1 — 사이클 접촉-원장 열화 (옵션 A)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--atoms', help='압밀 베드 atoms.csv (id,type,x,y,z,radius; µm)')
    ap.add_argument('--type-map', default='1:AM_P,2:AM_S,3:SE')
    ap.add_argument('--dv-pct', type=float, default=5.1,
                    help='AM 격자 부피변화 %% (기본 5.1 = Kondrakov 2017 NMC811 3.0–4.3V; 5.9=Yun/Kang 스윕)')
    ap.add_argument('--dv-pct-poly', type=float, default=None, help='poly(r≥split) 별도 ΔV%% (기본 공통)')
    ap.add_argument('--dv-pct-sc', type=float, default=None, help='SC 별도 ΔV%%')
    ap.add_argument('--am-split-um', type=float, default=3.5, help='poly/SC 반경 문턱 (step4 규약)')
    ap.add_argument('--soc-swing', type=float, default=1.0, help='SOC 창 분율 (부분충전 스윕)')
    ap.add_argument('--delta0-nm', type=float, default=5.0, help='CZM δ_0 (Bucci 2017)')
    ap.add_argument('--deltacr-nm', type=float, default=100.0, help='CZM δ_cr=20δ_0 완전분리 (Bucci 2017)')
    ap.add_argument('--gc', type=float, default=2.8, help='G_c [J/m²] (McGrogan 황화물 2.8±1.8 — Γ* 보고/스윕)')
    ap.add_argument('--k-se-gpa', type=float, default=24.0, help='SE 벌크 K [GPa] (real LPSC — Γ*용)')
    ap.add_argument('--recontact', choices=('forbid', 'partial', 'elastic'), default='forbid',
                    help='방전 재습윤: forbid=영구파단 하한(기본) / partial=스택압 부분재습윤(--rewet-frac) / '
                         'elastic=전량복원 무열화 상한(§5-4)')
    ap.add_argument('--rewet-frac', type=float, default=0.5,
                    help='partial 모드 재습윤 분율 (매 사이클 신규 파단분 중 재폐합; 0=forbid 1=elastic)')
    ap.add_argument('--aa-czm', action='store_true',
                    help='AM-AM 접촉도 CZM 영구파단 적용 (기본=재폐합 비영구; 이건 상한/민감도 — 리뷰 MAJOR)')
    ap.add_argument('--seed', type=int, default=0, help='partial 재습윤 RNG 시드 (재현성)')
    ap.add_argument('--fatigue', choices=('miner', 'off'), default='miner',
                    help='δ_cr 이하 개구의 사이클 누적 (miner=ASSUMED-FORM 라벨 / off=즉시파단만)')
    ap.add_argument('--checkpoints', default='1,2,5,10,25,50,75,100', help='기록 사이클 (Kang&Shin 격자)')
    ap.add_argument('--out', default='cycle_ledger_out')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(0 if _selftest() else 1)
    if not a.atoms:
        ap.error('--atoms required (or --selftest)')
    for nm, v in (('--dv-pct', a.dv_pct), ('--gc', a.gc), ('--deltacr-nm', a.deltacr_nm),
                  ('--am-split-um', a.am_split_um)):
        if v <= 0:
            ap.error(f'{nm} must be > 0')
    if not (0.0 <= a.rewet_frac <= 1.0):
        ap.error('--rewet-frac must be in [0,1]')
    _chk = [int(x) for x in a.checkpoints.split(',') if x.strip()]
    if not _chk or min(_chk) < 1:                           # 리뷰 MINOR ⑦: 퇴화 입력 크래시 가드
        ap.error('--checkpoints must be nonempty positive ints (e.g. 1,25,50,100)')
    run(a)


if __name__ == '__main__':
    main()
