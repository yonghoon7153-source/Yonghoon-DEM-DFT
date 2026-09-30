# 85차 게이트 수신 검토 — 2a 종결 보류
2026-10-01 · 고정 커밋 읽기 전용 코드·증거 검토

**판정: PARTIAL_ACCEPTANCE / ROUND2A_NOT_CLOSED. P1 잔여 1건(G85-N1).** G84-N3·N4와 R2-e·R2-f는 이번 검토 범위에서 수용한다. G84-N1의 전체 SHA 표현과 시작 전 결속은 수용하지만, 사후 validator의 closure 구성원 검증은 미완이다. 2b·실행 GO·새 연구 leg·p_ini 구현은 승인하지 않는다.

## 1. 식별과 검토 수준

- 요청/발송 HEAD: `b49c24fabe94be7a5986bdc54de2d4278c4ebf65`.
- 코드 대상: `f89b1401fb1ab21371bd7755289e64281681b5be`.
- 58개 RUN_SCOPE의 Git blob 및 4개 디렉터리 tree를 대조하고 source_digest를 독립 재계산했다: **`ba51cd20caa10b7b`**.
- 직전 수용 코드 대비 실제 생산 변경은 `src/fitting.py`, `src/io.py`, `tools/preserve.py` 3개다. GREEN 변경 통계 167 추가/40 삭제, GREEN→대상→발송 HEAD의 RUN_SCOPE 추가 변경 없음. design_wire·run.sh·scripts·configs·requirements는 불변이다.
- 수신 소스는 텍스트/AST로만 읽었다. 받은 모듈 import, pytest, 변이 재생, fitting/분석 실행, 복원·영수증 재생성·COMSOL/JVM 실행은 **0회**다. 검토자 자체 바이트/AST/산술 확인 165건은 제품 기능 시험 165건이 아니다.
- 발신 보고의 2039 passed·1 xfailed, smoke rc0, 변이 kill 수와 실행 시간은 독립 재실행 실측으로 바꾸지 않는다. 직전 Gate84 패키지의 manifest/decision은 로컬 원본과 일치한다.

근거: SOURCE_IDENTITIES.json, STATIC_AUDIT.json, PRODUCTION.diff, MUTATION_REGISTRATION_STATIC.json. 아래 줄번호는 위 고정 HEAD의 reference 사본 기준이다.

## 2. 차단 항목 G85-N1 — closure의 파일 목록을 독립 재구성하지 않는다 (P1)

### 확인한 코드

`src/fitting.py:901–929`의 생산 시작 경로는 실제 `config_dependencies`를 사용해 부모→leaf 연쇄의 파일 SHA를 모은다. 전체 SHA의 preimage는 정렬된 `logical_path=file_sha256` 줄이며, v5 값은 같은 전체 SHA의 앞 16자다. 이 부분과 `_stage3_preflight`의 실제 staged closure 대조는 맞다.

하지만 `src/io.py:1955–1974`의 사후 `base_config_결속`은 다음만 한다.

1. 검사 대상 `run_spec.stage3.base_config_closure_keys`를 구성원 목록으로 받는다.
2. 해당 키의 `sealed_inputs`에서 스냅샷을 찾아 실제 바이트를 다시 해시한다.
3. 그 **선택된 목록**의 digest를 run_spec과 계획의 두 digest에 대조한다.

이 블록은 `run_spec.base_config`를 출발점으로 삼지 않고, 봉인 config의 `extends` 연쇄를 읽거나 목록의 정확 집합·중복 여부를 대조하지 않는다. 일반 입력봉인/스냅샷 검사(`src/io.py:2118–2152`)는 전체 봉인 파일의 보존을 확인할 뿐, 선택된 closure 목록의 완전성을 확인하지 않는다.

따라서 §6-f의 “키를 위조하면 재계산 값이 달라져 실패”는 **계획과 run_spec의 digest를 고정해 둔 변이**에만 맞는다. 같은 문서가 요구하는 자기일관 위조 경계에서는 충분하지 않다.

### 최소 반례와 관측 경계

정상 입력이 `leaf.yaml → base.yaml`이고 두 파일의 스냅샷·입력 봉인은 전혀 바뀌지 않았다고 하자.

- `base_config_closure_keys`에서 parent만 뺀다.
- leaf 한 파일로 계산한 digest를 계획과 run_spec 양쪽에 적는다.
- 관련 내용주소/서명은 기존 자기일관 변조 회귀와 마찬가지로 다시 맞추는 상황을 고려한다.

현재 closure 블록의 두 비교는 같은 leaf-only 값을 보므로 성립한다. 그러나 실제 dependency closure의 값과는 다르다. parent-only/불필요 구성원 추가도 같은 문제이며, 중복 키는 dict로 합쳐진다. 해시 충돌이나 스냅샷 바이트 변경이 필요하지 않다.

**이 검토에서 직접 실행한 것은 검토자 소유의 SHA/집합 산술 모형뿐이다.** CLOSURE_COUNTERMODEL.json은 정상·부모 누락·leaf 누락·불필요 구성원·중복의 5개 모형을 보존한다. 실제 `validate_provenance` 전체를 호출하거나 위조 parquet/run artifact를 생성·통과시킨 실측이라고 주장하지 않는다. 차단 근거는 공개된 검사 본문의 구성원 재구성 부재와 그 국소 판정식의 반례다.

현재 n1_04(`tests/test_gate84_round2a.py:142` 이하)는 키 목록을 그대로 둔 채 digest를 임의의 `f*64`로 바꾼다. 그래서 이 빈틈을 겨냥하지 않는다. 그 시험의 마지막 manifest 변경 뒤 전체 run signature 불일치까지 제거한 end-to-end 반례인지도 별도로 구분해야 한다.

### 필요한 최소 보완

새 해시 형식이나 2b 기능은 필요 없다. **2a의 사후 closure 결속만** 보완한다.

- 봉인된 논리 root config와 그 바이트의 dependency 관계에서 정확 구성원 집합을 재구성하거나, 동등하게 독립된 고정 구성원 근거에 대조한다. 검사 대상 key 목록을 그 자체의 정답으로 쓰지 않는다.
- root의 기존 spec/입력 식별, parent 연쇄, 정확·유일한 정규화 경로 집합, 구성원별 봉인 바이트가 일치해야 한다. 누락·추가·중복·모호한 경로/순환은 실패로 남긴다. 현재 디스크의 다른 config로 조용히 대체해 증거를 채우지 않는다.
- 같은 snapshot을 유지하면서 key 목록과 두 digest를 함께 바꾼 음성을 검사한다. 정상 parent+leaf·재배치 양성과 대조하고, 필요한 계획/record/signature/output 봉인은 일관되게 맞춰 **기존 다른 검사 때문이 아니라 구성원 결속 때문에** 거부되는지 확인한다.
- v5 preimage/값, 이미 수용한 preflight·N4·2b 경계는 유지한다.

보완 구현·시험은 별도 사용자 승인 대상이다. 이 리뷰로 실행하지 않았다.

## 3. 항목별 답

| 질문/항목 | 판정 | 이유 |
|---|---|---|
| G84-N1 전체 hex64·v5 prefix·시작 전 null/불일치 거부 | 부분 수용 | 같은 preimage/실제 dependency 시작 대조 확인. 사후 구성원 검증은 G85-N1 잔여 |
| G84-N3 공통 선행 검사 | 수용 | preflight 1982 → halfcell 분기 1985 → self-fit 2015 순서. 다른 source/reference 및 v6 거부가 앞에 있고 legacy는 건너뜀 |
| G84-N4 v2 계수·v1 읽기 | 수용 | 저장 J 유한 수와 legacy True 수를 별도로 집계. writer v2, consumer schema 분기, 닫힌 키/범위 검사. 정상 종료 수로 해석하지 않음 |
| R2-e dead 정의 삭제 | 수용 | normalize 정의 하나. 살아 있는 reader AST 및 _minimize_until_stable/_fit_one AST는 직전 코드와 동일 |
| R2-f 계약 v6 열 | 수용 | legacy 설명과 현재 v6 경로를 분리. 이 문서 수용은 실물 v6 leg·pilot 승인 아님 |
| 2a 종결 | **아니오** | P1 G85-N1 한 건 남음 |
| 새 세대 영수증 | 한정 수용 | 기존 두 역사 leg의 기록/식별 갱신으로 수용. 미검증 v6 closure 경로의 무결성 증명으로 확대하지 않음 |
| 2b·실행 GO | 요청 범위 밖/미승인 | R2-a·R2-c·G84-N2 및 p_ini 구현에 착수하지 않음 |

## 4. 자체 신고와 과거 판정의 영향

### G85-C1 — “영향 없음”은 대상별로 나누어 써야 한다 (비차단 기록 정정)

실제 before/after diff에서 54차 fixture 보강, 59차 read-back/게시명 및 link 반례 수정, 61차 두 시험의 customization 층 치환이 확인된다. 이 수정들은 시험 층이며, 뒤의 3개 정정 커밋은 생산 코드를 바꾸지 않았다. 61차의 치환은 해당 두 시험 안에서만 이루어지므로 **그 완전성 reader의 단위 증인 격리**로 수용한다. 전체 customization 경로까지 통합 검증했다고 쓰면 안 된다.

- 기존 수치/보존 산출이나 생산 방어가 실제로 깨졌다는 증거는 이 수정들만으로 나오지 않는다. 76차·라운드1 종결을 소급 취소하지 않는다.
- 반대로 과거 **회귀·변이가 해당 성질을 독립적으로 검사했다는 근거에는 공백이 있었다.** “이전 판정에 어떤 영향도 없다”는 포괄 문구는 수용하지 않는다.
- 정확한 표현은 “생산·수치 오류는 확인되지 않았으나 일부 기간의 시험 증인에 공백이 있었고, 현재 수정과 보고된 재생으로 해당 증인을 보강했다”이다. e·e2·e3·e5의 해당 기간/노드를 원장에 한정 기록하면 된다.
- 최종 변이 근거는 **28d0effe 전체 344/345 + 예외 g61을 f89b1401에서 정정 후 단독 확인**이다. “최종 f89에서 등록부 전체 345/345를 다시 실행”으로 합쳐 쓰지 않는다. 동일 생산 코드와 제한된 시험 diff에 기반한 합성 증거로 평가할 수 있으며, 표기만을 위해 전체 재실행을 요구하지 않는다.
- 신규 g84 변이 12개는 현재 텍스트에 preimage가 각각 한 번 있음을 AST/문자열로 확인했다. 이는 kill 재생 12/12의 독립 재현이 아니다.

### §6-a RED 탐침

시험 파일 밖 탐침도 사전 코드 식별·스크립트·raw 반환·실제 실패 이유가 연결되면 증거가 될 수 있다. 위치가 scratchpad라는 이유만으로 배제하지 않는다. 다만 이번 고정 커밋의 `scratchpad/g84_probe_real_reasons.txt`는 조회되지 않았다. 추가로 요청한 raw 탐침/재생 원문을 받기 전에는 **제출자 보고**로 남긴다. 새 함수를 찾지 못한 11개 AttributeError를 결함 RED로 세지 않는 분리는 수용한다. 새로 시험을 반복하라는 요구가 아니다.

### G85-C2 — n4_02 설명의 범위 (비차단)

n4_02의 `J=NaN, converged=True`는 계수 재대조용 합성 행이다. 실제 legacy의 “유한 성공 다음 nonfinite round”는 이전 best의 **유한 J**를 반환하면서 ok=True·outer=nonfinite가 공존할 수 있다. 따라서 그 합성 행을 해당 실제 경로의 반환 모습이라고 부르지 말아야 한다.

그 시험이 마지막에 확인하는 것도 `실현_재계산` 한 항목이지 전체 validator PASS가 아니다. 설명을 “합성 NaN/legacy-flag 계수 검사”로 좁히고, 실제 legacy 사례의 의미는 기존 80차 회귀와 구분해 인용한다. N4 생산 계수 코드의 오류를 새로 발견했다는 뜻은 아니다.

## 5. 영수증과 보존

두 history 파일은 직전 수용본 바이트와 같다. 현재 core 텍스트는 validator_source_digest·src_io_sha256를 제외하면 직전과 같고, 검사 수 paired 35/grid 34, producer·bundle·outputs·restore 내용도 같다. 현행 core 식별은 원장에 연결돼 있다.

- paired core: `4d6cdc7b285f0538c33baa2d7ae9a131ebd782cfa6351f53e13438e19939fa64`
- grid core: `3f706067d5fbc8663310faadfb05301a35222d91d0de5f1a436e8b87f66b363f`

수신 파일 SHA/Git blob 및 core 텍스트를 대조했으며, YAML core의 재직렬화 hash나 복원/재채점은 이번에 재생성하지 않았다. 원본 stamp는 paired dirty=false, grid dirty=true다. clean 착수 보고와 순차 기록 중 stamp는 별개이며, 두 stamp가 모두 clean이었다고 고쳐 쓰지 않는다. 이것만으로 생산 코드가 dirty였다고 단정하지도 않는다.

선택한 로컬 Gate84 기록 전후 해시는 동일하다. 원격 머신 전체·실행 당시 프로세스·전체 이력을 새로 관측한 것은 아니다.

## 6. 다음 회신 범위

**G85-N1 구성원 결속 보완 결과 + C1/C2 기록 정정**만 요청한다. 기존 N3/N4/R2-e/f를 원점부터 다시 열거나 2b 구현을 섞지 않는다. 보완에 따라 RUN_SCOPE가 바뀌면 기존 보존/영수증 절차의 영향은 새 사용자 승인 범위에 명시한다. 이 검토는 코드 수정·시험 실행 권한을 대신하지 않는다.

전체 gate76·라운드1의 기존 종결, grid_fit_v5 진단 전용, 새 연구 실행 0 상태를 유지한다.
