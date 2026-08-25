---
title: Codex 리뷰 과제 — Double Bacon-Watts knee-onset/knee-point (ADR 0021)
created: 2026-08-25
updated: 2026-08-25
type: guide
tags: [review, audit, crosscheck, knee, dbw]
sources: [docs/adr/0021-double-bacon-watts-onset-and-point.md, docs/adr/0005-multi-criterion-knee.md]
confidence: high
explored: false
verificationStatus: unverified
---

# Codex 리뷰 — DBW knee-onset/knee-point

새 knee 기준이 들어왔고 **primary 가 바뀌었다**: Double Bacon-Watts
(Fermín-Cueto 2020) 가 검출되면 그것이 대표값이다. 모든 셀의 리포트 카드
숫자가 바뀔 수 있는 변경이라, 조용히 틀리면 가장 넓게 틀린다.

Claude 쪽 자체 적대 리뷰는 끝났다 (14개 공격 지점, 1건 수정: bootstrap
n_boot<=0 가드). 이쪽 결과를 먼저 읽지 말 것 — 독립성이 교차검증의 값어치다.

## 1. 먼저 동기화

```text
git fetch origin
git merge --no-ff origin/claude/battery-charge-discharge-webapp-dq4ja3
```

`feat: DBW — knee-onset 과 knee-point 를 한 적합으로 (ADR 0021)` (6adb04e3) 와
그 뒤 `feat: DBW 를 API·화면에` (cb44dcd1 언저리) 가 보이면 준비된 것이다.

## 2. 리뷰 과제 (붙여넣기)

```text
DBW knee 기준(커밋 6adb04e3, cb44dcd1 및 후속)을 적대적으로 리뷰해줘. 결과는
docs/reviews/2026-08-26-codex-dbw-result.md 로 같은 브랜치에 커밋해줘.

먼저 읽을 것 (코드보다 먼저):
- docs/adr/0021-double-bacon-watts-onset-and-point.md
- docs/adr/0005-multi-criterion-knee.md (기존 4기준과 게이트 철학)
- CLAUDE.md §0.4 (모르면 None), §3 (기준 사이클 3, formation 제외)

대상 파일:
- packages/wrdkit/src/wrdkit/knee.py — _dbw_model/_dbw_jacobian/_bw_model/
  _bw_jacobian/_transition_seeds/_dbw_fit/_bw_fit/_judge_bacon_watts/
  _dbw_knee/dbw_confidence_interval, KneeResult.onset_cycle, ranked 순서
- packages/wrdkit/tests/test_knee.py — dbw 섹션 + null sweep + 블록 격자 17/30
- apps/api/app/main.py knee_methods, apps/web/src/components/ReportCard.tsx,
  apps/web/src/pages/SampleDetail.tsx kneeMarkers, apps/web/src/lib/i18n.ts

검증 실행:
    make check
    .venv/bin/python -m pytest packages/wrdkit/tests/test_knee.py -q

공격 지점 (우선순위 순):

A. 수식 대조.  DBW 모델이 Fermín-Cueto 2020 정의와 같은가:
   Q(x)=α0+α1(x−x1)+α2(x−x1)tanh((x−x1)/γ1)+α3(x−x2)tanh((x−x2)/γ2).
   해석적 야코비안(_dbw_jacobian/_bw_jacobian)을 유한차분과 독립적으로 대조.
   점근 기울기 (α1−α2−α3)→(α1+α2+α3) 와 중간 기울기의 유도가 맞는지.
   (x1,γ1,α2)↔(x2,γ2,α3) 교환 대칭 주장(라벨 재정렬의 근거)이 실제로 항등인지
   — α1(x−x1) 항의 −α1·x1 상수 처리까지.

B. 변수 분리 씨앗.  격자마다 curve_fit 대신 (x1,x2,γ) 고정 lstsq 로 SSE 를
   재는 것이 "grid search 로 지역최소 회피" 를 정말 대체하는가.  상위 3 씨앗
   정련이 놓치는 지역최소를 만들 수 있는 곡선을 구성해봐라 (γ 축이 1.0/5.0
   둘뿐인 것, DBW_FIT_TOL=1e-6, maxfev=20000 의 상호작용 포함).
   seed 는 없다 — 같은 데이터에 항상 같은 답인지.

C. 승격과 게이트.  단일 BW 로 먼저 적합하고 두 번째 전환이
   _f_gain(bw_sse, dbw_sse, n, 2, parameters=8) >= 100 일 때만 이중 —
   이 자유도 계산이 맞는지, MIN_FIT_GAIN_F=100 재사용이 여기서 보수적인지
   느슨한지.  검증된 실패 모양 세 가지가 정말 막히는지 재현:
   (1) 순수 힌지에서 x2 표류 → onset=None 강등,
   (2) a3>=0 (급감 후 완화) → 사퇴,
   (3) x2−x1 > 2(γ1+γ2) (두 사건) → 사퇴.
   그리고 이 게이트들이 **정상 검출을 죽이는** 곡선이 있는지 — 특히
   경계 근처: x2−x1 ≈ 2(γ1+γ2), γ 가 상한 20 에 붙는 완만한 knee.

D. null 과 블록.  직선 200개 sweep 에서 dbw 검출 0·유예 0 이 유지되는지
   직접 돌려라.  블록+knee 격자 17/30 — 15/30(종전)에서 나빠진 2건이
   문서 말대로 "excursion 미검출 배치의 블록 복귀 에지" 인지, 아니면 더
   넓은 퇴행인지.  당신이 다른 블록 배치를 만들어 17 이 하한인지 시험해라.

E. primary 교체의 파급.  dbw 가 primary 가 되면서 기존 화면·API 소비자가
   깨지는 곳: knee_trend_index(대시보드), criteria_spread 문구, 비교 화면,
   기준 전환 UI(kneeMethod 'dbw' 기본), i18n 미번역 이유 문자열.
   onset_cycle 이 None 인 detected(단일 전환)와 onset 있는 detected 를
   화면·클립보드가 다르게 말하는지.

F. 성능.  대시보드는 셀마다 detect_knee 를 다시 돈다.  워밍업 후 곡선당
   추가 비용을 실측하고 (문서 주장: +50~90 ms), n=500 사이클·잡음 큰
   기록에서 폭주하는지.  test_dbw_stays_fast_enough 의 1.5 s 상한이
   당신 환경에서도 여유 있는지.

G. bootstrap CI.  dbw_confidence_interval — 사례 재표집이 Fermín-Cueto 의
   절차와 같은지, 수렴 실패 절반 규칙과 n_boot<=0 가드, 라벨 교차(x1>x2)
   재표집의 sorted() 처리.  API 경로에서 안 부르는 결정(ADR 0021)이
   문서와 코드에서 일치하는지.

이미 알고 있는 것 (다시 보고하지 않아도 된다):
- 블록+knee 격자는 17/30 으로 알려진 한계다 (테스트가 고정).
- 실측 knee 데이터로는 아직 검증 전 — 실측 파일의 fade 곡선이 오면 추가.
- curvature 는 여전히 panel 전용이다.

결과 문서 형식: 표 (# | 심각도 | 파일:줄 | 증상 | 재현 | 제안), 재현 못 한
의심은 별도 표, 마지막에 "리뷰가 못 본 곳" 한 단락.
```

## 3. 끝나면

결과가 커밋되면 Claude 쪽 자체 리뷰(공격 14지점)와 교차해서 겹치는 것부터
닫는다. 대응 현황은 이 문서 옆에 회답으로 남긴다.
