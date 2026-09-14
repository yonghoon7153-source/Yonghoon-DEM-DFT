# R5 라운드 원장 — 발견 통합 · 상태 · 순서 (대상 0cb7b7a, 2026-09-11)

> **다음 세션은 이 파일부터 읽는다.** 리뷰 원문: `R5_CODEX.md` (외부, NO-GO · P1 7 · P2 4). 보조 보고서 셋은
> `r5_repros/reports/` (분야별 번호 — 정본 번호는 `R5_CODEX.md` 의 R5-01~11).
> Codex 반례 재생: `python3 reviews/r5_repros/harness_r5_replay.py --target <0cb7b7a 의 bms-balancing 절대경로> --output /tmp/r5.json`
> — 대상 SHA 를 확인하므로 `git worktree add <dir> 0cb7b7a` 로 만든 트리에서 돈다. 우리 재생 기록:
> `r5_repros/replay_ours_0cb7b7a.json` (11 단계 rc 전부 Codex 기록과 같음 — **열한 건 전부 재현, 반박 성립 없음**).
> 수정 뒤에는 반례의 "잘못된 결과를 재현했다" assertion 이 **실패해야** 정상이다 (아래 ‘수정 뒤 재실행’).

판정: **NO-GO** (Codex) — "현재 정본을 그대로 새 모델 설계의 확정 근거로 채택" 에 대한 것. R4-01·03·S-02 와
R4-02/04/05/06/07 의 원래 반례는 종결 인정. 192 값·LAM 부호·폭 순위는 뒤집히지 않았다.

## 발견 (Codex 번호 그대로)

| ID | 무엇 | 상태 | 어디서 | 회귀 |
|---|---|---|---|---|
| R5-01 | `%g` 반올림 구간이 대칭 반 단위가 아니다 — `%.2g` 0 vs 0.049 · 10 vs 9.6 · 0.0001 vs 9.6e-05, `%.0g` 1 vs 4 가 complete·0 | **닫힘 (코드)** | `token_excess`: 토큰 구간을 **같은 형식으로 실제로 찍어서** 정한다(같은 문자열이면 자리수 안, 아니면 경계까지 이분법). audit 이 토큰을 선언 형식으로 다시 찍어 일치 확인. 전제: Python format = C/MATLAB printf 규칙 | `test_r5_01_*` (8 경우: 경계 안/밖 · 0 · 십진 경계 · 지수 경계 · `%.0g`) |
| R5-02 | 형식 선언 두 번(뒤가 이김)·숫자 아닌 알려진 앵커가 meta 로 새어 complete/partial | **닫힘 (코드)** | `dd_eval_csv_audit`: 역할은 값 변환 전에 이름으로 — 선언은 유효한 하나만, 알려진 앵커는 숫자 하나만(비유한은 비교기가 incomplete), 아니면 `invalid` | `test_r5_02_*` (중복 선언 · 무효+유효 선언 · broken 앵커 · broken 만 · 알려지지 않은 meta 허용) |
| R5-03 | 파라미터 열 이름을 바꿔도 위치만 보고 complete | **닫힘 (코드)** | audit: `header[:5] == PARAM_COLS` 아니면 `invalid` | `test_r5_03_*` |
| R5-04 | A 의 CSV 게시·id 검사 뒤 meta 쓰기 직전 B 가 CSV+meta 게시 → CSV=B · meta=A, 둘 다 OK | **닫힘 (코드)** | `publish_lock`(`<산출>.lock` flock): verify.py 게시(`atomic_write_csv`)·shell 의 degeneracy `mv`·`write_meta` 가 같은 잠금. meta 작성자는 잠금 안에서 id 를 **필드로 다시** 확인하고 bytes sha256 을 meta 에 적는다; 실패면 meta 를 쓰지 않는다. `provenance --verify-unit` 이 게시 뒤 묶음을 확인 | `test_r5_04_*` (Codex 와 같은 schedule: shell `python3` 함수로 A 의 meta heredoc 을 멈춤 → 최종 B/B 묶음, A 거부), `test_r4_06_concurrent_*` (barrier 를 잠금 앞으로 옮김) |
| R5-05 | `fitted_pair` 가 고른 untracked `matrix_100_v2.csv` 가 provenance 에 안 남음 (두 실행 meta 동일) | **닫힘 (코드)** | `fitted_pair_info` + meta `consumed_inputs`: 소비한 matrix 파일 경로·sha256·행(index/half_cell/si/w_dqdv/run_id), 반쪽전지·문헌 입력의 경로·sha256 — tracked 여부 무관 | `test_r5_05_*` |
| R5-06 | "50 개 모두 유한이면 같다" 는 충분조건 아님 — raw 1e-20 이면 +eps 로 22205 배 | **닫힘 (코드+정정)** | `_auto_scales` 감사에 `raw_lower_half_mean`·`scale`·`eps_rel`·`equivalent_within_rel`(유한·예외 없음·eps_rel ≤ `SCALE_EQUIV_REL` 1e-9 — 상대 근사); §1-13·§0-1·§0-2 정정 — 동치 조건은 새 감사 줄로만 확인 (U13) | `test_r5_06_*` |
| R5-07 | 새 `matrix` 실행이 Inf 표본을 세고도 행·stdout 에 안 남김 | **닫힘 (코드)** | matrix 행: `scale_*_target/ref` · `scale_audit_target/ref`(JSON) · `scale_seed` · `n_scale_samples`; 행 JSON 이 stdout 에도 찍힘 | `test_r5_07_*` (평탄부 forward: target·ref 둘 다 Inf 36/50 기록) |
| R5-08 (P2) | 기본 호출 한 번에 행 id 둘 + 로그 id 하나; grep 은 다른 칸의 문자열도 통과 | **닫힘 (코드)** | `main()` 이 파싱 직후 `args.run_id` 를 고정; `provenance.check_run_id`(CSV `run_id` 열 전 행 / JSON 필드)를 `run`·`write_meta` 가 쓴다 | `test_r5_08_*` |
| R5-09 (P2) | 16 줄은 4×4 식별자가 아님; 192 값 중 GITT·Li 는 96 값뿐 | **닫힘 (정정)** | §1-13: 증거 수준 "보고 순서의 16 줄(식별자 없음)", 96/192 범위, Kunz·step_005C 96 값 실측 밖; 감사 줄에 식별자(state·source·si·seed·n) 추가; `test_u12_*` 문구 한정 | `test_r5_docs_*`, `test_u12_*` |
| R5-10 (P2) | 둘째 항 예외 시 첫째 항 n=100 | **닫힘 (코드)** | 항별 try — 표본당 한 기록, `n_exception` 별도 | `test_r5_10_*` |
| R5-11 (P2) | 한글 산출물 경로가 따옴표·8진수로 찍혀 코드 수정으로 분류 | **닫힘 (코드)** | `git status --porcelain -z` 레코드(rename 은 원 경로 레코드 건너뜀) | `test_r5_11_*` |

Q1: 해석 못 하는 선언은 명시 옵션이 대체한다는 예외를 README 에 적었다. Q2: grep → 필드, 동시 실행은 잠금 안 "마지막 온전한 묶음" 정책. Q3: 요구서 항목(평탄부 dQ/dV 정의·단위·마스킹 후 유효 구간·zero/near-zero scale·NaN/Inf/예외 구분·소비한 scale·seed·표본 기록) §1-13 에. Q4: "코드 = commit" 과 "이 입력에서 이 결과" 를 별도 필드(`consumed_inputs`)로. Q5: §0-1 요약에 한정어; 다섯 관측은 R6 요청문 §4.

## 수정 뒤 재실행 (이 커밋, 우리 트리)

| 무엇 | 결과 |
|---|---|
| `python3 -m pytest tests/ -q` | 86 passed (R5 신규 11 · R3-05/U12/race 테스트 갱신) |
| `bash matlab/tests/run_all.sh` (Octave 없음 → 4·5 단계) | 전부 통과 |
| `harness_r5_port_repros.py --case …` | `sig2_*`·`sig0` 4 건 → `model_mismatch`, `duplicate_declaration`·`nonnumeric_anchor`·`duplicate_anchor_text`·`parameter_header_swap` 4 건 → `invalid` — 반례 assertion **실패**(= 닫힘); 양성 대조 3 건(경계 정상 반올림 · fixed10 밖 · 정확 일치) 통과 |
| `harness_r5_inference_repros.py --case exception / matrix` | n=100 · 감사 없음 assertion **실패** (= 닫힘). `epsilon`: 감사 dict 에 새 키가 붙어 그 비교에서 멈춤 — 22205 배 차이 자체는 사실이고 flag 로 표시하는 쪽을 택했다. `population`·`scope`: 통과 — population 은 증거 수준을 사본으로 한정한 결과(의도), scope 는 §0-2 의 **철회 인용문**이 옛 문장을 담고 있어 전체 텍스트 검색에 걸린다(살아 있는 §1-13 문장은 `test_r5_docs_*` 가 없음을 확인) |
| `harness_r5_claims_repros.py` | `quoted_path_roles`: git_dirty False → assertion **실패** (= 닫힘). `consumed_untracked_input`: 옛 다섯 필드는 여전히 같다(의도) — 닫힘은 새 `consumed_inputs` 필드, `test_r5_05_*` |
| `harness_r5_execution_repros.py` | `metadata_race`: A rc ≠ 0 → assertion **실패** (= 닫힘); 뒤 두 사례는 그 뒤라 안 돌았고 `test_r5_08_*` 이 덮는다 |
| RED 확인 | 신규 11 이 옛 코드·문서(0cb7b7a)에서 11 실패 — 이유 확인 |

## 닫는 순서 (실행 기록)

1. ~~재현~~ — worktree `0cb7b7a` 에서 11 단계 rc 일치
2. ~~RED~~ — 11 실패 확인
3. ~~코드~~ — `verify.py`(01·02·03·04·07·08) · `model.py`(06·10) · `provenance.py`(04·08·11) · `ne_shape.py`(05) · `run_states.sh`(04·08)
4. ~~문서~~ — FINDINGS §0-1·§0-2·§1-8·§1-13 · README ×2 · WORKING_STATE
5. ~~GREEN + 반례 재실행~~ — 위 표
6. ~~사용자 기계 (U13)~~ — 실측 완료 (`out/scale_audit_eval_u13.txt`, 18 줄): 전부 유한 · 예외 0 · eps_rel 4.7e-16~1.7e-15 · `equiv=1`; recompare 4 조합 포함. 루트 이름은 그 판 줄에 없어 보고 순서 — 다음 판부터 `root=` 를 붙이게 고침. `test_u13_*`.
7. R6 요청문 (`R6_REQUEST.md`)

## 유지되는 것 (Codex 가 종결로 인정한 것)

R4-01·03·S-02 · R4-02/04/05/06/07 원래 반례 · 192 값 경험적 일치 · LAM 부호 산술 · 폭 순위 · 12 normalization 행.
