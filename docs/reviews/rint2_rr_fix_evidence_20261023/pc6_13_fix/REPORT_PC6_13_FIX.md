# Rint ② PC6-13 (선택지 A) · PC6-02 CUDA 라이브러리 표지 고침 (11-02 · 작업 트리 에이전트)

기준 `e12756051` · 바꾼 파일 `scripts/rint_r_chain.py` · `scripts/test_rint_r_chain.py` · `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · 결정 = 1저자 11-02 *"권고대로해요"* (원장 `PC6-13` · `PC6-02` decision_note)
본 가지 커밋 (11-02 `cherry-pick -x` · 충돌 0): `c738a6826` (시험 먼저 · 고치기 전 0/7) · `4499f3ffd` (고침) · `7f277f9e7` (증거) · `2bef88e60` (등록 R 문구) · `2c1a06c57` (증거 보탬).  아래 줄 번호 = `4499f3ffd` 의 `scripts/rint_r_chain.py`.  본문 = 에이전트 반환문 (sha 만 본 가지 값으로 바꿈).

## 이번에 닫는 것

- PC6-13 요약 있는 길 — `stop_cause` (:3643) 의 GROUP_UNCONFIRMED 가지 (:3667): 멈춘 런 기록 rc 가 실패 (`runner_rc_failed` :3620 = 정확한 int 0 · None 아님 · bool · 실수 · 글 = 실패 = 보수) 면 `words_cause(txt, 'runner_rc')` (잘못된 주소 → 자원 → CUDA 표지 → 기본 runner_rc) · 런 기록 rc = 러너가 스스로 끝났을 때만 (`Runner._execute` 그대로) → 사슬이 죽인 런 · 정리 중 신호 = None = 옛 그대로 group_unconfirmed · 멈춤 이름 그대로 (recover 먼저) · 멈춤 문장에 러너 rc (:4194 · 화면 · 단계 요약 stop.cause — 결과 줄 stop.reason · 다시 셈 무관)
- PC6-13 요약 없는 길 (창 = 사슬이 미확인 끝 기록을 쓴 뒤 · 단계 요약 전 사망) — `recover_group` (:6444) 이 갈아 쓰는 옛 끝 기록 (by chain) 요약 → 새 끝 기록 칸 `chain_end` {rc · cause · confirmed · ended_utc} (:6470 · :6518 · 앞 recover 의 chain_end 이어받음 · 새 끝 기록 rc = None 그대로 = `ResumeRunner._src_done` 무영향) · `orphan_cause` by recover (:3714) = `chain_end_failed` (:3627 · 원인 None + 실패 rc) 면 기본 runner_rc
- GROUP_UNCONFIRMED 가 원인 · 재실행 자격을 정하는 자리 전수 — ① stop_cause = 고침 ② `_execute` 멈춤 = 이름 · rc 기록 그대로 · 문장만 ③ recover_group + orphan_cause = 고침 (창) ④ 봉인 원천 런 미확인 = GraphSourceError → SV_UNCHECKED (재실행 결정 아님 · 그대로) ⑤ 사슬이 끝 기록 전에 죽은 런 = 러너 rc 없음 → 옛 그대로
- CUDA 표지 (PC6-02 decision_note) — `CUDA_ERROR_WORDS` (:2796) += `CUBLAS_STATUS_` · `CUSOLVER_STATUS_` · `CUSPARSE_STATUS_` · `CUFFT_` · `CUDA error:` · `words_cause` (:3600) 무변경 = 차례 그대로 · 모든 길이 이 함수
- 등록 R §10-5 아 ② (CUDA 표지 = 모든 길 · 라이브러리 문자열 · 차례 · 한정) · ⑦ (PC6-01 러너 세션 · 계보 · PC6-09 화면만 rc 3 · 아무것도 쓰지 않음 · PC6-12 한 함수 · PC6-13) + 나 ⑫ · 아 ⑥ 바뀐 자리 표지 + 머리 ★ 11-02 줄
- 웹앱 — grep (`GROUP_UNCONFIRMED` · `CUDA_ERROR_` · `runner_rc` · `group_unconfirmed` · `parent_dead` · `cudaError` · `CUBLAS`) = 0 건 → 바꿀 화면 없음

## 시험 (로그 = logs/)

- 새 7 (PD13 · PD13o · PD13g · PD13r · PD13d · PD02c · PD02cr) 고치기 전 0/7 (before_PD13_PD02c.log) → 7/7 (after_PD13_PD02c.log)
- 전체 421 → 428/428 (full_after.log) · 끝-끝 40/40 (e2e_after.log) · 3.8 (check_kgy_py38.sh 꼴 · 3.8.20 · numpy 1.24.4 · scipy 1.10.1) PD,PC 42/42 (py38_PD_PC.log)
- check_doc_refs rc 0 · check_review_findings rc 0 · --ban-sweep 누수 없음

## 변이 (mutate_pc6_13.py · mut_reasons.py)

19 (PC6-13 가드 12 = G13a–l · 라이브러리 표지 7 = L02a–g) = 잡힘 19 · 옳은 이유 19 · BASE 7/7 통과

## 닫지 않는 것

- 사슬이 끝 기록을 쓰기 전에 죽은 런 (러너 rc 를 모름) = 옛 그대로 parent_dead (로그에 파이썬 traceback 이 있어도 · traceback 낱말 규칙 = 결정 밖 · PD13o no_ce_python 이 경계)
- 정리 중 신호 (signal_after) — 요약 있는 길 ↔ 요약 없는 길의 원인 차이 = 옛부터 · 결정 밖
- ⚠ 자원 낱말 다섯이 없는 메모리 실패 꼴 (`*_ALLOC_FAILED` · `CUSPARSE_STATUS_INSUFFICIENT_RESOURCES` · 맨 `CUDA error: out of memory`) = 이제 runner_rc (보수) — 1저자 결정 문장 "메모리 부족은 그대로 resource" 는 자원 낱말이 함께 찍힌 줄 (cupy 꼴) 에서만 선다 (probe_open_q.log · 메인 설명 오기 = 원장 SELF-147)
- 표지 = 부분 문자열 · 대소문자 그대로 (`CUFFT_PLAN_CACHE_SIZE` 같은 무해한 언급 = 재실행 막음 · `CUDA Error:` = 못 잡음)
- 멈춘 런 기록이 없는 GROUP_UNCONFIRMED 요약 (손 고침) = 옛 그대로 group_unconfirmed
- 이 고침 전에 쓴 결과 줄 (그룹 미확인 + 러너 rc ≠ 0) = 다시 셈이 다르게 셈 (실제 R 원장 결과 줄 없음 · 봉인 전)
- kgy 실제 (3.8.10 · 비 root) · Codex 회차 ②

## 열린 질문 (1저자)

- Q1 자원 낱말 없는 메모리 실패 꼴을 자원 낱말 (재실행 자격) 에 넣을지 — 에이전트 권고: 지금대로 (자동 재실행 없음 · 보수 · 지금 payload (cupy) 의 메모리 부족은 이미 자원 낱말이 함께 찍힘)
- Q2 사슬이 끝 기록 전에 죽은 런의 파이썬 traceback 낱말 규칙 — 권고: 결정 밖 · Codex 회차 ② 요청서 한정
- Q3 signal_after 두 길 차이 — 권고: 한정으로 적고 Codex 회차 ② 에 묻기
