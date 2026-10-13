# Codex 발송 프롬프트 — REIL C4-0b1 한정 보완 (C4-0B1-N1–N3 · A1) 결과 재검토 · 2026-10-13

> 지난 회신 (C4-0b1 결과 검토 · 배열 수용 · 구현 종결 보류 · 상태 문서 §48) 의 세 항목과 승인 경계를, 사용자 승인 (§49) 범위대로 보완한 결과다 (§50).
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-0b1 의 P2 세 항목 (C4-0B1-N1–N3) 과 승인 경계 A1 을 승인 범위대로 한 번 보완했습니다. 재검토해 주세요. 브랜치
`claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다. 실행 기록 커밋은 `d02e1507` 이고, 착수 HEAD 는
`3f719cde` 입니다.

## 1. 승인과 고정본

- 승인 요청: `bms-balancing/docs/REIL_C4_0B1_FIX_APPROVAL_REQUEST_20261013.md`. 사용자 원문 "승인이야 / 권고대로 해" (§49) — §9 의 넷을 권고대로:
  범위 그대로 · 건조의 바이트 대조 전환 포함 · GREEN 에 기존 51 함께 · 건조 재실행 없음.
- 승인 **전에** 고정한 두 파일 (커밋 `c554e0ac`):
  - 대조 15: `docs/REIL_C4_0B1_FIX_CONTROLS_DRAFT_20261013.py.txt` (`7133c550…1297`) — 실행 때 `tests/test_reil_c4_0b1_fix.py` 로 바이트 그대로 복사.
  - 패치: `docs/REIL_C4_0B1_FIX_PATCH_DRAFT_20261013.diff` (`5d2b887c…387d`) — 결과 sha 기대값까지 고정.

## 2. 결과 (원문 `bms-balancing/evidence/reil_c4_0b1_fix_20261013/`)

| 단계 | 배정 | 실측 | rc | 결과 |
|---|---|---|---|---|
| 01 identity (C4-0b1 과 같은 스크립트 · 인자) | 60 s | 22.884 s | 0 | ok · problems [] |
| 02 RED (새 15 만 · 패치 전) | 600 s | 10.666 s | 1 | 10 실패 · 5 통과 — 승인 요청 §4 의 선언과 같음 (실패 종류 포함) |
| 패치 적용 | — | — | — | 고정본 `git apply` · `reil_c4_h.py` `7d49f132…` · `test_reil_c4_0b1.py` `1040e531…` = 기대 |
| 03 GREEN (기존 51 + 새 15 · `-rP`) | 600 s | 20.699 s | 0 | 66 통과 · stderr 0 B · 자동 수정 · 재시험 0 |

- 계산 합 54.249 s / 1,260 s. 끝 기록 129.1 s / 7,200 s 는 커밋 · push · 문서 작성 전 snapshot 입니다 (`04_end.json`).
- RED 실패 종류: n1_a `(3, None) ≠ (3, 2)` · n1_b partial 없음 · n1_c partial 이 task_id · unit · run_id 뿐 · n2_a `'solver_error'` · n2_b `DID NOT RAISE` ·
  n2_d `global_stop None` · n3_a `invalid:NONFINITE` · a1_a 건조가 `qmc.Sobol` 을 부름 · a1_b · a1_c `TypeError` (`regenerate` 없음). 통과 5 는
  n1_d · n2_c ×2 · n3_b · n3_c. 행동 반례 8 · 인터페이스 부재 2 입니다.
- 커밋한 29 파일: 비밀값 검사 0 · blob 29 / 29 일치. e3a · monitor · c5 · p0 · c6_profile 은 RED → 끝 sha 그대로입니다.

## 3. 항목별 대응

| 항목 | 회신의 닫힘 조건 | 변경 (`scripts/reil_c4_h.py`) | 대조 |
|---|---|---|---|
| N1 | 구조 오류 · 옵션 경고 양쪽에서 당시 확보한 행 · 계수 · 경고 · 원 오류를 partial 로 · 0 / 성공값 채움 없음 · 실제 worker→supervisor 반례 · 같은 경로 정상 대조 | `_partial(acc, info)` — 최적화 구조 오류 · 모르는 옵션 경고 · 미분류 termination · 재평가 · 라벨 · wrapper 의 모든 구조 중지 경로. 옵션 경고는 계수 · 경고를 행에 적은 뒤 중지 | n1_a (fork · NaN · NaN · MemoryError → `STARTED_INTERRUPTED` · 3 / 2 · `stop_error` MemoryError) · n1_b · n1_c · n1_d |
| N2 | 미분류 구조 중지 · 원 status / message · 부분 기록 · 성공 · 예산 양성 대조 · 미분류 전역 중지 경로 | `termination` = C5 `termination_of` (converged · budget · unclassified) · unclassified 는 재평가 · 증인 전에 `UnclassifiedTermination` 구조 중지 | n2_a · n2_b (재평가 0) · n2_c ×2 · n2_d (fork · 전역 중지) · 기존 test_07 기대값 정정 |
| N3 | 지역 재평가 예외 → REEVAL_ERROR · 정상 NaN → NONFINITE · 구조 오류 → 전체 중지 · 원 termination 보존 · 이유별 집계 | `witness(…, reeval_error)` — SOLVER_ERROR → REEVAL_ERROR → NONFINITE → INFEASIBLE_RETURN | n3_a (집계 분리 포함) · n3_b · n3_c |
| A1 | 05 범위 이탈 신고 · 분리 · 원 기록 보존 · 앞으로 건조는 읽기만 | 원장 §48 에 신고 · `dryrun` 은 PLAN.json 하나 (`execution` 최적화 · 목적 호출 · util import · Sobol 생성 0) · 봉인은 `check_h_arrays(regenerate=False)` 바이트 대조 | a1_a (Sobol · minimize · util 로드를 막아도 건조 통과) · a1_b · a1_c · 기존 test_10 기대값 정정 |

## 4. 밝힐 것

1. A1 의 바이트 대조 전환 (건조에서 Sobol 재생성을 뺌) 은 회신이 요구한 것이 아니라 제 제안이었고, 사용자가 승인했습니다 (05 답변에서 판단을 맡긴 부분).
2. 05 의 `SYNTHETIC_SAMPLE.json` 등 원 기록은 그대로입니다. 원장 §48 에 "사전 승인 없는 추가 합성 실행" 으로 신고했고, §47 의 "REEVAL_ERROR 는 C5 한정"
   은 틀린 읽기였다고 같은 절에 적었습니다.
3. 착수 직전 컨테이너가 재시작됐습니다 (t0 의 uptime 68.8 s). identity 대조가 통과해 시작했습니다 — 원인을 추정하지 않습니다.
4. 승인 요청 §7-1 에 밝힌 위험 (기존 실제 COBYQA 실행이 미분류 status 로 멈춤) 은 이번 GREEN 에서 일어나지 않았습니다. 그 실행들의 개별 termination 은
   기록하지 않았습니다.
5. GREEN 안의 합성 실행은 승인 요청 §5 의 표대로입니다 (실행별 로그는 남기지 않음). 보존 util + COBYQA 합성 표본은 0 입니다.
6. RED 명령은 `--tb=line`, GREEN 은 `-rP` 입니다. GREEN 로그의 argparse 오류 문구는 test_10_the_cli 가 기대하는 SystemExit 출력입니다.
7. 단계 실행기는 C4-0b1 의 것에서 증거 경로 · scratch 폴더 · env 두 이름만 다릅니다 (`00_step_runner.py`). RED / GREEN 은 C4-0 전체로 각 4 회입니다.
8. 회신의 조건 "ρ 는 두 단일 목적 Phase A 완료 뒤 · 공통 갱신은 등록 탐색 종료 뒤 1 회" 는 실제 연결부의 몫이라 이번에 넣지 않았습니다 (0b2 · C4-A).

## 5. 질문

- Q1. N1 · N2 · N3 을 닫을 수 있는가.
- Q2. A1 의 처리 (원장 신고 · 원 기록 보존 · 건조 읽기 전용 + 바이트 대조) 를 수용하는가.
- Q3. C4-0b1 을 종결할 수 있는가. 남는 차단이 있으면 무엇인가.
- Q4. 다음 C4-0b2 확인 요청을 회신 권고대로 (H4 합성 양성 / 음성 구현 대조 유지 · 이 자료의 H4 / ray 실제 탐색은 UNFIT 로 건너뜀 · ray 구현 유보 여부는
  범위 확인에서) 낼 때 더 고려할 것이 있는가.

## 6. 경계

자료 (xlsx · pkl · 노트북) 개봉 0 · 실제 셀 맞춤 0 · 건조 재실행 0 · 배열 재봉인 0 · full C6 check · 전체 suite · 환경 재구축 · 설치 0 · C4-0b2 ·
C4-E / A / B 0 · COMSOL 0.

---
