#!/usr/bin/env python3
"""build_aprime_interfaces.py — A′ 파일럿 계면 모델 빌더 + **registry 선택 규칙** (카드 v5 · S1 에서 고정하는 코드).

    python3 tools/wad/build_aprime_interfaces.py --selftest
    python3 tools/wad/build_aprime_interfaces.py --build V2 --out <dir>                  # Ag(111)√3 4층 + graphene 2×2 · registry 4
    python3 tools/wad/build_aprime_interfaces.py --build V3 --term s_outer --out <dir>   # Ag₄ | SE 4층 (정본 이완 좌표) · registry A·B
    python3 tools/wad/build_aprime_interfaces.py --build V4 --term li_outer --out <dir>  # C₆H₆ | SE 4층
    python3 tools/wad/build_aprime_interfaces.py --build V5 --term s_outer --out <dir>   # SE 2층 1×2 + Ag(111) 3층 2√3×7
    python3 tools/wad/build_aprime_interfaces.py --build P2S --term s_outer --out <dir>  # P2′ 작은 탄소 (외주 2차): SE 2층 1×3 + 흑연 AB 2층 · registry A 하나
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
DIP_WIDTH_A = 1.0        # 쌍극자 보정 톱니 불연속 구간(eopreg) 폭
DIP_MIN_CLEAR_A = 4.0    # 구간 가장자리 ↔ 어느 핵이든 최소 거리 (흡착층 꼭대기 · 기판 바닥의 주기 영상)


def dip_region(structs, width=DIP_WIDTH_A, min_clear=DIP_MIN_CLEAR_A):
    """쌍극자 보정(tefield+dipfield · edir 3) 톱니의 **불연속 구간을 진공 한가운데**에 놓는다 (개정 2 · 2026-09-26).

    structs = 같은 c · 같은 기판 바닥을 공유하는 구조 집합 (bound · far · G3 변형 …) — 집합 전체가 **같은** 구간을 쓴다.
    중심 = (집합의 최고 원자 z + (c + 최저 원자 z)) / 2, 즉 가장 높은 흡착층 꼭대기와 기판 바닥의 **주기 영상** 사이 한가운데.
    가장자리에서 어느 핵까지든 ≥ min_clear 가 아니면 SlabError (조용히 c 를 늘리거나 구간을 옮기지 않는다).
    배경: 종전 규칙 '[c−1.5, c−0.5] Å' 는 기판 바닥(z = margin/2 = 0.5 Å) 의 주기 영상에서 **1.0 Å 아래**여서 Ag 바닥층
    전자밀도 속에 불연속이 놓였고, QE 문서의 경고("change of slope must be in the empty region, or unphysical forces")
    그대로 V2_top_fcc_relax 가 200 스텝 동안 199 오르막 · 고정층 +0.195 Ry/Bohr 로 멈췼다. 종전 검사는 흡착층 쪽만
    보고 `empty_in_both_endpoints: True` 를 상수로 적었다 (한쪽 검사 + 상수 깃발 = 조용히 틀린 경로).
    이 함수가 못 하는 것: 전자밀도를 직접 보지 않는다 — 핵 거리 기준이다 (4 Å 이면 금속·그래핀 꼬리가 표면값의 ~1e-4)."""
    cs = {round(float(a.cell.array[2, 2]), 6) for a in structs}
    if len(cs) != 1:
        raise SlabError(f"dip_region: 구조들의 c 가 다르다 {sorted(cs)}")
    c = cs.pop()
    z_top = max(float(a.get_positions()[:, 2].max()) for a in structs)
    z_bot = min(float(a.get_positions()[:, 2].min()) for a in structs)
    if z_bot < 0 or z_top >= c:
        raise SlabError(f"dip_region: 원자 z 가 셀 [0, c) 밖 (min {z_bot:.3f} · max {z_top:.3f} · c {c:.3f})")
    center = 0.5 * (z_top + c + z_bot)
    lo, hi = center - width / 2, center + width / 2
    clear_top, clear_img = lo - z_top, (c + z_bot) - hi
    if min(clear_top, clear_img) < min_clear - 1e-6:
        raise SlabError(f"dip_region: 불연속 구간 여유 부족 — 흡착층 꼭대기까지 {clear_top:.3f} · 기판 바닥 영상까지 {clear_img:.3f} Å "
                        f"< {min_clear} Å (진공 {c + z_bot - z_top:.3f} Å · 폭 {width} Å)")
    return {"tefield": True, "dipfield": True, "edir": 3, "eamp": 0.0, "emaxpos": round(lo / c, 5), "eopreg": round((hi - lo) / c, 5),
            "region_A": [round(lo, 3), round(hi, 3)], "clearance_A": {"to_top_atom": round(clear_top, 3), "to_substrate_bottom_image": round(clear_img, 3)},
            "min_clear_rule_A": min_clear, "width_A": width, "empty_in_both_endpoints": True,
            "rule": "개정 2 (2026-09-26): 집합의 진공 중앙 · 양쪽 핵 ≥ 4 Å · 폭 1 Å · 집합(bound·far·G3 변형) 이 같은 구간 — dip_region 이 여유를 검사"}


def make_endpoints(bound, is_ads, gap=8.0, margin=1.0):
    """bound(흡착층 +z) → (bound′, far, meta). 같은 셀 · far = 흡착층 +Δ · 직접·영상 간격 ≥ gap · c 결정 · 쌍극자 구간 = dip_region([b, f])."""
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
    meta = {"c_A": round(c, 4), "delta_A": round(delta, 4), "d0_A": round(d0, 4), "gap_rule_A": gap,
            "bound_gap_direct_image_A": gb, "far_gap_direct_image_A": gf,
            "dipfield": dip_region([b, f])}
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


D_GRAPHITE = 3.35       # 흑연 층간 초기값 (cc_graphite.D_INIT 와 같다 · 이완이 정한다)


def graphite_rect_slab(a_c, nx=4, ny=7, layers=3, d=D_GRAPHITE):
    """흑연 AB(ABA…) 직사각 슬랩 — 셀 (nx·a, ny·√3a) · 층당 4·nx·ny 원자 · 첫 층이 z=0.

    직사각 단위 (a, √3a) 의 C 4 개 = 분수좌표 (0,0) (½,⅙) (½,½) (0,⅔) — 최근접 a/√3 · 배위 3.
    B 층은 결합 벡터 (½,⅙) 만큼 민다 (Bernal AB).
    """
    from ase import Atoms
    base = np.array([[0.0, 0.0], [0.5, 1.0 / 6.0], [0.5, 0.5], [0.0, 2.0 / 3.0]])
    shift = np.array([0.5, 1.0 / 6.0])
    A = np.array([a_c, 0.0]); Bv = np.array([0.0, np.sqrt(3.0) * a_c])
    pos = []
    for L in range(layers):
        off = shift if L % 2 == 1 else np.zeros(2)
        for i in range(nx):
            for j in range(ny):
                for f in base:
                    fr = (f + off) % 1.0
                    xy = (fr[0] + i) * A + (fr[1] + j) * Bv
                    pos.append([xy[0], xy[1], L * d])
    cell = [[nx * a_c, 0, 0], [0, ny * np.sqrt(3.0) * a_c, 0], [0, 0, (layers - 1) * d + 10.0]]
    return Atoms("C" * len(pos), positions=pos, cell=cell, pbc=(True, True, False))


def build_full(kind, term, a_ag=A_AG_PBE_D3, a_c=A_C_PBE_D3, d0=None, gap=10.0, ag_layers=4, c_layers=3):
    """P1 (LPSCl|Ag(111)) · P2 (LPSCl|흑연(0001)) **전체 계면** — SE 쌍 UMA+D3 예측 카드 (wad_se_pairs_uma_prediction_card_2026_10_01).

    · SE = 정본 4층 대칭 슬랩 (V100 PBE 이완 좌표 · V3·V4 와 같은 기판) — P1 1×2 · P2 1×3
    · 흡착층을 SE 에 맞춘다 (결정 7): P1 Ag(111) 2√3×7 × ag_layers · P2 흑연 AB 4×7√3 × c_layers
    · registry A·B = registry_select (초기 구조 · V5 와 같은 배치 — 흡착층 첫 층의 최소 ID 원자를 A 위 / A–B 중점 위)
    · 마스크 = SE far_half 만 (흡착층 자유 · V5 와 같다 — interface_check 가 흡착층 고정을 깃발로 본다) · 측방 제약 없음
    · 끝점 = make_endpoints (기본 gap 10 Å — WAD-CC 교훈)
    ⛔ 못 하는 것: 이완·에너지 없음 · 변형률 3 % 넘으면 거부만 한다.
    """
    from ase import Atoms
    if kind not in ("P1", "P2"):
        raise SlabError(f"build_full: 모르는 계면 {kind} (P1 · P2)")
    sub0, sp = se_slab_from_relaxed(term)
    rep = (1, 2, 1) if kind == "P1" else (1, 3, 1)
    sub = sub0.repeat(rep)
    reg = registry_select(sub, sp, sgn=1.0)
    Cse = sub.cell.array
    if kind == "P1":
        ads, el, d0 = ag111_rect_slab(a_ag, 7, 4, ag_layers), "Ag", (2.8 if d0 is None else d0)
        what, n_layers = f"P1 Ag(111) 2√3×7 × {ag_layers} on SE 1×2", ag_layers
    else:
        ads, el, d0 = graphite_rect_slab(a_c, 4, 7, c_layers), "C", (3.2 if d0 is None else d0)
        what, n_layers = f"P2 흑연 AB 4×7√3 × {c_layers} on SE 1×3", c_layers
    Ca = ads.cell.array
    eps = [100 * (Cse[0, 0] / Ca[0, 0] - 1), 100 * (Cse[1, 1] / Ca[1, 1] - 1)]
    _strain_guard(eps, what)
    x = ads.get_positions().copy(); x[:, 0] *= Cse[0, 0] / Ca[0, 0]; x[:, 1] *= Cse[1, 1] / Ca[1, 1]
    bottom = np.where(x[:, 2] < x[:, 2].min() + 0.3)[0]; anchor = int(bottom.min())
    out = {}
    for name, xy in (("A", reg["A_xy_A"]), ("B", reg["midpoint_xy_A"])):
        y = x.copy(); y[:, :2] += np.array(xy) - y[anchor, :2]
        y[:, 2] += (sub.get_positions()[:, 2].max() + d0) - y[:, 2].min()
        bound = sub + Atoms(el * len(y), positions=y)
        bound.set_cell(Cse); bound.set_pbc((True, True, False))
        is_ads = np.array([s == el for s in bound.get_chemical_symbols()])
        b, f, em = make_endpoints(bound, is_ads, gap)
        fixed = S.fixed_mask_policy(b, ads_elements=(el,))
        chk = S.interface_check(b, f, ads_elements=(el,), fixed_idx=fixed)
        out[name] = {"bound": b, "far": f, "meta": {"model": kind, "term": term, "registry": name, "registry_rule": reg, "se_layers": 4, "se_lateral": list(rep[:2]),
                                                    "se_source": sub0.info.get("source"), "se_source_sha256": sub0.info.get("source_sha256"),
                                                    "n_se": int((~is_ads).sum()), "n_ads": int(is_ads.sum()), "ads_element": el, "ads_layers": n_layers,
                                                    "ads_strain_pct_x_y": [round(e, 3) for e in eps], "anchor_ads_index_in_layer": anchor, "fixed_idx": fixed, "lateral_fixed_idx": [],
                                                    "d0_A": d0, "endpoints": em, "interface_check_flags": chk["flags"]}}
    return out


# ─────────────── P2′ 작은 탄소 모델 (외주 2차 카드 wad_p2small_vasp_card_2026_10_15 · 키 'P2S') ───────────────
P05_DZ_A = 0.5          # 카드 §1b · G1p — 이완한 부모 bound 의 흡착층 강체 +z (비이완 탐침)
RIGID_TOL_A = 1e-6      # G1p ① 성분별 허용 [Å]
FORMULA_ORDER = ("Li", "P", "S", "Cl", "C", "Ag", "H")


def _formula(symbols):
    n = {e: 0 for e in FORMULA_ORDER}
    for s in symbols:
        if s not in n:
            raise SlabError(f"_formula: 모르는 원소 {s}")
        n[s] += 1
    return "".join(f"{e}{n[e]}" for e in FORMULA_ORDER if n[e])


def build_p2small(term, a_c=A_C_PBE_D3, d0=3.2, gap=10.0, c_layers=2, vacuum_tmp=16.0):
    """P2′ 작은 탄소 모델 (카드 §1b) — SE 2층 (V5 절단) 1×3 + 흑연 AB 2층 4×7√3 · registry **A 하나**.

    · SE = `se_sym_slab.build_slab(n_layers=2)` (V5 와 같은 절단 · 이완 좌표 아님) × (1,3,1) — P2 전체 계면과 같은 옆 셀
    · 흑연 = graphite_rect_slab 를 SE 에 맞춘다 (P2 와 같은 배치 · 같은 변형) · 첫 층 최소 ID 원자를 registry A 위 · d0 3.2 Å
    · registry A = registry_select 그대로 (같은 종결 V5 의 A 와 같은 원자) — B 는 카드의 비용 선택으로 만들지 않는다
    · 마스크 = SE far_half 만 (흡착층 자유) · 측방 제약 없음 · 끝점 = make_endpoints (기본 gap 10 Å)
    ⛔ 못 하는 것: 이완·에너지 없음 · p05 는 여기서 만들지 않는다 (이완한 부모에서 `p05_probe`) · 변형률 3 % 넘으면 거부만 한다.
    """
    from ase import Atoms
    from ase.io import read
    bulk = read(S.BULK_DEFAULT)
    slab, smeta = S.build_slab(bulk, term, n_layers=2, vacuum=vacuum_tmp)
    sub = slab.repeat((1, 3, 1))
    reg = registry_select(sub, RELAXED[term][2], sgn=1.0)
    ads = graphite_rect_slab(a_c, 4, 7, c_layers)
    Cse, Ca = sub.cell.array, ads.cell.array
    eps = [100 * (Cse[0, 0] / Ca[0, 0] - 1), 100 * (Cse[1, 1] / Ca[1, 1] - 1)]
    _strain_guard(eps, f"P2′ 흑연 AB 4×7√3 × {c_layers} on SE 2층 1×3")
    x = ads.get_positions().copy(); x[:, 0] *= Cse[0, 0] / Ca[0, 0]; x[:, 1] *= Cse[1, 1] / Ca[1, 1]
    bottom = np.where(x[:, 2] < x[:, 2].min() + 0.3)[0]; anchor = int(bottom.min())
    x[:, :2] += np.array(reg["A_xy_A"]) - x[anchor, :2]
    x[:, 2] += (sub.get_positions()[:, 2].max() + d0) - x[:, 2].min()
    bound = sub + Atoms("C" * len(x), positions=x)
    bound.set_cell(Cse); bound.set_pbc((True, True, False))
    is_ads = np.array([s == "C" for s in bound.get_chemical_symbols()])
    b, f, em = make_endpoints(bound, is_ads, gap)
    fixed = S.fixed_mask_policy(b, ads_elements=("C",))
    chk = S.interface_check(b, f, ads_elements=("C",), fixed_idx=fixed)
    sym = b.get_chemical_symbols()
    meta = {"model": "P2S", "card": "wad_p2small_vasp_card_2026_10_15 (P2′)", "term": term, "registry": "A", "registry_rule": reg,
            "se_layers": 2, "se_lateral": [1, 3], "se_cut_meta": smeta,
            "se_formula": _formula([s for s, a in zip(sym, is_ads) if not a]), "n_se": int((~is_ads).sum()), "n_ads": int(is_ads.sum()),
            "ads_element": "C", "ads_layers": c_layers, "ads_strain_pct_x_y": [round(e, 3) for e in eps], "anchor_ads_index_in_layer": anchor,
            "fixed_idx": fixed, "lateral_fixed_idx": [], "d0_A": d0, "endpoints": em, "interface_check_flags": chk["flags"]}
    return {"A": {"bound": b, "far": f, "meta": meta}}


def check_rigid_shift(parent, probe, is_ads, dz=P05_DZ_A, tol=RIGID_TOL_A):
    """G1p ① 강체 이동 정확성 — 흡착층 원자마다 변위 (0, 0, dz) · 기판 변위 0 (성분별 ≤ tol) · 셀·원자 순서·원소 같음.
    봉인 단계가 파일에서 다시 읽은 구조로도 쓴다 (extxyz 는 1e-8 Å 자리까지 쓴다). 반환 dict (ok · violations · 최대 오차)."""
    if len(parent) != len(probe) or len(is_ads) != len(parent):
        return {"ok": False, "violations": [f"원자 수 부모 {len(parent)} · 탐침 {len(probe)} · 마스크 {len(is_ads)}"]}
    is_ads = np.asarray(is_ads, bool)
    bad = []
    if parent.get_chemical_symbols() != probe.get_chemical_symbols():
        bad.append("원소·원자 순서가 다르다")
    if not np.allclose(parent.cell.array, probe.cell.array, rtol=0, atol=tol):
        bad.append("셀이 다르다")
    if not is_ads.any() or is_ads.all():
        bad.append("흡착층·기판 둘 다 있어야 한다")
        return {"ok": False, "violations": bad}
    err = probe.get_positions() - parent.get_positions()
    err[is_ads, 2] -= dz
    e_ads, e_sub = float(np.abs(err[is_ads]).max()), float(np.abs(err[~is_ads]).max())
    if e_ads > tol:
        bad.append(f"흡착층 변위가 (0, 0, {dz}) 에서 {e_ads:.2e} Å 벗어난다 (> {tol})")
    if e_sub > tol:
        bad.append(f"기판 원자가 {e_sub:.2e} Å 움직였다 (> {tol})")
    return {"ok": not bad, "violations": bad, "dz_A": dz, "tol_A": tol, "max_err_ads_A": e_ads, "max_err_sub_A": e_sub,
            "n_ads": int(is_ads.sum()), "n_sub": int((~is_ads).sum())}


def p05_probe(parent_bound, parent_far, dz=P05_DZ_A, gap=10.0, ads_elements=("C",), fixed_idx=None, policy_ref=None):
    """카드 §1b · G1p — 이완한 부모 bound (make_endpoints 로 정규화한 것) 에서 흡착층 전체를 +dz 강체 이동한 **비이완 탐침**.
    far 는 부모와 공유한다 — 같은 규칙 (make_endpoints) 이 탐침에 주는 far 가 부모 far 와 같은지 확인해서 공유를 정당화한다.

    반환 (probe, rec): rec = G1p ① 강체 이동 (check_rigid_shift) · 공유 far 정합 · 쌍극자 구간 (탐침·far 집합 = 부모·far 집합) ·
      G1p ③ interface_check 깃발 (fixed_idx 를 주면 · 마스크 정책 기준 = policy_ref 를 주면 그 구조 = 부모 빌드 초기 구조 ·
      안 주면 탐침 자체 — 이완한 부모의 탐침에서는 중심면이 움직여 동률 원자가 깃발이 된다 · 2026-10-21) · 간격 (직접 +dz · 영상 −dz).
    거부 (SlabError): dz ≤ 0 · 흡착층 꼭대기가 셀 위끝을 넘음 · 부모가 끝점 정규화본이 아님 · 공유 far 불일치 (부모 직접 간격 > gap − dz) ·
      쌍극자 구간 불일치 · 강체 이동 검사 실패.
    ⛔ 못 하는 것: 이완하지 않는다 · sha 사슬 봉인은 부르는 쪽 (S3 와 같은 봉인 단계) 이 한다 — 여기선 변환 기록만 준다.
    """
    if not dz > 0:
        raise SlabError(f"p05_probe: dz {dz} — 계면을 벌리는 강체 인장만 (dz > 0)")
    is_ads = np.array([s in ads_elements for s in parent_bound.get_chemical_symbols()])
    x = parent_bound.get_positions().copy()
    x[is_ads, 2] += dz
    c = float(parent_bound.cell.array[2, 2])
    if x[is_ads, 2].max() >= c:
        raise SlabError(f"p05_probe: 흡착층 꼭대기 {x[is_ads, 2].max():.3f} Å 가 셀 위끝 c {c:.3f} Å 를 넘는다")
    probe = parent_bound.copy(); probe.set_positions(x)
    rig = check_rigid_shift(parent_bound, probe, is_ads, dz)
    if not rig["ok"]:
        raise SlabError(f"p05_probe: 강체 이동 검사 실패 {rig['violations']}")
    bb, ff, em = make_endpoints(probe, is_ads, gap)
    e_bound = float(np.abs(bb.get_positions() - x).max())
    if e_bound > RIGID_TOL_A:
        raise SlabError(f"p05_probe: 부모가 끝점 정규화(make_endpoints) 된 bound 가 아니다 — 탐침을 다시 정규화하면 좌표가 {e_bound:.3e} Å 움직인다")
    dc = float(bb.cell.array[2, 2]) - c
    if abs(dc) > RIGID_TOL_A:
        raise SlabError(f"p05_probe: 공유 far 불일치 — 규칙 (gap {gap}) 이 탐침에 주는 c 가 부모와 {dc:+.4f} Å 다르다 "
                        f"(부모 직접 간격 {em['d0_A'] - dz:.3f} Å 가 gap − dz 를 넘거나 부모의 gap 규칙이 다르다)")
    if len(ff) != len(parent_far) or ff.get_chemical_symbols() != parent_far.get_chemical_symbols():
        raise SlabError("p05_probe: 공유 far 와 원자 수·순서가 다르다")
    e_far = float(np.abs(ff.get_positions() - parent_far.get_positions()).max())
    e_cell = float(np.abs(ff.cell.array - parent_far.cell.array).max())
    if e_far > RIGID_TOL_A or e_cell > RIGID_TOL_A:
        raise SlabError(f"p05_probe: 공유 far 불일치 — 탐침의 규칙 far 와 부모 far 가 {max(e_far, e_cell):.3e} Å 다르다 (부모의 far 가 아니다)")
    d_par, d_pro = dip_region([parent_bound, parent_far]), dip_region([probe, parent_far])
    if (d_par["emaxpos"], d_par["eopreg"]) != (d_pro["emaxpos"], d_pro["eopreg"]):
        raise SlabError(f"p05_probe: 쌍극자 구간이 부모 집합과 다르다 {d_par['region_A']} ≠ {d_pro['region_A']}")

    def gaps(at):
        y = at.get_positions()
        return round(float(y[is_ads, 2].min() - y[~is_ads, 2].max()), 4), round(float(c - (y[is_ads, 2].max() - y[~is_ads, 2].min())), 4)
    rec = {"transform": {"kind": "흡착층 강체 +z (비이완)", "dz_A": dz, "ads_elements": list(ads_elements), "tol_A": RIGID_TOL_A},
           "rigid_check": rig, "shared_far": {"ok": True, "max_err_A": max(e_far, e_cell), "rule": f"make_endpoints(탐침, gap {gap}) 의 far ≡ 부모 far"},
           "dip_same_as_parent": True, "dipfield": d_pro, "gap_direct_image_A": {"parent": gaps(parent_bound), "probe": gaps(probe)}}
    if fixed_idx is not None:
        rec["interface_check_flags"] = S.interface_check(probe, parent_far, ads_elements=ads_elements, fixed_idx=fixed_idx,
                                                         policy_ref=policy_ref)["flags"]
        rec["mask_policy_ref"] = "given" if policy_ref is not None else "probe"
    return probe, rec


# ─────────────── registry 거리 (SE 쌍 카드 §4 '합쳐짐' — 이완 뒤 A·B 가 같은 자리로 모였나) ───────────────
MERGE_TOL_A = 0.2       # SE 쌍 카드 §4 registry_합쳐짐 — 결과 전 문턱


def ads_lattice(kind, cell):
    """P1·P2 흡착층의 면내 브라베 격자 기저 (행 = 벡터 · 셀에서 유도해 변형률이 들어가 있다).
    P1 Ag(111) 2√3×7 (fcc111 직교를 축 교환): (0, a) · (√3a/2, a/2) — a = Ly/7 · √3a/2 = Lx/4.
    P2 흑연 AB 4×7√3: (a, 0) · (a/2, √3a/2) — a = Lx/4 · √3a = Ly/7. 층 적층 (ABC · AB) 도 같은 격자다."""
    C = np.asarray(cell, float)
    Lx, Ly = C[0, 0], C[1, 1]
    if kind == "P1":
        return np.array([[0.0, Ly / 7.0], [Lx / 4.0, Ly / 14.0]])
    if kind == "P2":
        return np.array([[Lx / 4.0, 0.0], [Lx / 8.0, Ly / 14.0]])
    raise SlabError(f"ads_lattice: 모르는 계면 {kind} (P1 · P2)")


def lattice_reduce(v, basis):
    """면내 벡터 v 를 격자 basis (행 2 개 · 줄인 기저) 의 가장 짧은 대표로."""
    v = np.asarray(v, float)[:2]
    b = np.asarray(basis, float)
    f = np.floor(np.linalg.solve(b.T, v))
    cands = [v - (f[0] + i) * b[0] - (f[1] + j) * b[1] for i in (-1, 0, 1, 2) for j in (-1, 0, 1, 2)]
    return min(cands, key=lambda w: float(np.hypot(w[0], w[1])))


def layer_maps_onto(x, t, cell):
    """층 x (N×3) 를 면내 t 만큼 옮겼을 때 각 원자에서 가장 가까운 원래 원자까지 거리의 최댓값 (Å · 주기 xy) — 0 이면 t 는 이 층의 격자 이동."""
    M = np.asarray(cell, float)[:2, :2]
    F = np.linalg.solve(M.T, x[:, :2].T).T
    G = np.linalg.solve(M.T, (x[:, :2] + np.asarray(t, float)[:2]).T).T
    worst = 0.0
    for g in G:
        d = F - g
        d -= np.round(d)
        dd = d @ M
        worst = max(worst, float(np.hypot(dd[:, 0], dd[:, 1]).min()))
    return worst


def _mean_shift(xa, xb, basis):
    """같은 순서의 두 층의 면내 상대 이동 (격자로 줄임) · 원자별 퍼짐 (강체 이동에서 얼마나 벗어났나 · Å)."""
    d = xb[:, :2] - xa[:, :2]
    r0 = lattice_reduce(d[0], basis)
    e = np.array([lattice_reduce(di - r0, basis) for di in d])
    return lattice_reduce(r0 + e.mean(axis=0), basis), float(np.linalg.norm(e - e.mean(axis=0), axis=1).max())


def registry_distance(kind, bound_a, bound_b, relaxed_a, relaxed_b, ads_el, contact_tol=0.5, merge_tol=MERGE_TOL_A):
    """SE 쌍 카드 §4 'registry 합쳐짐' 판정량 — registry A·B 의 흡착층 **접촉층**(첫 층) 면내 상대 위치를 흡착층 격자로 줄인 길이 (Å).

    초기(빌더 bound) 와 이완 뒤(relaxed) 를 둘 다 내고, 이완 뒤 < merge_tol 이면 merged = True (카드: '합쳐짐' 으로 적고 하나로 보고).
    넷은 원자 수·순서·원소가 같아야 한다 (빌더가 같은 순서로 만든다). 격자 기저는 초기 접촉층에 대고 검사한다
    (b1·b2 로 옮기면 제자리 < 1e-3 Å · b1/2 로 옮기면 > 0.3 Å — 아니면 거부: 조용히 틀린 격자를 막는다).
    ⛔ 못 하는 것: SE 쪽 재배열·접촉층 내부 변형은 판정에 안 쓴다 (퍼짐만 보고) · P1·P2 만 안다 · 에너지는 모른다.
    """
    syms = {tuple(a.get_chemical_symbols()) for a in (bound_a, bound_b, relaxed_a, relaxed_b)}
    if len(syms) != 1:
        raise SlabError("registry_distance: 네 구조의 원자 수·순서·원소가 다르다 — 같은 빌더 출력의 A·B 와 그 이완본만 받는다")
    sym = np.array(next(iter(syms)))
    ads = np.where(sym == ads_el)[0]
    if not len(ads):
        raise SlabError(f"registry_distance: 흡착 원소 {ads_el} 이 없다")
    x0a = bound_a.get_positions()
    z = x0a[ads, 2]
    contact = ads[z < z.min() + contact_tol]
    cell = bound_a.cell.array
    basis = ads_lattice(kind, cell)
    lat = {"b1": layer_maps_onto(x0a[contact], basis[0], cell), "b2": layer_maps_onto(x0a[contact], basis[1], cell),
           "half_b1": layer_maps_onto(x0a[contact], 0.5 * basis[0], cell)}
    if max(lat["b1"], lat["b2"]) > 1e-3 or lat["half_b1"] < 0.3:
        raise SlabError(f"registry_distance: {kind} 격자 기저가 이 접촉층의 격자가 아니다 ({lat}) — 판정 안 함")
    d_init, s_init = _mean_shift(x0a[contact], bound_b.get_positions()[contact], basis)
    d_fin, s_fin = _mean_shift(relaxed_a.get_positions()[contact], relaxed_b.get_positions()[contact], basis)
    sc = np.array([cell[0, :2], cell[1, :2]])
    drift = {}
    for k, b0, b1 in (("A", bound_a, relaxed_a), ("B", bound_b, relaxed_b)):
        dv = (b1.get_positions()[contact] - b0.get_positions()[contact])[:, :2]
        drift[k] = [round(float(t), 4) for t in np.mean([lattice_reduce(v, sc) for v in dv], axis=0)]
    fin = float(np.hypot(d_fin[0], d_fin[1]))
    return {"kind": kind, "ads_element": ads_el, "n_contact": int(len(contact)), "contact_tol_A": contact_tol,
            "lattice_basis_A": np.round(basis, 5).tolist(), "lattice_check_A": {k: round(v, 5) for k, v in lat.items()},
            "init_A": round(float(np.hypot(d_init[0], d_init[1])), 4), "final_A": round(fin, 4), "final_vec_A": [round(float(t), 4) for t in d_fin],
            "spread_init_A": round(s_init, 4), "spread_final_A": round(s_fin, 4), "drift_contact_xy_A": drift,
            "merge_tol_A": merge_tol, "merged": bool(fin < merge_tol)}


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
    # ⑦-d 쌍극자 구간 (개정 2 · 2026-09-26): 진공 중앙 · 양쪽 핵 ≥ 4 Å · 종전 '[c−1.5, c−0.5]' 는 기판 바닥 영상 1 Å 아래였다
    from ase import Atoms
    dp, cA = ep["dipfield"], ep["c_A"]
    ck("V2: 쌍극자 구간 = 진공 중앙 · 꼭대기·바닥 영상 양쪽 ≥ 4 Å · 폭 1 Å", dp["clearance_A"]["to_top_atom"] >= 4 - 1e-6 and dp["clearance_A"]["to_substrate_bottom_image"] >= 4 - 1e-6 and abs((dp["region_A"][1] - dp["region_A"][0]) - 1.0) < 2e-3, dp)
    ck("V2: 종전 규칙이 아니다 — 구간 위끝이 바닥 영상(c+0.5) 에서 ≥ 4 Å · emaxpos ≠ (c−1.5)/c", dp["region_A"][1] <= cA + 0.5 - 4 + 1e-6 and abs(dp["emaxpos"] - (cA - 1.5) / cA) > 0.05, (dp["region_A"], cA, dp["emaxpos"]))
    slab = Atoms("Ag2C", positions=[[0, 0, 0.5], [0, 0, 2.9], [0, 0, 6.2]], cell=[[4, 0, 0], [0, 4, 0], [0, 0, 20.0]], pbc=(True, True, False))
    d1 = dip_region([slab])
    ck("dip_region: 중심 = (꼭대기 6.2 + c 20 + 바닥 0.5)/2 = 13.35 · 여유 6.65/6.65", abs(sum(d1["region_A"]) / 2 - 13.35) < 2e-3 and abs(d1["clearance_A"]["to_top_atom"] - 6.65) < 2e-3 and abs(d1["clearance_A"]["to_substrate_bottom_image"] - 6.65) < 2e-3, d1)
    narrow = slab.copy(); C = narrow.cell.array.copy(); C[2, 2] = 12.0; narrow.set_cell(C)
    try:
        dip_region([narrow]); bad = False
    except SlabError as e:
        bad = "여유 부족" in str(e)
    ck("⛔음성 dip_region: 진공 6.3 Å (여유 2.65 < 4) → SlabError (c 확대·구간 이동 없음)", bad)
    other = slab.copy(); C = other.cell.array.copy(); C[2, 2] = 22.0; other.set_cell(C)
    try:
        dip_region([slab, other]); bad = False
    except SlabError as e:
        bad = "c 가 다르다" in str(e)
    ck("⛔음성 dip_region: 집합의 c 가 다르면 SlabError", bad)
    isC = np.array([s == "C" for s in v2["top_fcc"]["bound"].get_chemical_symbols()])
    try:
        make_endpoints(v2["top_fcc"]["bound"], isC, gap=4.0); bad = False
    except SlabError as e:
        bad = "여유 부족" in str(e)
    ck("⛔음성 make_endpoints: gap 4 (영상 간격 5 Å → 여유 2 Å) → 쌍극자 여유 부족으로 거부", bad)
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
    # ⑪ 흑연 직사각 슬랩 (P2 부품): 최근접 a/√3 · 층 안 배위 3 · AB (둘째 층 절반은 첫 층 원자 위)
    g = graphite_rect_slab(A_C_PBE_D3, 4, 7, 3)
    from ase.geometry import get_distances
    p0 = g.get_positions()[g.get_positions()[:, 2] < 0.1]
    _, Dg = get_distances(p0, p0, cell=g.cell, pbc=(True, True, False))
    np.fill_diagonal(Dg, 99.0)
    ck("흑연 직사각: 층당 112 · 3 층 336 · 최근접 a/√3 · 배위 3", len(g) == 336 and len(p0) == 112 and abs(Dg.min() - A_C_PBE_D3 / np.sqrt(3)) < 1e-6
       and int(((Dg < 1.6).sum(axis=1) == 3).all()) == 1, (len(g), len(p0), round(float(Dg.min()), 4)))
    p1 = g.get_positions()[(g.get_positions()[:, 2] > 3.0) & (g.get_positions()[:, 2] < 3.5)]
    _, Dab = get_distances(p1, p0, cell=g.cell, pbc=(True, True, False))
    over = int((Dab.min(axis=1) < 3.35 + 1e-3).sum())
    ck("흑연 직사각: AB — 둘째 층 절반(56)만 첫 층 원자 바로 위", over == 56, over)
    # ⑫ P1 · P2 전체 계면 (SE 쌍 UMA 카드)
    p1m = build_full("P1", "s_outer"); m = p1m["A"]["meta"]
    ck("P1: SE 4층 1×2 (220) + Ag 4층 112 · 변형률 +0.85/−0.19 % · 깃발 0", m["n_se"] == 220 and m["n_ads"] == 112 and abs(m["ads_strain_pct_x_y"][0] - 0.848) < 0.01
       and abs(m["ads_strain_pct_x_y"][1] + 0.186) < 0.01 and not m["interface_check_flags"], (m["n_se"], m["n_ads"], m["ads_strain_pct_x_y"], m["interface_check_flags"]))
    ck("P1: 마스크 = SE 만 (흡착층 자유) · 측방 없음 · far 간격 ≥ 10 Å", all(i < 220 for i in m["fixed_idx"]) and 0 < len(m["fixed_idx"]) < 220 and m["lateral_fixed_idx"] == []
       and min(m["endpoints"]["far_gap_direct_image_A"]) >= 10.0 - 1e-6, (len(m["fixed_idx"]), m["endpoints"]["far_gap_direct_image_A"]))
    ia = [i for i, s in enumerate(p1m["A"]["bound"].get_chemical_symbols()) if s == "Ag"]; ib = [i for i, s in enumerate(p1m["B"]["bound"].get_chemical_symbols()) if s == "Ag"]
    ck("P1: registry A·B 의 흡착층 면내 위치가 다르다", not np.allclose(p1m["A"]["bound"].get_positions()[ia, :2], p1m["B"]["bound"].get_positions()[ib, :2]))
    p2m = build_full("P2", "li_outer"); m2 = p2m["B"]["meta"]
    ck("P2: SE 4층 1×3 (294) + 흑연 3층 336 · 변형률 +1.94/+0.89 % · 깃발 0", m2["n_se"] == 294 and m2["n_ads"] == 336 and abs(m2["ads_strain_pct_x_y"][0] - 1.935) < 0.02
       and abs(m2["ads_strain_pct_x_y"][1] - 0.890) < 0.02 and not m2["interface_check_flags"], (m2["n_se"], m2["n_ads"], m2["ads_strain_pct_x_y"], m2["interface_check_flags"]))
    try:
        build_full("P2", "s_outer", a_c=2.35); bad = False
    except SlabError as e:
        bad = "변형률" in str(e)
    ck("⛔음성 P2: 흑연 격자 2.35 → 변형률 > 3 % → 거부", bad)
    try:
        build_full("P3", "s_outer"); bad = False
    except SlabError as e:
        bad = "모르는 계면" in str(e)
    ck("⛔음성 build_full: 모르는 계면 이름 → 거부", bad)
    q1 = build_full("P1", "li_outer")["A"]["bound"].get_positions(); q2 = build_full("P1", "li_outer")["A"]["bound"].get_positions()
    ck("결정성: P1 li_outer A 두 번 → 같은 좌표", np.allclose(q1, q2))
    # ⑬ registry 거리 (SE 쌍 카드 §4 '합쳐짐' · 0.2 Å)
    A2, B2 = p2m["A"]["bound"], p2m["B"]["bound"]
    bas = ads_lattice("P2", A2.cell.array)

    def moved(at, t, el):
        y = at.copy(); p = y.get_positions(); mk = np.array([q == el for q in y.get_chemical_symbols()]); p[mk, :2] += np.asarray(t, float)[:2]
        y.set_positions(p); return y
    rd = registry_distance("P2", A2, B2, A2, B2, "C")
    ck("registry 거리 P2: 이완본 자리에 초기를 주면 초기 = 이완 · 1.31 Å · 합쳐짐 아님 · 접촉층 112",
       abs(rd["init_A"] - rd["final_A"]) < 1e-9 and abs(rd["init_A"] - 1.307) < 0.01 and not rd["merged"] and rd["n_contact"] == 112, rd)
    rg = p2m["A"]["meta"]["registry_rule"]
    s_mid = np.array(rg["midpoint_xy_A"]) - np.array(rg["A_xy_A"])
    ck("registry 거리 P2: 빌더 이동 (중점 − A) 을 격자로 줄인 길이와 같다", abs(rd["init_A"] - float(np.hypot(*lattice_reduce(s_mid, bas)))) < 1e-3, rd["init_A"])
    rd2 = registry_distance("P2", A2, B2, A2, moved(A2, bas[0] + bas[1], "C"), "C")
    ck("registry 거리: B 이완본 = A 를 격자 벡터만큼 민 것 → 0 · 합쳐짐", rd2["final_A"] < 1e-6 and rd2["merged"], rd2["final_A"])
    rd3 = registry_distance("P2", A2, B2, A2, moved(A2, 0.5 * bas[0], "C"), "C")
    ck("⛔음성 registry 거리: 반 격자 이동은 합쳐짐 아님 (> 0.3 Å)", rd3["final_A"] > 0.3 and not rd3["merged"], rd3["final_A"])
    rd4 = registry_distance("P2", A2, B2, A2, moved(A2, [0.15, 0.0], "C"), "C")
    ck("registry 거리: 0.15 Å 이동 → 0.15 · 합쳐짐 (문턱 0.2 미만)", abs(rd4["final_A"] - 0.15) < 1e-6 and rd4["merged"], rd4["final_A"])
    rd4b = registry_distance("P2", A2, B2, A2, moved(A2, [0.25, 0.0], "C"), "C")
    ck("⛔음성 registry 거리: 0.25 Å 이동 → 합쳐짐 아님 (문턱 0.2 이상)", abs(rd4b["final_A"] - 0.25) < 1e-6 and not rd4b["merged"], rd4b["final_A"])
    try:
        registry_distance("P1", A2, B2, A2, B2, "C"); bad = False
    except SlabError as e:
        bad = "격자 기저" in str(e)
    ck("⛔음성 registry 거리: 흑연에 Ag(111) 격자 → 거부 (조용히 틀린 격자 차단)", bad)
    try:
        registry_distance("P2", A2, p1m["A"]["bound"], A2, B2, "C"); bad = False
    except SlabError as e:
        bad = "원자 수" in str(e)
    ck("⛔음성 registry 거리: 다른 모델을 섞으면 거부", bad)
    rd5 = registry_distance("P1", p1m["A"]["bound"], p1m["B"]["bound"], p1m["A"]["bound"], p1m["B"]["bound"], "Ag")
    ck("registry 거리 P1: 초기 1.08 Å · 접촉층 28 · 격자 검사 통과", abs(rd5["init_A"] - 1.077) < 0.01 and rd5["n_contact"] == 28, rd5)
    # ⑭ P2′ 작은 탄소 모델 (외주 2차 카드 §1b · 조성은 카드에 적힌 식 그대로)
    want = {"s_outer": ("Li84P12S66Cl12", 398), "li_outer": ("Li60P12S54Cl12", 362)}
    ps = {}
    for term, (fse, ntot) in want.items():
        mm = build_p2small(term); ps[term] = mm; m = mm["A"]["meta"]; b = mm["A"]["bound"]
        isC = np.array([s == "C" for s in b.get_chemical_symbols()])
        ck(f"P2′ {term}: registry A 하나 (B 를 만들지 않는다) · 모델 키 P2S", list(mm) == ["A"] and m["model"] == "P2S" and m["registry"] == "A", list(mm))
        ck(f"P2′ {term}: SE {fse} + C224 = {ntot} (카드 식) · 깃발 0", m["se_formula"] == fse and m["n_ads"] == 224 == int(isC.sum()) and len(b) == ntot
           and _formula(b.get_chemical_symbols()) == fse + "C224" and not m["interface_check_flags"], (m["se_formula"], m["n_ads"], len(b), m["interface_check_flags"]))
        e = m["ads_strain_pct_x_y"]
        ck(f"P2′ {term}: 변형 +1.94/+0.89 % (P2 와 같다 · 두 방향 < 2 %)", abs(e[0] - 1.935) < 0.02 and abs(e[1] - 0.890) < 0.02 and max(abs(v) for v in e) < 2.0, e)
        r5 = build_v5(term)["A"]["meta"]["registry_rule"]
        ck(f"P2′ {term}: registry A = 같은 종결 V5 의 A (원자 ID · xy)", m["registry_rule"]["A"] == r5["A"] and np.allclose(m["registry_rule"]["A_xy_A"], r5["A_xy_A"], atol=1e-9),
           (m["registry_rule"]["A"], r5["A"]))
        xb = b.get_positions(); n_se = m["n_se"]
        ck(f"P2′ {term}: 흑연 첫 층 최소 ID 원자가 A 위 (xy) · 직접 간격 d0 3.2", np.allclose(xb[n_se + m["anchor_ads_index_in_layer"], :2], m["registry_rule"]["A_xy_A"], atol=1e-9)
           and abs(m["endpoints"]["d0_A"] - 3.2) < 1e-6, (xb[n_se + m["anchor_ads_index_in_layer"], :2], m["registry_rule"]["A_xy_A"]))
        zc = np.sort(np.unique(np.round(xb[isC, 2], 6)))
        lay0 = xb[isC & (xb[:, 2] < zc[0] + 0.1)].copy(); lay1 = xb[isC & (xb[:, 2] > zc[0] + 0.1)].copy()
        lay0[:, 2] = 0.0; lay1[:, 2] = 0.0
        _, Dl = get_distances(lay1, lay0, cell=b.cell, pbc=(True, True, False))
        ck(f"P2′ {term}: 흑연 2층 (112 + 112 · 간격 3.35) · AB (둘째 층 절반 56 만 첫 층 원자 위)", len(zc) == 2 and abs(zc[1] - zc[0] - D_GRAPHITE) < 1e-6
           and len(lay0) == len(lay1) == 112 and int((Dl.min(axis=1) < 1e-3).sum()) == 56, (zc, len(lay0), len(lay1)))
        ep = m["endpoints"]
        ck(f"P2′ {term}: 마스크 = SE 만 (0 < n < SE) · 측방 없음 · far 직접·영상 ≥ 10 Å · gap 규칙 10", all(i < n_se for i in m["fixed_idx"]) and 0 < len(m["fixed_idx"]) < n_se
           and m["lateral_fixed_idx"] == [] and min(ep["far_gap_direct_image_A"]) >= 10.0 - 1e-6 and ep["gap_rule_A"] == 10.0, (len(m["fixed_idx"]), ep["far_gap_direct_image_A"]))
    try:
        build_p2small("s_outer", a_c=2.35); bad = False
    except SlabError as e:
        bad = "변형률" in str(e)
    ck("⛔음성 P2′: 흑연 격자 2.35 → 변형률 > 3 % → 거부", bad)
    q1 = build_p2small("li_outer")["A"]["bound"].get_positions(); q2 = build_p2small("li_outer")["A"]["bound"].get_positions()
    ck("결정성: P2′ li_outer 두 번 → 같은 좌표", np.array_equal(q1, q2))
    # ⑮ p05 탐침 (G1p) — 부모 대역으로 빌드한 bound 를 쓴다 (실제 부모는 UMA+D3 이완본 · 변환 규칙은 같다)
    pb, pf, pm = ps["s_outer"]["A"]["bound"], ps["s_outer"]["A"]["far"], ps["s_outer"]["A"]["meta"]
    isC = np.array([s == "C" for s in pb.get_chemical_symbols()])
    pr, rec = p05_probe(pb, pf, fixed_idx=pm["fixed_idx"])
    dd = pr.get_positions() - pb.get_positions()
    ck("p05: 흡착층 변위 (0, 0, +0.5) · 기판 변위 0 · 셀·순서·원소 같음", np.abs(dd[isC] - [0.0, 0.0, 0.5]).max() < 1e-12 and not np.abs(dd[~isC]).any()
       and np.array_equal(pr.cell.array, pb.cell.array) and pr.get_chemical_symbols() == pb.get_chemical_symbols() and rec["rigid_check"]["ok"], rec["rigid_check"])
    gp = rec["gap_direct_image_A"]
    ck("p05: 공유 far = 탐침에 규칙이 주는 far · 쌍극자 구간 같음 · 깃발 0 · 직접 +0.5 / 영상 −0.5", rec["shared_far"]["ok"] and rec["dip_same_as_parent"]
       and rec["interface_check_flags"] == [] and abs(gp["probe"][0] - gp["parent"][0] - 0.5) < 1e-3 and abs(gp["parent"][1] - gp["probe"][1] - 0.5) < 1e-3, rec)
    import tempfile
    from ase.io import read as _read, write as _write
    with tempfile.TemporaryDirectory() as td:
        _write(os.path.join(td, "p.extxyz"), pb); _write(os.path.join(td, "q.extxyz"), pr)
        rt = check_rigid_shift(_read(os.path.join(td, "p.extxyz")), _read(os.path.join(td, "q.extxyz")), isC)
    ck("p05: extxyz 왕복 뒤에도 G1p ① 통과 (봉인 단계가 파일에서 다시 검사)", rt["ok"], rt)
    iC, iS = int(np.where(isC)[0][0]), int(np.where(~isC)[0][0])

    def broken(f):
        y = pr.copy(); f(y); return check_rigid_shift(pb, y, isC)

    def swap2(sy):
        j = next(k for k in range(len(sy)) if sy[k] != sy[0] and not isC[k]); sy = list(sy); sy[0], sy[j] = sy[j], sy[0]; return sy
    for name, f in (("흡착층 원자 하나 x 2e-6 Å", lambda y: y.positions.__setitem__((iC, 0), y.positions[iC, 0] + 2e-6)),
                    ("기판 원자 하나 z 2e-6 Å", lambda y: y.positions.__setitem__((iS, 2), y.positions[iS, 2] + 2e-6)),
                    ("흡착층 전체 dz 0.5 + 2e-6", lambda y: y.positions.__setitem__((isC, 2), y.positions[isC, 2] + 2e-6)),
                    ("셀 c +1e-3", lambda y: y.set_cell(y.cell.array + np.diag([0.0, 0.0, 1e-3]))),
                    ("원자 순서 (다른 원소 두 기판 원자 맞바꿈)", lambda y: y.set_chemical_symbols(swap2(y.get_chemical_symbols())))):
        r = broken(f)
        ck(f"⛔음성 G1p ①: {name} → 잡는다", not r["ok"], r)
    ck("⛔음성 G1p ①: 탐침 = 부모 그대로 (dz 0) → 잡는다", not check_rigid_shift(pb, pb, isC)["ok"])
    for name, kw, key in (("dz −0.5 (계면을 누름)", {"dz": -0.5}, "강체 인장만"), ("dz 40 (셀 위끝 넘음)", {"dz": 40.0}, "셀 위끝")):
        try:
            p05_probe(pb, pf, **kw); bad = False
        except SlabError as e:
            bad = key in str(e)
        ck(f"⛔음성 p05: {name} → 거부", bad)
    raw = pb.copy(); raw.positions[:, 2] += 1.0
    try:
        p05_probe(raw, pf); bad = False
    except SlabError as e:
        bad = "끝점 정규화" in str(e)
    ck("⛔음성 p05: 끝점 정규화 전 좌표를 부모로 주면 거부 (조용히 다른 셀)", bad)
    try:
        p05_probe(pb, pf, gap=12.0); bad = False
    except SlabError as e:
        bad = "공유 far 불일치" in str(e) and "c 가" in str(e)
    ck("⛔음성 p05: 부모와 다른 gap 규칙 (12) → 거부 (c 가 바뀜)", bad)
    near = build_p2small("s_outer", d0=9.8)["A"]
    try:
        p05_probe(near["bound"], near["far"]); bad = False
    except SlabError as e:
        bad = "공유 far 불일치" in str(e) and "c 가" in str(e)
    ck("⛔음성 p05: 부모 직접 간격 9.8 > gap − dz → c 가 바뀌어 공유 불가 → 거부", bad)
    wrongfar = pf.copy(); wrongfar.positions[np.where(isC)[0], 2] += 0.3
    try:
        p05_probe(pb, wrongfar); bad = False
    except SlabError as e:
        bad = "부모의 far 가 아니다" in str(e)
    ck("⛔음성 p05: 부모 far 가 아닌 far → 거부", bad)
    print(f"{'✅' if n_bad == 0 else '⛔'} build_aprime_interfaces selftest {n_ok}/{n_ok + n_bad} 통과")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--build", choices=["V2", "V3", "V4", "V5", "P1", "P2", "P2S"])
    ap.add_argument("--term", choices=["s_outer", "li_outer"], default="s_outer")
    ap.add_argument("--out")
    ap.add_argument("--a_ag", type=float, default=A_AG_PBE_D3)
    ap.add_argument("--a_c", type=float, default=A_C_PBE_D3)
    ap.add_argument("--gap", type=float, default=None, help="끝점 간격 (Å) — 기본 V2–V5 8 · P1·P2·P2S 10 (SE 쌍 카드 · 외주 2차 카드)")
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
        gap = a.gap if a.gap is not None else (10.0 if a.build in ("P1", "P2", "P2S") else 8.0)
        if a.build == "V2":
            models = build_v2(a.a_ag, a.a_c, gap=gap)
        elif a.build in ("V3", "V4"):
            models = build_v34(a.build, a.term, gap=gap)
        elif a.build == "V5":
            models = build_v5(a.term, a.a_ag, gap=gap)
        elif a.build == "P2S":
            models = build_p2small(a.term, a.a_c, gap=gap)
        else:
            models = build_full(a.build, a.term, a.a_ag, a.a_c, gap=gap)
        man = write_models(a.out, models)
        for k, v in man["models"].items():
            n1 = v.get("n_sub", v.get("n_se", v.get("n_Ag"))); n2 = v.get("n_ads", v.get("n_C", v.get("n_Ag")))
            print(f"✓ {a.build}/{k}: 원자 {n1}+{n2} · c {v['endpoints']['c_A']} Å · far 간격 {v['endpoints']['far_gap_direct_image_A']} · 깃발 {v['interface_check_flags']}")
        print(f"→ {a.out}/manifest.json")
        return 0
    ap.error("--selftest · --build · --registry 중 하나")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SlabError as e:
        print(f"⛔ {e}")
        sys.exit(2)
