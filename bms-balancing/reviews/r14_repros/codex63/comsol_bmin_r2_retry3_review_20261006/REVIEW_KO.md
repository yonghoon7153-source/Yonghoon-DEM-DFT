# B-min R2 retry3 — 한정 검증 수신 검토

2026-10-06. 대상은 `BMIN_R2_LIMITED_VALIDATION_RETRY3_RESULT_20261005.zip` 및 함께 받은 `BMIN_R2_RETRY3_NOTE_20261005.txt`다. 이전 게이트·REIL 심사와 분리한다.

## 판정

**실제로 수행된 62개 ID·77개 입력의 기대 결과 일치는 수용한다. 원안 전체를 그대로 이행했다는 종결 문구는 조건부다.** 생산 코드 수정이나 전체 suite 재실행을 요구하지 않는다. 아래 두 기록 정리를 권고한다.

1. 최종 집계에 남은 준비 단계 boolean의 의미를 별도 정정표로 바로잡는다.
2. PS01-16은 외부 fail-closed 결과만 수용하고 내부 TryParse 분기 관측은 미완으로 남긴다는 범위 조정을 승인권자가 확인한다. 내부 분기 확인을 계속 필수로 요구한다면 그 한 건만 별도 승인 후 관측한다. 이번 검토 자체는 추가 시험 승인도 아니다.

PY04-02와 PY05-03의 실제 fixture 차이는 아래 정적 근거를 붙여 **해당 거부 조건에 한정해 대체 증거로 수용 가능**하다. 원래 fixture를 실제 실행했다고 소급 기재하면 안 된다. 전체 계획의 문언 그대로 77/77 수행 완료라고 쓰지 않는다.

**native 150초 승인 없음.** 한정 검증 결과 수용과 실제 B-min 계산 승인은 별개다. `approved=false / usable=false`인 봉인 원문은 유지한다. 전체 수렴·정상 gate·실험 타당성을 이번 합성 검증으로 PASS로 바꾸지 않는다.

## 1. 독립적으로 확인한 자료 식별

| 항목 | 수신자 확인값 |
|---|---|
| ZIP 크기 | 1,619,237 bytes |
| ZIP SHA-256 | `ed0138b90cf2dc4e42f22ec18d8719ff56906780f74b4139850d604b096bb470` |
| PACKAGE_MANIFEST | 43,200 bytes / `97f51112bd6c4e0ae502e56db99eba5fb56026c7b7c79d0639661cf44727b91a` |
| 집합 | payload 244 + manifest 1 |
| 생산 CODE_MANIFEST | `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25` |
| PRE_TEST_SEAL | `c0145c2a11f7539f0c9567d01618e0413f1a9e1ac0a54d83012bf0585db491bc` |

파일별 크기/SHA·정확 집합·CRC·중복/대소문자 충돌·경로 탈출/링크를 검사했고 불일치가 없었다. 생산 manifest의 5개 파일을 실제 ZIP 바이트로 대조했다. 전후 생산 식별 기록도 동일하다. 42개 추출 조각은 원본의 기록된 byte offset으로 잘라 비교했으며 모두 동일하다. Java helper 안의 checkShape/TIMES도 해당 추출 조각과 결속된다.

1,543개 사전 봉인 항목과 사후 보존 기록은 서로 일치한다. 그중 이 ZIP에서 경로를 대응시켜 실제 바이트까지 직접 대조한 항목은 148개다. 나머지 1,395개에는 미동봉 CSV·현지 실행파일 등 수신자가 직접 읽지 않은 항목이 포함된다. 따라서 현지 파일 1,543개를 수신자가 직접 재해시했다고 주장하지 않는다.

근거: `ARCHIVE_VERIFICATION.json`, `EVIDENCE_CROSSCHECK.json`; 원자료 `PACKAGE_MANIFEST.json`, `EXTRACTION_MAP.json`, `SOURCE_IDENTITIES_BEFORE.json`, `SOURCE_PRESERVATION_AFTER.json`, `SEALED_INPUTS_PRESERVATION_AFTER.json`.

## 2. 시험 결과와 실행 증거

계획의 (ID, input_index) 집합을 결과 집합과 대조했다. 누락·중복 없이 77개이며 고유 ID는 62개다. Python·PowerShell 원 stdout의 JSON 행은 해당 결과 파일의 행과 같고, 최종 집계의 observed 행과도 같다. stdout/stderr의 실제 바이트는 RETURN 기록의 SHA/크기와 일치한다.

| 엔진 | 논리 입력 | 기록된 rc | 엔진 소요/한도(초) |
|---|---:|---:|---:|
| Python | 42 | 0 | 154.157 / 250 |
| Java helper 컴파일 | 입력 수에 더하지 않음 | 0 | 1.110 / 90 |
| Java helper 실행 | 2 | 0 | 0.296 / 60 |
| Windows PowerShell 5.1 | 33 | 0 | 8.579 / 240 |

음성 입력에서 candidate rc1 또는 INCOMPLETE가 나온 것은 기대된 거부이며 harness PASS와 모순되지 않는다. Java helper 컴파일/JVM은 수행됐다. **COMSOL 모델 실행 0과 JVM 전체 0은 다른 주장**이다.

엔진 기록은 제출자 실행 증거의 내부 결속 확인이다. 검토자가 당시 프로세스를 직접 관측하거나 시험을 재실행한 것은 아니다. 엔진 식별 기록의 크기/SHA 대조는 확인했지만 원격 실행파일의 현재 바이트까지 재측정하지 않았다.

## 3. 공개된 fixture 차이의 판정

### PY04-02 — 대체 증거 수용, 실제 NORMAL240 교체 시험으로 부르지 않음

원안은 baseline axes_runtime_settings.csv를 NORMAL240 read-back으로 교체한다. 실제 fixture는 합성 기준 CSV 뒤에 공백 한 바이트를 추가하고 원래 크기/SHA 기대값을 유지한다. 관측은 configuration 축의 SOURCE_IDENTITY 거부다.

`pinned()`는 파일 identity 전체를 기대값과 비교한 뒤 경로를 반환한다. `runtime_evidence()`는 baseline 내용을 읽기 전에 이 함수를 호출한다. 정상 대조군이 같은 경로를 통과하고 변조 입력이 여기서 거부됐다. 따라서 **고정 baseline identity 불일치 거부**의 목적에는 대체 증거를 받아들인다. 실제 NORMAL240 파일을 열거나 그 내용 차이를 재검사했다는 증거는 아니다.

근거: 원안 `LIMITED_VALIDATION_PLAN.json:268`; `build_fixtures.py:78–81`; `extracted/diagnostic_consumer__pinned.py.txt`; `runtime_evidence.py.txt:9`; 결과 `PY04-02_1.json`.

### PY05-03 — runtime 거부 목적의 대체 증거 수용

원안은 runtime tlist와 tables 양쪽의 120.1을 120.15로 바꾼다. 실제 fixture는 tlist만 바꿨다. 관측은 RUNTIME_TLIST 거부다.

`runtime_evidence()`는 tlist를 고정 계약의 requested_times_s와 직접 비교한다. table 숫자 비교보다 먼저 configuration 단계에서 반환한다. 계약이 그대로인 이 사례에서는 tables까지 같은 잘못된 시간으로 바꾸어도 이 독립 대조를 복구할 수 없다. 원안의 기대도 ‘configuration 축에서 비교 전 RUNTIME_TLIST’이므로 이 좁은 거부 목적에 대해 대체 증거를 수용한다.

다만 양쪽을 실제로 동시에 바꾼 시험은 수행되지 않았다. 이 결과를 table 시간 위조 전반의 실증으로 확대하지 않는다. 표 시간 누락·좌표·행 수는 다른 개별 사례의 범위다.

근거: 원안 `LIMITED_VALIDATION_PLAN.json:299–301`; `build_fixtures.py:50,69`; `runtime_evidence.py.txt:6`; `diagnostic_consumer__analyze.py.txt:9–18`.

### PS01-16 — 외부 결과 PASS, 원안의 내부 분기 관측 문장은 미충족

실제 GDecision에 정밀도 경계 문자열을 넣어 INCOMPLETE, GFields에서 INVALID/INCONCLUSIVE를 얻었다. 이 fail-closed 결과는 수용한다. 원안은 추가로 ‘actual path must be confirmed on the target engine’이라고 요구했다. 제출 기록에는 TryParse의 반환값·변환 후 decimal·어느 거부 분기였는지가 없다.

따라서 ‘반올림됨을 실제 확인’ 또는 ‘TryParse 실패를 실제 확인’으로 쓸 수 없다. 코드상 가능한 경로 설명과 실행 관측을 분리한다. 권고는 **내부 분기 특정 대신 외부 거부 보장을 수용 대상으로 한정한다는 문서상 범위 정리**다. 이 축소는 승인권자의 확인을 받아야 한다. 그 요구를 유지한다면 사전 봉인한 한정 관측 1건을 별도 승인해야 하며, 77개 전체 반복이나 생산 변경을 요구하지 않는다.

근거: 원안 PS01-16 expected; `ps_cases.ps1:34,42–54`; `extracted/GDecision.ps1.txt:69–76`; `results/PS_RESULTS.json` PS01-16; 제출자 `INPUT_FIDELITY_NOTES_KO.txt`.

## 4. 캐시·정적 봉인과 재시도

profile 호출 기록은 원 reader 성공 14회 + 동일 바이트 재사용 39회다. **53회 전부 원 reader 재파싱이 아니다.** 캐시 키는 CSV 전체 SHA·시간 튜플·좌표 튜플·domain·limit이다. 원 reader 성공 이후에만 캐시에 넣으며, 실패 입력은 저장하지 않는다. 현재 numeric 소비 경로는 캐시의 프로파일 값을 읽고 차를 만들 뿐 반환 객체를 수정하지 않는다. 수치 계산은 고정 precision 50의 localcontext 아래 수행된다.

고정 source와 이 단일 suite 범위에서는 재사용을 허용 가능한 시험 비용 절감으로 본다. reader 재파싱 횟수나 native 메모리/성능 시험으로 확대하지 않는다. 대형 fixture 원 CSV가 이 ZIP에는 없어 수신자가 각 CSV 값을 독립적으로 전부 재검산하지는 못했다. 생성기·pins·harness·결과 결속을 검토한 것이다.

retry3 seal 변경은 baseline 경로 resolve를 반복하는 검색을 미리 만든 집합 membership으로 바꾼 부분과 새 원점이다. 생산 5파일은 동일하다. CRLF 추출 실패, 이전 Python 시간 초과, retry2 preseal 중지 기록을 결과와 구분해 보존했다. 성공 기록으로 과거 실패를 덮어쓰지 않는다. 현지 모든 과거 상태 보존을 포괄적으로 증명한 것은 아니다.

## 5. 집계 정정 필요 — BMIN-R3-C1 (P2, 기록층)

`FINAL_INPUT_ACCOUNTING.json`의 77행 모두 `status=PASS`와 실제 observed 결과를 담으면서도 `fixture_created=false`, `actual_call_bound=false`를 유지한다. `INPUT_CASE_MAP.json`의 준비 단계 템플릿 값이 최종 집계에 복사된 흔적이다. 실제 시험 부재를 뜻한다고 판단하지는 않지만, 기계 소비자가 상반된 의미로 읽을 수 있다.

원 ZIP·생성 영수증을 수정하지 말고 별도 `ACCOUNTING_CORRECTION.json`을 권고한다. 원본 ZIP/manifest SHA와 각 (ID,input_index)에 결속하고 두 기존 필드는 준비 시점의 값이므로 최종 판정 권위가 없음을 명시한다. Python/PS/Java 각각 실제 입력 생성 방식과 harness/결과 근거를 적는다. 기존 false를 근거 없이 일괄 true로 덮어쓰지 않는다. 관측 시점과 의미를 분리한 정정이면 충분하며, 재시험은 필요하지 않다.

## 6. 전달·예산 경계

TXT에 포함된 외부 영수증/반환 전사의 ZIP·manifest 식별은 실제 받은 ZIP과 일치한다. 마지막 포장 도구 chunk f4653a / rc0, 반환 전 snapshot 431.767661 / 1,660초, 포장 5.328 / 300초로 보고됐다. wall time 5.9335443초를 snapshot에 더하지 않는다.

전사는 후속 제출 자료이지 수신자의 당시 직접 관측이나 원시 OS 감사가 아니다. 별도 원문 DELIVERY_RECEIPT.json의 897 bytes/SHA는 전사에만 있으므로 그 파일 자체를 직접 검증했다고 쓰지 않는다. 전체 경과는 seal_and_run.py의 UTC 차이이며 엔진 소요는 monotonic이다. 예산 이내라는 기록은 확인하되 시스템 시계 변경에 대한 별도 내성 증명으로 확대하지 않는다. 이번 수신 확인을 recipient=null에 소급 기입하지 않는다.

## 7. 다음 최소 행동

1. 새 코드/시험 없이 집계 정정표와 PS01-16 수용 범위 확인을 제출한다. 원 fixture 차이 두 건도 위 한계대로 남긴다.
2. 그 정리가 수용되면 **기존 고정 실행본의 native 150초 승인 요청 준비**로 넘어갈 수 있다. 정확 source/manifest, 기준 NORMAL480 자료, run/cwd/argv, 정책·자원·시간·정리·보존 범위를 함께 제시해야 한다. 이번 review는 그 실행 승인이 아니다.
3. 실제 native 계산은 사용자 별도 승인 뒤다. 960초 자동 연장, 과거 수용 suite 반복, 설정 완화, 다른 solver/물리 조건 추가는 포함하지 않는다.

### 검토 방법 및 자체 오류 공개

수신 ZIP을 데이터로 열어 manifest/JSON/원문/소스 텍스트를 대조했다. 첨부 source import·함수 호출·컴파일·suite·COMSOL 실행 0회다. 검토자 작성 `inspect_archive.py`만 사용했다. 문서 작성 스킬의 원칙에 따라 계획·실제 관측·추론·승인 상태를 분리했다.

검토 중 자료 구조 출력 명령 한 건에 불필요한 `&& nope`가 붙어 셸 rc1이 발생했다(chunk 2d67c0). 구조 출력은 완료됐으나 뒤 명령은 존재하지 않아 실패했다. 첨부 코드 실행이나 생산 자료 변경은 없었다. 이후 독립 자료 대조 명령은 rc0으로 완료했다. 이는 제출자의 시험 오류가 아니다.
