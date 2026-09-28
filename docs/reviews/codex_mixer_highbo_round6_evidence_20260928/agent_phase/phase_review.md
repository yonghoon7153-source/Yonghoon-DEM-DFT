# Independent phase receipt review

Target: `18787ab98a13361c37b2343bd07ae276142d0953`.
Evidence: `phase_probe.py`, `phase_probe_output.json`, `capture_selftest.py`, `phase_selftest_python.txt`, `phase_selftest_python.json` in this directory.
The probe imports production code from the pinned mirror, reuses the previous independent review's synthetic fixture writer, and executes only the Python run-status recorder extracted from `RUN_SH`. No simulator, MPI, job, Git mutation, or production edit occurred. Fixtures were generated under this directory and removed by `TemporaryDirectory` after the tests.

## Q1 / HBR5-05: original counterexample closed, separate residual defects

`scripts/mixer_restart_phase_test.py:112` (`deck_steps`) and `:362`–`:405` now derive completion and dump grids from the sealed decks, check A end = B `run ... upto` = A motion-clock end, and cross-check `gen.json`. `:387`–`:390` require B's logged resume step to equal A's checkpoint step.

Independent results:

| Probe key | Actual producer CLI rc | Actual result |
| --- | ---: | --- |
| `normal` | 0 | passed; A 28 / B 11; deck end 14,001; N1 9,000; residual 5.7007350e-16 m; A/B max 0 |
| `gen_end_truncated` | 1 | Original counterexample closed: sealed end 14,001, mutable gen end 9,500; A 19 / B 2; metadata mismatch, incomplete logs and 9 missing frames per part detected |
| `bad_resume_step` | 1 | Logged RESUME_STEP 9,500 rejected against sealed N1 9,000 |
| `banner_short_tail` | 0 | Still passed with both logs ending at 14,000, although sealed end is 14,001; A/B expected grid remains complete (28 / 11) |
| `changed_gen_motion_signature` | 0 | Passed and consumer accepted for a campaign with a different, unmeasured Drum |

The full 28 stock Python selftest assertions passed, 0 failed. A runtime guard stopped before the two Bash/fake-launcher assertions; they were not executed and this review does not claim 30/30. Windows invocation required `PYTHONUTF8=1`; the unmodified selftest otherwise reads UTF-8 generated decks using cp949.

### New source-binding defect (suggested P1, distinct from original HBR5-05)

`scripts/mixer_restart_phase_test.py:509` copies `gen.json.motion_signature` directly into the receipt. It never compares it to `motion_signature(a_deck, A_dir)` or the corresponding sealed B contract. The sealed STL hashes are checked for their own integrity (`:350`–`:359`), but the measured mesh contract and advertised signature are not joined. `scripts/check_contact_validity.py:606`–`:607` trusts that advertised signature for the campaign comparison; `:585`–`:589` only validate the receipt STL-hash list's shape and hash syntax, not its equality with the campaign geometry.

The probe kept all A/B decks, source STLs, dumps and their seal unchanged. It translated the *campaign* Drum by 0.01 source-coordinate units in y (149.277 micrometres after scale), recomputed the campaign launch seal, and changed only mutable `gen.json.motion_signature` to that campaign signature. `analyze` returned `passed=true`, CLI rc 0; `load_phase_receipt` accepted it. Its advertised position bound stayed 1.3915163690e-14 m. The measured A signature was `78c93320ad41c8acfbadb4e6f76a431c11f512ea2334ba75daf0131e995ef52a`; the accepted advertised signature was `b7588c4e36fbc3edb93e17d6484e90dcb009ab20fd27b6a8357e652f30969488`.

This does not assert that any committed receipt has the wrong mesh. It demonstrates that mutable metadata can claim a geometry the preserved measurement never tested. Required regression: `changed_gen_motion_signature` must return producer rc 1 (or advertise the recomputed measured signature, causing the mismatched campaign consumer to reject); the unmodified control remains rc 0. Recompute every claim that can be reconstructed from sealed sources, including facet count, and treat generation metadata as cross-checks.

### Narrow residual completion gap (suggested P2)

`scripts/mixer_restart_phase_test.py:90` makes a `Total wall time` substring sufficient regardless of the observed final thermo step. `:375`–`:378` accept this completion result. `banner_short_tail` holds end 14,001 and all required dump steps through 14,000 fixed, but puts final thermo step 14,000 and a wall-time banner in each log. The result is rc 0, `completion_basis="banner"`, and consumer acceptance.

This is a one-step unmeasured tail in the bounded example, not the original 4,501-step truncation and not evidence of an incorrect production mesh frame. It remains inconsistent with the receipt's complete-through-sealed-end claim. Acceptance test: when a numeric final step exists and contradicts the sealed end, a banner must not override it; rc 1. A completed no-banner log at the exact end must keep passing. If a banner-only compatibility path remains, define its separate, independently anchored completion evidence instead of silently overriding a contradictory final step.

### Additional contract hardening, not a claimed executed production failure

The probe also resealed a B deck whose read command is `read_restart unrelated/other.bin`; expected logs and synthetic geometry at N1 still produce rc 0. `deck_steps` only counts `read_restart`, rather than tying its file argument to A's unique `write_restart` and the copied checkpoint bytes. This fixture is not a real restart execution. Add an acceptance guard for A-write/B-read path and checkpoint identity if the receipt's assertion is specifically that B resumed A's checkpoint. Equal step numbers alone do not establish byte identity.

## Q2: approve implementation-and-test order, not MPI20 release yet

The planned sequence is sound: change the matcher, validate it synthetically and against preserved np1 raw evidence, then acquire a newly sealed np20 A/B receipt in the actual execution environment. The current comparator fails harmless reordering: independently reverse A triangle listing, rotate B listing by seven, and permute vertices within each triangle; `permuted_triangles` returns rc 1 at `scripts/mixer_restart_phase_test.py:424`–`:429`, with A/B numerical checks never reached. `:437`–`:448` also locate Drum by its contiguous output position; `:463` compares A/B arrays by position. All these paths need the same order-invariant correspondence.

Required comparison contract:

1. Treat each STL as a **multiset of complete three-vertex triangles**. A source-to-output assignment must be bijective, one output triangle consumed once, considering all six vertex permutations inside each triangle. A flattened vertex cloud, one-way nearest neighbour, triangle set, plane set, area, or bounds alone loses either topology or multiplicity.
2. Build expected components from the **sealed** source files and transforms, carrying the source component and triangle identities through the correspondence. Check complete Drum/Front/Back counts and the complete expected triangle multiset. Never infer Drum from an output slice after ranks reorder triangles. For identical triangles shared across component labels, a combined unlabelled STL cannot prove provenance labels; use per-component dumps/labels when that distinction matters.
3. Match A at global step s against the sealed A motion clock, and B at the same global step against that **continuous** phase. Do not derive B phase by treating redeclared movers as fresh step-zero motion, and do not freely rotate/translate either observed mesh to force agreement. Any small fitted angular offset must remain a measured error with a preregistered search interval and propagated residual; it cannot absorb a restart reset. A/B comparison should use the resulting source correspondence, with the same physical tolerance/rounding policy, not serialized ordering.
4. Handle tolerances with a one-to-one triangle assignment. Greedy nearest matches can reuse duplicates; coarse coordinate rounding can merge distinct triangles and change boundary decisions. Reject non-finite data and unsupported geometry/motion before reductions, and include every component in residual and position bounds. State ambiguity handling explicitly.
5. Derive facet count and reset-alternative separation from the sealed geometry and clock. Reordering introduces no authority to change the registered angle bound, position budget, sampling grid, or required coverage.

The exact synthetic `triangle_bag` oracle in `phase_probe.py` demonstrates two necessary failures without proposing a production algorithm: rewiring vertices between triangles preserves the full coordinate multiset but changes triangle topology, and replacing `[a,a,b]` with `[a,b,b]` preserves the triangle set but changes multiplicities. Both must fail. The oracle intentionally has no floating-point tolerance and is only an acceptance-data generator.

Executable acceptance cases for the future matcher/producer:

| Test input | Expected |
| --- | --- |
| Original independent normal fixture | rc 0, same measured bounds |
| Arbitrary triangle permutations and all 6 internal vertex permutations, independently in every A/B frame | rc 0; same phase and geometric bounds within explicit arithmetic tolerance |
| Rank-like splitting/interleaving and exact duplicate triangles that already exist in the source | rc 0, exact multiplicity preserved |
| `triangle_oracle` rewire with unchanged point bag | rc 1 |
| `triangle_oracle` altered duplicate counts with unchanged triangle set | rc 1 |
| Missing Front or Back; cap replaced with duplicate other cap; same triangle count but wrong connectivity | rc 1 |
| One changed vertex beyond permitted coordinate/position budget; source-bounds-only lookalike | rc 1 |
| NaN/Inf in A or B; empty, partial, duplicate-step or extra-step dump inventory; empty seal/hash lists | rc 1 |
| B reset to phase zero at N1, or B shifted by a known non-symmetric phase larger than allowed | rc 1; genuine continuous B remains rc 0 |
| Ambiguous nearest-neighbour or tolerance-boundary collision with no one-to-one assignment | rc 1 |
| `gen_end_truncated`, `bad_resume_step`, `changed_gen_motion_signature`, contradictory `banner_short_tail` | rc 1 |
| Saved np1 **raw** A/B inputs through old and new geometry comparators | Preserve step coverage, fitted errors, residuals, A/B bounds, and pass/fail within registered tolerance |
| Newly acquired np20 receipt vs selected campaign launch | Verify executable SHA, actual rank count/launcher/environment, sealed decks/STLs, complete A/B evidence and consumer compatibility |

Existing receipt JSON alone cannot exercise a new geometry comparator; retain raw decks, STLs, logs, dumps, seal and run-status files. The request explicitly says old A/B logs are absent from the repository. A geometry-only comparison on preserved raw dumps can be reported separately from re-certification under the newly required RESUME_STEP rule. If the old logs cannot establish that rule, acquire a new np1 baseline rather than upgrading old JSON's status. No new np1/np20 measurement was performed in this review.

Suggested evidence package for the future acquisition: sealed binary and launcher/rank metadata, A/B source hashes, tool hashes, scheduler/job-start evidence, A-write/B-read checkpoint hash, exit and end-step records, RESUME_STEP, exact per-step dump inventories and hashes, source-to-output component/count validation, reset negative control, per-step phase/residual/A-B metrics, and the propagated finite angle/position bounds. A pass at np1 remains only an np1 result; np20 compatibility must be validated and enforced, not inferred from a matching banner or binary hash.
