# PRE8-01·02 한정 재확인 — 2026-11-05

**판정: 두 결속 보완을 코드·소형 합성 재현 범위에서 수용한다. 새 P1/P2/P3 없음. 전체 게이트 HOLD 및 실제 실행 미승인은 그대로다.**

PRE8-01의 원 반례와 PRE8-02의 원 반례는 이전 코드에서 다시 발화했고, 새 핀에서는 TECH와 값 제거로 막혔다. 다만 이번 Windows 환경에서는 실제 심볼릭 링크를 만들 권한이 없어 그 경로의 독립 동적 검증은 하지 못했다. 이를 Linux 통과 또는 관측 시험 28/28 외부 통과로 적지 않는다.

## 1. 대상과 바이트 확인

| 항목 | 독립 확인 결과 |
|---|---|
| 새 검토 핀 | `ec484c2719d6a444214ddc9c48fe683a7735688b` |
| 이전 검토 핀 | `189930cc68b6e58beb6b4546d80353dc03852195` |
| 가지 | `codex/mixer-1104` |
| 입력 ZIP | `codex_mixer_precal_pre8_recheck_20261105_ec484c2719d6.zip` · 2,636,322 B |
| ZIP SHA256 | `a98c72a6930a2029b6e2ea21b8948503610a112e95315a85b62e6b6b0bbfc77c` |
| 포장 검사 | 107멤버 중 자기 목록을 제외한 106개 SHA256 일치 |
| 스냅샷 검사 | 89파일의 크기·SHA256·Git blob 전부 일치; 원격 고정 핀의 파일 SHA/크기 89개도 일치 |
| 이전 공통 파일 | 54개 중 51개 동일. 변경 3개 = 관측기·관측 시험·첫8 준비 README |
| 원 외부 판정·증거 ZIP | 이전에 반환한 파일과 바이트 동일. 증거 ZIP SHA256 `908d6194f3e522d50aadc826bafeefa68801401c7880b9e27336a7872764f949` |

`PIN.txt`를 새 대상으로, `PREVIOUSLY_REVIEWED_PIN.txt`를 과거 판정 대상으로 읽었다. `REQUEST.md`와 저장소 내 요청서는 같은 범위다. 기존 생성기·준비기·과학 계산 소스·조건표·SOP의 공통 파일은 변경되지 않았다. 작성 측의 통과 로그는 별도 제출 근거로 보존했으며 이번 외부 실행 수에 더하지 않았다.

원격 대조는 [해당 핀의 관측기](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/ec484c2719d6a444214ddc9c48fe683a7735688b/scripts/mixer_precal_observe.py)와 같은 핀의 디렉터리 메타데이터를 사용했다. 해시 일치는 출처 확인이며 실행·물리 자격을 뜻하지 않는다.

## 2. 항목별 판정

| 항목 | 판정 | 닫을 수 있는 범위 | 닫지 않은 범위 |
|---|---|---|---|
| PRE8-01 / P2 | **원 결함 닫힘 가능, 보완 한정 수용** | run/E0의 초기 부재 봉인, 일반 파일의 출현·삭제·내용 변경/교체 거부, TECH 시 값 제거 | 실제 symlink 동적 검증, 모든 순간의 생성·삭제 이력, 파일 객체 신원 불변 인증 |
| PRE8-02 / P2 | **원 결함 닫힘 가능, 보완 한정 수용** | 해시한 8의존 소스 bytes의 실행, 내부/지연 import·별칭·자기 소스 읽기, observer code 동등성, 입·출구 검사와 bootstrap 오류 응답 | Python/외부 라이브러리 공급망, 임의 메모리 변조, observer의 역사적 주석 원문 유일 복원 |
| 체크포인트 정정 | **문서 전달 범위 수용** | 비트 동일성 미보장·동일 방식 재계산 비교 선행·전체 쌍 힘 사영이라는 문구와 한정 | P1 소스/실행/334쌍 실측의 독립 판정 |

이 표는 원장 종결을 실행한 기록이 아니다. 이전 첫8 정적 준비의 수용도 이번 관측 연결 전체나 실제 실행 GO로 확대하지 않는다.

## 3. PRE8-01 — 초기 부재를 빠뜨리던 반례

### 이전/현재 실제 함수 대조

원 외부 탐침과 같은 3입자 E0 입력에서 `_load` 반환 직후 `n_expected`를 `999`로 생성했다.

| 코드 | 결과 | 반환 값 |
|---|---|---|
| 이전 핀 | `OK` | contact/mixing/counts 남음 |
| 현재 핀 | `TECH: optional input presence changed` | contact/mixing/counts 제거 |
| 같은 최종 파일을 현재 코드에 다시 입력 | `TECH: n_expected differs from planned count` | 값 제거 |

새 코드는 `scripts/mixer_precal_observe.py:340–350`에서 파일을 읽기 전 존재·부재를 별도로 기록한다. `:165–171`의 `lstat`는 dangling symlink를 부재로 오인하지 않도록 작성돼 있다. `:181–190`은 존재 스냅샷과 기존 파일의 SHA를 함께 확인하고, `:450`, `:452`, `:465`에서 계산 전·후 및 예외 뒤 재확인한다. `:468–469`는 비정상 응답의 contact/mixing/counts/reference_counts를 제거한다.

### 추가 독립 탐침

`task/pre8_absence/probe_pre8_absence.py`: **71개 실행 관측이 예상대로 동작**했다. TECH 59, 정상/비대상 대조 OK 12이며 시험 메서드 수와 합산하지 않는다.

- run/E0 reference 각각에서 정상 숫자와 잘못된 숫자의 파일 출현을 시험했다. `_load` 직후, 실제 contact 계산 반환, 실제 cell_stats 반환 시점 모두 TECH였다. 따라서 숫자가 맞으면 파일 출현을 허용하는 구조가 아니다.
- 기존 정상 파일의 삭제, 숫자 변경, 같은 숫자에 공백 추가, 다른 bytes 파일로 교체를 위 시점에 주입했다. 전부 TECH와 네 값 필드 제거였다.
- 기존 부재/정상 파일이 불변인 경우 OK, 처음부터 잘못된 값이면 TECH였다.
- 같은 bytes로 교체하거나 무관한 파일을 추가하면 OK였다. 이것은 내용/선택 경로 결속의 경계이며 inode 불변 인증이 아니다. 현재 요청도 모든 순간의 생성 후 삭제를 감시한다고 주장하지 않는다.

48입자·두 셀의 회전 run/E0 reference 양성 대조에서는 실제 contact·cell_stats를 사용했다. 세 격자에서 `S0=0.0017361111111111104`, `SR=0`, `M_mean=1`이었다. 이는 수정된 결속 검사가 모든 정상 계산을 막는지 보는 합성 대조다. `validate_case`만 단위 경계에서 mock했고, 계산·파서·해시·반환값은 mock하지 않았다. 실제 100000입자 준비→관측 양성 전체경로를 대체하지 않는다.

### 실제 심볼릭 링크 한정

실제 dangling symlink 생성은 Windows `WinError 1314`로 거부됐다. 독립 탐침의 21개 예정 조합은 **미실행**으로 기록했다. 소스의 `lstat`/regular-file 거부 경로는 읽었지만 Linux에서 독립 실행했다고 쓰지 않는다.

상주 시험도 이 한정을 드러냈다. `test_optional_n_expected_initial_presence_contract`는 링크 생성 단계에서 ERROR였다. 또한 `test_optional_n_expected_creation_is_tech`의 링크 생성은 observer 호출 안의 callback에 있으므로 권한 오류도 TECH로 잡혀 그 메서드가 통과할 수 있다(`test_mixer_precal_observe.py:385–418`). 그러므로 그 녹색만으로 링크 출현 반례가 발화했다고 세지 않았다. 전체 상주 묶음은 ERROR로 끝났으므로 전체 false-green은 아니며 새 제품 결함으로 등급을 붙이지 않았다. 선택적인 시험 보강은 링크 생성 성공 확인과 기대 사유 검사를 따로 두는 것이다.

## 4. PRE8-02 — 출처 해시와 실제 실행 소스

### 원 sentinel 반례

`measure_mixing_index.cell_stats`를 import한 뒤, 디스크 원문에 raising sentinel을 추가하고 분석했다.

| 관측 | 이전 핀 | 새 핀 |
|---|---|---|
| 같은 프로세스 | 옛 함수로 `OK` | `TECH: bound source changed: measure_mixing_index` |
| 기록 SHA | 변경된 원문 `9f3bb091…` | 실제 캡처 원문 `4375ec56…` |
| contact/mixing/counts | 남음 | 제거 |
| 변경된 원문을 새 프로세스로 읽음 | sentinel 실행 후 TECH | sentinel 실행 후 TECH |

수정 뒤에는 바뀐 디스크의 SHA를 옛 실행 코드의 출처로 붙이지 않는다. 원 외부 탐침의 이전/수정 기대판을 각각 실제 실행했고, 9관측씩 결과를 `external_replay_old/`, `external_replay_fixed/`에 남겼다. 기대판 변경만으로 수용한 것이 아니라 다음 별도 탐침으로 실행 경로를 확인했다.

### 새 로더에 대한 독립 12관측

`task/pre8_loader/probe_loader.py`: **12/12 예상대로 동작**, 새 반례 없음.

| 공격 | 독립 관측 |
|---|---|
| 동일 mtime·size를 유지한 OLD→NEW 소스와 오래된 timestamp pyc | canonical 모듈은 OLD, private 모듈과 실제 cell_stats의 표지는 NEW; 기록 SHA는 NEW bytes와 일치 |
| 8개 canonical 이름을 오래된 빈 객체로 선점 | 기존 sys.modules 객체를 바꾸지 않고 private 함수·6개 별칭이 새 집합에 결속 |
| 실제 diff의 lazy import | 메모리의 정적 U/C 자료로 readback/diff 실행 성공, canonical 선점 우회 없음 |
| 실제 generator.deck_meta의 자기 소스 읽기 중 디스크 변경 | generator SHA는 캡처 bytes; 덱/메타 동일. 변경 중 관측은 TECH, 복구 후 OK |
| 의존 소스 부재·구문 오류·실행 중 예외 | bootstrap TECH·값 제거; contact 예외 클래스 미정의로 인한 2차 예외 없음 |
| observer 자신의 stale pyc + 의미 코드 변경 | code 동등성 검사에서 TECH |
| observer stale pyc + 주석만 변경 | 동등 코드로 수용, 현재 기록 bytes SHA 사용; 문서의 역사 원문 비보장과 일치 |
| `_load` 뒤·실제 계산 중 의존 소스 변경 | TECH·모든 값 제거 |

구현 근거는 `mixer_precal_observe.py:35–43`(소스 capture), `:47–83`(private import/open 및 실제 compile/exec), `:86–107`(자기 code 대조·8의존 집합·고정 digest), `:174–190`(경계 대조), `:428–438`(고정 SHA 기록·bootstrap 조기 TECH)다. 파일을 나중에 다시 import하여 해시와 계산이 갈라지는 원래 경로는 제거됐다.

추가로 `task/pre8_boundary/probe_boundary.py`의 **7그룹**에서 자기코드 삭제/불일치, 실제 CLI의 소스 부재·SyntaxError(JSON TECH·rc 2·stderr 없음), 같은 모듈의 `OK→TECH→OK→TECH→OK`, 성공/실패 뒤 생성기 전역상태 복구, `-O` 실행을 확인했다. 이 7그룹은 12관측 또는 상주 메서드 수에 합치지 않는다.

의존 8개는 해시한 bytes를 실제 실행하며, observer 자신은 기록 bytes와 실행 중 module code의 동등성을 확인한다. 이 둘의 보증은 다르다. 주석이 다른 동등 코드는 허용될 수 있고, bootstrap TECH에 부분 SHA가 남는 것은 전체 로딩 성공을 뜻하지 않는다. 그 경계는 요청서·출력·README에 이미 명시돼 있어 새 결함으로 올리지 않는다.

## 5. 상주 시험과 실행 범위

외부 실행 환경: **Windows 11 · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3**. Python 3.8/3.11은 작성 측 기록이며 여기서 재실행하지 않았다.

| 묶음 | 이번 독립 실행 | 해석 |
|---|---|---|
| 원본 관측 상주 시험 | 28메서드 실행: 27 OK, 1 ERROR | ERROR는 symlink 생성 권한; rc 1. 28/28 PASS로 고치지 않음 |
| 원 외부 탐침 재생 | 이전 9관측 / 현재 9관측 | 두 원 결함의 전후 결과 보존 |
| PRE8-01 추가 | 71관측 예상대로 / 실제 symlink 21 미실행 | 작은 일반 파일 입력 경계 |
| PRE8-02 추가 | 12관측 예상대로 | 캐시·private 로더·자기 읽기 등 |
| bootstrap/재호출 추가 | 7그룹 예상대로 | 자기 코드·CLI·상태 복구 |
| 준비 14메서드 / 전체 check_all | **이번 미실행** | 이전 준비 수용을 새 실행 수로 세지 않음 |

PRE8-02 및 경계 탐침의 최초 래퍼 실행은 기본 임시 폴더 접근 문제로 일부 fixture 진입 전에 실패했다. 실패 기록은 보존했고, 탐침의 tempfile 위치만 작업 디렉터리로 고정한 뒤 완료했다. 대상 코드 수정으로 실패를 덮지 않았다.

모든 수정 주입은 임시 복제본에만 수행했다. 받은 소스 10파일은 전후 동일하고, 완료 때 스냅샷 89개/포장 106개도 재검산했다. 과학 수식·등록·공유 원장을 고치지 않았다.

## 6. 체크포인트 정정·수령 기록

`docs/reviews/mixer_precal_first8_preparation_20261104/README.md:33` 및 새 수령 README §4는 다음 세 내용을 전달 자료로 한정한다.

1. `write_restart`도 원 런 스텝 끝 접촉 덤프와 비트 동일성을 보장하지 않는다는 정정.
2. 같은 방식으로 재계산한 값끼리 비교하는 정의를 먼저 고정한다는 후속 원칙.
3. `force_normal`은 전체 쌍 힘의 중심선 사영이며, 전달받은 334/3,111쌍 관찰은 이 검토의 실행/독립 P1 판정이 아니라는 한정.

문구와 범위는 요청과 일치한다. 이 판정은 그 물리·수치 해석을 새로 재현한 인증이 아니다. P1 코드·허용폭·RJ323957·실제 checkpoint 시험은 다루지 않았다. 기존 MXD2R 재확인 대기, D0.7 종료 후·1저자 승인 후라는 순서, Rint② 우선, 실행/등록/통합 미승인은 보존돼 있다.

## 7. 재현과 최소 후속

증거 ZIP을 풀고 그 최상위에서 NumPy/SciPy가 있는 Python으로 실행한다. 실제 호스트나 연구 경로가 필요하지 않다.

```text
python -I -B -X utf8 verify_intake.py
python -I -B -X utf8 run_resident.py
python -I -B -X utf8 replay_external.py old
python -I -B -X utf8 replay_external.py fixed
python -I -B -X utf8 task/pre8_absence/probe_pre8_absence.py
python -I -B -X utf8 task/pre8_loader/probe_loader.py
python -I -B -X utf8 task/pre8_boundary/probe_boundary.py
```

`run_resident.py`는 대상 소스를 수정하지 않고 임시 위치와 import 경로만 지정한다. Windows symlink 권한이 없으면 원본 시험의 rc 1을 그대로 기대한다. 실 symlink 분기까지 외부 동적 통과를 주장하려면 링크 생성 가능한 허용된 합성 환경에서 그 분기를 따로 확인하고 실제 생성·기대 사유를 기록해야 한다. 이 요구는 실제 ibb/WSL 실행을 뜻하지 않는다.

새 차단 코드 수정 요구는 없다. 원장에는 이 판정의 두 결속 보완 범위와 미실행 경계를 함께 옮길 수 있으나, 이 검토자가 원장을 변경하거나 종결 작업을 실행하지는 않았다.

**PRE8-01·02 보완 한정 수용 / 새 P1·P2·P3 없음 / 전체 HOLD·실제 실행 미승인 유지.**
