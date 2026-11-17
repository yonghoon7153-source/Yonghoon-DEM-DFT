# A2: RT 소비자 · 증서 · fixture 판독 준비 — 2026-11-17

## 1. 범위

바탕 = 5d8e628ab80b66cbfddf8a8d7404dad2da1282d7, 같은 codex/dem-rt-numeric-1117 가지.
정본 = docs/reviews/dem_unloading_ps45_prereg_20261009.md §15-4b · §15-5 · §15-5b–d.
앞 층 = docs/reviews/p1_rt_numeric_preparation_20261117/README.md.

이번 완료: RT 기술/reset/목록을 앞 수치 관문에 연결, 읽기 전용 복원 어댑터와 배타 발행 구현, 닫힌 소스의 독립 fixture 판독기 20검사 및 원자료 재판독 사전 대조 구현.
모든 확인은 합성 입력·새 복사본이다. 현장 실행0·실제 값 열람0·운영 재봉인0·실행 GO 없음.

## 2. 연결

| 새 파일 (모두 docs/reviews/p1_rt_consumer_preparation_20261117/ 아래) | 하는 일 | 유지하는 경계 |
|---|---|---|
| rt_contract.py | R·UN·해당 Ut0·RT1·RT2 기술, R·RT1·RT2 reset, post 접두별 정확 목록, 원자 보고, G2cp·ⓡ·ⓣ 처분 | 기술/결합 모순이면 RT 수치·원자 읽기 생략; 부족한 결합/목록으로 왕복 PASS를 만들지 않음 |
| rt_restore.py | 원 ul_reader.restore_verdict의 나머지 검사와 새 RT 결과 조립; 기본 stdout만 | 옛 G2c는 G2c_cont 보고로만; G0/G1/G2/mesh/G3/PRE=POST/UN/이력 자격 보존 |
| rt_publish.py | 완성 JSON 임시 파일 쓰기·fsync 후 같은 폴더 hard-link 배타 공개 | 목적지 선점·동시 발행·부분 쓰기/오류는 성공 rc 금지; overwrite/replace 없음 |
| rt_grammar_core.py | 등록된 fixture 20검사, 생산자 끝 전단 이력 대조 | deltaMax는 생산자 이력 값 대조 밖; 20개 Boolean이 모두 True일 때만 PASS |
| rt_fixture_prereq.py | 후보 신원·동일 바이너리·단계 덱/STL·저장 판정·검증한 판독기의 원자료 재판독 | JSON의 PASS만으로 수용하지 않음; operational_go=False |
| prepare_consumer.py | 앞 복사 층에 위 파일과 독립 판독기/계약/후보 해시표 추가 | 원94·앞113파일 불변; 새 복사122파일; 러너 즉시rc2 유지 |

기술 실패/결합 모순 → SYNTAX_FAIL, 확인된 값·reset/G0 위반 → VALUE_MISMATCH, 남은 결손 → UNCONFIRMED, 그 밖의 계약 충족 → RESTORED. 마지막 이름은 이 판독 계약의 결과이며 물리 자격/실행 승인과 다르다.

쓴 S0 원천 선택은 RJ의 in 원 로그, 10:0 RJ2의 EXT 또는 EXT2 중 해당 고정 S0 하나다. 두 화면을 이어 붙이거나 먼저 발견한 덤프로 대체하지 않는다. 기존 G3 등 역사 검사 자체는 원 함수 그대로이며 새 선택은 연속성 관문에 적용한다.
원자 기본12열과 바닥 이력4열의 비트 대조는 별도 보고. 새로운 원자 수치 판정선은 추가하지 않았다.

## 3. 발행 · 다시 읽기

준비 복사본의 rt_restore.py 기본 호출은 stdout뿐이며 파일·증서·영수증을 쓰지 않는다. 명시적 --publish-new만 이번 판독의 완성 JSON을 restore_verdict.json으로 한 번 공개한다. 후보 CLI는 기존 증서를 재판독 결과로 덮지 않는다. publication 오류는 rc3, 미복원 결과는 rc2, RESTORED 판독은 rc0이다.

공개 직후 완료 응답에서 실패하면 완성 증서가 남을 수 있다. 이 경우에도 rc0을 주지 않고 그 파일을 지우거나 자동 재발행하지 않는다. 다음 관문은 rev5 표지·해당 침대/잡·기존 완료 영수증과 두 문법 사전 점검 PASS 단일 기록을 함께 요구한다. 모순/중복 사전 점검 기록은 거부한다.
로컬 Windows와 Linux의 동시 두 발행은 한 개만 성공했다. 해당 확인은 실제 현장 파일시스템의 전원 장애 내구성이나 모든 OS 자격이 아니다.

## 4. fixture 소스 닫힘과 사전 대조

생성 read_rt_grammar.py에는 앞 rt_numeric.py/rt_binding.py 전체 바이트, 이번 공통 계약, 원 read_history.py의 _num/read_dump/_close/local_map 함수 원문과 필요한 표준 모듈을 포함한다. Python -I로 그 파일 하나를 별도 폴더에서 실행해도 리포 모듈을 import하지 않는다. 함수 코드뿐 아니라 숫자·상수·정규식의 소속 바이트 해시를 기록한다.
history_params.json의 허용폭·reset 표·pair 열과 fixture step/입자 수를 복사·대조한다. 역사 판독 함수는 수정하지 않았으며, 그 함수의 float 변환 전에 ID 원 토큰의 정확 정수성과 ASCII 유한 숫자 꼴을 검사한다. bind_sha/bind_path 두 검사는 같은 엄격한 결합 검사 결과를 함께 요구한다.

RT_CANDIDATE_SHA256SUMS 및 RT_FIXTURE_CANDIDATE_IDENTITIES.json은 후보 바이트 목록이다. 기존 운영 SHA256SUMS·봉인 상수를 갱신하지 않는다.
사전 대조는 mode=rt_grammar·end·kit·sums_sha256·lmp_sha256의 유일한 기록, 후보 파일6개의 기대 해시, P/RT1/RT2의 rc/deck/STL 사본, 판정 파일과 run_dir의 실제 경로, 20검사 및 같은 원자료의 재판독을 요구한다. 검증한 판독기 바이트를 그대로 실행해 나중에 다른 파일을 import하지 않는다. 정상 심볼릭 런 별칭도 확인했다. 실제 운영 승인을 의미하지 않는다.

## 5. 시험과 확인

| 묶음 | 최종 Windows / 로컬 Linux | 앞 실패 확인 |
|---|---|---|
| 기술/reset/목록/처분 | 20/20 · 20/20 | 첫18 미구현 실패18; 추가 읽기 생략/미확정2는 수정 전 실패2 |
| 배타 발행 | 8/8 · 8/8 | 첫6 미구현 실패6; fd 소유권 반례는 수정 전 오류1; 뒤 추가 실패 응답 사례 포함 |
| fixture 20검사 | 9/9 · 9/9 | 준비기 미구현 실패9; 숫자 토큰 0_1 반례 수정 전 실패1 |
| 후보 신원/재판독 | 8/8 · 8/8 | 후보 신원 목록 미배송 상태 실패8 |
| 실제 legacy 연결/CLI/관문 | 7/7 · 7/7 | 모순·중복 사전 점검 반례 수정 전 실패1; 원천 선택 실패의 우선순위/기록 보존 1방법6관측 실패6 |

20개 fixture 검사는 별도 고유 unittest 20개가 아니다. 한 시험의 각 음성 관측·환경 반복과 방법 수를 합산하지 않는다. 실제 legacy 판독기의 작은 합성 RJ 사례는 왕복 PASS여도 칸 N<100 때문에 UNCONFIRMED로 남았다.
Windows 기본 격리 임시 경로의 # 문자 때문에 초기 결합 fixture가 실패했고, 임시 출력 위치를 지정한 동일 코드에서 확인했다. 제한 환경의 hard-link 거부는 별도 로컬 시험 권한으로 확인했다. 역사 함수의 unclosed-file ResourceWarning 및 최초 합성 원 로그 G3 행 누락도 기록했다. 원천 선택 회귀의 임시 폴더 누락 오류1과 최초 assertion의 KeyError2도 고쳐 동일 expected-correct 시험의 실패6→7/7을 확인했다. 이를 현장 실패나 연구 결과로 세지 않는다.

원천을 하나로 고를 수 없어도 앞서 확인한 기술/값 실패를 UNCONFIRMED로 낮추지 않는다. 기존 검사 기록은 남기고, 판정에서 제외된 옛 G2c만 G2c_cont 보고로 옮긴다. Linux 문서 참조 검사: 깨진 경로0·커밋0. 전체 게이트는 실행하지 않았다.

리포 루트에서 각 시험:

    python -I -X utf8 -B docs/reviews/p1_rt_consumer_preparation_20261117/test_rt_contract.py
    python -I -X utf8 -B docs/reviews/p1_rt_consumer_preparation_20261117/test_rt_publish.py
    python -I -X utf8 -B docs/reviews/p1_rt_consumer_preparation_20261117/test_rt_fixture.py
    python -I -X utf8 -B docs/reviews/p1_rt_consumer_preparation_20261117/test_rt_prereq.py
    python -I -X utf8 -B docs/reviews/p1_rt_consumer_preparation_20261117/test_rt_restore.py

Windows에서 RT_TEST_TMPDIR은 공백/# 없는 새 합성 임시 폴더로 지정한다. 실제 호스트·엔진·MPI·원자료가 필요 없다.

## 6. 남은 것

- run_history의 새 RT fixture 흐름/복사 목록과 준비 러너의 새 소비자·사전 점검 호출을 연결하는 마지막 조립이 남는다. 기존 실행 진입의 즉시 중단은 아직 해제하지 않는다.
- 별도 사전 점검 호출과 모의 러너 흐름을 확인한 뒤 완성 키트 봉인 직전 독립 반박 1회. 운영 봉인·현장 fixture/7:3 사전 셈·새 RJ는 그 뒤 1저자 권한이다.
- CPU/메모리·실제 POSIX/Lustre 원자성·현장 grammar 실행·물리 자격을 이번 합성 확인으로 닫지 않는다. 기존 Rint·B N40000·RJ323957·50kg 응력에는 변경 없다.
