#!/usr/bin/env python3
"""assemble_report_card.py — build a standardized electrochemical report card
for a (doped) solid electrolyte from existing db/ results + cascade screening.

v1 foundation: reads a system's db/properties files, maps them to the report-card
schema (factory/schema/report_card.schema.json), links the upstream cascade
candidate (versioned, loose coupling), and writes JSON + Markdown to factory/cards/.

  python3 factory/assemble_report_card.py b2o3

Every section carries status/confidence/method/source/caveats so the card never
over-claims. Sections with no clean source are marked 'pending' (e.g. b2o3 elastic
still running on KISTI). The orchestrator (v1.1) will run the stages; this v1.0
proves the schema + the cascade<->deep link on real data.
"""
import argparse, json, csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBP = ROOT / "db" / "properties"
CARDS = Path(__file__).resolve().parent / "cards"


def jload(name):
    p = DBP / name
    return json.loads(p.read_text()) if p.exists() else None


def csv_rows(name):
    p = DBP / name
    if not p.exists():
        return []
    return [r for r in csv.reader(p.open()) if r and not r[0].startswith("#")]


def cascade_row(csv_name, key_col, key):
    rows = csv_rows(csv_name)
    if not rows:
        return None
    hdr = rows[0]
    ci = hdr.index(key_col) if key_col in hdr else 0
    for r in rows[1:]:
        if r[ci] == key:
            return dict(zip(hdr, r))
    return None


# ---- system registry (which sources map to a system). cascade = versioned link ----
SYSTEMS = {
    "b2o3": {
        "id": "b2o3",
        "composition": "Li58P8S41Cl16B2O3",
        "structure_ref": "db/structures/b2o3_relaxV0.cif",
        "n_atoms": 128,
        "provenance": "DFT V0 fixed-cell relax (B2O3-doped LPSCl1.6 champion)",
        "cascade": {"version": "cascade_v23", "champ_id": "B2O3_x010",
                    "ranked_dopant": "B2O3"},
    },
}


def f(x):
    try:
        return round(float(x), 4)
    except Exception:
        return None


def sec(status, **kw):
    d = {"status": status}
    d.update(kw)
    return d


def build_screening(sysmeta):
    c = sysmeta.get("cascade")
    if not c:
        return sec("n.a.", source="—")
    champ = cascade_row("cascade_v23_champions.csv", "_dir", c["champ_id"])
    li = cascade_row("cascade_v23_litransport.csv", "_dir", c["champ_id"])
    rk = cascade_row("cascade_v23_ranked.csv", "dopant", c["ranked_dopant"])
    ox = cascade_row("oxidation_stability_cascade.csv", "dopant", c["ranked_dopant"])
    desc = {}
    if li:
        desc = {"bvs_li_proxy_score": f(li.get("bvs_li_proxy_score")),
                "migration_volume_fraction": f(li.get("migration_volume_fraction")),
                "blocking_fraction": f(li.get("tier2_dopant_blocking_fraction")),
                "li_li_disorder_std": f(li.get("tier2_li_li_disorder_std")),
                "cation_site": li.get("cation_site"), "anion_site": li.get("anion_site")}
    est = {}
    if champ:
        est.update({"eos_B0_GPa": f(champ.get("eos_B0_GPa")),
                    "elastic_E_GPa": f(champ.get("elastic_E_young_GPa")),
                    "elastic_nu": f(champ.get("elastic_poisson_nu")),
                    "pugh_GoverB": f(champ.get("elastic_pugh_GoverB"))})
    if ox:
        est.update({"ox_V": f(ox.get("ox_V")), "red_V": f(ox.get("red_V")),
                    "window_V": f(ox.get("window_V"))})
    return sec("done", source_pipeline=c["version"], candidate_id=c["champ_id"],
               rank=int(rk["rank"]) if rk else (1 if champ else None),
               score=f(champ.get("combined_score")) if champ else (f(rk.get("score")) if rk else None),
               descriptors=desc, cascade_fast_estimates=est,
               confidence="C", method="cascade tier descriptors (fast proxy)",
               caveats="fast screening estimate; deep-validation sections below are high-fidelity. "
                       "cascade evolves -> re-link by (version, candidate_id).")


def build(sysid):
    m = SYSTEMS[sysid]
    md = jload("b2o3_vs_modelc_md.json")
    mdb = (md or {}).get("b2o3_doped", {})
    hull = jload("b2o3_ehull_result.json") or {}
    hb = hull.get("b2o3_doped", {})
    esw = (jload("b2o3_esw.json") or {}).get("b2o3", {})
    sei = jload("b2o3_sei_gaps.json") or {}
    seigaps = sei.get("sei_gaps_MP_eV", {})
    phon = jload("b2o3_phonon_stability.json") or {}
    eos = jload("b2o3_eos_dft_result.json") or {}
    bonds = jload("b2o3_bond_lengths.json") or {}

    card = {
        "schema_version": "0.1",
        "generated_utc": "STAMP_AT_CALLER",
        "system": {k: m[k] for k in ("id", "composition", "structure_ref", "n_atoms", "provenance")},
        "screening": build_screening(m),
        "transport": sec("done", confidence="B",
            method="UMA-s-1p1 MLIP-MD, MSD window 2-50 ps, 3pt Arrhenius, Nernst-Einstein (Haven=1)",
            source="db/properties/b2o3_vs_modelc_md.json + kb/methodology/md_conductivity_protocol.md",
            sigma_300K_mS_cm=f(mdb.get("sigma_300K_mS_cm")), sigma_273K_mS_cm=f(mdb.get("sigma_273K_mS_cm")),
            Ea_eV=f(mdb.get("Ea_eV")), D0_cm2_s=f(mdb.get("D0_cm2_s")),
            caveats="MLIP NE overestimates absolute sigma ~3-5x; Ea + relative-vs-modelc robust. "
                    "vs modelc (LPSCl1.6): same Ea, ~1.33x higher sigma (D0-driven)."),
        "thermodynamic_stability": sec("done", confidence="B",
            method="UMA-consistent convex hull (e_above_hull), MP chemsys " + str(hull.get("b2o3_doped", {}).get("chemsys", "")),
            source="db/properties/b2o3_ehull_result.json",
            e_above_hull_meV_atom=f(hb.get("E_above_hull_meV_atom")),
            decomposition=hb.get("decomposition"),
            caveats="metastable (+37.5 meV/atom) but phonon-stable real phase; decomp includes Li3BS3 (BS3 thioborate)."),
        "electrochemical_window": sec("done", confidence="B",
            method="grand-potential ESW (MP GGA/GGA+U hull) + MP band gaps of SEI products",
            source="db/properties/b2o3_esw.json + b2o3_sei_gaps.json",
            esw_reduction_V=f(esw.get("reduction_V")), esw_oxidation_V=f(esw.get("oxidation_V")),
            window_V=f(esw.get("window_V")),
            sei_products=[{"phase": k, "gap_eV": v, "passivating": v >= 4.0}
                          for k, v in sorted(seigaps.items(), key=lambda x: -x[1])][:8],
            caveats="window narrows (1.72-2.03 V) but SEI is wide-gap passivating (B2O3 8.4, BPO4 7.0, Li3PO4 5.7) -> e- blocking."),
        "mechanical": sec("pending", confidence=None,
            method="DFT relaxed-ion finite-strain Cij (running on KISTI); EOS B0 as proxy",
            source="db/properties/b2o3_eos_dft_result.json (B0); elastic Cij pending",
            B_GPa=None, G_GPa=None, E_GPa=None, nu=None, B0_eos_GPa=f(eos.get("B0_GPa")),
            caveats="elastic relaxed-ion 12-strain chain running; cascade fast-estimate E~41-43 GPa (screening). "
                    "EOS B0 24.5 GPa (+13% vs undoped, DFT)."),
        "electronic": sec("done", confidence="A",
            method="DFT DOS/PDOS (scf->nscf->projwfc)",
            source="db/properties/b2o3_dos_smooth.csv + b2o3_pdos_*_smooth.csv; kb/results b2o3 DOS",
            band_gap_eV=1.97, N_EF=0.0, vbm_character="S 3p ~89.5% (free-S shallowest)",
            caveats="gap 1.97 eV (VBM 2.47 / CBM 4.44); insulating bulk."),
        "structure_chemistry": sec("done", confidence="A",
            method="coordination/bond-length + Bader (oxidation) + Lowdin (S-site order)",
            source="db/properties/b2o3_bond_lengths.json + b2o3_charge_xps.csv + b2o3_coordination_bonds.json",
            coordination_motifs=["trigonal BS3 (B-S 1.83)", "free-S2- (6)", "phosphate P-O (1.56, PS4-xOx)"],
            bond_lengths={k: v.get("mean") for k, v in (bonds.get("bonds", {}) or {}).items()},
            oxidation_states={"B": "+3.00", "P": "+4.69", "O": "-1.92", "Cl": "-0.91", "Li": "+0.88", "S": "~-1.8"},
            caveats="BS3 confirmed 5 ways (coord/hull/DOS/ESW/charge). USPP charges = relative."),
        "dynamical_stability": sec("done", confidence="B",
            method="UMA Gamma-point finite-displacement phonons",
            source="db/properties/b2o3_phonon_stability.json",
            imaginary_modes=phon.get("imaginary_below_-30_cm"),
            verdict="DYNAMICALLY STABLE (0 imaginary; soft Li band ~14 cm-1)",
            caveats="Gamma-only (UMA); qualitative stability robust; quantitative Raman/IR needs DFPT."),
        "testable_predictions": sec("done", confidence="B",
            method="aggregated fingerprints for experimental validation",
            source="derived from structure_chemistry + dynamical_stability",
            xps=["S 2p: free-S2-(low BE) < PS4-S < B-S/BS3(high BE shoulder)", "B 1s B3+", "P 2p P5+ (PS4-xOx)"],
            raman_ir=["P-O phosphate stretch ~900-1013 cm-1 (absent in undoped)"],
            nmr=["11B trigonal BS3", "31P PS4 / PS4-xOx", "7Li"],
            caveats="positions/order computable; Nd 3d is literature-only (multiplet). Quantitative XPS eV needs dSCF core-hole."),
    }
    # completeness + overall
    secs = ["screening", "transport", "thermodynamic_stability", "electrochemical_window",
            "mechanical", "electronic", "structure_chemistry", "dynamical_stability", "testable_predictions"]
    done = sum(1 for s in secs if card[s]["status"] == "done")
    card["overall"] = {
        "summary": "B2O3-doped LPSCl1.6 champion (cascade rank-1): higher RT conductivity than undoped "
                   "(sigma300 ~18.5 mS/cm, same Ea, D0-driven), metastable but phonon-stable, narrow ESW "
                   "compensated by wide-gap passivating B/O SEI, stiffer framework (EOS B0 +13%). Promising dopant.",
        "flags": ["transport:+", "stability:metastable(+37.5)", "ESW:narrow-but-SEI-compensated",
                  "dynamical:stable", "mechanical:pending"],
        "honesty_notes": ["absolute sigma is MLIP upper bound (cite Ea+ratio)",
                          "elastic Cij pending (KISTI); EOS B0 proxy",
                          "single Li-config", "cascade fast-estimates vs deep-validation differ (seeds ML calibration)"],
        "completeness": f"{done}/{len(secs)} sections done",
    }
    return card


def to_md(card):
    s = card["system"]; o = card["overall"]; sc = card.get("screening", {})
    L = [f"# Report card — {s['id']} ({s['composition']})",
         f"\n**구조** `{s['structure_ref']}` ({s.get('n_atoms')} atom) · {s.get('provenance','')}",
         f"**완성도** {o['completeness']} · schema {card['schema_version']}",
         f"\n> {o['summary']}\n",
         "## Screening (upstream cascade)"]
    if sc.get("status") == "done":
        L.append(f"- **{sc['source_pipeline']} / {sc['candidate_id']}** rank={sc.get('rank')} score={sc.get('score')}")
        L.append(f"- descriptors: {sc.get('descriptors')}")
        L.append(f"- cascade fast-est: {sc.get('cascade_fast_estimates')}  ⚠ {sc.get('caveats','')}")
    L.append("\n## 검증 섹션 (deep validation)")
    L.append("| 섹션 | status | conf | 핵심값 |")
    L.append("|---|---|---|---|")
    def kv(d, keys):
        return ", ".join(f"{k}={d.get(k)}" for k in keys if d.get(k) is not None)
    rows = [
        ("transport", ["sigma_300K_mS_cm", "sigma_273K_mS_cm", "Ea_eV"]),
        ("thermodynamic_stability", ["e_above_hull_meV_atom"]),
        ("electrochemical_window", ["esw_reduction_V", "esw_oxidation_V", "window_V"]),
        ("mechanical", ["E_GPa", "B_GPa", "G_GPa", "nu", "B0_eos_GPa"]),
        ("electronic", ["band_gap_eV", "N_EF", "vbm_character"]),
        ("structure_chemistry", ["coordination_motifs"]),
        ("dynamical_stability", ["imaginary_modes", "verdict"]),
        ("testable_predictions", ["xps", "raman_ir", "nmr"]),
    ]
    for name, keys in rows:
        d = card[name]
        L.append(f"| {name} | {d['status']} | {d.get('confidence') or '-'} | {kv(d, keys)[:90]} |")
    L.append("\n## 정직한 한계")
    for n in o["honesty_notes"]:
        L.append(f"- {n}")
    L.append("\n*Generated by `factory/assemble_report_card.py` (v1 foundation). "
             "Sections marked pending are validated by the running orchestrator stages.*")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("system", choices=list(SYSTEMS))
    args = ap.parse_args()
    card = build(args.system)
    CARDS.mkdir(parents=True, exist_ok=True)
    (CARDS / f"{args.system}_report_card.json").write_text(json.dumps(card, indent=2, ensure_ascii=False))
    (CARDS / f"{args.system}_report_card.md").write_text(to_md(card))
    print(f"-> factory/cards/{args.system}_report_card.json + .md  ({card['overall']['completeness']})")


if __name__ == "__main__":
    main()
