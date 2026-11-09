---
title: "DU 프롬프트 — 셀구축 v1 (도핑 argyrodite 셀 만들기 · 고르기 · 안정성 · 후처리) + b2o3 B·O 배치 카드 개정 1 설계 리뷰 (결과 0 건 · 계산 전)"
date: 2026-11-09
updated: 2026-11-09
tags: [review, b2o3, cell-construction, uma, dft, phonon, framework, codex, prompt, letter]
letter: DU
track: b2o3
channel: codex
kind: prompt
status: 발송 완료 · 회신 수령 2026-11-09 **NO-GO** (`codex_DU_reply_cell_construction_v1_2026_11_09.md` · P1 9 · P2 4 · 1 단계 실행 보류 · 선행 도구 고침은 진행 가능) · 기준 커밋 af6b9464
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD / B₂O₃ 계산 쪽 (1저자 = 사용자). ⛔ b2o3 전도도 (D · Ea · σ) 값은 싣지 않는다 (08-25 마감 · 인용 불가).
> B₂O₃ 원고 (paper #2) 의 1저자는 사용자가 아니다 — 원고 문장은 리뷰 대상이 아니다.
> 기준 커밋 `af6b9464` (브랜치 `claude/evac-2026-11-08`). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DU_reply_cell_construction_v1_2026_11_09.md` 로 원문 보존.

---

**[b2o3 · 셀구축 v1] 도핑 argyrodite 셀 구축 절차 + B₂O₃ B·O 배치 카드 개정 1 — 설계 리뷰 (계산 0 건)**

## 0. 무엇을 묻나

배경 (짧게):
- b2o3 (B₂O₃ 도핑 LPSCl1.6) UMA-MD 전도도 축은 2026-08-25 에 닫혔다. 골격 (S · Cl · P) 이 움직여 Li D 가 정의되지 않았고, 같은 조건의 대조 modelc · lpsocl 은 단단했다 (`db/properties/b2o3_md_closed_retrospective_2026_08_25.json`).
- 그 MD 는 전부 6 월 '챔피언' **한 배치**였다 — 원시 셀 1×1×10 (modelc × (1,1,2) · 128 원자 · 수직폭 5.72 · 5.72 · 57.2 Å). 512 원자 런은 그 2×2×1 복사였다.
- 11-09 사후 탐색 (판정 아님 · `db/properties/b2o3_eventrate_site_localization_2026_11_09.json`): 15 런의 골격 사건이 처음 구조의 9 자리에 몰렸다 — B30 의 BS₃ 에 붙은 S 셋 · O 가 둘 붙은 PS₂O₂ (P29) · 그 옆 Cl/S. 같은 셀의 B31 BS₃ 와 PS₃O (P92) 는 0 이었다.
- 6 월 탐색에서 O 꼴 (B 에 붙음 대 P 에 붙음) 은 UMA 로 원자당 1–3 meV 근접 축퇴였고, 꼴끼리 DFT 비교는 하지 않았다 (`kb/results/b2o3_champion_coordination_2026_06_29.md` L63 · L87–88).
- 사용자 (1저자) 가 B·O 자리 선호를 개선된 코드로 다시 탐색하자고 했다. 그 과정을 '셀구축' 으로 정의하고, 후처리 (띠틈 · DOS …) · 포논 · 열적 안정 확인까지 지금까지의 노하우를 담으라고 했다.

이번에 리뷰할 것 (결과 0 건 · 아무것도 안 돌았다):
1. 셀구축 v1 — `db/properties/cell_construction_protocol_v1_2026_11_09.json` · 결정 `D-2026-11-09-cell-construction-protocol-v1` (proposed)
2. 그 첫 적용 — b2o3 B·O 배치 카드 개정 1 (`db/properties/b2o3_bo_placement_estimand_2026_11_09.json` 의 `개정_1_셀구축_v1_2026_11_09` · 결정 `D-2026-11-09-b2o3-bo-placement-amend1` proposed). 원 카드 (v0 · 결정 active) 위에 얹는 개정이다.
3. 이 절차가 기대는 기존 코드 (§1).

**물음: 이 절차 · 적용 설계에 결과를 틀리게 만들 결함이 있는가 (P0 / P1 / P2) · 기존 코드에 조용히 틀린 경로가 더 있는가 · 이대로 선행 도구 고침 → 1 단계 실행으로 가도 되는가 (GO / 조건부 GO / NO-GO).**

솔직히 적는다 — v0 카드 (같은 날 비준) 에서 내가 둘을 틀렸다.
① 2 단계 온도를 표준 (MLIP-MD 600/800/1000 K) 에서 벗어난 600/650/700 K 로 이유 없이 넣었다 (사용자 지적 · 09-23 사건 빈도 카드에서 옮겼다).
② 셀 근거로 '면내 ≳ 11 Å 에서 Dcc 수렴' 을 인용했는데 08-27 150 ps 재검에서 철회된 관찰이었다 (자체 발견).
개정 1 이 둘을 고친다. 셀은 사용자가 정했다 — 처음 낸 2×2×5 (256 원자) 는 너무 커서 취소, 본 셀은 사용자가 제안한 **1×2×5** (128 원자) 다. 그래서 이번 정의에는 규칙마다 **[기존] (출처) / [제안] (내가 정한 값)** 꼬리표를 달았다 — [제안] 은 전부 의심해 달라.

## 1. 보는 범위 (기준 커밋 af6b9464)

- 절차 · 카드 · 결정: 위 두 파일 + `db/governance/decisions.json` 의 두 결정 (proposed) + v0 결정 `D-2026-11-09-b2o3-bo-placement-uma` (active)
- 근거 기록: `b2o3_md_closed_retrospective_2026_08_25.json` · `b2o3_cell_expansion_result_2026_09_10.json` · `b2o3_vs_modelc_framework_fair_2026_09_10.json` · `b2o3_uma_vs_dft_force_result_2026_09_11.json` · `b2o3_framework_event_rate_result_2026_09_26.json` · `b2o3_eventrate_site_localization_2026_11_09.json` · `lpsocl_shape_compare_70ps_2026_08_27.json` (`📬_150ps_재검`) · `b2o3_mechanism_correction_2026_09_12.json` · `kb/methodology/b2o3_doping_chemistry.md` §5.3 · §5.7 · `ndo_lpscl16_o_motif_estimand_2026_09_09.json` · `b2o3_site_screen_estimand_2026_10_14.json` · `site_uma_modelc10_readout_2026_10_16.json` (모두 `db/properties/` 아래)
- 코드 (지금 판 — 고치기 전):
  - `tools/doping/b2o3_enumerate.py` — `site_pools` · `li_vacancy_candidates` · `main` (Ewald 열거 · 욕심 Li · 할로겐 표본) · `pick_o_sites` · `build_struct` · `_selftest`
  - `tools/doping/run_anneal.py` (500 K 어닐 + FrechetCellFilter 이완)
  - `db/inputs/ndo_site_2026_10_14/run_uma_kgy.sh` (실행기 · 가드)
  - `tools/electronic/uma_phonon.py` (UMA Γ 유한 변위)
  - `tools/ionic/framework_site_census.py` · `tools/ionic/msd_diffusive_check.py --framework`

## 2. 우리가 이미 찾은 것 (고칠 목록 — 다시 짚지 않아도 된다 · 빠진 게 있으면 짚어 달라)

1. `pick_o_sites`: 가족 자리가 O 개수보다 모자라면 PS₄ 전체로 **조용히** 넘어간다 → 멈춤으로
2. `main`: 꼴을 못 만들면 (`None`) **조용히 건너뛴다** → 멈춤으로
3. 할로겐: 조합이 n_samples 보다 많으면 **무작위 표본**이고, 정본 배열을 고정하는 옵션이 없다 → `--fix_halogen`
4. 상위 목록에 대칭 등가 배치가 겹칠 수 있다 → Ewald 반올림 중복 제거
5. `li_vacancy_candidates`: spglib 예외를 **삼키고** void-finder 로 넘어간다 → 기록 + 멈춤 (허용 플래그로만)
6. 조성식 검사가 없다 → 추가
7. `framework_site_census.py`: P 중심 규칙이라 B 를 안 세고, BS₃ 의 S 를 '자유 S' 로 센다 → 도펀트 중심 반영 (2 단계 전)
8. 실행기는 kgy 경로가 기본값이다 → 기계 무관하게 (환경 변수) · '이완만' 모드 추가

## 3. 물음

**Q1 셀.** 본 셀 1×2×5 = modelc × (1,2,1) (128 원자 · 수직폭 5.72 · 11.44 · 28.61 Å · 종횡비 5 · 옛 챔피언과 같은 조성 Li58P8B2S41O3Cl16 · B 배치 45 전수). 옛 챔피언 1×1×10 은 5.72 · 5.72 · 57.21 Å (종횡비 10) 이었다. 2×2×5 (11.44 · 11.44 · 28.61 · 256 원자) 는 사용자가 비용으로 뺐다. 살아남은 형상 관찰은 '최소 폭 5.67 Å 셀은 Tr/3 확산이 34–42 % 낮다 (제약 확실)' 와 '11.4 Å 바늘형 대 17 Å 상자형 Tr/3 14.4 % 차 (1 시드)' 뿐이다 — 1×2×5 는 그 5.7 Å 제약을 한 방향에 안고 간다. 그래서 2 단계는 같은 1×2×5 셀 modelc (124 원자) 대조와만 견주고 셀 의존은 주장하지 않기로 했다. (a) 이 셀로 'B·O 꼴 순서' 와 '골격이 단단한가' 를 묻는 게 방어되나? (b) '바늘 셀이 문제였나' 를 직접 보려면 옛 1×1×10 을 같은 절차로 한 번 더 도는 대조 팔 (같은 원자 수 · 조성) 이 필요한가, 아니면 같은 셀 대조로 충분한가?

**Q2 할로겐 고정.** 6 월은 B 자리와 할로겐 (자유 자리 S/Cl) 을 같이 열거했다. 고정이 B·O 가족 비교를 기울이는가 (예: 정본 할로겐 배열이 F_free 가족에 유리하거나 불리)?

**Q3 Ewald + 욕심 Li.** 1×2×5 는 B 2 개를 10 P 자리에 놓는 45 가지를 전부 보고, 보상 Li 4 개는 형식전하 Ewald 욕심 배치로 채운다. 욕심 Li 채움이 어닐 앞단으로 충분한가 (6 월 문서는 Li 배열 잡음이 1,162 meV 라 경고했다)? '서로 다른 Ewald (1e-3 eV 반올림)' 로 대칭 중복을 지우는 게 맞나 (서로 다른 배치가 우연히 같은 반올림 값을 가질 수 있다)?

**Q4 꼴 가족.** F_B (도펀트 중심 사면체 꼭짓점) · F_P (도펀트 없는 PS₄ 꼭짓점) · F_free (자유 S 자리) 셋이고, 섞인 꼴 (일부 O 는 B · 일부는 P) 은 뺐다. 섞인 꼴을 빼는 게 P0 인가? 짝 설계 (같은 바탕 배치에 세 가족) 와 '가족 표지는 시작 배치 · 끝 꼴은 G3 로 따로 센다' 가 맞나?

**Q5 거름 → 어닐.** UMA 이완만으로 최대 135 개를 거르고, 가족마다 상위 6 바탕 배치의 합집합 (≤ 18) 에서 세 가족을 다 어닐한다 (≤ 54 · 짝 유지). 이 거름이 어닐 뒤 순위를 바꿀 배치를 잘라낼 위험은? 어닐 길이 탐침 규칙 (최저 하나를 100 ps 어닐 · 20/50/100 ps 에서 떼어 이완 · 차 0.05 eV/B₂O₃ 이하면 20 ps) 은 충분한가 — 표본이 하나라는 점, 500 K 어닐 중 골격 사건 (옛 배치는 600 K 에서 이미 사건) 이 꼴을 바꿀 위험은?

**Q6 여유.** UMA 0.20 eV/B₂O₃ (셀당 ≈ 1.6 meV/atom) · DFT 0.10 eV/B₂O₃. 근거가 약하다 (6 월 근접 축퇴 폭 · Nd O 꼴 카드의 셀 잡음 38 meV/3O). 더 나은 근거나 값이 있나?

**Q7 DFT.** ① 가족마다 UMA 최저 둘을 단일점 (PBE · B₂O₃ 캠페인 PP · 52/520 Ry · smearing gaussian 0.01 · k 3×2×1) ② 단일점 최저 둘에 k 4×2×1 탐침 (가족 차가 0.05 eV/B₂O₃ 넘게 움직이면 다시) ③ 가족 최저 셋을 고정셀 이온 이완 — 기준 셀 = 1×2×5 모양을 옛 챔피언의 DFT V₀ 2436.33 Å³ (같은 조성 · 같은 원자 수) 로 등방 스케일 · 압력 어림 규칙 (|P| ≤ 2 GPa 이고 보정이 순서 · 여유를 못 바꾸면 EOS 안 함) ④ 띠틈 · DOS 는 SCF fixed → nscf fixed k 7×4×2 (정본 +B2O3 1.9671 eV 의 7×7×1 @ 1×1×10 과 같은 k 밀도). k 격자 · 기준 셀 · 두 단계 (단일점 → 이완) 가 같은 조성 비교에 맞나? 단일점 · 이완의 smearing 과 띠틈의 fixed 가 섞이는 게 문제인가?

**Q8 고르기 · 2 단계 (골격 열적 안정).** 에너지만으로 셋을 고르고 → 300/600/800/1000 K × 시드 2 × 400 ps (128 원자) + 같은 1×2×5 셀 modelc 대조 4 온도 × 2 · 배치마다 8 런 사건 합 ≤ 2 '단단' · ≥ 12 '움직임' · 대조 합 > 2 면 비교 무효. 이 문턱 · 시드 수 · 온도가 '전도도를 잴 만큼 단단한가' 에 답하나? (옛 512 원자 b2o3 는 600–700 K 런마다 사건 23–69 · 대조 558 원자 30 런은 0 — 셀 크기가 이번과 다르다.) 관측창 문장 (1000 K · 0.8 ns · Ea_max ≈ 0.78 eV) 은 맞나?

**Q9 안정성 · 후처리.** 포논 = UMA Γ (fmax ≤ 0.01 로 다시 이완 · −30 cm⁻¹ 문턱 · 6N = 768 힘) 로 충분한가 — 1×2×5 는 5.72 Å 방향 때문에 담기는 q 가 적다 (허용 문장을 '이 셀 · Γ (UMA) 에서 허수 모드 없음' + 셀 폭으로 묶었다)? 띠틈 · DOS 모듈 (fixed-occ nscf · 판독 R1–R6 · DOS 창 −8..0 eV) 을 도핑 셀 (9 단계 이완본) 에 그대로 쓰는 데 빠진 게 있나? 꺼 둔 모듈 (hull · Bader · ELF · ICOHP · BVSE · 탄성) 판단은?

**Q10 코드.** §2 밖에, 이 절차를 조용히 틀리게 만들 경로가 지금 코드에 더 있나 (예: Ewald 커널 · Li 후보 자리 · 욕심 배치 · 셀 필터 · 이완 수렴 판정 · 포논 문턱)?

## 4. 답 꼴

GO / 조건부 GO / NO-GO · P0 / P1 / P2 (재현 단계나 근거와 함께) · Q1–Q10 답.
'새 계산이 필요한 지적' 은 따로 표시해 달라 — 이 설계 리뷰에서 생산 계산은 하지 않는다.
