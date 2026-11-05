# 보정 전 믹싱 첫8 준비와 관측 연결 독립 검토

검토 대상: `189930cc68b6e58beb6b4546d80353dc03852195`, `codex/mixer-1104`.

**판정: 첫8 정적 준비는 범위 수용. 관측 연결 전체 수용은 PRE8-01·02 수정 전 HOLD. 새 P1 없음, P2 두 건, P3 없음.** 이전 초안·PRECAL-NOTE01의 문서 수용을 변경하는 판정이 아니다. 두 발견은 계산식 자체가 아니라 관측 입력 집합과 코드 출처 결속에 관한 것이다.

전체 게이트 HOLD, 실제 연구 실행·등록·실험·배포·통합·원장 종결 미승인은 유지한다. 요청 범위에서 소스·정본·원장을 수정하지 않았다. ibb/WSL/LIGGGHTS 및 전체 게이트를 실행하지 않았다. 후속 시점은 D0.7 종료 후·1저자 승인 후이며, Rint② 우선 순서를 변경하지 않는다.

## 1. 고정 바이트와 재현 범위

| 항목 | 독립 대조 결과 |
| --- | --- |
| 첨부 ZIP | 474,146 B; SHA256 `51abe64c003c5767dcf791aee4cd582a4855793ffdb7b96d98ad078b8f740d92` |
| PIN·SNAPSHOT_MANIFEST | 위 핀 일치. 54개 파일의 길이·SHA256·Git blob SHA1 전부 일치 |
| 원격 핀 | 고정 핀의 GitHub contents 메타데이터와 54개 blob·길이 전부 일치 |
| 포장 | PACKAGE_SHA256SUMS 71개 일치. CRC·경로 이탈·중복 이름·심볼릭 링크 항목 검사 통과 |
| 요청서 | REQUEST.md와 동봉 정본 요청서 바이트 동일 |
| 이전 NOTE01 묶음과 공통 파일 | 등록 초안·SOP·조건표·비용 근거·기존 생성기/M/접촉 판독기 등 공통 13개 모두 바이트 동일. 공통에 없는 파일까지 보존을 입증한 것으로 확대하지 않음 |

이번 실행 환경은 Windows, Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3이다. 작성 측 Python 3.8.20/3.11.17 기록은 동봉 증거로 읽었으며, 이 검토에서 그 환경의 실행을 다시 했다고 세지 않는다.

| 독립 실행 | 결과와 한계 |
| --- | --- |
| 제출 준비 시험 | 14개 unittest 메서드 PASS |
| 제출 관측 시험 | 20개 unittest 메서드 PASS; 기존 prepare binding mock 및 회전 wiring의 cell_stats mock 유지 |
| 준비 추가 탐침 | 208개 검사 PASS. 8개 메모리 덱·56개 다른 case 교환·72개 해시를 다시 맞춘 덱 변형·24개 메타 변형·예외/이름 충돌 복구 등. 메서드 수 또는 연구 조건 수와 합산하지 않음 |
| 관측 의미 추가 탐침 | 5개 묶음 PASS, 최대 80개 합성 입자. 실제 contact 및 cell_stats 사용. 디스크 경로에서는 prepare binding만 mock |
| 완료 로그 추가 탐침 | 실제 준비 덱에서 읽은 E0/U run 계획에 대해 합성 정상 로그 2종 및 변형 로그 24종. 모두 기대 상태 |
| 입력·소스 결속 탐침 | PRE8-01·02 재현. 파일 목록 추가·초기 해시 후 소스 변경은 TECH라는 대조도 함께 보존 |

첫 로컬 시험 시도는 검토 래퍼의 `-I` 경로 설정과 Windows 기본 임시 디렉터리 권한 때문에 실패했다. 두 번째 래퍼에서는 unittest에 전달할 argv를 정리하지 않아 실패했다. 세 번째에는 소스 변경 없이 scripts 경로·쓰기 가능한 합성 임시 폴더·argv만 지정하여 14/20 통과했다. 두 실패 원문은 `environment_attempt1/`, `environment_attempt2/`에 보존했다. 대상 코드 결함이나 Linux 시험 실패로 세지 않는다. 기존 ResourceWarning도 삭제하지 않았다.

## 2. REQUEST 여섯 질문별 판정

| 질문 | 판정 | 근거와 남는 경계 |
| --- | --- | --- |
| Q1 첫8·변형 거부·상태 복구 | 범위 수용 | prepare:41–47,71–105,154–168. r=0.10의 B 3수준×U/C와 N0/E0만 허용한다. 외부 덱/메타 변형·다른 case 교환을 거부하고 임시 ARMS/TYPES를 복구했다. 정확한 현재 소스 출력 대조와 별도 양의 Bo D2 검사를 구분한다. |
| Q2 N0/E0 별도 계약 | 범위 수용 | prepare:94–99,123–143. 영 CED·등록 없음·N0 층상/2회전·E0 균일/0회전으로 분리되며 양의 GM/D2에 Bo0 우회를 만들지 않는다. 현재 출력의 공통 재료/시간은 별도 산술로 일치했다. 다만 zero helper가 D2의 모든 수치 시간 검사를 독립 반복하는 것은 아니다. |
| Q3 bytes·기하·E0·파일/소스 변경 | **부분, PRE8-01·02 열림** | 덱·메타·선택 dump·로그는 해시한 bytes를 직접 파싱한다. 출력 template 반경·선언 mesh scale·격자·E0 연결은 지켜진다. 그러나 없던 n_expected의 추가와 import 뒤 첫 해시 전 소스 변경에는 아래 반례가 있다. |
| Q4 D13·상별 수·E0 | 범위 수용 | observe:119–161. 초기 총누락0–10, ID1..N, 후속 ID별 type/radius 보존. 같은 재고의 행 순서 변경은 허용, ID별 type 바꿔치기는 거부. 계획/관측 상별 수는 별도로 남기고 새 상별 상한을 만들지 않는다. E0의 role·seed·세대·기하·계획수 등 비교 및 실제 prepare 경로가 N0/옛 E0 대체를 막는다. |
| Q5 접촉·군집·기존 M | 계산 의미 범위 수용 | contact:324–352, observe:269–308. 순간 겹침·전체 SE 분모·상별 중복을 올바르게 유지한다. 실제 cell_stats 합성 검산에서 세 격자 모두 S0=0.25, SR=0, S=0.0625, M=0.75. n_min20·원분산·QC·비유한/미정의·비클립을 대조했다. |
| Q6 fresh 완료 로그 | 합성 문법 범위 수용 | observe:209–240. 고정5열·run별 누적 endpoint·4개 Loop 조건을 검사한다. ERROR·resume·완전 연결 로그·열 결손·중간/최종 잘못된 endpoint 등의 변형을 거부한다. 실제 로그 호환성·프로세스 종료·rank·동일 실행·체크포인트 이력을 인증하지 않는다는 한정은 적절하다. |

파일명 단축은 `scripts/mixer_precal_prepare.py`, `scripts/mixer_precal_observe.py`, `scripts/mixer_contact_reader.py`를 뜻한다. 모든 행 번호는 위 핀의 동봉 파일 기준이다.

## 3. PRE8-01 P2 선택 입력 파일의 부재 상태가 봉인되지 않음

**위치:** `scripts/mixer_precal_observe.py:249–252`, 최종 재검사 `:85–89`, `:349–364`.

`n_expected`는 처음 존재하면 계획수와 대조하고 해시한다. 처음 없으면 그 **부재 자체**를 기록하지 않는다. 이후 검사에서는 이미 읽은 파일과 post/ 프레임 목록만 재확인하므로, 판독 중 새 n_expected가 생겨도 값이 반환된다.

**실제 반례:** 제출된 작은 E0 fixture와 같은 3입자 입력에서 `_load`가 반환한 직후 `n_expected`에 `999`를 새로 썼다. 결과는 `status=OK`, contact 존재, E0 원 격자 통계 존재, `counts.planned_total=3`, `observed_total=3`이었다. 새 파일은 `input_sha256`에 없다. **그대로인 최종 파일들을 즉시 다시 읽으면** `TECH: n_expected differs from planned count`가 되고 값은 제거된다.

프로파일 callback은 파일 생성 시점만 정하며 `_load` 반환값·검사·해시·계산을 대체하지 않는다. prepare binding만 작은 fixture용으로 mock했다. E0의 mixing 필드는 원분산과 `NOT_APPLICABLE`이므로, 이 반례가 유한한 정규화 M을 실측했다는 뜻은 아니다.

**무너지는 결론:** 판독 도중 계약에 참여하는 선택 파일의 추가도 탐지한다는 입력 집합 결속. 읽었던 dump bytes의 무결성이나 접촉 공식 자체가 틀렸다는 반례는 아니다. 정상 불변 파일 트리에서는 이 반례가 발생하지 않는다.

**최소 수정:** run과 E0 각각의 n_expected 존재/부재 상태를 최초에 고정하고 모든 반환 전 재검사에 포함한다. 기존 파일은 지금처럼 해시 검사, 처음 없던 파일의 출현은 TECH와 값 제거. dangling symlink도 같은 존재 상태 규약으로 처리한다. `_load` 후와 계산 도중의 생성, run/E0 양쪽에 회귀를 둔다. 다른 무관한 파일 전체를 감시하라는 요구는 아니다.

## 4. PRE8-02 P2 실행한 의존 코드와 기록된 소스 해시가 달라질 수 있음

**위치:** `scripts/mixer_precal_observe.py:20–23`, `:332–340`.

관측 모듈은 의존 모듈을 먼저 import한다. `analyse_run`은 그 뒤 디스크 소스 파일의 현재 SHA를 기록한다. 따라서 API를 import한 뒤 파일이 변경되면 메모리의 옛 함수로 계산하면서 새 파일을 출처로 기록할 수 있다. 첫 해시 이후의 변경은 현재 검사로 잡히지만, 이 구간은 잡히지 않는다.

**실제 반례:** 임시 복사 트리에서 정상 observer를 import한 뒤, 디스크의 `measure_mixing_index.py`에만 `cell_stats` 진입 즉시 `ValueError('Q34_STALE_MODULE_SENTINEL')`를 던지도록 추가했다. 메모리 함수는 바꾸지 않았다.

| 같은 소스 파일과 입력에 대한 호출 | 실제 결과 |
| --- | --- |
| 먼저 import한 프로세스의 analyse_run | OK, 기존 메모리 cell_stats 결과 반환 |
| 그 결과가 기록한 module SHA | `9f3bb091c49b3dafec3243ae5c27030ad27c95f7e6360c717d659f35876c6448` — 예외를 던지는 새 소스의 SHA |
| 같은 디스크 소스로 새 프로세스를 시작 | TECH, `Q34_STALE_MODULE_SENTINEL`, contact/mixing 없음 |

원래 파일 SHA는 `4375ec56c39ac997b9eca4d0bf30feb8ded06456a722329550230c1e0867c31a`이다. 원본 ZIP/수령 소스는 건드리지 않았고 임시 사본만 변형했다. 여기서도 prepare binding만 mock했으며 cell_stats·해시·파일 파서는 실제 함수다.

**무너지는 결론:** `module_sha256`만으로 해당 계산을 수행한 소스 bytes를 재현할 수 있다는 출처 결속. API import부터 종료까지 소스가 불변인 새 프로세스에서는 재현되지 않는 제한된 반례다. 수치 공식 자체의 결함 또는 정상 고정 트리 결과의 오류를 주장하지 않는다. 요청 Q3가 의존 소스 변경을 명시하고 있으므로 P2로 분류한다.

**최소 수정:** 실제 로딩 경계의 코드/해시를 결속하고 진입·반환 때 그 고정본과 비교한다. 예를 들어 검증한 불변 소스 사본에서 새 프로세스로 실행하거나, 해시한 로컬 소스 bytes를 실제 로딩/컴파일에도 쓰는 경계를 둔다. `analyse_run` 진입에서 디스크를 다시 해시하는 것만으로는 이미 메모리에 있는 코드와의 차이를 해결하지 못한다. 단순 디스크 현황 기록만 의도했다면 이름·계약을 그 수준으로 좁혀야 하며, 실행 코드 결속을 확보했다고 인계해서는 안 된다. import 후 파일 변경 반례와 새 프로세스 대조를 회귀로 남긴다.

## 5. 재현 명령과 증거 위치

증거 ZIP을 풀면 `received/`가 검토 핀의 한정 소스다. numpy/scipy가 있는 Python으로 리뷰 폴더에서 실행한다. 새로 쓰는 것은 리뷰 임시/결과 파일뿐이다.

```text
python verify_bundle.py
python run_direct_tests.py
python prepare_review/probe_prepare.py
python observe_binding_review/probe_observe_binding.py
python observe_semantics_review/probe_semantics.py
python probe_fresh_log.py
```

- PRE8-01·02: `observe_binding_review/probe_results.json`의 `optional_n_expected_created_after_load`, `same_files_next_invocation`, `dependency_changed_after_import_before_entry`, `fresh_process_same_recorded_source`.
- 대조: `post_listing_added_after_load`, `dependency_changed_after_load`는 TECH, 값 없음. D13 재고 재정렬/ID별 type 변경도 기록.
- 입력 ZIP과 원격 대조: `bundle_validation.json`, `remote_metadata.json`, `verify_bundle.py`.
- 기존 초안 보존 대조: `prior_common_file_comparison.json`.
- 직접 시험: `direct_test_results.json`, 두 stdout/stderr 로그. 초기 검토 래퍼 오류는 별도 폴더에 보존.
- 준비·관측 의미·로그 탐침은 각각 별도 결과 JSON에 있으며 시험 수를 합산하지 않는다.

## 6. 발견으로 추가하지 않은 경계

1. **N0/E0 현재 소스 공통 원인:** `_baseline`은 문법·재료/수·삽입 구조를 검사하지만 D2의 모든 수치 시간 검사를 반복하지 않는다. `_generate` 자체를 mock하여 일관되지 않은 timestep을 정답으로 돌려주는 경우 helper 통과를 보았으나, 정상 API는 그 외부 bytes를 거부한다. 명시된 현재 소스 출력 한계에 해당한다. 이번 8개 실제 메모리 출력은 공통 재료·dt `2.373e-7 s`·각 정착 `560606 step`·period `0.7825079857241121 s`로 별도 대조했다.
2. **선택 프레임:** 이 연결은 t0 및 마지막 완전 bin1, E0의 t0를 자격화한다. 그 외 프레임의 수치 내용을 전수 검증했다고 쓰지 않는다. post/에서 인식되는 목록 자체의 변경은 검사한다.
3. **기존 M의 공간 정의:** `measure_mixing_index.py:132–135`는 횡방향 bin 밖 좌표를 가장자리로 clip하고 축 방향 범위를 프레임 min/max로 정한다. 이번 어댑터는 기존 M을 재사용하며 입자 용기 내 존재나 실제 STL 기하를 인증하지 않는다. 이는 새 경로의 기하 자격을 과장하지 않기 위한 한정이다.
4. **QC와 결측:** n_min 미달 셀을 제외한 원분산, 전 비어 있지 않은 셀 분산, 상별 유지 부피 및 QC를 같이 남긴다. QC 실패는 유한 M을 자동 삭제하지 않는다. 분모 미정의·비유한 M은 UNDEFINED, 보조 원통계의 NaN은 null이다. E0의 M은 NOT_APPLICABLE이다.
5. **합성 양성 경로:** 독립 80입자 탐침은 실제 contact/cell_stats로 M을 계산했지만 prepare binding은 mock했다. 제출 자료의 unmocked 8조건 확인은 정상 덱이 프레임 부재에서 멈추는 음성 경계뿐이다. 둘을 합쳐 실제100000입자 양성 전체 경로가 통과했다고 주장하지 않는다.
6. **ABA 시험:** 옛 `test_raw_aba_cannot_change_metrics`는 현재 쓰지 않는 `O.read_dump` 이름을 patch한다. 다만 새 `_parse_dump` seam의 실제 ABA 시험이 별도로 있으며 수정 효력을 검증한다. 전체 ABA 보강이 무효라는 새 finding으로 세지 않는다.
7. **범위 보존:** 수령 기록의 Q1–Q4 채택은 저자 결정 기록으로 읽는다. 이번 검토가 비준을 대신하지 않는다. MXD2R 별도 외부 재확인 대기와 실제 로그/바이너리/MPI/물리 자격 미검증을 유지한다.

**최종: 첫8 정적 준비 수용. 합성 관측 연결의 전체 수용은 PRE8-01·02 보완 전 HOLD. 전체 게이트 및 실제 실행/배포는 계속 HOLD.**
