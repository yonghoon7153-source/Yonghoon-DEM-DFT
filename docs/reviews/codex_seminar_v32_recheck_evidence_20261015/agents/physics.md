# v3.2 physics/status review notes

Scope: Q1, Q2, Q7 and the distinction between the old 300 MPa calibration target and generation-2 plans. Read-only review; no simulation, no production edits. Review date 2026-10-15 (KST). These are subagent notes, not the final verdict.

## Material outcome

No new P1 established in this scope. The new p11 visibly discloses history reset, unverified equilibrium and 13 SE losses. The new p15 visibly says “plan, no runs yet” and labels the density unverified. Those disclosures matter: neither page, read in full, says the pending campaign is validated or authorized.

One P2 wording correction is recommended on p11: “model-internal until the open checks pass” is an imprecise status boundary. Passing numerical equilibrium/conservation/history qualification does not promote a model-internal result to experimental validity. The endpoint can become interpretable as a nominal static model state; it remains a model result. Replace the clause with “model-internal diagnostic; static-equilibrium and conservation checks pending.” This is not a new numerical defect.

## Q1 — p11 causal interpretation

The main text calls the intervention a “servo branch ... (damping 1e-5).” The adjacent visible table states “Plate re-created at servo start: contact history reset,” status open. Notes explicitly identify the combined intervention of history reset, damping reduction and force hold. Therefore the important confound is already on the slide, not hidden exclusively in speaker notes.

Implementation independently confirms a joint intervention: `in.branch_B.liggghts` lines 214–246 deletes `zwall_top` and `top_mesh`, builds a new servo mesh and `wall/gran`, then deletes/recreates global damping at 1e-5. This is not a clean servo-only or damping-only comparison. A stronger main sentence would be:

> A combined follow-up protocol (plate-contact history reset, lower damping and force hold) changed thickness from 111.05 to 105.84 µm. The endpoint remains a model-internal diagnostic pending static-equilibrium and conservation checks.

The prior model-validation Q11 wording permits reporting the observed changes of the registered follow-up protocol, subject to those qualifications. It does not allow attributing the entire change to removal of damping or treating a predicted-band hit as validation.

## Q2 — numbers and plot interpretation

The supplied F_p4 CSV/plot strings agree with the recorded README §1/§4/§12-4 values. The following calculations were independently performed from the reported values (not a raw-dump remeasurement):

| Calculation | Result |
|---|---:|
| 105.842 − 111.052 | −5.210000 µm |
| 100(105.842/111.052 − 1) | −4.6914958758% |
| 10.769 − 14.953 | −4.184000 percentage points |
| 434.18/750 ×100 | 57.8906666667% |
| 434.3/750 ×100 (older rounded record) | 57.9066666667% |
| (300.906−165.34)/300.906 ×100 | 45.0526077911% |
| 13/160420 ×100 | 0.0081037277% of particles |

Thus the 57.9% shown inside the stop-pressure bar is a drag/target-force ratio, not the measured pressure relaxation fraction (45.05%) or an independently identified partition of the top-plate force. The text correctly says “of the target force.” Do not say “subtract 57.9% to obtain the static pressure.”

The band 8.3–11.7% was present in the older pre-result README §4 B2, as was the 103–107 µm thickness band. p11 labels it registered before the run and hatches the servo-end value with an explicit open-check caption. It is a model prediction interval chosen in the registration, not an experimental interval, confidence interval or validated target. A short “registered prediction band” label would make this clearer but the current full-slide reading does not state experimental agreement.

The plotted pressure values round correctly: 300.906→300.9, 165.34→165.3, 299.274→299.3 MPa. The plotted sphere-volume values round correctly: 14.953→14.95, 10.769→10.77%. The notes preserve the distinction from earlier union-porosity panels.

Force unit caution: 750 N is explicitly labelled “deck units.” At 300 MPa over the physical 50×50 µm area, the corresponding force is 0.75 N. Do not drop the scaling qualifier in oral explanation.

Loss consistency check: the rounded thickness/porosity pairs imply sphere-volume sums 236115.9861 and 236109.68755 µm³, a difference of 6.29855 µm³. Thirteen 0.5 µm-radius SE spheres have 6.80678408 µm³ volume. The ~0.508 µm³ difference is below the rounding uncertainty of the displayed porosities. The numbers are consistent with the stated loss; they do not certify conservation. Treating all lost particles as negligible merely because the particle-count fraction is small remains inappropriate for a conservation certificate.

## Q7 — p15/p16 status and future calibration

### Unloading

The actual prior re-read evidence (`dem_unloading_kit_reverify_20261014/evidence/history_reread.json`) has H0–H5 PASS, while the kit verdict remains HOLD. The slide’s separation “history test passed; kit re-review HOLD, fixes ratified” is therefore appropriate. H0–H5 is a narrow contact-history/restart test, not proof that the full unloading experiment ran or passed. The main text does not claim that.

### Generation 2

“Plan, no runs yet” is visible and the notes state that a plan document, author ratification and review still follow. “Heckel analysis redone” would read more naturally as “Heckel analysis to be redone,” because no new result is available. This is a minor tense correction, not a scientific finding.

The proposed ε_union=10–13% target is not an independently validated experimental measurement operator. The notes explicitly preserve MV-03: choosing union alone cannot resolve disagreement with mass-based porosity. The visible line should ideally say “provisional geometry target; experimental definition/state matching pending.” Otherwise the exact-looking range beside “lab standard” can look more established than the accompanying plan disclaimer warrants.

This does not require deleting the generation-2 plan from a seminar. It does require keeping presentation approval separate from approval to fit E to that target. A mass/density/area/thickness experiment measures ε_mass=1−m/(ρAh), not automatically a geometric union. The future plan must freeze the experimental load/unload state, density basis, measurement operator and numerical qualification before recalibration. The old p5 10% calibration target and new p15 10–13% geometric target must not be described as the same validation series.

The p16 summary line should remain: it accurately flags that the nominal 300 MPa loading criterion includes damping and that revision is planned. It introduces no new magnitude and does not universalize the one-bed 57.9% result.

## Visual inspection and limitations

Viewed supplied full-slide PNGs 11, 15 and 16. No clipping or missing warnings identified on these three slides. The p11 caveat table is visible next to the figure. p15 has visible plan/no-runs and unverified-density labels. Actual PowerPoint rendering and complete deck inheritance are the parent agent’s tasks.

## Addendum — pin source and raw run records obtained

Read `source/docs/data/ps73_damping_branch_20261007/ibb_20261009/B_20261009_101443.report.tgz` directly without extraction or execution. Its SHA256 is `9cb7100b5ce1da6e32bc87975af2dfc25ca6ff81804b05fdf0424b58b12f5db1`, matching the recorded receipt. Archive has raw `log.liggghts`, `screen.out`, plate meshes, `branch_trace.csv` and derived `analysis_branch.json`; it does **not** include the atom dumps named inside the analysis JSON.

Independent original-record checks:

- Normal integration thermo at step 3,125,000: atoms 160420, KinEng 1.6950666e-05, pressMPa 0.30090644 deck units = 300.90644 physical MPa.
- Normal integration thermo at step 3,735,000: atoms 160407, KinEng 2.175747e-07, pressMPa 0.29927373 = 299.27373 physical MPa.
- Stop and end plate STL vertices have constant z 0.111052 and 0.105842 deck m, respectively. Under the recorded length scaling these reproduce 111.052 and 105.842 µm.
- `branch_trace.csv` records stop pressure 0.300906437914227, end 0.299273726411317, end z 0.105842060204728. The small STL precision difference does not affect the slide rounding.
- Same-timestep setup/run-0 rows are different: 326.70943 MPa at stop and 326.05006 MPa at end. The slide uses the correct normal integration endpoint, not these setup artefacts.
- Derived analysis JSON has stop solid-volume sum 0.00023611582065890635 deck m³, end 0.0002361090138748218. Their difference is 6.80678408455 µm³, matching exactly thirteen 0.5-µm SE spheres to the recorded precision. Phase counts are 280/1376/158764→280/1376/158751. Because the actual atom files are absent, this phase and radii statement remains an audit of the saved analyzer output, not a new atom-level census.
- Saved analyzer output has drag 434.18047796400066 N and drag share 57.89073039520009%, ε_sphere 14.953059590495876→10.769254596541355%, Δε −4.183804993954521%p. Those round to the slide exactly. Velocities and individual radii cannot be independently re-summed from this report archive.

The original-run relaxed pressure 165.34 MPa is a different path from B, correctly labelled “original run” in the figure caption. Independently read the earlier verified source archive `dem_unloading_kit_reverify_20261014/source/docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz`, member `home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_r8_220537.out`: normal integration row 3,225,000 has atoms 160417, KE 1.2554088e-07, pressure 0.16534203 deck MPa = 165.34203 physical MPa. That supports the plotted 165.3 and recorded 165.34. This is source raw-log evidence, not a new run. Its atom loss (3) is different from B's loss (13), another reason not to regard the three bars as one uninterrupted branch.

## New P2 — p15 no longer matches the author's latest ratified sequence at the same pin

This is a concrete source-to-slide mismatch, independent of the unresolved calibration question.

- At `source/docs/session_20260923_progress.md:1067`, the **10-14 night 7** record says Q1/Q7/Q8 are ratified as recommended, with the explicit order **relaxation → unloading → platen separation**.
- The **night 9** record at line 1069 records the v3.2 deck import later in the same sequence.
- Actual p15 flow is **relaxation → platen removal → unloading**. Its speaker notes repeat that order. The slide builder and slide-text source agree with the wrong order, so merely rerendering will not fix it.

These are different protocols for the hysteretic system: removing the platen is an abrupt release, while controlled unloading before separation maintains contact until the specified zero-load/separation event. The new plan's latest ratified sequence should be displayed. Minimum edit: swap the last two p15 boxes to “unloading → platen removal” and update notes/build/source map. This does not require a new simulation or invalidate the reported generation-1 numbers.

Proposed finding ID for parent assignment: `SEM32-PH-02`, severity P2, current author decision mismatch. Confirm the exact draft clause if the full plan document is fetched; the ratification sentence already provides direct evidence.
