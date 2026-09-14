# α·β 검증 하네스 R5 — Codex 리뷰

## 판정

**NO-GO — 현재 정본을 그대로 새 모델 설계의 확정 근거로 채택하는 것에 대한 판정이다.**

R4 수정은 실제로 효과가 있다. 그러나 비교기는 다른 숫자·다른 이름의 parameter를 complete로 처리하며, 동시 실행의 결과 파일과 출처 기록이 서로 다른 시도에 속할 수 있다. 새 scale 감사에도 동치 조건·실제 게시 경로·증거 범위의 문제가 남았다.

**P1 7건, P2 4건**으로 묶었다. 예전 반례나 신고된 U 한계의 존재를 다시 센 것이 아니다. R5-09의 두 사례는 같은 U12 증거 범위 문제로 묶었다. 보조 보고서의 분야별 번호·심각도 제안과 다를 때 이 문서가 최종 분류다.

이 판정은 “새 모델 요구서 초안을 쓰지 말라”가 아니다. **관측 → 후보 원인 → 구분 시험 → 채택 기준 → 한계**를 구별한 초안 작성은 진행해도 된다. 기존 192값의 경험적 일치·LAM 부호·폭 순위가 이번 반례로 뒤집혔다는 판정도 아니다.

## 1. 대상과 실행 증거

- 대상: `claude/bms-alpha-beta-verify`, **`0cb7b7a380a90f61c1f25cabcb28204749b88076`**.
- 요청문: [R5_REQUEST.md](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/reviews/R5_REQUEST.md). R4 본체 `274f1f8` 및 뒤에 추가된 U12 실측/회귀까지 포함했다.
- 범위: `bms-balancing/`만. 별도 checkout 사용, 실행 전후 tracked status 모두 빈 문자열.
- Python 3.12.3 / NumPy 2.5.3 / SciPy 1.18.1 / pandas 3.0.5 / openpyxl 3.1.5 / pytest 9.1.1.
- 비공개 원자료·원본 MATLAB·Octave는 실행하지 않았다. 대체한 수치 입력·최적화는 각 스크립트에 명시했다. parser, 비교/종료 코드, 감사 산술, 결과 게시, 메타데이터 함수는 대상 코드로 실행했다.

| 검사 | 이 환경의 관측 |
|---|---|
| 전체 pytest | **75 passed in 15.19s**, rc 0 |
| 요청문 74와의 차이 | 최신 `0cb7b7a`가 U12 회귀 1개를 추가했다. 74는 갱신 전 수치 |
| MATLAB 측 검사 스크립트 | **4·5단계 통과**, rc 0. Octave 부재로 **1–3단계 미실행** |
| 네 루트 `compare_states` | rc 0 |
| 옛 R4 port / shape / execution | 각각 rc 1, 요청문이 예고한 첫 assertion에서 멈춤 |
| 옛 R4 plateau | rc 0, 비유한 정책 차이 자체는 그대로 재현 |
| 새 R5 port | 합성 30사례, helper와 별도 CLI dispatcher의 기대 결과 모두 확인 |
| 새 R5 inference / claims / execution | 모두 rc 0, 아래 반례와 양성 대조 재현 |
| 통합 재생 | **11단계 전부 기대 rc와 일치** |

스크립트의 rc 0은 **반례/대조군의 예상 결과를 관측했다**는 뜻이지 하네스 GO가 아니다. 옛 스크립트가 첫 assertion에서 실패했다고 그 뒤 모든 축까지 닫혔다고 세지 않았다. 새 대조군으로 따로 확인했다.

전문: [실행 기록 JSON](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_replay_results.json).

### 재생

ZIP을 별도 디렉터리에 풀고 변수만 자신의 경로로 지정한다. Linux/WSL과 대상 requirements 및 pytest가 필요하다. 검토 대상 소스는 수정하지 않는다.

```bash
TARGET=/absolute/path/to/checkout/bms-balancing
REVIEW=/absolute/path/to/unzipped-review
python "$REVIEW/harness_r5_replay.py" \
  --target "$TARGET" --output "$REVIEW/replayed.json"
```

## 2. 새 P1 — GO 전에 닫거나 지원 범위를 명시적으로 제외할 조건

### R5-01 [P1 · 수치 비교] `%g`의 반올림 구간이 실제 출력과 다르다

위치: [verify.py:720](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:720), [cell_tol:732](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:732).

`cell_tol`은 출력값의 지수로 **대칭** 반폭을 계산한다. 10의 거듭제곱으로 올라가는 경계의 아래쪽은 다른 자릿수에서 반올림된다. 출력 0에 임의의 절대 폭을 주는 것도 `%g`의 유효숫자 규칙이 아니다. `%.0g`는 한 자리로 정규화되지 않는다.

| 선언·CSV 값 | Python 값 | 그 값을 같은 형식으로 출력 | 실제 판정 |
|---|---:|---|---|
| `%.2g`, `0` | .049 | `0.049` | **complete, rc 0** |
| `%.2g`, `10` | 9.6 | `9.6` | **complete, rc 0** |
| `%.2g`, `.0001` | .000096 | `9.6e-05` | **complete, rc 0** |
| `%.0g`, `1` | 4 | `4` | **complete, rc 0** |

첫 사례는 상대차 100%, 두 번째는 4.1667%다. 비교기는 이를 `worst_rel=0`인 “자리수 안”으로 지운다. 실제 유효 반올림인 9.96 → `10`은 정상 대조에서 통과했다.

```bash
python "$REVIEW/harness_r5_port_repros.py" --target "$TARGET" --case sig2_zero_false_complete
python "$REVIEW/harness_r5_port_repros.py" --target "$TARGET" --case sig2_decade_false_complete
```

**최소 조건:** 지원 `%g` 토큰이 나올 수 있는 실제 반올림 구간을 검증하고 수치 잡음 허용량을 따로 적용한다. 영점·양/음 지수 경계·올림 전후를 각각 회귀로 고정한다. 구현 전에는 문제가 있는 형식을 complete 지원에서 제외해도 된다. 기존 fixed 반 단위 수정은 유지한다.

### R5-02 [P1 · schema/정밀도] 중복 선언과 잘못된 앵커가 파싱 중 사라진다

위치: [dd_eval_csv_audit:569](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:569), [read_dd_eval_meta:671](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:671).

audit은 숫자로 변환되는 주석만 앵커로 센다. 변환 실패는 metadata라고 간주해 건너뛰며, metadata dict는 같은 이름을 마지막 값으로 덮는다.

- 선언 하나 `%.17g`, CSV .1 vs Python .149: 정상 대조 **model_mismatch/1**.
- 같은 파일에 `# printed_format,%.1f` 추가: **complete/0**, `precision_conflict=False`.
- 정상 `# E_PE_0p5,1`과 `# E_PE_0p5,broken`을 함께 둠: **complete/0**.
- 정상 앵커를 `broken`으로 바꾸고 `--allow-partial`: malformed가 아니라 “누락”이 되어 **partial/0**.

```bash
python "$REVIEW/harness_r5_port_repros.py" --target "$TARGET" --case duplicate_declaration_false_complete
python "$REVIEW/harness_r5_port_repros.py" --target "$TARGET" --case nonnumeric_anchor_allowed_as_legacy
```

**최소 조건:** 값 변환 전에 이름으로 역할과 등장 횟수를 확정한다. 형식 선언은 유효한 하나만, 알려진 앵커는 유한 숫자 하나만 허용한다. 잘못 존재하는 필드는 실제 legacy 누락과 구별하여 invalid/2가 되어야 한다. 기존 숫자/NaN 중복 거부는 양성 대조에서 작동했다.

### R5-03 [P1 · 같은 입력의 결속] parameter 이름을 바꿔도 same-p로 인증한다

위치: [헤더 audit:578](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:578), [parameter 대조:1018](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:1018).

정상 CSV의 `b_PE`와 `b_NE` **헤더 이름만** 바꾸고 숫자는 그대로 둔다.

| 좌표 | Python 정본 p | CSV 헤더가 뜻하는 p |
|---|---:|---:|
| b_PE | −.022949 | .000309 |
| b_NE | .000309 | −.022949 |

모든 이름이 유일하고 행 폭이 같아 audit이 통과한다. p 대조는 첫 다섯 숫자의 **위치**만 보므로 앵커 16/16·RMSE 32/32, **complete/0**이다.

```bash
python "$REVIEW/harness_r5_port_repros.py" --target "$TARGET" --case parameter_header_swap_false_complete
```

**최소 조건:** 첫 다섯 이름/순서를 정확히 제한하거나 이름으로 재배열해서 p를 비교한다. 이 fixture는 어느 정책에서도 complete여서는 안 된다. 시험의 목적함수는 합성값이며, 서로 다른 실제 battery parameter의 목적함수가 같다는 주장이 아니다.

### R5-04 [P1 · 결과 소유] 두 실행 모두 성공하고 결과=B, 메타데이터=A가 남는다

위치: [run_states.sh:40](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/run_states.sh:40), [메타데이터 쓰기:52](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/run_states.sh:52), [profile 호출부:169](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/run_states.sh:169).

실제 profile CLI 두 개를 합성 성공 적합으로 돌렸다. 실제 `run`·`write_meta` 함수를 그대로 사용하고 A의 metadata Python 실행만 **grep 성공 직후**에 잠시 멈췄다.

1. A가 자기 CSV를 게시하고 A ID 검사를 통과.
2. A는 메타데이터 쓰기 직전에 대기.
3. B가 자기 CSV와 B 메타데이터를 게시하고 성공.
4. A가 재개해 A 메타데이터로 덮고 성공.

```text
A rc = 0, a_NE = 1.1
B rc = 0, a_NE = 1.3
최종 CSV run_id = B
최종 .meta.json run_id = A
두 wrapper 모두 OK
```

```bash
python "$REVIEW/harness_r5_execution_repros.py" --target "$TARGET"
```

**왜 못 막는가:** CSV 고유 임시파일은 올바르게 고쳐졌다. 그러나 CSV와 별도 metadata의 게시가 하나의 시도로 묶이지 않는다. `grep` 이후 다른 실행이 파일을 교체할 수 있고, metadata writer는 이미 읽은 ID로 pathname 옆에 기록한다.

**최소 조건:** 마지막 쓰기 허용 정책을 유지하려면 결과+metadata를 같은 불변 실행 단위로 만들고 그 단위를 게시한다. 또는 모든 writer가 지키는 직렬화 범위 안에서 검증·결과 게시·metadata 게시를 끝낸다. reader도 두 ID/해시 불일치를 성공으로 소비하지 않아야 한다. 최종 재검사 한 번만 추가하면 그 다음 창이 남는다.

동시 실행을 무조건 금지할 필요는 없다. “마지막 실행의 온전한 한 묶음이 남는다”면 된다. 현재 반례는 단순 last-writer-wins가 아니라 두 시도의 혼합이다.

### R5-05 [P1 · 소비 입력의 출처] 실제 선택한 새 matrix가 provenance에 전혀 남지 않는다

위치: [ne_shape.py:84](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/ne_shape.py:84), [출처 기록:138](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/ne_shape.py:138), [provenance.py:57](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/provenance.py:57).

`fitted_pair`는 `matrix_<state>*.csv`를 역순으로 고른다. 새 untracked `matrix_100_v2.csv`도 실제 입력이 된다. 하지만 git 출처는 untracked를 빼고, `gamma_from`은 선택된 파일 대신 포괄적인 경로 설명을 남긴다.

합성 전극 입력에서 실제 `fitted_pair → main → CSV/meta writer`를 실행했다.

| 상태 | 소비 입력 | γ_target | 진폭비 b/a |
|---|---|---:|---:|
| 전 | tracked `matrix_100.csv` | .16 | .032960 |
| 후 | 새 untracked `matrix_100_v2.csv` | .45 | 1.000000 |

두 metadata의 `git_commit`, `git_dirty=False`, `git_modified_code=[]`, `git_modified_outputs=[]`, `gamma_from`이 **모두 동일**했다. 값은 출력에 남지만 그 값을 공급한 정확한 입력 파일의 identity가 없다.

```bash
python "$REVIEW/harness_r5_claims_repros.py" --target "$TARGET"
```

**최소 조건:** 코드 dirty와 입력 provenance를 분리한다. 실제 소비 파일의 경로·내용 해시·선택한 행/역할을 tracked 여부와 무관하게 결과에 남긴다. 이미 읽은 데이터에서 이 정보를 함께 전달한다. 모든 untracked를 코드 dirty로 돌리는 수정은 필요하지 않다. tracked matrix 수정이 `git_modified_outputs`에 나타나는 R4-07 대조는 통과했다.

### R5-06 [P1 · 동치 조건] “50개 모두 유한하면 같다”는 충분조건이 아니다

위치: [model.py:431](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/model.py:431), [FINDINGS.md:934](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/FINDINGS.md:934), [새 한정:939](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/FINDINGS.md:939).

**eps 가드의 존재 자체는 이미 신고됐다.** 새 반례는 그 가드가 있는 상태를 포함하면서 “모두 유한”을 동치의 충분조건으로 삼은 것이다. 절대 eps의 상대 영향은 `eps / lower_half_mean`이며, 유한성은 양의 하한을 주지 않는다.

모든 raw RMSE가 양수 유한 `1e-20`인 합성 Objective에서 실제 `_auto_scales`와 `__call__`을 실행했다. 비교하는 원본은 정본에 기재된 하위절반 평균 식이지 독립 실행한 MATLAB이 아니다.

```text
세 항 감사: n=50, finite=50, Inf=0, NaN=0
문서의 원본 설명식 scale = 1e-20
포팅 scale = 2.2205460492503133e-16
비율 = 22205.460492503134
동일 point objective: 원본 설명식 3.0 / 포팅 0.00013510190437225297
```

```bash
python "$REVIEW/harness_r5_inference_repros.py" --target "$TARGET" --case epsilon
```

**최소 조건:** 정확 동치와 허용오차 내 근사를 구분한다. raw 평균·최종 scale·eps 상대 영향을 남기고, 양의 평균과 허용 상대오차 조건을 함께 검사하거나 작은/0 scale 정책을 별도로 선언한다. 기존 셀의 scale이 이 정도로 작다는 주장은 아니다. 16개 감사 줄의 개수만으로 실제 scale 크기는 알 수 없다.

### R5-07 [P1 · 감사의 실행 배선] 새 matrix 실행은 비유한 표본을 세고도 기록하지 않는다

위치: [FINDINGS.md:948](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/FINDINGS.md:948), [build 호출:1157](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:1157), [행 게시:1170](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:1170).

정본은 미측정 소스 조합의 Inf 여부를 새 `matrix`/`eval`의 감사 줄로 보라고 한다. 그러나 matrix 행과 stdout에는 scale/audit가 없다.

실제 `cmd_matrix`를 실행했다. 입력 존재와 최적화만 빠른 대역으로 대체했고, Objective는 기존 R4 평탄부 forward와 실제 `_auto_scales`를 사용했다.

```text
w_dqdv = 1.0
reference dqdv Inf = 36 / 50
target dqdv Inf = 36 / 50
게시 CSV = 1행
stdout scale_audit 없음
CSV scale/audit 필드 없음
```

```bash
python "$REVIEW/harness_r5_inference_repros.py" --target "$TARGET" --case matrix
```

**최소 조건:** matrix 결과에도 reference/target 각각의 사용 scale·audit·정책·seed·표본 수를 실어 영역 밖 결과를 식별할 수 있게 한다. 비유한 결과를 무조건 거부할 필요는 없다. 양쪽을 독립적으로 비유한으로 만드는 회귀가 각 산출 기록을 검사해야 한다. eval/degeneracy의 새 감사 배선은 인정한다.

## 3. 새 P2 — 범위·기록 정확성

### R5-08 [P2 · run ID 계약] 기본 호출 한 번에 세 ID, 검증은 필드가 아닌 문자열 검색

위치: [run_id_of:40](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:40), [profile 행:1329](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:1329), [완료 문구:1365](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/verify.py:1365), [ID 검사:111](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/run_states.sh:111).

`--run-id`와 환경변수를 주지 않고 2행짜리 실제 profile을 실행하면 **행 ID 둘과 완료 로그 ID가 모두 다르다**. UUID를 호출마다 새로 만들기 때문이다. 명시 환경 ID를 준 정상 대조는 하나로 유지됐다.

또 합성 CSV의 `run_id=previous-attempt`, 별도 `note=이번 UUID`로 `run → write_meta`를 호출하면 **rc 0**으로 새 meta가 붙는다. 현재 optimizer가 이런 note를 낸다는 주장이 아니라, Q2의 “파일 안에 grep으로 있으면 충분한가”에 대한 직접 대조다.

재현: `harness_r5_execution_repros.py`의 `default_attempt_ids`, `membership_not_schema`.

**최소 조건:** command 시작 시 ID 하나를 고정하고 모든 행/JSON/로그에 재사용한다. CSV/JSON을 파싱하여 해당 역할의 ID가 전부 같은지 검증한다. 다른 필드의 문자열은 증거가 아니다. 이 수정만으로 R5-04의 두 파일 게시 경주까지 닫히지는 않는다.

### R5-09 [P2 · U12 증거 범위] 16줄은 4×4 식별자가 아니며, 192값 전체도 그 설정 안이 아니다

위치: [scale_audit_eval.txt:3](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/out/scale_audit_eval.txt:3), [U12 회귀:2462](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/tests/test_review_findings.py:2462), [FINDINGS.md:946](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/FINDINGS.md:946).

- 실제 U12 회귀에 임시 사본을 주었다. **한 감사 record를 16번 복제**하고 머리에 “4×4 전수가 아니다”라고 적어도 PASS. Inf 하나를 넣는 대조는 FAIL. 숫자는 검사하지만 실행 구성 집합은 검사하지 않는다.
- 네 recompare CSV의 실제 헤더를 읽으면 GITT·Li 두 조합은 96값, **Kunz와 step_005C는 나머지 96값**이다. U12의 GITT·Li 설정이 §1-8 전체 192값을 포함한다는 연결은 틀리다.

```bash
python "$REVIEW/harness_r5_inference_repros.py" --target "$TARGET" --case population
python "$REVIEW/harness_r5_inference_repros.py" --target "$TARGET" --case scope
```

사용자가 16 build를 실행하지 않았다는 증거가 아니다. 보존 파일 자체도 각 줄에서 식별자를 뺐다고 신고한다. **“사용자 보고 순서의 16개 감사 줄”**은 인정할 수 있지만 **“회귀가 4×4 전수를 확인”**했다고 확대하지 않는다.

**최소 조건:** 기존 사본은 이 증거 수준으로 한정한다. 다음 감사에는 안정 root label·state·source·Si·seed·표본 수를 붙여 기대 tuple 집합의 중복/누락을 검사한다. 192값의 경험적 일치는 그대로 두고, scale 감사가 모든 조합을 덮는다는 연결만 정정한다. 이 정정을 위해 비공개 재실행을 반드시 요구하는 것은 아니다.

### R5-10 [P2 · 감사 개수] 둘째 metric에서 예외가 나면 첫째 표본 수가 100이 된다

위치: [model.py:413](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/bms_balancing/model.py:413).

`rmse_pocv=1` 반환 뒤 `rmse_dvdq`가 예외를 내도록 50회 실행했다. 실제 pocv 호출은 50회인데 감사는 **n=100, finite=50, NaN=50**이다. 앞에서 append한 값을 둔 채 catch가 세 배열에 NaN을 다시 넣는다.

```bash
python "$REVIEW/harness_r5_inference_repros.py" --target "$TARGET" --case exception
```

**최소 조건:** 한 표본에서 각 metric에 정확히 한 기록만 추가한다. 시도 횟수·실제 metric 평가 횟수·예외 개수를 구별한다. 이 반례는 all-finite를 거짓 통과시키지는 않으므로 P2다.

### R5-11 [P2 · 출처 분류] Git이 따옴표로 표시한 한글 산출물을 코드 수정으로 센다

위치: [provenance.py:74](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/provenance.py:74).

정상 Git 기본 quoted-path 설정에서 tracked `out/측정.csv` 값만 바꾸었다. 실제 `git_provenance`는 `git_dirty=True`, `git_modified_outputs=[]`를 내고, escaped/quoted 문자열을 `git_modified_code`에 넣었다. ASCII 출력 대조는 의도대로 분리됐다.

재현: `harness_r5_claims_repros.py`의 `quoted_path_roles`.

**최소 조건:** `git status --porcelain -z` 등의 구조화된 경로 레코드를 사용하고 rename 레코드도 그 형식대로 해석한다. 사람이 읽는 quoted 문자열을 실제 pathname으로 붙이지 않는다.

## 4. R4 대응과 R3 §5의 GO 조건 재판정

| R4 항목 | 이번 판정 | 근거 |
|---|---|---|
| 01 `(c)>30%` 보편 부적합 결론 | **닫힘** | 실제 Blend 가족원·68% fixture에서 옛 보편 문구가 나오지 않음 |
| 02 추정/g14/미지원 선언 complete | **원래 반례 닫힘, 전체 부분** | 추정3·g14 차이1·미지원2; 새 sig/선언 경계는 R5-01·02 |
| 03 fixed 두 배 허용폭 | **닫힘** | `.01234567894` 허용 / `…899` 불일치, 실제 CLI 확인 |
| 04 숫자/NaN 중복 열·앵커 | **원래 반례 닫힘, 전체 부분** | invalid2/비교0; 비숫자 역할·parameter 이름은 R5-02·03 |
| 05 비유한 정책 동치 주장 | **철회·감사 인정, 종결 부분** | plateau Inf36을 정확히 셈; 충분조건·matrix 배선은 R5-06·07 |
| 06 공유 CSV 임시파일/touch | **원래 반례 닫힘, 결과 결속 부분** | 고유 임시파일로 두 publisher 성공·touch 거부; metadata 혼합 R5-04 |
| 07 연속 재생성 dirty 오분류 | **원래 순서 닫힘, 역할 분리 부분** | tracked 출력과 코드 대조 통과; 새 소비 입력/quoted 경계 R5-05·11 |
| S-02 방향/크기 | **닫힘** | 100 같은 방향·약40배, 200 반대, 고정ref·501×400 표집 한정 확인 |

| R3 §5 최소 조건 | R5 판정 | 한 줄 근거 |
|---|---|---|
| 1 원인·표현 주장 | **주요 철회 닫힘 / 정본 범위는 부분** | γ/원인 과장은 좁혀짐. scale 동치 충분조건과 U12 범위 정정 필요 |
| 2 표의 identity | **닫힘 유지** | 대상/기준 분모·소스·집합 정정 회귀 통과 |
| 3 비교 성공 조건 | **부분** | 정상·기존 실패 대조는 통과하지만 R5-01~03이 complete/0 |
| 4 실행 결과 소유 | **부분** | 옛 CSV 재사용 방어는 작동, 결과·metadata·소비 입력 결속은 남음 |
| 5 기록을 지키는 시험 | **192값 조건은 닫힘 유지** | 원시 수치 재대조 회귀 통과; 새 U12 구성 회귀는 별개로 R5-09 |

U2·U3·U4~U10·S-04 등을 미구현이라는 이유만으로 새 발견에 올리지 않았다. S-03의 용량 축 혼합도 신고된 구분 시험으로 유지한다.

## 5. 질문에 대한 답

**Q1 — 정밀도 정책:** 추정=partial3, 느슨한 override=partial3라는 방향은 적정하고 대조군에서 집행된다. 하지만 `%g` 역상과 선언/앵커 역할을 닫기 전에는 “완전한 지원 범위만 0”이 아니다. 또한 **명시 옵션이 없는 경우**에만 미지원 선언=invalid다. `--precision g17`이 있으면 미지원 선언을 대체하고 complete가 될 수 있으므로 문구에 그 예외를 붙인다.

**Q2 — grep과 동시 실행:** grep만으로 충분하지 않다(R5-08). 동시 실행 자체를 금지할 필요도 없다. ID가 일치하는 결과+metadata 한 묶음을 게시해야 한다(R5-04). 고유 CSV 임시파일 수정은 필요한 부분을 실제로 고쳤다.

**Q3 — 비유한 정책을 원본과 달리 유지:** 가능하다. 정확 동치·허용오차 근사·다른 정책 적용을 구별하면 된다. 새 모델에는 plateau/작은 slope의 역도함수 정의, 단위, 마스킹 후 유효 구간, zero/near-zero scale, NaN/Inf/exception의 구분, 실제 소비한 scale·seed·sample 조건의 기록을 넣는다. 유한 개수만으로 동치를 판단하지 않는다.

**Q4 — 입력 artifact 역할:** `git_modified_outputs`는 변경 목록이지 실제 소비 입력 목록이 아니다. tracked 입력 변경 대조만으로 충분하지 않다(R5-05). “코드는 commit과 같음”과 “이 데이터에서 이 결과가 나옴”을 별도 필드로 기록한다. 입력 해시를 위해 비공개 원자료 자체를 공개할 필요는 없다.

**Q5 — 다섯 관측을 요구서로 옮겨도 되는가:** **한정어를 함께 옮기면 초안의 관측 열로 사용할 수 있다.**

1. 포팅: 192값의 경험적 일치 / 사용자 원본 함수 대조 기록 / 신고된 16-build 감사는 서로 다른 증거다. 마지막 것이 모든 조합·모든 유한 scale의 동치를 보장하지 않는다.
2. 음수 LAM_NE: 공개 5행·고정 기준의 부호 산술로 유지. 경계 변경의 인과로 옮기지 않는다.
3. 파우치 폭: 해당 네 상태·설정의 탐색 하한 순위. 식별성·정확도 보장으로 옮기지 않는다.
4. 원통형/PE 대조: 명시한 소스 집합·분모·통계량의 기술값으로 유지한다.
5. 잔차/γ: 선택된 쌍의 진폭 및 고정ref 표집 증인이지 원인이나 모양 적합의 증명이 아니다.

(d) 증인에 관한 새 출력 문구도 정리하는 것이 좋다. 같은 진폭·같은 γ=.5 증인을 가진 두 합성 측정에 대해 한쪽의 격자 최소 max잔차는 0, 다른 쪽은 60.6453mV였다. **진폭 존재 증인은 다른 γ의 모양 잔차 판정이 아니다.** 이는 신고된 U9/S-04와 연결되는 설명 개선으로만 남기며 새 P1로 세지 않았다. 문서 초반의 무조건적 “MATLAB과 같다” 요약에도 뒤 절의 한정을 함께 붙인다.

## 6. 최소 다음 작업과 최종 판정

큰 실험을 먼저 돌리기보다 다음 경계를 작게 닫는 순서가 맞다.

1. R5-01~03: 지원 정밀도·선언·앵커·parameter 역할의 성공 조건을 통일한다.
2. R5-04·05·08: 실행 ID 하나, 실제 소비 입력, 결과+metadata 한 묶음을 연결한다.
3. R5-06·07: scale의 수치 동치 조건을 바로잡고 matrix가 실제 audit를 내보내게 한다.
4. R5-09~11: U12 증거 수준/범위, 감사 개수, 경로 분류를 정정한다. 문서 한정으로 해결할 수 있는 부분은 그렇게 처리한다.

**최종 NO-GO.** 다만 위 범위를 명시한 새 모델 설계 요구서 초안은 지금 진행 가능하다. 하네스의 일반 성공 판정이나 특정 새 전극 표현의 필요성을 이미 입증된 사실로 전제해서는 안 된다.

## 파일 구성

- [통합 재생](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_replay.py) / [실행 출력 전문](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_replay_results.json)
- [비교 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_port_repros.py) / [수치·감사 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_inference_repros.py)
- [입력·주장 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_claims_repros.py) / [실행·metadata 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_execution_repros.py)
- 독립 담당 보고서 3개를 ZIP에 포함했다. 최종 번호와 판정은 이 보고서를 따른다.

