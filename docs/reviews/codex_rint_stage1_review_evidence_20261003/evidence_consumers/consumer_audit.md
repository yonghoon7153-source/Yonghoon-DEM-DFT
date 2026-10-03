# Independent consumer audit — Q1 / Q8 / P2-4 / P3

Pinned code is the source snapshot supplied by the parent review. No source implementation was modified. `probe_consumers.py` imports actual pinned functions and runs CPU toys; `consumer_results.json` contains measured values and SHA-256 of the three principal source files. The STEP4 serialization test executes the actual producer AST call with a capturing `np.savez_compressed` substitute; it does not run an entire production payload. The reaction film comparison uses a separately derived series-resistor oracle whose OFF value matches the actual reaction solver.

## Priority findings

### P2 — AM current-map contamination remains after an iid-only fix (Q1)

- `scripts/step3_sigma.py:1113-1115` bins every nonnegative `pid`, even when the final sid is carbon. Producer contract at `:440` says pid is an AM particle index and -1 means not AM. Carbon stamping changes sid but preserves pid (`:647-676`), and payload exports the resulting `je` (`scripts/mpm_webapp_payload.py:1989`, `:3029`).
- Independent actual-rasterize toy: two R=1 µm AM spheres, vox=.2 µm, one tangential VGCF line with **every input point outside both AM spheres**. Segment stamping yields 20 carbon cells, eight with inherited AM pid. Unmasked je is `[0.0383162435, 0.0377561038]`; AM-sid-masked je is `[0.0003027511, 0.0003121740]`. Inflation is **126.56× and 120.95×**, and the apparent AM ranking reverses. No interface resistance is enabled. This is a producer-path counterexample, not an estimate of the frequency or magnitude in real beds.
- In a synthetic fully overwritten particle, zero AM cells remain but the reported AM proxy is 9.0. Hence this is not an AM volume average. Anchored-contact carbon current can be a separate intentionally defined statistic, but does not justify calling this the mean AM |Jz|.
- Minimal fix: `per_particle_current` must select final sid in {1,2} as well as a valid AM pid. A separate immutable raw ownership/anchor grid can be retained if needed. Do not needlessly change all downstream fields.
- `solve_reaction_current` **already gates AM sid** at `:1891,1902` before consuming `pid` at `:1912`. `am_surface_patches` **already gates AM sid** at `:3340,3362` before consuming pid at `:3363`. Both are bitwise unchanged in the independent cleanup probes. `step4_dyn.CellSystem` also gates AM at `:1105,1116` before pid at `:1121`.
- Conclusion affected: per-particle current colors/rankings and any interpretation of which AM particles carry current. Sigma and reaction current are not changed by merely fixing the consumer mask.
- The emergency same-sid AM whitelist closes false VGCF/SE same-sid interfaces in stage ①, provided enforced at both parser/API and face rule. iid namespaces masked by final sid are appropriate for future ownership, but **iid alone leaves je wrong**. Add this consumer correction to the same review bundle.
- Draft incompatibility: `contact_resistance_pipeline_draft_20261002.md:41,53` promises all r-OFF outputs remain bitwise unchanged. A correct je fix necessarily changes r-OFF je. Preserve sigma/phi/patch/rxn and explicitly version/document the corrected je exception instead of claiming all payload output is identical.

### P2 — Joule map omits the dominant interface heat (P2-4 / Q8)

- `scripts/step3_sigma.py:1492-1494` correctly recomputes the r-adjusted current, then forms only bulk `J²/sigma`. It never assigns `I_face² R_interface` to a face or voxel. The exact interface dissipation already exists in `phase_current_share` at `:1212-1215`.
- Actual-function equal-sigma two-slab toy, 4×4×10 cells, vox=.5 µm, sigma=1 S/cm, r=.01 Ω cm²: sigma changes 1 → .0476190476; interface share is **.9523809539**, agreeing with independent series formula .9523809524. Nonetheless normalized Joule maps differ by only **2.03e-6** (solver precision), both `hot_frac_50=.425`, and concentration remains 1.17647. The sheet holding 95.24% of total heat is absent as a hotspot.
- Payload at `scripts/mpm_webapp_payload.py:2164-2168` presents this as where heat is generated and as the fraction holding half of q, without saying the interface term is excluded. Viewer reinforces this at `webapp/static/js/viewer3d.js:3394,3463`.
- Minimal stage-① fix: label the map and summary **bulk-only Joule heating**, add machine-readable included/excluded terms and excluded interface share, and avoid total-heat hotspot conclusions. Full closure needs a face heat map (or a documented area/volume deposition operator), with raw total bulk+interface(+plate as applicable) power checked against IV. A note does not make current `hot_frac_50` a total-heating metric.
- Grade is P2 for the current opt-in prototype. It would invalidate an r-ON heat-location conclusion; no evidence that sealed r-OFF production outputs already contain this new error.

### P2 — STEP4 reaction and NPZ silently use a different transport model (P2-4 / Q8)

- `scripts/mpm_webapp_payload.py:2737-2738` calls the reaction function without a resistance table. `scripts/step3_sigma.py:1867-1874` couples both networks with bulk harmonic conductances; its signature has no rint parameter. Payload `rxn.trust` at `:2752-2755` lacks this distinction.
- Independent two-path reaction toy: real reaction solver yields `[.04347826087,.04347826087]`, normalized `[1,1]`. One path contains AM|VGCF, so adding the same r=.01 Ω cm² film in a physically consistent chain changes its current to .002364066194 (94.56% suppression), normalized `[.1031390135,1.8968609865]`. OFF oracle is exactly 1/23 and agrees with the actual function; this is not an implemented r-ON reaction solver claim.
- Executing the producer's actual save expression (`scripts/mpm_webapp_payload.py:2771-2789`) captures only ten keys: `am_r_um, origin_shift_um, periodic_xy, pid, sid, sig_e_S_cm, sig_i_S_cm, temperature_provenance, vox_um, z_top_um`. **No interface identity, table, or applied flag survives.** `scripts/step4_dyn.py:3067-3083` loads sigma tables and `:1062` creates harmonic bulk-only edges; CellSystem has no interface argument (`:970-971`).
- Minimal stage-① fix: machine-readable model scope on sigma, je, rxn, Joule, thermal, tau_geo and exports; explicitly label reaction as a CONTACT_FREE transport counterfactual when r is enabled. Reject r-ON + `--save-step4-grid` until an export schema and reader can preserve/validate the transport law. Merely saving table metadata does not fix a consumer that ignores it. When iid/contact ledgers arrive, the resolved edge law or a fully versioned reconstructible representation must travel as well.
- Same-channel sigma metadata must derive from actual solve records; a global CLI interface flag cannot truthfully describe all these blocks. Existing stages may intentionally exclude reaction, heat conduction or plates, but their outputs must not be represented as a single r-ON model.

## P3 reassessment

| Self-review item | Independent judgment / evidence | Minimal action |
|---|---|---|
| P3-1 zero/irrelevant table ULP and interface=0 key | Confirmed P3. r=0 sigma and phi bitwise equal, share delta only 1.68e-18, extra -1:0 key. No numerical significance but breaks proposed exact output contract. | Use a diagnostic r context only when active faces exist; preserve separately requested/applied metadata. |
| P3-2 API silent casts | Confirmed P3 input contract bug: actual `_check_rint_table({(1.7,3):True})` returns `{(1,3):1.0}`; sid0 also accepted, cannot roundtrip through phase-name parser. | Validate integer sid in SID_NAME (exclude bool), real finite r (exclude bool), then normalize. |
| P3-3 compare_dirs | Contracts agent owns. | — |
| P3-4 no-ion | Contracts agent owns. | — |
| P3-5 NODIGEST cache | Contracts agent owns. | — |
| P3-6 interface bucket sums all pairs | Correct aggregate metric, not itself a numerical bug. It equals sensitivity to scaling all r together; it cannot establish individual pair sensitivity. | Pair buckets and centered-log per-pair perturbations needed before per-pair claims; stage ①′ enhancement. |
| P3-7 similar `interface_rint_*` versus terminal-cell ASR `r_int_ohm_cm2` names | P3 clarity improvement, **no literal key collision found**. Distinct keys/physical scopes exist. | Prefer iface prefix and explicit units/scope, but do not claim a demonstrated overwrite. |
| P3-8 viewer calls all loss bars phases | Confirmed P3 label: viewer `:5340-5341,5356` says each phase's loss; interface is not a phase. | Label phase/interface loss shares and interface separately. |
| P3-9 diagnostics accept caller sid | Confirmed P3 defensive API gap in current call graph; no mismatched production caller established. Same-shaped wrong sid at identical sigma gives 101× max |J| and interface share .95238→0 without rejection. Large consequence if misused, but not proof of a current payload mismatch. | Sid fingerprint is useful but **not sufficient**: also bind/validate pid and sigma field or consume frozen resolved edge ledger. |

Additional P3-9 probe: solve retains original pid by reference (`step3_sigma.py:1082`). Mutating caller pid to one ID after a same-sid solve changes reported interface share .95238→0 while saved `n_faces_rint=9` remains. This specifically defeats the proposed sid-only fingerprint. Store immutable context or hash/validate all law-defining inputs (including iid once introduced); the accepted long-term I3 design, diagnostics consuming resolved edges, is stronger.

## G1 / Q1 / Q8 recommendation

G1 HOLD for declaring defects closed. The whitelist is a valid emergency stage-① closure for false non-AM same-sid interfaces; final-sid-masked iid is a good ownership separation. Neither alone fixes the existing AM current proxy or mixed consumer contracts. Release conditions: sid ownership on je; explicit r-OFF output exception; reaction/Joule scope; STEP4 export guard/schema; same edge law for assembly and diagnostics, with context integrity beyond sid. No additional P1 affecting scalar sigma with r absent was demonstrated by this consumer audit.
