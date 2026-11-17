# 탈압 A1 — RT 순서와 재개 파일 결속 준비 (2026-11-17)

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 탈압 A | RT1 → RT2 연결 | 1: 복사본 구현·소형 모의 확인 | 러너 12/12; 결속 19통과·1건너뜀; 현장 0 | 30열 왕복·연속 관문 → 증서 발행/재판독 → 20검사 fixture 연결 |
| 탈압 B | 기존 NP2/4 N40000 | 2: 개발 자료 고정 | 3144/3144 · 3103/3103 (기수령) | 반복하지 않음; 알려진 실패 경로 한계 보존 |

## 1. 바탕과 이번 연결

바탕 커밋은 `716c59f9afe18d88674712835d870fa3cb5b68eb` (stoic 반입 ⑦)이다. 정본은 docs/reviews/dem_unloading_ps45_prereg_20261009.md §15-2·15-4·15-5·15-5c/d, 작업 순서는 docs/reviews/p1_g2cp_mpi_development_20261116/results_20261116/next_steps.md §3이다. 앞 덱 층은 docs/reviews/p1_rt_deck_preparation_20261116/README.md에 있다.

docs/reviews/p1_rt_runner_preparation_20261117/prepare_rt_runner.py는 원 러너의 고정 바이트를 확인하고 새 복사본에 RT 연결 후보를 만든다. 기존 `run_deck` 함수와 NP·실행 파일·MPI·추가 변수 전달은 바꾸지 않는다. G0 → (7:3) Ut0 → R → UN 뒤 RT1 → RT2를 넣고, 성공 뒤에만 해당 UK로 간다. 앞 단계 실패는 RT 둘을 명시적으로 건너뛰고, RT1 실패·표지/바이너리 결손·해시 오류/변경은 RT2를 막으며 RT2 실패도 UK를 막는다. 10:0 RJ는 UK가 없고 RJ2에는 있다.

잡 머리의 `job_dir`, RT1 뒤 `rt1_bin`, RT2 직전 `rt2_ckpt`를 별도 키로 적는다. 두 기록과 RT2 입력은 같은 `$JD/RT1/rt.bin` 글자를 사용한다. RT1 뒤와 RT2 직전의 파일 해시를 비교한다. 두 시점 해시 확인은 임의의 동시 쓰기를 잠그는 기능이 아니다.

docs/reviews/p1_rt_runner_preparation_20261117/rt_binding.py는 위 세 키의 중복·형식, 로그의 치환된 `read_restart`, 글자 일치와 양쪽 실제 경로, 파일 실제 SHA256을 읽기 전용으로 대조한다. 기록 모순은 누락보다 먼저 SYNTAX_FAIL, 모순 없이 증거만 빠지면 UNCONFIRMED다. PASS는 **결속 일치만** 뜻하며 RT 기술·reset·수치·문법 자격이나 RESTORED 판정이 아니다. 기존 증서·영수증을 쓰지 않는다. fixture는 같은 함수의 `log.liggghts`·`ckpt.txt` 경로를 쓴다.

## 2. 복사본과 실행 경계

원 키트 docs/data/ps45_unload_20261009/의 94파일은 그대로다. 앞 덱 층 13추가와 그 목록, 이번 새 러너·결속 판독기·목록을 합친 복사본은 111파일이다. 원 `run_unload.sh`와 원 SHA256SUMS를 교체하지 않는다. 옛 목록은 역사 입력만 가리킨다.

새 후보 `run_unload_rt_dev.sh`는 시작 즉시 RT_RUNNER_LAYER_ONLY를 표시하고 rc2로 끝난다. 아직 구 판독기를 통해 실행하거나 증서를 발행할 수 있는 키트가 아니다. 모의 시험은 이 후보에서 실제 RJ/RJ2 분기와 RT 함수를 추출해 가짜 단계로 실행한다. 완성 진입점의 rc2와 셸 문법도 따로 확인한다. 엔진·MPI·현장·원 연구 값은 호출/열람하지 않았다. 이는 남은 구현 연결을 구분한 것이며 개발 계산에 새 등록·반박 관문을 추가한 것이 아니다.

## 3. 시험과 보존

| 시험 단위 | 연결 전, 같은 최종 시험 | 연결 뒤 | 의미 |
|---|---|---|---|
| RT 순서 12메서드 | rc1 · 실패19관측 · 오류0 | rc0 · 12/12 | 정상 순서, 기술 실패/표지 결손, 해시 실패/변경, UK 차단, 원 단계 함수 보존 |
| 결속 20메서드 | rc1 · 실패36관측 · 오류0 · 건너뜀1 | rc0 · 통과19 · 건너뜀1 | 중복·형식·누락 우선순위, 다른 시도·이름 변경, 실제 해시·로그/fixture 결속 |
| 앞 RT 덱 12메서드 | 앞 묶음 기록 그대로 | rc0 · 12/12 | 덱·표 생성 회귀 |
| 새 복사본 바이트 | — | 원94/94 동일 · 추가13/13 동일 | 원 봉인·러너·판독기 보존; 운영 재봉인 아님 |

전후의 `before/` 두 파일은 **미구현 연결을 표현하는 시험 어댑터**다. 빈 모듈에는 결속 API가 없고, 러너 어댑터는 역사 러너 바이트를 그대로 돌려준다. 옛 운영 코드에 이번 결함이 있었다는 반례로 세지 않는다. 실패 관측에는 subtest가 있어 메서드 수와 더하지 않는다. Windows Python 3.12.14·Git Bash에서 확인했다. 실제 디렉터리 링크 시험 하나는 이 환경의 링크 생성 권한 부재로 건너뛰었으며 POSIX/Lustre 자격을 주장하지 않는다.

준비 중 오류도 보존했다. 초기 제한 환경은 Bash 시작을 거부했고, 기본 임시 경로의 `#`는 합성 로그의 주석으로 읽혔다. 해시 모의 함수는 `--`를 파일 인자로 오인해 수정했다. Windows 셸 종료 직후 임시 폴더 정리 충돌 및 절대경로 전달 차이는 정리만 짧게 재시도하고 전체 진입점/문법 검사를 표준입력으로 전달하도록 바꿨다. 시험 실행·assertion 재시도는 없다. 최종 동일 시험으로 전후를 재확인했으며 앞 준비 실패를 후보 통과로 세지 않는다.

docs/reviews/p1_rt_runner_preparation_20261117/verification.json에 원 로그 해시·수·소스 해시와 보존 확인을 적었다. 같은 폴더 `evidence/`에는 경로를 자리표로 치환하고 LF 및 줄끝 공백을 정규화한 로그가 있다. 원 출력은 리포 밖에 보존한다.

## 4. 다음 구현 (A1 전체 완결 아님)

| 순서 | 남은 것 | 다음 확인 |
|---|---|---|
| 1 | 30열 G2cp·정확 ID·연속 전역/칸별 관문 | §15-5/15-5b의 정상·작은 반례, 최소 쌍100·위반 우선순위 보존 |
| 2 | 전체 RT 기술/reset/표지·목록 검사와 결속 판독 연결 | 이번 PASS를 전체 RESTORED로 쓰지 않음; 모의 표지 검사만으로 reset/step/NP를 인증하지 않음 |
| 3 | 최초 증서 발행과 다시 읽기 분리 | §15-5c의 배타적 완성본 발행·기존 파일/링크 거부·다시 읽기 무변경; 이번 후보의 `--publish-new`는 연결 예정 인자 |
| 4 | 작은 RT fixture 20검사·함수/상수 닫힘·사전 점검 | §15-4b·R43; 이번 결속 20메서드와 fixture 20검사는 다른 단위 |
| 5 | 완성 복사본의 봉인 전 확인 → NP6 fixture·7:3 사전 셈 블록 | 1저자 실행; 원 RJ323957 재실행·기존 B N40000 반복 없음 |

위 연결이 끝나기 전에는 이 후보를 현장 실행 블록으로 내지 않는다. B 소비자·실패 경로의 알려진 한계는 그대로 적되 A 구현을 막는 조건으로 올리지 않는다.

## 5. 재현

리포 루트에서 다음 소형 시험을 실행한다. `RT_TEST_TMPDIR`는 공백·`#` 없는 쓰기 가능한 별도 임시 부모를 지정하고, `RT_BASH`는 로컬 Bash 실행 파일을 지정할 수 있다. 현장 명령 블록이 아니다.

```text
python -I -X utf8 -B docs/reviews/p1_rt_runner_preparation_20261117/test_rt_binding.py
python -I -X utf8 -B docs/reviews/p1_rt_runner_preparation_20261117/test_rt_runner.py
python -I -X utf8 -B docs/reviews/p1_rt_deck_preparation_20261116/test_rt_decks.py
```

전후 대조는 `RT_BINDING_SOURCE=docs/reviews/p1_rt_runner_preparation_20261117/before/binding_unimplemented.py`, `RT_RUNNER_SOURCE=docs/reviews/p1_rt_runner_preparation_20261117/before/runner_unchanged.py`를 각각 해당 시험에만 지정한다. 모듈 경로는 리포 루트 기준이며 전후 시험 파일은 같다. 새 복사본은 생성기에 `--source docs/data/ps45_unload_20261009 --output <존재하지 않는 별도 폴더>`를 주면 된다. 기존 대상 거부는 앞 덱 층 생성기의 계약을 따른다.
