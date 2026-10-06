# GATE93 단계 4 제한 구현 검토

판정은 **수정 후 재검토**다. G92-N3의 사본 9키 대조와 provider edge 해시 통일은 수용한다. G92-N2에는 **v6 경로에서 유효한 v3 envelope를 차단하지 않는 잔여 1건**이 있다. 별도로 고정 커밋의 원문 로그 누락 때문에 실행 결과 증거의 최종 수용은 보류한다. 묶음 6 전체 종결이나 실행 GO가 아니다.

## 고정 대상과 확인 범위

- 요청문 커밋: `0e3c244ea79db1b17f09a8f8043d808ab51ff43c`. 첨부에 요청 SHA가 없어서 해당 파일의 Git 이력에서 확정했고, 고정 커밋의 요청문 blob `6496a3abf1e6c436fcba83f2547aece0e616a49c`를 다시 읽었다.
- 판정 코드: `d7a97aa57ea926916d56c985ee4bc2bed96fa81a`.
- 제출 검증 커밋: `3ec8aadb13e4ee4eb9e3434fbd28e503a7c03a34`.
- 제출 source_digest: `c7f48918ff971e91`. 요청문·영수증이 같은 값을 가리킨다. 수신자는 저장소의 source_digest 함수를 실행하지 않았다.
- RUN_SCOPE 60개 파일을 비절단 Git tree의 blob·mode로 대조했다. 이전 코드 `b08bb6944`에서 변경된 것은 `src/io.py`, `src/fitting.py` 둘뿐이다. 코드 → 검증 → 요청 커밋의 RUN_SCOPE 차이는 0이다.
- 고정 표 §16과 증거 매트릭스는 구현 전 `9cc97ec0f`와 검토본의 blob이 같다. 승인 기록 §145·§146의 범위와 두 `-k` 확장 기록을 읽었다.
- 수신 소스는 텍스트로만 검토했다. import·시험·probe·COMSOL·수치 계산·복원·영수증 재생성은 하지 않았다. 파일·텍스트·해시 대조와 회신 포장만 수행했다.

## G93-N1 P2 유효한 v3 envelope가 v6 재유도로 넘어간다

**위치:** [src/io.py 2021](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d7a97aa57ea926916d56c985ee4bc2bed96fa81a/degradation-degeneracy/src/io.py#L2021), 관련 [1895](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d7a97aa57ea926916d56c985ee4bc2bed96fa81a/degradation-degeneracy/src/io.py#L1895)와 [1686](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/d7a97aa57ea926916d56c985ee4bc2bed96fa81a/degradation-degeneracy/src/io.py#L1686).

`ebad = check_planned_envelope(env)`는 공통 v3/v4 reader의 결과다. 이 reader는 유효한 `planned-leg/v3`에 빈 오류 목록을 돌려준다. 반면 현재 v6 validator는 `stage3_planned_envelope`에서 v4가 아니라고 판정하면서도, 아래 재유도 차단에서는 **`if ebad`만** 사용한다.

코드로 추적한 반례는 다음과 같다. 실행 재현을 했다는 뜻은 아니다.

1. 정상 sig 6 산출 사본에서 `s3.planned_envelope`만 **역사적 v3 계약으로 유효한 객체**로 바꾼다. leg·source·설계 SHA는 대조군에서 가져오고, protocol_generation은 문법상 허용되는 `v6`를 쓸 수 있다. 나머지 v3 필드는 정렬된 objectives·양의 budget·기존 mode·retention 하한으로 채운다.
2. `s3.planned_id`와 run signature 등 필요한 봉인은 그 내용에 맞춘다. candidate map·fits·설계 본체는 정상 대조군 그대로 둔다.
3. 공통 `check_planned_envelope`는 v3 reader로 분기하여 `[]`를 반환한다. v6의 `stage3_planned_envelope`와 `stage3_축_유도`는 실패하지만, 그 실패가 재유도 차단 조건에는 반영되지 않는다. `check_execution_record`도 v4가 아니라는 실패를 반환할 뿐 여기서 실행 흐름을 끝내지 않는다.
4. 정상 map/fits이면 `_stage3_rederive`가 호출된다. 유효한 설계와 같은 pairing SHA를 사용한 위 반례에서는 `io.py:1686`의 `env["parameter_order_sha256"]`에 도달한다. v3의 닫힌 9키에는 이 키가 없으므로 **구조화된 실패 반환 대신 KeyError로 빠지는 경로**가 남아 있다. 상위 `validate_provenance`의 호출도 이를 감싸지 않는다.

근거는 `preserve.py:3042–3045,3126–3163,3275–3284,3306–3308`, `design_wire.py:570–596`, `io.py:1895–1934,2021–2033,1674–1686`이다. `STATIC_COUNTEREXAMPLE_SOURCE.json`에 해당 원문을 모았다.

현재 k04_env는 **v4 내부 generator가 philox인 경우**만 다루므로 이 경로를 막았다는 증거가 아니다. G92-N2/§16-3의 “v6 경로에 부적합한 envelope를 재유도에 넘기지 않고 이유 있는 실패로 반환” 조건은 아직 닫히지 않았다. 정상 결과의 수치 오류나 위조 PASS를 확인했다는 뜻은 아니며, 실패 처리 계약의 결함이다.

### 최소 수정 및 종결 조건

- `_stage3_checks`에서 **지원 schema가 v4인지와 그 구조 유효성**을 함께 재유도 선행 조건으로 사용한다. v3 역사적 reader 자체를 바꾸지 않는다.
- 단순히 `stage3_planned_envelope`의 전체 성공 여부로 모든 경로를 막지는 않는다. 유효한 v4에서 planned_id만 불일치한 k06의 기존 독립 검사 의미를 유지해야 한다.
- 정상 v4 대조·역사적 v3 reader 대조·sig6 아래 유효 v3 음성·기존 philox 음성을 구분한다. sig6/v3 음성은 실제 `validate_provenance`가 예외 없이 이유 있는 실패를 반환하고 재유도 호출이 0임을 단언한다.
- 이를 막는 schema 조건을 제거한 변이에 해당 새 node가 지정 이유로 실패하는지 확인한다. 임의 예외 발생을 정상 거부 성공으로 세지 않는다.

이번 회신은 수정·시험의 실행 승인을 새로 부여하지 않는다. 사용자 승인 범위를 확인한 뒤 좁은 변경과 결과를 제출한다.

## G93-N2 P2 고정 증거 디렉터리에 원문 로그가 없다

**위치:** `docs/22p_gap/gate93_evidence/README.md:5–16`.

증거 커밋 `2ab61069b26c9d55a78b1bd829d14edc873334b3`과 요청 커밋 모두에서, recursive tree는 `truncated=false`이고 이 디렉터리의 blob은 **README 하나**다. README가 지칭한 00·03·04a·04b·05a·05b·06·08·10·11·12와 aborted 로그는 들어 있지 않다. 결과 수치가 거짓이라는 판정이 아니라, 현재 인계본으로 원문을 확인할 수 없다는 뜻이다.

따라서 2320 passed / 1 xfailed, smoke rc0, 421/421, 각 단계 시작·종료 HEAD 및 dirty 0, RED의 5개 예외 분리, 첫 실패 보존은 현재 **제출자 보고**로 분류한다. mutation EXPECT가 소스에 들어 있는 사실은 확인했지만 실제 실행 원문을 대신하지 않는다.

남아 있는 **당시 파일**을 보충 커밋 또는 ZIP으로 전달하고 파일별 크기·전체 SHA·실행 상태를 적으면 된다. 원문이 없는 항목은 없다고 표시하고, 대화 전사라면 후속 전사임을 구분한다. 이 누락을 채우기 위해 시험이나 과거 영수증을 다시 생성하지 않는다. 자료 추가 후 G93-N2만 별도로 재확인할 수 있다.

## 수용하는 부분

| 항목 | 판정 |
|---|---|
| G92-N1 고정 매트릭스 | consumer·키·기대값 출처·정확 node·이유·변이·이월을 분리했다. 좁힌 범위의 제출 형식은 충족한다. 실행 효과는 원문 보충 대기다. |
| s3 닫힌 16키와 직접 값 자료형 | sig6 안에서 누락·추가·자료형을 검사하고 s3 오류 시 조기 반환한다. 역사적 sig5 분기는 바꾸지 않았다. |
| candidate map | 최상위 2키·항목 7키·문자열 5개·정수 i·source별 bank_index를 검사한다. bool은 정수로 받지 않으며 오류 map은 재유도에 넘기지 않는다. |
| G92-N3 사본 9키 | helper 투영 6 + env 직접 3만 비교한다. 기존 planned_id·설계·bounds·closure의 독립 재계산을 대체하거나 중복 비교하지 않았다. |
| provider edge SHA | writer와 승인 축이 같은 canonical `digest(env["provider_edges"])`를 사용한다. warm 양성 대조와 k07이 이 차이를 겨냥한다. |
| 새 시험 구성 | 정적 파라미터 집계 138개. k03/04는 검사 이름·이유와 재유도 호출 0, k05/06/12는 실패 검사 집합을 단언한다. 이는 수신자가 138개를 실행했다는 뜻이 아니다. |
| 변이 및 확장 | 새 9개와 두 기존 `-k` 확장의 소스·EXPECT·승인 기록을 확인했다. 같은 비교 위치의 키별 사례와 변이를 구분했고 39개 위치 변이는 이월했다. |

## 영수증과 기존 결과 보존

두 leg의 **재생성 직전 현행본**과 history 파일은 Git blob이 정확히 같다. 더 오래된 G91 코드 커밋의 영수증은 그 뒤 재생성되기 전 세대이므로, history 보존 대조의 기준으로 혼동하지 않았다.

현행 core와 history core의 텍스트를 비교하면 두 validator identity 필드 외에는 같다. 검사 집합 35/34, bundle·restore·outputs·semantic digest는 유지됐다. 원래 artifacts의 26/29개 blob과 mode도 이전 코드 대비 같다.

| leg | 새 core SHA256 | 검사 수 |
|---|---|---:|
| paired_fixed5_v4 | d527cde9fc7251a285d5e753048235f1c3aff54661c7588733cc0ffcd63ad9f7 | 35 |
| grid_fit_v5 | 8de4e4aff4d4550bc4e093949407cf748c540fc42b256d88bff44673cd45292d | 34 |

원장의 core 및 validator source_digest 앵커 네 값은 현행본과 맞는다. 새 `src_io_sha256=cde0be140cabc8dc`는 수신한 io.py 전체 바이트의 SHA256 접두와 맞는다. 단, 수신자는 core 생성 함수나 복원·재채점은 실행하지 않았다.

stamp에는 환경 C **MISMATCH 34**가 실제로 적혀 있다. 판 13·RECORD 16·lock 밖 4·shadowed 1이고, lock SHA는 유지됐다. paired dirty=false, grid dirty=true도 보존됐다. 이는 G91 정본 환경 MATCH나 모든 영수증이 clean tree에서 나왔다는 증거가 아니다. 기록 전용 C 정책 안의 관측으로 한정하며, 환경을 같다고 만들기 위한 설치·lock 재생성을 요구하지 않는다.

앵커 누락과 계약 줄 인용 정정은 현재 파일에서 정리된 것을 확인했다. 첫 실패의 실행 경위와 보존은 원문 보충 뒤 확인한다. 두 줄 인용 수정이 §13.1 밖이었다는 신고도 유지한다.

## 다음 제출과 남는 경계

다음은 **G93-N1의 좁은 차단 수정·해당 회귀와 G93-N2 당시 원문 보충**이다. 다른 소비자 전면 재작성이나 이미 수용한 수치 결과의 재계산을 요구하지 않는다. RUN_SCOPE 변경에 따른 identity·영수증·기존 검증 절차는 승인된 범위와 횟수를 명시해 별도로 준수한다.

기존 위치 변이 39, C8 재개, C7 envelope↔원장, run_spec 최상위·solution map header·원장 항목의 세 제외 범위는 그대로 남는다. 이 제출의 일부를 수용해도 묶음 6 전체 종결·새 연구 leg·p_ini·class·투영 게시·실행 GO로 확대하지 않는다.
