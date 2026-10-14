# LHS214 실행 증거 독립 대조

검토 핀: `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`. 아래 `E/`는 `submitted/lhs214_run_evidence_1014_1520/`, `P/`는 그 아래 `net194_1087a9b2f/`, `S/`는 `netsupp20_1087a9b2f/`다. 원본 60파일을 읽고 SHA256 목록을 남겼다. 원본·실행 코드는 바꾸지 않았고 생산/솔버 재실행도 하지 않았다.

재현: 저장소 작업 디렉터리에서 `& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 'lhs214_failures_review_20261014/probes/evidence_audit.py'`. 결과: `evidence/evidence_recomputed.json`. TSV는 원래 값과 ID를 그대로 읽어 JSON/로그/계획 큐와 대조했다. 이 검토에서 생성한 JSON은 입력 원본을 대체하는 영수증이 아니다.

## 결론과 증거 강도

현재 자료는 **214건을 같은 봉인 코드에서 한 번씩 시도했고, 200건 완료·14건 게시 차단되었다**는 설명과 일치한다. 봉인 감사 rc 0과 다시 읽기 rc 1은 모순이 아니다. 전자는 실행 코드/기록 무결성, 후자는 등록 집합 전체의 게시·완료 조건을 검사한다. 이 자료만으로 현재 214건의 v1.3 완성·배포를 승인할 수 없다.

제출된 lhsx_054 진단의 FULL Physics 이온 증서에는 이미 `over_conduction_guard / sigma_ratio > 1.5`가 명시되어 있다. 잔차·전류 보존 기준도 통과했다. 그러므로 **진단 한 건의 메커니즘은 확인됨**으로 수정할 수 있다. 그러나 나머지 13건에 동일 가드가 걸렸다는 것과 진단이 원 생산 입력·코드에 바이트 단위로 묶인다는 것은 현재 아카이브로 독립 확정할 수 없다.

## 재계산한 집계

| 관측 | production194 | supp20 |
|---|---:|---:|
| plan.queue 고유 ID / progress 행 | 194 / 194 | 20 / 20 |
| done / failed | 186 / 8 | 14 / 6 |
| cohort별 done | lhs130 + lhsx56 | lhss14 |
| audit 사례/SEALED/merged same | 194/194/194 | 20/20/20 |
| audit generation g2 / null | 186 / 8 | 14 / 6 |
| reread 고유 사례 / 누락 | 186 / 8 | 14 / 6 |
| reread 실패 meta 검사 / 사례 K1–K7 실패 | 2 / 0 | 2 / 0 |
| 관측 프로세스 고유 수 / final=true | 970 / 970 | 100 / 100 |
| 관측 worker / network_solver / other | 194 / 194 / 582 | 20 / 20 / 60 |
| completed_attempts / stage_binding.attempts | 186 / 186 | 14 / 14 |

모든 214행은 attempt=1, run=1이고 신호 칸이 비었다. 진행 로그의 194+20 완료 통지 ID, outcome, rc는 각각 progress.tsv와 완전히 같다. audit JSON 사례의 record_status와 TSV도 progress와 일치한다. reread의 읽은 ID는 progress done 집합과 정확히 같고 missing은 failed 집합과 정확히 같다. `n_fail=2`는 실패 침대 2개를 뜻하지 않고 M2와 M3 검사 두 개를 뜻한다.

근거: `P/progress.tsv:1`, `S/progress.tsv:1` 전 행, `E/net194_run_1014_1431.log:225`, `E/netsupp20_run_1014_1502.log:50`, 양쪽 `seal_audit.json $.cases[*]`, `$.import_observation.processes[*]`, `$.import_observation.completed_attempts`, `$.import_observation.stage_binding.attempts`; `P/reread.json:41,60,44373`, `S/reread.json:26,43,3412`. 상세 재계산 위치는 `evidence_recomputed.json $.batches`.

각 사례에 최종 관측 프로세스가 정확히 5개 있으며 모두 manifest의 import_obs_run_id, run_no=1, attempt=1에 묶인다. 30개 관측 소스 경로가 봉인 32파일 안에 있다. 완료 사례의 stage_binding expected/observed 사전은 전부 같다. 실패 14건은 completed_attempts·stage_binding 집계에 들어가지 않는 것이 현재 구현의 의미이며, 이것을 누락된 완료 증거라고 부르면 안 된다. 실패건 자체에는 worker+network_solver+기타3의 final 관측 항목이 있다. 단 이들은 감사 JSON에 담긴 2차 요약이며 원 import_obs 로그가 없어 원 관측 파일을 다시 파싱하는 독립 감사는 수행하지 못했다.

## 실패 14건: 공통 직접 원인과 수치 하위 원인을 구별

14건 모두 `failed/<case>/network_attempt.json`의 `$.failure_kind='solver'`, `$.reason`이 동일한 Physics ionic solve_failed 게시 전 검증 실패다. `$.solver_status`와 `$.latest_attempt_status`는 failed, `$.active_status='none'`, `$.active_network_run_id=null`, `$.previous_generation_kept=false`. code_sha도 핀과 같다. 각 worker의 시도 수 1, seal.record_sha와 audit의 record_sha 일치, 시작/끝 fp·git sha 일치다. 실패 로그는 개별 worker 상태와 같은 실패를 기록한다.

모든 worker stage_plan의 Network Solver는 **rc=0, ok=false**, 이어서 Network Merge / Stage E가 rc=1이다. 외부 worker rc=1을 솔버 프로세스가 rc=1로 종료했다는 뜻으로 쓰면 부정확하다. Parse·Contact·Coverage 단계는 모두 rc0/ok true다. 로그의 `physics v2 판정 {'ok':1}`은 Coverage 상태이며 network Physics 성공을 뜻하지 않는다. 표의 벽시간은 worker의 monotonic wall_s다.

| ID | progress 행 | audit TSV 행 | wall_s | peak_rss_mb | 확정 가능한 하위 원인 |
|---|---:|---:|---:|---:|---|
| lhsx_051 | P:36 | P:182 | 71.20 | 896.5 | generic Physics ionic solve_failed |
| lhsx_053 | P:46 | P:184 | 65.67 | 878.6 | generic Physics ionic solve_failed |
| lhsx_054 | P:23 | P:185 | 70.27 | 911.0 | 생산 기록은 generic; 별도 진단은 q 상한 가드 |
| lhsx_060 | P:92 | P:191 | 167.53 | 1334.4 | generic Physics ionic solve_failed |
| lhsx_061 | P:165 | P:192 | 209.94 | 1447.3 | generic Physics ionic solve_failed |
| lhsx_062 | P:49 | P:193 | 160.90 | 1458.8 | generic Physics ionic solve_failed |
| lhsx_063 | P:54 | P:194 | 87.16 | 980.4 | generic Physics ionic solve_failed |
| lhsx_064 | P:180 | P:195 | 176.18 | 1159.2 | generic Physics ionic solve_failed |
| lhss_001 | S:6 | S:2 | 72.81 | 1050.0 | generic Physics ionic solve_failed |
| lhss_003 | S:15 | S:4 | 65.29 | 843.7 | generic Physics ionic solve_failed |
| lhss_008 | S:10 | S:9 | 79.62 | 1012.6 | generic Physics ionic solve_failed |
| lhss_009 | S:21 | S:10 | 102.80 | 1070.8 | generic Physics ionic solve_failed |
| lhss_011 | S:2 | S:12 | 29.56 | 527.8 | generic Physics ionic solve_failed |
| lhss_014 | S:20 | S:15 | 121.82 | 1937.9 | generic Physics ionic solve_failed |

동일한 구조의 정확한 JSONpath: 각 `worker.json $.attempts[0].stage_plan.stages[3]`와 `[4]`, `$.attempts[0].seal`, 각 `network_attempt.json $.reason`. 예: `P/failed/lhsx_054/worker.json:112` 및 `:117`, `S/failed/lhss_011/worker.json:112` 및 `:117`. 각 개별 파일 원문과 대조 결과는 `evidence_recomputed.json $.failures`에 보존했다.

요청서의 RSS 범위 0.88–1.94GB는 수정 필요: 기록상 전체 실패 최소는 lhss_011의 **527.8MiB**, 최대는 lhss_014의 **1937.9MiB**다. 계산은 `ru_maxrss / 1024`이고 source `scripts/run_network_194_parallel.py:2211`은 이것이 프로세스+기다린 자식 중 최대이며 트리 합계가 아님을 명시한다. rc0의 망 프로세스 이후 내용 검증 차단이라는 관측은 직접 OOM 종료를 지지하지 않는다. RSS 한 숫자만으로 시스템의 메모리 문제를 절대 배제할 수 있다고 확대하면 안 된다.

## lhsx_054 진단의 확인 가능한 수치

`E/diag_lhsx054/network_conductivity_physics.json:23` status=`over_conduction_guard`; `:24` reason=`sigma_ratio > 1.5`; `:48` attempts[0].outcome=`pass`; krylov_info=0. 같은 증서의 I_bottom=106.85001549443174 (`:30`), delta_V=1, g_to_q=0.014384959999999995 (`:38`). 따라서 미게시 진단 q = I_bottom / delta_V × g_to_q = **1.5370331988867802**. conservation_rel=6.195679060858629e-11, residual_rel=9.071411744344477e-11 (`:32–33`), 각 허용치1e-6 이하. n_boundary_overlap=0, n_area_physics_unavailable=0. 이는 계산 인증 뒤 FULL의 모형 가드가 값을 거부했다는 구체적인 증거다.

같은 JSON의 $.sigma_full=null, $.sigma_full_status=not_computed, $.sigma_full_reason=solve_failed, $.ionic_status=failed는 상위 분류가 하위 증서보다 덜 구체적임을 보여준다. Hertz JSON $.sigma_full=0.66147876이며 Physics 전자·열은 computed다. Physics CF=2.04783126/model_over_conduction, 협착-only는 zero_resistance_requires_contraction이다. 이들은 FULL q 가드와 별개인 기존 모델 상태다.

단독 stdout에는 마지막 출력 파일 경로와 cg/spsolve 과정이 있으나 명령·종료코드·실행 핀을 기록한 wrapper는 없다. diag 입력 atoms.csv/contacts.csv, 입력 digest, network_conductivity_dual.json, network_provenance.json도 제출되지 않았다. 최초 생산 worker의 contacts=207740과 stdout의207740이 같지만 바이트 동일성을 증명하지 않는다. 따라서 이 진단 q를 원 생산 레코드에 복사하거나 14건 모두를 미리 full_over_conduction으로 확정하면 안 된다.

## 핀·봉인·입력·영수증

양쪽 manifest git.sha·seal.code_fp·code_hashes·handover_code_hashes는 같다. code_hashes 32개를 현재 검토 핀에서 받은 `source/` 파일의 바이트로 모두 SHA256 재계산하여 일치했다. 정렬한 해시 사전의 JSON SHA256로 다시 만든 code_fp도 **e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71**이다. manifest의 SHA256은 reread가 기록한 값과 일치한다. 두 handover 도구 해시도 실제 source와 일치한다. 사후 영수증이 기록한 별도 도구5개도 source 바이트와 일치한다.

계획 큐에서 `(case,cohort)`를 cohort,case 순서로 정렬해 `case\tcohort\n`를 SHA256하면 production194=`a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf`, supp20=`991cf1150b183f64bc69926a8b3e7c05453ec47e13b89ba3a6ad2fd2c981c694`. manifest·로그 INPUT_DIGEST_JSON과 같고 핀 source `run_network_194_parallel.py:1003` 등록과도 같다. raw_sha256_table_sha256와 cohort_tsv_sha256은 로그↔manifest↔영수증 간 대조는 되었으나 원 수확 JSON/raw/코호트 TSV가 이 실행 증거에 없어 원 바이트로 다시 계산하지 못했다.

`E/supp20_postrun_receipt.json`은39/39 체크 true·rc0이며 파일 이름에 postrun이 들어가도 **$.scope='launch'** (`:341`)이다. 실행 후 만들어졌다는 사실이 결과 완료 영수증으로 성격을 바꾸지 않는다. 이 파일의 $.manual 세 항목은 verified_by_tool=false (`:259–270`)이며 fast16/real4 결과와 저자 발사 승인 자체를 검증했다고 읽으면 안 된다. 실제 preflight log/receipt는 경로·해시만 존재 (`:247–253`)하고 원문은 제출되지 않았다.

## Q5: 그 밖의 해석 주의점

1. 기존 봉인 감사는 실패 상태를 별도의 bad로 더하지 않는다. source `run_network_194_parallel.py:2994`의 rc 정의, `:3035`의 generation null 제외, `:3069` 부근 bad 합계가 이 의미를 보여준다. 현재 audit0/reread1은 예상 가능한 실패 보존 상태이고 숨겨진 성공 판정 충돌은 아니다. `reread` M2/M3 실패를 릴리스 과정에서 무시하면 문제다.
2. 시간은 단위/시계가 혼재한다. production progress first start14:31:19 → last end15:01:52는 **1833초(30분33초)**, supp15:02:15→15:07:38는 **323초(5분23초)**. 합2156초(35분56초), 중간23초 포함 전체 **2179초(36분19초)**다. 로그 printed wall_h는0.476+0.084=0.560h(33분36초)이다. source는 elapsed에 time.monotonic, 날짜에 now_iso를 쓰고 종료 증거 생성 후 end timestamp를 기록한다 (`:2181,:2209,:2221,:2329`). 차이의 원인을 이 자료만으로 특정할 수 없다. '약40분'은 운영 추정으로는 가능하지만 재계산 실측40분이나 시간 상한 증거로 쓰지 말 것. 동시 수16/9는 TSV 반열린 구간 중첩으로도 일치한다.
3. MODEL_BELOW_CONTINUUM_BOUND는 q>1의 동의어가 아니다. reread에서 Physics 해당 사례62개 중 q<1도 있다. 핀 tau_flux.py:1133–1136의 판정은 f=q·L_gap/L_mc와 t²=phi_mc/f <1이다. 제출 본문의1.04–1.48은 높은 q 예시로는 맞지만 해당 상태 전체 범위라는 표현이면 부정확하다. 'SE가 많은 사례에 집중'은 별도 조성 원자료 없이 재검증하지 않았다.
4. 현재 성공한200건의 reread K1–K7은 모두 통과했다고 요약되어 있다. 하지만 canonical dual/full_metrics/provenance와 status.json/metrics_flat.csv가 없어 그 관문을 원 파일에서 독립 재실행하지 못했다. 성공200건을 수치적으로 독립 재계산했다고 보고하지 않는다.

## 현재 아카이브에 없는 자료와 Q4의 최소 새 증거

없는 자료: 양쪽 원 ROOT의 `runs/*.json`, `import_obs/log/*`, 모든200 성공 사례 worker/log 및 모든214 원 case record/status.json·metrics_flat.csv·parallel_cases.tsv, canonical `network_conductivity_dual.json/full_metrics.json/network_provenance.json`, 두 dry-run 완료 영수증과 그에 해시로 묶인 전체 로그, fast16/real4 전체 결과, 손 대조 기록·발사 승인 원문, 원 수확/코호트 TSV/raw 입력, pressure 기록, v1.3 handover/columns/tau_provenance/excluded, 릴리스 감사/묶음 영수증. 제출 archive는 실패 검토용 발췌이므로 이 결손 자체를 생산 코드 결함으로 판정하지 않는다. 다만 전면 재검증·배포 완료 증거로는 불충분하다.

재발사 증거 제안(다른 코드/계약 검토와 합쳐 적용):

- 먼저 14건 각각에 대해 새 분류가 진짜 인증 통과 후 q>1.5인지 구체적 증서로 식별. 원 입력 digest, 코드 핀, mode/channel/branch/role, candidate q, residual/conservation, status/reason을 같은 실행에 묶어 보존. 기존 모호한 attempt 문자열을 근거로 일괄 상태 변환하지 말 것.
- q=1.5와 바로 위/아래, 인증 실패·예외·비양수/비유한 전압·상한/경계 중첩 등 경로가 새 예외로 유입되지 않음을 보이는 양성/음성 시험. Physics/H0/H12 및 일반/stop 경로와 τ/인계/릴리스/화면의 동일 의미 확인은 계약 담당 검토에 따른다. 무영향 수치가 같다는 증거는 원 수치 canonical 비교로 제시.
- 새 승인 핀에서 fast16+real4, 두 등록 §3 새 code_fp, 두 ROOT의 `--dry-run --observe-imports --preflight-receipt` 전체 로그+완료 영수증과 검증, 등록 §2 손 대조, 새 발사 승인. 과거 ROOT는 그대로 보존.
- 194+20 **전부** 새 ROOT에 실행. plan/ID/입력 지문/세대/관측/코드 봉인 동일성, 모든214 시도 기록·원 import 로그, 완료 후 audit0 **그리고** reread `--expect-set production194`/`supp20` 각각0, missing/extra0 및 read_n=194/20. 새 채널 NOT_COMPUTED를 정상 게시로 허용하더라도 등록 ID 누락을 면제하지 말 것.
- postrun 입력 영수증의 launch scope와 별도로 실제 handover/릴리스 관문 결과·canonical source 해시 및 pressure 증거를 보존. Hertz 주 값 거부 시 릴리스의 명시적 정책을 검증. 실패했던14개 Physics만 공란+정확한 사유가 되는지, Hertz와 다른 채널·분기 값/상태가 살아 있는지 행별 대조표를 포함.

새 분류의 예외는 증서로 입증된 하위 사유에만 열고, 성공 봉인/입력 영수증을 배포 완료로 대신하지 않는 것이 핵심이다.
