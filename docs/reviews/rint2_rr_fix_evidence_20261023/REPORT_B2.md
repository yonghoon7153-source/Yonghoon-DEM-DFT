# 묶음 B″ 보고 — 생산 봉인 원천 (러너 조립만) · venv · `.venv/` · 메모리 · 위조 한정 · 엄격 검사 셋 (Rint ② RR · 10-26)

> 원문 = 작업 트리 에이전트의 마지막 보고입니다.  하위 에이전트 정책으로 보고 파일 쓰기가 막혀 메인이 옮겨 적습니다.
> 지시 = 1저자 10-26 *"다 권고대로 해도 되고 kgy에서 돌리면될듯"* = 묶음 B 보고 `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_B.md` §13 결정 1–8 의 권고 → Q1–Q6.
> 형식 = `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF.md` §보고 · `docs/reviews/rint2_rr_fix_evidence_20261023/BRIEF_B.md`.
> 숫자와 전칭은 에이전트 실행 출력입니다 (범위와 시험 판을 같이 적었습니다 · `SELF-124`).
>
> **메인 반입 (10-26 밤)** = 에이전트 가지 `rr-fix-b2` 의 9 커밋을 메인 `d417dbd11` 위에 `cherry-pick -x` (충돌 0 · 원장은 자동 병합).  아래 본문의 커밋 번호는 **메인 번호로 바꿔 적었습니다** (에이전트 가지 번호는 원격에 없어 적지 않는다 · 커밋 메시지 끝의 `cherry picked from` 줄이 대응을 담는다).  시험 수는 에이전트 트리 (시작 `ce1be4cdc`) 의 값이고, 메인에서는 전체 게이트로 다시 돈다.
>
> **메인 게이트 1 회차 (10-26 밤)** = 118 통과 · **1 실패** — `scripts/test_rint_receipts.py` A0 (주 솔브가 `rint=` 를 `**_kw3` 묶음으로 받게 된 뒤 AST 판독기가 직접 키워드만 봐서 주 솔브를 못 셌다 → 주 솔브 변이 B1 · B2 두 건이 조용히 빠졌다 · 생산 코드는 바뀐 것 없음).  시험 판독기 · 변이를 `dict(...)` 묶음까지 따라가게 고침 (A00 판독기 자기 점검 2 · A0b 조립만 출구 = 같은 `_kw3`) → 고치기 전 99 통과 · 1 실패 → 뒤 **105 통과 · 0 실패** (주 솔브 변이 = exit 4 · `STEP3_INTERFACE` · `electronic_main`).

묶음 B″ 를 마쳤습니다.  이제 사슬이 SV 끝 그래프의 생산 봉인 원천을 갖습니다.  같은 러너 · 같은 env 로 payload 를 조립만 다시 돌리고, 그 지문을 증서 지문과 대조합니다.

끝 트리 회귀는 Python 3.11.17 에서 전부 rc 0 입니다.  kgy 판 (3.8.20) 11 묶음도 통과합니다.

변이 첫 판에서 시험 빈자리 넷을 찾았습니다 (조립만 기록의 칸 안 값 검사).  시험 SGF 를 보태 넷 다 잡았습니다.

| 항목 | 내용 |
|---|---|
| 가지 · 커밋 | 에이전트 `rr-fix-b2` · 시작 `ce1be4cdc` (메인 · 묶음 B 반입) · 커밋 9 → 메인 `fafd95693` … `0315b085a` |
| 하지 않은 것 | push · fetch · `scripts/check_all.sh` · GPU · 킷 풀이 (SBE · DBE) |
| 봉인 32 파일 | `scripts/run_network_194_parallel.py` 의 CODE_FILES (AST 로 읽음) ∩ 바뀐 파일 14 = 0 |
| 웹앱 | 바꾸지 않았습니다 (§9) |

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (claimed · 확인 = Codex) | 닫지 않는 것 |
|---|---|
| 결정 1 — RR1-01 의 생산 원천 (D1).  Q1 (가) 러너 조립만: payload `dccd4b323` · 러너 `aba86a2a2` · 사슬 `75a1f3411` | 결정 2 — 위조 한정 (D2).  1저자 Q2 = 한정 그대로 (새 기전 없음) · Codex 회차 ② 질문 (등록 R §13-3 B2-Q1) |
| 결정 3 — 메모리.  Q3 = 쪼개기 없음 · 추정 기록 · 런 전 확인 줄 (kgy 명령 문서 `541e2bfa0`) | 실침대 비용 · 메모리 = 추정 (픽스처만 실측 · §5) |
| 결정 4 — 러너 venv.  Q4 = 사슬이 `MPM_NO_VENV=1` 을 준다 (`930e9e2ac`) | 생산 팔 payload 의 환경 단위를 런마다 대조하는 것 (선택지 3 · 안 고름 · 원천 런만 자기 환경 단위를 대조) |
| 결정 5 — `.venv/`.  Q5 = `.gitignore` (`fafd95693`) | 묶음 C · 등록 R HOLD · R 에 쓰는 S0 보고 재생성 (끝 핀 · §11) · 회차 ② 조건 |
| 결정 6 · 7 · 8 — 엄격 검사 셋.  Q6 = 받아들임 (코드 변경 없음 · 지키는 시험 확인 §7 · 등록 R `e059c4906`) | |

## 1. 커밋

| 항목 | 커밋 (메인) | 무엇 |
|---|---|---|
| Q5 | `fafd95693` | `.gitignore` 에 `.venv/`.  러너가 찾는 venv 자리 `$SCR/../.venv` 가 고정 트리를 dirty (`CODE_PIN_MISMATCH`) 로 만들지 않는다 |
| Q4 | `930e9e2ac` | 사슬이 런마다 러너 env 에 `MPM_NO_VENV=1` 을 준다 (`RUNNER_EXEC_ENV` · 부모 셸 값과 무관).  payload = 사슬 프로세스의 python |
| Q1 1/3 | `dccd4b323` | payload `--step3-cjunc-graph-only`.  주 풀이 인자를 한 번 만들고 (`_kw3`) 같은 인자로 `step3_sigma.solve_sigma_z(cjunc_graph_only=True)` → 봉인 원천 기록 (`run_contract.cjunc_graph_only_record` · 칸 고정 = σ 칸 없음 · `.part` → replace) → exit 0 (CG · 증서 · σ · 매니페스트 없음).  입구 거부 (`FLAG_WITHOUT_CJUNC` · `GRAPH_ONLY_RASTERIZE_ONLY`) · 구조화 종료 (`S2_CJUNC_GRAPH_ONLY|ASSEMBLE|RECORD|WRITE|`).  step3 조립만 반환에 `bind` (`step3_conv_cert.bind_record`) · 환경 단위 = `run_contract.env_unit_now` (사슬 `env_record` 와 같은 함수) |
| Q1 2/3 | `aba86a2a2` | 러너 `CJUNC_GRAPH_ONLY=1`.  값 · CJUNC 짝 = 발사 전 거부 · 영수증 선택 칸 `cjunc_graph_only` (켬일 때만 · 옛 digest · OUTDIR 그대로) · payload 플래그 + 태그 `_cjgo` · 출력 `cjgraph_<팔>.json` (팔 JSON `p2_*` 이름꼴 밖) · 있으면 거부 (캐시 없음 · 옛 파일 그대로) · 꼴 검사 뒤에만 옮김 · 봉인 · 판정 · 원값 없음 · 조립만 영수증은 팔을 증명하지 않음 (`RCPT|cjunc_graph_only|`) · 규율 검사 `_RUNNER_AXES` |
| Q1 3/3 | `75a1f3411` | 사슬 `RunnerGraphSource` · 기본 `SV_GRAPH_SOURCE` = `RUNNER_GRAPH_SOURCE` · `runner_env_delta` (생산 팔과 같은 함수) · 대조 순서 (§8) · 예측 · 판정 · 다시 판정이 각자 다시 조립 · 기록 `sv_graph_source` · `verdict_graph_src.json` |
| Q3 | `541e2bfa0` | kgy 명령 문서 §3.  원천 런 · venv · 메모리 설명 + 런 전 확인 줄 (`free -g` · 기록만) |
| Q2 + Q6 | `e059c4906` | 등록 R.  머리 줄 (B″) · B6 줄의 "결정 필요" 철회 표지 · §5-6 SV 행 (생산 원천 · 위조 한정 · 엄격 검사 셋 받아들임 · 시험 목록) · §13-3 B2-Q1 |
| 변이 보강 | `cc60153aa` | `scripts/test_ca_ext_b6.py` SGF.  조립만 기록 꼴을 칸 안 값마다 29 꼴로 깨 본다 (시험만) |
| 원장 | `0315b085a` | `docs/reviews/findings.json` RR1-01 · RCA2-04 note 덧붙임 (§10) |

## 2. 시험 수 — 고치기 전 → 뒤

고치기 전 = 그 항목 직전 코드에 새 시험을 얹어 돌린 값입니다 (Python 3.11).

| 항목 | 묶음 | 고치기 전 | 뒤 |
|---|---|---|---|
| Q5 | `scripts/test_rint_r_chain.py` Y13 | 실패 (옛 `.gitignore` → 고정물 clone dirty True · `CODE_PIN_MISMATCH`) | 통과 |
| Q4 | test_rint_r_chain Y14 | 실패 (러너 env 의 MPM_NO_VENV = 부모 셸 그대로) | 통과 |
| Q4 | `scripts/test_rint_r_chain_e2e.py` E11a · E11b | 1/2 (E11a 실패 = 러너 자리의 미끼 venv 를 켬) | 2/2 |
| Q1 1/3 | `scripts/test_ca_ext_b6.py` SG1–SG9 | 0/9 (모르는 플래그) | 9/9 |
| Q1 2/3 | `scripts/test_ca_ext_runner.py` N0 · N9 · N11 | 8 통과 / 16 실패 | 24/24 |
| Q1 3/3 | test_rint_r_chain RG08–RG13 | 7/13 (RG08–RG13 실패) | 13/13 |
| Q1 3/3 | test_rint_r_chain_e2e E12 | 0/1 (`RunnerGraphSource` 없음) | 4/4 |
| 변이 보강 | test_ca_ext_b6 SGF0 · SGF1 | 지금 코드 = 통과 · 변이 사본 넷 (§6 계약 칸 안 값) = SGF1 실패 | 2/2 |

- Q4 의 고치기 전 사본은 git 밖이라 Y13 도 실패합니다 (환경 탓).  Q5 의 증거는 Q5 커밋과 §6 의 작업 트리 변이입니다.
- Q1 2/3 의 고치기 전 판에서 N11g 는 통과했습니다.  옛 러너의 env 관문이 모르는 손잡이를 죽였기 때문입니다.  그래서 N11g 혼자는 판별하지 않습니다 (판별 = N11a–f · h–j).

## 3. 회귀 — 시작 `ce1be4cdc` → 끝 (에이전트 트리)

환경 = Python 3.11.17 · numpy 2.4.6 · scipy 1.17.1 · BLAS 1 · nice 19.  전부 rc 0.

| 묶음 | 시작 `ce1be4cdc` | 끝 |
|---|---|---|
| `scripts/test_rint_r_chain.py` | 276/276 | 284/284 |
| `scripts/test_rint_r_chain_e2e.py` (실제 러너 · payload) | 20/20 | 26/26 |
| `scripts/test_ca_s0_census.py` | 163/163 | 163/163 |
| `scripts/test_carbon_junction.py` | 466/466 † | 466/466 |
| `scripts/test_ca_ext_b6.py` | 490/490 | 501/501 |
| `scripts/test_ca_ext_runner.py` | 128/128 | 142/142 |
| `scripts/test_ca_ext_verdict.py` | 31/31 | 31/31 |
| `scripts/test_ca_ext_z1.py` · `scripts/test_ca_ext_z3.py` | 95 · 84 | 95 · 84 |
| `scripts/test_ptfe_face_alpha.py` | 242/242 | 242/242 |
| `scripts/test_step3_target_cert.py` 빠른 판 | 264/264 † | 264/264 |
| `scripts/test_step3_conv_cert.py` | 30/30 † | 30/30 |
| `scripts/run_contract.py --selftest` | 124/124 | 124/124 |
| `scripts/step3_sigma.py --selftest-rint` · `--selftest` | PASS · PASS | PASS · PASS |
| `webapp/test_ca_ext_labels.py` | 92/92 | 92/92 |
| `webapp/test_rint_explainer_page.py` | 71/71 | 71/71 |
| `webapp/test_rint_scope_labels.py` | 31/31 | 31/31 |
| `scripts/check_method_discipline.py` | 0 오류 · 경고 17 † | 0 오류 · 경고 17 |
| `scripts/check_method_discipline.py --selftest` | 128/128 † | 128/128 |

- 시작 칸은 `ce1be4cdc` 의 git 밖 사본 (scripts · docs · webapp) 에서 돌렸습니다.
- † = 저장소가 필요한 묶음입니다 (기준 모듈을 git 커밋에서 읽음 · CI yml).  사본에서는 그 이유로 실패했습니다.  그래서 작업 트리에 `ce1be4cdc` 판 13 파일을 잠시 꺼내 다시 돌렸고, 그 값을 적었습니다 (뒤에 HEAD 로 되돌림 · `git status` 빈칸).
- 끝 칸은 Q2 + Q6 커밋 (메인 `e059c4906`) 의 트리입니다.  단 b6 · 규율 검사는 변이 보강 커밋 (메인 `cc60153aa`) 에서 돌렸습니다 (그 커밋은 b6 시험 파일만 바꿈).  원장 커밋 (메인 `0315b085a`) 은 원장 JSON 만 바꿉니다.
- 늘어난 수: 사슬 8 = Y13 · Y14 · RG08–RG13 · e2e 6 = E11a · E11b · E12a–d · b6 11 = SG1–SG9 · SGF0 · SGF1 · 러너 14.

## 4. kgy 판 — `scripts/check_kgy_py38.sh`

Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · 트리 = 변이 보강 커밋 (메인 `cc60153aa`) · 11/11 통과.

| 묶음 | 결과 |
|---|---|
| run_contract | 124/124 |
| step3 rint | PASS |
| ptfe_face_alpha | 242/242 |
| carbon_junction | 466/466 |
| ca_ext_b6 | 501/501 |
| ca_ext_runner | 142/142 |
| rint_r_chain | 284/284 |
| rint_r_chain_e2e | 26/26 (E12 포함 · 3.8 원천 런의 환경 단위 3.8 = 사슬) |
| step3_target_cert 빠른 판 | 264/264 |
| step3_conv_cert | 29/29 (3.8 판의 수 · 기존 kgy 단계와 같음) |
| ca_s0_census | 163/163 |

## 5. 비용 — 픽스처 실측 · 실침대 추정

| 자리 | 값 | 출처 |
|---|---|---|
| 원천 런 하나 (실제 러너 + payload 조립만 · DBE 픽스처 · e2e E12) | 3.11 세 번: 벽시계 2.58–2.97 s · payload STEP3 0.047–0.063 s · 조립 0.021–0.026 s · 최대 RSS 99,572–99,812 kB.  3.8 한 번: 2.14 s · 0.048 s · 0.018 s · 96,856 kB | E12 단독 · 전체 e2e 두 번 · kgy 판 e2e |
| 같은 SV 런 전체 (원천 런 포함) | 3.11 5.8–6.6 s · 3.8 4.8 s | 같음 |
| payload 조립만 (b6 SG · 다리 덩어리 픽스처) | STEP3 0.045 s · 조립 0.024 s · 최대 RSS 189,672 kB | 끝 회귀 b6 (전체 실행 중 값) |
| 러너 관문.  실제 러너는 원천 런마다 규율 검사기를 한 번 돈다 (시험 심은 건너뜀) | 이 컨테이너 25 s (`check_method_discipline.py` 저장소 판) · kgy 미측정 | 끝 회귀 |
| 실침대 지문 (SBE vox 0.15 · n_dof 26,438,766 · 간선 ≤ 79 M) | 지문 하나 ≈ 70–85 s · ≈ 6 GB 일시 (**추정**) · SV 팔마다 2–3 개 | 묶음 B 보고 §8 |
| 실침대 payload 의 CG 밖 부분 (raster · 원장 · 조립) | 미측정 | — |
| 단계마다 원천 런 수 | 계획 `sv_cf_scope` = `R_j0` → SV 모서리 4 → 원천 런 4 · `all3` → 12 · 예측 · 판정 · 다시 판정이 각자 | 사슬 `Predict._sv_on` · RG08 (예측 4 + 판정 4) |

- 픽스처 시간은 러너 관문 (심) 과 인터프리터 시작이 지배합니다.  실침대 비용의 근거가 아닙니다.
- 메모리 (1저자 Q3) = 쪼개기 없음.  런 전 확인 줄은 kgy 명령 문서 §3 에 있습니다 (`free -g` · 기록만 · 문턱 숫자 등록 없음).

## 6. 변이 표

규칙 줄 하나를 되돌린 사본에, 그 규칙을 잡아야 할 시험 부분집합을 돌렸습니다 (scripts = 사본 · docs = 링크).

- 대조 (변이 없음 · 같은 사본 환경): 사슬 RG08 · RG10 · RG11 · RG12 · Y14 5/5 · e2e E11 · E12 6/6 · 러너 N11 14/14 · b6 SG 9/9 가 통과했습니다.
- 사슬 Y13 은 사본이 git 밖이라 대조에서도 실패합니다 (환경 탓).  그래서 Q5 변이는 작업 트리에서 돌렸습니다.

| 묶음 | 변이 | 잡은 시험 |
|---|---|---|
| 사슬 원천 (Q1 3/3) | 환경 단위 대조 끔 | RG10 (go_env) · E12c |
| | 결합 대조 끔 | RG10 (go_bind) · E12d |
| | 출력 정확히 하나 · 이름 검사 → 하나 이상 | RG10 (go_two) |
| | 기록 꼴 검사 끔 | RG10 (go_form) |
| | 러너 rc 검사 끔 | RG10 (go_rc · 사유 'rc 3' 없음) |
| | 지문 없음 (조기 반환) 검사 끔 | RG10 (go_none) |
| | 기본 원천 = None (옛) | RG08 |
| | 생산 팔 read_run 에 원천을 안 넘김 | RG08 (예측 원천 런 0) |
| | 판정 · 다시 판정의 기본 원천 없음 | RG08 · RG11 · RG12 |
| | 판정의 예측 다시 계산에 원천을 안 넘김 | RG08 · RG11 |
| | 원천 env 바탕의 축 이름을 안 지움 | RG13 |
| | 원천 env 에 `CJUNC_GRAPH_ONLY=1` 을 안 넣음 | RG08 · RG13 |
| | 다시 판정의 임시 폴더를 안 지움 | RG12 |
| | 팔 i > 0 의 ARM_LIST 를 안 넣음 | RG13 |
| venv (Q4) | 러너 env 에 MPM_NO_VENV 를 안 넣음 | Y14 · RG08 · E11a |
| 러너 (Q1 2/3) | 조립만 출력이 있어도 거부 안 함 (캐시) | N11e |
| | 옮기기 전 꼴 검사 끔 | N11h |
| | 조립만 런 끝의 exit 0 뺌 (봉인으로 진행) | N11d |
| | 조립만 영수증의 팔 증명 거부 끔 | N11i |
| | 보기에 payload 플래그를 안 넣음 | N11a · N11b · N11c · N11d |
| payload (Q1 1/3) | 조립만 뒤 exit 0 뺌 | SG1–SG6 등 |
| | step3 조립만 반환에서 bind 뺌 | SG1–SG6 등 |
| | 조립만 + rasterize-only 거부 끔 | SG8 |
| 계약 (Q1 1/3) | 기록 꼴의 env 값 검사 끔 | 첫 판 생존 → SGF1 |
| | cost 값 검사 끔 | 첫 판 생존 → SGF1 |
| | bind 값 검사 끔 | 첫 판 생존 → SGF1 |
| | graphs 꼴 검사 끔 | 첫 판 생존 → SGF1 |
| `.venv/` (Q5 · 작업 트리) | `.gitignore` 에서 `.venv/` 뺌 | Y13 (check-ignore rc 1 · dirty True · `CODE_PIN_MISMATCH`) |

- 합계: 변이 28 개 중 첫 판에 24 개를 잡았습니다.  생존 4 개는 계약의 칸 안 값 검사였습니다 (SG · N11 · RG10 은 정직한 실제 출력과 칸 빠짐만 밟았기 때문).  SGF 를 더한 뒤 28/28 입니다.
- 첫 판에서 Q5 변이를 사본에서 돌려 나온 "잡힘" 은 셈에 넣지 않았습니다.  변이 없는 대조도 같은 이유로 실패하는 환경 탓이기 때문입니다.  위 표의 Q5 행은 작업 트리 값입니다.

## 7. Q6 — 엄격 검사 셋 (받아들임 · 코드 변경 없음)

| 묶음 B 결정 | 내용 | 지키는 시험 |
|---|---|---|
| 6 | X3 이 (b) · (b′) · (c) 를 끊은 수 그대로면 거부합니다.  그 칸까지 0 으로 고친 일관 편집은 받습니다 (남은 한정) | `scripts/test_carbon_junction.py` QD7 ⑥ (b) · (c) · ⑥′ (b′) · QX35 ② |
| 7 | `k + kul ≤ ku` (아래 끝 새 칸 + 위 끝의 아래 끝 대비 새 칸 ≤ 위 끝 새 칸) | QX35 ④ (QDX · QD4 · QD2-1 — 위 끝 대비 새 칸 = 위 끝 − 아래 끝 + 1) · `scripts/test_ca_ext_b6.py` S8x5 (computed 끝 없는 기록) |
| 8 | ⑦ (위 끝 `n_sv_faces_cut` = 아래 끝) 을 X5 와 함께 앞으로 | b6 S8x5 (위 끝 = 아래 끝 + 1) · QX35 ③ |

- 세 묶음 다 끝 회귀에서 통과합니다 (carbon_junction 466/466 · b6 501/501).

## 8. 설계 · 한정 (Q1)

- 원천 런 = 같은 러너 · 같은 킷 뿌리 · 같은 런 env + `CJUNC_GRAPH_ONLY=1`.  env 는 `runner_env_delta` 로 만듭니다 (생산 팔과 같은 함수 · 사본 없음).  팔은 하나입니다 (팔 0 = ARMS 1 · 팔 i > 0 = ARM_LIST i).  새 폴더 · 캐시 없음.
- payload = 같은 주 풀이 인자 + 조립만.  기록 칸이 고정이라 σ 가 들어올 칸이 없습니다.  결합 칸 = 같은 입력 정체성.
- 사슬 대조 순서: ① 러너 rc ② 출력이 정확히 하나 (그 팔 이름) ③ 꼴 ④ 환경 단위 = 사슬 ⑤ 결합 = 그 런 주 증서 결합 ⑥ 지문 있음 ⑦ `ca_ext_svcf.graph_problem`.
- 지문 ≠ 증서이면 `CA_EXT_RECORD` 로 멈춥니다.  원천이 실패하면 미확인 → `SV_UNCHECKED` 입니다 (멈춤도 clear 도 아님).
- 예측 · 판정 · 다시 판정이 각자 다시 조립합니다.  RG11: 판정 때 원천 지문이 다르면 판정이 멈춥니다 (예측의 대조를 믿지 않음).  RG12: 다시 판정은 REVERIFY_SAME 이고, 원천 런이 넷 더 돌며, 판정 폴더는 그대로입니다.
- 원천 런 기록 = 단계 요약 `sv_graph_source` · 판정 `verdict_graph_src.json` (칸 = 이름 · 런 · 팔 · rc · 초 · 상태 · 사유 · 출력 이름 · sha256 · 비용 · 환경 단위 · σ 없음).  판정 JSON 밖에 있으므로 다시 판정의 바이트 대조와 무관합니다.
- 한정:
  - 위조 (Q2): 증서 칸 지문까지 원천 값으로 고친 편집은 못 가립니다.
  - 원천은 그 런과 같은 코드 · 킷입니다.  그 코드 · 킷 자체의 결함은 원천도 같이 갖습니다 (코드 · 침대 대조 = 단계 관문).
  - 환경 단위는 원천 런 것만 대조합니다.  생산 팔은 Q4 (MPM_NO_VENV) 로 구성상 같지만, 런마다 대조하지는 않습니다.
  - 판정 · 다시 판정의 원천 런에는 시간 상한이 없습니다 (예측은 그 단계의 `--max-hours` 안).
  - 다시 판정의 원천 기록은 화면에만 남습니다 (임시 폴더 · 판정 폴더에 쓰지 않음).

## 9. 문서 · 웹앱 고친 자리

| 자리 | 항목 | 무엇 |
|---|---|---|
| `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` | Q1 · Q2 · Q6 | 머리 줄 (B″) · B6 줄의 "결정 필요" 철회 표지 · §5-6 SV 행 (생산 원천 · 위조 한정 · 엄격 검사 셋 받아들임 · 시험 목록) · §13-3 B2-Q1 · 결과 0 건 · 새 합격선 숫자 · 새 멈춤 이름 없음 |
| `docs/reviews/rint2_kgy_commands_20261020.md` | Q1 · Q3 · Q4 | §3 설명 줄 (원천 런 · venv · 메모리) · 런 전 확인 줄 `free -g` (기록만) |
| 웹앱 | — | 바꾸지 않았습니다.  SV 줄 문구 "그래프 귀속 = 사슬 대조 (봉인 원천 · 없음 = SV_UNCHECKED)" (B6) 는 그대로 맞습니다 (화면은 대조하지 않고 생산자 기록만 보입니다).  다만 원천 실패도 `SV_UNCHECKED` 라는 말은 화면에 없습니다 (§12 결정 3) |
| `scripts/carbon_junction.py` CJUNC_QUALIFIERS | — | 바꾸지 않았습니다 (생산자 한정어 = 매니페스트 바이트) |

## 10. 원장

- `docs/reviews/findings.json` (메인 `0315b085a`) — note 덧붙임만입니다.  status · claimed_fixed_sha 는 그대로이고 새 ID 는 없습니다.  RR1-01: 생산 원천 배선 · 커밋 · 시험 · 한정 (위조 = Codex 회차 ② 질문).  RCA2-04: 닫는 조건의 원천 부분 · Q6 받아들임 · 지키는 시험.  (메인 반입 때 note 안의 에이전트 커밋 번호를 메인 번호로 바꿨다.)
- 에이전트가 실행한 검사: `check_review_findings` rc 0 · `--ban-sweep` 누수 없음 · `check_doc_refs` rc 0.

## 11. S0_SAME_FILES · 작업 트리

- `S0_SAME_FILES` 일곱 중 이 묶음이 바꾼 것은 둘입니다: `scripts/step3_sigma.py` (조립만 반환 bind) · `scripts/mpm_webapp_payload.py` (조립만 플래그).  그래서 R 에 쓰는 S0 보고 (단계 1 · 2) 는 끝 핀에서 다시 만들어야 합니다 (묶음 B 와 같은 요구).
- 사슬 코드 키에 드는 파일 (`scripts/rint_r_chain.py` · `scripts/run_contract.py` · 러너 등) 이 바뀌었으니 새 핀입니다.

## 12. 결정 필요 (고르지 않은 자리)

1. **[Q1 · 비용] 판정 · 다시 판정의 원천 재조립.**  지금은 예측 · 판정 · 다시 판정이 각자 원천 런을 돕니다 (`R_j0` = 4 · `all3` = 12).  실침대에서는 원천 런마다 러너 관문 (이 컨테이너 25 s) · payload 의 CG 밖 부분 (미측정) · 지문 2–3 개 (≈ 70–85 s · 추정) 가 듭니다.  권고 = 그대로 (판정은 단계 요약을 믿지 않는다) · 비용은 첫 실제 런의 원천 기록 (`cost`) 으로 다시 봅니다.
2. **[Q4] 생산 팔 환경 단위의 런마다 대조.**  지금은 원천 런만 대조합니다 (생산 팔은 MPM_NO_VENV 로 구성상 같음 · 매니페스트 `exec_env` 는 대조 안 함).  권고 = 그대로.
3. **[웹앱] SV 줄 문구** — "봉인 원천 · 없음 = SV_UNCHECKED" 를 "봉인 원천 · 없음 · 실패 = SV_UNCHECKED" 로 바꿀지.  권고 = 다음 웹앱 묶음 (`webapp/test_ca_ext_labels.py` W17 한 줄).
4. **[Codex 회차 ②]** 등록 R §13-3 B2-Q1 (위조 한정) 을 요청서에 옮기는 일은 메인 몫입니다.
5. **[kgy] 메모리** — `free -g` 출력을 받은 뒤 판단은 1저자 몫입니다 (문턱 숫자 등록 없음).
