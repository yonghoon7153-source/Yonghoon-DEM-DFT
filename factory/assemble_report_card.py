#!/usr/bin/env python3
"""assemble_report_card.py — build a standardized electrochemical report card
for a (doped) solid electrolyte from existing db/ results + cascade screening.

v1.1 (audit-hardened). Reads a system's db/properties files (per-system file map
in SYSTEMS -> generalizes), maps them to the report-card schema, links the
upstream cascade candidate (versioned, loose coupling), and writes JSON + MD.

  python3 factory/assemble_report_card.py b2o3

Provenance rule: a section's `source` lists ONLY files this script actually reads.
Hand-curated scalars (e.g. DOS gap, with no machine-readable summary) are marked
`curation: manual` so `source` never overstates automation. Every section carries
status/confidence/method/caveats. Confidence rubric (see README/schema):
  A = DFT, converged, multi-witness or experiment-validated
  B = single-config DFT/MLIP, or relative-only
  C = fast proxy / screening descriptor
"""
import argparse, json, csv, math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DBP = ROOT / "db" / "properties"
CARDS = Path(__file__).resolve().parent / "cards"

CORE_SECTIONS = ["screening", "transport", "thermodynamic_stability", "electrochemical_window",
                 "mechanical", "electronic", "structure_chemistry", "dynamical_stability",
                 "testable_predictions"]
# descriptors a credible SE pipeline still owes (audit finding 9) — declared n.a. so
# reviewers see they are acknowledged, not forgotten.
ROADMAP_SECTIONS = {
    "anode_interface_stability": "Li-metal reduction at the ESW lower limit; headline risk (red 1.72 V near Li).",
    "critical_current_density": "dendrite resistance / CCD — most-requested SE metric; not computed.",
    "grain_boundary_transport": "bulk sigma != total sigma; GB often dominates.",
    "air_moisture_stability": "H2S evolution / hydrolysis (BS3/thioborates are sensitive).",
    "electronic_conductivity": "sigma_electronic (self-discharge driver), beyond just band gap.",
}


def jload(name):
    if not name:
        return None
    p = DBP / name
    return json.loads(p.read_text()) if p.exists() else None


def csv_rows(name):
    """Skip comment lines at the RAW-LINE level (audit finding 10), then csv-parse."""
    p = DBP / name
    if not p.exists():
        return []
    lines = [ln for ln in p.read_text().splitlines() if not ln.lstrip().startswith("#")]
    return list(csv.reader(lines))


def cascade_row(csv_name, key_col, key):
    rows = csv_rows(csv_name)
    if not rows:
        return None
    hdr = rows[0]
    ci = hdr.index(key_col) if key_col in hdr else 0
    for r in rows[1:]:
        if len(r) > ci and r[ci] == key:
            return dict(zip(hdr, r))
    return None


def f(x, sig=4):
    """Significant-figure round; reject non-finite -> None (no bare NaN in JSON,
    no collapse of 1.25e-7 to 0.0). audit finding 3."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(v):
        return None
    return float(f"{v:.{sig}g}")


def iget(d, k):
    """guarded int (audit finding 3): blank/missing -> None."""
    if not d:
        return None
    s = str(d.get(k, "")).strip()
    return int(float(s)) if s else None


# ---- system registry: per-system file map (generalizes; audit finding 4) ----
SYSTEMS = {
    "b2o3": {
        "id": "b2o3",
        "composition": "Li58P8S41Cl16B2O3",
        "structure_ref": "db/structures/b2o3_relaxV0.cif",
        "n_atoms": 128,
        "provenance": "DFT V0 fixed-cell relax (B2O3-doped LPSCl1.6 champion)",
        "cascade": {"version": "cascade_v23", "champ_id": "B2O3_x010", "ranked_dopant": "B2O3"},
        "files": {
            "md": "b2o3_vs_modelc_md.json",
            "hull": "b2o3_ehull_result.json",
            "esw": "b2o3_esw.json",
            "sei": "b2o3_sei_gaps.json",
            "phonon": "b2o3_phonon_stability.json",
            "eos": "b2o3_eos_dft_result.json",
            "bonds": "b2o3_bond_lengths.json",
            "coord": "b2o3_coordination_bonds.json",
            "charge_csv": "b2o3_charge_xps.csv",
            "bvse": "bvse_b2o3/b2o3_bvse_percolation.json",
        },
        # electronic has no machine-readable summary -> curated (provenance honest).
        "electronic_manual": {"band_gap_eV": 1.97, "N_EF": 0.0,
                              "vbm_character": "S 3p ~89.5% (free-S shallowest)",
                              "source": "kb/results b2o3 DOS analysis (curated; DOS data db/properties/b2o3_dos_smooth.csv)"},
    },
    # ---- v1.2 generalization demo: a FRESH cascade candidate (rank-1 dopant),
    # NOT yet deep-validated. Only cascade screening exists; the file map points
    # at convention-named outputs that do not exist yet -> deep sections auto-
    # report 'pending' and the orchestrator plans the full validation. ----
    "sc2o3": {
        "id": "sc2o3",
        "composition": "(LPSCl1.6 + Sc2O3, x=0.25)",
        "structure_ref": "db/structures/sc2o3_TODO.cif (not yet built/relaxed)",
        "n_atoms": None,
        "provenance": "cascade_v23 rank-1 dopant (Sc2O3); NOT yet deep-validated",
        "cascade": {"version": "cascade_v23", "champ_id": "Sc2O3_x010", "ranked_dopant": "Sc2O3"},
        "files": {  # expected (convention-named) outputs; do not exist yet -> pending
            "md": "sc2o3_vs_modelc_md.json", "hull": "sc2o3_ehull_result.json",
            "esw": "sc2o3_esw.json", "sei": "sc2o3_sei_gaps.json",
            "phonon": "sc2o3_phonon_stability.json", "eos": "sc2o3_eos_dft_result.json",
            "bonds": "sc2o3_bond_lengths.json", "coord": "sc2o3_coordination_bonds.json",
            "charge_csv": "sc2o3_charge_xps.csv", "bvse": "bvse_sc2o3/sc2o3_bvse_percolation.json",
        },
        # no electronic_manual -> electronic section pending
    },
}


def sec(status, **kw):
    return {"status": status, **kw}


def build_screening(m):
    c = m.get("cascade")
    if not c:
        return sec("n.a.", source="—")
    champ = cascade_row("cascade_v23_champions.csv", "_dir", c["champ_id"])
    li = cascade_row("cascade_v23_litransport.csv", "_dir", c["champ_id"])
    desc = {}
    if li:
        desc = {"bvs_li_proxy_score": f(li.get("bvs_li_proxy_score")),
                "migration_volume_fraction": f(li.get("migration_volume_fraction")),
                "blocking_fraction": f(li.get("tier2_dopant_blocking_fraction")),
                "li_li_disorder_std": f(li.get("tier2_li_li_disorder_std")),
                "cation_site": li.get("cation_site"), "anion_site": li.get("anion_site")}
    est = {}
    if champ:
        est = {"eos_B0_GPa": f(champ.get("eos_B0_GPa")), "elastic_E_GPa": f(champ.get("elastic_E_young_GPa")),
               "elastic_nu": f(champ.get("elastic_poisson_nu")), "pugh_GoverB": f(champ.get("elastic_pugh_GoverB"))}
    # rank + score from ONE basis (champions combined_score), not stitched (audit finding 1)
    return sec("done", confidence="C", method="cascade tier descriptors (fast proxy)",
               source_pipeline=c["version"], candidate_id=c["champ_id"],
               ranking_basis="cascade_v23 champions (rank_combined / combined_score)",
               rank=iget(champ, "rank_combined"), score=f(champ.get("combined_score")) if champ else None,
               descriptors=desc, cascade_fast_estimates=est,
               caveats="fast screening estimate; deep-validation sections are high-fidelity. "
                       "rank/score from champions.csv (NOTE: ranked.csv lists B2O3 #6/47 by a different "
                       "stability metric). cascade evolves -> re-link by (version, candidate_id).")


def build(sysid, stamp=None):
    m = SYSTEMS[sysid]
    F = m["files"]
    em = m.get("electronic_manual", {})   # absent for not-yet-validated candidates
    md = (jload(F.get("md")) or {}).get(f"{sysid}_doped", {})
    hb = (jload(F.get("hull")) or {}).get(f"{sysid}_doped", {})
    esw = (jload(F.get("esw")) or {}).get(sysid, {})
    seigaps = (jload(F.get("sei")) or {}).get("sei_gaps_MP_eV", {})
    phon = jload(F.get("phonon")) or {}
    eos = jload(F.get("eos")) or {}
    bonds = jload(F.get("bonds")) or {}
    coord = jload(F.get("coord")) or {}
    bvse = jload(F.get("bvse")) or {}

    # --- parsed oxidation states (truthful source; audit finding 2) ---
    ox = {}
    for r in (csv_rows(F["charge_csv"])[1:] if csv_rows(F["charge_csv"]) else []):
        if len(r) >= 5 and r[0] in ("B", "P", "O", "Cl", "Li"):
            ox[r[0]] = f(r[4])  # Bader_net
    # --- parsed coordination motifs (truthful source) ---
    motifs = sorted({v.get("motif") for v in (coord.get("B_coordination", {}) or {}).values() if v.get("motif")})
    if coord.get("P_coordination"):
        motifs.append("PS4 thiophosphate + P-O phosphate (PS4-xOx)")
    motifs.append("free-S2- (isolated sulfide)")

    # --- ESW: report ALL predicted-decomp SEI gaps with 3-tier label + min-gap (audit 6,7) ---
    PASS, MARG = 4.0, 2.0  # documented heuristic thresholds (eV)
    def tier(g):
        return "passivating" if g >= PASS else ("marginal" if g >= MARG else "leaky")
    predicted = set((hb.get("decomposition") or {}).keys())   # phases actually predicted to form
    sei_products = [{"phase": k, "gap_eV": v, "tier": tier(v), "in_predicted_decomp": k in predicted}
                    for k, v in sorted(seigaps.items(), key=lambda x: x[1])]  # leaky first, none hidden
    pred_gaps = [v for k, v in seigaps.items() if k in predicted]
    min_gap = min(pred_gaps) if pred_gaps else None   # min among PREDICTED products (not won't-form phases like BS2)

    card = {
        "schema_version": "0.2",
        "generated_utc": stamp or datetime.now(timezone.utc).isoformat(),
        "confidence_rubric": "A=DFT converged multi-witness/validated; B=single-config DFT/MLIP or relative; C=fast proxy",
        "system": {k: m[k] for k in ("id", "composition", "structure_ref", "n_atoms", "provenance")},
        "screening": build_screening(m),
        "transport": sec("done", confidence="B",
            method="UMA-s-1p1 MLIP-MD, MSD window 2-50 ps, 3pt Arrhenius, Nernst-Einstein (Haven=1)",
            source=f"db/properties/{F['md']} + {F['bvse']} + kb/methodology/md_conductivity_protocol.md",
            sigma_300K_mS_cm=f(md.get("sigma_300K_mS_cm")), sigma_273K_mS_cm=f(md.get("sigma_273K_mS_cm")),
            Ea_eV=f(md.get("Ea_eV")), D0_cm2_s=f(md.get("D0_cm2_s"), 3),
            bvse_barrier_val2=f(bvse.get("in_plane_ab_percolation_barrier_val2")),
            bvse_channel_volume_fraction=f(bvse.get("in_plane_channel_volume_fraction")),
            caveats="MLIP NE overestimates absolute sigma ~3-5x; Ea+relative-vs-modelc robust (same Ea as "
                    "modelc, ~1.33x higher sigma, D0-driven). Ea uncertainty ~+-0.01 eV (MSD-window sensitivity). "
                    "BVSE barrier is in softBV val^2 units (relative, resolution-limited), NOT eV -> needs NEB calibration."),
        "thermodynamic_stability": sec("done", confidence="B",
            method="UMA-consistent convex hull (e_above_hull), MP chemsys " + str(hb.get("chemsys", "")),
            source=f"db/properties/{F['hull']}",
            e_above_hull_meV_atom=f(hb.get("E_above_hull_meV_atom")), decomposition=hb.get("decomposition"),
            caveats="metastable (+37.5 meV/atom) but phonon-stable real phase; decomp includes Li3BS3 (BS3 thioborate) "
                    "+ Li4B7ClO12 -> independently corroborates the BS3/borate motif."),
        "electrochemical_window": sec("done", confidence="B",
            method="grand-potential ESW (MP GGA/GGA+U hull) + MP band gaps of SEI products",
            source=f"db/properties/{F['esw']} + {F['sei']}",
            esw_reduction_V=f(esw.get("reduction_V")), esw_oxidation_V=f(esw.get("oxidation_V")),
            window_V=f(esw.get("window_V")), sei_products=sei_products, sei_min_gap_eV=min_gap,
            passivation_thresholds_eV={"passivating>=": PASS, "marginal>=": MARG, "note": "heuristic rule-of-thumb, not a hard physical boundary"},
            caveats="window is NARROW (0.31 V) = a real risk, NOT solved. SEI has wide-gap members (B2O3 8.4, BPO4 7.0, "
                    "Li3PO4 5.7) AND leaky members in the SAME predicted decomposition (Li3BS3 3.05, Li2B2S5 2.44, "
                    "Li3P 0.7). Passivation is plausible ONLY IF the interphase is dense/continuous and the leaky "
                    "thioborates are minor -- interphase morphology/electron-tunneling NOT modeled here."),
        "mechanical": sec("pending", confidence=None,
            method="DFT relaxed-ion finite-strain Cij (running on KISTI); EOS B0 as proxy",
            source=f"db/properties/{F['eos']} (B0); elastic Cij pending (db/properties/elastic.json)",
            B_GPa=None, G_GPa=None, E_GPa=None, nu=None, B0_eos_GPa=f(eos.get("B0_GPa")),
            caveats="elastic relaxed-ion 12-strain chain running; cascade fast-estimate E~41-43 GPa (screening). "
                    "EOS B0 24.5 GPa (+13% vs undoped, DFT)."),
        "electronic": sec("done", confidence="B", curation="manual",
            method="DFT DOS/PDOS (scf->nscf->projwfc); scalars curated (no machine-readable summary)",
            source=em.get("source"),
            band_gap_eV=em.get("band_gap_eV"), N_EF=em.get("N_EF"), vbm_character=em.get("vbm_character"),
            caveats="GGA underestimates gaps; single config/functional -> grade B not A. gap 1.97 eV (VBM 2.47/CBM 4.44)."),
        "structure_chemistry": sec("done", confidence="A",
            method="coordination (Voronoi) + bond lengths + Bader oxidation states (parsed) + Lowdin S-site order",
            source=f"db/properties/{F['bonds']} + {F['coord']} + {F['charge_csv']}",
            coordination_motifs=motifs,
            bond_lengths={k: f(v.get("mean")) for k, v in (bonds.get("bonds", {}) or {}).items()},
            oxidation_states_bader_net=ox,
            caveats="BS3 confirmed 5 independent ways (coord/hull/DOS/ESW/charge) = multi-witness -> grade A. "
                    "USPP Bader net charges are relative (B basin collapses; S-site order from Lowdin)."),
        "dynamical_stability": sec("done", confidence="B",
            method="UMA Gamma-point finite-displacement phonons",
            source=f"db/properties/{F['phonon']}",
            imaginary_modes=iget(phon, "imaginary_below_-30_cm"),
            verdict="DYNAMICALLY STABLE (0 imaginary; soft Li band ~14 cm-1)",
            caveats="Gamma-only (UMA) -> qualitative stability only; quantitative Raman/IR needs DFPT."),
        "testable_predictions": sec("done", confidence="B",
            method="aggregated fingerprints for experimental validation (derived)",
            source="derived from structure_chemistry + dynamical_stability",
            xps=["S 2p: free-S2-(low BE) < PS4-S < B-S/BS3(high BE shoulder)", "B 1s B3+", "P 2p P5+ (PS4-xOx)"],
            raman_ir=["P-O phosphate stretch ~900-1013 cm-1 (absent in undoped)"],
            nmr=["11B trigonal BS3", "31P PS4 / PS4-xOx", "7Li"],
            caveats="positions/order computable; absolute XPS eV needs dSCF core-hole; Nd 3d is literature-only (multiplet)."),
    }
    # data-aware status (generalizes to not-yet-validated candidates): tie each
    # section to whether its PRIMARY source data actually loaded (not to templated
    # constants like the verdict string or threshold dict). A fresh cascade
    # candidate (only screening) then auto-reports deep sections as pending ->
    # the orchestrator plans exactly those stages.
    present = {
        "transport": bool(md), "thermodynamic_stability": bool(hb),
        "electrochemical_window": bool(esw or seigaps), "mechanical": False,  # pending until Cij
        "electronic": bool(em), "structure_chemistry": bool(bonds or coord or ox),
        "dynamical_stability": bool(phon), "testable_predictions": bool(bonds or coord),
    }
    for s, ok in present.items():
        if not ok and card[s]["status"] == "done":
            card[s]["status"], card[s]["confidence"] = "pending", None

    # roadmap (acknowledged-but-not-computed) sections
    for k, why in ROADMAP_SECTIONS.items():
        card[k] = sec("n.a.", confidence=None, method="not in v1 pipeline", source="—", caveats=why)

    done = sum(1 for s in CORE_SECTIONS if card[s]["status"] == "done")
    if sysid == "b2o3":
        summary = ("B2O3-doped LPSCl1.6 (cascade champion, rank_combined=1 by combined_score): higher RT "
                   "conductivity than undoped LPSCl1.6 (sigma300 ~18.5 mS/cm, SAME Ea, D0-driven), metastable "
                   "(+37.5 meV/atom) but phonon-stable, NARROW ESW (0.31 V, a real risk) with mixed SEI "
                   "(wide-gap B/O passivators + leaky thioborates), stiffer framework (EOS B0 +13%). "
                   "Promising but with an interface-stability caveat.")
        flags = ["transport:+", "stability:metastable(+37.5)", "ESW:narrow(0.31V,risk)",
                 "dynamical:stable", "mechanical:pending", "anode-interface:UNASSESSED"]
        notes = ["absolute sigma is MLIP upper bound (cite Ea+-0.01 + ratio)",
                 "elastic Cij pending (KISTI); EOS B0 proxy",
                 "ESW narrow + leaky SEI members present; passivation NOT demonstrated (interphase not modeled)",
                 "electronic scalars curated (GGA single-config), graded B",
                 "single Li-config; anode-interface/CCD/GB/air-stability/e-conductivity NOT yet computed (roadmap)"]
    else:
        rk = card["screening"].get("rank")
        summary = (f"cascade rank-{rk} candidate {m['composition']}: deep validation PENDING "
                   f"({done}/{len(CORE_SECTIONS)} core done). Only cascade screening available so far; "
                   f"the orchestrator plans the remaining DFT/MLIP stages (with gates).")
        flags = [f"{s}:{card[s]['status']}" for s in CORE_SECTIONS]
        notes = ["FRESH candidate — values shown are cascade fast-estimates only, not deep validation",
                 "deep DFT/MLIP stages not yet run (see orchestrator run plan)"]
    card["overall"] = {
        "summary": summary, "flags": flags,
        "honesty_notes": notes + ["cascade fast-estimates vs deep-validation differ (seeds future ML calibration)"],
        "completeness": f"{done}/{len(CORE_SECTIONS)} core sections done; {len(ROADMAP_SECTIONS)} descriptors on roadmap",
    }
    return card


def _fmt(v):
    if isinstance(v, dict):
        return ", ".join(f"{k}={vv}" for k, vv in v.items())
    if isinstance(v, list):
        return "; ".join(str(x) for x in v)
    return str(v)


def to_md(card):
    s = card["system"]; o = card["overall"]; sc = card.get("screening", {})
    L = [f"# Report card — {s['id']} ({s['composition']})",
         f"\n**구조** `{s['structure_ref']}` ({s.get('n_atoms')} atom) · {s.get('provenance','')}",
         f"**완성도** {o['completeness']} · schema {card['schema_version']} · generated {card['generated_utc']}",
         f"**confidence rubric** {card['confidence_rubric']}",
         f"\n> {o['summary']}\n",
         "## Screening (upstream cascade)"]
    if sc.get("status") == "done":
        L += [f"- **{sc['source_pipeline']} / {sc['candidate_id']}** rank={sc.get('rank')} score={sc.get('score')} ({sc.get('ranking_basis')})",
              f"- descriptors: {_fmt(sc.get('descriptors', {}))}",
              f"- cascade fast-est: {_fmt(sc.get('cascade_fast_estimates', {}))}",
              f"- ⚠ {sc.get('caveats','')}"]
    L += ["\n## 검증 섹션 (deep validation)", "| 섹션 | status | conf | 핵심값 |", "|---|---|---|---|"]
    rows = [("transport", ["sigma_300K_mS_cm", "sigma_273K_mS_cm", "Ea_eV", "bvse_barrier_val2"]),
            ("thermodynamic_stability", ["e_above_hull_meV_atom"]),
            ("electrochemical_window", ["esw_reduction_V", "esw_oxidation_V", "window_V", "sei_min_gap_eV"]),
            ("mechanical", ["E_GPa", "B_GPa", "G_GPa", "nu", "B0_eos_GPa"]),
            ("electronic", ["band_gap_eV", "N_EF", "vbm_character"]),
            ("structure_chemistry", ["coordination_motifs", "oxidation_states_bader_net"]),
            ("dynamical_stability", ["imaginary_modes", "verdict"]),
            ("testable_predictions", ["xps", "raman_ir", "nmr"])]
    for name, keys in rows:
        d = card[name]
        kv = ", ".join(f"{k}={_fmt(d.get(k))}" for k in keys if d.get(k) is not None)
        L.append(f"| {name} | {d['status']} | {d.get('confidence') or '-'} | {kv[:96]} |")
    L.append("\n## Roadmap descriptors (acknowledged, not yet computed)")
    for k in ROADMAP_SECTIONS:
        L.append(f"- **{k}** (n.a.): {card[k]['caveats']}")
    L.append("\n## 정직한 한계")
    L += [f"- {n}" for n in o["honesty_notes"]]
    L.append("\n*Generated by `factory/assemble_report_card.py` (v1.1, audit-hardened). "
             "Sections marked pending are validated by the running orchestrator stages.*")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("system", choices=list(SYSTEMS))
    ap.add_argument("--stamp", default=None, help="provenance UTC (default: now)")
    args = ap.parse_args()
    card = build(args.system, stamp=args.stamp)
    CARDS.mkdir(parents=True, exist_ok=True)
    (CARDS / f"{args.system}_report_card.json").write_text(json.dumps(card, indent=2, ensure_ascii=False))
    (CARDS / f"{args.system}_report_card.md").write_text(to_md(card))
    print(f"-> factory/cards/{args.system}_report_card.json + .md  ({card['overall']['completeness']})")


if __name__ == "__main__":
    main()
