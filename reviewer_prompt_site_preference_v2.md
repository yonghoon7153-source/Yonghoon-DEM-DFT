# Reviewer prompt v2 — VERIFY the fixes to the site_preference literature-override

You are reviewing the SECOND iteration of a change to a DFT/MLIP dopant-screening
pipeline for Li6PS5Cl argyrodite. Two prior reviews flagged issues; they have now
been fixed. Your job is to VERIFY the fixes are correct and physically sound, and
to hunt for NEW problems the fixes may have introduced. Do not re-litigate the
original design; focus on the new code. Files in scope:
`scripts/doping/site_preference.py`, `scripts/doping/substitute_struct.py`,
`scripts/doping/analyze_screening.py` (downstream consumer), and the regenerated
`db/doping/site_preference_initial.json` / `data/doping_screening/site_preference_initial.json`.

## What was changed in response to review
1. **Acceptor charge compensation (was the #1 blocker).** `substitute_struct.py`
   gained `find_interstitial_sites()` (scipy cKDTree void finder) and
   `add_li_interstitial()`. `apply_charge_compensation`'s acceptor branch (Δq<0)
   now ADDS |Δq| Li at interstitial pockets (was a TODO that left cells
   'imbalanced'). So Y/Si/Ge/Sn/Ti/Zr on P now generate charge-neutral cells
   (e.g. Y@P → label `Li_int_2`, 54-atom cell). If fewer than |Δq| pockets are
   found, the cell is GATED out (`generate_for_dopant` skips any `imbalanced_*`).
2. **Evidence propagation.** `generate_for_dopant` now copies
   `site_source`/`evidence`/`reference` into each emitted record.
3. **`--min_evidence` gate.** Optional: skips LITERATURE sites weaker than a
   threshold (e.g. `analog` drops rietveld-only Y@P); heuristic sites never gated.
4. **site_preference.py:** import-time schema check `_validate_known_substitutions()`;
   literature `compatibility_score` floored to 0.5; `VALIDATION_SET` now checks
   site×source (optional 4th tuple element); added `Ta5+→P` (analog) and
   `La3+→Li` (exp); retagged N as aliovalent.
5. Regenerated `site_preference_initial.json` (32 dopants, now carries
   source/evidence and Y→P_4b).

## VERIFY (with concrete pass/fail + evidence)
1. **Interstitial finder physical soundness (highest priority).** Read
   `find_interstitial_sites`. Is the 3×3×3-image min-image distance logic correct?
   Are the defaults sane (`d_min=1.7`, `d_anion_max=3.0`, `grid_spacing=0.7`)?
   Could it place Li (a) overlapping/too close to the dopant or another Li,
   (b) in a non-physical spot that makes the downstream UMA/FrechetCell relax
   diverge or migrate wildly, or (c) clustered rather than spread? Is the
   farthest-first + seeded RNG deterministic and reproducible? What happens for a
   small cell or a fully-packed structure (does it silently return too few and
   gate, which is acceptable, or misbehave)? Does it ever add the WRONG count
   (must be exactly |Δq|)?
2. **Charge neutrality, all acceptor cases.** Confirm the emitted cell is net-zero
   for Δq=−1 (Si/Ge/Sn/Ti/Zr@P, N@S) and Δq=−2 (Y@P). Any off-by-one? Does the
   donor path (Δq>0, Li vacancy) still work unchanged?
3. **Gate integrity.** Is there ANY path where an `imbalanced_*` cell still reaches
   the output `structures_summary.json` or disk? Does gating happen before the
   xyz is written?
4. **Evidence propagation completeness.** `generate_for_dopant` now carries
   source/evidence/reference — but does `analyze_screening.py` actually CONSUME
   them (tier/weight/flag), or are they still dead metadata one stage further
   down? If unused, say so and propose the minimal hook.
5. **Score floor side-effects.** Flooring literature `compatibility_score` to 0.5:
   does it now over-rank a genuinely poor-fit literature site above good heuristic
   ones in `analyze_screening` (w_s term)? Is 0.5 the right floor vs heuristic
   scores (~0.32–0.50)?
6. **`--min_evidence` correctness.** Rank comparison direction right? Interaction
   with the imbalanced gate and with heuristic sites? Off-by-one at the threshold?
7. **Regenerated JSON consistency.** 32 entries well-formed? Every `compatible_sites`
   has source/evidence/compensation? Any entry with zero sites that should have
   some (or vice-versa)? Does it match what `substitute_struct --site_pref` expects?
8. **New science.** Ta (r=0.64,+5) and La (r=1.03,+3) radii/charges correct and
   site assignments defensible? Is the N retag (aliovalent acceptor on S) right,
   and does N@S now go through the interstitial path correctly?
9. **Regressions.** Backward compat (`element=None`), `validate` still 0 mismatches,
   single-mode (`--dopant/--site`) path still works, no import-order hazard from the
   import-time schema assert.

Return prioritized findings (P0/P1/P2), each with file:line, why it matters, and a
fix. End with a one-line verdict: safe-as-is / keep-with-followups / needs-fix.
Pay special attention to the interstitial finder — it is new, physics-bearing, and
feeds every acceptor structure into UMA/DFT.
