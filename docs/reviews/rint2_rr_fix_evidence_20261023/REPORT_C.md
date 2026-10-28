# Rint ② RR 묶음 C 코드 보고 (C1 재시도 봉인 · C2 예측 12 단위) — 에이전트 원 보고 · 10-27

- 무엇: 1저자 10-27 *"Rint는 권고대로 해도돼"* (11 월 전체 · 범위 그대로 · 시험 깊이) 로 띄운 코드 에이전트의 마지막 보고 원문.  지시서 = `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF_C_code.md` · 문서 쪽 (C3) = `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF_C_docs.md` · 메인 반입 `e743d50c9`..`3c108bba9` (10-27).
- 반입: 메인 가지 `2c1308bb2`..`db97d0644` 15 커밋 (`cherry-pick -x` · 충돌 0 · 10-28).  이 문서의 커밋 번호는 전부 **메인 번호로 바꿔 적었다** (원 보고의 에이전트 가지 번호 15 개 → 메인 번호 · 원장 `SELF-116` · 에이전트 번호는 각 커밋 메시지의 `cherry picked from commit` 줄에 있다).  리포 밖 경로 셋 (작업 트리 · /tmp 폴더 · 스크래치) 은 설명으로 바꿨다.  그 밖의 글자 = 원 보고 그대로.
- 숫자 = 에이전트 실행 출력 (메인은 게이트에서 같은 시험을 다시 돌린다 — 결과는 진행 기록 · 원장 `RCA2-05` evidence).
- §11 의 결정 25 = 1저자 (보고 때 묶어서 묻는다) · §10 이름 표 → 등록 R · Q9 §7 개정 = 결정 뒤.
- → §11 결정 = 1저자 10-28 *"Rint 권고대로"* (적용 = Q9 개정 6 · 등록 R 10-28 블록)

---

묶음 C 코드 작업을 끝냈습니다. 가지 `rr-fix-c`, 커밋 15 개, 작업 트리는 깨끗합니다. 끝 트리에서 Python 3.11 회귀 21 묶음이 모두 rc 0 이고, kgy 판 (3.8.20) 은 2 회차에서 11/11 통과했습니다. 1 회차의 e2e 실패 둘은 제 시험 도구 결함이었고, 생산 코드 결함은 아닙니다 (§5).

| 항목 | 내용 |
|---|---|
| 작업 트리 | 에이전트 작업 트리 (반입 뒤 지움) · 시작 `5288ff3c4` → 끝 `db97d0644` (메인 번호) |
| 바뀐 파일 9 (모두 `scripts/`) | `rint_r_chain.py` · `rint_first_result.py` (새) · `sdcp_gain_vox015_8arm.sh` · `check_all.sh` (단계 줄 하나 + 주석) · 시험 5 (`test_rint_r_chain.py` · `test_rint_r_chain_e2e.py` · `test_ca_ext_runner.py` · `test_ca_s0_census.py` · `test_rint_first_result.py` (새)) |
| 하지 않은 것 | push · fetch · `check_all.sh` 실행 · GPU · 킷 풀이 · 등록 R · Q9 · README · 웹앱 · `findings.json` · 다른 호스트 · 문서에 SHA 적기 |
| 봉인 32 · S0_SAME_FILES | CODE_FILES 32 ∩ 바뀐 파일 = 0 · S0_SAME_FILES 7 ∩ 바뀐 파일 = 0 (단 §9 한정) |

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (claimed · 확인은 Codex 몫) | 닫지 않는 것 |
|---|---|
| C1 (RCA2-05): 실행 정책 칸, `--max-hours` 대조, 최대 시도 수, 결과 전 멈춤만 재시도, 같은 설정, 첫 완주 채택, `attempt_<n>` 보존, 팔마다 기계 이름, 문서 숫자 생성·정확 대조, 시도 원장, 재실행 | 숫자 (시간 상한 · 최대 시도 수 · 기계 목록 · env_unit 판) — 봉인 때 넣을 몫이라 비워 둠 |
| C2: 12 단위 · 세 명령 · 합치기 · 넘침 런 · 첫 풀이 끝 표지 · 러너 프로세스 그룹 · `.unchecked/` · 새 순서 · no-op 사다리 끝 · 판정 같은 묶음 | 등록 R · Q9 개정 (§10 이름 표 → 메인) · 원장 상태 (RCA2-05 · 07 → 메인) |
| Codex ① 같은 프로세스 문구 · ② 부모 사망 뒤 종료 확인 (`--stage recover`) · ③ `REVERIFY_DIFF` + 보고 · RCA2-07 구현 주석 | 실침대 · GPU · 다른 하드웨어 · Codex 회차 ② 조건 (B/C 통합 · 작은 실제 producer→판정→재판정) |

## 1. 커밋

| 항목 | 시험 → 구현 | 무엇 |
|---|---|---|
| C1a | `2c1308bb2` → `fcf20b822` | 계획 `rint-r-plan-v3` 의 `exec_policy` (값 칸 넷이 null 이면 `PLAN_NUMBER_UNREGISTERED`, 규칙 칸 넷). `--max-hours` = 계획 값. `--machine` 필수, 런 기록마다 기계, 판정이 대조. `--stage plan-doc` (블록 생성 · `--check-doc` 정확 대조). RCA2-07 주석 |
| C2a | `63d092e18` → `db39116f8` | no-op 을 사다리 끝으로 (`ladder_noop`). 예측 첫머리에서 옛 이름으로 냄. 새 순서 · 이른 단조 `checks['r_monotone_early']`. `_replay_ladder` · `_replay_predict` |
| C2b | `a95d8177d` → `4ed966b5d` | `run_in_group` (새 세션 · env 표지 · `groups/<런>.launch.json` · `.end.json`). 종료를 확인한 뒤에만 팔을 읽음 (`GROUP_UNCONFIRMED`). `P2_ATTEMPT=1`, 감싸개 `rint_first_result.py`, payload 는 런 폴더 `.unchecked/`. `--stage recover` |
| C1b | `b89513826` → `ae8ea5ebd` | 시도 원장 (git · 덧붙이기만 · `--stage ledger --init/--add`), `attempt_<n>`, 풀기 전 대조, 결과 줄, 채택, 원장 예측 · 판정, `recover --ledger` |
| C1b-2 | `a45603c01` → `8b2bc633a` | 재실행 (`--add --resume` · `ResumeRunner` · 끝난 런 복사 · 남은 payload 바이트 대조 `RESUME_MISMATCH`) |
| C2d | `7c5349bf8` → `a74604e98` | `--unit` · `--point --expand` · `--merge` (`MergeFetch` · 부분 채택 · 늦은 대조 · 사본 · 원장 묶음 · `EXPANSION_NEEDED`). 합친 예측은 원장 판정만 |
| C2e | `3529ebf6d` → `f1698cf83` | `verdict_env.json` · `--reverify --out` → `reverify_report.json` |
| 시험 고침 | `db97d0644` | e2e E13 명령줄 자름 (§5). `check_all.sh` 주석 F01–F08 → F01–F09 |

15 커밋 모두에 `author 10-27 approved bundle C` 와 끝 두 줄이 있습니다. 커밋마다 `check_doc_refs` · `check_review_findings` 둘 다 rc 0 이었습니다.

## 2. 시험 수 — 고치기 전 → 뒤 (3.11)

| 항목 | 시험 | 고치기 전 (직전 코드 + 새 시험) | 뒤 |
|---|---|---|---|
| C1a | `test_rint_r_chain` EP | 284/294 (EP 10 개 실패) | 295/295 (EP12 는 구현과 함께) |
| C1a | `test_ca_s0_census` L3ep | 163 + 4 실패 | 167/167 |
| C1a | e2e E1m | 26 + 1 실패 | 27/27 |
| C2a | chain NP · OR · P01 · P01b · P03 · V14 | 1/17 (P01b 만 통과) | 309/309 |
| C2b | chain GR01–10 · runner N12a–e · e2e E1 · E13 | 0/10 · 0/7 · 12 통과 5 실패 | 323 · 151 · 36/36 |
| C2b | `test_rint_first_result` | FileNotFoundError (감싸개 없음) | 9/9 |
| C1b | chain AL01–18 · e2e E14 | 0/18 · 0/1 | 351/351 (AL19–28 은 구현과 함께) · 37/37 |
| C1b-2 | chain RS01–05 · e2e E15 | 0/5 · 0/1 | 357/357 · 38/38 |
| C2d | chain UM01–16 | 0/16 | 380/380 (UM17–23 · E16 은 구현과 함께) · e2e 39/39 |
| C2e | chain RV01–04 | 0/4 | 384/384 |
| 시험 고침 | e2e E13 · E13t · E13p | 3.8 에서 E13b · E13e 실패 | 3.8 5/5 · 3.11 5/5 |

늘어난 수: chain +100 (EP 11 · NP 8 · OR 6 · GR 14 · AL 28 · RS 6 · UM 23 · RV 4), e2e +13, census +4, runner +9, first_result 9 (새 파일).

## 3. 회귀 — 시작 `5288ff3c4` ↔ 끝 (3.11.15 · numpy 2.4.6 · scipy 1.17.1 · BLAS 스레드 1 · nice 19)

| 묶음 | 시작 | 끝 |
|---|---|---|
| rint_r_chain · e2e | 284 · 26 | 384 · 39 |
| ca_s0_census · ca_ext_runner | 163 · 142 | 167 · 151 |
| carbon_junction · b6 · verdict · z1 · z3 | 466 · 501 · 31 · 95 · 84 | 같음 |
| ptfe_face_alpha · target_cert (빠른 판) · conv_cert | 242 · 264 · 30 | 같음 |
| run_contract selftest · step3 `--selftest-rint` · `--selftest` | 124 · PASS · PASS | 같음 |
| rint_receipts · webapp 셋 (labels · explainer · scope) | 105 · 92 · 71 · 31 | 같음 |
| 규율 검사 · 규율 selftest | 0 오류 (경고 17) · 128 | 같음 |

- 21 묶음은 `f1698cf83` 에서 돌렸고 모두 rc 0 입니다.
- `db97d0644` 은 e2e 시험 파일과 주석만 바꿉니다. 그 뒤에 e2e 39/39, 규율 0 오류 · 128/128, first_result 9/9 (3.11 · 3.8) 를 다시 돌렸습니다.

## 4. 끈 경로 · 기존 경로 비트 대조

**끈 경로 (R4-06 (a) 좁힌 문장 기준)**: 시작 판 시험 틀과 끝 판 시험 틀을, 같은 가짜 러너 세계의 두 장면 (V10 넘침 없음 · P05 넘침 있음) 에서 비교했습니다.

| 비교 | 시작 → 끝 | 결과 |
|---|---|---|
| 사다리 P0 · P1 | CALIBRATED · 13 → 14 런 | 앞 13 런 (요청 칸 · 팔 sha · 이름) 같음 · 끝 런 = `sbe_noop` · 사다리 칸 같음 |
| 예측 (넘침 없음) | 26 → 24 런 | no-op 2 (시작 P01 · P02) 가 사다리 끝으로 옮겨감. DBE 요청 · 차례 · 팔 sha · rc 같음, 이름은 두 칸 당겨짐, checks · origin 같음 |
| 판정 (넘침 없음) | PASS_INFORMATIVE ↔ 같음 | 등급 칸 다섯 같음 · 결과 JSON (증서 칸 뺌) 같음 · 증서 52 칸 = 이름 당김 + no-op 2 값 같음 |
| 판정 공개 칸 차이 (넷) | — | `arms` 는 경로만 다름 (sha 다중집합 70/70 같음) · `input_dirs` 임시 폴더 · `inputs` 요약 sha · `registration` (계획 v2 → v3 = exec_policy 때문에 해시 다름) |
| 예측 · 판정 (넘침 있음 P05) | 38 → 36 런 | DBE 요청 집합 · 팔 · rc 같음 · checks 같음 + `r_monotone_early` 4 칸 · 차례 = 새 차례 · 판정 같음 |

**기존 경로**: 시작 SHA 사본 (scripts 644 파일이 `git show` 와 바이트 같음, 여기에 docs 넷 + `.gitignore`) 과 대조했습니다.

| 묶음 | 결과 |
|---|---|
| b6 B (`--expect-identical`) | 39/39 · 차이 0 |
| z3 O (`--expect-identical`) | 15/15 · 차이 0 |
| 러너 NB (`--old-runner`) | 2/2 |

첫 판에서는 b6 B 와 z3 O 의 payload 꼴이 모두 실패했습니다. 차이 칸은 `collector.anchors_source` · `pristine_precision` 둘이었습니다. 사본에 `docs/data/rint_eis_anchors.csv` 가 없어서 생긴 환경 차이이고, B0u-6 이 일부러 실패시키도록 만든 꼴입니다. CSV 를 넣고 다시 돌리니 차이가 0 이었습니다.

## 5. kgy 판 — `scripts/check_kgy_py38.sh` (Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1)

| 회차 | 결과 |
|---|---|
| 1 회차 (`f1698cf83`) | 10 묶음 통과 · e2e 37/39 (E13b · E13e 실패) |
| 2 회차 (`db97d0644`) | **11/11**: run_contract 124 · step3 rint PASS · ptfe 242 · carbon 466 · b6 501 · 러너 151 · chain 384/384 · e2e 39/39 · target_cert 264 · conv_cert 29/29 (3.8 의 수) · census 167 |

1 회차 실패의 원인은 제 시험 도구 결함입니다.
- `e13_cmdlines` 가 `/proc/<pid>/cmdline` 을 160 자로 자른 뒤 `rint_first_result.py` 이름을 찾았습니다.
- 시험 심은 진짜 인터프리터의 절대 경로로 exec 합니다. 3.11 경로는 22 자, uv 3.8 경로는 74 자입니다.
- 그래서 3.8 에서는 감싸개 이름이 160 자 밖으로 밀렸고, 죽이는 손이 "표지 앞" 창을 보지 못했습니다. 120 s 를 기다린 뒤 이미 끝난 런을 죽였습니다.
- 사슬 쪽은 정상이었습니다: 런 rc 0, 끝 기록 by chain, 원인 None, 확인 True.

고친 내용 (`db97d0644`, 시험만):
- 명령줄을 자르지 않고 전체로 찾습니다.
- 죽이는 손이 창을 실제로 봤는지 (`saw_window`) 를 E13b · c · e · f 검사에 넣었습니다.

원장 등재 후보 (메인 몫): 제 결함 SELF 항목 하나.

## 6. 기계 간 결정성 (Q9 §8 · Codex Q-E)

같은 컨테이너 CPU 에서 두 판을 비교했습니다: 3.11.15 / 2.4.6 / 1.17.1 ↔ 3.8.20 / 1.24.4 / 1.10.1. 침대는 한 번만 합성했고, 실물 러너와 payload 를 CPU 로 돌렸습니다.

- SBE o0 + DBE o0–7 의 `sid_fp`: **9/9 같음**.
- σ: **9/9 비트 같음** (최대 상대 차 0).

## 7. 변이 (가드마다 한 줄 · 그 가드를 보는 시험 부분집합)

| 항목 | 변이 | 잡힘 | 생존 | 첫 판 생존 → 처리 |
|---|---|---|---|---|
| C1a | 24 | 24 | 0 | — |
| C2a | 16 | 16 | 0 | MC12 는 적용 오류 → MC12a–c 셋으로 나눔 |
| C2b | 51 | 50 | 1 (MG04) | — |
| C1b | 57 | 56 | 1 (ML09) | ML14 · 40 · 48 · 54 → 시험 보강 뒤 잡힘 |
| C1b-2 | 12 | 12 | 0 | MQ08 · MQ11 → RS06 + RS05 보강 |
| C2d | 41 | 41 | 0 | MU10 · 11 · 34 · 37 → UM07 (g)(h) · UM13 보강 · MU41 새로 더함 |
| C2e | 6 | 6 | 0 | — |
| **합** | **207** | **205** | **2** | |

살아남은 둘은 같은 동작이라 잡을 수 없는 변이입니다.
- **MG04** (zombie 를 살아 있다고 셈): zombie 의 environ 을 못 읽어서 (ESRCH 실측) 그룹 원으로 잡히지 않습니다. 동작이 같습니다.
- **ML09** (끝 줄바꿈 검사 끔): 끝 줄바꿈이 없으면 마지막 줄 JSON 이 깨져 같은 멈춤 `ATTEMPT_LEDGER_MISMATCH` 가 납니다.

## 8. 실경로 kill 시험 (실제 러너 · payload · 프로세스 그룹 · 합성 킷 · CPU)

| 시험 | 죽이는 것 | 확인한 것 |
|---|---|---|
| E13b | 러너만 SIGKILL (표지 앞) | RUNNER_RC · 그룹 죽이고 확인 True · 표지 프로세스 0 · 지연이 끝난 뒤에도 표지 · payload 없음 |
| E13c | 러너만 SIGKILL (표지 뒤) | 확인 True · 표지 하나 (`.unchecked/`) · 팔 payload 없음 |
| E13d | 시간 초과 (6 s · 지연 20 s) | TIME_LIMIT · 원인 timeout · 확인 · 아무것도 남지 않음 |
| E13e | 사슬 부모 SIGKILL (표지 앞) | 그룹은 살아 있고 끝 기록 없음 → recover 가 죽이고 확인 (by recover · parent_dead) · 지연 뒤에도 파일 없음 |
| E13f | 사슬 부모 SIGKILL (표지 뒤) | recover 확인 · 표지 하나 · payload 없음 |
| E14 · E15 | 원장 시도 · 표지 뒤 부모 SIGKILL | 결과 줄 · 폴더 sha (독립 계산) · recover → `--resume` → CALIBRATED · 사다리 칸 = E14 와 같음 |
| E16 | 합치기 fetch 가정 | 같은 요청 · 다른 이름 (P05_corner ↔ U01_corner) · 다른 폴더 → 팔 JSON 바이트 같음 · SV 귀속 verified |
| E1g · E1u · E8u · E12g | 정상 런 | 런마다 그룹 · 표지 기록 · 조기 반환 표지 · 원천 런도 그룹 |
| 실경로 변이 RP1 | run_in_group 의 남은 프로세스 정리 끔 | E13b · E13c 실패 → 잡힘 |
| 실경로 변이 RP2 | recover_group 의 그룹 죽이기 끔 | E13e · E13f 실패 → 잡힘 |

## 9. S0_SAME_FILES

일곱 파일 모두 바뀌지 않았습니다. 다만 `ca_s0_census.py` 가 `rint_r_chain.require_plan_numbers` 를 import 합니다. 그래서 **S0 단계 2 관문도 exec_policy 값이 null 이면 거부**하게 되었습니다. 이것은 census L3ep 4 개가 시험합니다.

## 10. 등록 개정에 쓸 이름 표

- **Q9 §7 이름 그대로 쓴 것**: `MACHINE_NOT_ALLOWED` · `ATTEMPT_LEDGER_MISMATCH` · `ATTEMPT_ORDER_MISMATCH` · `ATTEMPT_AFTER_ADOPTED` · `RESUME_NOT_ALLOWED` · `RESUME_MISMATCH` · `UNIT_MISSING` · `UNIT_EXTRA` · `UNIT_PROVENANCE_MISMATCH` · `EXPANSION_NEEDED` · `unused_runs` · `REVERIFY_DIFF`.
- **새로 지은 것**:

| 종류 | 이름 |
|---|---|
| CLI | `--stage plan-doc --plan [--registration --check-doc]` · `--machine` (사다리 · 예측 · ledger --add 필수) · `--stage ledger --ledger L --init --plan` / `--add --ledger-target --machine --plan --runner --root [--resume n]` · `--ledger L --attempt n` · `--stage verdict --ledger [--attempt-dirs]` · `--stage recover --out [--ledger]` · `--stage predict --unit <법칙>_c<c>_<R>` · `--point <이름> --expand <expansion.json>` · `--merge <폴더…> [--expand]` · `--reverify … --out` |
| 원장 대상 | `ladder:P0\|P1[:FIBRE\|UNREG\|GRID]` · `predict[:FIBRE\|UNREG\|GRID\|SVORDER]` · `unit[:V]:<이름>` · `point[:V]:<이름>` |
| 새 멈춤 | `PLAN_DOC_MISMATCH` · `GROUP_UNCONFIRMED` · `ATTEMPT_LIMIT` |
| 상태 · rc | 단위 · 점 요약 = `UNIT_DONE` · `POINT_DONE` · 합치기 = `EXPANSION_NEEDED` (rc 4) · 결과 줄 status `completed\|stopped\|rejected\|interrupted` · side `pre\|post` · cause `timeout · signal · parent_dead · group_unconfirmed · resource · runner_rc · gate · check · presolve` |
| 화면 줄 | `PLAN_DOC_SAME` · `LEDGER_INIT` · `ATTEMPT_ADDED n=` · `ATTEMPT_REJECTED` · `ATTEMPT_RESULT` · `ATTEMPT_OPEN` · `REVERIFY_SAME` |
| 칸 | 요약 · 런 `machine` · 사다리 `noop {law · rj · status · ok · stop}` · `checks.r_monotone_early` · `attempt` · 런 `group_cause` · `copied_from` · `source` · `resume {from · copied · rerun · compared · determinism}` · `merge {ledger · expansion · units · attempts · unused_runs[why] · missing_points}` · 판정 `ledger` · `ledger_input` |
| 거부 기록 · 원장 | `attempt_<n>/rejected.json` 또는 옆 파일 `attempt_<n>.rejected.json` (rint-r-rejected-v1: n · code · cause · ledger_commit) · `rint_r_attempts.jsonl` (rint-r-ledger-v1 · 머리 · 항목 · 결과 줄) · `attempt.json` (rint-r-attempt-v1) |
| 폴더 꼴 | `<out>/attempt_<n>/` · `<단계>/groups/<런>.launch.json` · `.end.json` (rint-r-group-v1) · `<런>/.unchecked/<팔>.json.first_result.json` (rint-first-result-v1) · 합치기 `units/<대상 ':'→'-'>/attempt_<n>` · `ledger/ledger.bundle` · `expansion.json` (rint-r-expansion-v1) · `merge_summary.json` (rint-r-merge-v1) · 판정 `verdict_env.json` (rint-r-verdict-env-v1) · `reverify_report.json` (rint-r-reverify-v1) |
| 실행 정책 칸 | `exec_policy {max_hours · max_attempts · allowed_machines · env_unit {python_minor · numpy · scipy} · retry_rule=pre_result_only_v1 · same_config=plan_code_bed_env_v1 · adoption=first_not_pre_result_v1 · attempt_dir=attempt_<n>}` · 블록 표지 `<!-- rint-r-plan-doc:begin v1 -->` … `<!-- rint-r-plan-doc:end -->` · env `P2_ATTEMPT=1` · `RINT_RUN_TOKEN` |

## 11. 결정 필요 (등록이 정하지 않아 고르지 않은 자리)

각 항목에서 지금 구현은 보수 쪽으로 해 두었습니다. 줄 끝이 권고입니다.

1. **`--machine` 필수.** 등록 R · kgy 명령 문서는 `[--machine]` (선택) 로 적혀 있습니다. → 문서를 필수로 고칩니다.
2. **등록 R 의 계획 숫자 블록 자리.** 블록이 없으면 R 진입을 거부합니다. → §2-1 옆에, 봉인 커밋에서 `plan-doc` 출력을 그대로 붙입니다.
3. **S0 단계 2 관문도 exec_policy null 이면 거부 (§9).** → 그대로 둡니다 (DBE 단계 2 전에 계획 하나).
4. **`MACHINE_NOT_ALLOWED` 하나가 두 경우를 덮음** (허용 목록 밖 + 런 기계 ≠ 단계 기계). → 이름 하나로 두고 사유 문장으로 가릅니다.
5. **`GROUP_UNCONFIRMED` (새 이름) 와 구현 상수 `GROUP_GONE_WAIT_S = 30 s`.** 이 값은 숫자이고 등록 밖입니다. → 등록에 "대기 상한 = 판정 무관 구현 상수" 한 줄을 넣습니다.
6. **다른 기계 · pid 이름공간 · 기계를 모르는 다른 부팅에서 recover 하면 미확인 (rc 3).** 확인할 때까지 결과 줄이 없어 다음 시도가 막힙니다. → 그대로 둡니다.
7. **`ATTEMPT_LIMIT` 의 셈.** 거부 항목과 재실행 항목도 셉니다. → 확인 필요.
8. **`RESOURCE_WORDS` 표 (낱말 10).** 재실행 자격을 정합니다. `CUDA_ERROR_ILLEGAL_ADDRESS` 는 코드 결함일 수도 있습니다. → 등록이 표를 확정합니다.
9. **판정 `--ledger` 가 선택 (없으면 ledger null).** 합친 예측은 필수입니다. → 등록 R 판정 명령에 필수로 적습니다.
10. **시도 번호는 원장에서 정함 (폴더를 덮지 않음).** 재실행은 같은 바탕 폴더에서만 됩니다. 재실행 자격은 환경 지문의 모든 칸이 같아야 합니다 (BLAS 는 새 인터프리터로 잼). → 확인 필요.
11. **GPU 비결정성이면 남은 payload 대조가 `RESUME_MISMATCH` 가 됨.** 그러면 GPU 런은 사실상 재실행이 안 됩니다. → 결정 필요.
12. **`group_unconfirmed` 를 재실행 원인으로 둠** (recover 가 확인한 뒤에만) · 정리 중 신호 = `signal_after`. → 확인 필요.
13. **결정 기록에 W0 를 넣지 않음.** Q9 §3-2 는 "W0 기록" 이라 적었지만 W0 는 σ 값에서 나와 봉인 대상입니다. → 넣지 않는 쪽을 권고합니다.
14. **Q9 안에서 원장 접두 어긋남의 이름이 둘** (줄 82 = `UNIT_PROVENANCE_MISMATCH` · 줄 122 = `ATTEMPT_LEDGER_MISMATCH`). 구현은 `ATTEMPT_LEDGER_MISMATCH` 를 씁니다. → Q9 문구를 하나로 맞춥니다.
15. **한 원장에 `predict` 대상과 `unit:*` 대상이 함께 있을 수 있음** (경로 사이 선택을 막지 않음). → 원장 하나에 경로 하나로 등록합니다.
16. **합치기 사본이 통째 바이트 복사임** (실침대 크기 · 보관 자리 미정).
17. **`EXPANSION_NEEDED` rc 4 · `merge_summary.json` 이름.**
18. **끝 합치기에서 빠진 점이 `EXPANSION_NEEDED` (missing_points) 로 나옴** (모두 결과 전인 점 포함).
19. **단위 시도마다 첫머리에서 no-op 검사.**
20. **요청 안 된 대상의 대조 실패를 `UNIT_EXTRA` 로 봄** (보수 쪽).
21. **다시 판정 보고의 결과 칸은 이름만** (값 봉인).
22. **판정 환경 옆 파일은 새 판정에만 있음.**
23. **변이는 SVORDER 만 시험했음.**
24. **합치기에 러너와 킷이 필요** (SV 모서리 봉인 원천 = 조립만 런).
25. **다시 판정이 경로에 묶임** (입력 폴더 · 원장 절대 경로).

## 12. 한정

- **끈 경로 비교**는 가짜 러너 세계 두 장면입니다. 실물은 E16 의 요청 하나뿐입니다. 기존 경로 비교는 합성 픽스처 payload 입니다.
- **결정성**은 같은 CPU 에서 두 인터프리터 판을 비교한 것입니다. 다른 하드웨어 (AVX-512 ↔ AVX2 = RCA-07 칼날), GPU, kgy 기계 자체는 시험하지 않았습니다. kgy 판 인터프리터는 3.8.20 이고 kgy 는 3.8.10 입니다.
- **실경로 kill** 은 이 컨테이너의 같은 pid 이름공간에서만 돌렸습니다. 다른 기계 · 이름공간 · 재부팅 규칙은 단위 시험 (GR) 만 있습니다.
- **Codex 한정 그대로**:
  - Q-D: 그림자 런 · 모든 사본의 일관 편집은 못 막습니다.
  - Q-G: 플랫폼 무관 판정을 보장하지 않습니다.
  - Q-I: 이전 사슬과 모든 STOP 우선순위가 같다고 쓰지 않습니다.
  - Q-J: 남은 payload 가 없으면 결정성 가정입니다.
  - Q-K: 표지는 종료된 그룹의 snapshot 으로만 뜻이 있습니다.
- **표지 "덮지 않기"** 는 확인 뒤 replace 입니다. 짧은 창이 남고, 시도 폴더와 런 이름 규칙이 그 창을 막습니다 (기계적인 원자 보장은 아님).
- **변이**는 그 가드를 보는 시험 부분집합만 돌렸습니다.
- **임시 폴더 하나를 지웠습니다**: 이전 맥락에서 이 시험의 이름꼴 (rint_r_chain_t_ 로 시작하는 /tmp 폴더 하나). 같은 이름의 시험 프로세스가 없음을 확인한 뒤였습니다. 메인 게이트와 겹쳤다면 그 단계를 다시 돌려야 할 수 있습니다.

## 13. 정리 · 근거 파일

시작 SHA 사본 · 임시 폴더 · SID 워크스페이스는 지웠습니다 (스크래치 6.9 MB 남음). 실행 로그 (모두 메인 세션 스크래치 rint_c/ 아래 · 리포에 넣지 않았다 · 컨테이너가 바뀌면 없다):
- 회귀: base_logs/_summary.txt (시작) · logs_final/_summary.txt (끝) · logs_postfix/_summary.txt (고침 뒤)
- 기존 경로: logs_offpath2/
- kgy: logs_kgy_r1/ · kgy_check_r1.out · logs_kgy_r2/ · kgy_check_r2.out
- E13 고침: logs_e13fix/
- 결정성: sid_311.json · sid_38.json
- 변이: mut_*_res.json · mut_realpath_res.json
- ★ (10-28 밤 · 사전 공격 5 회차 PC5-11) 위 목록 = 리포 사본 `docs/reviews/rint2_rr_fix_evidence_20261023/report_c_raw/` (바이트 그대로 · 93 파일 · `SHA256SUMS` · 출처 · 고른 것 = `SOURCE.txt`) — 위 "리포에 넣지 않았다 · 컨테이너가 바뀌면 없다" = 10-27 시점.
