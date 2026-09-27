# Gate79 회신 — G78-N1/N2 수용, 기록 의미 P2 한 건만 정정

대상 HEAD `b0203d1090b2659c31f8eb6f55e5a144657e9052`, 코드 `3dc269d80a7441b294d475b625b096baf3d1a459`, source_digest `c78d7969ef49fd07`를 대조했다. 코드→HEAD RUN_SCOPE diff 0이며 이전 대비 src/fitting.py·src/io.py만 바뀌었다.

**G78-N1 관측 쌍 key와 G78-N2 누락·분모 정정은 설계 문장 범위에서 종결 수용한다.** 9상태 bounds와 40쌍 반례도 맞다. 76차 종결 유지. 단계 2 범위도 적합하나 아래 **G79-N1 P2 한 건** 때문에 단계 1+2의 무조건 최종 종결은 보류한다. 실행 GO를 요청하거나 내리는 회신이 아니다.

## G79-N1 — 마지막 native success와 legacy converged를 동일시하지 말 것

`src/fitting.py:219–224`는 비유한 fun이면 `ok` 대입 전에 break한다. 따라서 유한 round1(fun=1, success=true) 뒤 비유한 round2(success=false)가 오면 `ok=true`를 유지하면서 `native_last.success=false / outer=nonfinite`가 기록된다. 기존 계산 동작은 보존됐지만, 새 docstring·요청문·serializer 주석의 “마지막 round success”라는 설명은 일반적으로 틀리다.

최소 보완은 다음이다.

1. 기존 p/J/ok 제어 경로를 바꾸지 말고 **“마지막 유한 fun round에서 갱신한 success, 그런 round가 없으면 초기 false”**로 의미를 정정한다.
2. native_last/native_best/outer와 legacy ok를 구분한다. nonfinite 종료를 ok 하나로 정상 완료 처리하지 않는다.
3. fake-minimize로 유한-success → 비유한-failure와 첫 비유한 대조를 추가해 반환 p/J/ok 유지 및 종료 기록을 함께 고정한다. 현재 g79_03b는 첫 비유한에서 outer/native_best만 검사한다.

**`ok` 대입을 break 앞으로 옮기는 수정은 요구하지 않는다.** 기존 의미를 보존한다는 이번 경계에 어긋난다. 여기서 새 계산·광범위 재설계로 확대할 필요도 없다. 위 정정·한정 회귀와 최종 식별을 다음 회신으로 받으면 된다. RUN_SCOPE가 움직이면 기존 원본/history를 보존하고 승인된 영수증 규칙을 따른다. 이 회신 자체는 실행·수정 권한이 아니다.

나머지 수용: 두 역사 영수증 바이트 보존, 현재 core 재해시/원장 참조, 구성원55개 SHA, validation/outputs 불변, producer 불변을 확인했다. paired의 역사적 evidence.out 부재는 그대로이며 새 attach 수용으로 바꾸지 않는다. grid dirty=true도 보존한다. 수신자가 복원·재채점·pytest·smoke를 수행한 것은 아니다.

비차단: normalize_restart_record의 일부 새 키만 있는 행은 지금 legacy_dict로 내려가 관측값을 잃는다. 현재 producer/옛 기록 경계의 이번 종결 조건으로 늘리지 않고, 단계 3/4 세대 dispatch에서 혼합/손상 행 정책을 정할 때 다룬다.

단계 1은 종결, 단계 2는 위 한 건 확인 뒤 종결이다. 그 후 단계 3은 새 사용자 승인으로만 열 수 있다. grid_fit_v5 진단 전용, 새 연구 실행/COMSOL/복원/class 변경/투영 게시/단계 3 착수 금지 경계는 유지한다.
