#!/usr/bin/env python
"""substitute_compound.py — Compound-set substitution for LPSCl doping.

Mirrors real synthesis routes where dopants enter the lattice as ionic
compounds (Nd2O3, Al2O3, MgO, ZnO, Li2O, …) rather than single elements.
The cation and anion of the precursor enter their respective sites in
stoichiometric ratio, so the compound is charge-neutral by construction.

Three modes (see kb / db/literature/lpscl_doping_precursor_compounds_review.md):

Type A — Compound set substitution (Nd2O3, MgO, …):
  - cation(s) → ``--cation_site`` (default Li_24g)
  - anion(s) → ``--anion_site``   (default S_16e — PS4 → P-anion preferred,
    matches ACS AMI 2021 oxysulfide O-on-S_16e finding)
  - Net cation aliovalency at the Li site is compensated by additional Li
    vacancies (the compound itself is neutral, but cation Δq at the host
    site is positive for divalent+/trivalent dopants and demands vacancies).

Type B — Halide-rich (anion-only swap with auto Li vacancy):
  - S²⁻ → halide⁻ on the chosen S-site, one Li vacancy per swap.
    Reproduces the Li6−xPS5−xCl1+x / Li5.4PS4.4Cl1.6 family (Adeli 2019,
    Kraft 2017).

Type C — Aliovalent cation + halide co-doping:
  - Implementable as TWO sequential Type-A / Type-B calls; this script
    handles them via the ``--also_halide_rich`` flag.

Usage:
  # Type A — Nd2O3 5 mol% (Nd→Li_24g, O→S_16e)
  python3 substitute_compound.py \\
      --base db/structures/comp1_V0_k444.cif \\
      --compound Nd2O3 --x_compound 0.05 \\
      --cation_site Li_24g --anion_site S_16e \\
      --out runs/doping_compound/nd2o3_005/

  # Type B — Li5.4PS4.4Cl1.6 (halide-rich, x=0.6)
  python3 substitute_compound.py \\
      --base ... --halide_rich Cl --excess_per_fu 0.6 \\
      --anion_site S_4a --out runs/doping_compound/lpscl16/

  # Type C — Al-Cl co-doping (Li5.4Al0.1PS4.7Cl1.3)
  python3 substitute_compound.py \\
      --base ... --compound Al2O3 --x_compound 0.025 \\
      --also_halide_rich Cl --excess_per_fu 0.3 \\
      --out runs/doping_compound/al_cl/
"""
import argparse
import json
import re
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import Atoms

import sys
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cascade'))
# ⭐ S1 계약 (BJ2 재심 조건 #3) — 부모 자리 승계 · 전체 보상 수지 · 농도 양자화.
#    규약을 여기 복사하지 않는다: 계약은 tools/cascade/s1_contract.py 한 곳에만 있다.
from s1_contract import (S1ContractError, freeze_parent_sites, SiteCarrier,     # noqa: E402
                         charge_ledger, quantize_concentration)
from site_preference import DOPANT_DB, HOST_SITES, site_preference_filter
from _provenance import get_provenance
from substitute_struct import (
    find_host_indices, find_host_indices_for_site,
    select_substitution_sites, SITE_TO_HOST,
    halide_s_contacts, refuse_unphysical_base,      # 2026-11-17 할로젠–S 접촉 관문
)


def compatible_sites_for_element(element: str, db: dict) -> set[str]:
    """Return the set of HOST_SITES names where ``element`` can sit,
    according to the literature-calibrated radius+charge filter in
    site_preference.py. Skipping incompatible (cation_site, anion_site)
    combinations saves UMA cost and avoids reporting non-physical
    placements (e.g., La³⁺ at S_4a, or O²⁻ at P_4b).
    """
    if element not in db:
        return set()
    info = db[element]
    # v4.5.23: pass element so LITERATURE_SITES union applies (documented
    # per-dopant sites added to the radius/charge filter result).
    matches = site_preference_filter(info['charge'], info['radius'],
                                     element=element)
    return {m['site_name'] for m in matches}


def parse_compound(formula: str) -> dict[str, int]:
    """Parse 'Nd2O3' → {'Nd': 2, 'O': 3}.

    Supports single capital + optional lowercase + optional integer.
    Numeric subscripts only; no parentheses or hydrate notation.
    """
    matches = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    parsed: dict[str, int] = {}
    for el, count in matches:
        if not el:
            continue
        parsed[el] = parsed.get(el, 0) + (int(count) if count else 1)
    if not parsed:
        raise ValueError(f"Could not parse compound formula: {formula!r}")
    return parsed


def classify_compound(composition: dict[str, int], db: dict
                      ) -> tuple[dict[str, int], dict[str, int], int]:
    """Split compound into (cations, anions, net charge)."""
    missing = [el for el in composition if el not in db]
    if missing:
        raise ValueError(f"Elements {missing} not in DOPANT_DB. Add them first.")
    cations = {el: n for el, n in composition.items() if db[el]['charge'] > 0}
    anions  = {el: n for el, n in composition.items() if db[el]['charge'] < 0}
    net_q = sum(db[el]['charge'] * n for el, n in composition.items())
    return cations, anions, net_q


# Common alternative oxidation states per element — used by auto-valence
# inference when the default charge gives a non-neutral compound (e.g.,
# MnO2, CrO3, Fe3O4). Searched in order; first valence giving net_q==0 wins.
ALTERNATIVE_VALENCES = {
    'Cr': [+3, +6, +4, +2],     # Cr2O3 default; CrO3 needs +6; CrO2 needs +4
    'Mn': [+2, +4, +7, +3, +6], # MnO default; MnO2 +4; KMnO4 +7
    'Fe': [+3, +2],              # Fe2O3 default; FeO needs +2
    'Co': [+2, +3, +4],          # CoO default; Co2O3 +3; Co3O4 mixed
    'Ni': [+2, +3, +4],
    'Cu': [+1, +2],              # Cu2O default; CuO +2
    'V':  [+5, +4, +3, +2],      # V2O5 default; VO2 +4
    'Mo': [+6, +4, +5, +3],
    'W':  [+6, +4, +5],
    'Re': [+7, +6, +4],
    'Ti': [+4, +3],
    'Sn': [+4, +2],              # SnO2 default; SnO +2
    'Pb': [+4, +2],
    'Sb': [+5, +3],              # Sb2O5 default; Sb2O3 +3
    # ⛔ 2026-08-20 — **여기 'As' 가 빠져 있어서 As2S3 가 즉사했다.**
    #   DOPANT_DB['As'] 기본이 +5 라 As2S3 의 net_q = 2(+5)+3(−2) = +4 로 중성이 아니고,
    #   대안 원자가가 없으니 재시도도 못 하고 n_structures = 0 으로 끝났다.
    #   바로 윗줄 Sb 는 같은 15족·같은 M2S3·같은 +5 기본인데 [+5,+3] 이 있어서 통과했다.
    #   ⇒ **물리 판정이 아니라 사전 누락**이다. cascade_pool_accounting.csv 의
    #     "As2S3 · stage-01 · n_structures = 0" 이 이것이다.
    'As': [+5, +3],              # As2O5 default; As2S3 / As2O3 need +3
    'Bi': [+3, +5],
    'Ce': [+4, +3],              # CeO2 default; Ce2O3 +3
    'Eu': [+3, +2],
    'U':  [+6, +5, +4, +3],
    'P':  [+5, +3],
}


def find_li_interstitial_sites(atoms: Atoms, n_needed: int,
                              min_dist_to_atom: float = 1.8,
                              min_dist_between: float = 2.5,
                              grid_resolution: int = 25) -> list[np.ndarray]:
    """Locate empty space for Li interstitials by sampling a fractional grid
    and keeping points far from existing atoms (Voronoi-style heuristic).

    Used to compensate ACCEPTOR cations at P_4b (B³⁺ at P⁵⁺, Si⁴⁺ at P⁵⁺
    leave the cell charge-deficient — real synthesis incorporates Li⁺
    interstitials at empty octahedral voids in the argyrodite cage).

    Args:
        n_needed: number of interstitial Li atoms to place
        min_dist_to_atom: Å, smallest acceptable distance to any existing atom
          (1.8 ≈ Li-S equilibrium minus 0.4 for a starting void; UMA relax
          will then settle the interstitial into its actual minimum).
        min_dist_between: Å, smallest spacing between two interstitial Li
          (2.5 ≈ Li-Li ionic contact in Li metal / Li₂S).
        grid_resolution: candidate points per axis (25³ = 15625 candidates).

    Returns:
        list of Cartesian positions (np.ndarray shape (3,)) for the n_needed
        interstitial Li atoms; length 0 if not enough voids found.
    """
    from scipy.spatial import cKDTree
    cell = atoms.cell.array
    n = grid_resolution
    frac = np.array(np.meshgrid(np.linspace(0, 1, n, endpoint=False),
                                np.linspace(0, 1, n, endpoint=False),
                                np.linspace(0, 1, n, endpoint=False),
                                indexing='ij')).reshape(3, -1).T
    cart = frac @ cell

    # Distance from each candidate to nearest atom (PBC-aware tree query
    # via duplicating in 3x3x3 supercell for the tree)
    pos = atoms.get_positions()
    shifts = np.array([[i, j, k] for i in (-1, 0, 1)
                       for j in (-1, 0, 1) for k in (-1, 0, 1)])
    pos_pbc = np.concatenate([pos + s @ cell for s in shifts])
    tree = cKDTree(pos_pbc)
    dists, _ = tree.query(cart)

    # Keep candidates with d > min_dist_to_atom, sorted by farthest-first
    mask = dists > min_dist_to_atom
    candidates = sorted(zip(cart[mask], dists[mask]),
                       key=lambda x: -x[1])

    # Pick n_needed maximally separated voids
    chosen: list[np.ndarray] = []
    for pos_cand, _ in candidates:
        if len(chosen) >= n_needed:
            break
        # Check spacing to already chosen (also PBC-aware via mic_dist)
        ok = True
        for c in chosen:
            # Minimum image distance
            d_vec = pos_cand - c
            d_frac = np.linalg.solve(cell.T, d_vec)
            d_frac -= np.round(d_frac)
            d_mic = np.linalg.norm(d_frac @ cell)
            if d_mic < min_dist_between:
                ok = False
                break
        if ok:
            chosen.append(pos_cand)
    return chosen


def add_li_interstitials(atoms: Atoms, n_int: int) -> tuple[Atoms, list]:
    """Append ``n_int`` Li atoms at empty interstitial voids.

    Returns (new_atoms, positions_added). UMA relax afterwards will let
    the interstitials settle into the actual energy minimum (typically
    near the Cl_4d / S_4a faces of the Li2S sublattice).
    """
    if n_int <= 0:
        return atoms, []
    sites = find_li_interstitial_sites(atoms, n_int)
    if len(sites) < n_int:
        raise RuntimeError(
            f"Could only find {len(sites)} interstitial voids out of "
            f"{n_int} needed; supercell may be too small or already too "
            "crowded. Try a larger supercell.")
    new = atoms.copy()
    for pos in sites:
        new.append('Li')
        new.positions[-1] = pos
    return new, sites


def auto_balance_compound(composition: dict[str, int],
                         db: dict) -> tuple[dict, dict]:
    """If compound is non-neutral with default DB charges, search for a single
    cation whose valence can be substituted from ALTERNATIVE_VALENCES to
    achieve neutrality. Returns (modified_db_subset, info).

    Example: MnO2 = {Mn:1, O:2}. Default Mn=+2 gives net=-2.
    Try Mn=+4 → 1×4 + 2×(-2) = 0 ✓. Returns DB-overlay {Mn:+4}.
    """
    cations, anions, net_q = classify_compound(composition, db)
    if net_q == 0:
        return {}, {'status': 'already_neutral', 'net_q': 0}
    if len(cations) != 1:
        # Multi-cation: more complex; just report imbalance for now
        return {}, {'status': 'multi_cation_imbalance', 'net_q': net_q}
    # Try alternative valences for the single cation
    cat, n_cat = next(iter(cations.items()))
    if cat not in ALTERNATIVE_VALENCES:
        return {}, {'status': 'no_alt_valences_known',
                   'cation': cat, 'net_q': net_q}
    anion_q = sum(db[a]['charge'] * n for a, n in anions.items())
    for v in ALTERNATIVE_VALENCES[cat]:
        if v * n_cat + anion_q == 0:
            return {cat: {**db[cat], 'charge': v}}, {
                'status': 'auto_valence',
                'cation': cat,
                'old_charge': db[cat]['charge'],
                'new_charge': v,
            }
    return {}, {'status': 'no_neutral_valence_found',
               'cation': cat, 'tried': ALTERNATIVE_VALENCES[cat],
               'net_q': net_q}


PARENT_ALIAS = {'Li_24g': 'Li_any', 'Li_48h': 'Li_any'}   # Li Wyckoff 는 입력에서 못 가른다


def build_parent_site_map(atoms: Atoms) -> dict:
    """치환 **전** host 의 원자별 부모 자리를 굳힌다 (BJ2 P0-2).

    이 지도가 생긴 뒤로는 자리를 **현재 배위로 다시 분류하지 않는다**. P→Nd/B 치환 뒤
    PS₄ 의 S 가 free S 로 넘어가던 것이 바로 그 재분류였다.
    """
    sym = atoms.get_chemical_symbols()
    s16 = set(find_host_indices_for_site(atoms, 'S_16e'))
    s4a = set(find_host_indices_for_site(atoms, 'S_4a'))
    site_of: dict[int, str] = {}
    for i, el in enumerate(sym):
        if el == 'S':
            if i in s16:
                site_of[i] = 'S_16e'
            elif i in s4a:
                site_of[i] = 'S_4a'
            else:
                raise S1ContractError(f"⛔ S #{i} 가 S_16e 도 S_4a 도 아니다 — 부모 지도를 못 굳힌다")
        elif el == 'Li':
            site_of[i] = 'Li_any'
        elif el == 'P':
            site_of[i] = 'P_4b'
        elif el == 'Cl':
            site_of[i] = 'Cl_4d'
        else:
            site_of[i] = f'other_{el}'
    return freeze_parent_sites(sym, site_of)


def parent_host_indices(carrier: SiteCarrier, site: str) -> list[int]:
    """부모 자리가 ``site`` 이고 아직 host 원소가 앉아 있는 원자들."""
    want = PARENT_ALIAS.get(site, site)
    host_el = SITE_TO_HOST[site]
    return [i for i in carrier.indices_of_parent_site(want) if carrier.occupant[i] == host_el]


def _host_sites(atoms: Atoms, carrier, site: str, contract: str) -> list[int]:
    if carrier is not None:
        return parent_host_indices(carrier, site)
    if contract == 'enforce':
        raise S1ContractError(
            "⛔ S1 계약(enforce) 인데 부모 자리 지도가 없다 — 치환 전 host 에서 지도를 굳혀 넘겨라 "
            "(--s1_contract legacy_bypass 로만 옛 배위 재분류 경로를 쓴다)")
    return find_host_indices_for_site(atoms, site)


def compute_substitution_count(n_units: int, multiplicity: int) -> int:
    """Atoms of one element introduced when ``n_units`` formula units of the
    compound enter the cell."""
    return n_units * multiplicity


def li_vacancies_needed(atoms: Atoms, cations: dict[str, int],
                       cation_site: str, n_units: int, db: dict) -> int:
    """Compute charge surplus from cation placement; positive value = need
    that many Li vacancies; negative value = need Li interstitials (NOT
    modelled — acceptor cations like B³⁺ at P⁵⁺, Si⁴⁺ at P⁵⁺ leave the cell
    charge-unbalanced and will rank low under UMA's energy filter).

    Each cation at the cation_site introduces ``(q_cation - q_host)`` extra
    charge per atom. Sum across all compound cations gives net surplus.
    """
    host_q = HOST_SITES[cation_site]['charge']
    n_vac = 0
    for cat, mult in cations.items():
        dq_per_atom = db[cat]['charge'] - host_q
        n_atoms = compute_substitution_count(n_units, mult)
        n_vac += dq_per_atom * n_atoms
    return max(n_vac, 0)  # only remove Li if net positive surplus
    # NOTE: when n_vac < 0 (acceptor case, e.g., B/Si/Al at P site), the
    # cell ends up charge-imbalanced. UMA energy will reflect this through a
    # higher binding penalty. Future work: model Li interstitials or
    # reverse-halide-rich (Cl→S swap with extra Li) as compensation paths.


# ══════════════════════════════════════════════════════════════════════════
# 음이온 자리의 **부모 양이온 분산** (2026-09-13 · 카드 v4 §1b · BO 조건 #2)
#
# 왜 필요한가
#   S_16e 는 PS₄ 사면체의 모서리 S 다. O 를 3개 넣을 때 **같은 P 에 딸린 S** 로
#   몰리면 `PS₁O₃` 한 덩어리가 생긴다. 그건 *희석된 O 치환* 이 아니라
#   **한 사면체만 심하게 산화된 것**이고 국소 화학이 다르다. 카드가 고른 것은
#   서로 다른 P 에 하나씩 = **PS₃O 세 개** 다.
#
# ⛔ 기존 선택기는 이것을 보장하지 않는다 — `select_substitution_sites` 의
#   docstring 이 스스로 *"May leave the seed PS4 and hop into adjacent PS4"* 라고
#   적고 있고, 'spread' 도 거리로만 고르지 부모를 보지 않는다.
#
# ⛔ 이 코드가 **못 하는 것**
#   · 부모 원소를 추론하지 않는다. `parent_symbol` 을 받는다(기본 'P').
#   · 결합을 양자화학으로 판정하지 않는다. **거리 컷오프**로 가장 가까운 부모를 고른다.
#   · 어느 배치가 물리적으로 옳은지 판정하지 않는다. 카드가 정한 규칙을 **집행**할 뿐이다.
#   · 기본값으로 켜지지 않는다 — 다른 캠페인(Nd₂O₃ 5 mol% 등)은 이 규칙을 안 쓴다.
# ══════════════════════════════════════════════════════════════════════════
def anion_parent_map(atoms, s_indices, parent_symbol='P', cutoff=2.6):
    """S 인덱스 → 가장 가까운 부모 양이온 인덱스. **애매하면 멈춘다.**

    raise:
      · 부모 후보가 컷오프 안에 **하나도 없다** → 자리 지도를 못 만든다
      · **둘 이상** 있다 → 어느 사면체인지 애매하다 (컷오프가 크거나 구조가 깨졌다)
    """
    sym = atoms.get_chemical_symbols()
    parents = [i for i, e in enumerate(sym) if e == parent_symbol]
    if not parents:
        raise S1ContractError(f"⛔ 부모 원소 {parent_symbol} 가 구조에 없다 — 부모 분산 규칙을 집행할 수 없다")
    out = {}
    for si in s_indices:
        d = atoms.get_distances(si, parents, mic=True)
        near = [(float(dd), pj) for dd, pj in zip(d, parents) if dd <= cutoff]
        if not near:
            raise S1ContractError(
                f"⛔ S #{si} 주변 {cutoff} Å 안에 {parent_symbol} 가 없다 "
                f"(최근접 {float(min(d)):.3f} Å) — 부모를 못 정한다")
        if len(near) > 1:
            raise S1ContractError(
                f"⛔ S #{si} 주변 {cutoff} Å 안에 {parent_symbol} 가 {len(near)}개다 "
                f"({[f'#{j}@{dd:.3f}' for dd, j in sorted(near)]}) — 어느 사면체인지 애매하다")
        out[si] = near[0][1]
    return out


def select_distinct_parent_sites(host_idx, n, method, seed, atoms,
                                 parent_symbol='P', cutoff=2.6):
    """부모가 **서로 다른** 자리 n 개를 고른다. 못 고르면 **멈춘다**(조용히 완화 없음).

    방법: 부모별로 자리를 묶고 → 부모를 seed 로 섞어 n 개 고르고 →
          각 부모 안에서 다시 seed 로 하나씩 고른다. 같은 seed 면 같은 결과다.
    """
    import random as _random
    pmap = anion_parent_map(atoms, host_idx, parent_symbol, cutoff)
    groups = {}
    for si, pj in pmap.items():
        groups.setdefault(pj, []).append(si)
    if len(groups) < n:
        raise S1ContractError(
            f"⛔ 부모 {parent_symbol} 가 {len(groups)}종뿐인데 서로 다른 부모 {n} 자리를 요구했다 "
            f"— 규칙을 만족할 수 없다. 셀을 키우거나 규칙을 바꿔라(조용히 완화하지 않는다)")
    rng = _random.Random(seed)
    chosen_parents = rng.sample(sorted(groups), n)
    return sorted(rng.choice(sorted(groups[pj])) for pj in chosen_parents)


def assert_distinct_parents(atoms, targets, parent_symbol='P', cutoff=2.6, where='anion_sites'):
    """이미 정해진 자리들이 규칙을 지키는지 **검사**한다. `index_plan` 경로용."""
    pmap = anion_parent_map(atoms, targets, parent_symbol, cutoff)
    par = [pmap[t] for t in targets]
    if len(set(par)) != len(par):
        dup = {pj for pj in par if par.count(pj) > 1}
        detail = {f"{parent_symbol}#{pj}": [t for t in targets if pmap[t] == pj] for pj in sorted(dup)}
        raise S1ContractError(
            f"⛔ {where}: 부모 {parent_symbol} 가 겹친다 {detail} — 카드 §1b 는 "
            f"**서로 다른 부모**를 요구한다. index_plan 을 고치거나 규칙을 끄고 그 사실을 적어라")
    return pmap


def _plan_or_select(plan, key, elem, host_idx, n, fallback):
    """⭐ 회신 BO 조건 2 (2026-09-12): **공통 부모 배열** 을 P1/P2 로 복제하려면 난수가 아니라
    **실제 인덱스 대응표** 로 자리를 정해야 한다. `index_plan` 이 그 표다.

      index_plan = {"cation_sites": [i, j] | {"Al": [i, j]},
                    "anion_sites":  [k, l, m] | {"O": [...]},
                    "vacancy_sites": [p, q, r, s]}

    · 리스트면 원소 무관(단일 원소 처방용 — P1 의 O₃ 와 P2 의 S₃ 가 **같은 리스트**를 쓴다).
    · 딕셔너리면 원소별.
    · 인덱스는 치환 **전** host 원자 순서. 공공은 **삭제 전** 인덱스.
    · 검증: 길이 = 필요 수 · 전부 그 자리의 허용 host 집합 안 · 중복 없음. 하나라도 어기면
      S1ContractError — 조용히 난수로 대체하지 않는다.
    ⛔ 이 헬퍼가 못 하는 것: 인덱스가 **물리적으로 좋은** 자리인지는 모른다. 표집 정책은 호출부 몫.
    """
    if not plan or key not in plan:
        return fallback()
    v = plan[key]
    if isinstance(v, dict):
        if elem not in v:
            raise S1ContractError(
                f"⛔ index_plan[{key!r}] 에 {elem} 항목이 없다 — 있는 것은 {sorted(v)}. "
                f"P1/P2 짝(같은 **자리**에 다른 원소, 예: O₃ ↔ no-op S₃)을 만들려는 것이면 "
                f"이 표는 **원소 고정(by_element)** 이라 못 쓴다. "
                f"부모 쪽을 `--emit_plan_shape positional` 로 다시 떨궈라 — 리스트 형식은 "
                f"원소 무관이라 양쪽이 같은 파일을 쓴다 (카드 §1b 공통 부모 배열)")
        v = v[elem]
    v = [int(x) for x in v]
    if len(v) != n:
        raise S1ContractError(f"⛔ index_plan[{key!r}] 길이 {len(v)} ≠ 필요 {n} ({elem})")
    if len(set(v)) != len(v):
        raise S1ContractError(f"⛔ index_plan[{key!r}] 에 중복 인덱스 {v}")
    allowed = set(int(x) for x in host_idx)
    bad = [x for x in v if x not in allowed]
    if bad:
        raise S1ContractError(f"⛔ index_plan[{key!r}] 인덱스 {bad} 가 {elem} 의 허용 host 자리 집합 밖이다")
    return v


def substitute_compound_at_sites(atoms: Atoms, composition: dict[str, int],
                                 n_units: int, cation_site: str, anion_site: str,
                                 method: str, seed: int, db: dict,
                                 vacancy_method: str = 'random',
                                 vacancy_cutoff: float = 5.0,
                                 carrier=None, contract: str = 'enforce'
                                 ,
                                 index_plan: dict | None = None,
                                 distinct_anion_parent: bool = False,
                                 anion_parent_symbol: str = 'P',
                                 anion_parent_cutoff: float = 2.6) -> tuple[Atoms, dict]:
    """Place all atoms of one compound unit-cluster into target sites.

    ``vacancy_method`` is decoupled from ``method`` and defaults to 'random'.
    Real LPSCl₁₊ₓ-style halide-rich phases have *disordered* Li vacancies
    (Kraft 2017 NMR / Adeli 2019 PDF) — using 'spread' for vacancies would
    create an artificial ordered Li-vacancy superlattice that does not match
    experiment. Subsitution sites for the dopant atoms themselves can still
    use 'spread' or 'cluster' to model precursor placement geometry.
    """
    new = atoms.copy()
    # Auto-valence inference (MnO2, CrO3, Fe3O4, …) before charge check.
    overlay, av_info = auto_balance_compound(composition, db)
    if overlay:
        db = {**db, **overlay}
    cations, anions, net_q = classify_compound(composition, db)
    if net_q != 0:
        raise ValueError(
            f"Compound {composition} is not charge-neutral (Σq={net_q:+d}, "
            f"auto-valence search status={av_info.get('status', 'n/a')}). "
            "Use --halide_rich, split into separate Type A + B steps, or "
            "add a custom valence to ALTERNATIVE_VALENCES.")

    placement_log = {'cation_site': cation_site, 'anion_site': anion_site,
                     'placements': []}

    # 1. Substitute cations
    seed_local = seed
    for cat, mult in cations.items():
        n_sub = compute_substitution_count(n_units, mult)
        host_idx = _host_sites(new, carrier, cation_site, contract)
        if n_sub > len(host_idx):
            raise ValueError(
                f"Need {n_sub} {cat} at {cation_site}, but only "
                f"{len(host_idx)} sites available")
        targets = _plan_or_select(index_plan, 'cation_sites', cat, host_idx, n_sub,
                                  lambda: select_substitution_sites(host_idx, n_sub, method, seed_local, atoms=new))
        syms = new.get_chemical_symbols()
        for i in targets:
            syms[i] = cat
        new.set_chemical_symbols(syms)
        if carrier is not None:
            carrier.substitute(targets, cat, syms)
        placement_log['placements'].append(
            {'element': cat, 'site': cation_site, 'n': n_sub,
             'targets': targets})
        seed_local += 1

    # 2. Substitute anions
    for an, mult in anions.items():
        n_sub = compute_substitution_count(n_units, mult)
        host_idx = _host_sites(new, carrier, anion_site, contract)
        if n_sub > len(host_idx):
            raise ValueError(
                f"Need {n_sub} {an} at {anion_site}, but only "
                f"{len(host_idx)} sites available")
        # ⭐ 카드 v4 §1b — 부모 양이온 분산 규칙 (기본 꺼짐, 파일럿에서 켠다)
        #   index_plan 경로도 **검사한다** — 계획으로 넣었다고 규칙을 비켜 가지 않는다.
        if distinct_anion_parent:
            targets = _plan_or_select(
                index_plan, 'anion_sites', an, host_idx, n_sub,
                lambda: select_distinct_parent_sites(host_idx, n_sub, method, seed_local, new,
                                                     anion_parent_symbol, anion_parent_cutoff))
            _pmap = assert_distinct_parents(new, targets, anion_parent_symbol,
                                            anion_parent_cutoff, where=f"anion_sites[{an}]")
        else:
            targets = _plan_or_select(index_plan, 'anion_sites', an, host_idx, n_sub,
                                      lambda: select_substitution_sites(host_idx, n_sub, method, seed_local, atoms=new))
            _pmap = None
        syms = new.get_chemical_symbols()
        for i in targets:
            syms[i] = an
        new.set_chemical_symbols(syms)
        if carrier is not None:
            carrier.substitute(targets, an, syms)
        _rec = {'element': an, 'site': anion_site, 'n': n_sub, 'targets': targets,
                'distinct_parent_rule': bool(distinct_anion_parent)}
        if _pmap is not None:
            _rec['parent_map'] = {int(k): int(v) for k, v in _pmap.items() if k in targets}
            _rec['parent_symbol'] = anion_parent_symbol
            _rec['parent_cutoff_A'] = anion_parent_cutoff
        placement_log['placements'].append(_rec)
        seed_local += 1

    # 3. Charge compensation — Li vacancies (donor case) or Li interstitials
    #    (acceptor case, e.g., B³⁺/Si⁴⁺ at P⁵⁺). Compute signed surplus first.
    # ⭐ BJ2 #3: 양이온만 더하던 수지에 **음이온 치환**을 넣는다. S²⁻→Cl⁻ 는 자리당 Δq=+1 이라
    #    빠뜨리면 보상이 그만큼 모자란 셀이 조용히 나간다.
    _placements = ([{'element': c, 'site': cation_site, 'n': compute_substitution_count(n_units, m)}
                    for c, m in cations.items()]
                   + [{'element': a, 'site': anion_site, 'n': compute_substitution_count(n_units, m)}
                      for a, m in anions.items()])
    _charges = {e: db[e]['charge'] for e in list(cations) + list(anions)}
    _site_q = {cation_site: HOST_SITES[cation_site]['charge'],
               anion_site: HOST_SITES[anion_site]['charge']}
    ledger = charge_ledger(_placements, _charges, _site_q)
    placement_log['charge_ledger'] = ledger
    surplus = ledger['net_charge']
    n_vac = max(surplus, 0)
    n_int = max(-surplus, 0)
    if n_int > 0:
        try:
            new, int_positions = add_li_interstitials(new, n_int)
            placement_log['li_interstitials'] = {
                'n': n_int, 'positions': [list(p) for p in int_positions]}
            if carrier is not None:
                carrier.append(['Li'] * n_int)
        except RuntimeError as e:
            placement_log['li_interstitials'] = {'n': n_int, 'error': str(e)}
            if contract == 'enforce':
                raise S1ContractError(
                    f"⛔ Li 침입 {n_int}개를 못 넣었다 ({e}) — 전하 불균형 셀을 "
                    "'UMA 가 낮게 매길 것' 으로 흘려보내지 않는다 (BJ2 #3 실패 시 중단)") from e
    if n_vac > 0:
        li_idx = find_host_indices(new, 'Li')
        if n_vac >= len(li_idx):
            raise ValueError(
                f"Need {n_vac} Li vacancies but only {len(li_idx)} Li remain")
        # Reference for 'near_cation': aliovalent cation positions
        # (Mg, Al, Nd, etc. — the actually substituted atoms)
        ref_idx = [i for i, s in enumerate(new.get_chemical_symbols())
                  if s in cations]
        # CR-5 fix (2026-05-16): propagate cluster_radius from CLI so
        # --vacancy_cutoff actually controls the near_cation exponential decay.
        vac_targets = _plan_or_select(
            index_plan, 'vacancy_sites', 'Li', li_idx, n_vac,
            lambda: select_substitution_sites(
                li_idx, n_vac, vacancy_method, seed_local + 100, atoms=new,
                reference_indices=ref_idx,
                cluster_radius=vacancy_cutoff))
        keep = [i for i in range(len(new)) if i not in vac_targets]
        new = new[keep]
        if carrier is not None:
            carrier.delete(vac_targets)
        placement_log['li_vacancies'] = {'n': n_vac, 'indices': vac_targets}
    else:
        placement_log['li_vacancies'] = {'n': 0, 'indices': []}

    # ⭐ 회신 BO: 실제로 쓴 인덱스 표. `--emit_index_plan` 이 이걸 떨궈 짝 처방이 재사용한다.
    _cat = {pl['element']: list(pl['targets']) for pl in placement_log['placements']
            if pl['site'] == cation_site}
    _an = {pl['element']: list(pl['targets']) for pl in placement_log['placements']
           if pl['site'] == anion_site}
    placement_log['index_plan_used'] = {
        'cation_sites': _cat,
        'anion_sites': _an,
        'vacancy_sites': list(placement_log['li_vacancies']['indices']),
        'index_basis': '치환 전 host 원자 순서 · 공공은 삭제 전 인덱스',
        'from_plan': bool(index_plan),
    }
    # ⭐ P1/P2 짝용 **원소 무관** 판(positional). 자리 하나에 원소가 정확히 하나일 때만 만든다 —
    #   둘 이상이면 리스트로 접는 순간 어느 인덱스가 어느 원소였는지 잃는다.
    #   ⛔ 이게 없으면 `--emit_index_plan` 이 자기 목적(P1/P2 가 같은 파일을 쓴다)을 못 한다:
    #     by_element 표는 O 로 굳어 있어 no-op S₃ 처방이 계약거부로 막힌다 (2026-09-13 실측).
    if len(_cat) <= 1 and len(_an) <= 1:
        placement_log['index_plan_used_positional'] = {
            'cation_sites': list(next(iter(_cat.values()), [])),
            'anion_sites': list(next(iter(_an.values()), [])),
            'vacancy_sites': list(placement_log['li_vacancies']['indices']),
            'index_basis': '치환 전 host 원자 순서 · 공공은 삭제 전 인덱스',
            'from_plan': bool(index_plan),
            '_shape': 'positional — 원소 무관. 같은 자리에 다른 원소를 놓는 짝 처방용',
            '_emitted_for': {'cation': sorted(_cat), 'anion': sorted(_an)},
        }
    return new, placement_log


def mixed_halide_swap(atoms: Atoms, halide_excess: dict[str, float],
                     n_fu: int, anion_site: str, method: str, seed: int,
                     vacancy_method: str = 'random',
                     carrier=None, contract: str = 'enforce',
                     quantize_policy: str = 'exact', approved_by=None) -> tuple[Atoms, dict]:
    """Multi-halide halide-rich substitution (LPSClBr-style precursors).

    ``halide_excess`` = {'Cl': 0.3, 'Br': 0.3} → 0.3 + 0.3 = 0.6 total excess
    per f.u., giving Li5.4PS4.4Cl1.3Br0.3 (4 fu = 24 Li → 22.4 ≈ 22 Li after
    2 S→halide swaps + 2 Li vacancies; halides split 1 Cl + 1 Br for the 2
    swaps). Replicates comp2/3/4/5 chemistry (Cl₁₋ₓBrₓ argyrodite family).
    """
    new = atoms.copy()
    host_idx = _host_sites(new, carrier, anion_site, contract)
    # ⭐ BJ2 Q6: max(1, round(...)) 은 요청 농도를 표현 못 할 때 **묵시적으로 1 unit** 을 넣었다.
    _q = {h: quantize_concentration(x, n_fu, policy=quantize_policy, approved_by=approved_by,
                                    label=f"halide_excess:{h}")
          for h, x in halide_excess.items()}
    n_swap_per_halide = {h: q['n_units'] for h, q in _q.items()}
    total_swap = sum(n_swap_per_halide.values())
    if total_swap > len(host_idx):
        raise ValueError(
            f"Need {total_swap} S→halide swaps at {anion_site}, "
            f"but only {len(host_idx)} sites")

    # Pick total_swap S sites then partition by halide stoichiometry
    targets = select_substitution_sites(host_idx, total_swap, method, seed,
                                       atoms=new)
    syms = new.get_chemical_symbols()
    idx_iter = iter(targets)
    placements = {}
    for halide, n in n_swap_per_halide.items():
        these = [next(idx_iter) for _ in range(n)]
        for i in these:
            syms[i] = halide
        placements[halide] = these
    new.set_chemical_symbols(syms)

    li_idx = find_host_indices(new, 'Li')
    if total_swap >= len(li_idx):
        raise ValueError(
            f"Need {total_swap} Li vacancies but only {len(li_idx)} Li remain")
    vac_targets = select_substitution_sites(
        li_idx, total_swap, vacancy_method, seed + 1, atoms=new)
    keep = [i for i in range(len(new)) if i not in vac_targets]
    new = new[keep]

    return new, {
        'mixed_halides': halide_excess,
        'n_swap_per_halide': n_swap_per_halide,
        'swap_targets': placements,
        'li_vacancies': vac_targets,
    }


def halide_rich_swap(atoms: Atoms, halide: str, n_swap: int,
                    anion_site: str, method: str, seed: int,
                    vacancy_method: str = 'random',
                    carrier=None, contract: str = 'enforce') -> tuple[Atoms, dict]:
    """Type B — replace ``n_swap`` S atoms at ``anion_site`` with ``halide``,
    and remove the same number of Li atoms.

    Reproduces the Li6−xPS5−xCl1+x family stoichiometry. Charge balance is
    automatic: each S→Cl swap drops the local charge by +1, each Li vacancy
    drops it by −1; the two cancel.

    Li vacancies use ``vacancy_method='random'`` by default — Kraft 2017
    NMR / Adeli 2019 PDF show Li vacancies are positionally disordered, not
    ordered into a superlattice.
    """
    new = atoms.copy()
    host_idx = _host_sites(new, carrier, anion_site, contract)
    if n_swap > len(host_idx):
        raise ValueError(
            f"Need {n_swap} S→{halide} swaps at {anion_site}, but only "
            f"{len(host_idx)} sites available")
    targets = select_substitution_sites(host_idx, n_swap, method, seed, atoms=new)
    syms = new.get_chemical_symbols()
    for i in targets:
        syms[i] = halide
    new.set_chemical_symbols(syms)
    if carrier is not None:
        carrier.substitute(targets, halide, syms)

    li_idx = find_host_indices(new, 'Li')
    if n_swap >= len(li_idx):
        raise ValueError(
            f"Need {n_swap} Li vacancies but only {len(li_idx)} Li remain")
    vac_targets = select_substitution_sites(
        li_idx, n_swap, vacancy_method, seed + 1, atoms=new)
    keep = [i for i in range(len(new)) if i not in vac_targets]
    new = new[keep]
    if carrier is not None:
        carrier.delete(vac_targets)

    return new, {
        'halide_rich': halide,
        'n_swap': n_swap,
        'swap_targets': targets,
        'li_vacancies': vac_targets,
    }


def composition_summary(atoms: Atoms) -> dict[str, int]:
    syms = atoms.get_chemical_symbols()
    return {el: int(c) for el, c in
            zip(*np.unique(syms, return_counts=True))}


def _selftest() -> int:
    """S1 계약 **결선** 시험 (BJ2 #3). 계약 자체는 tools/cascade/s1_contract.py --selftest.

    여기서 보는 것은 "생성기가 계약을 실제로 쓰는가" 다 — 음성 경로 포함.
    """
    from ase.io import read as _read
    ok = bad = 0

    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += bool(c); bad += (not c)

    base = _read(str(Path(__file__).resolve().parents[2]
                     / 'db/structures/lpscl_F43m_24G_ideal_Clcage_2026_11_17.cif'))   # 2026-11-17: 깨진 정본 대신
    pm = build_parent_site_map(base)
    chk(pm['counts'] == {'Cl_4d': 4, 'Li_any': 24, 'P_4b': 4, 'S_16e': 16, 'S_4a': 4},
        f"부모 지도 동결: {pm['counts']}")

    # ⭐ P0-2 회귀: P 절반을 치환한 뒤 배위로 다시 분류하면 S_16e 가 반토막 난다
    car = SiteCarrier(pm, base.get_chemical_symbols())
    tgt = parent_host_indices(car, 'P_4b')[:2]
    new = base.copy(); sy = new.get_chemical_symbols()
    for i in tgt:
        sy[i] = 'Nd'
    new.set_chemical_symbols(sy); car.substitute(tgt, 'Nd', sy)
    legacy_16e = len(find_host_indices_for_site(new, 'S_16e'))
    legacy_4a = len(find_host_indices_for_site(new, 'S_4a'))
    chk(legacy_16e == 8 and legacy_4a == 12,
        f"P0-2 재현: 옛 배위 재분류는 S_16e {legacy_16e} (참 16) · S_4a {legacy_4a} (참 4)")
    chk(len(parent_host_indices(car, 'S_16e')) == 16 and len(parent_host_indices(car, 'S_4a')) == 4,
        "계약 경로는 부모 자리를 그대로 승계한다 (16 · 4)")

    # ⭐ 음이온 항이 빠지던 수지
    Q = {'Nd': 3, 'Cl': -1}
    SQ = {'P_4b': HOST_SITES['P_4b']['charge'], 'S_4a': HOST_SITES['S_4a']['charge']}
    pl = [{'element': 'Nd', 'site': 'P_4b', 'n': 1}, {'element': 'Cl', 'site': 'S_4a', 'n': 3}]
    chk(charge_ledger(pl[:1], Q, SQ)['net_charge'] == -2
        and charge_ledger(pl, Q, SQ)['required'] == {'li_vacancy': 1},
        "NdCl₃: 양이온만 보면 −2 (Li 침입 2), 음이온까지 보면 +1 (Li 공공 1)")

    # ⛔음성: 계약 enforce 인데 지도를 안 넘기면 시작하지 않는다
    try:
        _host_sites(new, None, 'S_16e', 'enforce'); n1 = False
    except S1ContractError as e:
        n1 = '부모 자리 지도가 없다' in str(e)
    chk(n1, "⛔음성: enforce 인데 carrier 가 없으면 멈춘다")

    # ⛔음성: 농도가 정수가 아니면 생성 거부 (묵시적 1 unit 없음)
    try:
        quantize_concentration(0.1, 4); n2 = False
    except S1ContractError:
        n2 = True
    chk(n2, "⛔음성: x=0.1·n_fu=4 는 거부 (옛 max(1,round) 이면 1 unit 을 넣었다)")

    # ⛔음성: info['concentration'] 키 충돌 회귀 — 하류가 float 로 읽는 자리를 dict 로 덮지 않는다
    src = Path(__file__).read_text(encoding='utf-8')
    _needle = "info['conc" + "entration'] = _q"      # 쪼개 둔다 — 안 그러면 이 줄 자신이 걸린다
    chk(_needle not in src,
        "⛔음성: 양자화 기록을 info['concentration'] 에 넣지 않는다 (하류가 float 로 읽는 키)")
    # ⭐ 회신 BO 조건 2 — index_plan: 공통 부모 배열을 P1/P2 로 복제
    _car0 = SiteCarrier(pm, base.get_chemical_symbols())
    _li = parent_host_indices(_car0, 'Li_24g'); _s16 = parent_host_indices(_car0, 'S_16e')
    _plan = {'cation_sites': _li[:2], 'anion_sites': _s16[:3], 'vacancy_sites': _li[2:6]}
    def _run(comp):
        c = SiteCarrier(pm, base.get_chemical_symbols())
        return substitute_compound_at_sites(base.copy(), comp, 1, 'Li_24g', 'S_16e', 'random', 7,
                                            DOPANT_DB, carrier=c, contract='enforce', index_plan=_plan)
    try:
        d1, l1 = _run({'Al': 2, 'O': 3}); d2, l2 = _run({'Al': 2, 'S': 3})
        u1, u2 = l1['index_plan_used'], l2['index_plan_used']
        chk(u1['cation_sites'] == {'Al': _li[:2]} and u2['cation_sites'] == {'Al': _li[:2]},
            "index_plan: P1/P2 가 같은 Al 자리를 쓴다 (CLI 자리명 Li_24g → 부모지도 Li_any 로 접힘)")
        chk(u1['anion_sites'] == {'O': _s16[:3]} and u2['anion_sites'] == {'S': _s16[:3]},
            "index_plan: 같은 16e 인덱스에 P1 은 O, P2 는 S(no-op)")
        chk(u1['vacancy_sites'] == _li[2:6] == u2['vacancy_sites'], "index_plan: 같은 공공 4")
        chk(len(d1) == len(d2) == len(base) - 4 and u1['from_plan'] and u2['from_plan'],
            "index_plan: 둘 다 204→48원자(1×1×1: 52−4) · from_plan 표시")
        _sy1 = d1.get_chemical_symbols(); _sy2 = d2.get_chemical_symbols()
        chk(sum(a != b for a, b in zip(_sy1, _sy2)) == 3,
            "index_plan: 두 구조의 심볼 차이가 정확히 3 (O₃ vs S₃)")
    except Exception as _e:
        chk(False, f"index_plan 양성 경로 예외: {_e}")
    # ⭐ 2026-09-13 — positional(원소 무관) 판. `--emit_index_plan` 이 by_element 만 떨구면
    #   그 표는 O 로 굳어 있어 **no-op S₃ 짝이 계약거부로 막힌다** (파일럿 실행 중 실측).
    #   이 자리가 P1/P2 가 실제로 같은 파일을 쓰는 경로다.
    try:
        _cf = SiteCarrier(pm, base.get_chemical_symbols())
        _dp, _lp = substitute_compound_at_sites(base.copy(), {'Al': 2, 'O': 3}, 1, 'Li_24g', 'S_16e',
                                                'random', 7, DOPANT_DB, carrier=_cf,
                                                contract='enforce')
        _pos = _lp.get('index_plan_used_positional')
        chk(isinstance(_pos, dict) and isinstance(_pos['anion_sites'], list)
            and isinstance(_pos['cation_sites'], list),
            "positional: 자리당 원소 1개면 리스트 판을 같이 낸다")
        chk(_pos['anion_sites'] == _lp['index_plan_used']['anion_sites']['O']
            and _pos['cation_sites'] == _lp['index_plan_used']['cation_sites']['Al'],
            "positional: by_element 판과 **같은 인덱스**다 (다른 자리를 고르지 않는다)")
        # 그 리스트 판으로 no-op S₃ 를 실제로 만든다 — 이게 막혔던 그 경로다
        _c2 = SiteCarrier(pm, base.get_chemical_symbols())
        _d2, _l2 = substitute_compound_at_sites(base.copy(), {'Al': 2, 'S': 3}, 1, 'Li_24g', 'S_16e',
                                                'random', 7, DOPANT_DB, carrier=_c2,
                                                contract='enforce', index_plan=_pos)
        chk(_l2['index_plan_used']['anion_sites']['S'] == _pos['anion_sites'],
            "positional: O 로 떨군 표로 **S no-op 짝**이 같은 자리에 만들어진다")
        chk(sum(a != b for a, b in zip(_dp.get_chemical_symbols(),
                                       _d2.get_chemical_symbols())) == 3,
            "positional: 두 구조 차이가 정확히 3 (O₃ ↔ S₃)")
    except Exception as _e:
        chk(False, f"positional 양성 경로 예외: {_e}")

    # ⛔음성: by_element 표로 다른 원소를 놓으려 하면 거부하고, **positional 을 이름으로 댄다**
    try:
        _cb = SiteCarrier(pm, base.get_chemical_symbols())
        substitute_compound_at_sites(base.copy(), {'Al': 2, 'S': 3}, 1, 'Li_24g', 'S_16e',
                                     'random', 7, DOPANT_DB, carrier=_cb, contract='enforce',
                                     index_plan={'cation_sites': {'Al': _li[:2]},
                                                 'anion_sites': {'O': _s16[:3]},
                                                 'vacancy_sites': _li[2:6]})
        chk(False, "⛔음성: by_element 표 + 다른 원소 → 거부해야 한다")
    except S1ContractError as _e:
        chk('positional' in str(_e),
            "⛔음성: 거부 문구가 **positional 경로를 이름으로 댄다** (막다른 골목이 아니다)")
    except Exception as _e:
        chk(False, f"⛔음성: 예상과 다른 예외 {type(_e).__name__}: {_e}")

    # ⛔음성: 한 자리에 원소가 둘이면 positional 판을 **안 만든다** (접으면 원소를 잃는다)
    try:
        _cm = SiteCarrier(pm, base.get_chemical_symbols())
        _dm, _lm = substitute_compound_at_sites(base.copy(), {'Al': 2, 'O': 2, 'S': 1}, 1,
                                                'Li_24g', 'S_16e', 'random', 7, DOPANT_DB,
                                                carrier=_cm, contract='enforce')
        _multi = len(_lm['index_plan_used']['anion_sites']) > 1
        chk(_multi and 'index_plan_used_positional' not in _lm,
            "⛔음성: 음이온 자리에 원소 2종이면 positional 판을 만들지 않는다")
    except S1ContractError:
        chk(True, "⛔음성: 혼합 음이온 처방 자체가 계약에서 거부된다 (그래도 조용한 접힘은 없다)")
    except Exception as _e:
        chk(False, f"⛔음성: 혼합 음이온에서 예상 밖 예외 {type(_e).__name__}: {_e}")

    for _bad_plan, _msg in (
        ({**_plan, 'vacancy_sites': [-1, 0, 1, 2]}, "⛔음성: 허용 집합 밖 인덱스 → 거부"),
        ({**_plan, 'cation_sites': _li[:1]}, "⛔음성: 길이 불일치(1≠2) → 거부"),
        ({**_plan, 'anion_sites': [_s16[0], _s16[0], _s16[1]]}, "⛔음성: 중복 인덱스 → 거부"),
        ({**_plan, 'cation_sites': _s16[:2]}, "⛔음성: S 자리를 Al 자리로 지정 → 거부"),
    ):
        try:
            c = SiteCarrier(pm, base.get_chemical_symbols())
            substitute_compound_at_sites(base.copy(), {'Al': 2, 'O': 3}, 1, 'Li_24g', 'S_16e', 'random', 7,
                                         DOPANT_DB, carrier=c, contract='enforce', index_plan=_bad_plan)
            chk(False, _msg)
        except S1ContractError:
            chk(True, _msg)
    # ══ 카드 v4 §1b — 음이온 자리의 부모 양이온 분산 (BO 조건 2) ══════════════
    #   ⛔ 이 규칙이 없으면 O 3개가 같은 PS4 에 몰려 PS1O3 한 덩어리가 된다.
    #     기존 선택기는 이것을 보장하지 않는다(docstring 이 스스로 인정한다).
    try:
        _pmap_all = anion_parent_map(base, _s16, 'P', 2.6)
        chk(len(_pmap_all) == len(_s16) and all(base.get_chemical_symbols()[v] == 'P'
                                                for v in _pmap_all.values()),
            "부모지도: S_16e 전부가 P 하나에 배정된다")
        _groups = {}
        for _si, _pj in _pmap_all.items():
            _groups.setdefault(_pj, []).append(_si)
        chk(all(len(v) == 4 for v in _groups.values()),
            f"부모지도: PS₄ 라 부모당 S 가 4개씩 ({sorted(len(v) for v in _groups.values())})")

        _sel = select_distinct_parent_sites(_s16, 3, 'random', 7, base, 'P', 2.6)
        _par = [_pmap_all[i] for i in _sel]
        chk(len(set(_par)) == 3, f"선택기: 부모가 서로 다른 3자리 (부모 {_par})")
        chk(_sel == select_distinct_parent_sites(_s16, 3, 'random', 7, base, 'P', 2.6),
            "선택기: 같은 seed → 같은 결과 (재현성)")

        # 양성: 규칙을 켜고 돌면 통과하고 기록이 남는다
        _c = SiteCarrier(pm, base.get_chemical_symbols())
        _d, _l = substitute_compound_at_sites(
            base.copy(), {'Al': 2, 'O': 3}, 1, 'Li_24g', 'S_16e', 'random', 7,
            DOPANT_DB, carrier=_c, contract='enforce', distinct_anion_parent=True)
        _op = [q for q in _l['placements'] if q['element'] == 'O'][0]
        chk(_op['distinct_parent_rule'] and len(set(_op['parent_map'].values())) == 3,
            "양성: 규칙 켜고 생성 → 부모 3종 · placement_log 에 parent_map 기록")
    except Exception as _e:
        chk(False, f"부모 분산 양성 경로 예외: {_e}")

    # ⛔음성 ① 같은 부모에 2개를 넣은 index_plan 은 거부된다
    _same_parent = sorted(_groups[sorted(_groups)[0]])[:2] + [sorted(_groups[sorted(_groups)[1]])[0]]
    try:
        _c = SiteCarrier(pm, base.get_chemical_symbols())
        substitute_compound_at_sites(
            base.copy(), {'Al': 2, 'O': 3}, 1, 'Li_24g', 'S_16e', 'random', 7, DOPANT_DB,
            carrier=_c, contract='enforce',
            index_plan={**_plan, 'anion_sites': _same_parent}, distinct_anion_parent=True)
        chk(False, "⛔음성: 같은 부모 P 에 O 2개인 index_plan → 거부")
    except S1ContractError:
        chk(True, "⛔음성: 같은 부모 P 에 O 2개인 index_plan → 거부")

    # ⛔음성 ② 규칙을 끄면 **그 계획이 통과한다** — 위 거부가 규칙 덕분임을 보인다
    #    (이게 없으면 다른 이유로 거부된 것일 수도 있어 시험이 아무것도 안 본 게 된다)
    try:
        _c = SiteCarrier(pm, base.get_chemical_symbols())
        _d0, _l0 = substitute_compound_at_sites(
            base.copy(), {'Al': 2, 'O': 3}, 1, 'Li_24g', 'S_16e', 'random', 7, DOPANT_DB,
            carrier=_c, contract='enforce',
            index_plan={**_plan, 'anion_sites': _same_parent}, distinct_anion_parent=False)
        _op0 = [q for q in _l0['placements'] if q['element'] == 'O'][0]
        chk(_op0['distinct_parent_rule'] is False and 'parent_map' not in _op0,
            "⛔음성 대조: 규칙을 끄면 같은 계획이 통과한다 (거부가 이 규칙 덕분임을 보인다)")
    except Exception as _e:
        chk(False, f"규칙 OFF 대조 경로 예외: {_e}")

    # ⛔음성 ③ 부모 종류보다 많이 요구하면 **조용히 완화하지 않고 멈춘다**
    try:
        select_distinct_parent_sites(_s16, len(_groups) + 1, 'random', 7, base, 'P', 2.6)
        chk(False, "⛔음성: 부모 종류보다 많은 자리 요구 → 거부")
    except S1ContractError:
        chk(True, "⛔음성: 부모 종류보다 많은 자리 요구 → 거부 (조용한 완화 없음)")

    # ⛔음성 ④ 컷오프가 너무 작으면 부모를 못 정하고 멈춘다 (추측하지 않는다)
    try:
        anion_parent_map(base, _s16[:1], 'P', 0.5)
        chk(False, "⛔음성: 컷오프 0.5 Å → 부모 없음으로 거부")
    except S1ContractError:
        chk(True, "⛔음성: 컷오프 0.5 Å → 부모 없음으로 거부 (추측하지 않는다)")


    # ⛔음성 ⑤ (2026-11-17) 할로젠–S 접촉 관문 — 정본 F-43m CIF 는 Cl 이 4d 구멍 (PS₄ S 넷에서 2.36 Å)
    _root = Path(__file__).resolve().parents[2]
    _broken = _read(str(_root / 'db/structures/lpscl_F43m_24G_canonical.cif'))
    _bc = halide_s_contacts(_broken)
    _bmin = min(b[2] for b in _bc) if _bc else float('nan')
    chk(len(_bc) == 16 and abs(_bmin - 2.356) < 0.01,
        f"⛔음성: 깨진 정본 CIF 의 할로젠–S < 3 Å 쌍 16 · 최소 2.356 Å (잰 값 {len(_bc)} 쌍 · {_bmin:.3f} Å)")
    try:
        refuse_unphysical_base(_broken, 'selftest 깨진 정본')
        chk(False, "⛔음성: 깨진 정본을 base 로 주면 시작하지 않는다")
    except SystemExit as e:
        chk('4d' in str(e) and 'comp1_V0_k444' in str(e),
            "⛔음성: 깨진 정본 → SystemExit (이유와 쓸 경로를 같이 말한다)")
    refuse_unphysical_base(_broken, 'selftest 옛 기록 재현', allow=True)   # 경고만 — 예외면 시험이 여기서 죽는다
    chk(True, "allow=True (옛 기록 재현) 는 경고만 하고 계속한다")
    for _p in ('db/structures/lpscl_F43m_24G_ideal_Clcage_2026_11_17.cif', 'db/structures/comp1_V0_k444.cif'):
        chk(halide_s_contacts(_read(str(_root / _p))) == [], f"⭕양성: {_p.split('/')[-1]} 할로젠–S 접촉 없음")

    print(f"selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--selftest', action='store_true', help='S1 계약 결선 시험 (음성 경로 포함)')
    if '--selftest' in sys.argv:
        raise SystemExit(_selftest())
    parser.add_argument('--base', required=True, help='LPSCl base structure')
    parser.add_argument('--allow_unphysical_base', action='store_true',
                        help='할로젠–S < 3 Å base 를 경고만 하고 계속 (봉인된 옛 기록 재현용 · 새 설계에 쓰지 않는다)')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument('--supercell', nargs=3, type=int, default=[1, 1, 1],
                       metavar=('NX', 'NY', 'NZ'),
                       help='Multiply base cell (default 1 1 1 = 4 f.u. / 52 atoms; '
                            '2 1 1 = 8 f.u., 2 2 1 = 16 f.u., 2 2 2 = 32 f.u. — '
                            'needed when combining Type A + Type B doping at low '
                            'concentrations so a single integer atom does not '
                            'exceed the requested mole fraction).')
    parser.add_argument('--s1_contract', choices=['enforce', 'legacy_bypass'], default='enforce',
                       help="S1 계약 (BJ2 재심 조건 #3). enforce=부모 자리 승계·전체 보상 수지·"
                            "실패 시 중단. legacy_bypass=옛 배위 재분류 경로 (기록에 낙인 찍힌다)")
    parser.add_argument('--quantize_policy', choices=['exact', 'approve_nearest', 'refuse'],
                       default='exact',
                       help="요청 농도가 유한 셀에서 정수가 아닐 때. exact=생성 거부(기본) · "
                            "approve_nearest=--quantize_approved_by 와 함께 승인 양자화 · refuse=무조건 거부. "
                            "옛 max(1,round) 묵시 삽입은 없다 (BJ2 Q6)")
    parser.add_argument('--quantize_approved_by', default=None, help='양자화 승인자 (사람 이름/역할)')
    parser.add_argument('--max_quantize_rel_error', type=float, default=None,
                       help='양자화 상대오차 상한 — 넘으면 거부')
    parser.add_argument('--auto_anion_sites', action='store_true',
                       help='For Type A: generate one structure per available '
                            'anion site (S_16e, S_4a, Cl_4d) instead of using '
                            'a single --anion_site. Lets UMA energy decide '
                            'whether O prefers PS4→PO4 (S_16e), free O²⁻ (S_4a), '
                            'or oxychloride (Cl_4d).')
    parser.add_argument('--auto_cation_sites', action='store_true',
                       help='For Type A: also iterate cation sites '
                            '{Li_24g, Li_48h, P_4b}.')
    parser.add_argument('--allow_exotic', action='store_true',
                       help='Bypass the site_preference radius filter and let '
                            'UMA energy rank chemically unusual placements '
                            '(e.g., La at P_4b, B at Li_24g, O at P_4b). '
                            'Useful when --auto_*_sites would otherwise drop '
                            'a combination you want to explore manually.')

    # Type A
    parser.add_argument('--compound',
                       help="Compound formula, e.g., 'Nd2O3', 'MgO', 'Al2O3'")
    parser.add_argument('--x_compound', type=float, default=0.05,
                       help='Mole fraction of compound per f.u. (default 0.05)')
    parser.add_argument('--cation_site', default='Li_24g',
                       help='Target site for cations (default Li_24g)')
    parser.add_argument('--anion_site', default='S_16e',
                       help='Target site for anions (default S_16e; ACS AMI 2021 '
                            'shows O prefers S_16e — PS4 → PO4 formation)')

    # Type B
    parser.add_argument('--halide_rich',
                       help="Halide element for Li6-xPS5-xX1+x family, e.g. 'Cl'")
    parser.add_argument('--excess_per_fu', type=float,
                       help='Halide excess x per f.u. (e.g., 0.6 for Li5.4PS4.4Cl1.6)')
    parser.add_argument('--mixed_halides',
                       help="Multi-halide co-substitution as 'Cl:0.3,Br:0.3' — "
                            "reproduces LPSClBr / comp2-5 chemistry. Excess "
                            "values sum to total S→halide swap fraction per f.u.")
    parser.add_argument('--mixed_compounds',
                       help="Multi-compound (이중 화합물 / high-entropy) doping "
                            "as 'Nd2O3:0.025,Al2O3:0.025,MgO:0.05'. Each pair "
                            "compound:x_compound is applied sequentially at "
                            "the chosen --cation_site / --anion_site; Li "
                            "vacancies / interstitials accumulate over all "
                            "compounds for global charge balance. Use this "
                            "for high-entropy oxide screening (Nd+La+Sm+Y "
                            "simultaneously) — newer sulfide-SE direction "
                            "than single-cation doping.")
    parser.add_argument('--vacancy_method', default='random',
                       choices=['random', 'spread', 'cluster', 'first',
                                'near_cation'],
                       help='Method for Li vacancy placement (default random — '
                            'matches experimental Kraft 2017 NMR / Adeli 2019 '
                            'PDF showing Li vacancies are disordered, not '
                            'arranged in a superlattice). "near_cation" '
                            'biases vacancy formation toward Li atoms within '
                            '--vacancy_cutoff Å of the aliovalent dopant, '
                            'matching the local charge-compensation picture '
                            '(Pham 2021 oxysulfide; aliovalent defect '
                            'theory).')
    parser.add_argument('--vacancy_cutoff', type=float, default=5.0,
                       help='Radius (Å) for --vacancy_method near_cation; '
                            'default 5.0 ≈ 2× P-S bond, captures the dopant '
                            "cation's first/second coordination shells.")

    # Type C (chain Type A + Type B)
    parser.add_argument('--also_halide_rich',
                       help='After Type A, additionally do halide-rich swap')

    # Common
    parser.add_argument('--n_fu', type=int, default=4,
                       help='Number of formula units in the base cell (default 4)')
    parser.add_argument('--method', default='spread',
                       choices=['spread', 'random', 'first'])
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--index_plan', default=None,
                        help='⭐ 회신 BO 조건 2: 공통 부모 배열의 인덱스 표(JSON). 주면 난수 대신 이 자리를 쓴다 '
                             '(cation_sites·anion_sites·vacancy_sites). P1/P2 짝은 같은 파일을 준다')
    parser.add_argument('--distinct_anion_parent', action='store_true',
                        help='⭐ 카드 v4 §1b (BO 조건 2): 음이온 치환 자리들이 **서로 다른 부모 양이온**에 '
                             '속하도록 강제한다. O 3개가 같은 PS4 에 몰리면 PS1O3 한 덩어리가 되어 '
                             '희석 치환이 아니게 되기 때문이다. index_plan 으로 넣은 자리도 **검사한다**. '
                             '만족 못 하면 조용히 완화하지 않고 멈춘다')
    parser.add_argument('--anion_parent_symbol', default='P',
                        help='부모 양이온 원소 (기본 P — S_16e 의 PS4 중심)')
    parser.add_argument('--anion_parent_cutoff', type=float, default=2.6,
                        help='부모 판정 거리 컷오프 Å (기본 2.6). 컷오프 안에 부모가 0개거나 2개 이상이면 멈춘다')
    parser.add_argument('--emit_index_plan', default=None,
                        help='첫 성공 구조가 실제로 쓴 인덱스 표를 이 JSON 으로 떨군다 — 짝 처방이 --index_plan 으로 재사용')
    parser.add_argument('--emit_plan_shape', choices=['by_element', 'positional'],
                        default='by_element',
                        help='--emit_index_plan 의 모양. by_element(기본) = {"O": [...]} 원소 고정. '
                             'positional = [...] 원소 무관 — **P1/P2 짝(같은 자리·다른 원소)은 이것을 쓴다**. '
                             '자리 하나에 원소가 둘 이상이면 positional 은 만들 수 없어 거부한다')
    parser.add_argument('--n_seeds', type=int, default=1,
                       help='Ensemble size (only meaningful with --method random)')
    args = parser.parse_args()
    _index_plan = json.load(open(args.index_plan)) if args.index_plan else None
    _index_plan_emitted = [False]

    if (not args.compound and not args.halide_rich
            and not args.mixed_halides and not args.mixed_compounds):
        parser.error(
            "Provide --compound (Type A), --halide_rich (Type B), "
            "--mixed_halides (Type B'), or --mixed_compounds (Type D — "
            "이중 / high-entropy co-doping)")

    base = read(args.base)
    # ⛔ 2026-11-17 — base 의 할로젠–S 접촉을 잰다 (정본 F-43m CIF 는 Cl 이 4d 구멍 · 이름이 아니라 거리로 막는다)
    refuse_unphysical_base(base, f"--base {args.base}", allow=args.allow_unphysical_base)
    if args.supercell != [1, 1, 1]:
        base = base.repeat(args.supercell)
        # Scale n_fu by the supercell multiplier
        cell_mult = args.supercell[0] * args.supercell[1] * args.supercell[2]
        n_fu_actual = args.n_fu * cell_mult
        print(f"Supercell {args.supercell}: base now {len(base)} atoms, "
              f"n_fu={n_fu_actual}")
    else:
        n_fu_actual = args.n_fu
    print(f"Loaded base: {len(base)} atoms, composition: {composition_summary(base)}")
    print(f"Effective f.u. per cell: {n_fu_actual}")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    seeds = ([args.seed] if args.method != 'random'
             else [args.seed + i for i in range(args.n_seeds)])

    # Decide the (cation_site, anion_site) combinations to iterate.
    if args.auto_cation_sites:
        cation_sites = ['Li_24g', 'Li_48h', 'P_4b']
    else:
        cation_sites = [args.cation_site]
    if args.auto_anion_sites:
        anion_sites = ['S_16e', 'S_4a', 'Cl_4d']
    else:
        anion_sites = [args.anion_site]

    # Pre-filter site combinations against site_preference (only when iterating
    # auto modes — explicit single-site requests are kept as-is to let the user
    # force unusual placements like Sundar-style oxide-at-anion-site coatings).
    # --allow_exotic bypasses the filter so every combination is tried.
    if args.compound and not args.allow_exotic:
        compound_atoms = parse_compound(args.compound)
        cations_in = [el for el, _ in compound_atoms.items()
                      if DOPANT_DB.get(el, {}).get('charge', 0) > 0]
        anions_in = [el for el, _ in compound_atoms.items()
                     if DOPANT_DB.get(el, {}).get('charge', 0) < 0]
        if args.auto_cation_sites:
            allowed_c = set.intersection(*(compatible_sites_for_element(c, DOPANT_DB)
                                           for c in cations_in)) if cations_in else set()
            before = list(cation_sites)
            cation_sites = [s for s in cation_sites if s in allowed_c]
            if before != cation_sites:
                print(f"  site_preference filter (cations {cations_in}): "
                      f"{before} → {cation_sites}")
        if args.auto_anion_sites:
            allowed_a = set.intersection(*(compatible_sites_for_element(a, DOPANT_DB)
                                           for a in anions_in)) if anions_in else set()
            before = list(anion_sites)
            anion_sites = [s for s in anion_sites if s in allowed_a]
            if before != anion_sites:
                print(f"  site_preference filter (anions {anions_in}): "
                      f"{before} → {anion_sites}")
        if args.auto_cation_sites and not cation_sites:
            parser.error(f"No compatible cation sites for {cations_in}")
        if args.auto_anion_sites and not anion_sites:
            parser.error(f"No compatible anion sites for {anions_in}")

    print(f"Iterating: {len(cation_sites)} cation sites × "
          f"{len(anion_sites)} anion sites × {len(seeds)} seeds = "
          f"{len(cation_sites)*len(anion_sites)*len(seeds)} structures")

    generated: list[dict] = []
    refusals: list[dict] = []          # ⭐ 계약 거부는 **물리적 탈락이 아니다** — 따로 센다 (BJ2 Q6)
    parent_map = None
    if args.s1_contract == 'enforce':
        parent_map = build_parent_site_map(base)
        print(f"S1 계약 enforce — 부모 자리 지도 동결: {parent_map['counts']} · {parent_map['digest'][:23]}…")
    else:
        print("⚠⚠ S1 계약 legacy_bypass — 치환 뒤 **현재 배위**로 자리를 다시 분류한다 (BJ2 P0-2 경로). "
              "이 실행의 산출물은 계약본과 섞지 않는다.")

    def _refuse(kind, detail, **ctx):
        rec = {'kind': kind, 'detail': str(detail), 'is_physics_elimination': False, **ctx}
        refusals.append(rec)
        print(f"  ⛔ 계약거부[{kind}] {detail}")

    for cation_site in cation_sites:
      for anion_site in anion_sites:
        for seed in seeds:
            doped = base.copy()
            carrier = (SiteCarrier(parent_map, doped.get_chemical_symbols())
                       if parent_map is not None else None)
            info: dict = {
                's1_contract': args.s1_contract,
                'seed': seed,
                'cation_site_used': cation_site,
                'anion_site_used': anion_site,
                'steps': [],
            }

            # --- Type A ---
            if args.compound:
                composition = parse_compound(args.compound)
                try:
                    _q = quantize_concentration(
                        args.x_compound, n_fu_actual, policy=args.quantize_policy,
                        approved_by=args.quantize_approved_by,
                        max_rel_error=args.max_quantize_rel_error, label='x_compound')
                except S1ContractError as e:
                    _refuse('concentration_quantization', e, compound=args.compound,
                            x_request=args.x_compound, n_fu=n_fu_actual, seed=seed)
                    continue
                n_units, actual_x = _q['n_units'], _q['x_actual']
                if not _q['is_doped_candidate']:
                    _refuse('undoped_control_not_a_doped_candidate',
                            f"x={args.x_compound} → 0 unit", compound=args.compound, seed=seed)
                    continue
                info['concentration_quantization'] = _q   # ⛔ 'concentration' 은 뒤에서 float 로 쓰인다
                try:
                    doped, log = substitute_compound_at_sites(
                        doped, composition, n_units,
                        cation_site, anion_site,
                        args.method, seed, DOPANT_DB,
                        vacancy_method=args.vacancy_method,
                        vacancy_cutoff=args.vacancy_cutoff,
                        carrier=carrier, contract=args.s1_contract,
                        index_plan=_index_plan,
                        distinct_anion_parent=args.distinct_anion_parent,
                        anion_parent_symbol=args.anion_parent_symbol,
                        anion_parent_cutoff=args.anion_parent_cutoff)
                    if args.emit_index_plan and not _index_plan_emitted[0]:
                        _key = ('index_plan_used_positional'
                                if args.emit_plan_shape == 'positional' else 'index_plan_used')
                        if _key not in log:
                            raise S1ContractError(
                                f"⛔ --emit_plan_shape positional 을 요청했는데 만들 수 없다 — "
                                f"한 자리에 원소가 둘 이상이다 "
                                f"(cation {sorted(log['index_plan_used']['cation_sites'])} · "
                                f"anion {sorted(log['index_plan_used']['anion_sites'])}). "
                                f"리스트로 접으면 어느 인덱스가 어느 원소였는지 잃는다 — "
                                f"by_element 로 떨구고 짝 처방 쪽을 다르게 풀어라")
                        Path(args.emit_index_plan).write_text(
                            json.dumps(log[_key], ensure_ascii=False, indent=1))
                        _index_plan_emitted[0] = True
                        print(f"  index_plan[{args.emit_plan_shape}] → {args.emit_index_plan}")
                    info['steps'].append({
                        'type': 'A_compound',
                        'compound': args.compound,
                        'composition': composition,
                        'n_units': n_units,
                        'actual_x': actual_x,
                        **log,
                    })
                except (ValueError, S1ContractError) as e:
                    _refuse('generator_contract', e, compound=args.compound,
                            cation_site=cation_site, anion_site=anion_site, seed=seed)
                    continue

            # --- Type B (single halide) ---
            if args.halide_rich:
                if args.excess_per_fu is None:
                    parser.error("--halide_rich requires --excess_per_fu")
                try:
                    _qb = quantize_concentration(
                        args.excess_per_fu, n_fu_actual, policy=args.quantize_policy,
                        approved_by=args.quantize_approved_by,
                        max_rel_error=args.max_quantize_rel_error, label='excess_per_fu')
                except S1ContractError as e:
                    _refuse('concentration_quantization', e, halide=args.halide_rich,
                            x_request=args.excess_per_fu, n_fu=n_fu_actual, seed=seed)
                    continue
                n_swap = _qb['n_units']
                if not _qb['is_doped_candidate']:
                    _refuse('undoped_control_not_a_doped_candidate',
                            f"excess={args.excess_per_fu} → 0 swap", halide=args.halide_rich, seed=seed)
                    continue
                doped, log = halide_rich_swap(
                    doped, args.halide_rich, n_swap,
                    anion_site if anion_site.startswith('S') else 'S_4a',
                    args.method, seed + 50,
                    vacancy_method=args.vacancy_method,
                    carrier=carrier, contract=args.s1_contract)
                info['steps'].append({
                    'type': 'B_halide_rich',
                    'halide': args.halide_rich,
                    'n_swap': n_swap,
                    'actual_excess': n_swap / n_fu_actual,
                    **log,
                })
            # --- Type B' (mixed halides — LPSClBr) ---
            elif args.mixed_halides:
                # Parse 'Cl:0.3,Br:0.3' format
                mix = {}
                for entry in args.mixed_halides.split(','):
                    h, x = entry.split(':')
                    mix[h.strip()] = float(x)
                try:
                    doped, log = mixed_halide_swap(
                        doped, mix, n_fu_actual,
                        anion_site if anion_site.startswith('S') else 'S_4a',
                        args.method, seed + 60,
                        vacancy_method=args.vacancy_method,
                        carrier=carrier, contract=args.s1_contract,
                        quantize_policy=args.quantize_policy,
                        approved_by=args.quantize_approved_by)
                except S1ContractError as e:
                    _refuse('concentration_quantization', e, mix=mix, n_fu=n_fu_actual, seed=seed)
                    continue
                info['steps'].append({
                    'type': 'B_mixed_halide',
                    'mix': mix,
                    **log,
                })
            elif args.also_halide_rich:
                if args.excess_per_fu is None:
                    parser.error("--also_halide_rich requires --excess_per_fu")
                try:
                    _qc = quantize_concentration(
                        args.excess_per_fu, n_fu_actual, policy=args.quantize_policy,
                        approved_by=args.quantize_approved_by,
                        max_rel_error=args.max_quantize_rel_error, label='excess_per_fu(chain)')
                except S1ContractError as e:
                    _refuse('concentration_quantization', e, halide=args.also_halide_rich,
                            x_request=args.excess_per_fu, n_fu=n_fu_actual, seed=seed)
                    continue
                n_swap = _qc['n_units']
                if not _qc['is_doped_candidate']:
                    _refuse('undoped_control_not_a_doped_candidate',
                            f"excess={args.excess_per_fu} → 0 swap", halide=args.also_halide_rich, seed=seed)
                    continue
                doped, log = halide_rich_swap(
                    doped, args.also_halide_rich, n_swap,
                    'S_4a', args.method, seed + 70,
                    vacancy_method=args.vacancy_method,
                    carrier=carrier, contract=args.s1_contract)
                info['steps'].append({
                    'type': 'C_chain_halide_rich',
                    'halide': args.also_halide_rich,
                    'n_swap': n_swap,
                    **log,
                })

            # --- Type D (multi-compound / high-entropy) ---
            if args.mixed_compounds:
                compound_specs = []
                for entry in args.mixed_compounds.split(','):
                    cname, xstr = entry.strip().split(':')
                    compound_specs.append((cname.strip(), float(xstr)))
                step_seed = seed + 80
                for cname, x_each in compound_specs:
                    composition = parse_compound(cname)
                    try:
                        _qd = quantize_concentration(
                            x_each, n_fu_actual, policy=args.quantize_policy,
                            approved_by=args.quantize_approved_by,
                            max_rel_error=args.max_quantize_rel_error, label=f'mixed:{cname}')
                        n_units = _qd['n_units']
                        if not _qd['is_doped_candidate']:
                            raise S1ContractError(f"x={x_each} → 0 unit (무도핑 대조군, 도핑 후보 아님)")
                        doped, log = substitute_compound_at_sites(
                            doped, composition, n_units,
                            cation_site, anion_site,
                            args.method, step_seed, DOPANT_DB,
                            vacancy_method=args.vacancy_method,
                            vacancy_cutoff=args.vacancy_cutoff,
                            carrier=carrier, contract=args.s1_contract,
                        index_plan=_index_plan,
                        distinct_anion_parent=args.distinct_anion_parent,
                        anion_parent_symbol=args.anion_parent_symbol,
                        anion_parent_cutoff=args.anion_parent_cutoff)
                        info['steps'].append({
                            'type': 'D_multi_compound',
                            'compound': cname, 'x': x_each,
                            'n_units': n_units,
                            **log,
                        })
                    except (ValueError, S1ContractError) as e:
                        _refuse('generator_contract', e, compound=cname, x=x_each, seed=seed)
                    step_seed += 10

            # Name + write
            parts = []
            if args.compound:
                parts.append(f"{args.compound}_x{int(args.x_compound*1000):03d}")
            if args.halide_rich:
                parts.append(
                    f"{args.halide_rich}rich_x{int(args.excess_per_fu*1000):03d}")
            if args.also_halide_rich:
                parts.append(
                    f"chain_{args.also_halide_rich}_x{int(args.excess_per_fu*1000):03d}")
            # Disambiguate by site combination only when iterating multiple
            if len(cation_sites) > 1 or len(anion_sites) > 1:
                site_tag = f"c{cation_site.replace('_','')}a{anion_site.replace('_','')}"
                parts.append(site_tag)
            if args.supercell != [1, 1, 1]:
                parts.append("sc" + "x".join(str(s) for s in args.supercell))
            if args.method == 'random':
                parts.append(f"s{seed - args.seed:02d}")
            name = "_".join(parts) if parts else "doped"
            xyz_path = out_dir / f'{name}.xyz'
            write(xyz_path, doped)

            # Derive grouping keys at write-time so downstream tools
            # (select_winners, combine_rankings) work even when this script
            # is called standalone (without run_compound_batch.sh's merge
            # step). Fixes the chain-integrity bug noted in the external
            # review (CR-2, 2026-05-16).
            type_a_step = next((s for s in info['steps']
                                if s.get('type') == 'A_compound'), None)
            type_b_step = next((s for s in info['steps']
                                if s.get('type') == 'B_halide_rich'), None)
            type_c_step = next((s for s in info['steps']
                                if s.get('type') == 'C_chain_halide_rich'), None)
            type_d_step = next((s for s in info['steps']
                                if s.get('type') == 'D_multi_compound'), None)
            type_bp_step = next((s for s in info['steps']
                                 if s.get('type') == 'B_mixed_halide'), None)
            if type_a_step and type_c_step:
                derived_dopant = f"{type_a_step['compound']}+{type_c_step['halide']}rich"
                comp_label = 'compound_set_chain'
                derived_conc = type_a_step.get('actual_x', 0.0)
            elif type_a_step and type_d_step:
                derived_dopant = type_a_step['compound'] + "+multi"
                comp_label = 'compound_set_multi'
                derived_conc = type_a_step.get('actual_x', 0.0)
            elif type_a_step:
                derived_dopant = type_a_step['compound']
                comp_label = 'compound_set'
                derived_conc = type_a_step.get('actual_x', 0.0)
            elif type_b_step:
                derived_dopant = f"{type_b_step['halide']}rich"
                comp_label = 'halide_rich_vac'
                derived_conc = type_b_step.get('actual_excess', 0.0)
            elif type_bp_step:
                derived_dopant = "+".join(f"{h}rich" for h in type_bp_step.get('mix', {}))
                comp_label = 'mixed_halide_vac'
                derived_conc = sum(type_bp_step.get('mix', {}).values())
            elif type_d_step:
                derived_dopant = type_d_step['compound'] + "+multi"
                comp_label = 'multi_compound'
                derived_conc = type_d_step.get('x', 0.0)
            else:
                derived_dopant = 'unknown'
                comp_label = 'unknown'
                derived_conc = 0.0

            info.update({
                'name': name,
                'dopant': derived_dopant,
                'site': cation_site,
                'anion_site_label': anion_site,
                'concentration': derived_conc,
                'charge_compensation': comp_label,
                'host': 'compound',
                'n_atoms': len(doped),
                'composition': composition_summary(doped),
                'xyz_file': str(xyz_path),
                'n_fu_actual': n_fu_actual,
                'supercell': args.supercell,
            })
            if carrier is not None:
                info['parent_sites'] = carrier.as_record()
            generated.append(info)
            print(f"  ✓ {name}: {len(doped)} atoms, {composition_summary(doped)}")

    summary = {
        'base_file': args.base,
        'n_fu': args.n_fu,
        'n_fu_actual': n_fu_actual,
        'supercell': args.supercell,
        'method': args.method,
        'n_seeds': args.n_seeds,
        'cation_sites_tried': cation_sites,
        'anion_sites_tried': anion_sites,
        'structures': generated,
        's1_contract': args.s1_contract,
        'parent_site_map': parent_map,
        'quantize_policy': args.quantize_policy,
        'contract_refusals': refusals,
        '⛔_refusal_semantics': ('contract_refusals 는 **코드 계약 실패**다. 물리적으로 나쁜 후보의 탈락으로 '
                                '세지 않는다 (BJ2 Q6). 무도핑 대조군도 도핑 후보 수에서 분리돼 있다.'),
    }
    summary['provenance'] = get_provenance()  # v4.5.13 NEW-1 fix
    summary_path = out_dir / 'compound_summary.json'
    summary_path.write_text(json.dumps(summary, indent=2, default=str))
    print(f"\n✓ Generated {len(generated)} structures")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    main()
