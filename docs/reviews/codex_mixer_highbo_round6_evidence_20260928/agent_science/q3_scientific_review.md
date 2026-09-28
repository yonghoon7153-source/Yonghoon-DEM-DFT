# Q3 stiffness-validation review

Scope: read-only source review and synthetic arithmetic for pinned snapshot `18787ab98a13361c37b2343bd07ae276142d0953`. No DEM executable, campaign frame, Git mutation, or production edit was used. `stiffness_probe.py` imports the actual generator with bytecode disabled and reports exact generator outputs plus explicitly labelled contact-law approximations.

## Main finding

The proposed SE-only stiffness test is useful development work but is not yet a validation design. Its timestep estimate is approximately correct. Its claim that SE x14 brings the observed maximum below 1%, and its blanket assertion that the generator holds Bo fixed, are not correct even within the generator's own small-overlap Hertz/SJKR approximation. An early-plateau test or new E0/L0 seeds alone cannot validate the registered 8-turn LC-minus-LH estimand.

## Generator arithmetic

Source anchors: `scripts/make_mixer_deck.py:132` (SE baseline E and overlap convention), `:142` (phase moduli), `:192`–`:222` (same-type E*, overlap and Bo inversion), `:337`–`:388` (pairwise min CED and wall construction), `:408`–`:459` (plan and timestep), `:728` and `:737` (hertz/history/sjkr/cdt).

Production geometry from `plan(100000, cgf=151.4)`: particle diameters AM_P 0.0013626 m, AM_S 0.0006056 m, SE 0.0001514 m; drum R=0.013137687235248028 m.

| Quantity | Baseline | SE E x14 |
|---|---:|---:|
| SE E, Pa | 1.0e7 | 1.4e8 |
| AM–SE E*, Pa | 10,880,913.2832 | 135,061,213.8578 |
| SE–SE E*, Pa | 5,494,505.4945 | 76,923,076.9231 |
| SE–wall E*, Pa | 10,915,259.2374 | 140,550,807.2175 |
| 20%-Rayleigh AM_P dt, s | 1.5873496531e-6 | unchanged |
| 20%-Rayleigh AM_S dt, s | 7.0548873472e-7 | unchanged |
| 20%-Rayleigh SE dt, s | 1.1718901912e-6 | 3.1320082788e-7 |
| limiting phase | AM_S | SE |
| generator dt, s | 7.0548873472e-7 | 3.1320082788e-7 |
| emitted deck dt, s | 7.055e-7 | 3.132e-7 |

Thus dt shrinks by **2.252512356**, not sqrt(14), because the limiting phase changes. The generator comment at :447 saying SE currently limits dt is stale. This is a step-count estimate, not a measured wall-clock-cost promise. Actual emitted timestep, run counts, physical settling time, rotation period, and output cadence must be recorded because the deck rounds dt to four significant digits (:730) while deriving run/dump counts from full precision (:564–566).

For a fixed external load, Hertz gives delta proportional to E*^(-2/3). AM–SE E* grows **12.412672571**, not 14. Applying that conditional relation to the already observed AM_P–SE maximum 5.763% gives **1.074991639%**, still above 1%. The formal SE multiplier needed to make this one fixed-load extrapolation 1% is **15.85666649**, without any reserve for other contacts or network changes. For fixed collision velocity and mass, the elastic impact relation instead gives delta_max proportional to E*^(-2/5), yielding **2.104275021%** from the same starting number. Neither calculation predicts a new network's maximum; they distinguish assumptions. LH forces and velocities have not been measured and need not match E0.

### Actual CED matrices

Order is AM_P, AM_S, SE, WALL. Units J/m3. These are generator values before deck decimal formatting.

Baseline LC:

```text
108795.275037 108795.275037 10458.232424 59063.162232
108795.275037 142562.140392 10458.232424 77394.637068
10458.232424  10458.232424  10458.232424 5677.602066
59063.162232  77394.637068  5677.602066  0
```

SE x14 LC:

```text
108795.275037 108795.275037 60749.631302 59063.162232
108795.275037 142562.140392 60749.631302 77394.637068
60749.631302  60749.631302  60749.631302 32979.973881
59063.162232  77394.637068  32979.973881 0
```

Baseline LH:

```text
3563475.400947 2719440.696302 10458.232424 1934552.080927
2719440.696302 2719440.696302 10458.232424 1476339.546665
10458.232424   10458.232424   10458.232424 5677.602066
1934552.080927 1476339.546665 5677.602066  0
```

SE x14 LH:

```text
3563475.400947 2719440.696302 60749.631302 1934552.080927
2719440.696302 2719440.696302 60749.631302 1476339.546665
60749.631302   60749.631302   60749.631302 32979.973881
1934552.080927 1476339.546665 32979.973881 0
```

### What Bo inversion does and does not preserve

At small overlap write F_net=A delta^(3/2) - B delta, where A=(4/3)E*sqrt(R*) and B=2*pi*R*CED. Then delta0=(B/A)^2, zero-load adhesive force F0=B^3/A^2, and pull-off in this approximation is (4/27)F0. CED proportional to E*^(2/3) preserves those force scales for a particular pair with fixed geometry/mass. The generator instead inverts same-type E and takes the smaller phase candidate for mixed pairs (:378–382), and divides each same-type diagonal to make its wall entry (:384).

| Pair | E* ratio | CED ratio | F0 / Bo ratio | zero-load delta ratio | separation-work ratio |
|---|---:|---:|---:|---:|---:|
| AM_P–SE, AM_S–SE | 12.412672571 | 5.808785734 | **1.272112360** | 0.218997983 | 0.278590041 |
| SE–SE | 14 | 5.808785734 | 1 | 0.172153019 | 0.172153019 |
| SE–WALL | 12.876543210 | 5.808785734 | **1.182108914** | 0.203503618 | 0.240563441 |
| AM–AM and AM–WALL | 1 | 1 | 1 | 1 | 1 |

Ratios of Bo mean the same fixed mass/weight convention before and after; no claim that mixed-pair Bo equals the declared same-type Bo. Ratios apply to the generator's **small-overlap, adhesive-dominated, isolated-contact** definition. The actual deck selects `sjkr`, whose finite-overlap sphere-intersection area differs from 2*pi*R*delta. They are not exact engine measurements.

Even perfect pairwise preservation of this approximate Bo would not preserve adhesion separation work: U_sep=B*delta0^2/10 is proportional to E*^(-2/3) under fixed force-scale Bo. Contact time, contact area, shear stiffness, damping coefficients, friction-history evolution, sticking and detachment dynamics also change. Keeping the input restitution and friction coefficients fixed is useful but does not prove invariant cohesive collision outcomes. SE-only scaling additionally changes the AM/SE modulus ratio 103.7 to 7.40714. Decide whether the tested object is an SE-only counterfactual (legitimate, limited scope) or a convergence path preserving phase-modulus ratios; do not call them identical.

Official implementation references checked: [Hertz law](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/normal_model_hertz.h), lines 198 and 216–222; [SJKR area](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/master/src/cohesion_model_sjkr.h), lines 85–89; [timestep criteria](https://www.cfdem.com/media/DEM/docu/fix_check_timestep_gran.html). These are current upstream references, not a verified source binding to the ibb executable. Bind the planned test to the actual binary/source before claiming exact law identity.

## Minimal preregistration that can answer the proposed question

1. **Freeze the estimand and population.** Primary quantity remains d_s=M_final(LC,s)-M_final(LH,s), M_final being the complete registered bin 7 of eight revolutions. Define q_s=d_s(soft)-d_s(reference stiffness). Declare the seed sampling rule and target domain (these exact cases versus a population of equivalent seeds), including 100,000 particles, composition, geometry, Fr, insertion/settling treatment and LC/LH contact matrices. Source: high-Bo prereg :82–92 and :175–179. The existing flatness rule does not establish stiffness invariance at eight turns.

2. **Separate development from confirmation.** Existing E0 outcomes and the x14 extrapolation are development evidence. Use separate pilot seeds to pick stiffness levels, contact invariant, sample size and failure rules; lock them before independent holdout seeds. Fresh E0 can validate normalization and static overlap, while L0 probes noncohesive layered motion. Neither covers cohesive LC/LH nor the high-Bo arm, so neither alone releases the extension. At each held-out seed, the minimal effect-validation block is LC and LH at soft and reference stiffness plus the matching E0 normalization at each stiffness: four full eight-turn trajectories and two settle-only references. Extra convergence levels need not repeat every development job, but the chosen reference must have independent evidence of adequacy.

3. **Qualify the reference.** A larger E is not automatically ground truth. Before holdout outcomes, demonstrate that the selected high-stiffness condition satisfies the chosen contact-validity criterion across relevant pair/wall populations and that its result is insensitive within the allocated error to a further stiffness refinement. Check timestep convergence at fixed stiffness separately (e.g. half dt), otherwise stiffness and integration error are confounded. A selective SE change validates only that path; it does not demonstrate insensitivity to AM or wall stiffness. The tests can establish numerical robustness for the chosen observable and model; they do not supply experimental validation of real material behavior.

4. **Retain the endpoint; permit a short pilot only.** The observed early plateau was at the old stiffness and conditions. It cannot bound future drift, segregation, agglomeration, or the stiffness interaction in LH. Short runs may reject an unsuitable candidate cheaply, but cannot certify the eight-turn primary endpoint. Either run confirmatory tests through eight turns or explicitly preregister a different short-time scientific claim, losing the eight-turn transfer claim.

5. **Register a contrast error budget.** A candidate b_E=0.02 is a transparent policy allocation of 20% of the registered minimum relevant difference 0.10; the literature does not justify that fraction. State why 20% is tolerable, what other uncertainties use the remainder, and the decision guard band. Estimate q_s directly with independent seed replication. Bounds |M_soft-M_ref|<=0.02 on each arm separately only imply |d_soft-d_ref|<=0.04; use 0.01 per arm for a conservative 0.02 contrast bound, or test the paired contrast directly. An equivalence CI must lie within [-b_E,+b_E]; failure to find a difference is not equivalence. Freeze CI level, sample size/power basis, multiplicity rule if using trajectories, and the inconclusive outcome. Three seeds are not automatically sufficient; frames within a run are not independent replicates.

6. **Propagate the reference and threshold uncertainty.** M=(S0-S(t))/(S0-SR), with the quantities here denoting variances. The E0 denominator is part of the observable. Use the same declared normalization protocol at each stiffness and report S0, SR, S(t), cell inclusion/counts and paired M. Reusing one old E0 can hide denominator sensitivity; changing E0 can produce a real numerical pipeline effect that belongs in q_s. Even with identical S0 for both arms, d=(S_H-S_C)/(S0-SR), so shared E0 does not algebraically cancel. State how the error band affects both the 0.10 effect threshold and the 2*SE criterion; a case near either boundary is indeterminate unless the bound establishes the classification. Merely demonstrating b_E=0.02 does not justify unguarded classification of a measured Delta=0.101.

7. **Fix the contact statistic and observation contract.** Preserve or explicitly amend the original snapshot maximum definition: delta/r_min for particle pairs and delta/r for walls; exact phase/pair populations; all stored frames from t0 through the endpoint; rigid-self exclusions; missing/duplicate/nonfinite data rules; loss/type/radius preservation; measured wall geometry/phase uncertainty; reporting of maxima, p99/p99.9 and exceedance counts. A mean or tail quantile cannot silently replace a maximum, nor can a 1%-diameter statement silently replace 1%-radius. Specify an envelope for the validated stiffness/model/Bo domain and a fail-closed rule if holdout tails exceed it. If the claim concerns every integration step, stored frames are inadequate: add appropriate online/integration-scale maxima or explicitly retain NOT OBSERVED between frames. Source: high-Bo prereg :94–137.

8. **Freeze implementation and keep validation independent of the efficacy decision.** Seal generator/reader/checker versions, exact emitted decks and CED matrices, binary/build, machine/rank count, precision, dt policy, seeds and initial-state protocol. Comparing same seed on the same rank controls a source of variation but does not guarantee identical settled beds once contact laws differ. Keep the original full insertion-plus-settling treatment if validating the original total intervention. A common post-settling checkpoint answers a conditional rotation-only intervention and must be separately labelled. Holdout results can release or fail the frozen validation; using them to tune stiffness or acceptance makes them development data and requires a new holdout.

## Paulick primary-source status and limits

[Publisher record](https://www.sciencedirect.com/science/article/abs/pii/S0032591015002533) independently confirms Paulick, Morgeneyer and Kwade, *Powder Technology* 283 (2015) 66–76, DOI 10.1016/j.powtec.2015.03.040; its abstract states that lowering elastic parameters to reduce runtime can change the numerical response. Its visible section snippet classifies slow mixing among dense contact systems. [UTC institutional publication list](https://timr.utc.fr/productions-scientifiques-timr/publications/) confirms the citation.

The publisher exposes only preview/section snippets in this review environment. Attempts through the article, DOI, publisher text API and institutional repository searches did **not retrieve the full paper**. Accordingly the specific assertions about **1% of diameter**, **maximum versus average**, and **low-energy applications using average** are **not independently primary-text verified here**. The local literature card in the separate friendly_meitner_6abaae3 snapshot quotes those claims; it is secondary internal interpretation, not a substitute for the paper. Do not mark those sentences primary-verified or use the card as an independent holdout.

Even if the full paper confirms the quotations, a broad review's overlap heuristic cannot by itself certify a 1% radius maximum for this polydisperse cohesive mixer or authorize 2.3–2.9% diameter overlaps. It does not establish a 0.02 mixing-index error bound. The required bridge is observable-specific, domain-specific validation as above. The exact page/paragraph, statistic, diameter definition for unequal particles, and scope should be recorded from the primary full text before it becomes the normative support for an amended D-1 contract.
