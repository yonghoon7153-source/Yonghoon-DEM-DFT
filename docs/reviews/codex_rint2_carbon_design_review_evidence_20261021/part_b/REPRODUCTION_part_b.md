# Part B 재현 안내 — 독립적으로 풀어 쓰는 패키지

작업 위치는 ZIP을 푼 **리뷰 루트**(`source/`와 `part_b/`가 나란히 있는 폴더)이다. Python 3.10 이상과 설치된 NumPy·SciPy가 필요하다. 검토 환경은 Python 3.12.14 / NumPy 2.5.3 / SciPy 1.16.3이었다. 네트워크·Git·DEM/MPM 실행 파일·이전 리뷰 폴더는 아래 재현에 필요 없다.

`run_review.py`는 현 PC의 기존 의존성 폴더가 있으면 재사용하지만, 그런 폴더가 없는 다른 PC에서는 일반 Python 설치 패키지를 사용한다. 모든 임시 파일·출력은 `part_b/tmp`, `part_b/evidence`, `part_b/adapted` 아래에만 쓴다. `source/`는 수정하지 않는다.

## 최소 재현

```bash
python -X utf8 -B part_b/independent_join_checks.py
python -X utf8 -B part_b/known_limit_and_mutant.py
python -X utf8 -B part_b/run_review.py test test_rint_g2_join.py
```

- 독립 대조 62건: 예상과 일치. 32 PASS에는 공개된 잔여 F1 false-G-frame 8건이 포함되므로 “62건 인증”이라는 뜻이 아님.
- wd-only 현행 REJECT → 메모리 변이 PASS, 공개된 단위 underflow PASS를 재현.
- 원 시험: Linux 예상 324/324(저자 보고), 이 검토의 Windows 실제 320/324. 네 실패는 CRLF 픽스처 재변환 문제이다.

Windows에서 그 네 실패의 원인이 **시험 작성기 한 줄**임을 분리:

```bash
python -X utf8 -B part_b/run_review.py test test_rint_g2_join.py --lf-test-writer
```

이 옵션은 실행 메모리에서만 시험의 `open(...,'w')`에 `newline='\n'`을 준다. 생산 parser·원본 시험 파일은 안 바꾼다. 검토 실측 324/324.

## 지난 탐침의 동일 논리 재생

```bash
python -X utf8 -B part_b/run_review.py probe structure_probe.py
python -X utf8 -B part_b/run_review.py probe numeric_review.py
python -X utf8 -B part_b/run_review.py probe numeric_overflow_replay.py
python -X utf8 -B part_b/run_review.py probe structure_minimal_replay.py
```

`numeric_overflow_replay.py`는 앞선 `numeric_review.py`가 만든 합성 입력을 읽으므로 위 순서로 실행한다. 마지막 `structure_minimal_replay.py`는 수정된 실제 정량 관문이 첫 반례를 차단하여 **반환코드 1, `join_gate_failed(T4-2 n=1)`**로 끝나는 것이 예상 결과다. 144건 구조 탐침이 대응 두 반례를 모두 포함한다.

이전 탐침 원문 네 개와 실제 사용한 옛 join 모듈 둘·보존 합성 입력 30개(총 36파일, 152,916바이트)는 `part_b/baseline/`에 정확 바이트로 동봉했다. `MANIFEST.json`에 SHA256과 원 핀을 적었다. harness가 경로만 이 패키지로 바꾸며 산술·assertion은 변경하지 않는다. 과거 탐침 JSON 내부의 과거 `source_pin` 문자열은 보존된 설명이다. 이번 실제 실행 경로·import 해시와 함께 읽는다.

옛 모듈 비교는 **join 모듈만 바꾸고 현재 의존성과 소비자를 유지하는 통제된 대조**이다. 과거 전체 스택을 재구성했다는 뜻은 아니다.

## 주변 selftest

```bash
python -X utf8 -B part_b/run_review.py test step3_sigma.py --test-arg=--selftest
python -X utf8 -B part_b/run_review.py test step3_sigma.py --test-arg=--selftest-rint
python -X utf8 -B part_b/run_review.py test rint_t41_census.py --test-arg=--selftest
```

현재 전체 핀에서 셋 모두 PASS. Windows에 없는 `resource`는 메모리 사용량 표시만 NaN으로 만드는 shim을 쓴다. solver·NumPy·SciPy·수치 입력은 대체하지 않는다. cleanup은 `part_b/tmp`의 자식 경로만 허용한다.

## 현재 패키지만으로 다시 실행하지 않는 역사 비교

- 현재 324 assertion을 이전 전체 모듈에 적용한 179/324 결과.
- 이전 138 assertion의 현행 통과, 초기 주변 228 assertion 결과.

이 실행 로그와 import 해시는 동봉하되, 이전 전체 snapshot과 이전 시험 파일 전체를 다시 중복 포장하지 않았다. 이 결과를 재실행하려면 해당 과거 리뷰 source/test 판본이 별도로 필요하다. `verify_fullpin.py`와 `package_baseline.py`도 검토자의 초기 포장/대조용 도구이며, 수신자가 위 재현을 위해 실행할 필요는 없다.
