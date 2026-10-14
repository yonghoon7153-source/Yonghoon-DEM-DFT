# Codex 짧은 재확인 요청 — DEM 언로딩 키트 수정 (ULKR-01~12 · 등록 개정 3) (2026-10-14 · 결과 0 건 · 리뷰 핀 ⬜ · 발송 = 1저자)

> **한 줄**: 키트 재검토 (핀 `2783061ea` · **HOLD**) 의 P1 여섯 · P2 여섯을 판정문 §3–§4 의 최소 해결대로 고쳤다 (시험 먼저 · LIGGGHTS 없음) —
> 각 반례가 고친 트리에서 거부되고 정상 경로가 그대로인지, 등록 개정 3 (REG §14) 이 판정문 §4 · §7 해제 조건을 그대로 담는지 짧게 판정해 달라.
> ✅ **1저자 10-14** — 수정 계획 `docs/reviews/dem_unloading_kit_fix_plan_20261014.md` Q1–Q9 = 전부 (가) (*"q1~q9는 권고대로야"*) · 실행 기록 = 그 문서 §5.
> **리뷰 핀** = ⬜ (이 요청서를 담은 커밋이 본 가지에 병합된 뒤의 SHA — 발송 때 1저자가 적는다) · **기준** = `2783061ea` (판정문 핀) · 수정 가지 시작 = `6f80eddb3` (판정문 · 증거 반입).

> ⚠ **정정 표지 10-14 밤 (`SELF-116`)**: 본문 (§1 표) 의 커밋 번호는 수정 작업 트리 (에이전트) 판이라 원격에 없다 — 본 가지 대응 (cherry-pick · `git patch-id` 같음) = `docs/reviews/dem_unloading_kit_fix_plan_20261014.md` §5 표 (정정판) · `docs/reviews/doc_refs_sha_exceptions.tsv`.  본문은 보낸 그대로 둔다 (판정 = 핀 `a30fe150e`).

## 0. 대상 · 지위

- 판정문 `docs/reviews/codex_review_dem_unloading_kit_20261014.md` · 증거 `docs/reviews/codex_dem_unloading_kit_review_evidence_20261014/` (우리는 그 탐침 스크립트를 **실행하지 않았다** —
  자료 (`evidence/*.json` · `_cases_20261014.tgz` · `notes/`) 로만 읽고 반례를 우리 시험으로 다시 만들었다.  판정문 §11 탐침을 고친 트리에서 다시 돌려 주면 좋다).
- 바뀐 곳 = 키트 `docs/data/ps45_unload_20261009/` (판독기 · 관측자 · 관문 · 러너 · 생성기 · 덱 42 재생성 · 봉인 · 모의 시험 · README) · 이력 시험 키트 `history_test/` (문법 fixture 더함 · H0–H5 덱 여덟 바이트 그대로) ·
  등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §14 (개정 3 · 결과 0 건) · 수정 계획 §5.
- 바꾸지 않은 것 (판정문이 바꿀 근거 없다고 한 것): 물리 목표 · P_meas 1 MPa · 결정표 0.10 %p · S1 · S2 · S4 문턱 · KE 계수 10 · C1 총힘 정의 · 판 법선력 부호 −1 · 명시 restart · 다섯 침대 · S0 · Q9 (매 창 쌍 덤프 유지).
- 실행 · 재실행 없음 (본 R · 10:0 연장 · U · H0–H5).  원장 `docs/reviews/findings.json` 은 이 수정 가지에서 고치지 않았다 (claimed_fixed 표시 = 메인 세션 · 1저자).

## 1. 판정문 해제 조건 ↔ 수정 (커밋 · 시험 = 계획 §5 표)

| 원장 | 해제 조건 (판정문) | 수정 · 자리 | 시험 (고치기 전 → 뒤) |
|---|---|---|---|
| `ULKR-01` | 확인 두 단의 순서 · 완료 · 등록 정상성 · 파일 → 판독 → 관문 | `ul_reader.py` `arm_verdict.confirmations` (k* + 1 · k* + 2 · B · CONFIRM · 덱 정상 · S3 · 유한 · 판 접촉 요구 없음 = Q1) · REG §14-1 | `ul_reader` R20 (`fbf59cc78`) |
| `ULKR-02` | k = 0 부터 모든 교차 · 보고 구간 ⊇ 첫 교차 괄호 | `crossings(steps, Pm)` 전 구간 · 외곽 [최소, 최대] · 비유한 = 미계산 · REG §14-2 | R21 (`fbf59cc78`) |
| `ULKR-03` | UTc 가 해시로 묶인 UT 부모 관측 · 경계 · 최종 report 까지 UT 주 값 보존 | 러너 `parent_UT.sha256` + manifest · `_continuation` · `_read_run_cont` (경계 중복 · 누락) · `_t3_entry` (UT 주 값 + UTc 보조) · REG §14-3 | R23 · `ul_runner_test` M9 (`e90f903f1`) |
| `ULKR-04` | 모든 경로 파싱 · 열 · 유한 · 요청 step · ID · 버린 행 재사용 금지 | `_atom_frame` · `_wall_rows` · `_s3_at` · `_s0_dump` · CSV 결손 · k 불연속 = 주 값 미식별 · REG §14-10 | R22 (`fbf59cc78`) |
| `ULKR-05` | 관측 전체 parse · 고유 ID 집합 · 기대 시점 · R_END ↔ UN · 선행 기술 실패 = RESTORED 없음 · 다음 제출 거부 | `restore_verdict` (`_obs_frame` · `_stage_tech` · Ut0 · R · UN) · `ul_gates.restoration_verdict` · 관문 `_job_restored` (RJ 잡 끝 줄 fails=0) · REG §14-10 | R17 · R18 · `ul_gates` F2 (`2b6500869`) |
| `ULKR-06` | 미지원 JOB RESUME 거부 · 1 회 · 기록 비덮어쓰기 · 같은 승인 팔 | `run_unload.sh` 초기 거부 · `resume_check` (`gate=ALLOW` · `resume=0` · 요약 없음 · 한 번) · REG §14-4 | `ul_runner_test` M7 · M7a · M11–M14 (`a03cff857`) |
| `ULKR-07` | 재접촉 = 같은 높이 · 남은 예산 · 예산 끝과 분리 뒤 4 창 · 판독기 불일치 = 보조 미완료 | 생성기 `_machine` (재접촉 → `ul_win_rc` · 예산 끝 `SEP_INCOMPLETE`) · 덱 재생성 · 판독기 `separation` (이동 = 초기화 · SEPARATE 창) · DONE ↔ SEPARATED · POST_DONE · 선언 창 ≤ 예산 · REG §14-7 | `make_unload_decks` GD15 (덱 모의기) · `ul_reader` R24 (`f67f242bb`) |
| `ULKR-08` | SYN PASS + 측정 부호 = 표 필수 · 총힘 시점 | `_hist_qualifies` · 반입된 실제 이력 시험 (be0acbd7…) 으로 대조 | R18 (`2b6500869`) |
| `ULKR-09` | 정확한 S0 · 무이동 · T_W 간격 · 완전 · 연속 · 고유 세 창 · 파싱 / 실행 성공 · 미달 = 기준 파일 없음 | `_uk_check` · `kebase` (rc 2 · 파일 없음 → S2 쓰는 팔 관문 거부) | R25 · `ul_runner_test` M18 (Codex `one_uk_row`) (`f67f242bb`) |
| `ULKR-10` | (A) 범위 확정 · 덱별 표 (B) S3 g 규약 · 배선 | (A) Q4 = 첫 재평형만 · 덱 그대로 · REG §14-5 (B) `_arm_g` (G_* = g_aux) · REG §14-6 | GD16 (중력 팔 20 덱 표) · R26 (`f67f242bb`) |
| `ULKR-11` | 단계 rc 포착 · 필수 선행 실패 중단 · 정상 미식별 ↔ 프로그램 오류 | 러너 `note` · `reader()` (`reader_<명령>_rc`) · G0 · Ut0 실패 = R · UN · UK 없음 · REG §14-10 | M4 · M15–M17 (`a03cff857`) |
| `ULKR-12` | 보고에 넣거나 미보고 명시 · C_all = 검증한 S0 봉인 · 프레임 완전성 · 묶음 | `ul_observers.s0_volumes` · `eps_sphere` · `w_proxy` · `ul_reader._aux_eps_w` (팔 판정 · report) · 러너 `bundle` (EXT2 · s0_decision · ul_base · selection) · README §3 · REG §14-8 | `ul_observers` O11–O12 · R27 · M19 (`d9e51323d`) |
| (Q8 · 판정문 §6) | SYN 이 지나가지 않은 경로 (바깥 include 재개 · 변수 주기 덤프 · move/mesh 반복 · state 복귀) | 이력 시험 키트 `in.hist_grammar.liggghts` · `run_history.sh --grammar-only` · `read_history.py --grammar` · 생성기 모의기 · README §1-6 · REG §14-9 | `make_history_decks` ⑯ · `read_history` S33–S37 (`e6c9049dc`) |

## 2. 명령 (Linux · 표준 라이브러리 · LIGGGHTS 없음 · 리뷰 핀 체크아웃 뒤)

```bash
K=docs/data/ps45_unload_20261009
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
for m in ul_lib ul_s3 ul_observers ul_gates ul_reader; do python3 -I $K/$m.py --selftest | tail -1; done   # 19 · 14 · 21 · 35 · 111 — 전부 PASS
python3 -I $K/make_unload_decks.py --selftest | tail -1 && python3 -I $K/make_unload_decks.py --check          # 291 / 291 · 덱 64 = 생성 결과
python3 -I $K/seal_kit.py --selftest | tail -1 && python3 -I $K/seal_kit.py --check && python3 -I $K/seal_kit.py --rules | head -3   # 76 파일 · 규칙 22 · 폐기 0
python3 -I $K/ul_runner_test.py --selftest | tail -1                                                          # 25 / 25 (가짜 mpirun · lmp)
python3 -I $K/history_test/make_history_decks.py --selftest | tail -1 && python3 -I $K/history_test/make_history_decks.py --check   # 156 / 156 · 덱 9
python3 -I $K/history_test/read_history.py --selftest | tail -1                                              # 53 / 53
```

- 봉인: 키트 `SHA256SUMS` sha256 `213695a0be89c7b6f8d59aea0b3132bf0cd080079a6de198a8e8c9964671aa86` · 이력 시험 `history_test/SHA256SUMS` `debe83877657978cdaf87b18e08edda501e520979dd40876f5e100c24e902163`.
- 판정문 §11 탐침 (증거 `probes/*.py`) 을 이 트리에서 다시 돌리면: `reader_adversarial` (확인 단 · 합집합 · NaN 행 · done_recontact · done_missing) · `reader_continuation` (UTc) ·
  `observer_adversarial` (one_uk_row · fixed_volume · gravity_floor) · `history_restore` (불완전 PRE · POST · 다른 ID UN · UN rc 1 · SYN 결손) 의 반례는 거부 · 정상은 그대로가 기대다
  (`deck_control` 의 재접촉 분기는 생성기 GD15 의 모의기로 같은 꼴을 시험했다).

## 3. 묻는 것

| Q | 무엇 |
|---|---|
| Q1 | REG §14-1 (확인 단 = 등록 정상 완료 · 판 접촉 요구 없음 · 덱은 그대로 세고 판독기가 판정) 이 C14 · C15 와 `ULKR-01` 해제를 충족하는가 |
| Q2 | 판독기 분리 규칙에 "같은 단 안 · SEPARATE 단계 창 · 이동 = 연속 초기화" 를 더하고 덱 DONE 을 `SEPARATED` · `POST_DONE` 사건 step 과 대조했다 (REG §14-7) — `ULKR-07` 의 판독기 쪽 해제로 충분한가 · 과한가 |
| Q3 | ε · W_proxy 를 UT (7:3 t3) · 팔 판정에서 냈다 (S0 → M 구간) · 비교 프레임 불완전 = 그 자리 미계산 (REG §14-8) — §12-9 의 뜻 · `ULKR-12` 해제와 맞는가 |
| Q4 | 문법 fixture 판정표 (키트 README §1-6) 가 판정문 §6 의 빠진 경로를 다 덮는가 · 생성기 모의기의 해석 가정 (변수 주기 덤프 = run setup 에서 공식 · 쓴 뒤 다시 · 고정 주기 setup 쓰기 = step % N = 0 이고 마지막이 그 step 아닐 때) 이 3d5c00f `output.cpp` 와 맞는가 |
| Q5 | 문법 fixture PASS 를 지금은 **절차** 로 두었다 (REG §14-9 · 러너 · 판독기 관문 아님) — 코드 관문 (예: RJ 복원 판정이 문법 판정 JSON 도 요구) 이 필요한가 (1저자 결정 대기) |
| Q6 | UC 는 단 끝 restart 를 쓰지 않아 RESUME 가 서지 않는다 (정책상 허용 팔 · 실제 = 새 시도 · REG §14-4 괄호) — 이대로 괜찮은가 |
| Q7 | 원장 처리 — `ULKR-01`~`12` 의 verified 범위 · 남는 것 (있으면 새 ID) · 판정문 §9 의 부분 (`ULR1-01` · `03` · `05` · `UL-*`) 에 이 수정이 미치는 범위 |

## 4. 다음 (1저자)

- 문법 fixture ibb 한 번 (키트 README §1-6 명령 · 수 분 · 결과 묶음 `gram_<시각>.report.tgz` 반입) — Codex 재확인과 순서 무관 · 둘 다 본 R 전.
- GO 뒤 = 등록 §13-6 순서 그대로 (R · 10:0 연장 → 7:3 개발 팔 → 본 U).  ⛔ 그 전에 본 R · U 를 내지 않는다.
