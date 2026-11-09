#!/usr/bin/env python3
"""B2O3 doping of LPSCl1.6 (modelC) — Stage 0: Ewald joint pre-rank.

UPGRADED protocol (kb/methodology/b2o3_doping_chemistry.md §5.7).

B2O3 -> bare B3+ at P (4b tetrahedral, -2 acceptor) + O2- at S (16e, isovalent).
Charge compensation: fill existing Li vacancies (LPSCl1.6 has ~0.6 vac/fu).

KEY POINT — what Ewald can / cannot rank:
  charged DOF (Ewald-RIGOROUS)   : B@P (+3 vs +5), halogen S2-/Cl- on free 4a/4d,
                                   Li-fill (+1 vs vacancy 0), acceptor-vacancy assoc.
  isovalent DOF (Ewald-BLIND)    : O@S (both -2) -> O placement decided by COVALENCY,
                                   handled here as chemistry MOTIFS (BO4 / distributed /
                                   free-S) emitted per top config for UMA/DFT to rank.

This avoids the two failure modes of the old sequential-greedy method:
  (1) Li-ordering noise (1162 meV) contaminating a "1 representative Li" ranking,
  (2) greedy cut discarding coupled minima (B-O / acceptor-vacancy coupling).

Pipeline:
  1. supercell -> oxidation states -> site pools
  2. Li candidate sites — void finder (declared method · validated in the real host:
     Li–Li ≥ --li_min_dist · Li–cation ≥ --cation_min_dist · 27-image minimum image) → li_candidates.json
     (2026-11-09: the spglib symmetry path was removed — Codex DU P1-2)
  3. precompute geometric Ewald kernel M once (positions fixed across configs)
  4. enumerate {B sites} × {halogen pattern | --fix_halogen}; Li fill under the pair-distance
     constraint — exhaustive when C(n_cand, n_fill) ≤ cap, else greedy (initial-point generator)
  5. exact config-key dedup (no energy-rounding dedup) -> keep top-N by Ewald
  6. per top-K (--o_motif_top N|all): O motifs bo4 / distributed / free_s (family pool only — stops
     if short) -> cif/ ; O-less bases -> base_noO/ ; composition + charge checked ; manifest.json
     verified (--verify OUT re-checks it)

Deps: ase, numpy, scipy.
Usage:
  python3 b2o3_enumerate.py --base db/structures/modelc_V0_k663.xyz \
      --supercell 1 1 2 --n_B 2 --n_O 3 --n_samples 80000 --top 300 \
      --o_motif_top 20 --out b2o3_stage0
  python3 b2o3_enumerate.py --verify b2o3_stage0      # manifest 재검증만
"""
import argparse, json, itertools, hashlib, math
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.neighborlist import neighbor_list

KE = 14.399645351950543  # e^2/(4*pi*eps0) in eV*Angstrom
OXI = {"Li": +1, "P": +5, "B": +3, "Nd": +3, "S": -2, "O": -2, "Cl": -1, "VAC": 0}
HALOGENS = ("Cl", "Br", "I")


# ----------------------------------------------------------------------
# Rietveld (부분점유) CIF → 정수 조성 골격          (2026-09-07 신설)
# ----------------------------------------------------------------------
#   왜 여기인가: 이 도구가 이미 "도펀트³⁺@4b + O²⁻@16e + 할로겐 4a/4c + Li 충전" 을
#   Ewald 로 순위매긴다. 빠져 있던 것은 **입력이 정렬 구조여야 한다**는 것뿐이었다.
#   협업자 Rietveld 는 부분점유라 그대로 못 넣는다 → 여기서 정수화해 같은 파이프라인에 얹는다.
#
# ⛔ 이 경로가 **못 하는 것**
#   · 점유율을 "맞추지" 않는다. 자리 수가 모자라면 반올림이고, 그 편차를 report 에 적는다.
#     (4자리에서 0.85 와 0.75 는 둘 다 3 이 된다 — 실측 선호가 뭉개지는 것을 숨기지 않는다.)
#   · 도펀트 농도를 정련값으로 두지 않는다. n_B·n_O 로 **선언**하는 값이다.
#   · 원자를 이완하지 않는다. 격자도 안 건드린다 (Rietveld a 를 그대로 쓴다).
#   · 대칭 축약에 spglib 을 쓰지 않는다 — F-centered 를 fcc 벡터로 직접 내린다.
#     그 외 격자중심(I/C/R)은 지원하지 않고 **거부한다**(조용히 틀리는 것보다 낫다).

def primitive_fcc(atoms, tol=0.02):
    """면심(F) 관용셀 → 원시셀. spglib 없이 fcc 원시벡터로 직접 내린다."""
    C = atoms.cell.array
    M = np.array([[0.0, .5, .5], [.5, 0.0, .5], [.5, .5, 0.0]])
    P = M @ C
    inv = np.linalg.inv(P)
    seen, keep = [], []
    for i, r in enumerate(atoms.get_positions()):
        f = (r @ inv) % 1.0
        if not any(np.linalg.norm((f - u + .5) % 1.0 - .5) < tol for u in seen):
            seen.append(f)
            keep.append(i)
    out = atoms[keep]
    out.set_cell(P)
    out.set_scaled_positions(out.get_positions() @ inv % 1.0)
    return out


def _site_classes(cif_path):
    """CIF 의 자리 클래스 → (atoms, tag별 역할·점유율). ASE store_tags 를 쓴다."""
    a = read(str(cif_path), store_tags=True)
    occ = a.info.get("occupancy")
    kinds = a.arrays.get("spacegroup_kinds")
    if not occ or kinds is None:
        raise SystemExit(f"⛔ {cif_path}: 부분점유 정보가 없다 "
                         f"(occupancy/spacegroup_kinds). Rietveld CIF 가 맞나?")
    occ = {int(k): v for k, v in occ.items()}
    roles = {}
    for tag in sorted(set(int(t) for t in kinds)):
        o = occ.get(tag) or {}
        if not o:
            raise SystemExit(f"⛔ tag {tag} 에 점유율이 없다")
        major = max(o, key=o.get)
        if major == "Li":
            role = "li"
        elif major in HALOGENS:
            role = "free_anion"
        elif major == "S":
            role = "ps4S"
        elif OXI.get(major, 0) > 0:
            role = "cation4b"
        else:
            raise SystemExit(f"⛔ tag {tag} 의 대표 원소 {major} 를 어느 자리로 볼지 모른다 "
                             f"— 추측하지 않는다 (점유율 {o})")
        roles[tag] = (role, o)
    for need in ("li", "cation4b", "ps4S", "free_anion"):
        if not any(r == need for r, _ in roles.values()):
            raise SystemExit(f"⛔ 자리 역할 '{need}' 를 못 찾았다 — argyrodite CIF 가 맞나?")
    return a, roles


def base_from_rietveld(cif_path, supercell, n_dop, n_O, primitive=False):
    """부분점유 CIF → (골격 atoms · Li후보 좌표 · 목표조성 · report).

    골격에는 **Li 를 넣지 않는다** — Li 는 전량 Ewald 가 배치한다(호출자가 n_li_fill 로).
    """
    a0, roles = _site_classes(cif_path)
    if primitive:
        a0 = primitive_fcc(a0)
        kinds = a0.arrays["spacegroup_kinds"]
    a = a0 * tuple(supercell)
    kinds = np.asarray(a.arrays["spacegroup_kinds"], dtype=int)
    idx = {r: [] for r in ("li", "cation4b", "ps4S", "free_anion")}
    for i, t in enumerate(kinds):
        idx[roles[int(t)][0]].append(i)

    # 자유음이온: **tag 마다 따로 반올림** — 4c(0.85) 와 4a(0.75) 의 선호를 뭉개지 않는다
    cl_sites, freeS_sites, rep = [], [], []
    for tag, (role, o) in roles.items():
        if role != "free_anion":
            continue
        sites = [i for i in idx["free_anion"] if int(kinds[i]) == tag]
        pcl = sum(v for e, v in o.items() if e in HALOGENS)
        ncl = int(round(pcl * len(sites)))
        cl_sites += sites[:ncl]
        freeS_sites += sites[ncl:]
        rep.append({"tag": int(tag), "n_sites": len(sites), "occ_halide": round(pcl, 4),
                    "raw": round(pcl * len(sites), 3), "int": ncl,
                    "dev": round(ncl - pcl * len(sites), 3)})

    syms = list(a.get_chemical_symbols())
    for i in idx["cation4b"]:
        syms[i] = "P"
    for i in idx["ps4S"]:
        syms[i] = "S"
    for i in cl_sites:
        syms[i] = "Cl"
    for i in freeS_sites:
        syms[i] = "S"
    a.set_chemical_symbols(syms)
    li_pos = a.get_positions()[idx["li"]].copy()
    base = a[[i for i in range(len(a)) if i not in set(idx["li"])]]

    # ⛔⛔ 2026-09-07 실측 버그 — **정수화해 놓고 부분점유 꼬리표를 안 떼면 도로 부분점유가 된다.**
    #   ASE 의 CIF **라이터**는 `info["occupancy"]` + `arrays["spacegroup_kinds"]` 가 남아
    #   있으면 그걸 보고 혼합 자리를 **복원해서 써낸다**. 실제로 첫 판이
    #       Nd Nd1 1.0 0.5 0.5 0.5 0.0200
    #       P  P1  1.0 0.5 0.0 0.0 0.9800
    #   처럼 같은 자리에 두 원소를 적어, 되읽으면 P4·Nd4·O16 (전하 +6) 이 나왔다.
    #   **조용히 틀린 DFT 입력이 만들어지는 경로**라 여기서 확실히 끊는다.
    for _obj in (a, base):
        _obj.info.pop("occupancy", None)
        if "spacegroup_kinds" in _obj.arrays:
            del _obj.arrays["spacegroup_kinds"]

    # ── 목표 조성: 자리 수는 정확히, Li 는 **전하중성이 결정한다** ────────────
    n4b, n16e = len(idx["cation4b"]), len(idx["ps4S"])
    # ⛔ 자리보다 많은 도펀트를 조용히 받으면 nP 가 음수가 되고, 그 음수가 전하식에
    #   그대로 들어가 **말이 되는 것처럼 보이는 Li 개수**가 나온다 (2026-09-07 시험이 잡음).
    if not (0 <= n_dop <= n4b):
        raise SystemExit(f"⛔ 도펀트 {n_dop} 개가 4b 자리 {n4b} 개를 넘는다")
    if not (0 <= n_O <= n16e):
        raise SystemExit(f"⛔ O {n_O} 개가 16e 자리 {n16e} 개를 넘는다")
    nP, nNd = n4b - n_dop, n_dop
    nS = (n16e - n_O) + len(freeS_sites)
    nCl, nO = len(cl_sites), n_O
    nLi = 2 * nS + nCl + 2 * nO - 5 * nP - 3 * nNd
    if nLi < 0 or nLi > len(idx["li"]):
        raise SystemExit(f"⛔ 전하중성이 요구하는 Li {nLi} 개가 48h 자리 "
                         f"{len(idx['li'])} 개에 안 들어간다 — n_dop/n_O 를 줄여라")
    report = {"n_fu": n4b, "sites": {"4b": n4b, "16e": n16e,
                                     "free_anion": len(idx["free_anion"]),
                                     "48h": len(idx["li"])},
              "free_anion_rounding": rep,
              "target": {"Li": nLi, "P": nP, "dopant": nNd, "S": nS, "Cl": nCl, "O": nO},
              "n_atoms": nLi + nP + nNd + nS + nCl + nO,
              "charge": nLi + 5 * nP + 3 * nNd - 2 * nS - nCl - 2 * nO,
              "cell_A": [round(x, 5) for x in a.cell.cellpar()]}
    return base, li_pos, nLi, report


# ----------------------------------------------------------------------
# Ewald (neutral cell) — geometric kernel M s.t. E = q^T M q  (eV)
# ----------------------------------------------------------------------
def ewald_matrix(pos, cell, alpha=None, rcut=None, kcut=None):
    """Return N×N matrix M with E_ewald = sum_ij q_i q_j M_ij (neutral cell).

    E = ½ Σ_ij Σ_L' q_i q_j erfc(α|r_ij+L|)/|r_ij+L|                       (real)
      + (2π/V) Σ_{G≠0} e^{−G²/4α²}/G² |S(G)|² ,  S(G) = Σ_i q_i e^{iG·r_i}  (reciprocal)
      − (α/√π) Σ_i q_i²                                                     (self)

    ⛔ 2026-11-09 고침 (Codex DU P1-1 · 재현: α 만 바꿔도 −3.51 → −5.53 → −7.56 eV · 독립 합 −2.931):
      ① 역격자 항에 ½ 을 **두 번** 곱했다 — (2π/V) 가 이미 ½ · (4π/V) 다. 그래서 역격자 몫이 절반이었고
        에너지가 α 에 따라 움직였다 (수렴한 Ewald 합은 α 와 무관해야 한다).
      ② (예방) 이미지 범위를 격자 벡터 길이 대신 수직폭으로 · 차 벡터를 분율 [−½, ½) 로 감싼다 · 역격자 범위를
        2π/|a_i| 로 — 기운 셀에서 이론상 컷오프 안 이미지를 빠뜨릴 수 있었다. ⚠ 깨기로 재 보니 정밀도 계수 3.6 에서
        옛 범위의 차이는 10⁻⁶ 상대 이하라 시험이 못 잡는다 (M2–M4 초록) — 실제로 값이 틀렸던 것은 ① 하나다.
      ③ 정밀도 계수 3.2 → 3.6 (3.2 의 역격자 절단 ≈ 3.6e-5 상대 · 기운 원시셀 Madelung 3.0e-5 어긋남).
      selftest: Madelung 상수 (NaCl · CsCl · 외부 기준) · 기운 원시셀 · 길쭉 기운 셀 · α 불변 (modelc 꼴 포함) ·
      전하 0 자리 불변 · 슈퍼셀 가산 — 깨기 M1 (½ 이중 되살림) → 8 빨강.
    ⛔ 이 함수가 못 하는 것: 전하가 0 이 아닌 셀의 배경 보정 (호출부가 중성을 보장해야 한다 — 검사 안 함).
    """
    pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    N = len(pos); V = abs(np.linalg.det(cell))
    if alpha is None:
        alpha = (N * np.pi**3 / V**2) ** (1.0 / 6.0)  # standard heuristic
    ACC = 3.6   # erfc(3.6) ≈ 3.6e-7 · exp(−3.6²) ≈ 2.4e-6 — 2026-11-09 3.2 → 3.6 (3.2 는 역격자 절단 ≈ 3.6e-5 상대오차)
    if rcut is None:
        rcut = ACC / alpha
    if kcut is None:
        kcut = 2.0 * alpha * ACC
    inv = np.linalg.inv(cell)
    recip = 2 * np.pi * inv.T
    lens = np.linalg.norm(cell, axis=1)
    widths = np.array([V / np.linalg.norm(np.cross(cell[(i + 1) % 3], cell[(i + 2) % 3]))
                       for i in range(3)])

    # --- real space (differences wrapped to fractional [-1/2, 1/2) → every image within rcut
    #     has |n_i| <= rcut/w_i + 1/2 along each lattice direction) ---
    nmax = np.ceil(rcut / widths + 0.5).astype(int)
    shifts = np.array(list(itertools.product(
        range(-nmax[0], nmax[0] + 1), range(-nmax[1], nmax[1] + 1),
        range(-nmax[2], nmax[2] + 1))))
    Lvecs = shifts @ cell
    M = np.zeros((N, N))
    from scipy.special import erfc
    dij = pos[:, None, :] - pos[None, :, :]              # N,N,3
    f = dij @ inv
    f -= np.round(f)
    dij = f @ cell
    for L in Lvecs:
        r = np.linalg.norm(dij + L, axis=2)              # N,N
        zero = r < 1e-8
        r[zero] = 1.0
        contrib = erfc(alpha * r) / r
        contrib[zero] = 0.0
        M += 0.5 * contrib                                # 0.5: each pair counted twice over i,j
    # --- reciprocal (reciprocal-cell plane spacing along b_i is 2π/|a_i|) ---
    kmax = np.ceil(kcut * lens / (2 * np.pi)).astype(int)
    ks = np.array(list(itertools.product(
        range(-kmax[0], kmax[0] + 1), range(-kmax[1], kmax[1] + 1),
        range(-kmax[2], kmax[2] + 1))))
    ks = ks[np.any(ks != 0, axis=1)]
    G = ks @ recip
    G2 = np.einsum("ij,ij->i", G, G)
    keep = G2 < kcut**2
    G, G2 = G[keep], G2[keep]
    pref = (2 * np.pi / V) * np.exp(-G2 / (4 * alpha**2)) / G2   # = ½·(4π/V): the ½ is already here
    arg = pos @ G.T                                       # N,K
    C, S = np.cos(arg), np.sin(arg)
    M += (C * pref) @ C.T + (S * pref) @ S.T              # Σ_G pref cos(G·(r_i − r_j))
    # --- self term (diagonal) ---
    M[np.diag_indices(N)] -= alpha / np.sqrt(np.pi)
    return KE * M


def ewald_energy(M, q):
    return float(q @ M @ q)


# ----------------------------------------------------------------------
# site pools
# ----------------------------------------------------------------------
def site_pools(atoms):
    s = atoms.get_chemical_symbols()
    ii, jj = neighbor_list("ij", atoms, {("P", "S"): 2.4})
    ps4 = set()
    for a, b in zip(ii, jj):
        if s[a] == "S": ps4.add(a)
        if s[b] == "S": ps4.add(b)
    P = [i for i in range(len(atoms)) if s[i] == "P"]
    Cl = [i for i in range(len(atoms)) if s[i] == "Cl"]
    freeS = [i for i in range(len(atoms)) if s[i] == "S" and i not in ps4]
    ps4S = sorted(ps4)
    return dict(P=P, Cl=Cl, freeS=freeS, ps4S=ps4S,
                free_anion=sorted(freeS + Cl))  # 4a/4d pool


# ----------------------------------------------------------------------
# 거리 — 최소상 (일반 격자)
# ----------------------------------------------------------------------
_SHIFTS27 = np.array(list(itertools.product((-1, 0, 1), repeat=3)), float)


def perp_widths(cell):
    cell = np.asarray(cell, float)
    V = abs(np.linalg.det(cell))
    return np.array([V / np.linalg.norm(np.cross(cell[(i + 1) % 3], cell[(i + 2) % 3]))
                     for i in range(3)])


def mic_images(P, X, cell):
    """(n,3)·(m,3) 데카르트 → (27, n, m) 거리 — 분율 [−½, ½] 감싼 뒤 이웃 27 이미지.

    길이 d 인 이미지의 i 성분은 |f_i + n_i| ≤ d / w_i 이고 감싼 뒤 |f_i| ≤ ½ 이므로 |n_i| ≤ d / w_i + ½ →
    d < 1.5 · min(수직폭) 이면 27 개로 **빠짐없이** 본다 (2026-11-09 · 옛 감싸기 하나는 d < ½ · min(w) 만 정확 —
    우리 셀 수직폭 5.72 Å 에서 배위 반경 3.25 Å 는 그 밖이었다).
    """
    cell = np.asarray(cell, float)
    inv = np.linalg.inv(cell)
    f = (np.asarray(P, float)[:, None, :] - np.asarray(X, float)[None, :, :]) @ inv
    f -= np.round(f)
    return np.stack([np.linalg.norm((f + s) @ cell, axis=2) for s in _SHIFTS27])


def mic_dists(P, X, cell):
    """최소상 거리 (n, m). 최소상 거리가 1.5 · min(수직폭) 보다 짧을 때 정확하다 (호출부가 확인)."""
    if len(X) == 0:
        return np.full((len(P), 0), np.inf)
    return mic_images(P, X, cell).min(axis=0)


def min_dist(p, pts, cell):
    if len(pts) == 0:
        return 1e9
    return float(mic_dists(np.asarray(p, float)[None, :], np.asarray(pts, float), cell).min())


# ----------------------------------------------------------------------
# Li 후보 자리 — void 탐색 (명시한 생성법 · 실제 host 에서 검증)      (2026-11-09 고침)
# ----------------------------------------------------------------------
#   ⛔ 옛 spglib 경로를 뺐다 (Codex DU P1-2). 점유 Li 까지 넣은 구조의 종 보존 대칭으로 기존 Li 를
#     복제하면 정확한 대칭에서는 기존 Li 가 기존 Li 로 간다 → **공공이 원리상 안 생긴다**. 실제 modelc
#     셀에서는 spglib 이 연산 2 개만 찾아 예외 · 부족으로 늘 void 탐색으로 넘어갔다 — 6 월 이후 실제로
#     쓰인 것은 void 탐색뿐이다 (6 월 로그 'Li 후보 자리: 80 (void_finder)').
#   거리 문턱 [제안 2026-11-09 — 근거는 이 저장소 실측]:
#     LI_MIN_DIST 2.1 Å — Rietveld CIF 의 48h 짝 거리 2.06 Å (argyrodite 48h 짝은 한 Li 의 두 자리라
#       같이 차지하지 않는다) 보다 조금 위 · host 최소 Li–Li 2.73 Å (modelc_V0_k663).
#       후보 ↔ 점유 Li · 새로 놓는 Li 끼리 둘 다에 건다.
#     CATION_MIN_DIST 2.6 Å — host 최소 Li–P 3.12 Å · 옛 문턱 1.7 Å 는 P 에서 1.96 Å 인 후보를 받았다
#       (P–S 2.05 Å 보다 가깝다).
#   실측 (modelc_V0_k663 × (1,2,1)): 옛 후보 88 개는 **전부** 점유 Li 에서 2.6 Å 안 (14 개는 1.8 Å 안).
LI_MIN_DIST = 2.1
CATION_MIN_DIST = 2.6
ANIONS = ("S", "Cl", "O", "Br", "I")


def li_void_candidates(atoms, li_min=LI_MIN_DIST, cation_min=CATION_MIN_DIST,
                       min_anion=2.3, max_anion=2.95, coord_r=3.25, min_coord=3,
                       grid=0.4, dedup=1.2):
    """void 탐색 Li 후보 + 검증 보고 → (후보 (n,3) 데카르트, report).

    격자점마다 넷을 다 만족해야 남는다:
      · 가장 가까운 음이온 (S·Cl·O·…) 거리 ∈ (min_anion, max_anion)   [기존 2.3–2.95 Å]
      · coord_r 안 음이온 **이미지** ≥ min_coord                       [기존 3.25 Å · 3]
      · 비-Li 양이온 (P·B·Nd·…) ≥ cation_min                           [제안 2.6 Å · 옛 1.7]
      · 점유 Li ≥ li_min                                               [제안 2.1 Å · 옛 0.9]
    → 배위 높은 점부터 dedup 안 점을 합친다 [기존 1.2 Å · 정렬은 안정 정렬].
    거리는 27-이미지 최소상 — 쓰는 가장 긴 거리가 1.5 · min(수직폭) 이상이면 멈춘다.

    ⛔ 못 하는 것: 자리 에너지를 판정하지 않는다 (거르기만) · 48h 이름표를 붙이지 않는다
      (이완된 host 에서는 점유 Li 가 이상 48h 에서 평균 0.6 Å · 최대 1.6 Å 벗어나 짝 대응이 깨끗하지
      않다 — 2026-11-09 실측) · host 를 이완하지 않는다 · 문턱 자체가 옳은지는 시험하지 않는다.
    """
    s = np.array(atoms.get_chemical_symbols())
    cell = atoms.cell.array
    pos = atoms.get_positions()
    w = perp_widths(cell)
    rmax = max(max_anion, coord_r, li_min, cation_min)
    if rmax >= 1.5 * w.min():
        raise SystemExit(f"⛔ 셀 수직폭 {w.min():.2f} Å 의 1.5 배가 후보 판정 거리 {rmax:.2f} Å 보다 작다 — "
                         f"27-이미지 최소상이 이미지를 빠뜨릴 수 있다 (슈퍼셀을 키워라)")
    an = pos[np.isin(s, ANIONS)]
    li = pos[s == "Li"]
    cat = pos[~np.isin(s, ANIONS + ("Li",))]
    na = (np.linalg.norm(cell, axis=1) / grid).astype(int)             # [기존] 격자 수
    g = np.array(np.meshgrid(*[np.linspace(0, 1, n, endpoint=False) for n in na],
                             indexing="ij")).reshape(3, -1).T
    gc = g @ cell
    keep = np.zeros(len(gc), bool)
    score = np.zeros(len(gc), int)
    cnt = dict(grid=len(gc), anion_window=0, coordination=0, cation_ok=0, li_ok=0)
    for k0 in range(0, len(gc), 2048):
        P = gc[k0:k0 + 2048]
        img = mic_images(P, an, cell)
        dmin = img.min(axis=(0, 2))
        nco = (img < coord_r).sum(axis=(0, 2))
        win = (dmin > min_anion) & (dmin < max_anion)
        co = win & (nco >= min_coord)
        dc = mic_dists(P, cat, cell).min(axis=1) if len(cat) else np.full(len(P), np.inf)
        ca = co & (dc >= cation_min)
        dl = mic_dists(P, li, cell).min(axis=1) if len(li) else np.full(len(P), np.inf)
        ok = ca & (dl >= li_min)
        cnt["anion_window"] += int(win.sum()); cnt["coordination"] += int(co.sum())
        cnt["cation_ok"] += int(ca.sum()); cnt["li_ok"] += int(ok.sum())
        keep[k0:k0 + len(P)] = ok
        score[k0:k0 + len(P)] = nco
    idx = np.nonzero(keep)[0]
    order = idx[np.argsort(-score[idx], kind="stable")]
    cand = []
    for i in order:
        if not cand or mic_dists(gc[i][None, :], np.array(cand), cell).min() >= dedup:
            cand.append(gc[i])
    cand = np.array(cand, float).reshape(-1, 3)
    cnt["after_dedup"] = len(cand)
    diag = []
    if len(cand):
        img = mic_images(cand, an, cell)
        dli = mic_dists(cand, li, cell).min(axis=1) if len(li) else np.full(len(cand), np.inf)
        dca = mic_dists(cand, cat, cell).min(axis=1) if len(cat) else np.full(len(cand), np.inf)
        dcc = mic_dists(cand, cand, cell) + np.eye(len(cand)) * 1e9
        for k, p in enumerate(cand):
            diag.append({"xyz": [round(float(x), 4) for x in p],
                         "d_anion_min": round(float(img[:, k, :].min()), 3),
                         "n_anion_images_lt_coord_r": int((img[:, k, :] < coord_r).sum()),
                         "d_Li_occupied_min": round(float(dli[k]), 3) if np.isfinite(dli[k]) else None,
                         "d_cation_min": round(float(dca[k]), 3) if np.isfinite(dca[k]) else None,
                         "d_candidate_min": round(float(dcc[k].min()), 3) if len(cand) > 1 else None})
    rep = {"method": "void_finder (명시한 생성법 · 2026-11-09 · spglib 경로 없음)",
           "params": {"li_min_A": li_min, "cation_min_A": cation_min, "anion_window_A": [min_anion, max_anion],
                      "coord_r_A": coord_r, "min_coord": min_coord, "grid_A": grid, "dedup_A": dedup,
                      "mic": "27-image after fractional wrap"},
           "cell_perp_widths_A": [round(float(x), 3) for x in w],
           "counts": cnt, "candidates": diag,
           "sha256_xyz_4dp": hashlib.sha256(np.round(cand, 4).tobytes()).hexdigest()}
    return cand, rep


def rietveld_li_report(licand, cell):
    """Rietveld 경로의 Li 후보 (48h 자리 전부) 보고 — 거르지 않는다 (자리 정본이 CIF 다).

    ⛔ 2026-11-09 실측 한계: 이 CIF 의 이상 48h 는 자리마다 2.04 Å 이웃이 둘 (60 자리 · 60 쌍 / 5 f.u.) 이라
      Li–Li ≥ 2.1 Å (기본) + 욕심 채우기로는 host Li 27 (5 f.u.) 도, Nd 도핑 Li 31 도 **못 놓고 멈춘다**.
      옛 동작 (짝 동시 점유 허용 — 09-07 Nd 셀은 2.04 Å 쌍 10–11 개로 시작했다) 재현은 --li_min_dist 0 을
      **명시**해야 한다. 이 경로를 새 계산에 다시 쓰려면 Li 배치 규칙부터 카드로 새로 정한다.
    """
    dcc = mic_dists(licand, licand, cell) + np.eye(len(licand)) * 1e9 if len(licand) else np.zeros((0, 0))
    return {"method": "rietveld_cif 48h 자리 전부 (거르지 않음)",
            "counts": {"after_dedup": len(licand)},
            "d_candidate_min_A": round(float(dcc.min()), 3) if len(licand) > 1 else None,
            "sha256_xyz_4dp": hashlib.sha256(np.round(np.asarray(licand, float), 4).tobytes()).hexdigest()}


# ----------------------------------------------------------------------
# Li 채우기 — 쌍 거리 제약 + 전수 / 욕심                              (2026-11-09 신설)
# ----------------------------------------------------------------------
def fill_li(M, q, cand_master, cand_xyz, cell, n_fill, li_min=LI_MIN_DIST,
            mode="auto", cap=1_000_000):
    """n_fill 개 Li(+1) 를 후보에 놓는다 — 놓인 Li 끼리 ≥ li_min.

    E(q + Σ e_c) = E(q) + Σ_c (M_cc + 2 (M q)_c) + 2 Σ_{c<d} M_cd   (E = qᵀ M q)
    mode: 'exhaustive' = 제약 안 Ewald 최저 (전수) · 'greedy' = 한 개씩 한계 에너지 최저 (초기점 생성법 —
          최적 보장 없음 · Codex DU Q3) · 'auto' = C(n_cand, n_fill) ≤ cap 이면 exhaustive.
    → (고른 후보 번호 정렬 리스트 · 쓴 mode) · 제약 안에서 못 놓으면 (None, mode).
    실측 (modelc_V0_k663 × (1,2,1) · B 2 · Li 4 · 후보 50 · 2026-11-09): 욕심이 제약 안 최저를 놓친 B 배치
      18/45 (최대 1.10 eV) — B 쌍 순서 상위 5 는 같았다. 그래서 auto 상한을 10⁶ 으로 둔다.
    ⛔ 못 하는 것: Li 잡음이 어닐로 사라진다는 보장 · 동률 (대칭 등가) 에서 '물리적으로 맞는' 쪽 고르기
      (동률이면 사전순 첫 조합 — 결정적이지만 임의다).
    """
    cm = np.asarray(cand_master, int)
    n = len(cm)
    if n_fill == 0:
        return [], "none"
    if mode == "auto":
        mode = "exhaustive" if math.comb(n, n_fill) <= cap else "greedy"
    if n < n_fill:
        return None, mode
    bad = mic_dists(cand_xyz, cand_xyz, cell) < li_min
    np.fill_diagonal(bad, False)
    a = np.diag(M)[cm] + 2.0 * (M[cm] @ q)
    if mode == "exhaustive":
        if math.comb(n, n_fill) > cap:
            raise SystemExit(f"⛔ 전수 {math.comb(n, n_fill)} 조합 > 상한 {cap} — --li_fill greedy 나 상한을 명시하라")
        C = np.array(list(itertools.combinations(range(n), n_fill)), int)
        Mc = M[np.ix_(cm, cm)]
        E = a[C].sum(axis=1)
        ok = np.ones(len(C), bool)
        for i, j in itertools.combinations(range(n_fill), 2):
            ok &= ~bad[C[:, i], C[:, j]]
            E = E + 2.0 * Mc[C[:, i], C[:, j]]
        if not ok.any():
            return None, mode
        E = np.where(ok, E, np.inf)
        return sorted(int(x) for x in C[int(np.argmin(E))]), mode
    if mode != "greedy":
        raise SystemExit(f"⛔ 모르는 Li 채우기 mode {mode}")
    qq = np.array(q, float).copy()
    avail = np.ones(n, bool)
    placed = []
    Md = np.diag(M)[cm]
    for _ in range(n_fill):
        marg = Md + 2.0 * (M[cm] @ qq)
        marg[~avail] = np.inf
        if not np.isfinite(marg).any():
            return None, mode
        c = int(np.argmin(marg))
        placed.append(c)
        qq[cm[c]] += OXI["Li"]
        avail[c] = False
        avail &= ~bad[c]
    return sorted(placed), mode


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
FAMILIES = ("bo4", "distributed", "free_s")      # 카드의 F_B · F_P · F_free


def _parse_args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="정렬된 구조 (xyz/cif). --rietveld_cif 와 택일")
    ap.add_argument("--rietveld_cif", help="부분점유 Rietveld CIF — 여기서 정수화한다")
    ap.add_argument("--primitive", action="store_true",
                    help="관용 F 셀을 원시셀로 내린 뒤 --supercell 적용 (5 f.u. 같은 배수용)")
    ap.add_argument("--dopant", default="B", help="4b 에 넣을 +3 억셉터 (B·Nd·…)")
    ap.add_argument("--n_li_fill", type=int, default=None,
                    help="Ewald 가 놓을 Li 개수. 기본 2×n_B(보상분만). rietveld 경로에서는 전량이 자동 계산된다")
    ap.add_argument("--supercell", nargs=3, type=int, default=[1, 1, 2])
    ap.add_argument("--n_B", type=int, default=2)
    ap.add_argument("--n_O", type=int, default=3)
    ap.add_argument("--n_samples", type=int, default=80000)
    ap.add_argument("--top", type=int, default=300)
    ap.add_argument("--o_motif_top", default="20",
                    help="O 꼴을 만들 상위 바탕 수 — 정수 또는 'all' (= 쓰는 바탕 전부)")
    ap.add_argument("--fix_halogen", action="store_true",
                    help="바탕의 S/Cl 배열을 그대로 둔다 (할로겐 재배치 안 함 · 2026-11-09)")
    ap.add_argument("--li_min_dist", type=float, default=LI_MIN_DIST,
                    help=f"Li–Li 최소 거리 (후보↔점유 · 새 Li 끼리) [제안 {LI_MIN_DIST} Å]")
    ap.add_argument("--cation_min_dist", type=float, default=CATION_MIN_DIST,
                    help=f"후보↔비-Li 양이온 최소 거리 [제안 {CATION_MIN_DIST} Å]")
    ap.add_argument("--li_fill", choices=("auto", "exhaustive", "greedy"), default="auto")
    ap.add_argument("--li_exhaustive_cap", type=int, default=1_000_000,
                    help="auto 에서 전수로 가는 조합 수 상한 [제안 10⁶ — 1×2×5 · Li 4 · 후보 50 = 230,300 조합 · 45 바탕 11 s]")
    ap.add_argument("--allow_infeasible", action="store_true",
                    help="Li 를 제약 안에 못 놓는 바탕을 세고 넘어간다 (기본은 멈춤)")
    ap.add_argument("--legacy_o_fallback", action="store_true",
                    help="옛 동작 재현 전용 — 가족 자리가 모자라면 PS₄ 전체로 (manifest 에 기록)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="b2o3_stage0")
    ap.add_argument("--verify", metavar="OUT", help="OUT/manifest.json 검증만 하고 끝낸다 (문제 있으면 종료코드 1)")
    return ap.parse_args(argv)


def _sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _counts(atoms):
    c = {}
    for x in atoms.get_chemical_symbols():
        c[x] = c.get(x, 0) + 1
    return c


def _charge(counts):
    return sum(OXI[k] * v for k, v in counts.items())


def _fp(atoms):
    f = np.mod(atoms.get_scaled_positions(), 1.0)
    return tuple(sorted((s,) + tuple(np.round(x, 3) % 1.0) for s, x in zip(atoms.get_chemical_symbols(), f)))


def main(argv=None):
    import sys as _sys
    A = _parse_args(argv)
    if A.verify:
        prob = verify_manifest(A.verify)
        for p in prob:
            print("  ✗", p)
        print(f"verify {'OK' if not prob else 'FAIL'} — 문제 {len(prob)} 건")
        raise SystemExit(1 if prob else 0)
    rng = np.random.default_rng(A.seed)
    out = Path(A.out)
    cif_dir = out / "cif"
    cif_dir.mkdir(parents=True, exist_ok=True)
    stray = sorted(p.name for d in (cif_dir, out / "base_noO") if d.exists() for p in d.glob("*.cif"))
    if stray:
        raise SystemExit(f"⛔ 출력 폴더에 이미 CIF {len(stray)} 개가 있다 ({stray[:3]} …) — 새 폴더를 쓰라 "
                         f"(섞이면 manifest 밖 파일이 다음 단계로 넘어간다)")

    DOP = A.dopant
    if DOP not in OXI:
        raise SystemExit(f"⛔ 도펀트 {DOP} 의 산화수를 모른다 — OXI 에 추가하고 오라 "
                         f"(추측하지 않는다). 아는 것: {sorted(OXI)}")
    if OXI[DOP] != +3:
        raise SystemExit(f"⛔ 이 파이프라인은 **+3 억셉터@4b** 전용이다 "
                         f"({DOP} 는 {OXI[DOP]:+d}). Li 보상 수(2×n)가 안 맞는다.")

    if A.rietveld_cif:
        # 부분점유 CIF 를 정수화해 골격을 만든다. Li 는 골격에 없고 **전량** Ewald 가 놓는다.
        base, licand, n_Li_fill, rep = base_from_rietveld(
            A.rietveld_cif, A.supercell, A.n_B, A.n_O, primitive=A.primitive)
        (out / "integerization.json").write_text(
            json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
        print(f"Rietveld 정수화: {rep['n_fu']} f.u. · 목표 {rep['target']} "
              f"· 총 {rep['n_atoms']}원자 · 전하 {rep['charge']:+d}")
        for r in rep["free_anion_rounding"]:
            print(f"   자유음이온 tag{r['tag']}: {r['n_sites']}자리 × {r['occ_halide']} "
                  f"= {r['raw']} → {r['int']} (편차 {r['dev']:+.2f})")
        lirep = rietveld_li_report(licand, base.cell.array)
    else:
        base = read(A.base) * tuple(A.supercell)
        n_Li_fill = A.n_li_fill if A.n_li_fill else 2 * A.n_B   # P5+ -> M3+ = -2 each
        licand, lirep = li_void_candidates(base, li_min=A.li_min_dist, cation_min=A.cation_min_dist)
    if A.n_li_fill:
        n_Li_fill = A.n_li_fill
    src = lirep["method"]
    (out / "li_candidates.json").write_text(json.dumps(lirep, ensure_ascii=False, indent=1) + "\n")
    pools = site_pools(base)
    n_freeS = len(pools["freeS"])             # keep same free-S count (halogen reshuffle)
    print(f"supercell {A.supercell}  nat {len(base)}  pools: P {len(pools['P'])} "
          f"free_anion {len(pools['free_anion'])} (freeS {n_freeS}) ps4S {len(pools['ps4S'])}")
    print(f"doping: {A.n_B} {DOP}@P, {A.n_O} O@S, {n_Li_fill} Li 배치")
    print(f"Li 후보 자리: {len(licand)} ({src}) · 거르기 {lirep['counts']}")
    if len(licand) < n_Li_fill:
        raise SystemExit(f"⛔ Li {n_Li_fill} 개를 놓을 후보가 {len(licand)} 개뿐이다 — "
                         f"문턱 (--li_min_dist {A.li_min_dist} · --cation_min_dist {A.cation_min_dist}) 을 "
                         f"바꾸려면 이유를 적고 명시하라")
    if A.n_B > len(pools["P"]) or A.n_O > len(pools["ps4S"]) + len(pools["freeS"]):
        raise SystemExit("⛔ 도펀트 · O 수가 자리 수를 넘는다")

    # --- 목표 조성 (O 없는 바탕 · O 꼴) — 다르면 멈춘다 ---
    c0 = _counts(base)
    tgt_base = dict(c0)
    tgt_base["P"] = tgt_base.get("P", 0) - A.n_B
    tgt_base[DOP] = tgt_base.get(DOP, 0) + A.n_B
    tgt_base["Li"] = tgt_base.get("Li", 0) + n_Li_fill
    tgt = dict(tgt_base)
    if A.n_O:
        tgt["S"] = tgt["S"] - A.n_O
        tgt["O"] = tgt.get("O", 0) + A.n_O
    tgt_base = {k: v for k, v in tgt_base.items() if v}
    tgt = {k: v for k, v in tgt.items() if v}
    if _charge(tgt) != 0:
        raise SystemExit(f"⛔ 목표 조성 {tgt} 의 형식전하가 {_charge(tgt):+d} — Li 채우기 수가 틀렸다")

    # --- master position list: framework + Li-occupied + Li-candidate ---
    s0 = base.get_chemical_symbols()
    fw_idx = [i for i in range(len(base)) if s0[i] != "Li"]   # P/S/Cl positions (fixed)
    li_occ_idx = [i for i in range(len(base)) if s0[i] == "Li"]
    pos = np.vstack([base.get_positions()[fw_idx],
                     base.get_positions()[li_occ_idx],
                     np.asarray(licand, float).reshape(-1, 3)])
    cell = base.cell.array
    fw_of = {old: k for k, old in enumerate(fw_idx)}
    nfw = len(fw_idx); nliocc = len(li_occ_idx)
    licand_master = list(range(nfw + nliocc, nfw + nliocc + len(licand)))
    liocc_master = list(range(nfw, nfw + nliocc))

    print("precomputing Ewald kernel ...", flush=True)
    M = ewald_matrix(pos, cell)

    q0 = np.zeros(len(pos))
    for old in fw_idx:
        q0[fw_of[old]] = OXI[s0[old]]
    for m in liocc_master:
        q0[m] = OXI["Li"]
    P_master = [fw_of[i] for i in pools["P"]]
    freeanion_master = [fw_of[i] for i in pools["free_anion"]]
    n_free = len(freeanion_master)

    cand_arr = np.array(licand_master)
    cand_xyz = pos[cand_arr] if len(cand_arr) else np.zeros((0, 3))
    B_combos = list(itertools.combinations(range(len(P_master)), A.n_B))
    if A.fix_halogen:
        H_combos = [tuple(k for k, orig in enumerate(pools["free_anion"]) if s0[orig] == "S")]
    else:
        H_combos = list(itertools.combinations(range(n_free), n_freeS))
    n_total = len(B_combos) * len(H_combos)
    print(f"enumerating {len(B_combos)} {DOP} × {len(H_combos)} halogen"
          f"{' (고정)' if A.fix_halogen else ''} = {n_total} base configs · Li 채우기 {A.li_fill} "
          f"(쌍 ≥ {A.li_min_dist} Å) ...", flush=True)
    if A.n_samples and n_total > A.n_samples:
        keep = max(1, A.n_samples // len(B_combos))
        idx = rng.choice(len(H_combos), min(keep, len(H_combos)), replace=False)
        H_combos = [H_combos[i] for i in idx]
        print(f"  halogen subsampled to {len(H_combos)} (n_samples cap {A.n_samples})")

    seen, modes, infeasible = {}, {}, []
    done = 0
    for bsel in B_combos:
        for Hsel in H_combos:
            q = q0.copy()
            for b in bsel:
                q[P_master[b]] = OXI[DOP]
            Hset = set(Hsel)
            for k, m in enumerate(freeanion_master):
                q[m] = OXI["S"] if k in Hset else OXI["Cl"]
            placed, mode = fill_li(M, q, cand_arr, cand_xyz, cell, n_Li_fill,
                                   li_min=A.li_min_dist, mode=A.li_fill, cap=A.li_exhaustive_cap)
            bkey = tuple(sorted(int(P_master[b]) for b in bsel))
            hkey = tuple(sorted(int(freeanion_master[k]) for k in Hsel))
            if placed is None:
                infeasible.append([list(bkey), list(hkey)])
                done += 1
                continue
            for c in placed:
                q[cand_arr[c]] = OXI["Li"]
            key = (bkey, hkey, tuple(sorted(int(cand_arr[c]) for c in placed)))
            if key not in seen:
                seen[key] = ewald_energy(M, q)
                modes[key] = mode
            done += 1
            if done % 20000 == 0:
                print(f"  {done}/{n_total} ...", flush=True)
    if infeasible:
        msg = (f"Li {n_Li_fill} 개를 쌍 ≥ {A.li_min_dist} Å 로 못 놓는 바탕 {len(infeasible)} 개 "
               f"(예 {infeasible[:2]})")
        if not A.allow_infeasible:
            raise SystemExit("⛔ " + msg + " — 멈춘다 (--allow_infeasible 이면 세고 넘어간다 · "
                             "문턱을 낮추려면 이유를 적고 --li_min_dist 를 명시)")
        print("  ⚠ " + msg)
    if not seen:
        raise SystemExit("⛔ 놓을 수 있는 배치가 하나도 없다")

    ranked = sorted(seen.items(), key=lambda kv: kv[1])
    print(f"unique configs {len(ranked)}; lowest Ewald {ranked[0][1]:.3f} eV, "
          f"highest {ranked[-1][1]:.3f} eV, span {ranked[-1][1]-ranked[0][1]:.3f} eV")

    top = ranked[:A.top]
    n_motif = len(top) if str(A.o_motif_top).lower() == "all" else int(A.o_motif_top)
    n_motif = min(n_motif, len(top)) if A.n_O else 0
    base_dir = (out / "base_noO") if A.n_O else cif_dir
    base_dir.mkdir(parents=True, exist_ok=True)

    def _check(st, want, label):
        got = _counts(st)
        if got != want:
            raise SystemExit(f"⛔ {label}: 조성 {got} ≠ 목표 {want} — 멈춘다")
        if _charge(got) != 0:
            raise SystemExit(f"⛔ {label}: 형식전하 {_charge(got):+d}")

    rows, mbases, fps = [], [], {}
    for rank, (key, E) in enumerate(top):
        bpos, sfree, lifill = key
        st = build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                          bpos, sfree, lifill, pools, o_sites=None, dopant=DOP)
        name = f"cfg{rank:04d}_E{E:.3f}"
        _check(st, tgt_base if A.n_O else tgt, name)
        fbase = base_dir / f"{name}.cif"
        write(fbase, st)
        rows.append(dict(rank=rank, ewald_eV=round(E, 4), name=name,
                         B_sites=list(bpos), n_Li_fill=len(lifill)))
        entry = {"rank": rank, "name": name, "ewald_eV": round(E, 4), "fill_mode": modes[key],
                 "dopant_sites_orig": [int(fw_idx[m]) for m in bpos],
                 "free_S_sites_orig": [int(fw_idx[m]) for m in sfree],
                 "li_fill_xyz": [[round(float(x), 4) for x in pos[m]] for m in lifill],
                 "file": str(fbase.relative_to(out)), "sha256": _sha_file(fbase), "motifs": {}}
        if rank < n_motif:
            free_S_orig = [int(fw_idx[m]) for m in sfree]
            for motif in FAMILIES:
                o_sites, fb = pick_o_sites(base, bpos, pools, A.n_O, motif, rng, fw_idx,
                                           free_S_orig, legacy_fallback=A.legacy_o_fallback)
                st_o = build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                                    bpos, sfree, lifill, pools, o_sites=o_sites, dopant=DOP)
                _check(st_o, tgt, f"{name}_O-{motif}")
                fo = cif_dir / f"{name}_O-{motif}.cif"
                write(fo, st_o)
                fpo = _fp(read(fo))
                if fpo in fps:
                    raise SystemExit(f"⛔ {fo.name} 가 {fps[fpo]} 와 같은 구조다 — 멈춘다")
                fps[fpo] = fo.name
                entry["motifs"][motif] = {"file": str(fo.relative_to(out)), "sha256": _sha_file(fo),
                                          "O_sites_orig": o_sites, "legacy_fallback": fb}
        mbases.append(entry)

    json.dump(rows, open(out / "stage0_ranked.json", "w"), indent=2)
    with open(out / "stage0_ranked.csv", "w") as f:
        f.write("rank,ewald_eV,name,n_B,n_Li_fill\n")
        for r in rows:
            f.write(f"{r['rank']},{r['ewald_eV']},{r['name']},{len(r['B_sites'])},{r['n_Li_fill']}\n")
    man = {"schema": "b2o3_enumerate_manifest/v1",
           "argv": list(argv) if argv is not None else _sys.argv[1:],
           "tool_sha256": _sha_file(__file__),
           "params": {k: v for k, v in vars(A).items() if k != "verify"},
           "li_candidates": {"method": src, "n": len(licand), "file": "li_candidates.json",
                             "sha256": _sha_file(out / "li_candidates.json")},
           "n_configs_scored": len(seen), "n_infeasible": len(infeasible),
           "fill_modes": sorted(set(modes.values())),
           "dopant": DOP, "families": list(FAMILIES) if n_motif else [],
           "base_formula_counts": tgt_base if A.n_O else tgt, "target_formula_counts": tgt,
           "expect": {"n_bases": len(top), "n_motif_bases": n_motif,
                      "n_motif_files": n_motif * (len(FAMILIES) if n_motif else 0)},
           "bases": mbases,
           "⛔_못_하는_것": ["배치의 실제 안정성 판정 (형식전하 Ewald 거르기일 뿐)",
                          "O 꼴은 가족마다 표본 하나 (rng) — '선언한 표본에서 찾은 최저' 까지만",
                          "대칭 등가 배치를 합치지 않는다 (Ewald 반올림 중복 제거 안 함 — Codex DU P1-3)"]}
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    prob = verify_manifest(out)
    if prob:
        raise SystemExit("⛔ 방금 쓴 manifest 가 검증을 못 넘는다: " + " | ".join(prob[:5]))
    print(f"\nwrote {len(rows)} bases -> {base_dir}/  + O 꼴 {n_motif}×{len(FAMILIES)} -> {cif_dir}/")
    print(f"manifest: {out}/manifest.json (검증 통과) · ranked: {out}/stage0_ranked.csv|json")


def pick_o_sites(base, bpos, pools, n_O, motif, rng, fw_idx, free_S_orig, legacy_fallback=False):
    """O 로 바꿀 S 자리 n_O 개 (원래 번호) — 가족 정의 안에서만 고른다 → (자리, 옛 넘어가기 썼나).

    bo4 (F_B)         : 도펀트 자리 P 의 PS₄ 꼭짓점 S
    distributed (F_P) : 도펀트에 안 붙은 PS₄ S
    free_s (F_free)   : **이 배치의** 자유 S (할로겐 재배치 뒤의 실제 S — 2026-11-09 Codex DU P2:
                        옛 코드는 바탕의 freeS 목록을 써서 Cl 자리를 O 로 바꿀 수 있었다)
    ⛔ 가족 자리가 n_O 보다 모자라면 **멈춘다** (옛 'PS₄ 전체로 넘어감' 은 --legacy_o_fallback 재현 전용).
    """
    s = base.get_chemical_symbols()
    b_orig = [fw_idx[mb] for mb in bpos]
    ii, jj = neighbor_list("ij", base, {("P", "S"): 2.4})
    corner_of = {p: set() for p in b_orig}
    for a_, b_ in zip(ii, jj):
        if a_ in corner_of and s[b_] == "S":
            corner_of[a_].add(int(b_))
    b_corners = sorted({c for v in corner_of.values() for c in v})
    if motif == "bo4":
        pool = list(b_corners)
    elif motif == "free_s":
        pool = sorted(int(x) for x in free_S_orig)
    elif motif == "distributed":
        bc = set(b_corners)
        pool = [i for i in pools["ps4S"] if i not in bc]
    else:
        raise SystemExit(f"⛔ 모르는 O 꼴 {motif}")
    used_fallback = False
    if len(pool) < n_O:
        if not legacy_fallback:
            raise SystemExit(f"⛔ O 꼴 '{motif}': 가족 자리 {len(pool)} 개 < O {n_O} 개 — 멈춘다 "
                             f"(옛 'PS₄ 전체로 넘어감' 은 --legacy_o_fallback 재현 전용)")
        pool = list(pools["ps4S"])
        used_fallback = True
        if len(pool) < n_O:
            raise SystemExit(f"⛔ PS₄ S {len(pool)} 개 < O {n_O} 개")
    return sorted(int(x) for x in rng.choice(pool, n_O, replace=False)), used_fallback


def build_struct(base, fw_idx, li_occ_idx, licand, pos, cell,
                 bpos, sfree, lifill, pools, o_sites, dopant="B"):
    """Assemble ASE Atoms for a given config (bpos/sfree/lifill are master indices)."""
    from ase import Atom
    new = base.copy()
    syms = list(new.get_chemical_symbols())
    for mb in bpos:
        syms[fw_idx[mb]] = dopant
    sset = set(fw_idx[m] for m in sfree)
    for orig in pools["free_anion"]:
        syms[orig] = "S" if orig in sset else "Cl"
    if o_sites:
        for o in o_sites:
            if syms[o] != "S":
                raise SystemExit(f"⛔ O 자리 {o} 가 S 가 아니다 ({syms[o]}) — 멈춘다")
            syms[o] = "O"
    new.set_chemical_symbols(syms)
    for ml in lifill:
        new.append(Atom("Li", position=pos[ml]))
    return new


def verify_manifest(out):
    """manifest 검증 → 문제 목록 (빈 목록이면 통과).

    본다: 바탕 수 · (바탕 × 가족) 조합이 정확히 다 있는가 · 파일 존재 · sha256 · 조성 · 형식전하 0 ·
    O 자리 번호가 실제 O 인가 · 가족 정의 (기하로 다시 봄: F_B 의 O 는 도펀트에 2.4 Å 안 · F_P 는 P 에 붙고
    도펀트에 안 붙음 · F_free 는 P · 도펀트에서 2.4 Å 밖) · 같은 구조 중복 · manifest 밖 CIF.
    ⛔ 못 하는 것: 배치가 '좋은지' · Ewald 값이 맞는지 (다시 계산 안 함).
    """
    out = Path(out)
    prob = []
    mf = out / "manifest.json"
    if not mf.exists():
        return [f"manifest 없음: {mf}"]
    m = json.loads(mf.read_text())
    dop = m.get("dopant", "B")
    tb, tt = m["base_formula_counts"], m["target_formula_counts"]
    fams = m.get("families", [])
    exp = m["expect"]
    if len(m["bases"]) != exp["n_bases"]:
        prob.append(f"바탕 {len(m['bases'])} 개 ≠ 기대 {exp['n_bases']}")
    listed, fps = set(), {}
    n_mot = 0

    def _one(rel, sha, want, label):
        f = out / rel
        listed.add(str(Path(rel)))
        if not f.exists():
            prob.append(f"{label}: 파일 없음 {rel}")
            return None
        if _sha_file(f) != sha:
            prob.append(f"{label}: sha256 불일치")
        st = read(f)
        got = _counts(st)
        if got != want:
            prob.append(f"{label}: 조성 {got} ≠ {want}")
        if _charge(got) != 0:
            prob.append(f"{label}: 형식전하 {_charge(got):+d}")
        fp = _fp(st)
        if fp in fps:
            prob.append(f"{label}: {fps[fp]} 와 같은 구조")
        fps[fp] = label
        return st

    for b in m["bases"]:
        _one(b["file"], b["sha256"], tb, b["name"])
        want_fams = set(fams) if b["rank"] < exp["n_motif_bases"] else set()
        if set(b["motifs"]) != want_fams:
            prob.append(f"{b['name']}: O 꼴 {sorted(b['motifs'])} ≠ 기대 {sorted(want_fams)}")
        for fam, e in b["motifs"].items():
            n_mot += 1
            st = _one(e["file"], e["sha256"], tt, f"{b['name']}_O-{fam}")
            if st is None:
                continue
            sy = np.array(st.get_chemical_symbols())
            if any(sy[i] != "O" for i in e["O_sites_orig"]):
                prob.append(f"{b['name']}_O-{fam}: 기록된 O 자리에 O 가 아닌 원자")
            if e.get("legacy_fallback"):
                continue      # --legacy_o_fallback 재현 — 가족 기하는 원래 안 맞는다 (manifest 에 표시됨)
            iO = np.nonzero(sy == "O")[0]
            dD = mic_dists(st.positions[iO], st.positions[sy == dop], st.cell.array).min(axis=1) \
                if (sy == dop).any() else np.full(len(iO), np.inf)
            dP = mic_dists(st.positions[iO], st.positions[sy == "P"], st.cell.array).min(axis=1) \
                if (sy == "P").any() else np.full(len(iO), np.inf)
            if fam == "bo4" and not (dD < 2.4).all():
                prob.append(f"{b['name']}_O-bo4: 도펀트에 안 붙은 O 가 있다")
            if fam == "distributed" and not ((dP < 2.4) & (dD >= 2.4)).all():
                prob.append(f"{b['name']}_O-distributed: P 에 안 붙었거나 도펀트에 붙은 O 가 있다")
            if fam == "free_s" and not ((dP >= 2.4) & (dD >= 2.4)).all():
                prob.append(f"{b['name']}_O-free_s: P · 도펀트에 붙은 O 가 있다")
    if n_mot != exp["n_motif_files"]:
        prob.append(f"O 꼴 파일 {n_mot} 개 ≠ 기대 {exp['n_motif_files']}")
    for d in ("cif", "base_noO"):
        if (out / d).exists():
            for f in sorted((out / d).glob("*.cif")):
                if str(f.relative_to(out)) not in listed:
                    prob.append(f"manifest 밖 CIF: {f.relative_to(out)}")
    return prob


def _selftest():
    """자체시험 (Rietveld 정수화 · Ewald · 생성기). **음성 경로 위주** — 양성만 있는 시험은 아무것도 보증 못 한다."""
    import tempfile
    from ase import Atoms
    bad = []
    _checks = []

    def chk(cond, msg):
        _checks.append(msg)
        print(("  ✓ " if cond else "  ✗ ") + msg)
        if not cond:
            bad.append(msg)

    CIF = """data_t
_cell_length_a 9.79770
_cell_length_b 9.79770
_cell_length_c 9.79770
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_space_group_name_H-M_alt "F -4 3 m"
_symmetry_Int_Tables_number 216
loop_
 _atom_site_label
 _atom_site_type_symbol
 _atom_site_fract_x
 _atom_site_fract_y
 _atom_site_fract_z
 _atom_site_occupancy
s1 Li 0.1626 0.1626 0.0153 0.4533
s2 P  0.5 0.5 0.5 0.98
s2b Nd 0.5 0.5 0.5 0.02
s3 S  0.6235 0.6235 0.6235 0.9925
s3b O  0.6235 0.6235 0.6235 0.0075
s4 Cl 0.25 0.25 0.25 0.85
s4b S  0.25 0.25 0.25 0.15
s5 Cl 0.0 0.0 0.0 0.75
s5b S  0.0 0.0 0.0 0.25
"""
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "t.cif"
        p.write_text(CIF)

        base, li, nLi, rep = base_from_rietveld(p, (1, 1, 1), n_dop=2, n_O=3)
        chk(rep["charge"] == 0, "[양성] 전하중성이 정확히 0")
        chk(rep["n_atoms"] == 54 and nLi == 26,
            f"[양성] 4 f.u. → 54원자 · Li 26 (실제 {rep['n_atoms']}/{nLi})")
        chk(len(li) == 48, f"[양성] 48h 자리를 전부 Li 후보로 준다 (실제 {len(li)})")

        # ⛔음성 ★ 이 버그가 실제로 났다 (2026-09-07): 정수화 후 부분점유 꼬리표가 남으면
        #   ASE CIF 라이터가 혼합 자리를 복원해 써낸다 → 되읽으면 조성·전하가 깨진다.
        chk("occupancy" not in base.info and "spacegroup_kinds" not in base.arrays,
            "⛔음성: 골격에 부분점유 꼬리표가 남지 않는다 (남으면 CIF 로 왕복하며 되살아난다)")
        rt = Path(td) / "rt.cif"
        write(rt, base)
        back = read(rt)
        chk(len(back) == len(base) and
            sorted(back.get_chemical_symbols()) == sorted(base.get_chemical_symbols()),
            "⛔음성: **CIF 로 쓰고 되읽어도 조성이 그대로다** (왕복 시험 — 위 버그의 관문)")

        # ⛔음성: 원시 축약이 실제로 자리 수를 1/4 로 줄이는가 (안 줄면 F 중심을 못 읽은 것)
        b5, li5, nLi5, rep5 = base_from_rietveld(p, (1, 1, 5), 2, 3, primitive=True)
        chk(rep5["n_fu"] == 5 and rep5["n_atoms"] == 66,
            f"[양성] 원시×5 → 5 f.u. · 66원자 (실제 {rep5['n_fu']}/{rep5['n_atoms']})")
        chk(abs(b5.cell.cellpar()[0] - 9.79770 / (2 ** 0.5)) < 1e-3,
            "⛔음성: 원시 격자상수가 a/√2 다 (관용셀 그대로면 F 중심을 안 내린 것)")

        # ⛔음성: 자유음이온을 tag 마다 따로 반올림하는가 (한 통에 몰면 4c 선호가 사라진다)
        chk(len(rep["free_anion_rounding"]) == 2,
            "⛔음성: 자유음이온 tag 를 합치지 않고 **따로** 반올림한다 (4a·4c 두 줄)")

        # ⛔음성: 전하중성이 48h 자리 수를 넘으면 조용히 넘어가지 않는다
        try:
            base_from_rietveld(p, (1, 1, 1), n_dop=5, n_O=3)   # 4b 자리는 4개뿐
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "⛔음성: **자리보다 많은 도펀트**를 SystemExit 로 막는다 "
            "(안 막으면 nP 가 음수가 되어 그럴듯한 Li 개수가 나온다)")

        # ⛔음성: 점유율 정보가 없는 평범한 CIF 는 거부한다
        plain = Path(td) / "plain.cif"
        write(plain, Atoms("LiCl", positions=[[0, 0, 0], [2, 0, 0]], cell=[6, 6, 6], pbc=True))
        try:
            base_from_rietveld(plain, (1, 1, 1), 2, 3)
            ok = False
        except SystemExit:
            ok = True
        chk(ok, "⛔음성: 부분점유가 없는 CIF 를 Rietveld 로 받아주지 않는다")

    # ------------------------------------------------------------------
    # Ewald (2026-11-09 · Codex DU P1-1) — 외부 기준 (Madelung 상수) · α 불변 · 전하 0 자리 · 슈퍼셀
    # ⛔ 이 시험들은 역격자 ½ 이중 · 기운 셀 이미지 누락을 되살리면 빨개져야 한다 (깨기로 확인).
    # ------------------------------------------------------------------
    M_NACL, M_CSCL = 1.74756459463, 1.76267477307
    a = 5.64
    nacl_c = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0],
                       [.5, 0, 0], [0, .5, 0], [0, 0, .5], [.5, .5, .5]]) * a
    q_c = np.array([1, 1, 1, 1, -1, -1, -1, -1], float)
    E = ewald_energy(ewald_matrix(nacl_c, np.eye(3) * a), q_c)
    ref = -4 * KE * M_NACL / (a / 2)
    chk(abs(E / ref - 1) < 2e-5, f"[외부 기준] NaCl 관용셀 Madelung (상대오차 {abs(E / ref - 1):.1e})")
    prim = np.array([[0, a / 2, a / 2], [a / 2, 0, a / 2], [a / 2, a / 2, 0]])
    nacl_p = np.array([[0, 0, 0], [a / 2, a / 2, a / 2]])
    q_p = np.array([1.0, -1.0])
    Ep = ewald_energy(ewald_matrix(nacl_p, prim), q_p)
    refp = -KE * M_NACL / (a / 2)
    chk(abs(Ep / refp - 1) < 2e-5,
        f"⛔음성: **기운 원시셀 (60°)** NaCl 도 같은 Madelung (상대오차 {abs(Ep / refp - 1):.1e})")
    acs = 4.12
    Ecs = ewald_energy(ewald_matrix(np.array([[0, 0, 0], [acs / 2] * 3]), np.eye(3) * acs), q_p)
    refcs = -KE * M_CSCL / (acs * np.sqrt(3) / 2)
    chk(abs(Ecs / refcs - 1) < 2e-5, f"[외부 기준] CsCl Madelung (상대오차 {abs(Ecs / refcs - 1):.1e})")
    N = len(nacl_p); V = abs(np.linalg.det(prim))
    a0 = (N * np.pi**3 / V**2) ** (1.0 / 6.0)
    Es = [ewald_energy(ewald_matrix(nacl_p, prim, alpha=a0 * s), q_p) for s in (0.6, 1.0, 1.6)]
    spread = (max(Es) - min(Es)) / abs(np.mean(Es))
    chk(spread < 1e-5, f"⛔음성: **α 를 0.6–1.6 배로 바꿔도 같은 에너지** (상대 퍼짐 {spread:.1e}) — 역격자 ½ 이중이면 α 따라 움직인다")
    rng0 = np.random.default_rng(7)
    ghost = rng0.random((3, 3)) @ prim
    Eg = ewald_energy(ewald_matrix(np.vstack([nacl_p, ghost]), prim), np.concatenate([q_p, np.zeros(3)]))
    chk(abs(Eg / Ep - 1) < 1e-5, f"⛔음성: 전하 0 자리 (Li 후보) 를 더해도 에너지 그대로 (상대 {abs(Eg / Ep - 1):.1e})")
    sc = (2, 1, 3)
    shifts = np.array(list(itertools.product(*[range(n) for n in sc]))) @ prim
    pos_sc = np.vstack([nacl_p + s for s in shifts])
    q_sc = np.tile(q_p, len(shifts))
    E_sc = ewald_energy(ewald_matrix(pos_sc, np.diag(sc) @ prim), q_sc)
    chk(abs(E_sc / (len(shifts) * Ep) - 1) < 2e-5,
        f"[양성] 슈퍼셀 2×1×3 = 원시 × 6 (상대 {abs(E_sc / (len(shifts) * Ep) - 1):.1e})")

    # 길쭉하고 기운 셀 (우리 셀 꼴 — modelc 원시 1×1×5 는 7.0 × 7.0 × 35.0 Å · 60°) — 작은 원시셀은
    #   이미지 범위 · 감싸기 · 역격자 범위 구멍을 못 건드린다 (깨기 M2–M4 가 첫 판 시험에서 초록이었다).
    long = np.diag([1, 1, 5]) @ prim
    pos_l = np.vstack([nacl_p + k * prim[2] for k in range(5)])
    E_l = ewald_energy(ewald_matrix(pos_l, long), np.tile(q_p, 5))
    chk(abs(E_l / (5 * Ep) - 1) < 1e-5,
        f"⛔음성: **길쭉 · 기운 셀** (원시 × (1,1,5)) = 원시 × 5 (상대 {abs(E_l / (5 * Ep) - 1):.1e})")
    mc = np.array([[7.01, 0, 0], [3.505, 6.0709, 0], [3.505, 2.0236, 28.6122 * 35.04 / 35.04]])
    mc[2] = mc[2] / np.linalg.norm(mc[2]) * 35.04
    rng1 = np.random.default_rng(11)
    pos_r = rng1.random((24, 3)) @ mc
    q_r = np.array([1.0, -1.0] * 12)
    N_r = len(pos_r); V_r = abs(np.linalg.det(mc)); a_r = (N_r * np.pi**3 / V_r**2) ** (1.0 / 6.0)
    Er = [ewald_energy(ewald_matrix(pos_r, mc, alpha=a_r * s), q_r) for s in (0.6, 1.0, 1.6)]
    sp_r = (max(Er) - min(Er)) / abs(np.mean(Er))
    chk(sp_r < 1e-5, f"⛔음성: modelc 꼴 (7 × 7 × 35 Å · 60°) 무작위 중성 전하에서 α 불변 (상대 퍼짐 {sp_r:.1e})")

    # ------------------------------------------------------------------
    # 생성기 (2026-11-09 · Codex DU P1-2 · P1-3 · P2 · Q10) — 최소상 · Li 후보 · Li 채우기 · O 꼴 · manifest
    # ------------------------------------------------------------------
    # (1) 27-이미지 최소상 = 넓은 범위 무식 탐색 (1.5 × 최소 수직폭 안) · 옛 감싸기 하나는 틀리는 쌍이 있다
    cw = np.array([[7.0, 0, 0], [3.5, 6.0622, 0], [3.5, 2.0207, 5.7155]]) @ np.diag([1, 1, 1])
    cw[2] *= 5.0
    rngm = np.random.default_rng(3)
    Pm_ = rngm.random((40, 3)) @ cw
    Xm_ = rngm.random((40, 3)) @ cw
    brute = np.full((40, 40), np.inf)
    inv_ = np.linalg.inv(cw)
    for nvec in itertools.product(range(-3, 4), repeat=3):
        d_ = np.linalg.norm(Pm_[:, None, :] - Xm_[None, :, :] - np.array(nvec) @ cw, axis=2)
        brute = np.minimum(brute, d_)
    wmin = perp_widths(cw).min()
    sel = brute < 1.5 * wmin
    got = mic_dists(Pm_, Xm_, cw)
    chk(np.allclose(got[sel], brute[sel], atol=1e-9),
        f"⛔음성: 27-이미지 최소상 = 무식 탐색 (거리 < 1.5 × 최소 수직폭 {wmin:.2f} Å · {int(sel.sum())} 쌍)")
    f1 = (Pm_[:, None, :] - Xm_[None, :, :]) @ inv_
    f1 -= np.round(f1)
    one = np.linalg.norm(f1 @ cw, axis=2)
    chk(bool((one[sel] > brute[sel] + 1e-6).any()),
        "[대조] 옛 감싸기 하나는 이 셀에서 최소상보다 긴 거리를 주는 쌍이 있다 (위 시험이 그 차이를 볼 수 있다)")

    # (2) Li 채우기 — 쌍 거리 제약 · 전수 ≤ 욕심 · 제약을 끄면 가까운 쌍을 고른다 · 못 놓으면 None
    cellf = np.eye(3) * 20.0
    xyz = np.array([[5, 5, 5], [5, 5, 6.5], [5, 5, 3.5], [15, 15, 15]], float)   # A · B(A 1.5) · C(A 1.5 · B 3.0) · D
    Mf = np.diag([-10.0, -9.0, -9.0, -1.0])
    qf = np.zeros(4)
    ex, mex = fill_li(Mf, qf, [0, 1, 2, 3], xyz, cellf, 2, li_min=2.1, mode="exhaustive")
    gr, mgr = fill_li(Mf, qf, [0, 1, 2, 3], xyz, cellf, 2, li_min=2.1, mode="greedy")
    chk(ex == [1, 2] and gr == [0, 3],
        f"⛔음성: 전수는 제약 안 최저 (B+C −18) · 욕심은 A 를 먼저 잡아 A+D (−11) — 실제 {ex} · {gr}")
    ex0, _ = fill_li(Mf, qf, [0, 1, 2, 3], xyz, cellf, 2, li_min=0.0, mode="exhaustive")
    chk(ex0 in ([0, 1], [0, 2]),
        f"⛔음성: 제약을 끄면 1.5 Å 쌍 (A+B 또는 A+C) 을 고른다 — 시험이 제약을 실제로 본다 (실제 {ex0})")
    tri = np.array([[5, 5, 5], [5, 5, 6.5], [5, 6.3, 5.7]], float)
    nf, _ = fill_li(np.diag([-1.0, -1.0, -1.0]), np.zeros(3), [0, 1, 2], tri, cellf, 2, li_min=2.1, mode="exhaustive")
    ng, _ = fill_li(np.diag([-1.0, -1.0, -1.0]), np.zeros(3), [0, 1, 2], tri, cellf, 2, li_min=2.1, mode="greedy")
    chk(nf is None and ng is None, "⛔음성: 서로 2.1 Å 안 후보 셋에 Li 둘 → 못 놓는다 (None · 조용히 겹쳐 놓지 않는다)")
    _, mauto = fill_li(Mf, qf, [0, 1, 2, 3], xyz, cellf, 2, li_min=2.1, mode="auto", cap=5)
    chk(mauto == "greedy", "[양성] auto 는 조합 수 > 상한이면 욕심으로 간다 (C(4,2)=6 > 5)")

    # (3) O 꼴 — 가족 자리가 모자라면 멈춘다 · free_s 는 이 배치의 실제 S 만
    from ase import Atoms as _At
    toy = _At("PS4S2Cl", positions=[[5, 5, 5], [7.05, 5, 5], [2.95, 5, 5], [5, 7.05, 5], [5, 2.95, 5],
                                      [15, 15, 15], [15, 5, 15], [5, 15, 15]], cell=[20, 20, 20], pbc=True)
    pools_t = site_pools(toy)
    fw_t = list(range(len(toy)))
    try:
        pick_o_sites(toy, [0], pools_t, 3, "free_s", np.random.default_rng(0), fw_t, [5, 6])
        ok = False
    except SystemExit:
        ok = True
    chk(ok, "⛔음성: F_free 자리 2 < O 3 → **멈춘다** (옛 코드는 PS₄ 전체로 조용히 넘어갔다)")
    o_l, fb = pick_o_sites(toy, [0], pools_t, 3, "free_s", np.random.default_rng(0), fw_t, [5, 6],
                           legacy_fallback=True)
    chk(fb and set(o_l) <= set(pools_t["ps4S"]), "[양성] --legacy_o_fallback 은 옛 동작을 재현하고 표시한다")
    o_f, _ = pick_o_sites(toy, [0], pools_t, 1, "free_s", np.random.default_rng(0), fw_t, [7])
    chk(o_f == [7], f"⛔음성: free_s 는 **이 배치의** 자유 S 에서만 (바탕 freeS {pools_t['freeS']} 아님) — 실제 {o_f}")
    o_b, _ = pick_o_sites(toy, [0], pools_t, 3, "bo4", np.random.default_rng(0), fw_t, [5, 6])
    chk(set(o_b) <= {1, 2, 3, 4}, "[양성] bo4 는 도펀트 P 의 꼭짓점 S 에서만")

    # (4) 끝-끝: modelc 원시×5 (62 원자) · B 1 · O 2 · 할로겐 고정 · 전부 꼴 → manifest 검증 · 망가뜨리면 잡는가
    mpath = Path(__file__).resolve().parents[2] / "db/structures/modelc_V0_k663.xyz"
    if not mpath.exists():
        chk(False, f"끝-끝 시험 입력 없음 {mpath}")
    else:
        import shutil
        with tempfile.TemporaryDirectory() as td:
            o1 = Path(td) / "r1"
            arg = ["--base", str(mpath), "--supercell", "1", "1", "1", "--n_B", "1", "--n_O", "2",
                   "--fix_halogen", "--top", "99", "--o_motif_top", "all", "--seed", "0", "--out", str(o1)]
            main(arg)
            man = json.loads((o1 / "manifest.json").read_text())
            chk(man["expect"] == {"n_bases": 5, "n_motif_bases": 5, "n_motif_files": 15} and not verify_manifest(o1),
                f"[양성] 바탕 5 × 가족 3 = 15 · manifest 검증 통과 (실제 {man['expect']})")
            chk(all("_O-" in f.name for f in (o1 / "cif").glob("*.cif"))
                and len(list((o1 / "cif").glob("*.cif"))) == 15
                and len(list((o1 / "base_noO").glob("*.cif"))) == 5,
                "⛔음성: O 없는 바탕은 base_noO/ 에만 — cif/ 에는 O 꼴만 (Codex DU Q10)")
            lc = json.loads((o1 / "li_candidates.json").read_text())
            st0 = read(mpath)
            sy0 = np.array(st0.get_chemical_symbols())
            cx = np.array([c["xyz"] for c in lc["candidates"]])
            from ase.geometry import get_distances
            dli = get_distances(cx, st0.positions[sy0 == "Li"], cell=st0.cell, pbc=True)[1].min(axis=1)
            dca = get_distances(cx, st0.positions[sy0 == "P"], cell=st0.cell, pbc=True)[1].min(axis=1)
            chk(len(cx) >= 2 and (dli >= LI_MIN_DIST - 1e-3).all() and (dca >= CATION_MIN_DIST - 1e-3).all(),
                f"⛔음성: Li 후보 {len(cx)} 개 전부 점유 Li ≥ {LI_MIN_DIST} Å · P ≥ {CATION_MIN_DIST} Å "
                f"(ASE 최소상으로 따로 잼 · 최소 {dli.min():.2f} · {dca.min():.2f})")
            try:
                main(arg)
                ok = False
            except SystemExit:
                ok = True
            chk(ok, "⛔음성: CIF 가 이미 있는 출력 폴더는 거부한다 (manifest 밖 파일이 섞이지 않게)")

            def _tamper(fn, label):
                o2 = Path(td) / f"t_{label}"
                shutil.copytree(o1, o2)
                fn(o2)
                return verify_manifest(o2)

            b0 = man["bases"][0]
            p_ = _tamper(lambda o: (o / b0["motifs"]["free_s"]["file"]).unlink(), "missing")
            chk(any("파일 없음" in x for x in p_), "⛔음성: O 꼴 파일 하나 지우면 잡는다")
            p_ = _tamper(lambda o: (o / b0["file"]).write_text((o / b0["file"]).read_text() + "\n"), "sha")
            chk(any("sha256" in x for x in p_), "⛔음성: 파일 내용이 바뀌면 sha256 으로 잡는다")
            p_ = _tamper(lambda o: shutil.copy(o / b0["motifs"]["bo4"]["file"], o / "cif" / "stray.cif"), "stray")
            chk(any("manifest 밖" in x for x in p_), "⛔음성: manifest 밖 CIF 가 섞이면 잡는다")

            def _swap(o):
                mm = json.loads((o / "manifest.json").read_text())
                e_b = mm["bases"][0]["motifs"]["bo4"]
                e_f = mm["bases"][0]["motifs"]["free_s"]
                shutil.copy(o / e_b["file"], o / e_f["file"])
                e_f["sha256"] = _sha_file(o / e_f["file"])
                e_f["O_sites_orig"] = e_b["O_sites_orig"]
                (o / "manifest.json").write_text(json.dumps(mm, ensure_ascii=False))
            p_ = _tamper(_swap, "swap")
            chk(any("free_s: P · 도펀트에 붙은 O" in x for x in p_) and any("같은 구조" in x for x in p_),
                "⛔음성: 해시까지 맞춰 F_B 구조를 F_free 자리에 넣어도 가족 기하 · 중복으로 잡는다")

            def _drop(o):
                mm = json.loads((o / "manifest.json").read_text())
                mm["bases"] = mm["bases"][1:]
                (o / "manifest.json").write_text(json.dumps(mm, ensure_ascii=False))
            p_ = _tamper(_drop, "drop")
            chk(any("바탕 4 개 ≠ 기대 5" in x for x in p_), "⛔음성: 바탕 항목이 빠지면 개수로 잡는다")

            try:
                main(["--base", str(mpath), "--supercell", "1", "1", "1", "--n_B", "1", "--n_O", "3",
                      "--fix_halogen", "--top", "99", "--o_motif_top", "all", "--out", str(Path(td) / "r3")])
                ok = False
            except SystemExit:
                ok = True
            chk(ok, "⛔음성: 끝-끝에서도 F_free 자리 2 < O 3 이면 건너뛰지 않고 멈춘다 (옛 main 은 continue)")

    n_all = len(_checks)
    print(f"selftest {'PASS' if not bad else 'FAIL'} — {n_all - len(bad)}/{n_all} ok")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    main()
