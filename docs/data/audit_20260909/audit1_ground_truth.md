## GROUND TRUTH BRIEF — repo `/home/user/Yonghoon-DEM-DFT`, branch `claude/stoic-knuth-NObVQ`, as of 2026-09-08

---

### 1. FORBIDDEN NUMBERS — the machine registry (`docs/reviews/claims.json` → `quotation_ban`, 22 entries, verbatim patterns)

`check_review_findings.py --ban-sweep` scans CLAUDE.md, `docs/**`, `wiki/**`, webapp templates/JS, deck generators, and Office zips (pptx slides + speaker notes, `word/document`), matching these as **literal context-bearing strings** (with normalization for NBSP, thin space, JSON `\u0025`, trailing zeros). An occurrence is an ERROR unless (a) the file is in `allowed_in` or `BAN_ALLOW_ALWAYS`, (b) the file's first 12 lines carry both a marker (`HISTORICAL`/`⛔`/`인용 금지`/`철회`/`반증`/`retired`/`~~`/`폐기`/`무효`) **and** a ledger anchor (`claims.json`/`CL-`/`CLAUDE.md`/`인용 금지`), or (c) a retraction word (`인용 금지`, `철회`, `반증`, `폐기`, `무효`, `~~`, `CL-`) appears within ±2 lines.

| # | pattern (verbatim) | claim | why | allowed_in |
|---|---|---|---|---|
| 1 | `+52.0 %` | CL-24 | vox 0.4 point-stamp artifact; tightening the same convention walks it down | — |
| 2 | `+5.6 %` | CL-24 | ionic gain of the same run; sign flips on refinement | — |
| 3 | `+42.15` | CL-24 | vox 0.4 grid artifact | — |
| 4 | `×35.79` | CL-15 | segment↔point multiplier is a convention difference, not an under-estimate factor | — |
| 5 | `f_artifact` | CL-24 | the 0.147 artifact decomposition (and its 14.7 %/85.3 % split) held only under vox 0.4 | — |
| 6 | `준정적 답은 ~9.4` | CL-04 | R1 measured ε_sphere 1.13 %; "three independent extrapolations" was 1.5-fold double counting | — |
| 7 | `9.4 % vs 실험 15.6` | CL-04 | same refutation | — |
| 8 | `1.14508` | CL-41 | discarded intermediate for vox 0.125 | `docs/data/prereg_v2/raw_sigma.json` |
| 9 | `+52 %` | CL-24 | notation variant | — |
| 10 | `+52%` | CL-24 | notation variant | — |
| 11 | `+5.6%` | CL-24 | notation variant | — |
| 12 | `+52.0%` | CL-24 | no-space variant (missed by an earlier negative control) | — |
| 13 | `1.1232` | CL-33 | sphere-stamp σ_e ratio solved under the **p1 plate rule**; banned until p2 re-measurement (R5-CX-06) | `docs/data/prereg_v2/raw_sigma.json` |
| 14 | `1.123191` | CL-33 | precise form of the same | same |
| 15 | `1.123214` | CL-58 | same family (doping baseline) | same |
| 16 | `+12.3 %` | CL-33 | percentage form of 1.1232 | same |
| 17 | `+12.3%` | CL-33 | no-space variant | same |
| 18 | `+12.32` | CL-33 | decimal variant | same |
| 19 | `1.143817` | CL-41 | vox 0.125 p1 value | same |
| 20 | `1.155448` | CL-41 | vox 0.115 p1 value | same |
| 21 | `+14.38` | CL-41 | percentage form of 1.143817 | same |
| 22 | `+15.54` | CL-41 | percentage form of 1.155448 | same |

Always-allowed files (registry layer, do not "fix" them): `docs/reviews/claims.json`, `docs/reviews/findings.json`, `docs/reviews/fable_audit_docs_20260820.md`, `docs/reviews/fable_audit_code_20260820.md`, and archived verbatim external-review transcripts.

### 1b. FORBIDDEN — the CLAUDE.md prose list (a SUPERSET of the machine registry; these are banned by canon even where no regex exists)

`+52.0 %` · `+5.6 %` · `+42.15 %` · `f_artifact = 0.147` · `14.7 % 인공물 / 85.3 % 물리` · `0.0277 = 참값 천장` · `브래킷 [0.000574, 0.0277] 폭 48.2배` · `점 → 참값 [×0.112, ×5.41]` · `σ_e 절대값 2.67~4.62배 과대` · `규약 민감도 ≈ 7.4 % × VGCF wt%` · `×35.79` · `직경-보존 σ 는 하한` · `1D 망 = 격자 의존의 근본 해법` · `실험의 3.6배`.

Additional standing bans not in the registry table but binding in the ledger text: every σ_e/gain value from the three-grid sphere-stamp sweep (vox 0.15 / 0.125 / 0.115) — p1 plate-rule products, numbers live only inside CL-41 (`hold`); the Richardson extrapolation derived from them (≈1.16); the vox 0.4 Phase-A wiring-arm σ_e pair from CL-84/CL-85 (not the registered grid, prereg excludes them from judgment); `coverage_AM_*` voxel-preview coverage (~26 %) which never converges; the `k = 1.4855` staircase factor as a physical correction coefficient (CL-20, estimator discarded path order via `np.unique`); the CL-59 span mean/median and the `r` parameter value itself (unidentified); the "≈0.1 mS/cm convergence" statement for binder-film σ_ion (CL-62); "σ_ion increases/decreases" under SDCP substitution (sign unidentified, CL-59).

**Adjacency warning:** ratios such as `1.1263`, `1.3092`, `1.308`, `1.124` are *not* string-matched by the registry but sit one digit away from banned values and belong to the same p1/convention families. Check `quotation_ban` before writing any four-digit ratio.

---

### 2. RETRACTED / SUPERSEDED — id → what was claimed → what replaced it

**`retired` (4):**
- **CL-17** — "SR-01 bracket closed by measurement; true-value ceiling 0.0277, point-stamp upper multiplier ×5.41" → superseded: the sign was re-derived the same day (`R_ras = k·R_true` ⇒ the diameter-preserving value is a **lower** bound, not upper), then CL-21 showed grid non-convergence swamps the whole bracket argument. Only the raw four-arm σ_e measurements survive as raw data.
- **CL-18** — "the ionic axis is nearly insensitive to raster convention, bracket 8.0 %" → the 8 % holds only for a VGCF 1 wt% bed; on the SDCP pair it is 21 %. The surviving statement is the **ratio** is robust, not the absolute. The derived scaling rule `≈7.4 % × VGCF wt%` is banned.
- **CL-19** — "14.7 % of the SDCP gain is raster-made; headline moves +51 → +42 %" → both h0 and h1 missed; the whole `f_artifact` decomposition and the new headline are banned (CL-24 replaced it with "electronic gain +42 → +8.5 % and ionic gain flips sign").
- **CL-20** — "staircase factor k = 1.486 measured; diameter-preserving σ_e is a lower bound" → superseded by CL-21; Codex CDX-02 re-ran k at three grids (1.4855 / 1.4917 / 1.4461, not grid-independent) and found the estimator discarded path order. k may not be used as a physical correction.

**`hold` (6) — evidence awaiting re-measurement, quotation prohibited:**
- **CL-23** (since 2026-08-13) — "1D fibre resistor network has zero discretization dependence; the fundamental fix" → cut down by Codex CDX-06/07/08 to one sentence: "the axial edge conductance of an ordered, contact-free fixed polyline is invariant to subdivision and matches the straight-line analytic solution." `couple_to_voxel_grid` still does not exist.
- **CL-30** — origin-averaged σ_ion within ±3 % at SE Ø/dx ≳ 4 → demoted by CL-74: the convergence verdict leaked at the last grid, and the 0.15 point (Ø/dx 6.67) comes in at −3.17 %. Measurements valid, convergence statement dead. Also the origin test moved the physical crop, not just the grid phase.
- **CL-31** — "the true-sphere gain is flat in grid" → headline retracted 2026-08-18: the sphere arm had no `d/vox ≥ 2` production gate, so 78.7/47.8/19.3 % of SDCP particles got zero cells at vox 0.4/0.3/0.25. Only one legal grid (vox 0.15) ever existed. All CL-31 numbers void (CL-34 states the comparison itself does not stand).
- **CL-33** (hold since 2026-08-25, R5-CX-06) — prereg v2 verdict h1; sphere-stamp σ_e ratio → all values are p1 plate-rule products; `superseded_by_protocol: p2-occupied-surface-first`. The ratio is not protected by common-mode cancellation (κ_DBE = κ_SBE was never shown), and the plate rule touches σ_ion and STEP4 too.
- **CL-41** (same hold) — three-grid sphere-stamp ratio stability → same p1 problem. What survives shape-wise: the gain increases monotonically with refinement and does not stop; incremental ratio 1.773 vs the 2.187 floor any `R = R∞ − C·h^p` can produce ⇒ **no p > 0 fits, Richardson extrapolation is meaningless**. CL-72 then retracted even the "reported values are lower bounds" reading.
- **CL-58** (same hold) — doping-track σ_ion baseline at vox 0.15 sphere-stamp → p1 product.

**`rejected` (20) — historical failure specimens the discipline checkers must keep rejecting; if one passes, the rule has lost its teeth:**
- **CL-01** (VGCF is well wired; likelihood ratio 1 — both hypotheses predicted ≈4 % share, and 4 % *was* the defect size), **CL-02** (MPM measured f_AM itself; LR 1, replaced by R2.5-v2 z-slice), **CL-03** (point stamp electrically severs carbon; count→consequence leap, replaced by CL-06), **CL-16** (self-rejected: scalar diameter-preserving rescale impossible — the 42× spread was read off a mixed VGCF+PTFE population; VGCF is uniform Ø so the scalar **is** correct for σ_e).
- **CDX-09 / CDX-10 / CDX-11** — Stage 22.5 LOOCV 0.9531, Thermal T1 0.9028, ionic 0.9752 do **not** certify external/family-level generalization (case-level folds retain family information; selection was in-corpus).
- **CDX-12** — E_SE 1.35 ≡ 1.5 GPa "identical regime": equivalence language rejected (one seed inside three).
- **CDX-13** — four-pressure Heckel P_y = 137.8 MPa / 46 MPa as physical material quantities: rejected, descriptive fit only.
- **CDX-14** — d_h collapse R² = 0.926 as a transferable one-parameter collapse: rejected, exploratory.
- **CDX-15** — SDCP → 3.002 S/cm, +52.0 % as a physical headline: rejected (this is the origin of ban patterns 1/9/10/12).
- **CDX-16** — MPM 49.6/48.2 % vs DEM 48.3/51.8 % coverage as independent cross-validation: rejected, shared scaffold.
- **CDX-17** — "the same 18× softening is independently required by DEM and MPM": rejected; the kit maps DEM `e_se_eff_gpa` into MPM shear.
- **CDX-18** — Furnas dip "cross-validated by two independent tools": the word *independent* rejected.
- **CDX-20 / CDX-22** — f_AM band-membership (any value in [0.60,0.95] matching 0.847) and "0.847, 0.809, 0.880 are three independent confirmations": both rejected.
- **CDX-21** — three extrapolations agreeing at porosity 9.4–9.5 %: rejected (correlated error; this is ban pattern 6/7).
- **CDX-23** — voxel 11.76 vs DEM 11.75 mS/cm as mutual solver validation: rejected.
- **CDX-24** — voxel/DEM ionic ratio 5.7 reproducing dashboard 5.8: rejected; voxel ionic is explicitly an upper bound.
- **CDX-25** — 2D synthetic slice matching supplied 3D coverage: rejected, "target-conditioned rendering."
- **CDX-19** is the one **live** CDX claim (DEM AM-AM load fraction is pressure-sensitive on the audited four-pressure bed).

Ledger census: **104 claims — 74 live, 20 rejected, 6 hold, 4 retired.** Rule G in `check_method_discipline.py` errors if a superseded claim is left `live`; a `hold` claim treated as `live` is also an error.

---

### 3. THE 8–10 THINGS THAT ARE CURRENTLY TRUE AND MOST IMPORTANT (2026-09-08)

1. **Phase A's four 6 mAh beds (VGCF 1·2·3·4 wt%, PTFE 1) all completed at fixed Mach 0.03; the `seed × λ` thickness identity holds to ±0.015 % (±0.1 cell) and reached pressure varies only ±4 % across the composition axis — the Grade-B common-mode premise is now measured at both ends of the additive axis (CL-85, CL-83).**
2. **Reached pressure and bed state are decoupled: raising stress 9.6× on the same bed made it 0.2 µm *thicker*, so `settled_over_target` is not a measure of the bed and scaffold-run porosity must never be read as evidence of successful compaction (CL-82 ①, CL-80).**
3. **The platen stops kinematically, not at target stress — every Phase A run lands short of 300 MPa, and this is the repo's standing convention (Grade B: relative ordering at matched Mach), not a new blocker (CL-80, canon `docs/mpm_platen_kinematic_stop_defect.md`).**
4. **The voxel STEP3 solver sits on the branch this repo already named `CONTACT_FREE` — SE–SE faces get a harmonic mean and the Holm/Maxwell constriction term `R = 1/(2σa)` is exactly zero — and the gap size was already stored: `R_brug_over_full` median 4.04× (Hertz) / 6.69× (Physics) over n=157, triangulating with kim2025's GB-only 3.75× to within 8 % (CL-81).**
   > ⛔⛔ **이 항목의 마지막 절(문헌 삼각측량)은 철회됐다** — `SELF-24` · `L2-07`
   > (2026-09-13).  `R_brug_over_full` 은 **CONTACT_FREE/FULL** 이고 CF 는 **같은
   > 접촉망의 bulk-only 가지**이므로 그 배수는 **그 접촉 모델·그래프 내부의 민감도**이지
   > 실험 대비 오차가 아니다.  Codex 반례: 같은 4구에서 CF/FULL 3.6477 인데
   > Bruggeman/FULL 0.2771 — 하나는 1보다 크고 하나는 작다.
   > ⇒ **`3.75×` 삼각측량 문장을 인용하지 말 것.**  배수 4.04/6.69 자체도 재계산되지 않았다.
   > ★ **무너지지 않은 것**: 복셀 FV 가 CF 가지 위에 있고 Holm 항이 정확히 0 이라는
   >   **구조적 결론**은 그대로다 — L2 판정이 CF = bulk-only 임을 오히려 확인했다.
   > ⚠ 이 파일은 `check_review_findings.py:178` 의 `BAN_ALLOW_ALWAYS` 에 **영구 등재**돼
   >   자동 스윕이 **파일째 건너뛴다** ⇒ 이 표지는 **사람만 유지할 수 있다**.
   >   (표지 추가 2026-09-18, 원장 `GAP3-DOC` ㉘)
5. **That gap has two components with different prescriptions: geometric constriction improves with refinement, but the intrinsic interfacial resistance term does not exist at all and stays zero as h→0 — and the multiplier scatters 6× across the corpus (2.3–13.6×), so relative σ_ion comparisons are *not* automatically common-mode safe (CL-81).**
6. **The prereg's `bridge = 0` would have tied bridge geometry to the grid (0.300/0.240/0.180 µm across the three compared grids), reproducing CL-22; amended to a physical `BRIDGE_UM = 0.24 µm` common to all grids, above the √3/2·vox geometric floor where the miss rate is 0 % — amended with zero Phase A STEP3 results in hand (CL-87).**
7. **The closure joint sweep is DIRECTION-ROBUST: `R̄ − 3·SD > 1.01` at all nine grid points (minimum 1.0522), and σ_SDCP is asymmetric — ×100 changes the gain by only +3.5 % (saturated) while ÷100 removes 78 % yet still leaves R > 1, so the SDCP defense now rests on sensitivity, not on literature (CL-70).**
8. **σ_SDCP = 250 S/cm has no literature anchor: reference [35] (Patil 1987) is 3-substituted polythiophene, not an EDOT-class polymer, so the "material anchor" label is retracted and the canonical label is `Assumed (specified by the authors, S-PEDOT class)` — and the CL-47 band argument that rescues σ_VGCF = 100 does **not** transfer to SDCP (CL-61, CL-81).**
9. **The Methods/SI package is on SUBMISSION HOLD: the reported ratio 1.308 is **DBE/SBE** (it was written inverted), the grid is `334×334×490` at vox 0.15 (not 484 — the plate-gap arithmetic missed a 6-cell void cap), "only the electrolyte densifies" is refuted by the code (additives are material points receiving J2 updates; only AM is frozen), the 0.5–0.6 % origin figure is a *population* CV while the range is 1.7–1.9 %, and realized AM:SE mass is 72.25:27.75 against a nominal 70:27 (CL-86).**
10. **"Monotone across three grids ⇒ the reported value is a lower bound" is refuted by an elementary counterexample; conductivities are reported separately per spacing, grid convergence is *not* demonstrated, and the sign of the continuum error below 0.15 µm is unknown (CL-72, CL-74).**

---

### 4. LIVE vs CLOSED tracks

**LIVE:**
- **Phase A — 6 mAh VGCF+PTFE composition ordering (STEP3).** Prereg `docs/reviews/phase_a_6mah_order_prereg_20260907.md` (v2, post-Codex-R9). Four STEP2 beds done at Mach 0.03; STEP3 wiring verified; 96 arms (4 compositions × 3 grids 0.25/0.20/0.15 × 8 origins, `--no-ion`) not yet run. Immediate gate: the 4-arm bridge sensitivity check (`0.24` vs `0.30`, both end compositions, vox 0.25, ~1.5 h) with thresholds written first — `|Δd| ≤ 0.05` proceed, `0.05–0.20` proceed with a caveat, `> 0.20` stop and re-register. Verdict grade is B: ordering conditional on the Mach 0.03 convention. Ledger CL-71/72/74/75/76/77/78/79/80/82/83/84/85/87.
- **Manuscript / Methods + SI (SUBMISSION HOLD).** Five P1s from Codex, three of them authored in this session; four of five reproduced in-repo. Open: the Q3 reproduction gap (code default PTFE `off` yields 1.124 while the paper reports 1.308 under `centerline`) — author's call; the nominal run configuration (`VOX=.15`, `SDCP_SPHERE_D=.30`, `PTFE_STAMP=centerline`, 8 origins) must be recorded somewhere. `methods_simulation_v7_draft.md` still carries a PROVISIONAL banner (release conditions 5 and 7 partial). CL-86.
- **Voxel vs contact-network σ_ion cross-check (CL-81).** Canon `docs/voxel_contact_free_gap.md`. Not free: the repo has no bed with matched additive state on both discretizations, so it needs either one additive-free STEP3 σ_ion arm on a bed that exists in the DEM corpus, or bounding via the PTFE ion-blocking sweep. Binding citation rule while live: any STEP3 σ_ion absolute quoted next to experiment must carry "constriction/GB not included = `CONTACT_FREE` upper bound."
- **p2 plate-rule re-measurement.** Everything under CL-33 / CL-41 / CL-58 stays quotation-banned until a p2 (`p2-occupied-surface-first`) 8-arm GPU re-run exists.
- **Platen kinematic-stop defect × AM load sharing.** Canon `docs/mpm_platen_kinematic_stop_defect.md` (rev7). Fixing the stop alone makes it worse: R1 hit `wallP 0.3003 = target` but gave ε_sphere 1.13 % against experiment 15.6 % = 14.5 %p over-compression. f_AM remains unresolved (prereg §10-1 value comes from a forbidden path; §34 validation run not executed). CL-04.
- **Registered-but-unmeasured pre-run claims:** CL-44 (measured, h1), CL-45 (measured, BOTH_REJECTED), CL-48 (σ_VGCF single-fibre probe), CL-49 (PTFE electronic stamping — arm 0 only, no SE, ratio not quantitatively citable). CL-59's fourth convention arm (`r = 0`, SDCP ionically insulating) is still missing from the span table.
- **Open review findings — 19 items** (see §6).

**CLOSED / SETTLED:**
- SR-01 in its original form: the +52 %/+42 % headline family is finally retracted (CL-33 h1, though h1 means "the gain follows represented volume," *not* "SDCP does nothing").
- CL-59 (ionic `r` sensitivity): h0 — |R − 1| < 2 % under every convention, direction unidentifiable ⇒ Fig 4b's ratio is electronic-only, and the D13 / 8-arm ionic runs became unnecessary for the manuscript.
- CL-70 closure sweep (direction-robust across all nine grid points).
- CL-66/67 (PTFE geometry: `PTFE_D = 0.25 µm` anchored to Lee 2025 rope Ø 0.248; `PTFE_L = 40 µm` retracted to `Assumed`; the two PTFE geometry rows deleted from Table S2).
- CL-68 (OAT: friction is not a substitute for softening — 15.2× weaker), CL-69 (local LHS cannot estimate φ_c; its two `perc=0` cases are instrument artifacts).
- CL-75 (exact replay byte-identical 3/3 ⇒ the re-run component of `δ_num` is 0; the 0.108 % discrepancy was a stale, and wrong, committed artifact from before the plate-penetration fix).
- A1–A7, A9, A13, A14 digest-application backlog items.
- Phase 1 transport triad (σ_ionic / σ_e / σ_thermal scaling laws) — frozen forms; **do not re-screen φc, do not re-add the four dropped Stage 22.5 terms, do not re-fit the five locked exponents, do not push thermal higher.** Note the CL-12 banner: the thermal k_weight (5.7×) was never applied in production, so T1's *causal narrative* is not citable even though its numbers are.

---

### 5. STANDING CONVENTIONS THAT ALL CONTENT MUST OBEY

- **The ledger is canon over prose.** `docs/reviews/claims.json` beats CLAUDE.md beats `docs/*.md` beats wiki beats slides. `wiki/index.md` is a pointer layer and never replaces canon. Prose that restates a number without the ledger id is the failure mode this whole apparatus exists to stop (CLAUDE.md rule ④: canon leaks unless enforced from outside — a value refuted on 08-12 was re-asserted in a new 08-19 document and an independent review passed it as "consistent" against the stale canon).
- **A commit that retracts a number fixes the ledger and every derived document in the same commit.** A file-head banner explains a file; it does not fix a table cell (SELF-07: the one populated cell in Table S3 was a `hold` value while every other cell read `—`).
- **American spelling in manuscript prose — enforced by rule O** (`check_method_discipline.py`), scanning `docs/manuscript/methods_simulation_v7_draft.md` and every Methods/Table string inside `scripts/build_methods_docx.py`. Banned: `fibre`, `voxelisation`, `idealised`, `optimise/-ation`, `analyse/-ed/-ing`, `modelled/modelling`, `centre/centreline`, `behaviour`, `colour`, `labelled`, `whilst`, `sulphide`, `aluminium`, `micrometre`, `litre`, and the whole `-ise/-isation` family. Code spans in backticks and fenced blocks are exempt, so code identifiers (`fibre_stamp`, `--fibre-buckle`) must be backticked.
- **No model identifiers in pushed artifacts.** CLAUDE.md ("Never put the model identifier in commits/PRs") and `wiki/tools/lint.py` treats any model-ID pattern in a wiki page body or frontmatter as an **error**, not a warning.
- **Preregistration windows never move after results.** Each prereg carries the line "do not change this document's thresholds, windows, or verdict rules after seeing results; doing so voids the registration." CL-83 is the model case: two of the author's own pre-run predictions were badly wrong (one by 43×) and the window stayed put, so all four gradable predictions still stand. A judge printing `h0`/`h1` outside the registered scope is a **measurement statement**, not a hypothesis test (CL-41, CL-58) — write it as "under convention X at grid Y the ratio is Z," never as a verdict.
- **Bans on counting arguments:** a number is evidence only if the competing hypothesis's prediction sits on the same line (rule D1); if h0 and h1 predict the same value the likelihood ratio is 1 and the evidence content is zero (CL-01, CL-02, CL-03 are the canonical failures). Claiming a consequence from a count requires an explicit `bridge` field (rule D).
- **Filters are the blind spot.** Never select candidates by name fragment or file subset — run the real parser and enumerate the real manifest keys (rule M); an unclassified manifest key is HOLD *even if its value matches*. A `SE_PROXY` bed may not be used to assert σ.
- **`bash scripts/check_all.sh` before every commit.** `--selftest` asks whether the checkers are right; the bare run asks whether the repo is right; they do not substitute for each other. Both are re-run by `.github/workflows/discipline.yml` on push/PR with `fetch-depth: 0` (the checkers verify SHA existence). A ledger typo in this path is a fail-closed gate that blocks the user's GPU runs.
- **Measurement JSONs must carry the code SHA that produced them; without it, do not cite** (new standing rule from CL-75).
- **Grade-B labeling:** any comparison at matched Mach is relative-ordering-only; absolute values are not claimed. Any grid-swept quantity is reported per spacing, never extrapolated and never called a bound.
- **Bed-anchor labeling:** the whole vox 0.4→0.115 grid sweep sits on 2026-08-12 beds using SDCP E = 23.6 GPa, i.e. **before** ADD_E_SET (PTFE 1.80 / SDCP 9.00 GPa). Cross-grid comparison is safe because the bed is shared; absolute gains must be labeled with that anchor (CL-56, CL-42).
- **litdb duplicate checks use `git ls-tree FETCH_HEAD litdb/papers/`, never an INDEX file** — there are three indexes and searching only `INDEX.md` has already produced a near-duplicate of an existing 526-line card.

---

### 6. FINDINGS LEDGER (`docs/reviews/findings.json`) — 123 items: 19 open, 93 claimed_fixed, 8 verified, 3 wontfix; severity 93 P1 / 29 P2 / 1 P3. `status: verified` requires a verifier who is not the implementer.

**Open (19)** — SR-02 (the ±22.3 % Δσ_e figure has no committed raw/harness ⇒ evidence grade C, do not cite), SR-03 (STEP3 CG is Jacobi-only; 2.7 M-dof electronic solve = 58 min CPU; never swap solvers mid-experiment), DR3-05 (grid sweep is confounded with a σ_VGCF sweep because the diameter-preserving rescale is a function of vox: 78.54/113.10/176.72), DR3-06 (VGCF is rasterized as a 1-cell tube regardless of diameter ⇒ label the sweep "grid-convention sensitivity," not "grid convergence"), CDXIJ-2 (the verdict tool does not enforce the causal-input contract, exact 8 arms, origin pairing, or prereg nominal values; paired stats zip by filename sort), CDXR2-2 (`--fibre-dia` is not wired into the raster, loads after the solve, and swallows length mismatch = fail-open), CDXR2-5 (runner was not fully fail-fast; garbage arms could be cached permanently), R5CX-09 (SWCNT plate regression does not consume the production phase map), SELF-07 (Table S3's only populated value was a `hold`), SELF-10 (CL-39's convergence verdict has no discriminating power — batch means are unbiased at any resolution; per-particle CV is the quantity that moves, 26.1 % → 1.6 %), SELF-11 (**Q-B2 candidate**: SDCP is the only phase without contact quantization correction and the whole gain rides on it — at vox 0.15 it misses 35 % of true contacts and fabricates 32.5 % of 10 % gaps, two errors of opposite sign with different convergence rates, which is *why* no single `h^p` fits; and because SDCP is DBE-only there is no common-mode cancellation between beds), SELF-12 (the prereg's design justification `0.30 %` does not come out of the cohort it cites — recomputation gives 0.228 % paired SD, 0.667 % range), SELF-13 (all six phase σ values in `SIGMA_DEFAULT` are order-of-magnitude hooks; none is tied to a measurement), R20-03 (Bazzoun digest had a 100× unit error, `1 S/cm` for `1 S/m`, and an argument was built on it), R20-04 (the `83 → 100` derivation narrative is false — 100 predates the audit — and the recommendation to switch to 83 is itself refuted, since 83 is a compacted-powder specimen value while the voxel needs a local fibre closure), R20-05 (the "common scale protects the ratio" argument is refuted; the uncertainty lives in two independent contrasts `σ_AM_S/σ_VGCF` and `σ_SDCP/σ_VGCF` that do not cancel and can flip sign), R20-06 (calling the contact-network solver "physical ground truth" is overstatement, and it solves a different estimand — AM–AM only), SELF-15 (unread axis env vars silently ignored produced a run that gave *correct* numbers while testing nothing — the danger class is "right answer with no warrant"), SELF-16 (directory tag rule strips dots, collapsing the registered σ_SDCP grid points `2.5` and `25` into one name and silently reusing arms across two different experiments).

**Wontfix (3)** — R18-1/2/3, from the dropped Proposal A/B: A adds a new interfacial shell rather than restoring partial volume (PTFE volume has no rounding loss to restore — stamped 0.091792 vs target 0.091743); B's global rank `f` is not monotone in PTFE amount or distance and cannot express the intended semantics; and AM–AM bridges overwrite SE, so **no bridge-touching operator is electron-only** — removing a bridge returns that cell to SE and grows the ionic network.

**Verified (8)** — RC6-02/03/04/07/08, CDXIJ-1/3/6.