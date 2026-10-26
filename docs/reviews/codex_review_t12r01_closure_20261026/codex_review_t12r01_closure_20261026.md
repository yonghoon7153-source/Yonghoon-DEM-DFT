# Codex 외부 재확인 — T12R-01 자동 fetch 차단 (2026-10-26)

검토 핀: **`96f15ed17e03181b6096fb65f71ec7f577f17523`**, `codex/dem-gen2-t12r`.
코드 후보: `3eecce8af503556b678f8f4a02343e6bce3d0b83`.
비교 기준: `bffc42cab29da37b45f8a713e30e8572b91e7da3`.
고정 소비자: `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`.

## 1. 종결 판정

**T12R-01 [P2] — CLOSED. 고정 소비자 snapshot 읽기의 자동 fetch 차단과 정상 52개 결과 보존을 수용한다.**

누락 객체의 실패 코드만 확인한 판정이 아니다. 실제 Git trace에서 **fetch 자식 호출 0회**, 각 읽기의 **명시적 금지 옵션·금지 환경**, **시험 저장소 전체 파일의 byte hash 불변**을 함께 확인했다. 동일 환경에서 보호를 제거한 대조는 실제 fetch **3회**를 기록했다.

이 종결은 오프라인 소스 읽기 경계에 한정된다. 기존 P1 계약/52 관측 해석 및 ULPRI-01/02의 좁은 종결은 유지한다. **실제 P2 T12는 NOT_RUN, 물리 실행 GO는 부여하지 않는다.** 새 등록값·실제 생산자·WSL 실행·Claude 통합·전체 설계 GO를 의미하지 않는다.

## 2. 질문별 답

| 질문 | 판정 | 독립 증거 |
|---|---|---|
| Q1. 모든 snapshot Git 호출이 두 보호를 강제하는가 | **수용** | `snapshot()`은 호출자 환경을 복사한 뒤 `GIT_NO_LAZY_FETCH="1"`로 덮어쓰고 모든 `git show`에 `--no-lazy-fetch`를 지정. 상위 환경을 0으로 준 실제 실행에서도 trace의 값은 1, 옵션도 존재. |
| Q2. 누락 commit/tree/blob에서 rc 2와 fetch 0, 객체 DB 불변인가 | **수용** | commit 1개·tree 4개·blob 6개를 각각 누락시킨 **11조건 전부** rc 2 / fetch 0 / 전체 저장소 파일 불변. 보호 전체 제거 대조는 rc 2이지만 fetch 3. |
| Q3. 정상 52·소스 hash·기존 거부/변이 시험이 보존됐는가 | **수용** | 완전한 필요 객체 입력: 52/52 PASS, 사례별 기대/관측값 동일, 여섯 소비자 hash 동일. 기존 소스/계약 거부 8/8, 표적 소비자 변이 13/13 재현. |
| Q4. 지원하지 않는 Git·오류 안내·플랫폼 한정이 정확한가 | **수용, 검증 환경 한정 유지** | 옵션 미지원 응답은 명시적 mock으로 시험: 첫 호출에서 거부, 읽어 쓴 소스 파일 0개, 보호 없는 재시도 없음. 실제 Windows Git 2.55.0에서 보호를 검증. 옛 Git 실물 또는 모든 플랫폼을 검증했다는 주장은 하지 않음. |

## 3. 입력과 변경 범위

제출 ZIP: `codex-dem-gen2-t12r-96f15ed17e03.zip`.

- 크기: **3,078,303 bytes**.
- SHA256: **`fd52dd397e47ee93d91432b4c045c43196b51527d5c52038b4c863d233518bb7`**.
- 373항목, 저장소 파일 **369개**, MANIFEST **372개 항목**: 길이·SHA256·Git blob ID 대조 전부 일치.
- 원격에서 `96f15… → 3eecce… → bffc42…` 부모 관계를 확인했다. 후보 변경 목록 168개와 최종 증거 커밋 변경 목록 12개를 두 페이지까지 읽어, 직전 외부 검토에서 원격과 대조한 190개 기반 파일에 적용했다. **369개 모두 고정 핀 blob과 일치**한다. 두 Python 파일은 고정 원격에서 직접 읽어 bytes도 대조했다.
- 기존 파일 수정은 `scripts/test_dem_gen2_t12_consumer_contract.py` **하나**다. 새 오프라인 회귀와 문서/증거는 추가다. 소비자 여섯 파일·params·52개 기대값이 변경됐다는 증거는 없다.

핵심 diff는 다음뿐이다. 전체 diff는 `evidence/runner.diff`에 보존했다.

```python
git_env = dict(os.environ, GIT_NO_LAZY_FETCH="1")
result = subprocess.run(
    ["git", "--no-lazy-fetch", "-C", str(repo), "show", f"{PIN}:{PREFIX}{name}"],
    capture_output=True, check=False, env=git_env,
)
```

위치: [`scripts/test_dem_gen2_t12_consumer_contract.py:38–46`](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/96f15ed17e03181b6096fb65f71ec7f577f17523/scripts/test_dem_gen2_t12_consumer_contract.py#L38).

상위 환경에 맡기지 않으며, 환경 변수만 무시하는 버전에 조용히 의존하지도 않는다. 전역 옵션을 지원하지 않으면 해당 Git 실행 자체가 실패하고 `snapshot()`이 ValueError로 중단한다. 이전의 무조건적 `No fetch was run.` 문구는 능력 요구·명시적 소스 확보 안내·보호된 읽기 설명으로 교체됐다. 자동으로 옵션을 빼서 재시도하는 fallback은 없다.

## 4. 실제 재현 — rc와 fetch를 분리해서 관측

### 4-1. 환경과 방법

외부 재확인 환경: **Windows / Python 3.12.14 / Git 2.55.0.windows.3**.

독립 스크립트 `probe_offline_independent.py`를 새로 작성하여 수정된 runner 원문을 실행했다. 작성자 오프라인 회귀의 PASS 선언을 읽어 판정한 것이 아니다.

- 원래 commit/tree/blob의 SHA1을 검증한 별도 객체 저장소 사용. 필요한 객체는 commit 1·tree 4·여섯 소비자 blob, 합계 11개.
- 시험마다 별도 저장소를 만들고 해당 객체 하나만 제거.
- promisor/partial-clone 설정과 빈 **로컬 bare 원격** 사용. `GIT_ALLOW_PROTOCOL=file`로 외부 전송 차단.
- 호출자 `GIT_NO_LAZY_FETCH=0` 고정. Git trace2의 실행 argv와 환경값을 기록.
- `.git/objects`뿐 아니라 시험 저장소의 **모든 파일**을 전후 SHA256으로 대조. trace/결과 출력은 저장소 밖에 기록.
- 공유 checkout·브랜치·인덱스·생산 소스는 변경하지 않음. 물리 시뮬레이션·MPI·WSL·클러스터는 실행하지 않음.

### 4-2. 결과

| 입력 | 조건 수 | 반환 코드 | 실제 fetch 호출 | 저장소 파일 |
|---|---:|---:|---:|---|
| 필요한 객체 11개 모두 존재 | 1 | **0** | **0** | 불변 |
| 소비자 commit 누락 | 1 | **2** | **0** | 불변 |
| root/docs/data/kit tree 각각 누락 | 4 | **2** | **각각 0** | 전부 불변 |
| 여섯 소비자 blob 각각 누락 | 6 | **2** | **각각 0** | 전부 불변 |
| 보호 환경 강제 + 옵션을 둘 다 제거한 대조 | 1 | **2** | **3** | 대조의 fetch 발생으로 결함 검출 |

누락 tree는 root와 최종 kit만이 아니라 중간 `docs`, `docs/data`까지 포함한다. blob은 `ul_gates.py` 한 개에 한정하지 않고 `ul_reader.py`, `ul_lib.py`, `ul_observers.py`, `ul_s3.py`, `unload_params.json`까지 각각 시험했다.

정상 조건에서 실제 `show`는 **6회**이며, 여섯 호출 모두 `--no-lazy-fetch`가 있고 환경 trace의 `GIT_NO_LAZY_FETCH`가 **1**이다. 누락 조건에서 실행된 읽기들도 전부 동일한 보호를 갖는다.

보호 제거 대조에서는 다음 실제 자식 명령이 trace에 나타났다:

```text
git -c fetch.negotiationAlgorithm=noop fetch origin --no-tags
    --no-write-fetch-head --recurse-submodules=no --filter=blob:none --stdin
```

실패 코드가 같은 rc 2여도 자동 fetch는 발생할 수 있다는 직전 반례가 살아 있다. 이번 수정은 그 반례에서 **fetch를 없앤 것**까지 관측됐다. `evidence/independent_offline/result.json`과 조건별 `trace.jsonl`이 근거다.

### 4-3. 정상 52개 결과 보존

완전한 필요 객체 조건의 stdout JSON을 기존 `fixture-results.json`과 직접 비교했다.

- `case_count=passed=52`, `status=PASS`.
- **52개 사례의 case/function/expected/observed/kind/pass 등 전체 `cases` 배열 동일**.
- **여섯 `source_sha256` 동일**, manifest 및 기존 영수증과 모두 일치.
- `physical_ready=false`, `physical_T12=NOT_RUN` 유지.
- runner 자체가 수정됐으므로 `fixture_script_sha256`은 새 파일을 가리켜야 한다. 이를 옛 값과 같아야 하는 항목으로 취급하지 않았다.

### 4-4. 기존 거부·변이 재현과 호환성 한정

새 runner를 `--source`로 주고 고정 소비자 소스를 그대로 사용하는 기존 harness도 재실행했다.

| 검사 | 실제 결과 | 범위 |
|---|---|---|
| 소스 오류 5 + 계약 결손 3 | **8/8** | 기존 거부 유지 |
| 소비자 표적 변이 | **13/13 검출** | 지정 의미 실패 검출. crash를 검출로 대신하지 않음 |
| 옵션 미지원 응답 | **mock PASS** | 자식 호출 1회, 출력 소스 0개, 보호 강제, ValueError. 실제 옛 Git 시험 아님 |

Windows harness 자식에는 UTF-8 옵션만 추가했다. 대상 소스·기대값을 바꾸지 않았다. 이번 독립 결과는 작성자의 Linux Git 2.52.0 기록과 별개이며, 모든 Windows/Git 버전 지원 인증으로 확대하지 않는다.

공유 **155**는 새 후보의 제출 로그와 영수증 연결만 감사했다. 로그 hash 일치·성공 표지 155를 확인했으나 독립으로 155개를 다시 실행하지 않았다. 새 직접/오프라인 시험의 CI 배선은 여전히 별도다. 52·8·13·13개 조건 등을 하나의 물리 커버리지 숫자로 합산하지 않는다.

## 5. 상주 회귀와 남는 경계

`scripts/test_dem_gen2_t12_offline.py`의 검사 구조도 목적과 일치한다.

- `:108`에서 상위 금지 값을 0으로 놓는다.
- `:114–124`에서 실제 fetch 자식·옵션·객체 DB 불변·rc를 함께 검사한다.
- `:127–134`에서 여섯 읽기와 기존 52개 관측/소스 hash 보존을 확인한다.
- `:136–139`는 commit/root-tree/kit-tree/blob 누락 조건.
- `:140–155`는 명시적으로 구분한 미지원 옵션 mock.
- `:157–174`는 두 보호를 제거해 실제 로컬 fetch가 발생하는지 확인하는 대조.

상주 회귀 소스를 읽고 그 핵심 주장을 독립 구현으로 재현했다. 이 Windows 재확인에서 작성자 `test_dem_gen2_t12_offline.py` 자체를 원 명령으로 재실행했다고 주장하지 않는다. 사용자 질문의 대상인 **수정된 실제 loader**는 13개 독립 실제 조건에서 실행했다.

지원 Git의 올바른 동작과 신뢰할 수 있는 Git 실행 파일이라는 정상 전제 아래의 보장이다. 임의의 대체 실행 파일이나 악성 환경 전체를 격리한 보안 sandbox 인증은 아니다. 이 한정은 T12R-01을 다시 열 근거가 아니다.

P2 인터페이스·R-a/S0·실제 바이너리/이력·T10–T13·Q7–Q9 측정·통합 트리 조건은 직전 회신 그대로 남는다. **오프라인 loader 종결은 물리 자격의 대체 증서가 아니다.**

## 6. 재현과 반환

검토 ZIP을 새 폴더에 펼친 뒤:

```bash
python3 -I -X utf8 -B build_object_repo.py
python3 -I -X utf8 -B probe_offline_independent.py --out ./fresh_offline_recheck
```

Python 표준 라이브러리와 Git 필요. 객체 저장소는 동봉한 원 metadata와 여섯 소비자 파일로 새 검토 폴더 안에 재구성하고 원 Git 객체 ID를 확인한다. 외부 fetch가 필요하지 않다. 대조의 fetch는 로컬 file 원격뿐이다. 출력 폴더는 새 이름을 쓴다.

`evidence/independent_offline/result.json`, `evidence/loader/report.json`, `evidence/mutants/report.json`, `evidence/provenance_audit.json`, `evidence/runner.diff`에 근거를 보존했다. `review_scope.json`은 범위 한정 외부 종결 기록이며 범용 실행 GO 칸에 넣지 않는다.

**T12R-01 CLOSED — 자동 fetch 차단과 정상 52개 보존에 한한 GO. 실제 물리 실행 GO는 별도.**
