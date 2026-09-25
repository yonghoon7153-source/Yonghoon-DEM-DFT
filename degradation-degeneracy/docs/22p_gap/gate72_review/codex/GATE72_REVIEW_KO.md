# Gate72 수신 검토 — E9-R 수용, E3-R 원장 결속 1건 잔여

2026-09-25. **현재 고정 제출본의 한정 실행 GO: 아니오.** 잔여는 E3-R의 원장 실행 자리 결속 **[P1] 1건**이다. E9-R 재개 명세와 이번 문구 정정은 수용한다. 무제한 독립 GO를 요구하거나 E1/E2/E4를 다시 열어서 내린 판정이 아니다.

## 1. 요청 §3에 대한 답

| 질문 | 답 | 범위 |
|---|---|---|
| ① E3-R 종결 | **아니오 — 대부분 수용, 원장 `evidence.out` 필수 대조만 잔여** | 누락 시 신규 승격 경로가 열리고, 멱등 반환은 대조보다 먼저 발생 |
| ② E9-R 정책 | **예** | grid/fit 실패 즉시 정지 → 동일 plan/token/source 및 재개 가능한 부분 산출 확인 → 명시 `--resume` 정확히 1회 → 재실패 시 재승인 |
| ③ 한정 실행 GO | **현재는 아니오** | 아래 유한 보완 뒤 고정 식별로 재판정. prospective 작성·커밋·본 실행을 지금 승인하지 않음 |

서로 다른 항목을 합쳐 ‘전부 실패’로 처리하지 않는다. 영수증 비교 쌍·semantic 값 일치·fits 결속·복원 지도·봉인 summary의 보완은 확인했다. 이번 잔여는 그다음 **원장과의 연결**이다.

## 2. 대상 식별·직접 확인

| 항목 | 수신 확인 |
|---|---|
| 요청/검토 HEAD | `c4b77ccf71d736dec9162cd5a5377f60f66c0782` |
| 코드 기준 | `82854571d0240951c929d4a9b90260e53ca38e88` |
| 독립 byte 계산 source_digest | `518d4f63076b77e3` — RUN_SCOPE 57개 경로·바이트 |
| 코드 기준 → 요청 HEAD | RUN_SCOPE diff 0 bytes |
| 요청문 Git blob | checkout과 동일, 9,561 bytes / SHA `1db93f99f95a2b5ca61a811c44909000047151d338aefa0cbc1a3909b4697d05` |
| 보고된 전체 시험 HEAD → 요청 HEAD | `b921333322f17a9ac5d92153865da441dc0c9bd7` 이후 문서 3개만 변경 |
| 71차 리뷰 원본 | ZIP 271,500 bytes / SHA `e65ab85ffc764f30a78ad12805651ba0392a6ce4a5b5bfd85c565ae61a620d8e`, 기존 수신본과 바이트 동일. 펼친 manifest 37/37 검증 |
| `_exec_class` | 최상위 JSON 367개, 71차 checkout과 이름·바이트 식별 동일 |
| prospective | 원장의 구조화 값에서 `grid_fit_v5` 항목 미관측. 검토자가 작성하지 않음 |

근거: IDENTITY.json, DATA_AUDIT.json, CODE_TO_HEAD_SCOPE.diff, G71_TO_G72_SCOPE.diff, TEST_REPORT_TO_HEAD.diff. 현재 원격 branch의 이후 이동까지 고정했다는 뜻은 아니며 발송된 commit을 판정했다.

## 3. 수용한 E3 보완

고정 소스의 지정 reader/helper AST를 원문 그대로 추출해 확인했다. 프로젝트 전체 모듈과 과학 분석 코드는 import하지 않았다. `src.io.source_digest`는 별도 byte 계산값으로 대체했다.

- 역할마다 정확히 한 항목과 닫힌 key 집합을 요구한다.
- 같은 schema/canonicalizer의 두 semantic digest가 실제로 같아야 한다. `outputs_agree=True`만으로 대신하지 않는다. 코드는 그 플래그도 여전히 True인지 확인하므로 ‘플래그를 전혀 읽지 않는다’보다는 ‘플래그만 신뢰하지 않는다’가 정확하다.
- rescored source fits SHA와 bundle fits SHA를 대조한다.
- identity 일곱 값의 hex16 형식을 확인한다. 형식 검사가 독립 서명/attestation은 아니다.
- 복원 자리와 묶음 restore_map, sealed_summary SHA와 실제 묶음 파일을 대조한다.
- 기존 한-output 양성 fixture가 생산 계약의 두-output fixture로 바뀌었다.

수신 국소 검사 **14건**: 실물 정상 양성 1건 수용, 결손/불일치/잘못된 leg·validation 등 13건은 reader 또는 뒤따르는 bundle-binding helper에서 거부됐다. R07 복원 자리와 R11 봉인 파일 반례는 reader 단독이 아니라 helper에서 거부된다. 이 구분을 유지한다.

실물 묶음은 index 25개 구성원과 정확 집합·각 SHA, 전체 26개 파일·23,863,555 bytes, index 및 fits SHA를 데이터로 재계산해 영수증과 일치했다. 복원이나 재채점은 하지 않았다.

근거: [reader와 pair 검사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c4b77ccf71d736dec9162cd5a5377f60f66c0782/degradation-degeneracy/tools/preserve.py#L7750), [묶음 결속 helper](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c4b77ccf71d736dec9162cd5a5377f60f66c0782/degradation-degeneracy/tools/preserve.py#L7819), RECEIVER_CHECKS.json.

## 4. E3-R 잔여 [P1] — `out` 대조가 선택적이고 멱등 반환 뒤에 있다

### 4.1 신규 승격: 필드가 없으면 검사하지 않는다

`attach_bundle_evidence` 7936행의 조건은 `if "out" in ev:`다. `LIFECYCLE_OWNED_EVIDENCE_KEYS`(7386–7387행)는 phases/attempt_id/run_spec_digest/attempt_verifier/verifier_origin 다섯 키이며 `out`은 없다. 따라서 앞의 lifecycle-key 검사도 `out` 누락을 막지 않는다.

`preservation_pending` 원장에서 `out` 하나만 빠져도, 다른 전제가 통과하면 원장 실행 자리와의 대조를 건너뛰고 7959–7961행의 full_bundle/current_validated 쓰기 경로에 도달한다. ‘실행 자리가 다르면 거부’는 있으나 **‘실행 자리가 없으면 결속할 수 없으므로 거부’가 없다.**

근거: [필수 키](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c4b77ccf71d736dec9162cd5a5377f60f66c0782/degradation-degeneracy/tools/preserve.py#L7386), [선택적 검사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c4b77ccf71d736dec9162cd5a5377f60f66c0782/degradation-degeneracy/tools/preserve.py#L7929).

### 4.2 멱등 성공: 불일치가 있어도 검사 이전에 반환한다

7917–7921행은 이미 full_bundle이고 receipt 경로/core SHA가 같으면 `idempotent=True`로 반환한다. 이 반환이 원장 `out` 대조보다 먼저다. 그래서 같은 영수증을 가리키되 현재 원장 `out`이 다른 값이거나 없는 상태도 이번 결속 검사를 거치지 않고 성공 응답을 받는다. **이 분기는 새 승격 쓰기가 아니라, 현재 모순을 확인하지 않는 성공 반환 문제**로 구분한다.

근거: [조기 멱등 반환](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/c4b77ccf71d736dec9162cd5a5377f60f66c0782/degradation-degeneracy/tools/preserve.py#L7914).

### 4.3 수신 제어 경로 확인 — 실제 원장 write 0회

추출한 **실제 attach 함수 본문**을 대상으로 선행 검증 진입·OS lock·content-id·write sink를 명시적으로 inert 처리했다. 영수증/묶음 실물 검사는 앞에서 별도 수행했다. 쓰기 함수는 호출되면 제안 문서만 메모리로 읽고 예외를 던져 파일에 쓰지 않는다. 프로젝트 모듈 전체 실행, Linux 잠금 검증, 실제 attach 성공 재현이 아니다.

| 사례 | 입력 상태 | 결과 |
|---|---|---|
| A00 양성 | pending, 일치하는 out | 승격 쓰기 지점 도달, **쓰기 차단** |
| A01 음성 대조 | pending, 다른 out | PreserveError로 거부 |
| **A02 잔여** | pending, out 누락 | full_bundle/current_validated 쓰기 지점 도달, **쓰기 차단** |
| A03 멱등 양성 | full_bundle, 같은 영수증·일치 out | idempotent 성공 반환 |
| **A04 잔여** | full_bundle, 같은 영수증·다른 out | **idempotent 성공 반환** |
| **A05 잔여** | full_bundle, 같은 영수증·out 누락 | **idempotent 성공 반환** |

6개 fixture 모두 호출 전후 바이트 동일. 실제 운영 원장·class·claim·token은 변경하지 않았다. stub 목록과 소스 SHA/행 범위는 RECEIVER_CHECKS.json에 있다. 이 확인의 핵심은 upstream 검증의 완전성을 증명하는 것이 아니라, **기존 검증을 통과한 뒤 새로 넣은 out 분기가 누락/멱등 경로에서 실행되지 않는다는 점**이다.

### 4.4 왜 새 회귀가 놓쳤는가

`test_g71_e3r_07b`(113행)는 `out`을 다른 문자열로 바꾸는 경우만 검사한다. fixture는 항상 out을 넣는다. 누락 반례와 full_bundle 조기 반환 반례는 없다. `attach-binds-the-ledger-run-location-g71` 변이도 이 존재하는-but-다른 값 경로만 겨냥한다. 보고된 3/3 변이 검출과 이번 잔여는 모순되지 않는다.

현재 실물 과거 `paired_fixed5_v4`의 원장 evidence에는 실제로 out이 없다(DATA_AUDIT.json). 이것을 새 가짜 실행 증거의 증명으로 단정하지도, 현재 값으로 소급 채우라고 요청하지도 않는다. 새 회귀의 실물 양성은 reader/helper 검사이며 원장 out/멱등 경로를 확인하지 않는다. **과거 자료를 읽을 수 있음과 새 승격·현재 결속 성공을 허용함을 구분**해야 한다.

### 4.5 유한 종결 조건

1. 신규 pending→full_bundle 소비에서 원장 `evidence.out`을 필수 비어 있지 않은 문자열로 확인하고, 묶음/영수증에 결속한 실행 자리와 일치해야 진행한다. 필드 부재를 skip하지 않는다.
2. 멱등 성공을 돌려주기 전에도 그 실행 결속을 확인한다. 역사적 out 부재는 임의 보충·과거 record 재작성 없이 별도 미결속/거부로 처리할 수 있다. 그것을 새 승격 또는 무조건적 현재 결속 성공의 예외로 쓰지 않는다.
3. 정상 대조 + pending의 누락/불일치 + full_bundle의 누락/불일치 회귀를 고정하고 거부 시 원장 불변을 확인한다. 위 6개 경우로 충분하며 E1/E2/E4 전면 구현·서명·새 principal·과거 class 이관을 추가 요구하지 않는다.

실행 전 사람이 `out`을 한 번 읽는 조건만으로 **typed 소비자 자체가 닫혔다**고 표시하지 않는다. 이번 한정 실행에도 채택한 attach의 성공 의미에 관한 잔여이므로 E3-R을 종결할 수 없다.

## 5. E9-R와 문구 정정 수용

명시 초기 argv와 재개 argv의 차이 `--resume`이 분명하다. `run.sh` 522–557행은 이 플래그를 하위 grid/fit에 전달한다. `precheck_leg_run` 7319–7354행의 resume 분기는 token 파일·claim 소유 증명과 source_digest를 확인하고 `kind=resume`을 반환한다. 명세는 여기에 사람이 부분 산출 온전성까지 확인하도록 요구한다.

따라서 **grid/fit 실패에 대한 최초 실행 1회 + 확인 후 재개 최대 1회**의 정책을 수용한다. finalize 거부 또는 archive/영수증/attach 실패까지 같은 재개 argv로 자동 해결하는 승인이 아니다. 그 단계는 정정된 E9-4의 별도 중지/기록 절차가 유지된다. `--resume`의 모든 장애 복구 성공이나 실제 실패 후 재개를 수신 측에서 시험한 것은 아니다.

D7의 최종 승인 HEAD/RUN_SCOPE 구분, D8의 `unset CANONICAL_RUN LEG`, D9의 4+4+3=11 표본은 72차 정본 문구로 수용한다. 과거 71차 문서에 남은 역사적 8/옛 digest를 새 실행 식별로 사용하지 않는다.

E6의 requirements*.txt 복사와 자식 프로세스 source_digest 동일성 시험은 소스 변경을 확인했다. 이 수신 검토에서 그 자식이나 전체 pytest를 실행하지 않았다. 기존 격리/배타 운영 창의 한정 수용을 유지한다.

## 6. 시험 결과·보존·다음 요청

송신자의 1869 passed/2 xfailed·34:59·smoke rc0·152 passed/1 xfailed·후속370 passed 및 RED→GREEN은 보고된 실행 증거다. 새 시험 정의 14개와 변이 대상, 시험 HEAD 이후 문서 3개만 변경된 사실은 직접 대조했다. 그 원격 프로세스/로그를 직접 재관측하거나 full suite를 재실행한 것으로 쓰지 않는다. 원래 통과를 실패로 재분류하지 않는다.

다음 요청은 **E3-R 원장 실행 자리 필수화/멱등 순서 수정만**이면 된다. 최소 diff·위 한정 회귀·변경 후 commit/source_digest를 제출하면 E9를 다시 열지 않고 재검토할 수 있다. 코드 식별 변경에 따른 영수증 갱신은 기존 승인 범위 안에서만 수행하며, 이 리뷰가 새 복원·재채점·class 변경을 승인하는 것은 아니다.

GO가 아직 없으므로 prospective를 쓰거나 본 실행을 시작하지 않는다. 종결 뒤에도 사람이 계획을 커밋한 최종 승인 HEAD, 코드 범위 동일성, 실행별 입력/환경 및 배타 창을 확인해야 한다. 정상적인 다음 단계와 이번 P1 잔여를 구분한다.

이번 검토: Git 객체 읽기와 별도 checkout 생성, 독립 byte/JSON/YAML 검사, 지정 AST reader 및 write 차단 제어 경로 검사, 보고서/소유 fixture 작성. COMSOL·Java·과학 분석·grid/fit·복원·운영 원장/class 변경·full pytest/smoke 실행은 0회다. 검토 checkout 추적 파일 보존 결과는 PRESERVATION_AFTER.json에 기록한다.
