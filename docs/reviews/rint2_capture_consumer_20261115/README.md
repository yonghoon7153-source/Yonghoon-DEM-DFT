# Rint Q12 — 조립 결과의 실제 소비 지점 준비

## 1. 확인 범위

바탕 8704a2d725b885a8eb11505c9a9d76bab7937f9e. 실행 소스 고정 핀은 64e4d213e8267bafaf3ae5af00a42996cefd3f33 그대로다. 이전 `docs/reviews/rint2_capture_map_20261114/README.md`의 생산자 지도를 실제 소비 함수 `scripts/step3_sigma.py`의 `solve_sigma_z`까지 이었다.

`consumer_map.json`은 두 고정 소스의 Git blob·SHA와 선택 분기/대입/호출 위치다. source import·조립·solve·실제 배열·σ 열람0. 실행 코드, S0/Q11/⑥ 블록, 등록·운영 봉인 무변경, 전체 HOLD.

## 2. 분기별 실제 순서

| 경로 | 고정 소스 위치 | 관찰 | Q12 수집기의 다음 계약 |
|---|---|---|---|
| cjunc 미사용 | step3 2321 조건 거짓 | 기존 L/b 경로가 계속됨 | 이번 cjunc 완료 capture로 조용히 대체하지 않음. 적용 범위를 명시 |
| graph_only | 2325 build, 2327–2331 return | graph 지문 경로가 주 solve 앞에서 반환 | 그래프 지문 존재를 CSR/RHS/원 DOF capture 완료로 세지 않음 |
| reason 반환 | 2332–2337 | 단락·관통 없음 등 reason 경로는 주 solve 전에 반환 | 정상 조립 양성 행으로 채우지 않음. 기존 reason 의미는 유지 |
| 완료 cjunc | 2338–2341 | out에서 L/b/판 결합·좌표·개수를 소비함 | 같은 완료 객체를 묶을 위치 후보. 현재 out에는 원 DOF가 없음 |
| 주 solve | 2344–2347 | LAST_CG 초기화 → _solve_cg(L,b) → 잔차 계산 | 조립 동등성 수집의 후보 위치는 주 solve 전. 풀이 결과에서 원 조립을 재구성하지 않음 |
| 후속 진단/반사실 | 2417–2423, 2458 | record와 sys 사용, 조건부 sv_counterfactual 호출 | 주/반사실 역할을 분리. 이후 graph/state를 읽어 앞 시도 capture로 귀속하지 않음 |

graph_fp=True는 graph_only 또는 CONV_CERT와 SV 활성 조합에서 요청한다(2325–2326). 일반 build를 호출하는 모든 경로에서 지문이 존재한다고 가정할 수 없다. 수집 목적의 지문 요구를 추가하면 기존 옵션/호환성·핀 영향 검토가 필요하다. 이번에는 조건을 바꾸지 않았다.

최종 완료 반환은 carbon_junction 2819의 L, b, Ab, gb, At, gt, cb, ct, n_dof다. 원 DOF는 2789에서 `np.flatnonzero(kept)`로 그래프 지문에 쓰이고 2797에서 재번호화되지만 반환되지 않는다. 따라서 step3 2338에 기록 호출 하나만 덧붙여 완전한 capture라고 할 수 없다.

## 3. 두 연결을 함께 준비할 것

1. **생산자:** 같은 kept 상태에서 원 번호 순서를 확보하고 완료 조립 객체와 귀속을 결속한다. count나 좌표로 원 번호를 추측하지 않는다.
2. **소비자:** 2338–2341의 완료 분기를 지나 주 solve 전에 CSR/RHS/판 결합/원 DOF/graph 및 시도 출처를 같은 수집 구간으로 묶는다. graph_only·reason 분기는 그 전에 분리한다.

이는 위치 제안이지 구현/소유권 선택이 아니다. 기존 `docs/reviews/rint2_capture_ownership_20261114/ownership_options.md`의 O1 단일 소유 / O2 일관 사본 / O3 불변 객체는 미선택이다. out과 self.sys의 배열 별칭, graph_fp의 수명, 9개 descriptor의 순차 해시는 이전 한정 그대로다.

현재 소스는 이 Q12 수집 계약을 보장한다고 표방한 구현이 아니므로, 누락한 capture 연결을 새 원장 결함이나 현재 R 런의 틀린 결과로 계상하지 않는다. 반대로 현재 주 solve가 가능하다는 이유로 Q12 동등성 자격을 얻었다고 하지도 않는다.

## 4. 통합 전 작은 분기 시험 준비

전부 **미실행**이며 기존 CAP01–10에 연결할 준비다. 고정 소스 테스트 통과나 신규 고유 시험 수로 보고하지 않는다.

| 경계 | 작은 입력 / 대조 | 기대 |
|---|---|---|
| 적용 대상 | cjunc 없음 / 있음 | 수집 대상 지위가 명시되고 legacy를 cjunc 증거로 승격하지 않음 |
| 조기 반환 | graph_only와 reason 각각 | 정상 완료 capture가 생성되지 않음. 이유/역할을 보존 |
| 지문 조건 | 일반 / CONV_CERT+SV / graph_only 조합 | 요청하지 않은 지문을 있다고 채우지 않음. 캡처 요구의 미충족을 드러냄 |
| 원 DOF·plate 별칭 | 삭제된 DOF가 있는 작은 순서, 후속 원 배열 변경 | 정확한 kept 순서와 한 완료 객체의 결속. 후속 변경이 기존 기록을 바꾸지 않는다는 선택 계약 확인 |
| 주/반사실 | 주 완료 뒤 별도 반사실 호출 | 역할·시도별 capture 구별. 주 증거를 다른 조립의 증거로 재사용하지 않음 |
| capture 실패 | solve 직전 descriptor 또는 출처 결속 실패 | 채택 가능한 완결 기록 없음. 실제 solve 중단/계속 정책은 구현 전 명시적으로 정함 |

마지막 행의 정책을 이번 문서로 바꾸지 않는다. 기존 실행을 자동 중단하거나 계속시키는 코드도 넣지 않았다. 6개 고유 기하 열쇠·지원 환경별 명부/비용 계획은 이전 비준 그대로이며 실제 대조 GO가 아니다.

## 5. 재현과 다음

리포 루트에서 `python -I -X utf8 -B docs/reviews/rint2_capture_consumer_20261115/inspect_consumer.py`는 고정 Git 소스의 AST 목록과 JSON 바이트를 대조한다. Python3.12.14/stdlib·Git 읽기만 수행하며 수치 라이브러리를 import하지 않는다.

다음 실제 연결 때 생산자 원 DOF 노출·소비자 수집·소유권/비용·오류 처분을 한 고정 후보로 다루고, 변경 범위 시험과 독립 확인 뒤 운영 핀 영향을 판단한다. 실행 환경·운영자·UTC·자원·S0/Q11 수령·⑥ 시도3/4 GO는 별도이며 이번에 확정하지 않았다. 저장소 검사와 보존은 `check_results.json`, `scope_check.json`에 남긴다. 전달문·인계 ZIP은 생성하지 않는다.
