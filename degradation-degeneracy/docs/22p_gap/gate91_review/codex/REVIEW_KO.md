# GATE91 독립 정적 검토 회신

2026-10-05 · 판정: **ACCEPTED — G90-N1 및 C1 종결, 환경 프로필 C 기록 대조 라운드 종결.** 추가 차단 지적 없음. 실행 GO 아님.

## 1. 판정 대상과 검토 경계

| 구분 | 고정 식별 |
| --- | --- |
| 저장소 | yonghoon7153-source/Yonghoon-DEM-DFT |
| 요청 HEAD | `43056f78d845741b43357181fcfd64fc78a8ef0c` |
| 판정 코드 | `b08bb6944b03511c97c8deeb38e6a347bbb1f1fb` |
| 직전 판정 코드 | `e2160c2ef276d4944fa4ad76fbaa001671a1a95e` |
| source_digest | `f0175fff71132003` |
| 발송 후 로그 보충 | `85c9cbe1162b6e4b01390345ff1dfb768c5a61cb` |

검토자는 고정 커밋의 원문·diff·시험 소스·등록부·영수증·제출 로그를 읽었다. 자체 작성한 도구로 텍스트, AST, 파일 식별과 로그 해시를 대조했다. 제출 소스 import/실행, pytest, smoke, 변이 재생, 영수증 재생성, 복원·재채점, 설치 및 COMSOL/JVM/PyBaMM 실행은 하지 않았다. 아래 시험 수치는 제출자의 보존 로그에서 확인한 값이며 검토자 재실행 값이 아니다.

주요 원문: [요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/43056f78d845741b43357181fcfd64fc78a8ef0c/degradation-degeneracy/docs/22p_gap/GATE91_REQUEST.md), [판정 소스](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/b08bb6944b03511c97c8deeb38e6a347bbb1f1fb/degradation-degeneracy/tools/env_profile.py), [증거 목록](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/85c9cbe1162b6e4b01390345ff1dfb768c5a61cb/degradation-degeneracy/docs/22p_gap/gate91_evidence/README.md).

## 2. 요청 네 항목에 대한 답

| 요청 | 판정 | 근거와 수용 한계 |
| --- | --- | --- |
| G90-N1 최소 종결 조건 | 종결 수용 | 경로 검색 결과의 RECORD 소속으로 이름·설명·요약·stamp가 좁혀졌고, 실제 로드 origin은 세 상태 모두 미측정으로 선언된다. |
| C1 적용 경계 | 종결 수용 | C의 일치 여부는 실행 gate가 아니다. 다만 측정 기능을 요구하는 e06/e08은 지원 환경에서 측정 불가를 시험 실패로 삼는다. |
| 판정 로직·lock·기존 연결 불변 | 수용 | 변경은 이름·문구·범위 선언이다. lock, requirements, smoke, make_receipt, run.sh 및 수치 경로의 바이트 불변을 확인했다. |
| 회귀·변이·영수증·전체 검증 | 제출 근거 수용 | 원문 로그 14개 크기/SHA 일치, 실패 이력 보존, 최종 검증과 새 영수증 연결을 확인했다. 검토자가 해당 실행을 재현한 것은 아니다. |

### G90-N1: 실제로 무엇을 확인했는지가 결과에 남는다

`tools/env_profile.py`의 `_origin`은 여전히 `PathFinder.find_spec(module, paths)`가 반환한 파일의 RECORD 소속을 검사한다. 이미 로드된 `sys.modules` 객체, 그 `__file__`/`__spec__.origin`, 다른 meta-path finder의 선택을 측정하는 코드가 아니다. 이번에는 그 기능을 넓히지 않고 다음과 같이 주장을 바로잡았다.

- `counts.path_origins_in_record`, `unverifiable.path_origins`, 불일치 축 `path_origin`으로 변경했다. 내부 측정 결과도 `path_origins.in_record`로 일치시켰다.
- `NOT_MEASURED = ("loaded_module_origin",)`와 결과의 `not_measured`가 MATCH/MISMATCH/UNMEASURED 모두에 남는다. `compare_lock`이 lock을 읽기 전에 결과를 초기화한다.
- 모듈·함수 설명과 CLI 요약은 경로 검색의 범위를 밝히며, 새 영수증 stamp도 같은 이름과 미측정 선언을 사용한다.
- 고정 표 §13-4, 원장 §138, 요청문 §1·§4·§5·§6-d가 과거 표현에 대한 유효 정정을 명시한다. 과거 기록 자체를 고쳐 쓴 것은 아니다.

`not_measured`는 측정값이 아니라 도구 범위 선언이다. 따라서 UNMEASURED에서도 이 목록을 남기는 것은 측정하지 않은 값을 만든 행위가 아니다. 이 구분 아래 원장 §137의 최소 종결 조건을 충족한다.

새 s02는 실제 numpy가 로드된 상태와 합성 경로의 numpy 검색 결과가 달라도 MATCH일 수 있음을 고정한다. 이는 loaded-origin 일치를 증명하는 양성 시험이 아니라, **그 일치를 주장하지 않아야 한다는 범위 회귀**다. 이제 결과에 그 한계가 남으므로 해당 반례의 의미와 구현이 맞는다.

관련 소스: `env_profile.py` 6–17, 49–52, 115–139, 306–307, 319–357, 362–381행.

### C1: 기록 도구와 그 도구의 기능 시험은 다른 조건이다

모듈 설명 6–7행, 고정 표 §13-4, 요청문 §6-e의 정정을 수용한다. C의 MATCH/MISMATCH 자체가 연구 실행을 차단하는 정책은 아니며, smoke/run.sh/영수증의 기록 단계는 UNMEASURED도 기록한다. 반면 e06/e08은 측정 기능 자체를 시험하므로 해당 지원 환경에서 UNMEASURED를 실패로 판단할 수 있다. 이를 모든 환경에서 pytest가 무조건 통과한다는 주장으로 읽지 않는다.

## 3. 변경 범위와 식별의 독립 대조

코드 변경 전 고정 표 커밋 `69b35f65dda21378287c94ec1fabaf98a2ca94d8`의 표와 요청 HEAD의 표는 Git blob `48b4aa86c4739b39f39ea326a10c7bd66b67ba3f`로 같다. 시험 이름 따라가기와 변이 원문 갱신은 이 표에 미리 포함되어 있다.

Git 코드 커밋은 `tools/env_profile.py` 한 파일 +30/−17이다. 직전 코드→이번 코드의 RUN_SCOPE 차이는 이 파일뿐이며, 이번 코드→요청 HEAD 및 요청 HEAD→보충 커밋의 RUN_SCOPE 차이는 없다. 60개 RUN_SCOPE 파일 바이트에서 source_digest를 독립 재계산한 결과 `f0175fff71132003`이다. 기존 저장 사본을 재사용한 파일은 현재 커밋의 Git blob 일치를 먼저 확인했다.

이름 변경·docstring 제거·추가 범위 선언의 명시적 정규화를 적용한 AST 대조에서 11개 함수의 구조가 같았다. CLI 요약 변경은 diff로 별도 읽었다. 이 대조는 전체 프로그램 동치의 형식 증명은 아니지만, 이번 한정 정정에서 판정 조건·rc·lock 문법·실행 연결을 바꾸지 않았다는 근거가 된다.

Git blob 불변 확인: `requirements-validation-C.lock.txt`, `requirements.txt`, `scripts/smoke_e2e.sh`, `docs/22p_gap/make_receipt.py`, `docs/22p_gap/env_profile_B_v4.yaml`, `src/io.py`, `src/fitting.py`, `run.sh`, `tests/conftest.py`.

## 4. 시험·변이·자체 신고의 해석

보존 로그 14개 모두 README의 크기/SHA와 맞는다. 보충 커밋의 발송 HEAD docs-lint도 확인했으므로 이 항목은 제출자 요약만 남은 상태가 아니다.

| 제출 기록 | 확인 내용 |
| --- | --- |
| RED | 38 failed / 5 passed. 기존 결과의 닫힌 키 변경과 새 범위 시험이 주된 이유이며, 38개의 새로운 수치 결함으로 세지 않는다. |
| GREEN | G90/G91 관련 43 passed. 기존 G90 node 집합 불변, 기대 필드·문구 갱신을 확인했다. |
| 관련 모듈 초기 실패 | 577 passed / 10 failed의 오래된 영수증 validator 식별 오류를 보존했다. 영수증 갱신 후 관련 모듈 113 passed. |
| g9 변이 | 새 둘의 EXPECT 등록 전 emit-expect 반환과 뒤의 15/15 rc0을 구분한다. 기존 g90 13개 증인/기대 결과 불변. |
| 전체 pytest | clean `f27006370`: 2182 passed / 1 xfailed / rc0, 3447.10초. |
| strict smoke | 같은 고정 코드에서 rc0. 제출자 실행에 작은 grid/fit/score/restore가 포함되며 이번 검토에서 실행하지 않았다. |
| 등록부 전체 재생 | 412 검출 / 생존0 / 실행오류0 / 별도 선언11, rc0. scenario423과 실제 실행412를 혼동하지 않는다. |
| 발송 HEAD docs-lint | 358 passed / rc0, 시작·끝 `43056f78d`, dirty0. 원문 보존은 후속 `85c9cbe1`이다. |

기존 xfail은 저장소 밖 입력 staging을 지원하지 않는 선언 항목으로 유지된다. 2182 pass를 모든 기능의 무제한 지원으로 확대하지 않는다.

요청문 §6 a–h는 이번 종결을 막지 않는다. a의 기존 시험 변경은 사전 고정된 이름 따라가기이고, b의 s02는 범위 반례이며, c의 선언/측정 구분과 d의 덧붙인 정정은 타당하다. e는 C1을 닫는다. f/g의 lock 불변과 내부 이름 정합성, h의 코드 식별도 대조했다. 고정 커밋 간 비교는 전 중간 커밋의 실행 이력을 전수 감사한 것은 아니다.

## 5. 영수증 수용

두 leg의 history는 직전 현행 영수증과 바이트 동일하다. 현재 core 내용에서 바뀐 항목은 validator_source_digest이며 core_sha256과 원장 앵커도 새 값으로 대응한다. 생산자·묶음·산출·복원·검사 결과 부분은 유지된다.

| leg | 검사 수 | 현재 core SHA |
| --- | ---: | --- |
| paired_fixed5_v4 | 35 | `1e3ea7c806f8d53524d16e24c846755e0aa22dc3840f81fd0e5c114b3b1ac411` |
| grid_fit_v5 | 34 | `23c78ed0c9cd7b89c495ef2ef3216829f812ac145957a64a50c768f679390d66` |

stamp의 `environment_profile_C`는 새 이름과 `not_measured`를 담는다. lock SHA는 `d886f30ff675fef723fb9bcedd98297910fb1f8f1809370c18d8980dc5e63b39`로 유지된다. 제출 환경의 MATCH는 170개 배포판, 경로 검색 origin의 RECORD 소속9, 해당 origin 확인 불가 yaml, loaded_module_origin 미측정이라는 범위에서 수용한다.

paired의 validator_tree_dirty=false / grid의 true를 그대로 보존했다. 순차 영수증 작성의 기존 한계를 숨기거나 둘 다 clean으로 해석하지 않는다. 이번 검토는 YAML 재직렬화 core 해시 재생성이나 복원/재채점을 수행하지 않았으며, 기록된 core 식별·원장 앵커·불변 영역·제출된 재생성 검증 로그를 대조했다.

## 6. 검토자 작업의 한계 및 후속

검토자 자체 점검 도중 로컬 참조 목록에 없던 `tests/conftest.py`와 이전 mutation registry를 요구해 두 번 KeyError가 났다. 전자는 고정 트리 blob 대조로, 후자는 직전 고정 커밋의 원문을 읽어 보완했다. 이는 제출 코드·시험 실패가 아니다. 최초 반환과 최종 정적 대조 rc0을 `REVIEWER_TOOL_RETURNS.json`에 구분했다.

이번 결론은 **환경 프로필 C 기록 대조 라운드의 종결**이다. 실제 loaded-origin 측정, producer 실행 환경과의 동일성 보증, D guard, C fail-closed, lock 재생성/설치, 새 연구 leg, 운영 v6 계획/세대표, p_ini/class/투영 및 COMSOL 실행을 승인하지 않는다. `grid_fit_v5` 진단 전용 지위도 바꾸지 않는다.

다음 최소 행동은 이 회신을 원장에 접수하고 해당 라운드를 닫는 것이다. 같은 결함을 닫기 위한 반복 전체 시험은 요구하지 않는다. 다음 작업이 필요하면 목적·범위와 사용자 승인을 별도로 정한다. 검토자는 원장이나 저장소를 변경하지 않았다.

증거 묶음의 `STATIC_AUDIT.json`, `SOURCE_DIFF.txt`, `TEST90_DIFF.txt`, `MUTATION_DIFF.txt`, 두 영수증 diff 및 `REFERENCE_TEXT.json`에 이번 대조 근거를 보존했다.
