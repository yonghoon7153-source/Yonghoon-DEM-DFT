# α·β 검증 하네스 R3 — Codex 리뷰

## 판정: NO-GO

**현재 정본의 결론 5개를 그대로 새 모델의 설계 전제로 채택하는 것은 NO-GO다.** 관측을 보존하고 원인 해석을 검증할 가설로 낮추면, 새 모델의 요구서를 작성하는 일 자체를 미룰 필요는 없다.

이번 판정은 외부 팀에 회신할 수 있는지가 아니다. 요청문의 바뀐 목표, 즉 **“정본이 우리 새 모델의 설계 근거로 쓸 만한가”**를 적용했다. 동결된 `FOR_BMS_TEAM.md`는 현재 주장으로 채점하지 않았다. 공개하지 못한 원자료나 신고된 U1′~U10의 존재만으로 NO-GO를 주지 않았다.

**P1 9건**을 실행 확인했다. 핵심은 두 가지다. 첫째, 잔차 증가와 선택된 γ 쌍의 변화량은 원인을 블렌드의 표현 오류로 좁히지 못한다. 둘째, 검증 결과와 새 실행의 산출물이 실제 숫자·실행 상태에 끝까지 연결되지 않은 경로가 남아 있다. 현재 저장된 192개 수치가 틀렸다는 판정은 아니다.

| 대상 | 확인값 |
|---|---|
| 저장소·범위 | `yonghoon7153-source/Yonghoon-DEM-DFT`, `bms-balancing/`만 |
| 브랜치 | `claude/bms-alpha-beta-verify` |
| 리뷰 HEAD | `a432d239c72c44a780be56679b8d9c1b9aaf3dc0` |
| 코드·문서 정본 | `f5d9aafd2c2a3f40287f365ee37cb55753d6e36e` — HEAD는 요청문만 추가 |
| 수행 범위 | 기존 시험, 저장 산출물 재계산, 합성 수치·실행 상태 반례 |
| 변경 | 리뷰 대상의 추적 파일 변경 없음; 반례 파일과 보고서만 별도 작성 |

## 1. 실제 실행한 증거

최종 통합 재생 로그는 `harness_r3_replay_results.json`이다. 다음은 그 출력이며 요청문에서 옮겨 적은 수치가 아니다.

| 검사 | 이 기계의 결과 | 해석 |
|---|---|---|
| 기존 pytest 전체 | **54 passed in 6.04s**, rc 0 | 요청문의 개수와 일치 |
| MATLAB 쪽 `run_all.sh` | rc 0 | **Octave 없음: 단계 1~3 미실행**. Python 비교 시험·합성 xlsx smoke만 통과 |
| 4개 루트 `compare_states.py` | rc 0 | `best [min,max]` 표시, 혼합 소스 경고 확인 |
| 커밋된 R2 반례 재생 | 전체 rc 1 | port/inference의 옛 assertion 실패, shape는 `E_PE` 없는 옛 fixture로 중단, consumed-axis rc 0 |
| R3 port 반례 | rc 0 | 아래 R3-05~08 재현 |
| R3 inference 반례 | rc 0 | 아래 R3-01·04 재현 |
| R3 shape 반례 | rc 0 | 아래 R3-02·03 재현. 새 PE accessor를 넣어 실제 진단까지 도달 |
| R3 artifact 반례 | rc 0 | 아래 R3-09 및 192값 직접 대조 |

환경: WSL Ubuntu, Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, openpyxl 3.1.5, pytest 9.1.1. 반례 스크립트의 **rc 0은 잘못된 결과가 재현됐다는 뜻이지 GO가 아니다.**

원본 MATLAB, 원자료 xlsx와 문헌 OCP를 이 기계에서 새로 실행·검증하지 않았다. §1-13의 비공개 원본 함수 대조도 독립 확인하지 못했다. 따라서 요청문의 Octave·MATLAB 실행을 이 기계의 통과로 대체하지 않는다. 옛 R2 shape의 `AttributeError`도 종결 증거로 인정하지 않았다.

### 유지되는 긍정적 증거

새 `out/recompare`의 MATLAB CSV와 같은 이름의 TXT 앞부분에 보존된 Python 수치를 직접 읽었다. 판정 문구를 사용하지 않고 4×(16 anchors + 32 metrics)를 대조했다. 모든 parameter 행이 같고, 비교한 값이 유한했다.

| 저장된 쌍 | 재계산한 RMSE 최대 상대차 |
|---|---:|
| 300 Li | 4.042289976866168e-12 |
| pristine Kunz | 2.5354636469008477e-12 |
| pristine Li 005C | 3.2797605797850125e-12 |
| pristine Li | 2.6849350033632538e-12 |

**192개 기록의 수치적 일치는 인정한다.** 이는 해당 출력 쌍의 표본 일치이며 모든 입력에서의 프로그램 동치나 비공개 원본의 독립 재실행은 아니다. 12개 normalization 행의 matrix/degeneracy 사이 대상·기준 parameter와 objective도 정확히 같았다. 서로 다른 최적해를 섞었다는 의심은 이 12개에서는 성립하지 않았다.

## 2. 실행 확인한 P1 반례

아래 재현 명령은 ZIP의 다섯 Python 파일을 같은 디렉터리에 풀고 실행한다. `TARGET`은 해당 커밋의 `bms-balancing` 절대경로다. Linux/WSL과 대상 requirements 및 pytest가 필요하다. 원자료는 필요 없다. 모든 fixture 변경은 임시 사본에만 한다.

```bash
python harness_r3_replay.py --target "$TARGET" --output r3.json
```

수정 후에는 반례의 “잘못된 결과를 재현했다” assertion이 실패해야 한다. 보고서의 최소 조건을 정상 동작 assertion으로 뒤집어 RED→GREEN 회귀로 옮길 수 있다.

### R3-01 [P1 · 원인 추론] 정확한 모델에 잡음만으로 잔차 증가 표를 재현한다

위치: [FINDINGS.md:738](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/FINDINGS.md:738), [750](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/FINDINGS.md:750), 정본 결론 5.

```bash
python harness_r3_inference_repros.py --root "$TARGET" --case noise
```

**만든 상태:** 모든 상태의 참 모델을 `V(x)=3.25+0.85x`로 동일하게 두고, 501점의 잡음 크기만 공개 artifact의 RMSE에 맞췄다. 재적합한 뒤 실제 `Objective.rmse_pocv()`로 잔차를 계산했다.

| 셀 | 잡음만으로 재현한 100→300 RMSE, mV | 300/100 |
|---|---|---:|
| pouch | 9.795021 → 7.586385 | 0.774514 |
| c168 | 24.469404 → 39.222427 | 1.602917 |
| c171 | 30.943967 → 47.159702 | 1.524035 |

fixedhc까지 **12개 값을 모두 재현**했다. 참 모델의 표현 오차는 0, parameter 재적합 오차는 최대 1.33e-15였다. 별도의 iid Gaussian 반복에서도 상태별 분산만 다르면 같은 추세가 나왔다. 평형 전압 모델은 정확하고 `I·R_state(x)` 관측 항만 달라지는 예도 실행했다.

**왜 못 막는가:** 잔차의 크기는 모델 표현 오차, 관측 조건, 잡음 분산을 분리하지 않는다. “무작위 잡음이면 상태에 따라 커질 이유가 없다”는 전제는 측정되지 않았다. 이는 실제 자료가 잡음뿐이라는 주장이 아니라, **이 표로 잡음 가설을 배제할 수 없다는 구성적 반례**다. 신고된 U3의 존재가 아니라, 이번에 U3를 “한 칸 좁혔다”는 새 주장을 반증한다.

**최소 종결 조건:** 잔차 증가 자체는 유지하되 “잡음 가설과 맞지 않는다”, “자료 대신 모델 부적합으로 좁혔다”를 철회한다. 원인 판정을 유지하려면 상태별 반복성·측정 조건과 모델 표현을 구분하는 별도 시험이 필요하다. 자료가 없으면 가설로 낮추는 것으로 종결 가능하다.

### R3-02 [P1 · 모델 선택] 정확히 표현 가능한 곡선에도 ‘블렌드 모양이 아니다’라고 출력한다

위치: [ne_shape.py:233](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/scripts/ne_shape.py:233), [FINDINGS.md:1222](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/FINDINGS.md:1222).

```bash
python harness_r3_shape_repros.py --target "$TARGET"
```

**만든 상태:** 실제 `Blend`로 pristine γ=0.15, 측정 대상 γ=0.45를 생성한다. full-cell에서 선택된 γ 쌍이라는 입력은 0.15→0.16으로 준다. PE와 용량은 동일하게 두고 새 `E_PE` accessor도 제공한다.

```text
측정 변화                    53.41711175 mV
선택된 γ 쌍의 변화            1.76062467 mV
비                             0.03295994
합법적인 γ=0.45의 표현 오차    0.0 V
실제 출력                    “블렌드 모양이 아니라는(모델 부적합) 쪽을 가리키며”
```

**왜 못 막는가:** 진단은 선택된 γ 쌍만 읽는다. full-cell 목적함수의 선택·다른 parameter의 보상·수렴 상태와, half-cell 함수족의 표현 가능성은 다른 질문이다. 여기서 제공한 fitted pair는 진단의 합성 입력이며 새 optimizer 결과라고 주장하지 않는다. 그 입력에 대해 **함수족에 정확히 속하는 곡선에도 반대 해석을 출력**하는 것은 확인됐다.

**최소 종결 조건:** “선택된 full-cell γ 쌍의 진폭비는 3~16%”까지만 남긴다. Blend 거부의 근거로 쓰려면 직접 제약 적합·공통 정렬·잔차 기준과, 참 가족원/비가족원 대조를 마련해야 한다. 직접 γ 적합 미구현(U9)을 다시 발견으로 세는 것이 아니라, 그 시험 전에 이미 출력하는 긍정적 원인 진단을 문제 삼는다.

### R3-03 [P1 · 경계 산술] 총 상자 폭 0.5는 현재 기준점에서 가능한 이동량이 아니다

위치: [FINDINGS.md:1217](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/FINDINGS.md:1217), [ne_shape.py:228](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/scripts/ne_shape.py:228). 재현은 R3-02와 같은 스크립트다.

**현재 artifact 자체의 반례:** `300_0009`의 γ 기준은 0.2952987936이다. 허용 γ가 [0,0.5]이므로 가능한 Δγ는 **[−0.2952987936,+0.2047012064]**다. 본문 방식으로 구한 필요 이동량 0.3653169727을 더하거나 빼면:

```text
γ_ref + 0.3653169727 =  0.6606157664  → 범위 밖
γ_ref - 0.3653169727 = -0.0700181791  → 범위 밖
```

**실행 진단의 반례도 확인:** γ_ref=0.25에서 측정 변화를 100 mV로 만든 합성 입력에, 합법 γ 전체의 가능한 최대 변화가 **`ne_shape`의 x=0.02~0.98, 400점 진단 격자에서** 45.20971840 mV뿐인데도 실제 코드가 “같은 크기를 낼 Δγ는 상자 안”이라고 출력했다. 해당 합성 가족은 성분곡선의 순서가 고정되어 끝점으로 포락선을 구할 수 있고, γ 1,001점도 대조했다. x 연속구간의 전역 최댓값을 별도 증명했다는 뜻은 아니다.

**왜 못 막는가:** 코드의 조건은 `(b)/(a)<0.34`일 뿐 기준점의 양방향 여유나 실제 도달 가능한 진폭을 검사하지 않는다. 또한 선택된 두 점의 secant를 전체 가족의 기울기 한계로 외삽할 수 없다. 앞의 실물 산술 반례만으로 실물 Blend의 표현 불가능성을 증명했다고 주장하지 않는다.

**최소 종결 조건:** 무조건적인 “상자 안” 문장을 삭제한다. 가능하다고 말하려면 같은 기준에서 해당 진폭을 내는 합법 γ를 실제로 제시해야 한다. 내부 기준점·양방향 여유·비선형 응답을 회귀에 포함한다.

### R3-04 [P1 · 표의 의미] pristine 분모라는 표가 target 분모이며, 7 적합이라는 표가 6 적합이다

위치: [FINDINGS.md:716](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/FINDINGS.md:716), [test_review_findings.py:1527](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/tests/test_review_findings.py:1527), [1557](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/tests/test_review_findings.py:1557).

```bash
python harness_r3_inference_repros.py --root "$TARGET" --case denominator
```

현재 회귀의 tuple은 `(target_rmse, reference_rmse)`이고 나눗셈은 `[0]`을 사용한다. 본문은 **pristine 적합의 RMSE**라고 설명한다.

| 실제 계산 | 파우치 범위 | 원통형 범위 | max/max | 범위 겹침 |
|---|---:|---:|---:|---|
| target RMSE로 나눔 — 현재 표 | .029285~.071394 | .058782~.203710 | 2.853336 | 예 |
| pristine RMSE로 나눔 — 선언대로 | .024422~.049124 | .099777~.245045 | 4.988267 | 아니오 |

또 실제 파우치 집합은 pouch/fixedhc × GITT 3상태 = **6 적합**이다. 7번째 `300_0147`은 다른 소스라 제외됐다. 제외 자체는 타당할 수 있지만 머리글은 7이라고 쓴다. raw median/median은 6개이면 10.04107, 표시한 7개이면 9.75647이다.

**왜 못 막는가:** 회귀는 선택한 숫자끼리는 잘 대조하지만 분모 역할·모집단 이름을 검사하지 않는다. 현재 숫자를 제대로 재현하는 시험이 의미가 다른 설명까지 승인한다.

**최소 종결 조건:** target/reference 중 분모를 명시적으로 선택하고 단위·행 집합·개수·소스와 함께 봉인한다. 표의 숫자뿐 아니라 그 이름을 검증한다. 어느 분모도 공통 문턱 효과를 제거한 “진짜 차이”가 되는 것은 아니다.

### R3-05 [P1 · 대조 완결성] 앵커 누락·NaN과 parameter NaN은 여전히 complete다

위치: [verify.py:656](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/bms_balancing/verify.py:656), [693](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/bms_balancing/verify.py:693).

```bash
python harness_r3_port_repros.py --target "$TARGET"
```

유효한 16앵커·8행·4metric CSV에서 각각 독립적으로 다음 입력을 만들었다.

| 변경 | 실제 결과 |
|---|---|
| `E_PE_0p5` 앵커 삭제 | `status=complete`, “앵커 15개와 rmse 32개 … 전부 일치” |
| 같은 앵커를 NaN으로 | `status=complete`, “전부 일치” |
| parameter 첫 좌표 `a_PE`를 NaN으로 | `status=complete`, metric 32/32 비교, “전부 일치” |

양성 대조도 했다. RMSE 행 누락·RMSE NaN은 새 코드가 `incomplete`로, 유한한 RMSE 차이는 `model_mismatch`로 판정한다. 이 부분의 R2 수정은 작동한다.

**왜 못 막는가:** 기대/비교 개수와 유한성 검사가 metric에만 적용된다. 누락 앵커는 `continue`, NaN 상대차는 `> threshold`를 만족하지 않는다. parameter의 `max(abs(...)) > tol`도 NaN을 명시적으로 거부하지 않는다.

**최소 종결 조건:** 기대 앵커 schema와 모든 parameter 좌표를 먼저 검증한다. 옛 앵커 누락을 허용할 때도 `partial`이어야 한다. 비유한 값은 성공으로 다루지 않는다. R2의 수정된 RMSE 사례를 재보고한 것이 아니라 그 검사 밖에 남은 경계다.

### R3-06 [P1 · 정밀도] 전정밀도 열의 값이 모두 짧으면 실제 차이를 반올림으로 지운다

위치: [verify.py:538](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/bms_balancing/verify.py:538), [571](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/bms_balancing/verify.py:571). 같은 port 재현의 `all_short_g17_column`이다.

`%.17g`로 만든 RMSE 열 전체가 정확한 0.125라고 하자. 비교할 Python 값 하나만 `0.1259765625`로 바꾼다. 둘 다 정확히 표현 가능한 이진 유리수다.

```text
실제 절대차   0.0009765625 = 1/1024
실제 상대차   0.00775193798  (약 0.775%)
추론된 atol   0.001
실제 판정     complete, worst_rel=0, “전부 일치”
```

**왜 못 막는가:** 긴 토큰의 존재는 정밀도에 관한 증거일 수 있지만, 긴 토큰이 없다고 저정밀도 출력인 것은 아니다. 파일 전체에서 열별로 범위를 좁혀도 값으로 producer 형식을 추정하는 구조가 남는다.

**최소 종결 조건:** 내보내기 형식/version을 명시하거나 입력 옵션으로 선택한다. 알려진 `.17g`는 값 길이와 무관하게 전정밀도로 처리한다. 형식이 불명인 legacy 자료는 추정의 불확실성을 표기한다. 이 반례는 긴 토큰이 있는 현재 네 recompare 쌍이 틀렸다는 주장은 아니다.

### R3-07 [P1 · 공개 실행 결과] 비교가 실패해도 실제 명령의 종료 코드는 0이다

위치: [verify.py:625](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/bms_balancing/verify.py:625), [1213](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/bms_balancing/verify.py:1213). 같은 port 재현의 `comparison_cli`다.

유효한 합성 objective와 일부가 다른 CSV를 사용해 별도 process에서 실제 `verify.main(['eval', …, '--compare', csv])`를 호출했다.

```text
stdout: “앵커는 전부 맞는데 rmse 가 갈린다 (최대 상대차 5.85e+02)”
process returncode: 0
```

**왜 못 막는가:** helper는 실패 dict를 돌려주지만 `cmd_eval()`이 반환값을 버린다. `main()`까지 None이 올라가 `sys.exit(None)`은 성공이 된다. 사람이 읽는 불일치 로그는 존재한다. 문제는 자동 실행의 성공/실패 신호다.

**최소 종결 조건:** 완전한 지원 범위의 일치만 0으로, mismatch/invalid는 nonzero로 연결한다. partial의 정책도 명시한다. helper 단위시험 외에 process 종료 코드 회귀가 필요하다.

### R3-08 [P1 · 새 실행의 증거] profile이 전부 실패하면 이전 CSV를 새 성공으로 재사용한다

위치: [verify.py:1012](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/bms_balancing/verify.py:1012), [run_states.sh:89](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/scripts/run_states.sh:89), [144](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/scripts/run_states.sh:144). 같은 port 재현의 `stale_profile`이다.

**만든 상태:** 지정된 output에 유효한 이전 profile CSV를 둔다. 참조·자유 적합은 성공 결과를 반환하도록 대체하고, 고정 γ profile의 optimizer 네 호출만 모두 `success=False`가 되게 한다. 실제 profile 명령과, 원본 shell에서 그대로 추출한 `run`/`check_artifact` 함수를 실행한다.

```text
profile: 모든 γ가 실패; “저장할 행이 없다 … 를 쓰지 않는다”
이전 CSV: byte-for-byte 그대로
run_states helper: “OK … → profile.csv”
helper returncode: 0
```

**왜 못 막는가:** 새 all-failed 경로는 파일을 쓰지 않고 정상 반환한다. wrapper는 이번 시도가 만든 파일인지 보지 않고 기존 파일의 비어 있지 않은 행만 확인한다. 이어지는 실제 shell의 `&& write_meta`는 옛 파일에 새 provenance를 붙일 수 있다. **그 마지막 metadata 기록은 실행했다고 주장하지 않는다; 성공 뒤 호출되는 코드 경로를 확인한 것이다.**

**최소 종결 조건:** 각 시도의 새 임시 산출물을 검증한 뒤 게시한다. all-failed는 실패/미완 상태를 반환하고 wrapper가 게시·새 metadata 기록을 거부해야 한다. 옛 산출물 보존은 괜찮지만 새 실행의 결과로 인정하면 안 된다. output이 없는 경우뿐 아니라 이미 있는 경우의 재실행 시험이 필요하다.

이는 U8의 “옛 profile의 수렴 상태 미상”을 다시 센 것이 아니다. **새 성공 필터를 적용한 재실행이 실제로 전부 실패했을 때 만들어지는 신규 경로**다.

### R3-09 [P1 · 증거 회귀] 192값 검사는 숫자를 바꿔도 판정문만 그대로면 통과한다

위치: [test_review_findings.py:1484](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r3-target/bms-balancing/tests/test_review_findings.py:1484).

```bash
python harness_r3_artifact_repros.py --target "$TARGET"
```

**만든 상태:** `FINDINGS`와 recompare 산출물을 임시 디렉터리로 복사한다. 현재 C21 시험을 그대로 실행해 통과를 확인한다. pristine Li CSV의 첫 RMSE만 `0.01167578409815818 → 9.0`으로 바꾸고 TXT와 본문은 그대로 둔다.

```text
원래 시험                             통과
CSV 숫자만 9.0으로 바꾼 뒤 같은 시험   통과
TXT의 Python 원시값                   0.011675784098158164
실제 상대차                           769.8261753
판정문의 일치 문구를 지우는 대조       AssertionError
```

**왜 못 막는가:** 시험은 CSV의 개수·행 수·헤더를 확인하고, 상대차는 TXT 판정문의 숫자를 읽는다. 두 파일의 원시 수치끼리는 비교하지 않는다. 문구를 지우면 실패하지만 증거 값이 크게 바뀌어도 성공한다. U10의 INTRO/HANDOFF 미검사와는 별개인 **이번 C21 결속의 빈틈**이다.

**최소 종결 조건:** 이미 TXT에 있는 Python 원시값과 CSV의 anchor·parameter·metric을 직접 대조하여 최대차를 재계산하고 그 결과를 본문에 연결한다. 외부 원자료 없이 닫을 수 있다. 현재 보존된 192값은 직접 계산하면 실제로 맞으므로, 이 발견은 현재 기록의 오류가 아니라 그 기록을 지키는 시험의 오류다.

## 3. R2 조건별 판정

| R2 조건 | R3 판정 | 근거 |
|---|---|---|
| 01 미대조 셀도 일치 | **부분** | RMSE 행/NaN 검사는 작동. 앵커·parameter 및 공개 종료 코드에 R3-05·07 |
| 02 짧은 토큰의 tolerance | **부분** | 다른 열로 누출되던 반례는 닫힘. 전정밀도 열 전체가 짧으면 R3-06 |
| 03 실패 optimizer 저장 | **부분** | 실패 행 필터는 작동. all-failed 재실행이 옛 산출을 성공 처리하는 R3-08 |
| 04 best±span/2 | **닫힘** | 실제 compare 출력과 본문이 best [min,max]로 변경 |
| 05 hull 겹침=공유값 | **문서 주장 닫힘** | 외곽 범위로 한정. 새 격자 보존은 진전; 공유 parameter 증인은 U9 미결로 유지 |
| 06 /best의 교란 제거 주장 | **철회 닫힘** | 임의 재척도화로 정정. 새 표의 의미 오류 R3-04는 별개 |
| 07 미소비 NE·대조의 이전 | **철회 닫힘** | PE 채널의 실험으로 좁히고 cross-cell 배제를 철회. PE 강도 기록 추가 |
| 08 γ 표현력 | **안 닫힘** | 옛 상한 주장은 철회했지만 새 ‘상자 안/블렌드 아님’ 진단이 R3-02·03에 실패 |
| 09 단일 <1.20 임계 | **닫힘** | 5개 행의 조건부 임계 1.1774195~1.1962177 및 고정 기준 한정 확인 |
| 10 gamma_ref 열 | **닫힘** | 3개 행 모두 target/ref가 현재 matrix의 해당 역할과 일치 |

옛 R2 스크립트의 rc 1은 해당 실행이 멈춘 첫 assertion 또는 fixture 오류의 증거다. 그 뒤 모든 축까지 닫혔다는 뜻은 아니다. 이번에는 새 fixture로 진단까지 통과시킨 뒤 위 판정을 냈다.

## 4. 요청문 질문 5개에 대한 답

### Q1. PE 고정 실험의 해석은 충분히 좁혀졌는가?

**주요 문장은 수용 가능하다.** “이 파우치의 PE 고정 실험은 원통형 규모의 LLI 하한 폭을 만들지 않았다”는 해당 실험의 관측이다. LAM_PE가 반대 패턴을 보인 사실과 개입 강도가 상태별로 다르다는 한정도 유지됐다.

다만 “100에서 LLI 변화가 격차의 약 5%”는 두 기술량의 비율일 뿐, **PE 처리의 원인 기여율이 5%**라는 추정이 아니다. 그렇게 읽힐 표현은 피해야 한다. 한 상태에서 개입이 컸다는 사실도 원통형의 관측 조건으로 옮길 근거가 되지는 않는다. 이 전제를 명시하면 R2-07을 다시 열 필요는 없다.

### Q2. 정규화 표를 남겨도 되는가?

**분모·모집단을 고친 뒤 민감도 기술표로는 남길 수 있다.** 각 반폭을 어떤 양으로 나누었을 때 관측되는 숫자라는 범위다. 서로 다른 상대 문턱에서 얻은 탐색 하한의 비교이지, 공통 문턱에서의 식별성 차이·교란 제거·신뢰구간의 비교가 아니다.

현재의 “분모에 따라 2.9~10.5배”는 target 분모를 실제로 썼다는 조건을 붙여야 한다. pristine이라고 부르면 같은 숫자가 아니다. 서로 차원이 다른 `/RMSE`, `/sqrt(RMSE)`를 나란히 두는 목적도 재척도화 민감도임을 적어야 한다. **범위의 겹침 변화로 원인이나 공유 가능값을 결론 내리지 않는 것**이 핵심이다.

### Q3. 잔차 증가와 §5-2로 모델 부적합이라는 제3의 답을 지지할 수 있는가?

**후보 가설을 제안할 수는 있지만, 현재 방식으로 다른 후보를 줄였다고 할 수는 없다.** R3-01과 R3-02는 각각의 근거를 독립적으로 반증했다. 두 관측을 함께 설명하는 잡음·기준·parameter 보상 가설과 비교하지 않았으므로, 현재 결합만으로 다른 원인을 배제했다고 할 수 없다. 개별 반례 두 개로 모든 결합 논증의 불가능성을 증명했다는 뜻은 아니다. 여기서 관측된 것은 “현재 선택된 적합의 잔차가 크다/증가한다”이며, “더 나은 음극 함수족이 필요하다고 입증됐다”가 아니다.

### Q4. 표를 산출물에 묶는 시험의 빈틈은?

**숫자의 의미와 계산 경로가 빠져 있다.** R3-04는 숫자가 맞아도 분모 역할·집합이 틀릴 수 있음을, R3-09는 원시 숫자를 바꾸어도 판정문이 남으면 통과함을 보인다. 실패 경로는 fresh output뿐 아니라 재실행 상태까지 검증해야 한다(R3-08). U10에 이미 적은 한정어/다른 문서 사각지대와 별도로 닫을 수 있는 항목들이다.

### Q5. 새 모델 설계 요구서에는 무엇을 더 넣어야 하는가?

제안한 세 방향은 합리적인 **비교 후보**다. 아직 필수 해법으로 증명된 것은 아니다. 아래처럼 모델 선택과 채택 시험을 함께 적는 편이 맞다.

| 설계 후보/요구 | 먼저 명시할 것 | 채택을 판단할 최소 시험 |
|---|---|---|
| 측정 NE를 쓰는 표현 | 측정 프로토콜, 절대 용량·화학양론 좌표 정렬, 원자료 처리와 불확실성 | Blend에 정확히 속하는 자료/속하지 않는 자료를 구분; 직접 half-cell 적합과 미사용 full-cell 예측을 분리 |
| PE 기준 처리 선택 | 고정 PE/상태별 PE, pristine 기준과 대상의 역할, 동일 소스 조건 | 같은 조건에서 한 축만 바꾼 비교; 전압뿐 아니라 목적함수가 소비하는 미분량의 변화도 확인 |
| 잡음 모델이 있는 목적함수 | 상태별 분산·상관, 전류/온도/휴지 효과와 모델 오차의 구별 | 알려진 잡음의 합성 회복; 반복 자료가 없을 때 원인·신뢰구간 판정을 보류하는 경우 |
| 새 forward/미분 구현 | 단위, 용량 좌표, 연쇄법칙, 정규화 선택 | 해석적으로 미분 가능한 합성곡선과 수치미분 대조; 원자료와 재표본 입력의 차이 확인 |
| 열화량과 기준 불확실성 | 대상만 움직이는 분석과 기준도 움직이는 분석을 별도 정의 | 무열화·알려진 열화의 회복, 경계 활성화와 보상 방향의 실패 사례 보존 |
| 검증·산출 신뢰성 | 입력/설정/seed/시도 ID, 수렴 여부, 출력 형식·정밀도 | mismatch가 실제 명령 실패로 이어짐; 전부 실패한 재실행이 옛 결과에 새 provenance를 붙이지 않음 |

전압에서 만든 dV/dQ·dQ/dV는 같은 관측을 변환한 값이다. 별도 손실항으로 넣는 것과 독립 정보를 얻는 것은 다르므로, 중복 가중·상관을 요구서에서 다뤄야 한다. 추정의 성공뿐 아니라 **구분 못 하는 조건에서 판정을 보류하는 동작**도 합격 기준에 포함해야 한다.

이 단계에서 모든 비공개 시험을 끝낼 필요는 없다. `관측 → 후보 원인 → 구분 시험 → 채택 기준 → 남는 한계`를 구분한 요구서를 작성할 수 있으면 된다. 특정 전극 표현의 채택은 그 시험 뒤의 결정이다.

## 5. GO를 위한 최소 조건

1. **원인·표현 주장:** R3-01~03의 긍정적 원인 진단과 잘못된 γ 여유 계산을 철회하거나, 실제로 구분하는 시험으로 대체한다. “모델 부적합이 확인됐으므로 새 NE 표현”을 설계의 확정 전제로 쓰지 않는다.
2. **표의 identity:** R3-04의 분모·역할·개수·소스 집합을 일치시키고 회귀가 이를 검사한다.
3. **비교의 성공 조건:** R3-05~07을 닫아 schema·유한성·명시된 정밀도·공개 종료 코드가 같은 결과를 말하게 한다.
4. **실행 결과의 소유:** R3-08을 닫아 실패한 새 시도가 이전 파일을 자기 성공 산출물로 취급하지 못하게 한다.
5. **기록을 지키는 시험:** R3-09를 닫아 판정문 대신 보존된 192개의 실제 수치에서 대조 결과를 재계산한다.

**최종 NO-GO — 현재 정본 그대로의 설계 전제 채택에 대한 판정이다.** 수정된 관측과 후보 가설로 새 요구서를 초안 작성하는 일은 진행할 수 있다. 장기 미결을 모두 새 “발견”으로 올리거나, 또 한 번의 큰 실험 없이는 아무 작업도 못 한다는 판정은 아니다.

## 재현 파일 구성

- `harness_r3_replay.py`: 대상 SHA를 확인하고 기존 검사·반례를 모아 실행; 원본 출력과 script hash 저장.
- `harness_r3_port_repros.py`: R3-05~08, 유효/실패 대조, 기록된 192값 재계산.
- `harness_r3_inference_repros.py`: R3-01·04, 잡음/전류 대안과 표의 분모·집합.
- `harness_r3_shape_repros.py`: R3-02·03, 실제 Blend/진단 함수 실행과 R2-09·10 재점검.
- `harness_r3_artifact_repros.py`: R3-09, 임시 사본의 실제 C21 회귀와 숫자 직접 대조.
- `harness_r3_replay_results.json`: 이번 실행 stdout/stderr 전문, 환경, 대상 SHA와 변경 없음 기록.

독립 담당 보고서 3개도 ZIP에 포함했다. 보조 보고서의 번호는 분야별 번호이고 **최종 발견 번호·집계는 이 문서의 R3-01~09가 정본**이다.
