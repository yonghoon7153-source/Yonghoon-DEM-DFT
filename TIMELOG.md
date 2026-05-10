# TIMELOG — 세션 작업 기록 (방 터졌을 때 빠른 복구용)

> **규칙**: Claude는 모든 작업 시작/완료 시 이 파일에 한 줄 추가.
> 형식: `YYYY-MM-DD HH:MM | branch | action | status | notes`
> status: START / DONE / BLOCKED / CRASHED-RESUME-NEEDED
> 가장 최근 항목이 위로 오도록 (역순).

---

## 2026-05-10

| 시각 | branch | action | status | notes |
|------|--------|--------|--------|-------|
| 21:50 | debug-api-500-error-iukkt | commit + push spawn templates | PENDING | 다음 단계 |
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
