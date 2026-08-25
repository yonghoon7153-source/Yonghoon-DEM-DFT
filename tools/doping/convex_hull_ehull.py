#!/usr/bin/env python3
"""E_above_hull (convex-hull stability) for a doped argyrodite.

Two modes:
  --mode uma  (DEFAULT, self-consistent): UMA single-points OUR structure AND
      every MP competing phase in the chemsys, builds the PhaseDiagram from
      those UMA energies -> internally consistent E_above_hull. UMA(omat) is one
      method for everything, so the number is meaningful (no QE-vs-MP mixing).
  --mode mp   (fast, products only): builds the hull from MP energies and reports
      what OUR composition decomposes into + the hull energy at that composition.
      Does NOT give our structure's absolute E_above_hull (would need an
      MP-compatible energy for it), but the decomposition PRODUCTS are robust.

Needs: pymatgen, mp_api, MP_API_KEY env; for --mode uma also fairchem + a GPU.
Run on gabia (has the oxidation env + internet + UMA).

  MP_API_KEY=... python3 tools/doping/convex_hull_ehull.py \
      --cif db/structures/b2o3_relaxV0.cif --mode uma --device cuda \
      --out /data/work/runs/b2o3_ehull/ehull_uma.json
"""
import argparse, os, json
from pathlib import Path


def get_mp_entries(elements, key):
    from mp_api.client import MPRester
    with MPRester(key) as mpr:
        try:
            ents = mpr.get_entries_in_chemsys(elements, inc_structure=True)
        except TypeError:
            ents = mpr.get_entries_in_chemsys(elements)   # older client
    return ents


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cif", required=True, nargs="+",
                    help="구조 파일 1개 이상. **여러 개를 주면 경쟁상 hull 을 한 번만 "
                         "만들어 재사용한다** — 같은 chemsys 를 구조마다 다시 도는 것은 "
                         "GPU 시간 낭비이고, 다른 GPU 런과 같이 돌 때는 위험까지 된다.")
    ap.add_argument("--elements", nargs="+",
                    default=["Li", "P", "S", "Cl", "B", "O"])
    ap.add_argument("--mode", choices=["uma", "mp"], default="uma")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--out", default="ehull_result.json",
                    help="구조가 여러 개면 파일명에 구조 stem 을 끼워 넣는다")
    ap.add_argument("--vram_fraction", type=float, default=None,
                    help="이 프로세스의 VRAM 상한 (예: 0.10). 다른 UMA 런과 같이 돌 때 "
                         "**이쪽이 먼저 죽게** 만들어 기존 런을 지킨다.")
    args = ap.parse_args()
    key = os.environ.get("MP_API_KEY")
    if not key:
        raise SystemExit("set MP_API_KEY env var")

    if args.vram_fraction:
        import torch
        if torch.cuda.is_available():
            torch.cuda.set_per_process_memory_fraction(args.vram_fraction)
            print(f"⚙ VRAM 상한 {args.vram_fraction:.0%} — 넘으면 **이 프로세스가** 죽는다")

    from pymatgen.core import Structure
    from pymatgen.entries.computed_entries import ComputedEntry
    from pymatgen.analysis.phase_diagram import PhaseDiagram

    struct_paths = [Path(c) for c in args.cif]
    structs = [(sp, Structure.from_file(sp)) for sp in struct_paths]
    for sp, s in structs:
        print(f"our composition: {s.composition.reduced_formula}  "
              f"({s.composition.formula})   [{sp.name}]")
    ours, comp = structs[0][1], structs[0][1].composition
    mp_entries = get_mp_entries(args.elements, key)
    print(f"MP entries in {'-'.join(args.elements)}: {len(mp_entries)}")

    result = {"cif": args.cif, "composition": comp.formula,
              "reduced": comp.reduced_formula, "elements": args.elements,
              "mode": args.mode, "n_mp_entries": len(mp_entries)}

    if args.mode == "uma":
        from fairchem.core import pretrained_mlip
        from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
        from pymatgen.io.ase import AseAtomsAdaptor
        pred = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device)
        calc = FAIRChemCalculator(pred, task_name="omat")
        ad = AseAtomsAdaptor()

        def uma_E(struct):
            at = ad.get_atoms(struct); at.calc = calc
            return float(at.get_potential_energy())

        # ★ 경쟁상 단일점은 **한 번만** — 구조마다 다시 돌면 같은 계산을 N 번 한다.
        entries, skipped, fails = [], 0, []
        for i, e in enumerate(mp_entries):
            if i and i % 200 == 0:
                print(f"  경쟁상 단일점 {i}/{len(mp_entries)} …", flush=True)
            st = getattr(e, "structure", None)
            if st is None:
                skipped += 1
                fails.append("no_structure")
                continue
            try:
                entries.append(ComputedEntry(st.composition, uma_E(st)))
            except Exception as ex:
                skipped += 1
                fails.append(type(ex).__name__)
        frac = skipped / max(len(mp_entries), 1)
        print(f"  경쟁상 {len(entries)} 계산 · 건너뜀 {skipped} ({frac:.1%})")
        if frac > 0.05:
            # ⛔ 건너뛴 상은 hull 에서 빠진다 = hull 이 실제보다 **높게** 잡힌다
            #    = E_above_hull 이 실제보다 **낮게** 나온다. 조용히 넘기면 안 된다.
            import collections as _c
            print(f"  ⚠⚠ 건너뛴 비율이 {frac:.1%} 다 — hull 이 **불완전한 경쟁상 집합**에서 "
                  f"만들어졌고 E_above_hull 이 실제보다 낮게 나온다. "
                  f"사유: {dict(_c.Counter(fails).most_common(3))}")

        result["n_uma_entries"] = len(entries)
        result["skipped"] = skipped
        result["skipped_fraction"] = round(frac, 4)
        result["skip_reasons"] = dict(__import__("collections").Counter(fails).most_common(5))
        result["uma_model"] = args.uma_model
        result["hull_is_complete"] = bool(frac <= 0.05)

        outs = []
        for sp, s in structs:
            c = s.composition
            our_E = uma_E(s)
            our_entry = ComputedEntry(c, our_E)
            pd = PhaseDiagram(entries + [our_entry])
            eah = pd.get_e_above_hull(our_entry)            # eV/atom
            decomp = pd.get_decomposition(c)
            r = dict(result)
            r.update({
                "cif": str(sp), "composition": c.formula,
                "reduced": c.reduced_formula,
                "our_E_eV": our_E, "our_E_per_atom": our_E / len(s),
                "E_above_hull_eV_per_atom": eah,
                "on_hull": bool(eah < 1e-3),
                "decomposition": {d.composition.reduced_formula: round(amt, 4)
                                  for d, amt in decomp.items()},
                "note": "UMA(omat)-consistent hull: our structure + all MP phases "
                        "single-pointed with UMA. E_above_hull is internally "
                        "consistent (MLIP, not DFT-absolute).",
                "⛔_do_not": "조성이 다른 구조끼리 E/atom 을 비교하지 말 것. "
                             "그 비교는 화학퍼텐셜을 섞는다 — E_above_hull 이 그것을 "
                             "정확히 흡수하므로 판정은 이 값으로만 한다.",
            })
            print(f"\n[{sp.stem}] E_above_hull = {eah*1000:.1f} meV/atom  "
                  f"({'ON HULL / stable' if eah < 1e-3 else 'metastable'})")
            print("  decomposes into:", r["decomposition"])
            outs.append((sp, r))

        if len(outs) > 1:
            ranked = sorted(outs, key=lambda x: x[1]["E_above_hull_eV_per_atom"])
            gap = (ranked[1][1]["E_above_hull_eV_per_atom"]
                   - ranked[0][1]["E_above_hull_eV_per_atom"]) * 1000
            print(f"\n★ 낮은 쪽: {ranked[0][0].stem}  (차이 {gap:.1f} meV/atom)")
            if not result["hull_is_complete"]:
                print("  ⚠ 다만 경쟁상 집합이 불완전하다 — 위 순서를 확정으로 쓰지 말 것")
        for sp, r in outs:
            o = Path(args.out)
            if len(outs) > 1:
                o = o.with_name(f"{o.stem}_{sp.stem}{o.suffix}")
            o.parent.mkdir(parents=True, exist_ok=True)
            o.write_text(json.dumps(r, indent=2))
            print(f"-> {o}")
        return
    else:
        # ⛔ mp 모드는 구조 하나만 처리한다. 여러 개를 받고 **조용히 첫 번째만** 쓰면
        #   나머지가 계산된 줄 안다 — 이 파이프라인의 상습 결함이라 거부한다.
        if len(structs) > 1:
            raise SystemExit(
                f"⛔ --mode mp 는 구조 하나만 받는다 ({len(structs)}개 받음). "
                f"여러 구조는 --mode uma 로 (경쟁상 hull 을 한 번만 만들어 재사용한다).")
        pd = PhaseDiagram(mp_entries)
        decomp = pd.get_decomposition(comp)
        hull_e = pd.get_hull_energy(comp)
        result.update({
            "hull_energy_eV": float(hull_e),
            "hull_energy_per_atom": float(hull_e) / comp.num_atoms,
            "decomposition_products": {d.composition.reduced_formula: round(amt, 4)
                                       for d, amt in decomp.items()},
            "note": "MP-energy hull. Products + hull energy at our composition. "
                    "Absolute E_above_hull of OUR structure needs an MP-compatible "
                    "energy (use --mode uma for a self-consistent number).",
        })
        print("\nMP-hull decomposition products at our composition:")
        print(result["decomposition_products"])

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
