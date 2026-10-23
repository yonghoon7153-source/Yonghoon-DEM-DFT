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


def mp_db_version(key):
    """MP DB 판 (기저를 봉인할 때 같이 적는다 · 못 읽으면 None — 조용히 지어내지 않는다)."""
    try:
        from mp_api.client import MPRester
        with MPRester(key) as mpr:
            return str(mpr.get_database_version())
    except Exception as e:                      # noqa: BLE001 — 판 기록은 부가 정보
        return f"unknown ({type(e).__name__})"


def decomposition_entries(decomp):
    """pd.get_decomposition 결과 → [{formula, entry_id, amount}] (amount = 원자 분율).

    2026-10-23 (Nd Q2 기저): 환원식만 남기면 **어느 다형체인지** 가 사라진다 —
    분해상 구조를 받을 때 그 엔트리 (mp-id) 를 그대로 쓰려고 id 를 같이 남긴다."""
    out = [{"formula": d.composition.reduced_formula,
            "entry_id": getattr(d, "entry_id", None),
            "amount": round(float(a), 6)} for d, a in decomp.items()]
    return sorted(out, key=lambda r: -r["amount"])


def tieline_points(xs, compA, nA, eA_tot, compB, nB, eB_tot, hull_fn):
    """유사이원계 (1−x)·A + x·B 선을 훑어 **반응에너지** ΔE_rxn(x) 를 낸다.

        ΔE_rxn(x) = E_hull(c(x)) − [(1−x)·e_A + x·e_B]      [eV/atom]

    c(x) 는 **1 원자로 정규화한** 조성이므로 `hull_fn` 이 그 조성의 hull 에너지를
    돌려주면 곧바로 원자당 값이다.

    ⛔ 부호를 읽는 법 — 이걸 모르면 결과를 거꾸로 읽는다:
      · A·B 가 **둘 다 hull 위**면 볼록성 때문에 ΔE ≤ 0 이 **구조적으로 보장**된다.
        따라서 "양수가 나오면 반응 안 함" 은 틀린 해석이다.
      · ΔE ≈ 0  → A–B 가 hull 의 **tie-line** 이다 = 사이에 안정한 중간상이 없다
                  = **이상(二相) 공존**. 이것이 '새 결정상 없음' 이다.
      · ΔE < 0  → 직선 아래에 중간상이 있다 = **새 상 생성**. 무엇인지는
                  `decomp_fn` (호출부)이 따로 답한다.
      · ΔE > 0  → **양 끝점이 hull 위에 없다**(우리 구조가 준안정). 판정이 아니라
                  게이트 위반 신호다 — 그대로 쓰지 말고 끝점 E_above_hull 부터 본다.
        ⇒ 그래서 이 함수는 양수를 **조용히 넘기지 않고** `endpoints_off_hull` 로 표시한다.

    ⛔ 이 함수가 못 하는 것
      · hull 을 만들지 않는다 (`hull_fn` 을 받는다 — 그래서 pymatgen 없이 시험 가능)
      · 생성물이 **무엇인지** 답하지 않는다 (분해 목록은 호출부)
      · 비평형(볼밀·비정질)을 답하지 않는다 — 결정 평형만이다
    """
    aA = {el: v / nA for el, v in compA.items()}
    aB = {el: v / nB for el, v in compB.items()}
    eA, eB = eA_tot / nA, eB_tot / nB
    out = []
    for x in xs:
        c = {el: (1 - x) * aA.get(el, 0.0) + x * aB.get(el, 0.0)
             for el in set(aA) | set(aB)}
        eref = (1 - x) * eA + x * eB
        ehull = hull_fn(c)
        d = (ehull - eref) * 1000.0
        out.append({"x": round(x, 4), "comp_per_atom": {k: round(v, 6) for k, v in c.items()},
                    "E_unreacted_mix_per_atom_eV": eref, "E_hull_per_atom_eV": ehull,
                    "dE_rxn_meV_per_atom": d,
                    "endpoints_off_hull": bool(d > 1.0)})
    return out


def _selftest_tieline():
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  \u2b55 " if c else "  \u26d4 ") + m)
        ok, bad = ok + (1 if c else 0), bad + (0 if c else 1)

    A, nA, eA = {"Li": 6, "P": 1, "S": 5, "Cl": 1}, 13, -13.0    # e/atom = -1.0
    B, nB, eB = {"Li": 2, "S": 1}, 3, -6.0                        # e/atom = -2.0
    line = lambda c, xs=None: None
    def hull_on_line(c):      # hull 이 직선과 정확히 같다 = tie-line
        x = c["Li"]           # 아래 산술로 x 를 되뽑지 않고 직접 계산한다
        return None
    # 직선 위 hull: eref 를 그대로 돌려주는 hull_fn 을 x 로부터 만든다
    xs = [0.0, 0.25, 0.5, 0.75, 1.0]
    ref = [(1 - x) * (eA / nA) + x * (eB / nB) for x in xs]
    it = iter(ref)
    r0 = tieline_points(xs, A, nA, eA, B, nB, eB, lambda c: next(it))
    chk(all(abs(r["dE_rxn_meV_per_atom"]) < 1e-9 for r in r0),
        "hull 이 직선과 같으면 \u0394E = 0 (tie-line = 이상 공존)")
    # ⚠ `comp_per_atom` 은 **출력용으로 round(…,6)** 된 값이다. 원소 4종이면 합의
    #   오차가 최대 2e-6 이라 1e-9 로 재면 통과할 수가 없다 — 첫 판에 이걸로 실패했다.
    chk(all(abs(sum(r["comp_per_atom"].values()) - 1.0) < 5e-6 for r in r0),
        "조성이 모든 x 에서 1 원자로 정규화된다 (출력 반올림 허용오차 5e-6)")
    chk(r0[0]["comp_per_atom"]["Cl"] > 0 and r0[-1]["comp_per_atom"].get("Cl", 0) == 0,
        "x=0 은 A(Cl 있음) · x=1 은 B(Cl 없음)")
    # decomposition_entries (2026-10-23) — id 를 남기고 · 없는 id 를 지어내지 않는다
    from types import SimpleNamespace as _NS

    class _Ent:                       # dict 키라 해시가 돼야 한다 (SimpleNamespace 는 안 된다)
        def __init__(self, f, i):
            self.composition = _NS(reduced_formula=f)
            if i is not None:
                self.entry_id = i
    _e = _Ent
    de = decomposition_entries({_e("Li2S", "mp-1153-GGA"): 0.25, _e("LiCl", None): 0.75})
    chk(de[0]["formula"] == "LiCl" and de[1]["entry_id"] == "mp-1153-GGA",
        "분해 엔트리: 큰 분율 순 · mp-id 를 그대로 남긴다")
    chk(de[0]["entry_id"] is None, "⛔음성: id 가 없는 엔트리는 None — 지어내지 않는다")
    it2 = iter([v - 0.05 for v in ref])
    r1 = tieline_points(xs, A, nA, eA, B, nB, eB, lambda c: next(it2))
    chk(all(abs(r["dE_rxn_meV_per_atom"] + 50.0) < 1e-6 for r in r1),
        "hull 이 직선보다 50 meV/atom 낮으면 \u0394E = \u221250 (새 상 생성)")
    chk(not any(r["endpoints_off_hull"] for r in r1),
        "\u26d4음성: 음수 \u0394E 를 끝점 이상으로 오인하지 않는다")
    it3 = iter([v + 0.05 for v in ref])
    r2 = tieline_points(xs, A, nA, eA, B, nB, eB, lambda c: next(it3))
    chk(all(r["endpoints_off_hull"] for r in r2),
        "\u26d4음성: 양수 \u0394E 는 **끝점이 hull 위에 없다**로 표시한다 (판정으로 쓰지 않는다)")
    # ⛔음성 — **이 시험이 오늘 놓친 실패 유형이다.** 2026-09-11 에 `--tieline` 플래그와
    #   순수함수는 만들었는데 `main()` 에서 **부르지 않아** 플래그가 조용히 무시됐다.
    #   순수함수 시험은 6/6 으로 통과했다. 배선을 소스에서 직접 확인한다.
    import inspect, re as _re
    src = pathlib.Path(inspect.getfile(inspect.currentframe())).read_text(encoding="utf-8") \
        if False else open(__file__, encoding="utf-8").read()
    body = src.split("def main(")[-1]
    chk(bool(_re.search(r"\btieline_points\s*\(", body)),
        "⛔음성: main() 이 tieline_points() 를 **실제로 부른다** (플래그만 있고 배선 없는 상태를 잡는다)")
    chk("args.tieline" in body,
        "⛔음성: main() 이 args.tieline 을 읽는다")
    print(f"tieline selftest: \u2b55 {ok} \u00b7 \u26d4 {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="tie-line 산술만 시험한다 (pymatgen·UMA·MP 불필요)")
    ap.add_argument("--tieline", nargs=2, type=int, metavar=("iA", "iB"),
                    help="--cif 목록의 두 인덱스를 유사이원계 끝점으로 삼아 dE_rxn(x) 를 낸다")
    ap.add_argument("--x", nargs="+", type=float, default=[0.10, 0.25, 0.50, 0.75, 0.90],
                    help="tie-line 을 훑을 x (B 쪽 몰분율)")
    ap.add_argument("--cif", nargs="+",
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
    if args.selftest:
        raise SystemExit(_selftest_tieline())
    if not args.cif:
        ap.error('--cif 가 필요하다 (--selftest 제외)')
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
        _ends = []          # ★ tie-line 용 — 끝점의 (조성·원자수·총에너지) 를 모은다
        for sp, s in structs:
            c = s.composition
            our_E = uma_E(s)
            our_entry = ComputedEntry(c, our_E)
            _ends.append({"path": str(sp), "reduced": c.reduced_formula,
                          "comp": {str(el): float(n) for el, n in c.get_el_amt_dict().items()},
                          "n": len(s), "E_tot": our_E, "entry": our_entry})
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

        # ── tie-line 스캔 (--tieline) ─────────────────────────────────────
        #   ⛔ 2026-09-11 — 플래그와 순수함수만 있고 **여기서 부르지 않아** `--tieline`
        #     이 조용히 무시됐다. selftest 가 순수함수만 봐서 통과했다 —
        #     CLAUDE.md 가 경고한 "양성만 있는 selftest" 다. 던지기 전에 잡았다.
        if args.tieline:
            from pymatgen.core import Composition
            iA, iB = args.tieline
            if not (0 <= iA < len(_ends) and 0 <= iB < len(_ends) and iA != iB):
                raise SystemExit(f"⛔ --tieline 인덱스가 --cif 범위 밖이거나 같다: {args.tieline} "
                                 f"(--cif 는 {len(_ends)}개)")
            A, B = _ends[iA], _ends[iB]
            pd_all = PhaseDiagram(entries + [e["entry"] for e in _ends])

            def _hull(cdict):
                return float(pd_all.get_hull_energy(Composition(cdict)))

            pts = tieline_points(args.x, A["comp"], A["n"], A["E_tot"],
                                 B["comp"], B["n"], B["E_tot"], _hull)
            for pt in pts:                    # 각 x 에서 **무엇으로** 분해되는지
                dec = pd_all.get_decomposition(Composition(pt["comp_per_atom"]))
                pt["decomposition"] = {d.composition.reduced_formula: round(a, 4)
                                       for d, a in dec.items()}
            tl = {"A": {k: A[k] for k in ("path", "reduced", "n", "E_tot")},
                  "B": {k: B[k] for k in ("path", "reduced", "n", "E_tot")},
                  "x_is_mole_fraction_of": B["reduced"],
                  "points": pts,
                  "⛔_부호_읽는_법": ("A·B 가 둘 다 hull 위면 볼록성 때문에 ΔE ≤ 0 이 구조적으로 "
                      "보장된다. ΔE ≈ 0 = tie-line = 이상 공존(새 결정상 없음) · ΔE < 0 = 새 상 생성 · "
                      "ΔE > 0 = **끝점이 hull 위에 없다**(판정 아님, 게이트 위반 신호)."),
                  "⛔_못_하는_것": "결정 평형만 답한다. 비평형(볼밀·비정질)은 이 수가 답하지 않는다."}
            print(f"\n── tie-line: (1−x)·{A['reduced']} + x·{B['reduced']} ──")
            for pt in pts:
                flag = "  ⛔끝점이 hull 위에 없다" if pt["endpoints_off_hull"] else ""
                print(f"  x={pt['x']:<6} ΔE_rxn = {pt['dE_rxn_meV_per_atom']:+8.1f} meV/atom"
                      f"   → {pt['decomposition']}{flag}")
            for _, r in outs:
                r["tieline"] = tl

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
        from datetime import datetime, timezone
        result.update({
            "hull_energy_eV": float(hull_e),
            "hull_energy_per_atom": float(hull_e) / comp.num_atoms,
            "decomposition_products": {d.composition.reduced_formula: round(amt, 4)
                                       for d, amt in decomp.items()},
            "decomposition_entries": decomposition_entries(decomp),
            "mp_database_version": mp_db_version(key),
            "query_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "note": "MP-energy hull. Products + hull energy at our composition. "
                    "Absolute E_above_hull of OUR structure needs an MP-compatible "
                    "energy (use --mode uma for a self-consistent number).",
        })
        print("\nMP-hull decomposition products at our composition:")
        print(result["decomposition_products"])
        for r_ in result["decomposition_entries"]:
            print(f"  {r_['formula']:<14} {r_['entry_id']}  원자 분율 {r_['amount']:.4f}")
        print(f"  MP DB {result['mp_database_version']} · {result['query_utc']}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2))
    print(f"-> {args.out}")


if __name__ == "__main__":
    main()
