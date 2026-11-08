# Rint ② 회차 ④ — 독립 재확인 판정 (2026-11-09)

**지정된 11개 항목은 아래 한정으로 닫힘. 재개 정책 전체는 HOLD. 새 P1/P2는 없고 새 P3는 1건(RR4-01: 비동치 변이를 동치로 제외한 증거 회계)이다.**

- 대상: 1f9f3607eb2f0118d322eeff780bba6eb17b85a2, claude/sdcp-dem-manuscript-si-pqwtv8.
- 비교: 17d45fb9cdfc7033bdfd41509527cea23ba1654c.
- 입력 ZIP: codex_rint2_rr_round4_1f9f3607eb2f.zip, 3,992,042 B, SHA256 ab3d7da16df298be7378ea62251d06983e319860f8688f14e498256882d23b3f.
- 포장 404개 해시 및 내부 6개 목록 일치. repo/ 403파일 전부 원격 고정 핀의 Git blob과 일치. 제출 의존 28파일 중 변경은 rint_r_chain.py, test_rint_r_chain.py 2개이며 나머지 26개 동일.
- 실행: Windows Python 3.12.14, 작은 합성 입력·실제 판독 함수·scratch Git 원장. 실제 물리 풀이, WSL/ibb/kgy, GPU, 제출, 등록, 운영 원장 변경 없음. 전체 게이트/495개 전체 사슬/현장 자격은 재실행하지 않았다.
- 아래 파일:행은 이 핀의 package/repo/ 상대 경로. 재현 명령은 동봉 증거 루트 기준. 코드 수정 지시나 실제 실행 승인이 아니다.

## 1. Q1 — 항목별 닫힘 범위

| ID | 판정 | 실제 근거·남는 경계 |
|---|---|---|
| RR3-01 (P2) | **닫힘** | scripts/rint_r_chain.py:2167, :2246, :4330. 실패 생산자/복사/합치기의 3칸 파일 신원은 file_ids; 완료 ARM_PUBLIC과 분리된다. 원 반례의 stop 두 칸 편집은 timeout, resume_ok=False, 다음 항목 RESUME_NOT_ALLOWED. 성공 생산/복사/합치기 30기록은 verified 보존. 바이트 출처 인증은 아니다. |
| PC12-03 | **닫힘 — 앞 런 판독 완료 계약** | :4330–4339. 앞 런은 exit_ok와 성공 ARM_PUBLIC 계약을 함께 만족해야 한다. 실패/빈/파일 신원 목록을 완료로 세던 구체 부류는 닫힘. 모든 재개 출처 변조까지 닫지 않는다. |
| RR3-02 (P3) | **닫힘** | docs/reviews/codex_rint2_rr_round3_request_20261108.md:83,84,86,94,135,140,154. 7개 해당 줄이 역사 보존+현재 범위 정정으로 바뀜. 기존 rg 6개 적중 모두 정정 표지 있음. |
| PC13-01 (P2) | **닫힘 — 원 반례와 지정 보완** | rint_r_chain.py:4351, :4367. RESUME_MISMATCH의 stop 두 칸 편집, same=True 추가 편집을 원천 payload가 남은 조건에서 거부. 단 **같은 부류 전체 종결은 불가**: PC14-02/03 생존. |
| PC13-02 (P2) | **닫힘** | :2195, :2282, :2478. 값 계약을 분류기와 실제 read_run이 공유. 실제 reader에 sentinel 거부를 넣으면 ARM_UNREADABLE로 멈춤. impossible/null 값으로 완료 승격하는 지정 반례 차단. |
| PC13-04 (P3) | **닫힘** | :2177, :2273, :2342, :5462. 분류·판독·RunnerGraphSource가 같은 파일 접두 함수 사용. 지정 복제 식 제거의 확인이며 모든 별칭/dataflow의 보편 증명은 아님. |
| PC14-01 (P3) | **닫힘** | :2236–2242. positive cg_resid를 유한수 검사 후 conv_ok에 넘김. ±10**400 및 4300자리 정수가 분류·summary JSON·recount에서 예외 없이 거부. 4301자리 JSON은 이 Python의 reader가 먼저 거부. kgy 3.8.10 자격은 미검증. |
| PC14-04 (P3) | **닫힘 — 선언된 값 영역** | :2191–2192, :2212–2230. pid16hex/sid32hex와 기존 τ 상한. τ 자체 수용, 바로 위 representable float 거부. 생산 성공/zero 출력 보존. 실제 실행 귀속까지 검증한 것은 아님. |
| PC14-05 (P3) | **닫힘** | :4348, :4397–4399. resume 5칸 정확 집합 검사. extra/missing determinism은 자격 False, 정직 before/after-rerun 양성 보존. |
| PC14-06 (P3) | **닫힘 — 지정 네 생존 변이** | test_rint_r_chain.py:16720–16723, :16739–16753. M14/M18/M47/M54 입력은 현재 거부; 해당 보호 제거는 허용 또는 AttributeError. 정직 from=resume_of=2 등 보존. **추가 M56 문제는 별도 RR4-01**. |
| SELF-158 (P3) | **닫힘 — 문장 정정만** | 회차③ 요청서 :134에서 옛 GU rc 종결 과장을 명시적으로 철회·한정. 비교 핀부터 있던 문장으로 이번 diff에서 불변. 런타임 추가 종결을 뜻하지 않음. |

PC13-03, PC14-02/03, PC11-05–08, SELF-155 실침대와 현장·봉인 조건은 그대로 남는다. 원장을 실제로 고치지 않았다.

## 2. Q2 — 팔 기록 계약: 수용

**검증 완료 형식의 기록과 판독 실패 때 보존한 파일 신원 목록을 구분하는 이번 계약은 수용한다.** 구조뿐 아니라 실제 생산자의 상태·값 영역까지 좁혔고 세 생산자가 같은 생성 함수에 연결됐다.

| 이번 독립 탐침 | 관측 |
|---|---|
| 팔 0–7의 비어 있지 않은 255부분집합 × positive/zero | 510/510 정상 분류 |
| 구조 음성 | 38/38 기대대로 거부/비완료 |
| JSON 값 영역 변이 | 728분류에서 미처리 예외 0; 허용되는 선언 한정도 기록 |
| strict summary → recount | 14/14 기대 판정, 직접 셈과 디스크 재계산 일치 |
| 실제 Runner/read_run → copy → MergeFetch | 10합성 시나리오 × 3경로, 성공 기록 30/30 보존 |
| 세 경로의 실제 판독 실패 | 3/3 ARM_JSON_COUNT → file_ids |

원 회차③ 탐침은 원문 그대로 재실행했다. 옛 ‘편집 후 허용’ assert가 더 이상 맞지 않아 rc1. 오류와 출력을 보존했다. 두 개의 결함 존재 assert만 닫힘 기대값으로 바꾼 사본은 rc0이며 diff도 동봉했다. 원본 SHA256은 7f335c758c036c6de5ab10ef5b9ab3d35d6eb10ab3f0182694bdea03914b74d7. 원 스크립트의 옛 pin은 탐침 신원이며 실제 로드 소스 SHA256은 이번 47a520e8ad300101c6f8d2660d7368eead77f0f3b425bdcf1d37c379fe0c8720이다.

~~~bash
python -I -X utf8 -B arm_contract/probe_arm_contract.py
python -I -X utf8 -B arm_contract/replay_original.py
~~~

완료 기록의 SHA↔디스크 원자료, 다른 런의 정직한 기록 차용, zero의 자유 칸·반복 수 상한 등은 이 계약만으로 검증하지 못한다. 728분류에서 예외가 없었다는 결과를 ‘728개 위조 전부 거부’로 쓰면 틀린다.

실제 MergeFetch 판독은 썼지만 원장 열기는 최소 이미 열린 객체로 제공했고, run_in_group은 작은 Python 가짜 writer로 바꿨다. 물리 모델·프로세스 그룹 자격 시험은 아니다. fixture 생성만 제출된 FAKE_SRC/record_templates를 사용했으며 독립 기대값과 판정은 별도로 작성했다.

## 3. Q3 — 지정 재개 수정 수용, 일반 정책 종결은 불가

현재 보호는 PC13-01의 두 칸 편집과 PC14-05 필드 결손을 차단한다. 그러나 PC14-02/03은 **실제 디스크/원장과 모순인 상태를 현재 자격 길이 통과시키는 한정**이다. 모든 사본을 일관되게 고친 위조의 암호학적 인증을 새로 요구하는 문제가 아니다.

resume_attack/probe_resume_independent.py는 실제 request·ResumeRunner 비교·result/recount·원장 읽기/순서를 호출한다. _execute만 작은 SYNTHETIC writer로 대체했다.

| 입력 | resume_ok | 다음 항목 순서 검사 | 풀기 전 재계산 |
|---|---:|---|---|
| 정직 RESUME_MISMATCH | False | RESUME_NOT_ALLOWED | 자격 없음 |
| stop 두 칸만 TIME_LIMIT/다음 런으로 편집 | False | RESUME_NOT_ALLOWED | 자격 없음 |
| 위 편집에 compared.same=True 추가, 원천 남음 | False | RESUME_NOT_ALLOWED | 자격 없음 |
| 정직한 비교 완료 후 timeout | True | 통과 | 통과 |
| PC14-02 R1/R2: 복사/새 런 경계 재표기 | **True** | **통과** | **통과** |
| PC14-03: attempt.resume_of=null + summary.resume=null 등 | **True** | **통과** | **통과** |
| PC14-03: 3시도에서 from을 옛 시도로 다시 결속 | **True** | **통과** | **통과** |

### PC14-02 — 원천이 있어도 다른 L02를 완료 복사로 바꾸면 통과

rint_r_chain.py:4415–4421은 첫 새 런/rerun을 기록에서 고른다. :4423–4427은 멈춘 런=rerun이면 바이트 대조 전에 반환하며, :4443–4450은 **선택된** 런의 원천 payload만 다시 비교한다. _src_done은 :5310.

독립 R1/R2에서는 원천 attempt_1과 대상 attempt_2의 **L02 payload와 launch bytes가 모두 다르다.** 그 bytes는 유지하고 요약에서 L02를 복사 런으로, rerun을 뒤로 옮겼다. 현재 결과는 timeout/True, 다음 재개의 _src_done(L02)도 True다. R1은 scratch Git의 실제 main(recover --ledger)가 rc0으로 resume_ok=True 결과 커밋을 만들었다. found_attempts_problem도 이 경계를 거부하지 않는다.

실제 연구값 오류가 이미 발생했다는 뜻은 아니다. 그러나 ‘출처가 어긋난 완료/새 런 경계는 재개 전에 막는다’는 일반 보장은 성립하지 않는다.

### PC14-03 — 원장 항목과 resume source 결합이 늦거나 없다

:3779–3801은 사슬 결과 줄을 재계산하지만 attempt.resume_of를 해당 원장 entry와 대조하지 않는다. 그 대조는 found_attempts_problem의 :4843–4848에 있다. :4403–4409는 from 범위 검사이며 당시 유효 사슬 끝과 같은지 검사하지 않는다.

- attempt-null 반례는 실제 recover 결과 커밋, 다음 순서 검사, 풀기 전 재계산까지 통과. 후속 found_attempts_problem에서만 원장 불일치 검출.
- 3시도 from-rebind는 found_attempts_problem도 통과. from=1이 범위에는 들어가도 당시 필요한 유효 source는 별개다.

**PC14-02/03은 열림 유지. 봉인 전 한 번 확인으로 넘기고 미래 재개 정책 전체 GO를 주는 것은 반대한다.** 미래 시도 폴더·launch/end·복사 경계는 봉인 뒤에 생긴다. 봉인 시 과거 기록이 정직했다는 확인은 미래 기록의 자격을 검사하지 못한다.

최소 처리 선택지:

1. 권고: 자격 결과 쓰기와 다음 재개 허용 전에 복사 표기↔원천 launch/end 및 필요한 파일 신원, attempt.resume_of↔원장 entry, resume.from↔그 시점 유효 사슬 끝을 공통 검증에 연결한다. 원 반례·정직 3시도·복사/새 런 양성을 보존한다.
2. 코드 보완을 미루려면 **각 recover/재개마다** 실제 기록을 독립 대조하고 근거/hash를 남기기 전 진행하지 않는 외부 관문을 별도 정책으로 고정한다. 이때도 코드 단독 재개 정책 전체 GO라고 부르지 않는다. ‘봉인 때 한 번 확인’은 이 대안이 아니다.

이번 답으로 이를 구현·등록·승인하지 않았다. 기존 P3 두 건을 새 P1/P2로 중복 등재하지 않는다.

~~~bash
python -I -X utf8 -B resume_attack/probe_resume_independent.py
~~~

결과에는 15개 경우+별도 M54, 네 보호 제거, 실제 recover 4회가 있다. Git은 scratch 저장소만 사용하고 잠금·부모 생존·그룹 정리는 공개 모의다. recover rc0은 결과 기록 성공이며 재개 자격 True와 별개다.

## 4. 새 P3 — RR4-01: M56을 동치로 제외한 검출률이 틀림

- 대상: 이번 핀.
- 위치: docs/reviews/codex_rint2_rr_round4_request_20261109.md:103, docs/reviews/rint2_rr2_fix_evidence_20261105/preattack14/REPORT.md:9, 그 폴더 probes/mutate.py:60 및 mutation 원기록.
- 주장: 변이 51개 중 동치 2개(M46·M56)를 빼면 49개, 45/49 검출, 비동치 생존 4개.
- 반례: M56은 ‘if not src.is_dir():’를 ‘if not src.exists():’로 바꾼다. 모든 오류 입력에서 동치가 아니다.

작은 로컬 합성 입력에 attempt_1을 **일반 파일**로 만들고 옆에 attempt_1.rejected.json을 둔다. from=1, copied=[], rerun=R, compared=[], determinism=assumed인 post-rerun 요약을 실제 resume_rerun_problem에 넣었다. helper 모의 없이 현재 함수와 그 한 줄 변이를 비교했다.

| 코드 | 직접 결과 |
|---|---|
| 현재 is_dir | 원천이 옆 거부 기록이라는 사유 반환 |
| M56 exists | **None — 같은 사유를 놓침** |

~~~bash
python -I -X utf8 -B docs_tests/probe_m56.py
~~~

docs_tests/m56_result.json에 입력과 두 결과가 있다. 현재 분기는 rint_r_chain.py:4438–4442, leftovers는 :5283–5293. **현재 생산 코드는 이 반례를 거부한다. 현재 코드의 CLI 재개 허용 결함을 새로 발견한 것이 아니다.** 동치 분류와 그에 의존한 시험 회계가 무너진다.

최소 수정:

- 역사 원로그는 보존. M56을 동치가 아니라 **구별 가능한 미검출 변이**로 정정한다. M46의 JSON 영역 동치 처리를 유지하면 당시 수는 **45/50, 비동치 생존 5개**다.
- 전체 입력 영역을 주장하려면 이 파일/거부기록 경우를 음성 시험에 넣어 M56을 검출한다. 유효 원천 디렉터리만 시험한 것이라면 그 입력 한정과 미검출을 명시한다.
- 현재 PA14 선정 23/23 및 M14/M18/M47/M54 네 건의 종결과 혼합하지 않는다. 이 반례로 그 네 보호가 무너진 것은 아니다.

## 5. Q4 — 기대 변경 수용

test_rint_r_chain.py:14936의 CT06_ARM은 실패 출력의 3칸이다. 완료된 앞 런을 시험하려면 :14944의 ct06_pub으로 바꾸는 것이 맞다.

독립 diff/AST 대조에서 기존 시험 함수를 삭제하지 않았다. 기존 함수 중 본문 변경은 t_PC12C이며 의도한 성공 앞 런을 성공 꼴로 보정하고 kit/request 맥락을 보탰다. 실패 신원 목록과 group_cause 결손 음성은 남는다. 실패를 지워 통과시킨 처리가 아니다.

pid/sid 정정도 생산 함수와 일치한다.

- run_contract.py:722: p3ca- + SHA256 16자리.
- step3_sigma.py:232–239: BLAKE2b 16바이트 → hex32자리.
- rint_r_chain.py:2420–2433: zero 오차0.0, positive 증서 판정에서 오차 계산.

제출 로그의 옛 시험×새 코드 479/481도 개별 줄과 행 JSON으로 대조했다. 실패 둘은 CT06/PC12C이고 바뀐 행은 의도한 완료 고정물이 file_ids였던 자리다. **제출 실행 기록의 재집계**를 이번 독립 전체 사슬 재실행으로 세지 않는다.

## 6. Q5 — 사용할 수 있는 결론

요청한 **‘코드·설계·문서 GO(재개 정책 포함)+봉인 전 확인’은 그대로 줄 수 없다.** 지정 보호 수정과 문서 정정은 수용하지만 현재 자격 경로의 PC14-02/03을 봉인 때 한 번 보는 것으로 미래 재개를 인증하지 못한다. 새 RR4-01은 시험 증거의 별도 문구/회계 정정 사항이다.

사용 가능한 문장:

> RR3-01·02, PC12-03, PC13-01·02·04, PC14-01·04·05·06 및 SELF-158 문장 정정은 지정한 코드·합성·문서 범위에서 닫힌다. 재개 출처·복사 경계의 PC14-02/03은 열림이며 재개 정책 전체는 HOLD다. 실제 환경 자격·S0 단계1 채택·12단위 통합·새 계획/핀 봉인 및 연구 실행 승인은 별도다. 변이 M56의 비동치 생존을 RR4-01로 기록하고 검출률을 정정한다.

현장 자격, kgy S0 실침대와 SELF-155 채택, 12단위 끝-끝, 숫자/실행 정책 및 새 계획 봉인을 남은 이름 목록만으로 완료 처리하지 않는다. 기존 순서와 바깥 범위는 바꾸지 않는다.

## 7. 검증 회계와 한계

| 이번 독립 작업 | 결과 |
|---|---|
| 포장/고정 Git blob | 404 해시/403 repo blob 일치, 26 의존 동일 |
| ARM 독립 묶음 | 9개 검사군 성공; 상세 관측 수는 §2, 합산 금지 |
| 원 RR3 반례 | 원문 rc1(옛 결함 존재 assert 반전), 두 assert 정정 사본 rc0 |
| 재개 탐침 | 15경우+M54, 실제 recover4회, 네 보호 제거; declared bypass 보존 |
| 문서·fixture·네 변이 작은 검사 | 24/24; helper 추출/합성 identity 한정 |
| 작성 측 상주 시험 선별 재실행 | RR3A/B/C, PA14A 4메서드 통과; PA14C 값 하위26행 별도 통과. 전체 PA14C나 495/495로 세지 않음 |
| M56 | 실제 helper 두 실행에서 비동치; 현 코드 거부 |
| 제출 원로그 재집계 | 481→487→491→495, targeted/py38/e2e 행 수 및 source/test diff 확인. M56 동치 해석은 반증 |
| 미실행 | 전체 게이트·전체 사슬·전체 변이 캠페인·Linux /proc/flock/NFS·실제 SIGKILL/호스트·연구 계산 |

ARM 탐침 개발 중 세 오류(request/env 정규화, Runner 인수 순서, 재사용 merge 대상)는 리뷰 스크립트 오류로 보존·설명했다. 대상 코드를 고쳐 통과시킨 것이 아니다. Windows O_NONBLOCK=0은 일반 임시 파일에만 적용; FIFO 인증이 아니다. Python3.8 결과는 제출 로그 확인이며 여기서 새 실행한 것이 아니다.

동봉 REPRODUCE.md, probe/결과 JSON, 원문/변경 assert diff, 제출 package, 원격 tree 응답으로 재현할 수 있다. 판정문·증거가 제품 코드·운영 원장·등록을 바꾸지 않는다.

**최종: 지정 수정 한정 수용 / 재개 정책 전체 HOLD / 물리 실행·생산 GO 미부여.**

