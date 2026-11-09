# Rint ② 회차 ④ (11-09) 뒤 수정 계획 — PC14-02 · PC14-03 (재개 출처 공통 검증) · RR4-01 (변이 회계)

- 근거 = Codex 판정문 `docs/reviews/codex_review_rint2_rr_round4_20261109.md` (리뷰 핀 `1f9f3607e` · 판정 = **지정 11 항목 한정 닫힘 · 재개 정책 전체 HOLD** · 새 P1 · P2 0 · 새 P3 1 = RR4-01) · 반입 `docs/reviews/codex_rint2_rr_round4_evidence_20261109/README_import.md` · 우리 트리 재현 = 판정값 차이 0 (`docs/reviews/codex_rint2_rr_round4_evidence_20261109/_repro_ours_20261109/README.md` — PC14-02 R1 · R2 · PC14-03 attempt-null · from-rebind 가 우리 핀 · 우리 Linux 에서도 자격 True · 실제 recover 결과 줄 resume_ok True).
- 상태 = ~~⬜ **1저자 비준 대기** · 결과 0 건 (이 계획은 코드 · 시험 · 문서를 아직 하나도 바꾸지 않는다 · 반입 커밋 = 판정문 · 증거 · 원장 · 이 계획 · 진행 기록 한 줄)~~ → ✅ 1저자 11-09 *"권고대로"* = Q1–Q3 (가) · 고침 = §6 실행 기록 (작업 트리 커밋 하나 · 원장 · 게이트 · push = 메인 세션 · 다음 = 사전 공격 15 → Codex 회차 ⑤).
- 줄 번호 = 핀 `1f9f3607e` 의 `scripts/rint_r_chain.py` (sha256 47a520e8… = 판정문 §2 의 실제 로드 소스) · 핀 → 반입 바탕 `e814b73c3` 사이 `scripts/` 변경 없음.

## 0. 쉽게 말하면

- 회차 ④ 는 요청한 11 항목 (RR3-01 · 02 · PC12-03 · PC13-01 · 02 · 04 · PC14-01 · 04 · 05 · 06 · SELF-158) 을 지정 범위에서 **닫았다** (원장 verified 11).  새 치명 · 중대 결함은 없다.
- 재개 정책 전체 GO 를 막는 것은 이미 등록된 한정 둘 (`PC14-02` · `PC14-03`, P3 · 열림) 이다 — 재개 자격을 정하는 길이 **디스크 · 원장과 모순인 요약을 그대로 믿는다**:
  - PC14-02: 요약에서 "어느 런이 복사이고 어느 런이 새로 돌았나" 표기만 바꾸면 자격 True.  디스크에는 가를 증거가 남아 있다 — 복사한 런의 launch / end 기록은 원천과 바이트가 같고 (`ResumeRunner._copy` 가 그대로 복사), 새로 돈 런은 새 기록이다.  지금 자격 함수는 그 대조를 하지 않는다.
  - PC14-03: attempt.json 의 resume_of 를 null 로 바꾸거나, 3 시도 사슬에서 resume.from 을 그 시점 사슬 끝 (attempt_2) 이 아니라 옛 시도 (attempt_1) 로 바꿔도 자격 True.  원장 항목과의 대조는 판정 · 합치기 (`found_attempts_problem`) 에서만 하고, from 은 그것도 안 본다.
- Codex: "봉인 때 한 번 확인" 으로 넘기는 것은 **반대** (봉인 뒤 생기는 시도 폴더 · launch/end · 복사 경계는 봉인 때 없다).  ① (권고) 자격 결과를 쓰기 전과 다음 재개를 허용하기 전에 공통 검증 · ② 매 recover · 재개마다 외부 관문.
- 새 P3 `RR4-01` = 사전 공격 14 의 변이 회계에서 M56 을 동치로 뺐는데 실제로는 구별되는 변이다 (일반 파일 attempt_1 + 옆 거부 기록) → 역사 수를 45/50 · 생존 5 로 정정하고 그 입력을 음성 시험으로.  지금 코드 결함은 아니다 (현재 코드는 그 입력을 거부).
- 권고 = Q1 (가) 코드 공통 검증 · Q2 둘 다 · Q3 시험 먼저 → 고침 → 사전 공격 15 (독립) → Codex 회차 ⑤ 짧은 재확인.

## 1. PC14-02 · PC14-03 — 무엇이 어디서

| 자리 | 줄 (핀) | 지금 | 판정문 · 하위 보고 |
|---|---|---|---|
| `resume_rerun_problem` (자격 원인 멈춤의 resume 칸 대조) | 4367 · 칸 집합 4397–4399 · from 범위 4403–4409 · 복사 목록 4410–4417 · 첫 새 런 4415–4421 · 대조 전 멈춤 4423–4427 · 원천 바이트 다시 대조 4437–4450 | from = `resume_of ≤ from < n` 범위만 · 복사 목록 = 런 기록 copied_from 자기 신고 · 첫 새 런 = 기록에서 고름 · 멈춘 런 = rerun 이면 바이트 대조 전에 반환 · **고른** 런의 원천 payload 만 다시 대조 · docstring 4383–4386 이 두 한정을 스스로 적음 | §3 PC14-02 (4415–4421 · 4423–4427 · 4443–4450) · PC14-03 (4403–4409) |
| `resume_rerun_problem` resume 칸 null 길 | 4390–4396 | resume null + attempt.json resume_of null = 새 시도로 보고 None | resume_attack/REPORT.md (attempt-null) |
| `read_attempt` | 3473–3489 | 키 · schema · 번호 · target · 시작 커밋 꼴만 (원장 entry 대조 없음) | 같은 보고 |
| `resume_chain_problem` (풀기 전 사슬 다시 셈) | 3779–3801 | 사슬 시도의 결과 줄 폴더 · 지문 · 다시 셈만 · attempt.resume_of ↔ 원장 entry 대조 없음 | §3 PC14-03 |
| `found_attempts_problem` | 4816 · 4843–4848 | attempt.json target · machine · resume_of ↔ 원장 entry — 판정 · 합치기 자리 (4879 · 5009 · 5057 · 6876) 에서만 · from 은 안 봄 | §3 PC14-03 |
| `recover_ledger` (recover 결과 줄) | 7925 · 7948–7951 · 7991 | 원장 entry ↔ 폴더 = target · 시작 커밋 조상만 → `attempt_result_line` (resume_ok) | resume_attack/REPORT.md |
| `attempt_close` (사슬 끝 결과 줄) | 4762 · 4769 | `attempt_result_line` → resume_ok (같은 쓰기 자리) | — |
| `result_recount` · `result_line_problem` (결과 줄 다시 셈) | 4732–4747 · 4750–4759 | 폴더 증거만으로 다시 셈 (`result_fields`) ↔ 결과 줄 | (§2 설계 위험) |
| `attempt_order_problem` (다음 항목 · `--add --resume`) | 3545 · 3564–3574 | 결과 줄 resume_ok · 사슬 끝 · 기계 · 환경만 | §3 표 "다음 항목 순서 검사" |
| `attempt_presolve_problem` (풀기 전) | 3749 · 3770–3775 | 원천 폴더 = 결과 줄 폴더 · 지문 → `resume_chain_problem` | §3 표 "풀기 전 재계산" |
| `adoption` | 3492–3532 | effective = 그 대상 재실행 사슬 끝 (from 이 맞춰야 할 기준) | — |
| `ResumeRunner._src_done` · `_copy` | 5310–5316 · 5335–5359 | 원천 끝 기록 rc 0 + 런 폴더 → 복사 · 복사 = 런 폴더 copytree + 로그 · launch / end 를 바이트 그대로 (5340–5344) → copied_from 기록 | §3 PC14-02 (다음 재개 `_src_done(L02)` True) |

- 반례 (판정문 §3 · 우리 재현 같음 · 입력 = `docs/reviews/codex_rint2_rr_round4_evidence_20261109/resume_attack/frozen_cases/`):
  - **R1** (PC14-02) — 정직 RESUME_MISMATCH 요약 7 칸만 편집 (stop 두 칸 → TIME_LIMIT / L03 · L02.copied_from = 1 · copied [L01, L02] · rerun L03 · compared [] · determinism null) → 4423–4427 에서 대조 전에 반환 · resume_ok True · 다음 순서 통과 · 풀기 전 다시 셈 통과 · scratch Git 실제 recover rc 0 · resume_ok True · 다음 재개 `_src_done(L02)` True.  디스크: L02 launch · payload ≠ 원천 (복사가 아니라는 증거).
  - **R2** (PC14-02) — 6 칸 (stop 두 칸 · L01.copied_from 지움 · copied [] · rerun L01 · compared.same True) → 첫 새 런 = L01 (실제로는 복사) · 4443–4450 이 같은 L01 사본만 다시 대조 · resume_ok True.  디스크: L01 launch = 원천과 같음 (복사 흔적).
  - **attempt-null** (PC14-03) — stop 두 칸 · summary.resume null · attempt.json resume_of 1 → null (원장 entry 2 의 resume_of = 1 그대로) → 4390–4396 = 새 시도로 봄 · recover 결과 줄 True · 다음 순서 · 풀기 전 다시 셈 통과 · `found_attempts_problem` 만 거부 (판정 · 합치기).
  - **3 시도 from-rebind** (PC14-03) — attempt_3 의 실제 원천 = attempt_2 (effective) · 5 칸 (stop 두 칸 · resume.from 2 → 1 · L01.copied_from 2 → 1 · compared.same True) → from 1 = 범위 안 · attempt_1 의 L02 와 바이트 같음 → resume_ok True · `found_attempts_problem` 도 통과.

## 2. PC14-02 · 03 고침 안 — Q1

**(가) 코드 공통 검증 (판정문 §3 ① · 권고)**

- 새 함수 (가칭) `resume_provenance_problem(st, n, folder, s)` → 사유 | None — 원장 상태 st (항목 n 의 entry + 그 앞) 를 받는다:
  - ⓐ attempt 신원 ↔ 원장 entry — `read_attempt(folder)` 의 n · target · machine · resume_of = `st['entries'][n]` (4843–4848 의 대조를 작은 공용 함수로 떼어 `found_attempts_problem` 과 같이 씀 · 판정 · 합치기 쪽 동작 그대로).
  - ⓑ resume.from ↔ 그 시점 유효 사슬 끝 — entry resume_of 있음 ⇒ s['resume'] = 객체 · from = `adoption(st, target, upto=n)['effective']` (= 풀기 전 `resume_source` 의 eff · 3771) / entry resume_of null ⇒ s['resume'] null 이고 attempt.json 도 null.
  - ⓒ 복사 / 새 런 경계 ↔ 디스크 — copied_from 있는 런 기록마다 이 시도의 groups/<런>.launch.json · .end.json 바이트 = 원천 attempt_<from> 의 같은 파일 (`_copy` 5340–5344 가 copy2) · 그 런 폴더 payload (p2_*.json) 신원 = 원천과 같음 (필요한 파일 신원) / copied_from 없는 런 (첫 새 런부터) 은 원천에 같은 이름 launch 가 있으면 바이트가 달라야 함 (새로 돈 흔적) · 어긋나면 모순 = 사유.
  - ⓓ 그 뒤 기존 원천 payload 다시 대조 (4437–4450) 를 ⓒ 로 묶인 **실제** 첫 새 런에 · 멈춘 런 = rerun (대조 전 멈춤 · 4423–4427) 이어도 ⓐ–ⓒ 는 먼저 본다 (R1 우회 막음).
- 부르는 자리 (판정문 ① "자격 결과 쓰기와 다음 재개 허용 전"):
  1. 결과 줄 쓰기 — `attempt_close` (4769 · 사슬) · `recover_ledger` (7991 · recover) 가 `attempt_result_line` 전에 부르고, 사유가 있으면 resume_ok False (원인 = 검사 실패 쪽 · 사유 = 원장 커밋 글).
  2. 다음 재개 허용 — `attempt_order_problem` (3564–3574 · `--add --resume`) 과 `attempt_presolve_problem` → `resume_chain_problem` (3779–3801 · 사슬 시도마다) 이 같은 함수를 부르고 사유면 RESUME_NOT_ALLOWED.
  3. ⚠ 설계 위험 — 결과 줄 다시 셈 (`result_line_problem` 4750–4759 · `result_recount` 4732–4747) 은 지금 폴더 증거만으로 센다.  1 이 원장 의존 검사로 resume_ok 를 False 로 쓰면, 폴더만 다시 센 값 (True) 과 어긋나 ATTEMPT_LEDGER_MISMATCH 가 난다 → 다시 셈도 같은 st 를 받아 같은 함수를 부르거나, 원장 의존 검사를 resume_ok 밖의 따로 칸 · 관문으로 둔다 (구현 전 확인 · 시험 먼저에 행 하나).
  4. `ResumeRunner._src_done` (5310) = 그대로 (2 의 관문이 앞에서 막음 · 바꾸면 복사 · 재실행 동작이 바뀐다) — 한정에 적음.
- 시험 먼저 (고치기 전 실패 확인 → 고침 → 통과):
  - 음성 (지금 자격 True → 고친 뒤 False / RESUME_NOT_ALLOWED): N1 = R1 (7 칸) · N2 = R2 (6 칸) · N3 = attempt-null · N4 = 3 시도 from-rebind — 각각 결과 줄 쓰기 (scratch Git 실제 `recover --ledger`) · `attempt_order_problem` · `resume_chain_problem` 세 자리에서 (판정문 §3 입력 꼴 = 반입 frozen_cases 와 같게).
  - 양성 (지금 그대로): 정직 RESUME_MISMATCH (False 그대로) · 정직 비교 뒤 멈춤 (True) · 정직 첫 재실행 전 멈춤 (True) · 정직 부분 재실행 멈춤 · 정직 3 시도 사슬 (from = effective · True) · 정직 3 시도 mismatch (False) · 정직 복사 (launch / end 바이트 같음) · 새 런 (새 기록) · 새 시도 (resume_of null · resume null) · 원 PC13-01 · PC14-05 · 06 행 (PA13 · PA14) · RR3 · PC12 행 그대로.
  - 변이: 새 가드 하나 ↔ 검사 하나 (ⓐ · ⓑ · ⓒ 를 각각 지우면 N3 · N4 · N1/N2 중 해당 행이 통과로 바뀜).
  - Codex 탐침 무변경 재실행 — resume_attack/probe_resume_independent.py (반입에서 뺀 ZIP 안 이름 · 받은 묶음에 있음 · sha256 83622e5a…) 는 PC14-02 · 03 을 True 로 assert 한다 → 고친 뒤에는 AssertionError 로 멈춰야 한다 (기대한 뒤집힘 · 회차 ③ 탐침 · `docs/reviews/codex_rint2_rr_round4_evidence_20261109/arm_contract/replay_original.py` 와 같은 처리 · 그 탐침을 고쳐 PASS 로 세지 않음 · 거부 oracle = 상주 N1–N4).
  - 웹앱 = 재실행 자격 · 원장 화면 없음 (회차 ③ · ④ 요청서와 같음) → "없음" 기록.
- 한정 (그대로 적음): 모든 사본 (launch / end · payload · 요약 · attempt.json) 을 일관되게 고친 위조 = 이 계약 밖 (판정문 §3 "새로 요구하는 문제가 아니다") · 원천이 같은 바탕에 없는 시도 (다른 곳 · 판정 `--attempt-dirs`) = ⓒ ⓓ 못 함 → 지금 4442 는 None (대조 안 함) · 고칠 때 "재개 허용 안 함" 쪽으로 바꿀지 = 구현 전 확인.

**(나) 매 recover · 재개 외부 관문 (판정문 §3 ②)**

- 코드 보완을 미루고 각 `recover` · `--add --resume` 전에 사람이 원장 핀 · 요약 · attempt.json · launch / end · payload 해시를 고정하고 effective 원천 · attempt 신원 · 복사 / 새 경계 · 첫 새 런 바이트 비교를 독립 대조 · 근거 / hash 기록 전 진행 금지 · 불일치 · 미확인 = HOLD · 승인 뒤 증거가 바뀌면 다시 · 책임 · 시점 · 불변 증거 · 해제 조건을 절차 문서에.
- 표현 = "매회 수동 확인을 조건으로 한 제한적 재개 운영 수용" (코드 단독 재개 정책 GO 아님 · "봉인 때 한 번" 은 이 대안이 아님).
- 약점 = 매 재개마다 사람 손 · 비용 · 놓치기 쉬움 · 자동 정책 문장을 못 씀.

- 권고 = **(가)** — 이미 있는 대조 (`found_attempts_problem` · `adoption` · `_copy` 의 바이트 그대로 복사) 를 모아 자격 소비자에 연결하는 범위이고, 판정문이 권고한 길이며 봉인 뒤 생기는 시도도 자동으로 막는다 · (나) 는 매번 사람 손에 기대고 코드 정책 GO 를 쓰지 못한다.

## 3. RR4-01 — 무엇을 고치나 (Q2)

| 자리 | 지금 | 정정 (판정문 §4) |
|---|---|---|
| 회차 ④ 요청서 `docs/reviews/codex_rint2_rr_round4_request_20261109.md` 103 줄 | "변이 51 (동치 2) 중 45/49 를 PA13A–D 가 잡음" | 원문 취소선 + "11-09 정정 (RR4-01 · 판정문 §4): 동치 1 (M46 · JSON 영역) · 45/50 · 비동치 생존 5 (M14 · M18 · M47 · M54 · M56) · M56 = 구별 가능한 미검출 (일반 파일 attempt_1 + 옆 거부 기록)" |
| 사전 공격 14 보고 `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack14/REPORT.md` 9 줄 | "변이 51 (동치 2 = M46 · M56) 중 45/49" | 같은 꼴 제자리 표지 (역사 글 보존 · 정정 문장 덧붙임) |
| 원기록 (out/mutation_PA13.json · out/mutation_PA13_extra.json · probes/mutate.py 60 줄) | 51 · 잡힘 45 · 생존 6 · M56 killed false | **그대로** (바이트 보존 · 판정문 "역사 원로그는 보존") |
| 상주 시험 | 유효 원천 폴더만 · 일반 파일 + 옆 거부 기록 입력 없음 | 음성 행 하나: 원천 자리 = 일반 파일 attempt_<from> + 옆 attempt_<from>.rejected.json → `resume_rerun_problem` = 거부 사유 (지금 코드 통과) · M56 (is_dir → exists) 을 적용하면 그 행이 실패해야 (변이 검출 · 변이 기록 남김) |

- 처분 선택지: (가) 둘 다 (문구 정정 + 음성 시험 행) · (나) 문구 정정만 + "유효 원천 디렉터리만 시험 · 일반 파일 / 거부 기록 입력 = 미검출" 한정 명시 · (다) 시험만.
- 권고 = **(가) 둘 다** — 문구는 판정문이 요구한 회계 정정이고, 시험 행 하나로 M56 이 검출되어 "전체 입력 영역" 문장을 쓸 수 있다 · PA14 선정 23/23 · M14 · M18 · M47 · M54 종결과 섞지 않는다 (판정문 §4 끝).

## 4. 그대로 남는 것 (이 계획 밖)

- PC13-03 · PC11-05–08 (한정) · SELF-155 실침대 (kgy S0 단계 1 재실행 · 채택 조건 = `docs/reviews/rint2_rr3_fix_plan_20261108.md` §5) · 현장 자격 · 12 단위 끝-끝 · 숫자 / 실행 정책 · 새 계획 / 핀 봉인 · S0 단계 2 · 등록 R · 정량 판정 · 생산 GO — 판정문 §6 순서 · 바깥 범위 그대로.
- 이번 회차로 쓸 수 있는 문장 = 판정문 §6 인용 그대로: "RR3-01·02, PC12-03, PC13-01·02·04, PC14-01·04·05·06 및 SELF-158 문장 정정은 지정한 코드·합성·문서 범위에서 닫힌다. 재개 출처·복사 경계의 PC14-02/03은 열림이며 재개 정책 전체는 HOLD다. 실제 환경 자격·S0 단계1 채택·12단위 통합·새 계획/핀 봉인 및 연구 실행 승인은 별도다. 변이 M56의 비동치 생존을 RR4-01로 기록하고 검출률을 정정한다."

## 5. 결정 질문 (✅ 1저자 11-09 *"권고대로"* = Q1–Q3 (가))

**Q1 — PC14-02 · 03 처리 방식** (§2)
- (가) 코드 공통 검증 (ⓐ attempt 신원 ↔ 원장 entry · ⓑ resume.from ↔ 그 시점 effective · ⓒ 복사 / 새 경계 ↔ 원천 launch / end · 파일 신원 · ⓓ 실제 첫 새 런 payload 다시 대조 · 결과 줄 쓰기 · 다음 재개 허용 · 다시 셈이 같은 함수) / (나) 매 recover · 재개 외부 관문 (절차 문서 · 코드 정책 GO 아님).
- 권고 = **(가)** — 판정문 권고 · 봉인 뒤 시도까지 자동 · 이미 있는 대조를 모으는 범위.

**Q2 — RR4-01 처분** (§3)
- (가) 역사 문구 정정 (원로그 보존 · 45/50 · 비동치 생존 5) + 일반 파일 / 거부 기록 음성 시험 행 (M56 검출) / (나) 문구 정정만 + 입력 한정 명시 / (다) 시험만.
- 권고 = **(가) 둘 다**.

**Q3 — 순서**
- (가) 시험 먼저 (N1–N4 · RR4-01 행 · 고치기 전 실패 확인) → 고침 (커밋 하나 → 게이트 → push) → 사전 공격 15 (독립 · diff 만 · 보장마다 작은 해석 반례 · 같은 부류 = 다른 런 정직 기록 차용 · 원천이 다른 바탕 · 다시 셈 일치) → Codex 회차 ⑤ 짧은 재확인 (PC14-02 · 03 · RR4-01 만 · 회차 ④ 재개 탐침 무변경 재실행 = 기대한 뒤집힘).
- (나) Codex 에 설계 (§2) 먼저 확인받은 뒤 고침.
- 권고 = **(가)** — 판정문 §3 이 최소 처리를 이미 구체로 적었고 (공통 검증 셋 · 양성 보존 목록), 회차 ③ → ④ 와 같은 흐름이다.

## 6. 실행 기록 (11-09 · 작업 트리 에이전트 · 바탕 `e48e5fa04` · 커밋 하나 · 원장 · 게이트 · push = 메인 세션)

- 증거 = `docs/reviews/rint2_rr4_fix_evidence_20261109/` (code.diff · code_sha256.txt · logs · tools · SHA256SUMS) · 코드 sha256 `scripts/rint_r_chain.py` 47a520e8… → d0e04017… · `scripts/test_rint_r_chain.py` d5e1d9ea… → 92998cbc… · 웹앱 = 없음 (재개 자격 · 원장 화면 0 건).
- Q1 (가) = 공통 함수 `resume_provenance_problem` (ⓐ attempt.json ↔ 원장 항목 = `found_attempts_problem` 과 같은 `attempt_entry_diff` · ⓑ resume.from ↔ `adoption(...)['effective']` · 원천 attempt_<from> 찾기 · ⓒ 복사 / 새 경계 ↔ 원천 launch / end 바이트 · 남은 payload · 새 런 launch 다름 · ⓓ 실제 첫 새 런 payload 다시 대조 · 멈춘 런 = rerun 이어도 ⓐ–ⓒ) · 부르는 자리 = 결과 줄 쓰기 (`attempt_close` · `recover_ledger` → 자격 False · 사유 = 원장 커밋 글 · 화면) · 다시 셈 (`result_recount` · `result_line_problem` = 같은 원장 상태 · 같은 셈 함수 `result_fields_ledger` = §2-3 설계 위험 해소) · 다음 재개 허용 (`attempt_order_problem` · `resume_chain_problem` → RESUME_NOT_ALLOWED) · `ResumeRunner._src_done` 그대로 (한정).
- §2 한정 "원천이 같은 바탕에 없는 시도" = 메인 결정 fail-closed 로 구현 (못 찾음 · 확인 못 함 = 사유 [원천]) · 구현 전 확인 = 정직 흐름 깨짐 없음 (아래 수) → STOP 없음.
- Q2 (가) = 요청서 103 줄 · 사전 공격 14 보고 9 줄 제자리 정정 (취소선 + "11-09 정정 (RR4-01 · 판정문 §4)" · 원로그 셋 바이트 그대로 · 사전 공격 14 SHA256SUMS 의 REPORT.md 줄만 갱신) + 상주 음성 행 RR4C · 변이 M56 = 잡힘.
- Q3 (가) 수 = 고친 시험을 바탕 사슬에 먼저 `--only RR3,PA13,PA14,RR4` 15/19 (음성 9 행 전부 받음 · RR4C 만 통과) → 고친 뒤 19/19 · 사슬 495 → 500/500 (3.11 · kgy 판 3.8.20) · 끝-끝 51 PASS (3.11 · 3.8.20) · kgy 판 11 묶음 통과 · 변이 12/12 (ⓐ · ⓑ · ⓒ · ⓓ · 원천 · 부르는 자리 다섯 · M56) · Codex 재개 탐침 무변경 = AssertionError 181 줄 (PC14_03 attempt-null 단언 · 기대한 뒤집힘).
- 벗어남 = 고정물 하나 (`pa13_ledger` 합성 원장 항목 기계 'synthetic' → attempt.json 과 같은 MACH · 기대값 그대로 · 옛 값이면 PA13A 의 한 행만 다음 재개 [ⓐ] = 생산자 밖 고정물 모순) · 결과 줄 칸 · 원인 칸 그대로 (사유 = 커밋 글 · 화면 · 폴더 증거 모순과 같은 처리).
- 다음 = 사전 공격 15 (독립 · diff 만) → Codex 회차 ⑤ 짧은 재확인 (PC14-02 · 03 · RR4-01 만) · 원장 claimed_fixed = 메인 세션.
