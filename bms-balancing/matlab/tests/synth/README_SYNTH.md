# `synth/` — 규진팀 함수 자리에 끼우는 **합성 대역품**

여기 있는 `electrode_ocv.m` · `build_blend_functions.m` · `differential.m` ·
`averageDuplicates.m` 는 **규진팀 코드가 아니다.** 이름·시그니처·반환 구조만
같게 만든 해석적(analytic) 가짜다.

## 무엇을 재려고 이렇게 하나

`dd_eval.m` 에서 **한 번도 실행된 적 없는 것은 모델이 아니라 배관**이다:
컬럼 인덱싱(`2*col-1`), `readmatrix` Range, `averageDuplicates` 뒤의
`c_cell = cap(end)`, 방향 정규화 분기, `quantile` 창 자르기와 `idx` 마스크,
파라미터 변환 `(cap - b)/a`, RMSE 식, CSV 쓰기.

그 배관을 재려면 **모델이 정확할 필요가 없다.** 모델 자리에 결정론적
해석 함수를 끼우고, 같은 입력에 대해 `dd_eval.m` 과 **그것을 줄 단위로 옮긴
Python 전사본**(`mirror_dd_eval.py`)이 같은 수를 내는지만 보면 된다.

## 그러므로 이 테스트가 증명하는 것 / 못 하는 것

- **증명한다**: `dd_eval.m` 의 배관 산술이 Python 쪽 배관과 같다.
  둘 중 하나에 인덱싱·마스크·부호 실수가 있으면 여기서 갈린다.
- **증명 못 한다**: 규진팀 모델이 맞는지, MATLAB 의 `pchip`/`interp1` 이
  scipy 와 같은 수를 내는지, MathWorks `sgolayfilt` 가 우리 shim 과 같은지.
  그건 사용자 기계의 실제 실행으로만 알 수 있다.
