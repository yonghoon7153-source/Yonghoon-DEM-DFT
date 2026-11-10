# Rint ② 회차 ⑥ 판정 처분 · 수정 계획 (2026-11-10 · 서브 세션 · 가지 B)

판정문 = `docs/reviews/codex_review_rint2_rr_round6_20261110.md` (리뷰 핀 `aec8ca2f6` · 반입 = 이 문서가 든 커밋) · 증거 = `docs/reviews/codex_rint2_rr_round6_evidence_20261110/` (반입 기록 `README_import.md` · 우리 트리 재현 `_repro_ours_20261110/`).  전체 HOLD 그대로 · 실행 승인 아님.

## 0. 판정 요지

| 질문 | 판정 | 이 커밋의 처분 |
|---|---|---|
| Q1 RR5-01 | 닫힘 (문서 결함 한정) | 원장 RR5-01 → verified (범위 = 판정문 §2 Q1 칸) · RCA-11 전체 · 실제 계획 `s_min_um` 0 봉인 · 후속 기술 보고는 남음 (RCA-11 메모) |
| Q2 Q6 수용 문장 | 수용 | 처분 없음 (재개 정책 전체 · 모든 prefix · 현장 자격 인증으로 넓히지 않는다) |
| Q3 S0 반입 경계 | 수용 | 처분 없음 (SBE 원자료 채택 유지 · importer 자동 인증 아님) |
| Q4 현장 자격 | 부분 수용 · §7④ 미종결 | `docs/reviews/rint2_rr3_fix_plan_20261108.md` §7④ 아래에 판정문 §3-3 권고 문장 그대로 · 남은 운영 조건 = 아래 §2 |
| Q5 남은 순서 | 보완 필요 | `docs/reviews/rint2_rr5_fix_plan_20261109.md` §4 끝에 판정문 §5 권고 문안 그대로 (⑥ SBE 수치 탐침 · 기하 · 실측 반복 수 검토 회신 · 비용 결정점 · s_min 선택 ≠ 최종 봉인) |
| 새 P3 RR6-01 | C02b 가 자식 rc 를 버림 | 고침 (아래 §1) |
| 새 P3 RR6-02 | 준비 폴더 README 해시가 옛 판 | 고침 (아래 §1) |

## 1. 이 커밋에서 고친 것 (Codex 최소 수정 그대로)

- **RR6-01** `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` C02b: PASS 에 자식 rc 0 을 함께 요구 · `path_python3_rc` 기록 · stderr 끝 200 자 (`path_python3_stderr_tail`) · detail 에 rc.  시험 먼저 = `docs/reviews/rint2_siteq_prep_20261109/tools/test_siteq_c02b.py` (Codex 와 같은 AST 메모리 방식 · 실제 자식 0 회) 고치기 전 5/10 → 뒤 10/10 · 게이트 단계로 넣음.  Codex 탐침을 고친 트리에 무수정으로 돌리면 61 행 AssertionError (옛 동작 PASS,PASS,FAIL,FAIL 을 단언 · 기대된 실패) · 기대만 바꾼 사본은 rc 0 · rc 1 사례 = FAIL (`docs/reviews/codex_rint2_rr_round6_evidence_20261110/_repro_ours_20261110/repro_summary.json`).
- **RR6-02** 준비 폴더 `SHA256SUMS` 를 지금 바이트로 다시 씀 (README · 고친 도구 · 새 시험 · 6 행 `sha256sum -c` OK) · README 에 역사 해시 줄 (두 현장 기록이 쓴 판 = 도구 `a490b9ad…` · README `6401d4f9…` · db86ce9b9).
- 두 현장 기록 (kgy · gabia 11-09) 의 C02b 는 고치기 전 도구의 결과라 PATH python3 자식의 정상 종료 증서가 아니다 (한정 그대로 · 재실행 자동 요구 없음).
- 원장: RR6-01 · RR6-02 = open (고침 = 이 커밋 · claimed_fixed 는 sha 가 필요해 다음 커밋 = 본 세션).

## 2. 1저자 결정 (봉인 전) — ✅ 1저자 11-10 *"권고대로"* (Q1–Q4 전부 권고 칸 그대로)

| # | 질문 | 권고 = 결정 (11-10) |
|---|---|---|
| Q1 | kgy 의 umask 002 를 R 실행 전에 022 로 둘까요 (결과 · 원장 · 계획 파일 = 단일 작성자) | 예.  실행 셸에서 umask 022 + 실제 파일 · 폴더 모드 확인 |
| Q2 | gabia 를 root (UID 0) 로 그대로 쓸까요 | 일반 계정이 있으면 그 계정 · 없으면 root 그대로 두고 실행 정책에 UID 0 과 값 비열람 절차를 적는다 |
| Q3 | 고친 도구로 C02b 를 현장에서 다시 볼까요 | 봉인 직전 현장 확인 때 한 번에 (C02b + 실제 계획 경로 C26 + umask) · 따로 블록을 돌리지 않는다 |
| Q4 | RR6-01 · RR6-02 고침을 Codex 가 언제 확인할까요 | 따로 회차를 열지 않고 다음 실질 회차 (⑥ SBE 수치 탐침 결과 · 봉인 전 묶음) 에 함께 |

## 3. 다음 순서 (판정문 §5 문안 = rr5 계획 §4 끝)

1. 현장 자격의 남은 경로 · 문맥 · 권한 조건과 12 단위 연결 확인 계획을 구체화한다.
2. 등록된 ⑥ SBE 수치 탐침 (σ 봉인 · 사슬 밖) 을 돌리고 기하 · 실측 반복 수 검토 회신과 비용 결정점을 거친다 (실행 = 1저자 GO).
3. 숫자 · 실행 정책 · s_min · S0/R 계획 해시를 단일 개정 커밋으로 최종 봉인한다.
4. 핀 · 의존 지문 · 동일 코드 조건을 확인한 뒤 S0 단계 2 (DBE) 진입을 따로 판단한다.
