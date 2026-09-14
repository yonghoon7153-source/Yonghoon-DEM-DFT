# R6 최종 d431404 — 독립 수치·추론 검토

대상 `d4314048c63605fb4613f8b0a91859271fddda98`, 작업 디렉터리 `work/harness-r6-d431404/bms-balancing/`.
사용자 정본 `R6_REQUEST_d431404.md`를 완독하고 내부 원장·파생 보고서 검증판정·해당 수정 코드를 확인했다. 구판 `1049894`의 판정을 자동 이전하지 않았다.

## 결론

**이 담당 범위에서 새 P1급 과학적 결론 반전을 확인하지 않았다.** R5 scale 충분조건·예외 개수·matrix 감사 배선의 원래 반례는 닫혔다. DF-01/DF-05의 정정도 인정한다. U14의 수치 대조는 아래 범위에서 재현됐다.

새 **P2 후보 1건**은 U14 해석의 실행 예산 설명이다. 실제 γ profile은 84행 모두 **25개 시작점**을 썼는데, 요청문은 다른 계산이 24-start인 것과 대비해 γ profile이 “적은 시작”이라 흔들렸다고 적었다. 이미 신고된 U16(차이의 원인이 SciPy인가)을 재발견으로 세는 것이 아니라, 비교에 쓴 실행 예산 사실이 잘못됐다는 지적이다.

전체 GO/NO-GO는 게시·소비 입력·비교기 담당 결과와 합쳐야 한다. 이 수치 검토는 새 모델 요구서의 **한정된 관측 열**을 작성하는 일을 막지 않는다. 일반적인 포팅 동치, 최적해의 유일성, 프로파일 수렴 보증으로 확대해서는 안 된다.

## 실제 실행

```sh
cd /path/to/d431404/bms-balancing
PYTHONPATH=/path/to/pytest-deps python /path/to/harness_r6_final_inference_repros.py \
  --old /path/to/extracted-bfc4623-parent/bms-balancing/out
```

Python 3.12.3 / NumPy 2.5.3 / SciPy 1.18.1. 최종 **rc 0**, `R6_FINAL_INFERENCE_CHECKS_PASSED`.
구판 자료는 부모 agent가 native `git archive bfc4623^`로 꺼냈다. 원자료·비공개 MATLAB은 실행하지 않았다. target은 변경하지 않았다.

### R5 및 내부 정정 양성 확인

- 실제 R5 관련 회귀 6개 통과. 내부 DF-01/03/05/07/08/09 회귀 6개 통과.
- 보통 유한 scale은 true; `1e-20`, zero, Inf, NaN, exception은 false. 둘째 metric에서 50회 예외가 나도 각 metric `n=50`, 실패 metric의 `n_exception=50`이며 뒤 metric은 정상 평가된다.
- 실제 `cmd_matrix` 게시 경로에서 **target만 Inf36 / reference만 Inf36**을 각각 실행했다. 두 산출 audit는 서로 바뀌거나 서로를 가리지 않고, 각 side가 실제 소비한 scale과 게시한 scale이 일치했다. raw 원자료와 optimizer만 빠른 합성 fixture로 대체한 배선 검사다.
- U13은 18줄·54 metric record, 인쇄된 `eps_rel` 범위 `4.74e-16`–`1.71e-15`다. Kunz 누락, step_005C 누락, eps 조건만 위반, flag만 false로 만든 네 독립 임시 fixture를 실제 U13 회귀가 거부했다.
- U13의 root 차원이 수기 보고 순서라는 한계와 미측정 B축은 정직하게 신고되어 있다. 새 발견으로 세지 않았다.
- 192 raw metric/anchor의 경험적 일치와 scale 감사는 별개라는 DF-05 정정은 맞다. 실제 192값 재대조 회귀도 새 SHA에서 통과했다.

## U14 독립 대조 결과

버전별 baseline은 `check_u14.baseline_for`로 선택하되, 비교 자체는 스크립트에서 키·행 중복·수치를 다시 읽어 수행했다. 300_0009는 구판 `_v2`가 기준이다. 새로 추가된 서명/환경 필드는 구판 수치 비교에 섞지 않았다.

| 대조 | 독립 관측 |
|---|---|
| 네 matrix | 공통 수치 **2,240셀 전부 정확히 같음**; 네 상태 32/32/32/16행 |
| 네 degeneracy의 3 mode span | **12개 전부 정확히 같음** |
| 네 γ profile | 총 84행. 일부 개별 값은 다름. 전 행 `n_tried=25` |
| FINDINGS §5의 인쇄 표 | 35개 수치가 현재 CSV를 해당 자릿수로 반올림한 값과 일치 |
| §5-1 문턱 표 | n·γ 범위 동일, 폭·최악 objective ratio는 **문서 인쇄 자릿수에서 동일** |

주요 개별 행 변화:

- state 100, γ=.125: LAM_NE `-10.1645535991 → -10.4456897930 %`, 차이 `-0.2811361939 %p`, 상대차 `0.027658489`.
- state 300_0009, γ=.375: b_NE `-0.000292904408 → -0.000397099930`, 상대차 `0.355732176`; pOCV RMSE `13.679551239 → 13.968329971 mV`, 상대차 `0.021110249`.
- state 300_0009, γ=0: LAM_NE `-5.888668939 → -5.738733047 %`, 차이 `+0.149935892 %p`.

따라서 “개별 행이 같다”거나 “최악 비가 원시 float까지 동일”하다고 말하면 안 된다. 문서가 사용하는 집계의 인쇄 정밀도에서 같다는 관측이다.

| pOCV 문턱 | n (구/신) | LAM_NE 폭 구 → 신 (%p) | 새 최악 objective ratio |
|---|---:|---|---:|
| 8 mV | 6 / 6 | 7.249022552 → 7.249017897 | 1.201199054 |
| 10 mV | 10 / 10 | 13.585981898 → 13.585947105 | 1.349977640 |
| 11 mV | 12 / 12 | 15.995470764 → 15.995447612 | 1.349977640 |
| 12 mV | 13 / 13 | 17.375253465 → 17.375225857 | 1.429167473 |

이 결과는 두 보존 실행의 해당 집계가 안정적이었다는 증거다. 모든 환경·seed·시작점 예산에서 안정적이라는 보장은 아니며, 변화의 원인을 분리한 실험도 아니다.

## 새 P2 후보 — γ profile의 시작점 예산을 다른 profile과 혼동했다

위치:

- `reviews/R6_REQUEST.md:117`–`:118`
- `reviews/R6_LEDGER.md:151`–`:153`
- 실제 γ profile 시작점 생성: `bms_balancing/verify.py:1517`
- 산출: `out/profile_gamma_*_Li.csv:2`부터 전 행의 `n_tried`; 각 `.meta.json:6`의 `starts=24`.

재현:

```sh
python /path/to/harness_r6_final_inference_repros.py --target /path/to/d431404/bms-balancing \
  --old /path/to/bfc4623-parent/bms-balancing/out --case u14
```

실제 출력:

```text
requested_random_starts_per_gamma = [24,24,24,24]
actual_attempts_per_gamma = [25,25,25,25]
source = best[:4] + args.starts random starts
```

`cmd_profile`은 **L-BFGS-B에서 γ를 제거한 4변수 함수**를 best 하나+random 24개로 푼다. `mode_profile_extrema`의 SLSQP 등식 profile과는 다른 경로다. 이 둘을 “등식 제약을 적은 시작으로 풀었다”라고 합치면, 관측된 차이를 설명하는 실험 설정 자체가 바뀐다.

최소 수정: U14 해석에서 “적은 시작이어서”를 제거하고 실제 예산(γ당 25회)을 적는다. 추가 budget 실험을 하더라도 “multistart를 처음 도입”하는 것이 아니라 **이미 있는 multistart 예산을 늘리는 실험**이다. U16 원인 미확정은 그대로 유지한다. 이 오류 자체가 위 인쇄 집계나 새 모델 설계 방향을 반전시키지는 않는다.

## Q4 — DF-01 정정과 LLI 1.0832의 근거

**탐색 하한으로 인용하는 데 힌트 없는 격자 재실행이 필수는 아니다.** 힌트가 들어간 두 번째 방법을 독립 확인으로 세지 않으면 된다.

구판 `_v2`와 새 U14 JSON을 각각 읽어 세 mode의 grid를 재구성했다. base 21점의 index 5/15에 constrained min/max가 들어가며, LLI에서 profile min/max가 그 두 값과 같다. LAM_PE의 profile min은 constrained min까지 못 가고, LAM_NE는 profile이 더 멀리 내려간다. 기록된 LLI 합집합 폭은 두 판 모두 `1.0832389268006661 %p`, `is_lower_bound=true`다. 새 U14 판에는 `attainable_pct`·`grid_pct`도 들어 있다.

그 숫자는 “이 유한 탐색과 실현가능성 허용치에서 확인한 폭”이지 참 집합의 정확한 폭·신뢰구간·전역 수렴 인증이 아니다. 원자료가 없어 실제 endpoint의 목적함수를 여기서 독립 재계산하지는 못했다. 앞으로 endpoint parameter, 실제 J, limit, equality/bound 잔차를 같이 보존하면 이 하한의 witness를 훨씬 직접적으로 감사할 수 있다. 독립 수렴을 다시 주장하려면 힌트 없는 탐색·다른 seed/방법 같은 독립 조건이 필요하다.

## Q5 — U14 profile이 달라도 §5·§5-1을 인용할 수 있는가

**현재 표의 인쇄 정밀도와 기술적 범위를 함께 인용할 수 있다.** 위 35셀·문턱 집계를 실제로 재계산했으므로 단순히 “결론은 안 바뀐다”는 보고를 믿은 것이 아니다.

profile 예산 증대는 안정성 평가를 강화할 추가 실험이지 이 한정된 표를 인용하기 위한 선행 필수조건은 아니다. 다만 정확한 γ별 parameter, 분기 전환 위치, 새 profile 전체의 재현성을 주장하려면 반복 seed·예산 ladder·공통 시작점/warm start 정책·목적함수값과 parameter값의 안정성을 분리해 재야 한다. U16은 이미 신고되어 있으므로 새 결함으로 세지 않는다.

`eps_rel ≤ 1e-9`도 scale 또는 고정 parameter에서의 목적함수 교란을 작게 만든다는 조건이다. 거의 동률인 후보 사이에서 **argmin의 위치가 그대로**라는 보증은 아니다. 스크립트에는 허용 eps 조건을 모두 만족하면서 A/B 순위만 바뀌는 두 유한 metric vector를 설계 메모로 넣었다. 이것을 실제 배터리 결과 반전이나 현행 flag의 새 결함으로 세지 않았다.

## Q6 — 다섯 관측을 요구서의 관측 열로

1. 포팅: 192값의 경험적 대조, 사용자 원본 식 대조, U13의 scale 상대근사를 서로 다른 증거 층으로 쓴다. DF-05 이후의 구분은 맞다.
2. 음수 LAM_NE: 공개 5행·고정 기준의 부호 산술로 한정한다. 경계 변경 재적합의 인과를 넣지 않는다.
3. 파우치 폭: 네 상태·설정의 **탐색 하한 순위**다. 양수 하한 범위 밖의 값을 배제하거나 정확도를 보장하지 않는다.
4. 원통형/PE 대조: 소스·분모·집합·`raw max/max 10.5`라는 통계량을 함께 적는다.
5. 잔차/γ: RMSE 변화·선택된 쌍·고정 reference의 표집 증인·힌트 끝점 재확인이다. 원인·보상 경로·전역 수렴으로 높이지 않는다.

이러한 관측에서 후보 모델과 **구분 실험**을 설계하는 것은 가능하다. 특정 새 모델이 필요하거나 옳다는 결론은 그 구분 실험의 채택 기준을 통과한 뒤의 일이다.

## 제외한 스트레스/기존 한계

- `--case overflow`는 helper에 `1e308` raw 반환을 직접 주는 일반 수치 스트레스다. 평균이 Inf인데 flag가 true가 되는 약점은 보이지만, 현행 raw `sqrt(mean(r²))` 함수가 그러한 크기를 유한하게 반환하는 실제 경로는 증명하지 못했다. **새 P1/GO 차단으로 세지 않았다.** 향후 안정형 RMSE 등으로 수치 domain을 바꾸면 raw mean·최종 scale 자체의 유한성도 검사하면 된다.
- root 사본 한계, B축 미측정, SciPy 원인 미확정은 요청문의 신고를 존중했다.
- 구판 `_v2`가 새 unversioned U14보다 먼저 선택되는 reader 문제는 부모 agent가 따로 실측한다. 이 보고서의 U14 대조는 새 unversioned 12개를 명시적으로 읽었다.
