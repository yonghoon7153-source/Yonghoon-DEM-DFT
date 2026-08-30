#!/usr/bin/env python
"""run_anneal.py — Pipeline Step 3: Li-selective thermal annealing.

Takes champion candidate structures from screening and runs MLIP MD at
500 K for tens of ps. At 500 K Li⁺ hops actively (Eₐ ≈ 0.2 eV << kT = 0.043
eV) while PS₄ framework (P-S ≈ 3.5 eV) and the Cl⁻ cage stay rigid — i.e.,
we re-optimize only the Li sublattice while keeping the anion arrangement
fixed (D'Amore 2022, Pustorino 2025 ordering ↔ B0 evidence).

After MD, a final UMA relax (FIRE) gives the post-anneal energy. Compare
to the pre-anneal energy from screening to see whether the deeper basin
shifted the candidate ranking — Pipeline doc cites a Li6PS5Cl example
where screening 4th → anneal 1st.

Usage:
  # Anneal a hand-picked list of xyz files (one per champion).
  python3 run_anneal.py \\
      --xyz path/to/Nd2O3_x050_s00.xyz path/to/La2O3_x050_s00.xyz ... \\
      --out runs/anneal_top5_2026_05_15/ \\
      --temperature 500 --time_ps 50

  # Or pull the top-N candidates straight from analyze_screening output.
  python3 run_anneal.py \\
      --top_candidates runs/.../top_candidates_v2.json \\
      --top 5 --out runs/anneal_top5_2026_05_15/
"""
import argparse
import json
import zlib
import sys
import time
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import FIRE
from ase import units

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance

try:
    from ase.filters import FrechetCellFilter as CellFilter
except ImportError:
    try:
        from ase.constraints import ExpCellFilter as CellFilter
    except ImportError:
        from ase.constraints import UnitCellFilter as CellFilter


def load_uma_calc(device: str = 'cuda', task: str = 'omat'):
    """Load UMA-s-1p1 calculator (FAIRChem)."""
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit('uma-s-1p1', device=device)
    return FAIRChemCalculator(predictor, task_name=task)


def _struct_hash(atoms) -> str:
    """구조의 **종 인식** 해시 — 원소 순서·좌표·셀을 다 담는다. 앞 16자만 쓴다.

    ⛔ 못 하는 것: 대칭 등가 구조를 같다고 하지 않는다 (좌표 그대로 본다) ·
       부동소수 표현에 민감하므로 **1e-6 Å 로 반올림**해서 잰다.
    """
    import hashlib
    import numpy as _np
    parts = [",".join(atoms.get_chemical_symbols()),
             _np.round(_np.asarray(atoms.get_positions()), 6).tobytes(),
             _np.round(_np.asarray(atoms.cell.array), 6).tobytes()]
    h = hashlib.sha256()
    for x in parts:
        h.update(x.encode() if isinstance(x, str) else x)
    return h.hexdigest()[:16]


def winner_name(xyz_path):
    """v4.5.18 NEW-D defensive fix: cascade outputs share stem
    'post_relax' or 'post_md' across winners. Use parent dir name in
    that case. Same pattern as bvse_proxy/run_mlip_postproc (v4.5.17)
    + combine_rankings.py CR-A (v4.5.8). Round 3 reviewer flagged this
    as 'conditional hole — safe in current cascade flow but manual
    re-anneal of post_relax.xyz would collide'. Defensive patch."""
    p = Path(xyz_path)
    if p.stem in ('post_relax', 'post_md'):
        return p.parent.name
    return p.stem


def anneal_one(xyz_path: Path, calc, out_dir: Path,
              temperature_K: float = 500, time_ps: float = 50,
              dt_fs: float = 2.0, friction: float = 0.01,
              relax_steps: int = 1500, relax_fmax: float = 0.05,
              cell_relax: bool = True, log_every: int = 500,
              seed: int = 0) -> dict:
    """Run Langevin NVT MD at ``temperature_K`` for ``time_ps``, then a final
    cell+positions relax. Records pre-anneal, post-MD, and post-relax energies
    so you can see how much extra binding the thermal sampling found.

    ⛔⛔ 2026-08-30 (회신 AL P0-3) — **이 함수는 seed 를 안 받았다.**
      `MaxwellBoltzmannDistribution` 과 `Langevin` 이 전역 numpy 상태를 쓰는데
      그걸 고정하지도 기록하지도 않아서, **같은 입력을 다시 돌리면 다른 endpoint** 로 갔다.
      정본 CSV 실측: 같은 설계의 복제본 삼중쌍 227개 중 anneal **후** 에너지가
      1e-4 안에서 일치하는 것이 **0개** (상대산포 중앙 6.0e-3 · 최대 2.8e-2).
      예 Ag2O: E_post = −4.1964 / −4.1888 / −4.1113 eV/atom, ΔV = −7.97 / −3.69 / −2.85 %.
      그 위에서 계산된 BVS·탄성 G 가 Pareto front 와 사전등록 순위를 정하고 있었다.
      ⇒ 이제 `seed` 를 **받아서 두 곳에 다 주입하고 결과에 기록한다.**

    ⛔ 이 함수가 못 하는 것
      · seed 를 고정해도 **비트 단위 재현을 보장하지 못한다** — GPU 커널 비결정성·
        ASE/torch 버전·장치가 바뀌면 달라진다. seed 는 재현의 **필요조건**이지 충분조건이 아니다.
      · 결과 구조가 물리적으로 옳은지 판정하지 않는다 (수렴 플래그만 낸다).
    """
    name = winner_name(xyz_path)
    work = out_dir / name
    work.mkdir(parents=True, exist_ok=True)

    atoms = read(str(xyz_path))
    atoms.calc = calc
    E_pre = float(atoms.get_potential_energy())
    n_atoms = len(atoms)

    # ⛔ seed 를 **두 곳 다** 준다 — 초기속도와 Langevin 잡음은 서로 다른 난수원이다.
    #   하나만 고정하면 여전히 비결정적이다 (회신 AL P0-3).
    rng_v = np.random.default_rng(seed)
    rng_md = np.random.default_rng(seed + 1_000_003)      # 서로 다른 스트림
    MaxwellBoltzmannDistribution(atoms, temperature_K=temperature_K, rng=rng_v)

    n_steps = int(time_ps * 1000 / dt_fs)
    print(f"  [{name}] MD: T={temperature_K}K, dt={dt_fs}fs, "
          f"steps={n_steps} ({time_ps}ps), {n_atoms} atoms")

    md_log = work / 'md.log'
    md_traj = work / 'md.traj'
    dyn = Langevin(atoms, dt_fs * units.fs,
                   temperature_K=temperature_K,
                   friction=friction,
                   logfile=str(md_log),
                   trajectory=str(md_traj),
                   rng=rng_md,
                   loginterval=log_every)

    t0 = time.time()
    dyn.run(n_steps)
    t_md = time.time() - t0
    E_md_final = float(atoms.get_potential_energy())
    print(f"  [{name}] MD done ({t_md:.1f}s) "
          f"E_pre={E_pre/n_atoms:.4f} → E_md={E_md_final/n_atoms:.4f} eV/atom")

    # Save post-MD snapshot
    write(work / 'post_md.xyz', atoms)

    # Final relax
    target = CellFilter(atoms) if cell_relax else atoms
    opt = FIRE(target, logfile=str(work / 'relax.log'))
    t0 = time.time()
    opt.run(fmax=relax_fmax, steps=relax_steps)
    t_relax = time.time() - t0
    n_relax_steps = opt.get_number_of_steps()
    converged = n_relax_steps < relax_steps
    E_post = float(atoms.get_potential_energy())
    write(work / 'post_relax.xyz', atoms)

    delta_E_per_atom = (E_post - E_pre) / n_atoms
    print(f"  [{name}] relax {n_relax_steps} steps ({t_relax:.1f}s) "
          f"E_post={E_post/n_atoms:.4f} eV/atom, "
          f"ΔE_anneal={delta_E_per_atom*1000:+.1f} meV/atom, "
          f"conv={converged}")

    return {
        'name': name,
        # ⛔ 계보 3종 — 이게 없으면 "같은 구조인가" 를 나중에 되물을 수 없다 (회신 AL P0-3)
        'seed': int(seed),
        'rng_streams': {'velocities': int(seed), 'langevin': int(seed) + 1_000_003},
        'struct_sha256': {
            'input': _struct_hash(read(str(xyz_path))),
            'post_md': _struct_hash(read(str(work / 'post_md.xyz'))),
            'post_relax': _struct_hash(atoms),
        },
        '⚠_재현': ('seed 고정은 재현의 **필요조건**이지 충분조건이 아니다 — GPU 커널 '
                   '비결정성·ASE/torch 버전·장치가 바뀌면 달라진다'),
        'xyz_input': str(xyz_path),
        'n_atoms': n_atoms,
        'temperature_K': temperature_K,
        'time_ps': time_ps,
        'dt_fs': dt_fs,
        'E_pre_anneal': E_pre,
        'E_md_final': E_md_final,
        'E_post_relax': E_post,
        'delta_E_anneal_meV_per_atom': delta_E_per_atom * 1000,
        'cell_pre': read(str(xyz_path)).cell.array.tolist(),
        'cell_post': atoms.cell.array.tolist(),
        'volume_pre': float(read(str(xyz_path)).get_volume()),
        'volume_post': float(atoms.get_volume()),
        't_md_s': t_md,
        't_relax_s': t_relax,
        'n_relax_steps': n_relax_steps,
        'converged': converged,
        'post_md_xyz': str(work / 'post_md.xyz'),
        'post_relax_xyz': str(work / 'post_relax.xyz'),
    }



def _selftest() -> int:
    """seed 배관 검사 — **음성 경로가 핵심**이다 (양성만 있으면 아무것도 보증 못 한다)."""
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    import inspect
    src = inspect.getsource(anneal_one)
    chk("rng=rng_v" in src,
        "① 초기속도(MaxwellBoltzmann)에 rng 를 준다")
    chk("rng=rng_md" in src,
        "① Langevin 에도 rng 를 준다 (하나만 고정하면 여전히 비결정적)")
    chk(src.count("default_rng") == 2,
        "① 두 난수원이 **서로 다른 스트림**이다")
    chk("'seed': int(seed)" in src and "struct_sha256" in src,
        "② seed 와 구조 해시 3종(input·post_md·post_relax)을 결과에 남긴다")
    # ⛔음성 — seed 는 required 다. 안 주면 argparse 가 거부해야 한다.
    import subprocess
    r = subprocess.run([sys.executable, __file__, "--help"],
                       capture_output=True, text=True)
    chk("--seed" in r.stdout and "필수" in r.stdout,
        "⛔음성: --seed 가 **필수**로 노출된다 (기본값을 두면 안 준 것과 구분이 안 된다)")

    # ③ 구조 해시 — 좌표가 1e-6 넘게 다르면 갈라져야 하고, 그 아래면 같아야 한다
    class _A:
        def __init__(self, pos, sym=("Li", "Ni")):
            self._p, self._s = pos, list(sym)
            self.cell = type("C", (), {"array": [[5, 0, 0], [0, 5, 0], [0, 0, 5]]})()

        def get_chemical_symbols(self): return self._s
        def get_positions(self): return self._p

    a = _A([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    b = _A([[0.0, 0.0, 0.0], [1.0 + 1e-9, 0.0, 0.0]])
    c = _A([[0.0, 0.0, 0.0], [1.001, 0.0, 0.0]])
    d = _A([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], sym=("Ni", "Li"))
    chk(_struct_hash(a) == _struct_hash(b),
        "③ 1e-6 Å 아래 차이는 같은 구조로 본다 (부동소수 잡음에 안 흔들린다)")
    chk(_struct_hash(a) != _struct_hash(c),
        "③ [음성] 0.001 Å 차이는 다른 구조다")
    chk(_struct_hash(a) != _struct_hash(d),
        "③ [음성] **종 순서가 다르면 다른 구조다** (좌표만 보면 놓친다)")
    print("  " + ("✅ selftest 통과" if ok[1] == ok[0] else
                  f"⛔ selftest 실패 {ok[0]-ok[1]}/{ok[0]}"))
    return 0 if ok[1] == ok[0] else 1


def main():
    # ⚠ `--selftest` 는 parse_args() **앞에서** 가로챈다 — `--out`/`--seed` 가 required 라
    #   그대로 두면 selftest 를 돌릴 수 없다 (watch_all.py 가 `-h` 로 똑같이 걸렸다).
    if "--selftest" in sys.argv[1:]:
        return _selftest()

    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--xyz', nargs='+',
                       help='xyz files to anneal (one or more)')
    parser.add_argument('--xyz_dir',
                       help='Directory of xyz files to anneal — recursive '
                            'glob "**/*.xyz". Use for "anneal ALL screening '
                            'candidates" mode since UMA pre-anneal ranking is '
                            'a heuristic and Pipeline Step 3 docs note '
                            'screening can re-order under anneal.')
    parser.add_argument('--summary_json',
                       help='Structures summary JSON (substitute_compound '
                            "output); pulls xyz_file from each entry's "
                            "'xyz_file' field. Alternative to --xyz_dir for "
                            'a specific batch.')
    parser.add_argument('--top_candidates',
                       help='analyze_screening top_candidates JSON; pulls '
                            'xyz_file path from each record')
    parser.add_argument('--top', type=int, default=5,
                       help='If --top_candidates: number of top entries to anneal')
    parser.add_argument('--per_compound_top', type=int, default=None,
                       help='Per-compound stratified Top-N anneal: groups the '
                            'input (from --summary_json or --uma_results) by '
                            "dopant, anneals the lowest-ΔE/atom N entries of "
                            "each group. Recommended for compound batches "
                            "where ranking is heavy-tailed (one strong cation "
                            "family dominates the global Top-N otherwise).")
    parser.add_argument('--uma_results',
                       help='UMA screening results JSON (has uma_relaxed.'
                            'de_per_atom_vs_baseline per record). Used as '
                            'sort key when --per_compound_top is set.')
    parser.add_argument('--light', action='store_true',
                       help='Light anneal preset (300K, 20 ps, 500 relax '
                            'steps) — for stratified per-compound Top-N to '
                            'cheaply relieve unphysical Li placement before '
                            'reranking. Override individual flags as needed.')
    parser.add_argument('--out', required=True, help='Output base directory')
    parser.add_argument('--temperature', type=float, default=500,
                       help='Annealing temperature in K (default 500; pipeline '
                            'doc cites Li hop Eₐ~0.2 eV, kT@500K=0.043 eV; '
                            'avoid >800K — Cl cage starts to break)')
    parser.add_argument('--time_ps', type=float, default=50,
                       help='MD duration in ps (default 50; 25 ps minimum '
                            'for Li sub-lattice equilibration)')
    parser.add_argument('--dt_fs', type=float, default=2.0,
                       help='MD time step in fs')
    parser.add_argument('--friction', type=float, default=0.01,
                       help='Langevin friction (ase units)')
    parser.add_argument('--relax_steps', type=int, default=1500,
                       help='Post-MD FIRE max steps (default 1500 to match '
                            'compound-substitution screening)')
    parser.add_argument('--relax_fmax', type=float, default=0.05)
    parser.add_argument('--no_cell_relax', action='store_true',
                       help='Position-only final relax (fix cell)')
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--task', default='omat')
    parser.add_argument('--log_every', type=int, default=500,
                       help='MD log interval (steps)')
    # ⛔ 회신 AL P0-3 — seed 는 **필수**다. 기본값을 두면 안 준 것과 준 것이 구분 안 되고,
    #   정본 CSV 가 정확히 그 상태(seed 미기록)라 복제본이 서로 다른 endpoint 로 갔다.
    parser.add_argument('--seed', type=int, required=True,
                       help='Langevin·초기속도 RNG seed. **필수** — 이게 없으면 '
                            'anneal 이 비결정적이라 같은 입력이 다른 endpoint 로 간다 '
                            '(2026-08-30 회신 AL P0-3). 결과 json 에 기록된다.')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()

    if not args.xyz and not args.top_candidates and not args.summary_json and not args.xyz_dir:
        parser.error("Provide --xyz files, --xyz_dir, --top_candidates, or --summary_json JSON")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # Build xyz list (multiple input modes)
    if args.xyz:
        xyz_paths = [Path(p) for p in args.xyz]
    elif args.xyz_dir:
        xyz_paths = sorted(Path(args.xyz_dir).rglob('*.xyz'))
        # Filter out anneal-produced (post_md.xyz, post_relax.xyz) to avoid
        # re-annealing our own outputs if --xyz_dir overlaps --out
        xyz_paths = [p for p in xyz_paths
                     if p.name not in ('post_md.xyz', 'post_relax.xyz')]
        print(f"  Discovered {len(xyz_paths)} xyz files under {args.xyz_dir}")
    elif args.summary_json:
        data = json.loads(Path(args.summary_json).read_text())
        # Accept the key conventions used by upstream tools:
        #   substitute_compound output → {'structures': [...]}
        #   run_uma_screening output   → {'results':    [...]}
        #   select_winners output      → {'winners':    [...]}  (cascade Stage 03)
        recs = (data.get('winners')
                or data.get('structures')
                or data.get('results', [])
                if isinstance(data, dict) else data)
        xyz_paths = [Path(r['xyz_file']) for r in recs
                     if 'xyz_file' in r and Path(r['xyz_file']).exists()]
        print(f"  Loaded {len(xyz_paths)} xyz from summary {args.summary_json}")
    elif args.top_candidates:
        data = json.loads(Path(args.top_candidates).read_text())
        top = data.get('top_candidates', [])[:args.top]
        xyz_paths = []
        for entry in top:
            xpath = entry.get('xyz_file')
            if xpath and Path(xpath).exists():
                xyz_paths.append(Path(xpath))
            else:
                print(f"  ⚠ skip {entry.get('name')}: xyz_file not found "
                      f"({xpath})")
    else:
        parser.error("Provide --xyz, --xyz_dir, --summary_json, or --top_candidates")
    if not xyz_paths:
        raise SystemExit("No xyz files found")

    # Per-compound stratified Top-N filter
    if args.per_compound_top:
        if not args.uma_results:
            parser.error("--per_compound_top requires --uma_results "
                        "(needs ΔE/atom for ranking within each dopant group)")
        uma = json.loads(Path(args.uma_results).read_text())['results']
        # Map xyz path → ΔE/atom + dopant
        name_to_xpath = {winner_name(p): p for p in xyz_paths}
        from collections import defaultdict
        groups = defaultdict(list)
        for rec in uma:
            name = rec.get('name')
            if name in name_to_xpath:
                groups[rec.get('dopant', 'unknown')].append((
                    rec['uma_relaxed']['de_per_atom_vs_baseline'],
                    name_to_xpath[name],
                ))
        filtered: list = []
        for dop, items in groups.items():
            items.sort()  # ascending ΔE → most stable first
            keep = items[:args.per_compound_top]
            filtered.extend(p for _, p in keep)
            print(f"  per-compound Top-{args.per_compound_top}: {dop} → "
                  f"{len(keep)}/{len(items)}")
        xyz_paths = filtered
        print(f"  Stratified Top-{args.per_compound_top}: "
              f"{len(xyz_paths)} structures across {len(groups)} dopants")

    # --light preset
    if args.light:
        args.temperature = min(args.temperature, 300)
        args.time_ps = min(args.time_ps, 20)
        args.relax_steps = min(args.relax_steps, 500)
        print(f"  --light preset: T={args.temperature}K, "
              f"t={args.time_ps}ps, relax steps={args.relax_steps}")

    print(f"Loading UMA-s-1p1 ({args.device})...")
    calc = load_uma_calc(args.device, args.task)

    # Existing results (resume support)
    results_path = out / 'anneal_results.json'
    done = {}
    if results_path.exists():
        existing = json.loads(results_path.read_text())
        done = {r['name']: r for r in existing.get('results', [])}
        print(f"Resume: {len(done)} already annealed")

    todo = [p for p in xyz_paths if winner_name(p) not in done]
    print(f"To process: {len(todo)}/{len(xyz_paths)}")

    results = list(done.values())
    t_start = time.time()
    for i, p in enumerate(todo):
        print(f"\n[{i+1}/{len(todo)}] {winner_name(p)}")
        try:
            rec = anneal_one(
                p, calc, out,
                temperature_K=args.temperature,
                time_ps=args.time_ps,
                dt_fs=args.dt_fs,
                friction=args.friction,
                relax_steps=args.relax_steps,
                relax_fmax=args.relax_fmax,
                cell_relax=not args.no_cell_relax,
                log_every=args.log_every,
                # ⛔ 구조마다 **다른** seed 를 쓰되 이름에서 결정론적으로 유도한다
                #   (같은 구조를 다시 돌리면 같은 seed → 같은 궤적).
                #   전부 같은 seed 를 쓰면 서로 다른 계가 같은 잡음을 공유한다.
                seed=args.seed + (zlib.crc32(winner_name(p).encode()) & 0xFFFF),
            )
            results.append(rec)
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            results.append({'name': winner_name(p), 'xyz_input': str(p),
                           'error': str(e)})
        # Periodic save
        if (i + 1) % 2 == 0 or (i + 1) == len(todo):
            results_path.write_text(json.dumps({
                'provenance': get_provenance(),
                'temperature_K': args.temperature,
                'time_ps': args.time_ps,
                'n_done': len(results),
                'results': results,
            }, indent=2, default=str))

    # Final summary
    print(f"\n{'='*68}")
    print(f"{'Champion':<35}{'E_pre':>10}{'E_post':>10}{'ΔE meV/at':>12}")
    print('-' * 68)
    for r in sorted([x for x in results if 'error' not in x],
                   key=lambda x: x.get('delta_E_anneal_meV_per_atom', 0)):
        nat = r.get('n_atoms', 1)
        ep = r.get('E_pre_anneal', 0) / nat
        epo = r.get('E_post_relax', 0) / nat
        de = r.get('delta_E_anneal_meV_per_atom', 0)
        print(f"{r['name']:<35}{ep:>+10.4f}{epo:>+10.4f}{de:>+10.1f}")
    print('=' * 68)
    print(f"Total: {time.time() - t_start:.1f}s")
    print(f"Results: {results_path}")


if __name__ == '__main__':
    main()
