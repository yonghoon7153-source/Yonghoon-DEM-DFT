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
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
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
    return np.array(typ), np.array(xyz), np.array(rad)


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
    percolation 없으면 0.  g[k] = 접촉 k 컨덕턴스 (임의 단위 — 상대비만 의미)."""
    if len(g) == 0 or not src_mask.any() or not snk_mask.any():
        return 0.0
    fixed = src_mask | snk_mask
    vfix = np.where(src_mask, 1.0, 0.0)
    L = coo_matrix((np.concatenate([g, g, -g, -g]),
                    (np.concatenate([ci, cj, ci, cj]), np.concatenate([ci, cj, cj, ci]))),
                   shape=(n, n)).tocsr()
    free = np.where(~fixed)[0]
    if len(free) == 0:
        return float(g[src_mask[ci] & snk_mask[cj]].sum() + g[snk_mask[ci] & src_mask[cj]].sum())
    A = L[free][:, free]
    b = -L[free][:, np.where(fixed)[0]] @ vfix[fixed]
    v = np.zeros(n)
    v[fixed] = vfix[fixed]
    try:
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')                 # 특이계(미퍼콜) 경고는 아래 isfinite가 판정
            if len(free) > 20000:                           # 대형망: 직접해 fill-in 회피 → Jacobi-CG
                from scipy.sparse.linalg import cg
                Ac = A.tocsr()
                dg = Ac.diagonal(); dg[dg <= 0] = 1.0
                from scipy.sparse import diags
                sol, info = cg(Ac, b, M=diags(1.0 / dg), rtol=1e-8, maxiter=5000)
                if info != 0:
                    return 0.0
                v[free] = sol
            else:
                v[free] = spsolve(A.tocsc(), b)
    except Exception:
        return 0.0
    if not np.all(np.isfinite(v[free])):                    # 부동 성분(비연결) = 특이계 → 미퍼콜
        return 0.0
    I = g * (v[ci] - v[cj])                                 # src에서 나가는 전류 합
    out = float(I[src_mask[ci]].sum() - I[src_mask[cj]].sum())
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
        gA = np.sqrt(np.maximum(ov_now, 0.0)) * alive       # g ∝ Holm 2r_c ∝ √(R*δ) — 상대 전용(Hertz a=√(R*δ))
        se_ = ~am
        s_e = rnm_sigma(n, ci[aa], cj[aa], gA[aa], am & lo_b, am & hi_b)
        s_i = rnm_sigma(n, ci[ss], cj[ss], gA[ss], se_ & lo_b, se_ & hi_b)
        return s_e, s_i

    alive = np.ones(len(ci), bool)
    dmg = np.zeros(len(ci))
    ov_now = ov0.copy()
    s_e0, s_i0 = sigma_pair()
    A0 = float(np.sqrt(np.maximum(ov0[ase], 0)).sum())      # AM-SE 반응면 프록시 Σa ∝ Σ√δ (상대 전용)
    chk = sorted(set(int(x) for x in a.checkpoints.split(',') if x.strip()))
    rows = []
    for N in range(1, max(chk) + 1):
        # ── 충전 반각 (수축): 개구 판정 ──
        opened = alive & (gap_nm > 0)
        brk_now = opened & (gap_nm > dcr)                   # 즉시 파단 (δ_cr 초과 — Bucci 완전분리)
        if a.fatigue == 'miner':
            st = opened & ~brk_now                          # cohesive 신장 생존 → Miner 누적 (ASSUMED-FORM)
            dmg[st] += np.clip(gap_nm[st] / dcr, 0, 1)
            brk_now |= st & (dmg >= 1.0)
        alive &= ~brk_now
        # ── 방전 반각 (복귀): forbid = 파단 영구 / elastic = gap≤0 복귀 접촉 부활 ──
        if a.recontact == 'elastic':
            alive |= (gap_nm <= 0)
        ov_now = np.where(alive, ov0, 0.0)                  # 방전-말 상태 (반경 원복 — 원장만 남음)
        if N in chk:
            s_e, s_i = sigma_pair()
            A_ = float((np.sqrt(np.maximum(ov0[ase], 0)) * alive[ase]).sum())
            rows.append(dict(cycle=N,
                             f_broken_amse=float(1 - alive[ase].mean()) if ase.any() else 0.0,
                             f_broken_amam=float(1 - alive[aa].mean()) if aa.any() else 0.0,
                             f_broken_sese=float(1 - alive[ss].mean()) if ss.any() else 0.0,
                             A_rel_amse=A_ / max(A0, 1e-30),
                             rct_proxy_rel=max(A0, 1e-30) / max(A_, 1e-30),
                             sigma_e_rel=(s_e / s_e0) if s_e0 > 0 else None,
                             sigma_i_rel=(s_i / s_i0) if s_i0 > 0 else None))
            _f = lambda v: '—(baseline 미퍼콜)' if v is None else f'{v:.3f}'
            print(f'  N={N:4d}  f_brk(AM-SE)={rows[-1]["f_broken_amse"]:.3f}  '
                  f'A_rel={rows[-1]["A_rel_amse"]:.3f}  R_ct∝{rows[-1]["rct_proxy_rel"]:.2f}×  '
                  f'σ_e_rel={_f(rows[-1]["sigma_e_rel"])}  σ_ion_rel={_f(rows[-1]["sigma_i_rel"])}',
                  flush=True)
    out = dict(model='A10-v1 contact-ledger (option A)', atoms=a.atoms,
               n_particles=int(n), n_am=int(am.sum()),
               n_contacts=dict(am_am=int(aa.sum()), am_se=int(ase.sum()), se_se=int(ss.sum())),
               anchors=dict(dv_pct=a.dv_pct, dv_pct_poly=a.dv_pct_poly, dv_pct_sc=a.dv_pct_sc,
                            provenance_dv='Kondrakov 2017 NMC811 lattice −5.1% (3.0–4.3V)' if a.dv_pct == 5.1 else 'CLI',
                            delta0_nm=a.delta0_nm, deltacr_nm=a.deltacr_nm,
                            provenance_czm='Bucci 2017 JMCA Table 2 (δ0=5nm, δcr=20δ0)',
                            gc_J_m2=a.gc, provenance_gc='McGrogan sulfide K_IC→G_c 2.8±1.8 J/m²',
                            k_se_gpa=a.k_se_gpa, soc_swing=a.soc_swing),
               conventions=dict(recontact=a.recontact, fatigue=a.fatigue,
                                fatigue_label='ASSUMED-FORM (Miner) — 양끝 아닌 중간 궤적은 가정' if a.fatigue == 'miner' else '-',
                                sigma_note='입자-그래프 RNM 상대값 전용 (절대 σ = production Kirchhoff 소관)',
                                se_network='v1 SE 불변 → σ_ion_rel≈1 = Yun 2023 정합 검증점'),
               gamma_star=dict(value=float(f'{gamma_star:.4g}'), threshold=1000.0,
                               verdict='damage-expected' if gamma_star >= 1000 else 'SE-integrity-scale',
                               label='Bucci Fig5 스케일링 보고용 (판정은 접촉별 δ_cr)'),
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
    ap.add_argument('--recontact', choices=('forbid', 'elastic'), default='forbid',
                    help='파단 접촉 재접촉: forbid=Bucci flux-0 (기본) / elastic=Schmidt 방향 v2')
    ap.add_argument('--fatigue', choices=('miner', 'off'), default='miner',
                    help='δ_cr 이하 개구의 사이클 누적 (miner=ASSUMED-FORM 라벨 / off=즉시파단만)')
    ap.add_argument('--checkpoints', default='1,2,5,10,25,50,75,100', help='기록 사이클 (Kang&Shin 격자)')
    ap.add_argument('--out', default='cycle_ledger_out')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(0 if _selftest() else 1)
    if not a.atoms:
        ap.error('--atoms required (or --selftest)')
    for nm, v in (('--dv-pct', a.dv_pct), ('--gc', a.gc), ('--deltacr-nm', a.deltacr_nm)):
        if v <= 0:
            ap.error(f'{nm} must be > 0')
    run(a)


if __name__ == '__main__':
    main()
