# Gate88 검토 결과

2026-10-04. **수정 요청 — 라운드 2b 종결 보류. P1 한 건인 G88-N1만 남긴다.** 기존 G87-N1의 정상 fit-only 완료 연결은 고쳐졌다. 그러나 저장된 완료 receipt를 재개·최종화할 때 입력 묶음의 구성원 검사를 다시 하지 않아, 필요한 증거가 누락되거나 바뀐 상태도 `executed`로 옮길 수 있다.

이는 고정 코드의 정적 호출·데이터 흐름 판정이다. 받은 코드·pytest·변이·복원·COMSOL은 실행하지 않았다. 수치 결과가 틀렸거나 과거 산출이 오염됐다는 판정은 아니다. 2a와 이전 수용 부분은 유지하며 실행 GO를 부여하지 않는다.

## 고정 대상과 확인 범위

| 항목 | 직접 확인 |
|---|---|
| 요청 커밋 | `d6056415baac1a80496274407b1a22f718ba4ad5` |
| 생산 코드 | `e462a3d1929c9a6be4a8ca3665dce7f80bc7134d` |
| 독립 source_digest | RUN_SCOPE 58파일 원문으로 재계산한 `7dd546baaee9e823` 일치 |
| 생산 변경 | 87차 대비 `src/fitting.py`, `tools/preserve.py` 두 파일만. 나머지 56파일 Git blob 동일 |
| 생산 코드 이후 | 요청 커밋까지 7커밋이며 RUN_SCOPE 변경 없음 |
| 본진 계보 | 동결 `e2f5697192b2008d0a11b7334c2d3f3546a85809`가 요청 커밋의 조상임을 비교 API의 merge-base로 확인 |
| 수신 원문 | 소스·문서·로그의 UTF-8 바이트를 Git blob SHA-1과 대조. 로그 16개는 README의 크기·전체 SHA-256도 모두 일치 |

현재 브랜치를 checkout하거나 원격 이력을 바꾸지 않고 고정 커밋을 읽었다. 검토 자료의 JSON 안에 원문 문자열과 원 Git blob 식별을 보관했다. 정적 감사 프로그램은 검토자 작성 코드이며 받은 모듈을 import하지 않는다.

## G88-N1 P1 저장된 inputs를 최종화에서 다시 검사해야 함

기록 시점에는 `phase_done()`가 공통 `_assert_external_input_binding(receipt)`를 호출한다. 이 함수는 `inputs`의 정확한 키 집합·hex64 값·묶음 digest 재계산을 확인한다. [검사 본문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d6056415baac1a80496274407b1a22f718ba4ad5/degradation-degeneracy/tools/preserve.py#L6721), [기록 시 호출](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d6056415baac1a80496274407b1a22f718ba4ad5/degradation-degeneracy/tools/preserve.py#L6949)

반면 최종화의 fit-only 분기는 아래 **문자열 세 값**만 비교한다.

- `consumed.external_input`
- 계획의 `fit.in_digest`
- receipt의 `input_package_digest`

최종화에는 `receipt.inputs`의 존재·형식·재계산 검사도, 위 공통 검사 함수 호출도 없다. `resume_claim()` 역시 token·계획 식별을 확인할 뿐 이 입력 구성원을 검증하지 않는다. [최종 비교](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d6056415baac1a80496274407b1a22f718ba4ad5/degradation-degeneracy/tools/preserve.py#L9130), [재개](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d6056415baac1a80496274407b1a22f718ba4ad5/degradation-degeneracy/tools/preserve.py#L7559)

### 좁은 반례

정상 v3 계획·token·attempt 아래 `phase_done("fit", valid_receipt)`까지 끝났다고 하자. 그 뒤 **저장 claim의 `phases.fit.receipt.inputs`만 삭제**하고 나머지는 그대로 둔다. 실제 변조나 실행을 이번 검토에서 수행한 것은 아니며, 다음은 정적 경로 추적이다.

1. claim 최상위 키·소유 증명·계획 identity는 변하지 않아 재개 검사를 통과한다.
2. fit phase는 존재하고, fit-only 집합도 계획과 일치한다.
3. fit은 유일한 첫 phase라 선행 phase 소비 대조는 건너뛴다.
4. 남아 있는 세 digest 문자열은 모두 원래 값 K이므로 새 최종 비교도 통과한다.
5. `inputs`가 없는 receipt를 포함한 snapshot이 실행 기록에 복사된다.

`inputs.curves_sha256`만 다른 유효 hex64로 바꾸거나 inputs에 키를 추가해도 같은 미검사 경로다. 이것은 완전히 다른 위협 모델을 추가한 것이 아니다. 이번 f03_03과 f03_06의 `receipt_package_tampered`도 **phase 기록 뒤 durable claim 변조**를 검토 대상으로 삼았다. 단지 그 두 시험이 변조하는 필드와 이번에 빠진 필드가 다르다.

누락된 자료는 수치 재계산으로 복구할 문제가 아니다. 최종화가 바로 읽어 원장에 옮길 receipt의 내부 결속을 먼저 검증해야 한다. [snapshot 복사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d6056415baac1a80496274407b1a22f718ba4ad5/degradation-degeneracy/tools/preserve.py#L9174)

### 기존 시험이 놓치는 이유

f03_02와 f03_06의 inputs 관련 음성은 **phase_done에 잘못된 receipt를 처음 주는 경우**를 검사한다. 최종화 뒤쪽을 겨냥한 f03_06은 `input_package_digest`만 바꾼다. 따라서 작성 시점의 inputs 검사와 최종화의 digest 문자열 대조는 각각 시험됐지만, **작성 후 변경된 inputs의 소비**는 검사되지 않는다. 2133 PASS·395/395를 이 빈칸이 없다는 증거로 확대하지 않는다.

### 필요한 최소 보완

별도 사용자 승인 후, fit-only 최종화가 사용하는 **같은 snap의 receipt**에 기존 공통 `_assert_external_input_binding` 검사를 적용한다. 원장 상태 변경 전에 수행하고, 기존 계획/consumed/receipt digest 비교는 유지한다. v2 순서·키·receipt·기존 수용 영역은 바꾸지 않는다.

정상 durable receipt 양성, 기록 후 inputs 삭제·유효 hex64 값 교체·추가 키·비hex 값 음성을 실제 finalize 경로로 확인하라. 거부 이유를 결속 오류로 한정하고 원장 바이트 불변을 대조한다. 새 최종 검사 호출을 제거하는 변이가 이 회귀를 깨는지도 고정한다. 연구 계산이나 COMSOL은 필요하지 않다. 이 회신은 수정·시험 실행 승인이 아니다.

## 수용하는 부분

| 항목 | 판정 |
|---|---|
| 원래 G87-N1의 grid 선행 거부 | 정상 경로 수정 수용. v3 외부 입력은 fit-only, v3 null은 index에서 거부, 비-smoke 완료·최종화 양성이 연결됨 |
| 입력 생산자 의미 | 수용. 가짜 grid 대신 실제 staged 입력 묶음과 external_input을 기록함 |
| v2 불변 | 한정 수용. legacy grid→fit 순서·소비 결속 유지, fit receipt에 새 입력 결속을 싣지 않는 분기 확인 |
| 87차 수용 부분 | 유지. v2/v3 builder·stage3 축·승인/입력 검사·preflight·prepare·수치 본체·문맥 진입 함수의 AST 동일. run.sh·src/io.py·src/grid.py 바이트 동일 |
| 재개·상태 view | 정상 도달 상태의 fit-only 표시는 수용. CLAIM_PHASES 필터 유지의 등가 설명은 임의로 손상된 durable state 전체에 대한 보증으로 확대하지 않음 |
| 새 영수증 | 이력 보존·내용 차이·원장 앵커 범위 한정 수용 |
| 라운드 2b 종결 | G88-N1 때문에 보류. 2a·이전 종결은 재개방하지 않음 |

새 영수증의 이전 원문 두 개는 history와 바이트 동일하다. 차이는 core_sha256, validator_source_digest, stamp의 validator_commit·시각·platform뿐이다. src_io 식별·producer·bundle·outputs·restore·35/34 검사 수는 그대로이며, 원장 변경도 두 leg의 core와 validator digest뿐이다. canonical YAML core hash 재생성·격리 복원·재채점은 수행하지 않았다.

## 로그 수용과 절차 한계

원문 13·14·15에서 `07aefea11ffb15124f9705d186d5e087d2a8983e`의 시작/끝 HEAD, dirty=0, pytest 2133 passed/1 xfailed/rc0, smoke rc0, 전체 변이 395 hit/0 미검출/rc0를 확인했다. 원문 11의 g88 21/21도 확인했다. 이는 **보존된 제출자 기록의 대조**이며 검토자의 원격 프로세스 관측·재실행은 아니다.

RED 9/7, 영수증 재생성 전 820/9, 탐침 오염 중단, baseline 충돌, 자체 점검 추가를 위한 중단은 각각 보존된 다른 회차로 취급한다. emit-expect의 미선언 표시를 전부 실제 변이 생존으로 세지 않았다. 생존/오염 회차를 최종 성공에 합산하지 않는다.

고정 scratch 동시 사용과 격리 fixture 없는 탐침은 절차 문제다. 최종 순차 기록을 수용하되, 시작/끝 dirty=0만으로 실행 중 작업 트리 전체의 무변경을 증명했다고 쓰지 않는다. §6-l은 별도 sandbox 재생과 본 checkout 문서 작업을 구분한 제출자 설명으로 남긴다. 발송 HEAD의 docs-lint 358 PASS는 발송문 보고이며 이번 16원문 집합에서 별도 원문 확인하지 않았다. 이것만을 이유로 추가 전체 재시험을 요구하지 않는다.

## 다음 경계

후속은 G88-N1 한정 보완과 그 증거 제출뿐이다. 새 연구 leg·운영 v6 계획 항목·세대표 등록·p_ini·class/투영 게시·requirements 변경·실행 GO는 이 리뷰에서 승인하지 않는다. PyBaMM 고정은 이미 분리한 별도 라운드로 유지한다.

문서 작성 스킬에 따라 정상 경로의 수용, 잔여 결함, 제출자 로그, 정적 추론을 구분했다. 산출물 개수나 시험 개수를 새 기능 검증 실적으로 부풀리지 않았다.
