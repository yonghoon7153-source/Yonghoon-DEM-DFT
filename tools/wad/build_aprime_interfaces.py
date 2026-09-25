#!/usr/bin/env python3
"""build_aprime_interfaces.py — A′ 파일럿 계면 모델 빌더 + **registry 선택 규칙** (카드 v5 · S1 에서 고정하는 코드).

    python3 tools/wad/build_aprime_interfaces.py --selftest
    python3 tools/wad/build_aprime_interfaces.py --build V2 --out <dir>                  # Ag(111)√3 4층 + graphene 2×2 · registry 4
    python3 tools/wad/build_aprime_interfaces.py --build V3 --term s_outer --out <dir>   # Ag₄ | SE 4층 (정본 이완 좌표) · registry A·B
    python3 tools/wad/build_aprime_interfaces.py --build V4 --term li_outer --out <dir>  # C₆H₆ | SE 4층
    python3 tools/wad/build_aprime_interfaces.py --build V5 --term s_outer --out <dir>   # SE 2층 1×2 + Ag(111) 3층 2√3×7
    python3 tools/wad/build_aprime_interfaces.py --registry <구조> --species S           # 임의 구조에서 규칙 적용 결과만

registry 선택 규칙 (카드 v5 §0 `registry_선택_규칙_결정적` · Codex CB Q4 반영 · **초기 구조에서만**):
  Σ  = 표면 종(species) 원자 중 z_max − z_i < REG_Z_TOL (법선 부호 적용). A = Σ 의 원자 ID 최소.
  B  = Σ∖{A} 의 원자 j 와 면내 이미지 (n_a, n_b) ∈ {−1,0,1}² 전부에 대해 d = |r_j + n·cell − r_A| (면내) 를 구하고,
       d_min 을 먼저 정한 뒤 **전역** 동률 집합 {d − d_min < REG_TIE_TOL} 에서 (원자 ID, n_a, n_b) 사전순 최소.
       중점 m = r_A + ½·Δ (Δ = 그 이미지의 변위) → 분수좌표 [0,1) 로 감는다.
  Σ∖{A} 가 비면 **B 생성을 차단**한다 (창을 넓히거나 다른 registry 로 대체하지 않는다).
끝점 (MoLE): bound 와 far 는 같은 셀. far = 흡착층 +z 강체 이동 Δ 로 직접 간격 ≥ gap · 영상 간격 ≥ gap 이 되게 c 를 정한다
  (c = z_ads,max + Δ − z_sub,min + gap · 결합 끝점도 같은 c). 쌍극자 보정 불연속 구간 = 셀 위끝 [c−1.5, c−0.5] Å (두 끝점 다 빈 공간).

⛔ 이 도구가 못 하는 것: UMA/DFT 를 돌리지 않는다 · 에너지가 없다 · 이완 뒤 구조의 검사는 `se_sym_slab.py --interface_check` ·
   변형률 3 % 규칙은 **거부**만 한다 (예외는 카드에 선언해야 한다) · V5 의 자원 적합성은 여기서 모른다 (프로브가 정한다).
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import se_sym_slab as S  # noqa: E402  (SlabError · fixed_mask_policy · interface_check · build_slab · _read_positions_block)

SlabError = S.SlabError
REPO = S.REPO
REG_Z_TOL = 0.05        # Σ 창 [Å]
REG_TIE_TOL = 1e-3      # 동률 [Å] — 전역 d_min 기준
STRAIN_MAX_PCT = 3.0    # 결정 7 재개 규칙 — 넘으면 빌더가 거부한다
A_AG_PBE_D3 = 4.07045   # 선행 배치 09-25 (db/raw/wad_aprime_prep_2026_09_25)
A_C_PBE_D3 = 2.46604
SE_A = 10.0550956357
RELAXED = {"s_outer": ("db/raw/wad_sese_4L_2026_09_25/s_outer_relaxed_final_coords.txt", "db/structures/wad_se_slabs_4L_2026_09_24/comp1_001_s_outer_L4.vasp", "S"),
           "li_outer": ("db/raw/wad_sese_4L_2026_09_25/li_outer_relaxed_final_coords.txt", "db/structures/wad_se_slabs_4L_2026_09_24/comp1_001_li_outer_L4.vasp", "Li")}
V2_REGISTRIES = {"top_fcc": (0.0, 0.0), "top_hcp": (1 / 3, 2 / 3), "bridge": (0.5, 0.0), "hollow_fcc": (2 / 3, 1 / 3)}   # Ag 표면 원시 격자 좌표


# ─────────────────────────────── registry 규칙 ───────────────────────────────
def _images_inplane(dr, cell):
    a, b = cell[0, :2], cell[1, :2]
    out = []
    for na in (-1, 0, 1):
        for nb in (-1, 0, 1):
            v = dr[:2] + na * a + nb * b
            out.append((float(np.hypot(v[0], v[1])), na, nb, v))
    return out


def wrap_frac_inplane(xy, cell):
    M = cell[:2, :2]
    f = np.linalg.solve(M.T, np.asarray(xy, float))
    f = f - np.floor(f)
    f[np.isclose(f, 1.0)] = 0.0
    return f, f @ M


def registry_select(atoms, species, sgn=1.0, z_tol=REG_Z_TOL, tie_tol=REG_TIE_TOL, candidate_order=None):
    """규칙 그대로 (docstring 맨 위). candidate_order 는 시험용 — 후보 순회 순서를 바꿔도 결과가 같아야 한다."""
    sym = np.array(atoms.get_chemical_symbols())
    x = atoms.get_positions()
    C = atoms.cell.array
    if not np.isfinite(x).all() or not np.isfinite(C).all():
        raise SlabError("좌표/셀에 NaN")
    m = sym == species
    if not m.any():
        raise SlabError(f"표면 종 {species} 원자가 없다")
    zs = sgn * x[:, 2]
    zmax = float(zs[m].max())
    Sigma = sorted(int(i) for i in np.where(m & (zmax - zs < z_tol))[0])
    a = Sigma[0]
    cands = [j for j in Sigma if j != a]
    if not cands:
        raise SlabError(f"Σ∖{{A}} 가 비었다 (Σ = {Sigma}) — B 생성 차단 · 창을 넓히거나 다른 registry 로 대체하지 않는다 (CB Q4)")
    if candidate_order is not None:
        cands = [cands[k] for k in candidate_order]
    rows = []
    for j in cands:
        for d, na, nb, v in _images_inplane(x[j] - x[a], C):
            rows.append((d, j, na, nb, v))
    dmin = min(r[0] for r in rows)
    ties = sorted([r for r in rows if r[0] - dmin < tie_tol], key=lambda r: (r[1], r[2], r[3]))
    d, j, na, nb, v = ties[0]
    mid = x[a][:2] + 0.5 * v
    frac, mid_w = wrap_frac_inplane(mid, C)
    return {"species": species, "z_tol_A": z_tol, "tie_tol_A": tie_tol, "Sigma": Sigma, "A": a, "A_xy_A": [round(float(t), 4) for t in x[a][:2]],
            "B_neighbor": int(j), "B_image": [int(na), int(nb)], "d_min_A": round(dmin, 4), "n_ties": len(ties),
            "tie_set": [(int(r[1]), int(r[2]), int(r[3])) for r in ties], "delta_mic_A": [round(float(v[0]), 4), round(float(v[1]), 4)],
            "midpoint_xy_A": [round(float(t), 4) for t in mid_w], "midpoint_frac": [round(float(t), 6) for t in frac],
            "z_surface_A": round(float(sgn * zmax), 4)}


# ─────────────────────────────── 조각·층 ───────────────────────────────
def se_slab_from_relaxed(term):
    """정본 4층 슬랩 — 셀은 구조 파일, 좌표는 V100 PBE 이완 최종 좌표 (sha 는 manifest 에)."""
    from ase import Atoms
    from ase.io import read
    txt, vasp, sp = RELAXED[term]
    cell = read(os.path.join(REPO, vasp)).cell.array
    sym, x = S._read_positions_block(open(os.path.join(REPO, txt), encoding="utf-8").read())
    at = Atoms(sym, positions=x, cell=cell, pbc=(True, True, False))
    at.info["source"] = txt
    at.info["source_sha256"] = hashlib.sha256(open(os.path.join(REPO, txt), "rb").read()).hexdigest()
    return at, sp


def ag4_tetrahedron(edge=2.89):
    from ase import Atoms
    e = edge
    p = np.array([[0, 0, 0], [e, 0, 0], [e / 2, e * np.sqrt(3) / 2, 0], [e / 2, e * np.sqrt(3) / 6, e * np.sqrt(2 / 3)]])
    p -= p[:3].mean(axis=0)
    return Atoms("Ag4", positions=p)


def benzene_flat():
    from ase.build import molecule
    m = molecule("C6H6")
    x = m.get_positions() - m.get_positions().mean(axis=0)
    _, _, vt = np.linalg.svd(x)
    n = vt[2]                                   # 평면 법선 → z 로
    z = np.array([0, 0, 1.0])
    v = np.cross(n, z); s = np.linalg.norm(v); c = float(n @ z)
    if s > 1e-8:
        K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        R = np.eye(3) + K + K @ K * ((1 - c) / s ** 2)
        x = x @ R.T
    m.set_positions(x)
    return m


def ag111_root_slab(a_ag, layers=4):
    from ase.build import fcc111_root
    s = fcc111_root("Ag", 3, size=(1, 1, layers), a=a_ag, vacuum=None)
    x = s.get_positions(); x[:, 2] -= x[:, 2].min(); s.set_positions(x)
    return s


def graphene_2x2_in_cell(cell2, a_c):
    """60° 육방 셀(cell2 = 2×2 in-plane 벡터) 안의 그래핀 2×2 (8 C) · 변형률 = L/(2a_C) − 1."""
    L = float(np.linalg.norm(cell2[0]))
    strain = 100 * (L / (2 * a_c) - 1)
    fr = []
    for i in range(2):
        for j in range(2):
            fr.append([(i + 0.0) / 2, (j + 0.0) / 2])
            fr.append([(i + 1 / 3) / 2, (j + 1 / 3) / 2])
    xy = np.array(fr) @ cell2[:2, :2]
    return xy, strain


def ag111_rect_slab(a_ag, nx=7, ny=4, layers=3):
    """직교 fcc(111) 셀 (ASE orthogonal) → 축 교환해 x 짧은 쪽(2√3·a_s) · y 긴 쪽(7·a_s)."""
    from ase.build import fcc111
    s = fcc111("Ag", size=(nx, ny, layers), a=a_ag, orthogonal=True, vacuum=None)
    x = s.get_positions().copy(); C = s.cell.array.copy()
    x[:, [0, 1]] = x[:, [1, 0]]                                   # 축 교환
    C2 = np.zeros((3, 3)); C2[0, 0] = C[1, 1]; C2[1, 1] = C[0, 0]; C2[2, 2] = 0.0
    x[:, 2] -= x[:, 2].min()
    s.set_cell(C2); s.set_positions(x)
    return s


def _top_layer_primitive(sub, tol=0.3):
    """최상층 원자들에서 표면 원시 벡터 p1·p2 (60°) 를 낸다 (최근접 6 방향 · p1 = 극각 최소 ≥ 0)."""
    x = sub.get_positions(); C = sub.cell.array
    top = np.where(x[:, 2] > x[:, 2].max() - tol)[0]
    t0 = int(top.min())
    vecs = []
    for j in top:
        for d, na, nb, v in _images_inplane(x[j] - x[t0], C):
            if d > 1e-6:
                vecs.append((d, v))
    dmin = min(d for d, _ in vecs)
    nn = [v for d, v in vecs if d - dmin < 1e-3]
    ang = sorted(((np.degrees(np.arctan2(v[1], v[0])) % 360.0), v) for v in nn)
    p1 = ang[0][1]
    a1 = ang[0][0]
    p2 = min(ang[1:], key=lambda t: abs((t[0] - a1) % 360.0 - 60.0))[1]
    return t0, p1, p2


# ─────────────────────────────── 끝점 ───────────────────────────────
def make_endpoints(bound, is_ads, gap=8.0, margin=1.0, dip_top=(1.5, 0.5)):
    """bound(흡착층 +z) → (bound′, far, meta). 같은 셀 · far = 흡착층 +Δ · 직접·영상 간격 ≥ gap · c 결정."""
    x = bound.get_positions().copy()
    z_sub_min, z_sub_max = x[~is_ads, 2].min(), x[~is_ads, 2].max()
    z_ads_min, z_ads_max = x[is_ads, 2].min(), x[is_ads, 2].max()
    d0 = float(z_ads_min - z_sub_max)
    if d0 <= 0:
        raise SlabError("흡착층이 기판 위에 있지 않다 (직접 간격 ≤ 0)")
    delta = max(0.0, gap - d0)
    c = float(z_ads_max + delta - z_sub_min + gap + margin)
    shift = margin / 2 - z_sub_min
    C = bound.cell.array.copy(); C[2] = [0.0, 0.0, c]
    b = bound.copy(); xb = x.copy(); xb[:, 2] += shift; b.set_cell(C); b.set_positions(xb); b.set_pbc((True, True, False))
    f = b.copy(); xf = xb.copy(); xf[is_ads, 2] += delta; f.set_positions(xf)
    def gaps(at):
        y = at.get_positions()
        direct = float(y[is_ads, 2].min() - y[~is_ads, 2].max())
        image = float(at.cell.array[2, 2] - (y[is_ads, 2].max() - y[~is_ads, 2].min()))
        return round(direct, 4), round(image, 4)
    gb, gf = gaps(b), gaps(f)
    if gf[0] < gap - 1e-6 or gf[1] < gap - 1e-6:
        raise SlabError(f"far 끝점 간격 부족 직접 {gf[0]} · 영상 {gf[1]} < {gap}")
    lo, hi = c - dip_top[0], c - dip_top[1]
    top_atom = max(xb[:, 2].max(), xf[:, 2].max())
    if top_atom >= lo:
        raise SlabError("쌍극자 보정 불연속 구간에 원자가 있다")
    meta = {"c_A": round(c, 4), "delta_A": round(delta, 4), "d0_A": round(d0, 4), "gap_rule_A": gap,
            "bound_gap_direct_image_A": gb, "far_gap_direct_image_A": gf,
            "dipfield": {"tefield": True, "dipfield": True, "edir": 3, "eamp": 0.0, "emaxpos": round(lo / c, 5), "eopreg": round((hi - lo) / c, 5),
                         "region_A": [round(lo, 3), round(hi, 3)], "empty_in_both_endpoints": True}}
    return b, f, meta


# ─────────────────────────────── 모델 ───────────────────────────────
def _strain_guard(eps_pct, what):
    bad = [e for e in np.atleast_1d(eps_pct) if abs(e) > STRAIN_MAX_PCT]
    if bad:
        raise SlabError(f"{what}: 변형률 {[round(float(e), 3) for e in np.atleast_1d(eps_pct)]} % 가 {STRAIN_MAX_PCT} % 를 넘는다 — 결정 7 재개 규칙 · 예외는 카드에 선언해야 한다")


def build_v2(a_ag=A_AG_PBE_D3, a_c=A_C_PBE_D3, d0=3.3, gap=8.0, layers=4):
    """V2: Ag(111) (√3×√3)R30° layers 층 + graphene 2×2 (Ag 에 맞춤) · registry 4 · fixed = far_half(Ag) · lateral = C 전부."""
    from ase import Atoms
    sub = ag111_root_slab(a_ag, layers)
    xy_c, strain = graphene_2x2_in_cell(sub.cell.array, a_c)
    _strain_guard([strain], "V2 graphene on Ag(111)√3")
    t0, p1, p2 = _top_layer_primitive(sub)
    z_top = sub.get_positions()[:, 2].max()
    out = {}
    for name, (f1, f2) in V2_REGISTRIES.items():
        shift = f1 * p1 + f2 * p2
        anchor = sub.get_positions()[t0, :2] + shift
        xy = xy_c - xy_c[0] + anchor                   # C0 (인덱스 최소) 가 기준 Ag(t0) 바로 위 + registry 이동
        pos = np.column_stack([xy, np.full(len(xy), z_top + d0)])
        gr = Atoms("C" * len(xy), positions=pos)
        bound = sub + gr
        bound.set_cell(sub.cell.array); bound.set_pbc((True, True, False))
        is_ads = np.array([s == "C" for s in bound.get_chemical_symbols()])
        b, f, em = make_endpoints(bound, is_ads, gap)
        fixed = S.fixed_mask_policy(b, ads_elements=("C",), substrate_elements=("Ag",))
        lateral = [int(i) for i in np.where(is_ads)[0]]
        chk = S.interface_check(b, f, ads_elements=("C",), substrate_elements=("Ag",), fixed_idx=fixed, lateral_fixed_idx=lateral)
        out[name] = {"bound": b, "far": f, "meta": {"model": "V2", "registry": name, "shift_frac_primitive": [f1, f2], "shift_A": [round(float(shift[0]), 4), round(float(shift[1]), 4)],
                                                    "anchor_Ag_index": t0, "anchor_C_index": int(np.where(is_ads)[0][0]), "a_Ag_A": a_ag, "a_C_A": a_c, "graphene_strain_pct": round(strain, 3),
                                                    "n_Ag": int((~is_ads).sum()), "n_C": int(is_ads.sum()), "fixed_idx": fixed, "lateral_fixed_idx": lateral,
                                                    "d0_A": d0, "endpoints": em, "interface_check_flags": chk["flags"]}}
    return out


def _place_fragment(sub, frag, xy_target, height):
    from ase import Atoms
    x = frag.get_positions().copy()
    x[:, :2] -= x[:, :2].mean(axis=0); x[:, :2] += xy_target
    x[:, 2] += (sub.get_positions()[:, 2].max() + height) - x[:, 2].min()
    fr = Atoms(frag.get_chemical_symbols(), positions=x)
    bound = sub + fr
    bound.set_cell(sub.cell.array); bound.set_pbc((True, True, False))
    return bound


def build_v34(kind, term, d0=2.8, gap=8.0):
    """V3 (Ag₄) / V4 (C₆H₆) 조각을 정본 4층 SE 슬랩 +z 면 위 registry A·B 에."""
    sub, sp = se_slab_from_relaxed(term)
    reg = registry_select(sub, sp, sgn=1.0)
    frag = ag4_tetrahedron() if kind == "V3" else benzene_flat()
    ads_el = ("Ag",) if kind == "V3" else ("C", "H")
    out = {}
    for name, xy in (("A", reg["A_xy_A"]), ("B", reg["midpoint_xy_A"])):
        bound = _place_fragment(sub, frag, np.array(xy), d0)
        is_ads = np.array([s in ads_el for s in bound.get_chemical_symbols()])
        b, f, em = make_endpoints(bound, is_ads, gap)
        fixed = S.fixed_mask_policy(b, ads_elements=ads_el)
        chk = S.interface_check(b, f, ads_elements=ads_el, fixed_idx=fixed)
        out[name] = {"bound": b, "far": f, "meta": {"model": kind, "term": term, "registry": name, "registry_rule": reg, "fragment": frag.get_chemical_formula(),
                                                    "n_sub": int((~is_ads).sum()), "n_ads": int(is_ads.sum()), "fixed_idx": fixed, "lateral_fixed_idx": [],
                                                    "substrate_source": sub.info["source"], "substrate_source_sha256": sub.info["source_sha256"],
                                                    "lateral_image_gap_A": round(float(np.linalg.norm(sub.cell.array[0]) - (frag.get_positions()[:, :2].max(axis=0) - frag.get_positions()[:, :2].min(axis=0)).max()), 3),
                                                    "d0_A": d0, "endpoints": em, "interface_check_flags": chk["flags"]}}
    return out


def build_v5(term, a_ag=A_AG_PBE_D3, d0=2.8, gap=8.0, ag_layers=3, vacuum_tmp=16.0):
    """V5: SE 2층 (새 절단 · se_sym_slab.build_slab n_layers=2) 1×2 + Ag(111) 3층 2√3×7 (SE 에 맞춤) · registry A·B."""
    from ase.io import read
    bulk = read(S.BULK_DEFAULT)
    slab, smeta = S.build_slab(bulk, term, n_layers=2, vacuum=vacuum_tmp)
    sub = slab.repeat((1, 2, 1))
    sp = RELAXED[term][2]
    reg = registry_select(sub, sp, sgn=1.0)
    ag = ag111_rect_slab(a_ag, 7, 4, ag_layers)
    Cag = ag.cell.array.copy(); Cse = sub.cell.array
    eps = [100 * (Cse[0, 0] / Cag[0, 0] - 1), 100 * (Cse[1, 1] / Cag[1, 1] - 1)]
    _strain_guard(eps, "V5 Ag(111) 2√3×7 on SE 1×2")
    x = ag.get_positions().copy(); x[:, 0] *= Cse[0, 0] / Cag[0, 0]; x[:, 1] *= Cse[1, 1] / Cag[1, 1]
    bottom = np.where(x[:, 2] < x[:, 2].min() + 0.3)[0]; anchor = int(bottom.min())
    out = {}
    for name, xy in (("A", reg["A_xy_A"]), ("B", reg["midpoint_xy_A"])):
        from ase import Atoms
        y = x.copy(); y[:, :2] += np.array(xy) - y[anchor, :2]
        y[:, 2] += (sub.get_positions()[:, 2].max() + d0) - y[:, 2].min()
        agl = Atoms("Ag" * len(y), positions=y)
        bound = sub + agl
        bound.set_cell(Cse); bound.set_pbc((True, True, False))
        is_ads = np.array([s == "Ag" for s in bound.get_chemical_symbols()])
        b, f, em = make_endpoints(bound, is_ads, gap)
        fixed = S.fixed_mask_policy(b, ads_elements=("Ag",))
        chk = S.interface_check(b, f, ads_elements=("Ag",), fixed_idx=fixed)
        out[name] = {"bound": b, "far": f, "meta": {"model": "V5", "term": term, "registry": name, "registry_rule": reg, "se_layers": 2, "se_lateral": [1, 2],
                                                    "se_cut_meta": smeta, "n_se": int((~is_ads).sum()), "n_Ag": int(is_ads.sum()), "ag_layers": ag_layers,
                                                    "ag_strain_pct_x_y": [round(e, 3) for e in eps], "anchor_Ag_index_in_layer": anchor, "fixed_idx": fixed, "lateral_fixed_idx": [],
                                                    "d0_A": d0, "endpoints": em, "interface_check_flags": chk["flags"]}}
    return out


def write_models(out_dir, models):
    from ase.io import write
    os.makedirs(out_dir, exist_ok=True)
    man = {"tool": os.path.basename(__file__), "constants": {"REG_Z_TOL": REG_Z_TOL, "REG_TIE_TOL": REG_TIE_TOL, "STRAIN_MAX_PCT": STRAIN_MAX_PCT, "A_AG_PBE_D3": A_AG_PBE_D3, "A_C_PBE_D3": A_C_PBE_D3}, "models": {}}
    for name, m in models.items():
        d = os.path.join(out_dir, name); os.makedirs(d, exist_ok=True)
        for k in ("bound", "far"):
            write(os.path.join(d, f"{k}.extxyz"), m[k])
        meta = dict(m["meta"])
        meta["sha256"] = {k: hashlib.sha256(open(os.path.join(d, f"{k}.extxyz"), "rb").read()).hexdigest() for k in ("bound", "far")}
        json.dump(meta, open(os.path.join(d, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
        man["models"][name] = meta
    json.dump(man, open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return man


# ─────────────────────────────── selftest ───────────────────────────────
def _selftest():
    from ase import Atoms
    n_ok, n_bad = 0, 0

    def ck(name, cond, info=""):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  ✗ {name} {info}")

    def sq(L, pts, syms):
        at = Atoms(syms, positions=[[p[0], p[1], 0.0] for p in pts], cell=[[L, 0, 0], [0, L, 0], [0, 0, 20]], pbc=(True, True, False))
        return at
    # ① 주기 반례 (CB Q4): x 0.1 · 9.9 → 최소영상 Δ −0.2 · 중점 0.0 (5.0 아님)
    r = registry_select(sq(10, [(0.1, 2.0), (9.9, 2.0)], "SS"), "S")
    ck("registry ①: 주기 반례 — 중점 0.0 (감기) · d 0.2 · 이미지 (−1,0)", abs(r["midpoint_xy_A"][0]) < 1e-6 and abs(r["d_min_A"] - 0.2) < 1e-6 and r["B_image"] == [-1, 0], r)
    ck("registry ①: 좌표 평균(5.0)이 아니다", abs(r["midpoint_xy_A"][0] - 5.0) > 1, r["midpoint_xy_A"])
    # ② 전역 d_min 동률 집합: 거리 1.0000 (ID 3) · 1.0008 (ID 1) · 1.0016 (ID 2) → 동률 {3,1} → ID 최소 1 (쌍끼리 잇는 방식이면 2 도 들어간다)
    at = sq(30, [(10.0, 10.0), (10.0, 11.0008), (10.0, 8.9984), (11.0, 10.0)], "SSSS")   # A=0 · ID1 d=1.0008 · ID2 d=1.0016 · ID3 d=1.0000
    r = registry_select(at, "S")
    ck("registry ②: 전역 동률 집합 = {ID3 1.0000, ID1 1.0008} (1.0016 제외) → ID 1 선택", r["n_ties"] == 2 and r["B_neighbor"] == 1 and set(t[0] for t in r["tie_set"]) == {1, 3}, r)
    # ③ 후보 순회 순서를 바꿔도 같은 결과
    r2 = registry_select(at, "S", candidate_order=[2, 0, 1])
    ck("registry ③: 후보 순서 바꿔도 동일 (B·이미지·중점)", (r2["B_neighbor"], r2["B_image"], r2["midpoint_xy_A"]) == (r["B_neighbor"], r["B_image"], r["midpoint_xy_A"]))
    # ④ 같은 원자 두 이미지 동률 → 이미지 오프셋 사전순 최소
    r = registry_select(sq(10, [(0.0, 0.0), (5.0, 0.0)], "SS"), "S")
    ck("registry ④: 같은 j 두 이미지 동률(5.0) → (−1,0) 선택 · 중점 감기 7.5", r["n_ties"] == 2 and r["B_image"] == [-1, 0] and abs(r["midpoint_xy_A"][0] - 7.5) < 1e-6, r)
    # ⑤ Σ∖{A} 비면 차단
    try:
        registry_select(sq(10, [(1.0, 1.0), (5.0, 5.0)], "SS").copy(), "S")  # 두 S 가 같은 z → Σ 2 개 → 통과해야 함
        one = sq(10, [(1.0, 1.0), (5.0, 5.0)], "SS"); p = one.get_positions(); p[1, 2] = -1.0; one.set_positions(p)   # 두 번째를 0.05 밖으로
        registry_select(one, "S"); bad = False
    except SlabError as e:
        bad = "차단" in str(e)
    ck("⛔음성 registry ⑤: Σ∖{A} 비면 SlabError (창 확대·대체 없음)", bad)
    try:
        registry_select(sq(10, [(1.0, 1.0)], "S"), "Xx"); bad = False
    except SlabError:
        bad = True
    ck("⛔음성 registry: 없는 종 → SlabError", bad)
    # ⑥ 실제 4층 슬랩
    for term, want in (("s_outer", (108, 109)), ("li_outer", (93, 94))):
        sub, sp = se_slab_from_relaxed(term)
        r = registry_select(sub, sp)
        ck(f"registry ⑥ 실제 {term}: Σ={list(want)} · A={want[0]} · B={want[1]}", tuple(r["Sigma"]) == want and r["A"] == want[0] and r["B_neighbor"] == want[1], r)
    # ⑦ V2
    v2 = build_v2()
    m = v2["top_fcc"]["meta"]
    ck("V2: 12 Ag + 8 C · 그래핀 변형률 +1.08 %", m["n_Ag"] == 12 and m["n_C"] == 8 and abs(m["graphene_strain_pct"] - 1.078) < 0.01, m)
    ck("V2: 고정 = Ag 아래 2층 (6) · 측방 = C 8 · interface_check 깃발 0 (4 registry)", all(len(v["meta"]["fixed_idx"]) == 6 and len(v["meta"]["lateral_fixed_idx"]) == 8 and not v["meta"]["interface_check_flags"] for v in v2.values()))
    anchors = {tuple(np.round(v["bound"].get_positions()[v["meta"]["anchor_C_index"], :2], 3)) for v in v2.values()}
    ck("V2: registry 4 개의 C0 위치가 서로 다르다", len(anchors) == 4, anchors)
    ep = m["endpoints"]
    ck("V2: 끝점 — far 직접·영상 간격 ≥ 8 · 쌍극자 구간 빈 공간", ep["far_gap_direct_image_A"][0] >= 8 and ep["far_gap_direct_image_A"][1] >= 8 and ep["dipfield"]["empty_in_both_endpoints"], ep)
    try:
        build_v2(a_c=2.35); bad = False
    except SlabError as e:
        bad = "변형률" in str(e)
    ck("⛔음성 V2: 그래핀 격자 2.35 → 변형률 > 3 % → 거부", bad)
    # ⑧ V3 · V4
    v3 = build_v34("V3", "s_outer"); m = v3["A"]["meta"]
    ck("V3: 110 + Ag₄ · registry A 위 · 깃발 0 · 마스크 = 정책", m["n_sub"] == 110 and m["n_ads"] == 4 and not m["interface_check_flags"] and m["registry_rule"]["A"] == 108, m["interface_check_flags"])
    xa = v3["A"]["bound"].get_positions(); ia = [i for i, s in enumerate(v3["A"]["bound"].get_chemical_symbols()) if s == "Ag"]
    ck("V3: Ag₄ 무게중심 xy 가 A(108) 위", np.allclose(xa[ia, :2].mean(axis=0), np.array(m["registry_rule"]["A_xy_A"]), atol=1e-3))
    v4 = build_v34("V4", "li_outer"); m4 = v4["B"]["meta"]
    ck("V4: 98 + C₆H₆(12) · registry B(중점) · 깃발 0", m4["n_sub"] == 98 and m4["n_ads"] == 12 and not m4["interface_check_flags"], m4["interface_check_flags"])
    # ⑨ V5
    v5 = build_v5("s_outer"); m5 = v5["A"]["meta"]
    ck("V5: SE 2층 1×2 (116) + Ag 84 = 200 · 변형률 +0.85/−0.19 % · 깃발 0", m5["n_se"] == 116 and m5["n_Ag"] == 84 and abs(m5["ag_strain_pct_x_y"][0] - 0.848) < 0.01 and abs(m5["ag_strain_pct_x_y"][1] + 0.186) < 0.01 and not m5["interface_check_flags"], (m5["n_se"], m5["n_Ag"], m5["ag_strain_pct_x_y"], m5["interface_check_flags"]))
    ck("V5: 고정 마스크 = SE 아래 절반 (Ag 없음)", all(i < 116 for i in m5["fixed_idx"]) and 0 < len(m5["fixed_idx"]) < 116, len(m5["fixed_idx"]))
    # ⑩ 결정성: 두 번 빌드 → 같은 좌표
    b1 = build_v34("V3", "s_outer")["B"]["bound"].get_positions(); b2 = build_v34("V3", "s_outer")["B"]["bound"].get_positions()
    ck("결정성: 같은 입력 → 같은 좌표 (V3 B)", np.allclose(b1, b2))
    print(f"{'✅' if n_bad == 0 else '⛔'} build_aprime_interfaces selftest {n_ok}/{n_ok + n_bad} 통과")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--build", choices=["V2", "V3", "V4", "V5"])
    ap.add_argument("--term", choices=["s_outer", "li_outer"], default="s_outer")
    ap.add_argument("--out")
    ap.add_argument("--a_ag", type=float, default=A_AG_PBE_D3)
    ap.add_argument("--a_c", type=float, default=A_C_PBE_D3)
    ap.add_argument("--gap", type=float, default=8.0)
    ap.add_argument("--registry", metavar="STRUCT", help="임의 구조에 규칙만 적용해 JSON 출력")
    ap.add_argument("--species", default="S")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.registry:
        from ase.io import read
        print(json.dumps(registry_select(read(a.registry), a.species), ensure_ascii=False, indent=1, default=float))
        return 0
    if a.build:
        if not a.out:
            ap.error("--out 이 필요하다")
        if a.build == "V2":
            models = build_v2(a.a_ag, a.a_c, gap=a.gap)
        elif a.build in ("V3", "V4"):
            models = build_v34(a.build, a.term, gap=a.gap)
        else:
            models = build_v5(a.term, a.a_ag, gap=a.gap)
        man = write_models(a.out, models)
        for k, v in man["models"].items():
            print(f"✓ {a.build}/{k}: 원자 {v.get('n_sub', v.get('n_se', v.get('n_Ag')))}+{v.get('n_ads', v.get('n_C', v.get('n_Ag')))} · c {v['endpoints']['c_A']} Å · far 간격 {v['endpoints']['far_gap_direct_image_A']} · 깃발 {v['interface_check_flags']}")
        print(f"→ {a.out}/manifest.json")
        return 0
    ap.error("--selftest · --build · --registry 중 하나")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SlabError as e:
        print(f"⛔ {e}")
        sys.exit(2)
