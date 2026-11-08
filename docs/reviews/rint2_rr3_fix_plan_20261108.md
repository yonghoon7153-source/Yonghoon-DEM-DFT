# Rint ② 회차 ③ (11-08) 뒤 수정 계획 — RR3-01 · RR3-02 · 봉인 전 확인 · kgy S0 단계 1 채택 조건

- 근거 = Codex 판정문 `docs/reviews/codex_review_rint2_rr_round3_20261108.md` (리뷰 핀 `17d45fb9c` · 판정 **HOLD** · 새 P1 0 · P2 1 · P3 1 · 닫힘 30 · 부분 2) · 반입 `docs/reviews/codex_rint2_rr_round3_evidence_20261108/README_import.md` · 우리 트리 재현 = 판정값 차이 0 (`docs/reviews/codex_rint2_rr_round3_evidence_20261108/_repro_ours_20261108/README.md` — RR3-01 반례가 우리 핀 · 우리 Linux 에서도 같다).
- 상태 = ⬜ **1저자 비준 대기** · 결과 0 건 (이 계획은 코드 · 문서를 아직 하나도 바꾸지 않는다 · 반입 커밋 = 판정문 · 증거 · 원장 · 이 계획 · 진행 기록 한 줄).
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

## 6. 결정 질문 (⬜ 1저자)

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
