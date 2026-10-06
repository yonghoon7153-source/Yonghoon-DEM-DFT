# REIL P0 결과 수용 검토

2026-10-06 · 게이트 차수 밖 · 고정 커밋 `b38855c2c2212ce8f3513adfc3a5ef2601528512`

**판정: C3의 고정 P0 출력은 한정 수용한다. 실행 승인 조건 전체의 준수·기록 완결은 확인되지 않았다. 다음은 누락 신고와 C5 비용 파일럿 승인 요청문 준비이며, 실행 승인이 아니다.**

제출자의 후속 답변에서 종료 식별·실행 환경 결속 기록 부재와 메모리·디스크 미측정을 확인했다. 이를 수치 오류로 바꾸어 P0를 재실행하지 않는다. 반대로 정상 rc와 짧은 실행시간을 근거로 미측정 항목을 PASS로 만들지도 않는다.

## 수용 범위

| 질문 | 판정 | 범위 |
|---|---|---|
| Q1 C3 출력 고정 | 한정 수용 | 제출 JSON의 일곱 출력, 구간식·집계·소스 흐름·기존 로그의 일치. 원 XLSX에서 결과를 독립 재생성한 판정은 아님 |
| Q2 허용 차이 결정 가 | 이번 새 기준 봉인에 한해 수용 | 자료 개봉 전 사용자 결정과 제한 세 조건에 결속. 옛 환경 전체 바이트 동일성 증명은 아님 |
| Q3 AST·cycle·방향 규칙 | 이번 고정 입력 범위에서 수용 | 아래 AST 한계를 유지. 일반 안전 검사기나 다른 자료의 완전한 매핑 구현으로 승격하지 않음 |
| Q4 대응표 판정 불가 | C5 및 E3a 요청에 붙일 제한으로 적합 | 다섯 번째 cycle·충전 방향의 실증 확인으로 쓰지 않음. 선택 경로 자동 변경 금지 |
| Q5 다음 작업 | C5 승인 요청문 준비 가능 | 비용 측정·맞춤·E3a/E3b·본 분석은 여전히 별도 승인 |

[검토 요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/docs/REIL_P0_RESULT_REVIEW_REQUEST_20261006.md)과 [P0 승인 요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/docs/REIL_P0_APPROVAL_REQUEST_20261006.md)을 기준으로 한다.

## 확인한 P0 결과

수신한 문서·소스·텍스트 로그·JSON 40개의 UTF-8 바이트를 재구성해 모두 Git blob 식별과 대조했다. 다음 두 SHA도 제출값과 같다.

- P0 결과 127,971 bytes: `3875e65092b38c9b08c907926bd8d1f4ee25674c97c28b5ada935e9027d12a90`
- P0 소스 23,941 bytes: `793b326ebf86a6db3b855d828aff4d6b6dddc824bed8d00f4161537b1cc06e3a`

### 사전 양립성

제출 max_q의 IEEE 754 값에 대응하는 정확한 분수는 `886368576912267/281474976710656`이다. 부속 A §2-5의 독립 구간식으로 제출 JSON을 검산했다. 11개 명목점 × τ 세 값 × 영역 세 값의 정확한 99키가 있고, P·N·I·lhs·rhs의 분수 끝점 및 판정이 전부 일치했다.

| 판정 | 칸 수 |
|---|---:|
| PRIOR_COMPATIBLE | 83 |
| PRIOR_INCOMPATIBLE | 16 |
| P0_UNFIT | 0 |

배제 16칸은 #0·#4·#5의 τ=0에서 A0/A1 여섯 칸, #3의 모든 τ에서 A0/A1 여섯 칸, #2·#8의 τ=0/0.02에서 A0 네 칸이다. 마지막 네 칸은 max_q가 25/8보다 크다는 등록 경계와 맞는다. 이는 **상자·제약과 명목점의 대수적 양립성**이며, 맞춤 성공·실측 참값 확인·명목점 오류 판정이 아니다. [구간식과 경계표](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md#L157-L175)

### 나머지 출력

결과에는 추출 13개 OK, σ̂_v 11개 OK, 대응표 및 셀 열 목록 각 13개, 분석 밖 시트 6개가 있다. σ̂_v 범위는 0.0003153178128297169–0.0012809288186791722 V다. 소스의 SG window 21·polyorder 3·interp 및 RMS 계산은 등록 규칙과 맞는다. 이 값은 경험적 허용 폭을 만드는 수치이며, 독립 잡음분산 또는 신뢰수준의 검증으로 해석하지 않는다.

대응표에는 cycle·step·전류 메타데이터가 없다는 raw 기록이 있고, 두 축 및 종합 13개가 모두 판정 불가다. 추출 배열의 기록용 재구성이 원 추출과 같다는 결과도 13개에 남아 있다. 시트 19개, 세 입력 SHA, 노트북 상수 일치는 결과·기존 식별 로그끼리 일치한다. **금지된 XLSX·노트북·PKL을 이번에 열지 않았으므로, 원 측정점으로 max_q·σ̂_v·추출 배열을 다시 계산한 검증은 아니다.** [결과 정본](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/evidence/reil_p0_20261006/P0_RESULT.json)

## 기록 정정이 필요한 사항

### P0 N1 실행 준수 기록 미완

우선순위 P2 · C3의 고정 출력 수용을 뒤집지는 않지만, 전체 실행 준수 PASS에는 사용할 수 없다.

승인문 §7은 환경 lock SHA, 시작·끝 HEAD와 작업트리 상태를 보존하도록 했다. 실제 meta에는 명령·cwd·시작/끝 UTC·시작 HEAD·dirty 줄 수 2·rc0만 있다. 결과 JSON도 Python·numpy·scipy·pandas 버전만 담는다. 후속 사용자 답변에서 다음 부재가 확정됐다.

| 항목 | 현재 결론 |
|---|---|
| 종료 HEAD | 실행 당시 기록 없음. 제출자가 설명한 reflog는 간접 근거이며, 이번에 원문 확인하지 않음 |
| 시작 dirty 두 줄의 파일·내용 및 종료 작업트리 | 기록 없음. clean 또는 생산 코드 불변을 이 기록으로 증명할 수 없음 |
| 실행과 환경 lock SHA의 직접 연결 | 없음. 실행 전 봉인·venv 경로·커밋 순서의 간접 연결만 남음 |
| 메모리 4 GB·디스크 3 GB 상한 | 당시 측정·감시하지 않음. 준수 여부 UNVERIFIED이며 초과가 입증됐다는 뜻도 아님 |
| P0 시간 | meta의 08:02:41Z–08:03:09Z, timeout 1800, 외부 rc0 기록으로 28초 실행을 확인 |

따라서 상태 문서 §20의 “메모리·디스크 상한 안”은 철회·정정해야 한다. 제목의 “중단 조건 0”도 모든 상한을 관측했다는 뜻으로 쓰지 말고, **보고된 P0 실행 오류 없음·자원 상한 미관측·기록 미완**으로 한정한다. [문제 문구](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md#L319-L340) · [실행 meta](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/evidence/reil_p0_20261006/12_p0_run.meta.txt)

다음 문서 작업에서는 상태 문서 새 §22에 누락·원인·영향을 추가하고, §20 해당 문구에서 정정 위치로 연결하면 충분하다. 기존 P0 결과·meta·로그·봉인은 고치지 않는다. 결과·소스·환경 봉인·기존 로그의 현재 SHA를 별도 사후 연결표에 묶는 것은 가능하지만, 이를 실행 당시의 환경 측정이나 종료 기록으로 부르지 않는다. 현재 측정·재실행으로 과거 누락을 채우지 않는다.

### P0 N2 AST 안전성 문구 한정

우선순위 P3 · 현재 출력 비차단, 향후 재사용 제한.

`util_static_check`는 함수 정의를 그대로 허용하고, 클래스도 메서드 정의의 decorator·기본값·annotation이나 기반 클래스의 생성 훅까지 확인하지 않는다. 따라서 200행의 “본문이 import 때 실행할 코드가 없다”는 일반 보증은 성립하지 않는다. 메서드 정의만 있다는 이유로 import 부작용 전체가 배제되지는 않는다. [소스 185–204행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/scripts/reil_p0.py#L185-L204)

이번 결정은 고정 util SHA와 제출된 수동 정적 열람 기록에 한정한다. 데이터의 판정 기준을 바꾸지 않은 실행 전 검사 규칙 정정으로 수용하되, AST PASS·grep 0을 보안 샌드박스나 다른 버전의 안전 증명으로 쓰지 않는다. 원 P0 소스를 소급 고칠 필요는 없다. 향후 자동 사전검사로 재사용하려면 허용 대상과 이 한계를 별도 명시해야 한다. 현재 검토에서는 해당 코드를 실행하지 않았다.

## 환경 변경과 시험 이력

새 lock과 옛 lock의 배포판 집합·버전 30개 및 `#@ files` 집계는 같다. RECORD SHA가 달라진 것은 cffi·fonttools·numpy·pip 네 배포판이다. 이는 대조 로그에 있는 bin 스크립트 포함 배포판 집합과 같다. 두 manifest는 10항목 중 lock SHA만 다르고 나머지 9항목의 SHA는 동일하다. 당시 비교 로그도 같은 9파일을 SAME으로 기록했다.

- 새 lock SHA: `b392f7b01f9492337a4c52ef323d9348af076866e6997d96179bc438375fe9ef`
- 새 manifest SHA: `a14617ecad1954a86122922072b8d1656e9b13fdbf003d131ad32e0ff52a91f5`

상태 §18의 중지 → §19의 자료 개봉 전 사용자 결정 → emit/check와 변이 증명 기록 → P0 실행 순서를 구분한다. 결정 가는 **이번 새 환경을 기준으로 채택하는 명시적 예외**로 수용한다. 옛 RECORD 원문이 없으므로, “네 배포판의 변경은 오직 shebang뿐”이나 “bin 밖 파일은 전부 옛 환경과 동일”까지는 확인되지 않았다. 다음 재구축에서 RECORD 차이를 자동 허용하는 규칙으로 확대하지 않는다. [대조 로그](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/evidence/reil_p0_20261006/04_seal_compare.txt) · [승인 기록](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md#L278-L317)

시험 원문은 최종 한정 P0 시험 37 PASS/rc0을 지지한다. 시스템 Python 35 PASS/1 skipped, 앞선 venv 36 PASS는 별도 기록이다. bms 전체는 583 PASS/1 FAIL/1 skipped이며, 이후 문서 수 정정 시험 1개만 다시 통과했다. 이를 “최종 전체 586 PASS”로 합산하지 않는다. 첫 수집 실패 로그와 중간 GREEN이 덮였다는 신고도 유지한다. 이번 수용을 위해 기존 전체 suite나 P0의 반복을 요구하지 않는다.

결과 JSON의 `fitting_calls/objective_calls/optimizer_calls=0`은 소스에서 초기값으로 넣은 값이다. 정적 실행 흐름과 제출 로그는 맞춤을 수행하지 않는 P0 범위와 부합하지만, 그 필드를 계측된 호출 차단기나 전역 실행 감사로 표현하지 않는다. stderr의 gradient 경고도 보존한다. 제출 설명상 P0가 쓰지 않는 dQ/dV 배열의 경고이며, 이번에 원 util을 실행해 원인을 재현하지 않았다.

## 판정 불가 대응표의 다음 사용

부속 D §3-4는 불일치와 판정 불가를 E3a·H 결과 옆에 유지하고, 노트북 선택 경로를 자동 변경하지 않도록 정한다. 따라서 13개 판정 불가는 **C5 및 E3a 승인 요청을 작성하는 것을 막는 새 선행 조건이 아니다.** 문서화된 cycle 매핑·부호 규약을 찾는 별도 작업은 가능하나, 이번 리뷰가 저자 문의나 자료 추가 개봉을 승인하는 것은 아니다. [부속 D](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_D.md#L97-L130)

C5는 특정 노트북 선택 입력의 비용 파일럿으로만 부른다. E3a도 그 선택 경로의 재현이라는 범위를 넘어서 “논문 다섯 번째 cycle의 동일 충전 자료임을 확인했다”고 쓰지 않는다. 이후 확실한 매핑이 나와 선택 데이터를 바꾸려면 별도 등록과 승인이 필요하다. 현재 cycle 함수의 좁은 허용 조건과 방향의 항상 판정 불가는 이번 메타데이터 없는 고정 입력에서 보수적이지만, D §3-2가 허용한 모든 문서화 매핑을 구현했다는 뜻은 아니다.

## C5 승인 요청문에 고정할 사항

아래는 작성 권고이며 실행 허가가 아니다. C5 자체가 맞춤이다. [부속 A §3-9](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b38855c2c2212ce8f3513adfc3a5ef2601528512/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md#L276-L285)

1. **단위:** 셀 하나의 이름·행·cell_idx·step_idx 및 선택 이유를 비용 결과를 보기 전에 고정한다. A0·J_V·Phase A만 허용하고, 다른 셀로 자동 교체하지 않는다. P0 결과 SHA 및 cycle·방향 판정 불가를 연결한다.
2. **시작과 옵션:** 등록된 seed 0/1의 각 64개, 총 128개 시작과 COBYQA 옵션을 유지한다. 실행 환경에서 승인받아 정식 봉인할 배열·manifest의 정확 SHA 및 옛 식별 대조 절차를 적는다. 이번 리뷰가 Sobol 재생성을 승인하지 않는다.
3. **횟수와 호출:** 지역 실행 최대 128, 각 maxfev 2000이면 optimizer 내부 목적 평가 상한은 256,000이다. 반환점 독립 재평가·진단 호출은 별도 집계·상한에 포함한다. 결과가 나쁘다는 이유로 시작점·지역 실행을 추가하거나 전부 자동 재시도하지 않는다.
4. **실행본과 환경:** 구현/검증이 더 필요한지 먼저 적고 그 범위를 분리한다. 정확 command·cwd·Python·소스 SHA·새 lock/manifest SHA를 실행 기록에 직접 넣으며, check가 다르면 자료 처리 전에 중지한다. 이번 새 봉인 수용을 새 기계 환경의 확인으로 갈음하지 않는다.
5. **자원과 종료:** 준비·파일럿·정리·전달 및 전체 벽시계, 메모리·디스크·병렬 수를 숫자로 요청한다. 실제 관측/집계 대상과 중단 방식도 적는다. 시작·종료 HEAD와 작업트리 목록, 환경 식별, 마지막 기록 뒤 시각, 외부 rc를 실패 경로에도 남긴다. 지원되지 않는 관측을 PASS로 가정하지 말고 실행 전에 해결하거나 승인 조건을 명시적으로 바꾼다.
6. **결과:** 시작점·반환점·J·nfev·status/message·termination·독립 재평가·선형 잔차·증인 등급과 이유를 기록한다. 등록된 budget 종료·무효 증인은 결과로 보존하고, 구조 오류·식별 불일치·상한 초과는 중지한다. 미실행 수를 표시하며 수렴하지 않았다는 이유로 추가 계산하지 않는다.
7. **용도:** 확인적 분석에서 제외한 비용 파일럿으로 봉인한다. 결과 후 조정은 등록대로 벽시계 예산·병렬 수에 한정한다. 문턱·상자·옵션·시작·상태 정의를 바꾸려면 새 등록이다. E3a/E3b·H1–H4·프로파일·운영 연구 실행으로 이어서 진행하지 않는다.

## 최종 경계

검토자가 수행한 것은 고정 문서·소스·로그 읽기, 텍스트 식별 대조, 제출 JSON의 구간 산술 검산과 회신 작성이다. 받은 소스 import·시험·P0·맞춤·설치·환경 재구축·COMSOL은 수행하지 않았다. 소스 저장소와 과거 결과는 수정하지 않았다.

`C3_OUTPUTS_ACCEPTED_WITH_EXECUTION_RECORD_GAPS`와 `C5_NOT_APPROVED`를 함께 유지한다. P0 재실행은 필요하지 않다. 다음 안전한 행동은 누락의 문서 신고와 별도 C5 승인 요청문 작성이다.
