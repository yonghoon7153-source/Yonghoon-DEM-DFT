#!/usr/bin/env python
"""analyze_screening.py — Rank UMA screening results, produce Top-N report.

Reads uma_screening_results.json from run_uma_screening.py and produces a
ranked Top-N report of doped LPSCl candidates by composite score.

Scoring components (weights configurable):
  - Energy (lower is better, normalized): w_E
  - Volume change |ΔV/V0| (smaller is better): w_V
  - Site preference compatibility_score: w_S
  - Charge compensation penalty (imbalanced > 0): w_C

Usage:
  python3 analyze_screening.py \\
      --results data/doping_screening/uma_screening_results.json \\
      --top 20 \\
      --out data/doping_screening/top_candidates.json

  # Custom weights
  python3 analyze_screening.py --results ... --out ... \\
      --w_e 0.4 --w_v 0.3 --w_s 0.2 --w_c 0.1
"""
import argparse
import json
from pathlib import Path
import numpy as np


def normalize(values: list[float], invert: bool = False) -> list[float]:
    """Min-max normalize to [0, 1]. invert=True flips (lower=better)."""
    arr = np.array(values, dtype=float)
    lo, hi = arr.min(), arr.max()
    if hi - lo < 1e-12:
        return [0.5] * len(values)
    norm = (arr - lo) / (hi - lo)
    return (1.0 - norm if invert else norm).tolist()


def _dopant_atom_count(record: dict) -> int:
    """How many atoms of the dopant compound were introduced into the cell.

    Sums all 'n' fields across the placement steps (cation + anion in Type A,
    halide swaps in Type B). Used by ranking objectives that normalize by
    the number of foreign atoms added rather than total cell atoms.
    """
    n_dopant = 0
    for step in record.get('steps', []):
        for placement in step.get('placements', []):
            n_dopant += placement.get('n', 0)
        n_dopant += step.get('n_swap', 0)
    return max(1, n_dopant)  # floor 1 to avoid /0


def compute_score(records: list[dict],
                  objective: str = 'composite',
                  w_e: float = 0.4, w_v: float = 0.3,
                  w_s: float = 0.2, w_c: float = 0.1,
                  converged_penalty: float = 0.10,
                  precursor_mu: dict | None = None) -> list[dict]:
    """Annotate ``records`` with composite_score under the chosen objective.

    Objectives:
      'composite'    — weighted min-max heuristic (current default; arbitrary
                       but useful for first-pass ranking).
      'binding_E'    — sort by ΔE/atom directly. Sundar 2025-style "lower
                       binding energy = more stable doped phase". No
                       normalization, returns the raw absolute value as a
                       positive score (so higher = more negative ΔE).
      'binding_per_dopant' — ΔE × n_atoms / n_dopant_atoms. Removes the
                       systematic bias against high-vacancy compounds. Useful
                       for cross-compound comparison (Y₂O₃ vs Li₂O have
                       different dopant counts per cell).
      'formation_E'  — E_doped − E_LPSCl − Σ Δn_i × μ_i  where Δn_i is the
                       net atom count change for element i and μ_i is the
                       precursor chemical potential (precursor_mu dict; if
                       missing, falls back to ΔE/atom and warns).
      'disorder_sensitivity' — within-ensemble σ ΔE/atom (groups records by
                       (dopant, site, anion_site_label)). Per-record score
                       = group σ. High σ → Pustorino-style ordering
                       sensitivity, may correlate with disorder-enabled
                       conductivity but not stability.
    """
    if not records:
        return records
    if objective != 'composite':
        # Apply soft convergence penalty universally
        for r in records:
            r.setdefault('_score_components', {})

    if objective == 'binding_E':
        for r in records:
            de = r['uma_relaxed']['de_per_atom_vs_baseline']
            score = -de
            if not r.get('converged'):
                score -= converged_penalty
            r['composite_score'] = score
        print(f"  Score: binding_E (raw -ΔE/atom)")
        return records

    if objective == 'binding_per_dopant':
        for r in records:
            de = r['uma_relaxed']['de_per_atom_vs_baseline']
            n_at = r['uma_relaxed']['n_atoms']
            n_dop = _dopant_atom_count(r)
            score = -de * n_at / n_dop
            if not r.get('converged'):
                score -= converged_penalty
            r['composite_score'] = score
        print(f"  Score: binding_per_dopant (-ΔE × n_at / n_dopant_atoms)")
        return records

    if objective == 'formation_E':
        if precursor_mu is None:
            print("  ⚠ --objective formation_E without --precursor_mu, "
                  "falling back to binding_E.")
            return compute_score(records, 'binding_E', converged_penalty=converged_penalty)
        base_E = records[0].get('baseline_e_per_atom', 0)
        for r in records:
            E = r['uma_relaxed']['e_total']
            comp = r['uma_relaxed']['composition']
            base_n = sum(comp.values())  # rough — assumes Li6PS5Cl scale
            f = E - base_E * base_n
            for el, n in comp.items():
                f -= n * precursor_mu.get(el, 0)
            score = -f / base_n
            if not r.get('converged'):
                score -= converged_penalty
            r['composite_score'] = score
        print(f"  Score: formation_E (eV/atom)")
        return records

    if objective == 'disorder_sensitivity':
        from collections import defaultdict
        import statistics
        groups = defaultdict(list)
        for r in records:
            key = (r.get('dopant'), r.get('site'), r.get('anion_site_label'))
            groups[key].append(r)
        for key, rs in groups.items():
            if len(rs) > 1:
                des = [r['uma_relaxed']['de_per_atom_vs_baseline'] for r in rs]
                sigma = statistics.stdev(des)
            else:
                sigma = 0.0
            for r in rs:
                r['composite_score'] = sigma  # higher = more disorder
        print(f"  Score: disorder_sensitivity (σ ΔE within ensemble)")
        return records

    # Default — composite heuristic (kept for backward compat)
    return compute_composite_score(records, w_e, w_v, w_s, w_c,
                                  converged_penalty)


def compute_composite_score(records: list[dict],
                           w_e: float = 0.4, w_v: float = 0.3,
                           w_s: float = 0.2, w_c: float = 0.1,
                           converged_penalty: float = 0.10) -> list[dict]:
    """Composite score per record. Higher = better.

    Non-converged records are kept and ranked (a soft penalty is subtracted
    from the final score, default 0.10 ≈ ten percent of the normalized
    range). Compound-substitution structures often need >300 FIRE steps
    because foreign atoms and multiple Li vacancies create large initial
    strain; dropping them entirely loses real chemistry, while ignoring the
    convergence flag would over-credit them.
    """
    if not records:
        return records

    de = [r['uma_relaxed']['de_per_atom_vs_baseline'] for r in records]
    dv = [abs(r['dV_over_V0']) for r in records]
    sp = [r.get('compatibility_score', 0.0) for r in records]
    cp = [1.0 if str(r.get('charge_compensation', '')).startswith('imbalanced')
          else 0.0 for r in records]

    n_de = normalize(de, invert=True)   # lower energy → higher score
    n_dv = normalize(dv, invert=True)   # smaller |ΔV| → higher score
    n_sp = normalize(sp, invert=False)  # higher compatibility → higher score
    n_cp = normalize(cp, invert=True)   # lower penalty → higher score

    n_conv = sum(1 for r in records if r.get('converged'))
    print(f"  Score: converged {n_conv}/{len(records)}, "
          f"non-converged penalty = {converged_penalty:.2f}")

    for r, ne, nv, ns, nc in zip(records, n_de, n_dv, n_sp, n_cp):
        r['_score_components'] = {
            'energy': ne, 'volume': nv,
            'site_pref': ns, 'charge_comp': nc,
        }
        score = w_e * ne + w_v * nv + w_s * ns + w_c * nc
        if not r.get('converged', False):
            score -= converged_penalty
        r['composite_score'] = score
    return records


#: 축이 이 정도로 붙어 있으면 사실상 한 축이다 — 다목적 최적화가 할 일이 없다.
#: 근거: Yang 2026(BML) `Fig. 17` — σ↔Q_CC 가 좁은 띠라 Pareto 를 돌려도 σ 는 2.9 %
#:   밖에 안 움직였고, 독립축인 Damage 만 64.5 % 개선됐다.
#:   (litdb/talks/yang2026_ncm_radial_microstructure_ml.md · 축은 DEM 이지만 절차는 공통)
AXIS_COLLINEAR = 0.85


def _spearman(a, b):
    """순위 상관. scipy 없이 — 동점은 평균순위."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.size < 3 or np.allclose(a, a[0]) or np.allclose(b, b[0]):
        return float("nan")

    def rank(x):
        o = np.argsort(x, kind="mergesort")
        r = np.empty_like(o, dtype=float)
        r[o] = np.arange(len(x), dtype=float)
        # 동점 평균순위
        for v in np.unique(x):
            m = x == v
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r
    ra, rb = rank(a), rank(b)
    ra -= ra.mean(); rb -= rb.mean()
    d = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / d) if d else float("nan")


def axis_correlations(records: list[dict]) -> dict:
    """점수 축들이 서로 얼마나 붙어 있나 — **Pareto 를 돌리기 전에 본다.**

    왜 (2026-08-25, Yang 2026 에서 이전): 다목적 최적화는 축이 **독립일 때만** 일을 한다.
      두 축이 좁은 띠를 그리면 그건 사실상 한 축이고, Pareto 를 돌려도 그 축은 안 움직인다.
      우리는 지금 가중합(w_e/w_v/w_s/w_c)으로 축을 하나의 숫자로 **뭉개고** 있어서,
      충돌이 있는지 없는지조차 화면에 안 나온다.

    ⛔ 이 함수가 못 하는 것: 인과를 말하지 않는다. 두 축이 붙어 있다는 것이
      "하나가 다른 하나를 만든다" 는 뜻은 아니다. 그리고 상관이 낮다고 그 축이
      **중요한** 것도 아니다 — 독립일 뿐이다.
    """
    axes = ("energy", "volume", "site_pref", "charge_comp")
    col = {k: [r.get("_score_components", {}).get(k) for r in records] for k in axes}
    col = {k: v for k, v in col.items()
           if sum(x is not None for x in v) >= 3}
    out, pairs = {}, []
    keys = list(col)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            va = [x for x, y in zip(col[a], col[b]) if x is not None and y is not None]
            vb = [y for x, y in zip(col[a], col[b]) if x is not None and y is not None]
            rho = _spearman(va, vb)
            pairs.append({"a": a, "b": b, "spearman": rho, "n": len(va),
                          "collinear": bool(abs(rho) >= AXIS_COLLINEAR)
                          if rho == rho else False})
    out["pairs"] = sorted(pairs, key=lambda p: -abs(p["spearman"])
                          if p["spearman"] == p["spearman"] else 0)
    out["n_records"] = len(records)
    out["threshold"] = AXIS_COLLINEAR
    return out


def print_axis_corr(rep: dict):
    print(f"\n{'='*72}\n 점수 축 상관 — Pareto 를 돌릴 값어치가 있나 (n={rep['n_records']})\n{'='*72}")
    print("  ⚠ 축이 서로 붙어 있으면 다목적 최적화가 할 일이 없다.")
    print(f"     |ρ| ≥ {rep['threshold']} 를 '사실상 한 축' 으로 본다.\n")
    bad = 0
    for p in rep["pairs"]:
        rho = p["spearman"]
        if rho != rho:
            print(f"  ·  {p['a']:12s} ↔ {p['b']:12s}   ρ = —      (한쪽이 상수)")
            continue
        mark = "⛔" if p["collinear"] else ("🟡" if abs(rho) >= 0.6 else "✅")
        bad += p["collinear"]
        print(f"  {mark} {p['a']:12s} ↔ {p['b']:12s}   ρ = {rho:+.3f}   n={p['n']}")
    print()
    if bad:
        print(f"  ⛔ 사실상 한 축인 쌍이 {bad}건이다 — 그 축들끼리는 Pareto 가 무의미하다.")
        print("     가중치를 바꿔도 순위가 거의 안 변한다는 뜻이기도 하다.")
    else:
        print("  ✅ 축이 서로 충분히 독립이다 — 다목적(Pareto)이 실제로 일을 한다.")
    print("  ⛔ 인과는 말하지 않는다. 상관이 낮다고 그 축이 중요한 것도 아니다(독립일 뿐).")


def pareto_front(records: list[dict]) -> list[dict]:
    """4축 **비지배(non-dominated)** 집합. 가중합이 지우는 충돌을 그대로 남긴다.

    왜: 가중합은 축을 하나의 숫자로 뭉갠다 — b2o3 가 전도 1등이면서 공기안정성
      최악군인 것 같은 **충돌이 화면에서 사라진다**(open_items #11).
      Pareto 는 "어느 것도 다른 것에 전부 지지 않는" 후보만 남기므로 충돌이 보존된다.

    ⛔ 못 하는 것: 순위를 매기지 않는다. Pareto 는 **집합**이지 순서가 아니다.
      front 안에서 무엇을 고를지는 사람이 정한다(그게 이 방법의 요점이다).
    """
    axes = ("energy", "volume", "site_pref", "charge_comp")
    pts = []
    for r in records:
        c = r.get("_score_components", {})
        v = [c.get(k) for k in axes]
        pts.append(None if any(x is None for x in v) else np.asarray(v, float))
    front = []
    for i, p in enumerate(pts):
        if p is None:
            continue
        dominated = False
        for j, q in enumerate(pts):
            if i == j or q is None:
                continue
            # q 가 모든 축에서 p 이상이고 하나 이상에서 진짜 크면 p 는 지배당한다
            if np.all(q >= p) and np.any(q > p):
                dominated = True
                break
        if not dominated:
            records[i]["_pareto"] = True
            front.append(records[i])
        else:
            records[i]["_pareto"] = False
    return front


def print_top_table(ranked: list[dict], n: int = 20):
    """Print human-readable Top-N table."""
    print(f"\n{'='*100}")
    print(f"{'Rank':<5}{'Dopant':<8}{'Site':<10}{'x':<8}"
          f"{'ΔE/atom':<12}{'ΔV/V0':<10}{'CompScore':<12}{'Charge_comp':<20}")
    print('-' * 100)
    for i, r in enumerate(ranked[:n], 1):
        print(f"{i:<5}{r['dopant']:<8}{r['site']:<10}"
              f"{r['concentration']*100:>5.1f}% "
              f"{r['uma_relaxed']['de_per_atom_vs_baseline']:>+8.4f} eV  "
              f"{r['dV_over_V0']*100:>+6.2f}%  "
              f"{r['composite_score']:>8.4f}    "
              f"{r['charge_compensation']:<20}")
    print('=' * 100)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--results', required=True,
                       help='uma_screening_results.json')
    parser.add_argument('--out', required=True,
                       help='Top-N output JSON')
    parser.add_argument('--top', type=int, default=20,
                       help='Number of top candidates to report')
    parser.add_argument('--w_e', type=float, default=0.4,
                       help='Weight: energy')
    parser.add_argument('--w_v', type=float, default=0.3,
                       help='Weight: volume change')
    parser.add_argument('--w_s', type=float, default=0.2,
                       help='Weight: site preference')
    parser.add_argument('--w_c', type=float, default=0.1,
                       help='Weight: charge compensation penalty')
    parser.add_argument('--objective', default='composite',
                       choices=['composite', 'binding_E', 'formation_E',
                                'binding_per_dopant', 'disorder_sensitivity'],
                       help='Ranking metric (default composite — heuristic; '
                            'binding_E = raw ΔE/atom; '
                            'formation_E = E_doped − n_LPSCl×μ_LPSCl − Σ n_i × μ_i '
                            '(needs --precursor_mu JSON); '
                            'binding_per_dopant = ΔE normalized by number of '
                            'dopant atoms introduced (penalty-free per-atom); '
                            'disorder_sensitivity = σ ΔE across ensemble '
                            'seeds, higher = more Li-ordering sensitive '
                            '(Pustorino-style metric).')
    parser.add_argument('--axis_corr', action='store_true',
                       help='점수 축들이 서로 붙어 있는지 먼저 본다. 축이 사실상 하나면 '
                            'Pareto·가중치 조정이 할 일이 없다 (Yang 2026 Fig.17 이전).')
    parser.add_argument('--pareto', action='store_true',
                       help='4축 비지배 집합(Pareto front)을 같이 낸다. 가중합이 지우는 '
                            '축 간 충돌을 보존한다 — 순위가 아니라 **집합**이다.')
    parser.add_argument('--precursor_mu',
                       help='JSON {element_or_compound: chemical_potential_eV} '
                            'for --objective formation_E. Without it falls '
                            'back to ΔE/atom of dopant-containing cell.')
    parser.add_argument('--max_dv', type=float, default=0.10,
                       help='Filter: max |ΔV/V0| (default 10%%). Compound '
                            'substitution often needs 0.20 because foreign '
                            'large cations + multiple Li vacancies expand the '
                            'lattice by 10-17%% (BaO, SrO, ZnO, Nd2O3, Y2O3).')
    parser.add_argument('--converged_penalty', type=float, default=0.10,
                       help='Composite-score penalty for non-converged FIRE '
                            'relaxations (default 0.10). Set 0 to ignore the '
                            'flag; set higher to be stricter.')
    parser.add_argument('--max_de', type=float, default=None,
                       help='Filter: max ΔE/atom vs baseline (eV)')
    parser.add_argument('--min_li_per_fu', type=float, default=4.0,
                       help='Filter: minimum Li atoms per formula unit '
                            '(default 4.0 = Li4PS5Cl floor; Sundar/Kraft '
                            'literature working range is Li5.4-6.0). Set to '
                            '0 to disable.')
    parser.add_argument('--n_fu', type=int, default=4,
                       help='Formula units per cell (default 4 for Li6PS5Cl '
                            'conventional cell)')
    parser.add_argument('--dedupe', action='store_true', default=True,
                       help='Drop duplicate records with identical composition '
                            'and ΔE within 1 meV/atom (default on)')
    args = parser.parse_args()

    data = json.loads(Path(args.results).read_text())
    records = data.get('results', [])
    print(f"Loaded {len(records)} records from {args.results}")

    # Filter pre-screen
    pre = records
    n_before = len(pre)
    if args.max_dv is not None:
        pre = [r for r in pre if abs(r.get('dV_over_V0', 1e9)) <= args.max_dv]
    if args.max_de is not None:
        pre = [r for r in pre
               if r['uma_relaxed']['de_per_atom_vs_baseline'] <= args.max_de]
    if args.min_li_per_fu > 0:
        before_li = len(pre)
        pre = [r for r in pre
               if r['uma_relaxed']['composition'].get('Li', 0) / args.n_fu
                  >= args.min_li_per_fu]
        print(f"  Li-retention filter (≥{args.min_li_per_fu} Li/f.u.): "
              f"{before_li} → {len(pre)} records")
    if args.dedupe:
        before_dd = len(pre)
        seen: set[tuple] = set()
        dedup = []
        for r in pre:
            comp = tuple(sorted(r['uma_relaxed']['composition'].items()))
            de = round(r['uma_relaxed']['de_per_atom_vs_baseline'] * 1000)
            key = (comp, de)
            if key not in seen:
                seen.add(key)
                dedup.append(r)
        pre = dedup
        print(f"  Dedup (composition + ΔE/atom 1 meV bucket): "
              f"{before_dd} → {len(pre)} records")
    print(f"  Total after all filters: {len(pre)}/{n_before}")

    precursor_mu = None
    if args.precursor_mu:
        precursor_mu = json.loads(Path(args.precursor_mu).read_text())
    scored = compute_score(pre, args.objective,
                          args.w_e, args.w_v, args.w_s, args.w_c,
                          args.converged_penalty, precursor_mu)
    ranked = sorted(scored, key=lambda r: r['composite_score'], reverse=True)

    print_top_table(ranked, args.top)

    # Per-dopant best (across the full ranked list, so all dopants get a row)
    by_dopant = {}
    for r in ranked:
        d = r['dopant']
        if d not in by_dopant:
            by_dopant[d] = r

    # Unique dopants WITHIN top-N (the previous wording conflated this with
    # the per-dopant-best count over the full ranked list).
    top_slice = ranked[:args.top]
    unique_in_top = {r['dopant'] for r in top_slice}
    print(f"\nUnique dopants in Top-{args.top}: {len(unique_in_top)} "
          f"({', '.join(sorted(unique_in_top))})")
    print(f"Unique dopants across all {len(ranked)} ranked records: "
          f"{len(by_dopant)}")

    axis_rep = pareto = None
    if args.axis_corr:
        axis_rep = axis_correlations(ranked)
        print_axis_corr(axis_rep)
    if args.pareto:
        pareto = pareto_front(ranked)
        print(f"\n{'='*72}\n Pareto front — 어느 것도 전부 지지는 않는 후보\n{'='*72}")
        print(f"  {len(pareto)}/{len(ranked)} 이 비지배다.")
        print("  ⛔ 이건 **순위가 아니라 집합**이다 — 안에서 무엇을 고를지는 사람이 정한다.")
        if axis_rep and any(p['collinear'] for p in axis_rep['pairs']):
            print("  ⚠ 위에서 사실상 한 축인 쌍이 나왔다 — 그 축들에 대해서는 이 front 가")
            print("     실제 선택지를 주지 않는다(같은 방향으로만 움직인다).")
        for r in pareto[:args.top]:
            c = r.get('_score_components', {})
            print(f"    {r.get('dopant','?'):4s} {str(r.get('site','')):10s} "
                  f"E {c.get('energy', float('nan')):.2f} V {c.get('volume', float('nan')):.2f} "
                  f"S {c.get('site_pref', float('nan')):.2f} C {c.get('charge_comp', float('nan')):.2f}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        'baseline': data.get('baseline'),
        'axis_correlations': axis_rep,
        'pareto_front': [{'dopant': r.get('dopant'), 'site': r.get('site'),
                          'components': r.get('_score_components')} for r in pareto]
                        if pareto is not None else None,
        'weights': {'energy': args.w_e, 'volume': args.w_v,
                    'site_pref': args.w_s, 'charge_comp': args.w_c},
        'filters': {'max_dv': args.max_dv, 'max_de': args.max_de},
        'n_total': len(records),
        'n_after_filter': len(pre),
        'top_n': args.top,
        'top_candidates': ranked[:args.top],
        'best_per_dopant': list(by_dopant.values()),
    }, indent=2, default=str))
    print(f"\n✓ Top-{args.top}: {out_path}")


def _selftest():
    """axis_correlations · pareto_front 자체검사. **음성 경로 포함.**"""
    ok = True

    def say(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok = ok and c

    print("── analyze_screening selftest ──")
    def rec(e, v, s_, c):
        return {"_score_components": {"energy": e, "volume": v,
                                      "site_pref": s_, "charge_comp": c}}
    # ① 양성: 완전히 붙은 두 축을 잡는다
    n = 20
    R = [rec(i / n, i / n, (n - i) / n, 0.5) for i in range(n)]
    rep = axis_correlations(R)
    pair = next(p for p in rep["pairs"] if {p["a"], p["b"]} == {"energy", "volume"})
    say(pair["collinear"] and pair["spearman"] > 0.99, "① 같은 축은 ρ≈1 · collinear")
    # ② 양성: 반대로 가는 축도 사실상 한 축이다 (부호가 아니라 |ρ|)
    pair = next(p for p in rep["pairs"] if {p["a"], p["b"]} == {"energy", "site_pref"})
    say(pair["collinear"] and pair["spearman"] < -0.99, "② 역상관도 collinear (|ρ| 로 본다)")
    # ③ [음성] 상수 축은 nan 이고 collinear 가 **아니다** (붙었다고 하면 안 된다)
    pair = next(p for p in rep["pairs"] if {p["a"], p["b"]} == {"energy", "charge_comp"})
    say(pair["spearman"] != pair["spearman"] and not pair["collinear"],
        "③ [음성] 한쪽이 상수면 ρ=nan · collinear 아님")
    # ④ [음성] 독립 축을 collinear 로 오판하지 않는다
    import random as _r
    _r.seed(0)
    R2 = [rec(_r.random(), _r.random(), _r.random(), _r.random()) for _ in range(200)]
    rep2 = axis_correlations(R2)
    say(not any(p["collinear"] for p in rep2["pairs"]),
        "④ [음성] 무작위(독립) 축을 collinear 로 오판하지 않는다")
    # ⑤ Pareto — 명백히 지배당하는 점은 front 에 없다
    # ⚠ 첫 픽스처는 A 를 전 축 1.0 으로 뒀다가 A 가 C 를 **지배해버려** 테스트가 틀렸다
    #   (코드가 아니라 테스트가 틀린 경우다). 서로 못 이기는 쌍으로 세운다.
    A = rec(1.0, 0.2, 1.0, 0.2)          # 에너지·자리선호 우세
    B = rec(0.1, 0.1, 0.1, 0.1)          # 둘 다에게 전 축에서 짐
    C = rec(0.2, 1.0, 0.2, 1.0)          # 부피·전하보상 우세 → 충돌. 둘 다 남아야 한다
    fr = pareto_front([A, B, C])
    say(B not in fr, "⑤ 전 축에서 지는 점은 front 에서 빠진다")
    say(A in fr and C in fr,
        "⑤ 서로 다른 축에서 이기는 둘은 **둘 다** 남는다 (가중합이 지우는 충돌)")
    # ⑥ [음성] 축 값이 없는 레코드를 front 에 넣지 않는다
    D = {"_score_components": {"energy": 0.9}}
    fr2 = pareto_front([rec(1.0, 1.0, 1.0, 1.0), D])
    say(D not in fr2, "⑥ [음성] 축이 빠진 레코드는 front 에 안 넣는다")
    print("  " + ("✅ selftest 통과" if ok else "⛔ selftest 실패"))
    return 0 if ok else 1


if __name__ == '__main__':
    import sys as _s
    _s.exit(_selftest() if '--selftest' in _s.argv else main())
