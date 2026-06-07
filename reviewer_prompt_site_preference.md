# Reviewer prompt — site_preference.py literature-override change

You are reviewing a change to a DFT/MLIP materials-screening pipeline that picks
which crystallographic site a dopant substitutes in Li6PS5Cl argyrodite solid
electrolyte. Files in scope: `scripts/doping/site_preference.py` (changed) and
`scripts/doping/substitute_struct.py` (downstream consumer, unchanged but coupled).

## CONTEXT
- The pipeline screens ~273 dopant/compound cases. `site_preference.py` is the
  Tier-1 (no-DFT) filter that, for each dopant, returns candidate host sites
  (`Li_24g`/`Li_48h`, `P_4b` = PS4 center, `S_16e`/`S_4a`, `Cl_4d`).
  `substitute_struct.py` then GENERATES a structure for every returned site ×
  concentration × seed, applies charge compensation, and hands them to UMA/DFT
  relaxation + energy ranking.
- PREVIOUS behaviour: a per-site radius cutoff (`RADIUS_TOL`) decided admission.
  Problem found: it silently EXCLUDED literature-reported cases (e.g. Y3+→P5+,
  |Δr|=0.73 > P cutoff 0.55), so those sites were never generated/tested.
- THIS CHANGE: added `KNOWN_SUBSTITUTIONS` (element → {site: (evidence, ref)}),
  tagged by evidence strength (`dft_exp` / `exp` / `analog` / `rietveld`). The
  filter now admits literature sites REGARDLESS of the radius cutoff
  (`source='literature'`), uses the radius heuristic only for the rest
  (`source='heuristic'`), and is unchanged when no `element` is passed. Intent:
  don't trust weak claims blindly — GENERATE them so our own UMA/DFT can confirm
  or REFUTE by energy.

## PLEASE CRITICALLY EVALUATE
1. **Scientific validity of the `KNOWN_SUBSTITUTIONS` table**: are the site
   assignments and evidence levels defensible against the cited literature?
   Is Y3+→P5+ correctly down-weighted as `rietveld` (XRD-only, dilute dopant =
   poorly separable Y@P vs Y@Li)? Any assignment that is wrong or mis-tagged?
   Any well-known case MISSING (e.g. Ta5+/Bi5+→P; La/In/Ga; isovalent S/Cl set)?
2. **Over-/under-admission**: does literature-bypass-cutoff risk admitting an
   UNPHYSICAL site for any element? Does the radius heuristic still correctly
   reject un-studied large cations (Sc stays Li-only — right)?
3. **\*\*\* Coupling with charge compensation (highest priority) \*\*\***:
   `substitute_struct.apply_charge_compensation` leaves ACCEPTOR cases
   (`delta_q<0`) as `'imbalanced_{delta_q}'` (Li-interstitial insertion is a
   TODO). Y3+→P5+ is a −2 acceptor. So does adding Y→P generate a
   CHARGE-UNBALANCED structure, which UMA/DFT would then score as high-energy for
   the WRONG reason (bad compensation, not bad site) — i.e. we'd "refute" Y→P
   spuriously? Assess whether the literature-override is meaningful for acceptor
   P-site dopants until acceptor compensation is implemented.
4. **Code correctness**: backward compatibility (`element=None` path), the
   literature-first sort order and any downstream effect on generation order in
   `substitute_struct.generate_for_dopant`, the charge-sign sanity check on
   literature entries, dict/tuple unpacking, and whether evidence should GATE
   behaviour (e.g. skip generating `rietveld` in production runs) rather than
   only annotate.
5. **Design**: should `KNOWN_SUBSTITUTIONS` live in code or a versioned data
   file? Is the evidence taxonomy sufficient/auditable?

Give concrete, prioritized findings. Flag anything that would silently corrupt
the screening (wrong site generated, or right site generated but unfairly
scored). Do not rubber-stamp.
