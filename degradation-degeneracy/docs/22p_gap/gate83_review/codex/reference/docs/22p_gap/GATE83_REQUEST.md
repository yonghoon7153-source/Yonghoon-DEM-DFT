# 83차 게이트 리뷰 요청 — 82차 잔여 **G82-N1 · N2 · N3 제한 보완** 결과 (라운드 1 종결 판정 요청 · 실행 GO 아님 · 라운드 2 착수 아님)

> 이 문서는 리뷰 요청문이다. 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요. 리뷰어는 exact HEAD 를 fetch 해 재실행·검증한다.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` (본진 — 2026-09-30 서브 ff 복귀 뒤 · `BRANCHES.md` "복귀 결과") |
| **코드 (판정 대상 HEAD)** | **`ea2af59e68a85b561c3e185f66b815aec877ca57`** — RUN_SCOPE 를 바꾼 커밋은 하나: **`7d291fbc88c0140df355e64ee43625af2c246278`** (G82 GREEN). `source_digest` **`02a776a7a0a3f4ba` → `7187bd31740514d4`** (`python -c "from src.io import source_digest; print(source_digest())"` 실측). 그 뒤 커밋 (변이 EXPECT `8e18ae83` · 증인 정정 `6723b2ad` · COMSOL 보존 `58bc7eef` · §36 `393f747e` · 2차 영수증 보존 `5313731c` · 새 세대 영수증 `4307b6f8` · 계약 줄번호 `ea2af59e`) 은 RUN_SCOPE 밖 |
| 사용자 승인 | 원장 §116 끝 (2026-09-30): "G82-N1·N2·N3 제한 보완 코드 라운드 … 승인된 4 파일만 최소 수정, RED 회귀 먼저, 변이, 2차 영수증 보존 후 새 세대 영수증 1회, 전체 회귀·smoke, GATE83 요청. 라운드 2·p_ini·연구 계산·실행 GO 는 제외" → **"승인 — 지금 착수"** · 검토자 `gate82_review/codex/NEXT_SCOPE_DRAFT.md` 범위 그대로 |
| 시작 전 고정 표 | `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` **§10** (`dfdd91a9`, 코드 변경 전 — §1–§9 불변) |
| RED | `6bc46caf` — `tests/test_gate82_residuals.py` 19 node, 패치 전 **18 failed / 1 passed** (대조군 `n2_00b` 골든 bank) — 이유 분류 §3 |
| GREEN | `7d291fbc` — gate82 **19 passed** · stage3 이웃 (gate81 44 + gate79 15 + design_wire) 109 passed |
| 영수증 | 2차본 보존 `5313731c` (`history/<leg>.validate.02a776a7a0a3f4ba.yaml`, cmp 동일) → **새 세대 `4307b6f8`** (clean `5313731c` · 원장 앵커 같은 커밋) — §5 |
| 변이 | `-g82` **12** — 첫 관측 12/12 rc 1 (`--emit-expect -k g82`, clean `7d291fbc`) · 재생 12/12 (clean `8e18ae83`) · 최종 재생 12/12 (clean `ea2af59e`, 전체 회귀와 같은 러너 · 시작 HEAD = 끝 HEAD) |
| 82차 패키지 원본 | `docs/22p_gap/gate82_review/` (zip `6445eb4a…` 1,036,284 B · `codex/` 105 · PACKAGE_MANIFEST `cbfa846b…` · `-text` 규칙 `4d88b9d5` 먼저 → 풀기 `3ae4aaf4` → blob 105/105) · 접수 원장 §116 |

## §0 묻는 것 / 묻지 않는 것

| 묻는 것 | 묻지 않는 것 |
|---|---|
| §1 표가 G82-N1 · N2 · N3 를 **코드로** 닫았는가 (검토자 닫힘 조건 대비) · 반례가 지금 어떤 검사에 어떤 이유로 걸리는가 | 실행 GO · 새 연구 leg · floor · pilot · 단계 4–6 · 12-P canary |
| 라운드 1 (G81-N1·N2·N3 + 자체 점검 + G82 잔여) **종결 판정** | 라운드 2 착수 (실물 v6 leg gate 배선 · 세대표 등록 · p_ini · dead 정의 삭제 · 계약 §0 정정) — 종결되어도 별도 사용자 승인 |
| §5 새 세대 영수증 수용 · §6 자기 신고 판정 | class/투영 게시 · 복원 (영수증용 격리 복원 제외) |

## §1 반영 표 (발견 → 닫힘 조건 → 코드 자리 → 시험 → 변이)

줄번호는 판정 대상 HEAD `ea2af59e` 실측 (`7d291fbc` 와 RUN_SCOPE 동일).

| 발견 | 검토자 닫힘 조건 | 코드 자리 | 시험 (`tests/test_gate82_residuals.py`) | 변이 (`-g82`) |
|---|---|---|---|---|
| **G82-N1** 관측 roster 재구성 | 봉인 입력 ↔ 출력 cond_id/objective/obs_key 연결 대조 · 관측 roster 독립 재구성 → 계획 · record 양쪽 · 출력에 없는 noise realization 은 봉인 입력에서 (추론 금지) · 양성 1 + 음성 (한 objective noise 변경 · realization 교차 · 같은 개수 다른 roster) · 봉인 · record 해시 일관 갱신 자료 | 공유 함수 `src/io.py` `observed_roster` :1573 (봉인 curves 의 cond_id 별 `lli · lam_pe · lam_ne · lam_pe_type · lam_ne_type · noise · seed` ↔ 각 fits 행 truth 열 정확 비교 · 관측 cond_id 마다 objective_order 정확히 한 행씩 · `DW.roster_from_conditions` 로 재구성) · `_sealed_curves_snapshot` :1628 (`_inputs/*_curves.parquet` 중 **계획 `inputs.curves_sha256` 와 바이트가 같은 것**만) · validator 새 검사 **`관측_roster_재구성`** :1919 (스냅샷 없음 → 실패 · problems · 재구성 sha ↔ 계획 `roster_sha256` · ↔ record `roster_observed_sha256` · 관측 수 ↔ `n_obs`; fits/map 을 못 읽는 조기 반환도 실패 :1872) · writer `src/fitting.py` `write_execution_record` :1402 (인자 `roster_sha256` 폐지 → `curves_df` · `design`; 같은 함수로 계산 · problems 면 기록을 쓰지 않고 `RuntimeError`) · 호출부는 실행이 읽은 봉인 스냅샷 `df` (:1795 `pd.read_parquet(_snap[…curves.parquet])`) 를 넘긴다 | n1_00 (양성 · 두 noise 실현) · n1_01 (한 objective 행 noise · `_reseal_fits` 뒤 `출력봉인_재계산` 통과 확인) · n1_02 (두 실현 noise 교차) · n1_03 (record roster 를 같은 n_obs 의 다른 유효 roster 로) · n1_04 (스냅샷 삭제 → fail-closed) · n1_05 (writer 계산 · 불일치 거부) | `observed-roster-compares-rows-to-the-sealed-inputs-g82` · `record-roster-is-compared-to-the-rebuilt-roster-g82` · `a-missing-sealed-snapshot-is-a-failure-g82` · `the-writer-refuses-rows-that-disagree-with-the-inputs-g82` |
| **G82-N2** bank 선언 ↔ 구현 | 지원 profile **하나** 명시 → 실행 전 소비자 · validator 가 모두 검사 (envelope · 설계 generator/version, 설계 seed rule · dtype · endian · space) · 미지원 선언 거부 · 별칭은 명시 대응표만 · ID 도메인 · 골든 · 정상 bank 바이트 불변 | `tools/design_wire.py` `STAGE3_BANK_PROFILE` :565 (`pcg64` · `H(pair_group_id, bank_version)` · `float64` · `little` · `unit_cube`) · `STAGE3_BANK_VERSIONS = ("v6.0",)` · `check_bank_profile(design_bank, envelope_bank)` :570 (필드별 정확 문자열 · 둘 다 주면 generator · version 상호 일치 · **별칭 없음**) · 호출 셋: `tools/preserve.py` `check_envelope_v4` :3235 (→ `PlannedLegV4` 봉인 · `check_planned_envelope` · `run_transaction` · `check_receipt`) · `src/fitting.py` `_prepare_stage3` :1317 (설계 + envelope, 시작 전) · `src/io.py` `_stage3_rederive` :1660 (validator). `check_design` (설계 선언 **문법**) 은 넓힌 채 그대로 — 선언 reader · 골든 경로를 좁히지 않고 실행 · 검증 경로에서 거부한다 (§6-c) | n2_00 (양성) · n2_00b (골든 bank sha `c3009d16…` — 대조군, 처음부터 GREEN) · n2_01 ×5 (generator · version · seed_derivation · dtype · endian 각각) · n2_02 (envelope 만 philox → 봉인 거부 · envelope version v6.1) · n2_03 (시작 전: 설계 dtype float32 · stub envelope philox → fits 미생성) · n2_04 (validator: run_spec 설계 dtype · envelope generator 위조 + digest 사슬 재계산) | `unsupported-profile-values-are-refused-g82` · `the-envelope-bank-is-checked-against-the-profile-g82` · `the-consumer-checks-the-profile-before-start-g82` · `the-validator-checks-the-profile-g82` |
| **G82-N3** 세대 연결 | v6 실행/검증 경로의 지원 protocol generation 명시 연결 · sig_version · plan · record · 행 record_generation 불일치를 구조 오류로 거부 · v3/v4 역사적 읽기 일괄 금지 없음 · 소급 없음 | `tools/design_wire.py` `STAGE3_PROTOCOL_GENERATION = "v6"` :560 · `src/fitting.py` `_prepare_stage3` :1300 (계획 `protocol_generation != "v6"` → 시작 거부) · `src/io.py` validator 새 검사 **`세대_연결`** :1834 (sig_version 6 · 계획 · record · 행 `record_generation` 집합 == {v6}; 행 열을 못 읽으면 실패). `check_envelope_v4` · `check_execution_record` 의 세대 **문법** 검사와 역사적 v3 reader · legacy/prep reader 불변 | n3_00 (양성) · n3_01 (계획 v5 → 시작 거부 · fits 미생성) · n3_02 (계획 · record 함께 v5 — `check_execution_record` 는 `[]` 임을 시험 안에서 확인 → `세대_연결` 이 계획 · record 두 이유 문장을 **각각** · 한 행만 v5 도 같은 검사) | `the-v6-path-refuses-another-plan-generation-g82` · `the-validator-links-the-plan-generation-g82` · `the-validator-links-the-record-generation-g82` · `the-validator-links-the-row-generations-g82` |

## §2 최소 diff (승인 범위 4 파일)

`git diff --stat 8f54427c..ea2af59e -- src tools configs scripts run.sh requirements*.txt` (82차 발송 SHA 기준):

```
 src/fitting.py       |  24 +++++-
 src/io.py            | 116 ++++++++++++++++++++++++++++
 tools/design_wire.py |  40 ++++++++++
 tools/preserve.py    |   4 +
 4 files changed, 180 insertions(+), 4 deletions(-)
```

삭제 4 줄 전수 (`git diff -U0 … | grep '^-'`): writer 시그니처 `roster_sha256: str) -> dict:` · import `from src.io import realized_from_fits` (→ `observed_roster, realized_from_fits`) · record 의 `"roster_observed_sha256": roster_sha256,` (→ 재구성 sha) · 호출부 `roster_sha256=_s3["roster_sha256"])` (→ `curves_df=df, design=stage3["design"])`). 새 production 파일 0 · fitting 수치 알고리즘 · ID 도메인 · candidate/bank 골든 불변 (n2_00b · gate79 골든 · gate81 w03). sig 5 경로 불변 — 새 검사 둘은 `_stage3_checks` (sig 6) 안에만 있어 두 leg 영수증의 검사 수가 그대로다 (§5).

RUN_SCOPE 밖 동반 변경: `tests/test_gate82_residuals.py` (신규 19 node) · `tests/conftest.py` +2 (gated 등록 — production `run_fit` 을 smoke namespace 에서) · `docs/22p_gap/mutation_replay.py` (변이 12 + EXPECT 12) · `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` §10 · `docs/22p_gap/STAGE3_CONTRACT.md` (§1 줄번호 인용 1940→1955 · 1895→1910, 본문 불변) · 영수증 2 + history 2 · `LEG_PRESERVATION.yaml` (앵커 2 값 × 2 leg).

## §3 RED 이유 분류 (82차 §7-4 · §8-i 기준)

| node | 패치 전 실패 | 분류 |
|---|---|---|
| n1_01 · n1_02 | `AssertionError: []` — 봉인을 다시 맞춘 noise 위조가 **실패 검사 0 개**로 통과 | **실제 결함** (검토자 정적 반례의 실측) |
| n1_03 | `['실현_재계산']` 만 — record ↔ 계획 비교는 있으나 출력 재구성 없음 | 실제 결함 |
| n1_04 | `['입력_스냅샷']` 만 — roster 출처 부재를 따로 보지 않음 | 실제 결함 |
| n1_00 · n3_00 | 검사 없음 (`None == '통과'`) | 실제 결함 (검사 부재) |
| n2_02 · n2_03 · n3_01 | `DID NOT RAISE` — philox envelope 봉인 · float32 설계로 실행 시작 · v5 계획으로 v6 실행 시작 | 실제 결함 |
| n2_04 | `후보_재유도` 가 설계 digest 변경에 따른 pair_group 재유도 실패로만 떨어짐 — "bank profile" 이유 없음 | 실제 결함 (선언 대조 부재 · 다른 검사가 우연히 가림) |
| n3_02 | `['run_signature_재계산']` 만 — 계획 · record 함께 v5 인 산출이 stage3 검사를 전부 통과 | 실제 결함 |
| n1_05 | `TypeError` (writer 새 인자) | **무관 예외 — RED 증거로 세지 않는다.** 실제 결함은 n1_01 · n1_02 (writer 가 시작 전 SHA 를 복사) 와 같은 축 |
| n2_00 · n2_01 ×5 | `AttributeError` (새 함수) | **무관 예외 — RED 증거로 세지 않는다.** 실제 결함은 n2_02 · n2_03 · n2_04 |
| n2_00b | passed | 대조군 (정상 bank 바이트 불변) |

## §4 시험 · 변이 결과

| 단계 | 결과 |
|---|---|
| RED (`6bc46caf`) | 19 node — 18 failed / 1 passed (`scratchpad/red_gate82_initial.txt`) |
| GREEN (`7d291fbc`) | gate82 19 passed (32.56 s) · gate82 + gate81 + gate79 + design_wire **109 passed** (76.15 s) |
| 이웃 회귀 (`7d291fbc`, 영수증 재생성 **전**) | fitting · gate70 · 71 · 72 · 74 · 75 · hessian · io_bookkeeping · preserve: **644 passed · 17 failed** — 17 건 전부 영수증 identity 가족 (`g70_e3_17` · `g71_e3r_12` · `g72_a07` · `g74_3_01` · `g74_3_03[6]` · `g75_n3_00` · `g75_n3_01[5]` · `g75_n3_01b`). 새 세대 영수증 · 앵커 뒤 (`4307b6f8`) gate70–75 + 계약 인용: 135 passed · 1 failed (계약 줄번호 인용 → `ea2af59e` 정정 → 1 passed) |
| 변이 첫 관측 (`--emit-expect -k g82`, clean `7d291fbc`) | **12/12** 기대 node 를 물었다 (rc 1 은 EXPECT 미기재 때문 — 첫 관측 rc 0 없음) · `--check-preimages -k g82`: "모든 변이 지점이 정확히 한 번 나타난다" |
| 변이 재생 (clean `8e18ae83`, 시작 HEAD = 끝 HEAD · status 0) | **12/12** — "실행한 변이 12건이 전부 기대 node 를 call 단계에서 물었다" (scenario_total 12 · executable 12 · ran 12 · rc 0) |
| 등록부 규칙 시험 (`8e18ae83`) | gate67 · evidence_layer_58 · producer_closure_58 · promotion_seal_62 · scope_model_62: **3 failed** / 64 passed — `test_evidence_layer_58` 의 합성 정상 조각 3 시험 "정상 조각이 거부됐다": 증인 셋의 **끝 공백** (report 는 longrepr 끝 공백을 잘라 읽는다) → `6723b2ad` 정정 → 합성 조각 `check_coverage` rc 0 (등록부 344 · executable 333 · declared 11 전부 덮음) — §6-f |
| 최종 (clean `ea2af59e`) | clean `ea2af59e` · 시작 HEAD = 끝 HEAD = `ea2af59e68a85b561c3e185f66b815aec877ca57` · 시작/끝 status 0 줄 · 도는 동안 커밋 0 · 2026-09-30T06:18:27Z → 07:26:04Z: 전체 pytest (tests/ — docs-lint 358 포함) **0 failed · 2023 passed · 1 xfailed** (3525.11 s = 58:45 · rc 0) · strict smoke **rc 0** (191 s · "✅ pipeline smoke 통과" — 작은 grid/fit/score/restore 계산 포함, 연구용 새 실행 0) · 변이 재생 `-k g82` **12/12** — "실행한 변이 12건이 전부 기대 node 를 call 단계에서 물었다" (rc 0) · `--check-preimages -k g82` "모든 변이 지점이 정확히 한 번 나타난다". xfailed 1 = `test_gate63_defensive.py::test_staging_an_input_outside_the_repo_is_still_unsupported` (선언된 예상 실패 — 82차와 같음). 요청문 커밋의 docs-lint 는 발송문에 적는다 |

## §5 영수증 diff (2차 `02a776a7a0a3f4ba` ↔ 새 세대 `7187bd31740514d4`)

`make_receipt.py paired_fixed5_v4 grid_fit_v5` — 시작 HEAD = 끝 HEAD = `5313731c` · 시작 status 0 · rc 0 (2026-09-30T06:12:57Z → 06:14:55Z). paired ✅ 검사 35 · core `1eb98e213edb9f8b…` · grid ✅ 검사 34 · core `ee7c405a1495eff0…`.

| 필드 | paired_fixed5_v4 | grid_fit_v5 |
|---|---|---|
| `core_sha256` | `acbe8791… → 1eb98e21…` | `e7f3a624… → ee7c405a…` |
| `core.identity.validator_source_digest` | `02a776a7a0a3f4ba → 7187bd31740514d4` | 같음 |
| `core.identity.src_io_sha256` | `9c71bf42711ff184 → e0577ad8af02b0b3` | 같음 |
| `core.identity` 나머지 5 항 (producer cut) · `core.validation` (ok True · fail [] · **n_checks 35 · 34 불변**) · `bundle` · `outputs` · `restore` | 동일 | 동일 |
| stamp | `validator_commit 23670e58 → 5313731c` · 시각 · platform (`fc-v37 → fc-v50`) · `validator_tree_dirty` false | 같음 · dirty **true** (paired 파일을 먼저 쓴 뒤 grid — 세 세대와 같은 패턴) |

`LEG_PRESERVATION.yaml` (같은 커밋 `4307b6f8`): leg 마다 `verification_receipt_core_sha256` · `validator_identity.source_digest` 두 값 (n_checks 불변 · `leg_source_digest` 불변). 세대표 `CLAIM_STATUS.yaml::source_digest_generations` 에는 `7187bd31740514d4` 도 없다 — 라운드 2 의 일.

## §6 우리가 스스로 신고하는 것

| # | 신고 | 처리 · 판정 요청 |
|---|---|---|
| a | **N1 의 출처 선택** — 관측 noise realization 을 fits 가 아니라 `run_dir/_inputs/*_curves.parquet` (계획 curves sha 와 바이트 동일한 것) 에서 가져온다. fits 에 관측 seed 열을 새로 쓰는 방식은 택하지 않았다 (쓰는 쪽과 대조하는 쪽이 같은 파일이면 자기일관 위조를 못 본다 — N1 의 원래 모양) | 판정 요청: 이 출처가 닫힘 조건 "봉인 입력 또는 명시적으로 보존한 roster" 를 충족하는가 |
| b | **행 대조는 정확 비교** — truth 열을 `float(row) == float(curves)` 로 본다 (허용차 없음). 두 값 모두 같은 curves 바이트에서 `float(g[k].iloc[0])` 로 온다 (`fitting.py` task truth · parquet 왕복) | 허용차가 필요한 경로가 있으면 지적 요청 |
| c | **`check_design` 은 넓힌 채 그대로** — 설계 선언 문법 (`endian ∈ {little, big}` · 문자열) 은 좁히지 않고, 이 라운드의 실행 · 검증 경로 (envelope 봉인 · 시작 전 · validator) 에서 지원 profile 로 거부한다. 설계 digest (`pairing_design_sha256`) 는 미지원 선언에도 계산된다 | 판정 요청: 닫힘 조건 "실행 전 소비자와 validator 가 모두 검사" 로 충분한가, 선언 reader 도 좁혀야 하는가 |
| d | **envelope 검사가 봉인 단계에서 거부** — `check_envelope_v4` 에 profile 대조를 넣었으므로 `PlannedLegV4(bank.generator="philox")` 는 생성 자체가 `PreserveError("planned_seal")` 로 거부된다. 그래서 n2_03 (b) 는 봉인을 우회한 stub 계획으로 시작 전 검사의 도달을 따로 잰다 | 수용 여부 |
| e | **N3 는 v4 envelope 문법을 좁히지 않았다** — `planned-leg/v4` 계획이 `protocol_generation: v5` 를 선언하는 것 자체는 봉인 가능하고, v6 실행 (`_prepare_stage3`) 과 sig 6 validator 에서만 거부된다. 역사적 읽기 소급 금지 조건을 따른 선택 | 판정 요청: v4 envelope 자체를 v6 로 묶어야 하는가 (라운드 2 의 세대표 등록과 함께?) |
| f | **등록부 규칙 시험의 첫 실행 red (3 failed)** — 변이 EXPECT 를 붙인 뒤 규칙 시험을 **따로 돌린** 결과다 (82차 §8-m 교훈을 절차로 넣었다). 원인은 증인 끝 공백 3 개 — 정정 `6723b2ad` 뒤 합성 조각 rc 0, 최종 전체 회귀에 포함 | 절차 수용 여부 |
| g | **writer 인자 변경** — `write_execution_record` 의 `roster_sha256` 인자를 폐지했다 (주면 `TypeError`). 호출부는 production 한 곳뿐 (`_run_fit_locked`) | — |
| h | **계약 §1 줄번호 인용** 을 세 번째로 갱신 (1955 · 1910; 743-767 불변) — 라운드 1 때 §1 머리 갱신 기록에 적지 않았던 라운드 1 의 이동도 이번에 함께 적었다 | — |
| i | **이월 (82차 수용 · 이번에 손대지 않음)**: Q1 dead 정의 (`fitting.py:350`) · Q7 비유한 J 의 `returned` 계수 · 라운드 2 전체 | — |

## §7 리뷰어에게 묻는 것

| # | 질문 | 우리 제안 |
|---|---|---|
| Q1 | §1 로 G82-N1 · N2 · N3 가 닫혔는가 | 닫혔다고 본다 |
| Q2 | 라운드 1 (G81-N1·N2·N3 · 자체 점검 F1–F12 · G82 잔여) 종결 판정 | 종결 제안 — 종결되어도 라운드 2 는 별도 사용자 승인 |
| Q3 | §6-a 출처 · §6-c 선언 reader · §6-e v4 envelope 세대 문법 | 셋 다 현 상태 수용 제안 (c · e 는 라운드 2 의 세대 등록과 함께 다시 볼 수 있다) |
| Q4 | §5 새 세대 영수증 수용 | 수용 제안 (clean 커밋 · 2차본 바이트 보존 · 차이 = validator identity 2 항 · 검사 수 불변 · producer · outputs · restore 불변) |

## §8 다음 계획 (83차 회신 뒤)

1. 회신 접수 → 원장 §118 · 상태 문서.
2. 라운드 1 종결이면 라운드 2 범위 (82차 §9-Q5 제안 + 이번 §6-c · e) 를 사용자에게 **별도 승인** 요청 — 이번 요청은 그것을 묻지 않는다.
3. 실행 GO · 새 연구 leg 없음 · grid_fit_v5 진단 전용 유지.

## §9 발송 규칙

70차 §6 그대로. 발송 SHA · 검증 숫자는 발송문에 방금 실행한 출력으로만 적는다. 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.
