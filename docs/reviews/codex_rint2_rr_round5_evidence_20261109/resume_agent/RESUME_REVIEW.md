# Rint② 회차 ⑤ — 재개 경로 독립 검토 메모

대상 핀 `abf0911ebc994167ac50132c78207c6c8d4421f1`. 범위 Q1–Q4/Q6, PC14-02·03 및 PC15-01–06의 재개 논리. 요청서 `docs/reviews/codex_rint2_rr_round5_request_20261109.md` 50–87, 129–139행. 생산 소스와 원장·패키지는 수정하지 않았다. 아래 줄은 이 핀 `scripts/rint_r_chain.py` 기준이다.

## 1. 판정

원 PC14-02/03 반례와 PC15-01–05의 지정 실패형은 고친 경로에서 막힌다. 기존 정직 2·3시도, 부분 재실행, 첫 재실행 전 종료, 원천이 해당 런을 아직 시작하지 않은 경우를 유지한다. PC15-06은 집중 행과 소스 연결을 확인했으나 71개 전체 변이를 이 검토에서 다시 돌리지 않았으므로 그 전수 수치는 주 검토의 별도 회계와 합쳐 판정해야 한다.

**Q6의 전칭 문장은 그대로 수용할 수 없다.** (a) 확인된 모순에는 `resume_ok=false`인 결과 줄을 남긴다. 결과 줄 자체가 없는 것은 `[원천]` 미확인 등 별도 경로다. (b) 요약 없는 재개에서 이미 복사한 선행 런의 원천 동일성 대조는 건너뛴다. 이 명시적 한정을 독립 반례로 재현했다. 이 반례는 실제 하드웨어 고장 재현이나 일반 정상 중단만으로 잘못된 결과가 생긴다는 증명이 아니다. 따라서 이를 숨은 새 P1/P2로 주장하지 않으며, 전체 재개 정책의 무제한 인증과 구별한다.

| 항목 | 지정 수정 판정 | 실제 재현 / 코드 |
|---|---|---|
| PC14-02 | 닫힘 — 원 R1·R2 및 요약 있는 복사/새 런 경계 | R1·R2 모두 쓰기 자격 false, 다음 차례·풀기 전 `RESUME_NOT_ALLOWED`, 공통 사유 `[ⓒ]`. 4601–4673, 4756. 요약 없는 copied prefix의 추가 한정은 §4 |
| PC14-03 | 닫힘 — 원 attempt-null·3시도 from 재결속 | `[ⓐ]` 및 `[ⓑ]`, 세 자리 거부. 4552–4591, 4710–4764, 5222–5230 |
| PC15-01 | 닫힘 — 디스크상 첫 미완료 런 | summaryless mismatch·정직 signal_after mismatch 자격 false `[ⓓ]`; 같은 bytes·rc1 부분 런·아직 폴더 없음은 유지. 4528–4549, 4676–4707 |
| PC15-02 | 닫힘 — 명시된 새 런 이름/outdir/완료 결속 | outdir 가짜 별칭·first rerun 기록 생략 거부. 원천에 해당 시작 기록이 없는 정직 새 런은 허용. 4502–4518, 4618–4663 |
| PC15-03 | 닫힘 — 원천 위치 미확인과 영구 false 기록 분리 | 원천 옮김→`ResultHeld`/결과 없음; 원상 복원→자격 true. 5004–5030. CLI 실제 호스트·잠금은 이번 독립 자격 아님 |
| PC15-04 | 닫힘 — bool/float 별칭 | summaryless `resume_of=true`, `1.0` 모두 `[ⓐ]` 거부. 5227 |
| PC15-05 | 닫힘 — 지정 shape 회귀 | runs=5, stop='invalid' → 두 다음 재개 경로 모두 `RESUME_NOT_ALLOWED [꼴]`, traceback 없음. 4735–4738, 4914–4933 |
| PC15-06 | 부분 검증 메모 | 분리 가드의 양·음성 API 결과 및 소비자 배선 확인. 전체 71변이 재계수는 주 검토와 결합할 사항. 시험 `RR5F`, 원장 재계산 세 위치 연결은 실재 |

RR4-01(M56 회계)은 주 검토 담당 범위이며 이 메모가 중복 판정하지 않는다.

## 2. 소비자 배선과 기대 변경

- 결과 줄: `attempt_close` 5158–5177 및 `recover_ledger` 8342–8426 → `attempt_result` 5016 → `result_fields_ledger` 4974 → `resume_provenance_problem` 4710.
- 다시 셈: `_result_recount` 5113–5130 → 같은 `result_fields_ledger`; `result_line_problem` 5144–5155는 실제 기록과 다시 셈을 비교한다. 모순 결과를 false로 적었으면 다시 셈도 false여야 하므로 그 자체는 mismatch가 아니다.
- 다음 재개: `attempt_order_problem` 3556–3588 → `resume_chain_provenance_problem` 4767–4787; 풀기 전 `resume_chain_problem` 3793–3822도 같은 검증을 부른다.
- `result_fields`/`attempt_result_line`의 원장 없는 API는 의도적으로 예전 폴더 증거 값이다. 이 값을 공용 쓰기 경로의 최종 자격으로 읽으면 안 된다. 원 R1/R2는 원장 없는 값은 true지만 새 실제 쓰기 및 다음 재개는 false/거부다.
- Q3 기대 변경은 수용 가능: cause는 관측된 resource/timeout/signal 등의 원인이고 resume eligibility는 별도 변수다. 모순 때문에 cause를 거짓으로 다시 쓰지 않고 자격만 false로 만드는 것은 정합적이다.
- `[원천]`은 알려진 모순과 달리 미확인이다. 옮겼다가 되돌리면 다시 처리할 수 있으므로 false 결과를 영구 고정하지 않는 변경도 정합적이다.
- pa13_ledger machine 고정물 수정은 attempt.json과 원장 항목이 같은 생산자 값을 써야 한다는 새 검사에 맞추는 것이다. 새 가드 자체를 우회하는 `attempt_entry_diff` 대체가 아니다.
- PC15-05의 멈춤 이름은 `ATTEMPT_LEDGER_MISMATCH`/무검사에서 `RESUME_NOT_ALLOWED [꼴]`로 달라져도, 지정 오류를 traceback 없이 차단한다는 검출 경계는 강화된다.

## 3. 독립 탐침과 결과

1. **원 round4 독립 탐침 무수정 실행**: `original_probe/probe_resume_independent.py`; 작성 당시 원 핀 문자열도 그대로 보존. 현재 repo는 환경변수로 연결한다. 181행의 과거 `attempt-null order is None` 단언에서 실패한다. 새 가드가 반례를 막아 예전 false-green 기대가 뒤집혔기 때문이다. `original_probe/run.log` 참조.
2. **같은 원 탐침의 기대만 변경**: `expectation_adjusted/probe_resume_independent.py`. 입력 생성·변조·호출은 동일하다. 두 guard 단언과 CLI 기대 두 boolean만 변경했다(`expectation_only.diff`). 실제 scratch Git 원장 recover 네 건의 rc는 모두 0, 결과 resume_ok는 모두 false(정직 mismatch, 기존 PC13 두칸, R1, attempt-null). 이 rc0은 복구 명령이 비자격 결과를 성공적으로 기록했다는 뜻이며 연구/재개 GO가 아니다. 결과는 `expectation_adjusted/results.json`.
3. **독립 집중 API 관측**: `probe_resume_focus.py`, `probe_results.json`, `probe_focus.log`. 기존 fixture는 작은 파일 생성과 fake_execute/read_run만 재사용하며 `ResumeRunner.run/_copy`, result writer, recount, order, presolve는 후보 실제 함수다. 원 반례 네 개, 정직 흐름, summaryless, bool/float, source 이동, shape 및 copied prefix 변이를 기록했다. 작성 측 506개 전수 시험이나 71개 변이 수와 합산하지 않는다.
4. **요약 없는 copied prefix 경계**: `probe_summaryless_copy.py`, `copy_boundary_results.json`, `copy_boundary.log`. 실제 `_copy`를 실행하고 read_run 지점의 모의 BaseException으로 요약 미생성 중단 상태를 만들었다. 틀린 쪽에는 복사된 payload 한 파일만 합성 변경했다. 소스·원천 원장·launch/end를 함께 변조하지 않았다. 이 오류 주입은 그 자체가 실제 정상 copytree 동작이라는 주장이 아니다.

Windows Python 3.12의 일반 파일을 사용했다. 후보 `read_regular_file`은 `os.O_NONBLOCK`을 요구하므로 첫 원형 실행은 해당 상수 부재로 실패했다. 후속 집중 탐침은 **일반 파일에만 `O_NONBLOCK=0` 호환값**을 사용했다. 실제 FIFO·POSIX·프로세스·NFS/잠금·현장 신원 자격을 부여하지 않는다. 원 독립 CLI 탐침의 직렬 lock 대체와 dead-parent 선언도 원형 그대로이며 그 한계를 유지한다.

재현:

```powershell
$env:RINT_REVIEW_REPO='C:/path/to/pinned/repo'
python -I -B -X utf8 .\original_probe\probe_resume_independent.py
# 원래 false-green 단언 181행 실패가 기대됨
python -I -B -X utf8 .\expectation_adjusted\probe_resume_independent.py
python -I -B -X utf8 .\probe_resume_focus.py C:/path/to/pinned/repo
python -I -B -X utf8 .\probe_summaryless_copy.py C:/path/to/pinned/repo
```

탐침은 자기 디렉터리 아래 scratch를 만든다. 실제 연구 경로, 호스트, solver는 사용하지 않는다. Linux에서도 동일 경로 인자를 줄 수 있으며 그 경우 O_NONBLOCK 호환 대입은 실행되지 않는다.

## 4. Q6 한정을 실제로 가르는 반례 — 새 전칭 수용 불가

최소 상태:

- 원천 attempt_1: L01 완료, L02 자원 실패·부분 payload. 원천 결과와 해시는 정상.
- attempt_2: 실제 `ResumeRunner._copy`가 L01 payload와 groups를 복사함.
- 그 시점 부모 사망을 모의하여 요약은 애초 쓰지 않음. 음성은 복사된 L01 payload 한 파일에만 불일치 주입. 양성은 그대로.
- source digest/attempt/ledger는 그대로다. 모든 사본을 일관되게 고친 공격이 아니다.

| 값 | 정상 중단 대조 | 단일 copied payload fault |
|---|---:|---:|
| source vs L01 copied payload | 같음 | 다름 |
| stage summary | absent | absent |
| groups 문제 | null | null |
| 결과 cause | parent_dead | parent_dead |
| 결과 resume_ok | true | true |
| 다음 order 문제 | null | null |
| presolve 문제 | null | null |
| 다음 runner `_src_done(L01)` | true | true |

불일치 source SHA `b17effb4271344f6d481395eca4c304756b38dd168f7060a5cbca437797f5b81`, target SHA `05d7ef1056ff26f09c380b64d7f78a67bf849e88eb0dbc9a442a8755549440cc`.

원인: 공통 검증은 4756행에서 `isinstance(s, dict)`일 때만 `resume_boundary_problem`을 호출한다. summaryless일 때 ⓓ는 원천의 첫 미완료 L02만 확인한다(4676–4707). 선행 완료 L01의 바이트 대조가 없으므로 다음 `_src_done`은 L01의 rc0·폴더를 보고 다시 복사 가능(5727–5733). 요청서 §4에 명시된 한정이 실제로 발화한다.

**무너지지 않는 것:** 원 R1/R2·from·attempt 결속 수정, 첫 미완료 런의 비결정적 재계산 차단, 정직 `_copy` 단독의 바이트 보존. `shutil.copytree` → 로그 → launch/end → read_run 순서(5755–5768)는 일반 복사 중단을 실패로 만든다. 본 탐침은 디스크 부족/중단만으로 잘못된 payload를 만드는 것을 입증하지 않았다. 따라서 합성 결속 수용을 실제 I/O 무결성 전체 보증으로 확장하지 않는 경계다.

남은 최소 선택:

- 보장을 현재 코드 범위로 제한한다면: **요약 없는 재개에서 원천과 불일치한 이미 복사된 선행 런을 모두 검출한다는 보장은 제외**한다고 Q6에 명시. “서로 어긋난 기록이면 모두”라는 표현은 쓰지 않는다.
- 이 부류까지 닫는다면: summaryless에서도 실제 원천상 완료된 prefix 중 현재 시도에 완료 흔적이 있는 런의 launch/end와 payload를 원천에 대조. 단, 아직 복사하지 않은 prefix나 중단된 복사 자체를 새 결과로 요구하지 말 것. 위 정상 중단은 유지하고 단일 payload/launch/end 불일치만 거부하는 회귀를 추가. `rerun=None`일 때 원천 완료 prefix 전부, 첫 새 런 미시작, 3시도 effective 원천을 각각 포함.

## 5. Q4/Q6 권고 문구

> PC14-02/03 및 PC15-01–05의 지정 재개 결속 반례는 고정 코드와 합성 입력 범위에서 차단됨을 확인했다. 원천 미확인은 결과 줄을 보류하며, 확인된 결속 모순은 재개 불가 결과로 기록하고 다음 재개를 거부한다. 요약 없는 시도의 이미 복사된 prefix 무결성, 모든 파일의 일관된 변경, 실제 호스트·I/O·프로세스 자격은 이 확인의 보증 범위가 아니다. 현장 자격·12단위 끝-끝·새 봉인과 S0 단계 2/등록 R의 진입 판단은 별도다.

“정직한 흐름에서 틀린 결과를 받아들이지 않는다”는 무제한 문장 대신 **검사한 정상·고장 사례와 계약 가정을 함께 쓰는 것**을 권고한다. 다음과 같은 말을 현재 증거만으로 쓰지 않는다: 모든 중단/재부팅/파일 손상에서 안전함, 다른 기계 이동이 자동 허용됨, 모든 모순은 결과 줄이 생기기 전에 차단됨. 특히 동일 재개사슬은 machine/env를 같게 요구한다(3582–3584); 다른 기계 재실행이라는 말은 허용 절차를 따로 구분해야 한다.
