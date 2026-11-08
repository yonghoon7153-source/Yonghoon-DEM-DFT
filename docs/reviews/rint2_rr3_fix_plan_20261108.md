# Rint ② 회차 ③ (11-08) 뒤 수정 계획 — RR3-01 · RR3-02 · 봉인 전 확인 · kgy S0 단계 1 채택 조건

- 근거 = Codex 판정문 `docs/reviews/codex_review_rint2_rr_round3_20261108.md` (리뷰 핀 `17d45fb9c` · 판정 **HOLD** · 새 P1 0 · P2 1 · P3 1 · 닫힘 30 · 부분 2) · 반입 `docs/reviews/codex_rint2_rr_round3_evidence_20261108/README_import.md` · 우리 트리 재현 = 판정값 차이 0 (`docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/README.md` — RR3-01 반례가 우리 핀 · 우리 Linux 에서도 같다).
- 상태 = ~~⬜ **1저자 비준 대기** · 결과 0 건 (이 계획은 코드 · 문서를 아직 하나도 바꾸지 않는다 · 반입 커밋 = 판정문 · 증거 · 원장 · 이 계획 · 진행 기록 한 줄).~~ → ✅ **1저자 11-08 *"권고대로"* = Q1–Q7 (가)** · 고침 = 작업 트리 커밋 하나 (RR3-01 구조 계약 · 시험 먼저 · RR3-02 요청서 제자리 정정 · §7 봉인 전 확인 목록 · §8 kgy S0 단계 1 채택 조건) · 실행 기록 = §9 · 증거 폴더 `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/` · 원장 (PC12-03 claimed_fixed 그대로 · RR3-01 · 02) = push 뒤 다음 커밋 (메인 세션) · 다음 = 짧은 사전 공격 → Codex 짧은 재확인 (Q7).
- 줄 번호 = 핀 `17d45fb9c` 의 `scripts/rint_r_chain.py` (sha256 48f0e7ff… · 핀 → 반입 바탕 `f5fb89792` 사이 이 파일 변경 없음).

## 0. 쉽게 말하면

- 회차 ③ 은 회차 ② 고침 (RR2-01–03 · PC6-05 · PC6-13) 과 사전 공격 9 · 10 · 11 · 12 고침 대부분을 **닫았다** (원장 verified 30).  새 치명 결함은 없다.
- 남은 큰 것 하나 (`RR3-01`, P2): 앞 런이 실제로는 팔 판독 (`read_run`) 에서 실패했는데, 실패 때 남겨 둔 파일 해시 목록 (`{file, index, sha256}`) 도 "비지 않은 목록" 이라 `prior_runs_problem` 이 그 런을 **끝난 런** 으로 읽는다 → 요약의 두 칸 (`stop.code` ARM_JSON_COUNT → TIME_LIMIT · `stop.run` L01_floor → L02_ceiling) 만 바꾸면 재개 자격 (resume_ok) 이 열리고 다음 `--resume` 원장 항목이 허용된다.  실제 재개 복사 (`ResumeRunner._copy`) 는 그 팔을 다시 읽어 같은 ARM_JSON_COUNT 로 거부한다 — 틀린 연구 값이 만들어지는 반례가 아니라 **원장 자격의 거짓 양성** 이다.
- 나머지 하나 (`RR3-02`, P3) = 회차 ③ 요청서의 한정표 · §5-3 세 문장이 PC12 고침 **전** 상태를 현재형으로 적었다 → 역사는 두고 표지 · 현재 범위 문장.
- 봉인 전 확인 (판정문 §5 ③ ④) 과 kgy S0 단계 1 채택 조건 (§6) 은 문서로 박아 둔다 (새 차단 결함으로 올리지 않는다).

## 1. RR3-01 — 무엇이 어디서

| 자리 | 줄 | 지금 |
|---|---|---|
| `Runner._execute` (생산) | 4966 · 4990–4997 | 성공 = `[{k: a[k] for k in ARM_PUBLIC}]` (`ARM_PUBLIC` 14 칸 · 2118–2120) · `read_run` 실패 = `arm_file_shas(outdir)` (`{file, index, sha256}`) 를 적고 Stop |
| `ResumeRunner._copy` (복사) | 5071 · 5073–5079 | 같은 두 꼴 |
| `MergeFetch.run` (합치기) | 6397 · 6407–6415 | 같은 두 꼴 |
| `arm_file_shas` | 2131–2141 | 파일 신원만 — docstring "계약 판정은 하지 않는다" |
| `prior_runs_problem` (자격 소비자) | 4157–4176 (반례 자리 4168–4175) | `run_record_shape == exit_ok` + `type(ar) is list and ar` → 끝난 런 |
| `stopped_record_problem` | 4068–4070 | 멈춘 런 기록 arms_read = [] 요구 (그대로) |
| `result_fields` → resume_ok | 4356–4359 | `stop_record_readable` → `stop_record_problem` → `prior_runs_problem` |
| `attempt_order_problem` | 3418–3424 | 결과 줄 resume_ok 로 다음 `--resume` 항목 허용 |
| arms_read 의 sha256 만 쓰는 자리 | 5238 `Replay.run` · 5521 `noop_check` · 6020 `load_ladders` · 6501 `MergeFetch.unused_runs` · 6979 `_verdict_compute` | 원 팔을 `want_sha` 로 다시 읽는다 (자격 판정 아님 · 이번 범위 밖 — 확인만) |
| `ResumeRunner._src_done` | 5034–5040 | 끝 기록 rc 성공 + 원 폴더 있음 → 복사 길 (복사가 다시 읽어 거부 = fail-closed) |

- 반례 (판정문 §2 · 우리 재현 같음): 실제 `Runner._execute` → 실제 `read_run` 실패 (ARM_JSON_COUNT · 합성 `p2_wrong_kit_a0.json`) → 생산 기록 `rc 0 · group_cause null · arms_read [{file, index, sha256}]` 그대로 + 요약 두 칸 편집 → `result_fields` cause check → timeout · resume_ok false → **true** · `stop_record_problem` None · 결과 줄 → `ledger_parse` resume_ok true · `attempt_order_problem(resume_of=1)` RESUME_NOT_ALLOWED → **None** · `result_line_problem` 재계산 대조 None / None · 실제 `_copy` = ARM_JSON_COUNT 거부.
- 판정문 최소 해결: 앞 런의 "검증을 마친 팔 기록" 과 "실패 때 보존한 파일 신원 목록" 을 생산 · 복사 · 합치기 · 자격 소비자가 **공유하는 계약** 으로 구분 — 성공 경로의 완성 `ARM_PUBLIC` 구조와 요청 팔 대응을 검사하거나, 명시적 판독 완료 상태를 생산 · 검증.  "비지 않은 목록" 조건만으로는 부족.  음성 = 위 실제 판독 실패 · 양성 = 성공 앞 런 · 복사된 성공 앞 런 · 원 PC12 반례 보존 · 수치 모형 · 등록 문턱 변경 불필요.

## 2. RR3-01 고침 안

- **(가) 구조 계약 하나** — 공용 함수 둘: 생성 = 성공 기록 (`ARM_PUBLIC` 투영) · 실패 기록 (`arm_file_shas`) 을 세 생산자 (`Runner._execute` · `ResumeRunner._copy` · `MergeFetch.run`) 가 같은 함수로 쓰고, 분류 = `arms_read` → `verified` (비지 않은 목록 · 원소마다 dict · 칸 집합 = `ARM_PUBLIC` 정확히 · index 차례 = 그 기록의 요청 팔 (`arm_indices(req)` · `request_fields_problem` 통과 뒤) · sha256 = 64 자리 소문자 hex · 파일 이름 끝 `_a<index>.json`) / `file_ids` (원소 칸 = `{file, index, sha256}` 정확히) / `empty` / `bad`.  `prior_runs_problem` = 앞 런 전부 `exit_ok` + `verified` 일 때만 끝난 런 (사유 글에 분류 이름).  요약 꼴 바뀜 없음 = 옛 정직 요약의 성공 기록은 그대로 읽힌다.
- (나) 명시 상태 칸 — 생산자가 `arms_state` (`read_ok` / `read_failed`) 를 적고 복사 · 합치기가 옮기며 `prior_runs_problem` 이 `read_ok` 를 요구 · 칸 없는 옛 요약 = 끝난 런 아님 (보수).  약점 = 칸 하나 편집 (`read_failed` → `read_ok`) 이 새 위조 면이 된다 (반례의 두 칸 + 한 칸 = 세 칸 · 구조 대조가 없으면 그대로 통과).
- (다) (가) + (나) — 상태 칸과 구조가 서로 맞아야 (불일치 = 모순).  요약 꼴 바뀜 · 고정물 전부 갱신 · 얻는 것 = 모든 사본을 일관되게 고친 위조 쪽 (판정문 §5 끝 = 새 요구 아님).
- 권고 = **(가)** — 생산자의 실패 기록 꼴 (칸 셋) 은 성공 꼴 (칸 14) 과 겹칠 수 없어 "실패 경로 기록 + 요약 몇 칸 편집" 부류가 구조로 막히고, 요약 꼴 · 원장 꼴을 바꾸지 않는다 · (나) 단독은 막을 부류를 새 한 칸에 옮길 뿐이다.
- 시험 먼저 (고치기 전 실패 확인 → 고침 → 통과):
  - 음성 N1 = 판정문 반례 그대로 상주화 (실제 `Runner._execute` + 모의 `run_in_group` · 실제 `read_run` 실패 · 요약 두 칸 편집) → resume_ok False · `stop_record_problem` 사유 있음 · 결과 줄 → `ledger_parse` → `attempt_order_problem(resume_of=1)` = RESUME_NOT_ALLOWED.  N1b · N1c = 같은 꼴을 `ResumeRunner._copy` · `MergeFetch.run` 실패 기록에서.  N1d = 실패 기록의 원소에 칸 몇 개만 더한 꼴 (`ARM_PUBLIC` 정확히가 아님) · index 차례가 요청 팔과 다른 성공 꼴 = 거부.
  - 양성 P1 = 정직한 성공 앞 런 + 정직 TIME_LIMIT (다음 런) = resume_ok True 그대로 · P2 = 복사된 성공 앞 런 (`_copy` 성공 기록) · P3 = 합치기 사본 성공 기록 (만들 수 있으면 · 아니면 한정에 적음).
  - 그대로 통과: PC12A–E (원 PC12 반례) · 결과 다시 셈 (`result_line_problem`) · 사슬 전체 · 끝-끝 · kgy 판 3.8 11 묶음 · 변이 (새 가드 하나 ↔ 검사 하나).
  - Codex 탐침 `docs/reviews/codex_rint2_rr_round3_evidence_20261108/pc12_attack/probe_pc12_independent.py` 무변경 재실행 = 고친 뒤에는 RR3-01 존재 assert 에서 **AssertionError 로 멈춰야 한다** (기대한 뒤집힘 · REPRODUCE.md "수정 후에는 같은 공격 입력의 거부를 새 oracle 로 명시 · 현 반례 존재 assert 를 조용히 PASS 로 바꾸지 않는다") — 거부 oracle 은 상주 N1 로 옮긴다 · 그 탐침을 고쳐 PASS 로 세지 않는다.
  - 웹앱 = 재실행 자격 · resume_ok · 원장 화면 없음 (회차 ③ 요청서 §4 끝 행 · grep 0) → "없음" 기록.

## 3. RR3-02 고침 안 (문서만 · 코드 0)

- 자리 = `docs/reviews/codex_rint2_rr_round3_request_20261108.md` (리뷰 핀 안 문서 · 핀 → 바탕 사이 변경 없음).

| 줄 | 지금 (현재형) | 현재 범위 (판정문 §2 RR3-02) |
|---|---|---|
| 83 (§4) | 런 기록 ↔ 그룹 끝 기록 교차 대조 없음 | 읽을 수 있는 사슬 쪽 끝 기록은 원인 · rc · 확인을 대조 (4072–4077 · 4133–4153 · PC12-02) · 남는 것 = 없는 / 결합되지 않은 끝 기록 · chain_end 없는 옛 recover 끝 기록 유예 |
| 84 (§4) | 디스크 signal_after 받음 | 요약 있는 길 = 거부 (PC12-02) · 요약 없는 길 (orphan) = 종전대로 받음 — 길을 나눠 적음 |
| 86 (§4) | code 의 STOPS 소속 안 봄 | 소속 검사 있음 (4410 · PC12-05) · 남는 것 = 발생 자리에서 생산 가능한 STOPS 부분집합까지 안 좁힘 |
| 94 (§4 ②) · 140 (§5-3 F3) | 앞 런 = exit_ok + arms_read 비지 않음 → 끝난 런 | RR3-01 로 축소 — 판독 실패 때 남긴 파일 신원 목록도 비지 않은 목록이라 충분조건 아님 |
| 154 (Q4) | 한정 (§4 · PC11-05–08 · 교차 대조 없음) | "교차 대조 없음" → 83 줄과 같은 범위로 좁힘 |

- (가) 제자리 정정 — 원문은 취소선으로 남기고 바로 뒤에 "→ 11-08 정정 (RR3-02 · 판정문 §2): <현재 범위>" (회차 ② RR2-02 · PC9-06 의 처리와 같은 꼴) · 끝에 판정문 §2 의 `rg` 한 줄로 걸린 줄마다 표지가 붙었는지 확인.
- (나) 따로 정오표 파일 (요청서는 그대로).
- 권고 = **(가)** — 요청서가 현재 남은 경계를 읽는 자리라 같은 자리에 표지가 있어야 다시 잘못 읽지 않는다 · 역사 글은 취소선으로 보존.
- 판정문 §2: 이 P3 만으로 실행 차단을 더하지 않는다 · 단 문서 전체 종결을 주장하기 전 정정 필요.

## 4. 봉인 전 확인 목록 (판정문 §5 · 하위 보고 보조 관측)

1. RR3-01 보완 (§2) — 앞 런 판독 실패를 timeout 으로 바꿔도 재개 자격 · 다음 원장 항목이 열리지 않음 · 성공 · 복사 성공 양성 · 원 PC12 반례 · 결과 다시 셈 길 함께 확인.
2. RR3-02 정정 (§3).
3. 선언된 PC11-05–08 · PC12 한정은 자동으로 새 차단 결함이 아니다 — 단 봉인할 **실제** 계획 · 시도 기록에서 확인: 요청 칸 (arms · arm_list) 있음 · 런 이름 유일 · 실제 순서 = 계획 순서 · launch / end 결합 · 필요한 chain_end 있음 · 복사 출처 (copied_from) 맞음 · 지수 넘침 수 (1e400 꼴) 없음 · 그 자리에서 생산 가능한 멈춤 이름만 · utc 꼴.  결손을 구형 예외로 흡수하고 일반 정책 GO 를 주장하지 않는다.
4. 그대로 남는 조건 — 현장 자격 (프로세스 · 잠금 · 권한 · 파일 시스템 · FIFO · NFS) · 원인 미확정 최초 실패 기록 · 검토 핀 → 봉인 핀 diff · 의존 지문 (합성 PASS 로 대신하지 않음).
5. 보조 관측 (하위 보고 · 결함 아님 · 한정에 적음) — 그룹 기록 판독 (3738 `_read_group_json`) 은 일반 `json.loads` · PC12-04 엄격 JSON = 단계 요약 한정.

## 5. kgy S0 단계 1 재실행 채택 조건 (판정문 §6 · SELF-155 닫는 확인)

- 지금 문서 (`docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md` 98 줄) = "rc 0 + 여섯 파일 (`s0_stage1_kit_SBE_vgcf100.json` · `s0_junctions_*.npz` · `s0_instances_*.npz` · `cjunc_plan.json` · `cjunc_plan.sha256` · `payload_capture_*.log`) 있음" → 필요한 완료 점검이지 채택 충분조건 전체가 아님.  더할 것:
  1. rc = S0 **Python 자식** 의 rc — `docs/reviews/rint2_s0_mem_fix_20261106/tools/run2.sh` 15 줄 (`wait $PID; echo "rc=$?" >> rss.log`) 의 rss.log 값 · 감시 셸의 `$?` (= echo 성공 0) 를 읽지 않는다 · 신호 · 메모리 중단 없음.
  2. 여섯 산출물을 실제로 읽음 — JSON 의 stage · kit · code · input · NPZ 두 개의 실제 배열 · 계획 정준 바이트 SHA = `cjunc_plan.sha256` = 보고 plan.sha256 · payload 로그 신원 → 같은 실행에 결속 · 부분 / 실패 출력 = 성공 자료로 채택 안 함.
  3. 새 빈 폴더 · SBE 한 침대 · stage 1 · σ 비열람 · 원 입력 무쓰기 · 실패 보존 (`ca_s0_census.py` 1727–1742 = stage1 한 킷 · 출력 혼합 금지 검사).
  4. 고정 환경 · 코드 지문 · 새 핀 · 종료 / 신호 · 시간 · RSS 보존 — 5 초 간격 최대 = **"표본 최대 RSS"** (실제 peak 라고 부르려면 고수위 자료).
  5. 두 예외의 실침대 영향 = 미확인 문구 유지 · 단계1 → s_min → ⑥ → 기하 · 반복 수 → 숫자 · 실행 정책 → 새 계획 / 핀 봉인 → 단계2 → 등록 R 진입 판단 순서 그대로 · 판정문 답 = kgy 실행 승인 · 실측 성공 인증 아님.
- 사실 (핀): S0 코드 지문 묶음 `S0_SAME_FILES` (`scripts/rint_r_chain.py` 316–317) = ca_s0_census · carbon_junction · ptfe_face_alpha · step3_sigma · mpm_webapp_payload · fibre_segment_raster · sr01_stamp_compare — `rint_r_chain.py` 는 없다 ⇒ RR3-01 고침 (`rint_r_chain.py` · 그 시험) 은 S0 단계 1 결과의 코드 지문을 바꾸지 않는다 (같은 핀 위 재실행이면).

## 6. 결정 질문 (~~⬜ 1저자~~ → ✅ 1저자 11-08 *"권고대로"* = Q1–Q7 (가))

**Q1 — RR3-01 고침 방식** (§2)
- (가) 구조 계약 하나 (`ARM_PUBLIC` 정확한 칸 + 요청 팔 대응 · 공용 생성 · 분류 함수) / (나) 명시 상태 칸 / (다) 둘 다.
- 권고 = **(가)** — 요약 꼴을 안 바꾸고 실패 경로 기록 + 몇 칸 편집 부류를 구조로 막는다 · (나) 는 위조 면을 새 칸 하나로 옮길 뿐.

**Q2 — 공용 계약을 쓰는 자리**
- (가) 생산 셋 (`Runner._execute` · `ResumeRunner._copy` · `MergeFetch.run`) = 같은 생성 함수 · 자격 소비자 `prior_runs_problem` = 분류 함수 · `_src_done` · `_copy` 재판독 · `want_sha` 소비자 다섯 = 그대로 (이미 다시 읽어 거부).
- (나) (가) + `_src_done` 도 요약의 분류를 보게 (복사 대신 재실행 · 동작 바뀜).
- 권고 = **(가)** — 판정문 최소 해결 범위이고 실제 복사 길은 이미 fail-closed (판정문 §2 · 우리 재현 같음).

**Q3 — PC12-03 원장 상태**
- (가) claimed_fixed 그대로 + RR3-01 고침 · 재확인과 함께 닫음 (회차 ② 반입 관례 = PC6-13 ↔ RR2-01 · 이 반입 커밋이 그렇게 적음).
- (나) open 으로 재개방.
- 권고 = **(가)** — 원 F3 반례 (rc 실패 · 빈 목록) 는 닫혔고 남은 부류는 RR3-01 이 따로 추적한다 · (나) 를 고르면 상태 칸 하나만 바꾼다.

**Q4 — RR3-02 정정 방식** (§3)
- (가) 요청서 제자리 취소선 + "11-08 정정 (RR3-02)" 현재 범위 문장 (83 · 84 · 86 · 94 · 140 · 154 줄) / (나) 따로 정오표.
- 권고 = **(가)** — 읽는 자리에 표지 · 역사 보존 (RR2-02 와 같은 처리).

**Q5 — 봉인 전 확인 목록** (§4)
- (가) 봉인 체크리스트로 등록 (새 차단 결함 격상 없이 · 봉인 때 실제 계획 · 시도 기록을 대조 · 결과 = 봉인 기록에) / (나) PC11-05–08 을 지금 고침.
- 권고 = **(가)** — 판정문 §5 ③ 그대로 · 생산자는 그 꼴을 쓰지 않으므로 실제 기록 대조로 충분.

**Q6 — kgy S0 단계 1 채택 조건** (§5)
- (가) 다섯 조건 채택 · RSS 는 "표본 최대 RSS" 로 적음 · 명령 그대로.
- (나) (가) + 자식 고수위 RSS (`/proc/<pid>/status` VmHWM 또는 GNU time 최대 RSS) 를 감시 셸에 더해 "peak" 라고 씀 (명령 바뀜 · kgy 에 그 도구가 있는지 미확인).
- 권고 = **(가)** — 판정문이 둘 다 허용 · 명령을 바꾸지 않고 SELF-155 의 메모리 개선 확인 (표본 최대 RSS · 시간 · rc · 완성 산출물) 은 선다.

**Q7 — 다음 순서**
- (가) Q1–Q4 고침 (시험 먼저 · 커밋 하나씩) → 짧은 사전 공격 (바뀐 함수 · 같은 부류 · 보장마다 작은 반례) → Codex 짧은 재확인 (RR3-01 · RR3-02 · PC12-03 만) → 판정문 §7 순서 · kgy S0 단계 1 재실행 = 병행 가능 (§5 사실 · 1저자 명령 시점).
- (나) 고침 · 재확인을 S0 단계 1 결과 뒤로.
- 권고 = **(가)** — RR3-01 은 재개 정책 · S0 단계 1 은 census 도구라 코드 지문이 겹치지 않는다.
- → 11-08 실행: 작업 트리 커밋 **하나** (RR3-01 시험 · 고침 · RR3-02 · §7 · §8 · 증거 — 메인 세션 지시 · 반입 · push · 게이트 = 메인) · 시험 먼저 = 새 시험을 고치기 전 판에서 실패로 확인한 뒤 고침 (§9-2).

## 7. 봉인 전 확인 목록 (Q5 (가) · 판정문 §5 · 새 차단 결함 아님 · 결과 = 봉인 기록)

| # | 확인 | 어디서 · 무엇으로 | 상태 |
|---|---|---|---|
| ① | RR3-01 보완 — 앞 런 판독 실패를 timeout 으로 바꿔도 재개 자격 · 다음 원장 항목이 열리지 않음 · 성공 · 복사 성공 양성 · 원 PC12 반례 · 결과 다시 셈 길 함께 | 상주 시험 RR3A–E · RR3P · PC12A–E (`scripts/test_rint_r_chain.py`) · 실행 기록 §9 | ✅ 고침 (11-08) · ⬜ Codex 짧은 재확인 |
| ② | RR3-02 현행 한정표 정정 | 요청서 `docs/reviews/codex_rint2_rr_round3_request_20261108.md` 83 · 84 · 86 · 94 · 135 · 140 · 154 줄 = 취소선 + "11-08 정정 (RR3-02)" · 판정문 §2 의 rg 한 줄에 걸린 줄마다 표지 | ✅ (11-08) · ⬜ Codex 짧은 재확인 |
| ③ | 선언된 PC11-05–08 · PC12 한정 = 봉인할 **실제** 계획 · 시도 기록이 그 미검증 영역을 쓰지 않는가 — 요청 칸 (arms · arm_list) 있음 · 런 이름 유일 · 실제 순서 = 계획 순서 · launch / end 결합 · 필요한 chain_end 있음 · 복사 출처 (copied_from) 맞음 · 지수 넘침 수 (1e400 꼴) 없음 · 그 자리에서 생산 가능한 멈춤 이름만 · utc 꼴 | 봉인 때 실제 기록 대조 (명령 · 결과 = 봉인 기록) · 결손을 구형 예외로 흡수 금지 · 일반 정책 GO 주장 안 함 | ⬜ 봉인 때 |
| ④ | 그대로 남는 조건 — 현장 자격 (프로세스 · 잠금 · 권한 · 파일 시스템 · FIFO · NFS) · 원인 미확정 최초 실패 기록 · 검토 핀 → 봉인 핀 diff · 의존 지문 (합성 PASS 로 대신하지 않음) · RR3-01 고침으로 `rint_r_chain.py` 가 바뀜 = R 계획 code key (`CODE_FILES`) 바뀜 → 봉인 = 새 핀 | 판정문 §5 ④ · §7 | ⬜ 봉인 때 |
| ⑤ | 보조 관측 (하위 보고 · 결함 아님) — 그룹 기록 판독 (`_read_group_json`) = 일반 json.loads · PC12-04 엄격 JSON = 단계 요약 한정 | 한정 문구 (요청서 · 봉인 기록) | 한정 |

## 8. kgy S0 단계 1 재실행 채택 조건 (Q6 (가) · 확정 · 명령 그대로)

- 채택 = 아래 다섯이 모두 ✓ 일 때만 · 하나라도 ✗ · 미확인 = 성공 자료로 채택 안 함 (실패 보존 · 기록) · §5 의 다섯을 그대로 확정한 것.
  1. ⬜ rc = S0 **Python 자식** 의 rc — `docs/reviews/rint2_s0_mem_fix_20261106/tools/run2.sh` 15 줄 (`wait $PID; echo "rc=$?"`) 이 rss.log 에 적은 `rc=` 값 = 0 · 감시 셸의 `$?` (echo 성공 = 0) 는 읽지 않는다 · rss.log 에 `CAP_TERM` 줄 없음 (같은 파일 12 줄 = 상한에서 USR1 · TERM) · 신호 · 메모리 중단 없음.
  2. ⬜ 여섯 산출물을 실제로 읽고 같은 실행에 결속 — `s0_stage1_kit_SBE_vgcf100.json` 의 stage · kit · code · input 칸 · `s0_junctions_*.npz` · `s0_instances_*.npz` 의 실제 배열 (연다) · `cjunc_plan.json` 정준 바이트 SHA = `cjunc_plan.sha256` 의 값 = 보고 plan.sha256 · `payload_capture_*.log` 신원 → 같은 실행 · 부분 / 실패 출력 = 성공 자료로 채택 안 함 (있음 = 필요조건일 뿐).
  3. ⬜ 새 빈 폴더 · SBE 한 침대 · stage 1 · σ 비열람 · 원 입력 무쓰기 · 실패 보존.
  4. ⬜ 고정 환경 · 코드 지문 · 새 핀 · 종료 / 신호 · 시간 · RSS 보존 — 5 초 간격 최대 = **"표본 최대 RSS"** (실제 peak 라고 부르지 않는다 · 고수위 자료 없음 · Q6 (가) = VmHWM · GNU time 안 붙임).
  5. ⬜ 두 예외 (정준 동률 순서 · 옛 판이 놓친 경계 참 쌍) 의 실침대 영향 = 미확인 문구 유지 · 순서 그대로 (단계 1 → s_min → ⑥ → 기하 · 반복 수 → 숫자 · 실행 정책 → 새 계획 / 핀 봉인 → 단계 2 → 등록 R 진입 판단) · 이 조건 = kgy 실행 승인 · 실측 성공 인증 아님 (판정문 §6).
- 명령 바뀜 없음 (`docs/reviews/rint2_kgy_commands_20261020.md` · run2.sh 그대로) · S0 코드 지문 묶음 `S0_SAME_FILES` 에 `rint_r_chain.py` 없음 → RR3-01 고침은 S0 단계 1 결과의 코드 지문을 바꾸지 않는다 (같은 핀 위 재실행이면 · §5 끝 사실 그대로) · 옛 채택 문장 (S0 REPORT §12 = rc 0 + 여섯 파일 있음) 은 이 §8 의 필요조건 일부.

## 9. 실행 기록 (11-08 · 작업 트리 에이전트 · 시험 먼저 · 증거 폴더 `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/`)

- 바탕 `40d9658c0` · 바뀐 코드 두 파일 sha256 (바탕 → 이 커밋 · `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/logs/code_sha256.txt`) = `scripts/rint_r_chain.py` 48f0e7ff… → b37ef7c6… · `scripts/test_rint_r_chain.py` fedba635… → d83539a1… · 깨끗한 바탕 + `apply_chain.py` · `apply_tests.py` (같은 폴더) = 이 바이트 그대로 · 시험 · 변이 · 탐침 다시 = 이 바이트 · push · 게이트 (`scripts/check_all.sh`) · 원장 = 메인 세션 · **웹앱 화면 없음** (`webapp/` 에 resume_ok · RESUME_NOT_ALLOWED · arms_read · prior_runs_problem · rint_r_chain · "재실행 자격" = 0 건).
- ⚠ 증거 폴더의 REPORT.md = 만들지 않았다 (작업 트리 에이전트의 보고 파일 쓰기가 막혔다 · 이 §9 + 폴더의 로그 · 스크립트 · SHA256SUMS 가 그 자리).
- 환경 = Linux 6.18 · Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · kgy 판 = uv CPython 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 4 코어 · 합성 폴더 · 가짜 러너 · 모의 `run_in_group` (러너 반환 · 출력만) · 실제 git 원장 · 이 컨테이너 (kgy 3.8.10 · ibb · GPU · 실제 SIGKILL · flock · NFS 아님).

### 9-1. 바꾼 것 (줄 = 고친 판 `scripts/rint_r_chain.py`)

| 자리 | 줄 | 무엇 |
|---|---|---|
| 머리말 ★ 11-08 RR3-01 문단 | 176–181 | 구조 계약 요약 (CT08 = 이름 붙인 함수 · 상수가 모듈에 있음) |
| `ARM_FILE_ID_KEYS` · `ARM_SHA256_RE` (새) | 2151–2152 | 판독 실패 파일 신원 칸 셋 · sha256 꼴 (64 자리 소문자 hex) |
| `arms_read_record` (새 · 생성) | 2155–2162 | arms_ 있음 = 팔마다 ARM_PUBLIC 칸 (옛 세 자리 안쪽 식 그대로) · 없음 = `arm_file_shas(outdir)` (그대로) |
| `arm_file_prefix` (새) | 2165–2167 | `read_run` 의 킷 대조와 같은 식 `p2_<kit[4:]>_` (read_run 자리 글은 그대로) |
| `arms_read_kind` (새 · 분류) | 2170–2205 | verified (ARM_PUBLIC 칸 정확히 + 그 기록 요청 칸 (`request_fields_problem` 통과) 의 요청 팔 (`arm_indices`) 과 일대일 = 수 · 차례대로 번호 (정수 · bool 아님) · 파일 = 이름만 · 킷 앞자리 · 끝 _a<번호>.json · sha256 꼴) · file_ids (칸 정확히 {file, index, sha256}) · empty · bad (사유 글) |
| `prior_runs_problem` | 4221–4246 (몸 4240–4245) | "arms_read 비지 않은 목록" → `arms_read_kind(...) == 'verified'` · 사유 글 = 분류 이름 + 까닭 · 독스트링 ★ 11-08 RR3-01 |
| `Runner._execute` · `ResumeRunner._copy` · `MergeFetch.run` | 5066 · 5068 · 5148 · 5150 · 6481 · 6486 | 실패 = `arms_read_record(outdir=outdir)` · 성공 = `arms_read_record(arms_)` (값 그대로) |

- 바뀌지 않은 것 (Q2 (가)): `_src_done` (5105 · 글 그대로) · `_copy` 의 `read_run` 다시 읽기 · want_sha 소비자 다섯 (`Replay.run` · `noop_check` · `load_ladders` · `MergeFetch.unused_runs` · `_verdict_compute`) · `stopped_record_problem` ③ · `read_run` · `arm_file_shas` · 요약 · 원장 꼴.

### 9-2. 수 (고치기 전 → 뒤 · 로그 = 증거 폴더 `logs/`)

| 묶음 | 고치기 전 | 고친 뒤 |
|---|---|---|
| 새 시험 + 고정물 바꾼 둘 (`--only RR3,CT06,PC12C` · 끝 시험 파일) | **3/8 PASS** (`before_RR3.log` · 사슬 = 바탕 · 깨끗한 사본 트리) — 실패 RR3A (9 행 중 6) · RR3B (6 중 4) · RR3C (48 중 48 = 분류 함수 없음 · 행동 = 음성 34 중 33 이 자격 True · n_pub_tuple 만 옛 목록 검사로 False) · RR3D (6 중 6) · RR3E (2 중 1 = 실제 git 원장 resume rc 0) · 통과 = CT06 · PC12C · RR3P (양성 대조) · 행 = `before_RR3_rows.json` · `before_RR3_summary.txt` | **8/8 PASS** (`after_RR3.log` · 행 `after_RR3_rows.json` · `after_RR3_summary.txt`) |
| 겨냥 (`--only RR3,CT06,PC12,CT08,RC01`) | — | **15/15 PASS** (`after_RR3_targeted.log` · PC12 · PC12A–E · RC01 rc 스캐너 · CT08 머리말 이름) |
| 사슬 `scripts/test_rint_r_chain.py` (3.11) | 481/481 PASS (364.3 s · `before_chain_full_py311.log` · 바탕 트리) | **487/487 PASS** (465.7 s · `after_chain_full_py311.log` · 이 바이트 · 0 FAIL) |
| 옛 시험 파일 (바탕) × 고친 사슬 (기대 바뀜 확인) | — | **479/481 PASS** (512.4 s · `cross_oldtests_fixedchain.log` · 사본 트리 = 바탕 시험 파일 + 고친 사슬 b37ef7c6…) — 실패 = CT06 · PC12C 둘뿐 = §9-3 기대 바뀜 그대로 · 행 (`cross_oldtests_fixedchain_rows.json` · `.out`) = CT06 c_prev_record · PC12C cli_honest_tl_after_ok · gu_after_ok · rr_after_copied · rr_signal_after_ok · tl_none_after_ok · 사유 = file_ids (CLI 행 cli_honest_tl_after_ok = 실제 원장 [recover 0, 자격 True, resume 0, 거부 False] → [0, False, 3, True]) |
| 끝-끝 `scripts/test_rint_r_chain_e2e.py` (3.11) | 51 PASS · 0 FAIL (807.4 s · `before_e2e_py311.log` · 바탕 트리) | **51 PASS · 0 FAIL** (881.3 s · `after_e2e_py311.log` · 이 바이트) |
| kgy 판 3.8 (`scripts/check_kgy_py38.sh`) | — | **11 묶음 통과** (rc 0 · `check_kgy_py38.out` · `logs/py38/` · Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · rint_r_chain 487/487 (627.1 s) · 끝-끝 51 PASS · 0 FAIL (624.2 s) · 그 밖 9 = run_contract 124/124 · step3_rint PASS · ptfe_face_alpha 242/0 · carbon_junction 547/547 · ca_ext_b6 502/0 · ca_ext_runner 151/0 · step3_target_cert 264/264 · step3_conv_cert 29/29 · ca_s0_census 186/0) |
| 변이 (§9-4) | — | **23/23 잡힘** · 무변이 9/9 PASS · 되돌림 sha256 = 시작 (`mutation_rr3.json` · `mutation_rr3.out` · 사슬 b37ef7c6…) |
| RR3-02 rg 확인 (`rr3_02_check.py`) | rg 걸린 줄 83 · 84 · 86 · 94 · 135 · 154 (표지 0) | 같은 6 줄 전부 표지 · 계획 목록 6 줄 다 · 바뀐 줄 = 표지 줄 7 개뿐 (`rr3_02_rg_check.log` · OK) |

새 검사 (`scripts/test_rint_r_chain.py` · ★ 11-08 RR3-01 블록 · 실행 줄 앞):

| 검사 | 무엇 | 고치기 전 → 뒤 |
|---|---|---|
| RR3A | 판정문 반례 그대로 (실제 `Runner._execute` + 모의 `run_in_group` · 실제 `read_run` ARM_JSON_COUNT) · 원 기록 · 편집 L02_ceiling · zzz · 위조 L02 {timeout · null} TIME_LIMIT · {None · 0} GU (+ 그 로그) · 결과 줄 → 원장 읽기 → `attempt_order_problem(resume_of=1)` · 다시 셈 | 편집 넷 = 자격 True · 사유 없음 · 원장 None → 자격 False · 사유 (file_ids) · RESUME_NOT_ALLOWED · 원 기록 check · False · 다시 셈 None / None 그대로 |
| RR3B | ⓐ `ResumeRunner._copy` 판독 실패 기록 (`_src_done` True · 복사 다시 읽기 ARM_JSON_COUNT · copied_from 1) + 두 칸 ⓑ `MergeFetch.run` 판독 실패 기록을 앞 런으로 ⓒ 합치기 성공 기록을 앞 런으로 (양성) | ⓐ ⓑ 자격 True → False · ⓒ True 그대로 |
| RR3C | 앞 런 변이 47 (정직 7 · 파일 신원 꼴 4 · 칸 집합 7 · 요청 칸 · kit 5 · 일대일 9 · 파일 4 · sha256 5 · 대조 6) + 고정물 칸 = 사슬 ARM_PUBLIC | 음성 34 중 자격 True 33 → 0 · 정직 7 · 대조 6 그대로 |
| RR3D | 원천 구조 (arm_file_shas 부르는 함수 = `arms_read_record` 하나 · ARM_PUBLIC 투영 = 그 하나 · 생산자 셋 = 두 번씩 · `arms_read_kind` 소비자 = `prior_runs_problem` 하나) · 실제 생산자 기록 분류 (RR3P 사다리 = verified · verified · RR3A = file_ids) | 함수 없음 → 전부 맞음 |
| RR3E | 실제 git 원장 (recover → 결과 줄 → --add --resume 1) · 앞 런 = 판독 실패 파일 신원 (판정문 반례 기록) / 판독 완료 꼴 | 파일 신원 [recover 0, 자격 True, resume 0, 거부 아님] → [0, False, 3, RESUME_NOT_ALLOWED] · 판독 완료 [0, True, 0] 그대로 |
| RR3P | 실제 사슬 (가짜 러너): 시도 1 = 천장 OOM · --resume 1 · 시도 2 = 바닥 복사 (copied_from 1) 뒤 천장 OOM → 결과 줄 1 · 2 = resource · 자격 True · 앞 런 칸 = ARM_PUBLIC | 고치기 전 · 뒤 같음 (양성) |

### 9-3. 기대 바뀜 (고정물 · 뜻 그대로)

- 옛 정직 고정물 `CT06_ARM` = 칸 셋 {file, index, sha256} = 생산자의 **판독 실패** 꼴 (`arm_file_shas`) — 생산자는 성공에 그 꼴을 쓰지 않는다 → 정직한 앞 런 고정물 = 생산자 성공 꼴 `ct06_pub` · `CT06_PUB` (ARM_PUBLIC 14 칸 + 요청 칸 arms · arm_list · kit).  멈춘 런 기록에 팔 읽음을 넣은 행 (CT06 f_*_arms · CT06_ARMS) 은 그대로.
- 옛 시험 파일 × 고친 사슬 = 바뀐 행 = CT06 c_prev_record (timeout · True → False) · PC12C tl_none_after_ok · gu_after_ok · rr_signal_after_ok · rr_after_copied (True → False) · cli_honest_tl_after_ok (실제 원장 [0, True, 0, False] → [0, False, 3, True]) — 전부 앞 런 고정물이 CT06_ARM 이던 행 · 사유 = file_ids · 그 밖 행 · 검사 그대로 · PC12C rr_after_prior_no_gc (group_cause 칸 없음 = False 그대로) 도 CT06_PUB 로 바꿔 결함을 group_cause 하나로 남김.

### 9-4. 변이 · Codex 탐침 다시

- 변이 (`mutate_rr3.py` · 리포 밖 사본 트리 = 깨끗한 `40d9658c0` + 두 apply 스크립트 · 한 번에 하나 · 매번 원 바이트로 되돌림 · `--only RR3,CT06,PC12C,RS01`): M01 `prior_runs_problem` = 옛 규칙 → RR3A · B · C · E · M02 파일 신원 = verified → RR3A–E · M03–M19 분류 조건 하나씩 (칸 집합 · 원소 객체 · 목록 · 빈 갈래 · 요청 칸 · 요청 범위 · kit 글 · 팔 수 · 번호 정수 · 번호 = 요청 팔 · 파일 글 · 이름만 · 킷 앞자리 · 끝 _a<번호>.json · sha256 없앰 · fullmatch → match · sha256 글) → RR3C · M20 생성 성공 = 파일 신원 칸만 → RR3B · D · P (+ RS01) · M21 생성 실패 = [] → RR3A · B · D · M22 · M23 생산자 우회 → RR3D (`docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/logs/mutation_rr3.json`).
- Codex 탐침 (`pc12_attack/probe_pc12_independent.py` · 반입 원본 바이트 sha256 7f335c75… · 리포 밖 스크래치 · `python3 -I -B -X utf8` · `RINT_REVIEW_REPO` = 이 작업 트리 · 결과 `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/probe_rerun/`): ① 원본 그대로 = rc 1 · AssertionError at 144 `assert ledger_rows[1]['attempt_order_problem'] is None` (RR3-01 존재 assert · 기대한 뒤집힘 · PASS 로 바꾸지 않음) ② 그 assert 두 줄 (144 · 163) 만 거부 oracle 로 바꾼 사본 (차이 = 같은 폴더 oracle.diff) = rc 0 · 편집 뒤 timeout · resume_ok **False** · stop_record_problem 사유 · 원장 다음 항목 original · edited 둘 다 **RESUME_NOT_ALLOWED** · result_line_problem None / None · `_src_done` True · 복사 다시 읽기 ARM_JSON_COUNT · results.json ↔ 우리 고치기 전 재현 = 잎 159 → 160 · 다른 잎 10 = 사슬 sha256 1 · 결과 줄 utc 2 · RR3-01 뒤집힘 7 · 그 밖 (요청 255 / 21 · 끝 기록 175 행 (같음) · 엄격 요약 · 거부 이름 · PC11 · 옆 이름 흔적 · 머리말 이름) 같음 (`docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/probe_rerun/leaf_diff.json` · `docs/reviews/rint2_rr2_fix_evidence_20261105/rr3_fix/probe_rerun/rerun_report.json`).

### 9-5. 생산자 꼴 표 (고친 판)

| 생산자 | 길 | arms_read (`arms_read_record`) | `arms_read_kind` | 앞 런 자격 |
|---|---|---|---|---|
| `Runner._execute` | `read_run` 성공 / 실패 (Stop) | 팔마다 ARM_PUBLIC 14 칸 · 요청 팔 차례 (5068) / 파일 신원 = 디스크 p2_*_a<번호>.json (5066 · 없으면 []) | verified / file_ids (empty) | 끝난 런 / 아님 (그 런에서 멈춤) |
| 〃 | 팔 읽기 전 멈춤 (시간 · rc · 신호 · 미확인) | [] | empty | 아님 |
| `ResumeRunner._copy` | 복사 다시 읽기 성공 / 실패 | ARM_PUBLIC (5150) / 파일 신원 (5148) · copied_from | verified / file_ids | 끝난 런 / 아님 |
| `MergeFetch.run` | 사본 다시 읽기 성공 / 실패 | ARM_PUBLIC (6486) / 파일 신원 (6481) · source | verified / file_ids | 끝난 런 / 아님 |

- 두 꼴의 칸 집합 = 14 대 3 (겹치지 않음) → 실패 기록 + 요약 몇 칸 편집은 구조로 갈린다 · 판독 완료 꼴 = 그 기록의 요청 칸 (arms · arm_list · kit) 과 일대일 (요청 칸 없음 = 요청 팔 모름 = bad).

### 9-6. 한정 (닫지 않은 것)

- 구조 계약은 **값** 을 대조하지 않는다 — sha256 ↔ 디스크 파일 · 다른 런에서 옮겨 붙인 판독 완료 기록 · 모든 사본을 일관되게 고친 위조 = 이 계약 밖 (판정문 §5 끝 = 새 요구 아님 · 실제 재개 복사는 원 팔을 다시 읽어 거부).
- 관찰 (시험으로 확인 안 함): 앞 런이 모두 판독 완료인 뒤의 단계 차원 검사 멈춤 (값 판정) 을 런 전 TIME_LIMIT (다음 이름) 로 바꾼 두 칸 편집 = 정직한 런 전 TIME_LIMIT 와 기록 꼴이 같아 이 구조 계약으로 못 가른다 (시간 회계 대조 등 = 범위 밖 · 짧은 사전 공격에서 볼 것).
- 파일 이름 = `_a<번호>.json` 글자 그대로 (read_run 은 `_a(\d+)\.json` + int 라 a00 · 유니코드 숫자도 받는다 · 실제 러너 = `_a${i}` ASCII) → 그런 이름의 정직 기록 · ARM_PUBLIC 칸 집합이 지금과 다른 옛 판 요약 · 요청 칸 (arms · kit) 없는 기록 = verified 아님 = 재실행 자격 없음 (보수 쪽).  ARM_PUBLIC 의 그 밖 칸 (state · cert_pass · cg_* …) 값 꼴은 안 본다.
- RR3-02: §3 표의 74 줄 (요청서 §3 PC12-03 행 "exit_ok + arms_read 비지 않음") = `d346ca943` 이 한 일의 서술 (역사) · rg 에 안 걸림 · 계획 목록 밖 → 손대지 않음 · 135 줄 = rg 에 걸린 인용 (고치기 전 한정 글) → 취소선 없이 표지만.
- 이 고침에 대한 독립 재공격 = 없음 (다음 = 짧은 사전 공격 → Codex 짧은 재확인 · Q7) · `rint_r_chain.py` sha 바뀜 → R 계획 code key (`CODE_FILES`) 바뀜 = §7 ④.
