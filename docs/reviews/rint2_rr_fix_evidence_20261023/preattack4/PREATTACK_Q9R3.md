# 사전 공격 리뷰 4 회차 — Q9 설계 개정 3 + 10-24 결정 (`4040e4388`) · 비교 기준 개정 2 (`9a72d65c6`)
결론: **P1 0 · P2 4 · P3 9 · 질문 5** · 3 회차 발견 26 (P2 5 · P3 15 · 질문 6) = **닫힘 22 · 부분 4 · 열림 0**

- 읽은 것: 설계 `git show 4040e4388:…/q9_predict_units_design.md` (줄 번호 = 그 파일) · diff `9a72d65c6..4040e4388` · 3 회차 보고 §A–§D (메인 메모 절 안 읽음) · `scripts/rint_r_chain.py` · `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/mpm_webapp_payload.py` · `scripts/step3_sigma.py` · `scripts/step3_conv_cert.py` · `scripts/run_contract.py` (전부 `4040e4388`) · `q9_time_budget.{py,json}` · 등록 R · 수정 계획 Q2–Q4.  안 읽은 것: `REPORT_A*` · `BRIEF*` · 진행 기록 10-23 · 10-24 줄 · py38 증거 README.
- 탐침 = 사본 트리 (`git archive 4040e4388`) 의 실제 `Predict` · `judge` · `sig3` 등 + 가짜 fetch · CPU · 리포 무수정 (§E).  "L<n>" = 설계 줄.

## A. 발견

| ID | 등급 | 보장 (문서 줄) | 반례 (손으로 따라가기) | 고칠 길 / 문장 줄이기 |
|---|---|---|---|---|
| R4-01 | **P2** | L141 *"원장은 결과를 본 뒤 배정을 고르는 길을 막는다"* · L134 *"(결과를 본 뒤가 아니므로 고르기는 아니다)"* · Q-G (L207) 의 전제 | ① 단위 U(c1,P0,R_j_lo) 를 원장 밖에서 kgy · gabia 둘 다 돌린다 (L134 가 *"못 막는 것"* 으로 인정한 그림자 런). ② 두 σ 가 4.68 × (1 ∓ 2e-10) mS/cm 이면 `judge` = **FAIL ↔ PASS_INFORMATIVE** (탐침 knife (1)). ③ 고른 기계로 원장 #1 하나만 커밋 · 실행 → 결정적이라 그림자와 같은 비트 → 첫 시도 = 채택. 차례 · 시작 sha · 접두 · ATTEMPT_AFTER_ADOPTED 전부 통과 · 파일 편집 없음. ⇒ L134 의 "미리 볼 수 있다" 가 곧 "기계를 고를 수 있다" — L134 ↔ L141 모순 | 문장: *"원장은 원장에 적힌 시도끼리 결과를 본 뒤 고르는 것만 막는다. 원장 밖 그림자 런 (어느 기계든) 으로 결과를 본 뒤 첫 시도의 기계를 고르는 것은 막지 못한다 (배정 비봉인의 대가 · 칼날에서만 뜻)"* · L134 괄호 삭제 · Q-D · Q-G 문구 · 질문 D1 |
| R4-02 | **P2** | L119 결과 전 = 시도 폴더 (`.unchecked/` 포함) payload 0 + 원인 ∈ {풀기 전 거부 · 신호 9 · CUDA OOM} · L134 *"좁은 틈"* | payload 는 시도 폴더 밖 `$RUN` (킷 런 폴더) 에서 만들어지고 검사 통과 뒤에야 옮겨진다 (러너 L855 · L868 · L880 · payload L3872–3893). 사슬은 러너 bash PID 만 죽인다 (`rint_r_chain.py` L1531–1533 `subprocess.run(timeout=)`). 반례: #1 (U · kgy) 런 1 풀이 중 러너 bash 에 `kill -9` → 사슬이 본 rc **−9** = 신호 9 · 시도 폴더 payload **0** → 결과 전. 그런데 payload 프로세스는 고아로 살아 **3 s 뒤 `$RUN/p2_…json` 에 σ** (탐침 orphan K · 러너 구조 흉내 · GPU 없음). `--max-hours` 초과도 같은 고아를 남긴다 (탐침 T · 분류는 R4-09 ①). σ 를 읽고 #2 를 gabia 로 → 채택 (탐침 S6 = PREDICTED). L126 은 스스로 "킷 런 폴더" 를 payload 자리로 적는데 L119 만 그 자리를 안 본다. 덤: 고아가 GPU 를 계속 잡아 다음 단위가 CUDA OOM 날 수 있다 | ① 러너가 payload (`.part` · `.failed` 포함) 를 처음부터 시도 폴더 안 (예 `$OUTDIR/.unchecked/`) 에 쓰고 검사 뒤 올린다 ② 사슬은 멈출 때 러너 프로세스 그룹 전체를 죽인다 (`start_new_session` + `killpg`) ③ §8 시험 (러너 SIGKILL · 시간 초과 · 검사 중 사망) ④ L134 정정 · 질문 D2 |
| R4-03 | **P2** | L105 *"채택 뒤 시도는 생길 이유가 없다"* · L62 *"(풀기 전 거부) 다시 할 수 있다"* · L93 · L187 *"gabia = kgy 판으로 맞춘다"* | 10-24 ① 이 늦게 드러난 실수를 되돌릴 수 없게 만든다 (셋 다 = 등록 판정 없음): **(a)** 채택된 단위를 실수로 다시 시작 — 풀기 전 대조의 "원장 차례" 는 앞 항목 결과 줄만 보므로 #1 완주 · 결과 줄 뒤 #2 시작을 막지 않는다 (L112 · L62) → 합치기 ATTEMPT_AFTER_ADOPTED (개정 2 = "처음 완주 채택" 만 · #2 처분 없음 = 사실상 무시). **(b)** gabia venv 가 numpy 1.24.3 · 원장 항목에 그 지문 커밋 → 풀기 전 대조 = "항목 지문 = 지금" 이라 통과 → 완주 · 채택 → 합치기의 판 같음 (L92 · L102) 실패 → 바른 venv 로 다시 = ATTEMPT_AFTER_ADOPTED (탐침 S5 · S5b: 어느 길도 PREDICTED 없음 · 사다리를 그 venv 에서 돌렸으면 수정 계획 Q4 "결과 뒤 = 같은 등록의 재시도 아님" 으로 같은 꼴). **(c)** 재실행 항목이 풀기 전 거부 (스레드 env 하나 다름) 된 뒤 바른 재실행 — 거부된 항목이 "재실행 사슬" (L129) 에 드는지 미정: 읽기 A = ATTEMPT_AFTER_ADOPTED · STOPPED / 읽기 B = PREDICTED (탐침 S3) | 풀기 전 대조에 더함: ① 계획에 봉인한 python · numpy · scipy 판 (단위 = D3) ② 같은 단위에 결과 전이 아닌 앞 항목이 있으면 거부 (그 시도를 가리키는 재실행 항목만 예외) → 결과 전 ③ 재실행 사슬 = 원 시도를 가리키는 재실행 항목 전부 (풀기 전 거부된 것은 건너뜀) · L105 근거 문장 정정 · §8 시험 셋 |
| R4-04 | **P2** | L123 재실행 조건 *"(… 러너 멈춤 기록 없음 …) 이 첫 payload 뒤에 나면 (= 폴더 판정상 결과 뒤)"* ↔ L128 *"러너 멈춤 기록이 없는 시도 = 같은 기계 · 환경 = 재실행"* · L119 | 정전 · 컨테이너 재시작이 #1 의 **첫 런 중** 에 남 → payload 0 · 러너 기록 0. L119: 기록이 없으니 결과 전 아님 → 결과 뒤 → #1 채택. L123: 첫 payload 앞이라 재실행 불가 → 단위 멈춤 → 등록 판정 없음. L128: 기록 없는 시도 = 같은 기계 재실행 → 계속. 같은 사건에 두 답 (탐침 S4: L123 = STOPPED · L128 = PREDICTED). "(= 폴더 판정상 결과 뒤)" 등식이 이 꼴에서 깨진다 · §8 에 이 꼴 시험 없음 | 한 문장: *"결과 뒤로 친 자원 · 인프라 멈춤 (러너 기록 없음 포함) 은 첫 payload 앞뒤 무관하게 같은 기계 · 환경에서 멈춘 런부터 재실행"* (L128 쪽) · §8 시험 |
| R4-05 | P3 | L135–L136 · L186 · Q-H *"명목값을 문턱과 비교하는 자리 전부"* | 개정 3 은 사다리 둘을 두 기계에 나누는 꼴을 승인 (L58 · L171 · L196) — 사다리의 문턱 비교도 배정을 따른다 (탐침 knife (2), 2e-10 차): R_j,0 = `sig3(interp_lnln)` (L1750) 유효숫자 3 자리 경계 → **1.23e6 ↔ 1.24e6 (0.81 %)** · 확인 런 `abs(s0/T − 1) ≤ 0.02` (L1754 · 보호 띠 없음) → 통과 ↔ 실패 · SBE origin ≤ 0.02 (L501–504 → 차단 표지 CALIB_ORIGIN_SENSITIVE) → 통과 ↔ 실패 · 바닥 ≤ T ≤ 천장. 사다리 시도 · 배정은 원장 밖 (L109 항목 = 단위 \| 넘침 점 \| 재실행) — 개정 3 이 no-op 도 거기로 옮겼다 · 판정문 RCA2-05 · §8 (멈춘 단계 재실행 · `CALIB_LADDER_EXHAUSTED` 예) 은 사다리 시도도 봉인 범위로 본다 — 이 문서는 사다리 시도가 어디서 봉인되는지 안 적는다 | "전부" 를 "예측 단계" 로 한정 + 사다리 칼날 · 사다리 시도가 원장 밖이라는 한정 (§3-5 · §7 · Q-H) · 또는 사다리도 원장에 (질문 D5) |
| R4-06 | P3 | L84 · L197 *"넘침 없는 꼴은 지금 코드와 요청 런 · 순서 · 판정 · `checks` 칸이 같다"* · L16 · L44 · L69 | no-op 을 사다리로 옮긴 것 (L31) 이 나머지에 안 퍼졌다: (a) 지금 코드는 예측 첫 두 런이 `sbe_noop` (L1832) → 개정 3 예측 = 런 26 → 24 · 이름 `P01…` 두 칸 밀림 · `checks['sbe_noop']` 출처 바뀜 · 사다리 `runs` +1 → "같다" 거짓 (b) L44 "런 18 · 24" · L69 "런 5 · 14" = no-op 2 런을 센 옛 코드 숫자 (개정 3 틀 = 16 · 22 · 3 · 12 — 탐침 S1: dbe 런 12 / no-op 포함 14) (c) 판정 단계 `_replay_ladder` 가 no-op 런을 다시 읽지 않으면 `rp.done()` (L2238) = REPLAY_MISMATCH · `predict_of` (L2518) 도 바뀜 — §7 에 판정 단계 변경 없음 (d) no-op NOT_COMPUTED → 사다리 status NOT_COMPUTED (L2050 · L173–175 `REGISTERED_OUTCOMES` = CALIB_ORDER) = 보정된 사다리가 "보정 NOT_COMPUTED" 로 보고 (판정 이름은 같음) — L16 · §4 · §7 의 "우선순위 둘" 밖 (e) 사다리엔 재실행이 없다 → 끝에 붙은 no-op 런의 자원 · 시간 멈춤 = 사다리 전체 잃음 (개정 2 = 따로 다시 하던 단위) (f) `q9_time_budget.py` 는 '2 대 · 지금 사슬' 예측 기계에 no-op 2 런 (개정 3 = 1 · 차 ≈ 1.2–1.5 h · 추정) | (a) 문장 = "DBE 런 · 순서 · 판정 같음 · no-op 두 런은 사다리로 (런 수 −2 · 이름 바뀜)" · §8 끈 경로 기준 = "지금 코드에서 no-op 두 런을 뺀 꼴" (b) 숫자 고침 (c)–(e) §4 · §7 에 적기 |
| R4-07 | P3 | L113 *"합치기는 그 커밋에 … 앞 항목들의 결과 줄이 모두 있는지 본다"* | 곁가지 커밋 S (원장에 #1 결과 줄 자리표) 에서 #2 를 먼저 시작 → 글자대로의 대조 통과 · S 는 main 의 조상 아님 · S 의 원장은 합칠 원장의 접두 아님 (탐침 ledger: literal **true** · prefix **false** · ancestor **false**). 얻는 것은 ATTEMPT_AFTER_ADOPTED 덕에 거부권 {#2 채택 \| STOPPED} 뿐 (σ 두 개 중 고르기 아님) | "시작 커밋의 원장 = 합칠 원장의 바이트 접두 (= 조상)" · 합치기 입력에 원장 git (파일 하나로는 커밋 대조 불가) · §8 시험 |
| R4-08 | P3 | L123–L127 재실행 · L80 UNIT_EXTRA | (a) L126 "킷 런 폴더" 에 남은 payload 는 재실행 자신의 같은 이름 쓰기 (`$RUN/<TAG>.json` · payload L3893 `os.replace`) 가 먼저 덮어 대조 불가 (b) 재실행이 대신한 원 시도의 멈춘 런 폴더 (부분 payload) 가 L80 "남는 런 = UNIT_EXTRA" 로 세어질 수 있음 (c) 자격 없는 재실행 (불수렴 · 검사 거부 뒤) 의 멈춤 이름 없음 (§7 · §8 은 시험만) (d) 재실행 조건 "같은 환경 지문" 이 L57 의 기록 전용 칸 (CPU 모델 · GPU 이름 · CUDA 판) 까지인지 미정 — 재실행이 겨냥한 사고 (재시작 · 정전) 뒤 클라우드 VM 이 다른 호스트 · 드라이버로 오면 재실행 불가 → 등록 판정 없음 | (a) 재실행은 돌기 전에 `$RUN/<TAG>*` 를 해시 · 시도 폴더로 옮긴다 (b) "대신한 원 시도 런 = UNIT_EXTRA 아님 (RESUME 대조 대상)" (c) 이름 하나 (d) 재실행 조건 칸 목록 |
| R4-09 | P3 | L119–L122 원인 목록 · Q-K | 목록 밖 = "만" 규칙으로 결과 뒤 (그 단위 끝): ① TIME_LIMIT (L81) 분류 없음 — `subprocess.run` 시간 초과는 bash 에 SIGKILL 이라 "신호 9" 로 적히면 결과 전 (R4-02 고아 σ 와 겹침) ② 러너 · payload 의 풀기 전 실패 (러너 ABORT exit 2 · "압밀 런 없음" 러너 L698 · payload ImportError = gabia 새 venv 에 cupy 없음 (10-24 ②) · 영수증 조립 실패) 는 사슬의 "풀기 전 대조" (L62) 밖 ③ ENOSPC ④ "러너" = L119 사슬 부모 · L122 bash 러너 두 뜻 | Q-K 목록에 ①–③ · 원인 기록 주체 한 이름 · (질문 D2) |
| R4-10 | P3 | L93 · L187 · Q-E *"Python 3.8.10 … gabia 도 같은 판"* | 판의 단위 없음: 게이트 `check_kgy_py38.sh` = `want = ((3, 8), '1.24.4', '1.10.1')` (부 판 무시) · 재현 = `uv python install 3.8` (`setup_kgy_py38.sh`) · venv 는 인터프리터 판을 못 바꾼다. v100 (Q11 허용 기계 · §6 "3 대") 판 규칙 없음 | 단위 · v100 정하기 (질문 D3) |
| R4-11 | P3 | L77 *"첫 · 끝 합치기와 판정 = 같은 기계 · 같은 환경 지문 · 다르면 멈춤"* · L106 | 다른 플랫폼 (Codex Windows — RCA-07 이 Windows ↔ Linux 차를 이미 보임) 의 `--reverify` 는 늘 UNIT_PROVENANCE_MISMATCH = 제3자 다시 판정 불가 · 컨테이너 (재시작 때 CPU 모델이 바뀔 수 있음) 에서 첫 합치기를 하면 끝 합치기가 막힘 — 한정 · 합치기 기계 지정 없음 | 한정 문장 + 합치기 · 판정 기계 = 계획에 정한 한 대 · 또는 대조 = 넘침 목록 · 시도 sha (질문 D4) |
| R4-12 | P3 | L58 · L171 · L196 *"'2 대 · 지금 사슬' 이 이제 그대로 돈다"* | 지금 `code_key` 에 러너 절대 경로 (`runner_path` L1115) → 두 기계 체크아웃 경로가 다르면 `load_ladders` CODE_PIN_MISMATCH (L2105 · 등록 R L515 *"기계마다 경로가 다르면 멈춘다"*). 개정 3 은 §3-3 (L90) 의 "묶음 B 에서 상대 경로로" 꼬리를 지웠다 | "묶음 B (상대 경로 키) 뒤" 조건을 다시 적기 |
| R4-13 | P3 | 문구 | L18 "(정하는 것으로 옮김)" ↔ L13 목록에 ATTEMPT_AFTER_ADOPTED 없음 · 거부 기록만 있는 시도 (옆자리 `.rejected.json`) 의 "폴더 요약 sha" (L111) 정의 없음 · 이미 결과 줄 있는 항목을 다시 부르면 거부 기록이 그 항목의 둘째 결과가 되는지 미정 · L78 `R01_corner` (예측 Runner prefix = 'P' · L2177) · `q9_time_budget.json` `overflow_note` 는 아직 "≈ +87 h (×6.05)" | 문구 정리 |

## B. 깨지 못한 보장

| 보장 | 시도 | 결과 |
|---|---|---|
| 부분 채택 = 한 기계 사슬과 같은 상태 · 같은 런 수 (L68 · L148) | 3 회차 반례 (A origin NOT_COMPUTED · B corner ARM_CONTRACT) · 재실행 사슬 (탐침 S1 · S2) | 성립 — S1 사슬 = 합치기 STOPPED · ARM_CONTRACT · DBE 런 12 · S2 PREDICTED 24 = 24 (거부된 재실행 · 첫 런 사망은 R4-03 · R4-04 별건) |
| same_p 칼날 아님 (L140) | ⓓ = 정확 분수 `max(hi − G, G − lo) ≤ τ·G` (`step3_conv_cert.py` L587–617 · τ = 1e-4 L78) → σ* ∈ [σ(1−e), σ(1+e)] → d ≥ ln((1−1e-4)/(1+1e-4)) ≈ −2.0e-4 > −1e-3 | 못 깸 |
| R 단조 칼날 아님 (L138) | 같은 origin 세 R = 같은 래스터 (SID_GRID) · Rayleigh 단조 · 증서 구간이 참값을 품음 · 비교 = 정확 분수 (`r_monotone_problem`) | 못 깸 (증서 유효 조건부) |
| 넘침 없는 꼴의 `checks['r_monotone']` = 지금 코드 (L73) | 이른 점 = 끝 점 · 순서 법칙 → c → 최종 추정량 → origin (`_r_monotone` L1882–) · 3 회차 S0b 의 차이를 L73 이 같은 칸으로 고침 | 못 깸 (no-op 이동의 다른 차이 = R4-06) |
| 합친 런 이름 = 사슬 요청 순서 이름 (L78) | `cert_reg` 키 `<폴더>/<이름>` (L1578) · 폴더는 `outdir` 로 따로 (`self.dir / outdir`) | 못 깸 |
| 우선순위 바뀜 = 둘 (예측 단계 안 · L44) | 새 순서 ①→②→③→④ ↔ 지금 순서 짝짓기: 바뀌는 쌍 = ⓐ 이른 단조 > origin8 멈춤 · ⓑ 뒤 모서리 origin 표본 > 앞 모서리 origin8 | 못 깸 (no-op 단계 귀속은 R4-06 (d)) |
| 넘침 86.7 – 104.9 h (L173) | 24 × 2,578 s × 5.0446 · 6.1018 = 86.70 · 104.87 h · 배수 = 1 + 0.80091 × (6.05 · 7.37 − 1) 다시 셈 같음 · `q9_time_budget.py` 다시 돌림 = JSON 내용 같음 (탐침 overflow) | 맞음 |
| 재실행 비트 같음이 가능한가 (L126) | payload 에 시각 · pid · 경로 칸 없음 (`time.time()` 은 print 에만 · 난수 seed 고정 — grep) | 못 깸 (GPU 결정성 = 추정) |
| no-op 같은 프로세스 = 같은 환경 (L31 · L53) | 사다리 확인 팔과 no-op 둘 다 한 사슬 부모 (`Runner.env_base`) 의 자식 | 못 깸 (GPU 결정성 가정) |
| 칼날 목록 (예측 단계 안) | `dbe_origin_ok` · `judge` · `grade_W` · 증서 · `conv_ok` · `sv_assess` 의 문턱 비교 전부 목록에 있음 · 상태 다름 · PTFE 셀 0 = 위상 (결정적) | 못 깸 (사다리 = R4-05) |
| 원장 안 동시 시도로 σ 둘 중 고르기 | 곁가지 우회 (R4-07) 까지 써도 ATTEMPT_AFTER_ADOPTED 때문에 {채택 \| STOPPED} 뿐 (탐침 ledger 결과표) | 못 깸 (원장 밖은 R4-01) |

## C. 3 회차 발견 상태 (PREATTACK_Q9R2 §A · §D)

| 3 회차 | 개정 3 처리 | 판정 | 근거 |
|---|---|---|---|
| P2 lazy 대조 + 둘째 런 멈춤 | 부분 채택 (L68–69) | **닫힘** | 탐침 S1 |
| P2 payload 시도 폴더 밖 · RUNNER_RC 분류 | 원인 목록 · `.unchecked/` (L119–122) | **부분** | payload 는 여전히 `$RUN` 에서 생김 · 고아 → R4-02 · TIME_LIMIT 등 → R4-09 |
| P2 원장 순서 ≠ 시작 순서 · 동시 · 일부러 낸 결과 전 | 차례 · 시작 sha · 접두 · 한정 (L112–115 · L134) | **부분** | 원장 안 = 거부권으로 줄음 · 조상 대조 없음 R4-07 · 그림자 런 선택 R4-01 |
| P2 칼날 목록 · §3-3 괄호 | 목록 넓힘 · 괄호 정정 (L95 · L135–141) | **닫힘** | 예측 단계 범위 (사다리 = R4-05) |
| P2 막다른 길 | 풀기 전 대조 · 거부 기록 · no-op 이동 | **부분** | 원 반례 셋 닫힘 · 새 막다른 길 R4-03 · R4-04 |
| P3 순서 ① 우선순위 | L44 · L147 · L184 | 닫힘 | — |
| P3 넘침 없는 꼴 `checks` | L73 같은 칸 | 닫힘 | no-op 이동이 "지금 코드와 같음" 을 다시 깸 (R4-06) |
| P3 런 이름 겹침 | L78 | 닫힘 | — |
| P3 §6 '2 대' 못 돎 | no-op 사다리로 | 닫힘 | 조건 R4-12 |
| P3 +87 h | 86.7–104.9 h | 닫힘 | §B |
| P3 원장 덧붙이기만 미검증 | 시작 sha · 접두 · 다른 체크아웃 | **부분** | R4-07 |
| P3 한 attempt 여럿 | 단수 (L52 · L61 · L82) | 닫힘 | — |
| P3 '채택 시도 둘' · 채택 뒤 처분 | ATTEMPT_AFTER_ADOPTED | 닫힘 | 새 문제 R4-03 |
| P3 다시 판정 자리 | 모든 시도 폴더 · 원장 사본 (L86) | 닫힘 | — |
| P3 시간 상한 뜻 | 실행마다 · 같음 한정 (L81 · L150) | 닫힘 | 분류 R4-09 |
| P3 W0 libm | 같은 환경 고정 (L77) | 닫힘 | 대가 R4-11 |
| P3 비용 문장 | L118 | 닫힘 | — |
| P3 §9 낡음 | §9 머리 · Q-A | 닫힘 | — |
| P3 SID_GRID 범위 | L158 · L196 | 닫힘 | — |
| P3 CPU · SIMD 칸 | L57 | 닫힘 | 대가 R4-08 (d) |
| 질문 1 재실행 | 결정 반영 (L123–128) | 닫힘 | 빈틈 R4-04 · R4-08 |
| 질문 2 폴더 없는 시도 | 결정 반영 (L118) | 닫힘 | R4-13 |
| 질문 3 차례 | 결정 반영 (L112–115) | 닫힘 | R4-07 |
| 질문 4 no-op | 결정 반영 (L31 · L53) | 닫힘 | R4-06 |
| 질문 5 칼날 문장 | 결정 반영 (L135–141) | 닫힘 | R4-05 |
| 질문 6 RUNNER_RC 원인 | 결정 반영 (L119–122) | 닫힘 | R4-02 · R4-09 |

## D. 질문 (1저자 몫 · 리뷰어는 고르지 않음)

1. **배정** — 비봉인 그대로 두고 *"그림자 런으로 첫 시도의 기계를 고를 수 있다"* 를 한정으로 적을지, 계획에 단위 ↔ 기계 배정을 봉인하고 다른 기계 이어받기를 "기계 소실" 에만 둘지 (봉인해도 일부러 낸 결과 전 멈춤으로 넘길 수 있어 완전히는 못 막음) (R4-01).
2. **결과 전 기준** — 원인 이름 목록 (10-24 ⑥) 그대로 + R4-02 고침, 또는 "풀이 끝 표지" (payload 프로세스가 σ 를 쓰기 전 시도 폴더에 남김 · 없으면 원인 무관 결과 전 · 있으면 결과 뒤) 로 바꿀지 — 후자면 TIME_LIMIT · 러너 사망 · ImportError 가 한 규칙 (R4-02 · R4-09).
3. **판 같음의 단위** — Python 3.8.10 정확 / 3.8 · v100 도 같은 판 요구 (R4-10).
4. **다시 판정** — 첫 합치기 환경에서만 (제3자 불가 · 합치기 기계 지정) / 결정 기록 대조를 구조 칸 (넘침 목록 · 시도 sha) 으로 · W0 끝자리 차 = 칼날 보고 (R4-11).
5. **사다리 단계 (no-op 포함) 의 시도 · 배정** — 이 원장에 넣을지 / 원장 밖 한정으로 둘지 (R4-05).

## E. 탐침 · 로그 (이 폴더)

| 탐침 | 로그 | 보는 것 |
|---|---|---|
| `probes/partial_adoption_r3_probe.py` (+ `probes/q9r3_lib.py`) | `logs/partial_adoption_r3_probe.out` | 실제 `Predict` + 개정 3 규칙 글자대로: S1 부분 채택 · S2 재실행 · S3 거부된 재실행 (읽기 A/B) · S4 첫 런 사망 (L123/L128) · S5 판 불일치 · S6 신호 9 뒤 다른 기계 |
| `probes/orphan_kill_probe.py` | `logs/orphan_kill_probe.out` | 러너 꼴 흉내 — 시간 초과 (T) · `kill -9` (K) 뒤 시도 폴더 payload [] · `$RUN` 에 3 s 뒤 payload · K 의 rc −9 |
| `probes/ledger_branch_probe.py` | `logs/ledger_branch_probe.out` | git 곁가지 커밋 — L113 글자 대조 true · 접두 false · 조상 false · 얻는 것 = 거부권 |
| `probes/knife_and_shadow_probe.py` | `logs/knife_and_shadow_probe.out` | 실제 `judge` FAIL ↔ PASS_INFORMATIVE (2e-10) · 사다리 `sig3` 1.23e6 ↔ 1.24e6 · 확인 0.02 · SBE origin 0.02 |
| `probes/overflow_hours.py` | `logs/overflow_hours.out` · `logs/q9_time_budget_rerun.txt` | 86.70 · 104.87 h · 배수 다시 셈 · 시간 스크립트 다시 돌림 (커밋 JSON 과 내용 같음) |

다시 돌리기 (작업 폴더 = 이 폴더):
```
mkdir -p tree work && git -C /home/user/Yonghoon-DEM-DFT archive 4040e4388 scripts docs/reviews/rint2_rr_fix_evidence_20261023 | tar -x -C tree
OPENBLAS_NUM_THREADS=1 nice -n 19 python3 -I -B probes/partial_adoption_r3_probe.py tree/scripts probes
OPENBLAS_NUM_THREADS=1 nice -n 19 python3 -I probes/orphan_kill_probe.py work
OPENBLAS_NUM_THREADS=1 nice -n 19 python3 -I probes/ledger_branch_probe.py work
OPENBLAS_NUM_THREADS=1 nice -n 19 python3 -I probes/knife_and_shadow_probe.py tree/scripts
python3 -I probes/overflow_hours.py tree/docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json
python3 -I tree/docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.py
```
