# R7 독립 검토 — 입력 사본·기준 입력·진단 소비

대상: `521be85e74acef80feec45bd147dd339e25b8d0a`, `work/harness-r7-target/bms-balancing/`. 첨부 `R7_REQUEST (1).md` 완독 후 현행 파일을 검토했다. 아래는 부모 리뷰의 일부이며 전체 시험 통과 수를 대신하지 않는다.

재현 파일: [harness_r7_claims_repros.py](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_claims_repros.py). 원본 데이터·대상 코드는 수정하지 않는다. 저장소의 합성 워크북 생성기를 임시 디렉터리에서 실행하고, 파일을 정상 XLSX/CSV로 재-export한다. 명령 수준 재현은 실제 `Objective`, 실제 `multistart`/SciPy 최적화다. 실행 시간을 제한하려고 GITT/Li/대상 200/w=0, starts=2, seed=0을 사용했다. 최적화 결과를 fixture 값으로 대체하지 않았다. XLSX 자체 생성 시각과 임시 절대경로 때문에 digest 문자열은 실행마다 달라질 수 있다. 시험은 digest의 동일/부등 관계와 수치 결과를 검증한다.

## 먼저 닫힘을 인정하는 부분

`data.InputBytes`와 `build()`의 R6-03 수정은 검사한 네 입력에서 구조적으로 작동한다. 입력을 한 번 읽은 직후 같은 경로에 정상 B 파일을 재-export해도 계산 배열과 서명이 모두 A에 남는다. stable B를 따로 읽었을 때는 서명과 계산이 함께 바뀐다.

| 입력 | pathname 읽기 횟수 | 재-export 중 계산/서명 | stable B에서 8개 점 RMSE 최대 변화 |
|---|---:|---|---:|
| 풀셀 XLSX | 1 | A/A | 0.01424704410442132 V |
| 반쪽전지 XLSX | 1 | A/A | 0.015507340852541907 V |
| 문헌 Si CSV | 1 | A/A | 0.0013621508717585606 V |
| 문헌 Gr XLSX | 1 | A/A | 0.006831702837433201 V |

`ne_shape.main()`도 같은 반쪽전지 bytes에서 HalfCell·raw capacity·identity를 만든다. 200의 snapshot 뒤 PE +20 mV와 NE capacity ×0.8을 재-export한 경우 읽기는 1회였고, 재-export 중 산출은 A의 `cap_delta_pct=0.0000`, `pe_shape_max_mV=8.000000`을 유지했다. stable B는 각각 `-20.0000`, `12.000000`이었다. 양쪽 meta의 identity도 정확히 A/B로 갈렸다.

R6-05는 `out/a -> b.csv`와 `out/측정.csv`를 실제 git 저장소에서 수정하여 확인했다. 두 경로가 원문 그대로 `git_modified_outputs`에 있고 `git_modified_code=[]`, `git_dirty=False`였다. 이전 arrow/인용 경로 반례를 재보고하지 않는다.

실행: `python outputs/harness_r7_claims_repros.py --case closures` → rc 0.

## C1 — P1: noise 명령이 A의 적합 잔차와 다시 읽은 B의 측정 잡음을 결합한다

영향: 진단 수치의 입력 결속. 현재 정본의 비공개 실측값이 실제로 섞였다는 주장은 아니다.

위치: [verify.py:1700](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1700), 특히 1703의 두 번째 `D.load_full_cell(root, args.state)`; 1709–1728이 두 경로를 결합하고 1735–1743이 그 비율로 문장을 고른다.

만드는 상태와 호출:

1. 저장소의 생성기로 합성 입력 A를 만든다.
2. 실제 `cmd_noise()`의 `build()`가 완성된 직후, 같은 풀셀 XLSX의 200 전압에 seed 731, σ=0.020 V의 합성 잡음을 더해 정상 재-export B를 한다.
3. `cmd_noise()`의 본체와 최적화는 그대로 실행한다. 대조군은 파일을 바꾸지 않는 A/A와 재-export 후 일관되게 실행하는 B/B다.

| 관측 | A/A | 실제 중간 재-export A/B | B/B 대조군 |
|---|---:|---:|---:|
| misfit RMSE (V) | 0.028876177864090954 | **0.028876177864090954** | 0.025941618063608392 |
| σ at k=1 (V) | 0.00001334727534677551 | **0.018195773977771966** | 0.018195773977771966 |
| misfit/σ | 2163.451124956898 | **1.58697167261839** | 1.4256946747799122 |

A/B 행은 A의 분자와 B의 분모이며 어느 일관된 실행의 결과도 아니다. `verdict`도 A의 "거짓으로 좁은 구간"에서 "likelihood 기반 구간을 논의할 여지"로 바뀐다. 단 B/B도 후자의 분기이므로, 여기서 그 분기 자체가 일관 B의 결론과 반대라고 주장하지는 않는다. 확인한 결함은 서로 다른 입력 bytes의 혼합과 그 혼합 사실이 산출에 표시되지 않는다는 것이다.

현재 코드가 막지 못하는 이유: `InputBytes`는 각 `load_full_cell` 호출 내부에서는 맞지만 `cmd_noise`가 새 호출을 한다. 첫 snapshot은 Objective에 있고 두 번째 snapshot은 raw noise 배열에 있으며 둘의 identity를 공유하거나 대조하지 않는다. noise JSON은 이 입력 pair의 `consumed_inputs`도 기록하지 않는다. 이는 F01b/F08의 게시 신뢰 경계가 아니라 정상 입력 재-export 일정이다.

최소 닫힘 조건: 같은 풀셀 snapshot에서 Objective용 배열과 noise용 원시 배열을 전달한다. 이를 위해 원시 capacity/voltage와 identity를 담은 공통 입력 객체를 쓸 수 있다. 단 잡음 측정에 평활·재표본한 배열을 몰래 대용해서는 안 된다. A를 읽은 뒤 경로가 B로 바뀌어도 A/A 수치와 A identity를 출력하거나 명시적으로 재시작해야 한다. 위 A/B 수치가 성공으로 출력되면 여전히 열려 있다.

실행: `python outputs/harness_r7_claims_repros.py --case noise` → rc 0, 위 세 대조 모두 assert 확인.

## C2 — P1: matrix 계산의 reference 입력은 행의 소비 입력 서명에서 빠진다

영향: 참조 적합과 그로부터 계산한 LAM/LLI의 출처 재구성. `inputs_sha`가 **대상 상태**의 digest라는 계산 자체가 틀렸다는 지적이 아니다. 문제는 함께 소비한 reference 입력의 서명이 별도로 보존되지 않는다는 것이다.

위치: [verify.py:1366](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1366)에서 pristine을 적합, 1368에서 target을 적합, 1374에서 두 결과로 degradation을 계산하지만 1382의 `inputs_sha`는 `o` 하나뿐이다. 1395–1399의 ref 파라미터·점수는 입력 파일 서명이 아니다. [README.md:96](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/README.md:96)의 소비 입력 출처 설명과 R7의 루트 차원 계수 계획에는 이 구별이 필요하다.

재현 1 — pristine 전용 파일만 정상 변경:

- 실제 matrix A를 적합한다. pristine half-cell의 PE 전압만 +20 mV로 재-export한 후 실제 matrix B를 적합한다.
- 대상의 네 입력은 같으므로 두 CSV의 `inputs_sha`도 같다.
- 그런데 기준 실제 `inputs_sha`는 서로 다르고, CSV에는 ref input signature/consumed_inputs가 없다.
- 실제 LAM_NE: `2.849754951167859 → 3.8478713617817197 %`; LAM_PE: `10.35858679679474 → 11.06478725471723 %`.

재현 2 — 같은 풀셀 workbook을 두 build 사이에 정상 재-export:

- pristine A를 만든 뒤 공유 workbook의 pristine 전압 열만 +20 mV로 재-export B한다. 대상 200의 수치 열은 손대지 않는다.
- 같은 `cmd_matrix()`가 B에서 target을 만든다. 이것이 혼합 reference A/target B다.
- 이후 B/B로 일관되게 한 번 더 실행한다.

| 관측 | A/A | reference A/target B | B/B |
|---|---:|---:|---:|
| target a_NE | 1.1045322378434097 | 1.1045322378434097 | 1.1045322378434097 |
| reference a_NE | 1.011132905606683 | 1.011132905606683 | 1.0380391314056534 |
| LAM_NE (%) | 2.849754951167859 | **2.849754951167859** | **5.367912841968694** |
| 게시된 target inputs_sha | A 서명 | **B 서명** | **같은 B 서명** |

내부 reference signature는 A/B 차이를 정확히 안다. 누락은 `build()` 내부가 아니라 결과 행을 만드는 단계다. 파일 path만으로는 같은 workbook의 어느 export를 기준 계산에 사용했는지 알 수 없다. 두 입력 버전을 의도적으로 허용하는 설계도 가능하나, 그러려면 둘을 구분하여 기록해야 한다.

같은 누락은 profile에도 정적으로 확인된다: [verify.py:1488](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1488)에서 ref를 만들고 1538에서 소비하나 1551은 target signature만 쓴다. profile까지 실제 최적화를 재현했다는 주장은 하지 않는다. 반면 degeneracy JSON의 518–519는 `consumed_inputs`와 `ref_consumed_inputs`를 둘 다 보존한다. 그 양성 경로를 인정한다.

최소 닫힘 조건: matrix/profile 산출에 target/ref 각각의 실제 snapshot identity 또는 둘을 모두 도출할 수 있는 명확한 입력 묶음을 보존한다. 공유 입력이 같은 export여야 한다는 계약이면 같은 snapshot을 재사용하거나 동일성을 검사해야 한다. 다른 export도 허용한다면 그 차이를 입력 역할별로 남겨야 한다. 최소 회귀는 pristine 전용 변경과 공유 workbook 중간 재-export 각각이 reference provenance를 바꾸는지 확인하는 것이다.

실행: `python outputs/harness_r7_claims_repros.py --case matrix` → rc 0. 실제 최적화 두 종류의 일정, 대상 signature 동일/기준 signature 부등, 결과 변화 모두 assert 확인.

## C3 — P2 문서 정정: Q2의 실행 전 inputs_sha는 존재하지 않는다

[R7_REQUEST.md:104](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/reviews/R7_REQUEST.md:104)는 `run_states.sh`의 `inputs_sha`가 실행 직전 해시라고 가정한다. 현재 파일에서 해당 문자열은 0회다. [run_states.sh:151](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/run_states.sh:151)은 `LAST_PRE_PV`라는 git 상태와 시작 시각을 잡는다. 실제 입력 bytes의 signature는 각 `build()`가 생성한 `obj.inputs_sha`다.

따라서 현재 코드를 놓고 "preflight hash와 consumed_inputs가 다르면 어느 쪽을 택하나"라는 충돌 실험을 만들 수 없다. 우선 질문을 "Objective의 소비 snapshot이 정본이며 shell preflight는 코드 상태 확인뿐"으로 고쳐야 한다. 실행 전 원자료 승인까지 필요하다는 별도 설계는 현재 존재하지 않는 기능이다. 이것을 이번 코드 반례의 P1로 올리지 않는다.

## Q6와 범위 판정

R7 §5의 다섯 한정어는 이번 입력 검토로 반증되지 않았다. 표집 진폭을 γ 가족의 연속 도달 가능성·shape 적합·원인 증명으로 바꾸지 않고, 폭을 탐색 하한으로, 끝점 반복을 독립 수렴과 분리하는 현재 문구를 유지해야 한다. F08 복사 ID나 F01b 마지막 완전 묶음 복구를 새 발견으로 세지 않았다. 비공개 원자료 부재도 새 실패로 세지 않았다.

이 담당 범위의 결론: R6-03의 **한 Objective 내부**와 ne_shape 다중 소비는 닫힘. 파이프라인 전체의 입력 결속은 C1/C2가 남아 있어, 그 전체를 닫았다는 GO 근거에는 아직 사용할 수 없다. 기존 과학 관측의 수치가 틀렸다고 소급 판정한 것이 아니라, 다음 계산에서 그 수치와 소비 입력을 일관되게 재구성할 조건을 제시한 것이다.
