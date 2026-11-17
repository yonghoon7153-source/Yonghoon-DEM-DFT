# RT fixture 러너·사전 점검 조립 — 2026-11-17

## 1. 바탕과 지위

바탕 845fa26721de8827b8f572a7beaf7a61c4b1cd42, 새 가지 codex/dem-rt-fixture-runner-1117.
반입 ⑩의 수치/소비자 층 위에 새 파일만 더한다. 정본은 docs/reviews/dem_unloading_ps45_prereg_20261009.md §15-2·15-4b·15-5b–d; 이전 구현은 docs/reviews/p1_rt_consumer_preparation_20261117/README.md.

**비활성 조립 후보**다. 두 새 실행 진입점 모두 즉시 RT_ASSEMBLY_INACTIVE / rc2. 시험은 별도 합성 복사본에서만 이 문장을 제거하고 가짜 실행 파일을 지정했다. 원 키트·앞 준비본·운영 봉인·현장 실행·실제 값 열람·GO 변경0.

## 2. 연결

| 항목 | 이번 연결 | 확인 |
|---|---|---|
| fixture 순서 | 새 run_history_rt_candidate.sh의 --rt-grammar-only = P → RT1 → RT2 | 앞 단계 rc0와 필요한 파일 동시 요구; RT1 완료 표지·파일 해시 두 번 확인 |
| fixture 복사 | 앞 history 파일과 새 덱·판독기·계약을 별도 kit에 복사 | 이전 SHA256SUMS 그대로; 후보 history 목록을 추가; ul_gates/ul_lib import 없음 |
| 판독 | 단독 실행 read_rt_grammar.py로 20검사 → 새 JSON | 실패·불완전은 rc0 아님; 새 run 폴더/판정 파일, 기존 경로 덮어쓰기 없음 |
| 반환 | 새 run 폴더 바깥에 report.tgz, SHA256 출력 | tar 실패/기존 반환 경로도 비정상 종료; 실제 대용량 결과가 아님 |
| RJ/RJ2 사전 점검 | 기존 grammar_check 뒤 rt_grammar + orig_grid | 둘 다 통과하고 판정 파일 hash를 읽은 뒤에만 rt_grammar_prereq=PASS; 잡 폴더 생성 앞 |
| 쓴 격자 | RJ 원 로그+마지막 덱; RJ2 선택된 EXT 또는 EXT2 화면 하나 | 축별 grid/NP, balance 금지; 덤프 없이 로그·덱의 격자 기록만 판정 |
| 복원·다음 관문 | 새 rt_dispatch.py가 rev5 restore와 증서 소비 연결 | 기본 재판독 stdout, 런 최초 --publish-new 유지; 다음 관문은 새 증서+완료 영수증+두 grammar |
| 나머지 | 원 run_deck·EXT 이후 팔 분기·보조 부모 목록 명령 보존 | 광범위 dispatch 치환을 보존 시험이 잡아 필요한 두 호출로 좁힘 |

후보의 기존 문법 검사·inputs·parentsums 호출은 원 ul_reader.py를 그대로 사용한다. 새 dispatch의 나머지 명령은 원 함수를 부르고, _job_restored만 rev5 소비자로 연결한다. 공유 원 코드 파일을 수정한 것은 아니다.

## 3. 파일과 무결성

이번 원고/구현 자리 = docs/reviews/p1_rt_fixture_runner_preparation_20261117/.
prepare_assembly.py는 기존 prepare_consumer를 호출한 뒤 새 이름의 러너 둘·dispatch·후보 목록/메타만 추가한다.

- 원94파일·앞 준비본122파일 바이트 보존. 새 복사본128파일.
- RT_HISTORY_SNAPSHOT_SHA256SUMS: history 후보23파일.
- RT_ASSEMBLY_SHA256SUMS: 자기 목록을 제외한127파일.
- RT_CANDIDATE_SHA256SUMS: 앞 fixture 입력/판독기6파일 그대로.
- 이 목록들은 후보 복사 신원이다. 역사 SHA256SUMS를 바꾸거나 운영 봉인을 발행하지 않았다.
- stage의 NP/LMP/MPIRUN 전달 및 run_deck 원문은 보존했다. 실제 MPI/엔진은 이번에 실행하지 않았다.

## 4. 시험

| 단계 | 결과 | 구분 |
|---|---|---|
| 미구현 연결, 첫12메서드 | 실패12·오류0 | 후보 파일이 아직 없는 부모 빌더 사본; 역사 키트의 새 결함이라고 세지 않음 |
| 첫 구현, 같은12 | Linux 실패1·오류0 | 무관한 parentsums까지 새 dispatch로 돌린 변경을 보존 시험이 검출 |
| 해시 읽기 실패 회귀 | 1메서드·실패1 → 통과 | 빈 해시인데 PASS 기록 가능하던 후보 중간본을 거부하도록 수정 |
| 최종14, Linux Python3.12.3 | 14/14·실패0·오류0 | 복사→재실행→가짜 P/RT1/RT2→실제 판독기→실제 사전 대조 포함 |
| 최종14, Windows Python3.12.14/Git Bash | 9통과·5건너뜀·실패0·오류0 | 전체 mock fixture5메서드는 Linux에서만; Windows 현장 자격 아님 |

합성 fixture의 정상/심볼릭 뿌리 둘 다 20검사 PASS를 원자료에서 다시 확인했다. 생산자/RT1이 파일을 쓴 뒤 실패해도 다음 단계 없음, RT1 파일/표지/step 오류면 RT2 없음, RT2 실패/잘못된 덤프는 성공 아님을 확인했다. 방법·subtest·20 내부 검사·OS 반복은 합산하지 않는다.

이전 history 판독 함수의 ResourceWarning(unclosed file)은 그대로다. 원 함수 변경 없이 같은 소형 합성 자료를 읽는다. 최초 Windows 건너뜀10은 subtest별 표시였고, 최종에는 메서드 단위5로 표지를 옮겼다(Windows에서 실행한 범위를 늘렸다는 뜻 아님).

리포 루트에서 재현:

    python -I -X utf8 -B docs/reviews/p1_rt_fixture_runner_preparation_20261117/test_rt_assembly.py

RT_TEST_TMPDIR은 쓰기 가능한 합성 임시 부모, RT_BASH는 로컬 Bash다. 엔진/MPI/현장/네트워크가 필요 없다. 원 로그는 리포 밖, 해시·수는 docs/reviews/p1_rt_fixture_runner_preparation_20261117/validation.json.

문서 참조 검사: 깨진 경로0·커밋0. 원장 자기일관 검사: rc0(원장 무변경). 전체 게이트는 실행하지 않았다.

## 5. 남은 확인

- 완성 키트 봉인 직전 한 번의 독립 반박. 이번 것은 작성 측 합성 연결 확인이며 판정/verified 승격이 아니다.
- 실제 NP6 문법 fixture, 7:3 읽기 전용 사전 셈, 파일시스템/바이너리 자격, 운영 신원 고정 및 1저자 GO는 별도.
- 두 비활성 진입점을 현장 블록으로 전달하지 않는다. 실행 잠금 해제와 운영 봉인 준비는 다음 고정 후보에서 검토한다.
- Rint 고정 가지, 원 키트·앞 층, 공유 원장/CLAUDE/진행 기록/check_all 변경0.
