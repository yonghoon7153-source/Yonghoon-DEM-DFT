---
title: "Codex 회신 R2 요청 프롬프트 — 재개 설계 v3 재심사 (회신 R 조건 8 반영 확인)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, reopen, stage0, prompt]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 R2 요청 — 조건 8 반영본의 GO/NO-GO 재심사

회신 R 이 준 재심사 조건 8 을 v3 카드 + 빌더 manifest v2 로 반영했다. **여전히 계산 0 —**
반영이 충분한지, Stage 0 (기체상 microstate/method mapping) GO 인지 재심사받는다.

---

## 붙여넣을 프롬프트

```
당신은 계산재료 리뷰어다. 앞선 회신 R 에서 우리의 doped 재개 설계 v2 를 Stage 0 NO-GO
로 판정하며 재심사 조건 8 을 줬다. v3 로 반영했다. **아직 계산 0** — 반영이 충분한지
심사하고 Stage 0 GO / 조건부 GO / NO-GO 를 명시해 달라.

조건별 반영 내용:

[1. 화학종 확정] 카드에 독립 기대값을 박았다: 닫힌꼴 C_{11n}H_{14n+2-m}O_{6n}S_{2n},
N_e = 160n+2-m, 그리고 종 표 (DP3_h1_Q0 C33H43O18S6 481e doublet Na-Nb=1 · DP4_h1_Q0
641e · DP6_h1_Q0 961e · DP6_h2_Q0 960e RKS/UKS-t/UKS-BS · N1-N3 482/642/962e).
빌더가 닫힌꼴과 다르게 산출하면 SystemExit (실물 다이머 selftest: DP3_h1=481e 검증 통과).
machine ID 는 DPn_hm_Q0 형식. net_charge / multiplicity / n_alpha_minus_beta /
wavefunction_class 4필드 분리, "M=1" 표기 금지. removed-H 원자 ID 가 종 정의에 포함
(manifest removed_H_indices). counterion 은 당신 문구 그대로: "외부 이동성 counterion
미포함, m 개의 tethered SO3- 가 formal backbone oxidation +m 을 내부 보상하는 조건부
microstate" — 살아남는 결론을 그 stratum 으로 한정.

[2. conditioning 정화] conditioning = formal_oxidation_count·wavefunction_class·
multiplicity·n_alpha_minus_beta·removed_H_indices·localization_seed 만.
'backbone hole/polaron/bipolaron' 라벨은 manifest 에서 삭제 — selftest 가 그 단어의
부재를 기계 검사한다. 섹터 명칭: RKS closed-shell candidate / UKS triplet /
BS M_s=0 determinant (nominal OSS candidate).

[3. U_eff] 위치별 정의 채택: U_eff(a,b) = E_+2(a,b) + E_0 - E_+1(a) - E_+1(b).
조립 사슬은 비틀림이 달라 B≢E·C≢D 로 취급 — DP6_h1 singles hB·hC·hD·hE 4잡을 Stage 0
에 추가해 U_eff(C,D)·U_eff(B,E) 를 계산한다. (A,F) 쌍은 U_eff 없이 섹터 비교만
(singles hA·hF 는 batch-2 후보). 부수: DP6_h1↔DP6_h2 가 같은 n 의 hole-number 축.

[4. 관측량 분리] Stage 0 = carrier_localization_profile: manifest 의
atom_sets_neutral_frame (backbone/sulfonate_X/sidechain_rest — 전 원자 1회 분할을
selftest 로 검사) 위에서 집합별 charge·signed spin · sum|m_i| · centroid/participation
ratio · BLA/quinoid · UNO 지표. Löwdin·Hirshfeld 는 강건성 진단으로 강등.
Slab = carrier_retention_change: dq_M^A = q_M^A(complex) - q_M^A(isolated doped
fragment; frozen adsorbed geometry), 같은 셀·Hamiltonian·분할법, Bader/DDEC +
spin-density difference — 의미·atom-map·paired-reference 규약을 지금 고정, 구현은
Stage 0 뒤. Stage 0 결과를 slab retention 으로 부르지 않는다.

[5. vertical/BS 규약] R0_kp = 대응 N3 최적기하에서 지정 산성 H 2개 제거, 추가 이완
없음. 같은 R0_kp 에서 s/t/bs 전부 단일점(vertical 표) -> existence+stability 통과
상태만 각자 최적화(adiabatic 표, 분리) -> 필요시 교차 단일점. BS 는 raw E·<S2>·국소
signed spin·UNO/UCO 기록 + paired triplet, Yamaguchi AP 는 2-중심 식별시에만 민감도로
병기, 다중 중심이면 NA_SPIN_MODEL_NOT_IDENTIFIED (중단코드 등재). 결론 지배 최소점은
Hessian/불안정모드 재최적화로 최소성 확인 (전 conformer full freq 는 P2).

[6. 탐색 규칙] 패턴: DP3_h1 end/middle · DP4_h1 end/inner · DP6_h2 짧은(CD)/중간(BE)/
긴(AF) 3쌍 (9 symmetry class 존재 명시 — pilot 3쌍이 ensemble 대표라 주장 안 함,
결론이 위치쌍 민감하면 확장). 전 섹터 동일 conformer·seed 예산. seeded_separation
(빌더 기록) vs realized spin-centroid separation 분리. adaptive stopping: batch K=2
추가 시 최저에너지 구조·상태순서·localization class 셋 다 불변이면 정지.

[7. 방법 고정] 주: ORCA r2SCAN-3c Opt TightSCF serial maxcore6000.
교차: wB97X-D3 / def2-TZVP / defgrid3 / TightSCF · fresh-start (MORead 금지) ·
decision set = vertical 승자 + adiabatic 승자 + 0.10 eV 이내 경쟁 상태 · identity/순서
변화 시 그 상태만 hybrid 재최적화 · 갈리면 METHOD_DEPENDENT (평균 금지).
orca_version 은 회수 시 .out 배너에서 기입.

[8. conditional microstate 고정] microstate_id = (DP, formal_oxidation_count,
removed_H_indices, external_counterion_inventory, conformer_cluster,
wavefunction_spin_sector, localization_seed, realized_localization, pose, slab_basin)
— 빌더가 잡마다 발급. 보고는 microstate 별 값 + 관측 범위. 자유에너지·prior 없는
Boltzmann/"평균 SDCP" 금지. 허용 문장은 전부 "이 [stratum·DP·패턴·섹터] microstate
에서 ..." 형식. sentinel 정정: S1/S2 는 25%·33.3% sentinel 두 점 — bracket·도핑률
귀속 철회. EPR ⊕ 독립 total carrier 측정을 paired requirement 로 격상.
slab 전 별도 승인 예약: DFT 전용 판정바닥 envelope (수치수렴/basin/multistart/method/
reference-equivalence 분리, 반복=replicate 금지) + carrier boundary.

구현 증빙: 빌더 manifest v2 selftest 23건 PASS (닫힌꼴 실물검증 481e · conditioning
단어 부재 · atom_sets 완전분할 · parity 가드 · 중단코드 6종 · 음성 5건 포함).

심사 요청:
1. 조건 1-8 각각에 대해 반영 충분/불충분 판정 (불충분이면 무엇이 빠졌는지).
2. DP6_h1 을 hB·hC·hD·hE 4잡으로 잡은 것 — (A,F) 쌍의 U_eff 를 batch-2 로 미룬 것이
   허용되나, 아니면 hA·hF 까지 batch-1 필수인가?
3. R0 를 "N3 최적기하 - 2H" 로 정의했다 — DP6_h1 (홀 1개) 의 vertical 기준도 같은
   방식(N3 - 1H)으로 통일하는 것이 맞나, 아니면 h1 은 adiabatic 만으로 충분한가?
4. adaptive stopping 의 batch K=2 와 "셋 다 불변" 정지 조건이 local trap 을 수렴으로
   오판할 위험 — 최소 독립 torsion-seed 수를 지정해 달라.
5. 전체 판정: Stage 0 GO / 조건부 GO / NO-GO.

형식: 각 항목 P0/P1/P2 + 근거. 동의는 "동의" 한 줄.
```

---

## 왜 이 프롬프트인가

- 조건별 1:1 대응을 표로 보여 **반영 누락을 리뷰어가 대조하기 쉽게** 했다.
- 2·3·4번은 반영 과정에서 우리가 내린 재량 판단 셋 — 스스로 심사대에 올린다.
- 증빙은 selftest 로 기계화된 부분을 명시 — "카드에 적었다" 와 "기계가 강제한다" 를 구분.
