#!/usr/bin/env python
"""substitute_struct.py — Generate LPSCl + dopant structures.

For each (dopant, target_site, concentration) combo from
site_preference_initial.json, generates LPSCl-doped structure with
appropriate charge compensation (Li vacancy for donor, etc.).

Usage:
  # Default: all candidates from site_preference_initial.json, conc 0.05~0.20
  python3 substitute_struct.py \\
      --base data/lpscl_bulk.cif \\
      --site_pref data/doping_screening/site_preference_initial.json \\
      --concentrations 0.05 0.10 0.20 \\
      --out data/doping_screening/structures/

  # Single dopant test
  python3 substitute_struct.py --base data/lpscl_bulk.cif \\
      --dopant Mg --site Li_24g --conc 0.10 --out test_struct/
"""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import Atoms

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance

# Map site labels to host element (used to find substitution targets)
SITE_TO_HOST = {
    'Li_24g': 'Li', 'Li_48h': 'Li',
    'P_4b': 'P',
    'S_16e': 'S', 'S_4a': 'S',
    'Cl_4d': 'Cl',
}


def fetch_lpscl_from_mp(api_key: str = None, mp_id: str = 'mp-985592') -> Atoms:
    """Fetch Li6PS5Cl bulk structure from Materials Project.

    Common MP IDs for Li6PS5Cl: mp-985592, mp-987601 (variants).
    Falls back to manual structure if API not available.
    """
    try:
        from mp_api.client import MPRester
        with MPRester(api_key) as mpr:
            doc = mpr.materials.summary.search(material_ids=[mp_id])[0]
            struct = doc.structure
            from pymatgen.io.ase import AseAtomsAdaptor
            return AseAtomsAdaptor.get_atoms(struct)
    except Exception as e:
        print(f"  MP fetch failed: {e}")
        return None


def find_host_indices(atoms: Atoms, host_element: str) -> list[int]:
    """Find all atom indices matching host element."""
    return [i for i, sym in enumerate(atoms.get_chemical_symbols())
            if sym == host_element]


def find_host_indices_for_site(atoms: Atoms, site_name: str,
                               ps_cutoff: float = 2.7) -> list[int]:
    """Return indices matching host element AND specific Wyckoff site.

    Distinguishes the two crystallographically inequivalent S²⁻ environments
    in argyrodite Li6PS5Cl (cubic F-43m):

      * S_16e — bonded to P (P–S < ``ps_cutoff`` Å) → PS₄ tetrahedral S.
      * S_4a  — not bonded to P → free S²⁻ in the Li2S-like sublattice.

    For Li sites (Li_24g / Li_48h), Cl_4d, and P_4b, returns every host
    element atom: distinguishing Li 24g vs 48h reliably requires the
    Wyckoff metadata of the input file (not always available), and the
    other host sites have only one Wyckoff per element in this system.
    """
    host = SITE_TO_HOST[site_name]
    host_idx = [i for i, sym in enumerate(atoms.get_chemical_symbols())
                if sym == host]
    if site_name not in ('S_16e', 'S_4a'):
        return host_idx
    p_idx = [i for i, sym in enumerate(atoms.get_chemical_symbols())
             if sym == 'P']
    if not p_idx:
        return host_idx
    from ase.geometry import get_distances
    s_pos = atoms.get_positions()[host_idx]
    p_pos = atoms.get_positions()[p_idx]
    _, dists = get_distances(s_pos, p_pos,
                             cell=atoms.cell.array, pbc=atoms.pbc)
    bonded = (dists < ps_cutoff).any(axis=1)
    if site_name == 'S_16e':
        return [host_idx[i] for i, b in enumerate(bonded) if b]
    return [host_idx[i] for i, b in enumerate(bonded) if not b]


def select_substitution_sites(host_indices: list[int], n_sub: int,
                              method: str = 'first', seed: int = 42,
                              atoms: Atoms | None = None,
                              reference_indices: list[int] | None = None,
                              cluster_radius: float = 4.0) -> list[int]:
    """Pick n_sub indices to substitute. Selection strategy via ``method``:

      'first':  lowest indices (truly deterministic — same atoms regardless
                of seed). For reproducibility tests / ablation only.
      'random': uniform random subset; SEED-REPRODUCIBLE (same ``seed``
                gives same output, but different seeds give different
                outputs — this is the only mode that varies across seeds).
      'spread': PBC-aware farthest-point sampling. SEED-REPRODUCIBLE
                with random initial seed atom — different ``seed``
                values give different starting points (so the resulting
                set varies seed-to-seed even though selection is greedy
                deterministic afterwards). Models a homogeneous solid
                solution from extensive ball milling (Yu 2022, Kraft 2017).
                Requires ``atoms`` for PBC distance calc.
      'cluster': greedy chain growth — pick a seed atom (random per seed)
                and at each step add the host atom NEAREST to the already-
                chosen set. NOT a true radius-based cluster: this is
                'chain' clustering, where the selection extends through
                successive nearest neighbours. May leave the seed PS4 and
                hop into adjacent PS4 if those S atoms are closer to the
                last pick than the remaining same-PS4 S atoms. The mean
                pair distance ≈ PS4 S-S edge (~3.4 Å) on canonical LPSCl
                because the F-43m geometry happens to place inter-PS4 S
                farther than intra-PS4 S, but for distorted geometries
                this approximation breaks down.

    ``atoms`` must be supplied for 'spread' / 'cluster' so PBC distances
    can be computed (MIC = minimum image convention).
    """
    if n_sub >= len(host_indices):
        return host_indices
    if method == 'first':
        return host_indices[:n_sub]
    if method == 'random':
        rng = np.random.default_rng(seed)
        return sorted(rng.choice(host_indices, size=n_sub, replace=False).tolist())

    if method in ('spread', 'cluster'):
        if atoms is None:
            step = max(1, len(host_indices) // n_sub)
            return [host_indices[i * step] for i in range(n_sub)]
        rng = np.random.default_rng(seed)
        D_full = atoms.get_all_distances(mic=True)
        D = D_full[np.ix_(host_indices, host_indices)]
        chosen_local = [int(rng.integers(0, len(host_indices)))]
        for _ in range(n_sub - 1):
            min_d_to_chosen = D[:, chosen_local].min(axis=1)
            min_d_to_chosen[chosen_local] = -np.inf if method == 'spread' else np.inf
            if method == 'spread':
                next_local = int(np.argmax(min_d_to_chosen))
            else:  # cluster (chain — nearest to already chosen)
                next_local = int(np.argmin(min_d_to_chosen))
            chosen_local.append(next_local)
        return sorted(host_indices[i] for i in chosen_local)

    if method == 'near_cation':
        # Bias selection toward host atoms close to reference_indices (the
        # aliovalent cation positions). Models local charge compensation:
        # Li vacancy forms preferentially near a Mg²⁺/Al³⁺/Nd³⁺ dopant to
        # minimize Madelung energy of the defect pair.
        if atoms is None or not reference_indices:
            # Fallback to random when no reference available
            rng = np.random.default_rng(seed)
            return sorted(rng.choice(host_indices, size=n_sub,
                                    replace=False).tolist())
        D_full = atoms.get_all_distances(mic=True)
        # For each host_idx, distance to nearest reference atom
        min_d_to_ref = D_full[np.ix_(host_indices, reference_indices)].min(axis=1)
        # Probability weight ∝ exp(-d/cutoff) — exponential decay matches
        # Coulomb 1/r decay roughly while keeping things normalized.
        rng = np.random.default_rng(seed)
        weights = np.exp(-min_d_to_ref / cluster_radius)
        weights = weights / weights.sum()
        picks = rng.choice(len(host_indices), size=n_sub, replace=False,
                          p=weights)
        return sorted(host_indices[i] for i in picks)

    raise ValueError(f"Unknown selection method: {method!r}")


def substitute(atoms: Atoms, dopant: str, host_element: str,
               n_sub: int, method: str = 'spread', seed: int = 42,
               site_name: str | None = None) -> Atoms:
    """Replace n_sub host atoms with dopant atoms.

    If ``site_name`` is given (e.g., 'S_16e'), restrict the substitution to
    that specific Wyckoff site via :func:`find_host_indices_for_site`.
    Otherwise fall back to the chemical-element-only filter (legacy).
    """
    new = atoms.copy()
    if site_name is not None:
        host_idx = find_host_indices_for_site(new, site_name)
        if not host_idx:
            raise ValueError(
                f"No atoms at Wyckoff site {site_name} (host {host_element})")
    else:
        host_idx = find_host_indices(new, host_element)
        if not host_idx:
            raise ValueError(f"No {host_element} atoms in structure")
    targets = select_substitution_sites(host_idx, n_sub, method, seed=seed,
                                        atoms=new)
    syms = new.get_chemical_symbols()
    for i in targets:
        syms[i] = dopant
    new.set_chemical_symbols(syms)
    return new, targets


def add_li_vacancy(atoms: Atoms, n_vac: int = 1, method: str = 'spread',
                   seed: int = 42) -> Atoms:
    """Remove n_vac Li atoms (for donor charge compensation)."""
    li_idx = find_host_indices(atoms, 'Li')
    if n_vac >= len(li_idx):
        raise ValueError(f"Cannot remove {n_vac} Li from {len(li_idx)} atoms")
    # Use seed+1 so vacancy != substitution sites for the same nominal seed
    targets = select_substitution_sites(li_idx, n_vac, method, seed=seed + 1,
                                        atoms=atoms)
    keep = [i for i in range(len(atoms)) if i not in targets]
    return atoms[keep]


def apply_charge_compensation(atoms: Atoms, host_charge: int,
                              dopant_charge: int, n_dopants: int,
                              vacancy_method: str = 'spread',
                              seed: int = 42) -> Atoms:
    """Apply automatic charge compensation."""
    delta_q = (dopant_charge - host_charge) * n_dopants
    if delta_q == 0:
        return atoms, 'isovalent'
    elif delta_q > 0:
        # Donor: remove Li (each removal = +1 charge correction)
        return add_li_vacancy(atoms, n_vac=delta_q, method=vacancy_method,
                              seed=seed), f'Li_vac_{delta_q}'
    else:
        # Acceptor: simplest = add Li interstitial. For now, leave imbalanced
        # with note. (Proper treatment needs Li interstitial site finding.)
        return atoms, f'imbalanced_{delta_q}'


def generate_for_dopant(base_atoms: Atoms, dopant_entry: dict,
                       concentrations: list[float], out_dir: Path,
                       dopant_db: dict, method: str = 'spread',
                       n_seeds: int = 1, base_seed: int = 42,
                       polymorph: str = 'unknown',
                       li_ordering: str = 'unknown') -> list[dict]:
    """Generate structures for one dopant across all sites + concentrations.

    method: 'spread' (deterministic, default) or 'random' (paired with n_seeds).
    n_seeds: number of independent seeds when method='random' — required to build
        a Li-ordering ensemble that lets downstream UMA screening report mean±std
        of B0/E (Pustorino 2025, D'Amore 2022).
    polymorph / li_ordering: metadata stamped on every generated record so the
        downstream pipeline can group results by baseline polymorph/ordering.
    """
    element = dopant_entry['element']
    if element not in dopant_db:
        return []
    d_info = dopant_db[element]

    seeds = ([base_seed] if method != 'random'
             else [base_seed + i for i in range(n_seeds)])

    generated = []
    for site_info in dopant_entry.get('compatible_sites', []):
        site = site_info['site_name']
        host = SITE_TO_HOST[site]
        host_indices = find_host_indices_for_site(base_atoms, site)
        n_host = len(host_indices)
        if n_host == 0:
            print(f"  ⚠ {element} on {site}: 0 atoms at this Wyckoff site, "
                  f"skipping all concentrations")
            continue

        for conc in concentrations:
            n_sub = max(1, int(round(n_host * conc)))
            actual_conc = n_sub / n_host
            for seed in seeds:
                try:
                    doped, sub_idx = substitute(base_atoms, element, host,
                                                n_sub, method=method, seed=seed,
                                                site_name=site)
                    doped, comp_label = apply_charge_compensation(
                        doped, site_info['host_charge'], d_info['charge'],
                        n_sub, vacancy_method=method, seed=seed)

                    base_name = (f"{element}_{site}_x{int(actual_conc*1000):03d}"
                                 f"_{comp_label}")
                    name = (base_name if method != 'random'
                            else f"{base_name}_s{seed - base_seed:02d}")
                    xyz_path = out_dir / f'{name}.xyz'
                    write(xyz_path, doped)

                    generated.append({
                        'name': name,
                        'dopant': element,
                        'host': host,
                        'site': site,
                        'concentration': actual_conc,
                        'n_sub': n_sub,
                        'charge_compensation': comp_label,
                        'compatibility_score': site_info['compatibility_score'],
                        'n_atoms': len(doped),
                        'composition': dict(zip(*np.unique(
                            doped.get_chemical_symbols(), return_counts=True))),
                        'xyz_file': str(xyz_path),
                        'polymorph': polymorph,
                        'li_ordering': li_ordering,
                        'selection_method': method,
                        'seed': seed,
                    })
                except Exception as e:
                    print(f"  ❌ {element} on {site} conc={conc:.2f} "
                          f"seed={seed}: {e}")
    return generated



def permute_dopant(atoms, dopant: str, host: str, seed: int):
    """이미 도핑된 구조에서 **도판트를 같은 원소의 다른 자리로 옮긴다**.

    왜 이게 필요한가 (2026-08-26, Y 자리선호):
      배치 하나로 낸 E_above_hull 여유(27.6 meV/atom)가 MLIP 정확도와 같은 자릿수라
      "그 여유가 배치 산포보다 큰가" 를 물어야 한다. base 에서 다시 만들면 전하보상
      배치까지 같이 바뀌어 변수가 둘이 된다. **조성을 정확히 보존한 채 도판트 위치만**
      바꾸려면 도판트와 같은 원소 원자의 기호를 맞바꾸는 것이 가장 깨끗하다.

    ⛔ 못 하는 것
      · 공공(vacancy) 위치는 그대로 둔다 — 즉 Y–vacancy 거리는 따라 변한다.
        그것도 배치 자유도의 일부이므로 의도된 것이지만, '공공 배치 산포' 를
        따로 잰 것은 아니다.
      · 대칭 동등성을 판정하지 않는다. 같은 자리를 두 번 뽑을 수 있다 —
        중복은 호출부가 에너지로 걸러라(같은 값이 나온다).
    """
    import random
    sym = atoms.get_chemical_symbols()
    dop_idx = [i for i, s in enumerate(sym) if s == dopant]
    host_idx = [i for i, s in enumerate(sym) if s == host]
    if not dop_idx:
        raise SystemExit(f"⛔ 구조에 {dopant} 가 없다")
    if len(host_idx) < len(dop_idx):
        raise SystemExit(f"⛔ {host} 자리가 {len(host_idx)}개뿐이라 "
                         f"{dopant} {len(dop_idx)}개를 옮길 수 없다")
    # ★ 2026-08-26 수정 — **합집합에서 다시 고른다.**
    #   초판은 도판트 전부를 host 원자와 1:1 로 맞바꿨다. 그러면 '하나만 옮기기'(부분 이동)가
    #   불가능하다. host 자리가 많은 큰 셀에서는 티가 안 나지만, 작은 셀에서는 치명적이다:
    #   P_4b(56at)은 P 2개 · Y 2개라 실제 배치 공간이 C(4,2)=6 인데 초판 방식은 1가지만 낸다.
    #   올바른 모형은 "동등한 자리 전체에서 도판트가 앉을 자리를 다시 고른다" 이다.
    pool = sorted(dop_idx + host_idx)
    rng = random.Random(seed)
    picks = sorted(rng.sample(pool, len(dop_idx)))
    new = atoms.copy()
    s2 = list(sym)
    for i in pool:
        s2[i] = host                          # 일단 전부 host 로
    for i in picks:
        s2[i] = dopant                        # 고른 자리에만 도판트
    new.set_chemical_symbols(s2)
    moved = sum(1 for a, b in zip(sym, s2) if a != b)
    import math
    return new, {"seed": seed, "from": sorted(dop_idx), "to": picks,
                 "n_changed": moved,
                 "n_pool": len(pool),
                 "n_possible": math.comb(len(pool), len(dop_idx)),
                 "same_as_input": picks == sorted(dop_idx)}


def _selftest_permute():
    """permute_dopant 만 검증 (음성 포함)."""
    from ase import Atoms
    n_ok = n_bad = 0

    def chk(c, m):
        nonlocal n_ok, n_bad
        print(("  ✓ " if c else "  ✗ ") + m)
        n_ok, n_bad = n_ok + bool(c), n_bad + (not c)

    import collections
    a = Atoms("Y2Li6S2", positions=[[i, 0, 0] for i in range(10)], cell=[20, 20, 20], pbc=True)
    b, meta = permute_dopant(a, "Y", "Li", seed=1)
    chk(collections.Counter(b.get_chemical_symbols()) ==
        collections.Counter(a.get_chemical_symbols()),
        "★ 조성이 정확히 보존된다 (hull 비교가 성립하려면 필수)")
    chk(b.get_chemical_symbols() != a.get_chemical_symbols(),
        "Y 가 실제로 다른 자리로 간다")
    chk(sum(1 for s in b.get_chemical_symbols() if s == "Y") == 2,
        "도판트 개수 불변")
    b2, _ = permute_dopant(a, "Y", "Li", seed=1)
    chk(b2.get_chemical_symbols() == b.get_chemical_symbols(),
        "같은 seed 는 같은 결과 (재현 가능)")
    b3, _ = permute_dopant(a, "Y", "Li", seed=99)
    chk(b3.get_chemical_symbols() != b.get_chemical_symbols(),
        "다른 seed 는 다른 배치 (seed 가 실제로 먹는다)")
    chk(all(s != "S" for i, s in enumerate(b.get_chemical_symbols())
            if a.get_chemical_symbols()[i] == "Y"),
        "[음성] 지정한 host 원소(Li)로만 옮긴다 — S 로 가지 않는다")
    try:
        permute_dopant(a, "Zr", "Li", seed=1)
        chk(False, "[음성] 없는 도판트는 거부해야 한다")
    except SystemExit:
        chk(True, "[음성] 구조에 없는 도판트는 거부한다")
    try:
        permute_dopant(a, "Y", "S", seed=1)   # S 2개, Y 2개 → 가능
        ok = True
    except SystemExit:
        ok = False
    chk(ok, "host 자리 수가 딱 맞으면 통과")
    try:
        permute_dopant(Atoms("Y3Li1", positions=[[i, 0, 0] for i in range(4)],
                             cell=[9, 9, 9], pbc=True), "Y", "Li", seed=1)
        chk(False, "[음성] host 자리가 모자라면 거부해야 한다")
    except SystemExit:
        chk(True, "[음성] host 자리가 모자라면 거부한다 (조용히 일부만 옮기지 않는다)")

    # ★ 작은 셀: 부분 이동이 되나 (2026-08-26 수정의 핵심)
    small = Atoms("Y2P2S4", positions=[[i, 0, 0] for i in range(8)],
                  cell=[20, 20, 20], pbc=True)
    seen = set()
    for s in range(40):
        b, m = permute_dopant(small, "Y", "P", seed=s)
        seen.add(tuple(i for i, x in enumerate(b.get_chemical_symbols()) if x == "Y"))
        chk_pool = m["n_pool"]
    chk(chk_pool == 4 and m["n_possible"] == 6,
        "작은 셀: 풀 = 도판트+host 4자리, 가능 배치 C(4,2)=6 으로 센다")
    chk(len(seen) == 6,
        "★ [음성] Y2P2 에서 **6가지 배치를 전부** 낸다 — 초판은 1가지밖에 못 냈다")
    chk(any(len(set(x) & {0, 1}) == 1 for x in seen),
        "★ [음성] **부분 이동**(Y 하나만 옮기기)이 실제로 나온다")
    import collections as _c
    chk(all(_c.Counter(permute_dopant(small, "Y", "P", seed=s)[0]
            .get_chemical_symbols()) ==
            _c.Counter(small.get_chemical_symbols()) for s in range(10)),
        "작은 셀에서도 조성 보존")
    print(f"selftest {'PASS' if not n_bad else 'FAIL'} — {n_ok} ok, {n_bad} bad")
    return 1 if n_bad else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--base',
                       help='LPSCl base structure (cif/xyz/POSCAR)')
    parser.add_argument('--permute_dopant', metavar='DOPANT',
                       help='이미 도핑된 구조에서 **도판트만 같은 원소의 다른 자리로** '
                            '옮겨 배치 앙상블을 만든다 (--base 를 입력 구조로 쓴다). '
                            '조성이 정확히 보존되므로 E_above_hull 비교가 그대로 성립한다. '
                            '--host_element 와 --n_seeds 를 같이 준다.')
    parser.add_argument('--host_element',
                       help='--permute_dopant 가 옮겨갈 자리의 원소 (Li_24g→Li, P_4b→P)')
    parser.add_argument('--selftest', action='store_true',
                       help='permute_dopant 로직만 검증 (음성 경로 포함)')
    parser.add_argument('--site_pref', help='site_preference_initial.json')
    parser.add_argument('--dopant', help='Single dopant (e.g., Mg)')
    parser.add_argument('--site', help='Single site (e.g., Li_24g)')
    parser.add_argument('--conc', type=float, help='Single concentration')
    parser.add_argument('--concentrations', nargs='+', type=float,
                       default=[0.05, 0.10, 0.20],
                       help='Concentration list (mole fraction)')
    parser.add_argument('--out', help='Output directory')
    parser.add_argument('--polymorph', default='unknown',
                       choices=['unknown', 'cubic_F-43m', 'pseudo_cubic_P1',
                                'monoclinic_Pm'],
                       help='Baseline polymorph label (metadata only — pass the '
                            'matching --base file). See '
                            'kb/literature_db/damore_2022_lpscl_symmetry_breaking_qha.md.')
    parser.add_argument('--li_ordering', default='unknown',
                       choices=['unknown', '24G', '48H', '48HR', '48HR_inv',
                                '48H_low'],
                       help='Baseline Li ordering label (metadata only — pass the '
                            'matching --base file). See '
                            'kb/literature_db/pustorino_2025_lpscl_li_ordering_mechanical.md.')
    parser.add_argument('--method', default='spread',
                       choices=['spread', 'random', 'first'],
                       help="Substitution-site selection: 'spread' (deterministic, "
                            "default) or 'random' (use with --n_seeds for ensemble).")
    parser.add_argument('--n_seeds', type=int, default=1,
                       help='Number of random seeds per (dopant, site, conc) when '
                            "--method=random. Enables Li-ordering ensemble for "
                            'mean±std B0/E (Pustorino 2025: ~16 GPa B0 spread).')
    parser.add_argument('--seed', type=int, default=42,
                       help='Base RNG seed (used directly when --method!=random).')
    args = parser.parse_args()

    if args.selftest:
        return _selftest_permute()

    if args.permute_dopant:
        if not (args.base and args.host_element and args.out):
            print("⛔ --permute_dopant 는 --base --host_element --out 이 필요하다")
            return 2
        src = read(args.base)
        od = Path(args.out); od.mkdir(parents=True, exist_ok=True)
        stem = Path(args.base).stem
        meta_all, n_same, n_dup, seen = [], 0, 0, set()
        for k in range(args.n_seeds):
            new, meta = permute_dopant(src, args.permute_dopant,
                                       args.host_element, seed=args.seed + k)
            key = tuple(meta["to"])
            dup = key in seen
            seen.add(key)
            if meta["same_as_input"]:
                n_same += 1
            if dup:
                n_dup += 1
            f = od / f"{stem}_perm{k:02d}.xyz"
            write(f, new)
            meta_all.append({**meta, "file": f.name, "duplicate": dup})
            flags = ("   ⚠ 입력과 같은 자리" if meta["same_as_input"] else "") + \
                    ("   ⚠ 앞 배치와 중복" if dup else "")
            print(f"  [{k}] seed {args.seed+k} → {f.name}  "
                  f"{args.permute_dopant} {meta['from']} → {meta['to']}{flags}")
        # ⛔ 배치 공간이 좁으면 seed 를 늘려도 새 배치가 안 나온다. 그걸 말해준다 —
        #   중복을 독립 표본으로 세면 산포가 실제보다 작아 보인다.
        n_poss = meta_all[0]["n_possible"] if meta_all else 0
        if args.n_seeds >= n_poss:
            print(f"  ⚠⚠ 가능한 배치가 **{n_poss}가지뿐**인데 {args.n_seeds}개를 뽑았다 "
                  f"(고유 {len(seen)}가지). 중복을 독립 표본으로 세면 산포가 "
                  f"실제보다 작게 나온다 — 통계에 쓸 때는 고유 배치만 센다.")
        (od / f"{stem}_permute_meta.json").write_text(json.dumps({
            "source": str(args.base), "dopant": args.permute_dopant,
            "host_element": args.host_element, "n_seeds": args.n_seeds,
            "base_seed": args.seed, "configs": meta_all,
            "n_identical_to_input": n_same,
            "n_duplicate": n_dup, "n_unique": len(seen),
            "n_possible": (meta_all[0]["n_possible"] if meta_all else None),
            "⛔_note": "조성은 정확히 보존된다. 공공 위치는 그대로이므로 "
                       "도판트-공공 거리는 배치마다 달라진다 (의도된 자유도).",
        }, indent=2, ensure_ascii=False))
        print(f"✓ {args.n_seeds}개 배치 → {od}  (고유 {len(seen)} / 가능 {n_poss})"
              + (f"   ⚠ 입력과 같은 자리 {n_same}개" if n_same else "")
              + (f"   ⚠ 중복 {n_dup}개" if n_dup else ""))
        return 0

    if not args.base or not args.out:
        print("⛔ --base 와 --out 이 필요하다")
        return 2

    if args.method == 'random' and args.n_seeds < 2:
        print("⚠ --method=random with --n_seeds=1 gives a single configuration "
              "(no ensemble). Set --n_seeds≥3 for B0/E mean±std.")
    if args.polymorph == 'unknown' or args.li_ordering == 'unknown':
        print("⚠ Baseline polymorph or Li ordering is 'unknown'. Recommended: "
              "--polymorph monoclinic_Pm --li_ordering 48HR (ground state). "
              "mp-985592 is metastable cubic_F-43m / 24G.")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading LPSCl base from: {args.base}")
    base = read(args.base)
    print(f"  base: {len(base)} atoms, "
          f"composition: {dict(zip(*np.unique(base.get_chemical_symbols(), return_counts=True)))}")
    print(f"  polymorph={args.polymorph}, li_ordering={args.li_ordering}, "
          f"method={args.method}, n_seeds={args.n_seeds}")

    # Load DOPANT_DB from site_preference module
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from site_preference import DOPANT_DB

    common_kw = dict(method=args.method, n_seeds=args.n_seeds,
                     base_seed=args.seed, polymorph=args.polymorph,
                     li_ordering=args.li_ordering)

    if args.site_pref:
        site_pref_data = json.loads(Path(args.site_pref).read_text())
        all_generated = []
        for entry in site_pref_data:
            gens = generate_for_dopant(base, entry, args.concentrations,
                                      out_dir, DOPANT_DB, **common_kw)
            all_generated.extend(gens)
            print(f"  {entry['element']}: {len(gens)} structures")
    elif args.dopant and args.site and args.conc:
        # Single mode
        d_info = DOPANT_DB[args.dopant]
        host = SITE_TO_HOST[args.site]
        n_host = len(find_host_indices_for_site(base, args.site))
        n_sub = max(1, int(round(n_host * args.conc)))
        from site_preference import HOST_SITES
        site_info = {**HOST_SITES[args.site], 'site_name': args.site,
                    'host_charge': HOST_SITES[args.site]['charge']}
        entry = {'element': args.dopant, 'compatible_sites': [{
            **site_info, 'compatibility_score': 1.0,
        }]}
        all_generated = generate_for_dopant(base, entry, [args.conc],
                                           out_dir, DOPANT_DB, **common_kw)
    else:
        parser.error("Provide --site_pref OR (--dopant --site --conc)")

    summary_path = out_dir / 'structures_summary.json'
    summary_path.write_text(json.dumps({
        'provenance': get_provenance(),  # v4.5.13 NEW-1 fix
        'baseline': {
            'base_file': args.base,
            'polymorph': args.polymorph,
            'li_ordering': args.li_ordering,
            'selection_method': args.method,
            'n_seeds': args.n_seeds,
            'base_seed': args.seed,
        },
        'structures': all_generated,
    }, indent=2, default=str))
    print(f"\n✓ Generated {len(all_generated)} structures")
    print(f"✓ Summary: {summary_path}")


if __name__ == '__main__':
    sys.exit(main() or 0)
