# Rint ② 회차 ③ — RR2 · PC9 · PC10 및 기대 변경 독립 보조 검토

- 대상 pin: `17d45fb9cdfc7033bdfd41509527cea23ba1654c`.
- 패키지 소스: `package/repo/`. 실제 읽은 `scripts/rint_r_chain.py` SHA-256 = `48f0e7fff068eea752407ad56955c159e937f8a33801148786b0d5a3e650f95c`.
- 범위: RR2-01–03, PC6-05/13의 이번 잔여, PC9-01–07, PC10-01–10, Q3 기대 변경 및 Q6 문구. PC11/12 신선 공격과 S0는 별도 검토 결과를 합쳐 판정한다. 이전 verified 35는 재판정하지 않았다.
- 독립 실행: `contracts_probe.py` **105/105 관측**. 작성 측 메서드 수나 이전 303/311과 합산하지 않는다. 실제 모듈 함수에 작은 합성 기록·일반 파일을 주었고, 시뮬레이터·WSL·ibb·연구 값·실행 정책은 건드리지 않았다.
- 환경 한계: 실행 결과에 기록된 **Windows Python 3.12.14**. 없는 `os.O_NONBLOCK` 상수만 `0`으로 주어 **일반 파일** 판독을 시험했다. FIFO/nonblocking, /proc, process kill, flock, 현장 파일시스템은 이 실행으로 인증하지 않는다. 그 부분은 소스 대조만이다.

## 1. finding별 판단

아래 닫힘은 원 finding의 최소 수정과 이번 검토 경계에 한정한다. 재개 정책 전체·현장 자격·생산 GO와 동의어가 아니다. `S`=독립 소스/문서 대조, `E`=이번 직접 함수·합성 파일 실행.

| ID | 판단 | 근거 및 독립 검출 | 남는 한계 |
|---|---|---|---|
| RR2-01 | 닫힘 | `rint_r_chain.py:3832–3841`은 `type(rc) is int`만 성공, `:4276`의 orphan skip도 공용 판독. E: 0/1/false/0.0/-0.0/"0"/null/true의 실제 orphan→result_fields에서 정수0만 parent_dead/자격True, 나머지는 runner_rc/False. recover wrapper도 같은 음성. | 이번 보조 탐침은 Git CLI까지의 연결이 아님. 부모의 구 회차 실경로 재실행과 합쳐 판단. 정상 int0 + 자기 로그 Traceback을 무조건 오류로 판정하는 새 정책은 요구하지 않음. |
| PC6-13 | 닫힘 — 이번 남은 rc 분기 | `:3866`, `:4189`, `:4233`, `:4285–4287`이 스스로 종료한 null/bool/float와 정수 실패를 실패/자격불가로 읽음. E: chain_end null 포함 recover 대조. | 원인 글의 범용 실제 원인 인증은 아님. 그룹 종료 확인의 실제 OS 자격은 별도. |
| PC6-05 | 닫힘 — 판독 코드 | `:3935–3942`, `:3955–3964`, `:4352–4356`이 로그 상태와 텍스트를 분리. E: missing·directory 로그 False, 정직 timeout+읽힌 빈 일반로그 True. | 빈 정상 파일의 내용이 실행 사실을 증명하지는 않음. EACCES·FIFO·실제 끊긴 링크는 소스만 읽음. |
| RR2-02 | 닫힘 | Q9 설계 `q9_predict_units_design.md:69`, 회차② 요청서 `:374`, 회차① 요청서 `:130`, `q9_time_budget.py:6–7`에 현재 계약 명시/과거 문구 비활성 표지. E: 현재 산식 stdout(LF 정규화)와 수정 전 보존 출력 일치, 저장 JSON 의미도 일치. | byte 재현은 현재 계산 경로의 환경 결정성 보증이 아님. payload 없는 재개는 여전히 결정성 가정. |
| RR2-03 | 닫힘 | 등록 R `:283`, 설계 v1 `:339`의 현행 문구가 두 곧은 평행 레일·축정렬·이웃셀·R̄sh2=1·정수 Lc 및 Δ/λ=0.02–0.63, q=0.4–19 한정. E: AST로 읽은 `carbon_junction.CJUNC_QUALIFIERS[3]`에 정확 인용 포함, 축저항 제외/임의 교차 미검증 문구 존재. | BAN8 자체 재실행 및 다른 기하 검증은 하지 않음. RINT2-L01은 그대로 open. |
| PC9-01 | 닫힘 | `:3886–3888`, `:4285`, `:4290–4291`이 by-chain/recover의 unknown cause를 모두 자격불가로 함. E: 모르는 글/false/0/빈글/list/dict × 양쪽경로 12관측 모두 False. | 원인 **글**까지 같다는 주장은 하지 않음. |
| PC9-02 | 닫힘 | `load_ladders :6017–6018`이 Rj0 확인 런 rc를 팔 읽기 전에 `rc_success`로 검증하고 LADDER_SET. S. | 이 보조 실행에서 완전한 사다리 fixture 재구성은 하지 않음. |
| PC9-03 | 닫힘 | `:5749–5786`이 present-unreadable과 absent 구분; `:5789–5792` 원자적 summary쓰기. E: truncated/list/bool/duplicate/NaN→unreadable, 없음→absent. | rename/fsync의 실제 파일시스템 내구성은 미검증. |
| PC9-04 | 닫힘 — 코드 수정 | `:3914` 한 번 open, `:3920` 같은 fd fstat, `:3924` 같은 fd read, `:3932` close. is_file 후 다른 경로 재open 창이 없음. S + 일반파일 E. | FIFO/nonblocking 실동작은 Windows 검토로 인증하지 않음. |
| PC9-05 | 닫힘 — 명시한 검사 범위 | `test_rint_r_chain.py:12834–13027` alias 추적 및 허용 문맥. E: 새 bool alias/closure/raw==0/dict.get/pop/f-string비교 여섯을 검출하고 정상 공용reader는 허용. | 동적 계산 열쇠, 값 순서로 꺼내기, 다른 모듈 등은 명시된 비검출 범위(:12829). 보편적 데이터흐름 검증은 아님. |
| PC9-06 | 닫힘 | 회차① 요청서 `:130` 과거 발송 문장 보존 + 현재 계약 표지. S. | 역사 원문을 삭제할 필요 없음. |
| PC9-07 | 닫힘 | 회차② 요청서 `:347` 및 findings RINT2-L01 note의 11-05 정정에서 BAN8 좁은 범위를 명시; L01 open 보존. S. | L01 실침대 노출 보고 조건은 닫지 않음. |
| PC10-01 | 닫힘 | `chain_end_failed :3866`, `run_record_shape :4005–4012`, `run_exit_failed :4189` 공통 의미. E: null cause/null rc, malformed rc 양쪽 경로 자격False. | 모르는 원인/미확인과 실제 자원 실패 확정을 혼동하지 말 것. |
| PC10-02 | 닫힘 | `_verdict_compute :6912–6919`, `MergeFetch.unused_runs :6492–6495`이 unreadable 요약을 조용히 제외하지 않음. E: 실제 판정 입구 다섯 malformed summary가 INPUT_NOT_STAGE. 합치기 가지는 S. | 미채택 시도의 unreadable도 합치기를 막는 보수적 범위 확장임을 유지. |
| PC10-03 | 닫힘 — 코드 수정 | `_read_group_json :3734`, `read_attempt :3328`, `rejected_record :4378`이 같은 fd 읽기 사용. S. | 실제 FIFO 및 Linux 권한/종료 시점 검증 별도. 처음부터 rejected.json이 특수파일이면 상위 is_file 분기가 어떻게 보고하는지는 기존 한정. |
| PC10-04 | 닫힘 — RC 스캐너 범위 | 위 PC9-05의 독립 새 표현 여섯 및 현재 pin source scan 0건. `:12822–12829`에 허용·미검출 범위 정직하게 구분. E. | scanner가 오직 'rc' 표식에 의존하므로 인증으로 확대 금지. |
| PC10-05 | 닫힘 | source `:3879–3882`, `:4254–4256`; 원 보고 §0의 “같은 답” 취소 및 “같은 자격” 정정. 실제 E: unknown+MemoryError에서 원인 글이 다를 수 있어도 둘 다 False. | 차이가 사라졌다고 쓰지 않음. |
| PC10-06 | 닫힘 | `run_traces :3972–3979`, `stop_record_problem :4030–4031`. E: 진짜 prerun/no-trace만 True; end/log/output 흔적 각각 False. | 실제 디렉터리 권한·네트워크 파일시스템 오류는 현장 별도. |
| PC10-07 | 닫힘 | `preattack10_fix/REPORT.md:59`, 원 보고 `:93`; 보존 전 로그 끝 `FAILED: ['PE03u','CE01','CE02']`와 맞음. S. | push된 역사 메시지 수정 요구 없음. |
| PC10-08 | 닫힘 | `:3993–3995`, `:4027–4029`, `:4223–4224`가 RUNNER_RC→TIME_LIMIT 이름 바꾸기 자격 승격을 막음. E: 옛 TIME_LIMIT/nullcause/nullrc 7기대행 모두 False, 원인 두 runner_rc/다섯resource. | 모든 producer-impossible 문서가 다 닫혔다는 포괄 주장과 별개. PC11/12 잔여·새 반례 대조 필요. |
| PC10-09 | 닫힘 | `:4007–4012`: killed 원인+정수rc는 bad. E: timeout+1, signal+0, signal_after+false 거부. | orphan 끝기록의 signal/timeout+int는 실제 wait 경합 가능하여 원래 반례와 다름. |
| PC10-10 | 닫힘 | `:4373–4387` 공용 rejected parser, result_recount `:4465` 및 recover 호출부 사용. E: list/null/bool/숫자/truncated/duplicate 모두 Stop ATTEMPT_LEDGER_MISMATCH, AttributeError 없음. | 완전한 recover CLI의 폴더 순회는 부모의 재실행 근거와 합침. |

## 2. Q3 — 303/311의 여덟 기대 변경

수정 측 결과 JSON을 숫자만 인용하지 않고 원 탐침 입력(`runtime_review/probe_runtime.py:65–71`)과 생산자(`rint_r_chain.py:4974–4988`)를 대조했다.

- `summary_{plain,python,oom,host,disk,gpu,cupy_oom}_TIME_LIMIT_None`은 **TIME_LIMIT + group_cause=None + rc=None**을 만든다. 실제 러너가 시간 초과를 기록하면 `group_cause='timeout'`, rc=null이다. 원 입력은 정상 생산자 조합이 아니므로 timeout을 강제한 옛 기대를 버리는 것이 맞다. 첫 두 개 runner_rc, 나머지 다섯 resource여도 **재실행 자격은 모두 False**다. 이 일곱은 원인 문자열 검사였으므로 문자열 변화만 보고 “재개가 열림/닫힘”으로 세면 안 된다. 별도 actual result_fields 7관측으로 False를 확인했다.
- `known_PC6_05_summary_missing_log_resume=True`는 당시 열린 결함을 의도적으로 고정한 행이다. 새 False가 수정 목적이다. 독립 양성쌍은 동일 정직 timeout 기록에 읽힌 일반 로그를 추가하면 True임을 확인했다.
- 따라서 이 **8개 기대 수정은 수용**한다. 다만 “303/311 PASS”를 “8개 무시하면 전부 통과”로 쓰지 말고, 옛 기대/새 원인/새 자격을 각 행으로 공개해야 한다. 이번 보조 검토는 핀의 전체 원 probe를 재실행한 숫자가 아니며 부모 재실행 결과와 별개다.

PC12가 넓힌 네 규약도 생산자 근거와 맞는다(구체 독립 공격은 별도 담당 결과에 의존).

1. TIME_LIMIT/RUNNER_RC는 `Runner._execute:4976–4988`에서 confirmed=True 뒤에만 나온다. false면 GROUP_UNCONFIRMED가 먼저이므로 새 확인 모순 거부는 정상 생산자 거부가 아니다.
2. 앞선 성공 런은 `:4997–5004`, 복사 성공 런은 `:5071–5079`에서 비어 있지 않은 arms_read 뒤에 반환한다. 실패 앞 런을 남기고 다음 런으로 진행한 요약은 재개 자격을 줄 수 없다. 10-27 이전 형식은 같은 의미로 인증하지 않고 별도 역사 비호환으로 표지하는 처리가 맞다.
3. `run_in_group:2791–2800`은 디스크 end를 cause=None으로 먼저 쓴 뒤 반환값만 signal_after로 바꾼다. summary 있는 경로가 디스크 signal_after를 거부하는 것은 정합적이다. **orphan 경로에서는 아직 받아들이는 범위**가 남는다.
4. `write_summary :5792` → canon_bytes/clean 생산자 바이트가 중복 키·NaN·Infinity를 내지 않으므로 strict JSON 거부는 정합적이다. 1e400→inf 잔여는 요청서가 명시한 한정이며 일반 JSON 문법/전 필드 유한성 인증으로 확대하지 않는다.

## 3. 새 문서 정정 권고 — 현재 한정표에 이전 세대 한정이 활성 문장으로 남음

**P3 후보, 문서만.** `codex_rint2_rr_round3_request_20261108.md:83–86`과 `:93–94`를 함께 읽으면 다음 세 문장이 서로 다른 세대의 상태를 현재형으로 말한다.

- :83 “런 기록 ↔ 그룹 끝 기록 교차 대조 없음” ↔ 실제 `rint_r_chain.py:4072–4077, :4133–4153`은 읽을 수 있는 사슬 쪽 끝기록의 원인·rc·확인을 대조함.
- :84 “디스크 signal_after 받음” ↔ :94는 요약 있는 경로의 불허를 명시함. 실제 orphan은 받고 summary 경로는 거부하므로 **경로 한정** 필요.
- :86 “code의 STOPS 소속 안 봄” ↔ 실제 `:4410`은 검사함. 남는 것은 STOPS 중 해당 위치에서 생산될 수 있는 부분집합까지 좁히지 않았다는 점.

최소 수정: 역사 원 REPORT는 보존하고 현재 요청서 첫 네 행에 `PC12 이전 한정 — 이후 상태는 …`를 붙이거나, 현행 잔여로 치환한다. 새 코드 결함이나 과학값 오류라는 판정은 아니다. 하지만 “한정표를 근거로 어떤 부분을 미검증으로 남겼는가”라는 해석에는 직접 영향을 주므로 문서 종결 시 정리한다. Q4의 `교차 대조 없음`도 `읽히지 않는/결합되지 않는 끝 기록의 대조 유예`로 좁혀야 한다.

재현(정적):

```text
rg -n '교차 대조 없음|디스크 signal_after 받음|STOPS 소속 안 봄|PC12 고침으로' docs/reviews/codex_rint2_rr_round3_request_20261108.md
```

## 4. Q4/Q6 권고 경계

이 보조 검토에서 닫은 RR2·PC6-05·PC9·PC10의 수정은 기존 HOLD 이유의 해당 부분을 제거한다. 그렇다고 `생산자가 쓰지 않는 모든 조합 거부`나 `재개 정책 일반 인증`이 성립하지 않는다. 요청서가 이미 남긴 missing-field 호환, 시작 기록 결속 부재, 없거나 구형인 끝 기록, 중복 런 이름, prerun 이름 차례, 복사 출처 등의 경계와 PC12 담당의 새 반례가 있으면 그 등급을 우선한다.

“남은 것 = 현장 자격 + S0-1 + 12단위 끝끝 + 봉인”은 작업 묶음의 짧은 이름으로는 가능하지만 **네 작업을 끝내면 자동 GO**라는 뜻은 아니다. 이전 판정 :195의 `S0-1 → s_min 개발 → ⑥ 비용/반복수 → 기하/반복수 확인 → 숫자/실행정책 → 새 계획/핀 → S0-2 → R` 순서를 생략하지 말고, 실제 S0 채택 조건·예외·계획해시와 최종 통합 핀 diff를 포함해야 한다. S0·PC12 별도 독립 판정 및 현장 자격 결과 없이는 캠페인 해제 문장을 만들 수 없다.

안전한 최종 문구 후보:

> 이번 핀의 지정된 수정과 합성 기록 판독 범위는 수용한다. 재개 정책의 기존 반례에 대한 코드 수정도 이 경계에서 수용하며, 실제 환경 자격·남은 한정·S0 개발 및 새 계획 봉인·12단위 통합 확인은 별도다. 실제 실행·등록 R 캠페인·정량 판정·생산 GO를 뜻하지 않는다.

## 5. 증거와 재현

- `contracts_probe.py`, `contracts_probe_results.json` (105/105, 원 소스 SHA 기록).
- 명령: `python -I -B -X utf8 contracts_probe.py` (review root; sibling `package/repo` 필요).
- 초기 결과 `contracts_probe_results_initial_quote_locator_error.json`는 88/89. 1실패는 리뷰어의 문서 인용 탐침이 Python 인접 문자열을 **원 소스 텍스트 substring**으로 비교한 잘못이었다. AST 상수로 결합한 정확한 실제 상수로 수정했다. 패키지 소스/문서 변경은 없으며 이 실패를 제품 finding으로 세지 않는다. 이후 자체 탐침에 PC9-01/PC10-06 16관측을 추가하여 최종105이다.

## 6. 보충 — PC12 원 p2/p4 입력의 실제 Git 원장 → 재개 자격 대조

원 `preattack12/p2_real_ledger.py`와 `p4_tl_none_after_fail.py`의 핵심 요약·끝기록·로그·결과 흔적을 작은 로컬 Git 원장으로 옮겼다. 패키지 소스는 변경하지 않고 실제 `recover_ledger`로 result 행을 커밋한 뒤 실제 `attempt_order_problem`을 호출했다. 원 전체 fixture는 Windows symlink 권한 때문에 사용하지 않았으며, 이 보충은 원 fixture 시험 수를 대신하지 않는다.

- 파일: `contracts_p2p4_git.py`, `contracts_p2p4_git_evidence/results.json`, 같은 폴더의 각 케이스 로그와 scratch Git 저장소.
- 실행: `python -I -B -X utf8 contracts_p2p4_git.py` (review root; 실제 Git 설치 필요).
- **12/12 기대 일치**. 105개 보조 함수 관측·작성 측 사슬 481·원 회차 311과 합산하지 않는다.
- 실제 Git header/entry/start/result의 바이트 연결·커밋과 재개 관문을 시험했다. POSIX `ledger_lock`, host/process 생존 확인, group cleanup은 순차 합성용 모의이므로 Linux /proc·flock·종료 확인이나 물리 재개를 인증하지 않는다. CLI launcher와 solver는 호출하지 않았다.

| 원 탐침/대조 | 독립 재계산 결과 | 관문 |
|---|---|---|
| p2 1a: arm9 경로, arms=1, 실제 결과 표지 | resource, side=post, resume_ok=false | RESUME_NOT_ALLOWED |
| p2 1b: arm9 경로, arms=9로 함께 변경, 실제 결과 표지 | resource, side=post, resume_ok=false | RESUME_NOT_ALLOWED |
| p2 1c: 정직 arm1 경로·결과 표지 | resource, side=post, resume_ok=false | RESUME_NOT_ALLOWED |
| p2 2a: 정직 GU, 요약 rc1 = 끝 rc1 | runner_rc, resume_ok=false | RESUME_NOT_ALLOWED |
| p2 2b: GU 요약 rc0 ↔ 끝 rc1 | group_unconfirmed, resume_ok=false | RESUME_NOT_ALLOWED |
| p2 2c: GU 요약 timeout/null ↔ 끝 None/1 | group_unconfirmed, resume_ok=false | RESUME_NOT_ALLOWED |
| p4 정직 RUNNER_RC/L01/rc1 + Traceback | runner_rc, resume_ok=false | RESUME_NOT_ALLOWED |
| p4 TIME_LIMIT/L02로 이름 변경 | timeout, resume_ok=false | RESUME_NOT_ALLOWED |
| p4 TIME_LIMIT/zzz로 이름 변경 | timeout, resume_ok=false | RESUME_NOT_ALLOWED |
| 정직 timeout/-9 끝 + timeout/null 요약, 읽힌 빈 로그 | timeout, resume_ok=true | 허용 |
| 정직 signal/-9 끝 + signal/null 요약, 읽힌 빈 로그 | signal, resume_ok=true | 허용 |
| 정직 GU/rc0 끝·요약, 합성 cleanup 확인 | group_unconfirmed, resume_ok=true | 허용 |

12건 모두 result 행이 실제 커밋됐고 재개 관문 호출 자체는 원장 바이트를 바꾸지 않았으며 마지막 Git 상태는 clean이었다. F2/F3의 위조 입력을 거부하는 결속은 이 실경로에서도 살아 있다. 원인 문자열 `timeout`만 보고 자격을 추론하면 안 된다. 위 L02/zzz는 원인이 timeout으로 남아도 자격은 false다.

