# REIL C4-0b1 한정 보완 2 (C4-0B1-N1 잔여 한 건) 승인 요청 · 2026-10-14

> 근거: C4-0b1 한정 보완 결과 재검토 회신 (상태 문서 §51 · `reviews/review_reil_c4_0b1_fix_result_20261014/`). 회신 원문: "다음 한정 보완안에는
> 정상 반환 결과를 경고 중지 전 partial에 보존하는 변경과 해당 음성·무경고 양성 대조를 넣어 주세요. … 파일·시험·횟수·예산을 고정해 사용자 승인을 먼저 받으세요."
> 이 문서는 승인 요청이다. 승인 전에는 저장소의 코드 · 시험을 바꾸거나 돌리지 않는다 (§1 의 두 파일은 `docs/` 의 고정본이고 pytest 가 모으지 않는다).

## 1. 먼저 고정한 것 (승인 전 · 실행 0)

| 대상 | 파일 | sha256 |
|---|---|---|
| 대조 (시험 5) | `docs/REIL_C4_0B1_FIX2_CONTROLS_DRAFT_20261014.py.txt` | `b861f16b7fe651b5c68ad57ed77d9079f918bf4ec59d2028cc5b82101f847602` |
| 변경부 (패치) | `docs/REIL_C4_0B1_FIX2_PATCH_DRAFT_20261014.diff` | `dd4b1be3203cf429ac8518a89374a4f6288bdcc42eb1d75390ddc90ffc3ef2d7` |
| 패치 전 (지금) | `scripts/reil_c4_h.py` | `7d49f132…3c0d` (한정 보완 1 의 결과 · `d02e1507`) |
| 패치 뒤 기대 | `scripts/reil_c4_h.py` | `f69a4ad19a065c6a822c6de452174b39909d508fade468d44e524433b01ababb` |

확인은 정적인 것만 했다: scratch 사본에 적용한 결과의 parse · 이름 검사 (symtable) · 모듈 속성 대조 · `git apply --check` 통과 · 적용 결과 = 기대 sha.

## 2. 생산 변경 — `scripts/reil_c4_h.py` 의 `_run_phase_a` 한 곳

- 최적화가 끝난 뒤 (계수 · 경고를 행에 적은 직후) **모르는 옵션 경고를 보기 전에** solver 결과를 행에 적는다:
  - 정상 반환이면 반환점 `x` · `fun` · `status` · `message` · `nfev` · `nit` · `termination` 을 적는다 → 경고 중지의 partial 에 그대로 실린다.
  - 반환이 없으면 (최적화 중 지역 예외) **원 지역 오류 (`error`) 만** 적는다. 반환 필드 · termination 은 채우지 않는다.
- 그 뒤의 흐름은 그대로다: 모르는 옵션 경고 → OptimizeWarning 구조 중지 (재평가 · 증인 · 완료로 가지 않음) → 반환 없음이면 `solver_error` 행 (최종 행의 내용은
  지금과 같다) → 미분류면 구조 중지 → 재평가 …
- **바꾸지 않는 것:** 다른 함수 · 기존 시험 파일 둘 (`test_reil_c4_0b1.py` · `test_reil_c4_0b1_fix.py`) · 배열 · 기존 증거.

## 3. 대조 5 — 지금 코드 (패치 전) 에서의 RED 예상

| 시험 | 경로 | 종류 | RED 예상 |
|---|---|---|---|
| r1_a 경고 + 알려진 정상 반환 (가짜 minimize) → OptimizeWarning 중지 · partial 에 반환 필드 7 개 · 계수 · 경고 · 중지 오류 · 재평가 0 | 경고 · 반환 있음 | 음성 | 실패 — partial 의 반환 필드가 모두 없음 |
| r1_b 같은 경고 + 반환을 실제 fork 작업자 1 로 → 전역 중지 · 작업 중단 · 부모의 `structural_partial` 에 x · status · termination · 평가 수 | worker → supervisor | 음성 | 실패 — `structural_partial` 에 반환점 · status 없음 |
| r1_c 경고 뒤 util 지역 오류로 반환 없음 → OptimizeWarning 중지 · partial 에 원 지역 오류 (ValueError · util) · 반환 필드 · termination 없음 | 경고 · 반환 없음 | 음성 | 실패 — partial 에 원 지역 오류 없음 |
| r1_d 같은 알려진 반환 · 경고 없음 → 완료 · 반환 필드 그대로 · 재평가 1 회 · 유효 증인 | 무경고 | 양성 | 통과 |
| r1_e 실제 minimize (COBYQA) 에 모르는 옵션 → scipy 경고 · 실제 반환 → partial 에 반환점 (유한 4 값) · status · message · termination · nfev · 재평가 0 | 실제 scipy 경고 경로 | 음성 | 실패 — partial 에 반환점 없음 |

- 기대: **4 실패 · 1 통과**. 실패는 모두 행동 반례다 (인터페이스 부재 0).
- r1_e 는 COBYQA 의 실제 status 에 기대지 않는다 — 경고 중지가 미분류 판정보다 먼저이므로 termination 이 셋 중 무엇이든 단언이 선다.

## 4. 합성 사례 · 횟수

| 실행 | RED (새 5 만) | GREEN (기존 51 + 보완 1 의 15 + 새 5 = 71) |
|---|---|---|
| 가짜 minimize (최적화기 없음 · 목적 0–2 호출) | 4 — r1_a · r1_b (fork) · r1_c · r1_d | 12 — 위 4 + 보완 1 의 8 |
| 실제 COBYQA · 가짜 목적 (건조 옵션 maxfev 50) | 1 — r1_e | 9 — 위 1 + 보완 1 의 3 (n1_a · n1_b · n1_d) + 기존 test_08 의 5 |
| 보존 util 사본 (합성 곡선 · 최적화 없음) | 0 | 기존 test_06 의 평가 몇 회 (바뀌지 않음) |
| 보존 util 사본 + COBYQA · REIL 자료 | 0 | 0 |

## 5. 실행 순서와 배정 (승인하면)

1. 착수 전에 `.gitattributes` 에 `evidence/reil_c4_0b1_fix2_20261014/** -text` 를 넣고 커밋한다 (승인 기록 §52 와 함께).
2. 착수 기록 (t0 · HEAD · uptime) — 증거 폴더가 이미 있으면 중지한다.
3. **identity 1 회 (60 s)** — 같은 대조 스크립트 · 같은 인자. 맞지 않으면 시작하지 않는다.
4. 대조 고정본을 `tests/test_reil_c4_0b1_fix2.py` 로 복사하고 sha 를 대조한다 (`b861f16b…`).
5. **RED 1 회 (600 s)** — 새 시험 파일만, 지금 코드로. §3 의 예상 (4 실패 · 1 통과 · 실패 종류) 과 다르거나 무관한 하네스 실패면 원문을 보존하고 멈춘다.
6. 패치를 적용한다 (`git apply` · 고정본 sha `dd4b1be3…`). 결과 sha 가 §1 의 기대값과 다르면 멈춘다.
7. **GREEN 1 회 (600 s)** — 기존 51 + 보완 1 의 15 + 새 5 = **71**, `-rP`. 예상 밖 실패는 원문을 보존하고 멈춘다 (자동 수정 · 재시험 없음).
8. 끝 기록 · 비밀값 검사 · 커밋 · push · 결과 기록 (§53) · 재검토 발송문을 쓰고 멈춘다.

- **배정:** identity 60 + RED 600 + GREEN 600 = 계산 1,260 s · 전체 작업 2 h · 자동 재시험 0.
- **단계 실행기:** 보완 1 의 것에서 증거 경로 · scratch · env 두 이름 (`REIL_C4_0B1_FIX2_EVIDENCE` · `REIL_C4_0B1_FIX2_STEP`) 만 바꾼다.

## 6. 밝힐 것

1. r1_c 의 "반환 없음 → 원 지역 오류만" 은 회신의 "반환이 없으면 x/status/termination 등을 성공값이나 0으로 채우지 않는다" 를 엄격하게 읽은 것이다 —
   반환 없는 경로의 partial 에는 termination (`solver_error`) 도 넣지 않는다. 경고가 없을 때의 최종 행 (`solver_error` · `invalid:SOLVER_ERROR`) 은 지금과 같다.
2. 원 지역 오류의 키 이름은 완료 행과 같은 `error` 다 (중지 오류는 따로 `stop_error`).
3. RED / GREEN 은 C4-0 전체로 각 5 회가 된다 (0a · 0a 보완 · 0b1 · 0b1 보완 · 0b1 보완 2).

## 7. 하지 않는 것

기존 기록 · 증거 (05 의 SYNTHETIC_SAMPLE.json 포함) · 배열 · 환경 봉인을 덮어쓰거나 지우지 않는다. 건조 재실행 · 배열 재봉인 · full C6 check · 전체 suite ·
환경 재구축 · 설치 · C4-0b2 · C4-E / A / B · 자료 개봉 · 맞춤 · COMSOL 은 범위 밖이다.

## 8. 정하실 것

1. **위 범위 그대로 승인할지.**
2. GREEN 에 기존 66 (51 + 15) 을 같이 돌릴지 — **권장: 같이 돈다.** 바뀌는 `_run_phase_a` 를 기존 시험 대부분이 지난다.
