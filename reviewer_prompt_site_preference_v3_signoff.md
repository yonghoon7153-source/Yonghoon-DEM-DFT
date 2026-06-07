# Reviewer prompt v3 — FINAL sign-off pass (go / no-go)

You are giving the **final** review of a change to a DFT/MLIP dopant-screening
pipeline for Li6PS5Cl argyrodite. This change has already been through TWO review
cycles; the findings of both were fixed. Your job is to confirm the fixes are
correct and then **make a decision**: either approve it for production with an
explicit sign-off, or name the specific remaining blocker(s). This is meant to be
the last pass — be decisive, and do not invent nitpicks that would not actually
corrupt results.

Files in scope: `scripts/doping/site_preference.py`,
`scripts/doping/substitute_struct.py`, `scripts/doping/analyze_screening.py`,
and the regenerated `db/doping/site_preference_initial.json` /
`data/doping_screening/site_preference_initial.json`. Run the code if useful
(deps: ase, numpy, scipy). Base structure: `db/structures/comp1_V0_k444.cif`.

## Full history (what was built, then fixed)
The change makes literature-reported dopant sites override a radius cutoff
(`RADIUS_TOL`) that was silently dropping real cases (e.g. Y3+→P5+). Sites carry an
evidence tag (`dft_exp`/`exp`/`analog`/`rietveld`); weak claims are generated so
the pipeline's own UMA/DFT can confirm/refute them by energy.

Review cycle 1 found and we fixed:
- **Acceptor charge compensation** (was the #1 blocker): `apply_charge_compensation`'s
  acceptor branch (Δq<0) was an unimplemented TODO leaving cells 'imbalanced', so
  Y/Si/Ge/Sn/Ti/Zr on P were handed to UMA as charge-UNBALANCED cells → false
  refute. Now implemented via `find_interstitial_sites()` (scipy cKDTree void
  finder) + `add_li_interstitial()`; if no pocket is found the cell is GATED out
  before any xyz is written.
- Evidence/source/reference propagated into generated records.
- `--min_evidence` gate; import-time schema check `_validate_known_substitutions()`;
  `VALIDATION_SET` now checks site×source; added Ta5+→P, La3+→Li; N retagged
  aliovalent; literature `compatibility_score` floored.
- Regenerated `site_preference_initial.json` (the committed snapshot predated the
  override, so the change was not live).

Review cycle 2 (verification) confirmed no P0 and found 3 P1s, now fixed:
- **d_min 1.7→2.0 Å** in `find_interstitial_sites` (1.7 produced 1.73 Å pockets =
  65% of ideal Li–S 2.6 Å → relax-divergence risk). Now pockets land at 2.0–2.32 Å,
  still found (no extra gating). `min_int_dist` stamped on each record.
- **Evidence-GRADED score floor** (was flat 0.5, which promoted Y@P rietveld 0.366→0.5
  ABOVE Y@Li heuristic 0.467 — the weakest claim over the more plausible site). Now
  `{dft_exp:0.60, exp:0.55, analog:0.50, rietveld:0.42}`; Y@P now 0.42 < 0.467.
- **`analyze_screening` consumes evidence** → `evidence_tier`
  (literature_strong / literature_weak / heuristic) column in the ranked output and
  Top-N table (was dead metadata).

## VERIFY then DECIDE
1. Confirm the three cycle-2 P1 fixes are correctly implemented and do what they
   claim (run it): d_min=2.0 gives ≥2.0 Å pockets without newly gating the common
   acceptors; `min_int_dist` is stamped; the graded floor puts Y@P below Y@Li while
   protecting strong literature; `evidence_tier` appears in ranked output and flags
   a rietveld site as weak.
2. Confirm no regression from cycle-1 (charge neutrality for all acceptor Δq,
   gate-before-write integrity, donor path unchanged, `validate` 0 mismatches incl.
   site×source, backward compat `element=None`, schema fail-fast).
3. Confirm the end-to-end "honesty chain": a weak (rietveld) site is (a) generated
   as a charge-neutral cell so energy can judge it, (b) not artificially promoted in
   the site-preference score, and (c) tagged `literature_weak` in the final ranking.
4. Look once more for anything that would SILENTLY corrupt screening (wrong site or
   count generated, an imbalanced cell escaping the gate, a divergent interstitial,
   evidence mis-propagated). Only real, demonstrable corruption counts as a blocker.

## REQUIRED OUTPUT — end with exactly one of:
- **"APPROVED — production-ready; no further review pass needed."** — if you find no
  production-blocking issue. You MAY list optional P2 polish, but it must be marked
  explicitly NON-BLOCKING and must not gate approval.
- **"NOT APPROVED — remaining blocker(s): …"** — only if there is a concrete issue
  that would corrupt screening results or produce a false scientific conclusion.
  List each with file:line, a reproduction, and the minimal fix.

Be decisive. If it is correct, say so plainly and sign off.
