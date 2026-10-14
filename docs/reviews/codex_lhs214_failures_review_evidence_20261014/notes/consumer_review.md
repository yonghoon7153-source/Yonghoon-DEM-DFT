# LHS214 implementation-before review — consumer contract

Pin: `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`. Read the submitted request in full. No production solve, code fix, seal, ledger, or Git mutation. Sources below are the pinned `source/` files. Synthetic probe: `probes/consumer_contracts.py`; results: `evidence/consumer_contracts.json`.

## Answers within this review scope

- **Q1: conditional support for a new, narrow policy; not a no-op rename.** C1-5 withholds the inadmissible FULL value and retains diagnostic CF/constriction values. The producer already explicitly says the FULL cap is a model-output guard, not evidence of numerical nonconvergence (`scripts/network_conductivity.py:1226–1250`; `docs/reviews/gen2_network_design_20261006.md:19`). A separately certified `full_over_conduction` category can preserve this while permitting other valid mode/channel outputs. However current WEB-03, τ, handover, and release language makes all FULL `not_computed` technical/unpublishable. Record publication is an intentional contract revision; amend/register it and retain old failed attempts as history.
- **Q2: use the same model/numerical distinction for H0, Physics and H12, within the actual cap's domain.** The cap concerns single-phase FULL ionic/electronic outputs. Thermal uses a different upper bound and must not acquire a generic `q > 1.5` exception. A new valid H0 model-limit record may be archived/published as a record, but must not fabricate the primary target from Physics/H12, zero, the cap, or the diagnostic rejected q. For this v1.3 release, retain the existing primary-target eligibility policy: any unregistered H0 model-limit case stops the **primary-target release gate**, even if record publication succeeds. A later explicitly registered masked-target release could retain such rows and count them; it is not an automatic consequence of classifying Physics as optional.
- **Q3: Physics-only limits can be represented in an opt-in appendix without losing a registered row, if the new predicates and all gates are changed together.** Require primary H0 eligibility, all required other channels/modes valid or exactly approved model-limit combinations, branch certificates/labels valid, exact cohort IDs unchanged, and blank Physics numeric targets with explicit reason. This is not authorization to label all 14 old failures `full_over_conduction`: only lhsx_054 has the attached detailed diagnostic record in this scope; the other 13 need per-case evidence/re-run confirmation. Existing `MODEL_BELOW_CONTINUUM_BOUND` rows keep their finite values. Existing technical failures still block the whole record.
- **Q4: fast16/real4/receipts are necessary integration checks but do not replace the category, mixed-record, failure-priority, and consumer tests below.** The new full-set reread must verify the exact allowed state/reason/value/certificate combination, not count a broad `NOT_COMPUTED` as success.

## Finding C1 — certificate and role exceptions are safe only while FULL not_computed is rejected

This is the central required design change. The proposal says the mode/channel has a model limit and may be published, but its current state token is also the token for incomplete/failed producer records.

1. `tau_flux.ion_record_problem` treats every FULL `not_computed` as `solver_guard` (`scripts/tau_flux.py:238–240`).
2. `certificate_binding_problems` returns `[]` immediately whenever that technical check fails (`:747–754`). This currently makes sense because every consumer rejects the record for the earlier reason. It also skips the branch table, CF/constriction certificates and sigma0 binding for that record.
3. `_g2_mode_problems` exempts **every** FULL `not_computed` record from missing required labels (`:793–810`), because the record will be rejected elsewhere. This accommodates sparse H12 exception records.
4. `_cert_unpublished_problem` rejects a numerical certificate with finite `I_bottom` on an unpublished branch (`:616–632`). A real over-conduction solve has such a certificate. The attached lhsx_054 Physics certificate is `over_conduction_guard`, finite bottom/top current and residual, and reconstructs q = **1.5370331988867802**. It is numerically solved but its primary value is withheld — different from “no solution certificate.”

Actual pinned-function probes show:

| Synthetic copy of the attached diagnostic | Actual current function/result | Implication for the proposed allowed category |
|---|---|---|
| Set FULL reason to `full_over_conduction`; corrupt CF certificate residual to 1.0 | `certificate_binding_problems('physics', rec) == []` | Do not authorize it through a reason-only bypass while preserving old failure exemptions. All still-published CF/constriction values require their bound certificates. |
| Same state/reason; delete `bulk_model` | `_g2_mode_problems('physics', rec) == []` | The approved model-limit category requires all normal generation/role labels; do not inherit sparse-failure exemption. |
| Keep the real finite FULL over-conduction certificate | `_cert_unpublished_problem(...)` rejects “certificate claims a solution” | Add a narrow numerical-pass/model-withheld contract. Do not delete the numerical proof to fit the old null branch rule. |

These are **not existing published-data escapes**: existing record/stop gates reject these inputs. They are counterexamples to simply whitelisting the new reason at those gates.

Required predicate, shared by producer/consumers: exact eligible branch+channel+mode, finite real q strictly greater than 1.5 (no bool/string/NaN/Inf coercion), successful numerical certificate and matching role/channel/branch/geometry/normalization, complete generation labels, expected through connectivity, accepted temperature/sigma0 pairing, primary published sigma pair exactly null, all derived FULL values absent, diagnostic q stored separately and reconstructable from the certificate. Existing genuine numerical/identity/geometry/schema failures take precedence over model limitation. This category cannot be used to hide a bad certificate, failed sibling channel, or corrupt diagnostic branch. Bool/null/unknown statuses and missing labels/reasons remain errors.

The shared certificate contract currently binds stored sigma values to current/geometry (`tau_flux.py:539–613`). The new diagnostic q must receive equivalent binding; a free-form reason and unverified diagnostic q are not proof. Keep CF/constriction `model_over_conduction` under the existing value-retaining rule. Keep `zero_resistance_requires_contraction` under its existing diagnostic-branch-only rule.

## Finding C2 — all consumer gates currently reject the proposal, and broadening a status whitelist loses distinctions

| Surface | Existing pinned behavior/source | Required narrow change |
|---|---|---|
| Producer channel state | `_channel_solve_failure`, `network_conductivity.py:1898–1909`: all FULL `not_computed` -> channel `failed` | Numerically certified model-limit category must map distinctly; true failure remains `failed`. Do not let `status_for_value(None)` reinterpret it as nonpercolation. |
| Channel content gate | `pipeline_service.py:767–794,823–842`: per mode × ionic/electronic/thermal; unknown new status rejected in strict mode | A `not_computed` channel currently produces `unknown`. Admit only the approved state+reason+proof, not every `not_computed`/unknown/null. All six ordinary channels must still be checked. |
| General prepublish | `app.py:3518–3559`: projection -> channel -> sigma0 -> optional stop -> common record check | Both general and stop paths need the same predicate. General path must not reach Stage E with counterfeit/fallback targets. |
| Shared record check | `pipeline_service.py:1119–1165`: checks dual, both mode files, legacy, H12 and generation | Extend exact category consistently in all copies; record-wide invalidity still wins. |
| Stop contract | `pipeline_service.py:850–872,989–1041,1088–1107`: FULL allowed only computed/valid_zero; τ allowed only OK/MBCB/BAND_FALLBACK/NOT_PERCOLATING | Model-limit case is through and withheld. Do not put it in the existing valid_zero `else` path (`:1002–1006`), which requires graph percolation 0. Validate CPS null/reason explicitly too (`:1007–1014`), and H12 separately. |
| τ consumer | `tau_flux.py:1036–1139`: current reason becomes `solver_guard`; state priorities include technical and generation checks before scientific holds | Preserve exact `full_over_conduction` reason and empty four numerical τ/f fields. In mixed failures, technical/generation errors cannot be overwritten by model-limit reason. L1/L2, missing ledger, invalid percolation and temperature pairing retain their own precedence. |
| Reread K6 | `g2_network_reread.py:510–520`: every FULL state outside computed/valid_zero fails | Add exact producer+τ pair validation, not `NOT_COMPUTED` wholesale. K2 certificates/K7 branch table and H1 must still pass. |
| Handover P4 | `lhs_design_dataset.py:1935–1978,2039–2072`: invokes the same generation, stamp and stop contracts; technical NOT_COMPUTED not handed over | Reuse the new category predicate; preserve all identity/stamp/copy/read-stability checks. Existing P0–P4 safeguards must not be disabled to obtain rows. |
| Release representation | `lhs_release_build.py:652,833–930`: `NOT_COMPUTED` blanks already encode but are labeled technical; H0 classifier becomes blank even when graph percolation=100 | Update dictionary/category counts and primary release decision. Distinguish numerical failure, approved model limit and nonpercolation. Preserve all IDs. No whole-case filtering because optional Physics is unavailable. |
| Refit | `lhs_release_build.py:1777–1810`: H0 NOT_COMPUTED skipped, exclusion reason only status | If primary masking is ever registered, retain exact missingness reason and counts, including per-case exclusion provenance; do not silently change the trained population. |

The concrete proposal-on-current-consumers probe returns Physics `NOT_COMPUTED/solver_guard`, channel `unknown`, and false for both stop whitelists. The appendix blank checker already accepts a synthetic Physics `NOT_COMPUTED/full_over_conduction` row, but that is only representation validation, **not release permission**; upstream P4/reread still block.

Existing policy that must be amended explicitly: `tau_flux.py:48–50`; handover dictionary `lhs_design_dataset.py:1757–1772` (“NOT_COMPUTED is technical; never in handover”); `lhs_release_build.py:652`; `webapp/app.py:823,921–922`. `docs/reviews/findings.json:7941–7948` records WEB-03's closed requirement to reject true percolating solve failures on both paths. `docs/reviews/lhs_network_batch_registration_20261007_g2.md:274–280` binds branch certificate policy and model combinations. “Physics is opt-in” does not waive these record-wide technical guarantees.

## Finding C3 — newly publishable null Physics will be shown as Hertz in current webapp

This is an actual helper reproduction of a **newly reachable display defect under the proposed publication policy**, not a claim that the currently blocked 14 records were displayed.

`webapp/app.py:_dual_row` at **649–655** intentionally uses Hertz for the Physics cell when `p_val is None`. `transform_network_summary_4col` uses it directly for ionic conductivity at **3058–3062** and electronic/thermal conductivity at **3114–3129**. It also explicitly falls back to Hertz for the Physics Bruggeman ratio at **3089–3091** and **3207–3209**. Existing two-column CSV rows are expanded by copying values too (`:2873–2901`). By comparison `_dual_row_strict` and `_tau_block_rows` correctly leave missing Physics τ blank (`:672–707`).

The exact pinned function bodies were compiled from AST without edits (to avoid Flask/server startup); only import adapters for τ and se_material were supplied. Actual `transform_network_summary_4col` output for a synthetic publishable mixed record (Hertz σ=0.6, Physics σ=null, Physics reason=`full_over_conduction`) is:

| Row | Hertz shown | Physics shown | Delta shown |
|---|---:|---:|---|
| σ_ionic | 0.6 | **0.6** | **0%** |
| σ_brug / σ_ionic | 2.0× | **2.0×** | **0%** |
| τ² | 2.5 | — | empty |
| σ_ionic status | computed | not_computed/full_over_conduction | empty |

The same fallback also gives electronic 2.0 in both cells when Physics electronic σ is null. An existing Network Solver CSV section reproduces the ratio fallback as well. The allowed record would therefore show a Physics number alongside a contradictory missing status. Acceptance tests must cover both absent/new section and existing CSV section, live and archive callers, nullable ionic/electronic channels, Δ and derived ratios. All mode-specific missing numeric values and ratios must remain missing with the explicit model-limit reason. This extends beyond the requested τ wording change.

## Minimal acceptance matrix for implementation review

1. Each eligible mode (H0, Physics, H12) and single-phase FULL channel: certificate passes + q>1.5 => exact model-limit state/reason, all target values withheld; record succeeds only if every other required contract passes. Physics unavailable/H0 valid retains the same cohort ID and eligible H0 target.
2. Boundary q cases: below, equal, and just above 1.5; never round a displayed 1.50 into/out of the guard. CF/constriction q>1.5 keeps its existing diagnostic value/state. Thermal q>1.5 is not classified by this cap.
3. Mixed record: allowed Physics limit + H0 numerical failure; allowed H0 limit + Physics electronic/thermal failure; H12 failure; failed numerical certificate + high q; invalid branch/role/geometry/sigma0; unknown/missing/null/bool state or diagnostic. All remain blocked across normal and stop paths.
4. Preserve negative evidence: no Stage E/publish on failure; previous valid generation retained; first-run failure has no active generation; failed attempt remains recorded. A model-limit record must carry current successful record identity with explicit channel availability, not be mislabeled as a failed attempt or use stale values.
5. Consumer roundtrip: producer files -> content/record/stop -> τ -> real publication -> reread K1–K7/H1 -> handover -> v1.3 build/check -> UI. Assert exact state/reason, null vs empty CSV, branch certificates, original ID sets and availability counts. Any q diagnostic cannot become `sigma_full`, f, τ, target, zero, or a substituted other-mode value.
6. Primary H0 policy must be an executable gate: current v1.3 should reject unregistered primary model-limit targets, while preserving the published record for diagnosis; optional Physics limits alone can pass the revised gate. If another masked-target policy is chosen, register it before the new batch and test its percolation-class and regression masks/counts explicitly.
7. Baseline acceptable records retain all unaffected numbers bit-for-bit. Existing true-failure and case15 negative controls continue rejecting for their precise reasons; all existing seal/root/cross-batch receipt/identity checks remain in force. Then fresh roots and all 214 rerun under one new code fingerprint, exact registered set rereads, and fresh receipts.

## Probe execution

Executed successfully with bundled Python, `-X utf8 -B`, using existing scientific dependencies from sibling review directories. No production solve was run. For the attached lhsx_054 record only, changing the certificate category on an in-memory copy to `computed` lets the existing pure numeric certificate validator evaluate the remaining fields and returns no numeric error. This normalization is explicitly diagnostic, not a proposed producer mutation or a claim that the old raw certificate passes current publication validation.
