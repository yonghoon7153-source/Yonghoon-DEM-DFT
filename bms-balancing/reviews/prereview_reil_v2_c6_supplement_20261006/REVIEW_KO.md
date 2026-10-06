# REIL C6 보충 검토와 종결 판정

2026-10-06. 고정 커밋 `563813885a377ecc570a1290e87f97b97a31a43c`의 문서와 요청된 코드 구간·기존 로그를 검토했다.

**C6-N1과 C6-N2의 국소 보충을 수용하고 C6 사전 준비 검토를 종결한다.** 기존 부속 D 수용도 유지한다. 이는 역사적 봉인·정적 구현·근거 한계를 수용한다는 뜻이며, 새 환경이 실행 준비를 마쳤다는 판정은 아니다. P0 범위·예산·중단 조건을 사용자에게 제안하는 다음 단계로 넘어갈 수 있다. 자료 개봉·환경 재구축·설치·P0·맞춤은 여전히 별도 승인 대상이다.

## C6-N1 충돌 예외

요청한 한정 목적에서 종결한다. 새 분류기는 다음 조건을 모두 요구한다.

- 경로 문자열이 `../../../LICENSE`와 정확히 일치한다.
- 덮인 쪽은 about-time 4.2.1, 디스크 쪽은 alive-progress 3.3.0이며 방향을 바꾸지 않는다.
- 두 RECORD 파일 SHA가 이전 봉인 lock의 고정값과 일치한다.
- mismatch 제공 배포판 외에 해당 경로를 주장하는 배포판이 정확히 하나다.
- 실제 디스크 해시가 그 다른 배포판의 RECORD expected 값과 같다.
- 배포판 식별 정보가 없거나 위 조건에 맞지 않으면 fatal로 남긴다.

통과한 충돌에는 covered expected, disk_owner expected, 실제 disk 해시를 모두 기록한다. `lock_text()`가 실제 `prof["dists"]`를 분류기에 넘기고 fatal/shadowed가 있으면 봉인을 중단하며, collision 객체를 lock에 직렬화하는 연결도 확인했다. 두 RECORD 상수는 기존 봉인 13·14행의 값과 같다. [허용 목록과 호출부](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/563813885a377ecc570a1290e87f97b97a31a43c/bms-balancing/scripts/reil_c6_profile.py#L61-L131)

이 판정은 기존 `measure()`에서 온 mismatch·배포판 identity와 `record_index()`의 RECORD 자료를 소비하는 현 경로에 대한 것이다. 임의로 위조한 in-memory dict 자체의 진실성이나 심볼릭 링크를 포함한 모든 플랫폼의 실제 파일 위치를 독립 인증하는 새 보안 장치로 해석하지 않는다. 이번 변경은 경로 문자열을 한 항목으로 좁힌 것이며, 일반 경로 정규화 검증기를 추가한 것이 아니다.

양성 대조 하나, 배포판 식별 누락, 실행 파일 충돌, 두 배포판 각각의 버전/RECORD 변이, 역방향, 경로 철자 세 경우, 셋째 주장자에 대한 시험 본문을 확인했다. 해당 국소 결함의 정정 근거로 충분하다. RED 원문에는 실제 거부 누락 AssertionError 2건과 새 인자 부재 TypeError 10건이 분리되어 있다. 12건 전부를 기존 동작 결함의 실증으로 세지 않는다. [허용된 시험 구간](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/563813885a377ecc570a1290e87f97b97a31a43c/bms-balancing/tests/test_reil_c6_profile.py#L1-L105)

비차단 시험 한계: 마지막 기존 fatal 세 시험은 `dists`를 주지 않아 새 코드에서는 식별 누락 조건만으로도 거부된다. 따라서 그 시험들이 각각의 깊은 거부 분기를 독립적으로 검증한다고 주장하지 않는다. 현재 코드의 exact allowlist 및 디스크 대조는 정적으로 확인했으므로 이번 종결을 다시 막지는 않는다. 향후 checker 검증 범위에 손댈 때에는 유효한 DISTS 아래의 거부 사례도 구분하는 것이 적절하다.

## C6-N2 미보존과 옵션 전달

**미보존 사실과 주장 수준 정정을 수용해 종결한다.** C6_RUN.log 및 과거 9개 시험·12개 변이·538개 전체 시험의 원문은 복구되지 않았다. 그 수치는 계속 제출자 보고이며, 이번 보충을 근거로 원문 확인 완료로 올리지 않는다. 로그를 새로 실행해 과거 기록처럼 만드는 것도 요구하지 않는다.

봉인을 생성한 구판 `17e03fa2c`의 허용 구간에서 옵션 표가 `COBYQA_OPTIONS.items()`를 읽고, 호출이 `options=dict(COBYQA_OPTIONS)`를 사용함을 확인했다. 따라서 **표와 호출이 동일한 8개 옵션 상수에서 구성되는 코드 구조**는 확인됐다. 당시 실행 중 전달된 dict의 직접 캡처나 각 옵션이 실제로 영향을 주었다는 관측은 아니다. [구판 상수](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/17e03fa2c149babb760550151955f1c54cd045c3/bms-balancing/scripts/reil_c6_profile.py#L32-L33) · [구판 호출과 결과 생성](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/17e03fa2c149babb760550151955f1c54cd045c3/bms-balancing/scripts/reil_c6_profile.py#L121-L154)

이제 정적 코드 근거와 성공 boolean·제출자 보고의 한계가 구분됐으므로 C6 문서 종결에 옵션별 효과 실험을 새로 요구하지 않는다. 특히 제약 없는 합성 함수의 성공만으로 feasibility_tol의 효과를 입증하지 않는다. 기본값과 같은 옵션이 명시 전달됐다는 구조와 그 옵션이 수치 결과를 바꿨다는 주장은 다르다.

값별 효과 관측이 향후 연구 주장에 실제로 필요해진다면 같은 판 환경 재구축 또는 맞춤 전 실행 검증의 별도 승인 항목으로 정한다. 지금 8개 전부의 효과 실험이나 전체 회귀 반복을 자동 선행 조건으로 추가하지 않는다.

## 보존과 시험 로그의 정확한 범위

이전 수신 snapshot의 Git blob/size와 현재 고정 커밋의 디렉터리 정보를 비교했다. 봉인 payload 10개와 MANIFEST·README, 총 12개 파일의 집합·blob·크기가 모두 동일하다. manifest SHA도 `e4adba0fed22e51de37d98067a623e2e3e9575cc9e1ea039a3a88363e2378e9f`로 같다. 이전 봉인 식별 수용은 유지한다. 새 checker가 예전 봉인을 만들었다고 소급 서술하지 않는다.

| 이번에 보존된 로그 | 확인 범위 |
|---|---|
| 01_red_12failed_8passed.log | traceback 포함, 12 failed / 8 passed. 실제 AssertionError 2 + TypeError 10 |
| 02_green_20passed.log | 20 passed / 0.14초라는 2행 출력. 별도 host rc·시작/끝 HEAD는 없음 |
| 03_bms_full_548passed_1failed_count_line.log | 375 bytes의 짧은 보존 기록. 시작 HEAD 10378b0b, dirty=3, 548 passed + 1 failed, rc1, 기대 시험 수 검사 실패 |

셋째 파일은 전체 traceback을 포함한 완전한 pytest 원문이 아니다. 기대 수를 550→549로 고친 뒤 해당 시험이 통과했다는 것은 제출자 보고다. **전체 549개가 고정 커밋에서 clean 재실행되어 모두 통과했다는 독립 확인은 없다.** 이 구분을 유지하면 좁은 충돌 규칙의 종결을 위해 전체 재시험을 요구할 필요는 없다. [보존 로그 디렉터리](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/563813885a377ecc570a1290e87f97b97a31a43c/bms-balancing/evidence/reil_c6_n1_20261006)

## 다음 단계에서 고정할 조건

다음 산출물은 **P0 승인 요청문**이다. P0 자체를 시작하는 것이 아니다. 요청문에는 최소한 다음 경계를 넣는다.

1. 버리는 환경 재구축이 필요하면 그 설치 범위·판·자원·시간을 명시적으로 승인받는다. 새 세션의 환경 일치는 과거 C6 수용으로 대신하지 않는다.
2. 새 checker의 emit/check는 아직 실행되지 않았음을 유지한다. 실제 환경 사용 전 이를 확인할 범위를 승인안에 둔다. 새 collision lock 형식은 별도 새 경로·manifest로 봉인하고, 옛 10파일은 덮지 않는다.
3. 예상된 collision 메타데이터 추가와 예상 밖 패키지/RECORD/배열 차이를 구분한다. ‘형식 변경’이라는 이유로 임의 바이트 차이를 일괄 허용하지 않는다. Sobol 정식 재생성의 시점과 기존 SHA 대조는 이미 수용한 계약을 유지한다.
4. P0의 허용 입력·시트/셀/cycle/방향 확인·정확 유리수 판정·산출물·중단 조건을 고정한다. pickle·노트북 실행·맞춤·비용 측정·E3b 등록은 자동 포함하지 않는다.
5. 실제 후속 실행에서는 명령·코드/환경 식별·stdout/stderr·외부 rc·시간을 종료 직후 보존한다. 옵션 dict도 명시 기록해 이번과 같은 사후 근거 공백을 피한다.

사용자에게 이 범위와 예산을 제시하고 승인 대기하면 된다. 기존 문서 종결을 다시 열거나 새 계산을 먼저 수행할 필요는 없다.

## 검토 기록

이번 검토는 지정 문서, 신규 코드 61–131행, 시험 1–105행, 구판 옵션 32–33·121–154행 및 기록된 로그만 읽었다. REIL xlsx/pkl·노트북은 열지 않았으며 제공 source import·시험·optimizer·설치·환경 재구축·P0·COMSOL 실행은 하지 않았다. 코드 excerpt의 SHA는 GitHub의 전체 blob 메타데이터와 대조한 것이며, 허용 범위 밖 전체 코드를 가져와 재해시한 것은 아니다.

검토자 데이터 확인은 32/32 일치했다. 첫 확인 스크립트는 pytest AssertionError 앞의 공백 수를 고정해 1건을 잘못 셌다(31/32). 가변 공백을 허용하도록 검토자 집계만 고쳤고 첫 스크립트·오류 요약을 보존했다. 이는 제출자 시험 재실행이나 생산 오류가 아니다. 문서 작성 스킬에 따라 역사적 봉인, 정적 근거, 실행 관측, 향후 승인을 구분해 회신을 구성했다.
