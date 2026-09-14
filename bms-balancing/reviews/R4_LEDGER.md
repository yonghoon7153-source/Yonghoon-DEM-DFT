# R4 라운드 원장 — 발견 통합 · 상태 · 순서 (대상 39a5fe0, 2026-09-11)

> **다음 세션은 이 파일부터 읽는다.** 리뷰 원문: `R4_CODEX.md` (외부, NO-GO · P1 6 · P2 1). 보조 보고서 셋은
> `r4_repros/reports/` (분야별 번호 — 정본 번호는 `R4_CODEX.md` 의 R4-01~07).
> Codex 반례 재생: `python3 reviews/r4_repros/harness_r4_replay.py --target <39a5fe0 의 bms-balancing 절대경로> --output /tmp/r4.json`
> — 대상 SHA 를 확인하므로 `git worktree add <dir> 39a5fe0` 로 만든 트리에서 돈다. 우리 재생 기록:
> `r4_repros/replay_ours_39a5fe0.json` (12 단계 rc 전부 Codex 기록과 같음 — **일곱 건 전부 재현, 반박 성립 없음**).
> 수정 뒤에는 반례의 "잘못된 결과를 재현했다" assertion 이 **실패해야** 정상이다 (아래 ‘수정 뒤 재실행’).

판정: **NO-GO** (Codex) — "R3 의 다섯 GO 조건 전체 종결 + 현재 하네스 성공 판정의 무조건 채택" 에 대한 것.
R3-01·03(계산)·04·09 와 R3-05/07 의 원래 사례, R3-08 의 순차 사례는 종결로 인정했다. 관측·표·192값은 보존.

## 발견 (Codex 번호 그대로) + 보류 S-02~04

| ID | 무엇 | 상태 | 어디서 | 회귀 |
|---|---|---|---|---|
| R4-01 | `ne_shape` (c) 의 `>30 %` 갈래가 "블렌드가 이 음극의 모양이 아니다 · γ 를 어떻게 고르든 남고 · a_NE·b_NE 가 흡수한다 = 계통 편향" 출력 — 정확히 `Blend(x,0.5)` 인 곡선(선택 쌍 0.15→0.0, 68 %)에서도, 같은 실행의 (d) 가 γ=0.5 증인을 찾는데도 | **닫힘 (코드+철회)** | (c) 는 선택된 γ 에서의 max·rms·초과 비율만 말한다; §0-2 행 | `test_r4_01_ne_shape_c_branch_reports_statistics_not_a_universal_verdict` (>30 % fixture + 판정문 소스 검사) |
| R4-02 | 추정 정밀도가 complete·종료 0; `%.14g` 선언을 버리고 추정; 미지원 선언도 추정 | **닫힘 (코드)** | `resolve_precision`: 옵션 → 선언 → 추정. 추정은 `partial`(사유 "정밀도 추정", 종료 3)이고 `--allow-partial` 은 스키마 누락만 0 으로 만든다; `%.Ng` 는 유효 N 자리의 반 단위로 지원(`parse_precision_spec`, `cell_tol`); 해석 불가 선언은 `invalid`(종료 2); 옵션이 선언보다 느슨하면 `partial`(충돌 기록, Q3) | `test_r4_02_inferred_or_unsupported_precision_is_never_complete` (helper 4 경우 + 공개 경로 2 경우) |
| R4-03 | fixed 정밀도 허용량이 반올림 구간의 두 배(10⁻ᴺ 전체) — `%.10f` 0.0123456789 vs 0.01234567899, `%.1f` 0.1 vs 0.199 가 complete | **닫힘 (코드)** | `cell_tol`: 반 단위 0.5·10⁻ᴺ; 판정은 초과분/|p| 로 (자리수 안 / 수치 잡음 ≤1e-9 / 모델 차이) | `test_r4_03_fixed_precision_uses_half_unit_plus_numeric_noise` (10·1 자리 × 호환/비호환) |
| R4-04 | 중복 열(`rmse_pocv` 두 번, NaN)·중복 앵커 줄이 complete·expected=40 | **닫힘 (코드)** | `dd_eval_csv_audit`: 중복 앵커·중복 열·열 수 불일치·숫자 아닌 칸 → `invalid`(종료 2), 비교하지 않음 | `test_r4_04_duplicate_anchor_or_column_names_are_invalid` |
| R4-05 | §1-13 "Inf 는 안 나옴 · 빈-표본 가드 둘뿐" 이 성립하지 않음 — 평탄부 forward 에서 raw `rmse_dqdv` 50 중 36 Inf; 원본 설명식(NaN 만 제거) scale=Inf vs 포팅 유한 | **닫힘 (한정+감사+실측)** | §1-13: 동치를 **유한 RMSE 영역**으로 한정, 비유한 정책 차이 명시; `Objective.scale_audit`(n·유한·Inf·NaN) + `NONFINITE_SCALE_POLICY`; `eval` 의 `# scale_audit` 줄, degeneracy JSON `scale_audit`/`ref_scale_audit`. 실제 자료의 Inf 개수는 **U12** (사용자 기계 `eval` 네 루트) | `test_r4_05_auto_scale_records_its_nonfinite_policy_and_findings_limits_u1` |
| R4-06 | 공유 `.part` — A 가 B 의 행을 게시하고 rc 0, B 는 FileNotFoundError; Q4: 시각 도장은 `touch` 만 해도 OK | **닫힘 (코드)** | `atomic_write_csv`: 시도별 고유 임시 파일(`NamedTemporaryFile`) → `os.replace`; `run_id_of`: `--run-id`/`BMS_RUN_ID`/uuid 가 degeneracy JSON·matrix 행·profile 행에 박힘; `run_states.sh run`: 시도마다 id 를 만들어 명령에 주고 **파일 안에 그 id 가 있어야** OK (시각 도장 제거); `write_meta`: 같은 id 확인·기록, 없으면 거부 | `test_r4_06_concurrent_profiles_publish_their_own_rows_with_run_ids` (실제 두 process, barrier), `test_r4_06_run_helper_binds_the_artifact_to_the_attempt_not_to_mtime` (touch → FAIL, id → OK, write_meta 거부) |
| R4-07 (P2) | 코드 같은 채로 산출 둘을 차례로 재생성하면 두 번째 meta 가 dirty | **닫힘 (코드)** | `provenance.git_provenance`: 코드 dirty(산출 디렉터리 밖)와 `git_modified_outputs`(산출 디렉터리 안, 자신 제외)를 분리해 둘 다 기록 — `out/` 을 숨기지 않는다; `ne_shape`·`write_meta` 가 쓴다 | `test_r4_07_metadata_separates_code_dirty_from_modified_outputs`, S-01 테스트 갱신 |
| S-02 (보류→닫힘) | §5-2 "100·200 모두 크기도 방향도 다르다" — 100 은 같은 방향 (R4 Q2 도 지적) | **닫힘 (정정)** | §5-2: 100 방향 같음·크기 40 배, 200 반대; 300_0009 를 "γ_ref 고정 · 격자에서 증인 없음" 으로 | `test_r4_docs_direction_sentence_precision_order_and_line_endings` |
| S-03 (보류) | (a)(정규화 뒤, 용량 축 섞임) vs 가족 최대(순수 γ 축)의 차원 불일치 | **기록 유지** | Codex Q2 가 격자·정규화 한정어를 적절하다고 봤다 — §5-2 의 한정어 그대로; 용량 축을 뺀 (a) 재측정은 새 모델 요구서의 구분 시험 항목 | — |
| S-04 (보류) | 증인 최근접 하나만 기록, 가족 최대가 세 행 동일 | **열림 (개선 후보)** | Codex 가 요구하지 않음; §5-2 에 "반대쪽 도달 여부 미기록" 명시 | — |
| — | 리뷰어 Windows 사본에서 shell CRLF 구문 오류 | 닫힘 | `.gitattributes`: `*.sh`·`*.py` LF 고정 | 같은 docs 테스트 |

Q1(현재 자료로 더 가를 수 있나): 관측 유지·후보 가설 대응은 충분; SOC별 잔차·전처리 민감도·직접 제약 적합은 앞으로의 시험 → 요구서. 간격 균일성만으로 U2 를 닫지 않는다 (원시 timestamp·export 설정 필요) — U2 문구 갱신.
Q3: 실제 순서는 옵션 → 선언 → 추정 (README 정정). Q5: 정본 결론 5 는 범위를 붙인 다섯 행으로 요구서 관측 열에 옮긴다.

## 수정 뒤 재실행 (이 커밋, 우리 트리)

| 무엇 | 결과 |
|---|---|
| `python3 -m pytest tests/ -q` | 74 passed (R4 신규 9 + R3 테스트 4 개정 + S-01 갱신) |
| `bash matlab/tests/run_all.sh` (Octave 없음 → 4·5 단계) | 전부 통과 (bisect 시험은 `%.10f` 선언을 적어 선언 경로로) |
| `harness_r4_port_repros.py --target $PWD` | `inferred_precision_false_complete` 가 `model_mismatch`(partial 표시) 라 반례 assertion **실패** (= 닫힘) |
| `harness_r4_shape_repros.py --target $PWD` | 보편 판정 문구 없음 → assertion **실패** (= 닫힘) |
| `harness_r4_execution_repros.py --target $PWD` | `shared_profile_part`: B 도 rc 0, FileNotFoundError 없음 → assertion **실패** (= 닫힘) |
| `harness_r4_inference_repros.py --case plateau` | 그대로 재현 — 원본 설명식 Inf vs 포팅 유한의 **차이 자체**는 사실이고, 우리는 정책을 맞추는 대신 영역을 한정하고 감사를 남기는 쪽(R4-05 최소 조건 중 전자)을 택했다 |
| RED 확인 | 신규 9 + 개정 3 이 옛 코드·문서(d945402)에서 12 실패 — 이유 확인(complete on inferred, 종료 0, touch OK, 보편 판정, g14/fixed10 complete, 중복 complete, scale_audit 없음, B rc 1, 두 번째 meta dirty, 문서) |

## 닫는 순서 (실행 기록)

1. ~~재현~~ — worktree `39a5fe0` 에서 12 단계 rc 일치
2. ~~RED~~ — 12 실패 확인
3. ~~코드~~ — `verify.py`(02·03·04·06) · `model.py`(05) · `ne_shape.py`(01·07) · `provenance.py`(07) · `run_states.sh`(06·07) · `.gitattributes`
4. ~~문서~~ — FINDINGS §0-2·§1-8·§1-13·§5-2 · README ×2 · WORKING_STATE
5. ~~GREEN + 반례 재실행~~ — 위 표
6. ~~사용자 기계 (U12)~~ — 실측 완료: 4 루트 × 4 상태 16 build 전부 Inf 0 · NaN 0 (`out/scale_audit_eval.txt`, GITT · Li · seed 0 범위). §1-13 에 범위 붙여 닫음; `test_u12_*`. `eval --out` 도 감사 줄을 파일에 남기게 고침.
7. R5 요청문 (`R5_REQUEST.md`)

## 유지되는 것 (Codex 가 종결로 인정한 것)

R3-01 철회 · R3-03 계산(격자 한정) · R3-04 · R3-05/07 원래 사례 · R3-08 순차 사례 · R3-09 · 12 normalization 행 정확 일치 · 192 값 4.04e-12.
