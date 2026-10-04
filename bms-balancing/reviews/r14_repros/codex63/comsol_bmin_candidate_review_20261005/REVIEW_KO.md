# COMSOL B-min 후보 준비 검토

2026-10-05. 판정: **국소 정정 필요 — P2 2건.** 고정 후보의 허용 변경 범위·원본 결속·기준 식별은 수용한다. 다만 최종 세 필드의 독립성과 필수 transient 자유도 기록의 누락 처리를 정정한 새 봉인본이 필요하다. 전면 재설계나 기존 NORMAL480·rtol30 시험의 재개방은 요구하지 않는다.

이번 판정은 오프라인 준비 검토다. 변경부 검증 승인·기능 PASS·native 실행 승인과 다르다. 후보·제출 도구의 import, 구문 컴파일, 기능 실행과 COMSOL/JVM 호출은 모두 하지 않았다.

## 대상과 독립 확인

- 고정 커밋: 74502af93db0f01bb3ae99eca981cc215300b8bf.
- 요청문 Git blob: 1c4f56ce61e663451e2b5118137e39808e9d9687 — 수신 내용으로 재계산하여 일치.
- CODE_MANIFEST: 1,050 bytes / SHA-256 3722a51fb1caeddd72fca3751f2ed78ed3e05d5f1938fa452503b3fa5c421a03.
- 검토 경로: bms-balancing/comsol_candidates/bmin_particle640_20261004/.
- 기준: COMSOL_BMIN_SCOPE_v2_20261004.md 및 COMSOL_REBUILD_SPEC.md §44-2·45·46, 특히 §46-7의 보존 기준 고정 정정.

검토자 작성 정적 도구가 JSON·소스 문자열·해시·기존 ZIP 데이터만 읽었다. 받은 build_candidate.py 또는 static_audit.py를 실행하지 않았다. 선언된 역치환을 독립 구현하여 Java·entry·consumer·부모 네 파일 모두 NORMAL480 원본 전체 바이트로 돌아감을 확인했다. LF/CRLF 규칙도 맞는다. consumer 11개 및 부모 5개 유지 함수의 텍스트도 대조했다. 블록이 선언됐다는 사실만으로 의미가 맞다고 보지 않고, 아래 판정 흐름을 별도로 읽었다.

원 NORMAL480 결과 ZIP을 다시 해시했다. 420,748,594 bytes / SHA e991ab4c918f6576b18d6225a86ed41759ab6ee726dd6543b9a9158e581cbc30으로 수용 기록과 일치한다. 그 안의 기준 생산 8파일 및 runtime CSV가 저장소 basis의 9파일과 바이트 동일하다. 새 계약이 참조하는 기준 CSV 9개도 ZIP member의 실제 크기/SHA와 전부 일치했다. 수치 비교 자체는 반복하지 않았다.

§46-7의 고정 전커밋 899f966de97f37541d37e39b3dfc53e41b0f72fb와 대상 커밋의 Git tree를 비교했다. 선택 88개 blob은 전부 동일하고, 당시 SPEC 원문은 현재 SPEC의 정확한 접두다. 이는 저장소 보존 확인이며 원격 Windows 전체나 현재 실행 경로의 현황 확인은 아니다.

## BMIN-N1 P2 최종 판정에서도 종료 사실과 증거 유효성을 분리해야 한다

위치: candidate/PARENT_COMMAND.ps1 134–140행 GFields, 175–177행 및 188–200행 최종 호출. 연관 검증안: LIMITED_VALIDATION_PLAN.json의 PS01-09, PS01-05. 선언 범위는 ④ 판정 연결이다.

consumer는 종료를 먼저 확인하고, 이후 설정 증거가 실패해도 native_completion=NORMAL_150S_COMPLETED를 보존한다. 그러나 부모 GFields는 Limited가 정상 수용 대기 또는 보호중단 두 라벨이 아니면 native_completion을 일괄 NOT_ESTABLISHED로 바꾼다.

정적 경로 반례는 다음과 같다.

1. native 자식 rc0·150초 도달·보호식 미발동·종료 로그 결속은 유효하다.
2. 이후 mesh read-back 등 구성 증거만 실패한다. consumer 254–258·271–295행은 종료 정상 / 증거 무효 / 비교 미결을 구분한다.
3. 부모 GDecision은 INCOMPLETE를 돌려주고, GFields 137–140행은 정상 종료까지 NOT_ESTABLISHED로 바꾼다. PS01-09가 이 결과를 기대값으로 고정했다.
4. 분석 901초 또는 전달 최종 예산 초과도 동일한 축 혼합을 만든다. 최종 비교를 INCONCLUSIVE로 내리는 것은 옳지만 이미 확인된 native 종료 사실과는 별개다.

consumer_native_completion_unverified에 원문을 남기는 것은 유용하나, 최종 권위라는 세 필드 자체가 독립적이지 않은 문제를 해결하지는 않는다. 이는 정상 실행을 거짓 성공으로 만드는 결함이 아니라, 서로 다른 실패 원인을 한 축으로 합쳐 보고하는 계약 불일치다.

최소 보완: 부모가 native 자식 반환·run/manifest 결속·종료 증거를 확인하는 종료 축을 비교/분석/전달 수용 여부와 분리한다. 확인된 종료 정상은 유지하되 증거 실패나 후속 예산 초과 시 evidence_validity=INVALID, mesh_comparison=INCONCLUSIVE로 한다. consumer 문자열 하나를 무검증 복사하라는 뜻은 아니다. native 반환 또는 종료 근거 자체가 없거나 실패한 경우에는 NOT_ESTABLISHED와 원인을 유지한다. 보호중단도 그 관측을 독립적으로 보존한다.

필요한 한정 사례: 정상 종료+구성 증거 실패, 정상 종료+분석 예산 초과, 정상 종료+최종 전달 예산 초과, 실제 native 실패/종료 근거 누락. PS01-09의 기대값부터 위 계약에 맞춰 고정한다. native/C2/Job 제어 본문을 새로 바꾸거나 실제 실행을 요구하지 않는다.

근거: [GFields](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/74502af93db0f01bb3ae99eca981cc215300b8bf/bms-balancing/comsol_candidates/bmin_particle640_20261004/candidate/PARENT_COMMAND.ps1#L134), [consumer 종료 축](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/74502af93db0f01bb3ae99eca981cc215300b8bf/bms-balancing/comsol_candidates/bmin_particle640_20261004/candidate/src/diagnostic_consumer.py#L247).

## BMIN-N2 P2 자유도 예상값 불일치와 관측 누락을 구분해야 한다

위치: candidate/src/diagnostic_consumer.py 313–320행 mesh_evidence. 연관: PARENT_COMMAND.ps1 104행, LIMITED_VALIDATION_PLAN.json PY03-05. 선언 범위는 ④ I-3 증거 소비다.

현재는 batch 전체에서 DOF 문구를 찾은 뒤, 결과가 빈 배열이어도 status=PASS를 반환한다. 초기화 solver의 DOF 한 줄만 남고 transient DOF가 사라진 경우에도 그 마지막 값을 기록하고 PASS다. 부모는 mesh_readback.status만 PASS인지 보므로 이 누락을 닫지 못한다.

고정 계약 I-3의 “transient 자유도 read-back을 기록”은 필수다. 예상 156,925+12가 외삽이라는 이유로 실제 값의 일치를 합격 조건으로 삼지 않는 것은 타당하다. 하지만 실제 관측이 없는 경우까지 합격으로 두는 것은 다르다.

NORMAL480 원 로그에서도 두 값이 구분된다. batch.log 86행의 Stationary 1202+12와 131행의 Time-Dependent 79485+12는 서로 다른 단계다. 단순히 전체 로그의 마지막 DOF를 선택하는 규칙보다, 이미 확인하는 단일 Time-Dependent Solver 구간에 관측을 연결해야 한다.

최소 보완: 해당 transient 구간에서 유효하고 명확한 DOF 관측을 요구하고, 누락·구간 밖 값만 존재·해석 불가/모호한 값은 I-3 미완으로 남긴다. 반면 유효한 실제 값이 외삽 예상과 다른 경우에는 실제값·차이·검토 필요 사유를 남기되 그 차이만으로 실패시키지 않는다. 예상 DOF를 새로운 수치 합격 문턱으로 바꾸지 않는다.

필요한 한정 사례: 유효하고 예상과 같은 값, 유효하지만 예상과 다른 값, transient DOF 삭제, 초기화 DOF만 남음, 모호한 transient 관측. 기존 PY03-05는 처음 두 경우만 다룬다. 이 보완은 실제 COMSOL 로그의 새로운 발생을 요구하지 않는 inert 로그 사례다.

근거: [mesh_evidence](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/74502af93db0f01bb3ae99eca981cc215300b8bf/bms-balancing/comsol_candidates/bmin_particle640_20261004/candidate/src/diagnostic_consumer.py#L313).

## Q1부터 Q6까지의 답

| 질문 | 판단 |
|---|---|
| Q1 허용 diff | 수용. 네 소스 역재구성 모두 바이트 일치. Java 8치환·10곳, entry 5·7곳, consumer 7치환+5블록+1삽입, 부모 25치환·27곳+1블록+1삽입으로 설명된다. 두 삽입은 consumer와 부모에 각 하나다. 변경 의미도 입자 Nel·시간·식별·비교/증거/예산 범위에 들어간다. 선언 밖 물리/수치 변경은 발견하지 않았다. |
| Q2 판정 | 주 비교 301·보조 제외·초과를 결과로 처리·consumer의 ≤ 및 부모 decimal 비교 구조는 수용한다. 최종 세 필드 독립성은 BMIN-N1 정정 필요. 기능 실행 결과를 확인한 것은 아니다. |
| Q3 I1–I8 | 기준 해시, 22개 설정 키 대조, 요청/좌표·유한값·Li·guard·예산의 정적 연결은 확인했다. I-3의 실제 DOF 관측 누락은 BMIN-N2 정정 필요. 예산 검사는 기존 협조적 검사이며 모든 동기 I/O 강제 중단 보증이 아니다. |
| Q4 제거 | 수용. 기준은 NORMAL480 run/tables이고 150초 후보이므로 B020 재비교·NORMAL240 접두 비교·240초 이후 요약을 제거한 것은 범위에 맞다. SAMPLE_TOLERANCE raise 제거도 초과≠오류 계약에 맞다. 창 밖 guard·유한값·Li·전체 좌표 검사는 유지된다. |
| Q5 경로 | 과거 NORMAL480 DIAGNOSTIC_RESULT.json의 tables_manifest 9항목과 새 계약의 path/bytes/SHA가 정확히 같다. 경로는 과거 증거로 확인됐다. 현 실행 기계에 지금도 같은 바이트가 존재하는지는 미관측이며 native 전 기존 identity 검사로 다시 확인한다. 기준을 다른 폴더로 바꾸거나 재생성할 필요는 없다. |
| Q6 검증·예산 | 9군·고유 ID 41개와 예산 합 1,470초는 맞고 v2 §8-3의 주요 축을 담았다. N1/N2의 음성·양성 대조를 보완해 새 ID/기대값/횟수/예산을 시험 전에 고정해야 한다. native 10,500초 및 15GiB는 기존 수용된 시나리오 기반 제안으로 유지할 수 있으나 실제 충분성이나 승인으로 확대하지 않는다. |

계약 요청 1,637개는 NORMAL480 목록의 앞 1,637개와 정확히 같다. 주 비교 목록도 그 안의 120–150초·0.1초 간격 301개와 같다. 좌표 N/P 각 241개 원문, limits, runtime_settings_required는 원 계약과 동일하다. 같은 크기의 다른 목록이나 근접 시각으로 바꿔 쓴 것이 아니다.

NORMAL480 batch_console.log의 SHA는 69caf6ffcb91ffcab61ddd336804825369dd54cce683b59c4e6b930242e8a58b다. 원시 로그의 물리 120/60/120, 두 입자의 Nel=320|Nord=1|Distribution=CubicRoot, mesh1 edges=300|vertices=301을 직접 읽었다. 새 후보는 Nel만 640을 요구하므로 Nord/Distribution의 전용 근거는 확인됐다. 이 사실은 미래 640 실행을 이미 관측했다는 뜻이 아니다.

## 비차단 문구 정리 C1

PREPARATION_KO.md 102–103행과 요청문의 자체 신고 d는 PS01-03·04가 decimal 유효 자릿수 경계를 본다고 표현한다. 실제 계획은 0.0010000000001의 라벨 변조와 정확한 0.001/0.0001만 다룬다. 이는 한도 부근 및 라벨 일치 검사이지 고정 자릿수 표현의 반올림 경계 검사가 아니다.

해당 문구를 실제 검증 범위로 좁히면 된다. 정밀도 경계까지 검사한다고 유지하려면 별도 고정 사례와 불일치 시 미완 처리 원칙을 넣는다. 이 문구 정리를 이유로 실제 native 수치 결과가 잘못된 것처럼 표현하거나, 비교 허용치를 완화하지 않는다.

## 다음 제출물과 권한 경계

다음 보완은 N1/N2 및 C1에 한정한다. 기존 Java·entry·물리·시간 목록·좌표·기준 CSV·한도는 유지하고, 수정한 판정/증거 소비부와 계획·변경표·manifest만 다시 결속하는 것이 최소 범위다. 수정 필요가 그 범위를 넘으면 먼저 이유와 새 범위를 제시한다.

제출물은 최소 diff, 새 CODE_MANIFEST, 정적 역재구성, 두 항목의 이유별 검증안 및 비활성 승인문이면 된다. 이번 검토는 수정 작업 자체의 새 사용자 권한을 대신하지 않는다. 사용자가 국소 보완을 승인한 뒤 수행하며, **변경부 검증과 native 최대 1회는 여전히 각각 별도 승인**이다. 검토 회신만 보고 기존 41사례 또는 COMSOL을 자동 실행하지 않는다.

기존 초기 공간 시험·rtol30·0–480초 분석의 한정 수용, overall/정상 gate INCOMPLETE, 실효 정책·실제 코어 UNVERIFIED, 960초·유한 σ·다른 공간 축 미승인은 유지한다.

## 검토 범위와 산출물

INDEPENDENT_STATIC_AUDIT.json은 검토자 독립 역재구성·해시·기존 ZIP 데이터 대조다. ADDITIONAL_STATIC_AUDIT.json은 유지 함수·명령·예산 연결, PRESERVATION_GIT_AUDIT.json은 88개 Git blob 보존 대조다. STATIC_PATH_CASES.json은 위 두 결함의 제어 흐름 논증이며 실행 시험 결과가 아니다.

REFERENCE_TEXT.json은 고정 커밋에서 받은 원문·Git blob 식별을 담는다. reference의 txt는 줄 번호를 보기 위한 LF 표시 사본이며 정확한 원문 바이트 증거는 REFERENCE_TEXT.json의 UTF-8 내용과 blob/SHA를 따른다. 과거 NORMAL480 ZIP의 모든 12,893 payload를 다시 전수 심사한 것은 아니며, 전체 ZIP 식별과 이번에 필요한 소스·CSV·로그만 재대조했다.

새 검토 문서 이외에 생산 원문·실패·pending·영수증·정책은 변경하지 않았고, 외부 발송도 하지 않았다. 문서 작성 스킬에 따라 근거 확인, 정적 추론, 미실행 검증안과 사용자 승인 경계를 구분했다.

