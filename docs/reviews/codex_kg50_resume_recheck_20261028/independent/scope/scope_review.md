# KG50 재개 재검토 — 증거 경계와 Q6–Q8 독립 검토

핀 `f118c1fd1e3eb1a558299663dcee6a0bf83b9942`. 리포/생산 코드 변경·LIGGGHTS·MPI·WSL·SLURM 실행 없음. 코드·문서·제공 보고 2건 읽기와 합성 산술만 수행.

## 가장 중요한 구분

기존 KG50-02의 최소 처방은 실패한 trial의 본 제출 승격을 막는 G0/구간 결손 처리였다. prior `docs/reviews/codex_kg50_decks_review_20261026/codex_review_kg50_decks_20261026.md:81`과 추가 한계 `:83`은 서로 구분해야 한다. G0 수정의 합성 재현이 맞으면 그 좁은 결함은 닫을 수 있다. 다만 `state identity`, 실제 설치판 동일성, 새 after_settling 경로의 실물 호환성까지 닫힌 것으로 쓰면 안 된다.

## 증거가 직접 말하는 것

- `docs/data/kg50_resume_tests_20261027/resume_r4_1027_2110.md:1–2`: 보고 머리 두 줄뿐. 179999 거부는 이 파일에서 독립 재계산 불가. README의 저자 전달을 별도 지위로 둔다.
- `docs/data/kg50_resume_tests_20261027/resume_r4_1027_2230.md:9–12`: +1 step 보정·정적 PASS·job 327010·G0 COMPLETED/0:0/final 22001 보고. 실제 원본 trial 로그와 sacct 원문은 없음.
- 같은 파일 `:14–19`: Atoms=22353, KE(S0=20001)=2.3980032, KE(21000)=2.5527533 양쪽 동일이라는 보고. 원자 상태 덤프는 없고 G2는 KE 대체이며 `:20`은 -T 시험만.
- README `:11`은 plan/fixrun/deckcheck/nohup 원본 미수령을 명시. `:14`는 최신 e59c43e6 도구의 실측이 아님을 명시. 이 자료를 최신 pinned implementation의 실제 실행 증거로 전용하면 안 됨.
- 합성 45장면 바이트 동일은 해당 fixture 입력의 회귀 보존이다. 외부 dem_restart.py의 모든 실 출력, 실행 노드 바이너리/라이브 파일/NP 호환성을 일반적으로 증명하지 않음.

## Q6 — 수정안: 상태 비교는 추가하되, 원 런 복원 증명과 분리

1. KE와 입자 수는 상태를 결정하지 못한다. 독립 산술 `probe_state_observability.py`는 N=2, KE=1.000000 J가 완전히 같은데 위치·속도 방향·type·radius가 다른 두 상태를 만든다. 이는 실제 KG50 오류가 아니라 식별 불가능성 반례이다.
2. `scripts/resume_ckpt.sh:751`의 settling KE 대체를 `G2 상태 덤프 PASS`로 쓰는 것은 이름과 증거가 다르다. `:774`의 문구는 `ATOM_STATE_NOT_VERIFIED; KE surrogate matched`처럼 분리하는 편이 맞다. 이 한계는 요청서에서 이미 공개했으므로 새 P1 발견으로 포장하지 않는다.
3. 요청서 `:148`의 'G3가 21000·22000을 본다'는 수치 전수 대조가 아니다. 코드 `:754–760`은 모든 정규 step의 존재를 확인하고, **최초 F2 한 줄만** sane(Atoms/압력 또는 KE 5%)로 대조한다. 따라서 22000의 동일 수치까지 근거로 들 수 없다.
4. 같은 checkpoint를 별도 최소 reader로 `read_restart→dump→run 0`한 기준 상태와 trial의 S0 상태를 비교하는 안은 유용하다. 다만 둘 다 같은 파일·같은 reader 계열이므로 **재개 덱이 읽어낸 가시 상태를 바꾸지 않았음**을 시험할 뿐, checkpoint 쓰기 전 원 런의 상태·숨은 이력이 온전히 저장됐음을 독립 입증하지 못한다.
5. 기준/시험은 동일한 관측 시점과 좌표/단위·float 출력 정밀도를 고정하고 ID 집합·중복·step·type·radius·mass 또는 density·x/y/z·vx/vy/vz·omega를 필수로 검사할 것. 현 sel(:646)은 omega/mass를 포함하지 않는다. 파일 SHA만 비교하면 MPI 행 순서·포맷 변화에 오탐이 생기므로 ID 정렬한 필수 필드와 등록 허용치를 비교한다. 두 파일의 원본 SHA는 별도 보존한다.
6. 판 높이/mesh·접촉 이력·활성 fix 복원은 별도 범위다. after_settling의 PLATE HEIGHT 한 줄 일치(:738–740)는 전체 원자 상태 증명이 아니다. 특히 접촉 이력의 보존을 주장하려면 지정 바이너리의 연속/중단-재개 자격 시험 또는 관련 이력 원자료가 필요하다. 이번 재검토에서 이를 수행하지 않음.

## Q7 — 동의: 설치판 신원 연결이 필요

현재 `:673`의 external dem_restart.py 호출, `:699`의 runner 문자열 검사, `:710/:779`의 제출은 실제 실행 프로그램 hash와 pin을 연결하지 않는다. `:650–651`, `:762–775` 보고도 경로/명령/결과만 쓰고 도구·helper·checkpoint·실행 바이너리 SHA를 남기지 않는다. 요청서 `:28`은 이미 도구 사본이 구판으로 돌아간 사실을 고지한다. 그러므로 '보고 줄 모양이 특정 판에만 있다'는 버전 추론은 실제 runtime SHA의 대체가 아니다.

최소안: 제출 전 review pin↔wrapper SHA 일치, 실제 helper SHA 별도 승인/봉인, 원 덱·생성 본 덱·trial 덱·runner·checkpoint SHA와 NP, trial/main job ID를 한 영수증으로 연결. helper는 repo 밖이므로 'repo hash가 없다'를 새 사실처럼 보지 말고 실제 소스를 확보·독립 식별해 기대 digest를 정한다. 실행 노드에서 실제 resolve된 lmp_mpi 경로/hash(가능하면 MPI/build)도 기록. 미상 또는 기대값 불일치면 trial/main 승격 금지. trial 검증 뒤 main이 읽는 입력이 바뀌지 않았음을 재검사하거나 검증된 불변 사본을 제출한다. SHA가 같아도 물리 자격을 의미하지는 않는다.

등급을 붙이면 P2 운영 provenance의 알려진 미해제: 검토한 코드와 실제 main job이 같은 도구라는 결론이 아직 입증되지 않음. 코드 수치 결함으로 확대하지 않는다.

## Q8 — 본 제출의 무조건 GO는 아님

- 실제 구판 -T 보고 한 건과 합성 회귀 보존만으로 최신 e59c43e6 + 외부 helper + 각각 NP4/NP56의 실제 경로를 모두 수용할 수는 없다. 수정/핀 일치 뒤 해당 경로·해당 NP·실제 checkpoint의 -T를 먼저 수행하고 원본 로그·생성 덱·정적 기록·완료 증거·manifest를 보존하는 것이 최소 실행 전 순서다.
- after_settling은 실제 helper의 산출조차 이 패키지에 없다(요청서 :27, 절차 :367). 새 정적 검사 양성/음성 합성시험을 통한 코드 수정 수용과 실제 -T 요구를 분리하라. 실제 -T 한 건이 먼저다. NP4 settling 성공을 NP56 after_settling 성공으로 옮기지 않는다.
- D0.7 안정화/압축의 dt·감쇠 자격은 Q5 별건이다. 이 resume tool 리뷰가 KG50-04를 닫지 않는다. D1 대기, D2 진행 허용이라는 저자 결정 역시 수치 정확성 인증과 구분한다. 이미 실행 중이라고 저자가 보고한 job을 이 리뷰에서 임의 중단/재실행하지 않는다.

## 새 문서 충돌 — P3 제안

`docs/reviews/codex_kg50_resume_tool_recheck_request_20261027.md:29` 및 :111은 '실제 본 제출 아직 없음/성공 -T 한 건'이라고 한다. 하지만 같은 핀 `docs/data/kg50_resume_tests_20261027/README.md:15`에는 10-28 09:42 test328597→main328599(NP4 RUNNING) 저자 보고를 추가했다. 원 보고 resume_r4_1028_0942.md는 미수령이고 화면만 근거다.

최소 해결: 요청서에 '10-27 -T 보고 원본 수령; 10-28 main 제출은 저자 화면 보고, 원본 미수령; 최신 e59판 실 실행은 미확인'으로 시간·증거 지위를 맞춘다. main이 실제 실행됐다고 독립 확인했다고 쓰거나, 아직 한 번도 제출하지 않았다고 단정하는 둘 다 피한다. 이 충돌은 실제 solver 실패를 입증하지 않는다.

## per-KG 상태 제안 (나머지 에이전트 실제 탐침과 통합할 것)

- KG50-02: G0와 원 로그 구간 결손 수정에 한정한 닫힘 여부는 scheduler 탐침으로 판정. KE 대체→state hash 추가 한계는 계속 부분/열림. 둘을 한 단어로 뭉개지 말 것.
- KG50-16/17: 합성 및 공개 생성 덱의 안전성은 코드 탐침으로 닫을 수 있음. 실제 external generator 일반 호환성·runtime version 인증은 별도 미검토/부분. 22:30 보고를 원본 로그를 직접 재계산한 것으로 쓰지 말 것.
- KG50-18/19: 합성 fix 자체 닫힘과 실물 after_settling/compress 생산 진입은 분리. 해당 실물 통합 시험은 아직 필요. 단지 '실물이 없다'만으로 모든 단위 수준 수정의 닫힘을 부정할 필요는 없음.

재현: `python -B independent/scope/probe_state_observability.py`; 결과 `state_observability.json`. 순수 합성 산술이며 실제 LIGGGHTS/SLURM 실행 증거가 아님.
