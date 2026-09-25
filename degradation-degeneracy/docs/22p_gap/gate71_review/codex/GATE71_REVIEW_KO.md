# Gate71 수신 검토 — 한정 실행 GO 보류, E3·E9 잔여만 보완

2026-09-25. **현재 제출본에 대한 한정 실행 판정: NO-GO.** E1/E2/E4의 명시된 한계를 수용해도, 선택한 보존 전이의 E3와 실패 처리 명세 E9가 남는다. 무제한 독립 GO를 요구해서 내린 판정이 아니다.

이번에 확인한 잔여는 **E3 소비 계약 [P1] 1건, E9 재개 명세 [P2] 1건**이다. 기존 종료 목록 안의 잔여이며 새 보안 과제를 더한 것이 아니다. G70-N1, E5, E6의 이번 실행 한정 조치, E10의 양성 fixture 보완은 수용한다. E7/E8은 유지한다.

## 1. 판정 대상과 직접 확인

| 항목 | 수신 확인 |
|---|---|
| 요청/HEAD | `4505b70c6e63453e0424239cac7d48488fee022a` |
| 코드 대상 | `876429562f6a69b59793c70700cb5b375391ab67` |
| 직접 계산 source_digest | `b705a21a1237ec73` — RUN_SCOPE 57개 파일의 경로·원문 바이트로 별도 계산 |
| 코드 대상 → 요청 HEAD | RUN_SCOPE diff 0 bytes |
| 요청문 | Git blob와 checkout 바이트 동일, SHA `9f8d453b7245000d67ec24fa26dbe1ecbc26397fa4730cc4da15307e945a9748` |
| 전체 회귀 보고 HEAD → 요청 HEAD | `0e6348be… → 4505b70c…`에서 문서 3개만 변경. 코드·시험·의존 파일 변화 없음 |
| 등록부 | tracked/disk 각각 367. modern 351 / legacy 16. 문구 분류 4+12+174+177 일치 |
| 검토 전후 | 분리된 검토 checkout의 DD 추적 파일 2,459개 크기·SHA 동일, Git clean |

등록부 분류는 문구·형식의 확인이며 367건의 실제 과학 실행을 독립 재현했다는 뜻이 아니다. 근거 파일: `IDENTITY.json`, `SOURCE_BEFORE.json`, `PRESERVATION_AFTER.json`, 세 diff와 `EXCERPT_IDENTITIES.json`.

## 2. E3-R [P1] — 생산자가 거부하는 부분·불일치 영수증을 새 소비자가 수용

### 실제 누락

새 `read_verification_receipt`는 output마다 비어 있지 않은 `semantic_sha256`·`canonicalizer`, `rescored_summary` 역할의 존재와 `outputs_agree is True`를 확인한다. 그러나 다음을 대조하지 않는다.

- `sealed_summary`라는 비교 상대가 실제로 있는지.
- 같은 schema/canonicalizer의 두 semantic SHA가 실제로 같은지.
- `rescored_summary.source_file_sha256`이 영수증의 `bundle.fits_sha256`과 같은지, 또는 그 필드가 있는지.

이후 `attach_bundle_evidence`는 묶음/index/member SHA와 **bundle 쪽** fits SHA를 디스크와 대조하지만, 위 output 모순을 다시 확인하지 않고 `current_validated`와 `rescored_from_restored_fits=True`를 기록한다. 원장 실행 evidence도 lifecycle 키의 존재만 확인하고, 영수증 `restore.run_dir_relative`와 원장 `evidence.out`/해당 실행 산출 식별을 대조하지 않는다.

근거: [reader](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4505b70c6e63453e0424239cac7d48488fee022a/degradation-degeneracy/tools/preserve.py#L7737), [attach의 디스크 대조](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4505b70c6e63453e0424239cac7d48488fee022a/degradation-degeneracy/tools/preserve.py#L7796), [원장 전이](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4505b70c6e63453e0424239cac7d48488fee022a/degradation-degeneracy/tools/preserve.py#L7830).

### 수신 확인 범위와 결과

실제 고정 소스에서 지정한 AST 함수 정의만 그대로 추출해 **읽기 함수와 순수 비교 술어**를 확인했다. 프로젝트 전체 모듈은 import하지 않았고 `src.io.source_digest`만 별도로 측정한 값으로 대체했다. 실제 `attach`, 원장 write, class 승격, 복원, 재채점은 실행하지 않았다.

기준 입력은 커밋에 있는 `paired_fixed5_v4.validate.yaml`의 바이트다. 변형은 검토자 소유 파일에서만 했고 core 자기 해시는 다시 맞췄다. 따라서 깨진 SHA가 아니라 **내부 주장 간 모순**을 검사한다.

| 입력 | 새 reader | 기존 생산자의 순수 `_outputs_agree` |
|---|---|---|
| 원래 실물 영수증 | 수용 | True |
| 다른 leg / 잘못된 core SHA / validation.ok=False | 각각 거부 | 해당 없음 |
| sealed_summary 제거, outputs_agree=True 유지 | **수용** | **거부: 비교 상대 없음** |
| 두 summary의 semantic SHA 불일치, outputs_agree=True 유지 | **수용** | **거부: 불일치** |
| source fits SHA를 다른 값으로 변경 / 필드 제거 | **둘 다 수용** | 이 술어의 검사 범위 아님 |
| restore 경로를 `results/ANOTHER_RUN`으로 변경 | **수용** | 이 술어의 검사 범위 아님 |

전체 reader 11건(정상·거부 대조 4, 결손/모순 수용 7), 순수 생산자 비교 3건을 기록했다. 나머지 수용 2건은 비hex semantic 값과 개별 producer identity의 null이다. 후자는 넓은 “typed” 표현의 한계로만 기록하며 독립 attestation 신규 조건으로 세지 않는다.

`READER_CHECKS.json`은 국소 소비자 실측이다. **전체 Linux attach 경로의 승격 성공 실험이라고 표현하지 않는다.** 실제 전이 영향은 고정 소스의 후속 호출과 write 분기를 정적으로 확인한 결과다. 이 결과가 현재 실물 영수증의 수치가 틀렸다는 뜻도 아니다.

### 왜 기존 회귀가 놓쳤나

`test_gate70_defensive.py:302–323`의 정상 fixture 자체가 `rescored_summary` 하나만 넣고 `outputs_agree=True`를 설정한다. `:372–387`은 이를 full_bundle/current_validated의 양성으로 사용한다. 반면 생산자는 [비교 상대와 실제 일치](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4505b70c6e63453e0424239cac7d48488fee022a/degradation-degeneracy/docs/22p_gap/make_receipt.py#L330)를 요구한다. 새 소비자가 생산 계약보다 약한 fixture를 정답으로 삼은 것이다.

### E3의 유한 종결 조건

1. 선택한 schema 2 영수증의 필수 비교 쌍·형식·실제 semantic 일치·source fits 결속을 소비 단계에서 확인한다. `outputs_agree` 한 필드로 대신하지 않는다.
2. 원장의 해당 실행과 복원 경로/산출 식별을 **기존 evidence와 묶음에 있는 값으로** 대조한다. leg 문자열과 lifecycle 키 존재만으로 대체하지 않는다.
3. 실물 정상 양성과 위 결손·불일치·다른 실행 반례를 소유 fixture에서 검사하며, 거부 시 원장이 불변임을 확인한다. 원래 생산자가 만들 수 없는 한-output fixture를 정상 계약으로 유지하지 않는다.

서명, 별도 OS principal, object-lock, E1 projection의 독립 producer attestation을 추가하라는 요청이 아니다. 이미 요청한 “실제 상태·bundle 식별을 결속하는 typed 소비”의 종결이다. YAML index fail-closed와 member 재해시는 수용한다. 실제 index 25개 구성원의 집합·SHA도 데이터로 직접 대조해 일치했다.

## 3. E9-R [P2] — 실패 뒤 ‘같은 명령’은 chunk 재개 명령이 아니다

[요청문 E9-4](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4505b70c6e63453e0424239cac7d48488fee022a/degradation-degeneracy/docs/22p_gap/GATE71_REQUEST.md#L115)는 grid/fit 중단 뒤 같은 명령을 다시 실행해 이어간다고 한다. 그러나 최초 명령에는 `--resume`이 없고, `run.sh:56` 기본값은 false다. 하위 두 단계도 true일 때만 그 플래그를 받는다(`:522–557`).

[grid.py:601–612](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4505b70c6e63453e0424239cac7d48488fee022a/degradation-degeneracy/src/grid.py#L601)는 resume=false이면 완료 집합을 비우며, 기존 기록이 있으면 재계산/청크 중복 누적을 경고한다. `fitting.py:1524–1526`도 완료 집합을 resume일 때만 읽는다. **claim 소유권 재개와 청크 건너뛰기는 다른 조건**이다.

이 검토에서 실패 실행이나 청크 재계산을 실제로 유발하지 않았다. 명세와 제어 분기의 직접 불일치다.

종결은 명확한 실패 정책으로 충분하다. 같은 plan/token/source/부분 산출 상태가 재개 가능한지 확인한 뒤 `--resume`이 포함된 별도 재개 argv와 허용 횟수를 고정하거나, 이번 한정 실행에서는 실패 즉시 정지·재승인으로 좁혀라. 코드 변경이나 본 계산을 먼저 요구하지 않는다. `--resume`을 붙이기만 하면 모든 실패가 복구된다고 보증하지 않는다.

### 함께 정정할 명세 표현 — 별도 차단 항목으로 늘리지 않음

- 실행 checkout은 사람이 prospective 항목을 커밋한 **최종 승인 HEAD**여야 한다. `87642956`은 코드 기준이다. 그 옛 커밋으로 checkout하면 새 계획이 없으므로, 최종 HEAD와 RUN_SCOPE 동일성을 함께 적는다.
- `CANONICAL_RUN`을 “주지 않음”은 상속된 환경변수 제거와 다르다. 실제 shell에서 unset/고정 여부를 명시해 `docs/RESULTS.md`를 보호한다.
- E4는 §1·§4의 premise 4 + g70 4 = 8과 E9-5의 4+1이 충돌한다. 보고된 8개 범위에 맞춰 통일한다.
- E6 격리 코드는 root `requirements.txt`·`requirements-gpu.txt`를 복사하지 않는다. “격리 tree의 source_digest까지 원본과 동일”이라는 주석은 보장하지 않는다. 운영 authority 격리/배타 창의 수용과 구분해서 문장을 좁힌다. 이를 새 본 실행 차단이나 351개 이관 요구로 확대하지 않는다.

## 4. E1–E10 종결표와 요청 §3 답변

| ID | 이번 판정 | 남는 경계 |
|---|---|---|
| E1 | 명시 한계 수용 | 독립 projection producer 결속을 입증한 것은 아님 |
| E2 | 명시 한계 수용 | 디스크 자기 측정이며 독립 launcher attestation 아님 |
| E3 | **미종결** | index 보완 수용. 위 E3-R 소비 계약만 남음 |
| E4 | 명시 한계 수용 | 표본/수행 주체를 구분, 8/5 문구 정정 |
| E5 | **수용** | 두 typed variant 및 sealed의 bool 판정. 역사적 class 수정 없음 |
| E6 | **이번 실행 한정 수용** | 격리 + 전용 checkout/배타 창/전후 delta. 과거 등록부 재분류 승인 아님 |
| E7 | 수용 유지 | F50b와 git_dirty 유지 |
| E8 | 종결 유지 | 이전 항목 재개봉 안 함 |
| E9 | **실패 정책 보완 필요** | 초기 명령/목적/별도 보관 순서는 수용. 재개 명세를 고정할 것 |
| E10 | **보완 수용, 증거 출처 한정** | 양성 fixture 변경과 최종 시험 코드 동일성 확인. 전체 Linux 실행은 송신 보고 |

§3 답: **① E3 아니오 / E5 예 / E6 예(명시 운영 범위) / E10 예(송신 실행 증거 범위), ② 한계 라벨 예(수량 정정), ③ E9 부분 수용, ④ 현재 한정 GO 아니오.**

G70-N1의 shell→Python 플래그 경계는 수정 및 새 하위 parser 회귀를 정적으로 확인해 종결한다. 이번에 shell이나 Python grid/fit을 실행하지 않았다. E5는 지정 typed 함수의 대조군 5건과 기존 367개 JSON을 읽어 확인했다. promotion writer→reader 전체 경로를 수신 측이 재실행했다고 쓰지 않는다.

E10의 1855 passed/2 xfailed, strict smoke rc0, 후속 404 passed는 송신자의 커밋된 요청/보고 및 사용자 전달값이다. 이번에 그 원격 프로세스를 직접 관측하거나 43분 전체 suite를 재실행하지 않았다. `0e6348be→4505b70c`가 문서 3개만 바뀐 것은 직접 확인했다. raw 로그의 독립 수신 검증 완료로 확대하지 않되, 이것만을 이유로 동일 suite 반복을 새 조건으로 추가하지 않는다.

## 5. 다음 회신에 필요한 최소 자료

범위를 **E3-R + E9-R**로 유지한다. E1/E2/E4 전면 구현이나 과거 class 정리를 요구하지 않는다.

1. E3 소비자 제한 수정 diff, 유효한 생산 계약 양성 및 결손/불일치/다른 실행 반례, 실패 시 원장 불변 근거.
2. 수정 후 최종 commit/source_digest. RUN_SCOPE 변경 전후를 구분하고 해당 validator 영수증/영향 회귀의 식별을 맞춘다. 실행 승인 없는 복원·재채점은 이번 리뷰를 근거로 수행하지 않는다.
3. E9의 정확한 재개 또는 실패 즉시 정지 정책, 승인 HEAD/환경변수/E4 수량 정정.

그 뒤 고정된 최종본에 대해 한정 GO를 판단한다. **지금 prospective 계획 항목을 작성/커밋하거나 본 실행을 시작하라는 승인이 아니다.** GO 이후에도 사람이 확정한 계획 commit과 실행별 전제는 필요하다. 목표는 synthetic grid/fit 기능·보존 진단이며 실셀 정량 타당성 보증이 아니다.

## 6. 실행·보존 기록

- 검토자 도구: 독립 byte identity, 선택 AST reader/pure predicate, 데이터-only index/member hash, 소스 정적 대조. reader 검사 실제 rc0 (`0f2f90`), 식별 확인 rc0 (`959347`), 전후 보존 확인 rc0 (`3429c3`).
- COMSOL·제공된 Java·과학 분석 프로그램·grid/fit 본 계산·복원·class/운영 원장 변경: 모두 0회. full pytest/smoke 재실행도 0회.
- reviewer 입력 fixture/보고서 작성과 Git 객체 fetch/분리 checkout 생성은 있었다. 파일시스템 쓰기 0이라고 주장하지 않는다.
- 중단 전 identity 도구는 promisor Git 객체를 가져오지 못해 rc1로 끝났다. 권한을 받은 뒤 같은 읽기 검사를 재개해 완료했다. 조회 중 존재하지 않는 후보 파일 경로 오류도 있었으며 제품 실패로 분류하지 않는다.
- 보존 범위는 **검토 checkout의 DD 추적 파일 2,459개**다. 생산자 PC 전체, 모든 프로세스, 역사적 모든 원자료를 원격 검증했다는 뜻이 아니다.

수신 스크립트는 증거/재현 설명이며 자동 실행 요청이 아니다. 본 리뷰는 수정·계산·복원·승인 활성화·외부 발송을 수행하지 않았다.
