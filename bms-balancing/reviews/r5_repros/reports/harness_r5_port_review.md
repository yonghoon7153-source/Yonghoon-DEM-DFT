# R5 comparator / precision review

대상: `work/harness-r5-target/bms-balancing`, HEAD `0cb7b7a380a90f61c1f25cabcb28204749b88076`.
요청문 `reviews/R5_REQUEST.md` 전체를 먼저 읽었다. 대상 파일은 수정하지 않았다.

범위: R4-02~04의 precision parser / `cell_tol` / CSV schema / partial 및 CLI 정책.
다른 담당자가 확인하는 실행 산출물 게시·run id·provenance·scale 감사는 여기서 판정하지 않는다.

## 실행 범위와 기존 수정 인정

`outputs/harness_r5_port_repros.py`의 30개 합성 사례를 전부 실행했다. 각 사례는 (1) 실제
`_compare_dd_eval` helper와 (2) 별도 process의 실제 `verify.main(["eval", "--compare", ...])`를
호출한다. 원자료 적재, Objective 값, anchor만 명시적인 시험 대역이다. parser·precision·비교·종료
코드 처리는 대상 코드 그대로다. 전체 재현 script rc 0은 예상한 결과를 모두 관측했다는 뜻이며,
하위 비교 명령의 rc는 아래에 별도로 적는다. MATLAB 및 비공개 원자료를 재실행한 증거는 아니다.

```bash
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing
```

| 기존 축 / 정상 대조군 | 관측 |
|---|---|
| 명시 `%.17g`의 동일 값 / 차이 1/1024 | complete/0 · model_mismatch/1 |
| 선언 없는 동일 값 | partial/3; `--allow-partial`을 주어도 3 |
| 지원하지 않는 선언, 명시 option 없음 | invalid/2, 비교 0 |
| `%.14g`, .125 vs .1259765625 | model_mismatch/1 |
| fixed:10, .0123456789 vs .01234567894 / …899 | complete/0 · model_mismatch/1 |
| 중복 metric NaN / 중복 숫자 anchor NaN | invalid/2, 비교 0 |
| metric의 비숫자 칸 | invalid/2 |
| 실제 두 metric이 없는 legacy 파일 | partial/3; 명시 `--allow-partial`에서만 0 |
| 전정밀도 선언보다 느슨한 fixed:1 override | conflict=True, partial/3; allow-partial에서도 3 |
| 명시적으로 더 엄격한 g17 override | conflict=True, override_looser=False, complete/0 |
| `%.2g`: 1.2 vs 1.24 / 1.26 | complete/0 · model_mismatch/1 |

따라서 R4-02의 원래 추정·미지원 선언·g14 사례, R4-03의 fixed 반 단위 사례,
R4-04의 숫자/NaN 중복 사례는 닫힌 것으로 인정한다. 아래는 새로 지원한 경계나 다른 입력 역할이다.
현재 보존된 네 `%.17g` recompare 쌍의 192값이 이 반례로 틀렸다고 주장하지 않는다.

## P1-P1 — `sig:N`의 허용 구간이 실제 `%g` 반올림 역상이 아니다

위치: `bms_balancing/verify.py:720`, `:723`, `:732`, 특히 `:743`~`:745`; 소비 `:1039`~`:1047`.

`cell_tol`은 **출력값**의 지수에서 대칭 반 단위를 계산한다. 출력이 10의 거듭제곱으로 올라갔다면
그 아래쪽 값은 한 단계 더 작은 지수에서 반올림되므로, 아래쪽 허용 구간은 대칭이 아니다.
출력 0에는 유효숫자의 첫 자릿수가 존재하지 않는데 임의의 절대 폭을 준다.
또 `%.0g`를 `sig:0`으로 그대로 받아 printf의 유효 한 자리 의미보다 10배 넓게 잡는다.

모든 사례는 anchor 16개 및 RMSE 32개를 기대·비교했고, 비교기는 `worst_rel=0`,
`partial=False`, **complete 및 rc 0**을 냈다.

| 재현 case | CSV 선언/값 | Python 값 및 같은 형식 출력 | 적용 반폭 | 관측 문제 |
|---|---|---|---:|---|
| `sig2_zero_false_complete` | `%.2g`, `0` | .049 → `0.049` | .05 | 100% 상대차를 자리수 안이라고 판정 |
| `sig2_decade_false_complete` | `%.2g`, `10` | 9.6 → `9.6` | .5 | 4.1667% 상대차를 자리수 안이라고 판정 |
| `sig2_small_decade_false_complete` | `%.2g`, `.0001` | .000096 → `9.6e-05` | .000005 | 지수 표기 경계를 넘어도 같은 오류 |
| `sig0_false_complete` | `%.0g`, `1` | 4 → `4` | 5 | 75% 상대차를 자리수 안이라고 판정 |

```bash
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing --case sig2_zero_false_complete
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing --case sig2_decade_false_complete
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing --case sig2_small_decade_false_complete
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing --case sig0_false_complete
```

정상 대조: `sig2_decade_valid_rounding_control`의 9.96은 실제로 `10`으로 출력되며 complete/0이다.
따라서 10의 거듭제곱인 토큰을 전부 거부하는 수정은 필요하지 않다. 기대값은 유효한 반올림은 인정하되
위 네 값은 model_mismatch/1 또는 그 형식을 미지원으로 명시하여 nonzero가 되는 것이다.

최소 수정 조건: 지원하는 `%g` 출력 토큰의 실제 반올림 역상을 모델링하고 수치 잡음 허용량을 별도로
더할 것. 영점과 양/음의 지수 경계에서 양쪽 구간을 시험할 것. `sig:0`은 거부하고 `%.0g`는 정확히
한 자리 의미로 정규화하거나 미지원 처리할 것. 구현 전에는 해당 형식을 complete 정책에서 제외할 수 있다.
이는 기존 fixed 반 단위 수정을 재부정하는 것이 아니라 새 sig 지원의 수치적 결함이다.

## P1-P2 — 값으로 필드 역할을 추정하므로 중복 선언과 malformed anchor가 사라진다

위치: `bms_balancing/verify.py:569`~`:576` (audit), `:671`~`:682` (meta dict 덮어쓰기),
`:533`~`:541` (anchor 파싱), `:803`~`:825` (최종 하나의 선언만 사용), `:886`~`:894` (partial 예외).

`dd_eval_csv_audit`은 float로 변환되는 comment 값만 anchor로 세고, 숫자가 아니면 모두 metadata로
취급하여 건너뛴다. 이름이 이미 알려진 anchor인지, `printed_format`이 이미 등장했는지는 보지 않는다.

| 재현 case | 만드는 상태 | 실제 결과 | 기대 |
|---|---|---|---|
| `duplicate_declaration_strict_control` | `%.17g` 선언 하나, CSV .1 vs Python .149 | model_mismatch/1, worst_rel=.328859… | 정상 대조 |
| `duplicate_declaration_false_complete` | 같은 파일에 `# printed_format,%.1f`도 추가 | complete/0, precision_declared=`%.1f`, conflict=False | 선언 중복 invalid/2, 비교 0 |
| `duplicate_declaration_invalid_then_valid` | 미지원 선언 뒤 `%.17g` 선언 | complete/0 | 앞의 invalid 선언을 숨기지 말 것 |
| `duplicate_anchor_text_false_complete` | 정상 `# E_PE_0p5,1`과 `# E_PE_0p5,broken`이 둘 다 있음 | complete/0, problems=[] | 알려진 필드의 중복/형식 오류 invalid/2 |
| `nonnumeric_anchor_allowed_as_legacy` | 정상 anchor 줄을 `# E_PE_0p5,broken`으로 바꾸고 `--allow-partial` | missing_anchors=[E_PE_0p5], partial, **rc 0** | 존재하는 malformed field는 legacy 누락이 아님: invalid/2 |

```bash
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing --case duplicate_declaration_false_complete
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing --case nonnumeric_anchor_allowed_as_legacy
```

정상 대조군에서는 실제로 없는 두 legacy metric이 allow-partial에서만 0이 된다. 숫자 NaN 중복은
invalid/2다. 즉 기존 NaN 방어가 작동해도, 그 검사 전에 field가 다른 역할로 분류되는 경계가 남는다.

최소 수정 조건: 값 변환 전에 필드 이름/역할과 등장 횟수를 정하고, 알려진 anchor는 유한 숫자 타입을
검사할 것. `printed_format`은 0회 또는 유효한 선언 정확히 1회만 허용할 것. 잘못 존재하는 필드와
아예 없는 legacy 필드를 구분하여 `--allow-partial`이 전자를 성공으로 바꾸지 못하게 할 것.

## P1-P3 — 첫 다섯 parameter 열의 이름을 무시하여 다른 named p를 같은 p로 인증한다

위치: `bms_balancing/verify.py:578`~`:598`, `:1018`~`:1027`.

`parameter_header_swap_false_complete`는 정상 파일에서 헤더의 `b_PE`와 `b_NE` 이름만 맞바꾼다.
숫자 및 metric 셀은 그대로다. 첫 행의 의미는 다음처럼 달라진다.

| 필드 | Python 정본 p | CSV 헤더를 따른 p |
|---|---:|---:|
| b_PE | -.022949 | .000309 |
| b_NE | .000309 | -.022949 |

헤더 이름은 모두 유일하고 행 길이는 같으므로 audit은 통과한다. 파라미터 대조는 `mr[j]`를
정본 `pp[j]`에 위치로만 비교한다. 결과는 anchors 16/16, RMSE 32/32,
problems=[], complete/0이며 같은 p라는 결론까지 출력한다.

```bash
python outputs/harness_r5_port_repros.py --target work/harness-r5-target/bms-balancing --case parameter_header_swap_false_complete
```

이 사례의 목적함수는 합성 시험 대역이며 실제 battery objective가 같은 값이라고 주장하지 않는다.
반증된 것은 서로 다른 명명된 입력 좌표를 same-p 비교로 인증하는 입력 결속이다. 정상 헤더를 가진
`exact_equal_control`은 complete/0이며 유지되어야 한다.

최소 수정 조건: 첫 다섯 열을 `a_PE,b_PE,a_NE,b_NE,gamma_Si` 정확한 순서로 제한하고 아니면
invalid로 거부하거나, 이름으로 올바르게 재배열한 후 정본 p에 비교할 것. 현재의 이름만 바꾼 파일은
어느 정책에서도 complete가 되면 안 된다.

## 요청 Q1에 대한 답 및 별도 발견으로 세지 않은 정책 사항

추정=partial/3, 느슨한 override=partial/3, allow-partial은 실제 legacy 누락만 허용한다는 방향은
타당하고 기존 대조군에서 집행된다. 그러나 위 P1-P1/P1-P2 때문에 "지원하는 완전한 비교만 0"은
아직 일반 명제로 성립하지 않는다.

실제 우선순위는 option → declaration → inference다. `%.1f`보다 엄격한 g17 옵션은 conflict를
기록하면서 complete를 허용하고, 느슨한 fixed:1은 3이다. 명시 옵션이 있는 경우에는 해석 불가 선언도
`invalid`가 아니라 적용 옵션으로 대체할 수 있다: `unknown_declaration_explicit_option`은
`--precision g17`에서 complete/0, raw 선언과 적용 사실을 label에 기록한다. 이를 독립 수치 결함으로
세지는 않지만, 요청문의 "해석 불가 선언=invalid"에는 **명시 option이 없는 경우**라는 한정이 필요하다.

보존된 192값·범위를 붙인 관측 자체를 위 합성 사례만으로 폐기하지 않는다. 일반 comparator 성공을
무조건 설계 근거로 채택하려면 P1-P1~P1-P3를 닫거나, 검증된 정밀도/스키마 범위를 명시적으로 좁혀야 한다.
