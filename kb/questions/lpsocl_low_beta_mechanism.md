---
title: 저β 런의 정체 — 케이지 절편인가, 진짜 sub-diffusion인가, 느린 전이인가
date: 2026-08-11
updated: 2026-08-11
tags: [mlip-md, msd, beta-gate, lpsocl, arrhenius, mto]
status: active
confidence: medium
verificationStatus: disputed
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-mixed
feedsInto: 6점 아레니우스 적합 집합 → 논문 Ea 표 (ΔEa +90 meV 주장의 생사)
---

## 질문

arrhenius_6pt 21런 중 β<0.8 로 탈락한 8런(창 2–50 ps)은 무엇인가 —
**(A) 케이지 절편** (MSD = c + 6Dt, D 인용 가능) · **(B) 진짜 sub-diffusion** (D 인용 금지) ·
**(C) 느린 전이** (D 존재, 창만 이르다 — 처방은 제거가 아니라 창 이동) ·
**(D) 추정량 잡음** (2026-08-11 추가 — 단일 시간원점 β 의 산포. 처방은 MTO 재측정)?

## 왜 중요한가

lpsocl 이 9런 중 5런 탈락이라 **6점 아레니우스가 이 답에 걸려 있다.** (A)면 8점 복구,
(B)면 제거가 정당, (C)면 창 통일로 해소 — 셋의 처방이 전부 다르고, ΔEa(+90 meV) 주장이
창 효과(242 meV)보다 작아서 잘못 고르면 논문 헤드라인이 통째로 틀어진다.

## 가설

계·온도점마다 다르다 — 단일 기구가 아니다 (modelc/700 은 A 쪽, b2o3/700 은 이상치).

## Evidence For

- **(A) 지지**: 귀무검정에 케이지 항을 넣으면 C≈2 Å² 만으로 P(β<0.8)=27.7% —
  실측 절편 1.7–4.0 Å² 로 8/21 탈락이 재현된다 (tools/ionic/beta_null_test.py).
  캠페인 D 는 전부 자유 절편 기울기라 절편에 오염되지 않음(코드 7곳 확인).
- **(A) modelc/700**: 잔차 검정(관측 β vs (c,m) 직선 함의 β) 전 창 |Δβ|≤0.025,
  cage joint p=0.935 — 조건부 생존 (db/properties/msd_trend_verdict_arrhenius6pt.json).
- **(B) 후보 b2o3/700**: β 가 여섯 창 전부 0.83–0.86 평평 — 멱함수 서명.
- **(D) 지지 (중간, n=1)**: MTO 파일럿 700 K 첫 두 계 — modelc β 0.681→**0.901**
  (게이트 통과로 뒤집힘), lpsocl 0.863→0.829. MTO 는 Jensen 때문에 기댓값이 **약간
  내려가는 게 정상**인데 modelc 만 +0.220 으로 반대 방향 대폭 이동 —
  STO 값이 물리가 아니라 산포였다는 서명. (kgy `~/work/runs/mto_pilot/`)

## Evidence Against

- (A) 일괄 적용 반박: lpsocl/700·900 은 늦은 창 적합이 붕괴(c 음수·|c|>40 Å²)해 **판별 불가**.
- (B) b2o3/700 반박: 'β 평평(range 0.030)' 은 cage 0.10%·멱함수 0.55% — **두 모형 다
  재현 못 하는 이상치** (우도비 5.5:1 뿐, 제거 기각).
- 추세 자동판정 자체가 기각됨: 중첩창 n_eff≈3.2, 오분류 8~13%, 'SUBDIFF' 는 (C) 대비
  동전(47~50%) — 도구는 진단 제안으로 격하 (tools/ionic/msd_diffusive_check.py).
- (C) 를 초판이 아예 몰랐다 — 세 번째 모형의 존재 자체가 재검토 산물.
- **(D) 반박 유보**: modelc 의 +0.220 은 **계마다 1시드**라 잡음 감소인지 단일시드
  우연인지 구분 불가 — 오늘 철회한 단일시드 1.33× 와 같은 함정이다. lpsocl 은
  −0.034 로 예상대로 움직여 (D) 를 지지하지 않는다. 2/3 계가 아직 없다.

## 결정 실험

**MTO 파일럿** (kgy, 3계 × 700 K × 1시드, --save_traj 포함 — watch ⑤).
① β(MTO) 로 판별 불가 3점 재판정 ② traj 로 홉 통계·van Hove (기구 직접 분해)
③ 그래도 애매하면 **세 계 같은 온도 집합** 유지 + 창 통일 — 점 제거는 최후수단.

⚠ (D) 가 추가되면서 파일럿만으로는 부족해졌다. **1시드 × 3계로는 잡음 가설을 검정할 수
없다** — 산포를 재려면 같은 계·같은 온도에 시드가 여럿이어야 한다. 이어지는 결정 실험:
**lpsocl 600 K** (지금 kgy 에서 s2 진행 중). 구 4시드 STO 앙상블이 β=0.61 로 탈락한
바로 그 점이라, MTO 재측정이 0.8 을 넘으면 (D) 가 실질 근거를 얻고 여전히 0.6 대면
(A)/(B)/(C) 판별로 돌아간다 (러너: tools/ionic/run_arrhenius_6pt.sh 의 LPSOCL_EXTRA).

## Status Log

- 2026-08-11 (저녁): MTO 파일럿 2/3 계 완료 — modelc 0.681→**0.901**(게이트 뒤집힘),
  lpsocl 0.863→0.829. **네 번째 갈래 (D) 추정량 잡음**을 질문에 추가. b2o3/700 대기,
  lpsocl/600(MTO) 진행 중 — 후자가 (D) 의 실검정. traj 2건 확보(각 ~14 MB)로 홉 통계 가능.
- 2026-08-11: 8/21 탈락 발견 → 귀무검정 v1("진짜 sub-diffusion") → 재검토로 기각
  (귀무에 케이지 절편 부재) → 추세 판정 v1(복구/제거 제안) → 재검토로 2/3 기각 →
  전 조치 보류, MTO 파일럿 착수. 원장: kb/open_items.md ·
  질문지: kb/reviews/codex_stats_question_2026_08_11.md
