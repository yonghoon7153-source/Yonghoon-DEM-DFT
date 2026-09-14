# R5 독립 수치·추론 검토

대상: `0cb7b7a380a90f61c1f25cabcb28204749b88076`, `work/harness-r5-target/bms-balancing/`.
`reviews/R5_REQUEST.md` 전체를 먼저 읽었다. 대상 파일은 변경하지 않았다.

범위: R4-05의 유한 영역 한정, `Objective.scale_audit`, U12 증거 집합·배선, Q3/Q5.
원자료와 원본 MATLAB은 실행하지 않았다. 아래 합성 반례는 실물 셀의 값/원인이 틀렸다는 증명이 아니다.

## 실행 결과

```sh
cd /path/to/bms-balancing
PYTHONPATH=/path/to/pytest-deps python /path/to/harness_r5_inference_repros.py
```

Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1. 전체 rc 0, `R5_INFERENCE_REPRO_ASSERTIONS_PASSED`.
각각 `--case closure|population|scope|matrix|exception|epsilon`으로 분리 실행할 수 있다.

양성 확인:

- 실제 R4-05·U12·192값 회귀 3개가 통과했다.
- 기존 평탄부 합성례의 50개 표본이 유한 14 / Inf 36 / NaN 0이라고 **새 감사가 정확히 기록**한다. R4의 "Inf를 못 본다"는 문제는 그 경로에서 닫혔다.
- 보존된 192값의 원시값 재대조 회귀도 통과했다. 아래 문제는 그 경험적 일치 자체를 뒤집지 않는다.
- 이전 R3-01/R3-04의 수치·범위 회귀와 두 음성 대조를 현행 트리에서 다시 실행했다. 12개의 matrix/degeneracy pair에서 best/ref parameter·objective가 일치했다. 대상 RMSE 분모의 최대비는 2.8533359, pristine 분모는 4.9882666; 각 집합은 6개씩이다. 파우치 `300/100`은 0.7745144, c168은 1.6029171, c171은 1.5240354. 원인 주장이 아니라 해당 집합의 기술값이라는 R4 정정은 유지된다.

## I-01 — 새 유한 영역 조건은 `+eps`의 상대 오차를 제한하지 않는다

제안 심각도: **P1(동치 조건)**. 실제 셀 계산이 틀렸다는 판정이 아니라, 새로 제시한 충분조건의 반례다.

위치:

- `bms_balancing/model.py:431`: 하위 절반 평균에 절대 `np.finfo(float).eps`를 더한다.
- `bms_balancing/model.py:392`: Inf 0이면 그 실행에서 동치라고 적는다.
- `FINDINGS.md:934`: 이 항의 상대 차이를 `1e-16`이라 일반화한다.
- `FINDINGS.md:939`, `:946`: 50개 전부 유한이라는 조건으로 scale 동치를 주장한다.

재현: `--case epsilon`. 세 raw RMSE가 각 표본에서 양수 유한 `1e-20`인 합성 `Objective`에 **현행 `_auto_scales(0,50)`과 `__call__`**을 실행한다. 비교하는 원본은 §1-13에 적힌 `NaN 제거 → 정렬 → 하위 절반 평균`이라는 식이며, 비공개 MATLAB을 독립 실행한 것이 아니다.

관측:

```text
세 항 모두 n=50, finite=50, Inf=0, NaN=0
문서의 원본 설명식 평균 = 1e-20
현행 scale = 2.2205460492503133e-16
scale 비율 = 22205.460492503134
동일 point objective = 원본 설명식 3.0 / 현행 0.00013510190437225297
```

`+eps`의 상대 영향은 `eps / lower_half_mean`이다. 유한이라는 조건은 양의 하한을 주지 않는다. 영(0) RMSE도 유한하므로 0 분모 정책 차이 역시 이 조건만으로는 제외되지 않는다.

새 발견으로 셀 때 주의: **eps guard 존재 자체는 이미 신고된 사실**이다. 새 반례는 "유한 영역으로 한정하면 충분하다"는 새 종결 조건이 그 guard를 포함한다는 점이다. U12의 실제 scale 크기는 이번 표본 개수 사본만으로 알 수 없다. 실제 16 build가 위와 같은 작은 scale이라는 주장은 하지 않는다.

최소 방향: 정확 동치와 허용오차 이내 근사를 분리하고, raw 하위절반 평균·최종 scale·`eps/mean`을 기록한다. 예를 들어 상대 허용치가 `tau`면 `mean > 0`과 `eps/mean <= tau` 같은 조건을 검사하거나, 0/작은 scale을 별도의 명시 정책으로 다룬다. zero·near-zero·ordinary-finite·Inf·NaN를 각각 회귀에 넣는다.

## I-02 — U12를 대체할 새 `matrix` 실행의 감사 경로가 배선되지 않았다

제안 심각도: **P1(증거 배선)**. 미실측 조합 자체를 새 발견으로 세는 것이 아니다.

위치:

- `FINDINGS.md:947`–`:948`: 다른 Si와 `step_005C`는 새 `matrix`/`eval` 실행의 감사 줄로 확인하라고 안내한다.
- `bms_balancing/verify.py:1157`–`:1170`: reference/target Objective를 실제로 만든다.
- `bms_balancing/verify.py:1170`–`:1187`: 결과 행에 scale·audit가 없다.
- `bms_balancing/verify.py:1253`–`:1257`: 이 행만 stdout/CSV로 내보낸다.

재현: `--case matrix`. 파일 존재와 최적화만 빠른 fixture로 대체하고, 실제 `cmd_matrix`의 게시 경로를 실행한다. Objective는 R4와 같은 유한·연속 평탄부 합성 forward이며, 실제 `_auto_scales`가 reference/target 각각 dQ/dV Inf 36개를 센다. `w_dqdv=1.0`이므로 이 항을 사용하는 설정이다.

관측:

```text
reference audit: dqdv Inf=36
target audit: dqdv Inf=36
published CSV rows=1
stdout scale_audit 없음
CSV scale/audit 필드 없음
```

따라서 문서대로 새 matrix를 돌려도 이 조합이 제한 영역 안인지 판정할 기록이 남지 않는다. `eval`과 degeneracy 배선은 존재하며 이를 부정하지 않는다.

최소 방향: matrix에도 양쪽 audit와 사용한 scale·정책·seed·표본 수·source/state/Si를 붙인다. 정책을 거부 방식으로 바꿀 필요는 없지만, 영역 밖 결과는 식별 가능해야 한다. reference에만 Inf, target에만 Inf를 주는 두 독립 회귀가 각각 게시물을 검사해야 한다. 프로파일처럼 scale을 재산출하는 경로에는 그 행이 실제 소비한 scale과 audit를 함께 묶는 것이 안전하다.

## I-03 — U12의 16줄은 4×4 구성의 증거 집합을 검증하지 않는다

제안 심각도: **P2(회귀의 증거 범위)**. 사용자가 16 build를 실제로 하지 않았다는 발견은 아니다.

위치:

- `out/scale_audit_eval.txt:3`–`:5`: 실행 순서는 산문이며 각 줄에는 root/state가 없다.
- `tests/test_review_findings.py:2462`–`:2475`: 줄 개수 16, metric 개수·수치, 문서의 단어만 검사한다.
- `bms_balancing/verify.py:846`–`:849`: 분리된 감사 줄에 root/state/seed 등의 식별자가 없다.

재현: `--case population`. 임시 디렉터리에서 현행 FINDINGS를 그대로 쓰고, 한 감사 record를 16번 복제한 사본을 만든다. 사본 머리에도 "one root/state repeated 16, NOT 4x4"를 명시한다. 실제 U12 회귀의 `ROOT`만 그 디렉터리로 지정한다.

관측: **실제 회귀 PASS**. 다른 fixture에서 Inf 하나만 넣으면 FAIL. 즉 숫자 축은 물지만 구성 집합 축은 물지 않는다. 커밋된 16개 감사 줄도 문자열로는 모두 동일하다.

현재 허용 가능한 표현은 "사용자가 이 순서로 16 build를 실행했다고 보고했고, 보존된 16줄의 비유한 개수는 0"이다. "회귀가 4×4 전수를 검증"했다고 확대하면 안 된다.

최소 방향: 각 record에 안정 root label·state·source·Si·seed·n·run/build id·실제 scale을 붙이고 expected tuple 집합의 정확 일치, 중복/누락 거부를 검사한다. private 경로 자체를 공개할 필요는 없다.

## I-04 — U12 설정 범위를 §1-8 전체 192값으로 확대했다

제안 심각도: **P2(문서 범위)**. 비교 결과 자체가 아니라 연결 문장의 오류다.

위치: `FINDINGS.md:946`–`:948`, `out/recompare/dd_eval_*_r2.csv:1`.

재현: `--case scope`는 실제 네 CSV의 식별 헤더와 anchor/metric 수를 읽는다.

| 조합 | 보존 비교값 | U12의 GITT·Li 설정 안? |
|---|---:|---|
| GITT · Li · pristine | 48 | 예 |
| GITT · Li · 300_0009 | 48 | 예 |
| GITT · Kunz · pristine | 48 | 아니오 |
| step_005C · Li · pristine | 48 | 아니오 |

실측 범위에 넣을 수 있는 것은 **최대 96/192값의 설정**이다. 다른 96값은 다음 문장에서 명시적으로 미측정이다. 또한 192값은 raw metric/anchor의 경험적 대조이고 scale 감사와 별개인 증거 층이다.

최소 방향: §1-8의 192값 경험적 일치는 그대로 두고, U12가 그 전부의 scale 영역을 증명한다는 연결 문장만 제거한다. 필요하면 빠진 두 설정의 audit를 실제 실행해서 별도 추가한다.

## I-05 — 두 번째 metric의 예외는 첫 metric 표본 수를 두 배로 센다

제안 심각도: **P2(감사 개수)**. all-finite를 잘못 통과시키는 반례는 아니다.

위치: `bms_balancing/model.py:413`–`:419`, `:423`–`:425`.

재현: `--case exception`. `rmse_pocv`는 유한 1을 반환하고 `rmse_dvdq`는 매번 예외를 낸다. 실제 `_auto_scales(0,50)` 실행.

관측: pocv 실제 호출 50회인데 `scale_audit['pocv'] = {n:100, finite:50, Inf:0, NaN:50}`. 앞의 append를 유지한 채 catch가 세 배열 모두에 NaN을 한 번 더 넣기 때문이다. 두 번째 이후 항은 n=50이다.

최소 방향: 한 parameter의 세 반환값을 임시 tuple에 담고 한 번씩만 append하거나, 실패 항별로 정확히 한 record를 만든다. `n_attempts`·`n_metric_evaluated`·`n_exceptions`를 구별한다. R5의 기존 plateau 회귀는 예외 없는 경로만 실행한다.

## Q3 답변

원본의 비유한 정책과 달라도 **정책을 명시하고 관측의 범위를 엄밀히 나누는 방식** 자체는 타당하다. 다만 현재 `finite count`만으로 scale 동치의 수치 허용범위를 보장하지는 못한다(I-01). 새 모델 요구서에는 다음을 분리하는 것이 좋다.

1. plateau/작은 기울기에서 역도함수 정의: 양의 slope 하한, 단위, 마스킹/절단/직접 dQ/dV 적합 중 선택, 마스킹 후 최소 유효 구간.
2. raw NaN/Inf/exception과 물리적 plateau를 서로 다른 상태로 기록. “측정되지 않음”을 작은 scale로 둔갑시키지 않기.
3. zero·near-zero scale의 수치 정책과 목표 허용오차. finite만이 아니라 raw mean 및 epsilon 영향 확인.
4. 계산이 실제 사용한 metric/weight, scale bounds·seed·sample tuple, 최종 scale과 audit를 같은 결과 record에 보존.
5. 데이터/모델·seed·source·bounds가 바뀌면 범위를 새로 평가. 파라미터 profile에서 scale을 다시 구하면 행별 감사.

이 요구가 기존 실물 셀에 plateau가 있음을 증명하는 것은 아니다.

## Q5 답변 및 범위 판정

관측 열의 2–4행은 현재 붙은 한정어를 유지하면 새 모델의 **문제 정의 자료**로 쓸 수 있다. 낮은 하한의 순위를 “식별성이 좋음”으로, hull 중첩을 “공유 가능한 값 존재”로, RMSE 증가를 “모델 미스핏 원인 확정”으로 바꾸면 안 된다. 5행 γ 부분은 담당 agent의 R5 결과와 합칠 것.

1행은 증거 층을 나눠야 한다: “네 조합 192값의 경험적 일치”, “사용자 제공 원본 함수 식 대조”, “신고된 GITT·Li·seed0 16 build의 Inf/NaN 개수 0”은 서로 다른 진술이다. 마지막 진술이 앞의 모든 조합이나 모든 유한 scale의 동치를 보증하지 않는다.

**하네스 전체 GO/NO-GO는 다른 독립 검토와 합쳐 판단할 것.** 이 검토만으로 기존 192값·LAM 부호·폭 순위·정규화 수치가 반전됐다고 판단하지 않는다. 정본을 현재 문장 그대로 동치와 감사 완결성의 근거로 복사하는 것은 I-01/I-02 때문에 승인하지 않되, 위 범위를 붙인 경험적 관측으로 요구서 초안을 만드는 일 자체를 막을 필요는 없다.
