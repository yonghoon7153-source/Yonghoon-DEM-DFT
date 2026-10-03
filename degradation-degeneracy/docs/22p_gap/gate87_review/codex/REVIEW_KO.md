# Gate87 독립 검토 — 2b 종결 보류, P1 한 건

2026-10-03. **판정: REQUEST_CHANGES — ROUND2B_NOT_CLOSED.** G87-N1(P1) 한 건. 2a와 이전 종결은 유지한다. 실행 GO를 심사하거나 부여한 문서가 아니다.

## 1. 결론

v5 spec 불변, v3 계획/문맥 분리, envelope 결속, CLI 배선, 기존 preflight/prepare 유지, v6 이름 체계는 확인했다. 그러나 **새 v6 fit-only 진입 경로와 기존 grid→fit 완료 계약이 연결되지 않았다.** 따라서 R2-a 전체와 라운드 2b는 아직 닫을 수 없다.

이것은 새 연구 실행에서 관측한 실패가 아니라, 고정 코드의 호출 순서·분기·초기 상태를 대조한 정적 결함이다. 받은 프로그램, 프로젝트 시험, 변이, COMSOL, 복원, 연구 계산은 실행하지 않았다.

## 2. 고정 식별과 직접 확인

| 구분 | 확인값 |
|---|---|
| 요청 HEAD | `672ab83b209c925c3d83ab0fca9b39b90d87f1fd` |
| 생산 코드 | `b8d4b69338f00083ece7e554660888b41d1b4905` |
| 사전 고정 표 | `0b21490d31b74a90317a1d7000d33d68e29178a0`의 §13 |
| 독립 재계산 source_digest | `864edfb73b9695a1` |
| RUN_SCOPE | 58개 파일. Git blob 및 src/tools/configs/scripts tree 결속 확인 |
| 생산 변경 | `run.sh`, `src/fitting.py`, `tools/preserve.py`만. `src/io.py` 불변 |
| 생산 코드→요청 HEAD | RUN_SCOPE diff 0 |
| 검증 로그 커밋→요청 HEAD | `7fbaa45b1f2a217a41272426260f75bdabf62a28` 이후 코드·시험·변이 등록부 변경 없음; 문서/증거 추가 |

GitHub 고정 커밋의 파일을 데이터로 받아 원 Git blob SHA-1과 대조했다. 변경 없는 55개 RUN_SCOPE 파일은 이전 수신 사본을 이번 tree의 blob SHA에 다시 결속했다. 로컬 운영 checkout을 수정하거나 원격 브랜치를 갱신하지 않았다.

## 3. G87-N1 — P1: fit-only 새 claim이 완료 기록에서 grid 선행 조건에 막힘

### 코드에서 연결되는 경로

1. 새 shell 옵션은 `--mode fit`만 허용한다. grid/all v6 경로는 명시적으로 제외된다. [run.sh:222](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/run.sh#L222)
2. 비-smoke v3 계획과 맞는 문맥이면 새 claim을 열 수 있다. claim 초기값은 `phases={}`다. [fitting.py:1284](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/src/fitting.py#L1284), [preserve.py:7382](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/tools/preserve.py#L7382)
3. 외부 입력의 올바른 `fit.in_digest`를 주면 입력 검사는 같은 claim의 grid 영수증 없이 통과할 수 있다. 이 digest는 curves 단독 SHA가 아니라 입력 묶음 digest다. [fitting.py:1184](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/src/fitting.py#L1184)
4. fit 본체가 정상 반환한다고 가정하면, `commit_run_outputs` 다음에 `_record_phase(claim, "fit", …)`를 호출한다. 즉 완료 기록의 거부는 산출 commit보다 뒤다. [fitting.py:1735](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/src/fitting.py#L1735)
5. 그런데 `CLAIM_PHASES=("grid","fit")`이고 `phase_done("fit")`는 선행 grid가 없으면 PreserveError를 낸다. 새 경로에는 그 grid 영수증을 정당하게 만드는 연결이 없다. [preserve.py:3997](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/tools/preserve.py#L3997), [preserve.py:6895](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/tools/preserve.py#L6895)

따라서 정상 입력의 새 비-smoke v6 leg는 **claim 발급 → fit 산출 → fit 완료 영수증 거부**에 도달할 수 있다. 계산을 시작할 수 있다는 사실과 승인된 실행을 정상 완료할 수 있다는 사실이 분리돼 있다. 산출물이 틀렸다는 판정은 아니다.

### 기존 grid를 먼저 돌리면 되는가

그것도 현재 제시된 v6 경로가 아니다. `src.grid._assert_grid_authorized()`는 여전히 v2 `leg_run_spec()`을 만들므로 v3 승인 spec/claim의 digest와 일치하지 않는다. 다른 leg의 grid claim을 자동으로 이전하는 배선도 제출 범위에 없다. `finalize_leg()` 역시 두 phase를 필수로 요구한다. [grid.py:436](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/src/grid.py#L436), [preserve.py:7335](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/tools/preserve.py#L7335), [preserve.py:8938](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/tools/preserve.py#L8938)

수동으로 grid receipt를 채우거나 기존 순서 검사를 삭제하는 것은 해결로 수용하지 않는다. 외부 producer 입력을 소비한 사실과 이 claim에서 grid를 계산한 사실은 구분해야 한다.

### 왜 63개 양성/음성 시험과 374개 변이가 놓치는가

- s02_04의 비-smoke 양성은 `_assert_fit_authorized()`의 **claim 발급까지만** 검사한다.
- s04_01의 실제 fit 완주는 **smoke namespace**다. 이 경우 claim=None이며 `_record_phase`는 즉시 반환해 문제의 선행 phase 검사를 지나지 않는다.
- CLI 양성은 context builder/run_fit을 대체한 배선 시험이고 shell 양성은 dry argv 시험이다.

이 시험들은 각각의 선언 범위에서는 유효하다. 그러나 비-smoke의 발급과 완료를 합친 양성 증거는 아니다. [시험 s02_04·s04_01](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/tests/test_gate87_round2b.py#L339), [기록의 claim=None 면제](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/672ab83b209c925c3d83ab0fca9b39b90d87f1fd/degradation-degeneracy/src/fitting.py#L854)

추가 회귀에서는 기존 s02 fixture의 curves 단독 SHA를 복사하지 말고 실제 `fit_input_package_digest(_fit_input_digests(...))` 계약을 만족시켜야 한다. 그렇지 않으면 앞단 입력 거부가 이 결함을 다시 가린다. 이 주의는 G87-N1의 재현 조건이며 별도 결함으로 중복 집계하지 않는다.

### 종결에 필요한 최소 보완

1. **외부 입력을 쓰는 v6 fit-only의 phase 계약**을 먼저 고정한다. 입력 바이트/producer 근거, claim 소유권, 완료/재개/최종화의 연결이 필요하다. 실제 grid 계산을 한 것처럼 기록하지 않는다.
2. v2 승인·claim·grid→fit 순서 규칙은 유지한다. 변경이 기존 승인 파일 경계를 넘으면 그 범위만 별도 승인받는다.
3. 격리 원장 + 비-smoke 출력 + 올바른 외부 입력으로, 실제 승인 검사→완료 기록→최종화까지 연결한 양성 회귀를 넣는다. 연구 계산을 추가하는 대신 수치 본체만 inert 처리할 수 있지만 **claim/phase/종결 함수는 대체하거나 선행 영수증을 수동 삽입하지 않는다.**
4. 잘못된 외부 입력·부족한 결속·다른 attempt는 거부하고, 기존 v2의 순서 역전도 계속 거부하는 음성 대조를 붙인다. 해당 순서/결속을 제거하는 변이를 확인한다.

이 문서는 수정·시험 실행의 승인이 아니다. 위 한 건의 범위 고정과 사용자 승인 후 진행할 후속 요구다.

## 4. 수용하는 부분

| 항목 | 판정·근거 |
|---|---|
| G84-N2 / v5 spec 불변 | 수용. 공유 helper를 원위치에 대입한 AST가 이전 builder와 동일. 검토자 독립 canonical 계산의 골든 `b8f90ad97a7509f72742f0962c50646787171fb0214ea83478c9e597117073b4` 일치. 기존 계획 바이트·주소 불변 |
| v3 builder/index 결속 | 수용. 9키 축, envelope 유도, leg/source/세대, context 양쪽 필수, provider 키 집합 검사 확인 |
| 진입점/CLI 배선 | 부분 수용. 기존 preflight/prepare 우회는 발견하지 않음. 실행 완료까지의 수용은 G87-N1 때문에 보류 |
| R2-c 이름 | 수용. v6 하나, 새 validator digest를 운영 세대표에 등록하지 않음 |
| 새 영수증 | 한정 수용. 이전 두 원문이 history와 바이트 동일. 변경은 core_sha256/validator_source_digest/validator_commit/generated_at_utc뿐. 검사 수 35/34, producer·bundle·outputs·restore 불변. 실제 재복원·재채점은 이번에 하지 않음 |
| 2a·이전 종결 | 유지. 이번 발견은 새 fit-only 경로의 완료 연결 문제 |
| 2b 전체 종결 | 보류 — P1 한 건 |

## 5. 원문 로그 확인과 한계

README에 적힌 13개 로그의 크기·전체 SHA-256을 모두 대조했다. 7fbaa45b 시작 dirty=0, pytest 2109 passed/1 xfailed/rc0, smoke rc0, 전체 변이 374 hit/0 survived/0 error/11 declared 및 rc0가 원문에 있다. 이는 **보존 로그의 확인**이지 검토자가 그 원격 프로세스를 직접 관측·재실행한 것은 아니다.

첫 전체 변이 254개 뒤 rc124 중단은 성공으로 합산하지 않았다. g87 첫 emit-expect 로그의 실제 생존은 3건이며, EXPECT 미선언 표시를 전부 생존으로 세지 않았다. 이후 자기일관 위조로 고친 22/22와 전체 재생 기록은 수용한다. 시험 통과를 G87-N1 미존재의 증명으로 확대하지 않는다.

검토자 자체 정적/데이터 검사 162건 + 79건은 기능 시험 수가 아니다. 검토자 도구의 라이브러리 부재·필드명 가정·이전 로컬 사본 누락은 정정 경위를 별도 기록했다. 제출자의 생산 코드/시험 실패로 분류하지 않는다. 이전 Gate86 검토 파일 156개는 전후 동일하다.

원문 영수증 core YAML의 canonical hash는 이번에 독립 재생성하지 않았다. 내용 차이·원문 보존·원장 앵커 범위의 수용이다. v6 실물 연구 leg 성공, 운영 보존 profile, 새 계산, class/투영 게시, p_ini, requirements 상한은 이번 수용에 포함되지 않는다.
