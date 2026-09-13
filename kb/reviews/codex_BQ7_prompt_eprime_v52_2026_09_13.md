---
title: 회신 BQ-7 프롬프트 — 카드 v5.2: ② 를 도구 실검사와 맞췄다 (aggregation_eligible)
kind: review-prompt
date: 2026-09-13
updated: 2026-09-13
tags: [cascade, review, codex, bq7, eprime, estimand, msd]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: single-source
---

# 회신 BQ-7 — BQ-6 의 ② (P0-1 · P0-2 · P1) 를 닫았는지 묻는다 (계산 0건)

> 대상: 카드 `db/properties/cascade_rebuild_estimand_card_v5_Eprime_2026_09_13.json` (schema v5.2) · 도구 `tools/ionic/msd_diffusive_check.py` (신설 `aggregation_eligible` · `framework_alarm`)
> BQ-6 판정: ① ΔEa 명시로 해제 · ③ 절차 해제(숫자 1저자) · **② 미해제** — 도구가 실제로 검사하는 것과 카드 선언이 달랐다.
> 리뷰어의 합성 사례 두 개를 **실제 함수로 재현**했고(수치 일치), 그대로 selftest 에 박았다.

## 무엇을 했나

**① ΔEa** — meV 척도로 풀어 씀: ΔEa: (p,k) 마다 600/800/1000 K × 속도 2 = 6점 겉보기 Arrhenius 적합(부적합 따로 보고, 해당 온도 구간의 겉보기 기울기). a_k = Ea(P1_k) − Ea(P2_k) [meV] · ā = (a_A + a_B)/2 · SE_a = |a_A − a_B|/2 · CI_a = ā ± 12.706·SE_a — **meV 척도, …

**② 집계 자격** — `run_verdict` 의 CITABLE 을 승격하지 않는다. 신설 `aggregation_eligible(t, y, events_per_run)`:
```json
{
  "⛔_정정": "v5.1 의 'run_verdict 세 축' 은 **사실과 달랐다**. run_verdict 는 D_inc plateau + MSD 대용값만 본다. 부창 검사는 호출되지 않는다 (회신 BQ-6 P0-2, 우리 합성 재현 일치)",
  "집계_자격_함수": "tools/ionic/msd_diffusive_check.py **`aggregation_eligible(t, y, events_per_run)`** (2026-09-13 신설) — 실행 시 git 해시를 기록",
  "자격_=_전부_참": [
    "① `run_verdict` ≠ NO_VALUE — D_inc plateau: 창 (2,50)·(10,50)·(25,100)·(50,100) ps 상대산포 ≤ 0.10, 최소 3창",
    "② **부창 기울기 비** `sub_window_ratios`: (2–18)·(18–34)·(34–50) 각 기울기 / (2–50) 기울기 ∈ [0.80, 1.20] — 셋 다. 창을 못 맞추면 검사 불가 = 자격 없음",
    "③ **선언한 변위 사건 수** ≥ 50/런 — 호출자가 궤적에서 센 값(|r_i(t) − r_i(t_ref)| > 2.5 Å 첫 발생 → 1, t_ref 갱신). None 이면 검사 불가 = 자격 없음"
  ],
  "⛔_CITABLE_승격_금지": "run_verdict 의 CITABLE 하나를 전체 통과로 승격하지 않는다. 합성 시험: D_inc 창 끝점만 지키고 중간을 흔든 곡선은 plateau 산포 0·CITABLE 인데 부창 비가 기준 밖 → 자격 없음 (selftest 에 박음)",
  "MSD_대용값_역할": "`hops_per_ion_msd` = max(MSD)/d² 는 **MSD 규모의 운영 경보**(`msd_magnitude_alarm`)다. 실제 홉·독립 표본수·정밀도 확보의 증거로 **쓰지 않는다** — 절편만 27 Å² 올려도 1.1 → 4.1 로 바뀐다. 다른 계(LPSOCl 3×3×1) 에서 본 상관계수 f 를 이 파일럿에 승계하지 않는다",
  "정책_변경_명시": "v4 의 사건 게이트(2.5 Å 카운터 ≥50/런)를 **유지**하고, v5.1 이 도입했던 MSD 대용값 판정을 **폐기**한다. 사건 수는 '독립성이 입증된 사건 수' 가 아니라 **선언한 변위 사건 수**다 — 시간원점 중복만 피하고 통계적 독립성은 보증하지 않는다",
  "β": "**경보만** (BETA_OK 0.80–1.20 밖이면 기록). 판정 아님",
  "골격_경보_P1": "`framework_alarm` (신설, `framework_com_split` 껍질). **범위**: 원소 수 < 8 인 종은 판정 평균에서 빠진다 → **Al₂·O₃ 는 이 경보가 보지 않는다** (별도로 Al·O 5 원자의 첫↔마지막 프레임 변위를 기록만) · 첫 프레임 대비 마지막 프레임 MSD(원자수 가중) — 시간원점 평균·2–50 ps 창이 아니다 · 전역 COM 하나만 제거 · 입력 = 생산 200 ps 전 구간 unwrap 직교좌표. state ∈ unavailable·framework_static·ok·alarm; **None → unavailable = 검사 불가 → 미판정** ('경보 없음' 아님). alarm → 진단 중단·미판정, 결합 재배열 확정 안 함. 전체 비-Li 연결성·이동을 인증하지 않는다",
  "상태_어휘": "집계 = aggregation_eligible True 인 런만. run_verdict 코드는 세부에 기록"
}
```

**selftest (리뷰어 합성 사례 그대로 · 141 ok · 5종 고장 전부 빨간불 확인)**
```
  ✓ [재현 BQ-6 ①] 절편 27 Å² 만 다른 두 곡선에서 run_verdict 가 hold ↔ citable 로 갈린다 (MSD 대용값 1.1 → 4.1)
  ✓ [음성 BQ-6 P0-1] 집계 자격은 절편에 **안 갈린다** — MSD 대용값은 경보로만 남고 자격을 안 정한다
  ✓ [재현 BQ-6 ②] D_inc 창 끝점만 지키고 중간을 흔들면 plateau 산포 0 · run_verdict CITABLE
  ✓ [음성 BQ-6 P0-2] 그 곡선은 부창 기울기 비가 기준 밖이고 **집계 자격이 없다** — CITABLE 하나가 통과로 승격되지 않는다
  ✓ [양성] 직선 + 사건 60 → 자격 있음
  ✓ [음성] 사건 수 None 은 '검사 불가' 이지 통과가 아니다
  ✓ [음성] 선언 사건 49 < 50 → 자격 없음
  ✓ [음성] D_inc 가 움직이면(NO_VALUE) 사건이 충분해도 자격 없음
  ✓ [음성 BQ-6 P1] 골격 분해가 None 이면 'unavailable' — '경보 없음(ok)' 으로 읽지 않는다
```
합성 ② 실측: 부창 비 [2.804, −0.505, 3.483] · plateau · run_verdict citable · **aggregation_eligible False**.

**P1 골격 경보** — `framework_alarm`: n<8 종 제외(Al₂·O₃ 안 봄) · 첫↔마지막 프레임 MSD · 전역 COM · None → unavailable(검사 불가). 연결성 인증 아님.

**잔존 문구 4 곳** 정정 (골격 연결성 보존 가정 · H0 예외 · 1.923 % · 결정 원장 '완화 상태 다수성'). '≥ 상한'.

## 묻는 것
**Q1.** P0-1 — MSD 대용값을 경보로 강등하고 **선언한 변위 사건 수**(2.5 Å 카운터, 독립성 입증 아님)를 자격 입력으로 유지한 정책이 맞나. v4 사건 게이트 유지 + v5.1 대용값 판정 폐기를 명시했다.
**Q2.** P0-2 — 자격 = plateau ∧ 부창 비 셋 ∧ 사건 ≥50 (None = 검사 불가) 로 합쳐 정한 것이 "무엇을 합쳐 자격을 정하는지" 를 만족하나. 합성 ② 가 실제로 집계에서 막히는 것을 selftest 로 보였다.
**Q3.** P1 — 골격 경보의 범위 서술(Al₂·O₃ 미포함 · 첫↔마지막 프레임 · unavailable 처리)이 충분한가. Al·O 5 원자는 별도 변위 기록만 한다.
**Q4.** 이 판으로 ② 가 닫히고 **카드 확정**이 가능한가 (③ 숫자는 1저자 기입 후).
