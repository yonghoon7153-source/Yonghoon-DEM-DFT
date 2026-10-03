# pybamm 상한 · 고정 — Codex 사전 검토 회신 접수 (2026-10-03 · 게이트 차수 밖 · RUN_SCOPE 0 · 결정은 사용자)

요청문 `PYBAMM_PIN_PREREVIEW_20261003.md` (커밋 `00ed85b44`) 에 대한 회신이다. 요청문은 원문 그대로 두고 (요청문은 새 파일로만
덧붙인다), 회신의 판정 · 우리 사실 정정 · 우리 의견을 이 파일에 적는다. **이 회신은 구현 · 실행 · requirements 변경 · G87-N1 범위
확장 승인이 아니다** (검토자 `DECISION.json` `approved` 네 칸 전부 false).

## §0 묶음 · 무결성 (우리 실측)

| 항목 | 값 |
|---|---|
| 보존 위치 | `bms-balancing/reviews/prereview_pybamm_reil_20261003/` (REIL 프로토콜 검토와 한 묶음 · ZIP + 풀어 둔 payload · `-text` 규칙을 같은 커밋에서 먼저) |
| ZIP | `PYBAMM_REIL_PREREVIEW_20261003.zip` 134,489 B · sha256 `c0f32a8de5b1b87e7a1fe552c8b477b3439f3d3fc13ff6ad60bc34f4d2961262` · `testzip` 이상 없음 |
| manifest | `PACKAGE_MANIFEST.json` payload 23 · 크기 · sha256 23/23 일치 · 빠짐 · 남는 파일 0 · CRLF 파일 0 |
| 우리 원문 사본 | `reference/` 의 우리 파일 6 (요청문 둘 · requirements · `src/io.py` · `src/grid.py` · `src/runner.py`) = 커밋 `00ed85b44` 의 바이트와 sha256 동일 |
| 검토 기준 커밋 | `00ed85b4402169bae788b7269ffe69d76a0c40aa` (검토자 `DECISION.json` `review_ref`) |
| 검토자 행위 | 코드 import · 실행 0 · 설치 0 · 시험 0 · PyBaMM solve 0 · COMSOL 0 · 생산 파일 편집 0 · 외부 발송 0 (`DECISION.json` `actions`) |

## §1 판정 (사본)

`PINNING_RECOMMENDED_WITH_SEPARATE_PROFILES` — 고정은 필요하다. 다만 A–E 하나를 모든 용도에 쓰지 않는다.

| 용도 | 권고 프로필 | 뜻 |
|---|---|---|
| 지금 검증 (validator · 회귀 · smoke) | **C** 정확 고정 (`pybamm 26.8.0.0` · `pybammsolvers 0.9.1` · `casadi 3.7.2`) | 현재 검증 환경의 동결 — **정본 생산 환경과 같다고 선언하지 않는다** |
| 정본 재생성 | **B** 에 해당하는 역사적 프로필 (`26.7.1.0` · `0.9.0` · `3.7.2`) | 당시 환경 증거 (producer manifest · 환경 기록) 로 복원 · 확인하거나, 명시적으로 **새 세대 생산**으로 분류 |
| 새 truth 생산 | **D** guard — 승인된 불변 프로필에 결속 | expected identity 는 실행 환경을 베끼지 않는다. 사전에 봉인한 profile 파일의 해시를 prospective 계획이 참조 |
| A (상한만) · E (문서 경고만) | 최종 통제로 수용하지 않음 | A 는 임시 상한일 뿐 |
| 두 조건 1 μV 선택 규칙 (우리 Q2 예시) | `NOT_ACCEPTED_AS_GENERAL_EQUIVALENCE` | 두 조건 sentinel 통과는 "선택 두 조건의 sentinel 통과" 일 뿐 |

Q1–Q6 답 (사본 요지): Q1 필요 — C 정확 고정 · B 별도 · D 신규 생산 · Q2 26.7.1 ↔ 26.8 비교는 고정 결정의 선행 조건이 **아니다** — 두
환경의 동등 · 대체 가능을 주장하거나 정본 생산 환경을 옮길 때 사전 고정된 비교가 필요 · Q3 solver 배포판 · 실제 solver class/옵션 ·
전이 의존성 · Python/플랫폼을 함께 묶고, 허용하지 않은 fallback 은 생산 전에 거부 · Q4 **G87-N1 종결 뒤 별도 사용자 승인 · 별도
라운드** (같은 영수증 사이클에 넣지 않는다) · Q5 목적별 lock/해시 · 원본 보존 · 설치 식별과 실제 origin · guard 양성 · 음성 · 회귀 ·
smoke · 전체 변이 · 역사 영수증 보존 · 새 validator 식별 (재생성 동등성 주장 때만 계산 비교 추가) · Q6 기준은 승인 전 고정된 profile
파일 해시 — 역사 프로필의 출처는 정본 producer manifest, 신규 프로필의 출처는 별도 사용자 결정. 원문은 묶음의 `PYBAMM_REVIEW_KO.md`.

## §2 우리 요청문의 사실 정정 (검토자 P1 · P2 · P3 — 우리 raw 로 다시 확인)

| # | 요청문 원문 (`00ed85b44`) | 정정 | 근거 (우리 쪽 재확인) |
|---|---|---|---|
| P1-a | §1 "균일 격자면 6e-8 V" | **조건마다 다르다**: pristine full-cell 최대 차이 **3.614e-4 V (0.3614 mV)** · 용량 Δ −0.0657 mAh · degraded **6.002e-8 V**. "두 조건 모두 6e-8 V" 로 요약하지 않는다 | `wiki/raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md` 균일 강제 출력 원문 (`[lli=0.0 …] v_full: max|Δ|=3.614e-04`) |
| P1-b | §1 행 이름 "26.8 ↔ 26.9 (#5755 · x 격자 접합부)" · §2 A "26.9 (#5755 2.7 mV)" | 2.707 mV 는 **두 환경의 차이**다 — pybamm 26.8.0.0 + pybammsolvers 0.9.1 + CasADi 3.7.2 ↔ 26.9.0.0 + 0.10.0 + 3.8.1. **#5755 하나의 인과 효과로 확정하지 않는다.** 균일 강제 비교는 접합부만이 아니라 격자 해상도도 바꿨으므로 (x 20/20/20 → 71/10/63 점) 남은 차이를 solver 몫으로도 확정하지 않는다. #5755 (비균일 node 간격의 보간 · 외삽 수정) 는 메커니즘상 관련 근거로 남는다 | 같은 raw 의 solver identity 줄 · `UNIFORM_X=1` 의 `var_pts` 줄 |
| P2-a | §2 B "정본 재생성 환경의 drift 전부" | "**명시한 세 배포판의 버전 drift**" 로 좁힌다 — Python · NumPy/SciPy · 플랫폼/아키텍처 · native 라이브러리 · 실제 wheel/source · 로컬 패치 · solver 옵션은 남는다 (#5813 패치 비교는 같은 버전 문자열에서 바이트가 바뀐 사례) | `wiki/raw/repositories/2026-10-03-pybamm-pr5813-graded-electrode-and-synthetic-truth.md` |
| P2-b | §1 requirements 주석 Python 3.11 과 정본 생산 Python 3.10.12 를 한 표에 | 섞지 않는다 — 3.10.12 는 인계문 (`docs/05_HANDOFF.md:267`) 이 인용하는 값이며, B 프로필을 확정할 때 producer manifest · 당시 환경 기록으로 확인할 대상 | 검토자 P2 |
| P3 | §1 마지막 행 "실행 환경 ↔ 정본 생산 환경의 동일성은 아무 곳도 묻지 않는다" | 문장은 맞다. 다만 "환경을 기록하지 않는다" 로 읽히면 틀리다 — `src/io.py:233–275` 가 Python · 플랫폼 · 주요 패키지를 기록 · `:1344–1348` 이 effective_solver 필수 정보의 **존재**를 검사 · `src/grid.py:264–266` 이 실제 solver 와 환경을 서명에 넣음 · `:273–298` 이 worker ↔ parent 서명 대조 (청크 저장 전 — 승인 프로필로 생산하기 위한 최초 허가 검사와 같지 않다) · `src/runner.py:36` 이후 IDAKLU 생성 실패 시 CasADi fallback 경로. **빠진 것은 독립적으로 승인된 expected profile ↔ 새 생산 환경의 대조**다 | 검토자 P3 (좌표는 `00ed85b44` — 그 뒤 `src/io.py` · `src/grid.py` · `src/runner.py` 불변) |

같은 단일 원인 문장의 사본: `wiki/entities/pybamm.md` · `wiki/questions/22p-physics-or-degeneracy.md` · `wiki/index.md` ·
`HANDOFF_2026_10_02_DASHBOARD.md` §1-2 → 이 접수와 같은 커밋에서 취소선 + 정정 (덮어쓰지 않는다 — `wiki/SCHEMA.md` Update Policy).
`docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md:320` (§13-7 보류 문단의 괄호 "26.9 #5755 가 합성 truth 를 ≤2.7 mV 움직임") 는 승인된 고정 표라
고치지 않는다 — 정정본은 이 파일이다.

## §3 우리 의견 (결정은 사용자)

- **수용한다.** 목적별 프로필 분리 (B 역사 재생성 · C 현재 검증 · D 신규 생산 guard) 는 우리 초안 A–E 의 빈칸 — "어느 환경의
  무엇을 보호하는가" 가 섞여 있던 것 — 을 정확히 가른다. 우리 요청문의 "선행 측정 제안" (26.7.1 ↔ 26.8 두 조건 · 약 10 s) 은 고정
  결정의 선행 조건이 아니게 됐다 → **후보로만 남긴다** (나중에 두 환경의 동등 · 대체를 주장할 때 사전 고정 비교의 sentinel 하나).
  1 μV 단일 문턱 꼴의 규칙은 내려놓는다 (solver rtol/atol 1e-6 은 전압 절대 오차 1 μV 보증이 아니라는 지적도 수용).
- **D 의 기준이 실행 환경이 아니라 봉인 profile 이어야 한다**는 점은 우리 v6 계획 구조와 같은 결이다 — 계획 index 가 이미
  `planned_envelope` 를 digest 로 결속하므로, profile 파일 digest 를 계획의 결속 축으로 더하는 꼴이 자연스럽다. 설계는 그
  라운드의 고정 표에서 한다 (지금 정하지 않는다).
- **기존 정본 수용은 소급 취소하지 않는다** (검토자와 같음) — 현 validator 가 옛 producer 자료를 검사할 수 있다는 것과 현 환경으로
  옛 자료를 같게 다시 만들 수 있다는 것은 다른 주장이다.
- **배치:** G87-N1 종결 (GATE88 회신) 뒤 별도 사용자 승인 · 별도 라운드. 이번 영수증 사이클 (`38522285f` · validator
  `7dd546baaee9e823`) 에는 넣지 않았다 — 지금 그대로다.

## §4 다음 사용자 결정

G87-N1 이 닫힌 뒤: **환경 고정 라운드 착수 여부** — 승인하면 그 라운드 첫 커밋이 고정 표 (C 프로필 lock 범위 · B 프로필의
역사 증거 출처 · D guard 의 결속 자리와 음성 사례 목록 — 검토자 "D 의 최소 설계와 닫힘 조건") 이고, RED → 최소 구현 → 변이 →
영수증 → 전체 회귀 · smoke · 전체 재생 → 게이트 요청 순서는 같다.

## §5 이 접수가 바꾸지 않는 것

`requirements.txt` · RUN_SCOPE · 진행 중 GATE88 (판정 대상 `e462a3d19`) · 운영 환경 · 기존 정본 · 영수증. 검토자 수치는 제출자 원문
로그의 재인용이며 재측정이 아니다 (검토자 `limits`).
