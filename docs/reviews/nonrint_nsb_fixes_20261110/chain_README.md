# NSB-C01/C02 — P2 수치 보존과 예정 POST 부족 음성 보완

**작성측 수정 후보: 새 회귀 11/11, 기존 P2 29/29·행렬 25/25. 독립 재확인 미수령, 전체 HOLD.** 바탕은 `a69095c7f1cc4908a14b93912d97cb93cc33eb64`다. 실제 자료·원 로그·현장·연구 engine·전체 gate·운영 봉인·원장 변경은 없다.

| 항목 | 상태 | 바뀐 것 | 남는 경계 |
|---|---:|---|---|
| NSB-C01 | 0 | P2 `_number`가 정확한 내장 int를 float로 먼저 바꾸지 않음. 기존 Fraction 비교에 원 값을 전달. | 작은 합성 입력의 수치 계약. 실제 T0/T5/T11/T12/T13·숨은 이력·물리 자격 아님. |
| NSB-C02 | 0 | 행렬의 EXPECTED_NEGATIVE를 재검증한 분리·clear·완전 POST 1–3창과 등록된 4창 종료 예산에 결속. | 합성 음성 역할의 공개된 명료화. 실제 정량값·자격 또는 1저자 추가 정책 비준 아님. |
| 다른 경계 | 1 | S0/LIVE 재검사·신원·재고·시도/재개·dt/2 및 모든 실제 권한 false 보존. 기존 fixture/시험 바이트도 보존. | 앞서 한정 수용된 다른 단위를 이번 수정으로 재개방하지 않음. |
| 독립 판정·실제 운영 | 2 | 새 후보의 독립 검토 NOT_RECEIVED, 운영 NOT_RUN. | 원장 종결·실제 값 열람·실행 GO 없음. |

상태 0 = 작성측 수정·합성 확인, 1 = 기존 범위 보존, 2 = 별도 미수행/미승인이다. `0`을 원장 verified나 외부 GO로 해석하지 않는다.

## 1. NSB-C01 수치 계약

`scripts/dem_gen2_p2_contract.py`의 `_number`는 exact built-in int/float만 받는다. int는 원 정수, float는 원 유한 이진 부동소수점 값을 반환한다. bool·하위형·비유한 float와 음수 금지 필드의 음수는 기존대로 거부한다. `Fraction(value)`가 int를 정확히 보존하고 float의 실제 이진 값으로 비교하므로 `Fraction(str(value))` 같은 십진 의미 전환은 없다.

수령 반례의 POST 높이 `2**53`와 `2**53+1` 차이 1, KE 한계 `2**53`와 관측 `2**53+1`의 초과 1이 더는 사라지지 않는다. 같은 큰 정수 높이를 계속 쓰는 양성과 한계에 정확히 같은 KE는 보존된다. 행렬의 P2 packet에서 같은 반례를 만들되 메타·계획 hash를 일관되게 결속해도 수치 실패가 전파된다. 오래된 hash의 불일치만으로 막힌 결과가 아니다.

이 helper는 pressure·plate_z·입자 재고의 같은 숫자 읽기에도 쓰이므로 기존 P2 29개와 행렬 25개를 함께 확인했다. 기존 float 문턱은 정확한 1/8과 그 바로 위 이진 float를 구분한다. 임의 실제 물리 신호의 정확도를 인증하거나 기존 S0/LIVE가 이미 잃은 정보를 복구하는 수정은 아니다.

## 2. NSB-C02 음성 역할 계약

P2의 기존 broad reason `SEPARATION_OR_POST_BUDGET_INCOMPLETE`와 V1 계획 형식은 보존한다. 행렬이 그 문자열만으로 EXPECTED_NEGATIVE를 충족했다고 세지 않도록 `scripts/dem_gen2_qualification_matrix.py`의 `_packet`에서 원 P2/S0/LIVE 입력을 다시 검증한 결과를 다음과 결속한다.

1. `second_zero_window_end`와 `plate_clear_event`가 존재한다. 임의 PASS 영수증을 입력받지 않는다.
2. `post_end`는 없고 완전 POST 창은 **1–3개**다. 0창, 빈 trace, contact만, 두 zero까지만, clear만 있는 trace는 예정 POST 부족을 증명하지 않는다.
3. 선택 grid의 `compiled.selected_window_steps`를 `w`라 할 때 `planned_end_step = clear.step + 등록된 post_windows(4) * w`여야 한다. coarse 값을 half에 고정해서 쓰지 않는다.
4. 마지막 완전 POST 끝은 `clear.step + checked_post_windows*w`이고 계획 끝보다 앞서야 한다. plan을 다시 해시해 계획 끝을 현재 끝으로 줄이거나 임의로 늘려도 수용하지 않는다.
5. 원 재고·접촉·샘플 완전성·step 연속성·명부/시도·시간 검사는 그대로다. 후행 샘플 결손 `STEP_SAMPLES_MISSING`나 접촉 재출현은 이 예정 음성이 아니다. 압력 첫 crossing은 이 계약의 새 필수 분리 근거로 추가하지 않았다.

**권고안 전제(Q-QUAL-A/B)의 명료화:** 1–3개의 완전 POST 뒤 등록된 4창 예산에 못 미친 역할만 허용한다. 기존 3 POST fixture를 그대로 유지하며 새 1/2 POST는 이 공개된 합성 범위의 대조다. 임의 실제 자격의 허용폭·정량 문턱·종료 규칙을 승인한 것이 아니다.

음성 행은 `negative_scope=POST_SHORTAGE_AFTER_SEPARATION_AND_CLEAR`, `checked_post_windows`, `missing_post_windows`를 추가로 기록한다. 양성 역할의 `negative_scope`와 `missing_post_windows`는 null이다. 이 진단을 actual qualification·연구 성공으로 세지 않으며 세 계획 사례의 기대 일치가 물리 성공 세 건을 뜻하지 않는다. 실제 권한·등록/신원 인증은 계속 false/NOT_RUN이다.

## 3. 시험 먼저와 결과

수령 파일 `review/chain/independent_regression_tests.py`(SHA256 `8ef842355869cb629f84de08219abc840c5dc9409c3ae1a67d6bf137760c4e4e`)는 읽고 내용만 검토했다. 그 top-level 실행기/파일 writer를 실행하지 않았다. 세 기대 정답 주장을 새 `scripts/test_dem_gen2_nsb_chain_regression.py`의 `test_received_*`에 편입하고, 고정 repo 합성 fixture와 이미 설치된 audit 아래 실행했다. 원 입력 불변·사유·권한 false도 추가 확인한다.

| 관측 | 메서드 | assertion/subtest 실패 | 오류 | rc |
|---|---:|---:|---:|---:|
| 고정 구본 + 새 시험, 구현 수정 전 | 11 | 13 | 0 | 1 |
| 최소 후보 + 같은 시험 | 11 | 0 | 0 | 0 |
| 기존 P2 회귀 | 29 | 0 | 0 | 0 |
| 기존 행렬 회귀 | 25 | 0 | 0 | 0 |
| int→float 변환 복원 복사본 | 같은 11 | 4 | 0 | 1 |
| 음성 증거 검사를 label/count만으로 대치한 복사본 | 같은 11 | 6 | 0 | 1 |
| 계획 끝=clear+4*w 검사만 제거한 복사본 | 같은 11 | 1 | 0 | 1 |

새 고유 메서드는 11개이며 수령 세 주장을 포함한다. 메서드 수·subtest 실패·내부 반복·기존 회귀·약화 대조를 합산한 새 총수를 만들지 않는다. 새 시험 파일은 old red 이후 바꾸지 않았다. 기존 P2·행렬 시험 본문도 그대로다. 과거 T11/LIVE/S0 작성 순서의 한계는 이번 엄격한 red→구현 순서로 소급 해소되지 않는다.

변이 준비 중 메타 스크립트가 4개 tuple 항목을 3변수로 풀어 한 번 중단됐다. 프로젝트 실행·변이 source 기록 전에 난 준비 오류이며 보존 note에 구분했다. 이후 새 복사본으로 세 대조를 수행했다. 이를 코드 반례나 고유 시험으로 세지 않는다.

## 4. 신원·실행·한계

- P2 구본 SHA `cb5b3b66bbb89c39d2faf843c68f1b04853e28d9bcddc69de458f4aa2c194899` → 후보 `5a1830c9cf38f7081edbcb687fbc133449af767b0320cfaa1297b578b2f34f8d`.
- 행렬 구본 SHA `b407782264018f0bf2ff704169ff6ef3f9da7c05a865278679daa16d4f950d77` → 후보 `54919d9d3c8b52c0861deb80a6bdb4b34febb039af93c3827b705e3f27e35755`.
- 신규 시험 SHA `3a243579bff25958909b7392658a4554187fc64739f3a9a8c1993f81351b48cd`.
- fixture의 기존 선언 핀은 계약의 역사 참조로 유지한다. 실행한 후보의 실제 바이트 신원은 위 새 SHA와 보고서가 구분한다. 선언 핀·계획 hash를 source authentication으로 승격하지 않는다.
- Windows Python 3.12.14, `-I -B`. 복사한 source를 읽기 전에 Python process/network audit를 설치했다. 일곱 호출에서 해당 audit 시도 0을 관측했다. OS 전체 syscall 감사·다른 OS/버전 자격은 아니다.
- full stdout/stderr·test log·rc·시각·source/test SHA와 변이 복사본은 리포 밖 raw에 보존한다. `final_raw_manifest.json`은 자신 제외 152파일을 결속하며 SHA256은 `a98e8a2d69a2e5d9047316bbed5339d14bd5f3cb381efe9a3f36861bd2300017`이다.

작성측 별도 정적 검토는 새 source·시험의 해당 범위에서 추가 구체 누락을 발견하지 못했다. 외부 반박 판정은 아니다. NSB-F01(T5)은 같은 묶음의 별도 담당 범위이며, 기존 수용 항목 전체를 다시 감사하지 않았다. 실제 실행·값 열람·현장·운영 재봉인·원장 종결은 미수행이다. **전체 HOLD.**
