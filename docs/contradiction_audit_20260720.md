# 코드/md 모순점 감사 (2026-07-20)

워크플로 codebase-contradiction-audit(28 agents) 산출. 21개 검사 → 15개 REAL 확정. 각 후보 적대검증 통과분만.

# Prioritized Fix List — Verified Contradictions

**Verification tally:** 15 contradiction candidates were handed to me as the VERIFIED-REAL set; **all 15 survived verification (verdict = REAL).** I additionally re-confirmed 5 load-bearing code-side facts by direct grep (`mpm_dem_match.py` `--readout` default = `f50`; `mpm_input_from_case.py` `--step4-x100` = `0.9084`, `--step4-vmin` = `3.0`; `generate_comparison_plots.py` `_thermal_fit` alpha = `0.05`; `_SIGMA_S_LOCKED=10.0`/`_SIGMA_P_LOCKED=5.0` carry corrected single/poly comments; stale "18 features" comment at line 6646) — every check matched the JSON. The 15 candidates collapse to **5 root-cause areas / ~13 distinct fixes** (two σ_electronic-provenance items share one root; four SDCP items share one propagation root).

In almost every case **the code / dated data-file is correct and the always-loaded narrative (CLAUDE.md, or a manuscript body) is stale.**

---

## Severity-ranked summary (would-mislead-most first)

| # | Area | Issue | Correct side | Severity |
|---|------|-------|--------------|----------|
| 1 | SDCP manuscript/ledger | "Final" manuscript body + "ledger of record" still headline the superseded σ_SDCP=150 result (+45.4% / σ_e 2.871); ledger even forbids citing the real 250 result | σ_SDCP=250 → **+52.0% / 3.002 / share 7.3%** | **Critical** |
| 2 | MPM/DEM tooling | `mpm_dem_match.py` default readout is `f50` (trend-only, ~+14 %p wrong) but CLAUDE.md says default is `wallP` | code default is `f50`; doc wrong | **Critical** |
| 3 | σ_electronic provenance | σ_S=10 / σ_P=5 endpoints cited as "Trevisanello 2021 literature" — A1 (CLOSED) + code say they are corpus-fit values | code / A1: **corpus-fit, not Trevisanello** | **Critical** |
| 4 | STEP4 window | CLAUDE.md says production x100 = 0.854; webapp+kit already default to 0.9084 (~9% shift in I_1C) | code: **x100 = 0.9084** | **High** |
| 5 | σ_electronic provenance | CLAUDE.md labels σ_S=10 as "poly" and σ_P=5 as "single-crystal" — reversed vs NCM811 GB physics | code: **σ_S=single, σ_P=poly** | **High** |
| 6 | MPM/DEM tooling | CLAUDE.md:253 states MPM production E_SE = 1.35 GPa; champion + code default = 1.53 | **1.53 GPa** | **High** |
| 7 | STEP4 window | Review doc says new runs auto-reach full SOC via card v_min 2.5; every code path defaults v_min = 3.0 | code: **v_min = 3.0** | **High** |
| 8 | σ_thermal/electronic finalized | Ridge α claimed 0.1 in the FINALIZED section + plot title; code fits at 0.05 | code: **α = 0.05** | **Medium** |
| 9 | σ_thermal/electronic finalized | "16 features" header/integration line; production list = 14 (stale "18" code comment too) | code: **14 features** | **Medium** |
| 10 | σ_thermal/electronic finalized | EXCL count stated 21 (electronic) / 23 (thermal); code list = 25 (Rounds 1–7) | code: **25** | **Medium** |
| 11 | MPM/DEM frame | Top "controlling" frame[5] block lists Furnas dip as "Both"; CORRECTION 2 + 2026-06-16 division say DEM-only | **DEM-only** | **Medium** |
| 12 | SDCP | DBE R_geom = 9.36e-6 (manuscript/ledger, 150-run) vs 9.05e-6 (project doc, 250-run) | **9.05e-6** (250) — tiny magnitude | **Low** |

---

## Area A — SDCP σ_SDCP=150 → 250 headline not propagated (Critical)

**Root cause:** the σ_SDCP=250 re-run completed 2026-07-17 and its headline (σ_e **3.002 S/cm / +52.0% / e-share 7.3% / DBE R_geom 9.05e-6**) was recorded in `CLAUDE.md` and in the manuscript's top blockquote — but the manuscript **body/tables**, the numeric **ledger**, and the ledger's **top warning** were never updated. This is the highest-severity area because it is the **active manuscript track** and puts a wrong *headline number* into a paper, and one doc actively forbids citing the correct value.

**A1 — manuscript internal self-contradiction (Critical)**
- Stale: `docs/manuscript_sdcp_sigma_e_mechanism.md` §1 결론 (:26), §2 results table (:98), §3 ledger (:103), §4 main-text draft — all read **+45.4% / σ_e 2.871** (σ_SDCP=150).
- Correct: same file's blockquote (:9–13) + §8 (:272–275) give **+52.0% / 3.002** and explicitly instruct "본문 +45.4% 표기는 +52.0%로 교체할 것" — an instruction never executed.
- **Fix:** execute that self-instruction — update §1/§3/§4/§7 to σ_SDCP=250 values (σ_e→3.002, +45.4%→+52.0%, e-share 10.0→7.3%, DBE R_geom→9.05e-6). File is titled "최종판 (CLOSED)" yet self-contradicts; resolve before any paper text is lifted.

**A2 — ledger of record is stale AND actively forbids the correct number (Critical)**
- Stale: `docs/sdcp_318_base_sbe_dbe_comparison.md` — §3 table (:40,:49) = σ_e 2.871 / +45.4% / share 10.0%; §7 (:101) same; sweep (:53–58) lists only {15/50/150/1500}, no 250 row; the value 3.002 appears **nowhere**. Header (:5–7) says the 250 re-run is "교체 예정 … **실행 전 인용 금지**" (pending; don't cite before running) — now false, and its own dated note is stale.
- Correct: the run is done (per CLAUDE.md + manuscript + `docs/data/sdcp318_sigma_sdcp_sweep/sweep_summary.csv` 250 row → 3.002 / 52.0 / 7.3).
- **Fix:** add the 250 row to §3 + sweep, replace the DBE electronic block with 250 values, and **delete the "교체 예정 / 실행 전 인용 금지" warning** — it steers readers away from the true result. CLAUDE.md designates this file "수치 원장" (ledger of record), so its body must match.

**A3 — CLAUDE.md headline vs the docs it certifies as final (Critical, same root)**
- CLAUDE.md:160–166 correctly states +52.0% / 3.002 = "새 헤드라인" and names the two docs above as "(최종판)"/"(수치 원장)" — but those docs' bodies carry +45.4%. **Fix = A1 + A2** (propagate into the docs it points at). No change needed to CLAUDE.md's headline itself.

**A4 — DBE R_geom 9.36e-6 vs 9.05e-6 (Low, same root)**
- Stale: manuscript §3 (:103) + ledger (:44) = **9.36e-6** (150-run).
- Correct: `docs/project_rint_fullcell_cycling.md`:11 = **9.05e-6**, matching `…/sdcp318_sigma_sdcp_sweep/step3_sdcp250.json`:54.
- Magnitude ~3.3%, R_geom ≪ R_int → **no conclusion changes**; fix as part of the A1/A2 propagation. Also correct the ledger caveat's inaccurate "기하 축은 σ_SDCP 무관" claim (R_geom did move 9.36→9.05e-6 across the sweep).

---

## Area B — MPM/DEM tooling & frame (Critical → Medium)

**B1 — `mpm_dem_match.py` `--readout` default: `f50`, not `wallP` (Critical)**
- Doc: CLAUDE.md:440 — "…default **wallP** for the matcher."
- Code: `scripts/mpm_dem_match.py`:621 — `default='f50'`. The per-case matcher (`:492`) and composition sweep (`:466`) honor this f50 default.
- **Why worst-in-class:** CLAUDE.md:439 itself calls f50 "self-normalised = 22%, TREND-only, **rejected for absolute**." A session running the tool without `--readout`, trusting the doc, silently gets ~22% instead of the ~12.7% wallP absolute — a **~14 %p silent error** posing as a production number, with no guardrail. `docs/mpm_dem_wallP_crossvalidation.md` always passes `--readout wallP` explicitly, confirming the code default is not wallP.
- **Fix (prefer code side):** change the argparse `default` to `'wallP'` (the intended production readout per the section's own verdict); or, if the default must stay, correct CLAUDE.md:440 to "default f50 — pass `--readout wallP` for the 512 absolute porosity."

**B2 — MPM production E_SE: 1.35 vs 1.53 GPa (High)**
- Stale: CLAUDE.md:253 — "Production E_SE/σ_y for MPM = **1.35 GPa** / 0.3 GPa" (this was the 2026-06-06 first-cut value).
- Correct: CLAUDE.md:16 (controlling frame [1], FINALIZED), :265 (champion), :504 (LOCKED default), and `scripts/mpm3d_compaction.py`:164 (`--e-se default=1.53`) all say **1.53 GPa / σ_y 0.15**. (1.35 is the *DEM* effective modulus, not MPM.)
- **Fix:** annotate line 253 as the superseded 2026-06-06 first cut, or update to 1.53/0.15 to match the code default.

**B3 — frame[5] Furnas-dip ownership: "Both" vs DEM-only (Medium)**
- Stale: CLAUDE.md:74 — top "controlling epistemology" block (FINALIZED 2026-06-07) lists "Furnas dip presence/depth/location" under **Both**; part [3] (:44–50) still says "dip survives partially" in MPM.
- Correct: CORRECTION 2 (:469–484, 2026-06-10, labels the earlier co-location claim WRONG, proof by material sweep) + concrete division (:578, 2026-06-16) put the dip under **DEM-only** — the resolved-grain plastic MPM cannot reproduce it at any calibration.
- **Fix:** move "Furnas dip" from the "Both" list to the "DEM unique" list in the top block, and fix part [3]'s "dip survives partially" line. (The retraction lives ~400 lines away and never edited the authoritative block.)

---

## Area C — σ_electronic form provenance (Critical / High)

Both trace to **A1 (2026-06-30, marked ✅ CLOSED)**, fixed in code + `docs/a1_sigma_e_direction_closeout.md` but never propagated into CLAUDE.md's Stage 22.5 / Stage 21 "FINALIZED" derivation text.

**C1 — σ_S=10 / σ_P=5 falsely attributed to "Trevisanello 2021" (Critical)** *(merges JSON items #1 and #13 — same root)*
- Stale: CLAUDE.md:1388 "[LOCKED Trevisanello endpoints]", :1397 "σ_S=10, σ_P=5 mS/cm (Trevisanello 2021)", :1445, :1556, :1565.
- Correct: `scripts/generate_comparison_plots.py`:5710–5723 (A1 correction: "the OLD 'Trevisanello 2021' attribution … was WRONG — Trevisanello measured Li⁺ diffusion / BET / R_ct, NOT electronic σ_e … the σ_S/σ_P VALUES are OURS (corpus fit)"; comments "corpus-fit ~9.1/~4.1, rounded") + `docs/a1_sigma_e_direction_closeout.md`:8–23. Only the **NCM(r) GB-direction** is Trevisanello-supported, not the endpoint magnitudes.
- **Why Critical:** a manuscript session would falsely cite Trevisanello 2021 for corpus-fit values — a citation-integrity error the code explicitly repudiates; CLAUDE.md self-contradicts (backlog says "A1 CLOSED" while the derivation still carries the pre-A1 citation). Numbers agree (10/5) and LOOCV is unaffected — **text-only fix**.
- **Fix:** relabel Stage 22.5/21 σ_S/σ_P as "corpus-fit endpoints (NCM811 default, ~9.1/4.1 rounded to 10/5); Trevisanello supports only the NCM(r) GB direction, not the σ_e magnitudes."

**C2 — poly vs single-crystal labels swapped (High)** *(JSON #14)*
- Stale: CLAUDE.md:773–774 — σ_AM_eff ≈ 10 = "S-heavy **poly** NCM", ≈ 5 = "P-heavy **single-crystal**" (asserts poly > single for σ_e — reverse of GB physics).
- Correct: `generate_comparison_plots.py`:5722–5723 + A1 doc:11–14 — σ_S=10 = small **single-crystal** (no internal GB → higher σ_e), σ_P=5 = large **polycrystalline** (GB-reduced). A1 explicitly names this swap as a bug it fixed in code.
- **Note:** the surrounding block is tagged "(SUPERSEDED)", but the crystal-type direction is stated as bare fact, and the 10/5 values it mislabels are still live. **Fix:** swap the labels (σ_S≈10 = single-crystal / σ_P≈5 = poly) or delete the superseded 2026-05-29 checkpoint block.

---

## Area D — STEP4 discharge window (High)

**D1 — production x100 default: 0.854 (doc) vs 0.9084 (code) (High)**
- Stale: CLAUDE.md:167–168 (PENDING block, 2026-07-19) — "현 x0=0.264/**x100=0.854**"; grep confirms CLAUDE.md never mentions 0.9084.
- Correct: `scripts/mpm_input_from_case.py`:89 (`--step4-x100 default=0.9084`, overrides Chen 0.854) + `webapp/app.py`:5340–5345 + `docs/step4_assb_window_review.md`:65–71 (change marked DONE 2026-07-20). Every new STEP4 run now uses 0.9084 unless `&s4x100=` overrides.
- **Impact:** |x100−x0| 0.590→0.645 (~9%) → I_1C and all absolute discharge currents/capacities differ ~9% from what CLAUDE.md implies. **Fix:** update the PENDING block to "x100 default = 0.9084 (webapp+kit, 2026-07-20); x0=0.264 unchanged." (Other PENDING items — real NMC-vs-Li OCP anchor, I_1C convention doc, corpus re-run — remain genuinely open; only the "현 x100=0.854" clause is false.)

**D2 — v_min "card default 2.5 / full SOC" claim vs actual 3.0 (High)**
- Stale: `docs/step4_assb_window_review.md`:68 — "이제 모든 신규 STEP4가 x100=0.9084 + (카드)**v_min 2.5** 로 전 SOC" (present tense, automatic full-SOC to 2.5 V).
- Correct: every code path defaults v_min = **3.0** — `webapp/templates/single.html`:286 (`value="3.0"`), `app.py`:5336 (`_cut('s4vmin', 3.0, …)`), `mpm_input_from_case.py`:81 (`default=3.0`); and the **same doc** §3 (:35) says "v_min 기본 3.0."
- **Impact:** only x100 moved; with v_min=3.0 the cell hits the 3.0 V cutoff (~x≈0.88) *before* x=0.9084 (~2.5 V), so the 0.854→0.9084 tail is unreachable and "전 SOC" is NOT automatic — it requires an explicit `--step4-vmin 2.5`. **Fix:** correct §6 to state v_min default stays 3.0 (tail exercised only when 2.5 is set explicitly), or actually lower the card/kit v_min default to 2.5 to match the claim.

---

## Area E — σ_thermal / σ_electronic FINALIZED-section numeric staleness (Medium)

All doc-vs-code numeric drift where the CLAUDE.md "FINALIZED" narrative wasn't updated after a same-section refinement; **code is authoritative.**

**E1 — σ_thermal Ridge α: 0.1 vs 0.05 (Medium)**
- Stale: CLAUDE.md:1242 "(α=0.1)", :1264 "Ridge α=0.1 (NOT OLS)", and the hardcoded plot title `generate_comparison_plots.py`:6982 "[Ridge α=0.1, …]".
- Correct: `_thermal_fit(…, alpha=0.05)` (:6766) with all three production callsites (:6811/6866/6946) passing no override; CLAUDE.md:801 also says 0.05. Reproducing LOOCV 0.9028 at α=0.1 gives different coefficients than production. **Fix:** change CLAUDE.md:1242/1264 and the plot label at :6982 to 0.05.

**E2 — σ_thermal feature count: 16 vs 14 (Medium)**
- Stale: CLAUDE.md:1242/1264/1310 "16 features" (+ n/k 5.1:1 + "CODE INTEGRATION → 16 features"), plus stale code comments "18 features" at `generate_comparison_plots.py`:6637/6646.
- Correct: same CLAUDE.md section's refinement note (:1338–1342) says "Production now 14 features"; `_THERMAL_T1_FEATURES` (:6672–6691) has exactly 14 active entries. **Fix:** correct the "16" header/n-k/integration lines to 14 and the "18" code comments to 14.

**E3 — σ_electronic AUDIT-EXCLUDED count: 21 vs 23 vs 25 (Medium)**
- Stale: CLAUDE.md:1465 "21 (Rounds 1-6 cumulative)"; CLAUDE.md:1329 "23 σ_e EXCL cases"; supporting nit — the "THE 10 EXCL CASES" header (:1621) actually lists 11.
- Correct: `_EXCLUDED_NAMES_EL` (`generate_comparison_plots.py`:5604–5694) = **25 entries** (Rounds 1–7; Round 7 = `8mAh_real_14/_15` at :5687–5693). By the code's own round comments, Rounds 1–6 = 23, so "21" is wrong even for its stated scope. **Fix:** update electronic "21" and thermal "23" to 25, document Round 7 in the CLAUDE.md EXCL narrative, and fix the "10 EXCL CASES" header to 11.

---

## Cross-cutting note for the fix pass

Every item resolves the **same way**: the executable/dated artifact (code default, data JSON, dated correction) is correct, and a narrative doc is stale. Two structural failure modes recur and are worth a guard:
1. **CLAUDE.md "FINALIZED" sections not updated after their own same-section refinement/correction** (E1/E2/E3, B3, C1/C2) — the correction is written a few lines or a few hundred lines later but the headline/summary line is left intact.
2. **Headline propagated to CLAUDE.md but not to the docs CLAUDE.md certifies as canonical** (Area A) — and, worse, a stale "do-not-cite/pending" warning left in place after the work is done.

Recommended order of execution: **Area A first** (active manuscript, publication-facing, plus an actively-false citation prohibition) → **B1** (silent wrong production number) → **C1** (false literature citation) → **D1/D2, B2, C2** → **E1–E3, B3** (reproducibility/audit hygiene) → **A4** (cosmetic).
