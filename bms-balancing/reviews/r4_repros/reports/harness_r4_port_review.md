# R4 독립 검토 — 비교기 schema·정밀도·종료 코드

대상 `39a5fe06215710b16e9b42bf3dc3c04c63cb8663`, `bms-balancing/`.
`reviews/R4_REQUEST.md`를 먼저 전체 읽었다. 목표는 새 모델 요구서의 근거 적절성이다.
원본 MATLAB 실행·비공개 자료의 재생은 하지 않았으며 대상 파일도 수정하지 않았다.

## 실행 범위

```sh
/home/yonghoon71/ddvenv/bin/python /mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r4_port_repros.py
```

20개 사례를 helper 및 별도 process의 실제 `verify.main(['eval', '--compare', ...])`
호출로 각각 실행했다. 데이터 적재·목적함수 수치는 명시적인 합성 대역이다. 전체 script
rc 0이며, 잘못된 결과와 정상 대조에 대한 모든 단언이 충족됐다. run_states/profile,
provenance, C21는 다른 담당의 범위여서 실행하지 않았다.

## 작동하는 수정

| 사례 | 실제 판정·process 종료 코드 |
|---|---|
| 선언된 `%.17g`, 같은 값 | complete · 0 |
| 유일한 anchor에 NaN | incomplete · 2 |
| parameter에 NaN | incomplete · 2 |
| anchor 누락 | partial · 3 |
| `%.17g` 선언 또는 `--precision g17`, 실제 0.775% 차이 | model_mismatch · 1 |
| 옛 두 metric schema | partial · 3 |
| 위 두 metric schema + `--allow-partial` | partial · 0, 허용했다는 문구 |
| 두 metric schema의 NaN + `--allow-partial` | incomplete · 2 |
| 잘못된 `--precision bogus` | invalid · 2 |

R3-05의 단일 NaN/누락 사례와 R3-07의 실패 dict 전달은 실제로 고쳐졌다.
`--allow-partial`이 비유한 실패까지 성공으로 바꾸는 것은 확인되지 않았다.

## P1-P1 — 추정된 정밀도는 여전히 complete·rc 0으로 승격된다

위치: `bms_balancing/verify.py:629` (`declared_precision`), `:647`
(`resolve_precision`), `:751` (추정 경고), `:810` (partial 계산),
`:728` (`EXIT_BY_STATUS`).

같은 입력으로 선언/옵션만 바꿨다. CSV의 pOCV 열은 전부 정확한 `0.125`, Python의
한 값만 정확한 `0.1259765625`다. 절대차는 `1/1024`, 상대차는
`0.007751937984496124`(약 0.775%)다.

| 형식의 근거 | 실제 결과 |
|---|---|
| 파일 `# printed_format,%.17g` | 차이 검출, rc 1 |
| `--precision g17` | 차이 검출, rc 1 |
| 선언·옵션 없음 | inferred, complete, worst_rel=0, rc 0 |
| 파일 `# printed_format,%.14g` | inferred, complete, worst_rel=0, rc 0 |
| 파일 `# printed_format,unsupported-format` | inferred, complete, worst_rel=0, rc 0 |

후자의 세 경우에는 “추정”이라는 경고가 분명히 있다. 그러나 최종 출력은 다시
“전부 일치”, “종료 코드 0 (complete)”다. schema partial 여부만 status에 반영하고
정밀도 근거의 불확실성은 반영하지 않기 때문이다. 이는 요청문 §6 Q3의 “완전한 지원
범위의 일치만 0”을 만족하지 않는다.

`%.14g`의 경우는 단순히 정밀도를 모르는 파일도 아니다. 실제로 `.14g`로 CSV를 썼고,
Python 값을 같은 형식으로 출력하면 `0.1259765625`이므로 `0.125`와 다르다.
14자리 유효숫자 형식을 3자리 토큰의 절대오차로 바꾸면서 이미 주어진 정보를 버린다.

최소 종결 조건: 정밀도가 불명/미지원이면 기본으로 incomplete 또는 별도 partial 상태와
nonzero를 반환한다. 불명확한 결과의 탐색적 허용을 지원하더라도 complete와 구분한다.
`%.Ng`를 지원하려면 각 값의 유효숫자 반올림 구간으로 계산하고, 지원하지 않으면
명시적으로 미지원이라고 멈춘다. “추정”이라는 경고만 추가하는 것으로는 종결되지 않는다.

## P1-P2 — 선언된 fixed 형식도 실제 반올림 가능 구간의 두 배를 허용한다

위치: `bms_balancing/verify.py:609`~`:626` (`fixed:N → 10^-N`),
metric 비교의 `abs(mv-pv) > atols[...]` 분기.

원본 CSV는 이미 한 번 반올림됐고 비교 상대 Python 값은 full precision이다. 가까운
정수로 반올림하는 `%.Nf`의 허용량은 반 단위 `0.5*10^-N`이며 수치 오차는 별도로
더해야 한다. 현재 코드는 한 단위 전체를 순수한 출력 반올림으로 처리한다.

실제 옛 MATLAB 형식과 같은 `%.10f` 사례:

```text
CSV:                 0.0123456789
Python:              0.01234567899
Python을 %.10f로:    0.0123456790       ← 같은 출력이 아님
실제 절대차:         8.9999998773e-11
반올림 반 단위:      5e-11
MODEL_REL 허용량:    약 1.2345679e-11
실제 판정:           complete · worst_rel=0 · rc 0
```

차이는 반올림 반 단위와 현재 상대 수치오차 허용량의 합보다도 크다. 양성 대조로
Python `0.01234567894`는 같은 `0.0123456789`로 출력되고 현재 비교기도 받아들인다.

더 쉽게 읽히는 `%.1f` 사례도 실행했다. CSV `0.1`과 Python `0.199`는 Python을
같은 형식으로 쓰면 `0.2`가 되는데 complete·rc 0이다. 차이 `0.099`가 잘못 잡은
atol `0.1` 이내이기 때문이다. 반면 Python `0.149`가 `0.1`로 출력되는 정상 대조도
실행했다.

최소 종결 조건: 명시된 producer 반올림 규칙으로 해당 토큰이 대표하는 구간을 계산하고,
Python full-precision 값이 그 구간 및 별도의 수치 허용량 안에 있는지 확인한다.
단지 `fixed:N`을 알고 있다는 이유로 한 단위 오차를 “출력 반올림”이라고 부르면 안 된다.

## P1-P3 — 중복 이름은 유한성 검사 전에 정보를 지우거나 같은 열을 두 번 읽는다

위치: `bms_balancing/verify.py:509` (`anchors[k]` 덮어쓰기),
`:812` (중복을 포함한 expected), `:832` (`m_header.index(c)`).

실제 재현 두 가지:

1. 정상 4개 metric 뒤에 다섯 번째 `rmse_pocv` 열을 붙이고 그 열의 8개 값을 전부
   NaN으로 둔다. 모든 이름을 순회하지만 `header.index('rmse_pocv')`는 두 번 모두
   첫 열만 읽는다. 실제 출력은 **“rmse 40개 … 전부 일치”**, helper는
   expected=40·compared=40·problems=[]·complete, process는 rc 0이다.
2. 정상 `# E_PE_0p5,1` 앞에 `# E_PE_0p5,nan`을 추가한다. 파서의 dict 덮어쓰기에서
   NaN이 사라지고 16개 유효 anchor로 complete·rc 0이 된다.

유일한 anchor/metric의 NaN을 넣은 정상 음성 대조는 rc 2로 실패한다. 따라서 이번
사례는 그 수정이 되돌아갔다는 뜻이 아니라 파싱/이름 해석 단계에서 생기는 다른 경계다.

최소 종결 조건: schema를 해석하기 전에 anchor 및 metric 이름의 유일성을 강제한다.
한 이름이 여러 번 나타나는 모호한 파일은 incomplete/invalid로 거부하며, 비교 수는
유일하게 식별된 실제 셀 기준으로 계산한다. malformed 중복을 legacy partial의 허용
대상으로 바꾸지 않는다. 현재 네 recompare artifact에 중복이 있었다는 주장은 아니다.

## 정밀도 옵션·선언 충돌 및 partial 정책 답변

요청문 §6 Q3의 “선언 → 옵션 → 추정”은 구현과 다르다. 구현·§2 설명은
**옵션 → 선언 → 추정**이며 실행으로도 확인했다. 선언이 `%.17g`여도
`--precision fixed:1`이면 source=`option`, label=`--precision fixed:1`이고 그
허용량을 적용한다.

명시적인 override 자체를 별도 발견으로 세지 않는다. 사용자가 의식적으로 선택하는
정책일 수 있다. 다만 그때의 complete는 선택한 허용량에 대한 판정이며 파일이 선언한
전정밀도 일치의 증거가 아니다. 선언/옵션 충돌과 실제 적용 정책을 결과에 함께 남기고,
문서의 우선순위를 통일하는 편이 맞다.

`partial=3` 및 `--allow-partial` 정책은 시험한 옛 두 열 사례에서 의도대로 작동했다.
문제는 `--allow-partial`이 없어도 **정밀도 추정 경로가 complete·0**이라는 별도 경로다.
따라서 그 예외 옵션의 존재만으로 P1-P1이 정당화되지는 않는다.

## 판정 범위

현재 기록된 192값이 틀렸거나 새 모델 요구서 작성을 모두 멈춰야 한다고 주장하지 않는다.
단, R4의 “complete·rc 0은 완전한 지원 범위의 일치”를 새 실험 자동화의 전제로
삼으려면 위 세 조건을 닫거나 지원 범위를 명시적으로 제한해야 한다. 특히 정밀도 근거가
불명확한 입력과 중복 schema를 성공으로 취급하지 않는 것은 비공개 원자료 없이 고칠 수 있다.
