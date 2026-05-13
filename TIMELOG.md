# TIMELOG — 세션 작업 기록 (방 터졌을 때 빠른 복구용)

> **규칙**: Claude는 모든 작업 시작/완료 시 이 파일에 한 줄 추가.
> 형식: `YYYY-MM-DD HH:MM | branch | action | status | notes`
> status: START / DONE / BLOCKED / CRASHED-RESUME-NEEDED
> 가장 최근 항목이 위로 오도록 (역순).

---

## 📌 PENDING (오늘 미루고 나중에 할 것) — 2026-05-13 기준

| Priority | 작업 | 상태 | 재개 방법 |
|----------|------|------|----------|
| MEDIUM | **comp3 v2 DFT EOS** (KISTI GPU0) | ▶ 진행 중 (v098 BFGS step 1) | `auto_restart.sh` 자동 재시작. 며칠 더. `comp3_lpscbr/dft_eos/v098-v108/relax.out` 확인. |
| MEDIUM | **comp5 v2 DFT EOS** (KISTI GPU1) | NOT STARTED | comp4 paper scripts (gen_dft_eos_comp4.py, run_dft_eos.sh, auto_restart.sh) copy → sed comp4→comp5 → champion symlink → `nohup ./auto_restart.sh`. v104 grid center (MLIP V0/V_cell=1.0414). |
| LOW | **EOS priority 3-vol strategy** | NOT IMPLEMENTED | 빠른 V0/B0만 필요하면 ALL_VOLS reorder: comp3="103 102 104 ..." / comp5="104 103 105 ...". 3 vols (~30h) 후 parabolic fit. |
| LOW | **comp3 anneal_chain resume** | KILLED at 8/25 pairs | r0 (5/5) + r1/li0-li2 done, r1/li3 was at MD 75%. Resume: re-launch watchdog, chain skips done pairs. r2-r4 unlikely to beat r0/li0 (-256.370). |
| LOW | **comp5 anneal_chain resume** | KILLED at 10/25 pairs | r0+r1 fully done. r2-r4 unlikely to beat r1/li1 (-254.919). Champion finalized. |
| LOW | **comp3/5 post-processing** (Bader/PDOS) | NEEDS V0 DFT EOS done | After DFT EOS → tight SCF → pp.x + projwfc.x. Reference: comp4_lpscbrbr/dft_eos/v0_fit/ structure. |
| LOW | **comp3/5 v2 bond length analysis** | NEEDS V0 structure | mic distance from V0.xyz + cutoffs (Li-O 2.8, Li-S 3.0, Li-Cl 3.2, Li-Br 3.4 Å). |

## 📌 TODAY'S FOCUS — 2026-05-13

**Goal:** Adhesion paper figure 오늘 안에 완료

| 시각 | branch | action | status | notes |
|------|--------|--------|--------|-------|
| 15:17 | debug-api-500-error-iukkt | comp5 champion 추출 + MLIP EOS done | DONE | rank1/li1, E=-254.919 eV. V0=1254.04, B0=22.0 GPa (paper v1: 20.8, Δ+1.2). V0/V_cell=1.0414 → v104. |
| 15:14 | debug-api-500-error-iukkt | comp5 anneal_chain stop (10/25 pairs done) | DONE | r0+r1 fully done. Champion = r1/li1 -254.919 eV. r2-r4 안 돌림. |
| 14:43 | debug-api-500-error-iukkt | comp3 v2 DFT EOS KISTI 시작 (paper protocol K=2x2x1) | START | gen_dft_eos_comp4.py mirror + auto_restart.sh. GPU0. v098 BFGS step 1 진행 중. |
| 14:37 | debug-api-500-error-iukkt | comp3 anneal_chain stop + champion 추출 | DONE | r0/li0 = -256.370 eV. anneal_champion.xyz saved. |
| 11:47 | debug-api-500-error-iukkt | gabia v30u_1L 시작 (1L NCM PRESERVED, 5z×36xy, 6 comps) | START | paper protocol replica. comp1+2 done, comp3 진행 중. ~16:30 완료 예상. |
| 09:24 | debug-api-500-error-iukkt | comp3 v2 MLIP EOS (gabia) | DONE | V0=1236.55, B0=23.20 GPa. R²=0.9999. V0/V_cell=1.0268 → v103. |
| earlier | debug-api-500-error-iukkt | v30u_full_ensemble 분석 (3L NCM, 5z×36xy) | DONE | R=+0.92 (5 paper comps). Wells tiny (~3 mJ/m², 3L NCM convergence). |
| earlier | debug-api-500-error-iukkt | comp4 v1 swap (v2 anneal Cl exposed anomaly 발견) | DONE | comp4_slab_v1_PRESERVED.xyz (KISTI). R=0.92 → 0.93 회복 (1L에서는). |

## 🎯 핵심 발견 — adhesion paper

1. **OLD figure (1L NCM, 36 xy mean, R=0.931)** — paper-acceptable, paper draft 시점 검증된 figure
2. **Wad 절대값 1L NCM artifact로 paper-scale align** (1L "broken structure" per inventory)
3. **paper exp는 aJ 단위 (R=10nm tip), mJ/m² 변환 model-dependent (factor ~2)**
4. **UMA Wad : paper Wad = 0.32 ± 0.03 ratio (consistent across 5 comps)** — systematic ~3x scaling, NOT calibrated/cherry-picked
5. **Rank order R = +0.93 robust** — Li5.4 family >> Li6 family (~100+ mJ/m² 차이)

---

## 2026-05-11

| 시각 | branch | action | status | notes |
|------|--------|--------|--------|-------|
| 07:18 | debug-api-500-error-iukkt | kisti_monitor.sh 작성 (엄청 자세한 watch) | DONE | `필독/step1_halogen_li_anneal/kisti_monitor.sh` — GPU 사용량/온도, ps, watchdog crash count, Stage1a/1b/2/3 진행 카운트, run.log age, last 3 lines, champion 발견 시 best_cl/br/Li/E 자동 print. `watch -n 30 ./kisti_monitor.sh` 사용. |
| 07:10 | debug-api-500-error-iukkt | figure 보정: image1 (v4) → image2 style 복원 | DONE | (a) 원인: `plot_binding_curves_v4.py` 가 max-over-registry CSV 읽고 modelC 포함 + cubic spline 없음 + asymptote subtract 후 Y range 매우 넓음. (b) 처방: `plot_binding_curves_v7.py` 작성 — JSON 기반 mean over 36 + asymptote subtract + 5 paper comps 만 + cubic spline + gap window 1.2-1.6 음영 + R(well, paper) title + auto-fit Y. (c) v4 에 DEPRECATED warning 추가. commit `f8f59f7` |
| 06:58 | debug-api-500-error-iukkt | portable scripts commit + push | DONE | commit `92b14a5` |
| 06:56 | debug-api-500-error-iukkt | watchdog/run scripts portable화 (cwd-relative + conda activate 제거 + GPU env 외부 주입) | DONE | comp3/comp5 watchdog + run_ranks 모두. `cd "$(dirname "$(readlink -f "$0")")"` 사용. fairchem import sanity check 추가. |
| 06:55 | debug-api-500-error-iukkt | KISTI deploy v1 실패 확인 | BLOCKED→FIXING | (a) `/data/work/`은 gabia 경로, KISTI는 `/scratch/x3430a02/kgy/...` → `mkdir` Permission denied → wget 파일들이 `adhesion_v5_v2/` 로 잘못 들어감. (b) `/data/apps/miniforge3/...` conda path 도 gabia용. KISTI는 `(uma)` 이미 active. |

---

## 2026-05-10

| 시각 | branch | action | status | notes |
|------|--------|--------|--------|-------|
| 21:52 | debug-api-500-error-iukkt | git push origin claude/debug-api-500-error-iukkt | DONE | commit `59e16e1` (676c455 → 59e16e1), 18 files / 1583 insertions |
| 21:51 | debug-api-500-error-iukkt | git commit (spawn + docs) | DONE | commit `59e16e1` |
| 21:50 | debug-api-500-error-iukkt | spawn-critical lines verification (grep halogen_perms / total / output filenames) | DONE | comp3=range(8),5 5*56 / comp4=range(8),4 5*70 / comp5=range(8),3 5*56 ✓ |
| 21:48 | debug-api-500-error-iukkt | CODE_INVENTORY.md 갱신 — Pipeline v2 status table + spawn entries | DONE | comp3/5 ⏳ template only, comp4 ⏳ KISTI 진행 중 |
| 21:47 | debug-api-500-error-iukkt | DEPLOY.md 작성 (comp345_v2_DEPLOY.md) | DONE | wget 명령, halogen split table, cache_stage1b.json 알려진 gap 명시 |
| 21:46 | debug-api-500-error-iukkt | comp5_v2 spawn 4 files (Cl=3 Br=5, watchdog GPU1) | DONE | `필독/step1_halogen_li_anneal/comp5_lpscbr/` |
| 21:43 | debug-api-500-error-iukkt | comp3_v2 spawn 4 files (Cl=5 Br=3, watchdog GPU0) | DONE | `필독/step1_halogen_li_anneal/comp3_lpscbr/` |
| 21:40 | debug-api-500-error-iukkt | comp4_v2 reference 4 files + ref_comp3.cif (verbatim from KISTI paste) | DONE | `필독/step1_halogen_li_anneal/comp4_lpscbr/` |
| 21:38 | debug-api-500-error-iukkt | 사용자 답변: spawn destination = 필독/, GPU0=comp3 GPU1=comp5, 두번째사진 = 이미지 재공유 대기 | DONE | AskUserQuestion |
| 21:35 | debug-api-500-error-iukkt | session start: read CLAUDE.md + CODE_INVENTORY.md, set up TIMELOG.md | DONE | 이전 세션(`session_01Cp6qS9TkaZYTp2zwaM4nDF`) 크래시 — comp3/5 v2 spawn 미완 |

---

## 이전 세션 (크래시) 복구 메모

**`session_01Cp6qS9TkaZYTp2zwaM4nDF` (지난 세션, 정확한 시각 모름):**
- 사용자가 KISTI `/data/work/comp4_v2/1_step1to3/`에서 production code 3개 paste:
  - `comp4_v2_step1to3.py` (Stage 1a/1b/2/3 main)
  - `anneal_rank.py` (rank N halogen × 20 Li × top 5 anneal)
  - `ref_comp3.cif` (Li27P5S22Br3Cl5 rhombo 5fu, 62 atoms)
- 이전 Claude가 "spawn" 함 (자체 보고): 아래 4개 파일 + ref_comp3.cif 생성
  - `comp3_v2_step1to3.py` (Cl=5, Br=3)
  - `comp3_v2_anneal_rank.py`
  - `comp5_v2_step1to3.py` (Cl=3, Br=5)
  - `comp5_v2_anneal_rank.py`
- **결과: git에 push 안 됨**. 어느 branch에도 commit 없음 (확인: `git log --all -- 'ref_comp3.cif'` 결과 없음).
- 이전 Claude가 따로 KISTI에 ssh 해서 만든 흔적도 없음 (확인 불가).

**사용자 보충 지시 (방 터지기 직전):**
- "이거 asyma말고 두번째사진처럼 보정해달라고" — figure plot 관련 (asymptote subtract 빼고 두번째 이미지처럼) — **이미지 없음, 사용자 확인 필요**
- "앞으로 최상위 폴더에 timelog를 적어놔라" — ✅ 본 파일 생성

---

## TODO (이 세션)

1. ⏳ comp3 v2 / comp5 v2 spawn destination 결정 (KISTI만? + repo 미러?)
2. ⏳ "두번째사진" 이미지 재공유 받기 — 어느 figure script 수정인지 확인
3. ⏳ spawn 후 CODE_INVENTORY.md 갱신 (Pipeline v2 status table comp3/4/5 ⏳ → ✅)

