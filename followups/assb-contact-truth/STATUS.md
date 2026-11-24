# ASSB 합성 truth — 접촉 손실 (θ · φ) ↔ `LAM_PE` · 독립 흐름 상태판

> **흐름 이름:** ASSB 합성 truth · **시작:** 2026-11-24 · 사용자 결정 "권고대로 진행하고 백그라운드 에이전트로 진행"
> (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-k 결정 3 의 ✅ 문단).
> 게이트 루프 · REIL · COMSOL · 논문 후속 (Phantom pOCV) 과 **섞지 않는다.** RUN_SCOPE (`degradation-degeneracy/` 의
> `src/ tools/ configs/ scripts/ run.sh requirements*.txt`) 를 바꾸지 않는다 — forward 쓸기는 저장소 밖 버리는 사본 · 스크래치패드에서만
> (P3 선례). `degradation-degeneracy` 코드로 옮기는 단계만 게이트 루프를 거친다 (지금 리뷰어 사용 불가 → 대기). 결과 수치는 진단
> 전용이고 위키에 옮겨 적지 않는다.

## 근거

| 항목 | 위치 |
|---|---|
| 결정 | `bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-k 결정 3 (✅ 2026-11-24) |
| 닻 물음 (카드) | `wiki/questions/assb-contact-loss-vs-lampe.md` |
| 요구 R1–R8 · 설계 선택지 기록 | `wiki/concepts/assb-synthetic-truth-contact-loss-requirements.md` |
| 곱 축퇴와 처방 표 | `wiki/concepts/assb-lampe-contact-product-degeneracy.md` |
| 첫 실행 후보 | 원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b (차)(처) · 선결 (투)(무) |
| 설계서 | `followups/assb-contact-truth/DESIGN_v1.md` (v1 · 2026-11-24 · 문서만) |
| 선례 (사전 등록 · 버리는 사본) | `followups/phantom-pocv/P3_APPROVAL_REQUEST.md` · `followups/phantom-pocv/p3_20261106/README.md` |

## 진행표

| 단계 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| D0 다음 방향 — 문헌 접고 합성 truth | **완료** (2026-11-24 사용자 결정 · 권고대로) | `ASSB_TRANSFER_NOTE.md` §6-3-k 결정 3 · `wiki/log.md` 2026-11-24 | — |
| D1 설계서 v1 | **작성 — 검토 대기** (2026-11-24 · 코드 0 · 설치 0 · 실행 0) | `DESIGN_v1.md` | 사용자 검토 · `DESIGN_v1.md` §7-3 결정 D1–D8 |
| S 구현 스파이크 (S0–S6) | 대기 — C1 승인 뒤 첫 단계 | `DESIGN_v1.md` §3-2 | 미확인 PyBaMM 기능 확인 · 실패하면 격자 전에 중단 |
| C1a (차) 면적 ↔ `j₀` 서명 표 · 검출 지도 | **대기** (승인 전 실행 0) | `DESIGN_v1.md` §5-2 · §5-4 · §5-5 | 승인 문구 `DESIGN_v1.md` §7-4 (D1) |
| C1b (처) 바인더 짝 · 65호 모양 재현 · 첫 충전 상한 검사 | **대기** | `DESIGN_v1.md` §5-3 · §5-6 | 같은 승인 |
| C1 선택 팔 — AD 대리 (면적 노브의 확산 몫) | 대기 · 사용자 결정 | `DESIGN_v1.md` §2-3 · §5-9 순서 8 | D3 |
| C1 선택 — EIS (`pybamm-eis` 새 의존성) | 대기 · 사용자 결정 | `DESIGN_v1.md` §1-2 · §4-1 B5 | D4 |
| C2 역문제 · 식별성 (C2a 펄스 적합 · C2b OCV 3 매개) | 미착수 — C1 뒤 새 설계 | `DESIGN_v1.md` §6-1 · §6-2 | — |
| C3 동역학 truth (R8 두 형태 · R4 재연결 · d_LAM) | 미착수 | `DESIGN_v1.md` §2-7 · §6-3 | 판 (≥26.10 새 프로필) · d_LAM — D7 |
| 게이트 (본 연구 코드로 이식) | 대기 — 리뷰어 사용 불가 | `DESIGN_v1.md` §6-5 | — |

## 규칙

- 설계 (격자 · 판정 · 중단 조건) 는 **실행 전에** 설계서 §5 와 §8 (실행 전 고정값) 에 고정하고, 결과를 본 뒤 바꾸지 않는다. 바꿔야
  하면 기록 → 사용자 승인 → 새 시계 원점 (P3 2 · 3 차 선례).
- C1 수치는 **같은 실행 묶음 안에서만** 비교한다 — 본 연구 수치와 섞지 않는다 (code · env identity 가 다르다).
- 실행 기록: 시작 / 종료 HEAD (저장소 · 사본) · 사본 sha · 환경 (판 · pip freeze sha256) · 명령 · stdout / stderr · 외부 rc ·
  자원 관측 · 결과 파일 sha.
- 결론 문장에는 그 결론을 만든 R 가정 (특히 R5) 과 truth 꼴 (1D 균질) 을 단다 (설계서 §2-8 · §5-5).

## 게이트 후보로 넘길 것 (이 흐름에서 고치지 않음)

- ASSB forward 를 `degradation-degeneracy` 로 옮길 때 `src/modes.py` 의 `LAM_PE` 꼴 (죽은 자리 → 공극 · `docs/07_LAM_LLI.md` §2) 을
  그대로 쓰지 않는다 — 액체셀에서는 정당한 선택이지만 ASSB truth 에서는 R3 위반이다 (설계서 §2-4).
- 3 매개 상자 · `degradation_modes` 재정의 (`ASSB_TRANSFER_NOTE.md` §1-1 · §4).
- 두 상 양극 + 이중층 truth 는 PyBaMM ≥26.10 (#5805) — 의존성 파일 변경 = RUN_SCOPE (설계서 §1-2).
