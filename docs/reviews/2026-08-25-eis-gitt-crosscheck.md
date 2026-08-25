---
title: EIS·DRT·GITT 교차검증 — Claude 5구역 × Codex 33건 대응 현황
created: 2026-08-25
updated: 2026-08-25
type: review
tags: [review, audit, crosscheck, eis, gitt]
sources: [docs/reviews/2026-08-25-codex-eis-gitt-result.md, docs/reviews/codex-review-eis-gitt.md]
confidence: high
explored: false
verificationStatus: verified
---

# EIS·DRT·GITT 교차검증 대응 현황

두 리뷰는 서로를 읽지 않고 같은 범위(`b6df17bb..7b0531d1`)를 봤다.
Claude 쪽은 fable 에이전트 5구역(리더/피팅/GITT/API/화면)으로 ~27건을 확정했고,
Codex 는 33건을 확정했다. **Codex 의 범위는 7b0531d1 에 고정**되어 있어서,
그 뒤에 이미 커밋된 Claude 쪽 수정 7건(fe338f35..4c12aab0)과 겹치는 항목이 있다 —
겹친 것은 Codex 의 재현 절차를 현재 HEAD 에서 다시 돌려 닫힘을 검증했다.

## 겹친 것 (독립적으로 같은 결함을 봤다 — 교차검증 성공)

| Codex # | Claude | 상태 | 검증 |
| ---: | :---: | --- | --- |
| 1 | F2 | **수정 완료** `bb58fd15` | Codex 재현 재실행: `CPE9_Q=999.999997`(상한)·`CPE9_n=0.300`(하한) 둘 다 `stderr=None`, `determined=False` |
| 2 | F1 | **수정 완료** `b72f18d2` | Codex 재현 재실행: 저장 χ²=반환 곡선 χ²(1.27e-5 로 일치, 1528배 발산 소멸), 정렬은 f_c 큰 분기 먼저 유지 |
| 3 | G5 | **수정 완료** `3bfe47b1` | Codex 재현 재실행: `L0-R0-p..p` 에서 bulk 5e-4 / GB 2.5e-4 / total 1.667e-4 S/cm, 60 Ω — Codex 기대값과 일치 |
| 8 | S1 | **수정 완료** `2db59787` | POST 본문 reference_cycle → `model_fields_set` 로 source=user; formationless 스케줄 뒤에도 생존 (회귀 테스트 포함) |
| 14 | G1 | **수정 완료** `fe338f35` | 리셋 차분 → 증분 재구성; 다사이클 합성 테스트 2건 |
| 15 | G2 | **수정 완료** `d4df7a31` | ΔE_t = slope·√τ (IR 제외 구간 적합 기울기); 닫힌식 기대값 테스트 |
| 16 | G3(+G4) | **수정 완료** `746d1722` | 방향 전환·짧은 휴지에서 시리즈 상태 리셋 + 이유 있는 D=None 점 |
| 6 | W1 | 대기 (높음) | 클라이언트 fitCurve 가 L/Ws/Wo/중첩을 못 그림 — 같은 발견 |
| 13 | W2 | 대기 (높음) | `.mps` 짝짓기의 `_C\d+` 정규화 — 같은 발견 |
| 19 | W4 | 대기 (높음) | DrtPanel 이전 차수 데이터/추천 index 잔존 — 같은 발견 |
| 22 | A3 | 대기 (중간) | dedup 시 새 메타데이터 무시 — 같은 발견 (Codex 는 409/구분 응답까지 제안) |
| 23 | A1+A2 | 대기 (중간) | 캐시/원본 소실 후 재업로드가 복구 못 함 — 같은 발견 |
| 24 | A5 | 대기 (중간) | clear 가 계측기 유래 필드까지 지움 — 같은 발견 |
| 30 | W5·W6 인접 | 대기 (중간) | Codex 는 12개 제한 초과·stale 선택까지 확장 — 합쳐 처리 |
| 32 | W6 인접 | 대기 (낮음) | D=0 의 truthy 필터 — 같은 발견 |

## Codex 만 본 것 (Claude 리뷰의 사각)

| Codex # | 심각도 | 요지 | 상태 |
| ---: | :---: | --- | --- |
| 4 | 높음 | DRT TRF 해가 KKT 최적점에서 멀다 — 깨끗한 1-RC 에서 Rp 절반·가짜 봉우리 8개 | 대기 |
| 5 | 높음 | DRT kernel 의 quadrature(끝점 가중)와 total 보고값(사다리꼴)이 다른 적분 | 대기 |
| 7 | 높음 | origin.ts 가 미결정 파라미터를 확정 숫자로 내보냄 (기존 테스트가 오답을 고정) | 대기 |
| 9 | 높음 | 셀 삭제가 SpectrumRecord 를 detach 안 함 → SQLite id 재사용 시 남의 측정으로 재귀속 | 대기 |
| 10 | 높음 | `.mpr` 모듈 길이 1바이트 손상에도 anchor 이동으로 쓰레기 수용 (F4 인접, Codex 재현이 구체적) | 대기 |
| 11 | 높음 | `.mpt` 열 수 불일치를 행 삭제/열 이동으로 처리 (F6 인접, Codex 는 거절을 제안) | 대기 |
| 12 | 높음 | points.npz 캐시가 원본 SHA 와 미결합 — 바꿔치기 미검출 | 대기 |
| 17 | 높음 | diffusion 점이 rest_s·drift 증거를 버림 (ADR 0020 위반) | 대기 |
| 18 | 높음 | diffusion 의 방전 용량축이 pOCV 와 반대 부호 | 대기 |
| 20 | 중간 | 대역 밖 τ 끝점 pile-up 은 find_peaks 미검출로 대역 검사 우회 (`fe92478d` 커버 여부 재확인 필요) | 확인 중 |
| 21 | 중간 | `.mps` 원문 미보존 — 파서 모르는 설정 영구 손실 (§0.2 정신) | 대기 |
| 25 | 중간 | 휴지 없는/짧은 펄스가 행째 사라짐 (`746d1722` 가 짧은 휴지는 커버 — 마지막 rest 없음 케이스 확인) | 확인 중 |
| 26 | 중간 | GITT 분할이 CELL STATUS 를 안 쓰고 p90 문턱이 offset 전류에 속음 | 대기 |
| 27 | 중간 | Bode 가 선형 x·단일 y — 8-decade 판독 불가 | 대기 |
| 28 | 중간 | 전도도 안내가 시키는 면적 입력란이 화면에 없음 | 대기 |
| 29 | 중간 | liquid/solid kind 를 화면에서 교정 불가 + dedup 이 재업로드를 삼킴 | 대기 |
| 31 | 중간 | CellName 미수정 blur 가 남의 동시 수정을 옛 값으로 덮음 | 대기 |
| 33 | 낮음 | massFromName 이 쉼표 소수·과학표기의 꼬리만 읽음 | 대기 |

## Claude 만 본 것 (Codex 의 사각 — 이미 수정됐거나 대기)

| Claude | 요지 | 상태 |
| :---: | --- | --- |
| S2 | 기준 사이클 칸 스치기 blur 가 자동 앵커를 영구 고정 | **수정 완료** `4c12aab0` |
| S3 | clear["reference_cycle"] 가 NOT NULL·SampleOut(int) 를 깨 500 | **수정 완료** `2db59787` |
| S4 | formation 판정이 루프 **뒤** 종료 방전에 속음 | **수정 완료** `a06f7165` |
| S5 | 스케줄 없는 run 이 무표 처리돼 "no" 가 과확신 | **수정 완료** `a06f7165` |
| S6 | ReportOut 에 reference_cycle_reason 누락 — 카드가 항상 "default" | **수정 완료** `2db59787` |
| A4 | ids 파라미터 int 변환 실패 시 500 (422 여야) | 대기 |
| A6 | fit-batch 가 한 건 예외로 전체 중단 | 대기 |
| W3 | equalAspect 가 한 축 스케일만 봄 (Nyquist 대각 왜곡) | 대기 |
| F5 | 초기 추정 클램프 폴백 | 대기 |

## 서로 반박된 것

없다. Codex 의 "정상으로 확인한 것" 은 Claude 확정과 모순되지 않고, 두 의심
항목은 Claude 쪽에서 이미 결정·구현된 것과 만난다:

- **전고체 3번째 아크 합산** — G5 로 결정 완료: 전해질은 처음 두 아크만,
  3번째는 빼고 `excluded` 로 표기 (`3bfe47b1`). Codex 가 요구한 "결정" 이
  바로 이것이다.
- **GITT 첫 펄스 용량 0 기준** — G3/G4 수정에서 "시리즈마다 0부터(상대)" 로
  결정. ADR 0020 에 계약 명문화가 남아 있다 (대기).

## 처리 순서

숫자가 틀리는 것부터: #4+#5 (DRT) → #10+#11 (리더 거절) → #12·#9 (무결성)
→ #13·#22·#23 (dedup/짝짓기) → #6·#7·#19 (화면·클립보드의 거짓) → #17·#18
(GITT 증거·부호) → #24·#25·#26 → #20 재확인 → 나머지 중간·낮음과 Claude 단독
대기(A4·A6·W3·F5·W5·W6). 항목마다 회귀 테스트 선행, `docs/log.md` 한 줄,
이 표의 상태 갱신.
